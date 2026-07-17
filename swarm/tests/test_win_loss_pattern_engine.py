"""Comprehensive pytest test suite for swarm/intelligence/win_loss_pattern_engine.py.

Run from /home/user/TEST with:
    python3 -m pytest swarm/tests/test_win_loss_pattern_engine.py -x -q
"""

from __future__ import annotations

import dataclasses

import pytest

from swarm.intelligence.win_loss_pattern_engine import (
    DealOutcome,
    LossReason,
    RepBehaviorPattern,
    WinLossAction,
    WinLossPatternEngine,
    WinLossPatternInput,
    WinLossPatternResult,
)


# ---------------------------------------------------------------------------
# Shared factory helper
# ---------------------------------------------------------------------------

def make_input(
    deal_id: str = "D001",
    deal_name: str = "Test Deal",
    rep_id: str = "R001",
    deal_outcome: str = "closed_won",
    deal_size_usd: float = 100_000.0,
    sales_cycle_days: int = 90,
    expected_cycle_days: int = 120,
    discovery_calls_completed: int = 3,
    stakeholders_engaged: int = 6,
    exec_sponsor_engaged: int = 1,
    champion_active_at_close: int = 1,
    proposal_revision_count: int = 0,
    demo_count: int = 2,
    mutual_action_plan_used: int = 1,
    competitive_deal: int = 0,
    competitor_displacement: int = 0,
    price_discount_pct: float = 0.0,
    close_date_slips: int = 0,
    objections_raised: int = 3,
    objections_resolved_pct: float = 90.0,
    post_deal_survey_score: float = 85.0,
    rep_activity_score: float = 90.0,
) -> WinLossPatternInput:
    """Factory with sensible defaults for a perfect closed_won deal."""
    return WinLossPatternInput(
        deal_id=deal_id,
        deal_name=deal_name,
        rep_id=rep_id,
        deal_outcome=deal_outcome,
        deal_size_usd=deal_size_usd,
        sales_cycle_days=sales_cycle_days,
        expected_cycle_days=expected_cycle_days,
        discovery_calls_completed=discovery_calls_completed,
        stakeholders_engaged=stakeholders_engaged,
        exec_sponsor_engaged=exec_sponsor_engaged,
        champion_active_at_close=champion_active_at_close,
        proposal_revision_count=proposal_revision_count,
        demo_count=demo_count,
        mutual_action_plan_used=mutual_action_plan_used,
        competitive_deal=competitive_deal,
        competitor_displacement=competitor_displacement,
        price_discount_pct=price_discount_pct,
        close_date_slips=close_date_slips,
        objections_raised=objections_raised,
        objections_resolved_pct=objections_resolved_pct,
        post_deal_survey_score=post_deal_survey_score,
        rep_activity_score=rep_activity_score,
    )


def make_lost_input(**kwargs) -> WinLossPatternInput:
    """Factory for a typical closed_lost deal with weak execution."""
    defaults = dict(
        deal_outcome="closed_lost",
        discovery_calls_completed=1,
        stakeholders_engaged=1,
        exec_sponsor_engaged=0,
        champion_active_at_close=0,
        proposal_revision_count=4,
        demo_count=1,
        mutual_action_plan_used=0,
        competitive_deal=1,
        competitor_displacement=0,
        price_discount_pct=0.0,
        close_date_slips=0,
        objections_raised=5,
        objections_resolved_pct=20.0,
        post_deal_survey_score=-1.0,
        rep_activity_score=30.0,
    )
    defaults.update(kwargs)
    return make_input(**defaults)


@pytest.fixture
def engine() -> WinLossPatternEngine:
    return WinLossPatternEngine()


@pytest.fixture
def perfect_won() -> WinLossPatternInput:
    return make_input()


@pytest.fixture
def weak_lost() -> WinLossPatternInput:
    return make_lost_input()


# ===========================================================================
# 1. TestDealOutcomeEnum
# ===========================================================================

class TestDealOutcomeEnum:

    def test_closed_won_value(self):
        assert DealOutcome.CLOSED_WON.value == "closed_won"

    def test_closed_lost_value(self):
        assert DealOutcome.CLOSED_LOST.value == "closed_lost"

    def test_no_decision_value(self):
        assert DealOutcome.NO_DECISION.value == "no_decision"

    def test_churned_value(self):
        assert DealOutcome.CHURNED.value == "churned"

    def test_member_count(self):
        assert len(DealOutcome) == 4

    def test_is_string_enum(self):
        assert isinstance(DealOutcome.CLOSED_WON, str)

    def test_equality_with_string(self):
        assert DealOutcome.CLOSED_WON == "closed_won"

    def test_construct_from_value(self):
        assert DealOutcome("closed_lost") == DealOutcome.CLOSED_LOST

    def test_invalid_value_raises(self):
        with pytest.raises(ValueError):
            DealOutcome("won")

    def test_no_decision_construct(self):
        assert DealOutcome("no_decision") == DealOutcome.NO_DECISION

    def test_churned_construct(self):
        assert DealOutcome("churned") == DealOutcome.CHURNED


# ===========================================================================
# 2. TestLossReasonEnum
# ===========================================================================

class TestLossReasonEnum:

    def test_price_value(self):
        assert LossReason.PRICE.value == "price"

    def test_timing_value(self):
        assert LossReason.TIMING.value == "timing"

    def test_competitor_value(self):
        assert LossReason.COMPETITOR.value == "competitor"

    def test_champion_loss_value(self):
        assert LossReason.CHAMPION_LOSS.value == "champion_loss"

    def test_poor_process_value(self):
        assert LossReason.POOR_PROCESS.value == "poor_process"

    def test_no_loss_value(self):
        assert LossReason.NO_LOSS.value == "no_loss"

    def test_member_count(self):
        assert len(LossReason) == 6

    def test_is_string_enum(self):
        assert isinstance(LossReason.NO_LOSS, str)

    def test_equality_with_string(self):
        assert LossReason.COMPETITOR == "competitor"

    def test_construct_from_value(self):
        assert LossReason("price") == LossReason.PRICE

    def test_invalid_value_raises(self):
        with pytest.raises(ValueError):
            LossReason("unknown")


# ===========================================================================
# 3. TestRepBehaviorPatternEnum
# ===========================================================================

class TestRepBehaviorPatternEnum:

    def test_exemplary_value(self):
        assert RepBehaviorPattern.EXEMPLARY.value == "exemplary"

    def test_solid_value(self):
        assert RepBehaviorPattern.SOLID.value == "solid"

    def test_improvable_value(self):
        assert RepBehaviorPattern.IMPROVABLE.value == "improvable"

    def test_high_risk_value(self):
        assert RepBehaviorPattern.HIGH_RISK.value == "high_risk"

    def test_member_count(self):
        assert len(RepBehaviorPattern) == 4

    def test_is_string_enum(self):
        assert isinstance(RepBehaviorPattern.EXEMPLARY, str)

    def test_equality_with_string(self):
        assert RepBehaviorPattern.HIGH_RISK == "high_risk"

    def test_construct_from_value(self):
        assert RepBehaviorPattern("solid") == RepBehaviorPattern.SOLID

    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            RepBehaviorPattern("bad")


# ===========================================================================
# 4. TestWinLossActionEnum
# ===========================================================================

class TestWinLossActionEnum:

    def test_replicate_value(self):
        assert WinLossAction.REPLICATE.value == "replicate"

    def test_share_as_best_practice_value(self):
        assert WinLossAction.SHARE_AS_BEST_PRACTICE.value == "share_as_best_practice"

    def test_coach_and_improve_value(self):
        assert WinLossAction.COACH_AND_IMPROVE.value == "coach_and_improve"

    def test_urgent_intervention_value(self):
        assert WinLossAction.URGENT_INTERVENTION.value == "urgent_intervention"

    def test_member_count(self):
        assert len(WinLossAction) == 4

    def test_is_string_enum(self):
        assert isinstance(WinLossAction.REPLICATE, str)

    def test_equality_with_string(self):
        assert WinLossAction.URGENT_INTERVENTION == "urgent_intervention"

    def test_construct_from_value(self):
        assert WinLossAction("coach_and_improve") == WinLossAction.COACH_AND_IMPROVE

    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            WinLossAction("noop")


# ===========================================================================
# 5. TestWinLossPatternInputDataclass
# ===========================================================================

