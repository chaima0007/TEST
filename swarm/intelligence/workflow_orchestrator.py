"""
Workflow Orchestrator — the top-level decision engine of the swarm.

Combines signals from all intelligence modules to decide:
  - Which agent division should act on a prospect (1–6)
  - What specific action to trigger
  - Why (transparent reasoning chain)
  - Priority order across all prospects

Decision inputs:
  - Funnel stage (lead → negotiating → won)
  - BANT qualification score (0–100)
  - Days since last contact
  - Last reply classification (objection type, buying signal)
  - Negotiation status (if any)
  - Number of touches

Decision outputs:
  - WorkflowDecision with agent_id, action, reasoning, confidence
  - Global queue sorted by urgency across all prospects
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


# ── Enums ─────────────────────────────────────────────────────────────────────

class DivisionTarget(str, Enum):
    DETECTION     = "1"   # Web scouting
    OUTREACH      = "2"   # Email / copywriting
    NEGOTIATION   = "3"   # Reply handling, objection, closing
    PRODUCTION    = "4"   # Deliverable creation
    FINANCE       = "5"   # Quote, invoice, payment
    BRANDING      = "6"   # Portfolio, memory, reporting


class WorkflowAction(str, Enum):
    SEND_FIRST_EMAIL     = "send_first_email"
    SEND_FOLLOWUP_EMAIL  = "send_followup_email"
    HANDLE_OBJECTION     = "handle_objection"
    SCHEDULE_DEMO        = "schedule_demo"
    SEND_QUOTE           = "send_quote"
    FOLLOW_UP_QUOTE      = "follow_up_quote"
    NEGOTIATE            = "negotiate"
    CLOSE                = "close"
    GENERATE_INVOICE     = "generate_invoice"
    ENRICH_PROSPECT      = "enrich_prospect"
    NURTURE              = "nurture"
    ARCHIVE              = "archive"
    ESCALATE             = "escalate"
    WAIT                 = "wait"


class DecisionConfidence(str, Enum):
    HIGH    = "high"     # > 0.75 — clear signals
    MEDIUM  = "medium"   # 0.50–0.75 — some ambiguity
    LOW     = "low"      # < 0.50 — weak signals


# ── Signal bundle ─────────────────────────────────────────────────────────────

@dataclass
class ProspectSignals:
    """All signals for a single prospect at decision time."""
    prospect_id:        str
    company_name:       str
    sector:             str = ""
    funnel_stage:       str = "lead"          # lead / contacted / replied / demo / quoted / negotiating / won / lost
    bant_score:         int = 0               # 0–100
    days_since_contact: float = 0.0
    touches:            int = 0
    buying_signal:      float = 0.0           # 0.0–1.0
    objection_type:     str = "none"          # price / trust / timing / competitor / technical / none
    negotiation_status: str = ""              # opened / in_progress / agreed / failed / abandoned / ""
    quote_sent:         bool = False
    invoice_sent:       bool = False
    is_lost:            bool = False


# ── Decision output ───────────────────────────────────────────────────────────

@dataclass
class WorkflowDecision:
    prospect_id:    str
    company_name:   str
    division:       DivisionTarget
    agent_id:       str                        # e.g. "3.5" = Division 3, Agent 5
    action:         WorkflowAction
    urgency_score:  int                        # 0–100
    confidence:     DecisionConfidence
    reasoning:      str
    signals_used:   List[str] = field(default_factory=list)
    created_at:     datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "prospect_id":   self.prospect_id,
            "company_name":  self.company_name,
            "division":      self.division.value,
            "agent_id":      self.agent_id,
            "action":        self.action.value,
            "urgency_score": self.urgency_score,
            "confidence":    self.confidence.value,
            "reasoning":     self.reasoning,
            "signals_used":  self.signals_used,
            "created_at":    self.created_at.isoformat(),
        }


# ── Rule helpers ──────────────────────────────────────────────────────────────

def _urgency(signals: ProspectSignals) -> int:
    """Lightweight urgency scorer for queue ordering."""
    from intelligence.followup_scheduler import (
        _recency_urgency, _bant_urgency, _touches_penalty, _STAGE_URGENCY,
    )
    raw = (
        _recency_urgency(signals.days_since_contact)
        + _STAGE_URGENCY.get(signals.funnel_stage, 0)
        + _bant_urgency(signals.bant_score)
        + _touches_penalty(signals.touches)
        + round(signals.buying_signal * 10)  # 0–10 bonus for buying signal
    )
    return max(0, min(100, raw))


def _confidence(signals: ProspectSignals, clear_rule: bool) -> DecisionConfidence:
    if clear_rule and signals.bant_score >= 50:
        return DecisionConfidence.HIGH
    if clear_rule:
        return DecisionConfidence.MEDIUM
    return DecisionConfidence.LOW


# ── Orchestrator ──────────────────────────────────────────────────────────────

class WorkflowOrchestrator:
    """
    Decides the next agent action for a prospect based on all available signals.

    Rule priority (first match wins):
      1. Lost / opted-out → Archive
      2. Won → Generate invoice or close
      3. Negotiating → Continue or escalate
      4. Quoted → Follow-up on quote
      5. Demo stage → Schedule or confirm demo
      6. Has replied with buying signal → Fast-close path
      7. Has replied with objection → Handle objection
      8. Replied (no clear signal) → Nurture/call
      9. First contact or opened → Follow-up email
     10. Lead with low BANT → Enrich prospect
     11. Default → Wait
    """

    def __init__(self) -> None:
        self._decisions: Dict[str, WorkflowDecision] = {}

    # ── Main decision engine ──────────────────────────────────────────────────

    def decide(self, signals: ProspectSignals, ts: Optional[datetime] = None) -> WorkflowDecision:
        """Evaluate signals and produce a WorkflowDecision."""
        score = _urgency(signals)
        decision = self._apply_rules(signals, score, ts)
        self._decisions[signals.prospect_id] = decision
        return decision

    def _apply_rules(
        self,
        s: ProspectSignals,
        score: int,
        ts: Optional[datetime],
    ) -> WorkflowDecision:
        ts = ts or datetime.utcnow()

        def make(
            division: DivisionTarget,
            agent_id: str,
            action: WorkflowAction,
            reasoning: str,
            signals_used: List[str],
            confidence: DecisionConfidence = DecisionConfidence.HIGH,
        ) -> WorkflowDecision:
            return WorkflowDecision(
                prospect_id=s.prospect_id,
                company_name=s.company_name,
                division=division,
                agent_id=agent_id,
                action=action,
                urgency_score=score,
                confidence=confidence,
                reasoning=reasoning,
                signals_used=signals_used,
                created_at=ts,
            )

        # Rule 1 — Lost / opted-out
        if s.is_lost or s.funnel_stage == "lost":
            return make(
                DivisionTarget.BRANDING, "6.9",
                WorkflowAction.ARCHIVE,
                "Prospect marqué perdu ou désinscrit. Archivage et mise à jour de la mémoire.",
                ["is_lost", "funnel_stage"],
            )

        # Rule 2 — Won prospect: generate invoice
        if s.funnel_stage == "won":
            if not s.invoice_sent:
                return make(
                    DivisionTarget.FINANCE, "5.1",
                    WorkflowAction.GENERATE_INVOICE,
                    "Prospect gagné — génération de la facture via l'agent Finance 5.1.",
                    ["funnel_stage"],
                )
            return make(
                DivisionTarget.PRODUCTION, "4.0",
                WorkflowAction.CLOSE,
                "Facture envoyée — lancement de la production par Division 4.",
                ["funnel_stage", "invoice_sent"],
            )

        # Rule 3 — Negotiating
        if s.funnel_stage == "negotiating" or s.negotiation_status in ("opened", "in_progress"):
            if s.negotiation_status == "failed":
                return make(
                    DivisionTarget.NEGOTIATION, "3.3",
                    WorkflowAction.NURTURE,
                    "Négociation échouée — Agent 3.3 lance une séquence d'empathie post-refus.",
                    ["negotiation_status"],
                    confidence=DecisionConfidence.MEDIUM,
                )
            if s.buying_signal >= 0.5:
                return make(
                    DivisionTarget.NEGOTIATION, "3.5",
                    WorkflowAction.CLOSE,
                    f"Signal d'achat fort ({s.buying_signal:.0%}) en cours de négociation — closing immédiat.",
                    ["funnel_stage", "buying_signal"],
                )
            return make(
                DivisionTarget.NEGOTIATION, "3.0",
                WorkflowAction.NEGOTIATE,
                "Prospect en négociation — agent Manager Division 3 coordonne l'offre.",
                ["funnel_stage", "negotiation_status"],
            )

        # Rule 4 — Quote sent, follow-up needed
        if s.funnel_stage == "quoted" or s.quote_sent:
            if s.days_since_contact >= 14:
                return make(
                    DivisionTarget.NEGOTIATION, "3.5",
                    WorkflowAction.FOLLOW_UP_QUOTE,
                    f"Devis sans réponse depuis {s.days_since_contact:.0f}j — relance urgente Agent 3.5.",
                    ["funnel_stage", "days_since_contact"],
                    confidence=DecisionConfidence.HIGH,
                )
            if s.days_since_contact >= 5:
                return make(
                    DivisionTarget.OUTREACH, "2.5",
                    WorkflowAction.FOLLOW_UP_QUOTE,
                    f"Relance devis J+{s.days_since_contact:.0f} via Agent 2.5 (email personnalisé).",
                    ["funnel_stage", "days_since_contact"],
                )
            return make(
                DivisionTarget.OUTREACH, "2.5",
                WorkflowAction.WAIT,
                "Devis récent — attente de réponse (< 5 jours).",
                ["funnel_stage", "days_since_contact"],
                confidence=DecisionConfidence.MEDIUM,
            )

        # Rule 5 — Demo stage
        if s.funnel_stage == "demo":
            return make(
                DivisionTarget.NEGOTIATION, "3.4",
                WorkflowAction.SCHEDULE_DEMO,
                "Prospect en phase démo — Agent 3.4 planifie ou confirme la démonstration.",
                ["funnel_stage"],
            )

        # Rule 6 — Replied with strong buying signal
        if s.funnel_stage == "replied" and s.buying_signal >= 0.5:
            if s.bant_score >= 75:
                return make(
                    DivisionTarget.FINANCE, "5.2",
                    WorkflowAction.SEND_QUOTE,
                    f"Prospect chaud (BANT {s.bant_score}, signal {s.buying_signal:.0%}) — envoi devis via Agent 5.2.",
                    ["funnel_stage", "buying_signal", "bant_score"],
                )
            return make(
                DivisionTarget.NEGOTIATION, "3.5",
                WorkflowAction.SCHEDULE_DEMO,
                f"Intérêt confirmé (signal {s.buying_signal:.0%}) mais BANT {s.bant_score} — démo de qualification.",
                ["buying_signal", "bant_score"],
                confidence=DecisionConfidence.MEDIUM,
            )

        # Rule 7 — Replied with objection
        if s.funnel_stage == "replied" and s.objection_type != "none":
            agent_map = {
                "price":      ("3.1", "Agent 3.1 — argumentation ROI et comparatif prix."),
                "trust":      ("3.2", "Agent 3.2 — envoi preuves sociales et audit gratuit."),
                "timing":     ("3.5", "Agent 3.5 — reframe coût du délai et effort minimal."),
                "competitor": ("3.1", "Agent 3.1 — email de différenciation concurrentielle."),
                "technical":  ("3.4", "Agent 3.4 — démo personnalisée + guide onboarding."),
            }
            agent_id, reason = agent_map.get(s.objection_type, ("3.0", "Agent 3.0 — traitement objection générique."))
            return make(
                DivisionTarget.NEGOTIATION, agent_id,
                WorkflowAction.HANDLE_OBJECTION,
                f"Objection '{s.objection_type}' détectée. {reason}",
                ["funnel_stage", "objection_type"],
            )

        # Rule 8 — Replied but no clear signal
        if s.funnel_stage == "replied":
            return make(
                DivisionTarget.OUTREACH, "2.3",
                WorkflowAction.SEND_FOLLOWUP_EMAIL,
                "Réponse reçue sans signal clair — Agent 2.3 envoie un email de qualification.",
                ["funnel_stage"],
                confidence=DecisionConfidence.MEDIUM,
            )

        # Rule 9 — Contacted or opened → follow-up
        if s.funnel_stage in ("contacted", "opened"):
            if s.days_since_contact >= 7:
                return make(
                    DivisionTarget.OUTREACH, "2.4",
                    WorkflowAction.SEND_FOLLOWUP_EMAIL,
                    f"Email ouvert/envoyé sans réponse depuis {s.days_since_contact:.0f}j — relance Agent 2.4.",
                    ["funnel_stage", "days_since_contact"],
                )
            return make(
                DivisionTarget.OUTREACH, "2.4",
                WorkflowAction.WAIT,
                f"Email récent ({s.days_since_contact:.0f}j) — attente de réponse.",
                ["funnel_stage", "days_since_contact"],
                confidence=DecisionConfidence.MEDIUM,
            )

        # Rule 10 — Lead with low BANT → enrich first
        if s.funnel_stage == "lead":
            if s.bant_score < 25:
                return make(
                    DivisionTarget.DETECTION, "1.5",
                    WorkflowAction.ENRICH_PROSPECT,
                    f"Nouveau lead avec BANT faible ({s.bant_score}) — Agent 1.5 enrichit le profil.",
                    ["funnel_stage", "bant_score"],
                    confidence=DecisionConfidence.MEDIUM,
                )
            return make(
                DivisionTarget.OUTREACH, "2.1",
                WorkflowAction.SEND_FIRST_EMAIL,
                f"Lead qualifié (BANT {s.bant_score}) — Agent 2.1 rédige le premier email personnalisé.",
                ["funnel_stage", "bant_score"],
            )

        # Default
        return make(
            DivisionTarget.OUTREACH, "2.0",
            WorkflowAction.WAIT,
            "Aucune règle déclenchée — monitoring passif par Agent 2.0.",
            [],
            confidence=DecisionConfidence.LOW,
        )

    # ── Batch ────────────────────────────────────────────────────────────────

    def decide_batch(
        self,
        signals_list: List[ProspectSignals],
        ts: Optional[datetime] = None,
    ) -> List[WorkflowDecision]:
        """Decide for multiple prospects; returns list sorted by urgency_score desc."""
        decisions = [self.decide(s, ts) for s in signals_list]
        decisions.sort(key=lambda d: d.urgency_score, reverse=True)
        return decisions

    # ── Getters ──────────────────────────────────────────────────────────────

    def get(self, prospect_id: str) -> Optional[WorkflowDecision]:
        return self._decisions.get(prospect_id)

    def get_queue(self, limit: Optional[int] = None) -> List[WorkflowDecision]:
        """Return all stored decisions sorted by urgency_score desc."""
        queue = sorted(self._decisions.values(), key=lambda d: d.urgency_score, reverse=True)
        return queue[:limit] if limit else queue

    def by_division(self, division: DivisionTarget) -> List[WorkflowDecision]:
        return [d for d in self._decisions.values() if d.division == division]

    def by_action(self, action: WorkflowAction) -> List[WorkflowDecision]:
        return [d for d in self._decisions.values() if d.action == action]

    def by_confidence(self, confidence: DecisionConfidence) -> List[WorkflowDecision]:
        return [d for d in self._decisions.values() if d.confidence == confidence]

    # ── Analytics ────────────────────────────────────────────────────────────

    def division_distribution(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for d in self._decisions.values():
            counts[d.division.value] = counts.get(d.division.value, 0) + 1
        return counts

    def action_distribution(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for d in self._decisions.values():
            counts[d.action.value] = counts.get(d.action.value, 0) + 1
        return counts

    def average_urgency(self) -> float:
        if not self._decisions:
            return 0.0
        return round(sum(d.urgency_score for d in self._decisions.values()) / len(self._decisions), 1)

    def confidence_distribution(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for d in self._decisions.values():
            counts[d.confidence.value] = counts.get(d.confidence.value, 0) + 1
        return counts

    def summary(self) -> dict:
        return {
            "total":                  len(self._decisions),
            "avg_urgency_score":      self.average_urgency(),
            "division_distribution":  self.division_distribution(),
            "action_distribution":    self.action_distribution(),
            "confidence_distribution": self.confidence_distribution(),
        }

    # ── Reset ────────────────────────────────────────────────────────────────

    def reset(self) -> None:
        self._decisions.clear()
