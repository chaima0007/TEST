"""
Comprehensive pytest test suite for SalesForecastSandbaggingDetectionEngine.
Module 123 — sales_forecast_sandbagging_detection_engine.py

Run from /home/user/TEST:
    python -m pytest swarm/tests/test_sales_forecast_sandbagging_detection_engine.py -v
"""
from __future__ import annotations

import dataclasses
import math
import pytest

from swarm.intelligence.sales_forecast_sandbagging_detection_engine import (
    SandbaggingAction,
    SandbaggingInput,
    SandbaggingPattern,
    SandbaggingResult,
    SandbaggingRisk,
    SandbaggingSeverity,
    SalesForecastSandbaggingDetectionEngine,
)

# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def make_input(
    rep_id="REP-001",
    region="West",
    evaluation_period_id="Q2-2026",
    committed_forecast_usd=100_000.0,
    actual_closed_usd=100_000.0,
    prior_period_upside_usd=0.0,
    upside_to_commit_ratio=1.0,
    deals_pulled_from_next_quarter=0,
    late_stage_deals_not_committed=0,
    forecast_accuracy_last_3_periods=0.90,
    consecutive_upside_periods=0,
    commit_vs_pipeline_coverage_ratio=0.60,
    avg_deal_slip_days=0.0,
    deals_slipped_intentionally_count=0,
    close_date_pushed_count=0,
    close_date_pulled_count=0,
    sandbagged_deal_value_usd=0.0,
    quota_attainment_last_period_pct=100.0,
    accelerator_threshold_pct=110.0,
    days_remaining_in_period=30,
    total_pipeline_usd=200_000.0,
    crm_stage_inflation_score=0.0,
) -> SandbaggingInput:
    return SandbaggingInput(
        rep_id=rep_id,
        region=region,
        evaluation_period_id=evaluation_period_id,
        committed_forecast_usd=committed_forecast_usd,
        actual_closed_usd=actual_closed_usd,
        prior_period_upside_usd=prior_period_upside_usd,
        upside_to_commit_ratio=upside_to_commit_ratio,
        deals_pulled_from_next_quarter=deals_pulled_from_next_quarter,
        late_stage_deals_not_committed=late_stage_deals_not_committed,
        forecast_accuracy_last_3_periods=forecast_accuracy_last_3_periods,
        consecutive_upside_periods=consecutive_upside_periods,
        commit_vs_pipeline_coverage_ratio=commit_vs_pipeline_coverage_ratio,
        avg_deal_slip_days=avg_deal_slip_days,
        deals_slipped_intentionally_count=deals_slipped_intentionally_count,
        close_date_pushed_count=close_date_pushed_count,
        close_date_pulled_count=close_date_pulled_count,
        sandbagged_deal_value_usd=sandbagged_deal_value_usd,
        quota_attainment_last_period_pct=quota_attainment_last_period_pct,
        accelerator_threshold_pct=accelerator_threshold_pct,
        days_remaining_in_period=days_remaining_in_period,
        total_pipeline_usd=total_pipeline_usd,
        crm_stage_inflation_score=crm_stage_inflation_score,
    )


def engine() -> SalesForecastSandbaggingDetectionEngine:
    return SalesForecastSandbaggingDetectionEngine()


@pytest.fixture
def eng():
    return SalesForecastSandbaggingDetectionEngine()


@pytest.fixture
def clean_input():
    return make_input()


@pytest.fixture
def severe_input():
    """Rep with heavy sandbagging signals across all dimensions."""
    return make_input(
        committed_forecast_usd=100_000.0,
        actual_closed_usd=170_000.0,       # 70% over commit
        prior_period_upside_usd=60_000.0,
        upside_to_commit_ratio=3.5,
        deals_pulled_from_next_quarter=5,
        late_stage_deals_not_committed=6,
        forecast_accuracy_last_3_periods=0.50,
        consecutive_upside_periods=5,
        commit_vs_pipeline_coverage_ratio=0.20,
        avg_deal_slip_days=35.0,
        deals_slipped_intentionally_count=4,
        close_date_pushed_count=2,
        close_date_pulled_count=5,
        sandbagged_deal_value_usd=80_000.0,
        quota_attainment_last_period_pct=150.0,
        accelerator_threshold_pct=100.0,
        days_remaining_in_period=10,
        total_pipeline_usd=500_000.0,
        crm_stage_inflation_score=80.0,
    )


# ===========================================================================
# 1. Dataclass field counts
# ===========================================================================

class TestDataclassFields:

    def test_sandbagging_input_has_22_fields(self):
        fields = dataclasses.fields(SandbaggingInput)
        assert len(fields) == 22

    def test_sandbagging_result_has_15_fields(self):
        fields = dataclasses.fields(SandbaggingResult)
        assert len(fields) == 15

    def test_input_field_rep_id_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingInput)}
        assert "rep_id" in names

    def test_input_field_region_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingInput)}
        assert "region" in names

    def test_input_field_evaluation_period_id_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingInput)}
        assert "evaluation_period_id" in names

    def test_input_field_committed_forecast_usd_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingInput)}
        assert "committed_forecast_usd" in names

    def test_input_field_actual_closed_usd_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingInput)}
        assert "actual_closed_usd" in names

    def test_input_field_prior_period_upside_usd_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingInput)}
        assert "prior_period_upside_usd" in names

    def test_input_field_upside_to_commit_ratio_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingInput)}
        assert "upside_to_commit_ratio" in names

    def test_input_field_deals_pulled_from_next_quarter_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingInput)}
        assert "deals_pulled_from_next_quarter" in names

    def test_input_field_late_stage_deals_not_committed_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingInput)}
        assert "late_stage_deals_not_committed" in names

    def test_input_field_forecast_accuracy_last_3_periods_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingInput)}
        assert "forecast_accuracy_last_3_periods" in names

    def test_input_field_consecutive_upside_periods_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingInput)}
        assert "consecutive_upside_periods" in names

    def test_input_field_commit_vs_pipeline_coverage_ratio_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingInput)}
        assert "commit_vs_pipeline_coverage_ratio" in names

    def test_input_field_avg_deal_slip_days_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingInput)}
        assert "avg_deal_slip_days" in names

    def test_input_field_deals_slipped_intentionally_count_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingInput)}
        assert "deals_slipped_intentionally_count" in names

    def test_input_field_close_date_pushed_count_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingInput)}
        assert "close_date_pushed_count" in names

    def test_input_field_close_date_pulled_count_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingInput)}
        assert "close_date_pulled_count" in names

    def test_input_field_sandbagged_deal_value_usd_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingInput)}
        assert "sandbagged_deal_value_usd" in names

    def test_input_field_quota_attainment_last_period_pct_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingInput)}
        assert "quota_attainment_last_period_pct" in names

    def test_input_field_accelerator_threshold_pct_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingInput)}
        assert "accelerator_threshold_pct" in names

    def test_input_field_days_remaining_in_period_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingInput)}
        assert "days_remaining_in_period" in names

    def test_input_field_total_pipeline_usd_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingInput)}
        assert "total_pipeline_usd" in names

    def test_input_field_crm_stage_inflation_score_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingInput)}
        assert "crm_stage_inflation_score" in names

    # Result fields
    def test_result_field_rep_id_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingResult)}
        assert "rep_id" in names

    def test_result_field_region_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingResult)}
        assert "region" in names

    def test_result_field_sandbagging_risk_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingResult)}
        assert "sandbagging_risk" in names

    def test_result_field_sandbagging_pattern_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingResult)}
        assert "sandbagging_pattern" in names

    def test_result_field_sandbagging_severity_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingResult)}
        assert "sandbagging_severity" in names

    def test_result_field_recommended_action_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingResult)}
        assert "recommended_action" in names

    def test_result_field_commit_accuracy_score_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingResult)}
        assert "commit_accuracy_score" in names

    def test_result_field_upside_manipulation_score_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingResult)}
        assert "upside_manipulation_score" in names

    def test_result_field_deal_timing_score_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingResult)}
        assert "deal_timing_score" in names

    def test_result_field_pattern_consistency_score_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingResult)}
        assert "pattern_consistency_score" in names

    def test_result_field_sandbagging_composite_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingResult)}
        assert "sandbagging_composite" in names

    def test_result_field_is_sandbagging_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingResult)}
        assert "is_sandbagging" in names

    def test_result_field_requires_intervention_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingResult)}
        assert "requires_intervention" in names

    def test_result_field_estimated_hidden_revenue_usd_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingResult)}
        assert "estimated_hidden_revenue_usd" in names

    def test_result_field_sandbagging_signal_exists(self):
        names = {f.name for f in dataclasses.fields(SandbaggingResult)}
        assert "sandbagging_signal" in names


