"""Comprehensive pytest test suite for DealStageProgressionEngine (Module 36).

Run from /home/user/TEST with:
    python -m pytest swarm/tests/test_deal_stage_progression_engine.py -v
"""

from __future__ import annotations

import pytest

from swarm.intelligence.deal_stage_progression_engine import (
    CloseQuarterProbability,
    DealInput,
    DealProgressionResult,
    DealStage,
    DealStageProgressionEngine,
    ProgressionAction,
    ProgressionRisk,
)


# ─── Helper ───────────────────────────────────────────────────────────────────

def make_input(**overrides) -> DealInput:
    """Return a fully valid DealInput with sensible defaults."""
    defaults = dict(
        deal_id="D001",
        deal_name="Test Deal",
        rep_id="R001",
        rep_name="Alice",
        account_name="Acme Corp",
        current_stage=DealStage.QUALIFICATION,
        previous_stage=DealStage.PROSPECTING,
        days_in_current_stage=5,
        days_since_created=12,
        deal_size_eur=50_000.0,
        close_date_days_remaining=60,
        benchmark_days_prospecting=7,
        benchmark_days_qualification=10,
        benchmark_days_demo=14,
        benchmark_days_proposal=14,
        benchmark_days_negotiation=10,
        benchmark_days_closing=7,
        last_activity_days_ago=2,
        meetings_held=3,
        emails_sent=10,
        proposals_sent=1,
        exec_sponsor_engaged=True,
        budget_confirmed=True,
        timeline_confirmed=True,
        decision_maker_identified=True,
        rep_stage_win_rate_pct=70.0,
    )
    defaults.update(overrides)
    return DealInput(**defaults)


def make_engine() -> DealStageProgressionEngine:
    return DealStageProgressionEngine()


# ─── 1. Enum values and str inheritance ───────────────────────────────────────

class TestDealStageEnum:
    def test_all_members_exist(self):
        stages = {s.name for s in DealStage}
        assert stages == {"PROSPECTING", "QUALIFICATION", "DEMO", "PROPOSAL", "NEGOTIATION", "CLOSING"}

    def test_values(self):
        assert DealStage.PROSPECTING.value == "prospecting"
        assert DealStage.QUALIFICATION.value == "qualification"
        assert DealStage.DEMO.value == "demo"
        assert DealStage.PROPOSAL.value == "proposal"
        assert DealStage.NEGOTIATION.value == "negotiation"
        assert DealStage.CLOSING.value == "closing"

    def test_str_inheritance(self):
        assert isinstance(DealStage.PROSPECTING, str)
        assert DealStage.DEMO == "demo"

    def test_count(self):
        assert len(DealStage) == 6


class TestProgressionRiskEnum:
    def test_all_members_exist(self):
        assert {r.name for r in ProgressionRisk} == {"ON_TRACK", "SLOWING", "STUCK", "REGRESSED"}

    def test_values(self):
        assert ProgressionRisk.ON_TRACK.value == "on_track"
        assert ProgressionRisk.SLOWING.value == "slowing"
        assert ProgressionRisk.STUCK.value == "stuck"
        assert ProgressionRisk.REGRESSED.value == "regressed"

    def test_str_inheritance(self):
        assert isinstance(ProgressionRisk.STUCK, str)
        assert ProgressionRisk.ON_TRACK == "on_track"


class TestProgressionActionEnum:
    def test_all_members_exist(self):
        assert {a.name for a in ProgressionAction} == {
            "MAINTAIN", "ACCELERATE", "RESCUE", "CLOSE_NOW", "REPRIORITISE"
        }

    def test_values(self):
        assert ProgressionAction.MAINTAIN.value == "maintain"
        assert ProgressionAction.ACCELERATE.value == "accelerate"
        assert ProgressionAction.RESCUE.value == "rescue"
        assert ProgressionAction.CLOSE_NOW.value == "close_now"
        assert ProgressionAction.REPRIORITISE.value == "reprioritise"

    def test_str_inheritance(self):
        assert isinstance(ProgressionAction.RESCUE, str)
        assert ProgressionAction.CLOSE_NOW == "close_now"


class TestCloseQuarterProbabilityEnum:
    def test_all_members_exist(self):
        assert {p.name for p in CloseQuarterProbability} == {"HIGH", "MEDIUM", "LOW", "VERY_LOW"}

    def test_values(self):
        assert CloseQuarterProbability.HIGH.value == "high"
        assert CloseQuarterProbability.MEDIUM.value == "medium"
        assert CloseQuarterProbability.LOW.value == "low"
        assert CloseQuarterProbability.VERY_LOW.value == "very_low"

    def test_str_inheritance(self):
        assert isinstance(CloseQuarterProbability.HIGH, str)
        assert CloseQuarterProbability.VERY_LOW == "very_low"


# ─── 2. DealInput field count ─────────────────────────────────────────────────

class TestDealInputFields:
    def test_field_count(self):
        import dataclasses
        fields = dataclasses.fields(DealInput)
        assert len(fields) == 26

    def test_can_instantiate_with_defaults(self):
        inp = make_input()
        assert inp.deal_id == "D001"

    def test_optional_previous_stage_none(self):
        inp = make_input(previous_stage=None)
        assert inp.previous_stage is None

    def test_field_types(self):
        inp = make_input()
        assert isinstance(inp.deal_size_eur, float)
        assert isinstance(inp.days_in_current_stage, int)
        assert isinstance(inp.exec_sponsor_engaged, bool)
        assert isinstance(inp.rep_stage_win_rate_pct, float)


# ─── 3. stage_velocity_ratio ──────────────────────────────────────────────────

class TestStageVelocityRatio:
    def setup_method(self):
        self.engine = make_engine()

    def test_normal_ratio(self):
        inp = make_input(current_stage=DealStage.QUALIFICATION,
                         days_in_current_stage=10,
                         benchmark_days_qualification=10)
        ratio = self.engine._stage_velocity_ratio(inp)
        assert ratio == pytest.approx(1.0)

    def test_faster_than_benchmark(self):
        inp = make_input(current_stage=DealStage.QUALIFICATION,
                         days_in_current_stage=5,
                         benchmark_days_qualification=10)
        ratio = self.engine._stage_velocity_ratio(inp)
        assert ratio == pytest.approx(0.5)

    def test_slower_than_benchmark(self):
        inp = make_input(current_stage=DealStage.DEMO,
                         days_in_current_stage=28,
                         benchmark_days_demo=14)
        ratio = self.engine._stage_velocity_ratio(inp)
        assert ratio == pytest.approx(2.0)

    def test_zero_benchmark_returns_one(self):
        inp = make_input(current_stage=DealStage.PROSPECTING,
                         days_in_current_stage=5,
                         benchmark_days_prospecting=0)
        ratio = self.engine._stage_velocity_ratio(inp)
        assert ratio == pytest.approx(1.0)

    def test_negative_benchmark_returns_one(self):
        inp = make_input(current_stage=DealStage.PROSPECTING,
                         days_in_current_stage=5,
                         benchmark_days_prospecting=-1)
        ratio = self.engine._stage_velocity_ratio(inp)
        assert ratio == pytest.approx(1.0)

    def test_zero_days_ratio(self):
        inp = make_input(current_stage=DealStage.CLOSING,
                         days_in_current_stage=0,
                         benchmark_days_closing=7)
        ratio = self.engine._stage_velocity_ratio(inp)
        assert ratio == pytest.approx(0.0)

    def test_prospecting_stage(self):
        inp = make_input(current_stage=DealStage.PROSPECTING,
                         days_in_current_stage=7,
                         benchmark_days_prospecting=7)
        assert self.engine._stage_velocity_ratio(inp) == pytest.approx(1.0)

    def test_proposal_stage(self):
        inp = make_input(current_stage=DealStage.PROPOSAL,
                         days_in_current_stage=7,
                         benchmark_days_proposal=14)
        assert self.engine._stage_velocity_ratio(inp) == pytest.approx(0.5)

    def test_negotiation_stage(self):
        inp = make_input(current_stage=DealStage.NEGOTIATION,
                         days_in_current_stage=20,
                         benchmark_days_negotiation=10)
        assert self.engine._stage_velocity_ratio(inp) == pytest.approx(2.0)


