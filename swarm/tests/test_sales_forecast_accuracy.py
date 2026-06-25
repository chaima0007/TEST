"""
Tests for SalesForecastAccuracyIntelligenceEngine
"""
import pytest
from dataclasses import fields as dc_fields
from intelligence.sales_forecast_accuracy_intelligence_engine import (
    SalesForecastAccuracyIntelligenceEngine,
    ForecastInput,
    ForecastResult,
    ForecastRisk,
    ForecastPattern,
    ForecastSeverity,
    ForecastAction,
)


@pytest.fixture
def engine():
    return SalesForecastAccuracyIntelligenceEngine()


@pytest.fixture
def healthy_input():
    return ForecastInput(
        total_deals=20,
        avg_deal_value=25000.0,
        forecast_variance_pct=8.0,
        commit_to_close_ratio=0.85,
        over_forecast_frequency=0.10,
        under_forecast_frequency=0.10,
        stage_accuracy_pct=85.0,
        deals_pulled_forward=1,
        deals_slipped_last_quarter=2,
        avg_slip_days=10.0,
        commit_change_frequency=0.10,
        late_stage_add_rate=0.05,
        close_date_change_avg=7.0,
        commit_lost_pct=0.05,
        weighted_pipeline=520000.0,
        quota=500000.0,
        actual_closed=490000.0,
        forecast_submitted=500000.0,
        deals_in_commit=12,
        deals_in_best_case=6,
        crm_last_update_days_avg=2.0,
        historical_accuracy_pct=88.0,
    )


@pytest.fixture
def risky_input():
    return ForecastInput(
        total_deals=20,
        avg_deal_value=25000.0,
        forecast_variance_pct=35.0,
        commit_to_close_ratio=0.45,
        over_forecast_frequency=0.50,
        under_forecast_frequency=0.10,
        stage_accuracy_pct=40.0,
        deals_pulled_forward=6,
        deals_slipped_last_quarter=8,
        avg_slip_days=35.0,
        commit_change_frequency=0.40,
        late_stage_add_rate=0.30,
        close_date_change_avg=25.0,
        commit_lost_pct=0.25,
        weighted_pipeline=300000.0,
        quota=500000.0,
        actual_closed=220000.0,
        forecast_submitted=350000.0,
        deals_in_commit=5,
        deals_in_best_case=3,
        crm_last_update_days_avg=12.0,
        historical_accuracy_pct=55.0,
    )


# ── Result structure ──────────────────────────────────────────────────────────

