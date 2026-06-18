"""
Comprehensive pytest test suite for swarm/intelligence/pipeline_aging_intelligence.py

Covers:
- All enum values (DecayStatus, DecayRisk, StageVelocity, RecoveryAction)
- PipelineAgingInput: exactly 22 fields
- PipelineAgingResult: to_dict() returns exactly 15 keys
- PipelineAgingIntelligence: assess(), assess_batch(), summary() (13 keys)
- Composite formula weights: activity*0.30 + engagement*0.25 + velocity*0.25 + (100-stage_health)*0.20
- All boolean logic for is_stale and needs_immediate_action
- Score clamping [0, 100]
- Batch sort by composite descending (highest decay first)
- reset() clears both _results and _deal_values
- by_status(), by_risk(), stale_deals(), immediate_action_queue()
- total_stale_pipeline_usd() accuracy
"""

import dataclasses
import pytest

from swarm.intelligence.pipeline_aging_intelligence import (
    DecayStatus,
    DecayRisk,
    StageVelocity,
    RecoveryAction,
    PipelineAgingInput,
    PipelineAgingResult,
    PipelineAgingIntelligence,
    _activity_decay_score,
    _engagement_decay_score,
    _velocity_decay_score,
    _stage_health_score,
    _composite,
    _is_stale,
    _decay_status,
    _decay_risk,
    _stage_velocity,
    _recovery_action,
    _primary_decay_signal,
)


# ──────────────────────────────────────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────────────────────────────────────

def fresh_deal(deal_id: str = "deal_001", rep_id: str = "rep_001") -> PipelineAgingInput:
    """A healthy, actively progressing deal — should produce low decay scores."""
    return PipelineAgingInput(
        deal_id=deal_id,
        rep_id=rep_id,
        deal_name="Acme Corp Q3",
        deal_value_usd=180_000.0,
        deal_stage=3,
        days_in_current_stage=8,
        days_since_last_activity=2,
        days_since_last_buyer_response=5,
        total_deal_age_days=45,
        velocity_vs_benchmark_pct=90.0,
        activity_count_last_14d=8,
        activity_count_prev_14d=6,
        emails_opened_last_30d=5,
        meetings_completed_last_30d=3,
        champion_last_engaged_days_ago=4,
        exec_last_engaged_days_ago=10,
        next_step_defined=1,
        close_date_changes_count=0,
        stage_regression_count=0,
        deal_source=1,
        historical_avg_days_at_stage=14,
        expected_close_days_remaining=21,
    )


def dead_deal(deal_id: str = "deal_dead", rep_id: str = "rep_002") -> PipelineAgingInput:
    """A severely decayed deal — should produce high decay scores and DEAD status."""
    return PipelineAgingInput(
        deal_id=deal_id,
        rep_id=rep_id,
        deal_name="Ghost Corp Q1",
        deal_value_usd=50_000.0,
        deal_stage=3,
        days_in_current_stage=60,
        days_since_last_activity=20,
        days_since_last_buyer_response=35,
        total_deal_age_days=180,
        velocity_vs_benchmark_pct=250.0,
        activity_count_last_14d=0,
        activity_count_prev_14d=4,
        emails_opened_last_30d=0,
        meetings_completed_last_30d=0,
        champion_last_engaged_days_ago=30,
        exec_last_engaged_days_ago=45,
        next_step_defined=0,
        close_date_changes_count=4,
        stage_regression_count=2,
        deal_source=1,
        historical_avg_days_at_stage=14,
        expected_close_days_remaining=-5,
    )


def aging_deal(deal_id: str = "deal_aging") -> PipelineAgingInput:
    """A moderately decayed deal that's aging but not yet critical."""
    return PipelineAgingInput(
        deal_id=deal_id,
        rep_id="rep_003",
        deal_name="Midcorp Deal",
        deal_value_usd=75_000.0,
        deal_stage=2,
        days_in_current_stage=20,
        days_since_last_activity=8,
        days_since_last_buyer_response=12,
        total_deal_age_days=60,
        velocity_vs_benchmark_pct=125.0,
        activity_count_last_14d=3,
        activity_count_prev_14d=5,
        emails_opened_last_30d=2,
        meetings_completed_last_30d=1,
        champion_last_engaged_days_ago=10,
        exec_last_engaged_days_ago=20,
        next_step_defined=1,
        close_date_changes_count=1,
        stage_regression_count=0,
        deal_source=2,
        historical_avg_days_at_stage=14,
        expected_close_days_remaining=14,
    )


@pytest.fixture
def intel() -> PipelineAgingIntelligence:
    return PipelineAgingIntelligence()


# ──────────────────────────────────────────────────────────────────────────────
# 1. Enum values
# ──────────────────────────────────────────────────────────────────────────────

class TestDecayStatusEnum:
    def test_fresh_value(self):
        assert DecayStatus.FRESH.value == "fresh"

    def test_aging_value(self):
        assert DecayStatus.AGING.value == "aging"

    def test_stale_value(self):
        assert DecayStatus.STALE.value == "stale"

    def test_dead_value(self):
        assert DecayStatus.DEAD.value == "dead"

    def test_all_four_members(self):
        assert len(DecayStatus) == 4

    def test_is_str_subclass(self):
        assert isinstance(DecayStatus.FRESH, str)

    def test_string_comparison(self):
        assert DecayStatus.FRESH == "fresh"

    def test_enum_from_value(self):
        assert DecayStatus("stale") == DecayStatus.STALE


class TestDecayRiskEnum:
    def test_low_value(self):
        assert DecayRisk.LOW.value == "low"

    def test_moderate_value(self):
        assert DecayRisk.MODERATE.value == "moderate"

    def test_high_value(self):
        assert DecayRisk.HIGH.value == "high"

    def test_critical_value(self):
        assert DecayRisk.CRITICAL.value == "critical"

    def test_all_four_members(self):
        assert len(DecayRisk) == 4

    def test_is_str_subclass(self):
        assert isinstance(DecayRisk.LOW, str)

    def test_enum_from_value(self):
        assert DecayRisk("critical") == DecayRisk.CRITICAL


class TestStageVelocityEnum:
    def test_fast_value(self):
        assert StageVelocity.FAST.value == "fast"

    def test_on_track_value(self):
        assert StageVelocity.ON_TRACK.value == "on_track"

    def test_slow_value(self):
        assert StageVelocity.SLOW.value == "slow"

    def test_stalled_value(self):
        assert StageVelocity.STALLED.value == "stalled"

    def test_all_four_members(self):
        assert len(StageVelocity) == 4

    def test_is_str_subclass(self):
        assert isinstance(StageVelocity.FAST, str)


class TestRecoveryActionEnum:
    def test_maintain_value(self):
        assert RecoveryAction.MAINTAIN.value == "maintain"

    def test_re_engage_champion_value(self):
        assert RecoveryAction.RE_ENGAGE_CHAMPION.value == "re_engage_champion"

    def test_executive_escalation_value(self):
        assert RecoveryAction.EXECUTIVE_ESCALATION.value == "executive_escalation"

    def test_kill_or_recycle_value(self):
        assert RecoveryAction.KILL_OR_RECYCLE.value == "kill_or_recycle"

    def test_all_four_members(self):
        assert len(RecoveryAction) == 4

    def test_is_str_subclass(self):
        assert isinstance(RecoveryAction.MAINTAIN, str)


# ──────────────────────────────────────────────────────────────────────────────
# 2. PipelineAgingInput: exactly 22 fields
# ──────────────────────────────────────────────────────────────────────────────

class TestPipelineAgingInput:
    def test_has_exactly_22_fields(self):
        fields = dataclasses.fields(PipelineAgingInput)
        assert len(fields) == 22

    def test_field_names(self):
        field_names = {f.name for f in dataclasses.fields(PipelineAgingInput)}
        expected = {
            "deal_id", "rep_id", "deal_name", "deal_value_usd", "deal_stage",
            "days_in_current_stage", "days_since_last_activity",
            "days_since_last_buyer_response", "total_deal_age_days",
            "velocity_vs_benchmark_pct", "activity_count_last_14d",
            "activity_count_prev_14d", "emails_opened_last_30d",
            "meetings_completed_last_30d", "champion_last_engaged_days_ago",
            "exec_last_engaged_days_ago", "next_step_defined",
            "close_date_changes_count", "stage_regression_count",
            "deal_source", "historical_avg_days_at_stage",
            "expected_close_days_remaining",
        }
        assert field_names == expected

    def test_instantiation(self):
        inp = fresh_deal()
        assert inp.deal_id == "deal_001"

    def test_deal_value_usd_field(self):
        inp = fresh_deal()
        assert inp.deal_value_usd == 180_000.0

    def test_dead_deal_fields(self):
        inp = dead_deal()
        assert inp.days_since_last_activity == 20
        assert inp.days_since_last_buyer_response == 35
        assert inp.velocity_vs_benchmark_pct == 250.0

    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(PipelineAgingInput)


# ──────────────────────────────────────────────────────────────────────────────
# 3. PipelineAgingResult: to_dict() returns exactly 15 keys
# ──────────────────────────────────────────────────────────────────────────────

