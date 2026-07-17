"""
Comprehensive pytest test suite for Module 28 — Forecast Accuracy Engine.
Target: 22 test classes, 270+ tests, all passing.
"""

from __future__ import annotations

import pytest

from swarm.intelligence.forecast_accuracy_engine import (
    ForecastAccuracy,
    ForecastAction,
    ForecastAccuracyEngine,
    ForecastBias,
    ForecastInput,
    ForecastResult,
    RepTier,
    _accuracy_pct,
    _accuracy_tier,
    _attainment_pct,
    _bias,
    _forecast_action,
    _reliability_score,
    _rep_tier,
    _variance_eur,
    _accuracy_drivers,
    _accuracy_gaps,
    _coaching_recommendations,
)


# ---------------------------------------------------------------------------
# Factory helper
# ---------------------------------------------------------------------------

def make_rep(
    rep_id: str = "REP001",
    rep_name: str = "Alice Dupont",
    region: str = "EMEA",
    segment: str = "enterprise",
    periods: int = 4,
    total_committed_eur: float = 100_000.0,
    total_actual_eur: float = 95_000.0,
    crm_update_lag_days: float = 1.0,
    pipeline_coverage_ratio: float = 3.5,
    late_stage_pull_ins: int = 0,
    sandbagging_events: int = 0,
    avg_deal_slip_days: float = 3.0,
    quota_eur: float = 100_000.0,
) -> ForecastInput:
    """Return a ForecastInput with sensible defaults (neutral/good rep)."""
    return ForecastInput(
        rep_id=rep_id,
        rep_name=rep_name,
        region=region,
        segment=segment,
        periods=periods,
        total_committed_eur=total_committed_eur,
        total_actual_eur=total_actual_eur,
        crm_update_lag_days=crm_update_lag_days,
        pipeline_coverage_ratio=pipeline_coverage_ratio,
        late_stage_pull_ins=late_stage_pull_ins,
        sandbagging_events=sandbagging_events,
        avg_deal_slip_days=avg_deal_slip_days,
        quota_eur=quota_eur,
    )


# ---------------------------------------------------------------------------
# Class 1 — Enum membership and values
# ---------------------------------------------------------------------------

class TestEnums:
    def test_forecast_accuracy_members(self):
        members = {e.name for e in ForecastAccuracy}
        assert members == {"EXCELLENT", "GOOD", "FAIR", "POOR"}

    def test_forecast_accuracy_values(self):
        assert ForecastAccuracy.EXCELLENT.value == "excellent"
        assert ForecastAccuracy.GOOD.value == "good"
        assert ForecastAccuracy.FAIR.value == "fair"
        assert ForecastAccuracy.POOR.value == "poor"

    def test_forecast_bias_members(self):
        members = {e.name for e in ForecastBias}
        assert members == {"OPTIMISTIC", "NEUTRAL", "PESSIMISTIC"}

    def test_forecast_bias_values(self):
        assert ForecastBias.OPTIMISTIC.value == "optimistic"
        assert ForecastBias.NEUTRAL.value == "neutral"
        assert ForecastBias.PESSIMISTIC.value == "pessimistic"

    def test_forecast_action_members(self):
        members = {e.name for e in ForecastAction}
        assert members == {"CELEBRATE", "CALIBRATE", "IMPROVE", "OVERHAUL"}

    def test_forecast_action_values(self):
        assert ForecastAction.CELEBRATE.value == "celebrate"
        assert ForecastAction.CALIBRATE.value == "calibrate"
        assert ForecastAction.IMPROVE.value == "improve"
        assert ForecastAction.OVERHAUL.value == "overhaul"

    def test_rep_tier_members(self):
        members = {e.name for e in RepTier}
        assert members == {"TOP", "SOLID", "DEVELOPING", "STRUGGLING"}

    def test_rep_tier_values(self):
        assert RepTier.TOP.value == "top"
        assert RepTier.SOLID.value == "solid"
        assert RepTier.DEVELOPING.value == "developing"
        assert RepTier.STRUGGLING.value == "struggling"

    def test_enums_are_str_subclasses(self):
        assert isinstance(ForecastAccuracy.EXCELLENT, str)
        assert isinstance(ForecastBias.NEUTRAL, str)
        assert isinstance(ForecastAction.CELEBRATE, str)
        assert isinstance(RepTier.TOP, str)


# ---------------------------------------------------------------------------
# Class 2 — ForecastInput dataclass
# ---------------------------------------------------------------------------

class TestForecastInput:
    def test_creation_with_defaults(self):
        inp = make_rep()
        assert inp.rep_id == "REP001"
        assert inp.rep_name == "Alice Dupont"

    def test_all_fields_accessible(self):
        inp = make_rep()
        assert hasattr(inp, "rep_id")
        assert hasattr(inp, "rep_name")
        assert hasattr(inp, "region")
        assert hasattr(inp, "segment")
        assert hasattr(inp, "periods")
        assert hasattr(inp, "total_committed_eur")
        assert hasattr(inp, "total_actual_eur")
        assert hasattr(inp, "crm_update_lag_days")
        assert hasattr(inp, "pipeline_coverage_ratio")
        assert hasattr(inp, "late_stage_pull_ins")
        assert hasattr(inp, "sandbagging_events")
        assert hasattr(inp, "avg_deal_slip_days")
        assert hasattr(inp, "quota_eur")

    def test_custom_field_values(self):
        inp = make_rep(rep_id="X99", region="APAC", segment="smb", periods=2)
        assert inp.rep_id == "X99"
        assert inp.region == "APAC"
        assert inp.segment == "smb"
        assert inp.periods == 2

    def test_numeric_fields_accept_floats(self):
        inp = make_rep(total_committed_eur=123456.78, crm_update_lag_days=2.5)
        assert inp.total_committed_eur == 123456.78
        assert inp.crm_update_lag_days == 2.5


# ---------------------------------------------------------------------------
# Class 3 — _accuracy_pct formula
# ---------------------------------------------------------------------------

class TestAccuracyPct:
    def test_perfect_accuracy(self):
        inp = make_rep(total_committed_eur=100_000, total_actual_eur=100_000)
        assert _accuracy_pct(inp) == 100.0

    def test_five_pct_miss(self):
        inp = make_rep(total_committed_eur=100_000, total_actual_eur=95_000)
        assert _accuracy_pct(inp) == 95.0

    def test_ten_pct_over(self):
        inp = make_rep(total_committed_eur=100_000, total_actual_eur=110_000)
        assert _accuracy_pct(inp) == 90.0

    def test_zero_committed_returns_zero(self):
        inp = make_rep(total_committed_eur=0, total_actual_eur=50_000)
        assert _accuracy_pct(inp) == 0.0

    def test_negative_committed_returns_zero(self):
        inp = make_rep(total_committed_eur=-1, total_actual_eur=50_000)
        assert _accuracy_pct(inp) == 0.0

    def test_large_miss_clamped_to_zero(self):
        inp = make_rep(total_committed_eur=100_000, total_actual_eur=0)
        assert _accuracy_pct(inp) == 0.0

    def test_slight_miss_90_boundary(self):
        # 10% miss → 90% accuracy (boundary EXCELLENT/GOOD)
        inp = make_rep(total_committed_eur=100_000, total_actual_eur=90_000)
        assert _accuracy_pct(inp) == 90.0

    def test_return_is_float(self):
        inp = make_rep(total_committed_eur=100_000, total_actual_eur=95_000)
        result = _accuracy_pct(inp)
        assert isinstance(result, (int, float))

    def test_result_rounded_to_one_decimal(self):
        # 1/3 variance → non-trivial rounding
        inp = make_rep(total_committed_eur=300, total_actual_eur=200)
        result = _accuracy_pct(inp)
        assert result == round(result, 1)

    def test_symmetry_over_and_under(self):
        over = make_rep(total_committed_eur=100_000, total_actual_eur=115_000)
        under = make_rep(total_committed_eur=100_000, total_actual_eur=85_000)
        assert _accuracy_pct(over) == _accuracy_pct(under)

    def test_small_committed(self):
        inp = make_rep(total_committed_eur=1, total_actual_eur=1)
        assert _accuracy_pct(inp) == 100.0


