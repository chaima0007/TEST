from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List


class CapacityStatus(str, Enum):
    SURPLUS = "surplus"
    BALANCED = "balanced"
    GAP = "gap"
    CRITICAL_GAP = "critical_gap"


class CapacityRisk(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class GrowthConstraint(str, Enum):
    NONE = "none"
    HEADCOUNT = "headcount"
    PIPELINE = "pipeline"
    PRODUCTIVITY = "productivity"
    HIRING_SPEED = "hiring_speed"


class CapacityAction(str, Enum):
    MAINTAIN = "maintain"
    ACCELERATE_HIRING = "accelerate_hiring"
    RESTRUCTURE_TERRITORY = "restructure_territory"
    REDUCE_TARGET = "reduce_target"


@dataclass
class SalesCapacityInput:
    region_id: str
    region_name: str
    region_head: str
    annual_revenue_target_usd: float
    current_headcount: int
    avg_productivity_per_rep_usd: float
    avg_ramp_months: float
    expected_attrition_rate_pct: float
    current_pipeline_coverage_ratio: float
    open_headcount_req: int
    time_to_hire_days: float
    quota_attainment_pct: float
    avg_deal_size_usd: float
    avg_sales_cycle_days: float
    win_rate_pct: float
    lead_volume_monthly: int
    lead_to_opportunity_rate_pct: float
    expansion_revenue_pct: float
    partner_revenue_pct: float
    seasonal_peak_factor: float
    territory_saturation_pct: float
    rep_productivity_trend: float


@dataclass
class SalesCapacityResult:
    region_id: str
    region_name: str
    capacity_status: CapacityStatus
    capacity_risk: CapacityRisk
    growth_constraint: GrowthConstraint
    capacity_action: CapacityAction
    required_headcount: int
    capacity_gap: int
    productivity_score: float
    pipeline_health_score: float
    hiring_efficiency_score: float
    capacity_composite: float
    is_understaffed: bool
    revenue_at_risk_usd: float
    capacity_signal: str

    def to_dict(self) -> dict:
        return {
            "region_id": self.region_id,
            "region_name": self.region_name,
            "capacity_status": self.capacity_status.value,
            "capacity_risk": self.capacity_risk.value,
            "growth_constraint": self.growth_constraint.value,
            "capacity_action": self.capacity_action.value,
            "required_headcount": self.required_headcount,
            "capacity_gap": self.capacity_gap,
            "productivity_score": self.productivity_score,
            "pipeline_health_score": self.pipeline_health_score,
            "hiring_efficiency_score": self.hiring_efficiency_score,
            "capacity_composite": self.capacity_composite,
            "is_understaffed": self.is_understaffed,
            "revenue_at_risk_usd": self.revenue_at_risk_usd,
            "capacity_signal": self.capacity_signal,
        }


def _required_headcount(inp: SalesCapacityInput) -> int:
    if inp.avg_productivity_per_rep_usd <= 0:
        return inp.current_headcount
    # Adjust for attrition buffer
    attrition_factor = 1.0 + (inp.expected_attrition_rate_pct / 100.0) * 0.5
    # Adjust for ramp: ramping reps produce at ~50% productivity on average
    ramp_factor = 1.0 + (inp.avg_ramp_months / 12.0) * 0.5
    effective_productivity = inp.avg_productivity_per_rep_usd * inp.quota_attainment_pct / 100.0
    if effective_productivity <= 0:
        effective_productivity = inp.avg_productivity_per_rep_usd
    raw = (inp.annual_revenue_target_usd / effective_productivity) * attrition_factor * ramp_factor
    return max(1, round(raw))


def _productivity_score(inp: SalesCapacityInput) -> float:
    score = 0.0
    # Attainment vs target (0-35)
    if inp.quota_attainment_pct >= 90:
        score += 35.0
    elif inp.quota_attainment_pct >= 80:
        score += 26.0
    elif inp.quota_attainment_pct >= 65:
        score += 16.0
    elif inp.quota_attainment_pct >= 50:
        score += 8.0
    # Productivity trend (0-25): positive trend good
    if inp.rep_productivity_trend >= 0.5:
        score += 25.0
    elif inp.rep_productivity_trend >= 0:
        score += 18.0
    elif inp.rep_productivity_trend >= -0.3:
        score += 10.0
    # Win rate (0-25)
    if inp.win_rate_pct >= 30:
        score += 25.0
    elif inp.win_rate_pct >= 20:
        score += 18.0
    elif inp.win_rate_pct >= 12:
        score += 10.0
    elif inp.win_rate_pct >= 5:
        score += 4.0
    # Territory saturation (0-15): not over-saturated
    if inp.territory_saturation_pct <= 40:
        score += 15.0
    elif inp.territory_saturation_pct <= 60:
        score += 10.0
    elif inp.territory_saturation_pct <= 80:
        score += 4.0
    return max(0.0, min(100.0, round(score, 1)))


def _pipeline_health_score(inp: SalesCapacityInput) -> float:
    score = 0.0
    # Coverage ratio (0-35): 3-5x ideal
    if 3.0 <= inp.current_pipeline_coverage_ratio <= 5.0:
        score += 35.0
    elif 2.0 <= inp.current_pipeline_coverage_ratio < 3.0:
        score += 24.0
    elif 5.0 < inp.current_pipeline_coverage_ratio <= 7.0:
        score += 20.0
    elif 1.0 <= inp.current_pipeline_coverage_ratio < 2.0:
        score += 10.0
    # Lead volume (0-25): enough leads per rep
    leads_per_rep = inp.lead_volume_monthly / max(1, inp.current_headcount)
    if leads_per_rep >= 30:
        score += 25.0
    elif leads_per_rep >= 20:
        score += 18.0
    elif leads_per_rep >= 10:
        score += 10.0
    elif leads_per_rep >= 5:
        score += 4.0
    # Lead-to-opp conversion (0-20)
    if inp.lead_to_opportunity_rate_pct >= 20:
        score += 20.0
    elif inp.lead_to_opportunity_rate_pct >= 12:
        score += 14.0
    elif inp.lead_to_opportunity_rate_pct >= 6:
        score += 7.0
    # Expansion revenue contribution (0-20): recurring expansion reduces new logo pressure
    if inp.expansion_revenue_pct >= 30:
        score += 20.0
    elif inp.expansion_revenue_pct >= 20:
        score += 14.0
    elif inp.expansion_revenue_pct >= 10:
        score += 7.0
    return max(0.0, min(100.0, round(score, 1)))


def _hiring_efficiency_score(inp: SalesCapacityInput) -> float:
    score = 0.0
    # Time to hire (0-40): faster is better
    if inp.time_to_hire_days <= 30:
        score += 40.0
    elif inp.time_to_hire_days <= 60:
        score += 28.0
    elif inp.time_to_hire_days <= 90:
        score += 16.0
    elif inp.time_to_hire_days <= 120:
        score += 6.0
    # Attrition rate (0-35)
    if inp.expected_attrition_rate_pct <= 10:
        score += 35.0
    elif inp.expected_attrition_rate_pct <= 20:
        score += 24.0
    elif inp.expected_attrition_rate_pct <= 30:
        score += 12.0
    elif inp.expected_attrition_rate_pct <= 40:
        score += 4.0
    # Open req ratio (0-25): not too many open roles relative to team size
    if inp.current_headcount > 0:
        open_ratio = inp.open_headcount_req / inp.current_headcount
    else:
        open_ratio = 1.0
    if open_ratio <= 0.1:
        score += 25.0
    elif open_ratio <= 0.2:
        score += 18.0
    elif open_ratio <= 0.35:
        score += 8.0
    return max(0.0, min(100.0, round(score, 1)))


def _composite(productivity: float, pipeline: float, hiring: float) -> float:
    raw = productivity * 0.40 + pipeline * 0.35 + hiring * 0.25
    return round(raw, 1)


def _capacity_status(gap: int, current_headcount: int) -> CapacityStatus:
    if gap <= -3:
        return CapacityStatus.SURPLUS
    if gap <= 0:
        return CapacityStatus.BALANCED
    if gap <= 3:
        return CapacityStatus.GAP
    return CapacityStatus.CRITICAL_GAP


def _capacity_risk(composite: float, gap: int) -> CapacityRisk:
    if composite < 25 or gap >= 8:
        return CapacityRisk.CRITICAL
    if composite < 40 or gap >= 5:
        return CapacityRisk.HIGH
    if composite < 60 or gap >= 2:
        return CapacityRisk.MODERATE
    return CapacityRisk.LOW


def _growth_constraint(inp: SalesCapacityInput, gap: int) -> GrowthConstraint:
    if gap >= 3 and inp.time_to_hire_days > 90:
        return GrowthConstraint.HIRING_SPEED
    if gap >= 3:
        return GrowthConstraint.HEADCOUNT
    if inp.current_pipeline_coverage_ratio < 2.0:
        return GrowthConstraint.PIPELINE
    if inp.quota_attainment_pct < 60:
        return GrowthConstraint.PRODUCTIVITY
    return GrowthConstraint.NONE


def _capacity_action(risk: CapacityRisk, status: CapacityStatus) -> CapacityAction:
    if status == CapacityStatus.CRITICAL_GAP:
        return CapacityAction.ACCELERATE_HIRING
    if status == CapacityStatus.GAP:
        if risk == CapacityRisk.HIGH:
            return CapacityAction.ACCELERATE_HIRING
        return CapacityAction.RESTRUCTURE_TERRITORY
    if risk in (CapacityRisk.CRITICAL, CapacityRisk.HIGH):
        return CapacityAction.REDUCE_TARGET
    return CapacityAction.MAINTAIN


def _revenue_at_risk_usd(inp: SalesCapacityInput, gap: int, composite: float) -> float:
    if gap <= 0:
        risk_factor = (100.0 - composite) / 200.0  # low risk from low composite even if staffed
    else:
        rep_gap_revenue = gap * inp.avg_productivity_per_rep_usd * inp.quota_attainment_pct / 100.0
        composite_risk = inp.annual_revenue_target_usd * (100.0 - composite) / 400.0
        risk_factor = 0.0
        return round(rep_gap_revenue + composite_risk, 2)
    return round(inp.annual_revenue_target_usd * risk_factor, 2)


def _capacity_signal(inp: SalesCapacityInput, gap: int, constraint: GrowthConstraint) -> str:
    if gap >= 5:
        return f"critical headcount gap of {gap} reps — {inp.annual_revenue_target_usd/1e6:.1f}M target at risk"
    if constraint == GrowthConstraint.HIRING_SPEED:
        return f"hiring bottleneck — avg {inp.time_to_hire_days:.0f} days to hire with {gap} open roles needed"
    if constraint == GrowthConstraint.PIPELINE:
        return f"pipeline coverage {inp.current_pipeline_coverage_ratio:.1f}x — insufficient to support target attainment"
    if constraint == GrowthConstraint.PRODUCTIVITY:
        return f"rep productivity at {inp.quota_attainment_pct:.0f}% — headcount increase won't solve attainment issue"
    if gap > 0:
        return f"headcount gap of {gap} reps against target — accelerate recruiting"
    if gap < -2:
        return f"surplus of {abs(gap)} reps — consider territory expansion or increased quotas"
    return f"capacity balanced — {inp.current_headcount} reps supporting {inp.annual_revenue_target_usd/1e6:.1f}M target"


class SalesCapacityPlanningEngine:
    def __init__(self) -> None:
        self._results: dict[str, SalesCapacityResult] = {}

    def assess(self, inp: SalesCapacityInput) -> SalesCapacityResult:
        required = _required_headcount(inp)
        gap = required - inp.current_headcount

        productivity = _productivity_score(inp)
        pipeline = _pipeline_health_score(inp)
        hiring = _hiring_efficiency_score(inp)
        composite = _composite(productivity, pipeline, hiring)

        status = _capacity_status(gap, inp.current_headcount)
        risk = _capacity_risk(composite, gap)
        constraint = _growth_constraint(inp, gap)
        action = _capacity_action(risk, status)
        is_understaffed = gap > 0
        rev_at_risk = _revenue_at_risk_usd(inp, gap, composite)
        signal = _capacity_signal(inp, gap, constraint)

        result = SalesCapacityResult(
            region_id=inp.region_id,
            region_name=inp.region_name,
            capacity_status=status,
            capacity_risk=risk,
            growth_constraint=constraint,
            capacity_action=action,
            required_headcount=required,
            capacity_gap=gap,
            productivity_score=productivity,
            pipeline_health_score=pipeline,
            hiring_efficiency_score=hiring,
            capacity_composite=composite,
            is_understaffed=is_understaffed,
            revenue_at_risk_usd=rev_at_risk,
            capacity_signal=signal,
        )
        self._results[inp.region_id] = result
        return result

    def assess_batch(self, inputs: List[SalesCapacityInput]) -> List[SalesCapacityResult]:
        results = [self.assess(inp) for inp in inputs]
        results.sort(key=lambda r: r.capacity_composite, reverse=True)
        return results

    def get(self, region_id: str) -> SalesCapacityResult | None:
        return self._results.get(region_id)

    def all_regions(self) -> List[SalesCapacityResult]:
        return sorted(self._results.values(), key=lambda r: r.capacity_composite, reverse=True)

    def understaffed_regions(self) -> List[SalesCapacityResult]:
        return [r for r in self._results.values() if r.is_understaffed]

    def by_status(self, status: CapacityStatus) -> List[SalesCapacityResult]:
        return [r for r in self._results.values() if r.capacity_status == status]

    def by_risk(self, risk: CapacityRisk) -> List[SalesCapacityResult]:
        return [r for r in self._results.values() if r.capacity_risk == risk]

    def total_headcount_gap(self) -> int:
        return sum(max(0, r.capacity_gap) for r in self._results.values())

    def total_revenue_at_risk_usd(self) -> float:
        return round(sum(r.revenue_at_risk_usd for r in self._results.values()), 2)

    def avg_capacity_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.capacity_composite for r in self._results.values()) / len(self._results), 1)

    def reset(self) -> None:
        self._results.clear()

    def summary(self) -> dict:
        results = list(self._results.values())
        n = len(results)
        status_counts: dict[str, int] = {}
        risk_counts: dict[str, int] = {}
        constraint_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        for r in results:
            status_counts[r.capacity_status.value] = status_counts.get(r.capacity_status.value, 0) + 1
            risk_counts[r.capacity_risk.value] = risk_counts.get(r.capacity_risk.value, 0) + 1
            constraint_counts[r.growth_constraint.value] = constraint_counts.get(r.growth_constraint.value, 0) + 1
            action_counts[r.capacity_action.value] = action_counts.get(r.capacity_action.value, 0) + 1
        total_req = sum(r.required_headcount for r in results)
        total_curr = sum(r.required_headcount - r.capacity_gap for r in results)
        return {
            "total": n,
            "status_counts": status_counts,
            "risk_counts": risk_counts,
            "constraint_counts": constraint_counts,
            "action_counts": action_counts,
            "avg_capacity_composite": self.avg_capacity_composite(),
            "understaffed_count": len(self.understaffed_regions()),
            "total_headcount_gap": self.total_headcount_gap(),
            "avg_productivity_score": round(sum(r.productivity_score for r in results) / n, 1) if n else 0.0,
            "avg_pipeline_health_score": round(sum(r.pipeline_health_score for r in results) / n, 1) if n else 0.0,
            "avg_hiring_efficiency_score": round(sum(r.hiring_efficiency_score for r in results) / n, 1) if n else 0.0,
            "total_revenue_at_risk_usd": self.total_revenue_at_risk_usd(),
            "optimal_headcount_range": f"{total_curr}-{total_req}",
        }
