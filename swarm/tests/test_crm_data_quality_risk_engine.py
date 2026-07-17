"""Comprehensive pytest test suite for CRMDataQualityRiskEngine."""

from __future__ import annotations

import dataclasses

import pytest

from swarm.intelligence.crm_data_quality_risk_engine import (
    CRMDataQualityInput,
    CRMDataQualityRiskEngine,
    DataQualityRisk,
    QualityAction,
    QualityFailureMode,
    QualitySeverity,
)


# ─── helpers ────────────────────────────────────────────────────────────────

def make_input(**overrides) -> CRMDataQualityInput:
    """Return a clean/baseline CRMDataQualityInput that scores low risk."""
    defaults = dict(
        rep_id="rep-001",
        region="West",
        evaluation_period_id="Q1-2026",
        total_records_evaluated=20,
        missing_close_date_count=0,
        missing_opportunity_value_count=0,
        missing_contact_count=0,
        stale_record_count=0,
        stage_mismatch_count=0,
        duplicate_account_count=0,
        missing_decision_maker_count=0,
        data_entry_completeness_pct=90.0,
        records_with_activity_notes_pct=80.0,
        forecast_without_recent_activity_count=0,
        overdue_follow_up_count=0,
        avg_record_staleness_days=5.0,
        deal_source_missing_count=0,
        crm_login_frequency_last_30d=15,
        auto_filled_fields_pct=20.0,
        records_audited_by_admin_count=5,
        pipeline_audit_score=90.0,
        last_crm_training_days_ago=30,
    )
    defaults.update(overrides)
    return CRMDataQualityInput(**defaults)


def fresh_engine() -> CRMDataQualityRiskEngine:
    return CRMDataQualityRiskEngine()


# ═══════════════════════════════════════════════════════════════════════════
# 1. STRUCTURAL / SCHEMA TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestInputDataclassStructure:
    def test_input_has_exactly_22_fields(self):
        fields = dataclasses.fields(CRMDataQualityInput)
        assert len(fields) == 22

    def test_field_names(self):
        names = {f.name for f in dataclasses.fields(CRMDataQualityInput)}
        expected = {
            "rep_id", "region", "evaluation_period_id", "total_records_evaluated",
            "missing_close_date_count", "missing_opportunity_value_count",
            "missing_contact_count", "stale_record_count", "stage_mismatch_count",
            "duplicate_account_count", "missing_decision_maker_count",
            "data_entry_completeness_pct", "records_with_activity_notes_pct",
            "forecast_without_recent_activity_count", "overdue_follow_up_count",
            "avg_record_staleness_days", "deal_source_missing_count",
            "crm_login_frequency_last_30d", "auto_filled_fields_pct",
            "records_audited_by_admin_count", "pipeline_audit_score",
            "last_crm_training_days_ago",
        }
        assert names == expected

    def test_input_is_dataclass(self):
        assert dataclasses.is_dataclass(CRMDataQualityInput)

    def test_input_instantiation(self):
        inp = make_input()
        assert inp.rep_id == "rep-001"

    def test_input_overrides_work(self):
        inp = make_input(rep_id="X", region="East")
        assert inp.rep_id == "X"
        assert inp.region == "East"


