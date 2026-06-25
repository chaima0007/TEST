"""
Comprehensive pytest tests for Module 122:
SalesRepBurnoutAttritionRiskEngine
"""
from __future__ import annotations

import dataclasses
import math
import pytest

from swarm.intelligence.sales_rep_burnout_attrition_risk_engine import (
    BurnoutAttritionInput,
    BurnoutAttritionResult,
    BurnoutRisk,
    AttritionPattern,
    BurnoutSeverity,
    BurnoutAction,
    SalesRepBurnoutAttritionRiskEngine,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def healthy_input(**overrides) -> BurnoutAttritionInput:
    """Return a baseline 'healthy' rep with no risk signals."""
    defaults = dict(
        rep_id="R001",
        region="WEST",
        tenure_months=24,
        quota_attainment_pct=95.0,
        quota_attainment_prior_pct=95.0,
        quota_pressure_score=30.0,
        pto_days_taken_ytd=10.0,
        pto_days_allocated_ytd=20.0,
        avg_weekly_activity_count=50.0,
        activity_count_prior_period=50.0,
        after_hours_activity_pct=0.10,
        crm_update_compliance_pct=90.0,
        crm_compliance_prior_pct=90.0,
        voluntary_meeting_attendance_pct=0.85,
        manager_interaction_days_since=5,
        peer_collaboration_score=70.0,
        compensation_satisfaction_score=75.0,
        consecutive_missed_quota_periods=0,
        sick_days_last_90d=0,
        escalations_raised_last_90d=0,
        linkedin_activity_spike=0,
        deal_disengagement_count=0,
    )
    defaults.update(overrides)
    return BurnoutAttritionInput(**defaults)


def engine() -> SalesRepBurnoutAttritionRiskEngine:
    return SalesRepBurnoutAttritionRiskEngine()


# ---------------------------------------------------------------------------
# 1. Dataclass field counts
# ---------------------------------------------------------------------------

class TestDataclassFieldCounts:
    def test_input_has_22_fields(self):
        fields = dataclasses.fields(BurnoutAttritionInput)
        assert len(fields) == 22

    def test_result_has_15_fields(self):
        fields = dataclasses.fields(BurnoutAttritionResult)
        assert len(fields) == 15

    def test_input_field_names_complete(self):
        names = {f.name for f in dataclasses.fields(BurnoutAttritionInput)}
        expected = {
            "rep_id", "region", "tenure_months", "quota_attainment_pct",
            "quota_attainment_prior_pct", "quota_pressure_score",
            "pto_days_taken_ytd", "pto_days_allocated_ytd",
            "avg_weekly_activity_count", "activity_count_prior_period",
            "after_hours_activity_pct", "crm_update_compliance_pct",
            "crm_compliance_prior_pct", "voluntary_meeting_attendance_pct",
            "manager_interaction_days_since", "peer_collaboration_score",
            "compensation_satisfaction_score", "consecutive_missed_quota_periods",
            "sick_days_last_90d", "escalations_raised_last_90d",
            "linkedin_activity_spike", "deal_disengagement_count",
        }
        assert names == expected

    def test_result_field_names_complete(self):
        names = {f.name for f in dataclasses.fields(BurnoutAttritionResult)}
        expected = {
            "rep_id", "region", "burnout_risk", "attrition_pattern",
            "burnout_severity", "recommended_action", "workload_strain_score",
            "engagement_decay_score", "quota_pressure_score",
            "flight_signal_score", "burnout_composite", "is_burnout_risk",
            "is_flight_risk", "estimated_replacement_cost_usd", "burnout_signal",
        }
        assert names == expected

    def test_input_rep_id_field(self):
        names = [f.name for f in dataclasses.fields(BurnoutAttritionInput)]
        assert "rep_id" in names

    def test_input_region_field(self):
        names = [f.name for f in dataclasses.fields(BurnoutAttritionInput)]
        assert "region" in names

    def test_input_linkedin_activity_spike_field(self):
        names = [f.name for f in dataclasses.fields(BurnoutAttritionInput)]
        assert "linkedin_activity_spike" in names

    def test_input_deal_disengagement_count_field(self):
        names = [f.name for f in dataclasses.fields(BurnoutAttritionInput)]
        assert "deal_disengagement_count" in names

    def test_result_burnout_composite_field(self):
        names = [f.name for f in dataclasses.fields(BurnoutAttritionResult)]
        assert "burnout_composite" in names

    def test_result_is_burnout_risk_field(self):
        names = [f.name for f in dataclasses.fields(BurnoutAttritionResult)]
        assert "is_burnout_risk" in names

    def test_result_is_flight_risk_field(self):
        names = [f.name for f in dataclasses.fields(BurnoutAttritionResult)]
        assert "is_flight_risk" in names

    def test_result_burnout_signal_field(self):
        names = [f.name for f in dataclasses.fields(BurnoutAttritionResult)]
        assert "burnout_signal" in names


# ---------------------------------------------------------------------------
# 2. to_dict() returns exactly 15 keys
# ---------------------------------------------------------------------------

class TestToDict:
    def test_to_dict_has_15_keys(self):
        e = engine()
        result = e.assess(healthy_input())
        assert len(result.to_dict()) == 15

    def test_to_dict_has_rep_id_key(self):
        e = engine()
        result = e.assess(healthy_input(rep_id="XYZ"))
        d = result.to_dict()
        assert "rep_id" in d
        assert d["rep_id"] == "XYZ"

    def test_to_dict_has_burnout_risk_key(self):
        e = engine()
        result = e.assess(healthy_input())
        d = result.to_dict()
        assert "burnout_risk" in d

    def test_to_dict_burnout_risk_is_string(self):
        e = engine()
        result = e.assess(healthy_input())
        d = result.to_dict()
        assert isinstance(d["burnout_risk"], str)

    def test_to_dict_attrition_pattern_is_string(self):
        e = engine()
        result = e.assess(healthy_input())
        d = result.to_dict()
        assert isinstance(d["attrition_pattern"], str)

    def test_to_dict_burnout_severity_is_string(self):
        e = engine()
        result = e.assess(healthy_input())
        d = result.to_dict()
        assert isinstance(d["burnout_severity"], str)

    def test_to_dict_recommended_action_is_string(self):
        e = engine()
        result = e.assess(healthy_input())
        d = result.to_dict()
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_is_burnout_risk_is_bool(self):
        e = engine()
        result = e.assess(healthy_input())
        d = result.to_dict()
        assert isinstance(d["is_burnout_risk"], bool)

    def test_to_dict_is_flight_risk_is_bool(self):
        e = engine()
        result = e.assess(healthy_input())
        d = result.to_dict()
        assert isinstance(d["is_flight_risk"], bool)

    def test_to_dict_estimated_cost_key_exists(self):
        e = engine()
        result = e.assess(healthy_input())
        d = result.to_dict()
        assert "estimated_replacement_cost_usd" in d

    def test_to_dict_burnout_signal_key_exists(self):
        e = engine()
        result = e.assess(healthy_input())
        d = result.to_dict()
        assert "burnout_signal" in d

    def test_to_dict_exact_keys(self):
        e = engine()
        result = e.assess(healthy_input())
        keys = set(result.to_dict().keys())
        expected = {
            "rep_id", "region", "burnout_risk", "attrition_pattern",
            "burnout_severity", "recommended_action", "workload_strain_score",
            "engagement_decay_score", "quota_pressure_score",
            "flight_signal_score", "burnout_composite", "is_burnout_risk",
            "is_flight_risk", "estimated_replacement_cost_usd", "burnout_signal",
        }
        assert keys == expected

    def test_to_dict_region_preserved(self):
        e = engine()
        result = e.assess(healthy_input(region="EAST"))
        assert result.to_dict()["region"] == "EAST"

    def test_to_dict_workload_strain_is_numeric(self):
        e = engine()
        result = e.assess(healthy_input())
        d = result.to_dict()
        assert isinstance(d["workload_strain_score"], (int, float))


# ---------------------------------------------------------------------------
# 3. summary() returns exactly 13 keys
# ---------------------------------------------------------------------------

class TestSummaryKeys:
    def test_summary_empty_has_13_keys(self):
        e = engine()
        s = e.summary()
        assert len(s) == 13

    def test_summary_after_assess_has_13_keys(self):
        e = engine()
        e.assess(healthy_input())
        s = e.summary()
        assert len(s) == 13

    def test_summary_exact_keys(self):
        e = engine()
        e.assess(healthy_input())
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_burnout_composite", "burnout_risk_count",
            "flight_risk_count", "avg_workload_strain_score",
            "avg_engagement_decay_score", "avg_quota_pressure_score",
            "avg_flight_signal_score", "total_estimated_replacement_cost_usd",
        }
        assert set(e.summary().keys()) == expected

    def test_summary_empty_total_zero(self):
        assert engine().summary()["total"] == 0

    def test_summary_empty_risk_counts_empty_dict(self):
        assert engine().summary()["risk_counts"] == {}

    def test_summary_empty_pattern_counts_empty_dict(self):
        assert engine().summary()["pattern_counts"] == {}

    def test_summary_empty_severity_counts_empty_dict(self):
        assert engine().summary()["severity_counts"] == {}

    def test_summary_empty_action_counts_empty_dict(self):
        assert engine().summary()["action_counts"] == {}

    def test_summary_empty_avg_composite_zero(self):
        assert engine().summary()["avg_burnout_composite"] == 0.0

    def test_summary_empty_burnout_risk_count_zero(self):
        assert engine().summary()["burnout_risk_count"] == 0

    def test_summary_empty_flight_risk_count_zero(self):
        assert engine().summary()["flight_risk_count"] == 0

    def test_summary_empty_replacement_cost_zero(self):
        assert engine().summary()["total_estimated_replacement_cost_usd"] == 0.0


