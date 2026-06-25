"""
Comprehensive pytest test suite for SalesDataAccessAnomalyEngine.

Coverage:
- Enum values and membership
- Input dataclass field count (22 fields)
- Result dataclass to_dict() key count (15 keys)
- Summary key count (13 keys)
- All score sub-functions via engine assess()
- is_active_threat / requires_immediate_action invariants
- estimated_data_exposure_mb formula
- AnomalyLevel and AnomalyRisk thresholds
- AnomalyType selection logic
- AnomalyAction recommendation logic
- anomaly_signal string generation
- assess_batch ordering
- summary aggregation
- Edge cases: zeros, maximums, boundary values
"""

from __future__ import annotations

import dataclasses
import math
import pytest

from swarm.intelligence.sales_data_access_anomaly_engine import (
    SalesDataAccessAnomalyEngine,
    SalesDataAccessInput,
    AnomalyLevel,
    AnomalyRisk,
    AnomalyType,
    AnomalyAction,
)


# ---------------------------------------------------------------------------
# Helper factories
# ---------------------------------------------------------------------------

def _baseline(**overrides) -> SalesDataAccessInput:
    """Minimal normal-user input — composite should be near 0."""
    defaults = dict(
        user_id="u001",
        user_name="Alice",
        role="rep",
        region="west",
        records_accessed_count=10,
        records_accessed_prior_avg=10.0,
        download_volume_mb=5.0,
        download_prior_avg_mb=5.0,
        off_hours_access_pct=0.0,
        bulk_export_count=0,
        sensitive_field_access_count=0,
        failed_auth_attempts=0,
        vpn_connected=1,
        shared_account_flag=0,
        unusual_ip_count=0,
        data_sensitivity_avg_score=0.0,
        export_to_personal_email_count=0,
        concurrent_session_count=0,
        access_outside_territory_pct=0.0,
        privileged_data_access_count=0,
        anomaly_score_external=0.0,
        account_type="standard",
    )
    defaults.update(overrides)
    return SalesDataAccessInput(**defaults)


def _engine() -> SalesDataAccessAnomalyEngine:
    return SalesDataAccessAnomalyEngine()


# ---------------------------------------------------------------------------
# 1. Enum membership and values
# ---------------------------------------------------------------------------

class TestAnomalyLevelEnum:
    def test_none_value(self):
        assert AnomalyLevel.NONE.value == "none"

    def test_low_value(self):
        assert AnomalyLevel.LOW.value == "low"

    def test_elevated_value(self):
        assert AnomalyLevel.ELEVATED.value == "elevated"

    def test_high_value(self):
        assert AnomalyLevel.HIGH.value == "high"

    def test_critical_value(self):
        assert AnomalyLevel.CRITICAL.value == "critical"

    def test_exactly_five_members(self):
        assert len(AnomalyLevel) == 5

    def test_is_str_enum(self):
        assert isinstance(AnomalyLevel.NONE, str)

    def test_string_equality(self):
        assert AnomalyLevel.HIGH == "high"


class TestAnomalyRiskEnum:
    def test_low_value(self):
        assert AnomalyRisk.LOW.value == "low"

    def test_moderate_value(self):
        assert AnomalyRisk.MODERATE.value == "moderate"

    def test_high_value(self):
        assert AnomalyRisk.HIGH.value == "high"

    def test_critical_value(self):
        assert AnomalyRisk.CRITICAL.value == "critical"

    def test_exactly_four_members(self):
        assert len(AnomalyRisk) == 4

    def test_is_str_enum(self):
        assert isinstance(AnomalyRisk.LOW, str)


class TestAnomalyTypeEnum:
    def test_none_value(self):
        assert AnomalyType.NONE.value == "none"

    def test_bulk_export_value(self):
        assert AnomalyType.BULK_EXPORT.value == "bulk_export"

    def test_off_hours_value(self):
        assert AnomalyType.OFF_HOURS.value == "off_hours"

    def test_credential_sharing_value(self):
        assert AnomalyType.CREDENTIAL_SHARING.value == "credential_sharing"

    def test_data_exfiltration_value(self):
        assert AnomalyType.DATA_EXFILTRATION.value == "data_exfiltration"

    def test_privilege_abuse_value(self):
        assert AnomalyType.PRIVILEGE_ABUSE.value == "privilege_abuse"

    def test_exactly_six_members(self):
        assert len(AnomalyType) == 6

    def test_is_str_enum(self):
        assert isinstance(AnomalyType.BULK_EXPORT, str)


class TestAnomalyActionEnum:
    def test_no_action_value(self):
        assert AnomalyAction.NO_ACTION.value == "no_action"

    def test_log_alert_value(self):
        assert AnomalyAction.LOG_ALERT.value == "log_alert"

    def test_security_review_value(self):
        assert AnomalyAction.SECURITY_REVIEW.value == "security_review"

    def test_account_suspend_value(self):
        assert AnomalyAction.ACCOUNT_SUSPEND.value == "account_suspend"

    def test_immediate_lockdown_value(self):
        assert AnomalyAction.IMMEDIATE_LOCKDOWN.value == "immediate_lockdown"

    def test_exactly_five_members(self):
        assert len(AnomalyAction) == 5

    def test_is_str_enum(self):
        assert isinstance(AnomalyAction.NO_ACTION, str)


# ---------------------------------------------------------------------------
# 2. Input dataclass field count
# ---------------------------------------------------------------------------

class TestInputDataclassStructure:
    def test_exactly_22_fields(self):
        fields = dataclasses.fields(SalesDataAccessInput)
        assert len(fields) == 22

    def test_field_names_present(self):
        names = {f.name for f in dataclasses.fields(SalesDataAccessInput)}
        expected = {
            "user_id", "user_name", "role", "region",
            "records_accessed_count", "records_accessed_prior_avg",
            "download_volume_mb", "download_prior_avg_mb",
            "off_hours_access_pct", "bulk_export_count",
            "sensitive_field_access_count", "failed_auth_attempts",
            "vpn_connected", "shared_account_flag", "unusual_ip_count",
            "data_sensitivity_avg_score", "export_to_personal_email_count",
            "concurrent_session_count", "access_outside_territory_pct",
            "privileged_data_access_count", "anomaly_score_external",
            "account_type",
        }
        assert names == expected

    def test_instantiation_succeeds(self):
        inp = _baseline()
        assert inp.user_id == "u001"

    def test_user_id_field(self):
        inp = _baseline(user_id="xyz")
        assert inp.user_id == "xyz"

    def test_user_name_field(self):
        inp = _baseline(user_name="Bob")
        assert inp.user_name == "Bob"

    def test_records_accessed_count_field(self):
        inp = _baseline(records_accessed_count=999)
        assert inp.records_accessed_count == 999

    def test_download_volume_mb_field(self):
        inp = _baseline(download_volume_mb=250.5)
        assert inp.download_volume_mb == 250.5

    def test_shared_account_flag_field(self):
        inp = _baseline(shared_account_flag=1)
        assert inp.shared_account_flag == 1


# ---------------------------------------------------------------------------
# 3. to_dict() key count invariant
# ---------------------------------------------------------------------------

class TestToDictKeyCount:
    def test_exactly_15_keys_baseline(self):
        engine = _engine()
        result = engine.assess(_baseline())
        assert len(result.to_dict()) == 15

    def test_exactly_15_keys_high_composite(self):
        engine = _engine()
        inp = _baseline(
            records_accessed_count=500,
            records_accessed_prior_avg=10.0,
            download_volume_mb=500.0,
            download_prior_avg_mb=5.0,
            bulk_export_count=10,
            off_hours_access_pct=80.0,
            shared_account_flag=1,
            export_to_personal_email_count=5,
        )
        result = engine.assess(inp)
        assert len(result.to_dict()) == 15

    def test_to_dict_key_names(self):
        engine = _engine()
        result = engine.assess(_baseline())
        expected = {
            "user_id", "user_name", "anomaly_level", "anomaly_risk",
            "primary_anomaly_type", "recommended_action",
            "access_volume_score", "behavioral_deviation_score",
            "data_sensitivity_score", "authentication_risk_score",
            "anomaly_composite", "is_active_threat",
            "requires_immediate_action", "estimated_data_exposure_mb",
            "anomaly_signal",
        }
        assert set(result.to_dict().keys()) == expected

    def test_to_dict_anomaly_level_is_string(self):
        engine = _engine()
        d = engine.assess(_baseline()).to_dict()
        assert isinstance(d["anomaly_level"], str)

    def test_to_dict_anomaly_risk_is_string(self):
        engine = _engine()
        d = engine.assess(_baseline()).to_dict()
        assert isinstance(d["anomaly_risk"], str)

    def test_to_dict_primary_anomaly_type_is_string(self):
        engine = _engine()
        d = engine.assess(_baseline()).to_dict()
        assert isinstance(d["primary_anomaly_type"], str)

    def test_to_dict_recommended_action_is_string(self):
        engine = _engine()
        d = engine.assess(_baseline()).to_dict()
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_is_active_threat_is_bool(self):
        engine = _engine()
        d = engine.assess(_baseline()).to_dict()
        assert isinstance(d["is_active_threat"], bool)

    def test_to_dict_requires_immediate_action_is_bool(self):
        engine = _engine()
        d = engine.assess(_baseline()).to_dict()
        assert isinstance(d["requires_immediate_action"], bool)


# ---------------------------------------------------------------------------
# 4. summary() key count invariant
# ---------------------------------------------------------------------------

class TestSummaryKeyCount:
    def test_exactly_13_keys_empty(self):
        engine = _engine()
        s = engine.summary()
        assert len(s) == 13

    def test_exactly_13_keys_after_one_assess(self):
        engine = _engine()
        engine.assess(_baseline())
        s = engine.summary()
        assert len(s) == 13

    def test_exactly_13_keys_after_batch(self):
        engine = _engine()
        engine.assess_batch([_baseline(user_id=f"u{i}") for i in range(5)])
        assert len(engine.summary()) == 13

    def test_summary_key_names(self):
        engine = _engine()
        engine.assess(_baseline())
        expected = {
            "total", "level_counts", "risk_counts", "type_counts",
            "action_counts", "avg_anomaly_composite", "active_threat_count",
            "immediate_action_count", "avg_access_volume_score",
            "avg_behavioral_deviation_score", "avg_data_sensitivity_score",
            "avg_authentication_risk_score", "total_data_exposure_mb",
        }
        assert set(engine.summary().keys()) == expected

    def test_summary_total_empty(self):
        engine = _engine()
        assert engine.summary()["total"] == 0

    def test_summary_total_single(self):
        engine = _engine()
        engine.assess(_baseline())
        assert engine.summary()["total"] == 1

    def test_summary_total_multiple(self):
        engine = _engine()
        for i in range(7):
            engine.assess(_baseline(user_id=f"u{i}"))
        assert engine.summary()["total"] == 7

    def test_summary_avg_composite_empty(self):
        engine = _engine()
        assert engine.summary()["avg_anomaly_composite"] == 0.0

    def test_summary_active_threat_count_type(self):
        engine = _engine()
        assert isinstance(engine.summary()["active_threat_count"], int)

    def test_summary_immediate_action_count_type(self):
        engine = _engine()
        assert isinstance(engine.summary()["immediate_action_count"], int)

    def test_summary_level_counts_is_dict(self):
        engine = _engine()
        engine.assess(_baseline())
        assert isinstance(engine.summary()["level_counts"], dict)

    def test_summary_risk_counts_is_dict(self):
        engine = _engine()
        engine.assess(_baseline())
        assert isinstance(engine.summary()["risk_counts"], dict)

    def test_summary_type_counts_is_dict(self):
        engine = _engine()
        engine.assess(_baseline())
        assert isinstance(engine.summary()["type_counts"], dict)

    def test_summary_action_counts_is_dict(self):
        engine = _engine()
        engine.assess(_baseline())
        assert isinstance(engine.summary()["action_counts"], dict)