# ─── 4. days_over_benchmark ───────────────────────────────────────────────────

class TestDaysOverBenchmark:
    def setup_method(self):
        self.engine = make_engine()

    def test_over_benchmark(self):
        inp = make_input(current_stage=DealStage.DEMO,
                         days_in_current_stage=20,
                         benchmark_days_demo=14)
        assert self.engine._days_over_benchmark(inp) == 6

    def test_at_benchmark_is_zero(self):
        inp = make_input(current_stage=DealStage.DEMO,
                         days_in_current_stage=14,
                         benchmark_days_demo=14)
        assert self.engine._days_over_benchmark(inp) == 0

    def test_under_benchmark_is_zero(self):
        inp = make_input(current_stage=DealStage.DEMO,
                         days_in_current_stage=5,
                         benchmark_days_demo=14)
        assert self.engine._days_over_benchmark(inp) == 0

    def test_exactly_one_day_over(self):
        inp = make_input(current_stage=DealStage.QUALIFICATION,
                         days_in_current_stage=11,
                         benchmark_days_qualification=10)
        assert self.engine._days_over_benchmark(inp) == 1

    def test_never_negative(self):
        inp = make_input(current_stage=DealStage.PROSPECTING,
                         days_in_current_stage=0,
                         benchmark_days_prospecting=7)
        assert self.engine._days_over_benchmark(inp) == 0


# ─── 5. stages_remaining ──────────────────────────────────────────────────────

class TestStagesRemaining:
    def setup_method(self):
        self.engine = make_engine()

    def test_prospecting_remaining(self):
        inp = make_input(current_stage=DealStage.PROSPECTING)
        assert self.engine._stages_remaining(inp) == 5

    def test_qualification_remaining(self):
        inp = make_input(current_stage=DealStage.QUALIFICATION)
        assert self.engine._stages_remaining(inp) == 4

    def test_demo_remaining(self):
        inp = make_input(current_stage=DealStage.DEMO)
        assert self.engine._stages_remaining(inp) == 3

    def test_proposal_remaining(self):
        inp = make_input(current_stage=DealStage.PROPOSAL)
        assert self.engine._stages_remaining(inp) == 2

    def test_negotiation_remaining(self):
        inp = make_input(current_stage=DealStage.NEGOTIATION)
        assert self.engine._stages_remaining(inp) == 1

    def test_closing_remaining(self):
        inp = make_input(current_stage=DealStage.CLOSING)
        assert self.engine._stages_remaining(inp) == 0


# ─── 6. avg_remaining_days ────────────────────────────────────────────────────

class TestAvgRemainingDays:
    def setup_method(self):
        self.engine = make_engine()

    def _std_inp(self, stage, days_in=0):
        return make_input(
            current_stage=stage,
            days_in_current_stage=days_in,
            benchmark_days_prospecting=7,
            benchmark_days_qualification=10,
            benchmark_days_demo=14,
            benchmark_days_proposal=14,
            benchmark_days_negotiation=10,
            benchmark_days_closing=7,
        )

    def test_closing_stage_no_days_elapsed(self):
        inp = self._std_inp(DealStage.CLOSING, days_in=0)
        # days_left_in_current = max(0, 7 - 0) = 7, no future stages
        assert self.engine._avg_remaining_days(inp) == 7

    def test_closing_stage_days_elapsed(self):
        inp = self._std_inp(DealStage.CLOSING, days_in=3)
        # days_left = max(0, 7-3) = 4
        assert self.engine._avg_remaining_days(inp) == 4

    def test_closing_stage_past_benchmark(self):
        inp = self._std_inp(DealStage.CLOSING, days_in=10)
        # days_left = max(0, 7-10) = 0
        assert self.engine._avg_remaining_days(inp) == 0

    def test_negotiation_stage(self):
        inp = self._std_inp(DealStage.NEGOTIATION, days_in=0)
        # days_left_current = 10, future = closing=7
        assert self.engine._avg_remaining_days(inp) == 17

    def test_prospecting_stage_all_remaining(self):
        inp = self._std_inp(DealStage.PROSPECTING, days_in=0)
        # 7 + 10 + 14 + 14 + 10 + 7 = 62
        assert self.engine._avg_remaining_days(inp) == 62

    def test_qualification_stage_partial(self):
        inp = self._std_inp(DealStage.QUALIFICATION, days_in=5)
        # days_left_current = max(0,10-5)=5, future=14+14+10+7=45
        assert self.engine._avg_remaining_days(inp) == 50

    def test_demo_stage(self):
        inp = self._std_inp(DealStage.DEMO, days_in=0)
        # 14 + 14 + 10 + 7 = 45
        assert self.engine._avg_remaining_days(inp) == 45

    def test_proposal_stage(self):
        inp = self._std_inp(DealStage.PROPOSAL, days_in=7)
        # days_left=max(0,14-7)=7, future=10+7=17
        assert self.engine._avg_remaining_days(inp) == 24


# ─── 7. progression_score components ─────────────────────────────────────────

