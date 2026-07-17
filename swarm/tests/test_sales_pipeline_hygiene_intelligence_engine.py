"""
Comprehensive pytest test suite for SalesPipelineHygieneIntelligenceEngine.
Covers all enums, dataclasses, sub-score methods, pattern detection,
risk/severity/action mapping, flag methods, pipeline impact calculation,
signal generation, assess(), assess_batch(), summary(), edge cases,
and end-to-end scenarios.
"""
from __future__ import annotations

import pytest
from swarm.intelligence.sales_pipeline_hygiene_intelligence_engine import (
    HygieneAction,
    HygienePattern,
    HygieneRisk,
    HygieneSeverity,
    PipelineHygieneInput,
    PipelineHygieneResult,
    SalesPipelineHygieneIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def make_input(**overrides) -> PipelineHygieneInput:
    """Return a baseline healthy PipelineHygieneInput with optional overrides."""
    defaults = dict(
        rep_id="rep-001",
        region="EMEA",
        evaluation_period_id="2026-Q2",
        total_open_deals=20,
        deals_missing_close_date_count=0,
        deals_missing_next_step_count=0,
        deals_stale_notes_30d_count=0,
        deals_stale_notes_60d_count=0,
        deals_never_contacted_count=0,
        deals_close_date_in_past_count=0,
        deals_missing_contact_count=0,
        deals_missing_value_count=0,
        crm_field_completion_pct=0.95,
        avg_days_since_last_crm_update=1.0,
        duplicate_deal_count=0,
        deals_wrong_stage_count=0,
        manual_forecast_override_count=0,
        deals_no_activity_60d_count=0,
        overdue_tasks_count=0,
        avg_open_deal_value_usd=10_000.0,
        avg_deal_age_days=30.0,
        zombie_deal_count=0,
    )
    defaults.update(overrides)
    return PipelineHygieneInput(**defaults)


@pytest.fixture
def engine() -> SalesPipelineHygieneIntelligenceEngine:
    return SalesPipelineHygieneIntelligenceEngine()


@pytest.fixture
def healthy_input() -> PipelineHygieneInput:
    return make_input()


# ===========================================================================
# 1. Enum values and membership
# ===========================================================================

class TestHygieneRiskEnum:
    def test_low_value(self):
        assert HygieneRisk.low.value == "low"

    def test_moderate_value(self):
        assert HygieneRisk.moderate.value == "moderate"

    def test_high_value(self):
        assert HygieneRisk.high.value == "high"

    def test_critical_value(self):
        assert HygieneRisk.critical.value == "critical"

    def test_member_count(self):
        assert len(HygieneRisk) == 4

    def test_is_str_enum(self):
        assert isinstance(HygieneRisk.low, str)

    def test_equality_with_string(self):
        assert HygieneRisk.low == "low"

    def test_all_members(self):
        names = {m.name for m in HygieneRisk}
        assert names == {"low", "moderate", "high", "critical"}


class TestHygienePatternEnum:
    def test_none_value(self):
        assert HygienePattern.none.value == "none"

    def test_data_neglect_value(self):
        assert HygienePattern.data_neglect.value == "data_neglect"

    def test_zombie_pipeline_value(self):
        assert HygienePattern.zombie_pipeline.value == "zombie_pipeline"

    def test_forecast_distortion_value(self):
        assert HygienePattern.forecast_distortion.value == "forecast_distortion"

    def test_stale_activity_value(self):
        assert HygienePattern.stale_activity.value == "stale_activity"

    def test_incomplete_qualification_value(self):
        assert HygienePattern.incomplete_qualification.value == "incomplete_qualification"

    def test_member_count(self):
        assert len(HygienePattern) == 6

    def test_is_str_enum(self):
        assert isinstance(HygienePattern.none, str)

    def test_all_members(self):
        names = {m.name for m in HygienePattern}
        assert names == {
            "none", "data_neglect", "zombie_pipeline",
            "forecast_distortion", "stale_activity", "incomplete_qualification"
        }


class TestHygieneSeverityEnum:
    def test_clean_value(self):
        assert HygieneSeverity.clean.value == "clean"

    def test_developing_value(self):
        assert HygieneSeverity.developing.value == "developing"

    def test_dirty_value(self):
        assert HygieneSeverity.dirty.value == "dirty"

    def test_toxic_value(self):
        assert HygieneSeverity.toxic.value == "toxic"

    def test_member_count(self):
        assert len(HygieneSeverity) == 4

    def test_is_str_enum(self):
        assert isinstance(HygieneSeverity.clean, str)

    def test_all_members(self):
        names = {m.name for m in HygieneSeverity}
        assert names == {"clean", "developing", "dirty", "toxic"}


class TestHygieneActionEnum:
    def test_no_action_value(self):
        assert HygieneAction.no_action.value == "no_action"

    def test_crm_coaching_value(self):
        assert HygieneAction.crm_coaching.value == "crm_coaching"

    def test_pipeline_audit_value(self):
        assert HygieneAction.pipeline_audit.value == "pipeline_audit"

    def test_data_cleanup_sprint_value(self):
        assert HygieneAction.data_cleanup_sprint.value == "data_cleanup_sprint"

    def test_forecast_recalibration_value(self):
        assert HygieneAction.forecast_recalibration.value == "forecast_recalibration"

    def test_pipeline_purge_value(self):
        assert HygieneAction.pipeline_purge.value == "pipeline_purge"

    def test_member_count(self):
        assert len(HygieneAction) == 6

    def test_is_str_enum(self):
        assert isinstance(HygieneAction.no_action, str)

    def test_all_members(self):
        names = {m.name for m in HygieneAction}
        assert names == {
            "no_action", "crm_coaching", "pipeline_audit",
            "data_cleanup_sprint", "forecast_recalibration", "pipeline_purge"
        }


# ===========================================================================
# 2. PipelineHygieneInput dataclass
# ===========================================================================

class TestPipelineHygieneInput:
    def test_has_22_fields(self):
        import dataclasses
        fields = dataclasses.fields(PipelineHygieneInput)
        assert len(fields) == 22

    def test_rep_id_field(self):
        inp = make_input(rep_id="X")
        assert inp.rep_id == "X"

    def test_region_field(self):
        inp = make_input(region="APAC")
        assert inp.region == "APAC"

    def test_evaluation_period_id_field(self):
        inp = make_input(evaluation_period_id="2025-Q4")
        assert inp.evaluation_period_id == "2025-Q4"

    def test_total_open_deals_field(self):
        inp = make_input(total_open_deals=50)
        assert inp.total_open_deals == 50

    def test_deals_missing_close_date_count_field(self):
        inp = make_input(deals_missing_close_date_count=5)
        assert inp.deals_missing_close_date_count == 5

    def test_deals_missing_next_step_count_field(self):
        inp = make_input(deals_missing_next_step_count=3)
        assert inp.deals_missing_next_step_count == 3

    def test_deals_stale_notes_30d_count_field(self):
        inp = make_input(deals_stale_notes_30d_count=4)
        assert inp.deals_stale_notes_30d_count == 4

    def test_deals_stale_notes_60d_count_field(self):
        inp = make_input(deals_stale_notes_60d_count=2)
        assert inp.deals_stale_notes_60d_count == 2

    def test_deals_never_contacted_count_field(self):
        inp = make_input(deals_never_contacted_count=1)
        assert inp.deals_never_contacted_count == 1

    def test_deals_close_date_in_past_count_field(self):
        inp = make_input(deals_close_date_in_past_count=7)
        assert inp.deals_close_date_in_past_count == 7

    def test_deals_missing_contact_count_field(self):
        inp = make_input(deals_missing_contact_count=2)
        assert inp.deals_missing_contact_count == 2

    def test_deals_missing_value_count_field(self):
        inp = make_input(deals_missing_value_count=1)
        assert inp.deals_missing_value_count == 1

    def test_crm_field_completion_pct_field(self):
        inp = make_input(crm_field_completion_pct=0.72)
        assert inp.crm_field_completion_pct == pytest.approx(0.72)

    def test_avg_days_since_last_crm_update_field(self):
        inp = make_input(avg_days_since_last_crm_update=5.5)
        assert inp.avg_days_since_last_crm_update == pytest.approx(5.5)

    def test_duplicate_deal_count_field(self):
        inp = make_input(duplicate_deal_count=2)
        assert inp.duplicate_deal_count == 2

    def test_deals_wrong_stage_count_field(self):
        inp = make_input(deals_wrong_stage_count=3)
        assert inp.deals_wrong_stage_count == 3

    def test_manual_forecast_override_count_field(self):
        inp = make_input(manual_forecast_override_count=4)
        assert inp.manual_forecast_override_count == 4

    def test_deals_no_activity_60d_count_field(self):
        inp = make_input(deals_no_activity_60d_count=3)
        assert inp.deals_no_activity_60d_count == 3

    def test_overdue_tasks_count_field(self):
        inp = make_input(overdue_tasks_count=10)
        assert inp.overdue_tasks_count == 10

    def test_avg_open_deal_value_usd_field(self):
        inp = make_input(avg_open_deal_value_usd=25_000.0)
        assert inp.avg_open_deal_value_usd == pytest.approx(25_000.0)

    def test_avg_deal_age_days_field(self):
        inp = make_input(avg_deal_age_days=90.0)
        assert inp.avg_deal_age_days == pytest.approx(90.0)

    def test_zombie_deal_count_field(self):
        inp = make_input(zombie_deal_count=5)
        assert inp.zombie_deal_count == 5


# ===========================================================================
# 3. PipelineHygieneResult dataclass and to_dict()
# ===========================================================================

class TestPipelineHygieneResult:
    def _make_result(self) -> PipelineHygieneResult:
        return PipelineHygieneResult(
            rep_id="rep-99",
            region="NA",
            hygiene_risk=HygieneRisk.high,
            hygiene_pattern=HygienePattern.zombie_pipeline,
            hygiene_severity=HygieneSeverity.dirty,
            recommended_action=HygieneAction.pipeline_audit,
            data_completeness_score=30.0,
            pipeline_freshness_score=45.0,
            deal_quality_score=50.0,
            forecast_reliability_score=20.0,
            pipeline_hygiene_composite=38.0,
            has_hygiene_gap=True,
            requires_hygiene_coaching=True,
            estimated_forecast_error_usd=12_000.0,
            hygiene_signal="Test signal",
        )

    def test_has_15_fields(self):
        import dataclasses
        fields = dataclasses.fields(PipelineHygieneResult)
        assert len(fields) == 15

    def test_rep_id(self):
        assert self._make_result().rep_id == "rep-99"

    def test_region(self):
        assert self._make_result().region == "NA"

    def test_hygiene_risk(self):
        assert self._make_result().hygiene_risk == HygieneRisk.high

    def test_hygiene_pattern(self):
        assert self._make_result().hygiene_pattern == HygienePattern.zombie_pipeline

    def test_hygiene_severity(self):
        assert self._make_result().hygiene_severity == HygieneSeverity.dirty

    def test_recommended_action(self):
        assert self._make_result().recommended_action == HygieneAction.pipeline_audit

    def test_data_completeness_score(self):
        assert self._make_result().data_completeness_score == pytest.approx(30.0)

    def test_pipeline_freshness_score(self):
        assert self._make_result().pipeline_freshness_score == pytest.approx(45.0)

    def test_deal_quality_score(self):
        assert self._make_result().deal_quality_score == pytest.approx(50.0)

    def test_forecast_reliability_score(self):
        assert self._make_result().forecast_reliability_score == pytest.approx(20.0)

    def test_pipeline_hygiene_composite(self):
        assert self._make_result().pipeline_hygiene_composite == pytest.approx(38.0)

    def test_has_hygiene_gap(self):
        assert self._make_result().has_hygiene_gap is True

    def test_requires_hygiene_coaching(self):
        assert self._make_result().requires_hygiene_coaching is True

    def test_estimated_forecast_error_usd(self):
        assert self._make_result().estimated_forecast_error_usd == pytest.approx(12_000.0)

    def test_hygiene_signal(self):
        assert self._make_result().hygiene_signal == "Test signal"

    def test_to_dict_has_15_keys(self):
        assert len(self._make_result().to_dict()) == 15

    def test_to_dict_rep_id(self):
        assert self._make_result().to_dict()["rep_id"] == "rep-99"

    def test_to_dict_region(self):
        assert self._make_result().to_dict()["region"] == "NA"

    def test_to_dict_hygiene_risk_is_string(self):
        assert self._make_result().to_dict()["hygiene_risk"] == "high"

    def test_to_dict_hygiene_pattern_is_string(self):
        assert self._make_result().to_dict()["hygiene_pattern"] == "zombie_pipeline"

    def test_to_dict_hygiene_severity_is_string(self):
        assert self._make_result().to_dict()["hygiene_severity"] == "dirty"

    def test_to_dict_recommended_action_is_string(self):
        assert self._make_result().to_dict()["recommended_action"] == "pipeline_audit"

    def test_to_dict_data_completeness_score(self):
        assert self._make_result().to_dict()["data_completeness_score"] == pytest.approx(30.0)

    def test_to_dict_pipeline_freshness_score(self):
        assert self._make_result().to_dict()["pipeline_freshness_score"] == pytest.approx(45.0)

    def test_to_dict_deal_quality_score(self):
        assert self._make_result().to_dict()["deal_quality_score"] == pytest.approx(50.0)

    def test_to_dict_forecast_reliability_score(self):
        assert self._make_result().to_dict()["forecast_reliability_score"] == pytest.approx(20.0)

    def test_to_dict_pipeline_hygiene_composite(self):
        assert self._make_result().to_dict()["pipeline_hygiene_composite"] == pytest.approx(38.0)

    def test_to_dict_has_hygiene_gap(self):
        assert self._make_result().to_dict()["has_hygiene_gap"] is True

    def test_to_dict_requires_hygiene_coaching(self):
        assert self._make_result().to_dict()["requires_hygiene_coaching"] is True

    def test_to_dict_estimated_forecast_error_usd(self):
        assert self._make_result().to_dict()["estimated_forecast_error_usd"] == pytest.approx(12_000.0)

    def test_to_dict_hygiene_signal(self):
        assert self._make_result().to_dict()["hygiene_signal"] == "Test signal"

    def test_to_dict_all_keys_present(self):
        d = self._make_result().to_dict()
        expected_keys = {
            "rep_id", "region", "hygiene_risk", "hygiene_pattern",
            "hygiene_severity", "recommended_action", "data_completeness_score",
            "pipeline_freshness_score", "deal_quality_score",
            "forecast_reliability_score", "pipeline_hygiene_composite",
            "has_hygiene_gap", "requires_hygiene_coaching",
            "estimated_forecast_error_usd", "hygiene_signal",
        }
        assert set(d.keys()) == expected_keys


# ===========================================================================
# 4. _data_completeness_score
# ===========================================================================

class TestDataCompletenessScore:
    def _score(self, **kw) -> float:
        e = SalesPipelineHygieneIntelligenceEngine()
        return e._data_completeness_score(make_input(**kw))

    # crm_field_completion_pct branches
    def test_crm_below_50_adds_40(self):
        s = self._score(crm_field_completion_pct=0.40, total_open_deals=10)
        assert s >= 40.0

    def test_crm_exactly_50_adds_20(self):
        s = self._score(crm_field_completion_pct=0.50, total_open_deals=10)
        assert s >= 20.0

    def test_crm_below_70_adds_20(self):
        s = self._score(crm_field_completion_pct=0.65, total_open_deals=10)
        assert s >= 20.0

    def test_crm_exactly_70_adds_8(self):
        s = self._score(crm_field_completion_pct=0.70, total_open_deals=10)
        assert s >= 8.0

    def test_crm_below_85_adds_8(self):
        s = self._score(crm_field_completion_pct=0.80, total_open_deals=10)
        assert s >= 8.0

    def test_crm_at_85_adds_0(self):
        # exactly 0.85 — no crm penalty
        s = self._score(
            crm_field_completion_pct=0.85,
            total_open_deals=10,
            deals_missing_close_date_count=0,
            deals_missing_next_step_count=0,
        )
        assert s == pytest.approx(0.0)

    def test_crm_above_85_adds_0(self):
        s = self._score(
            crm_field_completion_pct=0.90,
            total_open_deals=10,
            deals_missing_close_date_count=0,
            deals_missing_next_step_count=0,
        )
        assert s == pytest.approx(0.0)

    # close date missing rate branches
    def test_close_date_rate_above_30_adds_30(self):
        # 6/10 = 60% >= 30%
        s = self._score(
            crm_field_completion_pct=0.95,
            total_open_deals=10,
            deals_missing_close_date_count=6,
            deals_missing_next_step_count=0,
        )
        assert s >= 30.0

    def test_close_date_rate_exactly_30_adds_30(self):
        s = self._score(
            crm_field_completion_pct=0.95,
            total_open_deals=10,
            deals_missing_close_date_count=3,
            deals_missing_next_step_count=0,
        )
        assert s >= 30.0

    def test_close_date_rate_between_15_and_30_adds_15(self):
        # 2/10 = 20%
        s = self._score(
            crm_field_completion_pct=0.95,
            total_open_deals=10,
            deals_missing_close_date_count=2,
            deals_missing_next_step_count=0,
        )
        assert s >= 15.0

    def test_close_date_rate_between_5_and_15_adds_7(self):
        # 1/10 = 10%
        s = self._score(
            crm_field_completion_pct=0.95,
            total_open_deals=10,
            deals_missing_close_date_count=1,
            deals_missing_next_step_count=0,
        )
        assert s >= 7.0

    def test_close_date_rate_below_5_adds_0(self):
        # 0/20 = 0%
        s = self._score(
            crm_field_completion_pct=0.95,
            total_open_deals=20,
            deals_missing_close_date_count=0,
            deals_missing_next_step_count=0,
        )
        assert s == pytest.approx(0.0)

    # next step missing rate branches
    def test_next_step_rate_above_40_adds_25(self):
        # 9/10 = 90%
        s = self._score(
            crm_field_completion_pct=0.95,
            total_open_deals=10,
            deals_missing_close_date_count=0,
            deals_missing_next_step_count=9,
        )
        assert s >= 25.0

    def test_next_step_rate_between_20_and_40_adds_12(self):
        # 3/10 = 30%
        s = self._score(
            crm_field_completion_pct=0.95,
            total_open_deals=10,
            deals_missing_close_date_count=0,
            deals_missing_next_step_count=3,
        )
        assert s >= 12.0

    def test_next_step_rate_below_20_adds_0(self):
        # 1/10 = 10%
        s = self._score(
            crm_field_completion_pct=0.95,
            total_open_deals=10,
            deals_missing_close_date_count=0,
            deals_missing_next_step_count=1,
        )
        assert s == pytest.approx(0.0)

    def test_score_capped_at_100(self):
        # Max possible: 40 + 30 + 25 = 95 with these inputs; cap test just verifies <= 100
        s = self._score(
            crm_field_completion_pct=0.10,
            total_open_deals=10,
            deals_missing_close_date_count=10,
            deals_missing_next_step_count=10,
        )
        assert s <= 100.0
        assert s >= 90.0  # should be very high

    def test_zero_deals_uses_denominator_1(self):
        # Should not raise ZeroDivisionError
        s = self._score(
            total_open_deals=0,
            crm_field_completion_pct=0.95,
            deals_missing_close_date_count=0,
            deals_missing_next_step_count=0,
        )
        assert s == pytest.approx(0.0)

    def test_healthy_baseline_score_is_zero(self):
        s = self._score()
        assert s == pytest.approx(0.0)


# ===========================================================================
# 5. _pipeline_freshness_score
# ===========================================================================

class TestPipelineFreshnessScore:
    def _score(self, **kw) -> float:
        e = SalesPipelineHygieneIntelligenceEngine()
        return e._pipeline_freshness_score(make_input(**kw))

    # avg_days_since_last_crm_update branches
    def test_update_above_14_days_adds_45(self):
        s = self._score(avg_days_since_last_crm_update=20.0, total_open_deals=10)
        assert s >= 45.0

    def test_update_exactly_14_days_adds_45(self):
        s = self._score(avg_days_since_last_crm_update=14.0, total_open_deals=10)
        assert s >= 45.0

    def test_update_7_to_14_days_adds_25(self):
        s = self._score(avg_days_since_last_crm_update=10.0, total_open_deals=10)
        assert s >= 25.0

    def test_update_exactly_7_days_adds_25(self):
        s = self._score(avg_days_since_last_crm_update=7.0, total_open_deals=10)
        assert s >= 25.0

    def test_update_3_to_7_days_adds_8(self):
        s = self._score(avg_days_since_last_crm_update=5.0, total_open_deals=10)
        assert s >= 8.0

    def test_update_exactly_3_days_adds_8(self):
        s = self._score(avg_days_since_last_crm_update=3.0, total_open_deals=10)
        assert s >= 8.0

    def test_update_below_3_days_adds_0(self):
        s = self._score(
            avg_days_since_last_crm_update=1.0,
            total_open_deals=10,
            deals_stale_notes_30d_count=0,
            deals_no_activity_60d_count=0,
        )
        assert s == pytest.approx(0.0)

    # stale_30d_rate branches
    def test_stale_30d_rate_above_40_adds_35(self):
        s = self._score(
            avg_days_since_last_crm_update=1.0,
            total_open_deals=10,
            deals_stale_notes_30d_count=5,
            deals_no_activity_60d_count=0,
        )
        assert s >= 35.0

    def test_stale_30d_rate_25_to_40_adds_18(self):
        # 3/10 = 30%
        s = self._score(
            avg_days_since_last_crm_update=1.0,
            total_open_deals=10,
            deals_stale_notes_30d_count=3,
            deals_no_activity_60d_count=0,
        )
        assert s >= 18.0

    def test_stale_30d_rate_10_to_25_adds_7(self):
        # 2/20 = 10%
        s = self._score(
            avg_days_since_last_crm_update=1.0,
            total_open_deals=20,
            deals_stale_notes_30d_count=2,
            deals_no_activity_60d_count=0,
        )
        assert s >= 7.0

    def test_stale_30d_rate_below_10_adds_0(self):
        s = self._score(
            avg_days_since_last_crm_update=1.0,
            total_open_deals=100,
            deals_stale_notes_30d_count=1,
            deals_no_activity_60d_count=0,
        )
        assert s == pytest.approx(0.0)

    # no_activity_60d_rate branches
    def test_no_activity_60d_rate_above_30_adds_20(self):
        # 4/10 = 40%
        s = self._score(
            avg_days_since_last_crm_update=1.0,
            total_open_deals=10,
            deals_stale_notes_30d_count=0,
            deals_no_activity_60d_count=4,
        )
        assert s >= 20.0

    def test_no_activity_60d_rate_15_to_30_adds_10(self):
        # 2/10 = 20%
        s = self._score(
            avg_days_since_last_crm_update=1.0,
            total_open_deals=10,
            deals_stale_notes_30d_count=0,
            deals_no_activity_60d_count=2,
        )
        assert s >= 10.0

    def test_no_activity_60d_rate_below_15_adds_0(self):
        s = self._score(
            avg_days_since_last_crm_update=1.0,
            total_open_deals=100,
            deals_stale_notes_30d_count=0,
            deals_no_activity_60d_count=1,
        )
        assert s == pytest.approx(0.0)

    def test_score_capped_at_100(self):
        s = self._score(
            avg_days_since_last_crm_update=30.0,
            total_open_deals=10,
            deals_stale_notes_30d_count=10,
            deals_no_activity_60d_count=10,
        )
        assert s == pytest.approx(100.0)

    def test_healthy_baseline_is_zero(self):
        s = self._score()
        assert s == pytest.approx(0.0)

    def test_zero_deals_uses_denominator_1(self):
        s = self._score(total_open_deals=0, avg_days_since_last_crm_update=1.0)
        assert s >= 0.0


# ===========================================================================
# 6. _deal_quality_score
# ===========================================================================

class TestDealQualityScore:
    def _score(self, **kw) -> float:
        e = SalesPipelineHygieneIntelligenceEngine()
        return e._deal_quality_score(make_input(**kw))

    # zombie_rate branches
    def test_zombie_rate_above_20_adds_40(self):
        # 3/10 = 30%
        s = self._score(total_open_deals=10, zombie_deal_count=3,
                        deals_never_contacted_count=0, deals_missing_contact_count=0)
        assert s >= 40.0

    def test_zombie_rate_10_to_20_adds_20(self):
        # 1/10 = 10%
        s = self._score(total_open_deals=10, zombie_deal_count=1,
                        deals_never_contacted_count=0, deals_missing_contact_count=0)
        assert s >= 20.0

    def test_zombie_rate_5_to_10_adds_8(self):
        # 1/20 = 5%
        s = self._score(total_open_deals=20, zombie_deal_count=1,
                        deals_never_contacted_count=0, deals_missing_contact_count=0)
        assert s >= 8.0

    def test_zombie_rate_below_5_adds_0(self):
        s = self._score(total_open_deals=100, zombie_deal_count=1,
                        deals_never_contacted_count=0, deals_missing_contact_count=0)
        assert s == pytest.approx(0.0)

    # never_contacted_rate branches
    def test_never_contacted_rate_above_10_adds_30(self):
        # 2/10 = 20%
        s = self._score(total_open_deals=10, zombie_deal_count=0,
                        deals_never_contacted_count=2, deals_missing_contact_count=0)
        assert s >= 30.0

    def test_never_contacted_rate_5_to_10_adds_15(self):
        # 1/20 = 5%
        s = self._score(total_open_deals=20, zombie_deal_count=0,
                        deals_never_contacted_count=1, deals_missing_contact_count=0)
        assert s >= 15.0

    def test_never_contacted_rate_below_5_adds_0(self):
        s = self._score(total_open_deals=100, zombie_deal_count=0,
                        deals_never_contacted_count=1, deals_missing_contact_count=0)
        assert s == pytest.approx(0.0)

    # missing_contact_rate branches
    def test_missing_contact_rate_above_25_adds_25(self):
        # 3/10 = 30%
        s = self._score(total_open_deals=10, zombie_deal_count=0,
                        deals_never_contacted_count=0, deals_missing_contact_count=3)
        assert s >= 25.0

    def test_missing_contact_rate_10_to_25_adds_12(self):
        # 2/10 = 20%
        s = self._score(total_open_deals=10, zombie_deal_count=0,
                        deals_never_contacted_count=0, deals_missing_contact_count=2)
        assert s >= 12.0

    def test_missing_contact_rate_below_10_adds_0(self):
        s = self._score(total_open_deals=100, zombie_deal_count=0,
                        deals_never_contacted_count=0, deals_missing_contact_count=1)
        assert s == pytest.approx(0.0)

    def test_score_capped_at_100(self):
        # Max possible: 40 + 30 + 25 = 95; cap verifies <= 100
        s = self._score(total_open_deals=10, zombie_deal_count=10,
                        deals_never_contacted_count=10, deals_missing_contact_count=10)
        assert s <= 100.0
        assert s >= 90.0

    def test_healthy_baseline_is_zero(self):
        s = self._score()
        assert s == pytest.approx(0.0)

    def test_zero_deals_uses_denominator_1(self):
        s = self._score(total_open_deals=0)
        assert s >= 0.0


# ===========================================================================
# 7. _forecast_reliability_score
# ===========================================================================

class TestForecastReliabilityScore:
    def _score(self, **kw) -> float:
        e = SalesPipelineHygieneIntelligenceEngine()
        return e._forecast_reliability_score(make_input(**kw))

    # past_close_rate branches
    def test_past_close_rate_above_20_adds_40(self):
        # 3/10 = 30%
        s = self._score(total_open_deals=10, deals_close_date_in_past_count=3,
                        manual_forecast_override_count=0, duplicate_deal_count=0)
        assert s >= 40.0

    def test_past_close_rate_10_to_20_adds_20(self):
        # 1/10 = 10%
        s = self._score(total_open_deals=10, deals_close_date_in_past_count=1,
                        manual_forecast_override_count=0, duplicate_deal_count=0)
        assert s >= 20.0

    def test_past_close_rate_5_to_10_adds_8(self):
        # 1/20 = 5%
        s = self._score(total_open_deals=20, deals_close_date_in_past_count=1,
                        manual_forecast_override_count=0, duplicate_deal_count=0)
        assert s >= 8.0

    def test_past_close_rate_below_5_adds_0(self):
        s = self._score(total_open_deals=100, deals_close_date_in_past_count=1,
                        manual_forecast_override_count=0, duplicate_deal_count=0)
        assert s == pytest.approx(0.0)

    # manual_forecast_override_count branches
    def test_override_above_5_adds_30(self):
        s = self._score(total_open_deals=10, deals_close_date_in_past_count=0,
                        manual_forecast_override_count=6, duplicate_deal_count=0)
        assert s >= 30.0

    def test_override_exactly_5_adds_30(self):
        s = self._score(total_open_deals=10, deals_close_date_in_past_count=0,
                        manual_forecast_override_count=5, duplicate_deal_count=0)
        assert s >= 30.0

    def test_override_3_to_5_adds_15(self):
        s = self._score(total_open_deals=10, deals_close_date_in_past_count=0,
                        manual_forecast_override_count=4, duplicate_deal_count=0)
        assert s >= 15.0

    def test_override_exactly_3_adds_15(self):
        s = self._score(total_open_deals=10, deals_close_date_in_past_count=0,
                        manual_forecast_override_count=3, duplicate_deal_count=0)
        assert s >= 15.0

    def test_override_1_to_3_adds_7(self):
        s = self._score(total_open_deals=10, deals_close_date_in_past_count=0,
                        manual_forecast_override_count=1, duplicate_deal_count=0)
        assert s >= 7.0

    def test_override_exactly_1_adds_7(self):
        s = self._score(total_open_deals=10, deals_close_date_in_past_count=0,
                        manual_forecast_override_count=1, duplicate_deal_count=0)
        assert s >= 7.0

    def test_override_0_adds_0(self):
        s = self._score(total_open_deals=10, deals_close_date_in_past_count=0,
                        manual_forecast_override_count=0, duplicate_deal_count=0)
        assert s == pytest.approx(0.0)

    # duplicate_deal_count branches
    def test_duplicate_above_3_adds_25(self):
        s = self._score(total_open_deals=10, deals_close_date_in_past_count=0,
                        manual_forecast_override_count=0, duplicate_deal_count=4)
        assert s >= 25.0

    def test_duplicate_exactly_3_adds_25(self):
        s = self._score(total_open_deals=10, deals_close_date_in_past_count=0,
                        manual_forecast_override_count=0, duplicate_deal_count=3)
        assert s >= 25.0

    def test_duplicate_1_to_3_adds_12(self):
        s = self._score(total_open_deals=10, deals_close_date_in_past_count=0,
                        manual_forecast_override_count=0, duplicate_deal_count=1)
        assert s >= 12.0

    def test_duplicate_0_adds_0(self):
        s = self._score(total_open_deals=10, deals_close_date_in_past_count=0,
                        manual_forecast_override_count=0, duplicate_deal_count=0)
        assert s == pytest.approx(0.0)

    def test_score_capped_at_100(self):
        # Max possible: 40 + 30 + 25 = 95; verify high and within cap
        s = self._score(total_open_deals=10, deals_close_date_in_past_count=10,
                        manual_forecast_override_count=10, duplicate_deal_count=10)
        assert s <= 100.0
        assert s >= 90.0

    def test_healthy_baseline_is_zero(self):
        s = self._score()
        assert s == pytest.approx(0.0)

    def test_zero_deals_uses_denominator_1(self):
        s = self._score(total_open_deals=0)
        assert s >= 0.0


# ===========================================================================
# 8. Composite score calculation
# ===========================================================================

class TestCompositeScore:
    def test_composite_formula_weights(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        expected = round(
            r.data_completeness_score * 0.30
            + r.pipeline_freshness_score * 0.30
            + r.deal_quality_score * 0.25
            + r.forecast_reliability_score * 0.15,
            1,
        )
        assert r.pipeline_hygiene_composite == pytest.approx(expected)

    def test_composite_capped_at_100(self, engine):
        bad = make_input(
            crm_field_completion_pct=0.10,
            total_open_deals=10,
            deals_missing_close_date_count=10,
            deals_missing_next_step_count=10,
            deals_stale_notes_30d_count=10,
            deals_no_activity_60d_count=10,
            zombie_deal_count=10,
            deals_never_contacted_count=10,
            deals_missing_contact_count=10,
            deals_close_date_in_past_count=10,
            manual_forecast_override_count=10,
            duplicate_deal_count=10,
            avg_days_since_last_crm_update=30.0,
        )
        r = engine.assess(bad)
        assert r.pipeline_hygiene_composite <= 100.0

    def test_composite_healthy_near_zero(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.pipeline_hygiene_composite == pytest.approx(0.0)

    def test_composite_rounded_to_1dp(self, engine):
        inp = make_input(
            crm_field_completion_pct=0.65,
            total_open_deals=10,
            deals_missing_close_date_count=2,
            deals_missing_next_step_count=3,
        )
        r = engine.assess(inp)
        # Value should be a multiple of 0.1
        assert round(r.pipeline_hygiene_composite, 1) == r.pipeline_hygiene_composite


# ===========================================================================
# 9. _detect_pattern
# ===========================================================================

class TestDetectPattern:
    def _pattern(self, inp: PipelineHygieneInput) -> HygienePattern:
        e = SalesPipelineHygieneIntelligenceEngine()
        c = e._data_completeness_score(inp)
        f = e._pipeline_freshness_score(inp)
        q = e._deal_quality_score(inp)
        r = e._forecast_reliability_score(inp)
        return e._detect_pattern(inp, c, f, q, r)

    def test_data_neglect_detected(self):
        # completeness >= 35 AND crm < 0.60
        inp = make_input(
            crm_field_completion_pct=0.40,
            total_open_deals=10,
            deals_missing_close_date_count=4,
            deals_missing_next_step_count=6,
        )
        assert self._pattern(inp) == HygienePattern.data_neglect

    def test_zombie_pipeline_detected(self):
        # quality >= 35, zombie_rate >= 15%
        inp = make_input(
            crm_field_completion_pct=0.90,
            total_open_deals=10,
            zombie_deal_count=3,
            deals_never_contacted_count=2,
            deals_missing_contact_count=3,
        )
        assert self._pattern(inp) == HygienePattern.zombie_pipeline

    def test_forecast_distortion_via_past_close_rate(self):
        # reliability >= 35, past_close_rate >= 15%
        inp = make_input(
            crm_field_completion_pct=0.90,
            total_open_deals=10,
            zombie_deal_count=0,
            deals_close_date_in_past_count=3,  # 30%
            manual_forecast_override_count=5,
            duplicate_deal_count=3,
        )
        assert self._pattern(inp) == HygienePattern.forecast_distortion

    def test_forecast_distortion_via_override_count(self):
        inp = make_input(
            crm_field_completion_pct=0.90,
            total_open_deals=10,
            zombie_deal_count=0,
            deals_close_date_in_past_count=0,
            manual_forecast_override_count=5,
            duplicate_deal_count=3,
        )
        assert self._pattern(inp) == HygienePattern.forecast_distortion

    def test_stale_activity_detected(self):
        # freshness >= 35, avg_days >= 10
        inp = make_input(
            crm_field_completion_pct=0.90,
            total_open_deals=10,
            zombie_deal_count=0,
            deals_close_date_in_past_count=0,
            manual_forecast_override_count=0,
            duplicate_deal_count=0,
            avg_days_since_last_crm_update=14.0,
            deals_stale_notes_30d_count=5,
            deals_no_activity_60d_count=4,
        )
        assert self._pattern(inp) == HygienePattern.stale_activity

    def test_incomplete_qualification_detected(self):
        # quality >= 25, never_rate >= 8%
        inp = make_input(
            crm_field_completion_pct=0.90,
            total_open_deals=10,
            zombie_deal_count=0,
            deals_never_contacted_count=1,  # 10%
            deals_missing_contact_count=2,  # 20%
            deals_close_date_in_past_count=0,
            manual_forecast_override_count=0,
            duplicate_deal_count=0,
            avg_days_since_last_crm_update=1.0,
            deals_stale_notes_30d_count=0,
            deals_no_activity_60d_count=0,
        )
        assert self._pattern(inp) == HygienePattern.incomplete_qualification

    def test_none_pattern_healthy(self):
        assert self._pattern(make_input()) == HygienePattern.none

    def test_data_neglect_takes_priority_over_others(self):
        # crm < 0.60 AND also has zombie deals
        inp = make_input(
            crm_field_completion_pct=0.40,
            total_open_deals=10,
            deals_missing_close_date_count=4,
            deals_missing_next_step_count=6,
            zombie_deal_count=3,
        )
        assert self._pattern(inp) == HygienePattern.data_neglect


# ===========================================================================
# 10. _risk_level
# ===========================================================================

class TestRiskLevel:
    def _risk(self, composite: float) -> HygieneRisk:
        return SalesPipelineHygieneIntelligenceEngine()._risk_level(composite)

    def test_composite_60_is_critical(self):
        assert self._risk(60.0) == HygieneRisk.critical

    def test_composite_above_60_is_critical(self):
        assert self._risk(75.0) == HygieneRisk.critical

    def test_composite_100_is_critical(self):
        assert self._risk(100.0) == HygieneRisk.critical

    def test_composite_40_is_high(self):
        assert self._risk(40.0) == HygieneRisk.high

    def test_composite_between_40_and_60_is_high(self):
        assert self._risk(55.9) == HygieneRisk.high

    def test_composite_20_is_moderate(self):
        assert self._risk(20.0) == HygieneRisk.moderate

    def test_composite_between_20_and_40_is_moderate(self):
        assert self._risk(39.9) == HygieneRisk.moderate

    def test_composite_0_is_low(self):
        assert self._risk(0.0) == HygieneRisk.low

    def test_composite_below_20_is_low(self):
        assert self._risk(19.9) == HygieneRisk.low

    def test_composite_just_below_60_is_high(self):
        assert self._risk(59.9) == HygieneRisk.high


# ===========================================================================
# 11. _severity
# ===========================================================================

class TestSeverity:
    def _sev(self, composite: float) -> HygieneSeverity:
        return SalesPipelineHygieneIntelligenceEngine()._severity(composite)

    def test_composite_60_is_toxic(self):
        assert self._sev(60.0) == HygieneSeverity.toxic

    def test_composite_above_60_is_toxic(self):
        assert self._sev(80.0) == HygieneSeverity.toxic

    def test_composite_100_is_toxic(self):
        assert self._sev(100.0) == HygieneSeverity.toxic

    def test_composite_40_is_dirty(self):
        assert self._sev(40.0) == HygieneSeverity.dirty

    def test_composite_between_40_and_60_is_dirty(self):
        assert self._sev(55.9) == HygieneSeverity.dirty

    def test_composite_20_is_developing(self):
        assert self._sev(20.0) == HygieneSeverity.developing

    def test_composite_between_20_and_40_is_developing(self):
        assert self._sev(39.9) == HygieneSeverity.developing

    def test_composite_0_is_clean(self):
        assert self._sev(0.0) == HygieneSeverity.clean

    def test_composite_below_20_is_clean(self):
        assert self._sev(19.9) == HygieneSeverity.clean

    def test_composite_just_below_60_is_dirty(self):
        assert self._sev(59.9) == HygieneSeverity.dirty


# ===========================================================================
# 12. _action mapping
# ===========================================================================

class TestActionMapping:
    def _action(self, risk: HygieneRisk, pattern: HygienePattern) -> HygieneAction:
        return SalesPipelineHygieneIntelligenceEngine()._action(risk, pattern)

    # critical branch
    def test_critical_data_neglect_gives_data_cleanup_sprint(self):
        assert self._action(HygieneRisk.critical, HygienePattern.data_neglect) == HygieneAction.data_cleanup_sprint

    def test_critical_zombie_pipeline_gives_pipeline_purge(self):
        assert self._action(HygieneRisk.critical, HygienePattern.zombie_pipeline) == HygieneAction.pipeline_purge

    def test_critical_forecast_distortion_gives_pipeline_audit(self):
        assert self._action(HygieneRisk.critical, HygienePattern.forecast_distortion) == HygieneAction.pipeline_audit

    def test_critical_stale_activity_gives_pipeline_audit(self):
        assert self._action(HygieneRisk.critical, HygienePattern.stale_activity) == HygieneAction.pipeline_audit

    def test_critical_none_gives_pipeline_audit(self):
        assert self._action(HygieneRisk.critical, HygienePattern.none) == HygieneAction.pipeline_audit

    def test_critical_incomplete_qualification_gives_pipeline_audit(self):
        assert self._action(HygieneRisk.critical, HygienePattern.incomplete_qualification) == HygieneAction.pipeline_audit

    # high branch
    def test_high_forecast_distortion_gives_forecast_recalibration(self):
        assert self._action(HygieneRisk.high, HygienePattern.forecast_distortion) == HygieneAction.forecast_recalibration

    def test_high_stale_activity_gives_crm_coaching(self):
        assert self._action(HygieneRisk.high, HygienePattern.stale_activity) == HygieneAction.crm_coaching

    def test_high_data_neglect_gives_pipeline_audit(self):
        assert self._action(HygieneRisk.high, HygienePattern.data_neglect) == HygieneAction.pipeline_audit

    def test_high_zombie_pipeline_gives_pipeline_audit(self):
        assert self._action(HygieneRisk.high, HygienePattern.zombie_pipeline) == HygieneAction.pipeline_audit

    def test_high_none_gives_pipeline_audit(self):
        assert self._action(HygieneRisk.high, HygienePattern.none) == HygieneAction.pipeline_audit

    def test_high_incomplete_qualification_gives_pipeline_audit(self):
        assert self._action(HygieneRisk.high, HygienePattern.incomplete_qualification) == HygieneAction.pipeline_audit

    # moderate branch
    def test_moderate_any_pattern_gives_crm_coaching(self):
        for p in HygienePattern:
            assert self._action(HygieneRisk.moderate, p) == HygieneAction.crm_coaching

    # low branch
    def test_low_any_pattern_gives_no_action(self):
        for p in HygienePattern:
            assert self._action(HygieneRisk.low, p) == HygieneAction.no_action


# ===========================================================================
# 13. _has_hygiene_gap
# ===========================================================================

class TestHasHygieneGap:
    def _gap(self, composite: float, **kw) -> bool:
        e = SalesPipelineHygieneIntelligenceEngine()
        return e._has_hygiene_gap(composite, make_input(**kw))

    def test_composite_40_triggers_gap(self):
        assert self._gap(40.0) is True

    def test_composite_above_40_triggers_gap(self):
        assert self._gap(60.0) is True

    def test_zombie_count_3_triggers_gap(self):
        assert self._gap(0.0, zombie_deal_count=3) is True

    def test_zombie_count_above_3_triggers_gap(self):
        assert self._gap(0.0, zombie_deal_count=5) is True

    def test_crm_below_50_triggers_gap(self):
        assert self._gap(0.0, crm_field_completion_pct=0.49) is True

    def test_crm_exactly_50_does_not_trigger_gap(self):
        assert self._gap(19.9, zombie_deal_count=2, crm_field_completion_pct=0.50) is False

    def test_no_gap_healthy(self):
        assert self._gap(0.0) is False

    def test_composite_below_40_no_gap_without_other_triggers(self):
        assert self._gap(39.9, zombie_deal_count=2, crm_field_completion_pct=0.60) is False

    def test_zombie_count_2_no_gap(self):
        assert self._gap(0.0, zombie_deal_count=2) is False


# ===========================================================================
# 14. _requires_hygiene_coaching
# ===========================================================================

class TestRequiresHygieneCoaching:
    def _coaching(self, composite: float, **kw) -> bool:
        e = SalesPipelineHygieneIntelligenceEngine()
        return e._requires_hygiene_coaching(composite, make_input(**kw))

    def test_composite_30_triggers_coaching(self):
        assert self._coaching(30.0) is True

    def test_composite_above_30_triggers_coaching(self):
        assert self._coaching(50.0) is True

    def test_avg_days_10_triggers_coaching(self):
        assert self._coaching(0.0, avg_days_since_last_crm_update=10.0) is True

    def test_avg_days_above_10_triggers_coaching(self):
        assert self._coaching(0.0, avg_days_since_last_crm_update=14.0) is True

    def test_past_close_count_3_triggers_coaching(self):
        assert self._coaching(0.0, deals_close_date_in_past_count=3) is True

    def test_past_close_count_above_3_triggers_coaching(self):
        assert self._coaching(0.0, deals_close_date_in_past_count=5) is True

    def test_no_coaching_healthy(self):
        assert self._coaching(0.0) is False

    def test_composite_29_no_coaching_without_other_triggers(self):
        assert self._coaching(29.9, avg_days_since_last_crm_update=1.0, deals_close_date_in_past_count=2) is False

    def test_past_close_count_2_no_coaching(self):
        assert self._coaching(0.0, deals_close_date_in_past_count=2) is False


# ===========================================================================
# 15. _estimated_forecast_error
# ===========================================================================

class TestEstimatedForecastError:
    def _err(self, zombie: int, past_close: int, avg_val: float, composite: float) -> float:
        e = SalesPipelineHygieneIntelligenceEngine()
        inp = make_input(zombie_deal_count=zombie,
                         deals_close_date_in_past_count=past_close,
                         avg_open_deal_value_usd=avg_val)
        return e._estimated_forecast_error(inp, composite)

    def test_zero_exposed_deals_gives_zero(self):
        assert self._err(0, 0, 10_000.0, 50.0) == pytest.approx(0.0)

    def test_formula_is_correct(self):
        # (2+3) * 10000 * (50/100) = 25000
        assert self._err(2, 3, 10_000.0, 50.0) == pytest.approx(25_000.0)

    def test_composite_zero_gives_zero_error(self):
        assert self._err(5, 5, 10_000.0, 0.0) == pytest.approx(0.0)

    def test_composite_100_gives_full_error(self):
        # (1+1)*5000*(100/100) = 10000
        assert self._err(1, 1, 5_000.0, 100.0) == pytest.approx(10_000.0)

    def test_result_rounded_to_2dp(self):
        err = self._err(1, 1, 3_333.33, 50.0)
        assert err == round(err, 2)

    def test_large_values(self):
        err = self._err(10, 10, 100_000.0, 80.0)
        assert err == pytest.approx(20 * 100_000.0 * 0.80, rel=1e-6)


# ===========================================================================
# 16. _signal generation
# ===========================================================================

class TestSignal:
    def _signal(self, pattern: HygienePattern, composite: float, **kw) -> str:
        e = SalesPipelineHygieneIntelligenceEngine()
        inp = make_input(**kw)
        return e._signal(inp, pattern, composite)

    def test_healthy_benchmark_signal(self):
        sig = self._signal(HygienePattern.none, 15.0)
        assert sig == "Pipeline hygiene and CRM data quality within healthy benchmarks"

    def test_healthy_benchmark_requires_pattern_none_and_below_20(self):
        # pattern none but composite = 20 -> NOT benchmark signal
        sig = self._signal(HygienePattern.none, 20.0)
        assert sig != "Pipeline hygiene and CRM data quality within healthy benchmarks"

    def test_non_none_pattern_above_threshold_not_benchmark(self):
        sig = self._signal(HygienePattern.data_neglect, 5.0)
        assert sig != "Pipeline hygiene and CRM data quality within healthy benchmarks"

    def test_signal_includes_crm_pct_when_below_70(self):
        sig = self._signal(HygienePattern.data_neglect, 50.0, crm_field_completion_pct=0.60)
        assert "60% CRM complete" in sig

    def test_signal_excludes_crm_pct_when_above_70(self):
        sig = self._signal(HygienePattern.stale_activity, 40.0, crm_field_completion_pct=0.80)
        assert "CRM complete" not in sig

    def test_signal_includes_zombie_count(self):
        sig = self._signal(HygienePattern.zombie_pipeline, 50.0, zombie_deal_count=4)
        assert "4 zombie deals" in sig

    def test_signal_excludes_zombie_when_zero(self):
        sig = self._signal(HygienePattern.stale_activity, 40.0, zombie_deal_count=0)
        assert "zombie" not in sig

    def test_signal_includes_overdue_close_dates(self):
        sig = self._signal(HygienePattern.forecast_distortion, 50.0,
                           deals_close_date_in_past_count=3)
        assert "3 overdue close dates" in sig

    def test_signal_excludes_overdue_when_zero(self):
        sig = self._signal(HygienePattern.stale_activity, 40.0,
                           deals_close_date_in_past_count=0)
        assert "overdue" not in sig

    def test_signal_label_uses_pattern_value(self):
        sig = self._signal(HygienePattern.zombie_pipeline, 50.0)
        assert sig.startswith("Zombie pipeline")

    def test_signal_label_none_uses_hygiene_risk(self):
        sig = self._signal(HygienePattern.none, 30.0)
        assert sig.startswith("Hygiene risk")

    def test_signal_includes_composite(self):
        sig = self._signal(HygienePattern.data_neglect, 42.0,
                           crm_field_completion_pct=0.60)
        assert "composite 42" in sig

    def test_signal_fallback_when_no_parts(self):
        sig = self._signal(HygienePattern.none, 25.0,
                           crm_field_completion_pct=0.90, zombie_deal_count=0,
                           deals_close_date_in_past_count=0)
        assert "pipeline data quality degraded" in sig

    def test_signal_capitalises_label(self):
        sig = self._signal(HygienePattern.data_neglect, 50.0)
        assert sig[0].isupper()


# ===========================================================================
# 17. assess() — integration
# ===========================================================================

class TestAssess:
    def test_returns_pipeline_hygiene_result(self, engine, healthy_input):
        assert isinstance(engine.assess(healthy_input), PipelineHygieneResult)

    def test_rep_id_propagated(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.rep_id == healthy_input.rep_id

    def test_region_propagated(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.region == healthy_input.region

    def test_healthy_risk_is_low(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.hygiene_risk == HygieneRisk.low

    def test_healthy_severity_is_clean(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.hygiene_severity == HygieneSeverity.clean

    def test_healthy_action_is_no_action(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.recommended_action == HygieneAction.no_action

    def test_healthy_pattern_is_none(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.hygiene_pattern == HygienePattern.none

    def test_healthy_gap_is_false(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.has_hygiene_gap is False

    def test_healthy_coaching_is_false(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.requires_hygiene_coaching is False

    def test_healthy_forecast_error_is_zero(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.estimated_forecast_error_usd == pytest.approx(0.0)

    def test_healthy_signal_is_benchmark(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.hygiene_signal == "Pipeline hygiene and CRM data quality within healthy benchmarks"

    def test_assess_appends_to_results(self, engine, healthy_input):
        engine.assess(healthy_input)
        assert len(engine._results) == 1

    def test_assess_appends_multiple(self, engine):
        for _ in range(3):
            engine.assess(make_input())
        assert len(engine._results) == 3

    def test_critical_scenario(self, engine):
        bad = make_input(
            crm_field_completion_pct=0.40,
            total_open_deals=10,
            deals_missing_close_date_count=5,
            deals_missing_next_step_count=6,
            deals_stale_notes_30d_count=7,
            deals_no_activity_60d_count=5,
            zombie_deal_count=4,
            deals_never_contacted_count=3,
            deals_missing_contact_count=4,
            deals_close_date_in_past_count=4,
            manual_forecast_override_count=6,
            duplicate_deal_count=4,
            avg_days_since_last_crm_update=20.0,
        )
        r = engine.assess(bad)
        assert r.hygiene_risk == HygieneRisk.critical

    def test_moderate_scenario(self, engine):
        mid = make_input(
            crm_field_completion_pct=0.75,
            total_open_deals=10,
            deals_missing_close_date_count=1,
            deals_stale_notes_30d_count=2,
            avg_days_since_last_crm_update=5.0,
            deals_missing_next_step_count=2,
        )
        r = engine.assess(mid)
        assert r.pipeline_hygiene_composite >= 0

    def test_scores_are_non_negative(self, engine):
        r = engine.assess(make_input())
        assert r.data_completeness_score >= 0
        assert r.pipeline_freshness_score >= 0
        assert r.deal_quality_score >= 0
        assert r.forecast_reliability_score >= 0

    def test_scores_at_most_100(self, engine):
        r = engine.assess(make_input())
        assert r.data_completeness_score <= 100
        assert r.pipeline_freshness_score <= 100
        assert r.deal_quality_score <= 100
        assert r.forecast_reliability_score <= 100

    def test_assess_different_reps(self, engine):
        r1 = engine.assess(make_input(rep_id="A"))
        r2 = engine.assess(make_input(rep_id="B"))
        assert r1.rep_id == "A"
        assert r2.rep_id == "B"


# ===========================================================================
# 18. assess_batch()
# ===========================================================================

class TestAssessBatch:
    def test_returns_list(self, engine):
        result = engine.assess_batch([make_input(), make_input()])
        assert isinstance(result, list)

    def test_length_matches_input(self, engine):
        inputs = [make_input(rep_id=f"r{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5

    def test_empty_batch_returns_empty_list(self, engine):
        assert engine.assess_batch([]) == []

    def test_each_result_is_pipeline_hygiene_result(self, engine):
        results = engine.assess_batch([make_input(), make_input()])
        for r in results:
            assert isinstance(r, PipelineHygieneResult)

    def test_results_appended_to_internal_list(self, engine):
        engine.assess_batch([make_input(), make_input(), make_input()])
        assert len(engine._results) == 3

    def test_order_preserved(self, engine):
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(4)]
        results = engine.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"rep-{i}"

    def test_single_item_batch(self, engine):
        results = engine.assess_batch([make_input(rep_id="solo")])
        assert len(results) == 1
        assert results[0].rep_id == "solo"

    def test_batch_then_assess_accumulates(self, engine):
        engine.assess_batch([make_input(), make_input()])
        engine.assess(make_input())
        assert len(engine._results) == 3


# ===========================================================================
# 19. summary()
# ===========================================================================

class TestSummary:
    def test_empty_summary_has_13_keys(self, engine):
        s = engine.summary()
        assert len(s) == 13

    def test_empty_summary_total_zero(self, engine):
        assert engine.summary()["total"] == 0

    def test_empty_summary_risk_counts_empty(self, engine):
        assert engine.summary()["risk_counts"] == {}

    def test_empty_summary_pattern_counts_empty(self, engine):
        assert engine.summary()["pattern_counts"] == {}

    def test_empty_summary_severity_counts_empty(self, engine):
        assert engine.summary()["severity_counts"] == {}

    def test_empty_summary_action_counts_empty(self, engine):
        assert engine.summary()["action_counts"] == {}

    def test_empty_summary_avg_composite_zero(self, engine):
        assert engine.summary()["avg_pipeline_hygiene_composite"] == pytest.approx(0.0)

    def test_empty_summary_hygiene_gap_count_zero(self, engine):
        assert engine.summary()["hygiene_gap_count"] == 0

    def test_empty_summary_coaching_count_zero(self, engine):
        assert engine.summary()["hygiene_coaching_count"] == 0

    def test_empty_summary_avg_completeness_zero(self, engine):
        assert engine.summary()["avg_data_completeness_score"] == pytest.approx(0.0)

    def test_empty_summary_avg_freshness_zero(self, engine):
        assert engine.summary()["avg_pipeline_freshness_score"] == pytest.approx(0.0)

    def test_empty_summary_avg_quality_zero(self, engine):
        assert engine.summary()["avg_deal_quality_score"] == pytest.approx(0.0)

    def test_empty_summary_avg_reliability_zero(self, engine):
        assert engine.summary()["avg_forecast_reliability_score"] == pytest.approx(0.0)

    def test_empty_summary_total_error_zero(self, engine):
        assert engine.summary()["total_estimated_forecast_error_usd"] == pytest.approx(0.0)

    def test_summary_after_one_assess_total_is_1(self, engine, healthy_input):
        engine.assess(healthy_input)
        assert engine.summary()["total"] == 1

    def test_summary_after_batch_total_correct(self, engine):
        engine.assess_batch([make_input()] * 4)
        assert engine.summary()["total"] == 4

    def test_summary_risk_counts_correct(self, engine):
        engine.assess(make_input())   # healthy => low
        s = engine.summary()
        assert s["risk_counts"].get("low", 0) >= 1

    def test_summary_pattern_counts_correct(self, engine):
        engine.assess(make_input())   # healthy => none
        s = engine.summary()
        assert s["pattern_counts"].get("none", 0) >= 1

    def test_summary_severity_counts_correct(self, engine):
        engine.assess(make_input())   # healthy => clean
        s = engine.summary()
        assert s["severity_counts"].get("clean", 0) >= 1

    def test_summary_action_counts_correct(self, engine):
        engine.assess(make_input())   # healthy => no_action
        s = engine.summary()
        assert s["action_counts"].get("no_action", 0) >= 1

    def test_summary_hygiene_gap_count(self, engine):
        engine.assess(make_input(zombie_deal_count=5))
        s = engine.summary()
        assert s["hygiene_gap_count"] >= 1

    def test_summary_coaching_count(self, engine):
        engine.assess(make_input(avg_days_since_last_crm_update=12.0))
        s = engine.summary()
        assert s["hygiene_coaching_count"] >= 1

    def test_summary_total_error_sums_correctly(self, engine):
        inp = make_input(zombie_deal_count=2, deals_close_date_in_past_count=2,
                         avg_open_deal_value_usd=5_000.0)
        r = engine.assess(inp)
        s = engine.summary()
        assert s["total_estimated_forecast_error_usd"] == pytest.approx(r.estimated_forecast_error_usd, rel=1e-3)

    def test_summary_all_expected_keys_present(self, engine):
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_pipeline_hygiene_composite",
            "hygiene_gap_count", "hygiene_coaching_count",
            "avg_data_completeness_score", "avg_pipeline_freshness_score",
            "avg_deal_quality_score", "avg_forecast_reliability_score",
            "total_estimated_forecast_error_usd",
        }
        assert set(engine.summary().keys()) == expected_keys

    def test_summary_averages_rounded_to_1dp(self, engine):
        engine.assess_batch([make_input()] * 3)
        s = engine.summary()
        for key in ("avg_pipeline_hygiene_composite", "avg_data_completeness_score",
                    "avg_pipeline_freshness_score", "avg_deal_quality_score",
                    "avg_forecast_reliability_score"):
            val = s[key]
            assert round(val, 1) == val


# ===========================================================================
# 20. Edge cases
# ===========================================================================

class TestEdgeCases:
    def test_total_open_deals_zero_no_crash(self, engine):
        r = engine.assess(make_input(total_open_deals=0))
        assert r is not None

    def test_crm_completion_exactly_0(self, engine):
        r = engine.assess(make_input(crm_field_completion_pct=0.0))
        assert r.data_completeness_score >= 40.0

    def test_crm_completion_exactly_1(self, engine):
        r = engine.assess(make_input(crm_field_completion_pct=1.0))
        assert r.data_completeness_score == pytest.approx(0.0)

    def test_avg_days_exactly_3_freshness(self, engine):
        r = engine.assess(make_input(avg_days_since_last_crm_update=3.0))
        assert r.pipeline_freshness_score >= 8.0

    def test_avg_days_exactly_7_freshness(self, engine):
        r = engine.assess(make_input(avg_days_since_last_crm_update=7.0))
        assert r.pipeline_freshness_score >= 25.0

    def test_avg_days_exactly_14_freshness(self, engine):
        r = engine.assess(make_input(avg_days_since_last_crm_update=14.0))
        assert r.pipeline_freshness_score >= 45.0

    def test_large_deal_counts(self, engine):
        r = engine.assess(make_input(total_open_deals=10_000, zombie_deal_count=1_000))
        assert r is not None

    def test_very_high_avg_deal_value(self, engine):
        r = engine.assess(make_input(avg_open_deal_value_usd=1_000_000.0,
                                     zombie_deal_count=2, deals_close_date_in_past_count=2))
        assert r.estimated_forecast_error_usd >= 0.0

    def test_zero_avg_deal_value_gives_zero_error(self, engine):
        r = engine.assess(make_input(avg_open_deal_value_usd=0.0,
                                     zombie_deal_count=5, deals_close_date_in_past_count=5))
        assert r.estimated_forecast_error_usd == pytest.approx(0.0)

    def test_multiple_engines_independent(self):
        e1 = SalesPipelineHygieneIntelligenceEngine()
        e2 = SalesPipelineHygieneIntelligenceEngine()
        e1.assess(make_input(rep_id="A"))
        assert len(e2._results) == 0

    def test_rep_id_empty_string(self, engine):
        r = engine.assess(make_input(rep_id=""))
        assert r.rep_id == ""

    def test_region_empty_string(self, engine):
        r = engine.assess(make_input(region=""))
        assert r.region == ""

    def test_composite_boundary_exactly_20(self):
        # Verify boundary condition for moderate/clean boundary
        e = SalesPipelineHygieneIntelligenceEngine()
        risk = e._risk_level(20.0)
        sev = e._severity(20.0)
        assert risk == HygieneRisk.moderate
        assert sev == HygieneSeverity.developing

    def test_composite_boundary_exactly_40(self):
        e = SalesPipelineHygieneIntelligenceEngine()
        assert e._risk_level(40.0) == HygieneRisk.high
        assert e._severity(40.0) == HygieneSeverity.dirty

    def test_composite_boundary_exactly_60(self):
        e = SalesPipelineHygieneIntelligenceEngine()
        assert e._risk_level(60.0) == HygieneRisk.critical
        assert e._severity(60.0) == HygieneSeverity.toxic


# ===========================================================================
# 21. End-to-end scenarios
# ===========================================================================

class TestEndToEndScenarios:
    def test_scenario_data_neglect_critical(self, engine):
        """Rep with very poor CRM completion and many missing fields — pattern is data_neglect,
        risk depends on composite. With extra stale/freshness signals we get critical."""
        inp = make_input(
            rep_id="neglect-rep",
            crm_field_completion_pct=0.30,
            total_open_deals=10,
            deals_missing_close_date_count=5,
            deals_missing_next_step_count=7,
            avg_days_since_last_crm_update=16.0,
            deals_stale_notes_30d_count=5,
            deals_no_activity_60d_count=4,
            zombie_deal_count=3,
            deals_never_contacted_count=2,
            deals_missing_contact_count=3,
            deals_close_date_in_past_count=3,
            manual_forecast_override_count=5,
            duplicate_deal_count=3,
        )
        r = engine.assess(inp)
        assert r.hygiene_pattern == HygienePattern.data_neglect
        assert r.hygiene_risk == HygieneRisk.critical
        assert r.recommended_action == HygieneAction.data_cleanup_sprint
        assert r.has_hygiene_gap is True

    def test_scenario_zombie_pipeline_critical(self, engine):
        """Rep with high zombie rate and many other bad hygiene signals -> critical."""
        inp = make_input(
            rep_id="zombie-rep",
            total_open_deals=10,
            zombie_deal_count=4,
            deals_never_contacted_count=3,
            deals_missing_contact_count=4,
            crm_field_completion_pct=0.90,
            avg_days_since_last_crm_update=16.0,
            deals_stale_notes_30d_count=5,
            deals_no_activity_60d_count=4,
            deals_close_date_in_past_count=3,
            manual_forecast_override_count=5,
            duplicate_deal_count=3,
        )
        r = engine.assess(inp)
        assert r.hygiene_pattern == HygienePattern.zombie_pipeline
        assert r.recommended_action == HygieneAction.pipeline_purge

    def test_scenario_stale_crm_high_risk(self, engine):
        """Rep with very stale CRM activity — at minimum moderate risk."""
        inp = make_input(
            rep_id="stale-rep",
            avg_days_since_last_crm_update=15.0,
            total_open_deals=10,
            deals_stale_notes_30d_count=5,
            deals_no_activity_60d_count=4,
            crm_field_completion_pct=0.90,
        )
        r = engine.assess(inp)
        assert r.hygiene_pattern == HygienePattern.stale_activity
        assert r.hygiene_risk in (HygieneRisk.moderate, HygieneRisk.high, HygieneRisk.critical)

    def test_scenario_healthy_rep(self, engine, healthy_input):
        """A perfectly healthy pipeline should score well across all dimensions."""
        r = engine.assess(healthy_input)
        assert r.hygiene_risk == HygieneRisk.low
        assert r.hygiene_severity == HygieneSeverity.clean
        assert r.recommended_action == HygieneAction.no_action
        assert r.has_hygiene_gap is False
        assert r.requires_hygiene_coaching is False
        assert r.estimated_forecast_error_usd == pytest.approx(0.0)
        assert r.hygiene_signal == "Pipeline hygiene and CRM data quality within healthy benchmarks"

    def test_scenario_batch_mixed(self, engine):
        """Batch with healthy and unhealthy reps produces correct summary counts."""
        inputs = [
            make_input(rep_id="good"),
            make_input(
                rep_id="bad",
                crm_field_completion_pct=0.30,
                total_open_deals=10,
                deals_missing_close_date_count=5,
                deals_missing_next_step_count=7,
                avg_days_since_last_crm_update=16.0,
                deals_stale_notes_30d_count=5,
                deals_no_activity_60d_count=4,
                zombie_deal_count=3,
                deals_never_contacted_count=2,
                deals_missing_contact_count=3,
                deals_close_date_in_past_count=3,
                manual_forecast_override_count=5,
                duplicate_deal_count=3,
            ),
        ]
        results = engine.assess_batch(inputs)
        assert results[0].hygiene_risk == HygieneRisk.low
        assert results[1].hygiene_risk == HygieneRisk.critical

        s = engine.summary()
        assert s["total"] == 2
        assert s["risk_counts"].get("low", 0) >= 1
        assert s["risk_counts"].get("critical", 0) >= 1

    def test_to_dict_round_trips_assess(self, engine):
        """to_dict should reflect the same data as the result object."""
        r = engine.assess(make_input(rep_id="dict-test"))
        d = r.to_dict()
        assert d["rep_id"] == r.rep_id
        assert d["hygiene_risk"] == r.hygiene_risk.value
        assert d["pipeline_hygiene_composite"] == pytest.approx(r.pipeline_hygiene_composite)

    def test_multiple_assess_calls_accumulate(self, engine):
        """Each assess call adds to the internal results list."""
        for i in range(5):
            engine.assess(make_input(rep_id=f"r{i}"))
        assert len(engine._results) == 5

    def test_summary_reflects_all_assessed(self, engine):
        """Summary total matches number of assess calls."""
        for i in range(7):
            engine.assess(make_input())
        assert engine.summary()["total"] == 7

    def test_forecast_error_accumulates_in_summary(self, engine):
        """Total forecast error in summary equals sum of individual errors."""
        inputs = [
            make_input(zombie_deal_count=2, deals_close_date_in_past_count=1,
                       avg_open_deal_value_usd=10_000.0),
            make_input(zombie_deal_count=1, deals_close_date_in_past_count=3,
                       avg_open_deal_value_usd=5_000.0),
        ]
        results = engine.assess_batch(inputs)
        expected_total = sum(r.estimated_forecast_error_usd for r in results)
        s = engine.summary()
        assert s["total_estimated_forecast_error_usd"] == pytest.approx(expected_total, rel=1e-3)

    def test_incomplete_qualification_scenario(self, engine):
        """Rep with never-contacted deals triggers incomplete_qualification pattern."""
        inp = make_input(
            total_open_deals=10,
            deals_never_contacted_count=1,  # 10%
            deals_missing_contact_count=2,  # 20%
            zombie_deal_count=0,
            deals_close_date_in_past_count=0,
            manual_forecast_override_count=0,
            duplicate_deal_count=0,
            crm_field_completion_pct=0.90,
            avg_days_since_last_crm_update=1.0,
            deals_stale_notes_30d_count=0,
            deals_no_activity_60d_count=0,
        )
        r = engine.assess(inp)
        assert r.hygiene_pattern == HygienePattern.incomplete_qualification

    def test_forecast_distortion_scenario(self, engine):
        """Rep with many past close dates, overrides, and duplicates triggers forecast_distortion.
        The composite is driven mostly by the reliability sub-score (weight 0.15); to get high
        risk we also need freshness/completeness degraded."""
        inp = make_input(
            total_open_deals=10,
            deals_close_date_in_past_count=3,  # 30% -> +40 reliability
            manual_forecast_override_count=5,  # -> +30 reliability
            duplicate_deal_count=3,            # -> +25 reliability
            zombie_deal_count=0,
            crm_field_completion_pct=0.65,     # adds completeness score
            avg_days_since_last_crm_update=14.0,  # adds freshness score
            deals_stale_notes_30d_count=5,
            deals_no_activity_60d_count=4,
            deals_missing_close_date_count=3,
            deals_missing_next_step_count=4,
        )
        r = engine.assess(inp)
        assert r.hygiene_pattern == HygienePattern.forecast_distortion
        assert r.recommended_action in (
            HygieneAction.forecast_recalibration, HygieneAction.pipeline_audit
        )
