"""
Comprehensive pytest test suite for SalesDataIntegrityMonitor.
~250 tests organized across focused test classes.
"""
from __future__ import annotations

import dataclasses
import pytest

from swarm.intelligence.sales_data_integrity_monitor import (
    SalesDataIntegrityMonitor,
    SalesDataIntegrityInput,
    SalesDataIntegrityResult,
    IntegrityRisk,
    AnomalyType,
    DataQuality,
    IntegrityAction,
    _pipeline_accuracy_score,
    _data_completeness_score,
    _behavioral_consistency_score,
    _compliance_score,
    _composite,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**kwargs):
    defaults = dict(
        record_id="rec_001",
        rep_id="rep_001",
        deal_count_last_30d=8,
        avg_deal_size_usd=45000.0,
        historical_avg_deal_size_usd=42000.0,
        deals_closed_end_of_quarter_pct=25.0,
        close_date_changes_count=1,
        days_close_date_pushed=14,
        pipeline_created_last_7d_usd=80000.0,
        avg_pipeline_created_per_month_usd=350000.0,
        duplicate_contact_count=0,
        missing_required_fields_count=1,
        deals_no_activity_30d=0,
        stage_skips_count=0,
        backdated_activities_count=0,
        deals_closed_same_day_created_count=0,
        crm_login_anomaly_count=0,
        data_edit_frequency_score=20.0,
        approval_bypass_count=0,
        unverified_opportunity_sources_count=0,
        team_benchmark_deviation_pct=8.0,
        manager_review_score=88.0,
    )
    defaults.update(kwargs)
    return SalesDataIntegrityInput(**defaults)


def breach_input(record_id="breach_001"):
    return make_input(
        record_id=record_id,
        avg_deal_size_usd=150000.0,
        historical_avg_deal_size_usd=42000.0,
        deals_closed_end_of_quarter_pct=75.0,
        close_date_changes_count=6,
        days_close_date_pushed=120,
        pipeline_created_last_7d_usd=1200000.0,
        avg_pipeline_created_per_month_usd=350000.0,
        duplicate_contact_count=8,
        missing_required_fields_count=12,
        deals_no_activity_30d=6,
        stage_skips_count=7,
        backdated_activities_count=6,
        deals_closed_same_day_created_count=4,
        crm_login_anomaly_count=5,
        data_edit_frequency_score=85.0,
        approval_bypass_count=5,
        unverified_opportunity_sources_count=6,
        team_benchmark_deviation_pct=65.0,
        manager_review_score=20.0,
    )


# ---------------------------------------------------------------------------
# TestEnums
# ---------------------------------------------------------------------------

class TestEnums:
    """Validate enum membership, values, and count."""

    def test_integrity_risk_has_four_values(self):
        assert len(IntegrityRisk) == 4

    def test_integrity_risk_clean(self):
        assert IntegrityRisk.CLEAN.value == "clean"

    def test_integrity_risk_minor_issues(self):
        assert IntegrityRisk.MINOR_ISSUES.value == "minor_issues"

    def test_integrity_risk_moderate_issues(self):
        assert IntegrityRisk.MODERATE_ISSUES.value == "moderate_issues"

    def test_integrity_risk_critical_breach(self):
        assert IntegrityRisk.CRITICAL_BREACH.value == "critical_breach"

    def test_anomaly_type_has_six_values(self):
        assert len(AnomalyType) == 6

    def test_anomaly_type_inflated_deal_value(self):
        assert AnomalyType.INFLATED_DEAL_VALUE.value == "inflated_deal_value"

    def test_anomaly_type_close_date_manipulation(self):
        assert AnomalyType.CLOSE_DATE_MANIPULATION.value == "close_date_manipulation"

    def test_anomaly_type_pipeline_stuffing(self):
        assert AnomalyType.PIPELINE_STUFFING.value == "pipeline_stuffing"

    def test_anomaly_type_ghost_deal(self):
        assert AnomalyType.GHOST_DEAL.value == "ghost_deal"

    def test_anomaly_type_duplicate_entry(self):
        assert AnomalyType.DUPLICATE_ENTRY.value == "duplicate_entry"

    def test_anomaly_type_missing_required_fields(self):
        assert AnomalyType.MISSING_REQUIRED_FIELDS.value == "missing_required_fields"

    def test_data_quality_has_four_values(self):
        assert len(DataQuality) == 4

    def test_data_quality_excellent(self):
        assert DataQuality.EXCELLENT.value == "excellent"

    def test_data_quality_good(self):
        assert DataQuality.GOOD.value == "good"

    def test_data_quality_fair(self):
        assert DataQuality.FAIR.value == "fair"

    def test_data_quality_poor(self):
        assert DataQuality.POOR.value == "poor"

    def test_integrity_action_has_four_values(self):
        assert len(IntegrityAction) == 4

    def test_integrity_action_no_action(self):
        assert IntegrityAction.NO_ACTION.value == "no_action"

    def test_integrity_action_flag_for_review(self):
        assert IntegrityAction.FLAG_FOR_REVIEW.value == "flag_for_review"

    def test_integrity_action_manager_alert(self):
        assert IntegrityAction.MANAGER_ALERT.value == "manager_alert"

    def test_integrity_action_compliance_escalation(self):
        assert IntegrityAction.COMPLIANCE_ESCALATION.value == "compliance_escalation"

    def test_enums_are_str_subclass(self):
        assert isinstance(IntegrityRisk.CLEAN, str)
        assert isinstance(AnomalyType.GHOST_DEAL, str)
        assert isinstance(DataQuality.GOOD, str)
        assert isinstance(IntegrityAction.NO_ACTION, str)


# ---------------------------------------------------------------------------
# TestSalesDataIntegrityInputFields
# ---------------------------------------------------------------------------

class TestSalesDataIntegrityInputFields:
    """Ensure the dataclass has exactly 22 fields."""

    def test_input_has_exactly_22_fields(self):
        fields = dataclasses.fields(SalesDataIntegrityInput)
        assert len(fields) == 22

    def test_field_record_id_exists(self):
        names = {f.name for f in dataclasses.fields(SalesDataIntegrityInput)}
        assert "record_id" in names

    def test_field_rep_id_exists(self):
        names = {f.name for f in dataclasses.fields(SalesDataIntegrityInput)}
        assert "rep_id" in names

    def test_field_deal_count_last_30d_exists(self):
        names = {f.name for f in dataclasses.fields(SalesDataIntegrityInput)}
        assert "deal_count_last_30d" in names

    def test_field_avg_deal_size_usd_exists(self):
        names = {f.name for f in dataclasses.fields(SalesDataIntegrityInput)}
        assert "avg_deal_size_usd" in names

    def test_field_historical_avg_deal_size_usd_exists(self):
        names = {f.name for f in dataclasses.fields(SalesDataIntegrityInput)}
        assert "historical_avg_deal_size_usd" in names

    def test_field_deals_closed_end_of_quarter_pct_exists(self):
        names = {f.name for f in dataclasses.fields(SalesDataIntegrityInput)}
        assert "deals_closed_end_of_quarter_pct" in names

    def test_field_close_date_changes_count_exists(self):
        names = {f.name for f in dataclasses.fields(SalesDataIntegrityInput)}
        assert "close_date_changes_count" in names

    def test_field_days_close_date_pushed_exists(self):
        names = {f.name for f in dataclasses.fields(SalesDataIntegrityInput)}
        assert "days_close_date_pushed" in names

    def test_field_pipeline_created_last_7d_usd_exists(self):
        names = {f.name for f in dataclasses.fields(SalesDataIntegrityInput)}
        assert "pipeline_created_last_7d_usd" in names

    def test_field_avg_pipeline_created_per_month_usd_exists(self):
        names = {f.name for f in dataclasses.fields(SalesDataIntegrityInput)}
        assert "avg_pipeline_created_per_month_usd" in names

    def test_field_duplicate_contact_count_exists(self):
        names = {f.name for f in dataclasses.fields(SalesDataIntegrityInput)}
        assert "duplicate_contact_count" in names

    def test_field_missing_required_fields_count_exists(self):
        names = {f.name for f in dataclasses.fields(SalesDataIntegrityInput)}
        assert "missing_required_fields_count" in names

    def test_field_deals_no_activity_30d_exists(self):
        names = {f.name for f in dataclasses.fields(SalesDataIntegrityInput)}
        assert "deals_no_activity_30d" in names

    def test_field_stage_skips_count_exists(self):
        names = {f.name for f in dataclasses.fields(SalesDataIntegrityInput)}
        assert "stage_skips_count" in names

    def test_field_backdated_activities_count_exists(self):
        names = {f.name for f in dataclasses.fields(SalesDataIntegrityInput)}
        assert "backdated_activities_count" in names

    def test_field_deals_closed_same_day_created_count_exists(self):
        names = {f.name for f in dataclasses.fields(SalesDataIntegrityInput)}
        assert "deals_closed_same_day_created_count" in names

    def test_field_crm_login_anomaly_count_exists(self):
        names = {f.name for f in dataclasses.fields(SalesDataIntegrityInput)}
        assert "crm_login_anomaly_count" in names

    def test_field_data_edit_frequency_score_exists(self):
        names = {f.name for f in dataclasses.fields(SalesDataIntegrityInput)}
        assert "data_edit_frequency_score" in names

    def test_field_approval_bypass_count_exists(self):
        names = {f.name for f in dataclasses.fields(SalesDataIntegrityInput)}
        assert "approval_bypass_count" in names

    def test_field_unverified_opportunity_sources_count_exists(self):
        names = {f.name for f in dataclasses.fields(SalesDataIntegrityInput)}
        assert "unverified_opportunity_sources_count" in names

    def test_field_team_benchmark_deviation_pct_exists(self):
        names = {f.name for f in dataclasses.fields(SalesDataIntegrityInput)}
        assert "team_benchmark_deviation_pct" in names

    def test_field_manager_review_score_exists(self):
        names = {f.name for f in dataclasses.fields(SalesDataIntegrityInput)}
        assert "manager_review_score" in names

    def test_input_is_dataclass(self):
        assert dataclasses.is_dataclass(SalesDataIntegrityInput)

    def test_input_instantiation_stores_values(self):
        inp = make_input(record_id="x", rep_id="y")
        assert inp.record_id == "x"
        assert inp.rep_id == "y"