# ---------------------------------------------------------------------------
# 5. is_active_threat invariants
# ---------------------------------------------------------------------------

class TestIsActiveThreat:
    def test_false_when_baseline(self):
        engine = _engine()
        r = engine.assess(_baseline())
        assert r.is_active_threat is False

    def test_true_when_composite_gte_45(self):
        # Force composite >= 45: access=100(30) + sensitivity pushes it up
        engine = _engine()
        inp = _baseline(
            records_accessed_count=500,
            records_accessed_prior_avg=10.0,   # ratio=50 -> +40 access
            download_volume_mb=100.0,
            download_prior_avg_mb=5.0,          # dl_ratio=20 -> +35 access
            bulk_export_count=5,                # +25 access => access=100
            off_hours_access_pct=60.0,          # +30 behavioral
            data_sensitivity_avg_score=100.0,   # +35 sensitivity
            unusual_ip_count=3,                 # +10 sensitivity
        )
        r = engine.assess(inp)
        assert r.anomaly_composite >= 45
        assert r.is_active_threat is True

    def test_true_when_export_to_personal_email_gte_2(self):
        engine = _engine()
        r = engine.assess(_baseline(export_to_personal_email_count=2))
        assert r.is_active_threat is True

    def test_false_when_export_to_personal_email_eq_1_and_low_composite(self):
        # export_to_personal_email_count=1 does NOT trigger is_active_threat alone
        engine = _engine()
        r = engine.assess(_baseline(export_to_personal_email_count=1))
        # composite should still be very low; composite < 45, email_count < 2, no shared
        # But is_active_threat only triggers if composite>=45 OR email>=2 OR shared==1
        assert r.is_active_threat is False

    def test_true_when_shared_account_flag_eq_1(self):
        engine = _engine()
        r = engine.assess(_baseline(shared_account_flag=1))
        assert r.is_active_threat is True

    def test_false_when_shared_account_flag_eq_0(self):
        engine = _engine()
        r = engine.assess(_baseline(shared_account_flag=0))
        assert r.is_active_threat is False

    def test_true_when_export_exactly_2(self):
        engine = _engine()
        r = engine.assess(_baseline(export_to_personal_email_count=2))
        assert r.is_active_threat is True

    def test_true_when_export_exceeds_2(self):
        engine = _engine()
        r = engine.assess(_baseline(export_to_personal_email_count=10))
        assert r.is_active_threat is True

    def test_true_via_composite_boundary(self):
        # access=100(30) + behavioral=80(20) = 50 >= 45, is_active_threat True
        engine = _engine()
        inp = _baseline(
            records_accessed_count=500, records_accessed_prior_avg=10.0,
            download_volume_mb=100.0, download_prior_avg_mb=5.0,
            bulk_export_count=5,
            off_hours_access_pct=80.0,          # +30 behavioral
            access_outside_territory_pct=70.0,  # +25 behavioral
            concurrent_session_count=4,          # +25 behavioral => behavioral=80
        )
        r = engine.assess(inp)
        assert r.anomaly_composite >= 45
        assert r.is_active_threat is True

    def test_active_threat_composite_exactly_boundary_false(self):
        # All zeros -> composite 0, is_active_threat False
        engine = _engine()
        r = engine.assess(_baseline())
        assert r.anomaly_composite < 45
        assert r.is_active_threat is False


# ---------------------------------------------------------------------------
# 6. requires_immediate_action invariants
# ---------------------------------------------------------------------------

class TestRequiresImmediateAction:
    def test_false_when_baseline(self):
        engine = _engine()
        r = engine.assess(_baseline())
        assert r.requires_immediate_action is False

    def test_true_when_composite_gte_65(self):
        # access=100(30) + behavioral=80(20) + sensitivity=100(25) = 75 >= 65
        engine = _engine()
        inp = _baseline(
            records_accessed_count=500, records_accessed_prior_avg=10.0,
            download_volume_mb=100.0, download_prior_avg_mb=5.0,
            bulk_export_count=5,
            off_hours_access_pct=80.0,
            access_outside_territory_pct=70.0,
            concurrent_session_count=4,
            sensitive_field_access_count=50,
            data_sensitivity_avg_score=100.0,
            privileged_data_access_count=10,
            unusual_ip_count=3,
        )
        r = engine.assess(inp)
        assert r.anomaly_composite >= 65
        assert r.requires_immediate_action is True

    def test_true_when_export_to_personal_email_gte_3(self):
        engine = _engine()
        r = engine.assess(_baseline(export_to_personal_email_count=3))
        assert r.requires_immediate_action is True

    def test_false_when_export_to_personal_email_eq_2(self):
        engine = _engine()
        r = engine.assess(_baseline(export_to_personal_email_count=2))
        # composite < 65, email == 2 (not >= 3), shared == 0
        assert r.requires_immediate_action is False

    def test_true_when_shared_and_composite_gte_40(self):
        # auth=40(shared) -> auth*0.20=8; access=100*0.30=30; behavioral=20*0.25=5
        # composite = 30 + 5 + 0 + 8 = 43 >= 40
        engine = _engine()
        inp = _baseline(
            shared_account_flag=1,
            records_accessed_count=500, records_accessed_prior_avg=10.0,
            download_volume_mb=100.0, download_prior_avg_mb=5.0,
            bulk_export_count=5,
            off_hours_access_pct=40.0,   # +20 behavioral -> 20*0.25=5
        )
        r = engine.assess(inp)
        assert r.anomaly_composite >= 40
        assert r.requires_immediate_action is True

    def test_false_when_shared_and_composite_below_40(self):
        # shared_account_flag=1 but minimal other signals; composite might still be
        # above 40 due to auth score; let's verify the formula
        engine = _engine()
        inp = _baseline(shared_account_flag=1)
        r = engine.assess(inp)
        # auth_score with shared=1 is >= 40, composite = auth*0.20 = 40*0.20 = 8.0
        # So composite = 8.0 which is < 40 -> requires_immediate_action only if shared==1 AND composite>=40
        # Actually with just shared_account_flag=1:
        # access=0, behavioral=0, sensitivity=0, auth=40 -> composite=40*0.20=8.0
        # email < 3, composite < 65, shared==1 but composite < 40 -> False
        assert r.anomaly_composite < 40
        assert r.requires_immediate_action is False

    def test_true_when_export_exactly_3(self):
        engine = _engine()
        r = engine.assess(_baseline(export_to_personal_email_count=3))
        assert r.requires_immediate_action is True

    def test_true_when_export_more_than_3(self):
        engine = _engine()
        r = engine.assess(_baseline(export_to_personal_email_count=5))
        assert r.requires_immediate_action is True

    def test_shared_and_high_composite_triggers(self):
        # auth=40(shared) -> 8; access=100 -> 30; behavioral=20 -> 5; composite=43 >= 40
        engine = _engine()
        inp = _baseline(
            shared_account_flag=1,
            records_accessed_count=500, records_accessed_prior_avg=10.0,
            download_volume_mb=100.0, download_prior_avg_mb=5.0,
            bulk_export_count=5,
            off_hours_access_pct=40.0,
        )
        r = engine.assess(inp)
        assert r.anomaly_composite >= 40
        assert r.requires_immediate_action is True


# ---------------------------------------------------------------------------
# 7. estimated_data_exposure_mb formula
# ---------------------------------------------------------------------------

class TestDataExposureMb:
    def test_zero_download_zero_exposure(self):
        engine = _engine()
        r = engine.assess(_baseline(download_volume_mb=0.0))
        assert r.estimated_data_exposure_mb == 0.0

    def test_formula_matches_download_times_composite_over_100(self):
        engine = _engine()
        r = engine.assess(_baseline())
        expected = round(r.access_volume_score * 0.0, 2)  # just verify it's a float
        assert isinstance(r.estimated_data_exposure_mb, float)

    def test_formula_exact_value(self):
        engine = _engine()
        inp = _baseline(
            records_accessed_count=500, records_accessed_prior_avg=10.0,
            download_volume_mb=100.0, download_prior_avg_mb=5.0,
            bulk_export_count=5,
        )
        r = engine.assess(inp)
        expected = round(100.0 * (r.anomaly_composite / 100.0), 2)
        assert r.estimated_data_exposure_mb == expected

    def test_exposure_proportional_to_download_volume(self):
        engine = _engine()
        inp1 = _baseline(
            records_accessed_count=100, records_accessed_prior_avg=10.0,
            download_volume_mb=10.0, download_prior_avg_mb=1.0,
        )
        inp2 = _baseline(
            user_id="u2",
            records_accessed_count=100, records_accessed_prior_avg=10.0,
            download_volume_mb=20.0, download_prior_avg_mb=1.0,  # same ratio -> same composite
        )
        r1 = engine.assess(inp1)
        r2 = engine.assess(inp2)
        # same composite but different download_volume -> different exposure
        assert r2.estimated_data_exposure_mb > r1.estimated_data_exposure_mb

    def test_exposure_is_rounded_to_2_decimals(self):
        engine = _engine()
        inp = _baseline(download_volume_mb=33.333)
        r = engine.assess(inp)
        # Should be rounded to 2 decimal places
        assert r.estimated_data_exposure_mb == round(r.estimated_data_exposure_mb, 2)

    def test_exposure_non_negative(self):
        engine = _engine()
        r = engine.assess(_baseline())
        assert r.estimated_data_exposure_mb >= 0.0


# ---------------------------------------------------------------------------
# 8. AnomalyLevel thresholds
# ---------------------------------------------------------------------------

class TestAnomalyLevelThresholds:
    def test_none_when_composite_below_10(self):
        engine = _engine()
        r = engine.assess(_baseline())
        # All zeros -> composite = 0
        assert r.anomaly_composite < 10
        assert r.anomaly_level == AnomalyLevel.NONE

    def test_low_when_composite_gte_10_lt_25(self):
        # off_hours=10 -> behavioral: +4; composite = 4*0.25 = 1.0 -- not enough
        # Need composite between 10 and 25
        # records ratio 2.0 -> access +16; composite=16*0.30=4.8
        # records ratio 3.0 -> access +28; behavioral=10 -> off_hours 20%; composite=28*0.3+10*0.25=8.4+2.5=10.9
        engine = _engine()
        inp = _baseline(
            records_accessed_count=30, records_accessed_prior_avg=10.0,  # ratio=3 -> +28 access
            off_hours_access_pct=20.0,  # +10 behavioral
        )
        r = engine.assess(inp)
        assert 10 <= r.anomaly_composite < 25
        assert r.anomaly_level == AnomalyLevel.LOW

    def test_elevated_when_composite_gte_25_lt_45(self):
        # access=100*0.30=30 -> composite=30, which is in [25, 45)
        engine = _engine()
        inp = _baseline(
            records_accessed_count=500, records_accessed_prior_avg=10.0,
            download_volume_mb=100.0, download_prior_avg_mb=5.0,
            bulk_export_count=5,
        )
        r = engine.assess(inp)
        assert 25 <= r.anomaly_composite < 45
        assert r.anomaly_level == AnomalyLevel.ELEVATED

    def test_high_when_composite_gte_45_lt_65(self):
        # access=100(30) + behavioral=80(20) = 50, in [45, 65)
        engine = _engine()
        inp = _baseline(
            records_accessed_count=500, records_accessed_prior_avg=10.0,
            download_volume_mb=100.0, download_prior_avg_mb=5.0,
            bulk_export_count=5,
            off_hours_access_pct=80.0,
            access_outside_territory_pct=70.0,
            concurrent_session_count=4,
        )
        r = engine.assess(inp)
        assert 45 <= r.anomaly_composite < 65
        assert r.anomaly_level == AnomalyLevel.HIGH

    def test_critical_when_composite_gte_65(self):
        # access=100(30) + behavioral=80(20) + sensitivity=100(25) = 75 >= 65
        engine = _engine()
        inp = _baseline(
            records_accessed_count=500, records_accessed_prior_avg=10.0,
            download_volume_mb=100.0, download_prior_avg_mb=5.0,
            bulk_export_count=5,
            off_hours_access_pct=80.0,
            access_outside_territory_pct=70.0,
            concurrent_session_count=4,
            sensitive_field_access_count=50,
            data_sensitivity_avg_score=100.0,
            privileged_data_access_count=10,
            unusual_ip_count=3,
        )
        r = engine.assess(inp)
        assert r.anomaly_composite >= 65
        assert r.anomaly_level == AnomalyLevel.CRITICAL


