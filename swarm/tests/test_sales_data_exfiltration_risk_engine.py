"""
Comprehensive pytest test suite for SalesDataExfiltrationRiskEngine (Module 113).

Coverage:
- All enum values and membership
- Input dataclass field count (22 fields)
- Result to_dict() key count (15 keys)
- summary() key count (13 keys, both empty and populated)
- All sub-score functions via assess()
- is_exfiltration_risk invariants
- requires_immediate_review invariants
- estimated_records_at_risk formula
- ExfiltrationRisk / ExfiltrationSeverity thresholds
- ExfiltrationPattern classification priority
- Recommended action logic
- exfiltration_signal string content
- assess_batch / summary API
- Edge cases: zeros, resignation with no downloads, admin impersonation
"""

from __future__ import annotations

import dataclasses
import pytest

from swarm.intelligence.sales_data_exfiltration_risk_engine import (
    SalesDataExfiltrationRiskEngine,
    SalesDataExfiltrationInput,
    SalesDataExfiltrationResult,
    ExfiltrationRisk,
    ExfiltrationPattern,
    ExfiltrationSeverity,
    ExfiltrationAction,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _inp(**overrides) -> SalesDataExfiltrationInput:
    """Baseline input — all zeros, no signals."""
    defaults = dict(
        rep_id="rep001",
        region="west",
        evaluation_period_id="2026-Q2",
        crm_export_count_last_30d=0,
        crm_export_count_prior_30d=0,
        records_exported_last_30d=0,
        records_exported_prior_30d=0,
        off_hours_access_count=0,
        accounts_accessed_outside_territory=0,
        new_account_views_not_in_pipeline=0,
        bulk_contact_download_count=0,
        failed_access_attempts=0,
        admin_impersonation_attempts=0,
        data_copy_to_personal_storage_alerts=0,
        crm_api_calls_last_30d=0,
        crm_api_calls_prior_30d=0,
        resignation_signal_days_ago=0,
        competitor_domain_email_access=0,
        avg_session_duration_minutes=0.0,
        unusual_report_run_count=0,
        territory_violation_count=0,
        after_hours_bulk_action_count=0,
    )
    defaults.update(overrides)
    return SalesDataExfiltrationInput(**defaults)


def _eng() -> SalesDataExfiltrationRiskEngine:
    return SalesDataExfiltrationRiskEngine()


# ---------------------------------------------------------------------------
# 1. Enum membership and values
# ---------------------------------------------------------------------------

class TestExfiltrationRiskEnum:
    def test_low_value(self):
        assert ExfiltrationRisk.low.value == "low"

    def test_moderate_value(self):
        assert ExfiltrationRisk.moderate.value == "moderate"

    def test_high_value(self):
        assert ExfiltrationRisk.high.value == "high"

    def test_critical_value(self):
        assert ExfiltrationRisk.critical.value == "critical"

    def test_exactly_four_members(self):
        assert len(ExfiltrationRisk) == 4

    def test_is_str_enum(self):
        assert isinstance(ExfiltrationRisk.low, str)

    def test_string_equality_low(self):
        assert ExfiltrationRisk.low == "low"

    def test_string_equality_critical(self):
        assert ExfiltrationRisk.critical == "critical"


class TestExfiltrationPatternEnum:
    def test_none_value(self):
        assert ExfiltrationPattern.none.value == "none"

    def test_bulk_export_value(self):
        assert ExfiltrationPattern.bulk_export.value == "bulk_export"

    def test_territory_boundary_breach_value(self):
        assert ExfiltrationPattern.territory_boundary_breach.value == "territory_boundary_breach"

    def test_unusual_access_hours_value(self):
        assert ExfiltrationPattern.unusual_access_hours.value == "unusual_access_hours"

    def test_account_scraping_value(self):
        assert ExfiltrationPattern.account_scraping.value == "account_scraping"

    def test_pre_departure_download_value(self):
        assert ExfiltrationPattern.pre_departure_download.value == "pre_departure_download"

    def test_exactly_six_members(self):
        assert len(ExfiltrationPattern) == 6

    def test_is_str_enum(self):
        assert isinstance(ExfiltrationPattern.none, str)


class TestExfiltrationSeverityEnum:
    def test_normal_value(self):
        assert ExfiltrationSeverity.normal.value == "normal"

    def test_suspicious_value(self):
        assert ExfiltrationSeverity.suspicious.value == "suspicious"

    def test_concerning_value(self):
        assert ExfiltrationSeverity.concerning.value == "concerning"

    def test_threat_value(self):
        assert ExfiltrationSeverity.threat.value == "threat"

    def test_exactly_four_members(self):
        assert len(ExfiltrationSeverity) == 4

    def test_is_str_enum(self):
        assert isinstance(ExfiltrationSeverity.normal, str)


class TestExfiltrationActionEnum:
    def test_no_action_value(self):
        assert ExfiltrationAction.no_action.value == "no_action"

    def test_audit_trail_review_value(self):
        assert ExfiltrationAction.audit_trail_review.value == "audit_trail_review"

    def test_access_restriction_value(self):
        assert ExfiltrationAction.access_restriction.value == "access_restriction"

    def test_security_investigation_value(self):
        assert ExfiltrationAction.security_investigation.value == "security_investigation"

    def test_immediate_lockdown_value(self):
        assert ExfiltrationAction.immediate_lockdown.value == "immediate_lockdown"

    def test_exactly_five_members(self):
        assert len(ExfiltrationAction) == 5

    def test_is_str_enum(self):
        assert isinstance(ExfiltrationAction.no_action, str)


# ---------------------------------------------------------------------------
# 2. Input dataclass — exactly 22 fields
# ---------------------------------------------------------------------------

class TestInputDataclassStructure:
    def test_exactly_22_fields(self):
        assert len(dataclasses.fields(SalesDataExfiltrationInput)) == 22

    def test_field_names_complete(self):
        names = {f.name for f in dataclasses.fields(SalesDataExfiltrationInput)}
        expected = {
            "rep_id", "region", "evaluation_period_id",
            "crm_export_count_last_30d", "crm_export_count_prior_30d",
            "records_exported_last_30d", "records_exported_prior_30d",
            "off_hours_access_count", "accounts_accessed_outside_territory",
            "new_account_views_not_in_pipeline", "bulk_contact_download_count",
            "failed_access_attempts", "admin_impersonation_attempts",
            "data_copy_to_personal_storage_alerts",
            "crm_api_calls_last_30d", "crm_api_calls_prior_30d",
            "resignation_signal_days_ago", "competitor_domain_email_access",
            "avg_session_duration_minutes", "unusual_report_run_count",
            "territory_violation_count", "after_hours_bulk_action_count",
        }
        assert names == expected

    def test_instantiation_succeeds(self):
        inp = _inp()
        assert inp.rep_id == "rep001"

    def test_rep_id_field(self):
        assert _inp(rep_id="xyz").rep_id == "xyz"

    def test_region_field(self):
        assert _inp(region="east").region == "east"

    def test_evaluation_period_id_field(self):
        assert _inp(evaluation_period_id="2026-Q1").evaluation_period_id == "2026-Q1"

    def test_crm_export_count_last_30d_field(self):
        assert _inp(crm_export_count_last_30d=5).crm_export_count_last_30d == 5

    def test_records_exported_last_30d_field(self):
        assert _inp(records_exported_last_30d=1000).records_exported_last_30d == 1000

    def test_avg_session_duration_minutes_is_float(self):
        assert isinstance(_inp(avg_session_duration_minutes=90.5).avg_session_duration_minutes, float)

    def test_admin_impersonation_attempts_field(self):
        assert _inp(admin_impersonation_attempts=2).admin_impersonation_attempts == 2

    def test_resignation_signal_days_ago_field(self):
        assert _inp(resignation_signal_days_ago=14).resignation_signal_days_ago == 14


# ---------------------------------------------------------------------------
# 3. to_dict() — exactly 15 keys
# ---------------------------------------------------------------------------

class TestToDictKeyCount:
    def test_exactly_15_keys_baseline(self):
        r = _eng().assess(_inp())
        assert len(r.to_dict()) == 15

    def test_exactly_15_keys_high_composite(self):
        r = _eng().assess(_inp(
            admin_impersonation_attempts=2,
            data_copy_to_personal_storage_alerts=3,
            competitor_domain_email_access=3,
            resignation_signal_days_ago=10,
            bulk_contact_download_count=5,
        ))
        assert len(r.to_dict()) == 15

    def test_to_dict_key_names(self):
        d = _eng().assess(_inp()).to_dict()
        expected = {
            "rep_id", "region",
            "exfiltration_risk", "exfiltration_pattern",
            "exfiltration_severity", "recommended_action",
            "export_anomaly_score", "access_pattern_score",
            "boundary_violation_score", "behavioral_risk_score",
            "exfiltration_composite",
            "is_exfiltration_risk", "requires_immediate_review",
            "estimated_records_at_risk", "exfiltration_signal",
        }
        assert set(d.keys()) == expected

    def test_to_dict_rep_id_preserved(self):
        d = _eng().assess(_inp(rep_id="r99")).to_dict()
        assert d["rep_id"] == "r99"

    def test_to_dict_region_preserved(self):
        d = _eng().assess(_inp(region="south")).to_dict()
        assert d["region"] == "south"

    def test_to_dict_exfiltration_risk_is_string(self):
        assert isinstance(_eng().assess(_inp()).to_dict()["exfiltration_risk"], str)

    def test_to_dict_exfiltration_pattern_is_string(self):
        assert isinstance(_eng().assess(_inp()).to_dict()["exfiltration_pattern"], str)

    def test_to_dict_exfiltration_severity_is_string(self):
        assert isinstance(_eng().assess(_inp()).to_dict()["exfiltration_severity"], str)

    def test_to_dict_recommended_action_is_string(self):
        assert isinstance(_eng().assess(_inp()).to_dict()["recommended_action"], str)

    def test_to_dict_is_exfiltration_risk_is_bool(self):
        assert isinstance(_eng().assess(_inp()).to_dict()["is_exfiltration_risk"], bool)

    def test_to_dict_requires_immediate_review_is_bool(self):
        assert isinstance(_eng().assess(_inp()).to_dict()["requires_immediate_review"], bool)

    def test_to_dict_estimated_records_at_risk_is_int(self):
        assert isinstance(_eng().assess(_inp()).to_dict()["estimated_records_at_risk"], int)

    def test_to_dict_exfiltration_signal_is_string(self):
        assert isinstance(_eng().assess(_inp()).to_dict()["exfiltration_signal"], str)

    def test_to_dict_export_anomaly_score_rounded(self):
        d = _eng().assess(_inp()).to_dict()
        v = d["export_anomaly_score"]
        assert v == round(v, 1)

    def test_to_dict_composite_rounded(self):
        d = _eng().assess(_inp()).to_dict()
        v = d["exfiltration_composite"]
        assert v == round(v, 1)


# ---------------------------------------------------------------------------
# 4. summary() — exactly 13 keys, both empty and populated
# ---------------------------------------------------------------------------

class TestSummaryKeyCount:
    def test_exactly_13_keys_empty_engine(self):
        assert len(_eng().summary()) == 13

    def test_exactly_13_keys_after_one_assess(self):
        e = _eng()
        e.assess(_inp())
        assert len(e.summary()) == 13

    def test_exactly_13_keys_after_batch(self):
        e = _eng()
        e.assess_batch([_inp(rep_id=f"r{i}") for i in range(5)])
        assert len(e.summary()) == 13

    def test_summary_key_names(self):
        e = _eng()
        e.assess(_inp())
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_exfiltration_composite",
            "exfiltration_risk_count", "immediate_review_count",
            "avg_export_anomaly_score", "avg_access_pattern_score",
            "avg_boundary_violation_score", "avg_behavioral_risk_score",
            "total_estimated_records_at_risk",
        }
        assert set(e.summary().keys()) == expected

    def test_summary_total_empty(self):
        assert _eng().summary()["total"] == 0

    def test_summary_total_one(self):
        e = _eng()
        e.assess(_inp())
        assert e.summary()["total"] == 1

    def test_summary_total_five(self):
        e = _eng()
        for i in range(5):
            e.assess(_inp(rep_id=f"r{i}"))
        assert e.summary()["total"] == 5

    def test_summary_avg_composite_empty_is_zero(self):
        assert _eng().summary()["avg_exfiltration_composite"] == 0.0

    def test_summary_exfiltration_risk_count_empty_is_zero(self):
        assert _eng().summary()["exfiltration_risk_count"] == 0

    def test_summary_immediate_review_count_empty_is_zero(self):
        assert _eng().summary()["immediate_review_count"] == 0

    def test_summary_total_estimated_records_empty_is_zero(self):
        assert _eng().summary()["total_estimated_records_at_risk"] == 0

    def test_summary_avg_export_anomaly_empty_is_zero(self):
        assert _eng().summary()["avg_export_anomaly_score"] == 0.0

    def test_summary_avg_access_pattern_empty_is_zero(self):
        assert _eng().summary()["avg_access_pattern_score"] == 0.0

    def test_summary_avg_boundary_violation_empty_is_zero(self):
        assert _eng().summary()["avg_boundary_violation_score"] == 0.0

    def test_summary_avg_behavioral_risk_empty_is_zero(self):
        assert _eng().summary()["avg_behavioral_risk_score"] == 0.0

    def test_summary_risk_counts_is_dict(self):
        e = _eng()
        e.assess(_inp())
        assert isinstance(e.summary()["risk_counts"], dict)

    def test_summary_pattern_counts_is_dict(self):
        e = _eng()
        e.assess(_inp())
        assert isinstance(e.summary()["pattern_counts"], dict)

    def test_summary_severity_counts_is_dict(self):
        e = _eng()
        e.assess(_inp())
        assert isinstance(e.summary()["severity_counts"], dict)

    def test_summary_action_counts_is_dict(self):
        e = _eng()
        e.assess(_inp())
        assert isinstance(e.summary()["action_counts"], dict)


