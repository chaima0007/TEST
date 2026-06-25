"""Comprehensive pytest test suite for swarm/intelligence/win_loss_intelligence.py.

Run from /home/user/TEST with:
    python -m pytest swarm/tests/test_win_loss_intelligence.py -v
"""

from __future__ import annotations

import pytest

from swarm.intelligence.win_loss_intelligence import (
    DealOutcome,
    ExecutionQuality,
    WinLossAction,
    WinLossInput,
    WinLossResult,
    WinLossIntelligenceEngine,
    _execution_score,
    _execution_quality,
    _cycle_efficiency,
    _discount_pressure,
    _wl_action,
    _build_signals,
)


# ---------------------------------------------------------------------------
# Helpers / shared fixtures
# ---------------------------------------------------------------------------

def make_input(
    deal_id: str = "D001",
    deal_name: str = "Test Deal",
    account_name: str = "Acme",
    segment: str = "enterprise",
    arr_eur: float = 100_000.0,
    outcome: DealOutcome = DealOutcome.WON,
    had_champion: bool = True,
    executive_engaged: bool = True,
    poc_done: bool = True,
    budget_confirmed: bool = True,
    decision_maker_met: bool = True,
    multi_thread_count: int = 3,
    next_step_always_present: bool = True,
    days_to_outcome: int = 90,
    expected_cycle_days: int = 120,
    discount_given_pct: float = 0.0,
    loss_reason: str = "none",
    competitor_lost_to: str = "",
    num_meetings: int = 6,
    objections_handled: int = 3,
    references_provided: bool = True,
    case_study_shared: bool = True,
) -> WinLossInput:
    """Factory with sensible defaults (perfect-execution won deal)."""
    return WinLossInput(
        deal_id=deal_id,
        deal_name=deal_name,
        account_name=account_name,
        segment=segment,
        arr_eur=arr_eur,
        outcome=outcome,
        had_champion=had_champion,
        executive_engaged=executive_engaged,
        poc_done=poc_done,
        budget_confirmed=budget_confirmed,
        decision_maker_met=decision_maker_met,
        multi_thread_count=multi_thread_count,
        next_step_always_present=next_step_always_present,
        days_to_outcome=days_to_outcome,
        expected_cycle_days=expected_cycle_days,
        discount_given_pct=discount_given_pct,
        loss_reason=loss_reason,
        competitor_lost_to=competitor_lost_to,
        num_meetings=num_meetings,
        objections_handled=objections_handled,
        references_provided=references_provided,
        case_study_shared=case_study_shared,
    )


@pytest.fixture
def perfect_won_input() -> WinLossInput:
    """All flags True, multi_thread=3 → score 100, EXCELLENT, WON."""
    return make_input()


@pytest.fixture
def zero_input() -> WinLossInput:
    """All flags False, multi_thread=0 → score 0, POOR."""
    return make_input(
        had_champion=False,
        executive_engaged=False,
        poc_done=False,
        budget_confirmed=False,
        decision_maker_met=False,
        multi_thread_count=0,
        next_step_always_present=False,
        outcome=DealOutcome.LOST,
    )


@pytest.fixture
def engine() -> WinLossIntelligenceEngine:
    return WinLossIntelligenceEngine()


# ===========================================================================
# 1. TestDealOutcomeEnum
# ===========================================================================

class TestDealOutcomeEnum:

    def test_won_value(self):
        assert DealOutcome.WON.value == "won"

    def test_lost_value(self):
        assert DealOutcome.LOST.value == "lost"

    def test_no_decision_value(self):
        assert DealOutcome.NO_DECISION.value == "no_decision"

    def test_is_string_enum(self):
        assert isinstance(DealOutcome.WON, str)

    def test_members_count(self):
        assert len(DealOutcome) == 3

    def test_equality_with_string(self):
        assert DealOutcome.WON == "won"

    def test_from_value_won(self):
        assert DealOutcome("won") == DealOutcome.WON

    def test_from_value_lost(self):
        assert DealOutcome("lost") == DealOutcome.LOST

    def test_from_value_no_decision(self):
        assert DealOutcome("no_decision") == DealOutcome.NO_DECISION

    def test_invalid_value_raises(self):
        with pytest.raises(ValueError):
            DealOutcome("invalid")


# ===========================================================================
# 2. TestExecutionQualityEnum
# ===========================================================================

class TestExecutionQualityEnum:

    def test_excellent_value(self):
        assert ExecutionQuality.EXCELLENT.value == "excellent"

    def test_good_value(self):
        assert ExecutionQuality.GOOD.value == "good"

    def test_fair_value(self):
        assert ExecutionQuality.FAIR.value == "fair"

    def test_poor_value(self):
        assert ExecutionQuality.POOR.value == "poor"

    def test_is_string_enum(self):
        assert isinstance(ExecutionQuality.EXCELLENT, str)

    def test_members_count(self):
        assert len(ExecutionQuality) == 4

    def test_from_value_excellent(self):
        assert ExecutionQuality("excellent") == ExecutionQuality.EXCELLENT

    def test_from_value_poor(self):
        assert ExecutionQuality("poor") == ExecutionQuality.POOR

    def test_equality_with_string(self):
        assert ExecutionQuality.GOOD == "good"

    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            ExecutionQuality("bad")


# ===========================================================================
# 3. TestWinLossActionEnum
# ===========================================================================

class TestWinLossActionEnum:

    def test_replicate_value(self):
        assert WinLossAction.REPLICATE.value == "replicate"

    def test_debrief_value(self):
        assert WinLossAction.DEBRIEF.value == "debrief"

    def test_investigate_value(self):
        assert WinLossAction.INVESTIGATE.value == "investigate"

    def test_coach_value(self):
        assert WinLossAction.COACH.value == "coach"

    def test_is_string_enum(self):
        assert isinstance(WinLossAction.REPLICATE, str)

    def test_members_count(self):
        assert len(WinLossAction) == 4

    def test_from_value(self):
        assert WinLossAction("coach") == WinLossAction.COACH

    def test_equality_string(self):
        assert WinLossAction.DEBRIEF == "debrief"

    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            WinLossAction("noop")


# ===========================================================================
# 4. TestWinLossInputDataclass
# ===========================================================================