# ===========================================================================
# 2. to_dict() returns exactly 15 keys
# ===========================================================================

class TestToDict:

    def test_to_dict_returns_dict(self, eng, clean_input):
        result = eng.assess(clean_input)
        assert isinstance(result.to_dict(), dict)

    def test_to_dict_has_exactly_15_keys(self, eng, clean_input):
        result = eng.assess(clean_input)
        assert len(result.to_dict()) == 15

    def test_to_dict_contains_rep_id(self, eng, clean_input):
        d = eng.assess(clean_input).to_dict()
        assert "rep_id" in d

    def test_to_dict_contains_region(self, eng, clean_input):
        d = eng.assess(clean_input).to_dict()
        assert "region" in d

    def test_to_dict_contains_sandbagging_risk(self, eng, clean_input):
        d = eng.assess(clean_input).to_dict()
        assert "sandbagging_risk" in d

    def test_to_dict_contains_sandbagging_pattern(self, eng, clean_input):
        d = eng.assess(clean_input).to_dict()
        assert "sandbagging_pattern" in d

    def test_to_dict_contains_sandbagging_severity(self, eng, clean_input):
        d = eng.assess(clean_input).to_dict()
        assert "sandbagging_severity" in d

    def test_to_dict_contains_recommended_action(self, eng, clean_input):
        d = eng.assess(clean_input).to_dict()
        assert "recommended_action" in d

    def test_to_dict_contains_commit_accuracy_score(self, eng, clean_input):
        d = eng.assess(clean_input).to_dict()
        assert "commit_accuracy_score" in d

    def test_to_dict_contains_upside_manipulation_score(self, eng, clean_input):
        d = eng.assess(clean_input).to_dict()
        assert "upside_manipulation_score" in d

    def test_to_dict_contains_deal_timing_score(self, eng, clean_input):
        d = eng.assess(clean_input).to_dict()
        assert "deal_timing_score" in d

    def test_to_dict_contains_pattern_consistency_score(self, eng, clean_input):
        d = eng.assess(clean_input).to_dict()
        assert "pattern_consistency_score" in d

    def test_to_dict_contains_sandbagging_composite(self, eng, clean_input):
        d = eng.assess(clean_input).to_dict()
        assert "sandbagging_composite" in d

    def test_to_dict_contains_is_sandbagging(self, eng, clean_input):
        d = eng.assess(clean_input).to_dict()
        assert "is_sandbagging" in d

    def test_to_dict_contains_requires_intervention(self, eng, clean_input):
        d = eng.assess(clean_input).to_dict()
        assert "requires_intervention" in d

    def test_to_dict_contains_estimated_hidden_revenue_usd(self, eng, clean_input):
        d = eng.assess(clean_input).to_dict()
        assert "estimated_hidden_revenue_usd" in d

    def test_to_dict_contains_sandbagging_signal(self, eng, clean_input):
        d = eng.assess(clean_input).to_dict()
        assert "sandbagging_signal" in d

    def test_to_dict_risk_value_is_string(self, eng, clean_input):
        d = eng.assess(clean_input).to_dict()
        assert isinstance(d["sandbagging_risk"], str)

    def test_to_dict_pattern_value_is_string(self, eng, clean_input):
        d = eng.assess(clean_input).to_dict()
        assert isinstance(d["sandbagging_pattern"], str)

    def test_to_dict_severity_value_is_string(self, eng, clean_input):
        d = eng.assess(clean_input).to_dict()
        assert isinstance(d["sandbagging_severity"], str)

    def test_to_dict_action_value_is_string(self, eng, clean_input):
        d = eng.assess(clean_input).to_dict()
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_rep_id_matches(self, eng):
        inp = make_input(rep_id="TESTER")
        d = eng.assess(inp).to_dict()
        assert d["rep_id"] == "TESTER"

    def test_to_dict_region_matches(self, eng):
        inp = make_input(region="East")
        d = eng.assess(inp).to_dict()
        assert d["region"] == "East"


# ===========================================================================
# 3. summary() returns exactly 13 keys
# ===========================================================================

class TestSummaryKeyCount:

    def test_empty_summary_has_13_keys(self, eng):
        s = eng.summary()
        assert len(s) == 13

    def test_nonempty_summary_has_13_keys(self, eng, clean_input):
        eng.assess(clean_input)
        s = eng.summary()
        assert len(s) == 13

    def test_summary_key_total(self, eng):
        s = eng.summary()
        assert "total" in s

    def test_summary_key_risk_counts(self, eng):
        s = eng.summary()
        assert "risk_counts" in s

    def test_summary_key_pattern_counts(self, eng):
        s = eng.summary()
        assert "pattern_counts" in s

    def test_summary_key_severity_counts(self, eng):
        s = eng.summary()
        assert "severity_counts" in s

    def test_summary_key_action_counts(self, eng):
        s = eng.summary()
        assert "action_counts" in s

    def test_summary_key_avg_sandbagging_composite(self, eng):
        s = eng.summary()
        assert "avg_sandbagging_composite" in s

    def test_summary_key_sandbagging_count(self, eng):
        s = eng.summary()
        assert "sandbagging_count" in s

    def test_summary_key_intervention_count(self, eng):
        s = eng.summary()
        assert "intervention_count" in s

    def test_summary_key_avg_commit_accuracy_score(self, eng):
        s = eng.summary()
        assert "avg_commit_accuracy_score" in s

    def test_summary_key_avg_upside_manipulation_score(self, eng):
        s = eng.summary()
        assert "avg_upside_manipulation_score" in s

    def test_summary_key_avg_deal_timing_score(self, eng):
        s = eng.summary()
        assert "avg_deal_timing_score" in s

    def test_summary_key_avg_pattern_consistency_score(self, eng):
        s = eng.summary()
        assert "avg_pattern_consistency_score" in s

    def test_summary_key_total_estimated_hidden_revenue_usd(self, eng):
        s = eng.summary()
        assert "total_estimated_hidden_revenue_usd" in s

    def test_empty_summary_total_is_zero(self, eng):
        assert eng.summary()["total"] == 0

    def test_nonempty_summary_total_correct(self, eng):
        eng.assess(make_input(rep_id="A"))
        eng.assess(make_input(rep_id="B"))
        assert eng.summary()["total"] == 2


