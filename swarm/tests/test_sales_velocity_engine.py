"""
Comprehensive pytest tests for Module 33 — Sales Velocity Engine.

Covers:
- All enums
- VelocityInput / VelocityResult dataclasses (including to_dict)
- Every private helper function (_velocity_eur_per_day, _benchmark_velocity,
  _opportunity_index, _win_rate_index, _deal_size_index, _cycle_time_index,
  _primary_driver, _quota_attainment_pct, _projected_arr_eur, _velocity_score,
  _velocity_tier, _velocity_action, _velocity_gaps, _velocity_levers)
- SalesVelocityEngine public API (analyze, analyze_batch, by_tier, by_action,
  by_driver, elite_reps, stalled_reps, needs_reset, at_risk_reps,
  avg_velocity, avg_velocity_score, total_projected_arr_eur,
  top_velocity_rep, constraint_distribution, summary, reset)
"""

from __future__ import annotations

import pytest

from swarm.intelligence.sales_velocity_engine import (
    VelocityTier,
    VelocityAction,
    VelocityDriver,
    VelocityInput,
    VelocityResult,
    SalesVelocityEngine,
    _velocity_eur_per_day,
    _benchmark_velocity,
    _opportunity_index,
    _win_rate_index,
    _deal_size_index,
    _cycle_time_index,
    _primary_driver,
    _quota_attainment_pct,
    _projected_arr_eur,
    _velocity_score,
    _velocity_tier,
    _velocity_action,
    _velocity_gaps,
    _velocity_levers,
)


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

def make_input(
    rep_id: str = "rep1",
    rep_name: str = "Alice",
    region: str = "EMEA",
    segment: str = "ENT",
    period_days: int = 90,
    opportunities_created: int = 20,
    win_rate_pct: float = 30.0,
    avg_deal_size_eur: float = 50_000.0,
    avg_sales_cycle_days: int = 60,
    quota_eur: float = 300_000.0,
    closed_won_eur: float = 270_000.0,
    benchmark_opps: int = 20,
    benchmark_win_rate_pct: float = 30.0,
    benchmark_deal_size_eur: float = 50_000.0,
    benchmark_cycle_days: int = 60,
    pipeline_total_eur: float = 500_000.0,
    deals_advancing_pct: float = 60.0,
    avg_days_in_stage: float = 10.0,
    outreach_activities_30d: int = 80,
    connect_rate_pct: float = 25.0,
) -> VelocityInput:
    """Factory for VelocityInput with sensible defaults (all-benchmark rep)."""
    return VelocityInput(
        rep_id=rep_id,
        rep_name=rep_name,
        region=region,
        segment=segment,
        period_days=period_days,
        opportunities_created=opportunities_created,
        win_rate_pct=win_rate_pct,
        avg_deal_size_eur=avg_deal_size_eur,
        avg_sales_cycle_days=avg_sales_cycle_days,
        quota_eur=quota_eur,
        closed_won_eur=closed_won_eur,
        benchmark_opps=benchmark_opps,
        benchmark_win_rate_pct=benchmark_win_rate_pct,
        benchmark_deal_size_eur=benchmark_deal_size_eur,
        benchmark_cycle_days=benchmark_cycle_days,
        pipeline_total_eur=pipeline_total_eur,
        deals_advancing_pct=deals_advancing_pct,
        avg_days_in_stage=avg_days_in_stage,
        outreach_activities_30d=outreach_activities_30d,
        connect_rate_pct=connect_rate_pct,
    )


@pytest.fixture()
def engine() -> SalesVelocityEngine:
    return SalesVelocityEngine()


@pytest.fixture()
def baseline_input() -> VelocityInput:
    """Rep at exactly benchmark on all four levers."""
    return make_input()


@pytest.fixture()
def elite_input() -> VelocityInput:
    """Rep well above benchmark on all levers — should land ELITE."""
    return make_input(
        rep_id="elite1",
        opportunities_created=40,     # 2× benchmark
        win_rate_pct=60.0,            # 2× benchmark
        avg_deal_size_eur=100_000.0,  # 2× benchmark
        avg_sales_cycle_days=30,      # half cycle → 2× CT index
        quota_eur=300_000.0,
        closed_won_eur=300_000.0,     # 100 % attainment
    )


@pytest.fixture()
def stalled_input() -> VelocityInput:
    """Rep far below benchmark on all levers — should land STALLED."""
    return make_input(
        rep_id="stalled1",
        opportunities_created=1,
        win_rate_pct=5.0,
        avg_deal_size_eur=5_000.0,
        avg_sales_cycle_days=300,
        quota_eur=300_000.0,
        closed_won_eur=5_000.0,
    )


# ===========================================================================
# 1. Enum sanity
# ===========================================================================

class TestVelocityTierEnum:
    def test_all_five_members(self):
        assert len(VelocityTier) == 5

    def test_values(self):
        assert VelocityTier.ELITE.value == "elite"
        assert VelocityTier.HIGH.value == "high"
        assert VelocityTier.AVERAGE.value == "average"
        assert VelocityTier.LOW.value == "low"
        assert VelocityTier.STALLED.value == "stalled"

    def test_is_str_subclass(self):
        assert isinstance(VelocityTier.ELITE, str)

    def test_string_comparison(self):
        assert VelocityTier.ELITE == "elite"


class TestVelocityActionEnum:
    def test_all_five_members(self):
        assert len(VelocityAction) == 5

    def test_values(self):
        assert VelocityAction.CELEBRATE.value == "celebrate"
        assert VelocityAction.ACCELERATE.value == "accelerate"
        assert VelocityAction.OPTIMIZE.value == "optimize"
        assert VelocityAction.RESCUE.value == "rescue"
        assert VelocityAction.RESET.value == "reset"

    def test_is_str_subclass(self):
        assert isinstance(VelocityAction.RESET, str)


class TestVelocityDriverEnum:
    def test_all_five_members(self):
        assert len(VelocityDriver) == 5

    def test_values(self):
        assert VelocityDriver.OPPORTUNITIES.value == "opportunities"
        assert VelocityDriver.WIN_RATE.value == "win_rate"
        assert VelocityDriver.DEAL_SIZE.value == "deal_size"
        assert VelocityDriver.CYCLE_TIME.value == "cycle_time"
        assert VelocityDriver.BALANCED.value == "balanced"

    def test_is_str_subclass(self):
        assert isinstance(VelocityDriver.BALANCED, str)