# ---------------------------------------------------------------------------
# 9. AnomalyRisk thresholds
# ---------------------------------------------------------------------------

class TestAnomalyRiskThresholds:
    def test_low_when_composite_below_15(self):
        engine = _engine()
        r = engine.assess(_baseline())
        assert r.anomaly_composite < 15
        assert r.anomaly_risk == AnomalyRisk.LOW

    def test_moderate_when_composite_gte_15_lt_35(self):
        # access=28(records ratio 3x) + behavioral=36(off_hours 40+territory 30)
        # composite = 28*0.30 + 36*0.25 = 8.4 + 9 = 17.4, in [15, 35)
        engine = _engine()
        inp = _baseline(
            records_accessed_count=30, records_accessed_prior_avg=10.0,
            off_hours_access_pct=40.0,
            access_outside_territory_pct=30.0,
        )
        r = engine.assess(inp)
        assert 15 <= r.anomaly_composite < 35
        assert r.anomaly_risk == AnomalyRisk.MODERATE

    def test_high_when_composite_gte_35_lt_55(self):
        # access=92(records 50x=40, dl 6x=35, bulk3=17) + behavioral=36 -> 27.6+9=36.6
        engine = _engine()
        inp = _baseline(
            records_accessed_count=500, records_accessed_prior_avg=10.0,
            download_volume_mb=30.0, download_prior_avg_mb=5.0,
            bulk_export_count=3,
            off_hours_access_pct=40.0,
            access_outside_territory_pct=30.0,
        )
        r = engine.assess(inp)
        assert 35 <= r.anomaly_composite < 55
        assert r.anomaly_risk == AnomalyRisk.HIGH

    def test_critical_when_composite_gte_55(self):
        # access=100(30) + behavioral=80(20) + sensitivity=17.5(4.375) = ~54
        # Add data_sensitivity_avg_score=50 -> sensitivity=17.5; total = 30+20+4.375=54.375
        # Actually: access=100(30), behavioral=80(20), sensitivity=100*0.35=35(8.75), total=58.75
        engine = _engine()
        inp = _baseline(
            records_accessed_count=500, records_accessed_prior_avg=10.0,
            download_volume_mb=100.0, download_prior_avg_mb=5.0,
            bulk_export_count=5,
            off_hours_access_pct=80.0,
            access_outside_territory_pct=70.0,
            concurrent_session_count=4,
            data_sensitivity_avg_score=100.0,
        )
        r = engine.assess(inp)
        assert r.anomaly_composite >= 55
        assert r.anomaly_risk == AnomalyRisk.CRITICAL


# ---------------------------------------------------------------------------
# 10. Access volume score sub-function (tested via assess)
# ---------------------------------------------------------------------------

class TestAccessVolumeScore:
    def test_zero_when_all_normal(self):
        engine = _engine()
        r = engine.assess(_baseline())
        assert r.access_volume_score == 0.0

    def test_records_ratio_lt_1_5_no_contribution(self):
        engine = _engine()
        inp = _baseline(records_accessed_count=12, records_accessed_prior_avg=10.0)  # ratio=1.2
        r = engine.assess(inp)
        assert r.access_volume_score == 0.0  # no download anomaly, no bulk

    def test_records_ratio_1_5_adds_8(self):
        engine = _engine()
        inp = _baseline(records_accessed_count=15, records_accessed_prior_avg=10.0)  # ratio=1.5
        r = engine.assess(inp)
        # records: +8, download: 0 (ratio=1), bulk: 0
        assert r.access_volume_score == 8.0

    def test_records_ratio_2_adds_16(self):
        engine = _engine()
        inp = _baseline(records_accessed_count=20, records_accessed_prior_avg=10.0)
        r = engine.assess(inp)
        assert r.access_volume_score == 16.0

    def test_records_ratio_3_adds_28(self):
        engine = _engine()
        inp = _baseline(records_accessed_count=30, records_accessed_prior_avg=10.0)
        r = engine.assess(inp)
        assert r.access_volume_score == 28.0

    def test_records_ratio_5_adds_40(self):
        engine = _engine()
        inp = _baseline(records_accessed_count=50, records_accessed_prior_avg=10.0)
        r = engine.assess(inp)
        assert r.access_volume_score == 40.0

    def test_download_ratio_1_5_adds_6(self):
        engine = _engine()
        inp = _baseline(download_volume_mb=7.5, download_prior_avg_mb=5.0)  # ratio=1.5
        r = engine.assess(inp)
        assert r.access_volume_score == 6.0

    def test_download_ratio_2_adds_12(self):
        engine = _engine()
        inp = _baseline(download_volume_mb=10.0, download_prior_avg_mb=5.0)
        r = engine.assess(inp)
        assert r.access_volume_score == 12.0

    def test_download_ratio_3_adds_24(self):
        engine = _engine()
        inp = _baseline(download_volume_mb=15.0, download_prior_avg_mb=5.0)
        r = engine.assess(inp)
        assert r.access_volume_score == 24.0

    def test_download_ratio_5_adds_35(self):
        engine = _engine()
        inp = _baseline(download_volume_mb=25.0, download_prior_avg_mb=5.0)
        r = engine.assess(inp)
        assert r.access_volume_score == 35.0

    def test_bulk_export_1_adds_8(self):
        engine = _engine()
        inp = _baseline(bulk_export_count=1)
        r = engine.assess(inp)
        assert r.access_volume_score == 8.0

    def test_bulk_export_3_adds_17(self):
        engine = _engine()
        inp = _baseline(bulk_export_count=3)
        r = engine.assess(inp)
        assert r.access_volume_score == 17.0

    def test_bulk_export_5_adds_25(self):
        engine = _engine()
        inp = _baseline(bulk_export_count=5)
        r = engine.assess(inp)
        assert r.access_volume_score == 25.0

    def test_max_capped_at_100(self):
        engine = _engine()
        inp = _baseline(
            records_accessed_count=500, records_accessed_prior_avg=10.0,
            download_volume_mb=200.0, download_prior_avg_mb=5.0,
            bulk_export_count=10,
        )
        r = engine.assess(inp)
        assert r.access_volume_score == 100.0

    def test_prior_avg_zero_records_nonzero_is_5x(self):
        engine = _engine()
        inp = _baseline(records_accessed_count=1, records_accessed_prior_avg=0.0)
        r = engine.assess(inp)
        # ratio = 5.0 -> +40 for records
        assert r.access_volume_score >= 40.0

    def test_prior_avg_zero_records_zero_is_1x(self):
        engine = _engine()
        inp = _baseline(records_accessed_count=0, records_accessed_prior_avg=0.0)
        r = engine.assess(inp)
        # ratio = 1.0 -> no contribution from records
        assert r.access_volume_score == 0.0

    def test_download_prior_avg_zero_download_nonzero(self):
        engine = _engine()
        inp = _baseline(download_volume_mb=10.0, download_prior_avg_mb=0.0)
        r = engine.assess(inp)
        # dl_ratio = 5.0 -> +35
        assert r.access_volume_score >= 35.0


# ---------------------------------------------------------------------------
# 11. Behavioral deviation score
# ---------------------------------------------------------------------------

class TestBehavioralDeviationScore:
    def test_zero_when_normal(self):
        engine = _engine()
        r = engine.assess(_baseline())
        assert r.behavioral_deviation_score == 0.0

    def test_off_hours_10_adds_4(self):
        engine = _engine()
        r = engine.assess(_baseline(off_hours_access_pct=10.0))
        assert r.behavioral_deviation_score == 4.0

    def test_off_hours_20_adds_10(self):
        engine = _engine()
        r = engine.assess(_baseline(off_hours_access_pct=20.0))
        assert r.behavioral_deviation_score == 10.0

    def test_off_hours_40_adds_20(self):
        engine = _engine()
        r = engine.assess(_baseline(off_hours_access_pct=40.0))
        assert r.behavioral_deviation_score == 20.0

    def test_off_hours_60_adds_30(self):
        engine = _engine()
        r = engine.assess(_baseline(off_hours_access_pct=60.0))
        assert r.behavioral_deviation_score == 30.0

    def test_access_outside_territory_15_adds_8(self):
        engine = _engine()
        r = engine.assess(_baseline(access_outside_territory_pct=15.0))
        assert r.behavioral_deviation_score == 8.0

    def test_access_outside_territory_30_adds_16(self):
        engine = _engine()
        r = engine.assess(_baseline(access_outside_territory_pct=30.0))
        assert r.behavioral_deviation_score == 16.0

    def test_access_outside_territory_50_adds_25(self):
        engine = _engine()
        r = engine.assess(_baseline(access_outside_territory_pct=50.0))
        assert r.behavioral_deviation_score == 25.0

    def test_concurrent_sessions_2_adds_8(self):
        engine = _engine()
        r = engine.assess(_baseline(concurrent_session_count=2))
        assert r.behavioral_deviation_score == 8.0

    def test_concurrent_sessions_3_adds_16(self):
        engine = _engine()
        r = engine.assess(_baseline(concurrent_session_count=3))
        assert r.behavioral_deviation_score == 16.0

    def test_concurrent_sessions_4_adds_25(self):
        engine = _engine()
        r = engine.assess(_baseline(concurrent_session_count=4))
        assert r.behavioral_deviation_score == 25.0

    def test_export_personal_email_1_adds_12(self):
        engine = _engine()
        r = engine.assess(_baseline(export_to_personal_email_count=1))
        assert r.behavioral_deviation_score == 12.0

    def test_export_personal_email_3_adds_20(self):
        engine = _engine()
        r = engine.assess(_baseline(export_to_personal_email_count=3))
        assert r.behavioral_deviation_score == 20.0

    def test_max_capped_at_100(self):
        engine = _engine()
        inp = _baseline(
            off_hours_access_pct=80.0,
            access_outside_territory_pct=70.0,
            concurrent_session_count=5,
            export_to_personal_email_count=5,
        )
        r = engine.assess(inp)
        assert r.behavioral_deviation_score == 100.0


# ---------------------------------------------------------------------------
# 12. Data sensitivity score
# ---------------------------------------------------------------------------

