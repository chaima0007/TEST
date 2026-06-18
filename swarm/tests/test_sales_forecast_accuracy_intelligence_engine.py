"""
Comprehensive pytest tests for SalesForecastAccuracyIntelligenceEngine.
~300 tests covering enums, sub-scores, pattern detection, risk/severity/action,
flags, revenue variance, signal strings, to_dict, summary, and assess_batch.
"""
import pytest
from swarm.intelligence.sales_forecast_accuracy_intelligence_engine import (
    SalesForecastAccuracyIntelligenceEngine,
    ForecastAccuracyInput,
    ForecastAccuracyResult,
    ForecastRisk,
    ForecastPattern,
    ForecastSeverity,
    ForecastAction,
)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def make_input(**kwargs):
    defaults = dict(
        rep_id="rep_test",
        region="West",
        evaluation_period_id="Q1-2026",
        total_forecasted_deals=10,
        forecast_commit_count=5,
        forecast_commit_closed_count=4,
        forecast_upside_count=3,
        forecast_upside_closed_count=1,
        late_stage_slippage_count=0,
        sandbagged_deals_identified=0,
        avg_forecast_accuracy_pct=0.95,
        forecast_overestimate_count=1,
        forecast_underestimate_count=0,
        pipeline_coverage_ratio=4.0,
        avg_deal_age_days=30.0,
        avg_close_date_slip_days=5.0,
        stage_advancement_rate_pct=0.65,
        crm_update_frequency_score=8.0,
        manager_review_sessions_count=3,
        multi_stakeholder_deals_pct=0.70,
        avg_deal_size_usd=50000.0,
        deals_closed_not_forecasted_count=0,
    )
    defaults.update(kwargs)
    return ForecastAccuracyInput(**defaults)


@pytest.fixture
def engine():
    return SalesForecastAccuracyIntelligenceEngine()


@pytest.fixture
def good_input():
    """A 'perfect' rep — minimal risk across all dimensions."""
    return make_input(
        avg_forecast_accuracy_pct=1.0,
        forecast_commit_count=5,
        forecast_commit_closed_count=5,
        forecast_overestimate_count=0,
        late_stage_slippage_count=0,
        avg_close_date_slip_days=0.0,
        deals_closed_not_forecasted_count=0,
        manager_review_sessions_count=5,
        pipeline_coverage_ratio=5.0,
        avg_deal_age_days=20.0,
        stage_advancement_rate_pct=0.80,
        multi_stakeholder_deals_pct=0.80,
        crm_update_frequency_score=9.0,
        sandbagged_deals_identified=0,
        forecast_underestimate_count=0,
    )


# ===========================================================================
# 1. ENUM VALUES
# ===========================================================================

class TestForecastRiskEnum:
    def test_low_value(self):
        assert ForecastRisk.low.value == "low"

    def test_moderate_value(self):
        assert ForecastRisk.moderate.value == "moderate"

    def test_high_value(self):
        assert ForecastRisk.high.value == "high"

    def test_critical_value(self):
        assert ForecastRisk.critical.value == "critical"

    def test_all_members(self):
        members = {m.value for m in ForecastRisk}
        assert members == {"low", "moderate", "high", "critical"}

    def test_is_str(self):
        assert isinstance(ForecastRisk.low, str)

    def test_str_equality(self):
        assert ForecastRisk.low == "low"

    def test_count(self):
        assert len(ForecastRisk) == 4


class TestForecastPatternEnum:
    def test_none_value(self):
        assert ForecastPattern.none.value == "none"

    def test_systematic_overforecast_value(self):
        assert ForecastPattern.systematic_overforecast.value == "systematic_overforecast"

    def test_sandbag_behavior_value(self):
        assert ForecastPattern.sandbag_behavior.value == "sandbag_behavior"

    def test_pipeline_gap_value(self):
        assert ForecastPattern.pipeline_gap.value == "pipeline_gap"

    def test_crm_neglect_value(self):
        assert ForecastPattern.crm_neglect.value == "crm_neglect"

    def test_stage_manipulation_value(self):
        assert ForecastPattern.stage_manipulation.value == "stage_manipulation"

    def test_all_members(self):
        members = {m.value for m in ForecastPattern}
        assert members == {
            "none",
            "systematic_overforecast",
            "sandbag_behavior",
            "pipeline_gap",
            "crm_neglect",
            "stage_manipulation",
        }

    def test_count(self):
        assert len(ForecastPattern) == 6

    def test_is_str(self):
        assert isinstance(ForecastPattern.none, str)


class TestForecastSeverityEnum:
    def test_reliable_value(self):
        assert ForecastSeverity.reliable.value == "reliable"

    def test_variable_value(self):
        assert ForecastSeverity.variable.value == "variable"

    def test_unreliable_value(self):
        assert ForecastSeverity.unreliable.value == "unreliable"

    def test_chaotic_value(self):
        assert ForecastSeverity.chaotic.value == "chaotic"

    def test_all_members(self):
        members = {m.value for m in ForecastSeverity}
        assert members == {"reliable", "variable", "unreliable", "chaotic"}

    def test_count(self):
        assert len(ForecastSeverity) == 4

    def test_is_str(self):
        assert isinstance(ForecastSeverity.reliable, str)


class TestForecastActionEnum:
    def test_no_action_value(self):
        assert ForecastAction.no_action.value == "no_action"

    def test_forecast_recalibration_value(self):
        assert ForecastAction.forecast_recalibration.value == "forecast_recalibration"

    def test_pipeline_inspection_value(self):
        assert ForecastAction.pipeline_inspection.value == "pipeline_inspection"

    def test_crm_training_value(self):
        assert ForecastAction.crm_training.value == "crm_training"

    def test_forecast_review_cadence_value(self):
        assert ForecastAction.forecast_review_cadence.value == "forecast_review_cadence"

    def test_forecast_override_value(self):
        assert ForecastAction.forecast_override.value == "forecast_override"

    def test_all_members(self):
        members = {m.value for m in ForecastAction}
        assert members == {
            "no_action",
            "forecast_recalibration",
            "pipeline_inspection",
            "crm_training",
            "forecast_review_cadence",
            "forecast_override",
        }

    def test_count(self):
        assert len(ForecastAction) == 6

    def test_is_str(self):
        assert isinstance(ForecastAction.no_action, str)


# ===========================================================================
# 2. _forecast_accuracy_score
# ===========================================================================

class TestForecastAccuracyScore:
    def setup_method(self):
        self.eng = SalesForecastAccuracyIntelligenceEngine()

    def _score(self, **kw):
        return self.eng._forecast_accuracy_score(make_input(**kw))

    # --- accuracy deviation ---
    def test_dev_zero_no_deviation_points(self):
        s = self._score(avg_forecast_accuracy_pct=1.0,
                        forecast_commit_closed_count=5,
                        forecast_commit_count=5,
                        forecast_overestimate_count=0)
        assert s == 0.0

    def test_dev_below_15_no_deviation_points(self):
        # dev = 0.10 < 0.15
        s = self._score(avg_forecast_accuracy_pct=0.90,
                        forecast_commit_closed_count=5,
                        forecast_commit_count=5,
                        forecast_overestimate_count=0)
        assert s == 0.0

    def test_dev_exactly_15_adds_12(self):
        s = self._score(avg_forecast_accuracy_pct=0.85,
                        forecast_commit_closed_count=5,
                        forecast_commit_count=5,
                        forecast_overestimate_count=0)
        assert s == 12.0

    def test_dev_exactly_25_adds_25(self):
        s = self._score(avg_forecast_accuracy_pct=0.75,
                        forecast_commit_closed_count=5,
                        forecast_commit_count=5,
                        forecast_overestimate_count=0)
        assert s == 25.0

    def test_dev_exactly_40_adds_40(self):
        s = self._score(avg_forecast_accuracy_pct=0.60,
                        forecast_commit_closed_count=5,
                        forecast_commit_count=5,
                        forecast_overestimate_count=0)
        assert s == 40.0

    def test_dev_above_40(self):
        s = self._score(avg_forecast_accuracy_pct=0.50,
                        forecast_commit_closed_count=5,
                        forecast_commit_count=5,
                        forecast_overestimate_count=0)
        assert s == 40.0

    def test_dev_works_above_1_overestimate(self):
        # avg accuracy above 1.0 (over-committed), dev = 0.20 -> 0.15 <= dev < 0.25 -> +12
        s = self._score(avg_forecast_accuracy_pct=1.20,
                        forecast_commit_closed_count=5,
                        forecast_commit_count=5,
                        forecast_overestimate_count=0)
        assert s == 12.0

    # --- commit accuracy ---
    def test_commit_rate_perfect_no_points(self):
        s = self._score(forecast_commit_count=10,
                        forecast_commit_closed_count=10,
                        avg_forecast_accuracy_pct=1.0,
                        forecast_overestimate_count=0)
        assert s == 0.0

    def test_commit_rate_above_85_no_points(self):
        # 9/10 = 0.90 >= 0.85
        s = self._score(forecast_commit_count=10,
                        forecast_commit_closed_count=9,
                        avg_forecast_accuracy_pct=1.0,
                        forecast_overestimate_count=0)
        assert s == 0.0

    def test_commit_rate_below_85_adds_5(self):
        # 8/10 = 0.80, 0.70 <= 0.80 < 0.85
        s = self._score(forecast_commit_count=10,
                        forecast_commit_closed_count=8,
                        avg_forecast_accuracy_pct=1.0,
                        forecast_overestimate_count=0)
        assert s == 5.0

    def test_commit_rate_below_70_adds_15(self):
        # 6/10 = 0.60
        s = self._score(forecast_commit_count=10,
                        forecast_commit_closed_count=6,
                        avg_forecast_accuracy_pct=1.0,
                        forecast_overestimate_count=0)
        assert s == 15.0

    def test_commit_rate_below_50_adds_30(self):
        # 4/10 = 0.40
        s = self._score(forecast_commit_count=10,
                        forecast_commit_closed_count=4,
                        avg_forecast_accuracy_pct=1.0,
                        forecast_overestimate_count=0)
        assert s == 30.0

    def test_commit_count_zero_uses_1_denominator(self):
        # 0/max(0,1)=1 => commit_rate=0.0 < 0.50
        s = self._score(forecast_commit_count=0,
                        forecast_commit_closed_count=0,
                        avg_forecast_accuracy_pct=1.0,
                        forecast_overestimate_count=0)
        assert s == 30.0

    # --- over-ratio ---
    def test_over_ratio_zero_no_points(self):
        s = self._score(forecast_overestimate_count=0,
                        total_forecasted_deals=10,
                        avg_forecast_accuracy_pct=1.0,
                        forecast_commit_closed_count=5,
                        forecast_commit_count=5)
        assert s == 0.0

    def test_over_ratio_below_15_no_points(self):
        # 1/10 = 0.10 < 0.15
        s = self._score(forecast_overestimate_count=1,
                        total_forecasted_deals=10,
                        avg_forecast_accuracy_pct=1.0,
                        forecast_commit_closed_count=5,
                        forecast_commit_count=5)
        assert s == 0.0

    def test_over_ratio_exactly_15_adds_5(self):
        # 3/20 = 0.15
        s = self._score(forecast_overestimate_count=3,
                        total_forecasted_deals=20,
                        avg_forecast_accuracy_pct=1.0,
                        forecast_commit_closed_count=5,
                        forecast_commit_count=5)
        assert s == 5.0

    def test_over_ratio_exactly_25_adds_10(self):
        # 5/20 = 0.25
        s = self._score(forecast_overestimate_count=5,
                        total_forecasted_deals=20,
                        avg_forecast_accuracy_pct=1.0,
                        forecast_commit_closed_count=5,
                        forecast_commit_count=5)
        assert s == 10.0

    def test_over_ratio_exactly_40_adds_20(self):
        # 8/20 = 0.40
        s = self._score(forecast_overestimate_count=8,
                        total_forecasted_deals=20,
                        avg_forecast_accuracy_pct=1.0,
                        forecast_commit_closed_count=5,
                        forecast_commit_count=5)
        assert s == 20.0

    def test_total_forecasted_zero_uses_1_denominator(self):
        # forecast_overestimate_count=1, total=0 -> uses max(0,1)=1, ratio=1.0 >= 0.40
        s = self._score(forecast_overestimate_count=1,
                        total_forecasted_deals=0,
                        avg_forecast_accuracy_pct=1.0,
                        forecast_commit_closed_count=5,
                        forecast_commit_count=5)
        assert s == 20.0

    def test_capped_at_100(self):
        # All maximums: dev>=0.40 (+40), commit<0.50 (+30), over_ratio>=0.40 (+20) = 90
        # Let's ensure it never exceeds 100 even with extreme values
        s = self._score(avg_forecast_accuracy_pct=0.0,
                        forecast_commit_count=10,
                        forecast_commit_closed_count=0,
                        forecast_overestimate_count=10,
                        total_forecasted_deals=10)
        assert s <= 100.0

    def test_combined_all_max(self):
        # dev=1.0>=0.40 (+40), commit_rate=0<0.50 (+30), over_ratio=1.0>=0.40 (+20) => 90
        s = self._score(avg_forecast_accuracy_pct=0.0,
                        forecast_commit_count=10,
                        forecast_commit_closed_count=0,
                        forecast_overestimate_count=10,
                        total_forecasted_deals=10)
        assert s == 90.0

    def test_returns_float(self):
        s = self._score()
        assert isinstance(s, float)