class TestWinLossPatternInputDataclass:

    def test_instantiation(self, perfect_won):
        assert perfect_won.deal_id == "D001"

    def test_exactly_22_fields(self, perfect_won):
        fields = dataclasses.fields(perfect_won)
        assert len(fields) == 22

    def test_all_field_names(self, perfect_won):
        expected = {
            "deal_id", "deal_name", "rep_id", "deal_outcome", "deal_size_usd",
            "sales_cycle_days", "expected_cycle_days", "discovery_calls_completed",
            "stakeholders_engaged", "exec_sponsor_engaged", "champion_active_at_close",
            "proposal_revision_count", "demo_count", "mutual_action_plan_used",
            "competitive_deal", "competitor_displacement", "price_discount_pct",
            "close_date_slips", "objections_raised", "objections_resolved_pct",
            "post_deal_survey_score", "rep_activity_score",
        }
        actual = {f.name for f in dataclasses.fields(perfect_won)}
        assert actual == expected

    def test_deal_outcome_field(self, perfect_won):
        assert perfect_won.deal_outcome == "closed_won"

    def test_deal_size_usd_field(self, perfect_won):
        assert perfect_won.deal_size_usd == 100_000.0

    def test_exec_sponsor_flag(self, perfect_won):
        assert perfect_won.exec_sponsor_engaged == 1

    def test_champion_active_flag(self, perfect_won):
        assert perfect_won.champion_active_at_close == 1

    def test_mutual_action_plan_flag(self, perfect_won):
        assert perfect_won.mutual_action_plan_used == 1

    def test_price_discount_pct(self, perfect_won):
        assert perfect_won.price_discount_pct == 0.0

    def test_objections_resolved_pct(self, perfect_won):
        assert perfect_won.objections_resolved_pct == 90.0

    def test_rep_activity_score(self, perfect_won):
        assert perfect_won.rep_activity_score == 90.0

    def test_post_deal_survey_score(self, perfect_won):
        assert perfect_won.post_deal_survey_score == 85.0

    def test_lost_input_outcome(self, weak_lost):
        assert weak_lost.deal_outcome == "closed_lost"


# ===========================================================================
# 6. TestWinLossPatternResultToDict
# ===========================================================================

class TestWinLossPatternResultToDict:

    def test_to_dict_returns_dict(self, engine, perfect_won):
        d = engine.analyze(perfect_won).to_dict()
        assert isinstance(d, dict)

    def test_to_dict_exactly_15_keys(self, engine, perfect_won):
        d = engine.analyze(perfect_won).to_dict()
        assert len(d) == 15

    def test_to_dict_key_set(self, engine, perfect_won):
        d = engine.analyze(perfect_won).to_dict()
        expected = {
            "deal_id", "deal_name", "deal_outcome", "loss_reason",
            "rep_behavior_pattern", "win_loss_action",
            "process_quality_score", "execution_score", "relationship_score",
            "deal_health_score", "win_loss_composite", "win_probability_index",
            "replication_value", "is_best_practice", "needs_coaching",
        }
        assert set(d.keys()) == expected

    def test_deal_outcome_is_string(self, engine, perfect_won):
        d = engine.analyze(perfect_won).to_dict()
        assert isinstance(d["deal_outcome"], str)
        assert d["deal_outcome"] == "closed_won"

    def test_loss_reason_is_string(self, engine, perfect_won):
        d = engine.analyze(perfect_won).to_dict()
        assert isinstance(d["loss_reason"], str)

    def test_rep_behavior_pattern_is_string(self, engine, perfect_won):
        d = engine.analyze(perfect_won).to_dict()
        assert isinstance(d["rep_behavior_pattern"], str)

    def test_win_loss_action_is_string(self, engine, perfect_won):
        d = engine.analyze(perfect_won).to_dict()
        assert isinstance(d["win_loss_action"], str)

    def test_is_best_practice_is_bool(self, engine, perfect_won):
        d = engine.analyze(perfect_won).to_dict()
        assert isinstance(d["is_best_practice"], bool)

    def test_needs_coaching_is_bool(self, engine, perfect_won):
        d = engine.analyze(perfect_won).to_dict()
        assert isinstance(d["needs_coaching"], bool)

    def test_scores_are_numeric(self, engine, perfect_won):
        d = engine.analyze(perfect_won).to_dict()
        for key in ("process_quality_score", "execution_score", "relationship_score",
                    "deal_health_score", "win_loss_composite", "win_probability_index",
                    "replication_value"):
            assert isinstance(d[key], (int, float)), f"{key} should be numeric"

    def test_deal_id_preserved(self, engine, perfect_won):
        d = engine.analyze(perfect_won).to_dict()
        assert d["deal_id"] == "D001"

    def test_deal_name_preserved(self, engine, perfect_won):
        d = engine.analyze(perfect_won).to_dict()
        assert d["deal_name"] == "Test Deal"

    def test_lost_outcome_in_dict(self, engine, weak_lost):
        d = engine.analyze(weak_lost).to_dict()
        assert d["deal_outcome"] == "closed_lost"


# ===========================================================================
# 7. TestSummaryKeys
# ===========================================================================

class TestSummaryKeys:

    def test_empty_summary_returns_13_keys(self, engine):
        s = engine.summary()
        assert len(s) == 13

    def test_summary_key_set_empty(self, engine):
        s = engine.summary()
        expected = {
            "total", "outcome_counts", "loss_reason_counts", "behavior_counts",
            "action_counts", "avg_win_loss_composite", "win_rate",
            "best_practice_count", "coaching_count",
            "avg_process_quality_score", "avg_execution_score",
            "avg_relationship_score", "avg_replication_value",
        }
        assert set(s.keys()) == expected

    def test_summary_returns_13_keys_with_data(self, engine, perfect_won):
        engine.analyze(perfect_won)
        s = engine.summary()
        assert len(s) == 13

    def test_summary_key_set_with_data(self, engine, perfect_won):
        engine.analyze(perfect_won)
        s = engine.summary()
        expected = {
            "total", "outcome_counts", "loss_reason_counts", "behavior_counts",
            "action_counts", "avg_win_loss_composite", "win_rate",
            "best_practice_count", "coaching_count",
            "avg_process_quality_score", "avg_execution_score",
            "avg_relationship_score", "avg_replication_value",
        }
        assert set(s.keys()) == expected

    def test_empty_summary_total_zero(self, engine):
        assert engine.summary()["total"] == 0

    def test_empty_summary_win_rate_zero(self, engine):
        assert engine.summary()["win_rate"] == 0.0

    def test_empty_summary_composite_zero(self, engine):
        assert engine.summary()["avg_win_loss_composite"] == 0.0

    def test_empty_summary_counts_empty_dicts(self, engine):
        s = engine.summary()
        assert s["outcome_counts"] == {}
        assert s["loss_reason_counts"] == {}
        assert s["behavior_counts"] == {}
        assert s["action_counts"] == {}

    def test_empty_summary_best_practice_zero(self, engine):
        assert engine.summary()["best_practice_count"] == 0

    def test_empty_summary_coaching_zero(self, engine):
        assert engine.summary()["coaching_count"] == 0

    def test_summary_total_increases(self, engine, perfect_won):
        engine.analyze(perfect_won)
        assert engine.summary()["total"] == 1

    def test_summary_total_multiple(self, engine):
        engine.analyze(make_input(deal_id="A"))
        engine.analyze(make_input(deal_id="B"))
        engine.analyze(make_input(deal_id="C"))
        assert engine.summary()["total"] == 3


# ===========================================================================
# 8. TestProcessQualityScore
# ===========================================================================