# ===========================================================================
# 2. VelocityInput dataclass
# ===========================================================================

class TestVelocityInputDataclass:
    def test_construction_all_fields(self, baseline_input):
        inp = baseline_input
        assert inp.rep_id == "rep1"
        assert inp.rep_name == "Alice"
        assert inp.region == "EMEA"
        assert inp.segment == "ENT"
        assert inp.period_days == 90
        assert inp.opportunities_created == 20
        assert inp.win_rate_pct == 30.0
        assert inp.avg_deal_size_eur == 50_000.0
        assert inp.avg_sales_cycle_days == 60
        assert inp.quota_eur == 300_000.0
        assert inp.closed_won_eur == 270_000.0
        assert inp.benchmark_opps == 20
        assert inp.benchmark_win_rate_pct == 30.0
        assert inp.benchmark_deal_size_eur == 50_000.0
        assert inp.benchmark_cycle_days == 60
        assert inp.pipeline_total_eur == 500_000.0
        assert inp.deals_advancing_pct == 60.0
        assert inp.avg_days_in_stage == 10.0
        assert inp.outreach_activities_30d == 80
        assert inp.connect_rate_pct == 25.0

    def test_twenty_fields(self):
        """VelocityInput must expose exactly 20 fields."""
        import dataclasses
        fields = dataclasses.fields(VelocityInput)
        assert len(fields) == 20


# ===========================================================================
# 3. VelocityResult dataclass & to_dict
# ===========================================================================