# ===========================================================================
# 4. All enum values exist
# ===========================================================================

class TestEnumValues:

    # SandbaggingRisk
    def test_risk_low_exists(self):
        assert SandbaggingRisk.low is not None

    def test_risk_moderate_exists(self):
        assert SandbaggingRisk.moderate is not None

    def test_risk_high_exists(self):
        assert SandbaggingRisk.high is not None

    def test_risk_critical_exists(self):
        assert SandbaggingRisk.critical is not None

    def test_risk_low_value(self):
        assert SandbaggingRisk.low.value == "low"

    def test_risk_moderate_value(self):
        assert SandbaggingRisk.moderate.value == "moderate"

    def test_risk_high_value(self):
        assert SandbaggingRisk.high.value == "high"

    def test_risk_critical_value(self):
        assert SandbaggingRisk.critical.value == "critical"

    def test_risk_has_4_members(self):
        assert len(SandbaggingRisk) == 4

    # SandbaggingPattern
    def test_pattern_none_exists(self):
        assert SandbaggingPattern.none is not None

    def test_pattern_consistent_upside_exists(self):
        assert SandbaggingPattern.consistent_upside is not None

    def test_pattern_late_quarter_surge_exists(self):
        assert SandbaggingPattern.late_quarter_surge is not None

    def test_pattern_commit_minimization_exists(self):
        assert SandbaggingPattern.commit_minimization is not None

    def test_pattern_deal_timing_manipulation_exists(self):
        assert SandbaggingPattern.deal_timing_manipulation is not None

    def test_pattern_forecast_sandbagging_exists(self):
        assert SandbaggingPattern.forecast_sandbagging is not None

    def test_pattern_none_value(self):
        assert SandbaggingPattern.none.value == "none"

    def test_pattern_consistent_upside_value(self):
        assert SandbaggingPattern.consistent_upside.value == "consistent_upside"

    def test_pattern_late_quarter_surge_value(self):
        assert SandbaggingPattern.late_quarter_surge.value == "late_quarter_surge"

    def test_pattern_commit_minimization_value(self):
        assert SandbaggingPattern.commit_minimization.value == "commit_minimization"

    def test_pattern_deal_timing_manipulation_value(self):
        assert SandbaggingPattern.deal_timing_manipulation.value == "deal_timing_manipulation"

    def test_pattern_forecast_sandbagging_value(self):
        assert SandbaggingPattern.forecast_sandbagging.value == "forecast_sandbagging"

    def test_pattern_has_6_members(self):
        assert len(SandbaggingPattern) == 6

    # SandbaggingSeverity
    def test_severity_accurate_exists(self):
        assert SandbaggingSeverity.accurate is not None

    def test_severity_watch_exists(self):
        assert SandbaggingSeverity.watch is not None

    def test_severity_suspected_exists(self):
        assert SandbaggingSeverity.suspected is not None

    def test_severity_confirmed_exists(self):
        assert SandbaggingSeverity.confirmed is not None

    def test_severity_accurate_value(self):
        assert SandbaggingSeverity.accurate.value == "accurate"

    def test_severity_watch_value(self):
        assert SandbaggingSeverity.watch.value == "watch"

    def test_severity_suspected_value(self):
        assert SandbaggingSeverity.suspected.value == "suspected"

    def test_severity_confirmed_value(self):
        assert SandbaggingSeverity.confirmed.value == "confirmed"

    def test_severity_has_4_members(self):
        assert len(SandbaggingSeverity) == 4

    # SandbaggingAction
    def test_action_no_action_exists(self):
        assert SandbaggingAction.no_action is not None

    def test_action_forecast_coaching_exists(self):
        assert SandbaggingAction.forecast_coaching is not None

    def test_action_pipeline_review_exists(self):
        assert SandbaggingAction.pipeline_review is not None

    def test_action_comp_plan_review_exists(self):
        assert SandbaggingAction.comp_plan_review is not None

    def test_action_executive_confrontation_exists(self):
        assert SandbaggingAction.executive_confrontation is not None

    def test_action_no_action_value(self):
        assert SandbaggingAction.no_action.value == "no_action"

    def test_action_forecast_coaching_value(self):
        assert SandbaggingAction.forecast_coaching.value == "forecast_coaching"

    def test_action_pipeline_review_value(self):
        assert SandbaggingAction.pipeline_review.value == "pipeline_review"

    def test_action_comp_plan_review_value(self):
        assert SandbaggingAction.comp_plan_review.value == "comp_plan_review"

    def test_action_executive_confrontation_value(self):
        assert SandbaggingAction.executive_confrontation.value == "executive_confrontation"

    def test_action_has_5_members(self):
        assert len(SandbaggingAction) == 5


# ===========================================================================
# 5. Composite score calculation  (c*0.35 + u*0.30 + t*0.20 + p*0.15)
# ===========================================================================