class TestProcessQualityScore:

    def _score(self, engine, **kwargs) -> float:
        inp = make_input(**kwargs)
        return engine._process_quality_score(inp)

    def test_max_possible_score(self, engine):
        # 3 discovery(25) + MAP(20) + orr>=80(30) + 0 slips(15) + 0 revisions = 90
        score = self._score(
            engine,
            discovery_calls_completed=3,
            mutual_action_plan_used=1,
            objections_resolved_pct=90.0,
            close_date_slips=0,
            proposal_revision_count=0,
        )
        assert score == 90.0

    def test_discovery_3_gets_25(self, engine):
        base = self._score(
            engine,
            discovery_calls_completed=3,
            mutual_action_plan_used=0,
            objections_resolved_pct=0.0,
            close_date_slips=1,
            proposal_revision_count=0,
        )
        # 25 (discovery) + 0 (MAP) + 0 (orr) + 7 (1 slip) = 32
        assert base == 32.0

    def test_discovery_2_gets_16(self, engine):
        score = self._score(
            engine,
            discovery_calls_completed=2,
            mutual_action_plan_used=0,
            objections_resolved_pct=0.0,
            close_date_slips=1,
            proposal_revision_count=0,
        )
        # 16 + 0 + 0 + 7 = 23
        assert score == 23.0

    def test_discovery_1_gets_8(self, engine):
        score = self._score(
            engine,
            discovery_calls_completed=1,
            mutual_action_plan_used=0,
            objections_resolved_pct=0.0,
            close_date_slips=1,
            proposal_revision_count=0,
        )
        # 8 + 0 + 0 + 7 = 15
        assert score == 15.0

    def test_discovery_0_gets_0(self, engine):
        score = self._score(
            engine,
            discovery_calls_completed=0,
            mutual_action_plan_used=0,
            objections_resolved_pct=0.0,
            close_date_slips=1,
            proposal_revision_count=0,
        )
        # 0 + 0 + 0 + 7 = 7
        assert score == 7.0

    def test_map_adds_20(self, engine):
        with_map = self._score(
            engine,
            discovery_calls_completed=0,
            mutual_action_plan_used=1,
            objections_resolved_pct=0.0,
            close_date_slips=1,
            proposal_revision_count=0,
        )
        # 0 + 20 + 0 + 7 = 27
        assert with_map == 27.0

    def test_orr_80_gets_30(self, engine):
        score = self._score(
            engine,
            discovery_calls_completed=0,
            mutual_action_plan_used=0,
            objections_resolved_pct=80.0,
            close_date_slips=1,
            proposal_revision_count=0,
        )
        # 0 + 0 + 30 + 7 = 37
        assert score == 37.0

    def test_orr_60_to_79_gets_20(self, engine):
        score = self._score(
            engine,
            discovery_calls_completed=0,
            mutual_action_plan_used=0,
            objections_resolved_pct=60.0,
            close_date_slips=1,
            proposal_revision_count=0,
        )
        # 0 + 0 + 20 + 7 = 27
        assert score == 27.0

    def test_orr_40_to_59_gets_10(self, engine):
        score = self._score(
            engine,
            discovery_calls_completed=0,
            mutual_action_plan_used=0,
            objections_resolved_pct=40.0,
            close_date_slips=1,
            proposal_revision_count=0,
        )
        # 0 + 0 + 10 + 7 = 17
        assert score == 17.0

    def test_orr_below_40_gets_0(self, engine):
        score = self._score(
            engine,
            discovery_calls_completed=0,
            mutual_action_plan_used=0,
            objections_resolved_pct=39.0,
            close_date_slips=1,
            proposal_revision_count=0,
        )
        # 0 + 0 + 0 + 7 = 7
        assert score == 7.0

    def test_0_slips_adds_15(self, engine):
        score = self._score(
            engine,
            discovery_calls_completed=0,
            mutual_action_plan_used=0,
            objections_resolved_pct=0.0,
            close_date_slips=0,
            proposal_revision_count=0,
        )
        # 0 + 0 + 0 + 15 = 15
        assert score == 15.0

    def test_1_slip_adds_7(self, engine):
        score = self._score(
            engine,
            discovery_calls_completed=0,
            mutual_action_plan_used=0,
            objections_resolved_pct=0.0,
            close_date_slips=1,
            proposal_revision_count=0,
        )
        assert score == 7.0

    def test_2_slips_adds_0(self, engine):
        score = self._score(
            engine,
            discovery_calls_completed=0,
            mutual_action_plan_used=0,
            objections_resolved_pct=0.0,
            close_date_slips=2,
            proposal_revision_count=0,
        )
        assert score == 0.0

    def test_3_plus_slips_penalty_10(self, engine):
        score = self._score(
            engine,
            discovery_calls_completed=3,
            mutual_action_plan_used=0,
            objections_resolved_pct=0.0,
            close_date_slips=3,
            proposal_revision_count=0,
        )
        # 25 + 0 + 0 - 10 = 15
        assert score == 15.0

    def test_4_plus_revisions_penalty_10(self, engine):
        score = self._score(
            engine,
            discovery_calls_completed=3,
            mutual_action_plan_used=0,
            objections_resolved_pct=0.0,
            close_date_slips=0,
            proposal_revision_count=4,
        )
        # 25 + 0 + 0 + 15 - 10 = 30
        assert score == 30.0

    def test_2_or_3_revisions_penalty_5(self, engine):
        score = self._score(
            engine,
            discovery_calls_completed=3,
            mutual_action_plan_used=0,
            objections_resolved_pct=0.0,
            close_date_slips=0,
            proposal_revision_count=2,
        )
        # 25 + 0 + 0 + 15 - 5 = 35
        assert score == 35.0

    def test_score_clamped_at_zero(self, engine):
        # Penalty scenario: 3+ slips and 4+ revisions — could go negative
        score = self._score(
            engine,
            discovery_calls_completed=0,
            mutual_action_plan_used=0,
            objections_resolved_pct=0.0,
            close_date_slips=3,
            proposal_revision_count=4,
        )
        assert score >= 0.0

    def test_score_clamped_at_100(self, engine):
        score = self._score(
            engine,
            discovery_calls_completed=10,
            mutual_action_plan_used=1,
            objections_resolved_pct=100.0,
            close_date_slips=0,
            proposal_revision_count=0,
        )
        assert score <= 100.0

    def test_returns_float(self, engine, perfect_won):
        score = engine._process_quality_score(perfect_won)
        assert isinstance(score, float)


# ===========================================================================
# 9. TestExecutionScore
# ===========================================================================

class TestExecutionScore:

    def _score(self, engine, **kwargs) -> float:
        inp = make_input(**kwargs)
        return engine._execution_score(inp)

    def test_fast_cycle_ratio_lte_0_8_gets_35(self, engine):
        # 90/120 = 0.75 <= 0.8
        score = self._score(
            engine,
            sales_cycle_days=90,
            expected_cycle_days=120,
            rep_activity_score=0.0,
            demo_count=0,
            competitor_displacement=0,
        )
        assert score == 35.0

    def test_cycle_ratio_lte_1_0_gets_25(self, engine):
        score = self._score(
            engine,
            sales_cycle_days=100,
            expected_cycle_days=100,
            rep_activity_score=0.0,
            demo_count=0,
            competitor_displacement=0,
        )
        assert score == 25.0

    def test_cycle_ratio_lte_1_3_gets_12(self, engine):
        score = self._score(
            engine,
            sales_cycle_days=120,
            expected_cycle_days=100,
            rep_activity_score=0.0,
            demo_count=0,
            competitor_displacement=0,
        )
        assert score == 12.0

    def test_cycle_ratio_lte_1_7_gets_5(self, engine):
        score = self._score(
            engine,
            sales_cycle_days=150,
            expected_cycle_days=100,
            rep_activity_score=0.0,
            demo_count=0,
            competitor_displacement=0,
        )
        assert score == 5.0

    def test_cycle_ratio_over_1_7_gets_0(self, engine):
        score = self._score(
            engine,
            sales_cycle_days=200,
            expected_cycle_days=100,
            rep_activity_score=0.0,
            demo_count=0,
            competitor_displacement=0,
        )
        assert score == 0.0

    def test_expected_cycle_0_skips_cycle_component(self, engine):
        score = self._score(
            engine,
            sales_cycle_days=100,
            expected_cycle_days=0,
            rep_activity_score=0.0,
            demo_count=0,
            competitor_displacement=0,
        )
        assert score == 0.0

    def test_activity_score_gte_80_gets_35(self, engine):
        score = self._score(
            engine,
            sales_cycle_days=100,
            expected_cycle_days=0,
            rep_activity_score=80.0,
            demo_count=0,
            competitor_displacement=0,
        )
        assert score == 35.0

    def test_activity_score_60_to_79_gets_22(self, engine):
        score = self._score(
            engine,
            sales_cycle_days=100,
            expected_cycle_days=0,
            rep_activity_score=60.0,
            demo_count=0,
            competitor_displacement=0,
        )
        assert score == 22.0

    def test_activity_score_40_to_59_gets_10(self, engine):
        score = self._score(
            engine,
            sales_cycle_days=100,
            expected_cycle_days=0,
            rep_activity_score=40.0,
            demo_count=0,
            competitor_displacement=0,
        )
        assert score == 10.0

    def test_activity_score_below_40_gets_0(self, engine):
        score = self._score(
            engine,
            sales_cycle_days=100,
            expected_cycle_days=0,
            rep_activity_score=39.0,
            demo_count=0,
            competitor_displacement=0,
        )
        assert score == 0.0

    def test_demo_count_2_or_3_gets_20(self, engine):
        score = self._score(
            engine,
            sales_cycle_days=100,
            expected_cycle_days=0,
            rep_activity_score=0.0,
            demo_count=2,
            competitor_displacement=0,
        )
        assert score == 20.0

    def test_demo_count_3_gets_20(self, engine):
        score = self._score(
            engine,
            sales_cycle_days=100,
            expected_cycle_days=0,
            rep_activity_score=0.0,
            demo_count=3,
            competitor_displacement=0,
        )
        assert score == 20.0

    def test_demo_count_1_gets_10(self, engine):
        score = self._score(
            engine,
            sales_cycle_days=100,
            expected_cycle_days=0,
            rep_activity_score=0.0,
            demo_count=1,
            competitor_displacement=0,
        )
        assert score == 10.0

    def test_demo_count_4_gets_10(self, engine):
        score = self._score(
            engine,
            sales_cycle_days=100,
            expected_cycle_days=0,
            rep_activity_score=0.0,
            demo_count=4,
            competitor_displacement=0,
        )
        assert score == 10.0

    def test_demo_count_0_gets_0(self, engine):
        score = self._score(
            engine,
            sales_cycle_days=100,
            expected_cycle_days=0,
            rep_activity_score=0.0,
            demo_count=0,
            competitor_displacement=0,
        )
        assert score == 0.0

    def test_competitor_displacement_bonus_10(self, engine):
        without = self._score(
            engine,
            sales_cycle_days=100,
            expected_cycle_days=0,
            rep_activity_score=0.0,
            demo_count=0,
            competitor_displacement=0,
        )
        with_disp = self._score(
            engine,
            sales_cycle_days=100,
            expected_cycle_days=0,
            rep_activity_score=0.0,
            demo_count=0,
            competitor_displacement=1,
        )
        assert with_disp == without + 10.0

    def test_score_clamped_at_100(self, engine):
        score = self._score(
            engine,
            sales_cycle_days=50,
            expected_cycle_days=100,
            rep_activity_score=100.0,
            demo_count=2,
            competitor_displacement=1,
        )
        assert score <= 100.0

    def test_score_returns_float(self, engine, perfect_won):
        assert isinstance(engine._execution_score(perfect_won), float)


