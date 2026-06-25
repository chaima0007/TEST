"""Module 26 — Deal Risk Analyzer."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class RiskLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class StallReason(str, Enum):
    NO_CHAMPION = "no_champion"
    SINGLE_THREADED = "single_threaded"
    BUDGET_FREEZE = "budget_freeze"
    COMPETITOR_THREAT = "competitor_threat"
    TECHNICAL_BLOCKER = "technical_blocker"
    EXECUTIVE_MISALIGNMENT = "executive_misalignment"
    PROCUREMENT_DELAY = "procurement_delay"
    SCOPE_CREEP = "scope_creep"


class DealAction(str, Enum):
    ACCELERATE = "accelerate"
    INTERVENE = "intervene"
    MONITOR = "monitor"
    ESCALATE = "escalate"
    ABANDON = "abandon"


class SalesStage(str, Enum):
    DISCOVERY = "discovery"
    QUALIFICATION = "qualification"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSING = "closing"


@dataclass
class DealProfile:
    deal_id: str
    account_name: str
    segment: str
    arr_eur: float
    stage: SalesStage
    days_in_stage: int               # days stuck in current stage
    expected_close_date_days: int    # days until expected close
    # People signals
    has_champion: bool
    champion_strength: float         # 0-10 (0 = no champion)
    stakeholder_count: int           # number of engaged stakeholders
    executive_sponsor: bool
    # Activity signals
    days_since_last_contact: int
    last_meeting_had_next_step: bool
    email_response_rate_pct: float   # 0-100
    # Deal health
    mutual_action_plan: bool
    legal_engaged: bool
    procurement_engaged: bool
    technical_validation_done: bool
    # Risk flags
    competitor_active: bool
    price_objection_raised: bool
    scope_changed: bool
    budget_confirmed: bool
    decision_criteria_agreed: bool
    # Forecast
    rep_confidence_pct: float        # rep's stated confidence 0-100


@dataclass
class DealRiskResult:
    deal_id: str
    account_name: str
    segment: str
    arr_eur: float
    stage: str
    risk_score: float              # 0-100 (higher = more risky)
    risk_level: RiskLevel
    deal_action: DealAction
    stall_reasons: list[str]
    risk_factors: list[str]
    positive_signals: list[str]
    intervention_plan: list[str]
    forecast_adjustment_pct: float  # suggested adjustment to rep confidence

    def to_dict(self) -> dict:
        return {
            "deal_id": self.deal_id,
            "account_name": self.account_name,
            "segment": self.segment,
            "arr_eur": self.arr_eur,
            "stage": self.stage,
            "risk_score": self.risk_score,
            "risk_level": self.risk_level.value,
            "deal_action": self.deal_action.value,
            "stall_reasons": self.stall_reasons,
            "risk_factors": self.risk_factors,
            "positive_signals": self.positive_signals,
            "intervention_plan": self.intervention_plan,
            "forecast_adjustment_pct": self.forecast_adjustment_pct,
        }


def _risk_score(deal: DealProfile) -> float:
    """Compute risk score 0-100 (higher = riskier)."""
    pts = 0.0

    # Stage stall: up to 25 pts
    stage_thresholds = {
        SalesStage.DISCOVERY: (14, 30),
        SalesStage.QUALIFICATION: (21, 45),
        SalesStage.PROPOSAL: (14, 28),
        SalesStage.NEGOTIATION: (10, 21),
        SalesStage.CLOSING: (7, 14),
    }
    warn, crit = stage_thresholds.get(deal.stage, (21, 45))
    if deal.days_in_stage >= crit:
        pts += 25
    elif deal.days_in_stage >= warn:
        pts += 14

    # People risk: up to 25 pts
    if not deal.has_champion:
        pts += 15
    elif deal.champion_strength < 5:
        pts += 8
    if deal.stakeholder_count <= 1:
        pts += 10
    elif deal.stakeholder_count == 2:
        pts += 4
    if not deal.executive_sponsor and deal.arr_eur >= 50000:
        pts += 5

    # Activity risk: up to 20 pts
    if deal.days_since_last_contact >= 14:
        pts += 12
    elif deal.days_since_last_contact >= 7:
        pts += 6
    if not deal.last_meeting_had_next_step:
        pts += 5
    if deal.email_response_rate_pct < 30:
        pts += 3

    # Process risk: up to 20 pts
    if not deal.mutual_action_plan:
        pts += 7
    if not deal.decision_criteria_agreed:
        pts += 6
    if not deal.budget_confirmed and deal.expected_close_date_days <= 60:
        pts += 7

    # Deal risk flags: up to 10 pts
    if deal.competitor_active:
        pts += 5
    if deal.scope_changed:
        pts += 3
    if deal.price_objection_raised and not deal.budget_confirmed:
        pts += 2

    return max(0.0, min(100.0, round(pts, 1)))


def _risk_level(score: float) -> RiskLevel:
    if score >= 65:
        return RiskLevel.CRITICAL
    if score >= 45:
        return RiskLevel.HIGH
    if score >= 25:
        return RiskLevel.MODERATE
    return RiskLevel.LOW


def _deal_action(risk: RiskLevel, deal: DealProfile) -> DealAction:
    if risk == RiskLevel.CRITICAL:
        if deal.days_since_last_contact >= 21 and not deal.has_champion:
            return DealAction.ABANDON
        return DealAction.ESCALATE
    if risk == RiskLevel.HIGH:
        return DealAction.INTERVENE
    if risk == RiskLevel.MODERATE:
        return DealAction.ACCELERATE
    return DealAction.MONITOR


def _stall_reasons(deal: DealProfile) -> list[str]:
    reasons: list[str] = []
    if not deal.has_champion:
        reasons.append(StallReason.NO_CHAMPION.value)
    if deal.stakeholder_count <= 1:
        reasons.append(StallReason.SINGLE_THREADED.value)
    if not deal.budget_confirmed and deal.expected_close_date_days <= 60:
        reasons.append(StallReason.BUDGET_FREEZE.value)
    if deal.competitor_active:
        reasons.append(StallReason.COMPETITOR_THREAT.value)
    if not deal.technical_validation_done and deal.stage in (SalesStage.NEGOTIATION, SalesStage.CLOSING):
        reasons.append(StallReason.TECHNICAL_BLOCKER.value)
    if not deal.executive_sponsor and deal.arr_eur >= 50000:
        reasons.append(StallReason.EXECUTIVE_MISALIGNMENT.value)
    if deal.procurement_engaged and not deal.legal_engaged and deal.stage == SalesStage.CLOSING:
        reasons.append(StallReason.PROCUREMENT_DELAY.value)
    if deal.scope_changed:
        reasons.append(StallReason.SCOPE_CREEP.value)
    return reasons


def _risk_factors(deal: DealProfile) -> list[str]:
    factors: list[str] = []
    stage_thresholds = {
        SalesStage.DISCOVERY: (14, 30),
        SalesStage.QUALIFICATION: (21, 45),
        SalesStage.PROPOSAL: (14, 28),
        SalesStage.NEGOTIATION: (10, 21),
        SalesStage.CLOSING: (7, 14),
    }
    warn, crit = stage_thresholds.get(deal.stage, (21, 45))
    if deal.days_in_stage >= crit:
        factors.append(f"Deal bloqué en {deal.stage.value} depuis {deal.days_in_stage}j — seuil critique dépassé")
    elif deal.days_in_stage >= warn:
        factors.append(f"Progression lente en {deal.stage.value} ({deal.days_in_stage}j) — risque de stagnation")
    if not deal.has_champion:
        factors.append("Aucun champion interne identifié — deal vulnérable à tout changement d'interlocuteur")
    elif deal.champion_strength < 5:
        factors.append(f"Champion faible ({deal.champion_strength}/10) — risque de perte d'influence interne")
    if deal.stakeholder_count <= 1:
        factors.append("Deal mono-thread — un seul interlocuteur actif, risque de blocage")
    if deal.days_since_last_contact >= 14:
        factors.append(f"Pas de contact depuis {deal.days_since_last_contact}j — deal potentiellement dormant")
    if not deal.last_meeting_had_next_step:
        factors.append("Dernière réunion sans prochaine étape définie — momentum perdu")
    if deal.competitor_active:
        factors.append("Concurrent actif sur le deal — risque de displacement")
    if not deal.budget_confirmed and deal.expected_close_date_days <= 60:
        factors.append("Budget non confirmé à moins de 60j de la close date — risque de report")
    if not deal.mutual_action_plan:
        factors.append("Pas de plan d'action mutuel — deal non structuré côté client")
    if deal.scope_changed:
        factors.append("Scope du deal modifié — risque de re-qualification et de retard")
    return factors


def _positive_signals(deal: DealProfile) -> list[str]:
    signals: list[str] = []
    if deal.has_champion and deal.champion_strength >= 7:
        signals.append(f"Champion fort ({deal.champion_strength}/10) — défenseur interne actif")
    if deal.stakeholder_count >= 4:
        signals.append(f"{deal.stakeholder_count} parties prenantes engagées — base de support large")
    elif deal.stakeholder_count >= 3:
        signals.append(f"{deal.stakeholder_count} parties prenantes actives — alignment multi-thread")
    if deal.executive_sponsor:
        signals.append("Sponsor exécutif engagé — décision facilitée")
    if deal.mutual_action_plan:
        signals.append("Plan d'action mutuel en place — deal bien structuré")
    if deal.legal_engaged:
        signals.append("Équipe légale engagée — progression vers la signature")
    if deal.technical_validation_done:
        signals.append("Validation technique complète — risque produit éliminé")
    if deal.budget_confirmed:
        signals.append("Budget confirmé — deal qualifié côté financement")
    if deal.decision_criteria_agreed:
        signals.append("Critères de décision alignés — processus d'évaluation transparent")
    if deal.last_meeting_had_next_step:
        signals.append("Prochaine étape définie — momentum maintenu")
    if deal.email_response_rate_pct >= 70:
        signals.append(f"Taux de réponse email élevé ({deal.email_response_rate_pct:.0f}%) — engagement actif")
    return signals


def _intervention_plan(deal: DealProfile, action: DealAction) -> list[str]:
    if action == DealAction.ABANDON:
        return [
            "Archiver le deal — critères d'abandon atteints",
            "Documenter les raisons d'abandon pour amélioration process",
            "Recycler dans une séquence nurture à 6 mois",
        ]
    if action == DealAction.ESCALATE:
        plan = ["Escalade C-level — mobiliser le management pour débloquer le deal"]
        if not deal.has_champion:
            plan.append("Identifier un champion interne en urgence — contacter 3 nouvelles personas")
        if deal.days_since_last_contact >= 14:
            plan.append("Reprendre contact immédiatement — appel direct sans email intermédiaire")
        plan.append("QBR de récupération — ROI, roadmap, valeur démontrée en réunion urgente")
        plan.append("Proposer un POC rapide ou une période de test pour relancer l'engagement")
        return plan
    if action == DealAction.INTERVENE:
        plan = []
        if deal.stakeholder_count <= 1:
            plan.append("Élargir le mapping relationnel — identifier et engager 2 nouveaux stakeholders")
        if not deal.mutual_action_plan:
            plan.append("Établir un plan d'action mutuel — cadrer les prochaines étapes avec le client")
        if deal.competitor_active:
            plan.append("Préparer un battlecard concurrentiel — différenciation et arguments ROI")
        if not deal.budget_confirmed:
            plan.append("Qualifier le budget en priorité — appel finance ou sponsor pour confirmation")
        plan.append("Fixer une deadline de décision avec le client — créer l'urgence")
        return plan
    if action == DealAction.ACCELERATE:
        return [
            "Accélérer la prochaine étape — réduire le cycle de décision",
            "Renforcer les preuves de valeur — étude de cas, démonstration ciblée",
            "Préparer la proposition commerciale finale",
            "Engager le sponsor exécutif pour validation finale",
        ]
    # MONITOR
    return [
        "Maintenir le cadence de contact hebdomadaire",
        "Tracker les jalons du plan d'action mutuel",
        "Mettre à jour le CRM après chaque interaction",
    ]


def _forecast_adjustment(deal: DealProfile, risk_score: float, risk: RiskLevel) -> float:
    """Suggest adjusting rep confidence down based on risk."""
    base_adj = 0.0
    if risk == RiskLevel.CRITICAL:
        base_adj = -35.0
    elif risk == RiskLevel.HIGH:
        base_adj = -20.0
    elif risk == RiskLevel.MODERATE:
        base_adj = -10.0
    # Additional adjustments
    if not deal.has_champion:
        base_adj -= 5.0
    if deal.stakeholder_count <= 1:
        base_adj -= 5.0
    if deal.competitor_active:
        base_adj -= 5.0
    if not deal.budget_confirmed:
        base_adj -= 5.0
    # Positive offset
    if deal.executive_sponsor:
        base_adj += 5.0
    if deal.mutual_action_plan and deal.decision_criteria_agreed:
        base_adj += 5.0
    return round(max(-60.0, min(0.0, base_adj)), 1)


class DealRiskAnalyzerEngine:
    """Analyzes deal risk and prescribes interventions."""

    def __init__(self) -> None:
        self._results: dict[str, DealRiskResult] = {}

    def analyze(self, deal: DealProfile) -> DealRiskResult:
        score = _risk_score(deal)
        risk = _risk_level(score)
        action = _deal_action(risk, deal)
        stalls = _stall_reasons(deal)
        factors = _risk_factors(deal)
        positives = _positive_signals(deal)
        plan = _intervention_plan(deal, action)
        forecast_adj = _forecast_adjustment(deal, score, risk)

        result = DealRiskResult(
            deal_id=deal.deal_id,
            account_name=deal.account_name,
            segment=deal.segment,
            arr_eur=deal.arr_eur,
            stage=deal.stage.value,
            risk_score=score,
            risk_level=risk,
            deal_action=action,
            stall_reasons=stalls,
            risk_factors=factors,
            positive_signals=positives,
            intervention_plan=plan,
            forecast_adjustment_pct=forecast_adj,
        )
        self._results[deal.deal_id] = result
        return result

    def analyze_batch(self, deals: list[DealProfile]) -> list[DealRiskResult]:
        results = [self.analyze(d) for d in deals]
        return sorted(results, key=lambda r: r.risk_score, reverse=True)

    # ── Read helpers ──────────────────────────────────────────────────────────

    def all_deals(self) -> list[DealRiskResult]:
        return sorted(self._results.values(), key=lambda r: r.risk_score, reverse=True)

    def by_risk(self, risk: RiskLevel) -> list[DealRiskResult]:
        return [r for r in self.all_deals() if r.risk_level == risk]

    def by_action(self, action: DealAction) -> list[DealRiskResult]:
        return [r for r in self.all_deals() if r.deal_action == action]

    def by_stage(self, stage: str) -> list[DealRiskResult]:
        return [r for r in self.all_deals() if r.stage == stage]

    def critical_deals(self) -> list[DealRiskResult]:
        return self.by_risk(RiskLevel.CRITICAL)

    def needs_escalation(self) -> list[DealRiskResult]:
        return self.by_action(DealAction.ESCALATE)

    def stalled_deals(self) -> list[DealRiskResult]:
        return [r for r in self.all_deals() if r.stall_reasons]

    def total_arr_at_risk_eur(self) -> float:
        return round(
            sum(
                r.arr_eur
                for r in self._results.values()
                if r.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL)
            ),
            2,
        )

    def avg_risk_score(self) -> float:
        deals = list(self._results.values())
        if not deals:
            return 0.0
        return round(sum(r.risk_score for r in deals) / len(deals), 1)

    def summary(self) -> dict:
        deals = list(self._results.values())
        n = len(deals)
        risk_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        stage_counts: dict[str, int] = {}
        stall_reason_counts: dict[str, int] = {}
        for r in deals:
            risk_counts[r.risk_level.value] = risk_counts.get(r.risk_level.value, 0) + 1
            action_counts[r.deal_action.value] = action_counts.get(r.deal_action.value, 0) + 1
            stage_counts[r.stage] = stage_counts.get(r.stage, 0) + 1
            for s in r.stall_reasons:
                stall_reason_counts[s] = stall_reason_counts.get(s, 0) + 1
        return {
            "total": n,
            "risk_counts": risk_counts,
            "action_counts": action_counts,
            "stage_counts": stage_counts,
            "top_stall_reasons": stall_reason_counts,
            "avg_risk_score": self.avg_risk_score(),
            "critical_count": len(self.critical_deals()),
            "escalation_count": len(self.needs_escalation()),
            "total_arr_at_risk_eur": self.total_arr_at_risk_eur(),
        }

    def reset(self) -> None:
        self._results.clear()