# ---------------------------------------------------------------------------
# Class 4 — _attainment_pct formula
# ---------------------------------------------------------------------------

class TestAttainmentPct:
    def test_full_attainment(self):
        inp = make_rep(total_actual_eur=100_000, quota_eur=100_000)
        assert _attainment_pct(inp) == 100.0

    def test_partial_attainment(self):
        inp = make_rep(total_actual_eur=80_000, quota_eur=100_000)
        assert _attainment_pct(inp) == 80.0

    def test_over_attainment(self):
        inp = make_rep(total_actual_eur=125_000, quota_eur=100_000)
        assert _attainment_pct(inp) == 125.0

    def test_zero_quota_returns_zero(self):
        inp = make_rep(total_actual_eur=50_000, quota_eur=0)
        assert _attainment_pct(inp) == 0.0

    def test_negative_quota_returns_zero(self):
        inp = make_rep(total_actual_eur=50_000, quota_eur=-1)
        assert _attainment_pct(inp) == 0.0

    def test_return_is_float(self):
        inp = make_rep(total_actual_eur=80_000, quota_eur=100_000)
        assert isinstance(_attainment_pct(inp), (int, float))

    def test_result_rounded_to_one_decimal(self):
        inp = make_rep(total_actual_eur=10_000, quota_eur=30_000)
        result = _attainment_pct(inp)
        assert result == round(result, 1)

    def test_zero_actual(self):
        inp = make_rep(total_actual_eur=0, quota_eur=100_000)
        assert _attainment_pct(inp) == 0.0


# ---------------------------------------------------------------------------
# Class 5 — _variance_eur formula
# ---------------------------------------------------------------------------

class TestVarianceEur:
    def test_positive_variance(self):
        inp = make_rep(total_committed_eur=100_000, total_actual_eur=110_000)
        assert _variance_eur(inp) == 10_000.0

    def test_negative_variance(self):
        inp = make_rep(total_committed_eur=100_000, total_actual_eur=90_000)
        assert _variance_eur(inp) == -10_000.0

    def test_zero_variance(self):
        inp = make_rep(total_committed_eur=100_000, total_actual_eur=100_000)
        assert _variance_eur(inp) == 0.0

    def test_return_is_numeric(self):
        inp = make_rep(total_committed_eur=100_000, total_actual_eur=95_000)
        assert isinstance(_variance_eur(inp), (int, float))

    def test_large_values(self):
        inp = make_rep(total_committed_eur=1_000_000, total_actual_eur=1_200_000)
        assert _variance_eur(inp) == 200_000.0


# ---------------------------------------------------------------------------
# Class 6 — _accuracy_tier thresholds
# ---------------------------------------------------------------------------

class TestAccuracyTier:
    def test_exactly_90_is_excellent(self):
        assert _accuracy_tier(90.0) == ForecastAccuracy.EXCELLENT

    def test_above_90_is_excellent(self):
        assert _accuracy_tier(95.0) == ForecastAccuracy.EXCELLENT
        assert _accuracy_tier(100.0) == ForecastAccuracy.EXCELLENT

    def test_exactly_75_is_good(self):
        assert _accuracy_tier(75.0) == ForecastAccuracy.GOOD

    def test_between_75_and_90_is_good(self):
        assert _accuracy_tier(80.0) == ForecastAccuracy.GOOD
        assert _accuracy_tier(89.9) == ForecastAccuracy.GOOD

    def test_exactly_55_is_fair(self):
        assert _accuracy_tier(55.0) == ForecastAccuracy.FAIR

    def test_between_55_and_75_is_fair(self):
        assert _accuracy_tier(65.0) == ForecastAccuracy.FAIR
        assert _accuracy_tier(74.9) == ForecastAccuracy.FAIR

    def test_below_55_is_poor(self):
        assert _accuracy_tier(54.9) == ForecastAccuracy.POOR
        assert _accuracy_tier(0.0) == ForecastAccuracy.POOR

    def test_return_type(self):
        assert isinstance(_accuracy_tier(80.0), ForecastAccuracy)


# ---------------------------------------------------------------------------
# Class 7 — _bias thresholds
# ---------------------------------------------------------------------------

class TestBias:
    def test_neutral_within_range(self):
        inp = make_rep(total_committed_eur=100_000, total_actual_eur=105_000)
        assert _bias(inp) == ForecastBias.NEUTRAL

    def test_neutral_exact_zero(self):
        inp = make_rep(total_committed_eur=100_000, total_actual_eur=100_000)
        assert _bias(inp) == ForecastBias.NEUTRAL

    def test_pessimistic_when_actual_exceeds_by_more_than_10_pct(self):
        inp = make_rep(total_committed_eur=100_000, total_actual_eur=115_000)
        assert _bias(inp) == ForecastBias.PESSIMISTIC

    def test_optimistic_when_actual_misses_by_more_than_10_pct(self):
        inp = make_rep(total_committed_eur=100_000, total_actual_eur=85_000)
        assert _bias(inp) == ForecastBias.OPTIMISTIC

    def test_exactly_minus_10_pct_is_neutral(self):
        inp = make_rep(total_committed_eur=100_000, total_actual_eur=90_000)
        assert _bias(inp) == ForecastBias.NEUTRAL

    def test_exactly_plus_10_pct_is_neutral(self):
        inp = make_rep(total_committed_eur=100_000, total_actual_eur=110_000)
        assert _bias(inp) == ForecastBias.NEUTRAL

    def test_zero_committed_returns_neutral(self):
        inp = make_rep(total_committed_eur=0, total_actual_eur=50_000)
        assert _bias(inp) == ForecastBias.NEUTRAL

    def test_return_type(self):
        inp = make_rep()
        assert isinstance(_bias(inp), ForecastBias)

    def test_borderline_optimistic(self):
        # Just over 10% miss → OPTIMISTIC
        inp = make_rep(total_committed_eur=100_000, total_actual_eur=89_000)
        assert _bias(inp) == ForecastBias.OPTIMISTIC

    def test_borderline_pessimistic(self):
        # Just over 10% beat → PESSIMISTIC
        inp = make_rep(total_committed_eur=100_000, total_actual_eur=111_000)
        assert _bias(inp) == ForecastBias.PESSIMISTIC


# ---------------------------------------------------------------------------
# Class 8 — _forecast_action mapping
# ---------------------------------------------------------------------------

class TestForecastAction:
    def test_excellent_maps_to_celebrate(self):
        assert _forecast_action(ForecastAccuracy.EXCELLENT) == ForecastAction.CELEBRATE

    def test_good_maps_to_calibrate(self):
        assert _forecast_action(ForecastAccuracy.GOOD) == ForecastAction.CALIBRATE

    def test_fair_maps_to_improve(self):
        assert _forecast_action(ForecastAccuracy.FAIR) == ForecastAction.IMPROVE

    def test_poor_maps_to_overhaul(self):
        assert _forecast_action(ForecastAccuracy.POOR) == ForecastAction.OVERHAUL

    def test_return_type(self):
        assert isinstance(_forecast_action(ForecastAccuracy.GOOD), ForecastAction)


# ---------------------------------------------------------------------------
# Class 9 — _rep_tier thresholds
# ---------------------------------------------------------------------------

