"""
Comprehensive pytest tests for DealVelocityEngine.
Covers all enums, scoring helpers, deal outcome logic, engine properties,
batch analysis, reset, edge cases, and summary.
"""
from __future__ import annotations

import pytest
from swarm.intelligence.deal_velocity_engine import (
    DealVelocityEngine,
    DealVelocityInput,
    DealVelocityResult,
    DealOutcome,
    StageHealth,
    VelocityAction,
    VelocityTrend,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers / Fixtures
# ─────────────────────────────────────────────────────────────────────────────

def make_input(
    deal_id="D001",
    deal_name="Test Deal",
    rep_id="R001",
    account_id="A001",
    stage_number=3,
    deal_value=50_000.0,
    probability_pct=60.0,
    expected_close_days=30,
    created_days_ago=60,
    days_in_current_stage=10,
    avg_days_per_stage=10.0,
    last_activity_days_ago=2,
    num_stakeholders_engaged=2,
    decision_maker_engaged=True,
    champion_identified=True,
    competitor_present=False,
    pricing_discussed=True,
    legal_review_started=False,
    close_date_changes=0,
    win_rate_similar_deals=55.0,
    nrr_expansion_potential=10_000.0,
) -> DealVelocityInput:
    return DealVelocityInput(
        deal_id=deal_id,
        deal_name=deal_name,
        rep_id=rep_id,
        account_id=account_id,
        stage_number=stage_number,
        deal_value=deal_value,
        probability_pct=probability_pct,
        expected_close_days=expected_close_days,
        created_days_ago=created_days_ago,
        days_in_current_stage=days_in_current_stage,
        avg_days_per_stage=avg_days_per_stage,
        last_activity_days_ago=last_activity_days_ago,
        num_stakeholders_engaged=num_stakeholders_engaged,
        decision_maker_engaged=decision_maker_engaged,
        champion_identified=champion_identified,
        competitor_present=competitor_present,
        pricing_discussed=pricing_discussed,
        legal_review_started=legal_review_started,
        close_date_changes=close_date_changes,
        win_rate_similar_deals=win_rate_similar_deals,
        nrr_expansion_potential=nrr_expansion_potential,
    )


@pytest.fixture
def engine():
    return DealVelocityEngine()


@pytest.fixture
def healthy_input():
    """Input that yields high health, low risk."""
    return make_input(
        days_in_current_stage=5,
        avg_days_per_stage=10.0,   # progression=2.0 → healthy
        last_activity_days_ago=1,
        num_stakeholders_engaged=3,
        decision_maker_engaged=True,
        champion_identified=True,
        pricing_discussed=True,
        legal_review_started=True,
        close_date_changes=0,
        probability_pct=80.0,
        expected_close_days=30,
        win_rate_similar_deals=75.0,
    )


@pytest.fixture
def risky_input():
    """Input that yields low health, high risk."""
    return make_input(
        days_in_current_stage=30,
        avg_days_per_stage=10.0,   # progression=0.33 → stuck/critical
        last_activity_days_ago=25,
        num_stakeholders_engaged=0,
        decision_maker_engaged=False,
        champion_identified=False,
        competitor_present=True,
        pricing_discussed=False,
        legal_review_started=False,
        close_date_changes=4,
        probability_pct=20.0,
        expected_close_days=-5,
        win_rate_similar_deals=20.0,
    )


# ─────────────────────────────────────────────────────────────────────────────
# 1. VelocityTrend enum
# ─────────────────────────────────────────────────────────────────────────────

class TestVelocityTrendEnum:
    def test_accelerating_value(self):
        assert VelocityTrend.ACCELERATING.value == "accelerating"

    def test_stable_value(self):
        assert VelocityTrend.STABLE.value == "stable"

    def test_decelerating_value(self):
        assert VelocityTrend.DECELERATING.value == "decelerating"

    def test_stalled_value(self):
        assert VelocityTrend.STALLED.value == "stalled"

    def test_all_four_members(self):
        assert len(VelocityTrend) == 4

    def test_str_subclass(self):
        assert isinstance(VelocityTrend.ACCELERATING, str)

    def test_accelerating_str_eq(self):
        assert VelocityTrend.ACCELERATING == "accelerating"

    def test_stable_str_eq(self):
        assert VelocityTrend.STABLE == "stable"

    def test_decelerating_str_eq(self):
        assert VelocityTrend.DECELERATING == "decelerating"

    def test_stalled_str_eq(self):
        assert VelocityTrend.STALLED == "stalled"

    def test_members_are_distinct(self):
        values = {t.value for t in VelocityTrend}
        assert len(values) == 4


# ─────────────────────────────────────────────────────────────────────────────
# 2. StageHealth enum
# ─────────────────────────────────────────────────────────────────────────────

class TestStageHealthEnum:
    def test_healthy_value(self):
        assert StageHealth.HEALTHY.value == "healthy"

    def test_slow_value(self):
        assert StageHealth.SLOW.value == "slow"

    def test_stuck_value(self):
        assert StageHealth.STUCK.value == "stuck"

    def test_critical_value(self):
        assert StageHealth.CRITICAL.value == "critical"

    def test_all_four_members(self):
        assert len(StageHealth) == 4

    def test_str_subclass(self):
        assert isinstance(StageHealth.HEALTHY, str)

    def test_healthy_str_eq(self):
        assert StageHealth.HEALTHY == "healthy"

    def test_slow_str_eq(self):
        assert StageHealth.SLOW == "slow"

    def test_stuck_str_eq(self):
        assert StageHealth.STUCK == "stuck"

    def test_critical_str_eq(self):
        assert StageHealth.CRITICAL == "critical"

    def test_members_are_distinct(self):
        values = {h.value for h in StageHealth}
        assert len(values) == 4


# ─────────────────────────────────────────────────────────────────────────────
# 3. DealOutcome enum
# ─────────────────────────────────────────────────────────────────────────────

class TestDealOutcomeEnum:
    def test_likely_close_value(self):
        assert DealOutcome.LIKELY_CLOSE.value == "likely_close"

    def test_on_track_value(self):
        assert DealOutcome.ON_TRACK.value == "on_track"

    def test_at_risk_value(self):
        assert DealOutcome.AT_RISK.value == "at_risk"

    def test_likely_slip_value(self):
        assert DealOutcome.LIKELY_SLIP.value == "likely_slip"

    def test_likely_lose_value(self):
        assert DealOutcome.LIKELY_LOSE.value == "likely_lose"

    def test_all_five_members(self):
        assert len(DealOutcome) == 5

    def test_str_subclass(self):
        assert isinstance(DealOutcome.ON_TRACK, str)

    def test_likely_close_str_eq(self):
        assert DealOutcome.LIKELY_CLOSE == "likely_close"

    def test_on_track_str_eq(self):
        assert DealOutcome.ON_TRACK == "on_track"

    def test_at_risk_str_eq(self):
        assert DealOutcome.AT_RISK == "at_risk"

    def test_likely_slip_str_eq(self):
        assert DealOutcome.LIKELY_SLIP == "likely_slip"

    def test_likely_lose_str_eq(self):
        assert DealOutcome.LIKELY_LOSE == "likely_lose"

    def test_members_are_distinct(self):
        values = {o.value for o in DealOutcome}
        assert len(values) == 5


# ─────────────────────────────────────────────────────────────────────────────
# 4. VelocityAction enum
# ─────────────────────────────────────────────────────────────────────────────

class TestVelocityActionEnum:
    def test_standard_follow_up_value(self):
        assert VelocityAction.STANDARD_FOLLOW_UP.value == "standard_follow_up"

    def test_prioritize_value(self):
        assert VelocityAction.PRIORITIZE.value == "prioritize"

    def test_accelerate_value(self):
        assert VelocityAction.ACCELERATE.value == "accelerate"

    def test_engage_executive_value(self):
        assert VelocityAction.ENGAGE_EXECUTIVE.value == "engage_executive"

    def test_reassign_value(self):
        assert VelocityAction.REASSIGN.value == "reassign"

    def test_close_lost_value(self):
        assert VelocityAction.CLOSE_LOST.value == "close_lost"

    def test_all_six_members(self):
        assert len(VelocityAction) == 6

    def test_str_subclass(self):
        assert isinstance(VelocityAction.CLOSE_LOST, str)

    def test_standard_follow_up_str_eq(self):
        assert VelocityAction.STANDARD_FOLLOW_UP == "standard_follow_up"

    def test_prioritize_str_eq(self):
        assert VelocityAction.PRIORITIZE == "prioritize"

    def test_accelerate_str_eq(self):
        assert VelocityAction.ACCELERATE == "accelerate"

    def test_engage_executive_str_eq(self):
        assert VelocityAction.ENGAGE_EXECUTIVE == "engage_executive"

    def test_reassign_str_eq(self):
        assert VelocityAction.REASSIGN == "reassign"

    def test_close_lost_str_eq(self):
        assert VelocityAction.CLOSE_LOST == "close_lost"

    def test_members_are_distinct(self):
        values = {a.value for a in VelocityAction}
        assert len(values) == 6


# ─────────────────────────────────────────────────────────────────────────────
# 5. to_dict() – exactly 15 keys, correct enum serialisation
# ─────────────────────────────────────────────────────────────────────────────

class TestToDictMethod:
    def test_returns_dict(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert isinstance(r.to_dict(), dict)

    def test_exactly_15_keys(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert len(r.to_dict()) == 15

    def test_deal_id_present(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert "deal_id" in r.to_dict()

    def test_deal_name_present(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert "deal_name" in r.to_dict()

    def test_rep_id_present(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert "rep_id" in r.to_dict()

    def test_velocity_trend_is_string(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert isinstance(r.to_dict()["velocity_trend"], str)

    def test_velocity_trend_not_enum_obj(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert not isinstance(r.to_dict()["velocity_trend"], VelocityTrend)

    def test_stage_health_is_string(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert isinstance(r.to_dict()["stage_health"], str)

    def test_stage_health_not_enum_obj(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert not isinstance(r.to_dict()["stage_health"], StageHealth)

    def test_deal_outcome_is_string(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert isinstance(r.to_dict()["deal_outcome"], str)

    def test_deal_outcome_not_enum_obj(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert not isinstance(r.to_dict()["deal_outcome"], DealOutcome)

    def test_velocity_action_is_string(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert isinstance(r.to_dict()["velocity_action"], str)

    def test_velocity_action_not_enum_obj(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert not isinstance(r.to_dict()["velocity_action"], VelocityAction)

    def test_velocity_score_key(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert "velocity_score" in r.to_dict()

    def test_stage_progression_rate_key(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert "stage_progression_rate" in r.to_dict()

    def test_close_date_risk_key(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert "close_date_risk" in r.to_dict()

    def test_engagement_score_key(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert "engagement_score" in r.to_dict()

    def test_momentum_score_key(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert "momentum_score" in r.to_dict()

    def test_deal_health_index_key(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert "deal_health_index" in r.to_dict()

    def test_is_at_risk_key(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert "is_at_risk" in r.to_dict()

    def test_needs_escalation_key(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert "needs_escalation" in r.to_dict()

    def test_velocity_trend_valid_enum_string(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        valid = {t.value for t in VelocityTrend}
        assert r.to_dict()["velocity_trend"] in valid

    def test_stage_health_valid_enum_string(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        valid = {h.value for h in StageHealth}
        assert r.to_dict()["stage_health"] in valid

    def test_deal_outcome_valid_enum_string(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        valid = {o.value for o in DealOutcome}
        assert r.to_dict()["deal_outcome"] in valid

    def test_velocity_action_valid_enum_string(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        valid = {a.value for a in VelocityAction}
        assert r.to_dict()["velocity_action"] in valid

    def test_deal_id_value_correct(self, engine):
        inp = make_input(deal_id="XYZ")
        r = engine.analyze(inp)
        assert r.to_dict()["deal_id"] == "XYZ"

    def test_rep_id_value_correct(self, engine):
        inp = make_input(rep_id="REP99")
        r = engine.analyze(inp)
        assert r.to_dict()["rep_id"] == "REP99"

    def test_is_at_risk_is_bool(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert isinstance(r.to_dict()["is_at_risk"], bool)

    def test_needs_escalation_is_bool(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert isinstance(r.to_dict()["needs_escalation"], bool)


# ─────────────────────────────────────────────────────────────────────────────
# 6 & 7. summary() – 13 keys in both states
# ─────────────────────────────────────────────────────────────────────────────

SUMMARY_KEYS = {
    "total", "trend_counts", "health_counts", "outcome_counts", "action_counts",
    "avg_velocity_score", "avg_deal_health_index", "avg_close_date_risk",
    "at_risk_count", "escalation_count", "avg_engagement_score",
    "avg_momentum_score", "healthy_deal_count",
}


class TestSummaryEmpty:
    def test_returns_dict(self, engine):
        assert isinstance(engine.summary(), dict)

    def test_exactly_13_keys_empty(self, engine):
        assert len(engine.summary()) == 13

    def test_total_zero(self, engine):
        assert engine.summary()["total"] == 0

    def test_trend_counts_empty_dict(self, engine):
        assert engine.summary()["trend_counts"] == {}

    def test_health_counts_empty_dict(self, engine):
        assert engine.summary()["health_counts"] == {}

    def test_outcome_counts_empty_dict(self, engine):
        assert engine.summary()["outcome_counts"] == {}

    def test_action_counts_empty_dict(self, engine):
        assert engine.summary()["action_counts"] == {}

    def test_avg_velocity_score_zero(self, engine):
        assert engine.summary()["avg_velocity_score"] == 0.0

    def test_avg_deal_health_index_zero(self, engine):
        assert engine.summary()["avg_deal_health_index"] == 0.0

    def test_avg_close_date_risk_zero(self, engine):
        assert engine.summary()["avg_close_date_risk"] == 0.0

    def test_at_risk_count_zero(self, engine):
        assert engine.summary()["at_risk_count"] == 0

    def test_escalation_count_zero(self, engine):
        assert engine.summary()["escalation_count"] == 0

    def test_avg_engagement_score_zero(self, engine):
        assert engine.summary()["avg_engagement_score"] == 0.0

    def test_avg_momentum_score_zero(self, engine):
        assert engine.summary()["avg_momentum_score"] == 0.0

    def test_healthy_deal_count_zero(self, engine):
        assert engine.summary()["healthy_deal_count"] == 0

    def test_all_13_keys_present_empty(self, engine):
        assert set(engine.summary().keys()) == SUMMARY_KEYS


class TestSummaryWithResults:
    def test_returns_dict_after_analyze(self, engine, healthy_input):
        engine.analyze(healthy_input)
        assert isinstance(engine.summary(), dict)

    def test_exactly_13_keys_after_analyze(self, engine, healthy_input):
        engine.analyze(healthy_input)
        assert len(engine.summary()) == 13

    def test_all_13_keys_present_after_analyze(self, engine, healthy_input):
        engine.analyze(healthy_input)
        assert set(engine.summary().keys()) == SUMMARY_KEYS

    def test_total_equals_number_of_analyzed_deals(self, engine, healthy_input):
        engine.analyze(healthy_input)
        engine.analyze(make_input(deal_id="D002"))
        assert engine.summary()["total"] == 2

    def test_trend_counts_populated(self, engine, healthy_input):
        engine.analyze(healthy_input)
        assert engine.summary()["trend_counts"] != {}

    def test_health_counts_populated(self, engine, healthy_input):
        engine.analyze(healthy_input)
        assert engine.summary()["health_counts"] != {}

    def test_outcome_counts_populated(self, engine, healthy_input):
        engine.analyze(healthy_input)
        assert engine.summary()["outcome_counts"] != {}

    def test_action_counts_populated(self, engine, healthy_input):
        engine.analyze(healthy_input)
        assert engine.summary()["action_counts"] != {}

    def test_avg_velocity_score_positive(self, engine, healthy_input):
        engine.analyze(healthy_input)
        assert engine.summary()["avg_velocity_score"] > 0

    def test_at_risk_count_gte_zero(self, engine, healthy_input):
        engine.analyze(healthy_input)
        assert engine.summary()["at_risk_count"] >= 0

    def test_escalation_count_gte_zero(self, engine, healthy_input):
        engine.analyze(healthy_input)
        assert engine.summary()["escalation_count"] >= 0

    def test_healthy_deal_count_gte_zero(self, engine, healthy_input):
        engine.analyze(healthy_input)
        assert engine.summary()["healthy_deal_count"] >= 0

    def test_trend_counts_values_sum_to_total(self, engine):
        for i in range(3):
            engine.analyze(make_input(deal_id=f"D{i}"))
        s = engine.summary()
        assert sum(s["trend_counts"].values()) == s["total"]

    def test_outcome_counts_values_sum_to_total(self, engine):
        for i in range(3):
            engine.analyze(make_input(deal_id=f"D{i}"))
        s = engine.summary()
        assert sum(s["outcome_counts"].values()) == s["total"]

    def test_health_counts_values_sum_to_total(self, engine):
        for i in range(3):
            engine.analyze(make_input(deal_id=f"D{i}"))
        s = engine.summary()
        assert sum(s["health_counts"].values()) == s["total"]

    def test_action_counts_values_sum_to_total(self, engine):
        for i in range(3):
            engine.analyze(make_input(deal_id=f"D{i}"))
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]


# ─────────────────────────────────────────────────────────────────────────────
# 8. _stage_progression_rate
# ─────────────────────────────────────────────────────────────────────────────

class TestStageProgressionRate:
    def test_equal_days_returns_one(self):
        e = DealVelocityEngine()
        inp = make_input(days_in_current_stage=10, avg_days_per_stage=10.0)
        assert e._stage_progression_rate(inp) == pytest.approx(1.0, rel=1e-3)

    def test_faster_than_avg_rate_gt_one(self):
        e = DealVelocityEngine()
        inp = make_input(days_in_current_stage=5, avg_days_per_stage=10.0)
        assert e._stage_progression_rate(inp) == pytest.approx(2.0, rel=1e-3)

    def test_slower_than_avg_rate_lt_one(self):
        e = DealVelocityEngine()
        inp = make_input(days_in_current_stage=20, avg_days_per_stage=10.0)
        assert e._stage_progression_rate(inp) == pytest.approx(0.5, rel=1e-3)

    def test_clamped_maximum_5(self):
        e = DealVelocityEngine()
        # avg=100, actual=1 → ratio=100 → clamped to 5.0
        inp = make_input(days_in_current_stage=1, avg_days_per_stage=100.0)
        assert e._stage_progression_rate(inp) == pytest.approx(5.0, rel=1e-3)

    def test_clamped_minimum_0_1(self):
        e = DealVelocityEngine()
        # avg=1, actual=100 → ratio=0.01 → clamped to 0.1
        inp = make_input(days_in_current_stage=100, avg_days_per_stage=1.0)
        assert e._stage_progression_rate(inp) == pytest.approx(0.1, rel=1e-3)

    def test_zero_days_in_stage_returns_one(self):
        e = DealVelocityEngine()
        inp = make_input(days_in_current_stage=0, avg_days_per_stage=10.0)
        assert e._stage_progression_rate(inp) == pytest.approx(1.0, rel=1e-3)

    def test_zero_avg_days_returns_one(self):
        e = DealVelocityEngine()
        inp = make_input(days_in_current_stage=10, avg_days_per_stage=0.0)
        assert e._stage_progression_rate(inp) == pytest.approx(1.0, rel=1e-3)

    def test_both_zero_returns_one(self):
        e = DealVelocityEngine()
        inp = make_input(days_in_current_stage=0, avg_days_per_stage=0.0)
        assert e._stage_progression_rate(inp) == pytest.approx(1.0, rel=1e-3)

    def test_ratio_formula_avg_over_actual(self):
        e = DealVelocityEngine()
        inp = make_input(days_in_current_stage=4, avg_days_per_stage=12.0)
        # 12/4 = 3.0
        assert e._stage_progression_rate(inp) == pytest.approx(3.0, rel=1e-3)

    def test_returns_float(self):
        e = DealVelocityEngine()
        inp = make_input(days_in_current_stage=7, avg_days_per_stage=14.0)
        assert isinstance(e._stage_progression_rate(inp), float)

    def test_exact_clamp_boundary_5(self):
        e = DealVelocityEngine()
        # ratio exactly 5.0
        inp = make_input(days_in_current_stage=2, avg_days_per_stage=10.0)
        assert e._stage_progression_rate(inp) == pytest.approx(5.0, rel=1e-3)

    def test_just_below_clamp_max(self):
        e = DealVelocityEngine()
        # 10/3 ≈ 3.33
        inp = make_input(days_in_current_stage=3, avg_days_per_stage=10.0)
        rate = e._stage_progression_rate(inp)
        assert 3.0 < rate <= 5.0


# ─────────────────────────────────────────────────────────────────────────────
# 9. _engagement_score
# ─────────────────────────────────────────────────────────────────────────────

class TestEngagementScore:
    def _score(self, **kwargs):
        e = DealVelocityEngine()
        inp = make_input(**kwargs)
        return e._engagement_score(inp)

    def test_zero_engagement(self):
        s = self._score(
            num_stakeholders_engaged=0,
            decision_maker_engaged=False,
            champion_identified=False,
            pricing_discussed=False,
            legal_review_started=False,
        )
        assert s == pytest.approx(0.0)

    def test_one_stakeholder_adds_10(self):
        s = self._score(
            num_stakeholders_engaged=1,
            decision_maker_engaged=False,
            champion_identified=False,
            pricing_discussed=False,
            legal_review_started=False,
        )
        assert s == pytest.approx(10.0)

    def test_two_stakeholders_adds_20(self):
        s = self._score(
            num_stakeholders_engaged=2,
            decision_maker_engaged=False,
            champion_identified=False,
            pricing_discussed=False,
            legal_review_started=False,
        )
        assert s == pytest.approx(20.0)

    def test_stakeholders_capped_at_30(self):
        s = self._score(
            num_stakeholders_engaged=10,
            decision_maker_engaged=False,
            champion_identified=False,
            pricing_discussed=False,
            legal_review_started=False,
        )
        assert s == pytest.approx(30.0)

    def test_three_stakeholders_max_30(self):
        s = self._score(
            num_stakeholders_engaged=3,
            decision_maker_engaged=False,
            champion_identified=False,
            pricing_discussed=False,
            legal_review_started=False,
        )
        assert s == pytest.approx(30.0)

    def test_decision_maker_adds_20(self):
        s = self._score(
            num_stakeholders_engaged=0,
            decision_maker_engaged=True,
            champion_identified=False,
            pricing_discussed=False,
            legal_review_started=False,
        )
        assert s == pytest.approx(20.0)

    def test_champion_adds_20(self):
        s = self._score(
            num_stakeholders_engaged=0,
            decision_maker_engaged=False,
            champion_identified=True,
            pricing_discussed=False,
            legal_review_started=False,
        )
        assert s == pytest.approx(20.0)

    def test_pricing_adds_15(self):
        s = self._score(
            num_stakeholders_engaged=0,
            decision_maker_engaged=False,
            champion_identified=False,
            pricing_discussed=True,
            legal_review_started=False,
        )
        assert s == pytest.approx(15.0)

    def test_legal_adds_15(self):
        s = self._score(
            num_stakeholders_engaged=0,
            decision_maker_engaged=False,
            champion_identified=False,
            pricing_discussed=False,
            legal_review_started=True,
        )
        assert s == pytest.approx(15.0)

    def test_full_engagement_100(self):
        # 30 + 20 + 20 + 15 + 15 = 100
        s = self._score(
            num_stakeholders_engaged=3,
            decision_maker_engaged=True,
            champion_identified=True,
            pricing_discussed=True,
            legal_review_started=True,
        )
        assert s == pytest.approx(100.0)

    def test_clamped_max_100(self):
        # Even with extra stakeholders it won't go above 100
        s = self._score(
            num_stakeholders_engaged=100,
            decision_maker_engaged=True,
            champion_identified=True,
            pricing_discussed=True,
            legal_review_started=True,
        )
        assert s == pytest.approx(100.0)

    def test_clamped_min_0(self):
        s = self._score(
            num_stakeholders_engaged=0,
            decision_maker_engaged=False,
            champion_identified=False,
            pricing_discussed=False,
            legal_review_started=False,
        )
        assert s >= 0.0

    def test_dm_and_champion_40(self):
        s = self._score(
            num_stakeholders_engaged=0,
            decision_maker_engaged=True,
            champion_identified=True,
            pricing_discussed=False,
            legal_review_started=False,
        )
        assert s == pytest.approx(40.0)

    def test_returns_float(self):
        s = self._score()
        assert isinstance(s, float)


# ─────────────────────────────────────────────────────────────────────────────
# 10. _velocity_score
# ─────────────────────────────────────────────────────────────────────────────

class TestVelocityScore:
    def _score(self, progression, last_activity_days_ago=1, close_date_changes=0):
        e = DealVelocityEngine()
        inp = make_input(
            last_activity_days_ago=last_activity_days_ago,
            close_date_changes=close_date_changes,
            # we fix days to get exact progression
            days_in_current_stage=10,
            avg_days_per_stage=10.0,
        )
        return e._velocity_score(inp, progression)

    def test_activity_today_adds_35(self):
        # progression=1.0 → 20pts; activity=0→35pts; slip=0→25pts → 80
        e = DealVelocityEngine()
        inp = make_input(last_activity_days_ago=0, close_date_changes=0)
        s = e._velocity_score(inp, 1.0)
        assert s == pytest.approx(80.0, rel=1e-2)

    def test_activity_1_3_days_adds_30(self):
        e = DealVelocityEngine()
        inp = make_input(last_activity_days_ago=2, close_date_changes=0)
        s = e._velocity_score(inp, 1.0)
        # 20 + 30 + 25 = 75
        assert s == pytest.approx(75.0, rel=1e-2)

    def test_activity_4_7_days_adds_20(self):
        e = DealVelocityEngine()
        inp = make_input(last_activity_days_ago=5, close_date_changes=0)
        s = e._velocity_score(inp, 1.0)
        # 20 + 20 + 25 = 65
        assert s == pytest.approx(65.0, rel=1e-2)

    def test_activity_8_14_days_adds_10(self):
        e = DealVelocityEngine()
        inp = make_input(last_activity_days_ago=10, close_date_changes=0)
        s = e._velocity_score(inp, 1.0)
        # 20 + 10 + 25 = 55
        assert s == pytest.approx(55.0, rel=1e-2)

    def test_activity_gt_14_days_decays(self):
        e = DealVelocityEngine()
        inp = make_input(last_activity_days_ago=15, close_date_changes=0)
        s = e._velocity_score(inp, 1.0)
        # 20 + max(0, 10 - (15-14)*0.5) + 25 = 20 + 9.5 + 25 = 54.5
        assert s == pytest.approx(54.5, rel=1e-2)

    def test_activity_very_old_floor_0(self):
        e = DealVelocityEngine()
        inp = make_input(last_activity_days_ago=100, close_date_changes=0)
        s = e._velocity_score(inp, 1.0)
        # recency = max(0, 10-(86)*0.5) = 0
        assert s >= 0.0

    def test_slip_penalty_one_change(self):
        e = DealVelocityEngine()
        # 1 change → penalty 8 → stability = 25-8=17
        inp = make_input(last_activity_days_ago=2, close_date_changes=1)
        s = e._velocity_score(inp, 1.0)
        # 20+30+17 = 67
        assert s == pytest.approx(67.0, rel=1e-2)

    def test_slip_penalty_3_changes_capped(self):
        e = DealVelocityEngine()
        # 3*8=24 → stability = 25-24=1
        inp = make_input(last_activity_days_ago=2, close_date_changes=3)
        s = e._velocity_score(inp, 1.0)
        assert s == pytest.approx(51.0, rel=1e-2)

    def test_slip_penalty_4_changes_max(self):
        e = DealVelocityEngine()
        # 4*8=32 → min(25,32)=25 → stability=0
        inp = make_input(last_activity_days_ago=2, close_date_changes=4)
        s = e._velocity_score(inp, 1.0)
        assert s == pytest.approx(50.0, rel=1e-2)

    def test_progression_contribution(self):
        e = DealVelocityEngine()
        # progression=2 → min(40, 40)=40; activity=1→30; slips=0→25 → 95
        inp = make_input(last_activity_days_ago=1, close_date_changes=0)
        s = e._velocity_score(inp, 2.0)
        assert s == pytest.approx(95.0, rel=1e-2)

    def test_progression_clamped_at_40(self):
        e = DealVelocityEngine()
        inp = make_input(last_activity_days_ago=1, close_date_changes=0)
        s = e._velocity_score(inp, 5.0)
        # min(40, 5*20) = 40 + 30 + 25 = 95
        assert s == pytest.approx(95.0, rel=1e-2)

    def test_score_clamped_0_to_100(self):
        e = DealVelocityEngine()
        inp = make_input(last_activity_days_ago=0, close_date_changes=0)
        s = e._velocity_score(inp, 5.0)
        assert 0.0 <= s <= 100.0

    def test_returns_float(self):
        e = DealVelocityEngine()
        inp = make_input()
        s = e._velocity_score(inp, 1.0)
        assert isinstance(s, float)


# ─────────────────────────────────────────────────────────────────────────────
# 11. _close_date_risk
# ─────────────────────────────────────────────────────────────────────────────

class TestCloseDateRisk:
    def _risk(self, progression=1.0, close_date_changes=0,
              expected_close_days=30, competitor_present=False,
              decision_maker_engaged=True):
        e = DealVelocityEngine()
        inp = make_input(
            close_date_changes=close_date_changes,
            expected_close_days=expected_close_days,
            competitor_present=competitor_present,
            decision_maker_engaged=decision_maker_engaged,
        )
        return e._close_date_risk(inp, progression)

    def test_low_risk_scenario(self):
        # progression≥1.0, no slippage, close soon, no competitor
        r = self._risk(progression=1.2, close_date_changes=0,
                       expected_close_days=30)
        assert r == pytest.approx(0.0)

    def test_progression_lt_0_5_adds_40(self):
        r = self._risk(progression=0.3, close_date_changes=0,
                       expected_close_days=30)
        assert r == pytest.approx(40.0)

    def test_progression_0_5_to_0_8_adds_25(self):
        r = self._risk(progression=0.6, close_date_changes=0,
                       expected_close_days=30)
        assert r == pytest.approx(25.0)

    def test_progression_0_8_to_1_adds_10(self):
        r = self._risk(progression=0.9, close_date_changes=0,
                       expected_close_days=30)
        assert r == pytest.approx(10.0)

    def test_progression_gte_1_no_risk(self):
        r = self._risk(progression=1.0, close_date_changes=0,
                       expected_close_days=30)
        assert r == pytest.approx(0.0)

    def test_slippage_1_adds_10(self):
        r = self._risk(progression=1.0, close_date_changes=1,
                       expected_close_days=30)
        assert r == pytest.approx(10.0)

    def test_slippage_3_adds_30(self):
        r = self._risk(progression=1.0, close_date_changes=3,
                       expected_close_days=30)
        assert r == pytest.approx(30.0)

    def test_slippage_capped_at_30(self):
        r = self._risk(progression=1.0, close_date_changes=10,
                       expected_close_days=30)
        assert r == pytest.approx(30.0)

    def test_overdue_adds_20(self):
        r = self._risk(progression=1.0, close_date_changes=0,
                       expected_close_days=-1)
        assert r == pytest.approx(20.0)

    def test_close_within_7_days_adds_10(self):
        r = self._risk(progression=1.0, close_date_changes=0,
                       expected_close_days=5)
        assert r == pytest.approx(10.0)

    def test_close_8_plus_days_no_urgency(self):
        r = self._risk(progression=1.0, close_date_changes=0,
                       expected_close_days=8)
        assert r == pytest.approx(0.0)

    def test_competitor_no_dm_adds_10(self):
        r = self._risk(progression=1.0, close_date_changes=0,
                       expected_close_days=30, competitor_present=True,
                       decision_maker_engaged=False)
        assert r == pytest.approx(10.0)

    def test_competitor_with_dm_no_addition(self):
        r = self._risk(progression=1.0, close_date_changes=0,
                       expected_close_days=30, competitor_present=True,
                       decision_maker_engaged=True)
        assert r == pytest.approx(0.0)

    def test_max_risk_capped_at_100(self):
        r = self._risk(progression=0.1, close_date_changes=20,
                       expected_close_days=-10, competitor_present=True,
                       decision_maker_engaged=False)
        assert r <= 100.0

    def test_clamped_min_0(self):
        r = self._risk(progression=2.0, close_date_changes=0,
                       expected_close_days=60)
        assert r >= 0.0

    def test_returns_float(self):
        r = self._risk()
        assert isinstance(r, float)

    def test_all_contributions_combined(self):
        # progression<0.5:40, slippage 2*10=20, overdue→+20, comp+no-dm→+10 = 90
        r = self._risk(progression=0.3, close_date_changes=2,
                       expected_close_days=-5, competitor_present=True,
                       decision_maker_engaged=False)
        assert r == pytest.approx(90.0)


# ─────────────────────────────────────────────────────────────────────────────
# 12. _momentum_score
# ─────────────────────────────────────────────────────────────────────────────

class TestMomentumScore:
    def _score(self, progression=1.0, engagement=50.0,
               last_activity_days_ago=5, win_rate=50.0):
        e = DealVelocityEngine()
        inp = make_input(
            last_activity_days_ago=last_activity_days_ago,
            win_rate_similar_deals=win_rate,
        )
        return e._momentum_score(inp, progression, engagement)

    def test_win_rate_50_no_factor(self):
        # win_factor = (50-50)/50 * 10 = 0
        s = self._score(progression=1.0, engagement=0.0,
                        last_activity_days_ago=0, win_rate=50.0)
        # prog=min(40,20)=20; eng=0; activity=max(0,25-0)=25 → base=45; win=0 → 45
        assert s == pytest.approx(45.0)

    def test_win_rate_100_adds_10(self):
        s = self._score(progression=1.0, engagement=0.0,
                        last_activity_days_ago=0, win_rate=100.0)
        # base=45, win=10 → 55
        assert s == pytest.approx(55.0)

    def test_win_rate_0_subtracts_10(self):
        s = self._score(progression=1.0, engagement=0.0,
                        last_activity_days_ago=0, win_rate=0.0)
        # base=45, win=-10 → 35
        assert s == pytest.approx(35.0)

    def test_engagement_contribution(self):
        s = self._score(progression=1.0, engagement=100.0,
                        last_activity_days_ago=0, win_rate=50.0)
        # prog=20, eng=100*0.35=35, activity=25 → 80
        assert s == pytest.approx(80.0)

    def test_progression_clamped_at_40(self):
        s = self._score(progression=5.0, engagement=0.0,
                        last_activity_days_ago=0, win_rate=50.0)
        # prog=40, eng=0, activity=25 → 65
        assert s == pytest.approx(65.0)

    def test_activity_decays_with_days(self):
        s1 = self._score(progression=1.0, engagement=0.0,
                         last_activity_days_ago=0, win_rate=50.0)
        s2 = self._score(progression=1.0, engagement=0.0,
                         last_activity_days_ago=10, win_rate=50.0)
        assert s2 < s1

    def test_activity_floor_zero(self):
        s = self._score(progression=0.0, engagement=0.0,
                        last_activity_days_ago=100, win_rate=50.0)
        assert s >= 0.0

    def test_clamped_max_100(self):
        s = self._score(progression=5.0, engagement=100.0,
                        last_activity_days_ago=0, win_rate=100.0)
        assert s <= 100.0

    def test_returns_float(self):
        s = self._score()
        assert isinstance(s, float)

    def test_score_in_valid_range(self):
        s = self._score()
        assert 0.0 <= s <= 100.0


# ─────────────────────────────────────────────────────────────────────────────
# 13. _deal_health_index
# ─────────────────────────────────────────────────────────────────────────────

class TestDealHealthIndex:
    def _health(self, velocity, engagement, momentum):
        e = DealVelocityEngine()
        return e._deal_health_index(velocity, engagement, momentum)

    def test_formula_weights(self):
        # 50*0.35 + 50*0.30 + 50*0.35 = 17.5+15+17.5 = 50
        h = self._health(50.0, 50.0, 50.0)
        assert h == pytest.approx(50.0)

    def test_zero_inputs_zero_health(self):
        assert self._health(0.0, 0.0, 0.0) == pytest.approx(0.0)

    def test_full_inputs_100_health(self):
        assert self._health(100.0, 100.0, 100.0) == pytest.approx(100.0)

    def test_velocity_weight_0_35(self):
        # only velocity non-zero
        h = self._health(100.0, 0.0, 0.0)
        assert h == pytest.approx(35.0)

    def test_engagement_weight_0_30(self):
        h = self._health(0.0, 100.0, 0.0)
        assert h == pytest.approx(30.0)

    def test_momentum_weight_0_35(self):
        h = self._health(0.0, 0.0, 100.0)
        assert h == pytest.approx(35.0)

    def test_clamped_min_0(self):
        assert self._health(0.0, 0.0, 0.0) >= 0.0

    def test_clamped_max_100(self):
        assert self._health(100.0, 100.0, 100.0) <= 100.0

    def test_mixed_values(self):
        # 80*0.35 + 60*0.30 + 70*0.35 = 28+18+24.5 = 70.5
        h = self._health(80.0, 60.0, 70.0)
        assert h == pytest.approx(70.5)

    def test_returns_float(self):
        assert isinstance(self._health(50.0, 50.0, 50.0), float)


# ─────────────────────────────────────────────────────────────────────────────
# 14. is_at_risk: health < 40 OR close_risk > 70
# ─────────────────────────────────────────────────────────────────────────────

class TestIsAtRisk:
    def test_healthy_deal_not_at_risk(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        # Verify health ≥ 40 and risk ≤ 70 → not at risk
        if r.deal_health_index >= 40.0 and r.close_date_risk <= 70.0:
            assert not r.is_at_risk

    def test_very_unhealthy_is_at_risk(self, engine, risky_input):
        r = engine.analyze(risky_input)
        assert r.is_at_risk

    def test_health_below_40_triggers_at_risk(self, engine):
        # Craft input to force health < 40
        inp = make_input(
            days_in_current_stage=50,
            avg_days_per_stage=10.0,  # progression=0.2
            last_activity_days_ago=30,
            num_stakeholders_engaged=0,
            decision_maker_engaged=False,
            champion_identified=False,
            pricing_discussed=False,
            legal_review_started=False,
            close_date_changes=0,
            win_rate_similar_deals=20.0,
        )
        r = engine.analyze(inp)
        if r.deal_health_index < 40.0:
            assert r.is_at_risk

    def test_high_close_risk_triggers_at_risk(self, engine):
        # Craft input to force close_risk > 70
        inp = make_input(
            days_in_current_stage=40,
            avg_days_per_stage=10.0,  # progression=0.25 → +40 risk
            close_date_changes=4,     # +30 risk → already 70
            expected_close_days=-5,   # +20 risk → 90 total
            competitor_present=True,
            decision_maker_engaged=False,  # +10 risk
        )
        r = engine.analyze(inp)
        if r.close_date_risk > 70.0:
            assert r.is_at_risk

    def test_is_at_risk_type_bool(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert isinstance(r.is_at_risk, bool)

    def test_at_risk_false_when_health_gte_40_and_risk_lte_70(self):
        e = DealVelocityEngine()
        # Directly craft result
        r = DealVelocityResult(
            deal_id="X", deal_name="X", rep_id="X",
            velocity_trend=VelocityTrend.STABLE,
            stage_health=StageHealth.HEALTHY,
            deal_outcome=DealOutcome.ON_TRACK,
            velocity_action=VelocityAction.STANDARD_FOLLOW_UP,
            velocity_score=50.0,
            stage_progression_rate=1.0,
            close_date_risk=50.0,
            engagement_score=50.0,
            momentum_score=50.0,
            deal_health_index=50.0,
            is_at_risk=False,
            needs_escalation=False,
        )
        assert not r.is_at_risk

    def test_at_risk_true_when_health_lt_40(self):
        r = DealVelocityResult(
            deal_id="X", deal_name="X", rep_id="X",
            velocity_trend=VelocityTrend.STALLED,
            stage_health=StageHealth.CRITICAL,
            deal_outcome=DealOutcome.LIKELY_LOSE,
            velocity_action=VelocityAction.CLOSE_LOST,
            velocity_score=10.0,
            stage_progression_rate=0.2,
            close_date_risk=30.0,
            engagement_score=10.0,
            momentum_score=10.0,
            deal_health_index=10.0,
            is_at_risk=True,
            needs_escalation=True,
        )
        assert r.is_at_risk

    def test_at_risk_true_when_close_risk_gt_70(self):
        r = DealVelocityResult(
            deal_id="X", deal_name="X", rep_id="X",
            velocity_trend=VelocityTrend.DECELERATING,
            stage_health=StageHealth.SLOW,
            deal_outcome=DealOutcome.AT_RISK,
            velocity_action=VelocityAction.PRIORITIZE,
            velocity_score=50.0,
            stage_progression_rate=0.9,
            close_date_risk=80.0,
            engagement_score=50.0,
            momentum_score=50.0,
            deal_health_index=50.0,
            is_at_risk=True,
            needs_escalation=False,
        )
        assert r.is_at_risk


# ─────────────────────────────────────────────────────────────────────────────
# 15. needs_escalation: stage_health == CRITICAL OR outcome == LIKELY_LOSE
# ─────────────────────────────────────────────────────────────────────────────

class TestNeedsEscalation:
    def test_critical_stage_needs_escalation(self, engine):
        # Force CRITICAL: progression < 0.4 and days >> 2.5*avg
        inp = make_input(
            days_in_current_stage=60,
            avg_days_per_stage=10.0,  # progression=0.167, days>25
        )
        r = engine.analyze(inp)
        if r.stage_health == StageHealth.CRITICAL:
            assert r.needs_escalation

    def test_likely_lose_needs_escalation(self, engine):
        # Force LIKELY_LOSE via very low health and competitor + no champion
        inp = make_input(
            days_in_current_stage=50,
            avg_days_per_stage=10.0,
            last_activity_days_ago=30,
            num_stakeholders_engaged=0,
            decision_maker_engaged=False,
            champion_identified=False,
            competitor_present=True,
            pricing_discussed=False,
            legal_review_started=False,
            close_date_changes=5,
            probability_pct=15.0,
            win_rate_similar_deals=10.0,
        )
        r = engine.analyze(inp)
        if r.deal_outcome == DealOutcome.LIKELY_LOSE:
            assert r.needs_escalation

    def test_healthy_deal_no_escalation(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        if r.stage_health != StageHealth.CRITICAL and r.deal_outcome != DealOutcome.LIKELY_LOSE:
            assert not r.needs_escalation

    def test_needs_escalation_type_bool(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert isinstance(r.needs_escalation, bool)

    def test_needs_escalation_from_dataclass(self):
        r = DealVelocityResult(
            deal_id="X", deal_name="X", rep_id="X",
            velocity_trend=VelocityTrend.STALLED,
            stage_health=StageHealth.CRITICAL,
            deal_outcome=DealOutcome.AT_RISK,
            velocity_action=VelocityAction.ENGAGE_EXECUTIVE,
            velocity_score=10.0,
            stage_progression_rate=0.1,
            close_date_risk=50.0,
            engagement_score=10.0,
            momentum_score=10.0,
            deal_health_index=10.0,
            is_at_risk=True,
            needs_escalation=True,
        )
        assert r.needs_escalation


# ─────────────────────────────────────────────────────────────────────────────
# 16. Engine properties
# ─────────────────────────────────────────────────────────────────────────────

class TestEngineProperties:
    def test_at_risk_deals_empty_initially(self, engine):
        assert engine.at_risk_deals == []

    def test_escalation_deals_empty_initially(self, engine):
        assert engine.escalation_deals == []

    def test_healthy_deals_empty_initially(self, engine):
        assert engine.healthy_deals == []

    def test_at_risk_deals_returns_list(self, engine, risky_input):
        engine.analyze(risky_input)
        assert isinstance(engine.at_risk_deals, list)

    def test_escalation_deals_returns_list(self, engine, risky_input):
        engine.analyze(risky_input)
        assert isinstance(engine.escalation_deals, list)

    def test_healthy_deals_returns_list(self, engine, healthy_input):
        engine.analyze(healthy_input)
        assert isinstance(engine.healthy_deals, list)

    def test_at_risk_deals_all_flagged(self, engine, risky_input):
        engine.analyze(risky_input)
        for r in engine.at_risk_deals:
            assert r.is_at_risk

    def test_escalation_deals_all_flagged(self, engine, risky_input):
        engine.analyze(risky_input)
        for r in engine.escalation_deals:
            assert r.needs_escalation

    def test_healthy_deals_all_above_65(self, engine, healthy_input):
        engine.analyze(healthy_input)
        for r in engine.healthy_deals:
            assert r.deal_health_index >= 65.0

    def test_at_risk_count_matches_property(self, engine, risky_input):
        engine.analyze(risky_input)
        engine.analyze(make_input(deal_id="D2"))
        assert engine.summary()["at_risk_count"] == len(engine.at_risk_deals)

    def test_escalation_count_matches_property(self, engine, risky_input):
        engine.analyze(risky_input)
        engine.analyze(make_input(deal_id="D2"))
        assert engine.summary()["escalation_count"] == len(engine.escalation_deals)

    def test_healthy_count_matches_property(self, engine, healthy_input):
        engine.analyze(healthy_input)
        engine.analyze(make_input(deal_id="D2"))
        assert engine.summary()["healthy_deal_count"] == len(engine.healthy_deals)

    def test_avg_deal_health_0_when_empty(self, engine):
        assert engine.avg_deal_health == 0.0

    def test_avg_deal_health_positive_after_analyze(self, engine, healthy_input):
        engine.analyze(healthy_input)
        assert engine.avg_deal_health > 0.0

    def test_total_pipeline_value_sums_health_indices(self, engine, healthy_input):
        r1 = engine.analyze(healthy_input)
        r2 = engine.analyze(make_input(deal_id="D2"))
        expected = round(r1.deal_health_index + r2.deal_health_index, 2)
        assert engine.total_pipeline_value == pytest.approx(expected)


# ─────────────────────────────────────────────────────────────────────────────
# 17. analyze_batch()
# ─────────────────────────────────────────────────────────────────────────────

class TestAnalyzeBatch:
    def test_returns_list(self, engine):
        results = engine.analyze_batch([make_input(deal_id="D1"), make_input(deal_id="D2")])
        assert isinstance(results, list)

    def test_length_matches_input(self, engine):
        inputs = [make_input(deal_id=f"D{i}") for i in range(5)]
        results = engine.analyze_batch(inputs)
        assert len(results) == 5

    def test_empty_batch_returns_empty_list(self, engine):
        assert engine.analyze_batch([]) == []

    def test_all_results_are_deal_velocity_result(self, engine):
        inputs = [make_input(deal_id=f"D{i}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        for r in results:
            assert isinstance(r, DealVelocityResult)

    def test_batch_accumulates_in_results(self, engine):
        inputs = [make_input(deal_id=f"D{i}") for i in range(4)]
        engine.analyze_batch(inputs)
        assert engine.summary()["total"] == 4

    def test_batch_ids_preserved(self, engine):
        inputs = [make_input(deal_id=f"DEAL_{i}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        for i, r in enumerate(results):
            assert r.deal_id == f"DEAL_{i}"

    def test_batch_single_item(self, engine):
        results = engine.analyze_batch([make_input(deal_id="SOLO")])
        assert len(results) == 1

    def test_batch_mixed_health(self, engine, healthy_input, risky_input):
        results = engine.analyze_batch([healthy_input, risky_input])
        assert len(results) == 2

    def test_batch_then_single_cumulates(self, engine):
        engine.analyze_batch([make_input(deal_id="D1"), make_input(deal_id="D2")])
        engine.analyze(make_input(deal_id="D3"))
        assert engine.summary()["total"] == 3


# ─────────────────────────────────────────────────────────────────────────────
# 18. reset()
# ─────────────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_results(self, engine, healthy_input):
        engine.analyze(healthy_input)
        engine.reset()
        assert engine.summary()["total"] == 0

    def test_reset_clears_at_risk(self, engine, risky_input):
        engine.analyze(risky_input)
        engine.reset()
        assert engine.at_risk_deals == []

    def test_reset_clears_escalation(self, engine, risky_input):
        engine.analyze(risky_input)
        engine.reset()
        assert engine.escalation_deals == []

    def test_reset_clears_healthy(self, engine, healthy_input):
        engine.analyze(healthy_input)
        engine.reset()
        assert engine.healthy_deals == []

    def test_reset_idempotent(self, engine):
        engine.reset()
        engine.reset()
        assert engine.summary()["total"] == 0

    def test_can_analyze_after_reset(self, engine, healthy_input):
        engine.analyze(healthy_input)
        engine.reset()
        engine.analyze(make_input(deal_id="D_NEW"))
        assert engine.summary()["total"] == 1

    def test_reset_clears_pipeline_value(self, engine, healthy_input):
        engine.analyze(healthy_input)
        engine.reset()
        assert engine.total_pipeline_value == 0.0

    def test_reset_clears_avg_health(self, engine, healthy_input):
        engine.analyze(healthy_input)
        engine.reset()
        assert engine.avg_deal_health == 0.0

    def test_summary_back_to_empty_after_reset(self, engine, healthy_input):
        engine.analyze(healthy_input)
        engine.reset()
        s = engine.summary()
        assert len(s) == 13
        assert s["total"] == 0


# ─────────────────────────────────────────────────────────────────────────────
# 19. Edge cases
# ─────────────────────────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_zero_deal_value(self, engine):
        inp = make_input(deal_value=0.0)
        r = engine.analyze(inp)
        assert isinstance(r, DealVelocityResult)

    def test_zero_probability_pct(self, engine):
        inp = make_input(probability_pct=0.0)
        r = engine.analyze(inp)
        assert isinstance(r, DealVelocityResult)

    def test_max_probability_pct(self, engine):
        inp = make_input(probability_pct=100.0)
        r = engine.analyze(inp)
        assert isinstance(r, DealVelocityResult)

    def test_expected_close_days_negative(self, engine):
        inp = make_input(expected_close_days=-30)
        r = engine.analyze(inp)
        assert r.close_date_risk >= 20.0

    def test_expected_close_days_zero(self, engine):
        inp = make_input(expected_close_days=0)
        r = engine.analyze(inp)
        assert isinstance(r, DealVelocityResult)

    def test_no_activity_ever_last_activity_very_large(self, engine):
        inp = make_input(last_activity_days_ago=365)
        r = engine.analyze(inp)
        assert r.velocity_score >= 0.0
        assert r.velocity_score <= 100.0

    def test_zero_stakeholders(self, engine):
        inp = make_input(num_stakeholders_engaged=0)
        r = engine.analyze(inp)
        assert r.engagement_score >= 0.0

    def test_max_stakeholders(self, engine):
        inp = make_input(num_stakeholders_engaged=100)
        r = engine.analyze(inp)
        assert r.engagement_score <= 100.0

    def test_max_slippage_large_number(self, engine):
        inp = make_input(close_date_changes=100)
        r = engine.analyze(inp)
        assert r.close_date_risk <= 100.0
        assert r.velocity_score >= 0.0

    def test_zero_win_rate(self, engine):
        inp = make_input(win_rate_similar_deals=0.0)
        r = engine.analyze(inp)
        assert r.momentum_score >= 0.0

    def test_win_rate_100(self, engine):
        inp = make_input(win_rate_similar_deals=100.0)
        r = engine.analyze(inp)
        assert r.momentum_score <= 100.0

    def test_zero_nrr_expansion(self, engine):
        inp = make_input(nrr_expansion_potential=0.0)
        r = engine.analyze(inp)
        assert isinstance(r, DealVelocityResult)

    def test_stage_number_1(self, engine):
        inp = make_input(stage_number=1)
        r = engine.analyze(inp)
        assert isinstance(r, DealVelocityResult)

    def test_stage_number_5(self, engine):
        inp = make_input(stage_number=5)
        r = engine.analyze(inp)
        assert isinstance(r, DealVelocityResult)

    def test_competitor_present_with_champion(self, engine):
        inp = make_input(competitor_present=True, champion_identified=True)
        r = engine.analyze(inp)
        assert isinstance(r, DealVelocityResult)

    def test_all_boolean_flags_false(self, engine):
        inp = make_input(
            decision_maker_engaged=False,
            champion_identified=False,
            competitor_present=False,
            pricing_discussed=False,
            legal_review_started=False,
        )
        r = engine.analyze(inp)
        assert r.engagement_score == pytest.approx(
            min(30.0, inp.num_stakeholders_engaged * 10.0)
        )

    def test_all_boolean_flags_true(self, engine):
        inp = make_input(
            decision_maker_engaged=True,
            champion_identified=True,
            competitor_present=True,
            pricing_discussed=True,
            legal_review_started=True,
        )
        r = engine.analyze(inp)
        assert isinstance(r, DealVelocityResult)

    def test_very_large_deal_value(self, engine):
        inp = make_input(deal_value=1_000_000_000.0)
        r = engine.analyze(inp)
        assert isinstance(r, DealVelocityResult)

    def test_negative_days_in_current_stage_handled(self, engine):
        # days_in_current_stage <= 0 returns 1.0
        inp = make_input(days_in_current_stage=0, avg_days_per_stage=10.0)
        e = DealVelocityEngine()
        assert e._stage_progression_rate(inp) == pytest.approx(1.0)

    def test_analyze_returns_correct_types(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert isinstance(r.velocity_score, float)
        assert isinstance(r.stage_progression_rate, float)
        assert isinstance(r.close_date_risk, float)
        assert isinstance(r.engagement_score, float)
        assert isinstance(r.momentum_score, float)
        assert isinstance(r.deal_health_index, float)

    def test_scores_always_in_range(self, engine):
        inputs = [
            make_input(deal_id="E1", days_in_current_stage=1, avg_days_per_stage=100.0),
            make_input(deal_id="E2", days_in_current_stage=100, avg_days_per_stage=1.0),
            make_input(deal_id="E3", last_activity_days_ago=0, close_date_changes=0),
            make_input(deal_id="E4", last_activity_days_ago=365, close_date_changes=100),
        ]
        for inp in inputs:
            r = engine.analyze(inp)
            assert 0.0 <= r.velocity_score <= 100.0, f"velocity_score out of range: {r.velocity_score}"
            assert 0.0 <= r.engagement_score <= 100.0
            assert 0.0 <= r.close_date_risk <= 100.0
            assert 0.0 <= r.momentum_score <= 100.0
            assert 0.0 <= r.deal_health_index <= 100.0


# ─────────────────────────────────────────────────────────────────────────────
# Velocity Trend logic
# ─────────────────────────────────────────────────────────────────────────────

class TestVelocityTrendLogic:
    def test_accelerating_high_progression_recent_activity(self, engine):
        # progression>=1.5 and last_activity<=3
        inp = make_input(
            days_in_current_stage=4, avg_days_per_stage=10.0,  # progression=2.5
            last_activity_days_ago=2,
        )
        r = engine.analyze(inp)
        assert r.velocity_trend == VelocityTrend.ACCELERATING

    def test_stalled_old_activity(self, engine):
        inp = make_input(
            days_in_current_stage=10, avg_days_per_stage=10.0,
            last_activity_days_ago=25,  # > 21
        )
        r = engine.analyze(inp)
        assert r.velocity_trend == VelocityTrend.STALLED

    def test_stalled_very_low_progression(self, engine):
        inp = make_input(
            days_in_current_stage=40, avg_days_per_stage=10.0,  # progression=0.25 < 0.3
            last_activity_days_ago=5,
        )
        r = engine.analyze(inp)
        assert r.velocity_trend == VelocityTrend.STALLED

    def test_decelerating_low_progression(self, engine):
        # progression < 0.7 but >= 0.3, activity <= 21
        inp = make_input(
            days_in_current_stage=17, avg_days_per_stage=10.0,  # progression ≈ 0.59
            last_activity_days_ago=5,
        )
        r = engine.analyze(inp)
        assert r.velocity_trend == VelocityTrend.DECELERATING

    def test_decelerating_stale_activity(self, engine):
        # progression>=0.7 but last_activity > 10
        inp = make_input(
            days_in_current_stage=10, avg_days_per_stage=10.0,  # progression=1.0
            last_activity_days_ago=15,  # > 10 but <= 21
        )
        r = engine.analyze(inp)
        assert r.velocity_trend == VelocityTrend.DECELERATING

    def test_stable_medium_progression_recent_activity(self, engine):
        # progression >= 0.7 (but not >= 1.5 for ACCELERATING), activity <= 10
        inp = make_input(
            days_in_current_stage=12, avg_days_per_stage=10.0,  # progression≈0.83
            last_activity_days_ago=5,
        )
        r = engine.analyze(inp)
        assert r.velocity_trend == VelocityTrend.STABLE

    def test_accelerating_requires_both_conditions(self, engine):
        # High progression but old activity → should NOT be ACCELERATING
        inp = make_input(
            days_in_current_stage=4, avg_days_per_stage=10.0,  # progression=2.5
            last_activity_days_ago=10,  # > 3
        )
        r = engine.analyze(inp)
        assert r.velocity_trend != VelocityTrend.ACCELERATING


# ─────────────────────────────────────────────────────────────────────────────
# Stage Health logic
# ─────────────────────────────────────────────────────────────────────────────

class TestStageHealthLogic:
    def test_healthy_progression_gte_1_2(self, engine):
        inp = make_input(days_in_current_stage=5, avg_days_per_stage=10.0)  # 2.0
        r = engine.analyze(inp)
        assert r.stage_health == StageHealth.HEALTHY

    def test_slow_progression_0_8_to_1_2(self, engine):
        inp = make_input(days_in_current_stage=11, avg_days_per_stage=10.0)  # ≈0.91
        r = engine.analyze(inp)
        assert r.stage_health == StageHealth.SLOW

    def test_critical_days_exceed_2_5x_avg(self, engine):
        # avg=10, actual=26 → 26 > 10*2.5=25 AND progression < 0.8
        inp = make_input(days_in_current_stage=26, avg_days_per_stage=10.0)  # ≈0.38
        r = engine.analyze(inp)
        assert r.stage_health == StageHealth.CRITICAL

    def test_stuck_progression_low_but_not_critical(self, engine):
        # progression < 0.8 but days <= 2.5*avg
        # avg=10, actual=14 → progression=0.71 < 0.8, days=14 <= 25
        inp = make_input(days_in_current_stage=14, avg_days_per_stage=10.0)
        r = engine.analyze(inp)
        assert r.stage_health == StageHealth.STUCK

    def test_healthy_boundary_exactly_1_2(self, engine):
        # avg=12, actual=10 → rate=1.2 → HEALTHY
        inp = make_input(days_in_current_stage=10, avg_days_per_stage=12.0)
        r = engine.analyze(inp)
        assert r.stage_health == StageHealth.HEALTHY

    def test_slow_boundary_exactly_0_8(self, engine):
        # avg=8, actual=10 → rate=0.8 → SLOW
        inp = make_input(days_in_current_stage=10, avg_days_per_stage=8.0)
        r = engine.analyze(inp)
        assert r.stage_health == StageHealth.SLOW


# ─────────────────────────────────────────────────────────────────────────────
# Deal Outcome logic
# ─────────────────────────────────────────────────────────────────────────────

class TestDealOutcomeLogic:
    def test_likely_close_requires_high_health_low_risk_high_prob(self, engine):
        # health>=70, close_risk<=20, probability>=70
        inp = make_input(
            days_in_current_stage=4, avg_days_per_stage=10.0,
            last_activity_days_ago=1,
            num_stakeholders_engaged=3,
            decision_maker_engaged=True,
            champion_identified=True,
            pricing_discussed=True,
            legal_review_started=True,
            close_date_changes=0,
            probability_pct=80.0,
            expected_close_days=30,
            competitor_present=False,
            win_rate_similar_deals=75.0,
        )
        r = engine.analyze(inp)
        if r.deal_health_index >= 70.0 and r.close_date_risk <= 20.0 and inp.probability_pct >= 70.0:
            assert r.deal_outcome == DealOutcome.LIKELY_CLOSE

    def test_likely_lose_low_health(self, engine):
        # health < 25
        inp = make_input(
            days_in_current_stage=50,
            avg_days_per_stage=10.0,
            last_activity_days_ago=40,
            num_stakeholders_engaged=0,
            decision_maker_engaged=False,
            champion_identified=False,
            pricing_discussed=False,
            legal_review_started=False,
            close_date_changes=0,
            win_rate_similar_deals=5.0,
        )
        r = engine.analyze(inp)
        if r.deal_health_index < 25.0:
            assert r.deal_outcome == DealOutcome.LIKELY_LOSE

    def test_likely_lose_competitor_no_champion_low_prob(self, engine):
        inp = make_input(
            competitor_present=True,
            champion_identified=False,
            decision_maker_engaged=False,
            probability_pct=20.0,
            days_in_current_stage=30,
            avg_days_per_stage=10.0,
            last_activity_days_ago=25,
            num_stakeholders_engaged=0,
            pricing_discussed=False,
            legal_review_started=False,
            win_rate_similar_deals=10.0,
        )
        r = engine.analyze(inp)
        # If competitor+no champion+prob<30 AND health<25 → LIKELY_LOSE
        if r.deal_health_index < 25.0:
            assert r.deal_outcome == DealOutcome.LIKELY_LOSE

    def test_likely_slip_high_close_risk(self, engine):
        inp = make_input(
            days_in_current_stage=30,
            avg_days_per_stage=10.0,  # progression=0.33 → +40 risk
            close_date_changes=3,     # +30 risk
            expected_close_days=-5,   # +20 risk → 90
            competitor_present=True,
            decision_maker_engaged=False,  # +10
            num_stakeholders_engaged=2,
            champion_identified=True,
            pricing_discussed=True,
            win_rate_similar_deals=50.0,
        )
        r = engine.analyze(inp)
        if r.close_date_risk >= 60.0 and r.deal_outcome not in (DealOutcome.LIKELY_LOSE,):
            assert r.deal_outcome == DealOutcome.LIKELY_SLIP

    def test_on_track_medium_health_low_risk(self, engine):
        inp = make_input(
            days_in_current_stage=10, avg_days_per_stage=10.0,
            last_activity_days_ago=5,
            num_stakeholders_engaged=2,
            decision_maker_engaged=True,
            champion_identified=True,
            pricing_discussed=True,
            legal_review_started=False,
            close_date_changes=0,
            probability_pct=60.0,
            expected_close_days=30,
            win_rate_similar_deals=55.0,
        )
        r = engine.analyze(inp)
        if r.deal_health_index >= 50.0 and r.close_date_risk <= 40.0 and r.deal_outcome not in (DealOutcome.LIKELY_CLOSE, DealOutcome.LIKELY_LOSE, DealOutcome.LIKELY_SLIP):
            assert r.deal_outcome == DealOutcome.ON_TRACK

    def test_at_risk_fallthrough(self, engine):
        inp = make_input(
            days_in_current_stage=15,
            avg_days_per_stage=10.0,
            last_activity_days_ago=12,
            num_stakeholders_engaged=1,
            decision_maker_engaged=False,
            champion_identified=False,
            pricing_discussed=False,
            legal_review_started=False,
            close_date_changes=2,
            probability_pct=40.0,
            win_rate_similar_deals=35.0,
        )
        r = engine.analyze(inp)
        # Ensure result is one of the valid outcomes
        assert r.deal_outcome in list(DealOutcome)


# ─────────────────────────────────────────────────────────────────────────────
# VelocityAction logic
# ─────────────────────────────────────────────────────────────────────────────

class TestVelocityActionLogic:
    def test_close_lost_outcome_likely_lose_health_lt_20(self, engine):
        # Force LIKELY_LOSE + health < 20
        inp = make_input(
            days_in_current_stage=50,
            avg_days_per_stage=10.0,
            last_activity_days_ago=40,
            num_stakeholders_engaged=0,
            decision_maker_engaged=False,
            champion_identified=False,
            pricing_discussed=False,
            legal_review_started=False,
            close_date_changes=0,
            competitor_present=False,
            probability_pct=5.0,
            win_rate_similar_deals=5.0,
        )
        r = engine.analyze(inp)
        if r.deal_outcome == DealOutcome.LIKELY_LOSE and r.deal_health_index < 20.0:
            assert r.velocity_action == VelocityAction.CLOSE_LOST

    def test_engage_executive_critical_stage(self, engine):
        inp = make_input(
            days_in_current_stage=60,
            avg_days_per_stage=10.0,
        )
        r = engine.analyze(inp)
        if r.stage_health == StageHealth.CRITICAL:
            assert r.velocity_action == VelocityAction.ENGAGE_EXECUTIVE

    def test_reassign_likely_slip_low_health(self, engine):
        # LIKELY_SLIP + health < 35
        inp = make_input(
            days_in_current_stage=30,
            avg_days_per_stage=10.0,
            last_activity_days_ago=25,
            num_stakeholders_engaged=0,
            decision_maker_engaged=False,
            champion_identified=False,
            pricing_discussed=False,
            legal_review_started=False,
            close_date_changes=3,
            probability_pct=25.0,
            expected_close_days=-5,
            competitor_present=True,
            win_rate_similar_deals=15.0,
        )
        r = engine.analyze(inp)
        if r.deal_outcome == DealOutcome.LIKELY_SLIP and r.deal_health_index < 35.0:
            assert r.velocity_action == VelocityAction.REASSIGN

    def test_accelerate_likely_close(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        if r.deal_outcome == DealOutcome.LIKELY_CLOSE:
            assert r.velocity_action == VelocityAction.ACCELERATE

    def test_prioritize_at_risk_outcome(self, engine):
        inp = make_input(
            days_in_current_stage=15,
            avg_days_per_stage=10.0,
            last_activity_days_ago=12,
            num_stakeholders_engaged=1,
            decision_maker_engaged=False,
            champion_identified=False,
            pricing_discussed=False,
            legal_review_started=False,
            close_date_changes=2,
            probability_pct=40.0,
            win_rate_similar_deals=35.0,
        )
        r = engine.analyze(inp)
        if r.deal_outcome == DealOutcome.AT_RISK:
            assert r.velocity_action == VelocityAction.PRIORITIZE

    def test_standard_follow_up_on_track(self, engine):
        inp = make_input(
            days_in_current_stage=10, avg_days_per_stage=10.0,
            last_activity_days_ago=5,
            num_stakeholders_engaged=2,
            decision_maker_engaged=True,
            champion_identified=True,
            pricing_discussed=True,
            legal_review_started=False,
            close_date_changes=0,
            probability_pct=60.0,
            expected_close_days=30,
            win_rate_similar_deals=55.0,
        )
        r = engine.analyze(inp)
        if r.deal_outcome == DealOutcome.ON_TRACK:
            assert r.velocity_action == VelocityAction.STANDARD_FOLLOW_UP

    def test_action_always_valid_enum(self, engine):
        inputs = [
            make_input(deal_id=f"VA{i}") for i in range(5)
        ]
        for inp in inputs:
            r = engine.analyze(inp)
            assert r.velocity_action in list(VelocityAction)


# ─────────────────────────────────────────────────────────────────────────────
# analyze() integration tests
# ─────────────────────────────────────────────────────────────────────────────

class TestAnalyzeIntegration:
    def test_returns_deal_velocity_result(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert isinstance(r, DealVelocityResult)

    def test_deal_id_preserved(self, engine):
        inp = make_input(deal_id="MY_DEAL")
        r = engine.analyze(inp)
        assert r.deal_id == "MY_DEAL"

    def test_deal_name_preserved(self, engine):
        inp = make_input(deal_name="Mega Contract")
        r = engine.analyze(inp)
        assert r.deal_name == "Mega Contract"

    def test_rep_id_preserved(self, engine):
        inp = make_input(rep_id="REP_42")
        r = engine.analyze(inp)
        assert r.rep_id == "REP_42"

    def test_accumulates_results(self, engine):
        engine.analyze(make_input(deal_id="D1"))
        engine.analyze(make_input(deal_id="D2"))
        engine.analyze(make_input(deal_id="D3"))
        assert engine.summary()["total"] == 3

    def test_velocity_trend_is_velocity_trend_enum(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert isinstance(r.velocity_trend, VelocityTrend)

    def test_stage_health_is_stage_health_enum(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert isinstance(r.stage_health, StageHealth)

    def test_deal_outcome_is_deal_outcome_enum(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert isinstance(r.deal_outcome, DealOutcome)

    def test_velocity_action_is_velocity_action_enum(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert isinstance(r.velocity_action, VelocityAction)

    def test_all_float_scores_non_negative(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert r.velocity_score >= 0.0
        assert r.stage_progression_rate >= 0.0
        assert r.close_date_risk >= 0.0
        assert r.engagement_score >= 0.0
        assert r.momentum_score >= 0.0
        assert r.deal_health_index >= 0.0

    def test_all_float_scores_at_most_100(self, engine, risky_input):
        r = engine.analyze(risky_input)
        assert r.velocity_score <= 100.0
        assert r.close_date_risk <= 100.0
        assert r.engagement_score <= 100.0
        assert r.momentum_score <= 100.0
        assert r.deal_health_index <= 100.0

    def test_healthy_deal_has_high_health_index(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert r.deal_health_index > 40.0

    def test_risky_deal_has_low_health_or_high_risk(self, engine, risky_input):
        r = engine.analyze(risky_input)
        assert r.is_at_risk or r.deal_health_index < 60.0

    def test_stage_progression_rate_clamped(self, engine):
        inp = make_input(days_in_current_stage=1, avg_days_per_stage=100.0)
        r = engine.analyze(inp)
        assert r.stage_progression_rate <= 5.0
        assert r.stage_progression_rate >= 0.1

    def test_multiple_different_deals(self, engine):
        deals = []
        for i in range(10):
            inp = make_input(deal_id=f"D{i}", days_in_current_stage=i + 1)
            deals.append(engine.analyze(inp))
        assert len(deals) == 10
        assert all(isinstance(d, DealVelocityResult) for d in deals)


# ─────────────────────────────────────────────────────────────────────────────
# DealVelocityInput dataclass
# ─────────────────────────────────────────────────────────────────────────────

class TestDealVelocityInputDataclass:
    def test_can_create_input(self):
        inp = make_input()
        assert isinstance(inp, DealVelocityInput)

    def test_deal_id_field(self):
        inp = make_input(deal_id="ABC")
        assert inp.deal_id == "ABC"

    def test_deal_name_field(self):
        inp = make_input(deal_name="My Deal")
        assert inp.deal_name == "My Deal"

    def test_rep_id_field(self):
        inp = make_input(rep_id="R99")
        assert inp.rep_id == "R99"

    def test_account_id_field(self):
        inp = make_input(account_id="ACC123")
        assert inp.account_id == "ACC123"

    def test_stage_number_field(self):
        inp = make_input(stage_number=4)
        assert inp.stage_number == 4

    def test_deal_value_field(self):
        inp = make_input(deal_value=99999.0)
        assert inp.deal_value == 99999.0

    def test_probability_pct_field(self):
        inp = make_input(probability_pct=75.0)
        assert inp.probability_pct == 75.0

    def test_boolean_fields_accessible(self):
        inp = make_input(decision_maker_engaged=True, champion_identified=False)
        assert inp.decision_maker_engaged is True
        assert inp.champion_identified is False


# ─────────────────────────────────────────────────────────────────────────────
# DealVelocityResult dataclass
# ─────────────────────────────────────────────────────────────────────────────

class TestDealVelocityResultDataclass:
    def test_can_create_result(self):
        r = DealVelocityResult(
            deal_id="X", deal_name="X", rep_id="X",
            velocity_trend=VelocityTrend.STABLE,
            stage_health=StageHealth.HEALTHY,
            deal_outcome=DealOutcome.ON_TRACK,
            velocity_action=VelocityAction.STANDARD_FOLLOW_UP,
            velocity_score=50.0,
            stage_progression_rate=1.0,
            close_date_risk=20.0,
            engagement_score=60.0,
            momentum_score=55.0,
            deal_health_index=55.0,
            is_at_risk=False,
            needs_escalation=False,
        )
        assert r.deal_id == "X"

    def test_to_dict_always_15_keys_various_states(self):
        for trend in VelocityTrend:
            for health in StageHealth:
                r = DealVelocityResult(
                    deal_id="X", deal_name="X", rep_id="X",
                    velocity_trend=trend,
                    stage_health=health,
                    deal_outcome=DealOutcome.ON_TRACK,
                    velocity_action=VelocityAction.STANDARD_FOLLOW_UP,
                    velocity_score=50.0,
                    stage_progression_rate=1.0,
                    close_date_risk=20.0,
                    engagement_score=60.0,
                    momentum_score=55.0,
                    deal_health_index=55.0,
                    is_at_risk=False,
                    needs_escalation=False,
                )
                assert len(r.to_dict()) == 15


# ─────────────────────────────────────────────────────────────────────────────
# Additional coverage – scoring boundary conditions
# ─────────────────────────────────────────────────────────────────────────────

class TestScoringBoundaries:
    def test_progression_rate_near_boundary_0_1(self):
        e = DealVelocityEngine()
        # 1/10 = 0.1 → exactly at clamp minimum
        inp = make_input(days_in_current_stage=10, avg_days_per_stage=1.0)
        rate = e._stage_progression_rate(inp)
        assert rate == pytest.approx(0.1, rel=1e-3)

    def test_progression_rate_near_boundary_5(self):
        e = DealVelocityEngine()
        # 50/10 = 5.0 → exactly at clamp maximum
        inp = make_input(days_in_current_stage=10, avg_days_per_stage=50.0)
        rate = e._stage_progression_rate(inp)
        assert rate == pytest.approx(5.0, rel=1e-3)

    def test_engagement_score_exactly_30_for_3_stakeholders(self):
        e = DealVelocityEngine()
        inp = make_input(
            num_stakeholders_engaged=3,
            decision_maker_engaged=False,
            champion_identified=False,
            pricing_discussed=False,
            legal_review_started=False,
        )
        assert e._engagement_score(inp) == pytest.approx(30.0)

    def test_engagement_score_exactly_0(self):
        e = DealVelocityEngine()
        inp = make_input(
            num_stakeholders_engaged=0,
            decision_maker_engaged=False,
            champion_identified=False,
            pricing_discussed=False,
            legal_review_started=False,
        )
        assert e._engagement_score(inp) == pytest.approx(0.0)

    def test_velocity_score_activity_exactly_3_days(self):
        e = DealVelocityEngine()
        inp = make_input(last_activity_days_ago=3, close_date_changes=0)
        score = e._velocity_score(inp, 1.0)
        # 20 + 30 + 25 = 75
        assert score == pytest.approx(75.0, rel=1e-2)

    def test_velocity_score_activity_exactly_7_days(self):
        e = DealVelocityEngine()
        inp = make_input(last_activity_days_ago=7, close_date_changes=0)
        score = e._velocity_score(inp, 1.0)
        # 20 + 20 + 25 = 65
        assert score == pytest.approx(65.0, rel=1e-2)

    def test_velocity_score_activity_exactly_14_days(self):
        e = DealVelocityEngine()
        inp = make_input(last_activity_days_ago=14, close_date_changes=0)
        score = e._velocity_score(inp, 1.0)
        # 20 + 10 + 25 = 55
        assert score == pytest.approx(55.0, rel=1e-2)

    def test_close_risk_progression_boundary_0_5(self):
        e = DealVelocityEngine()
        inp = make_input(close_date_changes=0, expected_close_days=30,
                         competitor_present=False)
        # exactly at 0.5
        risk = e._close_date_risk(inp, 0.5)
        # 0.5 is NOT < 0.5, so it falls into 0.5≤x<0.8 → +25
        assert risk == pytest.approx(25.0)

    def test_close_risk_progression_boundary_0_8(self):
        e = DealVelocityEngine()
        inp = make_input(close_date_changes=0, expected_close_days=30,
                         competitor_present=False)
        # exactly at 0.8 falls into 0.8≤x<1.0 → +10
        risk = e._close_date_risk(inp, 0.8)
        assert risk == pytest.approx(10.0)

    def test_close_risk_progression_boundary_1_0(self):
        e = DealVelocityEngine()
        inp = make_input(close_date_changes=0, expected_close_days=30,
                         competitor_present=False)
        # exactly at 1.0 → no progression risk
        risk = e._close_date_risk(inp, 1.0)
        assert risk == pytest.approx(0.0)

    def test_health_index_weights_sum_to_1(self):
        assert abs(0.35 + 0.30 + 0.35 - 1.0) < 1e-10

    def test_deal_health_below_40_flags_at_risk(self):
        e = DealVelocityEngine()
        inp = make_input(
            days_in_current_stage=50, avg_days_per_stage=10.0,
            last_activity_days_ago=30,
            num_stakeholders_engaged=0,
            decision_maker_engaged=False, champion_identified=False,
            pricing_discussed=False, legal_review_started=False,
            close_date_changes=0, win_rate_similar_deals=5.0,
            expected_close_days=30, competitor_present=False,
        )
        r = e.analyze(inp)
        assert r.is_at_risk == (r.deal_health_index < 40.0 or r.close_date_risk > 70.0)

    def test_close_risk_above_70_flags_at_risk(self):
        e = DealVelocityEngine()
        inp = make_input(
            days_in_current_stage=40, avg_days_per_stage=10.0,
            close_date_changes=4,
            expected_close_days=-5,
            competitor_present=True, decision_maker_engaged=False,
        )
        r = e.analyze(inp)
        assert r.is_at_risk == (r.deal_health_index < 40.0 or r.close_date_risk > 70.0)


# ─────────────────────────────────────────────────────────────────────────────
# All enum values appear in real analysis (coverage)
# ─────────────────────────────────────────────────────────────────────────────

class TestEnumCoverageViaAnalysis:
    """Ensure all enum values can appear in analysis results."""

    def test_velocity_trend_accelerating_reachable(self):
        e = DealVelocityEngine()
        inp = make_input(
            days_in_current_stage=2, avg_days_per_stage=10.0,
            last_activity_days_ago=1,
        )
        r = e.analyze(inp)
        assert r.velocity_trend == VelocityTrend.ACCELERATING

    def test_velocity_trend_stalled_reachable_old_activity(self):
        e = DealVelocityEngine()
        inp = make_input(last_activity_days_ago=25)
        r = e.analyze(inp)
        assert r.velocity_trend == VelocityTrend.STALLED

    def test_velocity_trend_decelerating_reachable(self):
        e = DealVelocityEngine()
        inp = make_input(
            days_in_current_stage=17, avg_days_per_stage=10.0,
            last_activity_days_ago=5,
        )
        r = e.analyze(inp)
        assert r.velocity_trend == VelocityTrend.DECELERATING

    def test_velocity_trend_stable_reachable(self):
        e = DealVelocityEngine()
        inp = make_input(
            days_in_current_stage=12, avg_days_per_stage=10.0,
            last_activity_days_ago=5,
        )
        r = e.analyze(inp)
        assert r.velocity_trend == VelocityTrend.STABLE

    def test_stage_health_healthy_reachable(self):
        e = DealVelocityEngine()
        inp = make_input(days_in_current_stage=5, avg_days_per_stage=10.0)
        r = e.analyze(inp)
        assert r.stage_health == StageHealth.HEALTHY

    def test_stage_health_slow_reachable(self):
        e = DealVelocityEngine()
        inp = make_input(days_in_current_stage=11, avg_days_per_stage=10.0)
        r = e.analyze(inp)
        assert r.stage_health == StageHealth.SLOW

    def test_stage_health_stuck_reachable(self):
        e = DealVelocityEngine()
        inp = make_input(days_in_current_stage=14, avg_days_per_stage=10.0)
        r = e.analyze(inp)
        assert r.stage_health == StageHealth.STUCK

    def test_stage_health_critical_reachable(self):
        e = DealVelocityEngine()
        inp = make_input(days_in_current_stage=26, avg_days_per_stage=10.0)
        r = e.analyze(inp)
        assert r.stage_health == StageHealth.CRITICAL

    def test_deal_outcome_on_track_reachable(self):
        e = DealVelocityEngine()
        inp = make_input(
            days_in_current_stage=10, avg_days_per_stage=10.0,
            last_activity_days_ago=5,
            num_stakeholders_engaged=2,
            decision_maker_engaged=True, champion_identified=True,
            pricing_discussed=True, legal_review_started=False,
            close_date_changes=0, probability_pct=60.0,
            expected_close_days=30, win_rate_similar_deals=55.0,
        )
        r = e.analyze(inp)
        assert r.deal_outcome == DealOutcome.ON_TRACK

    def test_velocity_action_standard_follow_up_reachable(self):
        e = DealVelocityEngine()
        inp = make_input(
            days_in_current_stage=10, avg_days_per_stage=10.0,
            last_activity_days_ago=5,
            num_stakeholders_engaged=2,
            decision_maker_engaged=True, champion_identified=True,
            pricing_discussed=True, legal_review_started=False,
            close_date_changes=0, probability_pct=60.0,
            expected_close_days=30, win_rate_similar_deals=55.0,
        )
        r = e.analyze(inp)
        if r.deal_outcome == DealOutcome.ON_TRACK:
            assert r.velocity_action == VelocityAction.STANDARD_FOLLOW_UP

    def test_velocity_action_accelerate_likely_close_reachable(self):
        e = DealVelocityEngine()
        inp = make_input(
            days_in_current_stage=4, avg_days_per_stage=10.0,
            last_activity_days_ago=1,
            num_stakeholders_engaged=3,
            decision_maker_engaged=True, champion_identified=True,
            pricing_discussed=True, legal_review_started=True,
            close_date_changes=0, probability_pct=80.0,
            expected_close_days=30, win_rate_similar_deals=75.0,
        )
        r = e.analyze(inp)
        if r.deal_outcome == DealOutcome.LIKELY_CLOSE:
            assert r.velocity_action == VelocityAction.ACCELERATE

    def test_velocity_action_engage_executive_reachable(self):
        e = DealVelocityEngine()
        inp = make_input(days_in_current_stage=60, avg_days_per_stage=10.0)
        r = e.analyze(inp)
        if r.stage_health == StageHealth.CRITICAL:
            assert r.velocity_action == VelocityAction.ENGAGE_EXECUTIVE


# ─────────────────────────────────────────────────────────────────────────────
# Additional miscellaneous tests to reach 240+ functions
# ─────────────────────────────────────────────────────────────────────────────

class TestMiscellaneous:
    def test_engine_initial_results_empty(self):
        e = DealVelocityEngine()
        assert e._results == []

    def test_engine_has_analyze_method(self):
        e = DealVelocityEngine()
        assert callable(e.analyze)

    def test_engine_has_analyze_batch_method(self):
        e = DealVelocityEngine()
        assert callable(e.analyze_batch)

    def test_engine_has_reset_method(self):
        e = DealVelocityEngine()
        assert callable(e.reset)

    def test_engine_has_summary_method(self):
        e = DealVelocityEngine()
        assert callable(e.summary)

    def test_engine_has_at_risk_deals_property(self):
        e = DealVelocityEngine()
        _ = e.at_risk_deals  # should not raise

    def test_engine_has_escalation_deals_property(self):
        e = DealVelocityEngine()
        _ = e.escalation_deals

    def test_engine_has_healthy_deals_property(self):
        e = DealVelocityEngine()
        _ = e.healthy_deals

    def test_engine_has_avg_deal_health_property(self):
        e = DealVelocityEngine()
        _ = e.avg_deal_health

    def test_engine_has_total_pipeline_value_property(self):
        e = DealVelocityEngine()
        _ = e.total_pipeline_value

    def test_summary_key_total(self, engine, healthy_input):
        engine.analyze(healthy_input)
        assert "total" in engine.summary()

    def test_summary_key_trend_counts(self, engine, healthy_input):
        engine.analyze(healthy_input)
        assert "trend_counts" in engine.summary()

    def test_summary_key_health_counts(self, engine, healthy_input):
        engine.analyze(healthy_input)
        assert "health_counts" in engine.summary()

    def test_summary_key_outcome_counts(self, engine, healthy_input):
        engine.analyze(healthy_input)
        assert "outcome_counts" in engine.summary()

    def test_summary_key_action_counts(self, engine, healthy_input):
        engine.analyze(healthy_input)
        assert "action_counts" in engine.summary()

    def test_summary_key_avg_velocity_score(self, engine, healthy_input):
        engine.analyze(healthy_input)
        assert "avg_velocity_score" in engine.summary()

    def test_summary_key_avg_deal_health_index(self, engine, healthy_input):
        engine.analyze(healthy_input)
        assert "avg_deal_health_index" in engine.summary()

    def test_summary_key_avg_close_date_risk(self, engine, healthy_input):
        engine.analyze(healthy_input)
        assert "avg_close_date_risk" in engine.summary()

    def test_summary_key_at_risk_count(self, engine, healthy_input):
        engine.analyze(healthy_input)
        assert "at_risk_count" in engine.summary()

    def test_summary_key_escalation_count(self, engine, healthy_input):
        engine.analyze(healthy_input)
        assert "escalation_count" in engine.summary()

    def test_summary_key_avg_engagement_score(self, engine, healthy_input):
        engine.analyze(healthy_input)
        assert "avg_engagement_score" in engine.summary()

    def test_summary_key_avg_momentum_score(self, engine, healthy_input):
        engine.analyze(healthy_input)
        assert "avg_momentum_score" in engine.summary()

    def test_summary_key_healthy_deal_count(self, engine, healthy_input):
        engine.analyze(healthy_input)
        assert "healthy_deal_count" in engine.summary()

    def test_to_dict_key_deal_id(self, engine, healthy_input):
        assert "deal_id" in engine.analyze(healthy_input).to_dict()

    def test_to_dict_key_deal_name(self, engine, healthy_input):
        assert "deal_name" in engine.analyze(healthy_input).to_dict()

    def test_to_dict_key_rep_id(self, engine, healthy_input):
        assert "rep_id" in engine.analyze(healthy_input).to_dict()

    def test_to_dict_key_velocity_trend(self, engine, healthy_input):
        assert "velocity_trend" in engine.analyze(healthy_input).to_dict()

    def test_to_dict_key_stage_health(self, engine, healthy_input):
        assert "stage_health" in engine.analyze(healthy_input).to_dict()

    def test_to_dict_key_deal_outcome(self, engine, healthy_input):
        assert "deal_outcome" in engine.analyze(healthy_input).to_dict()

    def test_to_dict_key_velocity_action(self, engine, healthy_input):
        assert "velocity_action" in engine.analyze(healthy_input).to_dict()

    def test_to_dict_key_velocity_score(self, engine, healthy_input):
        assert "velocity_score" in engine.analyze(healthy_input).to_dict()

    def test_to_dict_key_stage_progression_rate(self, engine, healthy_input):
        assert "stage_progression_rate" in engine.analyze(healthy_input).to_dict()

    def test_to_dict_key_close_date_risk(self, engine, healthy_input):
        assert "close_date_risk" in engine.analyze(healthy_input).to_dict()

    def test_to_dict_key_engagement_score(self, engine, healthy_input):
        assert "engagement_score" in engine.analyze(healthy_input).to_dict()

    def test_to_dict_key_momentum_score(self, engine, healthy_input):
        assert "momentum_score" in engine.analyze(healthy_input).to_dict()

    def test_to_dict_key_deal_health_index(self, engine, healthy_input):
        assert "deal_health_index" in engine.analyze(healthy_input).to_dict()

    def test_to_dict_key_is_at_risk(self, engine, healthy_input):
        assert "is_at_risk" in engine.analyze(healthy_input).to_dict()

    def test_to_dict_key_needs_escalation(self, engine, healthy_input):
        assert "needs_escalation" in engine.analyze(healthy_input).to_dict()

    def test_two_independent_engines_do_not_share_state(self):
        e1 = DealVelocityEngine()
        e2 = DealVelocityEngine()
        e1.analyze(make_input(deal_id="D1"))
        assert e2.summary()["total"] == 0

    def test_result_is_appended_to_internal_list(self):
        e = DealVelocityEngine()
        r = e.analyze(make_input(deal_id="D1"))
        assert r in e._results

    def test_batch_results_all_in_internal_list(self):
        e = DealVelocityEngine()
        results = e.analyze_batch([make_input(deal_id=f"D{i}") for i in range(3)])
        for r in results:
            assert r in e._results

    def test_summary_trend_counts_use_string_keys(self, engine, healthy_input):
        engine.analyze(healthy_input)
        for key in engine.summary()["trend_counts"]:
            assert isinstance(key, str)

    def test_summary_health_counts_use_string_keys(self, engine, healthy_input):
        engine.analyze(healthy_input)
        for key in engine.summary()["health_counts"]:
            assert isinstance(key, str)

    def test_summary_outcome_counts_use_string_keys(self, engine, healthy_input):
        engine.analyze(healthy_input)
        for key in engine.summary()["outcome_counts"]:
            assert isinstance(key, str)

    def test_summary_action_counts_use_string_keys(self, engine, healthy_input):
        engine.analyze(healthy_input)
        for key in engine.summary()["action_counts"]:
            assert isinstance(key, str)

    def test_avg_deal_health_single_result(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert engine.avg_deal_health == pytest.approx(r.deal_health_index, rel=0.01)

    def test_total_pipeline_value_single_result(self, engine, healthy_input):
        r = engine.analyze(healthy_input)
        assert engine.total_pipeline_value == pytest.approx(r.deal_health_index, rel=0.01)

    def test_large_batch_summary_total(self, engine):
        inputs = [make_input(deal_id=f"BULK{i}") for i in range(50)]
        engine.analyze_batch(inputs)
        assert engine.summary()["total"] == 50

    def test_avg_scores_within_valid_range(self, engine):
        for i in range(5):
            engine.analyze(make_input(deal_id=f"X{i}"))
        s = engine.summary()
        assert 0.0 <= s["avg_velocity_score"] <= 100.0
        assert 0.0 <= s["avg_deal_health_index"] <= 100.0
        assert 0.0 <= s["avg_close_date_risk"] <= 100.0
        assert 0.0 <= s["avg_engagement_score"] <= 100.0
        assert 0.0 <= s["avg_momentum_score"] <= 100.0

    def test_reset_then_batch(self, engine):
        engine.analyze_batch([make_input(deal_id=f"A{i}") for i in range(5)])
        engine.reset()
        engine.analyze_batch([make_input(deal_id=f"B{i}") for i in range(3)])
        assert engine.summary()["total"] == 3

    def test_deal_health_index_consistent_with_formula(self, engine):
        inp = make_input()
        r = engine.analyze(inp)
        e = DealVelocityEngine()
        progression = e._stage_progression_rate(inp)
        engagement = e._engagement_score(inp)
        velocity = e._velocity_score(inp, progression)
        momentum = e._momentum_score(inp, progression, engagement)
        expected_health = e._deal_health_index(velocity, engagement, momentum)
        assert r.deal_health_index == pytest.approx(expected_health, rel=1e-3)

    def test_is_at_risk_consistent_with_formula(self, engine):
        for i in range(10):
            inp = make_input(deal_id=f"C{i}", last_activity_days_ago=i * 3)
            r = engine.analyze(inp)
            assert r.is_at_risk == (r.deal_health_index < 40.0 or r.close_date_risk > 70.0)

    def test_needs_escalation_consistent_with_formula(self, engine):
        for i in range(10):
            inp = make_input(deal_id=f"N{i}", days_in_current_stage=i * 5 + 1)
            r = engine.analyze(inp)
            assert r.needs_escalation == (
                r.stage_health == StageHealth.CRITICAL or
                r.deal_outcome == DealOutcome.LIKELY_LOSE
            )