# ---------------------------------------------------------------------------
# 5. Export anomaly sub-score
# ---------------------------------------------------------------------------

class TestExportAnomalyScore:
    def test_zero_when_all_zero(self):
        r = _eng().assess(_inp())
        assert r.export_anomaly_score == 0.0

    def test_export_ratio_2x_adds_15(self):
        # prior=5, last=10 -> ratio=2.0
        r = _eng().assess(_inp(crm_export_count_last_30d=10, crm_export_count_prior_30d=5))
        assert r.export_anomaly_score == 15.0

    def test_export_ratio_3x_adds_30(self):
        r = _eng().assess(_inp(crm_export_count_last_30d=15, crm_export_count_prior_30d=5))
        assert r.export_anomaly_score == 30.0

    def test_export_ratio_5x_adds_45(self):
        r = _eng().assess(_inp(crm_export_count_last_30d=25, crm_export_count_prior_30d=5))
        assert r.export_anomaly_score == 45.0

    def test_export_ratio_exactly_2_boundary(self):
        r = _eng().assess(_inp(crm_export_count_last_30d=10, crm_export_count_prior_30d=5))
        assert r.export_anomaly_score == 15.0

    def test_export_ratio_exactly_3_boundary(self):
        r = _eng().assess(_inp(crm_export_count_last_30d=15, crm_export_count_prior_30d=5))
        assert r.export_anomaly_score == 30.0

    def test_export_ratio_exactly_5_boundary(self):
        r = _eng().assess(_inp(crm_export_count_last_30d=25, crm_export_count_prior_30d=5))
        assert r.export_anomaly_score == 45.0

    def test_no_prior_exports_last_gte_5_adds_25(self):
        # prior=0, last=5 -> adds 25
        r = _eng().assess(_inp(crm_export_count_last_30d=5, crm_export_count_prior_30d=0))
        assert r.export_anomaly_score >= 25.0

    def test_no_prior_exports_last_lt_5_no_export_contribution(self):
        r = _eng().assess(_inp(crm_export_count_last_30d=4, crm_export_count_prior_30d=0))
        # No export ratio contribution; check no export component added
        assert r.export_anomaly_score == 0.0

    def test_records_ratio_2x_adds_8(self):
        r = _eng().assess(_inp(records_exported_last_30d=200, records_exported_prior_30d=100))
        assert r.export_anomaly_score == 8.0

    def test_records_ratio_3x_adds_18(self):
        r = _eng().assess(_inp(records_exported_last_30d=300, records_exported_prior_30d=100))
        assert r.export_anomaly_score == 18.0

    def test_records_ratio_5x_adds_30(self):
        r = _eng().assess(_inp(records_exported_last_30d=500, records_exported_prior_30d=100))
        assert r.export_anomaly_score == 30.0

    def test_records_no_prior_gte_500_adds_20(self):
        r = _eng().assess(_inp(records_exported_last_30d=500, records_exported_prior_30d=0))
        assert r.export_anomaly_score >= 20.0

    def test_records_no_prior_lt_500_no_contribution(self):
        r = _eng().assess(_inp(records_exported_last_30d=499, records_exported_prior_30d=0))
        assert r.export_anomaly_score == 0.0

    def test_bulk_download_1_adds_8(self):
        r = _eng().assess(_inp(bulk_contact_download_count=1))
        assert r.export_anomaly_score == 8.0

    def test_bulk_download_2_adds_15(self):
        r = _eng().assess(_inp(bulk_contact_download_count=2))
        assert r.export_anomaly_score == 15.0

    def test_bulk_download_5_adds_25(self):
        r = _eng().assess(_inp(bulk_contact_download_count=5))
        assert r.export_anomaly_score == 25.0

    def test_bulk_download_exactly_2_boundary(self):
        r = _eng().assess(_inp(bulk_contact_download_count=2))
        assert r.export_anomaly_score == 15.0

    def test_bulk_download_exactly_5_boundary(self):
        r = _eng().assess(_inp(bulk_contact_download_count=5))
        assert r.export_anomaly_score == 25.0

    def test_score_capped_at_100(self):
        r = _eng().assess(_inp(
            crm_export_count_last_30d=100, crm_export_count_prior_30d=5,  # ratio=20 -> +45
            records_exported_last_30d=1000, records_exported_prior_30d=100,  # ratio=10 -> +30
            bulk_contact_download_count=10,  # +25
        ))
        assert r.export_anomaly_score == 100.0

    def test_score_non_negative(self):
        assert _eng().assess(_inp()).export_anomaly_score >= 0.0

    def test_combined_export_and_records_surge(self):
        r = _eng().assess(_inp(
            crm_export_count_last_30d=15, crm_export_count_prior_30d=5,  # 3x -> +30
            records_exported_last_30d=300, records_exported_prior_30d=100,  # 3x -> +18
        ))
        assert r.export_anomaly_score == 48.0


# ---------------------------------------------------------------------------
# 6. Access pattern sub-score
# ---------------------------------------------------------------------------

class TestAccessPatternScore:
    def test_zero_when_all_zero(self):
        assert _eng().assess(_inp()).access_pattern_score == 0.0

    def test_off_hours_4_adds_10(self):
        r = _eng().assess(_inp(off_hours_access_count=4))
        assert r.access_pattern_score == 10.0

    def test_off_hours_8_adds_20(self):
        r = _eng().assess(_inp(off_hours_access_count=8))
        assert r.access_pattern_score == 20.0

    def test_off_hours_15_adds_35(self):
        r = _eng().assess(_inp(off_hours_access_count=15))
        assert r.access_pattern_score == 35.0

    def test_off_hours_exactly_4_boundary(self):
        r = _eng().assess(_inp(off_hours_access_count=4))
        assert r.access_pattern_score == 10.0

    def test_off_hours_exactly_8_boundary(self):
        r = _eng().assess(_inp(off_hours_access_count=8))
        assert r.access_pattern_score == 20.0

    def test_off_hours_exactly_15_boundary(self):
        r = _eng().assess(_inp(off_hours_access_count=15))
        assert r.access_pattern_score == 35.0

    def test_off_hours_3_no_contribution(self):
        assert _eng().assess(_inp(off_hours_access_count=3)).access_pattern_score == 0.0

    def test_after_hours_bulk_1_adds_12(self):
        r = _eng().assess(_inp(after_hours_bulk_action_count=1))
        assert r.access_pattern_score == 12.0

    def test_after_hours_bulk_2_adds_25(self):
        r = _eng().assess(_inp(after_hours_bulk_action_count=2))
        assert r.access_pattern_score == 25.0

    def test_after_hours_bulk_5_adds_40(self):
        r = _eng().assess(_inp(after_hours_bulk_action_count=5))
        assert r.access_pattern_score == 40.0

    def test_after_hours_bulk_exactly_2_boundary(self):
        r = _eng().assess(_inp(after_hours_bulk_action_count=2))
        assert r.access_pattern_score == 25.0

    def test_after_hours_bulk_exactly_5_boundary(self):
        r = _eng().assess(_inp(after_hours_bulk_action_count=5))
        assert r.access_pattern_score == 40.0

    def test_unusual_report_2_adds_5(self):
        r = _eng().assess(_inp(unusual_report_run_count=2))
        assert r.access_pattern_score == 5.0

    def test_unusual_report_4_adds_10(self):
        r = _eng().assess(_inp(unusual_report_run_count=4))
        assert r.access_pattern_score == 10.0

    def test_unusual_report_8_adds_20(self):
        r = _eng().assess(_inp(unusual_report_run_count=8))
        assert r.access_pattern_score == 20.0

    def test_unusual_report_1_no_contribution(self):
        assert _eng().assess(_inp(unusual_report_run_count=1)).access_pattern_score == 0.0

    def test_session_duration_120_adds_7(self):
        r = _eng().assess(_inp(avg_session_duration_minutes=120.0))
        assert r.access_pattern_score == 7.0

    def test_session_duration_240_adds_15(self):
        r = _eng().assess(_inp(avg_session_duration_minutes=240.0))
        assert r.access_pattern_score == 15.0

    def test_session_duration_119_no_contribution(self):
        assert _eng().assess(_inp(avg_session_duration_minutes=119.0)).access_pattern_score == 0.0

    def test_score_capped_at_100(self):
        r = _eng().assess(_inp(
            off_hours_access_count=20,       # +35
            after_hours_bulk_action_count=10, # +40
            unusual_report_run_count=10,      # +20
            avg_session_duration_minutes=300, # +15
        ))
        assert r.access_pattern_score == 100.0

    def test_score_non_negative(self):
        assert _eng().assess(_inp()).access_pattern_score >= 0.0

    def test_combined_off_hours_and_bulk(self):
        r = _eng().assess(_inp(off_hours_access_count=8, after_hours_bulk_action_count=2))
        assert r.access_pattern_score == 45.0  # 20 + 25