class TestRepTier:
    def test_top_tier(self):
        assert _rep_tier(100.0, 80.0) == RepTier.TOP

    def test_top_tier_exact_boundary(self):
        assert _rep_tier(100.0, 80.0) == RepTier.TOP

    def test_top_tier_high_values(self):
        assert _rep_tier(130.0, 95.0) == RepTier.TOP

    def test_solid_tier(self):
        assert _rep_tier(80.0, 65.0) == RepTier.SOLID

    def test_solid_tier_exact_boundary(self):
        assert _rep_tier(80.0, 65.0) == RepTier.SOLID

    def test_developing_by_attainment(self):
        # attainment >= 60 but not solid/top
        assert _rep_tier(60.0, 40.0) == RepTier.DEVELOPING

    def test_developing_by_accuracy(self):
        # accuracy >= 55 but not solid/top
        assert _rep_tier(40.0, 55.0) == RepTier.DEVELOPING

    def test_struggling(self):
        assert _rep_tier(50.0, 40.0) == RepTier.STRUGGLING

    def test_struggling_zero_both(self):
        assert _rep_tier(0.0, 0.0) == RepTier.STRUGGLING

    def test_return_type(self):
        assert isinstance(_rep_tier(100.0, 90.0), RepTier)

    def test_top_requires_both_conditions(self):
        # High attainment but low accuracy → not TOP
        assert _rep_tier(120.0, 70.0) != RepTier.TOP

    def test_solid_requires_both_conditions(self):
        # High attainment but low accuracy → not SOLID (but may be DEVELOPING)
        result = _rep_tier(90.0, 50.0)
        assert result != RepTier.SOLID


# ---------------------------------------------------------------------------
# Class 10 — _reliability_score components
# ---------------------------------------------------------------------------

class TestReliabilityScore:
    def test_perfect_rep_score(self):
        inp = make_rep(
            total_committed_eur=100_000,
            total_actual_eur=100_000,
            crm_update_lag_days=1.0,
            pipeline_coverage_ratio=4.0,
            late_stage_pull_ins=0,
            sandbagging_events=0,
            avg_deal_slip_days=0.0,
            quota_eur=100_000,
        )
        # accuracy=100 → 40pts; attainment=100 → min(20,20)=20pts; lag=1→+10; cov=4→+10 = 80
        score = _reliability_score(inp, 100.0, 100.0)
        assert score == 80.0

    def test_score_clamped_at_100(self):
        inp = make_rep()
        score = _reliability_score(inp, 100.0, 200.0)
        assert score <= 100.0

    def test_score_clamped_at_zero(self):
        inp = make_rep(
            late_stage_pull_ins=10,
            sandbagging_events=10,
            avg_deal_slip_days=20.0,
            crm_update_lag_days=20.0,
            pipeline_coverage_ratio=0.0,
        )
        score = _reliability_score(inp, 0.0, 0.0)
        assert score == 0.0

    def test_accuracy_component(self):
        # With all other factors zero: accuracy * 0.4
        inp = make_rep(
            crm_update_lag_days=99.0,
            pipeline_coverage_ratio=0.0,
            late_stage_pull_ins=0,
            sandbagging_events=0,
            avg_deal_slip_days=0.0,
            quota_eur=100_000,
            total_actual_eur=0.0,
        )
        score = _reliability_score(inp, 80.0, 0.0)
        assert score == round(max(0.0, min(100.0, 80.0 * 0.40)), 1)

    def test_lag_le1_adds_10(self):
        base = make_rep(crm_update_lag_days=99, pipeline_coverage_ratio=0, quota_eur=100_000, total_actual_eur=0)
        lag1 = make_rep(crm_update_lag_days=1.0, pipeline_coverage_ratio=0, quota_eur=100_000, total_actual_eur=0)
        diff = _reliability_score(lag1, 0.0, 0.0) - _reliability_score(base, 0.0, 0.0)
        assert diff == 10.0

    def test_lag_le3_adds_7(self):
        base = make_rep(crm_update_lag_days=99, pipeline_coverage_ratio=0, quota_eur=100_000, total_actual_eur=0)
        lag3 = make_rep(crm_update_lag_days=3.0, pipeline_coverage_ratio=0, quota_eur=100_000, total_actual_eur=0)
        diff = _reliability_score(lag3, 0.0, 0.0) - _reliability_score(base, 0.0, 0.0)
        assert diff == 7.0

    def test_lag_le7_adds_4(self):
        base = make_rep(crm_update_lag_days=99, pipeline_coverage_ratio=0, quota_eur=100_000, total_actual_eur=0)
        lag7 = make_rep(crm_update_lag_days=7.0, pipeline_coverage_ratio=0, quota_eur=100_000, total_actual_eur=0)
        diff = _reliability_score(lag7, 0.0, 0.0) - _reliability_score(base, 0.0, 0.0)
        assert diff == 4.0

    def test_coverage_ge4_adds_10(self):
        base = make_rep(crm_update_lag_days=99, pipeline_coverage_ratio=0, quota_eur=100_000, total_actual_eur=0)
        cov4 = make_rep(crm_update_lag_days=99, pipeline_coverage_ratio=4.0, quota_eur=100_000, total_actual_eur=0)
        diff = _reliability_score(cov4, 0.0, 0.0) - _reliability_score(base, 0.0, 0.0)
        assert diff == 10.0

    def test_coverage_ge3_adds_7(self):
        base = make_rep(crm_update_lag_days=99, pipeline_coverage_ratio=0, quota_eur=100_000, total_actual_eur=0)
        cov3 = make_rep(crm_update_lag_days=99, pipeline_coverage_ratio=3.0, quota_eur=100_000, total_actual_eur=0)
        diff = _reliability_score(cov3, 0.0, 0.0) - _reliability_score(base, 0.0, 0.0)
        assert diff == 7.0

    def test_coverage_ge2_adds_4(self):
        base = make_rep(crm_update_lag_days=99, pipeline_coverage_ratio=0, quota_eur=100_000, total_actual_eur=0)
        cov2 = make_rep(crm_update_lag_days=99, pipeline_coverage_ratio=2.0, quota_eur=100_000, total_actual_eur=0)
        diff = _reliability_score(cov2, 0.0, 0.0) - _reliability_score(base, 0.0, 0.0)
        assert diff == 4.0

    def test_pull_in_penalty_capped_at_10(self):
        inp_many = make_rep(late_stage_pull_ins=10, crm_update_lag_days=99, pipeline_coverage_ratio=0, quota_eur=100_000, total_actual_eur=0)
        inp_huge = make_rep(late_stage_pull_ins=100, crm_update_lag_days=99, pipeline_coverage_ratio=0, quota_eur=100_000, total_actual_eur=0)
        assert _reliability_score(inp_many, 0.0, 0.0) == _reliability_score(inp_huge, 0.0, 0.0)

    def test_sandbagging_penalty_capped_at_5(self):
        inp_many = make_rep(sandbagging_events=4, crm_update_lag_days=99, pipeline_coverage_ratio=0, quota_eur=100_000, total_actual_eur=0)
        inp_huge = make_rep(sandbagging_events=100, crm_update_lag_days=99, pipeline_coverage_ratio=0, quota_eur=100_000, total_actual_eur=0)
        assert _reliability_score(inp_many, 0.0, 0.0) == _reliability_score(inp_huge, 0.0, 0.0)

    def test_slip_gt14_penalty_5(self):
        # Use accuracy=50 so base score is 20 pts, enough to see penalty
        no_slip = make_rep(avg_deal_slip_days=0, crm_update_lag_days=99, pipeline_coverage_ratio=0, quota_eur=100_000, total_actual_eur=0)
        heavy_slip = make_rep(avg_deal_slip_days=15, crm_update_lag_days=99, pipeline_coverage_ratio=0, quota_eur=100_000, total_actual_eur=0)
        diff = _reliability_score(no_slip, 50.0, 0.0) - _reliability_score(heavy_slip, 50.0, 0.0)
        assert diff == 5.0

    def test_slip_gt7_penalty_3(self):
        # Use accuracy=50 so base score is 20 pts, enough to see penalty
        no_slip = make_rep(avg_deal_slip_days=0, crm_update_lag_days=99, pipeline_coverage_ratio=0, quota_eur=100_000, total_actual_eur=0)
        med_slip = make_rep(avg_deal_slip_days=10, crm_update_lag_days=99, pipeline_coverage_ratio=0, quota_eur=100_000, total_actual_eur=0)
        diff = _reliability_score(no_slip, 50.0, 0.0) - _reliability_score(med_slip, 50.0, 0.0)
        assert diff == 3.0

    def test_return_type(self):
        inp = make_rep()
        assert isinstance(_reliability_score(inp, 90.0, 100.0), (int, float))

    def test_attainment_capped_at_20_pts(self):
        # attainment 200% → min(20, 200*0.2)=min(20,40)=20
        inp = make_rep(crm_update_lag_days=99, pipeline_coverage_ratio=0, quota_eur=100_000, total_actual_eur=0)
        score_200 = _reliability_score(inp, 0.0, 200.0)
        score_150 = _reliability_score(inp, 0.0, 150.0)
        # Both capped at 20 pts for attainment
        assert score_200 == score_150