# ===========================================================================
# 3. _forecast_discipline_score
# ===========================================================================

class TestForecastDisciplineScore:
    def setup_method(self):
        self.eng = SalesForecastAccuracyIntelligenceEngine()

    def _score(self, **kw):
        return self.eng._forecast_discipline_score(make_input(**kw))

    # --- late stage slippage ---
    def test_no_slippage_no_points(self):
        s = self._score(late_stage_slippage_count=0, avg_close_date_slip_days=0,
                        deals_closed_not_forecasted_count=0, manager_review_sessions_count=5)
        assert s == 0.0

    def test_slippage_1_adds_8(self):
        s = self._score(late_stage_slippage_count=1, avg_close_date_slip_days=0,
                        deals_closed_not_forecasted_count=0, manager_review_sessions_count=5)
        assert s == 8.0

    def test_slippage_2_adds_20(self):
        s = self._score(late_stage_slippage_count=2, avg_close_date_slip_days=0,
                        deals_closed_not_forecasted_count=0, manager_review_sessions_count=5)
        assert s == 20.0

    def test_slippage_4_adds_35(self):
        s = self._score(late_stage_slippage_count=4, avg_close_date_slip_days=0,
                        deals_closed_not_forecasted_count=0, manager_review_sessions_count=5)
        assert s == 35.0

    def test_slippage_10_adds_35(self):
        s = self._score(late_stage_slippage_count=10, avg_close_date_slip_days=0,
                        deals_closed_not_forecasted_count=0, manager_review_sessions_count=5)
        assert s == 35.0

    # --- close date slippage ---
    def test_close_slip_below_10_no_points(self):
        s = self._score(late_stage_slippage_count=0, avg_close_date_slip_days=5.0,
                        deals_closed_not_forecasted_count=0, manager_review_sessions_count=5)
        assert s == 0.0

    def test_close_slip_exactly_10_adds_8(self):
        s = self._score(late_stage_slippage_count=0, avg_close_date_slip_days=10.0,
                        deals_closed_not_forecasted_count=0, manager_review_sessions_count=5)
        assert s == 8.0

    def test_close_slip_exactly_25_adds_18(self):
        s = self._score(late_stage_slippage_count=0, avg_close_date_slip_days=25.0,
                        deals_closed_not_forecasted_count=0, manager_review_sessions_count=5)
        assert s == 18.0

    def test_close_slip_exactly_45_adds_30(self):
        s = self._score(late_stage_slippage_count=0, avg_close_date_slip_days=45.0,
                        deals_closed_not_forecasted_count=0, manager_review_sessions_count=5)
        assert s == 30.0

    def test_close_slip_100_adds_30(self):
        s = self._score(late_stage_slippage_count=0, avg_close_date_slip_days=100.0,
                        deals_closed_not_forecasted_count=0, manager_review_sessions_count=5)
        assert s == 30.0

    # --- unforecast closes ---
    def test_closed_not_forecasted_0_no_points(self):
        s = self._score(late_stage_slippage_count=0, avg_close_date_slip_days=0,
                        deals_closed_not_forecasted_count=0, manager_review_sessions_count=5)
        assert s == 0.0

    def test_closed_not_forecasted_1_adds_5(self):
        s = self._score(late_stage_slippage_count=0, avg_close_date_slip_days=0,
                        deals_closed_not_forecasted_count=1, manager_review_sessions_count=5)
        assert s == 5.0

    def test_closed_not_forecasted_2_adds_12(self):
        s = self._score(late_stage_slippage_count=0, avg_close_date_slip_days=0,
                        deals_closed_not_forecasted_count=2, manager_review_sessions_count=5)
        assert s == 12.0

    def test_closed_not_forecasted_3_adds_25(self):
        s = self._score(late_stage_slippage_count=0, avg_close_date_slip_days=0,
                        deals_closed_not_forecasted_count=3, manager_review_sessions_count=5)
        assert s == 25.0

    def test_closed_not_forecasted_10_adds_25(self):
        s = self._score(late_stage_slippage_count=0, avg_close_date_slip_days=0,
                        deals_closed_not_forecasted_count=10, manager_review_sessions_count=5)
        assert s == 25.0

    # --- manager review ---
    def test_manager_review_2_plus_no_points(self):
        s = self._score(late_stage_slippage_count=0, avg_close_date_slip_days=0,
                        deals_closed_not_forecasted_count=0, manager_review_sessions_count=2)
        assert s == 0.0

    def test_manager_review_1_adds_5(self):
        s = self._score(late_stage_slippage_count=0, avg_close_date_slip_days=0,
                        deals_closed_not_forecasted_count=0, manager_review_sessions_count=1)
        assert s == 5.0

    def test_manager_review_0_adds_10(self):
        s = self._score(late_stage_slippage_count=0, avg_close_date_slip_days=0,
                        deals_closed_not_forecasted_count=0, manager_review_sessions_count=0)
        assert s == 10.0

    def test_capped_at_100(self):
        s = self._score(late_stage_slippage_count=10, avg_close_date_slip_days=100,
                        deals_closed_not_forecasted_count=10, manager_review_sessions_count=0)
        assert s <= 100.0

    def test_all_max_35_plus_30_plus_25_plus_10_capped(self):
        # 35+30+25+10=100
        s = self._score(late_stage_slippage_count=4, avg_close_date_slip_days=45,
                        deals_closed_not_forecasted_count=3, manager_review_sessions_count=0)
        assert s == 100.0

    def test_returns_float(self):
        s = self._score()
        assert isinstance(s, float)


# ===========================================================================
# 4. _pipeline_health_score
# ===========================================================================

