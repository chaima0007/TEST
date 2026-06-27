from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List


class FairnessRating(str, Enum):
    VERY_FAIR = "very_fair"
    FAIR = "fair"
    QUESTIONABLE = "questionable"
    UNFAIR = "unfair"


class FairnessRisk(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class BiasDirection(str, Enum):
    OVER_QUOTED = "over_quoted"
    UNDER_QUOTED = "under_quoted"
    BALANCED = "balanced"


class QuotaAction(str, Enum):
    MAINTAIN = "maintain"
    RECALIBRATE_TERRITORY = "recalibrate_territory"
    REDUCE_QUOTA = "reduce_quota"
    INCREASE_QUOTA = "increase_quota"


@dataclass
class QuotaFairnessInput:
    rep_id: str
    rep_name: str
    region: str
    annual_quota_usd: float
    territory_market_potential_usd: float
    tenure_months: int
    previous_year_attainment_pct: float
    industry_growth_rate_pct: float
    competitive_intensity_score: float
    account_count: int
    new_logo_quota_pct: float
    avg_deal_size_usd: float
    sales_cycle_avg_days: int
    team_avg_quota_usd: float
    team_avg_attainment_pct: float
    years_experience: float
    product_maturity_score: float
    territory_adjusted_last_year: int
    peer_quota_variance_pct: float
    quota_increase_yoy_pct: float
    ramp_adjustment_applied: int
    manager_override_pct: float


@dataclass
class QuotaFairnessResult:
    rep_id: str
    rep_name: str
    fairness_rating: FairnessRating
    fairness_risk: FairnessRisk
    bias_direction: BiasDirection
    quota_action: QuotaAction
    market_alignment_score: float
    experience_alignment_score: float
    peer_equity_score: float
    attainment_sustainability_score: float
    fairness_composite: float
    is_over_quoted: bool
    is_under_quoted: bool
    estimated_fair_quota_usd: float
    fairness_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id": self.rep_id,
            "rep_name": self.rep_name,
            "fairness_rating": self.fairness_rating.value,
            "fairness_risk": self.fairness_risk.value,
            "bias_direction": self.bias_direction.value,
            "quota_action": self.quota_action.value,
            "market_alignment_score": self.market_alignment_score,
            "experience_alignment_score": self.experience_alignment_score,
            "peer_equity_score": self.peer_equity_score,
            "attainment_sustainability_score": self.attainment_sustainability_score,
            "fairness_composite": self.fairness_composite,
            "is_over_quoted": self.is_over_quoted,
            "is_under_quoted": self.is_under_quoted,
            "estimated_fair_quota_usd": self.estimated_fair_quota_usd,
            "fairness_signal": self.fairness_signal,
        }


def _market_alignment_score(inp: QuotaFairnessInput) -> float:
    score = 0.0
    # Quota vs territory potential (0-40): ideal is 20-40% of SAM
    if inp.territory_market_potential_usd > 0:
        quota_pct = (inp.annual_quota_usd / inp.territory_market_potential_usd) * 100.0
    else:
        quota_pct = 50.0
    if 20 <= quota_pct <= 40:
        score += 40.0
    elif 15 <= quota_pct < 20 or 40 < quota_pct <= 50:
        score += 28.0
    elif 10 <= quota_pct < 15 or 50 < quota_pct <= 65:
        score += 16.0
    elif quota_pct < 10 or quota_pct > 65:
        score += 4.0
    # Industry growth adjustment (0-20)
    if inp.industry_growth_rate_pct >= 20:
        score += 20.0
    elif inp.industry_growth_rate_pct >= 10:
        score += 15.0
    elif inp.industry_growth_rate_pct >= 0:
        score += 10.0
    elif inp.industry_growth_rate_pct >= -10:
        score += 5.0
    # Competitive intensity vs quota (0-20): high competition should mean lower quota expectation
    if inp.competitive_intensity_score >= 80:
        score += 5.0  # Very competitive markets — quota might be too high
    elif inp.competitive_intensity_score >= 60:
        score += 12.0
    elif inp.competitive_intensity_score >= 40:
        score += 18.0
    else:
        score += 20.0
    # Product maturity (0-20): mature products easier to sell
    score += inp.product_maturity_score * 0.20
    return max(0.0, min(100.0, round(score, 1)))