# ---------------------------------------------------------------------------
# Class 11 — _accuracy_drivers
# ---------------------------------------------------------------------------

class TestAccuracyDrivers:
    def test_high_accuracy_triggers_driver(self):
        inp = make_rep(total_committed_eur=100_000, total_actual_eur=90_000)  # 90% accuracy
        drivers = _accuracy_drivers(inp, 90.0, 100.0)
        assert any("forecast" in d.lower() or "précision" in d.lower() for d in drivers)

    def test_accuracy_below_85_no_accuracy_driver(self):
        drivers = _accuracy_drivers(make_rep(), 80.0, 100.0)
        # Should not mention forecast accuracy driver
        assert not any("90" in d or "85" in d or "80" in d for d in drivers if "précision" in d.lower())

    def test_full_attainment_triggers_driver(self):
        drivers = _accuracy_drivers(make_rep(), 90.0, 100.0)
        assert any("100%" in d or "quota" in d.lower() for d in drivers)

    def test_attainment_below_100_no_attainment_driver(self):
        drivers = _accuracy_drivers(make_rep(), 90.0, 99.0)
        assert not any("quota" in d.lower() for d in drivers)

    def test_low_crm_lag_triggers_driver(self):
        inp = make_rep(crm_update_lag_days=1.0)
        drivers = _accuracy_drivers(inp, 90.0, 100.0)
        assert any("crm" in d.lower() or "lag" in d.lower() or "hygiène" in d.lower() for d in drivers)

    def test_high_crm_lag_no_crm_driver(self):
        inp = make_rep(crm_update_lag_days=5.0)
        drivers = _accuracy_drivers(inp, 90.0, 100.0)
        assert not any("hygiène" in d.lower() and "irréprochable" in d.lower() for d in drivers)

    def test_high_coverage_triggers_driver(self):
        inp = make_rep(pipeline_coverage_ratio=4.0)
        drivers = _accuracy_drivers(inp, 90.0, 100.0)
        assert any("pipeline" in d.lower() or "couverture" in d.lower() for d in drivers)

    def test_low_coverage_no_pipeline_driver(self):
        inp = make_rep(pipeline_coverage_ratio=2.0)
        drivers = _accuracy_drivers(inp, 90.0, 100.0)
        assert not any("couverture" in d.lower() for d in drivers)

    def test_no_sandbagging_no_pull_ins_triggers_driver(self):
        inp = make_rep(sandbagging_events=0, late_stage_pull_ins=0)
        drivers = _accuracy_drivers(inp, 90.0, 100.0)
        assert any("sandbagging" in d.lower() or "comportement" in d.lower() for d in drivers)

    def test_pull_ins_suppress_clean_driver(self):
        inp = make_rep(late_stage_pull_ins=2)
        drivers = _accuracy_drivers(inp, 90.0, 100.0)
        assert not any("sandbagging" in d.lower() and "pull-in" in d.lower() for d in drivers)

    def test_low_slip_triggers_driver(self):
        inp = make_rep(avg_deal_slip_days=3.0)
        drivers = _accuracy_drivers(inp, 90.0, 100.0)
        assert any("slip" in d.lower() or "glissant" in d.lower() for d in drivers)

    def test_high_slip_no_slip_driver(self):
        inp = make_rep(avg_deal_slip_days=10.0)
        drivers = _accuracy_drivers(inp, 90.0, 100.0)
        assert not any("glissant" in d.lower() for d in drivers)

    def test_many_periods_triggers_driver(self):
        inp = make_rep(periods=4)
        drivers = _accuracy_drivers(inp, 90.0, 100.0)
        assert any("trimestre" in d.lower() or "période" in d.lower() or "4" in d for d in drivers)

    def test_few_periods_no_period_driver(self):
        inp = make_rep(periods=2)
        drivers = _accuracy_drivers(inp, 90.0, 100.0)
        assert not any("trimestre" in d.lower() for d in drivers)

    def test_returns_list(self):
        inp = make_rep()
        result = _accuracy_drivers(inp, 90.0, 100.0)
        assert isinstance(result, list)


# ---------------------------------------------------------------------------
# Class 12 — _accuracy_gaps
# ---------------------------------------------------------------------------

class TestAccuracyGaps:
    def test_low_accuracy_triggers_gap(self):
        gaps = _accuracy_gaps(make_rep(), 70.0, 100.0, ForecastBias.NEUTRAL)
        assert any("précision" in g.lower() or "insuffisante" in g.lower() for g in gaps)

    def test_high_accuracy_no_accuracy_gap(self):
        gaps = _accuracy_gaps(make_rep(), 80.0, 100.0, ForecastBias.NEUTRAL)
        assert not any("insuffisante" in g.lower() for g in gaps)

    def test_optimistic_bias_triggers_gap(self):
        gaps = _accuracy_gaps(make_rep(), 80.0, 100.0, ForecastBias.OPTIMISTIC)
        assert any("optimiste" in g.lower() for g in gaps)

    def test_pessimistic_bias_triggers_gap(self):
        gaps = _accuracy_gaps(make_rep(), 80.0, 100.0, ForecastBias.PESSIMISTIC)
        assert any("pessimiste" in g.lower() for g in gaps)

    def test_neutral_bias_no_bias_gap(self):
        gaps = _accuracy_gaps(make_rep(), 80.0, 100.0, ForecastBias.NEUTRAL)
        assert not any("optimiste" in g.lower() or "pessimiste" in g.lower() for g in gaps)

    def test_high_crm_lag_triggers_gap(self):
        inp = make_rep(crm_update_lag_days=10.0)
        gaps = _accuracy_gaps(inp, 80.0, 100.0, ForecastBias.NEUTRAL)
        assert any("crm" in g.lower() or "lag" in g.lower() or "hygiène" in g.lower() for g in gaps)

    def test_low_crm_lag_no_crm_gap(self):
        inp = make_rep(crm_update_lag_days=3.0)
        gaps = _accuracy_gaps(inp, 80.0, 100.0, ForecastBias.NEUTRAL)
        assert not any("hygiène" in g.lower() for g in gaps)

    def test_low_pipeline_coverage_triggers_gap(self):
        inp = make_rep(pipeline_coverage_ratio=2.0)
        gaps = _accuracy_gaps(inp, 80.0, 100.0, ForecastBias.NEUTRAL)
        assert any("pipeline" in g.lower() or "couverture" in g.lower() for g in gaps)

    def test_high_pipeline_coverage_no_gap(self):
        inp = make_rep(pipeline_coverage_ratio=3.0)
        gaps = _accuracy_gaps(inp, 80.0, 100.0, ForecastBias.NEUTRAL)
        assert not any("sous-alimenté" in g.lower() for g in gaps)

    def test_many_pull_ins_triggers_gap(self):
        inp = make_rep(late_stage_pull_ins=3)
        gaps = _accuracy_gaps(inp, 80.0, 100.0, ForecastBias.NEUTRAL)
        assert any("pull" in g.lower() for g in gaps)

    def test_few_pull_ins_no_gap(self):
        inp = make_rep(late_stage_pull_ins=2)
        gaps = _accuracy_gaps(inp, 80.0, 100.0, ForecastBias.NEUTRAL)
        assert not any("pull-in" in g.lower() for g in gaps)

    def test_many_sandbagging_triggers_gap(self):
        inp = make_rep(sandbagging_events=2)
        gaps = _accuracy_gaps(inp, 80.0, 100.0, ForecastBias.NEUTRAL)
        assert any("sandbagging" in g.lower() for g in gaps)

    def test_few_sandbagging_no_gap(self):
        inp = make_rep(sandbagging_events=1)
        gaps = _accuracy_gaps(inp, 80.0, 100.0, ForecastBias.NEUTRAL)
        assert not any("sandbagging" in g.lower() for g in gaps)

    def test_heavy_slip_triggers_gap(self):
        inp = make_rep(avg_deal_slip_days=20.0)
        gaps = _accuracy_gaps(inp, 80.0, 100.0, ForecastBias.NEUTRAL)
        assert any("glissant" in g.lower() for g in gaps)

    def test_light_slip_no_slip_gap(self):
        inp = make_rep(avg_deal_slip_days=10.0)
        gaps = _accuracy_gaps(inp, 80.0, 100.0, ForecastBias.NEUTRAL)
        assert not any("glissant" in g.lower() for g in gaps)

    def test_low_attainment_triggers_gap(self):
        gaps = _accuracy_gaps(make_rep(), 80.0, 60.0, ForecastBias.NEUTRAL)
        assert any("attainment" in g.lower() or "performance" in g.lower() for g in gaps)

    def test_high_attainment_no_attainment_gap(self):
        gaps = _accuracy_gaps(make_rep(), 80.0, 80.0, ForecastBias.NEUTRAL)
        assert not any("attainment" in g.lower() for g in gaps)

    def test_returns_list(self):
        gaps = _accuracy_gaps(make_rep(), 80.0, 100.0, ForecastBias.NEUTRAL)
        assert isinstance(gaps, list)