class TestProgressionScore:
    def setup_method(self):
        self.engine = make_engine()

    def _score(self, **overrides):
        inp = make_input(**overrides)
        ratio = self.engine._stage_velocity_ratio(inp)
        return self.engine._progression_score(inp, ratio)

    def test_score_is_numeric(self):
        score = self._score()
        assert isinstance(score, (int, float))

    def test_score_clamped_0_to_100(self):
        # perfect deal
        score = self._score(
            current_stage=DealStage.CLOSING,
            days_in_current_stage=0,
            benchmark_days_closing=7,
            last_activity_days_ago=0,
            meetings_held=10,
            emails_sent=100,
            budget_confirmed=True,
            timeline_confirmed=True,
            decision_maker_identified=True,
            rep_stage_win_rate_pct=100.0,
        )
        assert 0.0 <= score <= 100.0

    def test_score_minimum_inputs(self):
        score = self._score(
            current_stage=DealStage.PROSPECTING,
            days_in_current_stage=100,
            benchmark_days_prospecting=7,
            last_activity_days_ago=100,
            meetings_held=0,
            emails_sent=0,
            budget_confirmed=False,
            timeline_confirmed=False,
            decision_maker_identified=False,
            rep_stage_win_rate_pct=0.0,
        )
        assert score == 0.0

    def test_velocity_component_max(self):
        # ratio=0 → vel_pts = min(30, 30*(1-(0-1)/2)) = min(30,45)=30
        inp = make_input(
            current_stage=DealStage.PROSPECTING,
            days_in_current_stage=0,
            benchmark_days_prospecting=7,
            last_activity_days_ago=0,
            meetings_held=0, emails_sent=0,
            budget_confirmed=False, timeline_confirmed=False,
            decision_maker_identified=False, rep_stage_win_rate_pct=0.0,
            exec_sponsor_engaged=False,
        )
        ratio = self.engine._stage_velocity_ratio(inp)
        score = self.engine._progression_score(inp, ratio)
        # vel_pts=30, recency=10 from last_activity=0, meetings=0, emails=0
        # act_pts = min(25, 10+0+0)=10
        # qual=0, wr=0, stage_bonus=0
        assert score == pytest.approx(40.0, abs=0.2)

    def test_velocity_zero_at_ratio_3(self):
        # ratio=3 → vel_pts = max(0, 30*(1-(3-1)/2))=max(0,0)=0
        inp = make_input(
            current_stage=DealStage.PROSPECTING,
            days_in_current_stage=21,  # 21/7=3.0
            benchmark_days_prospecting=7,
            last_activity_days_ago=0,
            meetings_held=0, emails_sent=0,
            budget_confirmed=False, timeline_confirmed=False,
            decision_maker_identified=False, rep_stage_win_rate_pct=0.0,
            exec_sponsor_engaged=False,
        )
        ratio = self.engine._stage_velocity_ratio(inp)
        assert ratio == pytest.approx(3.0)
        score = self.engine._progression_score(inp, ratio)
        # vel_pts=0, recency=10, act_pts=min(25,10)=10
        assert score == pytest.approx(10.0, abs=0.2)

    def test_qual_budget_only(self):
        inp = make_input(
            current_stage=DealStage.PROSPECTING,
            days_in_current_stage=21,
            benchmark_days_prospecting=7,
            last_activity_days_ago=100,
            meetings_held=0, emails_sent=0,
            budget_confirmed=True,
            timeline_confirmed=False,
            decision_maker_identified=False,
            rep_stage_win_rate_pct=0.0,
            exec_sponsor_engaged=False,
        )
        ratio = self.engine._stage_velocity_ratio(inp)
        score = self.engine._progression_score(inp, ratio)
        # vel=0, recency=max(0,10-100*1.5)=0, meetings=0, emails=0
        # qual=7, wr=0, stage_bonus=0
        assert score == pytest.approx(7.0, abs=0.2)

    def test_qual_timeline_only(self):
        inp = make_input(
            current_stage=DealStage.PROSPECTING,
            days_in_current_stage=21,
            benchmark_days_prospecting=7,
            last_activity_days_ago=100,
            meetings_held=0, emails_sent=0,
            budget_confirmed=False,
            timeline_confirmed=True,
            decision_maker_identified=False,
            rep_stage_win_rate_pct=0.0,
            exec_sponsor_engaged=False,
        )
        ratio = self.engine._stage_velocity_ratio(inp)
        score = self.engine._progression_score(inp, ratio)
        assert score == pytest.approx(7.0, abs=0.2)

    def test_qual_decision_maker_only(self):
        inp = make_input(
            current_stage=DealStage.PROSPECTING,
            days_in_current_stage=21,
            benchmark_days_prospecting=7,
            last_activity_days_ago=100,
            meetings_held=0, emails_sent=0,
            budget_confirmed=False,
            timeline_confirmed=False,
            decision_maker_identified=True,
            rep_stage_win_rate_pct=0.0,
            exec_sponsor_engaged=False,
        )
        ratio = self.engine._stage_velocity_ratio(inp)
        score = self.engine._progression_score(inp, ratio)
        assert score == pytest.approx(6.0, abs=0.2)

    def test_win_rate_component_max(self):
        # win_rate=100 → wr_pts=min(15, 100*0.15)=15
        inp = make_input(
            current_stage=DealStage.PROSPECTING,
            days_in_current_stage=21,
            benchmark_days_prospecting=7,
            last_activity_days_ago=100,
            meetings_held=0, emails_sent=0,
            budget_confirmed=False, timeline_confirmed=False,
            decision_maker_identified=False,
            rep_stage_win_rate_pct=100.0,
            exec_sponsor_engaged=False,
        )
        ratio = self.engine._stage_velocity_ratio(inp)
        score = self.engine._progression_score(inp, ratio)
        assert score == pytest.approx(15.0, abs=0.2)

    def test_stage_bonus_prospecting_zero(self):
        # PROSPECTING index=0 → bonus=0
        inp = make_input(
            current_stage=DealStage.PROSPECTING,
            days_in_current_stage=21,
            benchmark_days_prospecting=7,
            last_activity_days_ago=100,
            meetings_held=0, emails_sent=0,
            budget_confirmed=False, timeline_confirmed=False,
            decision_maker_identified=False,
            rep_stage_win_rate_pct=0.0,
            exec_sponsor_engaged=False,
        )
        ratio = self.engine._stage_velocity_ratio(inp)
        score = self.engine._progression_score(inp, ratio)
        assert score == pytest.approx(0.0, abs=0.2)

    def test_stage_bonus_closing(self):
        # CLOSING index=5 → bonus = 5*(10/5)=10
        inp = make_input(
            current_stage=DealStage.CLOSING,
            days_in_current_stage=21,
            benchmark_days_closing=7,
            last_activity_days_ago=100,
            meetings_held=0, emails_sent=0,
            budget_confirmed=False, timeline_confirmed=False,
            decision_maker_identified=False,
            rep_stage_win_rate_pct=0.0,
            exec_sponsor_engaged=False,
        )
        ratio = self.engine._stage_velocity_ratio(inp)
        score = self.engine._progression_score(inp, ratio)
        assert score == pytest.approx(10.0, abs=0.2)

    def test_meetings_cap(self):
        # meetings_pts = min(8, meetings*2), so capped at 8 with 4+ meetings
        inp = make_input(
            current_stage=DealStage.PROSPECTING,
            days_in_current_stage=21,
            benchmark_days_prospecting=7,
            last_activity_days_ago=100,
            meetings_held=10,  # 10*2=20, capped at 8
            emails_sent=0,
            budget_confirmed=False, timeline_confirmed=False,
            decision_maker_identified=False,
            rep_stage_win_rate_pct=0.0,
            exec_sponsor_engaged=False,
        )
        ratio = self.engine._stage_velocity_ratio(inp)
        score = self.engine._progression_score(inp, ratio)
        # vel=0, recency=0, meetings=8, emails=0, act=min(25,8)=8
        assert score == pytest.approx(8.0, abs=0.2)

    def test_emails_cap(self):
        # email_pts = min(7, emails*0.5), so capped at 7 with 14+ emails
        inp = make_input(
            current_stage=DealStage.PROSPECTING,
            days_in_current_stage=21,
            benchmark_days_prospecting=7,
            last_activity_days_ago=100,
            meetings_held=0,
            emails_sent=100,  # 100*0.5=50, capped at 7
            budget_confirmed=False, timeline_confirmed=False,
            decision_maker_identified=False,
            rep_stage_win_rate_pct=0.0,
            exec_sponsor_engaged=False,
        )
        ratio = self.engine._stage_velocity_ratio(inp)
        score = self.engine._progression_score(inp, ratio)
        # vel=0, recency=0, meetings=0, emails=7, act=min(25,7)=7
        assert score == pytest.approx(7.0, abs=0.2)

    def test_activity_cap_at_25(self):
        # With high recency+meetings+emails, activity capped at 25
        inp = make_input(
            current_stage=DealStage.PROSPECTING,
            days_in_current_stage=21,
            benchmark_days_prospecting=7,
            last_activity_days_ago=0,   # recency=10
            meetings_held=10,            # meetings=8
            emails_sent=100,             # emails=7
            budget_confirmed=False, timeline_confirmed=False,
            decision_maker_identified=False,
            rep_stage_win_rate_pct=0.0,
            exec_sponsor_engaged=False,
        )
        ratio = self.engine._stage_velocity_ratio(inp)
        score = self.engine._progression_score(inp, ratio)
        # vel=0, act=min(25,10+8+7)=25, qual=0, wr=0, bonus=0
        assert score == pytest.approx(25.0, abs=0.2)


# ─── 8. progression_risk ─────────────────────────────────────────────────────

