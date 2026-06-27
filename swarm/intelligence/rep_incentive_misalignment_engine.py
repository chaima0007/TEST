from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List


class MisalignmentRating(str, Enum):
    ALIGNED = "aligned"
    MINOR = "minor"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"


class MisalignmentRisk(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class MisalignmentType(str, Enum):
    NONE = "none"
    SANDBAGGING = "sandbagging"
    CHERRY_PICKING = "cherry_picking"
    DISCOUNT_ABUSE = "discount_abuse"
    ACCOUNT_NEGLECT = "account_neglect"
    QUOTA_GAMING = "quota_gaming"


class IncentiveAction(str, Enum):
    NO_ACTION = "no_action"
    MONITOR = "monitor"
    PLAN_REVIEW = "plan_review"
    MANAGER_COACHING = "manager_coaching"
    COMP_RESTRUCTURE = "comp_restructure"


@dataclass
class RepIncentiveInput:
    rep_id: str
    rep_name: str
    region: str
    quota_usd: float
    closed_won_usd: float
    avg_deal_size_usd: float
    company_avg_deal_size_usd: float
    discount_pct_avg: float
    company_avg_discount_pct: float
    strategic_account_revenue_pct: float
    target_strategic_revenue_pct: float
    sandbagging_score: float
    late_quarter_close_pct: float
    multi_year_deal_pct: float
    target_multi_year_pct: float
    renewal_neglect_count: int
    upsell_attempt_rate_pct: float
    target_upsell_rate_pct: float
    commission_dispute_count: int
    spiff_overreliance_score: float
    forecast_accuracy_pct: float
    deal_size_variance_pct: float


@dataclass
class RepIncentiveResult:
    rep_id: str
    rep_name: str
    misalignment_rating: MisalignmentRating
    misalignment_risk: MisalignmentRisk
    primary_misalignment_type: MisalignmentType
    incentive_action: IncentiveAction
    behavior_alignment_score: float
    strategic_alignment_score: float
    discount_discipline_score: float
    revenue_quality_score: float
    misalignment_composite: float
    is_gaming_quota: bool
    requires_plan_review: bool
    estimated_revenue_risk_usd: float
    misalignment_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id": self.rep_id,
            "rep_name": self.rep_name,
            "misalignment_rating": self.misalignment_rating.value,
            "misalignment_risk": self.misalignment_risk.value,
            "primary_misalignment_type": self.primary_misalignment_type.value,
            "incentive_action": self.incentive_action.value,
            "behavior_alignment_score": self.behavior_alignment_score,
            "strategic_alignment_score": self.strategic_alignment_score,
            "discount_discipline_score": self.discount_discipline_score,
            "revenue_quality_score": self.revenue_quality_score,
            "misalignment_composite": self.misalignment_composite,
            "is_gaming_quota": self.is_gaming_quota,
            "requires_plan_review": self.requires_plan_review,
            "estimated_revenue_risk_usd": self.estimated_revenue_risk_usd,
            "misalignment_signal": self.misalignment_signal,
        }


def _behavior_alignment_score(inp: RepIncentiveInput) -> float:
    # HIGHER = more aligned behavior
    score = 0.0
    # Sandbagging — low score = sandbagger (0-35)
    if inp.sandbagging_score <= 20:
        score += 35.0
    elif inp.sandbagging_score <= 40:
        score += 25.0
    elif inp.sandbagging_score <= 60:
        score += 15.0
    elif inp.sandbagging_score <= 80:
        score += 6.0
    # Forecast accuracy (0-30)
    if inp.forecast_accuracy_pct >= 85:
        score += 30.0
    elif inp.forecast_accuracy_pct >= 70:
        score += 20.0
    elif inp.forecast_accuracy_pct >= 55:
        score += 10.0
    elif inp.forecast_accuracy_pct >= 40:
        score += 4.0
    # Late-quarter close pattern (0-20): very high % is sandbagging signal
    if inp.late_quarter_close_pct <= 30:
        score += 20.0
    elif inp.late_quarter_close_pct <= 50:
        score += 12.0
    elif inp.late_quarter_close_pct <= 70:
        score += 5.0
    # Commission disputes — more disputes = gaming (0-15)
    if inp.commission_dispute_count == 0:
        score += 15.0
    elif inp.commission_dispute_count == 1:
        score += 9.0
    elif inp.commission_dispute_count <= 2:
        score += 3.0
    return max(0.0, min(100.0, round(score, 1)))


