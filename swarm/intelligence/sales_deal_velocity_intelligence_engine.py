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
    stuck_deals             = "stuck_deals"
    slow_progression        = "slow_progression"
    late_stage_stall        = "late_stage_stall"
    early_stage_bottleneck  = "early_stage_bottleneck"
    cycle_time_bloat        = "cycle_time_bloat"


class VelocitySeverity(str, Enum):
    flowing    = "flowing"
    developing = "developing"
    slowing    = "slowing"
    stalled    = "stalled"


class VelocityAction(str, Enum):
    no_action                  = "no_action"
    deal_progression_coaching  = "deal_progression_coaching"
    pipeline_review            = "pipeline_review"
    stage_optimization         = "stage_optimization"
    deal_rescue                = "deal_rescue"
    cycle_time_reduction       = "cycle_time_reduction"


@dataclass
class DealVelocityInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    total_pipeline_deals: int
    avg_deal_cycle_days: float
    deals_over_180_days: int
    deals_over_90_days: int
    avg_days_in_current_stage: float
    stage_advancement_count: int
    deals_stalled_30_days: int
    deals_stalled_60_days: int
    lost_deals_due_to_age: int
    avg_stage_1_days: float
    avg_stage_2_days: float
    avg_stage_3_days: float
    avg_stage_4_days: float
    deals_close_date_slipped_count: int
    avg_close_date_slip_days: float
    follow_up_response_rate_pct: float
    mutual_action_plan_usage_pct: float
    avg_deal_size_pipeline_usd: float
    deals_moved_backward_count: int


@dataclass
class DealVelocityResult:
    rep_id: str
    region: str
    velocity_risk: VelocityRisk
    velocity_pattern: VelocityPattern
    velocity_severity: VelocitySeverity
    recommended_action: VelocityAction
    progression_speed_score: float
    pipeline_stagnation_score: float
    stage_efficiency_score: float
    deal_momentum_score: float
    deal_velocity_composite: float
    has_velocity_gap: bool
    requires_deal_coaching: bool
    estimated_revenue_delayed_usd: float
    velocity_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "velocity_risk":                    self.velocity_risk.value,
            "velocity_pattern":                 self.velocity_pattern.value,
            "velocity_severity":                self.velocity_severity.value,
            "recommended_action":               self.recommended_action.value,
            "progression_speed_score":          self.progression_speed_score,
            "pipeline_stagnation_score":        self.pipeline_stagnation_score,
            "stage_efficiency_score":           self.stage_efficiency_score,
            "deal_momentum_score":              self.deal_momentum_score,
            "deal_velocity_composite":          self.deal_velocity_composite,
            "has_velocity_gap":                 self.has_velocity_gap,
            "requires_deal_coaching":           self.requires_deal_coaching,
            "estimated_revenue_delayed_usd":    self.estimated_revenue_delayed_usd,
            "velocity_signal":                  self.velocity_signal,
        }


class SalesDealVelocityIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[DealVelocityResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _progression_speed_score(self, inp: DealVelocityInput) -> float:
        score = 0.0

        if inp.avg_deal_cycle_days >= 180:
            score += 45.0
        elif inp.avg_deal_cycle_days >= 90:
            score += 25.0
        elif inp.avg_deal_cycle_days >= 60:
            score += 10.0

        total = max(inp.total_pipeline_deals, 1)
        old_rate = inp.deals_over_90_days / total
        if old_rate >= 0.40:
            score += 30.0
        elif old_rate >= 0.25:
            score += 15.0
        elif old_rate >= 0.10:
            score += 5.0

        if inp.avg_days_in_current_stage >= 30:
            score += 15.0
        elif inp.avg_days_in_current_stage >= 15:
            score += 7.0

        return min(score, 100.0)

    def _pipeline_stagnation_score(self, inp: DealVelocityInput) -> float:
        score = 0.0
        total = max(inp.total_pipeline_deals, 1)

        stall_rate = inp.deals_stalled_30_days / total
        if stall_rate >= 0.40:
            score += 40.0
        elif stall_rate >= 0.25:
            score += 20.0
        elif stall_rate >= 0.10:
            score += 8.0

        deep_stall_rate = inp.deals_stalled_60_days / total
        if deep_stall_rate >= 0.20:
            score += 30.0
        elif deep_stall_rate >= 0.10:
            score += 15.0

        if inp.lost_deals_due_to_age >= 3:
            score += 20.0
        elif inp.lost_deals_due_to_age >= 1:
            score += 10.0

        return min(score, 100.0)

    def _stage_efficiency_score(self, inp: DealVelocityInput) -> float:
        score = 0.0

        if inp.avg_stage_3_days >= 30:
            score += 30.0
        elif inp.avg_stage_3_days >= 20:
            score += 15.0
        elif inp.avg_stage_3_days >= 12:
            score += 5.0

        if inp.avg_stage_4_days >= 30:
            score += 30.0
        elif inp.avg_stage_4_days >= 20:
            score += 15.0

        if inp.deals_close_date_slipped_count >= 5:
            score += 25.0
        elif inp.deals_close_date_slipped_count >= 3:
            score += 12.0
        elif inp.deals_close_date_slipped_count >= 1:
            score += 5.0

        return min(score, 100.0)

    def _deal_momentum_score(self, inp: DealVelocityInput) -> float:
        score = 0.0
        total = max(inp.total_pipeline_deals, 1)

        backward_rate = inp.deals_moved_backward_count / total
        if backward_rate >= 0.20:
            score += 40.0
        elif backward_rate >= 0.10:
            score += 20.0
        elif backward_rate >= 0.05:
            score += 8.0

        if inp.follow_up_response_rate_pct < 0.40:
            score += 30.0
        elif inp.follow_up_response_rate_pct < 0.60:
            score += 15.0

        if inp.mutual_action_plan_usage_pct < 0.20:
            score += 20.0
        elif inp.mutual_action_plan_usage_pct < 0.40:
            score += 10.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: DealVelocityInput,
                         speed: float, stagnation: float,
                         efficiency: float, momentum: float) -> VelocityPattern:
        total = max(inp.total_pipeline_deals, 1)
        stall_rate = inp.deals_stalled_30_days / total
        if stagnation >= 35 and stall_rate >= 0.30:
            return VelocityPattern.stuck_deals

        if speed >= 35 and inp.avg_deal_cycle_days >= 90:
            return VelocityPattern.slow_progression

        if efficiency >= 30 and (inp.avg_stage_3_days >= 25 or inp.avg_stage_4_days >= 25):
            return VelocityPattern.late_stage_stall

        if speed >= 25 and inp.avg_stage_1_days >= 20:
            return VelocityPattern.early_stage_bottleneck

        if efficiency >= 20 and inp.avg_close_date_slip_days >= 30:
            return VelocityPattern.cycle_time_bloat

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
            return VelocitySeverity.slowing
        if composite >= 20:
            return VelocitySeverity.developing
        return VelocitySeverity.flowing

    def _action(self, risk: VelocityRisk, pattern: VelocityPattern) -> VelocityAction:
        if risk == VelocityRisk.critical:
            if pattern == VelocityPattern.stuck_deals:
                return VelocityAction.deal_rescue
            if pattern == VelocityPattern.slow_progression:
                return VelocityAction.cycle_time_reduction
            return VelocityAction.pipeline_review
        if risk == VelocityRisk.high:
            if pattern == VelocityPattern.late_stage_stall:
                return VelocityAction.deal_progression_coaching
            if pattern == VelocityPattern.early_stage_bottleneck:
                return VelocityAction.stage_optimization
            return VelocityAction.deal_progression_coaching
        if risk == VelocityRisk.moderate:
            return VelocityAction.deal_progression_coaching
        return VelocityAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_velocity_gap(self, composite: float,
                           inp: DealVelocityInput) -> bool:
        return (
            composite >= 40
            or inp.deals_stalled_60_days >= 3
            or inp.avg_deal_cycle_days >= 120
        )

    def _requires_deal_coaching(self, composite: float,
                                 inp: DealVelocityInput) -> bool:
        total = max(inp.total_pipeline_deals, 1)
        stall_rate = inp.deals_stalled_30_days / total
        return (
            composite >= 30
            or stall_rate >= 0.25
            or inp.avg_days_in_current_stage >= 30
        )

    # ------------------------------------------------------------------
    # Revenue delayed
    # ------------------------------------------------------------------

    def _estimated_revenue_delayed(self, inp: DealVelocityInput,
                                    composite: float) -> float:
        return round(
            inp.deals_stalled_30_days * inp.avg_deal_size_pipeline_usd * (composite / 100.0), 2
        )

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: DealVelocityInput,
                 pattern: VelocityPattern, composite: float) -> str:
        if pattern == VelocityPattern.none and composite < 20:
            return "Deal velocity and pipeline progression within healthy benchmarks"
        parts: list[str] = []
        if inp.avg_deal_cycle_days >= 45:
            parts.append(f"{inp.avg_deal_cycle_days:.0f}d avg cycle")
        if inp.deals_stalled_30_days >= 1:
            parts.append(f"{inp.deals_stalled_30_days} stalled deals")
        if inp.deals_close_date_slipped_count >= 1:
            parts.append(f"{inp.deals_close_date_slipped_count} close dates slipped")
        label = pattern.value.replace("_", " ") if pattern != VelocityPattern.none else "Velocity risk"
        summary = " — ".join(parts) if parts else "deal progression slowing"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: DealVelocityInput) -> DealVelocityResult:
        speed      = round(self._progression_speed_score(inp), 1)
        stagnation = round(self._pipeline_stagnation_score(inp), 1)
        efficiency = round(self._stage_efficiency_score(inp), 1)
        momentum   = round(self._deal_momentum_score(inp), 1)

        composite = round(
            speed * 0.30 + stagnation * 0.30 + efficiency * 0.25 + momentum * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, speed, stagnation, efficiency, momentum)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap      = self._has_velocity_gap(composite, inp)
        coaching = self._requires_deal_coaching(composite, inp)
        delayed  = self._estimated_revenue_delayed(inp, composite)
        signal   = self._signal(inp, pattern, composite)

        result = DealVelocityResult(
            rep_id=inp.rep_id,
            region=inp.region,
            velocity_risk=risk,
            velocity_pattern=pattern,
            velocity_severity=severity,
            recommended_action=action,
            progression_speed_score=speed,
            pipeline_stagnation_score=stagnation,
            stage_efficiency_score=efficiency,
            deal_momentum_score=momentum,
            deal_velocity_composite=composite,
            has_velocity_gap=gap,
            requires_deal_coaching=coaching,
            estimated_revenue_delayed_usd=delayed,
            velocity_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[DealVelocityInput]) -> list[DealVelocityResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_deal_velocity_composite": 0.0,
                "velocity_gap_count": 0,
                "deal_coaching_count": 0,
                "avg_progression_speed_score": 0.0,
                "avg_pipeline_stagnation_score": 0.0,
                "avg_stage_efficiency_score": 0.0,
                "avg_deal_momentum_score": 0.0,
                "total_estimated_revenue_delayed_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_sp = total_stag = total_eff = total_mom = total_del = 0.0

        for r in self._results:
            risk_counts[r.velocity_risk.value]       = risk_counts.get(r.velocity_risk.value, 0) + 1
            pattern_counts[r.velocity_pattern.value] = pattern_counts.get(r.velocity_pattern.value, 0) + 1
            severity_counts[r.velocity_severity.value] = severity_counts.get(r.velocity_severity.value, 0) + 1
            action_counts[r.recommended_action.value]  = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.deal_velocity_composite
            total_sp   += r.progression_speed_score
            total_stag += r.pipeline_stagnation_score
            total_eff  += r.stage_efficiency_score
            total_mom  += r.deal_momentum_score
            total_del  += r.estimated_revenue_delayed_usd

        n = len(self._results)

        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_deal_velocity_composite":          round(total_comp / n, 1),
            "velocity_gap_count":                   sum(1 for r in self._results if r.has_velocity_gap),
            "deal_coaching_count":                  sum(1 for r in self._results if r.requires_deal_coaching),
            "avg_progression_speed_score":          round(total_sp / n, 1),
            "avg_pipeline_stagnation_score":        round(total_stag / n, 1),
            "avg_stage_efficiency_score":           round(total_eff / n, 1),
            "avg_deal_momentum_score":              round(total_mom / n, 1),
            "total_estimated_revenue_delayed_usd":  round(total_del, 2),
        }