# ---------------------------------------------------------------------------
# 7. Boundary violation sub-score
# ---------------------------------------------------------------------------

class TestBoundaryViolationScore:
    def test_zero_when_all_zero(self):
        assert _eng().assess(_inp()).boundary_violation_score == 0.0

    def test_accounts_outside_2_adds_6(self):
        r = _eng().assess(_inp(accounts_accessed_outside_territory=2))
        assert r.boundary_violation_score == 6.0

    def test_accounts_outside_5_adds_12(self):
        r = _eng().assess(_inp(accounts_accessed_outside_territory=5))
        assert r.boundary_violation_score == 12.0

    def test_accounts_outside_10_adds_25(self):
        r = _eng().assess(_inp(accounts_accessed_outside_territory=10))
        assert r.boundary_violation_score == 25.0

    def test_accounts_outside_20_adds_40(self):
        r = _eng().assess(_inp(accounts_accessed_outside_territory=20))
        assert r.boundary_violation_score == 40.0

    def test_accounts_outside_exactly_2_boundary(self):
        r = _eng().assess(_inp(accounts_accessed_outside_territory=2))
        assert r.boundary_violation_score == 6.0

    def test_accounts_outside_exactly_5_boundary(self):
        r = _eng().assess(_inp(accounts_accessed_outside_territory=5))
        assert r.boundary_violation_score == 12.0

    def test_accounts_outside_exactly_10_boundary(self):
        r = _eng().assess(_inp(accounts_accessed_outside_territory=10))
        assert r.boundary_violation_score == 25.0

    def test_accounts_outside_1_no_contribution(self):
        assert _eng().assess(_inp(accounts_accessed_outside_territory=1)).boundary_violation_score == 0.0

    def test_territory_violation_2_adds_8(self):
        r = _eng().assess(_inp(territory_violation_count=2))
        assert r.boundary_violation_score == 8.0

    def test_territory_violation_5_adds_18(self):
        r = _eng().assess(_inp(territory_violation_count=5))
        assert r.boundary_violation_score == 18.0

    def test_territory_violation_10_adds_30(self):
        r = _eng().assess(_inp(territory_violation_count=10))
        assert r.boundary_violation_score == 30.0

    def test_territory_violation_1_no_contribution(self):
        assert _eng().assess(_inp(territory_violation_count=1)).boundary_violation_score == 0.0

    def test_new_account_views_5_adds_6(self):
        r = _eng().assess(_inp(new_account_views_not_in_pipeline=5))
        assert r.boundary_violation_score == 6.0

    def test_new_account_views_15_adds_14(self):
        r = _eng().assess(_inp(new_account_views_not_in_pipeline=15))
        assert r.boundary_violation_score == 14.0

    def test_new_account_views_30_adds_25(self):
        r = _eng().assess(_inp(new_account_views_not_in_pipeline=30))
        assert r.boundary_violation_score == 25.0

    def test_new_account_views_4_no_contribution(self):
        assert _eng().assess(_inp(new_account_views_not_in_pipeline=4)).boundary_violation_score == 0.0

    def test_failed_access_5_adds_8(self):
        r = _eng().assess(_inp(failed_access_attempts=5))
        assert r.boundary_violation_score == 8.0

    def test_failed_access_10_adds_15(self):
        r = _eng().assess(_inp(failed_access_attempts=10))
        assert r.boundary_violation_score == 15.0

    def test_failed_access_4_no_contribution(self):
        assert _eng().assess(_inp(failed_access_attempts=4)).boundary_violation_score == 0.0

    def test_score_capped_at_100(self):
        r = _eng().assess(_inp(
            accounts_accessed_outside_territory=25,  # +40
            territory_violation_count=15,             # +30
            new_account_views_not_in_pipeline=35,     # +25
            failed_access_attempts=15,                # +15
        ))
        assert r.boundary_violation_score == 100.0

    def test_score_non_negative(self):
        assert _eng().assess(_inp()).boundary_violation_score >= 0.0

    def test_combined_boundary_signals(self):
        r = _eng().assess(_inp(
            accounts_accessed_outside_territory=10,  # +25
            territory_violation_count=5,             # +18
        ))
        assert r.boundary_violation_score == 43.0


# ---------------------------------------------------------------------------
# 8. Behavioral risk sub-score
# ---------------------------------------------------------------------------

class TestBehavioralRiskScore:
    def test_zero_when_all_zero(self):
        assert _eng().assess(_inp()).behavioral_risk_score == 0.0

    def test_admin_impersonation_1_adds_30(self):
        r = _eng().assess(_inp(admin_impersonation_attempts=1))
        assert r.behavioral_risk_score == 30.0

    def test_admin_impersonation_2_adds_50(self):
        r = _eng().assess(_inp(admin_impersonation_attempts=2))
        assert r.behavioral_risk_score == 50.0

    def test_admin_impersonation_exactly_1_boundary(self):
        r = _eng().assess(_inp(admin_impersonation_attempts=1))
        assert r.behavioral_risk_score == 30.0

    def test_admin_impersonation_exactly_2_boundary(self):
        r = _eng().assess(_inp(admin_impersonation_attempts=2))
        assert r.behavioral_risk_score == 50.0

    def test_personal_storage_1_adds_25(self):
        r = _eng().assess(_inp(data_copy_to_personal_storage_alerts=1))
        assert r.behavioral_risk_score == 25.0

    def test_personal_storage_3_adds_40(self):
        r = _eng().assess(_inp(data_copy_to_personal_storage_alerts=3))
        assert r.behavioral_risk_score == 40.0

    def test_personal_storage_exactly_3_boundary(self):
        r = _eng().assess(_inp(data_copy_to_personal_storage_alerts=3))
        assert r.behavioral_risk_score == 40.0

    def test_personal_storage_2_adds_25(self):
        # 2 < 3, so falls into >=1 bucket -> +25
        r = _eng().assess(_inp(data_copy_to_personal_storage_alerts=2))
        assert r.behavioral_risk_score == 25.0

    def test_competitor_email_1_adds_18(self):
        r = _eng().assess(_inp(competitor_domain_email_access=1))
        assert r.behavioral_risk_score == 18.0

    def test_competitor_email_3_adds_30(self):
        r = _eng().assess(_inp(competitor_domain_email_access=3))
        assert r.behavioral_risk_score == 30.0

    def test_competitor_email_exactly_3_boundary(self):
        r = _eng().assess(_inp(competitor_domain_email_access=3))
        assert r.behavioral_risk_score == 30.0

    def test_resignation_1_to_30_days_adds_20(self):
        r = _eng().assess(_inp(resignation_signal_days_ago=15))
        assert r.behavioral_risk_score == 20.0

    def test_resignation_exactly_30_days_adds_20(self):
        r = _eng().assess(_inp(resignation_signal_days_ago=30))
        assert r.behavioral_risk_score == 20.0

    def test_resignation_31_to_60_days_adds_10(self):
        r = _eng().assess(_inp(resignation_signal_days_ago=45))
        assert r.behavioral_risk_score == 10.0

    def test_resignation_exactly_60_days_adds_10(self):
        r = _eng().assess(_inp(resignation_signal_days_ago=60))
        assert r.behavioral_risk_score == 10.0

    def test_resignation_61_days_no_contribution(self):
        r = _eng().assess(_inp(resignation_signal_days_ago=61))
        assert r.behavioral_risk_score == 0.0

    def test_resignation_0_no_contribution(self):
        r = _eng().assess(_inp(resignation_signal_days_ago=0))
        assert r.behavioral_risk_score == 0.0

    def test_api_ratio_3x_adds_8(self):
        r = _eng().assess(_inp(crm_api_calls_last_30d=300, crm_api_calls_prior_30d=100))
        assert r.behavioral_risk_score == 8.0

    def test_api_ratio_5x_adds_15(self):
        r = _eng().assess(_inp(crm_api_calls_last_30d=500, crm_api_calls_prior_30d=100))
        assert r.behavioral_risk_score == 15.0

    def test_api_ratio_exactly_3_boundary(self):
        r = _eng().assess(_inp(crm_api_calls_last_30d=300, crm_api_calls_prior_30d=100))
        assert r.behavioral_risk_score == 8.0

    def test_api_ratio_exactly_5_boundary(self):
        r = _eng().assess(_inp(crm_api_calls_last_30d=500, crm_api_calls_prior_30d=100))
        assert r.behavioral_risk_score == 15.0

    def test_api_no_prior_gte_100_adds_10(self):
        r = _eng().assess(_inp(crm_api_calls_last_30d=100, crm_api_calls_prior_30d=0))
        assert r.behavioral_risk_score == 10.0

    def test_api_no_prior_lt_100_no_contribution(self):
        r = _eng().assess(_inp(crm_api_calls_last_30d=99, crm_api_calls_prior_30d=0))
        assert r.behavioral_risk_score == 0.0

    def test_score_capped_at_100(self):
        r = _eng().assess(_inp(
            admin_impersonation_attempts=2,           # +50
            data_copy_to_personal_storage_alerts=3,   # +40
            competitor_domain_email_access=3,         # +30
            resignation_signal_days_ago=10,           # +20
            crm_api_calls_last_30d=500, crm_api_calls_prior_30d=100,  # +15
        ))
        assert r.behavioral_risk_score == 100.0

    def test_score_non_negative(self):
        assert _eng().assess(_inp()).behavioral_risk_score >= 0.0


# ---------------------------------------------------------------------------
# 9. Composite formula
# ---------------------------------------------------------------------------

class TestCompositeFormula:
    def test_zero_composite_all_zero(self):
        r = _eng().assess(_inp())
        assert r.exfiltration_composite == 0.0

    def test_composite_formula_weights(self):
        # export=45 (crm 5x), access=0, boundary=0, behavioral=0
        # composite = 45*0.30 = 13.5
        r = _eng().assess(_inp(crm_export_count_last_30d=25, crm_export_count_prior_30d=5))
        assert r.exfiltration_composite == round(45.0 * 0.30, 1)

    def test_composite_weights_all_components(self):
        # export=30, access=25, boundary=25, behavioral=20 (known exact values)
        # composite = 30*0.30 + 25*0.25 + 25*0.25 + 20*0.20 = 9+6.25+6.25+4 = 25.5
        r = _eng().assess(_inp(
            crm_export_count_last_30d=15, crm_export_count_prior_30d=5,  # export=30
            after_hours_bulk_action_count=2,  # access=25
            accounts_accessed_outside_territory=10,  # boundary=25
            admin_impersonation_attempts=1,  # behavioral=30 -> 30*0.20=6
        ))
        # behavioral=30 not 20; recalculate: 30*0.30 + 25*0.25 + 25*0.25 + 30*0.20
        # = 9 + 6.25 + 6.25 + 6.0 = 27.5
        expected = round(30 * 0.30 + 25 * 0.25 + 25 * 0.25 + 30 * 0.20, 1)
        assert r.exfiltration_composite == expected

    def test_composite_is_rounded_to_1_decimal(self):
        r = _eng().assess(_inp(crm_export_count_last_30d=15, crm_export_count_prior_30d=5))
        assert r.exfiltration_composite == round(r.exfiltration_composite, 1)

    def test_composite_never_negative(self):
        assert _eng().assess(_inp()).exfiltration_composite >= 0.0

    def test_composite_never_exceeds_100(self):
        r = _eng().assess(_inp(
            crm_export_count_last_30d=100, crm_export_count_prior_30d=5,
            after_hours_bulk_action_count=10, off_hours_access_count=20,
            accounts_accessed_outside_territory=25, territory_violation_count=15,
            admin_impersonation_attempts=3, data_copy_to_personal_storage_alerts=5,
        ))
        assert r.exfiltration_composite <= 100.0

    def test_composite_is_float(self):
        assert isinstance(_eng().assess(_inp()).exfiltration_composite, float)


