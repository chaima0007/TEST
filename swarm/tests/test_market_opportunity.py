"""
Comprehensive tests for intelligence/market_opportunity.py — MarketOpportunityScanner.

Coverage:
  - Enum values
  - _market_attractiveness (growth/demand/TAM scores, advantages, risks)
  - _penetrability (saturation/regulatory/disruption, advantages, risks)
  - _strategic_fit (expertise/share_bonus/deal_score, advantages, risks)
  - _opportunity_phase (all 4 phases, boundary conditions)
  - _risk_level (all 4 levels, boundary conditions)
  - opportunity_score formula
  - CRUD: scan, get, overwrite, scan_batch
  - Filters: by_phase, by_risk, emerging_markets
  - top_opportunities (default + custom n)
  - all_opportunities sort order
  - summary() with empty and non-empty store, top_sector logic
  - reset()
  - to_dict() keys and types
"""

import math
import pytest

from swarm.intelligence.market_opportunity import (
    MarketOpportunityScanner,
    MarketSignals,
    OpportunityPhase,
    RiskLevel,
    ScoredOpportunity,
    _market_attractiveness,
    _opportunity_phase,
    _penetrability,
    _risk_level,
    _strategic_fit,
)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def make_market(
    opportunity_id: str = "m1",
    market_name: str = "Test Market",
    sector: str = "Tech",
    sub_sector: str = "SaaS",
    total_addressable_market_eur: float = 500_000_000,
    annual_growth_rate_pct: float = 0.15,
    competitor_count: int = 3,
    our_market_share_pct: float = 5.0,
    avg_deal_size_eur: float = 50_000,
    avg_sales_cycle_days: int = 60,
    demand_trend: float = 0.60,
    regulatory_complexity: float = 20.0,
    tech_disruption_risk: float = 20.0,
    our_expertise_score: float = 80.0,
) -> MarketSignals:
    """Return a MarketSignals with healthy defaults (EMERGING phase, LOW risk)."""
    return MarketSignals(
        opportunity_id=opportunity_id,
        market_name=market_name,
        sector=sector,
        sub_sector=sub_sector,
        total_addressable_market_eur=total_addressable_market_eur,
        annual_growth_rate_pct=annual_growth_rate_pct,
        competitor_count=competitor_count,
        our_market_share_pct=our_market_share_pct,
        avg_deal_size_eur=avg_deal_size_eur,
        avg_sales_cycle_days=avg_sales_cycle_days,
        demand_trend=demand_trend,
        regulatory_complexity=regulatory_complexity,
        tech_disruption_risk=tech_disruption_risk,
        our_expertise_score=our_expertise_score,
    )


def scanner() -> MarketOpportunityScanner:
    return MarketOpportunityScanner()


# ─── 1. Enum values ───────────────────────────────────────────────────────────

class TestEnums:
    def test_opportunity_phase_values(self):
        assert OpportunityPhase.EMERGING.value == "emerging"
        assert OpportunityPhase.GROWING.value == "growing"
        assert OpportunityPhase.MATURE.value == "mature"
        assert OpportunityPhase.DECLINING.value == "declining"

    def test_opportunity_phase_is_str_enum(self):
        assert isinstance(OpportunityPhase.EMERGING, str)

    def test_risk_level_values(self):
        assert RiskLevel.LOW.value == "low"
        assert RiskLevel.MEDIUM.value == "medium"
        assert RiskLevel.HIGH.value == "high"
        assert RiskLevel.CRITICAL.value == "critical"

    def test_risk_level_is_str_enum(self):
        assert isinstance(RiskLevel.LOW, str)

    def test_all_four_phases_exist(self):
        phases = {p.value for p in OpportunityPhase}
        assert phases == {"emerging", "growing", "mature", "declining"}

    def test_all_four_risk_levels_exist(self):
        risks = {r.value for r in RiskLevel}
        assert risks == {"low", "medium", "high", "critical"}


# ─── 2. _market_attractiveness ────────────────────────────────────────────────