# ===========================================================================
# 10. TestRelationshipScore
# ===========================================================================

class TestRelationshipScore:

    def _score(self, engine, **kwargs) -> float:
        inp = make_input(**kwargs)
        return engine._relationship_score(inp)

    def test_stakeholders_gte_6_gets_30(self, engine):
        score = self._score(
            engine,
            stakeholders_engaged=6,
            exec_sponsor_engaged=0,
            champion_active_at_close=0,
            post_deal_survey_score=-1.0,
        )
        assert score == 30.0

    def test_stakeholders_4_to_5_gets_20(self, engine):
        score = self._score(
            engine,
            stakeholders_engaged=4,
            exec_sponsor_engaged=0,
            champion_active_at_close=0,
            post_deal_survey_score=-1.0,
        )
        assert score == 20.0

    def test_stakeholders_2_to_3_gets_10(self, engine):
        score = self._score(
            engine,
            stakeholders_engaged=2,
            exec_sponsor_engaged=0,
            champion_active_at_close=0,
            post_deal_survey_score=-1.0,
        )
        assert score == 10.0

    def test_stakeholders_below_2_gets_0(self, engine):
        score = self._score(
            engine,
            stakeholders_engaged=1,
            exec_sponsor_engaged=0,
            champion_active_at_close=0,
            post_deal_survey_score=-1.0,
        )
        assert score == 0.0

    def test_exec_sponsor_adds_25(self, engine):
        with_exec = self._score(
            engine,
            stakeholders_engaged=1,
            exec_sponsor_engaged=1,
            champion_active_at_close=0,
            post_deal_survey_score=-1.0,
        )
        assert with_exec == 25.0

    def test_champion_active_adds_30(self, engine):
        score = self._score(
            engine,
            stakeholders_engaged=1,
            exec_sponsor_engaged=0,
            champion_active_at_close=1,
            post_deal_survey_score=-1.0,
        )
        assert score == 30.0

    def test_survey_gte_80_adds_15(self, engine):
        score = self._score(
            engine,
            stakeholders_engaged=1,
            exec_sponsor_engaged=0,
            champion_active_at_close=0,
            post_deal_survey_score=80.0,
        )
        assert score == 15.0

    def test_survey_60_to_79_adds_8(self, engine):
        score = self._score(
            engine,
            stakeholders_engaged=1,
            exec_sponsor_engaged=0,
            champion_active_at_close=0,
            post_deal_survey_score=60.0,
        )
        assert score == 8.0

    def test_survey_below_60_adds_0(self, engine):
        score = self._score(
            engine,
            stakeholders_engaged=1,
            exec_sponsor_engaged=0,
            champion_active_at_close=0,
            post_deal_survey_score=59.0,
        )
        assert score == 0.0

    def test_survey_negative_adds_0(self, engine):
        score = self._score(
            engine,
            stakeholders_engaged=1,
            exec_sponsor_engaged=0,
            champion_active_at_close=0,
            post_deal_survey_score=-1.0,
        )
        assert score == 0.0

    def test_score_clamped_at_100(self, engine):
        score = self._score(
            engine,
            stakeholders_engaged=6,
            exec_sponsor_engaged=1,
            champion_active_at_close=1,
            post_deal_survey_score=90.0,
        )
        assert score <= 100.0

    def test_returns_float(self, engine, perfect_won):
        assert isinstance(engine._relationship_score(perfect_won), float)


# ===========================================================================
# 11. TestDealHealthScore
# ===========================================================================

class TestDealHealthScore:

    def _score(self, engine, **kwargs) -> float:
        inp = make_input(**kwargs)
        return engine._deal_health_score(inp)

    def test_zero_discount_adds_30(self, engine):
        score = self._score(
            engine,
            price_discount_pct=0.0,
            deal_size_usd=0.0,
            deal_outcome="closed_lost",
        )
        assert score == 30.0

    def test_discount_lte_5_adds_22(self, engine):
        score = self._score(
            engine,
            price_discount_pct=5.0,
            deal_size_usd=0.0,
            deal_outcome="closed_lost",
        )
        assert score == 22.0

    def test_discount_lte_15_adds_12(self, engine):
        score = self._score(
            engine,
            price_discount_pct=15.0,
            deal_size_usd=0.0,
            deal_outcome="closed_lost",
        )
        assert score == 12.0

    def test_discount_lte_25_adds_4(self, engine):
        score = self._score(
            engine,
            price_discount_pct=25.0,
            deal_size_usd=0.0,
            deal_outcome="closed_lost",
        )
        assert score == 4.0

    def test_discount_above_25_adds_0(self, engine):
        score = self._score(
            engine,
            price_discount_pct=30.0,
            deal_size_usd=0.0,
            deal_outcome="closed_lost",
        )
        assert score == 0.0

    def test_deal_size_gte_200k_adds_25(self, engine):
        score = self._score(
            engine,
            price_discount_pct=0.0,
            deal_size_usd=200_000.0,
            deal_outcome="closed_lost",
        )
        # 30 + 25 = 55
        assert score == 55.0

    def test_deal_size_75k_to_199k_adds_15(self, engine):
        score = self._score(
            engine,
            price_discount_pct=0.0,
            deal_size_usd=75_000.0,
            deal_outcome="closed_lost",
        )
        assert score == 45.0

    def test_deal_size_25k_to_74k_adds_8(self, engine):
        score = self._score(
            engine,
            price_discount_pct=0.0,
            deal_size_usd=25_000.0,
            deal_outcome="closed_lost",
        )
        assert score == 38.0

    def test_deal_size_below_25k_adds_0(self, engine):
        score = self._score(
            engine,
            price_discount_pct=0.0,
            deal_size_usd=10_000.0,
            deal_outcome="closed_lost",
        )
        assert score == 30.0

    def test_closed_won_adds_35(self, engine):
        score = self._score(
            engine,
            price_discount_pct=0.0,
            deal_size_usd=0.0,
            deal_outcome="closed_won",
        )
        # 30 + 0 + 35 = 65
        assert score == 65.0

    def test_no_decision_adds_10(self, engine):
        score = self._score(
            engine,
            price_discount_pct=0.0,
            deal_size_usd=0.0,
            deal_outcome="no_decision",
        )
        # 30 + 0 + 10 = 40
        assert score == 40.0

    def test_closed_lost_adds_0(self, engine):
        score = self._score(
            engine,
            price_discount_pct=0.0,
            deal_size_usd=0.0,
            deal_outcome="closed_lost",
        )
        assert score == 30.0

    def test_score_clamped_at_100(self, engine):
        score = self._score(
            engine,
            price_discount_pct=0.0,
            deal_size_usd=200_000.0,
            deal_outcome="closed_won",
        )
        assert score <= 100.0

    def test_returns_float(self, engine, perfect_won):
        assert isinstance(engine._deal_health_score(perfect_won), float)


# ===========================================================================
# 12. TestComposite
# ===========================================================================

class TestComposite:

    def test_composite_formula(self, engine):
        # 0.30 + 0.30 + 0.25 + 0.15 weights
        c = engine._composite(100.0, 100.0, 100.0, 100.0)
        assert c == 100.0

    def test_composite_zeros(self, engine):
        c = engine._composite(0.0, 0.0, 0.0, 0.0)
        assert c == 0.0

    def test_composite_weights_process_30pct(self, engine):
        c = engine._composite(100.0, 0.0, 0.0, 0.0)
        assert c == pytest.approx(30.0, abs=0.1)

    def test_composite_weights_execution_30pct(self, engine):
        c = engine._composite(0.0, 100.0, 0.0, 0.0)
        assert c == pytest.approx(30.0, abs=0.1)

    def test_composite_weights_relationship_25pct(self, engine):
        c = engine._composite(0.0, 0.0, 100.0, 0.0)
        assert c == pytest.approx(25.0, abs=0.1)

    def test_composite_weights_health_15pct(self, engine):
        c = engine._composite(0.0, 0.0, 0.0, 100.0)
        assert c == pytest.approx(15.0, abs=0.1)

    def test_composite_clamped_at_100(self, engine):
        c = engine._composite(200.0, 200.0, 200.0, 200.0)
        assert c <= 100.0

    def test_composite_clamped_at_0(self, engine):
        c = engine._composite(-50.0, -50.0, -50.0, -50.0)
        assert c >= 0.0

    def test_composite_partial(self, engine):
        # 50*0.30 + 60*0.30 + 40*0.25 + 80*0.15 = 15+18+10+12 = 55
        c = engine._composite(50.0, 60.0, 40.0, 80.0)
        assert c == pytest.approx(55.0, abs=0.1)

    def test_composite_returns_float(self, engine):
        c = engine._composite(50.0, 50.0, 50.0, 50.0)
        assert isinstance(c, float)