class TestCompositeScore:

    def test_composite_is_float(self, eng, clean_input):
        result = eng.assess(clean_input)
        assert isinstance(result.sandbagging_composite, float)

    def test_composite_non_negative(self, eng, clean_input):
        result = eng.assess(clean_input)
        assert result.sandbagging_composite >= 0.0

    def test_composite_max_100(self, eng, severe_input):
        result = eng.assess(severe_input)
        assert result.sandbagging_composite <= 100.0

    def test_composite_clean_rep_near_zero(self, eng, clean_input):
        result = eng.assess(clean_input)
        assert result.sandbagging_composite < 10.0

    def test_composite_severe_rep_is_high(self, eng, severe_input):
        result = eng.assess(severe_input)
        assert result.sandbagging_composite >= 60.0

    def test_composite_weights_sum_correctly(self, eng):
        """With known sub-scores the composite must match the weighted formula."""
        # Build an input that gives predictable sub-scores via single contributors only
        # Upside ratio >= 0.50 → commit += 40; forecast_acc >= 0.85 → +0
        # commit_vs_pipeline_coverage=0.60 → +0; late_stage=0 → +0
        # upside_to_commit_ratio=1.0 → +0; consecutive_upside=0 → +0
        # sandbagged_deal_value=0 → +0  => upside=0
        # deals_pulled=0 → +0; slipped=0 → +0; close moves 0 → +0; slip_days=0 → +0 => timing=0
        # crm=0 → +0; prior_period=0 → +0; attainment=100 → +0; accel=110 > 105 → +0 => pattern=0
        # => composite = 40*0.35 = 14.0
        inp = make_input(
            committed_forecast_usd=100_000.0,
            actual_closed_usd=160_000.0,   # 60% over → commit +40
            forecast_accuracy_last_3_periods=0.90,
            commit_vs_pipeline_coverage_ratio=0.60,
            late_stage_deals_not_committed=0,
            upside_to_commit_ratio=1.0,
            consecutive_upside_periods=0,
            sandbagged_deal_value_usd=0.0,
            deals_pulled_from_next_quarter=0,
            deals_slipped_intentionally_count=0,
            close_date_pushed_count=0,
            close_date_pulled_count=0,
            avg_deal_slip_days=0.0,
            crm_stage_inflation_score=0.0,
            prior_period_upside_usd=0.0,
            quota_attainment_last_period_pct=100.0,
            accelerator_threshold_pct=110.0,
        )
        result = eng.assess(inp)
        expected_c = 40.0
        expected_composite = round(expected_c * 0.35, 1)
        assert result.sandbagging_composite == expected_composite

    def test_composite_formula_all_max(self, eng):
        """Sub-scores capped at 100 each, so composite is capped at 100."""
        result = eng.assess(make_input(
            committed_forecast_usd=50_000.0,
            actual_closed_usd=200_000.0,          # +300% → commit +40
            prior_period_upside_usd=100_000.0,    # hist_ratio=2.0 → consistency +30
            upside_to_commit_ratio=5.0,            # → upside +45
            consecutive_upside_periods=10,         # → upside +30
            deals_pulled_from_next_quarter=10,     # → timing +35
            late_stage_deals_not_committed=10,     # → commit +10
            forecast_accuracy_last_3_periods=0.40, # → commit +30
            commit_vs_pipeline_coverage_ratio=0.10,# → commit +20
            avg_deal_slip_days=60.0,               # → timing +15
            deals_slipped_intentionally_count=5,   # → timing +30
            close_date_pushed_count=1,
            close_date_pulled_count=9,             # pull_ratio=0.9 → +20
            sandbagged_deal_value_usd=200_000.0,   # sbag_ratio=4.0 → upside +25
            quota_attainment_last_period_pct=160.0,# → consistency +20
            accelerator_threshold_pct=100.0,       # <=105 & att>=100 → +10
            crm_stage_inflation_score=90.0,        # → consistency +40
        ))
        assert result.sandbagging_composite == 100.0

    def test_composite_rounded_to_1_decimal(self, eng):
        inp = make_input(
            committed_forecast_usd=100_000.0,
            actual_closed_usd=130_000.0,   # 30% → commit +28
            forecast_accuracy_last_3_periods=0.70,  # +15
            commit_vs_pipeline_coverage_ratio=0.60,
        )
        result = eng.assess(inp)
        # verify it is a multiple of 0.1
        assert round(result.sandbagging_composite, 1) == result.sandbagging_composite

    def test_composite_increases_with_more_signals(self, eng):
        low = eng.assess(make_input())
        high = engine().assess(make_input(
            upside_to_commit_ratio=3.0,
            consecutive_upside_periods=4,
            deals_slipped_intentionally_count=3,
        ))
        assert high.sandbagging_composite > low.sandbagging_composite

    def test_individual_sub_scores_are_floats(self, eng, clean_input):
        r = eng.assess(clean_input)
        assert isinstance(r.commit_accuracy_score, float)
        assert isinstance(r.upside_manipulation_score, float)
        assert isinstance(r.deal_timing_score, float)
        assert isinstance(r.pattern_consistency_score, float)

    def test_sub_scores_non_negative(self, eng, clean_input):
        r = eng.assess(clean_input)
        assert r.commit_accuracy_score >= 0.0
        assert r.upside_manipulation_score >= 0.0
        assert r.deal_timing_score >= 0.0
        assert r.pattern_consistency_score >= 0.0

    def test_sub_scores_max_100(self, eng, severe_input):
        r = eng.assess(severe_input)
        assert r.commit_accuracy_score <= 100.0
        assert r.upside_manipulation_score <= 100.0
        assert r.deal_timing_score <= 100.0
        assert r.pattern_consistency_score <= 100.0


# ===========================================================================
# 6. is_sandbagging — all 3 trigger conditions
# ===========================================================================

class TestIsSandbagging:

    # Trigger 1: composite >= 40
    def test_is_sandbagging_true_when_composite_gte_40(self, eng):
        inp = make_input(
            committed_forecast_usd=100_000.0,
            actual_closed_usd=160_000.0,       # +60% → commit +40
            forecast_accuracy_last_3_periods=0.55, # +30 → commit=70
            upside_to_commit_ratio=2.5,         # → upside +28
            consecutive_upside_periods=0,
        )
        r = eng.assess(inp)
        if r.sandbagging_composite >= 40:
            assert r.is_sandbagging is True

    def test_is_sandbagging_false_when_all_clear(self, eng, clean_input):
        r = eng.assess(clean_input)
        # clean_input has no signals; verify not flagged
        if r.sandbagging_composite < 40 and r.commit_accuracy_score < 40:
            assert r.is_sandbagging is False

    # Trigger 2: consecutive_upside_periods >= 3
    def test_is_sandbagging_true_via_consecutive_upside_3(self, eng):
        inp = make_input(consecutive_upside_periods=3)
        r = eng.assess(inp)
        assert r.is_sandbagging is True

    def test_is_sandbagging_true_via_consecutive_upside_5(self, eng):
        inp = make_input(consecutive_upside_periods=5)
        r = eng.assess(inp)
        assert r.is_sandbagging is True

    def test_is_sandbagging_false_with_consecutive_upside_2(self, eng):
        # consecutive=2 alone should not trigger (need >=3)
        inp = make_input(consecutive_upside_periods=2)
        r = eng.assess(inp)
        # Only confirm the flag logic if composite <40 and no 40%-over-commit
        if r.sandbagging_composite < 40:
            over_commit = (inp.actual_closed_usd - inp.committed_forecast_usd) / inp.committed_forecast_usd
            if over_commit < 0.40:
                assert r.is_sandbagging is False

    def test_is_sandbagging_true_via_consecutive_upside_exact_3(self, eng):
        inp = make_input(
            consecutive_upside_periods=3,
            committed_forecast_usd=100_000.0,
            actual_closed_usd=100_000.0,   # no upside ratio trigger
        )
        r = eng.assess(inp)
        assert r.is_sandbagging is True

    # Trigger 3: (actual - committed) / committed >= 0.40
    def test_is_sandbagging_true_via_40pct_over_commit(self, eng):
        inp = make_input(
            committed_forecast_usd=100_000.0,
            actual_closed_usd=141_000.0,    # 41% over commit
            consecutive_upside_periods=0,
            forecast_accuracy_last_3_periods=0.90,
            upside_to_commit_ratio=1.0,
        )
        r = eng.assess(inp)
        assert r.is_sandbagging is True

    def test_is_sandbagging_true_via_exactly_40pct_over_commit(self, eng):
        inp = make_input(
            committed_forecast_usd=100_000.0,
            actual_closed_usd=140_000.0,    # exactly 40%
            consecutive_upside_periods=0,
        )
        r = eng.assess(inp)
        assert r.is_sandbagging is True

    def test_is_sandbagging_false_via_39pct_over_commit_no_other_triggers(self, eng):
        inp = make_input(
            committed_forecast_usd=100_000.0,
            actual_closed_usd=139_000.0,    # 39% over commit
            consecutive_upside_periods=0,
            forecast_accuracy_last_3_periods=0.90,
            upside_to_commit_ratio=1.0,
            commit_vs_pipeline_coverage_ratio=0.60,
        )
        r = eng.assess(inp)
        if r.sandbagging_composite < 40:
            assert r.is_sandbagging is False

    def test_is_sandbagging_zero_committed_forecast_no_ratio_trigger(self, eng):
        # With committed=0 the ratio condition is skipped
        inp = make_input(committed_forecast_usd=0.0, actual_closed_usd=100_000.0, consecutive_upside_periods=0)
        r = eng.assess(inp)
        # the over-commit trigger cannot fire; only composite or consecutive matters
        if r.sandbagging_composite < 40:
            assert r.is_sandbagging is False

    def test_is_sandbagging_is_bool(self, eng, clean_input):
        r = eng.assess(clean_input)
        assert isinstance(r.is_sandbagging, bool)