def _strategic_alignment_score(inp: RepIncentiveInput) -> float:
    score = 0.0
    # Strategic account revenue vs target (0-35)
    if inp.target_strategic_revenue_pct > 0:
        ratio = inp.strategic_account_revenue_pct / inp.target_strategic_revenue_pct
    else:
        ratio = 1.0
    if ratio >= 0.90:
        score += 35.0
    elif ratio >= 0.70:
        score += 22.0
    elif ratio >= 0.50:
        score += 10.0
    elif ratio >= 0.30:
        score += 3.0
    # Multi-year deal rate (0-30)
    if inp.target_multi_year_pct > 0:
        my_ratio = inp.multi_year_deal_pct / inp.target_multi_year_pct
    else:
        my_ratio = 1.0
    if my_ratio >= 0.90:
        score += 30.0
    elif my_ratio >= 0.70:
        score += 20.0
    elif my_ratio >= 0.50:
        score += 8.0
    # Upsell attempt rate (0-20)
    if inp.target_upsell_rate_pct > 0:
        up_ratio = inp.upsell_attempt_rate_pct / inp.target_upsell_rate_pct
    else:
        up_ratio = 1.0
    if up_ratio >= 0.90:
        score += 20.0
    elif up_ratio >= 0.70:
        score += 12.0
    elif up_ratio >= 0.50:
        score += 5.0
    # Renewal neglect (0-15)
    if inp.renewal_neglect_count == 0:
        score += 15.0
    elif inp.renewal_neglect_count == 1:
        score += 8.0
    elif inp.renewal_neglect_count <= 3:
        score += 2.0
    return max(0.0, min(100.0, round(score, 1)))


def _discount_discipline_score(inp: RepIncentiveInput) -> float:
    score = 0.0
    # Discount vs company avg (0-50)
    discount_delta = inp.discount_pct_avg - inp.company_avg_discount_pct
    if discount_delta <= 2:
        score += 50.0
    elif discount_delta <= 5:
        score += 35.0
    elif discount_delta <= 10:
        score += 18.0
    elif discount_delta <= 15:
        score += 7.0
    # SPIFF overreliance (0-30): too dependent on SPIFFs = distorted behavior
    if inp.spiff_overreliance_score <= 20:
        score += 30.0
    elif inp.spiff_overreliance_score <= 40:
        score += 20.0
    elif inp.spiff_overreliance_score <= 60:
        score += 10.0
    elif inp.spiff_overreliance_score <= 80:
        score += 3.0
    # Deal size variance (0-20): very high variance = cherry-picking
    if inp.deal_size_variance_pct <= 20:
        score += 20.0
    elif inp.deal_size_variance_pct <= 40:
        score += 12.0
    elif inp.deal_size_variance_pct <= 65:
        score += 5.0
    return max(0.0, min(100.0, round(score, 1)))


def _revenue_quality_score(inp: RepIncentiveInput) -> float:
    score = 0.0
    # Deal size vs company avg (0-40): cherry-picking small deals = lower quality
    if inp.company_avg_deal_size_usd > 0:
        size_ratio = inp.avg_deal_size_usd / inp.company_avg_deal_size_usd
    else:
        size_ratio = 1.0
    if size_ratio >= 0.90:
        score += 40.0
    elif size_ratio >= 0.70:
        score += 26.0
    elif size_ratio >= 0.50:
        score += 12.0
    elif size_ratio >= 0.30:
        score += 4.0
    # Multi-year contribution (0-35)
    if inp.multi_year_deal_pct >= 30:
        score += 35.0
    elif inp.multi_year_deal_pct >= 20:
        score += 24.0
    elif inp.multi_year_deal_pct >= 10:
        score += 12.0
    elif inp.multi_year_deal_pct >= 5:
        score += 4.0
    # Quota attainment quality (0-25): at/above quota without gaming
    attain = inp.closed_won_usd / inp.quota_usd if inp.quota_usd > 0 else 0.0
    if 0.80 <= attain <= 1.25:
        score += 25.0
    elif 0.60 <= attain < 0.80 or 1.25 < attain <= 1.50:
        score += 15.0
    elif 0.40 <= attain < 0.60:
        score += 7.0
    return max(0.0, min(100.0, round(score, 1)))


def _misalignment_composite(behavior: float, strategic: float, discount: float, quality: float) -> float:
    # Invert: higher composite = more misaligned
    raw = (100 - behavior) * 0.30 + (100 - strategic) * 0.25 + (100 - discount) * 0.25 + (100 - quality) * 0.20
    return round(raw, 1)


