from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class VelocityRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class VelocityPattern(str, Enum):
    none                    = "none"
    stage_progression_stall = "stage_progression_stall"
    buyer_inactivity        = "buyer_inactivity"
    approval_bottleneck     = "approval_bottleneck"
    late_stage_drag         = "late_stage_drag"
    deal_aging              = "deal_aging"


class VelocitySeverity(str, Enum):
    healthy   = "healthy"
    slowing   = "slowing"
    degraded  = "degraded"
    stalled   = "stalled"


class VelocityAction(str, Enum):
    no_action               = "no_action"
    cycle_review            = "cycle_review"
    buyer_re_engagement     = "buyer_re_engagement"
    deal_qualification_reset= "deal_qualification_reset"
    executive_acceleration  = "executive_acceleration"


@dataclass
class VelocityDegradationInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    avg_sales_cycle_days_current: float
    avg_sales_cycle_days_benchmark: float
    avg_sales_cycle_days_prior: float
    deals_stalled_7d_plus: int
    deals_stalled_14d_plus: int
    deals_stalled_30d_plus: int
    stage_2_to_3_avg_days: float
    stage_3_to_4_avg_days: float
    stage_4_to_close_avg_days: float
    stage_benchmark_2_to_3_days: float
    stage_benchmark_3_to_4_days: float
    stage_benchmark_4_to_close_days: float
    buyer_response_time_avg_days: float
    mutual_action_plan_adherence_pct: float
    approval_cycle_avg_days: float
    approval_cycle_benchmark_days: float
    late_stage_deals_count: int
    late_stage_deals_stalled_count: int
    close_date_slipped_count: int


@dataclass
class VelocityDegradationResult:
    rep_id: str
    region: str
    velocity_risk: VelocityRisk
    velocity_pattern: VelocityPattern
    velocity_severity: VelocitySeverity
    recommended_action: VelocityAction
    cycle_length_score: float
    stage_stall_score: float
    buyer_engagement_score: float
    late_stage_drag_score: float
    velocity_composite: float
    is_velocity_degraded: bool
    requires_intervention: bool
    estimated_at_risk_deals: int
    velocity_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                    self.rep_id,
            "region":                    self.region,
            "velocity_risk":             self.velocity_risk.value,
            "velocity_pattern":          self.velocity_pattern.value,
            "velocity_severity":         self.velocity_severity.value,
            "recommended_action":        self.recommended_action.value,
            "cycle_length_score":        self.cycle_length_score,
            "stage_stall_score":         self.stage_stall_score,
            "buyer_engagement_score":    self.buyer_engagement_score,
            "late_stage_drag_score":     self.late_stage_drag_score,
            "velocity_composite":        self.velocity_composite,
            "is_velocity_degraded":      self.is_velocity_degraded,
            "requires_intervention":     self.requires_intervention,
            "estimated_at_risk_deals":   self.estimated_at_risk_deals,
            "velocity_signal":           self.velocity_signal,
        }