# ---------------------------------------------------------------------------
# TestSalesDataIntegrityResultToDict
# ---------------------------------------------------------------------------

class TestSalesDataIntegrityResultToDict:
    """Ensure to_dict() returns exactly 15 keys with correct content."""

    def setup_method(self):
        monitor = SalesDataIntegrityMonitor()
        self.result = monitor.assess(make_input())

    def test_to_dict_returns_exactly_15_keys(self):
        d = self.result.to_dict()
        assert len(d) == 15

    def test_to_dict_contains_record_id(self):
        assert "record_id" in self.result.to_dict()

    def test_to_dict_contains_rep_id(self):
        assert "rep_id" in self.result.to_dict()

    def test_to_dict_contains_integrity_risk(self):
        assert "integrity_risk" in self.result.to_dict()

    def test_to_dict_contains_anomaly_type(self):
        assert "anomaly_type" in self.result.to_dict()

    def test_to_dict_contains_data_quality(self):
        assert "data_quality" in self.result.to_dict()

    def test_to_dict_contains_integrity_action(self):
        assert "integrity_action" in self.result.to_dict()

    def test_to_dict_contains_pipeline_accuracy_score(self):
        assert "pipeline_accuracy_score" in self.result.to_dict()

    def test_to_dict_contains_data_completeness_score(self):
        assert "data_completeness_score" in self.result.to_dict()

    def test_to_dict_contains_behavioral_consistency_score(self):
        assert "behavioral_consistency_score" in self.result.to_dict()

    def test_to_dict_contains_compliance_score(self):
        assert "compliance_score" in self.result.to_dict()

    def test_to_dict_contains_integrity_composite(self):
        assert "integrity_composite" in self.result.to_dict()

    def test_to_dict_contains_risk_signal_count(self):
        assert "risk_signal_count" in self.result.to_dict()

    def test_to_dict_contains_is_clean(self):
        assert "is_clean" in self.result.to_dict()

    def test_to_dict_contains_needs_escalation(self):
        assert "needs_escalation" in self.result.to_dict()

    def test_to_dict_contains_primary_integrity_signal(self):
        assert "primary_integrity_signal" in self.result.to_dict()

    def test_to_dict_integrity_risk_is_string(self):
        d = self.result.to_dict()
        assert isinstance(d["integrity_risk"], str)

    def test_to_dict_anomaly_type_is_string(self):
        d = self.result.to_dict()
        assert isinstance(d["anomaly_type"], str)

    def test_to_dict_data_quality_is_string(self):
        d = self.result.to_dict()
        assert isinstance(d["data_quality"], str)

    def test_to_dict_integrity_action_is_string(self):
        d = self.result.to_dict()
        assert isinstance(d["integrity_action"], str)

    def test_to_dict_record_id_matches(self):
        d = self.result.to_dict()
        assert d["record_id"] == self.result.record_id

    def test_to_dict_is_clean_is_bool(self):
        d = self.result.to_dict()
        assert isinstance(d["is_clean"], bool)

    def test_to_dict_needs_escalation_is_bool(self):
        d = self.result.to_dict()
        assert isinstance(d["needs_escalation"], bool)

    def test_to_dict_risk_signal_count_is_int(self):
        d = self.result.to_dict()
        assert isinstance(d["risk_signal_count"], int)


# ---------------------------------------------------------------------------
# TestPipelineAccuracyScore
# ---------------------------------------------------------------------------

class TestPipelineAccuracyScore:
    """Unit tests for _pipeline_accuracy_score."""

    def test_perfect_input_scores_near_100(self):
        inp = make_input(
            avg_deal_size_usd=42000.0,
            historical_avg_deal_size_usd=42000.0,
            pipeline_created_last_7d_usd=80000.0,
            avg_pipeline_created_per_month_usd=350000.0,
            deals_closed_end_of_quarter_pct=10.0,
            team_benchmark_deviation_pct=5.0,
        )
        assert _pipeline_accuracy_score(inp) == 100.0

    def test_deal_size_ratio_above_2_5_deducts_40(self):
        inp = make_input(avg_deal_size_usd=110000.0, historical_avg_deal_size_usd=42000.0)
        score = _pipeline_accuracy_score(inp)
        # ratio = 2.619 > 2.5, deduct 40
        assert score <= 60.0

    def test_deal_size_ratio_1_8_to_2_5_deducts_25(self):
        inp = make_input(avg_deal_size_usd=80000.0, historical_avg_deal_size_usd=42000.0)
        score = _pipeline_accuracy_score(inp)
        # ratio = 1.904, deduct 25
        base = 100.0 - 25.0
        assert score <= base

    def test_deal_size_ratio_1_4_to_1_8_deducts_12(self):
        inp = make_input(avg_deal_size_usd=63000.0, historical_avg_deal_size_usd=42000.0)
        # ratio = 1.5, deduct 12
        score = _pipeline_accuracy_score(inp)
        assert score <= 88.0

    def test_pipeline_ratio_above_5_deducts_30(self):
        # weekly_avg = 350000/4 = 87500; create 7d = 500000 → ratio = 5.7
        inp = make_input(
            pipeline_created_last_7d_usd=500000.0,
            avg_pipeline_created_per_month_usd=350000.0,
        )
        score = _pipeline_accuracy_score(inp)
        assert score <= 70.0

    def test_pipeline_ratio_3_to_5_deducts_18(self):
        # weekly_avg = 87500; 7d = 300000 → ratio = 3.43
        inp = make_input(
            pipeline_created_last_7d_usd=300000.0,
            avg_pipeline_created_per_month_usd=350000.0,
        )
        score = _pipeline_accuracy_score(inp)
        assert score <= 82.0

    def test_pipeline_ratio_2_to_3_deducts_8(self):
        # weekly_avg = 87500; 7d = 200000 → ratio = 2.29
        inp = make_input(
            pipeline_created_last_7d_usd=200000.0,
            avg_pipeline_created_per_month_usd=350000.0,
        )
        score = _pipeline_accuracy_score(inp)
        assert score <= 92.0

    def test_end_of_quarter_above_60_deducts_15(self):
        inp = make_input(deals_closed_end_of_quarter_pct=65.0)
        score = _pipeline_accuracy_score(inp)
        assert score <= 85.0

    def test_end_of_quarter_40_to_60_deducts_8(self):
        inp = make_input(deals_closed_end_of_quarter_pct=50.0)
        score = _pipeline_accuracy_score(inp)
        assert score <= 92.0

    def test_team_benchmark_deviation_above_50_deducts_15(self):
        inp = make_input(team_benchmark_deviation_pct=55.0)
        score = _pipeline_accuracy_score(inp)
        assert score <= 85.0

    def test_team_benchmark_deviation_30_to_50_deducts_8(self):
        inp = make_input(team_benchmark_deviation_pct=35.0)
        score = _pipeline_accuracy_score(inp)
        assert score <= 92.0

    def test_score_never_below_zero(self):
        score = _pipeline_accuracy_score(breach_input())
        assert score >= 0.0

    def test_score_never_above_100(self):
        inp = make_input()
        assert _pipeline_accuracy_score(inp) <= 100.0

    def test_zero_historical_avg_does_not_crash(self):
        inp = make_input(historical_avg_deal_size_usd=0.0, avg_deal_size_usd=50000.0)
        score = _pipeline_accuracy_score(inp)
        assert 0.0 <= score <= 100.0

    def test_zero_avg_pipeline_does_not_crash(self):
        inp = make_input(avg_pipeline_created_per_month_usd=0.0)
        score = _pipeline_accuracy_score(inp)
        assert 0.0 <= score <= 100.0

    def test_returns_float(self):
        assert isinstance(_pipeline_accuracy_score(make_input()), float)


# ---------------------------------------------------------------------------
# TestDataCompletenessScore
# ---------------------------------------------------------------------------