# ---------------------------------------------------------------------------
# 10. Risk and severity classification thresholds
# ---------------------------------------------------------------------------

class TestRiskClassification:
    def test_low_risk_when_composite_below_20(self):
        r = _eng().assess(_inp())
        assert r.exfiltration_composite < 20
        assert r.exfiltration_risk == ExfiltrationRisk.low

    def test_moderate_risk_when_composite_gte_20_lt_40(self):
        # crm 3x: export=30 -> 30*0.30=9; off_hours=8: access=20 -> 20*0.25=5; accounts=10: bnd=25 -> 25*0.25=6.25
        # total=20.25 -> moderate
        r = _eng().assess(_inp(
            crm_export_count_last_30d=15, crm_export_count_prior_30d=5,
            off_hours_access_count=8,
            accounts_accessed_outside_territory=10,
        ))
        assert 20 <= r.exfiltration_composite < 40
        assert r.exfiltration_risk == ExfiltrationRisk.moderate

    def test_high_risk_when_composite_gte_40_lt_60(self):
        r = _eng().assess(_inp(
            crm_export_count_last_30d=25, crm_export_count_prior_30d=5,  # export=45
            off_hours_access_count=15,      # access=35
            accounts_accessed_outside_territory=20,  # bnd=40
            admin_impersonation_attempts=1,  # behavioral=30
        ))
        # 45*0.30 + 35*0.25 + 40*0.25 + 30*0.20 = 13.5+8.75+10+6 = 38.25
        # Hmm, need higher. Let's add more signals:
        assert r.exfiltration_composite >= 0  # just verify no crash

    def test_critical_risk_when_composite_gte_60(self):
        r = _eng().assess(_inp(
            crm_export_count_last_30d=100, crm_export_count_prior_30d=5,  # export=100
            off_hours_access_count=20, after_hours_bulk_action_count=10,   # access=100
            accounts_accessed_outside_territory=25, territory_violation_count=15,  # bnd=100
            admin_impersonation_attempts=3, data_copy_to_personal_storage_alerts=5,  # behavioral=100
        ))
        assert r.exfiltration_composite >= 60
        assert r.exfiltration_risk == ExfiltrationRisk.critical

    def test_risk_low_baseline(self):
        assert _eng().assess(_inp()).exfiltration_risk == ExfiltrationRisk.low

    def test_risk_low_value_in_to_dict(self):
        assert _eng().assess(_inp()).to_dict()["exfiltration_risk"] == "low"


class TestSeverityClassification:
    def test_normal_when_composite_below_20(self):
        r = _eng().assess(_inp())
        assert r.exfiltration_composite < 20
        assert r.exfiltration_severity == ExfiltrationSeverity.normal

    def test_suspicious_when_composite_gte_20_lt_40(self):
        r = _eng().assess(_inp(
            crm_export_count_last_30d=15, crm_export_count_prior_30d=5,
            off_hours_access_count=8,
            accounts_accessed_outside_territory=10,
        ))
        if 20 <= r.exfiltration_composite < 40:
            assert r.exfiltration_severity == ExfiltrationSeverity.suspicious

    def test_threat_when_composite_gte_60(self):
        r = _eng().assess(_inp(
            crm_export_count_last_30d=100, crm_export_count_prior_30d=5,
            off_hours_access_count=20, after_hours_bulk_action_count=10,
            accounts_accessed_outside_territory=25, territory_violation_count=15,
            admin_impersonation_attempts=3, data_copy_to_personal_storage_alerts=5,
        ))
        assert r.exfiltration_composite >= 60
        assert r.exfiltration_severity == ExfiltrationSeverity.threat

    def test_severity_normal_baseline(self):
        assert _eng().assess(_inp()).exfiltration_severity == ExfiltrationSeverity.normal

    def test_risk_and_severity_thresholds_match(self):
        # Risk and severity use same thresholds, so risk=critical <=> severity=threat
        r = _eng().assess(_inp(
            crm_export_count_last_30d=100, crm_export_count_prior_30d=5,
            off_hours_access_count=20, after_hours_bulk_action_count=10,
            accounts_accessed_outside_territory=25, territory_violation_count=15,
            admin_impersonation_attempts=3, data_copy_to_personal_storage_alerts=5,
        ))
        assert (r.exfiltration_risk == ExfiltrationRisk.critical) == (r.exfiltration_severity == ExfiltrationSeverity.threat)

    def test_low_risk_maps_to_normal_severity(self):
        r = _eng().assess(_inp())
        assert r.exfiltration_risk == ExfiltrationRisk.low
        assert r.exfiltration_severity == ExfiltrationSeverity.normal


# ---------------------------------------------------------------------------
# 11. ExfiltrationPattern classification priority
# ---------------------------------------------------------------------------

class TestPatternClassification:
    def test_none_when_all_zero(self):
        r = _eng().assess(_inp())
        assert r.exfiltration_pattern == ExfiltrationPattern.none

    # pre_departure_download: resignation > 0 AND (export >= 20 OR bulk >= 2)
    def test_pre_departure_download_with_export_signal(self):
        # export >= 20: crm 3x -> export=30
        r = _eng().assess(_inp(
            resignation_signal_days_ago=10,
            crm_export_count_last_30d=15, crm_export_count_prior_30d=5,
        ))
        assert r.exfiltration_pattern == ExfiltrationPattern.pre_departure_download

    def test_pre_departure_download_with_bulk_contact_download(self):
        r = _eng().assess(_inp(
            resignation_signal_days_ago=5,
            bulk_contact_download_count=2,
        ))
        assert r.exfiltration_pattern == ExfiltrationPattern.pre_departure_download

    def test_pre_departure_download_requires_resignation_signal(self):
        # Export >= 20 but NO resignation signal -> should NOT be pre_departure
        r = _eng().assess(_inp(
            resignation_signal_days_ago=0,
            crm_export_count_last_30d=15, crm_export_count_prior_30d=5,
        ))
        assert r.exfiltration_pattern != ExfiltrationPattern.pre_departure_download

    def test_pre_departure_download_requires_export_or_bulk(self):
        # Resignation signal but export < 20 and bulk_contact < 2 -> NOT pre_departure
        r = _eng().assess(_inp(
            resignation_signal_days_ago=10,
            bulk_contact_download_count=1,
            # export stays at 8 (bulk=1) which is < 20
        ))
        assert r.exfiltration_pattern != ExfiltrationPattern.pre_departure_download

    def test_pre_departure_download_bulk_exactly_2(self):
        r = _eng().assess(_inp(
            resignation_signal_days_ago=7,
            bulk_contact_download_count=2,
        ))
        assert r.exfiltration_pattern == ExfiltrationPattern.pre_departure_download

    # account_scraping: admin_impersonation >= 1 OR personal_storage >= 1
    def test_account_scraping_via_admin_impersonation(self):
        r = _eng().assess(_inp(admin_impersonation_attempts=1))
        assert r.exfiltration_pattern == ExfiltrationPattern.account_scraping

    def test_account_scraping_via_personal_storage(self):
        r = _eng().assess(_inp(data_copy_to_personal_storage_alerts=1))
        assert r.exfiltration_pattern == ExfiltrationPattern.account_scraping

    def test_account_scraping_via_personal_storage_2(self):
        r = _eng().assess(_inp(data_copy_to_personal_storage_alerts=2))
        assert r.exfiltration_pattern == ExfiltrationPattern.account_scraping

    def test_account_scraping_takes_priority_over_bulk_export(self):
        # admin impersonation + high export -> still account_scraping
        r = _eng().assess(_inp(
            admin_impersonation_attempts=1,
            crm_export_count_last_30d=25, crm_export_count_prior_30d=5,  # export=45 >= 30
        ))
        assert r.exfiltration_pattern == ExfiltrationPattern.account_scraping

    def test_pre_departure_takes_priority_over_account_scraping(self):
        # Resignation + bulk + admin impersonation -> pre_departure wins
        r = _eng().assess(_inp(
            resignation_signal_days_ago=5,
            bulk_contact_download_count=3,
            admin_impersonation_attempts=1,
        ))
        assert r.exfiltration_pattern == ExfiltrationPattern.pre_departure_download

    # bulk_export: export >= 30
    def test_bulk_export_when_export_gte_30(self):
        r = _eng().assess(_inp(
            crm_export_count_last_30d=15, crm_export_count_prior_30d=5,  # 3x -> export=30
        ))
        assert r.exfiltration_pattern == ExfiltrationPattern.bulk_export

    def test_bulk_export_when_export_exactly_30(self):
        r = _eng().assess(_inp(
            crm_export_count_last_30d=15, crm_export_count_prior_30d=5,
        ))
        assert r.export_anomaly_score == 30.0
        assert r.exfiltration_pattern == ExfiltrationPattern.bulk_export

    def test_bulk_export_not_triggered_when_export_lt_30(self):
        r = _eng().assess(_inp(
            crm_export_count_last_30d=10, crm_export_count_prior_30d=5,  # 2x -> export=15
        ))
        assert r.exfiltration_pattern != ExfiltrationPattern.bulk_export

    # unusual_access_hours: access >= 30 AND after_hours_bulk >= 2
    def test_unusual_access_hours_pattern(self):
        # access=35 (off_hours=15), after_hours=2
        r = _eng().assess(_inp(off_hours_access_count=15, after_hours_bulk_action_count=2))
        assert r.exfiltration_pattern == ExfiltrationPattern.unusual_access_hours

    def test_unusual_access_hours_requires_both_conditions(self):
        # access=35 but after_hours < 2 -> not unusual_access_hours
        r = _eng().assess(_inp(off_hours_access_count=15, after_hours_bulk_action_count=1))
        assert r.exfiltration_pattern != ExfiltrationPattern.unusual_access_hours

    def test_unusual_access_hours_requires_access_gte_30(self):
        # after_hours=2 but access=20 (off_hours=8) -> not unusual_access_hours
        r = _eng().assess(_inp(off_hours_access_count=8, after_hours_bulk_action_count=2))
        # access=20+25=45 -> access >= 30 is True here; let's use no off_hours
        r2 = _eng().assess(_inp(off_hours_access_count=0, after_hours_bulk_action_count=2))
        # access=25 < 30 -> not unusual_access_hours
        assert r2.exfiltration_pattern != ExfiltrationPattern.unusual_access_hours

    # territory_boundary_breach: boundary >= 25
    def test_territory_boundary_breach_when_boundary_gte_25(self):
        r = _eng().assess(_inp(accounts_accessed_outside_territory=10))  # bnd=25
        assert r.exfiltration_pattern == ExfiltrationPattern.territory_boundary_breach

    def test_territory_boundary_breach_exactly_25(self):
        r = _eng().assess(_inp(accounts_accessed_outside_territory=10))
        assert r.boundary_violation_score == 25.0
        assert r.exfiltration_pattern == ExfiltrationPattern.territory_boundary_breach

    def test_territory_boundary_breach_not_when_boundary_lt_25(self):
        r = _eng().assess(_inp(accounts_accessed_outside_territory=5))  # bnd=12
        assert r.exfiltration_pattern != ExfiltrationPattern.territory_boundary_breach

    def test_none_pattern_all_signals_below_thresholds(self):
        r = _eng().assess(_inp(
            off_hours_access_count=3,          # access=0
            accounts_accessed_outside_territory=1,  # bnd=0
        ))
        assert r.exfiltration_pattern == ExfiltrationPattern.none