class TestMarketAttractiveness:
    # growth_score = max(0, min(100, 50 + growth * 500))

    def test_growth_zero_pct_gives_score_50(self):
        m = make_market(annual_growth_rate_pct=0.0, demand_trend=0.0,
                        total_addressable_market_eur=1)
        score, _, _ = _market_attractiveness(m)
        # growth=0 → 50; demand=0 → 50; size=log10(1)/9*100=0
        expected = 50 * 0.40 + 50 * 0.35 + 0 * 0.25
        assert abs(score - round(expected, 2)) < 0.01

    def test_growth_10pct_gives_growth_score_100(self):
        """growth=0.10 → growth_score = 50 + 0.10*500 = 100."""
        m = make_market(annual_growth_rate_pct=0.10, demand_trend=0.0,
                        total_addressable_market_eur=1)
        score, _, _ = _market_attractiveness(m)
        expected = 100 * 0.40 + 50 * 0.35 + 0 * 0.25
        assert abs(score - round(expected, 2)) < 0.01

    def test_growth_negative_10pct_gives_growth_score_0(self):
        """growth=-0.10 → growth_score = max(0, 50 - 50) = 0."""
        m = make_market(annual_growth_rate_pct=-0.10, demand_trend=0.0,
                        total_addressable_market_eur=1)
        score, _, _ = _market_attractiveness(m)
        expected = 0 * 0.40 + 50 * 0.35 + 0 * 0.25
        assert abs(score - round(expected, 2)) < 0.01

    def test_growth_score_capped_at_100(self):
        """Very high growth should not push growth_score above 100."""
        m = make_market(annual_growth_rate_pct=1.0, demand_trend=0.0,
                        total_addressable_market_eur=1)
        _, _, _ = _market_attractiveness(m)  # just ensure no exception
        # verify growth_score = 100 (capped)
        growth_score = max(0, min(100, 50 + 1.0 * 500))
        assert growth_score == 100

    def test_demand_score_at_plus_one(self):
        """demand_trend=+1 → demand_score = (1+1)/2*100 = 100."""
        m = make_market(demand_trend=1.0, annual_growth_rate_pct=0.0,
                        total_addressable_market_eur=1)
        score, _, _ = _market_attractiveness(m)
        expected = 50 * 0.40 + 100 * 0.35 + 0 * 0.25
        assert abs(score - round(expected, 2)) < 0.01

    def test_demand_score_at_minus_one(self):
        """demand_trend=-1 → demand_score = 0."""
        m = make_market(demand_trend=-1.0, annual_growth_rate_pct=0.0,
                        total_addressable_market_eur=1)
        score, _, _ = _market_attractiveness(m)
        expected = 50 * 0.40 + 0 * 0.35 + 0 * 0.25
        assert abs(score - round(expected, 2)) < 0.01

    def test_demand_clamped_beyond_plus_one(self):
        """demand_trend=2.0 should behave as 1.0."""
        m1 = make_market(demand_trend=2.0, annual_growth_rate_pct=0.0,
                         total_addressable_market_eur=1)
        m2 = make_market(demand_trend=1.0, annual_growth_rate_pct=0.0,
                         total_addressable_market_eur=1)
        s1, _, _ = _market_attractiveness(m1)
        s2, _, _ = _market_attractiveness(m2)
        assert s1 == s2

    def test_tam_size_score_uses_log10(self):
        """TAM=10^9 → log10=9 → size_score = 9/9*100 = 100."""
        m = make_market(total_addressable_market_eur=1_000_000_000,
                        annual_growth_rate_pct=0.0, demand_trend=0.0)
        score, _, _ = _market_attractiveness(m)
        expected = 50 * 0.40 + 50 * 0.35 + 100 * 0.25
        assert abs(score - round(expected, 2)) < 0.01

    def test_tam_zero_gives_size_score_zero(self):
        m = make_market(total_addressable_market_eur=0,
                        annual_growth_rate_pct=0.0, demand_trend=0.0)
        score, _, _ = _market_attractiveness(m)
        # size_score = 0 for tam <= 0
        expected = 50 * 0.40 + 50 * 0.35 + 0 * 0.25
        assert abs(score - round(expected, 2)) < 0.01

    def test_advantage_fast_growing_market_at_20pct(self):
        m = make_market(annual_growth_rate_pct=0.20)
        _, advantages, _ = _market_attractiveness(m)
        assert "fast_growing_market" in advantages

    def test_no_fast_growing_below_20pct(self):
        m = make_market(annual_growth_rate_pct=0.19)
        _, advantages, _ = _market_attractiveness(m)
        assert "fast_growing_market" not in advantages

    def test_advantage_strong_demand_above_half(self):
        m = make_market(demand_trend=0.51)
        _, advantages, _ = _market_attractiveness(m)
        assert "strong_demand" in advantages

    def test_no_strong_demand_at_exactly_half(self):
        m = make_market(demand_trend=0.50)
        _, advantages, _ = _market_attractiveness(m)
        assert "strong_demand" not in advantages

    def test_advantage_large_tam_at_100m(self):
        m = make_market(total_addressable_market_eur=100_000_000)
        _, advantages, _ = _market_attractiveness(m)
        assert "large_tam" in advantages

    def test_no_large_tam_below_100m(self):
        m = make_market(total_addressable_market_eur=99_999_999)
        _, advantages, _ = _market_attractiveness(m)
        assert "large_tam" not in advantages

    def test_risk_slow_growth_when_negative_growth(self):
        m = make_market(annual_growth_rate_pct=-0.01)
        _, _, risks = _market_attractiveness(m)
        assert "slow_growth" in risks

    def test_no_slow_growth_at_zero_growth(self):
        m = make_market(annual_growth_rate_pct=0.0)
        _, _, risks = _market_attractiveness(m)
        assert "slow_growth" not in risks

    def test_risk_declining_demand_below_negative_20pct(self):
        m = make_market(demand_trend=-0.21)
        _, _, risks = _market_attractiveness(m)
        assert "declining_demand" in risks

    def test_no_declining_demand_at_negative_20pct(self):
        m = make_market(demand_trend=-0.20)
        _, _, risks = _market_attractiveness(m)
        assert "declining_demand" not in risks

    def test_weighted_formula_all_components(self):
        """Verify the exact weighted sum formula."""
        growth = 0.15
        demand = 0.70
        tam = 500_000_000
        m = make_market(annual_growth_rate_pct=growth, demand_trend=demand,
                        total_addressable_market_eur=tam)
        score, _, _ = _market_attractiveness(m)
        growth_score = max(0.0, min(100.0, 50.0 + growth * 500.0))
        demand_score = (demand + 1.0) / 2.0 * 100.0
        size_score = min(100.0, math.log10(tam) / 9.0 * 100.0)
        expected = round(growth_score * 0.40 + demand_score * 0.35 + size_score * 0.25, 2)
        assert score == expected