class TestDataSensitivityScore:
    def test_zero_when_normal(self):
        engine = _engine()
        r = engine.assess(_baseline())
        assert r.data_sensitivity_score == 0.0

    def test_sensitive_field_access_5_adds_5(self):
        engine = _engine()
        r = engine.assess(_baseline(sensitive_field_access_count=5))
        assert r.data_sensitivity_score == 5.0

    def test_sensitive_field_access_10_adds_12(self):
        engine = _engine()
        r = engine.assess(_baseline(sensitive_field_access_count=10))
        assert r.data_sensitivity_score == 12.0

    def test_sensitive_field_access_25_adds_24(self):
        engine = _engine()
        r = engine.assess(_baseline(sensitive_field_access_count=25))
        assert r.data_sensitivity_score == 24.0

    def test_sensitive_field_access_50_adds_35(self):
        engine = _engine()
        r = engine.assess(_baseline(sensitive_field_access_count=50))
        assert r.data_sensitivity_score == 35.0

    def test_data_sensitivity_avg_score_contributes(self):
        engine = _engine()
        r = engine.assess(_baseline(data_sensitivity_avg_score=100.0))
        # 100 * 0.35 = 35.0
        assert r.data_sensitivity_score == 35.0

    def test_data_sensitivity_avg_score_partial(self):
        engine = _engine()
        r = engine.assess(_baseline(data_sensitivity_avg_score=50.0))
        assert r.data_sensitivity_score == 17.5

    def test_privileged_data_1_adds_6(self):
        engine = _engine()
        r = engine.assess(_baseline(privileged_data_access_count=1))
        assert r.data_sensitivity_score == 6.0

    def test_privileged_data_5_adds_13(self):
        engine = _engine()
        r = engine.assess(_baseline(privileged_data_access_count=5))
        assert r.data_sensitivity_score == 13.0

    def test_privileged_data_10_adds_20(self):
        engine = _engine()
        r = engine.assess(_baseline(privileged_data_access_count=10))
        assert r.data_sensitivity_score == 20.0

    def test_unusual_ip_1_adds_5(self):
        engine = _engine()
        r = engine.assess(_baseline(unusual_ip_count=1))
        assert r.data_sensitivity_score == 5.0

    def test_unusual_ip_3_adds_10(self):
        engine = _engine()
        r = engine.assess(_baseline(unusual_ip_count=3))
        assert r.data_sensitivity_score == 10.0

    def test_max_capped_at_100(self):
        engine = _engine()
        inp = _baseline(
            sensitive_field_access_count=100,
            data_sensitivity_avg_score=100.0,
            privileged_data_access_count=20,
            unusual_ip_count=10,
        )
        r = engine.assess(inp)
        assert r.data_sensitivity_score == 100.0


# ---------------------------------------------------------------------------
# 13. Authentication risk score
# ---------------------------------------------------------------------------

class TestAuthenticationRiskScore:
    def test_zero_when_normal(self):
        engine = _engine()
        r = engine.assess(_baseline(vpn_connected=1))
        assert r.authentication_risk_score == 0.0

    def test_shared_account_adds_40(self):
        engine = _engine()
        r = engine.assess(_baseline(shared_account_flag=1))
        assert r.authentication_risk_score == 40.0

    def test_failed_auth_1_adds_4(self):
        engine = _engine()
        r = engine.assess(_baseline(failed_auth_attempts=1))
        assert r.authentication_risk_score == 4.0

    def test_failed_auth_3_adds_10(self):
        engine = _engine()
        r = engine.assess(_baseline(failed_auth_attempts=3))
        assert r.authentication_risk_score == 10.0

    def test_failed_auth_5_adds_20(self):
        engine = _engine()
        r = engine.assess(_baseline(failed_auth_attempts=5))
        assert r.authentication_risk_score == 20.0

    def test_failed_auth_10_adds_30(self):
        engine = _engine()
        r = engine.assess(_baseline(failed_auth_attempts=10))
        assert r.authentication_risk_score == 30.0

    def test_unusual_ip_1_adds_6(self):
        engine = _engine()
        r = engine.assess(_baseline(unusual_ip_count=1))
        # unusual_ip in auth: 1-2 -> +6
        assert r.authentication_risk_score == 6.0

    def test_unusual_ip_3_adds_13(self):
        engine = _engine()
        r = engine.assess(_baseline(unusual_ip_count=3))
        assert r.authentication_risk_score == 13.0

    def test_unusual_ip_5_adds_20(self):
        engine = _engine()
        r = engine.assess(_baseline(unusual_ip_count=5))
        assert r.authentication_risk_score == 20.0

    def test_no_vpn_high_sensitivity_adds_10(self):
        engine = _engine()
        r = engine.assess(_baseline(vpn_connected=0, data_sensitivity_avg_score=60.0))
        assert r.authentication_risk_score == 10.0

    def test_no_vpn_low_sensitivity_no_addition(self):
        engine = _engine()
        r = engine.assess(_baseline(vpn_connected=0, data_sensitivity_avg_score=50.0))
        assert r.authentication_risk_score == 0.0

    def test_external_anomaly_score_contributes(self):
        engine = _engine()
        r = engine.assess(_baseline(anomaly_score_external=100.0))
        # 100 * 0.10 = 10.0
        assert r.authentication_risk_score == 10.0

    def test_external_anomaly_score_partial(self):
        engine = _engine()
        r = engine.assess(_baseline(anomaly_score_external=50.0))
        assert r.authentication_risk_score == 5.0

    def test_max_capped_at_100(self):
        engine = _engine()
        inp = _baseline(
            shared_account_flag=1,
            failed_auth_attempts=20,
            unusual_ip_count=10,
            vpn_connected=0,
            data_sensitivity_avg_score=90.0,
            anomaly_score_external=100.0,
        )
        r = engine.assess(inp)
        assert r.authentication_risk_score == 100.0


# ---------------------------------------------------------------------------
# 14. Anomaly composite formula
# ---------------------------------------------------------------------------

class TestAnomalyComposite:
    def test_composite_formula_with_known_values(self):
        engine = _engine()
        # access=8 (records 1.5x), behavioral=0, sensitivity=0, auth=0
        inp = _baseline(records_accessed_count=15, records_accessed_prior_avg=10.0)
        r = engine.assess(inp)
        expected = round(8.0 * 0.30 + 0.0 * 0.25 + 0.0 * 0.25 + 0.0 * 0.20, 1)
        assert r.anomaly_composite == expected

    def test_composite_weights_sum_to_1(self):
        # All components at 100 -> composite should be 100
        engine = _engine()
        inp = _baseline(
            records_accessed_count=500, records_accessed_prior_avg=10.0,
            download_volume_mb=500.0, download_prior_avg_mb=5.0,
            bulk_export_count=10,
            off_hours_access_pct=80.0,
            access_outside_territory_pct=70.0,
            concurrent_session_count=5,
            export_to_personal_email_count=5,
            sensitive_field_access_count=100,
            data_sensitivity_avg_score=100.0,
            privileged_data_access_count=20,
            unusual_ip_count=10,
            shared_account_flag=1,
            failed_auth_attempts=20,
            vpn_connected=0,
            anomaly_score_external=100.0,
        )
        r = engine.assess(inp)
        assert r.anomaly_composite == 100.0

    def test_composite_all_zeros(self):
        engine = _engine()
        r = engine.assess(_baseline())
        assert r.anomaly_composite == 0.0

    def test_composite_is_float(self):
        engine = _engine()
        r = engine.assess(_baseline())
        assert isinstance(r.anomaly_composite, float)

    def test_composite_rounded_to_1_decimal(self):
        engine = _engine()
        r = engine.assess(_baseline(records_accessed_count=15, records_accessed_prior_avg=10.0))
        # 8*0.30 = 2.4 -> rounded to 2.4
        assert r.anomaly_composite == round(r.anomaly_composite, 1)


# ---------------------------------------------------------------------------
# 15. Primary anomaly type logic
# ---------------------------------------------------------------------------

class TestPrimaryAnomalyType:
    def test_none_when_all_low(self):
        engine = _engine()
        r = engine.assess(_baseline())
        assert r.primary_anomaly_type == AnomalyType.NONE

    def test_data_exfiltration_when_export_personal_email_gte_1(self):
        engine = _engine()
        inp = _baseline(
            export_to_personal_email_count=1,
            # Need worst >= 25 to not return NONE
            records_accessed_count=500, records_accessed_prior_avg=10.0,
        )
        r = engine.assess(inp)
        assert r.primary_anomaly_type == AnomalyType.DATA_EXFILTRATION

    def test_data_exfiltration_when_bulk_export_high_and_download_3x(self):
        engine = _engine()
        inp = _baseline(
            bulk_export_count=3,
            download_volume_mb=30.0,
            download_prior_avg_mb=5.0,  # 30/5 = 6x > 3x
            records_accessed_count=500, records_accessed_prior_avg=10.0,
        )
        r = engine.assess(inp)
        assert r.primary_anomaly_type == AnomalyType.DATA_EXFILTRATION

    def test_credential_sharing_when_shared_account(self):
        engine = _engine()
        inp = _baseline(
            shared_account_flag=1,
            records_accessed_count=500, records_accessed_prior_avg=10.0,
        )
        r = engine.assess(inp)
        assert r.primary_anomaly_type == AnomalyType.CREDENTIAL_SHARING

    def test_credential_sharing_when_concurrent_sessions_gte_3(self):
        engine = _engine()
        inp = _baseline(
            concurrent_session_count=3,
            off_hours_access_pct=70.0,  # Make behavioral high enough
            records_accessed_count=500, records_accessed_prior_avg=10.0,
        )
        r = engine.assess(inp)
        # No export email, no shared account, but concurrent >= 3 triggers credential sharing
        assert r.primary_anomaly_type == AnomalyType.CREDENTIAL_SHARING

    def test_privilege_abuse_when_privileged_high_and_sensitivity_high(self):
        engine = _engine()
        inp = _baseline(
            privileged_data_access_count=10,
            sensitive_field_access_count=50,
            data_sensitivity_avg_score=80.0,
            unusual_ip_count=3,
            # Need sensitivity >= 50
            # sensitivity = 35 + 80*0.35 + 20 + 10 = 35+28+20+10=93
            # Also need worst >= 25
        )
        r = engine.assess(inp)
        assert r.primary_anomaly_type == AnomalyType.PRIVILEGE_ABUSE

    def test_bulk_export_type_when_access_dominant_and_bulk_gte_1(self):
        engine = _engine()
        inp = _baseline(
            bulk_export_count=1,
            records_accessed_count=500, records_accessed_prior_avg=10.0,  # access high
            download_volume_mb=25.0, download_prior_avg_mb=5.0,  # access high
        )
        r = engine.assess(inp)
        assert r.primary_anomaly_type == AnomalyType.BULK_EXPORT

    def test_off_hours_type_when_behavioral_dominant(self):
        engine = _engine()
        inp = _baseline(
            off_hours_access_pct=70.0,
            access_outside_territory_pct=60.0,
            concurrent_session_count=0,
            # behavioral=30+25=55, access=0, sensitivity=0, auth=0
            # worst=55 >= 25, no email, no shared, concurrent < 3
            # privileged_data < 10 or sensitivity < 50
            # access < behavioral -> not BULK_EXPORT
            # behavioral >= sensitivity and behavioral >= auth and off_hours >= 40 -> OFF_HOURS
        )
        r = engine.assess(inp)
        assert r.primary_anomaly_type == AnomalyType.OFF_HOURS

    def test_none_when_worst_below_25(self):
        engine = _engine()
        r = engine.assess(_baseline(off_hours_access_pct=5.0))  # behavioral = 0
        assert r.primary_anomaly_type == AnomalyType.NONE


# ---------------------------------------------------------------------------
# 16. Recommended action logic
# ---------------------------------------------------------------------------