# ===========================================================================
# 13. TestParseOutcome
# ===========================================================================

class TestParseOutcome:

    def test_closed_won(self, engine):
        assert engine._parse_outcome("closed_won") == DealOutcome.CLOSED_WON

    def test_closed_lost(self, engine):
        assert engine._parse_outcome("closed_lost") == DealOutcome.CLOSED_LOST

    def test_no_decision(self, engine):
        assert engine._parse_outcome("no_decision") == DealOutcome.NO_DECISION

    def test_churned(self, engine):
        assert engine._parse_outcome("churned") == DealOutcome.CHURNED

    def test_invalid_falls_back_to_closed_lost(self, engine):
        assert engine._parse_outcome("garbage") == DealOutcome.CLOSED_LOST

    def test_empty_string_falls_back(self, engine):
        assert engine._parse_outcome("") == DealOutcome.CLOSED_LOST


# ===========================================================================
# 14. TestLossReason
# ===========================================================================

class TestLossReason:

    def _reason(self, engine, **kwargs) -> LossReason:
        inp = make_input(**kwargs)
        outcome = engine._parse_outcome(inp.deal_outcome)
        return engine._loss_reason(inp, outcome)

    def test_closed_won_returns_no_loss(self, engine):
        reason = self._reason(engine, deal_outcome="closed_won")
        assert reason == LossReason.NO_LOSS

    def test_champion_inactive_non_won_returns_champion_loss(self, engine):
        reason = self._reason(
            engine,
            deal_outcome="closed_lost",
            champion_active_at_close=0,
            competitive_deal=0,
            price_discount_pct=0.0,
        )
        assert reason == LossReason.CHAMPION_LOSS

    def test_champion_inactive_no_decision_not_champion_loss(self, engine):
        # NO_DECISION is excluded from champion_loss by the condition
        reason = self._reason(
            engine,
            deal_outcome="no_decision",
            champion_active_at_close=0,
            competitive_deal=0,
            price_discount_pct=0.0,
        )
        assert reason != LossReason.CHAMPION_LOSS

    def test_competitive_no_displacement_returns_competitor(self, engine):
        reason = self._reason(
            engine,
            deal_outcome="closed_lost",
            champion_active_at_close=1,
            competitive_deal=1,
            competitor_displacement=0,
            price_discount_pct=0.0,
        )
        assert reason == LossReason.COMPETITOR

    def test_competitive_with_displacement_not_competitor(self, engine):
        # If displaced, competitive branch is bypassed
        reason = self._reason(
            engine,
            deal_outcome="closed_lost",
            champion_active_at_close=1,
            competitive_deal=1,
            competitor_displacement=1,
            price_discount_pct=0.0,
            discovery_calls_completed=3,
            objections_resolved_pct=90.0,
            close_date_slips=0,
        )
        assert reason != LossReason.COMPETITOR

    def test_high_discount_returns_price(self, engine):
        reason = self._reason(
            engine,
            deal_outcome="closed_lost",
            champion_active_at_close=1,
            competitive_deal=0,
            price_discount_pct=20.0,
        )
        assert reason == LossReason.PRICE

    def test_discount_below_20_not_price(self, engine):
        reason = self._reason(
            engine,
            deal_outcome="closed_lost",
            champion_active_at_close=1,
            competitive_deal=0,
            price_discount_pct=19.0,
            close_date_slips=3,
        )
        # Falls to timing (3+ slips)
        assert reason == LossReason.TIMING

    def test_3_plus_slips_returns_timing(self, engine):
        reason = self._reason(
            engine,
            deal_outcome="closed_lost",
            champion_active_at_close=1,
            competitive_deal=0,
            price_discount_pct=0.0,
            close_date_slips=3,
        )
        assert reason == LossReason.TIMING

    def test_few_discovery_returns_poor_process(self, engine):
        reason = self._reason(
            engine,
            deal_outcome="closed_lost",
            champion_active_at_close=1,
            competitive_deal=0,
            price_discount_pct=0.0,
            close_date_slips=0,
            discovery_calls_completed=1,
            objections_resolved_pct=90.0,
        )
        assert reason == LossReason.POOR_PROCESS

    def test_low_orr_returns_poor_process(self, engine):
        reason = self._reason(
            engine,
            deal_outcome="closed_lost",
            champion_active_at_close=1,
            competitive_deal=0,
            price_discount_pct=0.0,
            close_date_slips=0,
            discovery_calls_completed=3,
            objections_resolved_pct=30.0,
        )
        assert reason == LossReason.POOR_PROCESS

    def test_default_fallback_returns_timing(self, engine):
        # No champions issue, no competition, no high discount, no slips, good process
        reason = self._reason(
            engine,
            deal_outcome="closed_lost",
            champion_active_at_close=1,
            competitive_deal=0,
            price_discount_pct=0.0,
            close_date_slips=0,
            discovery_calls_completed=3,
            objections_resolved_pct=90.0,
        )
        assert reason == LossReason.TIMING

    def test_churned_champion_inactive_returns_champion_loss(self, engine):
        reason = self._reason(
            engine,
            deal_outcome="churned",
            champion_active_at_close=0,
            competitive_deal=0,
        )
        assert reason == LossReason.CHAMPION_LOSS


# ===========================================================================
# 15. TestRepBehaviorPattern
# ===========================================================================

class TestRepBehaviorPattern:

    def _pattern(self, engine, composite, outcome_str, **kwargs) -> RepBehaviorPattern:
        inp = make_input(deal_outcome=outcome_str, **kwargs)
        outcome = engine._parse_outcome(outcome_str)
        return engine._rep_behavior_pattern(composite, inp, outcome)

    def test_composite_75_won_is_exemplary(self, engine):
        assert self._pattern(engine, 75.0, "closed_won") == RepBehaviorPattern.EXEMPLARY

    def test_composite_100_won_is_exemplary(self, engine):
        assert self._pattern(engine, 100.0, "closed_won") == RepBehaviorPattern.EXEMPLARY

    def test_composite_75_lost_not_exemplary(self, engine):
        # Must be closed_won for exemplary
        assert self._pattern(engine, 75.0, "closed_lost") != RepBehaviorPattern.EXEMPLARY

    def test_composite_60_any_is_solid(self, engine):
        assert self._pattern(engine, 60.0, "closed_lost") == RepBehaviorPattern.SOLID

    def test_composite_74_lost_is_solid(self, engine):
        assert self._pattern(engine, 74.0, "closed_lost") == RepBehaviorPattern.SOLID

    def test_composite_60_won_is_solid(self, engine):
        assert self._pattern(engine, 60.0, "closed_won") == RepBehaviorPattern.SOLID

    def test_composite_40_is_improvable(self, engine):
        assert self._pattern(engine, 40.0, "closed_lost") == RepBehaviorPattern.IMPROVABLE

    def test_composite_59_is_improvable(self, engine):
        assert self._pattern(engine, 59.0, "closed_lost") == RepBehaviorPattern.IMPROVABLE

    def test_composite_39_is_high_risk(self, engine):
        assert self._pattern(engine, 39.0, "closed_lost") == RepBehaviorPattern.HIGH_RISK

    def test_composite_0_is_high_risk(self, engine):
        assert self._pattern(engine, 0.0, "closed_lost") == RepBehaviorPattern.HIGH_RISK


# ===========================================================================
# 16. TestWinProbabilityIndex
# ===========================================================================