class TestWinLossInputDataclass:

    def test_instantiation(self, perfect_won_input):
        assert perfect_won_input.deal_id == "D001"

    def test_outcome_field(self, perfect_won_input):
        assert perfect_won_input.outcome == DealOutcome.WON

    def test_arr_eur_field(self, perfect_won_input):
        assert perfect_won_input.arr_eur == 100_000.0

    def test_bool_fields_true(self, perfect_won_input):
        assert perfect_won_input.had_champion is True
        assert perfect_won_input.executive_engaged is True
        assert perfect_won_input.poc_done is True
        assert perfect_won_input.budget_confirmed is True
        assert perfect_won_input.decision_maker_met is True

    def test_multi_thread_count(self, perfect_won_input):
        assert perfect_won_input.multi_thread_count == 3

    def test_timeline_fields(self, perfect_won_input):
        assert perfect_won_input.days_to_outcome == 90
        assert perfect_won_input.expected_cycle_days == 120

    def test_discount_field(self, perfect_won_input):
        assert perfect_won_input.discount_given_pct == 0.0

    def test_all_fields_accessible(self, perfect_won_input):
        # Ensure every declared field is reachable
        for field in [
            "deal_id", "deal_name", "account_name", "segment", "arr_eur", "outcome",
            "had_champion", "executive_engaged", "poc_done", "budget_confirmed",
            "decision_maker_met", "multi_thread_count", "next_step_always_present",
            "days_to_outcome", "expected_cycle_days", "discount_given_pct",
            "loss_reason", "competitor_lost_to", "num_meetings",
            "objections_handled", "references_provided", "case_study_shared",
        ]:
            assert hasattr(perfect_won_input, field)

    def test_zero_input_fields(self, zero_input):
        assert zero_input.had_champion is False
        assert zero_input.multi_thread_count == 0

    def test_custom_segment(self):
        inp = make_input(segment="smb")
        assert inp.segment == "smb"

    def test_loss_reason_field(self):
        inp = make_input(loss_reason="price", outcome=DealOutcome.LOST)
        assert inp.loss_reason == "price"

    def test_competitor_field(self):
        inp = make_input(competitor_lost_to="Salesforce")
        assert inp.competitor_lost_to == "Salesforce"


# ===========================================================================
# 5. TestWinLossResultToDict
# ===========================================================================

class TestWinLossResultToDict:

    def test_to_dict_returns_dict(self, engine, perfect_won_input):
        result = engine.analyze(perfect_won_input)
        d = result.to_dict()
        assert isinstance(d, dict)

    def test_to_dict_outcome_is_string(self, engine, perfect_won_input):
        d = engine.analyze(perfect_won_input).to_dict()
        assert isinstance(d["outcome"], str)
        assert d["outcome"] == "won"

    def test_to_dict_execution_quality_is_string(self, engine, perfect_won_input):
        d = engine.analyze(perfect_won_input).to_dict()
        assert isinstance(d["execution_quality"], str)

    def test_to_dict_wl_action_is_string(self, engine, perfect_won_input):
        d = engine.analyze(perfect_won_input).to_dict()
        assert isinstance(d["wl_action"], str)

    def test_to_dict_contains_all_keys(self, engine, perfect_won_input):
        d = engine.analyze(perfect_won_input).to_dict()
        expected_keys = {
            "deal_id", "deal_name", "account_name", "segment", "arr_eur",
            "outcome", "execution_quality", "wl_action", "execution_score",
            "cycle_efficiency_pct", "discount_pressure",
            "win_patterns", "loss_factors", "process_gaps", "coaching_insights",
        }
        assert expected_keys.issubset(d.keys())

    def test_to_dict_win_patterns_is_list(self, engine, perfect_won_input):
        d = engine.analyze(perfect_won_input).to_dict()
        assert isinstance(d["win_patterns"], list)

    def test_to_dict_loss_factors_is_list(self, engine, zero_input):
        d = engine.analyze(zero_input).to_dict()
        assert isinstance(d["loss_factors"], list)

    def test_to_dict_execution_score_numeric(self, engine, perfect_won_input):
        d = engine.analyze(perfect_won_input).to_dict()
        assert isinstance(d["execution_score"], (int, float))

    def test_to_dict_arr_eur(self, engine, perfect_won_input):
        d = engine.analyze(perfect_won_input).to_dict()
        assert d["arr_eur"] == 100_000.0

    def test_to_dict_lost_outcome(self, engine, zero_input):
        d = engine.analyze(zero_input).to_dict()
        assert d["outcome"] == "lost"


# ===========================================================================
# 6. TestExecutionScoreZero
# ===========================================================================

class TestExecutionScoreZero:

    def test_all_false_score_is_zero(self, zero_input):
        assert _execution_score(zero_input) == 0.0

    def test_zero_is_float(self, zero_input):
        assert isinstance(_execution_score(zero_input), float)

    def test_zero_clamped_not_negative(self, zero_input):
        assert _execution_score(zero_input) >= 0.0

    def test_multi_thread_zero_no_bonus(self):
        inp = make_input(
            had_champion=False, executive_engaged=False, poc_done=False,
            budget_confirmed=False, decision_maker_met=False,
            multi_thread_count=0, next_step_always_present=False,
        )
        assert _execution_score(inp) == 0.0

    def test_multi_thread_one_no_bonus(self):
        inp = make_input(
            had_champion=False, executive_engaged=False, poc_done=False,
            budget_confirmed=False, decision_maker_met=False,
            multi_thread_count=1, next_step_always_present=False,
        )
        assert _execution_score(inp) == 0.0


# ===========================================================================
# 7. TestExecutionScoreMax
# ===========================================================================

class TestExecutionScoreMax:

    def test_all_true_multi3_score_100(self, perfect_won_input):
        assert _execution_score(perfect_won_input) == 100.0

    def test_max_score_clamped(self, perfect_won_input):
        assert _execution_score(perfect_won_input) <= 100.0

    def test_champion_contributes_20(self):
        only_champion = make_input(
            had_champion=True, executive_engaged=False, poc_done=False,
            budget_confirmed=False, decision_maker_met=False,
            multi_thread_count=0, next_step_always_present=False,
        )
        assert _execution_score(only_champion) == 20.0

    def test_executive_contributes_15(self):
        inp = make_input(
            had_champion=False, executive_engaged=True, poc_done=False,
            budget_confirmed=False, decision_maker_met=False,
            multi_thread_count=0, next_step_always_present=False,
        )
        assert _execution_score(inp) == 15.0

    def test_multi_thread_3_contributes_10(self):
        inp = make_input(
            had_champion=False, executive_engaged=False, poc_done=False,
            budget_confirmed=False, decision_maker_met=False,
            multi_thread_count=3, next_step_always_present=False,
        )
        assert _execution_score(inp) == 10.0

    def test_next_step_contributes_10(self):
        inp = make_input(
            had_champion=False, executive_engaged=False, poc_done=False,
            budget_confirmed=False, decision_maker_met=False,
            multi_thread_count=0, next_step_always_present=True,
        )
        assert _execution_score(inp) == 10.0

    def test_all_true_multi5_still_100(self):
        inp = make_input(multi_thread_count=5)
        assert _execution_score(inp) == 100.0


# ===========================================================================
# 8. TestExecutionScorePartial
# ===========================================================================

