"""Module 39 — Meeting Intelligence Engine

Analyses each sales meeting record to score its quality, detect buying signals
and objections, determine whether the deal advanced, and generate prioritised
follow-up recommendations for the rep and manager.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


# ─── Enums ────────────────────────────────────────────────────────────────────

class MeetingOutcome(str, Enum):
    ADVANCED    = "advanced"       # deal moved to next stage
    MAINTAINED  = "maintained"     # held ground — no regression, no advance
    REGRESSED   = "regressed"      # deal moved backward or stakeholder disengaged
    NO_DECISION = "no_decision"    # meeting ended without next step agreed


class MeetingQuality(str, Enum):
    EXCELLENT = "excellent"    # highly productive — multiple signals, next step set
    GOOD      = "good"         # solid meeting — one advance, clear next step
    AVERAGE   = "average"      # partial engagement — mixed signals
    POOR      = "poor"         # low engagement or missed objective


class BuyingSignalStrength(str, Enum):
    STRONG  = "strong"    # ≥3 positive signals
    MODERATE = "moderate" # 1–2 positive signals
    WEAK    = "weak"      # positive signals outweighed by objections
    NEGATIVE = "negative" # no positive signals or critical objections raised


class FollowUpUrgency(str, Enum):
    IMMEDIATE  = "immediate"   # follow-up within 24h required
    SAME_WEEK  = "same_week"   # follow-up within 5 business days
    STANDARD   = "standard"    # standard follow-up cycle (7–14 days)
    MONITOR    = "monitor"     # low urgency — nurture cadence


# ─── Input ───────────────────────────────────────────────────────────────────

@dataclass
class MeetingInput:
    meeting_id: str
    deal_id: str
    rep_id: str
    rep_name: str
    account_name: str
    meeting_type: str                     # "discovery" / "demo" / "proposal" / "negotiation" / "qbr" / "other"
    duration_minutes: int
    attendees_count: int
    decision_maker_present: bool
    exec_sponsor_present: bool
    # Engagement signals (from call notes / CRM)
    prospect_asked_questions: bool
    prospect_requested_pricing: bool
    prospect_mentioned_timeline: bool
    prospect_mentioned_budget: bool
    competitor_mentioned: bool
    objections_raised: int                # count of distinct objections
    next_step_agreed: bool
    next_step_days_out: Optional[int]     # days until agreed next step (None if not set)
    # Rep behaviour
    talk_ratio_pct: float                 # rep's share of talk time 0–100
    demo_shown: bool
    proposal_sent: bool
    references_offered: bool
    # Historical context
    previous_meetings_count: int          # meetings held before this one for same deal
    days_since_last_meeting: int


# ─── Output ──────────────────────────────────────────────────────────────────

@dataclass
class MeetingResult:
    meeting_id: str
    deal_id: str
    rep_id: str
    rep_name: str
    account_name: str
    meeting_type: str

    # Assessments
    meeting_outcome: MeetingOutcome
    meeting_quality: MeetingQuality
    buying_signal_strength: BuyingSignalStrength
    follow_up_urgency: FollowUpUrgency
    quality_score: float           # 0–100
    engagement_score: float        # 0–100 (prospect engagement only)
    buying_signals_count: int
    objections_count: int
    next_step_agreed: bool
    next_step_days_out: Optional[int]

    # Narrative
    positive_signals: list[str]
    concerns: list[str]
    follow_up_actions: list[str]
    manager_alerts: list[str]

    def to_dict(self) -> dict:
        return {
            "meeting_id": self.meeting_id,
            "deal_id": self.deal_id,
            "rep_id": self.rep_id,
            "rep_name": self.rep_name,
            "account_name": self.account_name,
            "meeting_type": self.meeting_type,
            "meeting_outcome": self.meeting_outcome.value,
            "meeting_quality": self.meeting_quality.value,
            "buying_signal_strength": self.buying_signal_strength.value,
            "follow_up_urgency": self.follow_up_urgency.value,
            "quality_score": self.quality_score,
            "engagement_score": self.engagement_score,
            "buying_signals_count": self.buying_signals_count,
            "objections_count": self.objections_count,
            "next_step_agreed": self.next_step_agreed,
            "next_step_days_out": self.next_step_days_out,
            "positive_signals": self.positive_signals,
            "concerns": self.concerns,
            "follow_up_actions": self.follow_up_actions,
            "manager_alerts": self.manager_alerts,
        }


# ─── Engine ──────────────────────────────────────────────────────────────────

class MeetingIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[MeetingResult] = []

    # ── helpers ────────────────────────────────────────────────────────────

    def _buying_signals_count(self, inp: MeetingInput) -> int:
        count = 0
        if inp.prospect_asked_questions:  count += 1
        if inp.prospect_requested_pricing: count += 1
        if inp.prospect_mentioned_timeline: count += 1
        if inp.prospect_mentioned_budget:  count += 1
        if inp.decision_maker_present:     count += 1
        if inp.exec_sponsor_present:       count += 1
        return count

    def _buying_signal_strength(self, signals: int, objections: int) -> BuyingSignalStrength:
        if signals == 0 and objections >= 1:
            return BuyingSignalStrength.NEGATIVE
        if signals >= 3 and objections <= 1:
            return BuyingSignalStrength.STRONG
        if signals >= 1 and signals > objections:
            return BuyingSignalStrength.MODERATE
        if signals >= 1 and signals <= objections:
            return BuyingSignalStrength.WEAK
        return BuyingSignalStrength.NEGATIVE

    def _engagement_score(self, inp: MeetingInput) -> float:
        """
        0–100 score reflecting prospect engagement:
          questions       20 pts
          pricing request 20 pts
          timeline        15 pts
          budget          15 pts
          DM present      15 pts
          exec sponsor     5 pts
          minus: objections −5 pts each (min 0 after deduction)
        """
        raw = (
            (20.0 if inp.prospect_asked_questions else 0.0)
            + (20.0 if inp.prospect_requested_pricing else 0.0)
            + (15.0 if inp.prospect_mentioned_timeline else 0.0)
            + (15.0 if inp.prospect_mentioned_budget else 0.0)
            + (15.0 if inp.decision_maker_present else 0.0)
            + (5.0 if inp.exec_sponsor_present else 0.0)
            - (inp.objections_raised * 5.0)
        )
        return round(min(100.0, max(0.0, raw)), 1)

    def _quality_score(self, inp: MeetingInput, engagement: float) -> float:
        """
        0–100 quality score:
          engagement component  40 pts  → engagement / 100 × 40
          next step             20 pts  → 20 if agreed, else 0; −10 if next_step_days_out > 14
          rep behaviour         25 pts:
            talk ratio ≤ 50%    10 pts  (rep listens more)
            demo shown           8 pts
            proposal sent        7 pts
          meeting logistics     15 pts:
            duration ≥ 30 min    5 pts
            duration ≥ 60 min    5 pts additional
            attendees ≥ 2        5 pts
        """
        eng_pts  = (engagement / 100.0) * 40.0

        next_pts = 0.0
        if inp.next_step_agreed:
            next_pts = 20.0
            if inp.next_step_days_out is not None and inp.next_step_days_out > 14:
                next_pts -= 10.0

        talk_pts     = 10.0 if inp.talk_ratio_pct <= 50.0 else 0.0
        demo_pts     = 8.0 if inp.demo_shown else 0.0
        proposal_pts = 7.0 if inp.proposal_sent else 0.0

        dur_pts   = 5.0 if inp.duration_minutes >= 30 else 0.0
        dur_pts  += 5.0 if inp.duration_minutes >= 60 else 0.0
        att_pts   = 5.0 if inp.attendees_count >= 2 else 0.0

        raw = eng_pts + next_pts + talk_pts + demo_pts + proposal_pts + dur_pts + att_pts
        return round(min(100.0, max(0.0, raw)), 1)

    def _meeting_outcome(self, inp: MeetingInput, signals: int) -> MeetingOutcome:
        if not inp.next_step_agreed:
            if signals == 0 or inp.objections_raised >= 3:
                return MeetingOutcome.REGRESSED
            return MeetingOutcome.NO_DECISION
        # Next step agreed
        if signals >= 2 and inp.objections_raised <= 1:
            return MeetingOutcome.ADVANCED
        return MeetingOutcome.MAINTAINED

    def _meeting_quality(self, score: float) -> MeetingQuality:
        if score >= 75:
            return MeetingQuality.EXCELLENT
        if score >= 55:
            return MeetingQuality.GOOD
        if score >= 35:
            return MeetingQuality.AVERAGE
        return MeetingQuality.POOR

    def _follow_up_urgency(
        self, outcome: MeetingOutcome, signals: BuyingSignalStrength, inp: MeetingInput
    ) -> FollowUpUrgency:
        if outcome == MeetingOutcome.REGRESSED:
            return FollowUpUrgency.IMMEDIATE
        if signals == BuyingSignalStrength.STRONG:
            return FollowUpUrgency.SAME_WEEK
        if inp.prospect_requested_pricing or inp.prospect_mentioned_timeline:
            return FollowUpUrgency.SAME_WEEK
        if outcome == MeetingOutcome.MAINTAINED and inp.objections_raised >= 2:
            return FollowUpUrgency.SAME_WEEK
        if outcome == MeetingOutcome.NO_DECISION:
            return FollowUpUrgency.SAME_WEEK
        if signals == BuyingSignalStrength.MODERATE:
            return FollowUpUrgency.STANDARD
        return FollowUpUrgency.MONITOR

    def _positive_signals(self, inp: MeetingInput) -> list[str]:
        signals: list[str] = []
        if inp.prospect_asked_questions:
            signals.append("Le prospect a posé des questions — signe d'intérêt actif")
        if inp.prospect_requested_pricing:
            signals.append("Demande de tarification — acheteur potentiel identifié")
        if inp.prospect_mentioned_timeline:
            signals.append("Timeline mentionnée — urgence côté prospect confirmée")
        if inp.prospect_mentioned_budget:
            signals.append("Budget évoqué — signal d'achat fort")
        if inp.decision_maker_present:
            signals.append("Décideur présent — accès direct au pouvoir de signature")
        if inp.exec_sponsor_present:
            signals.append("Sponsor exécutif présent — relation stratégique engagée")
        if inp.next_step_agreed:
            days = inp.next_step_days_out
            signals.append(
                f"Prochaine étape validée{f' dans {days} jours' if days is not None else ''}"
            )
        return signals

    def _concerns(self, inp: MeetingInput) -> list[str]:
        concerns: list[str] = []
        if inp.objections_raised >= 1:
            concerns.append(f"{inp.objections_raised} objection(s) soulevée(s) — traitement requis")
        if inp.talk_ratio_pct > 65:
            concerns.append(
                f"Rep parle {inp.talk_ratio_pct:.0f}% du temps — améliorer l'écoute active"
            )
        if not inp.next_step_agreed:
            concerns.append("Aucune prochaine étape convenue — risque de décrochage")
        if inp.next_step_days_out is not None and inp.next_step_days_out > 14:
            concerns.append(
                f"Prochaine étape à {inp.next_step_days_out}j — délai long, relancer avant"
            )
        if inp.competitor_mentioned:
            concerns.append("Concurrent mentionné — évaluation comparative en cours")
        if inp.duration_minutes < 20:
            concerns.append(f"Réunion courte ({inp.duration_minutes} min) — engagement limité")
        return concerns

    def _follow_up_actions(self, inp: MeetingInput, outcome: MeetingOutcome) -> list[str]:
        actions: list[str] = []
        if inp.prospect_requested_pricing and not inp.proposal_sent:
            actions.append("Envoyer la proposition tarifaire dans les 24h")
        if inp.next_step_agreed and inp.next_step_days_out is not None:
            actions.append(
                f"Envoyer un email de confirmation avec l'ordre du jour de la prochaine réunion (J+{inp.next_step_days_out})"
            )
        if inp.objections_raised >= 1:
            actions.append("Préparer les réponses aux objections — envoyer la documentation de référence")
        if inp.competitor_mentioned:
            actions.append("Activer la battlecard compétitive — différenciation à renforcer")
        if inp.prospect_mentioned_budget:
            actions.append("Envoyer le ROI calculator personnalisé dans les 48h")
        if outcome == MeetingOutcome.REGRESSED:
            actions.append("Appel de suivi urgence — identifier les blocages et proposer une valeur immédiate")
        if not inp.next_step_agreed:
            actions.append("Relancer dans les 48h pour convenir d'une prochaine étape")
        if not actions:
            actions.append("Envoyer un email de remerciement avec les points clés abordés")
        return actions

    def _manager_alerts(
        self,
        inp: MeetingInput,
        outcome: MeetingOutcome,
        quality: MeetingQuality,
    ) -> list[str]:
        alerts: list[str] = []
        if outcome == MeetingOutcome.REGRESSED:
            alerts.append(f"⚠ Deal {inp.deal_id} régressé après réunion — revue manager recommandée")
        if quality == MeetingQuality.POOR and inp.previous_meetings_count >= 2:
            alerts.append(
                f"3ème+ réunion médiocre sur ce deal — envisager un coaching ou escalade"
            )
        if inp.talk_ratio_pct > 70:
            alerts.append(
                f"Ratio de parole rep: {inp.talk_ratio_pct:.0f}% — coaching écoute active requis"
            )
        if inp.competitor_mentioned and inp.objections_raised >= 2:
            alerts.append("Concurrent actif + objections multiples — deal en danger")
        if not inp.next_step_agreed and inp.previous_meetings_count >= 1:
            alerts.append("Pas de prochaine étape après 2+ réunions — deal potentiellement bloqué")
        return alerts

    # ── public API ─────────────────────────────────────────────────────────

    def analyze(self, inp: MeetingInput) -> MeetingResult:
        signals_count = self._buying_signals_count(inp)
        engagement    = self._engagement_score(inp)
        quality_sc    = self._quality_score(inp, engagement)
        signal_str    = self._buying_signal_strength(signals_count, inp.objections_raised)
        outcome       = self._meeting_outcome(inp, signals_count)
        quality       = self._meeting_quality(quality_sc)
        urgency       = self._follow_up_urgency(outcome, signal_str, inp)

        result = MeetingResult(
            meeting_id=inp.meeting_id,
            deal_id=inp.deal_id,
            rep_id=inp.rep_id,
            rep_name=inp.rep_name,
            account_name=inp.account_name,
            meeting_type=inp.meeting_type,
            meeting_outcome=outcome,
            meeting_quality=quality,
            buying_signal_strength=signal_str,
            follow_up_urgency=urgency,
            quality_score=quality_sc,
            engagement_score=engagement,
            buying_signals_count=signals_count,
            objections_count=inp.objections_raised,
            next_step_agreed=inp.next_step_agreed,
            next_step_days_out=inp.next_step_days_out,
            positive_signals=self._positive_signals(inp),
            concerns=self._concerns(inp),
            follow_up_actions=self._follow_up_actions(inp, outcome),
            manager_alerts=self._manager_alerts(inp, outcome, quality),
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[MeetingInput]) -> list[MeetingResult]:
        """Analyze batch, sorted DESC by quality_score (best meeting first)."""
        results = [self.analyze(inp) for inp in inputs]
        results.sort(key=lambda r: r.quality_score, reverse=True)
        return results

    # ── filter helpers ─────────────────────────────────────────────────────

    def all_meetings(self) -> list[MeetingResult]:
        return list(self._results)

    def by_outcome(self, outcome: MeetingOutcome) -> list[MeetingResult]:
        return [r for r in self._results if r.meeting_outcome == outcome]

    def by_quality(self, quality: MeetingQuality) -> list[MeetingResult]:
        return [r for r in self._results if r.meeting_quality == quality]

    def by_urgency(self, urgency: FollowUpUrgency) -> list[MeetingResult]:
        return [r for r in self._results if r.follow_up_urgency == urgency]

    def advanced_deals(self) -> list[MeetingResult]:
        return self.by_outcome(MeetingOutcome.ADVANCED)

    def regressed_deals(self) -> list[MeetingResult]:
        return self.by_outcome(MeetingOutcome.REGRESSED)

    def needs_immediate_follow_up(self) -> list[MeetingResult]:
        return self.by_urgency(FollowUpUrgency.IMMEDIATE)

    def with_manager_alerts(self) -> list[MeetingResult]:
        return [r for r in self._results if len(r.manager_alerts) > 0]

    def strong_buying_signals(self) -> list[MeetingResult]:
        return [r for r in self._results if r.buying_signal_strength == BuyingSignalStrength.STRONG]

    # ── aggregates ─────────────────────────────────────────────────────────

    def avg_quality_score(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.quality_score for r in self._results) / len(self._results), 1)

    def avg_engagement_score(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.engagement_score for r in self._results) / len(self._results), 1)

    def next_step_rate(self) -> float:
        """Percentage of meetings with a next step agreed (0–100)."""
        if not self._results:
            return 0.0
        agreed = sum(1 for r in self._results if r.next_step_agreed)
        return round(agreed / len(self._results) * 100, 1)

    def advancement_rate(self) -> float:
        """Percentage of meetings that advanced the deal (0–100)."""
        if not self._results:
            return 0.0
        advanced = sum(1 for r in self._results if r.meeting_outcome == MeetingOutcome.ADVANCED)
        return round(advanced / len(self._results) * 100, 1)

    def summary(self) -> dict:
        n = len(self._results)
        outcome_counts: dict[str, int] = {}
        quality_counts: dict[str, int] = {}
        urgency_counts: dict[str, int] = {}
        signal_counts:  dict[str, int] = {}
        for r in self._results:
            outcome_counts[r.meeting_outcome.value]          = outcome_counts.get(r.meeting_outcome.value, 0) + 1
            quality_counts[r.meeting_quality.value]          = quality_counts.get(r.meeting_quality.value, 0) + 1
            urgency_counts[r.follow_up_urgency.value]        = urgency_counts.get(r.follow_up_urgency.value, 0) + 1
            signal_counts[r.buying_signal_strength.value]    = signal_counts.get(r.buying_signal_strength.value, 0) + 1
        return {
            "total": n,
            "outcome_counts": outcome_counts,
            "quality_counts": quality_counts,
            "urgency_counts": urgency_counts,
            "signal_counts": signal_counts,
            "avg_quality_score": self.avg_quality_score(),
            "avg_engagement_score": self.avg_engagement_score(),
            "next_step_rate": self.next_step_rate(),
            "advancement_rate": self.advancement_rate(),
            "immediate_follow_up_count": len(self.needs_immediate_follow_up()),
        }

    def reset(self) -> None:
        self._results.clear()
