"""
Comprehensive pytest test suite for DealMomentumEngine.
Target: 300+ tests covering all enums, scoring formulas, logic branches,
properties, summary, reset, and end-to-end scenarios.
"""
from __future__ import annotations

import pytest
from swarm.intelligence.deal_momentum_engine import (
    DealMomentumEngine,
    DealMomentumInput,
    DealMomentumResult,
    MomentumAction,
    MomentumLevel,
    MomentumTrend,
    StallReason,
)


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _make_base(**overrides) -> DealMomentumInput:
    """Neutral baseline: all flags off, mid-range numbers, no risk."""
    defaults = dict(
        deal_id="d1",
        rep_id="r1",
        rep_name="Rep One",
        account_name="Acme Corp",
        days_in_stage=10,
        expected_days_in_stage=10,
        days_to_close=45,
        days_overdue=0,
        activities_last_14d=2,
        activities_last_30d=4,
        last_activity_days_ago=5,
        meetings_last_30d=1,
        next_step_defined=False,
        next_step_days_out=None,
        decision_maker_engaged_14d=False,
        champion_active=False,
        exec_sponsor_engaged=False,
        champion_left=False,
        stage_advances_90d=0,
        stage_regressions_90d=0,
        proposal_sent=False,
        pricing_discussed=False,
        poc_started=False,
        competitor_mentioned=False,
        competitor_demo_requested=False,
        objections_unresolved=0,
        technical_blockers=0,
        budget_confirmed=True,
        legal_engaged=False,
        prior_momentum_score=50.0,
    )
    defaults.update(overrides)
    return DealMomentumInput(**defaults)


def _make_accelerating() -> DealMomentumInput:
    return DealMomentumInput(
        deal_id="acc",
        rep_id="r1",
        rep_name="Rep",
        account_name="Co",
        days_in_stage=5,
        expected_days_in_stage=10,
        days_to_close=20,
        days_overdue=0,
        activities_last_14d=5,
        activities_last_30d=8,
        last_activity_days_ago=1,
        meetings_last_30d=3,
        next_step_defined=True,
        next_step_days_out=3,
        decision_maker_engaged_14d=True,
        champion_active=True,
        exec_sponsor_engaged=True,
        champion_left=False,
        stage_advances_90d=3,
        stage_regressions_90d=0,
        proposal_sent=True,
        pricing_discussed=True,
        poc_started=True,
        competitor_mentioned=False,
        competitor_demo_requested=False,
        objections_unresolved=0,
        technical_blockers=0,
        budget_confirmed=True,
        legal_engaged=True,
        prior_momentum_score=65.0,
    )


def _make_stalled() -> DealMomentumInput:
    return DealMomentumInput(
        deal_id="stl",
        rep_id="r2",
        rep_name="Rep Two",
        account_name="Bad Co",
        days_in_stage=60,
        expected_days_in_stage=14,
        days_to_close=5,
        days_overdue=45,
        activities_last_14d=0,
        activities_last_30d=0,
        last_activity_days_ago=30,
        meetings_last_30d=0,
        next_step_defined=False,
        next_step_days_out=None,
        decision_maker_engaged_14d=False,
        champion_active=False,
        exec_sponsor_engaged=False,
        champion_left=True,
        stage_advances_90d=0,
        stage_regressions_90d=3,
        proposal_sent=False,
        pricing_discussed=False,
        poc_started=False,
        competitor_mentioned=True,
        competitor_demo_requested=True,
        objections_unresolved=3,
        technical_blockers=2,
        budget_confirmed=False,
        legal_engaged=False,
        prior_momentum_score=20.0,
    )


def _engine() -> DealMomentumEngine:
    return DealMomentumEngine()


# ===========================================================================
# 1. ENUM TESTS
# ===========================================================================

class TestMomentumLevelEnum:
    def test_member_count(self):
        assert len(MomentumLevel) == 6

    def test_is_str_subclass(self):
        assert issubclass(MomentumLevel, str)

    def test_accelerating_value(self):
        assert MomentumLevel.ACCELERATING == "accelerating"

    def test_positive_value(self):
        assert MomentumLevel.POSITIVE == "positive"

    def test_neutral_value(self):
        assert MomentumLevel.NEUTRAL == "neutral"

    def test_stalling_value(self):
        assert MomentumLevel.STALLING == "stalling"

    def test_declining_value(self):
        assert MomentumLevel.DECLINING == "declining"

    def test_stalled_value(self):
        assert MomentumLevel.STALLED == "stalled"

    def test_all_members_present(self):
        names = {m.name for m in MomentumLevel}
        assert names == {"ACCELERATING", "POSITIVE", "NEUTRAL", "STALLING", "DECLINING", "STALLED"}

    def test_str_equality(self):
        assert MomentumLevel.ACCELERATING == MomentumLevel.ACCELERATING.value

    def test_enum_from_value(self):
        assert MomentumLevel("positive") == MomentumLevel.POSITIVE


class TestStallReasonEnum:
    def test_member_count(self):
        assert len(StallReason) == 8

    def test_is_str_subclass(self):
        assert issubclass(StallReason, str)

    def test_no_stall(self):
        assert StallReason.NO_STALL == "no_stall"

    def test_decision_delayed(self):
        assert StallReason.DECISION_DELAYED == "decision_delayed"

    def test_budget_frozen(self):
        assert StallReason.BUDGET_FROZEN == "budget_frozen"

    def test_stakeholder_change(self):
        assert StallReason.STAKEHOLDER_CHANGE == "stakeholder_change"

    def test_competitive_threat(self):
        assert StallReason.COMPETITIVE_THREAT == "competitive_threat"

    def test_champion_left(self):
        assert StallReason.CHAMPION_LEFT == "champion_left"

    def test_technical_blocker(self):
        assert StallReason.TECHNICAL_BLOCKER == "technical_blocker"

    def test_internal_misalignment(self):
        assert StallReason.INTERNAL_MISALIGNMENT == "internal_misalignment"

    def test_all_members_present(self):
        names = {m.name for m in StallReason}
        assert names == {
            "NO_STALL", "DECISION_DELAYED", "BUDGET_FROZEN", "STAKEHOLDER_CHANGE",
            "COMPETITIVE_THREAT", "CHAMPION_LEFT", "TECHNICAL_BLOCKER", "INTERNAL_MISALIGNMENT",
        }


class TestMomentumTrendEnum:
    def test_member_count(self):
        assert len(MomentumTrend) == 4

    def test_is_str_subclass(self):
        assert issubclass(MomentumTrend, str)

    def test_improving(self):
        assert MomentumTrend.IMPROVING == "improving"

    def test_stable(self):
        assert MomentumTrend.STABLE == "stable"

    def test_deteriorating(self):
        assert MomentumTrend.DETERIORATING == "deteriorating"

    def test_critical(self):
        assert MomentumTrend.CRITICAL == "critical"

    def test_all_members_present(self):
        names = {m.name for m in MomentumTrend}
        assert names == {"IMPROVING", "STABLE", "DETERIORATING", "CRITICAL"}


class TestMomentumActionEnum:
    def test_member_count(self):
        assert len(MomentumAction) == 8

    def test_is_str_subclass(self):
        assert issubclass(MomentumAction, str)

    def test_maintain(self):
        assert MomentumAction.MAINTAIN == "maintain"

    def test_accelerate(self):
        assert MomentumAction.ACCELERATE == "accelerate"

    def test_re_engage(self):
        assert MomentumAction.RE_ENGAGE == "re_engage"

    def test_executive_escalation(self):
        assert MomentumAction.EXECUTIVE_ESCALATION == "executive_escalation"

    def test_competitive_defense(self):
        assert MomentumAction.COMPETITIVE_DEFENSE == "competitive_defense"

    def test_champion_recovery(self):
        assert MomentumAction.CHAMPION_RECOVERY == "champion_recovery"

    def test_technical_resolution(self):
        assert MomentumAction.TECHNICAL_RESOLUTION == "technical_resolution"

    def test_close_or_abandon(self):
        assert MomentumAction.CLOSE_OR_ABANDON == "close_or_abandon"

    def test_all_members_present(self):
        names = {m.name for m in MomentumAction}
        assert names == {
            "MAINTAIN", "ACCELERATE", "RE_ENGAGE", "EXECUTIVE_ESCALATION",
            "COMPETITIVE_DEFENSE", "CHAMPION_RECOVERY", "TECHNICAL_RESOLUTION", "CLOSE_OR_ABANDON",
        }


# ===========================================================================
# 2. INPUT FIELD VALIDATION
# ===========================================================================

class TestDealMomentumInputFields:
    def setup_method(self):
        self.inp = _make_base()

    def test_deal_id(self):
        assert self.inp.deal_id == "d1"

    def test_rep_id(self):
        assert self.inp.rep_id == "r1"

    def test_rep_name(self):
        assert self.inp.rep_name == "Rep One"

    def test_account_name(self):
        assert self.inp.account_name == "Acme Corp"

    def test_days_in_stage(self):
        assert self.inp.days_in_stage == 10

    def test_expected_days_in_stage(self):
        assert self.inp.expected_days_in_stage == 10

    def test_days_to_close(self):
        assert self.inp.days_to_close == 45

    def test_days_overdue(self):
        assert self.inp.days_overdue == 0

    def test_activities_last_14d(self):
        assert self.inp.activities_last_14d == 2

    def test_activities_last_30d(self):
        assert self.inp.activities_last_30d == 4

    def test_last_activity_days_ago(self):
        assert self.inp.last_activity_days_ago == 5

    def test_meetings_last_30d(self):
        assert self.inp.meetings_last_30d == 1

    def test_next_step_defined(self):
        assert self.inp.next_step_defined is False

    def test_next_step_days_out_optional(self):
        assert self.inp.next_step_days_out is None

    def test_decision_maker_engaged_14d(self):
        assert self.inp.decision_maker_engaged_14d is False

    def test_champion_active(self):
        assert self.inp.champion_active is False

    def test_exec_sponsor_engaged(self):
        assert self.inp.exec_sponsor_engaged is False

    def test_champion_left(self):
        assert self.inp.champion_left is False

    def test_stage_advances_90d(self):
        assert self.inp.stage_advances_90d == 0

    def test_stage_regressions_90d(self):
        assert self.inp.stage_regressions_90d == 0

    def test_proposal_sent(self):
        assert self.inp.proposal_sent is False

    def test_pricing_discussed(self):
        assert self.inp.pricing_discussed is False

    def test_poc_started(self):
        assert self.inp.poc_started is False

    def test_competitor_mentioned(self):
        assert self.inp.competitor_mentioned is False

    def test_competitor_demo_requested(self):
        assert self.inp.competitor_demo_requested is False

    def test_objections_unresolved(self):
        assert self.inp.objections_unresolved == 0

    def test_technical_blockers(self):
        assert self.inp.technical_blockers == 0

    def test_budget_confirmed(self):
        assert self.inp.budget_confirmed is True

    def test_legal_engaged(self):
        assert self.inp.legal_engaged is False

    def test_prior_momentum_score_default(self):
        assert self.inp.prior_momentum_score == 50.0

    def test_total_field_count(self):
        import dataclasses
        fields = dataclasses.fields(DealMomentumInput)
        assert len(fields) == 30


# ===========================================================================
# 3. to_dict KEYS AND TYPES
# ===========================================================================