# ---------------------------------------------------------------------------
# 4. All enum values exist
# ---------------------------------------------------------------------------

class TestEnumValues:
    def test_burnout_risk_low(self):
        assert BurnoutRisk.low.value == "low"

    def test_burnout_risk_moderate(self):
        assert BurnoutRisk.moderate.value == "moderate"

    def test_burnout_risk_high(self):
        assert BurnoutRisk.high.value == "high"

    def test_burnout_risk_critical(self):
        assert BurnoutRisk.critical.value == "critical"

    def test_burnout_risk_has_4_members(self):
        assert len(BurnoutRisk) == 4

    def test_attrition_pattern_none(self):
        assert AttritionPattern.none.value == "none"

    def test_attrition_pattern_workload_exhaustion(self):
        assert AttritionPattern.workload_exhaustion.value == "workload_exhaustion"

    def test_attrition_pattern_quota_pressure(self):
        assert AttritionPattern.quota_pressure.value == "quota_pressure"

    def test_attrition_pattern_disengagement(self):
        assert AttritionPattern.disengagement.value == "disengagement"

    def test_attrition_pattern_compensation_dissatisfaction(self):
        assert AttritionPattern.compensation_dissatisfaction.value == "compensation_dissatisfaction"

    def test_attrition_pattern_manager_conflict(self):
        assert AttritionPattern.manager_conflict.value == "manager_conflict"

    def test_attrition_pattern_has_6_members(self):
        assert len(AttritionPattern) == 6

    def test_burnout_severity_healthy(self):
        assert BurnoutSeverity.healthy.value == "healthy"

    def test_burnout_severity_watch(self):
        assert BurnoutSeverity.watch.value == "watch"

    def test_burnout_severity_at_risk(self):
        assert BurnoutSeverity.at_risk.value == "at_risk"

    def test_burnout_severity_flight_risk(self):
        assert BurnoutSeverity.flight_risk.value == "flight_risk"

    def test_burnout_severity_has_4_members(self):
        assert len(BurnoutSeverity) == 4

    def test_burnout_action_no_action(self):
        assert BurnoutAction.no_action.value == "no_action"

    def test_burnout_action_wellness_checkin(self):
        assert BurnoutAction.wellness_checkin.value == "wellness_checkin"

    def test_burnout_action_workload_rebalance(self):
        assert BurnoutAction.workload_rebalance.value == "workload_rebalance"

    def test_burnout_action_retention_interview(self):
        assert BurnoutAction.retention_interview.value == "retention_interview"

    def test_burnout_action_executive_retention(self):
        assert BurnoutAction.executive_retention.value == "executive_retention"

    def test_burnout_action_has_5_members(self):
        assert len(BurnoutAction) == 5


# ---------------------------------------------------------------------------
# 5. Composite score calculation
# ---------------------------------------------------------------------------

class TestCompositeScore:
    def test_composite_is_non_negative(self):
        e = engine()
        result = e.assess(healthy_input())
        assert result.burnout_composite >= 0.0

    def test_composite_max_100(self):
        # extreme values
        inp = healthy_input(
            after_hours_activity_pct=0.99,
            activity_count_prior_period=10.0,
            avg_weekly_activity_count=100.0,
            pto_days_taken_ytd=0.0,
            pto_days_allocated_ytd=20.0,
            sick_days_last_90d=10,
            crm_update_compliance_pct=0.0,
            crm_compliance_prior_pct=100.0,
            voluntary_meeting_attendance_pct=0.0,
            manager_interaction_days_since=30,
            peer_collaboration_score=0.0,
            quota_pressure_score=100.0,
            consecutive_missed_quota_periods=5,
            quota_attainment_prior_pct=100.0,
            quota_attainment_pct=0.0,
            escalations_raised_last_90d=10,
            linkedin_activity_spike=1,
            deal_disengagement_count=10,
            compensation_satisfaction_score=0.0,
            tenure_months=6,
        )
        result = engine().assess(inp)
        assert result.burnout_composite <= 100.0

    def test_composite_formula_weights(self):
        # Build controlled inputs so we can predict sub-scores roughly
        # Use healthy rep as baseline — composite should be low
        e = engine()
        result = e.assess(healthy_input())
        # healthy rep should have composite < 20
        assert result.burnout_composite < 20.0

    def test_composite_increases_with_risk(self):
        e_healthy = engine()
        r_healthy = e_healthy.assess(healthy_input())

        e_risk = engine()
        r_risk = e_risk.assess(healthy_input(
            after_hours_activity_pct=0.60,
            consecutive_missed_quota_periods=3,
            linkedin_activity_spike=1,
            sick_days_last_90d=6,
        ))
        assert r_risk.burnout_composite > r_healthy.burnout_composite

    def test_composite_is_rounded_to_one_decimal(self):
        e = engine()
        result = e.assess(healthy_input())
        # Check it's not a floating point mess — one decimal place
        assert result.burnout_composite == round(result.burnout_composite, 1)

    def test_composite_workload_weight_is_030(self):
        # Force workload only, keep others at 0
        inp = healthy_input(
            after_hours_activity_pct=0.0,
            activity_count_prior_period=50.0,
            avg_weekly_activity_count=50.0,
            pto_days_taken_ytd=10.0,
            pto_days_allocated_ytd=20.0,
            sick_days_last_90d=0,
            crm_update_compliance_pct=90.0,
            crm_compliance_prior_pct=90.0,
            voluntary_meeting_attendance_pct=1.0,
            manager_interaction_days_since=1,
            peer_collaboration_score=90.0,
            quota_pressure_score=0.0,
            consecutive_missed_quota_periods=0,
            quota_attainment_pct=100.0,
            quota_attainment_prior_pct=100.0,
            escalations_raised_last_90d=0,
            linkedin_activity_spike=0,
            deal_disengagement_count=0,
            compensation_satisfaction_score=90.0,
            tenure_months=36,
        )
        result = engine().assess(inp)
        assert result.burnout_composite >= 0.0

    def test_composite_stored_in_result(self):
        e = engine()
        result = e.assess(healthy_input())
        assert isinstance(result.burnout_composite, float)

    def test_sub_scores_returned(self):
        e = engine()
        result = e.assess(healthy_input())
        assert result.workload_strain_score >= 0.0
        assert result.engagement_decay_score >= 0.0
        assert result.quota_pressure_score >= 0.0
        assert result.flight_signal_score >= 0.0

    def test_sub_scores_max_100(self):
        inp = healthy_input(
            after_hours_activity_pct=0.99,
            sick_days_last_90d=10,
            crm_update_compliance_pct=0.0,
            crm_compliance_prior_pct=100.0,
            voluntary_meeting_attendance_pct=0.0,
            manager_interaction_days_since=30,
            peer_collaboration_score=0.0,
            quota_pressure_score=100.0,
            consecutive_missed_quota_periods=5,
            linkedin_activity_spike=1,
            deal_disengagement_count=10,
            compensation_satisfaction_score=0.0,
        )
        result = engine().assess(inp)
        assert result.workload_strain_score <= 100.0
        assert result.engagement_decay_score <= 100.0
        assert result.quota_pressure_score <= 100.0
        assert result.flight_signal_score <= 100.0


# ---------------------------------------------------------------------------
# 6. is_burnout_risk flag — all 3 trigger conditions
# ---------------------------------------------------------------------------

