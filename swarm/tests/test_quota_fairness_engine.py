"""
Comprehensive pytest test suite for QuotaFairnessEngine.
Target: 250+ tests covering enums, dataclasses, scoring functions, engine methods,
edge cases, boundary conditions, composite formula, and summary().
"""
from __future__ import annotations

import math
import pytest

from swarm.intelligence.quota_fairness_engine import (
    FairnessRating,
    FairnessRisk,
    BiasDirection,
    QuotaAction,
    QuotaFairnessInput,
    QuotaFairnessResult,
    QuotaFairnessEngine,
    _market_alignment_score,
    _experience_alignment_score,
    _peer_equity_score,
    _attainment_sustainability_score,
    _composite,
    _fairness_rating,
    _fairness_risk,
    _bias_direction,
    _quota_action,
    _estimated_fair_quota,
    _fairness_signal,
)


# ---------------------------------------------------------------------------
# Helpers / Fixtures
# ---------------------------------------------------------------------------

def make_input(
    *,
    rep_id: str = "REP001",
    rep_name: str = "Alice Smith",
    region: str = "North",
    annual_quota_usd: float = 1_000_000.0,
    territory_market_potential_usd: float = 4_000_000.0,
    tenure_months: int = 24,
    previous_year_attainment_pct: float = 90.0,
    industry_growth_rate_pct: float = 10.0,
    competitive_intensity_score: float = 40.0,
    account_count: int = 100,
    new_logo_quota_pct: float = 30.0,
    avg_deal_size_usd: float = 50_000.0,
    sales_cycle_avg_days: int = 60,
    team_avg_quota_usd: float = 1_000_000.0,
    team_avg_attainment_pct: float = 85.0,
    years_experience: float = 6.0,
    product_maturity_score: float = 80.0,
    territory_adjusted_last_year: int = 0,
    peer_quota_variance_pct: float = 0.0,
    quota_increase_yoy_pct: float = 5.0,
    ramp_adjustment_applied: int = 0,
    manager_override_pct: float = 0.0,
) -> QuotaFairnessInput:
    return QuotaFairnessInput(
        rep_id=rep_id,
        rep_name=rep_name,
        region=region,
        annual_quota_usd=annual_quota_usd,
        territory_market_potential_usd=territory_market_potential_usd,
        tenure_months=tenure_months,
        previous_year_attainment_pct=previous_year_attainment_pct,
        industry_growth_rate_pct=industry_growth_rate_pct,
        competitive_intensity_score=competitive_intensity_score,
        account_count=account_count,
        new_logo_quota_pct=new_logo_quota_pct,
        avg_deal_size_usd=avg_deal_size_usd,
        sales_cycle_avg_days=sales_cycle_avg_days,
        team_avg_quota_usd=team_avg_quota_usd,
        team_avg_attainment_pct=team_avg_attainment_pct,
        years_experience=years_experience,
        product_maturity_score=product_maturity_score,
        territory_adjusted_last_year=territory_adjusted_last_year,
        peer_quota_variance_pct=peer_quota_variance_pct,
        quota_increase_yoy_pct=quota_increase_yoy_pct,
        ramp_adjustment_applied=ramp_adjustment_applied,
        manager_override_pct=manager_override_pct,
    )


@pytest.fixture
def engine() -> QuotaFairnessEngine:
    return QuotaFairnessEngine()


@pytest.fixture
def baseline_input() -> QuotaFairnessInput:
    """A 'good' rep input that should score highly."""
    return make_input()


# ---------------------------------------------------------------------------
# 1. Enum Tests
# ---------------------------------------------------------------------------

class TestFairnessRatingEnum:
    def test_values(self):
        assert FairnessRating.VERY_FAIR.value == "very_fair"
        assert FairnessRating.FAIR.value == "fair"
        assert FairnessRating.QUESTIONABLE.value == "questionable"
        assert FairnessRating.UNFAIR.value == "unfair"

    def test_membership(self):
        members = list(FairnessRating)
        assert len(members) == 4

    def test_is_str_enum(self):
        assert isinstance(FairnessRating.VERY_FAIR, str)
        assert FairnessRating.VERY_FAIR == "very_fair"

    def test_str_comparison(self):
        assert FairnessRating.FAIR == "fair"
        assert FairnessRating.UNFAIR != "fair"


class TestFairnessRiskEnum:
    def test_values(self):
        assert FairnessRisk.LOW.value == "low"
        assert FairnessRisk.MODERATE.value == "moderate"
        assert FairnessRisk.HIGH.value == "high"
        assert FairnessRisk.CRITICAL.value == "critical"

    def test_membership(self):
        assert len(list(FairnessRisk)) == 4

    def test_is_str_enum(self):
        assert isinstance(FairnessRisk.LOW, str)


class TestBiasDirectionEnum:
    def test_values(self):
        assert BiasDirection.OVER_QUOTED.value == "over_quoted"
        assert BiasDirection.UNDER_QUOTED.value == "under_quoted"
        assert BiasDirection.BALANCED.value == "balanced"

    def test_membership(self):
        assert len(list(BiasDirection)) == 3

    def test_is_str_enum(self):
        assert isinstance(BiasDirection.BALANCED, str)


class TestQuotaActionEnum:
    def test_values(self):
        assert QuotaAction.MAINTAIN.value == "maintain"
        assert QuotaAction.RECALIBRATE_TERRITORY.value == "recalibrate_territory"
        assert QuotaAction.REDUCE_QUOTA.value == "reduce_quota"
        assert QuotaAction.INCREASE_QUOTA.value == "increase_quota"

    def test_membership(self):
        assert len(list(QuotaAction)) == 4

    def test_is_str_enum(self):
        assert isinstance(QuotaAction.MAINTAIN, str)


# ---------------------------------------------------------------------------
# 2. QuotaFairnessInput dataclass
# ---------------------------------------------------------------------------

class TestQuotaFairnessInput:
    def test_has_22_fields(self):
        inp = make_input()
        fields = inp.__dataclass_fields__
        assert len(fields) == 22

    def test_field_names(self):
        expected = {
            "rep_id", "rep_name", "region", "annual_quota_usd",
            "territory_market_potential_usd", "tenure_months",
            "previous_year_attainment_pct", "industry_growth_rate_pct",
            "competitive_intensity_score", "account_count",
            "new_logo_quota_pct", "avg_deal_size_usd", "sales_cycle_avg_days",
            "team_avg_quota_usd", "team_avg_attainment_pct",
            "years_experience", "product_maturity_score",
            "territory_adjusted_last_year", "peer_quota_variance_pct",
            "quota_increase_yoy_pct", "ramp_adjustment_applied",
            "manager_override_pct",
        }
        assert set(make_input().__dataclass_fields__.keys()) == expected

    def test_instantiation(self):
        inp = make_input(rep_id="X1", rep_name="Bob", region="West")
        assert inp.rep_id == "X1"
        assert inp.rep_name == "Bob"
        assert inp.region == "West"

    def test_numeric_fields_stored(self):
        inp = make_input(annual_quota_usd=500_000.0, tenure_months=12)
        assert inp.annual_quota_usd == 500_000.0
        assert inp.tenure_months == 12


# ---------------------------------------------------------------------------
# 3. QuotaFairnessResult dataclass & to_dict()
# ---------------------------------------------------------------------------

class TestQuotaFairnessResult:
    def _make_result(self) -> QuotaFairnessResult:
        return QuotaFairnessResult(
            rep_id="R1",
            rep_name="Test",
            fairness_rating=FairnessRating.FAIR,
            fairness_risk=FairnessRisk.MODERATE,
            bias_direction=BiasDirection.BALANCED,
            quota_action=QuotaAction.MAINTAIN,
            market_alignment_score=70.0,
            experience_alignment_score=80.0,
            peer_equity_score=75.0,
            attainment_sustainability_score=65.0,
            fairness_composite=60.0,
            is_over_quoted=False,
            is_under_quoted=False,
            estimated_fair_quota_usd=900_000.0,
            fairness_signal="primary fairness gap: peer equity",
        )

    def test_has_15_fields(self):
        r = self._make_result()
        assert len(r.__dataclass_fields__) == 15

    def test_to_dict_returns_15_keys(self):
        d = self._make_result().to_dict()
        assert len(d) == 15

    def test_to_dict_exact_keys(self):
        expected = {
            "rep_id", "rep_name", "fairness_rating", "fairness_risk",
            "bias_direction", "quota_action", "market_alignment_score",
            "experience_alignment_score", "peer_equity_score",
            "attainment_sustainability_score", "fairness_composite",
            "is_over_quoted", "is_under_quoted", "estimated_fair_quota_usd",
            "fairness_signal",
        }
        assert set(self._make_result().to_dict().keys()) == expected

    def test_to_dict_enum_values_are_strings(self):
        d = self._make_result().to_dict()
        assert d["fairness_rating"] == "fair"
        assert d["fairness_risk"] == "moderate"
        assert d["bias_direction"] == "balanced"
        assert d["quota_action"] == "maintain"

    def test_to_dict_bool_fields(self):
        d = self._make_result().to_dict()
        assert d["is_over_quoted"] is False
        assert d["is_under_quoted"] is False

    def test_to_dict_numeric_fields(self):
        d = self._make_result().to_dict()
        assert d["market_alignment_score"] == 70.0
        assert d["fairness_composite"] == 60.0
        assert d["estimated_fair_quota_usd"] == 900_000.0


# ---------------------------------------------------------------------------
# 4. _market_alignment_score
# ---------------------------------------------------------------------------