class TestDealMomentumResultToDict:
    def setup_method(self):
        eng = _engine()
        self.result = eng.analyze(_make_accelerating())
        self.d = self.result.to_dict()

    def test_exactly_15_keys(self):
        assert len(self.d) == 15

    def test_key_deal_id(self):
        assert "deal_id" in self.d

    def test_key_rep_id(self):
        assert "rep_id" in self.d

    def test_key_rep_name(self):
        assert "rep_name" in self.d

    def test_key_account_name(self):
        assert "account_name" in self.d

    def test_key_momentum_score(self):
        assert "momentum_score" in self.d

    def test_key_velocity_score(self):
        assert "velocity_score" in self.d

    def test_key_engagement_score(self):
        assert "engagement_score" in self.d

    def test_key_risk_score(self):
        assert "risk_score" in self.d

    def test_key_momentum_level(self):
        assert "momentum_level" in self.d

    def test_key_stall_reason(self):
        assert "stall_reason" in self.d

    def test_key_momentum_trend(self):
        assert "momentum_trend" in self.d

    def test_key_momentum_action(self):
        assert "momentum_action" in self.d

    def test_key_momentum_indicators(self):
        assert "momentum_indicators" in self.d

    def test_key_risk_signals(self):
        assert "risk_signals" in self.d

    def test_key_recommended_actions(self):
        assert "recommended_actions" in self.d

    def test_momentum_score_type_float(self):
        assert isinstance(self.d["momentum_score"], float)

    def test_velocity_score_type_float(self):
        assert isinstance(self.d["velocity_score"], float)

    def test_engagement_score_type_float(self):
        assert isinstance(self.d["engagement_score"], float)

    def test_risk_score_type_float(self):
        assert isinstance(self.d["risk_score"], float)

    def test_momentum_level_type_str(self):
        assert isinstance(self.d["momentum_level"], str)

    def test_stall_reason_type_str(self):
        assert isinstance(self.d["stall_reason"], str)

    def test_momentum_trend_type_str(self):
        assert isinstance(self.d["momentum_trend"], str)

    def test_momentum_action_type_str(self):
        assert isinstance(self.d["momentum_action"], str)

    def test_momentum_indicators_is_list(self):
        assert isinstance(self.d["momentum_indicators"], list)

    def test_risk_signals_is_list(self):
        assert isinstance(self.d["risk_signals"], list)

    def test_recommended_actions_is_list(self):
        assert isinstance(self.d["recommended_actions"], list)

    def test_deal_id_correct_value(self):
        assert self.d["deal_id"] == "acc"

    def test_rep_id_correct_value(self):
        assert self.d["rep_id"] == "r1"

    def test_momentum_level_is_string_not_enum(self):
        # to_dict must return the .value, not the Enum object
        assert not isinstance(self.d["momentum_level"], MomentumLevel)

    def test_stall_reason_is_string_not_enum(self):
        assert not isinstance(self.d["stall_reason"], StallReason)

    def test_momentum_trend_is_string_not_enum(self):
        assert not isinstance(self.d["momentum_trend"], MomentumTrend)

    def test_momentum_action_is_string_not_enum(self):
        assert not isinstance(self.d["momentum_action"], MomentumAction)


# ===========================================================================
# 4. VELOCITY SCORE
# ===========================================================================

class TestVelocityScore:
    def setup_method(self):
        self.eng = _engine()

    def _vel(self, **kw) -> float:
        return self.eng._velocity_score(_make_base(**kw))

    def test_baseline_no_overrun_no_overdue(self):
        # No overrun, no overdue, no advances, no bonuses → 50.0
        score = self._vel(days_in_stage=10, expected_days_in_stage=10,
                          days_overdue=0, stage_advances_90d=0, stage_regressions_90d=0)
        assert score == 50.0

    def test_stage_overrun_penalty_partial(self):
        # overrun=5, expected=10 → penalty = 5/10 * 35 = 17.5 → 50 - 17.5 = 32.5
        score = self._vel(days_in_stage=15, expected_days_in_stage=10,
                          days_overdue=0, stage_advances_90d=0, stage_regressions_90d=0)
        assert score == pytest.approx(32.5)

    def test_stage_overrun_penalty_max(self):
        # overrun much larger → penalty capped at 35 → 50 - 35 = 15.0
        score = self._vel(days_in_stage=1000, expected_days_in_stage=10,
                          days_overdue=0, stage_advances_90d=0, stage_regressions_90d=0)
        assert score == pytest.approx(15.0)

    def test_stage_overrun_zero_no_penalty(self):
        # days_in_stage == expected → no penalty
        score = self._vel(days_in_stage=10, expected_days_in_stage=10)
        assert score == pytest.approx(50.0)

    def test_stage_no_penalty_when_expected_zero(self):
        # expected=0 → guard clause, no penalty
        score = self._vel(days_in_stage=100, expected_days_in_stage=0,
                          days_overdue=0, stage_advances_90d=0, stage_regressions_90d=0)
        assert score == pytest.approx(50.0)

    def test_days_overdue_penalty_partial(self):
        # overdue=5 → penalty = min(25, 10) = 10 → 50 - 10 = 40
        score = self._vel(days_in_stage=10, expected_days_in_stage=10,
                          days_overdue=5, stage_advances_90d=0, stage_regressions_90d=0)
        assert score == pytest.approx(40.0)

    def test_days_overdue_penalty_capped(self):
        # overdue=20 → penalty = min(25, 40) = 25 → 50 - 25 = 25
        score = self._vel(days_in_stage=10, expected_days_in_stage=10,
                          days_overdue=20, stage_advances_90d=0, stage_regressions_90d=0)
        assert score == pytest.approx(25.0)

    def test_days_overdue_zero_no_penalty(self):
        score = self._vel(days_overdue=0, stage_advances_90d=0, stage_regressions_90d=0)
        assert score == pytest.approx(50.0)

    def test_stage_advances_reward(self):
        # 1 advance = +8 → 58.0
        score = self._vel(stage_advances_90d=1, stage_regressions_90d=0, days_overdue=0)
        assert score == pytest.approx(58.0)

    def test_stage_advances_reward_capped(self):
        # 3 advances = min(20, 24) = +20 → 70.0
        score = self._vel(stage_advances_90d=3, stage_regressions_90d=0, days_overdue=0)
        assert score == pytest.approx(70.0)

    def test_stage_advances_reward_max_cap(self):
        # 100 advances = min(20, 800) = +20 → 70.0
        score = self._vel(stage_advances_90d=100, stage_regressions_90d=0, days_overdue=0)
        assert score == pytest.approx(70.0)

    def test_stage_regressions_penalty(self):
        # 1 regression = min(20, 10) = -10 → 40.0
        score = self._vel(stage_regressions_90d=1, stage_advances_90d=0, days_overdue=0)
        assert score == pytest.approx(40.0)

    def test_stage_regressions_penalty_capped(self):
        # 2 regressions = min(20, 20) = -20 → 30.0
        score = self._vel(stage_regressions_90d=2, stage_advances_90d=0, days_overdue=0)
        assert score == pytest.approx(30.0)

    def test_stage_regressions_penalty_max_cap(self):
        # 100 regressions = min(20, 1000) = -20 → 30.0
        score = self._vel(stage_regressions_90d=100, stage_advances_90d=0, days_overdue=0)
        assert score == pytest.approx(30.0)

    def test_proposal_sent_bonus(self):
        score = self._vel(proposal_sent=True, days_overdue=0, stage_advances_90d=0)
        assert score == pytest.approx(60.0)

    def test_pricing_discussed_bonus(self):
        score = self._vel(pricing_discussed=True, days_overdue=0, stage_advances_90d=0)
        assert score == pytest.approx(58.0)

    def test_poc_started_bonus(self):
        score = self._vel(poc_started=True, days_overdue=0, stage_advances_90d=0)
        assert score == pytest.approx(57.0)

    def test_all_progression_bonuses(self):
        # proposal+pricing+poc = +10+8+7 = +25 → 75.0
        score = self._vel(proposal_sent=True, pricing_discussed=True, poc_started=True,
                          days_overdue=0, stage_advances_90d=0, stage_regressions_90d=0)
        assert score == pytest.approx(75.0)

    def test_clamp_at_zero(self):
        # Massive overrun + overdue + regressions → clamp to 0
        score = self._vel(days_in_stage=10000, expected_days_in_stage=1,
                          days_overdue=100, stage_regressions_90d=10, stage_advances_90d=0)
        assert score == 0.0

    def test_clamp_at_100(self):
        # Max possible without clamping: 50 + 20 (advances) + 10 + 8 + 7 = 95
        # Adding overdue=0 and no overrun still gives 95; to reach 100 we need to
        # verify the clamp does not hurt a score that is already at/near 100.
        # Construct a case where raw arithmetic exceeds 100:
        # 50 + 20(advances) + 10(proposal) + 8(pricing) + 7(poc) = 95;
        # that's the natural max. Verify clamping: score <= 100.
        score = self._vel(
            days_in_stage=1, expected_days_in_stage=10,
            days_overdue=0,
            stage_advances_90d=10,
            stage_regressions_90d=0,
            proposal_sent=True, pricing_discussed=True, poc_started=True,
        )
        assert score <= 100.0
        assert score == pytest.approx(95.0)

    def test_combined_overrun_and_overdue(self):
        # overrun=10, expected=10 → -35; overdue=5 → -10; total: 50-35-10=5
        score = self._vel(days_in_stage=20, expected_days_in_stage=10,
                          days_overdue=5, stage_advances_90d=0, stage_regressions_90d=0)
        assert score == pytest.approx(5.0)


# ===========================================================================
# 5. ENGAGEMENT SCORE
# ===========================================================================