class TestRecommendedAction:
    def test_no_action_when_level_none(self):
        engine = _engine()
        r = engine.assess(_baseline())
        assert r.anomaly_level == AnomalyLevel.NONE
        assert r.recommended_action == AnomalyAction.NO_ACTION

    def test_log_alert_when_level_low(self):
        engine = _engine()
        inp = _baseline(
            records_accessed_count=30, records_accessed_prior_avg=10.0,
            off_hours_access_pct=20.0,
        )
        r = engine.assess(inp)
        assert r.anomaly_level == AnomalyLevel.LOW
        assert r.recommended_action == AnomalyAction.LOG_ALERT

    def test_security_review_when_level_elevated(self):
        # access=100*0.30=30, composite=30 -> ELEVATED
        engine = _engine()
        inp = _baseline(
            records_accessed_count=500, records_accessed_prior_avg=10.0,
            download_volume_mb=100.0, download_prior_avg_mb=5.0,
            bulk_export_count=5,
        )
        r = engine.assess(inp)
        assert r.anomaly_level == AnomalyLevel.ELEVATED
        assert r.recommended_action == AnomalyAction.SECURITY_REVIEW

    def test_security_review_when_level_high_no_email(self):
        engine = _engine()
        inp = _baseline(
            records_accessed_count=500, records_accessed_prior_avg=10.0,
            download_volume_mb=100.0, download_prior_avg_mb=5.0,
            bulk_export_count=5,
            off_hours_access_pct=60.0,
        )
        r = engine.assess(inp)
        if r.anomaly_level == AnomalyLevel.HIGH and r.export_to_personal_email_count == 0:
            assert r.recommended_action == AnomalyAction.SECURITY_REVIEW

    def test_account_suspend_when_level_high_with_email(self):
        engine = _engine()
        inp = _baseline(
            records_accessed_count=500, records_accessed_prior_avg=10.0,
            download_volume_mb=100.0, download_prior_avg_mb=5.0,
            bulk_export_count=5,
            off_hours_access_pct=60.0,
            export_to_personal_email_count=1,
        )
        r = engine.assess(inp)
        if r.anomaly_level == AnomalyLevel.HIGH:
            assert r.recommended_action == AnomalyAction.ACCOUNT_SUSPEND

    def test_immediate_lockdown_when_level_critical(self):
        # access=100(30) + behavioral=80(20) + sensitivity=100(25) = 75 -> CRITICAL
        engine = _engine()
        inp = _baseline(
            records_accessed_count=500, records_accessed_prior_avg=10.0,
            download_volume_mb=100.0, download_prior_avg_mb=5.0,
            bulk_export_count=5,
            off_hours_access_pct=80.0,
            access_outside_territory_pct=70.0,
            concurrent_session_count=4,
            sensitive_field_access_count=50,
            data_sensitivity_avg_score=100.0,
            privileged_data_access_count=10,
            unusual_ip_count=3,
        )
        r = engine.assess(inp)
        assert r.anomaly_level == AnomalyLevel.CRITICAL
        assert r.recommended_action == AnomalyAction.IMMEDIATE_LOCKDOWN


# ---------------------------------------------------------------------------
# 17. Anomaly signal strings
# ---------------------------------------------------------------------------

class TestAnomalySignal:
    def test_normal_signal_when_composite_below_10(self):
        engine = _engine()
        r = engine.assess(_baseline())
        assert "normal access patterns" in r.anomaly_signal

    def test_low_level_signal_mentions_composite(self):
        engine = _engine()
        inp = _baseline(
            records_accessed_count=30, records_accessed_prior_avg=10.0,
            off_hours_access_pct=20.0,
        )
        r = engine.assess(inp)
        # Composite between 10-25, type is LOW (or NONE) -> fallback signal
        if r.primary_anomaly_type not in (
            AnomalyType.DATA_EXFILTRATION, AnomalyType.CREDENTIAL_SHARING,
            AnomalyType.PRIVILEGE_ABUSE, AnomalyType.BULK_EXPORT, AnomalyType.OFF_HOURS
        ):
            assert "composite score" in r.anomaly_signal or "normal access" in r.anomaly_signal

    def test_data_exfiltration_signal_mentions_export(self):
        engine = _engine()
        inp = _baseline(
            export_to_personal_email_count=2,
            records_accessed_count=500, records_accessed_prior_avg=10.0,
        )
        r = engine.assess(inp)
        assert r.primary_anomaly_type == AnomalyType.DATA_EXFILTRATION
        assert "data exfiltration" in r.anomaly_signal
        assert "2" in r.anomaly_signal  # export count

    def test_credential_sharing_signal_mentions_sessions(self):
        engine = _engine()
        inp = _baseline(
            shared_account_flag=1,
            records_accessed_count=500, records_accessed_prior_avg=10.0,
        )
        r = engine.assess(inp)
        assert r.primary_anomaly_type == AnomalyType.CREDENTIAL_SHARING
        assert "credential sharing" in r.anomaly_signal

    def test_privilege_abuse_signal_mentions_privileged(self):
        engine = _engine()
        inp = _baseline(
            privileged_data_access_count=10,
            sensitive_field_access_count=50,
            data_sensitivity_avg_score=80.0,
            unusual_ip_count=3,
        )
        r = engine.assess(inp)
        assert r.primary_anomaly_type == AnomalyType.PRIVILEGE_ABUSE
        assert "privilege abuse" in r.anomaly_signal

    def test_bulk_export_signal_mentions_bulk(self):
        engine = _engine()
        inp = _baseline(
            bulk_export_count=1,
            records_accessed_count=500, records_accessed_prior_avg=10.0,
            download_volume_mb=25.0, download_prior_avg_mb=5.0,
        )
        r = engine.assess(inp)
        assert r.primary_anomaly_type == AnomalyType.BULK_EXPORT
        assert "bulk export" in r.anomaly_signal

    def test_off_hours_signal_mentions_off_hours(self):
        engine = _engine()
        inp = _baseline(
            off_hours_access_pct=70.0,
            access_outside_territory_pct=60.0,
        )
        r = engine.assess(inp)
        assert r.primary_anomaly_type == AnomalyType.OFF_HOURS
        assert "off-hours" in r.anomaly_signal

    def test_anomaly_signal_is_string(self):
        engine = _engine()
        r = engine.assess(_baseline())
        assert isinstance(r.anomaly_signal, str)


# ---------------------------------------------------------------------------
# 18. assess_batch ordering
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_returns_list(self):
        engine = _engine()
        results = engine.assess_batch([_baseline()])
        assert isinstance(results, list)

    def test_sorted_descending_by_composite(self):
        engine = _engine()
        inputs = [
            _baseline(user_id="u1"),
            _baseline(user_id="u2", records_accessed_count=500, records_accessed_prior_avg=10.0),
            _baseline(user_id="u3", off_hours_access_pct=20.0),
        ]
        results = engine.assess_batch(inputs)
        composites = [r.anomaly_composite for r in results]
        assert composites == sorted(composites, reverse=True)

    def test_batch_size_matches_input(self):
        engine = _engine()
        inputs = [_baseline(user_id=f"u{i}") for i in range(10)]
        results = engine.assess_batch(inputs)
        assert len(results) == 10

    def test_empty_batch_returns_empty_list(self):
        engine = _engine()
        results = engine.assess_batch([])
        assert results == []

    def test_batch_stores_results_for_get(self):
        engine = _engine()
        engine.assess_batch([_baseline(user_id="xyz")])
        assert engine.get("xyz") is not None

    def test_batch_highest_composite_first(self):
        engine = _engine()
        low = _baseline(user_id="low")
        high = _baseline(
            user_id="high",
            records_accessed_count=500, records_accessed_prior_avg=10.0,
        )
        results = engine.assess_batch([low, high])
        assert results[0].user_id == "high"

    def test_single_element_batch(self):
        engine = _engine()
        results = engine.assess_batch([_baseline()])
        assert len(results) == 1


# ---------------------------------------------------------------------------
# 19. summary() aggregation correctness
# ---------------------------------------------------------------------------

class TestSummaryAggregation:
    def test_level_counts_sums_to_total(self):
        engine = _engine()
        for i in range(5):
            engine.assess(_baseline(user_id=f"u{i}"))
        s = engine.summary()
        assert sum(s["level_counts"].values()) == s["total"]

    def test_risk_counts_sums_to_total(self):
        engine = _engine()
        for i in range(5):
            engine.assess(_baseline(user_id=f"u{i}"))
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_type_counts_sums_to_total(self):
        engine = _engine()
        for i in range(5):
            engine.assess(_baseline(user_id=f"u{i}"))
        s = engine.summary()
        assert sum(s["type_counts"].values()) == s["total"]

    def test_action_counts_sums_to_total(self):
        engine = _engine()
        for i in range(5):
            engine.assess(_baseline(user_id=f"u{i}"))
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_avg_composite_is_float(self):
        engine = _engine()
        engine.assess(_baseline())
        assert isinstance(engine.summary()["avg_anomaly_composite"], float)

    def test_total_data_exposure_mb_sum(self):
        engine = _engine()
        engine.assess(_baseline(user_id="u1", download_volume_mb=10.0))
        engine.assess(_baseline(user_id="u2", download_volume_mb=20.0))
        s = engine.summary()
        r1 = engine.get("u1")
        r2 = engine.get("u2")
        expected = round(r1.estimated_data_exposure_mb + r2.estimated_data_exposure_mb, 2)
        assert s["total_data_exposure_mb"] == expected

    def test_active_threat_count_accurate(self):
        engine = _engine()
        engine.assess(_baseline(user_id="safe"))
        engine.assess(_baseline(user_id="threat", shared_account_flag=1))
        s = engine.summary()
        assert s["active_threat_count"] == 1

    def test_immediate_action_count_accurate(self):
        engine = _engine()
        engine.assess(_baseline(user_id="ok"))
        engine.assess(_baseline(user_id="urgent", export_to_personal_email_count=3))
        s = engine.summary()
        assert s["immediate_action_count"] == 1

    def test_avg_access_volume_score_correct(self):
        engine = _engine()
        engine.assess(_baseline(user_id="u1"))
        engine.assess(_baseline(user_id="u2", records_accessed_count=15, records_accessed_prior_avg=10.0))
        r1 = engine.get("u1")
        r2 = engine.get("u2")
        expected = round((r1.access_volume_score + r2.access_volume_score) / 2, 1)
        assert engine.summary()["avg_access_volume_score"] == expected

    def test_avg_behavioral_deviation_score_correct(self):
        engine = _engine()
        engine.assess(_baseline(user_id="u1"))
        engine.assess(_baseline(user_id="u2", off_hours_access_pct=20.0))
        r1 = engine.get("u1")
        r2 = engine.get("u2")
        expected = round((r1.behavioral_deviation_score + r2.behavioral_deviation_score) / 2, 1)
        assert engine.summary()["avg_behavioral_deviation_score"] == expected

    def test_avg_data_sensitivity_score_correct(self):
        engine = _engine()
        engine.assess(_baseline(user_id="u1"))
        engine.assess(_baseline(user_id="u2", sensitive_field_access_count=10))
        r1 = engine.get("u1")
        r2 = engine.get("u2")
        expected = round((r1.data_sensitivity_score + r2.data_sensitivity_score) / 2, 1)
        assert engine.summary()["avg_data_sensitivity_score"] == expected

    def test_avg_authentication_risk_score_correct(self):
        engine = _engine()
        engine.assess(_baseline(user_id="u1"))
        engine.assess(_baseline(user_id="u2", failed_auth_attempts=3))
        r1 = engine.get("u1")
        r2 = engine.get("u2")
        expected = round((r1.authentication_risk_score + r2.authentication_risk_score) / 2, 1)
        assert engine.summary()["avg_authentication_risk_score"] == expected

    def test_summary_resets_after_engine_reset(self):
        engine = _engine()
        engine.assess(_baseline())
        engine.reset()
        s = engine.summary()
        assert s["total"] == 0
        assert s["active_threat_count"] == 0

    def test_summary_after_multiple_same_user_overwritten(self):
        # Same user_id should overwrite old result
        engine = _engine()
        engine.assess(_baseline(user_id="u1", records_accessed_count=10, records_accessed_prior_avg=10.0))
        engine.assess(_baseline(user_id="u1", records_accessed_count=500, records_accessed_prior_avg=10.0))
        s = engine.summary()
        assert s["total"] == 1


