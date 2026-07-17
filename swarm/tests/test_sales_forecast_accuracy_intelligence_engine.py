"""
Comprehensive pytest test suite for SalesForecastAccuracyIntelligenceEngine.
Covers: all enum values/counts, all 22 input fields, all 15 result fields,
to_dict 15 keys, all sub-score branches and caps, pattern detection priority
and all 6 patterns, risk/severity thresholds, all action mappings, both flag
conditions, revenue at risk formula, signal string, composite formula,
assess, assess_batch, summary (empty and populated with all 13 keys), edge cases.
"""
from __future__ import annotations

import pytest

from swarm.intelligence.sales_forecast_accuracy_intelligence_engine import (
    ForecastAction,
    ForecastInput,
    ForecastPattern,
    ForecastResult,
    ForecastRisk,
    ForecastSeverity,
    SalesForecastAccuracyIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def make_input(**overrides) -> ForecastInput:
    """Return a low-risk ForecastInput; any field can be overridden."""
    defaults = dict(
        rep_id="rep-001",
        region="West",
        evaluation_period_id="Q1-2026",
        forecast_vs_actual_variance_pct=0.05,   # < 0.10  → no accuracy pts
        over_forecast_frequency_pct=0.10,        # < 0.40  → no commit pts
        under_forecast_frequency_pct=0.10,       # < 0.30  → no commit pts
        commit_to_close_rate_pct=0.90,           # > 0.75  → no commit pts
        best_case_to_close_rate_pct=0.80,
        pipeline_to_quota_ratio=3.0,
        late_add_to_forecast_pct=0.05,           # < 0.20  → no discipline pts
        deals_pulled_from_forecast_pct=0.05,     # < 0.20  → no stage pts
        avg_deal_slip_days=5.0,                  # < 14    → no stage pts
        stage_advancement_accuracy_pct=0.90,     # > 0.75  → no stage pts
        close_date_accuracy_within_week_pct=0.80,  # > 0.55 → no accuracy pts
        forecast_change_frequency_per_qtr=0.5,   # < 1.5   → no discipline pts
        upside_deals_closed_pct=0.70,
        commit_deals_lost_pct=0.05,              # < 0.20  → no accuracy pts
        sandbag_conversion_rate_pct=0.20,
        multi_quarter_slip_rate_pct=0.05,        # < 0.15  → no discipline pts
        forecast_submitted_on_time_pct=0.95,
        total_deals_forecasted=10,
        avg_opportunity_value_usd=50_000.0,
    )
    defaults.update(overrides)
    return ForecastInput(**defaults)


@pytest.fixture()
def engine() -> SalesForecastAccuracyIntelligenceEngine:
    return SalesForecastAccuracyIntelligenceEngine()


def low_risk_input() -> ForecastInput:
    return make_input()


def critical_input() -> ForecastInput:
    """All sub-scores at maximum to guarantee composite >= 60."""
    return make_input(
        forecast_vs_actual_variance_pct=0.50,       # +40 accuracy
        commit_deals_lost_pct=0.50,                 # +35 accuracy
        close_date_accuracy_within_week_pct=0.20,   # +25 accuracy  → accuracy=100
        forecast_change_frequency_per_qtr=6.0,      # +40 discipline
        late_add_to_forecast_pct=0.50,              # +35 discipline
        multi_quarter_slip_rate_pct=0.40,           # +25 discipline → discipline=100
        stage_advancement_accuracy_pct=0.30,        # +40 stage
        deals_pulled_from_forecast_pct=0.40,        # +35 stage
        avg_deal_slip_days=35.0,                    # +25 stage      → stage=100
        commit_to_close_rate_pct=0.30,              # +45 commit
        over_forecast_frequency_pct=0.70,           # +30 commit
        under_forecast_frequency_pct=0.60,          # +25 commit     → commit=100
    )


# ---------------------------------------------------------------------------
# 1. Enum values and counts
# ---------------------------------------------------------------------------

class TestEnums:
    def test_forecast_risk_values(self):
        assert set(r.value for r in ForecastRisk) == {"low", "moderate", "high", "critical"}

    def test_forecast_risk_count(self):
        assert len(ForecastRisk) == 4

    def test_forecast_pattern_values(self):
        expected = {
            "none",
            "chronic_over_forecasting",
            "chronic_under_forecasting",
            "end_of_quarter_cliff",
            "recency_bias_sandbagging",
            "stage_inflation_blindspot",
        }
        assert set(p.value for p in ForecastPattern) == expected

    def test_forecast_pattern_count(self):
        assert len(ForecastPattern) == 6

    def test_forecast_severity_values(self):
        assert set(s.value for s in ForecastSeverity) == {
            "precise", "calibrating", "drifting", "unreliable"
        }

    def test_forecast_severity_count(self):
        assert len(ForecastSeverity) == 4

    def test_forecast_action_values(self):
        assert set(a.value for a in ForecastAction) == {
            "no_action",
            "forecast_calibration_coaching",
            "pipeline_inspection_coaching",
            "stage_criteria_coaching",
            "commit_discipline_coaching",
            "forecast_reset_intervention",
        }

    def test_forecast_action_count(self):
        assert len(ForecastAction) == 6

    def test_enums_are_str_subclass(self):
        assert isinstance(ForecastRisk.low, str)
        assert isinstance(ForecastPattern.none, str)
        assert isinstance(ForecastSeverity.precise, str)
        assert isinstance(ForecastAction.no_action, str)

    def test_forecast_risk_str_equality(self):
        assert ForecastRisk.low == "low"
        assert ForecastRisk.critical == "critical"

    def test_forecast_pattern_str_equality(self):
        assert ForecastPattern.none == "none"
        assert ForecastPattern.stage_inflation_blindspot == "stage_inflation_blindspot"


# ---------------------------------------------------------------------------
# 2. ForecastInput — all 22 fields
# ---------------------------------------------------------------------------

class TestForecastInput:
    def test_all_22_fields_present(self):
        inp = make_input()
        fields = [
            "rep_id", "region", "evaluation_period_id",
            "forecast_vs_actual_variance_pct", "over_forecast_frequency_pct",
            "under_forecast_frequency_pct", "commit_to_close_rate_pct",
            "best_case_to_close_rate_pct", "pipeline_to_quota_ratio",
            "late_add_to_forecast_pct", "deals_pulled_from_forecast_pct",
            "avg_deal_slip_days", "stage_advancement_accuracy_pct",
            "close_date_accuracy_within_week_pct", "forecast_change_frequency_per_qtr",
            "upside_deals_closed_pct", "commit_deals_lost_pct",
            "sandbag_conversion_rate_pct", "multi_quarter_slip_rate_pct",
            "forecast_submitted_on_time_pct", "total_deals_forecasted",
            "avg_opportunity_value_usd",
        ]
        assert len(fields) == 22
        for f in fields:
            assert hasattr(inp, f), f"Missing field: {f}"

    def test_field_count_is_22(self):
        from dataclasses import fields as dc_fields
        assert len(dc_fields(ForecastInput)) == 22

    def test_string_fields(self):
        inp = make_input()
        assert isinstance(inp.rep_id, str)
        assert isinstance(inp.region, str)
        assert isinstance(inp.evaluation_period_id, str)

    def test_int_field(self):
        inp = make_input()
        assert isinstance(inp.total_deals_forecasted, int)

    def test_float_fields(self):
        inp = make_input()
        float_fields = [
            "forecast_vs_actual_variance_pct", "over_forecast_frequency_pct",
            "under_forecast_frequency_pct", "commit_to_close_rate_pct",
            "best_case_to_close_rate_pct", "pipeline_to_quota_ratio",
            "late_add_to_forecast_pct", "deals_pulled_from_forecast_pct",
            "avg_deal_slip_days", "stage_advancement_accuracy_pct",
            "close_date_accuracy_within_week_pct", "forecast_change_frequency_per_qtr",
            "upside_deals_closed_pct", "commit_deals_lost_pct",
            "sandbag_conversion_rate_pct", "multi_quarter_slip_rate_pct",
            "forecast_submitted_on_time_pct", "avg_opportunity_value_usd",
        ]
        for f in float_fields:
            assert isinstance(getattr(inp, f), float), f"Expected float for {f}"


# ---------------------------------------------------------------------------
# 3. ForecastResult — all 15 fields + to_dict 15 keys
# ---------------------------------------------------------------------------

class TestForecastResult:
    def test_15_fields_present(self, engine):
        result = engine.assess(low_risk_input())
        fields = [
            "rep_id", "region", "forecast_risk", "forecast_pattern",
            "forecast_severity", "recommended_action", "accuracy_score",
            "discipline_score", "stage_score", "commit_score",
            "forecast_composite", "has_forecast_gap", "requires_forecast_coaching",
            "estimated_revenue_at_risk_usd", "forecast_signal",
        ]
        assert len(fields) == 15
        for f in fields:
            assert hasattr(result, f), f"Missing result field: {f}"

    def test_field_count_is_15(self):
        from dataclasses import fields as dc_fields
        assert len(dc_fields(ForecastResult)) == 15

    def test_to_dict_returns_15_keys(self, engine):
        d = engine.assess(low_risk_input()).to_dict()
        assert len(d) == 15

    def test_to_dict_exact_keys(self, engine):
        d = engine.assess(low_risk_input()).to_dict()
        expected_keys = {
            "rep_id", "region", "forecast_risk", "forecast_pattern",
            "forecast_severity", "recommended_action", "accuracy_score",
            "discipline_score", "stage_score", "commit_score",
            "forecast_composite", "has_forecast_gap", "requires_forecast_coaching",
            "estimated_revenue_at_risk_usd", "forecast_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_values_are_strings(self, engine):
        d = engine.assess(low_risk_input()).to_dict()
        assert isinstance(d["forecast_risk"], str)
        assert isinstance(d["forecast_pattern"], str)
        assert isinstance(d["forecast_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_rep_id_and_region(self, engine):
        inp = make_input(rep_id="rep-XYZ", region="East")
        d = engine.assess(inp).to_dict()
        assert d["rep_id"] == "rep-XYZ"
        assert d["region"] == "East"

    def test_to_dict_bool_values_preserved(self, engine):
        d = engine.assess(low_risk_input()).to_dict()
        assert isinstance(d["has_forecast_gap"], bool)
        assert isinstance(d["requires_forecast_coaching"], bool)

    def test_to_dict_numeric_values(self, engine):
        d = engine.assess(low_risk_input()).to_dict()
        for field in ["accuracy_score", "discipline_score", "stage_score",
                      "commit_score", "forecast_composite", "estimated_revenue_at_risk_usd"]:
            assert isinstance(d[field], (int, float)), f"Expected numeric for {field}"

    def test_to_dict_returns_dict_type(self, engine):
        assert isinstance(engine.assess(low_risk_input()).to_dict(), dict)


# ---------------------------------------------------------------------------
# 4. Accuracy sub-score branches and cap
# ---------------------------------------------------------------------------

class TestAccuracyScore:
    """_accuracy_score: higher score = more risk."""

    def _get(self, engine, **kw) -> float:
        return engine._accuracy_score(make_input(**kw))

    # forecast_vs_actual_variance_pct
    def test_variance_below_10_adds_0(self, engine):
        assert self._get(engine,
            forecast_vs_actual_variance_pct=0.05,
            commit_deals_lost_pct=0.05,
            close_date_accuracy_within_week_pct=0.80) == 0.0

    def test_variance_at_10_adds_8(self, engine):
        assert self._get(engine,
            forecast_vs_actual_variance_pct=0.10,
            commit_deals_lost_pct=0.05,
            close_date_accuracy_within_week_pct=0.80) == 8.0

    def test_variance_just_below_20_adds_8(self, engine):
        assert self._get(engine,
            forecast_vs_actual_variance_pct=0.19,
            commit_deals_lost_pct=0.05,
            close_date_accuracy_within_week_pct=0.80) == 8.0

    def test_variance_at_20_adds_22(self, engine):
        assert self._get(engine,
            forecast_vs_actual_variance_pct=0.20,
            commit_deals_lost_pct=0.05,
            close_date_accuracy_within_week_pct=0.80) == 22.0

    def test_variance_just_below_40_adds_22(self, engine):
        assert self._get(engine,
            forecast_vs_actual_variance_pct=0.39,
            commit_deals_lost_pct=0.05,
            close_date_accuracy_within_week_pct=0.80) == 22.0

    def test_variance_at_40_adds_40(self, engine):
        assert self._get(engine,
            forecast_vs_actual_variance_pct=0.40,
            commit_deals_lost_pct=0.05,
            close_date_accuracy_within_week_pct=0.80) == 40.0

    def test_variance_above_40_still_adds_40(self, engine):
        assert self._get(engine,
            forecast_vs_actual_variance_pct=0.99,
            commit_deals_lost_pct=0.05,
            close_date_accuracy_within_week_pct=0.80) == 40.0

    # commit_deals_lost_pct
    def test_commit_lost_below_20_adds_0(self, engine):
        assert self._get(engine,
            commit_deals_lost_pct=0.10,
            forecast_vs_actual_variance_pct=0.05,
            close_date_accuracy_within_week_pct=0.80) == 0.0

    def test_commit_lost_at_20_adds_18(self, engine):
        assert self._get(engine,
            commit_deals_lost_pct=0.20,
            forecast_vs_actual_variance_pct=0.05,
            close_date_accuracy_within_week_pct=0.80) == 18.0

    def test_commit_lost_just_below_40_adds_18(self, engine):
        assert self._get(engine,
            commit_deals_lost_pct=0.39,
            forecast_vs_actual_variance_pct=0.05,
            close_date_accuracy_within_week_pct=0.80) == 18.0

    def test_commit_lost_at_40_adds_35(self, engine):
        assert self._get(engine,
            commit_deals_lost_pct=0.40,
            forecast_vs_actual_variance_pct=0.05,
            close_date_accuracy_within_week_pct=0.80) == 35.0

    def test_commit_lost_above_40_still_adds_35(self, engine):
        assert self._get(engine,
            commit_deals_lost_pct=0.80,
            forecast_vs_actual_variance_pct=0.05,
            close_date_accuracy_within_week_pct=0.80) == 35.0

    # close_date_accuracy_within_week_pct
    def test_close_date_above_55_adds_0(self, engine):
        assert self._get(engine,
            close_date_accuracy_within_week_pct=0.80,
            forecast_vs_actual_variance_pct=0.05,
            commit_deals_lost_pct=0.05) == 0.0

    def test_close_date_at_55_adds_12(self, engine):
        assert self._get(engine,
            close_date_accuracy_within_week_pct=0.55,
            forecast_vs_actual_variance_pct=0.05,
            commit_deals_lost_pct=0.05) == 12.0

    def test_close_date_just_above_30_adds_12(self, engine):
        assert self._get(engine,
            close_date_accuracy_within_week_pct=0.31,
            forecast_vs_actual_variance_pct=0.05,
            commit_deals_lost_pct=0.05) == 12.0

    def test_close_date_at_30_adds_25(self, engine):
        assert self._get(engine,
            close_date_accuracy_within_week_pct=0.30,
            forecast_vs_actual_variance_pct=0.05,
            commit_deals_lost_pct=0.05) == 25.0

    def test_close_date_below_30_adds_25(self, engine):
        assert self._get(engine,
            close_date_accuracy_within_week_pct=0.10,
            forecast_vs_actual_variance_pct=0.05,
            commit_deals_lost_pct=0.05) == 25.0

    # cap
    def test_accuracy_score_exactly_100(self, engine):
        # 40 + 35 + 25 = 100
        score = self._get(engine,
            forecast_vs_actual_variance_pct=0.50,
            commit_deals_lost_pct=0.50,
            close_date_accuracy_within_week_pct=0.20)
        assert score == 100.0

    def test_accuracy_score_capped_at_100(self, engine):
        score = engine._accuracy_score(make_input(
            forecast_vs_actual_variance_pct=0.99,
            commit_deals_lost_pct=0.99,
            close_date_accuracy_within_week_pct=0.01))
        assert score <= 100.0


# ---------------------------------------------------------------------------
# 5. Discipline sub-score branches and cap
# ---------------------------------------------------------------------------

class TestDisciplineScore:
    def _get(self, engine, **kw) -> float:
        return engine._discipline_score(make_input(**kw))

    # forecast_change_frequency_per_qtr
    def test_change_freq_below_15_adds_0(self, engine):
        assert self._get(engine,
            forecast_change_frequency_per_qtr=1.0,
            late_add_to_forecast_pct=0.05,
            multi_quarter_slip_rate_pct=0.05) == 0.0

    def test_change_freq_at_15_adds_8(self, engine):
        assert self._get(engine,
            forecast_change_frequency_per_qtr=1.5,
            late_add_to_forecast_pct=0.05,
            multi_quarter_slip_rate_pct=0.05) == 8.0

    def test_change_freq_just_below_3_adds_8(self, engine):
        assert self._get(engine,
            forecast_change_frequency_per_qtr=2.9,
            late_add_to_forecast_pct=0.05,
            multi_quarter_slip_rate_pct=0.05) == 8.0

    def test_change_freq_at_3_adds_22(self, engine):
        assert self._get(engine,
            forecast_change_frequency_per_qtr=3.0,
            late_add_to_forecast_pct=0.05,
            multi_quarter_slip_rate_pct=0.05) == 22.0

    def test_change_freq_just_below_5_adds_22(self, engine):
        assert self._get(engine,
            forecast_change_frequency_per_qtr=4.9,
            late_add_to_forecast_pct=0.05,
            multi_quarter_slip_rate_pct=0.05) == 22.0

    def test_change_freq_at_5_adds_40(self, engine):
        assert self._get(engine,
            forecast_change_frequency_per_qtr=5.0,
            late_add_to_forecast_pct=0.05,
            multi_quarter_slip_rate_pct=0.05) == 40.0

    def test_change_freq_above_5_still_adds_40(self, engine):
        assert self._get(engine,
            forecast_change_frequency_per_qtr=10.0,
            late_add_to_forecast_pct=0.05,
            multi_quarter_slip_rate_pct=0.05) == 40.0

    # late_add_to_forecast_pct
    def test_late_add_below_20_adds_0(self, engine):
        assert self._get(engine,
            late_add_to_forecast_pct=0.10,
            forecast_change_frequency_per_qtr=0.5,
            multi_quarter_slip_rate_pct=0.05) == 0.0

    def test_late_add_at_20_adds_18(self, engine):
        assert self._get(engine,
            late_add_to_forecast_pct=0.20,
            forecast_change_frequency_per_qtr=0.5,
            multi_quarter_slip_rate_pct=0.05) == 18.0

    def test_late_add_just_below_40_adds_18(self, engine):
        assert self._get(engine,
            late_add_to_forecast_pct=0.39,
            forecast_change_frequency_per_qtr=0.5,
            multi_quarter_slip_rate_pct=0.05) == 18.0

    def test_late_add_at_40_adds_35(self, engine):
        assert self._get(engine,
            late_add_to_forecast_pct=0.40,
            forecast_change_frequency_per_qtr=0.5,
            multi_quarter_slip_rate_pct=0.05) == 35.0

    def test_late_add_above_40_still_adds_35(self, engine):
        assert self._get(engine,
            late_add_to_forecast_pct=0.80,
            forecast_change_frequency_per_qtr=0.5,
            multi_quarter_slip_rate_pct=0.05) == 35.0

    # multi_quarter_slip_rate_pct
    def test_slip_below_15_adds_0(self, engine):
        assert self._get(engine,
            multi_quarter_slip_rate_pct=0.10,
            forecast_change_frequency_per_qtr=0.5,
            late_add_to_forecast_pct=0.05) == 0.0

    def test_slip_at_15_adds_12(self, engine):
        assert self._get(engine,
            multi_quarter_slip_rate_pct=0.15,
            forecast_change_frequency_per_qtr=0.5,
            late_add_to_forecast_pct=0.05) == 12.0

    def test_slip_just_below_35_adds_12(self, engine):
        assert self._get(engine,
            multi_quarter_slip_rate_pct=0.34,
            forecast_change_frequency_per_qtr=0.5,
            late_add_to_forecast_pct=0.05) == 12.0

    def test_slip_at_35_adds_25(self, engine):
        assert self._get(engine,
            multi_quarter_slip_rate_pct=0.35,
            forecast_change_frequency_per_qtr=0.5,
            late_add_to_forecast_pct=0.05) == 25.0

    def test_slip_above_35_still_adds_25(self, engine):
        assert self._get(engine,
            multi_quarter_slip_rate_pct=0.80,
            forecast_change_frequency_per_qtr=0.5,
            late_add_to_forecast_pct=0.05) == 25.0

    # cap
    def test_discipline_score_exactly_100(self, engine):
        # 40 + 35 + 25 = 100
        score = self._get(engine,
            forecast_change_frequency_per_qtr=6.0,
            late_add_to_forecast_pct=0.50,
            multi_quarter_slip_rate_pct=0.40)
        assert score == 100.0

    def test_discipline_score_capped_at_100(self, engine):
        score = engine._discipline_score(make_input(
            forecast_change_frequency_per_qtr=99.0,
            late_add_to_forecast_pct=0.99,
            multi_quarter_slip_rate_pct=0.99))
        assert score <= 100.0


# ---------------------------------------------------------------------------
# 6. Stage sub-score branches and cap
# ---------------------------------------------------------------------------

class TestStageScore:
    def _get(self, engine, **kw) -> float:
        return engine._stage_score(make_input(**kw))

    # stage_advancement_accuracy_pct
    def test_stage_acc_above_75_adds_0(self, engine):
        assert self._get(engine,
            stage_advancement_accuracy_pct=0.80,
            deals_pulled_from_forecast_pct=0.05,
            avg_deal_slip_days=5.0) == 0.0

    def test_stage_acc_at_75_adds_8(self, engine):
        assert self._get(engine,
            stage_advancement_accuracy_pct=0.75,
            deals_pulled_from_forecast_pct=0.05,
            avg_deal_slip_days=5.0) == 8.0

    def test_stage_acc_just_above_60_adds_8(self, engine):
        assert self._get(engine,
            stage_advancement_accuracy_pct=0.61,
            deals_pulled_from_forecast_pct=0.05,
            avg_deal_slip_days=5.0) == 8.0

    def test_stage_acc_at_60_adds_22(self, engine):
        assert self._get(engine,
            stage_advancement_accuracy_pct=0.60,
            deals_pulled_from_forecast_pct=0.05,
            avg_deal_slip_days=5.0) == 22.0

    def test_stage_acc_just_above_40_adds_22(self, engine):
        assert self._get(engine,
            stage_advancement_accuracy_pct=0.41,
            deals_pulled_from_forecast_pct=0.05,
            avg_deal_slip_days=5.0) == 22.0

    def test_stage_acc_at_40_adds_40(self, engine):
        assert self._get(engine,
            stage_advancement_accuracy_pct=0.40,
            deals_pulled_from_forecast_pct=0.05,
            avg_deal_slip_days=5.0) == 40.0

    def test_stage_acc_below_40_still_adds_40(self, engine):
        assert self._get(engine,
            stage_advancement_accuracy_pct=0.10,
            deals_pulled_from_forecast_pct=0.05,
            avg_deal_slip_days=5.0) == 40.0

    # deals_pulled_from_forecast_pct
    def test_deals_pulled_below_20_adds_0(self, engine):
        assert self._get(engine,
            deals_pulled_from_forecast_pct=0.10,
            stage_advancement_accuracy_pct=0.90,
            avg_deal_slip_days=5.0) == 0.0

    def test_deals_pulled_at_20_adds_18(self, engine):
        assert self._get(engine,
            deals_pulled_from_forecast_pct=0.20,
            stage_advancement_accuracy_pct=0.90,
            avg_deal_slip_days=5.0) == 18.0

    def test_deals_pulled_just_below_35_adds_18(self, engine):
        assert self._get(engine,
            deals_pulled_from_forecast_pct=0.34,
            stage_advancement_accuracy_pct=0.90,
            avg_deal_slip_days=5.0) == 18.0

    def test_deals_pulled_at_35_adds_35(self, engine):
        assert self._get(engine,
            deals_pulled_from_forecast_pct=0.35,
            stage_advancement_accuracy_pct=0.90,
            avg_deal_slip_days=5.0) == 35.0

    def test_deals_pulled_above_35_still_adds_35(self, engine):
        assert self._get(engine,
            deals_pulled_from_forecast_pct=0.80,
            stage_advancement_accuracy_pct=0.90,
            avg_deal_slip_days=5.0) == 35.0

    # avg_deal_slip_days
    def test_slip_days_below_14_adds_0(self, engine):
        assert self._get(engine,
            avg_deal_slip_days=10.0,
            stage_advancement_accuracy_pct=0.90,
            deals_pulled_from_forecast_pct=0.05) == 0.0

    def test_slip_days_at_14_adds_12(self, engine):
        assert self._get(engine,
            avg_deal_slip_days=14.0,
            stage_advancement_accuracy_pct=0.90,
            deals_pulled_from_forecast_pct=0.05) == 12.0

    def test_slip_days_just_below_30_adds_12(self, engine):
        assert self._get(engine,
            avg_deal_slip_days=29.9,
            stage_advancement_accuracy_pct=0.90,
            deals_pulled_from_forecast_pct=0.05) == 12.0

    def test_slip_days_at_30_adds_25(self, engine):
        assert self._get(engine,
            avg_deal_slip_days=30.0,
            stage_advancement_accuracy_pct=0.90,
            deals_pulled_from_forecast_pct=0.05) == 25.0

    def test_slip_days_above_30_still_adds_25(self, engine):
        assert self._get(engine,
            avg_deal_slip_days=90.0,
            stage_advancement_accuracy_pct=0.90,
            deals_pulled_from_forecast_pct=0.05) == 25.0

    # cap
    def test_stage_score_exactly_100(self, engine):
        # 40 + 35 + 25 = 100
        score = self._get(engine,
            stage_advancement_accuracy_pct=0.30,
            deals_pulled_from_forecast_pct=0.40,
            avg_deal_slip_days=35.0)
        assert score == 100.0

    def test_stage_score_capped_at_100(self, engine):
        score = engine._stage_score(make_input(
            stage_advancement_accuracy_pct=0.01,
            deals_pulled_from_forecast_pct=0.99,
            avg_deal_slip_days=999.0))
        assert score <= 100.0


# ---------------------------------------------------------------------------
# 7. Commit sub-score branches and cap
# ---------------------------------------------------------------------------

class TestCommitScore:
    def _get(self, engine, **kw) -> float:
        return engine._commit_score(make_input(**kw))

    # commit_to_close_rate_pct
    def test_commit_close_above_75_adds_0(self, engine):
        assert self._get(engine,
            commit_to_close_rate_pct=0.80,
            over_forecast_frequency_pct=0.10,
            under_forecast_frequency_pct=0.10) == 0.0

    def test_commit_close_at_75_adds_10(self, engine):
        assert self._get(engine,
            commit_to_close_rate_pct=0.75,
            over_forecast_frequency_pct=0.10,
            under_forecast_frequency_pct=0.10) == 10.0

    def test_commit_close_just_above_60_adds_10(self, engine):
        assert self._get(engine,
            commit_to_close_rate_pct=0.61,
            over_forecast_frequency_pct=0.10,
            under_forecast_frequency_pct=0.10) == 10.0

    def test_commit_close_at_60_adds_25(self, engine):
        assert self._get(engine,
            commit_to_close_rate_pct=0.60,
            over_forecast_frequency_pct=0.10,
            under_forecast_frequency_pct=0.10) == 25.0

    def test_commit_close_just_above_40_adds_25(self, engine):
        assert self._get(engine,
            commit_to_close_rate_pct=0.41,
            over_forecast_frequency_pct=0.10,
            under_forecast_frequency_pct=0.10) == 25.0

    def test_commit_close_at_40_adds_45(self, engine):
        assert self._get(engine,
            commit_to_close_rate_pct=0.40,
            over_forecast_frequency_pct=0.10,
            under_forecast_frequency_pct=0.10) == 45.0

    def test_commit_close_below_40_still_adds_45(self, engine):
        assert self._get(engine,
            commit_to_close_rate_pct=0.10,
            over_forecast_frequency_pct=0.10,
            under_forecast_frequency_pct=0.10) == 45.0

    # over_forecast_frequency_pct
    def test_over_forecast_below_40_adds_0(self, engine):
        assert self._get(engine,
            over_forecast_frequency_pct=0.30,
            commit_to_close_rate_pct=0.90,
            under_forecast_frequency_pct=0.10) == 0.0

    def test_over_forecast_at_40_adds_15(self, engine):
        assert self._get(engine,
            over_forecast_frequency_pct=0.40,
            commit_to_close_rate_pct=0.90,
            under_forecast_frequency_pct=0.10) == 15.0

    def test_over_forecast_just_below_60_adds_15(self, engine):
        assert self._get(engine,
            over_forecast_frequency_pct=0.59,
            commit_to_close_rate_pct=0.90,
            under_forecast_frequency_pct=0.10) == 15.0

    def test_over_forecast_at_60_adds_30(self, engine):
        assert self._get(engine,
            over_forecast_frequency_pct=0.60,
            commit_to_close_rate_pct=0.90,
            under_forecast_frequency_pct=0.10) == 30.0

    def test_over_forecast_above_60_still_adds_30(self, engine):
        assert self._get(engine,
            over_forecast_frequency_pct=0.90,
            commit_to_close_rate_pct=0.90,
            under_forecast_frequency_pct=0.10) == 30.0

    # under_forecast_frequency_pct
    def test_under_forecast_below_30_adds_0(self, engine):
        assert self._get(engine,
            under_forecast_frequency_pct=0.20,
            commit_to_close_rate_pct=0.90,
            over_forecast_frequency_pct=0.10) == 0.0

    def test_under_forecast_at_30_adds_12(self, engine):
        assert self._get(engine,
            under_forecast_frequency_pct=0.30,
            commit_to_close_rate_pct=0.90,
            over_forecast_frequency_pct=0.10) == 12.0

    def test_under_forecast_just_below_50_adds_12(self, engine):
        assert self._get(engine,
            under_forecast_frequency_pct=0.49,
            commit_to_close_rate_pct=0.90,
            over_forecast_frequency_pct=0.10) == 12.0

    def test_under_forecast_at_50_adds_25(self, engine):
        assert self._get(engine,
            under_forecast_frequency_pct=0.50,
            commit_to_close_rate_pct=0.90,
            over_forecast_frequency_pct=0.10) == 25.0

    def test_under_forecast_above_50_still_adds_25(self, engine):
        assert self._get(engine,
            under_forecast_frequency_pct=0.90,
            commit_to_close_rate_pct=0.90,
            over_forecast_frequency_pct=0.10) == 25.0

    # cap
    def test_commit_score_exactly_100(self, engine):
        # 45 + 30 + 25 = 100
        score = self._get(engine,
            commit_to_close_rate_pct=0.30,
            over_forecast_frequency_pct=0.70,
            under_forecast_frequency_pct=0.60)
        assert score == 100.0

    def test_commit_score_capped_at_100(self, engine):
        score = engine._commit_score(make_input(
            commit_to_close_rate_pct=0.01,
            over_forecast_frequency_pct=0.99,
            under_forecast_frequency_pct=0.99))
        assert score <= 100.0


# ---------------------------------------------------------------------------
# 8. Composite formula and weights
# ---------------------------------------------------------------------------

class TestCompositeFormula:
    def test_composite_weights(self, engine):
        """accuracy*0.35 + discipline*0.25 + stage*0.25 + commit*0.15"""
        # accuracy: variance=0.10 (+8), commit_lost=0.20 (+18), close_date=0.80 (+0) = 26
        # discipline: change_freq=1.5 (+8), late_add=0.05 (+0), slip=0.05 (+0) = 8
        # stage: stage_acc=0.90 (+0), deals_pulled=0.05 (+0), slip_days=5.0 (+0) = 0
        # commit: commit_close=0.90 (+0), over_freq=0.10 (+0), under_freq=0.10 (+0) = 0
        inp = make_input(
            forecast_vs_actual_variance_pct=0.10,
            commit_deals_lost_pct=0.20,
            close_date_accuracy_within_week_pct=0.80,
            forecast_change_frequency_per_qtr=1.5,
            late_add_to_forecast_pct=0.05,
            multi_quarter_slip_rate_pct=0.05,
            stage_advancement_accuracy_pct=0.90,
            deals_pulled_from_forecast_pct=0.05,
            avg_deal_slip_days=5.0,
            commit_to_close_rate_pct=0.90,
            over_forecast_frequency_pct=0.10,
            under_forecast_frequency_pct=0.10,
        )
        result = engine.assess(inp)
        assert result.accuracy_score == 26.0
        assert result.discipline_score == 8.0
        assert result.stage_score == 0.0
        assert result.commit_score == 0.0
        expected = round(26.0 * 0.35 + 8.0 * 0.25 + 0.0 * 0.25 + 0.0 * 0.15, 1)
        assert result.forecast_composite == expected

    def test_composite_capped_at_100(self, engine):
        result = engine.assess(critical_input())
        assert result.forecast_composite <= 100.0

    def test_composite_all_zeros(self, engine):
        result = engine.assess(low_risk_input())
        assert result.forecast_composite == 0.0

    def test_composite_weighted_sum_formula(self, engine):
        # Use known-value inputs to verify weights exactly
        # accuracy=40, discipline=40, stage=40, commit=45 but commit capped still 45
        # composite = 40*0.35 + 40*0.25 + 40*0.25 + 45*0.15 = 14+10+10+6.75 = 40.75
        inp = make_input(
            forecast_vs_actual_variance_pct=0.50,   # +40 accuracy
            commit_deals_lost_pct=0.05,
            close_date_accuracy_within_week_pct=0.80,
            forecast_change_frequency_per_qtr=5.0,  # +40 discipline
            late_add_to_forecast_pct=0.05,
            multi_quarter_slip_rate_pct=0.05,
            stage_advancement_accuracy_pct=0.40,    # +40 stage
            deals_pulled_from_forecast_pct=0.05,
            avg_deal_slip_days=5.0,
            commit_to_close_rate_pct=0.40,          # +45 commit
            over_forecast_frequency_pct=0.10,
            under_forecast_frequency_pct=0.10,
        )
        result = engine.assess(inp)
        assert result.accuracy_score == 40.0
        assert result.discipline_score == 40.0
        assert result.stage_score == 40.0
        assert result.commit_score == 45.0
        expected = round(40.0 * 0.35 + 40.0 * 0.25 + 40.0 * 0.25 + 45.0 * 0.15, 1)
        assert result.forecast_composite == expected

    def test_scores_rounded_to_1dp(self, engine):
        result = engine.assess(make_input(forecast_vs_actual_variance_pct=0.15))
        for score in [result.accuracy_score, result.discipline_score,
                      result.stage_score, result.commit_score,
                      result.forecast_composite]:
            assert round(score, 1) == score


# ---------------------------------------------------------------------------
# 9. Pattern detection — all 6 patterns and priority
# ---------------------------------------------------------------------------

class TestPatternDetection:
    """
    Priority order:
    1. stage_inflation_blindspot
    2. chronic_over_forecasting
    3. end_of_quarter_cliff
    4. recency_bias_sandbagging
    5. chronic_under_forecasting
    6. none
    """

    def _detect(self, engine, **kw) -> ForecastPattern:
        inp = make_input(**kw)
        acc = engine._accuracy_score(inp)
        dis = engine._discipline_score(inp)
        sta = engine._stage_score(inp)
        com = engine._commit_score(inp)
        return engine._detect_pattern(inp, acc, dis, sta, com)

    # --- none ---
    def test_no_pattern_for_healthy_rep(self, engine):
        assert self._detect(engine) == ForecastPattern.none

    # --- stage_inflation_blindspot ---
    def test_stage_inflation_blindspot_detected(self, engine):
        pattern = self._detect(engine,
            stage_advancement_accuracy_pct=0.35,
            deals_pulled_from_forecast_pct=0.30)
        assert pattern == ForecastPattern.stage_inflation_blindspot

    def test_stage_inflation_at_exact_boundaries(self, engine):
        pattern = self._detect(engine,
            stage_advancement_accuracy_pct=0.35,
            deals_pulled_from_forecast_pct=0.30)
        assert pattern == ForecastPattern.stage_inflation_blindspot

    def test_stage_inflation_stage_acc_just_above_35_no_match(self, engine):
        pattern = self._detect(engine,
            stage_advancement_accuracy_pct=0.36,
            deals_pulled_from_forecast_pct=0.30)
        assert pattern != ForecastPattern.stage_inflation_blindspot

    def test_stage_inflation_deals_pulled_just_below_30_no_match(self, engine):
        pattern = self._detect(engine,
            stage_advancement_accuracy_pct=0.35,
            deals_pulled_from_forecast_pct=0.29)
        assert pattern != ForecastPattern.stage_inflation_blindspot

    # --- chronic_over_forecasting ---
    def test_chronic_over_forecasting_detected(self, engine):
        pattern = self._detect(engine,
            over_forecast_frequency_pct=0.55,
            commit_deals_lost_pct=0.30,
            stage_advancement_accuracy_pct=0.90,   # avoid blindspot
            deals_pulled_from_forecast_pct=0.05)
        assert pattern == ForecastPattern.chronic_over_forecasting

    def test_chronic_over_forecasting_at_exact_boundaries(self, engine):
        pattern = self._detect(engine,
            over_forecast_frequency_pct=0.55,
            commit_deals_lost_pct=0.30,
            stage_advancement_accuracy_pct=0.90,
            deals_pulled_from_forecast_pct=0.05)
        assert pattern == ForecastPattern.chronic_over_forecasting

    def test_chronic_over_freq_just_below_55_no_match(self, engine):
        pattern = self._detect(engine,
            over_forecast_frequency_pct=0.54,
            commit_deals_lost_pct=0.30,
            stage_advancement_accuracy_pct=0.90,
            deals_pulled_from_forecast_pct=0.05)
        assert pattern != ForecastPattern.chronic_over_forecasting

    def test_chronic_over_commit_lost_just_below_30_no_match(self, engine):
        pattern = self._detect(engine,
            over_forecast_frequency_pct=0.55,
            commit_deals_lost_pct=0.29,
            stage_advancement_accuracy_pct=0.90,
            deals_pulled_from_forecast_pct=0.05)
        assert pattern != ForecastPattern.chronic_over_forecasting

    # --- end_of_quarter_cliff ---
    def test_end_of_quarter_cliff_detected(self, engine):
        # discipline >= 35: change_freq=5.0 → +40 → discipline=40 >= 35
        inp = make_input(
            forecast_change_frequency_per_qtr=5.0,
            late_add_to_forecast_pct=0.05,
            multi_quarter_slip_rate_pct=0.25,
            stage_advancement_accuracy_pct=0.90,
            deals_pulled_from_forecast_pct=0.05,
            over_forecast_frequency_pct=0.10,
            commit_deals_lost_pct=0.05,
        )
        acc = engine._accuracy_score(inp)
        dis = engine._discipline_score(inp)
        sta = engine._stage_score(inp)
        com = engine._commit_score(inp)
        assert dis >= 35.0
        pattern = engine._detect_pattern(inp, acc, dis, sta, com)
        assert pattern == ForecastPattern.end_of_quarter_cliff

    def test_end_of_quarter_cliff_discipline_just_below_35_no_match(self, engine):
        # discipline=22 (change_freq=3.0, no other discipline pts)
        inp = make_input(
            forecast_change_frequency_per_qtr=3.0,
            late_add_to_forecast_pct=0.05,
            multi_quarter_slip_rate_pct=0.25,
            stage_advancement_accuracy_pct=0.90,
            deals_pulled_from_forecast_pct=0.05,
            over_forecast_frequency_pct=0.10,
            commit_deals_lost_pct=0.05,
        )
        acc = engine._accuracy_score(inp)
        dis = engine._discipline_score(inp)
        sta = engine._stage_score(inp)
        com = engine._commit_score(inp)
        # change_freq=3.0 (+22) + slip=0.25 (+12) = 34, still < 35
        assert dis == 34.0
        assert dis < 35.0
        pattern = engine._detect_pattern(inp, acc, dis, sta, com)
        assert pattern != ForecastPattern.end_of_quarter_cliff

    def test_end_of_quarter_cliff_slip_just_below_25_no_match(self, engine):
        inp = make_input(
            forecast_change_frequency_per_qtr=5.0,
            late_add_to_forecast_pct=0.05,
            multi_quarter_slip_rate_pct=0.24,
            stage_advancement_accuracy_pct=0.90,
            deals_pulled_from_forecast_pct=0.05,
            over_forecast_frequency_pct=0.10,
            commit_deals_lost_pct=0.05,
        )
        acc = engine._accuracy_score(inp)
        dis = engine._discipline_score(inp)
        sta = engine._stage_score(inp)
        com = engine._commit_score(inp)
        pattern = engine._detect_pattern(inp, acc, dis, sta, com)
        assert pattern != ForecastPattern.end_of_quarter_cliff

    # --- recency_bias_sandbagging ---
    def test_recency_bias_sandbagging_detected(self, engine):
        pattern = self._detect(engine,
            sandbag_conversion_rate_pct=0.50,
            late_add_to_forecast_pct=0.30,
            stage_advancement_accuracy_pct=0.90,
            deals_pulled_from_forecast_pct=0.05,
            over_forecast_frequency_pct=0.10,
            commit_deals_lost_pct=0.05,
            forecast_change_frequency_per_qtr=0.5,
            multi_quarter_slip_rate_pct=0.05)
        assert pattern == ForecastPattern.recency_bias_sandbagging

    def test_recency_bias_at_exact_boundaries(self, engine):
        pattern = self._detect(engine,
            sandbag_conversion_rate_pct=0.50,
            late_add_to_forecast_pct=0.30,
            stage_advancement_accuracy_pct=0.90,
            deals_pulled_from_forecast_pct=0.05,
            over_forecast_frequency_pct=0.10,
            commit_deals_lost_pct=0.05,
            forecast_change_frequency_per_qtr=0.5,
            multi_quarter_slip_rate_pct=0.05)
        assert pattern == ForecastPattern.recency_bias_sandbagging

    def test_recency_bias_sandbag_just_below_50_no_match(self, engine):
        pattern = self._detect(engine,
            sandbag_conversion_rate_pct=0.49,
            late_add_to_forecast_pct=0.30,
            stage_advancement_accuracy_pct=0.90,
            deals_pulled_from_forecast_pct=0.05,
            over_forecast_frequency_pct=0.10,
            commit_deals_lost_pct=0.05,
            forecast_change_frequency_per_qtr=0.5,
            multi_quarter_slip_rate_pct=0.05)
        assert pattern != ForecastPattern.recency_bias_sandbagging

    def test_recency_bias_late_add_just_below_30_no_match(self, engine):
        pattern = self._detect(engine,
            sandbag_conversion_rate_pct=0.50,
            late_add_to_forecast_pct=0.29,
            stage_advancement_accuracy_pct=0.90,
            deals_pulled_from_forecast_pct=0.05,
            over_forecast_frequency_pct=0.10,
            commit_deals_lost_pct=0.05,
            forecast_change_frequency_per_qtr=0.5,
            multi_quarter_slip_rate_pct=0.05)
        assert pattern != ForecastPattern.recency_bias_sandbagging

    # --- chronic_under_forecasting ---
    def test_chronic_under_forecasting_detected(self, engine):
        # under_freq >= 0.45 and commit_score >= 30
        # commit_score: commit_to_close=0.60 (+25), under_freq=0.45 (+12) → commit=37
        inp = make_input(
            under_forecast_frequency_pct=0.45,
            commit_to_close_rate_pct=0.60,
            stage_advancement_accuracy_pct=0.90,
            deals_pulled_from_forecast_pct=0.05,
            over_forecast_frequency_pct=0.10,
            commit_deals_lost_pct=0.05,
            forecast_change_frequency_per_qtr=0.5,
            multi_quarter_slip_rate_pct=0.05,
            sandbag_conversion_rate_pct=0.10,
            late_add_to_forecast_pct=0.05,
        )
        acc = engine._accuracy_score(inp)
        dis = engine._discipline_score(inp)
        sta = engine._stage_score(inp)
        com = engine._commit_score(inp)
        assert com >= 30
        pattern = engine._detect_pattern(inp, acc, dis, sta, com)
        assert pattern == ForecastPattern.chronic_under_forecasting

    def test_chronic_under_freq_just_below_45_no_match(self, engine):
        inp = make_input(
            under_forecast_frequency_pct=0.44,
            commit_to_close_rate_pct=0.60,
            stage_advancement_accuracy_pct=0.90,
            deals_pulled_from_forecast_pct=0.05,
            over_forecast_frequency_pct=0.10,
            commit_deals_lost_pct=0.05,
            forecast_change_frequency_per_qtr=0.5,
            multi_quarter_slip_rate_pct=0.05,
            sandbag_conversion_rate_pct=0.10,
            late_add_to_forecast_pct=0.05,
        )
        acc = engine._accuracy_score(inp)
        dis = engine._discipline_score(inp)
        sta = engine._stage_score(inp)
        com = engine._commit_score(inp)
        pattern = engine._detect_pattern(inp, acc, dis, sta, com)
        assert pattern != ForecastPattern.chronic_under_forecasting

    # --- priority tests ---
    def test_stage_inflation_overrides_chronic_over_forecasting(self, engine):
        # Both conditions met
        pattern = self._detect(engine,
            stage_advancement_accuracy_pct=0.35,
            deals_pulled_from_forecast_pct=0.30,
            over_forecast_frequency_pct=0.55,
            commit_deals_lost_pct=0.30)
        assert pattern == ForecastPattern.stage_inflation_blindspot

    def test_chronic_over_overrides_end_of_quarter(self, engine):
        inp = make_input(
            over_forecast_frequency_pct=0.55,
            commit_deals_lost_pct=0.30,
            forecast_change_frequency_per_qtr=5.0,
            multi_quarter_slip_rate_pct=0.25,
            stage_advancement_accuracy_pct=0.90,
            deals_pulled_from_forecast_pct=0.05,
            late_add_to_forecast_pct=0.05,
        )
        acc = engine._accuracy_score(inp)
        dis = engine._discipline_score(inp)
        sta = engine._stage_score(inp)
        com = engine._commit_score(inp)
        pattern = engine._detect_pattern(inp, acc, dis, sta, com)
        assert pattern == ForecastPattern.chronic_over_forecasting

    def test_stage_inflation_overrides_all_others(self, engine):
        # All conditions simultaneously met — stage_inflation should win
        inp = make_input(
            stage_advancement_accuracy_pct=0.35,
            deals_pulled_from_forecast_pct=0.30,
            over_forecast_frequency_pct=0.55,
            commit_deals_lost_pct=0.30,
            forecast_change_frequency_per_qtr=5.0,
            multi_quarter_slip_rate_pct=0.25,
            sandbag_conversion_rate_pct=0.50,
            late_add_to_forecast_pct=0.30,
            under_forecast_frequency_pct=0.45,
            commit_to_close_rate_pct=0.40,
        )
        acc = engine._accuracy_score(inp)
        dis = engine._discipline_score(inp)
        sta = engine._stage_score(inp)
        com = engine._commit_score(inp)
        pattern = engine._detect_pattern(inp, acc, dis, sta, com)
        assert pattern == ForecastPattern.stage_inflation_blindspot


# ---------------------------------------------------------------------------
# 10. Risk thresholds
# ---------------------------------------------------------------------------

class TestRiskLevel:
    def test_risk_low_at_zero(self, engine):
        assert engine._risk_level(0.0) == ForecastRisk.low

    def test_risk_low_just_below_20(self, engine):
        assert engine._risk_level(19.9) == ForecastRisk.low

    def test_risk_moderate_at_20(self, engine):
        assert engine._risk_level(20.0) == ForecastRisk.moderate

    def test_risk_moderate_just_below_40(self, engine):
        assert engine._risk_level(39.9) == ForecastRisk.moderate

    def test_risk_high_at_40(self, engine):
        assert engine._risk_level(40.0) == ForecastRisk.high

    def test_risk_high_just_below_60(self, engine):
        assert engine._risk_level(59.9) == ForecastRisk.high

    def test_risk_critical_at_60(self, engine):
        assert engine._risk_level(60.0) == ForecastRisk.critical

    def test_risk_critical_at_100(self, engine):
        assert engine._risk_level(100.0) == ForecastRisk.critical


# ---------------------------------------------------------------------------
# 11. Severity thresholds
# ---------------------------------------------------------------------------

class TestSeverity:
    def test_severity_precise_at_zero(self, engine):
        assert engine._severity(0.0) == ForecastSeverity.precise

    def test_severity_precise_just_below_20(self, engine):
        assert engine._severity(19.9) == ForecastSeverity.precise

    def test_severity_calibrating_at_20(self, engine):
        assert engine._severity(20.0) == ForecastSeverity.calibrating

    def test_severity_calibrating_just_below_40(self, engine):
        assert engine._severity(39.9) == ForecastSeverity.calibrating

    def test_severity_drifting_at_40(self, engine):
        assert engine._severity(40.0) == ForecastSeverity.drifting

    def test_severity_drifting_just_below_60(self, engine):
        assert engine._severity(59.9) == ForecastSeverity.drifting

    def test_severity_unreliable_at_60(self, engine):
        assert engine._severity(60.0) == ForecastSeverity.unreliable

    def test_severity_unreliable_at_100(self, engine):
        assert engine._severity(100.0) == ForecastSeverity.unreliable

    def test_severity_mirrors_risk_thresholds(self, engine):
        """Risk and severity use same composite thresholds."""
        pairs = [
            (0.0, ForecastSeverity.precise),
            (19.9, ForecastSeverity.precise),
            (20.0, ForecastSeverity.calibrating),
            (39.9, ForecastSeverity.calibrating),
            (40.0, ForecastSeverity.drifting),
            (59.9, ForecastSeverity.drifting),
            (60.0, ForecastSeverity.unreliable),
            (100.0, ForecastSeverity.unreliable),
        ]
        for composite, expected_sev in pairs:
            assert engine._severity(composite) == expected_sev


# ---------------------------------------------------------------------------
# 12. Action mappings — all branches
# ---------------------------------------------------------------------------

class TestActionMapping:
    # critical
    def test_critical_stage_inflation_blindspot(self, engine):
        assert engine._action(ForecastRisk.critical, ForecastPattern.stage_inflation_blindspot) \
               == ForecastAction.stage_criteria_coaching

    def test_critical_chronic_over_forecasting(self, engine):
        assert engine._action(ForecastRisk.critical, ForecastPattern.chronic_over_forecasting) \
               == ForecastAction.commit_discipline_coaching

    def test_critical_end_of_quarter_cliff(self, engine):
        assert engine._action(ForecastRisk.critical, ForecastPattern.end_of_quarter_cliff) \
               == ForecastAction.forecast_reset_intervention

    def test_critical_recency_bias_sandbagging(self, engine):
        assert engine._action(ForecastRisk.critical, ForecastPattern.recency_bias_sandbagging) \
               == ForecastAction.forecast_reset_intervention

    def test_critical_chronic_under_forecasting(self, engine):
        assert engine._action(ForecastRisk.critical, ForecastPattern.chronic_under_forecasting) \
               == ForecastAction.forecast_reset_intervention

    def test_critical_none(self, engine):
        assert engine._action(ForecastRisk.critical, ForecastPattern.none) \
               == ForecastAction.forecast_reset_intervention

    # high
    def test_high_end_of_quarter_cliff(self, engine):
        assert engine._action(ForecastRisk.high, ForecastPattern.end_of_quarter_cliff) \
               == ForecastAction.pipeline_inspection_coaching

    def test_high_recency_bias_sandbagging(self, engine):
        assert engine._action(ForecastRisk.high, ForecastPattern.recency_bias_sandbagging) \
               == ForecastAction.forecast_calibration_coaching

    def test_high_stage_inflation_blindspot(self, engine):
        assert engine._action(ForecastRisk.high, ForecastPattern.stage_inflation_blindspot) \
               == ForecastAction.commit_discipline_coaching

    def test_high_chronic_over_forecasting(self, engine):
        assert engine._action(ForecastRisk.high, ForecastPattern.chronic_over_forecasting) \
               == ForecastAction.commit_discipline_coaching

    def test_high_chronic_under_forecasting(self, engine):
        assert engine._action(ForecastRisk.high, ForecastPattern.chronic_under_forecasting) \
               == ForecastAction.commit_discipline_coaching

    def test_high_none(self, engine):
        assert engine._action(ForecastRisk.high, ForecastPattern.none) \
               == ForecastAction.commit_discipline_coaching

    # moderate — always forecast_calibration_coaching regardless of pattern
    def test_moderate_all_patterns(self, engine):
        for p in ForecastPattern:
            assert engine._action(ForecastRisk.moderate, p) \
                   == ForecastAction.forecast_calibration_coaching

    # low — always no_action regardless of pattern
    def test_low_all_patterns(self, engine):
        for p in ForecastPattern:
            assert engine._action(ForecastRisk.low, p) == ForecastAction.no_action


# ---------------------------------------------------------------------------
# 13. has_forecast_gap flag
# ---------------------------------------------------------------------------

class TestHasForecastGap:
    def test_gap_via_composite_at_40(self, engine):
        assert engine._has_forecast_gap(40.0, make_input(
            commit_deals_lost_pct=0.05, commit_to_close_rate_pct=0.90)) is True

    def test_no_gap_composite_just_below_40(self, engine):
        assert engine._has_forecast_gap(39.9, make_input(
            commit_deals_lost_pct=0.05, commit_to_close_rate_pct=0.90)) is False

    def test_gap_via_commit_deals_lost_at_030(self, engine):
        assert engine._has_forecast_gap(0.0, make_input(
            commit_deals_lost_pct=0.30, commit_to_close_rate_pct=0.90)) is True

    def test_no_gap_commit_deals_lost_just_below_030(self, engine):
        assert engine._has_forecast_gap(0.0, make_input(
            commit_deals_lost_pct=0.29, commit_to_close_rate_pct=0.90)) is False

    def test_gap_via_commit_close_at_050(self, engine):
        assert engine._has_forecast_gap(0.0, make_input(
            commit_to_close_rate_pct=0.50, commit_deals_lost_pct=0.05)) is True

    def test_no_gap_commit_close_just_above_050(self, engine):
        assert engine._has_forecast_gap(0.0, make_input(
            commit_to_close_rate_pct=0.51, commit_deals_lost_pct=0.05)) is False

    def test_no_gap_all_conditions_false(self, engine):
        assert engine._has_forecast_gap(10.0, make_input(
            commit_deals_lost_pct=0.05, commit_to_close_rate_pct=0.90)) is False

    def test_gap_returns_bool(self, engine):
        result = engine._has_forecast_gap(0.0, make_input())
        assert isinstance(result, bool)

    def test_gap_all_three_conditions_true(self, engine):
        assert engine._has_forecast_gap(50.0, make_input(
            commit_deals_lost_pct=0.40, commit_to_close_rate_pct=0.30)) is True


# ---------------------------------------------------------------------------
# 14. requires_forecast_coaching flag
# ---------------------------------------------------------------------------

class TestRequiresForecastCoaching:
    def test_coaching_via_composite_at_30(self, engine):
        assert engine._requires_forecast_coaching(30.0, make_input(
            forecast_vs_actual_variance_pct=0.05,
            stage_advancement_accuracy_pct=0.90)) is True

    def test_no_coaching_composite_just_below_30(self, engine):
        assert engine._requires_forecast_coaching(29.9, make_input(
            forecast_vs_actual_variance_pct=0.05,
            stage_advancement_accuracy_pct=0.90)) is False

    def test_coaching_via_variance_at_015(self, engine):
        assert engine._requires_forecast_coaching(0.0, make_input(
            forecast_vs_actual_variance_pct=0.15,
            stage_advancement_accuracy_pct=0.90)) is True

    def test_no_coaching_variance_just_below_015(self, engine):
        assert engine._requires_forecast_coaching(0.0, make_input(
            forecast_vs_actual_variance_pct=0.14,
            stage_advancement_accuracy_pct=0.90)) is False

    def test_coaching_via_stage_acc_at_060(self, engine):
        assert engine._requires_forecast_coaching(0.0, make_input(
            stage_advancement_accuracy_pct=0.60,
            forecast_vs_actual_variance_pct=0.05)) is True

    def test_no_coaching_stage_acc_just_above_060(self, engine):
        assert engine._requires_forecast_coaching(0.0, make_input(
            stage_advancement_accuracy_pct=0.61,
            forecast_vs_actual_variance_pct=0.05)) is False

    def test_no_coaching_all_conditions_false(self, engine):
        assert engine._requires_forecast_coaching(10.0, make_input(
            forecast_vs_actual_variance_pct=0.05,
            stage_advancement_accuracy_pct=0.90)) is False

    def test_coaching_returns_bool(self, engine):
        result = engine._requires_forecast_coaching(0.0, make_input())
        assert isinstance(result, bool)

    def test_coaching_all_three_conditions_true(self, engine):
        assert engine._requires_forecast_coaching(35.0, make_input(
            forecast_vs_actual_variance_pct=0.20,
            stage_advancement_accuracy_pct=0.50)) is True


# ---------------------------------------------------------------------------
# 15. Revenue at risk formula
# ---------------------------------------------------------------------------

class TestRevenueAtRisk:
    def test_formula_basic(self, engine):
        # 10 deals * $50k * 0.20 commit_lost * (50/100) = 50000
        inp = make_input(total_deals_forecasted=10,
                         avg_opportunity_value_usd=50_000.0,
                         commit_deals_lost_pct=0.20)
        result = engine._estimated_revenue_at_risk(inp, 50.0)
        assert result == round(10 * 50_000.0 * 0.20 * 0.50, 2)

    def test_formula_zero_composite(self, engine):
        inp = make_input(total_deals_forecasted=20,
                         avg_opportunity_value_usd=30_000.0,
                         commit_deals_lost_pct=0.50)
        assert engine._estimated_revenue_at_risk(inp, 0.0) == 0.0

    def test_formula_zero_deals(self, engine):
        inp = make_input(total_deals_forecasted=0,
                         avg_opportunity_value_usd=50_000.0,
                         commit_deals_lost_pct=0.30)
        assert engine._estimated_revenue_at_risk(inp, 80.0) == 0.0

    def test_formula_zero_commit_lost(self, engine):
        inp = make_input(total_deals_forecasted=5,
                         avg_opportunity_value_usd=100_000.0,
                         commit_deals_lost_pct=0.0)
        assert engine._estimated_revenue_at_risk(inp, 80.0) == 0.0

    def test_formula_rounded_to_2_decimals(self, engine):
        inp = make_input(total_deals_forecasted=3,
                         avg_opportunity_value_usd=33_333.33,
                         commit_deals_lost_pct=0.33)
        result = engine._estimated_revenue_at_risk(inp, 33.3)
        expected = round(3 * 33_333.33 * 0.33 * (33.3 / 100.0), 2)
        assert result == expected

    def test_formula_composite_100(self, engine):
        inp = make_input(total_deals_forecasted=2,
                         avg_opportunity_value_usd=50_000.0,
                         commit_deals_lost_pct=1.0)
        result = engine._estimated_revenue_at_risk(inp, 100.0)
        assert result == round(2 * 50_000.0 * 1.0 * 1.0, 2)

    def test_formula_matches_assess_output(self, engine):
        inp = make_input(
            total_deals_forecasted=5,
            avg_opportunity_value_usd=20_000.0,
            commit_deals_lost_pct=0.25,
        )
        result = engine.assess(inp)
        expected = round(
            5 * 20_000.0 * 0.25 * (result.forecast_composite / 100.0), 2)
        assert result.estimated_revenue_at_risk_usd == expected

    def test_formula_returns_float(self, engine):
        result = engine._estimated_revenue_at_risk(make_input(), 50.0)
        assert isinstance(result, float)


# ---------------------------------------------------------------------------
# 16. Signal string
# ---------------------------------------------------------------------------

class TestSignalString:
    def test_healthy_signal_when_no_pattern_and_low_composite(self, engine):
        result = engine.assess(low_risk_input())
        assert result.forecast_composite < 20
        assert result.forecast_pattern == ForecastPattern.none
        assert "healthy" in result.forecast_signal.lower()

    def test_healthy_signal_exact_content(self, engine):
        result = engine.assess(low_risk_input())
        expected = ("Forecast accuracy healthy — variance, commit discipline, "
                    "and stage accuracy within benchmarks")
        assert result.forecast_signal == expected

    def test_signal_contains_variance_pct(self, engine):
        result = engine.assess(critical_input())
        # Should contain "50% forecast variance" (0.50 * 100 = 50)
        assert "50% forecast variance" in result.forecast_signal

    def test_signal_contains_commit_to_close_rate(self, engine):
        result = engine.assess(critical_input())
        assert "commit-to-close rate" in result.forecast_signal

    def test_signal_contains_committed_deals_lost(self, engine):
        result = engine.assess(critical_input())
        assert "committed deals lost" in result.forecast_signal

    def test_signal_contains_composite(self, engine):
        result = engine.assess(critical_input())
        assert "composite" in result.forecast_signal.lower()

    def test_signal_includes_capitalized_pattern_label(self, engine):
        inp = make_input(
            stage_advancement_accuracy_pct=0.35,
            deals_pulled_from_forecast_pct=0.30,
            forecast_vs_actual_variance_pct=0.25,
            commit_deals_lost_pct=0.25,
        )
        result = engine.assess(inp)
        assert result.forecast_pattern == ForecastPattern.stage_inflation_blindspot
        assert "Stage inflation blindspot" in result.forecast_signal

    def test_signal_none_pattern_high_composite_uses_forecast_risk_label(self, engine):
        # Pattern=none, composite >= 20 → label is "Forecast risk"
        inp = make_input(
            forecast_vs_actual_variance_pct=0.50,
            forecast_change_frequency_per_qtr=5.0,
            close_date_accuracy_within_week_pct=0.80,
            commit_deals_lost_pct=0.05,
            late_add_to_forecast_pct=0.05,
            multi_quarter_slip_rate_pct=0.05,
            stage_advancement_accuracy_pct=0.90,
            deals_pulled_from_forecast_pct=0.05,
            avg_deal_slip_days=5.0,
            commit_to_close_rate_pct=0.90,
            over_forecast_frequency_pct=0.10,
            under_forecast_frequency_pct=0.10,
            sandbag_conversion_rate_pct=0.10,
        )
        result = engine.assess(inp)
        assert result.forecast_composite >= 20
        assert result.forecast_pattern == ForecastPattern.none
        assert "healthy" not in result.forecast_signal.lower()
        assert "Forecast risk" in result.forecast_signal

    def test_signal_returns_string(self, engine):
        assert isinstance(engine.assess(low_risk_input()).forecast_signal, str)

    def test_signal_chronic_over_forecasting_label(self, engine):
        inp = make_input(
            over_forecast_frequency_pct=0.55,
            commit_deals_lost_pct=0.30,
            stage_advancement_accuracy_pct=0.90,
            deals_pulled_from_forecast_pct=0.05,
            forecast_vs_actual_variance_pct=0.25,
        )
        result = engine.assess(inp)
        if result.forecast_pattern == ForecastPattern.chronic_over_forecasting:
            assert "Chronic over forecasting" in result.forecast_signal


# ---------------------------------------------------------------------------
# 17. assess() end-to-end
# ---------------------------------------------------------------------------

class TestAssessEndToEnd:
    def test_assess_returns_forecast_result(self, engine):
        assert isinstance(engine.assess(low_risk_input()), ForecastResult)

    def test_assess_low_risk_profile(self, engine):
        result = engine.assess(low_risk_input())
        assert result.forecast_risk == ForecastRisk.low
        assert result.forecast_severity == ForecastSeverity.precise
        assert result.recommended_action == ForecastAction.no_action
        assert result.forecast_pattern == ForecastPattern.none
        assert result.has_forecast_gap is False
        assert result.requires_forecast_coaching is False

    def test_assess_critical_profile(self, engine):
        result = engine.assess(critical_input())
        assert result.forecast_risk == ForecastRisk.critical
        assert result.forecast_severity == ForecastSeverity.unreliable
        assert result.forecast_composite >= 60.0

    def test_assess_propagates_rep_id(self, engine):
        result = engine.assess(make_input(rep_id="rep-ABC"))
        assert result.rep_id == "rep-ABC"

    def test_assess_propagates_region(self, engine):
        result = engine.assess(make_input(region="APAC"))
        assert result.region == "APAC"

    def test_assess_appends_to_results(self, engine):
        engine.assess(low_risk_input())
        engine.assess(low_risk_input())
        assert len(engine._results) == 2

    def test_assess_action_critical_stage_inflation(self, engine):
        inp = make_input(
            stage_advancement_accuracy_pct=0.35,
            deals_pulled_from_forecast_pct=0.30,
            forecast_vs_actual_variance_pct=0.50,
            commit_deals_lost_pct=0.50,
            close_date_accuracy_within_week_pct=0.20,
            forecast_change_frequency_per_qtr=6.0,
            late_add_to_forecast_pct=0.50,
            multi_quarter_slip_rate_pct=0.40,
            commit_to_close_rate_pct=0.30,
            over_forecast_frequency_pct=0.70,
            under_forecast_frequency_pct=0.60,
        )
        result = engine.assess(inp)
        assert result.forecast_risk == ForecastRisk.critical
        assert result.forecast_pattern == ForecastPattern.stage_inflation_blindspot
        assert result.recommended_action == ForecastAction.stage_criteria_coaching

    def test_assess_action_critical_chronic_over(self, engine):
        inp = make_input(
            over_forecast_frequency_pct=0.55,
            commit_deals_lost_pct=0.30,
            stage_advancement_accuracy_pct=0.90,
            deals_pulled_from_forecast_pct=0.05,
            forecast_vs_actual_variance_pct=0.50,
            close_date_accuracy_within_week_pct=0.20,
            forecast_change_frequency_per_qtr=6.0,
            late_add_to_forecast_pct=0.50,
            multi_quarter_slip_rate_pct=0.40,
            commit_to_close_rate_pct=0.30,
            under_forecast_frequency_pct=0.60,
        )
        result = engine.assess(inp)
        assert result.forecast_risk == ForecastRisk.critical
        assert result.forecast_pattern == ForecastPattern.chronic_over_forecasting
        assert result.recommended_action == ForecastAction.commit_discipline_coaching

    def test_assess_moderate_risk(self, engine):
        # accuracy=22 (variance=0.25), discipline=0, stage=0, commit=0
        # composite = 22*0.35 = 7.7 → too low for moderate
        # Need composite in [20,40): accuracy=40+discipline=22 → 14+5.5=19.5 still < 20
        # accuracy=40, discipline=40 → 14+10=24 → moderate
        inp = make_input(
            forecast_vs_actual_variance_pct=0.50,   # +40 accuracy
            close_date_accuracy_within_week_pct=0.80,
            commit_deals_lost_pct=0.05,
            forecast_change_frequency_per_qtr=5.0,  # +40 discipline
            late_add_to_forecast_pct=0.05,
            multi_quarter_slip_rate_pct=0.05,
            stage_advancement_accuracy_pct=0.90,
            deals_pulled_from_forecast_pct=0.05,
            avg_deal_slip_days=5.0,
            commit_to_close_rate_pct=0.90,
            over_forecast_frequency_pct=0.10,
            under_forecast_frequency_pct=0.10,
            sandbag_conversion_rate_pct=0.10,
        )
        result = engine.assess(inp)
        # composite = 40*0.35 + 40*0.25 = 14+10 = 24
        assert result.forecast_composite == 24.0
        assert result.forecast_risk == ForecastRisk.moderate
        assert result.recommended_action == ForecastAction.forecast_calibration_coaching

    def test_assess_high_risk_end_of_quarter_cliff(self, engine):
        # discipline=75(change_freq=5+late_add=0.40), stage=40(stage_acc=0.40)
        # accuracy=40(variance=0.50), commit=25(commit_close=0.60)
        # composite = 40*0.35 + 75*0.25 + 40*0.25 + 25*0.15 = 14+18.75+10+3.75 = 46.5 → high
        inp = make_input(
            forecast_vs_actual_variance_pct=0.50,
            commit_deals_lost_pct=0.05,
            close_date_accuracy_within_week_pct=0.80,
            forecast_change_frequency_per_qtr=5.0,
            late_add_to_forecast_pct=0.40,
            multi_quarter_slip_rate_pct=0.25,
            stage_advancement_accuracy_pct=0.40,
            deals_pulled_from_forecast_pct=0.05,
            avg_deal_slip_days=5.0,
            commit_to_close_rate_pct=0.60,
            over_forecast_frequency_pct=0.10,
            under_forecast_frequency_pct=0.10,
            sandbag_conversion_rate_pct=0.10,
        )
        result = engine.assess(inp)
        assert result.forecast_risk == ForecastRisk.high
        assert result.forecast_pattern == ForecastPattern.end_of_quarter_cliff
        assert result.recommended_action == ForecastAction.pipeline_inspection_coaching


# ---------------------------------------------------------------------------
# 18. assess_batch()
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_batch_returns_list(self, engine):
        results = engine.assess_batch([low_risk_input(), critical_input()])
        assert isinstance(results, list)
        assert len(results) == 2

    def test_batch_each_element_is_forecast_result(self, engine):
        for r in engine.assess_batch([low_risk_input(), critical_input()]):
            assert isinstance(r, ForecastResult)

    def test_batch_empty_list(self, engine):
        assert engine.assess_batch([]) == []

    def test_batch_appends_to_internal_results(self, engine):
        engine.assess_batch([low_risk_input(), critical_input(), low_risk_input()])
        assert len(engine._results) == 3

    def test_batch_preserves_order(self, engine):
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"rep-{i}"

    def test_batch_single_item(self, engine):
        results = engine.assess_batch([low_risk_input()])
        assert len(results) == 1
        assert isinstance(results[0], ForecastResult)


# ---------------------------------------------------------------------------
# 19. summary() — empty
# ---------------------------------------------------------------------------

class TestSummaryEmpty:
    def test_summary_empty_returns_13_keys(self, engine):
        assert len(engine.summary()) == 13

    def test_summary_empty_exact_keys(self, engine):
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_forecast_composite", "forecast_gap_count",
            "coaching_count", "avg_accuracy_score", "avg_discipline_score",
            "avg_stage_score", "avg_commit_score",
            "total_estimated_revenue_at_risk_usd",
        }
        assert set(engine.summary().keys()) == expected

    def test_summary_empty_total_is_zero(self, engine):
        assert engine.summary()["total"] == 0

    def test_summary_empty_risk_counts_empty_dict(self, engine):
        assert engine.summary()["risk_counts"] == {}

    def test_summary_empty_pattern_counts_empty_dict(self, engine):
        assert engine.summary()["pattern_counts"] == {}

    def test_summary_empty_severity_counts_empty_dict(self, engine):
        assert engine.summary()["severity_counts"] == {}

    def test_summary_empty_action_counts_empty_dict(self, engine):
        assert engine.summary()["action_counts"] == {}

    def test_summary_empty_avg_composite_zero(self, engine):
        assert engine.summary()["avg_forecast_composite"] == 0.0

    def test_summary_empty_avg_accuracy_zero(self, engine):
        assert engine.summary()["avg_accuracy_score"] == 0.0

    def test_summary_empty_avg_discipline_zero(self, engine):
        assert engine.summary()["avg_discipline_score"] == 0.0

    def test_summary_empty_avg_stage_zero(self, engine):
        assert engine.summary()["avg_stage_score"] == 0.0

    def test_summary_empty_avg_commit_zero(self, engine):
        assert engine.summary()["avg_commit_score"] == 0.0

    def test_summary_empty_gap_count_zero(self, engine):
        assert engine.summary()["forecast_gap_count"] == 0

    def test_summary_empty_coaching_count_zero(self, engine):
        assert engine.summary()["coaching_count"] == 0

    def test_summary_empty_revenue_at_risk_zero(self, engine):
        assert engine.summary()["total_estimated_revenue_at_risk_usd"] == 0.0


# ---------------------------------------------------------------------------
# 20. summary() — populated (all 13 keys verified)
# ---------------------------------------------------------------------------

class TestSummaryPopulated:
    def test_summary_13_keys(self, engine):
        engine.assess_batch([low_risk_input(), critical_input()])
        assert len(engine.summary()) == 13

    def test_summary_exact_13_keys(self, engine):
        engine.assess(low_risk_input())
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_forecast_composite", "forecast_gap_count",
            "coaching_count", "avg_accuracy_score", "avg_discipline_score",
            "avg_stage_score", "avg_commit_score",
            "total_estimated_revenue_at_risk_usd",
        }
        assert set(engine.summary().keys()) == expected

    def test_summary_total(self, engine):
        engine.assess_batch([low_risk_input(), low_risk_input(), critical_input()])
        assert engine.summary()["total"] == 3

    def test_summary_risk_counts_low(self, engine):
        engine.assess(low_risk_input())
        assert engine.summary()["risk_counts"]["low"] == 1

    def test_summary_risk_counts_critical(self, engine):
        engine.assess(critical_input())
        assert engine.summary()["risk_counts"]["critical"] == 1

    def test_summary_risk_counts_multiple(self, engine):
        engine.assess(low_risk_input())
        engine.assess(critical_input())
        s = engine.summary()
        assert s["risk_counts"].get("low", 0) == 1
        assert s["risk_counts"].get("critical", 0) == 1

    def test_summary_pattern_counts(self, engine):
        engine.assess(low_risk_input())
        assert engine.summary()["pattern_counts"]["none"] == 1

    def test_summary_severity_counts(self, engine):
        engine.assess(low_risk_input())
        assert engine.summary()["severity_counts"]["precise"] == 1

    def test_summary_action_counts(self, engine):
        engine.assess(low_risk_input())
        assert engine.summary()["action_counts"]["no_action"] == 1

    def test_summary_avg_composite(self, engine):
        r1 = engine.assess(low_risk_input())
        r2 = engine.assess(critical_input())
        expected = round((r1.forecast_composite + r2.forecast_composite) / 2, 1)
        assert engine.summary()["avg_forecast_composite"] == expected

    def test_summary_avg_accuracy_score(self, engine):
        r1 = engine.assess(low_risk_input())
        r2 = engine.assess(critical_input())
        expected = round((r1.accuracy_score + r2.accuracy_score) / 2, 1)
        assert engine.summary()["avg_accuracy_score"] == expected

    def test_summary_avg_discipline_score(self, engine):
        r1 = engine.assess(low_risk_input())
        r2 = engine.assess(critical_input())
        expected = round((r1.discipline_score + r2.discipline_score) / 2, 1)
        assert engine.summary()["avg_discipline_score"] == expected

    def test_summary_avg_stage_score(self, engine):
        r1 = engine.assess(low_risk_input())
        r2 = engine.assess(critical_input())
        expected = round((r1.stage_score + r2.stage_score) / 2, 1)
        assert engine.summary()["avg_stage_score"] == expected

    def test_summary_avg_commit_score(self, engine):
        r1 = engine.assess(low_risk_input())
        r2 = engine.assess(critical_input())
        expected = round((r1.commit_score + r2.commit_score) / 2, 1)
        assert engine.summary()["avg_commit_score"] == expected

    def test_summary_forecast_gap_count(self, engine):
        engine.assess(low_risk_input())   # no gap
        engine.assess(critical_input())   # has gap (composite >= 40)
        assert engine.summary()["forecast_gap_count"] >= 1

    def test_summary_coaching_count(self, engine):
        engine.assess(critical_input())
        assert engine.summary()["coaching_count"] >= 1

    def test_summary_total_revenue_at_risk(self, engine):
        r1 = engine.assess(low_risk_input())
        r2 = engine.assess(critical_input())
        expected = round(r1.estimated_revenue_at_risk_usd + r2.estimated_revenue_at_risk_usd, 2)
        assert engine.summary()["total_estimated_revenue_at_risk_usd"] == expected

    def test_summary_accumulates_across_assessments(self, engine):
        engine.assess(low_risk_input())
        engine.summary()  # calling summary should NOT reset state
        engine.assess(critical_input())
        assert engine.summary()["total"] == 2

    def test_summary_gap_count_none_when_all_healthy(self, engine):
        engine.assess_batch([low_risk_input(), low_risk_input()])
        assert engine.summary()["forecast_gap_count"] == 0


# ---------------------------------------------------------------------------
# 21. Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_all_zero_inputs_does_not_raise(self, engine):
        """All-zero float inputs should not raise."""
        inp = ForecastInput(
            rep_id="zero", region="none", evaluation_period_id="Q0",
            forecast_vs_actual_variance_pct=0.0,
            over_forecast_frequency_pct=0.0,
            under_forecast_frequency_pct=0.0,
            commit_to_close_rate_pct=0.0,
            best_case_to_close_rate_pct=0.0,
            pipeline_to_quota_ratio=0.0,
            late_add_to_forecast_pct=0.0,
            deals_pulled_from_forecast_pct=0.0,
            avg_deal_slip_days=0.0,
            stage_advancement_accuracy_pct=0.0,
            close_date_accuracy_within_week_pct=0.0,
            forecast_change_frequency_per_qtr=0.0,
            upside_deals_closed_pct=0.0,
            commit_deals_lost_pct=0.0,
            sandbag_conversion_rate_pct=0.0,
            multi_quarter_slip_rate_pct=0.0,
            forecast_submitted_on_time_pct=0.0,
            total_deals_forecasted=0,
            avg_opportunity_value_usd=0.0,
        )
        result = engine.assess(inp)
        assert isinstance(result, ForecastResult)
        assert result.estimated_revenue_at_risk_usd == 0.0

    def test_max_inputs_does_not_raise(self, engine):
        """Extreme inputs should not raise and composite stays <= 100."""
        inp = make_input(
            forecast_vs_actual_variance_pct=1.0,
            over_forecast_frequency_pct=1.0,
            under_forecast_frequency_pct=1.0,
            commit_to_close_rate_pct=0.0,
            late_add_to_forecast_pct=1.0,
            deals_pulled_from_forecast_pct=1.0,
            avg_deal_slip_days=999.0,
            stage_advancement_accuracy_pct=0.0,
            close_date_accuracy_within_week_pct=0.0,
            forecast_change_frequency_per_qtr=99.0,
            commit_deals_lost_pct=1.0,
            multi_quarter_slip_rate_pct=1.0,
            total_deals_forecasted=10_000,
            avg_opportunity_value_usd=1_000_000.0,
        )
        result = engine.assess(inp)
        assert result.forecast_composite <= 100.0

    def test_zero_deals_revenue_is_zero(self, engine):
        result = engine.assess(make_input(total_deals_forecasted=0,
                                          commit_deals_lost_pct=0.50))
        assert result.estimated_revenue_at_risk_usd == 0.0

    def test_exact_boundary_risk_20(self, engine):
        assert engine._risk_level(20.0) == ForecastRisk.moderate

    def test_exact_boundary_risk_40(self, engine):
        assert engine._risk_level(40.0) == ForecastRisk.high

    def test_exact_boundary_risk_60(self, engine):
        assert engine._risk_level(60.0) == ForecastRisk.critical

    def test_exact_boundary_severity_20(self, engine):
        assert engine._severity(20.0) == ForecastSeverity.calibrating

    def test_exact_boundary_severity_40(self, engine):
        assert engine._severity(40.0) == ForecastSeverity.drifting

    def test_exact_boundary_severity_60(self, engine):
        assert engine._severity(60.0) == ForecastSeverity.unreliable

    def test_multiple_engines_are_independent(self):
        e1 = SalesForecastAccuracyIntelligenceEngine()
        e2 = SalesForecastAccuracyIntelligenceEngine()
        e1.assess(low_risk_input())
        assert len(e1._results) == 1
        assert len(e2._results) == 0

    def test_summary_called_before_any_assess(self):
        fresh = SalesForecastAccuracyIntelligenceEngine()
        s = fresh.summary()
        assert s["total"] == 0

    def test_assess_result_stored_in_order(self, engine):
        inputs = [make_input(rep_id=f"r{i}") for i in range(10)]
        results = engine.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"r{i}"

    def test_large_deal_count_revenue(self, engine):
        inp = make_input(total_deals_forecasted=10_000,
                         avg_opportunity_value_usd=1_000_000.0,
                         commit_deals_lost_pct=0.50)
        result = engine.assess(inp)
        assert result.estimated_revenue_at_risk_usd >= 0.0

    def test_has_forecast_gap_exact_boundary_050(self, engine):
        # commit_to_close_rate_pct == 0.50 → <= 0.50 → True
        assert engine._has_forecast_gap(0.0, make_input(
            commit_to_close_rate_pct=0.50, commit_deals_lost_pct=0.05)) is True

    def test_requires_coaching_exact_boundary_060_stage(self, engine):
        # stage_advancement_accuracy_pct == 0.60 → <= 0.60 → True
        assert engine._requires_forecast_coaching(0.0, make_input(
            stage_advancement_accuracy_pct=0.60,
            forecast_vs_actual_variance_pct=0.05)) is True

    def test_all_scores_are_non_negative(self, engine):
        result = engine.assess(low_risk_input())
        assert result.accuracy_score >= 0
        assert result.discipline_score >= 0
        assert result.stage_score >= 0
        assert result.commit_score >= 0
        assert result.forecast_composite >= 0

    def test_summary_with_single_result(self, engine):
        r = engine.assess(low_risk_input())
        s = engine.summary()
        assert s["total"] == 1
        assert s["avg_forecast_composite"] == r.forecast_composite
        assert s["avg_accuracy_score"] == r.accuracy_score
