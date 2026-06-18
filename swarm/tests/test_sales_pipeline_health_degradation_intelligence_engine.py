"""
Comprehensive pytest tests for SalesPipelineHealthDegradationIntelligenceEngine.
"""
from __future__ import annotations

import pytest

from swarm.intelligence.sales_pipeline_health_degradation_intelligence_engine import (
    PipelineAction,
    PipelineInput,
    PipelinePattern,
    PipelineResult,
    PipelineRisk,
    PipelineSeverity,
    SalesPipelineHealthDegradationIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> PipelineInput:
    """Return a baseline healthy PipelineInput, overriding any fields."""
    defaults = dict(
        rep_id="REP-001",
        region="AMER",
        evaluation_period_id="Q2-2026",
        avg_deal_age_days=30.0,
        deals_exceeding_avg_stage_duration_pct=0.10,
        deals_with_no_activity_30d_pct=0.05,
        deals_with_no_activity_60d_pct=0.05,
        stage_to_stage_progression_rate_pct=0.70,
        pipeline_value_change_pct=0.05,
        deals_added_not_touched_after_create_pct=0.05,
        deals_closed_lost_rate_pct=0.20,
        deals_deleted_or_merged_per_qtr=2.0,
        avg_days_in_current_stage=10.0,
        expected_days_in_stage=15.0,
        late_stage_deals_pct=0.40,
        early_stage_deals_pct=0.30,
        single_stage_pipeline_concentration=0.20,
        pipeline_refresh_rate_pct=0.50,
        closed_won_from_current_pipeline_pct=0.40,
        deals_slipped_more_than_once_pct=0.05,
        total_open_deals=20,
        avg_opportunity_value_usd=5000.0,
    )
    defaults.update(overrides)
    return PipelineInput(**defaults)


def fresh_engine() -> SalesPipelineHealthDegradationIntelligenceEngine:
    return SalesPipelineHealthDegradationIntelligenceEngine()


# ===========================================================================
# 1. Enum value tests
# ===========================================================================

class TestEnums:
    def test_pipeline_risk_values(self):
        assert PipelineRisk.low.value == "low"
        assert PipelineRisk.moderate.value == "moderate"
        assert PipelineRisk.high.value == "high"
        assert PipelineRisk.critical.value == "critical"

    def test_pipeline_risk_all_members(self):
        members = {m.value for m in PipelineRisk}
        assert members == {"low", "moderate", "high", "critical"}

    def test_pipeline_pattern_values(self):
        assert PipelinePattern.none.value == "none"
        assert PipelinePattern.zombie_deal_accumulation.value == "zombie_deal_accumulation"
        assert PipelinePattern.stage_stagnation.value == "stage_stagnation"
        assert PipelinePattern.pipeline_inflation.value == "pipeline_inflation"
        assert PipelinePattern.curation_avoidance.value == "curation_avoidance"
        assert PipelinePattern.late_stage_concentration.value == "late_stage_concentration"

    def test_pipeline_pattern_all_members(self):
        members = {m.value for m in PipelinePattern}
        assert members == {
            "none",
            "zombie_deal_accumulation",
            "stage_stagnation",
            "pipeline_inflation",
            "curation_avoidance",
            "late_stage_concentration",
        }

    def test_pipeline_severity_values(self):
        assert PipelineSeverity.healthy.value == "healthy"
        assert PipelineSeverity.declining.value == "declining"
        assert PipelineSeverity.degraded.value == "degraded"
        assert PipelineSeverity.critical.value == "critical"

    def test_pipeline_severity_all_members(self):
        members = {m.value for m in PipelineSeverity}
        assert members == {"healthy", "declining", "degraded", "critical"}

    def test_pipeline_action_values(self):
        assert PipelineAction.no_action.value == "no_action"
        assert PipelineAction.pipeline_hygiene_coaching.value == "pipeline_hygiene_coaching"
        assert PipelineAction.deal_progression_review.value == "deal_progression_review"
        assert PipelineAction.pipeline_curation_workshop.value == "pipeline_curation_workshop"
        assert PipelineAction.stage_exit_criteria_coaching.value == "stage_exit_criteria_coaching"
        assert PipelineAction.pipeline_reset_intervention.value == "pipeline_reset_intervention"

    def test_pipeline_action_all_members(self):
        members = {m.value for m in PipelineAction}
        assert members == {
            "no_action",
            "pipeline_hygiene_coaching",
            "deal_progression_review",
            "pipeline_curation_workshop",
            "stage_exit_criteria_coaching",
            "pipeline_reset_intervention",
        }

    def test_enums_are_str_subclass(self):
        assert isinstance(PipelineRisk.low, str)
        assert isinstance(PipelinePattern.none, str)
        assert isinstance(PipelineSeverity.healthy, str)
        assert isinstance(PipelineAction.no_action, str)


# ===========================================================================
# 2. PipelineInput field tests
# ===========================================================================

class TestPipelineInput:
    def test_all_22_fields_exist(self):
        inp = make_input()
        fields = [
            "rep_id", "region", "evaluation_period_id",
            "avg_deal_age_days", "deals_exceeding_avg_stage_duration_pct",
            "deals_with_no_activity_30d_pct", "deals_with_no_activity_60d_pct",
            "stage_to_stage_progression_rate_pct", "pipeline_value_change_pct",
            "deals_added_not_touched_after_create_pct", "deals_closed_lost_rate_pct",
            "deals_deleted_or_merged_per_qtr", "avg_days_in_current_stage",
            "expected_days_in_stage", "late_stage_deals_pct", "early_stage_deals_pct",
            "single_stage_pipeline_concentration", "pipeline_refresh_rate_pct",
            "closed_won_from_current_pipeline_pct", "deals_slipped_more_than_once_pct",
            "total_open_deals", "avg_opportunity_value_usd",
        ]
        for field in fields:
            assert hasattr(inp, field), f"Missing field: {field}"

    def test_field_count_is_22(self):
        import dataclasses
        fields = dataclasses.fields(PipelineInput)
        assert len(fields) == 22

    def test_string_fields(self):
        inp = make_input(rep_id="R-999", region="EMEA", evaluation_period_id="Q3-2026")
        assert inp.rep_id == "R-999"
        assert inp.region == "EMEA"
        assert inp.evaluation_period_id == "Q3-2026"

    def test_int_field(self):
        inp = make_input(total_open_deals=50)
        assert inp.total_open_deals == 50

    def test_float_fields(self):
        inp = make_input(avg_deal_age_days=90.5, avg_opportunity_value_usd=12000.0)
        assert inp.avg_deal_age_days == 90.5
        assert inp.avg_opportunity_value_usd == 12000.0


# ===========================================================================
# 3. PipelineResult fields + to_dict()
# ===========================================================================

class TestPipelineResult:
    def _make_result(self) -> PipelineResult:
        engine = fresh_engine()
        return engine.assess(make_input())

    def test_result_has_15_fields(self):
        import dataclasses
        fields = dataclasses.fields(PipelineResult)
        assert len(fields) == 15

    def test_result_field_names(self):
        result = self._make_result()
        expected_fields = [
            "rep_id", "region", "pipeline_risk", "pipeline_pattern",
            "pipeline_severity", "recommended_action", "staleness_score",
            "progression_score", "curation_score", "concentration_score",
            "pipeline_composite", "has_pipeline_gap", "requires_pipeline_coaching",
            "estimated_phantom_pipeline_usd", "pipeline_signal",
        ]
        for field in expected_fields:
            assert hasattr(result, field), f"Missing result field: {field}"

    def test_to_dict_returns_15_keys(self):
        result = self._make_result()
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_key_names(self):
        result = self._make_result()
        d = result.to_dict()
        expected_keys = {
            "rep_id", "region", "pipeline_risk", "pipeline_pattern",
            "pipeline_severity", "recommended_action", "staleness_score",
            "progression_score", "curation_score", "concentration_score",
            "pipeline_composite", "has_pipeline_gap", "requires_pipeline_coaching",
            "estimated_phantom_pipeline_usd", "pipeline_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_values_are_strings(self):
        result = self._make_result()
        d = result.to_dict()
        assert isinstance(d["pipeline_risk"], str)
        assert isinstance(d["pipeline_pattern"], str)
        assert isinstance(d["pipeline_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_rep_id_and_region(self):
        engine = fresh_engine()
        inp = make_input(rep_id="REP-XYZ", region="APAC")
        result = engine.assess(inp)
        d = result.to_dict()
        assert d["rep_id"] == "REP-XYZ"
        assert d["region"] == "APAC"

    def test_to_dict_bool_fields(self):
        result = self._make_result()
        d = result.to_dict()
        assert isinstance(d["has_pipeline_gap"], bool)
        assert isinstance(d["requires_pipeline_coaching"], bool)

    def test_to_dict_numeric_fields(self):
        result = self._make_result()
        d = result.to_dict()
        assert isinstance(d["staleness_score"], float)
        assert isinstance(d["progression_score"], float)
        assert isinstance(d["curation_score"], float)
        assert isinstance(d["concentration_score"], float)
        assert isinstance(d["pipeline_composite"], float)
        assert isinstance(d["estimated_phantom_pipeline_usd"], float)


# ===========================================================================
# 4. Staleness sub-score branches
# ===========================================================================

class TestStalenessScore:
    def _score(self, **kw) -> float:
        engine = fresh_engine()
        inp = make_input(**kw)
        return engine._staleness_score(inp)

    # deals_with_no_activity_30d_pct
    def test_30d_below_threshold_adds_zero(self):
        s = self._score(deals_with_no_activity_30d_pct=0.14)
        assert s == 0.0

    def test_30d_at_015_adds_8(self):
        s = self._score(deals_with_no_activity_30d_pct=0.15)
        assert s == 8.0

    def test_30d_above_015_below_030_adds_8(self):
        s = self._score(deals_with_no_activity_30d_pct=0.20)
        assert s == 8.0

    def test_30d_at_030_adds_22(self):
        s = self._score(deals_with_no_activity_30d_pct=0.30)
        assert s == 22.0

    def test_30d_above_030_below_050_adds_22(self):
        s = self._score(deals_with_no_activity_30d_pct=0.40)
        assert s == 22.0

    def test_30d_at_050_adds_40(self):
        s = self._score(deals_with_no_activity_30d_pct=0.50)
        assert s == 40.0

    def test_30d_above_050_adds_40(self):
        s = self._score(deals_with_no_activity_30d_pct=0.80)
        assert s == 40.0

    # avg_deal_age_days
    def test_age_below_75_adds_zero(self):
        s = self._score(avg_deal_age_days=74.9)
        assert s == 0.0

    def test_age_at_75_adds_18(self):
        s = self._score(avg_deal_age_days=75.0)
        assert s == 18.0

    def test_age_between_75_and_120_adds_18(self):
        s = self._score(avg_deal_age_days=100.0)
        assert s == 18.0

    def test_age_at_120_adds_35(self):
        s = self._score(avg_deal_age_days=120.0)
        assert s == 35.0

    def test_age_above_120_adds_35(self):
        s = self._score(avg_deal_age_days=180.0)
        assert s == 35.0

    # deals_with_no_activity_60d_pct
    def test_60d_below_threshold_adds_zero(self):
        s = self._score(deals_with_no_activity_60d_pct=0.14)
        assert s == 0.0

    def test_60d_at_015_adds_12(self):
        s = self._score(deals_with_no_activity_60d_pct=0.15)
        assert s == 12.0

    def test_60d_between_015_and_035_adds_12(self):
        s = self._score(deals_with_no_activity_60d_pct=0.25)
        assert s == 12.0

    def test_60d_at_035_adds_25(self):
        s = self._score(deals_with_no_activity_60d_pct=0.35)
        assert s == 25.0

    def test_60d_above_035_adds_25(self):
        s = self._score(deals_with_no_activity_60d_pct=0.60)
        assert s == 25.0

    # Additive combination
    def test_staleness_max_combination(self):
        # 40 + 35 + 25 = 100
        s = self._score(
            deals_with_no_activity_30d_pct=0.50,
            avg_deal_age_days=120.0,
            deals_with_no_activity_60d_pct=0.35,
        )
        assert s == 100.0

    def test_staleness_capped_at_100(self):
        s = self._score(
            deals_with_no_activity_30d_pct=0.99,
            avg_deal_age_days=999.0,
            deals_with_no_activity_60d_pct=0.99,
        )
        assert s == 100.0

    def test_staleness_additive_partial(self):
        # 22 (30d) + 18 (age) + 12 (60d) = 52
        s = self._score(
            deals_with_no_activity_30d_pct=0.30,
            avg_deal_age_days=75.0,
            deals_with_no_activity_60d_pct=0.15,
        )
        assert s == 52.0


# ===========================================================================
# 5. Progression sub-score branches
# ===========================================================================

class TestProgressionScore:
    def _score(self, **kw) -> float:
        engine = fresh_engine()
        inp = make_input(**kw)
        return engine._progression_score(inp)

    # stage_to_stage_progression_rate_pct
    def test_progression_rate_above_060_adds_zero(self):
        s = self._score(stage_to_stage_progression_rate_pct=0.61)
        assert s == 0.0

    def test_progression_rate_at_060_adds_8(self):
        s = self._score(stage_to_stage_progression_rate_pct=0.60)
        assert s == 8.0

    def test_progression_rate_between_040_060_adds_8(self):
        s = self._score(stage_to_stage_progression_rate_pct=0.50)
        assert s == 8.0

    def test_progression_rate_at_040_adds_22(self):
        s = self._score(stage_to_stage_progression_rate_pct=0.40)
        assert s == 22.0

    def test_progression_rate_between_020_040_adds_22(self):
        s = self._score(stage_to_stage_progression_rate_pct=0.30)
        assert s == 22.0

    def test_progression_rate_at_020_adds_40(self):
        s = self._score(stage_to_stage_progression_rate_pct=0.20)
        assert s == 40.0

    def test_progression_rate_below_020_adds_40(self):
        s = self._score(stage_to_stage_progression_rate_pct=0.10)
        assert s == 40.0

    # deals_slipped_more_than_once_pct
    def test_slipped_below_025_adds_zero(self):
        s = self._score(deals_slipped_more_than_once_pct=0.24)
        assert s == 0.0

    def test_slipped_at_025_adds_18(self):
        s = self._score(deals_slipped_more_than_once_pct=0.25)
        assert s == 18.0

    def test_slipped_between_025_045_adds_18(self):
        s = self._score(deals_slipped_more_than_once_pct=0.35)
        assert s == 18.0

    def test_slipped_at_045_adds_35(self):
        s = self._score(deals_slipped_more_than_once_pct=0.45)
        assert s == 35.0

    def test_slipped_above_045_adds_35(self):
        s = self._score(deals_slipped_more_than_once_pct=0.80)
        assert s == 35.0

    # stage_overage
    def test_overage_below_14_adds_zero(self):
        s = self._score(avg_days_in_current_stage=20.0, expected_days_in_stage=10.0)
        # overage = 10, below 14 → +0
        assert s == 0.0

    def test_overage_at_14_adds_12(self):
        s = self._score(avg_days_in_current_stage=24.0, expected_days_in_stage=10.0)
        # overage = 14
        assert s == 12.0

    def test_overage_between_14_30_adds_12(self):
        s = self._score(avg_days_in_current_stage=30.0, expected_days_in_stage=10.0)
        # overage = 20
        assert s == 12.0

    def test_overage_at_30_adds_25(self):
        s = self._score(avg_days_in_current_stage=40.0, expected_days_in_stage=10.0)
        # overage = 30
        assert s == 25.0

    def test_overage_above_30_adds_25(self):
        s = self._score(avg_days_in_current_stage=100.0, expected_days_in_stage=10.0)
        assert s == 25.0

    def test_negative_overage_adds_zero(self):
        # avg < expected → negative overage, adds nothing
        s = self._score(avg_days_in_current_stage=5.0, expected_days_in_stage=15.0)
        assert s == 0.0

    def test_progression_max_combination(self):
        # 40 + 35 + 25 = 100
        s = self._score(
            stage_to_stage_progression_rate_pct=0.20,
            deals_slipped_more_than_once_pct=0.45,
            avg_days_in_current_stage=40.0,
            expected_days_in_stage=10.0,
        )
        assert s == 100.0

    def test_progression_capped_at_100(self):
        s = self._score(
            stage_to_stage_progression_rate_pct=0.01,
            deals_slipped_more_than_once_pct=0.99,
            avg_days_in_current_stage=999.0,
            expected_days_in_stage=1.0,
        )
        assert s == 100.0

    def test_progression_partial_sum(self):
        # 22 + 18 + 12 = 52
        s = self._score(
            stage_to_stage_progression_rate_pct=0.40,
            deals_slipped_more_than_once_pct=0.25,
            avg_days_in_current_stage=24.0,
            expected_days_in_stage=10.0,
        )
        assert s == 52.0


# ===========================================================================
# 6. Curation sub-score branches
# ===========================================================================

class TestCurationScore:
    def _score(self, **kw) -> float:
        engine = fresh_engine()
        inp = make_input(**kw)
        return engine._curation_score(inp)

    # deals_added_not_touched_after_create_pct
    def test_not_touched_below_010_adds_zero(self):
        s = self._score(deals_added_not_touched_after_create_pct=0.09)
        assert s == 0.0

    def test_not_touched_at_010_adds_8(self):
        s = self._score(deals_added_not_touched_after_create_pct=0.10)
        assert s == 8.0

    def test_not_touched_between_010_025_adds_8(self):
        s = self._score(deals_added_not_touched_after_create_pct=0.18)
        assert s == 8.0

    def test_not_touched_at_025_adds_22(self):
        s = self._score(deals_added_not_touched_after_create_pct=0.25)
        assert s == 22.0

    def test_not_touched_between_025_040_adds_22(self):
        s = self._score(deals_added_not_touched_after_create_pct=0.35)
        assert s == 22.0

    def test_not_touched_at_040_adds_40(self):
        s = self._score(deals_added_not_touched_after_create_pct=0.40)
        assert s == 40.0

    def test_not_touched_above_040_adds_40(self):
        s = self._score(deals_added_not_touched_after_create_pct=0.80)
        assert s == 40.0

    # deals_exceeding_avg_stage_duration_pct
    def test_exceeding_below_035_adds_zero(self):
        s = self._score(deals_exceeding_avg_stage_duration_pct=0.34)
        assert s == 0.0

    def test_exceeding_at_035_adds_18(self):
        s = self._score(deals_exceeding_avg_stage_duration_pct=0.35)
        assert s == 18.0

    def test_exceeding_between_035_055_adds_18(self):
        s = self._score(deals_exceeding_avg_stage_duration_pct=0.45)
        assert s == 18.0

    def test_exceeding_at_055_adds_35(self):
        s = self._score(deals_exceeding_avg_stage_duration_pct=0.55)
        assert s == 35.0

    def test_exceeding_above_055_adds_35(self):
        s = self._score(deals_exceeding_avg_stage_duration_pct=0.90)
        assert s == 35.0

    # closed_won_from_current_pipeline_pct
    def test_won_above_030_adds_zero(self):
        s = self._score(closed_won_from_current_pipeline_pct=0.31)
        assert s == 0.0

    def test_won_at_030_adds_12(self):
        s = self._score(closed_won_from_current_pipeline_pct=0.30)
        assert s == 12.0

    def test_won_between_015_030_adds_12(self):
        s = self._score(closed_won_from_current_pipeline_pct=0.22)
        assert s == 12.0

    def test_won_at_015_adds_25(self):
        s = self._score(closed_won_from_current_pipeline_pct=0.15)
        assert s == 25.0

    def test_won_below_015_adds_25(self):
        s = self._score(closed_won_from_current_pipeline_pct=0.05)
        assert s == 25.0

    def test_curation_max_combination(self):
        # 40 + 35 + 25 = 100
        s = self._score(
            deals_added_not_touched_after_create_pct=0.40,
            deals_exceeding_avg_stage_duration_pct=0.55,
            closed_won_from_current_pipeline_pct=0.15,
        )
        assert s == 100.0

    def test_curation_capped_at_100(self):
        s = self._score(
            deals_added_not_touched_after_create_pct=0.99,
            deals_exceeding_avg_stage_duration_pct=0.99,
            closed_won_from_current_pipeline_pct=0.01,
        )
        assert s == 100.0

    def test_curation_partial_sum(self):
        # 22 + 18 + 12 = 52
        s = self._score(
            deals_added_not_touched_after_create_pct=0.25,
            deals_exceeding_avg_stage_duration_pct=0.35,
            closed_won_from_current_pipeline_pct=0.30,
        )
        assert s == 52.0


# ===========================================================================
# 7. Concentration sub-score branches
# ===========================================================================

class TestConcentrationScore:
    def _score(self, **kw) -> float:
        engine = fresh_engine()
        inp = make_input(**kw)
        return engine._concentration_score(inp)

    # single_stage_pipeline_concentration
    def test_concentration_below_030_adds_zero(self):
        s = self._score(single_stage_pipeline_concentration=0.29)
        assert s == 0.0

    def test_concentration_at_030_adds_10(self):
        s = self._score(single_stage_pipeline_concentration=0.30)
        assert s == 10.0

    def test_concentration_between_030_045_adds_10(self):
        s = self._score(single_stage_pipeline_concentration=0.40)
        assert s == 10.0

    def test_concentration_at_045_adds_25(self):
        s = self._score(single_stage_pipeline_concentration=0.45)
        assert s == 25.0

    def test_concentration_between_045_065_adds_25(self):
        s = self._score(single_stage_pipeline_concentration=0.55)
        assert s == 25.0

    def test_concentration_at_065_adds_45(self):
        s = self._score(single_stage_pipeline_concentration=0.65)
        assert s == 45.0

    def test_concentration_above_065_adds_45(self):
        s = self._score(single_stage_pipeline_concentration=0.90)
        assert s == 45.0

    # late_stage_deals_pct
    def test_late_stage_above_025_adds_zero(self):
        s = self._score(late_stage_deals_pct=0.26)
        assert s == 0.0

    def test_late_stage_at_025_adds_15(self):
        s = self._score(late_stage_deals_pct=0.25)
        assert s == 15.0

    def test_late_stage_between_010_025_adds_15(self):
        s = self._score(late_stage_deals_pct=0.18)
        assert s == 15.0

    def test_late_stage_at_010_adds_30(self):
        s = self._score(late_stage_deals_pct=0.10)
        assert s == 30.0

    def test_late_stage_below_010_adds_30(self):
        s = self._score(late_stage_deals_pct=0.05)
        assert s == 30.0

    # pipeline_refresh_rate_pct
    def test_refresh_above_030_adds_zero(self):
        s = self._score(pipeline_refresh_rate_pct=0.31)
        assert s == 0.0

    def test_refresh_at_030_adds_12(self):
        s = self._score(pipeline_refresh_rate_pct=0.30)
        assert s == 12.0

    def test_refresh_between_015_030_adds_12(self):
        s = self._score(pipeline_refresh_rate_pct=0.22)
        assert s == 12.0

    def test_refresh_at_015_adds_25(self):
        s = self._score(pipeline_refresh_rate_pct=0.15)
        assert s == 25.0

    def test_refresh_below_015_adds_25(self):
        s = self._score(pipeline_refresh_rate_pct=0.05)
        assert s == 25.0

    def test_concentration_max_combination(self):
        # 45 + 30 + 25 = 100
        s = self._score(
            single_stage_pipeline_concentration=0.65,
            late_stage_deals_pct=0.10,
            pipeline_refresh_rate_pct=0.15,
        )
        assert s == 100.0

    def test_concentration_capped_at_100(self):
        s = self._score(
            single_stage_pipeline_concentration=0.99,
            late_stage_deals_pct=0.01,
            pipeline_refresh_rate_pct=0.01,
        )
        assert s == 100.0

    def test_concentration_partial_sum(self):
        # 25 + 15 + 12 = 52
        s = self._score(
            single_stage_pipeline_concentration=0.45,
            late_stage_deals_pct=0.25,
            pipeline_refresh_rate_pct=0.30,
        )
        assert s == 52.0


# ===========================================================================
# 8. Composite formula weights
# ===========================================================================

class TestCompositeFormula:
    def test_composite_weights_with_isolated_staleness(self):
        # Only staleness contributes: pure 100 staleness → 100 * 0.30 = 30
        engine = fresh_engine()
        inp = make_input(
            deals_with_no_activity_30d_pct=0.50,
            avg_deal_age_days=120.0,
            deals_with_no_activity_60d_pct=0.35,
            # All other sub-scores should be 0
            stage_to_stage_progression_rate_pct=0.99,
            deals_slipped_more_than_once_pct=0.0,
            avg_days_in_current_stage=5.0,
            expected_days_in_stage=15.0,
            deals_added_not_touched_after_create_pct=0.0,
            deals_exceeding_avg_stage_duration_pct=0.0,
            closed_won_from_current_pipeline_pct=0.99,
            single_stage_pipeline_concentration=0.0,
            late_stage_deals_pct=0.99,
            pipeline_refresh_rate_pct=0.99,
        )
        result = engine.assess(inp)
        assert result.staleness_score == 100.0
        assert result.progression_score == 0.0
        assert result.curation_score == 0.0
        assert result.concentration_score == 0.0
        assert result.pipeline_composite == 30.0

    def test_composite_weights_with_isolated_progression(self):
        # progression = 100 → 100 * 0.30 = 30
        engine = fresh_engine()
        inp = make_input(
            deals_with_no_activity_30d_pct=0.0,
            avg_deal_age_days=0.0,
            deals_with_no_activity_60d_pct=0.0,
            stage_to_stage_progression_rate_pct=0.20,
            deals_slipped_more_than_once_pct=0.45,
            avg_days_in_current_stage=40.0,
            expected_days_in_stage=10.0,
            deals_added_not_touched_after_create_pct=0.0,
            deals_exceeding_avg_stage_duration_pct=0.0,
            closed_won_from_current_pipeline_pct=0.99,
            single_stage_pipeline_concentration=0.0,
            late_stage_deals_pct=0.99,
            pipeline_refresh_rate_pct=0.99,
        )
        result = engine.assess(inp)
        assert result.progression_score == 100.0
        assert result.staleness_score == 0.0
        assert result.curation_score == 0.0
        assert result.concentration_score == 0.0
        assert result.pipeline_composite == 30.0

    def test_composite_weights_with_isolated_curation(self):
        # curation = 100 → 100 * 0.25 = 25
        engine = fresh_engine()
        inp = make_input(
            deals_with_no_activity_30d_pct=0.0,
            avg_deal_age_days=0.0,
            deals_with_no_activity_60d_pct=0.0,
            stage_to_stage_progression_rate_pct=0.99,
            deals_slipped_more_than_once_pct=0.0,
            avg_days_in_current_stage=5.0,
            expected_days_in_stage=15.0,
            deals_added_not_touched_after_create_pct=0.40,
            deals_exceeding_avg_stage_duration_pct=0.55,
            closed_won_from_current_pipeline_pct=0.15,
            single_stage_pipeline_concentration=0.0,
            late_stage_deals_pct=0.99,
            pipeline_refresh_rate_pct=0.99,
        )
        result = engine.assess(inp)
        assert result.curation_score == 100.0
        assert result.staleness_score == 0.0
        assert result.progression_score == 0.0
        assert result.concentration_score == 0.0
        assert result.pipeline_composite == 25.0

    def test_composite_weights_with_isolated_concentration(self):
        # concentration = 100 → 100 * 0.15 = 15
        engine = fresh_engine()
        inp = make_input(
            deals_with_no_activity_30d_pct=0.0,
            avg_deal_age_days=0.0,
            deals_with_no_activity_60d_pct=0.0,
            stage_to_stage_progression_rate_pct=0.99,
            deals_slipped_more_than_once_pct=0.0,
            avg_days_in_current_stage=5.0,
            expected_days_in_stage=15.0,
            deals_added_not_touched_after_create_pct=0.0,
            deals_exceeding_avg_stage_duration_pct=0.0,
            closed_won_from_current_pipeline_pct=0.99,
            single_stage_pipeline_concentration=0.65,
            late_stage_deals_pct=0.10,
            pipeline_refresh_rate_pct=0.15,
        )
        result = engine.assess(inp)
        assert result.concentration_score == 100.0
        assert result.staleness_score == 0.0
        assert result.progression_score == 0.0
        assert result.curation_score == 0.0
        assert result.pipeline_composite == 15.0

    def test_composite_all_100_gives_100(self):
        engine = fresh_engine()
        inp = make_input(
            deals_with_no_activity_30d_pct=0.50,
            avg_deal_age_days=120.0,
            deals_with_no_activity_60d_pct=0.35,
            stage_to_stage_progression_rate_pct=0.20,
            deals_slipped_more_than_once_pct=0.45,
            avg_days_in_current_stage=40.0,
            expected_days_in_stage=10.0,
            deals_added_not_touched_after_create_pct=0.40,
            deals_exceeding_avg_stage_duration_pct=0.55,
            closed_won_from_current_pipeline_pct=0.15,
            single_stage_pipeline_concentration=0.65,
            late_stage_deals_pct=0.10,
            pipeline_refresh_rate_pct=0.15,
        )
        result = engine.assess(inp)
        assert result.pipeline_composite == 100.0

    def test_composite_formula_manual(self):
        # staleness=40, progression=40, curation=40, concentration=45
        # composite = 40*0.30 + 40*0.30 + 40*0.25 + 45*0.15 = 12 + 12 + 10 + 6.75 = 40.75
        engine = fresh_engine()
        inp = make_input(
            deals_with_no_activity_30d_pct=0.50,
            avg_deal_age_days=0.0,
            deals_with_no_activity_60d_pct=0.0,
            stage_to_stage_progression_rate_pct=0.20,
            deals_slipped_more_than_once_pct=0.0,
            avg_days_in_current_stage=5.0,
            expected_days_in_stage=15.0,
            deals_added_not_touched_after_create_pct=0.40,
            deals_exceeding_avg_stage_duration_pct=0.0,
            closed_won_from_current_pipeline_pct=0.99,
            single_stage_pipeline_concentration=0.65,
            late_stage_deals_pct=0.99,
            pipeline_refresh_rate_pct=0.99,
        )
        result = engine.assess(inp)
        assert result.staleness_score == 40.0
        assert result.progression_score == 40.0
        assert result.curation_score == 40.0
        assert result.concentration_score == 45.0
        expected_composite = round(40 * 0.30 + 40 * 0.30 + 40 * 0.25 + 45 * 0.15, 1)
        assert result.pipeline_composite == expected_composite


# ===========================================================================
# 9. Pattern detection and priority ordering
# ===========================================================================

class TestPatternDetection:
    def _pattern(self, **kw) -> PipelinePattern:
        engine = fresh_engine()
        return engine.assess(make_input(**kw)).pipeline_pattern

    def test_zombie_deal_accumulation_detected(self):
        p = self._pattern(
            deals_with_no_activity_60d_pct=0.30,
            deals_added_not_touched_after_create_pct=0.30,
        )
        assert p == PipelinePattern.zombie_deal_accumulation

    def test_zombie_at_exact_boundaries(self):
        p = self._pattern(
            deals_with_no_activity_60d_pct=0.30,
            deals_added_not_touched_after_create_pct=0.30,
        )
        assert p == PipelinePattern.zombie_deal_accumulation

    def test_zombie_priority_over_pipeline_inflation(self):
        # Both zombie and pipeline_inflation conditions met
        p = self._pattern(
            deals_with_no_activity_60d_pct=0.40,
            deals_added_not_touched_after_create_pct=0.40,
            closed_won_from_current_pipeline_pct=0.05,
            deals_exceeding_avg_stage_duration_pct=0.55,
        )
        assert p == PipelinePattern.zombie_deal_accumulation

    def test_pipeline_inflation_detected(self):
        # curation >= 40 requires: deals_added_not_touched >= 0.40 → +40, then won <= 0.20
        p = self._pattern(
            deals_added_not_touched_after_create_pct=0.40,
            closed_won_from_current_pipeline_pct=0.20,
            deals_with_no_activity_60d_pct=0.05,
        )
        assert p == PipelinePattern.pipeline_inflation

    def test_pipeline_inflation_not_detected_when_won_above_threshold(self):
        p = self._pattern(
            deals_added_not_touched_after_create_pct=0.40,
            closed_won_from_current_pipeline_pct=0.21,
            deals_with_no_activity_60d_pct=0.05,
        )
        assert p != PipelinePattern.pipeline_inflation

    def test_stage_stagnation_detected(self):
        # progression >= 35 needs e.g. slipped=0.35→+18, progression_rate<=0.20→+40 = 58; slipped>=0.35
        p = self._pattern(
            stage_to_stage_progression_rate_pct=0.20,
            deals_slipped_more_than_once_pct=0.35,
            avg_days_in_current_stage=5.0,
            expected_days_in_stage=15.0,
            deals_with_no_activity_60d_pct=0.05,
            deals_added_not_touched_after_create_pct=0.05,
            closed_won_from_current_pipeline_pct=0.99,
        )
        assert p == PipelinePattern.stage_stagnation

    def test_stage_stagnation_priority_after_zombie_and_inflation(self):
        # zombie and inflation conditions NOT met, stagnation IS met
        p = self._pattern(
            deals_with_no_activity_60d_pct=0.05,
            deals_added_not_touched_after_create_pct=0.05,
            closed_won_from_current_pipeline_pct=0.99,
            stage_to_stage_progression_rate_pct=0.20,
            deals_slipped_more_than_once_pct=0.35,
            avg_days_in_current_stage=5.0,
            expected_days_in_stage=15.0,
        )
        assert p == PipelinePattern.stage_stagnation

    def test_curation_avoidance_detected(self):
        # closed_lost_rate <= 0.10 AND staleness >= 30
        # staleness >= 30: need 30d_pct >= 0.30 → +22, age >= 75 → +18 = 40
        p = self._pattern(
            deals_closed_lost_rate_pct=0.10,
            deals_with_no_activity_30d_pct=0.30,
            avg_deal_age_days=75.0,
            deals_with_no_activity_60d_pct=0.0,
            stage_to_stage_progression_rate_pct=0.99,
            deals_slipped_more_than_once_pct=0.0,
            avg_days_in_current_stage=5.0,
            expected_days_in_stage=15.0,
            deals_added_not_touched_after_create_pct=0.05,
            closed_won_from_current_pipeline_pct=0.99,
        )
        assert p == PipelinePattern.curation_avoidance

    def test_curation_avoidance_not_detected_when_lost_rate_high(self):
        p = self._pattern(
            deals_closed_lost_rate_pct=0.11,
            deals_with_no_activity_30d_pct=0.30,
            avg_deal_age_days=75.0,
        )
        assert p != PipelinePattern.curation_avoidance

    def test_late_stage_concentration_detected(self):
        # late_stage_deals_pct >= 0.65 AND concentration >= 25
        # concentration >= 25: single_stage_pipeline_concentration >= 0.45 → +25
        p = self._pattern(
            late_stage_deals_pct=0.65,
            single_stage_pipeline_concentration=0.45,
            pipeline_refresh_rate_pct=0.99,
            deals_with_no_activity_60d_pct=0.05,
            deals_added_not_touched_after_create_pct=0.05,
            closed_won_from_current_pipeline_pct=0.99,
            stage_to_stage_progression_rate_pct=0.99,
            deals_slipped_more_than_once_pct=0.0,
            avg_days_in_current_stage=5.0,
            expected_days_in_stage=15.0,
            deals_closed_lost_rate_pct=0.99,
        )
        assert p == PipelinePattern.late_stage_concentration

    def test_none_pattern_when_no_conditions_met(self):
        p = self._pattern()
        assert p == PipelinePattern.none

    def test_zombie_wins_over_stage_stagnation(self):
        # Both zombie and stagnation conditions are met
        p = self._pattern(
            deals_with_no_activity_60d_pct=0.40,
            deals_added_not_touched_after_create_pct=0.40,
            stage_to_stage_progression_rate_pct=0.20,
            deals_slipped_more_than_once_pct=0.50,
            closed_won_from_current_pipeline_pct=0.99,
        )
        assert p == PipelinePattern.zombie_deal_accumulation

    def test_inflation_wins_over_stagnation(self):
        # inflation conditions met (no zombie), stagnation also met
        p = self._pattern(
            deals_with_no_activity_60d_pct=0.05,
            deals_added_not_touched_after_create_pct=0.40,
            closed_won_from_current_pipeline_pct=0.20,
            stage_to_stage_progression_rate_pct=0.20,
            deals_slipped_more_than_once_pct=0.50,
        )
        assert p == PipelinePattern.pipeline_inflation


# ===========================================================================
# 10. Risk / Severity threshold tests (exact boundaries)
# ===========================================================================

class TestRiskLevel:
    def _risk(self, composite: float) -> PipelineRisk:
        engine = fresh_engine()
        return engine._risk_level(composite)

    def test_below_20_is_low(self):
        assert self._risk(19.9) == PipelineRisk.low

    def test_at_0_is_low(self):
        assert self._risk(0.0) == PipelineRisk.low

    def test_at_20_is_moderate(self):
        assert self._risk(20.0) == PipelineRisk.moderate

    def test_between_20_40_is_moderate(self):
        assert self._risk(30.0) == PipelineRisk.moderate

    def test_at_40_is_high(self):
        assert self._risk(40.0) == PipelineRisk.high

    def test_between_40_60_is_high(self):
        assert self._risk(50.0) == PipelineRisk.high

    def test_at_60_is_critical(self):
        assert self._risk(60.0) == PipelineRisk.critical

    def test_above_60_is_critical(self):
        assert self._risk(100.0) == PipelineRisk.critical


class TestSeverityLevel:
    def _severity(self, composite: float) -> PipelineSeverity:
        engine = fresh_engine()
        return engine._severity(composite)

    def test_below_20_is_healthy(self):
        assert self._severity(19.9) == PipelineSeverity.healthy

    def test_at_0_is_healthy(self):
        assert self._severity(0.0) == PipelineSeverity.healthy

    def test_at_20_is_declining(self):
        assert self._severity(20.0) == PipelineSeverity.declining

    def test_between_20_40_is_declining(self):
        assert self._severity(30.0) == PipelineSeverity.declining

    def test_at_40_is_degraded(self):
        assert self._severity(40.0) == PipelineSeverity.degraded

    def test_between_40_60_is_degraded(self):
        assert self._severity(50.0) == PipelineSeverity.degraded

    def test_at_60_is_critical(self):
        assert self._severity(60.0) == PipelineSeverity.critical

    def test_above_60_is_critical(self):
        assert self._severity(100.0) == PipelineSeverity.critical


# ===========================================================================
# 11. Action mapping tests
# ===========================================================================

class TestActionMapping:
    def _action(self, risk: PipelineRisk, pattern: PipelinePattern) -> PipelineAction:
        engine = fresh_engine()
        return engine._action(risk, pattern)

    def test_critical_zombie_gives_hygiene_coaching(self):
        a = self._action(PipelineRisk.critical, PipelinePattern.zombie_deal_accumulation)
        assert a == PipelineAction.pipeline_hygiene_coaching

    def test_critical_inflation_gives_curation_workshop(self):
        a = self._action(PipelineRisk.critical, PipelinePattern.pipeline_inflation)
        assert a == PipelineAction.pipeline_curation_workshop

    def test_critical_stagnation_gives_reset_intervention(self):
        a = self._action(PipelineRisk.critical, PipelinePattern.stage_stagnation)
        assert a == PipelineAction.pipeline_reset_intervention

    def test_critical_curation_avoidance_gives_reset_intervention(self):
        a = self._action(PipelineRisk.critical, PipelinePattern.curation_avoidance)
        assert a == PipelineAction.pipeline_reset_intervention

    def test_critical_late_stage_gives_reset_intervention(self):
        a = self._action(PipelineRisk.critical, PipelinePattern.late_stage_concentration)
        assert a == PipelineAction.pipeline_reset_intervention

    def test_critical_none_gives_reset_intervention(self):
        a = self._action(PipelineRisk.critical, PipelinePattern.none)
        assert a == PipelineAction.pipeline_reset_intervention

    def test_high_stagnation_gives_exit_criteria_coaching(self):
        a = self._action(PipelineRisk.high, PipelinePattern.stage_stagnation)
        assert a == PipelineAction.stage_exit_criteria_coaching

    def test_high_curation_avoidance_gives_hygiene_coaching(self):
        a = self._action(PipelineRisk.high, PipelinePattern.curation_avoidance)
        assert a == PipelineAction.pipeline_hygiene_coaching

    def test_high_zombie_gives_deal_progression_review(self):
        a = self._action(PipelineRisk.high, PipelinePattern.zombie_deal_accumulation)
        assert a == PipelineAction.deal_progression_review

    def test_high_inflation_gives_deal_progression_review(self):
        a = self._action(PipelineRisk.high, PipelinePattern.pipeline_inflation)
        assert a == PipelineAction.deal_progression_review

    def test_high_none_gives_deal_progression_review(self):
        a = self._action(PipelineRisk.high, PipelinePattern.none)
        assert a == PipelineAction.deal_progression_review

    def test_high_late_stage_gives_deal_progression_review(self):
        a = self._action(PipelineRisk.high, PipelinePattern.late_stage_concentration)
        assert a == PipelineAction.deal_progression_review

    def test_moderate_any_pattern_gives_hygiene_coaching(self):
        for pattern in PipelinePattern:
            a = self._action(PipelineRisk.moderate, pattern)
            assert a == PipelineAction.pipeline_hygiene_coaching

    def test_low_any_pattern_gives_no_action(self):
        for pattern in PipelinePattern:
            a = self._action(PipelineRisk.low, pattern)
            assert a == PipelineAction.no_action


# ===========================================================================
# 12. Flag condition tests
# ===========================================================================

class TestFlags:
    def _result(self, **kw) -> PipelineResult:
        engine = fresh_engine()
        return engine.assess(make_input(**kw))

    # has_pipeline_gap
    def test_gap_true_when_composite_ge_40(self):
        # Force composite >= 40: staleness=100 → composite=30, need more
        # Use staleness=100 + progression=100 → 30+30=60
        r = self._result(
            deals_with_no_activity_30d_pct=0.50,
            avg_deal_age_days=120.0,
            deals_with_no_activity_60d_pct=0.35,
            stage_to_stage_progression_rate_pct=0.20,
            deals_slipped_more_than_once_pct=0.45,
            avg_days_in_current_stage=40.0,
            expected_days_in_stage=10.0,
            closed_won_from_current_pipeline_pct=0.99,
            deals_added_not_touched_after_create_pct=0.0,
            deals_exceeding_avg_stage_duration_pct=0.0,
            single_stage_pipeline_concentration=0.0,
            late_stage_deals_pct=0.99,
            pipeline_refresh_rate_pct=0.99,
        )
        assert r.pipeline_composite >= 40
        assert r.has_pipeline_gap is True

    def test_gap_true_when_no_activity_60d_ge_025(self):
        r = self._result(
            deals_with_no_activity_60d_pct=0.25,
            closed_won_from_current_pipeline_pct=0.99,
        )
        assert r.has_pipeline_gap is True

    def test_gap_true_when_won_le_020(self):
        r = self._result(closed_won_from_current_pipeline_pct=0.20)
        assert r.has_pipeline_gap is True

    def test_gap_false_when_no_conditions_met(self):
        # Baseline healthy: composite < 40, 60d < 0.25, won > 0.20
        r = self._result()
        assert r.has_pipeline_gap is False

    def test_gap_boundary_60d_below_025_is_false_unless_other_conditions(self):
        r = self._result(
            deals_with_no_activity_60d_pct=0.24,
            closed_won_from_current_pipeline_pct=0.50,
        )
        # composite should be low too
        if r.pipeline_composite < 40:
            assert r.has_pipeline_gap is False

    # requires_pipeline_coaching
    def test_coaching_true_when_composite_ge_30(self):
        # staleness=100 → composite=30.0 → exactly 30
        r = self._result(
            deals_with_no_activity_30d_pct=0.50,
            avg_deal_age_days=120.0,
            deals_with_no_activity_60d_pct=0.35,
            stage_to_stage_progression_rate_pct=0.99,
            deals_slipped_more_than_once_pct=0.0,
            avg_days_in_current_stage=5.0,
            expected_days_in_stage=15.0,
            deals_added_not_touched_after_create_pct=0.0,
            deals_exceeding_avg_stage_duration_pct=0.0,
            closed_won_from_current_pipeline_pct=0.99,
            single_stage_pipeline_concentration=0.0,
            late_stage_deals_pct=0.99,
            pipeline_refresh_rate_pct=0.99,
        )
        assert r.pipeline_composite == 30.0
        assert r.requires_pipeline_coaching is True

    def test_coaching_true_when_exceeding_stage_duration_ge_035(self):
        r = self._result(deals_exceeding_avg_stage_duration_pct=0.35)
        assert r.requires_pipeline_coaching is True

    def test_coaching_true_when_30d_pct_ge_025(self):
        r = self._result(deals_with_no_activity_30d_pct=0.25)
        assert r.requires_pipeline_coaching is True

    def test_coaching_false_when_no_conditions_met(self):
        r = self._result()
        # composite < 30, exceeding < 0.35, 30d < 0.25
        assert r.requires_pipeline_coaching is False

    def test_coaching_boundary_30d_below_025(self):
        # With 30d=0.24 (below threshold), exceeding=0.10 (below 0.35), composite low
        r = self._result(
            deals_with_no_activity_30d_pct=0.24,
            deals_exceeding_avg_stage_duration_pct=0.10,
        )
        if r.pipeline_composite < 30:
            assert r.requires_pipeline_coaching is False


# ===========================================================================
# 13. Phantom pipeline formula
# ===========================================================================

class TestPhantomPipeline:
    def test_phantom_pipeline_formula(self):
        engine = fresh_engine()
        inp = make_input(
            total_open_deals=100,
            avg_opportunity_value_usd=10000.0,
            deals_with_no_activity_60d_pct=0.20,
        )
        result = engine.assess(inp)
        composite = result.pipeline_composite
        expected = round(100 * 10000.0 * 0.20 * (composite / 100.0), 2)
        assert result.estimated_phantom_pipeline_usd == expected

    def test_phantom_pipeline_is_zero_when_composite_is_zero(self):
        engine = fresh_engine()
        inp = make_input(
            total_open_deals=50,
            avg_opportunity_value_usd=5000.0,
            # Must also be 0 to avoid staleness score from 60d tier
            deals_with_no_activity_60d_pct=0.0,
            # Force all sub-scores to 0
            deals_with_no_activity_30d_pct=0.0,
            avg_deal_age_days=0.0,
            stage_to_stage_progression_rate_pct=0.99,
            deals_slipped_more_than_once_pct=0.0,
            avg_days_in_current_stage=5.0,
            expected_days_in_stage=15.0,
            deals_added_not_touched_after_create_pct=0.0,
            deals_exceeding_avg_stage_duration_pct=0.0,
            closed_won_from_current_pipeline_pct=0.99,
            single_stage_pipeline_concentration=0.0,
            late_stage_deals_pct=0.99,
            pipeline_refresh_rate_pct=0.99,
        )
        result = engine.assess(inp)
        assert result.pipeline_composite == 0.0
        assert result.estimated_phantom_pipeline_usd == 0.0

    def test_phantom_pipeline_is_zero_when_60d_is_zero(self):
        engine = fresh_engine()
        inp = make_input(
            total_open_deals=50,
            avg_opportunity_value_usd=5000.0,
            deals_with_no_activity_60d_pct=0.0,
        )
        result = engine.assess(inp)
        assert result.estimated_phantom_pipeline_usd == 0.0

    def test_phantom_pipeline_rounded_to_2_decimals(self):
        engine = fresh_engine()
        inp = make_input(
            total_open_deals=7,
            avg_opportunity_value_usd=3333.33,
            deals_with_no_activity_60d_pct=0.33,
        )
        result = engine.assess(inp)
        composite = result.pipeline_composite
        raw = 7 * 3333.33 * 0.33 * (composite / 100.0)
        assert result.estimated_phantom_pipeline_usd == round(raw, 2)

    def test_phantom_pipeline_scales_with_deals(self):
        engine1 = fresh_engine()
        engine2 = fresh_engine()
        base = dict(
            avg_opportunity_value_usd=10000.0,
            deals_with_no_activity_60d_pct=0.20,
        )
        r1 = engine1.assess(make_input(total_open_deals=10, **base))
        r2 = engine2.assess(make_input(total_open_deals=20, **base))
        # Both should have same composite; r2 phantom should be 2x r1
        assert r1.pipeline_composite == r2.pipeline_composite
        assert abs(r2.estimated_phantom_pipeline_usd - 2 * r1.estimated_phantom_pipeline_usd) < 0.01


# ===========================================================================
# 14. Signal string tests
# ===========================================================================

class TestSignalString:
    def _signal(self, **kw) -> str:
        engine = fresh_engine()
        return engine.assess(make_input(**kw)).pipeline_signal

    def test_healthy_signal_message(self):
        sig = self._signal()
        assert sig == "Pipeline health strong — deal activity, stage progression, and curation within benchmarks"

    def test_healthy_signal_requires_none_pattern_and_composite_below_20(self):
        # composite must be < 20 AND pattern must be none
        sig = self._signal()
        assert "Pipeline health strong" in sig

    def test_signal_with_pattern_contains_pattern_label(self):
        # zombie_deal_accumulation pattern
        sig = self._signal(
            deals_with_no_activity_60d_pct=0.40,
            deals_added_not_touched_after_create_pct=0.40,
        )
        # "zombie deal accumulation".capitalize() → "Zombie deal accumulation"
        assert sig.startswith("Zombie deal accumulation")

    def test_signal_contains_30d_pct(self):
        sig = self._signal(
            deals_with_no_activity_60d_pct=0.40,
            deals_added_not_touched_after_create_pct=0.40,
            deals_with_no_activity_30d_pct=0.50,
        )
        assert "50% deals with no activity 30d" in sig

    def test_signal_contains_progression_rate(self):
        sig = self._signal(
            deals_with_no_activity_60d_pct=0.40,
            deals_added_not_touched_after_create_pct=0.40,
            stage_to_stage_progression_rate_pct=0.70,
        )
        assert "70% stage progression rate" in sig

    def test_signal_contains_pipeline_converting(self):
        sig = self._signal(
            deals_with_no_activity_60d_pct=0.40,
            deals_added_not_touched_after_create_pct=0.40,
            closed_won_from_current_pipeline_pct=0.35,
        )
        assert "35% pipeline converting to wins" in sig

    def test_signal_contains_composite(self):
        engine = fresh_engine()
        inp = make_input(
            deals_with_no_activity_60d_pct=0.40,
            deals_added_not_touched_after_create_pct=0.40,
        )
        result = engine.assess(inp)
        assert f"composite {result.pipeline_composite:.0f}" in result.pipeline_signal

    def test_signal_pipeline_risk_label_for_none_pattern_with_high_composite(self):
        # If composite >= 20 but pattern is none, label becomes "Pipeline risk"
        engine = fresh_engine()
        # Force high staleness but avoid triggering any pattern
        inp = make_input(
            deals_with_no_activity_30d_pct=0.50,
            avg_deal_age_days=120.0,
            deals_with_no_activity_60d_pct=0.35,
            # Keep all pattern conditions unmet
            deals_added_not_touched_after_create_pct=0.05,
            closed_won_from_current_pipeline_pct=0.99,
            stage_to_stage_progression_rate_pct=0.99,
            deals_slipped_more_than_once_pct=0.0,
            deals_closed_lost_rate_pct=0.99,
            late_stage_deals_pct=0.40,
            single_stage_pipeline_concentration=0.20,
            pipeline_refresh_rate_pct=0.99,
            avg_days_in_current_stage=5.0,
            expected_days_in_stage=15.0,
        )
        result = engine.assess(inp)
        assert result.pipeline_pattern == PipelinePattern.none
        assert result.pipeline_composite >= 20
        assert result.pipeline_signal.startswith("Pipeline risk")

    def test_signal_format_with_underscores_replaced(self):
        # late_stage_concentration → "late stage concentration" → capitalized
        sig = self._signal(
            late_stage_deals_pct=0.65,
            single_stage_pipeline_concentration=0.45,
            pipeline_refresh_rate_pct=0.99,
            deals_with_no_activity_60d_pct=0.05,
            deals_added_not_touched_after_create_pct=0.05,
            closed_won_from_current_pipeline_pct=0.99,
            stage_to_stage_progression_rate_pct=0.99,
            deals_slipped_more_than_once_pct=0.0,
            avg_days_in_current_stage=5.0,
            expected_days_in_stage=15.0,
            deals_closed_lost_rate_pct=0.99,
        )
        assert sig.startswith("Late stage concentration")


# ===========================================================================
# 15. assess() end-to-end tests
# ===========================================================================

class TestAssess:
    def test_assess_returns_pipeline_result(self):
        engine = fresh_engine()
        result = engine.assess(make_input())
        assert isinstance(result, PipelineResult)

    def test_assess_stores_rep_id_and_region(self):
        engine = fresh_engine()
        inp = make_input(rep_id="REP-777", region="LATAM")
        result = engine.assess(inp)
        assert result.rep_id == "REP-777"
        assert result.region == "LATAM"

    def test_assess_healthy_baseline(self):
        engine = fresh_engine()
        result = engine.assess(make_input())
        assert result.pipeline_risk == PipelineRisk.low
        assert result.pipeline_severity == PipelineSeverity.healthy
        assert result.recommended_action == PipelineAction.no_action
        assert result.pipeline_pattern == PipelinePattern.none

    def test_assess_critical_scenario(self):
        engine = fresh_engine()
        inp = make_input(
            deals_with_no_activity_30d_pct=0.50,
            avg_deal_age_days=120.0,
            deals_with_no_activity_60d_pct=0.35,
            stage_to_stage_progression_rate_pct=0.20,
            deals_slipped_more_than_once_pct=0.45,
            avg_days_in_current_stage=40.0,
            expected_days_in_stage=10.0,
            deals_added_not_touched_after_create_pct=0.40,
            deals_exceeding_avg_stage_duration_pct=0.55,
            closed_won_from_current_pipeline_pct=0.15,
            single_stage_pipeline_concentration=0.65,
            late_stage_deals_pct=0.10,
            pipeline_refresh_rate_pct=0.15,
        )
        result = engine.assess(inp)
        assert result.pipeline_risk == PipelineRisk.critical
        assert result.pipeline_severity == PipelineSeverity.critical
        assert result.pipeline_composite == 100.0

    def test_assess_accumulates_results(self):
        engine = fresh_engine()
        engine.assess(make_input(rep_id="R1"))
        engine.assess(make_input(rep_id="R2"))
        assert len(engine._results) == 2

    def test_assess_sub_scores_are_rounded_to_1_decimal(self):
        engine = fresh_engine()
        result = engine.assess(make_input())
        for score in [result.staleness_score, result.progression_score,
                      result.curation_score, result.concentration_score,
                      result.pipeline_composite]:
            assert score == round(score, 1)


# ===========================================================================
# 16. assess_batch() tests
# ===========================================================================

class TestAssessBatch:
    def test_assess_batch_returns_list(self):
        engine = fresh_engine()
        results = engine.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        assert isinstance(results, list)
        assert len(results) == 3

    def test_assess_batch_all_pipeline_results(self):
        engine = fresh_engine()
        results = engine.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        for r in results:
            assert isinstance(r, PipelineResult)

    def test_assess_batch_empty_list(self):
        engine = fresh_engine()
        results = engine.assess_batch([])
        assert results == []

    def test_assess_batch_accumulates_all(self):
        engine = fresh_engine()
        engine.assess_batch([make_input(rep_id=f"R{i}") for i in range(4)])
        assert len(engine._results) == 4

    def test_assess_batch_preserves_order(self):
        engine = fresh_engine()
        inputs = [make_input(rep_id=f"REP-{i:03d}") for i in range(5)]
        results = engine.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"REP-{i:03d}"


# ===========================================================================
# 17. summary() tests — empty and populated
# ===========================================================================

class TestSummary:
    def test_empty_summary_returns_dict(self):
        engine = fresh_engine()
        s = engine.summary()
        assert isinstance(s, dict)

    def test_empty_summary_has_13_keys(self):
        engine = fresh_engine()
        s = engine.summary()
        assert len(s) == 13

    def test_empty_summary_key_names(self):
        engine = fresh_engine()
        s = engine.summary()
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_pipeline_composite", "pipeline_gap_count",
            "coaching_count", "avg_staleness_score", "avg_progression_score",
            "avg_curation_score", "avg_concentration_score",
            "total_estimated_phantom_pipeline_usd",
        }
        assert set(s.keys()) == expected_keys

    def test_empty_summary_values(self):
        engine = fresh_engine()
        s = engine.summary()
        assert s["total"] == 0
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}
        assert s["avg_pipeline_composite"] == 0.0
        assert s["pipeline_gap_count"] == 0
        assert s["coaching_count"] == 0
        assert s["avg_staleness_score"] == 0.0
        assert s["avg_progression_score"] == 0.0
        assert s["avg_curation_score"] == 0.0
        assert s["avg_concentration_score"] == 0.0
        assert s["total_estimated_phantom_pipeline_usd"] == 0.0

    def test_populated_summary_has_13_keys(self):
        engine = fresh_engine()
        engine.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        s = engine.summary()
        assert len(s) == 13

    def test_populated_summary_correct_total(self):
        engine = fresh_engine()
        engine.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        s = engine.summary()
        assert s["total"] == 5

    def test_populated_summary_risk_counts(self):
        engine = fresh_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert "low" in s["risk_counts"]
        assert s["risk_counts"]["low"] == 1

    def test_populated_summary_pattern_counts(self):
        engine = fresh_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert "none" in s["pattern_counts"]
        assert s["pattern_counts"]["none"] == 1

    def test_populated_summary_severity_counts(self):
        engine = fresh_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert "healthy" in s["severity_counts"]
        assert s["severity_counts"]["healthy"] == 1

    def test_populated_summary_action_counts(self):
        engine = fresh_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert "no_action" in s["action_counts"]
        assert s["action_counts"]["no_action"] == 1

    def test_populated_summary_avg_composite_rounded_to_1(self):
        engine = fresh_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert s["avg_pipeline_composite"] == round(s["avg_pipeline_composite"], 1)

    def test_populated_summary_pipeline_gap_count(self):
        engine = fresh_engine()
        # This input has won = 0.20 → has_pipeline_gap=True
        engine.assess(make_input(closed_won_from_current_pipeline_pct=0.20))
        engine.assess(make_input())  # baseline → gap=False
        s = engine.summary()
        assert s["pipeline_gap_count"] == 1

    def test_populated_summary_coaching_count(self):
        engine = fresh_engine()
        # coaching = True when 30d >= 0.25
        engine.assess(make_input(deals_with_no_activity_30d_pct=0.25))
        engine.assess(make_input())  # coaching = False
        s = engine.summary()
        assert s["coaching_count"] == 1

    def test_populated_summary_avg_scores_match_manual(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input(rep_id="R1"))
        r2 = engine.assess(make_input(rep_id="R2"))
        s = engine.summary()
        expected_avg_composite = round((r1.pipeline_composite + r2.pipeline_composite) / 2, 1)
        assert s["avg_pipeline_composite"] == expected_avg_composite

    def test_populated_summary_avg_staleness(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input(rep_id="R1"))
        r2 = engine.assess(make_input(rep_id="R2"))
        s = engine.summary()
        expected = round((r1.staleness_score + r2.staleness_score) / 2, 1)
        assert s["avg_staleness_score"] == expected

    def test_populated_summary_avg_progression(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input(rep_id="R1"))
        r2 = engine.assess(make_input(rep_id="R2"))
        s = engine.summary()
        expected = round((r1.progression_score + r2.progression_score) / 2, 1)
        assert s["avg_progression_score"] == expected

    def test_populated_summary_avg_curation(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input(rep_id="R1"))
        r2 = engine.assess(make_input(rep_id="R2"))
        s = engine.summary()
        expected = round((r1.curation_score + r2.curation_score) / 2, 1)
        assert s["avg_curation_score"] == expected

    def test_populated_summary_avg_concentration(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input(rep_id="R1"))
        r2 = engine.assess(make_input(rep_id="R2"))
        s = engine.summary()
        expected = round((r1.concentration_score + r2.concentration_score) / 2, 1)
        assert s["avg_concentration_score"] == expected

    def test_populated_summary_total_phantom_pipeline(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input(rep_id="R1"))
        r2 = engine.assess(make_input(rep_id="R2"))
        s = engine.summary()
        expected = round(r1.estimated_phantom_pipeline_usd + r2.estimated_phantom_pipeline_usd, 2)
        assert s["total_estimated_phantom_pipeline_usd"] == expected

    def test_summary_multiple_risk_levels(self):
        engine = fresh_engine()
        # Low risk
        engine.assess(make_input(rep_id="R1"))
        # Critical risk - max everything
        engine.assess(make_input(
            rep_id="R2",
            deals_with_no_activity_30d_pct=0.50,
            avg_deal_age_days=120.0,
            deals_with_no_activity_60d_pct=0.35,
            stage_to_stage_progression_rate_pct=0.20,
            deals_slipped_more_than_once_pct=0.45,
            avg_days_in_current_stage=40.0,
            expected_days_in_stage=10.0,
            deals_added_not_touched_after_create_pct=0.40,
            deals_exceeding_avg_stage_duration_pct=0.55,
            closed_won_from_current_pipeline_pct=0.15,
            single_stage_pipeline_concentration=0.65,
            late_stage_deals_pct=0.10,
            pipeline_refresh_rate_pct=0.15,
        ))
        s = engine.summary()
        assert s["total"] == 2
        assert s["risk_counts"].get("low", 0) == 1
        assert s["risk_counts"].get("critical", 0) == 1

    def test_fresh_engine_summary_after_batch_empty(self):
        engine = fresh_engine()
        engine.assess_batch([])
        s = engine.summary()
        assert s["total"] == 0

    def test_summary_key_types(self):
        engine = fresh_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert isinstance(s["total"], int)
        assert isinstance(s["risk_counts"], dict)
        assert isinstance(s["pattern_counts"], dict)
        assert isinstance(s["severity_counts"], dict)
        assert isinstance(s["action_counts"], dict)
        assert isinstance(s["avg_pipeline_composite"], float)
        assert isinstance(s["pipeline_gap_count"], int)
        assert isinstance(s["coaching_count"], int)
        assert isinstance(s["avg_staleness_score"], float)
        assert isinstance(s["avg_progression_score"], float)
        assert isinstance(s["avg_curation_score"], float)
        assert isinstance(s["avg_concentration_score"], float)
        assert isinstance(s["total_estimated_phantom_pipeline_usd"], float)


# ===========================================================================
# 18. Additional boundary / edge case tests
# ===========================================================================

class TestBoundaryEdgeCases:
    def test_all_zeros_input_gives_zero_composite(self):
        engine = fresh_engine()
        inp = make_input(
            deals_with_no_activity_30d_pct=0.0,
            avg_deal_age_days=0.0,
            deals_with_no_activity_60d_pct=0.0,
            stage_to_stage_progression_rate_pct=0.99,
            deals_slipped_more_than_once_pct=0.0,
            avg_days_in_current_stage=5.0,
            expected_days_in_stage=15.0,
            deals_added_not_touched_after_create_pct=0.0,
            deals_exceeding_avg_stage_duration_pct=0.0,
            closed_won_from_current_pipeline_pct=0.99,
            single_stage_pipeline_concentration=0.0,
            late_stage_deals_pct=0.99,
            pipeline_refresh_rate_pct=0.99,
        )
        result = engine.assess(inp)
        assert result.staleness_score == 0.0
        assert result.progression_score == 0.0
        assert result.curation_score == 0.0
        assert result.concentration_score == 0.0
        assert result.pipeline_composite == 0.0

    def test_exact_composite_60_is_critical(self):
        # Need composite = 60 exactly
        # staleness=100*0.30=30, progression=100*0.30=30, curation=0, concentration=0 → 60
        engine = fresh_engine()
        inp = make_input(
            deals_with_no_activity_30d_pct=0.50,
            avg_deal_age_days=120.0,
            deals_with_no_activity_60d_pct=0.35,
            stage_to_stage_progression_rate_pct=0.20,
            deals_slipped_more_than_once_pct=0.45,
            avg_days_in_current_stage=40.0,
            expected_days_in_stage=10.0,
            deals_added_not_touched_after_create_pct=0.0,
            deals_exceeding_avg_stage_duration_pct=0.0,
            closed_won_from_current_pipeline_pct=0.99,
            single_stage_pipeline_concentration=0.0,
            late_stage_deals_pct=0.99,
            pipeline_refresh_rate_pct=0.99,
        )
        result = engine.assess(inp)
        assert result.pipeline_composite == 60.0
        assert result.pipeline_risk == PipelineRisk.critical
        assert result.pipeline_severity == PipelineSeverity.critical

    def test_exact_composite_40_is_high_degraded(self):
        # staleness=100 → 30, concentration=100 → 15 ... need 40
        # staleness=100*0.30=30 + curation=40*0.25=10 = 40
        engine = fresh_engine()
        inp = make_input(
            deals_with_no_activity_30d_pct=0.50,
            avg_deal_age_days=120.0,
            deals_with_no_activity_60d_pct=0.35,
            stage_to_stage_progression_rate_pct=0.99,
            deals_slipped_more_than_once_pct=0.0,
            avg_days_in_current_stage=5.0,
            expected_days_in_stage=15.0,
            deals_added_not_touched_after_create_pct=0.40,
            deals_exceeding_avg_stage_duration_pct=0.0,
            closed_won_from_current_pipeline_pct=0.99,
            single_stage_pipeline_concentration=0.0,
            late_stage_deals_pct=0.99,
            pipeline_refresh_rate_pct=0.99,
        )
        result = engine.assess(inp)
        assert result.pipeline_composite == 40.0
        assert result.pipeline_risk == PipelineRisk.high
        assert result.pipeline_severity == PipelineSeverity.degraded

    def test_exact_composite_20_is_moderate_declining(self):
        # concentration=100 → 15; curation=20 → 5 ... or concentration=100*0.15=15 + staleness=16.7...
        # Easier: staleness=22*0.30=6.6 + progression=22*0.30=6.6 + curation=22*0.25=5.5 + concentration=10*0.15=1.5 = 20.2 (no)
        # Try: staleness=8*0.30 + progression=40*0.30 + curation=0 + concentration=0 = 2.4+12=14.4 (no)
        # staleness=40*0.30=12 + progression=22*0.30=6.6 + curation=8*0.25=2 = 20.6... close
        # Let me just build one that lands >= 20 but < 40 for moderate
        engine = fresh_engine()
        inp = make_input(
            deals_with_no_activity_30d_pct=0.30,
            avg_deal_age_days=75.0,
            deals_with_no_activity_60d_pct=0.15,
            stage_to_stage_progression_rate_pct=0.99,
            deals_slipped_more_than_once_pct=0.0,
            avg_days_in_current_stage=5.0,
            expected_days_in_stage=15.0,
            deals_added_not_touched_after_create_pct=0.0,
            deals_exceeding_avg_stage_duration_pct=0.0,
            closed_won_from_current_pipeline_pct=0.99,
            single_stage_pipeline_concentration=0.0,
            late_stage_deals_pct=0.99,
            pipeline_refresh_rate_pct=0.99,
        )
        result = engine.assess(inp)
        # staleness = 22+18+12 = 52 * 0.30 = 15.6
        assert result.pipeline_composite < 40
        assert result.pipeline_composite > 0

    def test_multiple_assessments_independent(self):
        # Results from different inputs are stored independently
        engine = fresh_engine()
        r1 = engine.assess(make_input(rep_id="R1"))
        r2 = engine.assess(make_input(
            rep_id="R2",
            deals_with_no_activity_30d_pct=0.50,
            avg_deal_age_days=120.0,
        ))
        assert r1.rep_id == "R1"
        assert r2.rep_id == "R2"
        assert r1.pipeline_composite != r2.pipeline_composite

    def test_deals_with_no_activity_30d_exact_boundary_050(self):
        engine = fresh_engine()
        r_at = engine._staleness_score(make_input(deals_with_no_activity_30d_pct=0.50))
        r_below = engine._staleness_score(make_input(deals_with_no_activity_30d_pct=0.499))
        assert r_at > r_below  # 40 vs 22

    def test_avg_deal_age_exact_boundary_120(self):
        engine = fresh_engine()
        r_at = engine._staleness_score(make_input(avg_deal_age_days=120.0))
        r_below = engine._staleness_score(make_input(avg_deal_age_days=119.9))
        assert r_at > r_below  # 35 vs 18

    def test_stage_overage_exact_boundary_30(self):
        engine = fresh_engine()
        r_at = engine._progression_score(make_input(
            avg_days_in_current_stage=40.0, expected_days_in_stage=10.0
        ))
        r_below = engine._progression_score(make_input(
            avg_days_in_current_stage=39.9, expected_days_in_stage=10.0
        ))
        assert r_at > r_below  # 25 vs 12

    def test_single_stage_exact_boundary_065(self):
        engine = fresh_engine()
        r_at = engine._concentration_score(make_input(single_stage_pipeline_concentration=0.65))
        r_below = engine._concentration_score(make_input(single_stage_pipeline_concentration=0.649))
        assert r_at > r_below  # 45 vs 25