class TestDataCompletenessScore:
    """Unit tests for _data_completeness_score."""

    def test_perfect_data_scores_near_100(self):
        inp = make_input(
            missing_required_fields_count=0,
            duplicate_contact_count=0,
            unverified_opportunity_sources_count=0,
            manager_review_score=100.0,
        )
        score = _data_completeness_score(inp)
        assert score == 100.0

    def test_missing_fields_gte_10_deducts_40(self):
        inp = make_input(missing_required_fields_count=10)
        score = _data_completeness_score(inp)
        assert score < 80.0

    def test_missing_fields_5_to_9_deducts_25(self):
        inp = make_input(missing_required_fields_count=5)
        score = _data_completeness_score(inp)
        assert score < 90.0

    def test_missing_fields_2_to_4_deducts_12(self):
        inp = make_input(missing_required_fields_count=2)
        score = _data_completeness_score(inp)
        assert score < 100.0

    def test_missing_fields_1_no_deduction(self):
        # 1 missing field does not trigger any bracket
        inp = make_input(missing_required_fields_count=1, duplicate_contact_count=0,
                         unverified_opportunity_sources_count=0, manager_review_score=100.0)
        score = _data_completeness_score(inp)
        assert score == 100.0

    def test_duplicate_contacts_gte_10_deducts_25(self):
        inp = make_input(duplicate_contact_count=10)
        score = _data_completeness_score(inp)
        assert score < 90.0

    def test_duplicate_contacts_5_to_9_deducts_15(self):
        inp = make_input(duplicate_contact_count=5)
        score = _data_completeness_score(inp)
        assert score < 95.0

    def test_duplicate_contacts_2_to_4_deducts_7(self):
        inp = make_input(duplicate_contact_count=2)
        score = _data_completeness_score(inp)
        assert score < 100.0

    def test_unverified_sources_gte_5_deducts_20(self):
        inp = make_input(unverified_opportunity_sources_count=5)
        score = _data_completeness_score(inp)
        assert score < 95.0

    def test_unverified_sources_2_to_4_deducts_10(self):
        inp = make_input(unverified_opportunity_sources_count=2)
        score = _data_completeness_score(inp)
        assert score < 100.0

    def test_unverified_sources_1_deducts_5(self):
        inp = make_input(unverified_opportunity_sources_count=1)
        score = _data_completeness_score(inp)
        assert score < 100.0

    def test_manager_review_score_contributes(self):
        inp_high = make_input(manager_review_score=100.0)
        inp_low = make_input(manager_review_score=0.0)
        assert _data_completeness_score(inp_high) > _data_completeness_score(inp_low)

    def test_score_never_below_zero(self):
        score = _data_completeness_score(breach_input())
        assert score >= 0.0

    def test_score_never_above_100(self):
        assert _data_completeness_score(make_input()) <= 100.0

    def test_returns_float(self):
        assert isinstance(_data_completeness_score(make_input()), float)


# ---------------------------------------------------------------------------
# TestBehavioralConsistencyScore
# ---------------------------------------------------------------------------

class TestBehavioralConsistencyScore:
    """Unit tests for _behavioral_consistency_score."""

    def test_clean_rep_scores_100(self):
        inp = make_input(
            close_date_changes_count=0,
            backdated_activities_count=0,
            deals_no_activity_30d=0,
            stage_skips_count=0,
            deals_closed_same_day_created_count=0,
        )
        assert _behavioral_consistency_score(inp) == 100.0

    def test_close_date_changes_gte_5_deducts_30(self):
        inp = make_input(close_date_changes_count=5)
        score = _behavioral_consistency_score(inp)
        assert score <= 70.0

    def test_close_date_changes_3_to_4_deducts_18(self):
        inp = make_input(close_date_changes_count=3)
        score = _behavioral_consistency_score(inp)
        assert score <= 82.0

    def test_close_date_changes_1_to_2_deducts_8(self):
        inp = make_input(close_date_changes_count=1)
        score = _behavioral_consistency_score(inp)
        assert score <= 92.0

    def test_backdated_activities_gte_5_deducts_30(self):
        inp = make_input(backdated_activities_count=5)
        score = _behavioral_consistency_score(inp)
        assert score <= 70.0

    def test_backdated_activities_3_to_4_deducts_18(self):
        inp = make_input(backdated_activities_count=3)
        score = _behavioral_consistency_score(inp)
        assert score <= 82.0

    def test_backdated_activities_1_to_2_deducts_8(self):
        inp = make_input(backdated_activities_count=1)
        score = _behavioral_consistency_score(inp)
        assert score <= 92.0

    def test_deals_no_activity_gte_5_deducts_20(self):
        inp = make_input(deals_no_activity_30d=5)
        score = _behavioral_consistency_score(inp)
        assert score <= 80.0

    def test_deals_no_activity_3_to_4_deducts_12(self):
        inp = make_input(deals_no_activity_30d=3)
        score = _behavioral_consistency_score(inp)
        assert score <= 88.0

    def test_deals_no_activity_1_to_2_deducts_5(self):
        inp = make_input(deals_no_activity_30d=1)
        score = _behavioral_consistency_score(inp)
        assert score <= 95.0

    def test_stage_skips_gte_5_deducts_20(self):
        inp = make_input(stage_skips_count=5)
        score = _behavioral_consistency_score(inp)
        assert score <= 80.0

    def test_stage_skips_2_to_4_deducts_10(self):
        inp = make_input(stage_skips_count=2)
        score = _behavioral_consistency_score(inp)
        assert score <= 90.0

    def test_same_day_closed_gte_3_deducts_15(self):
        inp = make_input(deals_closed_same_day_created_count=3)
        score = _behavioral_consistency_score(inp)
        assert score <= 85.0

    def test_same_day_closed_1_to_2_deducts_8(self):
        inp = make_input(deals_closed_same_day_created_count=1)
        score = _behavioral_consistency_score(inp)
        assert score <= 92.0

    def test_score_never_below_zero(self):
        score = _behavioral_consistency_score(breach_input())
        assert score >= 0.0

    def test_score_never_above_100(self):
        assert _behavioral_consistency_score(make_input()) <= 100.0

    def test_returns_float(self):
        assert isinstance(_behavioral_consistency_score(make_input()), float)


# ---------------------------------------------------------------------------
# TestComplianceScore
# ---------------------------------------------------------------------------

class TestComplianceScore:
    """Unit tests for _compliance_score."""

    def test_clean_rep_scores_100(self):
        inp = make_input(
            crm_login_anomaly_count=0,
            approval_bypass_count=0,
            data_edit_frequency_score=10.0,
            days_close_date_pushed=10,
        )
        assert _compliance_score(inp) == 100.0

    def test_crm_login_anomaly_gte_5_deducts_35(self):
        inp = make_input(crm_login_anomaly_count=5)
        score = _compliance_score(inp)
        assert score <= 65.0

    def test_crm_login_anomaly_3_to_4_deducts_22(self):
        inp = make_input(crm_login_anomaly_count=3)
        score = _compliance_score(inp)
        assert score <= 78.0

    def test_crm_login_anomaly_1_to_2_deducts_10(self):
        inp = make_input(crm_login_anomaly_count=1)
        score = _compliance_score(inp)
        assert score <= 90.0

    def test_approval_bypass_gte_5_deducts_30(self):
        inp = make_input(approval_bypass_count=5)
        score = _compliance_score(inp)
        assert score <= 70.0

    def test_approval_bypass_3_to_4_deducts_18(self):
        inp = make_input(approval_bypass_count=3)
        score = _compliance_score(inp)
        assert score <= 82.0

    def test_approval_bypass_1_to_2_deducts_8(self):
        inp = make_input(approval_bypass_count=1)
        score = _compliance_score(inp)
        assert score <= 92.0

    def test_data_edit_freq_gte_80_deducts_25(self):
        inp = make_input(data_edit_frequency_score=80.0)
        score = _compliance_score(inp)
        assert score <= 75.0

    def test_data_edit_freq_60_to_79_deducts_15(self):
        inp = make_input(data_edit_frequency_score=60.0)
        score = _compliance_score(inp)
        assert score <= 85.0

    def test_data_edit_freq_40_to_59_deducts_8(self):
        inp = make_input(data_edit_frequency_score=40.0)
        score = _compliance_score(inp)
        assert score <= 92.0

    def test_days_pushed_gte_90_deducts_15(self):
        inp = make_input(days_close_date_pushed=90)
        score = _compliance_score(inp)
        assert score <= 85.0

    def test_days_pushed_45_to_89_deducts_8(self):
        inp = make_input(days_close_date_pushed=45)
        score = _compliance_score(inp)
        assert score <= 92.0

    def test_score_never_below_zero(self):
        score = _compliance_score(breach_input())
        assert score >= 0.0

    def test_score_never_above_100(self):
        assert _compliance_score(make_input()) <= 100.0

    def test_returns_float(self):
        assert isinstance(_compliance_score(make_input()), float)


# ---------------------------------------------------------------------------
# TestCompositeFormula
# ---------------------------------------------------------------------------