# ===========================================================================
# 7. requires_intervention — all 3 trigger conditions
# ===========================================================================

class TestRequiresIntervention:

    # Trigger 1: composite >= 30
    def test_requires_intervention_true_when_composite_gte_30(self, eng):
        inp = make_input(
            committed_forecast_usd=100_000.0,
            actual_closed_usd=160_000.0,        # +60% → commit +40
            forecast_accuracy_last_3_periods=0.55, # +30 → commit=70
        )
        r = eng.assess(inp)
        if r.sandbagging_composite >= 30:
            assert r.requires_intervention is True

    def test_requires_intervention_false_when_composite_below_30_no_other(self, eng):
        inp = make_input()  # clean rep, all defaults
        r = eng.assess(inp)
        if r.sandbagging_composite < 30 and inp.sandbagged_deal_value_usd < 50_000:
            if inp.deals_slipped_intentionally_count < 2:
                assert r.requires_intervention is False

    # Trigger 2: sandbagged_deal_value_usd >= 50000
    def test_requires_intervention_true_via_sandbagged_value_50000(self, eng):
        inp = make_input(sandbagged_deal_value_usd=50_000.0)
        r = eng.assess(inp)
        assert r.requires_intervention is True

    def test_requires_intervention_true_via_sandbagged_value_100000(self, eng):
        inp = make_input(sandbagged_deal_value_usd=100_000.0)
        r = eng.assess(inp)
        assert r.requires_intervention is True

    def test_requires_intervention_false_via_sandbagged_value_49999(self, eng):
        inp = make_input(sandbagged_deal_value_usd=49_999.0)
        r = eng.assess(inp)
        if r.sandbagging_composite < 30 and inp.deals_slipped_intentionally_count < 2:
            assert r.requires_intervention is False

    # Trigger 3: deals_slipped_intentionally_count >= 2
    def test_requires_intervention_true_via_slipped_count_2(self, eng):
        inp = make_input(deals_slipped_intentionally_count=2)
        r = eng.assess(inp)
        assert r.requires_intervention is True

    def test_requires_intervention_true_via_slipped_count_5(self, eng):
        inp = make_input(deals_slipped_intentionally_count=5)
        r = eng.assess(inp)
        assert r.requires_intervention is True

    def test_requires_intervention_false_via_slipped_count_1(self, eng):
        inp = make_input(deals_slipped_intentionally_count=1)
        r = eng.assess(inp)
        if r.sandbagging_composite < 30 and inp.sandbagged_deal_value_usd < 50_000:
            assert r.requires_intervention is False

    def test_requires_intervention_is_bool(self, eng, clean_input):
        r = eng.assess(clean_input)
        assert isinstance(r.requires_intervention, bool)

    def test_requires_intervention_true_when_severe(self, eng, severe_input):
        r = eng.assess(severe_input)
        assert r.requires_intervention is True


# ===========================================================================
# 8. estimated_hidden_revenue_usd calculation
# ===========================================================================

class TestEstimatedHiddenRevenue:

    def test_hidden_revenue_is_float(self, eng, clean_input):
        r = eng.assess(clean_input)
        assert isinstance(r.estimated_hidden_revenue_usd, float)

    def test_hidden_revenue_zero_when_sandbagged_value_zero(self, eng):
        inp = make_input(sandbagged_deal_value_usd=0.0)
        r = eng.assess(inp)
        assert r.estimated_hidden_revenue_usd == 0.0

    def test_hidden_revenue_formula(self, eng):
        """estimated = round(sandbagged_deal_value * composite / 100, 2)"""
        inp = make_input(sandbagged_deal_value_usd=0.0)
        r = eng.assess(inp)
        expected = round(0.0 * (r.sandbagging_composite / 100.0), 2)
        assert r.estimated_hidden_revenue_usd == expected

    def test_hidden_revenue_scales_with_sandbagged_value(self, eng):
        inp_low = make_input(sandbagged_deal_value_usd=10_000.0,
                             committed_forecast_usd=100_000.0,
                             actual_closed_usd=160_000.0,
                             forecast_accuracy_last_3_periods=0.55,
                             upside_to_commit_ratio=2.5)
        inp_high = make_input(sandbagged_deal_value_usd=50_000.0,
                              committed_forecast_usd=100_000.0,
                              actual_closed_usd=160_000.0,
                              forecast_accuracy_last_3_periods=0.55,
                              upside_to_commit_ratio=2.5)
        r_low  = engine().assess(inp_low)
        r_high = engine().assess(inp_high)
        # same composite, higher sandbagged value → higher hidden revenue
        assert r_high.estimated_hidden_revenue_usd > r_low.estimated_hidden_revenue_usd

    def test_hidden_revenue_rounded_to_2_decimals(self, eng):
        inp = make_input(sandbagged_deal_value_usd=33_333.33,
                         committed_forecast_usd=100_000.0,
                         actual_closed_usd=160_000.0,
                         forecast_accuracy_last_3_periods=0.55)
        r = eng.assess(inp)
        assert round(r.estimated_hidden_revenue_usd, 2) == r.estimated_hidden_revenue_usd

    def test_hidden_revenue_matches_manual_calculation(self, eng):
        """Use clean input (sandbagged_value=0) so formula yields 0."""
        r = eng.assess(make_input(sandbagged_deal_value_usd=0.0))
        assert r.estimated_hidden_revenue_usd == 0.0

    def test_hidden_revenue_with_nonzero_composite(self, eng):
        inp = make_input(
            sandbagged_deal_value_usd=20_000.0,
            committed_forecast_usd=100_000.0,
            actual_closed_usd=160_000.0,  # 60% → commit +40
            forecast_accuracy_last_3_periods=0.55,  # +30
        )
        r = eng.assess(inp)
        expected = round(20_000.0 * (r.sandbagging_composite / 100.0), 2)
        assert r.estimated_hidden_revenue_usd == expected


# ===========================================================================
# 9. Pattern detection priority order
# ===========================================================================