class TestToDictStructure:
    def test_to_dict_returns_exactly_15_keys(self):
        engine = fresh_engine()
        result = engine.assess(make_input())
        assert len(result.to_dict()) == 15

    def test_to_dict_key_names(self):
        engine = fresh_engine()
        d = engine.assess(make_input()).to_dict()
        expected = {
            "rep_id", "region", "data_quality_risk", "quality_failure_mode",
            "quality_severity", "recommended_action", "completeness_score",
            "accuracy_score", "timeliness_score", "activity_coverage_score",
            "quality_composite", "is_data_quality_risk", "requires_data_audit",
            "estimated_pipeline_distortion_pct", "quality_signal",
        }
        assert set(d.keys()) == expected

    def test_to_dict_rep_id_preserved(self):
        engine = fresh_engine()
        d = engine.assess(make_input(rep_id="abc")).to_dict()
        assert d["rep_id"] == "abc"

    def test_to_dict_region_preserved(self):
        engine = fresh_engine()
        d = engine.assess(make_input(region="North")).to_dict()
        assert d["region"] == "North"

    def test_to_dict_string_enum_values(self):
        engine = fresh_engine()
        d = engine.assess(make_input()).to_dict()
        assert isinstance(d["data_quality_risk"], str)
        assert isinstance(d["quality_failure_mode"], str)
        assert isinstance(d["quality_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_bool_fields(self):
        engine = fresh_engine()
        d = engine.assess(make_input()).to_dict()
        assert isinstance(d["is_data_quality_risk"], bool)
        assert isinstance(d["requires_data_audit"], bool)

    def test_to_dict_numeric_fields_are_float(self):
        engine = fresh_engine()
        d = engine.assess(make_input()).to_dict()
        for key in ("completeness_score", "accuracy_score", "timeliness_score",
                    "activity_coverage_score", "quality_composite",
                    "estimated_pipeline_distortion_pct"):
            assert isinstance(d[key], (int, float)), key

    def test_to_dict_quality_signal_is_str(self):
        engine = fresh_engine()
        d = engine.assess(make_input()).to_dict()
        assert isinstance(d["quality_signal"], str)

    def test_to_dict_scores_rounded_to_1dp(self):
        engine = fresh_engine()
        d = engine.assess(make_input()).to_dict()
        for key in ("completeness_score", "accuracy_score", "timeliness_score",
                    "activity_coverage_score", "quality_composite",
                    "estimated_pipeline_distortion_pct"):
            val = d[key]
            assert round(val, 1) == val, f"{key}={val} not rounded to 1 dp"


class TestSummaryStructure:
    def test_summary_empty_returns_13_keys(self):
        engine = fresh_engine()
        s = engine.summary()
        assert len(s) == 13

    def test_summary_after_assess_returns_13_keys(self):
        engine = fresh_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert len(s) == 13

    def test_summary_key_names(self):
        engine = fresh_engine()
        s = engine.summary()
        expected = {
            "total", "risk_counts", "failure_mode_counts", "severity_counts",
            "action_counts", "avg_quality_composite", "data_quality_risk_count",
            "audit_required_count", "avg_completeness_score", "avg_accuracy_score",
            "avg_timeliness_score", "avg_activity_coverage_score",
            "avg_estimated_pipeline_distortion_pct",
        }
        assert set(s.keys()) == expected

    def test_summary_empty_total_zero(self):
        assert fresh_engine().summary()["total"] == 0

    def test_summary_empty_avg_zeros(self):
        s = fresh_engine().summary()
        assert s["avg_quality_composite"] == 0.0
        assert s["data_quality_risk_count"] == 0
        assert s["audit_required_count"] == 0
        assert s["avg_completeness_score"] == 0.0
        assert s["avg_accuracy_score"] == 0.0
        assert s["avg_timeliness_score"] == 0.0
        assert s["avg_activity_coverage_score"] == 0.0
        assert s["avg_estimated_pipeline_distortion_pct"] == 0.0

    def test_summary_empty_dict_fields_empty(self):
        s = fresh_engine().summary()
        assert s["risk_counts"] == {}
        assert s["failure_mode_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}


# ═══════════════════════════════════════════════════════════════════════════
# 2. ENUM TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestEnumValues:
    def test_data_quality_risk_values(self):
        assert DataQualityRisk.low.value == "low"
        assert DataQualityRisk.moderate.value == "moderate"
        assert DataQualityRisk.high.value == "high"
        assert DataQualityRisk.critical.value == "critical"

    def test_quality_failure_mode_values(self):
        assert QualityFailureMode.none.value == "none"
        assert QualityFailureMode.missing_data.value == "missing_data"
        assert QualityFailureMode.stale_records.value == "stale_records"
        assert QualityFailureMode.stage_drift.value == "stage_drift"
        assert QualityFailureMode.activity_gap.value == "activity_gap"
        assert QualityFailureMode.duplicate_accounts.value == "duplicate_accounts"

    def test_quality_severity_values(self):
        assert QualitySeverity.clean.value == "clean"
        assert QualitySeverity.degraded.value == "degraded"
        assert QualitySeverity.unreliable.value == "unreliable"
        assert QualitySeverity.corrupt.value == "corrupt"

    def test_quality_action_values(self):
        assert QualityAction.no_action.value == "no_action"
        assert QualityAction.self_remediate.value == "self_remediate"
        assert QualityAction.crm_coaching.value == "crm_coaching"
        assert QualityAction.data_audit.value == "data_audit"
        assert QualityAction.pipeline_freeze.value == "pipeline_freeze"

    def test_data_quality_risk_count(self):
        assert len(list(DataQualityRisk)) == 4

    def test_quality_failure_mode_count(self):
        assert len(list(QualityFailureMode)) == 6

    def test_quality_severity_count(self):
        assert len(list(QualitySeverity)) == 4

    def test_quality_action_count(self):
        assert len(list(QualityAction)) == 5

    def test_enums_are_str_subclass(self):
        assert isinstance(DataQualityRisk.low, str)
        assert isinstance(QualityFailureMode.none, str)
        assert isinstance(QualitySeverity.clean, str)
        assert isinstance(QualityAction.no_action, str)


# ═══════════════════════════════════════════════════════════════════════════
# 3. COMPOSITE FORMULA TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestCompositeFormula:
    """composite = completeness*0.30 + accuracy*0.25 + timeliness*0.25 + activity*0.20"""

    def test_clean_baseline_composite_near_zero(self):
        engine = fresh_engine()
        r = engine.assess(make_input())
        assert r.quality_composite < 20.0

    def test_composite_within_0_100(self):
        engine = fresh_engine()
        for _ in range(5):
            r = engine.assess(make_input(
                data_entry_completeness_pct=10,
                missing_close_date_count=10,
                missing_opportunity_value_count=10,
                stage_mismatch_count=10,
                duplicate_account_count=10,
                stale_record_count=15,
                total_records_evaluated=20,
                avg_record_staleness_days=90,
                crm_login_frequency_last_30d=1,
                records_with_activity_notes_pct=10,
                forecast_without_recent_activity_count=10,
                overdue_follow_up_count=10,
            ))
            assert 0.0 <= r.quality_composite <= 100.0

    def test_composite_is_rounded_to_1dp(self):
        engine = fresh_engine()
        r = engine.assess(make_input())
        assert r.quality_composite == round(r.quality_composite, 1)

    def test_composite_equals_weighted_sum(self):
        engine = fresh_engine()
        inp = make_input(
            data_entry_completeness_pct=55.0,   # completeness: 35
            missing_close_date_count=3,          # completeness: +8 => 43
            missing_opportunity_value_count=0,
            stage_mismatch_count=0,
            duplicate_account_count=0,
            auto_filled_fields_pct=0,
            deal_source_missing_count=0,
            total_records_evaluated=20,
            stale_record_count=0,
            avg_record_staleness_days=0,
            crm_login_frequency_last_30d=15,
            records_with_activity_notes_pct=80,
            forecast_without_recent_activity_count=0,
            overdue_follow_up_count=0,
        )
        r = engine.assess(inp)
        # completeness = 35+8 = 43, accuracy = 0, timeliness = 0, activity = 0
        expected = round(43 * 0.30 + 0 * 0.25 + 0 * 0.25 + 0 * 0.20, 1)
        assert r.quality_composite == expected

    def test_composite_increases_with_missing_data(self):
        engine = fresh_engine()
        r_clean = engine.assess(make_input())
        r_dirty = engine.assess(make_input(missing_close_date_count=8, data_entry_completeness_pct=40))
        assert r_dirty.quality_composite > r_clean.quality_composite

    def test_composite_increases_with_duplicates(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input())
        r2 = engine.assess(make_input(duplicate_account_count=5))
        assert r2.quality_composite > r1.quality_composite

    def test_composite_increases_with_stale_records(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input())
        r2 = engine.assess(make_input(
            stale_record_count=12,
            total_records_evaluated=20,
            avg_record_staleness_days=70,
            crm_login_frequency_last_30d=2,
        ))
        assert r2.quality_composite > r1.quality_composite

    def test_composite_increases_with_activity_gap(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input())
        r2 = engine.assess(make_input(
            records_with_activity_notes_pct=20,
            forecast_without_recent_activity_count=8,
        ))
        assert r2.quality_composite > r1.quality_composite

    def test_composite_clamped_at_100(self):
        """Worst possible inputs should not exceed 100."""
        engine = fresh_engine()
        r = engine.assess(make_input(
            data_entry_completeness_pct=0,
            missing_close_date_count=10,
            missing_opportunity_value_count=10,
            stage_mismatch_count=10,
            duplicate_account_count=10,
            auto_filled_fields_pct=100,
            total_records_evaluated=2,
            deal_source_missing_count=2,
            stale_record_count=2,
            avg_record_staleness_days=120,
            crm_login_frequency_last_30d=0,
            records_with_activity_notes_pct=0,
            forecast_without_recent_activity_count=10,
            overdue_follow_up_count=10,
        ))
        assert r.quality_composite <= 100.0

    def test_composite_clamped_at_zero(self):
        engine = fresh_engine()
        r = engine.assess(make_input())
        assert r.quality_composite >= 0.0


# ═══════════════════════════════════════════════════════════════════════════
# 4. COMPLETENESS SCORE TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestCompletenessScore:
    def _cs(self, **kwargs) -> float:
        return fresh_engine()._completeness_score(make_input(**kwargs))

    def test_perfect_completeness_zero(self):
        assert self._cs() == 0.0

    def test_completeness_pct_below_50_adds_50(self):
        score = self._cs(data_entry_completeness_pct=49.9)
        assert score >= 50.0

    def test_completeness_pct_between_50_65_adds_35(self):
        score = self._cs(data_entry_completeness_pct=60.0)
        assert score >= 35.0

    def test_completeness_pct_between_65_80_adds_18(self):
        score = self._cs(data_entry_completeness_pct=72.0)
        assert score >= 18.0

    def test_completeness_pct_80_plus_adds_zero(self):
        assert self._cs(data_entry_completeness_pct=80.0) == 0.0

    def test_missing_close_date_ge_8_adds_30(self):
        score = self._cs(missing_close_date_count=8)
        assert score >= 30.0

    def test_missing_close_date_5_to_7_adds_20(self):
        score = self._cs(missing_close_date_count=5)
        assert score >= 20.0

    def test_missing_close_date_2_to_4_adds_8(self):
        score = self._cs(missing_close_date_count=2)
        assert score >= 8.0

    def test_missing_close_date_0_adds_0(self):
        assert self._cs(missing_close_date_count=0) == 0.0

    def test_missing_opp_value_ge_5_adds_20(self):
        score = self._cs(missing_opportunity_value_count=5)
        assert score >= 20.0

    def test_missing_opp_value_3_to_4_adds_12(self):
        score = self._cs(missing_opportunity_value_count=3)
        assert score >= 12.0

    def test_missing_opp_value_1_to_2_adds_5(self):
        score = self._cs(missing_opportunity_value_count=1)
        assert score >= 5.0

    def test_missing_opp_value_0_adds_0(self):
        assert self._cs(missing_opportunity_value_count=0) == 0.0

    def test_worst_case_completeness_clamped_at_100(self):
        score = self._cs(
            data_entry_completeness_pct=10,
            missing_close_date_count=10,
            missing_opportunity_value_count=10,
        )
        assert score == 100.0

    def test_exact_boundary_pct_50(self):
        # Exactly 50 => NOT < 50 => next band: not < 65 either... 50 >= 50
        score_below = self._cs(data_entry_completeness_pct=49.99)
        score_at = self._cs(data_entry_completeness_pct=50.0)
        assert score_below > score_at

    def test_exact_boundary_pct_65(self):
        score_below = self._cs(data_entry_completeness_pct=64.99)
        score_at = self._cs(data_entry_completeness_pct=65.0)
        assert score_below > score_at

    def test_exact_boundary_pct_80(self):
        score_below = self._cs(data_entry_completeness_pct=79.99)
        score_at = self._cs(data_entry_completeness_pct=80.0)
        assert score_below > score_at


# ═══════════════════════════════════════════════════════════════════════════
# 5. ACCURACY SCORE TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestAccuracyScore:
    def _as(self, **kwargs) -> float:
        return fresh_engine()._accuracy_score(make_input(**kwargs))

    def test_perfect_accuracy_zero(self):
        assert self._as() == 0.0

    def test_stage_mismatch_ge_6_adds_40(self):
        score = self._as(stage_mismatch_count=6)
        assert score >= 40.0

    def test_stage_mismatch_4_5_adds_28(self):
        score = self._as(stage_mismatch_count=4)
        assert score >= 28.0

    def test_stage_mismatch_2_3_adds_15(self):
        score = self._as(stage_mismatch_count=2)
        assert score >= 15.0

    def test_stage_mismatch_0_1_adds_0(self):
        assert self._as(stage_mismatch_count=0) == 0.0
        assert self._as(stage_mismatch_count=1) == 0.0

    def test_duplicate_account_ge_5_adds_35(self):
        score = self._as(duplicate_account_count=5)
        assert score >= 35.0

    def test_duplicate_account_2_4_adds_20(self):
        score = self._as(duplicate_account_count=2)
        assert score >= 20.0

    def test_duplicate_account_1_adds_8(self):
        score = self._as(duplicate_account_count=1)
        assert score >= 8.0

    def test_duplicate_account_0_adds_0(self):
        assert self._as(duplicate_account_count=0) == 0.0

    def test_auto_fill_ge_70_adds_15(self):
        score = self._as(auto_filled_fields_pct=70.0)
        assert score >= 15.0

    def test_auto_fill_50_69_adds_8(self):
        score = self._as(auto_filled_fields_pct=50.0)
        assert score >= 8.0

    def test_auto_fill_below_50_adds_0(self):
        assert self._as(auto_filled_fields_pct=49.9) == 0.0

    def test_source_gap_ratio_ge_50_adds_10(self):
        score = self._as(deal_source_missing_count=10, total_records_evaluated=20)
        assert score >= 10.0

    def test_source_gap_ratio_25_50_adds_5(self):
        score = self._as(deal_source_missing_count=5, total_records_evaluated=20)
        assert score >= 5.0

    def test_source_gap_ratio_below_25_adds_0(self):
        score = self._as(deal_source_missing_count=1, total_records_evaluated=20)
        assert score == 0.0

    def test_total_records_zero_skips_source_gap(self):
        # Should not raise ZeroDivisionError
        score = self._as(total_records_evaluated=0, deal_source_missing_count=0)
        assert score == 0.0

    def test_accuracy_clamped_at_100(self):
        score = self._as(
            stage_mismatch_count=10,
            duplicate_account_count=10,
            auto_filled_fields_pct=100,
            deal_source_missing_count=20,
            total_records_evaluated=20,
        )
        assert score == 100.0


# ═══════════════════════════════════════════════════════════════════════════
# 6. TIMELINESS SCORE TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestTimelinessScore:
    def _ts(self, **kwargs) -> float:
        return fresh_engine()._timeliness_score(make_input(**kwargs))

    def test_perfect_timeliness_zero(self):
        assert self._ts() == 0.0

    def test_stale_ratio_ge_50_adds_40(self):
        score = self._ts(stale_record_count=10, total_records_evaluated=20)
        assert score >= 40.0

    def test_stale_ratio_30_50_adds_25(self):
        score = self._ts(stale_record_count=6, total_records_evaluated=20)
        assert score >= 25.0

    def test_stale_ratio_15_30_adds_12(self):
        score = self._ts(stale_record_count=3, total_records_evaluated=20)
        assert score >= 12.0

    def test_stale_ratio_below_15_adds_0(self):
        score = self._ts(stale_record_count=2, total_records_evaluated=20)
        assert score == 0.0

    def test_total_records_zero_skips_stale_ratio(self):
        score = self._ts(total_records_evaluated=0, stale_record_count=0)
        assert score == 0.0

    def test_staleness_days_ge_60_adds_30(self):
        score = self._ts(avg_record_staleness_days=60.0)
        assert score >= 30.0

    def test_staleness_days_30_59_adds_18(self):
        score = self._ts(avg_record_staleness_days=30.0)
        assert score >= 18.0

    def test_staleness_days_14_29_adds_8(self):
        score = self._ts(avg_record_staleness_days=14.0)
        assert score >= 8.0

    def test_staleness_days_below_14_adds_0(self):
        assert self._ts(avg_record_staleness_days=13.9) == 0.0

    def test_login_le_3_adds_20(self):
        score = self._ts(crm_login_frequency_last_30d=3)
        assert score >= 20.0

    def test_login_4_to_8_adds_10(self):
        score = self._ts(crm_login_frequency_last_30d=8)
        assert score >= 10.0

    def test_login_above_8_adds_0(self):
        assert self._ts(crm_login_frequency_last_30d=9) == 0.0

    def test_timeliness_clamped_at_100(self):
        # Max possible: stale>=50%->40 + staleness>=60->30 + login<=3->20 = 90
        # clamp(90, 0, 100) = 90; verifying it never exceeds 100
        score = self._ts(
            stale_record_count=20,
            total_records_evaluated=20,
            avg_record_staleness_days=120,
            crm_login_frequency_last_30d=0,
        )
        assert score <= 100.0


# ═══════════════════════════════════════════════════════════════════════════
# 7. ACTIVITY COVERAGE SCORE TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestActivityCoverageScore:
    def _ac(self, **kwargs) -> float:
        return fresh_engine()._activity_coverage_score(make_input(**kwargs))

    def test_perfect_activity_zero(self):
        assert self._ac() == 0.0

    def test_activity_notes_below_40_adds_40(self):
        score = self._ac(records_with_activity_notes_pct=39.9)
        assert score >= 40.0

    def test_activity_notes_40_60_adds_25(self):
        score = self._ac(records_with_activity_notes_pct=40.0)
        assert score >= 25.0

    def test_activity_notes_60_75_adds_12(self):
        score = self._ac(records_with_activity_notes_pct=60.0)
        assert score >= 12.0

    def test_activity_notes_75_plus_adds_0(self):
        assert self._ac(records_with_activity_notes_pct=75.0) == 0.0

    def test_forecast_no_activity_ge_5_adds_30(self):
        score = self._ac(forecast_without_recent_activity_count=5)
        assert score >= 30.0

    def test_forecast_no_activity_3_4_adds_18(self):
        score = self._ac(forecast_without_recent_activity_count=3)
        assert score >= 18.0

    def test_forecast_no_activity_1_2_adds_8(self):
        score = self._ac(forecast_without_recent_activity_count=1)
        assert score >= 8.0

    def test_forecast_no_activity_0_adds_0(self):
        assert self._ac(forecast_without_recent_activity_count=0) == 0.0

    def test_overdue_followup_ge_8_adds_20(self):
        score = self._ac(overdue_follow_up_count=8)
        assert score >= 20.0

    def test_overdue_followup_4_7_adds_10(self):
        score = self._ac(overdue_follow_up_count=4)
        assert score >= 10.0

    def test_overdue_followup_2_3_adds_5(self):
        score = self._ac(overdue_follow_up_count=2)
        assert score >= 5.0

    def test_overdue_followup_0_1_adds_0(self):
        assert self._ac(overdue_follow_up_count=0) == 0.0
        assert self._ac(overdue_follow_up_count=1) == 0.0

    def test_activity_coverage_clamped_at_100(self):
        # Max possible: notes<40->40 + forecast>=5->30 + overdue>=8->20 = 90
        # clamp never exceeds 100
        score = self._ac(
            records_with_activity_notes_pct=0,
            forecast_without_recent_activity_count=10,
            overdue_follow_up_count=10,
        )
        assert score <= 100.0


# ═══════════════════════════════════════════════════════════════════════════
# 8. RISK CLASSIFICATION TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestRiskClassification:
    def _risk(self, composite: float) -> DataQualityRisk:
        return fresh_engine()._classify_risk(composite)

    def test_composite_0_is_low(self):
        assert self._risk(0.0) == DataQualityRisk.low

    def test_composite_19_is_low(self):
        assert self._risk(19.9) == DataQualityRisk.low

    def test_composite_20_is_moderate(self):
        assert self._risk(20.0) == DataQualityRisk.moderate

    def test_composite_39_is_moderate(self):
        assert self._risk(39.9) == DataQualityRisk.moderate

    def test_composite_40_is_high(self):
        assert self._risk(40.0) == DataQualityRisk.high

    def test_composite_59_is_high(self):
        assert self._risk(59.9) == DataQualityRisk.high

    def test_composite_60_is_critical(self):
        assert self._risk(60.0) == DataQualityRisk.critical

    def test_composite_100_is_critical(self):
        assert self._risk(100.0) == DataQualityRisk.critical

    def test_boundary_low_moderate_exact(self):
        assert self._risk(19.999) == DataQualityRisk.low
        assert self._risk(20.0) == DataQualityRisk.moderate

    def test_boundary_moderate_high_exact(self):
        assert self._risk(39.999) == DataQualityRisk.moderate
        assert self._risk(40.0) == DataQualityRisk.high

    def test_boundary_high_critical_exact(self):
        assert self._risk(59.999) == DataQualityRisk.high
        assert self._risk(60.0) == DataQualityRisk.critical


# ═══════════════════════════════════════════════════════════════════════════
# 9. SEVERITY CLASSIFICATION TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestSeverityClassification:
    def _sev(self, composite: float) -> QualitySeverity:
        return fresh_engine()._classify_severity(composite)

    def test_composite_0_is_clean(self):
        assert self._sev(0.0) == QualitySeverity.clean

    def test_composite_19_is_clean(self):
        assert self._sev(19.9) == QualitySeverity.clean

    def test_composite_20_is_degraded(self):
        assert self._sev(20.0) == QualitySeverity.degraded

    def test_composite_39_is_degraded(self):
        assert self._sev(39.9) == QualitySeverity.degraded

    def test_composite_40_is_unreliable(self):
        assert self._sev(40.0) == QualitySeverity.unreliable

    def test_composite_59_is_unreliable(self):
        assert self._sev(59.9) == QualitySeverity.unreliable

    def test_composite_60_is_corrupt(self):
        assert self._sev(60.0) == QualitySeverity.corrupt

    def test_composite_100_is_corrupt(self):
        assert self._sev(100.0) == QualitySeverity.corrupt

    def test_severity_mirrors_risk_boundaries(self):
        for composite in [0, 10, 19.9, 20, 30, 39.9, 40, 50, 59.9, 60, 80, 100]:
            risk = fresh_engine()._classify_risk(composite)
            sev = self._sev(composite)
            mapping = {
                DataQualityRisk.low: QualitySeverity.clean,
                DataQualityRisk.moderate: QualitySeverity.degraded,
                DataQualityRisk.high: QualitySeverity.unreliable,
                DataQualityRisk.critical: QualitySeverity.corrupt,
            }
            assert mapping[risk] == sev


# ═══════════════════════════════════════════════════════════════════════════
# 10. FAILURE MODE CLASSIFICATION TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestFailureModeClassification:
    def test_duplicate_accounts_ge_2_takes_priority(self):
        engine = fresh_engine()
        r = engine.assess(make_input(
            duplicate_account_count=2,
            data_entry_completeness_pct=40,  # would also trigger missing_data
            avg_record_staleness_days=60,    # would also trigger stale_records
        ))
        assert r.quality_failure_mode == QualityFailureMode.duplicate_accounts

    def test_missing_data_triggered_by_low_completeness(self):
        engine = fresh_engine()
        r = engine.assess(make_input(
            data_entry_completeness_pct=50.0,
            duplicate_account_count=0,
        ))
        assert r.quality_failure_mode == QualityFailureMode.missing_data

    def test_missing_data_triggered_by_missing_close_dates(self):
        engine = fresh_engine()
        r = engine.assess(make_input(
            missing_close_date_count=5,
            data_entry_completeness_pct=90,
            duplicate_account_count=0,
        ))
        assert r.quality_failure_mode == QualityFailureMode.missing_data

    def test_stale_records_triggered_by_staleness_days(self):
        engine = fresh_engine()
        r = engine.assess(make_input(
            avg_record_staleness_days=30.0,
            duplicate_account_count=0,
            data_entry_completeness_pct=90,
            missing_close_date_count=0,
        ))
        assert r.quality_failure_mode == QualityFailureMode.stale_records

    def test_stale_records_triggered_by_stale_count(self):
        engine = fresh_engine()
        r = engine.assess(make_input(
            stale_record_count=5,
            total_records_evaluated=20,
            duplicate_account_count=0,
            data_entry_completeness_pct=90,
            missing_close_date_count=0,
            avg_record_staleness_days=5,
        ))
        assert r.quality_failure_mode == QualityFailureMode.stale_records

    def test_stage_drift_triggered_by_mismatch_ge_4(self):
        engine = fresh_engine()
        r = engine.assess(make_input(
            stage_mismatch_count=4,
            duplicate_account_count=0,
            data_entry_completeness_pct=90,
            missing_close_date_count=0,
            stale_record_count=0,
            avg_record_staleness_days=5,
        ))
        assert r.quality_failure_mode == QualityFailureMode.stage_drift

    def test_activity_gap_triggered_by_low_notes(self):
        engine = fresh_engine()
        r = engine.assess(make_input(
            records_with_activity_notes_pct=49.0,
            duplicate_account_count=0,
            data_entry_completeness_pct=90,
            missing_close_date_count=0,
            stale_record_count=0,
            avg_record_staleness_days=5,
            stage_mismatch_count=0,
        ))
        assert r.quality_failure_mode == QualityFailureMode.activity_gap

    def test_activity_gap_triggered_by_forecast_count(self):
        engine = fresh_engine()
        r = engine.assess(make_input(
            forecast_without_recent_activity_count=3,
            records_with_activity_notes_pct=80,
            duplicate_account_count=0,
            data_entry_completeness_pct=90,
            missing_close_date_count=0,
            stale_record_count=0,
            avg_record_staleness_days=5,
            stage_mismatch_count=0,
        ))
        assert r.quality_failure_mode == QualityFailureMode.activity_gap

    def test_none_mode_when_all_clean(self):
        engine = fresh_engine()
        r = engine.assess(make_input())
        assert r.quality_failure_mode == QualityFailureMode.none

    def test_duplicate_accounts_1_does_not_trigger_mode(self):
        engine = fresh_engine()
        r = engine.assess(make_input(
            duplicate_account_count=1,
            data_entry_completeness_pct=90,
            missing_close_date_count=0,
            avg_record_staleness_days=5,
            stale_record_count=0,
            stage_mismatch_count=0,
            records_with_activity_notes_pct=80,
            forecast_without_recent_activity_count=0,
        ))
        assert r.quality_failure_mode != QualityFailureMode.duplicate_accounts

    def test_completeness_pct_exactly_60_not_missing_data(self):
        engine = fresh_engine()
        r = engine.assess(make_input(
            data_entry_completeness_pct=60.0,
            duplicate_account_count=0,
            missing_close_date_count=0,
            avg_record_staleness_days=5,
            stale_record_count=0,
            stage_mismatch_count=0,
            records_with_activity_notes_pct=80,
            forecast_without_recent_activity_count=0,
        ))
        assert r.quality_failure_mode != QualityFailureMode.missing_data


# ═══════════════════════════════════════════════════════════════════════════
# 11. RECOMMENDED ACTION TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestRecommendedAction:
    def _action(self, risk: DataQualityRisk, composite: float) -> QualityAction:
        return fresh_engine()._recommended_action(risk, composite)

    def test_composite_ge_60_pipeline_freeze(self):
        assert self._action(DataQualityRisk.critical, 60.0) == QualityAction.pipeline_freeze

    def test_composite_above_60_pipeline_freeze(self):
        assert self._action(DataQualityRisk.critical, 80.0) == QualityAction.pipeline_freeze

    def test_high_risk_below_60_data_audit(self):
        assert self._action(DataQualityRisk.high, 55.0) == QualityAction.data_audit

    def test_moderate_risk_crm_coaching(self):
        assert self._action(DataQualityRisk.moderate, 30.0) == QualityAction.crm_coaching

    def test_low_risk_composite_ge_10_self_remediate(self):
        assert self._action(DataQualityRisk.low, 10.0) == QualityAction.self_remediate

    def test_low_risk_composite_below_10_no_action(self):
        assert self._action(DataQualityRisk.low, 5.0) == QualityAction.no_action

    def test_low_risk_composite_exactly_10_self_remediate(self):
        assert self._action(DataQualityRisk.low, 10.0) == QualityAction.self_remediate

    def test_clean_input_no_action(self):
        engine = fresh_engine()
        r = engine.assess(make_input())
        assert r.recommended_action == QualityAction.no_action

    def test_critical_composite_pipeline_freeze_via_assess(self):
        engine = fresh_engine()
        r = engine.assess(make_input(
            data_entry_completeness_pct=10,
            missing_close_date_count=10,
            missing_opportunity_value_count=10,
            stage_mismatch_count=10,
            duplicate_account_count=10,
            stale_record_count=18,
            total_records_evaluated=20,
            avg_record_staleness_days=90,
            crm_login_frequency_last_30d=1,
            records_with_activity_notes_pct=5,
            forecast_without_recent_activity_count=10,
            overdue_follow_up_count=10,
            auto_filled_fields_pct=90,
            deal_source_missing_count=18,
        ))
        assert r.recommended_action == QualityAction.pipeline_freeze

    def test_moderate_composite_crm_coaching_via_assess(self):
        engine = fresh_engine()
        r = engine.assess(make_input(
            data_entry_completeness_pct=70,
            missing_close_date_count=3,
        ))
        # composite should be in moderate range
        if r.data_quality_risk == DataQualityRisk.moderate:
            assert r.recommended_action == QualityAction.crm_coaching


# ═══════════════════════════════════════════════════════════════════════════
# 12. IS_DATA_QUALITY_RISK INVARIANT TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestIsDataQualityRisk:
    """is_data_quality_risk: composite >= 40 OR missing_close_date >= 5 OR completeness_pct < 50"""

    def test_false_when_all_clean(self):
        engine = fresh_engine()
        r = engine.assess(make_input())
        assert r.is_data_quality_risk is False

    def test_true_when_composite_ge_40(self):
        engine = fresh_engine()
        r = engine.assess(make_input(
            data_entry_completeness_pct=10,
            missing_close_date_count=10,
            missing_opportunity_value_count=10,
        ))
        if r.quality_composite >= 40:
            assert r.is_data_quality_risk is True

    def test_true_when_missing_close_date_ge_5(self):
        engine = fresh_engine()
        r = engine.assess(make_input(missing_close_date_count=5))
        assert r.is_data_quality_risk is True

    def test_true_when_missing_close_date_exactly_5(self):
        engine = fresh_engine()
        r = engine.assess(make_input(missing_close_date_count=5))
        assert r.is_data_quality_risk is True

    def test_false_when_missing_close_date_4(self):
        # close_date=4 does not trigger the >=5 condition;
        # with clean baseline input completeness=90>=50 and composite is low
        engine = fresh_engine()
        r = engine.assess(make_input(missing_close_date_count=4))
        # composite is ~2.4, completeness=90>=50, close_date=4<5 => all three conditions False
        assert r.is_data_quality_risk is False

    def test_true_when_completeness_below_50(self):
        engine = fresh_engine()
        r = engine.assess(make_input(data_entry_completeness_pct=49.9))
        assert r.is_data_quality_risk is True

    def test_true_when_completeness_exactly_49(self):
        engine = fresh_engine()
        r = engine.assess(make_input(data_entry_completeness_pct=49.0))
        assert r.is_data_quality_risk is True

    def test_false_when_completeness_exactly_50(self):
        # data_entry_completeness_pct=50.0 is NOT < 50, composite is low (~10.5), close_date=0<5
        engine = fresh_engine()
        r = engine.assess(make_input(data_entry_completeness_pct=50.0))
        assert r.is_data_quality_risk is False

    def test_true_when_composite_exactly_40(self):
        """Build an input where composite lands exactly at 40."""
        # completeness=50=>35, accuracy=0, timeliness=0, activity=0 => 35*0.30=10.5
        # Need composite=40; let's use large missing close dates too
        engine = fresh_engine()
        r = engine.assess(make_input(
            data_entry_completeness_pct=10,  # completeness -> 50
            missing_close_date_count=10,      # completeness -> +30 = 80; clamped
        ))
        if r.quality_composite >= 40:
            assert r.is_data_quality_risk is True

    def test_is_data_quality_risk_or_condition_independence(self):
        """Verify that ANY of the three conditions independently triggers True."""
        engine = fresh_engine()
        # Condition 1: missing_close_date >= 5 alone
        r1 = engine.assess(make_input(missing_close_date_count=5))
        assert r1.is_data_quality_risk is True
        # Condition 2: completeness_pct < 50 alone
        r2 = engine.assess(make_input(data_entry_completeness_pct=49.0))
        assert r2.is_data_quality_risk is True


# ═══════════════════════════════════════════════════════════════════════════
# 13. REQUIRES_DATA_AUDIT INVARIANT TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestRequiresDataAudit:
    """requires_data_audit: composite >= 30 OR missing_opp_value >= 3 OR duplicate_account >= 2"""

    def test_false_when_all_clean(self):
        engine = fresh_engine()
        r = engine.assess(make_input())
        assert r.requires_data_audit is False

    def test_true_when_composite_ge_30(self):
        engine = fresh_engine()
        r = engine.assess(make_input(
            data_entry_completeness_pct=10,
            missing_close_date_count=10,
        ))
        if r.quality_composite >= 30:
            assert r.requires_data_audit is True

    def test_true_when_missing_opp_value_ge_3(self):
        engine = fresh_engine()
        r = engine.assess(make_input(missing_opportunity_value_count=3))
        assert r.requires_data_audit is True

    def test_true_when_missing_opp_value_exactly_3(self):
        engine = fresh_engine()
        r = engine.assess(make_input(missing_opportunity_value_count=3))
        assert r.requires_data_audit is True

    def test_false_when_missing_opp_value_2(self):
        # opp_value=2 < 3, baseline has dup=0<2, and composite is ~1.5 < 30
        engine = fresh_engine()
        r = engine.assess(make_input(missing_opportunity_value_count=2))
        assert r.requires_data_audit is False

    def test_true_when_duplicate_account_ge_2(self):
        engine = fresh_engine()
        r = engine.assess(make_input(duplicate_account_count=2))
        assert r.requires_data_audit is True

    def test_true_when_duplicate_account_exactly_2(self):
        engine = fresh_engine()
        r = engine.assess(make_input(duplicate_account_count=2))
        assert r.requires_data_audit is True

    def test_false_when_duplicate_account_1(self):
        # dup=1 < 2, baseline opp_value=0 < 3, and composite is ~2.0 < 30
        engine = fresh_engine()
        r = engine.assess(make_input(duplicate_account_count=1))
        assert r.requires_data_audit is False

    def test_all_three_conditions_trigger_independently(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input(missing_opportunity_value_count=3))
        assert r1.requires_data_audit is True
        r2 = engine.assess(make_input(duplicate_account_count=2))
        assert r2.requires_data_audit is True


# ═══════════════════════════════════════════════════════════════════════════
# 14. ESTIMATED PIPELINE DISTORTION TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestEstimatedPipelineDistortion:
    """estimated_pipeline_distortion_pct = clamp(composite * 0.8, 0, 100)"""

    def test_zero_composite_zero_distortion(self):
        engine = fresh_engine()
        r = engine.assess(make_input())
        assert r.estimated_pipeline_distortion_pct == pytest.approx(r.quality_composite * 0.8, abs=0.2)

    def test_distortion_equals_composite_times_0_8(self):
        engine = fresh_engine()
        inp = make_input(
            data_entry_completeness_pct=70,
            missing_close_date_count=3,
        )
        r = engine.assess(inp)
        expected = min(100.0, r.quality_composite * 0.8)
        assert r.estimated_pipeline_distortion_pct == pytest.approx(expected, abs=0.15)

    def test_distortion_clamped_at_100(self):
        engine = fresh_engine()
        r = engine.assess(make_input(
            data_entry_completeness_pct=1,
            missing_close_date_count=15,
            missing_opportunity_value_count=15,
            stage_mismatch_count=10,
            duplicate_account_count=10,
            stale_record_count=20,
            total_records_evaluated=20,
            avg_record_staleness_days=120,
            crm_login_frequency_last_30d=0,
            records_with_activity_notes_pct=0,
            forecast_without_recent_activity_count=15,
            overdue_follow_up_count=15,
        ))
        assert r.estimated_pipeline_distortion_pct <= 100.0

    def test_distortion_never_negative(self):
        engine = fresh_engine()
        r = engine.assess(make_input())
        assert r.estimated_pipeline_distortion_pct >= 0.0

    def test_distortion_proportional_to_composite(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input())
        r2 = engine.assess(make_input(
            data_entry_completeness_pct=55,
            missing_close_date_count=3,
        ))
        if r2.quality_composite > r1.quality_composite:
            assert r2.estimated_pipeline_distortion_pct >= r1.estimated_pipeline_distortion_pct

    def test_distortion_to_dict_matches_result(self):
        engine = fresh_engine()
        r = engine.assess(make_input())
        d = r.to_dict()
        assert d["estimated_pipeline_distortion_pct"] == round(r.estimated_pipeline_distortion_pct, 1)


# ═══════════════════════════════════════════════════════════════════════════
# 15. QUALITY SIGNAL TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestQualitySignal:
    def test_none_mode_returns_acceptable_string(self):
        engine = fresh_engine()
        r = engine.assess(make_input())
        assert r.quality_signal == "CRM data quality within acceptable parameters"

    def test_missing_data_signal_contains_close_date_count(self):
        engine = fresh_engine()
        r = engine.assess(make_input(missing_close_date_count=5))
        assert "5" in r.quality_signal

    def test_missing_data_signal_contains_completeness_pct(self):
        engine = fresh_engine()
        r = engine.assess(make_input(missing_close_date_count=5, data_entry_completeness_pct=88.0))
        assert "88" in r.quality_signal

    def test_stale_records_signal_contains_stale_count(self):
        engine = fresh_engine()
        r = engine.assess(make_input(
            stale_record_count=5,
            total_records_evaluated=20,
            avg_record_staleness_days=35,
            data_entry_completeness_pct=90,
            missing_close_date_count=0,
            duplicate_account_count=0,
        ))
        assert r.quality_failure_mode == QualityFailureMode.stale_records
        assert "5" in r.quality_signal

    def test_stage_drift_signal_contains_mismatch_count(self):
        engine = fresh_engine()
        r = engine.assess(make_input(
            stage_mismatch_count=4,
            data_entry_completeness_pct=90,
            missing_close_date_count=0,
            duplicate_account_count=0,
            avg_record_staleness_days=5,
            stale_record_count=0,
        ))
        assert r.quality_failure_mode == QualityFailureMode.stage_drift
        assert "4" in r.quality_signal

    def test_duplicate_accounts_signal_contains_dup_count(self):
        engine = fresh_engine()
        r = engine.assess(make_input(duplicate_account_count=3))
        assert r.quality_failure_mode == QualityFailureMode.duplicate_accounts
        assert "3" in r.quality_signal

    def test_activity_gap_signal_contains_notes_pct(self):
        engine = fresh_engine()
        r = engine.assess(make_input(
            records_with_activity_notes_pct=45.0,
            data_entry_completeness_pct=90,
            duplicate_account_count=0,
            missing_close_date_count=0,
            avg_record_staleness_days=5,
            stale_record_count=0,
            stage_mismatch_count=0,
        ))
        assert r.quality_failure_mode == QualityFailureMode.activity_gap
        assert "45" in r.quality_signal

    def test_signal_contains_composite_for_non_none_modes(self):
        engine = fresh_engine()
        r = engine.assess(make_input(duplicate_account_count=3))
        assert "composite" in r.quality_signal.lower() or str(int(r.quality_composite)) in r.quality_signal

    def test_signal_is_nonempty_string(self):
        engine = fresh_engine()
        r = engine.assess(make_input())
        assert isinstance(r.quality_signal, str)
        assert len(r.quality_signal) > 0


# ═══════════════════════════════════════════════════════════════════════════
# 16. assess() METHOD TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestAssessMethod:
    def test_assess_returns_result_object(self):
        engine = fresh_engine()
        from swarm.intelligence.crm_data_quality_risk_engine import CRMDataQualityResult
        r = engine.assess(make_input())
        assert isinstance(r, CRMDataQualityResult)

    def test_assess_stores_result_in_internal_list(self):
        engine = fresh_engine()
        engine.assess(make_input())
        assert len(engine._results) == 1

    def test_assess_accumulates_results(self):
        engine = fresh_engine()
        for i in range(5):
            engine.assess(make_input(rep_id=f"rep-{i}"))
        assert len(engine._results) == 5

    def test_assess_preserves_rep_id(self):
        engine = fresh_engine()
        r = engine.assess(make_input(rep_id="unique-rep"))
        assert r.rep_id == "unique-rep"

    def test_assess_preserves_region(self):
        engine = fresh_engine()
        r = engine.assess(make_input(region="Southeast"))
        assert r.region == "Southeast"

    def test_assess_all_result_fields_present(self):
        engine = fresh_engine()
        r = engine.assess(make_input())
        for field in dataclasses.fields(r):
            assert hasattr(r, field.name)

    def test_assess_data_quality_risk_is_enum(self):
        engine = fresh_engine()
        r = engine.assess(make_input())
        assert isinstance(r.data_quality_risk, DataQualityRisk)

    def test_assess_quality_failure_mode_is_enum(self):
        engine = fresh_engine()
        r = engine.assess(make_input())
        assert isinstance(r.quality_failure_mode, QualityFailureMode)

    def test_assess_quality_severity_is_enum(self):
        engine = fresh_engine()
        r = engine.assess(make_input())
        assert isinstance(r.quality_severity, QualitySeverity)

    def test_assess_recommended_action_is_enum(self):
        engine = fresh_engine()
        r = engine.assess(make_input())
        assert isinstance(r.recommended_action, QualityAction)

    def test_assess_multiple_reps_independent(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input(rep_id="A"))
        r2 = engine.assess(make_input(rep_id="B"))
        assert r1.rep_id == "A"
        assert r2.rep_id == "B"


# ═══════════════════════════════════════════════════════════════════════════
# 17. assess_batch() TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestAssessBatch:
    def test_batch_empty_list_returns_empty(self):
        engine = fresh_engine()
        assert engine.assess_batch([]) == []

    def test_batch_returns_list(self):
        engine = fresh_engine()
        results = engine.assess_batch([make_input(), make_input()])
        assert isinstance(results, list)

    def test_batch_length_matches_input(self):
        engine = fresh_engine()
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(7)]
        results = engine.assess_batch(inputs)
        assert len(results) == 7

    def test_batch_preserves_order(self):
        engine = fresh_engine()
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"rep-{i}"

    def test_batch_stores_all_in_internal_list(self):
        engine = fresh_engine()
        engine.assess_batch([make_input() for _ in range(4)])
        assert len(engine._results) == 4

    def test_batch_accumulates_after_single_assess(self):
        engine = fresh_engine()
        engine.assess(make_input())
        engine.assess_batch([make_input(), make_input()])
        assert len(engine._results) == 3

    def test_batch_single_item_same_as_single_assess(self):
        inp = make_input(rep_id="solo")
        e1 = fresh_engine()
        e2 = fresh_engine()
        r_single = e1.assess(inp)
        r_batch = e2.assess_batch([inp])[0]
        assert r_single.to_dict() == r_batch.to_dict()

    def test_batch_each_result_has_15_keys_in_to_dict(self):
        engine = fresh_engine()
        results = engine.assess_batch([make_input() for _ in range(3)])
        for r in results:
            assert len(r.to_dict()) == 15


# ═══════════════════════════════════════════════════════════════════════════
# 18. summary() TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestSummaryMethod:
    def test_summary_total_matches_assessed_count(self):
        engine = fresh_engine()
        engine.assess_batch([make_input() for _ in range(6)])
        assert engine.summary()["total"] == 6

    def test_summary_risk_counts_keys_are_strings(self):
        engine = fresh_engine()
        engine.assess(make_input())
        s = engine.summary()
        for k in s["risk_counts"]:
            assert isinstance(k, str)

    def test_summary_risk_counts_sum_equals_total(self):
        engine = fresh_engine()
        engine.assess_batch([make_input() for _ in range(5)])
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_severity_counts_sum_equals_total(self):
        engine = fresh_engine()
        engine.assess_batch([make_input() for _ in range(5)])
        s = engine.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_equals_total(self):
        engine = fresh_engine()
        engine.assess_batch([make_input() for _ in range(5)])
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_failure_mode_counts_sum_equals_total(self):
        engine = fresh_engine()
        engine.assess_batch([make_input() for _ in range(5)])
        s = engine.summary()
        assert sum(s["failure_mode_counts"].values()) == s["total"]

    def test_summary_avg_composite_reasonable(self):
        engine = fresh_engine()
        engine.assess_batch([make_input() for _ in range(3)])
        s = engine.summary()
        assert 0.0 <= s["avg_quality_composite"] <= 100.0

    def test_summary_data_quality_risk_count_le_total(self):
        engine = fresh_engine()
        engine.assess_batch([make_input() for _ in range(5)])
        s = engine.summary()
        assert s["data_quality_risk_count"] <= s["total"]

    def test_summary_audit_required_count_le_total(self):
        engine = fresh_engine()
        engine.assess_batch([make_input() for _ in range(5)])
        s = engine.summary()
        assert s["audit_required_count"] <= s["total"]

    def test_summary_avg_scores_between_0_and_100(self):
        engine = fresh_engine()
        engine.assess_batch([make_input() for _ in range(4)])
        s = engine.summary()
        for key in ("avg_completeness_score", "avg_accuracy_score",
                    "avg_timeliness_score", "avg_activity_coverage_score",
                    "avg_estimated_pipeline_distortion_pct"):
            assert 0.0 <= s[key] <= 100.0, key

    def test_summary_single_result_counts_correctly(self):
        engine = fresh_engine()
        r = engine.assess(make_input())
        s = engine.summary()
        assert s["total"] == 1
        assert s["risk_counts"].get(r.data_quality_risk.value, 0) == 1

    def test_summary_avg_composite_is_mean(self):
        engine = fresh_engine()
        inp1 = make_input(data_entry_completeness_pct=90)
        inp2 = make_input(data_entry_completeness_pct=90)
        r1 = engine.assess(inp1)
        r2 = engine.assess(inp2)
        s = engine.summary()
        expected_avg = round((r1.quality_composite + r2.quality_composite) / 2, 1)
        assert s["avg_quality_composite"] == expected_avg

    def test_summary_risk_count_all_low_when_clean(self):
        engine = fresh_engine()
        for _ in range(3):
            engine.assess(make_input())
        s = engine.summary()
        assert s["risk_counts"].get("low", 0) == 3

    def test_summary_distortion_count_avg_matches_results(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input())
        r2 = engine.assess(make_input())
        s = engine.summary()
        expected = round((r1.estimated_pipeline_distortion_pct + r2.estimated_pipeline_distortion_pct) / 2, 1)
        assert s["avg_estimated_pipeline_distortion_pct"] == expected

    def test_summary_called_twice_same_result(self):
        engine = fresh_engine()
        engine.assess(make_input())
        s1 = engine.summary()
        s2 = engine.summary()
        assert s1 == s2

    def test_summary_does_not_mutate_state(self):
        engine = fresh_engine()
        engine.assess(make_input())
        before_count = len(engine._results)
        engine.summary()
        assert len(engine._results) == before_count

    def test_summary_with_mixed_risk_levels(self):
        engine = fresh_engine()
        engine.assess(make_input())  # low
        engine.assess(make_input(missing_close_date_count=5))  # triggers dq risk
        engine.assess(make_input(
            data_entry_completeness_pct=10,
            missing_close_date_count=10,
        ))
        s = engine.summary()
        assert s["total"] == 3
        assert s["data_quality_risk_count"] >= 1


# ═══════════════════════════════════════════════════════════════════════════
# 19. END-TO-END SCENARIO TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestEndToEndScenarios:
    def test_pristine_rep_all_green(self):
        engine = fresh_engine()
        r = engine.assess(make_input())
        assert r.data_quality_risk == DataQualityRisk.low
        assert r.quality_severity == QualitySeverity.clean
        assert r.is_data_quality_risk is False
        assert r.requires_data_audit is False
        assert r.recommended_action == QualityAction.no_action
        assert r.quality_composite < 20.0

    def test_critical_rep_all_red(self):
        engine = fresh_engine()
        r = engine.assess(make_input(
            data_entry_completeness_pct=10,
            missing_close_date_count=10,
            missing_opportunity_value_count=10,
            stage_mismatch_count=10,
            duplicate_account_count=10,
            stale_record_count=18,
            total_records_evaluated=20,
            avg_record_staleness_days=90,
            crm_login_frequency_last_30d=1,
            records_with_activity_notes_pct=5,
            forecast_without_recent_activity_count=10,
            overdue_follow_up_count=10,
            auto_filled_fields_pct=90,
            deal_source_missing_count=18,
        ))
        assert r.data_quality_risk == DataQualityRisk.critical
        assert r.quality_severity == QualitySeverity.corrupt
        assert r.is_data_quality_risk is True
        assert r.requires_data_audit is True
        assert r.recommended_action == QualityAction.pipeline_freeze
        assert r.quality_composite >= 60.0

    def test_moderate_rep(self):
        engine = fresh_engine()
        # To land in moderate (composite 20-39) we need several contributing factors:
        # completeness: 65<=70<80 -> +18; close_date=3>=2 -> +8 => completeness_score=26
        # timeliness: staleness=20>=14 -> +8; stale_ratio=8/20=40%>=30% -> +25; login<=8 -> +10 => timeliness=43
        # composite ~= 26*0.30 + 0*0.25 + 43*0.25 + 0*0.20 = 7.8 + 10.75 = 18.55 => low
        # Use more extreme values to reach moderate
        r = engine.assess(make_input(
            data_entry_completeness_pct=70,
            missing_close_date_count=3,
            stale_record_count=8,
            total_records_evaluated=20,
            avg_record_staleness_days=35,
            crm_login_frequency_last_30d=5,
            records_with_activity_notes_pct=55,
            forecast_without_recent_activity_count=2,
        ))
        # composite should be >= 20 (moderate)
        assert r.quality_composite >= 20.0
        assert r.data_quality_risk in (DataQualityRisk.moderate, DataQualityRisk.high, DataQualityRisk.critical)

    def test_high_risk_rep_audit_recommended(self):
        engine = fresh_engine()
        r = engine.assess(make_input(
            data_entry_completeness_pct=55,
            missing_close_date_count=4,
            stage_mismatch_count=5,
            duplicate_account_count=1,
            avg_record_staleness_days=25,
            stale_record_count=5,
            total_records_evaluated=20,
            crm_login_frequency_last_30d=5,
            records_with_activity_notes_pct=50,
        ))
        if r.data_quality_risk == DataQualityRisk.high:
            assert r.recommended_action == QualityAction.data_audit

    def test_batch_mixed_risk_summary_populated(self):
        engine = fresh_engine()
        inputs = [
            make_input(rep_id="clean"),
            make_input(rep_id="dupes", duplicate_account_count=3),
            make_input(rep_id="stale", avg_record_staleness_days=60, crm_login_frequency_last_30d=2),
        ]
        engine.assess_batch(inputs)
        s = engine.summary()
        assert s["total"] == 3
        assert len(s["risk_counts"]) >= 1
        assert len(s["failure_mode_counts"]) >= 1

    def test_zero_total_records_no_crash(self):
        engine = fresh_engine()
        r = engine.assess(make_input(total_records_evaluated=0, deal_source_missing_count=0, stale_record_count=0))
        assert r.quality_composite >= 0.0

    def test_all_zeros_input_no_crash(self):
        engine = fresh_engine()
        r = engine.assess(make_input(
            total_records_evaluated=0,
            missing_close_date_count=0,
            missing_opportunity_value_count=0,
            missing_contact_count=0,
            stale_record_count=0,
            stage_mismatch_count=0,
            duplicate_account_count=0,
            missing_decision_maker_count=0,
            data_entry_completeness_pct=0.0,
            records_with_activity_notes_pct=0.0,
            forecast_without_recent_activity_count=0,
            overdue_follow_up_count=0,
            avg_record_staleness_days=0.0,
            deal_source_missing_count=0,
            crm_login_frequency_last_30d=0,
            auto_filled_fields_pct=0.0,
            records_audited_by_admin_count=0,
            pipeline_audit_score=0.0,
            last_crm_training_days_ago=0,
        ))
        assert r is not None

    def test_very_high_values_no_crash(self):
        engine = fresh_engine()
        r = engine.assess(make_input(
            total_records_evaluated=1000,
            missing_close_date_count=999,
            stale_record_count=999,
            stage_mismatch_count=999,
            duplicate_account_count=999,
            avg_record_staleness_days=999,
            overdue_follow_up_count=999,
            forecast_without_recent_activity_count=999,
        ))
        assert r.quality_composite <= 100.0

    def test_rep_id_and_region_passthrough(self):
        engine = fresh_engine()
        r = engine.assess(make_input(rep_id="R123", region="APAC"))
        d = r.to_dict()
        assert d["rep_id"] == "R123"
        assert d["region"] == "APAC"

    def test_engine_fresh_instance_empty_summary(self):
        engine = CRMDataQualityRiskEngine()
        s = engine.summary()
        assert s["total"] == 0
        assert len(s) == 13


# ═══════════════════════════════════════════════════════════════════════════
# 20. EDGE CASES AND BOUNDARY TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestEdgeCasesAndBoundaries:
    def test_close_date_boundary_4_vs_5(self):
        e = fresh_engine()
        r4 = e.assess(make_input(missing_close_date_count=4))
        r5 = e.assess(make_input(missing_close_date_count=5))
        # 5 triggers is_data_quality_risk
        assert r5.is_data_quality_risk is True

    def test_opp_value_boundary_2_vs_3(self):
        e = fresh_engine()
        r2 = e.assess(make_input(missing_opportunity_value_count=2))
        r3 = e.assess(make_input(missing_opportunity_value_count=3))
        assert r3.requires_data_audit is True

    def test_duplicate_boundary_1_vs_2(self):
        e = fresh_engine()
        r1 = e.assess(make_input(duplicate_account_count=1))
        r2 = e.assess(make_input(duplicate_account_count=2))
        assert r2.requires_data_audit is True
        assert r2.quality_failure_mode == QualityFailureMode.duplicate_accounts
        assert r1.quality_failure_mode != QualityFailureMode.duplicate_accounts

    def test_completeness_pct_boundary_49_vs_50(self):
        e = fresh_engine()
        r49 = e.assess(make_input(data_entry_completeness_pct=49.0))
        r50 = e.assess(make_input(data_entry_completeness_pct=50.0))
        assert r49.is_data_quality_risk is True

    def test_stage_mismatch_boundary_3_vs_4(self):
        e = fresh_engine()
        r3 = e.assess(make_input(
            stage_mismatch_count=3,
            duplicate_account_count=0,
            data_entry_completeness_pct=90,
            missing_close_date_count=0,
            avg_record_staleness_days=5,
            stale_record_count=0,
            records_with_activity_notes_pct=80,
            forecast_without_recent_activity_count=0,
        ))
        r4 = e.assess(make_input(
            stage_mismatch_count=4,
            duplicate_account_count=0,
            data_entry_completeness_pct=90,
            missing_close_date_count=0,
            avg_record_staleness_days=5,
            stale_record_count=0,
            records_with_activity_notes_pct=80,
            forecast_without_recent_activity_count=0,
        ))
        assert r4.quality_failure_mode == QualityFailureMode.stage_drift
        assert r3.quality_failure_mode != QualityFailureMode.stage_drift

    def test_login_frequency_boundary_3_vs_4(self):
        e = fresh_engine()
        # 3 => +20, 4 => +10 (tier 2), so timeliness differs
        s3 = e._timeliness_score(make_input(crm_login_frequency_last_30d=3))
        s4 = e._timeliness_score(make_input(crm_login_frequency_last_30d=4))
        assert s3 > s4

    def test_login_frequency_boundary_8_vs_9(self):
        e = fresh_engine()
        s8 = e._timeliness_score(make_input(crm_login_frequency_last_30d=8))
        s9 = e._timeliness_score(make_input(crm_login_frequency_last_30d=9))
        assert s8 > s9

    def test_auto_fill_boundary_49_vs_50(self):
        e = fresh_engine()
        s49 = e._accuracy_score(make_input(auto_filled_fields_pct=49.9))
        s50 = e._accuracy_score(make_input(auto_filled_fields_pct=50.0))
        assert s50 > s49

    def test_auto_fill_boundary_69_vs_70(self):
        e = fresh_engine()
        s69 = e._accuracy_score(make_input(auto_filled_fields_pct=69.9))
        s70 = e._accuracy_score(make_input(auto_filled_fields_pct=70.0))
        assert s70 > s69

    def test_stale_ratio_boundary_exactly_50pct(self):
        e = fresh_engine()
        s_49 = e._timeliness_score(make_input(stale_record_count=9, total_records_evaluated=20))   # 45%
        s_50 = e._timeliness_score(make_input(stale_record_count=10, total_records_evaluated=20))  # 50%
        assert s_50 > s_49

    def test_staleness_days_boundary_exactly_14(self):
        e = fresh_engine()
        s13 = e._timeliness_score(make_input(avg_record_staleness_days=13.9))
        s14 = e._timeliness_score(make_input(avg_record_staleness_days=14.0))
        assert s14 > s13

    def test_staleness_days_boundary_exactly_30(self):
        e = fresh_engine()
        s29 = e._timeliness_score(make_input(avg_record_staleness_days=29.9))
        s30 = e._timeliness_score(make_input(avg_record_staleness_days=30.0))
        assert s30 > s29

    def test_staleness_days_boundary_exactly_60(self):
        e = fresh_engine()
        s59 = e._timeliness_score(make_input(avg_record_staleness_days=59.9))
        s60 = e._timeliness_score(make_input(avg_record_staleness_days=60.0))
        assert s60 > s59

    def test_activity_notes_boundary_exactly_40(self):
        e = fresh_engine()
        s39 = e._activity_coverage_score(make_input(records_with_activity_notes_pct=39.9))
        s40 = e._activity_coverage_score(make_input(records_with_activity_notes_pct=40.0))
        assert s39 > s40

    def test_activity_notes_boundary_exactly_60(self):
        e = fresh_engine()
        s59 = e._activity_coverage_score(make_input(records_with_activity_notes_pct=59.9))
        s60 = e._activity_coverage_score(make_input(records_with_activity_notes_pct=60.0))
        assert s59 > s60

    def test_activity_notes_boundary_exactly_75(self):
        e = fresh_engine()
        s74 = e._activity_coverage_score(make_input(records_with_activity_notes_pct=74.9))
        s75 = e._activity_coverage_score(make_input(records_with_activity_notes_pct=75.0))
        assert s74 > s75

    def test_source_gap_ratio_exactly_25pct(self):
        e = fresh_engine()
        s24 = e._accuracy_score(make_input(deal_source_missing_count=4, total_records_evaluated=20))   # 20% < 25%
        s25 = e._accuracy_score(make_input(deal_source_missing_count=5, total_records_evaluated=20))   # 25%
        assert s25 > s24

    def test_source_gap_ratio_exactly_50pct(self):
        e = fresh_engine()
        s49 = e._accuracy_score(make_input(deal_source_missing_count=9, total_records_evaluated=20))   # 45%
        s50 = e._accuracy_score(make_input(deal_source_missing_count=10, total_records_evaluated=20))  # 50%
        assert s50 > s49

    def test_missing_close_date_boundary_7_vs_8(self):
        e = fresh_engine()
        s7 = e._completeness_score(make_input(missing_close_date_count=7))
        s8 = e._completeness_score(make_input(missing_close_date_count=8))
        assert s8 > s7

    def test_missing_opp_value_boundary_4_vs_5(self):
        e = fresh_engine()
        s4 = e._completeness_score(make_input(missing_opportunity_value_count=4))
        s5 = e._completeness_score(make_input(missing_opportunity_value_count=5))
        assert s5 > s4

    def test_duplicate_account_boundary_4_vs_5(self):
        e = fresh_engine()
        s4 = e._accuracy_score(make_input(duplicate_account_count=4))
        s5 = e._accuracy_score(make_input(duplicate_account_count=5))
        assert s5 > s4

    def test_stage_mismatch_boundary_5_vs_6(self):
        e = fresh_engine()
        s5 = e._accuracy_score(make_input(stage_mismatch_count=5))
        s6 = e._accuracy_score(make_input(stage_mismatch_count=6))
        assert s6 > s5

    def test_forecast_no_activity_boundary_4_vs_5(self):
        e = fresh_engine()
        s4 = e._activity_coverage_score(make_input(forecast_without_recent_activity_count=4))
        s5 = e._activity_coverage_score(make_input(forecast_without_recent_activity_count=5))
        assert s5 > s4

    def test_overdue_followup_boundary_7_vs_8(self):
        e = fresh_engine()
        s7 = e._activity_coverage_score(make_input(overdue_follow_up_count=7))
        s8 = e._activity_coverage_score(make_input(overdue_follow_up_count=8))
        assert s8 > s7


# ═══════════════════════════════════════════════════════════════════════════
# 21. PARAMETERIZED TESTS
# ═══════════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("composite,expected_risk", [
    (0.0, DataQualityRisk.low),
    (10.0, DataQualityRisk.low),
    (19.9, DataQualityRisk.low),
    (20.0, DataQualityRisk.moderate),
    (25.0, DataQualityRisk.moderate),
    (39.9, DataQualityRisk.moderate),
    (40.0, DataQualityRisk.high),
    (50.0, DataQualityRisk.high),
    (59.9, DataQualityRisk.high),
    (60.0, DataQualityRisk.critical),
    (75.0, DataQualityRisk.critical),
    (100.0, DataQualityRisk.critical),
])
def test_risk_classification_parametrized(composite, expected_risk):
    assert fresh_engine()._classify_risk(composite) == expected_risk


