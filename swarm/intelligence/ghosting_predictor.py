from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class GhostingRisk(str, Enum):
    LOW         = "low"
    MODERATE    = "moderate"
    HIGH        = "high"
    CRITICAL    = "critical"


class GhostingPattern(str, Enum):
    ENGAGED         = "engaged"
    COOLING_OFF     = "cooling_off"
    SLOW_FADE       = "slow_fade"
    PARTIAL_GHOST   = "partial_ghost"
    FULL_GHOST      = "full_ghost"
    CHAMPION_EXIT   = "champion_exit"


class BuyerMomentum(str, Enum):
    ACCELERATING    = "accelerating"
    STABLE          = "stable"
    DECELERATING    = "decelerating"
    STALLED         = "stalled"


class GhostingAction(str, Enum):
    MAINTAIN        = "maintain"
    RE_ENGAGE       = "re_engage"
    ESCALATE_PATH   = "escalate_path"
    LAST_RESORT     = "last_resort"


@dataclass
class GhostingPredictorInput:
    deal_id:                        str
    deal_name:                      str
    rep_id:                         str
    days_since_last_buyer_reply:    int     # days since buyer last responded to any touchpoint
    days_since_last_meeting:        int     # days since last meeting was held
    meetings_cancelled_last_30d:    int     # meetings buyer cancelled in last 30 days
    meetings_rescheduled_last_30d:  int     # meetings rescheduled (softer signal)
    email_open_rate_last_30d:       float   # % of rep emails buyer opened in last 30 days (0-100)
    email_open_rate_prior_30d:      float   # % of rep emails buyer opened in prior 30 days (baseline)
    response_time_avg_hours_recent: float   # buyer's average response time (hours) last 30d
    response_time_avg_hours_prior:  float   # buyer's average response time (hours) prior 30d
    champion_last_active_days_ago:  int     # days since champion was last active/responsive
    champion_linkedin_gone_quiet:   int     # 1 if champion has stopped engaging on LinkedIn
    stakeholder_count_drop:         int     # # of stakeholders who dropped off email threads
    next_step_missed_count:         int     # # of agreed next steps buyer missed/ignored
    deal_stage_days_stuck:          int     # days stuck in current stage with no movement
    proposal_opened_last_7d:        int     # 1 if buyer opened proposal/pricing doc in last 7 days
    pricing_conversation_stalled:   int     # 1 if pricing discussion went silent after initial exchange
    internal_champion_change:       int     # 1 if buyer's champion/sponsor changed recently
    competitor_meeting_signal:      int     # 1 if signal that buyer met with competitor recently
    deal_value:                     float
    days_to_close_target:           int     # days remaining to target close date


@dataclass
class GhostingPredictorResult:
    deal_id:                str
    deal_name:              str
    ghosting_risk:          GhostingRisk
    ghosting_pattern:       GhostingPattern
    buyer_momentum:         BuyerMomentum
    ghosting_action:        GhostingAction
    silence_score:          float   # 0-100, higher = more silent
    engagement_decay_score: float   # 0-100, higher = more decayed
    behavioral_risk_score:  float   # 0-100, behavioral pre-ghost signals
    deal_urgency_score:     float   # 0-100, urgency to act now
    ghosting_composite:     float   # 0-100, overall ghost risk
    predicted_ghost_days:   int     # days until deal likely goes fully silent
    recovery_probability:   float   # 0-100, % chance of re-engaging this deal
    is_at_risk_of_ghosting: bool
    needs_escalation:       bool

    def to_dict(self) -> dict:
        return {
            "deal_id":                self.deal_id,
            "deal_name":              self.deal_name,
            "ghosting_risk":          self.ghosting_risk.value,
            "ghosting_pattern":       self.ghosting_pattern.value,
            "buyer_momentum":         self.buyer_momentum.value,
            "ghosting_action":        self.ghosting_action.value,
            "silence_score":          self.silence_score,
            "engagement_decay_score": self.engagement_decay_score,
            "behavioral_risk_score":  self.behavioral_risk_score,
            "deal_urgency_score":     self.deal_urgency_score,
            "ghosting_composite":     self.ghosting_composite,
            "predicted_ghost_days":   self.predicted_ghost_days,
            "recovery_probability":   self.recovery_probability,
            "is_at_risk_of_ghosting": self.is_at_risk_of_ghosting,
            "needs_escalation":       self.needs_escalation,
        }