def _misalignment_rating(composite: float) -> MisalignmentRating:
    if composite < 15:
        return MisalignmentRating.ALIGNED
    if composite < 30:
        return MisalignmentRating.MINOR
    if composite < 50:
        return MisalignmentRating.MODERATE
    if composite < 70:
        return MisalignmentRating.SEVERE
    return MisalignmentRating.CRITICAL


def _misalignment_risk(composite: float) -> MisalignmentRisk:
    if composite < 20:
        return MisalignmentRisk.LOW
    if composite < 40:
        return MisalignmentRisk.MODERATE
    if composite < 60:
        return MisalignmentRisk.HIGH
    return MisalignmentRisk.CRITICAL


def _primary_type(inp: RepIncentiveInput, behavior: float, strategic: float,
                  discount: float, quality: float) -> MisalignmentType:
    worst_score = min(behavior, strategic, discount, quality)
    if worst_score >= 70:
        return MisalignmentType.NONE
    # Map lowest-scoring dimension to misalignment type
    if behavior == worst_score and inp.sandbagging_score > 60:
        return MisalignmentType.SANDBAGGING
    if discount == worst_score and inp.discount_pct_avg > inp.company_avg_discount_pct + 5:
        return MisalignmentType.DISCOUNT_ABUSE
    if strategic == worst_score and inp.renewal_neglect_count >= 2:
        return MisalignmentType.ACCOUNT_NEGLECT
    if quality == worst_score and inp.avg_deal_size_usd < inp.company_avg_deal_size_usd * 0.65:
        return MisalignmentType.CHERRY_PICKING
    if behavior == worst_score and inp.late_quarter_close_pct > 60:
        return MisalignmentType.QUOTA_GAMING
    # Fallback: lowest dimension
    mapping = {
        MisalignmentType.SANDBAGGING: behavior,
        MisalignmentType.ACCOUNT_NEGLECT: strategic,
        MisalignmentType.DISCOUNT_ABUSE: discount,
        MisalignmentType.CHERRY_PICKING: quality,
    }
    return min(mapping, key=lambda k: mapping[k])


def _incentive_action(rating: MisalignmentRating) -> IncentiveAction:
    if rating == MisalignmentRating.CRITICAL:
        return IncentiveAction.COMP_RESTRUCTURE
    if rating == MisalignmentRating.SEVERE:
        return IncentiveAction.MANAGER_COACHING
    if rating == MisalignmentRating.MODERATE:
        return IncentiveAction.PLAN_REVIEW
    if rating == MisalignmentRating.MINOR:
        return IncentiveAction.MONITOR
    return IncentiveAction.NO_ACTION


def _revenue_risk_usd(inp: RepIncentiveInput, composite: float) -> float:
    risk_factor = composite / 100.0
    return round(inp.closed_won_usd * risk_factor * 0.25, 2)


def _misalignment_signal(inp: RepIncentiveInput, mtype: MisalignmentType, composite: float) -> str:
    if mtype == MisalignmentType.SANDBAGGING:
        return f"sandbagging detected — {inp.late_quarter_close_pct:.0f}% of closes in final 2 weeks, forecast accuracy {inp.forecast_accuracy_pct:.0f}%"
    if mtype == MisalignmentType.DISCOUNT_ABUSE:
        delta = inp.discount_pct_avg - inp.company_avg_discount_pct
        return f"discounting {delta:.1f}pts above company avg — margin erosion risk"
    if mtype == MisalignmentType.ACCOUNT_NEGLECT:
        return f"{inp.renewal_neglect_count} renewal neglects — strategic revenue {inp.strategic_account_revenue_pct:.0f}% vs {inp.target_strategic_revenue_pct:.0f}% target"
    if mtype == MisalignmentType.CHERRY_PICKING:
        return f"avg deal size ${inp.avg_deal_size_usd:,.0f} vs company avg ${inp.company_avg_deal_size_usd:,.0f} — cherry-picking small deals"
    if mtype == MisalignmentType.QUOTA_GAMING:
        return f"quota gaming pattern — {inp.late_quarter_close_pct:.0f}% late-quarter closes, {inp.commission_dispute_count} commission disputes"
    if composite < 15:
        return "compensation plan well-aligned — rep behavior matches company objectives"
    return f"minor incentive friction — composite misalignment score {composite:.0f}"