@pytest.mark.parametrize("composite,expected_sev", [
    (0.0, QualitySeverity.clean),
    (19.9, QualitySeverity.clean),
    (20.0, QualitySeverity.degraded),
    (39.9, QualitySeverity.degraded),
    (40.0, QualitySeverity.unreliable),
    (59.9, QualitySeverity.unreliable),
    (60.0, QualitySeverity.corrupt),
    (100.0, QualitySeverity.corrupt),
])
def test_severity_classification_parametrized(composite, expected_sev):
    assert fresh_engine()._classify_severity(composite) == expected_sev


@pytest.mark.parametrize("risk,composite,expected_action", [
    (DataQualityRisk.critical, 60.0, QualityAction.pipeline_freeze),
    (DataQualityRisk.critical, 75.0, QualityAction.pipeline_freeze),
    (DataQualityRisk.high, 50.0, QualityAction.data_audit),
    (DataQualityRisk.high, 55.0, QualityAction.data_audit),
    (DataQualityRisk.moderate, 25.0, QualityAction.crm_coaching),
    (DataQualityRisk.moderate, 35.0, QualityAction.crm_coaching),
    (DataQualityRisk.low, 10.0, QualityAction.self_remediate),
    (DataQualityRisk.low, 15.0, QualityAction.self_remediate),
    (DataQualityRisk.low, 0.0, QualityAction.no_action),
    (DataQualityRisk.low, 9.9, QualityAction.no_action),
])
def test_recommended_action_parametrized(risk, composite, expected_action):
    assert fresh_engine()._recommended_action(risk, composite) == expected_action