class TestMarketAlignmentScore:
    def test_ideal_range_20_to_40_pct(self):
        # quota = 30% of market => ideal => 40 pts for that component
        inp = make_input(annual_quota_usd=300_000, territory_market_potential_usd=1_000_000,
                         industry_growth_rate_pct=10, competitive_intensity_score=20,
                         product_maturity_score=100)
        score = _market_alignment_score(inp)
        assert score > 0

    def test_quota_pct_exactly_20(self):
        inp = make_input(annual_quota_usd=200_000, territory_market_potential_usd=1_000_000,
                         industry_growth_rate_pct=0, competitive_intensity_score=0,
                         product_maturity_score=0)
        score = _market_alignment_score(inp)
        # 40 + 10 + 20 + 0 = 70
        assert score == 70.0

    def test_quota_pct_exactly_40(self):
        inp = make_input(annual_quota_usd=400_000, territory_market_potential_usd=1_000_000,
                         industry_growth_rate_pct=0, competitive_intensity_score=0,
                         product_maturity_score=0)
        score = _market_alignment_score(inp)
        assert score == 70.0

    def test_quota_pct_15_to_20_range(self):
        # 17% => second band => 28 pts
        inp = make_input(annual_quota_usd=170_000, territory_market_potential_usd=1_000_000,
                         industry_growth_rate_pct=0, competitive_intensity_score=0,
                         product_maturity_score=0)
        score = _market_alignment_score(inp)
        assert score == 58.0  # 28 + 10 + 20 + 0

    def test_quota_pct_40_to_50_range(self):
        # 45% => 28 pts
        inp = make_input(annual_quota_usd=450_000, territory_market_potential_usd=1_000_000,
                         industry_growth_rate_pct=0, competitive_intensity_score=0,
                         product_maturity_score=0)
        score = _market_alignment_score(inp)
        assert score == 58.0

    def test_quota_pct_10_to_15_range(self):
        # 12% => 16 pts
        inp = make_input(annual_quota_usd=120_000, territory_market_potential_usd=1_000_000,
                         industry_growth_rate_pct=0, competitive_intensity_score=0,
                         product_maturity_score=0)
        score = _market_alignment_score(inp)
        assert score == 46.0

    def test_quota_pct_50_to_65_range(self):
        # 55% => 16 pts
        inp = make_input(annual_quota_usd=550_000, territory_market_potential_usd=1_000_000,
                         industry_growth_rate_pct=0, competitive_intensity_score=0,
                         product_maturity_score=0)
        score = _market_alignment_score(inp)
        assert score == 46.0

    def test_quota_pct_below_10(self):
        # 5% => 4 pts
        inp = make_input(annual_quota_usd=50_000, territory_market_potential_usd=1_000_000,
                         industry_growth_rate_pct=0, competitive_intensity_score=0,
                         product_maturity_score=0)
        score = _market_alignment_score(inp)
        assert score == 34.0

    def test_quota_pct_above_65(self):
        # 80% => 4 pts
        inp = make_input(annual_quota_usd=800_000, territory_market_potential_usd=1_000_000,
                         industry_growth_rate_pct=0, competitive_intensity_score=0,
                         product_maturity_score=0)
        score = _market_alignment_score(inp)
        assert score == 34.0

    def test_zero_market_potential_uses_50_pct_fallback(self):
        # territory_market_potential_usd=0 => quota_pct=50 => second band => 28
        inp = make_input(annual_quota_usd=1_000_000, territory_market_potential_usd=0,
                         industry_growth_rate_pct=0, competitive_intensity_score=0,
                         product_maturity_score=0)
        score = _market_alignment_score(inp)
        assert score == 58.0

    def test_industry_growth_above_20(self):
        inp = make_input(annual_quota_usd=300_000, territory_market_potential_usd=1_000_000,
                         industry_growth_rate_pct=25, competitive_intensity_score=0,
                         product_maturity_score=0)
        score = _market_alignment_score(inp)
        assert score == 80.0  # 40+20+20+0

    def test_industry_growth_10_to_20(self):
        inp = make_input(annual_quota_usd=300_000, territory_market_potential_usd=1_000_000,
                         industry_growth_rate_pct=15, competitive_intensity_score=0,
                         product_maturity_score=0)
        score = _market_alignment_score(inp)
        assert score == 75.0  # 40+15+20+0

    def test_industry_growth_0_to_10(self):
        inp = make_input(annual_quota_usd=300_000, territory_market_potential_usd=1_000_000,
                         industry_growth_rate_pct=5, competitive_intensity_score=0,
                         product_maturity_score=0)
        score = _market_alignment_score(inp)
        assert score == 70.0  # 40+10+20+0

    def test_industry_growth_minus10_to_0(self):
        inp = make_input(annual_quota_usd=300_000, territory_market_potential_usd=1_000_000,
                         industry_growth_rate_pct=-5, competitive_intensity_score=0,
                         product_maturity_score=0)
        score = _market_alignment_score(inp)
        assert score == 65.0  # 40+5+20+0

    def test_industry_growth_below_minus10(self):
        inp = make_input(annual_quota_usd=300_000, territory_market_potential_usd=1_000_000,
                         industry_growth_rate_pct=-15, competitive_intensity_score=0,
                         product_maturity_score=0)
        score = _market_alignment_score(inp)
        assert score == 60.0  # 40+0+20+0

    def test_competitive_intensity_above_80(self):
        inp = make_input(annual_quota_usd=300_000, territory_market_potential_usd=1_000_000,
                         industry_growth_rate_pct=0, competitive_intensity_score=85,
                         product_maturity_score=0)
        score = _market_alignment_score(inp)
        assert score == 55.0  # 40+10+5+0

    def test_competitive_intensity_60_to_80(self):
        inp = make_input(annual_quota_usd=300_000, territory_market_potential_usd=1_000_000,
                         industry_growth_rate_pct=0, competitive_intensity_score=70,
                         product_maturity_score=0)
        score = _market_alignment_score(inp)
        assert score == 62.0  # 40+10+12+0

    def test_competitive_intensity_40_to_60(self):
        inp = make_input(annual_quota_usd=300_000, territory_market_potential_usd=1_000_000,
                         industry_growth_rate_pct=0, competitive_intensity_score=50,
                         product_maturity_score=0)
        score = _market_alignment_score(inp)
        assert score == 68.0  # 40+10+18+0

    def test_competitive_intensity_below_40(self):
        inp = make_input(annual_quota_usd=300_000, territory_market_potential_usd=1_000_000,
                         industry_growth_rate_pct=0, competitive_intensity_score=30,
                         product_maturity_score=0)
        score = _market_alignment_score(inp)
        assert score == 70.0  # 40+10+20+0

    def test_product_maturity_contribution(self):
        inp = make_input(annual_quota_usd=300_000, territory_market_potential_usd=1_000_000,
                         industry_growth_rate_pct=0, competitive_intensity_score=0,
                         product_maturity_score=50)
        score = _market_alignment_score(inp)
        assert score == 80.0  # 40+10+20+10

    def test_product_maturity_max_100(self):
        inp = make_input(annual_quota_usd=300_000, territory_market_potential_usd=1_000_000,
                         industry_growth_rate_pct=0, competitive_intensity_score=0,
                         product_maturity_score=100)
        score = _market_alignment_score(inp)
        assert score == 90.0  # 40+10+20+20

    def test_score_capped_at_100(self):
        inp = make_input(annual_quota_usd=300_000, territory_market_potential_usd=1_000_000,
                         industry_growth_rate_pct=25, competitive_intensity_score=0,
                         product_maturity_score=100)
        score = _market_alignment_score(inp)
        assert score == 100.0  # 40+20+20+20 = 100

    def test_score_never_below_zero(self):
        inp = make_input(annual_quota_usd=0, territory_market_potential_usd=1_000_000,
                         industry_growth_rate_pct=-100, competitive_intensity_score=100,
                         product_maturity_score=0)
        score = _market_alignment_score(inp)
        assert score >= 0.0


# ---------------------------------------------------------------------------
# 5. _experience_alignment_score
# ---------------------------------------------------------------------------

class TestExperienceAlignmentScore:
    def test_high_experience_8_plus(self):
        inp = make_input(years_experience=10, ramp_adjustment_applied=0, tenure_months=24,
                         previous_year_attainment_pct=95, quota_increase_yoy_pct=5)
        score = _experience_alignment_score(inp)
        assert score == 100.0  # 30+20+30+20

    def test_experience_5_to_8(self):
        inp = make_input(years_experience=6, ramp_adjustment_applied=0, tenure_months=24,
                         previous_year_attainment_pct=95, quota_increase_yoy_pct=5)
        score = _experience_alignment_score(inp)
        assert score == 92.0  # 22+20+30+20

    def test_experience_3_to_5(self):
        inp = make_input(years_experience=4, ramp_adjustment_applied=0, tenure_months=24,
                         previous_year_attainment_pct=95, quota_increase_yoy_pct=5)
        score = _experience_alignment_score(inp)
        assert score == 85.0  # 15+20+30+20

    def test_experience_1_to_3(self):
        inp = make_input(years_experience=2, ramp_adjustment_applied=0, tenure_months=24,
                         previous_year_attainment_pct=95, quota_increase_yoy_pct=5)
        score = _experience_alignment_score(inp)
        assert score == 78.0  # 8+20+30+20

    def test_experience_below_1(self):
        inp = make_input(years_experience=0.5, ramp_adjustment_applied=0, tenure_months=24,
                         previous_year_attainment_pct=95, quota_increase_yoy_pct=5)
        score = _experience_alignment_score(inp)
        assert score == 70.0  # 0+20+30+20

    def test_ramp_adjustment_applied(self):
        inp = make_input(years_experience=10, ramp_adjustment_applied=1, tenure_months=24,
                         previous_year_attainment_pct=95, quota_increase_yoy_pct=5)
        score = _experience_alignment_score(inp)
        assert score == 100.0  # 30+20+30+20

    def test_no_ramp_but_new_rep_tenure_under_6(self):
        inp = make_input(years_experience=10, ramp_adjustment_applied=0, tenure_months=3,
                         previous_year_attainment_pct=95, quota_increase_yoy_pct=5)
        score = _experience_alignment_score(inp)
        assert score == 85.0  # 30+5+30+20

    def test_no_ramp_tenure_6_or_more(self):
        inp = make_input(years_experience=10, ramp_adjustment_applied=0, tenure_months=6,
                         previous_year_attainment_pct=95, quota_increase_yoy_pct=5)
        score = _experience_alignment_score(inp)
        assert score == 100.0  # 30+20+30+20

    def test_attainment_above_90(self):
        inp = make_input(years_experience=10, ramp_adjustment_applied=0, tenure_months=24,
                         previous_year_attainment_pct=100, quota_increase_yoy_pct=5)
        score = _experience_alignment_score(inp)
        assert score == 100.0

    def test_attainment_75_to_90(self):
        inp = make_input(years_experience=10, ramp_adjustment_applied=0, tenure_months=24,
                         previous_year_attainment_pct=80, quota_increase_yoy_pct=5)
        score = _experience_alignment_score(inp)
        assert score == 92.0  # 30+20+22+20

    def test_attainment_60_to_75(self):
        inp = make_input(years_experience=10, ramp_adjustment_applied=0, tenure_months=24,
                         previous_year_attainment_pct=65, quota_increase_yoy_pct=5)
        score = _experience_alignment_score(inp)
        assert score == 85.0  # 30+20+15+20

    def test_attainment_40_to_60(self):
        inp = make_input(years_experience=10, ramp_adjustment_applied=0, tenure_months=24,
                         previous_year_attainment_pct=50, quota_increase_yoy_pct=5)
        score = _experience_alignment_score(inp)
        assert score == 78.0  # 30+20+8+20

    def test_attainment_below_40(self):
        inp = make_input(years_experience=10, ramp_adjustment_applied=0, tenure_months=24,
                         previous_year_attainment_pct=30, quota_increase_yoy_pct=5)
        score = _experience_alignment_score(inp)
        assert score == 70.0  # 30+20+0+20

    def test_yoy_increase_le_10(self):
        inp = make_input(years_experience=10, ramp_adjustment_applied=0, tenure_months=24,
                         previous_year_attainment_pct=95, quota_increase_yoy_pct=10)
        score = _experience_alignment_score(inp)
        assert score == 100.0  # 30+20+30+20

    def test_yoy_increase_10_to_20(self):
        inp = make_input(years_experience=10, ramp_adjustment_applied=0, tenure_months=24,
                         previous_year_attainment_pct=95, quota_increase_yoy_pct=15)
        score = _experience_alignment_score(inp)
        assert score == 94.0  # 30+20+30+14

    def test_yoy_increase_20_to_30(self):
        inp = make_input(years_experience=10, ramp_adjustment_applied=0, tenure_months=24,
                         previous_year_attainment_pct=95, quota_increase_yoy_pct=25)
        score = _experience_alignment_score(inp)
        assert score == 87.0  # 30+20+30+7

    def test_yoy_increase_above_30(self):
        inp = make_input(years_experience=10, ramp_adjustment_applied=0, tenure_months=24,
                         previous_year_attainment_pct=95, quota_increase_yoy_pct=35)
        score = _experience_alignment_score(inp)
        assert score == 80.0  # 30+20+30+0

    def test_score_capped_at_100(self):
        inp = make_input(years_experience=10, ramp_adjustment_applied=1, tenure_months=24,
                         previous_year_attainment_pct=100, quota_increase_yoy_pct=0)
        score = _experience_alignment_score(inp)
        assert score == 100.0

    def test_score_minimum_zero(self):
        inp = make_input(years_experience=0, ramp_adjustment_applied=0, tenure_months=3,
                         previous_year_attainment_pct=0, quota_increase_yoy_pct=100)
        score = _experience_alignment_score(inp)
        assert score >= 0.0