# ---------------------------------------------------------------------------
# Class 13 — _coaching_recommendations
# ---------------------------------------------------------------------------

class TestCoachingRecommendations:
    def test_celebrate_returns_exactly_two_recs(self):
        recs = _coaching_recommendations(make_rep(), 95.0, 100.0, ForecastBias.NEUTRAL, ForecastAction.CELEBRATE)
        assert len(recs) == 2

    def test_celebrate_shares_practices(self):
        recs = _coaching_recommendations(make_rep(), 95.0, 100.0, ForecastBias.NEUTRAL, ForecastAction.CELEBRATE)
        assert any("pratique" in r.lower() or "standard" in r.lower() for r in recs)

    def test_celebrate_no_bias_recs(self):
        recs = _coaching_recommendations(make_rep(), 95.0, 100.0, ForecastBias.OPTIMISTIC, ForecastAction.CELEBRATE)
        # CELEBRATE exits early — no bias-based recs
        assert len(recs) == 2

    def test_optimistic_bias_triggers_commit_rec(self):
        recs = _coaching_recommendations(make_rep(), 70.0, 90.0, ForecastBias.OPTIMISTIC, ForecastAction.IMPROVE)
        assert any("commit" in r.lower() or "meddic" in r.lower() for r in recs)

    def test_pessimistic_bias_triggers_sandbagging_rec(self):
        recs = _coaching_recommendations(make_rep(), 70.0, 90.0, ForecastBias.PESSIMISTIC, ForecastAction.IMPROVE)
        assert any("sandbagging" in r.lower() or "calibration" in r.lower() for r in recs)

    def test_high_crm_lag_triggers_crm_rec(self):
        inp = make_rep(crm_update_lag_days=8.0)
        recs = _coaching_recommendations(inp, 70.0, 90.0, ForecastBias.NEUTRAL, ForecastAction.IMPROVE)
        assert any("crm" in r.lower() or "cadence" in r.lower() for r in recs)

    def test_low_crm_lag_no_crm_rec(self):
        inp = make_rep(crm_update_lag_days=2.0)
        recs = _coaching_recommendations(inp, 70.0, 90.0, ForecastBias.NEUTRAL, ForecastAction.IMPROVE)
        assert not any("cadence crm" in r.lower() for r in recs)

    def test_low_pipeline_triggers_pipeline_rec(self):
        inp = make_rep(pipeline_coverage_ratio=2.0)
        recs = _coaching_recommendations(inp, 70.0, 90.0, ForecastBias.NEUTRAL, ForecastAction.IMPROVE)
        assert any("pipeline" in r.lower() or "génération" in r.lower() for r in recs)

    def test_high_pipeline_no_pipeline_rec(self):
        inp = make_rep(pipeline_coverage_ratio=3.0)
        recs = _coaching_recommendations(inp, 70.0, 90.0, ForecastBias.NEUTRAL, ForecastAction.IMPROVE)
        assert not any("génération de pipeline" in r.lower() for r in recs)

    def test_many_pull_ins_triggers_pull_in_rec(self):
        inp = make_rep(late_stage_pull_ins=3)
        recs = _coaching_recommendations(inp, 70.0, 90.0, ForecastBias.NEUTRAL, ForecastAction.IMPROVE)
        assert any("pull-in" in r.lower() for r in recs)

    def test_few_pull_ins_no_pull_in_rec(self):
        inp = make_rep(late_stage_pull_ins=2)
        recs = _coaching_recommendations(inp, 70.0, 90.0, ForecastBias.NEUTRAL, ForecastAction.IMPROVE)
        assert not any("pull-in" in r.lower() for r in recs)

    def test_heavy_slip_triggers_slip_rec(self):
        inp = make_rep(avg_deal_slip_days=20.0)
        recs = _coaching_recommendations(inp, 70.0, 90.0, ForecastBias.NEUTRAL, ForecastAction.IMPROVE)
        assert any("close date" in r.lower() or "jalons" in r.lower() for r in recs)

    def test_light_slip_no_slip_rec(self):
        inp = make_rep(avg_deal_slip_days=5.0)
        recs = _coaching_recommendations(inp, 70.0, 90.0, ForecastBias.NEUTRAL, ForecastAction.IMPROVE)
        assert not any("close date" in r.lower() for r in recs)

    def test_low_attainment_triggers_plan_rec(self):
        recs = _coaching_recommendations(make_rep(), 70.0, 70.0, ForecastBias.NEUTRAL, ForecastAction.IMPROVE)
        assert any("90j" in r.lower() or "plan" in r.lower() for r in recs)

    def test_high_attainment_no_plan_rec(self):
        recs = _coaching_recommendations(make_rep(), 70.0, 85.0, ForecastBias.NEUTRAL, ForecastAction.IMPROVE)
        assert not any("90j" in r.lower() for r in recs)

    def test_overhaul_adds_overhaul_rec(self):
        recs = _coaching_recommendations(make_rep(), 40.0, 40.0, ForecastBias.NEUTRAL, ForecastAction.OVERHAUL)
        assert any("revops" in r.lower() or "révision" in r.lower() for r in recs)

    def test_non_overhaul_no_overhaul_rec(self):
        recs = _coaching_recommendations(make_rep(), 70.0, 90.0, ForecastBias.NEUTRAL, ForecastAction.IMPROVE)
        assert not any("revops" in r.lower() for r in recs)

    def test_returns_list(self):
        recs = _coaching_recommendations(make_rep(), 90.0, 100.0, ForecastBias.NEUTRAL, ForecastAction.CELEBRATE)
        assert isinstance(recs, list)


# ---------------------------------------------------------------------------
# Class 14 — ForecastResult structure
# ---------------------------------------------------------------------------