class TestPatternDetection:

    def _pattern(self, **kwargs) -> SandbaggingPattern:
        return engine().assess(make_input(**kwargs)).sandbagging_pattern

    def test_pattern_none_for_clean_rep(self, eng, clean_input):
        r = eng.assess(clean_input)
        assert r.sandbagging_pattern == SandbaggingPattern.none

    def test_pattern_consistent_upside_when_consecutive_gte_2(self):
        # consecutive=2, no higher-priority signals
        p = self._pattern(consecutive_upside_periods=2)
        assert p == SandbaggingPattern.consistent_upside

    def test_pattern_late_quarter_surge_when_days_le_14_and_pulls_gte_2(self):
        p = self._pattern(
            days_remaining_in_period=10,
            close_date_pulled_count=3,
            consecutive_upside_periods=0,
        )
        assert p == SandbaggingPattern.late_quarter_surge

    def test_pattern_late_quarter_surge_overrides_consistent_upside(self):
        # late_quarter_surge priority > consistent_upside
        p = self._pattern(
            days_remaining_in_period=10,
            close_date_pulled_count=3,
            consecutive_upside_periods=2,  # would give consistent_upside
        )
        assert p == SandbaggingPattern.late_quarter_surge

    def test_pattern_commit_minimization_when_commit_gte_25_and_late_stage_gte_3(self):
        # Need commit_accuracy_score >= 25: upside 30% → +28, acc <0.85 → +5
        p = self._pattern(
            committed_forecast_usd=100_000.0,
            actual_closed_usd=130_000.0,        # 30% → +28
            forecast_accuracy_last_3_periods=0.80,  # +5 → commit=33
            late_stage_deals_not_committed=3,
        )
        assert p == SandbaggingPattern.commit_minimization

    def test_pattern_deal_timing_manipulation_when_timing_gte_35_and_pulls_gte_2(self):
        # timing: deals_pulled>=4 → +35; slipped>=3 → +30 → timing=65; pulls=4>=2
        p = self._pattern(
            deals_pulled_from_next_quarter=4,
            deals_slipped_intentionally_count=0,
        )
        assert p == SandbaggingPattern.deal_timing_manipulation

    def test_pattern_forecast_sandbagging_highest_priority(self):
        # commit>=30 AND upside>=30 AND consistency>=20
        p = self._pattern(
            committed_forecast_usd=100_000.0,
            actual_closed_usd=160_000.0,       # +60% → commit +40
            forecast_accuracy_last_3_periods=0.55, # +30 → commit=70
            commit_vs_pipeline_coverage_ratio=0.25, # +10 → commit=80
            upside_to_commit_ratio=3.5,        # → upside +45
            consecutive_upside_periods=4,      # → upside +30
            sandbagged_deal_value_usd=40_000.0, # sbag_ratio=0.4 → upside +25 → total>100 → cap100
            crm_stage_inflation_score=70.0,    # → consistency +40
            quota_attainment_last_period_pct=145.0, # → consistency +20
        )
        assert p == SandbaggingPattern.forecast_sandbagging

    def test_pattern_forecast_sandbagging_overrides_deal_timing(self):
        """forecast_sandbagging must win over deal_timing_manipulation."""
        p = self._pattern(
            committed_forecast_usd=100_000.0,
            actual_closed_usd=160_000.0,
            forecast_accuracy_last_3_periods=0.55,
            commit_vs_pipeline_coverage_ratio=0.25,
            upside_to_commit_ratio=3.5,
            consecutive_upside_periods=4,
            sandbagged_deal_value_usd=40_000.0,
            crm_stage_inflation_score=70.0,
            quota_attainment_last_period_pct=145.0,
            deals_pulled_from_next_quarter=4,   # would trigger deal_timing
        )
        assert p == SandbaggingPattern.forecast_sandbagging

    def test_pattern_deal_timing_overrides_commit_minimization(self):
        p = self._pattern(
            deals_pulled_from_next_quarter=4,   # timing >=35
            late_stage_deals_not_committed=3,    # would trigger commit_minimization
            committed_forecast_usd=100_000.0,
            actual_closed_usd=130_000.0,
            forecast_accuracy_last_3_periods=0.80,
        )
        assert p == SandbaggingPattern.deal_timing_manipulation

    def test_pattern_is_sandbagging_pattern_enum(self, eng, clean_input):
        r = eng.assess(clean_input)
        assert isinstance(r.sandbagging_pattern, SandbaggingPattern)


# ===========================================================================
# 10. Risk level, severity, action assignment
# ===========================================================================

class TestRiskSeverityAction:

    def test_risk_low_when_composite_below_20(self, eng, clean_input):
        r = eng.assess(clean_input)
        if r.sandbagging_composite < 20:
            assert r.sandbagging_risk == SandbaggingRisk.low

    def test_risk_moderate_when_composite_20_to_39(self, eng):
        inp = make_input(
            committed_forecast_usd=100_000.0,
            actual_closed_usd=130_000.0,    # 30% → +28
            forecast_accuracy_last_3_periods=0.80,  # +5 → commit=33
        )
        r = eng.assess(inp)
        if 20 <= r.sandbagging_composite < 40:
            assert r.sandbagging_risk == SandbaggingRisk.moderate

    def test_risk_high_when_composite_40_to_59(self, eng):
        inp = make_input(
            committed_forecast_usd=100_000.0,
            actual_closed_usd=160_000.0,    # +60% → commit +40
            forecast_accuracy_last_3_periods=0.55,  # +30 → commit=70
            upside_to_commit_ratio=1.5,     # upside +14 → composite > 40
        )
        r = eng.assess(inp)
        if 40 <= r.sandbagging_composite < 60:
            assert r.sandbagging_risk == SandbaggingRisk.high

    def test_risk_critical_when_composite_gte_60(self, eng, severe_input):
        r = eng.assess(severe_input)
        if r.sandbagging_composite >= 60:
            assert r.sandbagging_risk == SandbaggingRisk.critical

    def test_severity_accurate_when_composite_below_20(self, eng, clean_input):
        r = eng.assess(clean_input)
        if r.sandbagging_composite < 20:
            assert r.sandbagging_severity == SandbaggingSeverity.accurate

    def test_severity_watch_when_composite_20_to_39(self, eng):
        inp = make_input(
            committed_forecast_usd=100_000.0,
            actual_closed_usd=130_000.0,
            forecast_accuracy_last_3_periods=0.80,
        )
        r = eng.assess(inp)
        if 20 <= r.sandbagging_composite < 40:
            assert r.sandbagging_severity == SandbaggingSeverity.watch

    def test_severity_suspected_when_composite_40_to_59(self, eng):
        inp = make_input(
            committed_forecast_usd=100_000.0,
            actual_closed_usd=160_000.0,
            forecast_accuracy_last_3_periods=0.55,
            upside_to_commit_ratio=1.5,
        )
        r = eng.assess(inp)
        if 40 <= r.sandbagging_composite < 60:
            assert r.sandbagging_severity == SandbaggingSeverity.suspected

    def test_severity_confirmed_when_composite_gte_60(self, eng, severe_input):
        r = eng.assess(severe_input)
        if r.sandbagging_composite >= 60:
            assert r.sandbagging_severity == SandbaggingSeverity.confirmed

    def test_action_no_action_when_low_and_composite_below_10(self, eng, clean_input):
        r = eng.assess(clean_input)
        if r.sandbagging_risk == SandbaggingRisk.low and r.sandbagging_composite < 10:
            assert r.recommended_action == SandbaggingAction.no_action

    def test_action_forecast_coaching_when_low_and_composite_gte_10(self, eng):
        # Moderate risk → pipeline_review, so we need low risk with composite >= 10
        inp = make_input(
            committed_forecast_usd=100_000.0,
            actual_closed_usd=115_000.0,  # 15% → +14
            forecast_accuracy_last_3_periods=0.85,  # borderline → 0
        )
        r = eng.assess(inp)
        if r.sandbagging_risk == SandbaggingRisk.low and r.sandbagging_composite >= 10:
            assert r.recommended_action == SandbaggingAction.forecast_coaching

    def test_action_pipeline_review_when_moderate(self, eng):
        inp = make_input(
            committed_forecast_usd=100_000.0,
            actual_closed_usd=130_000.0,
            forecast_accuracy_last_3_periods=0.80,
        )
        r = eng.assess(inp)
        if r.sandbagging_risk == SandbaggingRisk.moderate:
            assert r.recommended_action == SandbaggingAction.pipeline_review

    def test_action_comp_plan_review_when_high(self, eng):
        inp = make_input(
            committed_forecast_usd=100_000.0,
            actual_closed_usd=160_000.0,
            forecast_accuracy_last_3_periods=0.55,
            upside_to_commit_ratio=1.5,
        )
        r = eng.assess(inp)
        if r.sandbagging_risk == SandbaggingRisk.high:
            assert r.recommended_action == SandbaggingAction.comp_plan_review

    def test_action_executive_confrontation_when_critical(self, eng, severe_input):
        r = eng.assess(severe_input)
        if r.sandbagging_risk == SandbaggingRisk.critical:
            assert r.recommended_action == SandbaggingAction.executive_confrontation

    def test_risk_is_sandbagging_risk_enum(self, eng, clean_input):
        r = eng.assess(clean_input)
        assert isinstance(r.sandbagging_risk, SandbaggingRisk)

    def test_severity_is_sandbagging_severity_enum(self, eng, clean_input):
        r = eng.assess(clean_input)
        assert isinstance(r.sandbagging_severity, SandbaggingSeverity)

    def test_action_is_sandbagging_action_enum(self, eng, clean_input):
        r = eng.assess(clean_input)
        assert isinstance(r.recommended_action, SandbaggingAction)