# ---------------------------------------------------------------------------
# 6. _peer_equity_score
# ---------------------------------------------------------------------------

class TestPeerEquityScore:
    def test_variance_le_5(self):
        inp = make_input(peer_quota_variance_pct=3, annual_quota_usd=1_000_000,
                         team_avg_quota_usd=1_000_000, manager_override_pct=0)
        score = _peer_equity_score(inp)
        assert score == 100.0  # 50+30+20

    def test_variance_5_to_10(self):
        inp = make_input(peer_quota_variance_pct=8, annual_quota_usd=1_000_000,
                         team_avg_quota_usd=1_000_000, manager_override_pct=0)
        score = _peer_equity_score(inp)
        assert score == 88.0  # 38+30+20

    def test_variance_10_to_20(self):
        inp = make_input(peer_quota_variance_pct=15, annual_quota_usd=1_000_000,
                         team_avg_quota_usd=1_000_000, manager_override_pct=0)
        score = _peer_equity_score(inp)
        assert score == 72.0  # 22+30+20

    def test_variance_20_to_30(self):
        inp = make_input(peer_quota_variance_pct=25, annual_quota_usd=1_000_000,
                         team_avg_quota_usd=1_000_000, manager_override_pct=0)
        score = _peer_equity_score(inp)
        assert score == 60.0  # 10+30+20

    def test_variance_above_30(self):
        inp = make_input(peer_quota_variance_pct=40, annual_quota_usd=1_000_000,
                         team_avg_quota_usd=1_000_000, manager_override_pct=0)
        score = _peer_equity_score(inp)
        assert score == 50.0  # 0+30+20

    def test_negative_variance_uses_abs(self):
        inp = make_input(peer_quota_variance_pct=-8, annual_quota_usd=1_000_000,
                         team_avg_quota_usd=1_000_000, manager_override_pct=0)
        score = _peer_equity_score(inp)
        assert score == 88.0

    def test_team_var_le_10(self):
        inp = make_input(peer_quota_variance_pct=0, annual_quota_usd=1_050_000,
                         team_avg_quota_usd=1_000_000, manager_override_pct=0)
        score = _peer_equity_score(inp)
        assert score == 100.0  # 50+30+20

    def test_team_var_10_to_20(self):
        inp = make_input(peer_quota_variance_pct=0, annual_quota_usd=1_150_000,
                         team_avg_quota_usd=1_000_000, manager_override_pct=0)
        score = _peer_equity_score(inp)
        assert score == 90.0  # 50+20+20

    def test_team_var_20_to_35(self):
        inp = make_input(peer_quota_variance_pct=0, annual_quota_usd=1_300_000,
                         team_avg_quota_usd=1_000_000, manager_override_pct=0)
        score = _peer_equity_score(inp)
        assert score == 80.0  # 50+10+20

    def test_team_var_above_35(self):
        inp = make_input(peer_quota_variance_pct=0, annual_quota_usd=1_500_000,
                         team_avg_quota_usd=1_000_000, manager_override_pct=0)
        score = _peer_equity_score(inp)
        assert score == 70.0  # 50+0+20

    def test_team_avg_zero_uses_zero_variance(self):
        inp = make_input(peer_quota_variance_pct=0, annual_quota_usd=1_000_000,
                         team_avg_quota_usd=0, manager_override_pct=0)
        score = _peer_equity_score(inp)
        assert score == 100.0

    def test_manager_override_le_5(self):
        inp = make_input(peer_quota_variance_pct=0, annual_quota_usd=1_000_000,
                         team_avg_quota_usd=1_000_000, manager_override_pct=3)
        score = _peer_equity_score(inp)
        assert score == 100.0

    def test_manager_override_5_to_10(self):
        inp = make_input(peer_quota_variance_pct=0, annual_quota_usd=1_000_000,
                         team_avg_quota_usd=1_000_000, manager_override_pct=8)
        score = _peer_equity_score(inp)
        assert score == 94.0  # 50+30+14

    def test_manager_override_10_to_20(self):
        inp = make_input(peer_quota_variance_pct=0, annual_quota_usd=1_000_000,
                         team_avg_quota_usd=1_000_000, manager_override_pct=15)
        score = _peer_equity_score(inp)
        assert score == 87.0  # 50+30+7

    def test_manager_override_above_20(self):
        inp = make_input(peer_quota_variance_pct=0, annual_quota_usd=1_000_000,
                         team_avg_quota_usd=1_000_000, manager_override_pct=25)
        score = _peer_equity_score(inp)
        assert score == 80.0  # 50+30+0

    def test_negative_manager_override_uses_abs(self):
        inp = make_input(peer_quota_variance_pct=0, annual_quota_usd=1_000_000,
                         team_avg_quota_usd=1_000_000, manager_override_pct=-8)
        score = _peer_equity_score(inp)
        assert score == 94.0

    def test_score_capped_at_100(self):
        inp = make_input(peer_quota_variance_pct=0, annual_quota_usd=1_000_000,
                         team_avg_quota_usd=1_000_000, manager_override_pct=0)
        score = _peer_equity_score(inp)
        assert score <= 100.0

    def test_score_never_below_zero(self):
        inp = make_input(peer_quota_variance_pct=100, annual_quota_usd=2_000_000,
                         team_avg_quota_usd=1_000_000, manager_override_pct=50)
        score = _peer_equity_score(inp)
        assert score >= 0.0


# ---------------------------------------------------------------------------
# 7. _attainment_sustainability_score
# ---------------------------------------------------------------------------

class TestAttainmentSustainabilityScore:
    def test_all_best_conditions(self):
        inp = make_input(team_avg_attainment_pct=90, previous_year_attainment_pct=90,
                         annual_quota_usd=100_000, avg_deal_size_usd=1_000,
                         account_count=10_000, territory_adjusted_last_year=0)
        score = _attainment_sustainability_score(inp)
        assert score == 100.0  # 35+30+20+15

    def test_team_attainment_above_85(self):
        inp = make_input(team_avg_attainment_pct=90, previous_year_attainment_pct=90,
                         annual_quota_usd=100_000, avg_deal_size_usd=1_000,
                         account_count=10_000, territory_adjusted_last_year=0)
        score = _attainment_sustainability_score(inp)
        # 35 for team component
        assert score == 100.0

    def test_team_attainment_75_to_85(self):
        inp = make_input(team_avg_attainment_pct=80, previous_year_attainment_pct=90,
                         annual_quota_usd=100_000, avg_deal_size_usd=1_000,
                         account_count=10_000, territory_adjusted_last_year=0)
        score = _attainment_sustainability_score(inp)
        assert score == 90.0  # 25+30+20+15

    def test_team_attainment_65_to_75(self):
        inp = make_input(team_avg_attainment_pct=70, previous_year_attainment_pct=90,
                         annual_quota_usd=100_000, avg_deal_size_usd=1_000,
                         account_count=10_000, territory_adjusted_last_year=0)
        score = _attainment_sustainability_score(inp)
        assert score == 80.0  # 15+30+20+15

    def test_team_attainment_50_to_65(self):
        inp = make_input(team_avg_attainment_pct=55, previous_year_attainment_pct=90,
                         annual_quota_usd=100_000, avg_deal_size_usd=1_000,
                         account_count=10_000, territory_adjusted_last_year=0)
        score = _attainment_sustainability_score(inp)
        assert score == 72.0  # 7+30+20+15

    def test_team_attainment_below_50(self):
        inp = make_input(team_avg_attainment_pct=40, previous_year_attainment_pct=90,
                         annual_quota_usd=100_000, avg_deal_size_usd=1_000,
                         account_count=10_000, territory_adjusted_last_year=0)
        score = _attainment_sustainability_score(inp)
        assert score == 65.0  # 0+30+20+15

    def test_prev_attainment_above_80(self):
        inp = make_input(team_avg_attainment_pct=90, previous_year_attainment_pct=85,
                         annual_quota_usd=100_000, avg_deal_size_usd=1_000,
                         account_count=10_000, territory_adjusted_last_year=0)
        score = _attainment_sustainability_score(inp)
        assert score == 100.0

    def test_prev_attainment_65_to_80(self):
        inp = make_input(team_avg_attainment_pct=90, previous_year_attainment_pct=70,
                         annual_quota_usd=100_000, avg_deal_size_usd=1_000,
                         account_count=10_000, territory_adjusted_last_year=0)
        score = _attainment_sustainability_score(inp)
        assert score == 92.0  # 35+22+20+15

    def test_prev_attainment_50_to_65(self):
        inp = make_input(team_avg_attainment_pct=90, previous_year_attainment_pct=55,
                         annual_quota_usd=100_000, avg_deal_size_usd=1_000,
                         account_count=10_000, territory_adjusted_last_year=0)
        score = _attainment_sustainability_score(inp)
        assert score == 82.0  # 35+12+20+15

    def test_prev_attainment_below_50(self):
        inp = make_input(team_avg_attainment_pct=90, previous_year_attainment_pct=40,
                         annual_quota_usd=100_000, avg_deal_size_usd=1_000,
                         account_count=10_000, territory_adjusted_last_year=0)
        score = _attainment_sustainability_score(inp)
        assert score == 70.0  # 35+0+20+15

    def test_account_count_above_5x_deals_needed(self):
        # deals_needed = 100000/1000 = 100; account_count > 500
        inp = make_input(team_avg_attainment_pct=90, previous_year_attainment_pct=90,
                         annual_quota_usd=100_000, avg_deal_size_usd=1_000,
                         account_count=600, territory_adjusted_last_year=0)
        score = _attainment_sustainability_score(inp)
        assert score == 100.0

    def test_account_count_3x_to_5x_deals_needed(self):
        # deals_needed=100; 4*100=400 accounts
        inp = make_input(team_avg_attainment_pct=90, previous_year_attainment_pct=90,
                         annual_quota_usd=100_000, avg_deal_size_usd=1_000,
                         account_count=400, territory_adjusted_last_year=0)
        score = _attainment_sustainability_score(inp)
        assert score == 94.0  # 35+30+14+15

    def test_account_count_1x_to_3x_deals_needed(self):
        # deals_needed=100; 2*100=200 accounts
        inp = make_input(team_avg_attainment_pct=90, previous_year_attainment_pct=90,
                         annual_quota_usd=100_000, avg_deal_size_usd=1_000,
                         account_count=200, territory_adjusted_last_year=0)
        score = _attainment_sustainability_score(inp)
        assert score == 87.0  # 35+30+7+15

    def test_account_count_below_deals_needed(self):
        # deals_needed=100; account_count=50
        inp = make_input(team_avg_attainment_pct=90, previous_year_attainment_pct=90,
                         annual_quota_usd=100_000, avg_deal_size_usd=1_000,
                         account_count=50, territory_adjusted_last_year=0)
        score = _attainment_sustainability_score(inp)
        assert score == 80.0  # 35+30+0+15

    def test_territory_not_adjusted(self):
        inp = make_input(team_avg_attainment_pct=90, previous_year_attainment_pct=90,
                         annual_quota_usd=100_000, avg_deal_size_usd=1_000,
                         account_count=10_000, territory_adjusted_last_year=0)
        score = _attainment_sustainability_score(inp)
        assert score == 100.0  # includes 15 pts

    def test_territory_adjusted(self):
        inp = make_input(team_avg_attainment_pct=90, previous_year_attainment_pct=90,
                         annual_quota_usd=100_000, avg_deal_size_usd=1_000,
                         account_count=10_000, territory_adjusted_last_year=1)
        score = _attainment_sustainability_score(inp)
        assert score == 90.0  # 35+30+20+5

    def test_avg_deal_size_zero_uses_max_1(self):
        # deals_needed = 100000 / 1 = 100000; account_count=10 < deals_needed
        inp = make_input(team_avg_attainment_pct=90, previous_year_attainment_pct=90,
                         annual_quota_usd=100_000, avg_deal_size_usd=0,
                         account_count=10, territory_adjusted_last_year=0)
        score = _attainment_sustainability_score(inp)
        assert score == 80.0  # 35+30+0+15

    def test_score_capped_at_100(self):
        inp = make_input(team_avg_attainment_pct=100, previous_year_attainment_pct=100,
                         annual_quota_usd=100_000, avg_deal_size_usd=1_000,
                         account_count=100_000, territory_adjusted_last_year=0)
        score = _attainment_sustainability_score(inp)
        assert score <= 100.0

    def test_score_never_below_zero(self):
        inp = make_input(team_avg_attainment_pct=0, previous_year_attainment_pct=0,
                         annual_quota_usd=100_000, avg_deal_size_usd=1_000,
                         account_count=0, territory_adjusted_last_year=1)
        score = _attainment_sustainability_score(inp)
        assert score >= 0.0