class TestForecastResult:
    @pytest.fixture
    def result(self):
        engine = ForecastAccuracyEngine()
        return engine.analyze(make_rep())

    def test_is_dataclass_instance(self, result):
        assert isinstance(result, ForecastResult)

    def test_has_rep_id(self, result):
        assert result.rep_id == "REP001"

    def test_has_rep_name(self, result):
        assert result.rep_name == "Alice Dupont"

    def test_has_region(self, result):
        assert result.region == "EMEA"

    def test_has_segment(self, result):
        assert result.segment == "enterprise"

    def test_accuracy_pct_is_float(self, result):
        assert isinstance(result.accuracy_pct, (int, float))

    def test_accuracy_tier_is_enum(self, result):
        assert isinstance(result.accuracy_tier, ForecastAccuracy)

    def test_bias_is_enum(self, result):
        assert isinstance(result.bias, ForecastBias)

    def test_forecast_action_is_enum(self, result):
        assert isinstance(result.forecast_action, ForecastAction)

    def test_rep_tier_is_enum(self, result):
        assert isinstance(result.rep_tier, RepTier)

    def test_attainment_pct_is_float(self, result):
        assert isinstance(result.attainment_pct, (int, float))

    def test_variance_eur_is_numeric(self, result):
        assert isinstance(result.variance_eur, (int, float))

    def test_accuracy_drivers_is_list(self, result):
        assert isinstance(result.accuracy_drivers, list)

    def test_accuracy_gaps_is_list(self, result):
        assert isinstance(result.accuracy_gaps, list)

    def test_coaching_recommendations_is_list(self, result):
        assert isinstance(result.coaching_recommendations, list)

    def test_reliability_score_is_float(self, result):
        assert isinstance(result.reliability_score, (int, float))

    def test_reliability_score_in_range(self, result):
        assert 0.0 <= result.reliability_score <= 100.0


# ---------------------------------------------------------------------------
# Class 15 — ForecastResult.to_dict
# ---------------------------------------------------------------------------

class TestForecastResultToDict:
    @pytest.fixture
    def d(self):
        engine = ForecastAccuracyEngine()
        result = engine.analyze(make_rep())
        return result.to_dict()

    def test_returns_dict(self, d):
        assert isinstance(d, dict)

    def test_has_all_keys(self, d):
        expected_keys = {
            "rep_id", "rep_name", "region", "segment",
            "accuracy_pct", "accuracy_tier", "bias",
            "forecast_action", "rep_tier", "attainment_pct",
            "variance_eur", "accuracy_drivers", "accuracy_gaps",
            "coaching_recommendations", "reliability_score",
        }
        assert set(d.keys()) == expected_keys

    def test_enum_values_are_strings(self, d):
        assert isinstance(d["accuracy_tier"], str)
        assert isinstance(d["bias"], str)
        assert isinstance(d["forecast_action"], str)
        assert isinstance(d["rep_tier"], str)

    def test_accuracy_tier_value_matches(self, d):
        assert d["accuracy_tier"] in {"excellent", "good", "fair", "poor"}

    def test_bias_value_matches(self, d):
        assert d["bias"] in {"optimistic", "neutral", "pessimistic"}

    def test_rep_id_correct(self, d):
        assert d["rep_id"] == "REP001"

    def test_lists_serialized_as_lists(self, d):
        assert isinstance(d["accuracy_drivers"], list)
        assert isinstance(d["accuracy_gaps"], list)
        assert isinstance(d["coaching_recommendations"], list)


# ---------------------------------------------------------------------------
# Class 16 — ForecastAccuracyEngine.analyze
# ---------------------------------------------------------------------------

class TestEngineAnalyze:
    def test_returns_forecast_result(self):
        engine = ForecastAccuracyEngine()
        result = engine.analyze(make_rep())
        assert isinstance(result, ForecastResult)

    def test_stores_result_by_rep_id(self):
        engine = ForecastAccuracyEngine()
        engine.analyze(make_rep(rep_id="X01"))
        assert len(engine.all_reps()) == 1

    def test_overwrite_same_rep_id(self):
        engine = ForecastAccuracyEngine()
        engine.analyze(make_rep(rep_id="X01", total_actual_eur=80_000))
        engine.analyze(make_rep(rep_id="X01", total_actual_eur=95_000))
        reps = engine.all_reps()
        assert len(reps) == 1
        assert reps[0].attainment_pct == 95.0

    def test_excellent_accuracy_scenario(self):
        inp = make_rep(total_committed_eur=100_000, total_actual_eur=93_000)
        engine = ForecastAccuracyEngine()
        result = engine.analyze(inp)
        assert result.accuracy_tier == ForecastAccuracy.EXCELLENT
        assert result.forecast_action == ForecastAction.CELEBRATE

    def test_good_accuracy_scenario(self):
        inp = make_rep(total_committed_eur=100_000, total_actual_eur=80_000)
        engine = ForecastAccuracyEngine()
        result = engine.analyze(inp)
        assert result.accuracy_tier == ForecastAccuracy.GOOD
        assert result.forecast_action == ForecastAction.CALIBRATE

    def test_fair_accuracy_scenario(self):
        inp = make_rep(total_committed_eur=100_000, total_actual_eur=60_000)
        engine = ForecastAccuracyEngine()
        result = engine.analyze(inp)
        assert result.accuracy_tier == ForecastAccuracy.FAIR
        assert result.forecast_action == ForecastAction.IMPROVE

    def test_poor_accuracy_scenario(self):
        inp = make_rep(total_committed_eur=100_000, total_actual_eur=40_000)
        engine = ForecastAccuracyEngine()
        result = engine.analyze(inp)
        assert result.accuracy_tier == ForecastAccuracy.POOR
        assert result.forecast_action == ForecastAction.OVERHAUL

    def test_variance_is_actual_minus_committed(self):
        inp = make_rep(total_committed_eur=100_000, total_actual_eur=110_000)
        engine = ForecastAccuracyEngine()
        result = engine.analyze(inp)
        assert result.variance_eur == 10_000.0

    def test_default_rep_is_neutral_good(self):
        engine = ForecastAccuracyEngine()
        result = engine.analyze(make_rep())
        assert result.bias == ForecastBias.NEUTRAL
        assert result.accuracy_tier in {ForecastAccuracy.EXCELLENT, ForecastAccuracy.GOOD}


# ---------------------------------------------------------------------------
# Class 17 — ForecastAccuracyEngine.analyze_batch
# ---------------------------------------------------------------------------

class TestEngineAnalyzeBatch:
    def test_returns_list(self):
        engine = ForecastAccuracyEngine()
        results = engine.analyze_batch([make_rep()])
        assert isinstance(results, list)

    def test_length_matches_input(self):
        engine = ForecastAccuracyEngine()
        reps = [make_rep(rep_id=f"R{i}") for i in range(5)]
        results = engine.analyze_batch(reps)
        assert len(results) == 5

    def test_sorted_descending_by_accuracy(self):
        engine = ForecastAccuracyEngine()
        reps = [
            make_rep(rep_id="A", total_actual_eur=60_000),   # 60% accuracy
            make_rep(rep_id="B", total_actual_eur=95_000),   # 95% accuracy
            make_rep(rep_id="C", total_actual_eur=80_000),   # 80% accuracy
        ]
        results = engine.analyze_batch(reps)
        accuracies = [r.accuracy_pct for r in results]
        assert accuracies == sorted(accuracies, reverse=True)

    def test_all_results_stored_in_engine(self):
        engine = ForecastAccuracyEngine()
        reps = [make_rep(rep_id=f"R{i}") for i in range(3)]
        engine.analyze_batch(reps)
        assert len(engine.all_reps()) == 3

    def test_empty_batch_returns_empty_list(self):
        engine = ForecastAccuracyEngine()
        results = engine.analyze_batch([])
        assert results == []


# ---------------------------------------------------------------------------
# Class 18 — Engine query/filter methods
# ---------------------------------------------------------------------------