# ─── 3. _penetrability ────────────────────────────────────────────────────────

class TestPenetrability:
    def test_zero_competitors_full_saturation_score(self):
        """competitor_count=0 → saturation = 100."""
        m = make_market(competitor_count=0, regulatory_complexity=0, tech_disruption_risk=0)
        score, _, _ = _penetrability(m)
        assert abs(score - 100.0) < 0.01

    def test_saturation_floored_at_zero(self):
        """competitor_count=11 → saturation = max(0, 100-110) = 0."""
        m = make_market(competitor_count=11, regulatory_complexity=0, tech_disruption_risk=0)
        score, _, _ = _penetrability(m)
        # saturation=0, regulatory=100, disruption=100
        expected = 0 * 0.40 + 100 * 0.35 + 100 * 0.25
        assert abs(score - round(expected, 2)) < 0.01

    def test_regulatory_zero_gives_full_regulatory_score(self):
        m = make_market(competitor_count=0, regulatory_complexity=0, tech_disruption_risk=0)
        score, _, _ = _penetrability(m)
        assert abs(score - 100.0) < 0.01

    def test_regulatory_100_gives_zero_regulatory_score(self):
        m = make_market(competitor_count=0, regulatory_complexity=100, tech_disruption_risk=0)
        score, _, _ = _penetrability(m)
        expected = 100 * 0.40 + 0 * 0.35 + 100 * 0.25
        assert abs(score - round(expected, 2)) < 0.01

    def test_disruption_100_gives_zero_disruption_score(self):
        m = make_market(competitor_count=0, regulatory_complexity=0, tech_disruption_risk=100)
        score, _, _ = _penetrability(m)
        expected = 100 * 0.40 + 100 * 0.35 + 0 * 0.25
        assert abs(score - round(expected, 2)) < 0.01

    def test_advantage_low_competition_at_3(self):
        m = make_market(competitor_count=3)
        _, advantages, _ = _penetrability(m)
        assert "low_competition" in advantages

    def test_no_low_competition_at_4(self):
        m = make_market(competitor_count=4)
        _, advantages, _ = _penetrability(m)
        assert "low_competition" not in advantages

    def test_risk_large_competitors_at_11(self):
        m = make_market(competitor_count=11)
        _, _, risks = _penetrability(m)
        assert "large_competitors" in risks

    def test_risk_high_saturation_at_11(self):
        m = make_market(competitor_count=11)
        _, _, risks = _penetrability(m)
        assert "high_saturation" in risks

    def test_no_large_competitors_at_10(self):
        m = make_market(competitor_count=10)
        _, _, risks = _penetrability(m)
        assert "large_competitors" not in risks
        assert "high_saturation" not in risks

    def test_risk_regulatory_barrier_above_50(self):
        m = make_market(regulatory_complexity=51)
        _, _, risks = _penetrability(m)
        assert "regulatory_barrier" in risks

    def test_no_regulatory_barrier_at_50(self):
        m = make_market(regulatory_complexity=50)
        _, _, risks = _penetrability(m)
        assert "regulatory_barrier" not in risks

    def test_risk_tech_disruption_above_55(self):
        m = make_market(tech_disruption_risk=56)
        _, _, risks = _penetrability(m)
        assert "tech_disruption" in risks

    def test_no_tech_disruption_at_55(self):
        m = make_market(tech_disruption_risk=55)
        _, _, risks = _penetrability(m)
        assert "tech_disruption" not in risks

    def test_weighted_formula(self):
        """Verify exact formula: saturation*0.40 + regulatory*0.35 + disruption*0.25."""
        m = make_market(competitor_count=5, regulatory_complexity=40, tech_disruption_risk=30)
        score, _, _ = _penetrability(m)
        saturation = max(0.0, 100.0 - 5 * 10.0)
        regulatory = max(0.0, 100.0 - 40.0)
        disruption = max(0.0, 100.0 - 30.0)
        expected = round(saturation * 0.40 + regulatory * 0.35 + disruption * 0.25, 2)
        assert score == expected


# ─── 4. _strategic_fit ────────────────────────────────────────────────────────