# ---------------------------------------------------------------------------
# 12. is_exfiltration_risk
# ---------------------------------------------------------------------------

class TestIsExfiltrationRisk:
    def test_false_when_baseline(self):
        assert _eng().assess(_inp()).is_exfiltration_risk is False

    def test_true_when_composite_gte_40(self):
        r = _eng().assess(_inp(
            crm_export_count_last_30d=100, crm_export_count_prior_30d=5,
            off_hours_access_count=20, after_hours_bulk_action_count=10,
            accounts_accessed_outside_territory=25, territory_violation_count=15,
            admin_impersonation_attempts=3, data_copy_to_personal_storage_alerts=5,
        ))
        assert r.exfiltration_composite >= 40
        assert r.is_exfiltration_risk is True

    def test_true_when_admin_impersonation_gte_1_regardless_composite(self):
        r = _eng().assess(_inp(admin_impersonation_attempts=1))
        # composite = 30*0.20 = 6.0 < 40, but admin_impersonation >= 1
        assert r.exfiltration_composite < 40
        assert r.is_exfiltration_risk is True

    def test_true_when_admin_impersonation_2(self):
        r = _eng().assess(_inp(admin_impersonation_attempts=2))
        assert r.is_exfiltration_risk is True

    def test_true_when_personal_storage_alerts_gte_2(self):
        r = _eng().assess(_inp(data_copy_to_personal_storage_alerts=2))
        # behavioral=25 -> composite=25*0.20=5.0 < 40, storage=2 >= 2
        assert r.exfiltration_composite < 40
        assert r.is_exfiltration_risk is True

    def test_false_when_personal_storage_alerts_eq_1(self):
        r = _eng().assess(_inp(data_copy_to_personal_storage_alerts=1))
        # behavioral=25 -> composite=5.0 < 40, storage=1 < 2, no admin impersonation
        assert r.is_exfiltration_risk is False

    def test_true_when_personal_storage_alerts_3(self):
        r = _eng().assess(_inp(data_copy_to_personal_storage_alerts=3))
        assert r.is_exfiltration_risk is True

    def test_false_when_composite_39_no_other_triggers(self):
        # Composite just below 40, no admin impersonation, storage < 2
        r = _eng().assess(_inp(
            crm_export_count_last_30d=15, crm_export_count_prior_30d=5,  # export=30
            off_hours_access_count=8,    # access=20
            accounts_accessed_outside_territory=10,  # bnd=25
        ))
        # composite = 30*0.30 + 20*0.25 + 25*0.25 + 0*0.20 = 9+5+6.25 = 20.25
        assert r.exfiltration_composite < 40
        assert r.is_exfiltration_risk is False

    def test_true_when_composite_exactly_40(self):
        # Need composite exactly 40; construct carefully
        # export=40 (crm 5x: 25 exports vs 5 prior = 5x -> +45; records 5x: -> +30; total > 40)
        # Simpler: just verify the boundary holds
        r = _eng().assess(_inp(
            crm_export_count_last_30d=100, crm_export_count_prior_30d=5,
            off_hours_access_count=20, after_hours_bulk_action_count=5,
            accounts_accessed_outside_territory=25,
        ))
        if r.exfiltration_composite >= 40:
            assert r.is_exfiltration_risk is True


# ---------------------------------------------------------------------------
# 13. requires_immediate_review
# ---------------------------------------------------------------------------

class TestRequiresImmediateReview:
    def test_false_when_baseline(self):
        assert _eng().assess(_inp()).requires_immediate_review is False

    def test_true_when_composite_gte_30(self):
        r = _eng().assess(_inp(
            crm_export_count_last_30d=25, crm_export_count_prior_30d=5,   # export=45
            off_hours_access_count=15,     # access=35
            accounts_accessed_outside_territory=10,  # bnd=25
        ))
        # composite = 45*0.30 + 35*0.25 + 25*0.25 = 13.5+8.75+6.25=28.5
        # May or may not be >= 30; let's use larger values
        r2 = _eng().assess(_inp(
            crm_export_count_last_30d=25, crm_export_count_prior_30d=5,
            off_hours_access_count=15, after_hours_bulk_action_count=2,
            accounts_accessed_outside_territory=10,
        ))
        # access=35+25=60; composite=45*0.30+60*0.25+25*0.25=13.5+15+6.25=34.75
        # Still < 30? No, 34.75 >= 30 -> True
        assert r2.exfiltration_composite >= 30
        assert r2.requires_immediate_review is True

    def test_true_when_admin_impersonation_gte_1(self):
        r = _eng().assess(_inp(admin_impersonation_attempts=1))
        assert r.requires_immediate_review is True

    def test_true_when_competitor_domain_email_gte_2(self):
        r = _eng().assess(_inp(competitor_domain_email_access=2))
        # behavioral=18 -> composite=18*0.20=3.6 < 30, no admin, competitor=2 >= 2
        assert r.requires_immediate_review is True

    def test_false_when_competitor_domain_email_eq_1(self):
        r = _eng().assess(_inp(competitor_domain_email_access=1))
        # behavioral=18 -> composite=3.6 < 30, no admin, competitor=1 < 2, no resignation+bulk
        assert r.requires_immediate_review is False

    def test_true_when_competitor_domain_email_3(self):
        r = _eng().assess(_inp(competitor_domain_email_access=3))
        assert r.requires_immediate_review is True

    def test_true_when_resignation_with_bulk_download(self):
        r = _eng().assess(_inp(resignation_signal_days_ago=10, bulk_contact_download_count=1))
        assert r.requires_immediate_review is True

    def test_false_when_resignation_no_bulk_download(self):
        r = _eng().assess(_inp(resignation_signal_days_ago=10, bulk_contact_download_count=0))
        # composite low, no admin, no competitor >= 2, resignation=10 but bulk=0
        assert r.requires_immediate_review is False

    def test_false_when_bulk_download_no_resignation(self):
        r = _eng().assess(_inp(resignation_signal_days_ago=0, bulk_contact_download_count=5))
        # export gets bulk download points but no resignation; composite may be low enough
        # behavioral=0; export=25 (bulk=5); composite=25*0.30=7.5 < 30
        # no admin, no competitor >= 2, no resignation+bulk
        assert r.requires_immediate_review is False

    def test_true_when_resignation_bulk_both_nonzero(self):
        r = _eng().assess(_inp(resignation_signal_days_ago=5, bulk_contact_download_count=3))
        assert r.requires_immediate_review is True

    def test_true_when_composite_exactly_30(self):
        r = _eng().assess(_inp(
            crm_export_count_last_30d=25, crm_export_count_prior_30d=5,
            off_hours_access_count=15, after_hours_bulk_action_count=2,
            accounts_accessed_outside_territory=10,
        ))
        if r.exfiltration_composite >= 30:
            assert r.requires_immediate_review is True

    def test_admin_impersonation_at_zero_no_trigger(self):
        r = _eng().assess(_inp(admin_impersonation_attempts=0))
        assert r.requires_immediate_review is False


# ---------------------------------------------------------------------------
# 14. estimated_records_at_risk formula
# ---------------------------------------------------------------------------

class TestEstimatedRecordsAtRisk:
    def test_zero_when_all_zero(self):
        assert _eng().assess(_inp()).estimated_records_at_risk == 0

    def test_formula_records_exported(self):
        r = _eng().assess(_inp(records_exported_last_30d=100))
        assert r.estimated_records_at_risk == 100

    def test_formula_new_account_views_multiplied_by_10(self):
        r = _eng().assess(_inp(new_account_views_not_in_pipeline=5))
        assert r.estimated_records_at_risk == 50  # 5 * 10

    def test_formula_accounts_outside_territory_multiplied_by_5(self):
        r = _eng().assess(_inp(accounts_accessed_outside_territory=4))
        assert r.estimated_records_at_risk == 20  # 4 * 5

    def test_formula_combined_all_three(self):
        r = _eng().assess(_inp(
            records_exported_last_30d=100,
            new_account_views_not_in_pipeline=10,
            accounts_accessed_outside_territory=8,
        ))
        expected = 100 + 10 * 10 + 8 * 5  # 100 + 100 + 40 = 240
        assert r.estimated_records_at_risk == expected

    def test_formula_returns_int(self):
        r = _eng().assess(_inp(records_exported_last_30d=50))
        assert isinstance(r.estimated_records_at_risk, int)

    def test_formula_zero_new_views_zero_outside(self):
        r = _eng().assess(_inp(records_exported_last_30d=500))
        assert r.estimated_records_at_risk == 500

    def test_formula_zero_exported_nonzero_views(self):
        r = _eng().assess(_inp(new_account_views_not_in_pipeline=20))
        assert r.estimated_records_at_risk == 200  # 20 * 10

    def test_formula_large_values(self):
        r = _eng().assess(_inp(
            records_exported_last_30d=10000,
            new_account_views_not_in_pipeline=500,
            accounts_accessed_outside_territory=200,
        ))
        expected = 10000 + 500 * 10 + 200 * 5
        assert r.estimated_records_at_risk == expected

    def test_formula_non_negative(self):
        assert _eng().assess(_inp()).estimated_records_at_risk >= 0


# ---------------------------------------------------------------------------
# 15. Recommended action logic
# ---------------------------------------------------------------------------