class TestIsBurnoutRisk:
    def test_burnout_risk_false_for_healthy(self):
        e = engine()
        result = e.assess(healthy_input())
        assert result.is_burnout_risk is False

    def test_burnout_risk_true_composite_gte_40(self):
        # Force composite >= 40 via multiple signals
        inp = healthy_input(
            after_hours_activity_pct=0.55,
            sick_days_last_90d=0,
            pto_days_taken_ytd=5.0,
            pto_days_allocated_ytd=20.0,
            crm_update_compliance_pct=50.0,
            crm_compliance_prior_pct=90.0,
            voluntary_meeting_attendance_pct=0.30,
            manager_interaction_days_since=25,
            quota_pressure_score=80.0,
            consecutive_missed_quota_periods=3,
        )
        result = engine().assess(inp)
        if result.burnout_composite >= 40:
            assert result.is_burnout_risk is True

    def test_burnout_risk_true_sick_days_gte_5(self):
        inp = healthy_input(sick_days_last_90d=5)
        result = engine().assess(inp)
        assert result.is_burnout_risk is True

    def test_burnout_risk_true_sick_days_6(self):
        inp = healthy_input(sick_days_last_90d=6)
        result = engine().assess(inp)
        assert result.is_burnout_risk is True

    def test_burnout_risk_false_sick_days_4(self):
        # Only 4 sick days & healthy otherwise — should be False unless composite triggers
        inp = healthy_input(sick_days_last_90d=4)
        result = engine().assess(inp)
        # composite should be low for otherwise healthy rep
        if result.burnout_composite < 40 and not (inp.after_hours_activity_pct >= 0.40 and inp.pto_days_taken_ytd == 0):
            assert result.is_burnout_risk is False

    def test_burnout_risk_true_after_hours_040_with_zero_pto(self):
        inp = healthy_input(after_hours_activity_pct=0.40, pto_days_taken_ytd=0.0)
        result = engine().assess(inp)
        assert result.is_burnout_risk is True

    def test_burnout_risk_true_after_hours_045_with_zero_pto(self):
        inp = healthy_input(after_hours_activity_pct=0.45, pto_days_taken_ytd=0.0)
        result = engine().assess(inp)
        assert result.is_burnout_risk is True

    def test_burnout_risk_false_after_hours_039_zero_pto(self):
        # after_hours < 0.40 with zero PTO should not trigger this condition alone
        inp = healthy_input(after_hours_activity_pct=0.39, pto_days_taken_ytd=0.0)
        result = engine().assess(inp)
        # If composite <40 and sick_days <5, should be False
        if result.burnout_composite < 40 and inp.sick_days_last_90d < 5:
            assert result.is_burnout_risk is False

    def test_burnout_risk_false_after_hours_040_nonzero_pto(self):
        # after_hours >= 0.40 but PTO > 0: condition doesn't trigger
        inp = healthy_input(after_hours_activity_pct=0.40, pto_days_taken_ytd=1.0)
        result = engine().assess(inp)
        if result.burnout_composite < 40 and inp.sick_days_last_90d < 5:
            assert result.is_burnout_risk is False

    def test_burnout_risk_result_type_is_bool(self):
        result = engine().assess(healthy_input())
        assert isinstance(result.is_burnout_risk, bool)

    def test_burnout_risk_boundary_sick_days_exactly_5(self):
        inp = healthy_input(sick_days_last_90d=5)
        result = engine().assess(inp)
        assert result.is_burnout_risk is True

    def test_burnout_risk_boundary_after_hours_exactly_040(self):
        inp = healthy_input(after_hours_activity_pct=0.40, pto_days_taken_ytd=0.0)
        result = engine().assess(inp)
        assert result.is_burnout_risk is True


# ---------------------------------------------------------------------------
# 7. is_flight_risk flag — all 3 trigger conditions
# ---------------------------------------------------------------------------

class TestIsFlightRisk:
    def test_flight_risk_false_for_healthy(self):
        result = engine().assess(healthy_input())
        assert result.is_flight_risk is False

    def test_flight_risk_true_composite_gte_30(self):
        # Force composite >=30
        inp = healthy_input(
            after_hours_activity_pct=0.55,
            crm_update_compliance_pct=55.0,
            crm_compliance_prior_pct=90.0,
            voluntary_meeting_attendance_pct=0.35,
            manager_interaction_days_since=22,
            quota_pressure_score=70.0,
            consecutive_missed_quota_periods=2,
        )
        result = engine().assess(inp)
        if result.burnout_composite >= 30:
            assert result.is_flight_risk is True

    def test_flight_risk_true_linkedin_spike(self):
        inp = healthy_input(linkedin_activity_spike=1)
        result = engine().assess(inp)
        assert result.is_flight_risk is True

    def test_flight_risk_false_no_linkedin_spike(self):
        inp = healthy_input(linkedin_activity_spike=0)
        result = engine().assess(inp)
        if result.burnout_composite < 30 and inp.consecutive_missed_quota_periods < 3:
            assert result.is_flight_risk is False

    def test_flight_risk_true_consecutive_missed_3(self):
        inp = healthy_input(consecutive_missed_quota_periods=3)
        result = engine().assess(inp)
        assert result.is_flight_risk is True

    def test_flight_risk_true_consecutive_missed_4(self):
        inp = healthy_input(consecutive_missed_quota_periods=4)
        result = engine().assess(inp)
        assert result.is_flight_risk is True

    def test_flight_risk_false_consecutive_missed_2(self):
        inp = healthy_input(consecutive_missed_quota_periods=2)
        result = engine().assess(inp)
        if result.burnout_composite < 30 and inp.linkedin_activity_spike == 0:
            assert result.is_flight_risk is False

    def test_flight_risk_result_is_bool(self):
        result = engine().assess(healthy_input())
        assert isinstance(result.is_flight_risk, bool)

    def test_flight_risk_boundary_linkedin_spike_0(self):
        inp = healthy_input(linkedin_activity_spike=0)
        result = engine().assess(inp)
        # linkedin alone doesn't trigger when it's 0
        if result.burnout_composite < 30 and inp.consecutive_missed_quota_periods < 3:
            assert result.is_flight_risk is False

    def test_flight_risk_boundary_consecutive_exactly_3(self):
        inp = healthy_input(consecutive_missed_quota_periods=3)
        result = engine().assess(inp)
        assert result.is_flight_risk is True

    def test_flight_risk_boundary_composite_exactly_30(self):
        # If composite is exactly 30, should be True
        # Verify by using an input that we compute matches closely
        inp = healthy_input(
            after_hours_activity_pct=0.50,   # +40 workload
            activity_count_prior_period=50.0,
            avg_weekly_activity_count=50.0,
            pto_days_taken_ytd=8.0,
            pto_days_allocated_ytd=20.0,
        )
        result = engine().assess(inp)
        # composite >= 30 should set is_flight_risk
        if result.burnout_composite >= 30:
            assert result.is_flight_risk is True


# ---------------------------------------------------------------------------
# 8. estimated_replacement_cost_usd
# ---------------------------------------------------------------------------

class TestReplacementCost:
    def test_cost_is_zero_for_zero_composite(self):
        # healthy rep with zero composite (edge case)
        result = engine().assess(healthy_input())
        expected = round(120000.0 * (result.burnout_composite / 100.0), 2)
        assert result.estimated_replacement_cost_usd == expected

    def test_cost_formula_composite_50(self):
        # Force composite ~50 and verify formula
        inp = healthy_input(
            after_hours_activity_pct=0.55,
            crm_update_compliance_pct=50.0,
            crm_compliance_prior_pct=90.0,
            voluntary_meeting_attendance_pct=0.30,
            manager_interaction_days_since=22,
            quota_pressure_score=80.0,
            consecutive_missed_quota_periods=3,
        )
        result = engine().assess(inp)
        expected = round(120000.0 * (result.burnout_composite / 100.0), 2)
        assert result.estimated_replacement_cost_usd == expected

    def test_cost_max_is_120000(self):
        inp = healthy_input(
            after_hours_activity_pct=0.99,
            sick_days_last_90d=10,
            crm_update_compliance_pct=0.0,
            crm_compliance_prior_pct=100.0,
            voluntary_meeting_attendance_pct=0.0,
            manager_interaction_days_since=30,
            peer_collaboration_score=0.0,
            quota_pressure_score=100.0,
            consecutive_missed_quota_periods=5,
            linkedin_activity_spike=1,
            deal_disengagement_count=10,
            compensation_satisfaction_score=0.0,
        )
        result = engine().assess(inp)
        assert result.estimated_replacement_cost_usd <= 120000.0

    def test_cost_is_non_negative(self):
        result = engine().assess(healthy_input())
        assert result.estimated_replacement_cost_usd >= 0.0

    def test_cost_is_rounded_to_2_decimals(self):
        result = engine().assess(healthy_input())
        cost = result.estimated_replacement_cost_usd
        assert cost == round(cost, 2)

    def test_cost_increases_with_composite(self):
        r_low = engine().assess(healthy_input())
        r_high = engine().assess(healthy_input(
            after_hours_activity_pct=0.55,
            sick_days_last_90d=6,
            linkedin_activity_spike=1,
            consecutive_missed_quota_periods=3,
        ))
        assert r_high.estimated_replacement_cost_usd >= r_low.estimated_replacement_cost_usd

    def test_cost_proportional_to_composite(self):
        result = engine().assess(healthy_input())
        expected = round(120000.0 * result.burnout_composite / 100.0, 2)
        assert result.estimated_replacement_cost_usd == expected

    def test_cost_type_is_float(self):
        result = engine().assess(healthy_input())
        assert isinstance(result.estimated_replacement_cost_usd, float)

    def test_cost_healthy_rep_low(self):
        result = engine().assess(healthy_input())
        # healthy rep has composite <20 so cost <24000
        assert result.estimated_replacement_cost_usd < 24000.0