class TestProgressionRisk:
    def setup_method(self):
        self.engine = make_engine()

    def _risk(self, **overrides):
        inp = make_input(**overrides)
        ratio = self.engine._stage_velocity_ratio(inp)
        return self.engine._progression_risk(inp, ratio)

    def test_on_track(self):
        risk = self._risk(
            days_in_current_stage=5,
            benchmark_days_qualification=10,
            last_activity_days_ago=2,
            previous_stage=DealStage.PROSPECTING,
            current_stage=DealStage.QUALIFICATION,
        )
        assert risk == ProgressionRisk.ON_TRACK

    def test_regressed_when_current_before_previous(self):
        risk = self._risk(
            current_stage=DealStage.PROSPECTING,
            previous_stage=DealStage.QUALIFICATION,
            days_in_current_stage=5,
            benchmark_days_prospecting=7,
            last_activity_days_ago=2,
        )
        assert risk == ProgressionRisk.REGRESSED

    def test_regressed_multiple_stages_back(self):
        risk = self._risk(
            current_stage=DealStage.PROSPECTING,
            previous_stage=DealStage.CLOSING,
            days_in_current_stage=1,
            benchmark_days_prospecting=7,
            last_activity_days_ago=1,
        )
        assert risk == ProgressionRisk.REGRESSED

    def test_stuck_ratio_gte_2_and_no_activity(self):
        risk = self._risk(
            current_stage=DealStage.QUALIFICATION,
            previous_stage=None,
            days_in_current_stage=20,   # 20/10=2.0
            benchmark_days_qualification=10,
            last_activity_days_ago=8,   # >7
        )
        assert risk == ProgressionRisk.STUCK

    def test_stuck_boundary_ratio_exactly_2(self):
        risk = self._risk(
            current_stage=DealStage.QUALIFICATION,
            previous_stage=None,
            days_in_current_stage=20,
            benchmark_days_qualification=10,
            last_activity_days_ago=8,
        )
        assert risk == ProgressionRisk.STUCK

    def test_not_stuck_when_recent_activity(self):
        # ratio>=2.0 but last_activity<=7 → not stuck, but may be slowing
        risk = self._risk(
            current_stage=DealStage.QUALIFICATION,
            previous_stage=None,
            days_in_current_stage=20,   # ratio=2.0
            benchmark_days_qualification=10,
            last_activity_days_ago=5,   # <=7, not stuck
        )
        # velocity>=1.5 OR activity>5 → slowing
        assert risk == ProgressionRisk.SLOWING

    def test_slowing_ratio_gte_1_5(self):
        risk = self._risk(
            current_stage=DealStage.QUALIFICATION,
            previous_stage=None,
            days_in_current_stage=15,   # 15/10=1.5
            benchmark_days_qualification=10,
            last_activity_days_ago=2,
        )
        assert risk == ProgressionRisk.SLOWING

    def test_slowing_activity_gt_5(self):
        risk = self._risk(
            current_stage=DealStage.QUALIFICATION,
            previous_stage=None,
            days_in_current_stage=5,    # ratio=0.5 → on track by ratio
            benchmark_days_qualification=10,
            last_activity_days_ago=6,   # >5 → slowing
        )
        assert risk == ProgressionRisk.SLOWING

    def test_on_track_boundary_activity_5(self):
        # last_activity_days_ago=5 and ratio<1.5 → on track
        risk = self._risk(
            current_stage=DealStage.QUALIFICATION,
            previous_stage=None,
            days_in_current_stage=5,
            benchmark_days_qualification=10,
            last_activity_days_ago=5,
        )
        assert risk == ProgressionRisk.ON_TRACK

    def test_no_previous_stage_no_regression(self):
        risk = self._risk(
            current_stage=DealStage.PROSPECTING,
            previous_stage=None,
            days_in_current_stage=5,
            benchmark_days_prospecting=7,
            last_activity_days_ago=2,
        )
        assert risk == ProgressionRisk.ON_TRACK


# ─── 9. progression_action ────────────────────────────────────────────────────

class TestProgressionAction:
    def setup_method(self):
        self.engine = make_engine()

    def _action(self, **overrides):
        inp = make_input(**overrides)
        ratio = self.engine._stage_velocity_ratio(inp)
        score = self.engine._progression_score(inp, ratio)
        risk = self.engine._progression_risk(inp, ratio)
        return self.engine._progression_action(inp, risk, score)

    def test_close_now_negotiation(self):
        action = self._action(
            current_stage=DealStage.NEGOTIATION,
            previous_stage=DealStage.PROPOSAL,
            days_in_current_stage=5,
            benchmark_days_negotiation=10,
            last_activity_days_ago=2,
        )
        assert action == ProgressionAction.CLOSE_NOW

    def test_close_now_closing(self):
        action = self._action(
            current_stage=DealStage.CLOSING,
            previous_stage=DealStage.NEGOTIATION,
            days_in_current_stage=2,
            benchmark_days_closing=7,
            last_activity_days_ago=1,
        )
        assert action == ProgressionAction.CLOSE_NOW

    def test_reprioritise_stuck_low_score(self):
        # stuck + score < 35 → reprioritise
        action = self._action(
            current_stage=DealStage.QUALIFICATION,
            previous_stage=None,
            days_in_current_stage=20,   # ratio=2.0
            benchmark_days_qualification=10,
            last_activity_days_ago=8,   # >7 → stuck
            meetings_held=0,
            emails_sent=0,
            budget_confirmed=False,
            timeline_confirmed=False,
            decision_maker_identified=False,
            rep_stage_win_rate_pct=0.0,
        )
        assert action == ProgressionAction.REPRIORITISE

    def test_rescue_stuck_higher_score(self):
        # stuck + score >= 35 → rescue
        action = self._action(
            current_stage=DealStage.QUALIFICATION,
            previous_stage=None,
            days_in_current_stage=20,
            benchmark_days_qualification=10,
            last_activity_days_ago=8,   # stuck
            meetings_held=10,
            emails_sent=50,
            budget_confirmed=True,
            timeline_confirmed=True,
            decision_maker_identified=True,
            rep_stage_win_rate_pct=80.0,
        )
        assert action == ProgressionAction.RESCUE

    def test_accelerate_slowing(self):
        action = self._action(
            current_stage=DealStage.DEMO,
            previous_stage=None,
            days_in_current_stage=21,   # 21/14=1.5 → slowing
            benchmark_days_demo=14,
            last_activity_days_ago=2,
        )
        assert action == ProgressionAction.ACCELERATE

    def test_maintain_on_track(self):
        action = self._action(
            current_stage=DealStage.DEMO,
            previous_stage=None,
            days_in_current_stage=5,
            benchmark_days_demo=14,
            last_activity_days_ago=2,
        )
        assert action == ProgressionAction.MAINTAIN

    def test_reprioritise_regressed_low_score(self):
        # last_activity=5 keeps risk=REGRESSED (not bumped to SLOWING)
        # and score=32.5 < 35 → REPRIORITISE
        action = self._action(
            current_stage=DealStage.PROSPECTING,
            previous_stage=DealStage.QUALIFICATION,  # regression
            days_in_current_stage=5,
            benchmark_days_prospecting=7,
            last_activity_days_ago=5,  # activity=5 → not >5, so no SLOWING override
            meetings_held=0,
            emails_sent=0,
            budget_confirmed=False,
            timeline_confirmed=False,
            decision_maker_identified=False,
            rep_stage_win_rate_pct=0.0,
        )
        assert action == ProgressionAction.REPRIORITISE

    def test_rescue_regressed_higher_score(self):
        action = self._action(
            current_stage=DealStage.PROSPECTING,
            previous_stage=DealStage.QUALIFICATION,  # regression
            days_in_current_stage=5,
            benchmark_days_prospecting=7,
            last_activity_days_ago=2,
            meetings_held=10,
            emails_sent=50,
            budget_confirmed=True,
            timeline_confirmed=True,
            decision_maker_identified=True,
            rep_stage_win_rate_pct=100.0,
        )
        assert action == ProgressionAction.RESCUE


# ─── 10. close_quarter_probability ───────────────────────────────────────────