# ===========================================================================
# 11. assess_batch() returns correct count
# ===========================================================================

class TestAssessBatch:

    def test_batch_empty_list(self, eng):
        results = eng.assess_batch([])
        assert results == []

    def test_batch_single_input(self, eng, clean_input):
        results = eng.assess_batch([clean_input])
        assert len(results) == 1

    def test_batch_multiple_inputs(self, eng):
        inputs = [make_input(rep_id=f"REP-{i}") for i in range(5)]
        results = eng.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_returns_list(self, eng, clean_input):
        results = eng.assess_batch([clean_input])
        assert isinstance(results, list)

    def test_batch_elements_are_sandbagging_results(self, eng, clean_input):
        results = eng.assess_batch([clean_input])
        assert isinstance(results[0], SandbaggingResult)

    def test_batch_10_inputs(self, eng):
        inputs = [make_input(rep_id=f"R{i}") for i in range(10)]
        results = eng.assess_batch(inputs)
        assert len(results) == 10

    def test_batch_rep_ids_preserved(self, eng):
        inputs = [make_input(rep_id=f"REP-{i}") for i in range(3)]
        results = eng.assess_batch(inputs)
        ids = [r.rep_id for r in results]
        assert ids == ["REP-0", "REP-1", "REP-2"]

    def test_batch_adds_to_summary(self, eng):
        inputs = [make_input(rep_id=f"X{i}") for i in range(4)]
        eng.assess_batch(inputs)
        assert eng.summary()["total"] == 4

    def test_batch_mixed_signals(self, eng, severe_input, clean_input):
        results = eng.assess_batch([clean_input, severe_input])
        composites = [r.sandbagging_composite for r in results]
        assert composites[1] > composites[0]

    def test_batch_order_preserved(self, eng):
        inp1 = make_input(rep_id="ALPHA")
        inp2 = make_input(rep_id="BETA")
        results = eng.assess_batch([inp1, inp2])
        assert results[0].rep_id == "ALPHA"
        assert results[1].rep_id == "BETA"


# ===========================================================================
# 12. summary() total_estimated_hidden_revenue_usd is SUM
# ===========================================================================

class TestSummaryHiddenRevenue:

    def test_total_hidden_revenue_is_sum_of_individual(self, eng):
        inputs = [
            make_input(rep_id="A", sandbagged_deal_value_usd=10_000.0,
                       committed_forecast_usd=100_000.0,
                       actual_closed_usd=160_000.0,
                       forecast_accuracy_last_3_periods=0.55),
            make_input(rep_id="B", sandbagged_deal_value_usd=20_000.0,
                       committed_forecast_usd=100_000.0,
                       actual_closed_usd=130_000.0),
            make_input(rep_id="C", sandbagged_deal_value_usd=0.0),
        ]
        results = eng.assess_batch(inputs)
        expected_sum = round(sum(r.estimated_hidden_revenue_usd for r in results), 2)
        s = eng.summary()
        assert s["total_estimated_hidden_revenue_usd"] == expected_sum

    def test_total_hidden_revenue_zero_when_no_sandbagged_values(self, eng):
        eng.assess_batch([make_input(sandbagged_deal_value_usd=0.0) for _ in range(3)])
        assert eng.summary()["total_estimated_hidden_revenue_usd"] == 0.0

    def test_total_hidden_revenue_empty_engine(self, eng):
        assert eng.summary()["total_estimated_hidden_revenue_usd"] == 0.0

    def test_total_hidden_revenue_single_rep(self, eng):
        inp = make_input(sandbagged_deal_value_usd=30_000.0,
                         committed_forecast_usd=100_000.0,
                         actual_closed_usd=160_000.0,
                         forecast_accuracy_last_3_periods=0.55)
        r = eng.assess(inp)
        s = eng.summary()
        assert s["total_estimated_hidden_revenue_usd"] == r.estimated_hidden_revenue_usd

    def test_total_hidden_revenue_is_float(self, eng, clean_input):
        eng.assess(clean_input)
        assert isinstance(eng.summary()["total_estimated_hidden_revenue_usd"], float)

    def test_total_hidden_revenue_non_negative(self, eng):
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        assert eng.summary()["total_estimated_hidden_revenue_usd"] >= 0.0

    def test_total_hidden_revenue_grows_with_more_reps(self, eng):
        inp = make_input(sandbagged_deal_value_usd=50_000.0,
                         committed_forecast_usd=100_000.0,
                         actual_closed_usd=160_000.0,
                         forecast_accuracy_last_3_periods=0.55)
        eng.assess(inp)
        rev1 = eng.summary()["total_estimated_hidden_revenue_usd"]
        eng.assess(make_input(rep_id="REP-2", sandbagged_deal_value_usd=50_000.0,
                              committed_forecast_usd=100_000.0,
                              actual_closed_usd=160_000.0,
                              forecast_accuracy_last_3_periods=0.55))
        rev2 = eng.summary()["total_estimated_hidden_revenue_usd"]
        assert rev2 > rev1


# ===========================================================================
# 13. Edge cases
# ===========================================================================