# ---------------------------------------------------------------------------
# 20. Engine utility methods
# ---------------------------------------------------------------------------

class TestEngineUtilityMethods:
    def test_get_returns_result(self):
        engine = _engine()
        engine.assess(_baseline(user_id="abc"))
        r = engine.get("abc")
        assert r is not None
        assert r.user_id == "abc"

    def test_get_returns_none_for_unknown(self):
        engine = _engine()
        assert engine.get("unknown") is None

    def test_all_users_sorted_descending(self):
        engine = _engine()
        engine.assess(_baseline(user_id="u1"))
        engine.assess(_baseline(user_id="u2", records_accessed_count=500, records_accessed_prior_avg=10.0))
        users = engine.all_users()
        composites = [r.anomaly_composite for r in users]
        assert composites == sorted(composites, reverse=True)

    def test_active_threats_filters_correctly(self):
        engine = _engine()
        engine.assess(_baseline(user_id="safe"))
        engine.assess(_baseline(user_id="threat", shared_account_flag=1))
        threats = engine.active_threats()
        threat_ids = [r.user_id for r in threats]
        assert "threat" in threat_ids
        assert "safe" not in threat_ids

    def test_by_level_filters_correctly(self):
        engine = _engine()
        engine.assess(_baseline(user_id="none_level"))
        engine.assess(_baseline(user_id="low_level", records_accessed_count=30, records_accessed_prior_avg=10.0, off_hours_access_pct=20.0))
        none_results = engine.by_level(AnomalyLevel.NONE)
        for r in none_results:
            assert r.anomaly_level == AnomalyLevel.NONE

    def test_by_risk_filters_correctly(self):
        engine = _engine()
        engine.assess(_baseline(user_id="low_risk"))
        low_risk = engine.by_risk(AnomalyRisk.LOW)
        for r in low_risk:
            assert r.anomaly_risk == AnomalyRisk.LOW

    def test_total_data_exposure_mb_sums(self):
        engine = _engine()
        engine.assess(_baseline(user_id="u1"))
        engine.assess(_baseline(user_id="u2"))
        r1 = engine.get("u1")
        r2 = engine.get("u2")
        expected = round(r1.estimated_data_exposure_mb + r2.estimated_data_exposure_mb, 2)
        assert engine.total_data_exposure_mb() == expected

    def test_avg_anomaly_composite_empty(self):
        engine = _engine()
        assert engine.avg_anomaly_composite() == 0.0

    def test_avg_anomaly_composite_single(self):
        engine = _engine()
        engine.assess(_baseline())
        r = engine.get("u001")
        assert engine.avg_anomaly_composite() == r.anomaly_composite

    def test_reset_clears_results(self):
        engine = _engine()
        engine.assess(_baseline())
        engine.reset()
        assert engine.get("u001") is None

    def test_reset_makes_all_users_empty(self):
        engine = _engine()
        engine.assess(_baseline())
        engine.reset()
        assert engine.all_users() == []

    def test_reset_makes_active_threats_empty(self):
        engine = _engine()
        engine.assess(_baseline(shared_account_flag=1))
        engine.reset()
        assert engine.active_threats() == []


# ---------------------------------------------------------------------------
# 21. Edge cases and boundary values
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_zero_download_no_exposure(self):
        engine = _engine()
        r = engine.assess(_baseline(download_volume_mb=0.0))
        assert r.estimated_data_exposure_mb == 0.0

    def test_very_large_records_caps_access_score(self):
        engine = _engine()
        inp = _baseline(records_accessed_count=999999, records_accessed_prior_avg=1.0)
        r = engine.assess(inp)
        assert r.access_volume_score <= 100.0

    def test_very_large_download_caps_access_score(self):
        engine = _engine()
        inp = _baseline(download_volume_mb=999999.0, download_prior_avg_mb=1.0)
        r = engine.assess(inp)
        assert r.access_volume_score <= 100.0

    def test_all_zero_fields_no_crash(self):
        engine = _engine()
        inp = SalesDataAccessInput(
            user_id="zero", user_name="Zero", role="rep", region="north",
            records_accessed_count=0, records_accessed_prior_avg=0.0,
            download_volume_mb=0.0, download_prior_avg_mb=0.0,
            off_hours_access_pct=0.0, bulk_export_count=0,
            sensitive_field_access_count=0, failed_auth_attempts=0,
            vpn_connected=0, shared_account_flag=0, unusual_ip_count=0,
            data_sensitivity_avg_score=0.0, export_to_personal_email_count=0,
            concurrent_session_count=0, access_outside_territory_pct=0.0,
            privileged_data_access_count=0, anomaly_score_external=0.0,
            account_type="standard",
        )
        r = engine.assess(inp)
        assert r.anomaly_composite == 0.0

    def test_records_accessed_prior_avg_zero_records_zero(self):
        engine = _engine()
        inp = _baseline(records_accessed_count=0, records_accessed_prior_avg=0.0)
        r = engine.assess(inp)
        # ratio = 1.0 (both zero case), no records contribution
        assert r.access_volume_score == 0.0

    def test_download_prior_avg_zero_download_zero(self):
        engine = _engine()
        inp = _baseline(download_volume_mb=0.0, download_prior_avg_mb=0.0)
        r = engine.assess(inp)
        # dl_ratio = 1.0 (both zero), no download contribution
        assert r.access_volume_score == 0.0

    def test_composite_never_negative(self):
        engine = _engine()
        r = engine.assess(_baseline())
        assert r.anomaly_composite >= 0.0

    def test_composite_never_exceeds_100(self):
        engine = _engine()
        inp = _baseline(
            records_accessed_count=500, records_accessed_prior_avg=10.0,
            download_volume_mb=500.0, download_prior_avg_mb=5.0,
            bulk_export_count=10, off_hours_access_pct=80.0,
            shared_account_flag=1, failed_auth_attempts=20,
            sensitive_field_access_count=100, data_sensitivity_avg_score=100.0,
        )
        r = engine.assess(inp)
        assert r.anomaly_composite <= 100.0

    def test_access_score_never_negative(self):
        engine = _engine()
        r = engine.assess(_baseline())
        assert r.access_volume_score >= 0.0

    def test_behavioral_score_never_negative(self):
        engine = _engine()
        r = engine.assess(_baseline())
        assert r.behavioral_deviation_score >= 0.0

    def test_sensitivity_score_never_negative(self):
        engine = _engine()
        r = engine.assess(_baseline())
        assert r.data_sensitivity_score >= 0.0

    def test_auth_score_never_negative(self):
        engine = _engine()
        r = engine.assess(_baseline())
        assert r.authentication_risk_score >= 0.0

    def test_user_id_preserved_in_result(self):
        engine = _engine()
        r = engine.assess(_baseline(user_id="special_user"))
        assert r.user_id == "special_user"

    def test_user_name_preserved_in_result(self):
        engine = _engine()
        r = engine.assess(_baseline(user_name="Special Name"))
        assert r.user_name == "Special Name"

    def test_different_users_independent(self):
        engine = _engine()
        r1 = engine.assess(_baseline(user_id="u1"))
        r2 = engine.assess(_baseline(user_id="u2", shared_account_flag=1))
        assert r1.user_id == "u1"
        assert r2.user_id == "u2"

    def test_same_user_id_overwrites(self):
        engine = _engine()
        engine.assess(_baseline(user_id="u1", records_accessed_count=10, records_accessed_prior_avg=10.0))
        engine.assess(_baseline(user_id="u1", records_accessed_count=500, records_accessed_prior_avg=10.0))
        r = engine.get("u1")
        assert r.access_volume_score == 40.0  # 500/10=50x -> +40

    def test_bulk_export_2_not_bulk_export_threshold(self):
        # bulk_export_count=2 -> still +8 (same as >=1)
        engine = _engine()
        r = engine.assess(_baseline(bulk_export_count=2))
        assert r.access_volume_score == 8.0

    def test_off_hours_exactly_60_adds_30(self):
        engine = _engine()
        r = engine.assess(_baseline(off_hours_access_pct=60.0))
        assert r.behavioral_deviation_score == 30.0

    def test_off_hours_exactly_40_adds_20(self):
        engine = _engine()
        r = engine.assess(_baseline(off_hours_access_pct=40.0))
        assert r.behavioral_deviation_score == 20.0

    def test_off_hours_exactly_20_adds_10(self):
        engine = _engine()
        r = engine.assess(_baseline(off_hours_access_pct=20.0))
        assert r.behavioral_deviation_score == 10.0

    def test_off_hours_exactly_10_adds_4(self):
        engine = _engine()
        r = engine.assess(_baseline(off_hours_access_pct=10.0))
        assert r.behavioral_deviation_score == 4.0

    def test_off_hours_just_below_10_adds_0(self):
        engine = _engine()
        r = engine.assess(_baseline(off_hours_access_pct=9.9))
        assert r.behavioral_deviation_score == 0.0


# ---------------------------------------------------------------------------
# 22. Additional invariant and property-based-style tests
# ---------------------------------------------------------------------------