class TestEngagementScore:
    def setup_method(self):
        self.eng = _engine()

    def _eng_score(self, **kw) -> float:
        return self.eng._engagement_score(_make_base(**kw))

    def test_zero_activities_zero_base(self):
        # activities=0, no stakeholders, 5-day recency (neutral)
        score = self._eng_score(
            activities_last_14d=0, activities_last_30d=0,
            last_activity_days_ago=5,
            decision_maker_engaged_14d=False, champion_active=False,
            exec_sponsor_engaged=False, champion_left=False,
            next_step_defined=False,
        )
        assert score == pytest.approx(0.0)

    def test_activity_volume_partial(self):
        # 2 acts * 6 = 12
        score = self._eng_score(
            activities_last_14d=2, activities_last_30d=0,
            last_activity_days_ago=5,
            decision_maker_engaged_14d=False, champion_active=False,
            exec_sponsor_engaged=False, champion_left=False,
            next_step_defined=False,
        )
        assert score == pytest.approx(12.0)

    def test_activity_volume_capped_at_30(self):
        # 10 acts * 6 = 60 → min(30, 60) = 30
        score = self._eng_score(
            activities_last_14d=10, activities_last_30d=0,
            last_activity_days_ago=5,
            decision_maker_engaged_14d=False, champion_active=False,
            exec_sponsor_engaged=False, champion_left=False,
            next_step_defined=False,
        )
        assert score == pytest.approx(30.0)

    def test_activity_volume_cap_at_5_acts(self):
        # 5 acts * 6 = 30 → exactly at cap
        score = self._eng_score(
            activities_last_14d=5, activities_last_30d=0,
            last_activity_days_ago=5,
            decision_maker_engaged_14d=False, champion_active=False,
            exec_sponsor_engaged=False, champion_left=False,
            next_step_defined=False,
        )
        assert score == pytest.approx(30.0)

    def test_activity_trend_accelerating_bonus(self):
        # 14d=4 >= half_30d=2 (30d=4): +15
        score = self._eng_score(
            activities_last_14d=4, activities_last_30d=4,
            last_activity_days_ago=5,
            decision_maker_engaged_14d=False, champion_active=False,
            exec_sponsor_engaged=False, champion_left=False,
            next_step_defined=False,
        )
        # 4*6=24, cap=24, +15 trend = 39
        assert score == pytest.approx(39.0)

    def test_activity_trend_decelerating_penalty(self):
        # 14d=1 < half_30d=3 (30d=6): -10
        score = self._eng_score(
            activities_last_14d=1, activities_last_30d=6,
            last_activity_days_ago=5,
            decision_maker_engaged_14d=False, champion_active=False,
            exec_sponsor_engaged=False, champion_left=False,
            next_step_defined=False,
        )
        # 1*6=6, -10 trend = -4 → clamped to 0
        assert score == pytest.approx(0.0)

    def test_activity_trend_no_effect_when_30d_zero(self):
        # activities_last_30d=0 → no trend bonus/penalty
        score = self._eng_score(
            activities_last_14d=0, activities_last_30d=0,
            last_activity_days_ago=5,
            decision_maker_engaged_14d=False, champion_active=False,
            exec_sponsor_engaged=False, champion_left=False,
            next_step_defined=False,
        )
        assert score == pytest.approx(0.0)

    def test_decision_maker_engaged_bonus(self):
        score = self._eng_score(
            activities_last_14d=0, activities_last_30d=0,
            last_activity_days_ago=5,
            decision_maker_engaged_14d=True, champion_active=False,
            exec_sponsor_engaged=False, champion_left=False,
            next_step_defined=False,
        )
        assert score == pytest.approx(20.0)

    def test_champion_active_bonus(self):
        score = self._eng_score(
            activities_last_14d=0, activities_last_30d=0,
            last_activity_days_ago=5,
            decision_maker_engaged_14d=False, champion_active=True,
            exec_sponsor_engaged=False, champion_left=False,
            next_step_defined=False,
        )
        assert score == pytest.approx(15.0)

    def test_exec_sponsor_engaged_bonus(self):
        score = self._eng_score(
            activities_last_14d=0, activities_last_30d=0,
            last_activity_days_ago=5,
            decision_maker_engaged_14d=False, champion_active=False,
            exec_sponsor_engaged=True, champion_left=False,
            next_step_defined=False,
        )
        assert score == pytest.approx(10.0)

    def test_recency_3_days_bonus(self):
        # last 3 days → +10
        score = self._eng_score(
            activities_last_14d=0, activities_last_30d=0,
            last_activity_days_ago=3,
            decision_maker_engaged_14d=False, champion_active=False,
            exec_sponsor_engaged=False, champion_left=False,
            next_step_defined=False,
        )
        assert score == pytest.approx(10.0)

    def test_recency_1_day_bonus(self):
        score = self._eng_score(
            activities_last_14d=0, activities_last_30d=0,
            last_activity_days_ago=1,
            decision_maker_engaged_14d=False, champion_active=False,
            exec_sponsor_engaged=False, champion_left=False,
            next_step_defined=False,
        )
        assert score == pytest.approx(10.0)

    def test_recency_4_to_7_days_neutral(self):
        # 4-7 days → no bonus/penalty
        score = self._eng_score(
            activities_last_14d=0, activities_last_30d=0,
            last_activity_days_ago=7,
            decision_maker_engaged_14d=False, champion_active=False,
            exec_sponsor_engaged=False, champion_left=False,
            next_step_defined=False,
        )
        assert score == pytest.approx(0.0)

    def test_recency_8_to_14_days_penalty(self):
        # 8-14 days → -10
        score = self._eng_score(
            activities_last_14d=0, activities_last_30d=0,
            last_activity_days_ago=10,
            decision_maker_engaged_14d=False, champion_active=False,
            exec_sponsor_engaged=False, champion_left=False,
            next_step_defined=False,
        )
        # 0 - 10 = -10 → clamped to 0
        assert score == pytest.approx(0.0)

    def test_recency_8_to_14_days_penalty_not_zero_base(self):
        # With other bonuses, the -10 should apply
        score = self._eng_score(
            activities_last_14d=0, activities_last_30d=0,
            last_activity_days_ago=10,
            decision_maker_engaged_14d=True, champion_active=False,
            exec_sponsor_engaged=False, champion_left=False,
            next_step_defined=False,
        )
        # 20 - 10 = 10
        assert score == pytest.approx(10.0)

    def test_recency_over_14_days_penalty(self):
        # > 14 days → -20
        score = self._eng_score(
            activities_last_14d=0, activities_last_30d=0,
            last_activity_days_ago=15,
            decision_maker_engaged_14d=True, champion_active=False,
            exec_sponsor_engaged=False, champion_left=False,
            next_step_defined=False,
        )
        # 20 - 20 = 0
        assert score == pytest.approx(0.0)

    def test_recency_14_days_is_no_penalty_boundary(self):
        # Exactly 14 days → not > 14 → no -20 penalty (but > 7 → -10)
        score = self._eng_score(
            activities_last_14d=0, activities_last_30d=0,
            last_activity_days_ago=14,
            decision_maker_engaged_14d=True, champion_active=False,
            exec_sponsor_engaged=False, champion_left=False,
            next_step_defined=False,
        )
        # 20 - 10 (because >7, not >14) = 10
        assert score == pytest.approx(10.0)

    def test_next_step_defined_bonus(self):
        score = self._eng_score(
            activities_last_14d=0, activities_last_30d=0,
            last_activity_days_ago=5,
            decision_maker_engaged_14d=False, champion_active=False,
            exec_sponsor_engaged=False, champion_left=False,
            next_step_defined=True, next_step_days_out=5,
        )
        assert score == pytest.approx(10.0)

    def test_next_step_far_out_penalty(self):
        # next_step > 14 days → +10 - 5 = 5 net
        score = self._eng_score(
            activities_last_14d=0, activities_last_30d=0,
            last_activity_days_ago=5,
            decision_maker_engaged_14d=False, champion_active=False,
            exec_sponsor_engaged=False, champion_left=False,
            next_step_defined=True, next_step_days_out=15,
        )
        assert score == pytest.approx(5.0)

    def test_next_step_exactly_14_no_penalty(self):
        # exactly 14 days → not > 14 → no deduction
        score = self._eng_score(
            activities_last_14d=0, activities_last_30d=0,
            last_activity_days_ago=5,
            decision_maker_engaged_14d=False, champion_active=False,
            exec_sponsor_engaged=False, champion_left=False,
            next_step_defined=True, next_step_days_out=14,
        )
        assert score == pytest.approx(10.0)

    def test_champion_left_penalty(self):
        score = self._eng_score(
            activities_last_14d=0, activities_last_30d=0,
            last_activity_days_ago=5,
            decision_maker_engaged_14d=False, champion_active=False,
            exec_sponsor_engaged=False, champion_left=True,
            next_step_defined=False,
        )
        # 0 - 30 = -30 → clamped to 0
        assert score == pytest.approx(0.0)

    def test_champion_left_penalty_with_bonuses(self):
        # With full stakeholder bonuses: 20+15+10=45, -30 = 15
        score = self._eng_score(
            activities_last_14d=0, activities_last_30d=0,
            last_activity_days_ago=5,
            decision_maker_engaged_14d=True, champion_active=True,
            exec_sponsor_engaged=True, champion_left=True,
            next_step_defined=False,
        )
        assert score == pytest.approx(15.0)

    def test_clamp_at_zero(self):
        score = self._eng_score(
            activities_last_14d=0, activities_last_30d=10,
            last_activity_days_ago=30,
            champion_left=True,
            decision_maker_engaged_14d=False, champion_active=False,
            exec_sponsor_engaged=False, next_step_defined=False,
        )
        assert score == 0.0

    def test_clamp_at_100(self):
        # Max possible: 30 + 15 + 20 + 15 + 10 + 10 + 10 = 110 → clamped to 100
        score = self._eng_score(
            activities_last_14d=10, activities_last_30d=4,
            last_activity_days_ago=1,
            decision_maker_engaged_14d=True, champion_active=True,
            exec_sponsor_engaged=True, champion_left=False,
            next_step_defined=True, next_step_days_out=5,
        )
        assert score == 100.0


# ===========================================================================
# 6. RISK SCORE
# ===========================================================================

class TestRiskScore:
    def setup_method(self):
        self.eng = _engine()

    def _risk(self, **kw) -> float:
        return self.eng._risk_score(_make_base(**kw))

    def test_no_risk_factors_zero(self):
        score = self._risk(
            champion_left=False, competitor_demo_requested=False,
            competitor_mentioned=False, objections_unresolved=0,
            technical_blockers=0, budget_confirmed=True,
            days_to_close=45, stage_regressions_90d=0,
        )
        assert score == pytest.approx(0.0)

    def test_champion_left_adds_30(self):
        score = self._risk(
            champion_left=True, competitor_demo_requested=False,
            competitor_mentioned=False, objections_unresolved=0,
            technical_blockers=0, budget_confirmed=True,
            days_to_close=45, stage_regressions_90d=0,
        )
        assert score == pytest.approx(30.0)

    def test_competitor_demo_requested_adds_25(self):
        score = self._risk(
            champion_left=False, competitor_demo_requested=True,
            competitor_mentioned=False, objections_unresolved=0,
            technical_blockers=0, budget_confirmed=True,
            days_to_close=45, stage_regressions_90d=0,
        )
        assert score == pytest.approx(25.0)

    def test_competitor_mentioned_adds_15(self):
        score = self._risk(
            champion_left=False, competitor_demo_requested=False,
            competitor_mentioned=True, objections_unresolved=0,
            technical_blockers=0, budget_confirmed=True,
            days_to_close=45, stage_regressions_90d=0,
        )
        assert score == pytest.approx(15.0)

    def test_demo_takes_priority_over_mentioned(self):
        # When both are True, demo_requested (25) takes priority over mentioned (15)
        score = self._risk(
            champion_left=False, competitor_demo_requested=True,
            competitor_mentioned=True, objections_unresolved=0,
            technical_blockers=0, budget_confirmed=True,
            days_to_close=45, stage_regressions_90d=0,
        )
        assert score == pytest.approx(25.0)

    def test_objections_1(self):
        score = self._risk(
            champion_left=False, competitor_demo_requested=False,
            competitor_mentioned=False, objections_unresolved=1,
            technical_blockers=0, budget_confirmed=True,
            days_to_close=45, stage_regressions_90d=0,
        )
        assert score == pytest.approx(8.0)

    def test_objections_2(self):
        score = self._risk(
            champion_left=False, competitor_demo_requested=False,
            competitor_mentioned=False, objections_unresolved=2,
            technical_blockers=0, budget_confirmed=True,
            days_to_close=45, stage_regressions_90d=0,
        )
        assert score == pytest.approx(16.0)

    def test_objections_capped_at_20(self):
        # 3 * 8 = 24 → capped at 20
        score = self._risk(
            champion_left=False, competitor_demo_requested=False,
            competitor_mentioned=False, objections_unresolved=3,
            technical_blockers=0, budget_confirmed=True,
            days_to_close=45, stage_regressions_90d=0,
        )
        assert score == pytest.approx(20.0)

    def test_technical_blockers_1(self):
        score = self._risk(
            champion_left=False, competitor_demo_requested=False,
            competitor_mentioned=False, objections_unresolved=0,
            technical_blockers=1, budget_confirmed=True,
            days_to_close=45, stage_regressions_90d=0,
        )
        assert score == pytest.approx(10.0)

    def test_technical_blockers_2(self):
        score = self._risk(
            champion_left=False, competitor_demo_requested=False,
            competitor_mentioned=False, objections_unresolved=0,
            technical_blockers=2, budget_confirmed=True,
            days_to_close=45, stage_regressions_90d=0,
        )
        assert score == pytest.approx(20.0)

    def test_technical_blockers_capped_at_20(self):
        # 3 * 10 = 30 → capped at 20
        score = self._risk(
            champion_left=False, competitor_demo_requested=False,
            competitor_mentioned=False, objections_unresolved=0,
            technical_blockers=3, budget_confirmed=True,
            days_to_close=45, stage_regressions_90d=0,
        )
        assert score == pytest.approx(20.0)

    def test_budget_not_confirmed_close_in_30_adds_15(self):
        score = self._risk(
            champion_left=False, competitor_demo_requested=False,
            competitor_mentioned=False, objections_unresolved=0,
            technical_blockers=0, budget_confirmed=False,
            days_to_close=25, stage_regressions_90d=0,
        )
        assert score == pytest.approx(15.0)

    def test_budget_not_confirmed_beyond_30_no_penalty(self):
        score = self._risk(
            champion_left=False, competitor_demo_requested=False,
            competitor_mentioned=False, objections_unresolved=0,
            technical_blockers=0, budget_confirmed=False,
            days_to_close=31, stage_regressions_90d=0,
        )
        assert score == pytest.approx(0.0)

    def test_budget_confirmed_no_penalty_within_30(self):
        score = self._risk(
            champion_left=False, competitor_demo_requested=False,
            competitor_mentioned=False, objections_unresolved=0,
            technical_blockers=0, budget_confirmed=True,
            days_to_close=25, stage_regressions_90d=0,
        )
        assert score == pytest.approx(0.0)

    def test_budget_days_to_close_exactly_30(self):
        # days_to_close=30 → <= 30 → penalty applies
        score = self._risk(
            champion_left=False, competitor_demo_requested=False,
            competitor_mentioned=False, objections_unresolved=0,
            technical_blockers=0, budget_confirmed=False,
            days_to_close=30, stage_regressions_90d=0,
        )
        assert score == pytest.approx(15.0)

    def test_stage_regressions_1(self):
        score = self._risk(
            champion_left=False, competitor_demo_requested=False,
            competitor_mentioned=False, objections_unresolved=0,
            technical_blockers=0, budget_confirmed=True,
            days_to_close=45, stage_regressions_90d=1,
        )
        assert score == pytest.approx(5.0)

    def test_stage_regressions_2(self):
        score = self._risk(
            champion_left=False, competitor_demo_requested=False,
            competitor_mentioned=False, objections_unresolved=0,
            technical_blockers=0, budget_confirmed=True,
            days_to_close=45, stage_regressions_90d=2,
        )
        assert score == pytest.approx(10.0)

    def test_stage_regressions_capped_at_10(self):
        # 3 * 5 = 15 → capped at 10
        score = self._risk(
            champion_left=False, competitor_demo_requested=False,
            competitor_mentioned=False, objections_unresolved=0,
            technical_blockers=0, budget_confirmed=True,
            days_to_close=45, stage_regressions_90d=3,
        )
        assert score == pytest.approx(10.0)

    def test_clamp_at_100(self):
        # All risk factors together
        score = self._risk(
            champion_left=True, competitor_demo_requested=True,
            competitor_mentioned=True, objections_unresolved=10,
            technical_blockers=10, budget_confirmed=False,
            days_to_close=5, stage_regressions_90d=10,
        )
        assert score == 100.0

    def test_clamp_at_zero(self):
        score = self._risk(
            champion_left=False, competitor_demo_requested=False,
            competitor_mentioned=False, objections_unresolved=0,
            technical_blockers=0, budget_confirmed=True,
            days_to_close=100, stage_regressions_90d=0,
        )
        assert score == 0.0


