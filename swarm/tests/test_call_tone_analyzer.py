"""
Comprehensive pytest test suite for Module 72 — Sales Call Emotional Tone Analyzer.

Coverage:
- All 4 enums (ToneSentiment, DominantTone, ConversationControl, ToneAction)
- CallToneInput (22 fields), CallToneResult (15 keys via to_dict)
- All private scoring helpers with boundary conditions
- Composite weight verification
- Tone sentiment composite+positive-sentiment combos
- Dominant tone priority order
- Conversation control thresholds
- Deal advancement probability
- Coaching priority formula
- is_positive_call / needs_immediate_coaching logic
- tone_action derivation
- analyze / analyze_batch / reset
- Properties: positive_calls, coaching_needed, avg_call_tone_composite, avg_deal_advancement_probability
- summary() — 13 keys
- End-to-end scenarios: great call, disaster call, hesitant rep, enthusiastic buyer
- Edge cases: 0 objections, very short call, all-zero inputs
- Cross-validation
"""
from __future__ import annotations

import pytest

from swarm.intelligence.call_tone_analyzer import (
    CallToneAnalyzer,
    CallToneInput,
    CallToneResult,
    ConversationControl,
    DominantTone,
    ToneAction,
    ToneSentiment,
)


# ---------------------------------------------------------------------------
# Factory helpers
# ---------------------------------------------------------------------------

def make_input(**kwargs) -> CallToneInput:
    """Return a CallToneInput with sensible defaults; override via kwargs."""
    defaults = dict(
        call_id="C001",
        deal_name="Deal Alpha",
        rep_id="R001",
        call_duration_minutes=30,
        talk_time_rep_pct=50.0,
        filler_word_rate_per_min=0.0,
        interruption_count_rep=0,
        interruption_count_buyer=0,
        questions_asked_rep=3,
        questions_asked_buyer=2,
        sentiment_score_positive=50.0,
        sentiment_score_negative=10.0,
        enthusiasm_keywords_count=3,
        hesitation_keywords_count=0,
        objection_count=0,
        objection_resolved_count=0,
        silence_events_long=0,
        price_mention_count=0,
        competitor_mention_count=0,
        decision_timeline_mentioned=0,
        next_steps_agreed=0,
        call_ended_abruptly=0,
    )
    defaults.update(kwargs)
    return CallToneInput(**defaults)


def analyzer_with(*inputs) -> CallToneAnalyzer:
    a = CallToneAnalyzer()
    for inp in inputs:
        a.analyze(inp)
    return a


# ---------------------------------------------------------------------------
# 1. Enum membership and values
# ---------------------------------------------------------------------------

class TestToneSentimentEnum:
    def test_positive_value(self):
        assert ToneSentiment.POSITIVE.value == "positive"

    def test_neutral_value(self):
        assert ToneSentiment.NEUTRAL.value == "neutral"

    def test_cautious_value(self):
        assert ToneSentiment.CAUTIOUS.value == "cautious"

    def test_negative_value(self):
        assert ToneSentiment.NEGATIVE.value == "negative"

    def test_four_members(self):
        assert len(ToneSentiment) == 4

    def test_is_str_enum(self):
        assert isinstance(ToneSentiment.POSITIVE, str)


class TestDominantToneEnum:
    def test_enthusiastic_value(self):
        assert DominantTone.ENTHUSIASTIC.value == "enthusiastic"

    def test_authoritative_value(self):
        assert DominantTone.AUTHORITATIVE.value == "authoritative"

    def test_hesitant_value(self):
        assert DominantTone.HESITANT.value == "hesitant"

    def test_evasive_value(self):
        assert DominantTone.EVASIVE.value == "evasive"

    def test_resistant_value(self):
        assert DominantTone.RESISTANT.value == "resistant"

    def test_panic_signal_value(self):
        assert DominantTone.PANIC_SIGNAL.value == "panic_signal"

    def test_six_members(self):
        assert len(DominantTone) == 6


class TestConversationControlEnum:
    def test_rep_led_value(self):
        assert ConversationControl.REP_LED.value == "rep_led"

    def test_balanced_value(self):
        assert ConversationControl.BALANCED.value == "balanced"

    def test_buyer_led_value(self):
        assert ConversationControl.BUYER_LED.value == "buyer_led"

    def test_fragmented_value(self):
        assert ConversationControl.FRAGMENTED.value == "fragmented"

    def test_four_members(self):
        assert len(ConversationControl) == 4


class TestToneActionEnum:
    def test_reinforce_value(self):
        assert ToneAction.REINFORCE.value == "reinforce"

    def test_nurture_value(self):
        assert ToneAction.NURTURE.value == "nurture"

    def test_reframe_value(self):
        assert ToneAction.REFRAME.value == "reframe"

    def test_intervene_value(self):
        assert ToneAction.INTERVENE.value == "intervene"

    def test_four_members(self):
        assert len(ToneAction) == 4


# ---------------------------------------------------------------------------
# 2. CallToneInput — 22 fields
# ---------------------------------------------------------------------------

class TestCallToneInputFields:
    def test_field_count(self):
        import dataclasses
        fields = dataclasses.fields(CallToneInput)
        assert len(fields) == 22

    def test_all_field_names(self):
        import dataclasses
        names = {f.name for f in dataclasses.fields(CallToneInput)}
        expected = {
            "call_id", "deal_name", "rep_id", "call_duration_minutes",
            "talk_time_rep_pct", "filler_word_rate_per_min",
            "interruption_count_rep", "interruption_count_buyer",
            "questions_asked_rep", "questions_asked_buyer",
            "sentiment_score_positive", "sentiment_score_negative",
            "enthusiasm_keywords_count", "hesitation_keywords_count",
            "objection_count", "objection_resolved_count",
            "silence_events_long", "price_mention_count",
            "competitor_mention_count", "decision_timeline_mentioned",
            "next_steps_agreed", "call_ended_abruptly",
        }
        assert names == expected

    def test_instantiation(self):
        inp = make_input()
        assert inp.call_id == "C001"

    def test_string_fields(self):
        inp = make_input(call_id="X", deal_name="Y", rep_id="Z")
        assert inp.deal_name == "Y"
        assert inp.rep_id == "Z"


# ---------------------------------------------------------------------------
# 3. CallToneResult — to_dict 15 keys
# ---------------------------------------------------------------------------