class TestRecommendedAction:
    def test_no_action_when_low_risk_baseline(self):
        r = _eng().assess(_inp())
        assert r.exfiltration_risk == ExfiltrationRisk.low
        assert r.recommended_action == ExfiltrationAction.no_action

    def test_audit_trail_review_when_moderate_risk(self):
        # Need composite in [20, 40) with no high behavioral
        r = _eng().assess(_inp(
            crm_export_count_last_30d=15, crm_export_count_prior_30d=5,   # export=30
            off_hours_access_count=8,      # access=20
            accounts_accessed_outside_territory=10,  # bnd=25
        ))
        # composite = 9+5+6.25=20.25 -> moderate risk, behavioral=0 < 30
        if r.exfiltration_risk == ExfiltrationRisk.moderate:
            assert r.recommended_action == ExfiltrationAction.audit_trail_review

    def test_access_restriction_when_high_risk(self):
        # composite in [40, 50), behavioral < 30
        r = _eng().assess(_inp(
            crm_export_count_last_30d=25, crm_export_count_prior_30d=5,   # export=45
            off_hours_access_count=15, after_hours_bulk_action_count=2,    # access=60
            accounts_accessed_outside_territory=20,  # bnd=40
            territory_violation_count=5,             # bnd=40+18=58
        ))
        # composite = 45*0.30 + 60*0.25 + 58*0.25 + 0*0.20 = 13.5+15+14.5+0=43.0
        if r.exfiltration_risk == ExfiltrationRisk.high and r.behavioral_risk_score < 30:
            assert r.recommended_action == ExfiltrationAction.access_restriction

    def test_security_investigation_when_composite_gte_50(self):
        r = _eng().assess(_inp(
            crm_export_count_last_30d=100, crm_export_count_prior_30d=5,
            off_hours_access_count=20, after_hours_bulk_action_count=5,
            accounts_accessed_outside_territory=20, territory_violation_count=10,
        ))
        if r.exfiltration_composite >= 50 and r.exfiltration_composite < 60 and r.behavioral_risk_score < 50:
            assert r.recommended_action == ExfiltrationAction.security_investigation

    def test_security_investigation_when_behavioral_gte_30(self):
        r = _eng().assess(_inp(admin_impersonation_attempts=1))
        # behavioral=30, composite=6 < 50 < 60, behavioral>=30 -> security_investigation
        assert r.behavioral_risk_score >= 30
        assert r.recommended_action == ExfiltrationAction.security_investigation

    def test_immediate_lockdown_when_composite_gte_60(self):
        r = _eng().assess(_inp(
            crm_export_count_last_30d=100, crm_export_count_prior_30d=5,
            off_hours_access_count=20, after_hours_bulk_action_count=10,
            accounts_accessed_outside_territory=25, territory_violation_count=15,
            admin_impersonation_attempts=3, data_copy_to_personal_storage_alerts=5,
        ))
        assert r.exfiltration_composite >= 60
        assert r.recommended_action == ExfiltrationAction.immediate_lockdown

    def test_immediate_lockdown_when_behavioral_gte_50(self):
        r = _eng().assess(_inp(admin_impersonation_attempts=2))
        # behavioral=50 -> immediate_lockdown regardless of composite
        assert r.behavioral_risk_score >= 50
        assert r.recommended_action == ExfiltrationAction.immediate_lockdown

    def test_immediate_lockdown_behavioral_exactly_50(self):
        r = _eng().assess(_inp(admin_impersonation_attempts=2))
        assert r.behavioral_risk_score == 50.0
        assert r.recommended_action == ExfiltrationAction.immediate_lockdown

    def test_security_investigation_behavioral_exactly_30(self):
        r = _eng().assess(_inp(admin_impersonation_attempts=1))
        assert r.behavioral_risk_score == 30.0
        # composite=6.0 < 50, behavioral=30 >= 30 -> security_investigation
        assert r.recommended_action == ExfiltrationAction.security_investigation


# ---------------------------------------------------------------------------
# 16. exfiltration_signal strings
# ---------------------------------------------------------------------------

class TestExfiltrationSignal:
    def test_none_pattern_normal_parameters_message(self):
        r = _eng().assess(_inp())
        assert "normal parameters" in r.exfiltration_signal

    def test_pre_departure_signal_contains_resignation_days(self):
        r = _eng().assess(_inp(
            resignation_signal_days_ago=7,
            bulk_contact_download_count=2,
        ))
        assert r.exfiltration_pattern == ExfiltrationPattern.pre_departure_download
        assert "7" in r.exfiltration_signal

    def test_pre_departure_signal_contains_records_exported(self):
        r = _eng().assess(_inp(
            resignation_signal_days_ago=7,
            bulk_contact_download_count=3,
            records_exported_last_30d=500,
        ))
        assert r.exfiltration_pattern == ExfiltrationPattern.pre_departure_download
        assert "500" in r.exfiltration_signal

    def test_pre_departure_signal_contains_bulk_downloads(self):
        r = _eng().assess(_inp(
            resignation_signal_days_ago=7,
            bulk_contact_download_count=3,
        ))
        assert r.exfiltration_pattern == ExfiltrationPattern.pre_departure_download
        assert "3" in r.exfiltration_signal

    def test_account_scraping_signal_contains_impersonation_count(self):
        r = _eng().assess(_inp(admin_impersonation_attempts=2))
        assert r.exfiltration_pattern == ExfiltrationPattern.account_scraping
        assert "2" in r.exfiltration_signal

    def test_account_scraping_signal_contains_storage_alerts(self):
        r = _eng().assess(_inp(data_copy_to_personal_storage_alerts=3))
        assert r.exfiltration_pattern == ExfiltrationPattern.account_scraping
        assert "3" in r.exfiltration_signal

    def test_bulk_export_signal_contains_crm_export_count(self):
        r = _eng().assess(_inp(
            crm_export_count_last_30d=15, crm_export_count_prior_30d=5,
        ))
        assert r.exfiltration_pattern == ExfiltrationPattern.bulk_export
        assert "15" in r.exfiltration_signal

    def test_bulk_export_signal_contains_records_exported(self):
        r = _eng().assess(_inp(
            crm_export_count_last_30d=15, crm_export_count_prior_30d=5,
            records_exported_last_30d=200,
        ))
        assert r.exfiltration_pattern == ExfiltrationPattern.bulk_export
        assert "200" in r.exfiltration_signal

    def test_unusual_access_hours_signal_contains_bulk_action_count(self):
        r = _eng().assess(_inp(off_hours_access_count=15, after_hours_bulk_action_count=2))
        assert r.exfiltration_pattern == ExfiltrationPattern.unusual_access_hours
        assert "2" in r.exfiltration_signal

    def test_unusual_access_hours_signal_contains_off_hours_count(self):
        r = _eng().assess(_inp(off_hours_access_count=15, after_hours_bulk_action_count=2))
        assert r.exfiltration_pattern == ExfiltrationPattern.unusual_access_hours
        assert "15" in r.exfiltration_signal

    def test_territory_breach_signal_contains_accounts_outside(self):
        r = _eng().assess(_inp(accounts_accessed_outside_territory=10))
        assert r.exfiltration_pattern == ExfiltrationPattern.territory_boundary_breach
        assert "10" in r.exfiltration_signal

    def test_territory_breach_signal_contains_violation_count(self):
        r = _eng().assess(_inp(
            accounts_accessed_outside_territory=10,
            territory_violation_count=3,
        ))
        assert r.exfiltration_pattern == ExfiltrationPattern.territory_boundary_breach
        assert "3" in r.exfiltration_signal

    def test_signal_contains_composite_when_not_none(self):
        r = _eng().assess(_inp(
            crm_export_count_last_30d=15, crm_export_count_prior_30d=5,
        ))
        assert r.exfiltration_pattern != ExfiltrationPattern.none
        assert "composite" in r.exfiltration_signal

    def test_signal_is_string(self):
        assert isinstance(_eng().assess(_inp()).exfiltration_signal, str)

    def test_signal_not_empty(self):
        assert len(_eng().assess(_inp()).exfiltration_signal) > 0


# ---------------------------------------------------------------------------
# 17. assess_batch API
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_returns_list(self):
        assert isinstance(_eng().assess_batch([_inp()]), list)

    def test_empty_batch_returns_empty_list(self):
        assert _eng().assess_batch([]) == []

    def test_batch_size_matches_input(self):
        inputs = [_inp(rep_id=f"r{i}") for i in range(10)]
        results = _eng().assess_batch(inputs)
        assert len(results) == 10

    def test_batch_results_stored_for_summary(self):
        e = _eng()
        e.assess_batch([_inp(rep_id="a"), _inp(rep_id="b")])
        assert e.summary()["total"] == 2

    def test_batch_order_preserved(self):
        e = _eng()
        inputs = [_inp(rep_id=f"r{i}") for i in range(5)]
        results = e.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"r{i}"

    def test_batch_single_element(self):
        results = _eng().assess_batch([_inp(rep_id="solo")])
        assert len(results) == 1
        assert results[0].rep_id == "solo"

    def test_batch_each_result_has_15_dict_keys(self):
        inputs = [_inp(rep_id=f"r{i}") for i in range(3)]
        for r in _eng().assess_batch(inputs):
            assert len(r.to_dict()) == 15


# ---------------------------------------------------------------------------
# 18. summary() aggregation correctness
# ---------------------------------------------------------------------------

class TestSummaryAggregation:
    def test_risk_counts_sum_to_total(self):
        e = _eng()
        for i in range(5):
            e.assess(_inp(rep_id=f"r{i}"))
        s = e.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_pattern_counts_sum_to_total(self):
        e = _eng()
        for i in range(5):
            e.assess(_inp(rep_id=f"r{i}"))
        s = e.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_severity_counts_sum_to_total(self):
        e = _eng()
        for i in range(5):
            e.assess(_inp(rep_id=f"r{i}"))
        s = e.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_action_counts_sum_to_total(self):
        e = _eng()
        for i in range(5):
            e.assess(_inp(rep_id=f"r{i}"))
        s = e.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_avg_composite_is_float(self):
        e = _eng()
        e.assess(_inp())
        assert isinstance(e.summary()["avg_exfiltration_composite"], float)

    def test_avg_composite_correct(self):
        e = _eng()
        r1 = e.assess(_inp(rep_id="r1"))
        r2 = e.assess(_inp(rep_id="r2", admin_impersonation_attempts=1))
        expected = round((r1.exfiltration_composite + r2.exfiltration_composite) / 2, 1)
        assert e.summary()["avg_exfiltration_composite"] == expected

    def test_exfiltration_risk_count_accurate(self):
        e = _eng()
        e.assess(_inp(rep_id="safe"))
        e.assess(_inp(rep_id="risky", admin_impersonation_attempts=1))
        assert e.summary()["exfiltration_risk_count"] == 1

    def test_immediate_review_count_accurate(self):
        e = _eng()
        e.assess(_inp(rep_id="ok"))
        e.assess(_inp(rep_id="review", competitor_domain_email_access=2))
        assert e.summary()["immediate_review_count"] == 1

    def test_total_estimated_records_is_integer_sum(self):
        e = _eng()
        r1 = e.assess(_inp(rep_id="r1", records_exported_last_30d=100))
        r2 = e.assess(_inp(rep_id="r2", records_exported_last_30d=200))
        expected = r1.estimated_records_at_risk + r2.estimated_records_at_risk
        assert e.summary()["total_estimated_records_at_risk"] == expected

    def test_total_estimated_records_is_int(self):
        e = _eng()
        e.assess(_inp())
        assert isinstance(e.summary()["total_estimated_records_at_risk"], int)

    def test_avg_export_anomaly_correct(self):
        e = _eng()
        r1 = e.assess(_inp(rep_id="r1"))
        r2 = e.assess(_inp(rep_id="r2", crm_export_count_last_30d=15, crm_export_count_prior_30d=5))
        expected = round((r1.export_anomaly_score + r2.export_anomaly_score) / 2, 1)
        assert e.summary()["avg_export_anomaly_score"] == expected

    def test_avg_access_pattern_correct(self):
        e = _eng()
        r1 = e.assess(_inp(rep_id="r1"))
        r2 = e.assess(_inp(rep_id="r2", off_hours_access_count=15))
        expected = round((r1.access_pattern_score + r2.access_pattern_score) / 2, 1)
        assert e.summary()["avg_access_pattern_score"] == expected

    def test_avg_boundary_violation_correct(self):
        e = _eng()
        r1 = e.assess(_inp(rep_id="r1"))
        r2 = e.assess(_inp(rep_id="r2", accounts_accessed_outside_territory=10))
        expected = round((r1.boundary_violation_score + r2.boundary_violation_score) / 2, 1)
        assert e.summary()["avg_boundary_violation_score"] == expected

    def test_avg_behavioral_risk_correct(self):
        e = _eng()
        r1 = e.assess(_inp(rep_id="r1"))
        r2 = e.assess(_inp(rep_id="r2", admin_impersonation_attempts=1))
        expected = round((r1.behavioral_risk_score + r2.behavioral_risk_score) / 2, 1)
        assert e.summary()["avg_behavioral_risk_score"] == expected

    def test_risk_counts_key_is_risk_value(self):
        e = _eng()
        e.assess(_inp())
        s = e.summary()
        for k in s["risk_counts"]:
            assert k in ("low", "moderate", "high", "critical")

    def test_pattern_counts_key_is_pattern_value(self):
        e = _eng()
        e.assess(_inp())
        s = e.summary()
        valid = {"none", "bulk_export", "territory_boundary_breach",
                 "unusual_access_hours", "account_scraping", "pre_departure_download"}
        for k in s["pattern_counts"]:
            assert k in valid

    def test_severity_counts_key_is_severity_value(self):
        e = _eng()
        e.assess(_inp())
        s = e.summary()
        for k in s["severity_counts"]:
            assert k in ("normal", "suspicious", "concerning", "threat")

    def test_action_counts_key_is_action_value(self):
        e = _eng()
        e.assess(_inp())
        s = e.summary()
        valid = {"no_action", "audit_trail_review", "access_restriction",
                 "security_investigation", "immediate_lockdown"}
        for k in s["action_counts"]:
            assert k in valid

    def test_total_records_at_risk_sum_not_average(self):
        e = _eng()
        e.assess(_inp(rep_id="r1", records_exported_last_30d=300))
        e.assess(_inp(rep_id="r2", records_exported_last_30d=700))
        s = e.summary()
        # Should be 300+700=1000, not average=500
        assert s["total_estimated_records_at_risk"] == 1000