class TestEngineQueryMethods:
    @pytest.fixture
    def populated_engine(self):
        engine = ForecastAccuracyEngine()
        # EXCELLENT (95%)
        engine.analyze(make_rep(rep_id="E1", total_actual_eur=95_000, quota_eur=100_000))
        # GOOD (80%)
        engine.analyze(make_rep(rep_id="G1", total_actual_eur=80_000, quota_eur=100_000))
        # FAIR (60%)
        engine.analyze(make_rep(rep_id="F1", total_actual_eur=60_000, quota_eur=100_000))
        # POOR (40%)
        engine.analyze(make_rep(rep_id="P1", total_actual_eur=40_000, quota_eur=100_000))
        # Optimistic (85_000 actual on 100_000 committed = -15% → OPTIMISTIC)
        engine.analyze(make_rep(rep_id="OPT1", total_actual_eur=85_000, total_committed_eur=100_000))
        # Pessimistic (120_000 actual on 100_000 committed = +20% → PESSIMISTIC)
        engine.analyze(make_rep(rep_id="PES1", total_actual_eur=120_000, total_committed_eur=100_000))
        return engine

    def test_all_reps_returns_all(self, populated_engine):
        assert len(populated_engine.all_reps()) == 6

    def test_all_reps_sorted_descending(self, populated_engine):
        reps = populated_engine.all_reps()
        accuracies = [r.accuracy_pct for r in reps]
        assert accuracies == sorted(accuracies, reverse=True)

    def test_by_accuracy_excellent(self, populated_engine):
        results = populated_engine.by_accuracy(ForecastAccuracy.EXCELLENT)
        assert all(r.accuracy_tier == ForecastAccuracy.EXCELLENT for r in results)

    def test_by_accuracy_poor(self, populated_engine):
        results = populated_engine.by_accuracy(ForecastAccuracy.POOR)
        assert all(r.accuracy_tier == ForecastAccuracy.POOR for r in results)

    def test_by_action_celebrate(self, populated_engine):
        results = populated_engine.by_action(ForecastAction.CELEBRATE)
        assert all(r.forecast_action == ForecastAction.CELEBRATE for r in results)

    def test_by_action_overhaul(self, populated_engine):
        results = populated_engine.by_action(ForecastAction.OVERHAUL)
        assert all(r.forecast_action == ForecastAction.OVERHAUL for r in results)

    def test_by_bias_optimistic(self, populated_engine):
        results = populated_engine.by_bias(ForecastBias.OPTIMISTIC)
        assert all(r.bias == ForecastBias.OPTIMISTIC for r in results)
        assert len(results) >= 1

    def test_by_bias_pessimistic(self, populated_engine):
        results = populated_engine.by_bias(ForecastBias.PESSIMISTIC)
        assert all(r.bias == ForecastBias.PESSIMISTIC for r in results)
        assert len(results) >= 1

    def test_by_rep_tier_returns_correct_tier(self, populated_engine):
        for tier in RepTier:
            results = populated_engine.by_rep_tier(tier)
            assert all(r.rep_tier == tier for r in results)

    def test_excellent_forecasters_convenience(self, populated_engine):
        assert populated_engine.excellent_forecasters() == populated_engine.by_accuracy(ForecastAccuracy.EXCELLENT)

    def test_needs_overhaul_convenience(self, populated_engine):
        assert populated_engine.needs_overhaul() == populated_engine.by_action(ForecastAction.OVERHAUL)

    def test_optimistic_reps_convenience(self, populated_engine):
        assert populated_engine.optimistic_reps() == populated_engine.by_bias(ForecastBias.OPTIMISTIC)

    def test_sandbagging_reps_convenience(self, populated_engine):
        assert populated_engine.sandbagging_reps() == populated_engine.by_bias(ForecastBias.PESSIMISTIC)

    def test_top_performers_convenience(self, populated_engine):
        assert populated_engine.top_performers() == populated_engine.by_rep_tier(RepTier.TOP)

    def test_empty_engine_all_reps(self):
        engine = ForecastAccuracyEngine()
        assert engine.all_reps() == []

    def test_empty_engine_by_accuracy(self):
        engine = ForecastAccuracyEngine()
        assert engine.by_accuracy(ForecastAccuracy.EXCELLENT) == []

    def test_empty_engine_excellent_forecasters(self):
        engine = ForecastAccuracyEngine()
        assert engine.excellent_forecasters() == []


# ---------------------------------------------------------------------------
# Class 19 — Engine aggregate statistics
# ---------------------------------------------------------------------------

class TestEngineAggregates:
    @pytest.fixture
    def engine_two_reps(self):
        engine = ForecastAccuracyEngine()
        engine.analyze(make_rep(rep_id="R1", total_actual_eur=95_000, quota_eur=100_000))
        engine.analyze(make_rep(rep_id="R2", total_actual_eur=80_000, quota_eur=100_000))
        return engine

    def test_avg_accuracy_returns_float(self, engine_two_reps):
        result = engine_two_reps.avg_accuracy()
        assert isinstance(result, (int, float))

    def test_avg_accuracy_empty_engine(self):
        assert ForecastAccuracyEngine().avg_accuracy() == 0.0

    def test_avg_attainment_returns_float(self, engine_two_reps):
        result = engine_two_reps.avg_attainment()
        assert isinstance(result, (int, float))

    def test_avg_attainment_empty_engine(self):
        assert ForecastAccuracyEngine().avg_attainment() == 0.0

    def test_avg_reliability_returns_float(self, engine_two_reps):
        result = engine_two_reps.avg_reliability()
        assert isinstance(result, (int, float))

    def test_avg_reliability_empty_engine(self):
        assert ForecastAccuracyEngine().avg_reliability() == 0.0

    def test_total_variance_eur(self):
        engine = ForecastAccuracyEngine()
        engine.analyze(make_rep(rep_id="R1", total_committed_eur=100_000, total_actual_eur=110_000))
        engine.analyze(make_rep(rep_id="R2", total_committed_eur=100_000, total_actual_eur=90_000))
        assert engine.total_variance_eur() == 0.0  # +10k and -10k

    def test_total_variance_eur_empty(self):
        assert ForecastAccuracyEngine().total_variance_eur() == 0.0

    def test_avg_accuracy_correct_value(self, engine_two_reps):
        reps = engine_two_reps.all_reps()
        expected = round(sum(r.accuracy_pct for r in reps) / len(reps), 1)
        assert engine_two_reps.avg_accuracy() == expected

    def test_avg_attainment_correct_value(self):
        engine = ForecastAccuracyEngine()
        engine.analyze(make_rep(rep_id="R1", total_actual_eur=100_000, quota_eur=100_000))
        engine.analyze(make_rep(rep_id="R2", total_actual_eur=80_000, quota_eur=100_000))
        assert engine.avg_attainment() == 90.0

    def test_avg_reliability_in_range(self, engine_two_reps):
        score = engine_two_reps.avg_reliability()
        assert 0.0 <= score <= 100.0


# ---------------------------------------------------------------------------
# Class 20 — Engine.summary
# ---------------------------------------------------------------------------

class TestEngineSummary:
    @pytest.fixture
    def engine(self):
        e = ForecastAccuracyEngine()
        e.analyze(make_rep(rep_id="R1", total_actual_eur=95_000))
        e.analyze(make_rep(rep_id="R2", total_actual_eur=60_000))
        return e

    def test_returns_dict(self, engine):
        assert isinstance(engine.summary(), dict)

    def test_total_key(self, engine):
        assert engine.summary()["total"] == 2

    def test_accuracy_counts_key(self, engine):
        s = engine.summary()
        assert "accuracy_counts" in s
        assert isinstance(s["accuracy_counts"], dict)

    def test_accuracy_counts_all_tiers_present(self, engine):
        counts = engine.summary()["accuracy_counts"]
        for tier in ForecastAccuracy:
            assert tier.value in counts

    def test_action_counts_key(self, engine):
        s = engine.summary()
        assert "action_counts" in s
        for action in ForecastAction:
            assert action.value in s["action_counts"]

    def test_bias_counts_key(self, engine):
        s = engine.summary()
        assert "bias_counts" in s
        for bias in ForecastBias:
            assert bias.value in s["bias_counts"]

    def test_avg_accuracy_pct_key(self, engine):
        s = engine.summary()
        assert "avg_accuracy_pct" in s
        assert isinstance(s["avg_accuracy_pct"], (int, float))

    def test_avg_attainment_pct_key(self, engine):
        s = engine.summary()
        assert "avg_attainment_pct" in s

    def test_avg_reliability_score_key(self, engine):
        s = engine.summary()
        assert "avg_reliability_score" in s

    def test_excellent_count_key(self, engine):
        s = engine.summary()
        assert "excellent_count" in s
        assert isinstance(s["excellent_count"], int)

    def test_overhaul_count_key(self, engine):
        s = engine.summary()
        assert "overhaul_count" in s

    def test_total_variance_eur_key(self, engine):
        s = engine.summary()
        assert "total_variance_eur" in s

    def test_accuracy_counts_sum_to_total(self, engine):
        s = engine.summary()
        total = sum(s["accuracy_counts"].values())
        assert total == s["total"]

    def test_action_counts_sum_to_total(self, engine):
        s = engine.summary()
        total = sum(s["action_counts"].values())
        assert total == s["total"]

    def test_bias_counts_sum_to_total(self, engine):
        s = engine.summary()
        total = sum(s["bias_counts"].values())
        assert total == s["total"]

    def test_empty_engine_summary_total_zero(self):
        s = ForecastAccuracyEngine().summary()
        assert s["total"] == 0