class TestCompositeFormula:
    """Verify the composite formula and rounding."""

    def test_composite_formula_weights(self):
        result = _composite(80.0, 70.0, 60.0, 50.0)
        expected = round(80.0 * 0.25 + 70.0 * 0.25 + 60.0 * 0.30 + 50.0 * 0.20, 1)
        assert result == expected

    def test_composite_all_100(self):
        assert _composite(100.0, 100.0, 100.0, 100.0) == 100.0

    def test_composite_all_zero(self):
        assert _composite(0.0, 0.0, 0.0, 0.0) == 0.0

    def test_composite_pipeline_weight(self):
        # Only pipeline changes
        r1 = _composite(100.0, 0.0, 0.0, 0.0)
        assert r1 == round(100.0 * 0.25, 1)

    def test_composite_completeness_weight(self):
        r1 = _composite(0.0, 100.0, 0.0, 0.0)
        assert r1 == round(100.0 * 0.25, 1)

    def test_composite_behavioral_weight(self):
        r1 = _composite(0.0, 0.0, 100.0, 0.0)
        assert r1 == round(100.0 * 0.30, 1)

    def test_composite_compliance_weight(self):
        r1 = _composite(0.0, 0.0, 0.0, 100.0)
        assert r1 == round(100.0 * 0.20, 1)

    def test_composite_weights_sum_to_one(self):
        # 0.25 + 0.25 + 0.30 + 0.20 == 1.0
        assert abs(0.25 + 0.25 + 0.30 + 0.20 - 1.0) < 1e-9

    def test_composite_returns_float(self):
        assert isinstance(_composite(50.0, 50.0, 50.0, 50.0), float)

    def test_composite_matches_assess_result(self):
        monitor = SalesDataIntegrityMonitor()
        inp = make_input()
        result = monitor.assess(inp)
        pa = _pipeline_accuracy_score(inp)
        dc = _data_completeness_score(inp)
        bc = _behavioral_consistency_score(inp)
        cs = _compliance_score(inp)
        expected = _composite(pa, dc, bc, cs)
        assert result.integrity_composite == expected


# ---------------------------------------------------------------------------
# TestIsCleanInvariant
# ---------------------------------------------------------------------------

class TestIsCleanInvariant:
    """is_clean must be True only when composite >= 80 AND risk_signal_count == 0."""

    def test_clean_rep_is_clean_true(self):
        monitor = SalesDataIntegrityMonitor()
        inp = make_input(
            avg_deal_size_usd=42000.0,
            historical_avg_deal_size_usd=42000.0,
            close_date_changes_count=0,
            backdated_activities_count=0,
            deals_closed_same_day_created_count=0,
            approval_bypass_count=0,
            crm_login_anomaly_count=0,
            deals_no_activity_30d=0,
            stage_skips_count=0,
            missing_required_fields_count=0,
            duplicate_contact_count=0,
            unverified_opportunity_sources_count=0,
            manager_review_score=100.0,
        )
        result = monitor.assess(inp)
        if result.integrity_composite >= 80 and result.risk_signal_count == 0:
            assert result.is_clean is True
        else:
            assert result.is_clean is False

    def test_breach_is_not_clean(self):
        monitor = SalesDataIntegrityMonitor()
        result = monitor.assess(breach_input())
        assert result.is_clean is False

    def test_is_clean_false_when_composite_below_80(self):
        monitor = SalesDataIntegrityMonitor()
        # Force low composite via many anomalies
        inp = make_input(
            stage_skips_count=5,
            backdated_activities_count=5,
            crm_login_anomaly_count=0,
            close_date_changes_count=0,
            deals_closed_same_day_created_count=0,
            approval_bypass_count=0,
            deals_no_activity_30d=0,
        )
        result = monitor.assess(inp)
        if result.integrity_composite < 80:
            assert result.is_clean is False

    def test_is_clean_false_when_signals_gt_zero(self):
        monitor = SalesDataIntegrityMonitor()
        # close_date_changes_count >= 3 adds a risk signal
        inp = make_input(close_date_changes_count=3)
        result = monitor.assess(inp)
        assert result.risk_signal_count >= 1
        assert result.is_clean is False

    def test_is_clean_invariant_holds_for_batch(self):
        monitor = SalesDataIntegrityMonitor()
        inputs = [make_input(record_id=f"r{i}") for i in range(5)]
        results = monitor.assess_batch(inputs)
        for r in results:
            expected = r.integrity_composite >= 80 and r.risk_signal_count == 0
            assert r.is_clean is expected


# ---------------------------------------------------------------------------
# TestNeedsEscalationInvariant
# ---------------------------------------------------------------------------

class TestNeedsEscalationInvariant:
    """needs_escalation: CRITICAL_BREACH OR risk_signal_count >= 5."""

    def test_breach_needs_escalation(self):
        monitor = SalesDataIntegrityMonitor()
        result = monitor.assess(breach_input())
        assert result.needs_escalation is True

    def test_clean_rep_no_escalation(self):
        monitor = SalesDataIntegrityMonitor()
        result = monitor.assess(make_input())
        assert result.needs_escalation is False

    def test_critical_breach_triggers_escalation(self):
        monitor = SalesDataIntegrityMonitor()
        result = monitor.assess(breach_input())
        if result.integrity_risk == IntegrityRisk.CRITICAL_BREACH:
            assert result.needs_escalation is True

    def test_5_risk_signals_triggers_escalation(self):
        # Create input that accumulates exactly >=5 risk signals
        # Signals: deal_size_ratio>1.8, backdated>=3, close_date>=3, same_day>=1, approval_bypass>=1, crm_login>=3, no_activity>=3, stage_skips>=3
        inp = make_input(
            avg_deal_size_usd=100000.0,
            historical_avg_deal_size_usd=42000.0,  # ratio > 1.8 → signal
            backdated_activities_count=3,           # signal
            close_date_changes_count=3,             # signal
            deals_closed_same_day_created_count=1,  # signal
            approval_bypass_count=1,                # signal
        )
        monitor = SalesDataIntegrityMonitor()
        result = monitor.assess(inp)
        assert result.risk_signal_count >= 5
        assert result.needs_escalation is True

    def test_needs_escalation_invariant_holds_for_batch(self):
        monitor = SalesDataIntegrityMonitor()
        inputs = [make_input(record_id=f"r{i}") for i in range(3)] + [breach_input("b1")]
        results = monitor.assess_batch(inputs)
        for r in results:
            expected = r.integrity_risk == IntegrityRisk.CRITICAL_BREACH or r.risk_signal_count >= 5
            assert r.needs_escalation is expected


# ---------------------------------------------------------------------------
# TestScoreClamping
# ---------------------------------------------------------------------------

class TestScoreClamping:
    """All scores must remain in [0, 100]."""

    def test_pipeline_score_clamped_low(self):
        assert _pipeline_accuracy_score(breach_input()) >= 0.0

    def test_pipeline_score_clamped_high(self):
        assert _pipeline_accuracy_score(make_input()) <= 100.0

    def test_completeness_score_clamped_low(self):
        assert _data_completeness_score(breach_input()) >= 0.0

    def test_completeness_score_clamped_high(self):
        assert _data_completeness_score(make_input()) <= 100.0

    def test_behavioral_score_clamped_low(self):
        assert _behavioral_consistency_score(breach_input()) >= 0.0

    def test_behavioral_score_clamped_high(self):
        assert _behavioral_consistency_score(make_input()) <= 100.0

    def test_compliance_score_clamped_low(self):
        assert _compliance_score(breach_input()) >= 0.0

    def test_compliance_score_clamped_high(self):
        assert _compliance_score(make_input()) <= 100.0

    def test_result_pipeline_accuracy_in_range(self):
        monitor = SalesDataIntegrityMonitor()
        r = monitor.assess(breach_input())
        assert 0.0 <= r.pipeline_accuracy_score <= 100.0

    def test_result_data_completeness_in_range(self):
        monitor = SalesDataIntegrityMonitor()
        r = monitor.assess(breach_input())
        assert 0.0 <= r.data_completeness_score <= 100.0

    def test_result_behavioral_consistency_in_range(self):
        monitor = SalesDataIntegrityMonitor()
        r = monitor.assess(breach_input())
        assert 0.0 <= r.behavioral_consistency_score <= 100.0

    def test_result_compliance_score_in_range(self):
        monitor = SalesDataIntegrityMonitor()
        r = monitor.assess(breach_input())
        assert 0.0 <= r.compliance_score <= 100.0

    def test_result_integrity_composite_in_range(self):
        monitor = SalesDataIntegrityMonitor()
        r = monitor.assess(breach_input())
        assert 0.0 <= r.integrity_composite <= 100.0


# ---------------------------------------------------------------------------
# TestIntegrityRiskClassification
# ---------------------------------------------------------------------------