# ===========================================================================
# 7. MOMENTUM SCORE
# ===========================================================================

class TestMomentumScore:
    def setup_method(self):
        self.eng = _engine()

    def test_basic_formula(self):
        # vel=60, eng=70, risk=20, prior=50
        # raw = 60*0.35 + 70*0.40 + (100-20)*0.25 = 21 + 28 + 20 = 69
        # blended = 69*0.70 + 50*0.30 = 48.3 + 15 = 63.3
        result = self.eng._momentum_score(60.0, 70.0, 20.0, 50.0)
        assert result == pytest.approx(63.3)

    def test_prior_blending_effect(self):
        # Prior pulls the score toward itself
        high_prior = self.eng._momentum_score(50.0, 50.0, 50.0, 90.0)
        low_prior = self.eng._momentum_score(50.0, 50.0, 50.0, 10.0)
        assert high_prior > low_prior

    def test_clamp_at_100(self):
        result = self.eng._momentum_score(100.0, 100.0, 0.0, 100.0)
        assert result == 100.0

    def test_clamp_at_zero(self):
        result = self.eng._momentum_score(0.0, 0.0, 100.0, 0.0)
        assert result == 0.0

    def test_rounded_to_1_decimal(self):
        result = self.eng._momentum_score(55.0, 65.0, 30.0, 48.0)
        assert result == round(result, 1)

    def test_risk_contribution_inverted(self):
        # Higher risk → lower momentum score
        low_risk = self.eng._momentum_score(50.0, 50.0, 10.0, 50.0)
        high_risk = self.eng._momentum_score(50.0, 50.0, 90.0, 50.0)
        assert low_risk > high_risk

    def test_equal_components_50(self):
        # vel=50, eng=50, risk=50, prior=50
        # raw = 50*0.35 + 50*0.40 + 50*0.25 = 17.5+20+12.5=50
        # blended = 50*0.70 + 50*0.30 = 50
        result = self.eng._momentum_score(50.0, 50.0, 50.0, 50.0)
        assert result == pytest.approx(50.0)


# ===========================================================================
# 8. MOMENTUM LEVEL
# ===========================================================================

class TestMomentumLevel:
    def setup_method(self):
        self.eng = _engine()

    def test_score_75_is_accelerating(self):
        assert self.eng._momentum_level(75.0) == MomentumLevel.ACCELERATING

    def test_score_100_is_accelerating(self):
        assert self.eng._momentum_level(100.0) == MomentumLevel.ACCELERATING

    def test_score_74_is_positive(self):
        assert self.eng._momentum_level(74.9) == MomentumLevel.POSITIVE

    def test_score_60_is_positive(self):
        assert self.eng._momentum_level(60.0) == MomentumLevel.POSITIVE

    def test_score_59_is_neutral(self):
        assert self.eng._momentum_level(59.9) == MomentumLevel.NEUTRAL

    def test_score_45_is_neutral(self):
        assert self.eng._momentum_level(45.0) == MomentumLevel.NEUTRAL

    def test_score_44_is_stalling(self):
        assert self.eng._momentum_level(44.9) == MomentumLevel.STALLING

    def test_score_30_is_stalling(self):
        assert self.eng._momentum_level(30.0) == MomentumLevel.STALLING

    def test_score_29_is_declining(self):
        assert self.eng._momentum_level(29.9) == MomentumLevel.DECLINING

    def test_score_15_is_declining(self):
        assert self.eng._momentum_level(15.0) == MomentumLevel.DECLINING

    def test_score_14_is_stalled(self):
        assert self.eng._momentum_level(14.9) == MomentumLevel.STALLED

    def test_score_0_is_stalled(self):
        assert self.eng._momentum_level(0.0) == MomentumLevel.STALLED

    def test_boundary_75_exact(self):
        assert self.eng._momentum_level(75.0) == MomentumLevel.ACCELERATING

    def test_boundary_60_exact(self):
        assert self.eng._momentum_level(60.0) == MomentumLevel.POSITIVE

    def test_boundary_45_exact(self):
        assert self.eng._momentum_level(45.0) == MomentumLevel.NEUTRAL

    def test_boundary_30_exact(self):
        assert self.eng._momentum_level(30.0) == MomentumLevel.STALLING

    def test_boundary_15_exact(self):
        assert self.eng._momentum_level(15.0) == MomentumLevel.DECLINING


# ===========================================================================
# 9. STALL REASON
# ===========================================================================

class TestStallReason:
    def setup_method(self):
        self.eng = _engine()

    def _stall(self, level: MomentumLevel, **kw) -> StallReason:
        return self.eng._stall_reason(_make_base(**kw), level)

    # Priority 1: champion_left
    def test_champion_left_highest_priority(self):
        reason = self._stall(
            MomentumLevel.STALLED,
            champion_left=True,
            technical_blockers=3,
            competitor_demo_requested=True,
            stage_regressions_90d=3,
        )
        assert reason == StallReason.CHAMPION_LEFT

    def test_champion_left_any_level(self):
        for level in MomentumLevel:
            reason = self._stall(level, champion_left=True)
            assert reason == StallReason.CHAMPION_LEFT

    # Priority 2: technical_blockers >= 2
    def test_technical_blocker_two(self):
        reason = self._stall(
            MomentumLevel.STALLED,
            champion_left=False,
            technical_blockers=2,
            competitor_demo_requested=True,
        )
        assert reason == StallReason.TECHNICAL_BLOCKER

    def test_technical_blocker_one_not_triggered(self):
        reason = self._stall(
            MomentumLevel.STALLED,
            champion_left=False,
            technical_blockers=1,
            competitor_demo_requested=False,
            stage_regressions_90d=0,
            budget_confirmed=True,
            days_overdue=0,
            decision_maker_engaged_14d=False,
            champion_active=False,
        )
        # 1 blocker is not >= 2 → falls through to stakeholder or decision_delayed
        assert reason != StallReason.TECHNICAL_BLOCKER

    # Priority 3: competitor_demo_requested
    def test_competitive_threat(self):
        reason = self._stall(
            MomentumLevel.STALLED,
            champion_left=False,
            technical_blockers=0,
            competitor_demo_requested=True,
        )
        assert reason == StallReason.COMPETITIVE_THREAT

    def test_competitor_mentioned_not_demo_not_competitive_threat(self):
        reason = self._stall(
            MomentumLevel.ACCELERATING,
            champion_left=False,
            technical_blockers=0,
            competitor_demo_requested=False,
            competitor_mentioned=True,
            stage_regressions_90d=0,
            budget_confirmed=True,
            days_overdue=0,
        )
        assert reason == StallReason.NO_STALL

    # Priority 4: stage_regressions_90d >= 2
    def test_internal_misalignment(self):
        reason = self._stall(
            MomentumLevel.STALLED,
            champion_left=False,
            technical_blockers=0,
            competitor_demo_requested=False,
            stage_regressions_90d=2,
        )
        assert reason == StallReason.INTERNAL_MISALIGNMENT

    def test_one_regression_not_internal_misalignment(self):
        reason = self._stall(
            MomentumLevel.STALLING,
            champion_left=False,
            technical_blockers=0,
            competitor_demo_requested=False,
            stage_regressions_90d=1,
            budget_confirmed=True,
            days_overdue=0,
            decision_maker_engaged_14d=False,
            champion_active=False,
        )
        assert reason != StallReason.INTERNAL_MISALIGNMENT

    # Priority 5: not budget AND days_to_close <= 14
    def test_budget_frozen(self):
        reason = self._stall(
            MomentumLevel.STALLED,
            champion_left=False,
            technical_blockers=0,
            competitor_demo_requested=False,
            stage_regressions_90d=0,
            budget_confirmed=False,
            days_to_close=10,
            days_overdue=0,
        )
        assert reason == StallReason.BUDGET_FROZEN

    def test_budget_frozen_exactly_14(self):
        reason = self._stall(
            MomentumLevel.STALLED,
            champion_left=False,
            technical_blockers=0,
            competitor_demo_requested=False,
            stage_regressions_90d=0,
            budget_confirmed=False,
            days_to_close=14,
            days_overdue=0,
        )
        assert reason == StallReason.BUDGET_FROZEN

    def test_budget_frozen_15_days_out_no_trigger(self):
        reason = self._stall(
            MomentumLevel.STALLED,
            champion_left=False,
            technical_blockers=0,
            competitor_demo_requested=False,
            stage_regressions_90d=0,
            budget_confirmed=False,
            days_to_close=15,
            days_overdue=0,
            decision_maker_engaged_14d=False,
            champion_active=False,
        )
        assert reason != StallReason.BUDGET_FROZEN

    # Priority 6: days_overdue > 30
    def test_decision_delayed_overdue(self):
        reason = self._stall(
            MomentumLevel.ACCELERATING,
            champion_left=False,
            technical_blockers=0,
            competitor_demo_requested=False,
            stage_regressions_90d=0,
            budget_confirmed=True,
            days_overdue=31,
        )
        assert reason == StallReason.DECISION_DELAYED

    def test_decision_delayed_overdue_30_no_trigger(self):
        reason = self._stall(
            MomentumLevel.ACCELERATING,
            champion_left=False,
            technical_blockers=0,
            competitor_demo_requested=False,
            stage_regressions_90d=0,
            budget_confirmed=True,
            days_overdue=30,
        )
        # 30 is not > 30 → falls through to NO_STALL for ACCELERATING
        assert reason == StallReason.NO_STALL

    # Priority 7: stalling/declining/stalled without DM or champion
    def test_stakeholder_change_stalling(self):
        reason = self._stall(
            MomentumLevel.STALLING,
            champion_left=False,
            technical_blockers=0,
            competitor_demo_requested=False,
            stage_regressions_90d=0,
            budget_confirmed=True,
            days_overdue=0,
            decision_maker_engaged_14d=False,
            champion_active=False,
        )
        assert reason == StallReason.STAKEHOLDER_CHANGE

    def test_stakeholder_change_declining(self):
        reason = self._stall(
            MomentumLevel.DECLINING,
            champion_left=False,
            technical_blockers=0,
            competitor_demo_requested=False,
            stage_regressions_90d=0,
            budget_confirmed=True,
            days_overdue=0,
            decision_maker_engaged_14d=False,
            champion_active=False,
        )
        assert reason == StallReason.STAKEHOLDER_CHANGE

    # Priority 8: stalling/declining/stalled with DM or champion → decision_delayed
    def test_decision_delayed_stalling_with_dm(self):
        reason = self._stall(
            MomentumLevel.STALLING,
            champion_left=False,
            technical_blockers=0,
            competitor_demo_requested=False,
            stage_regressions_90d=0,
            budget_confirmed=True,
            days_overdue=0,
            decision_maker_engaged_14d=True,
            champion_active=False,
        )
        assert reason == StallReason.DECISION_DELAYED

    # Priority 9: else → NO_STALL
    def test_no_stall_accelerating_clean(self):
        reason = self._stall(
            MomentumLevel.ACCELERATING,
            champion_left=False,
            technical_blockers=0,
            competitor_demo_requested=False,
            stage_regressions_90d=0,
            budget_confirmed=True,
            days_overdue=0,
        )
        assert reason == StallReason.NO_STALL

    def test_no_stall_positive_clean(self):
        reason = self._stall(
            MomentumLevel.POSITIVE,
            champion_left=False,
            technical_blockers=0,
            competitor_demo_requested=False,
            stage_regressions_90d=0,
            budget_confirmed=True,
            days_overdue=0,
        )
        assert reason == StallReason.NO_STALL


