from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class HandoffRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class HandoffPattern(str, Enum):
    none                        = "none"
    oversell_setup              = "oversell_setup"
    expectation_mismatch        = "expectation_mismatch"
    incomplete_context_transfer = "incomplete_context_transfer"
    ghosting_at_handoff         = "ghosting_at_handoff"
    late_handoff_timing         = "late_handoff_timing"


class HandoffSeverity(str, Enum):
    seamless   = "seamless"
    adequate   = "adequate"
    disruptive = "disruptive"
    damaging   = "damaging"


class HandoffAction(str, Enum):
    no_action                          = "no_action"
    handoff_process_coaching           = "handoff_process_coaching"
    expectation_alignment_coaching     = "expectation_alignment_coaching"
    customer_success_partnership_coaching = "customer_success_partnership_coaching"
    post_sale_involvement_coaching     = "post_sale_involvement_coaching"
    handoff_reset_intervention         = "handoff_reset_intervention"


@dataclass
class HandoffInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    implementation_plan_provided_pct: float
    success_criteria_shared_with_cs_pct: float
    deal_history_documented_pct: float
    customer_expectation_alignment_rate_pct: float
    features_promised_not_delivered_pct: float
    time_to_first_value_slip_rate_pct: float
    rep_involved_in_onboarding_pct: float
    post_sale_check_in_rate_pct: float
    escalations_requiring_rep_re_engagement_pct: float
    days_between_close_and_handoff_avg: float
    handoff_meeting_attended_pct: float
    onboarding_start_delay_days_avg: float
    customer_satisfaction_at_90d_pct: float
    churn_within_12m_rate_pct: float
    expansion_revenue_from_cs_handoffs_pct: float
    nps_detractor_rate_pct: float
    reference_willingness_rate_pct: float
    total_deals_closed: int
    avg_opportunity_value_usd: float


@dataclass
class HandoffResult:
    rep_id: str
    region: str
    handoff_risk: HandoffRisk
    handoff_pattern: HandoffPattern
    handoff_severity: HandoffSeverity
    recommended_action: HandoffAction
    context_score: float
    expectation_score: float
    continuity_score: float
    timing_score: float
    handoff_composite: float
    has_handoff_gap: bool
    requires_handoff_coaching: bool
    estimated_churn_risk_usd: float
    handoff_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                       self.rep_id,
            "region":                       self.region,
            "handoff_risk":                 self.handoff_risk.value,
            "handoff_pattern":              self.handoff_pattern.value,
            "handoff_severity":             self.handoff_severity.value,
            "recommended_action":           self.recommended_action.value,
            "context_score":                self.context_score,
            "expectation_score":            self.expectation_score,
            "continuity_score":             self.continuity_score,
            "timing_score":                 self.timing_score,
            "handoff_composite":            self.handoff_composite,
            "has_handoff_gap":              self.has_handoff_gap,
            "requires_handoff_coaching":    self.requires_handoff_coaching,
            "estimated_churn_risk_usd":     self.estimated_churn_risk_usd,
            "handoff_signal":               self.handoff_signal,
        }


class SalesCustomerSuccessHandoffQualityIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[HandoffResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _context_score(self, inp: HandoffInput) -> float:
        score = 0.0

        if inp.implementation_plan_provided_pct <= 0.30:
            score += 40.0
        elif inp.implementation_plan_provided_pct <= 0.55:
            score += 22.0
        elif inp.implementation_plan_provided_pct <= 0.75:
            score += 8.0

        if inp.success_criteria_shared_with_cs_pct <= 0.35:
            score += 35.0
        elif inp.success_criteria_shared_with_cs_pct <= 0.60:
            score += 18.0

        if inp.deal_history_documented_pct <= 0.40:
            score += 25.0
        elif inp.deal_history_documented_pct <= 0.65:
            score += 12.0

        return min(score, 100.0)

    def _expectation_score(self, inp: HandoffInput) -> float:
        score = 0.0

        if inp.customer_expectation_alignment_rate_pct <= 0.50:
            score += 40.0
        elif inp.customer_expectation_alignment_rate_pct <= 0.70:
            score += 22.0
        elif inp.customer_expectation_alignment_rate_pct <= 0.85:
            score += 8.0

        if inp.features_promised_not_delivered_pct >= 0.25:
            score += 35.0
        elif inp.features_promised_not_delivered_pct >= 0.15:
            score += 18.0

        if inp.time_to_first_value_slip_rate_pct >= 0.45:
            score += 25.0
        elif inp.time_to_first_value_slip_rate_pct >= 0.25:
            score += 12.0

        return min(score, 100.0)

    def _continuity_score(self, inp: HandoffInput) -> float:
        score = 0.0

        if inp.rep_involved_in_onboarding_pct <= 0.30:
            score += 45.0
        elif inp.rep_involved_in_onboarding_pct <= 0.55:
            score += 25.0
        elif inp.rep_involved_in_onboarding_pct <= 0.75:
            score += 10.0

        if inp.post_sale_check_in_rate_pct <= 0.25:
            score += 30.0
        elif inp.post_sale_check_in_rate_pct <= 0.50:
            score += 15.0

        if inp.escalations_requiring_rep_re_engagement_pct >= 0.40:
            score += 25.0
        elif inp.escalations_requiring_rep_re_engagement_pct >= 0.20:
            score += 12.0

        return min(score, 100.0)

    def _timing_score(self, inp: HandoffInput) -> float:
        score = 0.0

        if inp.days_between_close_and_handoff_avg >= 14.0:
            score += 40.0
        elif inp.days_between_close_and_handoff_avg >= 7.0:
            score += 22.0
        elif inp.days_between_close_and_handoff_avg >= 3.0:
            score += 8.0

        if inp.handoff_meeting_attended_pct <= 0.40:
            score += 35.0
        elif inp.handoff_meeting_attended_pct <= 0.65:
            score += 18.0

        if inp.onboarding_start_delay_days_avg >= 21.0:
            score += 25.0
        elif inp.onboarding_start_delay_days_avg >= 10.0:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: HandoffInput,
                         context: float, expectation: float,
                         continuity: float, timing: float) -> HandoffPattern:
        # Oversell setup: rep promised features/outcomes that don't exist or can't be delivered
        if inp.features_promised_not_delivered_pct >= 0.20 and expectation >= 40:
            return HandoffPattern.oversell_setup

        # Expectation mismatch: customer expectations systematically misaligned
        if inp.customer_expectation_alignment_rate_pct <= 0.45 and inp.time_to_first_value_slip_rate_pct >= 0.40:
            return HandoffPattern.expectation_mismatch

        # Incomplete context transfer: rep doesn't share deal context with CS
        if context >= 40 and inp.implementation_plan_provided_pct <= 0.25:
            return HandoffPattern.incomplete_context_transfer

        # Ghosting at handoff: rep disappears after close, no onboarding involvement
        if inp.rep_involved_in_onboarding_pct <= 0.25 and continuity >= 30:
            return HandoffPattern.ghosting_at_handoff

        # Late handoff timing: drags feet on handing off to CS
        if inp.days_between_close_and_handoff_avg >= 10.0 and timing >= 30:
            return HandoffPattern.late_handoff_timing

        return HandoffPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> HandoffRisk:
        if composite >= 60:
            return HandoffRisk.critical
        if composite >= 40:
            return HandoffRisk.high
        if composite >= 20:
            return HandoffRisk.moderate
        return HandoffRisk.low

    def _severity(self, composite: float) -> HandoffSeverity:
        if composite >= 60:
            return HandoffSeverity.damaging
        if composite >= 40:
            return HandoffSeverity.disruptive
        if composite >= 20:
            return HandoffSeverity.adequate
        return HandoffSeverity.seamless

    def _action(self, risk: HandoffRisk, pattern: HandoffPattern) -> HandoffAction:
        if risk == HandoffRisk.critical:
            if pattern == HandoffPattern.oversell_setup:
                return HandoffAction.expectation_alignment_coaching
            if pattern == HandoffPattern.expectation_mismatch:
                return HandoffAction.expectation_alignment_coaching
            return HandoffAction.handoff_reset_intervention
        if risk == HandoffRisk.high:
            if pattern == HandoffPattern.incomplete_context_transfer:
                return HandoffAction.handoff_process_coaching
            if pattern == HandoffPattern.ghosting_at_handoff:
                return HandoffAction.post_sale_involvement_coaching
            return HandoffAction.customer_success_partnership_coaching
        if risk == HandoffRisk.moderate:
            return HandoffAction.handoff_process_coaching
        return HandoffAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_handoff_gap(self, composite: float, inp: HandoffInput) -> bool:
        return (
            composite >= 40
            or inp.customer_expectation_alignment_rate_pct <= 0.60
            or inp.rep_involved_in_onboarding_pct <= 0.35
        )

    def _requires_handoff_coaching(self, composite: float, inp: HandoffInput) -> bool:
        return (
            composite >= 30
            or inp.implementation_plan_provided_pct <= 0.45
            or inp.features_promised_not_delivered_pct >= 0.15
        )

    # ------------------------------------------------------------------
    # Churn risk estimate
    # ------------------------------------------------------------------

    def _estimated_churn_risk(self, inp: HandoffInput, composite: float) -> float:
        return round(
            inp.total_deals_closed
            * inp.avg_opportunity_value_usd
            * (1.0 - inp.customer_expectation_alignment_rate_pct)
            * (composite / 100.0),
            2,
        )

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: HandoffInput,
                 pattern: HandoffPattern, composite: float) -> str:
        if pattern == HandoffPattern.none and composite < 20:
            return "Customer handoff quality strong — context transfer, expectation alignment, and post-sale continuity within benchmarks"
        parts: list[str] = []
        parts.append(f"{inp.implementation_plan_provided_pct * 100:.0f}% provide implementation plan")
        parts.append(f"{inp.customer_expectation_alignment_rate_pct * 100:.0f}% expectation alignment rate")
        parts.append(f"{inp.rep_involved_in_onboarding_pct * 100:.0f}% rep involved in onboarding")
        label = pattern.value.replace("_", " ") if pattern != HandoffPattern.none else "Handoff risk"
        return f"{label.capitalize()} — {' — '.join(parts)} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: HandoffInput) -> HandoffResult:
        context     = round(self._context_score(inp), 1)
        expectation = round(self._expectation_score(inp), 1)
        continuity  = round(self._continuity_score(inp), 1)
        timing      = round(self._timing_score(inp), 1)

        composite = round(
            context * 0.30 + expectation * 0.30 + continuity * 0.25 + timing * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, context, expectation, continuity, timing)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap    = self._has_handoff_gap(composite, inp)
        coach  = self._requires_handoff_coaching(composite, inp)
        loss   = self._estimated_churn_risk(inp, composite)
        signal = self._signal(inp, pattern, composite)

        result = HandoffResult(
            rep_id=inp.rep_id,
            region=inp.region,
            handoff_risk=risk,
            handoff_pattern=pattern,
            handoff_severity=severity,
            recommended_action=action,
            context_score=context,
            expectation_score=expectation,
            continuity_score=continuity,
            timing_score=timing,
            handoff_composite=composite,
            has_handoff_gap=gap,
            requires_handoff_coaching=coach,
            estimated_churn_risk_usd=loss,
            handoff_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[HandoffInput]) -> list[HandoffResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_handoff_composite": 0.0,
                "handoff_gap_count": 0,
                "coaching_count": 0,
                "avg_context_score": 0.0,
                "avg_expectation_score": 0.0,
                "avg_continuity_score": 0.0,
                "avg_timing_score": 0.0,
                "total_estimated_churn_risk_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_ctx = total_exp = total_con = total_tim = total_loss = 0.0

        for r in self._results:
            risk_counts[r.handoff_risk.value]         = risk_counts.get(r.handoff_risk.value, 0) + 1
            pattern_counts[r.handoff_pattern.value]   = pattern_counts.get(r.handoff_pattern.value, 0) + 1
            severity_counts[r.handoff_severity.value] = severity_counts.get(r.handoff_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.handoff_composite
            total_ctx  += r.context_score
            total_exp  += r.expectation_score
            total_con  += r.continuity_score
            total_tim  += r.timing_score
            total_loss += r.estimated_churn_risk_usd

        n = len(self._results)

        return {
            "total":                              n,
            "risk_counts":                        risk_counts,
            "pattern_counts":                     pattern_counts,
            "severity_counts":                    severity_counts,
            "action_counts":                      action_counts,
            "avg_handoff_composite":              round(total_comp / n, 1),
            "handoff_gap_count":                  sum(1 for r in self._results if r.has_handoff_gap),
            "coaching_count":                     sum(1 for r in self._results if r.requires_handoff_coaching),
            "avg_context_score":                  round(total_ctx / n, 1),
            "avg_expectation_score":              round(total_exp / n, 1),
            "avg_continuity_score":               round(total_con / n, 1),
            "avg_timing_score":                   round(total_tim / n, 1),
            "total_estimated_churn_risk_usd":     round(total_loss, 2),
        }