def _experience_alignment_score(inp: QuotaFairnessInput) -> float:
    score = 0.0
    # Years of experience vs quota size (0-30)
    if inp.years_experience >= 8:
        score += 30.0
    elif inp.years_experience >= 5:
        score += 22.0
    elif inp.years_experience >= 3:
        score += 15.0
    elif inp.years_experience >= 1:
        score += 8.0
    # Ramp adjustment (0-20): ramping reps should get reduction
    if inp.ramp_adjustment_applied:
        score += 20.0
    elif inp.tenure_months < 6:
        score += 5.0  # new rep without ramp adjustment is unfair
    else:
        score += 20.0
    # Previous year attainment (0-30): quota should reflect actual performance
    if inp.previous_year_attainment_pct >= 90:
        score += 30.0
    elif inp.previous_year_attainment_pct >= 75:
        score += 22.0
    elif inp.previous_year_attainment_pct >= 60:
        score += 15.0
    elif inp.previous_year_attainment_pct >= 40:
        score += 8.0
    # YoY quota increase reasonableness (0-20)
    if inp.quota_increase_yoy_pct <= 10:
        score += 20.0
    elif inp.quota_increase_yoy_pct <= 20:
        score += 14.0
    elif inp.quota_increase_yoy_pct <= 30:
        score += 7.0
    return max(0.0, min(100.0, round(score, 1)))


def _peer_equity_score(inp: QuotaFairnessInput) -> float:
    score = 0.0
    # Variance from peers (0-50): closer to peers = more fair
    abs_var = abs(inp.peer_quota_variance_pct)
    if abs_var <= 5:
        score += 50.0
    elif abs_var <= 10:
        score += 38.0
    elif abs_var <= 20:
        score += 22.0
    elif abs_var <= 30:
        score += 10.0
    # vs team average (0-30)
    if inp.team_avg_quota_usd > 0:
        team_var_pct = abs((inp.annual_quota_usd - inp.team_avg_quota_usd) / inp.team_avg_quota_usd) * 100
    else:
        team_var_pct = 0.0
    if team_var_pct <= 10:
        score += 30.0
    elif team_var_pct <= 20:
        score += 20.0
    elif team_var_pct <= 35:
        score += 10.0
    # Manager override reasonableness (0-20)
    abs_override = abs(inp.manager_override_pct)
    if abs_override <= 5:
        score += 20.0
    elif abs_override <= 10:
        score += 14.0
    elif abs_override <= 20:
        score += 7.0
    return max(0.0, min(100.0, round(score, 1)))


def _attainment_sustainability_score(inp: QuotaFairnessInput) -> float:
    score = 0.0
    # Team avg attainment (0-35): if team avg < 80%, quotas likely too high
    if inp.team_avg_attainment_pct >= 85:
        score += 35.0
    elif inp.team_avg_attainment_pct >= 75:
        score += 25.0
    elif inp.team_avg_attainment_pct >= 65:
        score += 15.0
    elif inp.team_avg_attainment_pct >= 50:
        score += 7.0
    # Previous attainment sustainability (0-30)
    if inp.previous_year_attainment_pct >= 80:
        score += 30.0
    elif inp.previous_year_attainment_pct >= 65:
        score += 22.0
    elif inp.previous_year_attainment_pct >= 50:
        score += 12.0
    # Account count vs quota (0-20): enough accounts to close quota
    deals_needed = inp.annual_quota_usd / max(1, inp.avg_deal_size_usd)
    if inp.account_count > deals_needed * 5:
        score += 20.0
    elif inp.account_count > deals_needed * 3:
        score += 14.0
    elif inp.account_count > deals_needed:
        score += 7.0
    # Territory not disrupted last year (0-15)
    if not inp.territory_adjusted_last_year:
        score += 15.0
    else:
        score += 5.0
    return max(0.0, min(100.0, round(score, 1)))


def _composite(market: float, experience: float, peer: float, attainment: float) -> float:
    raw = market * 0.30 + experience * 0.25 + peer * 0.25 + attainment * 0.20
    return round(raw, 1)