class TestExecutionScorePartial:

    def test_champion_plus_exec_equals_35(self):
        inp = make_input(
            had_champion=True, executive_engaged=True, poc_done=False,
            budget_confirmed=False, decision_maker_met=False,
            multi_thread_count=0, next_step_always_present=False,
        )
        assert _execution_score(inp) == 35.0

    def test_multi_thread_2_contributes_5(self):
        inp = make_input(
            had_champion=False, executive_engaged=False, poc_done=False,
            budget_confirmed=False, decision_maker_met=False,
            multi_thread_count=2, next_step_always_present=False,
        )
        assert _execution_score(inp) == 5.0

    def test_champion_plus_multi2_equals_25(self):
        inp = make_input(
            had_champion=True, executive_engaged=False, poc_done=False,
            budget_confirmed=False, decision_maker_met=False,
            multi_thread_count=2, next_step_always_present=False,
        )
        assert _execution_score(inp) == 25.0

    def test_all_except_champion_score_80(self):
        # exec(15)+poc(15)+budget(15)+dm(15)+multi3(10)+next(10) = 80
        inp = make_input(
            had_champion=False, executive_engaged=True, poc_done=True,
            budget_confirmed=True, decision_maker_met=True,
            multi_thread_count=3, next_step_always_present=True,
        )
        assert _execution_score(inp) == 80.0

    def test_poc_budget_dm_equals_45(self):
        inp = make_input(
            had_champion=False, executive_engaged=False, poc_done=True,
            budget_confirmed=True, decision_maker_met=True,
            multi_thread_count=0, next_step_always_present=False,
        )
        assert _execution_score(inp) == 45.0

    def test_score_returns_float(self):
        inp = make_input(multi_thread_count=2)
        score = _execution_score(inp)
        assert isinstance(score, float)

    def test_champion_plus_next_step_equals_30(self):
        inp = make_input(
            had_champion=True, executive_engaged=False, poc_done=False,
            budget_confirmed=False, decision_maker_met=False,
            multi_thread_count=0, next_step_always_present=True,
        )
        assert _execution_score(inp) == 30.0

    def test_all_except_multi_thread_score_90(self):
        # champion(20)+exec(15)+poc(15)+budget(15)+dm(15)+next(10) = 90
        inp = make_input(multi_thread_count=0)
        assert _execution_score(inp) == 90.0

    def test_score_champion_exec_poc_budget_dm_next_no_multi_is_90(self):
        inp = make_input(multi_thread_count=1)
        # multi_thread=1 → no bonus (not >=2)
        assert _execution_score(inp) == 90.0

    def test_score_with_multi_thread_4(self):
        # multi_thread>=3 → 10
        inp = make_input(multi_thread_count=4)
        assert _execution_score(inp) == 100.0


# ===========================================================================
# 9. TestExecutionQualityThresholds
# ===========================================================================

class TestExecutionQualityThresholds:

    def test_score_80_is_excellent(self):
        assert _execution_quality(80.0) == ExecutionQuality.EXCELLENT

    def test_score_79_is_good(self):
        assert _execution_quality(79.0) == ExecutionQuality.GOOD

    def test_score_60_is_good(self):
        assert _execution_quality(60.0) == ExecutionQuality.GOOD

    def test_score_59_is_fair(self):
        assert _execution_quality(59.0) == ExecutionQuality.FAIR

    def test_score_40_is_fair(self):
        assert _execution_quality(40.0) == ExecutionQuality.FAIR

    def test_score_39_is_poor(self):
        assert _execution_quality(39.0) == ExecutionQuality.POOR

    def test_score_100_is_excellent(self):
        assert _execution_quality(100.0) == ExecutionQuality.EXCELLENT

    def test_score_0_is_poor(self):
        assert _execution_quality(0.0) == ExecutionQuality.POOR

    def test_score_1_is_poor(self):
        assert _execution_quality(1.0) == ExecutionQuality.POOR

    def test_score_99_is_excellent(self):
        assert _execution_quality(99.9) == ExecutionQuality.EXCELLENT

    def test_boundary_exactly_60(self):
        assert _execution_quality(60.0) == ExecutionQuality.GOOD

    def test_boundary_exactly_40(self):
        assert _execution_quality(40.0) == ExecutionQuality.FAIR


# ===========================================================================
# 10. TestCycleEfficiency
# ===========================================================================

class TestCycleEfficiency:

    def test_faster_than_expected_positive(self):
        # days=90, expected=120 → (1 - 90/120)*100 = 25.0
        inp = make_input(days_to_outcome=90, expected_cycle_days=120)
        assert _cycle_efficiency(inp) == 25.0

    def test_exactly_on_time_zero(self):
        inp = make_input(days_to_outcome=100, expected_cycle_days=100)
        assert _cycle_efficiency(inp) == 0.0

    def test_slower_than_expected_negative(self):
        # days=150, expected=100 → (1 - 150/100)*100 = -50.0
        inp = make_input(days_to_outcome=150, expected_cycle_days=100)
        assert _cycle_efficiency(inp) == -50.0

    def test_expected_zero_returns_zero(self):
        inp = make_input(expected_cycle_days=0)
        assert _cycle_efficiency(inp) == 0.0

    def test_expected_negative_returns_zero(self):
        inp = make_input(expected_cycle_days=-10)
        assert _cycle_efficiency(inp) == 0.0

    def test_returns_float(self):
        inp = make_input(days_to_outcome=90, expected_cycle_days=120)
        assert isinstance(_cycle_efficiency(inp), (int, float))

    def test_half_expected_days(self):
        # days=50, expected=100 → 50.0
        inp = make_input(days_to_outcome=50, expected_cycle_days=100)
        assert _cycle_efficiency(inp) == 50.0

    def test_rounding_one_decimal(self):
        # days=1, expected=3 → (1 - 1/3)*100 = 66.666... → 66.7
        inp = make_input(days_to_outcome=1, expected_cycle_days=3)
        result = _cycle_efficiency(inp)
        assert result == pytest.approx(66.7, abs=0.05)

    def test_double_expected_days(self):
        inp = make_input(days_to_outcome=200, expected_cycle_days=100)
        assert _cycle_efficiency(inp) == -100.0

    def test_very_fast_deal(self):
        # days=10, expected=100 → 90.0
        inp = make_input(days_to_outcome=10, expected_cycle_days=100)
        assert _cycle_efficiency(inp) == 90.0


# ===========================================================================
# 11. TestDiscountPressureThresholds
# ===========================================================================

class TestDiscountPressureThresholds:

    def test_zero_discount_is_none(self):
        inp = make_input(discount_given_pct=0.0)
        assert _discount_pressure(inp) == "none"

    def test_discount_10_is_low(self):
        inp = make_input(discount_given_pct=10.0)
        assert _discount_pressure(inp) == "low"

    def test_discount_5_is_low(self):
        inp = make_input(discount_given_pct=5.0)
        assert _discount_pressure(inp) == "low"

    def test_discount_11_is_medium(self):
        inp = make_input(discount_given_pct=11.0)
        assert _discount_pressure(inp) == "medium"

    def test_discount_25_is_medium(self):
        inp = make_input(discount_given_pct=25.0)
        assert _discount_pressure(inp) == "medium"

    def test_discount_26_is_high(self):
        inp = make_input(discount_given_pct=26.0)
        assert _discount_pressure(inp) == "high"

    def test_discount_100_is_high(self):
        inp = make_input(discount_given_pct=100.0)
        assert _discount_pressure(inp) == "high"

    def test_discount_50_is_high(self):
        inp = make_input(discount_given_pct=50.0)
        assert _discount_pressure(inp) == "high"

    def test_discount_1_is_low(self):
        inp = make_input(discount_given_pct=1.0)
        assert _discount_pressure(inp) == "low"

    def test_discount_0_point_1_is_low(self):
        # 0.1 != 0, so it falls to the <=10 branch
        inp = make_input(discount_given_pct=0.1)
        assert _discount_pressure(inp) == "low"