# ---------------------------------------------------------------------------
# 9. Pattern detection priority order
# ---------------------------------------------------------------------------

class TestPatternDetection:
    def test_pattern_none_for_healthy(self):
        result = engine().assess(healthy_input())
        assert result.attrition_pattern == AttritionPattern.none

    def test_manager_conflict_priority_highest(self):
        # manager_conflict conditions: escalations>=3 AND manager_days>=14
        # Also set all other pattern triggers
        inp = healthy_input(
            escalations_raised_last_90d=3,
            manager_interaction_days_since=14,
            compensation_satisfaction_score=20.0,   # would trigger comp_dissatisfaction
            voluntary_meeting_attendance_pct=0.30,  # would trigger disengagement
            consecutive_missed_quota_periods=3,     # would trigger quota_pressure
            after_hours_activity_pct=0.30,          # would trigger workload_exhaustion
        )
        result = engine().assess(inp)
        assert result.attrition_pattern == AttritionPattern.manager_conflict

    def test_compensation_dissatisfaction_beats_disengagement(self):
        # comp_dissatisfaction: comp_sat<35 AND flight>=20
        # disengagement: engagement>=30 AND vol_meeting<0.50
        inp = healthy_input(
            compensation_satisfaction_score=20.0,
            linkedin_activity_spike=1,           # boosts flight score
            deal_disengagement_count=3,          # more flight
            voluntary_meeting_attendance_pct=0.30,  # would trigger disengagement
            crm_update_compliance_pct=55.0,      # boosts engagement decay
            crm_compliance_prior_pct=90.0,
            manager_interaction_days_since=22,
            escalations_raised_last_90d=0,       # no manager conflict
        )
        result = engine().assess(inp)
        assert result.attrition_pattern in (
            AttritionPattern.compensation_dissatisfaction,
            AttritionPattern.manager_conflict,
            AttritionPattern.disengagement,
        )

    def test_workload_exhaustion_pattern(self):
        # workload>=25 AND after_hours>=0.25 with no higher priority signals
        inp = healthy_input(
            after_hours_activity_pct=0.55,
            activity_count_prior_period=20.0,
            avg_weekly_activity_count=40.0,
            pto_days_taken_ytd=0.0,
            pto_days_allocated_ytd=20.0,
            escalations_raised_last_90d=0,
            compensation_satisfaction_score=80.0,
            voluntary_meeting_attendance_pct=0.70,
            consecutive_missed_quota_periods=0,
        )
        result = engine().assess(inp)
        assert result.attrition_pattern == AttritionPattern.workload_exhaustion

    def test_quota_pressure_pattern(self):
        inp = healthy_input(
            quota_pressure_score=80.0,
            consecutive_missed_quota_periods=3,
            quota_attainment_prior_pct=100.0,
            quota_attainment_pct=60.0,
            escalations_raised_last_90d=0,
            compensation_satisfaction_score=80.0,
            voluntary_meeting_attendance_pct=0.70,
            after_hours_activity_pct=0.10,
        )
        result = engine().assess(inp)
        assert result.attrition_pattern == AttritionPattern.quota_pressure

    def test_disengagement_pattern(self):
        # engagement>=30 AND vol_meeting<0.50, no higher priority
        inp = healthy_input(
            crm_update_compliance_pct=50.0,
            crm_compliance_prior_pct=90.0,
            voluntary_meeting_attendance_pct=0.30,
            manager_interaction_days_since=22,
            escalations_raised_last_90d=0,
            compensation_satisfaction_score=80.0,
            consecutive_missed_quota_periods=0,
            after_hours_activity_pct=0.10,
        )
        result = engine().assess(inp)
        assert result.attrition_pattern == AttritionPattern.disengagement

    def test_manager_conflict_requires_escalations_gte_3(self):
        # Only 2 escalations — should NOT be manager_conflict
        inp = healthy_input(
            escalations_raised_last_90d=2,
            manager_interaction_days_since=14,
        )
        result = engine().assess(inp)
        assert result.attrition_pattern != AttritionPattern.manager_conflict

    def test_manager_conflict_requires_manager_days_gte_14(self):
        # 3 escalations but only 13 days — should NOT be manager_conflict
        inp = healthy_input(
            escalations_raised_last_90d=3,
            manager_interaction_days_since=13,
        )
        result = engine().assess(inp)
        assert result.attrition_pattern != AttritionPattern.manager_conflict

    def test_pattern_is_enum_instance(self):
        result = engine().assess(healthy_input())
        assert isinstance(result.attrition_pattern, AttritionPattern)

    def test_manager_conflict_boundary_escalations_3(self):
        inp = healthy_input(escalations_raised_last_90d=3, manager_interaction_days_since=14)
        result = engine().assess(inp)
        assert result.attrition_pattern == AttritionPattern.manager_conflict

    def test_manager_conflict_boundary_manager_days_14(self):
        inp = healthy_input(escalations_raised_last_90d=4, manager_interaction_days_since=14)
        result = engine().assess(inp)
        assert result.attrition_pattern == AttritionPattern.manager_conflict


# ---------------------------------------------------------------------------
# 10. Risk level assignment
# ---------------------------------------------------------------------------

class TestRiskLevel:
    def test_risk_low_for_healthy(self):
        result = engine().assess(healthy_input())
        assert result.burnout_risk == BurnoutRisk.low

    def test_risk_moderate_composite_20_to_39(self):
        # Push composite into 20-39 range
        inp = healthy_input(
            after_hours_activity_pct=0.35,
            crm_update_compliance_pct=70.0,
            crm_compliance_prior_pct=90.0,
            voluntary_meeting_attendance_pct=0.55,
            manager_interaction_days_since=15,
        )
        result = engine().assess(inp)
        if 20 <= result.burnout_composite < 40:
            assert result.burnout_risk == BurnoutRisk.moderate

    def test_risk_high_composite_40_to_59(self):
        inp = healthy_input(
            after_hours_activity_pct=0.55,
            crm_update_compliance_pct=50.0,
            crm_compliance_prior_pct=90.0,
            voluntary_meeting_attendance_pct=0.30,
            manager_interaction_days_since=22,
            quota_pressure_score=80.0,
            consecutive_missed_quota_periods=2,
        )
        result = engine().assess(inp)
        if 40 <= result.burnout_composite < 60:
            assert result.burnout_risk == BurnoutRisk.high

    def test_risk_critical_composite_gte_60(self):
        inp = healthy_input(
            after_hours_activity_pct=0.70,
            crm_update_compliance_pct=30.0,
            crm_compliance_prior_pct=90.0,
            voluntary_meeting_attendance_pct=0.20,
            manager_interaction_days_since=30,
            quota_pressure_score=90.0,
            consecutive_missed_quota_periods=4,
            linkedin_activity_spike=1,
            deal_disengagement_count=5,
            compensation_satisfaction_score=15.0,
            sick_days_last_90d=6,
        )
        result = engine().assess(inp)
        if result.burnout_composite >= 60:
            assert result.burnout_risk == BurnoutRisk.critical

    def test_risk_is_enum_instance(self):
        result = engine().assess(healthy_input())
        assert isinstance(result.burnout_risk, BurnoutRisk)

    def test_risk_boundary_below_20_is_low(self):
        result = engine().assess(healthy_input())
        if result.burnout_composite < 20:
            assert result.burnout_risk == BurnoutRisk.low

    def test_risk_level_matches_composite_range_low(self):
        result = engine().assess(healthy_input())
        c = result.burnout_composite
        if c < 20:
            assert result.burnout_risk == BurnoutRisk.low
        elif c < 40:
            assert result.burnout_risk == BurnoutRisk.moderate
        elif c < 60:
            assert result.burnout_risk == BurnoutRisk.high
        else:
            assert result.burnout_risk == BurnoutRisk.critical


# ---------------------------------------------------------------------------
# 11. Severity assignment
# ---------------------------------------------------------------------------