class RepIncentiveMisalignmentEngine:
    def __init__(self) -> None:
        self._results: dict[str, RepIncentiveResult] = {}
        self._quota_values: dict[str, float] = {}

    def assess(self, inp: RepIncentiveInput) -> RepIncentiveResult:
        behavior = _behavior_alignment_score(inp)
        strategic = _strategic_alignment_score(inp)
        discount = _discount_discipline_score(inp)
        quality = _revenue_quality_score(inp)
        composite = _misalignment_composite(behavior, strategic, discount, quality)

        rating = _misalignment_rating(composite)
        risk = _misalignment_risk(composite)
        mtype = _primary_type(inp, behavior, strategic, discount, quality)
        action = _incentive_action(rating)
        is_gaming = composite >= 40 and (inp.sandbagging_score > 60 or inp.late_quarter_close_pct > 60)
        requires_review = composite >= 30 or inp.commission_dispute_count >= 2
        rev_risk = _revenue_risk_usd(inp, composite)
        signal = _misalignment_signal(inp, mtype, composite)

        result = RepIncentiveResult(
            rep_id=inp.rep_id,
            rep_name=inp.rep_name,
            misalignment_rating=rating,
            misalignment_risk=risk,
            primary_misalignment_type=mtype,
            incentive_action=action,
            behavior_alignment_score=behavior,
            strategic_alignment_score=strategic,
            discount_discipline_score=discount,
            revenue_quality_score=quality,
            misalignment_composite=composite,
            is_gaming_quota=is_gaming,
            requires_plan_review=requires_review,
            estimated_revenue_risk_usd=rev_risk,
            misalignment_signal=signal,
        )
        self._results[inp.rep_id] = result
        self._quota_values[inp.rep_id] = inp.quota_usd
        return result

    def assess_batch(self, inputs: List[RepIncentiveInput]) -> List[RepIncentiveResult]:
        results = [self.assess(inp) for inp in inputs]
        results.sort(key=lambda r: r.misalignment_composite, reverse=True)
        return results

    def get(self, rep_id: str) -> RepIncentiveResult | None:
        return self._results.get(rep_id)

    def all_reps(self) -> List[RepIncentiveResult]:
        return sorted(self._results.values(), key=lambda r: r.misalignment_composite, reverse=True)

    def gaming_reps(self) -> List[RepIncentiveResult]:
        return [r for r in self._results.values() if r.is_gaming_quota]

    def by_rating(self, rating: MisalignmentRating) -> List[RepIncentiveResult]:
        return [r for r in self._results.values() if r.misalignment_rating == rating]

    def by_risk(self, risk: MisalignmentRisk) -> List[RepIncentiveResult]:
        return [r for r in self._results.values() if r.misalignment_risk == risk]

    def total_revenue_risk_usd(self) -> float:
        return round(sum(r.estimated_revenue_risk_usd for r in self._results.values()), 2)

    def avg_misalignment_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.misalignment_composite for r in self._results.values()) / len(self._results), 1)

    def reset(self) -> None:
        self._results.clear()
        self._quota_values.clear()

    def summary(self) -> dict:
        results = list(self._results.values())
        n = len(results)
        rating_counts: dict[str, int] = {}
        risk_counts: dict[str, int] = {}
        type_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        for r in results:
            rating_counts[r.misalignment_rating.value] = rating_counts.get(r.misalignment_rating.value, 0) + 1
            risk_counts[r.misalignment_risk.value] = risk_counts.get(r.misalignment_risk.value, 0) + 1
            type_counts[r.primary_misalignment_type.value] = type_counts.get(r.primary_misalignment_type.value, 0) + 1
            action_counts[r.incentive_action.value] = action_counts.get(r.incentive_action.value, 0) + 1
        return {
            "total": n,
            "rating_counts": rating_counts,
            "risk_counts": risk_counts,
            "type_counts": type_counts,
            "action_counts": action_counts,
            "avg_misalignment_composite": self.avg_misalignment_composite(),
            "gaming_quota_count": len(self.gaming_reps()),
            "plan_review_count": sum(1 for r in results if r.requires_plan_review),
            "avg_behavior_alignment_score": round(sum(r.behavior_alignment_score for r in results) / n, 1) if n else 0.0,
            "avg_strategic_alignment_score": round(sum(r.strategic_alignment_score for r in results) / n, 1) if n else 0.0,
            "avg_discount_discipline_score": round(sum(r.discount_discipline_score for r in results) / n, 1) if n else 0.0,
            "avg_revenue_quality_score": round(sum(r.revenue_quality_score for r in results) / n, 1) if n else 0.0,
            "total_revenue_risk_usd": self.total_revenue_risk_usd(),
        }