# ---------------------------------------------------------------------------
# Class 21 — Engine.reset
# ---------------------------------------------------------------------------

class TestEngineReset:
    def test_reset_clears_all_results(self):
        engine = ForecastAccuracyEngine()
        engine.analyze(make_rep(rep_id="R1"))
        engine.analyze(make_rep(rep_id="R2"))
        engine.reset()
        assert engine.all_reps() == []

    def test_reset_zeros_avg_accuracy(self):
        engine = ForecastAccuracyEngine()
        engine.analyze(make_rep())
        engine.reset()
        assert engine.avg_accuracy() == 0.0

    def test_reset_zeros_avg_attainment(self):
        engine = ForecastAccuracyEngine()
        engine.analyze(make_rep())
        engine.reset()
        assert engine.avg_attainment() == 0.0

    def test_reset_zeros_avg_reliability(self):
        engine = ForecastAccuracyEngine()
        engine.analyze(make_rep())
        engine.reset()
        assert engine.avg_reliability() == 0.0

    def test_reset_zeros_total_variance(self):
        engine = ForecastAccuracyEngine()
        engine.analyze(make_rep())
        engine.reset()
        assert engine.total_variance_eur() == 0.0

    def test_can_reuse_after_reset(self):
        engine = ForecastAccuracyEngine()
        engine.analyze(make_rep(rep_id="R1"))
        engine.reset()
        engine.analyze(make_rep(rep_id="R2"))
        assert len(engine.all_reps()) == 1

    def test_reset_is_idempotent(self):
        engine = ForecastAccuracyEngine()
        engine.reset()
        engine.reset()
        assert engine.all_reps() == []


# ---------------------------------------------------------------------------
# Class 22 — Integration / end-to-end scenarios
# ---------------------------------------------------------------------------

class TestIntegrationScenarios:
    def test_star_rep_full_pipeline(self):
        """Top performer: high accuracy + attainment, clean behaviour."""
        engine = ForecastAccuracyEngine()
        inp = make_rep(
            rep_id="STAR",
            total_committed_eur=200_000,
            total_actual_eur=205_000,
            crm_update_lag_days=0.5,
            pipeline_coverage_ratio=4.5,
            late_stage_pull_ins=0,
            sandbagging_events=0,
            avg_deal_slip_days=2.0,
            quota_eur=200_000,
            periods=6,
        )
        result = engine.analyze(inp)
        assert result.accuracy_tier == ForecastAccuracy.EXCELLENT
        assert result.rep_tier == RepTier.TOP
        assert result.forecast_action == ForecastAction.CELEBRATE
        assert result.reliability_score > 70.0

    def test_struggling_rep_full_pipeline(self):
        """Struggling rep: low accuracy, low attainment, poor CRM hygiene."""
        engine = ForecastAccuracyEngine()
        inp = make_rep(
            rep_id="STRUGGLE",
            total_committed_eur=100_000,
            total_actual_eur=40_000,
            crm_update_lag_days=12.0,
            pipeline_coverage_ratio=1.0,
            late_stage_pull_ins=5,
            sandbagging_events=3,
            avg_deal_slip_days=20.0,
            quota_eur=100_000,
        )
        result = engine.analyze(inp)
        assert result.accuracy_tier == ForecastAccuracy.POOR
        assert result.rep_tier == RepTier.STRUGGLING
        assert result.forecast_action == ForecastAction.OVERHAUL
        assert result.bias == ForecastBias.OPTIMISTIC
        assert len(result.coaching_recommendations) >= 3

    def test_sandbagging_rep(self):
        """Pessimistic bias rep who consistently beats forecast."""
        engine = ForecastAccuracyEngine()
        inp = make_rep(
            rep_id="SAND",
            total_committed_eur=100_000,
            total_actual_eur=130_000,
            quota_eur=100_000,
        )
        result = engine.analyze(inp)
        assert result.bias == ForecastBias.PESSIMISTIC
        assert result in engine.sandbagging_reps()

    def test_optimistic_rep(self):
        """Optimistic bias rep who misses forecast by >10%."""
        engine = ForecastAccuracyEngine()
        inp = make_rep(
            rep_id="OPT",
            total_committed_eur=100_000,
            total_actual_eur=80_000,
            quota_eur=100_000,
        )
        result = engine.analyze(inp)
        assert result.bias == ForecastBias.OPTIMISTIC
        assert result in engine.optimistic_reps()

    def test_batch_then_filter(self):
        """Batch analyze then filter for excellent."""
        engine = ForecastAccuracyEngine()
        reps = [
            make_rep(rep_id="E1", total_actual_eur=95_000),
            make_rep(rep_id="E2", total_actual_eur=92_000),
            make_rep(rep_id="G1", total_actual_eur=80_000),
            make_rep(rep_id="P1", total_actual_eur=40_000),
        ]
        engine.analyze_batch(reps)
        excellent = engine.excellent_forecasters()
        assert len(excellent) >= 2
        assert all(r.accuracy_pct >= 90.0 for r in excellent)

    def test_overhaul_in_needs_overhaul(self):
        engine = ForecastAccuracyEngine()
        engine.analyze(make_rep(rep_id="POOR", total_actual_eur=40_000))
        assert len(engine.needs_overhaul()) >= 1

    def test_summary_after_batch(self):
        engine = ForecastAccuracyEngine()
        reps = [make_rep(rep_id=f"R{i}", total_actual_eur=100_000 - i * 10_000) for i in range(5)]
        engine.analyze_batch(reps)
        s = engine.summary()
        assert s["total"] == 5
        assert sum(s["accuracy_counts"].values()) == 5

    def test_multiple_engines_are_independent(self):
        e1 = ForecastAccuracyEngine()
        e2 = ForecastAccuracyEngine()
        e1.analyze(make_rep(rep_id="R1"))
        assert len(e2.all_reps()) == 0

    def test_result_rep_id_matches_input(self):
        engine = ForecastAccuracyEngine()
        result = engine.analyze(make_rep(rep_id="UNIQUE123"))
        assert result.rep_id == "UNIQUE123"

    def test_to_dict_round_trip_accuracy_pct(self):
        engine = ForecastAccuracyEngine()
        result = engine.analyze(make_rep())
        d = result.to_dict()
        assert d["accuracy_pct"] == result.accuracy_pct

    def test_reliability_score_bounded_all_scenarios(self):
        engine = ForecastAccuracyEngine()
        scenarios = [
            make_rep(rep_id="S1", crm_update_lag_days=0.1, pipeline_coverage_ratio=5.0),
            make_rep(rep_id="S2", crm_update_lag_days=15.0, pipeline_coverage_ratio=0.5,
                     late_stage_pull_ins=5, sandbagging_events=4, avg_deal_slip_days=25.0),
        ]
        for inp in scenarios:
            r = engine.analyze(inp)
            assert 0.0 <= r.reliability_score <= 100.0

    def test_avg_stats_update_after_each_analyze(self):
        engine = ForecastAccuracyEngine()
        engine.analyze(make_rep(rep_id="R1", total_actual_eur=100_000, quota_eur=100_000))
        acc1 = engine.avg_accuracy()
        engine.analyze(make_rep(rep_id="R2", total_actual_eur=60_000, quota_eur=100_000))
        acc2 = engine.avg_accuracy()
        # Adding a rep with lower accuracy should reduce the average
        assert acc2 <= acc1