# ===========================================================================
# 12. TestWlActionWon
# ===========================================================================

class TestWlActionWon:

    def _won_inp(self):
        return make_input(outcome=DealOutcome.WON)

    def test_won_excellent_is_replicate(self):
        inp = self._won_inp()
        assert _wl_action(inp, ExecutionQuality.EXCELLENT) == WinLossAction.REPLICATE

    def test_won_good_is_replicate(self):
        inp = self._won_inp()
        assert _wl_action(inp, ExecutionQuality.GOOD) == WinLossAction.REPLICATE

    def test_won_fair_is_coach(self):
        inp = self._won_inp()
        assert _wl_action(inp, ExecutionQuality.FAIR) == WinLossAction.COACH

    def test_won_poor_is_coach(self):
        inp = self._won_inp()
        assert _wl_action(inp, ExecutionQuality.POOR) == WinLossAction.COACH

    def test_won_excellent_not_debrief(self):
        inp = self._won_inp()
        assert _wl_action(inp, ExecutionQuality.EXCELLENT) != WinLossAction.DEBRIEF

    def test_won_poor_not_replicate(self):
        inp = self._won_inp()
        assert _wl_action(inp, ExecutionQuality.POOR) != WinLossAction.REPLICATE

    def test_won_good_not_investigate(self):
        inp = self._won_inp()
        assert _wl_action(inp, ExecutionQuality.GOOD) != WinLossAction.INVESTIGATE


# ===========================================================================
# 13. TestWlActionLost
# ===========================================================================

class TestWlActionLost:

    def _lost_inp(self):
        return make_input(outcome=DealOutcome.LOST, loss_reason="price")

    def test_lost_excellent_is_debrief(self):
        inp = self._lost_inp()
        assert _wl_action(inp, ExecutionQuality.EXCELLENT) == WinLossAction.DEBRIEF

    def test_lost_good_is_debrief(self):
        inp = self._lost_inp()
        assert _wl_action(inp, ExecutionQuality.GOOD) == WinLossAction.DEBRIEF

    def test_lost_fair_is_coach(self):
        inp = self._lost_inp()
        assert _wl_action(inp, ExecutionQuality.FAIR) == WinLossAction.COACH

    def test_lost_poor_is_coach(self):
        inp = self._lost_inp()
        assert _wl_action(inp, ExecutionQuality.POOR) == WinLossAction.COACH

    def test_lost_excellent_not_coach(self):
        inp = self._lost_inp()
        assert _wl_action(inp, ExecutionQuality.EXCELLENT) != WinLossAction.COACH

    def test_lost_poor_not_debrief(self):
        inp = self._lost_inp()
        assert _wl_action(inp, ExecutionQuality.POOR) != WinLossAction.DEBRIEF

    def test_lost_good_not_replicate(self):
        inp = self._lost_inp()
        assert _wl_action(inp, ExecutionQuality.GOOD) != WinLossAction.REPLICATE


# ===========================================================================
# 14. TestWlActionNoDecision
# ===========================================================================

class TestWlActionNoDecision:

    def _nd_inp(self):
        return make_input(outcome=DealOutcome.NO_DECISION)

    def test_no_decision_excellent_is_investigate(self):
        assert _wl_action(self._nd_inp(), ExecutionQuality.EXCELLENT) == WinLossAction.INVESTIGATE

    def test_no_decision_good_is_investigate(self):
        assert _wl_action(self._nd_inp(), ExecutionQuality.GOOD) == WinLossAction.INVESTIGATE

    def test_no_decision_fair_is_investigate(self):
        assert _wl_action(self._nd_inp(), ExecutionQuality.FAIR) == WinLossAction.INVESTIGATE

    def test_no_decision_poor_is_investigate(self):
        assert _wl_action(self._nd_inp(), ExecutionQuality.POOR) == WinLossAction.INVESTIGATE

    def test_no_decision_not_coach(self):
        assert _wl_action(self._nd_inp(), ExecutionQuality.POOR) != WinLossAction.COACH

    def test_no_decision_not_replicate(self):
        assert _wl_action(self._nd_inp(), ExecutionQuality.EXCELLENT) != WinLossAction.REPLICATE

    def test_no_decision_not_debrief(self):
        assert _wl_action(self._nd_inp(), ExecutionQuality.GOOD) != WinLossAction.DEBRIEF


# ===========================================================================
# 15. TestBuildSignalsWonPatterns
# ===========================================================================

class TestBuildSignalsWonPatterns:

    def _signals(self, inp):
        score = _execution_score(inp)
        quality = _execution_quality(score)
        efficiency = _cycle_efficiency(inp)
        pressure = _discount_pressure(inp)
        return _build_signals(inp, quality, efficiency, pressure)

    def test_won_with_champion_has_pattern(self):
        inp = make_input(had_champion=True)
        win_patterns, _, _, _ = self._signals(inp)
        assert any("champion" in p.lower() for p in win_patterns)

    def test_won_with_exec_engaged_has_pattern(self):
        inp = make_input(executive_engaged=True)
        win_patterns, _, _, _ = self._signals(inp)
        assert any("xécut" in p.lower() or "executif" in p.lower() or "alignement" in p.lower() for p in win_patterns)

    def test_won_with_poc_has_pattern(self):
        inp = make_input(poc_done=True)
        win_patterns, _, _, _ = self._signals(inp)
        assert any("poc" in p.lower() for p in win_patterns)

    def test_won_zero_discount_pattern(self):
        inp = make_input(discount_given_pct=0.0)
        win_patterns, _, _, _ = self._signals(inp)
        assert any("remise" in p.lower() for p in win_patterns)

    def test_won_low_discount_pattern(self):
        inp = make_input(discount_given_pct=8.0)
        win_patterns, _, _, _ = self._signals(inp)
        assert any("faible pression" in p.lower() or "remise" in p.lower() for p in win_patterns)

    def test_won_many_meetings_pattern(self):
        inp = make_input(num_meetings=7)
        win_patterns, _, _, _ = self._signals(inp)
        assert any("7" in p for p in win_patterns)

    def test_lost_no_win_patterns(self):
        inp = make_input(outcome=DealOutcome.LOST, loss_reason="price")
        win_patterns, _, _, _ = self._signals(inp)
        assert win_patterns == []

    def test_no_decision_no_win_patterns(self):
        inp = make_input(outcome=DealOutcome.NO_DECISION)
        win_patterns, _, _, _ = self._signals(inp)
        assert win_patterns == []

    def test_won_references_pattern(self):
        inp = make_input(references_provided=True)
        win_patterns, _, _, _ = self._signals(inp)
        assert any("référence" in p.lower() for p in win_patterns)

    def test_won_case_study_pattern(self):
        inp = make_input(case_study_shared=True)
        win_patterns, _, _, _ = self._signals(inp)
        assert any("business case" in p.lower() or "case" in p.lower() for p in win_patterns)

    def test_won_multi_thread_pattern(self):
        inp = make_input(multi_thread_count=4)
        win_patterns, _, _, _ = self._signals(inp)
        assert any("multi" in p.lower() or "contact" in p.lower() for p in win_patterns)

    def test_won_fast_cycle_efficiency_pattern(self):
        # efficiency > 10 triggers the "cycle rapide" pattern
        inp = make_input(days_to_outcome=50, expected_cycle_days=100)
        win_patterns, _, _, _ = self._signals(inp)
        assert any("rapide" in p.lower() or "cycle" in p.lower() for p in win_patterns)