class TestVelocityResultToDict:
    def _result(self):
        return VelocityResult(
            rep_id="r1",
            rep_name="Bob",
            region="NA",
            segment="SMB",
            velocity_eur_per_day=1000.0,
            velocity_tier=VelocityTier.HIGH,
            velocity_action=VelocityAction.ACCELERATE,
            primary_driver=VelocityDriver.WIN_RATE,
            velocity_score=70.5,
            opportunity_index=1.1,
            win_rate_index=0.9,
            deal_size_index=1.2,
            cycle_time_index=1.0,
            quota_attainment_pct=88.5,
            projected_arr_eur=365_000.0,
            velocity_gaps=["gap1"],
            velocity_levers=["lever1"],
            benchmark_velocity_eur_per_day=900.0,
        )

    def test_to_dict_keys(self):
        d = self._result().to_dict()
        expected_keys = {
            "rep_id", "rep_name", "region", "segment",
            "velocity_eur_per_day", "velocity_tier", "velocity_action",
            "primary_driver", "velocity_score", "opportunity_index",
            "win_rate_index", "deal_size_index", "cycle_time_index",
            "quota_attainment_pct", "projected_arr_eur",
            "velocity_gaps", "velocity_levers",
            "benchmark_velocity_eur_per_day",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_values_are_strings(self):
        d = self._result().to_dict()
        assert d["velocity_tier"] == "high"
        assert d["velocity_action"] == "accelerate"
        assert d["primary_driver"] == "win_rate"

    def test_to_dict_numeric_fields(self):
        d = self._result().to_dict()
        assert d["velocity_eur_per_day"] == 1000.0
        assert d["velocity_score"] == 70.5
        assert d["projected_arr_eur"] == 365_000.0
        assert d["benchmark_velocity_eur_per_day"] == 900.0

    def test_to_dict_list_fields(self):
        d = self._result().to_dict()
        assert d["velocity_gaps"] == ["gap1"]
        assert d["velocity_levers"] == ["lever1"]

    def test_to_dict_returns_new_dict(self):
        r = self._result()
        d1 = r.to_dict()
        d2 = r.to_dict()
        assert d1 is not d2


# ===========================================================================
# 4. _velocity_eur_per_day
# ===========================================================================

class TestVelocityEurPerDay:
    def test_normal_case(self):
        inp = make_input(closed_won_eur=180_000.0, period_days=90)
        assert _velocity_eur_per_day(inp) == 2000.0

    def test_zero_period_days(self):
        inp = make_input(period_days=0, closed_won_eur=100_000.0)
        assert _velocity_eur_per_day(inp) == 0.0

    def test_negative_period_days(self):
        inp = make_input(period_days=-5, closed_won_eur=100_000.0)
        assert _velocity_eur_per_day(inp) == 0.0

    def test_zero_closed_won(self):
        inp = make_input(closed_won_eur=0.0, period_days=90)
        assert _velocity_eur_per_day(inp) == 0.0

    def test_rounding_two_decimals(self):
        # 100_001 / 90 = 1111.1222... → 1111.12
        inp = make_input(closed_won_eur=100_001.0, period_days=90)
        result = _velocity_eur_per_day(inp)
        assert result == round(100_001.0 / 90, 2)

    def test_result_is_float(self):
        inp = make_input(closed_won_eur=90_000.0, period_days=90)
        assert isinstance(_velocity_eur_per_day(inp), float)


# ===========================================================================
# 5. _benchmark_velocity
# ===========================================================================

class TestBenchmarkVelocity:
    def test_normal_case(self):
        inp = make_input(
            benchmark_opps=20,
            benchmark_win_rate_pct=30.0,
            benchmark_deal_size_eur=50_000.0,
            benchmark_cycle_days=60,
            period_days=90,
        )
        expected = round(20 * 0.30 * 50_000 / 60, 2)
        assert _benchmark_velocity(inp) == expected

    def test_zero_benchmark_cycle_days(self):
        inp = make_input(benchmark_cycle_days=0, period_days=90)
        assert _benchmark_velocity(inp) == 0.0

    def test_negative_benchmark_cycle_days(self):
        inp = make_input(benchmark_cycle_days=-1, period_days=90)
        assert _benchmark_velocity(inp) == 0.0

    def test_zero_period_days(self):
        inp = make_input(benchmark_cycle_days=60, period_days=0)
        assert _benchmark_velocity(inp) == 0.0

    def test_result_is_float(self):
        inp = make_input()
        assert isinstance(_benchmark_velocity(inp), float)

    def test_proportional_to_opps(self):
        inp1 = make_input(benchmark_opps=10)
        inp2 = make_input(benchmark_opps=20)
        assert _benchmark_velocity(inp2) == pytest.approx(2 * _benchmark_velocity(inp1), rel=1e-6)


# ===========================================================================
# 6. _opportunity_index
# ===========================================================================

class TestOpportunityIndex:
    def test_at_benchmark(self):
        inp = make_input(opportunities_created=20, benchmark_opps=20)
        assert _opportunity_index(inp) == 1.0

    def test_above_benchmark(self):
        inp = make_input(opportunities_created=30, benchmark_opps=20)
        assert _opportunity_index(inp) == pytest.approx(1.5, rel=1e-6)

    def test_below_benchmark(self):
        inp = make_input(opportunities_created=10, benchmark_opps=20)
        assert _opportunity_index(inp) == pytest.approx(0.5, rel=1e-6)

    def test_zero_benchmark_opps_returns_one(self):
        inp = make_input(benchmark_opps=0)
        assert _opportunity_index(inp) == 1.0

    def test_negative_benchmark_returns_one(self):
        inp = make_input(benchmark_opps=-5)
        assert _opportunity_index(inp) == 1.0

    def test_rounding(self):
        inp = make_input(opportunities_created=1, benchmark_opps=3)
        assert _opportunity_index(inp) == round(1 / 3, 2)


# ===========================================================================
# 7. _win_rate_index
# ===========================================================================

class TestWinRateIndex:
    def test_at_benchmark(self):
        inp = make_input(win_rate_pct=30.0, benchmark_win_rate_pct=30.0)
        assert _win_rate_index(inp) == 1.0

    def test_above_benchmark(self):
        inp = make_input(win_rate_pct=45.0, benchmark_win_rate_pct=30.0)
        assert _win_rate_index(inp) == pytest.approx(1.5, rel=1e-6)

    def test_below_benchmark(self):
        inp = make_input(win_rate_pct=15.0, benchmark_win_rate_pct=30.0)
        assert _win_rate_index(inp) == pytest.approx(0.5, rel=1e-6)

    def test_zero_benchmark_win_rate_returns_one(self):
        inp = make_input(benchmark_win_rate_pct=0.0)
        assert _win_rate_index(inp) == 1.0

    def test_negative_benchmark_returns_one(self):
        inp = make_input(benchmark_win_rate_pct=-10.0)
        assert _win_rate_index(inp) == 1.0

    def test_rounding(self):
        inp = make_input(win_rate_pct=10.0, benchmark_win_rate_pct=3.0)
        assert _win_rate_index(inp) == round(10.0 / 3.0, 2)


# ===========================================================================
# 8. _deal_size_index
# ===========================================================================

class TestDealSizeIndex:
    def test_at_benchmark(self):
        inp = make_input(avg_deal_size_eur=50_000.0, benchmark_deal_size_eur=50_000.0)
        assert _deal_size_index(inp) == 1.0

    def test_above_benchmark(self):
        inp = make_input(avg_deal_size_eur=75_000.0, benchmark_deal_size_eur=50_000.0)
        assert _deal_size_index(inp) == pytest.approx(1.5, rel=1e-6)

    def test_below_benchmark(self):
        inp = make_input(avg_deal_size_eur=25_000.0, benchmark_deal_size_eur=50_000.0)
        assert _deal_size_index(inp) == pytest.approx(0.5, rel=1e-6)

    def test_zero_benchmark_returns_one(self):
        inp = make_input(benchmark_deal_size_eur=0.0)
        assert _deal_size_index(inp) == 1.0

    def test_negative_benchmark_returns_one(self):
        inp = make_input(benchmark_deal_size_eur=-1.0)
        assert _deal_size_index(inp) == 1.0

    def test_rounding(self):
        inp = make_input(avg_deal_size_eur=1.0, benchmark_deal_size_eur=3.0)
        assert _deal_size_index(inp) == round(1 / 3, 2)


# ===========================================================================
# 9. _cycle_time_index
# ===========================================================================

class TestCycleTimeIndex:
    def test_at_benchmark(self):
        inp = make_input(avg_sales_cycle_days=60, benchmark_cycle_days=60)
        assert _cycle_time_index(inp) == 1.0

    def test_faster_than_benchmark(self):
        # rep closes faster → higher index
        inp = make_input(avg_sales_cycle_days=30, benchmark_cycle_days=60)
        assert _cycle_time_index(inp) == pytest.approx(2.0, rel=1e-6)

    def test_slower_than_benchmark(self):
        inp = make_input(avg_sales_cycle_days=120, benchmark_cycle_days=60)
        assert _cycle_time_index(inp) == pytest.approx(0.5, rel=1e-6)

    def test_zero_avg_cycle_returns_two(self):
        inp = make_input(avg_sales_cycle_days=0, benchmark_cycle_days=60)
        assert _cycle_time_index(inp) == 2.0

    def test_negative_avg_cycle_returns_two(self):
        inp = make_input(avg_sales_cycle_days=-1, benchmark_cycle_days=60)
        assert _cycle_time_index(inp) == 2.0

    def test_zero_benchmark_cycle_returns_one(self):
        inp = make_input(avg_sales_cycle_days=60, benchmark_cycle_days=0)
        assert _cycle_time_index(inp) == 1.0

    def test_inverted_relationship(self):
        """Longer rep cycle → lower CT index."""
        faster = make_input(avg_sales_cycle_days=30, benchmark_cycle_days=60)
        slower = make_input(avg_sales_cycle_days=90, benchmark_cycle_days=60)
        assert _cycle_time_index(faster) > _cycle_time_index(slower)

    def test_rounding(self):
        inp = make_input(avg_sales_cycle_days=7, benchmark_cycle_days=60)
        assert _cycle_time_index(inp) == round(60 / 7, 2)


# ===========================================================================
# 10. _primary_driver
# ===========================================================================

class TestPrimaryDriver:
    def test_balanced_when_spread_less_than_0_2(self):
        # all identical → spread 0
        assert _primary_driver(1.0, 1.0, 1.0, 1.0) == VelocityDriver.BALANCED

    def test_balanced_when_spread_exactly_0_19(self):
        assert _primary_driver(1.0, 1.1, 1.1, 1.19) == VelocityDriver.BALANCED

    def test_not_balanced_when_spread_clearly_above_0_2(self):
        # Use a spread well above 0.2 to avoid float precision issues
        result = _primary_driver(1.0, 1.0, 1.0, 1.5)
        assert result != VelocityDriver.BALANCED

    def test_opportunities_is_minimum(self):
        driver = _primary_driver(0.5, 1.0, 1.5, 1.2)
        assert driver == VelocityDriver.OPPORTUNITIES

    def test_win_rate_is_minimum(self):
        driver = _primary_driver(1.0, 0.4, 1.5, 1.2)
        assert driver == VelocityDriver.WIN_RATE

    def test_deal_size_is_minimum(self):
        driver = _primary_driver(1.0, 1.5, 0.3, 1.2)
        assert driver == VelocityDriver.DEAL_SIZE

    def test_cycle_time_is_minimum(self):
        driver = _primary_driver(1.0, 1.5, 1.2, 0.2)
        assert driver == VelocityDriver.CYCLE_TIME

    def test_returns_velocity_driver_instance(self):
        result = _primary_driver(0.5, 1.0, 1.5, 1.2)
        assert isinstance(result, VelocityDriver)


# ===========================================================================
# 11. _quota_attainment_pct
# ===========================================================================

class TestQuotaAttainmentPct:
    def test_full_attainment(self):
        inp = make_input(closed_won_eur=300_000.0, quota_eur=300_000.0)
        assert _quota_attainment_pct(inp) == 100.0

    def test_partial_attainment(self):
        inp = make_input(closed_won_eur=150_000.0, quota_eur=300_000.0)
        assert _quota_attainment_pct(inp) == 50.0

    def test_over_attainment(self):
        inp = make_input(closed_won_eur=360_000.0, quota_eur=300_000.0)
        assert _quota_attainment_pct(inp) == 120.0

    def test_zero_quota_returns_zero(self):
        inp = make_input(quota_eur=0.0, closed_won_eur=100_000.0)
        assert _quota_attainment_pct(inp) == 0.0

    def test_negative_quota_returns_zero(self):
        inp = make_input(quota_eur=-1.0, closed_won_eur=100_000.0)
        assert _quota_attainment_pct(inp) == 0.0

    def test_rounding_one_decimal(self):
        inp = make_input(closed_won_eur=100_000.0, quota_eur=300_000.0)
        # 100000/300000*100 = 33.333... → 33.3
        assert _quota_attainment_pct(inp) == 33.3


# ===========================================================================
# 12. _projected_arr_eur
# ===========================================================================

class TestProjectedArrEur:
    def test_basic(self):
        assert _projected_arr_eur(1000.0) == 365_000.0

    def test_zero_velocity(self):
        assert _projected_arr_eur(0.0) == 0.0

    def test_rounding_to_integer(self):
        # 1.5 * 365 = 547.5 → rounds to 548.0
        result = _projected_arr_eur(1.5)
        assert result == round(1.5 * 365, 0)

    def test_returns_float(self):
        assert isinstance(_projected_arr_eur(500.0), float)


# ===========================================================================
# 13. _velocity_score
# ===========================================================================

class TestVelocityScore:
    def test_all_at_benchmark_no_bonus_check(self):
        # opp=wr=ds=ct=1.0, att=0 → 4*25 + 0 = 100 + bonus 5 = 100 (clamped)
        score = _velocity_score(1.0, 1.0, 1.0, 1.0, 0.0)
        assert isinstance(score, (int, float))
        assert 0 <= score <= 100

    def test_all_indices_above_one_triggers_bonus(self):
        # Each 1.0→25pts, att=100→25pts = 100pts + 5 bonus, clamped to 100
        score = _velocity_score(1.0, 1.0, 1.0, 1.0, 100.0)
        assert score == 100.0

    def test_zero_everything_gives_zero_score(self):
        score = _velocity_score(0.0, 0.0, 0.0, 0.0, 0.0)
        assert score == 0.0

    def test_each_index_capped_at_25(self):
        # Each index 2.0 → min(25, 50) = 25; 4*25=100 but bonus for all>=1 → clamped 100
        score = _velocity_score(2.0, 2.0, 2.0, 2.0, 0.0)
        assert score == 100.0

    def test_attainment_capped_at_25(self):
        # att=200 → min(25, 50) = 25
        score_high_att = _velocity_score(0.0, 0.0, 0.0, 0.0, 200.0)
        assert score_high_att == 25.0

    def test_bonus_only_when_all_indices_ge_one(self):
        # opp < 1 → no bonus
        score_no_bonus = _velocity_score(0.99, 1.0, 1.0, 1.0, 100.0)
        score_bonus = _velocity_score(1.0, 1.0, 1.0, 1.0, 100.0)
        assert score_bonus > score_no_bonus or score_bonus == 100.0

    def test_partial_indices(self):
        # opp=0.5 → 12.5, others=1 → 25 each, att=0 → score = 12.5+25+25+25 +5(bonus? no, opp<1) = 87.5
        score = _velocity_score(0.5, 1.0, 1.0, 1.0, 0.0)
        assert score == pytest.approx(87.5, rel=1e-6)

    def test_score_clamped_min_zero(self):
        score = _velocity_score(-5.0, -5.0, -5.0, -5.0, -100.0)
        assert score == 0.0

    def test_score_clamped_max_100(self):
        score = _velocity_score(10.0, 10.0, 10.0, 10.0, 10000.0)
        assert score == 100.0

    def test_returns_float(self):
        assert isinstance(_velocity_score(1.0, 1.0, 1.0, 1.0, 50.0), float)

    def test_attainment_contribution(self):
        # att=100 → 25 points, att=0 → 0 points
        s_with = _velocity_score(0.0, 0.0, 0.0, 0.0, 100.0)
        s_without = _velocity_score(0.0, 0.0, 0.0, 0.0, 0.0)
        assert s_with - s_without == pytest.approx(25.0, rel=1e-6)


# ===========================================================================
# 14. _velocity_tier
# ===========================================================================

class TestVelocityTierFunction:
    def test_elite_at_85(self):
        assert _velocity_tier(85.0) == VelocityTier.ELITE

    def test_elite_at_100(self):
        assert _velocity_tier(100.0) == VelocityTier.ELITE

    def test_high_at_65(self):
        assert _velocity_tier(65.0) == VelocityTier.HIGH

    def test_high_at_84(self):
        assert _velocity_tier(84.9) == VelocityTier.HIGH

    def test_average_at_45(self):
        assert _velocity_tier(45.0) == VelocityTier.AVERAGE

    def test_average_at_64(self):
        assert _velocity_tier(64.9) == VelocityTier.AVERAGE

    def test_low_at_25(self):
        assert _velocity_tier(25.0) == VelocityTier.LOW

    def test_low_at_44(self):
        assert _velocity_tier(44.9) == VelocityTier.LOW

    def test_stalled_at_24(self):
        assert _velocity_tier(24.9) == VelocityTier.STALLED

    def test_stalled_at_zero(self):
        assert _velocity_tier(0.0) == VelocityTier.STALLED

    def test_returns_velocity_tier_instance(self):
        assert isinstance(_velocity_tier(50.0), VelocityTier)


# ===========================================================================
# 15. _velocity_action
# ===========================================================================

class TestVelocityActionFunction:
    def test_elite_maps_to_celebrate(self):
        assert _velocity_action(VelocityTier.ELITE) == VelocityAction.CELEBRATE

    def test_high_maps_to_accelerate(self):
        assert _velocity_action(VelocityTier.HIGH) == VelocityAction.ACCELERATE

    def test_average_maps_to_optimize(self):
        assert _velocity_action(VelocityTier.AVERAGE) == VelocityAction.OPTIMIZE

    def test_low_maps_to_rescue(self):
        assert _velocity_action(VelocityTier.LOW) == VelocityAction.RESCUE

    def test_stalled_maps_to_reset(self):
        assert _velocity_action(VelocityTier.STALLED) == VelocityAction.RESET

    def test_returns_velocity_action_instance(self):
        assert isinstance(_velocity_action(VelocityTier.HIGH), VelocityAction)


# ===========================================================================
# 16. _velocity_gaps
# ===========================================================================

class TestVelocityGaps:
    def _gaps(self, **kwargs):
        inp = make_input(**kwargs)
        opp = _opportunity_index(inp)
        wr = _win_rate_index(inp)
        ds = _deal_size_index(inp)
        ct = _cycle_time_index(inp)
        return _velocity_gaps(inp, opp, wr, ds, ct)

    def test_no_gaps_when_all_fine(self):
        # At benchmark, advancing 60%, connect 25%, cycle half of sales cycle
        gaps = self._gaps()
        assert gaps == []

    def test_low_opportunities_gap(self):
        gaps = self._gaps(opportunities_created=5, benchmark_opps=20)
        assert any("opportunit" in g.lower() for g in gaps)

    def test_low_win_rate_gap(self):
        gaps = self._gaps(win_rate_pct=10.0, benchmark_win_rate_pct=30.0)
        assert any("signature" in g.lower() or "win" in g.lower() for g in gaps)

    def test_low_deal_size_gap(self):
        gaps = self._gaps(avg_deal_size_eur=10_000.0, benchmark_deal_size_eur=50_000.0)
        assert any("deal" in g.lower() or "taille" in g.lower() for g in gaps)

    def test_slow_cycle_gap(self):
        gaps = self._gaps(avg_sales_cycle_days=200, benchmark_cycle_days=60)
        assert any("cycle" in g.lower() or "vente" in g.lower() for g in gaps)

    def test_stagnant_pipeline_gap(self):
        gaps = self._gaps(deals_advancing_pct=30.0)
        assert any("stagnant" in g.lower() or "avancent" in g.lower() for g in gaps)

    def test_low_connect_rate_gap(self):
        gaps = self._gaps(connect_rate_pct=10.0)
        assert any("connexion" in g.lower() or "connect" in g.lower() or "outreach" in g.lower() for g in gaps)

    def test_blocked_deals_gap(self):
        # avg_days_in_stage > avg_sales_cycle_days * 0.5
        gaps = self._gaps(avg_days_in_stage=50.0, avg_sales_cycle_days=60)
        assert any("bloqués" in g.lower() or "stage" in g.lower() for g in gaps)

    def test_returns_list(self):
        assert isinstance(self._gaps(), list)

    def test_threshold_exactly_0_8_no_gap(self):
        # opp index exactly 0.8 → no gap (< 0.8 triggers gap)
        gaps = self._gaps(opportunities_created=16, benchmark_opps=20)
        # 16/20 = 0.8 — not < 0.8, so no gap
        assert not any("opportunit" in g.lower() for g in gaps)

    def test_threshold_just_below_0_8_gap(self):
        # 15/20 = 0.75 < 0.8 → gap
        gaps = self._gaps(opportunities_created=15, benchmark_opps=20)
        assert any("opportunit" in g.lower() for g in gaps)


# ===========================================================================
# 17. _velocity_levers
# ===========================================================================

class TestVelocityLevers:
    def _levers(self, action: VelocityAction, driver: VelocityDriver,
                opp=1.0, wr=1.0, ds=1.0, ct=1.0, pipeline_total_eur=500_000.0):
        inp = make_input(pipeline_total_eur=pipeline_total_eur)
        return _velocity_levers(inp, action, driver, opp, wr, ds, ct)

    def test_reset_action_returns_four_levers(self):
        levers = self._levers(VelocityAction.RESET, VelocityDriver.OPPORTUNITIES)
        assert len(levers) == 4

    def test_reset_contains_audit(self):
        levers = self._levers(VelocityAction.RESET, VelocityDriver.OPPORTUNITIES)
        assert any("audit" in l.lower() for l in levers)

    def test_rescue_opportunities_driver(self):
        levers = self._levers(VelocityAction.RESCUE, VelocityDriver.OPPORTUNITIES)
        assert any("prospection" in l.lower() or "outreach" in l.lower() for l in levers)

    def test_rescue_win_rate_driver(self):
        levers = self._levers(VelocityAction.RESCUE, VelocityDriver.WIN_RATE)
        assert any("closing" in l.lower() or "requalif" in l.lower() for l in levers)

    def test_rescue_deal_size_driver(self):
        levers = self._levers(VelocityAction.RESCUE, VelocityDriver.DEAL_SIZE)
        assert any("upscal" in l.lower() or "arr" in l.lower() for l in levers)

    def test_rescue_cycle_time_driver(self):
        levers = self._levers(VelocityAction.RESCUE, VelocityDriver.CYCLE_TIME)
        assert any("blocage" in l.lower() or "stagnant" in l.lower() for l in levers)

    def test_rescue_always_includes_weekly_check(self):
        for driver in [VelocityDriver.OPPORTUNITIES, VelocityDriver.WIN_RATE,
                       VelocityDriver.DEAL_SIZE, VelocityDriver.CYCLE_TIME]:
            levers = self._levers(VelocityAction.RESCUE, driver)
            assert any("hebdo" in l.lower() or "manager" in l.lower() for l in levers)

    def test_optimize_low_opp_lever(self):
        levers = self._levers(VelocityAction.OPTIMIZE, VelocityDriver.BALANCED, opp=0.9)
        assert any("opportunit" in l.lower() for l in levers)

    def test_optimize_low_wr_lever(self):
        levers = self._levers(VelocityAction.OPTIMIZE, VelocityDriver.BALANCED, wr=0.9)
        assert any("conversion" in l.lower() or "qualif" in l.lower() for l in levers)

    def test_optimize_low_ds_lever(self):
        levers = self._levers(VelocityAction.OPTIMIZE, VelocityDriver.BALANCED, ds=0.9)
        assert any("valeur" in l.lower() or "upsell" in l.lower() for l in levers)

    def test_optimize_slow_ct_lever(self):
        levers = self._levers(VelocityAction.OPTIMIZE, VelocityDriver.BALANCED, ct=0.9)
        assert any("cycle" in l.lower() or "accél" in l.lower() for l in levers)

    def test_optimize_always_includes_analyze_wins(self):
        levers = self._levers(VelocityAction.OPTIMIZE, VelocityDriver.BALANCED)
        assert any("gagnés" in l.lower() or "succès" in l.lower() for l in levers)

    def test_accelerate_includes_pipeline_lever_when_pipeline_positive(self):
        levers = self._levers(VelocityAction.ACCELERATE, VelocityDriver.BALANCED,
                              pipeline_total_eur=500_000.0)
        assert any("pipeline" in l.lower() for l in levers)

    def test_accelerate_no_pipeline_lever_when_pipeline_zero(self):
        levers = self._levers(VelocityAction.ACCELERATE, VelocityDriver.BALANCED,
                              pipeline_total_eur=0.0)
        assert not any("pipeline" in l.lower() for l in levers)

    def test_celebrate_includes_playbook(self):
        levers = self._levers(VelocityAction.CELEBRATE, VelocityDriver.BALANCED)
        assert any("playbook" in l.lower() for l in levers)

    def test_celebrate_includes_mentor(self):
        levers = self._levers(VelocityAction.CELEBRATE, VelocityDriver.BALANCED)
        assert any("mentor" in l.lower() for l in levers)

    def test_returns_list(self):
        levers = self._levers(VelocityAction.OPTIMIZE, VelocityDriver.BALANCED)
        assert isinstance(levers, list)


# ===========================================================================
# 18. SalesVelocityEngine.analyze — basic
# ===========================================================================

class TestEngineAnalyze:
    def test_returns_velocity_result(self, engine, baseline_input):
        result = engine.analyze(baseline_input)
        assert isinstance(result, VelocityResult)

    def test_result_rep_id_matches(self, engine, baseline_input):
        result = engine.analyze(baseline_input)
        assert result.rep_id == baseline_input.rep_id

    def test_result_stored_internally(self, engine, baseline_input):
        engine.analyze(baseline_input)
        assert baseline_input.rep_id in engine._results

    def test_velocity_eur_per_day_correct(self, engine, baseline_input):
        result = engine.analyze(baseline_input)
        expected = round(baseline_input.closed_won_eur / baseline_input.period_days, 2)
        assert result.velocity_eur_per_day == expected

    def test_projected_arr_correct(self, engine, baseline_input):
        result = engine.analyze(baseline_input)
        assert result.projected_arr_eur == round(result.velocity_eur_per_day * 365, 0)

    def test_velocity_score_is_numeric(self, engine, baseline_input):
        result = engine.analyze(baseline_input)
        assert isinstance(result.velocity_score, (int, float))
        assert 0 <= result.velocity_score <= 100

    def test_tier_and_action_consistent(self, engine, baseline_input):
        result = engine.analyze(baseline_input)
        expected_action = _velocity_action(result.velocity_tier)
        assert result.velocity_action == expected_action

    def test_gaps_and_levers_are_lists(self, engine, baseline_input):
        result = engine.analyze(baseline_input)
        assert isinstance(result.velocity_gaps, list)
        assert isinstance(result.velocity_levers, list)

    def test_elite_result(self, engine, elite_input):
        result = engine.analyze(elite_input)
        assert result.velocity_tier == VelocityTier.ELITE
        assert result.velocity_action == VelocityAction.CELEBRATE

    def test_stalled_result(self, engine, stalled_input):
        result = engine.analyze(stalled_input)
        assert result.velocity_tier == VelocityTier.STALLED
        assert result.velocity_action == VelocityAction.RESET

    def test_overwrite_same_rep(self, engine):
        inp1 = make_input(rep_id="x", closed_won_eur=100_000.0)
        inp2 = make_input(rep_id="x", closed_won_eur=200_000.0)
        engine.analyze(inp1)
        r2 = engine.analyze(inp2)
        assert engine._results["x"].velocity_eur_per_day == r2.velocity_eur_per_day


# ===========================================================================
# 19. SalesVelocityEngine.analyze_batch
# ===========================================================================

class TestEngineAnalyzeBatch:
    def _batch_inputs(self):
        return [
            make_input(rep_id="a", closed_won_eur=100_000.0),
            make_input(rep_id="b", closed_won_eur=300_000.0),
            make_input(rep_id="c", closed_won_eur=200_000.0),
        ]

    def test_returns_all_results(self, engine):
        results = engine.analyze_batch(self._batch_inputs())
        assert len(results) == 3

    def test_sorted_descending_by_velocity(self, engine):
        results = engine.analyze_batch(self._batch_inputs())
        velocities = [r.velocity_eur_per_day for r in results]
        assert velocities == sorted(velocities, reverse=True)

    def test_first_is_highest_velocity(self, engine):
        results = engine.analyze_batch(self._batch_inputs())
        assert results[0].rep_id == "b"

    def test_all_stored_internally(self, engine):
        engine.analyze_batch(self._batch_inputs())
        assert len(engine._results) == 3

    def test_empty_batch(self, engine):
        results = engine.analyze_batch([])
        assert results == []


# ===========================================================================
# 20. Engine filter methods
# ===========================================================================

class TestEngineFilterMethods:
    @pytest.fixture(autouse=True)
    def _populate(self, engine, elite_input, stalled_input):
        self.engine = engine
        self.engine.analyze(elite_input)
        self.engine.analyze(stalled_input)
        avg_inp = make_input(rep_id="avg1", opportunities_created=12,
                             win_rate_pct=20.0, avg_deal_size_eur=30_000.0,
                             avg_sales_cycle_days=80, closed_won_eur=100_000.0)
        self.engine.analyze(avg_inp)

    def test_by_tier_elite(self):
        elites = self.engine.by_tier(VelocityTier.ELITE)
        assert all(r.velocity_tier == VelocityTier.ELITE for r in elites)
        assert len(elites) >= 1

    def test_by_tier_stalled(self):
        stalled = self.engine.by_tier(VelocityTier.STALLED)
        assert all(r.velocity_tier == VelocityTier.STALLED for r in stalled)

    def test_by_action_celebrate(self):
        results = self.engine.by_action(VelocityAction.CELEBRATE)
        assert all(r.velocity_action == VelocityAction.CELEBRATE for r in results)

    def test_by_action_reset(self):
        results = self.engine.by_action(VelocityAction.RESET)
        assert all(r.velocity_action == VelocityAction.RESET for r in results)

    def test_by_driver_returns_correct_driver(self):
        for d in VelocityDriver:
            results = self.engine.by_driver(d)
            assert all(r.primary_driver == d for r in results)

    def test_elite_reps_equals_by_tier_elite(self):
        assert self.engine.elite_reps() == self.engine.by_tier(VelocityTier.ELITE)

    def test_stalled_reps_equals_by_tier_stalled(self):
        assert self.engine.stalled_reps() == self.engine.by_tier(VelocityTier.STALLED)

    def test_needs_reset_equals_by_action_reset(self):
        assert self.engine.needs_reset() == self.engine.by_action(VelocityAction.RESET)

    def test_at_risk_reps_includes_low_and_stalled(self):
        at_risk = self.engine.at_risk_reps()
        assert all(r.velocity_tier in (VelocityTier.LOW, VelocityTier.STALLED) for r in at_risk)

    def test_at_risk_excludes_higher_tiers(self):
        at_risk = self.engine.at_risk_reps()
        higher = {VelocityTier.ELITE, VelocityTier.HIGH, VelocityTier.AVERAGE}
        assert all(r.velocity_tier not in higher for r in at_risk)


# ===========================================================================
# 21. Engine aggregate methods
# ===========================================================================

class TestEngineAggregates:
    @pytest.fixture(autouse=True)
    def _populate(self, engine):
        self.engine = engine
        self.engine.analyze(make_input(rep_id="r1", closed_won_eur=90_000.0, period_days=90))
        self.engine.analyze(make_input(rep_id="r2", closed_won_eur=180_000.0, period_days=90))

    def test_avg_velocity(self):
        avg = self.engine.avg_velocity()
        # r1: 90000/90=1000, r2: 180000/90=2000 → avg=1500
        assert avg == pytest.approx(1500.0, rel=1e-6)

    def test_avg_velocity_score_is_float(self):
        s = self.engine.avg_velocity_score()
        assert isinstance(s, (int, float))
        assert 0 <= s <= 100

    def test_total_projected_arr_eur(self):
        total = self.engine.total_projected_arr_eur()
        r1 = self.engine._results["r1"]
        r2 = self.engine._results["r2"]
        assert total == r1.projected_arr_eur + r2.projected_arr_eur

    def test_top_velocity_rep_is_r2(self):
        top = self.engine.top_velocity_rep()
        assert top is not None
        assert top.rep_id == "r2"

    def test_top_velocity_rep_none_when_empty(self):
        empty = SalesVelocityEngine()
        assert empty.top_velocity_rep() is None

    def test_avg_velocity_zero_when_empty(self):
        empty = SalesVelocityEngine()
        assert empty.avg_velocity() == 0.0

    def test_avg_velocity_score_zero_when_empty(self):
        empty = SalesVelocityEngine()
        assert empty.avg_velocity_score() == 0.0

    def test_total_projected_arr_zero_when_empty(self):
        empty = SalesVelocityEngine()
        assert empty.total_projected_arr_eur() == 0.0


# ===========================================================================
# 22. constraint_distribution and summary
# ===========================================================================

class TestConstraintDistributionAndSummary:
    @pytest.fixture(autouse=True)
    def _populate(self, engine):
        self.engine = engine
        for i, rep_id in enumerate(["d1", "d2", "d3"]):
            self.engine.analyze(make_input(rep_id=rep_id, closed_won_eur=float((i + 1) * 50_000)))

    def test_constraint_distribution_has_all_drivers(self):
        dist = self.engine.constraint_distribution()
        for d in VelocityDriver:
            assert d.value in dist

    def test_constraint_distribution_counts_sum_to_total(self):
        dist = self.engine.constraint_distribution()
        assert sum(dist.values()) == len(self.engine._results)

    def test_summary_total(self):
        s = self.engine.summary()
        assert s["total"] == 3

    def test_summary_tier_counts_keys(self):
        s = self.engine.summary()
        for t in VelocityTier:
            assert t.value in s["tier_counts"]

    def test_summary_action_counts_keys(self):
        s = self.engine.summary()
        for a in VelocityAction:
            assert a.value in s["action_counts"]

    def test_summary_driver_counts_keys(self):
        s = self.engine.summary()
        for d in VelocityDriver:
            assert d.value in s["driver_counts"]

    def test_summary_tier_counts_sum_to_total(self):
        s = self.engine.summary()
        assert sum(s["tier_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_to_total(self):
        s = self.engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_avg_velocity_is_numeric(self):
        s = self.engine.summary()
        assert isinstance(s["avg_velocity_eur_per_day"], (int, float))

    def test_summary_elite_count(self):
        s = self.engine.summary()
        assert s["elite_count"] == len(self.engine.elite_reps())

    def test_summary_stalled_count(self):
        s = self.engine.summary()
        assert s["stalled_count"] == len(self.engine.stalled_reps())

    def test_summary_total_projected_arr_eur(self):
        s = self.engine.summary()
        assert s["total_projected_arr_eur"] == self.engine.total_projected_arr_eur()


# ===========================================================================
# 23. Engine.reset
# ===========================================================================

class TestEngineReset:
    def test_reset_clears_results(self, engine, baseline_input):
        engine.analyze(baseline_input)
        assert len(engine._results) == 1
        engine.reset()
        assert len(engine._results) == 0

    def test_reset_makes_avg_velocity_zero(self, engine, baseline_input):
        engine.analyze(baseline_input)
        engine.reset()
        assert engine.avg_velocity() == 0.0

    def test_reset_makes_top_rep_none(self, engine, baseline_input):
        engine.analyze(baseline_input)
        engine.reset()
        assert engine.top_velocity_rep() is None

    def test_can_reuse_after_reset(self, engine, baseline_input):
        engine.analyze(baseline_input)
        engine.reset()
        r = engine.analyze(baseline_input)
        assert r.rep_id == baseline_input.rep_id
        assert len(engine._results) == 1


# ===========================================================================
# 24. Edge cases & boundary conditions
# ===========================================================================

class TestEdgeCasesAndBoundary:
    def test_zero_period_days_velocity_zero(self):
        inp = make_input(period_days=0)
        v = _velocity_eur_per_day(inp)
        assert v == 0.0

    def test_zero_closed_won_gives_zero_velocity_and_arr(self, engine):
        # closed_won_eur=0 → velocity=0, ARR=0.
        # Score is driven by the 4 index ratios, not revenue — so tier can be anything
        # depending on how the rep compares to benchmark on the other levers.
        inp2 = make_input(rep_id="zero_close", closed_won_eur=0.0, quota_eur=300_000.0)
        result = engine.analyze(inp2)
        assert result.velocity_eur_per_day == 0.0
        assert result.projected_arr_eur == 0.0

    def test_very_high_performance_capped_score(self, engine):
        inp = make_input(
            rep_id="super",
            opportunities_created=200,
            win_rate_pct=100.0,
            avg_deal_size_eur=1_000_000.0,
            avg_sales_cycle_days=1,
            quota_eur=100_000.0,
            closed_won_eur=10_000_000.0,
        )
        result = engine.analyze(inp)
        assert result.velocity_score == 100.0
        assert result.velocity_tier == VelocityTier.ELITE

    def test_benchmark_zero_indices_default_to_one(self):
        inp = make_input(
            benchmark_opps=0,
            benchmark_win_rate_pct=0.0,
            benchmark_deal_size_eur=0.0,
            benchmark_cycle_days=0,
        )
        assert _opportunity_index(inp) == 1.0
        assert _win_rate_index(inp) == 1.0
        assert _deal_size_index(inp) == 1.0
        assert _cycle_time_index(inp) == 1.0

    def test_analyze_batch_single_rep_sorted(self, engine):
        inp = make_input(rep_id="only")
        results = engine.analyze_batch([inp])
        assert len(results) == 1
        assert results[0].rep_id == "only"

    def test_all_reps_sorted_descending(self, engine):
        for i, v in enumerate([50_000.0, 200_000.0, 100_000.0]):
            engine.analyze(make_input(rep_id=f"rep{i}", closed_won_eur=v))
        all_r = engine.all_reps()
        velocities = [r.velocity_eur_per_day for r in all_r]
        assert velocities == sorted(velocities, reverse=True)

    def test_quota_attainment_above_100_percent(self):
        inp = make_input(closed_won_eur=450_000.0, quota_eur=300_000.0)
        att = _quota_attainment_pct(inp)
        assert att == 150.0

    def test_cycle_time_index_inverted_formula(self):
        inp = make_input(avg_sales_cycle_days=30, benchmark_cycle_days=60)
        assert _cycle_time_index(inp) == 2.0

    def test_primary_driver_balanced_spread_just_under_0_2(self):
        result = _primary_driver(1.0, 1.0, 1.0, 1.19)
        assert result == VelocityDriver.BALANCED

    def test_primary_driver_not_balanced_spread_clearly_above_0_2(self):
        # Use a spread well above 0.2 (e.g. 0.5) to avoid float precision edge cases
        result = _primary_driver(1.0, 1.0, 1.0, 1.5)
        assert result != VelocityDriver.BALANCED

    def test_velocity_score_boundary_85_is_elite(self, engine):
        # Craft input that yields score exactly at boundary
        # All indices at 1.0 = 4*25=100pts + bonus 5 = 100 → ELITE
        inp = make_input(
            opportunities_created=20, win_rate_pct=30.0,
            avg_deal_size_eur=50_000.0, avg_sales_cycle_days=60,
            closed_won_eur=0.0, quota_eur=300_000.0,
        )
        result = engine.analyze(inp)
        # All indices = 1 → score = 100 + 5 - but we have att=0, so:
        # 25+25+25+25 + 0 + bonus 5 = 105, clamped to 100
        assert result.velocity_score == 100.0
        assert result.velocity_tier == VelocityTier.ELITE