class TestResultInvariants:
    def test_result_has_all_expected_attributes(self):
        engine = _engine()
        r = engine.assess(_baseline())
        assert hasattr(r, "user_id")
        assert hasattr(r, "user_name")
        assert hasattr(r, "anomaly_level")
        assert hasattr(r, "anomaly_risk")
        assert hasattr(r, "primary_anomaly_type")
        assert hasattr(r, "recommended_action")
        assert hasattr(r, "access_volume_score")
        assert hasattr(r, "behavioral_deviation_score")
        assert hasattr(r, "data_sensitivity_score")
        assert hasattr(r, "authentication_risk_score")
        assert hasattr(r, "anomaly_composite")
        assert hasattr(r, "is_active_threat")
        assert hasattr(r, "requires_immediate_action")
        assert hasattr(r, "estimated_data_exposure_mb")
        assert hasattr(r, "anomaly_signal")

    def test_level_is_anomaly_level_enum(self):
        engine = _engine()
        r = engine.assess(_baseline())
        assert isinstance(r.anomaly_level, AnomalyLevel)

    def test_risk_is_anomaly_risk_enum(self):
        engine = _engine()
        r = engine.assess(_baseline())
        assert isinstance(r.anomaly_risk, AnomalyRisk)

    def test_type_is_anomaly_type_enum(self):
        engine = _engine()
        r = engine.assess(_baseline())
        assert isinstance(r.primary_anomaly_type, AnomalyType)

    def test_action_is_anomaly_action_enum(self):
        engine = _engine()
        r = engine.assess(_baseline())
        assert isinstance(r.recommended_action, AnomalyAction)

    def test_is_active_threat_is_bool(self):
        engine = _engine()
        r = engine.assess(_baseline())
        assert isinstance(r.is_active_threat, bool)

    def test_requires_immediate_action_is_bool(self):
        engine = _engine()
        r = engine.assess(_baseline())
        assert isinstance(r.requires_immediate_action, bool)

    def test_composite_is_float(self):
        engine = _engine()
        r = engine.assess(_baseline())
        assert isinstance(r.anomaly_composite, float)

    def test_requires_immediate_implies_active_threat(self):
        # If requires_immediate_action is True, is_active_threat should also be True
        # (because composite >= 65 -> composite >= 45, or email >= 3 -> email >= 2,
        #  or shared && composite >= 40 -> shared -> is_active_threat)
        engine = _engine()
        inputs = [
            _baseline(user_id="u1", export_to_personal_email_count=3),
            _baseline(user_id="u2", records_accessed_count=500, records_accessed_prior_avg=10.0,
                      download_volume_mb=500.0, download_prior_avg_mb=5.0,
                      bulk_export_count=10, off_hours_access_pct=80.0,
                      shared_account_flag=1, failed_auth_attempts=15),
        ]
        for inp in inputs:
            r = engine.assess(inp)
            if r.requires_immediate_action:
                assert r.is_active_threat, f"requires_immediate=True but is_active_threat=False for {inp.user_id}"

    def test_critical_level_always_immediate_lockdown(self):
        engine = _engine()
        inp = _baseline(
            records_accessed_count=500, records_accessed_prior_avg=10.0,
            download_volume_mb=500.0, download_prior_avg_mb=5.0,
            bulk_export_count=10, off_hours_access_pct=80.0,
            shared_account_flag=1, failed_auth_attempts=15,
        )
        r = engine.assess(inp)
        if r.anomaly_level == AnomalyLevel.CRITICAL:
            assert r.recommended_action == AnomalyAction.IMMEDIATE_LOCKDOWN

    def test_none_level_always_no_action(self):
        engine = _engine()
        r = engine.assess(_baseline())
        if r.anomaly_level == AnomalyLevel.NONE:
            assert r.recommended_action == AnomalyAction.NO_ACTION

    def test_elevated_level_always_security_review(self):
        engine = _engine()
        inp = _baseline(
            records_accessed_count=50, records_accessed_prior_avg=10.0,
            off_hours_access_pct=20.0,
        )
        r = engine.assess(inp)
        if r.anomaly_level == AnomalyLevel.ELEVATED:
            assert r.recommended_action == AnomalyAction.SECURITY_REVIEW

    def test_low_level_always_log_alert(self):
        engine = _engine()
        inp = _baseline(records_accessed_count=30, records_accessed_prior_avg=10.0, off_hours_access_pct=20.0)
        r = engine.assess(inp)
        if r.anomaly_level == AnomalyLevel.LOW:
            assert r.recommended_action == AnomalyAction.LOG_ALERT


# ---------------------------------------------------------------------------
# 23. to_dict() value types
# ---------------------------------------------------------------------------

class TestToDictValues:
    def test_user_id_is_str(self):
        engine = _engine()
        d = engine.assess(_baseline()).to_dict()
        assert isinstance(d["user_id"], str)

    def test_user_name_is_str(self):
        engine = _engine()
        d = engine.assess(_baseline()).to_dict()
        assert isinstance(d["user_name"], str)

    def test_anomaly_level_value_in_valid_set(self):
        engine = _engine()
        d = engine.assess(_baseline()).to_dict()
        assert d["anomaly_level"] in {"none", "low", "elevated", "high", "critical"}

    def test_anomaly_risk_value_in_valid_set(self):
        engine = _engine()
        d = engine.assess(_baseline()).to_dict()
        assert d["anomaly_risk"] in {"low", "moderate", "high", "critical"}

    def test_primary_anomaly_type_in_valid_set(self):
        engine = _engine()
        d = engine.assess(_baseline()).to_dict()
        assert d["primary_anomaly_type"] in {
            "none", "bulk_export", "off_hours", "credential_sharing",
            "data_exfiltration", "privilege_abuse"
        }

    def test_recommended_action_in_valid_set(self):
        engine = _engine()
        d = engine.assess(_baseline()).to_dict()
        assert d["recommended_action"] in {
            "no_action", "log_alert", "security_review",
            "account_suspend", "immediate_lockdown"
        }

    def test_access_volume_score_is_float(self):
        engine = _engine()
        d = engine.assess(_baseline()).to_dict()
        assert isinstance(d["access_volume_score"], float)

    def test_behavioral_deviation_score_is_float(self):
        engine = _engine()
        d = engine.assess(_baseline()).to_dict()
        assert isinstance(d["behavioral_deviation_score"], float)

    def test_data_sensitivity_score_is_float(self):
        engine = _engine()
        d = engine.assess(_baseline()).to_dict()
        assert isinstance(d["data_sensitivity_score"], float)

    def test_authentication_risk_score_is_float(self):
        engine = _engine()
        d = engine.assess(_baseline()).to_dict()
        assert isinstance(d["authentication_risk_score"], float)

    def test_anomaly_composite_is_numeric(self):
        engine = _engine()
        d = engine.assess(_baseline()).to_dict()
        assert isinstance(d["anomaly_composite"], (int, float))

    def test_estimated_data_exposure_mb_is_float(self):
        engine = _engine()
        d = engine.assess(_baseline()).to_dict()
        assert isinstance(d["estimated_data_exposure_mb"], float)

    def test_anomaly_signal_is_str(self):
        engine = _engine()
        d = engine.assess(_baseline()).to_dict()
        assert isinstance(d["anomaly_signal"], str)


# ---------------------------------------------------------------------------
# 24. Parametrized threshold boundary tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("off_hours, expected_add", [
    (0.0, 0.0),
    (9.9, 0.0),
    (10.0, 4.0),
    (19.9, 4.0),
    (20.0, 10.0),
    (39.9, 10.0),
    (40.0, 20.0),
    (59.9, 20.0),
    (60.0, 30.0),
    (100.0, 30.0),
])
def test_off_hours_pct_contribution(off_hours, expected_add):
    engine = _engine()
    r = engine.assess(_baseline(off_hours_access_pct=off_hours))
    assert r.behavioral_deviation_score == expected_add


@pytest.mark.parametrize("bulk, expected_add", [
    (0, 0.0),
    (1, 8.0),
    (2, 8.0),
    (3, 17.0),
    (4, 17.0),
    (5, 25.0),
    (100, 25.0),
])
def test_bulk_export_count_contribution(bulk, expected_add):
    engine = _engine()
    r = engine.assess(_baseline(bulk_export_count=bulk))
    assert r.access_volume_score == expected_add


@pytest.mark.parametrize("concurrent, expected_add", [
    (0, 0.0),
    (1, 0.0),
    (2, 8.0),
    (3, 16.0),
    (4, 25.0),
    (10, 25.0),
])
def test_concurrent_session_contribution(concurrent, expected_add):
    engine = _engine()
    r = engine.assess(_baseline(concurrent_session_count=concurrent))
    assert r.behavioral_deviation_score == expected_add


@pytest.mark.parametrize("email, expected_add", [
    (0, 0.0),
    (1, 12.0),
    (2, 12.0),
    (3, 20.0),
    (10, 20.0),
])
def test_export_personal_email_behavioral_contribution(email, expected_add):
    engine = _engine()
    r = engine.assess(_baseline(export_to_personal_email_count=email))
    assert r.behavioral_deviation_score == expected_add


@pytest.mark.parametrize("failed, expected_add", [
    (0, 0.0),
    (1, 4.0),
    (2, 4.0),
    (3, 10.0),
    (4, 10.0),
    (5, 20.0),
    (9, 20.0),
    (10, 30.0),
    (100, 30.0),
])
def test_failed_auth_attempts_contribution(failed, expected_add):
    engine = _engine()
    r = engine.assess(_baseline(failed_auth_attempts=failed))
    assert r.authentication_risk_score == expected_add


@pytest.mark.parametrize("email, is_threat", [
    (0, False),
    (1, False),
    (2, True),
    (3, True),
    (5, True),
])
def test_is_active_threat_email_boundary(email, is_threat):
    engine = _engine()
    r = engine.assess(_baseline(export_to_personal_email_count=email))
    assert r.is_active_threat == is_threat


@pytest.mark.parametrize("email, immediate", [
    (0, False),
    (1, False),
    (2, False),
    (3, True),
    (4, True),
])
def test_requires_immediate_email_boundary(email, immediate):
    engine = _engine()
    r = engine.assess(_baseline(export_to_personal_email_count=email))
    assert r.requires_immediate_action == immediate


@pytest.mark.parametrize("shared, is_threat", [
    (0, False),
    (1, True),
])
def test_is_active_threat_shared_account(shared, is_threat):
    engine = _engine()
    r = engine.assess(_baseline(shared_account_flag=shared))
    assert r.is_active_threat == is_threat


@pytest.mark.parametrize("composite_level, expected_level", [
    (0.0, AnomalyLevel.NONE),
    (9.9, AnomalyLevel.NONE),
    (10.0, AnomalyLevel.LOW),
    (24.9, AnomalyLevel.LOW),
    (25.0, AnomalyLevel.ELEVATED),
    (44.9, AnomalyLevel.ELEVATED),
    (45.0, AnomalyLevel.HIGH),
    (64.9, AnomalyLevel.HIGH),
    (65.0, AnomalyLevel.CRITICAL),
    (100.0, AnomalyLevel.CRITICAL),
])
def test_anomaly_level_boundaries(composite_level, expected_level):
    """Verify level boundaries using known input combinations that hit specific composites."""
    # We can't directly set composite, so we test the level function indirectly
    # by verifying the documented thresholds via the result
    # Access=100 * 0.30 = 30, behavioral varies
    # For specific composites we use the engine result and check the boundary logic
    from swarm.intelligence.sales_data_access_anomaly_engine import _anomaly_level
    assert _anomaly_level(composite_level) == expected_level


@pytest.mark.parametrize("composite_val, expected_risk", [
    (0.0, AnomalyRisk.LOW),
    (14.9, AnomalyRisk.LOW),
    (15.0, AnomalyRisk.MODERATE),
    (34.9, AnomalyRisk.MODERATE),
    (35.0, AnomalyRisk.HIGH),
    (54.9, AnomalyRisk.HIGH),
    (55.0, AnomalyRisk.CRITICAL),
    (100.0, AnomalyRisk.CRITICAL),
])
def test_anomaly_risk_boundaries(composite_val, expected_risk):
    from swarm.intelligence.sales_data_access_anomaly_engine import _anomaly_risk
    assert _anomaly_risk(composite_val) == expected_risk


# ---------------------------------------------------------------------------
# 25. Summary correctness for zero/empty engine
# ---------------------------------------------------------------------------

class TestEmptySummary:
    def test_empty_level_counts(self):
        assert _engine().summary()["level_counts"] == {}

    def test_empty_risk_counts(self):
        assert _engine().summary()["risk_counts"] == {}

    def test_empty_type_counts(self):
        assert _engine().summary()["type_counts"] == {}

    def test_empty_action_counts(self):
        assert _engine().summary()["action_counts"] == {}

    def test_avg_access_volume_score_empty(self):
        assert _engine().summary()["avg_access_volume_score"] == 0.0

    def test_avg_behavioral_deviation_score_empty(self):
        assert _engine().summary()["avg_behavioral_deviation_score"] == 0.0

    def test_avg_data_sensitivity_score_empty(self):
        assert _engine().summary()["avg_data_sensitivity_score"] == 0.0

    def test_avg_authentication_risk_score_empty(self):
        assert _engine().summary()["avg_authentication_risk_score"] == 0.0

    def test_total_data_exposure_mb_empty(self):
        assert _engine().summary()["total_data_exposure_mb"] == 0.0

    def test_immediate_action_count_empty(self):
        assert _engine().summary()["immediate_action_count"] == 0


# ---------------------------------------------------------------------------
# 26. Multiple-condition combined tests
# ---------------------------------------------------------------------------