# ===========================================================================
# 16. TestBuildSignalsLossFactors
# ===========================================================================

class TestBuildSignalsLossFactors:

    def _signals(self, inp):
        score = _execution_score(inp)
        quality = _execution_quality(score)
        efficiency = _cycle_efficiency(inp)
        pressure = _discount_pressure(inp)
        return _build_signals(inp, quality, efficiency, pressure)

    def test_lost_price_reason(self):
        inp = make_input(outcome=DealOutcome.LOST, loss_reason="price",
                         had_champion=True, executive_engaged=True,
                         budget_confirmed=True, multi_thread_count=3)
        _, loss_factors, _, _ = self._signals(inp)
        assert any("prix" in f.lower() for f in loss_factors)

    def test_lost_competitor_reason(self):
        inp = make_input(outcome=DealOutcome.LOST, loss_reason="competitor",
                         competitor_lost_to="SAP",
                         had_champion=True, executive_engaged=True,
                         budget_confirmed=True, multi_thread_count=3)
        _, loss_factors, _, _ = self._signals(inp)
        assert any("concurrent" in f.lower() for f in loss_factors)

    def test_lost_competitor_includes_name(self):
        inp = make_input(outcome=DealOutcome.LOST, loss_reason="competitor",
                         competitor_lost_to="Oracle",
                         had_champion=True, executive_engaged=True,
                         budget_confirmed=True, multi_thread_count=3)
        _, loss_factors, _, _ = self._signals(inp)
        assert any("Oracle" in f for f in loss_factors)

    def test_lost_timing_reason(self):
        inp = make_input(outcome=DealOutcome.LOST, loss_reason="timing",
                         had_champion=True, executive_engaged=True,
                         budget_confirmed=True, multi_thread_count=3)
        _, loss_factors, _, _ = self._signals(inp)
        assert any("timing" in f.lower() for f in loss_factors)

    def test_lost_product_gap_reason(self):
        inp = make_input(outcome=DealOutcome.LOST, loss_reason="product_gap",
                         had_champion=True, executive_engaged=True,
                         budget_confirmed=True, multi_thread_count=3)
        _, loss_factors, _, _ = self._signals(inp)
        assert any("produit" in f.lower() or "gap" in f.lower() for f in loss_factors)

    def test_lost_relationship_reason(self):
        inp = make_input(outcome=DealOutcome.LOST, loss_reason="relationship",
                         had_champion=True, executive_engaged=True,
                         budget_confirmed=True, multi_thread_count=3)
        _, loss_factors, _, _ = self._signals(inp)
        assert any("relation" in f.lower() for f in loss_factors)

    def test_lost_no_champion_reason(self):
        inp = make_input(outcome=DealOutcome.LOST, loss_reason="no_champion",
                         had_champion=False, executive_engaged=True,
                         budget_confirmed=True, multi_thread_count=3)
        _, loss_factors, _, _ = self._signals(inp)
        assert any("champion" in f.lower() for f in loss_factors)

    def test_no_decision_includes_status_quo_factor(self):
        inp = make_input(outcome=DealOutcome.NO_DECISION,
                         had_champion=True, executive_engaged=True,
                         budget_confirmed=True, multi_thread_count=3)
        _, loss_factors, _, _ = self._signals(inp)
        assert any("pas de décision" in f.lower() or "status quo" in f.lower() for f in loss_factors)

    def test_lost_high_discount_factor(self):
        inp = make_input(outcome=DealOutcome.LOST, discount_given_pct=30.0,
                         had_champion=True, executive_engaged=True,
                         budget_confirmed=True, multi_thread_count=3)
        _, loss_factors, _, _ = self._signals(inp)
        assert any("30" in f or "remise" in f.lower() or "prix" in f.lower() for f in loss_factors)

    def test_lost_no_champion_factor_when_missing(self):
        inp = make_input(outcome=DealOutcome.LOST, had_champion=False,
                         multi_thread_count=3, budget_confirmed=True,
                         executive_engaged=True)
        _, loss_factors, _, _ = self._signals(inp)
        assert any("champion" in f.lower() for f in loss_factors)

    def test_won_no_loss_factors(self):
        inp = make_input(outcome=DealOutcome.WON)
        _, loss_factors, _, _ = self._signals(inp)
        assert loss_factors == []


# ===========================================================================
# 17. TestBuildSignalsProcessGaps
# ===========================================================================

class TestBuildSignalsProcessGaps:

    def _signals(self, inp):
        score = _execution_score(inp)
        quality = _execution_quality(score)
        efficiency = _cycle_efficiency(inp)
        pressure = _discount_pressure(inp)
        return _build_signals(inp, quality, efficiency, pressure)

    def test_no_champion_gap(self):
        inp = make_input(had_champion=False)
        _, _, process_gaps, _ = self._signals(inp)
        assert any("champion" in g.lower() for g in process_gaps)

    def test_no_budget_confirmed_gap(self):
        inp = make_input(budget_confirmed=False)
        _, _, process_gaps, _ = self._signals(inp)
        assert any("budget" in g.lower() for g in process_gaps)

    def test_no_decision_maker_gap(self):
        inp = make_input(decision_maker_met=False)
        _, _, process_gaps, _ = self._signals(inp)
        assert any("décideur" in g.lower() or "decision" in g.lower() for g in process_gaps)

    def test_single_thread_gap(self):
        inp = make_input(multi_thread_count=1)
        _, _, process_gaps, _ = self._signals(inp)
        assert any("single" in g.lower() or "threading" in g.lower() for g in process_gaps)

    def test_no_next_step_gap(self):
        inp = make_input(next_step_always_present=False)
        _, _, process_gaps, _ = self._signals(inp)
        assert any("étape" in g.lower() or "prochaine" in g.lower() for g in process_gaps)

    def test_no_poc_large_deal_gap(self):
        inp = make_input(poc_done=False, arr_eur=60_000.0)
        _, _, process_gaps, _ = self._signals(inp)
        assert any("poc" in g.lower() for g in process_gaps)

    def test_poc_gap_not_triggered_small_deal(self):
        inp = make_input(poc_done=False, arr_eur=30_000.0)
        _, _, process_gaps, _ = self._signals(inp)
        assert not any("poc" in g.lower() for g in process_gaps)

    def test_few_meetings_gap(self):
        inp = make_input(num_meetings=2)
        _, _, process_gaps, _ = self._signals(inp)
        assert any("2" in g for g in process_gaps)

    def test_perfect_execution_minimal_gaps(self, perfect_won_input):
        _, _, process_gaps, _ = self._signals(perfect_won_input)
        # With all flags True, multi_thread=3, next_step=True, poc=True, meetings=6
        # None of the gap conditions should fire
        assert process_gaps == []

    def test_process_gaps_is_list(self, zero_input):
        _, _, process_gaps, _ = self._signals(zero_input)
        assert isinstance(process_gaps, list)