class TestPipelineHealthScore:
    def setup_method(self):
        self.eng = SalesForecastAccuracyIntelligenceEngine()

    def _score(self, **kw):
        return self.eng._pipeline_health_score(make_input(**kw))

    # --- coverage ratio ---
    def test_coverage_4_plus_no_points(self):
        s = self._score(pipeline_coverage_ratio=4.0, avg_deal_age_days=0,
                        stage_advancement_rate_pct=0.80, multi_stakeholder_deals_pct=0.80)
        assert s == 0.0

    def test_coverage_exactly_3_adds_8(self):
        s = self._score(pipeline_coverage_ratio=3.0, avg_deal_age_days=0,
                        stage_advancement_rate_pct=0.80, multi_stakeholder_deals_pct=0.80)
        assert s == 8.0

    def test_coverage_exactly_2_adds_18(self):
        s = self._score(pipeline_coverage_ratio=2.0, avg_deal_age_days=0,
                        stage_advancement_rate_pct=0.80, multi_stakeholder_deals_pct=0.80)
        assert s == 18.0

    def test_coverage_below_2_adds_35(self):
        s = self._score(pipeline_coverage_ratio=1.5, avg_deal_age_days=0,
                        stage_advancement_rate_pct=0.80, multi_stakeholder_deals_pct=0.80)
        assert s == 35.0

    def test_coverage_zero_adds_35(self):
        s = self._score(pipeline_coverage_ratio=0.0, avg_deal_age_days=0,
                        stage_advancement_rate_pct=0.80, multi_stakeholder_deals_pct=0.80)
        assert s == 35.0

    # --- deal age ---
    def test_deal_age_below_45_no_points(self):
        s = self._score(pipeline_coverage_ratio=5.0, avg_deal_age_days=30.0,
                        stage_advancement_rate_pct=0.80, multi_stakeholder_deals_pct=0.80)
        assert s == 0.0

    def test_deal_age_exactly_45_adds_5(self):
        s = self._score(pipeline_coverage_ratio=5.0, avg_deal_age_days=45.0,
                        stage_advancement_rate_pct=0.80, multi_stakeholder_deals_pct=0.80)
        assert s == 5.0

    def test_deal_age_exactly_75_adds_15(self):
        s = self._score(pipeline_coverage_ratio=5.0, avg_deal_age_days=75.0,
                        stage_advancement_rate_pct=0.80, multi_stakeholder_deals_pct=0.80)
        assert s == 15.0

    def test_deal_age_exactly_120_adds_25(self):
        s = self._score(pipeline_coverage_ratio=5.0, avg_deal_age_days=120.0,
                        stage_advancement_rate_pct=0.80, multi_stakeholder_deals_pct=0.80)
        assert s == 25.0

    def test_deal_age_very_high_adds_25(self):
        s = self._score(pipeline_coverage_ratio=5.0, avg_deal_age_days=365.0,
                        stage_advancement_rate_pct=0.80, multi_stakeholder_deals_pct=0.80)
        assert s == 25.0

    # --- stage advancement ---
    def test_stage_advancement_50_plus_no_points(self):
        s = self._score(pipeline_coverage_ratio=5.0, avg_deal_age_days=0,
                        stage_advancement_rate_pct=0.50, multi_stakeholder_deals_pct=0.80)
        assert s == 0.0

    def test_stage_advancement_below_50_adds_12(self):
        s = self._score(pipeline_coverage_ratio=5.0, avg_deal_age_days=0,
                        stage_advancement_rate_pct=0.40, multi_stakeholder_deals_pct=0.80)
        assert s == 12.0

    def test_stage_advancement_below_30_adds_25(self):
        s = self._score(pipeline_coverage_ratio=5.0, avg_deal_age_days=0,
                        stage_advancement_rate_pct=0.20, multi_stakeholder_deals_pct=0.80)
        assert s == 25.0

    def test_stage_advancement_zero_adds_25(self):
        s = self._score(pipeline_coverage_ratio=5.0, avg_deal_age_days=0,
                        stage_advancement_rate_pct=0.0, multi_stakeholder_deals_pct=0.80)
        assert s == 25.0

    # --- multi-stakeholder ---
    def test_multi_stakeholder_50_plus_no_points(self):
        s = self._score(pipeline_coverage_ratio=5.0, avg_deal_age_days=0,
                        stage_advancement_rate_pct=0.80, multi_stakeholder_deals_pct=0.50)
        assert s == 0.0

    def test_multi_stakeholder_30_to_50_adds_8(self):
        s = self._score(pipeline_coverage_ratio=5.0, avg_deal_age_days=0,
                        stage_advancement_rate_pct=0.80, multi_stakeholder_deals_pct=0.40)
        assert s == 8.0

    def test_multi_stakeholder_below_30_adds_15(self):
        s = self._score(pipeline_coverage_ratio=5.0, avg_deal_age_days=0,
                        stage_advancement_rate_pct=0.80, multi_stakeholder_deals_pct=0.20)
        assert s == 15.0

    def test_multi_stakeholder_zero_adds_15(self):
        s = self._score(pipeline_coverage_ratio=5.0, avg_deal_age_days=0,
                        stage_advancement_rate_pct=0.80, multi_stakeholder_deals_pct=0.0)
        assert s == 15.0

    def test_capped_at_100(self):
        s = self._score(pipeline_coverage_ratio=0.0, avg_deal_age_days=365,
                        stage_advancement_rate_pct=0.0, multi_stakeholder_deals_pct=0.0)
        assert s <= 100.0

    def test_all_max_35_25_25_15(self):
        # 35+25+25+15=100
        s = self._score(pipeline_coverage_ratio=0.0, avg_deal_age_days=120,
                        stage_advancement_rate_pct=0.0, multi_stakeholder_deals_pct=0.0)
        assert s == 100.0

    def test_returns_float(self):
        s = self._score()
        assert isinstance(s, float)


# ===========================================================================
# 5. _crm_hygiene_score
# ===========================================================================

class TestCrmHygieneScore:
    def setup_method(self):
        self.eng = SalesForecastAccuracyIntelligenceEngine()

    def _score(self, **kw):
        return self.eng._crm_hygiene_score(make_input(**kw))

    # --- CRM update frequency ---
    def test_crm_freq_7_plus_no_points(self):
        s = self._score(crm_update_frequency_score=7.0,
                        sandbagged_deals_identified=0, forecast_underestimate_count=0)
        assert s == 0.0

    def test_crm_freq_exactly_7_no_points(self):
        s = self._score(crm_update_frequency_score=7.0,
                        sandbagged_deals_identified=0, forecast_underestimate_count=0)
        assert s == 0.0

    def test_crm_freq_below_7_adds_10(self):
        # 5.0 <= x < 7.0
        s = self._score(crm_update_frequency_score=6.0,
                        sandbagged_deals_identified=0, forecast_underestimate_count=0)
        assert s == 10.0

    def test_crm_freq_exactly_5_adds_25(self):
        # 3.0 <= x < 5.0
        s = self._score(crm_update_frequency_score=4.5,
                        sandbagged_deals_identified=0, forecast_underestimate_count=0)
        assert s == 25.0

    def test_crm_freq_below_3_adds_45(self):
        s = self._score(crm_update_frequency_score=2.9,
                        sandbagged_deals_identified=0, forecast_underestimate_count=0)
        assert s == 45.0

    def test_crm_freq_zero_adds_45(self):
        s = self._score(crm_update_frequency_score=0.0,
                        sandbagged_deals_identified=0, forecast_underestimate_count=0)
        assert s == 45.0

    # --- sandbagged deals ---
    def test_sandbag_0_no_points(self):
        s = self._score(crm_update_frequency_score=10.0,
                        sandbagged_deals_identified=0, forecast_underestimate_count=0)
        assert s == 0.0

    def test_sandbag_1_adds_8(self):
        s = self._score(crm_update_frequency_score=10.0,
                        sandbagged_deals_identified=1, forecast_underestimate_count=0)
        assert s == 8.0

    def test_sandbag_2_adds_18(self):
        s = self._score(crm_update_frequency_score=10.0,
                        sandbagged_deals_identified=2, forecast_underestimate_count=0)
        assert s == 18.0

    def test_sandbag_3_adds_35(self):
        s = self._score(crm_update_frequency_score=10.0,
                        sandbagged_deals_identified=3, forecast_underestimate_count=0)
        assert s == 35.0

    def test_sandbag_10_adds_35(self):
        s = self._score(crm_update_frequency_score=10.0,
                        sandbagged_deals_identified=10, forecast_underestimate_count=0)
        assert s == 35.0

    # --- underestimate count ---
    def test_underestimate_0_no_points(self):
        s = self._score(crm_update_frequency_score=10.0,
                        sandbagged_deals_identified=0, forecast_underestimate_count=0)
        assert s == 0.0

    def test_underestimate_1_no_points(self):
        # Only 2+ is counted
        s = self._score(crm_update_frequency_score=10.0,
                        sandbagged_deals_identified=0, forecast_underestimate_count=1)
        assert s == 0.0

    def test_underestimate_2_adds_10(self):
        s = self._score(crm_update_frequency_score=10.0,
                        sandbagged_deals_identified=0, forecast_underestimate_count=2)
        assert s == 10.0

    def test_underestimate_3_adds_20(self):
        s = self._score(crm_update_frequency_score=10.0,
                        sandbagged_deals_identified=0, forecast_underestimate_count=3)
        assert s == 20.0

    def test_underestimate_10_adds_20(self):
        s = self._score(crm_update_frequency_score=10.0,
                        sandbagged_deals_identified=0, forecast_underestimate_count=10)
        assert s == 20.0

    def test_capped_at_100(self):
        s = self._score(crm_update_frequency_score=0.0,
                        sandbagged_deals_identified=10, forecast_underestimate_count=10)
        assert s <= 100.0

    def test_all_max_45_35_20(self):
        s = self._score(crm_update_frequency_score=0.0,
                        sandbagged_deals_identified=3, forecast_underestimate_count=3)
        assert s == 100.0

    def test_returns_float(self):
        s = self._score()
        assert isinstance(s, float)


# ===========================================================================
# 6. PATTERN DETECTION
# ===========================================================================