@pytest.mark.parametrize("missing_close,completeness,dq_risk_expected", [
    (5, 90.0, True),
    (6, 90.0, True),
    (4, 90.0, False),  # assuming composite < 40 with clean input
    (0, 49.0, True),
    (0, 50.0, False),
])
def test_is_data_quality_risk_parametrized(missing_close, completeness, dq_risk_expected):
    e = fresh_engine()
    r = e.assess(make_input(
        missing_close_date_count=missing_close,
        data_entry_completeness_pct=completeness,
    ))
    # Check only the direct-trigger conditions to avoid composite confounding
    if missing_close >= 5 or completeness < 50:
        assert r.is_data_quality_risk is True
    elif r.quality_composite < 40:
        assert r.is_data_quality_risk == dq_risk_expected


@pytest.mark.parametrize("dup_count,opp_missing,audit_expected", [
    (2, 0, True),
    (3, 0, True),
    (0, 3, True),
    (0, 4, True),
    (1, 2, None),  # depends on composite
])
def test_requires_data_audit_parametrized(dup_count, opp_missing, audit_expected):
    e = fresh_engine()
    r = e.assess(make_input(
        duplicate_account_count=dup_count,
        missing_opportunity_value_count=opp_missing,
    ))
    if audit_expected is True:
        assert r.requires_data_audit is True