class TestWinProbabilityIndex:

    def _wpi(self, engine, **kwargs) -> float:
        inp = make_input(**kwargs)
        return engine._win_probability_index(inp)

    def test_base_is_50(self, engine):
        score = self._wpi(
            engine,
            exec_sponsor_engaged=0,
            champion_active_at_close=0,
            mutual_action_plan_used=0,
            objections_resolved_pct=0.0,
            close_date_slips=0,
            price_discount_pct=0.0,
        )
        assert score == 50.0

    def test_exec_sponsor_adds_15(self, engine):
        score = self._wpi(
            engine,
            exec_sponsor_engaged=1,
            champion_active_at_close=0,
            mutual_action_plan_used=0,
            objections_resolved_pct=0.0,
            close_date_slips=0,
            price_discount_pct=0.0,
        )
        assert score == 65.0

    def test_champion_active_adds_15(self, engine):
        score = self._wpi(
            engine,
            exec_sponsor_engaged=0,
            champion_active_at_close=1,
            mutual_action_plan_used=0,
            objections_resolved_pct=0.0,
            close_date_slips=0,
            price_discount_pct=0.0,
        )
        assert score == 65.0

    def test_map_adds_10(self, engine):
        score = self._wpi(
            engine,
            exec_sponsor_engaged=0,
            champion_active_at_close=0,
            mutual_action_plan_used=1,
            objections_resolved_pct=0.0,
            close_date_slips=0,
            price_discount_pct=0.0,
        )
        assert score == 60.0

    def test_orr_gte_80_adds_10(self, engine):
        score = self._wpi(
            engine,
            exec_sponsor_engaged=0,
            champion_active_at_close=0,
            mutual_action_plan_used=0,
            objections_resolved_pct=80.0,
            close_date_slips=0,
            price_discount_pct=0.0,
        )
        assert score == 60.0

    def test_3_plus_slips_subtracts_15(self, engine):
        score = self._wpi(
            engine,
            exec_sponsor_engaged=0,
            champion_active_at_close=0,
            mutual_action_plan_used=0,
            objections_resolved_pct=0.0,
            close_date_slips=3,
            price_discount_pct=0.0,
        )
        assert score == 35.0

    def test_discount_gte_20_subtracts_10(self, engine):
        score = self._wpi(
            engine,
            exec_sponsor_engaged=0,
            champion_active_at_close=0,
            mutual_action_plan_used=0,
            objections_resolved_pct=0.0,
            close_date_slips=0,
            price_discount_pct=20.0,
        )
        assert score == 40.0

    def test_max_score_100(self, engine):
        score = self._wpi(
            engine,
            exec_sponsor_engaged=1,
            champion_active_at_close=1,
            mutual_action_plan_used=1,
            objections_resolved_pct=80.0,
            close_date_slips=0,
            price_discount_pct=0.0,
        )
        assert score <= 100.0

    def test_min_score_0(self, engine):
        score = self._wpi(
            engine,
            exec_sponsor_engaged=0,
            champion_active_at_close=0,
            mutual_action_plan_used=0,
            objections_resolved_pct=0.0,
            close_date_slips=3,
            price_discount_pct=50.0,
        )
        assert score >= 0.0

    def test_returns_float(self, engine, perfect_won):
        assert isinstance(engine._win_probability_index(perfect_won), float)


# ===========================================================================
# 17. TestReplicationValue
# ===========================================================================

class TestReplicationValue:

    def _repl(self, engine, composite, outcome_str) -> float:
        inp = make_input(deal_outcome=outcome_str)
        outcome = engine._parse_outcome(outcome_str)
        return engine._replication_value(composite, inp, outcome)

    def test_won_replication_value(self, engine):
        val = self._repl(engine, 80.0, "closed_won")
        assert val == pytest.approx(min(100.0, 80.0 * 1.1), abs=0.1)

    def test_lost_replication_value_is_reduced(self, engine):
        val = self._repl(engine, 80.0, "closed_lost")
        assert val == pytest.approx(80.0 * 0.4, abs=0.1)

    def test_no_decision_replication_reduced(self, engine):
        val = self._repl(engine, 50.0, "no_decision")
        assert val == pytest.approx(50.0 * 0.4, abs=0.1)

    def test_churned_replication_reduced(self, engine):
        val = self._repl(engine, 50.0, "churned")
        assert val == pytest.approx(50.0 * 0.4, abs=0.1)

    def test_won_composite_0_value_0(self, engine):
        val = self._repl(engine, 0.0, "closed_won")
        assert val == 0.0

    def test_lost_composite_0_value_0(self, engine):
        val = self._repl(engine, 0.0, "closed_lost")
        assert val == 0.0

    def test_won_capped_at_100(self, engine):
        val = self._repl(engine, 100.0, "closed_won")
        assert val <= 100.0

    def test_returns_float(self, engine, perfect_won):
        outcome = engine._parse_outcome(perfect_won.deal_outcome)
        val = engine._replication_value(80.0, perfect_won, outcome)
        assert isinstance(val, float)


# ===========================================================================
# 18. TestWinLossAction
# ===========================================================================

class TestWinLossActionClassifier:

    def test_exemplary_best_practice_gets_share(self, engine):
        action = engine._win_loss_action(RepBehaviorPattern.EXEMPLARY, True, False)
        assert action == WinLossAction.SHARE_AS_BEST_PRACTICE

    def test_high_risk_gets_urgent_intervention(self, engine):
        action = engine._win_loss_action(RepBehaviorPattern.HIGH_RISK, False, False)
        assert action == WinLossAction.URGENT_INTERVENTION

    def test_needs_coaching_not_high_risk_gets_urgent_intervention(self, engine):
        # needs_coaching=True → urgent_intervention (second check)
        action = engine._win_loss_action(RepBehaviorPattern.SOLID, False, True)
        assert action == WinLossAction.URGENT_INTERVENTION

    def test_improvable_no_coaching_gets_coach_and_improve(self, engine):
        action = engine._win_loss_action(RepBehaviorPattern.IMPROVABLE, False, False)
        assert action == WinLossAction.COACH_AND_IMPROVE

    def test_solid_no_coaching_gets_replicate(self, engine):
        action = engine._win_loss_action(RepBehaviorPattern.SOLID, False, False)
        assert action == WinLossAction.REPLICATE

    def test_exemplary_not_best_practice_gets_urgent_if_coaching(self, engine):
        action = engine._win_loss_action(RepBehaviorPattern.EXEMPLARY, False, True)
        assert action == WinLossAction.URGENT_INTERVENTION

    def test_exemplary_not_best_practice_no_coaching_gets_replicate(self, engine):
        action = engine._win_loss_action(RepBehaviorPattern.EXEMPLARY, False, False)
        assert action == WinLossAction.REPLICATE


# ===========================================================================
# 19. TestIsBestPractice
# ===========================================================================

class TestIsBestPractice:

    def test_won_composite_75_is_best_practice(self, engine, perfect_won):
        result = engine.analyze(perfect_won)
        # Perfect deal should be best_practice (composite >= 75 + closed_won)
        if result.win_loss_composite >= 75.0:
            assert result.is_best_practice is True

    def test_lost_not_best_practice(self, engine, weak_lost):
        result = engine.analyze(weak_lost)
        assert result.is_best_practice is False

    def test_won_low_composite_not_best_practice(self, engine):
        # Force low composite by degrading all scores
        inp = make_input(
            deal_outcome="closed_won",
            discovery_calls_completed=0,
            mutual_action_plan_used=0,
            objections_resolved_pct=0.0,
            close_date_slips=3,
            proposal_revision_count=4,
            rep_activity_score=10.0,
            stakeholders_engaged=1,
            exec_sponsor_engaged=0,
            champion_active_at_close=0,
            post_deal_survey_score=-1.0,
            demo_count=0,
            expected_cycle_days=0,
        )
        result = engine.analyze(inp)
        if result.win_loss_composite < 75.0:
            assert result.is_best_practice is False

    def test_no_decision_not_best_practice(self, engine):
        inp = make_input(deal_outcome="no_decision")
        result = engine.analyze(inp)
        assert result.is_best_practice is False


# ===========================================================================
# 20. TestNeedsCoaching
# ===========================================================================

class TestNeedsCoaching:

    def test_composite_below_45_needs_coaching(self, engine):
        inp = make_lost_input(
            discovery_calls_completed=0,
            mutual_action_plan_used=0,
            objections_resolved_pct=0.0,
            close_date_slips=3,
            proposal_revision_count=4,
            rep_activity_score=10.0,
            stakeholders_engaged=1,
            exec_sponsor_engaged=0,
            champion_active_at_close=0,
            demo_count=0,
        )
        result = engine.analyze(inp)
        if result.win_loss_composite < 45.0:
            assert result.needs_coaching is True

    def test_lost_low_process_needs_coaching(self, engine):
        # closed_lost AND process_quality_score < 50 → needs coaching
        inp = make_lost_input(
            discovery_calls_completed=1,
            mutual_action_plan_used=0,
            objections_resolved_pct=20.0,
            close_date_slips=0,
        )
        result = engine.analyze(inp)
        if result.deal_outcome == DealOutcome.CLOSED_LOST and result.process_quality_score < 50.0:
            assert result.needs_coaching is True

    def test_perfect_won_not_needs_coaching(self, engine, perfect_won):
        result = engine.analyze(perfect_won)
        if result.win_loss_composite >= 45.0 and result.deal_outcome == DealOutcome.CLOSED_WON:
            assert result.needs_coaching is False


# ===========================================================================
# 21. TestAnalyze
# ===========================================================================