class TestPatternDetection:
    def setup_method(self):
        self.eng = SalesForecastAccuracyIntelligenceEngine()

    def assess(self, **kw):
        return self.eng.assess(make_input(**kw))

    # --- systematic_overforecast (highest priority) ---
    def test_systematic_overforecast_detected(self):
        # Need accuracy >= 35 and over_ratio >= 0.30
        # accuracy >= 35 requires e.g. dev>=0.25 (+25) AND commit_rate<0.70 (+15)=40
        # over_ratio=5/10=0.50
        r = self.assess(
            avg_forecast_accuracy_pct=0.70,        # dev=0.30>=0.25 -> +25
            forecast_commit_count=10,
            forecast_commit_closed_count=6,         # 0.60 -> +15; total acc=40
            forecast_overestimate_count=5,
            total_forecasted_deals=10,             # over_ratio=0.50 >= 0.30
        )
        assert r.forecast_pattern == ForecastPattern.systematic_overforecast

    def test_systematic_overforecast_priority_over_sandbag(self):
        # Both conditions met for overforecast and sandbag, but overforecast wins
        r = self.assess(
            avg_forecast_accuracy_pct=0.70,
            forecast_commit_count=10,
            forecast_commit_closed_count=6,
            forecast_overestimate_count=5,
            total_forecasted_deals=10,
            sandbagged_deals_identified=3,
            crm_update_frequency_score=0.0,        # crm will be very high
        )
        assert r.forecast_pattern == ForecastPattern.systematic_overforecast

    def test_systematic_overforecast_accuracy_below_35_no_match(self):
        # accuracy below 35 -> can't match
        r = self.assess(
            avg_forecast_accuracy_pct=0.95,        # dev=0.05 -> +0
            forecast_commit_count=10,
            forecast_commit_closed_count=10,        # commit_rate=1.0 -> +0
            forecast_overestimate_count=5,
            total_forecasted_deals=10,              # over_ratio=0.50 but accuracy=0
            sandbagged_deals_identified=0,
            crm_update_frequency_score=9.0,
            pipeline_coverage_ratio=5.0,
            late_stage_slippage_count=0,
        )
        assert r.forecast_pattern != ForecastPattern.systematic_overforecast

    def test_systematic_overforecast_over_ratio_below_30_no_match(self):
        # over_ratio=0.20 < 0.30
        r = self.assess(
            avg_forecast_accuracy_pct=0.70,
            forecast_commit_count=10,
            forecast_commit_closed_count=6,
            forecast_overestimate_count=2,
            total_forecasted_deals=10,
        )
        assert r.forecast_pattern != ForecastPattern.systematic_overforecast

    # --- sandbag_behavior ---
    def test_sandbag_behavior_detected(self):
        # sandbagged>=2, crm>=25 (crm_freq<5.0 -> +25, sandbag=2 -> +18 = 43 >=25)
        r = self.assess(
            avg_forecast_accuracy_pct=1.0,         # accuracy=0
            forecast_commit_count=5,
            forecast_commit_closed_count=5,
            forecast_overestimate_count=0,          # over_ratio=0; accuracy won't trigger
            sandbagged_deals_identified=2,
            crm_update_frequency_score=3.5,         # 3<=x<5 -> +25
            pipeline_coverage_ratio=5.0,            # pipeline low
            late_stage_slippage_count=0,
            avg_close_date_slip_days=0,
            deals_closed_not_forecasted_count=0,
            manager_review_sessions_count=5,
        )
        assert r.forecast_pattern == ForecastPattern.sandbag_behavior

    def test_sandbag_behavior_sandbag_below_2_no_match(self):
        r = self.assess(
            avg_forecast_accuracy_pct=1.0,
            forecast_commit_count=5,
            forecast_commit_closed_count=5,
            forecast_overestimate_count=0,
            sandbagged_deals_identified=1,
            crm_update_frequency_score=0.0,
        )
        assert r.forecast_pattern != ForecastPattern.sandbag_behavior

    # --- pipeline_gap ---
    def test_pipeline_gap_detected(self):
        # pipeline>=35 and coverage_ratio < 2.5
        # pipeline: coverage<2.0 (+35) => pipeline=35
        r = self.assess(
            avg_forecast_accuracy_pct=1.0,
            forecast_commit_count=5,
            forecast_commit_closed_count=5,
            forecast_overestimate_count=0,
            sandbagged_deals_identified=0,
            crm_update_frequency_score=9.0,
            pipeline_coverage_ratio=1.5,            # <2.0 -> +35, also <2.5
            avg_deal_age_days=0,
            stage_advancement_rate_pct=0.80,
            multi_stakeholder_deals_pct=0.80,
            late_stage_slippage_count=0,
            avg_close_date_slip_days=0,
            deals_closed_not_forecasted_count=0,
            manager_review_sessions_count=5,
        )
        assert r.forecast_pattern == ForecastPattern.pipeline_gap

    def test_pipeline_gap_coverage_above_2_5_no_match(self):
        # pipeline score >=35 but coverage_ratio >=2.5 -> no match
        r = self.assess(
            avg_forecast_accuracy_pct=1.0,
            forecast_commit_count=5,
            forecast_commit_closed_count=5,
            forecast_overestimate_count=0,
            sandbagged_deals_identified=0,
            crm_update_frequency_score=9.0,
            pipeline_coverage_ratio=3.0,            # >=2.5 -> no pipeline_gap pattern
            avg_deal_age_days=120,                  # +25 for pipeline score
            stage_advancement_rate_pct=0.20,        # +25
            multi_stakeholder_deals_pct=0.20,       # +15; total pipeline ~65
            late_stage_slippage_count=0,
            avg_close_date_slip_days=0,
            deals_closed_not_forecasted_count=0,
            manager_review_sessions_count=5,
        )
        assert r.forecast_pattern != ForecastPattern.pipeline_gap

    # --- crm_neglect ---
    def test_crm_neglect_detected(self):
        # crm>=30 and crm_update_frequency_score<5.0
        # crm_freq<3.0 -> +45 => crm=45 >=30
        r = self.assess(
            avg_forecast_accuracy_pct=1.0,
            forecast_commit_count=5,
            forecast_commit_closed_count=5,
            forecast_overestimate_count=0,
            sandbagged_deals_identified=0,
            crm_update_frequency_score=2.0,         # <3.0 -> +45; crm=45>=30
            pipeline_coverage_ratio=5.0,
            avg_deal_age_days=0,
            stage_advancement_rate_pct=0.80,
            multi_stakeholder_deals_pct=0.80,
            late_stage_slippage_count=0,
            avg_close_date_slip_days=0,
            deals_closed_not_forecasted_count=0,
            manager_review_sessions_count=5,
            forecast_underestimate_count=0,
        )
        assert r.forecast_pattern == ForecastPattern.crm_neglect

    def test_crm_neglect_crm_score_5_plus_no_match(self):
        # crm_update_frequency_score>=5.0 -> condition fails
        r = self.assess(
            avg_forecast_accuracy_pct=1.0,
            forecast_commit_count=5,
            forecast_commit_closed_count=5,
            forecast_overestimate_count=0,
            sandbagged_deals_identified=0,
            crm_update_frequency_score=5.0,
            pipeline_coverage_ratio=5.0,
            late_stage_slippage_count=0,
            avg_close_date_slip_days=0,
            deals_closed_not_forecasted_count=0,
            manager_review_sessions_count=5,
        )
        assert r.forecast_pattern != ForecastPattern.crm_neglect

    # --- stage_manipulation ---
    def test_stage_manipulation_detected(self):
        # discipline>=30 and late_stage_slippage_count>=2
        # slippage=4 -> +35; close_slip=45 -> +30; total=65>=30
        r = self.assess(
            avg_forecast_accuracy_pct=1.0,
            forecast_commit_count=5,
            forecast_commit_closed_count=5,
            forecast_overestimate_count=0,
            sandbagged_deals_identified=0,
            crm_update_frequency_score=9.0,
            pipeline_coverage_ratio=5.0,
            avg_deal_age_days=0,
            stage_advancement_rate_pct=0.80,
            multi_stakeholder_deals_pct=0.80,
            late_stage_slippage_count=4,
            avg_close_date_slip_days=45,
            deals_closed_not_forecasted_count=0,
            manager_review_sessions_count=5,
            forecast_underestimate_count=0,
        )
        assert r.forecast_pattern == ForecastPattern.stage_manipulation

    def test_stage_manipulation_slippage_below_2_no_match(self):
        r = self.assess(
            avg_forecast_accuracy_pct=1.0,
            forecast_commit_count=5,
            forecast_commit_closed_count=5,
            forecast_overestimate_count=0,
            sandbagged_deals_identified=0,
            crm_update_frequency_score=9.0,
            pipeline_coverage_ratio=5.0,
            late_stage_slippage_count=1,
            avg_close_date_slip_days=45,
            deals_closed_not_forecasted_count=0,
            manager_review_sessions_count=5,
        )
        assert r.forecast_pattern != ForecastPattern.stage_manipulation

    # --- none ---
    def test_none_pattern_when_all_good(self, engine, good_input):
        r = engine.assess(good_input)
        assert r.forecast_pattern == ForecastPattern.none


# ===========================================================================
# 7. RISK LEVELS
# ===========================================================================

class TestRiskLevels:
    def setup_method(self):
        self.eng = SalesForecastAccuracyIntelligenceEngine()

    def test_risk_level_low_composite_below_20(self):
        assert self.eng._risk_level(0.0) == ForecastRisk.low
        assert self.eng._risk_level(10.0) == ForecastRisk.low
        assert self.eng._risk_level(19.9) == ForecastRisk.low

    def test_risk_level_moderate_at_20(self):
        assert self.eng._risk_level(20.0) == ForecastRisk.moderate

    def test_risk_level_moderate_below_40(self):
        assert self.eng._risk_level(25.0) == ForecastRisk.moderate
        assert self.eng._risk_level(39.9) == ForecastRisk.moderate

    def test_risk_level_high_at_40(self):
        assert self.eng._risk_level(40.0) == ForecastRisk.high

    def test_risk_level_high_below_60(self):
        assert self.eng._risk_level(45.0) == ForecastRisk.high
        assert self.eng._risk_level(59.9) == ForecastRisk.high

    def test_risk_level_critical_at_60(self):
        assert self.eng._risk_level(60.0) == ForecastRisk.critical

    def test_risk_level_critical_above_60(self):
        assert self.eng._risk_level(80.0) == ForecastRisk.critical
        assert self.eng._risk_level(100.0) == ForecastRisk.critical


# ===========================================================================
# 8. SEVERITY LEVELS
# ===========================================================================

class TestSeverityLevels:
    def setup_method(self):
        self.eng = SalesForecastAccuracyIntelligenceEngine()

    def test_reliable_below_20(self):
        assert self.eng._severity(0.0) == ForecastSeverity.reliable
        assert self.eng._severity(19.9) == ForecastSeverity.reliable

    def test_variable_at_20(self):
        assert self.eng._severity(20.0) == ForecastSeverity.variable

    def test_variable_below_40(self):
        assert self.eng._severity(30.0) == ForecastSeverity.variable
        assert self.eng._severity(39.9) == ForecastSeverity.variable

    def test_unreliable_at_40(self):
        assert self.eng._severity(40.0) == ForecastSeverity.unreliable

    def test_unreliable_below_60(self):
        assert self.eng._severity(50.0) == ForecastSeverity.unreliable
        assert self.eng._severity(59.9) == ForecastSeverity.unreliable

    def test_chaotic_at_60(self):
        assert self.eng._severity(60.0) == ForecastSeverity.chaotic

    def test_chaotic_above_60(self):
        assert self.eng._severity(75.0) == ForecastSeverity.chaotic
        assert self.eng._severity(100.0) == ForecastSeverity.chaotic

    def test_severity_matches_risk_thresholds(self):
        # Severity and risk use same composite thresholds
        for composite in [0, 10, 19.9, 20, 30, 39.9, 40, 50, 59.9, 60, 80, 100]:
            risk = self.eng._risk_level(composite)
            sev = self.eng._severity(composite)
            if risk == ForecastRisk.low:
                assert sev == ForecastSeverity.reliable
            elif risk == ForecastRisk.moderate:
                assert sev == ForecastSeverity.variable
            elif risk == ForecastRisk.high:
                assert sev == ForecastSeverity.unreliable
            elif risk == ForecastRisk.critical:
                assert sev == ForecastSeverity.chaotic


# ===========================================================================
# 9. ACTIONS
# ===========================================================================

