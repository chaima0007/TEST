"""Customer Sentiment Decay Engine — detects when positive customer sentiment
is eroding, predicting at-risk accounts before explicit churn signals appear."""

from __future__ import annotations

import dataclasses
from enum import Enum


class DecayStage(str, Enum):
    stable = "stable"
    early_warning = "early_warning"
    declining = "declining"
    critical = "critical"
    churning = "churning"


class DecayRisk(str, Enum):
    low = "low"
    moderate = "moderate"
    high = "high"
    critical = "critical"


class DecaySignal(str, Enum):
    none = "none"
    engagement_drop = "engagement_drop"
    support_escalation = "support_escalation"
    executive_silence = "executive_silence"
    nps_decline = "nps_decline"
    usage_reduction = "usage_reduction"
    payment_delay = "payment_delay"


class DecayAction(str, Enum):
    no_action = "no_action"
    monitor = "monitor"
    proactive_outreach = "proactive_outreach"
    executive_escalation = "executive_escalation"
    emergency_intervention = "emergency_intervention"


@dataclasses.dataclass
class CustomerSentimentDecayInput:
    account_id: str
    account_name: str
    csm_id: str
    region: str
    nps_current: float
    nps_prior_quarter: float
    nps_prior_year: float
    support_tickets_last_30d: int
    support_tickets_prior_30d: int
    critical_tickets_last_30d: int
    avg_ticket_resolution_hours: float
    executive_engagement_last_90d: int
    executive_meetings_prior_90d: int
    product_usage_pct_current: float
    product_usage_pct_prior: float
    feature_adoption_score: float
    login_frequency_last_30d: int
    login_frequency_prior_30d: int
    payment_delay_days: int
    contract_value_usd: float
    months_since_last_qbr: int
    expansion_discussions_last_90d: int


@dataclasses.dataclass
class CustomerSentimentDecayResult:
    account_id: str
    account_name: str
    decay_stage: DecayStage
    decay_risk: DecayRisk
    primary_decay_signal: DecaySignal
    recommended_action: DecayAction
    engagement_score: float
    support_health_score: float
    usage_vitality_score: float
    relationship_score: float
    decay_composite: float
    is_at_risk: bool
    requires_escalation: bool
    estimated_arr_at_risk_usd: float
    decay_signal: str

    def to_dict(self) -> dict:
        return {
            "account_id":             self.account_id,
            "account_name":           self.account_name,
            "decay_stage":            self.decay_stage.value,
            "decay_risk":             self.decay_risk.value,
            "primary_decay_signal":   self.primary_decay_signal.value,
            "recommended_action":     self.recommended_action.value,
            "engagement_score":       round(self.engagement_score, 1),
            "support_health_score":   round(self.support_health_score, 1),
            "usage_vitality_score":   round(self.usage_vitality_score, 1),
            "relationship_score":     round(self.relationship_score, 1),
            "decay_composite":        round(self.decay_composite, 1),
            "is_at_risk":             self.is_at_risk,
            "requires_escalation":    self.requires_escalation,
            "estimated_arr_at_risk_usd": round(self.estimated_arr_at_risk_usd, 2),
            "decay_signal":           self.decay_signal,
        }


def _clamp(v: float) -> float:
    return max(0.0, min(100.0, v))