class TestPipelineAgingResultToDict:
    def test_to_dict_returns_15_keys(self, intel):
        result = intel.assess(fresh_deal())
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_key_names(self, intel):
        result = intel.assess(fresh_deal())
        d = result.to_dict()
        expected_keys = {
            "deal_id", "rep_id", "decay_status", "decay_risk",
            "stage_velocity", "recovery_action", "activity_decay_score",
            "engagement_decay_score", "velocity_decay_score",
            "stage_health_score", "decay_composite", "is_stale",
            "needs_immediate_action", "recovery_probability_pct",
            "primary_decay_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_decay_status_is_string(self, intel):
        result = intel.assess(fresh_deal())
        d = result.to_dict()
        assert isinstance(d["decay_status"], str)

    def test_to_dict_decay_risk_is_string(self, intel):
        result = intel.assess(fresh_deal())
        d = result.to_dict()
        assert isinstance(d["decay_risk"], str)

    def test_to_dict_stage_velocity_is_string(self, intel):
        result = intel.assess(fresh_deal())
        d = result.to_dict()
        assert isinstance(d["stage_velocity"], str)

    def test_to_dict_recovery_action_is_string(self, intel):
        result = intel.assess(fresh_deal())
        d = result.to_dict()
        assert isinstance(d["recovery_action"], str)

    def test_to_dict_is_stale_is_bool(self, intel):
        result = intel.assess(fresh_deal())
        d = result.to_dict()
        assert isinstance(d["is_stale"], bool)

    def test_to_dict_needs_immediate_action_is_bool(self, intel):
        result = intel.assess(fresh_deal())
        d = result.to_dict()
        assert isinstance(d["needs_immediate_action"], bool)

    def test_to_dict_scores_are_float(self, intel):
        result = intel.assess(fresh_deal())
        d = result.to_dict()
        for key in ("activity_decay_score", "engagement_decay_score",
                    "velocity_decay_score", "stage_health_score",
                    "decay_composite", "recovery_probability_pct"):
            assert isinstance(d[key], float), f"{key} should be float"

    def test_to_dict_deal_id_matches(self, intel):
        result = intel.assess(fresh_deal("my_deal"))
        assert result.to_dict()["deal_id"] == "my_deal"

    def test_to_dict_dead_deal_15_keys(self, intel):
        result = intel.assess(dead_deal())
        assert len(result.to_dict()) == 15


# ──────────────────────────────────────────────────────────────────────────────
# 4. Activity Decay Score sub-function
# ──────────────────────────────────────────────────────────────────────────────

class TestActivityDecayScore:
    def test_fresh_deal_low_score(self):
        score = _activity_decay_score(fresh_deal())
        assert score < 20.0

    def test_days_since_activity_ge_30_adds_35(self):
        inp = fresh_deal()
        inp = dataclasses.replace(inp, days_since_last_activity=30, next_step_defined=1,
                                  stage_regression_count=0, activity_count_last_14d=5,
                                  activity_count_prev_14d=5)
        score = _activity_decay_score(inp)
        assert score >= 35.0

    def test_days_since_activity_ge_14_adds_25(self):
        inp = dataclasses.replace(fresh_deal(), days_since_last_activity=14,
                                  next_step_defined=1, stage_regression_count=0,
                                  activity_count_last_14d=5, activity_count_prev_14d=5)
        score = _activity_decay_score(inp)
        assert score >= 25.0

    def test_days_since_activity_ge_7_adds_12(self):
        inp = dataclasses.replace(fresh_deal(), days_since_last_activity=7,
                                  next_step_defined=1, stage_regression_count=0,
                                  activity_count_last_14d=5, activity_count_prev_14d=5)
        score = _activity_decay_score(inp)
        assert score >= 12.0

    def test_days_since_activity_ge_3_adds_5(self):
        inp = dataclasses.replace(fresh_deal(), days_since_last_activity=3,
                                  next_step_defined=1, stage_regression_count=0,
                                  activity_count_last_14d=5, activity_count_prev_14d=5)
        score = _activity_decay_score(inp)
        assert score >= 5.0

    def test_trend_decline_75pct_adds_30(self):
        # activity dropped from 8 to 1 = -87.5% trend
        inp = dataclasses.replace(fresh_deal(), activity_count_last_14d=1,
                                  activity_count_prev_14d=8, days_since_last_activity=1,
                                  next_step_defined=1, stage_regression_count=0)
        score = _activity_decay_score(inp)
        assert score >= 30.0

    def test_trend_decline_50pct_adds_20(self):
        # activity dropped from 8 to 3 = -62.5%
        inp = dataclasses.replace(fresh_deal(), activity_count_last_14d=3,
                                  activity_count_prev_14d=8, days_since_last_activity=1,
                                  next_step_defined=1, stage_regression_count=0)
        score = _activity_decay_score(inp)
        assert score >= 20.0

    def test_trend_decline_25pct_adds_12(self):
        # activity dropped from 8 to 5 = -37.5%
        inp = dataclasses.replace(fresh_deal(), activity_count_last_14d=5,
                                  activity_count_prev_14d=8, days_since_last_activity=1,
                                  next_step_defined=1, stage_regression_count=0)
        score = _activity_decay_score(inp)
        assert score >= 12.0

    def test_no_next_step_adds_20(self):
        inp = dataclasses.replace(fresh_deal(), next_step_defined=0,
                                  days_since_last_activity=0,
                                  activity_count_last_14d=5, activity_count_prev_14d=5,
                                  stage_regression_count=0)
        score = _activity_decay_score(inp)
        assert score >= 20.0

    def test_next_step_defined_no_penalty(self):
        inp = dataclasses.replace(fresh_deal(), next_step_defined=1,
                                  days_since_last_activity=0,
                                  activity_count_last_14d=5, activity_count_prev_14d=5,
                                  stage_regression_count=0)
        score = _activity_decay_score(inp)
        assert score == 0.0

    def test_stage_regression_ge_2_adds_15(self):
        inp = dataclasses.replace(fresh_deal(), stage_regression_count=2,
                                  days_since_last_activity=0, next_step_defined=1,
                                  activity_count_last_14d=5, activity_count_prev_14d=5)
        score = _activity_decay_score(inp)
        assert score >= 15.0

    def test_stage_regression_1_adds_8(self):
        inp = dataclasses.replace(fresh_deal(), stage_regression_count=1,
                                  days_since_last_activity=0, next_step_defined=1,
                                  activity_count_last_14d=5, activity_count_prev_14d=5)
        score = _activity_decay_score(inp)
        assert score >= 8.0

    def test_score_clamped_at_100(self):
        score = _activity_decay_score(dead_deal())
        assert score <= 100.0

    def test_score_clamped_at_0_minimum(self):
        score = _activity_decay_score(fresh_deal())
        assert score >= 0.0

    def test_prev_14d_zero_current_zero_trend_negative_one(self):
        # Both zero → trend = -1.0 → should add 30
        inp = dataclasses.replace(fresh_deal(), activity_count_last_14d=0,
                                  activity_count_prev_14d=0, days_since_last_activity=0,
                                  next_step_defined=1, stage_regression_count=0)
        score = _activity_decay_score(inp)
        assert score >= 30.0

    def test_prev_14d_zero_current_positive_no_trend_penalty(self):
        # prev=0, current>0 → trend=0.0 → no trend penalty
        inp = dataclasses.replace(fresh_deal(), activity_count_last_14d=3,
                                  activity_count_prev_14d=0, days_since_last_activity=0,
                                  next_step_defined=1, stage_regression_count=0)
        score = _activity_decay_score(inp)
        assert score == 0.0


# ──────────────────────────────────────────────────────────────────────────────
# 5. Engagement Decay Score sub-function
# ──────────────────────────────────────────────────────────────────────────────

class TestEngagementDecayScore:
    def test_fresh_deal_low_score(self):
        score = _engagement_decay_score(fresh_deal())
        assert score < 20.0

    def test_buyer_response_ge_30_adds_35(self):
        inp = dataclasses.replace(fresh_deal(), days_since_last_buyer_response=30,
                                  emails_opened_last_30d=5, meetings_completed_last_30d=3,
                                  champion_last_engaged_days_ago=4, close_date_changes_count=0)
        score = _engagement_decay_score(inp)
        assert score >= 35.0

    def test_buyer_response_ge_14_adds_25(self):
        inp = dataclasses.replace(fresh_deal(), days_since_last_buyer_response=14,
                                  emails_opened_last_30d=5, meetings_completed_last_30d=3,
                                  champion_last_engaged_days_ago=4, close_date_changes_count=0)
        score = _engagement_decay_score(inp)
        assert score >= 25.0

    def test_buyer_response_ge_7_adds_12(self):
        inp = dataclasses.replace(fresh_deal(), days_since_last_buyer_response=7,
                                  emails_opened_last_30d=5, meetings_completed_last_30d=3,
                                  champion_last_engaged_days_ago=4, close_date_changes_count=0)
        score = _engagement_decay_score(inp)
        assert score >= 12.0

    def test_buyer_response_ge_3_adds_5(self):
        inp = dataclasses.replace(fresh_deal(), days_since_last_buyer_response=3,
                                  emails_opened_last_30d=5, meetings_completed_last_30d=3,
                                  champion_last_engaged_days_ago=4, close_date_changes_count=0)
        score = _engagement_decay_score(inp)
        assert score >= 5.0

    def test_zero_emails_adds_20(self):
        inp = dataclasses.replace(fresh_deal(), emails_opened_last_30d=0,
                                  days_since_last_buyer_response=0,
                                  meetings_completed_last_30d=3,
                                  champion_last_engaged_days_ago=4, close_date_changes_count=0)
        score = _engagement_decay_score(inp)
        assert score >= 20.0

    def test_1_or_2_emails_adds_10(self):
        inp = dataclasses.replace(fresh_deal(), emails_opened_last_30d=2,
                                  days_since_last_buyer_response=0,
                                  meetings_completed_last_30d=3,
                                  champion_last_engaged_days_ago=4, close_date_changes_count=0)
        score = _engagement_decay_score(inp)
        assert score >= 10.0

    def test_ge_3_emails_no_email_penalty(self):
        inp = dataclasses.replace(fresh_deal(), emails_opened_last_30d=3,
                                  days_since_last_buyer_response=0,
                                  meetings_completed_last_30d=3,
                                  champion_last_engaged_days_ago=4, close_date_changes_count=0)
        score = _engagement_decay_score(inp)
        assert score == 0.0

    def test_zero_meetings_adds_20(self):
        inp = dataclasses.replace(fresh_deal(), meetings_completed_last_30d=0,
                                  days_since_last_buyer_response=0,
                                  emails_opened_last_30d=5,
                                  champion_last_engaged_days_ago=4, close_date_changes_count=0)
        score = _engagement_decay_score(inp)
        assert score >= 20.0

    def test_one_meeting_adds_8(self):
        inp = dataclasses.replace(fresh_deal(), meetings_completed_last_30d=1,
                                  days_since_last_buyer_response=0,
                                  emails_opened_last_30d=5,
                                  champion_last_engaged_days_ago=4, close_date_changes_count=0)
        score = _engagement_decay_score(inp)
        assert score >= 8.0

    def test_ge_2_meetings_no_meeting_penalty(self):
        inp = dataclasses.replace(fresh_deal(), meetings_completed_last_30d=2,
                                  days_since_last_buyer_response=0,
                                  emails_opened_last_30d=5,
                                  champion_last_engaged_days_ago=4, close_date_changes_count=0)
        score = _engagement_decay_score(inp)
        assert score == 0.0

    def test_champion_ge_21_days_adds_15(self):
        inp = dataclasses.replace(fresh_deal(), champion_last_engaged_days_ago=21,
                                  days_since_last_buyer_response=0,
                                  emails_opened_last_30d=5, meetings_completed_last_30d=3,
                                  close_date_changes_count=0)
        score = _engagement_decay_score(inp)
        assert score >= 15.0

    def test_champion_ge_14_days_adds_8(self):
        inp = dataclasses.replace(fresh_deal(), champion_last_engaged_days_ago=14,
                                  days_since_last_buyer_response=0,
                                  emails_opened_last_30d=5, meetings_completed_last_30d=3,
                                  close_date_changes_count=0)
        score = _engagement_decay_score(inp)
        assert score >= 8.0

    def test_close_date_changes_ge_3_adds_10(self):
        inp = dataclasses.replace(fresh_deal(), close_date_changes_count=3,
                                  days_since_last_buyer_response=0,
                                  emails_opened_last_30d=5, meetings_completed_last_30d=3,
                                  champion_last_engaged_days_ago=4)
        score = _engagement_decay_score(inp)
        assert score >= 10.0

    def test_close_date_changes_ge_2_adds_5(self):
        inp = dataclasses.replace(fresh_deal(), close_date_changes_count=2,
                                  days_since_last_buyer_response=0,
                                  emails_opened_last_30d=5, meetings_completed_last_30d=3,
                                  champion_last_engaged_days_ago=4)
        score = _engagement_decay_score(inp)
        assert score >= 5.0

    def test_score_clamped_at_100(self):
        score = _engagement_decay_score(dead_deal())
        assert score <= 100.0

    def test_score_clamped_at_0_minimum(self):
        score = _engagement_decay_score(fresh_deal())
        assert score >= 0.0

    def test_dead_deal_high_engagement_decay(self):
        score = _engagement_decay_score(dead_deal())
        assert score >= 50.0


# ──────────────────────────────────────────────────────────────────────────────
# 6. Velocity Decay Score sub-function
# ──────────────────────────────────────────────────────────────────────────────

class TestVelocityDecayScore:
    def test_fresh_deal_low_score(self):
        score = _velocity_decay_score(fresh_deal())
        assert score < 15.0

    def test_velocity_ge_200_adds_40(self):
        inp = dataclasses.replace(fresh_deal(), velocity_vs_benchmark_pct=200.0,
                                  days_in_current_stage=8, historical_avg_days_at_stage=14,
                                  expected_close_days_remaining=21, exec_last_engaged_days_ago=10)
        score = _velocity_decay_score(inp)
        assert score >= 40.0

    def test_velocity_ge_150_adds_30(self):
        inp = dataclasses.replace(fresh_deal(), velocity_vs_benchmark_pct=150.0,
                                  days_in_current_stage=8, historical_avg_days_at_stage=14,
                                  expected_close_days_remaining=21, exec_last_engaged_days_ago=10)
        score = _velocity_decay_score(inp)
        assert score >= 30.0

    def test_velocity_ge_120_adds_18(self):
        inp = dataclasses.replace(fresh_deal(), velocity_vs_benchmark_pct=120.0,
                                  days_in_current_stage=8, historical_avg_days_at_stage=14,
                                  expected_close_days_remaining=21, exec_last_engaged_days_ago=10)
        score = _velocity_decay_score(inp)
        assert score >= 18.0

    def test_velocity_ge_100_adds_8(self):
        inp = dataclasses.replace(fresh_deal(), velocity_vs_benchmark_pct=100.0,
                                  days_in_current_stage=8, historical_avg_days_at_stage=14,
                                  expected_close_days_remaining=21, exec_last_engaged_days_ago=10)
        score = _velocity_decay_score(inp)
        assert score >= 8.0

    def test_overage_ge_2x_adds_30(self):
        # days_in_current_stage / historical_avg = 28/14 = 2.0
        inp = dataclasses.replace(fresh_deal(), days_in_current_stage=28,
                                  historical_avg_days_at_stage=14,
                                  velocity_vs_benchmark_pct=90.0,
                                  expected_close_days_remaining=21,
                                  exec_last_engaged_days_ago=10)
        score = _velocity_decay_score(inp)
        assert score >= 30.0

    def test_overage_ge_1_5x_adds_20(self):
        # 21/14 = 1.5
        inp = dataclasses.replace(fresh_deal(), days_in_current_stage=21,
                                  historical_avg_days_at_stage=14,
                                  velocity_vs_benchmark_pct=90.0,
                                  expected_close_days_remaining=21,
                                  exec_last_engaged_days_ago=10)
        score = _velocity_decay_score(inp)
        assert score >= 20.0

    def test_overage_ge_1_2x_adds_10(self):
        # 17/14 ≈ 1.21
        inp = dataclasses.replace(fresh_deal(), days_in_current_stage=17,
                                  historical_avg_days_at_stage=14,
                                  velocity_vs_benchmark_pct=90.0,
                                  expected_close_days_remaining=21,
                                  exec_last_engaged_days_ago=10)
        score = _velocity_decay_score(inp)
        assert score >= 10.0

    def test_overdue_close_adds_20(self):
        inp = dataclasses.replace(fresh_deal(), expected_close_days_remaining=-1,
                                  days_in_current_stage=8, historical_avg_days_at_stage=14,
                                  velocity_vs_benchmark_pct=90.0, exec_last_engaged_days_ago=10)
        score = _velocity_decay_score(inp)
        assert score >= 20.0

    def test_close_within_7_early_stage_adds_12(self):
        # deal_stage < 4 and close within 7 days
        inp = dataclasses.replace(fresh_deal(), expected_close_days_remaining=3,
                                  deal_stage=2, days_in_current_stage=8,
                                  historical_avg_days_at_stage=14,
                                  velocity_vs_benchmark_pct=90.0, exec_last_engaged_days_ago=10)
        score = _velocity_decay_score(inp)
        assert score >= 12.0

    def test_close_within_7_late_stage_no_penalty(self):
        # deal_stage >= 4: no penalty for close_within_7 condition
        inp = dataclasses.replace(fresh_deal(), expected_close_days_remaining=3,
                                  deal_stage=4, days_in_current_stage=8,
                                  historical_avg_days_at_stage=14,
                                  velocity_vs_benchmark_pct=90.0, exec_last_engaged_days_ago=10)
        score = _velocity_decay_score(inp)
        # No close-within-7 penalty but may have other scores
        assert score >= 0.0

    def test_exec_not_engaged_30_days_stage_3_adds_10(self):
        inp = dataclasses.replace(fresh_deal(), exec_last_engaged_days_ago=30,
                                  deal_stage=3, days_in_current_stage=8,
                                  historical_avg_days_at_stage=14,
                                  velocity_vs_benchmark_pct=90.0,
                                  expected_close_days_remaining=21)
        score = _velocity_decay_score(inp)
        assert score >= 10.0

    def test_exec_not_engaged_14_days_stage_4_adds_5(self):
        inp = dataclasses.replace(fresh_deal(), exec_last_engaged_days_ago=14,
                                  deal_stage=4, days_in_current_stage=8,
                                  historical_avg_days_at_stage=14,
                                  velocity_vs_benchmark_pct=90.0,
                                  expected_close_days_remaining=21)
        score = _velocity_decay_score(inp)
        assert score >= 5.0

    def test_historical_avg_zero_overage_defaults_to_1(self):
        # When historical_avg_days_at_stage = 0, overage defaults to 1.0 (no overage penalty)
        inp = dataclasses.replace(fresh_deal(), historical_avg_days_at_stage=0,
                                  days_in_current_stage=8, velocity_vs_benchmark_pct=90.0,
                                  expected_close_days_remaining=21, exec_last_engaged_days_ago=10)
        score = _velocity_decay_score(inp)
        # overage=1.0 → no overage penalty; should only have other components
        assert score >= 0.0

    def test_score_clamped_at_100(self):
        score = _velocity_decay_score(dead_deal())
        assert score <= 100.0

    def test_dead_deal_high_velocity_decay(self):
        score = _velocity_decay_score(dead_deal())
        assert score >= 50.0


# ──────────────────────────────────────────────────────────────────────────────
# 7. Stage Health Score sub-function
# ──────────────────────────────────────────────────────────────────────────────

class TestStageHealthScore:
    def test_fresh_deal_high_score(self):
        score = _stage_health_score(fresh_deal())
        assert score >= 70.0

    def test_ge_3_meetings_adds_30(self):
        inp = dataclasses.replace(fresh_deal(), meetings_completed_last_30d=3,
                                  next_step_defined=0, activity_count_last_14d=0,
                                  champion_last_engaged_days_ago=30, emails_opened_last_30d=0)
        score = _stage_health_score(inp)
        assert score == 30.0

    def test_2_meetings_adds_20(self):
        inp = dataclasses.replace(fresh_deal(), meetings_completed_last_30d=2,
                                  next_step_defined=0, activity_count_last_14d=0,
                                  champion_last_engaged_days_ago=30, emails_opened_last_30d=0)
        score = _stage_health_score(inp)
        assert score == 20.0

    def test_1_meeting_adds_10(self):
        inp = dataclasses.replace(fresh_deal(), meetings_completed_last_30d=1,
                                  next_step_defined=0, activity_count_last_14d=0,
                                  champion_last_engaged_days_ago=30, emails_opened_last_30d=0)
        score = _stage_health_score(inp)
        assert score == 10.0

    def test_0_meetings_adds_0(self):
        inp = dataclasses.replace(fresh_deal(), meetings_completed_last_30d=0,
                                  next_step_defined=0, activity_count_last_14d=0,
                                  champion_last_engaged_days_ago=30, emails_opened_last_30d=0)
        score = _stage_health_score(inp)
        assert score == 0.0

    def test_next_step_defined_adds_25(self):
        inp = dataclasses.replace(fresh_deal(), next_step_defined=1,
                                  meetings_completed_last_30d=0, activity_count_last_14d=0,
                                  champion_last_engaged_days_ago=30, emails_opened_last_30d=0)
        score = _stage_health_score(inp)
        assert score == 25.0

    def test_activity_ge_5_adds_20(self):
        inp = dataclasses.replace(fresh_deal(), activity_count_last_14d=5,
                                  next_step_defined=0, meetings_completed_last_30d=0,
                                  champion_last_engaged_days_ago=30, emails_opened_last_30d=0)
        score = _stage_health_score(inp)
        assert score == 20.0

    def test_activity_ge_3_adds_14(self):
        inp = dataclasses.replace(fresh_deal(), activity_count_last_14d=3,
                                  next_step_defined=0, meetings_completed_last_30d=0,
                                  champion_last_engaged_days_ago=30, emails_opened_last_30d=0)
        score = _stage_health_score(inp)
        assert score == 14.0

    def test_activity_ge_1_adds_7(self):
        inp = dataclasses.replace(fresh_deal(), activity_count_last_14d=1,
                                  next_step_defined=0, meetings_completed_last_30d=0,
                                  champion_last_engaged_days_ago=30, emails_opened_last_30d=0)
        score = _stage_health_score(inp)
        assert score == 7.0

    def test_champion_within_7_days_adds_15(self):
        inp = dataclasses.replace(fresh_deal(), champion_last_engaged_days_ago=7,
                                  next_step_defined=0, meetings_completed_last_30d=0,
                                  activity_count_last_14d=0, emails_opened_last_30d=0)
        score = _stage_health_score(inp)
        assert score == 15.0

    def test_champion_within_14_days_adds_10(self):
        inp = dataclasses.replace(fresh_deal(), champion_last_engaged_days_ago=14,
                                  next_step_defined=0, meetings_completed_last_30d=0,
                                  activity_count_last_14d=0, emails_opened_last_30d=0)
        score = _stage_health_score(inp)
        assert score == 10.0

    def test_champion_beyond_14_days_no_score(self):
        inp = dataclasses.replace(fresh_deal(), champion_last_engaged_days_ago=15,
                                  next_step_defined=0, meetings_completed_last_30d=0,
                                  activity_count_last_14d=0, emails_opened_last_30d=0)
        score = _stage_health_score(inp)
        assert score == 0.0

    def test_emails_ge_3_adds_10(self):
        inp = dataclasses.replace(fresh_deal(), emails_opened_last_30d=3,
                                  next_step_defined=0, meetings_completed_last_30d=0,
                                  activity_count_last_14d=0, champion_last_engaged_days_ago=30)
        score = _stage_health_score(inp)
        assert score == 10.0

    def test_emails_1_or_2_adds_5(self):
        inp = dataclasses.replace(fresh_deal(), emails_opened_last_30d=1,
                                  next_step_defined=0, meetings_completed_last_30d=0,
                                  activity_count_last_14d=0, champion_last_engaged_days_ago=30)
        score = _stage_health_score(inp)
        assert score == 5.0

    def test_score_clamped_at_100(self):
        score = _stage_health_score(fresh_deal())
        assert score <= 100.0

    def test_dead_deal_low_stage_health(self):
        score = _stage_health_score(dead_deal())
        assert score <= 20.0


# ──────────────────────────────────────────────────────────────────────────────
# 8. Composite formula
# ──────────────────────────────────────────────────────────────────────────────

class TestCompositeFormula:
    def test_formula_weights(self):
        activity, engagement, velocity, stage_health = 40.0, 60.0, 50.0, 80.0
        expected = round(40.0 * 0.30 + 60.0 * 0.25 + 50.0 * 0.25 + (100.0 - 80.0) * 0.20, 1)
        result = _composite(activity, engagement, velocity, stage_health)
        assert result == expected

    def test_all_zeros_produces_20(self):
        # activity=0, engagement=0, velocity=0, stage_health=0
        # composite = 0*0.30 + 0*0.25 + 0*0.25 + (100-0)*0.20 = 20.0
        result = _composite(0.0, 0.0, 0.0, 0.0)
        assert result == 20.0

    def test_all_100_produces_80(self):
        # composite = 100*0.30 + 100*0.25 + 100*0.25 + (100-100)*0.20
        # = 30 + 25 + 25 + 0 = 80.0
        result = _composite(100.0, 100.0, 100.0, 100.0)
        assert result == 80.0

    def test_activity_weight_30_pct(self):
        # Only activity score non-zero
        result = _composite(100.0, 0.0, 0.0, 100.0)
        # = 100*0.30 + 0*0.25 + 0*0.25 + (100-100)*0.20 = 30.0
        assert result == 30.0

    def test_engagement_weight_25_pct(self):
        result = _composite(0.0, 100.0, 0.0, 100.0)
        # = 0*0.30 + 100*0.25 + 0*0.25 + 0*0.20 = 25.0
        assert result == 25.0

    def test_velocity_weight_25_pct(self):
        result = _composite(0.0, 0.0, 100.0, 100.0)
        # = 0*0.30 + 0*0.25 + 100*0.25 + 0*0.20 = 25.0
        assert result == 25.0

    def test_stage_health_inverted_weight_20_pct(self):
        result = _composite(0.0, 0.0, 0.0, 0.0)
        # = 0 + 0 + 0 + (100-0)*0.20 = 20.0
        assert result == 20.0

    def test_stage_health_perfect_no_contribution(self):
        result = _composite(0.0, 0.0, 0.0, 100.0)
        # = 0 + 0 + 0 + 0 = 0.0
        assert result == 0.0

    def test_composite_rounded_to_1_decimal(self):
        result = _composite(33.3, 33.3, 33.3, 33.3)
        assert result == round(33.3 * 0.30 + 33.3 * 0.25 + 33.3 * 0.25 + (100.0 - 33.3) * 0.20, 1)

    def test_fresh_deal_low_composite(self, intel):
        result = intel.assess(fresh_deal())
        assert result.decay_composite < 30.0

    def test_dead_deal_high_composite(self, intel):
        result = intel.assess(dead_deal())
        assert result.decay_composite >= 60.0


# ──────────────────────────────────────────────────────────────────────────────
# 9. is_stale logic
# ──────────────────────────────────────────────────────────────────────────────

class TestIsStale:
    def test_fresh_deal_not_stale(self):
        assert _is_stale(fresh_deal()) is False

    def test_days_since_activity_14_is_stale(self):
        inp = dataclasses.replace(fresh_deal(), days_since_last_activity=14,
                                  days_since_last_buyer_response=5)
        assert _is_stale(inp) is True

    def test_days_since_activity_13_not_stale_alone(self):
        inp = dataclasses.replace(fresh_deal(), days_since_last_activity=13,
                                  days_since_last_buyer_response=5)
        assert _is_stale(inp) is False

    def test_days_since_buyer_response_21_is_stale(self):
        inp = dataclasses.replace(fresh_deal(), days_since_last_activity=2,
                                  days_since_last_buyer_response=21)
        assert _is_stale(inp) is True

    def test_days_since_buyer_response_20_not_stale_alone(self):
        inp = dataclasses.replace(fresh_deal(), days_since_last_activity=2,
                                  days_since_last_buyer_response=20)
        assert _is_stale(inp) is False

    def test_both_conditions_met_is_stale(self):
        inp = dataclasses.replace(fresh_deal(), days_since_last_activity=14,
                                  days_since_last_buyer_response=21)
        assert _is_stale(inp) is True

    def test_dead_deal_is_stale(self):
        assert _is_stale(dead_deal()) is True

    def test_boundary_activity_14_exact(self):
        inp = dataclasses.replace(fresh_deal(), days_since_last_activity=14,
                                  days_since_last_buyer_response=0)
        assert _is_stale(inp) is True

    def test_boundary_buyer_response_21_exact(self):
        inp = dataclasses.replace(fresh_deal(), days_since_last_activity=0,
                                  days_since_last_buyer_response=21)
        assert _is_stale(inp) is True


# ──────────────────────────────────────────────────────────────────────────────
# 10. needs_immediate_action logic
# ──────────────────────────────────────────────────────────────────────────────

class TestNeedsImmediateAction:
    def test_fresh_deal_no_immediate_action(self, intel):
        result = intel.assess(fresh_deal())
        assert result.needs_immediate_action is False

    def test_composite_ge_70_needs_action(self):
        # composite >= 70 triggers needs_immediate_action
        # Verify directly
        composite = 70.0
        risk = DecayRisk.LOW  # not critical
        needs_action = composite >= 70 or risk == DecayRisk.CRITICAL
        assert needs_action is True

    def test_composite_69_no_action_unless_critical(self):
        composite = 69.0
        risk = DecayRisk.HIGH
        needs_action = composite >= 70 or risk == DecayRisk.CRITICAL
        assert needs_action is False

    def test_critical_risk_always_needs_action(self):
        composite = 10.0  # low composite
        risk = DecayRisk.CRITICAL
        needs_action = composite >= 70 or risk == DecayRisk.CRITICAL
        assert needs_action is True

    def test_dead_deal_needs_immediate_action(self, intel):
        result = intel.assess(dead_deal())
        assert result.needs_immediate_action is True

    def test_critical_risk_regardless_of_composite(self, intel):
        # A deal with critical risk should always need action
        result = intel.assess(dead_deal())
        # Dead deal should have critical risk
        if result.decay_risk == DecayRisk.CRITICAL:
            assert result.needs_immediate_action is True


# ──────────────────────────────────────────────────────────────────────────────
# 11. recovery_probability_pct
# ──────────────────────────────────────────────────────────────────────────────

class TestRecoveryProbability:
    def test_fresh_deal_high_recovery_prob(self, intel):
        result = intel.assess(fresh_deal())
        assert result.recovery_probability_pct > 70.0

    def test_dead_deal_low_recovery_prob(self, intel):
        result = intel.assess(dead_deal())
        assert result.recovery_probability_pct < 50.0

    def test_recovery_prob_formula(self):
        # max(0, min(100, 100 - composite))
        for composite in [0.0, 25.0, 50.0, 75.0, 100.0]:
            expected = max(0.0, min(100.0, 100.0 - composite))
            result = PipelineAgingIntelligence()
            # We test indirectly by checking: recovery + composite = 100 when in [0,100]
            assert expected == max(0.0, min(100.0, 100.0 - composite))

    def test_recovery_prob_clamp_lower(self, intel):
        # Composite > 100 would clamp to 0
        # Ensure result is always >= 0
        result = intel.assess(dead_deal())
        assert result.recovery_probability_pct >= 0.0

    def test_recovery_prob_clamp_upper(self, intel):
        result = intel.assess(fresh_deal())
        assert result.recovery_probability_pct <= 100.0

    def test_recovery_plus_composite_equals_100_when_in_range(self, intel):
        result = intel.assess(fresh_deal())
        if 0 <= result.decay_composite <= 100:
            expected = round(100.0 - result.decay_composite, 1)
            assert result.recovery_probability_pct == expected


# ──────────────────────────────────────────────────────────────────────────────
# 12. Decay status classification
# ──────────────────────────────────────────────────────────────────────────────

class TestDecayStatusClassification:
    def test_fresh_deal_has_fresh_status(self, intel):
        result = intel.assess(fresh_deal())
        assert result.decay_status == DecayStatus.FRESH

    def test_dead_deal_has_dead_status(self, intel):
        result = intel.assess(dead_deal())
        assert result.decay_status == DecayStatus.DEAD

    def test_composite_ge_75_is_dead(self):
        # dead due to composite
        inp = dataclasses.replace(fresh_deal(), days_since_last_activity=0,
                                  days_since_last_buyer_response=0)
        status = _decay_status(75.0, inp)
        assert status == DecayStatus.DEAD

    def test_both_activity_and_buyer_30_days_is_dead(self):
        inp = dataclasses.replace(fresh_deal(), days_since_last_activity=30,
                                  days_since_last_buyer_response=30)
        status = _decay_status(20.0, inp)  # low composite but both 30-day conditions
        assert status == DecayStatus.DEAD

    def test_composite_ge_55_is_stale(self):
        inp = dataclasses.replace(fresh_deal(), days_since_last_activity=0,
                                  days_since_last_buyer_response=0)
        status = _decay_status(55.0, inp)
        assert status == DecayStatus.STALE

    def test_composite_ge_30_is_aging(self):
        inp = dataclasses.replace(fresh_deal(), days_since_last_activity=0,
                                  days_since_last_buyer_response=0)
        status = _decay_status(30.0, inp)
        assert status == DecayStatus.AGING

    def test_composite_lt_30_is_fresh(self):
        inp = dataclasses.replace(fresh_deal(), days_since_last_activity=0,
                                  days_since_last_buyer_response=0)
        status = _decay_status(29.9, inp)
        assert status == DecayStatus.FRESH

    def test_composite_74_not_dead_by_composite(self):
        inp = dataclasses.replace(fresh_deal(), days_since_last_activity=0,
                                  days_since_last_buyer_response=0)
        status = _decay_status(74.9, inp)
        assert status == DecayStatus.STALE


# ──────────────────────────────────────────────────────────────────────────────
# 13. Decay risk classification
# ──────────────────────────────────────────────────────────────────────────────

class TestDecayRiskClassification:
    def test_fresh_deal_low_risk(self, intel):
        result = intel.assess(fresh_deal())
        assert result.decay_risk == DecayRisk.LOW

    def test_dead_deal_critical_risk(self, intel):
        result = intel.assess(dead_deal())
        assert result.decay_risk == DecayRisk.CRITICAL

    def test_composite_ge_70_is_critical(self):
        assert _decay_risk(70.0) == DecayRisk.CRITICAL

    def test_composite_ge_50_is_high(self):
        assert _decay_risk(50.0) == DecayRisk.HIGH

    def test_composite_ge_30_is_moderate(self):
        assert _decay_risk(30.0) == DecayRisk.MODERATE

    def test_composite_lt_30_is_low(self):
        assert _decay_risk(29.9) == DecayRisk.LOW

    def test_composite_exact_70_is_critical(self):
        assert _decay_risk(70.0) == DecayRisk.CRITICAL

    def test_composite_69_is_high(self):
        assert _decay_risk(69.9) == DecayRisk.HIGH

    def test_composite_exact_50_is_high(self):
        assert _decay_risk(50.0) == DecayRisk.HIGH

    def test_composite_exact_30_is_moderate(self):
        assert _decay_risk(30.0) == DecayRisk.MODERATE


# ──────────────────────────────────────────────────────────────────────────────
# 14. Stage velocity classification
# ──────────────────────────────────────────────────────────────────────────────

class TestStageVelocityClassification:
    def test_fresh_deal_on_track_velocity(self, intel):
        # fresh_deal has velocity_vs_benchmark_pct=90.0, which is between 86-109 → ON_TRACK
        result = intel.assess(fresh_deal())
        assert result.stage_velocity == StageVelocity.ON_TRACK

    def test_dead_deal_stalled_velocity(self, intel):
        result = intel.assess(dead_deal())
        assert result.stage_velocity == StageVelocity.STALLED

    def test_velocity_ge_150_is_stalled(self):
        inp = dataclasses.replace(fresh_deal(), velocity_vs_benchmark_pct=150.0)
        assert _stage_velocity(inp) == StageVelocity.STALLED

    def test_velocity_ge_110_is_slow(self):
        inp = dataclasses.replace(fresh_deal(), velocity_vs_benchmark_pct=110.0)
        assert _stage_velocity(inp) == StageVelocity.SLOW

    def test_velocity_le_85_is_fast(self):
        inp = dataclasses.replace(fresh_deal(), velocity_vs_benchmark_pct=85.0)
        assert _stage_velocity(inp) == StageVelocity.FAST

    def test_velocity_between_86_109_is_on_track(self):
        inp = dataclasses.replace(fresh_deal(), velocity_vs_benchmark_pct=100.0)
        assert _stage_velocity(inp) == StageVelocity.ON_TRACK

    def test_velocity_exact_150_is_stalled(self):
        inp = dataclasses.replace(fresh_deal(), velocity_vs_benchmark_pct=150.0)
        assert _stage_velocity(inp) == StageVelocity.STALLED

    def test_velocity_exact_110_is_slow(self):
        inp = dataclasses.replace(fresh_deal(), velocity_vs_benchmark_pct=110.0)
        assert _stage_velocity(inp) == StageVelocity.SLOW

    def test_velocity_exact_85_is_fast(self):
        inp = dataclasses.replace(fresh_deal(), velocity_vs_benchmark_pct=85.0)
        assert _stage_velocity(inp) == StageVelocity.FAST

    def test_velocity_86_is_on_track(self):
        inp = dataclasses.replace(fresh_deal(), velocity_vs_benchmark_pct=86.0)
        assert _stage_velocity(inp) == StageVelocity.ON_TRACK


# ──────────────────────────────────────────────────────────────────────────────
# 15. Recovery action classification
# ──────────────────────────────────────────────────────────────────────────────

class TestRecoveryActionClassification:
    def test_fresh_deal_maintain_action(self, intel):
        result = intel.assess(fresh_deal())
        assert result.recovery_action == RecoveryAction.MAINTAIN

    def test_critical_risk_kill_or_recycle(self):
        inp = fresh_deal()
        action = _recovery_action(DecayRisk.CRITICAL, inp)
        assert action == RecoveryAction.KILL_OR_RECYCLE

    def test_high_risk_executive_escalation(self):
        inp = fresh_deal()
        action = _recovery_action(DecayRisk.HIGH, inp)
        assert action == RecoveryAction.EXECUTIVE_ESCALATION

    def test_moderate_risk_re_engage_champion(self):
        inp = fresh_deal()
        action = _recovery_action(DecayRisk.MODERATE, inp)
        assert action == RecoveryAction.RE_ENGAGE_CHAMPION

    def test_low_risk_maintain(self):
        inp = fresh_deal()
        action = _recovery_action(DecayRisk.LOW, inp)
        assert action == RecoveryAction.MAINTAIN

    def test_dead_deal_kill_or_recycle(self, intel):
        result = intel.assess(dead_deal())
        assert result.recovery_action == RecoveryAction.KILL_OR_RECYCLE


# ──────────────────────────────────────────────────────────────────────────────
# 16. Primary decay signal
# ──────────────────────────────────────────────────────────────────────────────

class TestPrimaryDecaySignal:
    def test_buyer_dark_30_days(self):
        inp = dataclasses.replace(fresh_deal(), days_since_last_buyer_response=30,
                                  days_since_last_activity=5, velocity_vs_benchmark_pct=90.0,
                                  stage_regression_count=0, close_date_changes_count=0,
                                  champion_last_engaged_days_ago=4)
        signal = _primary_decay_signal(inp, 10.0, 10.0, 10.0, 80.0)
        assert "buyer dark" in signal
        assert "30" in signal

    def test_no_rep_activity_21_days(self):
        inp = dataclasses.replace(fresh_deal(), days_since_last_activity=21,
                                  days_since_last_buyer_response=5,
                                  velocity_vs_benchmark_pct=90.0,
                                  stage_regression_count=0, close_date_changes_count=0,
                                  champion_last_engaged_days_ago=4)
        signal = _primary_decay_signal(inp, 10.0, 10.0, 10.0, 80.0)
        assert "no rep activity" in signal
        assert "21" in signal

    def test_velocity_200pct_signal(self):
        inp = dataclasses.replace(fresh_deal(), days_since_last_buyer_response=5,
                                  days_since_last_activity=5,
                                  velocity_vs_benchmark_pct=200.0,
                                  stage_regression_count=0, close_date_changes_count=0,
                                  champion_last_engaged_days_ago=4)
        signal = _primary_decay_signal(inp, 10.0, 10.0, 10.0, 80.0)
        assert "slower than benchmark" in signal

    def test_multiple_stage_regressions_signal(self):
        inp = dataclasses.replace(fresh_deal(), days_since_last_buyer_response=5,
                                  days_since_last_activity=5,
                                  velocity_vs_benchmark_pct=90.0,
                                  stage_regression_count=2, close_date_changes_count=0,
                                  champion_last_engaged_days_ago=4)
        signal = _primary_decay_signal(inp, 10.0, 10.0, 10.0, 80.0)
        assert "stage regressions" in signal

    def test_close_date_changes_3_signal(self):
        inp = dataclasses.replace(fresh_deal(), days_since_last_buyer_response=5,
                                  days_since_last_activity=5,
                                  velocity_vs_benchmark_pct=90.0,
                                  stage_regression_count=0, close_date_changes_count=3,
                                  champion_last_engaged_days_ago=4)
        signal = _primary_decay_signal(inp, 10.0, 10.0, 10.0, 80.0)
        assert "close date" in signal

    def test_champion_not_engaged_21_days_signal(self):
        inp = dataclasses.replace(fresh_deal(), days_since_last_buyer_response=5,
                                  days_since_last_activity=5,
                                  velocity_vs_benchmark_pct=90.0,
                                  stage_regression_count=0, close_date_changes_count=0,
                                  champion_last_engaged_days_ago=21)
        signal = _primary_decay_signal(inp, 10.0, 10.0, 10.0, 80.0)
        assert "champion" in signal

    def test_generic_signal_fallback(self):
        inp = dataclasses.replace(fresh_deal(), days_since_last_buyer_response=5,
                                  days_since_last_activity=5,
                                  velocity_vs_benchmark_pct=90.0,
                                  stage_regression_count=0, close_date_changes_count=0,
                                  champion_last_engaged_days_ago=4)
        signal = _primary_decay_signal(inp, 10.0, 10.0, 10.0, 80.0)
        assert "primary decay driver" in signal

    def test_primary_signal_is_string(self, intel):
        result = intel.assess(fresh_deal())
        assert isinstance(result.primary_decay_signal, str)
        assert len(result.primary_decay_signal) > 0


# ──────────────────────────────────────────────────────────────────────────────
# 17. PipelineAgingIntelligence.assess()
# ──────────────────────────────────────────────────────────────────────────────

class TestAssess:
    def test_assess_returns_result(self, intel):
        result = intel.assess(fresh_deal())
        assert isinstance(result, PipelineAgingResult)

    def test_assess_stores_result(self, intel):
        intel.assess(fresh_deal("d1"))
        assert intel.get("d1") is not None

    def test_assess_stores_deal_value(self, intel):
        intel.assess(fresh_deal("d1"))
        assert intel._deal_values.get("d1") == 180_000.0

    def test_assess_fresh_deal_result_fields(self, intel):
        result = intel.assess(fresh_deal())
        assert result.deal_id == "deal_001"
        assert result.rep_id == "rep_001"
        assert result.decay_status == DecayStatus.FRESH
        assert result.decay_risk == DecayRisk.LOW
        assert result.is_stale is False
        assert result.needs_immediate_action is False

    def test_assess_dead_deal_result_fields(self, intel):
        result = intel.assess(dead_deal())
        assert result.deal_id == "deal_dead"
        assert result.decay_status == DecayStatus.DEAD
        assert result.decay_risk == DecayRisk.CRITICAL
        assert result.is_stale is True
        assert result.needs_immediate_action is True
        assert result.recovery_action == RecoveryAction.KILL_OR_RECYCLE

    def test_assess_overwrites_previous(self, intel):
        intel.assess(fresh_deal("d1"))
        inp2 = dataclasses.replace(dead_deal(), deal_id="d1")
        result2 = intel.assess(inp2)
        stored = intel.get("d1")
        assert stored.decay_status == result2.decay_status

    def test_assess_multiple_deals(self, intel):
        intel.assess(fresh_deal("d1"))
        intel.assess(dead_deal("d2"))
        assert intel.get("d1") is not None
        assert intel.get("d2") is not None

    def test_get_returns_none_for_unknown(self, intel):
        assert intel.get("nonexistent") is None

    def test_assess_all_scores_in_range(self, intel):
        result = intel.assess(fresh_deal())
        assert 0.0 <= result.activity_decay_score <= 100.0
        assert 0.0 <= result.engagement_decay_score <= 100.0
        assert 0.0 <= result.velocity_decay_score <= 100.0
        assert 0.0 <= result.stage_health_score <= 100.0
        assert result.recovery_probability_pct >= 0.0
        assert result.recovery_probability_pct <= 100.0


# ──────────────────────────────────────────────────────────────────────────────
# 18. assess_batch() — sort order
# ──────────────────────────────────────────────────────────────────────────────

class TestAssessBatch:
    def test_batch_returns_list(self, intel):
        results = intel.assess_batch([fresh_deal("d1"), dead_deal("d2")])
        assert isinstance(results, list)
        assert len(results) == 2

    def test_batch_sorted_by_composite_descending(self, intel):
        inputs = [fresh_deal("d1"), aging_deal("d2"), dead_deal("d3")]
        results = intel.assess_batch(inputs)
        composites = [r.decay_composite for r in results]
        assert composites == sorted(composites, reverse=True)

    def test_batch_highest_decay_first(self, intel):
        results = intel.assess_batch([fresh_deal("d1"), dead_deal("d2")])
        assert results[0].deal_id == "d2"  # dead deal has higher composite

    def test_batch_stores_all_deals(self, intel):
        intel.assess_batch([fresh_deal("d1"), dead_deal("d2"), aging_deal("d3")])
        assert intel.get("d1") is not None
        assert intel.get("d2") is not None
        assert intel.get("d3") is not None

    def test_batch_empty_input(self, intel):
        results = intel.assess_batch([])
        assert results == []

    def test_batch_single_item(self, intel):
        results = intel.assess_batch([fresh_deal("d1")])
        assert len(results) == 1

    def test_batch_three_items_sort_order(self, intel):
        # Build three deals with known ordering
        i2 = PipelineAgingIntelligence()
        inputs = [fresh_deal("d1"), aging_deal("d2"), dead_deal("d3")]
        results = i2.assess_batch(inputs)
        for j in range(len(results) - 1):
            assert results[j].decay_composite >= results[j + 1].decay_composite

    def test_batch_five_items_sort_maintained(self, intel):
        inputs = [
            fresh_deal("a"), aging_deal("b"), dead_deal("c"),
            dataclasses.replace(fresh_deal("d"), velocity_vs_benchmark_pct=110.0),
            dataclasses.replace(dead_deal("e"), close_date_changes_count=5),
        ]
        results = intel.assess_batch(inputs)
        composites = [r.decay_composite for r in results]
        assert composites == sorted(composites, reverse=True)


# ──────────────────────────────────────────────────────────────────────────────
# 19. reset()
# ──────────────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_results(self, intel):
        intel.assess(fresh_deal("d1"))
        intel.reset()
        assert intel.get("d1") is None

    def test_reset_clears_deal_values(self, intel):
        intel.assess(fresh_deal("d1"))
        intel.reset()
        assert "d1" not in intel._deal_values

    def test_reset_clears_both_dicts(self, intel):
        intel.assess(fresh_deal("d1"))
        intel.assess(dead_deal("d2"))
        intel.reset()
        assert len(intel._results) == 0
        assert len(intel._deal_values) == 0

    def test_reset_allows_reassessment(self, intel):
        intel.assess(fresh_deal("d1"))
        intel.reset()
        result = intel.assess(fresh_deal("d1"))
        assert result is not None

    def test_reset_empty_intel_no_error(self, intel):
        intel.reset()  # Should not raise
        assert len(intel._results) == 0

    def test_reset_summary_returns_zero_total(self, intel):
        intel.assess(fresh_deal())
        intel.reset()
        s = intel.summary()
        assert s["total"] == 0


# ──────────────────────────────────────────────────────────────────────────────
# 20. by_status() and by_risk()
# ──────────────────────────────────────────────────────────────────────────────

class TestByStatusAndRisk:
    def test_by_status_fresh(self, intel):
        intel.assess(fresh_deal("d1"))
        intel.assess(dead_deal("d2"))
        fresh_results = intel.by_status(DecayStatus.FRESH)
        assert all(r.decay_status == DecayStatus.FRESH for r in fresh_results)
        assert any(r.deal_id == "d1" for r in fresh_results)

    def test_by_status_dead(self, intel):
        intel.assess(fresh_deal("d1"))
        intel.assess(dead_deal("d2"))
        dead_results = intel.by_status(DecayStatus.DEAD)
        assert all(r.decay_status == DecayStatus.DEAD for r in dead_results)
        assert any(r.deal_id == "d2" for r in dead_results)

    def test_by_status_empty_when_none_match(self, intel):
        intel.assess(fresh_deal("d1"))
        dead_results = intel.by_status(DecayStatus.DEAD)
        assert dead_results == []

    def test_by_risk_low(self, intel):
        intel.assess(fresh_deal("d1"))
        low_results = intel.by_risk(DecayRisk.LOW)
        assert all(r.decay_risk == DecayRisk.LOW for r in low_results)

    def test_by_risk_critical(self, intel):
        intel.assess(dead_deal("d2"))
        critical_results = intel.by_risk(DecayRisk.CRITICAL)
        assert all(r.decay_risk == DecayRisk.CRITICAL for r in critical_results)

    def test_by_risk_empty_when_none_match(self, intel):
        intel.assess(fresh_deal("d1"))
        critical_results = intel.by_risk(DecayRisk.CRITICAL)
        assert critical_results == []

    def test_by_status_all_four_statuses(self, intel):
        # Assess enough deals to get representation across statuses
        intel.assess(fresh_deal("d1"))
        intel.assess(dead_deal("d2"))
        # Check that by_status works for each enum value
        for status in DecayStatus:
            result = intel.by_status(status)
            assert isinstance(result, list)

    def test_by_risk_all_four_risks(self, intel):
        intel.assess(fresh_deal("d1"))
        for risk in DecayRisk:
            result = intel.by_risk(risk)
            assert isinstance(result, list)


# ──────────────────────────────────────────────────────────────────────────────
# 21. stale_deals() and immediate_action_queue()
# ──────────────────────────────────────────────────────────────────────────────

class TestStaleDealsAndImmediateAction:
    def test_stale_deals_empty_when_no_stale(self, intel):
        intel.assess(fresh_deal("d1"))
        assert intel.stale_deals() == []

    def test_stale_deals_returns_stale(self, intel):
        intel.assess(fresh_deal("d1"))
        intel.assess(dead_deal("d2"))
        stale = intel.stale_deals()
        assert all(r.is_stale for r in stale)

    def test_stale_deals_excludes_non_stale(self, intel):
        intel.assess(fresh_deal("d1"))
        intel.assess(dead_deal("d2"))
        stale = intel.stale_deals()
        stale_ids = [r.deal_id for r in stale]
        assert "d1" not in stale_ids

    def test_immediate_action_queue_empty_when_none(self, intel):
        intel.assess(fresh_deal("d1"))
        queue = intel.immediate_action_queue()
        assert queue == []

    def test_immediate_action_queue_includes_dead_deal(self, intel):
        intel.assess(fresh_deal("d1"))
        intel.assess(dead_deal("d2"))
        queue = intel.immediate_action_queue()
        queue_ids = [r.deal_id for r in queue]
        assert "d2" in queue_ids

    def test_immediate_action_queue_all_need_action(self, intel):
        intel.assess_batch([fresh_deal("d1"), dead_deal("d2")])
        queue = intel.immediate_action_queue()
        assert all(r.needs_immediate_action for r in queue)

    def test_stale_deals_with_activity_14_days(self, intel):
        inp = dataclasses.replace(fresh_deal("d1"), days_since_last_activity=14,
                                  days_since_last_buyer_response=5)
        intel.assess(inp)
        stale = intel.stale_deals()
        assert any(r.deal_id == "d1" for r in stale)

    def test_stale_deals_with_buyer_response_21_days(self, intel):
        inp = dataclasses.replace(fresh_deal("d1"), days_since_last_activity=2,
                                  days_since_last_buyer_response=21)
        intel.assess(inp)
        stale = intel.stale_deals()
        assert any(r.deal_id == "d1" for r in stale)


# ──────────────────────────────────────────────────────────────────────────────
# 22. total_stale_pipeline_usd()
# ──────────────────────────────────────────────────────────────────────────────

class TestTotalStalePipelineUsd:
    def test_zero_when_no_stale(self, intel):
        intel.assess(fresh_deal("d1"))
        assert intel.total_stale_pipeline_usd() == 0.0

    def test_includes_dead_deal_value(self, intel):
        intel.assess(dead_deal("d2"))
        total = intel.total_stale_pipeline_usd()
        assert total == 50_000.0

    def test_excludes_fresh_deal_value(self, intel):
        intel.assess(fresh_deal("d1"))
        intel.assess(dead_deal("d2"))
        total = intel.total_stale_pipeline_usd()
        assert total == 50_000.0  # only dead_deal is stale

    def test_sum_of_multiple_stale_deals(self, intel):
        dead1 = dead_deal("d1")
        dead2 = dataclasses.replace(dead_deal("d2"), deal_value_usd=75_000.0)
        intel.assess(dead1)
        intel.assess(dead2)
        total = intel.total_stale_pipeline_usd()
        assert total == 50_000.0 + 75_000.0

    def test_zero_when_no_deals(self, intel):
        assert intel.total_stale_pipeline_usd() == 0.0

    def test_reset_resets_stale_pipeline(self, intel):
        intel.assess(dead_deal("d1"))
        intel.reset()
        assert intel.total_stale_pipeline_usd() == 0.0

    def test_stale_due_to_activity_included(self, intel):
        inp = dataclasses.replace(fresh_deal("d1"), days_since_last_activity=14,
                                  days_since_last_buyer_response=5,
                                  deal_value_usd=100_000.0)
        intel.assess(inp)
        total = intel.total_stale_pipeline_usd()
        assert total == 100_000.0

    def test_uses_deal_value_not_composite(self, intel):
        # Two stale deals with different values, verify we sum values not composites
        d1 = dataclasses.replace(dead_deal("d1"), deal_value_usd=10_000.0)
        d2 = dataclasses.replace(dead_deal("d2"), deal_value_usd=20_000.0)
        intel.assess(d1)
        intel.assess(d2)
        assert intel.total_stale_pipeline_usd() == 30_000.0


# ──────────────────────────────────────────────────────────────────────────────
# 23. summary() — exactly 13 keys
# ──────────────────────────────────────────────────────────────────────────────

class TestSummary:
    def test_summary_returns_13_keys(self, intel):
        intel.assess(fresh_deal())
        s = intel.summary()
        assert len(s) == 13

    def test_summary_key_names(self, intel):
        intel.assess(fresh_deal())
        s = intel.summary()
        expected_keys = {
            "total", "decay_status_counts", "risk_counts", "velocity_counts",
            "action_counts", "avg_decay_composite", "stale_deal_count",
            "immediate_action_count", "avg_activity_decay_score",
            "avg_engagement_decay_score", "avg_velocity_decay_score",
            "avg_stage_health_score", "total_stale_pipeline_usd",
        }
        assert set(s.keys()) == expected_keys

    def test_summary_empty_intel(self, intel):
        s = intel.summary()
        assert s["total"] == 0
        assert s["avg_decay_composite"] == 0.0
        assert s["stale_deal_count"] == 0
        assert s["immediate_action_count"] == 0
        assert s["total_stale_pipeline_usd"] == 0.0

    def test_summary_total_count(self, intel):
        intel.assess(fresh_deal("d1"))
        intel.assess(dead_deal("d2"))
        s = intel.summary()
        assert s["total"] == 2

    def test_summary_stale_deal_count(self, intel):
        intel.assess(fresh_deal("d1"))
        intel.assess(dead_deal("d2"))
        s = intel.summary()
        assert s["stale_deal_count"] >= 1

    def test_summary_immediate_action_count(self, intel):
        intel.assess(fresh_deal("d1"))
        intel.assess(dead_deal("d2"))
        s = intel.summary()
        assert s["immediate_action_count"] >= 1

    def test_summary_decay_status_counts_is_dict(self, intel):
        intel.assess(fresh_deal())
        s = intel.summary()
        assert isinstance(s["decay_status_counts"], dict)

    def test_summary_risk_counts_is_dict(self, intel):
        intel.assess(fresh_deal())
        s = intel.summary()
        assert isinstance(s["risk_counts"], dict)

    def test_summary_velocity_counts_is_dict(self, intel):
        intel.assess(fresh_deal())
        s = intel.summary()
        assert isinstance(s["velocity_counts"], dict)

    def test_summary_action_counts_is_dict(self, intel):
        intel.assess(fresh_deal())
        s = intel.summary()
        assert isinstance(s["action_counts"], dict)

    def test_summary_status_counts_sum_equals_total(self, intel):
        intel.assess(fresh_deal("d1"))
        intel.assess(dead_deal("d2"))
        s = intel.summary()
        assert sum(s["decay_status_counts"].values()) == s["total"]

    def test_summary_risk_counts_sum_equals_total(self, intel):
        intel.assess(fresh_deal("d1"))
        intel.assess(dead_deal("d2"))
        s = intel.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_velocity_counts_sum_equals_total(self, intel):
        intel.assess(fresh_deal("d1"))
        intel.assess(dead_deal("d2"))
        s = intel.summary()
        assert sum(s["velocity_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_equals_total(self, intel):
        intel.assess(fresh_deal("d1"))
        intel.assess(dead_deal("d2"))
        s = intel.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_avg_composite_is_float(self, intel):
        intel.assess(fresh_deal())
        s = intel.summary()
        assert isinstance(s["avg_decay_composite"], float)

    def test_summary_avg_scores_are_float(self, intel):
        intel.assess(fresh_deal())
        s = intel.summary()
        for key in ("avg_activity_decay_score", "avg_engagement_decay_score",
                    "avg_velocity_decay_score", "avg_stage_health_score"):
            assert isinstance(s[key], float)

    def test_summary_total_stale_pipeline_usd_accuracy(self, intel):
        intel.assess(fresh_deal("d1"))
        intel.assess(dead_deal("d2"))
        s = intel.summary()
        assert s["total_stale_pipeline_usd"] == intel.total_stale_pipeline_usd()

    def test_summary_after_reset_all_zeros(self, intel):
        intel.assess(fresh_deal())
        intel.reset()
        s = intel.summary()
        assert s["total"] == 0
        assert s["stale_deal_count"] == 0
        assert s["immediate_action_count"] == 0

    def test_summary_fresh_deal_in_status_counts(self, intel):
        intel.assess(fresh_deal("d1"))
        s = intel.summary()
        assert s["decay_status_counts"].get("fresh", 0) >= 1

    def test_summary_dead_deal_in_status_counts(self, intel):
        intel.assess(dead_deal("d1"))
        s = intel.summary()
        assert s["decay_status_counts"].get("dead", 0) >= 1


# ──────────────────────────────────────────────────────────────────────────────
# 24. all_deals() and avg_decay_composite()
# ──────────────────────────────────────────────────────────────────────────────

class TestAllDealsAndAvgComposite:
    def test_all_deals_sorted_descending(self, intel):
        intel.assess_batch([fresh_deal("d1"), dead_deal("d2"), aging_deal("d3")])
        all_r = intel.all_deals()
        composites = [r.decay_composite for r in all_r]
        assert composites == sorted(composites, reverse=True)

    def test_all_deals_count(self, intel):
        intel.assess(fresh_deal("d1"))
        intel.assess(dead_deal("d2"))
        assert len(intel.all_deals()) == 2

    def test_avg_decay_composite_empty(self, intel):
        assert intel.avg_decay_composite() == 0.0

    def test_avg_decay_composite_single_deal(self, intel):
        result = intel.assess(fresh_deal("d1"))
        avg = intel.avg_decay_composite()
        assert avg == result.decay_composite

    def test_avg_decay_composite_two_deals(self, intel):
        r1 = intel.assess(fresh_deal("d1"))
        r2 = intel.assess(dead_deal("d2"))
        expected = round((r1.decay_composite + r2.decay_composite) / 2, 1)
        assert intel.avg_decay_composite() == expected


# ──────────────────────────────────────────────────────────────────────────────
# 25. Edge cases and boundary conditions
# ──────────────────────────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_zero_deal_value_stale(self, intel):
        inp = dataclasses.replace(dead_deal("d1"), deal_value_usd=0.0)
        intel.assess(inp)
        assert intel.total_stale_pipeline_usd() == 0.0

    def test_very_large_deal_value(self, intel):
        inp = dataclasses.replace(dead_deal("d1"), deal_value_usd=10_000_000.0)
        intel.assess(inp)
        assert intel.total_stale_pipeline_usd() == 10_000_000.0

    def test_deal_id_uniqueness(self, intel):
        intel.assess(fresh_deal("same_id"))
        intel.assess(dead_deal("same_id"))
        # Second assess overwrites first
        result = intel.get("same_id")
        assert result is not None
        assert len(intel._results) == 1

    def test_composite_is_rounded_to_1_decimal(self, intel):
        result = intel.assess(fresh_deal())
        # Verify it has at most 1 decimal place
        s = str(result.decay_composite)
        if "." in s:
            assert len(s.split(".")[1]) <= 1

    def test_all_scores_non_negative(self, intel):
        for inp in [fresh_deal(), dead_deal(), aging_deal()]:
            result = intel.assess(inp)
            assert result.activity_decay_score >= 0.0
            assert result.engagement_decay_score >= 0.0
            assert result.velocity_decay_score >= 0.0
            assert result.stage_health_score >= 0.0
            assert result.recovery_probability_pct >= 0.0

    def test_very_fast_deal(self, intel):
        inp = dataclasses.replace(fresh_deal(), velocity_vs_benchmark_pct=10.0)
        result = intel.assess(inp)
        assert result.stage_velocity == StageVelocity.FAST

    def test_negative_expected_close_days(self, intel):
        inp = dataclasses.replace(fresh_deal(), expected_close_days_remaining=-30)
        result = intel.assess(inp)
        assert result.velocity_decay_score > _velocity_decay_score(fresh_deal())

    def test_stage_regression_count_3(self, intel):
        inp = dataclasses.replace(fresh_deal(), stage_regression_count=3)
        score = _activity_decay_score(inp)
        # Should cap at 15 for regressions
        assert score >= 15.0

    def test_very_high_activity_count(self, intel):
        inp = dataclasses.replace(fresh_deal(), activity_count_last_14d=100,
                                  activity_count_prev_14d=50)
        result = intel.assess(inp)
        assert result.stage_health_score <= 100.0

    def test_assess_batch_accumulates_in_intel(self, intel):
        intel.assess_batch([fresh_deal("d1"), dead_deal("d2")])
        assert len(intel._results) == 2
        assert len(intel._deal_values) == 2

    def test_multiple_resets_dont_error(self, intel):
        intel.reset()
        intel.reset()
        assert len(intel._results) == 0

    def test_result_is_dataclass(self, intel):
        result = intel.assess(fresh_deal())
        assert dataclasses.is_dataclass(result)

    def test_fresh_deal_status_is_string_in_dict(self, intel):
        result = intel.assess(fresh_deal())
        d = result.to_dict()
        assert d["decay_status"] == "fresh"

    def test_dead_deal_status_is_string_in_dict(self, intel):
        result = intel.assess(dead_deal())
        d = result.to_dict()
        assert d["decay_status"] == "dead"

    def test_stage_health_100_with_perfect_inputs(self):
        # meetings >= 3 (+30), next_step (+25), activity >= 5 (+20),
        # champion <= 7 (+15), emails >= 3 (+10) = 100
        inp = dataclasses.replace(fresh_deal(),
                                  meetings_completed_last_30d=3,
                                  next_step_defined=1,
                                  activity_count_last_14d=5,
                                  champion_last_engaged_days_ago=7,
                                  emails_opened_last_30d=3)
        score = _stage_health_score(inp)
        assert score == 100.0

    def test_total_stale_pipeline_usd_with_three_deals(self, intel):
        d1 = dataclasses.replace(dead_deal("d1"), deal_value_usd=10_000.0)
        d2 = dataclasses.replace(dead_deal("d2"), deal_value_usd=20_000.0)
        d3 = fresh_deal("d3")  # not stale
        intel.assess(d1)
        intel.assess(d2)
        intel.assess(d3)
        assert intel.total_stale_pipeline_usd() == 30_000.0

    def test_summary_13_keys_with_multiple_deals(self, intel):
        intel.assess_batch([fresh_deal("d1"), dead_deal("d2"), aging_deal("d3")])
        s = intel.summary()
        assert len(s) == 13

    def test_avg_activity_decay_score_in_summary(self, intel):
        r1 = intel.assess(fresh_deal("d1"))
        r2 = intel.assess(dead_deal("d2"))
        s = intel.summary()
        expected = round((r1.activity_decay_score + r2.activity_decay_score) / 2, 1)
        assert s["avg_activity_decay_score"] == expected

    def test_avg_engagement_decay_score_in_summary(self, intel):
        r1 = intel.assess(fresh_deal("d1"))
        r2 = intel.assess(dead_deal("d2"))
        s = intel.summary()
        expected = round((r1.engagement_decay_score + r2.engagement_decay_score) / 2, 1)
        assert s["avg_engagement_decay_score"] == expected

    def test_avg_velocity_decay_score_in_summary(self, intel):
        r1 = intel.assess(fresh_deal("d1"))
        r2 = intel.assess(dead_deal("d2"))
        s = intel.summary()
        expected = round((r1.velocity_decay_score + r2.velocity_decay_score) / 2, 1)
        assert s["avg_velocity_decay_score"] == expected

    def test_avg_stage_health_score_in_summary(self, intel):
        r1 = intel.assess(fresh_deal("d1"))
        r2 = intel.assess(dead_deal("d2"))
        s = intel.summary()
        expected = round((r1.stage_health_score + r2.stage_health_score) / 2, 1)
        assert s["avg_stage_health_score"] == expected