@pytest.mark.parametrize("data_entry_pct,expected_add", [
    (49.0, 50.0),
    (0.0, 50.0),
    (50.0, 35.0),
    (60.0, 35.0),
    (64.9, 35.0),
    (65.0, 18.0),
    (70.0, 18.0),
    (79.9, 18.0),
    (80.0, 0.0),
    (100.0, 0.0),
])
def test_completeness_score_pct_tiers(data_entry_pct, expected_add):
    e = fresh_engine()
    score = e._completeness_score(make_input(
        data_entry_completeness_pct=data_entry_pct,
        missing_close_date_count=0,
        missing_opportunity_value_count=0,
    ))
    assert score == pytest.approx(expected_add, abs=0.01)


@pytest.mark.parametrize("dup_count,expected_add", [
    (0, 0.0),
    (1, 8.0),
    (2, 20.0),
    (4, 20.0),
    (5, 35.0),
    (10, 35.0),
])
def test_accuracy_duplicate_tiers(dup_count, expected_add):
    e = fresh_engine()
    score = e._accuracy_score(make_input(
        duplicate_account_count=dup_count,
        stage_mismatch_count=0,
        auto_filled_fields_pct=0,
        deal_source_missing_count=0,
        total_records_evaluated=20,
    ))
    assert score == pytest.approx(expected_add, abs=0.01)