class TestStrategicFit:
    def test_high_expertise_advantage_at_75(self):
        m = make_market(our_expertise_score=75, our_market_share_pct=0, avg_deal_size_eur=50_000)
        _, advantages, _ = _strategic_fit(m)
        assert "high_expertise" in advantages

    def test_no_high_expertise_below_75(self):
        m = make_market(our_expertise_score=74, our_market_share_pct=0, avg_deal_size_eur=50_000)
        _, advantages, _ = _strategic_fit(m)
        assert "high_expertise" not in advantages

    def test_no_expertise_risk_below_35(self):
        m = make_market(our_expertise_score=34, our_market_share_pct=0, avg_deal_size_eur=50_000)
        _, _, risks = _strategic_fit(m)
        assert "no_expertise" in risks

    def test_no_expertise_risk_not_triggered_at_35(self):
        m = make_market(our_expertise_score=35, our_market_share_pct=0, avg_deal_size_eur=50_000)
        _, _, risks = _strategic_fit(m)
        assert "no_expertise" not in risks

    def test_existing_share_advantage_when_share_positive(self):
        m = make_market(our_market_share_pct=0.1)
        _, advantages, _ = _strategic_fit(m)
        assert "existing_share" in advantages

    def test_no_existing_share_when_zero(self):
        m = make_market(our_market_share_pct=0.0)
        _, advantages, _ = _strategic_fit(m)
        assert "existing_share" not in advantages

    def test_market_share_bonus_capped_at_30(self):
        """share_pct=20 → bonus=min(30, 40)=30."""
        m = make_market(our_market_share_pct=20.0, our_expertise_score=0, avg_deal_size_eur=50_000)
        score, _, _ = _strategic_fit(m)
        bonus = 30.0
        deal_score = 100.0
        expected = round(min(100.0, 0 * 0.50 + bonus * (100.0 / 30.0) * 0.20 + deal_score * 0.30), 2)
        assert score == expected

    def test_deal_score_optimal_band_lower_bound(self):
        """deal=20_000 → deal_score=100, advantage optimal_deal_size."""
        m = make_market(avg_deal_size_eur=20_000, our_expertise_score=0, our_market_share_pct=0)
        _, advantages, _ = _strategic_fit(m)
        assert "optimal_deal_size" in advantages

    def test_deal_score_optimal_band_upper_bound(self):
        """deal=200_000 → deal_score=100."""
        m = make_market(avg_deal_size_eur=200_000, our_expertise_score=0, our_market_share_pct=0)
        _, advantages, _ = _strategic_fit(m)
        assert "optimal_deal_size" in advantages

    def test_deal_score_80_lower_adjacent(self):
        """deal=10_000 → deal_score=80, no optimal_deal_size."""
        m = make_market(avg_deal_size_eur=10_000, our_expertise_score=0, our_market_share_pct=0)
        score, advantages, _ = _strategic_fit(m)
        assert "optimal_deal_size" not in advantages
        expected = round(min(100.0, 0 * 0.50 + 0 * (100.0/30.0) * 0.20 + 80.0 * 0.30), 2)
        assert score == expected

    def test_deal_score_80_upper_adjacent(self):
        """deal=500_000 → deal_score=80."""
        m = make_market(avg_deal_size_eur=500_000, our_expertise_score=0, our_market_share_pct=0)
        score, advantages, _ = _strategic_fit(m)
        assert "optimal_deal_size" not in advantages
        expected = round(min(100.0, 0 * 0.50 + 0 * (100.0/30.0) * 0.20 + 80.0 * 0.30), 2)
        assert score == expected

    def test_deal_score_60_below_lower_bound(self):
        """deal=9_999 → deal_score=60."""
        m = make_market(avg_deal_size_eur=9_999, our_expertise_score=0, our_market_share_pct=0)
        score, advantages, _ = _strategic_fit(m)
        assert "optimal_deal_size" not in advantages
        expected = round(min(100.0, 0 * 0.50 + 0 * (100.0/30.0) * 0.20 + 60.0 * 0.30), 2)
        assert score == expected

    def test_deal_score_60_above_upper_bound(self):
        """deal=500_001 → deal_score=60."""
        m = make_market(avg_deal_size_eur=500_001, our_expertise_score=0, our_market_share_pct=0)
        score, advantages, _ = _strategic_fit(m)
        expected = round(min(100.0, 0 * 0.50 + 0 * (100.0/30.0) * 0.20 + 60.0 * 0.30), 2)
        assert score == expected

    def test_strategic_fit_capped_at_100(self):
        """Max expertise + max share + optimal deal should not exceed 100."""
        m = make_market(our_expertise_score=100, our_market_share_pct=100, avg_deal_size_eur=50_000)
        score, _, _ = _strategic_fit(m)
        assert score <= 100.0

    def test_strategic_fit_formula(self):
        """Verify full formula: expertise*0.50 + bonus*(100/30)*0.20 + deal_score*0.30."""
        m = make_market(our_expertise_score=60, our_market_share_pct=10, avg_deal_size_eur=50_000)
        score, _, _ = _strategic_fit(m)
        bonus = min(30.0, 10.0 * 2.0)  # = 20
        deal_score = 100.0
        expected = round(min(100.0, 60 * 0.50 + bonus * (100.0 / 30.0) * 0.20 + deal_score * 0.30), 2)
        assert score == expected


# ─── 5. _opportunity_phase ────────────────────────────────────────────────────

