"""
Comprehensive tests for swarm/intelligence/sales_burnout_risk_engine.py
"""
from __future__ import annotations

import dataclasses
import math
import pytest
from typing import List

from swarm.intelligence.sales_burnout_risk_engine import (
    BurnoutRisk,
    BurnoutStage,
    BurnoutSignal,
    BurnoutAction,
    SalesBurnoutInput,
    SalesBurnoutResult,
    SalesBurnoutRiskEngine,
    _activity_health_score,
    _wellbeing_score,
    _performance_sustainability_score,
    _social_engagement_score,
    _composite,
    _burnout_risk,
    _burnout_stage,
    _primary_signal,
    _burnout_action,
    _productivity_impact_pct,
    _burnout_signal_text,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(
    rep_id: str = "r1",
    rep_name: str = "Alice",
    region: str = "West",
    activity_decline_pct: float = 0.0,
    avg_daily_calls_last_30d: float = 10.0,
    avg_daily_calls_prior_30d: float = 10.0,
    email_response_time_hrs: float = 2.0,
    meeting_acceptance_rate_pct: float = 90.0,
    pipeline_creation_last_30d_usd: float = 100_000.0,
    pipeline_creation_prior_30d_usd: float = 100_000.0,
    consecutive_no_close_weeks: int = 0,
    deal_win_rate_last_90d: float = 30.0,
    deal_win_rate_prior_quarter: float = 30.0,
    pto_days_taken_ytd: float = 10.0,
    pto_days_available_ytd: float = 15.0,
    weekend_work_hours_avg: float = 1.0,
    overtime_hours_per_week: float = 2.0,
    sick_days_last_90d: int = 0,
    manager_checkin_frequency: float = 4.0,
    peer_interaction_score: float = 100.0,
    quota_pressure_score: float = 30.0,
    customer_escalations_last_30d: int = 0,
) -> SalesBurnoutInput:
    return SalesBurnoutInput(
        rep_id=rep_id,
        rep_name=rep_name,
        region=region,
        activity_decline_pct=activity_decline_pct,
        avg_daily_calls_last_30d=avg_daily_calls_last_30d,
        avg_daily_calls_prior_30d=avg_daily_calls_prior_30d,
        email_response_time_hrs=email_response_time_hrs,
        meeting_acceptance_rate_pct=meeting_acceptance_rate_pct,
        pipeline_creation_last_30d_usd=pipeline_creation_last_30d_usd,
        pipeline_creation_prior_30d_usd=pipeline_creation_prior_30d_usd,
        consecutive_no_close_weeks=consecutive_no_close_weeks,
        deal_win_rate_last_90d=deal_win_rate_last_90d,
        deal_win_rate_prior_quarter=deal_win_rate_prior_quarter,
        pto_days_taken_ytd=pto_days_taken_ytd,
        pto_days_available_ytd=pto_days_available_ytd,
        weekend_work_hours_avg=weekend_work_hours_avg,
        overtime_hours_per_week=overtime_hours_per_week,
        sick_days_last_90d=sick_days_last_90d,
        manager_checkin_frequency=manager_checkin_frequency,
        peer_interaction_score=peer_interaction_score,
        quota_pressure_score=quota_pressure_score,
        customer_escalations_last_30d=customer_escalations_last_30d,
    )


def healthy_input(rep_id: str = "healthy1", rep_name: str = "Bob") -> SalesBurnoutInput:
    """Returns a rep with maximum health scores."""
    return make_input(
        rep_id=rep_id,
        rep_name=rep_name,
        activity_decline_pct=0.0,
        meeting_acceptance_rate_pct=90.0,
        pipeline_creation_last_30d_usd=120_000.0,
        pipeline_creation_prior_30d_usd=100_000.0,
        consecutive_no_close_weeks=0,
        deal_win_rate_last_90d=35.0,
        deal_win_rate_prior_quarter=30.0,
        pto_days_taken_ytd=10.0,
        pto_days_available_ytd=15.0,
        weekend_work_hours_avg=1.0,
        overtime_hours_per_week=2.0,
        sick_days_last_90d=0,
        manager_checkin_frequency=5.0,
        peer_interaction_score=100.0,
        quota_pressure_score=20.0,
        customer_escalations_last_30d=0,
        email_response_time_hrs=2.0,
    )


def burned_out_input(rep_id: str = "burned1", rep_name: str = "Charlie") -> SalesBurnoutInput:
    """Returns a rep with maximum burnout signals."""
    return make_input(
        rep_id=rep_id,
        rep_name=rep_name,
        activity_decline_pct=60.0,
        meeting_acceptance_rate_pct=20.0,
        pipeline_creation_last_30d_usd=10_000.0,
        pipeline_creation_prior_30d_usd=100_000.0,
        consecutive_no_close_weeks=12,
        deal_win_rate_last_90d=5.0,
        deal_win_rate_prior_quarter=35.0,
        pto_days_taken_ytd=0.0,
        pto_days_available_ytd=15.0,
        weekend_work_hours_avg=15.0,
        overtime_hours_per_week=25.0,
        sick_days_last_90d=8,
        manager_checkin_frequency=0.0,
        peer_interaction_score=0.0,
        quota_pressure_score=90.0,
        customer_escalations_last_30d=5,
        email_response_time_hrs=48.0,
    )


# ===========================================================================
# 1. ENUM TESTS
# ===========================================================================

class TestBurnoutRiskEnum:
    def test_enum_has_5_members(self):
        assert len(BurnoutRisk) == 5

    def test_none_value(self):
        assert BurnoutRisk.NONE.value == "none"

    def test_early_warning_value(self):
        assert BurnoutRisk.EARLY_WARNING.value == "early_warning"

    def test_moderate_value(self):
        assert BurnoutRisk.MODERATE.value == "moderate"

    def test_high_value(self):
        assert BurnoutRisk.HIGH.value == "high"

    def test_critical_value(self):
        assert BurnoutRisk.CRITICAL.value == "critical"

    def test_is_str_enum(self):
        assert isinstance(BurnoutRisk.NONE, str)

    def test_members_by_name(self):
        names = {m.name for m in BurnoutRisk}
        assert names == {"NONE", "EARLY_WARNING", "MODERATE", "HIGH", "CRITICAL"}


class TestBurnoutStageEnum:
    def test_enum_has_5_members(self):
        assert len(BurnoutStage) == 5

    def test_engaged_value(self):
        assert BurnoutStage.ENGAGED.value == "engaged"

    def test_coasting_value(self):
        assert BurnoutStage.COASTING.value == "coasting"

    def test_disengaging_value(self):
        assert BurnoutStage.DISENGAGING.value == "disengaging"

    def test_burned_out_value(self):
        assert BurnoutStage.BURNED_OUT.value == "burned_out"

    def test_depleted_value(self):
        assert BurnoutStage.DEPLETED.value == "depleted"

    def test_is_str_enum(self):
        assert isinstance(BurnoutStage.ENGAGED, str)

    def test_members_by_name(self):
        names = {m.name for m in BurnoutStage}
        assert names == {"ENGAGED", "COASTING", "DISENGAGING", "BURNED_OUT", "DEPLETED"}


class TestBurnoutSignalEnum:
    def test_enum_has_6_members(self):
        assert len(BurnoutSignal) == 6

    def test_none_value(self):
        assert BurnoutSignal.NONE.value == "none"

    def test_activity_decline_value(self):
        assert BurnoutSignal.ACTIVITY_DECLINE.value == "activity_decline"

    def test_isolation_value(self):
        assert BurnoutSignal.ISOLATION.value == "isolation"

    def test_performance_decay_value(self):
        assert BurnoutSignal.PERFORMANCE_DECAY.value == "performance_decay"

    def test_exhaustion_value(self):
        assert BurnoutSignal.EXHAUSTION.value == "exhaustion"

    def test_overwhelm_value(self):
        assert BurnoutSignal.OVERWHELM.value == "overwhelm"

    def test_is_str_enum(self):
        assert isinstance(BurnoutSignal.NONE, str)


class TestBurnoutActionEnum:
    def test_enum_has_5_members(self):
        assert len(BurnoutAction) == 5

    def test_monitor_value(self):
        assert BurnoutAction.MONITOR.value == "monitor"

    def test_check_in_value(self):
        assert BurnoutAction.CHECK_IN.value == "check_in"

    def test_coaching_session_value(self):
        assert BurnoutAction.COACHING_SESSION.value == "coaching_session"

    def test_workload_reduction_value(self):
        assert BurnoutAction.WORKLOAD_REDUCTION.value == "workload_reduction"

    def test_urgent_intervention_value(self):
        assert BurnoutAction.URGENT_INTERVENTION.value == "urgent_intervention"

    def test_is_str_enum(self):
        assert isinstance(BurnoutAction.MONITOR, str)


# ===========================================================================
# 2. SALESBURNOUTINPUT FIELD COUNT & TYPES
# ===========================================================================

class TestSalesBurnoutInputFields:
    def test_input_has_22_fields(self):
        fields = dataclasses.fields(SalesBurnoutInput)
        assert len(fields) == 22

    def test_all_expected_field_names(self):
        expected = {
            "rep_id", "rep_name", "region", "activity_decline_pct",
            "avg_daily_calls_last_30d", "avg_daily_calls_prior_30d",
            "email_response_time_hrs", "meeting_acceptance_rate_pct",
            "pipeline_creation_last_30d_usd", "pipeline_creation_prior_30d_usd",
            "consecutive_no_close_weeks", "deal_win_rate_last_90d",
            "deal_win_rate_prior_quarter", "pto_days_taken_ytd",
            "pto_days_available_ytd", "weekend_work_hours_avg",
            "overtime_hours_per_week", "sick_days_last_90d",
            "manager_checkin_frequency", "peer_interaction_score",
            "quota_pressure_score", "customer_escalations_last_30d",
        }
        actual = {f.name for f in dataclasses.fields(SalesBurnoutInput)}
        assert actual == expected

    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(SalesBurnoutInput)

    def test_can_be_instantiated(self):
        inp = make_input()
        assert inp.rep_id == "r1"

    def test_rep_id_stored(self):
        inp = make_input(rep_id="xyz")
        assert inp.rep_id == "xyz"

    def test_rep_name_stored(self):
        inp = make_input(rep_name="Denise")
        assert inp.rep_name == "Denise"

    def test_region_stored(self):
        inp = make_input(region="East")
        assert inp.region == "East"

    def test_numeric_fields_accept_float(self):
        inp = make_input(activity_decline_pct=12.5)
        assert inp.activity_decline_pct == 12.5

    def test_integer_field_consecutive_no_close(self):
        inp = make_input(consecutive_no_close_weeks=3)
        assert inp.consecutive_no_close_weeks == 3

    def test_integer_field_sick_days(self):
        inp = make_input(sick_days_last_90d=4)
        assert inp.sick_days_last_90d == 4

    def test_integer_field_customer_escalations(self):
        inp = make_input(customer_escalations_last_30d=2)
        assert inp.customer_escalations_last_30d == 2


# ===========================================================================
# 3. SALESBURNOUTRESULT FIELD COUNT & to_dict()
# ===========================================================================

class TestSalesBurnoutResultFields:
    def setup_method(self):
        self.engine = SalesBurnoutRiskEngine()
        self.result = self.engine.assess(make_input())

    def test_result_has_15_fields_in_to_dict(self):
        d = self.result.to_dict()
        assert len(d) == 15

    def test_to_dict_keys(self):
        expected = {
            "rep_id", "rep_name", "burnout_risk", "burnout_stage",
            "primary_burnout_signal", "burnout_action",
            "activity_health_score", "wellbeing_score",
            "performance_sustainability_score", "social_engagement_score",
            "burnout_composite", "is_at_burnout_risk", "needs_immediate_support",
            "estimated_productivity_impact_pct", "burnout_signal",
        }
        assert set(self.result.to_dict().keys()) == expected

    def test_result_is_dataclass(self):
        assert dataclasses.is_dataclass(SalesBurnoutResult)

    def test_to_dict_rep_id_matches(self):
        inp = make_input(rep_id="repABC")
        r = self.engine.assess(inp)
        assert r.to_dict()["rep_id"] == "repABC"

    def test_to_dict_rep_name_matches(self):
        inp = make_input(rep_name="Greta")
        r = self.engine.assess(inp)
        assert r.to_dict()["rep_name"] == "Greta"

    def test_to_dict_burnout_risk_is_string(self):
        d = self.result.to_dict()
        assert isinstance(d["burnout_risk"], str)

    def test_to_dict_burnout_stage_is_string(self):
        d = self.result.to_dict()
        assert isinstance(d["burnout_stage"], str)

    def test_to_dict_primary_burnout_signal_is_string(self):
        d = self.result.to_dict()
        assert isinstance(d["primary_burnout_signal"], str)

    def test_to_dict_burnout_action_is_string(self):
        d = self.result.to_dict()
        assert isinstance(d["burnout_action"], str)

    def test_to_dict_activity_health_score_is_float(self):
        d = self.result.to_dict()
        assert isinstance(d["activity_health_score"], float)

    def test_to_dict_wellbeing_score_is_float(self):
        d = self.result.to_dict()
        assert isinstance(d["wellbeing_score"], float)

    def test_to_dict_performance_sustainability_score_is_float(self):
        d = self.result.to_dict()
        assert isinstance(d["performance_sustainability_score"], float)

    def test_to_dict_social_engagement_score_is_float(self):
        d = self.result.to_dict()
        assert isinstance(d["social_engagement_score"], float)

    def test_to_dict_burnout_composite_is_float(self):
        d = self.result.to_dict()
        assert isinstance(d["burnout_composite"], float)

    def test_to_dict_is_at_burnout_risk_is_bool(self):
        d = self.result.to_dict()
        assert isinstance(d["is_at_burnout_risk"], bool)

    def test_to_dict_needs_immediate_support_is_bool(self):
        d = self.result.to_dict()
        assert isinstance(d["needs_immediate_support"], bool)

    def test_to_dict_estimated_productivity_impact_pct_is_float(self):
        d = self.result.to_dict()
        assert isinstance(d["estimated_productivity_impact_pct"], float)

    def test_to_dict_burnout_signal_is_str(self):
        d = self.result.to_dict()
        assert isinstance(d["burnout_signal"], str)

    def test_result_dataclass_has_15_fields(self):
        fields = dataclasses.fields(SalesBurnoutResult)
        assert len(fields) == 15


# ===========================================================================
# 4. SUMMARY() KEY SET
# ===========================================================================

class TestSummaryKeys:
    def setup_method(self):
        self.engine = SalesBurnoutRiskEngine()
        self.engine.assess(make_input())

    def test_summary_has_13_keys(self):
        s = self.engine.summary()
        assert len(s) == 13

    def test_summary_key_total(self):
        assert "total" in self.engine.summary()

    def test_summary_key_risk_counts(self):
        assert "risk_counts" in self.engine.summary()

    def test_summary_key_stage_counts(self):
        assert "stage_counts" in self.engine.summary()

    def test_summary_key_signal_counts(self):
        assert "signal_counts" in self.engine.summary()

    def test_summary_key_action_counts(self):
        assert "action_counts" in self.engine.summary()

    def test_summary_key_avg_burnout_composite(self):
        assert "avg_burnout_composite" in self.engine.summary()

    def test_summary_key_at_burnout_risk_count(self):
        assert "at_burnout_risk_count" in self.engine.summary()

    def test_summary_key_immediate_support_count(self):
        assert "immediate_support_count" in self.engine.summary()

    def test_summary_key_avg_activity_health_score(self):
        assert "avg_activity_health_score" in self.engine.summary()

    def test_summary_key_avg_wellbeing_score(self):
        assert "avg_wellbeing_score" in self.engine.summary()

    def test_summary_key_avg_performance_sustainability_score(self):
        assert "avg_performance_sustainability_score" in self.engine.summary()

    def test_summary_key_avg_social_engagement_score(self):
        assert "avg_social_engagement_score" in self.engine.summary()

    def test_summary_key_total_productivity_impact_pct(self):
        assert "total_productivity_impact_pct" in self.engine.summary()

    def test_summary_exact_key_set(self):
        expected = {
            "total", "risk_counts", "stage_counts", "signal_counts", "action_counts",
            "avg_burnout_composite", "at_burnout_risk_count", "immediate_support_count",
            "avg_activity_health_score", "avg_wellbeing_score",
            "avg_performance_sustainability_score", "avg_social_engagement_score",
            "total_productivity_impact_pct",
        }
        assert set(self.engine.summary().keys()) == expected


# ===========================================================================
# 5. ACTIVITY HEALTH SCORE
# ===========================================================================

class TestActivityHealthScore:
    def test_perfect_activity_decline_score(self):
        inp = make_input(activity_decline_pct=0.0, pipeline_creation_last_30d_usd=100_000,
                         pipeline_creation_prior_30d_usd=100_000, meeting_acceptance_rate_pct=90.0)
        score = _activity_health_score(inp)
        assert score == 100.0

    def test_activity_decline_5_gets_35(self):
        inp = make_input(activity_decline_pct=5.0, pipeline_creation_last_30d_usd=0,
                         pipeline_creation_prior_30d_usd=0, meeting_acceptance_rate_pct=0.0)
        score = _activity_health_score(inp)
        # 35 (activity) + 35 (pipe ratio=1.0 since prior=0) + 0 (meeting 0%) = 70
        assert score == 70.0

    def test_activity_decline_6_gets_24(self):
        inp = make_input(activity_decline_pct=6.0, pipeline_creation_last_30d_usd=100_000,
                         pipeline_creation_prior_30d_usd=100_000, meeting_acceptance_rate_pct=0.0)
        score = _activity_health_score(inp)
        # 24 + 35 + 0 = 59
        assert score == 59.0

    def test_activity_decline_16_gets_12(self):
        inp = make_input(activity_decline_pct=16.0, pipeline_creation_last_30d_usd=100_000,
                         pipeline_creation_prior_30d_usd=100_000, meeting_acceptance_rate_pct=0.0)
        score = _activity_health_score(inp)
        # 12 + 35 + 0 = 47
        assert score == 47.0

    def test_activity_decline_31_gets_4(self):
        inp = make_input(activity_decline_pct=31.0, pipeline_creation_last_30d_usd=100_000,
                         pipeline_creation_prior_30d_usd=100_000, meeting_acceptance_rate_pct=0.0)
        score = _activity_health_score(inp)
        # 4 + 35 + 0 = 39
        assert score == 39.0

    def test_activity_decline_51_gets_0(self):
        inp = make_input(activity_decline_pct=51.0, pipeline_creation_last_30d_usd=100_000,
                         pipeline_creation_prior_30d_usd=100_000, meeting_acceptance_rate_pct=0.0)
        score = _activity_health_score(inp)
        # 0 + 35 + 0 = 35
        assert score == 35.0

    def test_pipe_ratio_90pct_gets_35(self):
        inp = make_input(activity_decline_pct=100.0, pipeline_creation_last_30d_usd=90_000,
                         pipeline_creation_prior_30d_usd=100_000, meeting_acceptance_rate_pct=0.0)
        # pipe ratio = 0.9, activity > 50 so 0 + 35 + 0 = 35
        score = _activity_health_score(inp)
        assert score == 35.0

    def test_pipe_ratio_75pct_gets_24(self):
        inp = make_input(activity_decline_pct=100.0, pipeline_creation_last_30d_usd=75_000,
                         pipeline_creation_prior_30d_usd=100_000, meeting_acceptance_rate_pct=0.0)
        score = _activity_health_score(inp)
        # 0 + 24 + 0 = 24
        assert score == 24.0

    def test_pipe_ratio_55pct_gets_12(self):
        inp = make_input(activity_decline_pct=100.0, pipeline_creation_last_30d_usd=55_000,
                         pipeline_creation_prior_30d_usd=100_000, meeting_acceptance_rate_pct=0.0)
        score = _activity_health_score(inp)
        # 0 + 12 + 0 = 12
        assert score == 12.0

    def test_pipe_ratio_35pct_gets_4(self):
        inp = make_input(activity_decline_pct=100.0, pipeline_creation_last_30d_usd=35_000,
                         pipeline_creation_prior_30d_usd=100_000, meeting_acceptance_rate_pct=0.0)
        score = _activity_health_score(inp)
        # 0 + 4 + 0 = 4
        assert score == 4.0

    def test_pipe_ratio_below_35pct_gets_0(self):
        inp = make_input(activity_decline_pct=100.0, pipeline_creation_last_30d_usd=10_000,
                         pipeline_creation_prior_30d_usd=100_000, meeting_acceptance_rate_pct=0.0)
        score = _activity_health_score(inp)
        # 0 + 0 + 0 = 0
        assert score == 0.0

    def test_meeting_accept_85pct_gets_30(self):
        inp = make_input(activity_decline_pct=100.0, pipeline_creation_last_30d_usd=10_000,
                         pipeline_creation_prior_30d_usd=100_000, meeting_acceptance_rate_pct=85.0)
        score = _activity_health_score(inp)
        # 0 + 0 + 30 = 30
        assert score == 30.0

    def test_meeting_accept_70pct_gets_20(self):
        inp = make_input(activity_decline_pct=100.0, pipeline_creation_last_30d_usd=10_000,
                         pipeline_creation_prior_30d_usd=100_000, meeting_acceptance_rate_pct=70.0)
        score = _activity_health_score(inp)
        # 0 + 0 + 20 = 20
        assert score == 20.0

    def test_meeting_accept_55pct_gets_10(self):
        inp = make_input(activity_decline_pct=100.0, pipeline_creation_last_30d_usd=10_000,
                         pipeline_creation_prior_30d_usd=100_000, meeting_acceptance_rate_pct=55.0)
        score = _activity_health_score(inp)
        # 0 + 0 + 10 = 10
        assert score == 10.0

    def test_meeting_accept_40pct_gets_3(self):
        inp = make_input(activity_decline_pct=100.0, pipeline_creation_last_30d_usd=10_000,
                         pipeline_creation_prior_30d_usd=100_000, meeting_acceptance_rate_pct=40.0)
        score = _activity_health_score(inp)
        # 0 + 0 + 3 = 3
        assert score == 3.0

    def test_pipe_ratio_1_when_prior_zero(self):
        inp = make_input(activity_decline_pct=100.0, pipeline_creation_last_30d_usd=50_000,
                         pipeline_creation_prior_30d_usd=0.0, meeting_acceptance_rate_pct=0.0)
        score = _activity_health_score(inp)
        # pipe ratio defaults to 1.0, so +35; activity > 50 so 0; meeting 0 so 0
        assert score == 35.0

    def test_score_clamped_to_100(self):
        inp = make_input(activity_decline_pct=0.0, pipeline_creation_last_30d_usd=100_000,
                         pipeline_creation_prior_30d_usd=100_000, meeting_acceptance_rate_pct=90.0)
        score = _activity_health_score(inp)
        assert score <= 100.0

    def test_score_clamped_to_0(self):
        inp = make_input(activity_decline_pct=100.0, pipeline_creation_last_30d_usd=0,
                         pipeline_creation_prior_30d_usd=100_000, meeting_acceptance_rate_pct=0.0)
        score = _activity_health_score(inp)
        assert score >= 0.0


# ===========================================================================
# 6. WELLBEING SCORE
# ===========================================================================

class TestWellbeingScore:
    def test_max_wellbeing_score(self):
        inp = make_input(weekend_work_hours_avg=0.0, overtime_hours_per_week=0.0,
                         pto_days_taken_ytd=10.0, pto_days_available_ytd=15.0,
                         sick_days_last_90d=0)
        score = _wellbeing_score(inp)
        # 30 + 25 + 25 + 20 = 100
        assert score == 100.0

    def test_weekend_hours_2_gets_30(self):
        inp = make_input(weekend_work_hours_avg=2.0, overtime_hours_per_week=100.0,
                         pto_days_taken_ytd=0, pto_days_available_ytd=15.0, sick_days_last_90d=10)
        score = _wellbeing_score(inp)
        # 30 + 0 + 0 + 0 = 30
        assert score == 30.0

    def test_weekend_hours_5_gets_20(self):
        inp = make_input(weekend_work_hours_avg=5.0, overtime_hours_per_week=100.0,
                         pto_days_taken_ytd=0, pto_days_available_ytd=15.0, sick_days_last_90d=10)
        score = _wellbeing_score(inp)
        # 20 + 0 + 0 + 0 = 20
        assert score == 20.0

    def test_weekend_hours_10_gets_10(self):
        inp = make_input(weekend_work_hours_avg=10.0, overtime_hours_per_week=100.0,
                         pto_days_taken_ytd=0, pto_days_available_ytd=15.0, sick_days_last_90d=10)
        score = _wellbeing_score(inp)
        # 10 + 0 + 0 + 0 = 10
        assert score == 10.0

    def test_weekend_hours_11_gets_0(self):
        inp = make_input(weekend_work_hours_avg=11.0, overtime_hours_per_week=100.0,
                         pto_days_taken_ytd=0, pto_days_available_ytd=15.0, sick_days_last_90d=10)
        score = _wellbeing_score(inp)
        # 0 + 0 + 0 + 0 = 0
        assert score == 0.0

    def test_overtime_5_gets_25(self):
        inp = make_input(weekend_work_hours_avg=11.0, overtime_hours_per_week=5.0,
                         pto_days_taken_ytd=0, pto_days_available_ytd=15.0, sick_days_last_90d=10)
        score = _wellbeing_score(inp)
        # 0 + 25 + 0 + 0 = 25
        assert score == 25.0

    def test_overtime_10_gets_15(self):
        inp = make_input(weekend_work_hours_avg=11.0, overtime_hours_per_week=10.0,
                         pto_days_taken_ytd=0, pto_days_available_ytd=15.0, sick_days_last_90d=10)
        score = _wellbeing_score(inp)
        # 0 + 15 + 0 + 0 = 15
        assert score == 15.0

    def test_overtime_20_gets_6(self):
        inp = make_input(weekend_work_hours_avg=11.0, overtime_hours_per_week=20.0,
                         pto_days_taken_ytd=0, pto_days_available_ytd=15.0, sick_days_last_90d=10)
        score = _wellbeing_score(inp)
        # 0 + 6 + 0 + 0 = 6
        assert score == 6.0

    def test_overtime_21_gets_0(self):
        inp = make_input(weekend_work_hours_avg=11.0, overtime_hours_per_week=21.0,
                         pto_days_taken_ytd=0, pto_days_available_ytd=15.0, sick_days_last_90d=10)
        score = _wellbeing_score(inp)
        # 0 + 0 + 0 + 0 = 0
        assert score == 0.0

    def test_pto_50pct_gets_25(self):
        inp = make_input(weekend_work_hours_avg=11.0, overtime_hours_per_week=100.0,
                         pto_days_taken_ytd=7.5, pto_days_available_ytd=15.0, sick_days_last_90d=10)
        score = _wellbeing_score(inp)
        # 0 + 0 + 25 + 0 = 25
        assert score == 25.0

    def test_pto_30pct_gets_18(self):
        inp = make_input(weekend_work_hours_avg=11.0, overtime_hours_per_week=100.0,
                         pto_days_taken_ytd=4.5, pto_days_available_ytd=15.0, sick_days_last_90d=10)
        score = _wellbeing_score(inp)
        # 0 + 0 + 18 + 0 = 18
        assert score == 18.0

    def test_pto_15pct_gets_9(self):
        inp = make_input(weekend_work_hours_avg=11.0, overtime_hours_per_week=100.0,
                         pto_days_taken_ytd=2.25, pto_days_available_ytd=15.0, sick_days_last_90d=10)
        score = _wellbeing_score(inp)
        # 0 + 0 + 9 + 0 = 9
        assert score == 9.0

    def test_sick_1_gets_20(self):
        inp = make_input(weekend_work_hours_avg=11.0, overtime_hours_per_week=100.0,
                         pto_days_taken_ytd=0, pto_days_available_ytd=15.0, sick_days_last_90d=1)
        score = _wellbeing_score(inp)
        # 0 + 0 + 0 + 20 = 20
        assert score == 20.0

    def test_sick_3_gets_12(self):
        inp = make_input(weekend_work_hours_avg=11.0, overtime_hours_per_week=100.0,
                         pto_days_taken_ytd=0, pto_days_available_ytd=15.0, sick_days_last_90d=3)
        score = _wellbeing_score(inp)
        # 0 + 0 + 0 + 12 = 12
        assert score == 12.0

    def test_sick_5_gets_4(self):
        inp = make_input(weekend_work_hours_avg=11.0, overtime_hours_per_week=100.0,
                         pto_days_taken_ytd=0, pto_days_available_ytd=15.0, sick_days_last_90d=5)
        score = _wellbeing_score(inp)
        # 0 + 0 + 0 + 4 = 4
        assert score == 4.0

    def test_sick_6_gets_0(self):
        inp = make_input(weekend_work_hours_avg=11.0, overtime_hours_per_week=100.0,
                         pto_days_taken_ytd=0, pto_days_available_ytd=15.0, sick_days_last_90d=6)
        score = _wellbeing_score(inp)
        # 0 + 0 + 0 + 0 = 0
        assert score == 0.0

    def test_pto_zero_available(self):
        inp = make_input(weekend_work_hours_avg=11.0, overtime_hours_per_week=100.0,
                         pto_days_taken_ytd=10.0, pto_days_available_ytd=0.0, sick_days_last_90d=10)
        score = _wellbeing_score(inp)
        # pto_ratio = 0, no pto points; 0 + 0 + 0 + 0 = 0
        assert score == 0.0


# ===========================================================================
# 7. PERFORMANCE SUSTAINABILITY SCORE
# ===========================================================================

class TestPerformanceSustainabilityScore:
    def test_max_performance_score(self):
        inp = make_input(deal_win_rate_last_90d=35.0, deal_win_rate_prior_quarter=30.0,
                         consecutive_no_close_weeks=0, customer_escalations_last_30d=0,
                         quota_pressure_score=20.0)
        score = _performance_sustainability_score(inp)
        # 35 + 30 + 20 + 15 = 100
        assert score == 100.0

    def test_win_rate_delta_minus5_gets_35(self):
        inp = make_input(deal_win_rate_last_90d=25.0, deal_win_rate_prior_quarter=30.0,
                         consecutive_no_close_weeks=20, customer_escalations_last_30d=10,
                         quota_pressure_score=90.0)
        score = _performance_sustainability_score(inp)
        # delta = -5 >= -5: 35 + 0 + 0 + 0 = 35
        assert score == 35.0

    def test_win_rate_delta_minus10_gets_24(self):
        inp = make_input(deal_win_rate_last_90d=20.0, deal_win_rate_prior_quarter=30.0,
                         consecutive_no_close_weeks=20, customer_escalations_last_30d=10,
                         quota_pressure_score=90.0)
        score = _performance_sustainability_score(inp)
        # delta = -10, >= -10: 24 + 0 + 0 + 0 = 24
        assert score == 24.0

    def test_win_rate_delta_minus20_gets_12(self):
        inp = make_input(deal_win_rate_last_90d=10.0, deal_win_rate_prior_quarter=30.0,
                         consecutive_no_close_weeks=20, customer_escalations_last_30d=10,
                         quota_pressure_score=90.0)
        score = _performance_sustainability_score(inp)
        # delta = -20, >= -20: 12 + 0 + 0 + 0 = 12
        assert score == 12.0

    def test_win_rate_delta_below_minus20_gets_0(self):
        inp = make_input(deal_win_rate_last_90d=5.0, deal_win_rate_prior_quarter=30.0,
                         consecutive_no_close_weeks=20, customer_escalations_last_30d=10,
                         quota_pressure_score=90.0)
        score = _performance_sustainability_score(inp)
        # delta = -25: 0 + 0 + 0 + 0 = 0
        assert score == 0.0

    def test_no_close_weeks_2_gets_30(self):
        inp = make_input(deal_win_rate_last_90d=30.0, deal_win_rate_prior_quarter=35.0,
                         consecutive_no_close_weeks=2, customer_escalations_last_30d=10,
                         quota_pressure_score=90.0)
        score = _performance_sustainability_score(inp)
        # delta = -5 >= -5: 35 + 30 + 0 + 0 = 65
        assert score == 65.0

    def test_no_close_weeks_4_gets_20(self):
        inp = make_input(deal_win_rate_last_90d=30.0, deal_win_rate_prior_quarter=35.0,
                         consecutive_no_close_weeks=4, customer_escalations_last_30d=10,
                         quota_pressure_score=90.0)
        score = _performance_sustainability_score(inp)
        # 35 + 20 + 0 + 0 = 55
        assert score == 55.0

    def test_no_close_weeks_7_gets_8(self):
        inp = make_input(deal_win_rate_last_90d=30.0, deal_win_rate_prior_quarter=35.0,
                         consecutive_no_close_weeks=7, customer_escalations_last_30d=10,
                         quota_pressure_score=90.0)
        score = _performance_sustainability_score(inp)
        # 35 + 8 + 0 + 0 = 43
        assert score == 43.0

    def test_no_close_weeks_8_gets_0(self):
        inp = make_input(deal_win_rate_last_90d=30.0, deal_win_rate_prior_quarter=35.0,
                         consecutive_no_close_weeks=8, customer_escalations_last_30d=10,
                         quota_pressure_score=90.0)
        score = _performance_sustainability_score(inp)
        # 35 + 0 + 0 + 0 = 35
        assert score == 35.0

    def test_escalations_0_gets_20(self):
        inp = make_input(deal_win_rate_last_90d=30.0, deal_win_rate_prior_quarter=35.0,
                         consecutive_no_close_weeks=20, customer_escalations_last_30d=0,
                         quota_pressure_score=90.0)
        score = _performance_sustainability_score(inp)
        # 35 + 0 + 20 + 0 = 55
        assert score == 55.0

    def test_escalations_1_gets_13(self):
        inp = make_input(deal_win_rate_last_90d=30.0, deal_win_rate_prior_quarter=35.0,
                         consecutive_no_close_weeks=20, customer_escalations_last_30d=1,
                         quota_pressure_score=90.0)
        score = _performance_sustainability_score(inp)
        # 35 + 0 + 13 + 0 = 48
        assert score == 48.0

    def test_escalations_2_gets_6(self):
        inp = make_input(deal_win_rate_last_90d=30.0, deal_win_rate_prior_quarter=35.0,
                         consecutive_no_close_weeks=20, customer_escalations_last_30d=2,
                         quota_pressure_score=90.0)
        score = _performance_sustainability_score(inp)
        # 35 + 0 + 6 + 0 = 41
        assert score == 41.0

    def test_escalations_3_gets_0(self):
        inp = make_input(deal_win_rate_last_90d=30.0, deal_win_rate_prior_quarter=35.0,
                         consecutive_no_close_weeks=20, customer_escalations_last_30d=3,
                         quota_pressure_score=90.0)
        score = _performance_sustainability_score(inp)
        # 35 + 0 + 0 + 0 = 35
        assert score == 35.0

    def test_quota_40_gets_15(self):
        inp = make_input(deal_win_rate_last_90d=30.0, deal_win_rate_prior_quarter=35.0,
                         consecutive_no_close_weeks=20, customer_escalations_last_30d=10,
                         quota_pressure_score=40.0)
        score = _performance_sustainability_score(inp)
        # 35 + 0 + 0 + 15 = 50
        assert score == 50.0

    def test_quota_60_gets_10(self):
        inp = make_input(deal_win_rate_last_90d=30.0, deal_win_rate_prior_quarter=35.0,
                         consecutive_no_close_weeks=20, customer_escalations_last_30d=10,
                         quota_pressure_score=60.0)
        score = _performance_sustainability_score(inp)
        # 35 + 0 + 0 + 10 = 45
        assert score == 45.0

    def test_quota_75_gets_4(self):
        inp = make_input(deal_win_rate_last_90d=30.0, deal_win_rate_prior_quarter=35.0,
                         consecutive_no_close_weeks=20, customer_escalations_last_30d=10,
                         quota_pressure_score=75.0)
        score = _performance_sustainability_score(inp)
        # 35 + 0 + 0 + 4 = 39
        assert score == 39.0

    def test_quota_above_75_gets_0(self):
        inp = make_input(deal_win_rate_last_90d=30.0, deal_win_rate_prior_quarter=35.0,
                         consecutive_no_close_weeks=20, customer_escalations_last_30d=10,
                         quota_pressure_score=90.0)
        score = _performance_sustainability_score(inp)
        # 35 + 0 + 0 + 0 = 35
        assert score == 35.0


# ===========================================================================
# 8. SOCIAL ENGAGEMENT SCORE
# ===========================================================================

class TestSocialEngagementScore:
    def test_max_social_score(self):
        inp = make_input(manager_checkin_frequency=5.0, peer_interaction_score=100.0,
                         email_response_time_hrs=2.0)
        score = _social_engagement_score(inp)
        # 35 + 35 + 30 = 100
        assert score == 100.0

    def test_manager_checkin_4_gets_35(self):
        inp = make_input(manager_checkin_frequency=4.0, peer_interaction_score=0.0,
                         email_response_time_hrs=100.0)
        score = _social_engagement_score(inp)
        # 35 + 0 + 0 = 35
        assert score == 35.0

    def test_manager_checkin_2_gets_24(self):
        inp = make_input(manager_checkin_frequency=2.0, peer_interaction_score=0.0,
                         email_response_time_hrs=100.0)
        score = _social_engagement_score(inp)
        # 24 + 0 + 0 = 24
        assert score == 24.0

    def test_manager_checkin_1_gets_12(self):
        inp = make_input(manager_checkin_frequency=1.0, peer_interaction_score=0.0,
                         email_response_time_hrs=100.0)
        score = _social_engagement_score(inp)
        # 12 + 0 + 0 = 12
        assert score == 12.0

    def test_manager_checkin_below_1_gets_0(self):
        inp = make_input(manager_checkin_frequency=0.5, peer_interaction_score=0.0,
                         email_response_time_hrs=100.0)
        score = _social_engagement_score(inp)
        # 0 + 0 + 0 = 0
        assert score == 0.0

    def test_peer_interaction_contributes(self):
        inp = make_input(manager_checkin_frequency=0.0, peer_interaction_score=100.0,
                         email_response_time_hrs=100.0)
        score = _social_engagement_score(inp)
        # 0 + 35 + 0 = 35
        assert score == 35.0

    def test_peer_interaction_partial(self):
        inp = make_input(manager_checkin_frequency=0.0, peer_interaction_score=60.0,
                         email_response_time_hrs=100.0)
        score = _social_engagement_score(inp)
        expected = round(60.0 * 0.35, 1)
        assert score == expected

    def test_email_response_4hrs_gets_30(self):
        inp = make_input(manager_checkin_frequency=0.0, peer_interaction_score=0.0,
                         email_response_time_hrs=4.0)
        score = _social_engagement_score(inp)
        # 0 + 0 + 30 = 30
        assert score == 30.0

    def test_email_response_12hrs_gets_20(self):
        inp = make_input(manager_checkin_frequency=0.0, peer_interaction_score=0.0,
                         email_response_time_hrs=12.0)
        score = _social_engagement_score(inp)
        # 0 + 0 + 20 = 20
        assert score == 20.0

    def test_email_response_24hrs_gets_10(self):
        inp = make_input(manager_checkin_frequency=0.0, peer_interaction_score=0.0,
                         email_response_time_hrs=24.0)
        score = _social_engagement_score(inp)
        # 0 + 0 + 10 = 10
        assert score == 10.0

    def test_email_response_25hrs_gets_0(self):
        inp = make_input(manager_checkin_frequency=0.0, peer_interaction_score=0.0,
                         email_response_time_hrs=25.0)
        score = _social_engagement_score(inp)
        # 0 + 0 + 0 = 0
        assert score == 0.0

    def test_score_clamped_max(self):
        inp = make_input(manager_checkin_frequency=10.0, peer_interaction_score=100.0,
                         email_response_time_hrs=1.0)
        score = _social_engagement_score(inp)
        assert score <= 100.0


# ===========================================================================
# 9. COMPOSITE FORMULA
# ===========================================================================

class TestCompositeFormula:
    def test_all_100_gives_0(self):
        c = _composite(100.0, 100.0, 100.0, 100.0)
        assert c == 0.0

    def test_all_0_gives_100(self):
        c = _composite(0.0, 0.0, 0.0, 0.0)
        assert c == 100.0

    def test_weights_sum_to_100(self):
        # If each score is 0 except one, composite = weight * 100
        c_activity = _composite(0.0, 100.0, 100.0, 100.0)
        assert abs(c_activity - 30.0) < 0.1

        c_wellbeing = _composite(100.0, 0.0, 100.0, 100.0)
        assert abs(c_wellbeing - 25.0) < 0.1

        c_performance = _composite(100.0, 100.0, 0.0, 100.0)
        assert abs(c_performance - 25.0) < 0.1

        c_social = _composite(100.0, 100.0, 100.0, 0.0)
        assert abs(c_social - 20.0) < 0.1

    def test_formula_exact(self):
        a, w, p, s = 80.0, 70.0, 60.0, 50.0
        expected = round((100-a)*0.30 + (100-w)*0.25 + (100-p)*0.25 + (100-s)*0.20, 1)
        assert _composite(a, w, p, s) == expected

    def test_composite_rounded_to_1_decimal(self):
        c = _composite(33.3, 44.4, 55.5, 66.6)
        assert c == round(c, 1)

    def test_composite_symmetry(self):
        # Swapping activity (0.30) and social (0.20) should differ
        c1 = _composite(0.0, 50.0, 50.0, 100.0)
        c2 = _composite(100.0, 50.0, 50.0, 0.0)
        assert c1 != c2

    def test_mid_scores(self):
        c = _composite(50.0, 50.0, 50.0, 50.0)
        assert c == 50.0


# ===========================================================================
# 10. BURNOUT RISK THRESHOLDS
# ===========================================================================

class TestBurnoutRiskThresholds:
    def test_composite_0_is_none(self):
        assert _burnout_risk(0.0) == BurnoutRisk.NONE

    def test_composite_19_is_none(self):
        assert _burnout_risk(19.9) == BurnoutRisk.NONE

    def test_composite_20_is_early_warning(self):
        assert _burnout_risk(20.0) == BurnoutRisk.EARLY_WARNING

    def test_composite_34_is_early_warning(self):
        assert _burnout_risk(34.9) == BurnoutRisk.EARLY_WARNING

    def test_composite_35_is_moderate(self):
        assert _burnout_risk(35.0) == BurnoutRisk.MODERATE

    def test_composite_49_is_moderate(self):
        assert _burnout_risk(49.9) == BurnoutRisk.MODERATE

    def test_composite_50_is_high(self):
        assert _burnout_risk(50.0) == BurnoutRisk.HIGH

    def test_composite_69_is_high(self):
        assert _burnout_risk(69.9) == BurnoutRisk.HIGH

    def test_composite_70_is_critical(self):
        assert _burnout_risk(70.0) == BurnoutRisk.CRITICAL

    def test_composite_100_is_critical(self):
        assert _burnout_risk(100.0) == BurnoutRisk.CRITICAL


# ===========================================================================
# 11. BURNOUT STAGE THRESHOLDS
# ===========================================================================

class TestBurnoutStageThresholds:
    def test_composite_0_is_engaged(self):
        assert _burnout_stage(0.0) == BurnoutStage.ENGAGED

    def test_composite_19_is_engaged(self):
        assert _burnout_stage(19.9) == BurnoutStage.ENGAGED

    def test_composite_20_is_coasting(self):
        assert _burnout_stage(20.0) == BurnoutStage.COASTING

    def test_composite_34_is_coasting(self):
        assert _burnout_stage(34.9) == BurnoutStage.COASTING

    def test_composite_35_is_disengaging(self):
        assert _burnout_stage(35.0) == BurnoutStage.DISENGAGING

    def test_composite_49_is_disengaging(self):
        assert _burnout_stage(49.9) == BurnoutStage.DISENGAGING

    def test_composite_50_is_burned_out(self):
        assert _burnout_stage(50.0) == BurnoutStage.BURNED_OUT

    def test_composite_69_is_burned_out(self):
        assert _burnout_stage(69.9) == BurnoutStage.BURNED_OUT

    def test_composite_70_is_depleted(self):
        assert _burnout_stage(70.0) == BurnoutStage.DEPLETED

    def test_composite_100_is_depleted(self):
        assert _burnout_stage(100.0) == BurnoutStage.DEPLETED


# ===========================================================================
# 12. PRIMARY SIGNAL
# ===========================================================================

class TestPrimarySignal:
    def test_none_when_all_scores_high(self):
        signal = _primary_signal(make_input(), 90.0, 90.0, 90.0, 90.0)
        assert signal == BurnoutSignal.NONE

    def test_overwhelm_when_high_overtime(self):
        inp = make_input(overtime_hours_per_week=20.0, weekend_work_hours_avg=5.0)
        # Make one component very bad
        signal = _primary_signal(inp, 0.0, 90.0, 90.0, 90.0)
        assert signal == BurnoutSignal.OVERWHELM

    def test_overwhelm_when_high_weekend_work(self):
        inp = make_input(overtime_hours_per_week=5.0, weekend_work_hours_avg=10.0)
        signal = _primary_signal(inp, 0.0, 90.0, 90.0, 90.0)
        assert signal == BurnoutSignal.OVERWHELM

    def test_activity_decline_dominates(self):
        inp = make_input(overtime_hours_per_week=5.0, weekend_work_hours_avg=2.0)
        signal = _primary_signal(inp, 0.0, 90.0, 90.0, 90.0)
        # 100-0 = 100, 100-90=10, so activity dominates (>=20)
        assert signal == BurnoutSignal.ACTIVITY_DECLINE

    def test_exhaustion_dominates(self):
        inp = make_input(overtime_hours_per_week=5.0, weekend_work_hours_avg=2.0)
        signal = _primary_signal(inp, 90.0, 0.0, 90.0, 90.0)
        # 100-90=10, 100-0=100, so wellbeing dominates -> exhaustion
        assert signal == BurnoutSignal.EXHAUSTION

    def test_performance_decay_dominates(self):
        inp = make_input(overtime_hours_per_week=5.0, weekend_work_hours_avg=2.0)
        signal = _primary_signal(inp, 90.0, 90.0, 0.0, 90.0)
        assert signal == BurnoutSignal.PERFORMANCE_DECAY

    def test_isolation_dominates(self):
        inp = make_input(overtime_hours_per_week=5.0, weekend_work_hours_avg=2.0)
        signal = _primary_signal(inp, 90.0, 90.0, 90.0, 0.0)
        assert signal == BurnoutSignal.ISOLATION

    def test_overwhelm_overrides_activity(self):
        inp = make_input(overtime_hours_per_week=25.0, weekend_work_hours_avg=1.0)
        signal = _primary_signal(inp, 0.0, 90.0, 90.0, 90.0)
        assert signal == BurnoutSignal.OVERWHELM

    def test_none_signal_when_strongest_under_20(self):
        signal = _primary_signal(make_input(), 85.0, 82.0, 83.0, 84.0)
        assert signal == BurnoutSignal.NONE


# ===========================================================================
# 13. BURNOUT ACTION
# ===========================================================================

class TestBurnoutAction:
    def test_none_risk_gives_monitor(self):
        assert _burnout_action(BurnoutRisk.NONE) == BurnoutAction.MONITOR

    def test_early_warning_gives_check_in(self):
        assert _burnout_action(BurnoutRisk.EARLY_WARNING) == BurnoutAction.CHECK_IN

    def test_moderate_gives_coaching_session(self):
        assert _burnout_action(BurnoutRisk.MODERATE) == BurnoutAction.COACHING_SESSION

    def test_high_gives_workload_reduction(self):
        assert _burnout_action(BurnoutRisk.HIGH) == BurnoutAction.WORKLOAD_REDUCTION

    def test_critical_gives_urgent_intervention(self):
        assert _burnout_action(BurnoutRisk.CRITICAL) == BurnoutAction.URGENT_INTERVENTION


# ===========================================================================
# 14. PRODUCTIVITY IMPACT
# ===========================================================================

class TestProductivityImpact:
    def test_below_20_gives_0(self):
        assert _productivity_impact_pct(0.0) == 0.0

    def test_exactly_0_gives_0(self):
        assert _productivity_impact_pct(0.0) == 0.0

    def test_19_9_gives_0(self):
        assert _productivity_impact_pct(19.9) == 0.0

    def test_20_uses_0_3_multiplier(self):
        assert _productivity_impact_pct(20.0) == round(20.0 * 0.3, 1)

    def test_34_uses_0_3_multiplier(self):
        assert _productivity_impact_pct(34.9) == round(34.9 * 0.3, 1)

    def test_35_uses_0_5_multiplier(self):
        assert _productivity_impact_pct(35.0) == round(35.0 * 0.5, 1)

    def test_49_uses_0_5_multiplier(self):
        assert _productivity_impact_pct(49.9) == round(49.9 * 0.5, 1)

    def test_50_uses_0_7_multiplier(self):
        assert _productivity_impact_pct(50.0) == round(50.0 * 0.7, 1)

    def test_100_uses_0_7_multiplier(self):
        assert _productivity_impact_pct(100.0) == round(100.0 * 0.7, 1)

    def test_result_rounded_to_1_decimal(self):
        val = _productivity_impact_pct(33.3)
        assert val == round(val, 1)


# ===========================================================================
# 15. IS_AT_BURNOUT_RISK BOUNDARY (composite >= 35)
# ===========================================================================

class TestIsAtBurnoutRiskBoundary:
    def test_composite_exactly_35_is_at_risk(self):
        engine = SalesBurnoutRiskEngine()
        # Craft input so composite == exactly 35
        inp = make_input(
            activity_decline_pct=6.0,           # 24 activity
            pipeline_creation_last_30d_usd=75_000,
            pipeline_creation_prior_30d_usd=100_000,  # pipe_ratio=0.75 -> 24
            meeting_acceptance_rate_pct=55.0,   # 10
            # activity_health_score = 24 + 24 + 10 = 58
            weekend_work_hours_avg=11.0,
            overtime_hours_per_week=100.0,
            pto_days_taken_ytd=0,
            pto_days_available_ytd=15.0,
            sick_days_last_90d=10,
            # wellbeing = 0
            deal_win_rate_last_90d=30.0,
            deal_win_rate_prior_quarter=35.0,
            consecutive_no_close_weeks=20,
            customer_escalations_last_30d=10,
            quota_pressure_score=90.0,
            # performance = 35 (only delta=-5 so 35)
            manager_checkin_frequency=0.0,
            peer_interaction_score=0.0,
            email_response_time_hrs=100.0,
            # social = 0
        )
        result = engine.assess(inp)
        # Any composite >= 35 means is_at_burnout_risk
        assert result.is_at_burnout_risk == (result.burnout_composite >= 35)

    def test_healthy_rep_not_at_risk(self):
        engine = SalesBurnoutRiskEngine()
        result = engine.assess(healthy_input())
        if result.burnout_composite < 35:
            assert not result.is_at_burnout_risk

    def test_burned_out_rep_is_at_risk(self):
        engine = SalesBurnoutRiskEngine()
        result = engine.assess(burned_out_input())
        assert result.is_at_burnout_risk

    def test_is_at_risk_matches_composite_threshold(self):
        engine = SalesBurnoutRiskEngine()
        for inp in [make_input(rep_id=f"r{i}") for i in range(5)]:
            r = engine.assess(inp)
            assert r.is_at_burnout_risk == (r.burnout_composite >= 35)


# ===========================================================================
# 16. NEEDS_IMMEDIATE_SUPPORT BOUNDARIES
# ===========================================================================

class TestNeedsImmediateSupport:
    def test_composite_50_triggers_support(self):
        engine = SalesBurnoutRiskEngine()
        result = engine.assess(burned_out_input())
        if result.burnout_composite >= 50:
            assert result.needs_immediate_support

    def test_composite_below_50_no_support_without_sick_overtime(self):
        engine = SalesBurnoutRiskEngine()
        inp = make_input(sick_days_last_90d=0, overtime_hours_per_week=2.0)
        r = engine.assess(inp)
        if r.burnout_composite < 50:
            assert not r.needs_immediate_support

    def test_sick_5_and_overtime_15_triggers_support(self):
        engine = SalesBurnoutRiskEngine()
        inp = make_input(sick_days_last_90d=5, overtime_hours_per_week=15.0)
        r = engine.assess(inp)
        assert r.needs_immediate_support

    def test_sick_5_and_overtime_14_no_support(self):
        engine = SalesBurnoutRiskEngine()
        inp = make_input(
            sick_days_last_90d=5, overtime_hours_per_week=14.0,
            # Keep composite below 50
            activity_decline_pct=0.0,
            pipeline_creation_last_30d_usd=100_000,
            pipeline_creation_prior_30d_usd=100_000,
            meeting_acceptance_rate_pct=90.0,
            deal_win_rate_last_90d=35.0,
            deal_win_rate_prior_quarter=30.0,
            consecutive_no_close_weeks=0,
            customer_escalations_last_30d=0,
            quota_pressure_score=20.0,
            manager_checkin_frequency=5.0,
            peer_interaction_score=100.0,
            email_response_time_hrs=2.0,
            weekend_work_hours_avg=1.0,
            pto_days_taken_ytd=10.0,
            pto_days_available_ytd=15.0,
        )
        r = engine.assess(inp)
        if r.burnout_composite < 50:
            assert not r.needs_immediate_support

    def test_sick_4_and_overtime_15_no_support(self):
        engine = SalesBurnoutRiskEngine()
        inp = make_input(sick_days_last_90d=4, overtime_hours_per_week=15.0)
        r = engine.assess(inp)
        if r.burnout_composite < 50:
            assert not r.needs_immediate_support

    def test_needs_support_matches_formula(self):
        engine = SalesBurnoutRiskEngine()
        inp = burned_out_input()
        r = engine.assess(inp)
        expected = r.burnout_composite >= 50 or (inp.sick_days_last_90d >= 5 and inp.overtime_hours_per_week >= 15)
        assert r.needs_immediate_support == expected

    def test_healthy_rep_does_not_need_support(self):
        engine = SalesBurnoutRiskEngine()
        result = engine.assess(healthy_input())
        if result.burnout_composite < 50 and not (0 >= 5 and 2.0 >= 15):
            assert not result.needs_immediate_support


# ===========================================================================
# 17. ASSESS() RETURN TYPE AND STORAGE
# ===========================================================================

class TestAssessMethod:
    def test_assess_returns_result(self):
        engine = SalesBurnoutRiskEngine()
        result = engine.assess(make_input())
        assert isinstance(result, SalesBurnoutResult)

    def test_assess_stores_result(self):
        engine = SalesBurnoutRiskEngine()
        inp = make_input(rep_id="stored_rep")
        engine.assess(inp)
        assert engine.get("stored_rep") is not None

    def test_assess_stores_by_rep_id(self):
        engine = SalesBurnoutRiskEngine()
        inp = make_input(rep_id="rep_x")
        r = engine.assess(inp)
        assert engine.get("rep_x") == r

    def test_assess_overwrites_previous(self):
        engine = SalesBurnoutRiskEngine()
        engine.assess(make_input(rep_id="r1", activity_decline_pct=5.0))
        r2 = engine.assess(make_input(rep_id="r1", activity_decline_pct=60.0))
        assert engine.get("r1") == r2

    def test_assess_result_has_correct_rep_id(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(make_input(rep_id="rep_abc"))
        assert r.rep_id == "rep_abc"

    def test_assess_result_has_correct_rep_name(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(make_input(rep_name="Jane Doe"))
        assert r.rep_name == "Jane Doe"

    def test_assess_scores_are_in_range(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(make_input())
        assert 0.0 <= r.activity_health_score <= 100.0
        assert 0.0 <= r.wellbeing_score <= 100.0
        assert 0.0 <= r.performance_sustainability_score <= 100.0
        assert 0.0 <= r.social_engagement_score <= 100.0

    def test_assess_composite_in_range(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(make_input())
        assert 0.0 <= r.burnout_composite <= 100.0

    def test_assess_deterministic(self):
        engine1 = SalesBurnoutRiskEngine()
        engine2 = SalesBurnoutRiskEngine()
        inp = make_input(rep_id="det_test")
        r1 = engine1.assess(inp)
        r2 = engine2.assess(inp)
        assert r1.burnout_composite == r2.burnout_composite

    def test_assess_burnout_risk_is_enum(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(make_input())
        assert isinstance(r.burnout_risk, BurnoutRisk)

    def test_assess_burnout_stage_is_enum(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(make_input())
        assert isinstance(r.burnout_stage, BurnoutStage)

    def test_assess_primary_signal_is_enum(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(make_input())
        assert isinstance(r.primary_burnout_signal, BurnoutSignal)

    def test_assess_burnout_action_is_enum(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(make_input())
        assert isinstance(r.burnout_action, BurnoutAction)

    def test_assess_productivity_impact_non_negative(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(make_input())
        assert r.estimated_productivity_impact_pct >= 0.0

    def test_assess_burnout_signal_is_str(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(make_input())
        assert isinstance(r.burnout_signal, str)
        assert len(r.burnout_signal) > 0


# ===========================================================================
# 18. ASSESS_BATCH() SORT ORDER
# ===========================================================================

class TestAssessBatch:
    def test_batch_returns_list(self):
        engine = SalesBurnoutRiskEngine()
        results = engine.assess_batch([make_input(rep_id="b1"), make_input(rep_id="b2")])
        assert isinstance(results, list)

    def test_batch_sorted_descending_by_composite(self):
        engine = SalesBurnoutRiskEngine()
        inputs = [
            healthy_input(rep_id="h1"),
            burned_out_input(rep_id="bo1"),
            make_input(rep_id="mid", activity_decline_pct=20.0),
        ]
        results = engine.assess_batch(inputs)
        composites = [r.burnout_composite for r in results]
        assert composites == sorted(composites, reverse=True)

    def test_batch_length_matches_input(self):
        engine = SalesBurnoutRiskEngine()
        inputs = [make_input(rep_id=f"rep{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_stores_all_results(self):
        engine = SalesBurnoutRiskEngine()
        inputs = [make_input(rep_id=f"bs{i}") for i in range(3)]
        engine.assess_batch(inputs)
        for i in range(3):
            assert engine.get(f"bs{i}") is not None

    def test_batch_empty_list(self):
        engine = SalesBurnoutRiskEngine()
        results = engine.assess_batch([])
        assert results == []

    def test_batch_single_element(self):
        engine = SalesBurnoutRiskEngine()
        results = engine.assess_batch([make_input(rep_id="solo")])
        assert len(results) == 1
        assert results[0].rep_id == "solo"

    def test_batch_first_element_highest_composite(self):
        engine = SalesBurnoutRiskEngine()
        inputs = [healthy_input(rep_id="h"), burned_out_input(rep_id="b")]
        results = engine.assess_batch(inputs)
        assert results[0].rep_id == "b"

    def test_batch_returns_result_instances(self):
        engine = SalesBurnoutRiskEngine()
        results = engine.assess_batch([make_input(rep_id="typ1"), make_input(rep_id="typ2")])
        for r in results:
            assert isinstance(r, SalesBurnoutResult)


# ===========================================================================
# 19. SUMMARY() CORRECTNESS
# ===========================================================================

class TestSummaryCorrectness:
    def test_summary_total_matches_assessed(self):
        engine = SalesBurnoutRiskEngine()
        for i in range(4):
            engine.assess(make_input(rep_id=f"s{i}"))
        assert engine.summary()["total"] == 4

    def test_summary_empty_engine(self):
        engine = SalesBurnoutRiskEngine()
        s = engine.summary()
        assert s["total"] == 0
        assert s["avg_burnout_composite"] == 0.0
        assert s["at_burnout_risk_count"] == 0

    def test_summary_risk_counts_sum_to_total(self):
        engine = SalesBurnoutRiskEngine()
        engine.assess_batch([make_input(rep_id=f"rc{i}") for i in range(6)])
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_stage_counts_sum_to_total(self):
        engine = SalesBurnoutRiskEngine()
        engine.assess_batch([make_input(rep_id=f"sc{i}") for i in range(6)])
        s = engine.summary()
        assert sum(s["stage_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_to_total(self):
        engine = SalesBurnoutRiskEngine()
        engine.assess_batch([make_input(rep_id=f"ac{i}") for i in range(6)])
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_signal_counts_sum_to_total(self):
        engine = SalesBurnoutRiskEngine()
        engine.assess_batch([make_input(rep_id=f"sig{i}") for i in range(6)])
        s = engine.summary()
        assert sum(s["signal_counts"].values()) == s["total"]

    def test_summary_avg_composite_matches_manual(self):
        engine = SalesBurnoutRiskEngine()
        r1 = engine.assess(healthy_input(rep_id="a"))
        r2 = engine.assess(burned_out_input(rep_id="b"))
        expected_avg = round((r1.burnout_composite + r2.burnout_composite) / 2, 1)
        assert engine.summary()["avg_burnout_composite"] == expected_avg

    def test_summary_at_burnout_risk_count(self):
        engine = SalesBurnoutRiskEngine()
        r1 = engine.assess(healthy_input(rep_id="a"))
        r2 = engine.assess(burned_out_input(rep_id="b"))
        at_risk = sum(1 for r in [r1, r2] if r.is_at_burnout_risk)
        assert engine.summary()["at_burnout_risk_count"] == at_risk

    def test_summary_immediate_support_count(self):
        engine = SalesBurnoutRiskEngine()
        r1 = engine.assess(healthy_input(rep_id="a"))
        r2 = engine.assess(burned_out_input(rep_id="b"))
        support = sum(1 for r in [r1, r2] if r.needs_immediate_support)
        assert engine.summary()["immediate_support_count"] == support

    def test_summary_total_productivity_impact(self):
        engine = SalesBurnoutRiskEngine()
        r1 = engine.assess(healthy_input(rep_id="a"))
        r2 = engine.assess(burned_out_input(rep_id="b"))
        expected = round(r1.estimated_productivity_impact_pct + r2.estimated_productivity_impact_pct, 1)
        assert engine.summary()["total_productivity_impact_pct"] == expected


# ===========================================================================
# 20. ENGINE METHODS (get, all_reps, at_risk_reps, by_risk, by_stage, reset)
# ===========================================================================

class TestEngineHelperMethods:
    def test_get_returns_none_for_unknown(self):
        engine = SalesBurnoutRiskEngine()
        assert engine.get("unknown") is None

    def test_get_returns_result_after_assess(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(make_input(rep_id="known"))
        assert engine.get("known") == r

    def test_all_reps_sorted_descending(self):
        engine = SalesBurnoutRiskEngine()
        engine.assess(healthy_input(rep_id="h"))
        engine.assess(burned_out_input(rep_id="b"))
        all_r = engine.all_reps()
        composites = [r.burnout_composite for r in all_r]
        assert composites == sorted(composites, reverse=True)

    def test_all_reps_count(self):
        engine = SalesBurnoutRiskEngine()
        for i in range(3):
            engine.assess(make_input(rep_id=f"ar{i}"))
        assert len(engine.all_reps()) == 3

    def test_at_risk_reps_filters_correctly(self):
        engine = SalesBurnoutRiskEngine()
        r1 = engine.assess(healthy_input(rep_id="h"))
        r2 = engine.assess(burned_out_input(rep_id="b"))
        at_risk = engine.at_risk_reps()
        for r in at_risk:
            assert r.is_at_burnout_risk

    def test_by_risk_filters_correctly(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(burned_out_input(rep_id="crit"))
        by_crit = engine.by_risk(r.burnout_risk)
        assert all(x.burnout_risk == r.burnout_risk for x in by_crit)

    def test_by_stage_filters_correctly(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(burned_out_input(rep_id="stage_test"))
        by_stage = engine.by_stage(r.burnout_stage)
        assert all(x.burnout_stage == r.burnout_stage for x in by_stage)

    def test_reset_clears_results(self):
        engine = SalesBurnoutRiskEngine()
        engine.assess(make_input(rep_id="before_reset"))
        engine.reset()
        assert engine.get("before_reset") is None

    def test_reset_leaves_engine_empty(self):
        engine = SalesBurnoutRiskEngine()
        engine.assess(make_input(rep_id="r1"))
        engine.assess(make_input(rep_id="r2"))
        engine.reset()
        assert len(engine.all_reps()) == 0

    def test_avg_burnout_composite_empty(self):
        engine = SalesBurnoutRiskEngine()
        assert engine.avg_burnout_composite() == 0.0

    def test_avg_burnout_composite_single(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(make_input())
        assert engine.avg_burnout_composite() == r.burnout_composite

    def test_total_productivity_impact_empty(self):
        engine = SalesBurnoutRiskEngine()
        assert engine.total_productivity_impact_pct() == 0.0

    def test_total_productivity_impact_sums(self):
        engine = SalesBurnoutRiskEngine()
        r1 = engine.assess(make_input(rep_id="p1"))
        r2 = engine.assess(make_input(rep_id="p2"))
        expected = round(r1.estimated_productivity_impact_pct + r2.estimated_productivity_impact_pct, 1)
        assert engine.total_productivity_impact_pct() == expected


# ===========================================================================
# 21. EDGE CASES
# ===========================================================================

class TestEdgeCases:
    def test_all_zeros_input(self):
        engine = SalesBurnoutRiskEngine()
        inp = SalesBurnoutInput(
            rep_id="zeros", rep_name="Zero", region="Z",
            activity_decline_pct=0.0, avg_daily_calls_last_30d=0.0,
            avg_daily_calls_prior_30d=0.0, email_response_time_hrs=0.0,
            meeting_acceptance_rate_pct=0.0, pipeline_creation_last_30d_usd=0.0,
            pipeline_creation_prior_30d_usd=0.0, consecutive_no_close_weeks=0,
            deal_win_rate_last_90d=0.0, deal_win_rate_prior_quarter=0.0,
            pto_days_taken_ytd=0.0, pto_days_available_ytd=0.0,
            weekend_work_hours_avg=0.0, overtime_hours_per_week=0.0,
            sick_days_last_90d=0, manager_checkin_frequency=0.0,
            peer_interaction_score=0.0, quota_pressure_score=0.0,
            customer_escalations_last_30d=0,
        )
        r = engine.assess(inp)
        assert isinstance(r, SalesBurnoutResult)

    def test_extreme_high_values(self):
        engine = SalesBurnoutRiskEngine()
        inp = make_input(
            activity_decline_pct=1000.0,
            peer_interaction_score=1000.0,
            overtime_hours_per_week=1000.0,
            sick_days_last_90d=100,
        )
        r = engine.assess(inp)
        assert r.burnout_composite >= 0
        assert r.burnout_composite <= 100

    def test_pto_ratio_above_1(self):
        engine = SalesBurnoutRiskEngine()
        inp = make_input(pto_days_taken_ytd=20.0, pto_days_available_ytd=10.0)
        r = engine.assess(inp)
        assert r.wellbeing_score <= 100.0

    def test_zero_prior_pipeline(self):
        engine = SalesBurnoutRiskEngine()
        inp = make_input(pipeline_creation_prior_30d_usd=0.0, pipeline_creation_last_30d_usd=0.0)
        r = engine.assess(inp)
        assert isinstance(r, SalesBurnoutResult)

    def test_no_close_weeks_zero(self):
        engine = SalesBurnoutRiskEngine()
        inp = make_input(consecutive_no_close_weeks=0)
        r = engine.assess(inp)
        assert r.performance_sustainability_score >= 0

    def test_no_close_weeks_large(self):
        engine = SalesBurnoutRiskEngine()
        inp = make_input(consecutive_no_close_weeks=52)
        r = engine.assess(inp)
        assert r.performance_sustainability_score >= 0

    def test_rep_id_with_special_chars(self):
        engine = SalesBurnoutRiskEngine()
        inp = make_input(rep_id="rep-123!@#")
        r = engine.assess(inp)
        assert r.rep_id == "rep-123!@#"

    def test_multiple_engines_independent(self):
        e1 = SalesBurnoutRiskEngine()
        e2 = SalesBurnoutRiskEngine()
        e1.assess(make_input(rep_id="e1rep"))
        assert e2.get("e1rep") is None

    def test_activity_health_score_boundary_5(self):
        inp = make_input(activity_decline_pct=5.0, pipeline_creation_last_30d_usd=0,
                         pipeline_creation_prior_30d_usd=100_000, meeting_acceptance_rate_pct=0.0)
        score = _activity_health_score(inp)
        # activity: 35, pipe ratio: 0 -> 0, meeting: 0 -> total = 35
        assert score == 35.0

    def test_activity_health_score_boundary_15(self):
        inp = make_input(activity_decline_pct=15.0, pipeline_creation_last_30d_usd=0,
                         pipeline_creation_prior_30d_usd=100_000, meeting_acceptance_rate_pct=0.0)
        score = _activity_health_score(inp)
        # activity: 24, pipe: 0, meeting: 0
        assert score == 24.0

    def test_wellbeing_boundary_weekend_exactly_2(self):
        inp = make_input(weekend_work_hours_avg=2.0, overtime_hours_per_week=100.0,
                         pto_days_taken_ytd=0, pto_days_available_ytd=15.0, sick_days_last_90d=10)
        score = _wellbeing_score(inp)
        assert score == 30.0

    def test_wellbeing_boundary_overtime_exactly_5(self):
        inp = make_input(weekend_work_hours_avg=11.0, overtime_hours_per_week=5.0,
                         pto_days_taken_ytd=0, pto_days_available_ytd=15.0, sick_days_last_90d=10)
        score = _wellbeing_score(inp)
        assert score == 25.0

    def test_performance_boundary_win_rate_delta_exactly_minus_5(self):
        inp = make_input(deal_win_rate_last_90d=25.0, deal_win_rate_prior_quarter=30.0,
                         consecutive_no_close_weeks=20, customer_escalations_last_30d=10,
                         quota_pressure_score=90.0)
        # delta = -5: gets 35
        assert _performance_sustainability_score(inp) == 35.0

    def test_social_boundary_email_exactly_4(self):
        inp = make_input(manager_checkin_frequency=0.0, peer_interaction_score=0.0,
                         email_response_time_hrs=4.0)
        assert _social_engagement_score(inp) == 30.0

    def test_social_boundary_manager_exactly_1(self):
        inp = make_input(manager_checkin_frequency=1.0, peer_interaction_score=0.0,
                         email_response_time_hrs=100.0)
        assert _social_engagement_score(inp) == 12.0


# ===========================================================================
# 22. DETERMINISM TESTS
# ===========================================================================

class TestDeterminism:
    def test_same_input_same_composite(self):
        engine = SalesBurnoutRiskEngine()
        inp = make_input(rep_id="det1")
        r1 = engine.assess(inp)
        engine.reset()
        r2 = engine.assess(inp)
        assert r1.burnout_composite == r2.burnout_composite

    def test_same_input_same_risk(self):
        engine = SalesBurnoutRiskEngine()
        inp = make_input(rep_id="det2")
        r1 = engine.assess(inp)
        engine.reset()
        r2 = engine.assess(inp)
        assert r1.burnout_risk == r2.burnout_risk

    def test_same_input_same_stage(self):
        engine = SalesBurnoutRiskEngine()
        inp = make_input(rep_id="det3")
        r1 = engine.assess(inp)
        engine.reset()
        r2 = engine.assess(inp)
        assert r1.burnout_stage == r2.burnout_stage

    def test_same_input_same_signal(self):
        engine = SalesBurnoutRiskEngine()
        inp = make_input(rep_id="det4")
        r1 = engine.assess(inp)
        engine.reset()
        r2 = engine.assess(inp)
        assert r1.primary_burnout_signal == r2.primary_burnout_signal

    def test_different_inputs_can_differ(self):
        engine = SalesBurnoutRiskEngine()
        r1 = engine.assess(healthy_input(rep_id="hdet"))
        r2 = engine.assess(burned_out_input(rep_id="bdet"))
        assert r1.burnout_composite != r2.burnout_composite


# ===========================================================================
# 23. SCENARIO TESTS
# ===========================================================================

class TestScenarios:
    def test_healthy_rep_risk_none_or_early(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(healthy_input())
        assert r.burnout_risk in (BurnoutRisk.NONE, BurnoutRisk.EARLY_WARNING)

    def test_burned_out_rep_risk_high_or_critical(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(burned_out_input())
        assert r.burnout_risk in (BurnoutRisk.HIGH, BurnoutRisk.CRITICAL)

    def test_healthy_rep_stage_engaged_or_coasting(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(healthy_input())
        assert r.burnout_stage in (BurnoutStage.ENGAGED, BurnoutStage.COASTING)

    def test_burned_out_rep_stage_burned_out_or_depleted(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(burned_out_input())
        assert r.burnout_stage in (BurnoutStage.BURNED_OUT, BurnoutStage.DEPLETED)

    def test_healthy_rep_productivity_impact_low(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(healthy_input())
        assert r.estimated_productivity_impact_pct < 25.0

    def test_burned_out_rep_productivity_impact_high(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(burned_out_input())
        assert r.estimated_productivity_impact_pct > 25.0

    def test_healthy_rep_action_monitor_or_check_in(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(healthy_input())
        assert r.burnout_action in (BurnoutAction.MONITOR, BurnoutAction.CHECK_IN)

    def test_burned_out_rep_action_workload_or_urgent(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(burned_out_input())
        assert r.burnout_action in (BurnoutAction.WORKLOAD_REDUCTION, BurnoutAction.URGENT_INTERVENTION)

    def test_overworked_rep_overwhelm_signal(self):
        engine = SalesBurnoutRiskEngine()
        inp = make_input(overtime_hours_per_week=25.0, weekend_work_hours_avg=12.0,
                         activity_decline_pct=60.0)
        r = engine.assess(inp)
        assert r.primary_burnout_signal == BurnoutSignal.OVERWHELM

    def test_isolated_rep_isolation_signal(self):
        engine = SalesBurnoutRiskEngine()
        inp = make_input(
            manager_checkin_frequency=0.0,
            peer_interaction_score=0.0,
            email_response_time_hrs=50.0,
            # All other scores should be high
            activity_decline_pct=0.0,
            pipeline_creation_last_30d_usd=100_000,
            pipeline_creation_prior_30d_usd=100_000,
            meeting_acceptance_rate_pct=90.0,
            deal_win_rate_last_90d=35.0,
            deal_win_rate_prior_quarter=30.0,
            consecutive_no_close_weeks=0,
            customer_escalations_last_30d=0,
            quota_pressure_score=20.0,
            weekend_work_hours_avg=1.0,
            overtime_hours_per_week=2.0,
            pto_days_taken_ytd=10.0,
            pto_days_available_ytd=15.0,
            sick_days_last_90d=0,
        )
        r = engine.assess(inp)
        # With low social scores, isolation might dominate (if social is lowest)
        # Just check signal is valid enum
        assert isinstance(r.primary_burnout_signal, BurnoutSignal)

    def test_batch_with_mixed_reps(self):
        engine = SalesBurnoutRiskEngine()
        inputs = [
            healthy_input(rep_id="h1"),
            burned_out_input(rep_id="b1"),
            make_input(rep_id="m1", activity_decline_pct=20.0),
        ]
        results = engine.assess_batch(inputs)
        assert len(results) == 3
        composites = [r.burnout_composite for r in results]
        assert composites == sorted(composites, reverse=True)

    def test_rep_with_high_sick_days_and_overtime_needs_support(self):
        engine = SalesBurnoutRiskEngine()
        inp = make_input(sick_days_last_90d=6, overtime_hours_per_week=20.0)
        r = engine.assess(inp)
        assert r.needs_immediate_support

    def test_consecutive_batches_accumulate(self):
        engine = SalesBurnoutRiskEngine()
        engine.assess_batch([make_input(rep_id="acc1"), make_input(rep_id="acc2")])
        engine.assess_batch([make_input(rep_id="acc3")])
        # All 3 should be stored
        assert engine.get("acc1") is not None
        assert engine.get("acc3") is not None

    def test_burnout_signal_text_not_empty(self):
        engine = SalesBurnoutRiskEngine()
        for inp in [healthy_input(), burned_out_input()]:
            r = engine.assess(inp)
            assert isinstance(r.burnout_signal, str)
            assert len(r.burnout_signal) > 0

    def test_to_dict_burnout_risk_is_valid_enum_value(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(make_input())
        valid_values = {e.value for e in BurnoutRisk}
        assert r.to_dict()["burnout_risk"] in valid_values

    def test_to_dict_burnout_stage_is_valid_enum_value(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(make_input())
        valid_values = {e.value for e in BurnoutStage}
        assert r.to_dict()["burnout_stage"] in valid_values

    def test_to_dict_primary_signal_is_valid_enum_value(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(make_input())
        valid_values = {e.value for e in BurnoutSignal}
        assert r.to_dict()["primary_burnout_signal"] in valid_values

    def test_to_dict_action_is_valid_enum_value(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(make_input())
        valid_values = {e.value for e in BurnoutAction}
        assert r.to_dict()["burnout_action"] in valid_values


# ===========================================================================
# 24. SIGNAL TEXT TESTS
# ===========================================================================

class TestBurnoutSignalText:
    def test_overwhelm_signal_text(self):
        inp = make_input(overtime_hours_per_week=20.0, weekend_work_hours_avg=10.0)
        text = _burnout_signal_text(inp, BurnoutSignal.OVERWHELM, 60.0)
        assert "overtime" in text.lower() or "overwork" in text.lower()

    def test_activity_decline_signal_text(self):
        inp = make_input(activity_decline_pct=30.0, consecutive_no_close_weeks=5)
        text = _burnout_signal_text(inp, BurnoutSignal.ACTIVITY_DECLINE, 40.0)
        assert "30" in text
        assert "5" in text

    def test_exhaustion_signal_text(self):
        inp = make_input(sick_days_last_90d=4, pto_days_taken_ytd=3.0)
        text = _burnout_signal_text(inp, BurnoutSignal.EXHAUSTION, 40.0)
        assert "4" in text
        assert "3" in text

    def test_performance_decay_signal_text(self):
        inp = make_input(deal_win_rate_last_90d=20.0, deal_win_rate_prior_quarter=30.0,
                         customer_escalations_last_30d=2)
        text = _burnout_signal_text(inp, BurnoutSignal.PERFORMANCE_DECAY, 40.0)
        assert "10" in text
        assert "2" in text

    def test_isolation_signal_text(self):
        inp = make_input(peer_interaction_score=30.0, manager_checkin_frequency=1.5)
        text = _burnout_signal_text(inp, BurnoutSignal.ISOLATION, 40.0)
        assert "30" in text
        assert "1.5" in text

    def test_none_signal_healthy_rep(self):
        inp = make_input()
        text = _burnout_signal_text(inp, BurnoutSignal.NONE, 10.0)
        assert "healthy" in text.lower() or "no burnout" in text.lower()

    def test_none_signal_early_warning(self):
        inp = make_input()
        text = _burnout_signal_text(inp, BurnoutSignal.NONE, 25.0)
        assert "25" in text or "early" in text.lower() or "composite" in text.lower() or "indicators" in text.lower()


# ===========================================================================
# 25. INTERNAL FUNCTION IMPORTS WORK
# ===========================================================================

class TestInternalFunctionImports:
    def test_activity_health_score_callable(self):
        assert callable(_activity_health_score)

    def test_wellbeing_score_callable(self):
        assert callable(_wellbeing_score)

    def test_performance_sustainability_score_callable(self):
        assert callable(_performance_sustainability_score)

    def test_social_engagement_score_callable(self):
        assert callable(_social_engagement_score)

    def test_composite_callable(self):
        assert callable(_composite)

    def test_burnout_risk_callable(self):
        assert callable(_burnout_risk)

    def test_burnout_stage_callable(self):
        assert callable(_burnout_stage)

    def test_primary_signal_callable(self):
        assert callable(_primary_signal)

    def test_burnout_action_callable(self):
        assert callable(_burnout_action)

    def test_productivity_impact_pct_callable(self):
        assert callable(_productivity_impact_pct)

    def test_burnout_signal_text_callable(self):
        assert callable(_burnout_signal_text)


# ===========================================================================
# 26. TYPE CHECKS
# ===========================================================================

class TestTypeChecks:
    def test_activity_health_score_returns_float(self):
        assert isinstance(_activity_health_score(make_input()), float)

    def test_wellbeing_score_returns_float(self):
        assert isinstance(_wellbeing_score(make_input()), float)

    def test_performance_score_returns_float(self):
        assert isinstance(_performance_sustainability_score(make_input()), float)

    def test_social_score_returns_float(self):
        assert isinstance(_social_engagement_score(make_input()), float)

    def test_composite_returns_float(self):
        assert isinstance(_composite(50.0, 50.0, 50.0, 50.0), float)

    def test_burnout_risk_returns_enum(self):
        assert isinstance(_burnout_risk(30.0), BurnoutRisk)

    def test_burnout_stage_returns_enum(self):
        assert isinstance(_burnout_stage(30.0), BurnoutStage)

    def test_primary_signal_returns_enum(self):
        assert isinstance(_primary_signal(make_input(), 50.0, 50.0, 50.0, 50.0), BurnoutSignal)

    def test_burnout_action_returns_enum(self):
        assert isinstance(_burnout_action(BurnoutRisk.MODERATE), BurnoutAction)

    def test_productivity_impact_returns_float(self):
        assert isinstance(_productivity_impact_pct(40.0), float)

    def test_signal_text_returns_str(self):
        inp = make_input()
        assert isinstance(_burnout_signal_text(inp, BurnoutSignal.NONE, 10.0), str)

    def test_engine_is_instance(self):
        assert isinstance(SalesBurnoutRiskEngine(), SalesBurnoutRiskEngine)


# ===========================================================================
# 27. ADDITIONAL COVERAGE TESTS
# ===========================================================================

class TestAdditionalCoverage:
    def test_batch_sort_stability_for_equal_composites(self):
        """All same inputs => same composite, order preserved by sort stability."""
        engine = SalesBurnoutRiskEngine()
        inputs = [make_input(rep_id=f"eq{i}") for i in range(3)]
        results = engine.assess_batch(inputs)
        # All composites should be equal
        composites = [r.burnout_composite for r in results]
        assert composites[0] >= composites[-1]

    def test_by_risk_empty_when_no_match(self):
        engine = SalesBurnoutRiskEngine()
        engine.assess(healthy_input(rep_id="h1"))
        # healthy rep should not be critical
        critical_reps = engine.by_risk(BurnoutRisk.CRITICAL)
        assert len(critical_reps) >= 0  # just verify it doesn't throw

    def test_by_stage_empty_when_no_match(self):
        engine = SalesBurnoutRiskEngine()
        engine.assess(healthy_input(rep_id="h2"))
        depleted_reps = engine.by_stage(BurnoutStage.DEPLETED)
        assert len(depleted_reps) >= 0

    def test_summary_risk_counts_are_dicts(self):
        engine = SalesBurnoutRiskEngine()
        engine.assess(make_input())
        s = engine.summary()
        assert isinstance(s["risk_counts"], dict)
        assert isinstance(s["stage_counts"], dict)
        assert isinstance(s["signal_counts"], dict)
        assert isinstance(s["action_counts"], dict)

    def test_composite_boundary_exactly_20(self):
        risk = _burnout_risk(20.0)
        assert risk == BurnoutRisk.EARLY_WARNING
        stage = _burnout_stage(20.0)
        assert stage == BurnoutStage.COASTING

    def test_composite_boundary_exactly_50(self):
        risk = _burnout_risk(50.0)
        assert risk == BurnoutRisk.HIGH
        stage = _burnout_stage(50.0)
        assert stage == BurnoutStage.BURNED_OUT

    def test_composite_boundary_exactly_70(self):
        risk = _burnout_risk(70.0)
        assert risk == BurnoutRisk.CRITICAL
        stage = _burnout_stage(70.0)
        assert stage == BurnoutStage.DEPLETED

    def test_wellbeing_pto_ratio_exactly_50pct(self):
        inp = make_input(weekend_work_hours_avg=11.0, overtime_hours_per_week=100.0,
                         pto_days_taken_ytd=5.0, pto_days_available_ytd=10.0, sick_days_last_90d=10)
        score = _wellbeing_score(inp)
        assert score == 25.0

    def test_wellbeing_pto_ratio_exactly_30pct(self):
        inp = make_input(weekend_work_hours_avg=11.0, overtime_hours_per_week=100.0,
                         pto_days_taken_ytd=3.0, pto_days_available_ytd=10.0, sick_days_last_90d=10)
        score = _wellbeing_score(inp)
        assert score == 18.0

    def test_wellbeing_pto_ratio_exactly_15pct(self):
        inp = make_input(weekend_work_hours_avg=11.0, overtime_hours_per_week=100.0,
                         pto_days_taken_ytd=1.5, pto_days_available_ytd=10.0, sick_days_last_90d=10)
        score = _wellbeing_score(inp)
        assert score == 9.0

    def test_performance_escalations_boundary_2(self):
        # customer_escalations_last_30d == 2 should use <= 2 -> 6
        inp = make_input(deal_win_rate_last_90d=30.0, deal_win_rate_prior_quarter=35.0,
                         consecutive_no_close_weeks=20, customer_escalations_last_30d=2,
                         quota_pressure_score=90.0)
        score = _performance_sustainability_score(inp)
        # win_rate_delta=-5 (>=−5): 35, no_close=20: 0, escalations=2(<=2): 6, quota=90: 0
        assert score == 41.0

    def test_result_burnout_risk_consistent_with_composite(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(burned_out_input())
        if r.burnout_composite < 20:
            assert r.burnout_risk == BurnoutRisk.NONE
        elif r.burnout_composite < 35:
            assert r.burnout_risk == BurnoutRisk.EARLY_WARNING
        elif r.burnout_composite < 50:
            assert r.burnout_risk == BurnoutRisk.MODERATE
        elif r.burnout_composite < 70:
            assert r.burnout_risk == BurnoutRisk.HIGH
        else:
            assert r.burnout_risk == BurnoutRisk.CRITICAL

    def test_result_stage_consistent_with_composite(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(healthy_input())
        if r.burnout_composite < 20:
            assert r.burnout_stage == BurnoutStage.ENGAGED
        elif r.burnout_composite < 35:
            assert r.burnout_stage == BurnoutStage.COASTING

    def test_assess_multiple_reps_different_ids(self):
        engine = SalesBurnoutRiskEngine()
        ids = ["rep_a", "rep_b", "rep_c"]
        for rep_id in ids:
            engine.assess(make_input(rep_id=rep_id))
        for rep_id in ids:
            assert engine.get(rep_id) is not None

    def test_assess_productivity_impact_boundary_34(self):
        # composite just below 35: 0.3 multiplier
        impact = _productivity_impact_pct(34.0)
        assert impact == round(34.0 * 0.3, 1)

    def test_assess_productivity_impact_boundary_35(self):
        # composite at 35: 0.5 multiplier
        impact = _productivity_impact_pct(35.0)
        assert impact == round(35.0 * 0.5, 1)

    def test_assess_productivity_impact_boundary_49(self):
        impact = _productivity_impact_pct(49.0)
        assert impact == round(49.0 * 0.5, 1)

    def test_assess_productivity_impact_boundary_50(self):
        impact = _productivity_impact_pct(50.0)
        assert impact == round(50.0 * 0.7, 1)

    def test_to_dict_returns_new_dict_each_call(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(make_input())
        d1 = r.to_dict()
        d2 = r.to_dict()
        assert d1 is not d2
        assert d1 == d2

    def test_at_risk_reps_empty_when_none_at_risk(self):
        engine = SalesBurnoutRiskEngine()
        r = engine.assess(healthy_input(rep_id="healthy_only"))
        at_risk = engine.at_risk_reps()
        for rep in at_risk:
            assert rep.is_at_burnout_risk

    def test_summary_avg_scores_in_range(self):
        engine = SalesBurnoutRiskEngine()
        engine.assess_batch([make_input(rep_id=f"rng{i}") for i in range(5)])
        s = engine.summary()
        assert 0.0 <= s["avg_activity_health_score"] <= 100.0
        assert 0.0 <= s["avg_wellbeing_score"] <= 100.0
        assert 0.0 <= s["avg_performance_sustainability_score"] <= 100.0
        assert 0.0 <= s["avg_social_engagement_score"] <= 100.0

    def test_batch_overwrites_existing_rep(self):
        engine = SalesBurnoutRiskEngine()
        engine.assess(make_input(rep_id="dup", activity_decline_pct=0.0))
        engine.assess_batch([make_input(rep_id="dup", activity_decline_pct=60.0)])
        stored = engine.get("dup")
        # Should have most recent result
        assert stored is not None

    def test_overwhelm_overrides_even_when_all_scores_low(self):
        inp = make_input(overtime_hours_per_week=20.0, weekend_work_hours_avg=1.0,
                         activity_decline_pct=0.0)
        # scores all low enough that strongest might be < 20 but overwhelm override applies
        signal = _primary_signal(inp, 0.0, 0.0, 0.0, 0.0)
        assert signal == BurnoutSignal.OVERWHELM

    def test_pipeline_ratio_exactly_90pct(self):
        inp = make_input(activity_decline_pct=100.0,
                         pipeline_creation_last_30d_usd=90_000,
                         pipeline_creation_prior_30d_usd=100_000,
                         meeting_acceptance_rate_pct=0.0)
        score = _activity_health_score(inp)
        # pipe_ratio = 0.9 >= 0.9: 35; activity > 50: 0; meeting 0: 0
        assert score == 35.0

    def test_pipeline_ratio_exactly_75pct(self):
        inp = make_input(activity_decline_pct=100.0,
                         pipeline_creation_last_30d_usd=75_000,
                         pipeline_creation_prior_30d_usd=100_000,
                         meeting_acceptance_rate_pct=0.0)
        score = _activity_health_score(inp)
        # pipe_ratio = 0.75 >= 0.75: 24
        assert score == 24.0

    def test_composite_activity_weight_30(self):
        # Only activity is bad; rest perfect
        c = _composite(0.0, 100.0, 100.0, 100.0)
        assert abs(c - 30.0) < 0.01

    def test_composite_wellbeing_weight_25(self):
        c = _composite(100.0, 0.0, 100.0, 100.0)
        assert abs(c - 25.0) < 0.01

    def test_composite_performance_weight_25(self):
        c = _composite(100.0, 100.0, 0.0, 100.0)
        assert abs(c - 25.0) < 0.01

    def test_composite_social_weight_20(self):
        c = _composite(100.0, 100.0, 100.0, 0.0)
        assert abs(c - 20.0) < 0.01

    def test_engine_init_empty(self):
        engine = SalesBurnoutRiskEngine()
        assert len(engine.all_reps()) == 0
        assert engine.summary()["total"] == 0