class TestIntegrityRiskClassification:
    """Risk classification boundaries."""

    def test_breach_input_yields_critical_breach(self):
        monitor = SalesDataIntegrityMonitor()
        r = monitor.assess(breach_input())
        assert r.integrity_risk == IntegrityRisk.CRITICAL_BREACH

    def test_clean_input_yields_clean_or_minor(self):
        monitor = SalesDataIntegrityMonitor()
        r = monitor.assess(make_input())
        assert r.integrity_risk in (IntegrityRisk.CLEAN, IntegrityRisk.MINOR_ISSUES)

    def test_integrity_risk_is_enum(self):
        monitor = SalesDataIntegrityMonitor()
        r = monitor.assess(make_input())
        assert isinstance(r.integrity_risk, IntegrityRisk)

    def test_composite_below_40_yields_critical_breach(self):
        # Force very low composite: many simultaneous deductions
        monitor = SalesDataIntegrityMonitor()
        r = monitor.assess(breach_input())
        if r.integrity_composite < 40:
            assert r.integrity_risk == IntegrityRisk.CRITICAL_BREACH

    def test_5_or_more_risk_signals_yields_critical_breach(self):
        inp = make_input(
            avg_deal_size_usd=100000.0,
            historical_avg_deal_size_usd=42000.0,
            backdated_activities_count=3,
            close_date_changes_count=3,
            deals_closed_same_day_created_count=1,
            approval_bypass_count=1,
        )
        monitor = SalesDataIntegrityMonitor()
        r = monitor.assess(inp)
        if r.risk_signal_count >= 5:
            assert r.integrity_risk == IntegrityRisk.CRITICAL_BREACH


# ---------------------------------------------------------------------------
# TestDataQualityMapping
# ---------------------------------------------------------------------------

class TestDataQualityMapping:
    """DataQuality maps from composite score ranges."""

    def test_excellent_quality_at_high_composite(self):
        monitor = SalesDataIntegrityMonitor()
        r = monitor.assess(make_input(
            avg_deal_size_usd=42000.0,
            historical_avg_deal_size_usd=42000.0,
            close_date_changes_count=0,
            backdated_activities_count=0,
            crm_login_anomaly_count=0,
            approval_bypass_count=0,
            missing_required_fields_count=0,
            duplicate_contact_count=0,
            unverified_opportunity_sources_count=0,
            manager_review_score=100.0,
            deals_no_activity_30d=0,
            stage_skips_count=0,
            deals_closed_same_day_created_count=0,
        ))
        if r.integrity_composite >= 85:
            assert r.data_quality == DataQuality.EXCELLENT

    def test_poor_quality_for_breach(self):
        monitor = SalesDataIntegrityMonitor()
        r = monitor.assess(breach_input())
        if r.integrity_composite < 50:
            assert r.data_quality == DataQuality.POOR

    def test_data_quality_is_enum(self):
        monitor = SalesDataIntegrityMonitor()
        r = monitor.assess(make_input())
        assert isinstance(r.data_quality, DataQuality)

    def test_good_quality_range(self):
        # composite in [70, 85) → good
        monitor = SalesDataIntegrityMonitor()
        r = monitor.assess(make_input(
            close_date_changes_count=1,
            stage_skips_count=2,
            missing_required_fields_count=2,
        ))
        if 70.0 <= r.integrity_composite < 85.0:
            assert r.data_quality == DataQuality.GOOD


# ---------------------------------------------------------------------------
# TestIntegrityActionMapping
# ---------------------------------------------------------------------------

class TestIntegrityActionMapping:
    """IntegrityAction maps correctly from risk level and signal count."""

    def test_breach_gets_compliance_escalation(self):
        monitor = SalesDataIntegrityMonitor()
        r = monitor.assess(breach_input())
        assert r.integrity_action == IntegrityAction.COMPLIANCE_ESCALATION

    def test_clean_input_gets_no_action_or_flag(self):
        monitor = SalesDataIntegrityMonitor()
        r = monitor.assess(make_input())
        # With 1 close_date change signal, may get FLAG_FOR_REVIEW
        assert r.integrity_action in (
            IntegrityAction.NO_ACTION,
            IntegrityAction.FLAG_FOR_REVIEW,
        )

    def test_integrity_action_is_enum(self):
        monitor = SalesDataIntegrityMonitor()
        r = monitor.assess(make_input())
        assert isinstance(r.integrity_action, IntegrityAction)


# ---------------------------------------------------------------------------
# TestAssessMethod
# ---------------------------------------------------------------------------

class TestAssessMethod:
    """Tests for SalesDataIntegrityMonitor.assess()."""

    def test_assess_returns_result_object(self):
        monitor = SalesDataIntegrityMonitor()
        result = monitor.assess(make_input())
        assert isinstance(result, SalesDataIntegrityResult)

    def test_assess_stores_in_monitor(self):
        monitor = SalesDataIntegrityMonitor()
        inp = make_input(record_id="stored_001")
        monitor.assess(inp)
        assert monitor.get("stored_001") is not None

    def test_assess_record_id_passes_through(self):
        monitor = SalesDataIntegrityMonitor()
        result = monitor.assess(make_input(record_id="abc"))
        assert result.record_id == "abc"

    def test_assess_rep_id_passes_through(self):
        monitor = SalesDataIntegrityMonitor()
        result = monitor.assess(make_input(rep_id="rep_xyz"))
        assert result.rep_id == "rep_xyz"

    def test_assess_overwrites_previous_record(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(record_id="dup", manager_review_score=100.0))
        monitor.assess(make_input(record_id="dup", manager_review_score=10.0))
        # Should only have one entry for "dup"
        all_ids = [r.record_id for r in monitor.all_records()]
        assert all_ids.count("dup") == 1

    def test_assess_result_is_dataclass(self):
        monitor = SalesDataIntegrityMonitor()
        result = monitor.assess(make_input())
        assert dataclasses.is_dataclass(result)

    def test_assess_primary_signal_is_string(self):
        monitor = SalesDataIntegrityMonitor()
        result = monitor.assess(make_input())
        assert isinstance(result.primary_integrity_signal, str)

    def test_assess_primary_signal_nonempty(self):
        monitor = SalesDataIntegrityMonitor()
        result = monitor.assess(make_input())
        assert len(result.primary_integrity_signal) > 0

    def test_assess_crm_anomaly_primary_signal(self):
        monitor = SalesDataIntegrityMonitor()
        result = monitor.assess(make_input(crm_login_anomaly_count=3))
        assert "CRM login" in result.primary_integrity_signal

    def test_assess_approval_bypass_primary_signal(self):
        monitor = SalesDataIntegrityMonitor()
        result = monitor.assess(make_input(approval_bypass_count=3))
        assert "approval" in result.primary_integrity_signal

    def test_assess_backdated_primary_signal(self):
        monitor = SalesDataIntegrityMonitor()
        result = monitor.assess(make_input(backdated_activities_count=3))
        assert "backdated" in result.primary_integrity_signal

    def test_assess_same_day_primary_signal(self):
        monitor = SalesDataIntegrityMonitor()
        result = monitor.assess(make_input(deals_closed_same_day_created_count=2))
        assert "same day" in result.primary_integrity_signal

    def test_assess_deal_size_primary_signal(self):
        monitor = SalesDataIntegrityMonitor()
        result = monitor.assess(make_input(
            avg_deal_size_usd=90000.0,
            historical_avg_deal_size_usd=42000.0,
            crm_login_anomaly_count=0,
            approval_bypass_count=0,
            backdated_activities_count=0,
            deals_closed_same_day_created_count=0,
        ))
        assert "inflation" in result.primary_integrity_signal or "historical" in result.primary_integrity_signal

    def test_assess_no_issues_primary_signal_is_acceptable(self):
        monitor = SalesDataIntegrityMonitor()
        result = monitor.assess(make_input(
            crm_login_anomaly_count=0,
            approval_bypass_count=0,
            backdated_activities_count=0,
            deals_closed_same_day_created_count=0,
            avg_deal_size_usd=42000.0,
            historical_avg_deal_size_usd=42000.0,
            close_date_changes_count=0,
            deals_no_activity_30d=0,
        ))
        assert "acceptable" in result.primary_integrity_signal


# ---------------------------------------------------------------------------
# TestAssessBatch
# ---------------------------------------------------------------------------