class GhostingPredictor:
    def __init__(self) -> None:
        self._results: list[GhostingPredictorResult] = []

    # ── public API ──────────────────────────────────────────────────────────────

    def predict(self, inp: GhostingPredictorInput) -> GhostingPredictorResult:
        silence   = self._silence_score(inp)
        decay     = self._engagement_decay_score(inp)
        behav     = self._behavioral_risk_score(inp)
        urgency   = self._deal_urgency_score(inp)
        composite = self._composite(silence, decay, behav, urgency)
        risk      = self._ghosting_risk(composite)
        pattern   = self._ghosting_pattern(inp, composite)
        momentum  = self._buyer_momentum(inp)
        ghost_days = self._predicted_ghost_days(inp, composite)
        recovery  = self._recovery_probability(inp, composite)
        is_at_risk = composite >= 50.0 or inp.next_step_missed_count >= 3
        needs_esc  = composite >= 70.0 or inp.internal_champion_change == 1 or inp.days_since_last_buyer_reply >= 21
        action    = self._ghosting_action(risk, needs_esc, composite)

        result = GhostingPredictorResult(
            deal_id=inp.deal_id,
            deal_name=inp.deal_name,
            ghosting_risk=risk,
            ghosting_pattern=pattern,
            buyer_momentum=momentum,
            ghosting_action=action,
            silence_score=silence,
            engagement_decay_score=decay,
            behavioral_risk_score=behav,
            deal_urgency_score=urgency,
            ghosting_composite=composite,
            predicted_ghost_days=ghost_days,
            recovery_probability=recovery,
            is_at_risk_of_ghosting=is_at_risk,
            needs_escalation=needs_esc,
        )
        self._results.append(result)
        return result

    def predict_batch(self, inputs: list[GhostingPredictorInput]) -> list[GhostingPredictorResult]:
        return [self.predict(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ──────────────────────────────────────────────────────────────

    @property
    def at_risk_deals(self) -> list[GhostingPredictorResult]:
        return [r for r in self._results if r.is_at_risk_of_ghosting]

    @property
    def escalation_queue(self) -> list[GhostingPredictorResult]:
        return [r for r in self._results if r.needs_escalation]

    @property
    def avg_ghosting_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.ghosting_composite for r in self._results) / len(self._results), 1)

    @property
    def avg_recovery_probability(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.recovery_probability for r in self._results) / len(self._results), 1)

    # ── scoring helpers ─────────────────────────────────────────────────────────

    def _silence_score(self, inp: GhostingPredictorInput) -> float:
        score = 0.0
        # Days since last reply (primary signal)
        days_reply = inp.days_since_last_buyer_reply
        if days_reply >= 21:
            score += 50.0
        elif days_reply >= 14:
            score += 35.0
        elif days_reply >= 7:
            score += 20.0
        elif days_reply >= 3:
            score += 8.0
        # Days since last meeting
        days_mtg = inp.days_since_last_meeting
        if days_mtg >= 30:
            score += 25.0
        elif days_mtg >= 14:
            score += 15.0
        elif days_mtg >= 7:
            score += 8.0
        # Champion silence
        if inp.champion_last_active_days_ago >= 21:
            score += 15.0
        elif inp.champion_last_active_days_ago >= 10:
            score += 8.0
        # Proposal opened recently = NOT silent
        if inp.proposal_opened_last_7d:
            score = max(0.0, score - 15.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _engagement_decay_score(self, inp: GhostingPredictorInput) -> float:
        score = 0.0
        # Email open rate decay
        open_decay = inp.email_open_rate_prior_30d - inp.email_open_rate_last_30d
        if open_decay >= 40:
            score += 30.0
        elif open_decay >= 20:
            score += 20.0
        elif open_decay >= 10:
            score += 10.0
        elif open_decay < 0:
            # open rate improved — negative signal for ghosting
            score -= 10.0
        # Response time decay (increase = bad)
        rt_prior = inp.response_time_avg_hours_prior
        rt_recent = inp.response_time_avg_hours_recent
        if rt_prior > 0:
            rt_ratio = rt_recent / rt_prior
        else:
            rt_ratio = 1.0 if rt_recent == 0 else 2.0
        if rt_ratio >= 3.0:
            score += 30.0
        elif rt_ratio >= 2.0:
            score += 20.0
        elif rt_ratio >= 1.5:
            score += 10.0
        elif rt_ratio < 0.8:
            score -= 10.0
        # Stakeholder dropout
        if inp.stakeholder_count_drop >= 3:
            score += 20.0
        elif inp.stakeholder_count_drop >= 1:
            score += 10.0
        # LinkedIn silence
        if inp.champion_linkedin_gone_quiet:
            score += 10.0
        return round(max(0.0, min(100.0, score)), 1)

    def _behavioral_risk_score(self, inp: GhostingPredictorInput) -> float:
        score = 0.0
        # Next steps missed
        missed = inp.next_step_missed_count
        if missed >= 4:
            score += 35.0
        elif missed >= 2:
            score += 22.0
        elif missed >= 1:
            score += 10.0
        # Meetings cancelled
        cancelled = inp.meetings_cancelled_last_30d
        if cancelled >= 3:
            score += 20.0
        elif cancelled >= 2:
            score += 12.0
        elif cancelled >= 1:
            score += 6.0
        # Meetings rescheduled (softer)
        rescheduled = inp.meetings_rescheduled_last_30d
        if rescheduled >= 3:
            score += 8.0
        elif rescheduled >= 1:
            score += 4.0
        # Internal champion change = high risk
        if inp.internal_champion_change:
            score += 20.0
        # Competitor meeting signal
        if inp.competitor_meeting_signal:
            score += 12.0
        # Pricing stalled after initial exchange
        if inp.pricing_conversation_stalled:
            score += 10.0
        return round(max(0.0, min(100.0, score)), 1)

    def _deal_urgency_score(self, inp: GhostingPredictorInput) -> float:
        # Higher urgency = MORE important to act quickly (deal at risk)
        score = 0.0
        # Days stuck in stage
        stuck = inp.deal_stage_days_stuck
        if stuck >= 60:
            score += 40.0
        elif stuck >= 30:
            score += 25.0
        elif stuck >= 14:
            score += 12.0
        # Days to close target (less time = more urgent)
        days_left = inp.days_to_close_target
        if days_left <= 7:
            score += 30.0
        elif days_left <= 14:
            score += 20.0
        elif days_left <= 30:
            score += 12.0
        # Deal value weight (bigger deal = more urgent to address)
        if inp.deal_value >= 500_000:
            score += 20.0
        elif inp.deal_value >= 200_000:
            score += 12.0
        elif inp.deal_value >= 100_000:
            score += 6.0
        # Proposal opened recently = still some urgency (buyer IS looking)
        if inp.proposal_opened_last_7d:
            score = min(100.0, score + 10.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _composite(
        self,
        silence: float,
        decay: float,
        behav: float,
        urgency: float,
    ) -> float:
        composite = silence * 0.35 + decay * 0.30 + behav * 0.25 + urgency * 0.10
        return round(max(0.0, min(100.0, composite)), 1)

    def _ghosting_risk(self, composite: float) -> GhostingRisk:
        if composite >= 70:
            return GhostingRisk.CRITICAL
        if composite >= 50:
            return GhostingRisk.HIGH
        if composite >= 30:
            return GhostingRisk.MODERATE
        return GhostingRisk.LOW

    def _ghosting_pattern(self, inp: GhostingPredictorInput, composite: float) -> GhostingPattern:
        if inp.internal_champion_change and composite >= 50:
            return GhostingPattern.CHAMPION_EXIT
        if inp.days_since_last_buyer_reply >= 21 and composite >= 65:
            return GhostingPattern.FULL_GHOST
        if inp.stakeholder_count_drop >= 2 and composite >= 45:
            return GhostingPattern.PARTIAL_GHOST
        if inp.email_open_rate_last_30d < 10 and inp.email_open_rate_prior_30d >= 30:
            return GhostingPattern.SLOW_FADE
        if composite >= 35:
            return GhostingPattern.COOLING_OFF
        return GhostingPattern.ENGAGED

    def _buyer_momentum(self, inp: GhostingPredictorInput) -> BuyerMomentum:
        open_delta = inp.email_open_rate_last_30d - inp.email_open_rate_prior_30d
        if inp.response_time_avg_hours_prior > 0:
            rt_ratio = inp.response_time_avg_hours_recent / inp.response_time_avg_hours_prior
        else:
            rt_ratio = 1.0 if inp.response_time_avg_hours_recent == 0 else 2.0
        if open_delta >= 10 and rt_ratio < 0.8:
            return BuyerMomentum.ACCELERATING
        if open_delta <= -20 or rt_ratio >= 3.0 or inp.days_since_last_buyer_reply >= 14:
            return BuyerMomentum.STALLED
        if open_delta <= -10 or rt_ratio >= 1.5:
            return BuyerMomentum.DECELERATING
        return BuyerMomentum.STABLE

    def _predicted_ghost_days(self, inp: GhostingPredictorInput, composite: float) -> int:
        if composite >= 80:
            return 0  # already ghosting
        if composite >= 60:
            return max(0, 14 - inp.days_since_last_buyer_reply)
        if composite >= 40:
            return max(0, 21 - inp.days_since_last_buyer_reply)
        return max(0, 30 - inp.days_since_last_buyer_reply)

    def _recovery_probability(self, inp: GhostingPredictorInput, composite: float) -> float:
        base = max(0.0, 100.0 - composite)
        # Proposal recently opened = buyer still interested
        if inp.proposal_opened_last_7d:
            base = min(100.0, base + 15.0)
        # Champion exit = hard to recover
        if inp.internal_champion_change:
            base -= 20.0
        # Competitor signal = competition
        if inp.competitor_meeting_signal:
            base -= 15.0
        # Days since reply penalty
        if inp.days_since_last_buyer_reply >= 30:
            base -= 20.0
        elif inp.days_since_last_buyer_reply >= 14:
            base -= 10.0
        return round(max(0.0, min(100.0, base)), 1)

    def _ghosting_action(
        self,
        risk: GhostingRisk,
        needs_esc: bool,
        composite: float,
    ) -> GhostingAction:
        if needs_esc or risk == GhostingRisk.CRITICAL:
            return GhostingAction.LAST_RESORT
        if risk == GhostingRisk.HIGH:
            return GhostingAction.ESCALATE_PATH
        if risk == GhostingRisk.MODERATE:
            return GhostingAction.RE_ENGAGE
        return GhostingAction.MAINTAIN

    # ── summary ─────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                    0,
                "risk_counts":              {},
                "pattern_counts":           {},
                "momentum_counts":          {},
                "action_counts":            {},
                "avg_ghosting_composite":   0.0,
                "avg_recovery_probability": 0.0,
                "at_risk_count":            0,
                "escalation_count":         0,
                "avg_silence_score":        0.0,
                "avg_engagement_decay_score": 0.0,
                "avg_behavioral_risk_score": 0.0,
                "avg_deal_urgency_score":   0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        momentum_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = 0.0
        total_rec  = 0.0
        total_sil  = 0.0
        total_dec  = 0.0
        total_beh  = 0.0
        total_urg  = 0.0

        for r in self._results:
            risk_counts[r.ghosting_risk.value]       = risk_counts.get(r.ghosting_risk.value, 0) + 1
            pattern_counts[r.ghosting_pattern.value] = pattern_counts.get(r.ghosting_pattern.value, 0) + 1
            momentum_counts[r.buyer_momentum.value]  = momentum_counts.get(r.buyer_momentum.value, 0) + 1
            action_counts[r.ghosting_action.value]   = action_counts.get(r.ghosting_action.value, 0) + 1
            total_comp += r.ghosting_composite
            total_rec  += r.recovery_probability
            total_sil  += r.silence_score
            total_dec  += r.engagement_decay_score
            total_beh  += r.behavioral_risk_score
            total_urg  += r.deal_urgency_score

        return {
            "total":                        n,
            "risk_counts":                  risk_counts,
            "pattern_counts":               pattern_counts,
            "momentum_counts":              momentum_counts,
            "action_counts":                action_counts,
            "avg_ghosting_composite":       round(total_comp / n, 1),
            "avg_recovery_probability":     round(total_rec / n, 1),
            "at_risk_count":                len(self.at_risk_deals),
            "escalation_count":             len(self.escalation_queue),
            "avg_silence_score":            round(total_sil / n, 1),
            "avg_engagement_decay_score":   round(total_dec / n, 1),
            "avg_behavioral_risk_score":    round(total_beh / n, 1),
            "avg_deal_urgency_score":       round(total_urg / n, 1),
        }