# ---------------------------------------------------------------------------
# 8. _composite formula
# ---------------------------------------------------------------------------

class TestCompositeFormula:
    def test_formula_weights(self):
        result = _composite(80.0, 60.0, 70.0, 50.0)
        expected = round(80.0 * 0.30 + 60.0 * 0.25 + 70.0 * 0.25 + 50.0 * 0.20, 1)
        assert result == expected

    def test_all_100_gives_100(self):
        assert _composite(100.0, 100.0, 100.0, 100.0) == 100.0

    def test_all_0_gives_0(self):
        assert _composite(0.0, 0.0, 0.0, 0.0) == 0.0

    def test_rounding_to_one_decimal(self):
        result = _composite(33.3, 33.3, 33.3, 33.3)
        assert isinstance(result, float)
        # result should have at most 1 decimal
        assert result == round(result, 1)

    def test_market_weight_30_pct(self):
        # Only market score contributes
        result = _composite(100.0, 0.0, 0.0, 0.0)
        assert result == 30.0

    def test_experience_weight_25_pct(self):
        result = _composite(0.0, 100.0, 0.0, 0.0)
        assert result == 25.0

    def test_peer_weight_25_pct(self):
        result = _composite(0.0, 0.0, 100.0, 0.0)
        assert result == 25.0

    def test_attainment_weight_20_pct(self):
        result = _composite(0.0, 0.0, 0.0, 100.0)
        assert result == 20.0

    def test_weights_sum_to_100(self):
        # 30+25+25+20 = 100
        assert _composite(100.0, 100.0, 100.0, 100.0) == 100.0

    def test_specific_values(self):
        result = _composite(50.0, 50.0, 50.0, 50.0)
        assert result == 50.0


# ---------------------------------------------------------------------------
# 9. _fairness_rating
# ---------------------------------------------------------------------------

class TestFairnessRating:
    def test_75_and_above_very_fair(self):
        assert _fairness_rating(75.0) == FairnessRating.VERY_FAIR
        assert _fairness_rating(100.0) == FairnessRating.VERY_FAIR
        assert _fairness_rating(80.0) == FairnessRating.VERY_FAIR

    def test_55_to_75_fair(self):
        assert _fairness_rating(55.0) == FairnessRating.FAIR
        assert _fairness_rating(74.9) == FairnessRating.FAIR
        assert _fairness_rating(65.0) == FairnessRating.FAIR

    def test_35_to_55_questionable(self):
        assert _fairness_rating(35.0) == FairnessRating.QUESTIONABLE
        assert _fairness_rating(54.9) == FairnessRating.QUESTIONABLE
        assert _fairness_rating(45.0) == FairnessRating.QUESTIONABLE

    def test_below_35_unfair(self):
        assert _fairness_rating(34.9) == FairnessRating.UNFAIR
        assert _fairness_rating(0.0) == FairnessRating.UNFAIR
        assert _fairness_rating(20.0) == FairnessRating.UNFAIR

    def test_boundary_75_exact(self):
        assert _fairness_rating(75.0) == FairnessRating.VERY_FAIR

    def test_boundary_55_exact(self):
        assert _fairness_rating(55.0) == FairnessRating.FAIR

    def test_boundary_35_exact(self):
        assert _fairness_rating(35.0) == FairnessRating.QUESTIONABLE


# ---------------------------------------------------------------------------
# 10. _fairness_risk
# ---------------------------------------------------------------------------

class TestFairnessRisk:
    def test_below_25_critical(self):
        assert _fairness_risk(24.9) == FairnessRisk.CRITICAL
        assert _fairness_risk(0.0) == FairnessRisk.CRITICAL

    def test_25_to_40_high(self):
        assert _fairness_risk(25.0) == FairnessRisk.HIGH
        assert _fairness_risk(39.9) == FairnessRisk.HIGH

    def test_40_to_60_moderate(self):
        assert _fairness_risk(40.0) == FairnessRisk.MODERATE
        assert _fairness_risk(59.9) == FairnessRisk.MODERATE

    def test_60_and_above_low(self):
        assert _fairness_risk(60.0) == FairnessRisk.LOW
        assert _fairness_risk(100.0) == FairnessRisk.LOW

    def test_boundary_25_exact(self):
        assert _fairness_risk(25.0) == FairnessRisk.HIGH

    def test_boundary_40_exact(self):
        assert _fairness_risk(40.0) == FairnessRisk.MODERATE

    def test_boundary_60_exact(self):
        assert _fairness_risk(60.0) == FairnessRisk.LOW


# ---------------------------------------------------------------------------
# 11. _bias_direction
# ---------------------------------------------------------------------------

class TestBiasDirection:
    def test_over_quoted_via_peer_variance(self):
        inp = make_input(peer_quota_variance_pct=20, previous_year_attainment_pct=90,
                         quota_increase_yoy_pct=5)
        bias = _bias_direction(inp, composite=40.0)
        assert bias == BiasDirection.OVER_QUOTED

    def test_under_quoted_via_peer_variance(self):
        inp = make_input(peer_quota_variance_pct=-20, previous_year_attainment_pct=90,
                         quota_increase_yoy_pct=5)
        bias = _bias_direction(inp, composite=40.0)
        assert bias == BiasDirection.UNDER_QUOTED

    def test_over_quoted_via_attainment_and_yoy(self):
        inp = make_input(peer_quota_variance_pct=5, previous_year_attainment_pct=50,
                         quota_increase_yoy_pct=15)
        bias = _bias_direction(inp, composite=80.0)
        assert bias == BiasDirection.OVER_QUOTED

    def test_under_quoted_via_high_attainment(self):
        inp = make_input(peer_quota_variance_pct=5, previous_year_attainment_pct=125,
                         quota_increase_yoy_pct=5)
        bias = _bias_direction(inp, composite=80.0)
        assert bias == BiasDirection.UNDER_QUOTED

    def test_balanced_default(self):
        inp = make_input(peer_quota_variance_pct=5, previous_year_attainment_pct=90,
                         quota_increase_yoy_pct=5)
        bias = _bias_direction(inp, composite=80.0)
        assert bias == BiasDirection.BALANCED

    def test_peer_variance_exactly_15_not_over(self):
        # Threshold is >15 (strict), so 15 alone doesn't trigger over_quoted
        inp = make_input(peer_quota_variance_pct=15, previous_year_attainment_pct=90,
                         quota_increase_yoy_pct=5)
        bias = _bias_direction(inp, composite=40.0)
        # 15 is not > 15, so no over_quoted from variance
        # prev_attainment=90 >= 60, so no over_quoted from attainment rule
        # prev_attainment=90 <= 120, so no under_quoted
        assert bias == BiasDirection.BALANCED

    def test_peer_variance_over_15_but_composite_ge_55_balanced(self):
        inp = make_input(peer_quota_variance_pct=20, previous_year_attainment_pct=90,
                         quota_increase_yoy_pct=5)
        bias = _bias_direction(inp, composite=60.0)
        # peer_quota_variance_pct > 15 but composite >= 55 => no OVER_QUOTED via first rule
        # prev_attainment=90 >= 60 => no OVER_QUOTED via second rule
        # prev_attainment=90 <= 120 => no UNDER_QUOTED
        assert bias == BiasDirection.BALANCED

    def test_under_peer_variance_exactly_minus15_not_under(self):
        inp = make_input(peer_quota_variance_pct=-15, previous_year_attainment_pct=90,
                         quota_increase_yoy_pct=5)
        bias = _bias_direction(inp, composite=40.0)
        assert bias == BiasDirection.BALANCED

    def test_prev_attainment_exactly_60_not_over(self):
        # Rule: prev_attainment < 60, so exactly 60 is safe
        inp = make_input(peer_quota_variance_pct=5, previous_year_attainment_pct=60,
                         quota_increase_yoy_pct=15)
        bias = _bias_direction(inp, composite=80.0)
        assert bias == BiasDirection.BALANCED

    def test_prev_attainment_exactly_120_not_under(self):
        # Rule: prev_attainment > 120, so exactly 120 doesn't trigger
        inp = make_input(peer_quota_variance_pct=5, previous_year_attainment_pct=120,
                         quota_increase_yoy_pct=5)
        bias = _bias_direction(inp, composite=80.0)
        assert bias == BiasDirection.BALANCED


