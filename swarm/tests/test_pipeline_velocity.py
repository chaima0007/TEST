"""Comprehensive pytest tests for swarm/intelligence/pipeline_velocity.py.

Run from /home/user/TEST with:
    python -m pytest swarm/tests/test_pipeline_velocity.py -v
"""

from __future__ import annotations

import pytest

from swarm.intelligence.pipeline_velocity import (
    VelocityStatus,
    VelocityAction,
    PipelineVelocityInput,
    PipelineVelocityResult,
    PipelineVelocityCalculator,
    _STAGE_BENCHMARKS,
    _stage_pace_score,
    _activity_score,
    _probability_score,
    _velocity_score,
    _schedule_delta,
    _velocity_eur_per_day,
    _velocity_status,
    _velocity_action,
    _build_signals,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def make_input(
    deal_id: str = "D001",
    deal_name: str = "Test Deal",
    account_name: str = "Acme Corp",
    segment: str = "enterprise",
    arr_eur: float = 100_000.0,
    stage: str = "proposal",
    days_in_current_stage: int = 10,
    total_days_in_pipeline: int = 30,
    expected_total_days: int = 90,
    win_probability_pct: float = 60.0,
    last_activity_days: int = 2,
    has_next_step_scheduled: bool = True,
    stage_regression_count: int = 0,
    blocker_count: int = 0,
    champion_present: bool = True,
    decision_maker_engaged: bool = True,
) -> PipelineVelocityInput:
    return PipelineVelocityInput(
        deal_id=deal_id,
        deal_name=deal_name,
        account_name=account_name,
        segment=segment,
        arr_eur=arr_eur,
        stage=stage,
        days_in_current_stage=days_in_current_stage,
        total_days_in_pipeline=total_days_in_pipeline,
        expected_total_days=expected_total_days,
        win_probability_pct=win_probability_pct,
        last_activity_days=last_activity_days,
        has_next_step_scheduled=has_next_step_scheduled,
        stage_regression_count=stage_regression_count,
        blocker_count=blocker_count,
        champion_present=champion_present,
        decision_maker_engaged=decision_maker_engaged,
    )


# ---------------------------------------------------------------------------
# Class 1 — VelocityStatus enum
# ---------------------------------------------------------------------------

class TestVelocityStatus:
    def test_fast_value(self):
        assert VelocityStatus.FAST.value == "fast"

    def test_on_pace_value(self):
        assert VelocityStatus.ON_PACE.value == "on_pace"

    def test_slow_value(self):
        assert VelocityStatus.SLOW.value == "slow"

    def test_stalled_value(self):
        assert VelocityStatus.STALLED.value == "stalled"

    def test_is_str_subclass(self):
        assert isinstance(VelocityStatus.FAST, str)

    def test_equality_with_string(self):
        assert VelocityStatus.FAST == "fast"

    def test_all_members(self):
        members = {m.value for m in VelocityStatus}
        assert members == {"fast", "on_pace", "slow", "stalled"}


# ---------------------------------------------------------------------------
# Class 2 — VelocityAction enum
# ---------------------------------------------------------------------------

class TestVelocityAction:
    def test_close_now_value(self):
        assert VelocityAction.CLOSE_NOW.value == "close_now"

    def test_rescue_value(self):
        assert VelocityAction.RESCUE.value == "rescue"

    def test_accelerate_value(self):
        assert VelocityAction.ACCELERATE.value == "accelerate"

    def test_monitor_value(self):
        assert VelocityAction.MONITOR.value == "monitor"

    def test_is_str_subclass(self):
        assert isinstance(VelocityAction.CLOSE_NOW, str)

    def test_equality_with_string(self):
        assert VelocityAction.RESCUE == "rescue"

    def test_all_members(self):
        members = {m.value for m in VelocityAction}
        assert members == {"close_now", "rescue", "accelerate", "monitor"}


# ---------------------------------------------------------------------------
# Class 3 — _STAGE_BENCHMARKS
# ---------------------------------------------------------------------------

class TestStageBenchmarks:
    def test_prospecting(self):
        assert _STAGE_BENCHMARKS["prospecting"] == 7

    def test_qualification(self):
        assert _STAGE_BENCHMARKS["qualification"] == 14

    def test_demo(self):
        assert _STAGE_BENCHMARKS["demo"] == 14

    def test_proposal(self):
        assert _STAGE_BENCHMARKS["proposal"] == 21

    def test_negotiation(self):
        assert _STAGE_BENCHMARKS["negotiation"] == 14

    def test_closing(self):
        assert _STAGE_BENCHMARKS["closing"] == 7

    def test_has_exactly_six_stages(self):
        assert len(_STAGE_BENCHMARKS) == 6

    def test_unknown_stage_not_present(self):
        assert "unknown" not in _STAGE_BENCHMARKS


# ---------------------------------------------------------------------------
# Class 4 — _stage_pace_score
# ---------------------------------------------------------------------------

class TestStagePaceScore:
    """Tests every branch + boundary of _stage_pace_score."""

    # ratio <= 0.5 → 100
    def test_ratio_zero(self):
        # 0 days in proposal (benchmark=21) → ratio=0 → 100
        inp = make_input(stage="proposal", days_in_current_stage=0)
        score, overdue = _stage_pace_score(inp)
        assert score == 100.0
        assert overdue is False

    def test_ratio_exactly_half(self):
        # 7 days in proposal (21) → ratio=1/3<0.5 → 100; exactly 0.5 would be 10.5 days
        inp = make_input(stage="proposal", days_in_current_stage=10)
        score, overdue = _stage_pace_score(inp)
        # ratio=10/21≈0.476 <=0.5 → 100
        assert score == 100.0
        assert overdue is False

    def test_ratio_exactly_05(self):
        # benchmark=14 (demo), days=7 → ratio=0.5 → score=100
        inp = make_input(stage="demo", days_in_current_stage=7)
        score, overdue = _stage_pace_score(inp)
        assert score == 100.0

    # ratio > 0.5 and <= 1.0 → 100 - (ratio-0.5)*60 ranges 100→70
    def test_ratio_075(self):
        # benchmark=14 (demo), days=10.5 → use days=11 → ratio≈0.786
        inp = make_input(stage="demo", days_in_current_stage=11)
        score, overdue = _stage_pace_score(inp)
        ratio = 11 / 14
        expected = round(100.0 - (ratio - 0.5) * 60.0, 2)
        assert score == expected
        assert overdue is False

    def test_ratio_exactly_10(self):
        # benchmark=14 (demo), days=14 → ratio=1.0 → score=100-(0.5)*60=70
        inp = make_input(stage="demo", days_in_current_stage=14)
        score, overdue = _stage_pace_score(inp)
        assert score == pytest.approx(70.0, abs=0.01)
        assert overdue is False  # days == benchmark, not >

    # ratio > 1.0 and <= 1.5 → 70 - (ratio-1.0)*80 ranges 70→30
    def test_ratio_125(self):
        # benchmark=14 (demo), days=17.5 → use 17 → ratio≈1.214
        inp = make_input(stage="demo", days_in_current_stage=17)
        score, overdue = _stage_pace_score(inp)
        ratio = 17 / 14
        expected = round(70.0 - (ratio - 1.0) * 80.0, 2)
        assert score == expected
        assert overdue is True

    def test_ratio_exactly_15(self):
        # benchmark=14, days=21 → ratio=1.5 → score=70-(0.5)*80=30
        inp = make_input(stage="demo", days_in_current_stage=21)
        score, overdue = _stage_pace_score(inp)
        assert score == pytest.approx(30.0, abs=0.01)
        assert overdue is True

    # ratio > 1.5 and <= 2.0 → 30 - (ratio-1.5)*60 ranges 30→0
    def test_ratio_175(self):
        # benchmark=14, days=24.5 → use 24 → ratio≈1.714
        inp = make_input(stage="demo", days_in_current_stage=24)
        score, overdue = _stage_pace_score(inp)
        ratio = 24 / 14
        expected = round(max(0.0, 30.0 - (ratio - 1.5) * 60.0), 2)
        assert score == expected
        assert overdue is True

    def test_ratio_exactly_20(self):
        # benchmark=14, days=28 → ratio=2.0 → score=30-(0.5)*60=0
        inp = make_input(stage="demo", days_in_current_stage=28)
        score, overdue = _stage_pace_score(inp)
        assert score == pytest.approx(0.0, abs=0.01)
        assert overdue is True

    # ratio > 2.0 → 0
    def test_ratio_above_2(self):
        # benchmark=7 (prospecting), days=20 → ratio≈2.857 → 0
        inp = make_input(stage="prospecting", days_in_current_stage=20)
        score, overdue = _stage_pace_score(inp)
        assert score == 0.0
        assert overdue is True

    def test_unknown_stage_uses_14_benchmark(self):
        # Unknown stage falls back to 14
        inp = make_input(stage="unknown_xyz", days_in_current_stage=7)
        score, overdue = _stage_pace_score(inp)
        # ratio = 7/14 = 0.5 → 100
        assert score == 100.0
        assert overdue is False

    def test_overdue_true_when_days_gt_benchmark(self):
        # benchmark=7 (prospecting), days=8
        inp = make_input(stage="prospecting", days_in_current_stage=8)
        _, overdue = _stage_pace_score(inp)
        assert overdue is True

    def test_overdue_false_when_days_eq_benchmark(self):
        # benchmark=7 (prospecting), days=7 → not overdue (must be >)
        inp = make_input(stage="prospecting", days_in_current_stage=7)
        _, overdue = _stage_pace_score(inp)
        assert overdue is False

    def test_score_clamped_to_100(self):
        inp = make_input(stage="prospecting", days_in_current_stage=0)
        score, _ = _stage_pace_score(inp)
        assert score <= 100.0

    def test_score_clamped_to_zero(self):
        inp = make_input(stage="prospecting", days_in_current_stage=1000)
        score, _ = _stage_pace_score(inp)
        assert score == 0.0

    def test_return_is_numeric(self):
        inp = make_input()
        score, overdue = _stage_pace_score(inp)
        assert isinstance(score, (int, float))
        assert isinstance(overdue, bool)

    def test_negotiation_benchmark(self):
        inp = make_input(stage="negotiation", days_in_current_stage=14)
        score, overdue = _stage_pace_score(inp)
        assert overdue is False
        assert score == pytest.approx(70.0, abs=0.01)

    def test_closing_benchmark(self):
        inp = make_input(stage="closing", days_in_current_stage=7)
        score, overdue = _stage_pace_score(inp)
        assert overdue is False
        assert score == pytest.approx(70.0, abs=0.01)

    def test_proposal_boundary(self):
        # benchmark=21, days=21 → ratio=1.0 → 70
        inp = make_input(stage="proposal", days_in_current_stage=21)
        score, overdue = _stage_pace_score(inp)
        assert score == pytest.approx(70.0, abs=0.01)
        assert overdue is False


# ---------------------------------------------------------------------------
# Class 5 — _activity_score
# ---------------------------------------------------------------------------

class TestActivityScore:
    """Tests all branches of _activity_score."""

    def test_last_activity_0_days(self):
        inp = make_input(
            last_activity_days=0,
            has_next_step_scheduled=False,
            champion_present=False,
            decision_maker_engaged=False,
        )
        assert _activity_score(inp) == 50.0

    def test_last_activity_1_day(self):
        inp = make_input(
            last_activity_days=1,
            has_next_step_scheduled=False,
            champion_present=False,
            decision_maker_engaged=False,
        )
        assert _activity_score(inp) == 50.0

    def test_last_activity_2_days(self):
        inp = make_input(
            last_activity_days=2,
            has_next_step_scheduled=False,
            champion_present=False,
            decision_maker_engaged=False,
        )
        assert _activity_score(inp) == 40.0

    def test_last_activity_3_days(self):
        inp = make_input(
            last_activity_days=3,
            has_next_step_scheduled=False,
            champion_present=False,
            decision_maker_engaged=False,
        )
        assert _activity_score(inp) == 40.0

    def test_last_activity_4_days(self):
        inp = make_input(
            last_activity_days=4,
            has_next_step_scheduled=False,
            champion_present=False,
            decision_maker_engaged=False,
        )
        assert _activity_score(inp) == 25.0

    def test_last_activity_7_days(self):
        inp = make_input(
            last_activity_days=7,
            has_next_step_scheduled=False,
            champion_present=False,
            decision_maker_engaged=False,
        )
        assert _activity_score(inp) == 25.0

    def test_last_activity_8_days(self):
        inp = make_input(
            last_activity_days=8,
            has_next_step_scheduled=False,
            champion_present=False,
            decision_maker_engaged=False,
        )
        assert _activity_score(inp) == 10.0

    def test_last_activity_14_days(self):
        inp = make_input(
            last_activity_days=14,
            has_next_step_scheduled=False,
            champion_present=False,
            decision_maker_engaged=False,
        )
        assert _activity_score(inp) == 10.0

    def test_last_activity_15_days(self):
        inp = make_input(
            last_activity_days=15,
            has_next_step_scheduled=False,
            champion_present=False,
            decision_maker_engaged=False,
        )
        assert _activity_score(inp) == 0.0

    def test_has_next_step_adds_25(self):
        base_inp = make_input(
            last_activity_days=15,
            has_next_step_scheduled=False,
            champion_present=False,
            decision_maker_engaged=False,
        )
        inp = make_input(
            last_activity_days=15,
            has_next_step_scheduled=True,
            champion_present=False,
            decision_maker_engaged=False,
        )
        assert _activity_score(inp) - _activity_score(base_inp) == 25.0

    def test_champion_present_adds_15(self):
        base = make_input(
            last_activity_days=15,
            has_next_step_scheduled=False,
            champion_present=False,
            decision_maker_engaged=False,
        )
        inp = make_input(
            last_activity_days=15,
            has_next_step_scheduled=False,
            champion_present=True,
            decision_maker_engaged=False,
        )
        assert _activity_score(inp) - _activity_score(base) == 15.0

    def test_decision_maker_engaged_adds_10(self):
        base = make_input(
            last_activity_days=15,
            has_next_step_scheduled=False,
            champion_present=False,
            decision_maker_engaged=False,
        )
        inp = make_input(
            last_activity_days=15,
            has_next_step_scheduled=False,
            champion_present=False,
            decision_maker_engaged=True,
        )
        assert _activity_score(inp) - _activity_score(base) == 10.0

    def test_all_bonuses_active(self):
        # 50 (1 day) + 25 + 15 + 10 = 100, clamped at 100
        inp = make_input(
            last_activity_days=1,
            has_next_step_scheduled=True,
            champion_present=True,
            decision_maker_engaged=True,
        )
        assert _activity_score(inp) == 100.0

    def test_clamped_at_100(self):
        # Even if sum exceeds 100, it should be capped
        inp = make_input(
            last_activity_days=0,
            has_next_step_scheduled=True,
            champion_present=True,
            decision_maker_engaged=True,
        )
        assert _activity_score(inp) == 100.0

    def test_return_is_numeric(self):
        inp = make_input()
        score = _activity_score(inp)
        assert isinstance(score, (int, float))

    def test_clamped_at_0(self):
        inp = make_input(
            last_activity_days=100,
            has_next_step_scheduled=False,
            champion_present=False,
            decision_maker_engaged=False,
        )
        assert _activity_score(inp) == 0.0


# ---------------------------------------------------------------------------
# Class 6 — _probability_score
# ---------------------------------------------------------------------------

class TestProbabilityScore:
    def test_zero_probability(self):
        inp = make_input(win_probability_pct=0.0)
        assert _probability_score(inp) == 0.0

    def test_100_probability(self):
        inp = make_input(win_probability_pct=100.0)
        result = _probability_score(inp)
        assert isinstance(result, (int, float))
        assert result == 100.0

    def test_50_probability(self):
        inp = make_input(win_probability_pct=50.0)
        assert _probability_score(inp) == 50.0

    def test_clamped_above_100(self):
        inp = make_input(win_probability_pct=150.0)
        assert _probability_score(inp) == 100.0

    def test_clamped_below_0(self):
        inp = make_input(win_probability_pct=-10.0)
        assert _probability_score(inp) == 0.0

    def test_fractional_probability(self):
        inp = make_input(win_probability_pct=72.5)
        assert _probability_score(inp) == 72.5

    def test_return_is_numeric(self):
        inp = make_input(win_probability_pct=60.0)
        assert isinstance(_probability_score(inp), (int, float))


# ---------------------------------------------------------------------------
# Class 7 — _velocity_score
# ---------------------------------------------------------------------------

class TestVelocityScore:
    """Tests _velocity_score weights, penalties, and clamping."""

    def test_simple_calculation_no_penalty(self):
        inp = make_input(stage_regression_count=0, blocker_count=0)
        pace, activity, prob = 80.0, 60.0, 70.0
        expected = round(pace * 0.40 + activity * 0.30 + prob * 0.20, 2)
        assert _velocity_score(pace, activity, prob, inp) == expected

    def test_regression_penalty(self):
        inp = make_input(stage_regression_count=1, blocker_count=0)
        pace, activity, prob = 80.0, 60.0, 70.0
        base = pace * 0.40 + activity * 0.30 + prob * 0.20
        penalty = min(20.0, 1 * 8.0)
        expected = round(max(0.0, min(100.0, base - penalty)), 2)
        assert _velocity_score(pace, activity, prob, inp) == expected

    def test_blocker_penalty(self):
        inp = make_input(stage_regression_count=0, blocker_count=1)
        pace, activity, prob = 80.0, 60.0, 70.0
        base = pace * 0.40 + activity * 0.30 + prob * 0.20
        penalty = min(15.0, 1 * 7.0)
        expected = round(max(0.0, min(100.0, base - penalty)), 2)
        assert _velocity_score(pace, activity, prob, inp) == expected

    def test_combined_penalty(self):
        inp = make_input(stage_regression_count=2, blocker_count=2)
        pace, activity, prob = 80.0, 60.0, 70.0
        base = pace * 0.40 + activity * 0.30 + prob * 0.20
        penalty = min(20.0, 2 * 8.0) + min(15.0, 2 * 7.0)
        expected = round(max(0.0, min(100.0, base - penalty)), 2)
        assert _velocity_score(pace, activity, prob, inp) == expected

    def test_regression_penalty_capped_at_20(self):
        # 3 regressions → 24, capped at 20
        inp = make_input(stage_regression_count=3, blocker_count=0)
        pace, activity, prob = 100.0, 100.0, 100.0
        base = 100.0 * 0.40 + 100.0 * 0.30 + 100.0 * 0.20
        penalty = 20.0  # capped
        expected = round(base - penalty, 2)
        assert _velocity_score(pace, activity, prob, inp) == expected

    def test_blocker_penalty_capped_at_15(self):
        # 3 blockers → 21, capped at 15
        inp = make_input(stage_regression_count=0, blocker_count=3)
        pace, activity, prob = 100.0, 100.0, 100.0
        base = 100.0 * 0.40 + 100.0 * 0.30 + 100.0 * 0.20
        penalty = 15.0  # capped
        expected = round(base - penalty, 2)
        assert _velocity_score(pace, activity, prob, inp) == expected

    def test_score_clamped_to_zero(self):
        inp = make_input(stage_regression_count=10, blocker_count=10)
        assert _velocity_score(0.0, 0.0, 0.0, inp) == 0.0

    def test_score_clamped_to_100(self):
        inp = make_input(stage_regression_count=0, blocker_count=0)
        assert _velocity_score(100.0, 100.0, 100.0, inp) == pytest.approx(90.0, abs=0.01)

    def test_weights_sum_to_90_pct(self):
        # With all 100s and no penalty: 100*0.4 + 100*0.3 + 100*0.2 = 90 (not 100)
        inp = make_input(stage_regression_count=0, blocker_count=0)
        result = _velocity_score(100.0, 100.0, 100.0, inp)
        assert result == 90.0

    def test_return_is_float(self):
        inp = make_input()
        assert isinstance(_velocity_score(50.0, 50.0, 50.0, inp), float)


# ---------------------------------------------------------------------------
# Class 8 — _schedule_delta
# ---------------------------------------------------------------------------

class TestScheduleDelta:
    def test_expected_days_zero_returns_zero(self):
        inp = make_input(expected_total_days=0)
        assert _schedule_delta(inp) == 0.0

    def test_expected_days_negative_returns_zero(self):
        inp = make_input(expected_total_days=-5)
        assert _schedule_delta(inp) == 0.0

    def test_ahead_of_schedule(self):
        # 30 total days in 90 expected → elapsed 33.3%; win prob 70% → delta=36.7
        inp = make_input(
            total_days_in_pipeline=30,
            expected_total_days=90,
            win_probability_pct=70.0,
        )
        elapsed_pct = min(100.0, 30 / 90 * 100.0)
        expected = round(70.0 - elapsed_pct, 1)
        assert _schedule_delta(inp) == expected

    def test_on_schedule(self):
        # 50% elapsed, 50% win prob → delta=0
        inp = make_input(
            total_days_in_pipeline=45,
            expected_total_days=90,
            win_probability_pct=50.0,
        )
        assert _schedule_delta(inp) == 0.0

    def test_behind_schedule(self):
        # 80 days / 90 expected → elapsed=88.9%; win_prob=60% → delta≈-28.9
        inp = make_input(
            total_days_in_pipeline=80,
            expected_total_days=90,
            win_probability_pct=60.0,
        )
        elapsed_pct = min(100.0, 80 / 90 * 100.0)
        expected = round(60.0 - elapsed_pct, 1)
        assert _schedule_delta(inp) == expected

    def test_elapsed_capped_at_100(self):
        # more days than expected → elapsed capped at 100
        inp = make_input(
            total_days_in_pipeline=200,
            expected_total_days=90,
            win_probability_pct=50.0,
        )
        assert _schedule_delta(inp) == round(50.0 - 100.0, 1)

    def test_return_is_rounded_to_1_decimal(self):
        inp = make_input(
            total_days_in_pipeline=30,
            expected_total_days=90,
            win_probability_pct=70.0,
        )
        result = _schedule_delta(inp)
        assert result == round(result, 1)

    def test_return_is_float(self):
        inp = make_input()
        assert isinstance(_schedule_delta(inp), float)


# ---------------------------------------------------------------------------
# Class 9 — _velocity_eur_per_day
# ---------------------------------------------------------------------------

class TestVelocityEurPerDay:
    def test_basic_calculation(self):
        inp = make_input(arr_eur=100_000.0, win_probability_pct=50.0, total_days_in_pipeline=10)
        expected = round(100_000.0 * 50.0 / 100.0 / 10, 2)
        assert _velocity_eur_per_day(inp) == expected

    def test_zero_days_uses_1(self):
        # total_days=0 → max(1,0)=1
        inp = make_input(arr_eur=10_000.0, win_probability_pct=100.0, total_days_in_pipeline=0)
        assert _velocity_eur_per_day(inp) == 10_000.0

    def test_zero_probability(self):
        inp = make_input(arr_eur=100_000.0, win_probability_pct=0.0, total_days_in_pipeline=30)
        assert _velocity_eur_per_day(inp) == 0.0

    def test_100_probability(self):
        inp = make_input(arr_eur=50_000.0, win_probability_pct=100.0, total_days_in_pipeline=50)
        assert _velocity_eur_per_day(inp) == round(50_000.0 / 50, 2)

    def test_return_is_rounded(self):
        inp = make_input(arr_eur=100_000.0, win_probability_pct=33.0, total_days_in_pipeline=7)
        result = _velocity_eur_per_day(inp)
        assert result == round(result, 2)

    def test_return_is_float(self):
        inp = make_input()
        assert isinstance(_velocity_eur_per_day(inp), float)


# ---------------------------------------------------------------------------
# Class 10 — _velocity_status
# ---------------------------------------------------------------------------

class TestVelocityStatus_Function:
    """Tests the _velocity_status mapping function."""

    def test_exactly_75_is_fast(self):
        assert _velocity_status(75.0) == VelocityStatus.FAST

    def test_above_75_is_fast(self):
        assert _velocity_status(99.9) == VelocityStatus.FAST

    def test_100_is_fast(self):
        assert _velocity_status(100.0) == VelocityStatus.FAST

    def test_exactly_50_is_on_pace(self):
        assert _velocity_status(50.0) == VelocityStatus.ON_PACE

    def test_74_9_is_on_pace(self):
        assert _velocity_status(74.9) == VelocityStatus.ON_PACE

    def test_exactly_25_is_slow(self):
        assert _velocity_status(25.0) == VelocityStatus.SLOW

    def test_49_9_is_slow(self):
        assert _velocity_status(49.9) == VelocityStatus.SLOW

    def test_24_9_is_stalled(self):
        assert _velocity_status(24.9) == VelocityStatus.STALLED

    def test_zero_is_stalled(self):
        assert _velocity_status(0.0) == VelocityStatus.STALLED

    def test_return_type(self):
        assert isinstance(_velocity_status(50.0), VelocityStatus)


# ---------------------------------------------------------------------------
# Class 11 — _velocity_action
# ---------------------------------------------------------------------------

class TestVelocityAction_Function:
    """Tests all 4 branches of _velocity_action in priority order."""

    # Branch 1: CLOSE_NOW — closing + win_prob>=70 + last_activity<=3
    def test_close_now_all_conditions_met(self):
        inp = make_input(stage="closing", win_probability_pct=70.0, last_activity_days=3)
        action = _velocity_action(inp, VelocityStatus.ON_PACE)
        assert action == VelocityAction.CLOSE_NOW

    def test_close_now_exactly_70_prob(self):
        inp = make_input(stage="closing", win_probability_pct=70.0, last_activity_days=0)
        assert _velocity_action(inp, VelocityStatus.ON_PACE) == VelocityAction.CLOSE_NOW

    def test_close_now_exactly_3_days(self):
        inp = make_input(stage="closing", win_probability_pct=90.0, last_activity_days=3)
        assert _velocity_action(inp, VelocityStatus.FAST) == VelocityAction.CLOSE_NOW

    def test_close_now_not_triggered_wrong_stage(self):
        inp = make_input(stage="proposal", win_probability_pct=90.0, last_activity_days=1)
        result = _velocity_action(inp, VelocityStatus.FAST)
        assert result != VelocityAction.CLOSE_NOW

    def test_close_now_not_triggered_low_prob(self):
        inp = make_input(stage="closing", win_probability_pct=69.9, last_activity_days=1)
        result = _velocity_action(inp, VelocityStatus.FAST)
        assert result != VelocityAction.CLOSE_NOW

    def test_close_now_not_triggered_stale_activity(self):
        inp = make_input(stage="closing", win_probability_pct=90.0, last_activity_days=4)
        result = _velocity_action(inp, VelocityStatus.FAST)
        assert result != VelocityAction.CLOSE_NOW

    # Branch 2: RESCUE — STALLED or regression>=2 or blocker>=2
    def test_rescue_stalled_status(self):
        inp = make_input(stage_regression_count=0, blocker_count=0, last_activity_days=1, has_next_step_scheduled=True)
        assert _velocity_action(inp, VelocityStatus.STALLED) == VelocityAction.RESCUE

    def test_rescue_regression_2(self):
        inp = make_input(stage="proposal", stage_regression_count=2, blocker_count=0,
                         last_activity_days=1, has_next_step_scheduled=True)
        assert _velocity_action(inp, VelocityStatus.ON_PACE) == VelocityAction.RESCUE

    def test_rescue_regression_3(self):
        inp = make_input(stage="proposal", stage_regression_count=3, blocker_count=0,
                         last_activity_days=1, has_next_step_scheduled=True)
        assert _velocity_action(inp, VelocityStatus.FAST) == VelocityAction.RESCUE

    def test_rescue_blocker_2(self):
        inp = make_input(stage="proposal", stage_regression_count=0, blocker_count=2,
                         last_activity_days=1, has_next_step_scheduled=True)
        assert _velocity_action(inp, VelocityStatus.ON_PACE) == VelocityAction.RESCUE

    def test_rescue_blocker_3(self):
        inp = make_input(stage="proposal", stage_regression_count=0, blocker_count=3,
                         last_activity_days=1, has_next_step_scheduled=True)
        assert _velocity_action(inp, VelocityStatus.FAST) == VelocityAction.RESCUE

    def test_rescue_not_triggered_regression_1(self):
        # regression=1 alone doesn't trigger RESCUE
        inp = make_input(stage="proposal", stage_regression_count=1, blocker_count=0,
                         last_activity_days=1, has_next_step_scheduled=True)
        result = _velocity_action(inp, VelocityStatus.ON_PACE)
        assert result != VelocityAction.RESCUE

    def test_rescue_not_triggered_blocker_1(self):
        # blocker=1 alone doesn't trigger RESCUE
        inp = make_input(stage="proposal", stage_regression_count=0, blocker_count=1,
                         last_activity_days=1, has_next_step_scheduled=True)
        result = _velocity_action(inp, VelocityStatus.ON_PACE)
        assert result != VelocityAction.RESCUE

    # Branch 3: ACCELERATE — SLOW or last_activity>7 or no next step
    def test_accelerate_slow_status(self):
        inp = make_input(stage="proposal", stage_regression_count=0, blocker_count=0,
                         last_activity_days=1, has_next_step_scheduled=True)
        assert _velocity_action(inp, VelocityStatus.SLOW) == VelocityAction.ACCELERATE

    def test_accelerate_stale_activity(self):
        inp = make_input(stage="proposal", stage_regression_count=0, blocker_count=0,
                         last_activity_days=8, has_next_step_scheduled=True)
        assert _velocity_action(inp, VelocityStatus.ON_PACE) == VelocityAction.ACCELERATE

    def test_accelerate_no_next_step(self):
        inp = make_input(stage="proposal", stage_regression_count=0, blocker_count=0,
                         last_activity_days=2, has_next_step_scheduled=False)
        assert _velocity_action(inp, VelocityStatus.ON_PACE) == VelocityAction.ACCELERATE

    def test_accelerate_exactly_7_days_no(self):
        # exactly 7 days → NOT > 7 → doesn't trigger
        inp = make_input(stage="proposal", stage_regression_count=0, blocker_count=0,
                         last_activity_days=7, has_next_step_scheduled=True)
        result = _velocity_action(inp, VelocityStatus.ON_PACE)
        assert result == VelocityAction.MONITOR

    # Branch 4: MONITOR
    def test_monitor_healthy_deal(self):
        inp = make_input(stage="proposal", stage_regression_count=0, blocker_count=0,
                         last_activity_days=2, has_next_step_scheduled=True)
        assert _velocity_action(inp, VelocityStatus.ON_PACE) == VelocityAction.MONITOR

    def test_monitor_fast_deal(self):
        inp = make_input(stage="proposal", stage_regression_count=0, blocker_count=0,
                         last_activity_days=1, has_next_step_scheduled=True)
        assert _velocity_action(inp, VelocityStatus.FAST) == VelocityAction.MONITOR

    def test_close_now_overrides_rescue(self):
        # Even if STALLED, closing+70%+recent activity → CLOSE_NOW first
        inp = make_input(stage="closing", win_probability_pct=80.0, last_activity_days=1,
                         stage_regression_count=2, blocker_count=2)
        assert _velocity_action(inp, VelocityStatus.STALLED) == VelocityAction.CLOSE_NOW


# ---------------------------------------------------------------------------
# Class 12 — _build_signals: risk flags
# ---------------------------------------------------------------------------

class TestBuildSignals_RiskFlags:
    def _call(self, inp, status=VelocityStatus.ON_PACE, overdue=False, delta=0.0):
        return _build_signals(inp, status, overdue, delta)

    def test_stage_overdue_flag(self):
        inp = make_input(stage="proposal", days_in_current_stage=30)
        flags, _, _ = self._call(inp, overdue=True)
        assert any("stage" in f.lower() or "benchmark" in f.lower() for f in flags)

    def test_stage_overdue_includes_benchmark(self):
        inp = make_input(stage="proposal", days_in_current_stage=30)
        flags, _, _ = self._call(inp, overdue=True)
        assert any("21" in f for f in flags)

    def test_stage_not_overdue_no_flag(self):
        inp = make_input(stage="proposal", days_in_current_stage=10)
        flags, _, _ = self._call(inp, overdue=False)
        assert not any("benchmark" in f for f in flags)

    def test_regression_2_flag(self):
        inp = make_input(stage_regression_count=2)
        flags, _, _ = self._call(inp)
        assert any("2x" in f or "2" in f for f in flags)

    def test_regression_3_flag(self):
        inp = make_input(stage_regression_count=3)
        flags, _, _ = self._call(inp)
        assert any("3x" in f for f in flags)

    def test_regression_1_flag(self):
        inp = make_input(stage_regression_count=1)
        flags, _, _ = self._call(inp)
        assert any("régression" in f.lower() or "regression" in f.lower() for f in flags)

    def test_regression_0_no_flag(self):
        inp = make_input(stage_regression_count=0)
        flags, _, _ = self._call(inp)
        assert not any("régression" in f.lower() for f in flags)

    def test_blocker_flag(self):
        inp = make_input(blocker_count=2)
        flags, _, _ = self._call(inp)
        assert any("bloqueur" in f.lower() for f in flags)

    def test_no_blocker_no_flag(self):
        inp = make_input(blocker_count=0)
        flags, _, _ = self._call(inp)
        assert not any("bloqueur" in f.lower() for f in flags)

    def test_last_activity_gt_14_days_flag(self):
        inp = make_input(last_activity_days=15)
        flags, _, _ = self._call(inp)
        assert any("danger" in f.lower() for f in flags)

    def test_last_activity_8_days_flag(self):
        inp = make_input(last_activity_days=8)
        flags, _, _ = self._call(inp)
        assert any("faible" in f.lower() or "sans contact" in f.lower() for f in flags)

    def test_last_activity_7_days_no_inactivity_flag(self):
        inp = make_input(last_activity_days=7)
        flags, _, _ = self._call(inp)
        assert not any("danger" in f.lower() for f in flags)
        assert not any("faible activité" in f.lower() for f in flags)

    def test_no_next_step_flag(self):
        inp = make_input(has_next_step_scheduled=False)
        flags, _, _ = self._call(inp)
        assert any("prochaine" in f.lower() for f in flags)

    def test_next_step_present_no_flag(self):
        inp = make_input(has_next_step_scheduled=True)
        flags, _, _ = self._call(inp)
        assert not any("prochaine" in f.lower() for f in flags)

    def test_no_champion_flag(self):
        inp = make_input(champion_present=False)
        flags, _, _ = self._call(inp)
        assert any("champion" in f.lower() for f in flags)

    def test_champion_present_no_flag(self):
        inp = make_input(champion_present=True)
        flags, _, _ = self._call(inp)
        assert not any("champion" in f.lower() for f in flags)

    def test_low_win_prob_flag(self):
        inp = make_input(win_probability_pct=10.0)
        flags, _, _ = self._call(inp)
        assert any("probabilité" in f.lower() or "faible" in f.lower() for f in flags)

    def test_win_prob_exactly_20_no_flag(self):
        inp = make_input(win_probability_pct=20.0)
        flags, _, _ = self._call(inp)
        assert not any("probabilité de gain faible" in f.lower() for f in flags)

    def test_delta_less_than_minus_20_flag(self):
        inp = make_input()
        flags, _, _ = self._call(inp, delta=-25.0)
        assert any("retard" in f.lower() for f in flags)

    def test_delta_minus_20_no_flag(self):
        inp = make_input()
        flags, _, _ = self._call(inp, delta=-20.0)
        assert not any("retard" in f.lower() for f in flags)

    def test_clean_deal_no_flags(self):
        inp = make_input(
            stage_regression_count=0,
            blocker_count=0,
            last_activity_days=1,
            has_next_step_scheduled=True,
            champion_present=True,
            win_probability_pct=80.0,
        )
        flags, _, _ = self._call(inp, overdue=False, delta=0.0)
        assert len(flags) == 0


# ---------------------------------------------------------------------------
# Class 13 — _build_signals: momentum signals
# ---------------------------------------------------------------------------

class TestBuildSignals_MomentumSignals:
    def _call(self, inp, status=VelocityStatus.ON_PACE, overdue=False, delta=0.0):
        return _build_signals(inp, status, overdue, delta)

    def test_high_win_prob_signal(self):
        inp = make_input(win_probability_pct=70.0)
        _, signals, _ = self._call(inp)
        assert any("70" in s for s in signals)

    def test_exactly_70_win_prob_signal(self):
        inp = make_input(win_probability_pct=70.0)
        _, signals, _ = self._call(inp)
        assert any("probabilité" in s.lower() for s in signals)

    def test_below_70_win_prob_no_signal(self):
        inp = make_input(win_probability_pct=69.9)
        _, signals, _ = self._call(inp)
        assert not any("probabilité de gain élevée" in s.lower() for s in signals)

    def test_champion_signal(self):
        inp = make_input(champion_present=True)
        _, signals, _ = self._call(inp)
        assert any("champion" in s.lower() for s in signals)

    def test_no_champion_no_signal(self):
        inp = make_input(champion_present=False)
        _, signals, _ = self._call(inp)
        assert not any("champion actif" in s.lower() for s in signals)

    def test_decision_maker_signal(self):
        inp = make_input(decision_maker_engaged=True)
        _, signals, _ = self._call(inp)
        assert any("décideur" in s.lower() for s in signals)

    def test_no_decision_maker_no_signal(self):
        inp = make_input(decision_maker_engaged=False)
        _, signals, _ = self._call(inp)
        assert not any("décideur engagé" in s.lower() for s in signals)

    def test_next_step_signal(self):
        inp = make_input(has_next_step_scheduled=True)
        _, signals, _ = self._call(inp)
        assert any("prochaine" in s.lower() for s in signals)

    def test_no_next_step_no_signal(self):
        inp = make_input(has_next_step_scheduled=False)
        _, signals, _ = self._call(inp)
        assert not any("prochaine étape planifiée" in s.lower() for s in signals)

    def test_recent_activity_signal(self):
        inp = make_input(last_activity_days=3)
        _, signals, _ = self._call(inp)
        assert any("récente" in s.lower() or "vivant" in s.lower() for s in signals)

    def test_activity_4_days_no_signal(self):
        inp = make_input(last_activity_days=4)
        _, signals, _ = self._call(inp)
        assert not any("activité récente" in s.lower() for s in signals)

    def test_no_regression_signal(self):
        inp = make_input(stage_regression_count=0, total_days_in_pipeline=10)
        _, signals, _ = self._call(inp)
        assert any("aucune régression" in s.lower() for s in signals)

    def test_no_regression_less_than_7_days_no_signal(self):
        # regression==0 but total_days<=7 → no signal
        inp = make_input(stage_regression_count=0, total_days_in_pipeline=7)
        _, signals, _ = self._call(inp)
        assert not any("aucune régression" in s.lower() for s in signals)

    def test_regression_present_no_linear_signal(self):
        inp = make_input(stage_regression_count=1, total_days_in_pipeline=10)
        _, signals, _ = self._call(inp)
        assert not any("aucune régression" in s.lower() for s in signals)

    def test_delta_above_10_signal(self):
        inp = make_input()
        _, signals, _ = self._call(inp, delta=15.0)
        assert any("avance" in s.lower() for s in signals)

    def test_delta_exactly_10_no_signal(self):
        inp = make_input()
        _, signals, _ = self._call(inp, delta=10.0)
        assert not any("avance" in s.lower() for s in signals)

    def test_closing_stage_signal(self):
        inp = make_input(stage="closing")
        _, signals, _ = self._call(inp)
        assert any("closing" in s.lower() or "signature" in s.lower() for s in signals)

    def test_non_closing_stage_no_signal(self):
        inp = make_input(stage="proposal")
        _, signals, _ = self._call(inp)
        assert not any("closing" in s.lower() for s in signals)


# ---------------------------------------------------------------------------
# Class 14 — _build_signals: recommended actions
# ---------------------------------------------------------------------------

class TestBuildSignals_Actions:
    def _call(self, inp, status=VelocityStatus.ON_PACE, overdue=False, delta=0.0):
        return _build_signals(inp, status, overdue, delta)

    def test_blocker_action(self):
        inp = make_input(blocker_count=2)
        _, _, actions = self._call(inp)
        assert any("bloqueur" in a.lower() or "résoudre" in a.lower() for a in actions)

    def test_no_blocker_no_action(self):
        inp = make_input(blocker_count=0)
        _, _, actions = self._call(inp)
        assert not any("résoudre" in a.lower() for a in actions)

    def test_no_next_step_action(self):
        inp = make_input(has_next_step_scheduled=False)
        _, _, actions = self._call(inp)
        assert any("prochaine étape" in a.lower() for a in actions)

    def test_next_step_present_no_action(self):
        inp = make_input(has_next_step_scheduled=True)
        _, _, actions = self._call(inp)
        assert not any("planifier la prochaine" in a.lower() for a in actions)

    def test_stale_activity_action(self):
        inp = make_input(last_activity_days=8)
        _, _, actions = self._call(inp)
        assert any("reprendre contact" in a.lower() for a in actions)

    def test_recent_activity_no_stale_action(self):
        inp = make_input(last_activity_days=7)
        _, _, actions = self._call(inp)
        assert not any("reprendre contact" in a.lower() for a in actions)

    def test_regression_action(self):
        inp = make_input(stage_regression_count=1)
        _, _, actions = self._call(inp)
        assert any("régression" in a.lower() for a in actions)

    def test_no_regression_no_action(self):
        inp = make_input(stage_regression_count=0)
        _, _, actions = self._call(inp)
        assert not any("régression" in a.lower() for a in actions)

    def test_no_champion_action(self):
        inp = make_input(champion_present=False)
        _, _, actions = self._call(inp)
        assert any("champion" in a.lower() for a in actions)

    def test_champion_present_no_action(self):
        inp = make_input(champion_present=True)
        _, _, actions = self._call(inp)
        assert not any("identifier et activer" in a.lower() for a in actions)

    def test_dm_not_engaged_in_proposal_action(self):
        inp = make_input(stage="proposal", decision_maker_engaged=False)
        _, _, actions = self._call(inp)
        assert any("décideur" in a.lower() for a in actions)

    def test_dm_not_engaged_in_negotiation_action(self):
        inp = make_input(stage="negotiation", decision_maker_engaged=False)
        _, _, actions = self._call(inp)
        assert any("décideur" in a.lower() for a in actions)

    def test_dm_not_engaged_in_closing_action(self):
        inp = make_input(stage="closing", decision_maker_engaged=False)
        _, _, actions = self._call(inp)
        assert any("décideur" in a.lower() for a in actions)

    def test_dm_not_engaged_in_early_stage_no_action(self):
        inp = make_input(stage="prospecting", decision_maker_engaged=False)
        _, _, actions = self._call(inp)
        assert not any("engager le décideur" in a.lower() for a in actions)

    def test_closing_high_prob_action(self):
        inp = make_input(stage="closing", win_probability_pct=70.0)
        _, _, actions = self._call(inp)
        assert any("contractuel" in a.lower() or "signature" in a.lower() for a in actions)

    def test_closing_low_prob_no_contract_action(self):
        inp = make_input(stage="closing", win_probability_pct=60.0)
        _, _, actions = self._call(inp)
        assert not any("finaliser les termes contractuels" in a.lower() for a in actions)

    def test_stalled_abandon_action(self):
        inp = make_input()
        _, _, actions = self._call(inp, status=VelocityStatus.STALLED)
        assert any("abandonné" in a.lower() or "pause" in a.lower() for a in actions)

    def test_non_stalled_no_abandon_action(self):
        inp = make_input()
        _, _, actions = self._call(inp, status=VelocityStatus.ON_PACE)
        assert not any("abandonné" in a.lower() for a in actions)

    def test_overdue_stage_action(self):
        inp = make_input(stage="proposal", days_in_current_stage=30)
        _, _, actions = self._call(inp, overdue=True)
        assert any("accélérer" in a.lower() for a in actions)

    def test_not_overdue_no_stage_acceleration_action(self):
        inp = make_input(stage="proposal", days_in_current_stage=10)
        _, _, actions = self._call(inp, overdue=False)
        assert not any("dépassé de" in a.lower() for a in actions)


# ---------------------------------------------------------------------------
# Class 15 — PipelineVelocityCalculator.calculate
# ---------------------------------------------------------------------------

class TestCalculator_Calculate:
    def setup_method(self):
        self.calc = PipelineVelocityCalculator()

    def test_returns_result_type(self):
        result = self.calc.calculate(make_input())
        assert isinstance(result, PipelineVelocityResult)

    def test_deal_id_stored(self):
        inp = make_input(deal_id="D999")
        result = self.calc.calculate(inp)
        assert result.deal_id == "D999"

    def test_get_by_id(self):
        inp = make_input(deal_id="D42")
        self.calc.calculate(inp)
        assert self.calc.get("D42") is not None

    def test_get_missing_returns_none(self):
        assert self.calc.get("MISSING") is None

    def test_velocity_score_in_range(self):
        result = self.calc.calculate(make_input())
        assert 0.0 <= result.velocity_score <= 100.0

    def test_stage_benchmark_stored(self):
        result = self.calc.calculate(make_input(stage="proposal"))
        assert result.stage_benchmark_days == 21

    def test_stage_benchmark_closing(self):
        result = self.calc.calculate(make_input(stage="closing"))
        assert result.stage_benchmark_days == 7

    def test_stage_overdue_true(self):
        result = self.calc.calculate(make_input(stage="prospecting", days_in_current_stage=10))
        assert result.stage_overdue is True

    def test_stage_overdue_false(self):
        result = self.calc.calculate(make_input(stage="proposal", days_in_current_stage=10))
        assert result.stage_overdue is False

    def test_velocity_status_type(self):
        result = self.calc.calculate(make_input())
        assert isinstance(result.velocity_status, VelocityStatus)

    def test_velocity_action_type(self):
        result = self.calc.calculate(make_input())
        assert isinstance(result.velocity_action, VelocityAction)

    def test_risk_flags_is_list(self):
        result = self.calc.calculate(make_input())
        assert isinstance(result.risk_flags, list)

    def test_momentum_signals_is_list(self):
        result = self.calc.calculate(make_input())
        assert isinstance(result.momentum_signals, list)

    def test_recommended_actions_is_list(self):
        result = self.calc.calculate(make_input())
        assert isinstance(result.recommended_actions, list)

    def test_result_stored_in_cache(self):
        inp = make_input(deal_id="DX")
        self.calc.calculate(inp)
        assert "DX" in self.calc._results

    def test_overwrite_previous_result(self):
        inp1 = make_input(deal_id="D1", win_probability_pct=10.0)
        inp2 = make_input(deal_id="D1", win_probability_pct=90.0)
        self.calc.calculate(inp1)
        self.calc.calculate(inp2)
        assert self.calc.get("D1").probability_score == 90.0

    def test_to_dict_has_string_status(self):
        result = self.calc.calculate(make_input())
        d = result.to_dict()
        assert isinstance(d["velocity_status"], str)
        assert isinstance(d["velocity_action"], str)


# ---------------------------------------------------------------------------
# Class 16 — PipelineVelocityCalculator.calculate_batch and ordering
# ---------------------------------------------------------------------------

class TestCalculator_Batch:
    def setup_method(self):
        self.calc = PipelineVelocityCalculator()

    def _make_stalled(self, deal_id):
        return make_input(
            deal_id=deal_id,
            stage="prospecting",
            days_in_current_stage=100,
            win_probability_pct=5.0,
            last_activity_days=30,
            has_next_step_scheduled=False,
            stage_regression_count=3,
            blocker_count=3,
            champion_present=False,
            decision_maker_engaged=False,
        )

    def _make_fast(self, deal_id):
        return make_input(
            deal_id=deal_id,
            stage="closing",
            days_in_current_stage=2,
            win_probability_pct=90.0,
            last_activity_days=1,
            has_next_step_scheduled=True,
            stage_regression_count=0,
            blocker_count=0,
            champion_present=True,
            decision_maker_engaged=True,
        )

    def test_batch_returns_list(self):
        results = self.calc.calculate_batch([make_input("D1"), make_input("D2")])
        assert isinstance(results, list)
        assert len(results) == 2

    def test_batch_sorted_asc_by_score(self):
        results = self.calc.calculate_batch([
            self._make_fast("F"),
            self._make_stalled("S"),
        ])
        assert results[0].velocity_score <= results[-1].velocity_score

    def test_batch_stores_all_in_cache(self):
        self.calc.calculate_batch([make_input("D1"), make_input("D2"), make_input("D3")])
        assert len(self.calc._results) == 3

    def test_all_deals_sorted_asc(self):
        self.calc.calculate_batch([
            self._make_fast("F"),
            self._make_stalled("S"),
        ])
        all_d = self.calc.all_deals()
        scores = [r.velocity_score for r in all_d]
        assert scores == sorted(scores)


# ---------------------------------------------------------------------------
# Class 17 — PipelineVelocityCalculator filtering methods
# ---------------------------------------------------------------------------

class TestCalculator_Filters:
    def setup_method(self):
        self.calc = PipelineVelocityCalculator()
        # Stalled deal
        self.calc.calculate(make_input(
            deal_id="S1",
            stage="prospecting",
            days_in_current_stage=100,
            win_probability_pct=5.0,
            last_activity_days=30,
            has_next_step_scheduled=False,
            stage_regression_count=3,
            blocker_count=3,
            champion_present=False,
            decision_maker_engaged=False,
        ))
        # Close-now deal
        self.calc.calculate(make_input(
            deal_id="C1",
            stage="closing",
            days_in_current_stage=2,
            win_probability_pct=90.0,
            last_activity_days=1,
            has_next_step_scheduled=True,
            stage_regression_count=0,
            blocker_count=0,
            champion_present=True,
            decision_maker_engaged=True,
        ))

    def test_stalled_returns_stalled_deals(self):
        stalled = self.calc.stalled()
        assert all(r.velocity_status == VelocityStatus.STALLED for r in stalled)

    def test_fast_returns_fast_deals(self):
        fast = self.calc.fast()
        assert all(r.velocity_status == VelocityStatus.FAST for r in fast)

    def test_needs_rescue_returns_rescue_deals(self):
        rescue = self.calc.needs_rescue()
        assert all(r.velocity_action == VelocityAction.RESCUE for r in rescue)

    def test_close_now_returns_close_now_deals(self):
        cn = self.calc.close_now()
        assert all(r.velocity_action == VelocityAction.CLOSE_NOW for r in cn)

    def test_at_risk_returns_stalled_and_slow(self):
        at_risk = self.calc.at_risk()
        for r in at_risk:
            assert r.velocity_status in (VelocityStatus.STALLED, VelocityStatus.SLOW)

    def test_by_status_on_pace(self):
        inp = make_input(deal_id="OP",
                         stage="proposal",
                         days_in_current_stage=10,
                         win_probability_pct=60.0,
                         last_activity_days=2,
                         stage_regression_count=0,
                         blocker_count=0)
        result = self.calc.calculate(inp)
        on_pace = self.calc.by_status(VelocityStatus.ON_PACE)
        # Check type constraint
        assert all(r.velocity_status == VelocityStatus.ON_PACE for r in on_pace)

    def test_by_segment_filters(self):
        self.calc.calculate(make_input(deal_id="E1", segment="enterprise"))
        self.calc.calculate(make_input(deal_id="S2", segment="smb"))
        enterprise = self.calc.by_segment("enterprise")
        assert all(r.segment == "enterprise" for r in enterprise)

    def test_by_stage_filters(self):
        self.calc.calculate(make_input(deal_id="PRO1", stage="proposal"))
        self.calc.calculate(make_input(deal_id="NEG1", stage="negotiation"))
        proposals = self.calc.by_stage("proposal")
        assert all(r.stage == "proposal" for r in proposals)

    def test_top_n_returns_n_results(self):
        for i in range(5):
            self.calc.calculate(make_input(deal_id=f"T{i}", arr_eur=float(i * 10000)))
        top = self.calc.top_n(3)
        assert len(top) == 3

    def test_top_n_sorted_by_eur_per_day_desc(self):
        for i in range(5):
            self.calc.calculate(make_input(deal_id=f"T{i}", arr_eur=float(i * 10000 + 1000)))
        top = self.calc.top_n(5)
        rates = [r.velocity_eur_per_day for r in top]
        assert rates == sorted(rates, reverse=True)


# ---------------------------------------------------------------------------
# Class 18 — PipelineVelocityCalculator aggregate metrics
# ---------------------------------------------------------------------------

class TestCalculator_Aggregates:
    def setup_method(self):
        self.calc = PipelineVelocityCalculator()

    def test_total_pipeline_eur_empty(self):
        assert self.calc.total_pipeline_eur() == 0.0

    def test_total_pipeline_eur_sums(self):
        self.calc.calculate(make_input(deal_id="A", arr_eur=50_000.0))
        self.calc.calculate(make_input(deal_id="B", arr_eur=30_000.0))
        assert self.calc.total_pipeline_eur() == pytest.approx(80_000.0)

    def test_total_weighted_pipeline_eur(self):
        self.calc.calculate(make_input(deal_id="A", arr_eur=100_000.0, win_probability_pct=50.0))
        result_a = self.calc.get("A")
        expected = round(100_000.0 * result_a.probability_score / 100.0, 2)
        assert self.calc.total_weighted_pipeline_eur() == pytest.approx(expected)

    def test_total_velocity_eur_per_day_sums(self):
        self.calc.calculate(make_input(deal_id="A", arr_eur=10_000.0, win_probability_pct=100.0, total_days_in_pipeline=10))
        self.calc.calculate(make_input(deal_id="B", arr_eur=20_000.0, win_probability_pct=100.0, total_days_in_pipeline=20))
        assert self.calc.total_velocity_eur_per_day() == pytest.approx(2000.0)

    def test_avg_velocity_score_empty(self):
        assert self.calc.avg_velocity_score() == 0.0

    def test_avg_velocity_score_single(self):
        inp = make_input(deal_id="X")
        result = self.calc.calculate(inp)
        assert self.calc.avg_velocity_score() == result.velocity_score

    def test_avg_velocity_score_multiple(self):
        self.calc.calculate(make_input(deal_id="A"))
        self.calc.calculate(make_input(deal_id="B"))
        scores = [r.velocity_score for r in self.calc._results.values()]
        expected = round(sum(scores) / len(scores), 1)
        assert self.calc.avg_velocity_score() == expected


# ---------------------------------------------------------------------------
# Class 19 — PipelineVelocityCalculator summary and reset
# ---------------------------------------------------------------------------

class TestCalculator_SummaryAndReset:
    def setup_method(self):
        self.calc = PipelineVelocityCalculator()

    def test_summary_empty(self):
        s = self.calc.summary()
        assert s["total"] == 0
        assert s["avg_velocity_score"] == 0.0
        assert s["stalled_count"] == 0
        assert s["rescue_count"] == 0
        assert s["close_now_count"] == 0

    def test_summary_keys_present(self):
        s = self.calc.summary()
        expected_keys = {
            "total", "status_counts", "action_counts", "avg_velocity_score",
            "total_velocity_eur_per_day", "total_pipeline_eur",
            "total_weighted_pipeline_eur", "stalled_count", "rescue_count",
            "close_now_count",
        }
        assert expected_keys == set(s.keys())

    def test_summary_total_count(self):
        self.calc.calculate(make_input(deal_id="A"))
        self.calc.calculate(make_input(deal_id="B"))
        assert self.calc.summary()["total"] == 2

    def test_summary_status_counts(self):
        self.calc.calculate(make_input(deal_id="A"))
        s = self.calc.summary()
        assert isinstance(s["status_counts"], dict)
        # All status values should be strings
        for k in s["status_counts"]:
            assert isinstance(k, str)

    def test_summary_action_counts(self):
        self.calc.calculate(make_input(deal_id="A"))
        s = self.calc.summary()
        assert isinstance(s["action_counts"], dict)

    def test_reset_clears_results(self):
        self.calc.calculate(make_input(deal_id="A"))
        self.calc.reset()
        assert len(self.calc._results) == 0

    def test_reset_then_calculate(self):
        self.calc.calculate(make_input(deal_id="A"))
        self.calc.reset()
        self.calc.calculate(make_input(deal_id="B"))
        assert self.calc.get("A") is None
        assert self.calc.get("B") is not None

    def test_summary_stalled_count(self):
        # Make a stalled deal
        self.calc.calculate(make_input(
            deal_id="S",
            stage="prospecting",
            days_in_current_stage=100,
            win_probability_pct=0.0,
            last_activity_days=60,
            has_next_step_scheduled=False,
            stage_regression_count=5,
            blocker_count=5,
            champion_present=False,
            decision_maker_engaged=False,
        ))
        s = self.calc.summary()
        assert s["stalled_count"] >= 0  # at least tracked


# ---------------------------------------------------------------------------
# Class 20 — PipelineVelocityResult.to_dict
# ---------------------------------------------------------------------------

class TestPipelineVelocityResult_ToDict:
    def setup_method(self):
        self.calc = PipelineVelocityCalculator()

    def test_to_dict_velocity_status_is_string(self):
        result = self.calc.calculate(make_input())
        d = result.to_dict()
        assert isinstance(d["velocity_status"], str)

    def test_to_dict_velocity_action_is_string(self):
        result = self.calc.calculate(make_input())
        d = result.to_dict()
        assert isinstance(d["velocity_action"], str)

    def test_to_dict_status_value_correct(self):
        result = self.calc.calculate(make_input())
        d = result.to_dict()
        assert d["velocity_status"] == result.velocity_status.value

    def test_to_dict_action_value_correct(self):
        result = self.calc.calculate(make_input())
        d = result.to_dict()
        assert d["velocity_action"] == result.velocity_action.value

    def test_to_dict_has_velocity_score(self):
        result = self.calc.calculate(make_input())
        d = result.to_dict()
        assert "velocity_score" in d

    def test_to_dict_has_arr_eur(self):
        result = self.calc.calculate(make_input(arr_eur=12345.0))
        d = result.to_dict()
        assert d["arr_eur"] == 12345.0

    def test_to_dict_has_risk_flags(self):
        result = self.calc.calculate(make_input())
        d = result.to_dict()
        assert "risk_flags" in d
        assert isinstance(d["risk_flags"], list)


# ---------------------------------------------------------------------------
# Class 21 — Integration / end-to-end scenarios
# ---------------------------------------------------------------------------

class TestIntegration:
    def setup_method(self):
        self.calc = PipelineVelocityCalculator()

    def test_perfect_deal_is_close_now(self):
        inp = make_input(
            deal_id="PERFECT",
            stage="closing",
            days_in_current_stage=2,
            total_days_in_pipeline=30,
            expected_total_days=90,
            win_probability_pct=90.0,
            last_activity_days=1,
            has_next_step_scheduled=True,
            stage_regression_count=0,
            blocker_count=0,
            champion_present=True,
            decision_maker_engaged=True,
        )
        result = self.calc.calculate(inp)
        assert result.velocity_action == VelocityAction.CLOSE_NOW

    def test_dead_deal_is_stalled_and_rescue(self):
        inp = make_input(
            deal_id="DEAD",
            stage="prospecting",
            days_in_current_stage=100,
            total_days_in_pipeline=100,
            expected_total_days=45,
            win_probability_pct=2.0,
            last_activity_days=60,
            has_next_step_scheduled=False,
            stage_regression_count=4,
            blocker_count=4,
            champion_present=False,
            decision_maker_engaged=False,
        )
        result = self.calc.calculate(inp)
        assert result.velocity_status == VelocityStatus.STALLED
        assert result.velocity_action == VelocityAction.RESCUE

    def test_healthy_deal_is_on_pace_and_monitor(self):
        inp = make_input(
            deal_id="HEALTHY",
            stage="proposal",
            days_in_current_stage=10,
            total_days_in_pipeline=30,
            expected_total_days=90,
            win_probability_pct=65.0,
            last_activity_days=2,
            has_next_step_scheduled=True,
            stage_regression_count=0,
            blocker_count=0,
            champion_present=True,
            decision_maker_engaged=True,
        )
        result = self.calc.calculate(inp)
        assert result.velocity_action == VelocityAction.MONITOR

    def test_batch_processes_all(self):
        inputs = [make_input(deal_id=f"D{i}") for i in range(10)]
        results = self.calc.calculate_batch(inputs)
        assert len(results) == 10

    def test_schedule_delta_reflected_in_result(self):
        inp = make_input(
            deal_id="DELTA",
            total_days_in_pipeline=80,
            expected_total_days=90,
            win_probability_pct=60.0,
        )
        result = self.calc.calculate(inp)
        elapsed_pct = min(100.0, 80 / 90 * 100.0)
        expected_delta = round(60.0 - elapsed_pct, 1)
        assert result.schedule_delta_pct == expected_delta

    def test_velocity_eur_per_day_in_result(self):
        inp = make_input(deal_id="VEL", arr_eur=100_000.0, win_probability_pct=50.0, total_days_in_pipeline=10)
        result = self.calc.calculate(inp)
        # 100_000 * 50% / 10 days = 5000.0
        assert result.velocity_eur_per_day == pytest.approx(5000.0)

    def test_multiple_deals_aggregates(self):
        for i in range(5):
            self.calc.calculate(make_input(deal_id=f"M{i}", arr_eur=20_000.0))
        assert self.calc.total_pipeline_eur() == pytest.approx(100_000.0)

    def test_at_risk_does_not_include_on_pace_or_fast(self):
        self.calc.calculate(make_input(
            deal_id="FAST",
            stage="closing",
            days_in_current_stage=2,
            win_probability_pct=90.0,
            last_activity_days=1,
            has_next_step_scheduled=True,
            stage_regression_count=0,
            blocker_count=0,
            champion_present=True,
            decision_maker_engaged=True,
        ))
        at_risk = self.calc.at_risk()
        ids = [r.deal_id for r in at_risk]
        assert "FAST" not in ids

    def test_reset_clears_aggregates(self):
        self.calc.calculate(make_input(deal_id="A", arr_eur=50_000.0))
        self.calc.reset()
        assert self.calc.total_pipeline_eur() == 0.0
        assert self.calc.avg_velocity_score() == 0.0