def _fairness_rating(composite: float) -> FairnessRating:
    if composite >= 75:
        return FairnessRating.VERY_FAIR
    if composite >= 55:
        return FairnessRating.FAIR
    if composite >= 35:
        return FairnessRating.QUESTIONABLE
    return FairnessRating.UNFAIR


def _fairness_risk(composite: float) -> FairnessRisk:
    if composite < 25:
        return FairnessRisk.CRITICAL
    if composite < 40:
        return FairnessRisk.HIGH
    if composite < 60:
        return FairnessRisk.MODERATE
    return FairnessRisk.LOW


def _bias_direction(inp: QuotaFairnessInput, composite: float) -> BiasDirection:
    if inp.peer_quota_variance_pct > 15 and composite < 55:
        return BiasDirection.OVER_QUOTED
    if inp.peer_quota_variance_pct < -15 and composite < 55:
        return BiasDirection.UNDER_QUOTED
    if inp.previous_year_attainment_pct < 60 and inp.quota_increase_yoy_pct > 10:
        return BiasDirection.OVER_QUOTED
    if inp.previous_year_attainment_pct > 120:
        return BiasDirection.UNDER_QUOTED
    return BiasDirection.BALANCED


def _quota_action(risk: FairnessRisk, bias: BiasDirection) -> QuotaAction:
    if risk in (FairnessRisk.CRITICAL, FairnessRisk.HIGH):
        if bias == BiasDirection.OVER_QUOTED:
            return QuotaAction.REDUCE_QUOTA
        if bias == BiasDirection.UNDER_QUOTED:
            return QuotaAction.INCREASE_QUOTA
        return QuotaAction.RECALIBRATE_TERRITORY
    if risk == FairnessRisk.MODERATE:
        return QuotaAction.RECALIBRATE_TERRITORY
    return QuotaAction.MAINTAIN


def _estimated_fair_quota(inp: QuotaFairnessInput) -> float:
    if inp.territory_market_potential_usd <= 0:
        return inp.annual_quota_usd
    base = inp.territory_market_potential_usd * 0.30  # target 30% of SAM
    # Adjust for experience
    if inp.years_experience >= 5:
        base *= 1.0
    elif inp.years_experience >= 3:
        base *= 0.85
    else:
        base *= 0.70
    # Adjust for industry growth
    growth_factor = 1.0 + (inp.industry_growth_rate_pct / 100.0)
    base *= min(1.3, max(0.8, growth_factor))
    # Competitive adjustment
    if inp.competitive_intensity_score >= 70:
        base *= 0.85
    return round(base, 2)


def _fairness_signal(inp: QuotaFairnessInput, market: float, experience: float,
                     peer: float, attainment: float) -> str:
    if inp.peer_quota_variance_pct > 25:
        return f"quota is {inp.peer_quota_variance_pct:.0f}% above peers in similar territories — review required"
    if inp.peer_quota_variance_pct < -25:
        return f"quota is {abs(inp.peer_quota_variance_pct):.0f}% below peers — potential under-assignment"
    if inp.quota_increase_yoy_pct > 25 and inp.previous_year_attainment_pct < 70:
        return f"quota increased {inp.quota_increase_yoy_pct:.0f}% YoY while prior attainment was {inp.previous_year_attainment_pct:.0f}%"
    if inp.team_avg_attainment_pct < 60:
        return f"team average attainment {inp.team_avg_attainment_pct:.0f}% — systemic over-quota across team"
    scores = {
        "market alignment": market,
        "experience alignment": experience,
        "peer equity": peer,
        "attainment sustainability": attainment,
    }
    weakest = min(scores, key=lambda k: scores[k])
    return f"primary fairness gap: {weakest}"