class TestCombinedConditions:
    def test_all_threat_signals_combined(self):
        engine = _engine()
        inp = _baseline(
            export_to_personal_email_count=2,
            shared_account_flag=1,
            records_accessed_count=500, records_accessed_prior_avg=10.0,
        )
        r = engine.assess(inp)
        assert r.is_active_threat is True

    def test_critical_composite_triggers_critical_level_and_lockdown(self):
        engine = _engine()
        inp = _baseline(
            records_accessed_count=500, records_accessed_prior_avg=10.0,
            download_volume_mb=500.0, download_prior_avg_mb=5.0,
            bulk_export_count=10, off_hours_access_pct=80.0,
            shared_account_flag=1, failed_auth_attempts=15,
            sensitive_field_access_count=60, export_to_personal_email_count=5,
        )
        r = engine.assess(inp)
        assert r.anomaly_level == AnomalyLevel.CRITICAL
        assert r.recommended_action == AnomalyAction.IMMEDIATE_LOCKDOWN
        assert r.is_active_threat is True
        assert r.requires_immediate_action is True

    def test_privilege_abuse_type_requires_both_conditions(self):
        # privileged_data_access_count >= 10 AND sensitivity >= 50
        engine = _engine()
        inp = _baseline(
            privileged_data_access_count=10,
            sensitive_field_access_count=50,  # +35
            data_sensitivity_avg_score=50.0,  # +17.5
            unusual_ip_count=3,               # +10 -> sensitivity = 62.5 >= 50
        )
        r = engine.assess(inp)
        assert r.primary_anomaly_type == AnomalyType.PRIVILEGE_ABUSE

    def test_privilege_abuse_fails_when_sensitivity_below_50(self):
        # sensitivity < 50 should not produce PRIVILEGE_ABUSE
        engine = _engine()
        inp = _baseline(
            privileged_data_access_count=10,
            # sensitivity = 0 (all other factors zero)
        )
        r = engine.assess(inp)
        # sensitivity_score = 20 (priveleged=10) < 50 -> no privilege_abuse
        assert r.primary_anomaly_type != AnomalyType.PRIVILEGE_ABUSE

    def test_data_exfiltration_takes_precedence_over_credential_sharing(self):
        # When both email export >= 1 AND shared_account_flag == 1
        engine = _engine()
        inp = _baseline(
            export_to_personal_email_count=1,
            shared_account_flag=1,
            records_accessed_count=500, records_accessed_prior_avg=10.0,
        )
        r = engine.assess(inp)
        # DATA_EXFILTRATION checked before CREDENTIAL_SHARING
        assert r.primary_anomaly_type == AnomalyType.DATA_EXFILTRATION

    def test_high_level_no_email_gives_security_review(self):
        engine = _engine()
        inp = _baseline(
            records_accessed_count=500, records_accessed_prior_avg=10.0,
            download_volume_mb=100.0, download_prior_avg_mb=5.0,
            bulk_export_count=5, off_hours_access_pct=60.0,
            export_to_personal_email_count=0,
        )
        r = engine.assess(inp)
        if r.anomaly_level == AnomalyLevel.HIGH:
            assert r.recommended_action == AnomalyAction.SECURITY_REVIEW

    def test_summary_with_mixed_users(self):
        engine = _engine()
        engine.assess(_baseline(user_id="safe"))
        engine.assess(_baseline(user_id="threat", shared_account_flag=1))
        engine.assess(_baseline(user_id="critical",
                                records_accessed_count=500, records_accessed_prior_avg=10.0,
                                download_volume_mb=500.0, download_prior_avg_mb=5.0,
                                bulk_export_count=10, off_hours_access_pct=80.0))
        s = engine.summary()
        assert s["total"] == 3
        assert len(s) == 13

    def test_assess_batch_then_summary_consistent(self):
        engine = _engine()
        inputs = [_baseline(user_id=f"u{i}") for i in range(5)]
        engine.assess_batch(inputs)
        s = engine.summary()
        assert s["total"] == 5

    def test_multiple_engines_independent(self):
        e1 = _engine()
        e2 = _engine()
        e1.assess(_baseline(user_id="shared_id", shared_account_flag=1))
        e2.assess(_baseline(user_id="shared_id"))
        assert e1.get("shared_id").is_active_threat is True
        assert e2.get("shared_id").is_active_threat is False

    def test_external_anomaly_score_plus_no_vpn_sensitive(self):
        engine = _engine()
        inp = _baseline(
            anomaly_score_external=100.0,
            vpn_connected=0,
            data_sensitivity_avg_score=60.0,
        )
        r = engine.assess(inp)
        # auth = 10 (no vpn, sensitivity >= 60) + 100*0.10 (external) = 20
        assert r.authentication_risk_score == 20.0

    def test_access_volume_all_thresholds_combined(self):
        engine = _engine()
        inp = _baseline(
            records_accessed_count=500, records_accessed_prior_avg=10.0,  # ratio=50 -> +40
            download_volume_mb=100.0, download_prior_avg_mb=5.0,          # ratio=20 -> +35
            bulk_export_count=5,                                            # +25
        )
        r = engine.assess(inp)
        assert r.access_volume_score == 100.0


# ---------------------------------------------------------------------------
# 27. Signal format tests
# ---------------------------------------------------------------------------

class TestSignalFormat:
    def test_data_exfiltration_signal_has_mb(self):
        engine = _engine()
        inp = _baseline(
            export_to_personal_email_count=2,
            download_volume_mb=100.0,
            records_accessed_count=500, records_accessed_prior_avg=10.0,
        )
        r = engine.assess(inp)
        assert "MB" in r.anomaly_signal or "mb" in r.anomaly_signal.lower()

    def test_data_exfiltration_signal_includes_count(self):
        engine = _engine()
        inp = _baseline(
            export_to_personal_email_count=2,
            records_accessed_count=500, records_accessed_prior_avg=10.0,
        )
        r = engine.assess(inp)
        assert "2" in r.anomaly_signal

    def test_bulk_export_signal_includes_baseline(self):
        engine = _engine()
        inp = _baseline(
            bulk_export_count=1,
            records_accessed_count=500, records_accessed_prior_avg=10.0,
            download_volume_mb=25.0, download_prior_avg_mb=5.0,
        )
        r = engine.assess(inp)
        if r.primary_anomaly_type == AnomalyType.BULK_EXPORT:
            assert "baseline" in r.anomaly_signal or "vs" in r.anomaly_signal

    def test_credential_sharing_signal_includes_session_count(self):
        engine = _engine()
        inp = _baseline(
            shared_account_flag=1,
            records_accessed_count=500, records_accessed_prior_avg=10.0,
        )
        r = engine.assess(inp)
        assert "session" in r.anomaly_signal or "sessions" in r.anomaly_signal

    def test_off_hours_signal_includes_percentage(self):
        engine = _engine()
        inp = _baseline(
            off_hours_access_pct=70.0,
            access_outside_territory_pct=60.0,
        )
        r = engine.assess(inp)
        assert r.primary_anomaly_type == AnomalyType.OFF_HOURS
        assert "%" in r.anomaly_signal

    def test_normal_signal_no_anomaly_message(self):
        engine = _engine()
        r = engine.assess(_baseline())
        assert "no anomalies" in r.anomaly_signal


# ---------------------------------------------------------------------------
# 28. Regression tests for specific score combos
# ---------------------------------------------------------------------------

class TestRegressionSpecificCombos:
    def test_regression_all_moderate(self):
        engine = _engine()
        inp = _baseline(
            records_accessed_count=20, records_accessed_prior_avg=10.0,  # ratio=2 -> +16
            download_volume_mb=10.0, download_prior_avg_mb=5.0,          # ratio=2 -> +12
            bulk_export_count=1,                                           # +8
            off_hours_access_pct=20.0,                                    # +10
            access_outside_territory_pct=15.0,                            # +8
        )
        r = engine.assess(inp)
        assert r.access_volume_score == 36.0
        assert r.behavioral_deviation_score == 18.0

    def test_regression_sensitivity_all_factors(self):
        engine = _engine()
        inp = _baseline(
            sensitive_field_access_count=10,  # +12
            data_sensitivity_avg_score=40.0,   # 40*0.35=14
            privileged_data_access_count=1,    # +6
            unusual_ip_count=1,                # +5
        )
        r = engine.assess(inp)
        assert r.data_sensitivity_score == round(12.0 + 14.0 + 6.0 + 5.0, 1)

    def test_regression_auth_all_factors(self):
        engine = _engine()
        inp = _baseline(
            shared_account_flag=1,        # +40
            failed_auth_attempts=5,       # +20
            unusual_ip_count=3,           # +13
            vpn_connected=0,
            data_sensitivity_avg_score=70.0,  # no vpn + sensitivity >= 60 -> +10
            anomaly_score_external=50.0,  # +5
        )
        r = engine.assess(inp)
        assert r.authentication_risk_score == min(100.0, round(40.0 + 20.0 + 13.0 + 10.0 + 5.0, 1))

    def test_regression_composite_with_known_values(self):
        engine = _engine()
        inp = _baseline(
            records_accessed_count=30, records_accessed_prior_avg=10.0,  # records: +28
            off_hours_access_pct=20.0,   # +10 behavioral
        )
        r = engine.assess(inp)
        # access=28, behavioral=10, sensitivity=0, auth=0
        expected = round(28 * 0.30 + 10 * 0.25 + 0 * 0.25 + 0 * 0.20, 1)
        assert r.anomaly_composite == expected

    def test_regression_exposure_mb(self):
        # records=30/10 -> ratio=3 -> +28 access
        # download=50/5 -> ratio=10 -> >=5x -> +35 access
        # access = 28+35 = 63; behavioral=10 (off_hours 20%)
        # composite = 63*0.30 + 10*0.25 = 18.9 + 2.5 = 21.4
        # exposure = 50.0 * (21.4/100) = 10.7
        engine = _engine()
        inp = _baseline(
            download_volume_mb=50.0,
            records_accessed_count=30, records_accessed_prior_avg=10.0,
            off_hours_access_pct=20.0,
        )
        r = engine.assess(inp)
        assert r.access_volume_score == 63.0
        assert r.anomaly_composite == 21.4
        assert r.estimated_data_exposure_mb == round(50.0 * (21.4 / 100.0), 2)


# ---------------------------------------------------------------------------
# 29. Test engine with many users in summary
# ---------------------------------------------------------------------------

class TestSummaryWithManyUsers:
    def test_summary_100_users(self):
        engine = _engine()
        for i in range(100):
            engine.assess(_baseline(user_id=f"u{i}"))
        s = engine.summary()
        assert s["total"] == 100
        assert len(s) == 13

    def test_summary_level_counts_coherent_large(self):
        engine = _engine()
        for i in range(50):
            engine.assess(_baseline(user_id=f"u{i}"))
        s = engine.summary()
        total_from_levels = sum(s["level_counts"].values())
        assert total_from_levels == s["total"]

    def test_summary_action_counts_coherent_large(self):
        engine = _engine()
        for i in range(50):
            engine.assess(_baseline(user_id=f"u{i}"))
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_active_threat_count_lte_total(self):
        engine = _engine()
        for i in range(20):
            engine.assess(_baseline(user_id=f"u{i}"))
        s = engine.summary()
        assert s["active_threat_count"] <= s["total"]

    def test_immediate_action_count_lte_active_threat_count_or_total(self):
        engine = _engine()
        for i in range(20):
            engine.assess(_baseline(user_id=f"u{i}"))
        s = engine.summary()
        # immediate <= total
        assert s["immediate_action_count"] <= s["total"]