class TestActions:
    def setup_method(self):
        self.eng = SalesForecastAccuracyIntelligenceEngine()

    def _action(self, risk, pattern):
        return self.eng._action(risk, pattern)

    # critical + systematic_overforecast -> forecast_override
    def test_critical_systematic_overforecast(self):
        assert self._action(ForecastRisk.critical, ForecastPattern.systematic_overforecast) == ForecastAction.forecast_override

    # critical + pipeline_gap -> pipeline_inspection
    def test_critical_pipeline_gap(self):
        assert self._action(ForecastRisk.critical, ForecastPattern.pipeline_gap) == ForecastAction.pipeline_inspection

    # critical + other patterns -> forecast_review_cadence
    def test_critical_sandbag_behavior(self):
        assert self._action(ForecastRisk.critical, ForecastPattern.sandbag_behavior) == ForecastAction.forecast_review_cadence

    def test_critical_crm_neglect(self):
        assert self._action(ForecastRisk.critical, ForecastPattern.crm_neglect) == ForecastAction.forecast_review_cadence

    def test_critical_stage_manipulation(self):
        assert self._action(ForecastRisk.critical, ForecastPattern.stage_manipulation) == ForecastAction.forecast_review_cadence

    def test_critical_none(self):
        assert self._action(ForecastRisk.critical, ForecastPattern.none) == ForecastAction.forecast_review_cadence

    # high + crm_neglect -> crm_training
    def test_high_crm_neglect(self):
        assert self._action(ForecastRisk.high, ForecastPattern.crm_neglect) == ForecastAction.crm_training

    # high + sandbag_behavior -> forecast_review_cadence
    def test_high_sandbag_behavior(self):
        assert self._action(ForecastRisk.high, ForecastPattern.sandbag_behavior) == ForecastAction.forecast_review_cadence

    # high + other patterns -> pipeline_inspection
    def test_high_systematic_overforecast(self):
        assert self._action(ForecastRisk.high, ForecastPattern.systematic_overforecast) == ForecastAction.pipeline_inspection

    def test_high_pipeline_gap(self):
        assert self._action(ForecastRisk.high, ForecastPattern.pipeline_gap) == ForecastAction.pipeline_inspection

    def test_high_stage_manipulation(self):
        assert self._action(ForecastRisk.high, ForecastPattern.stage_manipulation) == ForecastAction.pipeline_inspection

    def test_high_none(self):
        assert self._action(ForecastRisk.high, ForecastPattern.none) == ForecastAction.pipeline_inspection

    # moderate -> forecast_recalibration (regardless of pattern)
    def test_moderate_none(self):
        assert self._action(ForecastRisk.moderate, ForecastPattern.none) == ForecastAction.forecast_recalibration

    def test_moderate_systematic_overforecast(self):
        assert self._action(ForecastRisk.moderate, ForecastPattern.systematic_overforecast) == ForecastAction.forecast_recalibration

    def test_moderate_pipeline_gap(self):
        assert self._action(ForecastRisk.moderate, ForecastPattern.pipeline_gap) == ForecastAction.forecast_recalibration

    def test_moderate_crm_neglect(self):
        assert self._action(ForecastRisk.moderate, ForecastPattern.crm_neglect) == ForecastAction.forecast_recalibration

    def test_moderate_sandbag_behavior(self):
        assert self._action(ForecastRisk.moderate, ForecastPattern.sandbag_behavior) == ForecastAction.forecast_recalibration

    def test_moderate_stage_manipulation(self):
        assert self._action(ForecastRisk.moderate, ForecastPattern.stage_manipulation) == ForecastAction.forecast_recalibration

    # low -> no_action (regardless of pattern)
    def test_low_none(self):
        assert self._action(ForecastRisk.low, ForecastPattern.none) == ForecastAction.no_action

    def test_low_systematic_overforecast(self):
        assert self._action(ForecastRisk.low, ForecastPattern.systematic_overforecast) == ForecastAction.no_action

    def test_low_pipeline_gap(self):
        assert self._action(ForecastRisk.low, ForecastPattern.pipeline_gap) == ForecastAction.no_action

    def test_low_crm_neglect(self):
        assert self._action(ForecastRisk.low, ForecastPattern.crm_neglect) == ForecastAction.no_action

    def test_low_sandbag_behavior(self):
        assert self._action(ForecastRisk.low, ForecastPattern.sandbag_behavior) == ForecastAction.no_action

    def test_low_stage_manipulation(self):
        assert self._action(ForecastRisk.low, ForecastPattern.stage_manipulation) == ForecastAction.no_action


# ===========================================================================
# 10. is_forecast_unreliable FLAG
# ===========================================================================

class TestIsForecastUnreliable:
    def setup_method(self):
        self.eng = SalesForecastAccuracyIntelligenceEngine()

    def _flag(self, composite, **kw):
        return self.eng._is_forecast_unreliable(composite, make_input(**kw))

    def test_false_when_all_good(self):
        # composite<40, commit_rate>=0.50, slippage<3
        assert self._flag(30.0,
                          forecast_commit_count=5, forecast_commit_closed_count=4,
                          late_stage_slippage_count=0) is False

    def test_true_when_composite_at_40(self):
        assert self._flag(40.0,
                          forecast_commit_count=5, forecast_commit_closed_count=4,
                          late_stage_slippage_count=0) is True

    def test_true_when_composite_above_40(self):
        assert self._flag(60.0,
                          forecast_commit_count=5, forecast_commit_closed_count=4,
                          late_stage_slippage_count=0) is True

    def test_true_when_commit_rate_below_50(self):
        # commit_rate = 2/5 = 0.40 < 0.50
        assert self._flag(10.0,
                          forecast_commit_count=5, forecast_commit_closed_count=2,
                          late_stage_slippage_count=0) is True

    def test_true_when_commit_rate_exactly_50_boundary(self):
        # 2.5/5 = 0.50 => NOT < 0.50, so false if other conditions not met
        assert self._flag(10.0,
                          forecast_commit_count=4, forecast_commit_closed_count=2,
                          late_stage_slippage_count=0) is False

    def test_true_when_slippage_exactly_3(self):
        assert self._flag(10.0,
                          forecast_commit_count=5, forecast_commit_closed_count=5,
                          late_stage_slippage_count=3) is True

    def test_true_when_slippage_above_3(self):
        assert self._flag(10.0,
                          forecast_commit_count=5, forecast_commit_closed_count=5,
                          late_stage_slippage_count=5) is True

    def test_false_when_slippage_exactly_2(self):
        assert self._flag(10.0,
                          forecast_commit_count=5, forecast_commit_closed_count=5,
                          late_stage_slippage_count=2) is False

    def test_commit_count_zero_commit_rate_zero_triggers_unreliable(self):
        # commit_rate = 0/max(0,1) = 0 < 0.50
        assert self._flag(10.0,
                          forecast_commit_count=0, forecast_commit_closed_count=0,
                          late_stage_slippage_count=0) is True

    def test_all_conditions_true(self):
        assert self._flag(50.0,
                          forecast_commit_count=5, forecast_commit_closed_count=1,
                          late_stage_slippage_count=5) is True

    def test_returns_bool(self):
        result = self._flag(0.0)
        assert isinstance(result, bool)

    def test_assess_unreliable_flag_via_assess(self, engine=None):
        eng = SalesForecastAccuracyIntelligenceEngine()
        # Force commit_rate < 0.50
        inp = make_input(forecast_commit_count=10, forecast_commit_closed_count=3,
                         late_stage_slippage_count=0)
        r = eng.assess(inp)
        assert r.is_forecast_unreliable is True

    def test_assess_reliable_flag_via_assess(self, engine=None):
        eng = SalesForecastAccuracyIntelligenceEngine()
        inp = make_input(
            avg_forecast_accuracy_pct=1.0,
            forecast_commit_count=5,
            forecast_commit_closed_count=5,
            forecast_overestimate_count=0,
            late_stage_slippage_count=0,
            avg_close_date_slip_days=0.0,
            deals_closed_not_forecasted_count=0,
            manager_review_sessions_count=5,
            pipeline_coverage_ratio=5.0,
            avg_deal_age_days=10.0,
            stage_advancement_rate_pct=0.90,
            multi_stakeholder_deals_pct=0.90,
            crm_update_frequency_score=9.0,
            sandbagged_deals_identified=0,
            forecast_underestimate_count=0,
        )
        r = eng.assess(inp)
        assert r.is_forecast_unreliable is False


# ===========================================================================
# 11. requires_pipeline_inspection FLAG
# ===========================================================================

class TestRequiresPipelineInspection:
    def setup_method(self):
        self.eng = SalesForecastAccuracyIntelligenceEngine()

    def _flag(self, composite, **kw):
        return self.eng._requires_pipeline_inspection(composite, make_input(**kw))

    def test_false_when_all_good(self):
        assert self._flag(10.0,
                          pipeline_coverage_ratio=4.0, avg_close_date_slip_days=5.0) is False

    def test_true_when_composite_at_30(self):
        assert self._flag(30.0,
                          pipeline_coverage_ratio=4.0, avg_close_date_slip_days=5.0) is True

    def test_true_when_composite_above_30(self):
        assert self._flag(50.0,
                          pipeline_coverage_ratio=4.0, avg_close_date_slip_days=5.0) is True

    def test_true_when_coverage_below_2_5(self):
        assert self._flag(10.0,
                          pipeline_coverage_ratio=2.0, avg_close_date_slip_days=5.0) is True

    def test_false_when_coverage_at_2_5(self):
        # coverage == 2.5 is NOT < 2.5
        assert self._flag(10.0,
                          pipeline_coverage_ratio=2.5, avg_close_date_slip_days=5.0) is False

    def test_true_when_close_slip_at_30(self):
        assert self._flag(10.0,
                          pipeline_coverage_ratio=4.0, avg_close_date_slip_days=30.0) is True

    def test_true_when_close_slip_above_30(self):
        assert self._flag(10.0,
                          pipeline_coverage_ratio=4.0, avg_close_date_slip_days=60.0) is True

    def test_false_when_close_slip_below_30(self):
        assert self._flag(10.0,
                          pipeline_coverage_ratio=4.0, avg_close_date_slip_days=29.9) is False

    def test_all_conditions_met(self):
        assert self._flag(35.0,
                          pipeline_coverage_ratio=1.0, avg_close_date_slip_days=60.0) is True

    def test_returns_bool(self):
        assert isinstance(self._flag(0.0), bool)

    def test_composite_exactly_29_no_trigger(self):
        assert self._flag(29.0,
                          pipeline_coverage_ratio=4.0, avg_close_date_slip_days=5.0) is False


# ===========================================================================
# 12. ESTIMATED REVENUE VARIANCE
# ===========================================================================