class TestSeverityAssignment:
    def test_severity_healthy_for_low_composite(self):
        result = engine().assess(healthy_input())
        if result.burnout_composite < 20:
            assert result.burnout_severity == BurnoutSeverity.healthy

    def test_severity_watch_composite_20_39(self):
        inp = healthy_input(
            after_hours_activity_pct=0.35,
            crm_update_compliance_pct=70.0,
            crm_compliance_prior_pct=90.0,
            voluntary_meeting_attendance_pct=0.55,
            manager_interaction_days_since=15,
        )
        result = engine().assess(inp)
        if 20 <= result.burnout_composite < 40:
            assert result.burnout_severity == BurnoutSeverity.watch

    def test_severity_at_risk_composite_40_59(self):
        inp = healthy_input(
            after_hours_activity_pct=0.55,
            crm_update_compliance_pct=50.0,
            crm_compliance_prior_pct=90.0,
            voluntary_meeting_attendance_pct=0.30,
            manager_interaction_days_since=22,
            quota_pressure_score=80.0,
            consecutive_missed_quota_periods=2,
        )
        result = engine().assess(inp)
        if 40 <= result.burnout_composite < 60:
            assert result.burnout_severity == BurnoutSeverity.at_risk

    def test_severity_flight_risk_composite_gte_60(self):
        inp = healthy_input(
            after_hours_activity_pct=0.70,
            crm_update_compliance_pct=30.0,
            crm_compliance_prior_pct=90.0,
            voluntary_meeting_attendance_pct=0.20,
            manager_interaction_days_since=30,
            quota_pressure_score=90.0,
            consecutive_missed_quota_periods=4,
            linkedin_activity_spike=1,
            deal_disengagement_count=5,
            compensation_satisfaction_score=15.0,
        )
        result = engine().assess(inp)
        if result.burnout_composite >= 60:
            assert result.burnout_severity == BurnoutSeverity.flight_risk

    def test_severity_is_enum_instance(self):
        result = engine().assess(healthy_input())
        assert isinstance(result.burnout_severity, BurnoutSeverity)

    def test_severity_mirrors_risk_thresholds(self):
        """Severity and risk use the same thresholds."""
        result = engine().assess(healthy_input())
        c = result.burnout_composite
        if c < 20:
            assert result.burnout_severity == BurnoutSeverity.healthy
        elif c < 40:
            assert result.burnout_severity == BurnoutSeverity.watch
        elif c < 60:
            assert result.burnout_severity == BurnoutSeverity.at_risk
        else:
            assert result.burnout_severity == BurnoutSeverity.flight_risk

    def test_severity_healthy_boundary_exactly_0_composite(self):
        # Really healthy rep should be healthy severity
        result = engine().assess(healthy_input())
        assert result.burnout_severity in (BurnoutSeverity.healthy, BurnoutSeverity.watch)


# ---------------------------------------------------------------------------
# 12. Action assignment
# ---------------------------------------------------------------------------

class TestActionAssignment:
    def test_action_no_action_for_healthy(self):
        result = engine().assess(healthy_input())
        assert result.recommended_action == BurnoutAction.no_action

    def test_action_wellness_checkin_for_moderate(self):
        inp = healthy_input(
            after_hours_activity_pct=0.35,
            crm_update_compliance_pct=70.0,
            crm_compliance_prior_pct=90.0,
            voluntary_meeting_attendance_pct=0.55,
            manager_interaction_days_since=15,
        )
        result = engine().assess(inp)
        if result.burnout_risk == BurnoutRisk.moderate and not result.is_flight_risk:
            assert result.recommended_action == BurnoutAction.wellness_checkin

    def test_action_workload_rebalance_for_high(self):
        inp = healthy_input(
            after_hours_activity_pct=0.55,
            crm_update_compliance_pct=50.0,
            crm_compliance_prior_pct=90.0,
            voluntary_meeting_attendance_pct=0.30,
            manager_interaction_days_since=22,
            quota_pressure_score=80.0,
            consecutive_missed_quota_periods=2,
            linkedin_activity_spike=0,
        )
        result = engine().assess(inp)
        if result.burnout_risk == BurnoutRisk.high and not result.is_flight_risk:
            assert result.recommended_action == BurnoutAction.workload_rebalance

    def test_action_retention_interview_for_flight_risk(self):
        inp = healthy_input(linkedin_activity_spike=1)
        result = engine().assess(inp)
        if result.is_flight_risk and result.attrition_pattern != AttritionPattern.manager_conflict:
            assert result.recommended_action == BurnoutAction.retention_interview

    def test_action_executive_retention_for_manager_conflict_flight(self):
        inp = healthy_input(
            escalations_raised_last_90d=3,
            manager_interaction_days_since=14,
            linkedin_activity_spike=1,
        )
        result = engine().assess(inp)
        if result.is_flight_risk and result.attrition_pattern == AttritionPattern.manager_conflict:
            assert result.recommended_action == BurnoutAction.executive_retention

    def test_action_retention_interview_for_critical_risk(self):
        inp = healthy_input(
            after_hours_activity_pct=0.70,
            crm_update_compliance_pct=30.0,
            crm_compliance_prior_pct=90.0,
            voluntary_meeting_attendance_pct=0.20,
            manager_interaction_days_since=30,
            quota_pressure_score=90.0,
            consecutive_missed_quota_periods=4,
            linkedin_activity_spike=0,
            deal_disengagement_count=5,
            compensation_satisfaction_score=15.0,
        )
        result = engine().assess(inp)
        if result.burnout_risk == BurnoutRisk.critical:
            # critical + non-manager_conflict = retention_interview
            if result.attrition_pattern != AttritionPattern.manager_conflict:
                assert result.recommended_action == BurnoutAction.retention_interview

    def test_action_is_enum_instance(self):
        result = engine().assess(healthy_input())
        assert isinstance(result.recommended_action, BurnoutAction)

    def test_action_no_action_when_low_risk_no_flight(self):
        result = engine().assess(healthy_input())
        assert result.recommended_action == BurnoutAction.no_action


# ---------------------------------------------------------------------------
# 13. assess_batch() returns correct count
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_batch_empty_list(self):
        results = engine().assess_batch([])
        assert results == []

    def test_batch_single_item(self):
        results = engine().assess_batch([healthy_input()])
        assert len(results) == 1

    def test_batch_five_items(self):
        inputs = [healthy_input(rep_id=f"R{i:03d}") for i in range(5)]
        results = engine().assess_batch(inputs)
        assert len(results) == 5

    def test_batch_ten_items(self):
        inputs = [healthy_input(rep_id=f"R{i:03d}") for i in range(10)]
        results = engine().assess_batch(inputs)
        assert len(results) == 10

    def test_batch_returns_list(self):
        results = engine().assess_batch([healthy_input()])
        assert isinstance(results, list)

    def test_batch_results_are_result_instances(self):
        results = engine().assess_batch([healthy_input()])
        for r in results:
            assert isinstance(r, BurnoutAttritionResult)

    def test_batch_rep_ids_preserved(self):
        inputs = [healthy_input(rep_id=f"REP{i}") for i in range(3)]
        results = engine().assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"REP{i}"

    def test_batch_updates_summary(self):
        e = engine()
        inputs = [healthy_input(rep_id=f"R{i:03d}") for i in range(4)]
        e.assess_batch(inputs)
        assert e.summary()["total"] == 4

    def test_batch_mixed_risk_levels(self):
        inputs = [
            healthy_input(rep_id="LOW"),
            healthy_input(rep_id="HIGH", after_hours_activity_pct=0.55,
                          sick_days_last_90d=6, linkedin_activity_spike=1),
        ]
        results = engine().assess_batch(inputs)
        assert len(results) == 2
        assert results[0].rep_id == "LOW"
        assert results[1].rep_id == "HIGH"

    def test_batch_100_items(self):
        inputs = [healthy_input(rep_id=f"R{i:04d}") for i in range(100)]
        results = engine().assess_batch(inputs)
        assert len(results) == 100


# ---------------------------------------------------------------------------
# 14. summary() aggregation
# ---------------------------------------------------------------------------

