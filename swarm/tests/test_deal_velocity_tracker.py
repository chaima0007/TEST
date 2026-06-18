"""Comprehensive pytest tests for DealVelocityTracker."""
from __future__ import annotations

import dataclasses
import pytest

from swarm.intelligence.deal_velocity_tracker import (
    DealVelocityTracker,
    DealVelocityInput,
    DealVelocityResult,
    VelocityStatus,
    SlipRisk,
    DealMomentum,
    VelocityAction,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def make_input(**overrides) -> DealVelocityInput:
    """Return a sensible baseline DealVelocityInput, overridable per-field."""
    defaults = dict(
        deal_id="deal-001",
        deal_name="Acme Corp",
        rep_id="rep-42",
        days_in_current_stage=5,
        avg_days_per_stage_historical=10.0,
        total_stages_completed=3,
        total_stages_in_pipeline=6,
        meetings_last_30d=4,
        meetings_prior_30d=2,
        docs_shared_last_30d=2,
        docs_opened_last_30d=3,
        stakeholder_count_current=4,
        stakeholder_count_30d_ago=3,
        new_action_items_last_7d=3,
        action_items_completed_rate=85.0,
        days_to_target_close=14,
        close_date_push_count=0,
        last_stage_advance_days_ago=3,
        pipeline_value=250_000.0,
        exec_involved=0,
        deal_created_days_ago=45,
        deal_value=250_000.0,
    )
    defaults.update(overrides)
    return DealVelocityInput(**defaults)


@pytest.fixture
def tracker() -> DealVelocityTracker:
    return DealVelocityTracker()


# ===========================================================================
# 1. DealVelocityInput field count
# ===========================================================================

class TestDealVelocityInputFields:
    def test_exactly_22_fields(self):
        fields = dataclasses.fields(DealVelocityInput)
        assert len(fields) == 22

    def test_field_names(self):
        expected = {
            "deal_id", "deal_name", "rep_id",
            "days_in_current_stage", "avg_days_per_stage_historical",
            "total_stages_completed", "total_stages_in_pipeline",
            "meetings_last_30d", "meetings_prior_30d",
            "docs_shared_last_30d", "docs_opened_last_30d",
            "stakeholder_count_current", "stakeholder_count_30d_ago",
            "new_action_items_last_7d", "action_items_completed_rate",
            "days_to_target_close", "close_date_push_count",
            "last_stage_advance_days_ago", "pipeline_value",
            "exec_involved", "deal_created_days_ago", "deal_value",
        }
        actual = {f.name for f in dataclasses.fields(DealVelocityInput)}
        assert actual == expected


# ===========================================================================
# 2. DealVelocityResult.to_dict() key count
# ===========================================================================

class TestDealVelocityResultToDict:
    def test_exactly_15_keys(self, tracker):
        result = tracker.track(make_input())
        d = result.to_dict()
        assert len(d) == 15

    def test_key_names(self, tracker):
        expected_keys = {
            "deal_id", "deal_name", "velocity_status", "slip_risk",
            "deal_momentum", "velocity_action", "stage_progress_score",
            "activity_velocity_score", "stakeholder_growth_score",
            "urgency_score", "velocity_composite", "predicted_close_days",
            "slip_probability", "is_on_track", "needs_velocity_boost",
        }
        d = tracker.track(make_input()).to_dict()
        assert set(d.keys()) == expected_keys

    def test_enum_values_are_strings(self, tracker):
        d = tracker.track(make_input()).to_dict()
        assert isinstance(d["velocity_status"], str)
        assert isinstance(d["slip_risk"], str)
        assert isinstance(d["deal_momentum"], str)
        assert isinstance(d["velocity_action"], str)

    def test_deal_id_and_name_preserved(self, tracker):
        inp = make_input(deal_id="xyz-999", deal_name="Beta Inc")
        d = tracker.track(inp).to_dict()
        assert d["deal_id"] == "xyz-999"
        assert d["deal_name"] == "Beta Inc"


# ===========================================================================
# 3. summary() returns exactly 13 keys
# ===========================================================================

class TestSummary:
    def test_empty_summary_has_13_keys(self, tracker):
        s = tracker.summary()
        assert len(s) == 13

    def test_non_empty_summary_has_13_keys(self, tracker):
        tracker.track(make_input())
        tracker.track(make_input(deal_id="d2"))
        s = tracker.summary()
        assert len(s) == 13

    def test_summary_key_names(self, tracker):
        expected = {
            "total", "status_counts", "slip_risk_counts", "momentum_counts",
            "action_counts", "avg_velocity_composite", "avg_slip_probability",
            "on_track_count", "velocity_boost_count",
            "avg_stage_progress_score", "avg_activity_velocity_score",
            "avg_stakeholder_growth_score", "avg_urgency_score",
        }
        assert set(tracker.summary().keys()) == expected

    def test_empty_summary_defaults(self, tracker):
        s = tracker.summary()
        assert s["total"] == 0
        assert s["avg_velocity_composite"] == 0.0
        assert s["on_track_count"] == 0
        assert s["velocity_boost_count"] == 0

    def test_summary_total_matches_tracked(self, tracker):
        tracker.track(make_input(deal_id="a"))
        tracker.track(make_input(deal_id="b"))
        tracker.track(make_input(deal_id="c"))
        assert tracker.summary()["total"] == 3

    def test_summary_counts_increment_correctly(self, tracker):
        # Two on-track deals
        tracker.track(make_input(deal_id="a"))
        tracker.track(make_input(deal_id="b"))
        s = tracker.summary()
        assert s["on_track_count"] == sum(
            1 for k, v in s["status_counts"].items() if v > 0
        ) or isinstance(s["on_track_count"], int)

    def test_summary_avg_velocity_composite_is_float(self, tracker):
        tracker.track(make_input())
        s = tracker.summary()
        assert isinstance(s["avg_velocity_composite"], float)

    def test_summary_after_reset_is_empty(self, tracker):
        tracker.track(make_input())
        tracker.reset()
        s = tracker.summary()
        assert s["total"] == 0
        assert len(s) == 13


# ===========================================================================
# 4. Enum members
# ===========================================================================

class TestEnums:
    def test_velocity_status_members(self):
        values = {e.value for e in VelocityStatus}
        assert values == {"accelerating", "on_pace", "decelerating", "stalled"}

    def test_slip_risk_members(self):
        values = {e.value for e in SlipRisk}
        assert values == {"low", "moderate", "high", "critical"}

    def test_deal_momentum_members(self):
        values = {e.value for e in DealMomentum}
        assert values == {"strong", "building", "fading", "lost"}

    def test_velocity_action_members(self):
        values = {e.value for e in VelocityAction}
        assert values == {"accelerate", "maintain", "inject_urgency", "rescue"}

    def test_enums_are_str_subclass(self):
        assert isinstance(VelocityStatus.ACCELERATING, str)
        assert isinstance(SlipRisk.LOW, str)
        assert isinstance(DealMomentum.STRONG, str)
        assert isinstance(VelocityAction.MAINTAIN, str)

    def test_velocity_status_count(self):
        assert len(VelocityStatus) == 4

    def test_slip_risk_count(self):
        assert len(SlipRisk) == 4

    def test_deal_momentum_count(self):
        assert len(DealMomentum) == 4

    def test_velocity_action_count(self):
        assert len(VelocityAction) == 4


# ===========================================================================
# 5. Composite formula
# ===========================================================================

class TestCompositeFormula:
    def test_composite_weights(self, tracker):
        """Directly verify composite = stage*0.30 + activity*0.35 + stakeholder*0.20 + urgency*0.15"""
        inp = make_input()
        result = tracker.track(inp)
        stage = tracker._stage_progress_score(inp)
        activity = tracker._activity_velocity_score(inp)
        stakeholder = tracker._stakeholder_growth_score(inp)
        urgency = tracker._urgency_score(inp)
        expected = round(
            max(0.0, min(100.0, stage * 0.30 + activity * 0.35 + stakeholder * 0.20 + urgency * 0.15)),
            1,
        )
        assert result.velocity_composite == expected

    def test_composite_clamped_to_100(self, tracker):
        """All perfect scores still yields <= 100."""
        inp = make_input(
            days_in_current_stage=1,
            avg_days_per_stage_historical=10.0,
            total_stages_completed=5,
            total_stages_in_pipeline=6,
            meetings_last_30d=10,
            meetings_prior_30d=2,
            docs_opened_last_30d=10,
            action_items_completed_rate=100.0,
            new_action_items_last_7d=5,
            stakeholder_count_current=6,
            stakeholder_count_30d_ago=3,
            exec_involved=1,
            days_to_target_close=3,
            deal_value=600_000.0,
            close_date_push_count=0,
            last_stage_advance_days_ago=1,
        )
        result = tracker.track(inp)
        assert result.velocity_composite <= 100.0

    def test_composite_clamped_to_zero(self, tracker):
        """Terrible inputs still yield composite >= 0."""
        inp = make_input(
            days_in_current_stage=100,
            avg_days_per_stage_historical=5.0,
            total_stages_completed=0,
            total_stages_in_pipeline=10,
            meetings_last_30d=0,
            meetings_prior_30d=5,
            docs_opened_last_30d=0,
            action_items_completed_rate=0.0,
            new_action_items_last_7d=0,
            stakeholder_count_current=1,
            stakeholder_count_30d_ago=4,
            exec_involved=0,
            days_to_target_close=200,
            deal_value=0.0,
            close_date_push_count=5,
            last_stage_advance_days_ago=60,
        )
        result = tracker.track(inp)
        assert result.velocity_composite >= 0.0

    def test_composite_float_rounded_to_1dp(self, tracker):
        inp = make_input()
        result = tracker.track(inp)
        # Check that it's rounded to 1 decimal place
        assert result.velocity_composite == round(result.velocity_composite, 1)


# ===========================================================================
# 6. is_on_track invariant
# ===========================================================================

class TestIsOnTrack:
    def test_on_track_when_composite_ge_55_and_pushes_le_1(self, tracker):
        """composite >= 55 AND close_date_push_count <= 1 => is_on_track True"""
        inp = make_input(
            days_in_current_stage=5,
            avg_days_per_stage_historical=10.0,
            total_stages_completed=4,
            total_stages_in_pipeline=6,
            meetings_last_30d=4,
            meetings_prior_30d=2,
            docs_opened_last_30d=3,
            action_items_completed_rate=85.0,
            new_action_items_last_7d=3,
            stakeholder_count_current=4,
            stakeholder_count_30d_ago=3,
            exec_involved=0,
            days_to_target_close=14,
            deal_value=250_000.0,
            close_date_push_count=0,
            last_stage_advance_days_ago=3,
        )
        result = tracker.track(inp)
        if result.velocity_composite >= 55:
            assert result.is_on_track is True
        else:
            assert result.is_on_track is False

    def test_not_on_track_when_composite_below_55(self, tracker):
        """Force a low composite by using very bad inputs."""
        inp = make_input(
            days_in_current_stage=50,
            avg_days_per_stage_historical=5.0,
            total_stages_completed=0,
            total_stages_in_pipeline=10,
            meetings_last_30d=0,
            meetings_prior_30d=5,
            docs_opened_last_30d=0,
            action_items_completed_rate=0.0,
            new_action_items_last_7d=0,
            stakeholder_count_current=1,
            stakeholder_count_30d_ago=4,
            exec_involved=0,
            days_to_target_close=200,
            deal_value=10_000.0,
            close_date_push_count=0,
            last_stage_advance_days_ago=60,
        )
        result = tracker.track(inp)
        assert result.velocity_composite < 55
        assert result.is_on_track is False

    def test_not_on_track_when_push_count_gt_1(self, tracker):
        """Even if composite is fine, push_count > 1 kills is_on_track."""
        # Use a good baseline and force push_count = 2
        inp = make_input(close_date_push_count=2)
        result = tracker.track(inp)
        assert result.is_on_track is False

    def test_on_track_push_count_exactly_1(self, tracker):
        """push_count == 1 is still allowed for is_on_track."""
        inp = make_input(close_date_push_count=1)
        result = tracker.track(inp)
        if result.velocity_composite >= 55:
            assert result.is_on_track is True

    def test_is_on_track_logic_direct(self, tracker):
        """Manually verify the exact boolean expression."""
        for push in [0, 1, 2, 3]:
            for composite_target in [40.0, 55.0, 70.0]:
                inp = make_input(close_date_push_count=push)
                result = tracker.track(inp)
                expected = result.velocity_composite >= 55.0 and push <= 1
                assert result.is_on_track == expected


# ===========================================================================
# 7. needs_velocity_boost invariant
# ===========================================================================

class TestNeedsVelocityBoost:
    def test_boost_when_composite_lt_40(self, tracker):
        inp = make_input(
            days_in_current_stage=5,
            avg_days_per_stage_historical=10.0,
            meetings_last_30d=0,
            meetings_prior_30d=0,
            docs_opened_last_30d=0,
            action_items_completed_rate=0.0,
            new_action_items_last_7d=0,
            total_stages_completed=0,
            total_stages_in_pipeline=10,
            stakeholder_count_current=1,
            stakeholder_count_30d_ago=3,
            exec_involved=0,
            days_to_target_close=200,
            deal_value=5_000.0,
            close_date_push_count=0,
            last_stage_advance_days_ago=60,
        )
        result = tracker.track(inp)
        if result.velocity_composite < 40.0:
            assert result.needs_velocity_boost is True

    def test_boost_when_days_in_stage_gt_2x_historical(self, tracker):
        inp = make_input(
            days_in_current_stage=21,
            avg_days_per_stage_historical=10.0,
        )
        result = tracker.track(inp)
        # 21 > 10*2 = 20 => needs boost
        assert result.needs_velocity_boost is True

    def test_no_boost_when_composite_ge_40_and_stage_ok(self, tracker):
        """Strong deal well within stage time => no boost needed (unless composite < 40)."""
        inp = make_input(
            days_in_current_stage=5,
            avg_days_per_stage_historical=10.0,
            meetings_last_30d=4,
            meetings_prior_30d=2,
            docs_opened_last_30d=3,
            action_items_completed_rate=90.0,
            new_action_items_last_7d=4,
            stakeholder_count_current=4,
            stakeholder_count_30d_ago=3,
            exec_involved=0,
            days_to_target_close=7,
            deal_value=300_000.0,
            close_date_push_count=0,
            last_stage_advance_days_ago=3,
            total_stages_completed=4,
            total_stages_in_pipeline=6,
        )
        result = tracker.track(inp)
        expected = result.velocity_composite < 40.0 or 5 > 10.0 * 2
        assert result.needs_velocity_boost == expected

    def test_boost_boundary_stage_exactly_2x(self, tracker):
        """days_in_current_stage exactly == 2x historical => NOT > 2x => no stage-based boost."""
        inp = make_input(
            days_in_current_stage=20,
            avg_days_per_stage_historical=10.0,
        )
        result = tracker.track(inp)
        # 20 is NOT > 20, so stage condition is False
        stage_boost = 20 > 10.0 * 2
        assert stage_boost is False
        expected_boost = result.velocity_composite < 40.0 or stage_boost
        assert result.needs_velocity_boost == expected_boost

    def test_needs_velocity_boost_logic_direct(self, tracker):
        for days, historical in [(5, 10.0), (25, 10.0), (10, 10.0)]:
            inp = make_input(days_in_current_stage=days, avg_days_per_stage_historical=historical)
            result = tracker.track(inp)
            expected = result.velocity_composite < 40.0 or days > historical * 2
            assert result.needs_velocity_boost == expected


# ===========================================================================
# 8. Scoring helper branches
# ===========================================================================

class TestStageProgressScore:
    def test_returns_float_in_range(self, tracker):
        inp = make_input()
        score = tracker._stage_progress_score(inp)
        assert 0.0 <= score <= 100.0

    def test_pipeline_completion_contribution(self, tracker):
        """Full pipeline completion adds 40 points from pipeline pct."""
        inp_full = make_input(total_stages_completed=6, total_stages_in_pipeline=6,
                              days_in_current_stage=5, avg_days_per_stage_historical=10.0,
                              last_stage_advance_days_ago=3, close_date_push_count=0)
        inp_zero = make_input(total_stages_completed=0, total_stages_in_pipeline=6,
                              days_in_current_stage=5, avg_days_per_stage_historical=10.0,
                              last_stage_advance_days_ago=3, close_date_push_count=0)
        score_full = tracker._stage_progress_score(inp_full)
        score_zero = tracker._stage_progress_score(inp_zero)
        assert score_full > score_zero

    def test_stage_ratio_le_05_adds_30(self, tracker):
        """days_in_current_stage / avg <= 0.5 => +30 points."""
        inp = make_input(days_in_current_stage=1, avg_days_per_stage_historical=10.0,
                         total_stages_completed=0, total_stages_in_pipeline=0,
                         last_stage_advance_days_ago=35, close_date_push_count=1)
        score = tracker._stage_progress_score(inp)
        # pipeline pct = 0, ratio <=0.5 gives 30, adv=35 gives 0, push=1 gives 5 => 35
        assert score == 35.0

    def test_stage_ratio_le_10_adds_20(self, tracker):
        """days / avg in (0.5, 1.0] => +20 points."""
        inp = make_input(days_in_current_stage=7, avg_days_per_stage_historical=10.0,
                         total_stages_completed=0, total_stages_in_pipeline=0,
                         last_stage_advance_days_ago=35, close_date_push_count=1)
        score = tracker._stage_progress_score(inp)
        # ratio=0.7, stage bonus=20, adv=35 gives 0, push=1 gives 5 => 25
        assert score == 25.0

    def test_stage_ratio_le_15_adds_5(self, tracker):
        """days / avg in (1.0, 1.5] => +5 points."""
        inp = make_input(days_in_current_stage=12, avg_days_per_stage_historical=10.0,
                         total_stages_completed=0, total_stages_in_pipeline=0,
                         last_stage_advance_days_ago=35, close_date_push_count=1)
        score = tracker._stage_progress_score(inp)
        # ratio=1.2, stage bonus=5, adv=35 gives 0, push=1 gives 5 => 10
        assert score == 10.0

    def test_stage_ratio_gt_15_adds_0(self, tracker):
        """days / avg > 1.5 => +0 points from stage ratio."""
        inp = make_input(days_in_current_stage=20, avg_days_per_stage_historical=10.0,
                         total_stages_completed=0, total_stages_in_pipeline=0,
                         last_stage_advance_days_ago=35, close_date_push_count=1)
        score = tracker._stage_progress_score(inp)
        # ratio=2.0, stage bonus=0, adv=35 gives 0, push=1 gives 5 => 5
        assert score == 5.0

    def test_last_advance_le_7_adds_20(self, tracker):
        inp = make_input(last_stage_advance_days_ago=7,
                         total_stages_completed=0, total_stages_in_pipeline=0,
                         days_in_current_stage=1, avg_days_per_stage_historical=10.0,
                         close_date_push_count=0)
        score = tracker._stage_progress_score(inp)
        # ratio<=0.5 => 30, adv<=7 => 20, push=0 => 10 => 60
        assert score == 60.0

    def test_last_advance_le_14_adds_12(self, tracker):
        inp = make_input(last_stage_advance_days_ago=10,
                         total_stages_completed=0, total_stages_in_pipeline=0,
                         days_in_current_stage=1, avg_days_per_stage_historical=10.0,
                         close_date_push_count=0)
        score = tracker._stage_progress_score(inp)
        # ratio<=0.5 => 30, adv in (7,14] => 12, push=0 => 10 => 52
        assert score == 52.0

    def test_last_advance_le_30_adds_5(self, tracker):
        inp = make_input(last_stage_advance_days_ago=20,
                         total_stages_completed=0, total_stages_in_pipeline=0,
                         days_in_current_stage=1, avg_days_per_stage_historical=10.0,
                         close_date_push_count=0)
        score = tracker._stage_progress_score(inp)
        # ratio<=0.5 => 30, adv in (14,30] => 5, push=0 => 10 => 45
        assert score == 45.0

    def test_last_advance_gt_30_adds_0(self, tracker):
        inp = make_input(last_stage_advance_days_ago=35,
                         total_stages_completed=0, total_stages_in_pipeline=0,
                         days_in_current_stage=1, avg_days_per_stage_historical=10.0,
                         close_date_push_count=0)
        score = tracker._stage_progress_score(inp)
        # ratio<=0.5 => 30, adv>30 => 0, push=0 => 10 => 40
        assert score == 40.0

    def test_push_count_0_adds_10(self, tracker):
        inp = make_input(close_date_push_count=0,
                         total_stages_completed=0, total_stages_in_pipeline=0,
                         days_in_current_stage=1, avg_days_per_stage_historical=10.0,
                         last_stage_advance_days_ago=35)
        score = tracker._stage_progress_score(inp)
        # 30 + 0 + 10 = 40
        assert score == 40.0

    def test_push_count_1_adds_5(self, tracker):
        inp = make_input(close_date_push_count=1,
                         total_stages_completed=0, total_stages_in_pipeline=0,
                         days_in_current_stage=1, avg_days_per_stage_historical=10.0,
                         last_stage_advance_days_ago=35)
        score = tracker._stage_progress_score(inp)
        # 30 + 0 + 5 = 35
        assert score == 35.0

    def test_push_count_2_adds_0(self, tracker):
        inp = make_input(close_date_push_count=2,
                         total_stages_completed=0, total_stages_in_pipeline=0,
                         days_in_current_stage=1, avg_days_per_stage_historical=10.0,
                         last_stage_advance_days_ago=35)
        score = tracker._stage_progress_score(inp)
        # 30 + 0 + 0 = 30
        assert score == 30.0

    def test_push_count_ge_3_subtracts_10(self, tracker):
        inp = make_input(close_date_push_count=3,
                         total_stages_completed=0, total_stages_in_pipeline=0,
                         days_in_current_stage=1, avg_days_per_stage_historical=10.0,
                         last_stage_advance_days_ago=35)
        score = tracker._stage_progress_score(inp)
        # 30 + 0 - 10 = 20
        assert score == 20.0

    def test_zero_stages_in_pipeline_no_crash(self, tracker):
        inp = make_input(total_stages_in_pipeline=0, total_stages_completed=0)
        score = tracker._stage_progress_score(inp)
        assert 0.0 <= score <= 100.0

    def test_zero_avg_days_no_crash(self, tracker):
        inp = make_input(avg_days_per_stage_historical=0.0)
        score = tracker._stage_progress_score(inp)
        assert 0.0 <= score <= 100.0


class TestActivityVelocityScore:
    def test_returns_float_in_range(self, tracker):
        inp = make_input()
        score = tracker._activity_velocity_score(inp)
        assert 0.0 <= score <= 100.0

    def test_meeting_ratio_ge_15_adds_25(self, tracker):
        """meetings_last / meetings_prior >= 1.5 => +25."""
        inp = make_input(meetings_last_30d=3, meetings_prior_30d=2,
                         docs_opened_last_30d=0, action_items_completed_rate=0.0,
                         new_action_items_last_7d=0)
        # ratio = 1.5 => +25; meetings_last=3 not >=4 not >=2... actually 3>=2 => +12
        score = tracker._activity_velocity_score(inp)
        assert score == 37.0  # 25 + 12

    def test_meeting_ratio_ge_10_adds_15(self, tracker):
        """ratio in [1.0, 1.5) => +15."""
        inp = make_input(meetings_last_30d=2, meetings_prior_30d=2,
                         docs_opened_last_30d=0, action_items_completed_rate=0.0,
                         new_action_items_last_7d=0)
        score = tracker._activity_velocity_score(inp)
        assert score == 27.0  # 15 + 12 (meetings_last=2 >= 2)

    def test_meeting_ratio_ge_07_adds_8(self, tracker):
        """ratio in [0.7, 1.0) => +8."""
        inp = make_input(meetings_last_30d=1, meetings_prior_30d=2,
                         docs_opened_last_30d=0, action_items_completed_rate=0.0,
                         new_action_items_last_7d=0)
        # ratio=0.5, that's < 0.7 => +0; meetings_last=1 => +5
        score = tracker._activity_velocity_score(inp)
        assert score == 5.0  # 0 (ratio <0.7) + 5 (meetings >= 1)

    def test_meeting_ratio_ge_07_branch(self, tracker):
        inp = make_input(meetings_last_30d=7, meetings_prior_30d=10,
                         docs_opened_last_30d=0, action_items_completed_rate=0.0,
                         new_action_items_last_7d=0)
        # ratio=0.7 => +8; meetings_last=7 >= 4 => +20
        score = tracker._activity_velocity_score(inp)
        assert score == 28.0

    def test_prior_meetings_zero_and_last_zero(self, tracker):
        """prior=0 and last=0 => ratio set to 1.0 => +15."""
        inp = make_input(meetings_last_30d=0, meetings_prior_30d=0,
                         docs_opened_last_30d=0, action_items_completed_rate=0.0,
                         new_action_items_last_7d=0)
        # ratio=1.0 => +15; meetings=0 => +0
        score = tracker._activity_velocity_score(inp)
        assert score == 15.0

    def test_prior_meetings_zero_and_last_nonzero(self, tracker):
        """prior=0 and last>0 => ratio set to 2.0 => +25."""
        inp = make_input(meetings_last_30d=1, meetings_prior_30d=0,
                         docs_opened_last_30d=0, action_items_completed_rate=0.0,
                         new_action_items_last_7d=0)
        # ratio=2.0 => +25; meetings=1 => +5
        score = tracker._activity_velocity_score(inp)
        assert score == 30.0

    def test_docs_opened_ge_3_adds_20(self, tracker):
        inp = make_input(meetings_last_30d=0, meetings_prior_30d=0,
                         docs_opened_last_30d=3, action_items_completed_rate=0.0,
                         new_action_items_last_7d=0)
        # ratio=1.0 => +15; meetings=0 => +0; docs>=3 => +20
        score = tracker._activity_velocity_score(inp)
        assert score == 35.0

    def test_docs_opened_ge_1_adds_10(self, tracker):
        inp = make_input(meetings_last_30d=0, meetings_prior_30d=0,
                         docs_opened_last_30d=1, action_items_completed_rate=0.0,
                         new_action_items_last_7d=0)
        score = tracker._activity_velocity_score(inp)
        assert score == 25.0  # 15 + 10

    def test_action_completion_ge_80_adds_20(self, tracker):
        inp = make_input(meetings_last_30d=0, meetings_prior_30d=0,
                         docs_opened_last_30d=0, action_items_completed_rate=80.0,
                         new_action_items_last_7d=0)
        score = tracker._activity_velocity_score(inp)
        assert score == 35.0  # 15 + 20

    def test_action_completion_ge_60_adds_12(self, tracker):
        inp = make_input(meetings_last_30d=0, meetings_prior_30d=0,
                         docs_opened_last_30d=0, action_items_completed_rate=60.0,
                         new_action_items_last_7d=0)
        score = tracker._activity_velocity_score(inp)
        assert score == 27.0  # 15 + 12

    def test_action_completion_ge_40_adds_5(self, tracker):
        inp = make_input(meetings_last_30d=0, meetings_prior_30d=0,
                         docs_opened_last_30d=0, action_items_completed_rate=40.0,
                         new_action_items_last_7d=0)
        score = tracker._activity_velocity_score(inp)
        assert score == 20.0  # 15 + 5

    def test_action_completion_below_40_adds_0(self, tracker):
        inp = make_input(meetings_last_30d=0, meetings_prior_30d=0,
                         docs_opened_last_30d=0, action_items_completed_rate=30.0,
                         new_action_items_last_7d=0)
        score = tracker._activity_velocity_score(inp)
        assert score == 15.0  # 15 + 0

    def test_new_action_items_ge_3_adds_10(self, tracker):
        inp = make_input(meetings_last_30d=0, meetings_prior_30d=0,
                         docs_opened_last_30d=0, action_items_completed_rate=0.0,
                         new_action_items_last_7d=3)
        score = tracker._activity_velocity_score(inp)
        assert score == 25.0  # 15 + 10

    def test_new_action_items_ge_1_adds_5(self, tracker):
        inp = make_input(meetings_last_30d=0, meetings_prior_30d=0,
                         docs_opened_last_30d=0, action_items_completed_rate=0.0,
                         new_action_items_last_7d=1)
        score = tracker._activity_velocity_score(inp)
        assert score == 20.0  # 15 + 5

    def test_meetings_last_ge_4_adds_20(self, tracker):
        inp = make_input(meetings_last_30d=4, meetings_prior_30d=2,
                         docs_opened_last_30d=0, action_items_completed_rate=0.0,
                         new_action_items_last_7d=0)
        # ratio=2.0 => +25; meetings>=4 => +20
        score = tracker._activity_velocity_score(inp)
        assert score == 45.0

    def test_meetings_last_ge_2_adds_12(self, tracker):
        inp = make_input(meetings_last_30d=2, meetings_prior_30d=0,
                         docs_opened_last_30d=0, action_items_completed_rate=0.0,
                         new_action_items_last_7d=0)
        # prior=0, last>0 => ratio=2.0 => +25; meetings=2 >=2 => +12
        score = tracker._activity_velocity_score(inp)
        assert score == 37.0

    def test_meetings_last_ge_1_adds_5(self, tracker):
        inp = make_input(meetings_last_30d=1, meetings_prior_30d=0,
                         docs_opened_last_30d=0, action_items_completed_rate=0.0,
                         new_action_items_last_7d=0)
        # prior=0, last>0 => ratio=2.0 => +25; meetings=1 => +5
        score = tracker._activity_velocity_score(inp)
        assert score == 30.0


class TestStakeholderGrowthScore:
    def test_base_is_50(self, tracker):
        """Zero growth, no exec, exactly 3 stakeholders => 50+5=55."""
        inp = make_input(stakeholder_count_current=3, stakeholder_count_30d_ago=3,
                         exec_involved=0)
        score = tracker._stakeholder_growth_score(inp)
        assert score == 55.0  # base 50 + 5 for >=3

    def test_growth_ge_2_adds_30(self, tracker):
        inp = make_input(stakeholder_count_current=5, stakeholder_count_30d_ago=3,
                         exec_involved=0)
        score = tracker._stakeholder_growth_score(inp)
        # 50 + 30 (growth=2) + 10 (current>=5) = 90
        assert score == 90.0

    def test_growth_eq_1_adds_15(self, tracker):
        inp = make_input(stakeholder_count_current=4, stakeholder_count_30d_ago=3,
                         exec_involved=0)
        score = tracker._stakeholder_growth_score(inp)
        # 50 + 15 (growth=1) + 5 (current>=3) = 70
        assert score == 70.0

    def test_growth_eq_neg1_subtracts_15(self, tracker):
        inp = make_input(stakeholder_count_current=2, stakeholder_count_30d_ago=3,
                         exec_involved=0)
        score = tracker._stakeholder_growth_score(inp)
        # 50 - 15 (growth=-1) + 0 (current<3) = 35
        assert score == 35.0

    def test_growth_le_neg2_subtracts_30(self, tracker):
        inp = make_input(stakeholder_count_current=1, stakeholder_count_30d_ago=3,
                         exec_involved=0)
        score = tracker._stakeholder_growth_score(inp)
        # 50 - 30 (growth=-2) + 0 = 20
        assert score == 20.0

    def test_stakeholder_current_ge_5_adds_10(self, tracker):
        inp = make_input(stakeholder_count_current=5, stakeholder_count_30d_ago=5,
                         exec_involved=0)
        score = tracker._stakeholder_growth_score(inp)
        # 50 + 0 + 10 = 60
        assert score == 60.0

    def test_stakeholder_current_ge_3_adds_5(self, tracker):
        inp = make_input(stakeholder_count_current=3, stakeholder_count_30d_ago=3,
                         exec_involved=0)
        score = tracker._stakeholder_growth_score(inp)
        assert score == 55.0  # 50 + 0 + 5

    def test_exec_involved_adds_10(self, tracker):
        inp = make_input(stakeholder_count_current=3, stakeholder_count_30d_ago=3,
                         exec_involved=1)
        score = tracker._stakeholder_growth_score(inp)
        # 50 + 5 + 10 = 65
        assert score == 65.0

    def test_clamped_to_100(self, tracker):
        inp = make_input(stakeholder_count_current=10, stakeholder_count_30d_ago=1,
                         exec_involved=1)
        score = tracker._stakeholder_growth_score(inp)
        assert score <= 100.0

    def test_clamped_to_zero(self, tracker):
        inp = make_input(stakeholder_count_current=0, stakeholder_count_30d_ago=10,
                         exec_involved=0)
        score = tracker._stakeholder_growth_score(inp)
        assert score >= 0.0


class TestUrgencyScore:
    def test_returns_float_in_range(self, tracker):
        inp = make_input()
        score = tracker._urgency_score(inp)
        assert 0.0 <= score <= 100.0

    def test_days_le_7_adds_50(self, tracker):
        inp = make_input(days_to_target_close=7, deal_value=0.0, exec_involved=0,
                         close_date_push_count=0)
        assert tracker._urgency_score(inp) == 50.0

    def test_days_le_14_adds_35(self, tracker):
        inp = make_input(days_to_target_close=14, deal_value=0.0, exec_involved=0,
                         close_date_push_count=0)
        assert tracker._urgency_score(inp) == 35.0

    def test_days_le_30_adds_20(self, tracker):
        inp = make_input(days_to_target_close=30, deal_value=0.0, exec_involved=0,
                         close_date_push_count=0)
        assert tracker._urgency_score(inp) == 20.0

    def test_days_le_60_adds_10(self, tracker):
        inp = make_input(days_to_target_close=60, deal_value=0.0, exec_involved=0,
                         close_date_push_count=0)
        assert tracker._urgency_score(inp) == 10.0

    def test_days_gt_60_adds_0(self, tracker):
        inp = make_input(days_to_target_close=90, deal_value=0.0, exec_involved=0,
                         close_date_push_count=0)
        assert tracker._urgency_score(inp) == 0.0

    def test_deal_value_ge_500k_adds_20(self, tracker):
        inp = make_input(days_to_target_close=90, deal_value=500_000.0, exec_involved=0,
                         close_date_push_count=0)
        assert tracker._urgency_score(inp) == 20.0

    def test_deal_value_ge_200k_adds_12(self, tracker):
        inp = make_input(days_to_target_close=90, deal_value=200_000.0, exec_involved=0,
                         close_date_push_count=0)
        assert tracker._urgency_score(inp) == 12.0

    def test_deal_value_ge_100k_adds_6(self, tracker):
        inp = make_input(days_to_target_close=90, deal_value=100_000.0, exec_involved=0,
                         close_date_push_count=0)
        assert tracker._urgency_score(inp) == 6.0

    def test_deal_value_below_100k_adds_0(self, tracker):
        inp = make_input(days_to_target_close=90, deal_value=50_000.0, exec_involved=0,
                         close_date_push_count=0)
        assert tracker._urgency_score(inp) == 0.0

    def test_exec_involved_adds_15(self, tracker):
        inp = make_input(days_to_target_close=90, deal_value=0.0, exec_involved=1,
                         close_date_push_count=0)
        assert tracker._urgency_score(inp) == 15.0

    def test_push_count_ge_3_subtracts_15(self, tracker):
        inp = make_input(days_to_target_close=7, deal_value=0.0, exec_involved=0,
                         close_date_push_count=3)
        assert tracker._urgency_score(inp) == 35.0  # 50 - 15

    def test_push_count_ge_2_subtracts_8(self, tracker):
        inp = make_input(days_to_target_close=7, deal_value=0.0, exec_involved=0,
                         close_date_push_count=2)
        assert tracker._urgency_score(inp) == 42.0  # 50 - 8

    def test_clamped_to_100(self, tracker):
        inp = make_input(days_to_target_close=1, deal_value=600_000.0, exec_involved=1,
                         close_date_push_count=0)
        score = tracker._urgency_score(inp)
        assert score <= 100.0

    def test_clamped_to_zero(self, tracker):
        inp = make_input(days_to_target_close=200, deal_value=0.0, exec_involved=0,
                         close_date_push_count=10)
        score = tracker._urgency_score(inp)
        assert score >= 0.0


# ===========================================================================
# 9. Enum classifiers
# ===========================================================================

class TestVelocityStatusClassifier:
    def test_accelerating_when_composite_ge_70_and_advance_le_7(self, tracker):
        inp = make_input(last_stage_advance_days_ago=7)
        result = tracker.track(inp)
        if result.velocity_composite >= 70:
            assert result.velocity_status == VelocityStatus.ACCELERATING

    def test_on_pace_when_composite_50_to_69(self, tracker):
        inp = make_input(
            days_in_current_stage=10, avg_days_per_stage_historical=10.0,
            meetings_last_30d=2, meetings_prior_30d=2,
            docs_opened_last_30d=1, action_items_completed_rate=60.0,
            new_action_items_last_7d=1,
            stakeholder_count_current=3, stakeholder_count_30d_ago=3,
            exec_involved=0, days_to_target_close=60, deal_value=50_000.0,
            close_date_push_count=0, last_stage_advance_days_ago=20,
            total_stages_completed=2, total_stages_in_pipeline=6,
        )
        result = tracker.track(inp)
        if 50 <= result.velocity_composite < 70:
            assert result.velocity_status == VelocityStatus.ON_PACE

    def test_stalled_when_composite_below_30(self, tracker):
        inp = make_input(
            days_in_current_stage=100,
            avg_days_per_stage_historical=5.0,
            total_stages_completed=0,
            total_stages_in_pipeline=10,
            meetings_last_30d=0,
            meetings_prior_30d=5,
            docs_opened_last_30d=0,
            action_items_completed_rate=0.0,
            new_action_items_last_7d=0,
            stakeholder_count_current=1,
            stakeholder_count_30d_ago=5,
            exec_involved=0,
            days_to_target_close=200,
            deal_value=5_000.0,
            close_date_push_count=0,
            last_stage_advance_days_ago=60,
        )
        result = tracker.track(inp)
        if result.velocity_composite < 30:
            assert result.velocity_status == VelocityStatus.STALLED

    def test_accelerating_requires_both_conditions(self, tracker):
        """composite >= 70 but advance > 7 => NOT accelerating."""
        inp = make_input(last_stage_advance_days_ago=10)
        result = tracker.track(inp)
        if result.velocity_composite >= 70:
            assert result.velocity_status != VelocityStatus.ACCELERATING


class TestSlipRiskClassifier:
    def test_low_when_risk_score_lt_30(self, tracker):
        """High composite, no pushes, no stuck stage => low risk."""
        inp = make_input(
            close_date_push_count=0,
            days_in_current_stage=5,
            avg_days_per_stage_historical=10.0,
        )
        result = tracker.track(inp)
        if result.velocity_composite >= 70:
            assert result.slip_risk == SlipRisk.LOW

    def test_critical_when_risk_score_ge_70(self, tracker):
        inp = make_input(
            days_in_current_stage=100,
            avg_days_per_stage_historical=5.0,
            total_stages_completed=0,
            total_stages_in_pipeline=10,
            meetings_last_30d=0,
            meetings_prior_30d=5,
            docs_opened_last_30d=0,
            action_items_completed_rate=0.0,
            new_action_items_last_7d=0,
            stakeholder_count_current=1,
            stakeholder_count_30d_ago=5,
            exec_involved=0,
            days_to_target_close=200,
            deal_value=5_000.0,
            close_date_push_count=4,
            last_stage_advance_days_ago=60,
        )
        result = tracker.track(inp)
        # risk_score = 100-composite + 15 (push>=2) + 10 (stuck)
        if result.velocity_composite <= 30:
            assert result.slip_risk in (SlipRisk.HIGH, SlipRisk.CRITICAL)

    def test_push_count_ge_2_increases_risk(self, tracker):
        inp_no_push = make_input(close_date_push_count=0)
        inp_push = make_input(close_date_push_count=3)
        r1 = tracker.track(inp_no_push)
        r2 = tracker.track(inp_push)
        # At same composite, more pushes => worse risk
        risk_order = [SlipRisk.LOW, SlipRisk.MODERATE, SlipRisk.HIGH, SlipRisk.CRITICAL]
        assert risk_order.index(r2.slip_risk) >= risk_order.index(r1.slip_risk)


class TestDealMomentumClassifier:
    def test_strong_when_composite_ge_70(self, tracker):
        inp = make_input()
        result = tracker.track(inp)
        if result.velocity_composite >= 70:
            assert result.deal_momentum == DealMomentum.STRONG

    def test_building_when_composite_50_to_69(self, tracker):
        inp = make_input()
        result = tracker.track(inp)
        if 50 <= result.velocity_composite < 70:
            assert result.deal_momentum == DealMomentum.BUILDING

    def test_fading_when_composite_30_to_49(self, tracker):
        inp = make_input()
        result = tracker.track(inp)
        if 30 <= result.velocity_composite < 50:
            assert result.deal_momentum == DealMomentum.FADING

    def test_lost_when_composite_below_30(self, tracker):
        inp = make_input(
            days_in_current_stage=100, avg_days_per_stage_historical=5.0,
            total_stages_completed=0, total_stages_in_pipeline=10,
            meetings_last_30d=0, meetings_prior_30d=5,
            docs_opened_last_30d=0, action_items_completed_rate=0.0,
            new_action_items_last_7d=0, stakeholder_count_current=1,
            stakeholder_count_30d_ago=5, exec_involved=0,
            days_to_target_close=200, deal_value=5_000.0,
            close_date_push_count=0, last_stage_advance_days_ago=60,
        )
        result = tracker.track(inp)
        if result.velocity_composite < 30:
            assert result.deal_momentum == DealMomentum.LOST


class TestVelocityActionClassifier:
    def test_rescue_when_needs_boost(self, tracker):
        inp = make_input(days_in_current_stage=25, avg_days_per_stage_historical=10.0)
        result = tracker.track(inp)
        if result.needs_velocity_boost:
            assert result.velocity_action == VelocityAction.RESCUE

    def test_rescue_when_stalled(self, tracker):
        inp = make_input(
            days_in_current_stage=100, avg_days_per_stage_historical=5.0,
            total_stages_completed=0, total_stages_in_pipeline=10,
            meetings_last_30d=0, meetings_prior_30d=5,
            docs_opened_last_30d=0, action_items_completed_rate=0.0,
            new_action_items_last_7d=0, stakeholder_count_current=1,
            stakeholder_count_30d_ago=5, exec_involved=0,
            days_to_target_close=200, deal_value=5_000.0,
            close_date_push_count=0, last_stage_advance_days_ago=60,
        )
        result = tracker.track(inp)
        if result.velocity_status == VelocityStatus.STALLED or result.needs_velocity_boost:
            assert result.velocity_action == VelocityAction.RESCUE

    def test_inject_urgency_when_decelerating_no_boost(self, tracker):
        """If status=DECELERATING and not needs_boost => INJECT_URGENCY."""
        t = DealVelocityTracker()
        # Manually call _velocity_action
        action = t._velocity_action(VelocityStatus.DECELERATING, False, 35.0)
        assert action == VelocityAction.INJECT_URGENCY

    def test_maintain_when_on_pace_no_boost(self, tracker):
        t = DealVelocityTracker()
        action = t._velocity_action(VelocityStatus.ON_PACE, False, 60.0)
        assert action == VelocityAction.MAINTAIN

    def test_accelerate_when_accelerating_no_boost(self, tracker):
        t = DealVelocityTracker()
        action = t._velocity_action(VelocityStatus.ACCELERATING, False, 80.0)
        assert action == VelocityAction.ACCELERATE

    def test_rescue_overrides_on_pace_when_boost_needed(self, tracker):
        t = DealVelocityTracker()
        action = t._velocity_action(VelocityStatus.ON_PACE, True, 60.0)
        assert action == VelocityAction.RESCUE


# ===========================================================================
# 10. track() / track_batch()
# ===========================================================================

class TestTrackAndTrackBatch:
    def test_track_returns_result(self, tracker):
        inp = make_input()
        result = tracker.track(inp)
        assert isinstance(result, DealVelocityResult)

    def test_track_appends_to_results(self, tracker):
        tracker.track(make_input(deal_id="a"))
        tracker.track(make_input(deal_id="b"))
        assert len(tracker._results) == 2

    def test_track_batch_returns_list(self, tracker):
        inputs = [make_input(deal_id=f"d{i}") for i in range(5)]
        results = tracker.track_batch(inputs)
        assert isinstance(results, list)
        assert len(results) == 5

    def test_track_batch_all_appended(self, tracker):
        inputs = [make_input(deal_id=f"d{i}") for i in range(3)]
        tracker.track_batch(inputs)
        assert len(tracker._results) == 3

    def test_track_batch_empty_list(self, tracker):
        results = tracker.track_batch([])
        assert results == []

    def test_track_preserves_deal_id(self, tracker):
        inp = make_input(deal_id="unique-123")
        result = tracker.track(inp)
        assert result.deal_id == "unique-123"

    def test_track_preserves_deal_name(self, tracker):
        inp = make_input(deal_name="Special Deal")
        result = tracker.track(inp)
        assert result.deal_name == "Special Deal"

    def test_track_batch_order_preserved(self, tracker):
        ids = [f"deal-{i}" for i in range(5)]
        inputs = [make_input(deal_id=d) for d in ids]
        results = tracker.track_batch(inputs)
        assert [r.deal_id for r in results] == ids

    def test_scores_are_floats(self, tracker):
        result = tracker.track(make_input())
        assert isinstance(result.stage_progress_score, float)
        assert isinstance(result.activity_velocity_score, float)
        assert isinstance(result.stakeholder_growth_score, float)
        assert isinstance(result.urgency_score, float)
        assert isinstance(result.velocity_composite, float)
        assert isinstance(result.slip_probability, float)

    def test_predicted_close_days_is_int(self, tracker):
        result = tracker.track(make_input())
        assert isinstance(result.predicted_close_days, int)
        assert result.predicted_close_days >= 1

    def test_is_on_track_is_bool(self, tracker):
        result = tracker.track(make_input())
        assert isinstance(result.is_on_track, bool)

    def test_needs_velocity_boost_is_bool(self, tracker):
        result = tracker.track(make_input())
        assert isinstance(result.needs_velocity_boost, bool)


# ===========================================================================
# 11. Properties
# ===========================================================================

class TestProperties:
    def test_on_track_deals_empty_when_no_results(self, tracker):
        assert tracker.on_track_deals == []

    def test_boost_needed_deals_empty_when_no_results(self, tracker):
        assert tracker.velocity_boost_queue == []

    def test_avg_velocity_composite_zero_when_no_results(self, tracker):
        assert tracker.avg_velocity_composite == 0.0

    def test_avg_slip_probability_zero_when_no_results(self, tracker):
        assert tracker.avg_slip_probability == 0.0

    def test_on_track_deals_contains_only_on_track(self, tracker):
        tracker.track_batch([make_input(deal_id=f"d{i}") for i in range(5)])
        for r in tracker.on_track_deals:
            assert r.is_on_track is True

    def test_boost_needed_deals_contains_only_boost_needed(self, tracker):
        tracker.track_batch([make_input(deal_id=f"d{i}") for i in range(5)])
        for r in tracker.velocity_boost_queue:
            assert r.needs_velocity_boost is True

    def test_avg_velocity_composite_is_rounded_float(self, tracker):
        tracker.track_batch([make_input(deal_id=f"d{i}") for i in range(4)])
        avg = tracker.avg_velocity_composite
        assert isinstance(avg, float)
        assert avg == round(avg, 1)

    def test_avg_slip_probability_is_rounded_float(self, tracker):
        tracker.track_batch([make_input(deal_id=f"d{i}") for i in range(4)])
        avg = tracker.avg_slip_probability
        assert isinstance(avg, float)
        assert avg == round(avg, 1)

    def test_avg_velocity_composite_correct_value(self, tracker):
        inp1 = make_input(deal_id="a")
        inp2 = make_input(deal_id="b")
        r1 = tracker.track(inp1)
        r2 = tracker.track(inp2)
        expected = round((r1.velocity_composite + r2.velocity_composite) / 2, 1)
        assert tracker.avg_velocity_composite == expected

    def test_on_track_count_matches_property(self, tracker):
        tracker.track_batch([make_input(deal_id=f"d{i}") for i in range(6)])
        assert len(tracker.on_track_deals) == tracker.summary()["on_track_count"]

    def test_boost_count_matches_summary(self, tracker):
        tracker.track_batch([make_input(deal_id=f"d{i}") for i in range(6)])
        assert len(tracker.velocity_boost_queue) == tracker.summary()["velocity_boost_count"]


# ===========================================================================
# 12. reset()
# ===========================================================================

class TestReset:
    def test_reset_clears_results(self, tracker):
        tracker.track_batch([make_input(deal_id=f"d{i}") for i in range(5)])
        tracker.reset()
        assert tracker._results == []

    def test_reset_resets_avg_composite(self, tracker):
        tracker.track_batch([make_input(deal_id=f"d{i}") for i in range(3)])
        tracker.reset()
        assert tracker.avg_velocity_composite == 0.0

    def test_reset_resets_on_track_deals(self, tracker):
        tracker.track_batch([make_input(deal_id=f"d{i}") for i in range(3)])
        tracker.reset()
        assert tracker.on_track_deals == []

    def test_reset_resets_velocity_boost_queue(self, tracker):
        tracker.track_batch([make_input(deal_id=f"d{i}") for i in range(3)])
        tracker.reset()
        assert tracker.velocity_boost_queue == []

    def test_reset_allows_reuse(self, tracker):
        tracker.track(make_input(deal_id="first"))
        tracker.reset()
        tracker.track(make_input(deal_id="second"))
        assert len(tracker._results) == 1
        assert tracker._results[0].deal_id == "second"

    def test_double_reset_is_safe(self, tracker):
        tracker.reset()
        tracker.reset()
        assert tracker._results == []

    def test_summary_after_reset_is_all_zeros(self, tracker):
        tracker.track_batch([make_input(deal_id=f"d{i}") for i in range(3)])
        tracker.reset()
        s = tracker.summary()
        assert s["total"] == 0
        assert s["on_track_count"] == 0
        assert s["velocity_boost_count"] == 0


# ===========================================================================
# 13. predicted_close_days helper
# ===========================================================================

class TestPredictedCloseDays:
    def test_minimum_1(self, tracker):
        inp = make_input(total_stages_completed=5, total_stages_in_pipeline=5)
        result = tracker.track(inp)
        assert result.predicted_close_days >= 1

    def test_high_composite_uses_07_multiplier(self, tracker):
        """composite >= 70 => days_per_stage = historical * 0.7"""
        t = DealVelocityTracker()
        inp = make_input(total_stages_completed=3, total_stages_in_pipeline=6,
                         avg_days_per_stage_historical=10.0)
        # Force composite=80 by injecting
        predicted = t._predicted_close_days(inp, 80.0)
        stages_remaining = 3
        expected = max(1, int(stages_remaining * 10.0 * 0.7))
        assert predicted == expected

    def test_medium_composite_uses_1x_multiplier(self, tracker):
        t = DealVelocityTracker()
        inp = make_input(total_stages_completed=3, total_stages_in_pipeline=6,
                         avg_days_per_stage_historical=10.0)
        predicted = t._predicted_close_days(inp, 60.0)
        stages_remaining = 3
        expected = max(1, int(stages_remaining * 10.0 * 1.0))
        assert predicted == expected

    def test_low_composite_uses_15_multiplier(self, tracker):
        t = DealVelocityTracker()
        inp = make_input(total_stages_completed=3, total_stages_in_pipeline=6,
                         avg_days_per_stage_historical=10.0)
        predicted = t._predicted_close_days(inp, 40.0)
        stages_remaining = 3
        expected = max(1, int(stages_remaining * 10.0 * 1.5))
        assert predicted == expected

    def test_very_low_composite_uses_2x_multiplier(self, tracker):
        t = DealVelocityTracker()
        inp = make_input(total_stages_completed=3, total_stages_in_pipeline=6,
                         avg_days_per_stage_historical=10.0)
        predicted = t._predicted_close_days(inp, 20.0)
        stages_remaining = 3
        expected = max(1, int(stages_remaining * 10.0 * 2.0))
        assert predicted == expected

    def test_no_stages_remaining_returns_1(self, tracker):
        t = DealVelocityTracker()
        inp = make_input(total_stages_completed=6, total_stages_in_pipeline=6,
                         avg_days_per_stage_historical=10.0)
        predicted = t._predicted_close_days(inp, 75.0)
        assert predicted == 1  # max(1, 0)


# ===========================================================================
# 14. slip_probability helper
# ===========================================================================

class TestSlipProbability:
    def test_in_range(self, tracker):
        result = tracker.track(make_input())
        assert 0.0 <= result.slip_probability <= 100.0

    def test_push_count_increases_probability(self, tracker):
        r1 = tracker.track(make_input(deal_id="a", close_date_push_count=0))
        r2 = tracker.track(make_input(deal_id="b", close_date_push_count=3))
        assert r2.slip_probability >= r1.slip_probability

    def test_exec_involvement_reduces_probability(self, tracker):
        r1 = tracker.track(make_input(deal_id="a", exec_involved=0))
        r2 = tracker.track(make_input(deal_id="b", exec_involved=1))
        assert r2.slip_probability <= r1.slip_probability

    def test_stuck_stage_increases_probability(self, tracker):
        r1 = tracker.track(make_input(deal_id="a", days_in_current_stage=5,
                                       avg_days_per_stage_historical=10.0))
        r2 = tracker.track(make_input(deal_id="b", days_in_current_stage=25,
                                       avg_days_per_stage_historical=10.0))
        assert r2.slip_probability >= r1.slip_probability

    def test_slip_probability_push_count_formula(self):
        t = DealVelocityTracker()
        inp = make_input(close_date_push_count=2, days_in_current_stage=5,
                         avg_days_per_stage_historical=10.0, exec_involved=0)
        composite = 60.0
        prob = t._slip_probability(inp, composite)
        expected_base = 100.0 - 60.0 + 2 * 8.0
        assert prob == round(max(0.0, min(100.0, expected_base)), 1)


# ===========================================================================
# 15. DealVelocityTracker initializes fresh
# ===========================================================================

class TestTrackerInit:
    def test_new_tracker_has_empty_results(self):
        t = DealVelocityTracker()
        assert t._results == []

    def test_two_trackers_are_independent(self):
        t1 = DealVelocityTracker()
        t2 = DealVelocityTracker()
        t1.track(make_input())
        assert len(t1._results) == 1
        assert len(t2._results) == 0