# ---------------------------------------------------------------------------
# 12. _quota_action
# ---------------------------------------------------------------------------

class TestQuotaAction:
    def test_critical_over_quoted_reduce(self):
        action = _quota_action(FairnessRisk.CRITICAL, BiasDirection.OVER_QUOTED)
        assert action == QuotaAction.REDUCE_QUOTA

    def test_critical_under_quoted_increase(self):
        action = _quota_action(FairnessRisk.CRITICAL, BiasDirection.UNDER_QUOTED)
        assert action == QuotaAction.INCREASE_QUOTA

    def test_critical_balanced_recalibrate(self):
        action = _quota_action(FairnessRisk.CRITICAL, BiasDirection.BALANCED)
        assert action == QuotaAction.RECALIBRATE_TERRITORY

    def test_high_over_quoted_reduce(self):
        action = _quota_action(FairnessRisk.HIGH, BiasDirection.OVER_QUOTED)
        assert action == QuotaAction.REDUCE_QUOTA

    def test_high_under_quoted_increase(self):
        action = _quota_action(FairnessRisk.HIGH, BiasDirection.UNDER_QUOTED)
        assert action == QuotaAction.INCREASE_QUOTA

    def test_high_balanced_recalibrate(self):
        action = _quota_action(FairnessRisk.HIGH, BiasDirection.BALANCED)
        assert action == QuotaAction.RECALIBRATE_TERRITORY

    def test_moderate_any_bias_recalibrate(self):
        assert _quota_action(FairnessRisk.MODERATE, BiasDirection.OVER_QUOTED) == QuotaAction.RECALIBRATE_TERRITORY
        assert _quota_action(FairnessRisk.MODERATE, BiasDirection.UNDER_QUOTED) == QuotaAction.RECALIBRATE_TERRITORY
        assert _quota_action(FairnessRisk.MODERATE, BiasDirection.BALANCED) == QuotaAction.RECALIBRATE_TERRITORY

    def test_low_any_bias_maintain(self):
        assert _quota_action(FairnessRisk.LOW, BiasDirection.OVER_QUOTED) == QuotaAction.MAINTAIN
        assert _quota_action(FairnessRisk.LOW, BiasDirection.UNDER_QUOTED) == QuotaAction.MAINTAIN
        assert _quota_action(FairnessRisk.LOW, BiasDirection.BALANCED) == QuotaAction.MAINTAIN


# ---------------------------------------------------------------------------
# 13. _estimated_fair_quota
# ---------------------------------------------------------------------------

class TestEstimatedFairQuota:
    def test_zero_market_returns_original_quota(self):
        inp = make_input(annual_quota_usd=500_000, territory_market_potential_usd=0)
        assert _estimated_fair_quota(inp) == 500_000.0

    def test_negative_market_returns_original_quota(self):
        inp = make_input(annual_quota_usd=500_000, territory_market_potential_usd=-100)
        assert _estimated_fair_quota(inp) == 500_000.0

    def test_base_is_30_pct_of_market(self):
        # No experience/growth/competitive adjustments
        inp = make_input(territory_market_potential_usd=1_000_000, years_experience=10,
                         industry_growth_rate_pct=0, competitive_intensity_score=50)
        fair = _estimated_fair_quota(inp)
        # base=300000 * 1.0 (exp>=5) * max(0.8,min(1.3, 1.0)) * 1.0 (competitive < 70)
        assert fair == 300_000.0

    def test_experience_below_3_reduces_by_30pct(self):
        inp = make_input(territory_market_potential_usd=1_000_000, years_experience=2,
                         industry_growth_rate_pct=0, competitive_intensity_score=50)
        fair = _estimated_fair_quota(inp)
        assert fair == round(1_000_000 * 0.30 * 0.70 * 1.0, 2)

    def test_experience_3_to_5_reduces_by_15pct(self):
        inp = make_input(territory_market_potential_usd=1_000_000, years_experience=4,
                         industry_growth_rate_pct=0, competitive_intensity_score=50)
        fair = _estimated_fair_quota(inp)
        assert fair == round(1_000_000 * 0.30 * 0.85 * 1.0, 2)

    def test_industry_growth_increases_quota(self):
        inp = make_input(territory_market_potential_usd=1_000_000, years_experience=10,
                         industry_growth_rate_pct=20, competitive_intensity_score=50)
        fair = _estimated_fair_quota(inp)
        # base=300000 * 1.0 * min(1.3, max(0.8, 1.20)) = 300000 * 1.2
        assert fair == round(300_000 * 1.2, 2)

    def test_industry_growth_capped_at_1_3(self):
        inp = make_input(territory_market_potential_usd=1_000_000, years_experience=10,
                         industry_growth_rate_pct=50, competitive_intensity_score=50)
        fair = _estimated_fair_quota(inp)
        # growth_factor = 1.5, capped at 1.3
        assert fair == round(300_000 * 1.3, 2)

    def test_industry_decline_floored_at_0_8(self):
        inp = make_input(territory_market_potential_usd=1_000_000, years_experience=10,
                         industry_growth_rate_pct=-50, competitive_intensity_score=50)
        fair = _estimated_fair_quota(inp)
        # growth_factor = 0.5, floored at 0.8
        assert fair == round(300_000 * 0.8, 2)

    def test_competitive_intensity_above_70_reduces(self):
        inp = make_input(territory_market_potential_usd=1_000_000, years_experience=10,
                         industry_growth_rate_pct=0, competitive_intensity_score=75)
        fair = _estimated_fair_quota(inp)
        assert fair == round(300_000 * 1.0 * 0.85, 2)

    def test_competitive_intensity_below_70_no_reduction(self):
        inp = make_input(territory_market_potential_usd=1_000_000, years_experience=10,
                         industry_growth_rate_pct=0, competitive_intensity_score=69)
        fair = _estimated_fair_quota(inp)
        assert fair == round(300_000 * 1.0, 2)

    def test_result_rounded_to_2_decimals(self):
        inp = make_input(territory_market_potential_usd=1_000_001, years_experience=10,
                         industry_growth_rate_pct=0, competitive_intensity_score=50)
        fair = _estimated_fair_quota(inp)
        assert fair == round(fair, 2)


# ---------------------------------------------------------------------------
# 14. _fairness_signal
# ---------------------------------------------------------------------------

class TestFairnessSignal:
    def test_peer_variance_above_25_mentions_review(self):
        inp = make_input(peer_quota_variance_pct=30, previous_year_attainment_pct=90,
                         quota_increase_yoy_pct=5, team_avg_attainment_pct=85)
        signal = _fairness_signal(inp, 80, 80, 80, 80)
        assert "review required" in signal
        assert "30%" in signal

    def test_peer_variance_below_minus25_mentions_under_assignment(self):
        inp = make_input(peer_quota_variance_pct=-30, previous_year_attainment_pct=90,
                         quota_increase_yoy_pct=5, team_avg_attainment_pct=85)
        signal = _fairness_signal(inp, 80, 80, 80, 80)
        assert "under-assignment" in signal
        assert "30%" in signal

    def test_yoy_increase_with_low_attainment(self):
        inp = make_input(peer_quota_variance_pct=10, previous_year_attainment_pct=60,
                         quota_increase_yoy_pct=30, team_avg_attainment_pct=85)
        signal = _fairness_signal(inp, 80, 80, 80, 80)
        assert "YoY" in signal or "quota increased" in signal

    def test_team_avg_attainment_below_60_systemic(self):
        inp = make_input(peer_quota_variance_pct=10, previous_year_attainment_pct=90,
                         quota_increase_yoy_pct=5, team_avg_attainment_pct=55)
        signal = _fairness_signal(inp, 80, 80, 80, 80)
        assert "systemic" in signal or "team average" in signal.lower()

    def test_fallback_to_weakest_score(self):
        inp = make_input(peer_quota_variance_pct=5, previous_year_attainment_pct=90,
                         quota_increase_yoy_pct=5, team_avg_attainment_pct=85)
        signal = _fairness_signal(inp, 80, 30, 80, 80)  # experience is weakest
        assert "experience alignment" in signal

    def test_fallback_market_alignment_weakest(self):
        inp = make_input(peer_quota_variance_pct=5, previous_year_attainment_pct=90,
                         quota_increase_yoy_pct=5, team_avg_attainment_pct=85)
        signal = _fairness_signal(inp, 20, 80, 80, 80)
        assert "market alignment" in signal

    def test_fallback_peer_equity_weakest(self):
        inp = make_input(peer_quota_variance_pct=5, previous_year_attainment_pct=90,
                         quota_increase_yoy_pct=5, team_avg_attainment_pct=85)
        signal = _fairness_signal(inp, 80, 80, 10, 80)
        assert "peer equity" in signal

    def test_fallback_attainment_sustainability_weakest(self):
        inp = make_input(peer_quota_variance_pct=5, previous_year_attainment_pct=90,
                         quota_increase_yoy_pct=5, team_avg_attainment_pct=85)
        signal = _fairness_signal(inp, 80, 80, 80, 5)
        assert "attainment sustainability" in signal

    def test_returns_string(self):
        inp = make_input()
        signal = _fairness_signal(inp, 70, 70, 70, 70)
        assert isinstance(signal, str)
        assert len(signal) > 0


# ---------------------------------------------------------------------------
# 15. QuotaFairnessEngine.assess()
# ---------------------------------------------------------------------------

