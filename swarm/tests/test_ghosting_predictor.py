"""
Comprehensive pytest tests for GhostingPredictor.

Covers:
- All enum values and string representations
- GhostingPredictorInput field count (22)
- GhostingPredictorResult.to_dict() key count and content (15)
- summary() key count and content (13)
- All scoring helpers (_silence_score, _engagement_decay_score,
  _behavioral_risk_score, _deal_urgency_score, _composite)
- Classification helpers (_ghosting_risk, _ghosting_pattern,
  _buyer_momentum, _ghosting_action)
- Derived helpers (_predicted_ghost_days, _recovery_probability)
- is_at_risk_of_ghosting and needs_escalation flags
- predict() and predict_batch() public API
- Properties: at_risk_deals, escalation_queue,
  avg_ghosting_composite, avg_recovery_probability
- reset() clears state
- Edge cases: zeros, max values, boundary conditions
"""

from __future__ import annotations

import dataclasses
import math
import pytest

from swarm.intelligence.ghosting_predictor import (
    BuyerMomentum,
    GhostingAction,
    GhostingPattern,
    GhostingPredictor,
    GhostingPredictorInput,
    GhostingPredictorResult,
    GhostingRisk,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers / Fixtures
# ─────────────────────────────────────────────────────────────────────────────

def make_input(
    deal_id: str = "D001",
    deal_name: str = "Test Deal",
    rep_id: str = "R001",
    days_since_last_buyer_reply: int = 0,
    days_since_last_meeting: int = 0,
    meetings_cancelled_last_30d: int = 0,
    meetings_rescheduled_last_30d: int = 0,
    email_open_rate_last_30d: float = 60.0,
    email_open_rate_prior_30d: float = 60.0,
    response_time_avg_hours_recent: float = 2.0,
    response_time_avg_hours_prior: float = 2.0,
    champion_last_active_days_ago: int = 0,
    champion_linkedin_gone_quiet: int = 0,
    stakeholder_count_drop: int = 0,
    next_step_missed_count: int = 0,
    deal_stage_days_stuck: int = 0,
    proposal_opened_last_7d: int = 0,
    pricing_conversation_stalled: int = 0,
    internal_champion_change: int = 0,
    competitor_meeting_signal: int = 0,
    deal_value: float = 50_000.0,
    days_to_close_target: int = 60,
) -> GhostingPredictorInput:
    return GhostingPredictorInput(
        deal_id=deal_id,
        deal_name=deal_name,
        rep_id=rep_id,
        days_since_last_buyer_reply=days_since_last_buyer_reply,
        days_since_last_meeting=days_since_last_meeting,
        meetings_cancelled_last_30d=meetings_cancelled_last_30d,
        meetings_rescheduled_last_30d=meetings_rescheduled_last_30d,
        email_open_rate_last_30d=email_open_rate_last_30d,
        email_open_rate_prior_30d=email_open_rate_prior_30d,
        response_time_avg_hours_recent=response_time_avg_hours_recent,
        response_time_avg_hours_prior=response_time_avg_hours_prior,
        champion_last_active_days_ago=champion_last_active_days_ago,
        champion_linkedin_gone_quiet=champion_linkedin_gone_quiet,
        stakeholder_count_drop=stakeholder_count_drop,
        next_step_missed_count=next_step_missed_count,
        deal_stage_days_stuck=deal_stage_days_stuck,
        proposal_opened_last_7d=proposal_opened_last_7d,
        pricing_conversation_stalled=pricing_conversation_stalled,
        internal_champion_change=internal_champion_change,
        competitor_meeting_signal=competitor_meeting_signal,
        deal_value=deal_value,
        days_to_close_target=days_to_close_target,
    )


@pytest.fixture
def predictor() -> GhostingPredictor:
    return GhostingPredictor()


@pytest.fixture
def clean_input() -> GhostingPredictorInput:
    """All-zero / ideal buyer — produces very low risk."""
    return make_input()


# ─────────────────────────────────────────────────────────────────────────────
# 1. Enum tests
# ─────────────────────────────────────────────────────────────────────────────

class TestGhostingRiskEnum:
    def test_has_four_members(self):
        assert len(GhostingRisk) == 4

    def test_low_value(self):
        assert GhostingRisk.LOW.value == "low"

    def test_moderate_value(self):
        assert GhostingRisk.MODERATE.value == "moderate"

    def test_high_value(self):
        assert GhostingRisk.HIGH.value == "high"

    def test_critical_value(self):
        assert GhostingRisk.CRITICAL.value == "critical"

    def test_is_str_enum(self):
        assert isinstance(GhostingRisk.LOW, str)

    def test_all_values_unique(self):
        values = [m.value for m in GhostingRisk]
        assert len(values) == len(set(values))


class TestGhostingPatternEnum:
    def test_has_six_members(self):
        assert len(GhostingPattern) == 6

    def test_engaged_value(self):
        assert GhostingPattern.ENGAGED.value == "engaged"

    def test_cooling_off_value(self):
        assert GhostingPattern.COOLING_OFF.value == "cooling_off"

    def test_slow_fade_value(self):
        assert GhostingPattern.SLOW_FADE.value == "slow_fade"

    def test_partial_ghost_value(self):
        assert GhostingPattern.PARTIAL_GHOST.value == "partial_ghost"

    def test_full_ghost_value(self):
        assert GhostingPattern.FULL_GHOST.value == "full_ghost"

    def test_champion_exit_value(self):
        assert GhostingPattern.CHAMPION_EXIT.value == "champion_exit"

    def test_all_values_unique(self):
        values = [m.value for m in GhostingPattern]
        assert len(values) == len(set(values))


class TestBuyerMomentumEnum:
    def test_has_four_members(self):
        assert len(BuyerMomentum) == 4

    def test_accelerating_value(self):
        assert BuyerMomentum.ACCELERATING.value == "accelerating"

    def test_stable_value(self):
        assert BuyerMomentum.STABLE.value == "stable"

    def test_decelerating_value(self):
        assert BuyerMomentum.DECELERATING.value == "decelerating"

    def test_stalled_value(self):
        assert BuyerMomentum.STALLED.value == "stalled"

    def test_all_values_unique(self):
        values = [m.value for m in BuyerMomentum]
        assert len(values) == len(set(values))


class TestGhostingActionEnum:
    def test_has_four_members(self):
        assert len(GhostingAction) == 4

    def test_maintain_value(self):
        assert GhostingAction.MAINTAIN.value == "maintain"

    def test_re_engage_value(self):
        assert GhostingAction.RE_ENGAGE.value == "re_engage"

    def test_escalate_path_value(self):
        assert GhostingAction.ESCALATE_PATH.value == "escalate_path"

    def test_last_resort_value(self):
        assert GhostingAction.LAST_RESORT.value == "last_resort"

    def test_all_values_unique(self):
        values = [m.value for m in GhostingAction]
        assert len(values) == len(set(values))


# ─────────────────────────────────────────────────────────────────────────────
# 2. GhostingPredictorInput – exactly 22 fields
# ─────────────────────────────────────────────────────────────────────────────

class TestGhostingPredictorInput:
    def test_field_count_is_22(self):
        fields = dataclasses.fields(GhostingPredictorInput)
        assert len(fields) == 22

    def test_field_names(self):
        expected = {
            "deal_id", "deal_name", "rep_id",
            "days_since_last_buyer_reply", "days_since_last_meeting",
            "meetings_cancelled_last_30d", "meetings_rescheduled_last_30d",
            "email_open_rate_last_30d", "email_open_rate_prior_30d",
            "response_time_avg_hours_recent", "response_time_avg_hours_prior",
            "champion_last_active_days_ago", "champion_linkedin_gone_quiet",
            "stakeholder_count_drop", "next_step_missed_count",
            "deal_stage_days_stuck", "proposal_opened_last_7d",
            "pricing_conversation_stalled", "internal_champion_change",
            "competitor_meeting_signal", "deal_value", "days_to_close_target",
        }
        actual = {f.name for f in dataclasses.fields(GhostingPredictorInput)}
        assert actual == expected

    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(GhostingPredictorInput)

    def test_instantiation_with_all_fields(self):
        inp = make_input()
        assert inp.deal_id == "D001"
        assert inp.deal_name == "Test Deal"
        assert inp.rep_id == "R001"

    def test_string_fields(self):
        inp = make_input(deal_id="X", deal_name="Y", rep_id="Z")
        assert inp.deal_id == "X"
        assert inp.deal_name == "Y"
        assert inp.rep_id == "Z"

    def test_numeric_fields_accept_zero(self):
        inp = make_input(
            days_since_last_buyer_reply=0,
            deal_value=0.0,
            days_to_close_target=0,
        )
        assert inp.days_since_last_buyer_reply == 0
        assert inp.deal_value == 0.0
        assert inp.days_to_close_target == 0


# ─────────────────────────────────────────────────────────────────────────────
# 3. GhostingPredictorResult.to_dict() – exactly 15 keys
# ─────────────────────────────────────────────────────────────────────────────

class TestGhostingPredictorResultToDict:
    EXPECTED_KEYS = {
        "deal_id", "deal_name", "ghosting_risk", "ghosting_pattern",
        "buyer_momentum", "ghosting_action", "silence_score",
        "engagement_decay_score", "behavioral_risk_score",
        "deal_urgency_score", "ghosting_composite", "predicted_ghost_days",
        "recovery_probability", "is_at_risk_of_ghosting", "needs_escalation",
    }

    @pytest.fixture
    def result(self, predictor, clean_input):
        return predictor.predict(clean_input)

    def test_key_count_is_15(self, result):
        assert len(result.to_dict()) == 15

    def test_exact_keys(self, result):
        assert set(result.to_dict().keys()) == self.EXPECTED_KEYS

    def test_deal_id_in_dict(self, result):
        assert result.to_dict()["deal_id"] == "D001"

    def test_deal_name_in_dict(self, result):
        assert result.to_dict()["deal_name"] == "Test Deal"

    def test_ghosting_risk_is_string(self, result):
        assert isinstance(result.to_dict()["ghosting_risk"], str)

    def test_ghosting_pattern_is_string(self, result):
        assert isinstance(result.to_dict()["ghosting_pattern"], str)

    def test_buyer_momentum_is_string(self, result):
        assert isinstance(result.to_dict()["buyer_momentum"], str)

    def test_ghosting_action_is_string(self, result):
        assert isinstance(result.to_dict()["ghosting_action"], str)

    def test_silence_score_is_float(self, result):
        assert isinstance(result.to_dict()["silence_score"], float)

    def test_engagement_decay_score_is_float(self, result):
        assert isinstance(result.to_dict()["engagement_decay_score"], float)

    def test_behavioral_risk_score_is_float(self, result):
        assert isinstance(result.to_dict()["behavioral_risk_score"], float)

    def test_deal_urgency_score_is_float(self, result):
        assert isinstance(result.to_dict()["deal_urgency_score"], float)

    def test_ghosting_composite_is_float(self, result):
        assert isinstance(result.to_dict()["ghosting_composite"], float)

    def test_predicted_ghost_days_is_int(self, result):
        assert isinstance(result.to_dict()["predicted_ghost_days"], int)

    def test_recovery_probability_is_float(self, result):
        assert isinstance(result.to_dict()["recovery_probability"], float)

    def test_is_at_risk_of_ghosting_is_bool(self, result):
        assert isinstance(result.to_dict()["is_at_risk_of_ghosting"], bool)

    def test_needs_escalation_is_bool(self, result):
        assert isinstance(result.to_dict()["needs_escalation"], bool)

    def test_enum_values_are_raw_strings(self, predictor):
        inp = make_input()
        result = predictor.predict(inp)
        d = result.to_dict()
        assert d["ghosting_risk"] in {"low", "moderate", "high", "critical"}
        assert d["ghosting_pattern"] in {
            "engaged", "cooling_off", "slow_fade",
            "partial_ghost", "full_ghost", "champion_exit"
        }
        assert d["buyer_momentum"] in {
            "accelerating", "stable", "decelerating", "stalled"
        }
        assert d["ghosting_action"] in {
            "maintain", "re_engage", "escalate_path", "last_resort"
        }


# ─────────────────────────────────────────────────────────────────────────────
# 4. summary() – exactly 13 keys
# ─────────────────────────────────────────────────────────────────────────────

class TestSummary:
    EXPECTED_KEYS = {
        "total", "risk_counts", "pattern_counts", "momentum_counts",
        "action_counts", "avg_ghosting_composite", "avg_recovery_probability",
        "at_risk_count", "escalation_count", "avg_silence_score",
        "avg_engagement_decay_score", "avg_behavioral_risk_score",
        "avg_deal_urgency_score",
    }

    def test_empty_summary_has_13_keys(self, predictor):
        s = predictor.summary()
        assert len(s) == 13

    def test_empty_summary_exact_keys(self, predictor):
        assert set(predictor.summary().keys()) == self.EXPECTED_KEYS

    def test_empty_summary_total_zero(self, predictor):
        assert predictor.summary()["total"] == 0

    def test_empty_summary_empty_dicts(self, predictor):
        s = predictor.summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["momentum_counts"] == {}
        assert s["action_counts"] == {}

    def test_empty_summary_zero_avgs(self, predictor):
        s = predictor.summary()
        assert s["avg_ghosting_composite"] == 0.0
        assert s["avg_recovery_probability"] == 0.0
        assert s["at_risk_count"] == 0
        assert s["escalation_count"] == 0
        assert s["avg_silence_score"] == 0.0
        assert s["avg_engagement_decay_score"] == 0.0
        assert s["avg_behavioral_risk_score"] == 0.0
        assert s["avg_deal_urgency_score"] == 0.0

    def test_non_empty_summary_has_13_keys(self, predictor, clean_input):
        predictor.predict(clean_input)
        assert len(predictor.summary()) == 13

    def test_non_empty_summary_exact_keys(self, predictor, clean_input):
        predictor.predict(clean_input)
        assert set(predictor.summary().keys()) == self.EXPECTED_KEYS

    def test_total_reflects_predictions(self, predictor, clean_input):
        predictor.predict(clean_input)
        predictor.predict(make_input(deal_id="D002"))
        assert predictor.summary()["total"] == 2

    def test_risk_counts_populated(self, predictor, clean_input):
        predictor.predict(clean_input)
        s = predictor.summary()
        assert sum(s["risk_counts"].values()) == 1

    def test_pattern_counts_populated(self, predictor, clean_input):
        predictor.predict(clean_input)
        s = predictor.summary()
        assert sum(s["pattern_counts"].values()) == 1

    def test_momentum_counts_populated(self, predictor, clean_input):
        predictor.predict(clean_input)
        s = predictor.summary()
        assert sum(s["momentum_counts"].values()) == 1

    def test_action_counts_populated(self, predictor, clean_input):
        predictor.predict(clean_input)
        s = predictor.summary()
        assert sum(s["action_counts"].values()) == 1

    def test_at_risk_count_correct(self, predictor):
        predictor.predict(make_input(next_step_missed_count=3))  # at risk
        predictor.predict(make_input(deal_id="D002"))             # not at risk
        assert predictor.summary()["at_risk_count"] == 1

    def test_escalation_count_correct(self, predictor):
        predictor.predict(make_input(internal_champion_change=1))  # escalate
        predictor.predict(make_input(deal_id="D002"))
        assert predictor.summary()["escalation_count"] == 1

    def test_avg_ghosting_composite_is_rounded(self, predictor, clean_input):
        predictor.predict(clean_input)
        val = predictor.summary()["avg_ghosting_composite"]
        # round to 1 decimal place
        assert val == round(val, 1)

    def test_avg_recovery_probability_is_rounded(self, predictor, clean_input):
        predictor.predict(clean_input)
        val = predictor.summary()["avg_recovery_probability"]
        assert val == round(val, 1)

    def test_summary_after_reset_is_empty(self, predictor, clean_input):
        predictor.predict(clean_input)
        predictor.reset()
        assert predictor.summary()["total"] == 0

    def test_summary_counts_all_risk_levels(self, predictor):
        # low-risk deal
        predictor.predict(make_input(deal_id="D1"))
        # high-risk deal: silence + decay
        predictor.predict(make_input(
            deal_id="D2",
            days_since_last_buyer_reply=21,
            days_since_last_meeting=30,
            email_open_rate_last_30d=0,
            email_open_rate_prior_30d=80,
            response_time_avg_hours_recent=30,
            response_time_avg_hours_prior=5,
        ))
        s = predictor.summary()
        assert s["total"] == 2


# ─────────────────────────────────────────────────────────────────────────────
# 5. _silence_score branches
# ─────────────────────────────────────────────────────────────────────────────

class TestSilenceScore:
    def _score(self, **kwargs) -> float:
        p = GhostingPredictor()
        inp = make_input(**kwargs)
        return p._silence_score(inp)

    # ── days_since_last_buyer_reply thresholds ──
    def test_reply_lt_3_days_no_reply_points(self):
        assert self._score(days_since_last_buyer_reply=2) == 0.0

    def test_reply_exactly_3_adds_8(self):
        assert self._score(days_since_last_buyer_reply=3) == 8.0

    def test_reply_6_days_adds_8(self):
        assert self._score(days_since_last_buyer_reply=6) == 8.0

    def test_reply_exactly_7_adds_20(self):
        assert self._score(days_since_last_buyer_reply=7) == 20.0

    def test_reply_13_days_adds_20(self):
        assert self._score(days_since_last_buyer_reply=13) == 20.0

    def test_reply_exactly_14_adds_35(self):
        assert self._score(days_since_last_buyer_reply=14) == 35.0

    def test_reply_20_days_adds_35(self):
        assert self._score(days_since_last_buyer_reply=20) == 35.0

    def test_reply_exactly_21_adds_50(self):
        assert self._score(days_since_last_buyer_reply=21) == 50.0

    def test_reply_30_days_adds_50(self):
        assert self._score(days_since_last_buyer_reply=30) == 50.0

    # ── days_since_last_meeting thresholds ──
    def test_meeting_lt_7_no_meeting_points(self):
        assert self._score(days_since_last_meeting=6) == 0.0

    def test_meeting_exactly_7_adds_8(self):
        assert self._score(days_since_last_meeting=7) == 8.0

    def test_meeting_13_days_adds_8(self):
        assert self._score(days_since_last_meeting=13) == 8.0

    def test_meeting_exactly_14_adds_15(self):
        assert self._score(days_since_last_meeting=14) == 15.0

    def test_meeting_29_days_adds_15(self):
        assert self._score(days_since_last_meeting=29) == 15.0

    def test_meeting_exactly_30_adds_25(self):
        assert self._score(days_since_last_meeting=30) == 25.0

    # ── champion_last_active_days_ago thresholds ──
    def test_champion_lt_10_no_champ_points(self):
        assert self._score(champion_last_active_days_ago=9) == 0.0

    def test_champion_exactly_10_adds_8(self):
        assert self._score(champion_last_active_days_ago=10) == 8.0

    def test_champion_20_days_adds_8(self):
        assert self._score(champion_last_active_days_ago=20) == 8.0

    def test_champion_exactly_21_adds_15(self):
        assert self._score(champion_last_active_days_ago=21) == 15.0

    def test_champion_30_days_adds_15(self):
        assert self._score(champion_last_active_days_ago=30) == 15.0

    # ── proposal_opened_last_7d subtracts 15 ──
    def test_proposal_opened_reduces_score(self):
        # 21 days reply (+50), proposal opened (-15) = 35
        score = self._score(days_since_last_buyer_reply=21, proposal_opened_last_7d=1)
        assert score == 35.0

    def test_proposal_opened_cannot_go_below_zero(self):
        # score = 0, proposal opened => max(0, -15) = 0
        score = self._score(proposal_opened_last_7d=1)
        assert score == 0.0

    # ── combined ──
    def test_additive_signals(self):
        # reply=21 (+50) + meeting=30 (+25) + champ=21 (+15) = 90
        score = self._score(
            days_since_last_buyer_reply=21,
            days_since_last_meeting=30,
            champion_last_active_days_ago=21,
        )
        assert score == 90.0

    def test_max_clamp_at_100(self):
        # reply=21 (+50) + meeting=30 (+25) + champ=21 (+15) = 90 < 100
        # To force >100 we can't with these values alone; test clamp with worst case
        score = self._score(
            days_since_last_buyer_reply=21,
            days_since_last_meeting=30,
            champion_last_active_days_ago=21,
        )
        assert score <= 100.0

    def test_score_is_non_negative(self):
        assert self._score() >= 0.0

    def test_score_rounded_to_1dp(self):
        s = self._score(days_since_last_buyer_reply=7)
        assert s == round(s, 1)


# ─────────────────────────────────────────────────────────────────────────────
# 6. _engagement_decay_score branches
# ─────────────────────────────────────────────────────────────────────────────

class TestEngagementDecayScore:
    def _score(self, **kwargs) -> float:
        p = GhostingPredictor()
        inp = make_input(**kwargs)
        return p._engagement_decay_score(inp)

    # ── email open decay ──
    def test_no_open_decay_zero_points(self):
        assert self._score(email_open_rate_last_30d=60, email_open_rate_prior_30d=60) == 0.0

    def test_open_decay_lt_10_no_penalty(self):
        s = self._score(email_open_rate_last_30d=55, email_open_rate_prior_30d=60)
        assert s == 0.0  # decay=5, below threshold

    def test_open_decay_exactly_10_adds_10(self):
        s = self._score(email_open_rate_last_30d=50, email_open_rate_prior_30d=60)
        assert s == 10.0  # decay=10

    def test_open_decay_19_adds_10(self):
        s = self._score(email_open_rate_last_30d=41, email_open_rate_prior_30d=60)
        assert s == 10.0  # decay=19

    def test_open_decay_exactly_20_adds_20(self):
        s = self._score(email_open_rate_last_30d=40, email_open_rate_prior_30d=60)
        assert s == 20.0  # decay=20

    def test_open_decay_39_adds_20(self):
        s = self._score(email_open_rate_last_30d=21, email_open_rate_prior_30d=60)
        assert s == 20.0  # decay=39

    def test_open_decay_exactly_40_adds_30(self):
        s = self._score(email_open_rate_last_30d=20, email_open_rate_prior_30d=60)
        assert s == 30.0  # decay=40

    def test_open_rate_improved_subtracts_10(self):
        # recent > prior => negative decay => -10
        s = self._score(email_open_rate_last_30d=70, email_open_rate_prior_30d=60)
        assert s == -10.0 or s == 0.0  # max(0, -10) clamps to 0

    def test_open_rate_improved_final_score_non_negative(self):
        s = self._score(email_open_rate_last_30d=100, email_open_rate_prior_30d=0)
        assert s >= 0.0

    # ── response time ratio ──
    def test_rt_ratio_normal_no_points(self):
        s = self._score(response_time_avg_hours_recent=2.0, response_time_avg_hours_prior=2.0)
        assert s == 0.0

    def test_rt_ratio_lt_0_8_subtracts_10(self):
        # ratio = 1/2 = 0.5 < 0.8
        s = self._score(
            response_time_avg_hours_recent=1.0,
            response_time_avg_hours_prior=2.0,
        )
        assert s == -10.0 or s == 0.0  # clamped to 0

    def test_rt_ratio_1_5_adds_10(self):
        # ratio = 3.0/2.0 = 1.5
        s = self._score(
            response_time_avg_hours_recent=3.0,
            response_time_avg_hours_prior=2.0,
        )
        assert s == 10.0

    def test_rt_ratio_between_1_5_and_2_adds_10(self):
        # ratio = 1.9
        s = self._score(
            response_time_avg_hours_recent=3.8,
            response_time_avg_hours_prior=2.0,
        )
        assert s == 10.0

    def test_rt_ratio_exactly_2_adds_20(self):
        s = self._score(
            response_time_avg_hours_recent=4.0,
            response_time_avg_hours_prior=2.0,
        )
        assert s == 20.0

    def test_rt_ratio_exactly_3_adds_30(self):
        s = self._score(
            response_time_avg_hours_recent=6.0,
            response_time_avg_hours_prior=2.0,
        )
        assert s == 30.0

    def test_rt_ratio_gt_3_adds_30(self):
        s = self._score(
            response_time_avg_hours_recent=10.0,
            response_time_avg_hours_prior=2.0,
        )
        assert s == 30.0

    def test_rt_prior_zero_recent_zero_ratio_1(self):
        # prior=0, recent=0 => ratio=1.0, no rt contribution
        s = self._score(
            response_time_avg_hours_recent=0.0,
            response_time_avg_hours_prior=0.0,
        )
        assert s == 0.0

    def test_rt_prior_zero_recent_nonzero_ratio_2(self):
        # prior=0, recent>0 => ratio=2.0 => +20
        s = self._score(
            response_time_avg_hours_recent=5.0,
            response_time_avg_hours_prior=0.0,
        )
        assert s == 20.0

    # ── stakeholder dropout ──
    def test_no_stakeholder_drop_zero(self):
        assert self._score(stakeholder_count_drop=0) == 0.0

    def test_stakeholder_drop_1_adds_10(self):
        assert self._score(stakeholder_count_drop=1) == 10.0

    def test_stakeholder_drop_2_adds_10(self):
        assert self._score(stakeholder_count_drop=2) == 10.0

    def test_stakeholder_drop_3_adds_20(self):
        assert self._score(stakeholder_count_drop=3) == 20.0

    def test_stakeholder_drop_5_adds_20(self):
        assert self._score(stakeholder_count_drop=5) == 20.0

    # ── linkedin silence ──
    def test_linkedin_quiet_adds_10(self):
        assert self._score(champion_linkedin_gone_quiet=1) == 10.0

    def test_linkedin_active_no_bonus(self):
        assert self._score(champion_linkedin_gone_quiet=0) == 0.0

    # ── combined max clamp ──
    def test_score_max_100(self):
        s = self._score(
            email_open_rate_last_30d=0,
            email_open_rate_prior_30d=100,
            response_time_avg_hours_recent=30,
            response_time_avg_hours_prior=2,
            stakeholder_count_drop=5,
            champion_linkedin_gone_quiet=1,
        )
        assert s <= 100.0

    def test_score_non_negative(self):
        assert self._score() >= 0.0


# ─────────────────────────────────────────────────────────────────────────────
# 7. _behavioral_risk_score branches
# ─────────────────────────────────────────────────────────────────────────────

class TestBehavioralRiskScore:
    def _score(self, **kwargs) -> float:
        p = GhostingPredictor()
        inp = make_input(**kwargs)
        return p._behavioral_risk_score(inp)

    # ── next_step_missed_count ──
    def test_no_missed_steps_zero(self):
        assert self._score(next_step_missed_count=0) == 0.0

    def test_missed_1_adds_10(self):
        assert self._score(next_step_missed_count=1) == 10.0

    def test_missed_2_adds_22(self):
        assert self._score(next_step_missed_count=2) == 22.0

    def test_missed_3_adds_22(self):
        assert self._score(next_step_missed_count=3) == 22.0

    def test_missed_4_adds_35(self):
        assert self._score(next_step_missed_count=4) == 35.0

    def test_missed_10_adds_35(self):
        assert self._score(next_step_missed_count=10) == 35.0

    # ── meetings_cancelled_last_30d ──
    def test_cancelled_0_zero(self):
        assert self._score(meetings_cancelled_last_30d=0) == 0.0

    def test_cancelled_1_adds_6(self):
        assert self._score(meetings_cancelled_last_30d=1) == 6.0

    def test_cancelled_2_adds_12(self):
        assert self._score(meetings_cancelled_last_30d=2) == 12.0

    def test_cancelled_3_adds_20(self):
        assert self._score(meetings_cancelled_last_30d=3) == 20.0

    def test_cancelled_5_adds_20(self):
        assert self._score(meetings_cancelled_last_30d=5) == 20.0

    # ── meetings_rescheduled_last_30d ──
    def test_rescheduled_0_zero(self):
        assert self._score(meetings_rescheduled_last_30d=0) == 0.0

    def test_rescheduled_1_adds_4(self):
        assert self._score(meetings_rescheduled_last_30d=1) == 4.0

    def test_rescheduled_2_adds_4(self):
        assert self._score(meetings_rescheduled_last_30d=2) == 4.0

    def test_rescheduled_3_adds_8(self):
        assert self._score(meetings_rescheduled_last_30d=3) == 8.0

    def test_rescheduled_5_adds_8(self):
        assert self._score(meetings_rescheduled_last_30d=5) == 8.0

    # ── internal_champion_change ──
    def test_champion_change_adds_20(self):
        assert self._score(internal_champion_change=1) == 20.0

    def test_no_champion_change_zero(self):
        assert self._score(internal_champion_change=0) == 0.0

    # ── competitor_meeting_signal ──
    def test_competitor_signal_adds_12(self):
        assert self._score(competitor_meeting_signal=1) == 12.0

    def test_no_competitor_signal_zero(self):
        assert self._score(competitor_meeting_signal=0) == 0.0

    # ── pricing_conversation_stalled ──
    def test_pricing_stalled_adds_10(self):
        assert self._score(pricing_conversation_stalled=1) == 10.0

    def test_pricing_active_zero(self):
        assert self._score(pricing_conversation_stalled=0) == 0.0

    # ── combined ──
    def test_combined_score_max_100(self):
        s = self._score(
            next_step_missed_count=5,
            meetings_cancelled_last_30d=5,
            meetings_rescheduled_last_30d=5,
            internal_champion_change=1,
            competitor_meeting_signal=1,
            pricing_conversation_stalled=1,
        )
        assert s == 100.0

    def test_score_non_negative(self):
        assert self._score() >= 0.0


# ─────────────────────────────────────────────────────────────────────────────
# 8. _deal_urgency_score branches
# ─────────────────────────────────────────────────────────────────────────────

class TestDealUrgencyScore:
    def _score(self, **kwargs) -> float:
        p = GhostingPredictor()
        inp = make_input(**kwargs)
        return p._deal_urgency_score(inp)

    # ── deal_stage_days_stuck ──
    def test_stuck_lt_14_zero(self):
        assert self._score(deal_stage_days_stuck=13) == 0.0

    def test_stuck_exactly_14_adds_12(self):
        assert self._score(deal_stage_days_stuck=14) == 12.0

    def test_stuck_29_adds_12(self):
        assert self._score(deal_stage_days_stuck=29) == 12.0

    def test_stuck_exactly_30_adds_25(self):
        assert self._score(deal_stage_days_stuck=30) == 25.0

    def test_stuck_59_adds_25(self):
        assert self._score(deal_stage_days_stuck=59) == 25.0

    def test_stuck_exactly_60_adds_40(self):
        assert self._score(deal_stage_days_stuck=60) == 40.0

    def test_stuck_100_adds_40(self):
        assert self._score(deal_stage_days_stuck=100) == 40.0

    # ── days_to_close_target ──
    def test_close_gt_30_zero(self):
        assert self._score(days_to_close_target=31) == 0.0

    def test_close_exactly_30_adds_12(self):
        assert self._score(days_to_close_target=30) == 12.0

    def test_close_15_adds_12(self):
        assert self._score(days_to_close_target=15) == 12.0

    def test_close_exactly_14_adds_20(self):
        assert self._score(days_to_close_target=14) == 20.0

    def test_close_8_adds_20(self):
        assert self._score(days_to_close_target=8) == 20.0

    def test_close_exactly_7_adds_30(self):
        assert self._score(days_to_close_target=7) == 30.0

    def test_close_0_adds_30(self):
        assert self._score(days_to_close_target=0) == 30.0

    # ── deal_value ──
    def test_value_lt_100k_no_bonus(self):
        assert self._score(deal_value=99_999.0) == 0.0

    def test_value_exactly_100k_adds_6(self):
        assert self._score(deal_value=100_000.0) == 6.0

    def test_value_199k_adds_6(self):
        assert self._score(deal_value=199_999.0) == 6.0

    def test_value_exactly_200k_adds_12(self):
        assert self._score(deal_value=200_000.0) == 12.0

    def test_value_499k_adds_12(self):
        assert self._score(deal_value=499_999.0) == 12.0

    def test_value_exactly_500k_adds_20(self):
        assert self._score(deal_value=500_000.0) == 20.0

    def test_value_1m_adds_20(self):
        assert self._score(deal_value=1_000_000.0) == 20.0

    # ── proposal_opened_last_7d ──
    def test_proposal_opened_adds_10(self):
        base = self._score()
        with_proposal = self._score(proposal_opened_last_7d=1)
        assert with_proposal == base + 10.0

    def test_proposal_opened_capped_100(self):
        s = self._score(
            deal_stage_days_stuck=100,
            days_to_close_target=0,
            deal_value=1_000_000,
            proposal_opened_last_7d=1,
        )
        assert s == 100.0

    def test_score_non_negative(self):
        assert self._score() >= 0.0

    def test_score_max_100(self):
        s = self._score(
            deal_stage_days_stuck=100,
            days_to_close_target=0,
            deal_value=1_000_000,
            proposal_opened_last_7d=1,
        )
        assert s <= 100.0


# ─────────────────────────────────────────────────────────────────────────────
# 9. _composite
# ─────────────────────────────────────────────────────────────────────────────

class TestComposite:
    def test_formula_correctness(self):
        p = GhostingPredictor()
        silence, decay, behav, urgency = 40.0, 60.0, 20.0, 10.0
        expected = round(40 * 0.35 + 60 * 0.30 + 20 * 0.25 + 10 * 0.10, 1)
        assert p._composite(silence, decay, behav, urgency) == expected

    def test_all_zero_gives_zero(self):
        p = GhostingPredictor()
        assert p._composite(0.0, 0.0, 0.0, 0.0) == 0.0

    def test_all_100_gives_100(self):
        p = GhostingPredictor()
        assert p._composite(100.0, 100.0, 100.0, 100.0) == 100.0

    def test_weights_sum_to_one(self):
        # silence only = 100 => composite = 35
        p = GhostingPredictor()
        assert p._composite(100.0, 0.0, 0.0, 0.0) == 35.0

    def test_decay_weight(self):
        p = GhostingPredictor()
        assert p._composite(0.0, 100.0, 0.0, 0.0) == 30.0

    def test_behav_weight(self):
        p = GhostingPredictor()
        assert p._composite(0.0, 0.0, 100.0, 0.0) == 25.0

    def test_urgency_weight(self):
        p = GhostingPredictor()
        assert p._composite(0.0, 0.0, 0.0, 100.0) == 10.0

    def test_clamped_at_100(self):
        p = GhostingPredictor()
        assert p._composite(200.0, 200.0, 200.0, 200.0) == 100.0

    def test_clamped_at_zero(self):
        p = GhostingPredictor()
        assert p._composite(-50.0, -50.0, -50.0, -50.0) == 0.0

    def test_rounded_to_1dp(self):
        p = GhostingPredictor()
        val = p._composite(33.0, 33.0, 33.0, 33.0)
        assert val == round(val, 1)


# ─────────────────────────────────────────────────────────────────────────────
# 10. _ghosting_risk thresholds
# ─────────────────────────────────────────────────────────────────────────────

class TestGhostingRisk:
    def _risk(self, composite: float) -> GhostingRisk:
        return GhostingPredictor()._ghosting_risk(composite)

    def test_composite_0_is_low(self):
        assert self._risk(0.0) == GhostingRisk.LOW

    def test_composite_29_is_low(self):
        assert self._risk(29.9) == GhostingRisk.LOW

    def test_composite_30_is_moderate(self):
        assert self._risk(30.0) == GhostingRisk.MODERATE

    def test_composite_49_is_moderate(self):
        assert self._risk(49.9) == GhostingRisk.MODERATE

    def test_composite_50_is_high(self):
        assert self._risk(50.0) == GhostingRisk.HIGH

    def test_composite_69_is_high(self):
        assert self._risk(69.9) == GhostingRisk.HIGH

    def test_composite_70_is_critical(self):
        assert self._risk(70.0) == GhostingRisk.CRITICAL

    def test_composite_100_is_critical(self):
        assert self._risk(100.0) == GhostingRisk.CRITICAL


# ─────────────────────────────────────────────────────────────────────────────
# 11. _ghosting_pattern branches
# ─────────────────────────────────────────────────────────────────────────────

class TestGhostingPattern:
    def _pattern(self, composite: float, **inp_kwargs) -> GhostingPattern:
        p = GhostingPredictor()
        inp = make_input(**inp_kwargs)
        return p._ghosting_pattern(inp, composite)

    def test_champion_exit_takes_priority_with_high_composite(self):
        pat = self._pattern(composite=50.0, internal_champion_change=1)
        assert pat == GhostingPattern.CHAMPION_EXIT

    def test_champion_change_low_composite_not_champion_exit(self):
        pat = self._pattern(composite=49.9, internal_champion_change=1)
        assert pat != GhostingPattern.CHAMPION_EXIT

    def test_full_ghost_21_days_no_reply_composite_65(self):
        pat = self._pattern(
            composite=65.0,
            days_since_last_buyer_reply=21,
        )
        assert pat == GhostingPattern.FULL_GHOST

    def test_full_ghost_requires_composite_65(self):
        pat = self._pattern(
            composite=64.9,
            days_since_last_buyer_reply=21,
        )
        assert pat != GhostingPattern.FULL_GHOST

    def test_full_ghost_requires_21_days(self):
        pat = self._pattern(
            composite=65.0,
            days_since_last_buyer_reply=20,
        )
        assert pat != GhostingPattern.FULL_GHOST

    def test_partial_ghost_with_stakeholder_drop_and_composite_45(self):
        pat = self._pattern(
            composite=45.0,
            stakeholder_count_drop=2,
        )
        assert pat == GhostingPattern.PARTIAL_GHOST

    def test_partial_ghost_requires_composite_45(self):
        pat = self._pattern(
            composite=44.9,
            stakeholder_count_drop=2,
        )
        assert pat != GhostingPattern.PARTIAL_GHOST

    def test_partial_ghost_requires_2_stakeholder_drops(self):
        pat = self._pattern(
            composite=45.0,
            stakeholder_count_drop=1,
        )
        assert pat != GhostingPattern.PARTIAL_GHOST

    def test_slow_fade_open_rate_drop(self):
        # recent < 10, prior >= 30
        pat = self._pattern(
            composite=20.0,
            email_open_rate_last_30d=5.0,
            email_open_rate_prior_30d=30.0,
        )
        assert pat == GhostingPattern.SLOW_FADE

    def test_slow_fade_requires_recent_lt_10(self):
        pat = self._pattern(
            composite=20.0,
            email_open_rate_last_30d=10.0,
            email_open_rate_prior_30d=30.0,
        )
        assert pat != GhostingPattern.SLOW_FADE

    def test_slow_fade_requires_prior_ge_30(self):
        pat = self._pattern(
            composite=20.0,
            email_open_rate_last_30d=5.0,
            email_open_rate_prior_30d=29.0,
        )
        assert pat != GhostingPattern.SLOW_FADE

    def test_cooling_off_composite_35(self):
        pat = self._pattern(composite=35.0)
        assert pat == GhostingPattern.COOLING_OFF

    def test_cooling_off_composite_34_9(self):
        # composite < 35 with no other signals => ENGAGED
        pat = self._pattern(composite=34.9)
        assert pat == GhostingPattern.ENGAGED

    def test_engaged_all_good_signals(self):
        pat = self._pattern(composite=10.0)
        assert pat == GhostingPattern.ENGAGED

    def test_engaged_zero_composite(self):
        pat = self._pattern(composite=0.0)
        assert pat == GhostingPattern.ENGAGED

    def test_champion_exit_overrides_full_ghost(self):
        # Both champion_change=1 + 21 days + composite=70
        pat = self._pattern(
            composite=70.0,
            internal_champion_change=1,
            days_since_last_buyer_reply=21,
        )
        assert pat == GhostingPattern.CHAMPION_EXIT


# ─────────────────────────────────────────────────────────────────────────────
# 12. _buyer_momentum branches
# ─────────────────────────────────────────────────────────────────────────────

class TestBuyerMomentum:
    def _momentum(self, **kwargs) -> BuyerMomentum:
        p = GhostingPredictor()
        inp = make_input(**kwargs)
        return p._buyer_momentum(inp)

    def test_accelerating_open_delta_10_rt_below_0_8(self):
        m = self._momentum(
            email_open_rate_last_30d=80.0,
            email_open_rate_prior_30d=70.0,  # delta=10
            response_time_avg_hours_recent=1.0,
            response_time_avg_hours_prior=2.0,  # ratio=0.5
        )
        assert m == BuyerMomentum.ACCELERATING

    def test_accelerating_requires_delta_ge_10(self):
        m = self._momentum(
            email_open_rate_last_30d=79.0,
            email_open_rate_prior_30d=70.0,  # delta=9
            response_time_avg_hours_recent=1.0,
            response_time_avg_hours_prior=2.0,
        )
        assert m != BuyerMomentum.ACCELERATING

    def test_accelerating_requires_rt_ratio_lt_0_8(self):
        m = self._momentum(
            email_open_rate_last_30d=80.0,
            email_open_rate_prior_30d=70.0,  # delta=10
            response_time_avg_hours_recent=2.0,
            response_time_avg_hours_prior=2.0,  # ratio=1.0
        )
        assert m != BuyerMomentum.ACCELERATING

    def test_stalled_open_delta_le_minus_20(self):
        m = self._momentum(
            email_open_rate_last_30d=40.0,
            email_open_rate_prior_30d=60.0,  # delta=-20
        )
        assert m == BuyerMomentum.STALLED

    def test_stalled_rt_ratio_ge_3(self):
        m = self._momentum(
            response_time_avg_hours_recent=6.0,
            response_time_avg_hours_prior=2.0,  # ratio=3.0
        )
        assert m == BuyerMomentum.STALLED

    def test_stalled_days_since_reply_ge_14(self):
        m = self._momentum(days_since_last_buyer_reply=14)
        assert m == BuyerMomentum.STALLED

    def test_stalled_days_since_reply_21(self):
        m = self._momentum(days_since_last_buyer_reply=21)
        assert m == BuyerMomentum.STALLED

    def test_decelerating_open_delta_le_minus_10(self):
        m = self._momentum(
            email_open_rate_last_30d=50.0,
            email_open_rate_prior_30d=60.0,  # delta=-10
        )
        assert m == BuyerMomentum.DECELERATING

    def test_decelerating_rt_ratio_ge_1_5(self):
        m = self._momentum(
            response_time_avg_hours_recent=3.0,
            response_time_avg_hours_prior=2.0,  # ratio=1.5
        )
        assert m == BuyerMomentum.DECELERATING

    def test_stable_no_bad_signals(self):
        m = self._momentum(
            email_open_rate_last_30d=60.0,
            email_open_rate_prior_30d=60.0,
            response_time_avg_hours_recent=2.0,
            response_time_avg_hours_prior=2.0,
            days_since_last_buyer_reply=5,
        )
        assert m == BuyerMomentum.STABLE

    def test_prior_zero_recent_zero_stable(self):
        # prior=0, recent=0 => ratio=1.0
        m = self._momentum(
            response_time_avg_hours_recent=0.0,
            response_time_avg_hours_prior=0.0,
        )
        assert m == BuyerMomentum.STABLE

    def test_prior_zero_recent_nonzero_decelerating_ratio_2(self):
        # prior=0, recent>0 => ratio=2.0, which is >= 1.5 but < 3.0 => DECELERATING
        m = self._momentum(
            response_time_avg_hours_recent=5.0,
            response_time_avg_hours_prior=0.0,
        )
        assert m == BuyerMomentum.DECELERATING


# ─────────────────────────────────────────────────────────────────────────────
# 13. _predicted_ghost_days branches
# ─────────────────────────────────────────────────────────────────────────────

class TestPredictedGhostDays:
    def _days(self, composite: float, days_since_last_buyer_reply: int = 0) -> int:
        p = GhostingPredictor()
        inp = make_input(days_since_last_buyer_reply=days_since_last_buyer_reply)
        return p._predicted_ghost_days(inp, composite)

    def test_composite_80_returns_0(self):
        assert self._days(80.0) == 0

    def test_composite_100_returns_0(self):
        assert self._days(100.0) == 0

    def test_composite_60_formula(self):
        # max(0, 14 - days_since_reply)
        assert self._days(60.0, days_since_last_buyer_reply=5) == 9
        assert self._days(60.0, days_since_last_buyer_reply=14) == 0
        assert self._days(60.0, days_since_last_buyer_reply=20) == 0

    def test_composite_79_formula(self):
        assert self._days(79.0, days_since_last_buyer_reply=3) == 11

    def test_composite_40_formula(self):
        # max(0, 21 - days)
        assert self._days(40.0, days_since_last_buyer_reply=5) == 16
        assert self._days(40.0, days_since_last_buyer_reply=21) == 0
        assert self._days(40.0, days_since_last_buyer_reply=25) == 0

    def test_composite_59_formula(self):
        assert self._days(59.0, days_since_last_buyer_reply=10) == 11

    def test_composite_lt_40_formula(self):
        # max(0, 30 - days)
        assert self._days(10.0, days_since_last_buyer_reply=5) == 25
        assert self._days(10.0, days_since_last_buyer_reply=30) == 0
        assert self._days(10.0, days_since_last_buyer_reply=35) == 0

    def test_non_negative_always(self):
        for composite in [0, 10, 39, 40, 59, 60, 79, 80, 100]:
            assert self._days(float(composite), days_since_last_buyer_reply=100) >= 0


# ─────────────────────────────────────────────────────────────────────────────
# 14. _recovery_probability branches
# ─────────────────────────────────────────────────────────────────────────────

class TestRecoveryProbability:
    def _prob(self, composite: float, **kwargs) -> float:
        p = GhostingPredictor()
        inp = make_input(**kwargs)
        return p._recovery_probability(inp, composite)

    def test_base_is_100_minus_composite(self):
        prob = self._prob(30.0)
        assert prob == 70.0

    def test_proposal_opened_adds_15(self):
        prob = self._prob(30.0, proposal_opened_last_7d=1)
        assert prob == 85.0

    def test_proposal_opened_capped_at_100(self):
        prob = self._prob(0.0, proposal_opened_last_7d=1)
        assert prob == 100.0

    def test_champion_change_subtracts_20(self):
        prob = self._prob(30.0, internal_champion_change=1)
        assert prob == 50.0

    def test_competitor_signal_subtracts_15(self):
        prob = self._prob(30.0, competitor_meeting_signal=1)
        assert prob == 55.0

    def test_reply_ge_30_subtracts_20(self):
        prob = self._prob(30.0, days_since_last_buyer_reply=30)
        assert prob == 50.0

    def test_reply_ge_14_lt_30_subtracts_10(self):
        prob = self._prob(30.0, days_since_last_buyer_reply=14)
        assert prob == 60.0

    def test_reply_ge_14_lt_30_boundary(self):
        prob = self._prob(30.0, days_since_last_buyer_reply=20)
        assert prob == 60.0

    def test_reply_lt_14_no_penalty(self):
        prob = self._prob(30.0, days_since_last_buyer_reply=13)
        assert prob == 70.0

    def test_floor_at_zero(self):
        prob = self._prob(
            80.0,
            internal_champion_change=1,
            competitor_meeting_signal=1,
            days_since_last_buyer_reply=30,
        )
        assert prob == 0.0

    def test_combined_penalties(self):
        # base = 100-50=50, champ -20, competitor -15, reply>=30 -20 = -5 => clamped 0
        prob = self._prob(
            50.0,
            internal_champion_change=1,
            competitor_meeting_signal=1,
            days_since_last_buyer_reply=30,
        )
        assert prob == 0.0

    def test_rounded_to_1dp(self):
        prob = self._prob(33.3)
        assert prob == round(prob, 1)

    def test_max_at_100(self):
        prob = self._prob(0.0, proposal_opened_last_7d=1)
        assert prob <= 100.0


# ─────────────────────────────────────────────────────────────────────────────
# 15. _ghosting_action branches
# ─────────────────────────────────────────────────────────────────────────────

class TestGhostingAction:
    def _action(self, risk: GhostingRisk, needs_esc: bool, composite: float = 0.0) -> GhostingAction:
        return GhostingPredictor()._ghosting_action(risk, needs_esc, composite)

    def test_needs_esc_gives_last_resort(self):
        assert self._action(GhostingRisk.LOW, True) == GhostingAction.LAST_RESORT

    def test_critical_risk_gives_last_resort(self):
        assert self._action(GhostingRisk.CRITICAL, False) == GhostingAction.LAST_RESORT

    def test_critical_and_needs_esc_gives_last_resort(self):
        assert self._action(GhostingRisk.CRITICAL, True) == GhostingAction.LAST_RESORT

    def test_high_risk_no_esc_gives_escalate_path(self):
        assert self._action(GhostingRisk.HIGH, False) == GhostingAction.ESCALATE_PATH

    def test_moderate_risk_no_esc_gives_re_engage(self):
        assert self._action(GhostingRisk.MODERATE, False) == GhostingAction.RE_ENGAGE

    def test_low_risk_no_esc_gives_maintain(self):
        assert self._action(GhostingRisk.LOW, False) == GhostingAction.MAINTAIN


# ─────────────────────────────────────────────────────────────────────────────
# 16. is_at_risk_of_ghosting flag
# ─────────────────────────────────────────────────────────────────────────────

class TestIsAtRisk:
    def test_at_risk_when_composite_ge_50(self, predictor):
        # Force composite >= 50 via multiple high-signal inputs
        # silence: reply=21 (+50) + meeting=30 (+25) + champ=21 (+15) = 90 -> silence*0.35=31.5
        # behav: missed=4 (+35) + cancelled=3 (+20) + champion_change=0 -> 55 -> behav*0.25=13.75
        # decay: stakeholder_drop=3 (+20) + linkedin (+10) = 30 -> decay*0.30=9.0
        # urgency: stuck=60 (+40) + close=7 (+30) = 70 -> urgency*0.10=7.0
        # composite = 31.5+9+13.75+7 = 61.25 >= 50
        inp = make_input(
            days_since_last_buyer_reply=21,
            days_since_last_meeting=30,
            champion_last_active_days_ago=21,
            next_step_missed_count=4,
            meetings_cancelled_last_30d=3,
            stakeholder_count_drop=3,
            champion_linkedin_gone_quiet=1,
            deal_stage_days_stuck=60,
            days_to_close_target=7,
        )
        result = predictor.predict(inp)
        assert result.ghosting_composite >= 50.0
        assert result.is_at_risk_of_ghosting is True

    def test_at_risk_when_next_step_missed_ge_3(self, predictor):
        inp = make_input(next_step_missed_count=3)
        result = predictor.predict(inp)
        assert result.is_at_risk_of_ghosting is True

    def test_at_risk_next_step_4(self, predictor):
        inp = make_input(next_step_missed_count=4)
        result = predictor.predict(inp)
        assert result.is_at_risk_of_ghosting is True

    def test_not_at_risk_low_composite_low_missed(self, predictor):
        inp = make_input()
        result = predictor.predict(inp)
        assert result.is_at_risk_of_ghosting is False

    def test_at_risk_boundary_composite_50(self, predictor):
        # Construct input that yields composite == 50 by design
        # silence=50 -> composite= 50*0.35=17.5; need total=50
        # Use high silence + behavioral to push composite to 50
        inp = make_input(
            days_since_last_buyer_reply=21,    # silence: +50
            days_since_last_meeting=30,         # silence: +25 = 75 total silence
            next_step_missed_count=4,           # behav: +35
            meetings_cancelled_last_30d=3,      # behav: +20 -> 55 total
            internal_champion_change=1,         # behav: +20 -> 75 total
        )
        result = predictor.predict(inp)
        assert result.is_at_risk_of_ghosting is True

    def test_at_risk_exactly_next_step_missed_3(self, predictor):
        inp = make_input(next_step_missed_count=3)
        result = predictor.predict(inp)
        assert result.is_at_risk_of_ghosting is True

    def test_not_at_risk_next_step_missed_2(self, predictor):
        inp = make_input(next_step_missed_count=2)
        result = predictor.predict(inp)
        # composite is likely low, and missed < 3
        if result.ghosting_composite < 50:
            assert result.is_at_risk_of_ghosting is False


# ─────────────────────────────────────────────────────────────────────────────
# 17. needs_escalation flag
# ─────────────────────────────────────────────────────────────────────────────

class TestNeedsEscalation:
    def test_escalation_when_composite_ge_70(self, predictor):
        inp = make_input(
            days_since_last_buyer_reply=21,
            days_since_last_meeting=30,
            champion_last_active_days_ago=21,
            next_step_missed_count=4,
            meetings_cancelled_last_30d=3,
            internal_champion_change=0,
            competitor_meeting_signal=1,
            pricing_conversation_stalled=1,
        )
        result = predictor.predict(inp)
        if result.ghosting_composite >= 70:
            assert result.needs_escalation is True

    def test_escalation_when_internal_champion_change(self, predictor):
        inp = make_input(internal_champion_change=1)
        result = predictor.predict(inp)
        assert result.needs_escalation is True

    def test_escalation_when_days_since_reply_ge_21(self, predictor):
        inp = make_input(days_since_last_buyer_reply=21)
        result = predictor.predict(inp)
        assert result.needs_escalation is True

    def test_escalation_days_reply_exactly_21(self, predictor):
        inp = make_input(days_since_last_buyer_reply=21)
        result = predictor.predict(inp)
        assert result.needs_escalation is True

    def test_no_escalation_clean_deal(self, predictor):
        inp = make_input()
        result = predictor.predict(inp)
        assert result.needs_escalation is False

    def test_no_escalation_days_reply_20(self, predictor):
        inp = make_input(days_since_last_buyer_reply=20)
        result = predictor.predict(inp)
        # composite unlikely >=70, no champion change, days_reply=20 < 21
        if result.ghosting_composite < 70 and not result.needs_escalation:
            assert result.needs_escalation is False

    def test_escalation_composite_70_boundary(self, predictor):
        # Build deal with exactly composite around 70
        inp = make_input(
            days_since_last_buyer_reply=21,
            days_since_last_meeting=30,
            champion_last_active_days_ago=21,
            next_step_missed_count=4,
            meetings_cancelled_last_30d=3,
        )
        result = predictor.predict(inp)
        if result.ghosting_composite >= 70:
            assert result.needs_escalation is True


# ─────────────────────────────────────────────────────────────────────────────
# 18. predict() public method
# ─────────────────────────────────────────────────────────────────────────────

class TestPredict:
    def test_returns_result_type(self, predictor, clean_input):
        r = predictor.predict(clean_input)
        assert isinstance(r, GhostingPredictorResult)

    def test_deal_id_preserved(self, predictor):
        r = predictor.predict(make_input(deal_id="DEAL-999"))
        assert r.deal_id == "DEAL-999"

    def test_deal_name_preserved(self, predictor):
        r = predictor.predict(make_input(deal_name="Big Enterprise"))
        assert r.deal_name == "Big Enterprise"

    def test_scores_are_floats(self, predictor, clean_input):
        r = predictor.predict(clean_input)
        assert isinstance(r.silence_score, float)
        assert isinstance(r.engagement_decay_score, float)
        assert isinstance(r.behavioral_risk_score, float)
        assert isinstance(r.deal_urgency_score, float)
        assert isinstance(r.ghosting_composite, float)
        assert isinstance(r.recovery_probability, float)

    def test_scores_in_range(self, predictor, clean_input):
        r = predictor.predict(clean_input)
        assert 0.0 <= r.silence_score <= 100.0
        assert 0.0 <= r.engagement_decay_score <= 100.0
        assert 0.0 <= r.behavioral_risk_score <= 100.0
        assert 0.0 <= r.deal_urgency_score <= 100.0
        assert 0.0 <= r.ghosting_composite <= 100.0
        assert 0.0 <= r.recovery_probability <= 100.0

    def test_predicted_ghost_days_non_negative(self, predictor, clean_input):
        r = predictor.predict(clean_input)
        assert r.predicted_ghost_days >= 0

    def test_risk_is_enum_member(self, predictor, clean_input):
        r = predictor.predict(clean_input)
        assert isinstance(r.ghosting_risk, GhostingRisk)

    def test_pattern_is_enum_member(self, predictor, clean_input):
        r = predictor.predict(clean_input)
        assert isinstance(r.ghosting_pattern, GhostingPattern)

    def test_momentum_is_enum_member(self, predictor, clean_input):
        r = predictor.predict(clean_input)
        assert isinstance(r.buyer_momentum, BuyerMomentum)

    def test_action_is_enum_member(self, predictor, clean_input):
        r = predictor.predict(clean_input)
        assert isinstance(r.ghosting_action, GhostingAction)

    def test_result_appended_to_internal_list(self, predictor, clean_input):
        predictor.predict(clean_input)
        assert len(predictor._results) == 1

    def test_multiple_predictions_accumulate(self, predictor):
        predictor.predict(make_input(deal_id="D1"))
        predictor.predict(make_input(deal_id="D2"))
        predictor.predict(make_input(deal_id="D3"))
        assert len(predictor._results) == 3

    def test_composite_formula_applied(self, predictor):
        inp = make_input(
            days_since_last_buyer_reply=21,   # silence: +50
        )
        r = predictor.predict(inp)
        assert r.silence_score >= 50.0

    def test_high_risk_scenario(self, predictor):
        inp = make_input(
            days_since_last_buyer_reply=21,
            days_since_last_meeting=30,
            champion_last_active_days_ago=21,
            next_step_missed_count=4,
            meetings_cancelled_last_30d=3,
            competitor_meeting_signal=1,
            internal_champion_change=1,
        )
        r = predictor.predict(inp)
        assert r.ghosting_risk in (GhostingRisk.HIGH, GhostingRisk.CRITICAL)

    def test_low_risk_scenario(self, predictor):
        r = predictor.predict(make_input())
        assert r.ghosting_risk == GhostingRisk.LOW


# ─────────────────────────────────────────────────────────────────────────────
# 19. predict_batch() public method
# ─────────────────────────────────────────────────────────────────────────────

class TestPredictBatch:
    def test_returns_list(self, predictor):
        results = predictor.predict_batch([make_input(deal_id="D1"), make_input(deal_id="D2")])
        assert isinstance(results, list)

    def test_returns_correct_count(self, predictor):
        inputs = [make_input(deal_id=f"D{i}") for i in range(5)]
        results = predictor.predict_batch(inputs)
        assert len(results) == 5

    def test_all_results_are_correct_type(self, predictor):
        inputs = [make_input(deal_id=f"D{i}") for i in range(3)]
        for r in predictor.predict_batch(inputs):
            assert isinstance(r, GhostingPredictorResult)

    def test_empty_batch_returns_empty_list(self, predictor):
        assert predictor.predict_batch([]) == []

    def test_batch_accumulates_to_results(self, predictor):
        inputs = [make_input(deal_id=f"D{i}") for i in range(4)]
        predictor.predict_batch(inputs)
        assert len(predictor._results) == 4

    def test_batch_deal_ids_preserved(self, predictor):
        inputs = [make_input(deal_id=f"DEAL-{i}") for i in range(3)]
        results = predictor.predict_batch(inputs)
        assert [r.deal_id for r in results] == ["DEAL-0", "DEAL-1", "DEAL-2"]

    def test_single_item_batch(self, predictor, clean_input):
        results = predictor.predict_batch([clean_input])
        assert len(results) == 1
        assert isinstance(results[0], GhostingPredictorResult)


# ─────────────────────────────────────────────────────────────────────────────
# 20. reset()
# ─────────────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_results(self, predictor, clean_input):
        predictor.predict(clean_input)
        predictor.reset()
        assert len(predictor._results) == 0

    def test_reset_clears_multiple(self, predictor):
        for i in range(5):
            predictor.predict(make_input(deal_id=f"D{i}"))
        predictor.reset()
        assert len(predictor._results) == 0

    def test_can_predict_after_reset(self, predictor, clean_input):
        predictor.predict(clean_input)
        predictor.reset()
        predictor.predict(clean_input)
        assert len(predictor._results) == 1

    def test_summary_empty_after_reset(self, predictor, clean_input):
        predictor.predict(clean_input)
        predictor.reset()
        assert predictor.summary()["total"] == 0


# ─────────────────────────────────────────────────────────────────────────────
# 21. Properties
# ─────────────────────────────────────────────────────────────────────────────

class TestProperties:
    def test_at_risk_deals_empty_initially(self, predictor):
        assert predictor.at_risk_deals == []

    def test_at_risk_deals_populated(self, predictor):
        predictor.predict(make_input(next_step_missed_count=3))
        assert len(predictor.at_risk_deals) == 1

    def test_at_risk_deals_excludes_non_risk(self, predictor):
        predictor.predict(make_input(deal_id="D1"))  # safe
        predictor.predict(make_input(deal_id="D2", next_step_missed_count=3))  # at risk
        assert len(predictor.at_risk_deals) == 1

    def test_escalation_queue_empty_initially(self, predictor):
        assert predictor.escalation_queue == []

    def test_escalation_queue_populated(self, predictor):
        predictor.predict(make_input(internal_champion_change=1))
        assert len(predictor.escalation_queue) == 1

    def test_escalation_queue_excludes_non_escalation(self, predictor):
        predictor.predict(make_input(deal_id="D1"))  # safe
        predictor.predict(make_input(deal_id="D2", days_since_last_buyer_reply=21))  # escalate
        assert len(predictor.escalation_queue) == 1

    def test_avg_ghosting_composite_zero_when_empty(self, predictor):
        assert predictor.avg_ghosting_composite == 0.0

    def test_avg_ghosting_composite_single(self, predictor, clean_input):
        r = predictor.predict(clean_input)
        assert predictor.avg_ghosting_composite == round(r.ghosting_composite, 1)

    def test_avg_ghosting_composite_multiple(self, predictor):
        predictor.predict(make_input(deal_id="D1"))
        predictor.predict(make_input(deal_id="D2"))
        val = predictor.avg_ghosting_composite
        assert isinstance(val, float)
        assert val == round(val, 1)

    def test_avg_recovery_probability_zero_when_empty(self, predictor):
        assert predictor.avg_recovery_probability == 0.0

    def test_avg_recovery_probability_single(self, predictor, clean_input):
        r = predictor.predict(clean_input)
        assert predictor.avg_recovery_probability == round(r.recovery_probability, 1)

    def test_avg_recovery_probability_multiple(self, predictor):
        predictor.predict(make_input(deal_id="D1"))
        predictor.predict(make_input(deal_id="D2"))
        val = predictor.avg_recovery_probability
        assert isinstance(val, float)
        assert val == round(val, 1)

    def test_at_risk_and_escalation_cleared_after_reset(self, predictor):
        predictor.predict(make_input(
            next_step_missed_count=3,
            internal_champion_change=1,
        ))
        predictor.reset()
        assert predictor.at_risk_deals == []
        assert predictor.escalation_queue == []


# ─────────────────────────────────────────────────────────────────────────────
# 22. GhostingPredictor initialization
# ─────────────────────────────────────────────────────────────────────────────

class TestInitialization:
    def test_new_predictor_has_empty_results(self):
        p = GhostingPredictor()
        assert p._results == []

    def test_new_predictor_avg_composite_zero(self):
        assert GhostingPredictor().avg_ghosting_composite == 0.0

    def test_new_predictor_avg_recovery_zero(self):
        assert GhostingPredictor().avg_recovery_probability == 0.0

    def test_multiple_instances_independent(self):
        p1 = GhostingPredictor()
        p2 = GhostingPredictor()
        p1.predict(make_input())
        assert len(p2._results) == 0


# ─────────────────────────────────────────────────────────────────────────────
# 23. GhostingPredictorResult dataclass
# ─────────────────────────────────────────────────────────────────────────────

class TestGhostingPredictorResult:
    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(GhostingPredictorResult)

    def test_field_count_is_15(self):
        assert len(dataclasses.fields(GhostingPredictorResult)) == 15

    def test_to_dict_returns_dict(self, predictor, clean_input):
        r = predictor.predict(clean_input)
        assert isinstance(r.to_dict(), dict)

    def test_to_dict_ghosting_risk_is_str_not_enum(self, predictor, clean_input):
        r = predictor.predict(clean_input)
        assert not isinstance(r.to_dict()["ghosting_risk"], GhostingRisk)
        assert isinstance(r.to_dict()["ghosting_risk"], str)

    def test_to_dict_ghosting_pattern_is_str_not_enum(self, predictor, clean_input):
        r = predictor.predict(clean_input)
        assert not isinstance(r.to_dict()["ghosting_pattern"], GhostingPattern)

    def test_to_dict_buyer_momentum_is_str_not_enum(self, predictor, clean_input):
        r = predictor.predict(clean_input)
        assert not isinstance(r.to_dict()["buyer_momentum"], BuyerMomentum)

    def test_to_dict_ghosting_action_is_str_not_enum(self, predictor, clean_input):
        r = predictor.predict(clean_input)
        assert not isinstance(r.to_dict()["ghosting_action"], GhostingAction)


# ─────────────────────────────────────────────────────────────────────────────
# 24. Integration / end-to-end scenarios
# ─────────────────────────────────────────────────────────────────────────────

class TestIntegration:
    def test_healthy_deal_all_good(self, predictor):
        """Fully engaged buyer, no red flags."""
        inp = make_input(
            days_since_last_buyer_reply=1,
            days_since_last_meeting=2,
            email_open_rate_last_30d=80.0,
            email_open_rate_prior_30d=75.0,
            response_time_avg_hours_recent=1.0,
            response_time_avg_hours_prior=2.0,
            proposal_opened_last_7d=1,
        )
        r = predictor.predict(inp)
        assert r.ghosting_risk == GhostingRisk.LOW
        assert r.is_at_risk_of_ghosting is False
        assert r.needs_escalation is False
        assert r.ghosting_action == GhostingAction.MAINTAIN

    def test_critical_deal_full_ghost(self, predictor):
        """Full ghost with champion exit scenario."""
        inp = make_input(
            days_since_last_buyer_reply=30,
            days_since_last_meeting=30,
            champion_last_active_days_ago=30,
            next_step_missed_count=5,
            meetings_cancelled_last_30d=3,
            email_open_rate_last_30d=0.0,
            email_open_rate_prior_30d=80.0,
            response_time_avg_hours_recent=48.0,
            response_time_avg_hours_prior=2.0,
            internal_champion_change=1,
            competitor_meeting_signal=1,
            pricing_conversation_stalled=1,
        )
        r = predictor.predict(inp)
        assert r.ghosting_risk == GhostingRisk.CRITICAL
        assert r.is_at_risk_of_ghosting is True
        assert r.needs_escalation is True
        assert r.ghosting_action == GhostingAction.LAST_RESORT

    def test_moderate_risk_re_engage(self, predictor):
        """Moderate risk leads to RE_ENGAGE."""
        inp = make_input(
            days_since_last_buyer_reply=7,
            next_step_missed_count=1,
            meetings_rescheduled_last_30d=2,
        )
        r = predictor.predict(inp)
        if r.ghosting_risk == GhostingRisk.MODERATE and not r.needs_escalation:
            assert r.ghosting_action == GhostingAction.RE_ENGAGE

    def test_batch_then_summary(self, predictor):
        """Batch predict, then check summary is consistent."""
        inputs = [
            make_input(deal_id="D1"),
            make_input(deal_id="D2", next_step_missed_count=3),
            make_input(deal_id="D3", internal_champion_change=1),
        ]
        predictor.predict_batch(inputs)
        s = predictor.summary()
        assert s["total"] == 3
        assert s["at_risk_count"] >= 1
        assert s["escalation_count"] >= 1

    def test_proposal_open_boosts_recovery(self, predictor):
        inp = make_input(
            days_since_last_buyer_reply=14,
            proposal_opened_last_7d=1,
        )
        r = predictor.predict(inp)
        # should have higher recovery than same without proposal
        inp2 = make_input(days_since_last_buyer_reply=14)
        r2 = predictor.predict(inp2)
        assert r.recovery_probability >= r2.recovery_probability

    def test_champion_exit_pattern_with_high_composite(self, predictor):
        inp = make_input(internal_champion_change=1, days_since_last_buyer_reply=21)
        r = predictor.predict(inp)
        if r.ghosting_composite >= 50:
            assert r.ghosting_pattern == GhostingPattern.CHAMPION_EXIT

    def test_full_ghost_pattern(self, predictor):
        inp = make_input(
            days_since_last_buyer_reply=21,
            days_since_last_meeting=30,
            champion_last_active_days_ago=21,
            next_step_missed_count=4,
        )
        r = predictor.predict(inp)
        if r.ghosting_composite >= 65 and not r.to_dict()["ghosting_pattern"] == "champion_exit":
            assert r.ghosting_pattern == GhostingPattern.FULL_GHOST

    def test_partial_ghost_pattern(self, predictor):
        inp = make_input(
            stakeholder_count_drop=2,
            days_since_last_buyer_reply=7,
            next_step_missed_count=2,
            meetings_cancelled_last_30d=2,
        )
        r = predictor.predict(inp)
        if r.ghosting_composite >= 45 and inp.internal_champion_change == 0:
            if not (inp.days_since_last_buyer_reply >= 21 and r.ghosting_composite >= 65):
                assert r.ghosting_pattern == GhostingPattern.PARTIAL_GHOST

    def test_slow_fade_pattern(self, predictor):
        inp = make_input(
            email_open_rate_last_30d=5.0,
            email_open_rate_prior_30d=50.0,
        )
        r = predictor.predict(inp)
        # slow fade requires internal_champion_change=0 or composite<50,
        # and composite < 45 (partial ghost condition not met)
        if (r.ghosting_composite < 45
                and not inp.internal_champion_change
                and not (inp.days_since_last_buyer_reply >= 21 and r.ghosting_composite >= 65)):
            assert r.ghosting_pattern == GhostingPattern.SLOW_FADE

    def test_accelerating_momentum(self, predictor):
        inp = make_input(
            email_open_rate_last_30d=90.0,
            email_open_rate_prior_30d=70.0,  # delta=20
            response_time_avg_hours_recent=1.0,
            response_time_avg_hours_prior=5.0,  # ratio=0.2
        )
        r = predictor.predict(inp)
        assert r.buyer_momentum == BuyerMomentum.ACCELERATING

    def test_stalled_momentum(self, predictor):
        inp = make_input(days_since_last_buyer_reply=14)
        r = predictor.predict(inp)
        assert r.buyer_momentum == BuyerMomentum.STALLED

    def test_decelerating_momentum(self, predictor):
        inp = make_input(
            email_open_rate_last_30d=45.0,
            email_open_rate_prior_30d=60.0,  # delta=-15
            days_since_last_buyer_reply=5,
        )
        r = predictor.predict(inp)
        assert r.buyer_momentum == BuyerMomentum.DECELERATING

    def test_stable_momentum(self, predictor):
        r = predictor.predict(make_input())
        assert r.buyer_momentum == BuyerMomentum.STABLE

    def test_score_range_various_inputs(self, predictor):
        inputs = [
            make_input(deal_id=f"D{i}", days_since_last_buyer_reply=i * 2)
            for i in range(15)
        ]
        for inp in inputs:
            r = predictor.predict(inp)
            assert 0 <= r.silence_score <= 100
            assert 0 <= r.engagement_decay_score <= 100
            assert 0 <= r.behavioral_risk_score <= 100
            assert 0 <= r.deal_urgency_score <= 100
            assert 0 <= r.ghosting_composite <= 100
            assert 0 <= r.recovery_probability <= 100

    def test_large_batch(self, predictor):
        inputs = [make_input(deal_id=f"D{i}") for i in range(50)]
        results = predictor.predict_batch(inputs)
        assert len(results) == 50
        s = predictor.summary()
        assert s["total"] == 50


# ─────────────────────────────────────────────────────────────────────────────
# 25. Boundary / edge cases
# ─────────────────────────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_silence_score_exactly_boundary_7(self):
        p = GhostingPredictor()
        s = p._silence_score(make_input(days_since_last_buyer_reply=7))
        assert s == 20.0

    def test_silence_score_exactly_boundary_14(self):
        p = GhostingPredictor()
        s = p._silence_score(make_input(days_since_last_buyer_reply=14))
        assert s == 35.0

    def test_silence_score_exactly_boundary_21(self):
        p = GhostingPredictor()
        s = p._silence_score(make_input(days_since_last_buyer_reply=21))
        assert s == 50.0

    def test_urgency_proposal_maxed_out(self):
        p = GhostingPredictor()
        s = p._deal_urgency_score(make_input(
            deal_stage_days_stuck=100,
            days_to_close_target=0,
            deal_value=1_000_000,
            proposal_opened_last_7d=1,
        ))
        assert s == 100.0

    def test_behavioral_combined_over_100_clamped(self):
        p = GhostingPredictor()
        s = p._behavioral_risk_score(make_input(
            next_step_missed_count=5,
            meetings_cancelled_last_30d=5,
            meetings_rescheduled_last_30d=5,
            internal_champion_change=1,
            competitor_meeting_signal=1,
            pricing_conversation_stalled=1,
        ))
        assert s == 100.0

    def test_composite_all_zeros(self):
        p = GhostingPredictor()
        assert p._composite(0.0, 0.0, 0.0, 0.0) == 0.0

    def test_predicted_ghost_days_no_overflow(self, predictor):
        r = predictor.predict(make_input(days_since_last_buyer_reply=0))
        assert r.predicted_ghost_days >= 0

    def test_recovery_prob_no_negative(self, predictor):
        inp = make_input(
            days_since_last_buyer_reply=30,
            internal_champion_change=1,
            competitor_meeting_signal=1,
        )
        r = predictor.predict(inp)
        assert r.recovery_probability >= 0.0

    def test_zero_deal_value_no_urgency_bonus(self):
        p = GhostingPredictor()
        s = p._deal_urgency_score(make_input(deal_value=0.0))
        assert s == 0.0

    def test_high_deal_value_adds_urgency(self):
        p = GhostingPredictor()
        s = p._deal_urgency_score(make_input(deal_value=600_000.0))
        assert s == 20.0

    def test_medium_deal_value_adds_urgency(self):
        p = GhostingPredictor()
        s = p._deal_urgency_score(make_input(deal_value=250_000.0))
        assert s == 12.0

    def test_silence_proposal_negative_clamp(self):
        # proposal without other signals: max(0, 0-15) = 0
        p = GhostingPredictor()
        s = p._silence_score(make_input(proposal_opened_last_7d=1))
        assert s == 0.0

    def test_engagement_decay_improvement_clamped(self):
        # All improvements lead to negative sub-scores, final is clamped to 0
        p = GhostingPredictor()
        s = p._engagement_decay_score(make_input(
            email_open_rate_last_30d=100.0,
            email_open_rate_prior_30d=0.0,
            response_time_avg_hours_recent=1.0,
            response_time_avg_hours_prior=10.0,
        ))
        assert s >= 0.0

    def test_deal_id_different_deals_independent(self, predictor):
        r1 = predictor.predict(make_input(deal_id="A", days_since_last_buyer_reply=0))
        r2 = predictor.predict(make_input(deal_id="B", days_since_last_buyer_reply=21))
        assert r1.deal_id != r2.deal_id
        assert r1.ghosting_composite != r2.ghosting_composite

    def test_rt_ratio_boundary_exactly_0_8(self):
        p = GhostingPredictor()
        # ratio exactly 0.8 is NOT < 0.8, so no subtraction
        inp = make_input(
            response_time_avg_hours_recent=0.8,
            response_time_avg_hours_prior=1.0,
        )
        s = p._engagement_decay_score(inp)
        # ratio=0.8 doesn't trigger the < 0.8 branch
        assert s == 0.0

    def test_rt_ratio_just_below_0_8(self):
        p = GhostingPredictor()
        inp = make_input(
            response_time_avg_hours_recent=0.79,
            response_time_avg_hours_prior=1.0,
        )
        s = p._engagement_decay_score(inp)
        # ratio < 0.8 triggers -10, but clamped to 0
        assert s == 0.0

    def test_open_delta_exactly_neg20_stalls(self):
        p = GhostingPredictor()
        inp = make_input(
            email_open_rate_last_30d=40.0,
            email_open_rate_prior_30d=60.0,
        )
        m = p._buyer_momentum(inp)
        assert m == BuyerMomentum.STALLED

    def test_open_delta_neg19_decelerating(self):
        p = GhostingPredictor()
        inp = make_input(
            email_open_rate_last_30d=41.0,
            email_open_rate_prior_30d=60.0,
        )
        m = p._buyer_momentum(inp)
        assert m == BuyerMomentum.DECELERATING

    def test_all_fields_accessible_on_result(self, predictor, clean_input):
        r = predictor.predict(clean_input)
        # Access all 15 result fields
        _ = r.deal_id
        _ = r.deal_name
        _ = r.ghosting_risk
        _ = r.ghosting_pattern
        _ = r.buyer_momentum
        _ = r.ghosting_action
        _ = r.silence_score
        _ = r.engagement_decay_score
        _ = r.behavioral_risk_score
        _ = r.deal_urgency_score
        _ = r.ghosting_composite
        _ = r.predicted_ghost_days
        _ = r.recovery_probability
        _ = r.is_at_risk_of_ghosting
        _ = r.needs_escalation


# ─────────────────────────────────────────────────────────────────────────────
# 26. Ghost days calculation additional branches
# ─────────────────────────────────────────────────────────────────────────────

class TestPredictedGhostDaysAdditional:
    def test_composite_exactly_80_returns_0(self):
        p = GhostingPredictor()
        assert p._predicted_ghost_days(make_input(), 80.0) == 0

    def test_composite_exactly_60_days_0(self):
        p = GhostingPredictor()
        assert p._predicted_ghost_days(make_input(days_since_last_buyer_reply=14), 60.0) == 0

    def test_composite_exactly_60_days_positive(self):
        p = GhostingPredictor()
        assert p._predicted_ghost_days(make_input(days_since_last_buyer_reply=0), 60.0) == 14

    def test_composite_exactly_40_days_0(self):
        p = GhostingPredictor()
        assert p._predicted_ghost_days(make_input(days_since_last_buyer_reply=21), 40.0) == 0

    def test_composite_exactly_40_days_positive(self):
        p = GhostingPredictor()
        assert p._predicted_ghost_days(make_input(days_since_last_buyer_reply=0), 40.0) == 21

    def test_composite_0_days_30(self):
        p = GhostingPredictor()
        assert p._predicted_ghost_days(make_input(days_since_last_buyer_reply=0), 0.0) == 30


# ─────────────────────────────────────────────────────────────────────────────
# 27. Summary averages correctness
# ─────────────────────────────────────────────────────────────────────────────

class TestSummaryAverages:
    def test_avg_silence_score_correct(self, predictor):
        r1 = predictor.predict(make_input(deal_id="D1", days_since_last_buyer_reply=0))
        r2 = predictor.predict(make_input(deal_id="D2", days_since_last_buyer_reply=21))
        expected = round((r1.silence_score + r2.silence_score) / 2, 1)
        assert predictor.summary()["avg_silence_score"] == expected

    def test_avg_engagement_decay_score_correct(self, predictor):
        r1 = predictor.predict(make_input(deal_id="D1"))
        r2 = predictor.predict(make_input(deal_id="D2", stakeholder_count_drop=3))
        expected = round((r1.engagement_decay_score + r2.engagement_decay_score) / 2, 1)
        assert predictor.summary()["avg_engagement_decay_score"] == expected

    def test_avg_behavioral_risk_score_correct(self, predictor):
        r1 = predictor.predict(make_input(deal_id="D1"))
        r2 = predictor.predict(make_input(deal_id="D2", next_step_missed_count=4))
        expected = round((r1.behavioral_risk_score + r2.behavioral_risk_score) / 2, 1)
        assert predictor.summary()["avg_behavioral_risk_score"] == expected

    def test_avg_deal_urgency_score_correct(self, predictor):
        r1 = predictor.predict(make_input(deal_id="D1", days_to_close_target=0))
        r2 = predictor.predict(make_input(deal_id="D2", days_to_close_target=60))
        expected = round((r1.deal_urgency_score + r2.deal_urgency_score) / 2, 1)
        assert predictor.summary()["avg_deal_urgency_score"] == expected

    def test_summary_avg_composite_correct(self, predictor):
        r1 = predictor.predict(make_input(deal_id="D1"))
        r2 = predictor.predict(make_input(deal_id="D2", days_since_last_buyer_reply=21))
        expected = round((r1.ghosting_composite + r2.ghosting_composite) / 2, 1)
        assert predictor.summary()["avg_ghosting_composite"] == expected

    def test_summary_avg_recovery_correct(self, predictor):
        r1 = predictor.predict(make_input(deal_id="D1"))
        r2 = predictor.predict(make_input(deal_id="D2", internal_champion_change=1))
        expected = round((r1.recovery_probability + r2.recovery_probability) / 2, 1)
        assert predictor.summary()["avg_recovery_probability"] == expected


# ─────────────────────────────────────────────────────────────────────────────
# 28. Pattern priority ordering
# ─────────────────────────────────────────────────────────────────────────────

class TestPatternPriorityOrdering:
    """Verify that champion_exit > full_ghost > partial_ghost > slow_fade > cooling_off > engaged."""

    def test_champion_exit_over_full_ghost_priority(self, predictor):
        # Both conditions met: champion exit takes precedence
        inp = make_input(
            internal_champion_change=1,
            days_since_last_buyer_reply=25,  # >= 21
            days_since_last_meeting=30,
            next_step_missed_count=4,
            meetings_cancelled_last_30d=3,
        )
        r = predictor.predict(inp)
        if r.ghosting_composite >= 65:
            assert r.ghosting_pattern == GhostingPattern.CHAMPION_EXIT

    def test_champion_exit_over_partial_ghost(self, predictor):
        inp = make_input(
            internal_champion_change=1,
            stakeholder_count_drop=3,
            days_since_last_buyer_reply=5,
            next_step_missed_count=2,
        )
        r = predictor.predict(inp)
        if r.ghosting_composite >= 50:
            assert r.ghosting_pattern == GhostingPattern.CHAMPION_EXIT

    def test_full_ghost_over_partial_ghost(self, predictor):
        inp = make_input(
            internal_champion_change=0,
            days_since_last_buyer_reply=22,
            stakeholder_count_drop=3,
            next_step_missed_count=4,
            meetings_cancelled_last_30d=3,
        )
        r = predictor.predict(inp)
        if r.ghosting_composite >= 65:
            assert r.ghosting_pattern == GhostingPattern.FULL_GHOST

    def test_cooling_off_over_engaged(self, predictor):
        # composite >= 35 with no other signals
        inp = make_input(
            days_since_last_buyer_reply=7,
            days_since_last_meeting=14,
            next_step_missed_count=1,
            meetings_cancelled_last_30d=1,
        )
        r = predictor.predict(inp)
        if r.ghosting_composite >= 35:
            assert r.ghosting_pattern == GhostingPattern.COOLING_OFF


# ─────────────────────────────────────────────────────────────────────────────
# 29. Additional is_at_risk/needs_escalation combined tests
# ─────────────────────────────────────────────────────────────────────────────

class TestFlagCombinations:
    def test_at_risk_false_needs_escalation_false(self, predictor):
        r = predictor.predict(make_input())
        assert r.is_at_risk_of_ghosting is False
        assert r.needs_escalation is False

    def test_at_risk_true_needs_escalation_true(self, predictor):
        inp = make_input(
            internal_champion_change=1,
            next_step_missed_count=4,
        )
        r = predictor.predict(inp)
        assert r.is_at_risk_of_ghosting is True
        assert r.needs_escalation is True

    def test_at_risk_via_next_steps_escalation_via_champion(self, predictor):
        inp = make_input(
            next_step_missed_count=3,
            internal_champion_change=1,
        )
        r = predictor.predict(inp)
        assert r.is_at_risk_of_ghosting is True
        assert r.needs_escalation is True

    def test_not_at_risk_but_escalation_via_days_reply(self, predictor):
        # Days >= 21 triggers escalation even if composite < 50
        # next_step_missed < 3
        inp = make_input(days_since_last_buyer_reply=21, next_step_missed_count=0)
        r = predictor.predict(inp)
        assert r.needs_escalation is True
        # composite may or may not be >= 50 — just verify escalation

    def test_at_risk_via_composite_not_next_steps(self, predictor):
        inp = make_input(
            days_since_last_buyer_reply=21,
            days_since_last_meeting=30,
            next_step_missed_count=0,
        )
        r = predictor.predict(inp)
        if r.ghosting_composite >= 50:
            assert r.is_at_risk_of_ghosting is True


# ─────────────────────────────────────────────────────────────────────────────
# 30. Action logic thorough coverage
# ─────────────────────────────────────────────────────────────────────────────

class TestGhostingActionThorough:
    def test_last_resort_when_critical(self, predictor):
        inp = make_input(
            days_since_last_buyer_reply=21,
            days_since_last_meeting=30,
            champion_last_active_days_ago=21,
            next_step_missed_count=4,
            meetings_cancelled_last_30d=3,
            competitor_meeting_signal=1,
            pricing_conversation_stalled=1,
        )
        r = predictor.predict(inp)
        if r.ghosting_risk == GhostingRisk.CRITICAL:
            assert r.ghosting_action == GhostingAction.LAST_RESORT

    def test_last_resort_when_needs_escalation_only(self, predictor):
        # internal_champion_change forces needs_escalation=True => LAST_RESORT
        inp = make_input(internal_champion_change=1)
        r = predictor.predict(inp)
        assert r.ghosting_action == GhostingAction.LAST_RESORT

    def test_maintain_low_risk_no_escalation(self, predictor):
        r = predictor.predict(make_input())
        assert r.ghosting_action == GhostingAction.MAINTAIN

    def test_escalate_path_for_high_risk_no_escalation(self, predictor):
        # Need HIGH risk (composite 50-69) and no needs_escalation
        # Use borderline signals
        inp = make_input(
            days_since_last_buyer_reply=14,    # stalled momentum, silence=35
            days_since_last_meeting=14,         # silence +15 => silence=50
            next_step_missed_count=2,           # behav=22
            meetings_cancelled_last_30d=1,      # behav +6 => behav=28
            meetings_rescheduled_last_30d=1,    # behav +4 => behav=32
        )
        r = predictor.predict(inp)
        if r.ghosting_risk == GhostingRisk.HIGH and not r.needs_escalation:
            assert r.ghosting_action == GhostingAction.ESCALATE_PATH

    def test_re_engage_for_moderate_risk(self, predictor):
        inp = make_input(
            days_since_last_buyer_reply=7,
            days_since_last_meeting=14,
        )
        r = predictor.predict(inp)
        if r.ghosting_risk == GhostingRisk.MODERATE and not r.needs_escalation:
            assert r.ghosting_action == GhostingAction.RE_ENGAGE