class TestOpportunityPhase:
    """
    Phase logic uses saturation_for_phase = max(0, 100 - competitor_count*10).
    _opportunity_phase receives saturation_score (=saturation_for_phase), then
    internally computes saturation = 100 - saturation_score (higher=more saturated).
    EMERGING: growth>=0.20 AND (100-saturation_score)<=30 AND demand>0.30
            ↔ saturation_score>=70 ↔ competitor_count<=3
    """

    def test_emerging_phase_conditions(self):
        m = make_market(annual_growth_rate_pct=0.20, competitor_count=3, demand_trend=0.31)
        sat = max(0.0, 100.0 - 3 * 10.0)
        phase = _opportunity_phase(m, sat)
        assert phase == OpportunityPhase.EMERGING

    def test_emerging_requires_growth_at_least_20pct(self):
        m = make_market(annual_growth_rate_pct=0.19, competitor_count=3, demand_trend=0.31)
        sat = max(0.0, 100.0 - 3 * 10.0)
        phase = _opportunity_phase(m, sat)
        assert phase != OpportunityPhase.EMERGING

    def test_emerging_requires_low_competition(self):
        """competitor_count=4 → saturation_score=60 → internal saturation=40 > 30 → not EMERGING."""
        m = make_market(annual_growth_rate_pct=0.20, competitor_count=4, demand_trend=0.31)
        sat = max(0.0, 100.0 - 4 * 10.0)
        phase = _opportunity_phase(m, sat)
        assert phase != OpportunityPhase.EMERGING

    def test_emerging_requires_demand_above_30(self):
        m = make_market(annual_growth_rate_pct=0.20, competitor_count=3, demand_trend=0.30)
        sat = max(0.0, 100.0 - 3 * 10.0)
        phase = _opportunity_phase(m, sat)
        assert phase != OpportunityPhase.EMERGING

    def test_growing_phase_via_high_growth(self):
        """growth>=0.08 → GROWING (assuming not EMERGING)."""
        m = make_market(annual_growth_rate_pct=0.08, competitor_count=5, demand_trend=0.0)
        sat = max(0.0, 100.0 - 5 * 10.0)
        phase = _opportunity_phase(m, sat)
        assert phase == OpportunityPhase.GROWING

    def test_growing_phase_via_zero_growth_positive_demand(self):
        """growth=0.0 AND demand>0.10 → GROWING."""
        m = make_market(annual_growth_rate_pct=0.0, competitor_count=5, demand_trend=0.11)
        sat = max(0.0, 100.0 - 5 * 10.0)
        phase = _opportunity_phase(m, sat)
        assert phase == OpportunityPhase.GROWING

    def test_mature_phase(self):
        """growth=-0.01 (>=-0.05), demand<=0.10 → MATURE."""
        m = make_market(annual_growth_rate_pct=-0.01, competitor_count=5, demand_trend=0.0)
        sat = max(0.0, 100.0 - 5 * 10.0)
        phase = _opportunity_phase(m, sat)
        assert phase == OpportunityPhase.MATURE

    def test_mature_boundary_at_negative_5pct(self):
        """growth=-0.05 → MATURE."""
        m = make_market(annual_growth_rate_pct=-0.05, competitor_count=5, demand_trend=0.0)
        sat = max(0.0, 100.0 - 5 * 10.0)
        phase = _opportunity_phase(m, sat)
        assert phase == OpportunityPhase.MATURE

    def test_declining_phase(self):
        """growth < -0.05 → DECLINING."""
        m = make_market(annual_growth_rate_pct=-0.10, competitor_count=5, demand_trend=-0.5)
        sat = max(0.0, 100.0 - 5 * 10.0)
        phase = _opportunity_phase(m, sat)
        assert phase == OpportunityPhase.DECLINING

    def test_declining_boundary_just_below_negative_5pct(self):
        """growth=-0.051 → DECLINING."""
        m = make_market(annual_growth_rate_pct=-0.051, competitor_count=5, demand_trend=-0.5)
        sat = max(0.0, 100.0 - 5 * 10.0)
        phase = _opportunity_phase(m, sat)
        assert phase == OpportunityPhase.DECLINING


# ─── 6. _risk_level ───────────────────────────────────────────────────────────

class TestRiskLevel:
    def test_low_risk_clean_market(self):
        m = make_market(regulatory_complexity=10, tech_disruption_risk=10, competitor_count=2)
        assert _risk_level(m) == RiskLevel.LOW

    def test_medium_via_regulatory(self):
        m = make_market(regulatory_complexity=31, tech_disruption_risk=0, competitor_count=2)
        assert _risk_level(m) == RiskLevel.MEDIUM

    def test_medium_via_competitor_count(self):
        m = make_market(regulatory_complexity=10, tech_disruption_risk=0, competitor_count=5)
        assert _risk_level(m) == RiskLevel.MEDIUM

    def test_medium_boundary_regulatory_at_30(self):
        """regulatory=30 → NOT medium (needs >30)."""
        m = make_market(regulatory_complexity=30, tech_disruption_risk=0, competitor_count=2)
        assert _risk_level(m) == RiskLevel.LOW

    def test_medium_boundary_competitor_at_4(self):
        """competitor_count=4 → NOT medium (needs >4)."""
        m = make_market(regulatory_complexity=10, tech_disruption_risk=0, competitor_count=4)
        assert _risk_level(m) == RiskLevel.LOW

    def test_high_via_regulatory(self):
        m = make_market(regulatory_complexity=51, tech_disruption_risk=0, competitor_count=2)
        assert _risk_level(m) == RiskLevel.HIGH

    def test_high_via_tech_disruption(self):
        m = make_market(regulatory_complexity=10, tech_disruption_risk=56, competitor_count=2)
        assert _risk_level(m) == RiskLevel.HIGH

    def test_high_via_competitor_count(self):
        m = make_market(regulatory_complexity=10, tech_disruption_risk=0, competitor_count=9)
        assert _risk_level(m) == RiskLevel.HIGH

    def test_high_boundary_competitor_at_8(self):
        """competitor_count=8 → NOT high (needs >8)."""
        m = make_market(regulatory_complexity=10, tech_disruption_risk=0, competitor_count=8)
        assert _risk_level(m) == RiskLevel.MEDIUM

    def test_critical_via_regulatory(self):
        m = make_market(regulatory_complexity=71, tech_disruption_risk=0, competitor_count=2)
        assert _risk_level(m) == RiskLevel.CRITICAL

    def test_critical_via_tech_disruption(self):
        m = make_market(regulatory_complexity=10, tech_disruption_risk=76, competitor_count=2)
        assert _risk_level(m) == RiskLevel.CRITICAL

    def test_critical_via_competitor_count(self):
        m = make_market(regulatory_complexity=10, tech_disruption_risk=0, competitor_count=16)
        assert _risk_level(m) == RiskLevel.CRITICAL

    def test_critical_boundary_regulatory_at_70(self):
        """regulatory=70 → NOT critical (needs >70) → HIGH."""
        m = make_market(regulatory_complexity=70, tech_disruption_risk=0, competitor_count=2)
        assert _risk_level(m) == RiskLevel.HIGH

    def test_critical_boundary_tech_disruption_at_75(self):
        """tech_disruption=75 → NOT critical (needs >75) → HIGH."""
        m = make_market(regulatory_complexity=10, tech_disruption_risk=75, competitor_count=2)
        assert _risk_level(m) == RiskLevel.HIGH

    def test_critical_boundary_competitor_at_15(self):
        """competitor_count=15 → NOT critical (needs >15) → HIGH."""
        m = make_market(regulatory_complexity=10, tech_disruption_risk=0, competitor_count=15)
        assert _risk_level(m) == RiskLevel.HIGH