# ===========================================================================
# 10. MOMENTUM TREND
# ===========================================================================

class TestMomentumTrend:
    def setup_method(self):
        self.eng = _engine()

    def _trend(self, score, prior, level):
        return self.eng._momentum_trend(score, prior, level)

    def test_improving_delta_exactly_10(self):
        assert self._trend(60.0, 50.0, MomentumLevel.POSITIVE) == MomentumTrend.IMPROVING

    def test_improving_delta_above_10(self):
        assert self._trend(70.0, 50.0, MomentumLevel.ACCELERATING) == MomentumTrend.IMPROVING

    def test_improving_delta_9_is_stable(self):
        assert self._trend(59.0, 50.0, MomentumLevel.POSITIVE) == MomentumTrend.STABLE

    def test_critical_delta_minus_15_declining(self):
        assert self._trend(10.0, 25.0, MomentumLevel.DECLINING) == MomentumTrend.CRITICAL

    def test_critical_delta_minus_15_stalled(self):
        assert self._trend(10.0, 25.0, MomentumLevel.STALLED) == MomentumTrend.CRITICAL

    def test_critical_requires_declining_or_stalled(self):
        # Same delta -15 but with NEUTRAL level → deteriorating (not critical)
        assert self._trend(35.0, 50.0, MomentumLevel.NEUTRAL) == MomentumTrend.DETERIORATING

    def test_critical_delta_exactly_minus_15(self):
        assert self._trend(5.0, 20.0, MomentumLevel.STALLED) == MomentumTrend.CRITICAL

    def test_deteriorating_delta_minus_5(self):
        assert self._trend(45.0, 50.0, MomentumLevel.NEUTRAL) == MomentumTrend.DETERIORATING

    def test_deteriorating_delta_minus_14(self):
        # -14 is <= -5 but not <= -15 → deteriorating
        assert self._trend(36.0, 50.0, MomentumLevel.NEUTRAL) == MomentumTrend.DETERIORATING

    def test_stable_small_negative_delta(self):
        # -4 → stable
        assert self._trend(46.0, 50.0, MomentumLevel.NEUTRAL) == MomentumTrend.STABLE

    def test_stable_zero_delta(self):
        assert self._trend(50.0, 50.0, MomentumLevel.NEUTRAL) == MomentumTrend.STABLE

    def test_stable_small_positive_delta(self):
        # +5 → not >= 10 → stable
        assert self._trend(55.0, 50.0, MomentumLevel.POSITIVE) == MomentumTrend.STABLE


# ===========================================================================
# 11. MOMENTUM ACTION
# ===========================================================================

class TestMomentumAction:
    def setup_method(self):
        self.eng = _engine()

    def _action(self, level, stall, trend, **kw):
        return self.eng._momentum_action(
            _make_base(**kw), level, stall, trend
        )

    # Path 1: CHAMPION_LEFT → CHAMPION_RECOVERY
    def test_champion_recovery_priority(self):
        action = self._action(
            MomentumLevel.STALLED,
            StallReason.CHAMPION_LEFT,
            MomentumTrend.CRITICAL,
            last_activity_days_ago=30,
        )
        assert action == MomentumAction.CHAMPION_RECOVERY

    def test_champion_recovery_overrides_stalled_inactive(self):
        # Even though STALLED + last_activity > 14, champion_left wins
        action = self._action(
            MomentumLevel.STALLED,
            StallReason.CHAMPION_LEFT,
            MomentumTrend.CRITICAL,
            last_activity_days_ago=30,
        )
        assert action == MomentumAction.CHAMPION_RECOVERY

    # Path 2: STALLED + last_activity > 14 → CLOSE_OR_ABANDON
    def test_close_or_abandon_stalled_inactive(self):
        action = self._action(
            MomentumLevel.STALLED,
            StallReason.DECISION_DELAYED,
            MomentumTrend.CRITICAL,
            last_activity_days_ago=15,
        )
        assert action == MomentumAction.CLOSE_OR_ABANDON

    def test_close_or_abandon_not_triggered_14_days(self):
        # Exactly 14 days → not > 14 → doesn't close
        action = self._action(
            MomentumLevel.STALLED,
            StallReason.DECISION_DELAYED,
            MomentumTrend.CRITICAL,
            last_activity_days_ago=14,
            exec_sponsor_engaged=False,
            decision_maker_engaged_14d=False,
            champion_active=False,
        )
        # Falls to path 6 or beyond
        assert action != MomentumAction.CLOSE_OR_ABANDON

    # Path 3: COMPETITIVE_THREAT → COMPETITIVE_DEFENSE
    def test_competitive_defense(self):
        action = self._action(
            MomentumLevel.POSITIVE,
            StallReason.COMPETITIVE_THREAT,
            MomentumTrend.STABLE,
        )
        assert action == MomentumAction.COMPETITIVE_DEFENSE

    # Path 4: TECHNICAL_BLOCKER → TECHNICAL_RESOLUTION
    def test_technical_resolution(self):
        action = self._action(
            MomentumLevel.STALLING,
            StallReason.TECHNICAL_BLOCKER,
            MomentumTrend.DETERIORATING,
        )
        assert action == MomentumAction.TECHNICAL_RESOLUTION

    # Path 5: DECLINING/STALLED + exec or dm engaged → EXECUTIVE_ESCALATION
    def test_executive_escalation_declining_exec(self):
        action = self._action(
            MomentumLevel.DECLINING,
            StallReason.DECISION_DELAYED,
            MomentumTrend.DETERIORATING,
            exec_sponsor_engaged=True,
            decision_maker_engaged_14d=False,
            last_activity_days_ago=5,
        )
        assert action == MomentumAction.EXECUTIVE_ESCALATION

    def test_executive_escalation_stalled_dm(self):
        action = self._action(
            MomentumLevel.STALLED,
            StallReason.STAKEHOLDER_CHANGE,
            MomentumTrend.CRITICAL,
            exec_sponsor_engaged=False,
            decision_maker_engaged_14d=True,
            last_activity_days_ago=5,
        )
        assert action == MomentumAction.EXECUTIVE_ESCALATION

    def test_executive_escalation_not_triggered_without_dm_exec(self):
        action = self._action(
            MomentumLevel.DECLINING,
            StallReason.DECISION_DELAYED,
            MomentumTrend.DETERIORATING,
            exec_sponsor_engaged=False,
            decision_maker_engaged_14d=False,
            last_activity_days_ago=5,
        )
        assert action == MomentumAction.RE_ENGAGE

    # Path 6: STALLING/DECLINING → RE_ENGAGE
    def test_re_engage_stalling(self):
        action = self._action(
            MomentumLevel.STALLING,
            StallReason.STAKEHOLDER_CHANGE,
            MomentumTrend.DETERIORATING,
            exec_sponsor_engaged=False,
            decision_maker_engaged_14d=False,
        )
        assert action == MomentumAction.RE_ENGAGE

    def test_re_engage_declining(self):
        action = self._action(
            MomentumLevel.DECLINING,
            StallReason.STAKEHOLDER_CHANGE,
            MomentumTrend.DETERIORATING,
            exec_sponsor_engaged=False,
            decision_maker_engaged_14d=False,
            last_activity_days_ago=5,
        )
        assert action == MomentumAction.RE_ENGAGE

    # Path 7: POSITIVE/ACCELERATING + close <= 30 → ACCELERATE
    def test_accelerate_positive_closing_soon(self):
        action = self._action(
            MomentumLevel.POSITIVE,
            StallReason.NO_STALL,
            MomentumTrend.STABLE,
            days_to_close=25,
        )
        assert action == MomentumAction.ACCELERATE

    def test_accelerate_accelerating_closing_soon(self):
        action = self._action(
            MomentumLevel.ACCELERATING,
            StallReason.NO_STALL,
            MomentumTrend.IMPROVING,
            days_to_close=10,
        )
        assert action == MomentumAction.ACCELERATE

    # Path 8: POSITIVE/ACCELERATING + close > 30 → MAINTAIN
    def test_maintain_positive_not_closing_soon(self):
        action = self._action(
            MomentumLevel.POSITIVE,
            StallReason.NO_STALL,
            MomentumTrend.STABLE,
            days_to_close=60,
        )
        assert action == MomentumAction.MAINTAIN

    def test_maintain_accelerating_not_closing_soon(self):
        action = self._action(
            MomentumLevel.ACCELERATING,
            StallReason.NO_STALL,
            MomentumTrend.IMPROVING,
            days_to_close=45,
        )
        assert action == MomentumAction.MAINTAIN

    # Path 9: NEUTRAL + next_step_defined → MAINTAIN
    def test_maintain_neutral_with_next_step(self):
        action = self._action(
            MomentumLevel.NEUTRAL,
            StallReason.NO_STALL,
            MomentumTrend.STABLE,
            next_step_defined=True,
            days_to_close=60,
        )
        assert action == MomentumAction.MAINTAIN

    # Path 10: else → ACCELERATE
    def test_accelerate_neutral_without_next_step(self):
        action = self._action(
            MomentumLevel.NEUTRAL,
            StallReason.NO_STALL,
            MomentumTrend.STABLE,
            next_step_defined=False,
            days_to_close=60,
        )
        assert action == MomentumAction.ACCELERATE


# ===========================================================================
# 12. HELPER PROPERTIES
# ===========================================================================