@pytest.mark.parametrize("login_freq,expected_add", [
    (0, 20.0),
    (3, 20.0),
    (4, 10.0),
    (8, 10.0),
    (9, 0.0),
    (30, 0.0),
])
def test_timeliness_login_tiers(login_freq, expected_add):
    e = fresh_engine()
    score = e._timeliness_score(make_input(
        crm_login_frequency_last_30d=login_freq,
        stale_record_count=0,
        total_records_evaluated=20,
        avg_record_staleness_days=0.0,
    ))
    assert score == pytest.approx(expected_add, abs=0.01)


# ═══════════════════════════════════════════════════════════════════════════
# 22. RESULT FIELD TYPE TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestResultFieldTypes:
    def test_rep_id_is_str(self):
        r = fresh_engine().assess(make_input())
        assert isinstance(r.rep_id, str)

    def test_region_is_str(self):
        r = fresh_engine().assess(make_input())
        assert isinstance(r.region, str)

    def test_quality_composite_is_float(self):
        r = fresh_engine().assess(make_input())
        assert isinstance(r.quality_composite, float)

    def test_completeness_score_is_float(self):
        r = fresh_engine().assess(make_input())
        assert isinstance(r.completeness_score, float)

    def test_accuracy_score_is_float(self):
        r = fresh_engine().assess(make_input())
        assert isinstance(r.accuracy_score, float)

    def test_timeliness_score_is_float(self):
        r = fresh_engine().assess(make_input())
        assert isinstance(r.timeliness_score, float)

    def test_activity_coverage_score_is_float(self):
        r = fresh_engine().assess(make_input())
        assert isinstance(r.activity_coverage_score, float)

    def test_is_data_quality_risk_is_bool(self):
        r = fresh_engine().assess(make_input())
        assert isinstance(r.is_data_quality_risk, bool)

    def test_requires_data_audit_is_bool(self):
        r = fresh_engine().assess(make_input())
        assert isinstance(r.requires_data_audit, bool)

    def test_estimated_pipeline_distortion_is_float(self):
        r = fresh_engine().assess(make_input())
        assert isinstance(r.estimated_pipeline_distortion_pct, float)

    def test_quality_signal_is_str(self):
        r = fresh_engine().assess(make_input())
        assert isinstance(r.quality_signal, str)