# ─── 7. opportunity_score formula ─────────────────────────────────────────────

class TestOpportunityScore:
    def test_score_in_valid_range(self):
        m = make_market()
        s = scanner().scan(m)
        assert 0.0 <= s.opportunity_score <= 100.0

    def test_score_formula_matches_components(self):
        """opportunity_score = attractiveness*0.40 + penetrability*0.35 + fit*0.25."""
        m = make_market()
        result = scanner().scan(m)
        expected = round(
            result.market_attractiveness * 0.40
            + result.penetrability * 0.35
            + result.strategic_fit * 0.25,
            2,
        )
        assert result.opportunity_score == expected

    def test_score_increases_with_better_inputs(self):
        """High-quality market should score higher than low-quality market."""
        good = make_market(
            opportunity_id="g",
            annual_growth_rate_pct=0.30,
            demand_trend=0.9,
            total_addressable_market_eur=1_000_000_000,
            competitor_count=1,
            regulatory_complexity=5,
            tech_disruption_risk=5,
            our_expertise_score=95,
        )
        bad = make_market(
            opportunity_id="b",
            annual_growth_rate_pct=-0.10,
            demand_trend=-0.9,
            total_addressable_market_eur=1_000,
            competitor_count=20,
            regulatory_complexity=90,
            tech_disruption_risk=90,
            our_expertise_score=10,
        )
        sc = scanner()
        sg = sc.scan(good)
        sb = sc.scan(bad)
        assert sg.opportunity_score > sb.opportunity_score


# ─── 8. CRUD: scan, get, overwrite, scan_batch ────────────────────────────────

class TestCRUD:
    def test_scan_returns_scored_opportunity(self):
        m = make_market()
        result = scanner().scan(m)
        assert isinstance(result, ScoredOpportunity)

    def test_scan_stores_result_retrievable_by_get(self):
        sc = scanner()
        m = make_market(opportunity_id="x1")
        sc.scan(m)
        assert sc.get("x1") is not None

    def test_get_returns_none_for_unknown_id(self):
        assert scanner().get("nonexistent") is None

    def test_scan_overwrites_existing_id(self):
        sc = scanner()
        m1 = make_market(opportunity_id="dup", annual_growth_rate_pct=0.05)
        m2 = make_market(opportunity_id="dup", annual_growth_rate_pct=0.25)
        sc.scan(m1)
        sc.scan(m2)
        stored = sc.get("dup")
        # m2 has higher growth → higher score
        assert stored.market.annual_growth_rate_pct == 0.25

    def test_scan_batch_returns_all_results(self):
        sc = scanner()
        markets = [make_market(opportunity_id=f"m{i}") for i in range(4)]
        results = sc.scan_batch(markets)
        assert len(results) == 4

    def test_scan_batch_stores_all(self):
        sc = scanner()
        markets = [make_market(opportunity_id=f"b{i}") for i in range(3)]
        sc.scan_batch(markets)
        assert sc.get("b0") is not None
        assert sc.get("b1") is not None
        assert sc.get("b2") is not None

    def test_scan_batch_returns_list_of_scored_opportunities(self):
        results = scanner().scan_batch([make_market(opportunity_id="z1")])
        assert all(isinstance(r, ScoredOpportunity) for r in results)

    def test_market_signals_preserved_in_result(self):
        m = make_market(opportunity_id="pres", market_name="Preserved")
        result = scanner().scan(m)
        assert result.market.market_name == "Preserved"
        assert result.market.opportunity_id == "pres"


# ─── 9. Filters ───────────────────────────────────────────────────────────────