class TestHelperProperties:
    def test_stalled_deals_empty(self):
        eng = _engine()
        assert eng.stalled_deals == []

    def test_at_risk_deals_empty(self):
        eng = _engine()
        assert eng.at_risk_deals == []

    def test_accelerating_deals_empty(self):
        eng = _engine()
        assert eng.accelerating_deals == []

    def test_requires_escalation_empty(self):
        eng = _engine()
        assert eng.requires_escalation == []

    def test_competitive_threats_empty(self):
        eng = _engine()
        assert eng.competitive_threats == []

    def test_accelerating_deals_included(self):
        eng = _engine()
        r = eng.analyze(_make_accelerating())
        if r.momentum_level == MomentumLevel.ACCELERATING:
            assert r in eng.accelerating_deals

    def test_non_stalled_not_in_stalled(self):
        eng = _engine()
        r = eng.analyze(_make_accelerating())
        if r.momentum_level != MomentumLevel.STALLED:
            assert r not in eng.stalled_deals

    def test_stalled_deal_in_stalled_deals(self):
        eng = _engine()
        r = eng.analyze(_make_stalled())
        if r.momentum_level == MomentumLevel.STALLED:
            assert r in eng.stalled_deals

    def test_stalled_deal_in_at_risk(self):
        eng = _engine()
        r = eng.analyze(_make_stalled())
        if r.momentum_level in (MomentumLevel.DECLINING, MomentumLevel.STALLED):
            assert r in eng.at_risk_deals

    def test_accelerating_not_in_at_risk(self):
        eng = _engine()
        r = eng.analyze(_make_accelerating())
        if r.momentum_level == MomentumLevel.ACCELERATING:
            assert r not in eng.at_risk_deals

    def test_requires_escalation_filter(self):
        eng = _engine()
        # Build a deal that triggers EXECUTIVE_ESCALATION
        inp = _make_base(
            champion_left=False,
            technical_blockers=0,
            competitor_demo_requested=False,
            days_in_stage=100,
            expected_days_in_stage=10,
            days_overdue=50,
            activities_last_14d=0,
            activities_last_30d=0,
            last_activity_days_ago=20,
            decision_maker_engaged_14d=True,
            exec_sponsor_engaged=True,
            champion_active=False,
            stage_regressions_90d=0,
            budget_confirmed=True,
            prior_momentum_score=10.0,
        )
        r = eng.analyze(inp)
        if r.momentum_action == MomentumAction.EXECUTIVE_ESCALATION:
            assert r in eng.requires_escalation
        else:
            assert r not in eng.requires_escalation

    def test_competitive_threat_filter(self):
        eng = _engine()
        inp = _make_base(
            competitor_demo_requested=True,
            champion_left=False,
            technical_blockers=0,
        )
        r = eng.analyze(inp)
        if r.stall_reason == StallReason.COMPETITIVE_THREAT:
            assert r in eng.competitive_threats
        else:
            assert r not in eng.competitive_threats

    def test_multiple_results_properties_correct(self):
        eng = _engine()
        eng.analyze(_make_accelerating())
        eng.analyze(_make_stalled())
        # Properties should only contain matching results
        for r in eng.stalled_deals:
            assert r.momentum_level == MomentumLevel.STALLED
        for r in eng.accelerating_deals:
            assert r.momentum_level == MomentumLevel.ACCELERATING
        for r in eng.at_risk_deals:
            assert r.momentum_level in (MomentumLevel.DECLINING, MomentumLevel.STALLED)

    def test_requires_escalation_only_escalation_actions(self):
        eng = _engine()
        eng.analyze(_make_accelerating())
        eng.analyze(_make_stalled())
        for r in eng.requires_escalation:
            assert r.momentum_action == MomentumAction.EXECUTIVE_ESCALATION

    def test_competitive_threats_only_competitive_stall(self):
        eng = _engine()
        eng.analyze(_make_accelerating())
        eng.analyze(_make_stalled())
        for r in eng.competitive_threats:
            assert r.stall_reason == StallReason.COMPETITIVE_THREAT


# ===========================================================================
# 13. SUMMARY
# ===========================================================================

class TestSummary:
    def test_empty_summary_has_11_keys(self):
        eng = _engine()
        s = eng.summary()
        assert len(s) == 11

    def test_empty_summary_total_zero(self):
        eng = _engine()
        assert eng.summary()["total"] == 0

    def test_empty_summary_level_counts_empty(self):
        eng = _engine()
        assert eng.summary()["level_counts"] == {}

    def test_empty_summary_stall_counts_empty(self):
        eng = _engine()
        assert eng.summary()["stall_counts"] == {}

    def test_empty_summary_trend_counts_empty(self):
        eng = _engine()
        assert eng.summary()["trend_counts"] == {}

    def test_empty_summary_action_counts_empty(self):
        eng = _engine()
        assert eng.summary()["action_counts"] == {}

    def test_empty_summary_avg_momentum_zero(self):
        eng = _engine()
        assert eng.summary()["avg_momentum_score"] == 0.0

    def test_empty_summary_avg_velocity_zero(self):
        eng = _engine()
        assert eng.summary()["avg_velocity_score"] == 0.0

    def test_empty_summary_avg_engagement_zero(self):
        eng = _engine()
        assert eng.summary()["avg_engagement_score"] == 0.0

    def test_empty_summary_avg_risk_zero(self):
        eng = _engine()
        assert eng.summary()["avg_risk_score"] == 0.0

    def test_empty_summary_at_risk_count_zero(self):
        eng = _engine()
        assert eng.summary()["at_risk_count"] == 0

    def test_empty_summary_escalation_count_zero(self):
        eng = _engine()
        assert eng.summary()["escalation_count"] == 0

    def test_summary_11_keys_after_analyze(self):
        eng = _engine()
        eng.analyze(_make_accelerating())
        assert len(eng.summary()) == 11

    def test_summary_total_correct(self):
        eng = _engine()
        eng.analyze(_make_accelerating())
        eng.analyze(_make_stalled())
        assert eng.summary()["total"] == 2

    def test_summary_level_counts_type_dict(self):
        eng = _engine()
        eng.analyze(_make_accelerating())
        assert isinstance(eng.summary()["level_counts"], dict)

    def test_summary_stall_counts_type_dict(self):
        eng = _engine()
        eng.analyze(_make_accelerating())
        assert isinstance(eng.summary()["stall_counts"], dict)

    def test_summary_trend_counts_type_dict(self):
        eng = _engine()
        eng.analyze(_make_accelerating())
        assert isinstance(eng.summary()["trend_counts"], dict)

    def test_summary_action_counts_type_dict(self):
        eng = _engine()
        eng.analyze(_make_accelerating())
        assert isinstance(eng.summary()["action_counts"], dict)

    def test_summary_level_counts_sums_to_total(self):
        eng = _engine()
        eng.analyze(_make_accelerating())
        eng.analyze(_make_stalled())
        s = eng.summary()
        assert sum(s["level_counts"].values()) == s["total"]

    def test_summary_stall_counts_sums_to_total(self):
        eng = _engine()
        eng.analyze(_make_accelerating())
        eng.analyze(_make_stalled())
        s = eng.summary()
        assert sum(s["stall_counts"].values()) == s["total"]

    def test_summary_trend_counts_sums_to_total(self):
        eng = _engine()
        eng.analyze(_make_accelerating())
        eng.analyze(_make_stalled())
        s = eng.summary()
        assert sum(s["trend_counts"].values()) == s["total"]

    def test_summary_action_counts_sums_to_total(self):
        eng = _engine()
        eng.analyze(_make_accelerating())
        eng.analyze(_make_stalled())
        s = eng.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_avg_momentum_is_float(self):
        eng = _engine()
        eng.analyze(_make_accelerating())
        assert isinstance(eng.summary()["avg_momentum_score"], float)

    def test_summary_avg_velocity_is_float(self):
        eng = _engine()
        eng.analyze(_make_accelerating())
        assert isinstance(eng.summary()["avg_velocity_score"], float)

    def test_summary_avg_engagement_is_float(self):
        eng = _engine()
        eng.analyze(_make_accelerating())
        assert isinstance(eng.summary()["avg_engagement_score"], float)

    def test_summary_avg_risk_is_float(self):
        eng = _engine()
        eng.analyze(_make_accelerating())
        assert isinstance(eng.summary()["avg_risk_score"], float)

    def test_summary_at_risk_count_matches_property(self):
        eng = _engine()
        eng.analyze(_make_accelerating())
        eng.analyze(_make_stalled())
        s = eng.summary()
        assert s["at_risk_count"] == len(eng.at_risk_deals)

    def test_summary_escalation_count_matches_property(self):
        eng = _engine()
        eng.analyze(_make_accelerating())
        eng.analyze(_make_stalled())
        s = eng.summary()
        assert s["escalation_count"] == len(eng.requires_escalation)

    def test_summary_avg_momentum_correct_single(self):
        eng = _engine()
        r = eng.analyze(_make_accelerating())
        s = eng.summary()
        assert s["avg_momentum_score"] == pytest.approx(r.momentum_score)

    def test_summary_all_score_averages_in_range(self):
        eng = _engine()
        eng.analyze(_make_accelerating())
        eng.analyze(_make_stalled())
        s = eng.summary()
        assert 0.0 <= s["avg_momentum_score"] <= 100.0
        assert 0.0 <= s["avg_velocity_score"] <= 100.0
        assert 0.0 <= s["avg_engagement_score"] <= 100.0
        assert 0.0 <= s["avg_risk_score"] <= 100.0


# ===========================================================================
# 14. RESET
# ===========================================================================

class TestReset:
    def test_reset_clears_results(self):
        eng = _engine()
        eng.analyze(_make_accelerating())
        eng.analyze(_make_stalled())
        assert len(eng.results) == 2
        eng.reset()
        assert len(eng.results) == 0

    def test_reset_clears_stalled_deals(self):
        eng = _engine()
        eng.analyze(_make_stalled())
        eng.reset()
        assert eng.stalled_deals == []

    def test_reset_clears_at_risk_deals(self):
        eng = _engine()
        eng.analyze(_make_stalled())
        eng.reset()
        assert eng.at_risk_deals == []

    def test_reset_allows_reuse(self):
        eng = _engine()
        eng.analyze(_make_accelerating())
        eng.reset()
        eng.analyze(_make_stalled())
        assert len(eng.results) == 1

    def test_reset_clears_summary(self):
        eng = _engine()
        eng.analyze(_make_accelerating())
        eng.reset()
        assert eng.summary()["total"] == 0

    def test_double_reset_safe(self):
        eng = _engine()
        eng.reset()
        eng.reset()
        assert eng.results == []

    def test_reset_then_reanalyze_correct_results(self):
        eng = _engine()
        eng.analyze(_make_accelerating())
        eng.reset()
        r = eng.analyze(_make_accelerating())
        assert r.deal_id == "acc"
        assert len(eng.results) == 1

    def test_results_start_empty(self):
        eng = _engine()
        assert eng.results == []


# ===========================================================================
# 15. ANALYZE - INTEGRATION
# ===========================================================================

class TestAnalyzeIntegration:
    def test_analyze_returns_result_type(self):
        eng = _engine()
        r = eng.analyze(_make_base())
        assert isinstance(r, DealMomentumResult)

    def test_analyze_appends_to_results(self):
        eng = _engine()
        assert len(eng.results) == 0
        eng.analyze(_make_base())
        assert len(eng.results) == 1

    def test_analyze_stores_correct_deal_id(self):
        eng = _engine()
        r = eng.analyze(_make_base(deal_id="unique123"))
        assert r.deal_id == "unique123"

    def test_analyze_scores_in_range(self):
        eng = _engine()
        r = eng.analyze(_make_base())
        assert 0.0 <= r.momentum_score <= 100.0
        assert 0.0 <= r.velocity_score <= 100.0
        assert 0.0 <= r.engagement_score <= 100.0
        assert 0.0 <= r.risk_score <= 100.0

    def test_analyze_produces_valid_level(self):
        eng = _engine()
        r = eng.analyze(_make_base())
        assert r.momentum_level in MomentumLevel

    def test_analyze_produces_valid_stall_reason(self):
        eng = _engine()
        r = eng.analyze(_make_base())
        assert r.stall_reason in StallReason

    def test_analyze_produces_valid_trend(self):
        eng = _engine()
        r = eng.analyze(_make_base())
        assert r.momentum_trend in MomentumTrend

    def test_analyze_produces_valid_action(self):
        eng = _engine()
        r = eng.analyze(_make_base())
        assert r.momentum_action in MomentumAction

    def test_analyze_indicators_is_list(self):
        eng = _engine()
        r = eng.analyze(_make_base())
        assert isinstance(r.momentum_indicators, list)

    def test_analyze_risk_signals_is_list(self):
        eng = _engine()
        r = eng.analyze(_make_base())
        assert isinstance(r.risk_signals, list)

    def test_analyze_recommended_actions_is_list(self):
        eng = _engine()
        r = eng.analyze(_make_base())
        assert isinstance(r.recommended_actions, list)

    def test_analyze_recommended_actions_not_empty(self):
        eng = _engine()
        r = eng.analyze(_make_base())
        assert len(r.recommended_actions) > 0