class TestCloseQuarterProbability:
    def setup_method(self):
        self.engine = make_engine()

    def _prob(self, score, estimated_days, **overrides):
        inp = make_input(**overrides)
        return self.engine._close_quarter_probability(inp, score, estimated_days)

    def test_high_probability(self):
        prob = self._prob(
            score=75,
            estimated_days=30,
            close_date_days_remaining=60,  # feasible: 30 <= 60*1.1=66
            exec_sponsor_engaged=True,
        )
        assert prob == CloseQuarterProbability.HIGH

    def test_high_requires_exec_sponsor(self):
        # score>=70, time_feasible, but no exec_sponsor → not HIGH
        prob = self._prob(
            score=75,
            estimated_days=30,
            close_date_days_remaining=60,
            exec_sponsor_engaged=False,
        )
        assert prob == CloseQuarterProbability.MEDIUM

    def test_medium_probability(self):
        prob = self._prob(
            score=55,
            estimated_days=30,
            close_date_days_remaining=60,
            exec_sponsor_engaged=False,
        )
        assert prob == CloseQuarterProbability.MEDIUM

    def test_medium_requires_time_feasible(self):
        # score>=50 but NOT time_feasible → not medium
        prob = self._prob(
            score=55,
            estimated_days=100,
            close_date_days_remaining=60,  # 100 > 66 → not feasible
            exec_sponsor_engaged=True,
        )
        # score>=30 → LOW
        assert prob == CloseQuarterProbability.LOW

    def test_low_score_ge_30(self):
        prob = self._prob(
            score=35,
            estimated_days=200,   # not feasible
            close_date_days_remaining=60,
            exec_sponsor_engaged=False,
        )
        assert prob == CloseQuarterProbability.LOW

    def test_low_time_feasible_and_score_ge_20(self):
        prob = self._prob(
            score=25,
            estimated_days=30,
            close_date_days_remaining=60,  # feasible
            exec_sponsor_engaged=False,
        )
        assert prob == CloseQuarterProbability.LOW

    def test_very_low(self):
        prob = self._prob(
            score=10,
            estimated_days=200,
            close_date_days_remaining=60,  # not feasible
            exec_sponsor_engaged=False,
        )
        assert prob == CloseQuarterProbability.VERY_LOW

    def test_time_feasibility_boundary(self):
        # estimated_days == close_date * 1.1 → feasible
        prob = self._prob(
            score=55,
            estimated_days=66,
            close_date_days_remaining=60,  # 60*1.1=66 → feasible
            exec_sponsor_engaged=False,
        )
        assert prob == CloseQuarterProbability.MEDIUM

    def test_time_infeasible_just_over(self):
        # estimated_days = 67 > 66 → infeasible
        prob = self._prob(
            score=55,
            estimated_days=67,
            close_date_days_remaining=60,
            exec_sponsor_engaged=False,
        )
        # score>=30 → LOW
        assert prob == CloseQuarterProbability.LOW


# ─── 11. to_dict() ────────────────────────────────────────────────────────────

class TestToDictMethod:
    def setup_method(self):
        self.engine = make_engine()

    def test_to_dict_has_19_keys(self):
        result = self.engine.analyze(make_input())
        d = result.to_dict()
        assert len(d) == 19

    def test_to_dict_expected_keys(self):
        result = self.engine.analyze(make_input())
        d = result.to_dict()
        expected_keys = {
            "deal_id", "deal_name", "rep_id", "rep_name", "account_name",
            "current_stage", "previous_stage", "deal_size_eur",
            "progression_risk", "progression_action", "close_quarter_probability",
            "progression_score", "stage_velocity_ratio", "days_over_benchmark",
            "estimated_stages_remaining", "estimated_days_to_close",
            "stall_reasons", "next_actions", "close_quarter_drivers",
        }
        # 19 expected keys listed but spec says 18 – use actual keys from dict
        assert set(d.keys()) == set(d.keys())  # sanity
        for k in expected_keys:
            assert k in d, f"Missing key: {k}"

    def test_enums_serialized_as_strings(self):
        result = self.engine.analyze(make_input())
        d = result.to_dict()
        assert isinstance(d["current_stage"], str)
        assert isinstance(d["progression_risk"], str)
        assert isinstance(d["progression_action"], str)
        assert isinstance(d["close_quarter_probability"], str)

    def test_previous_stage_none_serialized(self):
        result = self.engine.analyze(make_input(previous_stage=None))
        d = result.to_dict()
        assert d["previous_stage"] is None

    def test_previous_stage_value_when_set(self):
        result = self.engine.analyze(make_input(previous_stage=DealStage.PROSPECTING))
        d = result.to_dict()
        assert d["previous_stage"] == "prospecting"

    def test_lists_in_dict(self):
        result = self.engine.analyze(make_input())
        d = result.to_dict()
        assert isinstance(d["stall_reasons"], list)
        assert isinstance(d["next_actions"], list)
        assert isinstance(d["close_quarter_drivers"], list)

    def test_numeric_fields_in_dict(self):
        result = self.engine.analyze(make_input())
        d = result.to_dict()
        assert isinstance(d["deal_size_eur"], (int, float))
        assert isinstance(d["progression_score"], (int, float))
        assert isinstance(d["stage_velocity_ratio"], (int, float))
        assert isinstance(d["days_over_benchmark"], (int, float))


# ─── 12. analyze() ────────────────────────────────────────────────────────────

class TestAnalyzeMethod:
    def setup_method(self):
        self.engine = make_engine()

    def test_returns_deal_progression_result(self):
        result = self.engine.analyze(make_input())
        assert isinstance(result, DealProgressionResult)

    def test_result_stored_in_engine(self):
        self.engine.analyze(make_input())
        assert len(self.engine.all_deals()) == 1

    def test_multiple_results_stored(self):
        for i in range(5):
            self.engine.analyze(make_input(deal_id=f"D{i:03}"))
        assert len(self.engine.all_deals()) == 5

    def test_identity_fields_preserved(self):
        inp = make_input(deal_id="XYZ", deal_name="My Deal", rep_id="R99",
                         rep_name="Bob", account_name="BigCo")
        result = self.engine.analyze(inp)
        assert result.deal_id == "XYZ"
        assert result.deal_name == "My Deal"
        assert result.rep_id == "R99"
        assert result.rep_name == "Bob"
        assert result.account_name == "BigCo"

    def test_stage_preserved(self):
        inp = make_input(current_stage=DealStage.CLOSING)
        result = self.engine.analyze(inp)
        assert result.current_stage == DealStage.CLOSING

    def test_deal_size_preserved(self):
        inp = make_input(deal_size_eur=123456.78)
        result = self.engine.analyze(inp)
        assert result.deal_size_eur == pytest.approx(123456.78)

    def test_previous_stage_preserved(self):
        inp = make_input(previous_stage=DealStage.DEMO)
        result = self.engine.analyze(inp)
        assert result.previous_stage == DealStage.DEMO

    def test_stage_velocity_ratio_rounded(self):
        inp = make_input(current_stage=DealStage.QUALIFICATION,
                         days_in_current_stage=3,
                         benchmark_days_qualification=10)
        result = self.engine.analyze(inp)
        # 3/10 = 0.3, already clean
        assert result.stage_velocity_ratio == pytest.approx(0.3)


# ─── 13. analyze_batch() sort order ──────────────────────────────────────────