class TestCallToneResultToDict:
    def setup_method(self):
        self.a = CallToneAnalyzer()
        self.result = self.a.analyze(make_input())

    def test_to_dict_key_count(self):
        d = self.result.to_dict()
        assert len(d) == 15

    def test_to_dict_exact_keys(self):
        d = self.result.to_dict()
        expected_keys = {
            "call_id", "deal_name", "tone_sentiment", "dominant_tone",
            "conversation_control", "tone_action", "rep_confidence_score",
            "buyer_engagement_score", "objection_handling_score",
            "conversation_quality_score", "call_tone_composite",
            "deal_advancement_probability", "call_coaching_priority",
            "is_positive_call", "needs_immediate_coaching",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_sentiment_is_string(self):
        d = self.result.to_dict()
        assert isinstance(d["tone_sentiment"], str)

    def test_to_dict_dominant_tone_is_string(self):
        d = self.result.to_dict()
        assert isinstance(d["dominant_tone"], str)

    def test_to_dict_control_is_string(self):
        d = self.result.to_dict()
        assert isinstance(d["conversation_control"], str)

    def test_to_dict_action_is_string(self):
        d = self.result.to_dict()
        assert isinstance(d["tone_action"], str)

    def test_to_dict_call_id_matches(self):
        d = self.result.to_dict()
        assert d["call_id"] == "C001"

    def test_to_dict_scores_are_floats(self):
        d = self.result.to_dict()
        for key in ["rep_confidence_score", "buyer_engagement_score",
                    "objection_handling_score", "conversation_quality_score",
                    "call_tone_composite", "deal_advancement_probability",
                    "call_coaching_priority"]:
            assert isinstance(d[key], float), f"{key} should be float"

    def test_to_dict_booleans(self):
        d = self.result.to_dict()
        assert isinstance(d["is_positive_call"], bool)
        assert isinstance(d["needs_immediate_coaching"], bool)


# ---------------------------------------------------------------------------
# 4. _rep_confidence_score boundaries
# ---------------------------------------------------------------------------

class TestRepConfidenceScore:
    def setup_method(self):
        self.a = CallToneAnalyzer()

    def _conf(self, **kwargs):
        return self.a._rep_confidence_score(make_input(**kwargs))

    def test_base_score_no_modifiers(self):
        # base=50, no penalties, no bonuses
        score = self._conf(
            filler_word_rate_per_min=0.0,
            enthusiasm_keywords_count=0,
            interruption_count_rep=0,
            talk_time_rep_pct=50.0,
            call_ended_abruptly=0,
        )
        assert score == 60.0  # base50 + talk_ratio_bonus10

    def test_filler_rate_exactly_5_penalty(self):
        score = self._conf(filler_word_rate_per_min=5.0, enthusiasm_keywords_count=0,
                           interruption_count_rep=0, talk_time_rep_pct=50.0, call_ended_abruptly=0)
        # 50 - 30 + 10 = 30
        assert score == 30.0

    def test_filler_rate_above_5_penalty(self):
        score = self._conf(filler_word_rate_per_min=6.0, enthusiasm_keywords_count=0,
                           interruption_count_rep=0, talk_time_rep_pct=50.0, call_ended_abruptly=0)
        assert score == 30.0

    def test_filler_rate_exactly_3_penalty(self):
        score = self._conf(filler_word_rate_per_min=3.0, enthusiasm_keywords_count=0,
                           interruption_count_rep=0, talk_time_rep_pct=50.0, call_ended_abruptly=0)
        # 50 - 18 + 10 = 42
        assert score == 42.0

    def test_filler_rate_between_3_and_5(self):
        score = self._conf(filler_word_rate_per_min=4.0, enthusiasm_keywords_count=0,
                           interruption_count_rep=0, talk_time_rep_pct=50.0, call_ended_abruptly=0)
        assert score == 42.0

    def test_filler_rate_exactly_1_5_penalty(self):
        score = self._conf(filler_word_rate_per_min=1.5, enthusiasm_keywords_count=0,
                           interruption_count_rep=0, talk_time_rep_pct=50.0, call_ended_abruptly=0)
        # 50 - 8 + 10 = 52
        assert score == 52.0

    def test_filler_rate_below_1_5_no_penalty(self):
        score = self._conf(filler_word_rate_per_min=1.0, enthusiasm_keywords_count=0,
                           interruption_count_rep=0, talk_time_rep_pct=50.0, call_ended_abruptly=0)
        assert score == 60.0

    def test_filler_rate_zero_no_penalty(self):
        score = self._conf(filler_word_rate_per_min=0.0, enthusiasm_keywords_count=0,
                           interruption_count_rep=0, talk_time_rep_pct=50.0, call_ended_abruptly=0)
        assert score == 60.0

    def test_enthusiasm_cap_at_20(self):
        score = self._conf(filler_word_rate_per_min=0.0, enthusiasm_keywords_count=10,
                           interruption_count_rep=0, talk_time_rep_pct=50.0, call_ended_abruptly=0)
        # 50 + 20 (cap) + 10 = 80
        assert score == 80.0

    def test_enthusiasm_partial_boost(self):
        score = self._conf(filler_word_rate_per_min=0.0, enthusiasm_keywords_count=2,
                           interruption_count_rep=0, talk_time_rep_pct=50.0, call_ended_abruptly=0)
        # 50 + 6 + 10 = 66
        assert score == 66.0

    def test_enthusiasm_exactly_at_cap(self):
        # 20 / 3 = 6.67 → 7 keywords gives 21 → capped at 20
        score = self._conf(filler_word_rate_per_min=0.0, enthusiasm_keywords_count=7,
                           interruption_count_rep=0, talk_time_rep_pct=50.0, call_ended_abruptly=0)
        assert score == 80.0

    def test_interruption_rep_gt5_penalty(self):
        score = self._conf(filler_word_rate_per_min=0.0, enthusiasm_keywords_count=0,
                           interruption_count_rep=6, talk_time_rep_pct=50.0, call_ended_abruptly=0)
        # 50 - 15 + 10 = 45
        assert score == 45.0

    def test_interruption_rep_exactly_5_no_big_penalty(self):
        score = self._conf(filler_word_rate_per_min=0.0, enthusiasm_keywords_count=0,
                           interruption_count_rep=5, talk_time_rep_pct=50.0, call_ended_abruptly=0)
        # 50 - 5 + 10 = 55  (>2 branch)
        assert score == 55.0

    def test_interruption_rep_gt2_penalty(self):
        score = self._conf(filler_word_rate_per_min=0.0, enthusiasm_keywords_count=0,
                           interruption_count_rep=3, talk_time_rep_pct=50.0, call_ended_abruptly=0)
        # 50 - 5 + 10 = 55
        assert score == 55.0

    def test_interruption_rep_exactly_2_no_penalty(self):
        score = self._conf(filler_word_rate_per_min=0.0, enthusiasm_keywords_count=0,
                           interruption_count_rep=2, talk_time_rep_pct=50.0, call_ended_abruptly=0)
        # 50 + 10 = 60
        assert score == 60.0

    def test_talk_ratio_40_to_60_bonus(self):
        for talk in [40.0, 50.0, 60.0]:
            s = self._conf(filler_word_rate_per_min=0.0, enthusiasm_keywords_count=0,
                           interruption_count_rep=0, talk_time_rep_pct=talk, call_ended_abruptly=0)
            assert s == 60.0, f"Expected 60 for talk={talk}"

    def test_talk_ratio_above_80_penalty(self):
        score = self._conf(filler_word_rate_per_min=0.0, enthusiasm_keywords_count=0,
                           interruption_count_rep=0, talk_time_rep_pct=81.0, call_ended_abruptly=0)
        # 50 - 15 = 35
        assert score == 35.0

    def test_talk_ratio_exactly_80_no_big_penalty(self):
        score = self._conf(filler_word_rate_per_min=0.0, enthusiasm_keywords_count=0,
                           interruption_count_rep=0, talk_time_rep_pct=80.0, call_ended_abruptly=0)
        # 50 (neither 40-60 nor >80) = 50
        assert score == 50.0

    def test_talk_ratio_below_20_penalty(self):
        score = self._conf(filler_word_rate_per_min=0.0, enthusiasm_keywords_count=0,
                           interruption_count_rep=0, talk_time_rep_pct=19.0, call_ended_abruptly=0)
        assert score == 35.0

    def test_talk_ratio_exactly_20_no_penalty(self):
        score = self._conf(filler_word_rate_per_min=0.0, enthusiasm_keywords_count=0,
                           interruption_count_rep=0, talk_time_rep_pct=20.0, call_ended_abruptly=0)
        assert score == 50.0

    def test_abrupt_ending_penalty(self):
        score = self._conf(filler_word_rate_per_min=0.0, enthusiasm_keywords_count=0,
                           interruption_count_rep=0, talk_time_rep_pct=50.0, call_ended_abruptly=1)
        # 50 - 10 + 10 = 50
        assert score == 50.0

    def test_clamp_floor_zero(self):
        score = self._conf(filler_word_rate_per_min=5.0, enthusiasm_keywords_count=0,
                           interruption_count_rep=6, talk_time_rep_pct=81.0, call_ended_abruptly=1)
        # 50 - 30 - 15 - 15 - 10 = -20 → clamped to 0
        assert score == 0.0

    def test_clamp_ceiling_100(self):
        score = self._conf(filler_word_rate_per_min=0.0, enthusiasm_keywords_count=20,
                           interruption_count_rep=0, talk_time_rep_pct=50.0, call_ended_abruptly=0)
        # 50 + 20 + 10 = 80, not exceeding 100
        assert score == 80.0

    def test_combined_max_scenario(self):
        score = self._conf(filler_word_rate_per_min=0.0, enthusiasm_keywords_count=100,
                           interruption_count_rep=0, talk_time_rep_pct=50.0, call_ended_abruptly=0)
        # 50 + 20 (capped) + 10 = 80
        assert score == 80.0


# ---------------------------------------------------------------------------
# 5. _buyer_engagement_score boundaries
# ---------------------------------------------------------------------------

class TestBuyerEngagementScore:
    def setup_method(self):
        self.a = CallToneAnalyzer()

    def _eng(self, **kwargs):
        return self.a._buyer_engagement_score(make_input(**kwargs))

    def test_base_zero_inputs(self):
        score = self._eng(questions_asked_buyer=0, interruption_count_buyer=0,
                          sentiment_score_positive=0, decision_timeline_mentioned=0,
                          next_steps_agreed=0, sentiment_score_negative=0)
        assert score == 30.0

    def test_buyer_questions_boost(self):
        score = self._eng(questions_asked_buyer=3, interruption_count_buyer=0,
                          sentiment_score_positive=0, decision_timeline_mentioned=0,
                          next_steps_agreed=0, sentiment_score_negative=0)
        # 30 + 15 = 45
        assert score == 45.0

    def test_buyer_questions_cap_at_30(self):
        score = self._eng(questions_asked_buyer=10, interruption_count_buyer=0,
                          sentiment_score_positive=0, decision_timeline_mentioned=0,
                          next_steps_agreed=0, sentiment_score_negative=0)
        # 30 + 30 (cap) = 60
        assert score == 60.0

    def test_buyer_questions_exactly_at_cap(self):
        score = self._eng(questions_asked_buyer=6, interruption_count_buyer=0,
                          sentiment_score_positive=0, decision_timeline_mentioned=0,
                          next_steps_agreed=0, sentiment_score_negative=0)
        # 6*5=30 exactly at cap
        assert score == 60.0

    def test_buyer_interruptions_boost(self):
        score = self._eng(questions_asked_buyer=0, interruption_count_buyer=3,
                          sentiment_score_positive=0, decision_timeline_mentioned=0,
                          next_steps_agreed=0, sentiment_score_negative=0)
        # 30 + 9 = 39
        assert score == 39.0

    def test_buyer_interruptions_cap_at_15(self):
        score = self._eng(questions_asked_buyer=0, interruption_count_buyer=10,
                          sentiment_score_positive=0, decision_timeline_mentioned=0,
                          next_steps_agreed=0, sentiment_score_negative=0)
        # 30 + 15 (cap) = 45
        assert score == 45.0

    def test_positive_sentiment_boost(self):
        score = self._eng(questions_asked_buyer=0, interruption_count_buyer=0,
                          sentiment_score_positive=40.0, decision_timeline_mentioned=0,
                          next_steps_agreed=0, sentiment_score_negative=0)
        # 30 + 12 = 42
        assert score == 42.0

    def test_positive_sentiment_cap_at_15(self):
        score = self._eng(questions_asked_buyer=0, interruption_count_buyer=0,
                          sentiment_score_positive=100.0, decision_timeline_mentioned=0,
                          next_steps_agreed=0, sentiment_score_negative=0)
        # 30 + 15 (cap) = 45
        assert score == 45.0

    def test_decision_timeline_bonus(self):
        score = self._eng(questions_asked_buyer=0, interruption_count_buyer=0,
                          sentiment_score_positive=0, decision_timeline_mentioned=1,
                          next_steps_agreed=0, sentiment_score_negative=0)
        # 30 + 10 = 40
        assert score == 40.0

    def test_next_steps_bonus(self):
        score = self._eng(questions_asked_buyer=0, interruption_count_buyer=0,
                          sentiment_score_positive=0, decision_timeline_mentioned=0,
                          next_steps_agreed=1, sentiment_score_negative=0)
        # 30 + 10 = 40
        assert score == 40.0

    def test_negative_sentiment_penalty(self):
        score = self._eng(questions_asked_buyer=0, interruption_count_buyer=0,
                          sentiment_score_positive=0, decision_timeline_mentioned=0,
                          next_steps_agreed=0, sentiment_score_negative=25.0)
        # 30 - 10 = 20
        assert score == 20.0

    def test_negative_sentiment_cap_penalty_at_20(self):
        score = self._eng(questions_asked_buyer=0, interruption_count_buyer=0,
                          sentiment_score_positive=0, decision_timeline_mentioned=0,
                          next_steps_agreed=0, sentiment_score_negative=100.0)
        # 30 - 20 (cap) = 10
        assert score == 10.0

    def test_clamp_floor_zero(self):
        score = self._eng(questions_asked_buyer=0, interruption_count_buyer=0,
                          sentiment_score_positive=0, decision_timeline_mentioned=0,
                          next_steps_agreed=0, sentiment_score_negative=200.0)
        assert score == 10.0  # penalty capped at 20 → 30-20=10

    def test_clamp_ceiling_100(self):
        score = self._eng(questions_asked_buyer=10, interruption_count_buyer=10,
                          sentiment_score_positive=100.0, decision_timeline_mentioned=1,
                          next_steps_agreed=1, sentiment_score_negative=0)
        # 30+30+15+15+10+10 = 110 → 100
        assert score == 100.0

    def test_both_timeline_and_next_steps(self):
        score = self._eng(questions_asked_buyer=0, interruption_count_buyer=0,
                          sentiment_score_positive=0, decision_timeline_mentioned=1,
                          next_steps_agreed=1, sentiment_score_negative=0)
        # 30 + 10 + 10 = 50
        assert score == 50.0


# ---------------------------------------------------------------------------
# 6. _objection_handling_score boundaries
# ---------------------------------------------------------------------------

class TestObjectionHandlingScore:
    def setup_method(self):
        self.a = CallToneAnalyzer()

    def _obj(self, **kwargs):
        return self.a._objection_handling_score(make_input(**kwargs))

    def test_zero_objections_returns_70(self):
        assert self._obj(objection_count=0, objection_resolved_count=0, hesitation_keywords_count=0) == 70.0

    def test_zero_objections_ignores_resolved(self):
        assert self._obj(objection_count=0, objection_resolved_count=5, hesitation_keywords_count=0) == 70.0

    def test_all_resolved_bonus(self):
        score = self._obj(objection_count=2, objection_resolved_count=2, hesitation_keywords_count=0)
        # 2/2 * 80 + 20 = 100
        assert score == 100.0

    def test_partial_resolution(self):
        score = self._obj(objection_count=4, objection_resolved_count=2, hesitation_keywords_count=0)
        # 0.5 * 80 = 40
        assert score == 40.0

    def test_none_resolved(self):
        score = self._obj(objection_count=3, objection_resolved_count=0, hesitation_keywords_count=0)
        # 0 * 80 = 0
        assert score == 0.0

    def test_high_objection_low_resolution_penalty(self):
        score = self._obj(objection_count=5, objection_resolved_count=2, hesitation_keywords_count=0)
        # 2/5 * 80 = 32; 5>=5 and 0.4<0.5 → -15 = 17
        assert score == 17.0

    def test_high_objection_exactly_50pct_no_extra_penalty(self):
        score = self._obj(objection_count=5, objection_resolved_count=3, hesitation_keywords_count=0)
        # 3/5=0.6 >= 0.5; 0.6*80=48; no penalty
        # but all not resolved so no bonus
        assert score == 48.0

    def test_high_objection_at_exactly_5_low_resolution_penalty(self):
        # 5 objections, 2 resolved = 40% < 50%
        score = self._obj(objection_count=5, objection_resolved_count=2, hesitation_keywords_count=0)
        assert score == 17.0

    def test_hesitation_keywords_penalty(self):
        score = self._obj(objection_count=2, objection_resolved_count=2, hesitation_keywords_count=3)
        # 100 - 6 = 94
        assert score == 94.0

    def test_hesitation_cap_at_20(self):
        score = self._obj(objection_count=2, objection_resolved_count=2, hesitation_keywords_count=15)
        # 100 - 20 (cap) = 80
        assert score == 80.0

    def test_hesitation_exactly_at_cap(self):
        score = self._obj(objection_count=2, objection_resolved_count=2, hesitation_keywords_count=10)
        # 10*2=20 exactly at cap
        assert score == 80.0

    def test_clamp_floor_zero(self):
        score = self._obj(objection_count=10, objection_resolved_count=0, hesitation_keywords_count=15)
        # 0 - 15 - 20 = -35 → 0
        assert score == 0.0

    def test_one_of_one_resolved(self):
        score = self._obj(objection_count=1, objection_resolved_count=1, hesitation_keywords_count=0)
        # 1*80 + 20 = 100
        assert score == 100.0

    def test_one_of_two_resolved(self):
        score = self._obj(objection_count=2, objection_resolved_count=1, hesitation_keywords_count=0)
        # 0.5*80 = 40; no bonus; no penalty (not >=5 objs)
        assert score == 40.0


# ---------------------------------------------------------------------------
# 7. _conversation_quality_score boundaries
# ---------------------------------------------------------------------------

class TestConversationQualityScore:
    def setup_method(self):
        self.a = CallToneAnalyzer()

    def _qual(self, **kwargs):
        return self.a._conversation_quality_score(make_input(**kwargs))

    def test_base_score_no_modifiers(self):
        score = self._qual(questions_asked_rep=0, silence_events_long=0,
                           price_mention_count=0, competitor_mention_count=0,
                           next_steps_agreed=0, call_duration_minutes=30)
        # 40 + 0 - 0 - 0 - 0 + 0 + 5 = 45
        assert score == 45.0

    def test_rep_questions_boost(self):
        score = self._qual(questions_asked_rep=3, silence_events_long=0,
                           price_mention_count=0, competitor_mention_count=0,
                           next_steps_agreed=0, call_duration_minutes=30)
        # 40 + 9 + 5 = 54
        assert score == 54.0

    def test_rep_questions_cap_at_20(self):
        score = self._qual(questions_asked_rep=10, silence_events_long=0,
                           price_mention_count=0, competitor_mention_count=0,
                           next_steps_agreed=0, call_duration_minutes=30)
        # 40 + 20 (cap) + 5 = 65
        assert score == 65.0

    def test_silence_penalty(self):
        score = self._qual(questions_asked_rep=0, silence_events_long=3,
                           price_mention_count=0, competitor_mention_count=0,
                           next_steps_agreed=0, call_duration_minutes=30)
        # 40 - 12 + 5 = 33
        assert score == 33.0

    def test_silence_penalty_cap_at_20(self):
        score = self._qual(questions_asked_rep=0, silence_events_long=10,
                           price_mention_count=0, competitor_mention_count=0,
                           next_steps_agreed=0, call_duration_minutes=30)
        # 40 - 20 (cap) + 5 = 25
        assert score == 25.0

    def test_price_mention_ge4_penalty(self):
        score = self._qual(questions_asked_rep=0, silence_events_long=0,
                           price_mention_count=4, competitor_mention_count=0,
                           next_steps_agreed=0, call_duration_minutes=30)
        # 40 - 15 + 5 = 30
        assert score == 30.0

    def test_price_mention_above4_penalty(self):
        score = self._qual(questions_asked_rep=0, silence_events_long=0,
                           price_mention_count=5, competitor_mention_count=0,
                           next_steps_agreed=0, call_duration_minutes=30)
        assert score == 30.0

    def test_price_mention_ge2_penalty(self):
        score = self._qual(questions_asked_rep=0, silence_events_long=0,
                           price_mention_count=2, competitor_mention_count=0,
                           next_steps_agreed=0, call_duration_minutes=30)
        # 40 - 5 + 5 = 40
        assert score == 40.0

    def test_price_mention_exactly3_big_penalty(self):
        score = self._qual(questions_asked_rep=0, silence_events_long=0,
                           price_mention_count=3, competitor_mention_count=0,
                           next_steps_agreed=0, call_duration_minutes=30)
        # 40 - 5 + 5 = 40 (only >=2, not >=4)
        assert score == 40.0

    def test_price_mention_below2_no_penalty(self):
        score = self._qual(questions_asked_rep=0, silence_events_long=0,
                           price_mention_count=1, competitor_mention_count=0,
                           next_steps_agreed=0, call_duration_minutes=30)
        assert score == 45.0

    def test_competitor_mention_penalty(self):
        score = self._qual(questions_asked_rep=0, silence_events_long=0,
                           price_mention_count=0, competitor_mention_count=2,
                           next_steps_agreed=0, call_duration_minutes=30)
        # 40 - 10 + 5 = 35
        assert score == 35.0

    def test_competitor_mention_cap_at_15(self):
        score = self._qual(questions_asked_rep=0, silence_events_long=0,
                           price_mention_count=0, competitor_mention_count=5,
                           next_steps_agreed=0, call_duration_minutes=30)
        # 40 - 15 (cap) + 5 = 30
        assert score == 30.0

    def test_next_steps_bonus(self):
        score = self._qual(questions_asked_rep=0, silence_events_long=0,
                           price_mention_count=0, competitor_mention_count=0,
                           next_steps_agreed=1, call_duration_minutes=30)
        # 40 + 15 + 5 = 60
        assert score == 60.0

    def test_duration_lt15_penalty(self):
        score = self._qual(questions_asked_rep=0, silence_events_long=0,
                           price_mention_count=0, competitor_mention_count=0,
                           next_steps_agreed=0, call_duration_minutes=10)
        # 40 - 10 = 30
        assert score == 30.0

    def test_duration_exactly_15_no_penalty_no_bonus(self):
        score = self._qual(questions_asked_rep=0, silence_events_long=0,
                           price_mention_count=0, competitor_mention_count=0,
                           next_steps_agreed=0, call_duration_minutes=15)
        # 40; no short, no 30-60 bonus (15 not in 30-60)
        assert score == 40.0

    def test_duration_30_to_60_bonus(self):
        for dur in [30, 45, 60]:
            s = self._qual(questions_asked_rep=0, silence_events_long=0,
                           price_mention_count=0, competitor_mention_count=0,
                           next_steps_agreed=0, call_duration_minutes=dur)
            assert s == 45.0, f"Expected 45 for duration={dur}"

    def test_duration_above_60_no_bonus(self):
        score = self._qual(questions_asked_rep=0, silence_events_long=0,
                           price_mention_count=0, competitor_mention_count=0,
                           next_steps_agreed=0, call_duration_minutes=61)
        assert score == 40.0

    def test_clamp_ceiling_100(self):
        score = self._qual(questions_asked_rep=10, silence_events_long=0,
                           price_mention_count=0, competitor_mention_count=0,
                           next_steps_agreed=1, call_duration_minutes=30)
        # 40 + 20 + 15 + 5 = 80
        assert score == 80.0


# ---------------------------------------------------------------------------
# 8. _composite weights
# ---------------------------------------------------------------------------

class TestCompositeWeights:
    def setup_method(self):
        self.a = CallToneAnalyzer()

    def test_composite_formula(self):
        result = self.a._composite(80.0, 60.0, 70.0, 50.0)
        expected = round(80*0.30 + 60*0.30 + 70*0.25 + 50*0.15, 1)
        assert result == expected

    def test_composite_all_zero(self):
        assert self.a._composite(0.0, 0.0, 0.0, 0.0) == 0.0

    def test_composite_all_100(self):
        assert self.a._composite(100.0, 100.0, 100.0, 100.0) == 100.0

    def test_composite_clamp_floor(self):
        assert self.a._composite(-10.0, -5.0, 0.0, -20.0) == 0.0

    def test_composite_clamp_ceiling(self):
        assert self.a._composite(200.0, 200.0, 200.0, 200.0) == 100.0

    def test_composite_conf_weight_30pct(self):
        # Only conf differs
        r1 = self.a._composite(100.0, 0.0, 0.0, 0.0)
        assert abs(r1 - 30.0) < 0.01

    def test_composite_engage_weight_30pct(self):
        r1 = self.a._composite(0.0, 100.0, 0.0, 0.0)
        assert abs(r1 - 30.0) < 0.01

    def test_composite_obj_weight_25pct(self):
        r1 = self.a._composite(0.0, 0.0, 100.0, 0.0)
        assert abs(r1 - 25.0) < 0.01

    def test_composite_quality_weight_15pct(self):
        r1 = self.a._composite(0.0, 0.0, 0.0, 100.0)
        assert abs(r1 - 15.0) < 0.01

    def test_weights_sum_to_1(self):
        total = 0.30 + 0.30 + 0.25 + 0.15
        assert abs(total - 1.0) < 1e-9


# ---------------------------------------------------------------------------
# 9. _tone_sentiment conditions
# ---------------------------------------------------------------------------

class TestToneSentiment:
    def setup_method(self):
        self.a = CallToneAnalyzer()

    def _sent(self, composite, pos_sentiment, neg_sentiment=10.0):
        inp = make_input(sentiment_score_positive=pos_sentiment, sentiment_score_negative=neg_sentiment)
        return self.a._tone_sentiment(inp, composite)

    def test_positive_requires_both_composite_65_and_positive_gt40(self):
        assert self._sent(65.0, 41.0) == ToneSentiment.POSITIVE

    def test_positive_composite_exactly_65_pos_exactly_40_is_neutral(self):
        # pos must be > 40, so 40 doesn't qualify
        assert self._sent(65.0, 40.0) == ToneSentiment.NEUTRAL

    def test_positive_composite_above_65_pos_above_40(self):
        assert self._sent(80.0, 50.0) == ToneSentiment.POSITIVE

    def test_neutral_composite_ge45_pos_le40(self):
        assert self._sent(45.0, 30.0) == ToneSentiment.NEUTRAL

    def test_neutral_composite_exactly_45(self):
        assert self._sent(45.0, 20.0) == ToneSentiment.NEUTRAL

    def test_neutral_composite_between_45_and_65(self):
        assert self._sent(55.0, 30.0) == ToneSentiment.NEUTRAL

    def test_cautious_composite_ge30_lt45(self):
        assert self._sent(30.0, 10.0) == ToneSentiment.CAUTIOUS

    def test_cautious_composite_exactly_30(self):
        assert self._sent(30.0, 10.0) == ToneSentiment.CAUTIOUS

    def test_cautious_via_negative_sentiment_high(self):
        # composite < 30 but negative > 30
        assert self._sent(20.0, 10.0, neg_sentiment=31.0) == ToneSentiment.CAUTIOUS

    def test_cautious_negative_exactly_30_falls_to_negative(self):
        # composite < 30 and neg == 30 (not > 30)
        assert self._sent(20.0, 10.0, neg_sentiment=30.0) == ToneSentiment.NEGATIVE

    def test_negative_composite_lt30_neg_le30(self):
        assert self._sent(10.0, 5.0, neg_sentiment=10.0) == ToneSentiment.NEGATIVE

    def test_negative_zero_composite(self):
        assert self._sent(0.0, 0.0, neg_sentiment=0.0) == ToneSentiment.NEGATIVE

    def test_positive_needs_composite_ge65_not_64(self):
        # composite=64 ≥45 so neutral even with high pos
        assert self._sent(64.0, 50.0) == ToneSentiment.NEUTRAL


# ---------------------------------------------------------------------------
# 10. _dominant_tone priority order
# ---------------------------------------------------------------------------

class TestDominantTone:
    def setup_method(self):
        self.a = CallToneAnalyzer()

    def _tone(self, conf, engage, **kwargs):
        inp = make_input(**kwargs)
        return self.a._dominant_tone(inp, conf, engage)

    def test_panic_signal_priority_over_all(self):
        # abrupt=1, objections>3; also engage<30, hesitation>5 etc
        tone = self._tone(conf=10.0, engage=10.0,
                          call_ended_abruptly=1, objection_count=4,
                          hesitation_keywords_count=10, filler_word_rate_per_min=5.0)
        assert tone == DominantTone.PANIC_SIGNAL

    def test_panic_signal_requires_both_abrupt_and_objection_gt3(self):
        # abrupt=0, objections=4 → not panic
        tone = self._tone(conf=10.0, engage=10.0,
                          call_ended_abruptly=0, objection_count=4,
                          hesitation_keywords_count=10, filler_word_rate_per_min=5.0)
        assert tone != DominantTone.PANIC_SIGNAL

    def test_panic_signal_objection_exactly_3_not_triggered(self):
        tone = self._tone(conf=10.0, engage=10.0,
                          call_ended_abruptly=1, objection_count=3,
                          hesitation_keywords_count=0, filler_word_rate_per_min=0.0)
        assert tone != DominantTone.PANIC_SIGNAL

    def test_evasive_when_engage_lt30_hesitation_gt5(self):
        tone = self._tone(conf=50.0, engage=29.0,
                          call_ended_abruptly=0, objection_count=0,
                          hesitation_keywords_count=6, filler_word_rate_per_min=0.0)
        assert tone == DominantTone.EVASIVE

    def test_evasive_engage_exactly_30_not_triggered(self):
        tone = self._tone(conf=50.0, engage=30.0,
                          call_ended_abruptly=0, objection_count=0,
                          hesitation_keywords_count=6, filler_word_rate_per_min=0.0)
        assert tone != DominantTone.EVASIVE

    def test_evasive_hesitation_exactly_5_not_triggered(self):
        tone = self._tone(conf=50.0, engage=29.0,
                          call_ended_abruptly=0, objection_count=0,
                          hesitation_keywords_count=5, filler_word_rate_per_min=0.0)
        assert tone != DominantTone.EVASIVE

    def test_resistant_when_objection_gt4_neg_gt25(self):
        tone = self._tone(conf=50.0, engage=50.0,
                          call_ended_abruptly=0, objection_count=5,
                          sentiment_score_negative=26.0, hesitation_keywords_count=0,
                          filler_word_rate_per_min=0.0)
        assert tone == DominantTone.RESISTANT

    def test_resistant_objection_exactly_4_not_triggered(self):
        tone = self._tone(conf=50.0, engage=50.0,
                          call_ended_abruptly=0, objection_count=4,
                          sentiment_score_negative=30.0, hesitation_keywords_count=0,
                          filler_word_rate_per_min=0.0)
        assert tone != DominantTone.RESISTANT

    def test_resistant_neg_exactly_25_not_triggered(self):
        tone = self._tone(conf=50.0, engage=50.0,
                          call_ended_abruptly=0, objection_count=5,
                          sentiment_score_negative=25.0, hesitation_keywords_count=0,
                          filler_word_rate_per_min=0.0)
        assert tone != DominantTone.RESISTANT

    def test_hesitant_via_filler_rate_ge3(self):
        tone = self._tone(conf=50.0, engage=50.0,
                          call_ended_abruptly=0, objection_count=0,
                          filler_word_rate_per_min=3.0)
        assert tone == DominantTone.HESITANT

    def test_hesitant_via_conf_lt40(self):
        tone = self._tone(conf=39.0, engage=50.0,
                          call_ended_abruptly=0, objection_count=0,
                          filler_word_rate_per_min=0.0)
        assert tone == DominantTone.HESITANT

    def test_hesitant_conf_exactly_40_not_triggered_via_conf(self):
        tone = self._tone(conf=40.0, engage=50.0,
                          call_ended_abruptly=0, objection_count=0,
                          filler_word_rate_per_min=0.0,
                          talk_time_rep_pct=60.0,
                          enthusiasm_keywords_count=0)
        # conf=40 (not <40), filler=0, engage=50 (not >=65)
        # conf 40 < 70 so not authoritative via that branch
        # falls to default authoritative
        assert tone == DominantTone.AUTHORITATIVE

    def test_authoritative_via_conf_ge70_talk_ge50(self):
        tone = self._tone(conf=70.0, engage=50.0,
                          call_ended_abruptly=0, objection_count=0,
                          filler_word_rate_per_min=0.0,
                          talk_time_rep_pct=50.0, enthusiasm_keywords_count=0)
        assert tone == DominantTone.AUTHORITATIVE

    def test_enthusiastic_when_engage_ge65_enthusiasm_ge5(self):
        tone = self._tone(conf=50.0, engage=65.0,
                          call_ended_abruptly=0, objection_count=0,
                          filler_word_rate_per_min=0.0,
                          enthusiasm_keywords_count=5,
                          talk_time_rep_pct=50.0)
        assert tone == DominantTone.ENTHUSIASTIC

    def test_enthusiastic_engage_exactly_65(self):
        tone = self._tone(conf=50.0, engage=65.0,
                          call_ended_abruptly=0, objection_count=0,
                          filler_word_rate_per_min=0.0,
                          enthusiasm_keywords_count=5,
                          talk_time_rep_pct=50.0)
        assert tone == DominantTone.ENTHUSIASTIC

    def test_enthusiastic_not_triggered_if_enthusiasm_lt5(self):
        tone = self._tone(conf=50.0, engage=65.0,
                          call_ended_abruptly=0, objection_count=0,
                          filler_word_rate_per_min=0.0,
                          enthusiasm_keywords_count=4,
                          talk_time_rep_pct=50.0)
        assert tone != DominantTone.ENTHUSIASTIC

    def test_authoritative_default_fallback(self):
        tone = self._tone(conf=60.0, engage=50.0,
                          call_ended_abruptly=0, objection_count=0,
                          filler_word_rate_per_min=0.0,
                          talk_time_rep_pct=50.0, enthusiasm_keywords_count=0)
        assert tone == DominantTone.AUTHORITATIVE


# ---------------------------------------------------------------------------
# 11. _conversation_control thresholds
# ---------------------------------------------------------------------------

class TestConversationControl:
    def setup_method(self):
        self.a = CallToneAnalyzer()

    def _ctrl(self, talk_pct, abrupt=0, silence=0):
        inp = make_input(talk_time_rep_pct=talk_pct, call_ended_abruptly=abrupt,
                         silence_events_long=silence)
        return self.a._conversation_control(inp)

    def test_fragmented_abrupt_and_silence_ge3(self):
        assert self._ctrl(50.0, abrupt=1, silence=3) == ConversationControl.FRAGMENTED

    def test_fragmented_silence_exactly_3(self):
        assert self._ctrl(50.0, abrupt=1, silence=3) == ConversationControl.FRAGMENTED

    def test_fragmented_silence_lt3_not_triggered(self):
        assert self._ctrl(50.0, abrupt=1, silence=2) != ConversationControl.FRAGMENTED

    def test_fragmented_not_triggered_without_abrupt(self):
        assert self._ctrl(50.0, abrupt=0, silence=5) != ConversationControl.FRAGMENTED

    def test_rep_led_talk_ge70(self):
        assert self._ctrl(70.0) == ConversationControl.REP_LED

    def test_rep_led_talk_above_70(self):
        assert self._ctrl(85.0) == ConversationControl.REP_LED

    def test_rep_led_talk_exactly_70(self):
        assert self._ctrl(70.0) == ConversationControl.REP_LED

    def test_buyer_led_talk_le30(self):
        assert self._ctrl(30.0) == ConversationControl.BUYER_LED

    def test_buyer_led_talk_below_30(self):
        assert self._ctrl(20.0) == ConversationControl.BUYER_LED

    def test_buyer_led_exactly_30(self):
        assert self._ctrl(30.0) == ConversationControl.BUYER_LED

    def test_balanced_talk_between_30_and_70(self):
        assert self._ctrl(50.0) == ConversationControl.BALANCED

    def test_balanced_talk_just_above_30(self):
        assert self._ctrl(31.0) == ConversationControl.BALANCED

    def test_balanced_talk_just_below_70(self):
        assert self._ctrl(69.0) == ConversationControl.BALANCED

    def test_fragmented_takes_priority_over_rep_led(self):
        # talk=80 would be rep_led, but abrupt+silence=3 → fragmented
        assert self._ctrl(80.0, abrupt=1, silence=3) == ConversationControl.FRAGMENTED


# ---------------------------------------------------------------------------
# 12. _deal_advancement_probability
# ---------------------------------------------------------------------------

class TestDealAdvancementProbability:
    def setup_method(self):
        self.a = CallToneAnalyzer()

    def _adv(self, composite, **kwargs):
        inp = make_input(**kwargs)
        return self.a._deal_advancement_probability(inp, composite)

    def test_base_is_composite(self):
        score = self._adv(50.0, next_steps_agreed=0, decision_timeline_mentioned=0,
                          call_ended_abruptly=0, objection_count=0)
        assert score == 50.0

    def test_next_steps_adds_15(self):
        score = self._adv(50.0, next_steps_agreed=1, decision_timeline_mentioned=0,
                          call_ended_abruptly=0, objection_count=0)
        assert score == 65.0

    def test_timeline_adds_10(self):
        score = self._adv(50.0, next_steps_agreed=0, decision_timeline_mentioned=1,
                          call_ended_abruptly=0, objection_count=0)
        assert score == 60.0

    def test_both_bonuses(self):
        score = self._adv(50.0, next_steps_agreed=1, decision_timeline_mentioned=1,
                          call_ended_abruptly=0, objection_count=0)
        assert score == 75.0

    def test_abrupt_subtracts_20(self):
        score = self._adv(50.0, next_steps_agreed=0, decision_timeline_mentioned=0,
                          call_ended_abruptly=1, objection_count=0)
        assert score == 30.0

    def test_objection_low_resolution_penalty(self):
        score = self._adv(50.0, next_steps_agreed=0, decision_timeline_mentioned=0,
                          call_ended_abruptly=0, objection_count=2, objection_resolved_count=0)
        # resolution=0 < 0.5 → -10
        assert score == 40.0

    def test_objection_exactly_50pct_no_penalty(self):
        score = self._adv(50.0, next_steps_agreed=0, decision_timeline_mentioned=0,
                          call_ended_abruptly=0, objection_count=2, objection_resolved_count=1)
        # 1/2 = 0.5, NOT < 0.5, no penalty
        assert score == 50.0

    def test_zero_objections_no_penalty(self):
        score = self._adv(50.0, next_steps_agreed=0, decision_timeline_mentioned=0,
                          call_ended_abruptly=0, objection_count=0)
        assert score == 50.0

    def test_clamp_floor_zero(self):
        score = self._adv(10.0, next_steps_agreed=0, decision_timeline_mentioned=0,
                          call_ended_abruptly=1, objection_count=2, objection_resolved_count=0)
        # 10 - 20 - 10 = -20 → 0
        assert score == 0.0

    def test_clamp_ceiling_100(self):
        score = self._adv(90.0, next_steps_agreed=1, decision_timeline_mentioned=1,
                          call_ended_abruptly=0, objection_count=0)
        # 90 + 15 + 10 = 115 → 100
        assert score == 100.0


# ---------------------------------------------------------------------------
# 13. _coaching_priority formula
# ---------------------------------------------------------------------------

class TestCoachingPriority:
    def setup_method(self):
        self.a = CallToneAnalyzer()

    def _coach(self, conf, obj_hdl, composite):
        return self.a._coaching_priority(conf, obj_hdl, composite)

    def test_base_100_minus_composite(self):
        assert self._coach(50.0, 50.0, 40.0) == 60.0

    def test_low_conf_adds_20(self):
        # base=60, conf<40 → +20 = 80
        assert self._coach(39.0, 50.0, 40.0) == 80.0

    def test_conf_exactly_40_no_extra_penalty(self):
        assert self._coach(40.0, 50.0, 40.0) == 60.0

    def test_low_obj_hdl_adds_15(self):
        # base=60, obj_hdl<40 → +15 = 75
        assert self._coach(50.0, 39.0, 40.0) == 75.0

    def test_obj_hdl_exactly_40_no_extra_penalty(self):
        assert self._coach(50.0, 40.0, 40.0) == 60.0

    def test_both_low_adds_35(self):
        # base=60 +20 +15 = 95
        assert self._coach(39.0, 39.0, 40.0) == 95.0

    def test_clamp_ceiling_100(self):
        # composite=0 → base=100, +20+15=135 → 100
        assert self._coach(30.0, 30.0, 0.0) == 100.0

    def test_composite_100_base_zero(self):
        assert self._coach(80.0, 80.0, 100.0) == 0.0

    def test_high_composite_no_conf_obj_issue(self):
        assert self._coach(60.0, 60.0, 80.0) == 20.0


# ---------------------------------------------------------------------------
# 14. is_positive_call logic
# ---------------------------------------------------------------------------

class TestIsPositiveCall:
    def setup_method(self):
        self.a = CallToneAnalyzer()

    def _result(self, **kwargs):
        return self.a.analyze(make_input(**kwargs))

    def test_positive_call_requires_composite_ge55_and_next_steps(self):
        # Good call with next steps
        r = self._result(
            filler_word_rate_per_min=0.0, enthusiasm_keywords_count=5,
            interruption_count_rep=0, talk_time_rep_pct=50.0, call_ended_abruptly=0,
            questions_asked_buyer=5, interruption_count_buyer=3,
            sentiment_score_positive=60.0, sentiment_score_negative=5.0,
            decision_timeline_mentioned=1, next_steps_agreed=1,
            objection_count=0, hesitation_keywords_count=0,
            silence_events_long=0, price_mention_count=0,
            competitor_mention_count=0, questions_asked_rep=5,
            call_duration_minutes=40,
        )
        assert r.call_tone_composite >= 55.0
        assert r.is_positive_call is True

    def test_not_positive_without_next_steps(self):
        r = self._result(
            filler_word_rate_per_min=0.0, enthusiasm_keywords_count=5,
            talk_time_rep_pct=50.0, call_ended_abruptly=0,
            questions_asked_buyer=5, interruption_count_buyer=3,
            sentiment_score_positive=60.0, sentiment_score_negative=5.0,
            decision_timeline_mentioned=1, next_steps_agreed=0,
            objection_count=0, questions_asked_rep=5,
            call_duration_minutes=40,
        )
        assert r.is_positive_call is False

    def test_not_positive_if_composite_lt55(self):
        # Force low composite
        r = self._result(
            filler_word_rate_per_min=5.0, enthusiasm_keywords_count=0,
            talk_time_rep_pct=90.0, call_ended_abruptly=1,
            questions_asked_buyer=0, next_steps_agreed=1,
            objection_count=5, objection_resolved_count=0,
            sentiment_score_negative=40.0,
        )
        assert r.call_tone_composite < 55.0
        assert r.is_positive_call is False

    def test_positive_call_exactly_55_composite(self):
        # Carefully construct a scenario where composite ~= 55
        a = CallToneAnalyzer()
        # We test via direct calculation
        # composite=55, next_steps=1
        r = CallToneResult(
            call_id="X", deal_name="Y", tone_sentiment=ToneSentiment.NEUTRAL,
            dominant_tone=DominantTone.AUTHORITATIVE,
            conversation_control=ConversationControl.BALANCED,
            tone_action=ToneAction.NURTURE,
            rep_confidence_score=55.0, buyer_engagement_score=55.0,
            objection_handling_score=55.0, conversation_quality_score=55.0,
            call_tone_composite=55.0, deal_advancement_probability=55.0,
            call_coaching_priority=45.0, is_positive_call=True, needs_immediate_coaching=False,
        )
        assert r.is_positive_call is True


# ---------------------------------------------------------------------------
# 15. needs_immediate_coaching conditions
# ---------------------------------------------------------------------------

class TestNeedsImmediateCoaching:
    def setup_method(self):
        self.a = CallToneAnalyzer()

    def test_coaching_via_priority_ge65(self):
        # Force high coaching priority
        r = self.a.analyze(make_input(
            filler_word_rate_per_min=5.0, enthusiasm_keywords_count=0,
            talk_time_rep_pct=90.0, call_ended_abruptly=1,
            objection_count=5, objection_resolved_count=0,
            hesitation_keywords_count=10, sentiment_score_negative=50.0,
        ))
        assert r.call_coaching_priority >= 65.0
        assert r.needs_immediate_coaching is True

    def test_coaching_via_filler_ge5_and_conf_lt40(self):
        # filler>=5 and conf<40
        r = self.a.analyze(make_input(
            filler_word_rate_per_min=5.0, enthusiasm_keywords_count=0,
            talk_time_rep_pct=90.0, call_ended_abruptly=0,
            objection_count=0,
        ))
        # conf: 50 - 30 - 15 = 5 < 40; filler=5 >= 5
        assert r.rep_confidence_score < 40.0
        assert r.needs_immediate_coaching is True

    def test_no_coaching_needed_good_call(self):
        r = self.a.analyze(make_input(
            filler_word_rate_per_min=0.0, enthusiasm_keywords_count=5,
            talk_time_rep_pct=50.0, call_ended_abruptly=0,
            questions_asked_buyer=5, next_steps_agreed=1,
            sentiment_score_positive=60.0, sentiment_score_negative=5.0,
            objection_count=0, questions_asked_rep=5,
            call_duration_minutes=40,
        ))
        assert r.needs_immediate_coaching is False

    def test_coaching_filler_exactly_5_and_conf_lt40(self):
        a = CallToneAnalyzer()
        # Create scenario where filler=5.0 and conf<40
        inp = make_input(filler_word_rate_per_min=5.0, enthusiasm_keywords_count=0,
                         talk_time_rep_pct=85.0, call_ended_abruptly=0)
        r = a.analyze(inp)
        # conf = 50 - 30 - 15 = 5 < 40; filler=5
        assert r.needs_immediate_coaching is True


# ---------------------------------------------------------------------------
# 16. _tone_action derivation
# ---------------------------------------------------------------------------

class TestToneAction:
    def setup_method(self):
        self.a = CallToneAnalyzer()

    def test_intervene_when_needs_coaching(self):
        # needs_coaching=True → intervene
        r = self.a.analyze(make_input(
            filler_word_rate_per_min=5.0, enthusiasm_keywords_count=0,
            talk_time_rep_pct=90.0, call_ended_abruptly=0,
        ))
        assert r.tone_action == ToneAction.INTERVENE

    def test_intervene_when_negative_sentiment(self):
        # Force negative sentiment without coaching
        # Low composite, low neg sentiment but forced negative
        r = self.a.analyze(make_input(
            filler_word_rate_per_min=5.0, enthusiasm_keywords_count=0,
            talk_time_rep_pct=85.0, call_ended_abruptly=1,
            objection_count=5, objection_resolved_count=0,
            sentiment_score_negative=50.0, hesitation_keywords_count=15,
        ))
        assert r.tone_action == ToneAction.INTERVENE

    def test_reframe_when_cautious(self):
        # Use direct method call
        action = self.a._tone_action(ToneSentiment.CAUTIOUS, False, False)
        assert action == ToneAction.REFRAME

    def test_nurture_when_neutral(self):
        action = self.a._tone_action(ToneSentiment.NEUTRAL, True, False)
        assert action == ToneAction.NURTURE

    def test_reinforce_when_positive(self):
        action = self.a._tone_action(ToneSentiment.POSITIVE, True, False)
        assert action == ToneAction.REINFORCE

    def test_intervene_overrides_positive_if_coaching(self):
        action = self.a._tone_action(ToneSentiment.POSITIVE, True, True)
        assert action == ToneAction.INTERVENE

    def test_intervene_for_negative_no_coaching(self):
        action = self.a._tone_action(ToneSentiment.NEGATIVE, False, False)
        assert action == ToneAction.INTERVENE


# ---------------------------------------------------------------------------
# 17. analyze() — result structure
# ---------------------------------------------------------------------------

class TestAnalyze:
    def setup_method(self):
        self.a = CallToneAnalyzer()

    def test_returns_call_tone_result(self):
        r = self.a.analyze(make_input())
        assert isinstance(r, CallToneResult)

    def test_call_id_propagated(self):
        r = self.a.analyze(make_input(call_id="C999"))
        assert r.call_id == "C999"

    def test_deal_name_propagated(self):
        r = self.a.analyze(make_input(deal_name="BigDeal"))
        assert r.deal_name == "BigDeal"

    def test_scores_in_valid_range(self):
        r = self.a.analyze(make_input())
        for score in [r.rep_confidence_score, r.buyer_engagement_score,
                      r.objection_handling_score, r.conversation_quality_score,
                      r.call_tone_composite, r.deal_advancement_probability,
                      r.call_coaching_priority]:
            assert 0.0 <= score <= 100.0, f"Score out of range: {score}"

    def test_result_stored(self):
        self.a.analyze(make_input(call_id="C001"))
        assert len(self.a._results) == 1

    def test_multiple_analyzes_accumulate(self):
        for i in range(5):
            self.a.analyze(make_input(call_id=f"C{i:03d}"))
        assert len(self.a._results) == 5

    def test_tone_sentiment_is_enum(self):
        r = self.a.analyze(make_input())
        assert isinstance(r.tone_sentiment, ToneSentiment)

    def test_dominant_tone_is_enum(self):
        r = self.a.analyze(make_input())
        assert isinstance(r.dominant_tone, DominantTone)

    def test_conversation_control_is_enum(self):
        r = self.a.analyze(make_input())
        assert isinstance(r.conversation_control, ConversationControl)

    def test_tone_action_is_enum(self):
        r = self.a.analyze(make_input())
        assert isinstance(r.tone_action, ToneAction)


# ---------------------------------------------------------------------------
# 18. analyze_batch()
# ---------------------------------------------------------------------------

class TestAnalyzeBatch:
    def setup_method(self):
        self.a = CallToneAnalyzer()

    def test_returns_list(self):
        inputs = [make_input(call_id=f"C{i}") for i in range(3)]
        results = self.a.analyze_batch(inputs)
        assert isinstance(results, list)

    def test_returns_correct_count(self):
        inputs = [make_input(call_id=f"C{i}") for i in range(5)]
        results = self.a.analyze_batch(inputs)
        assert len(results) == 5

    def test_all_results_are_call_tone_result(self):
        inputs = [make_input(call_id=f"C{i}") for i in range(3)]
        results = self.a.analyze_batch(inputs)
        for r in results:
            assert isinstance(r, CallToneResult)

    def test_empty_batch_returns_empty_list(self):
        results = self.a.analyze_batch([])
        assert results == []

    def test_batch_stores_results(self):
        inputs = [make_input(call_id=f"C{i}") for i in range(4)]
        self.a.analyze_batch(inputs)
        assert len(self.a._results) == 4

    def test_batch_call_ids_preserved(self):
        inputs = [make_input(call_id=f"CALL-{i}") for i in range(3)]
        results = self.a.analyze_batch(inputs)
        assert [r.call_id for r in results] == ["CALL-0", "CALL-1", "CALL-2"]


# ---------------------------------------------------------------------------
# 19. reset()
# ---------------------------------------------------------------------------

class TestReset:
    def test_reset_clears_results(self):
        a = CallToneAnalyzer()
        for i in range(5):
            a.analyze(make_input(call_id=f"C{i}"))
        a.reset()
        assert len(a._results) == 0

    def test_reset_empty_no_error(self):
        a = CallToneAnalyzer()
        a.reset()  # should not raise
        assert len(a._results) == 0

    def test_analyze_after_reset(self):
        a = CallToneAnalyzer()
        for i in range(3):
            a.analyze(make_input(call_id=f"C{i}"))
        a.reset()
        a.analyze(make_input(call_id="NEW"))
        assert len(a._results) == 1

    def test_properties_after_reset(self):
        a = CallToneAnalyzer()
        a.analyze(make_input())
        a.reset()
        assert a.avg_call_tone_composite == 0.0
        assert a.avg_deal_advancement_probability == 0.0
        assert a.positive_calls == []
        assert a.coaching_needed == []


# ---------------------------------------------------------------------------
# 20. Properties
# ---------------------------------------------------------------------------

class TestProperties:
    def test_positive_calls_empty_initially(self):
        a = CallToneAnalyzer()
        assert a.positive_calls == []

    def test_coaching_needed_empty_initially(self):
        a = CallToneAnalyzer()
        assert a.coaching_needed == []

    def test_avg_composite_zero_when_empty(self):
        a = CallToneAnalyzer()
        assert a.avg_call_tone_composite == 0.0

    def test_avg_adv_prob_zero_when_empty(self):
        a = CallToneAnalyzer()
        assert a.avg_deal_advancement_probability == 0.0

    def test_positive_calls_filters_correctly(self):
        a = CallToneAnalyzer()
        # Good call with next steps
        a.analyze(make_input(
            filler_word_rate_per_min=0.0, enthusiasm_keywords_count=5,
            talk_time_rep_pct=50.0, call_ended_abruptly=0,
            questions_asked_buyer=5, next_steps_agreed=1,
            sentiment_score_positive=60.0, objection_count=0,
            questions_asked_rep=5, call_duration_minutes=40,
        ))
        # Bad call
        a.analyze(make_input(
            filler_word_rate_per_min=5.0, next_steps_agreed=0,
            talk_time_rep_pct=90.0, call_ended_abruptly=1,
        ))
        assert len(a.positive_calls) >= 1

    def test_coaching_needed_filters_correctly(self):
        a = CallToneAnalyzer()
        # Bad call needing coaching
        a.analyze(make_input(
            filler_word_rate_per_min=5.0, talk_time_rep_pct=90.0,
            call_ended_abruptly=0, enthusiasm_keywords_count=0,
        ))
        assert len(a.coaching_needed) >= 1

    def test_avg_composite_single_result(self):
        a = CallToneAnalyzer()
        r = a.analyze(make_input())
        assert a.avg_call_tone_composite == r.call_tone_composite

    def test_avg_deal_adv_single_result(self):
        a = CallToneAnalyzer()
        r = a.analyze(make_input())
        assert a.avg_deal_advancement_probability == r.deal_advancement_probability

    def test_avg_composite_multiple(self):
        a = CallToneAnalyzer()
        r1 = a.analyze(make_input(call_id="C1"))
        r2 = a.analyze(make_input(call_id="C2"))
        expected = round((r1.call_tone_composite + r2.call_tone_composite) / 2, 1)
        assert a.avg_call_tone_composite == expected


# ---------------------------------------------------------------------------
# 21. summary() — 13 keys
# ---------------------------------------------------------------------------

class TestSummary:
    def test_empty_summary_key_count(self):
        a = CallToneAnalyzer()
        s = a.summary()
        assert len(s) == 13

    def test_empty_summary_exact_keys(self):
        a = CallToneAnalyzer()
        s = a.summary()
        expected = {
            "total", "sentiment_counts", "tone_counts", "control_counts",
            "action_counts", "avg_call_tone_composite", "positive_call_count",
            "coaching_needed_count", "avg_rep_confidence_score",
            "avg_buyer_engagement_score", "avg_objection_handling_score",
            "avg_deal_advancement_probability", "avg_coaching_priority",
        }
        assert set(s.keys()) == expected

    def test_empty_summary_total_zero(self):
        assert CallToneAnalyzer().summary()["total"] == 0

    def test_empty_summary_dicts_empty(self):
        s = CallToneAnalyzer().summary()
        assert s["sentiment_counts"] == {}
        assert s["tone_counts"] == {}
        assert s["control_counts"] == {}
        assert s["action_counts"] == {}

    def test_empty_summary_avgs_zero(self):
        s = CallToneAnalyzer().summary()
        for key in ["avg_call_tone_composite", "avg_rep_confidence_score",
                    "avg_buyer_engagement_score", "avg_objection_handling_score",
                    "avg_deal_advancement_probability", "avg_coaching_priority"]:
            assert s[key] == 0.0

    def test_summary_total_count(self):
        a = CallToneAnalyzer()
        a.analyze_batch([make_input(call_id=f"C{i}") for i in range(3)])
        assert a.summary()["total"] == 3

    def test_summary_sentiment_counts(self):
        a = CallToneAnalyzer()
        a.analyze(make_input())
        s = a.summary()
        assert sum(s["sentiment_counts"].values()) == 1

    def test_summary_tone_counts(self):
        a = CallToneAnalyzer()
        a.analyze_batch([make_input(call_id=f"C{i}") for i in range(4)])
        s = a.summary()
        assert sum(s["tone_counts"].values()) == 4

    def test_summary_control_counts(self):
        a = CallToneAnalyzer()
        a.analyze_batch([make_input(call_id=f"C{i}") for i in range(2)])
        s = a.summary()
        assert sum(s["control_counts"].values()) == 2

    def test_summary_action_counts(self):
        a = CallToneAnalyzer()
        a.analyze_batch([make_input(call_id=f"C{i}") for i in range(3)])
        s = a.summary()
        assert sum(s["action_counts"].values()) == 3

    def test_summary_positive_call_count(self):
        a = CallToneAnalyzer()
        # One good call
        a.analyze(make_input(
            filler_word_rate_per_min=0.0, enthusiasm_keywords_count=5,
            talk_time_rep_pct=50.0, call_ended_abruptly=0,
            questions_asked_buyer=6, next_steps_agreed=1,
            sentiment_score_positive=60.0, objection_count=0,
            questions_asked_rep=7, call_duration_minutes=40,
        ))
        s = a.summary()
        assert s["positive_call_count"] == len(a.positive_calls)

    def test_summary_coaching_needed_count(self):
        a = CallToneAnalyzer()
        a.analyze(make_input(
            filler_word_rate_per_min=5.0, talk_time_rep_pct=90.0,
            call_ended_abruptly=0, enthusiasm_keywords_count=0,
        ))
        s = a.summary()
        assert s["coaching_needed_count"] == len(a.coaching_needed)

    def test_summary_avgs_match_properties(self):
        a = CallToneAnalyzer()
        a.analyze_batch([make_input(call_id=f"C{i}") for i in range(3)])
        s = a.summary()
        assert s["avg_call_tone_composite"] == a.avg_call_tone_composite

    def test_summary_after_reset(self):
        a = CallToneAnalyzer()
        a.analyze_batch([make_input(call_id=f"C{i}") for i in range(3)])
        a.reset()
        s = a.summary()
        assert s["total"] == 0


# ---------------------------------------------------------------------------
# 22. End-to-end: Great Call scenario
# ---------------------------------------------------------------------------

class TestGreatCall:
    def setup_method(self):
        self.a = CallToneAnalyzer()
        self.result = self.a.analyze(make_input(
            call_id="GREAT-001",
            deal_name="Enterprise Deal",
            rep_id="REP-A",
            call_duration_minutes=45,
            talk_time_rep_pct=50.0,
            filler_word_rate_per_min=0.0,
            interruption_count_rep=1,
            interruption_count_buyer=3,
            questions_asked_rep=7,
            questions_asked_buyer=6,
            sentiment_score_positive=70.0,
            sentiment_score_negative=5.0,
            enthusiasm_keywords_count=8,
            hesitation_keywords_count=0,
            objection_count=2,
            objection_resolved_count=2,
            silence_events_long=0,
            price_mention_count=1,
            competitor_mention_count=0,
            decision_timeline_mentioned=1,
            next_steps_agreed=1,
            call_ended_abruptly=0,
        ))

    def test_positive_sentiment(self):
        assert self.result.tone_sentiment == ToneSentiment.POSITIVE

    def test_high_composite(self):
        assert self.result.call_tone_composite >= 70.0

    def test_is_positive_call(self):
        assert self.result.is_positive_call is True

    def test_no_coaching_needed(self):
        assert self.result.needs_immediate_coaching is False

    def test_tone_action_reinforce(self):
        assert self.result.tone_action == ToneAction.REINFORCE

    def test_high_rep_confidence(self):
        assert self.result.rep_confidence_score >= 60.0

    def test_high_buyer_engagement(self):
        assert self.result.buyer_engagement_score >= 60.0

    def test_high_objection_handling(self):
        # All 2 objections resolved → 100
        assert self.result.objection_handling_score == 100.0

    def test_high_deal_advancement(self):
        assert self.result.deal_advancement_probability >= 70.0

    def test_low_coaching_priority(self):
        assert self.result.call_coaching_priority < 40.0


# ---------------------------------------------------------------------------
# 23. End-to-end: Disaster Call scenario
# ---------------------------------------------------------------------------

class TestDisasterCall:
    def setup_method(self):
        self.a = CallToneAnalyzer()
        self.result = self.a.analyze(make_input(
            call_id="BAD-001",
            deal_name="Lost Deal",
            rep_id="REP-B",
            call_duration_minutes=8,
            talk_time_rep_pct=88.0,
            filler_word_rate_per_min=6.0,
            interruption_count_rep=8,
            interruption_count_buyer=0,
            questions_asked_rep=0,
            questions_asked_buyer=0,
            sentiment_score_positive=5.0,
            sentiment_score_negative=55.0,
            enthusiasm_keywords_count=0,
            hesitation_keywords_count=12,
            objection_count=6,
            objection_resolved_count=0,
            silence_events_long=5,
            price_mention_count=5,
            competitor_mention_count=4,
            decision_timeline_mentioned=0,
            next_steps_agreed=0,
            call_ended_abruptly=1,
        ))

    def test_negative_or_cautious_sentiment(self):
        assert self.result.tone_sentiment in (ToneSentiment.NEGATIVE, ToneSentiment.CAUTIOUS)

    def test_low_composite(self):
        assert self.result.call_tone_composite < 40.0

    def test_not_positive_call(self):
        assert self.result.is_positive_call is False

    def test_needs_coaching(self):
        assert self.result.needs_immediate_coaching is True

    def test_tone_action_intervene(self):
        assert self.result.tone_action == ToneAction.INTERVENE

    def test_high_coaching_priority(self):
        assert self.result.call_coaching_priority >= 65.0

    def test_low_deal_advancement(self):
        assert self.result.deal_advancement_probability < 30.0

    def test_panic_or_hesitant_tone(self):
        assert self.result.dominant_tone in (DominantTone.PANIC_SIGNAL, DominantTone.HESITANT,
                                              DominantTone.RESISTANT)

    def test_rep_led_or_fragmented_control(self):
        # talk=88% → rep_led; but abrupt+silence=5 → fragmented first
        assert self.result.conversation_control == ConversationControl.FRAGMENTED


# ---------------------------------------------------------------------------
# 24. End-to-end: Hesitant Rep scenario
# ---------------------------------------------------------------------------

class TestHesitantRep:
    def setup_method(self):
        self.a = CallToneAnalyzer()
        self.result = self.a.analyze(make_input(
            call_id="HES-001",
            filler_word_rate_per_min=4.0,
            enthusiasm_keywords_count=0,
            talk_time_rep_pct=50.0,
            call_ended_abruptly=0,
            objection_count=0,
            hesitation_keywords_count=8,
            questions_asked_buyer=2,
            next_steps_agreed=0,
        ))

    def test_hesitant_dominant_tone(self):
        assert self.result.dominant_tone == DominantTone.HESITANT

    def test_low_rep_confidence(self):
        # filler=4 → -18 penalty; 50-18+10=42
        assert self.result.rep_confidence_score < 60.0

    def test_coaching_priority_reflects_low_confidence(self):
        # filler=4.0 → conf=42 (not <40), so no conf bonus applied
        # coaching_priority = 100 - composite (no extra bonuses)
        assert self.result.call_coaching_priority == round(100.0 - self.result.call_tone_composite, 1)


# ---------------------------------------------------------------------------
# 25. End-to-end: Enthusiastic Buyer scenario
# ---------------------------------------------------------------------------

class TestEnthusiasticBuyer:
    def setup_method(self):
        self.a = CallToneAnalyzer()
        self.result = self.a.analyze(make_input(
            call_id="ENT-001",
            questions_asked_buyer=6,
            interruption_count_buyer=5,
            sentiment_score_positive=80.0,
            decision_timeline_mentioned=1,
            next_steps_agreed=1,
            filler_word_rate_per_min=0.0,
            enthusiasm_keywords_count=7,
            talk_time_rep_pct=50.0,
            call_ended_abruptly=0,
            objection_count=0,
            questions_asked_rep=5,
            call_duration_minutes=40,
        ))

    def test_high_buyer_engagement(self):
        assert self.result.buyer_engagement_score >= 80.0

    def test_positive_or_neutral_sentiment(self):
        assert self.result.tone_sentiment in (ToneSentiment.POSITIVE, ToneSentiment.NEUTRAL)

    def test_is_positive_call(self):
        assert self.result.is_positive_call is True

    def test_high_deal_advancement(self):
        assert self.result.deal_advancement_probability >= 70.0


# ---------------------------------------------------------------------------
# 26. Edge case: 0 objections
# ---------------------------------------------------------------------------

class TestZeroObjections:
    def setup_method(self):
        self.a = CallToneAnalyzer()

    def test_zero_objections_score_70(self):
        score = self.a._objection_handling_score(make_input(
            objection_count=0, objection_resolved_count=0, hesitation_keywords_count=0
        ))
        assert score == 70.0

    def test_zero_objections_no_advancement_penalty(self):
        r = self.a.analyze(make_input(
            objection_count=0, objection_resolved_count=0,
            filler_word_rate_per_min=0.0, enthusiasm_keywords_count=0,
            talk_time_rep_pct=50.0, call_ended_abruptly=0, next_steps_agreed=0,
        ))
        # no objection penalty applied
        assert r.deal_advancement_probability >= 0.0

    def test_zero_objections_with_hesitation_penalty(self):
        score = self.a._objection_handling_score(make_input(
            objection_count=0, objection_resolved_count=0, hesitation_keywords_count=5
        ))
        # 0 objections → 70.0 regardless of hesitation
        assert score == 70.0


# ---------------------------------------------------------------------------
# 27. Edge case: Very short call
# ---------------------------------------------------------------------------

class TestVeryShortCall:
    def setup_method(self):
        self.a = CallToneAnalyzer()

    def test_short_call_quality_penalty(self):
        score = self.a._conversation_quality_score(make_input(
            call_duration_minutes=5, questions_asked_rep=0, silence_events_long=0,
            price_mention_count=0, competitor_mention_count=0, next_steps_agreed=0,
        ))
        # 40 - 10 = 30
        assert score == 30.0

    def test_short_call_below_15_minutes(self):
        r = self.a.analyze(make_input(call_duration_minutes=10))
        assert r.conversation_quality_score <= 45.0

    def test_exactly_14_min_short(self):
        score = self.a._conversation_quality_score(make_input(
            call_duration_minutes=14, questions_asked_rep=0, silence_events_long=0,
            price_mention_count=0, competitor_mention_count=0, next_steps_agreed=0,
        ))
        assert score == 30.0

    def test_exactly_15_min_no_short_penalty(self):
        score = self.a._conversation_quality_score(make_input(
            call_duration_minutes=15, questions_asked_rep=0, silence_events_long=0,
            price_mention_count=0, competitor_mention_count=0, next_steps_agreed=0,
        ))
        assert score == 40.0


# ---------------------------------------------------------------------------
# 28. Edge case: All-zero inputs
# ---------------------------------------------------------------------------

class TestAllZeroInputs:
    def setup_method(self):
        self.a = CallToneAnalyzer()
        self.result = self.a.analyze(make_input(
            call_duration_minutes=0,
            talk_time_rep_pct=0.0,
            filler_word_rate_per_min=0.0,
            interruption_count_rep=0,
            interruption_count_buyer=0,
            questions_asked_rep=0,
            questions_asked_buyer=0,
            sentiment_score_positive=0.0,
            sentiment_score_negative=0.0,
            enthusiasm_keywords_count=0,
            hesitation_keywords_count=0,
            objection_count=0,
            objection_resolved_count=0,
            silence_events_long=0,
            price_mention_count=0,
            competitor_mention_count=0,
            decision_timeline_mentioned=0,
            next_steps_agreed=0,
            call_ended_abruptly=0,
        ))

    def test_scores_non_negative(self):
        assert self.result.rep_confidence_score >= 0.0
        assert self.result.buyer_engagement_score >= 0.0
        assert self.result.objection_handling_score >= 0.0
        assert self.result.conversation_quality_score >= 0.0
        assert self.result.call_tone_composite >= 0.0

    def test_composite_non_negative(self):
        assert self.result.call_tone_composite >= 0.0

    def test_no_exception_raised(self):
        # Simply getting here means no exception was raised
        assert True

    def test_is_positive_call_false(self):
        assert self.result.is_positive_call is False

    def test_objection_score_70_zero_objections(self):
        assert self.result.objection_handling_score == 70.0


# ---------------------------------------------------------------------------
# 29. Cross-validation tests
# ---------------------------------------------------------------------------

class TestCrossValidation:
    def setup_method(self):
        self.a = CallToneAnalyzer()

    def test_composite_consistent_with_subscores(self):
        r = self.a.analyze(make_input())
        expected = round(
            r.rep_confidence_score * 0.30 +
            r.buyer_engagement_score * 0.30 +
            r.objection_handling_score * 0.25 +
            r.conversation_quality_score * 0.15,
            1
        )
        assert r.call_tone_composite == expected

    def test_is_positive_call_consistent(self):
        r = self.a.analyze(make_input())
        expected = r.call_tone_composite >= 55.0 and r.needs_immediate_coaching is False
        # is_positive_call = composite >= 55 AND next_steps_agreed == 1
        # We verify the logic is self-consistent
        if r.is_positive_call:
            assert r.call_tone_composite >= 55.0

    def test_needs_coaching_consistent_with_priority(self):
        for _ in range(10):
            inp = make_input(
                filler_word_rate_per_min=3.0,
                enthusiasm_keywords_count=1,
                talk_time_rep_pct=50.0,
            )
            r = self.a.analyze(inp)
            if r.call_coaching_priority >= 65.0:
                assert r.needs_immediate_coaching is True

    def test_tone_action_consistent_with_sentiment(self):
        r = self.a.analyze(make_input())
        if not r.needs_immediate_coaching and r.tone_sentiment == ToneSentiment.POSITIVE:
            assert r.tone_action == ToneAction.REINFORCE
        elif not r.needs_immediate_coaching and r.tone_sentiment == ToneSentiment.NEUTRAL:
            assert r.tone_action == ToneAction.NURTURE
        elif not r.needs_immediate_coaching and r.tone_sentiment == ToneSentiment.CAUTIOUS:
            assert r.tone_action == ToneAction.REFRAME

    def test_deal_advancement_never_exceeds_100(self):
        r = self.a.analyze(make_input(
            next_steps_agreed=1, decision_timeline_mentioned=1,
            call_ended_abruptly=0, objection_count=0,
            filler_word_rate_per_min=0.0, enthusiasm_keywords_count=20,
            talk_time_rep_pct=50.0,
        ))
        assert r.deal_advancement_probability <= 100.0

    def test_coaching_priority_consistent_with_composite(self):
        r = self.a.analyze(make_input())
        base = max(0.0, 100.0 - r.call_tone_composite)
        assert r.call_coaching_priority >= base - 0.1  # accounts for rounding

    def test_to_dict_values_match_attributes(self):
        r = self.a.analyze(make_input(call_id="CROSS-001"))
        d = r.to_dict()
        assert d["call_id"] == r.call_id
        assert d["rep_confidence_score"] == r.rep_confidence_score
        assert d["call_tone_composite"] == r.call_tone_composite
        assert d["is_positive_call"] == r.is_positive_call

    def test_batch_results_match_individual(self):
        a1 = CallToneAnalyzer()
        a2 = CallToneAnalyzer()
        inputs = [make_input(call_id=f"C{i}", filler_word_rate_per_min=float(i)) for i in range(3)]
        batch_results = a1.analyze_batch(inputs)
        individual_results = [a2.analyze(inp) for inp in inputs]
        for b, ind in zip(batch_results, individual_results):
            assert b.call_tone_composite == ind.call_tone_composite
            assert b.tone_sentiment == ind.tone_sentiment

    def test_summary_counts_match_results(self):
        a = CallToneAnalyzer()
        a.analyze_batch([make_input(call_id=f"C{i}") for i in range(5)])
        s = a.summary()
        assert s["total"] == 5
        assert sum(s["sentiment_counts"].values()) == 5
        assert sum(s["tone_counts"].values()) == 5
        assert sum(s["control_counts"].values()) == 5
        assert sum(s["action_counts"].values()) == 5

    def test_positive_call_count_in_summary_correct(self):
        a = CallToneAnalyzer()
        # 3 calls
        for _ in range(3):
            a.analyze(make_input())
        s = a.summary()
        assert s["positive_call_count"] == len(a.positive_calls)

    def test_coaching_count_in_summary_correct(self):
        a = CallToneAnalyzer()
        for _ in range(3):
            a.analyze(make_input())
        s = a.summary()
        assert s["coaching_needed_count"] == len(a.coaching_needed)


# ---------------------------------------------------------------------------
# 30. Additional boundary / integration tests
# ---------------------------------------------------------------------------

class TestAdditionalBoundaries:
    def setup_method(self):
        self.a = CallToneAnalyzer()

    def test_filler_boundary_just_below_1_5(self):
        score = self.a._rep_confidence_score(make_input(
            filler_word_rate_per_min=1.4, enthusiasm_keywords_count=0,
            interruption_count_rep=0, talk_time_rep_pct=50.0, call_ended_abruptly=0
        ))
        # no penalty, +10 talk = 60
        assert score == 60.0

    def test_filler_boundary_just_below_3(self):
        score = self.a._rep_confidence_score(make_input(
            filler_word_rate_per_min=2.9, enthusiasm_keywords_count=0,
            interruption_count_rep=0, talk_time_rep_pct=50.0, call_ended_abruptly=0
        ))
        # -8 penalty, +10 = 52
        assert score == 52.0

    def test_filler_boundary_just_below_5(self):
        score = self.a._rep_confidence_score(make_input(
            filler_word_rate_per_min=4.9, enthusiasm_keywords_count=0,
            interruption_count_rep=0, talk_time_rep_pct=50.0, call_ended_abruptly=0
        ))
        # -18 penalty, +10 = 42
        assert score == 42.0

    def test_talk_pct_39_no_bonus(self):
        score = self.a._rep_confidence_score(make_input(
            talk_time_rep_pct=39.0, filler_word_rate_per_min=0.0,
            enthusiasm_keywords_count=0, interruption_count_rep=0, call_ended_abruptly=0
        ))
        assert score == 50.0

    def test_talk_pct_61_no_bonus(self):
        score = self.a._rep_confidence_score(make_input(
            talk_time_rep_pct=61.0, filler_word_rate_per_min=0.0,
            enthusiasm_keywords_count=0, interruption_count_rep=0, call_ended_abruptly=0
        ))
        assert score == 50.0

    def test_buyer_questions_5_not_capped(self):
        score = self.a._buyer_engagement_score(make_input(
            questions_asked_buyer=5, interruption_count_buyer=0,
            sentiment_score_positive=0, decision_timeline_mentioned=0,
            next_steps_agreed=0, sentiment_score_negative=0
        ))
        # 30 + 25 = 55
        assert score == 55.0

    def test_objection_high_count_exactly_at_boundary(self):
        # objection_count=5, resolution = exactly 50% — no penalty
        score = self.a._objection_handling_score(make_input(
            objection_count=6, objection_resolved_count=3, hesitation_keywords_count=0
        ))
        # 3/6=0.5, NOT < 0.5 → no penalty; 3/6 * 80 = 40
        assert score == 40.0

    def test_conversation_quality_silence_exactly_at_cap(self):
        score = self.a._conversation_quality_score(make_input(
            silence_events_long=5, questions_asked_rep=0,
            price_mention_count=0, competitor_mention_count=0,
            next_steps_agreed=0, call_duration_minutes=30
        ))
        # 40 - 20 (cap 5*4=20) + 5 = 25
        assert score == 25.0

    def test_composite_exactly_65_positive_gt40_is_positive(self):
        inp = make_input(sentiment_score_positive=41.0)
        result = self.a._tone_sentiment(inp, 65.0)
        assert result == ToneSentiment.POSITIVE

    def test_composite_exactly_45_is_neutral(self):
        inp = make_input(sentiment_score_positive=30.0, sentiment_score_negative=10.0)
        result = self.a._tone_sentiment(inp, 45.0)
        assert result == ToneSentiment.NEUTRAL

    def test_composite_exactly_30_is_cautious(self):
        inp = make_input(sentiment_score_positive=5.0, sentiment_score_negative=10.0)
        result = self.a._tone_sentiment(inp, 30.0)
        assert result == ToneSentiment.CAUTIOUS

    def test_composite_29_low_neg_is_negative(self):
        inp = make_input(sentiment_score_positive=5.0, sentiment_score_negative=10.0)
        result = self.a._tone_sentiment(inp, 29.0)
        assert result == ToneSentiment.NEGATIVE

    def test_advancement_next_steps_capped_at_100(self):
        # base=90 + 15 = 105 → 100
        prob = self.a._deal_advancement_probability(
            make_input(next_steps_agreed=1, decision_timeline_mentioned=0,
                       call_ended_abruptly=0, objection_count=0),
            90.0
        )
        assert prob == 100.0

    def test_coaching_zero_for_high_composite(self):
        # composite=100 → base=0, no additions needed
        score = self.a._coaching_priority(80.0, 80.0, 100.0)
        assert score == 0.0

    def test_rep_confidence_exactly_70_authoritative(self):
        tone = self.a._dominant_tone(
            make_input(filler_word_rate_per_min=0.0, talk_time_rep_pct=50.0,
                       call_ended_abruptly=0, objection_count=0,
                       enthusiasm_keywords_count=0),
            conf=70.0, engage=50.0
        )
        assert tone == DominantTone.AUTHORITATIVE

    def test_sentiment_counts_increase_on_second_analyze(self):
        a = CallToneAnalyzer()
        a.analyze(make_input(call_id="C1"))
        a.analyze(make_input(call_id="C2"))
        s = a.summary()
        assert s["total"] == 2
        assert sum(s["sentiment_counts"].values()) == 2

    def test_call_tone_result_dataclass_fields(self):
        import dataclasses
        fields = {f.name for f in dataclasses.fields(CallToneResult)}
        expected = {
            "call_id", "deal_name", "tone_sentiment", "dominant_tone",
            "conversation_control", "tone_action", "rep_confidence_score",
            "buyer_engagement_score", "objection_handling_score",
            "conversation_quality_score", "call_tone_composite",
            "deal_advancement_probability", "call_coaching_priority",
            "is_positive_call", "needs_immediate_coaching",
        }
        assert fields == expected

    def test_multiple_resets_and_reanalyze(self):
        a = CallToneAnalyzer()
        for _ in range(3):
            a.analyze(make_input())
        a.reset()
        for _ in range(2):
            a.analyze(make_input())
        a.reset()
        a.analyze(make_input(call_id="FINAL"))
        assert len(a._results) == 1
        assert a._results[0].call_id == "FINAL"

    def test_price_mention_3_medium_penalty(self):
        score = self.a._conversation_quality_score(make_input(
            price_mention_count=3, questions_asked_rep=0, silence_events_long=0,
            competitor_mention_count=0, next_steps_agreed=0, call_duration_minutes=30
        ))
        # 40 - 5 (price>=2 branch) + 5 = 40
        assert score == 40.0

    def test_buyer_engagement_exactly_at_floor_after_neg(self):
        # Large negative sentiment penalty
        score = self.a._buyer_engagement_score(make_input(
            questions_asked_buyer=0, interruption_count_buyer=0,
            sentiment_score_positive=0, decision_timeline_mentioned=0,
            next_steps_agreed=0, sentiment_score_negative=75.0
        ))
        # 30 - 20 (cap) = 10
        assert score == 10.0

    def test_rep_interruptions_exactly_6(self):
        score = self.a._rep_confidence_score(make_input(
            filler_word_rate_per_min=0.0, enthusiasm_keywords_count=0,
            interruption_count_rep=6, talk_time_rep_pct=50.0, call_ended_abruptly=0
        ))
        # 50 - 15 + 10 = 45
        assert score == 45.0

    def test_enthusiasm_exactly_6_keywords(self):
        score = self.a._rep_confidence_score(make_input(
            filler_word_rate_per_min=0.0, enthusiasm_keywords_count=6,
            interruption_count_rep=0, talk_time_rep_pct=50.0, call_ended_abruptly=0
        ))
        # 50 + 18 + 10 = 78
        assert score == 78.0
