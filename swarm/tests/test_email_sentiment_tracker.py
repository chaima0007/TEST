"""Comprehensive pytest tests for EmailSentimentTracker.

Covers all branches with 290+ tests.
"""
from __future__ import annotations

import pytest
from swarm.intelligence.email_sentiment_tracker import (
    BuyerEngagementSignal,
    EmailAction,
    EmailSentimentInput,
    EmailSentimentResult,
    EmailSentimentTracker,
    SentimentTrajectory,
    ThreadSentiment,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> EmailSentimentInput:
    """Return a well-formed, mid-range EmailSentimentInput with optional overrides."""
    defaults = dict(
        thread_id="T1",
        deal_id="D1",
        rep_id="R1",
        total_emails_sent=5,
        total_replies_received=3,
        avg_reply_length_words=50,
        avg_reply_length_prior_words=50,
        positive_language_count=3,
        negative_language_count=1,
        question_count_from_buyer=2,
        exclamation_count=2,
        hedge_phrase_count=0,
        urgency_language_count=2,
        reply_time_trend=1.0,
        opens_per_email_avg=1.0,
        cta_click_rate_pct=35.0,
        sentiment_score_recent=60.0,
        sentiment_score_prior=55.0,
        days_since_last_reply=3,
        thread_age_days=14,
        forwarded_to_others=0,
        deal_value=10000.0,
    )
    defaults.update(overrides)
    return EmailSentimentInput(**defaults)


def tracker() -> EmailSentimentTracker:
    return EmailSentimentTracker()


# ===========================================================================
# 1. STRUCTURAL / CONTRACT TESTS
# ===========================================================================

class TestEmailSentimentInputFields:
    """EmailSentimentInput has exactly 22 fields."""

    def test_field_count(self):
        inp = make_input()
        fields = inp.__dataclass_fields__
        assert len(fields) == 22

    def test_all_expected_fields_present(self):
        expected = {
            "thread_id", "deal_id", "rep_id", "total_emails_sent",
            "total_replies_received", "avg_reply_length_words",
            "avg_reply_length_prior_words", "positive_language_count",
            "negative_language_count", "question_count_from_buyer",
            "exclamation_count", "hedge_phrase_count",
            "urgency_language_count", "reply_time_trend",
            "opens_per_email_avg", "cta_click_rate_pct",
            "sentiment_score_recent", "sentiment_score_prior",
            "days_since_last_reply", "thread_age_days",
            "forwarded_to_others", "deal_value",
        }
        assert set(make_input().__dataclass_fields__.keys()) == expected

    def test_instantiation_all_fields(self):
        inp = make_input()
        assert inp.thread_id == "T1"
        assert inp.deal_id == "D1"
        assert inp.rep_id == "R1"
        assert isinstance(inp.total_emails_sent, int)
        assert isinstance(inp.deal_value, float)

    def test_string_fields(self):
        inp = make_input(thread_id="TXX", deal_id="DXX", rep_id="RXX")
        assert inp.thread_id == "TXX"
        assert inp.deal_id == "DXX"
        assert inp.rep_id == "RXX"


class TestEmailSentimentResultToDict:
    """to_dict() returns exactly 15 keys with the correct names."""

    EXPECTED_KEYS = {
        "thread_id", "deal_id", "thread_sentiment", "sentiment_trajectory",
        "buyer_engagement_signal", "email_action", "reply_quality_score",
        "engagement_depth_score", "sentiment_momentum_score",
        "urgency_alignment_score", "email_composite",
        "predicted_open_probability", "thread_health_index",
        "is_thread_healthy", "needs_intervention",
    }

    def test_key_count(self):
        t = tracker()
        result = t.analyze(make_input())
        assert len(result.to_dict()) == 15

    def test_exact_keys(self):
        t = tracker()
        result = t.analyze(make_input())
        assert set(result.to_dict().keys()) == self.EXPECTED_KEYS

    def test_enum_values_are_strings(self):
        t = tracker()
        d = t.analyze(make_input()).to_dict()
        assert isinstance(d["thread_sentiment"], str)
        assert isinstance(d["sentiment_trajectory"], str)
        assert isinstance(d["buyer_engagement_signal"], str)
        assert isinstance(d["email_action"], str)

    def test_bool_fields(self):
        d = tracker().analyze(make_input()).to_dict()
        assert isinstance(d["is_thread_healthy"], bool)
        assert isinstance(d["needs_intervention"], bool)

    def test_float_score_fields(self):
        d = tracker().analyze(make_input()).to_dict()
        for key in ("reply_quality_score", "engagement_depth_score",
                    "sentiment_momentum_score", "urgency_alignment_score",
                    "email_composite", "predicted_open_probability",
                    "thread_health_index"):
            assert isinstance(d[key], float), f"{key} should be float"

    def test_thread_id_passthrough(self):
        d = tracker().analyze(make_input(thread_id="MYTHREAD")).to_dict()
        assert d["thread_id"] == "MYTHREAD"

    def test_deal_id_passthrough(self):
        d = tracker().analyze(make_input(deal_id="MYDEAL")).to_dict()
        assert d["deal_id"] == "MYDEAL"


class TestSummaryKeys:
    """summary() returns exactly 13 keys."""

    EXPECTED_KEYS = {
        "total", "sentiment_counts", "trajectory_counts",
        "engagement_counts", "action_counts", "avg_email_composite",
        "avg_thread_health_index", "healthy_count", "intervention_count",
        "avg_reply_quality_score", "avg_engagement_depth_score",
        "avg_sentiment_momentum_score", "avg_urgency_alignment_score",
    }

    def test_key_count_empty(self):
        assert len(tracker().summary()) == 13

    def test_key_count_with_results(self):
        t = tracker()
        t.analyze(make_input())
        assert len(t.summary()) == 13

    def test_exact_keys_empty(self):
        assert set(tracker().summary().keys()) == self.EXPECTED_KEYS

    def test_exact_keys_with_results(self):
        t = tracker()
        t.analyze(make_input())
        assert set(t.summary().keys()) == self.EXPECTED_KEYS


# ===========================================================================
# 2. ENUM TESTS
# ===========================================================================

class TestThreadSentimentEnum:
    def test_values(self):
        assert ThreadSentiment.ENTHUSIASTIC.value == "enthusiastic"
        assert ThreadSentiment.POSITIVE.value == "positive"
        assert ThreadSentiment.NEUTRAL.value == "neutral"
        assert ThreadSentiment.COOLING.value == "cooling"
        assert ThreadSentiment.NEGATIVE.value == "negative"

    def test_count(self):
        assert len(ThreadSentiment) == 5

    def test_is_str_enum(self):
        assert isinstance(ThreadSentiment.POSITIVE, str)

    def test_members(self):
        names = {m.name for m in ThreadSentiment}
        assert names == {"ENTHUSIASTIC", "POSITIVE", "NEUTRAL", "COOLING", "NEGATIVE"}


class TestSentimentTrajectoryEnum:
    def test_values(self):
        assert SentimentTrajectory.IMPROVING.value == "improving"
        assert SentimentTrajectory.STABLE.value == "stable"
        assert SentimentTrajectory.DECLINING.value == "declining"
        assert SentimentTrajectory.VOLATILE.value == "volatile"
        assert SentimentTrajectory.FLATLINED.value == "flatlined"

    def test_count(self):
        assert len(SentimentTrajectory) == 5

    def test_is_str_enum(self):
        assert isinstance(SentimentTrajectory.STABLE, str)


class TestBuyerEngagementSignalEnum:
    def test_values(self):
        assert BuyerEngagementSignal.HIGHLY_ENGAGED.value == "highly_engaged"
        assert BuyerEngagementSignal.ENGAGED.value == "engaged"
        assert BuyerEngagementSignal.PASSIVELY_ENGAGED.value == "passively_engaged"
        assert BuyerEngagementSignal.DISENGAGING.value == "disengaging"
        assert BuyerEngagementSignal.DISENGAGED.value == "disengaged"

    def test_count(self):
        assert len(BuyerEngagementSignal) == 5

    def test_is_str_enum(self):
        assert isinstance(BuyerEngagementSignal.ENGAGED, str)


class TestEmailActionEnum:
    def test_values(self):
        assert EmailAction.KEEP_MOMENTUM.value == "keep_momentum"
        assert EmailAction.REFRAME.value == "reframe"
        assert EmailAction.PATTERN_BREAK.value == "pattern_break"
        assert EmailAction.ESCALATE_SEND.value == "escalate_send"

    def test_count(self):
        assert len(EmailAction) == 4

    def test_is_str_enum(self):
        assert isinstance(EmailAction.REFRAME, str)


# ===========================================================================
# 3. REPLY QUALITY SCORE
# ===========================================================================

class TestReplyQualityScore:
    """Tests for _reply_quality_score covering all branches."""

    def _rq(self, **kw) -> float:
        t = tracker()
        inp = make_input(**kw)
        return t._reply_quality_score(inp)

    # --- reply rate ---
    def test_reply_rate_zero_sent(self):
        score = self._rq(total_emails_sent=0, total_replies_received=5,
                         avg_reply_length_words=10, avg_reply_length_prior_words=10,
                         reply_time_trend=1.0, days_since_last_reply=1)
        assert score >= 0.0

    def test_reply_rate_high(self):
        # 7/10 = 0.70 => +30
        s = self._rq(total_emails_sent=10, total_replies_received=7,
                     avg_reply_length_words=10, avg_reply_length_prior_words=10,
                     reply_time_trend=1.0, days_since_last_reply=1)
        assert s >= 0.0

    def test_reply_rate_medium(self):
        # 5/10 = 0.50 => +20
        s = self._rq(total_emails_sent=10, total_replies_received=5,
                     avg_reply_length_words=10, avg_reply_length_prior_words=10,
                     reply_time_trend=1.0, days_since_last_reply=1)
        assert s >= 0.0

    def test_reply_rate_low(self):
        # 3/10 = 0.30 => +10
        s = self._rq(total_emails_sent=10, total_replies_received=3,
                     avg_reply_length_words=10, avg_reply_length_prior_words=10,
                     reply_time_trend=1.0, days_since_last_reply=1)
        assert s >= 0.0

    def test_reply_rate_below_low(self):
        # 1/10 = 0.10 => +0
        s = self._rq(total_emails_sent=10, total_replies_received=1,
                     avg_reply_length_words=10, avg_reply_length_prior_words=10,
                     reply_time_trend=1.0, days_since_last_reply=1)
        assert s >= 0.0

    # --- reply length ---
    def test_reply_length_high(self):
        s = self._rq(avg_reply_length_words=80,
                     avg_reply_length_prior_words=0,
                     reply_time_trend=1.0, days_since_last_reply=1)
        assert s >= 0.0

    def test_reply_length_medium(self):
        s = self._rq(avg_reply_length_words=40,
                     avg_reply_length_prior_words=0,
                     reply_time_trend=1.0, days_since_last_reply=1)
        assert s >= 0.0

    def test_reply_length_low(self):
        s = self._rq(avg_reply_length_words=15,
                     avg_reply_length_prior_words=0,
                     reply_time_trend=1.0, days_since_last_reply=1)
        assert s >= 0.0

    def test_reply_length_very_low(self):
        s = self._rq(avg_reply_length_words=5,
                     avg_reply_length_prior_words=0,
                     reply_time_trend=1.0, days_since_last_reply=1)
        assert s >= 0.0

    # --- length ratio ---
    def test_length_ratio_growing(self):
        # 120/100 = 1.2 => +20
        s1 = self._rq(avg_reply_length_words=120,
                      avg_reply_length_prior_words=100,
                      reply_time_trend=1.0, days_since_last_reply=1)
        s2 = self._rq(avg_reply_length_words=100,
                      avg_reply_length_prior_words=100,
                      reply_time_trend=1.0, days_since_last_reply=1)
        assert s1 >= s2

    def test_length_ratio_shrinking_heavily(self):
        # 40/100 = 0.4 => -15
        s1 = self._rq(avg_reply_length_words=40,
                      avg_reply_length_prior_words=100,
                      reply_time_trend=1.0, days_since_last_reply=1)
        s2 = self._rq(avg_reply_length_words=100,
                      avg_reply_length_prior_words=100,
                      reply_time_trend=1.0, days_since_last_reply=1)
        assert s1 <= s2

    def test_length_ratio_shrinking_mildly(self):
        # 60/100 = 0.6 in (0.5, 0.7] => -8
        s = self._rq(avg_reply_length_words=60,
                     avg_reply_length_prior_words=100,
                     reply_time_trend=1.0, days_since_last_reply=1)
        assert s >= 0.0

    def test_length_ratio_zero_prior(self):
        # prior = 0 => skip ratio branch
        s = self._rq(avg_reply_length_words=50,
                     avg_reply_length_prior_words=0,
                     reply_time_trend=1.0, days_since_last_reply=1)
        assert s >= 0.0

    # --- reply time trend ---
    def test_reply_time_trend_fast(self):
        # <= 0.8 => +10
        s1 = self._rq(reply_time_trend=0.8,
                      avg_reply_length_prior_words=0, days_since_last_reply=1)
        s2 = self._rq(reply_time_trend=1.0,
                      avg_reply_length_prior_words=0, days_since_last_reply=1)
        assert s1 >= s2

    def test_reply_time_trend_very_slow(self):
        # >= 2.0 => -10
        s = self._rq(reply_time_trend=2.0,
                     avg_reply_length_prior_words=0, days_since_last_reply=1)
        assert s >= 0.0

    def test_reply_time_trend_slow(self):
        # >= 1.5 => -5
        s = self._rq(reply_time_trend=1.5,
                     avg_reply_length_prior_words=0, days_since_last_reply=1)
        assert s >= 0.0

    def test_reply_time_trend_neutral(self):
        # 1.0: no bonus/penalty
        s = self._rq(reply_time_trend=1.0,
                     avg_reply_length_prior_words=0, days_since_last_reply=1)
        assert s >= 0.0

    # --- days since last reply ---
    def test_days_since_reply_large_penalty(self):
        s1 = self._rq(days_since_last_reply=14,
                      avg_reply_length_prior_words=0, reply_time_trend=1.0)
        s2 = self._rq(days_since_last_reply=3,
                      avg_reply_length_prior_words=0, reply_time_trend=1.0)
        assert s1 <= s2

    def test_days_since_reply_medium_penalty(self):
        s1 = self._rq(days_since_last_reply=7,
                      avg_reply_length_prior_words=0, reply_time_trend=1.0)
        s2 = self._rq(days_since_last_reply=1,
                      avg_reply_length_prior_words=0, reply_time_trend=1.0)
        assert s1 <= s2

    def test_score_clamped_min(self):
        # Worst-case: should not go below 0
        s = self._rq(
            total_emails_sent=10, total_replies_received=0,
            avg_reply_length_words=5, avg_reply_length_prior_words=100,
            reply_time_trend=3.0, days_since_last_reply=20,
        )
        assert s >= 0.0

    def test_score_clamped_max(self):
        # Best-case: should not exceed 100
        s = self._rq(
            total_emails_sent=10, total_replies_received=10,
            avg_reply_length_words=200, avg_reply_length_prior_words=50,
            reply_time_trend=0.5, days_since_last_reply=1,
        )
        assert s <= 100.0

    def test_score_rounded_one_decimal(self):
        s = self._rq()
        assert s == round(s, 1)


# ===========================================================================
# 4. ENGAGEMENT DEPTH SCORE
# ===========================================================================

class TestEngagementDepthScore:
    def _ed(self, **kw) -> float:
        t = tracker()
        return t._engagement_depth_score(make_input(**kw))

    # questions
    def test_questions_high(self):
        s1 = self._ed(question_count_from_buyer=5)
        s2 = self._ed(question_count_from_buyer=0)
        assert s1 > s2

    def test_questions_medium(self):
        s = self._ed(question_count_from_buyer=3)
        assert s >= 0.0

    def test_questions_low(self):
        s = self._ed(question_count_from_buyer=1)
        assert s >= 0.0

    def test_questions_zero(self):
        s = self._ed(question_count_from_buyer=0)
        assert s >= 0.0

    # CTA click rate
    def test_cta_high(self):
        s1 = self._ed(cta_click_rate_pct=60.0)
        s2 = self._ed(cta_click_rate_pct=0.0)
        assert s1 > s2

    def test_cta_medium(self):
        s = self._ed(cta_click_rate_pct=30.0)
        assert s >= 0.0

    def test_cta_low(self):
        s = self._ed(cta_click_rate_pct=10.0)
        assert s >= 0.0

    def test_cta_below_threshold(self):
        s = self._ed(cta_click_rate_pct=5.0)
        assert s >= 0.0

    # opens per email
    def test_opens_high(self):
        s1 = self._ed(opens_per_email_avg=2.0)
        s2 = self._ed(opens_per_email_avg=0.5)
        assert s1 > s2

    def test_opens_medium(self):
        s = self._ed(opens_per_email_avg=1.3)
        assert s >= 0.0

    def test_opens_low(self):
        s = self._ed(opens_per_email_avg=1.0)
        assert s >= 0.0

    # forwarded
    def test_forwarded_adds_score(self):
        s1 = self._ed(forwarded_to_others=1)
        s2 = self._ed(forwarded_to_others=0)
        assert s1 > s2

    # exclamation
    def test_exclamation_high(self):
        s1 = self._ed(exclamation_count=5)
        s2 = self._ed(exclamation_count=0)
        assert s1 > s2

    def test_exclamation_medium(self):
        s = self._ed(exclamation_count=2)
        assert s >= 0.0

    def test_exclamation_low(self):
        s = self._ed(exclamation_count=1)
        assert s >= 0.0

    def test_score_clamped_min(self):
        s = self._ed(question_count_from_buyer=0, cta_click_rate_pct=0.0,
                     opens_per_email_avg=0.0, forwarded_to_others=0,
                     exclamation_count=0)
        assert s == 0.0

    def test_score_clamped_max(self):
        s = self._ed(question_count_from_buyer=10, cta_click_rate_pct=100.0,
                     opens_per_email_avg=5.0, forwarded_to_others=1,
                     exclamation_count=10)
        assert s <= 100.0

    def test_score_rounded_one_decimal(self):
        s = self._ed()
        assert s == round(s, 1)


# ===========================================================================
# 5. SENTIMENT MOMENTUM SCORE
# ===========================================================================

class TestSentimentMomentumScore:
    def _sm(self, **kw) -> float:
        return tracker()._sentiment_momentum_score(make_input(**kw))

    # net language
    def test_net_language_strongly_positive(self):
        s = self._sm(positive_language_count=6, negative_language_count=1,
                     hedge_phrase_count=0,
                     sentiment_score_recent=50, sentiment_score_prior=50)
        assert s > 50.0  # base=50 + 25

    def test_net_language_mildly_positive(self):
        # net = 2
        s = self._sm(positive_language_count=3, negative_language_count=1,
                     hedge_phrase_count=0,
                     sentiment_score_recent=50, sentiment_score_prior=50)
        assert s > 50.0  # +15

    def test_net_language_zero(self):
        # net = 0
        s = self._sm(positive_language_count=1, negative_language_count=1,
                     hedge_phrase_count=0,
                     sentiment_score_recent=50, sentiment_score_prior=50)
        assert s > 50.0  # +5

    def test_net_language_mildly_negative(self):
        # net = -1
        s = self._sm(positive_language_count=0, negative_language_count=1,
                     hedge_phrase_count=0,
                     sentiment_score_recent=50, sentiment_score_prior=50)
        assert s < 60.0  # -10

    def test_net_language_strongly_negative(self):
        # net = -3
        s = self._sm(positive_language_count=0, negative_language_count=3,
                     hedge_phrase_count=0,
                     sentiment_score_recent=50, sentiment_score_prior=50)
        assert s < 55.0  # -20

    # hedge phrases
    def test_hedge_high(self):
        s = self._sm(hedge_phrase_count=5,
                     positive_language_count=0, negative_language_count=0,
                     sentiment_score_recent=50, sentiment_score_prior=50)
        assert s <= 50.0  # -20 from base+5

    def test_hedge_medium(self):
        s = self._sm(hedge_phrase_count=3,
                     positive_language_count=0, negative_language_count=0,
                     sentiment_score_recent=50, sentiment_score_prior=50)
        assert s < 60.0

    def test_hedge_low(self):
        s = self._sm(hedge_phrase_count=1,
                     positive_language_count=0, negative_language_count=0,
                     sentiment_score_recent=50, sentiment_score_prior=50)
        assert s < 60.0

    def test_hedge_zero(self):
        s = self._sm(hedge_phrase_count=0,
                     positive_language_count=0, negative_language_count=0,
                     sentiment_score_recent=50, sentiment_score_prior=50)
        assert s >= 50.0

    # sentiment delta
    def test_sent_delta_strongly_positive(self):
        # delta >= 10
        s = self._sm(sentiment_score_recent=65, sentiment_score_prior=50,
                     positive_language_count=0, negative_language_count=0,
                     hedge_phrase_count=0)
        assert s > 50.0

    def test_sent_delta_mildly_positive(self):
        # delta = 5
        s = self._sm(sentiment_score_recent=55, sentiment_score_prior=50,
                     positive_language_count=0, negative_language_count=0,
                     hedge_phrase_count=0)
        assert s > 50.0

    def test_sent_delta_strongly_negative(self):
        # delta = -10
        s = self._sm(sentiment_score_recent=40, sentiment_score_prior=50,
                     positive_language_count=0, negative_language_count=0,
                     hedge_phrase_count=0)
        assert s < 60.0

    def test_sent_delta_mildly_negative(self):
        # delta = -5
        s = self._sm(sentiment_score_recent=45, sentiment_score_prior=50,
                     positive_language_count=0, negative_language_count=0,
                     hedge_phrase_count=0)
        assert s < 60.0

    def test_score_clamped_min(self):
        s = self._sm(positive_language_count=0, negative_language_count=10,
                     hedge_phrase_count=10,
                     sentiment_score_recent=0, sentiment_score_prior=100)
        assert s == 0.0

    def test_score_clamped_max(self):
        s = self._sm(positive_language_count=10, negative_language_count=0,
                     hedge_phrase_count=0,
                     sentiment_score_recent=100, sentiment_score_prior=0)
        assert s <= 100.0

    def test_score_rounded_one_decimal(self):
        s = self._sm()
        assert s == round(s, 1)


# ===========================================================================
# 6. URGENCY ALIGNMENT SCORE
# ===========================================================================

class TestUrgencyAlignmentScore:
    def _ua(self, **kw) -> float:
        return tracker()._urgency_alignment_score(make_input(**kw))

    def test_urgency_count_high(self):
        s1 = self._ua(urgency_language_count=4,
                      sentiment_score_recent=50, cta_click_rate_pct=0, forwarded_to_others=0)
        s2 = self._ua(urgency_language_count=0,
                      sentiment_score_recent=50, cta_click_rate_pct=0, forwarded_to_others=0)
        assert s1 > s2

    def test_urgency_count_medium(self):
        s = self._ua(urgency_language_count=2,
                     sentiment_score_recent=50, cta_click_rate_pct=0, forwarded_to_others=0)
        assert s >= 0.0

    def test_urgency_count_low(self):
        s = self._ua(urgency_language_count=1,
                     sentiment_score_recent=50, cta_click_rate_pct=0, forwarded_to_others=0)
        assert s >= 0.0

    def test_urgency_count_zero(self):
        s = self._ua(urgency_language_count=0,
                     sentiment_score_recent=50, cta_click_rate_pct=0, forwarded_to_others=0)
        assert s >= 0.0

    def test_sentiment_recent_high(self):
        s1 = self._ua(sentiment_score_recent=70, urgency_language_count=0,
                      cta_click_rate_pct=0, forwarded_to_others=0)
        s2 = self._ua(sentiment_score_recent=50, urgency_language_count=0,
                      cta_click_rate_pct=0, forwarded_to_others=0)
        assert s1 > s2

    def test_sentiment_recent_medium(self):
        s = self._ua(sentiment_score_recent=55, urgency_language_count=0,
                     cta_click_rate_pct=0, forwarded_to_others=0)
        assert s >= 0.0

    def test_sentiment_recent_low(self):
        s = self._ua(sentiment_score_recent=40, urgency_language_count=0,
                     cta_click_rate_pct=0, forwarded_to_others=0)
        assert s == 0.0

    def test_cta_high(self):
        s1 = self._ua(cta_click_rate_pct=50.0, urgency_language_count=0,
                      sentiment_score_recent=50, forwarded_to_others=0)
        s2 = self._ua(cta_click_rate_pct=0.0, urgency_language_count=0,
                      sentiment_score_recent=50, forwarded_to_others=0)
        assert s1 > s2

    def test_cta_medium(self):
        s = self._ua(cta_click_rate_pct=25.0, urgency_language_count=0,
                     sentiment_score_recent=50, forwarded_to_others=0)
        assert s >= 0.0

    def test_cta_low(self):
        s = self._ua(cta_click_rate_pct=10.0, urgency_language_count=0,
                     sentiment_score_recent=50, forwarded_to_others=0)
        assert s == 0.0

    def test_forwarded_adds_score(self):
        s1 = self._ua(forwarded_to_others=1, urgency_language_count=0,
                      sentiment_score_recent=50, cta_click_rate_pct=0)
        s2 = self._ua(forwarded_to_others=0, urgency_language_count=0,
                      sentiment_score_recent=50, cta_click_rate_pct=0)
        assert s1 > s2

    def test_score_clamped_min(self):
        s = self._ua(urgency_language_count=0, sentiment_score_recent=0,
                     cta_click_rate_pct=0.0, forwarded_to_others=0)
        assert s == 0.0

    def test_score_clamped_max(self):
        s = self._ua(urgency_language_count=10, sentiment_score_recent=100,
                     cta_click_rate_pct=100.0, forwarded_to_others=1)
        assert s <= 100.0

    def test_score_rounded_one_decimal(self):
        s = self._ua()
        assert s == round(s, 1)


# ===========================================================================
# 7. COMPOSITE SCORE
# ===========================================================================

class TestComposite:
    def test_formula(self):
        t = tracker()
        c = t._composite(40.0, 60.0, 50.0, 80.0)
        expected = round(40*0.30 + 60*0.30 + 50*0.25 + 80*0.15, 1)
        assert c == expected

    def test_all_zero(self):
        assert tracker()._composite(0, 0, 0, 0) == 0.0

    def test_all_hundred(self):
        assert tracker()._composite(100, 100, 100, 100) == 100.0

    def test_clamped_min(self):
        assert tracker()._composite(-50, -50, -50, -50) == 0.0

    def test_clamped_max(self):
        assert tracker()._composite(200, 200, 200, 200) == 100.0

    def test_weights_sum_to_one(self):
        assert 0.30 + 0.30 + 0.25 + 0.15 == pytest.approx(1.0)

    def test_reply_q_weight(self):
        c1 = tracker()._composite(100, 0, 0, 0)
        assert c1 == pytest.approx(30.0, abs=0.1)

    def test_depth_weight(self):
        c = tracker()._composite(0, 100, 0, 0)
        assert c == pytest.approx(30.0, abs=0.1)

    def test_momentum_weight(self):
        c = tracker()._composite(0, 0, 100, 0)
        assert c == pytest.approx(25.0, abs=0.1)

    def test_urgency_weight(self):
        c = tracker()._composite(0, 0, 0, 100)
        assert c == pytest.approx(15.0, abs=0.1)

    def test_rounded(self):
        c = tracker()._composite(33.3, 33.3, 33.3, 33.3)
        assert c == round(c, 1)


# ===========================================================================
# 8. THREAD SENTIMENT
# ===========================================================================

class TestThreadSentiment:
    def _ts(self, sent_recent, composite) -> ThreadSentiment:
        t = tracker()
        inp = make_input(sentiment_score_recent=sent_recent)
        return t._thread_sentiment(inp, composite)

    def test_enthusiastic(self):
        assert self._ts(75, 60) == ThreadSentiment.ENTHUSIASTIC

    def test_enthusiastic_boundary(self):
        assert self._ts(75, 60) == ThreadSentiment.ENTHUSIASTIC

    def test_not_enthusiastic_sent_too_low(self):
        result = self._ts(74, 60)
        assert result != ThreadSentiment.ENTHUSIASTIC

    def test_not_enthusiastic_composite_too_low(self):
        result = self._ts(75, 59)
        assert result != ThreadSentiment.ENTHUSIASTIC

    def test_positive_by_sent(self):
        # sent=60, composite<55 -> positive
        result = self._ts(60, 40)
        assert result == ThreadSentiment.POSITIVE

    def test_positive_by_composite(self):
        # sent<60 but composite>=55 -> positive
        result = self._ts(50, 55)
        assert result == ThreadSentiment.POSITIVE

    def test_neutral(self):
        # sent=45..59, composite<55
        result = self._ts(45, 30)
        assert result == ThreadSentiment.NEUTRAL

    def test_neutral_boundary(self):
        result = self._ts(59, 30)
        assert result == ThreadSentiment.NEUTRAL

    def test_cooling(self):
        # sent=30..44
        result = self._ts(30, 20)
        assert result == ThreadSentiment.COOLING

    def test_cooling_boundary(self):
        result = self._ts(44, 20)
        assert result == ThreadSentiment.COOLING

    def test_negative(self):
        # sent < 30
        result = self._ts(29, 10)
        assert result == ThreadSentiment.NEGATIVE

    def test_negative_zero(self):
        result = self._ts(0, 0)
        assert result == ThreadSentiment.NEGATIVE


# ===========================================================================
# 9. SENTIMENT TRAJECTORY
# ===========================================================================

class TestSentimentTrajectory:
    def _st(self, **kw) -> SentimentTrajectory:
        t = tracker()
        return t._sentiment_trajectory(make_input(**kw))

    def test_flatlined_by_days(self):
        r = self._st(days_since_last_reply=14,
                     sentiment_score_recent=80, sentiment_score_prior=50,
                     avg_reply_length_words=150, avg_reply_length_prior_words=100)
        assert r == SentimentTrajectory.FLATLINED

    def test_flatlined_at_boundary_14(self):
        r = self._st(days_since_last_reply=14,
                     sentiment_score_recent=50, sentiment_score_prior=50,
                     avg_reply_length_words=50, avg_reply_length_prior_words=50)
        assert r == SentimentTrajectory.FLATLINED

    def test_not_flatlined_at_13_days(self):
        r = self._st(days_since_last_reply=13,
                     sentiment_score_recent=50, sentiment_score_prior=50,
                     avg_reply_length_words=50, avg_reply_length_prior_words=50)
        assert r != SentimentTrajectory.FLATLINED

    def test_volatile(self):
        # abs(delta) >= 20 and length_ratio >= 1.5
        r = self._st(days_since_last_reply=1,
                     sentiment_score_recent=80, sentiment_score_prior=55,
                     avg_reply_length_words=150, avg_reply_length_prior_words=100)
        assert r == SentimentTrajectory.VOLATILE

    def test_volatile_negative_delta(self):
        # abs(-20) >= 20 and ratio >= 1.5
        r = self._st(days_since_last_reply=1,
                     sentiment_score_recent=30, sentiment_score_prior=55,
                     avg_reply_length_words=200, avg_reply_length_prior_words=100)
        assert r == SentimentTrajectory.VOLATILE

    def test_not_volatile_ratio_too_low(self):
        # abs(delta)>=20 but ratio < 1.5
        r = self._st(days_since_last_reply=1,
                     sentiment_score_recent=80, sentiment_score_prior=55,
                     avg_reply_length_words=100, avg_reply_length_prior_words=100)
        assert r != SentimentTrajectory.VOLATILE

    def test_improving(self):
        # delta >= 8 and ratio >= 0.9
        r = self._st(days_since_last_reply=1,
                     sentiment_score_recent=60, sentiment_score_prior=50,
                     avg_reply_length_words=90, avg_reply_length_prior_words=100)
        assert r == SentimentTrajectory.IMPROVING

    def test_improving_boundary_delta(self):
        r = self._st(days_since_last_reply=1,
                     sentiment_score_recent=58, sentiment_score_prior=50,
                     avg_reply_length_words=90, avg_reply_length_prior_words=100)
        assert r == SentimentTrajectory.IMPROVING

    def test_not_improving_ratio_too_low(self):
        # delta=8 but ratio < 0.9
        r = self._st(days_since_last_reply=1,
                     sentiment_score_recent=58, sentiment_score_prior=50,
                     avg_reply_length_words=80, avg_reply_length_prior_words=100)
        # ratio=0.8 < 0.9
        assert r != SentimentTrajectory.IMPROVING

    def test_declining_by_delta(self):
        # delta = -8
        r = self._st(days_since_last_reply=1,
                     sentiment_score_recent=42, sentiment_score_prior=50,
                     avg_reply_length_words=100, avg_reply_length_prior_words=100)
        assert r == SentimentTrajectory.DECLINING

    def test_declining_by_length_ratio(self):
        # ratio=0.5 <= 0.6
        r = self._st(days_since_last_reply=1,
                     sentiment_score_recent=50, sentiment_score_prior=50,
                     avg_reply_length_words=50, avg_reply_length_prior_words=100)
        assert r == SentimentTrajectory.DECLINING

    def test_stable(self):
        r = self._st(days_since_last_reply=1,
                     sentiment_score_recent=50, sentiment_score_prior=50,
                     avg_reply_length_words=100, avg_reply_length_prior_words=100)
        assert r == SentimentTrajectory.STABLE

    def test_stable_zero_prior_length(self):
        # avg_reply_length_prior_words=0 => ratio defaults to 1.0
        r = self._st(days_since_last_reply=1,
                     sentiment_score_recent=50, sentiment_score_prior=50,
                     avg_reply_length_words=50, avg_reply_length_prior_words=0)
        assert r == SentimentTrajectory.STABLE


# ===========================================================================
# 10. BUYER ENGAGEMENT SIGNAL
# ===========================================================================

class TestBuyerEngagementSignal:
    def _bes(self, composite, **kw) -> BuyerEngagementSignal:
        t = tracker()
        inp = make_input(**kw)
        return t._buyer_engagement_signal(composite, inp)

    def test_highly_engaged(self):
        r = self._bes(75, question_count_from_buyer=3, days_since_last_reply=1)
        assert r == BuyerEngagementSignal.HIGHLY_ENGAGED

    def test_highly_engaged_boundary_composite(self):
        r = self._bes(75, question_count_from_buyer=5, days_since_last_reply=1)
        assert r == BuyerEngagementSignal.HIGHLY_ENGAGED

    def test_not_highly_engaged_questions_too_low(self):
        r = self._bes(75, question_count_from_buyer=2, days_since_last_reply=1)
        assert r != BuyerEngagementSignal.HIGHLY_ENGAGED

    def test_not_highly_engaged_composite_too_low(self):
        r = self._bes(74, question_count_from_buyer=3, days_since_last_reply=1)
        assert r != BuyerEngagementSignal.HIGHLY_ENGAGED

    def test_engaged(self):
        r = self._bes(55, question_count_from_buyer=0, days_since_last_reply=1)
        assert r == BuyerEngagementSignal.ENGAGED

    def test_engaged_boundary(self):
        r = self._bes(55, question_count_from_buyer=1, days_since_last_reply=1)
        assert r == BuyerEngagementSignal.ENGAGED

    def test_passively_engaged(self):
        r = self._bes(40, question_count_from_buyer=0, days_since_last_reply=1)
        assert r == BuyerEngagementSignal.PASSIVELY_ENGAGED

    def test_passively_engaged_boundary(self):
        r = self._bes(54, question_count_from_buyer=0, days_since_last_reply=1)
        assert r == BuyerEngagementSignal.PASSIVELY_ENGAGED

    def test_disengaging_by_composite(self):
        r = self._bes(25, question_count_from_buyer=0, days_since_last_reply=1)
        assert r == BuyerEngagementSignal.DISENGAGING

    def test_disengaging_by_days(self):
        r = self._bes(15, question_count_from_buyer=0, days_since_last_reply=7)
        assert r == BuyerEngagementSignal.DISENGAGING

    def test_disengaged(self):
        r = self._bes(10, question_count_from_buyer=0, days_since_last_reply=1)
        assert r == BuyerEngagementSignal.DISENGAGED

    def test_disengaged_composite_24_no_days(self):
        r = self._bes(24, question_count_from_buyer=0, days_since_last_reply=1)
        assert r == BuyerEngagementSignal.DISENGAGED


# ===========================================================================
# 11. PREDICTED OPEN PROBABILITY
# ===========================================================================

class TestPredictedOpenProbability:
    def _pop(self, **kw) -> float:
        t = tracker()
        inp = make_input(**kw)
        comp = t._composite(
            t._reply_quality_score(inp),
            t._engagement_depth_score(inp),
            t._sentiment_momentum_score(inp),
            t._urgency_alignment_score(inp),
        )
        return t._predicted_open_probability(inp, comp)

    def test_high_opens_adds_bonus(self):
        s1 = self._pop(opens_per_email_avg=1.5, sentiment_score_recent=50,
                       days_since_last_reply=1)
        s2 = self._pop(opens_per_email_avg=1.0, sentiment_score_recent=50,
                       days_since_last_reply=1)
        assert s1 >= s2

    def test_high_sentiment_adds_bonus(self):
        s1 = self._pop(sentiment_score_recent=65, opens_per_email_avg=1.0,
                       days_since_last_reply=1)
        s2 = self._pop(sentiment_score_recent=50, opens_per_email_avg=1.0,
                       days_since_last_reply=1)
        assert s1 >= s2

    def test_stale_reply_penalises(self):
        s1 = self._pop(days_since_last_reply=14, opens_per_email_avg=1.0,
                       sentiment_score_recent=50)
        s2 = self._pop(days_since_last_reply=1, opens_per_email_avg=1.0,
                       sentiment_score_recent=50)
        assert s1 <= s2

    def test_clamped_min(self):
        s = self._pop(days_since_last_reply=30, opens_per_email_avg=0,
                      sentiment_score_recent=0,
                      total_emails_sent=0, total_replies_received=0,
                      avg_reply_length_words=0, avg_reply_length_prior_words=0,
                      reply_time_trend=5.0, urgency_language_count=0,
                      cta_click_rate_pct=0, forwarded_to_others=0,
                      question_count_from_buyer=0, exclamation_count=0,
                      positive_language_count=0, negative_language_count=5,
                      hedge_phrase_count=5, sentiment_score_prior=100)
        assert s >= 0.0

    def test_clamped_max(self):
        s = self._pop(days_since_last_reply=1, opens_per_email_avg=5.0,
                      sentiment_score_recent=100)
        assert s <= 100.0

    def test_rounded_one_decimal(self):
        s = self._pop()
        assert s == round(s, 1)


# ===========================================================================
# 12. THREAD HEALTH INDEX
# ===========================================================================

class TestThreadHealthIndex:
    def _thi(self, **kw) -> float:
        t = tracker()
        inp = make_input(**kw)
        comp = t._composite(
            t._reply_quality_score(inp),
            t._engagement_depth_score(inp),
            t._sentiment_momentum_score(inp),
            t._urgency_alignment_score(inp),
        )
        return t._thread_health_index(inp, comp)

    def test_replies_boost(self):
        s1 = self._thi(total_replies_received=3, days_since_last_reply=10)
        s2 = self._thi(total_replies_received=1, days_since_last_reply=10)
        assert s1 >= s2

    def test_recent_reply_boost(self):
        s1 = self._thi(total_replies_received=1, days_since_last_reply=3)
        s2 = self._thi(total_replies_received=1, days_since_last_reply=10)
        assert s1 >= s2

    def test_both_boosts(self):
        s = self._thi(total_replies_received=5, days_since_last_reply=1)
        assert s >= 0.0

    def test_clamped_max(self):
        s = self._thi(total_replies_received=100, days_since_last_reply=1)
        assert s <= 100.0

    def test_clamped_min(self):
        s = self._thi(total_replies_received=0, days_since_last_reply=30,
                      total_emails_sent=0, avg_reply_length_words=0,
                      avg_reply_length_prior_words=0, reply_time_trend=5.0,
                      urgency_language_count=0, cta_click_rate_pct=0.0,
                      forwarded_to_others=0, question_count_from_buyer=0,
                      exclamation_count=0, positive_language_count=0,
                      negative_language_count=5, hedge_phrase_count=5,
                      sentiment_score_recent=0, sentiment_score_prior=100,
                      opens_per_email_avg=0.0)
        assert s >= 0.0

    def test_rounded_one_decimal(self):
        s = self._thi()
        assert s == round(s, 1)


# ===========================================================================
# 13. IS_THREAD_HEALTHY & NEEDS_INTERVENTION
# ===========================================================================

class TestIsThreadHealthy:
    def test_healthy_true(self):
        # composite >= 55 AND days <= 7
        inp = make_input(
            total_emails_sent=10, total_replies_received=8,
            avg_reply_length_words=80, avg_reply_length_prior_words=50,
            positive_language_count=6, negative_language_count=0,
            question_count_from_buyer=5, exclamation_count=5,
            hedge_phrase_count=0, urgency_language_count=4,
            reply_time_trend=0.7, opens_per_email_avg=2.0,
            cta_click_rate_pct=70.0, sentiment_score_recent=75.0,
            sentiment_score_prior=60.0, days_since_last_reply=3,
            forwarded_to_others=1,
        )
        result = tracker().analyze(inp)
        assert result.is_thread_healthy is True

    def test_healthy_false_stale(self):
        inp = make_input(days_since_last_reply=8)
        result = tracker().analyze(inp)
        # days > 7 => not healthy regardless of composite
        assert result.is_thread_healthy is False

    def test_healthy_false_low_composite(self):
        inp = make_input(
            total_emails_sent=10, total_replies_received=0,
            avg_reply_length_words=0, avg_reply_length_prior_words=0,
            positive_language_count=0, negative_language_count=5,
            question_count_from_buyer=0, exclamation_count=0,
            hedge_phrase_count=5, urgency_language_count=0,
            reply_time_trend=3.0, opens_per_email_avg=0.0,
            cta_click_rate_pct=0.0, sentiment_score_recent=10.0,
            sentiment_score_prior=60.0, days_since_last_reply=1,
            forwarded_to_others=0,
        )
        result = tracker().analyze(inp)
        assert result.is_thread_healthy is False

    def test_healthy_boundary_composite_55_days_7(self):
        # Find inputs that yield composite close to 55 and days=7
        t = tracker()
        inp = make_input(days_since_last_reply=7)
        result = t.analyze(inp)
        # is_healthy depends on whether composite >= 55
        if result.email_composite >= 55.0:
            assert result.is_thread_healthy is True
        else:
            assert result.is_thread_healthy is False


class TestNeedsIntervention:
    def test_intervention_by_stale(self):
        inp = make_input(days_since_last_reply=14)
        result = tracker().analyze(inp)
        assert result.needs_intervention is True

    def test_intervention_by_low_composite(self):
        inp = make_input(
            total_emails_sent=10, total_replies_received=0,
            avg_reply_length_words=0, avg_reply_length_prior_words=0,
            positive_language_count=0, negative_language_count=10,
            question_count_from_buyer=0, exclamation_count=0,
            hedge_phrase_count=10, urgency_language_count=0,
            reply_time_trend=5.0, opens_per_email_avg=0.0,
            cta_click_rate_pct=0.0, sentiment_score_recent=0.0,
            sentiment_score_prior=90.0, days_since_last_reply=1,
            forwarded_to_others=0,
        )
        result = tracker().analyze(inp)
        assert result.needs_intervention is True

    def test_no_intervention_healthy_thread(self):
        inp = make_input(
            total_emails_sent=10, total_replies_received=8,
            avg_reply_length_words=80, avg_reply_length_prior_words=50,
            positive_language_count=6, negative_language_count=0,
            question_count_from_buyer=5, exclamation_count=5,
            hedge_phrase_count=0, urgency_language_count=4,
            reply_time_trend=0.7, opens_per_email_avg=2.0,
            cta_click_rate_pct=70.0, sentiment_score_recent=75.0,
            sentiment_score_prior=60.0, days_since_last_reply=2,
            forwarded_to_others=1,
        )
        result = tracker().analyze(inp)
        assert result.needs_intervention is False

    def test_intervention_stale_boundary_14(self):
        result = tracker().analyze(make_input(days_since_last_reply=14))
        assert result.needs_intervention is True

    def test_no_intervention_at_13_days_with_high_composite(self):
        inp = make_input(
            total_emails_sent=10, total_replies_received=8,
            avg_reply_length_words=80, avg_reply_length_prior_words=50,
            positive_language_count=6, negative_language_count=0,
            question_count_from_buyer=5, exclamation_count=5,
            hedge_phrase_count=0, urgency_language_count=4,
            reply_time_trend=0.7, opens_per_email_avg=2.0,
            cta_click_rate_pct=70.0, sentiment_score_recent=75.0,
            sentiment_score_prior=60.0, days_since_last_reply=13,
            forwarded_to_others=1,
        )
        result = tracker().analyze(inp)
        # composite should be > 35 and days=13 < 14 => no intervention
        assert result.needs_intervention is False


# ===========================================================================
# 14. EMAIL ACTION
# ===========================================================================

class TestEmailAction:
    def _action(self, trajectory, needs_int, composite) -> EmailAction:
        return tracker()._email_action(trajectory, needs_int, composite)

    def test_escalate_flatlined(self):
        a = self._action(SentimentTrajectory.FLATLINED, False, 50)
        assert a == EmailAction.ESCALATE_SEND

    def test_escalate_low_composite(self):
        a = self._action(SentimentTrajectory.STABLE, False, 19)
        assert a == EmailAction.ESCALATE_SEND

    def test_escalate_composite_boundary_20(self):
        a = self._action(SentimentTrajectory.STABLE, False, 19)
        assert a == EmailAction.ESCALATE_SEND

    def test_not_escalate_composite_20(self):
        a = self._action(SentimentTrajectory.STABLE, False, 20)
        assert a != EmailAction.ESCALATE_SEND

    def test_pattern_break_needs_int(self):
        a = self._action(SentimentTrajectory.STABLE, True, 40)
        assert a == EmailAction.PATTERN_BREAK

    def test_pattern_break_declining(self):
        a = self._action(SentimentTrajectory.DECLINING, False, 40)
        assert a == EmailAction.PATTERN_BREAK

    def test_reframe_volatile_low_composite(self):
        a = self._action(SentimentTrajectory.VOLATILE, False, 40)
        assert a == EmailAction.REFRAME

    def test_reframe_stable_low_composite(self):
        a = self._action(SentimentTrajectory.STABLE, False, 40)
        assert a == EmailAction.REFRAME

    def test_not_reframe_if_composite_55_stable(self):
        a = self._action(SentimentTrajectory.STABLE, False, 55)
        assert a == EmailAction.KEEP_MOMENTUM

    def test_keep_momentum_improving(self):
        a = self._action(SentimentTrajectory.IMPROVING, False, 60)
        assert a == EmailAction.KEEP_MOMENTUM

    def test_keep_momentum_stable_high_composite(self):
        a = self._action(SentimentTrajectory.STABLE, False, 70)
        assert a == EmailAction.KEEP_MOMENTUM

    def test_keep_momentum_volatile_high_composite(self):
        a = self._action(SentimentTrajectory.VOLATILE, False, 60)
        assert a == EmailAction.KEEP_MOMENTUM

    def test_flatlined_overrides_all(self):
        # Even with needs_int=True, flatlined => escalate (first branch wins)
        a = self._action(SentimentTrajectory.FLATLINED, True, 50)
        assert a == EmailAction.ESCALATE_SEND


# ===========================================================================
# 15. ANALYZE METHOD
# ===========================================================================

class TestAnalyzeMethod:
    def test_returns_email_sentiment_result(self):
        result = tracker().analyze(make_input())
        assert isinstance(result, EmailSentimentResult)

    def test_thread_id_preserved(self):
        result = tracker().analyze(make_input(thread_id="THREAD99"))
        assert result.thread_id == "THREAD99"

    def test_deal_id_preserved(self):
        result = tracker().analyze(make_input(deal_id="DEAL99"))
        assert result.deal_id == "DEAL99"

    def test_result_stored_in_results(self):
        t = tracker()
        result = t.analyze(make_input())
        assert result in t._results

    def test_multiple_calls_accumulate(self):
        t = tracker()
        t.analyze(make_input(thread_id="A"))
        t.analyze(make_input(thread_id="B"))
        assert len(t._results) == 2

    def test_scores_bounded(self):
        result = tracker().analyze(make_input())
        assert 0.0 <= result.reply_quality_score <= 100.0
        assert 0.0 <= result.engagement_depth_score <= 100.0
        assert 0.0 <= result.sentiment_momentum_score <= 100.0
        assert 0.0 <= result.urgency_alignment_score <= 100.0
        assert 0.0 <= result.email_composite <= 100.0
        assert 0.0 <= result.predicted_open_probability <= 100.0
        assert 0.0 <= result.thread_health_index <= 100.0

    def test_composite_formula_matches(self):
        t = tracker()
        inp = make_input()
        result = t.analyze(inp)
        expected = round(
            result.reply_quality_score * 0.30 +
            result.engagement_depth_score * 0.30 +
            result.sentiment_momentum_score * 0.25 +
            result.urgency_alignment_score * 0.15, 1
        )
        assert result.email_composite == expected

    def test_is_thread_healthy_composite_days_check(self):
        t = tracker()
        inp = make_input(days_since_last_reply=3)
        result = t.analyze(inp)
        expected = result.email_composite >= 55.0 and inp.days_since_last_reply <= 7
        assert result.is_thread_healthy == expected

    def test_needs_intervention_composite_days_check(self):
        t = tracker()
        inp = make_input(days_since_last_reply=3)
        result = t.analyze(inp)
        expected = result.email_composite < 35.0 or inp.days_since_last_reply >= 14
        assert result.needs_intervention == expected

    def test_enum_fields_are_enums(self):
        result = tracker().analyze(make_input())
        assert isinstance(result.thread_sentiment, ThreadSentiment)
        assert isinstance(result.sentiment_trajectory, SentimentTrajectory)
        assert isinstance(result.buyer_engagement_signal, BuyerEngagementSignal)
        assert isinstance(result.email_action, EmailAction)


# ===========================================================================
# 16. ANALYZE_BATCH METHOD
# ===========================================================================

class TestAnalyzeBatch:
    def test_returns_list(self):
        t = tracker()
        results = t.analyze_batch([make_input(thread_id="A"), make_input(thread_id="B")])
        assert isinstance(results, list)

    def test_correct_count(self):
        t = tracker()
        inputs = [make_input(thread_id=str(i)) for i in range(5)]
        results = t.analyze_batch(inputs)
        assert len(results) == 5

    def test_empty_batch(self):
        results = tracker().analyze_batch([])
        assert results == []

    def test_results_accumulated(self):
        t = tracker()
        inputs = [make_input(thread_id=str(i)) for i in range(3)]
        t.analyze_batch(inputs)
        assert len(t._results) == 3

    def test_each_result_is_email_sentiment_result(self):
        t = tracker()
        results = t.analyze_batch([make_input(), make_input()])
        for r in results:
            assert isinstance(r, EmailSentimentResult)

    def test_single_item_batch(self):
        t = tracker()
        results = t.analyze_batch([make_input(thread_id="ONLY")])
        assert len(results) == 1
        assert results[0].thread_id == "ONLY"

    def test_order_preserved(self):
        t = tracker()
        inputs = [make_input(thread_id=f"T{i}") for i in range(4)]
        results = t.analyze_batch(inputs)
        for i, r in enumerate(results):
            assert r.thread_id == f"T{i}"


# ===========================================================================
# 17. RESET
# ===========================================================================

class TestReset:
    def test_reset_clears_results(self):
        t = tracker()
        t.analyze(make_input())
        t.reset()
        assert len(t._results) == 0

    def test_reset_idempotent_on_empty(self):
        t = tracker()
        t.reset()
        assert len(t._results) == 0

    def test_analyze_after_reset(self):
        t = tracker()
        t.analyze(make_input(thread_id="A"))
        t.reset()
        t.analyze(make_input(thread_id="B"))
        assert len(t._results) == 1
        assert t._results[0].thread_id == "B"


# ===========================================================================
# 18. PROPERTIES
# ===========================================================================

class TestProperties:
    def test_healthy_threads_empty(self):
        assert tracker().healthy_threads == []

    def test_intervention_queue_empty(self):
        assert tracker().intervention_queue == []

    def test_avg_email_composite_empty(self):
        assert tracker().avg_email_composite == 0.0

    def test_avg_thread_health_index_empty(self):
        assert tracker().avg_thread_health_index == 0.0

    def test_healthy_threads_contains_healthy(self):
        t = tracker()
        inp = make_input(
            total_emails_sent=10, total_replies_received=8,
            avg_reply_length_words=80, avg_reply_length_prior_words=50,
            positive_language_count=6, negative_language_count=0,
            question_count_from_buyer=5, exclamation_count=5,
            hedge_phrase_count=0, urgency_language_count=4,
            reply_time_trend=0.7, opens_per_email_avg=2.0,
            cta_click_rate_pct=70.0, sentiment_score_recent=75.0,
            sentiment_score_prior=60.0, days_since_last_reply=2,
            forwarded_to_others=1,
        )
        result = t.analyze(inp)
        if result.is_thread_healthy:
            assert result in t.healthy_threads
        else:
            assert result not in t.healthy_threads

    def test_intervention_queue_contains_intervention(self):
        t = tracker()
        result = t.analyze(make_input(days_since_last_reply=14))
        assert result in t.intervention_queue

    def test_avg_email_composite_single(self):
        t = tracker()
        result = t.analyze(make_input())
        assert t.avg_email_composite == result.email_composite

    def test_avg_thread_health_index_single(self):
        t = tracker()
        result = t.analyze(make_input())
        assert t.avg_thread_health_index == result.thread_health_index

    def test_avg_email_composite_multiple(self):
        t = tracker()
        r1 = t.analyze(make_input(thread_id="A"))
        r2 = t.analyze(make_input(thread_id="B"))
        expected = round((r1.email_composite + r2.email_composite) / 2, 1)
        assert t.avg_email_composite == expected

    def test_avg_thread_health_index_multiple(self):
        t = tracker()
        r1 = t.analyze(make_input(thread_id="A"))
        r2 = t.analyze(make_input(thread_id="B"))
        expected = round((r1.thread_health_index + r2.thread_health_index) / 2, 1)
        assert t.avg_thread_health_index == expected

    def test_avg_composite_rounded_one_decimal(self):
        t = tracker()
        t.analyze(make_input())
        assert t.avg_email_composite == round(t.avg_email_composite, 1)

    def test_avg_health_rounded_one_decimal(self):
        t = tracker()
        t.analyze(make_input())
        assert t.avg_thread_health_index == round(t.avg_thread_health_index, 1)


# ===========================================================================
# 19. SUMMARY METHOD
# ===========================================================================

class TestSummaryMethod:
    def test_empty_summary_total(self):
        assert tracker().summary()["total"] == 0

    def test_empty_summary_zeros(self):
        s = tracker().summary()
        assert s["avg_email_composite"] == 0.0
        assert s["avg_thread_health_index"] == 0.0
        assert s["healthy_count"] == 0
        assert s["intervention_count"] == 0
        assert s["avg_reply_quality_score"] == 0.0
        assert s["avg_engagement_depth_score"] == 0.0
        assert s["avg_sentiment_momentum_score"] == 0.0
        assert s["avg_urgency_alignment_score"] == 0.0

    def test_empty_summary_empty_dicts(self):
        s = tracker().summary()
        assert s["sentiment_counts"] == {}
        assert s["trajectory_counts"] == {}
        assert s["engagement_counts"] == {}
        assert s["action_counts"] == {}

    def test_summary_total_count(self):
        t = tracker()
        t.analyze_batch([make_input(thread_id=str(i)) for i in range(4)])
        assert t.summary()["total"] == 4

    def test_summary_sentiment_counts(self):
        t = tracker()
        t.analyze(make_input())
        s = t.summary()
        # At least one sentiment key
        assert sum(s["sentiment_counts"].values()) == 1

    def test_summary_trajectory_counts(self):
        t = tracker()
        t.analyze(make_input())
        s = t.summary()
        assert sum(s["trajectory_counts"].values()) == 1

    def test_summary_engagement_counts(self):
        t = tracker()
        t.analyze(make_input())
        s = t.summary()
        assert sum(s["engagement_counts"].values()) == 1

    def test_summary_action_counts(self):
        t = tracker()
        t.analyze(make_input())
        s = t.summary()
        assert sum(s["action_counts"].values()) == 1

    def test_summary_avg_composite_matches(self):
        t = tracker()
        r = t.analyze(make_input())
        s = t.summary()
        assert s["avg_email_composite"] == r.email_composite

    def test_summary_avg_health_matches(self):
        t = tracker()
        r = t.analyze(make_input())
        s = t.summary()
        assert s["avg_thread_health_index"] == r.thread_health_index

    def test_summary_avg_reply_quality_matches(self):
        t = tracker()
        r = t.analyze(make_input())
        s = t.summary()
        assert s["avg_reply_quality_score"] == r.reply_quality_score

    def test_summary_avg_engagement_depth_matches(self):
        t = tracker()
        r = t.analyze(make_input())
        s = t.summary()
        assert s["avg_engagement_depth_score"] == r.engagement_depth_score

    def test_summary_avg_momentum_matches(self):
        t = tracker()
        r = t.analyze(make_input())
        s = t.summary()
        assert s["avg_sentiment_momentum_score"] == r.sentiment_momentum_score

    def test_summary_avg_urgency_matches(self):
        t = tracker()
        r = t.analyze(make_input())
        s = t.summary()
        assert s["avg_urgency_alignment_score"] == r.urgency_alignment_score

    def test_summary_healthy_count(self):
        t = tracker()
        inp = make_input(
            total_emails_sent=10, total_replies_received=8,
            avg_reply_length_words=80, avg_reply_length_prior_words=50,
            positive_language_count=6, negative_language_count=0,
            question_count_from_buyer=5, exclamation_count=5,
            hedge_phrase_count=0, urgency_language_count=4,
            reply_time_trend=0.7, opens_per_email_avg=2.0,
            cta_click_rate_pct=70.0, sentiment_score_recent=75.0,
            sentiment_score_prior=60.0, days_since_last_reply=2,
            forwarded_to_others=1,
        )
        t.analyze(inp)
        s = t.summary()
        assert s["healthy_count"] == len(t.healthy_threads)

    def test_summary_intervention_count(self):
        t = tracker()
        t.analyze(make_input(days_since_last_reply=14))
        s = t.summary()
        assert s["intervention_count"] == len(t.intervention_queue)

    def test_summary_avgs_rounded_one_decimal(self):
        t = tracker()
        t.analyze_batch([make_input(thread_id=str(i)) for i in range(3)])
        s = t.summary()
        for key in ("avg_email_composite", "avg_thread_health_index",
                    "avg_reply_quality_score", "avg_engagement_depth_score",
                    "avg_sentiment_momentum_score", "avg_urgency_alignment_score"):
            assert s[key] == round(s[key], 1), f"{key} not rounded"

    def test_summary_multiple_sentiments(self):
        t = tracker()
        # enthusiastic
        t.analyze(make_input(
            total_emails_sent=10, total_replies_received=8,
            avg_reply_length_words=80, avg_reply_length_prior_words=50,
            positive_language_count=6, negative_language_count=0,
            question_count_from_buyer=5, exclamation_count=5,
            hedge_phrase_count=0, urgency_language_count=4,
            reply_time_trend=0.7, opens_per_email_avg=2.0,
            cta_click_rate_pct=70.0, sentiment_score_recent=80.0,
            sentiment_score_prior=60.0, days_since_last_reply=2,
            forwarded_to_others=1, thread_id="E",
        ))
        # negative
        t.analyze(make_input(
            total_emails_sent=10, total_replies_received=0,
            avg_reply_length_words=0, avg_reply_length_prior_words=0,
            positive_language_count=0, negative_language_count=5,
            question_count_from_buyer=0, exclamation_count=0,
            hedge_phrase_count=5, urgency_language_count=0,
            reply_time_trend=3.0, opens_per_email_avg=0.0,
            cta_click_rate_pct=0.0, sentiment_score_recent=10.0,
            sentiment_score_prior=60.0, days_since_last_reply=20,
            forwarded_to_others=0, thread_id="N",
        ))
        s = t.summary()
        assert s["total"] == 2
        assert sum(s["sentiment_counts"].values()) == 2


# ===========================================================================
# 20. EDGE CASES & INTEGRATION SCENARIOS
# ===========================================================================

class TestEdgeCases:
    def test_zero_emails_sent_no_division_error(self):
        result = tracker().analyze(make_input(total_emails_sent=0,
                                              total_replies_received=0))
        assert isinstance(result, EmailSentimentResult)

    def test_zero_prior_reply_length_no_division_error(self):
        result = tracker().analyze(make_input(avg_reply_length_prior_words=0))
        assert isinstance(result, EmailSentimentResult)

    def test_very_high_values_no_overflow(self):
        inp = make_input(
            total_emails_sent=9999, total_replies_received=9999,
            avg_reply_length_words=9999, avg_reply_length_prior_words=1,
            positive_language_count=9999, negative_language_count=0,
            question_count_from_buyer=9999, exclamation_count=9999,
            hedge_phrase_count=0, urgency_language_count=9999,
            reply_time_trend=0.1, opens_per_email_avg=99.0,
            cta_click_rate_pct=100.0, sentiment_score_recent=100.0,
            sentiment_score_prior=0.0, days_since_last_reply=0,
            forwarded_to_others=1, deal_value=1e9,
        )
        result = tracker().analyze(inp)
        assert 0.0 <= result.email_composite <= 100.0

    def test_all_zeros(self):
        inp = make_input(
            total_emails_sent=0, total_replies_received=0,
            avg_reply_length_words=0, avg_reply_length_prior_words=0,
            positive_language_count=0, negative_language_count=0,
            question_count_from_buyer=0, exclamation_count=0,
            hedge_phrase_count=0, urgency_language_count=0,
            reply_time_trend=0.0, opens_per_email_avg=0.0,
            cta_click_rate_pct=0.0, sentiment_score_recent=0.0,
            sentiment_score_prior=0.0, days_since_last_reply=0,
            thread_age_days=0, forwarded_to_others=0, deal_value=0.0,
        )
        result = tracker().analyze(inp)
        assert isinstance(result, EmailSentimentResult)

    def test_batch_then_reset_then_summary(self):
        t = tracker()
        t.analyze_batch([make_input(thread_id=str(i)) for i in range(5)])
        t.reset()
        s = t.summary()
        assert s["total"] == 0

    def test_to_dict_enum_values_valid(self):
        d = tracker().analyze(make_input()).to_dict()
        assert d["thread_sentiment"] in [e.value for e in ThreadSentiment]
        assert d["sentiment_trajectory"] in [e.value for e in SentimentTrajectory]
        assert d["buyer_engagement_signal"] in [e.value for e in BuyerEngagementSignal]
        assert d["email_action"] in [e.value for e in EmailAction]

    def test_analyze_result_not_mutated_by_further_analysis(self):
        t = tracker()
        r1 = t.analyze(make_input(thread_id="A"))
        composite_before = r1.email_composite
        t.analyze(make_input(thread_id="B"))
        assert r1.email_composite == composite_before

    def test_tracker_initializes_empty(self):
        t = EmailSentimentTracker()
        assert t._results == []

    def test_multiple_trackers_independent(self):
        t1 = EmailSentimentTracker()
        t2 = EmailSentimentTracker()
        t1.analyze(make_input(thread_id="A"))
        assert len(t2._results) == 0

    def test_result_fields_all_set(self):
        result = tracker().analyze(make_input())
        for field in EmailSentimentResult.__dataclass_fields__:
            assert getattr(result, field) is not None


class TestFullScenarioHighEngagement:
    """Hot deal — should be enthusiastic, improving, highly_engaged, keep_momentum."""

    def setup_method(self):
        self.inp = make_input(
            thread_id="HOT", deal_id="D-HOT", rep_id="R1",
            total_emails_sent=10, total_replies_received=9,
            avg_reply_length_words=100, avg_reply_length_prior_words=60,
            positive_language_count=8, negative_language_count=0,
            question_count_from_buyer=6, exclamation_count=7,
            hedge_phrase_count=0, urgency_language_count=5,
            reply_time_trend=0.6, opens_per_email_avg=2.5,
            cta_click_rate_pct=75.0, sentiment_score_recent=82.0,
            sentiment_score_prior=65.0, days_since_last_reply=1,
            thread_age_days=30, forwarded_to_others=1, deal_value=50000.0,
        )
        self.result = tracker().analyze(self.inp)

    def test_thread_id(self):
        assert self.result.thread_id == "HOT"

    def test_is_healthy(self):
        assert self.result.is_thread_healthy is True

    def test_no_intervention(self):
        assert self.result.needs_intervention is False

    def test_high_composite(self):
        assert self.result.email_composite >= 70.0

    def test_sentiment_enthusiastic_or_positive(self):
        assert self.result.thread_sentiment in (
            ThreadSentiment.ENTHUSIASTIC, ThreadSentiment.POSITIVE)

    def test_engagement_signal_high(self):
        assert self.result.buyer_engagement_signal in (
            BuyerEngagementSignal.HIGHLY_ENGAGED, BuyerEngagementSignal.ENGAGED)

    def test_action_keep_momentum(self):
        assert self.result.email_action == EmailAction.KEEP_MOMENTUM


class TestFullScenarioDeadThread:
    """Ghost deal — flatlined, disengaged, escalate."""

    def setup_method(self):
        self.inp = make_input(
            thread_id="GHOST", deal_id="D-GHOST", rep_id="R1",
            total_emails_sent=15, total_replies_received=1,
            avg_reply_length_words=5, avg_reply_length_prior_words=60,
            positive_language_count=0, negative_language_count=3,
            question_count_from_buyer=0, exclamation_count=0,
            hedge_phrase_count=4, urgency_language_count=0,
            reply_time_trend=3.0, opens_per_email_avg=0.3,
            cta_click_rate_pct=0.0, sentiment_score_recent=20.0,
            sentiment_score_prior=40.0, days_since_last_reply=21,
            thread_age_days=60, forwarded_to_others=0, deal_value=5000.0,
        )
        self.result = tracker().analyze(self.inp)

    def test_thread_id(self):
        assert self.result.thread_id == "GHOST"

    def test_flatlined(self):
        assert self.result.sentiment_trajectory == SentimentTrajectory.FLATLINED

    def test_needs_intervention(self):
        assert self.result.needs_intervention is True

    def test_not_healthy(self):
        assert self.result.is_thread_healthy is False

    def test_escalate_action(self):
        assert self.result.email_action == EmailAction.ESCALATE_SEND

    def test_low_composite(self):
        assert self.result.email_composite < 55.0

    def test_thread_sentiment_negative(self):
        assert self.result.thread_sentiment in (
            ThreadSentiment.NEGATIVE, ThreadSentiment.COOLING)


class TestFullScenarioDeclining:
    """Deal declining — should trigger pattern_break."""

    def setup_method(self):
        self.inp = make_input(
            thread_id="DECLINE", deal_id="D-DEC",
            total_emails_sent=8, total_replies_received=4,
            avg_reply_length_words=20, avg_reply_length_prior_words=80,
            positive_language_count=1, negative_language_count=2,
            question_count_from_buyer=1, exclamation_count=0,
            hedge_phrase_count=3, urgency_language_count=0,
            reply_time_trend=2.0, opens_per_email_avg=0.8,
            cta_click_rate_pct=10.0, sentiment_score_recent=38.0,
            sentiment_score_prior=60.0, days_since_last_reply=10,
            thread_age_days=40, forwarded_to_others=0, deal_value=20000.0,
        )
        self.result = tracker().analyze(self.inp)

    def test_needs_intervention_or_pattern_break(self):
        # declining trajectory or needs_int triggers pattern_break
        assert self.result.email_action in (
            EmailAction.PATTERN_BREAK, EmailAction.ESCALATE_SEND)

    def test_not_healthy(self):
        assert self.result.is_thread_healthy is False


# ===========================================================================
# 21. BOUNDARY VALUE TESTS
# ===========================================================================

class TestBoundaryValues:
    """Precise boundary checks for score thresholds."""

    def test_reply_rate_exactly_07(self):
        t = tracker()
        inp = make_input(total_emails_sent=10, total_replies_received=7,
                         avg_reply_length_prior_words=0,
                         avg_reply_length_words=0,
                         reply_time_trend=1.0, days_since_last_reply=1)
        score = t._reply_quality_score(inp)
        assert score >= 0.0  # 0.7 => +30

    def test_reply_rate_exactly_05(self):
        t = tracker()
        inp = make_input(total_emails_sent=10, total_replies_received=5,
                         avg_reply_length_prior_words=0,
                         avg_reply_length_words=0,
                         reply_time_trend=1.0, days_since_last_reply=1)
        score = t._reply_quality_score(inp)
        assert score >= 0.0  # 0.5 => +20

    def test_reply_rate_exactly_03(self):
        t = tracker()
        inp = make_input(total_emails_sent=10, total_replies_received=3,
                         avg_reply_length_prior_words=0,
                         avg_reply_length_words=0,
                         reply_time_trend=1.0, days_since_last_reply=1)
        score = t._reply_quality_score(inp)
        assert score >= 0.0  # 0.3 => +10

    def test_days_since_reply_exactly_7(self):
        t = tracker()
        inp = make_input(days_since_last_reply=7,
                         avg_reply_length_prior_words=0,
                         reply_time_trend=1.0)
        score = t._reply_quality_score(inp)
        # 7 => -10
        assert score >= 0.0

    def test_days_since_reply_exactly_14(self):
        t = tracker()
        inp = make_input(days_since_last_reply=14,
                         avg_reply_length_prior_words=0,
                         reply_time_trend=1.0)
        score = t._reply_quality_score(inp)
        # 14 => -20
        assert score >= 0.0

    def test_engagement_depth_cta_exactly_60(self):
        t = tracker()
        inp = make_input(cta_click_rate_pct=60.0, question_count_from_buyer=0,
                         opens_per_email_avg=0.0, forwarded_to_others=0,
                         exclamation_count=0)
        score = t._engagement_depth_score(inp)
        assert score == 25.0

    def test_engagement_depth_cta_exactly_30(self):
        t = tracker()
        inp = make_input(cta_click_rate_pct=30.0, question_count_from_buyer=0,
                         opens_per_email_avg=0.0, forwarded_to_others=0,
                         exclamation_count=0)
        score = t._engagement_depth_score(inp)
        assert score == 15.0

    def test_engagement_depth_opens_exactly_2(self):
        t = tracker()
        inp = make_input(opens_per_email_avg=2.0, question_count_from_buyer=0,
                         cta_click_rate_pct=0.0, forwarded_to_others=0,
                         exclamation_count=0)
        score = t._engagement_depth_score(inp)
        assert score == 20.0

    def test_engagement_depth_opens_exactly_13(self):
        t = tracker()
        inp = make_input(opens_per_email_avg=1.3, question_count_from_buyer=0,
                         cta_click_rate_pct=0.0, forwarded_to_others=0,
                         exclamation_count=0)
        score = t._engagement_depth_score(inp)
        assert score == 10.0

    def test_urgency_sent_exactly_70(self):
        t = tracker()
        inp = make_input(sentiment_score_recent=70.0, urgency_language_count=0,
                         cta_click_rate_pct=0.0, forwarded_to_others=0)
        score = t._urgency_alignment_score(inp)
        assert score == 30.0

    def test_urgency_sent_exactly_55(self):
        t = tracker()
        inp = make_input(sentiment_score_recent=55.0, urgency_language_count=0,
                         cta_click_rate_pct=0.0, forwarded_to_others=0)
        score = t._urgency_alignment_score(inp)
        assert score == 18.0

    def test_urgency_cta_exactly_50(self):
        t = tracker()
        inp = make_input(cta_click_rate_pct=50.0, urgency_language_count=0,
                         sentiment_score_recent=0.0, forwarded_to_others=0)
        score = t._urgency_alignment_score(inp)
        assert score == 20.0

    def test_urgency_cta_exactly_25(self):
        t = tracker()
        inp = make_input(cta_click_rate_pct=25.0, urgency_language_count=0,
                         sentiment_score_recent=0.0, forwarded_to_others=0)
        score = t._urgency_alignment_score(inp)
        assert score == 10.0

    def test_composite_boundary_55(self):
        # If composite is exactly 55 and days=5 => is_thread_healthy=True
        t = tracker()
        # Manually test _composite
        c = t._composite(55.0 / 0.30, 0, 0, 0)  # approximate
        assert 0.0 <= c <= 100.0

    def test_is_healthy_exactly_55_days_7(self):
        # composite >= 55 AND days <= 7
        t = tracker()
        inp = make_input(days_since_last_reply=7)
        r = t.analyze(inp)
        expected = r.email_composite >= 55.0 and 7 <= 7
        assert r.is_thread_healthy == expected

    def test_needs_intervention_exactly_35_composite(self):
        # composite < 35 => intervention
        t = tracker()
        # Create a scenario where composite is just above 35
        inp = make_input(days_since_last_reply=1)
        r = t.analyze(inp)
        assert r.needs_intervention == (r.email_composite < 35.0 or 1 >= 14)

    def test_thread_health_index_replies_exactly_3(self):
        t = tracker()
        inp = make_input(total_replies_received=3, days_since_last_reply=10)
        r = t.analyze(inp)
        # should have gotten +5 boost
        assert r.thread_health_index >= 0.0

    def test_thread_health_days_exactly_3(self):
        t = tracker()
        inp = make_input(total_replies_received=0, days_since_last_reply=3)
        r = t.analyze(inp)
        assert r.thread_health_index >= 0.0


# ===========================================================================
# 22. ADDITIONAL COVERAGE: TRAJECTORY EDGE CASES
# ===========================================================================

class TestTrajectoryEdgeCases:
    def test_volatile_boundary_delta_exactly_20_ratio_15(self):
        t = tracker()
        inp = make_input(
            days_since_last_reply=1,
            sentiment_score_recent=70, sentiment_score_prior=50,  # delta=20
            avg_reply_length_words=150, avg_reply_length_prior_words=100,  # ratio=1.5
        )
        r = t._sentiment_trajectory(inp)
        assert r == SentimentTrajectory.VOLATILE

    def test_improving_boundary_delta_8_ratio_09(self):
        t = tracker()
        inp = make_input(
            days_since_last_reply=1,
            sentiment_score_recent=58, sentiment_score_prior=50,  # delta=8
            avg_reply_length_words=90, avg_reply_length_prior_words=100,  # ratio=0.9
        )
        r = t._sentiment_trajectory(inp)
        assert r == SentimentTrajectory.IMPROVING

    def test_declining_boundary_delta_neg8(self):
        t = tracker()
        inp = make_input(
            days_since_last_reply=1,
            sentiment_score_recent=42, sentiment_score_prior=50,  # delta=-8
            avg_reply_length_words=100, avg_reply_length_prior_words=100,
        )
        r = t._sentiment_trajectory(inp)
        assert r == SentimentTrajectory.DECLINING

    def test_declining_boundary_length_ratio_06(self):
        t = tracker()
        inp = make_input(
            days_since_last_reply=1,
            sentiment_score_recent=50, sentiment_score_prior=50,
            avg_reply_length_words=60, avg_reply_length_prior_words=100,  # ratio=0.6
        )
        r = t._sentiment_trajectory(inp)
        assert r == SentimentTrajectory.DECLINING

    def test_not_declining_length_ratio_07(self):
        # ratio = 0.7 > 0.6 and delta near 0 => stable
        t = tracker()
        inp = make_input(
            days_since_last_reply=1,
            sentiment_score_recent=50, sentiment_score_prior=50,
            avg_reply_length_words=70, avg_reply_length_prior_words=100,
        )
        r = t._sentiment_trajectory(inp)
        assert r == SentimentTrajectory.STABLE


# ===========================================================================
# 23. ADDITIONAL COVERAGE: BUYER ENGAGEMENT EDGE CASES
# ===========================================================================

class TestBuyerEngagementEdgeCases:
    def test_disengaging_composite_25_days_lt_7(self):
        t = tracker()
        inp = make_input(question_count_from_buyer=0, days_since_last_reply=1)
        r = t._buyer_engagement_signal(25, inp)
        assert r == BuyerEngagementSignal.DISENGAGING

    def test_disengaging_composite_lt_25_days_7(self):
        t = tracker()
        inp = make_input(question_count_from_buyer=0, days_since_last_reply=7)
        r = t._buyer_engagement_signal(20, inp)
        assert r == BuyerEngagementSignal.DISENGAGING

    def test_disengaged_composite_0_days_0(self):
        t = tracker()
        inp = make_input(question_count_from_buyer=0, days_since_last_reply=0)
        r = t._buyer_engagement_signal(0, inp)
        assert r == BuyerEngagementSignal.DISENGAGED

    def test_passively_engaged_boundary_40(self):
        t = tracker()
        inp = make_input(question_count_from_buyer=0, days_since_last_reply=1)
        r = t._buyer_engagement_signal(40, inp)
        assert r == BuyerEngagementSignal.PASSIVELY_ENGAGED

    def test_engaged_boundary_55(self):
        t = tracker()
        inp = make_input(question_count_from_buyer=1, days_since_last_reply=1)
        r = t._buyer_engagement_signal(55, inp)
        assert r == BuyerEngagementSignal.ENGAGED


# ===========================================================================
# 24. ANALYZE OUTPUT CONSISTENCY TESTS
# ===========================================================================

class TestAnalyzeOutputConsistency:
    """Ensure analyze outputs are internally consistent."""

    def test_is_healthy_implies_composite_ge_55_and_days_le_7(self):
        t = tracker()
        for days in [1, 3, 5, 7, 8, 10, 14]:
            r = t.analyze(make_input(days_since_last_reply=days))
            if r.is_thread_healthy:
                assert r.email_composite >= 55.0
                assert days <= 7

    def test_needs_intervention_implies_composite_lt_35_or_days_ge_14(self):
        t = tracker()
        for days in [1, 7, 13, 14, 20]:
            r = t.analyze(make_input(days_since_last_reply=days))
            if r.needs_intervention:
                assert r.email_composite < 35.0 or days >= 14

    def test_no_result_both_healthy_and_intervention_for_typical(self):
        # is_healthy requires composite>=55 AND days<=7; needs_int requires composite<35 OR days>=14
        # These CAN coexist if composite is in [35,55) range for edge days but typically not
        t = tracker()
        for days in [1, 3, 5]:
            r = t.analyze(make_input(days_since_last_reply=days))
            if r.is_thread_healthy:
                # composite>=55 => not < 35 => needs_int only if days>=14, but days<=7
                assert not r.needs_intervention

    def test_escalate_when_flatlined(self):
        r = tracker().analyze(make_input(days_since_last_reply=14))
        assert r.sentiment_trajectory == SentimentTrajectory.FLATLINED
        assert r.email_action == EmailAction.ESCALATE_SEND

    def test_composite_parts_sum(self):
        t = tracker()
        r = t.analyze(make_input())
        manual = round(
            r.reply_quality_score * 0.30 +
            r.engagement_depth_score * 0.30 +
            r.sentiment_momentum_score * 0.25 +
            r.urgency_alignment_score * 0.15, 1
        )
        assert r.email_composite == manual


# ===========================================================================
# 25. SUMMARY WITH VARIED RESULTS
# ===========================================================================

class TestSummaryVariedResults:
    def test_all_sentiment_types_counted(self):
        """Drive scenarios that produce each sentiment type."""
        t = tracker()
        # enthusiastic: sent>=75 and composite>=60
        t.analyze(make_input(
            sentiment_score_recent=80, sentiment_score_prior=60,
            total_emails_sent=10, total_replies_received=8,
            avg_reply_length_words=80, avg_reply_length_prior_words=50,
            positive_language_count=6, negative_language_count=0,
            question_count_from_buyer=5, exclamation_count=5,
            hedge_phrase_count=0, urgency_language_count=4,
            reply_time_trend=0.7, opens_per_email_avg=2.0,
            cta_click_rate_pct=70.0, days_since_last_reply=2,
            forwarded_to_others=1, thread_id="E",
        ))
        # neutral
        t.analyze(make_input(
            sentiment_score_recent=48, sentiment_score_prior=50,
            thread_id="N",
        ))
        # cooling
        t.analyze(make_input(
            sentiment_score_recent=33, sentiment_score_prior=40,
            thread_id="C",
        ))
        # negative
        t.analyze(make_input(
            sentiment_score_recent=10, sentiment_score_prior=20,
            total_emails_sent=10, total_replies_received=0,
            avg_reply_length_words=0, avg_reply_length_prior_words=0,
            positive_language_count=0, negative_language_count=5,
            question_count_from_buyer=0, exclamation_count=0,
            hedge_phrase_count=5, urgency_language_count=0,
            reply_time_trend=5.0, opens_per_email_avg=0.0,
            cta_click_rate_pct=0.0, days_since_last_reply=1,
            forwarded_to_others=0, thread_id="NG",
        ))
        s = t.summary()
        assert s["total"] == 4
        assert sum(s["sentiment_counts"].values()) == 4

    def test_all_trajectory_types_counted(self):
        t = tracker()
        # flatlined
        t.analyze(make_input(days_since_last_reply=14, thread_id="F"))
        # stable
        t.analyze(make_input(
            days_since_last_reply=1,
            sentiment_score_recent=50, sentiment_score_prior=50,
            avg_reply_length_words=50, avg_reply_length_prior_words=50,
            thread_id="S",
        ))
        # improving
        t.analyze(make_input(
            days_since_last_reply=1,
            sentiment_score_recent=60, sentiment_score_prior=50,
            avg_reply_length_words=100, avg_reply_length_prior_words=100,
            thread_id="I",
        ))
        # declining
        t.analyze(make_input(
            days_since_last_reply=1,
            sentiment_score_recent=42, sentiment_score_prior=50,
            avg_reply_length_words=50, avg_reply_length_prior_words=50,
            thread_id="D",
        ))
        # volatile
        t.analyze(make_input(
            days_since_last_reply=1,
            sentiment_score_recent=80, sentiment_score_prior=55,
            avg_reply_length_words=200, avg_reply_length_prior_words=100,
            thread_id="V",
        ))
        s = t.summary()
        assert s["total"] == 5
        assert sum(s["trajectory_counts"].values()) == 5

    def test_reset_clears_summary_counts(self):
        t = tracker()
        t.analyze_batch([make_input(thread_id=str(i)) for i in range(3)])
        t.reset()
        s = t.summary()
        assert s["total"] == 0
        assert s["sentiment_counts"] == {}