class TestAnalyze:

    def test_returns_win_loss_pattern_result(self, engine, perfect_won):
        result = engine.analyze(perfect_won)
        assert isinstance(result, WinLossPatternResult)

    def test_deal_id_preserved(self, engine, perfect_won):
        result = engine.analyze(perfect_won)
        assert result.deal_id == "D001"

    def test_deal_name_preserved(self, engine, perfect_won):
        result = engine.analyze(perfect_won)
        assert result.deal_name == "Test Deal"

    def test_deal_outcome_is_enum(self, engine, perfect_won):
        result = engine.analyze(perfect_won)
        assert isinstance(result.deal_outcome, DealOutcome)

    def test_loss_reason_is_enum(self, engine, perfect_won):
        result = engine.analyze(perfect_won)
        assert isinstance(result.loss_reason, LossReason)

    def test_rep_behavior_pattern_is_enum(self, engine, perfect_won):
        result = engine.analyze(perfect_won)
        assert isinstance(result.rep_behavior_pattern, RepBehaviorPattern)

    def test_win_loss_action_is_enum(self, engine, perfect_won):
        result = engine.analyze(perfect_won)
        assert isinstance(result.win_loss_action, WinLossAction)

    def test_scores_in_range(self, engine, perfect_won):
        result = engine.analyze(perfect_won)
        for score in (
            result.process_quality_score,
            result.execution_score,
            result.relationship_score,
            result.deal_health_score,
            result.win_loss_composite,
            result.win_probability_index,
            result.replication_value,
        ):
            assert 0.0 <= score <= 100.0, f"Score out of range: {score}"

    def test_perfect_won_no_loss_reason(self, engine, perfect_won):
        result = engine.analyze(perfect_won)
        assert result.loss_reason == LossReason.NO_LOSS

    def test_perfect_won_exemplary(self, engine, perfect_won):
        result = engine.analyze(perfect_won)
        assert result.rep_behavior_pattern == RepBehaviorPattern.EXEMPLARY

    def test_perfect_won_is_best_practice(self, engine, perfect_won):
        result = engine.analyze(perfect_won)
        assert result.is_best_practice is True

    def test_perfect_won_share_as_best_practice(self, engine, perfect_won):
        result = engine.analyze(perfect_won)
        assert result.win_loss_action == WinLossAction.SHARE_AS_BEST_PRACTICE

    def test_result_stored_in_results(self, engine, perfect_won):
        result = engine.analyze(perfect_won)
        assert result in engine._results

    def test_invalid_outcome_falls_back(self, engine):
        inp = make_input(deal_outcome="garbage")
        result = engine.analyze(inp)
        assert result.deal_outcome == DealOutcome.CLOSED_LOST

    def test_composite_calculation(self, engine, perfect_won):
        result = engine.analyze(perfect_won)
        expected = round(
            result.process_quality_score * 0.30
            + result.execution_score * 0.30
            + result.relationship_score * 0.25
            + result.deal_health_score * 0.15,
            1,
        )
        assert result.win_loss_composite == pytest.approx(expected, abs=0.1)

    def test_no_decision_outcome(self, engine):
        inp = make_input(deal_outcome="no_decision")
        result = engine.analyze(inp)
        assert result.deal_outcome == DealOutcome.NO_DECISION

    def test_churned_outcome(self, engine):
        inp = make_input(deal_outcome="churned")
        result = engine.analyze(inp)
        assert result.deal_outcome == DealOutcome.CHURNED


# ===========================================================================
# 22. TestAnalyzeBatch
# ===========================================================================

class TestAnalyzeBatch:

    def test_returns_list(self, engine):
        results = engine.analyze_batch([make_input(deal_id="B1"), make_input(deal_id="B2")])
        assert isinstance(results, list)

    def test_correct_length(self, engine):
        results = engine.analyze_batch([make_input(deal_id=f"X{i}") for i in range(5)])
        assert len(results) == 5

    def test_all_results_stored(self, engine):
        engine.analyze_batch([make_input(deal_id="BA1"), make_input(deal_id="BA2")])
        assert len(engine._results) == 2

    def test_empty_batch(self, engine):
        results = engine.analyze_batch([])
        assert results == []

    def test_order_preserved(self, engine):
        ids = ["Z1", "Z2", "Z3"]
        inps = [make_input(deal_id=i) for i in ids]
        results = engine.analyze_batch(inps)
        assert [r.deal_id for r in results] == ids

    def test_all_items_are_results(self, engine):
        results = engine.analyze_batch([make_input(deal_id="C1"), make_input(deal_id="C2")])
        for r in results:
            assert isinstance(r, WinLossPatternResult)


# ===========================================================================
# 23. TestBestPracticeDeals
# ===========================================================================

class TestBestPracticeDeals:

    def test_empty_engine_returns_empty(self, engine):
        assert engine.best_practice_deals == []

    def test_perfect_won_in_best_practice(self, engine, perfect_won):
        result = engine.analyze(perfect_won)
        if result.is_best_practice:
            assert result in engine.best_practice_deals

    def test_all_best_practice_deals_are_best_practice(self, engine, perfect_won):
        engine.analyze(perfect_won)
        assert all(r.is_best_practice for r in engine.best_practice_deals)

    def test_lost_not_in_best_practice(self, engine, weak_lost):
        engine.analyze(weak_lost)
        assert engine.best_practice_deals == []

    def test_mixed_batch(self, engine, perfect_won, weak_lost):
        engine.analyze(perfect_won)
        engine.analyze(weak_lost)
        for r in engine.best_practice_deals:
            assert r.is_best_practice is True


# ===========================================================================
# 24. TestCoachingQueue
# ===========================================================================

class TestCoachingQueue:

    def test_empty_engine_returns_empty(self, engine):
        assert engine.coaching_queue == []

    def test_all_coaching_queue_items_need_coaching(self, engine, weak_lost):
        engine.analyze(weak_lost)
        for r in engine.coaching_queue:
            assert r.needs_coaching is True

    def test_perfect_won_not_in_coaching(self, engine, perfect_won):
        result = engine.analyze(perfect_won)
        if not result.needs_coaching:
            assert result not in engine.coaching_queue

    def test_coaching_queue_is_list(self, engine, weak_lost):
        engine.analyze(weak_lost)
        assert isinstance(engine.coaching_queue, list)


# ===========================================================================
# 25. TestWinRate
# ===========================================================================

class TestWinRate:

    def test_empty_engine_returns_0(self, engine):
        assert engine.win_rate == 0.0

    def test_all_won_returns_100(self, engine):
        engine.analyze(make_input(deal_id="W1"))
        engine.analyze(make_input(deal_id="W2"))
        assert engine.win_rate == 100.0

    def test_no_won_returns_0(self, engine):
        engine.analyze(make_lost_input(deal_id="L1"))
        assert engine.win_rate == 0.0

    def test_one_of_three_won_returns_33_3(self, engine):
        engine.analyze(make_input(deal_id="W1"))
        engine.analyze(make_lost_input(deal_id="L1"))
        engine.analyze(make_lost_input(deal_id="L2"))
        assert engine.win_rate == pytest.approx(33.3, abs=0.1)

    def test_two_of_three_won_returns_66_7(self, engine):
        engine.analyze(make_input(deal_id="W1"))
        engine.analyze(make_input(deal_id="W2"))
        engine.analyze(make_lost_input(deal_id="L1"))
        assert engine.win_rate == pytest.approx(66.7, abs=0.1)

    def test_win_rate_rounded_one_decimal(self, engine):
        engine.analyze(make_input(deal_id="W1"))
        engine.analyze(make_lost_input(deal_id="L1"))
        rate = engine.win_rate
        assert rate == round(rate, 1)

    def test_no_decision_not_counted_as_won(self, engine):
        engine.analyze(make_input(deal_id="ND1", deal_outcome="no_decision"))
        assert engine.win_rate == 0.0

    def test_churned_not_counted_as_won(self, engine):
        engine.analyze(make_input(deal_id="CH1", deal_outcome="churned"))
        assert engine.win_rate == 0.0

    def test_win_rate_is_float(self, engine, perfect_won):
        engine.analyze(perfect_won)
        assert isinstance(engine.win_rate, float)


# ===========================================================================
# 26. TestAvgWinLossComposite
# ===========================================================================

class TestAvgWinLossComposite:

    def test_empty_returns_0(self, engine):
        assert engine.avg_win_loss_composite == 0.0

    def test_single_deal_avg_equals_composite(self, engine, perfect_won):
        result = engine.analyze(perfect_won)
        assert engine.avg_win_loss_composite == result.win_loss_composite

    def test_two_deals_avg(self, engine):
        r1 = engine.analyze(make_input(deal_id="A"))
        r2 = engine.analyze(make_lost_input(deal_id="B"))
        expected = round((r1.win_loss_composite + r2.win_loss_composite) / 2, 1)
        assert engine.avg_win_loss_composite == expected

    def test_returns_float(self, engine, perfect_won):
        engine.analyze(perfect_won)
        assert isinstance(engine.avg_win_loss_composite, float)

    def test_rounded_one_decimal(self, engine):
        engine.analyze(make_input(deal_id="X1"))
        engine.analyze(make_lost_input(deal_id="X2"))
        val = engine.avg_win_loss_composite
        assert val == round(val, 1)


# ===========================================================================
# 27. TestReset
# ===========================================================================