# ===========================================================================
# 16. ANALYZE_BATCH
# ===========================================================================

class TestAnalyzeBatch:
    def test_batch_returns_list(self):
        eng = _engine()
        results = eng.analyze_batch([_make_accelerating(), _make_stalled()])
        assert isinstance(results, list)

    def test_batch_processes_all_inputs(self):
        eng = _engine()
        results = eng.analyze_batch([_make_accelerating(), _make_stalled()])
        assert len(results) == 2

    def test_batch_sorted_by_momentum_score_desc(self):
        eng = _engine()
        results = eng.analyze_batch([_make_stalled(), _make_accelerating()])
        scores = [r.momentum_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_batch_empty_returns_empty(self):
        eng = _engine()
        results = eng.analyze_batch([])
        assert results == []

    def test_batch_accumulates_in_results(self):
        eng = _engine()
        eng.analyze_batch([_make_accelerating(), _make_stalled()])
        assert len(eng.results) == 2

    def test_batch_results_sorted_after_call(self):
        eng = _engine()
        inputs = [
            _make_base(deal_id="low", prior_momentum_score=5.0,
                       days_in_stage=100, expected_days_in_stage=5,
                       activities_last_14d=0, activities_last_30d=0,
                       last_activity_days_ago=30),
            _make_accelerating(),
        ]
        results = eng.analyze_batch(inputs)
        assert results[0].momentum_score >= results[1].momentum_score

    def test_batch_single_item(self):
        eng = _engine()
        results = eng.analyze_batch([_make_accelerating()])
        assert len(results) == 1


# ===========================================================================
# 17. END-TO-END SCENARIOS
# ===========================================================================

class TestEndToEndAccelerating:
    def setup_method(self):
        self.eng = _engine()
        self.inp = _make_accelerating()
        self.r = self.eng.analyze(self.inp)

    def test_deal_id_matches(self):
        assert self.r.deal_id == "acc"

    def test_momentum_score_above_60(self):
        # Fully accelerating deal should score high
        assert self.r.momentum_score >= 60.0

    def test_velocity_score_reasonable(self):
        assert self.r.velocity_score >= 50.0

    def test_engagement_score_high(self):
        assert self.r.engagement_score >= 50.0

    def test_risk_score_low(self):
        assert self.r.risk_score == 0.0

    def test_momentum_level_positive_or_better(self):
        assert self.r.momentum_level in (
            MomentumLevel.ACCELERATING,
            MomentumLevel.POSITIVE,
            MomentumLevel.NEUTRAL,
        )

    def test_no_champion_left_stall(self):
        assert self.r.stall_reason != StallReason.CHAMPION_LEFT

    def test_to_dict_works(self):
        d = self.r.to_dict()
        assert len(d) == 15

    def test_result_in_engine_results(self):
        assert self.r in self.eng.results

    def test_indicators_non_empty(self):
        assert len(self.r.momentum_indicators) > 0


class TestEndToEndStalled:
    def setup_method(self):
        self.eng = _engine()
        self.inp = _make_stalled()
        self.r = self.eng.analyze(self.inp)

    def test_deal_id_matches(self):
        assert self.r.deal_id == "stl"

    def test_momentum_score_low(self):
        assert self.r.momentum_score < 45.0

    def test_risk_score_very_high(self):
        # champion_left(30) + demo_requested(25) + objections(20cap) + blockers(20cap) + budget(15) + regressions(10cap) > 100 → clamped
        assert self.r.risk_score == 100.0

    def test_momentum_level_bad(self):
        assert self.r.momentum_level in (
            MomentumLevel.STALLED,
            MomentumLevel.DECLINING,
            MomentumLevel.STALLING,
        )

    def test_stall_reason_champion_left(self):
        # champion_left is highest priority
        assert self.r.stall_reason == StallReason.CHAMPION_LEFT

    def test_momentum_action_champion_recovery_or_close(self):
        # champion_left → CHAMPION_RECOVERY (path 1)
        assert self.r.momentum_action in (
            MomentumAction.CHAMPION_RECOVERY,
            MomentumAction.CLOSE_OR_ABANDON,
        )

    def test_risk_signals_non_empty(self):
        assert len(self.r.risk_signals) > 0

    def test_recommended_actions_non_empty(self):
        assert len(self.r.recommended_actions) > 0


class TestBatchSortingEndToEnd:
    def test_three_deals_sorted_desc(self):
        eng = _engine()
        inputs = [
            _make_stalled(),
            _make_accelerating(),
            _make_base(deal_id="mid"),
        ]
        results = eng.analyze_batch(inputs)
        scores = [r.momentum_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_batch_includes_all_deals(self):
        eng = _engine()
        deal_ids = ["d1", "d2", "d3", "d4", "d5"]
        inputs = [_make_base(deal_id=did) for did in deal_ids]
        results = eng.analyze_batch(inputs)
        result_ids = {r.deal_id for r in results}
        assert result_ids == set(deal_ids)

    def test_batch_summary_consistent(self):
        eng = _engine()
        eng.analyze_batch([_make_accelerating(), _make_stalled()])
        s = eng.summary()
        assert s["total"] == 2


# ===========================================================================
# 18. EDGE CASES
# ===========================================================================

class TestEdgeCases:
    def test_all_flags_off_stable(self):
        eng = _engine()
        r = eng.analyze(_make_base())
        assert r is not None

    def test_prior_score_zero(self):
        eng = _engine()
        r = eng.analyze(_make_base(prior_momentum_score=0.0))
        assert 0.0 <= r.momentum_score <= 100.0

    def test_prior_score_100(self):
        eng = _engine()
        r = eng.analyze(_make_base(prior_momentum_score=100.0))
        assert 0.0 <= r.momentum_score <= 100.0

    def test_days_to_close_zero(self):
        eng = _engine()
        r = eng.analyze(_make_base(days_to_close=0))
        assert r is not None

    def test_next_step_days_out_none_no_far_penalty(self):
        eng = _engine()
        # next_step_defined=True but days_out=None → should NOT apply far-out penalty
        inp = _make_base(next_step_defined=True, next_step_days_out=None,
                         activities_last_14d=0, activities_last_30d=0,
                         last_activity_days_ago=5,
                         decision_maker_engaged_14d=False, champion_active=False,
                         exec_sponsor_engaged=False, champion_left=False)
        score = eng._engagement_score(inp)
        assert score == pytest.approx(10.0)  # just the next_step bonus

    def test_stage_advances_zero(self):
        eng = _engine()
        vel = eng._velocity_score(_make_base(stage_advances_90d=0, days_overdue=0))
        assert vel == pytest.approx(50.0)

    def test_expected_days_zero_no_overrun_penalty(self):
        eng = _engine()
        vel = eng._velocity_score(_make_base(expected_days_in_stage=0, days_in_stage=100))
        assert vel == pytest.approx(50.0)

    def test_activities_14d_equals_half_30d_exact(self):
        # 14d=2, 30d=4 → half=2 → 14d >= half → trend bonus
        eng = _engine()
        score = eng._engagement_score(_make_base(
            activities_last_14d=2, activities_last_30d=4,
            last_activity_days_ago=5,
            decision_maker_engaged_14d=False, champion_active=False,
            exec_sponsor_engaged=False, champion_left=False, next_step_defined=False,
        ))
        # 2*6=12, +15 trend = 27
        assert score == pytest.approx(27.0)

    def test_multiple_analyses_accumulate(self):
        eng = _engine()
        for i in range(5):
            eng.analyze(_make_base(deal_id=f"d{i}"))
        assert len(eng.results) == 5

    def test_analyze_and_reset_and_batch(self):
        eng = _engine()
        eng.analyze(_make_accelerating())
        eng.reset()
        batch_results = eng.analyze_batch([_make_base(deal_id="n1"), _make_base(deal_id="n2")])
        assert len(batch_results) == 2
        assert len(eng.results) == 2

    def test_velocity_overrun_exactly_equal_expected(self):
        # days_in_stage == expected → overrun=0 → no penalty
        eng = _engine()
        vel = eng._velocity_score(_make_base(
            days_in_stage=15, expected_days_in_stage=15,
            days_overdue=0, stage_advances_90d=0, stage_regressions_90d=0,
        ))
        assert vel == pytest.approx(50.0)

    def test_risk_score_zero_when_all_clear(self):
        eng = _engine()
        risk = eng._risk_score(_make_base(
            champion_left=False, competitor_demo_requested=False,
            competitor_mentioned=False, objections_unresolved=0,
            technical_blockers=0, budget_confirmed=True,
            days_to_close=100, stage_regressions_90d=0,
        ))
        assert risk == 0.0

    def test_engagement_score_clamped_maximum(self):
        eng = _engine()
        score = eng._engagement_score(_make_base(
            activities_last_14d=10, activities_last_30d=4,
            last_activity_days_ago=1,
            decision_maker_engaged_14d=True, champion_active=True,
            exec_sponsor_engaged=True, champion_left=False,
            next_step_defined=True, next_step_days_out=5,
        ))
        assert score == 100.0

    def test_momentum_score_rounded(self):
        eng = _engine()
        r = eng.analyze(_make_base())
        # score should equal round(score, 1)
        assert r.momentum_score == round(r.momentum_score, 1)

    def test_velocity_score_rounded(self):
        eng = _engine()
        r = eng.analyze(_make_base())
        assert r.velocity_score == round(r.velocity_score, 1)

    def test_to_dict_momentum_level_valid_value(self):
        eng = _engine()
        d = eng.analyze(_make_base()).to_dict()
        valid_values = {m.value for m in MomentumLevel}
        assert d["momentum_level"] in valid_values

    def test_to_dict_stall_reason_valid_value(self):
        eng = _engine()
        d = eng.analyze(_make_base()).to_dict()
        valid_values = {m.value for m in StallReason}
        assert d["stall_reason"] in valid_values

    def test_to_dict_trend_valid_value(self):
        eng = _engine()
        d = eng.analyze(_make_base()).to_dict()
        valid_values = {m.value for m in MomentumTrend}
        assert d["momentum_trend"] in valid_values

    def test_to_dict_action_valid_value(self):
        eng = _engine()
        d = eng.analyze(_make_base()).to_dict()
        valid_values = {m.value for m in MomentumAction}
        assert d["momentum_action"] in valid_values


# ===========================================================================
# 19. SCORING FORMULA VERIFICATION
# ===========================================================================

class TestScoringFormulas:
    """Verify each sub-score formula with explicit manual calculations."""

    def test_velocity_stage_overrun_proportional(self):
        eng = _engine()
        # overrun=5, expected=10 → penalty = 5/10 * 35 = 17.5
        vel = eng._velocity_score(_make_base(
            days_in_stage=15, expected_days_in_stage=10,
            days_overdue=0, stage_advances_90d=0, stage_regressions_90d=0,
        ))
        assert vel == pytest.approx(50.0 - 17.5)

    def test_velocity_overdue_linear(self):
        eng = _engine()
        # overdue=3 → 3*2=6 penalty → 50-6=44
        vel = eng._velocity_score(_make_base(
            days_in_stage=10, expected_days_in_stage=10,
            days_overdue=3, stage_advances_90d=0, stage_regressions_90d=0,
        ))
        assert vel == pytest.approx(50.0 - 6.0)

    def test_engagement_full_stakeholder_stack(self):
        eng = _engine()
        # DM(20) + champion(15) + exec(10) + recency_bonus(10) + next_step(10) = 65
        score = eng._engagement_score(_make_base(
            activities_last_14d=0, activities_last_30d=0,
            last_activity_days_ago=1,
            decision_maker_engaged_14d=True,
            champion_active=True,
            exec_sponsor_engaged=True,
            champion_left=False,
            next_step_defined=True, next_step_days_out=5,
        ))
        assert score == pytest.approx(65.0)

    def test_risk_combined_champion_and_objections(self):
        eng = _engine()
        # champion_left(30) + objections(2*8=16) = 46
        score = eng._risk_score(_make_base(
            champion_left=True, competitor_demo_requested=False,
            competitor_mentioned=False, objections_unresolved=2,
            technical_blockers=0, budget_confirmed=True,
            days_to_close=100, stage_regressions_90d=0,
        ))
        assert score == pytest.approx(46.0)

    def test_momentum_formula_explicit(self):
        eng = _engine()
        # vel=80, eng=90, risk=10, prior=70
        # raw = 80*0.35 + 90*0.40 + 90*0.25 = 28+36+22.5=86.5
        # blended = 86.5*0.70 + 70*0.30 = 60.55+21=81.55 → round to 81.6
        result = eng._momentum_score(80.0, 90.0, 10.0, 70.0)
        assert result == pytest.approx(81.6, abs=0.1)

    def test_velocity_two_advances_two_bonuses(self):
        eng = _engine()
        # 2 advances = min(20, 16) = 16; proposal(10) + pricing(8) = 18; 50+16+18=84
        vel = eng._velocity_score(_make_base(
            days_in_stage=5, expected_days_in_stage=10,
            days_overdue=0,
            stage_advances_90d=2, stage_regressions_90d=0,
            proposal_sent=True, pricing_discussed=True, poc_started=False,
        ))
        assert vel == pytest.approx(84.0)

    def test_risk_all_six_contributors(self):
        eng = _engine()
        # champion_left(30) + demo_requested(25) + objections(min(20,3*8)=20) + blockers(min(20,2*10)=20) + budget(15) + regressions(min(10,2*5)=10) = 120 → clamped 100
        score = eng._risk_score(_make_base(
            champion_left=True, competitor_demo_requested=True,
            competitor_mentioned=False, objections_unresolved=3,
            technical_blockers=2, budget_confirmed=False,
            days_to_close=20, stage_regressions_90d=2,
        ))
        assert score == 100.0


# ===========================================================================
# 20. STALL REASON EDGE CASES
# ===========================================================================

class TestStallReasonEdgeCases:
    def test_champion_active_prevents_stakeholder_change(self):
        eng = _engine()
        # STALLING level + champion_active=True → should return DECISION_DELAYED, not STAKEHOLDER_CHANGE
        reason = eng._stall_reason(
            _make_base(
                champion_left=False, technical_blockers=0,
                competitor_demo_requested=False, stage_regressions_90d=0,
                budget_confirmed=True, days_overdue=0,
                decision_maker_engaged_14d=False, champion_active=True,
            ),
            MomentumLevel.STALLING,
        )
        assert reason == StallReason.DECISION_DELAYED

    def test_dm_engaged_prevents_stakeholder_change(self):
        eng = _engine()
        reason = eng._stall_reason(
            _make_base(
                champion_left=False, technical_blockers=0,
                competitor_demo_requested=False, stage_regressions_90d=0,
                budget_confirmed=True, days_overdue=0,
                decision_maker_engaged_14d=True, champion_active=False,
            ),
            MomentumLevel.DECLINING,
        )
        assert reason == StallReason.DECISION_DELAYED

    def test_neutral_level_not_stakeholder_change(self):
        eng = _engine()
        reason = eng._stall_reason(
            _make_base(
                champion_left=False, technical_blockers=0,
                competitor_demo_requested=False, stage_regressions_90d=0,
                budget_confirmed=True, days_overdue=0,
                decision_maker_engaged_14d=False, champion_active=False,
            ),
            MomentumLevel.NEUTRAL,
        )
        assert reason == StallReason.NO_STALL

    def test_budget_not_confirmed_beyond_14_no_budget_frozen(self):
        eng = _engine()
        reason = eng._stall_reason(
            _make_base(
                champion_left=False, technical_blockers=0,
                competitor_demo_requested=False, stage_regressions_90d=0,
                budget_confirmed=False, days_to_close=15, days_overdue=0,
                decision_maker_engaged_14d=False, champion_active=False,
            ),
            MomentumLevel.STALLING,
        )
        # days_to_close=15 > 14 → no budget_frozen; falls to stakeholder_change
        assert reason != StallReason.BUDGET_FROZEN

    def test_overdue_31_triggers_decision_delayed_even_high_level(self):
        eng = _engine()
        reason = eng._stall_reason(
            _make_base(
                champion_left=False, technical_blockers=0,
                competitor_demo_requested=False, stage_regressions_90d=0,
                budget_confirmed=True, days_overdue=31,
            ),
            MomentumLevel.POSITIVE,
        )
        assert reason == StallReason.DECISION_DELAYED


# ===========================================================================
# 21. MOMENTUM TREND EDGE CASES
# ===========================================================================

class TestMomentumTrendEdgeCases:
    def test_critical_requires_both_conditions(self):
        eng = _engine()
        # delta=-15 but level=POSITIVE → not critical
        trend = eng._momentum_trend(35.0, 50.0, MomentumLevel.POSITIVE)
        assert trend == MomentumTrend.DETERIORATING

    def test_improving_beats_all_other_checks(self):
        eng = _engine()
        # Even with declining level, +10 delta → IMPROVING
        trend = eng._momentum_trend(25.0, 15.0, MomentumLevel.DECLINING)
        assert trend == MomentumTrend.IMPROVING

    def test_stable_for_small_positive_delta(self):
        eng = _engine()
        trend = eng._momentum_trend(53.0, 50.0, MomentumLevel.NEUTRAL)
        assert trend == MomentumTrend.STABLE

    def test_deteriorating_not_critical_for_stalling_level(self):
        eng = _engine()
        # STALLING is not in (DECLINING, STALLED) → not critical even with -15
        trend = eng._momentum_trend(25.0, 40.0, MomentumLevel.STALLING)
        assert trend == MomentumTrend.DETERIORATING


# ===========================================================================
# 22. ADDITIONAL COVERAGE TESTS
# ===========================================================================

class TestAdditionalCoverage:
    def test_deal_result_fields_populated(self):
        eng = _engine()
        r = eng.analyze(_make_base())
        assert r.rep_id == "r1"
        assert r.rep_name == "Rep One"
        assert r.account_name == "Acme Corp"

    def test_analyze_multiple_engines_independent(self):
        eng1 = _engine()
        eng2 = _engine()
        eng1.analyze(_make_accelerating())
        assert len(eng1.results) == 1
        assert len(eng2.results) == 0

    def test_momentum_level_returns_enum(self):
        eng = _engine()
        level = eng._momentum_level(55.0)
        assert isinstance(level, MomentumLevel)

    def test_stall_reason_returns_enum(self):
        eng = _engine()
        reason = eng._stall_reason(_make_base(), MomentumLevel.NEUTRAL)
        assert isinstance(reason, StallReason)

    def test_momentum_trend_returns_enum(self):
        eng = _engine()
        trend = eng._momentum_trend(50.0, 50.0, MomentumLevel.NEUTRAL)
        assert isinstance(trend, MomentumTrend)

    def test_momentum_action_returns_enum(self):
        eng = _engine()
        action = eng._momentum_action(
            _make_base(), MomentumLevel.NEUTRAL, StallReason.NO_STALL, MomentumTrend.STABLE
        )
        assert isinstance(action, MomentumAction)

    def test_summary_returns_dict(self):
        eng = _engine()
        assert isinstance(eng.summary(), dict)

    def test_analyze_batch_returns_list(self):
        eng = _engine()
        result = eng.analyze_batch([])
        assert isinstance(result, list)

    def test_result_repname_matches(self):
        eng = _engine()
        r = eng.analyze(_make_base(rep_name="Alice"))
        assert r.rep_name == "Alice"

    def test_engagement_score_trend_boundary_activities_equal(self):
        eng = _engine()
        # 14d=2, 30d=4 → half=2.0 → 14d(2) >= half(2.0) → accelerating trend: +15
        score = eng._engagement_score(_make_base(
            activities_last_14d=2, activities_last_30d=4,
            last_activity_days_ago=5,
            decision_maker_engaged_14d=False, champion_active=False,
            exec_sponsor_engaged=False, champion_left=False, next_step_defined=False,
        ))
        # 2*6=12, +15 = 27
        assert score == pytest.approx(27.0)

    def test_stall_reason_technical_blocker_3(self):
        eng = _engine()
        reason = eng._stall_reason(
            _make_base(technical_blockers=3, champion_left=False),
            MomentumLevel.STALLING,
        )
        assert reason == StallReason.TECHNICAL_BLOCKER

    def test_risk_stage_regressions_exactly_2(self):
        eng = _engine()
        risk = eng._risk_score(_make_base(
            stage_regressions_90d=2, budget_confirmed=True,
            champion_left=False, competitor_demo_requested=False,
            competitor_mentioned=False, objections_unresolved=0,
            technical_blockers=0, days_to_close=100,
        ))
        assert risk == pytest.approx(10.0)

    def test_velocity_all_zero_no_bonuses(self):
        eng = _engine()
        vel = eng._velocity_score(_make_base(
            days_in_stage=10, expected_days_in_stage=10,
            days_overdue=0, stage_advances_90d=0, stage_regressions_90d=0,
            proposal_sent=False, pricing_discussed=False, poc_started=False,
        ))
        assert vel == pytest.approx(50.0)

    def test_engagement_last_activity_4_days_neutral_recency(self):
        eng = _engine()
        # 4 days ago → not <= 3, not > 7, not > 14 → no recency effect
        score = eng._engagement_score(_make_base(
            activities_last_14d=0, activities_last_30d=0,
            last_activity_days_ago=4,
            decision_maker_engaged_14d=False, champion_active=False,
            exec_sponsor_engaged=False, champion_left=False, next_step_defined=False,
        ))
        assert score == pytest.approx(0.0)

    def test_velocity_single_regression(self):
        eng = _engine()
        vel = eng._velocity_score(_make_base(
            days_in_stage=10, expected_days_in_stage=10,
            days_overdue=0, stage_advances_90d=0, stage_regressions_90d=1,
            proposal_sent=False, pricing_discussed=False, poc_started=False,
        ))
        assert vel == pytest.approx(40.0)

    def test_engagement_champion_left_overcomes_all_bonuses_clamp(self):
        eng = _engine()
        # max bonuses = 30+15+20+15+10+10+10 = 110, minus 30 = 80
        score = eng._engagement_score(_make_base(
            activities_last_14d=5, activities_last_30d=4,
            last_activity_days_ago=1,
            decision_maker_engaged_14d=True, champion_active=True,
            exec_sponsor_engaged=True, champion_left=True,
            next_step_defined=True, next_step_days_out=5,
        ))
        # 30+15+20+15+10+10+10-30=80
        assert score == pytest.approx(80.0)

    def test_summary_level_counts_keys_are_strings(self):
        eng = _engine()
        eng.analyze(_make_base())
        s = eng.summary()
        for k in s["level_counts"]:
            assert isinstance(k, str)

    def test_summary_stall_counts_keys_are_strings(self):
        eng = _engine()
        eng.analyze(_make_base())
        s = eng.summary()
        for k in s["stall_counts"]:
            assert isinstance(k, str)