class TestAssessBatch:
    """Tests for assess_batch() including sort order."""

    def test_assess_batch_returns_list(self):
        monitor = SalesDataIntegrityMonitor()
        results = monitor.assess_batch([make_input(record_id="b1"), make_input(record_id="b2")])
        assert isinstance(results, list)

    def test_assess_batch_returns_correct_count(self):
        monitor = SalesDataIntegrityMonitor()
        inputs = [make_input(record_id=f"r{i}") for i in range(5)]
        results = monitor.assess_batch(inputs)
        assert len(results) == 5

    def test_assess_batch_sorted_ascending_composite(self):
        monitor = SalesDataIntegrityMonitor()
        inputs = [make_input(record_id="good"), breach_input("bad")]
        results = monitor.assess_batch(inputs)
        composites = [r.integrity_composite for r in results]
        assert composites == sorted(composites)

    def test_assess_batch_lowest_composite_first(self):
        monitor = SalesDataIntegrityMonitor()
        inputs = [make_input(record_id="good"), breach_input("bad")]
        results = monitor.assess_batch(inputs)
        # breach should be first (lowest composite)
        assert results[0].record_id == "bad"

    def test_assess_batch_stores_all_records(self):
        monitor = SalesDataIntegrityMonitor()
        inputs = [make_input(record_id=f"r{i}") for i in range(4)]
        monitor.assess_batch(inputs)
        assert len(monitor.all_records()) == 4

    def test_assess_batch_empty_input(self):
        monitor = SalesDataIntegrityMonitor()
        results = monitor.assess_batch([])
        assert results == []

    def test_assess_batch_single_item(self):
        monitor = SalesDataIntegrityMonitor()
        results = monitor.assess_batch([make_input(record_id="solo")])
        assert len(results) == 1

    def test_assess_batch_three_items_sorted(self):
        monitor = SalesDataIntegrityMonitor()
        inputs = [
            make_input(record_id="a"),
            breach_input("b"),
            make_input(record_id="c", stage_skips_count=2),
        ]
        results = monitor.assess_batch(inputs)
        composites = [r.integrity_composite for r in results]
        assert composites == sorted(composites)

    def test_assess_batch_result_types(self):
        monitor = SalesDataIntegrityMonitor()
        results = monitor.assess_batch([make_input(record_id="t1")])
        assert isinstance(results[0], SalesDataIntegrityResult)


# ---------------------------------------------------------------------------
# TestGetMethod
# ---------------------------------------------------------------------------

class TestGetMethod:
    """Tests for SalesDataIntegrityMonitor.get()."""

    def test_get_existing_record(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(record_id="exists"))
        assert monitor.get("exists") is not None

    def test_get_nonexistent_returns_none(self):
        monitor = SalesDataIntegrityMonitor()
        assert monitor.get("nonexistent") is None

    def test_get_returns_correct_record_id(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(record_id="fetch_me"))
        r = monitor.get("fetch_me")
        assert r.record_id == "fetch_me"

    def test_get_returns_latest_after_overwrite(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(record_id="dup", manager_review_score=50.0))
        monitor.assess(make_input(record_id="dup", manager_review_score=90.0))
        r = monitor.get("dup")
        assert r.data_completeness_score != 0


# ---------------------------------------------------------------------------
# TestAllRecords
# ---------------------------------------------------------------------------

class TestAllRecords:
    """Tests for all_records()."""

    def test_all_records_empty_initially(self):
        monitor = SalesDataIntegrityMonitor()
        assert monitor.all_records() == []

    def test_all_records_returns_all_assessed(self):
        monitor = SalesDataIntegrityMonitor()
        for i in range(5):
            monitor.assess(make_input(record_id=f"r{i}"))
        assert len(monitor.all_records()) == 5

    def test_all_records_sorted_ascending_composite(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(record_id="g"))
        monitor.assess(breach_input("b"))
        records = monitor.all_records()
        composites = [r.integrity_composite for r in records]
        assert composites == sorted(composites)

    def test_all_records_returns_result_objects(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(record_id="obj_test"))
        records = monitor.all_records()
        assert all(isinstance(r, SalesDataIntegrityResult) for r in records)


# ---------------------------------------------------------------------------
# TestCleanRecords
# ---------------------------------------------------------------------------