class TestReset:

    def test_reset_clears_results(self, engine, perfect_won):
        engine.analyze(perfect_won)
        engine.reset()
        assert engine._results == []

    def test_reset_clears_multiple(self, engine):
        engine.analyze(make_input(deal_id="R1"))
        engine.analyze(make_input(deal_id="R2"))
        engine.analyze(make_lost_input(deal_id="R3"))
        engine.reset()
        assert len(engine._results) == 0

    def test_win_rate_zero_after_reset(self, engine, perfect_won):
        engine.analyze(perfect_won)
        engine.reset()
        assert engine.win_rate == 0.0

    def test_avg_composite_zero_after_reset(self, engine, perfect_won):
        engine.analyze(perfect_won)
        engine.reset()
        assert engine.avg_win_loss_composite == 0.0

    def test_best_practice_empty_after_reset(self, engine, perfect_won):
        engine.analyze(perfect_won)
        engine.reset()
        assert engine.best_practice_deals == []

    def test_coaching_queue_empty_after_reset(self, engine, weak_lost):
        engine.analyze(weak_lost)
        engine.reset()
        assert engine.coaching_queue == []

    def test_can_analyze_after_reset(self, engine, perfect_won):
        engine.analyze(perfect_won)
        engine.reset()
        result = engine.analyze(make_input(deal_id="NEW"))
        assert isinstance(result, WinLossPatternResult)
        assert len(engine._results) == 1

    def test_summary_resets_to_zero(self, engine, perfect_won):
        engine.analyze(perfect_won)
        engine.reset()
        assert engine.summary()["total"] == 0


# ===========================================================================
# 28. TestSummaryWithData
# ===========================================================================

class TestSummaryWithData:

    def _load(self, engine):
        engine.analyze(make_input(deal_id="S1", deal_outcome="closed_won"))
        engine.analyze(make_input(deal_id="S2", deal_outcome="closed_won"))
        engine.analyze(make_lost_input(deal_id="S3"))

    def test_total_correct(self, engine):
        self._load(engine)
        assert engine.summary()["total"] == 3

    def test_win_rate_matches_property(self, engine):
        self._load(engine)
        s = engine.summary()
        assert s["win_rate"] == engine.win_rate

    def test_outcome_counts_closed_won(self, engine):
        self._load(engine)
        s = engine.summary()
        assert s["outcome_counts"]["closed_won"] == 2

    def test_outcome_counts_closed_lost(self, engine):
        self._load(engine)
        s = engine.summary()
        assert s["outcome_counts"]["closed_lost"] == 1

    def test_loss_reason_counts_has_no_loss(self, engine):
        self._load(engine)
        s = engine.summary()
        # Won deals have no_loss
        assert "no_loss" in s["loss_reason_counts"]

    def test_behavior_counts_is_dict(self, engine):
        self._load(engine)
        s = engine.summary()
        assert isinstance(s["behavior_counts"], dict)

    def test_action_counts_is_dict(self, engine):
        self._load(engine)
        s = engine.summary()
        assert isinstance(s["action_counts"], dict)

    def test_avg_composite_matches_property(self, engine):
        self._load(engine)
        s = engine.summary()
        assert s["avg_win_loss_composite"] == engine.avg_win_loss_composite

    def test_best_practice_count_matches_property(self, engine):
        self._load(engine)
        s = engine.summary()
        assert s["best_practice_count"] == len(engine.best_practice_deals)

    def test_coaching_count_matches_property(self, engine):
        self._load(engine)
        s = engine.summary()
        assert s["coaching_count"] == len(engine.coaching_queue)

    def test_avg_process_quality_score_numeric(self, engine):
        self._load(engine)
        s = engine.summary()
        assert isinstance(s["avg_process_quality_score"], (int, float))

    def test_avg_execution_score_numeric(self, engine):
        self._load(engine)
        s = engine.summary()
        assert isinstance(s["avg_execution_score"], (int, float))

    def test_avg_relationship_score_numeric(self, engine):
        self._load(engine)
        s = engine.summary()
        assert isinstance(s["avg_relationship_score"], (int, float))

    def test_avg_replication_value_numeric(self, engine):
        self._load(engine)
        s = engine.summary()
        assert isinstance(s["avg_replication_value"], (int, float))

    def test_avg_scores_in_range(self, engine):
        self._load(engine)
        s = engine.summary()
        for key in (
            "avg_process_quality_score", "avg_execution_score",
            "avg_relationship_score", "avg_replication_value",
        ):
            assert 0.0 <= s[key] <= 100.0, f"{key} out of range"


# ===========================================================================
# 29. TestEdgeCases
# ===========================================================================

class TestEdgeCases:

    def test_all_zeros_input_does_not_crash(self, engine):
        inp = make_input(
            deal_outcome="closed_lost",
            deal_size_usd=0.0,
            sales_cycle_days=0,
            expected_cycle_days=0,
            discovery_calls_completed=0,
            stakeholders_engaged=0,
            exec_sponsor_engaged=0,
            champion_active_at_close=0,
            proposal_revision_count=0,
            demo_count=0,
            mutual_action_plan_used=0,
            competitive_deal=0,
            competitor_displacement=0,
            price_discount_pct=0.0,
            close_date_slips=0,
            objections_raised=0,
            objections_resolved_pct=0.0,
            post_deal_survey_score=-1.0,
            rep_activity_score=0.0,
        )
        result = engine.analyze(inp)
        assert isinstance(result, WinLossPatternResult)

    def test_max_discount_input(self, engine):
        inp = make_input(price_discount_pct=100.0, deal_outcome="closed_lost")
        result = engine.analyze(inp)
        assert result.loss_reason == LossReason.PRICE

    def test_multiple_analyses_accumulate(self, engine):
        for i in range(10):
            engine.analyze(make_input(deal_id=f"M{i}"))
        assert len(engine._results) == 10

    def test_composite_is_weighted_sum(self, engine, perfect_won):
        result = engine.analyze(perfect_won)
        expected = round(
            result.process_quality_score * 0.30
            + result.execution_score * 0.30
            + result.relationship_score * 0.25
            + result.deal_health_score * 0.15,
            1,
        )
        assert result.win_loss_composite == pytest.approx(expected, abs=0.05)

    def test_to_dict_enum_values_are_strings(self, engine, perfect_won):
        d = engine.analyze(perfect_won).to_dict()
        assert isinstance(d["deal_outcome"], str)
        assert isinstance(d["loss_reason"], str)
        assert isinstance(d["rep_behavior_pattern"], str)
        assert isinstance(d["win_loss_action"], str)

    def test_analyze_batch_accumulates_in_results(self, engine):
        engine.analyze_batch([make_input(deal_id=f"T{i}") for i in range(3)])
        assert len(engine._results) == 3

    def test_competitive_won_with_displacement(self, engine):
        inp = make_input(
            deal_outcome="closed_won",
            competitive_deal=1,
            competitor_displacement=1,
        )
        result = engine.analyze(inp)
        # Won → no_loss regardless of competitive situation
        assert result.loss_reason == LossReason.NO_LOSS

    def test_no_decision_champion_inactive_not_champion_loss(self, engine):
        inp = make_input(
            deal_outcome="no_decision",
            champion_active_at_close=0,
            competitive_deal=0,
            price_discount_pct=0.0,
        )
        result = engine.analyze(inp)
        assert result.loss_reason != LossReason.CHAMPION_LOSS

    def test_survey_score_boundary_80(self, engine):
        score = engine._relationship_score(make_input(
            stakeholders_engaged=1,
            exec_sponsor_engaged=0,
            champion_active_at_close=0,
            post_deal_survey_score=80.0,
        ))
        assert score == 15.0

    def test_survey_score_boundary_60(self, engine):
        score = engine._relationship_score(make_input(
            stakeholders_engaged=1,
            exec_sponsor_engaged=0,
            champion_active_at_close=0,
            post_deal_survey_score=60.0,
        ))
        assert score == 8.0

    def test_orr_boundary_80(self, engine):
        score = engine._process_quality_score(make_input(
            discovery_calls_completed=0,
            mutual_action_plan_used=0,
            objections_resolved_pct=80.0,
            close_date_slips=1,
            proposal_revision_count=0,
        ))
        # 0 + 0 + 30 + 7 = 37
        assert score == 37.0

    def test_orr_boundary_60(self, engine):
        score = engine._process_quality_score(make_input(
            discovery_calls_completed=0,
            mutual_action_plan_used=0,
            objections_resolved_pct=60.0,
            close_date_slips=1,
            proposal_revision_count=0,
        ))
        # 0 + 0 + 20 + 7 = 27
        assert score == 27.0

    def test_orr_boundary_40(self, engine):
        score = engine._process_quality_score(make_input(
            discovery_calls_completed=0,
            mutual_action_plan_used=0,
            objections_resolved_pct=40.0,
            close_date_slips=1,
            proposal_revision_count=0,
        ))
        # 0 + 0 + 10 + 7 = 17
        assert score == 17.0