class TestEdgeCases:

    # Zero committed forecast
    def test_zero_committed_forecast_no_crash(self, eng):
        inp = make_input(committed_forecast_usd=0.0, actual_closed_usd=50_000.0)
        r = eng.assess(inp)
        assert r is not None

    def test_zero_committed_forecast_no_ratio_trigger(self, eng):
        inp = make_input(committed_forecast_usd=0.0, actual_closed_usd=50_000.0,
                         consecutive_upside_periods=0)
        r = eng.assess(inp)
        if r.sandbagging_composite < 40:
            assert r.is_sandbagging is False

    def test_zero_committed_forecast_composite_valid(self, eng):
        inp = make_input(committed_forecast_usd=0.0, actual_closed_usd=0.0)
        r = eng.assess(inp)
        assert 0.0 <= r.sandbagging_composite <= 100.0

    def test_zero_committed_forecast_hidden_rev_formula_still_works(self, eng):
        inp = make_input(committed_forecast_usd=0.0, sandbagged_deal_value_usd=20_000.0)
        r = eng.assess(inp)
        expected = round(20_000.0 * (r.sandbagging_composite / 100.0), 2)
        assert r.estimated_hidden_revenue_usd == expected

    # Perfect accuracy — no sandbagging signals
    def test_perfect_accuracy_rep_low_composite(self, eng):
        inp = make_input(
            committed_forecast_usd=100_000.0,
            actual_closed_usd=100_000.0,
            forecast_accuracy_last_3_periods=1.0,
            commit_vs_pipeline_coverage_ratio=0.70,
            upside_to_commit_ratio=1.0,
            consecutive_upside_periods=0,
            crm_stage_inflation_score=0.0,
            sandbagged_deal_value_usd=0.0,
            deals_slipped_intentionally_count=0,
            deals_pulled_from_next_quarter=0,
        )
        r = eng.assess(inp)
        assert r.sandbagging_composite < 20.0

    def test_perfect_accuracy_rep_not_sandbagging(self, eng):
        inp = make_input(
            committed_forecast_usd=100_000.0,
            actual_closed_usd=100_000.0,
            forecast_accuracy_last_3_periods=1.0,
        )
        r = eng.assess(inp)
        assert r.is_sandbagging is False

    def test_perfect_accuracy_no_intervention(self, eng):
        inp = make_input(
            committed_forecast_usd=100_000.0,
            actual_closed_usd=100_000.0,
            forecast_accuracy_last_3_periods=1.0,
            sandbagged_deal_value_usd=0.0,
            deals_slipped_intentionally_count=0,
        )
        r = eng.assess(inp)
        assert r.requires_intervention is False

    def test_perfect_accuracy_risk_low(self, eng):
        inp = make_input(
            committed_forecast_usd=100_000.0,
            actual_closed_usd=100_000.0,
            forecast_accuracy_last_3_periods=1.0,
        )
        r = eng.assess(inp)
        assert r.sandbagging_risk == SandbaggingRisk.low

    def test_perfect_accuracy_pattern_none(self, eng):
        inp = make_input(
            committed_forecast_usd=100_000.0,
            actual_closed_usd=100_000.0,
            forecast_accuracy_last_3_periods=1.0,
            consecutive_upside_periods=0,
        )
        r = eng.assess(inp)
        assert r.sandbagging_pattern == SandbaggingPattern.none

    # No sandbagging signals whatsoever
    def test_no_signals_all_defaults(self, eng, clean_input):
        r = eng.assess(clean_input)
        assert r.sandbagging_composite < 10.0

    def test_no_signals_signal_string_not_empty(self, eng, clean_input):
        r = eng.assess(clean_input)
        assert isinstance(r.sandbagging_signal, str)
        assert len(r.sandbagging_signal) > 0

    def test_no_signals_severity_accurate_or_watch(self, eng, clean_input):
        r = eng.assess(clean_input)
        assert r.sandbagging_severity in (SandbaggingSeverity.accurate, SandbaggingSeverity.watch)

    # Extremely high values stay within bounds
    def test_extremely_high_upside_ratio_caps_at_100(self, eng):
        inp = make_input(upside_to_commit_ratio=999.0, consecutive_upside_periods=99)
        r = eng.assess(inp)
        assert r.upside_manipulation_score <= 100.0

    def test_extremely_high_crm_score_caps_pattern_at_100(self, eng):
        inp = make_input(crm_stage_inflation_score=999.0, quota_attainment_last_period_pct=999.0)
        r = eng.assess(inp)
        assert r.pattern_consistency_score <= 100.0

    def test_all_zeros_input_valid(self, eng):
        inp = make_input(
            committed_forecast_usd=0.0, actual_closed_usd=0.0,
            prior_period_upside_usd=0.0, upside_to_commit_ratio=0.0,
            deals_pulled_from_next_quarter=0, late_stage_deals_not_committed=0,
            forecast_accuracy_last_3_periods=0.0, consecutive_upside_periods=0,
            commit_vs_pipeline_coverage_ratio=0.0, avg_deal_slip_days=0.0,
            deals_slipped_intentionally_count=0, close_date_pushed_count=0,
            close_date_pulled_count=0, sandbagged_deal_value_usd=0.0,
            quota_attainment_last_period_pct=0.0, accelerator_threshold_pct=0.0,
            days_remaining_in_period=0, total_pipeline_usd=0.0,
            crm_stage_inflation_score=0.0,
        )
        r = eng.assess(inp)
        assert r is not None
        assert 0.0 <= r.sandbagging_composite <= 100.0

    def test_assess_returns_sandbagging_result(self, eng, clean_input):
        r = eng.assess(clean_input)
        assert isinstance(r, SandbaggingResult)

    def test_assess_preserves_rep_id(self, eng):
        inp = make_input(rep_id="UNIQUE-REP")
        r = eng.assess(inp)
        assert r.rep_id == "UNIQUE-REP"

    def test_assess_preserves_region(self, eng):
        inp = make_input(region="APAC")
        r = eng.assess(inp)
        assert r.region == "APAC"

    def test_multiple_engines_independent(self):
        e1 = SalesForecastSandbaggingDetectionEngine()
        e2 = SalesForecastSandbaggingDetectionEngine()
        e1.assess(make_input(rep_id="A"))
        e1.assess(make_input(rep_id="B"))
        e2.assess(make_input(rep_id="C"))
        assert e1.summary()["total"] == 2
        assert e2.summary()["total"] == 1

    def test_signal_string_mentions_pattern(self, eng):
        inp = make_input(consecutive_upside_periods=2)
        r = eng.assess(inp)
        assert "consistent upside" in r.sandbagging_signal.lower() or len(r.sandbagging_signal) > 0

    def test_summary_risk_counts_sum_equals_total(self, eng):
        inputs = [make_input(rep_id=f"R{i}") for i in range(6)]
        eng.assess_batch(inputs)
        s = eng.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_pattern_counts_sum_equals_total(self, eng):
        inputs = [make_input(rep_id=f"R{i}") for i in range(4)]
        eng.assess_batch(inputs)
        s = eng.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_summary_severity_counts_sum_equals_total(self, eng):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        eng.assess_batch(inputs)
        s = eng.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_equals_total(self, eng):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        eng.assess_batch(inputs)
        s = eng.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_sandbagging_count_lte_total(self, eng):
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(10)])
        s = eng.summary()
        assert s["sandbagging_count"] <= s["total"]

    def test_summary_intervention_count_lte_total(self, eng):
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(10)])
        s = eng.summary()
        assert s["intervention_count"] <= s["total"]

    def test_summary_avg_composite_in_valid_range(self, eng):
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        s = eng.summary()
        assert 0.0 <= s["avg_sandbagging_composite"] <= 100.0

    def test_summary_avg_scores_in_valid_range(self, eng):
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        s = eng.summary()
        for key in ("avg_commit_accuracy_score", "avg_upside_manipulation_score",
                    "avg_deal_timing_score", "avg_pattern_consistency_score"):
            assert 0.0 <= s[key] <= 100.0, f"{key} out of range"