class QuotaFairnessEngine:
    def __init__(self) -> None:
        self._results: dict[str, QuotaFairnessResult] = {}

    def assess(self, inp: QuotaFairnessInput) -> QuotaFairnessResult:
        market = _market_alignment_score(inp)
        experience = _experience_alignment_score(inp)
        peer = _peer_equity_score(inp)
        attainment = _attainment_sustainability_score(inp)
        composite = _composite(market, experience, peer, attainment)

        rating = _fairness_rating(composite)
        risk = _fairness_risk(composite)
        bias = _bias_direction(inp, composite)
        action = _quota_action(risk, bias)
        is_over = bias == BiasDirection.OVER_QUOTED and composite < 50
        is_under = bias == BiasDirection.UNDER_QUOTED and composite < 50
        fair_quota = _estimated_fair_quota(inp)
        signal = _fairness_signal(inp, market, experience, peer, attainment)

        result = QuotaFairnessResult(
            rep_id=inp.rep_id,
            rep_name=inp.rep_name,
            fairness_rating=rating,
            fairness_risk=risk,
            bias_direction=bias,
            quota_action=action,
            market_alignment_score=market,
            experience_alignment_score=experience,
            peer_equity_score=peer,
            attainment_sustainability_score=attainment,
            fairness_composite=composite,
            is_over_quoted=is_over,
            is_under_quoted=is_under,
            estimated_fair_quota_usd=fair_quota,
            fairness_signal=signal,
        )
        self._results[inp.rep_id] = result
        return result

    def assess_batch(self, inputs: List[QuotaFairnessInput]) -> List[QuotaFairnessResult]:
        results = [self.assess(inp) for inp in inputs]
        results.sort(key=lambda r: r.fairness_composite, reverse=True)
        return results

    def get(self, rep_id: str) -> QuotaFairnessResult | None:
        return self._results.get(rep_id)

    def all_reps(self) -> List[QuotaFairnessResult]:
        return sorted(self._results.values(), key=lambda r: r.fairness_composite, reverse=True)

    def over_quoted_reps(self) -> List[QuotaFairnessResult]:
        return [r for r in self._results.values() if r.is_over_quoted]

    def under_quoted_reps(self) -> List[QuotaFairnessResult]:
        return [r for r in self._results.values() if r.is_under_quoted]

    def by_rating(self, rating: FairnessRating) -> List[QuotaFairnessResult]:
        return [r for r in self._results.values() if r.fairness_rating == rating]

    def by_risk(self, risk: FairnessRisk) -> List[QuotaFairnessResult]:
        return [r for r in self._results.values() if r.fairness_risk == risk]

    def avg_fairness_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.fairness_composite for r in self._results.values()) / len(self._results), 1)

    def total_quota_adjustment_opportunity_usd(self) -> float:
        return round(sum(
            abs(r.estimated_fair_quota_usd - self._results[r.rep_id].fairness_composite)
            for r in self._results.values()
        ), 2)

    def reset(self) -> None:
        self._results.clear()

    def summary(self) -> dict:
        results = list(self._results.values())
        n = len(results)
        fairness_counts: dict[str, int] = {}
        risk_counts: dict[str, int] = {}
        bias_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        for r in results:
            fairness_counts[r.fairness_rating.value] = fairness_counts.get(r.fairness_rating.value, 0) + 1
            risk_counts[r.fairness_risk.value] = risk_counts.get(r.fairness_risk.value, 0) + 1
            bias_counts[r.bias_direction.value] = bias_counts.get(r.bias_direction.value, 0) + 1
            action_counts[r.quota_action.value] = action_counts.get(r.quota_action.value, 0) + 1
        return {
            "total": n,
            "fairness_counts": fairness_counts,
            "risk_counts": risk_counts,
            "bias_counts": bias_counts,
            "action_counts": action_counts,
            "avg_fairness_composite": self.avg_fairness_composite(),
            "over_quoted_count": len(self.over_quoted_reps()),
            "under_quoted_count": len(self.under_quoted_reps()),
            "avg_market_alignment_score": round(sum(r.market_alignment_score for r in results) / n, 1) if n else 0.0,
            "avg_experience_alignment_score": round(sum(r.experience_alignment_score for r in results) / n, 1) if n else 0.0,
            "avg_peer_equity_score": round(sum(r.peer_equity_score for r in results) / n, 1) if n else 0.0,
            "avg_attainment_sustainability_score": round(sum(r.attainment_sustainability_score for r in results) / n, 1) if n else 0.0,
            "total_quota_adjustment_opportunity_usd": self.total_quota_adjustment_opportunity_usd(),
        }