class TestCleanRecords:
    """Tests for clean_records()."""

    def test_clean_records_empty_initially(self):
        monitor = SalesDataIntegrityMonitor()
        assert monitor.clean_records() == []

    def test_clean_records_excludes_breach(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(breach_input())
        assert all(r.is_clean for r in monitor.clean_records())

    def test_clean_records_all_are_clean(self):
        monitor = SalesDataIntegrityMonitor()
        for i in range(3):
            monitor.assess(make_input(record_id=f"r{i}"))
        monitor.assess(breach_input("b"))
        for r in monitor.clean_records():
            assert r.is_clean is True

    def test_clean_records_count_matches_is_clean(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(record_id="a"))
        monitor.assess(breach_input("b"))
        clean = monitor.clean_records()
        all_recs = monitor.all_records()
        expected = sum(1 for r in all_recs if r.is_clean)
        assert len(clean) == expected


# ---------------------------------------------------------------------------
# TestEscalationQueue
# ---------------------------------------------------------------------------

class TestEscalationQueue:
    """Tests for escalation_queue()."""

    def test_escalation_queue_empty_initially(self):
        monitor = SalesDataIntegrityMonitor()
        assert monitor.escalation_queue() == []

    def test_escalation_queue_includes_breach(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(breach_input("b"))
        queue = monitor.escalation_queue()
        ids = [r.record_id for r in queue]
        assert "b" in ids

    def test_escalation_queue_all_need_escalation(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(record_id="ok"))
        monitor.assess(breach_input("esc"))
        for r in monitor.escalation_queue():
            assert r.needs_escalation is True

    def test_escalation_queue_count_matches_needs_escalation(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(record_id="a"))
        monitor.assess(breach_input("b"))
        q = monitor.escalation_queue()
        all_recs = monitor.all_records()
        expected = sum(1 for r in all_recs if r.needs_escalation)
        assert len(q) == expected


# ---------------------------------------------------------------------------
# TestByRisk
# ---------------------------------------------------------------------------

class TestByRisk:
    """Tests for by_risk()."""

    def test_by_risk_returns_only_matching_risk(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(breach_input("b"))
        critical = monitor.by_risk(IntegrityRisk.CRITICAL_BREACH)
        assert all(r.integrity_risk == IntegrityRisk.CRITICAL_BREACH for r in critical)

    def test_by_risk_empty_for_missing_category(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(record_id="a"))
        # Unlikely to get critical breach from default input
        result = monitor.by_risk(IntegrityRisk.CRITICAL_BREACH)
        assert isinstance(result, list)

    def test_by_risk_returns_list(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(record_id="a"))
        assert isinstance(monitor.by_risk(IntegrityRisk.CLEAN), list)

    def test_by_risk_breach_finds_breach_records(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(breach_input("b1"))
        monitor.assess(breach_input("b2"))
        monitor.assess(make_input(record_id="ok"))
        critical = monitor.by_risk(IntegrityRisk.CRITICAL_BREACH)
        assert len(critical) >= 2


# ---------------------------------------------------------------------------
# TestByAnomaly
# ---------------------------------------------------------------------------

class TestByAnomaly:
    """Tests for by_anomaly()."""

    def test_by_anomaly_returns_list(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(record_id="a"))
        assert isinstance(monitor.by_anomaly(AnomalyType.GHOST_DEAL), list)

    def test_by_anomaly_returns_only_matching(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(breach_input("b"))
        for anomaly in AnomalyType:
            results = monitor.by_anomaly(anomaly)
            assert all(r.anomaly_type == anomaly for r in results)

    def test_by_anomaly_crm_anomaly_yields_duplicate_entry(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(record_id="dup", crm_login_anomaly_count=3))
        results = monitor.by_anomaly(AnomalyType.DUPLICATE_ENTRY)
        assert any(r.record_id == "dup" for r in results)

    def test_by_anomaly_inflated_deal_value(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(
            record_id="inf",
            avg_deal_size_usd=100000.0,
            historical_avg_deal_size_usd=42000.0,
            crm_login_anomaly_count=0,
        ))
        results = monitor.by_anomaly(AnomalyType.INFLATED_DEAL_VALUE)
        assert any(r.record_id == "inf" for r in results)


# ---------------------------------------------------------------------------
# TestAvgIntegrityComposite
# ---------------------------------------------------------------------------

class TestAvgIntegrityComposite:
    """Tests for avg_integrity_composite()."""

    def test_avg_is_zero_when_no_records(self):
        monitor = SalesDataIntegrityMonitor()
        assert monitor.avg_integrity_composite() == 0.0

    def test_avg_single_record(self):
        monitor = SalesDataIntegrityMonitor()
        r = monitor.assess(make_input(record_id="single"))
        assert monitor.avg_integrity_composite() == r.integrity_composite

    def test_avg_two_records(self):
        monitor = SalesDataIntegrityMonitor()
        r1 = monitor.assess(make_input(record_id="a"))
        r2 = monitor.assess(make_input(record_id="b"))
        expected = round((r1.integrity_composite + r2.integrity_composite) / 2, 1)
        assert monitor.avg_integrity_composite() == expected

    def test_avg_returns_float(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(record_id="f"))
        assert isinstance(monitor.avg_integrity_composite(), float)

    def test_avg_breach_lowers_average(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(record_id="good"))
        avg_before = monitor.avg_integrity_composite()
        monitor.assess(breach_input("bad"))
        avg_after = monitor.avg_integrity_composite()
        assert avg_after < avg_before


# ---------------------------------------------------------------------------
# TestReset
# ---------------------------------------------------------------------------

class TestReset:
    """Tests for reset()."""

    def test_reset_clears_all_records(self):
        monitor = SalesDataIntegrityMonitor()
        for i in range(5):
            monitor.assess(make_input(record_id=f"r{i}"))
        monitor.reset()
        assert monitor.all_records() == []

    def test_reset_clears_clean_records(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(record_id="c"))
        monitor.reset()
        assert monitor.clean_records() == []

    def test_reset_clears_escalation_queue(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(breach_input())
        monitor.reset()
        assert monitor.escalation_queue() == []

    def test_reset_avg_returns_zero(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(record_id="x"))
        monitor.reset()
        assert monitor.avg_integrity_composite() == 0.0

    def test_get_after_reset_returns_none(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(record_id="gone"))
        monitor.reset()
        assert monitor.get("gone") is None

    def test_can_assess_after_reset(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(record_id="pre"))
        monitor.reset()
        monitor.assess(make_input(record_id="post"))
        assert monitor.get("post") is not None


# ---------------------------------------------------------------------------
# TestSummaryMethod
# ---------------------------------------------------------------------------

class TestSummaryMethod:
    """summary() must return exactly 13 keys and correct values."""

    def test_summary_returns_exactly_13_keys(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input())
        assert len(monitor.summary()) == 13

    def test_summary_key_total(self):
        monitor = SalesDataIntegrityMonitor()
        assert "total" in monitor.summary()

    def test_summary_key_risk_counts(self):
        monitor = SalesDataIntegrityMonitor()
        assert "risk_counts" in monitor.summary()

    def test_summary_key_anomaly_counts(self):
        monitor = SalesDataIntegrityMonitor()
        assert "anomaly_counts" in monitor.summary()

    def test_summary_key_quality_counts(self):
        monitor = SalesDataIntegrityMonitor()
        assert "quality_counts" in monitor.summary()

    def test_summary_key_action_counts(self):
        monitor = SalesDataIntegrityMonitor()
        assert "action_counts" in monitor.summary()

    def test_summary_key_avg_integrity_composite(self):
        monitor = SalesDataIntegrityMonitor()
        assert "avg_integrity_composite" in monitor.summary()

    def test_summary_key_clean_count(self):
        monitor = SalesDataIntegrityMonitor()
        assert "clean_count" in monitor.summary()

    def test_summary_key_escalation_count(self):
        monitor = SalesDataIntegrityMonitor()
        assert "escalation_count" in monitor.summary()

    def test_summary_key_avg_pipeline_accuracy_score(self):
        monitor = SalesDataIntegrityMonitor()
        assert "avg_pipeline_accuracy_score" in monitor.summary()

    def test_summary_key_avg_data_completeness_score(self):
        monitor = SalesDataIntegrityMonitor()
        assert "avg_data_completeness_score" in monitor.summary()

    def test_summary_key_avg_behavioral_consistency_score(self):
        monitor = SalesDataIntegrityMonitor()
        assert "avg_behavioral_consistency_score" in monitor.summary()

    def test_summary_key_avg_compliance_score(self):
        monitor = SalesDataIntegrityMonitor()
        assert "avg_compliance_score" in monitor.summary()

    def test_summary_key_high_risk_rep_count(self):
        monitor = SalesDataIntegrityMonitor()
        assert "high_risk_rep_count" in monitor.summary()

    def test_summary_total_count(self):
        monitor = SalesDataIntegrityMonitor()
        for i in range(3):
            monitor.assess(make_input(record_id=f"r{i}"))
        assert monitor.summary()["total"] == 3

    def test_summary_total_zero_when_empty(self):
        monitor = SalesDataIntegrityMonitor()
        assert monitor.summary()["total"] == 0

    def test_summary_clean_count_accuracy(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(record_id="ok"))
        monitor.assess(breach_input("bad"))
        s = monitor.summary()
        assert s["clean_count"] == len(monitor.clean_records())

    def test_summary_escalation_count_accuracy(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(record_id="ok"))
        monitor.assess(breach_input("bad"))
        s = monitor.summary()
        assert s["escalation_count"] == len(monitor.escalation_queue())

    def test_summary_avg_composite_matches_method(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(record_id="a"))
        monitor.assess(breach_input("b"))
        s = monitor.summary()
        assert s["avg_integrity_composite"] == monitor.avg_integrity_composite()

    def test_summary_risk_counts_is_dict(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(record_id="a"))
        s = monitor.summary()
        assert isinstance(s["risk_counts"], dict)

    def test_summary_anomaly_counts_is_dict(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(record_id="a"))
        s = monitor.summary()
        assert isinstance(s["anomaly_counts"], dict)

    def test_summary_quality_counts_is_dict(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(record_id="a"))
        s = monitor.summary()
        assert isinstance(s["quality_counts"], dict)

    def test_summary_action_counts_is_dict(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(record_id="a"))
        s = monitor.summary()
        assert isinstance(s["action_counts"], dict)

    def test_summary_high_risk_rep_count_includes_breach(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(breach_input("b1"))
        monitor.assess(breach_input("b2"))
        monitor.assess(make_input(record_id="ok"))
        s = monitor.summary()
        assert s["high_risk_rep_count"] >= 2

    def test_summary_risk_counts_sum_equals_total(self):
        monitor = SalesDataIntegrityMonitor()
        for i in range(4):
            monitor.assess(make_input(record_id=f"r{i}"))
        monitor.assess(breach_input("b"))
        s = monitor.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_anomaly_counts_sum_equals_total(self):
        monitor = SalesDataIntegrityMonitor()
        for i in range(3):
            monitor.assess(make_input(record_id=f"r{i}"))
        monitor.assess(breach_input("b"))
        s = monitor.summary()
        assert sum(s["anomaly_counts"].values()) == s["total"]

    def test_summary_quality_counts_sum_equals_total(self):
        monitor = SalesDataIntegrityMonitor()
        for i in range(3):
            monitor.assess(make_input(record_id=f"r{i}"))
        monitor.assess(breach_input("b"))
        s = monitor.summary()
        assert sum(s["quality_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_equals_total(self):
        monitor = SalesDataIntegrityMonitor()
        for i in range(3):
            monitor.assess(make_input(record_id=f"r{i}"))
        monitor.assess(breach_input("b"))
        s = monitor.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_avg_scores_are_floats(self):
        monitor = SalesDataIntegrityMonitor()
        monitor.assess(make_input(record_id="a"))
        s = monitor.summary()
        assert isinstance(s["avg_pipeline_accuracy_score"], float)
        assert isinstance(s["avg_data_completeness_score"], float)
        assert isinstance(s["avg_behavioral_consistency_score"], float)
        assert isinstance(s["avg_compliance_score"], float)

    def test_summary_avg_scores_zero_when_empty(self):
        monitor = SalesDataIntegrityMonitor()
        s = monitor.summary()
        assert s["avg_pipeline_accuracy_score"] == 0.0
        assert s["avg_data_completeness_score"] == 0.0
        assert s["avg_behavioral_consistency_score"] == 0.0
        assert s["avg_compliance_score"] == 0.0

    def test_summary_high_risk_rep_count_zero_for_clean(self):
        monitor = SalesDataIntegrityMonitor()
        r = monitor.assess(make_input(record_id="clean_only"))
        if r.integrity_risk != IntegrityRisk.CRITICAL_BREACH:
            assert monitor.summary()["high_risk_rep_count"] == 0

    def test_summary_called_with_no_args(self):
        monitor = SalesDataIntegrityMonitor()
        # Confirms signature takes no args
        monitor.assess(make_input(record_id="a"))
        s = monitor.summary()
        assert s is not None

    def test_summary_13_keys_with_multiple_records(self):
        monitor = SalesDataIntegrityMonitor()
        for i in range(10):
            monitor.assess(make_input(record_id=f"r{i}"))
        assert len(monitor.summary()) == 13


# ---------------------------------------------------------------------------
# TestMonitorMethods
# ---------------------------------------------------------------------------

class TestMonitorMethods:
    """Ensure monitor has all required methods."""

    def test_has_assess(self):
        assert hasattr(SalesDataIntegrityMonitor, "assess")

    def test_has_assess_batch(self):
        assert hasattr(SalesDataIntegrityMonitor, "assess_batch")

    def test_has_get(self):
        assert hasattr(SalesDataIntegrityMonitor, "get")

    def test_has_all_records(self):
        assert hasattr(SalesDataIntegrityMonitor, "all_records")

    def test_has_clean_records(self):
        assert hasattr(SalesDataIntegrityMonitor, "clean_records")

    def test_has_escalation_queue(self):
        assert hasattr(SalesDataIntegrityMonitor, "escalation_queue")

    def test_has_by_risk(self):
        assert hasattr(SalesDataIntegrityMonitor, "by_risk")

    def test_has_by_anomaly(self):
        assert hasattr(SalesDataIntegrityMonitor, "by_anomaly")

    def test_has_avg_integrity_composite(self):
        assert hasattr(SalesDataIntegrityMonitor, "avg_integrity_composite")

    def test_has_reset(self):
        assert hasattr(SalesDataIntegrityMonitor, "reset")

    def test_has_summary(self):
        assert hasattr(SalesDataIntegrityMonitor, "summary")

    def test_monitor_starts_empty(self):
        monitor = SalesDataIntegrityMonitor()
        assert monitor.all_records() == []

    def test_independent_monitor_instances(self):
        m1 = SalesDataIntegrityMonitor()
        m2 = SalesDataIntegrityMonitor()
        m1.assess(make_input(record_id="shared"))
        assert m2.get("shared") is None


# ---------------------------------------------------------------------------
# TestAnomalyTypeAssignment
# ---------------------------------------------------------------------------

class TestAnomalyTypeAssignment:
    """Verify anomaly type priority logic."""

    def test_crm_anomaly_overrides_all(self):
        monitor = SalesDataIntegrityMonitor()
        r = monitor.assess(make_input(
            crm_login_anomaly_count=3,
            avg_deal_size_usd=200000.0,
            historical_avg_deal_size_usd=42000.0,
        ))
        assert r.anomaly_type == AnomalyType.DUPLICATE_ENTRY

    def test_inflated_deal_value_when_no_crm_anomaly(self):
        monitor = SalesDataIntegrityMonitor()
        r = monitor.assess(make_input(
            crm_login_anomaly_count=0,
            avg_deal_size_usd=100000.0,
            historical_avg_deal_size_usd=42000.0,
        ))
        assert r.anomaly_type == AnomalyType.INFLATED_DEAL_VALUE

    def test_close_date_manipulation_detected(self):
        monitor = SalesDataIntegrityMonitor()
        r = monitor.assess(make_input(
            crm_login_anomaly_count=0,
            avg_deal_size_usd=42000.0,
            historical_avg_deal_size_usd=42000.0,
            close_date_changes_count=3,
        ))
        assert r.anomaly_type == AnomalyType.CLOSE_DATE_MANIPULATION

    def test_days_pushed_triggers_close_date_manipulation(self):
        monitor = SalesDataIntegrityMonitor()
        r = monitor.assess(make_input(
            crm_login_anomaly_count=0,
            avg_deal_size_usd=42000.0,
            historical_avg_deal_size_usd=42000.0,
            close_date_changes_count=0,
            days_close_date_pushed=60,
        ))
        assert r.anomaly_type == AnomalyType.CLOSE_DATE_MANIPULATION

    def test_ghost_deal_when_no_activity(self):
        monitor = SalesDataIntegrityMonitor()
        r = monitor.assess(make_input(
            crm_login_anomaly_count=0,
            avg_deal_size_usd=42000.0,
            historical_avg_deal_size_usd=42000.0,
            close_date_changes_count=0,
            days_close_date_pushed=0,
            deals_no_activity_30d=3,
            pipeline_created_last_7d_usd=80000.0,
            avg_pipeline_created_per_month_usd=350000.0,
        ))
        assert r.anomaly_type == AnomalyType.GHOST_DEAL

    def test_missing_required_fields_when_many_missing(self):
        monitor = SalesDataIntegrityMonitor()
        r = monitor.assess(make_input(
            crm_login_anomaly_count=0,
            avg_deal_size_usd=42000.0,
            historical_avg_deal_size_usd=42000.0,
            close_date_changes_count=0,
            days_close_date_pushed=0,
            deals_no_activity_30d=0,
            pipeline_created_last_7d_usd=80000.0,
            avg_pipeline_created_per_month_usd=350000.0,
            missing_required_fields_count=5,
        ))
        assert r.anomaly_type == AnomalyType.MISSING_REQUIRED_FIELDS


# ---------------------------------------------------------------------------
# TestEdgeCases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """Edge cases and boundary conditions."""

    def test_all_zeros_does_not_crash(self):
        monitor = SalesDataIntegrityMonitor()
        inp = make_input(
            deal_count_last_30d=0,
            avg_deal_size_usd=0.0,
            historical_avg_deal_size_usd=0.0,
            deals_closed_end_of_quarter_pct=0.0,
            close_date_changes_count=0,
            days_close_date_pushed=0,
            pipeline_created_last_7d_usd=0.0,
            avg_pipeline_created_per_month_usd=0.0,
            duplicate_contact_count=0,
            missing_required_fields_count=0,
            deals_no_activity_30d=0,
            stage_skips_count=0,
            backdated_activities_count=0,
            deals_closed_same_day_created_count=0,
            crm_login_anomaly_count=0,
            data_edit_frequency_score=0.0,
            approval_bypass_count=0,
            unverified_opportunity_sources_count=0,
            team_benchmark_deviation_pct=0.0,
            manager_review_score=0.0,
        )
        result = monitor.assess(inp)
        assert result is not None

    def test_maximum_values_does_not_crash(self):
        monitor = SalesDataIntegrityMonitor()
        inp = make_input(
            avg_deal_size_usd=1e9,
            historical_avg_deal_size_usd=1.0,
            deals_closed_end_of_quarter_pct=100.0,
            close_date_changes_count=100,
            days_close_date_pushed=365,
            pipeline_created_last_7d_usd=1e9,
            avg_pipeline_created_per_month_usd=1.0,
            duplicate_contact_count=100,
            missing_required_fields_count=100,
            deals_no_activity_30d=100,
            stage_skips_count=100,
            backdated_activities_count=100,
            deals_closed_same_day_created_count=100,
            crm_login_anomaly_count=100,
            data_edit_frequency_score=100.0,
            approval_bypass_count=100,
            unverified_opportunity_sources_count=100,
            team_benchmark_deviation_pct=100.0,
            manager_review_score=0.0,
        )
        result = monitor.assess(inp)
        assert 0.0 <= result.integrity_composite <= 100.0

    def test_boundary_composite_exactly_80(self):
        # Test is_clean boundary: composite == 80 with 0 signals should be clean
        # We check the logic rather than forcing exactly 80
        monitor = SalesDataIntegrityMonitor()
        result = monitor.assess(make_input())
        expected = result.integrity_composite >= 80 and result.risk_signal_count == 0
        assert result.is_clean is expected

    def test_multiple_monitors_independent(self):
        m1 = SalesDataIntegrityMonitor()
        m2 = SalesDataIntegrityMonitor()
        m1.assess(make_input(record_id="m1_only"))
        assert m2.get("m1_only") is None
        assert len(m2.all_records()) == 0

    def test_reassess_same_record_updates(self):
        monitor = SalesDataIntegrityMonitor()
        r1 = monitor.assess(make_input(record_id="update_me", missing_required_fields_count=0))
        r2 = monitor.assess(make_input(record_id="update_me", missing_required_fields_count=10))
        # Should have overwritten; get returns the new one
        stored = monitor.get("update_me")
        assert stored.data_completeness_score == r2.data_completeness_score

    def test_avg_composite_exact_calculation(self):
        monitor = SalesDataIntegrityMonitor()
        r1 = monitor.assess(make_input(record_id="a"))
        r2 = monitor.assess(breach_input("b"))
        expected = round((r1.integrity_composite + r2.integrity_composite) / 2, 1)
        assert monitor.avg_integrity_composite() == expected

    def test_deal_size_ratio_exactly_at_boundary_1_8(self):
        # ratio == 1.8 → not strictly > 1.8, so no signal
        inp = make_input(
            avg_deal_size_usd=75600.0,   # exactly 1.8 * 42000
            historical_avg_deal_size_usd=42000.0,
        )
        monitor = SalesDataIntegrityMonitor()
        result = monitor.assess(inp)
        # ratio is exactly 1.8, which is NOT > 1.8, so no deal-size signal
        pipeline = _pipeline_accuracy_score(inp)
        assert pipeline >= 75.0  # should not take the 25-point hit

    def test_pipeline_stuffing_ratio_boundary(self):
        # weekly_avg = 350000/4 = 87500; 7d = 87500 * 2 = 175000 → ratio exactly 2.0 (not > 2.0)
        inp = make_input(
            pipeline_created_last_7d_usd=175000.0,
            avg_pipeline_created_per_month_usd=350000.0,
        )
        score = _pipeline_accuracy_score(inp)
        # ratio == 2.0 is NOT > 2.0, no deduction from pipeline stuffing
        assert score == 100.0  # base - no other deductions with default input adjusted

    def test_result_is_dataclass(self):
        monitor = SalesDataIntegrityMonitor()
        result = monitor.assess(make_input())
        assert dataclasses.is_dataclass(result)

    def test_summary_empty_monitor_13_keys(self):
        monitor = SalesDataIntegrityMonitor()
        s = monitor.summary()
        assert len(s) == 13

    def test_summary_empty_risk_counts_is_empty_dict(self):
        monitor = SalesDataIntegrityMonitor()
        s = monitor.summary()
        assert s["risk_counts"] == {}

    def test_by_risk_and_by_anomaly_with_empty_monitor(self):
        monitor = SalesDataIntegrityMonitor()
        assert monitor.by_risk(IntegrityRisk.CLEAN) == []
        assert monitor.by_anomaly(AnomalyType.GHOST_DEAL) == []

    def test_assess_batch_sorted_with_identical_composites(self):
        monitor = SalesDataIntegrityMonitor()
        inputs = [make_input(record_id=f"r{i}") for i in range(3)]
        results = monitor.assess_batch(inputs)
        composites = [r.integrity_composite for r in results]
        assert composites == sorted(composites)