class TestEngineAssess:
    def test_returns_result_type(self, engine, baseline_input):
        result = engine.assess(baseline_input)
        assert isinstance(result, QuotaFairnessResult)

    def test_rep_id_and_name_preserved(self, engine):
        inp = make_input(rep_id="R99", rep_name="Jane Doe")
        result = engine.assess(inp)
        assert result.rep_id == "R99"
        assert result.rep_name == "Jane Doe"

    def test_scores_are_floats(self, engine, baseline_input):
        result = engine.assess(baseline_input)
        assert isinstance(result.market_alignment_score, float)
        assert isinstance(result.experience_alignment_score, float)
        assert isinstance(result.peer_equity_score, float)
        assert isinstance(result.attainment_sustainability_score, float)
        assert isinstance(result.fairness_composite, float)

    def test_scores_in_range_0_100(self, engine, baseline_input):
        result = engine.assess(baseline_input)
        for score in [result.market_alignment_score, result.experience_alignment_score,
                      result.peer_equity_score, result.attainment_sustainability_score]:
            assert 0.0 <= score <= 100.0

    def test_composite_matches_formula(self, engine, baseline_input):
        result = engine.assess(baseline_input)
        expected = _composite(result.market_alignment_score, result.experience_alignment_score,
                              result.peer_equity_score, result.attainment_sustainability_score)
        assert result.fairness_composite == expected

    def test_fairness_rating_type(self, engine, baseline_input):
        result = engine.assess(baseline_input)
        assert isinstance(result.fairness_rating, FairnessRating)

    def test_fairness_risk_type(self, engine, baseline_input):
        result = engine.assess(baseline_input)
        assert isinstance(result.fairness_risk, FairnessRisk)

    def test_bias_direction_type(self, engine, baseline_input):
        result = engine.assess(baseline_input)
        assert isinstance(result.bias_direction, BiasDirection)

    def test_quota_action_type(self, engine, baseline_input):
        result = engine.assess(baseline_input)
        assert isinstance(result.quota_action, QuotaAction)

    def test_is_over_quoted_bool(self, engine, baseline_input):
        result = engine.assess(baseline_input)
        assert isinstance(result.is_over_quoted, bool)

    def test_is_under_quoted_bool(self, engine, baseline_input):
        result = engine.assess(baseline_input)
        assert isinstance(result.is_under_quoted, bool)

    def test_estimated_fair_quota_positive(self, engine, baseline_input):
        result = engine.assess(baseline_input)
        assert result.estimated_fair_quota_usd > 0

    def test_fairness_signal_string(self, engine, baseline_input):
        result = engine.assess(baseline_input)
        assert isinstance(result.fairness_signal, str)

    def test_is_over_quoted_logic(self, engine):
        # Force over_quoted: peer_quota_variance_pct > 15, composite < 50
        inp = make_input(
            peer_quota_variance_pct=30,
            previous_year_attainment_pct=30,
            quota_increase_yoy_pct=5,
            team_avg_attainment_pct=40,
            competitive_intensity_score=90,
            industry_growth_rate_pct=-20,
            annual_quota_usd=900_000,
            territory_market_potential_usd=1_000_000,
            product_maturity_score=0,
            years_experience=0,
            ramp_adjustment_applied=0,
            tenure_months=3,
            team_avg_quota_usd=1_000_000,
            manager_override_pct=30,
            account_count=1,
        )
        result = engine.assess(inp)
        if result.bias_direction == BiasDirection.OVER_QUOTED and result.fairness_composite < 50:
            assert result.is_over_quoted is True
        else:
            assert result.is_over_quoted is False

    def test_is_under_quoted_logic(self, engine):
        inp = make_input(
            peer_quota_variance_pct=-30,
            previous_year_attainment_pct=30,
            quota_increase_yoy_pct=5,
            team_avg_attainment_pct=40,
            competitive_intensity_score=90,
            industry_growth_rate_pct=-20,
            annual_quota_usd=900_000,
            territory_market_potential_usd=1_000_000,
            product_maturity_score=0,
            years_experience=0,
            ramp_adjustment_applied=0,
            tenure_months=3,
            team_avg_quota_usd=1_000_000,
            manager_override_pct=30,
            account_count=1,
        )
        result = engine.assess(inp)
        if result.bias_direction == BiasDirection.UNDER_QUOTED and result.fairness_composite < 50:
            assert result.is_under_quoted is True
        else:
            assert result.is_under_quoted is False

    def test_result_stored_by_rep_id(self, engine):
        inp = make_input(rep_id="STORED_REP")
        engine.assess(inp)
        assert engine.get("STORED_REP") is not None

    def test_repeated_assess_overwrites(self, engine):
        inp1 = make_input(rep_id="R1", annual_quota_usd=500_000, territory_market_potential_usd=2_000_000)
        inp2 = make_input(rep_id="R1", annual_quota_usd=1_000_000, territory_market_potential_usd=4_000_000)
        r1 = engine.assess(inp1)
        r2 = engine.assess(inp2)
        stored = engine.get("R1")
        assert stored.market_alignment_score == r2.market_alignment_score

    def test_very_fair_scenario(self, engine):
        inp = make_input(
            annual_quota_usd=300_000,
            territory_market_potential_usd=1_000_000,
            years_experience=10,
            ramp_adjustment_applied=0,
            tenure_months=24,
            previous_year_attainment_pct=95,
            quota_increase_yoy_pct=5,
            industry_growth_rate_pct=20,
            competitive_intensity_score=20,
            product_maturity_score=100,
            peer_quota_variance_pct=3,
            team_avg_quota_usd=300_000,
            manager_override_pct=0,
            team_avg_attainment_pct=90,
            account_count=10_000,
            avg_deal_size_usd=1_000,
            territory_adjusted_last_year=0,
        )
        result = engine.assess(inp)
        assert result.fairness_rating == FairnessRating.VERY_FAIR

    def test_unfair_scenario(self, engine):
        inp = make_input(
            annual_quota_usd=800_000,
            territory_market_potential_usd=1_000_000,
            years_experience=0.5,
            ramp_adjustment_applied=0,
            tenure_months=2,
            previous_year_attainment_pct=30,
            quota_increase_yoy_pct=40,
            industry_growth_rate_pct=-20,
            competitive_intensity_score=95,
            product_maturity_score=0,
            peer_quota_variance_pct=35,
            team_avg_quota_usd=500_000,
            manager_override_pct=30,
            team_avg_attainment_pct=40,
            account_count=2,
            avg_deal_size_usd=50_000,
            territory_adjusted_last_year=1,
        )
        result = engine.assess(inp)
        assert result.fairness_rating == FairnessRating.UNFAIR

    def test_not_both_over_and_under_quoted(self, engine, baseline_input):
        result = engine.assess(baseline_input)
        assert not (result.is_over_quoted and result.is_under_quoted)


# ---------------------------------------------------------------------------
# 16. is_over_quoted / is_under_quoted conditions
# ---------------------------------------------------------------------------

class TestOverUnderQuotedConditions:
    def test_over_quoted_requires_composite_below_50(self, engine):
        # balanced bias, high composite => not over_quoted
        inp = make_input(peer_quota_variance_pct=0, previous_year_attainment_pct=90,
                         quota_increase_yoy_pct=5)
        result = engine.assess(inp)
        assert result.is_over_quoted is False

    def test_under_quoted_requires_composite_below_50(self, engine):
        inp = make_input(peer_quota_variance_pct=0, previous_year_attainment_pct=90,
                         quota_increase_yoy_pct=5)
        result = engine.assess(inp)
        assert result.is_under_quoted is False

    def test_over_quoted_false_when_balanced_bias(self, engine):
        inp = make_input(peer_quota_variance_pct=0, previous_year_attainment_pct=90,
                         quota_increase_yoy_pct=5)
        result = engine.assess(inp)
        if result.bias_direction == BiasDirection.BALANCED:
            assert result.is_over_quoted is False

    def test_under_quoted_false_when_balanced_bias(self, engine):
        inp = make_input(peer_quota_variance_pct=0, previous_year_attainment_pct=90,
                         quota_increase_yoy_pct=5)
        result = engine.assess(inp)
        if result.bias_direction == BiasDirection.BALANCED:
            assert result.is_under_quoted is False


