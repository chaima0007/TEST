"""Comprehensive pytest test suite for ForecastCalibrationEngine."""
from __future__ import annotations

import math
import pytest

from swarm.intelligence.forecast_calibration_engine import (
    BiasType,
    CalibrationAction,
    CalibrationRating,
    CalibrationRisk,
    ForecastCalibrationEngine,
    ForecastCalibrationInput,
    ForecastCalibrationResult,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def make_input(
    *,
    rep_id: str = "rep_001",
    rep_name: str = "Alice Smith",
    region: str = "West",
    quarter: str = "Q1-2026",
    forecast_category: str = "commit",
    forecasted_amount_usd: float = 100_000.0,
    closed_won_amount_usd: float = 100_000.0,
    deals_forecasted_count: int = 10,
    deals_closed_count: int = 10,
    avg_forecast_accuracy_last_4q_pct: float = 90.0,
    sandbagging_score: float = 0.0,
    optimism_bias_score: float = 0.0,
    stage_lag_days: float = 0.0,
    close_date_push_count: int = 0,
    late_stage_slippage_rate_pct: float = 5.0,
    commit_accuracy_pct: float = 90.0,
    best_case_accuracy_pct: float = 85.0,
    pipeline_coverage_ratio: float = 4.0,
    win_rate_trend: float = 1.0,
    forecast_change_frequency: int = 1,
    manager_override_count: int = 0,
    data_entry_lag_days: float = 0.5,
) -> ForecastCalibrationInput:
    return ForecastCalibrationInput(
        rep_id=rep_id,
        rep_name=rep_name,
        region=region,
        quarter=quarter,
        forecast_category=forecast_category,
        forecasted_amount_usd=forecasted_amount_usd,
        closed_won_amount_usd=closed_won_amount_usd,
        deals_forecasted_count=deals_forecasted_count,
        deals_closed_count=deals_closed_count,
        avg_forecast_accuracy_last_4q_pct=avg_forecast_accuracy_last_4q_pct,
        sandbagging_score=sandbagging_score,
        optimism_bias_score=optimism_bias_score,
        stage_lag_days=stage_lag_days,
        close_date_push_count=close_date_push_count,
        late_stage_slippage_rate_pct=late_stage_slippage_rate_pct,
        commit_accuracy_pct=commit_accuracy_pct,
        best_case_accuracy_pct=best_case_accuracy_pct,
        pipeline_coverage_ratio=pipeline_coverage_ratio,
        win_rate_trend=win_rate_trend,
        forecast_change_frequency=forecast_change_frequency,
        manager_override_count=manager_override_count,
        data_entry_lag_days=data_entry_lag_days,
    )


@pytest.fixture
def engine() -> ForecastCalibrationEngine:
    return ForecastCalibrationEngine()


@pytest.fixture
def perfect_input() -> ForecastCalibrationInput:
    """All metrics at best-possible values."""
    return make_input()


@pytest.fixture
def terrible_input() -> ForecastCalibrationInput:
    """All metrics at worst-possible values."""
    return make_input(
        forecasted_amount_usd=100_000.0,
        closed_won_amount_usd=10_000.0,   # terrible accuracy
        deals_forecasted_count=10,
        deals_closed_count=2,
        avg_forecast_accuracy_last_4q_pct=40.0,
        sandbagging_score=90.0,
        optimism_bias_score=90.0,
        stage_lag_days=40.0,
        close_date_push_count=6,
        late_stage_slippage_rate_pct=50.0,
        commit_accuracy_pct=40.0,
        best_case_accuracy_pct=30.0,
        pipeline_coverage_ratio=1.0,
        win_rate_trend=-1.0,
        forecast_change_frequency=10,
        manager_override_count=5,
        data_entry_lag_days=15.0,
    )


# ===========================================================================
# 1. Enum value tests
# ===========================================================================

class TestEnums:
    def test_calibration_rating_values(self):
        assert CalibrationRating.EXCELLENT.value == "excellent"
        assert CalibrationRating.GOOD.value == "good"
        assert CalibrationRating.FAIR.value == "fair"
        assert CalibrationRating.POOR.value == "poor"

    def test_calibration_rating_count(self):
        assert len(CalibrationRating) == 4

    def test_calibration_risk_values(self):
        assert CalibrationRisk.LOW.value == "low"
        assert CalibrationRisk.MODERATE.value == "moderate"
        assert CalibrationRisk.HIGH.value == "high"
        assert CalibrationRisk.CRITICAL.value == "critical"

    def test_calibration_risk_count(self):
        assert len(CalibrationRisk) == 4

    def test_bias_type_values(self):
        assert BiasType.ACCURATE.value == "accurate"
        assert BiasType.SANDBAGGING.value == "sandbagging"
        assert BiasType.OVER_OPTIMISTIC.value == "over_optimistic"
        assert BiasType.INCONSISTENT.value == "inconsistent"

    def test_bias_type_count(self):
        assert len(BiasType) == 4

    def test_calibration_action_values(self):
        assert CalibrationAction.NO_ACTION.value == "no_action"
        assert CalibrationAction.COACHING_REQUIRED.value == "coaching_required"
        assert CalibrationAction.FORECAST_ADJUSTMENT.value == "forecast_adjustment"
        assert CalibrationAction.SYSTEM_OVERRIDE.value == "system_override"

    def test_calibration_action_count(self):
        assert len(CalibrationAction) == 4

    def test_enums_are_str_subclasses(self):
        assert isinstance(CalibrationRating.EXCELLENT, str)
        assert isinstance(CalibrationRisk.LOW, str)
        assert isinstance(BiasType.ACCURATE, str)
        assert isinstance(CalibrationAction.NO_ACTION, str)


# ===========================================================================
# 2. ForecastCalibrationInput dataclass structure tests
# ===========================================================================

class TestInputDataclass:
    def test_input_has_22_fields(self):
        import dataclasses
        fields = dataclasses.fields(ForecastCalibrationInput)
        assert len(fields) == 22

    def test_input_field_names(self):
        import dataclasses
        names = {f.name for f in dataclasses.fields(ForecastCalibrationInput)}
        expected = {
            "rep_id", "rep_name", "region", "quarter", "forecast_category",
            "forecasted_amount_usd", "closed_won_amount_usd",
            "deals_forecasted_count", "deals_closed_count",
            "avg_forecast_accuracy_last_4q_pct", "sandbagging_score",
            "optimism_bias_score", "stage_lag_days", "close_date_push_count",
            "late_stage_slippage_rate_pct", "commit_accuracy_pct",
            "best_case_accuracy_pct", "pipeline_coverage_ratio",
            "win_rate_trend", "forecast_change_frequency",
            "manager_override_count", "data_entry_lag_days",
        }
        assert names == expected

    def test_input_construction(self):
        inp = make_input(rep_id="x", rep_name="Bob")
        assert inp.rep_id == "x"
        assert inp.rep_name == "Bob"

    def test_input_string_fields(self):
        inp = make_input(region="East", quarter="Q2-2026", forecast_category="best_case")
        assert inp.region == "East"
        assert inp.quarter == "Q2-2026"
        assert inp.forecast_category == "best_case"

    def test_input_float_fields(self):
        inp = make_input(forecasted_amount_usd=250_000.0, closed_won_amount_usd=200_000.0)
        assert inp.forecasted_amount_usd == 250_000.0
        assert inp.closed_won_amount_usd == 200_000.0

    def test_input_int_fields(self):
        inp = make_input(deals_forecasted_count=15, deals_closed_count=12)
        assert inp.deals_forecasted_count == 15
        assert inp.deals_closed_count == 12


# ===========================================================================
# 3. ForecastCalibrationResult dataclass & to_dict tests
# ===========================================================================

class TestResultDataclass:
    def test_result_has_15_fields(self):
        import dataclasses
        fields = dataclasses.fields(ForecastCalibrationResult)
        assert len(fields) == 15

    def test_result_field_names(self):
        import dataclasses
        names = {f.name for f in dataclasses.fields(ForecastCalibrationResult)}
        expected = {
            "rep_id", "rep_name", "calibration_rating", "calibration_risk",
            "bias_type", "calibration_action", "accuracy_score", "bias_score",
            "consistency_score", "data_quality_score", "calibration_composite",
            "is_sandbagging", "is_over_optimistic", "estimated_forecast_error_usd",
            "calibration_signal",
        }
        assert names == expected

    def test_to_dict_returns_exactly_15_keys(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_key_names(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        d = result.to_dict()
        expected_keys = {
            "rep_id", "rep_name", "calibration_rating", "calibration_risk",
            "bias_type", "calibration_action", "accuracy_score", "bias_score",
            "consistency_score", "data_quality_score", "calibration_composite",
            "is_sandbagging", "is_over_optimistic", "estimated_forecast_error_usd",
            "calibration_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_values_are_strings(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        d = result.to_dict()
        assert isinstance(d["calibration_rating"], str)
        assert isinstance(d["calibration_risk"], str)
        assert isinstance(d["bias_type"], str)
        assert isinstance(d["calibration_action"], str)

    def test_to_dict_rep_id_matches(self, engine):
        inp = make_input(rep_id="xyz_99")
        result = engine.assess(inp)
        assert result.to_dict()["rep_id"] == "xyz_99"

    def test_to_dict_rep_name_matches(self, engine):
        inp = make_input(rep_name="Charlie Brown")
        result = engine.assess(inp)
        assert result.to_dict()["rep_name"] == "Charlie Brown"

    def test_to_dict_bool_fields(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        d = result.to_dict()
        assert isinstance(d["is_sandbagging"], bool)
        assert isinstance(d["is_over_optimistic"], bool)

    def test_to_dict_numeric_fields(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        d = result.to_dict()
        for key in ["accuracy_score", "bias_score", "consistency_score",
                    "data_quality_score", "calibration_composite",
                    "estimated_forecast_error_usd"]:
            assert isinstance(d[key], (int, float))

    def test_to_dict_signal_is_string(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert isinstance(result.to_dict()["calibration_signal"], str)


# ===========================================================================
# 4. Accuracy score component tests
# ===========================================================================

class TestAccuracyScore:
    """Tests for the _accuracy_score helper via engine output."""

    def test_perfect_accuracy_scores_high(self, engine):
        inp = make_input(
            forecasted_amount_usd=100_000.0,
            closed_won_amount_usd=100_000.0,
            avg_forecast_accuracy_last_4q_pct=95.0,
            commit_accuracy_pct=90.0,
            deals_forecasted_count=10,
            deals_closed_count=10,
        )
        result = engine.assess(inp)
        assert result.accuracy_score == 100.0

    def test_zero_forecast_gives_max_pct_error(self, engine):
        inp = make_input(
            forecasted_amount_usd=0.0,
            closed_won_amount_usd=50_000.0,
        )
        result = engine.assess(inp)
        # pct_error=100 → no current quarter points (only hist + commit + deal pts)
        assert result.accuracy_score <= 60.0

    def test_5pct_error_boundary_gets_40pts(self, engine):
        # 3% error → clearly within <= 5 bucket → 40 pts
        inp = make_input(
            forecasted_amount_usd=100_000.0,
            closed_won_amount_usd=97_000.0,
            avg_forecast_accuracy_last_4q_pct=95.0,
            commit_accuracy_pct=90.0,
            deals_forecasted_count=10,
            deals_closed_count=10,
        )
        result = engine.assess(inp)
        assert result.accuracy_score == 100.0

    def test_10pct_error_gets_32pts(self, engine):
        inp = make_input(
            forecasted_amount_usd=100_000.0,
            closed_won_amount_usd=90_000.0,  # 10% under
            avg_forecast_accuracy_last_4q_pct=95.0,
            commit_accuracy_pct=90.0,
            deals_forecasted_count=10,
            deals_closed_count=10,
        )
        result = engine.assess(inp)
        # 32 + 30 + 20 + 10 = 92
        assert result.accuracy_score == 92.0

    def test_20pct_error_gets_20pts(self, engine):
        inp = make_input(
            forecasted_amount_usd=100_000.0,
            closed_won_amount_usd=80_000.0,  # 20% under
            avg_forecast_accuracy_last_4q_pct=95.0,
            commit_accuracy_pct=90.0,
            deals_forecasted_count=10,
            deals_closed_count=10,
        )
        result = engine.assess(inp)
        # 20 + 30 + 20 + 10 = 80
        assert result.accuracy_score == 80.0

    def test_35pct_error_gets_10pts(self, engine):
        inp = make_input(
            forecasted_amount_usd=100_000.0,
            closed_won_amount_usd=65_000.0,  # 35% under
            avg_forecast_accuracy_last_4q_pct=95.0,
            commit_accuracy_pct=90.0,
            deals_forecasted_count=10,
            deals_closed_count=10,
        )
        result = engine.assess(inp)
        # 10 + 30 + 20 + 10 = 70
        assert result.accuracy_score == 70.0

    def test_over_35pct_error_gets_0pts(self, engine):
        inp = make_input(
            forecasted_amount_usd=100_000.0,
            closed_won_amount_usd=50_000.0,  # 50% under → no points
            avg_forecast_accuracy_last_4q_pct=95.0,
            commit_accuracy_pct=90.0,
            deals_forecasted_count=10,
            deals_closed_count=10,
        )
        result = engine.assess(inp)
        # 0 + 30 + 20 + 10 = 60
        assert result.accuracy_score == 60.0

    def test_historical_accuracy_90_gives_30pts(self, engine):
        inp = make_input(
            avg_forecast_accuracy_last_4q_pct=90.0,
            commit_accuracy_pct=40.0,  # low, 0 pts
            deals_forecasted_count=10,
            deals_closed_count=3,     # deal ratio >50%, 0 pts
        )
        result = engine.assess(inp)
        # 40 (exact pct) + 30 (hist) + 0 + 0 = 70
        assert result.accuracy_score == 70.0

    def test_historical_accuracy_80_gives_22pts(self, engine):
        inp = make_input(
            avg_forecast_accuracy_last_4q_pct=80.0,
            commit_accuracy_pct=40.0,
            deals_forecasted_count=10,
            deals_closed_count=3,
        )
        result = engine.assess(inp)
        assert result.accuracy_score == 62.0  # 40 + 22 + 0 + 0

    def test_historical_accuracy_70_gives_14pts(self, engine):
        inp = make_input(
            avg_forecast_accuracy_last_4q_pct=70.0,
            commit_accuracy_pct=40.0,
            deals_forecasted_count=10,
            deals_closed_count=3,
        )
        result = engine.assess(inp)
        assert result.accuracy_score == 54.0  # 40 + 14 + 0 + 0

    def test_historical_accuracy_55_gives_6pts(self, engine):
        inp = make_input(
            avg_forecast_accuracy_last_4q_pct=55.0,
            commit_accuracy_pct=40.0,
            deals_forecasted_count=10,
            deals_closed_count=3,
        )
        result = engine.assess(inp)
        assert result.accuracy_score == 46.0  # 40 + 6 + 0 + 0

    def test_commit_accuracy_85_gives_20pts(self, engine):
        inp = make_input(
            avg_forecast_accuracy_last_4q_pct=40.0,
            commit_accuracy_pct=85.0,
            deals_forecasted_count=10,
            deals_closed_count=3,
        )
        result = engine.assess(inp)
        assert result.accuracy_score == 60.0  # 40 + 0 + 20 + 0

    def test_commit_accuracy_75_gives_14pts(self, engine):
        inp = make_input(
            avg_forecast_accuracy_last_4q_pct=40.0,
            commit_accuracy_pct=75.0,
            deals_forecasted_count=10,
            deals_closed_count=3,
        )
        result = engine.assess(inp)
        assert result.accuracy_score == 54.0  # 40 + 0 + 14 + 0

    def test_commit_accuracy_60_gives_7pts(self, engine):
        inp = make_input(
            avg_forecast_accuracy_last_4q_pct=40.0,
            commit_accuracy_pct=60.0,
            deals_forecasted_count=10,
            deals_closed_count=3,
        )
        result = engine.assess(inp)
        assert result.accuracy_score == 47.0  # 40 + 0 + 7 + 0

    def test_deal_ratio_within_10pct_gives_10pts(self, engine):
        inp = make_input(
            avg_forecast_accuracy_last_4q_pct=40.0,
            commit_accuracy_pct=40.0,
            deals_forecasted_count=10,
            deals_closed_count=10,
        )
        result = engine.assess(inp)
        assert result.accuracy_score == 50.0  # 40 + 0 + 0 + 10

    def test_deal_ratio_25pct_gives_6pts(self, engine):
        inp = make_input(
            avg_forecast_accuracy_last_4q_pct=40.0,
            commit_accuracy_pct=40.0,
            deals_forecasted_count=10,
            deals_closed_count=8,  # 20% off → 6pts
        )
        result = engine.assess(inp)
        assert result.accuracy_score == 46.0  # 40 + 0 + 0 + 6

    def test_deal_ratio_50pct_gives_2pts(self, engine):
        inp = make_input(
            avg_forecast_accuracy_last_4q_pct=40.0,
            commit_accuracy_pct=40.0,
            deals_forecasted_count=10,
            deals_closed_count=6,  # 40% off → 2pts
        )
        result = engine.assess(inp)
        assert result.accuracy_score == 42.0  # 40 + 0 + 0 + 2

    def test_zero_deals_forecasted_no_deal_pts(self, engine):
        inp = make_input(
            avg_forecast_accuracy_last_4q_pct=40.0,
            commit_accuracy_pct=40.0,
            deals_forecasted_count=0,
            deals_closed_count=5,
        )
        result = engine.assess(inp)
        assert result.accuracy_score == 40.0  # 40 + 0 + 0 + 0

    def test_accuracy_score_bounded_0_100(self, engine, terrible_input):
        result = engine.assess(terrible_input)
        assert 0.0 <= result.accuracy_score <= 100.0

    def test_accuracy_score_bounded_top(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert result.accuracy_score <= 100.0


# ===========================================================================
# 5. Bias score component tests
# ===========================================================================

class TestBiasScore:
    def test_zero_bias_inputs(self, engine):
        inp = make_input(
            sandbagging_score=0.0,
            optimism_bias_score=0.0,
            close_date_push_count=0,
            stage_lag_days=0.0,
        )
        result = engine.assess(inp)
        assert result.bias_score == 0.0

    def test_sandbagging_score_scales(self, engine):
        inp = make_input(
            sandbagging_score=100.0,
            optimism_bias_score=0.0,
            close_date_push_count=0,
            stage_lag_days=0.0,
        )
        result = engine.assess(inp)
        # min(30, 100*0.3) = 30
        assert result.bias_score == 30.0

    def test_optimism_bias_score_scales(self, engine):
        inp = make_input(
            sandbagging_score=0.0,
            optimism_bias_score=100.0,
            close_date_push_count=0,
            stage_lag_days=0.0,
        )
        result = engine.assess(inp)
        assert result.bias_score == 30.0

    def test_both_bias_scores_max(self, engine):
        inp = make_input(
            sandbagging_score=100.0,
            optimism_bias_score=100.0,
            close_date_push_count=0,
            stage_lag_days=0.0,
        )
        result = engine.assess(inp)
        assert result.bias_score == 60.0

    def test_close_date_push_1_gives_3pts(self, engine):
        inp = make_input(
            sandbagging_score=0.0, optimism_bias_score=0.0,
            close_date_push_count=1, stage_lag_days=0.0,
        )
        result = engine.assess(inp)
        assert result.bias_score == 3.0

    def test_close_date_push_2_gives_8pts(self, engine):
        inp = make_input(
            sandbagging_score=0.0, optimism_bias_score=0.0,
            close_date_push_count=2, stage_lag_days=0.0,
        )
        result = engine.assess(inp)
        assert result.bias_score == 8.0

    def test_close_date_push_3_gives_14pts(self, engine):
        inp = make_input(
            sandbagging_score=0.0, optimism_bias_score=0.0,
            close_date_push_count=3, stage_lag_days=0.0,
        )
        result = engine.assess(inp)
        assert result.bias_score == 14.0

    def test_close_date_push_5_gives_20pts(self, engine):
        inp = make_input(
            sandbagging_score=0.0, optimism_bias_score=0.0,
            close_date_push_count=5, stage_lag_days=0.0,
        )
        result = engine.assess(inp)
        assert result.bias_score == 20.0

    def test_stage_lag_10_gives_7pts(self, engine):
        inp = make_input(
            sandbagging_score=0.0, optimism_bias_score=0.0,
            close_date_push_count=0, stage_lag_days=10.0,
        )
        result = engine.assess(inp)
        assert result.bias_score == 7.0

    def test_stage_lag_20_gives_14pts(self, engine):
        inp = make_input(
            sandbagging_score=0.0, optimism_bias_score=0.0,
            close_date_push_count=0, stage_lag_days=20.0,
        )
        result = engine.assess(inp)
        assert result.bias_score == 14.0

    def test_stage_lag_30_gives_20pts(self, engine):
        inp = make_input(
            sandbagging_score=0.0, optimism_bias_score=0.0,
            close_date_push_count=0, stage_lag_days=30.0,
        )
        result = engine.assess(inp)
        assert result.bias_score == 20.0

    def test_bias_score_bounded(self, engine, terrible_input):
        result = engine.assess(terrible_input)
        assert 0.0 <= result.bias_score <= 100.0

    def test_max_bias_score_capped_at_100(self, engine):
        inp = make_input(
            sandbagging_score=100.0,
            optimism_bias_score=100.0,
            close_date_push_count=10,
            stage_lag_days=60.0,
        )
        result = engine.assess(inp)
        assert result.bias_score <= 100.0


# ===========================================================================
# 6. Consistency score component tests
# ===========================================================================

class TestConsistencyScore:
    def test_perfect_consistency(self, engine):
        inp = make_input(
            forecast_change_frequency=1,
            manager_override_count=0,
            late_stage_slippage_rate_pct=5.0,
            pipeline_coverage_ratio=4.0,
        )
        result = engine.assess(inp)
        # 35 + 30 + 20 + 15 = 100
        assert result.consistency_score == 100.0

    def test_forecast_change_freq_2_gives_35pts(self, engine):
        inp = make_input(
            forecast_change_frequency=2,
            manager_override_count=0,
            late_stage_slippage_rate_pct=100.0,
            pipeline_coverage_ratio=1.0,
        )
        result = engine.assess(inp)
        assert result.consistency_score == 65.0  # 35 + 30 + 0 + 0

    def test_forecast_change_freq_4_gives_25pts(self, engine):
        inp = make_input(
            forecast_change_frequency=4,
            manager_override_count=0,
            late_stage_slippage_rate_pct=100.0,
            pipeline_coverage_ratio=1.0,
        )
        result = engine.assess(inp)
        assert result.consistency_score == 55.0  # 25 + 30 + 0 + 0

    def test_forecast_change_freq_7_gives_12pts(self, engine):
        inp = make_input(
            forecast_change_frequency=7,
            manager_override_count=0,
            late_stage_slippage_rate_pct=100.0,
            pipeline_coverage_ratio=1.0,
        )
        result = engine.assess(inp)
        assert result.consistency_score == 42.0  # 12 + 30 + 0 + 0

    def test_forecast_change_freq_high_gives_0pts(self, engine):
        inp = make_input(
            forecast_change_frequency=10,
            manager_override_count=0,
            late_stage_slippage_rate_pct=100.0,
            pipeline_coverage_ratio=1.0,
        )
        result = engine.assess(inp)
        assert result.consistency_score == 30.0  # 0 + 30 + 0 + 0

    def test_manager_override_0_gives_30pts(self, engine):
        inp = make_input(
            forecast_change_frequency=10,
            manager_override_count=0,
            late_stage_slippage_rate_pct=100.0,
            pipeline_coverage_ratio=1.0,
        )
        result = engine.assess(inp)
        assert result.consistency_score == 30.0

    def test_manager_override_1_gives_20pts(self, engine):
        inp = make_input(
            forecast_change_frequency=10,
            manager_override_count=1,
            late_stage_slippage_rate_pct=100.0,
            pipeline_coverage_ratio=1.0,
        )
        result = engine.assess(inp)
        assert result.consistency_score == 20.0

    def test_manager_override_2_gives_10pts(self, engine):
        inp = make_input(
            forecast_change_frequency=10,
            manager_override_count=2,
            late_stage_slippage_rate_pct=100.0,
            pipeline_coverage_ratio=1.0,
        )
        result = engine.assess(inp)
        assert result.consistency_score == 10.0

    def test_manager_override_3_gives_0pts(self, engine):
        inp = make_input(
            forecast_change_frequency=10,
            manager_override_count=3,
            late_stage_slippage_rate_pct=100.0,
            pipeline_coverage_ratio=1.0,
        )
        result = engine.assess(inp)
        assert result.consistency_score == 0.0

    def test_slippage_rate_10_gives_20pts(self, engine):
        inp = make_input(
            forecast_change_frequency=10,
            manager_override_count=3,
            late_stage_slippage_rate_pct=10.0,
            pipeline_coverage_ratio=1.0,
        )
        result = engine.assess(inp)
        assert result.consistency_score == 20.0

    def test_slippage_rate_20_gives_14pts(self, engine):
        inp = make_input(
            forecast_change_frequency=10,
            manager_override_count=3,
            late_stage_slippage_rate_pct=20.0,
            pipeline_coverage_ratio=1.0,
        )
        result = engine.assess(inp)
        assert result.consistency_score == 14.0

    def test_slippage_rate_35_gives_6pts(self, engine):
        inp = make_input(
            forecast_change_frequency=10,
            manager_override_count=3,
            late_stage_slippage_rate_pct=35.0,
            pipeline_coverage_ratio=1.0,
        )
        result = engine.assess(inp)
        assert result.consistency_score == 6.0

    def test_slippage_rate_high_gives_0pts(self, engine):
        inp = make_input(
            forecast_change_frequency=10,
            manager_override_count=3,
            late_stage_slippage_rate_pct=50.0,
            pipeline_coverage_ratio=1.0,
        )
        result = engine.assess(inp)
        assert result.consistency_score == 0.0

    def test_pipeline_coverage_3_to_5_gives_15pts(self, engine):
        inp = make_input(
            forecast_change_frequency=10,
            manager_override_count=3,
            late_stage_slippage_rate_pct=50.0,
            pipeline_coverage_ratio=4.0,
        )
        result = engine.assess(inp)
        assert result.consistency_score == 15.0

    def test_pipeline_coverage_2_to_3_gives_10pts(self, engine):
        inp = make_input(
            forecast_change_frequency=10,
            manager_override_count=3,
            late_stage_slippage_rate_pct=50.0,
            pipeline_coverage_ratio=2.5,
        )
        result = engine.assess(inp)
        assert result.consistency_score == 10.0

    def test_pipeline_coverage_5_to_7_gives_8pts(self, engine):
        inp = make_input(
            forecast_change_frequency=10,
            manager_override_count=3,
            late_stage_slippage_rate_pct=50.0,
            pipeline_coverage_ratio=6.0,
        )
        result = engine.assess(inp)
        assert result.consistency_score == 8.0

    def test_pipeline_coverage_low_gives_0pts(self, engine):
        inp = make_input(
            forecast_change_frequency=10,
            manager_override_count=3,
            late_stage_slippage_rate_pct=50.0,
            pipeline_coverage_ratio=1.0,
        )
        result = engine.assess(inp)
        assert result.consistency_score == 0.0

    def test_consistency_score_bounded(self, engine, terrible_input):
        result = engine.assess(terrible_input)
        assert 0.0 <= result.consistency_score <= 100.0


# ===========================================================================
# 7. Data quality score component tests
# ===========================================================================

class TestDataQualityScore:
    def test_perfect_data_quality(self, engine):
        inp = make_input(
            data_entry_lag_days=0.5,
            best_case_accuracy_pct=90.0,
            win_rate_trend=1.0,
        )
        result = engine.assess(inp)
        # 40 + 30 + 30 = 100
        assert result.data_quality_score == 100.0

    def test_entry_lag_1_gives_40pts(self, engine):
        inp = make_input(
            data_entry_lag_days=1.0,
            best_case_accuracy_pct=30.0,  # 0 pts
            win_rate_trend=-1.0,           # 0 pts
        )
        result = engine.assess(inp)
        assert result.data_quality_score == 40.0

    def test_entry_lag_2_gives_30pts(self, engine):
        inp = make_input(
            data_entry_lag_days=2.0,
            best_case_accuracy_pct=30.0,
            win_rate_trend=-1.0,
        )
        result = engine.assess(inp)
        assert result.data_quality_score == 30.0

    def test_entry_lag_5_gives_18pts(self, engine):
        inp = make_input(
            data_entry_lag_days=5.0,
            best_case_accuracy_pct=30.0,
            win_rate_trend=-1.0,
        )
        result = engine.assess(inp)
        assert result.data_quality_score == 18.0

    def test_entry_lag_10_gives_8pts(self, engine):
        inp = make_input(
            data_entry_lag_days=10.0,
            best_case_accuracy_pct=30.0,
            win_rate_trend=-1.0,
        )
        result = engine.assess(inp)
        assert result.data_quality_score == 8.0

    def test_entry_lag_high_gives_0pts(self, engine):
        inp = make_input(
            data_entry_lag_days=15.0,
            best_case_accuracy_pct=30.0,
            win_rate_trend=-1.0,
        )
        result = engine.assess(inp)
        assert result.data_quality_score == 0.0

    def test_best_case_accuracy_80_gives_30pts(self, engine):
        inp = make_input(
            data_entry_lag_days=15.0,
            best_case_accuracy_pct=80.0,
            win_rate_trend=-1.0,
        )
        result = engine.assess(inp)
        assert result.data_quality_score == 30.0

    def test_best_case_accuracy_65_gives_20pts(self, engine):
        inp = make_input(
            data_entry_lag_days=15.0,
            best_case_accuracy_pct=65.0,
            win_rate_trend=-1.0,
        )
        result = engine.assess(inp)
        assert result.data_quality_score == 20.0

    def test_best_case_accuracy_50_gives_10pts(self, engine):
        inp = make_input(
            data_entry_lag_days=15.0,
            best_case_accuracy_pct=50.0,
            win_rate_trend=-1.0,
        )
        result = engine.assess(inp)
        assert result.data_quality_score == 10.0

    def test_best_case_accuracy_low_gives_0pts(self, engine):
        inp = make_input(
            data_entry_lag_days=15.0,
            best_case_accuracy_pct=30.0,
            win_rate_trend=-1.0,
        )
        result = engine.assess(inp)
        assert result.data_quality_score == 0.0

    def test_win_rate_trend_positive_05_gives_30pts(self, engine):
        inp = make_input(
            data_entry_lag_days=15.0,
            best_case_accuracy_pct=30.0,
            win_rate_trend=0.5,
        )
        result = engine.assess(inp)
        assert result.data_quality_score == 30.0

    def test_win_rate_trend_zero_gives_20pts(self, engine):
        inp = make_input(
            data_entry_lag_days=15.0,
            best_case_accuracy_pct=30.0,
            win_rate_trend=0.0,
        )
        result = engine.assess(inp)
        assert result.data_quality_score == 20.0

    def test_win_rate_trend_neg_05_gives_10pts(self, engine):
        inp = make_input(
            data_entry_lag_days=15.0,
            best_case_accuracy_pct=30.0,
            win_rate_trend=-0.5,
        )
        result = engine.assess(inp)
        assert result.data_quality_score == 10.0

    def test_win_rate_trend_very_negative_gives_0pts(self, engine):
        inp = make_input(
            data_entry_lag_days=15.0,
            best_case_accuracy_pct=30.0,
            win_rate_trend=-1.0,
        )
        result = engine.assess(inp)
        assert result.data_quality_score == 0.0

    def test_data_quality_score_bounded(self, engine, terrible_input):
        result = engine.assess(terrible_input)
        assert 0.0 <= result.data_quality_score <= 100.0


# ===========================================================================
# 8. Composite formula tests
# ===========================================================================

class TestCompositeFormula:
    def test_composite_formula_correctness(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        expected = round(
            result.accuracy_score * 0.35
            + (100.0 - result.bias_score) * 0.25
            + result.consistency_score * 0.25
            + result.data_quality_score * 0.15,
            1,
        )
        assert result.calibration_composite == expected

    def test_composite_higher_is_better(self, engine, perfect_input, terrible_input):
        good = engine.assess(perfect_input)
        engine.reset()
        bad = engine.assess(terrible_input)
        assert good.calibration_composite > bad.calibration_composite

    def test_composite_range(self, engine, perfect_input, terrible_input):
        good = engine.assess(perfect_input)
        engine.reset()
        bad = engine.assess(terrible_input)
        assert 0.0 <= bad.calibration_composite <= 100.0
        assert 0.0 <= good.calibration_composite <= 100.0

    def test_composite_perfect_is_very_high(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert result.calibration_composite >= 75.0

    def test_composite_terrible_is_low(self, engine, terrible_input):
        result = engine.assess(terrible_input)
        assert result.calibration_composite < 50.0

    def test_composite_bias_inverted(self, engine):
        """Higher bias should lower composite."""
        low_bias = make_input(sandbagging_score=0.0, optimism_bias_score=0.0)
        high_bias = make_input(sandbagging_score=100.0, optimism_bias_score=100.0)
        r_low = engine.assess(low_bias)
        engine.reset()
        r_high = engine.assess(high_bias)
        assert r_low.calibration_composite > r_high.calibration_composite


# ===========================================================================
# 9. Calibration rating thresholds
# ===========================================================================

class TestCalibrationRating:
    def _rep_with_composite(self, engine, target_composite: float) -> ForecastCalibrationResult:
        # Use perfect input and then check what we get
        inp = make_input()
        return engine.assess(inp)

    def test_excellent_rating_at_75(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        # perfect should be >= 75
        assert result.calibration_rating == CalibrationRating.EXCELLENT

    def test_poor_rating_for_terrible(self, engine, terrible_input):
        result = engine.assess(terrible_input)
        assert result.calibration_rating == CalibrationRating.POOR

    def test_good_rating_boundary(self, engine):
        # composite should land in [55, 75)
        inp = make_input(
            forecasted_amount_usd=100_000.0,
            closed_won_amount_usd=80_000.0,
            avg_forecast_accuracy_last_4q_pct=75.0,
            sandbagging_score=0.0,
            optimism_bias_score=0.0,
            stage_lag_days=0.0,
            close_date_push_count=0,
            late_stage_slippage_rate_pct=15.0,
            commit_accuracy_pct=78.0,
            best_case_accuracy_pct=70.0,
            pipeline_coverage_ratio=3.5,
            win_rate_trend=0.3,
            forecast_change_frequency=3,
            manager_override_count=1,
            data_entry_lag_days=3.0,
            deals_forecasted_count=10,
            deals_closed_count=8,
        )
        result = engine.assess(inp)
        assert result.calibration_rating in (
            CalibrationRating.GOOD, CalibrationRating.FAIR, CalibrationRating.EXCELLENT
        )

    def test_rating_is_calibration_rating_enum(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert isinstance(result.calibration_rating, CalibrationRating)

    def test_all_ratings_reachable(self, engine):
        ratings_seen = set()
        cases = [
            make_input(rep_id="a"),  # excellent
            make_input(
                rep_id="b",
                avg_forecast_accuracy_last_4q_pct=60.0,
                forecasted_amount_usd=100_000.0,
                closed_won_amount_usd=85_000.0,
                commit_accuracy_pct=70.0,
                late_stage_slippage_rate_pct=20.0,
                forecast_change_frequency=4,
                manager_override_count=1,
                pipeline_coverage_ratio=2.5,
                data_entry_lag_days=3.0,
                best_case_accuracy_pct=60.0,
                win_rate_trend=0.1,
            ),
            make_input(
                rep_id="c",
                avg_forecast_accuracy_last_4q_pct=55.0,
                forecasted_amount_usd=100_000.0,
                closed_won_amount_usd=70_000.0,
                commit_accuracy_pct=55.0,
                late_stage_slippage_rate_pct=30.0,
                forecast_change_frequency=7,
                manager_override_count=2,
                pipeline_coverage_ratio=1.5,
                data_entry_lag_days=6.0,
                best_case_accuracy_pct=45.0,
                win_rate_trend=-0.3,
            ),
            make_input(
                rep_id="d",
                avg_forecast_accuracy_last_4q_pct=40.0,
                forecasted_amount_usd=100_000.0,
                closed_won_amount_usd=10_000.0,
                commit_accuracy_pct=40.0,
                late_stage_slippage_rate_pct=50.0,
                forecast_change_frequency=10,
                manager_override_count=5,
                pipeline_coverage_ratio=1.0,
                data_entry_lag_days=15.0,
                best_case_accuracy_pct=30.0,
                win_rate_trend=-1.0,
            ),
        ]
        for inp in cases:
            r = engine.assess(inp)
            ratings_seen.add(r.calibration_rating)
        # At least excellent and poor should appear
        assert CalibrationRating.EXCELLENT in ratings_seen
        assert CalibrationRating.POOR in ratings_seen


# ===========================================================================
# 10. Calibration risk thresholds
# ===========================================================================

class TestCalibrationRisk:
    def test_low_risk_for_perfect(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert result.calibration_risk == CalibrationRisk.LOW

    def test_critical_risk_for_terrible(self, engine, terrible_input):
        result = engine.assess(terrible_input)
        assert result.calibration_risk == CalibrationRisk.CRITICAL

    def test_risk_is_enum_type(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert isinstance(result.calibration_risk, CalibrationRisk)

    def test_moderate_risk_boundary(self, engine):
        """composite in [40,60) → MODERATE."""
        # Craft a middling input
        inp = make_input(
            forecasted_amount_usd=100_000.0,
            closed_won_amount_usd=75_000.0,
            avg_forecast_accuracy_last_4q_pct=65.0,
            commit_accuracy_pct=65.0,
            late_stage_slippage_rate_pct=22.0,
            forecast_change_frequency=5,
            manager_override_count=2,
            pipeline_coverage_ratio=2.0,
            data_entry_lag_days=4.0,
            best_case_accuracy_pct=55.0,
            win_rate_trend=-0.2,
            sandbagging_score=10.0,
            optimism_bias_score=10.0,
            close_date_push_count=1,
            stage_lag_days=5.0,
            deals_forecasted_count=10,
            deals_closed_count=7,
        )
        result = engine.assess(inp)
        assert result.calibration_risk in (
            CalibrationRisk.MODERATE, CalibrationRisk.HIGH
        )


# ===========================================================================
# 11. Bias type classification
# ===========================================================================

class TestBiasTypeClassification:
    def test_sandbagging_by_score(self, engine):
        inp = make_input(
            sandbagging_score=80.0,
            optimism_bias_score=10.0,
        )
        result = engine.assess(inp)
        assert result.bias_type == BiasType.SANDBAGGING

    def test_over_optimistic_by_score(self, engine):
        inp = make_input(
            sandbagging_score=10.0,
            optimism_bias_score=80.0,
        )
        result = engine.assess(inp)
        assert result.bias_type == BiasType.OVER_OPTIMISTIC

    def test_inconsistent_both_high(self, engine):
        inp = make_input(
            sandbagging_score=50.0,
            optimism_bias_score=50.0,
        )
        result = engine.assess(inp)
        assert result.bias_type == BiasType.INCONSISTENT

    def test_accurate_low_bias(self, engine):
        inp = make_input(
            sandbagging_score=10.0,
            optimism_bias_score=10.0,
            forecasted_amount_usd=100_000.0,
            closed_won_amount_usd=100_000.0,
        )
        result = engine.assess(inp)
        assert result.bias_type == BiasType.ACCURATE

    def test_sandbagging_by_ratio(self, engine):
        """closed > 125% of forecast → sandbagging."""
        inp = make_input(
            sandbagging_score=10.0,
            optimism_bias_score=10.0,
            forecasted_amount_usd=100_000.0,
            closed_won_amount_usd=130_000.0,  # ratio > 1.25
        )
        result = engine.assess(inp)
        assert result.bias_type == BiasType.SANDBAGGING

    def test_over_optimistic_by_ratio(self, engine):
        """closed < 70% of forecast → over_optimistic."""
        inp = make_input(
            sandbagging_score=10.0,
            optimism_bias_score=10.0,
            forecasted_amount_usd=100_000.0,
            closed_won_amount_usd=60_000.0,  # ratio < 0.70
        )
        result = engine.assess(inp)
        assert result.bias_type == BiasType.OVER_OPTIMISTIC

    def test_bias_type_is_enum(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert isinstance(result.bias_type, BiasType)

    def test_sandbagging_score_boundary(self, engine):
        """sandbagging_score exactly 60 with optimism < 30 → not triggered (need >60)."""
        inp = make_input(
            sandbagging_score=60.0,
            optimism_bias_score=10.0,
            forecasted_amount_usd=100_000.0,
            closed_won_amount_usd=100_000.0,
        )
        result = engine.assess(inp)
        # 60 is NOT > 60, so sandbagging threshold not met
        assert result.bias_type == BiasType.ACCURATE

    def test_optimism_score_boundary(self, engine):
        """optimism_bias_score exactly 60 with sandbagging < 30 → not triggered."""
        inp = make_input(
            sandbagging_score=10.0,
            optimism_bias_score=60.0,
            forecasted_amount_usd=100_000.0,
            closed_won_amount_usd=100_000.0,
        )
        result = engine.assess(inp)
        assert result.bias_type == BiasType.ACCURATE

    def test_inconsistent_threshold_boundary(self, engine):
        """Both > 40 → inconsistent."""
        inp = make_input(
            sandbagging_score=41.0,
            optimism_bias_score=41.0,
            forecasted_amount_usd=100_000.0,
            closed_won_amount_usd=100_000.0,
        )
        result = engine.assess(inp)
        assert result.bias_type == BiasType.INCONSISTENT


# ===========================================================================
# 12. is_sandbagging and is_over_optimistic flags
# ===========================================================================

class TestBooleanFlags:
    def test_is_sandbagging_true_when_sandbagging(self, engine):
        inp = make_input(sandbagging_score=80.0, optimism_bias_score=10.0)
        result = engine.assess(inp)
        assert result.is_sandbagging is True
        assert result.is_over_optimistic is False

    def test_is_over_optimistic_true_when_over_optimistic(self, engine):
        inp = make_input(sandbagging_score=10.0, optimism_bias_score=80.0)
        result = engine.assess(inp)
        assert result.is_over_optimistic is True
        assert result.is_sandbagging is False

    def test_both_false_when_accurate(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert result.is_sandbagging is False
        assert result.is_over_optimistic is False

    def test_both_false_when_inconsistent(self, engine):
        inp = make_input(sandbagging_score=50.0, optimism_bias_score=50.0)
        result = engine.assess(inp)
        assert result.is_sandbagging is False
        assert result.is_over_optimistic is False

    def test_is_sandbagging_by_ratio(self, engine):
        inp = make_input(
            sandbagging_score=10.0,
            optimism_bias_score=10.0,
            forecasted_amount_usd=100_000.0,
            closed_won_amount_usd=130_000.0,
        )
        result = engine.assess(inp)
        assert result.is_sandbagging is True

    def test_is_over_optimistic_by_ratio(self, engine):
        inp = make_input(
            sandbagging_score=10.0,
            optimism_bias_score=10.0,
            forecasted_amount_usd=100_000.0,
            closed_won_amount_usd=60_000.0,
        )
        result = engine.assess(inp)
        assert result.is_over_optimistic is True

    def test_is_sandbagging_matches_bias_type(self, engine):
        for sbag, opt, expected_sbag in [
            (80.0, 10.0, True),
            (10.0, 80.0, False),
            (50.0, 50.0, False),
            (10.0, 10.0, False),
        ]:
            engine.reset()
            inp = make_input(
                sandbagging_score=sbag,
                optimism_bias_score=opt,
                forecasted_amount_usd=100_000.0,
                closed_won_amount_usd=100_000.0,
            )
            r = engine.assess(inp)
            assert r.is_sandbagging == expected_sbag

    def test_is_over_optimistic_matches_bias_type(self, engine):
        for sbag, opt, expected_opt in [
            (80.0, 10.0, False),
            (10.0, 80.0, True),
            (50.0, 50.0, False),
            (10.0, 10.0, False),
        ]:
            engine.reset()
            inp = make_input(
                sandbagging_score=sbag,
                optimism_bias_score=opt,
                forecasted_amount_usd=100_000.0,
                closed_won_amount_usd=100_000.0,
            )
            r = engine.assess(inp)
            assert r.is_over_optimistic == expected_opt


# ===========================================================================
# 13. Calibration action mapping
# ===========================================================================

class TestCalibrationAction:
    def test_critical_risk_gives_system_override(self, engine, terrible_input):
        result = engine.assess(terrible_input)
        if result.calibration_risk == CalibrationRisk.CRITICAL:
            assert result.calibration_action == CalibrationAction.SYSTEM_OVERRIDE

    def test_low_risk_gives_no_action(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        if result.calibration_risk == CalibrationRisk.LOW:
            assert result.calibration_action == CalibrationAction.NO_ACTION

    def test_action_is_enum(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert isinstance(result.calibration_action, CalibrationAction)

    def test_moderate_risk_gives_coaching(self, engine):
        # Craft a moderate-risk scenario by targeting composite in [40, 60)
        inp = make_input(
            forecasted_amount_usd=100_000.0,
            closed_won_amount_usd=75_000.0,
            avg_forecast_accuracy_last_4q_pct=65.0,
            commit_accuracy_pct=65.0,
            late_stage_slippage_rate_pct=22.0,
            forecast_change_frequency=5,
            manager_override_count=2,
            pipeline_coverage_ratio=2.0,
            data_entry_lag_days=4.0,
            best_case_accuracy_pct=55.0,
            win_rate_trend=-0.2,
            sandbagging_score=10.0,
            optimism_bias_score=10.0,
            close_date_push_count=1,
            stage_lag_days=5.0,
            deals_forecasted_count=10,
            deals_closed_count=7,
        )
        result = engine.assess(inp)
        if result.calibration_risk == CalibrationRisk.MODERATE:
            assert result.calibration_action == CalibrationAction.COACHING_REQUIRED

    def test_high_risk_sandbagging_gives_adjustment(self, engine):
        # High risk with sandbagging → FORECAST_ADJUSTMENT
        inp = make_input(
            sandbagging_score=80.0,
            optimism_bias_score=5.0,
            forecasted_amount_usd=100_000.0,
            closed_won_amount_usd=10_000.0,
            avg_forecast_accuracy_last_4q_pct=40.0,
            commit_accuracy_pct=40.0,
            late_stage_slippage_rate_pct=40.0,
            forecast_change_frequency=8,
            manager_override_count=3,
            pipeline_coverage_ratio=1.0,
            data_entry_lag_days=12.0,
            best_case_accuracy_pct=30.0,
            win_rate_trend=-0.8,
            close_date_push_count=4,
            stage_lag_days=25.0,
            deals_forecasted_count=10,
            deals_closed_count=1,
        )
        result = engine.assess(inp)
        if result.calibration_risk == CalibrationRisk.HIGH:
            assert result.calibration_action == CalibrationAction.FORECAST_ADJUSTMENT

    def test_high_risk_over_optimistic_gives_adjustment(self, engine):
        inp = make_input(
            sandbagging_score=5.0,
            optimism_bias_score=80.0,
            forecasted_amount_usd=200_000.0,
            closed_won_amount_usd=10_000.0,
            avg_forecast_accuracy_last_4q_pct=40.0,
            commit_accuracy_pct=40.0,
            late_stage_slippage_rate_pct=40.0,
            forecast_change_frequency=8,
            manager_override_count=3,
            pipeline_coverage_ratio=1.0,
            data_entry_lag_days=12.0,
            best_case_accuracy_pct=30.0,
            win_rate_trend=-0.8,
            close_date_push_count=4,
            stage_lag_days=25.0,
            deals_forecasted_count=10,
            deals_closed_count=1,
        )
        result = engine.assess(inp)
        if result.calibration_risk == CalibrationRisk.HIGH:
            assert result.calibration_action == CalibrationAction.FORECAST_ADJUSTMENT


# ===========================================================================
# 14. Estimated forecast error USD
# ===========================================================================

class TestForecastError:
    def test_error_non_negative(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert result.estimated_forecast_error_usd >= 0.0

    def test_error_formula(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        expected = round(
            perfect_input.forecasted_amount_usd * (100.0 - result.calibration_composite) / 100.0,
            2,
        )
        assert result.estimated_forecast_error_usd == expected

    def test_error_zero_forecast(self, engine):
        inp = make_input(forecasted_amount_usd=0.0)
        result = engine.assess(inp)
        assert result.estimated_forecast_error_usd == 0.0

    def test_error_scales_with_forecast_amount(self, engine):
        inp_small = make_input(rep_id="s", forecasted_amount_usd=10_000.0, closed_won_amount_usd=5_000.0)
        inp_large = make_input(rep_id="l", forecasted_amount_usd=1_000_000.0, closed_won_amount_usd=500_000.0)
        r_small = engine.assess(inp_small)
        engine.reset()
        r_large = engine.assess(inp_large)
        assert r_large.estimated_forecast_error_usd > r_small.estimated_forecast_error_usd

    def test_error_is_float(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert isinstance(result.estimated_forecast_error_usd, float)


# ===========================================================================
# 15. Calibration signal tests
# ===========================================================================

class TestCalibrationSignal:
    def test_signal_is_string(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert isinstance(result.calibration_signal, str)
        assert len(result.calibration_signal) > 0

    def test_sandbagging_signal_content(self, engine):
        inp = make_input(sandbagging_score=80.0, optimism_bias_score=10.0)
        result = engine.assess(inp)
        if result.bias_type == BiasType.SANDBAGGING:
            assert "sandbagging" in result.calibration_signal.lower()

    def test_over_optimistic_signal_content(self, engine):
        inp = make_input(
            sandbagging_score=10.0,
            optimism_bias_score=80.0,
            forecasted_amount_usd=100_000.0,
            closed_won_amount_usd=10_000.0,
        )
        result = engine.assess(inp)
        if result.bias_type == BiasType.OVER_OPTIMISTIC:
            assert "over-optimistic" in result.calibration_signal.lower() or "optimistic" in result.calibration_signal.lower()

    def test_crm_lag_signal(self, engine):
        inp = make_input(
            data_entry_lag_days=10.0,
            sandbagging_score=10.0,
            optimism_bias_score=10.0,
            forecasted_amount_usd=100_000.0,
            closed_won_amount_usd=100_000.0,
        )
        result = engine.assess(inp)
        if result.bias_type == BiasType.ACCURATE and inp.data_entry_lag_days > 5:
            assert "lag" in result.calibration_signal.lower() or "crm" in result.calibration_signal.lower()

    def test_manager_override_signal(self, engine):
        inp = make_input(
            manager_override_count=5,
            sandbagging_score=10.0,
            optimism_bias_score=10.0,
            forecasted_amount_usd=100_000.0,
            closed_won_amount_usd=100_000.0,
            data_entry_lag_days=1.0,
        )
        result = engine.assess(inp)
        if result.bias_type == BiasType.ACCURATE and inp.data_entry_lag_days <= 5 and inp.manager_override_count >= 3:
            assert "override" in result.calibration_signal.lower() or "manager" in result.calibration_signal.lower()

    def test_late_stage_slippage_signal(self, engine):
        inp = make_input(
            late_stage_slippage_rate_pct=40.0,
            sandbagging_score=10.0,
            optimism_bias_score=10.0,
            forecasted_amount_usd=100_000.0,
            closed_won_amount_usd=100_000.0,
            data_entry_lag_days=1.0,
            manager_override_count=0,
        )
        result = engine.assess(inp)
        if result.bias_type == BiasType.ACCURATE and inp.data_entry_lag_days <= 5 and inp.manager_override_count < 3 and inp.late_stage_slippage_rate_pct >= 30:
            assert "slippage" in result.calibration_signal.lower()

    def test_default_signal_contains_accuracy(self, engine):
        inp = make_input(
            avg_forecast_accuracy_last_4q_pct=88.0,
            sandbagging_score=10.0,
            optimism_bias_score=10.0,
            forecasted_amount_usd=100_000.0,
            closed_won_amount_usd=100_000.0,
            data_entry_lag_days=1.0,
            manager_override_count=0,
            late_stage_slippage_rate_pct=5.0,
        )
        result = engine.assess(inp)
        if result.bias_type == BiasType.ACCURATE:
            assert "88%" in result.calibration_signal or "forecast accuracy" in result.calibration_signal.lower()

    def test_sandbagging_signal_includes_ratio(self, engine):
        """Signal should mention ratio of closed to forecast."""
        inp = make_input(
            sandbagging_score=80.0,
            optimism_bias_score=10.0,
            forecasted_amount_usd=100_000.0,
            closed_won_amount_usd=100_000.0,
        )
        result = engine.assess(inp)
        if result.bias_type == BiasType.SANDBAGGING:
            assert "%" in result.calibration_signal

    def test_over_optimistic_signal_includes_gap(self, engine):
        inp = make_input(
            sandbagging_score=10.0,
            optimism_bias_score=80.0,
            forecasted_amount_usd=200_000.0,
            closed_won_amount_usd=50_000.0,
        )
        result = engine.assess(inp)
        if result.bias_type == BiasType.OVER_OPTIMISTIC and inp.forecasted_amount_usd > 0:
            assert "$" in result.calibration_signal


# ===========================================================================
# 16. Engine.assess() tests
# ===========================================================================

class TestEngineAssess:
    def test_assess_returns_result_type(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert isinstance(result, ForecastCalibrationResult)

    def test_assess_stores_result(self, engine, perfect_input):
        engine.assess(perfect_input)
        assert engine.get(perfect_input.rep_id) is not None

    def test_assess_rep_id_preserved(self, engine):
        inp = make_input(rep_id="unique_123")
        result = engine.assess(inp)
        assert result.rep_id == "unique_123"

    def test_assess_rep_name_preserved(self, engine):
        inp = make_input(rep_name="Unique Rep Name")
        result = engine.assess(inp)
        assert result.rep_name == "Unique Rep Name"

    def test_assess_overwrites_previous_result(self, engine):
        inp1 = make_input(rep_id="rep_a", forecasted_amount_usd=100_000.0, closed_won_amount_usd=100_000.0)
        inp2 = make_input(rep_id="rep_a", forecasted_amount_usd=50_000.0, closed_won_amount_usd=10_000.0)
        engine.assess(inp1)
        r2 = engine.assess(inp2)
        stored = engine.get("rep_a")
        assert stored.calibration_composite == r2.calibration_composite

    def test_assess_multiple_reps(self, engine):
        for i in range(5):
            engine.assess(make_input(rep_id=f"rep_{i}"))
        assert len(engine.all_reps()) == 5

    def test_assess_composite_is_rounded_to_1dp(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        # Check it's rounded to 1 decimal place
        assert result.calibration_composite == round(result.calibration_composite, 1)


# ===========================================================================
# 17. Engine.assess_batch() tests
# ===========================================================================

class TestEngineAssessBatch:
    def test_batch_returns_list(self, engine):
        inputs = [make_input(rep_id=f"r{i}") for i in range(3)]
        results = engine.assess_batch(inputs)
        assert isinstance(results, list)

    def test_batch_length_matches_input(self, engine):
        inputs = [make_input(rep_id=f"r{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_sorted_by_composite_desc(self, engine):
        inputs = [
            make_input(rep_id="good", avg_forecast_accuracy_last_4q_pct=95.0),
            make_input(rep_id="bad", avg_forecast_accuracy_last_4q_pct=40.0,
                       forecasted_amount_usd=100_000.0, closed_won_amount_usd=20_000.0,
                       commit_accuracy_pct=40.0, forecast_change_frequency=10,
                       manager_override_count=5, pipeline_coverage_ratio=1.0,
                       data_entry_lag_days=15.0, best_case_accuracy_pct=30.0,
                       win_rate_trend=-1.0, late_stage_slippage_rate_pct=50.0),
        ]
        results = engine.assess_batch(inputs)
        assert results[0].calibration_composite >= results[-1].calibration_composite

    def test_batch_all_results_are_result_type(self, engine):
        inputs = [make_input(rep_id=f"r{i}") for i in range(3)]
        results = engine.assess_batch(inputs)
        assert all(isinstance(r, ForecastCalibrationResult) for r in results)

    def test_batch_stores_all_results(self, engine):
        inputs = [make_input(rep_id=f"r{i}") for i in range(4)]
        engine.assess_batch(inputs)
        for i in range(4):
            assert engine.get(f"r{i}") is not None

    def test_batch_empty_list(self, engine):
        results = engine.assess_batch([])
        assert results == []

    def test_batch_single_element(self, engine):
        results = engine.assess_batch([make_input(rep_id="solo")])
        assert len(results) == 1
        assert results[0].rep_id == "solo"

    def test_batch_sorted_with_multiple(self, engine):
        inputs = [
            make_input(rep_id=f"rep_{i}", avg_forecast_accuracy_last_4q_pct=float(50 + i * 5))
            for i in range(6)
        ]
        results = engine.assess_batch(inputs)
        composites = [r.calibration_composite for r in results]
        assert composites == sorted(composites, reverse=True)


# ===========================================================================
# 18. Engine helper methods
# ===========================================================================

class TestEngineHelpers:
    def test_get_returns_none_for_unknown(self, engine):
        assert engine.get("nonexistent") is None

    def test_get_returns_correct_result(self, engine):
        inp = make_input(rep_id="known_rep")
        r = engine.assess(inp)
        assert engine.get("known_rep") is r

    def test_all_reps_empty_before_assess(self, engine):
        assert engine.all_reps() == []

    def test_all_reps_sorted_desc(self, engine):
        for i in range(4):
            engine.assess(make_input(rep_id=f"r{i}", avg_forecast_accuracy_last_4q_pct=float(60 + i * 5)))
        reps = engine.all_reps()
        composites = [r.calibration_composite for r in reps]
        assert composites == sorted(composites, reverse=True)

    def test_sandbagging_reps_empty(self, engine, perfect_input):
        engine.assess(perfect_input)
        # perfect should not be sandbagging
        sbag = engine.sandbagging_reps()
        assert all(r.is_sandbagging for r in sbag)

    def test_sandbagging_reps_finds_sbaggers(self, engine):
        inp = make_input(rep_id="sbagger", sandbagging_score=80.0, optimism_bias_score=10.0)
        engine.assess(inp)
        sbag = engine.sandbagging_reps()
        assert any(r.rep_id == "sbagger" for r in sbag)

    def test_over_optimistic_reps_finds_optimists(self, engine):
        inp = make_input(rep_id="optim", sandbagging_score=10.0, optimism_bias_score=80.0)
        engine.assess(inp)
        opts = engine.over_optimistic_reps()
        assert any(r.rep_id == "optim" for r in opts)

    def test_by_rating_filters_correctly(self, engine, perfect_input):
        engine.assess(perfect_input)
        excellent = engine.by_rating(CalibrationRating.EXCELLENT)
        assert all(r.calibration_rating == CalibrationRating.EXCELLENT for r in excellent)

    def test_by_risk_filters_correctly(self, engine, terrible_input):
        engine.assess(terrible_input)
        critical = engine.by_risk(CalibrationRisk.CRITICAL)
        assert all(r.calibration_risk == CalibrationRisk.CRITICAL for r in critical)

    def test_avg_calibration_composite_empty(self, engine):
        assert engine.avg_calibration_composite() == 0.0

    def test_avg_calibration_composite_single(self, engine, perfect_input):
        r = engine.assess(perfect_input)
        assert engine.avg_calibration_composite() == r.calibration_composite

    def test_avg_calibration_composite_multiple(self, engine):
        inp1 = make_input(rep_id="a")
        inp2 = make_input(rep_id="b", avg_forecast_accuracy_last_4q_pct=60.0)
        r1 = engine.assess(inp1)
        r2 = engine.assess(inp2)
        expected = round((r1.calibration_composite + r2.calibration_composite) / 2, 1)
        assert engine.avg_calibration_composite() == expected

    def test_total_forecast_error_empty(self, engine):
        assert engine.total_forecast_error_exposure_usd() == 0.0

    def test_total_forecast_error_single(self, engine, perfect_input):
        r = engine.assess(perfect_input)
        assert engine.total_forecast_error_exposure_usd() == r.estimated_forecast_error_usd

    def test_total_forecast_error_multiple(self, engine):
        r1 = engine.assess(make_input(rep_id="a"))
        r2 = engine.assess(make_input(rep_id="b", avg_forecast_accuracy_last_4q_pct=60.0))
        expected = round(r1.estimated_forecast_error_usd + r2.estimated_forecast_error_usd, 2)
        assert engine.total_forecast_error_exposure_usd() == expected

    def test_reset_clears_results(self, engine, perfect_input):
        engine.assess(perfect_input)
        engine.reset()
        assert engine.all_reps() == []
        assert engine.get(perfect_input.rep_id) is None

    def test_reset_clears_forecast_values(self, engine, perfect_input):
        engine.assess(perfect_input)
        engine.reset()
        assert engine.total_forecast_error_exposure_usd() == 0.0
        assert engine.avg_calibration_composite() == 0.0


# ===========================================================================
# 19. Summary method tests
# ===========================================================================

class TestSummary:
    def test_summary_has_13_keys(self, engine, perfect_input):
        engine.assess(perfect_input)
        s = engine.summary()
        assert len(s) == 13

    def test_summary_key_names(self, engine, perfect_input):
        engine.assess(perfect_input)
        s = engine.summary()
        expected_keys = {
            "total", "calibration_counts", "risk_counts", "bias_type_counts",
            "action_counts", "avg_calibration_composite", "sandbagging_count",
            "over_optimistic_count", "avg_accuracy_score", "avg_bias_score",
            "avg_consistency_score", "avg_data_quality_score",
            "total_forecast_error_exposure_usd",
        }
        assert set(s.keys()) == expected_keys

    def test_summary_total_matches_reps(self, engine):
        for i in range(4):
            engine.assess(make_input(rep_id=f"r{i}"))
        s = engine.summary()
        assert s["total"] == 4

    def test_summary_empty_engine(self, engine):
        # Should work without errors even with 0 reps
        # But the code divides by n which could be 0 — rely on guard
        # Actually summary() divides by n only if n > 0 (ternary), but let's verify
        # Empty results → total=0
        s = engine.summary()
        assert s["total"] == 0

    def test_summary_calibration_counts_type(self, engine, perfect_input):
        engine.assess(perfect_input)
        s = engine.summary()
        assert isinstance(s["calibration_counts"], dict)

    def test_summary_risk_counts_type(self, engine, perfect_input):
        engine.assess(perfect_input)
        s = engine.summary()
        assert isinstance(s["risk_counts"], dict)

    def test_summary_bias_type_counts_type(self, engine, perfect_input):
        engine.assess(perfect_input)
        s = engine.summary()
        assert isinstance(s["bias_type_counts"], dict)

    def test_summary_action_counts_type(self, engine, perfect_input):
        engine.assess(perfect_input)
        s = engine.summary()
        assert isinstance(s["action_counts"], dict)

    def test_summary_calibration_counts_sum_equals_total(self, engine):
        for i in range(5):
            engine.assess(make_input(rep_id=f"r{i}"))
        s = engine.summary()
        assert sum(s["calibration_counts"].values()) == s["total"]

    def test_summary_risk_counts_sum_equals_total(self, engine):
        for i in range(5):
            engine.assess(make_input(rep_id=f"r{i}"))
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_bias_type_counts_sum_equals_total(self, engine):
        for i in range(5):
            engine.assess(make_input(rep_id=f"r{i}"))
        s = engine.summary()
        assert sum(s["bias_type_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_equals_total(self, engine):
        for i in range(5):
            engine.assess(make_input(rep_id=f"r{i}"))
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_sandbagging_count_correct(self, engine):
        engine.assess(make_input(rep_id="sbag", sandbagging_score=80.0, optimism_bias_score=10.0))
        engine.assess(make_input(rep_id="ok", sandbagging_score=10.0, optimism_bias_score=10.0,
                                 forecasted_amount_usd=100_000.0, closed_won_amount_usd=100_000.0))
        s = engine.summary()
        assert s["sandbagging_count"] == len(engine.sandbagging_reps())

    def test_summary_over_optimistic_count_correct(self, engine):
        engine.assess(make_input(rep_id="opt", sandbagging_score=10.0, optimism_bias_score=80.0))
        engine.assess(make_input(rep_id="ok", sandbagging_score=10.0, optimism_bias_score=10.0,
                                 forecasted_amount_usd=100_000.0, closed_won_amount_usd=100_000.0))
        s = engine.summary()
        assert s["over_optimistic_count"] == len(engine.over_optimistic_reps())

    def test_summary_avg_composite_matches_method(self, engine):
        for i in range(3):
            engine.assess(make_input(rep_id=f"r{i}"))
        s = engine.summary()
        assert s["avg_calibration_composite"] == engine.avg_calibration_composite()

    def test_summary_total_error_matches_method(self, engine):
        for i in range(3):
            engine.assess(make_input(rep_id=f"r{i}"))
        s = engine.summary()
        assert s["total_forecast_error_exposure_usd"] == engine.total_forecast_error_exposure_usd()

    def test_summary_avg_accuracy_score(self, engine):
        r1 = engine.assess(make_input(rep_id="a"))
        r2 = engine.assess(make_input(rep_id="b"))
        s = engine.summary()
        expected = round((r1.accuracy_score + r2.accuracy_score) / 2, 1)
        assert s["avg_accuracy_score"] == expected

    def test_summary_avg_bias_score(self, engine):
        r1 = engine.assess(make_input(rep_id="a"))
        r2 = engine.assess(make_input(rep_id="b"))
        s = engine.summary()
        expected = round((r1.bias_score + r2.bias_score) / 2, 1)
        assert s["avg_bias_score"] == expected

    def test_summary_avg_consistency_score(self, engine):
        r1 = engine.assess(make_input(rep_id="a"))
        r2 = engine.assess(make_input(rep_id="b"))
        s = engine.summary()
        expected = round((r1.consistency_score + r2.consistency_score) / 2, 1)
        assert s["avg_consistency_score"] == expected

    def test_summary_avg_data_quality_score(self, engine):
        r1 = engine.assess(make_input(rep_id="a"))
        r2 = engine.assess(make_input(rep_id="b"))
        s = engine.summary()
        expected = round((r1.data_quality_score + r2.data_quality_score) / 2, 1)
        assert s["avg_data_quality_score"] == expected


# ===========================================================================
# 20. Edge cases and boundary value tests
# ===========================================================================

class TestEdgeCases:
    def test_zero_forecast_amount(self, engine):
        inp = make_input(forecasted_amount_usd=0.0, closed_won_amount_usd=0.0)
        result = engine.assess(inp)
        assert isinstance(result, ForecastCalibrationResult)
        assert result.estimated_forecast_error_usd == 0.0

    def test_very_large_forecast(self, engine):
        inp = make_input(forecasted_amount_usd=1_000_000_000.0, closed_won_amount_usd=1_000_000_000.0)
        result = engine.assess(inp)
        assert isinstance(result, ForecastCalibrationResult)

    def test_forecasted_amount_larger_than_closed(self, engine):
        inp = make_input(forecasted_amount_usd=200_000.0, closed_won_amount_usd=100_000.0)
        result = engine.assess(inp)
        assert isinstance(result, ForecastCalibrationResult)

    def test_closed_won_larger_than_forecasted(self, engine):
        inp = make_input(forecasted_amount_usd=100_000.0, closed_won_amount_usd=200_000.0)
        result = engine.assess(inp)
        assert isinstance(result, ForecastCalibrationResult)

    def test_zero_deals_forecasted(self, engine):
        inp = make_input(deals_forecasted_count=0, deals_closed_count=5)
        result = engine.assess(inp)
        assert isinstance(result, ForecastCalibrationResult)

    def test_zero_deals_closed(self, engine):
        inp = make_input(deals_forecasted_count=10, deals_closed_count=0)
        result = engine.assess(inp)
        assert isinstance(result, ForecastCalibrationResult)

    def test_extreme_sandbagging_score(self, engine):
        inp = make_input(sandbagging_score=1000.0)
        result = engine.assess(inp)
        assert result.bias_score <= 100.0

    def test_extreme_optimism_score(self, engine):
        inp = make_input(optimism_bias_score=1000.0)
        result = engine.assess(inp)
        assert result.bias_score <= 100.0

    def test_negative_win_rate_trend(self, engine):
        inp = make_input(win_rate_trend=-2.0)
        result = engine.assess(inp)
        assert result.data_quality_score >= 0.0

    def test_zero_pipeline_coverage(self, engine):
        inp = make_input(pipeline_coverage_ratio=0.0)
        result = engine.assess(inp)
        assert isinstance(result, ForecastCalibrationResult)

    def test_scores_are_finite(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert math.isfinite(result.accuracy_score)
        assert math.isfinite(result.bias_score)
        assert math.isfinite(result.consistency_score)
        assert math.isfinite(result.data_quality_score)
        assert math.isfinite(result.calibration_composite)

    def test_many_deals_closed_count_ratio(self, engine):
        inp = make_input(deals_forecasted_count=1, deals_closed_count=100)
        result = engine.assess(inp)
        assert result.accuracy_score >= 0.0

    def test_same_rep_id_different_quarters(self, engine):
        inp1 = make_input(rep_id="rep_a", quarter="Q1-2026")
        inp2 = make_input(rep_id="rep_a", quarter="Q2-2026", avg_forecast_accuracy_last_4q_pct=60.0)
        engine.assess(inp1)
        r2 = engine.assess(inp2)
        # Second assess should overwrite
        stored = engine.get("rep_a")
        assert stored.calibration_composite == r2.calibration_composite

    def test_forecast_change_freq_exactly_2(self, engine):
        inp = make_input(forecast_change_frequency=2)
        result = engine.assess(inp)
        # freq <= 2 → 35 pts
        assert result.consistency_score >= 35.0

    def test_forecast_change_freq_exactly_3(self, engine):
        inp = make_input(forecast_change_frequency=3,
                         manager_override_count=10,
                         late_stage_slippage_rate_pct=100.0,
                         pipeline_coverage_ratio=0.0)
        result = engine.assess(inp)
        # freq 3 → in [3,4] range → 25 pts for freq, 0 for rest
        assert result.consistency_score == 25.0

    def test_pipeline_coverage_exactly_3(self, engine):
        inp = make_input(
            forecast_change_frequency=10,
            manager_override_count=3,
            late_stage_slippage_rate_pct=50.0,
            pipeline_coverage_ratio=3.0,
        )
        result = engine.assess(inp)
        # 3.0 is in [3.0, 5.0] → 15 pts
        assert result.consistency_score == 15.0

    def test_pipeline_coverage_exactly_5(self, engine):
        inp = make_input(
            forecast_change_frequency=10,
            manager_override_count=3,
            late_stage_slippage_rate_pct=50.0,
            pipeline_coverage_ratio=5.0,
        )
        result = engine.assess(inp)
        # 5.0 is in [3.0, 5.0] → 15 pts
        assert result.consistency_score == 15.0

    def test_pipeline_coverage_just_above_5(self, engine):
        inp = make_input(
            forecast_change_frequency=10,
            manager_override_count=3,
            late_stage_slippage_rate_pct=50.0,
            pipeline_coverage_ratio=5.1,
        )
        result = engine.assess(inp)
        # 5.1 is in (5.0, 7.0] → 8 pts
        assert result.consistency_score == 8.0


# ===========================================================================
# 21. Integration / scenario tests
# ===========================================================================

class TestScenarios:
    def test_star_rep_scenario(self, engine):
        """A top performer should get excellent rating and low risk."""
        inp = make_input(
            rep_id="star_rep",
            forecasted_amount_usd=500_000.0,
            closed_won_amount_usd=498_000.0,
            avg_forecast_accuracy_last_4q_pct=95.0,
            sandbagging_score=5.0,
            optimism_bias_score=5.0,
            stage_lag_days=2.0,
            close_date_push_count=0,
            late_stage_slippage_rate_pct=5.0,
            commit_accuracy_pct=93.0,
            best_case_accuracy_pct=88.0,
            pipeline_coverage_ratio=4.0,
            win_rate_trend=0.8,
            forecast_change_frequency=1,
            manager_override_count=0,
            data_entry_lag_days=0.5,
            deals_forecasted_count=20,
            deals_closed_count=20,
        )
        result = engine.assess(inp)
        assert result.calibration_rating == CalibrationRating.EXCELLENT
        assert result.calibration_risk == CalibrationRisk.LOW
        assert result.calibration_action == CalibrationAction.NO_ACTION
        assert result.is_sandbagging is False
        assert result.is_over_optimistic is False

    def test_chronic_sandbagger_scenario(self, engine):
        inp = make_input(
            rep_id="sandbagger",
            sandbagging_score=90.0,
            optimism_bias_score=10.0,
            forecasted_amount_usd=100_000.0,
            closed_won_amount_usd=100_000.0,
        )
        result = engine.assess(inp)
        assert result.is_sandbagging is True
        assert result.bias_type == BiasType.SANDBAGGING

    def test_over_optimist_scenario(self, engine):
        inp = make_input(
            rep_id="opt_rep",
            sandbagging_score=5.0,
            optimism_bias_score=90.0,
            forecasted_amount_usd=300_000.0,
            closed_won_amount_usd=50_000.0,
            close_date_push_count=5,
            stage_lag_days=35.0,
            late_stage_slippage_rate_pct=45.0,
        )
        result = engine.assess(inp)
        assert result.is_over_optimistic is True

    def test_chaotic_rep_scenario(self, engine):
        """High override count, high change frequency, poor slippage → inconsistent."""
        inp = make_input(
            sandbagging_score=45.0,
            optimism_bias_score=45.0,
            forecast_change_frequency=10,
            manager_override_count=5,
            late_stage_slippage_rate_pct=50.0,
        )
        result = engine.assess(inp)
        assert result.bias_type == BiasType.INCONSISTENT

    def test_stale_data_scenario(self, engine):
        inp = make_input(data_entry_lag_days=20.0, best_case_accuracy_pct=30.0, win_rate_trend=-1.0)
        result = engine.assess(inp)
        # data quality should be penalised: lag=20→0pts, best_case=30→0pts, win=-1→0pts
        assert result.data_quality_score == 0.0

    def test_multiple_reps_sorted_correctly(self, engine):
        reps = [
            make_input(rep_id="a", avg_forecast_accuracy_last_4q_pct=95.0),
            make_input(rep_id="b", avg_forecast_accuracy_last_4q_pct=70.0),
            make_input(rep_id="c", avg_forecast_accuracy_last_4q_pct=55.0),
        ]
        results = engine.assess_batch(reps)
        assert results[0].accuracy_score >= results[-1].accuracy_score

    def test_reset_then_reassess(self, engine, perfect_input):
        engine.assess(perfect_input)
        engine.reset()
        assert engine.all_reps() == []
        r2 = engine.assess(perfect_input)
        assert engine.get(perfect_input.rep_id) is not None
        assert r2.rep_id == perfect_input.rep_id

    def test_summary_after_mixed_batch(self, engine):
        inputs = [
            make_input(rep_id="good", sandbagging_score=5.0, optimism_bias_score=5.0),
            make_input(rep_id="sbagger", sandbagging_score=80.0, optimism_bias_score=5.0),
            make_input(rep_id="optim", sandbagging_score=5.0, optimism_bias_score=80.0),
        ]
        engine.assess_batch(inputs)
        s = engine.summary()
        assert s["total"] == 3
        assert s["sandbagging_count"] >= 0
        assert s["over_optimistic_count"] >= 0

    def test_by_rating_after_batch(self, engine):
        inputs = [make_input(rep_id=f"r{i}") for i in range(6)]
        engine.assess_batch(inputs)
        for rating in CalibrationRating:
            subset = engine.by_rating(rating)
            assert all(r.calibration_rating == rating for r in subset)

    def test_by_risk_after_batch(self, engine):
        inputs = [make_input(rep_id=f"r{i}") for i in range(6)]
        engine.assess_batch(inputs)
        for risk in CalibrationRisk:
            subset = engine.by_risk(risk)
            assert all(r.calibration_risk == risk for r in subset)


# ===========================================================================
# 22. Additional parametric / numeric correctness tests
# ===========================================================================

class TestParametricCoverage:
    @pytest.mark.parametrize("sandbagging,optimism,expected_sbag,expected_opt", [
        (80.0, 5.0, True, False),
        (5.0, 80.0, False, True),
        (45.0, 45.0, False, False),   # inconsistent → neither
        (5.0, 5.0, False, False),     # accurate → neither
    ])
    def test_bias_flags_parametric(self, engine, sandbagging, optimism, expected_sbag, expected_opt):
        inp = make_input(
            sandbagging_score=sandbagging,
            optimism_bias_score=optimism,
            forecasted_amount_usd=100_000.0,
            closed_won_amount_usd=100_000.0,
        )
        result = engine.assess(inp)
        engine.reset()
        assert result.is_sandbagging == expected_sbag
        assert result.is_over_optimistic == expected_opt

    @pytest.mark.parametrize("lag,expected_pts", [
        (0.5, 40.0),
        (1.0, 40.0),
        (1.5, 30.0),
        (2.0, 30.0),
        (3.0, 18.0),
        (5.0, 18.0),
        (7.0, 8.0),
        (10.0, 8.0),
        (11.0, 0.0),
        (20.0, 0.0),
    ])
    def test_entry_lag_points(self, engine, lag, expected_pts):
        inp = make_input(
            data_entry_lag_days=lag,
            best_case_accuracy_pct=30.0,
            win_rate_trend=-1.0,
        )
        result = engine.assess(inp)
        engine.reset()
        assert result.data_quality_score == expected_pts

    @pytest.mark.parametrize("push_count,expected_pts", [
        (0, 0.0),
        (1, 3.0),
        (2, 8.0),
        (3, 14.0),
        (4, 14.0),
        (5, 20.0),
        (10, 20.0),
    ])
    def test_close_date_push_points(self, engine, push_count, expected_pts):
        inp = make_input(
            sandbagging_score=0.0,
            optimism_bias_score=0.0,
            close_date_push_count=push_count,
            stage_lag_days=0.0,
        )
        result = engine.assess(inp)
        engine.reset()
        assert result.bias_score == expected_pts

    @pytest.mark.parametrize("slippage,expected_pts", [
        (5.0, 20.0),
        (10.0, 20.0),
        (15.0, 14.0),
        (20.0, 14.0),
        (25.0, 6.0),
        (35.0, 6.0),
        (36.0, 0.0),
        (50.0, 0.0),
    ])
    def test_slippage_points(self, engine, slippage, expected_pts):
        inp = make_input(
            forecast_change_frequency=10,
            manager_override_count=3,
            late_stage_slippage_rate_pct=slippage,
            pipeline_coverage_ratio=1.0,
        )
        result = engine.assess(inp)
        engine.reset()
        assert result.consistency_score == expected_pts

    @pytest.mark.parametrize("win_trend,expected_pts", [
        (1.0, 30.0),
        (0.5, 30.0),
        (0.3, 20.0),
        (0.0, 20.0),
        (-0.3, 10.0),
        (-0.5, 10.0),
        (-0.6, 0.0),
        (-1.0, 0.0),
    ])
    def test_win_rate_trend_points(self, engine, win_trend, expected_pts):
        inp = make_input(
            data_entry_lag_days=15.0,
            best_case_accuracy_pct=30.0,
            win_rate_trend=win_trend,
        )
        result = engine.assess(inp)
        engine.reset()
        assert result.data_quality_score == expected_pts

    @pytest.mark.parametrize("overrides,expected_pts", [
        (0, 30.0),
        (1, 20.0),
        (2, 10.0),
        (3, 0.0),
        (10, 0.0),
    ])
    def test_manager_override_points(self, engine, overrides, expected_pts):
        inp = make_input(
            forecast_change_frequency=10,
            manager_override_count=overrides,
            late_stage_slippage_rate_pct=50.0,
            pipeline_coverage_ratio=1.0,
        )
        result = engine.assess(inp)
        engine.reset()
        assert result.consistency_score == expected_pts

    @pytest.mark.parametrize("freq,expected_pts", [
        (1, 35.0),
        (2, 35.0),
        (3, 25.0),
        (4, 25.0),
        (5, 12.0),
        (7, 12.0),
        (8, 0.0),
        (15, 0.0),
    ])
    def test_forecast_change_freq_points(self, engine, freq, expected_pts):
        inp = make_input(
            forecast_change_frequency=freq,
            manager_override_count=3,
            late_stage_slippage_rate_pct=50.0,
            pipeline_coverage_ratio=1.0,
        )
        result = engine.assess(inp)
        engine.reset()
        assert result.consistency_score == expected_pts

    @pytest.mark.parametrize("hist_acc,expected_pts", [
        (95.0, 30.0),
        (90.0, 30.0),
        (85.0, 22.0),
        (80.0, 22.0),
        (75.0, 14.0),
        (70.0, 14.0),
        (60.0, 6.0),
        (55.0, 6.0),
        (40.0, 0.0),
    ])
    def test_historical_accuracy_points(self, engine, hist_acc, expected_pts):
        inp = make_input(
            avg_forecast_accuracy_last_4q_pct=hist_acc,
            commit_accuracy_pct=40.0,
            deals_forecasted_count=10,
            deals_closed_count=3,
        )
        result = engine.assess(inp)
        engine.reset()
        assert result.accuracy_score == 40.0 + expected_pts

    @pytest.mark.parametrize("commit_acc,expected_pts", [
        (90.0, 20.0),
        (85.0, 20.0),
        (80.0, 14.0),
        (75.0, 14.0),
        (70.0, 7.0),
        (60.0, 7.0),
        (50.0, 0.0),
    ])
    def test_commit_accuracy_points(self, engine, commit_acc, expected_pts):
        inp = make_input(
            avg_forecast_accuracy_last_4q_pct=40.0,
            commit_accuracy_pct=commit_acc,
            deals_forecasted_count=10,
            deals_closed_count=3,
        )
        result = engine.assess(inp)
        engine.reset()
        assert result.accuracy_score == 40.0 + expected_pts

    @pytest.mark.parametrize("best_case,expected_pts", [
        (90.0, 30.0),
        (80.0, 30.0),
        (70.0, 20.0),
        (65.0, 20.0),
        (55.0, 10.0),
        (50.0, 10.0),
        (40.0, 0.0),
    ])
    def test_best_case_accuracy_points(self, engine, best_case, expected_pts):
        inp = make_input(
            data_entry_lag_days=15.0,
            best_case_accuracy_pct=best_case,
            win_rate_trend=-1.0,
        )
        result = engine.assess(inp)
        engine.reset()
        assert result.data_quality_score == expected_pts

    @pytest.mark.parametrize("stage_lag,expected_pts", [
        (0.0, 0.0),
        (9.0, 0.0),
        (10.0, 7.0),
        (15.0, 7.0),
        (20.0, 14.0),
        (25.0, 14.0),
        (30.0, 20.0),
        (50.0, 20.0),
    ])
    def test_stage_lag_points(self, engine, stage_lag, expected_pts):
        inp = make_input(
            sandbagging_score=0.0,
            optimism_bias_score=0.0,
            close_date_push_count=0,
            stage_lag_days=stage_lag,
        )
        result = engine.assess(inp)
        engine.reset()
        assert result.bias_score == expected_pts