# ===========================================================================
# 18. TestEngineAnalyze
# ===========================================================================

class TestEngineAnalyze:

    def test_returns_win_loss_result(self, engine, perfect_won_input):
        result = engine.analyze(perfect_won_input)
        assert isinstance(result, WinLossResult)

    def test_execution_score_correct(self, engine, perfect_won_input):
        result = engine.analyze(perfect_won_input)
        assert result.execution_score == 100.0

    def test_execution_quality_excellent(self, engine, perfect_won_input):
        result = engine.analyze(perfect_won_input)
        assert result.execution_quality == ExecutionQuality.EXCELLENT

    def test_wl_action_replicate_for_perfect_won(self, engine, perfect_won_input):
        result = engine.analyze(perfect_won_input)
        assert result.wl_action == WinLossAction.REPLICATE

    def test_discount_pressure_none(self, engine, perfect_won_input):
        result = engine.analyze(perfect_won_input)
        assert result.discount_pressure == "none"

    def test_cycle_efficiency_positive(self, engine, perfect_won_input):
        result = engine.analyze(perfect_won_input)
        assert result.cycle_efficiency_pct > 0

    def test_stored_in_engine(self, engine, perfect_won_input):
        result = engine.analyze(perfect_won_input)
        assert engine.get(perfect_won_input.deal_id) is result

    def test_deal_id_in_result(self, engine, perfect_won_input):
        result = engine.analyze(perfect_won_input)
        assert result.deal_id == perfect_won_input.deal_id

    def test_arr_eur_in_result(self, engine, perfect_won_input):
        result = engine.analyze(perfect_won_input)
        assert result.arr_eur == perfect_won_input.arr_eur

    def test_outcome_in_result(self, engine, perfect_won_input):
        result = engine.analyze(perfect_won_input)
        assert result.outcome == DealOutcome.WON

    def test_zero_input_score_is_zero(self, engine, zero_input):
        result = engine.analyze(zero_input)
        assert result.execution_score == 0.0

    def test_zero_input_quality_is_poor(self, engine, zero_input):
        result = engine.analyze(zero_input)
        assert result.execution_quality == ExecutionQuality.POOR

    def test_zero_lost_action_is_coach(self, engine, zero_input):
        result = engine.analyze(zero_input)
        assert result.wl_action == WinLossAction.COACH

    def test_get_unknown_returns_none(self, engine):
        assert engine.get("NONEXISTENT") is None

    def test_analyze_overwrites_same_id(self, engine):
        inp1 = make_input(deal_id="DX", arr_eur=10_000.0)
        inp2 = make_input(deal_id="DX", arr_eur=20_000.0)
        engine.analyze(inp1)
        r2 = engine.analyze(inp2)
        assert engine.get("DX").arr_eur == 20_000.0
        assert engine.get("DX") is r2

    def test_no_decision_analyze(self, engine):
        inp = make_input(outcome=DealOutcome.NO_DECISION, deal_id="ND1")
        result = engine.analyze(inp)
        assert result.wl_action == WinLossAction.INVESTIGATE


# ===========================================================================
# 19. TestEngineBatchAndFilters
# ===========================================================================