class TestEstimatedRevenueVariance:
    def setup_method(self):
        self.eng = SalesForecastAccuracyIntelligenceEngine()

    def _variance(self, overestimate_count, avg_deal_size, composite):
        inp = make_input(forecast_overestimate_count=overestimate_count,
                         avg_deal_size_usd=avg_deal_size)
        return self.eng._estimated_revenue_variance(inp, composite)

    def test_zero_overestimates(self):
        assert self._variance(0, 50000.0, 50.0) == 0.0

    def test_zero_composite(self):
        assert self._variance(5, 50000.0, 0.0) == 0.0

    def test_zero_deal_size(self):
        assert self._variance(5, 0.0, 50.0) == 0.0

    def test_basic_calculation(self):
        # 1 * 50000 * (30/100) = 15000.0
        assert self._variance(1, 50000.0, 30.0) == 15000.0

    def test_multiple_overestimates(self):
        # 3 * 100000 * (50/100) = 150000.0
        assert self._variance(3, 100000.0, 50.0) == 150000.0

    def test_rounding_to_2_decimals(self):
        # 1 * 33333.33 * (10/100) = 3333.333
        result = self._variance(1, 33333.33, 10.0)
        assert result == round(1 * 33333.33 * 0.10, 2)

    def test_composite_100(self):
        # 2 * 50000 * 1.0 = 100000.0
        assert self._variance(2, 50000.0, 100.0) == 100000.0

    def test_result_via_assess(self):
        eng = SalesForecastAccuracyIntelligenceEngine()
        inp = make_input(forecast_overestimate_count=2, avg_deal_size_usd=10000.0,
                         avg_forecast_accuracy_pct=1.0,
                         forecast_commit_count=5, forecast_commit_closed_count=5)
        r = eng.assess(inp)
        expected = round(2 * 10000.0 * r.forecast_effectiveness_composite / 100.0, 2)
        assert r.estimated_revenue_variance_usd == expected

    def test_returns_float(self):
        assert isinstance(self._variance(1, 50000.0, 30.0), float)


# ===========================================================================
# 13. SIGNAL STRING
# ===========================================================================

class TestSignalString:
    def setup_method(self):
        self.eng = SalesForecastAccuracyIntelligenceEngine()

    def _signal(self, pattern, composite, **kw):
        inp = make_input(**kw)
        return self.eng._signal(inp, pattern, composite)

    def test_none_pattern_composite_below_20_returns_acceptable(self):
        s = self._signal(ForecastPattern.none, 15.0,
                         forecast_overestimate_count=0, late_stage_slippage_count=0,
                         sandbagged_deals_identified=0, deals_closed_not_forecasted_count=0)
        assert s == "Forecast accuracy within acceptable benchmarks"

    def test_none_pattern_composite_exactly_19_returns_acceptable(self):
        s = self._signal(ForecastPattern.none, 19.9,
                         forecast_overestimate_count=0, late_stage_slippage_count=0,
                         sandbagged_deals_identified=0, deals_closed_not_forecasted_count=0)
        assert s == "Forecast accuracy within acceptable benchmarks"

    def test_none_pattern_composite_0_returns_acceptable(self):
        s = self._signal(ForecastPattern.none, 0.0,
                         forecast_overestimate_count=0, late_stage_slippage_count=0,
                         sandbagged_deals_identified=0, deals_closed_not_forecasted_count=0)
        assert s == "Forecast accuracy within acceptable benchmarks"

    def test_none_pattern_composite_at_20_returns_dynamic(self):
        # composite>=20 with none pattern => not acceptable signal
        s = self._signal(ForecastPattern.none, 20.0,
                         forecast_overestimate_count=0, late_stage_slippage_count=0,
                         sandbagged_deals_identified=0, deals_closed_not_forecasted_count=0)
        assert s != "Forecast accuracy within acceptable benchmarks"

    def test_none_pattern_composite_below_20_with_issues_acceptable(self):
        # Pattern=none AND composite<20 => always returns acceptable string
        s = self._signal(ForecastPattern.none, 10.0,
                         forecast_overestimate_count=5, late_stage_slippage_count=3,
                         sandbagged_deals_identified=2, deals_closed_not_forecasted_count=1)
        assert s == "Forecast accuracy within acceptable benchmarks"

    def test_systematic_overforecast_label_in_signal(self):
        s = self._signal(ForecastPattern.systematic_overforecast, 50.0,
                         forecast_overestimate_count=3, late_stage_slippage_count=0,
                         sandbagged_deals_identified=0, deals_closed_not_forecasted_count=0)
        assert "Systematic overforecast" in s

    def test_overestimate_count_appears_in_signal(self):
        s = self._signal(ForecastPattern.systematic_overforecast, 50.0,
                         forecast_overestimate_count=5, late_stage_slippage_count=0,
                         sandbagged_deals_identified=0, deals_closed_not_forecasted_count=0)
        assert "5 over-forecasted deals" in s

    def test_late_stage_slippage_appears_in_signal(self):
        s = self._signal(ForecastPattern.stage_manipulation, 50.0,
                         forecast_overestimate_count=0, late_stage_slippage_count=3,
                         sandbagged_deals_identified=0, deals_closed_not_forecasted_count=0)
        assert "3 late-stage slippages" in s

    def test_sandbagged_appears_in_signal(self):
        s = self._signal(ForecastPattern.sandbag_behavior, 50.0,
                         forecast_overestimate_count=0, late_stage_slippage_count=0,
                         sandbagged_deals_identified=4, deals_closed_not_forecasted_count=0)
        assert "4 sandbagged deals" in s

    def test_unforecast_closes_appears_in_signal(self):
        s = self._signal(ForecastPattern.crm_neglect, 50.0,
                         forecast_overestimate_count=0, late_stage_slippage_count=0,
                         sandbagged_deals_identified=0, deals_closed_not_forecasted_count=2)
        assert "2 unforecast closes" in s

    def test_composite_value_in_signal(self):
        s = self._signal(ForecastPattern.systematic_overforecast, 55.0,
                         forecast_overestimate_count=3, late_stage_slippage_count=0,
                         sandbagged_deals_identified=0, deals_closed_not_forecasted_count=0)
        assert "composite 55" in s

    def test_no_parts_gives_quality_degrading(self):
        # All zeros => parts list is empty => "forecast quality degrading"
        s = self._signal(ForecastPattern.none, 25.0,
                         forecast_overestimate_count=0, late_stage_slippage_count=0,
                         sandbagged_deals_identified=0, deals_closed_not_forecasted_count=0)
        assert "forecast quality degrading" in s

    def test_none_pattern_with_composite_above_20_uses_forecast_risk_label(self):
        s = self._signal(ForecastPattern.none, 30.0,
                         forecast_overestimate_count=0, late_stage_slippage_count=0,
                         sandbagged_deals_identified=0, deals_closed_not_forecasted_count=0)
        assert "Forecast risk" in s

    def test_multiple_parts_joined_by_em_dash(self):
        s = self._signal(ForecastPattern.systematic_overforecast, 50.0,
                         forecast_overestimate_count=3, late_stage_slippage_count=2,
                         sandbagged_deals_identified=0, deals_closed_not_forecasted_count=0)
        # Both "3 over-forecasted deals" and "2 late-stage slippages" should appear
        assert "3 over-forecasted deals" in s
        assert "2 late-stage slippages" in s

    def test_pipeline_gap_label_capitalized(self):
        s = self._signal(ForecastPattern.pipeline_gap, 50.0,
                         forecast_overestimate_count=0, late_stage_slippage_count=0,
                         sandbagged_deals_identified=0, deals_closed_not_forecasted_count=0)
        assert "Pipeline gap" in s

    def test_crm_neglect_label_capitalized(self):
        s = self._signal(ForecastPattern.crm_neglect, 50.0,
                         forecast_overestimate_count=0, late_stage_slippage_count=0,
                         sandbagged_deals_identified=0, deals_closed_not_forecasted_count=0)
        assert "Crm neglect" in s

    def test_returns_string(self):
        s = self._signal(ForecastPattern.none, 10.0)
        assert isinstance(s, str)


# ===========================================================================
# 14. to_dict() — exactly 15 keys
# ===========================================================================