class CustomerSentimentDecayEngine:
    """Detects decaying customer sentiment before explicit churn signals appear."""

    def __init__(self) -> None:
        self._results: list[CustomerSentimentDecayResult] = []

    # ── sub-scores (HIGHER = more decay/risk) ───────────────────────────────

    def _engagement_score(self, inp: CustomerSentimentDecayInput) -> float:
        score = 0.0
        # NPS decline
        nps_drop_qoq = inp.nps_prior_quarter - inp.nps_current
        nps_drop_yoy = inp.nps_prior_year - inp.nps_current
        if nps_drop_qoq > 30:
            score += 35.0
        elif nps_drop_qoq > 20:
            score += 24.0
        elif nps_drop_qoq > 10:
            score += 14.0
        elif nps_drop_qoq > 5:
            score += 7.0
        if nps_drop_yoy > 40:
            score += 20.0
        elif nps_drop_yoy > 20:
            score += 12.0
        # Absolute NPS level
        if inp.nps_current < 0:
            score += 25.0
        elif inp.nps_current < 20:
            score += 15.0
        elif inp.nps_current < 40:
            score += 8.0
        # QBR overdue
        if inp.months_since_last_qbr >= 6:
            score += 15.0
        elif inp.months_since_last_qbr >= 4:
            score += 8.0
        return _clamp(score)

    def _support_health_score(self, inp: CustomerSentimentDecayInput) -> float:
        score = 0.0
        # Ticket surge
        if inp.support_tickets_prior_30d > 0:
            ticket_ratio = inp.support_tickets_last_30d / inp.support_tickets_prior_30d
        else:
            ticket_ratio = 1.0 if inp.support_tickets_last_30d == 0 else 3.0
        if ticket_ratio >= 3.0:
            score += 35.0
        elif ticket_ratio >= 2.0:
            score += 22.0
        elif ticket_ratio >= 1.5:
            score += 12.0
        # Critical tickets
        if inp.critical_tickets_last_30d >= 3:
            score += 35.0
        elif inp.critical_tickets_last_30d >= 2:
            score += 24.0
        elif inp.critical_tickets_last_30d >= 1:
            score += 12.0
        # Slow resolution time
        if inp.avg_ticket_resolution_hours > 120:
            score += 20.0
        elif inp.avg_ticket_resolution_hours > 72:
            score += 12.0
        elif inp.avg_ticket_resolution_hours > 48:
            score += 6.0
        return _clamp(score)

    def _usage_vitality_score(self, inp: CustomerSentimentDecayInput) -> float:
        score = 0.0
        # Usage drop
        if inp.product_usage_pct_prior > 0:
            usage_change = inp.product_usage_pct_current - inp.product_usage_pct_prior
        else:
            usage_change = 0.0
        if usage_change < -30:
            score += 40.0
        elif usage_change < -20:
            score += 28.0
        elif usage_change < -10:
            score += 16.0
        elif usage_change < -5:
            score += 8.0
        # Absolute usage level
        if inp.product_usage_pct_current < 30:
            score += 25.0
        elif inp.product_usage_pct_current < 50:
            score += 15.0
        # Login frequency drop
        if inp.login_frequency_prior_30d > 0:
            login_ratio = inp.login_frequency_last_30d / inp.login_frequency_prior_30d
        else:
            login_ratio = 1.0
        if login_ratio < 0.3:
            score += 20.0
        elif login_ratio < 0.5:
            score += 12.0
        elif login_ratio < 0.7:
            score += 6.0
        # Low feature adoption
        if inp.feature_adoption_score < 20:
            score += 15.0
        elif inp.feature_adoption_score < 40:
            score += 8.0
        return _clamp(score)

    def _relationship_score(self, inp: CustomerSentimentDecayInput) -> float:
        score = 0.0
        # Executive disengagement
        exec_drop = inp.executive_meetings_prior_90d - inp.executive_engagement_last_90d
        if exec_drop >= 3:
            score += 40.0
        elif exec_drop >= 2:
            score += 28.0
        elif exec_drop >= 1:
            score += 15.0
        # Zero executive engagement
        if inp.executive_engagement_last_90d == 0 and inp.executive_meetings_prior_90d > 0:
            score += 20.0
        # Payment delays
        if inp.payment_delay_days > 45:
            score += 25.0
        elif inp.payment_delay_days > 30:
            score += 15.0
        elif inp.payment_delay_days > 15:
            score += 8.0
        # No expansion signals
        if inp.expansion_discussions_last_90d == 0:
            score += 15.0
        return _clamp(score)

    # ── classification ───────────────────────────────────────────────────────

    def _classify_stage(self, composite: float) -> DecayStage:
        if composite < 15:
            return DecayStage.stable
        if composite < 30:
            return DecayStage.early_warning
        if composite < 50:
            return DecayStage.declining
        if composite < 70:
            return DecayStage.critical
        return DecayStage.churning

    def _classify_risk(self, composite: float) -> DecayRisk:
        if composite < 20:
            return DecayRisk.low
        if composite < 40:
            return DecayRisk.moderate
        if composite < 60:
            return DecayRisk.high
        return DecayRisk.critical

    def _primary_signal(
        self,
        inp: CustomerSentimentDecayInput,
        engagement: float,
        support: float,
        usage: float,
        relationship: float,
    ) -> DecaySignal:
        worst = max(engagement, support, usage, relationship)
        if worst < 15:
            return DecaySignal.none
        scores = {
            DecaySignal.nps_decline:        engagement   if (inp.nps_prior_quarter - inp.nps_current) > 10 else 0,
            DecaySignal.support_escalation: support      if inp.critical_tickets_last_30d >= 1 else 0,
            DecaySignal.usage_reduction:    usage        if inp.product_usage_pct_current < inp.product_usage_pct_prior - 10 else 0,
            DecaySignal.executive_silence:  relationship if inp.executive_engagement_last_90d == 0 else 0,
            DecaySignal.payment_delay:      relationship if inp.payment_delay_days > 15 else 0,
            DecaySignal.engagement_drop:    engagement   if inp.months_since_last_qbr >= 4 else 0,
        }
        best = max(scores, key=lambda k: scores[k])
        if scores[best] == 0:
            return DecaySignal.none
        return best

    def _recommended_action(self, risk: DecayRisk, composite: float) -> DecayAction:
        if composite >= 70:
            return DecayAction.emergency_intervention
        if risk == DecayRisk.critical:
            return DecayAction.executive_escalation
        if risk == DecayRisk.high:
            return DecayAction.proactive_outreach
        if risk == DecayRisk.moderate:
            return DecayAction.monitor
        return DecayAction.no_action

    def _signal(
        self,
        stage: DecayStage,
        signal: DecaySignal,
        composite: float,
        inp: CustomerSentimentDecayInput,
    ) -> str:
        if stage == DecayStage.stable:
            return "customer sentiment stable — no decay signals detected"
        msgs = {
            DecaySignal.nps_decline: (
                f"NPS dropped {inp.nps_prior_quarter - inp.nps_current:.0f}pts QoQ "
                f"(now {inp.nps_current:.0f})"
            ),
            DecaySignal.support_escalation: (
                f"{inp.critical_tickets_last_30d} critical ticket(s) in 30 days — "
                f"{inp.support_tickets_last_30d} total tickets"
            ),
            DecaySignal.usage_reduction: (
                f"product usage dropped to {inp.product_usage_pct_current:.0f}% "
                f"(from {inp.product_usage_pct_prior:.0f}%)"
            ),
            DecaySignal.executive_silence: (
                f"zero executive meetings in 90 days (vs {inp.executive_meetings_prior_90d} prior)"
            ),
            DecaySignal.payment_delay: (
                f"payment {inp.payment_delay_days} days overdue"
            ),
            DecaySignal.engagement_drop: (
                f"no QBR in {inp.months_since_last_qbr} months — engagement gap"
            ),
        }
        base = msgs.get(signal, f"sentiment decay detected composite {composite:.0f}")
        return f"{base} — decay composite {composite:.0f}"

    # ── public API ───────────────────────────────────────────────────────────

    def assess(self, inp: CustomerSentimentDecayInput) -> CustomerSentimentDecayResult:
        engagement  = self._engagement_score(inp)
        support     = self._support_health_score(inp)
        usage       = self._usage_vitality_score(inp)
        relationship = self._relationship_score(inp)

        composite = _clamp(
            engagement  * 0.30
            + support   * 0.25
            + usage     * 0.25
            + relationship * 0.20
        )
        composite = round(composite, 1)

        stage  = self._classify_stage(composite)
        risk   = self._classify_risk(composite)
        signal = self._primary_signal(inp, engagement, support, usage, relationship)
        action = self._recommended_action(risk, composite)

        is_at_risk = (
            composite >= 35
            or inp.critical_tickets_last_30d >= 2
            or inp.nps_current < 0
        )
        requires_escalation = (
            composite >= 55
            or inp.payment_delay_days > 45
            or (inp.executive_engagement_last_90d == 0 and inp.executive_meetings_prior_90d >= 2)
        )

        estimated_arr_at_risk_usd = inp.contract_value_usd * (composite / 100.0)

        result = CustomerSentimentDecayResult(
            account_id=inp.account_id,
            account_name=inp.account_name,
            decay_stage=stage,
            decay_risk=risk,
            primary_decay_signal=signal,
            recommended_action=action,
            engagement_score=engagement,
            support_health_score=support,
            usage_vitality_score=usage,
            relationship_score=relationship,
            decay_composite=composite,
            is_at_risk=is_at_risk,
            requires_escalation=requires_escalation,
            estimated_arr_at_risk_usd=estimated_arr_at_risk_usd,
            decay_signal=self._signal(stage, signal, composite, inp),
        )
        self._results.append(result)
        return result

    def assess_batch(
        self, inputs: list[CustomerSentimentDecayInput]
    ) -> list[CustomerSentimentDecayResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "stage_counts": {},
                "risk_counts": {},
                "signal_counts": {},
                "action_counts": {},
                "avg_decay_composite": 0.0,
                "at_risk_count": 0,
                "escalation_count": 0,
                "avg_engagement_score": 0.0,
                "avg_support_health_score": 0.0,
                "avg_usage_vitality_score": 0.0,
                "avg_relationship_score": 0.0,
                "total_arr_at_risk_usd": 0.0,
            }

        stage_counts:  dict[str, int] = {}
        risk_counts:   dict[str, int] = {}
        signal_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        total_comp = total_eng = total_sup = total_use = total_rel = total_arr = 0.0
        at_risk = escalation = 0

        for r in self._results:
            stage_counts[r.decay_stage.value]          = stage_counts.get(r.decay_stage.value, 0) + 1
            risk_counts[r.decay_risk.value]            = risk_counts.get(r.decay_risk.value, 0) + 1
            signal_counts[r.primary_decay_signal.value] = signal_counts.get(r.primary_decay_signal.value, 0) + 1
            action_counts[r.recommended_action.value]  = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.decay_composite
            total_eng  += r.engagement_score
            total_sup  += r.support_health_score
            total_use  += r.usage_vitality_score
            total_rel  += r.relationship_score
            total_arr  += r.estimated_arr_at_risk_usd
            if r.is_at_risk:
                at_risk += 1
            if r.requires_escalation:
                escalation += 1

        n = len(self._results)
        return {
            "total":                    n,
            "stage_counts":             stage_counts,
            "risk_counts":              risk_counts,
            "signal_counts":            signal_counts,
            "action_counts":            action_counts,
            "avg_decay_composite":      round(total_comp / n, 1),
            "at_risk_count":            at_risk,
            "escalation_count":         escalation,
            "avg_engagement_score":     round(total_eng  / n, 1),
            "avg_support_health_score": round(total_sup  / n, 1),
            "avg_usage_vitality_score": round(total_use  / n, 1),
            "avg_relationship_score":   round(total_rel  / n, 1),
            "total_arr_at_risk_usd":    round(total_arr, 2),
        }