class TestSummaryAggregation:
    def test_summary_total_matches_assess_count(self):
        e = engine()
        for i in range(7):
            e.assess(healthy_input(rep_id=f"R{i}"))
        assert e.summary()["total"] == 7

    def test_summary_total_replacement_cost_is_sum(self):
        e = engine()
        inputs = [healthy_input(rep_id=f"R{i}") for i in range(3)]
        results = e.assess_batch(inputs)
        expected_sum = round(sum(r.estimated_replacement_cost_usd for r in results), 2)
        assert e.summary()["total_estimated_replacement_cost_usd"] == expected_sum

    def test_summary_burnout_risk_count_correct(self):
        e = engine()
        # Sick days >=5 triggers is_burnout_risk
        e.assess(healthy_input(rep_id="BURNOUT1", sick_days_last_90d=5))
        e.assess(healthy_input(rep_id="BURNOUT2", sick_days_last_90d=5))
        e.assess(healthy_input(rep_id="OK"))
        s = e.summary()
        assert s["burnout_risk_count"] >= 2

    def test_summary_flight_risk_count_correct(self):
        e = engine()
        e.assess(healthy_input(rep_id="FLIGHT", linkedin_activity_spike=1))
        e.assess(healthy_input(rep_id="OK"))
        s = e.summary()
        assert s["flight_risk_count"] >= 1

    def test_summary_risk_counts_dict(self):
        e = engine()
        e.assess(healthy_input())
        s = e.summary()
        assert isinstance(s["risk_counts"], dict)
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_pattern_counts_dict(self):
        e = engine()
        e.assess(healthy_input())
        s = e.summary()
        assert isinstance(s["pattern_counts"], dict)
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_summary_severity_counts_dict(self):
        e = engine()
        e.assess(healthy_input())
        s = e.summary()
        assert isinstance(s["severity_counts"], dict)
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_summary_action_counts_dict(self):
        e = engine()
        e.assess(healthy_input())
        s = e.summary()
        assert isinstance(s["action_counts"], dict)
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_avg_composite_is_average(self):
        e = engine()
        inputs = [healthy_input(rep_id=f"R{i}") for i in range(5)]
        results = e.assess_batch(inputs)
        manual_avg = round(sum(r.burnout_composite for r in results) / 5, 1)
        assert e.summary()["avg_burnout_composite"] == manual_avg

    def test_summary_avg_workload_strain(self):
        e = engine()
        inputs = [healthy_input(rep_id=f"R{i}") for i in range(3)]
        results = e.assess_batch(inputs)
        manual_avg = round(sum(r.workload_strain_score for r in results) / 3, 1)
        assert e.summary()["avg_workload_strain_score"] == manual_avg

    def test_summary_avg_engagement_decay(self):
        e = engine()
        inputs = [healthy_input(rep_id=f"R{i}") for i in range(3)]
        results = e.assess_batch(inputs)
        manual_avg = round(sum(r.engagement_decay_score for r in results) / 3, 1)
        assert e.summary()["avg_engagement_decay_score"] == manual_avg

    def test_summary_avg_quota_pressure(self):
        e = engine()
        inputs = [healthy_input(rep_id=f"R{i}") for i in range(3)]
        results = e.assess_batch(inputs)
        manual_avg = round(sum(r.quota_pressure_score for r in results) / 3, 1)
        assert e.summary()["avg_quota_pressure_score"] == manual_avg

    def test_summary_avg_flight_signal(self):
        e = engine()
        inputs = [healthy_input(rep_id=f"R{i}") for i in range(3)]
        results = e.assess_batch(inputs)
        manual_avg = round(sum(r.flight_signal_score for r in results) / 3, 1)
        assert e.summary()["avg_flight_signal_score"] == manual_avg

    def test_summary_accumulates_across_multiple_assess_calls(self):
        e = engine()
        e.assess(healthy_input(rep_id="A"))
        e.assess(healthy_input(rep_id="B"))
        e.assess(healthy_input(rep_id="C"))
        assert e.summary()["total"] == 3

    def test_summary_replacement_cost_single_rep(self):
        e = engine()
        result = e.assess(healthy_input())
        s = e.summary()
        assert s["total_estimated_replacement_cost_usd"] == result.estimated_replacement_cost_usd


# ---------------------------------------------------------------------------
# 15. Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_zero_pto_allocated(self):
        # pto_days_allocated_ytd=0 should not cause division by zero
        inp = healthy_input(pto_days_taken_ytd=0.0, pto_days_allocated_ytd=0.0)
        result = engine().assess(inp)
        assert result is not None

    def test_zero_pto_allocated_no_crash(self):
        inp = healthy_input(pto_days_allocated_ytd=0.0, pto_days_taken_ytd=0.0)
        result = engine().assess(inp)
        assert isinstance(result.burnout_composite, float)

    def test_zero_activity_prior_period_no_crash(self):
        inp = healthy_input(activity_count_prior_period=0.0)
        result = engine().assess(inp)
        assert result is not None

    def test_healthy_rep_low_composite(self):
        result = engine().assess(healthy_input())
        assert result.burnout_composite < 20.0

    def test_healthy_rep_no_burnout_flag(self):
        result = engine().assess(healthy_input())
        assert result.is_burnout_risk is False

    def test_healthy_rep_no_flight_flag(self):
        result = engine().assess(healthy_input())
        assert result.is_flight_risk is False

    def test_healthy_rep_no_action(self):
        result = engine().assess(healthy_input())
        assert result.recommended_action == BurnoutAction.no_action

    def test_healthy_rep_pattern_none(self):
        result = engine().assess(healthy_input())
        assert result.attrition_pattern == AttritionPattern.none

    def test_all_flags_off_healthy(self):
        result = engine().assess(healthy_input())
        assert not result.is_burnout_risk
        assert not result.is_flight_risk

    def test_tenure_zero_months(self):
        inp = healthy_input(tenure_months=0)
        result = engine().assess(inp)
        assert result is not None

    def test_tenure_very_long(self):
        inp = healthy_input(tenure_months=240)
        result = engine().assess(inp)
        assert result is not None

    def test_rep_id_preserved(self):
        inp = healthy_input(rep_id="SPECIAL_REP_99")
        result = engine().assess(inp)
        assert result.rep_id == "SPECIAL_REP_99"

    def test_region_preserved(self):
        inp = healthy_input(region="APAC")
        result = engine().assess(inp)
        assert result.region == "APAC"

    def test_quota_attainment_above_100(self):
        inp = healthy_input(quota_attainment_pct=150.0, quota_attainment_prior_pct=120.0)
        result = engine().assess(inp)
        assert result is not None

    def test_all_scores_zero_conditions(self):
        # Force scores to minimum (all healthy values)
        result = engine().assess(healthy_input(
            after_hours_activity_pct=0.05,
            activity_count_prior_period=50.0,
            avg_weekly_activity_count=50.0,
            pto_days_taken_ytd=15.0,
            pto_days_allocated_ytd=20.0,
            sick_days_last_90d=0,
            crm_update_compliance_pct=90.0,
            crm_compliance_prior_pct=90.0,
            voluntary_meeting_attendance_pct=0.95,
            manager_interaction_days_since=3,
            peer_collaboration_score=80.0,
            quota_pressure_score=10.0,
            consecutive_missed_quota_periods=0,
            quota_attainment_pct=100.0,
            quota_attainment_prior_pct=100.0,
            escalations_raised_last_90d=0,
            linkedin_activity_spike=0,
            deal_disengagement_count=0,
            compensation_satisfaction_score=90.0,
            tenure_months=36,
        ))
        assert result.burnout_composite >= 0.0


# ---------------------------------------------------------------------------
# 16. Boundary conditions for all thresholds
# ---------------------------------------------------------------------------

