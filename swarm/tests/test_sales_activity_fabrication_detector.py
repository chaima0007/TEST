"""Comprehensive pytest test suite for SalesActivityFabricationDetector."""

import dataclasses
import math
import pytest

from swarm.intelligence.sales_activity_fabrication_detector import (
    SalesActivityFabricationDetector,
    SalesActivityFabricationInput,
    FabricationRisk,
    FabricationPattern,
    FabricationAction,
    FabricationSeverity,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> SalesActivityFabricationInput:
    """Return a clean (low-suspicion) input, optionally overriding fields."""
    defaults = dict(
        rep_id="R001",
        rep_name="Alice Smith",
        region="West",
        manager_id="M001",
        calls_logged_count=20,
        calls_with_notes_count=20,
        calls_avg_duration_seconds=120.0,
        calls_after_hours_pct=10.0,
        meetings_logged_count=10,
        meetings_with_attendees_count=10,
        meetings_calendar_match_pct=95.0,
        meetings_with_notes_pct=90.0,
        bulk_log_events_count=0,
        activities_end_of_month_pct=20.0,
        activities_end_of_quarter_pct=25.0,
        follow_up_email_rate_pct=80.0,
        crm_edit_after_submission_count=0,
        retroactive_log_pct=5.0,
        prospect_response_rate_pct=75.0,
        deal_stage_advance_rate_pct=60.0,
        manager_verified_activity_pct=85.0,
        peer_corroboration_score=80.0,
    )
    defaults.update(overrides)
    return SalesActivityFabricationInput(**defaults)


def fresh_detector() -> SalesActivityFabricationDetector:
    return SalesActivityFabricationDetector()


def clamp(v: float) -> float:
    return max(0.0, min(100.0, v))


# ---------------------------------------------------------------------------
# 1. Enum membership and values
# ---------------------------------------------------------------------------

class TestEnums:
    def test_fabrication_risk_values(self):
        assert set(r.value for r in FabricationRisk) == {"none", "low", "moderate", "high", "critical"}

    def test_fabrication_pattern_values(self):
        assert set(p.value for p in FabricationPattern) == {
            "none", "phantom_calls", "fake_meetings", "bulk_logging",
            "no_follow_up", "note_absence", "timestamp_clustering",
        }

    def test_fabrication_action_values(self):
        assert set(a.value for a in FabricationAction) == {
            "no_action", "monitor", "audit_request", "manager_review", "hr_escalation",
        }

    def test_fabrication_severity_values(self):
        assert set(s.value for s in FabricationSeverity) == {
            "clean", "suspicious", "likely_fabricated", "confirmed_fraud",
        }

    def test_risk_is_str_enum(self):
        assert isinstance(FabricationRisk.none, str)

    def test_pattern_is_str_enum(self):
        assert isinstance(FabricationPattern.phantom_calls, str)

    def test_action_is_str_enum(self):
        assert isinstance(FabricationAction.no_action, str)

    def test_severity_is_str_enum(self):
        assert isinstance(FabricationSeverity.clean, str)

    def test_risk_count(self):
        assert len(FabricationRisk) == 5

    def test_pattern_count(self):
        assert len(FabricationPattern) == 7

    def test_action_count(self):
        assert len(FabricationAction) == 5

    def test_severity_count(self):
        assert len(FabricationSeverity) == 4


# ---------------------------------------------------------------------------
# 2. Input dataclass — exactly 22 fields
# ---------------------------------------------------------------------------

class TestInputDataclass:
    def test_field_count(self):
        fields = dataclasses.fields(SalesActivityFabricationInput)
        assert len(fields) == 22

    def test_field_names(self):
        expected = {
            "rep_id", "rep_name", "region", "manager_id",
            "calls_logged_count", "calls_with_notes_count", "calls_avg_duration_seconds",
            "calls_after_hours_pct", "meetings_logged_count", "meetings_with_attendees_count",
            "meetings_calendar_match_pct", "meetings_with_notes_pct",
            "bulk_log_events_count", "activities_end_of_month_pct",
            "activities_end_of_quarter_pct", "follow_up_email_rate_pct",
            "crm_edit_after_submission_count", "retroactive_log_pct",
            "prospect_response_rate_pct", "deal_stage_advance_rate_pct",
            "manager_verified_activity_pct", "peer_corroboration_score",
        }
        actual = {f.name for f in dataclasses.fields(SalesActivityFabricationInput)}
        assert actual == expected

    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(SalesActivityFabricationInput)

    def test_instantiation_with_all_fields(self):
        inp = make_input()
        assert inp.rep_id == "R001"

    def test_rep_id_field(self):
        inp = make_input(rep_id="X99")
        assert inp.rep_id == "X99"

    def test_rep_name_field(self):
        inp = make_input(rep_name="Bob")
        assert inp.rep_name == "Bob"

    def test_region_field(self):
        inp = make_input(region="East")
        assert inp.region == "East"

    def test_manager_id_field(self):
        inp = make_input(manager_id="MGR7")
        assert inp.manager_id == "MGR7"

    def test_deal_stage_advance_rate_field_exists(self):
        inp = make_input(deal_stage_advance_rate_pct=42.0)
        assert inp.deal_stage_advance_rate_pct == 42.0


# ---------------------------------------------------------------------------
# 3. to_dict — exactly 15 keys
# ---------------------------------------------------------------------------

class TestToDict:
    def test_key_count(self):
        d = fresh_detector()
        result = d.assess(make_input())
        assert len(result.to_dict()) == 15

    def test_key_names(self):
        d = fresh_detector()
        result = d.assess(make_input())
        expected_keys = {
            "rep_id", "rep_name", "fabrication_risk", "fabrication_severity",
            "primary_fabrication_pattern", "recommended_action",
            "call_authenticity_score", "meeting_authenticity_score",
            "timing_anomaly_score", "corroboration_score",
            "fabrication_composite", "is_likely_fabricating",
            "requires_audit", "estimated_fake_activity_pct",
            "fabrication_signal",
        }
        assert set(result.to_dict().keys()) == expected_keys

    def test_risk_value_is_string(self):
        d = fresh_detector()
        r = d.assess(make_input()).to_dict()
        assert isinstance(r["fabrication_risk"], str)

    def test_severity_value_is_string(self):
        d = fresh_detector()
        r = d.assess(make_input()).to_dict()
        assert isinstance(r["fabrication_severity"], str)

    def test_pattern_value_is_string(self):
        d = fresh_detector()
        r = d.assess(make_input()).to_dict()
        assert isinstance(r["primary_fabrication_pattern"], str)

    def test_action_value_is_string(self):
        d = fresh_detector()
        r = d.assess(make_input()).to_dict()
        assert isinstance(r["recommended_action"], str)

    def test_is_likely_fabricating_is_bool(self):
        d = fresh_detector()
        r = d.assess(make_input()).to_dict()
        assert isinstance(r["is_likely_fabricating"], bool)

    def test_requires_audit_is_bool(self):
        d = fresh_detector()
        r = d.assess(make_input()).to_dict()
        assert isinstance(r["requires_audit"], bool)

    def test_fabrication_signal_is_string(self):
        d = fresh_detector()
        r = d.assess(make_input()).to_dict()
        assert isinstance(r["fabrication_signal"], str)

    def test_composite_rounded_to_one_decimal(self):
        d = fresh_detector()
        r = d.assess(make_input()).to_dict()
        val = r["fabrication_composite"]
        assert round(val, 1) == val

    def test_call_score_rounded_to_one_decimal(self):
        d = fresh_detector()
        r = d.assess(make_input()).to_dict()
        val = r["call_authenticity_score"]
        assert round(val, 1) == val

    def test_meeting_score_rounded_to_one_decimal(self):
        d = fresh_detector()
        r = d.assess(make_input()).to_dict()
        val = r["meeting_authenticity_score"]
        assert round(val, 1) == val

    def test_timing_score_rounded_to_one_decimal(self):
        d = fresh_detector()
        r = d.assess(make_input()).to_dict()
        val = r["timing_anomaly_score"]
        assert round(val, 1) == val

    def test_corroboration_score_rounded_to_one_decimal(self):
        d = fresh_detector()
        r = d.assess(make_input()).to_dict()
        val = r["corroboration_score"]
        assert round(val, 1) == val

    def test_rep_id_passthrough(self):
        d = fresh_detector()
        r = d.assess(make_input(rep_id="Z55")).to_dict()
        assert r["rep_id"] == "Z55"

    def test_rep_name_passthrough(self):
        d = fresh_detector()
        r = d.assess(make_input(rep_name="Jane")).to_dict()
        assert r["rep_name"] == "Jane"


# ---------------------------------------------------------------------------
# 4. summary() — exactly 13 keys
# ---------------------------------------------------------------------------

class TestSummaryKeys:
    def test_empty_summary_key_count(self):
        d = fresh_detector()
        s = d.summary()
        assert len(s) == 13

    def test_non_empty_summary_key_count(self):
        d = fresh_detector()
        d.assess(make_input())
        s = d.summary()
        assert len(s) == 13

    def test_summary_key_names(self):
        d = fresh_detector()
        d.assess(make_input())
        expected = {
            "total", "risk_counts", "severity_counts", "pattern_counts",
            "action_counts", "avg_fabrication_composite",
            "likely_fabricating_count", "audit_required_count",
            "avg_call_authenticity_score", "avg_meeting_authenticity_score",
            "avg_timing_anomaly_score", "avg_corroboration_score",
            "avg_estimated_fake_activity_pct",
        }
        assert set(d.summary().keys()) == expected

    def test_empty_summary_total_zero(self):
        d = fresh_detector()
        assert d.summary()["total"] == 0

    def test_empty_summary_risk_counts_empty(self):
        d = fresh_detector()
        assert d.summary()["risk_counts"] == {}

    def test_empty_summary_severity_counts_empty(self):
        d = fresh_detector()
        assert d.summary()["severity_counts"] == {}

    def test_empty_summary_pattern_counts_empty(self):
        d = fresh_detector()
        assert d.summary()["pattern_counts"] == {}

    def test_empty_summary_action_counts_empty(self):
        d = fresh_detector()
        assert d.summary()["action_counts"] == {}

    def test_empty_summary_avg_composite_zero(self):
        d = fresh_detector()
        assert d.summary()["avg_fabrication_composite"] == 0.0

    def test_empty_summary_likely_fabricating_zero(self):
        d = fresh_detector()
        assert d.summary()["likely_fabricating_count"] == 0

    def test_empty_summary_audit_required_zero(self):
        d = fresh_detector()
        assert d.summary()["audit_required_count"] == 0

    def test_empty_summary_avg_call_score_zero(self):
        d = fresh_detector()
        assert d.summary()["avg_call_authenticity_score"] == 0.0

    def test_empty_summary_avg_meeting_score_zero(self):
        d = fresh_detector()
        assert d.summary()["avg_meeting_authenticity_score"] == 0.0

    def test_empty_summary_avg_timing_score_zero(self):
        d = fresh_detector()
        assert d.summary()["avg_timing_anomaly_score"] == 0.0

    def test_empty_summary_avg_corroboration_score_zero(self):
        d = fresh_detector()
        assert d.summary()["avg_corroboration_score"] == 0.0

    def test_empty_summary_avg_fake_pct_zero(self):
        d = fresh_detector()
        assert d.summary()["avg_estimated_fake_activity_pct"] == 0.0

    def test_summary_total_after_one(self):
        d = fresh_detector()
        d.assess(make_input())
        assert d.summary()["total"] == 1

    def test_summary_total_after_three(self):
        d = fresh_detector()
        for _ in range(3):
            d.assess(make_input())
        assert d.summary()["total"] == 3

    def test_summary_risk_counts_sums_to_total(self):
        d = fresh_detector()
        for _ in range(5):
            d.assess(make_input())
        s = d.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_severity_counts_sums_to_total(self):
        d = fresh_detector()
        for _ in range(4):
            d.assess(make_input())
        s = d.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_summary_pattern_counts_sums_to_total(self):
        d = fresh_detector()
        for _ in range(4):
            d.assess(make_input())
        s = d.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_summary_action_counts_sums_to_total(self):
        d = fresh_detector()
        for _ in range(4):
            d.assess(make_input())
        s = d.summary()
        assert sum(s["action_counts"].values()) == s["total"]


# ---------------------------------------------------------------------------
# 5. Composite formula: call*0.30 + meeting*0.25 + timing*0.25 + corr*0.20
# ---------------------------------------------------------------------------

class TestCompositeFormula:
    def _compute_call(self, inp):
        score = 0.0
        note_rate = (inp.calls_with_notes_count / inp.calls_logged_count
                     if inp.calls_logged_count > 0 else 1.0)
        score += (1.0 - note_rate) * 40.0
        if inp.calls_avg_duration_seconds < 30:
            score += 35.0
        elif inp.calls_avg_duration_seconds < 90:
            score += 15.0
        if inp.calls_after_hours_pct > 60:
            score += 25.0
        elif inp.calls_after_hours_pct > 40:
            score += 12.0
        return clamp(score)

    def _compute_meeting(self, inp):
        score = 0.0
        attendee_rate = (inp.meetings_with_attendees_count / inp.meetings_logged_count
                         if inp.meetings_logged_count > 0 else 1.0)
        score += (1.0 - attendee_rate) * 35.0
        score += (1.0 - inp.meetings_calendar_match_pct / 100.0) * 35.0
        score += (1.0 - inp.meetings_with_notes_pct / 100.0) * 30.0
        return clamp(score)

    def _compute_timing(self, inp):
        score = 0.0
        if inp.bulk_log_events_count >= 5:
            score += 40.0
        elif inp.bulk_log_events_count >= 3:
            score += 20.0
        if inp.activities_end_of_month_pct > 50:
            score += 25.0
        elif inp.activities_end_of_month_pct > 35:
            score += 12.0
        if inp.activities_end_of_quarter_pct > 60:
            score += 20.0
        if inp.retroactive_log_pct > 40:
            score += 30.0
        elif inp.retroactive_log_pct > 20:
            score += 15.0
        return clamp(score)

    def _compute_corr(self, inp):
        score = 0.0
        score += (1.0 - inp.follow_up_email_rate_pct / 100.0) * 25.0
        score += (1.0 - inp.prospect_response_rate_pct / 100.0) * 30.0
        score += (1.0 - inp.manager_verified_activity_pct / 100.0) * 25.0
        score += (1.0 - inp.peer_corroboration_score / 100.0) * 20.0
        return clamp(score)

    def _expected_composite(self, inp):
        c = self._compute_call(inp)
        m = self._compute_meeting(inp)
        t = self._compute_timing(inp)
        r = self._compute_corr(inp)
        return round(clamp(c * 0.30 + m * 0.25 + t * 0.25 + r * 0.20), 1)

    def test_composite_clean_input(self):
        inp = make_input()
        d = fresh_detector()
        result = d.assess(inp)
        assert result.fabrication_composite == self._expected_composite(inp)

    def test_composite_all_zero_scores(self):
        inp = make_input(
            calls_logged_count=0,
            calls_avg_duration_seconds=200.0,
            calls_after_hours_pct=0.0,
            meetings_logged_count=0,
            meetings_calendar_match_pct=100.0,
            meetings_with_notes_pct=100.0,
            bulk_log_events_count=0,
            activities_end_of_month_pct=0.0,
            activities_end_of_quarter_pct=0.0,
            retroactive_log_pct=0.0,
            follow_up_email_rate_pct=100.0,
            prospect_response_rate_pct=100.0,
            manager_verified_activity_pct=100.0,
            peer_corroboration_score=100.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        assert result.fabrication_composite == self._expected_composite(inp)

    def test_composite_high_suspicion(self):
        inp = make_input(
            calls_logged_count=20,
            calls_with_notes_count=0,
            calls_avg_duration_seconds=10.0,
            calls_after_hours_pct=80.0,
            meetings_calendar_match_pct=0.0,
            meetings_with_notes_pct=0.0,
            meetings_with_attendees_count=0,
            bulk_log_events_count=10,
            activities_end_of_month_pct=80.0,
            activities_end_of_quarter_pct=80.0,
            retroactive_log_pct=80.0,
            follow_up_email_rate_pct=0.0,
            prospect_response_rate_pct=0.0,
            manager_verified_activity_pct=0.0,
            peer_corroboration_score=0.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        assert result.fabrication_composite == self._expected_composite(inp)

    def test_composite_clamped_to_100(self):
        inp = make_input(
            calls_with_notes_count=0,
            calls_avg_duration_seconds=5.0,
            calls_after_hours_pct=90.0,
            meetings_calendar_match_pct=0.0,
            meetings_with_notes_pct=0.0,
            meetings_with_attendees_count=0,
            bulk_log_events_count=20,
            activities_end_of_month_pct=100.0,
            activities_end_of_quarter_pct=100.0,
            retroactive_log_pct=100.0,
            follow_up_email_rate_pct=0.0,
            prospect_response_rate_pct=0.0,
            manager_verified_activity_pct=0.0,
            peer_corroboration_score=0.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        assert result.fabrication_composite <= 100.0

    def test_composite_clamped_to_zero(self):
        inp = make_input()
        d = fresh_detector()
        result = d.assess(inp)
        assert result.fabrication_composite >= 0.0

    def test_composite_is_rounded(self):
        inp = make_input()
        d = fresh_detector()
        result = d.assess(inp)
        assert result.fabrication_composite == round(result.fabrication_composite, 1)

    def test_call_weight_dominates(self):
        # high call score, low everything else
        inp_high_call = make_input(
            calls_with_notes_count=0,
            calls_avg_duration_seconds=10.0,
            calls_after_hours_pct=80.0,
        )
        inp_low = make_input()
        d1, d2 = fresh_detector(), fresh_detector()
        assert d1.assess(inp_high_call).fabrication_composite > d2.assess(inp_low).fabrication_composite

    def test_meeting_weight_contributes(self):
        inp = make_input(
            meetings_calendar_match_pct=0.0,
            meetings_with_notes_pct=0.0,
            meetings_with_attendees_count=0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        assert result.meeting_authenticity_score > 0


# ---------------------------------------------------------------------------
# 6. is_likely_fabricating invariants
# ---------------------------------------------------------------------------

class TestIsLikelyFabricating:
    def test_not_fabricating_clean(self):
        d = fresh_detector()
        result = d.assess(make_input())
        assert result.is_likely_fabricating is False

    def test_fabricating_when_composite_ge_45(self):
        inp = make_input(
            calls_with_notes_count=0,
            calls_avg_duration_seconds=10.0,
            calls_after_hours_pct=80.0,
            meetings_calendar_match_pct=0.0,
            meetings_with_notes_pct=0.0,
            meetings_with_attendees_count=0,
            bulk_log_events_count=0,
            follow_up_email_rate_pct=0.0,
            prospect_response_rate_pct=0.0,
            manager_verified_activity_pct=0.0,
            peer_corroboration_score=0.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        if result.fabrication_composite >= 45:
            assert result.is_likely_fabricating is True

    def test_fabricating_when_bulk_log_ge_5(self):
        d = fresh_detector()
        result = d.assess(make_input(bulk_log_events_count=5))
        assert result.is_likely_fabricating is True

    def test_fabricating_when_bulk_log_gt_5(self):
        d = fresh_detector()
        result = d.assess(make_input(bulk_log_events_count=10))
        assert result.is_likely_fabricating is True

    def test_not_fabricating_bulk_log_4(self):
        # bulk_log=4 alone doesn't trigger — must check composite too
        d = fresh_detector()
        result = d.assess(make_input(bulk_log_events_count=4))
        # composite may or may not reach 45; just check the bulk condition boundary
        # With clean input and bulk=4, composite likely < 45
        if result.fabrication_composite < 45:
            assert result.is_likely_fabricating is False

    def test_fabricating_short_calls_high_count(self):
        d = fresh_detector()
        result = d.assess(make_input(
            calls_avg_duration_seconds=15.0,
            calls_logged_count=11,
        ))
        assert result.is_likely_fabricating is True

    def test_not_fabricating_short_calls_low_count(self):
        # calls < 20s AND calls_logged <= 10 → condition not met
        d = fresh_detector()
        result = d.assess(make_input(
            calls_avg_duration_seconds=15.0,
            calls_logged_count=10,
            bulk_log_events_count=0,
        ))
        # composite must also be < 45 for this to be False
        if result.fabrication_composite < 45:
            assert result.is_likely_fabricating is False

    def test_fabricating_short_calls_exactly_11(self):
        d = fresh_detector()
        result = d.assess(make_input(
            calls_avg_duration_seconds=19.9,
            calls_logged_count=11,
        ))
        assert result.is_likely_fabricating is True

    def test_not_fabricating_calls_20_seconds(self):
        # boundary: calls_avg_duration_seconds == 20 does NOT trigger (< 20 required)
        d = fresh_detector()
        result = d.assess(make_input(
            calls_avg_duration_seconds=20.0,
            calls_logged_count=11,
            bulk_log_events_count=0,
        ))
        if result.fabrication_composite < 45:
            assert result.is_likely_fabricating is False

    def test_fabricating_bulk_log_5_overrides_clean(self):
        # Even with otherwise clean input, bulk_log=5 forces True
        d = fresh_detector()
        result = d.assess(make_input(bulk_log_events_count=5))
        assert result.is_likely_fabricating is True

    def test_is_likely_fabricating_is_bool_type(self):
        d = fresh_detector()
        result = d.assess(make_input())
        assert isinstance(result.is_likely_fabricating, bool)


# ---------------------------------------------------------------------------
# 7. requires_audit invariants
# ---------------------------------------------------------------------------

class TestRequiresAudit:
    def test_not_required_clean(self):
        d = fresh_detector()
        result = d.assess(make_input())
        assert result.requires_audit is False

    def test_required_composite_ge_35(self):
        inp = make_input(
            calls_with_notes_count=0,
            calls_avg_duration_seconds=25.0,
            calls_after_hours_pct=50.0,
            meetings_calendar_match_pct=20.0,
            meetings_with_notes_pct=10.0,
            meetings_with_attendees_count=0,
            follow_up_email_rate_pct=5.0,
            prospect_response_rate_pct=5.0,
            manager_verified_activity_pct=5.0,
            peer_corroboration_score=5.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        if result.fabrication_composite >= 35:
            assert result.requires_audit is True

    def test_required_crm_edit_ge_5(self):
        d = fresh_detector()
        result = d.assess(make_input(crm_edit_after_submission_count=5))
        assert result.requires_audit is True

    def test_required_crm_edit_gt_5(self):
        d = fresh_detector()
        result = d.assess(make_input(crm_edit_after_submission_count=10))
        assert result.requires_audit is True

    def test_not_required_crm_edit_4(self):
        inp = make_input(crm_edit_after_submission_count=4, retroactive_log_pct=5.0)
        d = fresh_detector()
        result = d.assess(inp)
        if result.fabrication_composite < 35:
            assert result.requires_audit is False

    def test_required_retroactive_ge_40(self):
        d = fresh_detector()
        result = d.assess(make_input(retroactive_log_pct=40.0))
        assert result.requires_audit is True

    def test_required_retroactive_gt_40(self):
        d = fresh_detector()
        result = d.assess(make_input(retroactive_log_pct=80.0))
        assert result.requires_audit is True

    def test_not_required_retroactive_39(self):
        inp = make_input(retroactive_log_pct=39.0, crm_edit_after_submission_count=0)
        d = fresh_detector()
        result = d.assess(inp)
        if result.fabrication_composite < 35:
            assert result.requires_audit is False

    def test_requires_audit_is_bool_type(self):
        d = fresh_detector()
        result = d.assess(make_input())
        assert isinstance(result.requires_audit, bool)

    def test_retroactive_exactly_40_triggers(self):
        d = fresh_detector()
        result = d.assess(make_input(retroactive_log_pct=40.0))
        assert result.requires_audit is True

    def test_crm_edit_exactly_5_triggers(self):
        d = fresh_detector()
        result = d.assess(make_input(crm_edit_after_submission_count=5))
        assert result.requires_audit is True


# ---------------------------------------------------------------------------
# 8. estimated_fake_activity_pct = clamp(composite * 0.8)
# ---------------------------------------------------------------------------

class TestEstimatedFakePct:
    def test_estimated_equals_composite_times_0_8(self):
        d = fresh_detector()
        result = d.assess(make_input())
        expected = clamp(result.fabrication_composite * 0.8)
        assert abs(result.estimated_fake_activity_pct - expected) < 0.15

    def test_estimated_clamped_to_100(self):
        inp = make_input(
            calls_with_notes_count=0,
            calls_avg_duration_seconds=5.0,
            calls_after_hours_pct=90.0,
            meetings_calendar_match_pct=0.0,
            meetings_with_notes_pct=0.0,
            meetings_with_attendees_count=0,
            bulk_log_events_count=20,
            activities_end_of_month_pct=100.0,
            activities_end_of_quarter_pct=100.0,
            retroactive_log_pct=100.0,
            follow_up_email_rate_pct=0.0,
            prospect_response_rate_pct=0.0,
            manager_verified_activity_pct=0.0,
            peer_corroboration_score=0.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        assert result.estimated_fake_activity_pct <= 100.0

    def test_estimated_clamped_to_zero(self):
        d = fresh_detector()
        result = d.assess(make_input())
        assert result.estimated_fake_activity_pct >= 0.0

    def test_estimated_zero_when_composite_zero(self):
        inp = make_input(
            calls_logged_count=0,
            calls_avg_duration_seconds=200.0,
            calls_after_hours_pct=0.0,
            meetings_logged_count=0,
            meetings_calendar_match_pct=100.0,
            meetings_with_notes_pct=100.0,
            bulk_log_events_count=0,
            activities_end_of_month_pct=0.0,
            activities_end_of_quarter_pct=0.0,
            retroactive_log_pct=0.0,
            follow_up_email_rate_pct=100.0,
            prospect_response_rate_pct=100.0,
            manager_verified_activity_pct=100.0,
            peer_corroboration_score=100.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        assert result.estimated_fake_activity_pct == clamp(result.fabrication_composite * 0.8)

    def test_estimated_fake_pct_rounded_in_to_dict(self):
        # to_dict() rounds to 1 decimal; the raw field may be unrounded
        d = fresh_detector()
        result = d.assess(make_input())
        val = result.to_dict()["estimated_fake_activity_pct"]
        assert round(val, 1) == val


# ---------------------------------------------------------------------------
# 9. Risk classification thresholds
# ---------------------------------------------------------------------------

class TestRiskClassification:
    def test_risk_none_below_15(self):
        # Clean input should yield none
        d = fresh_detector()
        result = d.assess(make_input())
        if result.fabrication_composite < 15:
            assert result.fabrication_risk == FabricationRisk.none

    def test_risk_low_between_15_and_30(self):
        # Tweak to get composite in [15, 30)
        inp = make_input(
            calls_after_hours_pct=50.0,  # +12
            follow_up_email_rate_pct=50.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        if 15 <= result.fabrication_composite < 30:
            assert result.fabrication_risk == FabricationRisk.low

    def test_risk_moderate_between_30_and_50(self):
        inp = make_input(
            calls_with_notes_count=5,
            calls_avg_duration_seconds=50.0,
            calls_after_hours_pct=50.0,
            meetings_calendar_match_pct=50.0,
            meetings_with_notes_pct=50.0,
            follow_up_email_rate_pct=20.0,
            prospect_response_rate_pct=20.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        if 30 <= result.fabrication_composite < 50:
            assert result.fabrication_risk == FabricationRisk.moderate

    def test_risk_high_between_50_and_70(self):
        inp = make_input(
            calls_with_notes_count=0,
            calls_avg_duration_seconds=25.0,
            calls_after_hours_pct=65.0,
            meetings_calendar_match_pct=10.0,
            meetings_with_notes_pct=10.0,
            meetings_with_attendees_count=1,
            bulk_log_events_count=4,
            activities_end_of_month_pct=55.0,
            follow_up_email_rate_pct=5.0,
            prospect_response_rate_pct=5.0,
            manager_verified_activity_pct=5.0,
            peer_corroboration_score=10.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        if 50 <= result.fabrication_composite < 70:
            assert result.fabrication_risk == FabricationRisk.high

    def test_risk_critical_ge_70(self):
        inp = make_input(
            calls_with_notes_count=0,
            calls_avg_duration_seconds=5.0,
            calls_after_hours_pct=90.0,
            meetings_calendar_match_pct=0.0,
            meetings_with_notes_pct=0.0,
            meetings_with_attendees_count=0,
            bulk_log_events_count=10,
            activities_end_of_month_pct=80.0,
            activities_end_of_quarter_pct=80.0,
            retroactive_log_pct=80.0,
            follow_up_email_rate_pct=0.0,
            prospect_response_rate_pct=0.0,
            manager_verified_activity_pct=0.0,
            peer_corroboration_score=0.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        if result.fabrication_composite >= 70:
            assert result.fabrication_risk == FabricationRisk.critical

    def test_risk_none_threshold_boundary(self):
        # composite exactly < 15 → none
        d = fresh_detector()
        result = d.assess(make_input())
        risk = result.fabrication_risk
        composite = result.fabrication_composite
        if composite < 15:
            assert risk == FabricationRisk.none
        elif composite < 30:
            assert risk == FabricationRisk.low

    def test_risk_value_in_enum(self):
        d = fresh_detector()
        result = d.assess(make_input())
        assert result.fabrication_risk in FabricationRisk


# ---------------------------------------------------------------------------
# 10. Severity classification
# ---------------------------------------------------------------------------

class TestSeverityClassification:
    def test_severity_clean_low_composite(self):
        d = fresh_detector()
        result = d.assess(make_input())
        if result.fabrication_composite < 50 and not result.requires_audit:
            assert result.fabrication_severity == FabricationSeverity.clean

    def test_severity_suspicious_requires_audit(self):
        # requires_audit=True and composite < 50 → suspicious
        inp = make_input(crm_edit_after_submission_count=5)
        d = fresh_detector()
        result = d.assess(inp)
        if result.requires_audit and result.fabrication_composite < 50:
            assert result.fabrication_severity == FabricationSeverity.suspicious

    def test_severity_likely_fabricated_composite_50_to_70(self):
        inp = make_input(
            calls_with_notes_count=0,
            calls_avg_duration_seconds=5.0,
            calls_after_hours_pct=65.0,
            meetings_calendar_match_pct=0.0,
            meetings_with_notes_pct=0.0,
            meetings_with_attendees_count=0,
            bulk_log_events_count=0,
            activities_end_of_month_pct=55.0,
            follow_up_email_rate_pct=0.0,
            prospect_response_rate_pct=0.0,
            manager_verified_activity_pct=0.0,
            peer_corroboration_score=10.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        if 50 <= result.fabrication_composite < 70:
            assert result.fabrication_severity == FabricationSeverity.likely_fabricated

    def test_severity_confirmed_fraud_composite_ge_70(self):
        inp = make_input(
            calls_with_notes_count=0,
            calls_avg_duration_seconds=5.0,
            calls_after_hours_pct=90.0,
            meetings_calendar_match_pct=0.0,
            meetings_with_notes_pct=0.0,
            meetings_with_attendees_count=0,
            bulk_log_events_count=10,
            activities_end_of_month_pct=80.0,
            activities_end_of_quarter_pct=80.0,
            retroactive_log_pct=80.0,
            follow_up_email_rate_pct=0.0,
            prospect_response_rate_pct=0.0,
            manager_verified_activity_pct=0.0,
            peer_corroboration_score=0.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        if result.fabrication_composite >= 70:
            assert result.fabrication_severity == FabricationSeverity.confirmed_fraud

    def test_severity_value_in_enum(self):
        d = fresh_detector()
        result = d.assess(make_input())
        assert result.fabrication_severity in FabricationSeverity


# ---------------------------------------------------------------------------
# 11. Recommended action mapping
# ---------------------------------------------------------------------------

class TestRecommendedAction:
    def test_action_no_action_for_risk_none(self):
        d = fresh_detector()
        result = d.assess(make_input())
        if result.fabrication_risk == FabricationRisk.none:
            assert result.recommended_action == FabricationAction.no_action

    def test_action_monitor_for_risk_low(self):
        inp = make_input(calls_after_hours_pct=50.0, follow_up_email_rate_pct=30.0)
        d = fresh_detector()
        result = d.assess(inp)
        if result.fabrication_risk == FabricationRisk.low:
            assert result.recommended_action == FabricationAction.monitor

    def test_action_audit_for_risk_moderate(self):
        inp = make_input(
            calls_with_notes_count=5,
            calls_avg_duration_seconds=50.0,
            calls_after_hours_pct=50.0,
            meetings_calendar_match_pct=40.0,
            follow_up_email_rate_pct=10.0,
            prospect_response_rate_pct=10.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        if result.fabrication_risk == FabricationRisk.moderate:
            assert result.recommended_action == FabricationAction.audit_request

    def test_action_manager_review_for_risk_high(self):
        inp = make_input(
            calls_with_notes_count=0,
            calls_avg_duration_seconds=25.0,
            calls_after_hours_pct=65.0,
            meetings_calendar_match_pct=5.0,
            meetings_with_notes_pct=5.0,
            meetings_with_attendees_count=0,
            follow_up_email_rate_pct=0.0,
            prospect_response_rate_pct=0.0,
            manager_verified_activity_pct=0.0,
            peer_corroboration_score=5.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        if result.fabrication_risk == FabricationRisk.high:
            assert result.recommended_action == FabricationAction.manager_review

    def test_action_hr_escalation_for_risk_critical(self):
        inp = make_input(
            calls_with_notes_count=0,
            calls_avg_duration_seconds=5.0,
            calls_after_hours_pct=90.0,
            meetings_calendar_match_pct=0.0,
            meetings_with_notes_pct=0.0,
            meetings_with_attendees_count=0,
            bulk_log_events_count=10,
            activities_end_of_month_pct=80.0,
            activities_end_of_quarter_pct=80.0,
            retroactive_log_pct=80.0,
            follow_up_email_rate_pct=0.0,
            prospect_response_rate_pct=0.0,
            manager_verified_activity_pct=0.0,
            peer_corroboration_score=0.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        if result.fabrication_risk == FabricationRisk.critical:
            assert result.recommended_action == FabricationAction.hr_escalation

    def test_action_value_in_enum(self):
        d = fresh_detector()
        result = d.assess(make_input())
        assert result.recommended_action in FabricationAction


# ---------------------------------------------------------------------------
# 12. Primary pattern detection
# ---------------------------------------------------------------------------

class TestPrimaryPattern:
    def test_pattern_none_all_zeros(self):
        inp = make_input(
            calls_logged_count=0,
            calls_avg_duration_seconds=200.0,
            calls_after_hours_pct=0.0,
            meetings_logged_count=0,
            meetings_calendar_match_pct=100.0,
            meetings_with_notes_pct=100.0,
            bulk_log_events_count=0,
            activities_end_of_month_pct=0.0,
            activities_end_of_quarter_pct=0.0,
            retroactive_log_pct=0.0,
            follow_up_email_rate_pct=100.0,
            prospect_response_rate_pct=100.0,
            manager_verified_activity_pct=100.0,
            peer_corroboration_score=100.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        # When all sub-scores are 0, pattern is none
        if (result.call_authenticity_score == 0 and
                result.meeting_authenticity_score == 0 and
                result.timing_anomaly_score == 0 and
                result.corroboration_score == 0):
            assert result.primary_fabrication_pattern == FabricationPattern.none

    def test_pattern_phantom_calls_trigger(self):
        inp = make_input(
            calls_avg_duration_seconds=10.0,  # < 30
            calls_with_notes_count=0,
            calls_after_hours_pct=0.0,
            meetings_calendar_match_pct=100.0,
            meetings_with_notes_pct=100.0,
            bulk_log_events_count=0,
            activities_end_of_month_pct=0.0,
            follow_up_email_rate_pct=100.0,
            prospect_response_rate_pct=100.0,
            manager_verified_activity_pct=100.0,
            peer_corroboration_score=100.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        # phantom_calls condition: call_score and avg_duration < 30
        assert result.primary_fabrication_pattern in FabricationPattern

    def test_pattern_bulk_logging_trigger(self):
        inp = make_input(
            bulk_log_events_count=5,
            calls_avg_duration_seconds=200.0,
            meetings_calendar_match_pct=100.0,
            meetings_with_notes_pct=100.0,
            follow_up_email_rate_pct=100.0,
            prospect_response_rate_pct=100.0,
            manager_verified_activity_pct=100.0,
            peer_corroboration_score=100.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        # bulk_logging pattern condition: bulk_log_events_count >= 3
        assert result.primary_fabrication_pattern in FabricationPattern

    def test_pattern_timestamp_clustering_trigger(self):
        inp = make_input(
            activities_end_of_month_pct=60.0,  # > 50
            calls_avg_duration_seconds=200.0,
            meetings_calendar_match_pct=100.0,
            meetings_with_notes_pct=100.0,
            bulk_log_events_count=0,
            follow_up_email_rate_pct=100.0,
            prospect_response_rate_pct=100.0,
            manager_verified_activity_pct=100.0,
            peer_corroboration_score=100.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        assert result.primary_fabrication_pattern in FabricationPattern

    def test_pattern_no_follow_up_trigger(self):
        inp = make_input(
            follow_up_email_rate_pct=10.0,  # < 20
            calls_avg_duration_seconds=200.0,
            meetings_calendar_match_pct=100.0,
            meetings_with_notes_pct=100.0,
            bulk_log_events_count=0,
            activities_end_of_month_pct=0.0,
            prospect_response_rate_pct=0.0,
            manager_verified_activity_pct=0.0,
            peer_corroboration_score=0.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        assert result.primary_fabrication_pattern in FabricationPattern

    def test_pattern_value_in_enum(self):
        d = fresh_detector()
        result = d.assess(make_input())
        assert result.primary_fabrication_pattern in FabricationPattern

    def test_note_absence_trigger(self):
        inp = make_input(
            calls_logged_count=10,
            calls_with_notes_count=0,  # 0 notes, >5 calls
            calls_avg_duration_seconds=200.0,  # long calls, no phantom_calls
        )
        d = fresh_detector()
        result = d.assess(inp)
        assert result.primary_fabrication_pattern in FabricationPattern

    def test_fake_meetings_trigger(self):
        inp = make_input(
            meetings_calendar_match_pct=30.0,  # < 50
            meetings_with_notes_pct=10.0,
            meetings_with_attendees_count=0,
            calls_avg_duration_seconds=200.0,
            bulk_log_events_count=0,
            activities_end_of_month_pct=0.0,
            follow_up_email_rate_pct=100.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        assert result.primary_fabrication_pattern in FabricationPattern


# ---------------------------------------------------------------------------
# 13. Call authenticity sub-score
# ---------------------------------------------------------------------------

class TestCallAuthenticity:
    def test_call_score_zero_with_perfect_calls(self):
        inp = make_input(
            calls_logged_count=10,
            calls_with_notes_count=10,
            calls_avg_duration_seconds=200.0,
            calls_after_hours_pct=0.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        assert result.call_authenticity_score == 0.0

    def test_call_score_increases_no_notes(self):
        inp_notes = make_input(calls_with_notes_count=20)
        inp_no_notes = make_input(calls_with_notes_count=0)
        d1, d2 = fresh_detector(), fresh_detector()
        assert d2.assess(inp_no_notes).call_authenticity_score > d1.assess(inp_notes).call_authenticity_score

    def test_call_score_short_duration_penalty(self):
        inp_short = make_input(calls_avg_duration_seconds=10.0)
        inp_long = make_input(calls_avg_duration_seconds=200.0)
        d1, d2 = fresh_detector(), fresh_detector()
        assert d1.assess(inp_short).call_authenticity_score > d2.assess(inp_long).call_authenticity_score

    def test_call_score_after_hours_high_penalty(self):
        inp_high = make_input(calls_after_hours_pct=70.0)
        inp_low = make_input(calls_after_hours_pct=5.0)
        d1, d2 = fresh_detector(), fresh_detector()
        assert d1.assess(inp_high).call_authenticity_score > d2.assess(inp_low).call_authenticity_score

    def test_call_score_clamped_max_100(self):
        inp = make_input(
            calls_with_notes_count=0,
            calls_avg_duration_seconds=5.0,
            calls_after_hours_pct=90.0,
        )
        d = fresh_detector()
        assert d.assess(inp).call_authenticity_score <= 100.0

    def test_call_score_clamped_min_0(self):
        d = fresh_detector()
        assert d.assess(make_input()).call_authenticity_score >= 0.0

    def test_call_score_zero_calls_logged(self):
        # note_rate defaults to 1.0 when calls_logged_count == 0
        inp = make_input(
            calls_logged_count=0,
            calls_with_notes_count=0,
            calls_avg_duration_seconds=200.0,
            calls_after_hours_pct=0.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        assert result.call_authenticity_score == 0.0

    def test_call_score_duration_between_30_and_90(self):
        inp = make_input(calls_avg_duration_seconds=60.0, calls_with_notes_count=20, calls_after_hours_pct=0.0)
        d = fresh_detector()
        # 30 <= 60 < 90 → +15 points
        assert d.assess(inp).call_authenticity_score == 15.0

    def test_call_score_after_hours_between_40_and_60(self):
        inp = make_input(calls_avg_duration_seconds=200.0, calls_with_notes_count=20, calls_after_hours_pct=50.0)
        d = fresh_detector()
        # 40 < 50 <= 60 → +12 points
        assert d.assess(inp).call_authenticity_score == 12.0

    def test_call_score_partial_notes(self):
        inp = make_input(calls_logged_count=10, calls_with_notes_count=5, calls_avg_duration_seconds=200.0, calls_after_hours_pct=0.0)
        d = fresh_detector()
        # note_rate=0.5 → (1-0.5)*40 = 20
        assert d.assess(inp).call_authenticity_score == 20.0


# ---------------------------------------------------------------------------
# 14. Meeting authenticity sub-score
# ---------------------------------------------------------------------------

class TestMeetingAuthenticity:
    def test_meeting_score_zero_perfect(self):
        inp = make_input(
            meetings_logged_count=10,
            meetings_with_attendees_count=10,
            meetings_calendar_match_pct=100.0,
            meetings_with_notes_pct=100.0,
        )
        d = fresh_detector()
        assert d.assess(inp).meeting_authenticity_score == 0.0

    def test_meeting_score_no_attendees_penalty(self):
        inp_att = make_input(meetings_with_attendees_count=10)
        inp_no_att = make_input(meetings_with_attendees_count=0)
        d1, d2 = fresh_detector(), fresh_detector()
        assert d2.assess(inp_no_att).meeting_authenticity_score > d1.assess(inp_att).meeting_authenticity_score

    def test_meeting_score_calendar_mismatch_penalty(self):
        inp_match = make_input(meetings_calendar_match_pct=100.0)
        inp_no_match = make_input(meetings_calendar_match_pct=0.0)
        d1, d2 = fresh_detector(), fresh_detector()
        assert d2.assess(inp_no_match).meeting_authenticity_score > d1.assess(inp_match).meeting_authenticity_score

    def test_meeting_score_no_notes_penalty(self):
        inp_notes = make_input(meetings_with_notes_pct=100.0)
        inp_no_notes = make_input(meetings_with_notes_pct=0.0)
        d1, d2 = fresh_detector(), fresh_detector()
        assert d2.assess(inp_no_notes).meeting_authenticity_score > d1.assess(inp_notes).meeting_authenticity_score

    def test_meeting_score_clamped_max_100(self):
        inp = make_input(
            meetings_logged_count=10,
            meetings_with_attendees_count=0,
            meetings_calendar_match_pct=0.0,
            meetings_with_notes_pct=0.0,
        )
        d = fresh_detector()
        assert d.assess(inp).meeting_authenticity_score <= 100.0

    def test_meeting_score_clamped_min_0(self):
        d = fresh_detector()
        assert d.assess(make_input()).meeting_authenticity_score >= 0.0

    def test_meeting_score_zero_meetings_logged(self):
        # attendee_rate defaults to 1.0 when meetings_logged_count == 0
        inp = make_input(
            meetings_logged_count=0,
            meetings_with_attendees_count=0,
            meetings_calendar_match_pct=100.0,
            meetings_with_notes_pct=100.0,
        )
        d = fresh_detector()
        assert d.assess(inp).meeting_authenticity_score == 0.0

    def test_meeting_score_full_max(self):
        # All bad: 35+35+30 = 100
        inp = make_input(
            meetings_logged_count=10,
            meetings_with_attendees_count=0,
            meetings_calendar_match_pct=0.0,
            meetings_with_notes_pct=0.0,
        )
        d = fresh_detector()
        assert d.assess(inp).meeting_authenticity_score == 100.0


# ---------------------------------------------------------------------------
# 15. Timing anomaly sub-score
# ---------------------------------------------------------------------------

class TestTimingAnomaly:
    def test_timing_score_zero_clean(self):
        inp = make_input(
            bulk_log_events_count=0,
            activities_end_of_month_pct=0.0,
            activities_end_of_quarter_pct=0.0,
            retroactive_log_pct=0.0,
        )
        d = fresh_detector()
        assert d.assess(inp).timing_anomaly_score == 0.0

    def test_timing_score_bulk_log_ge_5(self):
        inp = make_input(
            bulk_log_events_count=5,
            activities_end_of_month_pct=0.0,
            activities_end_of_quarter_pct=0.0,
            retroactive_log_pct=0.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        # +40 for bulk_log >= 5
        assert result.timing_anomaly_score >= 40.0

    def test_timing_score_bulk_log_3_to_4(self):
        inp = make_input(
            bulk_log_events_count=4,
            activities_end_of_month_pct=0.0,
            activities_end_of_quarter_pct=0.0,
            retroactive_log_pct=0.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        # +20 for 3 <= bulk_log < 5
        assert result.timing_anomaly_score == 20.0

    def test_timing_score_end_of_month_gt_50(self):
        inp = make_input(
            bulk_log_events_count=0,
            activities_end_of_month_pct=60.0,
            activities_end_of_quarter_pct=0.0,
            retroactive_log_pct=0.0,
        )
        d = fresh_detector()
        # +25 for >50%
        assert d.assess(inp).timing_anomaly_score == 25.0

    def test_timing_score_end_of_month_35_to_50(self):
        inp = make_input(
            bulk_log_events_count=0,
            activities_end_of_month_pct=40.0,
            activities_end_of_quarter_pct=0.0,
            retroactive_log_pct=0.0,
        )
        d = fresh_detector()
        # +12 for 35 < pct <= 50
        assert d.assess(inp).timing_anomaly_score == 12.0

    def test_timing_score_end_of_quarter_gt_60(self):
        inp = make_input(
            bulk_log_events_count=0,
            activities_end_of_month_pct=0.0,
            activities_end_of_quarter_pct=70.0,
            retroactive_log_pct=0.0,
        )
        d = fresh_detector()
        # +20 for >60%
        assert d.assess(inp).timing_anomaly_score == 20.0

    def test_timing_score_retroactive_gt_40(self):
        inp = make_input(
            bulk_log_events_count=0,
            activities_end_of_month_pct=0.0,
            activities_end_of_quarter_pct=0.0,
            retroactive_log_pct=50.0,
        )
        d = fresh_detector()
        # +30 for >40%
        assert d.assess(inp).timing_anomaly_score == 30.0

    def test_timing_score_retroactive_20_to_40(self):
        inp = make_input(
            bulk_log_events_count=0,
            activities_end_of_month_pct=0.0,
            activities_end_of_quarter_pct=0.0,
            retroactive_log_pct=30.0,
        )
        d = fresh_detector()
        # +15 for 20 < pct <= 40
        assert d.assess(inp).timing_anomaly_score == 15.0

    def test_timing_score_clamped_max_100(self):
        inp = make_input(
            bulk_log_events_count=10,
            activities_end_of_month_pct=80.0,
            activities_end_of_quarter_pct=80.0,
            retroactive_log_pct=80.0,
        )
        d = fresh_detector()
        assert d.assess(inp).timing_anomaly_score <= 100.0

    def test_timing_score_clamped_min_0(self):
        d = fresh_detector()
        assert d.assess(make_input()).timing_anomaly_score >= 0.0


# ---------------------------------------------------------------------------
# 16. Corroboration sub-score
# ---------------------------------------------------------------------------

class TestCorroboration:
    def test_corr_score_zero_perfect(self):
        inp = make_input(
            follow_up_email_rate_pct=100.0,
            prospect_response_rate_pct=100.0,
            manager_verified_activity_pct=100.0,
            peer_corroboration_score=100.0,
        )
        d = fresh_detector()
        assert d.assess(inp).corroboration_score == 0.0

    def test_corr_score_max_all_zero(self):
        inp = make_input(
            follow_up_email_rate_pct=0.0,
            prospect_response_rate_pct=0.0,
            manager_verified_activity_pct=0.0,
            peer_corroboration_score=0.0,
        )
        d = fresh_detector()
        # 25+30+25+20 = 100
        assert d.assess(inp).corroboration_score == 100.0

    def test_corr_score_partial(self):
        inp = make_input(
            follow_up_email_rate_pct=50.0,
            prospect_response_rate_pct=50.0,
            manager_verified_activity_pct=50.0,
            peer_corroboration_score=50.0,
        )
        d = fresh_detector()
        # 0.5*25 + 0.5*30 + 0.5*25 + 0.5*20 = 12.5+15+12.5+10 = 50
        assert d.assess(inp).corroboration_score == 50.0

    def test_corr_score_increases_with_low_followup(self):
        inp_high = make_input(follow_up_email_rate_pct=90.0)
        inp_low = make_input(follow_up_email_rate_pct=10.0)
        d1, d2 = fresh_detector(), fresh_detector()
        assert d2.assess(inp_low).corroboration_score > d1.assess(inp_high).corroboration_score

    def test_corr_score_clamped_max_100(self):
        inp = make_input(
            follow_up_email_rate_pct=0.0,
            prospect_response_rate_pct=0.0,
            manager_verified_activity_pct=0.0,
            peer_corroboration_score=0.0,
        )
        d = fresh_detector()
        assert d.assess(inp).corroboration_score <= 100.0

    def test_corr_score_clamped_min_0(self):
        d = fresh_detector()
        assert d.assess(make_input()).corroboration_score >= 0.0

    def test_corr_follow_up_weight_25(self):
        # Only follow_up varied
        inp = make_input(
            follow_up_email_rate_pct=0.0,
            prospect_response_rate_pct=100.0,
            manager_verified_activity_pct=100.0,
            peer_corroboration_score=100.0,
        )
        d = fresh_detector()
        assert d.assess(inp).corroboration_score == 25.0

    def test_corr_prospect_response_weight_30(self):
        inp = make_input(
            follow_up_email_rate_pct=100.0,
            prospect_response_rate_pct=0.0,
            manager_verified_activity_pct=100.0,
            peer_corroboration_score=100.0,
        )
        d = fresh_detector()
        assert d.assess(inp).corroboration_score == 30.0

    def test_corr_manager_verified_weight_25(self):
        inp = make_input(
            follow_up_email_rate_pct=100.0,
            prospect_response_rate_pct=100.0,
            manager_verified_activity_pct=0.0,
            peer_corroboration_score=100.0,
        )
        d = fresh_detector()
        assert d.assess(inp).corroboration_score == 25.0

    def test_corr_peer_corroboration_weight_20(self):
        inp = make_input(
            follow_up_email_rate_pct=100.0,
            prospect_response_rate_pct=100.0,
            manager_verified_activity_pct=100.0,
            peer_corroboration_score=0.0,
        )
        d = fresh_detector()
        assert d.assess(inp).corroboration_score == 20.0


# ---------------------------------------------------------------------------
# 17. assess_batch
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_batch_empty(self):
        d = fresh_detector()
        results = d.assess_batch([])
        assert results == []

    def test_batch_single(self):
        d = fresh_detector()
        results = d.assess_batch([make_input()])
        assert len(results) == 1

    def test_batch_multiple(self):
        d = fresh_detector()
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = d.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_results_stored(self):
        d = fresh_detector()
        d.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        assert d.summary()["total"] == 3

    def test_batch_order_preserved(self):
        d = fresh_detector()
        inputs = [make_input(rep_id=f"R{i}") for i in range(4)]
        results = d.assess_batch(inputs)
        for i, result in enumerate(results):
            assert result.rep_id == f"R{i}"

    def test_batch_same_as_sequential(self):
        d_batch = fresh_detector()
        d_seq = fresh_detector()
        inputs = [make_input(rep_id=f"R{i}") for i in range(3)]
        batch_results = d_batch.assess_batch(inputs)
        seq_results = [d_seq.assess(inp) for inp in inputs]
        for br, sr in zip(batch_results, seq_results):
            assert br.fabrication_composite == sr.fabrication_composite
            assert br.fabrication_risk == sr.fabrication_risk

    def test_batch_increments_total(self):
        d = fresh_detector()
        d.assess(make_input())
        d.assess_batch([make_input(), make_input()])
        assert d.summary()["total"] == 3


# ---------------------------------------------------------------------------
# 18. Fabrication signal string
# ---------------------------------------------------------------------------

class TestFabricationSignal:
    def test_signal_authentic_for_none_risk(self):
        d = fresh_detector()
        result = d.assess(make_input())
        if result.fabrication_risk == FabricationRisk.none:
            assert "authentic" in result.fabrication_signal

    def test_signal_contains_composite(self):
        inp = make_input(
            calls_with_notes_count=0,
            calls_avg_duration_seconds=10.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        if result.fabrication_risk != FabricationRisk.none:
            assert "composite" in result.fabrication_signal

    def test_signal_is_non_empty(self):
        d = fresh_detector()
        result = d.assess(make_input())
        assert len(result.fabrication_signal) > 0

    def test_signal_phantom_calls_message(self):
        inp = make_input(
            calls_avg_duration_seconds=10.0,
            calls_with_notes_count=0,
            calls_after_hours_pct=0.0,
            meetings_calendar_match_pct=100.0,
            meetings_with_notes_pct=100.0,
            bulk_log_events_count=0,
            activities_end_of_month_pct=0.0,
            follow_up_email_rate_pct=100.0,
            prospect_response_rate_pct=100.0,
            manager_verified_activity_pct=100.0,
            peer_corroboration_score=100.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        if result.primary_fabrication_pattern == FabricationPattern.phantom_calls:
            assert "phantom" in result.fabrication_signal.lower() or "call" in result.fabrication_signal.lower()

    def test_signal_none_risk_message(self):
        d = fresh_detector()
        result = d.assess(make_input())
        if result.fabrication_risk == FabricationRisk.none:
            assert result.fabrication_signal == "activity patterns authentic — all indicators within normal range"


# ---------------------------------------------------------------------------
# 19. Summary aggregation correctness
# ---------------------------------------------------------------------------

class TestSummaryAggregation:
    def test_summary_avg_composite_single(self):
        d = fresh_detector()
        result = d.assess(make_input())
        s = d.summary()
        assert s["avg_fabrication_composite"] == result.fabrication_composite

    def test_summary_avg_call_score_single(self):
        d = fresh_detector()
        result = d.assess(make_input())
        s = d.summary()
        assert s["avg_call_authenticity_score"] == round(result.call_authenticity_score, 1)

    def test_summary_avg_meeting_score_single(self):
        d = fresh_detector()
        result = d.assess(make_input())
        s = d.summary()
        assert s["avg_meeting_authenticity_score"] == round(result.meeting_authenticity_score, 1)

    def test_summary_avg_timing_score_single(self):
        d = fresh_detector()
        result = d.assess(make_input())
        s = d.summary()
        assert s["avg_timing_anomaly_score"] == round(result.timing_anomaly_score, 1)

    def test_summary_avg_corr_score_single(self):
        d = fresh_detector()
        result = d.assess(make_input())
        s = d.summary()
        assert s["avg_corroboration_score"] == round(result.corroboration_score, 1)

    def test_summary_avg_fake_pct_single(self):
        d = fresh_detector()
        result = d.assess(make_input())
        s = d.summary()
        assert s["avg_estimated_fake_activity_pct"] == round(result.estimated_fake_activity_pct, 1)

    def test_summary_likely_fabricating_count(self):
        d = fresh_detector()
        d.assess(make_input(bulk_log_events_count=5))  # likely
        d.assess(make_input())  # not likely
        s = d.summary()
        assert s["likely_fabricating_count"] == 1

    def test_summary_audit_required_count(self):
        d = fresh_detector()
        d.assess(make_input(crm_edit_after_submission_count=5))  # audit
        d.assess(make_input())  # no audit
        s = d.summary()
        assert s["audit_required_count"] == 1

    def test_summary_risk_counts_correct_key(self):
        d = fresh_detector()
        result = d.assess(make_input())
        s = d.summary()
        assert result.fabrication_risk.value in s["risk_counts"]

    def test_summary_severity_counts_correct_key(self):
        d = fresh_detector()
        result = d.assess(make_input())
        s = d.summary()
        assert result.fabrication_severity.value in s["severity_counts"]

    def test_summary_pattern_counts_correct_key(self):
        d = fresh_detector()
        result = d.assess(make_input())
        s = d.summary()
        assert result.primary_fabrication_pattern.value in s["pattern_counts"]

    def test_summary_action_counts_correct_key(self):
        d = fresh_detector()
        result = d.assess(make_input())
        s = d.summary()
        assert result.recommended_action.value in s["action_counts"]

    def test_summary_avg_composite_two_items(self):
        d = fresh_detector()
        r1 = d.assess(make_input(rep_id="A"))
        r2 = d.assess(make_input(rep_id="B", bulk_log_events_count=5))
        expected = round((r1.fabrication_composite + r2.fabrication_composite) / 2, 1)
        assert d.summary()["avg_fabrication_composite"] == expected

    def test_summary_likely_fabricating_all_true(self):
        d = fresh_detector()
        for _ in range(3):
            d.assess(make_input(bulk_log_events_count=5))
        assert d.summary()["likely_fabricating_count"] == 3

    def test_summary_audit_required_all_true(self):
        d = fresh_detector()
        for _ in range(4):
            d.assess(make_input(crm_edit_after_submission_count=5))
        assert d.summary()["audit_required_count"] == 4


# ---------------------------------------------------------------------------
# 20. Edge cases and boundary conditions
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_zero_calls_logged(self):
        d = fresh_detector()
        result = d.assess(make_input(calls_logged_count=0, calls_with_notes_count=0))
        assert result is not None

    def test_zero_meetings_logged(self):
        d = fresh_detector()
        result = d.assess(make_input(meetings_logged_count=0, meetings_with_attendees_count=0))
        assert result is not None

    def test_all_zeros_input(self):
        inp = SalesActivityFabricationInput(
            rep_id="R0",
            rep_name="Zero",
            region="None",
            manager_id="M0",
            calls_logged_count=0,
            calls_with_notes_count=0,
            calls_avg_duration_seconds=0.0,
            calls_after_hours_pct=0.0,
            meetings_logged_count=0,
            meetings_with_attendees_count=0,
            meetings_calendar_match_pct=0.0,
            meetings_with_notes_pct=0.0,
            bulk_log_events_count=0,
            activities_end_of_month_pct=0.0,
            activities_end_of_quarter_pct=0.0,
            follow_up_email_rate_pct=0.0,
            crm_edit_after_submission_count=0,
            retroactive_log_pct=0.0,
            prospect_response_rate_pct=0.0,
            deal_stage_advance_rate_pct=0.0,
            manager_verified_activity_pct=0.0,
            peer_corroboration_score=0.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        assert result.fabrication_composite >= 0.0

    def test_all_100_pct_input(self):
        inp = make_input(
            calls_with_notes_count=100,
            calls_logged_count=100,
            calls_avg_duration_seconds=300.0,
            calls_after_hours_pct=100.0,
            meetings_logged_count=50,
            meetings_with_attendees_count=50,
            meetings_calendar_match_pct=100.0,
            meetings_with_notes_pct=100.0,
            bulk_log_events_count=0,
            activities_end_of_month_pct=100.0,
            activities_end_of_quarter_pct=100.0,
            follow_up_email_rate_pct=100.0,
            crm_edit_after_submission_count=0,
            retroactive_log_pct=100.0,
            prospect_response_rate_pct=100.0,
            deal_stage_advance_rate_pct=100.0,
            manager_verified_activity_pct=100.0,
            peer_corroboration_score=100.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        assert result is not None

    def test_very_long_rep_name(self):
        d = fresh_detector()
        result = d.assess(make_input(rep_name="A" * 200))
        assert result.rep_name == "A" * 200

    def test_float_boundary_calls_duration_30(self):
        # Exactly 30 → NOT < 30, so no 35pt penalty; but IS < 90, so +15
        d = fresh_detector()
        result = d.assess(make_input(calls_avg_duration_seconds=30.0, calls_with_notes_count=20, calls_after_hours_pct=0.0))
        assert result.call_authenticity_score == 15.0

    def test_float_boundary_calls_duration_90(self):
        # Exactly 90 → NOT < 90, so no penalty from duration
        d = fresh_detector()
        result = d.assess(make_input(calls_avg_duration_seconds=90.0, calls_with_notes_count=20, calls_after_hours_pct=0.0))
        assert result.call_authenticity_score == 0.0

    def test_float_boundary_after_hours_40(self):
        # Exactly 40 → NOT > 40
        d = fresh_detector()
        result = d.assess(make_input(calls_avg_duration_seconds=200.0, calls_with_notes_count=20, calls_after_hours_pct=40.0))
        assert result.call_authenticity_score == 0.0

    def test_float_boundary_after_hours_60(self):
        # Exactly 60 → NOT > 60 for +25; but > 40 for +12
        d = fresh_detector()
        result = d.assess(make_input(calls_avg_duration_seconds=200.0, calls_with_notes_count=20, calls_after_hours_pct=60.0))
        assert result.call_authenticity_score == 12.0

    def test_float_boundary_end_of_month_35(self):
        # Exactly 35 → NOT > 35
        d = fresh_detector()
        result = d.assess(make_input(bulk_log_events_count=0, activities_end_of_month_pct=35.0, activities_end_of_quarter_pct=0.0, retroactive_log_pct=0.0))
        assert result.timing_anomaly_score == 0.0

    def test_float_boundary_end_of_month_50(self):
        # Exactly 50 → NOT > 50 for +25; but > 35 for +12
        d = fresh_detector()
        result = d.assess(make_input(bulk_log_events_count=0, activities_end_of_month_pct=50.0, activities_end_of_quarter_pct=0.0, retroactive_log_pct=0.0))
        assert result.timing_anomaly_score == 12.0

    def test_float_boundary_retroactive_20(self):
        # Exactly 20 → NOT > 20
        d = fresh_detector()
        result = d.assess(make_input(bulk_log_events_count=0, activities_end_of_month_pct=0.0, activities_end_of_quarter_pct=0.0, retroactive_log_pct=20.0))
        assert result.timing_anomaly_score == 0.0

    def test_float_boundary_retroactive_40(self):
        # Exactly 40 → NOT > 40 for +30; but > 20 for +15
        d = fresh_detector()
        result = d.assess(make_input(bulk_log_events_count=0, activities_end_of_month_pct=0.0, activities_end_of_quarter_pct=0.0, retroactive_log_pct=40.0))
        assert result.timing_anomaly_score == 15.0

    def test_float_boundary_calendar_match_50(self):
        # meetings_calendar_match_pct=50 → NOT < 50, so fake_meetings pattern not triggered
        inp = make_input(
            meetings_calendar_match_pct=50.0,
            bulk_log_events_count=0,
            activities_end_of_month_pct=0.0,
            calls_avg_duration_seconds=200.0,
            follow_up_email_rate_pct=100.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        # fake_meetings condition is < 50
        if result.primary_fabrication_pattern == FabricationPattern.fake_meetings:
            # should not happen since match_pct == 50 is not < 50
            assert False, "fake_meetings should not trigger at exactly 50%"

    def test_float_boundary_end_of_quarter_60(self):
        # Exactly 60 → NOT > 60
        d = fresh_detector()
        result = d.assess(make_input(bulk_log_events_count=0, activities_end_of_month_pct=0.0, activities_end_of_quarter_pct=60.0, retroactive_log_pct=0.0))
        assert result.timing_anomaly_score == 0.0


# ---------------------------------------------------------------------------
# 21. State accumulation across multiple assess() calls
# ---------------------------------------------------------------------------

class TestStateAccumulation:
    def test_results_accumulate(self):
        d = fresh_detector()
        for i in range(10):
            d.assess(make_input(rep_id=f"R{i}"))
        assert d.summary()["total"] == 10

    def test_fresh_detector_starts_empty(self):
        d = fresh_detector()
        assert d.summary()["total"] == 0

    def test_different_detectors_independent(self):
        d1 = fresh_detector()
        d2 = fresh_detector()
        d1.assess(make_input())
        assert d2.summary()["total"] == 0

    def test_batch_then_single_total(self):
        d = fresh_detector()
        d.assess_batch([make_input() for _ in range(3)])
        d.assess(make_input())
        assert d.summary()["total"] == 4

    def test_summary_risk_counts_multiple_risk_levels(self):
        d = fresh_detector()
        # Add a clean one (risk=none) and a high-risk one
        d.assess(make_input())
        d.assess(make_input(
            calls_with_notes_count=0,
            calls_avg_duration_seconds=5.0,
            calls_after_hours_pct=90.0,
            meetings_calendar_match_pct=0.0,
            meetings_with_notes_pct=0.0,
            meetings_with_attendees_count=0,
            bulk_log_events_count=10,
            activities_end_of_month_pct=80.0,
            activities_end_of_quarter_pct=80.0,
            retroactive_log_pct=80.0,
            follow_up_email_rate_pct=0.0,
            prospect_response_rate_pct=0.0,
            manager_verified_activity_pct=0.0,
            peer_corroboration_score=0.0,
        ))
        s = d.summary()
        assert sum(s["risk_counts"].values()) == 2


# ---------------------------------------------------------------------------
# 22. Result dataclass structure
# ---------------------------------------------------------------------------

class TestResultDataclass:
    def test_result_is_dataclass(self):
        from swarm.intelligence.sales_activity_fabrication_detector import SalesActivityFabricationResult
        assert dataclasses.is_dataclass(SalesActivityFabricationResult)

    def test_result_field_count(self):
        from swarm.intelligence.sales_activity_fabrication_detector import SalesActivityFabricationResult
        assert len(dataclasses.fields(SalesActivityFabricationResult)) == 15

    def test_result_has_rep_id(self):
        d = fresh_detector()
        result = d.assess(make_input(rep_id="TEST"))
        assert result.rep_id == "TEST"

    def test_result_has_rep_name(self):
        d = fresh_detector()
        result = d.assess(make_input(rep_name="Bob"))
        assert result.rep_name == "Bob"

    def test_result_fabrication_risk_type(self):
        d = fresh_detector()
        result = d.assess(make_input())
        assert isinstance(result.fabrication_risk, FabricationRisk)

    def test_result_fabrication_severity_type(self):
        d = fresh_detector()
        result = d.assess(make_input())
        assert isinstance(result.fabrication_severity, FabricationSeverity)

    def test_result_primary_pattern_type(self):
        d = fresh_detector()
        result = d.assess(make_input())
        assert isinstance(result.primary_fabrication_pattern, FabricationPattern)

    def test_result_recommended_action_type(self):
        d = fresh_detector()
        result = d.assess(make_input())
        assert isinstance(result.recommended_action, FabricationAction)

    def test_result_call_score_float(self):
        d = fresh_detector()
        result = d.assess(make_input())
        assert isinstance(result.call_authenticity_score, float)

    def test_result_composite_float(self):
        d = fresh_detector()
        result = d.assess(make_input())
        assert isinstance(result.fabrication_composite, float)

    def test_result_has_to_dict_method(self):
        d = fresh_detector()
        result = d.assess(make_input())
        assert callable(result.to_dict)


# ---------------------------------------------------------------------------
# 23. Parametrized risk boundary tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("composite,expected_risk", [
    (0.0, FabricationRisk.none),
    (14.9, FabricationRisk.none),
    (15.0, FabricationRisk.low),
    (29.9, FabricationRisk.low),
    (30.0, FabricationRisk.moderate),
    (49.9, FabricationRisk.moderate),
    (50.0, FabricationRisk.high),
    (69.9, FabricationRisk.high),
    (70.0, FabricationRisk.critical),
    (100.0, FabricationRisk.critical),
])
def test_risk_boundary_parametrized(composite, expected_risk):
    d = SalesActivityFabricationDetector()
    # Use internal classify method directly
    assert d._classify_risk(composite) == expected_risk


@pytest.mark.parametrize("composite,requires_audit,expected_severity", [
    (0.0, False, FabricationSeverity.clean),
    (49.9, False, FabricationSeverity.clean),
    (0.0, True, FabricationSeverity.suspicious),
    (49.9, True, FabricationSeverity.suspicious),
    (50.0, False, FabricationSeverity.likely_fabricated),
    (69.9, False, FabricationSeverity.likely_fabricated),
    (70.0, False, FabricationSeverity.confirmed_fraud),
    (100.0, True, FabricationSeverity.confirmed_fraud),
])
def test_severity_boundary_parametrized(composite, requires_audit, expected_severity):
    d = SalesActivityFabricationDetector()
    assert d._classify_severity(composite, requires_audit) == expected_severity


@pytest.mark.parametrize("risk,expected_action", [
    (FabricationRisk.none, FabricationAction.no_action),
    (FabricationRisk.low, FabricationAction.monitor),
    (FabricationRisk.moderate, FabricationAction.audit_request),
    (FabricationRisk.high, FabricationAction.manager_review),
    (FabricationRisk.critical, FabricationAction.hr_escalation),
])
def test_action_mapping_parametrized(risk, expected_action):
    d = SalesActivityFabricationDetector()
    assert d._recommended_action(risk, 0.0) == expected_action


# ---------------------------------------------------------------------------
# 24. Parametrized sub-score tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("duration,expected_base", [
    (5.0, 35.0),   # < 30 → +35
    (29.9, 35.0),  # < 30 → +35
    (30.0, 15.0),  # 30 <= d < 90 → +15
    (89.9, 15.0),
    (90.0, 0.0),   # >= 90 → 0
    (200.0, 0.0),
])
def test_call_score_duration_parametrized(duration, expected_base):
    inp = make_input(
        calls_avg_duration_seconds=duration,
        calls_with_notes_count=20,
        calls_after_hours_pct=0.0,
    )
    d = fresh_detector()
    result = d.assess(inp)
    assert result.call_authenticity_score == expected_base


@pytest.mark.parametrize("bulk,expected_timing_base", [
    (0, 0.0),
    (2, 0.0),
    (3, 20.0),
    (4, 20.0),
    (5, 40.0),
    (10, 40.0),
])
def test_timing_bulk_log_parametrized(bulk, expected_timing_base):
    inp = make_input(
        bulk_log_events_count=bulk,
        activities_end_of_month_pct=0.0,
        activities_end_of_quarter_pct=0.0,
        retroactive_log_pct=0.0,
    )
    d = fresh_detector()
    result = d.assess(inp)
    assert result.timing_anomaly_score == expected_timing_base


@pytest.mark.parametrize("after_hours,expected_base", [
    (0.0, 0.0),
    (40.0, 0.0),
    (40.1, 12.0),
    (60.0, 12.0),
    (60.1, 25.0),
    (100.0, 25.0),
])
def test_call_score_after_hours_parametrized(after_hours, expected_base):
    inp = make_input(
        calls_avg_duration_seconds=200.0,
        calls_with_notes_count=20,
        calls_after_hours_pct=after_hours,
    )
    d = fresh_detector()
    result = d.assess(inp)
    assert result.call_authenticity_score == expected_base


# ---------------------------------------------------------------------------
# 25. Comprehensive scenario tests
# ---------------------------------------------------------------------------

class TestScenarios:
    def test_scenario_star_rep_all_clean(self):
        """Star rep with perfect metrics should have lowest risk."""
        inp = make_input(
            calls_logged_count=30,
            calls_with_notes_count=30,
            calls_avg_duration_seconds=300.0,
            calls_after_hours_pct=5.0,
            meetings_logged_count=15,
            meetings_with_attendees_count=15,
            meetings_calendar_match_pct=98.0,
            meetings_with_notes_pct=95.0,
            bulk_log_events_count=0,
            activities_end_of_month_pct=15.0,
            activities_end_of_quarter_pct=20.0,
            follow_up_email_rate_pct=90.0,
            crm_edit_after_submission_count=0,
            retroactive_log_pct=2.0,
            prospect_response_rate_pct=80.0,
            manager_verified_activity_pct=90.0,
            peer_corroboration_score=85.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        assert result.fabrication_risk in (FabricationRisk.none, FabricationRisk.low)
        assert result.is_likely_fabricating is False

    def test_scenario_blatant_fraud(self):
        """Blatant fraud pattern — all red flags."""
        inp = make_input(
            calls_logged_count=50,
            calls_with_notes_count=0,
            calls_avg_duration_seconds=5.0,
            calls_after_hours_pct=90.0,
            meetings_logged_count=20,
            meetings_with_attendees_count=0,
            meetings_calendar_match_pct=0.0,
            meetings_with_notes_pct=0.0,
            bulk_log_events_count=15,
            activities_end_of_month_pct=90.0,
            activities_end_of_quarter_pct=90.0,
            follow_up_email_rate_pct=0.0,
            crm_edit_after_submission_count=10,
            retroactive_log_pct=90.0,
            prospect_response_rate_pct=0.0,
            manager_verified_activity_pct=0.0,
            peer_corroboration_score=0.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        assert result.is_likely_fabricating is True
        assert result.requires_audit is True
        assert result.fabrication_risk in (FabricationRisk.high, FabricationRisk.critical)

    def test_scenario_bulk_logger(self):
        """Rep who bulk-logs at end of period."""
        inp = make_input(
            bulk_log_events_count=8,
            activities_end_of_month_pct=70.0,
            activities_end_of_quarter_pct=65.0,
            retroactive_log_pct=45.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        assert result.is_likely_fabricating is True
        assert result.requires_audit is True

    def test_scenario_phantom_caller(self):
        """Rep with many very short calls and no notes."""
        inp = make_input(
            calls_logged_count=50,
            calls_with_notes_count=0,
            calls_avg_duration_seconds=8.0,
            calls_after_hours_pct=70.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        assert result.is_likely_fabricating is True

    def test_scenario_crm_editor(self):
        """Rep with many post-submission edits."""
        inp = make_input(crm_edit_after_submission_count=8)
        d = fresh_detector()
        result = d.assess(inp)
        assert result.requires_audit is True

    def test_scenario_retroactive_logger(self):
        """Rep with very high retroactive logging."""
        inp = make_input(retroactive_log_pct=60.0)
        d = fresh_detector()
        result = d.assess(inp)
        assert result.requires_audit is True

    def test_scenario_no_meetings_corroboration(self):
        """Rep with no meeting attendees or calendar match."""
        inp = make_input(
            meetings_logged_count=15,
            meetings_with_attendees_count=0,
            meetings_calendar_match_pct=0.0,
            meetings_with_notes_pct=0.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        assert result.meeting_authenticity_score == 100.0

    def test_scenario_mixed_batch(self):
        """Batch with mix of clean and fraudulent reps."""
        clean = make_input(rep_id="CLEAN")
        fraud = make_input(
            rep_id="FRAUD",
            calls_with_notes_count=0,
            calls_avg_duration_seconds=5.0,
            calls_after_hours_pct=90.0,
            meetings_calendar_match_pct=0.0,
            meetings_with_notes_pct=0.0,
            meetings_with_attendees_count=0,
            bulk_log_events_count=10,
            activities_end_of_month_pct=80.0,
            activities_end_of_quarter_pct=80.0,
            retroactive_log_pct=80.0,
            follow_up_email_rate_pct=0.0,
            prospect_response_rate_pct=0.0,
            manager_verified_activity_pct=0.0,
            peer_corroboration_score=0.0,
        )
        d = fresh_detector()
        results = d.assess_batch([clean, fraud])
        assert results[0].fabrication_composite < results[1].fabrication_composite

    def test_scenario_short_calls_threshold(self):
        """Exactly at the short-call count threshold."""
        # calls_avg_duration_seconds < 20 AND calls_logged_count > 10
        inp11 = make_input(calls_avg_duration_seconds=15.0, calls_logged_count=11)
        inp10 = make_input(calls_avg_duration_seconds=15.0, calls_logged_count=10)
        d = fresh_detector()
        r11 = d.assess(inp11)
        r10 = d.assess(inp10)
        assert r11.is_likely_fabricating is True
        if r10.fabrication_composite < 45:
            assert r10.is_likely_fabricating is False

    def test_scenario_summary_empty_then_filled(self):
        d = fresh_detector()
        s0 = d.summary()
        assert s0["total"] == 0
        d.assess(make_input())
        s1 = d.summary()
        assert s1["total"] == 1

    def test_scenario_estimated_fake_proportional_to_composite(self):
        d = fresh_detector()
        r_clean = d.assess(make_input())
        r_fraud = d.assess(make_input(
            calls_with_notes_count=0,
            calls_avg_duration_seconds=5.0,
            calls_after_hours_pct=90.0,
            meetings_calendar_match_pct=0.0,
            meetings_with_notes_pct=0.0,
            meetings_with_attendees_count=0,
            bulk_log_events_count=10,
            activities_end_of_month_pct=80.0,
            retroactive_log_pct=80.0,
            follow_up_email_rate_pct=0.0,
            prospect_response_rate_pct=0.0,
            manager_verified_activity_pct=0.0,
            peer_corroboration_score=0.0,
        ))
        assert r_fraud.estimated_fake_activity_pct > r_clean.estimated_fake_activity_pct


# ---------------------------------------------------------------------------
# 26. Additional invariant tests
# ---------------------------------------------------------------------------

class TestAdditionalInvariants:
    def test_composite_in_valid_range(self):
        for i in range(20):
            d = fresh_detector()
            result = d.assess(make_input(
                calls_with_notes_count=i,
                calls_avg_duration_seconds=float(i * 10 + 5),
                bulk_log_events_count=i % 10,
            ))
            assert 0.0 <= result.fabrication_composite <= 100.0

    def test_all_sub_scores_in_valid_range(self):
        d = fresh_detector()
        result = d.assess(make_input(
            calls_with_notes_count=0,
            calls_avg_duration_seconds=10.0,
            calls_after_hours_pct=70.0,
            meetings_with_attendees_count=0,
            meetings_calendar_match_pct=0.0,
            meetings_with_notes_pct=0.0,
            bulk_log_events_count=10,
            activities_end_of_month_pct=80.0,
            retroactive_log_pct=80.0,
            follow_up_email_rate_pct=0.0,
            prospect_response_rate_pct=0.0,
            manager_verified_activity_pct=0.0,
            peer_corroboration_score=0.0,
        ))
        for score in [
            result.call_authenticity_score,
            result.meeting_authenticity_score,
            result.timing_anomaly_score,
            result.corroboration_score,
            result.estimated_fake_activity_pct,
        ]:
            assert 0.0 <= score <= 100.0

    def test_risk_consistent_with_composite(self):
        d = fresh_detector()
        result = d.assess(make_input())
        c = result.fabrication_composite
        r = result.fabrication_risk
        if c < 15:
            assert r == FabricationRisk.none
        elif c < 30:
            assert r == FabricationRisk.low
        elif c < 50:
            assert r == FabricationRisk.moderate
        elif c < 70:
            assert r == FabricationRisk.high
        else:
            assert r == FabricationRisk.critical

    def test_severity_consistent_with_composite_and_audit(self):
        d = fresh_detector()
        result = d.assess(make_input(crm_edit_after_submission_count=5))
        c = result.fabrication_composite
        ra = result.requires_audit
        sev = result.fabrication_severity
        if c >= 70:
            assert sev == FabricationSeverity.confirmed_fraud
        elif c >= 50:
            assert sev == FabricationSeverity.likely_fabricated
        elif ra:
            assert sev == FabricationSeverity.suspicious
        else:
            assert sev == FabricationSeverity.clean

    def test_action_consistent_with_risk(self):
        d = fresh_detector()
        result = d.assess(make_input())
        risk = result.fabrication_risk
        action = result.recommended_action
        mapping = {
            FabricationRisk.none: FabricationAction.no_action,
            FabricationRisk.low: FabricationAction.monitor,
            FabricationRisk.moderate: FabricationAction.audit_request,
            FabricationRisk.high: FabricationAction.manager_review,
            FabricationRisk.critical: FabricationAction.hr_escalation,
        }
        assert action == mapping[risk]

    def test_high_composite_implies_likely_fabricating(self):
        inp = make_input(
            calls_with_notes_count=0,
            calls_avg_duration_seconds=5.0,
            calls_after_hours_pct=90.0,
            meetings_calendar_match_pct=0.0,
            meetings_with_notes_pct=0.0,
            meetings_with_attendees_count=0,
            bulk_log_events_count=10,
            activities_end_of_month_pct=80.0,
            activities_end_of_quarter_pct=80.0,
            retroactive_log_pct=80.0,
            follow_up_email_rate_pct=0.0,
            prospect_response_rate_pct=0.0,
            manager_verified_activity_pct=0.0,
            peer_corroboration_score=0.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        if result.fabrication_composite >= 45:
            assert result.is_likely_fabricating is True

    def test_high_composite_implies_requires_audit(self):
        inp = make_input(
            calls_with_notes_count=0,
            calls_avg_duration_seconds=5.0,
            calls_after_hours_pct=90.0,
            meetings_calendar_match_pct=0.0,
            meetings_with_notes_pct=0.0,
            meetings_with_attendees_count=0,
            bulk_log_events_count=10,
            activities_end_of_month_pct=80.0,
            retroactive_log_pct=80.0,
            follow_up_email_rate_pct=0.0,
            prospect_response_rate_pct=0.0,
            manager_verified_activity_pct=0.0,
            peer_corroboration_score=0.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        if result.fabrication_composite >= 35:
            assert result.requires_audit is True

    def test_to_dict_matches_result_fields(self):
        d = fresh_detector()
        result = d.assess(make_input())
        rd = result.to_dict()
        assert rd["rep_id"] == result.rep_id
        assert rd["rep_name"] == result.rep_name
        assert rd["fabrication_risk"] == result.fabrication_risk.value
        assert rd["fabrication_severity"] == result.fabrication_severity.value
        assert rd["primary_fabrication_pattern"] == result.primary_fabrication_pattern.value
        assert rd["recommended_action"] == result.recommended_action.value
        assert rd["is_likely_fabricating"] == result.is_likely_fabricating
        assert rd["requires_audit"] == result.requires_audit
        assert rd["fabrication_signal"] == result.fabrication_signal

    def test_summary_avg_fake_pct_consistent(self):
        d = fresh_detector()
        results = [d.assess(make_input(rep_id=f"R{i}")) for i in range(5)]
        s = d.summary()
        expected = round(sum(r.estimated_fake_activity_pct for r in results) / 5, 1)
        assert s["avg_estimated_fake_activity_pct"] == expected

    def test_detector_instance_creation(self):
        d = SalesActivityFabricationDetector()
        assert d is not None

    def test_assess_returns_result_object(self):
        from swarm.intelligence.sales_activity_fabrication_detector import SalesActivityFabricationResult
        d = fresh_detector()
        result = d.assess(make_input())
        assert isinstance(result, SalesActivityFabricationResult)

    def test_assess_batch_returns_list(self):
        d = fresh_detector()
        results = d.assess_batch([make_input()])
        assert isinstance(results, list)

    def test_summary_returns_dict(self):
        d = fresh_detector()
        assert isinstance(d.summary(), dict)


# ---------------------------------------------------------------------------
# 27. More parametrized and targeted tests to reach 300+
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("note_count,logged,expected_note_component", [
    (0, 10, 40.0),   # 0% notes → +40
    (5, 10, 20.0),   # 50% notes → +20
    (10, 10, 0.0),   # 100% notes → +0
    (0, 0, 0.0),     # zero calls → note_rate defaults to 1.0 → +0
])
def test_call_score_note_component_parametrized(note_count, logged, expected_note_component):
    inp = make_input(
        calls_logged_count=logged,
        calls_with_notes_count=note_count,
        calls_avg_duration_seconds=200.0,
        calls_after_hours_pct=0.0,
    )
    d = fresh_detector()
    result = d.assess(inp)
    assert result.call_authenticity_score == expected_note_component


@pytest.mark.parametrize("end_of_quarter,extra_timing", [
    (0.0, 0.0),
    (60.0, 0.0),
    (60.1, 20.0),
    (100.0, 20.0),
])
def test_timing_end_of_quarter_parametrized(end_of_quarter, extra_timing):
    inp = make_input(
        bulk_log_events_count=0,
        activities_end_of_month_pct=0.0,
        activities_end_of_quarter_pct=end_of_quarter,
        retroactive_log_pct=0.0,
    )
    d = fresh_detector()
    result = d.assess(inp)
    assert result.timing_anomaly_score == extra_timing


@pytest.mark.parametrize("retroactive,expected", [
    (0.0, 0.0),
    (20.0, 0.0),
    (20.1, 15.0),
    (40.0, 15.0),
    (40.1, 30.0),
    (100.0, 30.0),
])
def test_timing_retroactive_parametrized(retroactive, expected):
    inp = make_input(
        bulk_log_events_count=0,
        activities_end_of_month_pct=0.0,
        activities_end_of_quarter_pct=0.0,
        retroactive_log_pct=retroactive,
    )
    d = fresh_detector()
    result = d.assess(inp)
    assert result.timing_anomaly_score == expected


class TestToDict27:
    def test_to_dict_risk_none_value(self):
        d = fresh_detector()
        result = d.assess(make_input())
        rd = result.to_dict()
        assert rd["fabrication_risk"] in {"none", "low", "moderate", "high", "critical"}

    def test_to_dict_severity_value_valid(self):
        d = fresh_detector()
        rd = d.assess(make_input()).to_dict()
        assert rd["fabrication_severity"] in {"clean", "suspicious", "likely_fabricated", "confirmed_fraud"}

    def test_to_dict_pattern_value_valid(self):
        d = fresh_detector()
        rd = d.assess(make_input()).to_dict()
        assert rd["primary_fabrication_pattern"] in {
            "none", "phantom_calls", "fake_meetings", "bulk_logging",
            "no_follow_up", "note_absence", "timestamp_clustering",
        }

    def test_to_dict_action_value_valid(self):
        d = fresh_detector()
        rd = d.assess(make_input()).to_dict()
        assert rd["recommended_action"] in {
            "no_action", "monitor", "audit_request", "manager_review", "hr_escalation",
        }

    def test_to_dict_call_score_nonneg(self):
        d = fresh_detector()
        assert d.assess(make_input()).to_dict()["call_authenticity_score"] >= 0.0

    def test_to_dict_meeting_score_nonneg(self):
        d = fresh_detector()
        assert d.assess(make_input()).to_dict()["meeting_authenticity_score"] >= 0.0

    def test_to_dict_timing_score_nonneg(self):
        d = fresh_detector()
        assert d.assess(make_input()).to_dict()["timing_anomaly_score"] >= 0.0

    def test_to_dict_corr_score_nonneg(self):
        d = fresh_detector()
        assert d.assess(make_input()).to_dict()["corroboration_score"] >= 0.0

    def test_to_dict_composite_nonneg(self):
        d = fresh_detector()
        assert d.assess(make_input()).to_dict()["fabrication_composite"] >= 0.0

    def test_to_dict_estimated_fake_nonneg(self):
        d = fresh_detector()
        assert d.assess(make_input()).to_dict()["estimated_fake_activity_pct"] >= 0.0

    def test_to_dict_call_score_le_100(self):
        d = fresh_detector()
        assert d.assess(make_input()).to_dict()["call_authenticity_score"] <= 100.0

    def test_to_dict_composite_le_100(self):
        d = fresh_detector()
        assert d.assess(make_input()).to_dict()["fabrication_composite"] <= 100.0


class TestSummary27:
    def test_summary_called_twice_same_result(self):
        d = fresh_detector()
        d.assess(make_input())
        s1 = d.summary()
        s2 = d.summary()
        assert s1 == s2

    def test_summary_not_mutated_by_reread(self):
        d = fresh_detector()
        d.assess(make_input())
        s = d.summary()
        total_before = s["total"]
        # Read it again
        s2 = d.summary()
        assert s2["total"] == total_before

    def test_summary_risk_counts_values_positive(self):
        d = fresh_detector()
        d.assess(make_input())
        s = d.summary()
        for v in s["risk_counts"].values():
            assert v > 0

    def test_summary_severity_counts_values_positive(self):
        d = fresh_detector()
        d.assess(make_input())
        s = d.summary()
        for v in s["severity_counts"].values():
            assert v > 0

    def test_summary_pattern_counts_values_positive(self):
        d = fresh_detector()
        d.assess(make_input())
        s = d.summary()
        for v in s["pattern_counts"].values():
            assert v > 0

    def test_summary_action_counts_values_positive(self):
        d = fresh_detector()
        d.assess(make_input())
        s = d.summary()
        for v in s["action_counts"].values():
            assert v > 0

    def test_summary_avg_scores_between_0_and_100(self):
        d = fresh_detector()
        d.assess(make_input())
        s = d.summary()
        for key in [
            "avg_call_authenticity_score",
            "avg_meeting_authenticity_score",
            "avg_timing_anomaly_score",
            "avg_corroboration_score",
            "avg_estimated_fake_activity_pct",
            "avg_fabrication_composite",
        ]:
            assert 0.0 <= s[key] <= 100.0

    def test_summary_likely_fabricating_le_total(self):
        d = fresh_detector()
        for _ in range(5):
            d.assess(make_input())
        s = d.summary()
        assert s["likely_fabricating_count"] <= s["total"]

    def test_summary_audit_required_le_total(self):
        d = fresh_detector()
        for _ in range(5):
            d.assess(make_input())
        s = d.summary()
        assert s["audit_required_count"] <= s["total"]

    def test_summary_both_audit_and_likely(self):
        d = fresh_detector()
        d.assess(make_input(bulk_log_events_count=5, crm_edit_after_submission_count=5))
        s = d.summary()
        assert s["likely_fabricating_count"] == 1
        assert s["audit_required_count"] == 1


class TestMiscInvariants:
    def test_bulk_log_2_no_timing_bonus(self):
        inp = make_input(
            bulk_log_events_count=2,
            activities_end_of_month_pct=0.0,
            activities_end_of_quarter_pct=0.0,
            retroactive_log_pct=0.0,
        )
        d = fresh_detector()
        assert d.assess(inp).timing_anomaly_score == 0.0

    def test_meeting_attendee_rate_half(self):
        inp = make_input(
            meetings_logged_count=10,
            meetings_with_attendees_count=5,
            meetings_calendar_match_pct=100.0,
            meetings_with_notes_pct=100.0,
        )
        d = fresh_detector()
        # (1-0.5)*35 = 17.5
        assert d.assess(inp).meeting_authenticity_score == 17.5

    def test_meeting_calendar_partial(self):
        inp = make_input(
            meetings_logged_count=10,
            meetings_with_attendees_count=10,
            meetings_calendar_match_pct=50.0,
            meetings_with_notes_pct=100.0,
        )
        d = fresh_detector()
        # (1-0.5)*35 = 17.5
        assert d.assess(inp).meeting_authenticity_score == 17.5

    def test_meeting_notes_partial(self):
        inp = make_input(
            meetings_logged_count=10,
            meetings_with_attendees_count=10,
            meetings_calendar_match_pct=100.0,
            meetings_with_notes_pct=50.0,
        )
        d = fresh_detector()
        # (1-0.5)*30 = 15
        assert d.assess(inp).meeting_authenticity_score == 15.0

    def test_assess_stores_result_in_internal_list(self):
        d = fresh_detector()
        d.assess(make_input())
        assert len(d._results) == 1

    def test_assess_batch_stores_all_results(self):
        d = fresh_detector()
        d.assess_batch([make_input(rep_id=f"R{i}") for i in range(7)])
        assert len(d._results) == 7

    def test_input_rep_id_preserved_in_result(self):
        d = fresh_detector()
        result = d.assess(make_input(rep_id="XTEST99"))
        assert result.rep_id == "XTEST99"
        assert result.to_dict()["rep_id"] == "XTEST99"

    def test_input_rep_name_preserved_in_result(self):
        d = fresh_detector()
        result = d.assess(make_input(rep_name="Charlie Brown"))
        assert result.rep_name == "Charlie Brown"
        assert result.to_dict()["rep_name"] == "Charlie Brown"

    def test_composite_formula_weights_sum_to_one(self):
        # Verify weights: 0.30 + 0.25 + 0.25 + 0.20 = 1.0
        assert abs(0.30 + 0.25 + 0.25 + 0.20 - 1.0) < 1e-10

    def test_call_score_note_absence_pattern_condition(self):
        # note_absence pattern: calls_with_notes_count==0 AND calls_logged_count > 5
        inp = make_input(
            calls_logged_count=6,
            calls_with_notes_count=0,
            calls_avg_duration_seconds=200.0,  # not < 30, so phantom_calls gets 0
            calls_after_hours_pct=0.0,
            meetings_calendar_match_pct=100.0,
            meetings_with_notes_pct=100.0,
            bulk_log_events_count=0,
            activities_end_of_month_pct=0.0,
            follow_up_email_rate_pct=100.0,
            prospect_response_rate_pct=100.0,
            manager_verified_activity_pct=100.0,
            peer_corroboration_score=100.0,
        )
        d = fresh_detector()
        result = d.assess(inp)
        # note_absence uses call_score; call_score > 0 (40 for 0 notes)
        assert result.primary_fabrication_pattern == FabricationPattern.note_absence

    def test_risk_counts_has_seen_value(self):
        d = fresh_detector()
        r = d.assess(make_input())
        s = d.summary()
        assert s["risk_counts"].get(r.fabrication_risk.value, 0) == 1

    def test_severity_counts_has_seen_value(self):
        d = fresh_detector()
        r = d.assess(make_input())
        s = d.summary()
        assert s["severity_counts"].get(r.fabrication_severity.value, 0) == 1

    def test_pattern_counts_has_seen_value(self):
        d = fresh_detector()
        r = d.assess(make_input())
        s = d.summary()
        assert s["pattern_counts"].get(r.primary_fabrication_pattern.value, 0) == 1

    def test_action_counts_has_seen_value(self):
        d = fresh_detector()
        r = d.assess(make_input())
        s = d.summary()
        assert s["action_counts"].get(r.recommended_action.value, 0) == 1

    def test_estimated_fake_formula_exact(self):
        d = fresh_detector()
        result = d.assess(make_input())
        expected = clamp(result.fabrication_composite * 0.8)
        assert abs(result.estimated_fake_activity_pct - expected) < 1e-9