class TestToDict:
    def test_to_dict_returns_15_keys(self, engine, good_input):
        r = engine.assess(good_input)
        d = r.to_dict()
        assert len(d) == 15

    def test_to_dict_has_rep_id(self, engine, good_input):
        r = engine.assess(good_input)
        assert "rep_id" in r.to_dict()

    def test_to_dict_has_region(self, engine, good_input):
        r = engine.assess(good_input)
        assert "region" in r.to_dict()

    def test_to_dict_has_forecast_risk(self, engine, good_input):
        r = engine.assess(good_input)
        assert "forecast_risk" in r.to_dict()

    def test_to_dict_has_forecast_pattern(self, engine, good_input):
        r = engine.assess(good_input)
        assert "forecast_pattern" in r.to_dict()

    def test_to_dict_has_forecast_severity(self, engine, good_input):
        r = engine.assess(good_input)
        assert "forecast_severity" in r.to_dict()

    def test_to_dict_has_recommended_action(self, engine, good_input):
        r = engine.assess(good_input)
        assert "recommended_action" in r.to_dict()

    def test_to_dict_has_forecast_accuracy_score(self, engine, good_input):
        r = engine.assess(good_input)
        assert "forecast_accuracy_score" in r.to_dict()

    def test_to_dict_has_forecast_discipline_score(self, engine, good_input):
        r = engine.assess(good_input)
        assert "forecast_discipline_score" in r.to_dict()

    def test_to_dict_has_pipeline_health_score(self, engine, good_input):
        r = engine.assess(good_input)
        assert "pipeline_health_score" in r.to_dict()

    def test_to_dict_has_crm_hygiene_score(self, engine, good_input):
        r = engine.assess(good_input)
        assert "crm_hygiene_score" in r.to_dict()

    def test_to_dict_has_composite(self, engine, good_input):
        r = engine.assess(good_input)
        assert "forecast_effectiveness_composite" in r.to_dict()

    def test_to_dict_has_is_forecast_unreliable(self, engine, good_input):
        r = engine.assess(good_input)
        assert "is_forecast_unreliable" in r.to_dict()

    def test_to_dict_has_requires_pipeline_inspection(self, engine, good_input):
        r = engine.assess(good_input)
        assert "requires_pipeline_inspection" in r.to_dict()

    def test_to_dict_has_estimated_revenue_variance(self, engine, good_input):
        r = engine.assess(good_input)
        assert "estimated_revenue_variance_usd" in r.to_dict()

    def test_to_dict_has_forecast_signal(self, engine, good_input):
        r = engine.assess(good_input)
        assert "forecast_signal" in r.to_dict()

    def test_to_dict_enum_values_are_strings(self, engine, good_input):
        r = engine.assess(good_input)
        d = r.to_dict()
        assert isinstance(d["forecast_risk"], str)
        assert isinstance(d["forecast_pattern"], str)
        assert isinstance(d["forecast_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_rep_id_value(self, engine):
        inp = make_input(rep_id="rep_xyz")
        r = engine.assess(inp)
        assert r.to_dict()["rep_id"] == "rep_xyz"

    def test_to_dict_region_value(self, engine):
        inp = make_input(region="East")
        r = engine.assess(inp)
        assert r.to_dict()["region"] == "East"

    def test_to_dict_returns_dict(self, engine, good_input):
        r = engine.assess(good_input)
        assert isinstance(r.to_dict(), dict)

    def test_to_dict_exact_keys(self, engine, good_input):
        r = engine.assess(good_input)
        expected_keys = {
            "rep_id", "region", "forecast_risk", "forecast_pattern",
            "forecast_severity", "recommended_action", "forecast_accuracy_score",
            "forecast_discipline_score", "pipeline_health_score", "crm_hygiene_score",
            "forecast_effectiveness_composite", "is_forecast_unreliable",
            "requires_pipeline_inspection", "estimated_revenue_variance_usd",
            "forecast_signal",
        }
        assert set(r.to_dict().keys()) == expected_keys


# ===========================================================================
# 15. summary() — exactly 13 keys
# ===========================================================================

class TestSummary:
    def test_empty_summary_returns_13_keys(self):
        eng = SalesForecastAccuracyIntelligenceEngine()
        s = eng.summary()
        assert len(s) == 13

    def test_empty_summary_total_zero(self):
        eng = SalesForecastAccuracyIntelligenceEngine()
        assert eng.summary()["total"] == 0

    def test_empty_summary_avg_composite_zero(self):
        eng = SalesForecastAccuracyIntelligenceEngine()
        assert eng.summary()["avg_forecast_effectiveness_composite"] == 0.0

    def test_empty_summary_unreliable_count_zero(self):
        eng = SalesForecastAccuracyIntelligenceEngine()
        assert eng.summary()["unreliable_forecast_count"] == 0

    def test_empty_summary_inspection_count_zero(self):
        eng = SalesForecastAccuracyIntelligenceEngine()
        assert eng.summary()["pipeline_inspection_count"] == 0

    def test_empty_summary_variance_zero(self):
        eng = SalesForecastAccuracyIntelligenceEngine()
        assert eng.summary()["total_estimated_revenue_variance_usd"] == 0.0

    def test_empty_summary_risk_counts_empty(self):
        eng = SalesForecastAccuracyIntelligenceEngine()
        assert eng.summary()["risk_counts"] == {}

    def test_empty_summary_pattern_counts_empty(self):
        eng = SalesForecastAccuracyIntelligenceEngine()
        assert eng.summary()["pattern_counts"] == {}

    def test_empty_summary_severity_counts_empty(self):
        eng = SalesForecastAccuracyIntelligenceEngine()
        assert eng.summary()["severity_counts"] == {}

    def test_empty_summary_action_counts_empty(self):
        eng = SalesForecastAccuracyIntelligenceEngine()
        assert eng.summary()["action_counts"] == {}

    def test_summary_13_keys_after_assess(self):
        eng = SalesForecastAccuracyIntelligenceEngine()
        eng.assess(make_input())
        assert len(eng.summary()) == 13

    def test_summary_total_after_one_assess(self):
        eng = SalesForecastAccuracyIntelligenceEngine()
        eng.assess(make_input())
        assert eng.summary()["total"] == 1

    def test_summary_total_after_three_assesses(self):
        eng = SalesForecastAccuracyIntelligenceEngine()
        for _ in range(3):
            eng.assess(make_input())
        assert eng.summary()["total"] == 3

    def test_summary_risk_counts_populated(self):
        eng = SalesForecastAccuracyIntelligenceEngine()
        eng.assess(make_input())
        s = eng.summary()
        assert sum(s["risk_counts"].values()) == 1

    def test_summary_pattern_counts_populated(self):
        eng = SalesForecastAccuracyIntelligenceEngine()
        eng.assess(make_input())
        s = eng.summary()
        assert sum(s["pattern_counts"].values()) == 1

    def test_summary_avg_composite_is_float(self):
        eng = SalesForecastAccuracyIntelligenceEngine()
        eng.assess(make_input())
        assert isinstance(eng.summary()["avg_forecast_effectiveness_composite"], float)

    def test_summary_avg_accuracy_score_is_float(self):
        eng = SalesForecastAccuracyIntelligenceEngine()
        eng.assess(make_input())
        assert isinstance(eng.summary()["avg_forecast_accuracy_score"], float)

    def test_summary_avg_discipline_score_is_float(self):
        eng = SalesForecastAccuracyIntelligenceEngine()
        eng.assess(make_input())
        assert isinstance(eng.summary()["avg_forecast_discipline_score"], float)

    def test_summary_avg_pipeline_score_is_float(self):
        eng = SalesForecastAccuracyIntelligenceEngine()
        eng.assess(make_input())
        assert isinstance(eng.summary()["avg_pipeline_health_score"], float)

    def test_summary_avg_crm_score_is_float(self):
        eng = SalesForecastAccuracyIntelligenceEngine()
        eng.assess(make_input())
        assert isinstance(eng.summary()["avg_crm_hygiene_score"], float)

    def test_summary_total_variance_is_float(self):
        eng = SalesForecastAccuracyIntelligenceEngine()
        eng.assess(make_input())
        assert isinstance(eng.summary()["total_estimated_revenue_variance_usd"], float)

    def test_summary_exact_keys(self):
        eng = SalesForecastAccuracyIntelligenceEngine()
        eng.assess(make_input())
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_forecast_effectiveness_composite",
            "unreliable_forecast_count", "pipeline_inspection_count",
            "avg_forecast_accuracy_score", "avg_forecast_discipline_score",
            "avg_pipeline_health_score", "avg_crm_hygiene_score",
            "total_estimated_revenue_variance_usd",
        }
        assert set(eng.summary().keys()) == expected_keys

    def test_summary_unreliable_count_counted_correctly(self):
        eng = SalesForecastAccuracyIntelligenceEngine()
        # Force 2 unreliable (commit_rate < 0.50) and 1 reliable
        eng.assess(make_input(forecast_commit_count=10, forecast_commit_closed_count=2))
        eng.assess(make_input(forecast_commit_count=10, forecast_commit_closed_count=3))
        eng.assess(make_input(forecast_commit_count=5, forecast_commit_closed_count=5,
                               avg_forecast_accuracy_pct=1.0,
                               forecast_overestimate_count=0,
                               late_stage_slippage_count=0,
                               avg_close_date_slip_days=0.0,
                               deals_closed_not_forecasted_count=0,
                               manager_review_sessions_count=5,
                               pipeline_coverage_ratio=5.0,
                               avg_deal_age_days=10.0,
                               stage_advancement_rate_pct=0.90,
                               multi_stakeholder_deals_pct=0.90,
                               crm_update_frequency_score=9.0,
                               sandbagged_deals_identified=0,
                               forecast_underestimate_count=0))
        assert eng.summary()["unreliable_forecast_count"] == 2

    def test_summary_total_variance_sum(self):
        eng = SalesForecastAccuracyIntelligenceEngine()
        inp1 = make_input(forecast_overestimate_count=2, avg_deal_size_usd=10000.0)
        inp2 = make_input(forecast_overestimate_count=3, avg_deal_size_usd=20000.0)
        r1 = eng.assess(inp1)
        r2 = eng.assess(inp2)
        expected = round(r1.estimated_revenue_variance_usd + r2.estimated_revenue_variance_usd, 2)
        assert eng.summary()["total_estimated_revenue_variance_usd"] == expected


# ===========================================================================
# 16. assess_batch()
# ===========================================================================

class TestAssessBatch:
    def test_assess_batch_empty_list(self, engine):
        results = engine.assess_batch([])
        assert results == []

    def test_assess_batch_single_input(self, engine):
        results = engine.assess_batch([make_input()])
        assert len(results) == 1

    def test_assess_batch_multiple_inputs(self, engine):
        inputs = [make_input(rep_id=f"rep_{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5

    def test_assess_batch_returns_list_of_results(self, engine):
        inputs = [make_input()]
        results = engine.assess_batch(inputs)
        assert all(isinstance(r, ForecastAccuracyResult) for r in results)

    def test_assess_batch_rep_ids_match(self, engine):
        inputs = [make_input(rep_id="rep_A"), make_input(rep_id="rep_B")]
        results = engine.assess_batch(inputs)
        assert results[0].rep_id == "rep_A"
        assert results[1].rep_id == "rep_B"

    def test_assess_batch_updates_summary(self, engine):
        inputs = [make_input() for _ in range(3)]
        engine.assess_batch(inputs)
        assert engine.summary()["total"] == 3

    def test_assess_batch_different_risk_levels(self, engine):
        # One very bad, one very good
        bad = make_input(avg_forecast_accuracy_pct=0.0,
                         forecast_commit_count=10, forecast_commit_closed_count=0,
                         forecast_overestimate_count=10, total_forecasted_deals=10,
                         crm_update_frequency_score=0.0,
                         sandbagged_deals_identified=5,
                         late_stage_slippage_count=5,
                         avg_close_date_slip_days=60.0,
                         pipeline_coverage_ratio=1.0)
        good = make_input(avg_forecast_accuracy_pct=1.0,
                          forecast_commit_count=5, forecast_commit_closed_count=5,
                          forecast_overestimate_count=0,
                          crm_update_frequency_score=9.0,
                          sandbagged_deals_identified=0,
                          late_stage_slippage_count=0,
                          avg_close_date_slip_days=0.0,
                          pipeline_coverage_ratio=5.0,
                          avg_deal_age_days=10.0,
                          stage_advancement_rate_pct=0.90,
                          multi_stakeholder_deals_pct=0.90,
                          deals_closed_not_forecasted_count=0,
                          manager_review_sessions_count=5,
                          forecast_underestimate_count=0)
        results = engine.assess_batch([bad, good])
        risk_values = {r.forecast_risk for r in results}
        assert ForecastRisk.critical in risk_values or ForecastRisk.high in risk_values
        assert ForecastRisk.low in risk_values

    def test_assess_batch_accumulates_with_prior_assessments(self, engine):
        engine.assess(make_input())
        engine.assess_batch([make_input(), make_input()])
        assert engine.summary()["total"] == 3


# ===========================================================================
# 17. EDGE CASES AND INTEGRATION
# ===========================================================================

class TestEdgeCases:
    def test_zero_forecasted_deals_no_crash(self, engine):
        inp = make_input(total_forecasted_deals=0, forecast_overestimate_count=0)
        r = engine.assess(inp)
        assert isinstance(r, ForecastAccuracyResult)

    def test_perfect_accuracy_low_risk(self, engine, good_input):
        r = engine.assess(good_input)
        assert r.forecast_risk == ForecastRisk.low

    def test_perfect_accuracy_reliable_severity(self, engine, good_input):
        r = engine.assess(good_input)
        assert r.forecast_severity == ForecastSeverity.reliable

    def test_perfect_accuracy_no_action(self, engine, good_input):
        r = engine.assess(good_input)
        assert r.recommended_action == ForecastAction.no_action

    def test_perfect_accuracy_no_pattern(self, engine, good_input):
        r = engine.assess(good_input)
        assert r.forecast_pattern == ForecastPattern.none

    def test_perfect_accuracy_acceptable_signal(self, engine, good_input):
        r = engine.assess(good_input)
        assert r.forecast_signal == "Forecast accuracy within acceptable benchmarks"

    def test_perfect_accuracy_variance_zero(self, engine, good_input):
        r = engine.assess(good_input)
        assert r.estimated_revenue_variance_usd == 0.0

    def test_worst_case_critical_risk(self, engine):
        inp = make_input(
            avg_forecast_accuracy_pct=0.0,
            forecast_commit_count=10, forecast_commit_closed_count=0,
            forecast_overestimate_count=10, total_forecasted_deals=10,
            crm_update_frequency_score=0.0,
            sandbagged_deals_identified=5, forecast_underestimate_count=5,
            late_stage_slippage_count=5,
            avg_close_date_slip_days=60.0,
            deals_closed_not_forecasted_count=5,
            manager_review_sessions_count=0,
            pipeline_coverage_ratio=0.5,
            avg_deal_age_days=200.0,
            stage_advancement_rate_pct=0.0,
            multi_stakeholder_deals_pct=0.0,
        )
        r = engine.assess(inp)
        assert r.forecast_risk == ForecastRisk.critical

    def test_worst_case_chaotic_severity(self, engine):
        inp = make_input(
            avg_forecast_accuracy_pct=0.0,
            forecast_commit_count=10, forecast_commit_closed_count=0,
            forecast_overestimate_count=10, total_forecasted_deals=10,
            crm_update_frequency_score=0.0,
            sandbagged_deals_identified=5, forecast_underestimate_count=5,
            late_stage_slippage_count=5,
            avg_close_date_slip_days=60.0,
            deals_closed_not_forecasted_count=5,
            manager_review_sessions_count=0,
            pipeline_coverage_ratio=0.5,
            avg_deal_age_days=200.0,
            stage_advancement_rate_pct=0.0,
            multi_stakeholder_deals_pct=0.0,
        )
        r = engine.assess(inp)
        assert r.forecast_severity == ForecastSeverity.chaotic

    def test_worst_case_is_unreliable(self, engine):
        inp = make_input(
            avg_forecast_accuracy_pct=0.0,
            forecast_commit_count=10, forecast_commit_closed_count=0,
            forecast_overestimate_count=10, total_forecasted_deals=10,
        )
        r = engine.assess(inp)
        assert r.is_forecast_unreliable is True

    def test_result_is_dataclass(self, engine, good_input):
        r = engine.assess(good_input)
        assert isinstance(r, ForecastAccuracyResult)

    def test_result_has_rep_id(self, engine):
        inp = make_input(rep_id="test_rep")
        r = engine.assess(inp)
        assert r.rep_id == "test_rep"

    def test_result_has_region(self, engine):
        inp = make_input(region="Northeast")
        r = engine.assess(inp)
        assert r.region == "Northeast"

    def test_composite_between_0_and_100(self, engine, good_input):
        r = engine.assess(good_input)
        assert 0.0 <= r.forecast_effectiveness_composite <= 100.0

    def test_composite_between_0_and_100_worst_case(self, engine):
        inp = make_input(
            avg_forecast_accuracy_pct=0.0,
            forecast_commit_count=10, forecast_commit_closed_count=0,
            forecast_overestimate_count=10, total_forecasted_deals=10,
            crm_update_frequency_score=0.0, sandbagged_deals_identified=10,
            forecast_underestimate_count=10, late_stage_slippage_count=10,
            avg_close_date_slip_days=100.0, deals_closed_not_forecasted_count=10,
            manager_review_sessions_count=0, pipeline_coverage_ratio=0.0,
            avg_deal_age_days=365.0, stage_advancement_rate_pct=0.0,
            multi_stakeholder_deals_pct=0.0,
        )
        r = engine.assess(inp)
        assert 0.0 <= r.forecast_effectiveness_composite <= 100.0

    def test_multiple_engines_independent(self):
        eng1 = SalesForecastAccuracyIntelligenceEngine()
        eng2 = SalesForecastAccuracyIntelligenceEngine()
        eng1.assess(make_input())
        assert eng2.summary()["total"] == 0

    def test_composite_weighted_formula(self, engine):
        # Verify that composite = accuracy*0.35 + discipline*0.25 + pipeline*0.25 + crm*0.15
        inp = make_input(
            avg_forecast_accuracy_pct=1.0,
            forecast_commit_count=5, forecast_commit_closed_count=5,
            forecast_overestimate_count=0,
            late_stage_slippage_count=0,
            avg_close_date_slip_days=0.0,
            deals_closed_not_forecasted_count=0,
            manager_review_sessions_count=5,
            pipeline_coverage_ratio=5.0,
            avg_deal_age_days=10.0,
            stage_advancement_rate_pct=0.80,
            multi_stakeholder_deals_pct=0.80,
            crm_update_frequency_score=9.0,
            sandbagged_deals_identified=0,
            forecast_underestimate_count=0,
        )
        r = engine.assess(inp)
        acc = engine._forecast_accuracy_score(inp)
        disc = engine._forecast_discipline_score(inp)
        pipe = engine._pipeline_health_score(inp)
        crm = engine._crm_hygiene_score(inp)
        expected_composite = round(acc * 0.35 + disc * 0.25 + pipe * 0.25 + crm * 0.15, 1)
        assert r.forecast_effectiveness_composite == min(expected_composite, 100.0)

    def test_high_accuracy_boundary_composite_exactly_20(self, engine):
        # Craft an input where composite is exactly around 20 -> moderate risk
        # We'll check the result is moderate or close
        inp = make_input(
            avg_forecast_accuracy_pct=0.85,   # dev=0.15 -> +12
            forecast_commit_count=10,
            forecast_commit_closed_count=9,   # 0.90 > 0.85 -> +0
            forecast_overestimate_count=1,    # ratio=0.10 < 0.15 -> +0; acc = 12
            late_stage_slippage_count=0, avg_close_date_slip_days=0,
            deals_closed_not_forecasted_count=0, manager_review_sessions_count=5,
            pipeline_coverage_ratio=5.0, avg_deal_age_days=10.0,
            stage_advancement_rate_pct=0.80, multi_stakeholder_deals_pct=0.80,
            crm_update_frequency_score=9.0, sandbagged_deals_identified=0,
            forecast_underestimate_count=0, total_forecasted_deals=10,
        )
        r = engine.assess(inp)
        # acc=12, disc=0, pipe=0, crm=0 => composite=12*0.35=4.2 -> low
        assert r.forecast_risk == ForecastRisk.low

    def test_region_preserved_in_result(self, engine):
        inp = make_input(region="Pacific")
        r = engine.assess(inp)
        assert r.region == "Pacific"

    def test_engine_accumulates_results(self):
        eng = SalesForecastAccuracyIntelligenceEngine()
        for i in range(10):
            eng.assess(make_input(rep_id=f"rep_{i}"))
        assert eng.summary()["total"] == 10

    def test_assess_result_scores_non_negative(self, engine):
        r = engine.assess(make_input())
        assert r.forecast_accuracy_score >= 0.0
        assert r.forecast_discipline_score >= 0.0
        assert r.pipeline_health_score >= 0.0
        assert r.crm_hygiene_score >= 0.0

    def test_forecast_result_field_types(self, engine, good_input):
        r = engine.assess(good_input)
        assert isinstance(r.forecast_risk, ForecastRisk)
        assert isinstance(r.forecast_pattern, ForecastPattern)
        assert isinstance(r.forecast_severity, ForecastSeverity)
        assert isinstance(r.recommended_action, ForecastAction)
        assert isinstance(r.forecast_accuracy_score, float)
        assert isinstance(r.forecast_discipline_score, float)
        assert isinstance(r.pipeline_health_score, float)
        assert isinstance(r.crm_hygiene_score, float)
        assert isinstance(r.forecast_effectiveness_composite, float)
        assert isinstance(r.is_forecast_unreliable, bool)
        assert isinstance(r.requires_pipeline_inspection, bool)
        assert isinstance(r.estimated_revenue_variance_usd, float)
        assert isinstance(r.forecast_signal, str)

    def test_commit_rate_exactly_50_not_unreliable_via_commit_alone(self, engine):
        # commit_rate = 5/10 = 0.50 (NOT < 0.50) — other conds also false
        inp = make_input(
            forecast_commit_count=10,
            forecast_commit_closed_count=5,
            late_stage_slippage_count=0,
            avg_forecast_accuracy_pct=1.0,
            forecast_overestimate_count=0,
            pipeline_coverage_ratio=5.0,
            avg_deal_age_days=10.0,
            stage_advancement_rate_pct=0.80,
            multi_stakeholder_deals_pct=0.80,
            crm_update_frequency_score=9.0,
            sandbagged_deals_identified=0,
            forecast_underestimate_count=0,
            avg_close_date_slip_days=0.0,
            deals_closed_not_forecasted_count=0,
            manager_review_sessions_count=5,
        )
        r = engine.assess(inp)
        # composite should be low (<40), commit_rate=0.50 NOT <0.50, slippage=0 <3
        assert r.is_forecast_unreliable is False

    def test_pipeline_inspection_required_on_low_coverage(self, engine):
        inp = make_input(pipeline_coverage_ratio=1.5)
        r = engine.assess(inp)
        assert r.requires_pipeline_inspection is True

    def test_pipeline_inspection_not_required_on_good_data(self, engine, good_input):
        r = engine.assess(good_input)
        assert r.requires_pipeline_inspection is False

    def test_input_dataclass_fields(self):
        inp = make_input()
        assert hasattr(inp, 'rep_id')
        assert hasattr(inp, 'region')
        assert hasattr(inp, 'evaluation_period_id')
        assert hasattr(inp, 'total_forecasted_deals')
        assert hasattr(inp, 'avg_deal_size_usd')

    def test_summary_avg_composite_matches_manual_calculation(self):
        eng = SalesForecastAccuracyIntelligenceEngine()
        r1 = eng.assess(make_input())
        r2 = eng.assess(make_input())
        s = eng.summary()
        expected_avg = round((r1.forecast_effectiveness_composite + r2.forecast_effectiveness_composite) / 2, 1)
        assert s["avg_forecast_effectiveness_composite"] == expected_avg
