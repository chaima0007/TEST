from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List


class WinProbabilityTier(str, Enum):
    VERY_LIKELY = "very_likely"
    LIKELY = "likely"
    TOSS_UP = "toss_up"
    UNLIKELY = "unlikely"
    VERY_UNLIKELY = "very_unlikely"


class WinRisk(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class PrimaryWinFactor(str, Enum):
    CHAMPION = "champion"
    PRICE = "price"
    FEATURES = "features"
    RELATIONSHIP = "relationship"
    MOMENTUM = "momentum"


class WinAction(str, Enum):
    MAINTAIN_COURSE = "maintain_course"
    STRENGTHEN_CHAMPION = "strengthen_champion"
    PRICE_ADJUSTMENT = "price_adjustment"
    FEATURE_DEMO = "feature_demo"
    EXECUTIVE_ALIGNMENT = "executive_alignment"


@dataclass
class CompetitiveWinInput:
    deal_id: str
    rep_id: str
    deal_name: str
    competitor_id: str
    competitor_name: str
    deal_value_usd: float
    deal_stage_num: int
    champion_strength_score: float
    economic_buyer_engaged: int
    technical_fit_score: float
    competitive_win_rate_vs_competitor_pct: float
    price_competitiveness_score: float
    feature_advantage_score: float
    relationship_strength_score: float
    incumbent_competitor: int
    days_until_close: int
    executive_sponsorship: int
    proof_of_concept_won: int
    competitor_activity_level: float
    deal_momentum_score: float
    reference_customer_provided: int
    multi_year_deal: int


@dataclass
class CompetitiveWinResult:
    deal_id: str
    deal_name: str
    win_probability_tier: WinProbabilityTier
    win_risk: WinRisk
    primary_win_factor: PrimaryWinFactor
    recommended_action: WinAction
    champion_score: float
    competitive_position_score: float
    relationship_momentum_score: float
    deal_strength_score: float
    win_probability_pct: float
    is_at_risk: bool
    requires_executive_intervention: bool
    estimated_win_value_usd: float
    win_signal: str

    def to_dict(self) -> dict:
        return {
            "deal_id": self.deal_id,
            "deal_name": self.deal_name,
            "win_probability_tier": self.win_probability_tier.value,
            "win_risk": self.win_risk.value,
            "primary_win_factor": self.primary_win_factor.value,
            "recommended_action": self.recommended_action.value,
            "champion_score": self.champion_score,
            "competitive_position_score": self.competitive_position_score,
            "relationship_momentum_score": self.relationship_momentum_score,
            "deal_strength_score": self.deal_strength_score,
            "win_probability_pct": self.win_probability_pct,
            "is_at_risk": self.is_at_risk,
            "requires_executive_intervention": self.requires_executive_intervention,
            "estimated_win_value_usd": self.estimated_win_value_usd,
            "win_signal": self.win_signal,
        }


def _champion_score(inp: CompetitiveWinInput) -> float:
    score = 0.0
    # Champion strength (0-40)
    score += inp.champion_strength_score * 0.40
    # Economic buyer engaged (0-25)
    if inp.economic_buyer_engaged:
        score += 25.0
    # Executive sponsorship (0-20)
    if inp.executive_sponsorship:
        score += 20.0
    # Reference customer (0-15)
    if inp.reference_customer_provided:
        score += 15.0
    return max(0.0, min(100.0, round(score, 1)))


def _competitive_position_score(inp: CompetitiveWinInput) -> float:
    score = 0.0
    # Feature advantage (0-30)
    score += inp.feature_advantage_score * 0.30
    # Price competitiveness (0-25)
    score += inp.price_competitiveness_score * 0.25
    # Technical fit (0-25)
    score += inp.technical_fit_score * 0.25
    # Historical win rate vs this competitor (0-20)
    score += (inp.competitive_win_rate_vs_competitor_pct / 100.0) * 20.0
    # Incumbent penalty: if competitor is incumbent, harder to win
    if inp.incumbent_competitor:
        score *= 0.80
    return max(0.0, min(100.0, round(score, 1)))


def _relationship_momentum_score(inp: CompetitiveWinInput) -> float:
    score = 0.0
    # Relationship strength (0-30)
    score += inp.relationship_strength_score * 0.30
    # Deal momentum (0-30)
    score += inp.deal_momentum_score * 0.30
    # POC won (0-20)
    if inp.proof_of_concept_won:
        score += 20.0
    # Deal stage progression (0-15): further in stage = more momentum
    stage_bonus = min(15.0, inp.deal_stage_num * 3.0)
    score += stage_bonus
    # Competitor activity: high competitor activity hurts momentum
    comp_penalty = (inp.competitor_activity_level / 100.0) * 5.0
    score -= comp_penalty
    # Multi-year signals higher commitment
    if inp.multi_year_deal:
        score += 5.0
    return max(0.0, min(100.0, round(score, 1)))


def _deal_strength_score(inp: CompetitiveWinInput) -> float:
    # Urgency and timing factors
    score = 0.0
    # Deal value: larger deals harder to win without strong position
    if inp.deal_value_usd >= 1_000_000:
        score += 15.0 if inp.executive_sponsorship else 5.0
    elif inp.deal_value_usd >= 500_000:
        score += 20.0
    elif inp.deal_value_usd >= 100_000:
        score += 25.0
    else:
        score += 30.0
    # Time pressure (0-25): reasonable close timeline
    if 15 <= inp.days_until_close <= 60:
        score += 25.0
    elif inp.days_until_close < 15:
        score += 10.0
    elif inp.days_until_close <= 90:
        score += 18.0
    else:
        score += 8.0
    # Multi-year deal commitment (0-20)
    if inp.multi_year_deal:
        score += 20.0
    else:
        score += 10.0
    # Stage appropriate activity (0-25)
    score += min(25.0, inp.deal_stage_num * 5.0)
    return max(0.0, min(100.0, round(score, 1)))


def _win_probability_pct(champion: float, competitive: float, momentum: float, strength: float) -> float:
    raw = champion * 0.35 + competitive * 0.30 + momentum * 0.25 + strength * 0.10
    return round(raw, 1)


def _win_tier(pct: float) -> WinProbabilityTier:
    if pct >= 75:
        return WinProbabilityTier.VERY_LIKELY
    if pct >= 58:
        return WinProbabilityTier.LIKELY
    if pct >= 42:
        return WinProbabilityTier.TOSS_UP
    if pct >= 25:
        return WinProbabilityTier.UNLIKELY
    return WinProbabilityTier.VERY_UNLIKELY


def _win_risk(pct: float) -> WinRisk:
    if pct >= 65:
        return WinRisk.LOW
    if pct >= 45:
        return WinRisk.MODERATE
    if pct >= 25:
        return WinRisk.HIGH
    return WinRisk.CRITICAL


def _primary_factor(champion: float, competitive: float, momentum: float, strength: float) -> PrimaryWinFactor:
    scores = {
        PrimaryWinFactor.CHAMPION: champion,
        PrimaryWinFactor.FEATURES: competitive,
        PrimaryWinFactor.MOMENTUM: momentum,
        PrimaryWinFactor.RELATIONSHIP: momentum,
    }
    # Simplify: map to 4 factors
    mapped = {
        PrimaryWinFactor.CHAMPION: champion,
        PrimaryWinFactor.FEATURES: competitive,
        PrimaryWinFactor.MOMENTUM: momentum,
        PrimaryWinFactor.PRICE: strength,
    }
    return max(mapped, key=lambda k: mapped[k])


def _recommended_action(pct: float, inp: CompetitiveWinInput) -> WinAction:
    if pct >= 65:
        return WinAction.MAINTAIN_COURSE
    if not inp.executive_sponsorship and inp.deal_value_usd >= 300_000:
        return WinAction.EXECUTIVE_ALIGNMENT
    if inp.champion_strength_score < 50:
        return WinAction.STRENGTHEN_CHAMPION
    if inp.price_competitiveness_score < 40:
        return WinAction.PRICE_ADJUSTMENT
    if inp.feature_advantage_score < 40 and not inp.proof_of_concept_won:
        return WinAction.FEATURE_DEMO
    return WinAction.STRENGTHEN_CHAMPION


def _win_signal(inp: CompetitiveWinInput, pct: float, tier: WinProbabilityTier) -> str:
    if inp.incumbent_competitor and pct < 50:
        return f"displacing incumbent {inp.competitor_name} — win rate historically {inp.competitive_win_rate_vs_competitor_pct:.0f}%"
    if inp.proof_of_concept_won and pct >= 60:
        return f"POC won vs {inp.competitor_name} — champion strong, path to close clear"
    if inp.economic_buyer_engaged and inp.executive_sponsorship:
        return f"executive + economic buyer aligned — {inp.competitor_name} at disadvantage"
    if inp.competitor_activity_level >= 70:
        return f"{inp.competitor_name} highly active in deal — competitive pressure intensifying"
    if pct >= 75:
        return f"strong position vs {inp.competitor_name} — {pct:.0f}% win probability, maintain course"
    if pct < 30:
        return f"at risk of losing to {inp.competitor_name} — immediate intervention required"
    return f"competitive with {inp.competitor_name} at {pct:.0f}% win probability"


class CompetitiveWinProbabilityEngine:
    def __init__(self) -> None:
        self._results: dict[str, CompetitiveWinResult] = {}
        self._deal_values: dict[str, float] = {}

    def assess(self, inp: CompetitiveWinInput) -> CompetitiveWinResult:
        champion = _champion_score(inp)
        competitive = _competitive_position_score(inp)
        momentum = _relationship_momentum_score(inp)
        strength = _deal_strength_score(inp)
        win_pct = _win_probability_pct(champion, competitive, momentum, strength)

        tier = _win_tier(win_pct)
        risk = _win_risk(win_pct)
        factor = _primary_factor(champion, competitive, momentum, strength)
        action = _recommended_action(win_pct, inp)
        is_at_risk = win_pct < 45 or inp.competitor_activity_level >= 80
        requires_exec = win_pct < 50 and inp.deal_value_usd >= 300_000 and not inp.executive_sponsorship
        win_value = round(win_pct / 100.0 * inp.deal_value_usd, 2)
        signal = _win_signal(inp, win_pct, tier)

        result = CompetitiveWinResult(
            deal_id=inp.deal_id,
            deal_name=inp.deal_name,
            win_probability_tier=tier,
            win_risk=risk,
            primary_win_factor=factor,
            recommended_action=action,
            champion_score=champion,
            competitive_position_score=competitive,
            relationship_momentum_score=momentum,
            deal_strength_score=strength,
            win_probability_pct=win_pct,
            is_at_risk=is_at_risk,
            requires_executive_intervention=requires_exec,
            estimated_win_value_usd=win_value,
            win_signal=signal,
        )
        self._results[inp.deal_id] = result
        self._deal_values[inp.deal_id] = inp.deal_value_usd
        return result

    def assess_batch(self, inputs: List[CompetitiveWinInput]) -> List[CompetitiveWinResult]:
        results = [self.assess(inp) for inp in inputs]
        results.sort(key=lambda r: r.win_probability_pct, reverse=True)
        return results

    def get(self, deal_id: str) -> CompetitiveWinResult | None:
        return self._results.get(deal_id)

    def all_deals(self) -> List[CompetitiveWinResult]:
        return sorted(self._results.values(), key=lambda r: r.win_probability_pct, reverse=True)

    def at_risk_deals(self) -> List[CompetitiveWinResult]:
        return [r for r in self._results.values() if r.is_at_risk]

    def by_tier(self, tier: WinProbabilityTier) -> List[CompetitiveWinResult]:
        return [r for r in self._results.values() if r.win_probability_tier == tier]

    def by_risk(self, risk: WinRisk) -> List[CompetitiveWinResult]:
        return [r for r in self._results.values() if r.win_risk == risk]

    def total_weighted_pipeline_usd(self) -> float:
        return round(sum(r.estimated_win_value_usd for r in self._results.values()), 2)

    def avg_win_probability_pct(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.win_probability_pct for r in self._results.values()) / len(self._results), 1)

    def reset(self) -> None:
        self._results.clear()
        self._deal_values.clear()

    def summary(self) -> dict:
        results = list(self._results.values())
        n = len(results)
        tier_counts: dict[str, int] = {}
        risk_counts: dict[str, int] = {}
        factor_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        for r in results:
            tier_counts[r.win_probability_tier.value] = tier_counts.get(r.win_probability_tier.value, 0) + 1
            risk_counts[r.win_risk.value] = risk_counts.get(r.win_risk.value, 0) + 1
            factor_counts[r.primary_win_factor.value] = factor_counts.get(r.primary_win_factor.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
        return {
            "total": n,
            "tier_counts": tier_counts,
            "risk_counts": risk_counts,
            "factor_counts": factor_counts,
            "action_counts": action_counts,
            "avg_win_probability_pct": self.avg_win_probability_pct(),
            "at_risk_count": len(self.at_risk_deals()),
            "executive_intervention_count": sum(1 for r in results if r.requires_executive_intervention),
            "avg_champion_score": round(sum(r.champion_score for r in results) / n, 1) if n else 0.0,
            "avg_competitive_position_score": round(sum(r.competitive_position_score for r in results) / n, 1) if n else 0.0,
            "avg_relationship_momentum_score": round(sum(r.relationship_momentum_score for r in results) / n, 1) if n else 0.0,
            "avg_deal_strength_score": round(sum(r.deal_strength_score for r in results) / n, 1) if n else 0.0,
            "total_weighted_pipeline_usd": self.total_weighted_pipeline_usd(),
        }