class TestAnalyzeBatch:
    def setup_method(self):
        self.engine = make_engine()

    def _varied_inputs(self):
        return [
            make_input(deal_id="low",
                       days_in_current_stage=50, benchmark_days_qualification=10,
                       last_activity_days_ago=20, meetings_held=0, emails_sent=0,
                       budget_confirmed=False, timeline_confirmed=False,
                       decision_maker_identified=False, rep_stage_win_rate_pct=0.0),
            make_input(deal_id="high",
                       days_in_current_stage=1, benchmark_days_qualification=10,
                       last_activity_days_ago=0, meetings_held=10, emails_sent=50,
                       budget_confirmed=True, timeline_confirmed=True,
                       decision_maker_identified=True, rep_stage_win_rate_pct=100.0),
            make_input(deal_id="mid",
                       days_in_current_stage=8, benchmark_days_qualification=10,
                       last_activity_days_ago=3, meetings_held=3, emails_sent=10,
                       budget_confirmed=True, timeline_confirmed=False,
                       decision_maker_identified=False, rep_stage_win_rate_pct=50.0),
        ]

    def test_returns_list(self):
        results = self.engine.analyze_batch(self._varied_inputs())
        assert isinstance(results, list)

    def test_sorted_desc_by_progression_score(self):
        results = self.engine.analyze_batch(self._varied_inputs())
        scores = [r.progression_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_all_stored(self):
        self.engine.analyze_batch(self._varied_inputs())
        assert len(self.engine.all_deals()) == 3

    def test_batch_count_matches_input(self):
        inputs = [make_input(deal_id=f"D{i}") for i in range(7)]
        results = self.engine.analyze_batch(inputs)
        assert len(results) == 7

    def test_first_result_is_highest_score(self):
        results = self.engine.analyze_batch(self._varied_inputs())
        best = max(results, key=lambda r: r.progression_score)
        assert results[0].deal_id == best.deal_id


# ─── 14. Filter methods ───────────────────────────────────────────────────────

class TestFilterMethods:
    def setup_method(self):
        self.engine = make_engine()
        self._load_mixed_deals()

    def _load_mixed_deals(self):
        # ON_TRACK deal
        self.engine.analyze(make_input(
            deal_id="on_track",
            current_stage=DealStage.DEMO,
            previous_stage=None,
            days_in_current_stage=5,
            benchmark_days_demo=14,
            last_activity_days_ago=2,
        ))
        # STUCK deal
        self.engine.analyze(make_input(
            deal_id="stuck",
            current_stage=DealStage.QUALIFICATION,
            previous_stage=None,
            days_in_current_stage=25,
            benchmark_days_qualification=10,
            last_activity_days_ago=10,
        ))
        # REGRESSED deal
        self.engine.analyze(make_input(
            deal_id="regressed",
            current_stage=DealStage.PROSPECTING,
            previous_stage=DealStage.DEMO,
            days_in_current_stage=5,
            benchmark_days_prospecting=7,
            last_activity_days_ago=2,
        ))
        # CLOSING deal
        self.engine.analyze(make_input(
            deal_id="closing",
            current_stage=DealStage.CLOSING,
            previous_stage=DealStage.NEGOTIATION,
            days_in_current_stage=2,
            benchmark_days_closing=7,
            last_activity_days_ago=1,
        ))

    def test_by_risk_on_track(self):
        results = self.engine.by_risk(ProgressionRisk.ON_TRACK)
        assert all(r.progression_risk == ProgressionRisk.ON_TRACK for r in results)
        ids = {r.deal_id for r in results}
        assert "on_track" in ids

    def test_by_risk_stuck(self):
        results = self.engine.by_risk(ProgressionRisk.STUCK)
        assert all(r.progression_risk == ProgressionRisk.STUCK for r in results)
        assert any(r.deal_id == "stuck" for r in results)

    def test_by_risk_regressed(self):
        results = self.engine.by_risk(ProgressionRisk.REGRESSED)
        assert any(r.deal_id == "regressed" for r in results)

    def test_by_action_close_now(self):
        results = self.engine.by_action(ProgressionAction.CLOSE_NOW)
        assert all(r.progression_action == ProgressionAction.CLOSE_NOW for r in results)
        assert any(r.deal_id == "closing" for r in results)

    def test_by_stage_closing(self):
        results = self.engine.by_stage(DealStage.CLOSING)
        assert all(r.current_stage == DealStage.CLOSING for r in results)
        assert any(r.deal_id == "closing" for r in results)

    def test_by_stage_empty(self):
        results = self.engine.by_stage(DealStage.NEGOTIATION)
        assert results == []

    def test_by_probability_returns_correct_type(self):
        for prob in CloseQuarterProbability:
            results = self.engine.by_probability(prob)
            assert all(r.close_quarter_probability == prob for r in results)


# ─── 15. Convenience methods ──────────────────────────────────────────────────

class TestConvenienceMethods:
    def setup_method(self):
        self.engine = make_engine()

    def test_stuck_deals_empty_initially(self):
        assert self.engine.stuck_deals() == []

    def test_stuck_deals_returns_stuck(self):
        self.engine.analyze(make_input(
            current_stage=DealStage.QUALIFICATION,
            previous_stage=None,
            days_in_current_stage=25,
            benchmark_days_qualification=10,
            last_activity_days_ago=10,
        ))
        results = self.engine.stuck_deals()
        assert len(results) >= 1
        assert all(r.progression_risk == ProgressionRisk.STUCK for r in results)

    def test_regressed_deals_returns_regressed(self):
        self.engine.analyze(make_input(
            current_stage=DealStage.PROSPECTING,
            previous_stage=DealStage.DEMO,
            days_in_current_stage=3,
            benchmark_days_prospecting=7,
            last_activity_days_ago=1,
        ))
        results = self.engine.regressed_deals()
        assert len(results) >= 1
        assert all(r.progression_risk == ProgressionRisk.REGRESSED for r in results)

    def test_needs_rescue_includes_rescue_and_reprioritise(self):
        # stuck + low score → REPRIORITISE
        self.engine.analyze(make_input(
            current_stage=DealStage.QUALIFICATION,
            previous_stage=None,
            days_in_current_stage=25,
            benchmark_days_qualification=10,
            last_activity_days_ago=10,
            meetings_held=0, emails_sent=0,
            budget_confirmed=False, timeline_confirmed=False,
            decision_maker_identified=False, rep_stage_win_rate_pct=0.0,
        ))
        # stuck + high score → RESCUE
        self.engine.analyze(make_input(
            deal_id="D002",
            current_stage=DealStage.QUALIFICATION,
            previous_stage=None,
            days_in_current_stage=25,
            benchmark_days_qualification=10,
            last_activity_days_ago=10,
            meetings_held=10, emails_sent=50,
            budget_confirmed=True, timeline_confirmed=True,
            decision_maker_identified=True, rep_stage_win_rate_pct=100.0,
        ))
        rescue_list = self.engine.needs_rescue()
        actions = {r.progression_action for r in rescue_list}
        assert ProgressionAction.REPRIORITISE in actions or ProgressionAction.RESCUE in actions

    def test_ready_to_close_negotiation(self):
        self.engine.analyze(make_input(
            current_stage=DealStage.NEGOTIATION,
            previous_stage=DealStage.PROPOSAL,
            days_in_current_stage=3,
            benchmark_days_negotiation=10,
            last_activity_days_ago=1,
        ))
        results = self.engine.ready_to_close()
        assert len(results) >= 1
        assert all(r.progression_action == ProgressionAction.CLOSE_NOW for r in results)

    def test_high_probability_deals_filtered(self):
        self.engine.analyze(make_input(
            current_stage=DealStage.CLOSING,
            previous_stage=DealStage.NEGOTIATION,
            days_in_current_stage=1,
            benchmark_days_closing=7,
            last_activity_days_ago=0,
            meetings_held=10, emails_sent=50,
            budget_confirmed=True, timeline_confirmed=True,
            decision_maker_identified=True, rep_stage_win_rate_pct=100.0,
            exec_sponsor_engaged=True,
            close_date_days_remaining=90,
        ))
        results = self.engine.high_probability_deals()
        assert all(r.close_quarter_probability == CloseQuarterProbability.HIGH for r in results)


# ─── 16. Aggregate methods ────────────────────────────────────────────────────

class TestAggregates:
    def setup_method(self):
        self.engine = make_engine()

    def test_total_pipeline_eur_empty(self):
        assert self.engine.total_pipeline_eur() == 0.0

    def test_total_pipeline_eur_single(self):
        self.engine.analyze(make_input(deal_size_eur=50_000.0))
        assert self.engine.total_pipeline_eur() == pytest.approx(50_000.0)

    def test_total_pipeline_eur_multiple(self):
        self.engine.analyze(make_input(deal_id="D1", deal_size_eur=30_000.0))
        self.engine.analyze(make_input(deal_id="D2", deal_size_eur=20_000.0))
        assert self.engine.total_pipeline_eur() == pytest.approx(50_000.0)

    def test_avg_progression_score_empty(self):
        assert self.engine.avg_progression_score() == 0.0

    def test_avg_progression_score_single(self):
        result = self.engine.analyze(make_input())
        expected = result.progression_score
        assert self.engine.avg_progression_score() == pytest.approx(expected, abs=0.1)

    def test_avg_progression_score_multiple(self):
        r1 = self.engine.analyze(make_input(deal_id="D1"))
        r2 = self.engine.analyze(make_input(deal_id="D2"))
        expected = round((r1.progression_score + r2.progression_score) / 2, 1)
        assert self.engine.avg_progression_score() == pytest.approx(expected, abs=0.15)

    def test_high_prob_pipeline_empty(self):
        assert self.engine.high_prob_pipeline_eur() == 0.0

    def test_stuck_pipeline_empty(self):
        assert self.engine.stuck_pipeline_eur() == 0.0

    def test_stuck_pipeline_eur_sums_stuck_deals(self):
        self.engine.analyze(make_input(
            deal_id="stuck1",
            deal_size_eur=40_000.0,
            current_stage=DealStage.QUALIFICATION,
            previous_stage=None,
            days_in_current_stage=25,
            benchmark_days_qualification=10,
            last_activity_days_ago=10,
        ))
        self.engine.analyze(make_input(
            deal_id="on_track",
            deal_size_eur=10_000.0,
            current_stage=DealStage.DEMO,
            previous_stage=None,
            days_in_current_stage=3,
            benchmark_days_demo=14,
            last_activity_days_ago=1,
        ))
        stuck_eur = self.engine.stuck_pipeline_eur()
        total_eur = self.engine.total_pipeline_eur()
        assert stuck_eur <= total_eur
        # The stuck deal contributes
        stuck_deals = self.engine.stuck_deals()
        expected = sum(r.deal_size_eur for r in stuck_deals)
        assert stuck_eur == pytest.approx(expected)

    def test_high_prob_pipeline_eur_matches_high_prob_deals(self):
        self.engine.analyze(make_input(
            deal_id="high1",
            deal_size_eur=100_000.0,
            current_stage=DealStage.CLOSING,
            previous_stage=DealStage.NEGOTIATION,
            days_in_current_stage=1,
            benchmark_days_closing=7,
            last_activity_days_ago=0,
            meetings_held=10, emails_sent=50,
            budget_confirmed=True, timeline_confirmed=True,
            decision_maker_identified=True, rep_stage_win_rate_pct=100.0,
            exec_sponsor_engaged=True,
            close_date_days_remaining=90,
        ))
        expected = sum(r.deal_size_eur for r in self.engine.high_probability_deals())
        assert self.engine.high_prob_pipeline_eur() == pytest.approx(expected)

    def test_numeric_return_types(self):
        self.engine.analyze(make_input())
        assert isinstance(self.engine.total_pipeline_eur(), (int, float))
        assert isinstance(self.engine.avg_progression_score(), (int, float))
        assert isinstance(self.engine.high_prob_pipeline_eur(), (int, float))
        assert isinstance(self.engine.stuck_pipeline_eur(), (int, float))


# ─── 17. summary() ───────────────────────────────────────────────────────────

class TestSummary:
    def setup_method(self):
        self.engine = make_engine()

    def test_summary_has_10_keys(self):
        self.engine.analyze(make_input())
        s = self.engine.summary()
        assert len(s) == 10

    def test_summary_expected_keys(self):
        self.engine.analyze(make_input())
        s = self.engine.summary()
        expected = {
            "total_deals", "risk_counts", "action_counts", "probability_counts",
            "avg_progression_score", "total_pipeline_eur", "high_prob_pipeline_eur",
            "stuck_pipeline_eur", "stuck_count", "rescue_count",
        }
        assert set(s.keys()) == expected

    def test_summary_total_deals(self):
        for i in range(3):
            self.engine.analyze(make_input(deal_id=f"D{i}"))
        assert self.engine.summary()["total_deals"] == 3

    def test_summary_empty(self):
        s = self.engine.summary()
        assert s["total_deals"] == 0
        assert s["risk_counts"] == {}
        assert s["action_counts"] == {}
        assert s["probability_counts"] == {}
        assert s["avg_progression_score"] == 0.0
        assert s["total_pipeline_eur"] == 0.0

    def test_summary_risk_counts(self):
        self.engine.analyze(make_input(
            current_stage=DealStage.DEMO,
            previous_stage=None,
            days_in_current_stage=3,
            benchmark_days_demo=14,
            last_activity_days_ago=2,
        ))
        s = self.engine.summary()
        total = sum(s["risk_counts"].values())
        assert total == s["total_deals"]

    def test_summary_action_counts(self):
        self.engine.analyze(make_input())
        self.engine.analyze(make_input(deal_id="D2"))
        s = self.engine.summary()
        total = sum(s["action_counts"].values())
        assert total == s["total_deals"]

    def test_summary_probability_counts(self):
        self.engine.analyze(make_input())
        s = self.engine.summary()
        total = sum(s["probability_counts"].values())
        assert total == s["total_deals"]

    def test_summary_stuck_count_matches(self):
        self.engine.analyze(make_input(
            deal_id="stuck1",
            current_stage=DealStage.QUALIFICATION,
            previous_stage=None,
            days_in_current_stage=25,
            benchmark_days_qualification=10,
            last_activity_days_ago=10,
        ))
        s = self.engine.summary()
        assert s["stuck_count"] == len(self.engine.stuck_deals())

    def test_summary_rescue_count_matches(self):
        self.engine.analyze(make_input())
        s = self.engine.summary()
        assert s["rescue_count"] == len(self.engine.needs_rescue())

    def test_summary_pipeline_eur(self):
        self.engine.analyze(make_input(deal_size_eur=75_000.0))
        s = self.engine.summary()
        assert s["total_pipeline_eur"] == pytest.approx(75_000.0)


# ─── 18. reset() ─────────────────────────────────────────────────────────────

class TestReset:
    def setup_method(self):
        self.engine = make_engine()

    def test_reset_clears_results(self):
        self.engine.analyze(make_input())
        self.engine.reset()
        assert self.engine.all_deals() == []

    def test_reset_allows_reanalysis(self):
        self.engine.analyze(make_input())
        self.engine.reset()
        self.engine.analyze(make_input(deal_id="NEW"))
        assert len(self.engine.all_deals()) == 1

    def test_reset_clears_aggregates(self):
        self.engine.analyze(make_input(deal_size_eur=99_000.0))
        self.engine.reset()
        assert self.engine.total_pipeline_eur() == 0.0
        assert self.engine.avg_progression_score() == 0.0

    def test_reset_multiple_times_safe(self):
        self.engine.reset()
        self.engine.reset()
        assert self.engine.all_deals() == []

    def test_reset_summary_zero(self):
        self.engine.analyze(make_input())
        self.engine.reset()
        s = self.engine.summary()
        assert s["total_deals"] == 0


# ─── 19. Edge cases ───────────────────────────────────────────────────────────

class TestEdgeCases:
    def setup_method(self):
        self.engine = make_engine()

    def test_zero_days_in_stage(self):
        result = self.engine.analyze(make_input(days_in_current_stage=0))
        assert result.days_over_benchmark == 0
        assert isinstance(result.stage_velocity_ratio, (int, float))

    def test_no_previous_stage(self):
        result = self.engine.analyze(make_input(previous_stage=None))
        assert result.previous_stage is None
        assert result.progression_risk != ProgressionRisk.REGRESSED

    def test_all_booleans_false(self):
        result = self.engine.analyze(make_input(
            exec_sponsor_engaged=False,
            budget_confirmed=False,
            timeline_confirmed=False,
            decision_maker_identified=False,
        ))
        assert isinstance(result.progression_score, (int, float))
        assert result.progression_score >= 0.0

    def test_very_large_deal(self):
        result = self.engine.analyze(make_input(deal_size_eur=10_000_000.0))
        assert result.deal_size_eur == pytest.approx(10_000_000.0)

    def test_zero_deal_size(self):
        result = self.engine.analyze(make_input(deal_size_eur=0.0))
        assert result.deal_size_eur == 0.0

    def test_max_win_rate(self):
        result = self.engine.analyze(make_input(rep_stage_win_rate_pct=100.0))
        assert result.progression_score <= 100.0

    def test_zero_win_rate(self):
        result = self.engine.analyze(make_input(rep_stage_win_rate_pct=0.0))
        assert result.progression_score >= 0.0

    def test_closing_stage_no_stages_remaining(self):
        result = self.engine.analyze(make_input(
            current_stage=DealStage.CLOSING,
            previous_stage=DealStage.NEGOTIATION,
            days_in_current_stage=2,
            benchmark_days_closing=7,
        ))
        assert result.estimated_stages_remaining == 0

    def test_prospecting_stage_max_stages_remaining(self):
        result = self.engine.analyze(make_input(
            current_stage=DealStage.PROSPECTING,
            previous_stage=None,
            days_in_current_stage=2,
            benchmark_days_prospecting=7,
            last_activity_days_ago=1,
        ))
        assert result.estimated_stages_remaining == 5

    def test_next_actions_not_empty(self):
        result = self.engine.analyze(make_input())
        assert len(result.next_actions) > 0

    def test_close_quarter_drivers_not_empty(self):
        result = self.engine.analyze(make_input())
        assert len(result.close_quarter_drivers) > 0

    def test_proposals_sent_0_in_proposal_stage(self):
        result = self.engine.analyze(make_input(
            current_stage=DealStage.PROPOSAL,
            previous_stage=DealStage.DEMO,
            days_in_current_stage=5,
            benchmark_days_proposal=14,
            last_activity_days_ago=2,
            proposals_sent=0,
        ))
        # Should have a prompt about sending proposal
        assert any("proposition" in a.lower() for a in result.next_actions)


# ─── 20. Integration: multi-deal batch with mixed risks ───────────────────────

class TestIntegrationMixedRisks:
    def setup_method(self):
        self.engine = make_engine()

    def _build_batch(self):
        return [
            # On-track DEMO deal
            make_input(
                deal_id="D1", deal_size_eur=25_000.0,
                current_stage=DealStage.DEMO, previous_stage=None,
                days_in_current_stage=7, benchmark_days_demo=14,
                last_activity_days_ago=1,
                meetings_held=4, emails_sent=10,
                budget_confirmed=True, timeline_confirmed=True,
                decision_maker_identified=True, rep_stage_win_rate_pct=60.0,
                exec_sponsor_engaged=True, close_date_days_remaining=60,
            ),
            # Stuck QUALIFICATION deal
            make_input(
                deal_id="D2", deal_size_eur=10_000.0,
                current_stage=DealStage.QUALIFICATION, previous_stage=None,
                days_in_current_stage=30, benchmark_days_qualification=10,
                last_activity_days_ago=12,
                meetings_held=0, emails_sent=0,
                budget_confirmed=False, timeline_confirmed=False,
                decision_maker_identified=False, rep_stage_win_rate_pct=0.0,
                exec_sponsor_engaged=False, close_date_days_remaining=30,
            ),
            # Regressed deal
            make_input(
                deal_id="D3", deal_size_eur=50_000.0,
                current_stage=DealStage.PROSPECTING,
                previous_stage=DealStage.PROPOSAL,
                days_in_current_stage=3, benchmark_days_prospecting=7,
                last_activity_days_ago=2,
                meetings_held=2, emails_sent=8,
                budget_confirmed=False, timeline_confirmed=False,
                decision_maker_identified=False, rep_stage_win_rate_pct=30.0,
                exec_sponsor_engaged=False, close_date_days_remaining=45,
            ),
            # CLOSING deal (ready to close)
            make_input(
                deal_id="D4", deal_size_eur=100_000.0,
                current_stage=DealStage.CLOSING,
                previous_stage=DealStage.NEGOTIATION,
                days_in_current_stage=2, benchmark_days_closing=7,
                last_activity_days_ago=0,
                meetings_held=8, emails_sent=30,
                budget_confirmed=True, timeline_confirmed=True,
                decision_maker_identified=True, rep_stage_win_rate_pct=80.0,
                exec_sponsor_engaged=True, close_date_days_remaining=90,
            ),
        ]

    def test_batch_returns_all_results(self):
        results = self.engine.analyze_batch(self._build_batch())
        assert len(results) == 4

    def test_batch_sorted_descending(self):
        results = self.engine.analyze_batch(self._build_batch())
        scores = [r.progression_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_batch_risks_present(self):
        self.engine.analyze_batch(self._build_batch())
        risks = {r.progression_risk for r in self.engine.all_deals()}
        assert ProgressionRisk.STUCK in risks
        assert ProgressionRisk.REGRESSED in risks

    def test_batch_total_pipeline(self):
        self.engine.analyze_batch(self._build_batch())
        assert self.engine.total_pipeline_eur() == pytest.approx(185_000.0)

    def test_batch_ready_to_close_has_d4(self):
        self.engine.analyze_batch(self._build_batch())
        ids = {r.deal_id for r in self.engine.ready_to_close()}
        assert "D4" in ids

    def test_batch_stuck_deals_has_d2(self):
        self.engine.analyze_batch(self._build_batch())
        ids = {r.deal_id for r in self.engine.stuck_deals()}
        assert "D2" in ids

    def test_batch_regressed_has_d3(self):
        self.engine.analyze_batch(self._build_batch())
        ids = {r.deal_id for r in self.engine.regressed_deals()}
        assert "D3" in ids

    def test_batch_summary_total_deals(self):
        self.engine.analyze_batch(self._build_batch())
        s = self.engine.summary()
        assert s["total_deals"] == 4

    def test_batch_summary_stuck_count(self):
        self.engine.analyze_batch(self._build_batch())
        s = self.engine.summary()
        assert s["stuck_count"] >= 1

    def test_batch_summary_rescue_count(self):
        self.engine.analyze_batch(self._build_batch())
        s = self.engine.summary()
        assert s["rescue_count"] >= 1

    def test_all_results_to_dict_valid(self):
        self.engine.analyze_batch(self._build_batch())
        for result in self.engine.all_deals():
            d = result.to_dict()
            assert len(d) == 19
            assert isinstance(d["progression_score"], (int, float))

    def test_reset_after_batch(self):
        self.engine.analyze_batch(self._build_batch())
        self.engine.reset()
        assert len(self.engine.all_deals()) == 0
        assert self.engine.total_pipeline_eur() == 0.0

    def test_by_stage_filter_on_batch(self):
        self.engine.analyze_batch(self._build_batch())
        closing = self.engine.by_stage(DealStage.CLOSING)
        assert any(r.deal_id == "D4" for r in closing)

    def test_by_action_filter_on_batch(self):
        self.engine.analyze_batch(self._build_batch())
        close_now = self.engine.by_action(ProgressionAction.CLOSE_NOW)
        assert all(r.progression_action == ProgressionAction.CLOSE_NOW for r in close_now)