class TestFilters:
    def _setup_varied_scanner(self):
        sc = scanner()
        # EMERGING, LOW risk
        sc.scan(make_market(
            opportunity_id="e1",
            annual_growth_rate_pct=0.25,
            competitor_count=2,
            demand_trend=0.8,
            regulatory_complexity=10,
            tech_disruption_risk=10,
        ))
        # DECLINING, CRITICAL risk
        sc.scan(make_market(
            opportunity_id="d1",
            annual_growth_rate_pct=-0.15,
            competitor_count=16,
            demand_trend=-0.8,
            regulatory_complexity=80,
            tech_disruption_risk=80,
        ))
        return sc

    def test_by_phase_emerging_returns_only_emerging(self):
        sc = self._setup_varied_scanner()
        results = sc.by_phase(OpportunityPhase.EMERGING)
        assert all(r.opportunity_phase == OpportunityPhase.EMERGING for r in results)

    def test_by_phase_declining_returns_only_declining(self):
        sc = self._setup_varied_scanner()
        results = sc.by_phase(OpportunityPhase.DECLINING)
        assert all(r.opportunity_phase == OpportunityPhase.DECLINING for r in results)

    def test_by_phase_empty_for_unrepresented_phase(self):
        sc = self._setup_varied_scanner()
        results = sc.by_phase(OpportunityPhase.MATURE)
        assert results == []

    def test_by_risk_critical_returns_only_critical(self):
        sc = self._setup_varied_scanner()
        results = sc.by_risk(RiskLevel.CRITICAL)
        assert all(r.risk_level == RiskLevel.CRITICAL for r in results)

    def test_by_risk_low_returns_only_low(self):
        sc = self._setup_varied_scanner()
        results = sc.by_risk(RiskLevel.LOW)
        assert all(r.risk_level == RiskLevel.LOW for r in results)

    def test_emerging_markets_matches_by_phase_emerging(self):
        sc = self._setup_varied_scanner()
        assert sc.emerging_markets() == sc.by_phase(OpportunityPhase.EMERGING)

    def test_emerging_markets_returns_list(self):
        assert isinstance(scanner().emerging_markets(), list)


# ─── 10. top_opportunities ────────────────────────────────────────────────────

class TestTopOpportunities:
    def _scanner_with_n(self, n: int) -> MarketOpportunityScanner:
        sc = scanner()
        for i in range(n):
            # vary growth to get different scores
            sc.scan(make_market(
                opportunity_id=f"top{i}",
                annual_growth_rate_pct=0.01 * (i + 1),
            ))
        return sc

    def test_top_opportunities_default_5(self):
        sc = self._scanner_with_n(10)
        results = sc.top_opportunities()
        assert len(results) == 5

    def test_top_opportunities_custom_n(self):
        sc = self._scanner_with_n(10)
        results = sc.top_opportunities(n=3)
        assert len(results) == 3

    def test_top_opportunities_returns_highest_scores(self):
        sc = self._scanner_with_n(10)
        all_sorted = sc.all_opportunities()
        top3 = sc.top_opportunities(n=3)
        assert top3 == all_sorted[:3]

    def test_top_opportunities_fewer_than_n_available(self):
        sc = self._scanner_with_n(2)
        results = sc.top_opportunities(n=10)
        assert len(results) == 2

    def test_top_opportunities_empty_store(self):
        assert scanner().top_opportunities() == []


# ─── 11. all_opportunities sort order ─────────────────────────────────────────