class TestEngineBatchAndFilters:

    def _batch_inputs(self):
        return [
            make_input(deal_id="W1", outcome=DealOutcome.WON,
                       had_champion=True, executive_engaged=True, poc_done=True,
                       budget_confirmed=True, decision_maker_met=True,
                       multi_thread_count=3, next_step_always_present=True),  # score=100
            make_input(deal_id="L1", outcome=DealOutcome.LOST, loss_reason="price",
                       had_champion=False, executive_engaged=False, poc_done=False,
                       budget_confirmed=False, decision_maker_met=False,
                       multi_thread_count=0, next_step_always_present=False),  # score=0
            make_input(deal_id="ND1", outcome=DealOutcome.NO_DECISION,
                       had_champion=True, executive_engaged=False, poc_done=True,
                       budget_confirmed=True, decision_maker_met=True,
                       multi_thread_count=2, next_step_always_present=False),  # score=20+15+15+15+5=70
        ]

    def test_analyze_batch_returns_list(self, engine):
        results = engine.analyze_batch(self._batch_inputs())
        assert isinstance(results, list)

    def test_analyze_batch_sorted_desc(self, engine):
        results = engine.analyze_batch(self._batch_inputs())
        scores = [r.execution_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_analyze_batch_length(self, engine):
        results = engine.analyze_batch(self._batch_inputs())
        assert len(results) == 3

    def test_analyze_batch_stores_all(self, engine):
        engine.analyze_batch(self._batch_inputs())
        assert engine.get("W1") is not None
        assert engine.get("L1") is not None
        assert engine.get("ND1") is not None

    def test_all_deals_sorted_desc(self, engine):
        engine.analyze_batch(self._batch_inputs())
        deals = engine.all_deals()
        scores = [d.execution_score for d in deals]
        assert scores == sorted(scores, reverse=True)

    def test_by_outcome_won(self, engine):
        engine.analyze_batch(self._batch_inputs())
        won = engine.by_outcome(DealOutcome.WON)
        assert all(r.outcome == DealOutcome.WON for r in won)
        assert len(won) == 1

    def test_by_outcome_lost(self, engine):
        engine.analyze_batch(self._batch_inputs())
        lost = engine.by_outcome(DealOutcome.LOST)
        assert all(r.outcome == DealOutcome.LOST for r in lost)
        assert len(lost) == 1

    def test_by_outcome_no_decision(self, engine):
        engine.analyze_batch(self._batch_inputs())
        nd = engine.by_outcome(DealOutcome.NO_DECISION)
        assert all(r.outcome == DealOutcome.NO_DECISION for r in nd)
        assert len(nd) == 1

    def test_won_shortcut(self, engine):
        engine.analyze_batch(self._batch_inputs())
        assert engine.won() == engine.by_outcome(DealOutcome.WON)

    def test_lost_shortcut(self, engine):
        engine.analyze_batch(self._batch_inputs())
        assert engine.lost() == engine.by_outcome(DealOutcome.LOST)

    def test_no_decision_shortcut(self, engine):
        engine.analyze_batch(self._batch_inputs())
        assert engine.no_decision() == engine.by_outcome(DealOutcome.NO_DECISION)

    def test_by_quality_excellent(self, engine):
        engine.analyze_batch(self._batch_inputs())
        excellent = engine.by_quality(ExecutionQuality.EXCELLENT)
        assert all(r.execution_quality == ExecutionQuality.EXCELLENT for r in excellent)

    def test_by_quality_poor(self, engine):
        engine.analyze_batch(self._batch_inputs())
        poor = engine.by_quality(ExecutionQuality.POOR)
        assert all(r.execution_quality == ExecutionQuality.POOR for r in poor)

    def test_needs_coaching_filter(self, engine):
        engine.analyze_batch(self._batch_inputs())
        coaching = engine.needs_coaching()
        assert all(r.wl_action == WinLossAction.COACH for r in coaching)

    def test_replicate_worthy_filter(self, engine):
        engine.analyze_batch(self._batch_inputs())
        replicate = engine.replicate_worthy()
        assert all(r.wl_action == WinLossAction.REPLICATE for r in replicate)

    def test_empty_engine_all_deals_empty(self, engine):
        assert engine.all_deals() == []

    def test_empty_engine_won_empty(self, engine):
        assert engine.won() == []

    def test_empty_engine_lost_empty(self, engine):
        assert engine.lost() == []


# ===========================================================================
# 20. TestEngineAggregates
# ===========================================================================

class TestEngineAggregates:

    def _load_three(self, engine):
        engine.analyze(make_input(deal_id="A1", outcome=DealOutcome.WON,
                                  arr_eur=50_000.0, discount_given_pct=0.0))
        engine.analyze(make_input(deal_id="A2", outcome=DealOutcome.WON,
                                  arr_eur=30_000.0, discount_given_pct=5.0))
        engine.analyze(make_input(deal_id="A3", outcome=DealOutcome.LOST,
                                  arr_eur=20_000.0, discount_given_pct=0.0,
                                  had_champion=False, executive_engaged=False,
                                  poc_done=False, budget_confirmed=False,
                                  decision_maker_met=False, multi_thread_count=0,
                                  next_step_always_present=False,
                                  loss_reason="price"))

    def test_win_rate_two_thirds(self, engine):
        self._load_three(engine)
        assert engine.win_rate() == pytest.approx(66.7, abs=0.05)

    def test_win_rate_empty(self, engine):
        assert engine.win_rate() == 0.0

    def test_win_rate_all_won(self, engine):
        engine.analyze(make_input(deal_id="X1", outcome=DealOutcome.WON))
        engine.analyze(make_input(deal_id="X2", outcome=DealOutcome.WON))
        assert engine.win_rate() == 100.0

    def test_win_rate_none_won(self, engine):
        engine.analyze(make_input(deal_id="X1", outcome=DealOutcome.LOST,
                                  loss_reason="price"))
        assert engine.win_rate() == 0.0

    def test_win_rate_rounded_one_decimal(self, engine):
        self._load_three(engine)
        rate = engine.win_rate()
        assert rate == round(rate, 1)

    def test_avg_execution_score_empty(self, engine):
        assert engine.avg_execution_score() == 0.0

    def test_avg_execution_score_returns_float(self, engine):
        self._load_three(engine)
        assert isinstance(engine.avg_execution_score(), (int, float))

    def test_avg_execution_score_rounded_one_decimal(self, engine):
        self._load_three(engine)
        avg = engine.avg_execution_score()
        assert avg == round(avg, 1)

    def test_total_won_arr_eur(self, engine):
        self._load_three(engine)
        assert engine.total_won_arr_eur() == pytest.approx(80_000.0)

    def test_total_lost_arr_eur(self, engine):
        self._load_three(engine)
        assert engine.total_lost_arr_eur() == pytest.approx(20_000.0)

    def test_total_won_arr_empty(self, engine):
        assert engine.total_won_arr_eur() == 0.0

    def test_total_lost_arr_empty(self, engine):
        assert engine.total_lost_arr_eur() == 0.0

    def test_reset_clears_all(self, engine):
        self._load_three(engine)
        engine.reset()
        assert engine.all_deals() == []
        assert engine.win_rate() == 0.0
        assert engine.total_won_arr_eur() == 0.0

    def test_summary_empty(self, engine):
        s = engine.summary()
        assert s["total"] == 0
        assert s["win_rate"] == 0.0

    def test_summary_total(self, engine):
        self._load_three(engine)
        s = engine.summary()
        assert s["total"] == 3

    def test_summary_win_rate(self, engine):
        self._load_three(engine)
        s = engine.summary()
        assert s["win_rate"] == engine.win_rate()

    def test_summary_outcome_counts(self, engine):
        self._load_three(engine)
        s = engine.summary()
        assert s["outcome_counts"].get("won") == 2
        assert s["outcome_counts"].get("lost") == 1

    def test_summary_quality_counts_present(self, engine):
        self._load_three(engine)
        s = engine.summary()
        assert "quality_counts" in s
        assert isinstance(s["quality_counts"], dict)

    def test_summary_action_counts_present(self, engine):
        self._load_three(engine)
        s = engine.summary()
        assert "action_counts" in s

    def test_summary_total_won_arr(self, engine):
        self._load_three(engine)
        s = engine.summary()
        assert s["total_won_arr_eur"] == pytest.approx(80_000.0)

    def test_summary_total_lost_arr(self, engine):
        self._load_three(engine)
        s = engine.summary()
        assert s["total_lost_arr_eur"] == pytest.approx(20_000.0)

    def test_summary_coaching_needed_count(self, engine):
        self._load_three(engine)
        s = engine.summary()
        assert s["coaching_needed_count"] == len(engine.needs_coaching())

    def test_summary_replicate_count(self, engine):
        self._load_three(engine)
        s = engine.summary()
        assert s["replicate_count"] == len(engine.replicate_worthy())

    def test_avg_execution_score_single_deal(self, engine):
        engine.analyze(make_input(deal_id="SOLO", multi_thread_count=3))
        assert engine.avg_execution_score() == 100.0


# ===========================================================================
# 21. TestEngineTopLossReasons
# ===========================================================================

class TestEngineTopLossReasons:

    def test_top_loss_reasons_empty_when_no_lost(self, engine):
        engine.analyze(make_input(deal_id="W1", outcome=DealOutcome.WON))
        assert engine.top_loss_reasons() == {}

    def test_top_loss_reasons_returns_dict(self, engine):
        engine.analyze(make_input(deal_id="L1", outcome=DealOutcome.LOST,
                                  loss_reason="price",
                                  had_champion=True, executive_engaged=True,
                                  budget_confirmed=True, multi_thread_count=3))
        result = engine.top_loss_reasons()
        assert isinstance(result, dict)

    def test_top_loss_reasons_counts_primary(self, engine):
        for i in range(3):
            engine.analyze(make_input(
                deal_id=f"LP{i}", outcome=DealOutcome.LOST, loss_reason="price",
                had_champion=True, executive_engaged=True,
                budget_confirmed=True, multi_thread_count=3,
            ))
        result = engine.top_loss_reasons()
        # The primary factor for all three should be the price-loss string
        total = sum(result.values())
        assert total == 3

    def test_top_loss_reasons_empty_engine(self, engine):
        assert engine.top_loss_reasons() == {}

    def test_top_loss_reasons_only_primary_factor(self, engine):
        """Each lost deal contributes at most one entry to the counts."""
        engine.analyze(make_input(deal_id="L1", outcome=DealOutcome.LOST,
                                  loss_reason="competitor", competitor_lost_to="SAP",
                                  had_champion=True, executive_engaged=True,
                                  budget_confirmed=True, multi_thread_count=3))
        result = engine.top_loss_reasons()
        total_counts = sum(result.values())
        assert total_counts == 1

    def test_top_loss_reasons_competitor_with_name(self, engine):
        engine.analyze(make_input(deal_id="LC1", outcome=DealOutcome.LOST,
                                  loss_reason="competitor", competitor_lost_to="Oracle",
                                  had_champion=True, executive_engaged=True,
                                  budget_confirmed=True, multi_thread_count=3))
        result = engine.top_loss_reasons()
        assert any("Oracle" in k for k in result.keys())

    def test_top_loss_reasons_multiple_reasons(self, engine):
        engine.analyze(make_input(deal_id="M1", outcome=DealOutcome.LOST,
                                  loss_reason="price",
                                  had_champion=True, executive_engaged=True,
                                  budget_confirmed=True, multi_thread_count=3))
        engine.analyze(make_input(deal_id="M2", outcome=DealOutcome.LOST,
                                  loss_reason="timing",
                                  had_champion=True, executive_engaged=True,
                                  budget_confirmed=True, multi_thread_count=3))
        result = engine.top_loss_reasons()
        assert len(result) == 2

    def test_top_loss_reasons_no_decision_excluded(self, engine):
        """top_loss_reasons should only count LOST deals, not NO_DECISION."""
        engine.analyze(make_input(deal_id="ND1", outcome=DealOutcome.NO_DECISION,
                                  loss_reason="timing"))
        result = engine.top_loss_reasons()
        assert result == {}


# ===========================================================================
# 22. TestEngineReplicateAndCoach
# ===========================================================================

class TestEngineReplicateAndCoach:

    def test_replicate_worthy_only_replicate_actions(self, engine):
        engine.analyze(make_input(deal_id="RW1", outcome=DealOutcome.WON,
                                  multi_thread_count=3))  # EXCELLENT → REPLICATE
        engine.analyze(make_input(deal_id="RW2", outcome=DealOutcome.LOST,
                                  loss_reason="price",
                                  had_champion=False, executive_engaged=False,
                                  poc_done=False, budget_confirmed=False,
                                  decision_maker_met=False, multi_thread_count=0,
                                  next_step_always_present=False))  # POOR → COACH
        worthy = engine.replicate_worthy()
        assert all(r.wl_action == WinLossAction.REPLICATE for r in worthy)

    def test_replicate_worthy_count(self, engine):
        engine.analyze(make_input(deal_id="R1", outcome=DealOutcome.WON))
        engine.analyze(make_input(deal_id="R2", outcome=DealOutcome.WON))
        engine.analyze(make_input(deal_id="R3", outcome=DealOutcome.LOST,
                                  loss_reason="price",
                                  had_champion=False, executive_engaged=False,
                                  poc_done=False, budget_confirmed=False,
                                  decision_maker_met=False, multi_thread_count=0,
                                  next_step_always_present=False))
        worthy = engine.replicate_worthy()
        assert len(worthy) == 2

    def test_needs_coaching_only_coach_actions(self, engine):
        engine.analyze(make_input(deal_id="C1", outcome=DealOutcome.WON,
                                  had_champion=False, executive_engaged=False,
                                  poc_done=False, budget_confirmed=False,
                                  decision_maker_met=False, multi_thread_count=0,
                                  next_step_always_present=False))  # POOR+WON → COACH
        engine.analyze(make_input(deal_id="C2", outcome=DealOutcome.WON,
                                  multi_thread_count=3))  # EXCELLENT → REPLICATE
        coaching = engine.needs_coaching()
        assert all(r.wl_action == WinLossAction.COACH for r in coaching)

    def test_needs_coaching_count(self, engine):
        # Two coach candidates
        for i in range(2):
            engine.analyze(make_input(
                deal_id=f"CC{i}", outcome=DealOutcome.LOST,
                loss_reason="price",
                had_champion=False, executive_engaged=False, poc_done=False,
                budget_confirmed=False, decision_maker_met=False,
                multi_thread_count=0, next_step_always_present=False,
            ))
        assert len(engine.needs_coaching()) == 2

    def test_replicate_worthy_empty_when_no_replicate(self, engine):
        engine.analyze(make_input(deal_id="NC1", outcome=DealOutcome.LOST,
                                  loss_reason="price",
                                  had_champion=False, executive_engaged=False,
                                  poc_done=False, budget_confirmed=False,
                                  decision_maker_met=False, multi_thread_count=0,
                                  next_step_always_present=False))
        assert engine.replicate_worthy() == []

    def test_needs_coaching_empty_when_no_coach(self, engine):
        engine.analyze(make_input(deal_id="NCC1", outcome=DealOutcome.WON))
        coaching = engine.needs_coaching()
        # Perfect execution WON → REPLICATE, not COACH
        assert all(r.wl_action == WinLossAction.COACH for r in coaching)

    def test_debrief_not_in_replicate(self, engine):
        # LOST + EXCELLENT → DEBRIEF, should not appear in replicate_worthy
        inp = make_input(deal_id="DB1", outcome=DealOutcome.LOST,
                         loss_reason="competitor", competitor_lost_to="SAP")
        engine.analyze(inp)
        worthy = engine.replicate_worthy()
        assert not any(r.deal_id == "DB1" for r in worthy)

    def test_investigate_not_in_coaching(self, engine):
        inp = make_input(deal_id="INV1", outcome=DealOutcome.NO_DECISION)
        engine.analyze(inp)
        coaching = engine.needs_coaching()
        assert not any(r.deal_id == "INV1" for r in coaching)

    def test_lost_excellent_in_coaching_when_poor(self, engine):
        # LOST + POOR → COACH
        inp = make_input(deal_id="LP1", outcome=DealOutcome.LOST,
                         loss_reason="price",
                         had_champion=False, executive_engaged=False,
                         poc_done=False, budget_confirmed=False,
                         decision_maker_met=False, multi_thread_count=0,
                         next_step_always_present=False)
        engine.analyze(inp)
        coaching = engine.needs_coaching()
        assert any(r.deal_id == "LP1" for r in coaching)

    def test_won_poor_in_coaching(self, engine):
        # WON + POOR → COACH
        inp = make_input(deal_id="WP1", outcome=DealOutcome.WON,
                         had_champion=False, executive_engaged=False,
                         poc_done=False, budget_confirmed=False,
                         decision_maker_met=False, multi_thread_count=0,
                         next_step_always_present=False)
        engine.analyze(inp)
        coaching = engine.needs_coaching()
        assert any(r.deal_id == "WP1" for r in coaching)