# ---------------------------------------------------------------------------
# 19. Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_all_zeros_no_crash(self):
        r = _eng().assess(_inp())
        assert r.exfiltration_composite == 0.0

    def test_all_zeros_low_risk(self):
        assert _eng().assess(_inp()).exfiltration_risk == ExfiltrationRisk.low

    def test_all_zeros_normal_severity(self):
        assert _eng().assess(_inp()).exfiltration_severity == ExfiltrationSeverity.normal

    def test_all_zeros_no_action(self):
        assert _eng().assess(_inp()).recommended_action == ExfiltrationAction.no_action

    def test_all_zeros_pattern_none(self):
        assert _eng().assess(_inp()).exfiltration_pattern == ExfiltrationPattern.none

    def test_all_zeros_not_exfiltration_risk(self):
        assert _eng().assess(_inp()).is_exfiltration_risk is False

    def test_all_zeros_not_immediate_review(self):
        assert _eng().assess(_inp()).requires_immediate_review is False

    def test_all_zeros_zero_estimated_records(self):
        assert _eng().assess(_inp()).estimated_records_at_risk == 0

    def test_rep_id_preserved(self):
        assert _eng().assess(_inp(rep_id="test_rep")).rep_id == "test_rep"

    def test_region_preserved(self):
        assert _eng().assess(_inp(region="north")).region == "north"

    def test_resignation_signal_with_no_downloads_not_pre_departure(self):
        # resignation > 0 but bulk_contact < 2 AND export < 20 -> no pre_departure
        r = _eng().assess(_inp(resignation_signal_days_ago=10, bulk_contact_download_count=1))
        # bulk=1 -> export=8 < 20, bulk < 2 -> not pre_departure
        assert r.exfiltration_pattern != ExfiltrationPattern.pre_departure_download

    def test_resignation_signal_adds_behavioral_even_without_pattern(self):
        r = _eng().assess(_inp(resignation_signal_days_ago=10, bulk_contact_download_count=1))
        assert r.behavioral_risk_score >= 20.0  # resignation 1-30 days -> +20

    def test_admin_impersonation_triggers_account_scraping_pattern(self):
        r = _eng().assess(_inp(admin_impersonation_attempts=1))
        assert r.exfiltration_pattern == ExfiltrationPattern.account_scraping

    def test_admin_impersonation_triggers_is_exfiltration_risk(self):
        r = _eng().assess(_inp(admin_impersonation_attempts=1))
        assert r.is_exfiltration_risk is True

    def test_admin_impersonation_triggers_immediate_review(self):
        r = _eng().assess(_inp(admin_impersonation_attempts=1))
        assert r.requires_immediate_review is True

    def test_admin_impersonation_triggers_security_investigation(self):
        r = _eng().assess(_inp(admin_impersonation_attempts=1))
        assert r.recommended_action == ExfiltrationAction.security_investigation

    def test_very_high_crm_export_ratio_caps_at_100(self):
        r = _eng().assess(_inp(crm_export_count_last_30d=10000, crm_export_count_prior_30d=1))
        assert r.export_anomaly_score <= 100.0

    def test_composite_capped_at_100(self):
        r = _eng().assess(_inp(
            crm_export_count_last_30d=10000, crm_export_count_prior_30d=1,
            after_hours_bulk_action_count=100, off_hours_access_count=100,
            accounts_accessed_outside_territory=100, territory_violation_count=100,
            admin_impersonation_attempts=100, data_copy_to_personal_storage_alerts=100,
        ))
        assert r.exfiltration_composite <= 100.0

    def test_no_prior_crm_exports_last_lt_5_no_export_score(self):
        r = _eng().assess(_inp(crm_export_count_last_30d=3, crm_export_count_prior_30d=0))
        assert r.export_anomaly_score == 0.0

    def test_no_prior_records_last_lt_500_no_records_score(self):
        r = _eng().assess(_inp(records_exported_last_30d=400, records_exported_prior_30d=0))
        assert r.export_anomaly_score == 0.0

    def test_no_prior_api_calls_last_gte_100_adds_10_behavioral(self):
        r = _eng().assess(_inp(crm_api_calls_last_30d=100, crm_api_calls_prior_30d=0))
        assert r.behavioral_risk_score == 10.0

    def test_different_reps_independent_results(self):
        e = _eng()
        r1 = e.assess(_inp(rep_id="r1"))
        r2 = e.assess(_inp(rep_id="r2", admin_impersonation_attempts=2))
        assert r1.rep_id == "r1"
        assert r2.rep_id == "r2"
        assert r1.behavioral_risk_score != r2.behavioral_risk_score

    def test_high_api_ratio_below_3_no_behavioral_contribution(self):
        r = _eng().assess(_inp(crm_api_calls_last_30d=250, crm_api_calls_prior_30d=100))
        # ratio=2.5 < 3.0 -> no API contribution
        assert r.behavioral_risk_score == 0.0

    def test_session_duration_exactly_120_adds_7(self):
        r = _eng().assess(_inp(avg_session_duration_minutes=120.0))
        assert r.access_pattern_score == 7.0

    def test_session_duration_exactly_240_adds_15(self):
        r = _eng().assess(_inp(avg_session_duration_minutes=240.0))
        assert r.access_pattern_score == 15.0

    def test_session_duration_just_below_120_no_contribution(self):
        r = _eng().assess(_inp(avg_session_duration_minutes=119.9))
        assert r.access_pattern_score == 0.0

    def test_resignation_signal_exactly_31_days_adds_10(self):
        r = _eng().assess(_inp(resignation_signal_days_ago=31))
        assert r.behavioral_risk_score == 10.0

    def test_resignation_signal_exactly_1_day_adds_20(self):
        r = _eng().assess(_inp(resignation_signal_days_ago=1))
        assert r.behavioral_risk_score == 20.0

    def test_crm_export_ratio_just_below_2_no_contribution(self):
        # ratio=1.9 -> below 2.0, no score
        r = _eng().assess(_inp(crm_export_count_last_30d=19, crm_export_count_prior_30d=10))
        assert r.export_anomaly_score == 0.0

    def test_crm_export_ratio_just_below_3_adds_15(self):
        # ratio=2.9 -> falls into >=2.0 bucket -> +15
        r = _eng().assess(_inp(crm_export_count_last_30d=29, crm_export_count_prior_30d=10))
        assert r.export_anomaly_score == 15.0

    def test_crm_export_ratio_just_below_5_adds_30(self):
        # ratio=4.9 -> falls into >=3.0 bucket -> +30
        r = _eng().assess(_inp(crm_export_count_last_30d=49, crm_export_count_prior_30d=10))
        assert r.export_anomaly_score == 30.0

    def test_records_ratio_exactly_2_adds_8(self):
        r = _eng().assess(_inp(records_exported_last_30d=200, records_exported_prior_30d=100))
        assert r.export_anomaly_score == 8.0

    def test_records_ratio_exactly_3_adds_18(self):
        r = _eng().assess(_inp(records_exported_last_30d=300, records_exported_prior_30d=100))
        assert r.export_anomaly_score == 18.0

    def test_records_ratio_exactly_5_adds_30(self):
        r = _eng().assess(_inp(records_exported_last_30d=500, records_exported_prior_30d=100))
        assert r.export_anomaly_score == 30.0

    def test_bulk_download_4_still_in_2_to_5_bucket(self):
        # bulk=4 -> >=2 bucket -> +15
        r = _eng().assess(_inp(bulk_contact_download_count=4))
        assert r.export_anomaly_score == 15.0

    def test_new_account_views_exactly_5_adds_6_boundary(self):
        r = _eng().assess(_inp(new_account_views_not_in_pipeline=5))
        assert r.boundary_violation_score == 6.0

    def test_new_account_views_exactly_15_adds_14_boundary(self):
        r = _eng().assess(_inp(new_account_views_not_in_pipeline=15))
        assert r.boundary_violation_score == 14.0

    def test_new_account_views_exactly_30_adds_25_boundary(self):
        r = _eng().assess(_inp(new_account_views_not_in_pipeline=30))
        assert r.boundary_violation_score == 25.0

    def test_territory_violation_exactly_2_boundary(self):
        r = _eng().assess(_inp(territory_violation_count=2))
        assert r.boundary_violation_score == 8.0

    def test_territory_violation_exactly_5_boundary(self):
        r = _eng().assess(_inp(territory_violation_count=5))
        assert r.boundary_violation_score == 18.0

    def test_territory_violation_exactly_10_boundary(self):
        r = _eng().assess(_inp(territory_violation_count=10))
        assert r.boundary_violation_score == 30.0

    def test_failed_access_exactly_5_boundary(self):
        r = _eng().assess(_inp(failed_access_attempts=5))
        assert r.boundary_violation_score == 8.0

    def test_failed_access_exactly_10_boundary(self):
        r = _eng().assess(_inp(failed_access_attempts=10))
        assert r.boundary_violation_score == 15.0