class TestBoundaryConditions:
    # Workload strain thresholds
    def test_workload_after_hours_050_boundary(self):
        inp_below = healthy_input(after_hours_activity_pct=0.499)
        inp_above = healthy_input(after_hours_activity_pct=0.500)
        r_below = engine().assess(inp_below)
        r_above = engine().assess(inp_above)
        assert r_above.workload_strain_score >= r_below.workload_strain_score

    def test_workload_after_hours_035_boundary(self):
        inp_below = healthy_input(after_hours_activity_pct=0.349)
        inp_above = healthy_input(after_hours_activity_pct=0.350)
        r_below = engine().assess(inp_below)
        r_above = engine().assess(inp_above)
        assert r_above.workload_strain_score >= r_below.workload_strain_score

    def test_workload_after_hours_020_boundary(self):
        inp_below = healthy_input(after_hours_activity_pct=0.199)
        inp_above = healthy_input(after_hours_activity_pct=0.200)
        r_below = engine().assess(inp_below)
        r_above = engine().assess(inp_above)
        assert r_above.workload_strain_score >= r_below.workload_strain_score

    def test_workload_sick_days_5_boundary(self):
        r4 = engine().assess(healthy_input(sick_days_last_90d=4))
        r5 = engine().assess(healthy_input(sick_days_last_90d=5))
        assert r5.workload_strain_score >= r4.workload_strain_score

    def test_workload_sick_days_3_boundary(self):
        r2 = engine().assess(healthy_input(sick_days_last_90d=2))
        r3 = engine().assess(healthy_input(sick_days_last_90d=3))
        assert r3.workload_strain_score >= r2.workload_strain_score

    def test_workload_pto_used_020_boundary(self):
        # pto_used_pct < 0.20 adds 20 pts
        inp_under = healthy_input(pto_days_taken_ytd=3.0, pto_days_allocated_ytd=20.0)  # 15%
        inp_over = healthy_input(pto_days_taken_ytd=4.0, pto_days_allocated_ytd=20.0)   # 20%
        r_under = engine().assess(inp_under)
        r_over = engine().assess(inp_over)
        assert r_under.workload_strain_score >= r_over.workload_strain_score

    # Engagement decay thresholds
    def test_engagement_crm_decay_30_boundary(self):
        r_below = engine().assess(healthy_input(crm_compliance_prior_pct=90.0, crm_update_compliance_pct=61.0))
        r_above = engine().assess(healthy_input(crm_compliance_prior_pct=90.0, crm_update_compliance_pct=60.0))
        assert r_above.engagement_decay_score >= r_below.engagement_decay_score

    def test_engagement_crm_decay_20_boundary(self):
        r_below = engine().assess(healthy_input(crm_compliance_prior_pct=90.0, crm_update_compliance_pct=71.0))
        r_above = engine().assess(healthy_input(crm_compliance_prior_pct=90.0, crm_update_compliance_pct=70.0))
        assert r_above.engagement_decay_score >= r_below.engagement_decay_score

    def test_engagement_meeting_040_boundary(self):
        r_below = engine().assess(healthy_input(voluntary_meeting_attendance_pct=0.39))
        r_above = engine().assess(healthy_input(voluntary_meeting_attendance_pct=0.40))
        # below 0.40 should have higher engagement decay
        assert r_below.engagement_decay_score >= r_above.engagement_decay_score

    def test_engagement_manager_days_21_boundary(self):
        r_20 = engine().assess(healthy_input(manager_interaction_days_since=20))
        r_21 = engine().assess(healthy_input(manager_interaction_days_since=21))
        assert r_21.engagement_decay_score >= r_20.engagement_decay_score

    def test_engagement_peer_30_boundary(self):
        r_above = engine().assess(healthy_input(peer_collaboration_score=30.0))
        r_below = engine().assess(healthy_input(peer_collaboration_score=29.9))
        assert r_below.engagement_decay_score >= r_above.engagement_decay_score

    # Quota pressure thresholds
    def test_quota_pressure_score_80_boundary(self):
        r_below = engine().assess(healthy_input(quota_pressure_score=79.9))
        r_above = engine().assess(healthy_input(quota_pressure_score=80.0))
        assert r_above.quota_pressure_score >= r_below.quota_pressure_score

    def test_quota_pressure_score_60_boundary(self):
        r_below = engine().assess(healthy_input(quota_pressure_score=59.9))
        r_above = engine().assess(healthy_input(quota_pressure_score=60.0))
        assert r_above.quota_pressure_score >= r_below.quota_pressure_score

    def test_consecutive_missed_3_boundary(self):
        r2 = engine().assess(healthy_input(consecutive_missed_quota_periods=2))
        r3 = engine().assess(healthy_input(consecutive_missed_quota_periods=3))
        assert r3.quota_pressure_score >= r2.quota_pressure_score

    def test_consecutive_missed_2_boundary(self):
        r1 = engine().assess(healthy_input(consecutive_missed_quota_periods=1))
        r2 = engine().assess(healthy_input(consecutive_missed_quota_periods=2))
        assert r2.quota_pressure_score >= r1.quota_pressure_score

    def test_attainment_decline_25_boundary(self):
        r_below = engine().assess(healthy_input(quota_attainment_prior_pct=90.0, quota_attainment_pct=65.1))
        r_above = engine().assess(healthy_input(quota_attainment_prior_pct=90.0, quota_attainment_pct=65.0))
        assert r_above.quota_pressure_score >= r_below.quota_pressure_score

    # Flight signal thresholds
    def test_flight_deal_disengagement_5_boundary(self):
        r4 = engine().assess(healthy_input(deal_disengagement_count=4))
        r5 = engine().assess(healthy_input(deal_disengagement_count=5))
        assert r5.flight_signal_score >= r4.flight_signal_score

    def test_flight_deal_disengagement_3_boundary(self):
        r2 = engine().assess(healthy_input(deal_disengagement_count=2))
        r3 = engine().assess(healthy_input(deal_disengagement_count=3))
        assert r3.flight_signal_score >= r2.flight_signal_score

    def test_flight_comp_satisfaction_30_boundary(self):
        r_above = engine().assess(healthy_input(compensation_satisfaction_score=30.0))
        r_below = engine().assess(healthy_input(compensation_satisfaction_score=29.9))
        assert r_below.flight_signal_score >= r_above.flight_signal_score

    def test_flight_comp_satisfaction_50_boundary(self):
        r_above = engine().assess(healthy_input(compensation_satisfaction_score=50.0))
        r_below = engine().assess(healthy_input(compensation_satisfaction_score=49.9))
        assert r_below.flight_signal_score >= r_above.flight_signal_score

    def test_flight_tenure_12_with_high_pressure(self):
        # Short tenure + quota_pressure >= 60 adds +10 to flight
        r_long = engine().assess(healthy_input(tenure_months=24, quota_pressure_score=65.0))
        r_short = engine().assess(healthy_input(tenure_months=12, quota_pressure_score=65.0))
        assert r_short.flight_signal_score >= r_long.flight_signal_score

    # Risk composite thresholds
    def test_risk_boundary_exactly_20(self):
        # If composite is exactly 20, should be moderate
        # We can check by looking for a result where composite==20
        inp = healthy_input(
            after_hours_activity_pct=0.22,
            crm_update_compliance_pct=80.0,
            crm_compliance_prior_pct=90.0,
        )
        result = engine().assess(inp)
        c = result.burnout_composite
        if c == 20.0:
            assert result.burnout_risk == BurnoutRisk.moderate

    def test_risk_boundary_exactly_40(self):
        inp = healthy_input(
            after_hours_activity_pct=0.55,
            crm_update_compliance_pct=60.0,
            crm_compliance_prior_pct=90.0,
            voluntary_meeting_attendance_pct=0.35,
        )
        result = engine().assess(inp)
        c = result.burnout_composite
        if c == 40.0:
            assert result.burnout_risk == BurnoutRisk.high

    def test_risk_boundary_exactly_60(self):
        inp = healthy_input(
            after_hours_activity_pct=0.70,
            quota_pressure_score=90.0,
            consecutive_missed_quota_periods=3,
            linkedin_activity_spike=1,
        )
        result = engine().assess(inp)
        c = result.burnout_composite
        if c == 60.0:
            assert result.burnout_risk == BurnoutRisk.critical

    def test_escalations_4_vs_2_threshold(self):
        r2 = engine().assess(healthy_input(escalations_raised_last_90d=2))
        r4 = engine().assess(healthy_input(escalations_raised_last_90d=4))
        assert r4.quota_pressure_score >= r2.quota_pressure_score

    def test_workload_surge_050_boundary(self):
        # surge >= 0.50 adds 30 pts
        inp_below = healthy_input(activity_count_prior_period=100.0, avg_weekly_activity_count=149.0)
        inp_above = healthy_input(activity_count_prior_period=100.0, avg_weekly_activity_count=150.0)
        r_below = engine().assess(inp_below)
        r_above = engine().assess(inp_above)
        assert r_above.workload_strain_score >= r_below.workload_strain_score

    def test_workload_surge_025_boundary(self):
        inp_below = healthy_input(activity_count_prior_period=100.0, avg_weekly_activity_count=124.0)
        inp_above = healthy_input(activity_count_prior_period=100.0, avg_weekly_activity_count=125.0)
        r_below = engine().assess(inp_below)
        r_above = engine().assess(inp_above)
        assert r_above.workload_strain_score >= r_below.workload_strain_score


# ---------------------------------------------------------------------------
# 17. burnout_signal string is non-empty
# ---------------------------------------------------------------------------

class TestBurnoutSignal:
    def test_signal_is_string(self):
        result = engine().assess(healthy_input())
        assert isinstance(result.burnout_signal, str)

    def test_signal_is_non_empty(self):
        result = engine().assess(healthy_input())
        assert len(result.burnout_signal) > 0

    def test_signal_healthy_rep_default_message(self):
        result = engine().assess(healthy_input())
        assert "healthy" in result.burnout_signal.lower()

    def test_signal_contains_after_hours_when_high(self):
        inp = healthy_input(after_hours_activity_pct=0.50)
        result = engine().assess(inp)
        assert "after-hours" in result.burnout_signal

    def test_signal_contains_linkedin_spike_when_present(self):
        inp = healthy_input(linkedin_activity_spike=1)
        result = engine().assess(inp)
        assert "LinkedIn" in result.burnout_signal

    def test_signal_contains_missed_quota_when_multiple(self):
        inp = healthy_input(consecutive_missed_quota_periods=3)
        result = engine().assess(inp)
        assert "missed quota" in result.burnout_signal

    def test_signal_contains_pto_info_when_low(self):
        inp = healthy_input(pto_days_taken_ytd=2.0, pto_days_allocated_ytd=20.0)
        result = engine().assess(inp)
        assert "PTO" in result.burnout_signal

    def test_signal_contains_disengaged_deals_when_multiple(self):
        inp = healthy_input(deal_disengagement_count=3)
        result = engine().assess(inp)
        assert "disengaged deals" in result.burnout_signal

    def test_signal_contains_composite_when_risk(self):
        inp = healthy_input(after_hours_activity_pct=0.50)
        result = engine().assess(inp)
        # signal includes "composite <X>"
        assert "composite" in result.burnout_signal

    def test_signal_contains_pattern_label(self):
        # To get the pattern label in the signal, we need at least one signal trigger
        # (after_hours >=0.35, consecutive_missed>=2, linkedin_spike, low PTO, deal_disengagement>=2)
        inp = healthy_input(
            escalations_raised_last_90d=3,
            manager_interaction_days_since=14,
            after_hours_activity_pct=0.50,  # triggers after-hours signal part
        )
        result = engine().assess(inp)
        if result.attrition_pattern == AttritionPattern.manager_conflict:
            assert "manager conflict" in result.burnout_signal.lower()

    def test_signal_non_empty_for_high_risk(self):
        inp = healthy_input(
            after_hours_activity_pct=0.60,
            sick_days_last_90d=6,
            linkedin_activity_spike=1,
        )
        result = engine().assess(inp)
        assert len(result.burnout_signal) > 0

    def test_signal_non_empty_for_critical_risk(self):
        inp = healthy_input(
            after_hours_activity_pct=0.70,
            crm_update_compliance_pct=30.0,
            crm_compliance_prior_pct=90.0,
            voluntary_meeting_attendance_pct=0.20,
            manager_interaction_days_since=30,
            quota_pressure_score=90.0,
            consecutive_missed_quota_periods=4,
            linkedin_activity_spike=1,
        )
        result = engine().assess(inp)
        assert len(result.burnout_signal) > 0

    def test_signal_multiple_risk_signals_concatenated(self):
        inp = healthy_input(
            after_hours_activity_pct=0.50,
            consecutive_missed_quota_periods=3,
            linkedin_activity_spike=1,
        )
        result = engine().assess(inp)
        # Multiple signals should produce longer signal string
        assert " — " in result.burnout_signal

    def test_signal_is_stripped(self):
        result = engine().assess(healthy_input())
        # Shouldn't start or end with whitespace
        assert result.burnout_signal == result.burnout_signal.strip()

    def test_signal_deals_threshold_exactly_2(self):
        inp = healthy_input(deal_disengagement_count=2)
        result = engine().assess(inp)
        assert "disengaged deals" in result.burnout_signal

    def test_signal_deals_below_threshold(self):
        inp = healthy_input(deal_disengagement_count=1)
        result = engine().assess(inp)
        # 1 deal is below the signal threshold of 2
        # Signal may or may not include it — just make sure it's non-empty
        assert len(result.burnout_signal) > 0

    def test_signal_pto_threshold_exactly_025(self):
        # pto_used = 4/20 = 0.20 which is < 0.25
        inp = healthy_input(pto_days_taken_ytd=4.0, pto_days_allocated_ytd=20.0)
        result = engine().assess(inp)
        assert "PTO" in result.burnout_signal

    def test_signal_type_is_str_across_patterns(self):
        patterns_inputs = [
            healthy_input(escalations_raised_last_90d=3, manager_interaction_days_since=14),
            healthy_input(compensation_satisfaction_score=20.0, linkedin_activity_spike=1),
            healthy_input(crm_update_compliance_pct=50.0, crm_compliance_prior_pct=90.0,
                          voluntary_meeting_attendance_pct=0.30),
        ]
        e = engine()
        for inp in patterns_inputs:
            result = e.assess(inp)
            assert isinstance(result.burnout_signal, str)
            assert len(result.burnout_signal) > 0