class TestResultStructure:
    def test_field_count_is_15(self):
        assert len(dc_fields(ForecastResult)) == 15

    def test_to_dict_has_15_keys(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert len(r.to_dict()) == 15

    def test_to_dict_keys(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        expected = {
            "composite_score", "risk", "pattern", "severity", "action",
            "accuracy_score", "discipline_score", "stage_score", "commit_score",
            "has_forecast_gap", "requires_forecast_coaching",
            "estimated_revenue_at_risk", "signal",
            "forecast_gap_pct", "commit_accuracy_pct",
        }
        assert set(d.keys()) == expected


# ── Healthy forecast ──────────────────────────────────────────────────────────

class TestHealthyForecast:
    def test_healthy_returns_low_risk(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.risk == ForecastRisk.low

    def test_healthy_returns_precise_severity(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.severity == ForecastSeverity.precise

    def test_healthy_composite_above_75(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.composite_score >= 75

    def test_healthy_signal_contains_healthy(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert "healthy" in r.signal.lower()

    def test_healthy_action_maintain(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.action == ForecastAction.maintain

    def test_healthy_no_forecast_gap(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert not r.has_forecast_gap


# ── Risky forecast ────────────────────────────────────────────────────────────

class TestRiskyForecast:
    def test_risky_returns_high_or_critical(self, engine, risky_input):
        r = engine.assess(risky_input)
        assert r.risk in (ForecastRisk.high, ForecastRisk.critical)

    def test_risky_composite_below_55(self, engine, risky_input):
        r = engine.assess(risky_input)
        assert r.composite_score < 55

    def test_risky_requires_coaching(self, engine, risky_input):
        r = engine.assess(risky_input)
        assert r.requires_forecast_coaching

    def test_risky_has_forecast_gap(self, engine, risky_input):
        r = engine.assess(risky_input)
        assert r.has_forecast_gap

    def test_risky_revenue_at_risk_positive(self, engine, risky_input):
        r = engine.assess(risky_input)
        assert r.estimated_revenue_at_risk > 0


# ── Score boundaries ──────────────────────────────────────────────────────────

class TestScoreBoundaries:
    def test_composite_between_0_and_100(self, engine):
        for inp in [
            ForecastInput(),
            ForecastInput(forecast_variance_pct=100.0, commit_lost_pct=1.0),
            ForecastInput(stage_accuracy_pct=0.0, over_forecast_frequency=1.0),
        ]:
            r = engine.assess(inp)
            assert 0.0 <= r.composite_score <= 100.0

    def test_sub_scores_bounded(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        for score in [r.accuracy_score, r.discipline_score, r.stage_score, r.commit_score]:
            assert 0.0 <= score <= 100.0

    def test_zero_deals_does_not_crash(self, engine):
        r = engine.assess(ForecastInput(total_deals=0))
        assert isinstance(r, ForecastResult)


# ── Pattern detection ─────────────────────────────────────────────────────────

class TestPatternDetection:
    def test_stage_inflation_detected(self, engine):
        inp = ForecastInput(stage_accuracy_pct=35.0)
        r = engine.assess(inp)
        assert r.pattern == ForecastPattern.stage_inflation_blindspot

    def test_chronic_over_forecasting_detected(self, engine):
        inp = ForecastInput(
            stage_accuracy_pct=75.0,
            over_forecast_frequency=0.50,
        )
        r = engine.assess(inp)
        assert r.pattern == ForecastPattern.chronic_over_forecasting

    def test_end_of_quarter_cliff_detected(self, engine):
        inp = ForecastInput(
            stage_accuracy_pct=75.0,
            over_forecast_frequency=0.20,
            deals_slipped_last_quarter=5,
            total_deals=20,
            avg_slip_days=25.0,
        )
        r = engine.assess(inp)
        assert r.pattern == ForecastPattern.end_of_quarter_cliff

    def test_sandbagging_detected(self, engine):
        inp = ForecastInput(
            stage_accuracy_pct=75.0,
            over_forecast_frequency=0.10,
            under_forecast_frequency=0.40,
            commit_to_close_ratio=0.95,
        )
        r = engine.assess(inp)
        assert r.pattern == ForecastPattern.recency_bias_sandbagging

    def test_healthy_pattern_none(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.pattern == ForecastPattern.none


# ── Action mapping ────────────────────────────────────────────────────────────

class TestActionMapping:
    def test_stage_inflation_action(self, engine):
        inp = ForecastInput(stage_accuracy_pct=30.0)
        r = engine.assess(inp)
        assert r.action == ForecastAction.stage_criteria_coaching

    def test_over_forecast_action(self, engine):
        inp = ForecastInput(stage_accuracy_pct=75.0, over_forecast_frequency=0.50)
        r = engine.assess(inp)
        assert r.action == ForecastAction.commit_discipline_coaching

    def test_healthy_action_maintain(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.action == ForecastAction.maintain


# ── Severity mapping ──────────────────────────────────────────────────────────

class TestSeverityMapping:
    def test_severity_maps_correctly(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        severity_map = {
            ForecastRisk.low: ForecastSeverity.precise,
            ForecastRisk.moderate: ForecastSeverity.calibrating,
            ForecastRisk.high: ForecastSeverity.drifting,
            ForecastRisk.critical: ForecastSeverity.unreliable,
        }
        assert r.severity == severity_map[r.risk]


# ── Batch and summary ─────────────────────────────────────────────────────────

class TestBatchAndSummary:
    def test_batch_processes_all(self, engine, healthy_input, risky_input):
        results = engine.batch([healthy_input, risky_input])
        assert len(results) == 2

    def test_summary_13_keys(self, engine, healthy_input, risky_input):
        results = engine.batch([healthy_input, risky_input])
        s = engine.summary(results)
        assert len(s) == 13

    def test_summary_empty_returns_empty_dict(self, engine):
        assert engine.summary([]) == {}

    def test_summary_total_reps(self, engine, healthy_input, risky_input):
        results = engine.batch([healthy_input, risky_input])
        s = engine.summary(results)
        assert s["total_reps"] == 2

    def test_summary_avg_score_between_0_and_100(self, engine, healthy_input, risky_input):
        results = engine.batch([healthy_input, risky_input])
        s = engine.summary(results)
        assert 0 <= s["avg_forecast_composite"] <= 100


# ── Enum validation ───────────────────────────────────────────────────────────

class TestEnums:
    def test_forecast_risk_values(self):
        assert set(ForecastRisk) == {ForecastRisk.low, ForecastRisk.moderate, ForecastRisk.high, ForecastRisk.critical}

    def test_forecast_pattern_count(self):
        assert len(ForecastPattern) == 6

    def test_forecast_action_values(self):
        actions = {a.value for a in ForecastAction}
        assert "maintain" in actions
        assert "stage_criteria_coaching" in actions
        assert "commit_discipline_coaching" in actions

    def test_result_action_is_valid_enum(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.action in ForecastAction

    def test_result_risk_is_valid_enum(self, engine, risky_input):
        r = engine.assess(risky_input)
        assert r.risk in ForecastRisk

    def test_forecast_gap_pct_non_negative(self, engine, risky_input):
        r = engine.assess(risky_input)
        assert r.forecast_gap_pct >= 0

    def test_commit_accuracy_pct_between_0_and_100(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert 0 <= r.commit_accuracy_pct <= 100