class SalesCycleVelocityDegradationEngine:

    def __init__(self) -> None:
        self._results: list[VelocityDegradationResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100)
    # ------------------------------------------------------------------

    def _cycle_length_score(self, inp: VelocityDegradationInput) -> float:
        score = 0.0

        # vs benchmark
        if inp.avg_sales_cycle_days_benchmark > 0:
            excess = (inp.avg_sales_cycle_days_current - inp.avg_sales_cycle_days_benchmark) / inp.avg_sales_cycle_days_benchmark
            if excess >= 0.50:
                score += 40.0
            elif excess >= 0.30:
                score += 25.0
            elif excess >= 0.15:
                score += 12.0

        # vs prior period (trend)
        if inp.avg_sales_cycle_days_prior > 0:
            trend = (inp.avg_sales_cycle_days_current - inp.avg_sales_cycle_days_prior) / inp.avg_sales_cycle_days_prior
            if trend >= 0.30:
                score += 30.0
            elif trend >= 0.15:
                score += 15.0
            elif trend >= 0.08:
                score += 6.0

        # Close date slippage
        if inp.close_date_slipped_count >= 5:
            score += 20.0
        elif inp.close_date_slipped_count >= 3:
            score += 12.0
        elif inp.close_date_slipped_count >= 1:
            score += 5.0

        # Absolute cycle length (very long = high risk regardless)
        if inp.avg_sales_cycle_days_current >= 180:
            score += 10.0
        elif inp.avg_sales_cycle_days_current >= 120:
            score += 5.0

        return min(score, 100.0)

    def _stage_stall_score(self, inp: VelocityDegradationInput) -> float:
        score = 0.0

        # Deals stalled
        if inp.deals_stalled_30d_plus >= 3:
            score += 40.0
        elif inp.deals_stalled_14d_plus >= 4:
            score += 28.0
        elif inp.deals_stalled_7d_plus >= 5:
            score += 14.0

        # Stage-specific slowdowns vs benchmarks
        total_stage_excess = 0.0
        benchmarks = [
            (inp.stage_2_to_3_avg_days, inp.stage_benchmark_2_to_3_days),
            (inp.stage_3_to_4_avg_days, inp.stage_benchmark_3_to_4_days),
            (inp.stage_4_to_close_avg_days, inp.stage_benchmark_4_to_close_days),
        ]
        for actual, bench in benchmarks:
            if bench > 0 and actual > bench:
                total_stage_excess += (actual - bench) / bench

        if total_stage_excess >= 1.50:
            score += 35.0
        elif total_stage_excess >= 0.75:
            score += 20.0
        elif total_stage_excess >= 0.30:
            score += 8.0

        # MAP adherence (low = slipping through)
        if inp.mutual_action_plan_adherence_pct < 0.40:
            score += 15.0
        elif inp.mutual_action_plan_adherence_pct < 0.60:
            score += 7.0

        return min(score, 100.0)

    def _buyer_engagement_score(self, inp: VelocityDegradationInput) -> float:
        score = 0.0

        # Buyer response time
        if inp.buyer_response_time_avg_days >= 7.0:
            score += 45.0
        elif inp.buyer_response_time_avg_days >= 4.0:
            score += 25.0
        elif inp.buyer_response_time_avg_days >= 2.0:
            score += 10.0

        # MAP adherence
        if inp.mutual_action_plan_adherence_pct < 0.30:
            score += 30.0
        elif inp.mutual_action_plan_adherence_pct < 0.50:
            score += 15.0

        # Stalled deals as % of total stalls
        if inp.deals_stalled_14d_plus >= 3:
            score += 20.0
        elif inp.deals_stalled_14d_plus >= 1:
            score += 8.0

        # Close date slippage driven by buyer
        if inp.close_date_slipped_count >= 3:
            score += 10.0

        return min(score, 100.0)

    def _late_stage_drag_score(self, inp: VelocityDegradationInput) -> float:
        score = 0.0

        # Late stage stall rate
        if inp.late_stage_deals_count > 0:
            stall_rate = inp.late_stage_deals_stalled_count / inp.late_stage_deals_count
            if stall_rate >= 0.60:
                score += 45.0
            elif stall_rate >= 0.40:
                score += 28.0
            elif stall_rate >= 0.20:
                score += 12.0

        # Approval cycle vs benchmark
        if inp.approval_cycle_benchmark_days > 0:
            approval_excess = (inp.approval_cycle_avg_days - inp.approval_cycle_benchmark_days) / inp.approval_cycle_benchmark_days
            if approval_excess >= 0.50:
                score += 30.0
            elif approval_excess >= 0.25:
                score += 15.0
            elif approval_excess >= 0.10:
                score += 6.0

        # Stage 4-to-close drag
        if inp.stage_benchmark_4_to_close_days > 0:
            close_excess = (inp.stage_4_to_close_avg_days - inp.stage_benchmark_4_to_close_days) / inp.stage_benchmark_4_to_close_days
            if close_excess >= 0.50:
                score += 20.0
            elif close_excess >= 0.25:
                score += 10.0

        # Many late-stage stalled deals
        if inp.late_stage_deals_stalled_count >= 4:
            score += 10.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: VelocityDegradationInput,
                         cycle: float, stage: float,
                         buyer: float, late: float) -> VelocityPattern:
        # Priority: deal_aging > late_stage_drag > approval_bottleneck
        #           > buyer_inactivity > stage_progression_stall > none
        if inp.deals_stalled_30d_plus >= 3 and cycle >= 20:
            return VelocityPattern.deal_aging
        if late >= 35 and inp.late_stage_deals_stalled_count >= 2:
            return VelocityPattern.late_stage_drag
        if inp.approval_cycle_benchmark_days > 0 and inp.approval_cycle_avg_days > inp.approval_cycle_benchmark_days * 1.40:
            return VelocityPattern.approval_bottleneck
        if buyer >= 25 and inp.buyer_response_time_avg_days >= 4.0:
            return VelocityPattern.buyer_inactivity
        if stage >= 20:
            return VelocityPattern.stage_progression_stall
        return VelocityPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> VelocityRisk:
        if composite >= 60:
            return VelocityRisk.critical
        if composite >= 40:
            return VelocityRisk.high
        if composite >= 20:
            return VelocityRisk.moderate
        return VelocityRisk.low

    def _severity(self, composite: float) -> VelocitySeverity:
        if composite >= 60:
            return VelocitySeverity.stalled
        if composite >= 40:
            return VelocitySeverity.degraded
        if composite >= 20:
            return VelocitySeverity.slowing
        return VelocitySeverity.healthy

    def _action(self, risk: VelocityRisk, pattern: VelocityPattern) -> VelocityAction:
        if risk == VelocityRisk.critical:
            return VelocityAction.executive_acceleration
        if risk == VelocityRisk.high:
            if pattern == VelocityPattern.deal_aging:
                return VelocityAction.deal_qualification_reset
            return VelocityAction.buyer_re_engagement
        if risk == VelocityRisk.moderate:
            return VelocityAction.cycle_review
        return VelocityAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _is_velocity_degraded(self, composite: float, inp: VelocityDegradationInput) -> bool:
        return (
            composite >= 40
            or inp.deals_stalled_30d_plus >= 3
            or (inp.avg_sales_cycle_days_benchmark > 0
                and inp.avg_sales_cycle_days_current >= inp.avg_sales_cycle_days_benchmark * 1.50)
        )

    def _requires_intervention(self, composite: float, inp: VelocityDegradationInput) -> bool:
        return (
            composite >= 30
            or inp.late_stage_deals_stalled_count >= 3
            or inp.buyer_response_time_avg_days >= 7.0
        )

    # ------------------------------------------------------------------
    # At-risk deal count
    # ------------------------------------------------------------------

    def _at_risk_deals(self, inp: VelocityDegradationInput) -> int:
        return inp.deals_stalled_14d_plus + inp.late_stage_deals_stalled_count

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: VelocityDegradationInput, pattern: VelocityPattern,
                composite: float) -> str:
        if composite < 5 and pattern == VelocityPattern.none:
            return "Sales cycle velocity within healthy parameters — no degradation signals"
        parts: list[str] = []
        if inp.avg_sales_cycle_days_benchmark > 0:
            excess_pct = (inp.avg_sales_cycle_days_current - inp.avg_sales_cycle_days_benchmark) / inp.avg_sales_cycle_days_benchmark * 100
            if excess_pct >= 10:
                parts.append(f"cycle {inp.avg_sales_cycle_days_current:.0f}d vs {inp.avg_sales_cycle_days_benchmark:.0f}d benchmark (+{excess_pct:.0f}%)")
        if inp.deals_stalled_14d_plus >= 1:
            parts.append(f"{inp.deals_stalled_14d_plus} deals stalled 14d+")
        if inp.late_stage_deals_stalled_count >= 1:
            parts.append(f"{inp.late_stage_deals_stalled_count} late-stage stalled")
        if inp.buyer_response_time_avg_days >= 3:
            parts.append(f"{inp.buyer_response_time_avg_days:.1f}d avg buyer response")
        label = pattern.value.replace("_", " ")
        summary = " — ".join(parts) if parts else "velocity degradation detected"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: VelocityDegradationInput) -> VelocityDegradationResult:
        cy = round(self._cycle_length_score(inp), 1)
        st = round(self._stage_stall_score(inp), 1)
        bu = round(self._buyer_engagement_score(inp), 1)
        la = round(self._late_stage_drag_score(inp), 1)

        composite = round(cy * 0.30 + st * 0.30 + bu * 0.25 + la * 0.15, 1)
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, cy, st, bu, la)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        is_vd = self._is_velocity_degraded(composite, inp)
        is_ri = self._requires_intervention(composite, inp)
        ar    = self._at_risk_deals(inp)
        signal= self._signal(inp, pattern, composite)

        result = VelocityDegradationResult(
            rep_id=inp.rep_id,
            region=inp.region,
            velocity_risk=risk,
            velocity_pattern=pattern,
            velocity_severity=severity,
            recommended_action=action,
            cycle_length_score=cy,
            stage_stall_score=st,
            buyer_engagement_score=bu,
            late_stage_drag_score=la,
            velocity_composite=composite,
            is_velocity_degraded=is_vd,
            requires_intervention=is_ri,
            estimated_at_risk_deals=ar,
            velocity_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[VelocityDegradationInput]) -> list[VelocityDegradationResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_velocity_composite": 0.0,
                "degraded_count": 0,
                "intervention_count": 0,
                "avg_cycle_length_score": 0.0,
                "avg_stage_stall_score": 0.0,
                "avg_buyer_engagement_score": 0.0,
                "avg_late_stage_drag_score": 0.0,
                "total_estimated_at_risk_deals": 0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_cy = total_st = total_bu = total_la = 0.0
        total_ar = 0

        for r in self._results:
            risk_counts[r.velocity_risk.value]       = risk_counts.get(r.velocity_risk.value, 0) + 1
            pattern_counts[r.velocity_pattern.value] = pattern_counts.get(r.velocity_pattern.value, 0) + 1
            severity_counts[r.velocity_severity.value] = severity_counts.get(r.velocity_severity.value, 0) + 1
            action_counts[r.recommended_action.value]  = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.velocity_composite
            total_cy   += r.cycle_length_score
            total_st   += r.stage_stall_score
            total_bu   += r.buyer_engagement_score
            total_la   += r.late_stage_drag_score
            total_ar   += r.estimated_at_risk_deals

        n = len(self._results)

        return {
            "total":                         n,
            "risk_counts":                   risk_counts,
            "pattern_counts":                pattern_counts,
            "severity_counts":               severity_counts,
            "action_counts":                 action_counts,
            "avg_velocity_composite":        round(total_comp / n, 1),
            "degraded_count":                sum(1 for r in self._results if r.is_velocity_degraded),
            "intervention_count":            sum(1 for r in self._results if r.requires_intervention),
            "avg_cycle_length_score":        round(total_cy / n, 1),
            "avg_stage_stall_score":         round(total_st / n, 1),
            "avg_buyer_engagement_score":    round(total_bu / n, 1),
            "avg_late_stage_drag_score":     round(total_la / n, 1),
            "total_estimated_at_risk_deals": total_ar,
        }