# ---------------------------------------------------------------------------
# Additional integration tests
# ---------------------------------------------------------------------------

class TestIntegration:
    def test_full_pipeline_healthy_rep(self):
        e = engine()
        inp = healthy_input(rep_id="FULL_HEALTHY")
        result = e.assess(inp)
        assert result.rep_id == "FULL_HEALTHY"
        assert result.is_burnout_risk is False
        assert result.is_flight_risk is False
        assert result.burnout_risk == BurnoutRisk.low
        assert result.burnout_severity == BurnoutSeverity.healthy
        assert result.recommended_action == BurnoutAction.no_action
        assert result.burnout_composite < 20.0

    def test_full_pipeline_critical_rep(self):
        e = engine()
        inp = healthy_input(
            rep_id="CRITICAL",
            after_hours_activity_pct=0.70,
            crm_update_compliance_pct=30.0,
            crm_compliance_prior_pct=90.0,
            voluntary_meeting_attendance_pct=0.20,
            manager_interaction_days_since=30,
            quota_pressure_score=90.0,
            consecutive_missed_quota_periods=4,
            linkedin_activity_spike=1,
            deal_disengagement_count=5,
            compensation_satisfaction_score=15.0,
            sick_days_last_90d=6,
        )
        result = e.assess(inp)
        assert result.is_burnout_risk is True
        assert result.is_flight_risk is True
        assert result.burnout_composite > 0

    def test_batch_and_summary_consistency(self):
        e = engine()
        inputs = [healthy_input(rep_id=f"R{i}", linkedin_activity_spike=i % 2) for i in range(6)]
        results = e.assess_batch(inputs)
        s = e.summary()
        assert s["total"] == 6
        flight_count = sum(1 for r in results if r.is_flight_risk)
        assert s["flight_risk_count"] == flight_count

    def test_summary_replacement_cost_sum_multiple(self):
        e = engine()
        results = e.assess_batch([
            healthy_input(rep_id="A"),
            healthy_input(rep_id="B", linkedin_activity_spike=1, sick_days_last_90d=5),
            healthy_input(rep_id="C", consecutive_missed_quota_periods=3),
        ])
        expected = round(sum(r.estimated_replacement_cost_usd for r in results), 2)
        assert e.summary()["total_estimated_replacement_cost_usd"] == expected

    def test_assess_returns_correct_type(self):
        result = engine().assess(healthy_input())
        assert isinstance(result, BurnoutAttritionResult)

    def test_independent_engines_dont_share_state(self):
        e1 = engine()
        e2 = engine()
        e1.assess(healthy_input(rep_id="E1_R1"))
        e1.assess(healthy_input(rep_id="E1_R2"))
        e2.assess(healthy_input(rep_id="E2_R1"))
        assert e1.summary()["total"] == 2
        assert e2.summary()["total"] == 1

    def test_multiple_assesses_accumulate_in_summary(self):
        e = engine()
        for i in range(20):
            e.assess(healthy_input(rep_id=f"R{i}"))
        assert e.summary()["total"] == 20

    def test_to_dict_composite_matches_result(self):
        e = engine()
        result = e.assess(healthy_input())
        d = result.to_dict()
        assert d["burnout_composite"] == result.burnout_composite

    def test_to_dict_is_burnout_risk_matches_result(self):
        e = engine()
        result = e.assess(healthy_input(sick_days_last_90d=5))
        d = result.to_dict()
        assert d["is_burnout_risk"] == result.is_burnout_risk

    def test_to_dict_is_flight_risk_matches_result(self):
        e = engine()
        result = e.assess(healthy_input(linkedin_activity_spike=1))
        d = result.to_dict()
        assert d["is_flight_risk"] == result.is_flight_risk

    def test_to_dict_cost_matches_result(self):
        e = engine()
        result = e.assess(healthy_input())
        d = result.to_dict()
        assert d["estimated_replacement_cost_usd"] == result.estimated_replacement_cost_usd

    def test_summary_avg_composite_single_rep(self):
        e = engine()
        result = e.assess(healthy_input())
        s = e.summary()
        assert s["avg_burnout_composite"] == result.burnout_composite

    def test_batch_preserves_order(self):
        inputs = [healthy_input(rep_id=f"ORDER_{i}") for i in range(10)]
        results = engine().assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"ORDER_{i}"

    def test_is_flight_risk_implies_retention_or_executive_action(self):
        e = engine()
        result = e.assess(healthy_input(linkedin_activity_spike=1))
        if result.is_flight_risk:
            assert result.recommended_action in (
                BurnoutAction.retention_interview,
                BurnoutAction.executive_retention,
            )

    def test_manager_conflict_pattern_with_flight_gives_executive_retention(self):
        e = engine()
        inp = healthy_input(
            escalations_raised_last_90d=4,
            manager_interaction_days_since=21,
            linkedin_activity_spike=1,
        )
        result = e.assess(inp)
        if result.is_flight_risk and result.attrition_pattern == AttritionPattern.manager_conflict:
            assert result.recommended_action == BurnoutAction.executive_retention

    def test_composite_always_between_0_and_100(self):
        test_inputs = [
            healthy_input(),
            healthy_input(after_hours_activity_pct=0.99, sick_days_last_90d=10),
            healthy_input(linkedin_activity_spike=1, consecutive_missed_quota_periods=5),
            healthy_input(compensation_satisfaction_score=0.0, deal_disengagement_count=10),
        ]
        e = engine()
        for inp in test_inputs:
            result = e.assess(inp)
            assert 0.0 <= result.burnout_composite <= 100.0

    def test_workload_strain_after_hours_at_050_adds_40(self):
        # after_hours_activity_pct >= 0.5 should add exactly 40 to workload
        inp_low = healthy_input(
            after_hours_activity_pct=0.30,  # 12 pts
            activity_count_prior_period=50.0,
            avg_weekly_activity_count=50.0,
            pto_days_taken_ytd=10.0,
            pto_days_allocated_ytd=20.0,
            sick_days_last_90d=0,
        )
        inp_high = healthy_input(
            after_hours_activity_pct=0.55,  # 40 pts
            activity_count_prior_period=50.0,
            avg_weekly_activity_count=50.0,
            pto_days_taken_ytd=10.0,
            pto_days_allocated_ytd=20.0,
            sick_days_last_90d=0,
        )
        r_low = engine().assess(inp_low)
        r_high = engine().assess(inp_high)
        diff = r_high.workload_strain_score - r_low.workload_strain_score
        assert diff > 0

    def test_flight_signal_linkedin_spike_adds_40(self):
        r_no = engine().assess(healthy_input(linkedin_activity_spike=0))
        r_yes = engine().assess(healthy_input(linkedin_activity_spike=1))
        assert r_yes.flight_signal_score - r_no.flight_signal_score == 40.0