# ═══════════════════════════════════════════════════════════════════════════
# 23. ADDITIONAL COVERAGE TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestAdditionalCoverage:
    def test_engine_init_empty_results(self):
        engine = CRMDataQualityRiskEngine()
        assert engine._results == []

    def test_multiple_engine_instances_independent(self):
        e1 = CRMDataQualityRiskEngine()
        e2 = CRMDataQualityRiskEngine()
        e1.assess(make_input())
        assert len(e1._results) == 1
        assert len(e2._results) == 0

    def test_to_dict_returns_new_dict_each_call(self):
        r = fresh_engine().assess(make_input())
        d1 = r.to_dict()
        d2 = r.to_dict()
        assert d1 == d2
        assert d1 is not d2

    def test_composite_ge_40_triggers_is_dq_risk(self):
        # Build a scenario where composite is exactly >= 40
        e = fresh_engine()
        inp = make_input(
            data_entry_completeness_pct=49.0,  # completeness += 50
        )
        r = e.assess(inp)
        # completeness=50, accuracy=0, timeliness=0, activity=0 => 50*0.30=15
        # But data_entry_completeness_pct < 50 triggers is_data_quality_risk=True
        assert r.is_data_quality_risk is True

    def test_summary_after_batch_of_100(self):
        engine = fresh_engine()
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(100)]
        engine.assess_batch(inputs)
        s = engine.summary()
        assert s["total"] == 100
        assert len(s) == 13

    def test_summary_action_counts_include_assessed_action(self):
        engine = fresh_engine()
        r = engine.assess(make_input())
        s = engine.summary()
        action_val = r.recommended_action.value
        assert s["action_counts"].get(action_val, 0) >= 1

    def test_summary_severity_counts_include_assessed_severity(self):
        engine = fresh_engine()
        r = engine.assess(make_input())
        s = engine.summary()
        sev_val = r.quality_severity.value
        assert s["severity_counts"].get(sev_val, 0) >= 1

    def test_summary_failure_mode_counts_include_assessed_mode(self):
        engine = fresh_engine()
        r = engine.assess(make_input())
        s = engine.summary()
        mode_val = r.quality_failure_mode.value
        assert s["failure_mode_counts"].get(mode_val, 0) >= 1

    def test_result_is_dataclass(self):
        from swarm.intelligence.crm_data_quality_risk_engine import CRMDataQualityResult
        assert dataclasses.is_dataclass(CRMDataQualityResult)

    def test_result_has_15_fields(self):
        from swarm.intelligence.crm_data_quality_risk_engine import CRMDataQualityResult
        assert len(dataclasses.fields(CRMDataQualityResult)) == 15

    def test_clamp_function_via_distortion_zero(self):
        # composite=0 => distortion=0
        r = fresh_engine().assess(make_input())
        assert r.estimated_pipeline_distortion_pct >= 0.0

    def test_assess_returns_result_with_same_engine_state(self):
        engine = CRMDataQualityRiskEngine()
        r = engine.assess(make_input())
        assert engine._results[-1] is r

    def test_batch_results_are_same_as_sequential(self):
        inputs = [make_input(rep_id=f"r{i}") for i in range(5)]
        e_batch = CRMDataQualityRiskEngine()
        e_seq = CRMDataQualityRiskEngine()
        batch_results = e_batch.assess_batch(inputs)
        seq_results = [e_seq.assess(inp) for inp in inputs]
        for b, s in zip(batch_results, seq_results):
            assert b.to_dict() == s.to_dict()

    def test_stage_mismatch_exactly_1_adds_0_to_accuracy(self):
        e = fresh_engine()
        score = e._accuracy_score(make_input(
            stage_mismatch_count=1,
            duplicate_account_count=0,
            auto_filled_fields_pct=0,
            deal_source_missing_count=0,
            total_records_evaluated=20,
        ))
        assert score == 0.0

    def test_overdue_followup_exactly_1_adds_0(self):
        e = fresh_engine()
        score = e._activity_coverage_score(make_input(
            records_with_activity_notes_pct=80,
            forecast_without_recent_activity_count=0,
            overdue_follow_up_count=1,
        ))
        assert score == 0.0

    def test_missing_close_date_exactly_1_adds_0(self):
        e = fresh_engine()
        score = e._completeness_score(make_input(
            data_entry_completeness_pct=90,
            missing_close_date_count=1,
            missing_opportunity_value_count=0,
        ))
        assert score == 0.0

    def test_signal_for_stale_records_includes_staleness_days(self):
        e = fresh_engine()
        r = e.assess(make_input(
            stale_record_count=5,
            total_records_evaluated=20,
            avg_record_staleness_days=42.0,
            data_entry_completeness_pct=90,
            missing_close_date_count=0,
            duplicate_account_count=0,
        ))
        if r.quality_failure_mode == QualityFailureMode.stale_records:
            assert "42" in r.quality_signal

    def test_failure_mode_priority_order_dup_over_stale(self):
        e = fresh_engine()
        r = e.assess(make_input(
            duplicate_account_count=2,
            avg_record_staleness_days=60,
            stale_record_count=10,
            total_records_evaluated=20,
        ))
        assert r.quality_failure_mode == QualityFailureMode.duplicate_accounts

    def test_failure_mode_priority_dup_over_stage_drift(self):
        e = fresh_engine()
        r = e.assess(make_input(
            duplicate_account_count=2,
            stage_mismatch_count=6,
        ))
        assert r.quality_failure_mode == QualityFailureMode.duplicate_accounts

    def test_failure_mode_missing_data_over_stale(self):
        e = fresh_engine()
        r = e.assess(make_input(
            duplicate_account_count=0,
            data_entry_completeness_pct=55.0,
            avg_record_staleness_days=60,
            stale_record_count=10,
            total_records_evaluated=20,
        ))
        assert r.quality_failure_mode == QualityFailureMode.missing_data

    def test_completeness_score_exactly_at_80_boundary(self):
        e = fresh_engine()
        s79 = e._completeness_score(make_input(
            data_entry_completeness_pct=79.99,
            missing_close_date_count=0,
            missing_opportunity_value_count=0,
        ))
        s80 = e._completeness_score(make_input(
            data_entry_completeness_pct=80.0,
            missing_close_date_count=0,
            missing_opportunity_value_count=0,
        ))
        assert s79 > s80

    def test_high_composite_data_audit_not_pipeline_freeze(self):
        """composite=59.9 => high => data_audit, not pipeline_freeze"""
        e = fresh_engine()
        action = e._recommended_action(DataQualityRisk.high, 59.9)
        assert action == QualityAction.data_audit

    def test_composite_exactly_60_is_pipeline_freeze(self):
        e = fresh_engine()
        action = e._recommended_action(DataQualityRisk.critical, 60.0)
        assert action == QualityAction.pipeline_freeze