# ---------------------------------------------------------------------------
# 17. assess_batch()
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_returns_list(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert isinstance(results, list)
        assert len(results) == 5

    def test_sorted_descending_by_composite(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        composites = [r.fairness_composite for r in results]
        assert composites == sorted(composites, reverse=True)

    def test_batch_empty_list(self, engine):
        results = engine.assess_batch([])
        assert results == []

    def test_batch_stores_all_results(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(3)]
        engine.assess_batch(inputs)
        for i in range(3):
            assert engine.get(f"R{i}") is not None

    def test_batch_single_item(self, engine):
        results = engine.assess_batch([make_input(rep_id="SOLO")])
        assert len(results) == 1
        assert results[0].rep_id == "SOLO"

    def test_batch_all_results_are_result_type(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(4)]
        results = engine.assess_batch(inputs)
        for r in results:
            assert isinstance(r, QuotaFairnessResult)

    def test_batch_different_composites_sorted(self, engine):
        # Create inputs with varying quality to get different composites
        inputs = [
            make_input(rep_id="HIGH", annual_quota_usd=300_000, territory_market_potential_usd=1_000_000,
                       years_experience=10, previous_year_attainment_pct=95,
                       team_avg_attainment_pct=90, product_maturity_score=100,
                       peer_quota_variance_pct=0, quota_increase_yoy_pct=5,
                       competitive_intensity_score=20, industry_growth_rate_pct=20),
            make_input(rep_id="LOW", annual_quota_usd=800_000, territory_market_potential_usd=1_000_000,
                       years_experience=0, previous_year_attainment_pct=30,
                       team_avg_attainment_pct=40, product_maturity_score=0,
                       peer_quota_variance_pct=40, quota_increase_yoy_pct=40,
                       competitive_intensity_score=90, industry_growth_rate_pct=-20),
        ]
        results = engine.assess_batch(inputs)
        assert results[0].fairness_composite >= results[1].fairness_composite


# ---------------------------------------------------------------------------
# 18. Engine get / all_reps / reset
# ---------------------------------------------------------------------------

class TestEngineGetAllRepsReset:
    def test_get_nonexistent_returns_none(self, engine):
        assert engine.get("NONE") is None

    def test_get_after_assess(self, engine):
        inp = make_input(rep_id="G1")
        engine.assess(inp)
        assert engine.get("G1") is not None

    def test_all_reps_empty(self, engine):
        assert engine.all_reps() == []

    def test_all_reps_sorted_descending(self, engine):
        for i in range(3):
            engine.assess(make_input(rep_id=f"R{i}"))
        reps = engine.all_reps()
        composites = [r.fairness_composite for r in reps]
        assert composites == sorted(composites, reverse=True)

    def test_reset_clears_results(self, engine):
        engine.assess(make_input(rep_id="R1"))
        engine.reset()
        assert engine.get("R1") is None
        assert engine.all_reps() == []

    def test_reset_allows_fresh_assess(self, engine):
        engine.assess(make_input(rep_id="R1"))
        engine.reset()
        engine.assess(make_input(rep_id="R2"))
        assert engine.get("R2") is not None
        assert engine.get("R1") is None


# ---------------------------------------------------------------------------
# 19. Engine over/under_quoted_reps / by_rating / by_risk
# ---------------------------------------------------------------------------

class TestEngineFilterMethods:
    def test_over_quoted_reps_returns_list(self, engine):
        engine.assess(make_input(rep_id="R1"))
        result = engine.over_quoted_reps()
        assert isinstance(result, list)

    def test_under_quoted_reps_returns_list(self, engine):
        engine.assess(make_input(rep_id="R1"))
        result = engine.under_quoted_reps()
        assert isinstance(result, list)

    def test_by_rating_returns_matching(self, engine):
        engine.assess(make_input(rep_id="R1"))
        for rating in FairnessRating:
            reps = engine.by_rating(rating)
            assert all(r.fairness_rating == rating for r in reps)

    def test_by_risk_returns_matching(self, engine):
        engine.assess(make_input(rep_id="R1"))
        for risk in FairnessRisk:
            reps = engine.by_risk(risk)
            assert all(r.fairness_risk == risk for r in reps)

    def test_over_and_under_reps_disjoint(self, engine):
        for i in range(5):
            engine.assess(make_input(rep_id=f"R{i}"))
        over_ids = {r.rep_id for r in engine.over_quoted_reps()}
        under_ids = {r.rep_id for r in engine.under_quoted_reps()}
        assert over_ids.isdisjoint(under_ids)

    def test_by_rating_all_categories_cover_all_reps(self, engine):
        for i in range(5):
            engine.assess(make_input(rep_id=f"R{i}"))
        all_by_rating = []
        for rating in FairnessRating:
            all_by_rating.extend(engine.by_rating(rating))
        assert len(all_by_rating) == len(engine.all_reps())


# ---------------------------------------------------------------------------
# 20. avg_fairness_composite
# ---------------------------------------------------------------------------

class TestAvgFairnessComposite:
    def test_empty_returns_0(self, engine):
        assert engine.avg_fairness_composite() == 0.0

    def test_single_rep(self, engine):
        inp = make_input(rep_id="R1")
        r = engine.assess(inp)
        assert engine.avg_fairness_composite() == r.fairness_composite

    def test_multiple_reps_average(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(3)]
        results = [engine.assess(inp) for inp in inputs]
        expected = round(sum(r.fairness_composite for r in results) / 3, 1)
        assert engine.avg_fairness_composite() == expected

    def test_returns_float(self, engine):
        engine.assess(make_input(rep_id="R1"))
        assert isinstance(engine.avg_fairness_composite(), float)


# ---------------------------------------------------------------------------
# 21. summary()
# ---------------------------------------------------------------------------

class TestSummary:
    def test_summary_returns_dict(self, engine):
        engine.assess(make_input())
        assert isinstance(engine.summary(), dict)

    def test_summary_has_13_keys(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert len(s) == 13

    def test_summary_exact_keys(self, engine):
        engine.assess(make_input())
        expected = {
            "total", "fairness_counts", "risk_counts", "bias_counts", "action_counts",
            "avg_fairness_composite", "over_quoted_count", "under_quoted_count",
            "avg_market_alignment_score", "avg_experience_alignment_score",
            "avg_peer_equity_score", "avg_attainment_sustainability_score",
            "total_quota_adjustment_opportunity_usd",
        }
        assert set(engine.summary().keys()) == expected

    def test_summary_total_matches_assessed_count(self, engine):
        for i in range(4):
            engine.assess(make_input(rep_id=f"R{i}"))
        assert engine.summary()["total"] == 4

    def test_summary_empty_engine(self, engine):
        # summary() with no results — check no zero-division errors
        s = engine.summary()
        assert s["total"] == 0
        assert s["avg_fairness_composite"] == 0.0
        assert s["over_quoted_count"] == 0
        assert s["under_quoted_count"] == 0

    def test_summary_fairness_counts_is_dict(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert isinstance(s["fairness_counts"], dict)

    def test_summary_risk_counts_is_dict(self, engine):
        engine.assess(make_input())
        assert isinstance(engine.summary()["risk_counts"], dict)

    def test_summary_bias_counts_is_dict(self, engine):
        engine.assess(make_input())
        assert isinstance(engine.summary()["bias_counts"], dict)

    def test_summary_action_counts_is_dict(self, engine):
        engine.assess(make_input())
        assert isinstance(engine.summary()["action_counts"], dict)

    def test_summary_fairness_counts_sum_equals_total(self, engine):
        for i in range(5):
            engine.assess(make_input(rep_id=f"R{i}"))
        s = engine.summary()
        assert sum(s["fairness_counts"].values()) == s["total"]

    def test_summary_risk_counts_sum_equals_total(self, engine):
        for i in range(5):
            engine.assess(make_input(rep_id=f"R{i}"))
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_bias_counts_sum_equals_total(self, engine):
        for i in range(5):
            engine.assess(make_input(rep_id=f"R{i}"))
        s = engine.summary()
        assert sum(s["bias_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_equals_total(self, engine):
        for i in range(5):
            engine.assess(make_input(rep_id=f"R{i}"))
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_avg_scores_are_floats(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        for key in ["avg_market_alignment_score", "avg_experience_alignment_score",
                    "avg_peer_equity_score", "avg_attainment_sustainability_score"]:
            assert isinstance(s[key], float)

    def test_summary_avg_composite_is_float(self, engine):
        engine.assess(make_input())
        assert isinstance(engine.summary()["avg_fairness_composite"], float)

    def test_summary_over_quoted_count_non_negative(self, engine):
        for i in range(5):
            engine.assess(make_input(rep_id=f"R{i}"))
        assert engine.summary()["over_quoted_count"] >= 0

    def test_summary_under_quoted_count_non_negative(self, engine):
        for i in range(5):
            engine.assess(make_input(rep_id=f"R{i}"))
        assert engine.summary()["under_quoted_count"] >= 0

    def test_summary_total_quota_adjustment_positive(self, engine):
        engine.assess(make_input())
        assert engine.summary()["total_quota_adjustment_opportunity_usd"] >= 0

    def test_summary_after_reset_empty(self, engine):
        engine.assess(make_input())
        engine.reset()
        s = engine.summary()
        assert s["total"] == 0
        assert s["fairness_counts"] == {}
        assert s["risk_counts"] == {}

    def test_summary_single_rep_avg_equals_rep_score(self, engine):
        inp = make_input()
        r = engine.assess(inp)
        s = engine.summary()
        assert s["avg_market_alignment_score"] == r.market_alignment_score

    def test_summary_fairness_counts_keys_are_rating_values(self, engine):
        for i in range(10):
            engine.assess(make_input(rep_id=f"R{i}"))
        s = engine.summary()
        valid_values = {fr.value for fr in FairnessRating}
        for key in s["fairness_counts"]:
            assert key in valid_values

    def test_summary_risk_counts_keys_are_risk_values(self, engine):
        for i in range(10):
            engine.assess(make_input(rep_id=f"R{i}"))
        s = engine.summary()
        valid_values = {fr.value for fr in FairnessRisk}
        for key in s["risk_counts"]:
            assert key in valid_values

    def test_summary_bias_counts_keys_are_bias_values(self, engine):
        for i in range(10):
            engine.assess(make_input(rep_id=f"R{i}"))
        s = engine.summary()
        valid_values = {b.value for b in BiasDirection}
        for key in s["bias_counts"]:
            assert key in valid_values

    def test_summary_action_counts_keys_are_action_values(self, engine):
        for i in range(10):
            engine.assess(make_input(rep_id=f"R{i}"))
        s = engine.summary()
        valid_values = {a.value for a in QuotaAction}
        for key in s["action_counts"]:
            assert key in valid_values


# ---------------------------------------------------------------------------
# 22. to_dict() full round-trip
# ---------------------------------------------------------------------------

class TestToDictRoundTrip:
    def test_to_dict_rep_id_matches(self, engine):
        inp = make_input(rep_id="DICT_TEST")
        r = engine.assess(inp)
        assert r.to_dict()["rep_id"] == "DICT_TEST"

    def test_to_dict_boolean_types(self, engine, baseline_input):
        r = engine.assess(baseline_input)
        d = r.to_dict()
        assert isinstance(d["is_over_quoted"], bool)
        assert isinstance(d["is_under_quoted"], bool)

    def test_to_dict_enum_strings_not_enum_objects(self, engine, baseline_input):
        r = engine.assess(baseline_input)
        d = r.to_dict()
        for key in ["fairness_rating", "fairness_risk", "bias_direction", "quota_action"]:
            assert isinstance(d[key], str)
            assert not isinstance(d[key], type(FairnessRating.FAIR))

    def test_to_dict_numeric_values_are_numbers(self, engine, baseline_input):
        r = engine.assess(baseline_input)
        d = r.to_dict()
        for key in ["market_alignment_score", "experience_alignment_score",
                    "peer_equity_score", "attainment_sustainability_score",
                    "fairness_composite", "estimated_fair_quota_usd"]:
            assert isinstance(d[key], (int, float))

    def test_to_dict_fairness_signal_is_str(self, engine, baseline_input):
        r = engine.assess(baseline_input)
        assert isinstance(r.to_dict()["fairness_signal"], str)


# ---------------------------------------------------------------------------
# 23. Edge cases and boundary conditions
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_zero_annual_quota(self, engine):
        inp = make_input(annual_quota_usd=0, territory_market_potential_usd=1_000_000)
        result = engine.assess(inp)
        assert isinstance(result, QuotaFairnessResult)

    def test_very_large_quota(self, engine):
        inp = make_input(annual_quota_usd=100_000_000, territory_market_potential_usd=1_000_000)
        result = engine.assess(inp)
        assert isinstance(result, QuotaFairnessResult)

    def test_zero_tenure(self, engine):
        inp = make_input(tenure_months=0, ramp_adjustment_applied=0)
        result = engine.assess(inp)
        assert isinstance(result, QuotaFairnessResult)

    def test_very_long_tenure(self, engine):
        inp = make_input(tenure_months=240)
        result = engine.assess(inp)
        assert isinstance(result, QuotaFairnessResult)

    def test_attainment_above_100(self, engine):
        inp = make_input(previous_year_attainment_pct=150)
        result = engine.assess(inp)
        assert isinstance(result, QuotaFairnessResult)

    def test_zero_attainment(self, engine):
        inp = make_input(previous_year_attainment_pct=0)
        result = engine.assess(inp)
        assert isinstance(result, QuotaFairnessResult)

    def test_zero_account_count(self, engine):
        inp = make_input(account_count=0)
        result = engine.assess(inp)
        assert isinstance(result, QuotaFairnessResult)

    def test_zero_avg_deal_size(self, engine):
        inp = make_input(avg_deal_size_usd=0)
        result = engine.assess(inp)
        assert isinstance(result, QuotaFairnessResult)

    def test_negative_industry_growth(self, engine):
        inp = make_input(industry_growth_rate_pct=-50)
        result = engine.assess(inp)
        assert isinstance(result, QuotaFairnessResult)

    def test_very_high_competitive_intensity(self, engine):
        inp = make_input(competitive_intensity_score=100)
        result = engine.assess(inp)
        assert isinstance(result, QuotaFairnessResult)

    def test_zero_competitive_intensity(self, engine):
        inp = make_input(competitive_intensity_score=0)
        result = engine.assess(inp)
        assert isinstance(result, QuotaFairnessResult)

    def test_extreme_peer_variance_positive(self, engine):
        inp = make_input(peer_quota_variance_pct=200)
        result = engine.assess(inp)
        assert isinstance(result, QuotaFairnessResult)

    def test_extreme_peer_variance_negative(self, engine):
        inp = make_input(peer_quota_variance_pct=-200)
        result = engine.assess(inp)
        assert isinstance(result, QuotaFairnessResult)

    def test_very_high_yoy_increase(self, engine):
        inp = make_input(quota_increase_yoy_pct=100)
        result = engine.assess(inp)
        assert isinstance(result, QuotaFairnessResult)

    def test_no_experience(self, engine):
        inp = make_input(years_experience=0)
        result = engine.assess(inp)
        assert isinstance(result, QuotaFairnessResult)

    def test_product_maturity_zero(self, engine):
        inp = make_input(product_maturity_score=0)
        result = engine.assess(inp)
        assert isinstance(result, QuotaFairnessResult)

    def test_product_maturity_100(self, engine):
        inp = make_input(product_maturity_score=100)
        result = engine.assess(inp)
        assert isinstance(result, QuotaFairnessResult)

    def test_multiple_reps_different_regions(self, engine):
        for region in ["North", "South", "East", "West"]:
            inp = make_input(rep_id=region, region=region)
            engine.assess(inp)
        assert len(engine.all_reps()) == 4

    def test_ramp_adjustment_applied_1(self, engine):
        inp = make_input(ramp_adjustment_applied=1, tenure_months=3)
        result = engine.assess(inp)
        assert isinstance(result, QuotaFairnessResult)

    def test_territory_adjusted_1(self, engine):
        inp = make_input(territory_adjusted_last_year=1)
        result = engine.assess(inp)
        assert isinstance(result, QuotaFairnessResult)

    def test_manager_override_zero(self, engine):
        inp = make_input(manager_override_pct=0.0)
        result = engine.assess(inp)
        assert isinstance(result, QuotaFairnessResult)

    def test_large_manager_override(self, engine):
        inp = make_input(manager_override_pct=50.0)
        result = engine.assess(inp)
        assert isinstance(result, QuotaFairnessResult)


# ---------------------------------------------------------------------------
# 24. Composite and rating/risk consistency
# ---------------------------------------------------------------------------

class TestCompositeConsistency:
    def test_high_composite_gives_low_risk(self, engine):
        # A very fair scenario should have low risk
        inp = make_input(
            annual_quota_usd=300_000, territory_market_potential_usd=1_000_000,
            years_experience=10, ramp_adjustment_applied=0, tenure_months=24,
            previous_year_attainment_pct=95, quota_increase_yoy_pct=5,
            industry_growth_rate_pct=20, competitive_intensity_score=20,
            product_maturity_score=100, peer_quota_variance_pct=3,
            team_avg_quota_usd=300_000, manager_override_pct=0,
            team_avg_attainment_pct=90, account_count=10_000,
            avg_deal_size_usd=1_000, territory_adjusted_last_year=0,
        )
        result = engine.assess(inp)
        if result.fairness_composite >= 60:
            assert result.fairness_risk == FairnessRisk.LOW

    def test_very_fair_implies_low_risk(self, engine):
        inp = make_input(
            annual_quota_usd=300_000, territory_market_potential_usd=1_000_000,
            years_experience=10, ramp_adjustment_applied=0, tenure_months=24,
            previous_year_attainment_pct=95, quota_increase_yoy_pct=5,
            industry_growth_rate_pct=20, competitive_intensity_score=20,
            product_maturity_score=100, peer_quota_variance_pct=3,
            team_avg_quota_usd=300_000, manager_override_pct=0,
            team_avg_attainment_pct=90, account_count=10_000,
            avg_deal_size_usd=1_000, territory_adjusted_last_year=0,
        )
        result = engine.assess(inp)
        if result.fairness_rating == FairnessRating.VERY_FAIR:
            assert result.fairness_risk == FairnessRisk.LOW

    def test_unfair_implies_high_or_critical_risk(self, engine):
        inp = make_input(
            annual_quota_usd=800_000, territory_market_potential_usd=1_000_000,
            years_experience=0.5, ramp_adjustment_applied=0, tenure_months=2,
            previous_year_attainment_pct=30, quota_increase_yoy_pct=40,
            industry_growth_rate_pct=-20, competitive_intensity_score=95,
            product_maturity_score=0, peer_quota_variance_pct=35,
            team_avg_quota_usd=500_000, manager_override_pct=30,
            team_avg_attainment_pct=40, account_count=2,
            avg_deal_size_usd=50_000, territory_adjusted_last_year=1,
        )
        result = engine.assess(inp)
        if result.fairness_rating == FairnessRating.UNFAIR:
            assert result.fairness_risk in (FairnessRisk.HIGH, FairnessRisk.CRITICAL)

    def test_composite_in_0_100_range(self, engine, baseline_input):
        result = engine.assess(baseline_input)
        assert 0.0 <= result.fairness_composite <= 100.0

    def test_maintain_action_for_low_risk(self, engine):
        # Low risk => maintain
        inp = make_input(
            annual_quota_usd=300_000, territory_market_potential_usd=1_000_000,
            years_experience=10, tenure_months=24, previous_year_attainment_pct=95,
            quota_increase_yoy_pct=5, industry_growth_rate_pct=20,
            competitive_intensity_score=20, product_maturity_score=100,
            peer_quota_variance_pct=3, team_avg_quota_usd=300_000,
            manager_override_pct=0, team_avg_attainment_pct=90,
            account_count=10_000, avg_deal_size_usd=1_000,
            territory_adjusted_last_year=0,
        )
        result = engine.assess(inp)
        if result.fairness_risk == FairnessRisk.LOW:
            assert result.quota_action == QuotaAction.MAINTAIN


# ---------------------------------------------------------------------------
# 25. Multiple engines isolation
# ---------------------------------------------------------------------------

class TestMultipleEngines:
    def test_engines_are_independent(self):
        e1 = QuotaFairnessEngine()
        e2 = QuotaFairnessEngine()
        e1.assess(make_input(rep_id="R1"))
        assert e2.get("R1") is None

    def test_reset_one_does_not_affect_other(self):
        e1 = QuotaFairnessEngine()
        e2 = QuotaFairnessEngine()
        e1.assess(make_input(rep_id="R1"))
        e2.assess(make_input(rep_id="R1"))
        e1.reset()
        assert e1.get("R1") is None
        assert e2.get("R1") is not None


# ---------------------------------------------------------------------------
# 26. Parameterized tests for quota % band boundaries
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("quota_pct,expected_pts", [
    (20, 40),   # exact lower boundary of ideal range
    (30, 40),   # mid ideal
    (40, 40),   # exact upper boundary of ideal range
    (17, 28),   # 15-20 band
    (45, 28),   # 40-50 band
    (12, 16),   # 10-15 band
    (55, 16),   # 50-65 band
    (5, 4),     # below 10
    (80, 4),    # above 65
])
def test_market_alignment_quota_pct_bands(quota_pct, expected_pts):
    inp = make_input(
        annual_quota_usd=quota_pct * 10_000,
        territory_market_potential_usd=1_000_000,
        industry_growth_rate_pct=0,
        competitive_intensity_score=0,
        product_maturity_score=0,
    )
    score = _market_alignment_score(inp)
    assert score == expected_pts + 10 + 20 + 0  # growth=10, comp<40=20, maturity=0


@pytest.mark.parametrize("composite,expected_rating", [
    (100.0, FairnessRating.VERY_FAIR),
    (75.0, FairnessRating.VERY_FAIR),
    (74.9, FairnessRating.FAIR),
    (55.0, FairnessRating.FAIR),
    (54.9, FairnessRating.QUESTIONABLE),
    (35.0, FairnessRating.QUESTIONABLE),
    (34.9, FairnessRating.UNFAIR),
    (0.0, FairnessRating.UNFAIR),
])
def test_fairness_rating_boundaries(composite, expected_rating):
    assert _fairness_rating(composite) == expected_rating


@pytest.mark.parametrize("composite,expected_risk", [
    (0.0, FairnessRisk.CRITICAL),
    (24.9, FairnessRisk.CRITICAL),
    (25.0, FairnessRisk.HIGH),
    (39.9, FairnessRisk.HIGH),
    (40.0, FairnessRisk.MODERATE),
    (59.9, FairnessRisk.MODERATE),
    (60.0, FairnessRisk.LOW),
    (100.0, FairnessRisk.LOW),
])
def test_fairness_risk_boundaries(composite, expected_risk):
    assert _fairness_risk(composite) == expected_risk


@pytest.mark.parametrize("risk,bias,expected_action", [
    (FairnessRisk.CRITICAL, BiasDirection.OVER_QUOTED, QuotaAction.REDUCE_QUOTA),
    (FairnessRisk.CRITICAL, BiasDirection.UNDER_QUOTED, QuotaAction.INCREASE_QUOTA),
    (FairnessRisk.CRITICAL, BiasDirection.BALANCED, QuotaAction.RECALIBRATE_TERRITORY),
    (FairnessRisk.HIGH, BiasDirection.OVER_QUOTED, QuotaAction.REDUCE_QUOTA),
    (FairnessRisk.HIGH, BiasDirection.UNDER_QUOTED, QuotaAction.INCREASE_QUOTA),
    (FairnessRisk.HIGH, BiasDirection.BALANCED, QuotaAction.RECALIBRATE_TERRITORY),
    (FairnessRisk.MODERATE, BiasDirection.OVER_QUOTED, QuotaAction.RECALIBRATE_TERRITORY),
    (FairnessRisk.MODERATE, BiasDirection.UNDER_QUOTED, QuotaAction.RECALIBRATE_TERRITORY),
    (FairnessRisk.MODERATE, BiasDirection.BALANCED, QuotaAction.RECALIBRATE_TERRITORY),
    (FairnessRisk.LOW, BiasDirection.OVER_QUOTED, QuotaAction.MAINTAIN),
    (FairnessRisk.LOW, BiasDirection.UNDER_QUOTED, QuotaAction.MAINTAIN),
    (FairnessRisk.LOW, BiasDirection.BALANCED, QuotaAction.MAINTAIN),
])
def test_quota_action_all_combinations(risk, bias, expected_action):
    assert _quota_action(risk, bias) == expected_action


# ---------------------------------------------------------------------------
# 27. Workflow tests (assess → summary consistency)
# ---------------------------------------------------------------------------

class TestWorkflow:
    def test_fresh_engine_summary_total_zero(self, engine):
        assert engine.summary()["total"] == 0

    def test_assess_then_summary(self, engine):
        engine.assess(make_input(rep_id="W1"))
        s = engine.summary()
        assert s["total"] == 1
        assert s["avg_fairness_composite"] > 0

    def test_batch_then_summary(self, engine):
        inputs = [make_input(rep_id=f"B{i}") for i in range(6)]
        engine.assess_batch(inputs)
        s = engine.summary()
        assert s["total"] == 6

    def test_assess_batch_then_all_reps(self, engine):
        inputs = [make_input(rep_id=f"X{i}") for i in range(4)]
        engine.assess_batch(inputs)
        reps = engine.all_reps()
        assert len(reps) == 4

    def test_reset_then_assess_again(self, engine):
        engine.assess(make_input(rep_id="OLD"))
        engine.reset()
        engine.assess(make_input(rep_id="NEW"))
        assert engine.summary()["total"] == 1
        assert engine.get("NEW") is not None
        assert engine.get("OLD") is None

    def test_assess_multiple_unique_reps(self, engine):
        for i in range(10):
            engine.assess(make_input(rep_id=f"U{i}"))
        assert len(engine.all_reps()) == 10

    def test_summary_avg_market_is_avg_of_individual(self, engine):
        inputs = [make_input(rep_id=f"M{i}") for i in range(3)]
        results = [engine.assess(inp) for inp in inputs]
        expected = round(sum(r.market_alignment_score for r in results) / 3, 1)
        assert engine.summary()["avg_market_alignment_score"] == expected