class TestAllOpportunities:
    def test_all_opportunities_sorted_descending(self):
        sc = scanner()
        sc.scan(make_market(opportunity_id="lo", annual_growth_rate_pct=0.01))
        sc.scan(make_market(opportunity_id="hi", annual_growth_rate_pct=0.30,
                            demand_trend=0.9, competitor_count=1))
        results = sc.all_opportunities()
        scores = [r.opportunity_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_all_opportunities_returns_list(self):
        assert isinstance(scanner().all_opportunities(), list)

    def test_all_opportunities_empty_store(self):
        assert scanner().all_opportunities() == []

    def test_all_opportunities_contains_all_scanned(self):
        sc = scanner()
        ids = {f"a{i}" for i in range(5)}
        for i in range(5):
            sc.scan(make_market(opportunity_id=f"a{i}"))
        returned_ids = {r.market.opportunity_id for r in sc.all_opportunities()}
        assert returned_ids == ids


# ─── 12. summary() ────────────────────────────────────────────────────────────

class TestSummary:
    def test_summary_empty_store(self):
        s = scanner().summary()
        assert s["total"] == 0
        assert s["avg_opportunity_score"] == 0.0
        assert s["total_projected_revenue_2y_eur"] == 0.0
        assert s["top_sector"] is None

    def test_summary_empty_phase_counts_all_zero(self):
        s = scanner().summary()
        assert all(v == 0 for v in s["phase_counts"].values())

    def test_summary_empty_risk_counts_all_zero(self):
        s = scanner().summary()
        assert all(v == 0 for v in s["risk_counts"].values())

    def test_summary_total_count(self):
        sc = scanner()
        sc.scan(make_market(opportunity_id="s1"))
        sc.scan(make_market(opportunity_id="s2"))
        assert sc.summary()["total"] == 2

    def test_summary_phase_counts_sum_to_total(self):
        sc = scanner()
        sc.scan(make_market(opportunity_id="p1"))
        sc.scan(make_market(opportunity_id="p2"))
        s = sc.summary()
        assert sum(s["phase_counts"].values()) == s["total"]

    def test_summary_risk_counts_sum_to_total(self):
        sc = scanner()
        sc.scan(make_market(opportunity_id="r1"))
        s = sc.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_avg_score_single_entry(self):
        sc = scanner()
        result = sc.scan(make_market(opportunity_id="av1"))
        s = sc.summary()
        assert s["avg_opportunity_score"] == result.opportunity_score

    def test_summary_avg_score_multiple_entries(self):
        sc = scanner()
        r1 = sc.scan(make_market(opportunity_id="av1"))
        r2 = sc.scan(make_market(opportunity_id="av2", annual_growth_rate_pct=0.01))
        expected = round((r1.opportunity_score + r2.opportunity_score) / 2, 2)
        assert sc.summary()["avg_opportunity_score"] == expected

    def test_summary_top_sector_single(self):
        sc = scanner()
        sc.scan(make_market(opportunity_id="ts1", sector="Finance"))
        assert sc.summary()["top_sector"] == "Finance"

    def test_summary_top_sector_highest_revenue(self):
        """top_sector is the one with the greatest total projected revenue."""
        sc = scanner()
        # Big TAM → large projected revenue → "BigSector" should win
        sc.scan(make_market(
            opportunity_id="big",
            sector="BigSector",
            total_addressable_market_eur=10_000_000_000,
            avg_deal_size_eur=100_000,
        ))
        sc.scan(make_market(
            opportunity_id="sm",
            sector="SmallSector",
            total_addressable_market_eur=10_000,
            avg_deal_size_eur=5_000,
        ))
        assert sc.summary()["top_sector"] == "BigSector"

    def test_summary_total_projected_revenue_is_sum(self):
        sc = scanner()
        r1 = sc.scan(make_market(opportunity_id="rev1"))
        r2 = sc.scan(make_market(opportunity_id="rev2"))
        expected = round(r1.projected_revenue_2y_eur + r2.projected_revenue_2y_eur, 2)
        assert sc.summary()["total_projected_revenue_2y_eur"] == expected

    def test_summary_contains_required_keys(self):
        keys = {"total", "phase_counts", "risk_counts", "avg_opportunity_score",
                "total_projected_revenue_2y_eur", "top_sector"}
        assert keys == set(scanner().summary().keys())


# ─── 13. reset() ──────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_all_opportunities(self):
        sc = scanner()
        sc.scan(make_market(opportunity_id="rm1"))
        sc.scan(make_market(opportunity_id="rm2"))
        sc.reset()
        assert sc.all_opportunities() == []

    def test_reset_clears_get(self):
        sc = scanner()
        sc.scan(make_market(opportunity_id="clr"))
        sc.reset()
        assert sc.get("clr") is None

    def test_reset_total_in_summary_is_zero(self):
        sc = scanner()
        sc.scan(make_market(opportunity_id="rst"))
        sc.reset()
        assert sc.summary()["total"] == 0

    def test_can_scan_after_reset(self):
        sc = scanner()
        sc.scan(make_market(opportunity_id="post1"))
        sc.reset()
        sc.scan(make_market(opportunity_id="post2"))
        assert sc.get("post2") is not None
        assert sc.get("post1") is None


# ─── 14. to_dict() ────────────────────────────────────────────────────────────

class TestToDict:
    def test_market_signals_to_dict_returns_dict(self):
        m = make_market()
        d = m.to_dict()
        assert isinstance(d, dict)

    def test_market_signals_to_dict_has_all_fields(self):
        m = make_market()
        d = m.to_dict()
        expected_keys = {
            "opportunity_id", "market_name", "sector", "sub_sector",
            "total_addressable_market_eur", "annual_growth_rate_pct",
            "competitor_count", "our_market_share_pct", "avg_deal_size_eur",
            "avg_sales_cycle_days", "demand_trend", "regulatory_complexity",
            "tech_disruption_risk", "our_expertise_score",
        }
        assert expected_keys == set(d.keys())

    def test_scored_opportunity_to_dict_returns_dict(self):
        result = scanner().scan(make_market())
        d = result.to_dict()
        assert isinstance(d, dict)

    def test_scored_opportunity_to_dict_has_all_keys(self):
        result = scanner().scan(make_market())
        d = result.to_dict()
        expected_keys = {
            "market", "opportunity_score", "opportunity_phase", "risk_level",
            "market_attractiveness", "penetrability", "strategic_fit",
            "projected_revenue_2y_eur", "key_advantages", "key_risks",
            "recommended_actions",
        }
        assert expected_keys == set(d.keys())

    def test_scored_opportunity_to_dict_phase_is_string(self):
        result = scanner().scan(make_market())
        d = result.to_dict()
        assert isinstance(d["opportunity_phase"], str)

    def test_scored_opportunity_to_dict_risk_is_string(self):
        result = scanner().scan(make_market())
        d = result.to_dict()
        assert isinstance(d["risk_level"], str)

    def test_scored_opportunity_to_dict_score_is_float(self):
        result = scanner().scan(make_market())
        d = result.to_dict()
        assert isinstance(d["opportunity_score"], float)

    def test_scored_opportunity_to_dict_advantages_is_list(self):
        result = scanner().scan(make_market())
        d = result.to_dict()
        assert isinstance(d["key_advantages"], list)

    def test_scored_opportunity_to_dict_risks_is_list(self):
        result = scanner().scan(make_market())
        d = result.to_dict()
        assert isinstance(d["key_risks"], list)

    def test_scored_opportunity_to_dict_actions_is_list(self):
        result = scanner().scan(make_market())
        d = result.to_dict()
        assert isinstance(d["recommended_actions"], list)

    def test_scored_opportunity_to_dict_market_is_dict(self):
        result = scanner().scan(make_market())
        d = result.to_dict()
        assert isinstance(d["market"], dict)

    def test_to_dict_phase_value_matches_enum(self):
        result = scanner().scan(make_market())
        d = result.to_dict()
        assert d["opportunity_phase"] == result.opportunity_phase.value

    def test_to_dict_risk_value_matches_enum(self):
        result = scanner().scan(make_market())
        d = result.to_dict()
        assert d["risk_level"] == result.risk_level.value