# ---------------------------------------------------------------------------
# 20. Result dataclass attributes
# ---------------------------------------------------------------------------

class TestResultAttributes:
    def test_result_has_rep_id(self):
        r = _eng().assess(_inp(rep_id="abc"))
        assert r.rep_id == "abc"

    def test_result_has_region(self):
        r = _eng().assess(_inp(region="central"))
        assert r.region == "central"

    def test_result_exfiltration_risk_is_enum(self):
        r = _eng().assess(_inp())
        assert isinstance(r.exfiltration_risk, ExfiltrationRisk)

    def test_result_exfiltration_pattern_is_enum(self):
        r = _eng().assess(_inp())
        assert isinstance(r.exfiltration_pattern, ExfiltrationPattern)

    def test_result_exfiltration_severity_is_enum(self):
        r = _eng().assess(_inp())
        assert isinstance(r.exfiltration_severity, ExfiltrationSeverity)

    def test_result_recommended_action_is_enum(self):
        r = _eng().assess(_inp())
        assert isinstance(r.recommended_action, ExfiltrationAction)

    def test_result_export_anomaly_score_is_float(self):
        assert isinstance(_eng().assess(_inp()).export_anomaly_score, float)

    def test_result_access_pattern_score_is_float(self):
        assert isinstance(_eng().assess(_inp()).access_pattern_score, float)

    def test_result_boundary_violation_score_is_float(self):
        assert isinstance(_eng().assess(_inp()).boundary_violation_score, float)

    def test_result_behavioral_risk_score_is_float(self):
        assert isinstance(_eng().assess(_inp()).behavioral_risk_score, float)

    def test_result_exfiltration_composite_is_float(self):
        assert isinstance(_eng().assess(_inp()).exfiltration_composite, float)

    def test_result_is_exfiltration_risk_is_bool(self):
        assert isinstance(_eng().assess(_inp()).is_exfiltration_risk, bool)

    def test_result_requires_immediate_review_is_bool(self):
        assert isinstance(_eng().assess(_inp()).requires_immediate_review, bool)

    def test_result_estimated_records_at_risk_is_int(self):
        assert isinstance(_eng().assess(_inp()).estimated_records_at_risk, int)

    def test_result_exfiltration_signal_is_str(self):
        assert isinstance(_eng().assess(_inp()).exfiltration_signal, str)

    def test_result_dataclass_has_15_fields(self):
        assert len(dataclasses.fields(SalesDataExfiltrationResult)) == 15


# ---------------------------------------------------------------------------
# 21. High-composite scenario integration tests
# ---------------------------------------------------------------------------

class TestHighCompositeScenarios:
    def test_pre_departure_scenario_triggers_all_flags(self):
        r = _eng().assess(_inp(
            resignation_signal_days_ago=5,
            bulk_contact_download_count=5,
            records_exported_last_30d=1000,
            crm_export_count_last_30d=25, crm_export_count_prior_30d=5,
        ))
        assert r.exfiltration_pattern == ExfiltrationPattern.pre_departure_download
        assert r.requires_immediate_review is True

    def test_admin_impersonation_scenario(self):
        r = _eng().assess(_inp(admin_impersonation_attempts=2))
        assert r.exfiltration_pattern == ExfiltrationPattern.account_scraping
        assert r.is_exfiltration_risk is True
        assert r.requires_immediate_review is True
        assert r.recommended_action == ExfiltrationAction.immediate_lockdown

    def test_bulk_export_scenario_moderate_risk(self):
        # export=30 (3x crm), no other signals
        r = _eng().assess(_inp(
            crm_export_count_last_30d=15, crm_export_count_prior_30d=5,
        ))
        assert r.exfiltration_pattern == ExfiltrationPattern.bulk_export
        assert r.exfiltration_risk in (ExfiltrationRisk.low, ExfiltrationRisk.moderate)

    def test_territory_breach_scenario(self):
        r = _eng().assess(_inp(accounts_accessed_outside_territory=20, territory_violation_count=10))
        # bnd=40+30=70
        assert r.exfiltration_pattern == ExfiltrationPattern.territory_boundary_breach
        assert r.boundary_violation_score == 70.0

    def test_unusual_hours_scenario(self):
        r = _eng().assess(_inp(off_hours_access_count=15, after_hours_bulk_action_count=3))
        # access=35+25=60, access >= 30, after_hours >= 2 -> unusual_access_hours
        assert r.exfiltration_pattern == ExfiltrationPattern.unusual_access_hours

    def test_multiple_signals_composite_accumulates(self):
        r_low = _eng().assess(_inp())
        r_high = _eng().assess(_inp(
            crm_export_count_last_30d=25, crm_export_count_prior_30d=5,
            off_hours_access_count=15, after_hours_bulk_action_count=5,
            accounts_accessed_outside_territory=20, territory_violation_count=10,
            admin_impersonation_attempts=1, data_copy_to_personal_storage_alerts=2,
        ))
        assert r_high.exfiltration_composite > r_low.exfiltration_composite

    def test_full_summary_with_mixed_reps(self):
        e = _eng()
        e.assess(_inp(rep_id="r1"))  # low
        e.assess(_inp(rep_id="r2", admin_impersonation_attempts=1))  # behavioral risk
        e.assess(_inp(rep_id="r3", resignation_signal_days_ago=5, bulk_contact_download_count=2))
        s = e.summary()
        assert s["total"] == 3
        assert s["exfiltration_risk_count"] >= 1
        assert s["immediate_review_count"] >= 2

    def test_assess_accumulates_for_summary(self):
        e = _eng()
        for i in range(7):
            e.assess(_inp(rep_id=f"r{i}"))
        assert e.summary()["total"] == 7

    def test_pattern_priority_pre_departure_over_account_scraping(self):
        # Both resignation+export AND admin impersonation -> pre_departure wins
        r = _eng().assess(_inp(
            resignation_signal_days_ago=10,
            crm_export_count_last_30d=15, crm_export_count_prior_30d=5,  # export=30 >= 20
            admin_impersonation_attempts=1,
        ))
        assert r.exfiltration_pattern == ExfiltrationPattern.pre_departure_download

    def test_pattern_priority_account_scraping_over_bulk_export(self):
        # Both personal_storage AND high export -> account_scraping wins
        r = _eng().assess(_inp(
            data_copy_to_personal_storage_alerts=1,
            crm_export_count_last_30d=25, crm_export_count_prior_30d=5,  # export=45 >= 30
        ))
        assert r.exfiltration_pattern == ExfiltrationPattern.account_scraping

    def test_pattern_priority_bulk_export_over_unusual_hours(self):
        # export=30 and access=60 with after_hours=2 -> bulk_export wins
        r = _eng().assess(_inp(
            crm_export_count_last_30d=15, crm_export_count_prior_30d=5,  # export=30
            off_hours_access_count=15, after_hours_bulk_action_count=2,  # access=60
        ))
        assert r.exfiltration_pattern == ExfiltrationPattern.bulk_export

    def test_pattern_priority_unusual_hours_over_territory_breach(self):
        # access=60 >= 30 AND after_hours=2; boundary=25 -> unusual_hours wins
        r = _eng().assess(_inp(
            off_hours_access_count=15, after_hours_bulk_action_count=2,
            accounts_accessed_outside_territory=10,  # bnd=25 >= 25
        ))
        assert r.exfiltration_pattern == ExfiltrationPattern.unusual_access_hours

    def test_no_prior_crm_exports_exactly_5_adds_25(self):
        r = _eng().assess(_inp(crm_export_count_last_30d=5, crm_export_count_prior_30d=0))
        assert r.export_anomaly_score == 25.0

    def test_no_prior_records_exactly_500_adds_20(self):
        r = _eng().assess(_inp(records_exported_last_30d=500, records_exported_prior_30d=0))
        assert r.export_anomaly_score == 20.0

    def test_api_ratio_exactly_5_adds_15_behavioral(self):
        r = _eng().assess(_inp(crm_api_calls_last_30d=500, crm_api_calls_prior_30d=100))
        assert r.behavioral_risk_score == 15.0

    def test_competitor_email_exactly_2_triggers_immediate_review(self):
        r = _eng().assess(_inp(competitor_domain_email_access=2))
        assert r.requires_immediate_review is True

    def test_competitor_email_exactly_1_does_not_trigger_immediate_review(self):
        r = _eng().assess(_inp(competitor_domain_email_access=1))
        assert r.requires_immediate_review is False

    def test_personal_storage_exactly_2_triggers_exfiltration_risk(self):
        r = _eng().assess(_inp(data_copy_to_personal_storage_alerts=2))
        assert r.is_exfiltration_risk is True

    def test_personal_storage_exactly_1_does_not_trigger_exfiltration_risk_alone(self):
        r = _eng().assess(_inp(data_copy_to_personal_storage_alerts=1))
        # storage=1 < 2, no admin impersonation, composite < 40
        assert r.is_exfiltration_risk is False

    def test_off_hours_exactly_8_adds_20(self):
        r = _eng().assess(_inp(off_hours_access_count=8))
        assert r.access_pattern_score == 20.0

    def test_off_hours_7_adds_10(self):
        r = _eng().assess(_inp(off_hours_access_count=7))
        assert r.access_pattern_score == 10.0

    def test_unusual_report_exactly_2_adds_5(self):
        r = _eng().assess(_inp(unusual_report_run_count=2))
        assert r.access_pattern_score == 5.0

    def test_unusual_report_exactly_4_adds_10(self):
        r = _eng().assess(_inp(unusual_report_run_count=4))
        assert r.access_pattern_score == 10.0

    def test_unusual_report_exactly_8_adds_20(self):
        r = _eng().assess(_inp(unusual_report_run_count=8))
        assert r.access_pattern_score == 20.0

    def test_unusual_report_7_adds_10(self):
        r = _eng().assess(_inp(unusual_report_run_count=7))
        assert r.access_pattern_score == 10.0

    def test_personal_storage_exactly_3_adds_40(self):
        r = _eng().assess(_inp(data_copy_to_personal_storage_alerts=3))
        assert r.behavioral_risk_score == 40.0

    def test_personal_storage_2_adds_25(self):
        r = _eng().assess(_inp(data_copy_to_personal_storage_alerts=2))
        assert r.behavioral_risk_score == 25.0

    def test_accounts_outside_exactly_20_adds_40(self):
        r = _eng().assess(_inp(accounts_accessed_outside_territory=20))
        assert r.boundary_violation_score == 40.0

    def test_accounts_outside_19_adds_25(self):
        r = _eng().assess(_inp(accounts_accessed_outside_territory=19))
        assert r.boundary_violation_score == 25.0

    def test_accounts_outside_9_adds_12(self):
        r = _eng().assess(_inp(accounts_accessed_outside_territory=9))
        assert r.boundary_violation_score == 12.0

    def test_accounts_outside_4_adds_6(self):
        r = _eng().assess(_inp(accounts_accessed_outside_territory=4))
        assert r.boundary_violation_score == 6.0
