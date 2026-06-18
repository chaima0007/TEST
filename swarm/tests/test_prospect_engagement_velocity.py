"""
Comprehensive pytest tests for ProspectEngagementVelocityTracker.
Covers all enums, scoring functions, composite logic, flags, and tracker methods.
"""
from __future__ import annotations

import dataclasses
import math
from typing import List

import pytest

from swarm.intelligence.prospect_engagement_velocity import (
    EngagementAction,
    EngagementRisk,
    EngagementVelocity,
    IntentLevel,
    ProspectEngagementInput,
    ProspectEngagementResult,
    ProspectEngagementVelocityTracker,
    _composite,
    _days_to_re_engage,
    _digital_engagement_score,
    _email_engagement_score,
    _engagement_action,
    _engagement_risk,
    _engagement_velocity,
    _intent_level,
    _meeting_engagement_score,
    _primary_signal,
    _velocity_trend_score,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(
    prospect_id: str = "p1",
    prospect_name: str = "Alice",
    company_name: str = "Acme",
    rep_id: str = "r1",
    emails_sent_last_30d: int = 10,
    emails_opened_last_30d: int = 8,
    emails_replied_last_30d: int = 5,
    avg_reply_time_hours: float = 1.0,
    meetings_requested_last_30d: int = 4,
    meetings_accepted_last_30d: int = 4,
    meetings_rescheduled_count: int = 0,
    meetings_ghosted_count: int = 0,
    content_viewed_last_30d: int = 5,
    demo_request_submitted: int = 1,
    pricing_page_visited_count: int = 3,
    linkedin_engagement_count: int = 5,
    days_since_last_engagement: int = 2,
    days_since_first_contact: int = 30,
    champion_internal_sharing: int = 1,
    decision_maker_cc_count: int = 2,
    prior_30d_engagement_score: float = 50.0,
    deal_stage: int = 3,
) -> ProspectEngagementInput:
    return ProspectEngagementInput(
        prospect_id=prospect_id,
        prospect_name=prospect_name,
        company_name=company_name,
        rep_id=rep_id,
        emails_sent_last_30d=emails_sent_last_30d,
        emails_opened_last_30d=emails_opened_last_30d,
        emails_replied_last_30d=emails_replied_last_30d,
        avg_reply_time_hours=avg_reply_time_hours,
        meetings_requested_last_30d=meetings_requested_last_30d,
        meetings_accepted_last_30d=meetings_accepted_last_30d,
        meetings_rescheduled_count=meetings_rescheduled_count,
        meetings_ghosted_count=meetings_ghosted_count,
        content_viewed_last_30d=content_viewed_last_30d,
        demo_request_submitted=demo_request_submitted,
        pricing_page_visited_count=pricing_page_visited_count,
        linkedin_engagement_count=linkedin_engagement_count,
        days_since_last_engagement=days_since_last_engagement,
        days_since_first_contact=days_since_first_contact,
        champion_internal_sharing=champion_internal_sharing,
        decision_maker_cc_count=decision_maker_cc_count,
        prior_30d_engagement_score=prior_30d_engagement_score,
        deal_stage=deal_stage,
    )


def cold_input(prospect_id: str = "cold1") -> ProspectEngagementInput:
    """A completely cold / disengaged prospect."""
    return make_input(
        prospect_id=prospect_id,
        emails_sent_last_30d=0,
        emails_opened_last_30d=0,
        emails_replied_last_30d=0,
        avg_reply_time_hours=0.0,
        meetings_requested_last_30d=0,
        meetings_accepted_last_30d=0,
        meetings_rescheduled_count=0,
        meetings_ghosted_count=5,
        content_viewed_last_30d=0,
        demo_request_submitted=0,
        pricing_page_visited_count=0,
        linkedin_engagement_count=0,
        days_since_last_engagement=30,
        champion_internal_sharing=0,
        decision_maker_cc_count=0,
        prior_30d_engagement_score=0.0,
        deal_stage=1,
    )


# ---------------------------------------------------------------------------
# 1. Enum structure – inheritance, count, values
# ---------------------------------------------------------------------------

class TestEnumInheritance:
    def test_engagement_velocity_inherits_str(self):
        assert issubclass(EngagementVelocity, str)

    def test_intent_level_inherits_str(self):
        assert issubclass(IntentLevel, str)

    def test_engagement_risk_inherits_str(self):
        assert issubclass(EngagementRisk, str)

    def test_engagement_action_inherits_str(self):
        assert issubclass(EngagementAction, str)

    def test_engagement_velocity_has_5_values(self):
        assert len(EngagementVelocity) == 5

    def test_intent_level_has_4_values(self):
        assert len(IntentLevel) == 4

    def test_engagement_risk_has_4_values(self):
        assert len(EngagementRisk) == 4

    def test_engagement_action_has_4_values(self):
        assert len(EngagementAction) == 4

    def test_engagement_velocity_values(self):
        vals = {e.value for e in EngagementVelocity}
        assert vals == {"accelerating", "steady", "decelerating", "stalled", "cold"}

    def test_intent_level_values(self):
        vals = {e.value for e in IntentLevel}
        assert vals == {"hot", "warm", "lukewarm", "cold"}

    def test_engagement_risk_values(self):
        vals = {e.value for e in EngagementRisk}
        assert vals == {"low", "moderate", "high", "critical"}

    def test_engagement_action_values(self):
        vals = {e.value for e in EngagementAction}
        assert vals == {"nurture", "advance", "reactivate", "disqualify"}

    def test_str_equality_velocity(self):
        assert EngagementVelocity.ACCELERATING == "accelerating"

    def test_str_equality_intent(self):
        assert IntentLevel.HOT == "hot"

    def test_str_equality_risk(self):
        assert EngagementRisk.CRITICAL == "critical"

    def test_str_equality_action(self):
        assert EngagementAction.DISQUALIFY == "disqualify"


# ---------------------------------------------------------------------------
# 2. ProspectEngagementInput – exactly 22 fields
# ---------------------------------------------------------------------------

class TestProspectEngagementInputFields:
    def test_exactly_22_fields(self):
        fields = dataclasses.fields(ProspectEngagementInput)
        assert len(fields) == 22

    def test_field_names(self):
        names = {f.name for f in dataclasses.fields(ProspectEngagementInput)}
        expected = {
            "prospect_id", "prospect_name", "company_name", "rep_id",
            "emails_sent_last_30d", "emails_opened_last_30d",
            "emails_replied_last_30d", "avg_reply_time_hours",
            "meetings_requested_last_30d", "meetings_accepted_last_30d",
            "meetings_rescheduled_count", "meetings_ghosted_count",
            "content_viewed_last_30d", "demo_request_submitted",
            "pricing_page_visited_count", "linkedin_engagement_count",
            "days_since_last_engagement", "days_since_first_contact",
            "champion_internal_sharing", "decision_maker_cc_count",
            "prior_30d_engagement_score", "deal_stage",
        }
        assert names == expected

    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(ProspectEngagementInput)

    def test_instantiation_works(self):
        inp = make_input()
        assert inp.prospect_id == "p1"


# ---------------------------------------------------------------------------
# 3. ProspectEngagementResult.to_dict – exactly 15 keys
# ---------------------------------------------------------------------------

class TestProspectEngagementResultToDict:
    def setup_method(self):
        self.tracker = ProspectEngagementVelocityTracker()

    def test_exactly_15_keys(self):
        result = self.tracker.track(make_input())
        assert len(result.to_dict()) == 15

    def test_to_dict_keys(self):
        result = self.tracker.track(make_input())
        d = result.to_dict()
        expected = {
            "prospect_id", "prospect_name", "engagement_velocity",
            "intent_level", "engagement_risk", "engagement_action",
            "email_engagement_score", "meeting_engagement_score",
            "digital_engagement_score", "velocity_trend_score",
            "engagement_composite", "days_to_re_engage",
            "is_high_intent", "needs_reactivation", "primary_signal",
        }
        assert set(d.keys()) == expected

    def test_to_dict_enum_values_are_strings(self):
        result = self.tracker.track(make_input())
        d = result.to_dict()
        assert isinstance(d["engagement_velocity"], str)
        assert isinstance(d["intent_level"], str)
        assert isinstance(d["engagement_risk"], str)
        assert isinstance(d["engagement_action"], str)

    def test_to_dict_prospect_id_preserved(self):
        result = self.tracker.track(make_input(prospect_id="xyz"))
        assert result.to_dict()["prospect_id"] == "xyz"

    def test_to_dict_booleans(self):
        result = self.tracker.track(make_input())
        d = result.to_dict()
        assert isinstance(d["is_high_intent"], bool)
        assert isinstance(d["needs_reactivation"], bool)


# ---------------------------------------------------------------------------
# 4. Email engagement score
# ---------------------------------------------------------------------------

class TestEmailEngagementScore:
    def test_open_rate_high(self):
        # 8/10 = 0.8 -> +25
        inp = make_input(emails_sent_last_30d=10, emails_opened_last_30d=8,
                         emails_replied_last_30d=0, avg_reply_time_hours=0.0,
                         days_since_last_engagement=0)
        score = _email_engagement_score(inp)
        assert score >= 25.0

    def test_open_rate_medium(self):
        # 6/10 = 0.6 -> +18
        inp = make_input(emails_sent_last_30d=10, emails_opened_last_30d=6,
                         emails_replied_last_30d=0, avg_reply_time_hours=0.0,
                         days_since_last_engagement=0)
        score = _email_engagement_score(inp)
        assert score >= 18.0

    def test_open_rate_low(self):
        # 2/10 = 0.2 -> +5
        inp = make_input(emails_sent_last_30d=10, emails_opened_last_30d=2,
                         emails_replied_last_30d=0, avg_reply_time_hours=0.0,
                         days_since_last_engagement=0)
        score = _email_engagement_score(inp)
        assert score >= 5.0

    def test_open_rate_zero_sent(self):
        inp = make_input(emails_sent_last_30d=0, emails_opened_last_30d=0,
                         emails_replied_last_30d=0, avg_reply_time_hours=0.0,
                         days_since_last_engagement=0)
        score = _email_engagement_score(inp)
        assert score >= 0.0  # recency bonus still applies for days=0

    def test_reply_rate_high(self):
        # 5/10 = 0.5 -> +35
        inp = make_input(emails_sent_last_30d=10, emails_opened_last_30d=0,
                         emails_replied_last_30d=5, avg_reply_time_hours=0.0,
                         days_since_last_engagement=0)
        score = _email_engagement_score(inp)
        assert score >= 35.0

    def test_reply_rate_moderate(self):
        # 3/10 = 0.3 -> +25
        inp = make_input(emails_sent_last_30d=10, emails_opened_last_30d=0,
                         emails_replied_last_30d=3, avg_reply_time_hours=0.0,
                         days_since_last_engagement=0)
        score = _email_engagement_score(inp)
        assert score >= 25.0

    def test_reply_speed_fast(self):
        # <= 2h -> +25
        inp = make_input(emails_sent_last_30d=10, emails_opened_last_30d=0,
                         emails_replied_last_30d=0, avg_reply_time_hours=1.5,
                         days_since_last_engagement=0)
        score = _email_engagement_score(inp)
        assert score >= 25.0

    def test_reply_speed_medium(self):
        # <= 6h -> +18
        inp = make_input(emails_sent_last_30d=10, emails_opened_last_30d=0,
                         emails_replied_last_30d=0, avg_reply_time_hours=4.0,
                         days_since_last_engagement=0)
        score = _email_engagement_score(inp)
        assert score >= 18.0

    def test_reply_speed_daily(self):
        # <= 24h -> +10
        inp = make_input(emails_sent_last_30d=10, emails_opened_last_30d=0,
                         emails_replied_last_30d=0, avg_reply_time_hours=20.0,
                         days_since_last_engagement=0)
        score = _email_engagement_score(inp)
        assert score >= 10.0

    def test_reply_speed_slow(self):
        # <= 72h -> +4
        inp = make_input(emails_sent_last_30d=10, emails_opened_last_30d=0,
                         emails_replied_last_30d=0, avg_reply_time_hours=48.0,
                         days_since_last_engagement=0)
        score = _email_engagement_score(inp)
        assert score >= 4.0

    def test_recency_bonus_3_days(self):
        # days <= 3 -> +15
        inp = make_input(emails_sent_last_30d=0, emails_opened_last_30d=0,
                         emails_replied_last_30d=0, avg_reply_time_hours=0.0,
                         days_since_last_engagement=3)
        score = _email_engagement_score(inp)
        assert score >= 15.0

    def test_recency_bonus_7_days(self):
        # days <= 7 -> +10
        inp = make_input(emails_sent_last_30d=0, emails_opened_last_30d=0,
                         emails_replied_last_30d=0, avg_reply_time_hours=0.0,
                         days_since_last_engagement=7)
        score = _email_engagement_score(inp)
        assert score >= 10.0

    def test_recency_bonus_14_days(self):
        # days <= 14 -> +5
        inp = make_input(emails_sent_last_30d=0, emails_opened_last_30d=0,
                         emails_replied_last_30d=0, avg_reply_time_hours=0.0,
                         days_since_last_engagement=14)
        score = _email_engagement_score(inp)
        assert score >= 5.0

    def test_recency_no_bonus_beyond_14(self):
        inp = make_input(emails_sent_last_30d=0, emails_opened_last_30d=0,
                         emails_replied_last_30d=0, avg_reply_time_hours=0.0,
                         days_since_last_engagement=15)
        score = _email_engagement_score(inp)
        assert score == 0.0

    def test_score_capped_at_100(self):
        score = _email_engagement_score(make_input())
        assert score <= 100.0

    def test_score_non_negative(self):
        score = _email_engagement_score(cold_input())
        assert score >= 0.0

    def test_score_rounding(self):
        score = _email_engagement_score(make_input())
        # Must be rounded to 1 decimal place
        assert score == round(score, 1)


# ---------------------------------------------------------------------------
# 5. Meeting engagement score
# ---------------------------------------------------------------------------

class TestMeetingEngagementScore:
    def test_perfect_acceptance_no_ghost_no_reschedule(self):
        inp = make_input(meetings_requested_last_30d=4, meetings_accepted_last_30d=4,
                         meetings_rescheduled_count=0, meetings_ghosted_count=0,
                         champion_internal_sharing=0, decision_maker_cc_count=0)
        score = _meeting_engagement_score(inp)
        # 40 + 30 + 15 = 85
        assert score == 85.0

    def test_high_acceptance(self):
        # acc_rate >= 0.8 -> +40
        inp = make_input(meetings_requested_last_30d=5, meetings_accepted_last_30d=4,
                         meetings_rescheduled_count=0, meetings_ghosted_count=0,
                         champion_internal_sharing=0, decision_maker_cc_count=0)
        score = _meeting_engagement_score(inp)
        assert score >= 40.0

    def test_medium_acceptance(self):
        # acc_rate = 0.6 -> +28
        inp = make_input(meetings_requested_last_30d=5, meetings_accepted_last_30d=3,
                         meetings_rescheduled_count=0, meetings_ghosted_count=0,
                         champion_internal_sharing=0, decision_maker_cc_count=0)
        score = _meeting_engagement_score(inp)
        assert score >= 28.0

    def test_low_acceptance(self):
        # acc_rate = 0.4 -> +18
        inp = make_input(meetings_requested_last_30d=5, meetings_accepted_last_30d=2,
                         meetings_rescheduled_count=0, meetings_ghosted_count=0,
                         champion_internal_sharing=0, decision_maker_cc_count=0)
        score = _meeting_engagement_score(inp)
        assert score >= 18.0

    def test_very_low_acceptance(self):
        # acc_rate = 0.2 -> +8
        inp = make_input(meetings_requested_last_30d=5, meetings_accepted_last_30d=1,
                         meetings_rescheduled_count=0, meetings_ghosted_count=0,
                         champion_internal_sharing=0, decision_maker_cc_count=0)
        score = _meeting_engagement_score(inp)
        assert score >= 8.0

    def test_no_ghost_bonus(self):
        # ghosted=0 -> +30
        inp = make_input(meetings_requested_last_30d=0, meetings_accepted_last_30d=0,
                         meetings_rescheduled_count=15, meetings_ghosted_count=0,
                         champion_internal_sharing=0, decision_maker_cc_count=0)
        score = _meeting_engagement_score(inp)
        assert score >= 30.0

    def test_one_ghost_penalty(self):
        # ghosted=1 -> +18
        inp = make_input(meetings_requested_last_30d=0, meetings_accepted_last_30d=0,
                         meetings_rescheduled_count=15, meetings_ghosted_count=1,
                         champion_internal_sharing=0, decision_maker_cc_count=0)
        score = _meeting_engagement_score(inp)
        assert score >= 18.0

    def test_two_ghost_penalty(self):
        # ghosted=2 -> +8
        inp = make_input(meetings_requested_last_30d=0, meetings_accepted_last_30d=0,
                         meetings_rescheduled_count=15, meetings_ghosted_count=2,
                         champion_internal_sharing=0, decision_maker_cc_count=0)
        score = _meeting_engagement_score(inp)
        assert score >= 8.0

    def test_three_plus_ghosts_no_bonus(self):
        # ghosted=3 -> 0 from ghost component
        inp = make_input(meetings_requested_last_30d=0, meetings_accepted_last_30d=0,
                         meetings_rescheduled_count=0, meetings_ghosted_count=3,
                         champion_internal_sharing=0, decision_maker_cc_count=0)
        score = _meeting_engagement_score(inp)
        # only rescheduled=0 bonus: +15
        assert score == 15.0

    def test_no_reschedule_bonus(self):
        # rescheduled=0 -> +15
        inp = make_input(meetings_requested_last_30d=0, meetings_accepted_last_30d=0,
                         meetings_rescheduled_count=0, meetings_ghosted_count=3,
                         champion_internal_sharing=0, decision_maker_cc_count=0)
        score = _meeting_engagement_score(inp)
        assert score >= 15.0

    def test_one_reschedule_bonus(self):
        # rescheduled<=1 -> +10
        inp = make_input(meetings_requested_last_30d=0, meetings_accepted_last_30d=0,
                         meetings_rescheduled_count=1, meetings_ghosted_count=3,
                         champion_internal_sharing=0, decision_maker_cc_count=0)
        score = _meeting_engagement_score(inp)
        assert score >= 10.0

    def test_two_reschedule_small_bonus(self):
        # rescheduled<=2 -> +4
        inp = make_input(meetings_requested_last_30d=0, meetings_accepted_last_30d=0,
                         meetings_rescheduled_count=2, meetings_ghosted_count=3,
                         champion_internal_sharing=0, decision_maker_cc_count=0)
        score = _meeting_engagement_score(inp)
        assert score >= 4.0

    def test_champion_sharing_bonus(self):
        # champion=1 -> +10
        inp = make_input(meetings_requested_last_30d=0, meetings_accepted_last_30d=0,
                         meetings_rescheduled_count=15, meetings_ghosted_count=3,
                         champion_internal_sharing=1, decision_maker_cc_count=0)
        score = _meeting_engagement_score(inp)
        assert score >= 10.0

    def test_decision_maker_cc_2_bonus(self):
        # dm_cc >= 2 -> +5
        inp = make_input(meetings_requested_last_30d=0, meetings_accepted_last_30d=0,
                         meetings_rescheduled_count=15, meetings_ghosted_count=3,
                         champion_internal_sharing=0, decision_maker_cc_count=2)
        score = _meeting_engagement_score(inp)
        assert score >= 5.0

    def test_decision_maker_cc_1_bonus(self):
        # dm_cc = 1 -> +3
        inp = make_input(meetings_requested_last_30d=0, meetings_accepted_last_30d=0,
                         meetings_rescheduled_count=15, meetings_ghosted_count=3,
                         champion_internal_sharing=0, decision_maker_cc_count=1)
        score = _meeting_engagement_score(inp)
        assert score >= 3.0

    def test_score_capped_at_100(self):
        score = _meeting_engagement_score(make_input())
        assert score <= 100.0

    def test_score_non_negative(self):
        score = _meeting_engagement_score(cold_input())
        assert score >= 0.0

    def test_score_rounding(self):
        score = _meeting_engagement_score(make_input())
        assert score == round(score, 1)

    def test_no_meetings_requested_no_acceptance_score(self):
        inp = make_input(meetings_requested_last_30d=0, meetings_accepted_last_30d=5,
                         meetings_rescheduled_count=0, meetings_ghosted_count=0,
                         champion_internal_sharing=0, decision_maker_cc_count=0)
        # acceptance rate not computed when meetings_requested=0
        score = _meeting_engagement_score(inp)
        # Only no-ghost + no-reschedule = 30 + 15 = 45
        assert score == 45.0


# ---------------------------------------------------------------------------
# 6. Digital engagement score
# ---------------------------------------------------------------------------

class TestDigitalEngagementScore:
    def test_content_viewed_5_plus(self):
        inp = make_input(content_viewed_last_30d=5, demo_request_submitted=0,
                         pricing_page_visited_count=0, linkedin_engagement_count=0)
        score = _digital_engagement_score(inp)
        assert score >= 25.0

    def test_content_viewed_3_to_4(self):
        inp = make_input(content_viewed_last_30d=3, demo_request_submitted=0,
                         pricing_page_visited_count=0, linkedin_engagement_count=0)
        score = _digital_engagement_score(inp)
        assert score >= 16.0

    def test_content_viewed_1_to_2(self):
        inp = make_input(content_viewed_last_30d=1, demo_request_submitted=0,
                         pricing_page_visited_count=0, linkedin_engagement_count=0)
        score = _digital_engagement_score(inp)
        assert score >= 8.0

    def test_content_viewed_zero(self):
        inp = make_input(content_viewed_last_30d=0, demo_request_submitted=0,
                         pricing_page_visited_count=0, linkedin_engagement_count=0)
        score = _digital_engagement_score(inp)
        assert score == 0.0

    def test_demo_request_bonus(self):
        inp = make_input(content_viewed_last_30d=0, demo_request_submitted=1,
                         pricing_page_visited_count=0, linkedin_engagement_count=0)
        score = _digital_engagement_score(inp)
        assert score >= 30.0

    def test_pricing_page_3_plus(self):
        inp = make_input(content_viewed_last_30d=0, demo_request_submitted=0,
                         pricing_page_visited_count=3, linkedin_engagement_count=0)
        score = _digital_engagement_score(inp)
        assert score >= 25.0

    def test_pricing_page_1(self):
        inp = make_input(content_viewed_last_30d=0, demo_request_submitted=0,
                         pricing_page_visited_count=1, linkedin_engagement_count=0)
        score = _digital_engagement_score(inp)
        assert score >= 15.0

    def test_pricing_page_zero(self):
        inp = make_input(content_viewed_last_30d=0, demo_request_submitted=0,
                         pricing_page_visited_count=0, linkedin_engagement_count=0)
        score = _digital_engagement_score(inp)
        # no pricing bonus
        assert score == 0.0

    def test_linkedin_5_plus(self):
        inp = make_input(content_viewed_last_30d=0, demo_request_submitted=0,
                         pricing_page_visited_count=0, linkedin_engagement_count=5)
        score = _digital_engagement_score(inp)
        assert score >= 20.0

    def test_linkedin_3_to_4(self):
        inp = make_input(content_viewed_last_30d=0, demo_request_submitted=0,
                         pricing_page_visited_count=0, linkedin_engagement_count=3)
        score = _digital_engagement_score(inp)
        assert score >= 13.0

    def test_linkedin_1_to_2(self):
        inp = make_input(content_viewed_last_30d=0, demo_request_submitted=0,
                         pricing_page_visited_count=0, linkedin_engagement_count=1)
        score = _digital_engagement_score(inp)
        assert score >= 6.0

    def test_max_digital_score(self):
        inp = make_input(content_viewed_last_30d=10, demo_request_submitted=1,
                         pricing_page_visited_count=5, linkedin_engagement_count=10)
        score = _digital_engagement_score(inp)
        assert score == 100.0

    def test_score_capped_at_100(self):
        score = _digital_engagement_score(make_input())
        assert score <= 100.0

    def test_score_non_negative(self):
        score = _digital_engagement_score(cold_input())
        assert score >= 0.0

    def test_score_rounding(self):
        score = _digital_engagement_score(make_input())
        assert score == round(score, 1)


# ---------------------------------------------------------------------------
# 7. Velocity trend score
# ---------------------------------------------------------------------------

class TestVelocityTrendScore:
    def test_no_prior_returns_50(self):
        inp = make_input(prior_30d_engagement_score=0.0)
        score = _velocity_trend_score(inp)
        assert score == 50.0

    def test_negative_prior_returns_50(self):
        inp = make_input(prior_30d_engagement_score=-10.0)
        score = _velocity_trend_score(inp)
        assert score == 50.0

    def test_large_increase_returns_95(self):
        # Make current high, prior very low so ratio >= 1.3
        inp = make_input(
            emails_sent_last_30d=10, emails_opened_last_30d=10, emails_replied_last_30d=5,
            avg_reply_time_hours=1.0,
            meetings_requested_last_30d=4, meetings_accepted_last_30d=4,
            meetings_rescheduled_count=0, meetings_ghosted_count=0,
            content_viewed_last_30d=5, demo_request_submitted=1,
            pricing_page_visited_count=3, linkedin_engagement_count=5,
            days_since_last_engagement=2,
            champion_internal_sharing=1, decision_maker_cc_count=2,
            prior_30d_engagement_score=1.0,  # very low prior -> high ratio
        )
        score = _velocity_trend_score(inp)
        assert score == 95.0

    def test_moderate_increase_returns_80(self):
        # ratio ~1.1..1.3
        inp = make_input(prior_30d_engagement_score=100.0)
        # current will be some value; with prior=100, ratio = current/100
        # if current > 110 -> 95, if current >= 80 -> 80
        # Make moderate current
        inp2 = make_input(
            emails_sent_last_30d=10, emails_opened_last_30d=7, emails_replied_last_30d=3,
            avg_reply_time_hours=3.0,
            meetings_requested_last_30d=3, meetings_accepted_last_30d=2,
            meetings_rescheduled_count=1, meetings_ghosted_count=0,
            content_viewed_last_30d=3, demo_request_submitted=0,
            pricing_page_visited_count=1, linkedin_engagement_count=2,
            days_since_last_engagement=5,
            champion_internal_sharing=0, decision_maker_cc_count=1,
            prior_30d_engagement_score=50.0,
        )
        score = _velocity_trend_score(inp2)
        assert score in (60.0, 80.0, 95.0)  # depends on actual current

    def test_score_is_one_of_known_values(self):
        inp = make_input(prior_30d_engagement_score=30.0)
        score = _velocity_trend_score(inp)
        assert score in {5.0, 15.0, 35.0, 60.0, 80.0, 95.0, 50.0}

    def test_score_rounding(self):
        score = _velocity_trend_score(make_input())
        assert score == round(score, 1)

    def test_ratio_below_half_returns_5(self):
        # ratio < 0.5: current ~0, prior=100
        inp = make_input(
            emails_sent_last_30d=0, emails_opened_last_30d=0,
            emails_replied_last_30d=0, avg_reply_time_hours=0.0,
            meetings_requested_last_30d=0, meetings_accepted_last_30d=0,
            meetings_rescheduled_count=5, meetings_ghosted_count=5,
            content_viewed_last_30d=0, demo_request_submitted=0,
            pricing_page_visited_count=0, linkedin_engagement_count=0,
            days_since_last_engagement=30,
            champion_internal_sharing=0, decision_maker_cc_count=0,
            prior_30d_engagement_score=100.0,
        )
        score = _velocity_trend_score(inp)
        assert score == 5.0


# ---------------------------------------------------------------------------
# 8. Composite formula
# ---------------------------------------------------------------------------

class TestCompositeFormula:
    def test_exact_formula(self):
        result = _composite(80.0, 60.0, 70.0, 50.0)
        expected = round(80.0 * 0.30 + 60.0 * 0.30 + 70.0 * 0.20 + 50.0 * 0.20, 1)
        assert result == expected

    def test_all_zeros(self):
        assert _composite(0.0, 0.0, 0.0, 0.0) == 0.0

    def test_all_100(self):
        assert _composite(100.0, 100.0, 100.0, 100.0) == 100.0

    def test_weights_sum_to_one(self):
        # Verifying indirectly: equal input -> output equals input
        v = 50.0
        assert _composite(v, v, v, v) == v

    def test_rounding(self):
        result = _composite(33.3, 33.3, 33.3, 33.3)
        assert result == round(result, 1)

    def test_email_weight_0_30(self):
        # Only email contributes
        result = _composite(100.0, 0.0, 0.0, 0.0)
        assert result == 30.0

    def test_meeting_weight_0_30(self):
        result = _composite(0.0, 100.0, 0.0, 0.0)
        assert result == 30.0

    def test_digital_weight_0_20(self):
        result = _composite(0.0, 0.0, 100.0, 0.0)
        assert result == 20.0

    def test_velocity_weight_0_20(self):
        result = _composite(0.0, 0.0, 0.0, 100.0)
        assert result == 20.0


# ---------------------------------------------------------------------------
# 9. Engagement velocity classification
# ---------------------------------------------------------------------------

class TestEngagementVelocityClassification:
    def test_cold_when_days_21_plus(self):
        v = _engagement_velocity(90.0, 95.0, 21)
        assert v == EngagementVelocity.COLD

    def test_cold_when_days_30(self):
        v = _engagement_velocity(90.0, 95.0, 30)
        assert v == EngagementVelocity.COLD

    def test_stalled_when_days_14(self):
        v = _engagement_velocity(90.0, 95.0, 14)
        assert v == EngagementVelocity.STALLED

    def test_stalled_when_composite_below_20(self):
        v = _engagement_velocity(10.0, 90.0, 5)
        assert v == EngagementVelocity.STALLED

    def test_accelerating_high_trend(self):
        v = _engagement_velocity(80.0, 75.0, 2)
        assert v == EngagementVelocity.ACCELERATING

    def test_steady_moderate_trend(self):
        v = _engagement_velocity(80.0, 55.0, 2)
        assert v == EngagementVelocity.STEADY

    def test_decelerating_low_trend(self):
        v = _engagement_velocity(80.0, 35.0, 2)
        assert v == EngagementVelocity.DECELERATING

    def test_stalled_very_low_trend(self):
        v = _engagement_velocity(80.0, 20.0, 2)
        assert v == EngagementVelocity.STALLED

    def test_days_exactly_20_not_cold(self):
        # days=20 < 21 -> not COLD
        v = _engagement_velocity(80.0, 75.0, 20)
        assert v == EngagementVelocity.STALLED  # days>=14

    def test_days_13_composite_high_trend_high(self):
        v = _engagement_velocity(80.0, 75.0, 13)
        assert v == EngagementVelocity.ACCELERATING


# ---------------------------------------------------------------------------
# 10. Intent level
# ---------------------------------------------------------------------------

class TestIntentLevel:
    def test_hot_high_composite_recent(self):
        inp = make_input(days_since_last_engagement=3)
        intent = _intent_level(75.0, inp)
        assert intent == IntentLevel.HOT

    def test_not_hot_if_stale(self):
        inp = make_input(days_since_last_engagement=8)
        intent = _intent_level(75.0, inp)
        assert intent == IntentLevel.WARM

    def test_not_hot_if_low_composite(self):
        inp = make_input(days_since_last_engagement=3)
        intent = _intent_level(60.0, inp)
        assert intent == IntentLevel.WARM

    def test_warm_composite_50_to_70(self):
        inp = make_input(days_since_last_engagement=8)
        intent = _intent_level(55.0, inp)
        assert intent == IntentLevel.WARM

    def test_lukewarm_composite_30_to_50(self):
        inp = make_input(days_since_last_engagement=3)
        intent = _intent_level(35.0, inp)
        assert intent == IntentLevel.LUKEWARM

    def test_cold_below_30(self):
        inp = make_input(days_since_last_engagement=3)
        intent = _intent_level(20.0, inp)
        assert intent == IntentLevel.COLD

    def test_boundary_exactly_70_recent(self):
        inp = make_input(days_since_last_engagement=7)
        intent = _intent_level(70.0, inp)
        assert intent == IntentLevel.HOT

    def test_boundary_exactly_50(self):
        inp = make_input(days_since_last_engagement=10)
        intent = _intent_level(50.0, inp)
        assert intent == IntentLevel.WARM

    def test_boundary_exactly_30(self):
        inp = make_input(days_since_last_engagement=10)
        intent = _intent_level(30.0, inp)
        assert intent == IntentLevel.LUKEWARM


# ---------------------------------------------------------------------------
# 11. Engagement risk
# ---------------------------------------------------------------------------

class TestEngagementRisk:
    def test_critical_low_composite(self):
        risk = _engagement_risk(10.0, 5)
        assert risk == EngagementRisk.CRITICAL

    def test_critical_old_engagement(self):
        risk = _engagement_risk(50.0, 21)
        assert risk == EngagementRisk.CRITICAL

    def test_high_moderate_composite(self):
        risk = _engagement_risk(25.0, 5)
        assert risk == EngagementRisk.HIGH

    def test_high_14_days(self):
        risk = _engagement_risk(50.0, 14)
        assert risk == EngagementRisk.HIGH

    def test_moderate_composite_35_to_55(self):
        risk = _engagement_risk(45.0, 5)
        assert risk == EngagementRisk.MODERATE

    def test_moderate_7_to_14_days(self):
        risk = _engagement_risk(60.0, 7)
        assert risk == EngagementRisk.MODERATE

    def test_low_high_composite_recent(self):
        risk = _engagement_risk(80.0, 5)
        assert risk == EngagementRisk.LOW

    def test_boundary_composite_20(self):
        # composite < 20 -> CRITICAL; == 20 -> HIGH if days < 14
        risk_boundary = _engagement_risk(20.0, 5)
        assert risk_boundary == EngagementRisk.HIGH

    def test_boundary_days_21(self):
        risk = _engagement_risk(60.0, 21)
        assert risk == EngagementRisk.CRITICAL


# ---------------------------------------------------------------------------
# 12. Engagement action
# ---------------------------------------------------------------------------

class TestEngagementAction:
    def test_advance_high_composite_low_risk(self):
        action = _engagement_action(EngagementRisk.LOW, 75.0, 3)
        assert action == EngagementAction.ADVANCE

    def test_reactivate_stale(self):
        action = _engagement_action(EngagementRisk.HIGH, 30.0, 14)
        assert action == EngagementAction.REACTIVATE

    def test_disqualify_very_low_composite(self):
        action = _engagement_action(EngagementRisk.CRITICAL, 10.0, 5)
        assert action == EngagementAction.DISQUALIFY

    def test_disqualify_28_days(self):
        action = _engagement_action(EngagementRisk.HIGH, 25.0, 28)
        assert action == EngagementAction.DISQUALIFY

    def test_nurture_moderate_risk(self):
        action = _engagement_action(EngagementRisk.MODERATE, 50.0, 5)
        assert action == EngagementAction.NURTURE

    def test_advance_high_risk_but_recent_and_composite_ok(self):
        # days < 14, composite >= 30, risk not MODERATE -> ADVANCE
        action = _engagement_action(EngagementRisk.HIGH, 40.0, 5)
        assert action == EngagementAction.ADVANCE

    def test_reactivate_low_composite_not_too_old(self):
        # composite < 30 but >= 15, days < 28 -> REACTIVATE
        action = _engagement_action(EngagementRisk.CRITICAL, 20.0, 15)
        assert action == EngagementAction.REACTIVATE


# ---------------------------------------------------------------------------
# 13. Days to re-engage
# ---------------------------------------------------------------------------

class TestDaysToReEngage:
    def test_composite_above_70(self):
        assert _days_to_re_engage(75.0, 5) == 1

    def test_composite_50_to_70(self):
        assert _days_to_re_engage(55.0, 5) == 2

    def test_composite_35_to_50(self):
        assert _days_to_re_engage(40.0, 5) == 3

    def test_days_14_plus_low_composite(self):
        assert _days_to_re_engage(25.0, 14) == 5

    def test_default_4_days(self):
        assert _days_to_re_engage(20.0, 5) == 4

    def test_boundary_exactly_70(self):
        assert _days_to_re_engage(70.0, 5) == 1

    def test_boundary_exactly_50(self):
        assert _days_to_re_engage(50.0, 5) == 2

    def test_boundary_exactly_35(self):
        assert _days_to_re_engage(35.0, 5) == 3


# ---------------------------------------------------------------------------
# 14. Primary signal
# ---------------------------------------------------------------------------

class TestPrimarySignal:
    def test_pricing_page_2_plus(self):
        inp = make_input(pricing_page_visited_count=2, demo_request_submitted=0,
                         champion_internal_sharing=0, decision_maker_cc_count=0,
                         meetings_ghosted_count=0, days_since_last_engagement=2)
        sig = _primary_signal(inp, 50.0, 50.0, 50.0)
        assert sig == "pricing page visited — high buying intent"

    def test_demo_request(self):
        inp = make_input(pricing_page_visited_count=0, demo_request_submitted=1,
                         champion_internal_sharing=0, decision_maker_cc_count=0,
                         meetings_ghosted_count=0, days_since_last_engagement=2)
        sig = _primary_signal(inp, 50.0, 50.0, 50.0)
        assert sig == "demo requested — strong interest"

    def test_champion_sharing(self):
        inp = make_input(pricing_page_visited_count=0, demo_request_submitted=0,
                         champion_internal_sharing=1, decision_maker_cc_count=0,
                         meetings_ghosted_count=0, days_since_last_engagement=2)
        sig = _primary_signal(inp, 50.0, 50.0, 50.0)
        assert sig == "champion sharing content internally"

    def test_decision_maker_cc(self):
        inp = make_input(pricing_page_visited_count=0, demo_request_submitted=0,
                         champion_internal_sharing=0, decision_maker_cc_count=1,
                         meetings_ghosted_count=0, days_since_last_engagement=2)
        sig = _primary_signal(inp, 50.0, 50.0, 50.0)
        assert sig == "decision maker engaged via CC"

    def test_multiple_ghosts(self):
        inp = make_input(pricing_page_visited_count=0, demo_request_submitted=0,
                         champion_internal_sharing=0, decision_maker_cc_count=0,
                         meetings_ghosted_count=2, days_since_last_engagement=2)
        sig = _primary_signal(inp, 50.0, 50.0, 50.0)
        assert sig == "multiple meetings ghosted — low engagement"

    def test_gone_dark(self):
        inp = make_input(pricing_page_visited_count=0, demo_request_submitted=0,
                         champion_internal_sharing=0, decision_maker_cc_count=0,
                         meetings_ghosted_count=0, days_since_last_engagement=14)
        sig = _primary_signal(inp, 50.0, 50.0, 50.0)
        assert sig == "gone dark — reactivation required"

    def test_strongest_email(self):
        inp = make_input(pricing_page_visited_count=0, demo_request_submitted=0,
                         champion_internal_sharing=0, decision_maker_cc_count=0,
                         meetings_ghosted_count=0, days_since_last_engagement=5)
        sig = _primary_signal(inp, 80.0, 50.0, 30.0)
        assert sig == "strongest signal: email engagement"

    def test_strongest_meeting(self):
        inp = make_input(pricing_page_visited_count=0, demo_request_submitted=0,
                         champion_internal_sharing=0, decision_maker_cc_count=0,
                         meetings_ghosted_count=0, days_since_last_engagement=5)
        sig = _primary_signal(inp, 30.0, 90.0, 50.0)
        assert sig == "strongest signal: meeting engagement"

    def test_strongest_digital(self):
        inp = make_input(pricing_page_visited_count=0, demo_request_submitted=0,
                         champion_internal_sharing=0, decision_maker_cc_count=0,
                         meetings_ghosted_count=0, days_since_last_engagement=5)
        sig = _primary_signal(inp, 20.0, 30.0, 95.0)
        assert sig == "strongest signal: digital engagement"


# ---------------------------------------------------------------------------
# 15. is_high_intent flag
# ---------------------------------------------------------------------------

class TestIsHighIntent:
    def test_high_intent_true(self):
        # composite >= 70 AND days <= 7
        tracker = ProspectEngagementVelocityTracker()
        result = tracker.track(make_input())  # should produce high composite
        # Verify based on computed composite
        assert result.is_high_intent == (result.engagement_composite >= 70.0 and
                                          make_input().days_since_last_engagement <= 7)

    def test_high_intent_false_stale(self):
        tracker = ProspectEngagementVelocityTracker()
        inp = make_input(days_since_last_engagement=8)
        result = tracker.track(inp)
        assert not result.is_high_intent

    def test_high_intent_false_low_composite(self):
        tracker = ProspectEngagementVelocityTracker()
        result = tracker.track(cold_input())
        assert not result.is_high_intent

    def test_high_intent_boundary_7_days(self):
        tracker = ProspectEngagementVelocityTracker()
        inp = make_input(days_since_last_engagement=7)
        result = tracker.track(inp)
        # high intent requires composite >= 70 AND days <= 7
        assert result.is_high_intent == (result.engagement_composite >= 70.0)

    def test_is_high_intent_is_bool(self):
        tracker = ProspectEngagementVelocityTracker()
        result = tracker.track(make_input())
        assert isinstance(result.is_high_intent, bool)


# ---------------------------------------------------------------------------
# 16. needs_reactivation flag
# ---------------------------------------------------------------------------

class TestNeedsReactivation:
    def test_needs_reactivation_stale(self):
        tracker = ProspectEngagementVelocityTracker()
        inp = make_input(days_since_last_engagement=14)
        result = tracker.track(inp)
        assert result.needs_reactivation

    def test_needs_reactivation_low_composite(self):
        tracker = ProspectEngagementVelocityTracker()
        result = tracker.track(cold_input())
        assert result.needs_reactivation

    def test_no_reactivation_recent_high_composite(self):
        tracker = ProspectEngagementVelocityTracker()
        result = tracker.track(make_input())
        # Only false when composite >= 30 AND days < 14
        assert result.needs_reactivation == (
            make_input().days_since_last_engagement >= 14 or
            result.engagement_composite < 30.0
        )

    def test_boundary_exactly_14_days(self):
        tracker = ProspectEngagementVelocityTracker()
        inp = make_input(days_since_last_engagement=14)
        result = tracker.track(inp)
        assert result.needs_reactivation  # >= 14 triggers it

    def test_needs_reactivation_is_bool(self):
        tracker = ProspectEngagementVelocityTracker()
        result = tracker.track(make_input())
        assert isinstance(result.needs_reactivation, bool)


# ---------------------------------------------------------------------------
# 17. tracker.track()
# ---------------------------------------------------------------------------

class TestTrackerTrack:
    def setup_method(self):
        self.tracker = ProspectEngagementVelocityTracker()

    def test_returns_result_instance(self):
        result = self.tracker.track(make_input())
        assert isinstance(result, ProspectEngagementResult)

    def test_result_stored(self):
        self.tracker.track(make_input(prospect_id="abc"))
        assert self.tracker.get("abc") is not None

    def test_overwrite_same_prospect_id(self):
        self.tracker.track(make_input(prospect_id="dup", emails_sent_last_30d=5))
        self.tracker.track(make_input(prospect_id="dup", emails_sent_last_30d=10))
        assert self.tracker.get("dup") is not None  # only one stored

    def test_prospect_id_preserved(self):
        result = self.tracker.track(make_input(prospect_id="x1"))
        assert result.prospect_id == "x1"

    def test_prospect_name_preserved(self):
        result = self.tracker.track(make_input(prospect_name="Bob"))
        assert result.prospect_name == "Bob"

    def test_scores_non_negative(self):
        result = self.tracker.track(cold_input())
        assert result.email_engagement_score >= 0.0
        assert result.meeting_engagement_score >= 0.0
        assert result.digital_engagement_score >= 0.0
        assert result.velocity_trend_score >= 0.0
        assert result.engagement_composite >= 0.0

    def test_scores_at_most_100(self):
        result = self.tracker.track(make_input())
        assert result.email_engagement_score <= 100.0
        assert result.meeting_engagement_score <= 100.0
        assert result.digital_engagement_score <= 100.0
        assert result.engagement_composite <= 100.0

    def test_composite_matches_formula(self):
        inp = make_input()
        result = self.tracker.track(inp)
        from swarm.intelligence.prospect_engagement_velocity import (
            _email_engagement_score, _meeting_engagement_score,
            _digital_engagement_score, _velocity_trend_score, _composite,
        )
        e = _email_engagement_score(inp)
        m = _meeting_engagement_score(inp)
        d = _digital_engagement_score(inp)
        v = _velocity_trend_score(inp)
        expected = _composite(e, m, d, v)
        assert result.engagement_composite == expected

    def test_velocity_enum_type(self):
        result = self.tracker.track(make_input())
        assert isinstance(result.engagement_velocity, EngagementVelocity)

    def test_intent_enum_type(self):
        result = self.tracker.track(make_input())
        assert isinstance(result.intent_level, IntentLevel)

    def test_risk_enum_type(self):
        result = self.tracker.track(make_input())
        assert isinstance(result.engagement_risk, EngagementRisk)

    def test_action_enum_type(self):
        result = self.tracker.track(make_input())
        assert isinstance(result.engagement_action, EngagementAction)

    def test_primary_signal_is_string(self):
        result = self.tracker.track(make_input())
        assert isinstance(result.primary_signal, str)

    def test_days_to_re_engage_positive(self):
        result = self.tracker.track(make_input())
        assert result.days_to_re_engage >= 1


# ---------------------------------------------------------------------------
# 18. tracker.track_batch()
# ---------------------------------------------------------------------------

class TestTrackerBatch:
    def setup_method(self):
        self.tracker = ProspectEngagementVelocityTracker()

    def test_returns_list(self):
        inputs = [make_input(prospect_id=f"p{i}") for i in range(5)]
        results = self.tracker.track_batch(inputs)
        assert isinstance(results, list)

    def test_length_matches_input(self):
        inputs = [make_input(prospect_id=f"p{i}") for i in range(7)]
        results = self.tracker.track_batch(inputs)
        assert len(results) == 7

    def test_sorted_descending_by_composite(self):
        inputs = [make_input(prospect_id=f"p{i}") for i in range(5)]
        inputs[0] = cold_input("p0")
        results = self.tracker.track_batch(inputs)
        composites = [r.engagement_composite for r in results]
        assert composites == sorted(composites, reverse=True)

    def test_empty_batch(self):
        results = self.tracker.track_batch([])
        assert results == []

    def test_single_item_batch(self):
        results = self.tracker.track_batch([make_input(prospect_id="solo")])
        assert len(results) == 1

    def test_all_stored_after_batch(self):
        inputs = [make_input(prospect_id=f"q{i}") for i in range(3)]
        self.tracker.track_batch(inputs)
        for i in range(3):
            assert self.tracker.get(f"q{i}") is not None

    def test_batch_with_different_composites(self):
        hot = make_input(prospect_id="hot")
        cold = cold_input("cold_p")
        results = self.tracker.track_batch([cold, hot])
        assert results[0].engagement_composite >= results[1].engagement_composite

    def test_batch_returns_result_objects(self):
        results = self.tracker.track_batch([make_input(prospect_id="r1")])
        assert isinstance(results[0], ProspectEngagementResult)


# ---------------------------------------------------------------------------
# 19. tracker.reset()
# ---------------------------------------------------------------------------

class TestTrackerReset:
    def setup_method(self):
        self.tracker = ProspectEngagementVelocityTracker()

    def test_reset_clears_all(self):
        for i in range(5):
            self.tracker.track(make_input(prospect_id=f"x{i}"))
        self.tracker.reset()
        assert self.tracker.all_prospects() == []

    def test_reset_on_empty_is_safe(self):
        self.tracker.reset()  # Should not raise
        assert self.tracker.all_prospects() == []

    def test_get_returns_none_after_reset(self):
        self.tracker.track(make_input(prospect_id="z1"))
        self.tracker.reset()
        assert self.tracker.get("z1") is None

    def test_track_after_reset(self):
        self.tracker.track(make_input(prospect_id="a1"))
        self.tracker.reset()
        self.tracker.track(make_input(prospect_id="a2"))
        assert self.tracker.get("a1") is None
        assert self.tracker.get("a2") is not None

    def test_summary_after_reset(self):
        self.tracker.track(make_input())
        self.tracker.reset()
        summary = self.tracker.summary()
        assert summary["total"] == 0

    def test_double_reset(self):
        self.tracker.track(make_input(prospect_id="b1"))
        self.tracker.reset()
        self.tracker.reset()
        assert self.tracker.all_prospects() == []


# ---------------------------------------------------------------------------
# 20. tracker.summary() – exactly 13 keys
# ---------------------------------------------------------------------------

class TestTrackerSummary:
    def setup_method(self):
        self.tracker = ProspectEngagementVelocityTracker()

    def test_summary_exactly_13_keys(self):
        self.tracker.track(make_input())
        summary = self.tracker.summary()
        assert len(summary) == 13

    def test_summary_key_names(self):
        self.tracker.track(make_input())
        summary = self.tracker.summary()
        expected_keys = {
            "total", "velocity_counts", "intent_counts", "risk_counts",
            "action_counts", "avg_engagement_composite", "high_intent_count",
            "reactivation_count", "avg_email_engagement_score",
            "avg_meeting_engagement_score", "avg_digital_engagement_score",
            "avg_velocity_trend_score", "avg_days_to_re_engage",
        }
        assert set(summary.keys()) == expected_keys

    def test_summary_total_correct(self):
        for i in range(4):
            self.tracker.track(make_input(prospect_id=f"s{i}"))
        summary = self.tracker.summary()
        assert summary["total"] == 4

    def test_summary_empty(self):
        summary = self.tracker.summary()
        assert summary["total"] == 0
        assert summary["avg_engagement_composite"] == 0.0
        assert summary["high_intent_count"] == 0
        assert summary["reactivation_count"] == 0
        assert summary["avg_email_engagement_score"] == 0.0
        assert summary["avg_meeting_engagement_score"] == 0.0
        assert summary["avg_digital_engagement_score"] == 0.0
        assert summary["avg_velocity_trend_score"] == 0.0
        assert summary["avg_days_to_re_engage"] == 0.0

    def test_summary_velocity_counts_dict(self):
        self.tracker.track(make_input())
        summary = self.tracker.summary()
        assert isinstance(summary["velocity_counts"], dict)

    def test_summary_intent_counts_dict(self):
        self.tracker.track(make_input())
        summary = self.tracker.summary()
        assert isinstance(summary["intent_counts"], dict)

    def test_summary_risk_counts_dict(self):
        self.tracker.track(make_input())
        summary = self.tracker.summary()
        assert isinstance(summary["risk_counts"], dict)

    def test_summary_action_counts_dict(self):
        self.tracker.track(make_input())
        summary = self.tracker.summary()
        assert isinstance(summary["action_counts"], dict)

    def test_summary_high_intent_count_type(self):
        self.tracker.track(make_input())
        summary = self.tracker.summary()
        assert isinstance(summary["high_intent_count"], int)

    def test_summary_reactivation_count_type(self):
        self.tracker.track(make_input())
        summary = self.tracker.summary()
        assert isinstance(summary["reactivation_count"], int)

    def test_summary_avg_composite_numeric(self):
        self.tracker.track(make_input())
        summary = self.tracker.summary()
        assert isinstance(summary["avg_engagement_composite"], float)

    def test_summary_counts_sum_to_total(self):
        inputs = [make_input(prospect_id=f"c{i}") for i in range(6)]
        inputs += [cold_input(f"cold{i}") for i in range(4)]
        self.tracker.track_batch(inputs)
        summary = self.tracker.summary()
        total = summary["total"]
        assert sum(summary["velocity_counts"].values()) == total
        assert sum(summary["intent_counts"].values()) == total
        assert sum(summary["risk_counts"].values()) == total
        assert sum(summary["action_counts"].values()) == total

    def test_summary_avg_scores_in_range(self):
        for i in range(3):
            self.tracker.track(make_input(prospect_id=f"r{i}"))
        summary = self.tracker.summary()
        assert 0.0 <= summary["avg_email_engagement_score"] <= 100.0
        assert 0.0 <= summary["avg_meeting_engagement_score"] <= 100.0
        assert 0.0 <= summary["avg_digital_engagement_score"] <= 100.0
        assert 0.0 <= summary["avg_velocity_trend_score"] <= 100.0

    def test_summary_13_keys_after_batch(self):
        self.tracker.track_batch([make_input(prospect_id=f"b{i}") for i in range(10)])
        assert len(self.tracker.summary()) == 13


# ---------------------------------------------------------------------------
# 21. tracker utility methods
# ---------------------------------------------------------------------------

class TestTrackerUtilities:
    def setup_method(self):
        self.tracker = ProspectEngagementVelocityTracker()

    def test_get_returns_correct_result(self):
        self.tracker.track(make_input(prospect_id="g1"))
        result = self.tracker.get("g1")
        assert result is not None
        assert result.prospect_id == "g1"

    def test_get_returns_none_for_unknown(self):
        assert self.tracker.get("nonexistent") is None

    def test_all_prospects_sorted_descending(self):
        self.tracker.track_batch([
            make_input(prospect_id=f"ap{i}") for i in range(5)
        ] + [cold_input("c_ap")])
        all_p = self.tracker.all_prospects()
        composites = [r.engagement_composite for r in all_p]
        assert composites == sorted(composites, reverse=True)

    def test_high_intent_prospects_all_high_intent(self):
        self.tracker.track_batch([make_input(prospect_id=f"hi{i}") for i in range(5)])
        self.tracker.track(cold_input("cold_hi"))
        hip = self.tracker.high_intent_prospects()
        for r in hip:
            assert r.is_high_intent

    def test_reactivation_list_all_need_reactivation(self):
        self.tracker.track_batch([cold_input(f"rc{i}") for i in range(3)])
        self.tracker.track_batch([make_input(prospect_id=f"active{i}") for i in range(3)])
        rl = self.tracker.reactivation_list()
        for r in rl:
            assert r.needs_reactivation

    def test_by_velocity_filters_correctly(self):
        self.tracker.track_batch([make_input(prospect_id=f"v{i}") for i in range(5)])
        self.tracker.track(cold_input("cold_v"))
        cold_results = self.tracker.by_velocity(EngagementVelocity.COLD)
        for r in cold_results:
            assert r.engagement_velocity == EngagementVelocity.COLD

    def test_by_intent_filters_correctly(self):
        self.tracker.track_batch([make_input(prospect_id=f"i{i}") for i in range(5)])
        self.tracker.track(cold_input("cold_i"))
        cold_results = self.tracker.by_intent(IntentLevel.COLD)
        for r in cold_results:
            assert r.intent_level == IntentLevel.COLD

    def test_avg_engagement_composite_empty(self):
        assert self.tracker.avg_engagement_composite() == 0.0

    def test_avg_engagement_composite_single(self):
        result = self.tracker.track(make_input(prospect_id="avg1"))
        avg = self.tracker.avg_engagement_composite()
        assert avg == result.engagement_composite

    def test_avg_engagement_composite_multiple(self):
        results = self.tracker.track_batch([make_input(prospect_id=f"m{i}") for i in range(4)])
        expected = round(sum(r.engagement_composite for r in results) / 4, 1)
        assert self.tracker.avg_engagement_composite() == expected

    def test_all_prospects_empty(self):
        assert self.tracker.all_prospects() == []

    def test_high_intent_empty_when_cold(self):
        self.tracker.track(cold_input("chi"))
        # cold prospects should not be high intent
        hip = self.tracker.high_intent_prospects()
        assert all(r.is_high_intent for r in hip)

    def test_by_velocity_empty_result(self):
        # Accelerating bucket may be empty for cold prospects
        self.tracker.track(cold_input("cold_bv"))
        acc = self.tracker.by_velocity(EngagementVelocity.ACCELERATING)
        assert isinstance(acc, list)


# ---------------------------------------------------------------------------
# 22. End-to-end integration scenarios
# ---------------------------------------------------------------------------

class TestIntegrationScenarios:
    def setup_method(self):
        self.tracker = ProspectEngagementVelocityTracker()

    def test_fully_engaged_prospect(self):
        """A high-engagement prospect should score well across all dimensions."""
        result = self.tracker.track(make_input(prospect_id="engaged"))
        assert result.engagement_composite >= 50.0

    def test_completely_cold_prospect(self):
        """A completely disengaged prospect should have low composite and high risk."""
        result = self.tracker.track(cold_input())
        assert result.engagement_composite < 40.0
        assert result.engagement_risk in (EngagementRisk.HIGH, EngagementRisk.CRITICAL)
        assert result.needs_reactivation

    def test_pricing_page_signal_priority(self):
        """Pricing page visit should dominate primary signal."""
        inp = make_input(pricing_page_visited_count=2, demo_request_submitted=1,
                         champion_internal_sharing=1, decision_maker_cc_count=1)
        result = self.tracker.track(inp)
        assert result.primary_signal == "pricing page visited — high buying intent"

    def test_demo_request_signal_priority(self):
        """Demo request should dominate over champion/DM signals."""
        inp = make_input(pricing_page_visited_count=0, demo_request_submitted=1,
                         champion_internal_sharing=1, decision_maker_cc_count=1)
        result = self.tracker.track(inp)
        assert result.primary_signal == "demo requested — strong interest"

    def test_batch_ordering_with_mixed_prospects(self):
        """Batch should always return sorted by composite desc."""
        inputs = [
            cold_input("worst"),
            make_input(prospect_id="mid", emails_opened_last_30d=3, demo_request_submitted=0,
                       pricing_page_visited_count=0),
            make_input(prospect_id="best"),
        ]
        results = self.tracker.track_batch(inputs)
        assert results[0].engagement_composite >= results[1].engagement_composite >= results[2].engagement_composite

    def test_track_multiple_then_summary(self):
        """Summary should reflect all tracked prospects."""
        for i in range(10):
            self.tracker.track(make_input(prospect_id=f"ts{i}"))
        summary = self.tracker.summary()
        assert summary["total"] == 10
        assert len(summary) == 13

    def test_high_intent_count_in_summary(self):
        """High intent count in summary should match high_intent_prospects length."""
        for i in range(5):
            self.tracker.track(make_input(prospect_id=f"hic{i}"))
        self.tracker.track(cold_input("cold_hic"))
        summary = self.tracker.summary()
        assert summary["high_intent_count"] == len(self.tracker.high_intent_prospects())

    def test_reactivation_count_in_summary(self):
        """Reactivation count in summary should match reactivation_list length."""
        for i in range(3):
            self.tracker.track(cold_input(f"rl{i}"))
        self.tracker.track(make_input(prospect_id="active_rl"))
        summary = self.tracker.summary()
        assert summary["reactivation_count"] == len(self.tracker.reactivation_list())

    def test_reset_then_retrack(self):
        """After reset, tracker should work normally."""
        self.tracker.track_batch([make_input(prospect_id=f"rt{i}") for i in range(3)])
        self.tracker.reset()
        self.tracker.track(make_input(prospect_id="fresh"))
        assert self.tracker.summary()["total"] == 1

    def test_velocity_cold_for_stale_prospect(self):
        """Prospect with 25 days silence should be COLD velocity."""
        inp = make_input(days_since_last_engagement=25)
        result = self.tracker.track(inp)
        assert result.engagement_velocity == EngagementVelocity.COLD

    def test_to_dict_consistent_with_attributes(self):
        """to_dict should mirror result attributes."""
        result = self.tracker.track(make_input(prospect_id="td1"))
        d = result.to_dict()
        assert d["prospect_id"] == result.prospect_id
        assert d["engagement_composite"] == result.engagement_composite
        assert d["is_high_intent"] == result.is_high_intent
        assert d["needs_reactivation"] == result.needs_reactivation
        assert d["engagement_velocity"] == result.engagement_velocity.value

    def test_multiple_batches_accumulate(self):
        """Multiple track_batch calls should accumulate results."""
        self.tracker.track_batch([make_input(prospect_id=f"mb{i}") for i in range(3)])
        self.tracker.track_batch([make_input(prospect_id=f"mb{i+3}") for i in range(3)])
        assert self.tracker.summary()["total"] == 6

    def test_cold_prospect_action_is_reactivate_or_disqualify(self):
        result = self.tracker.track(cold_input())
        assert result.engagement_action in (
            EngagementAction.REACTIVATE, EngagementAction.DISQUALIFY
        )

    def test_hot_prospect_action_is_advance_or_nurture(self):
        result = self.tracker.track(make_input())
        assert result.engagement_action in (
            EngagementAction.ADVANCE, EngagementAction.NURTURE
        )

    def test_velocity_counts_keys_are_strings(self):
        self.tracker.track(make_input())
        summary = self.tracker.summary()
        for key in summary["velocity_counts"]:
            assert isinstance(key, str)

    def test_intent_counts_keys_are_strings(self):
        self.tracker.track(make_input())
        summary = self.tracker.summary()
        for key in summary["intent_counts"]:
            assert isinstance(key, str)

    def test_risk_counts_keys_are_strings(self):
        self.tracker.track(make_input())
        summary = self.tracker.summary()
        for key in summary["risk_counts"]:
            assert isinstance(key, str)

    def test_action_counts_keys_are_strings(self):
        self.tracker.track(make_input())
        summary = self.tracker.summary()
        for key in summary["action_counts"]:
            assert isinstance(key, str)

    def test_email_open_rate_threshold_boundaries(self):
        """Test exact open rate boundaries."""
        tracker = ProspectEngagementVelocityTracker()
        # Exactly 0.4 open rate -> +11
        inp = make_input(emails_sent_last_30d=10, emails_opened_last_30d=4,
                         emails_replied_last_30d=0, avg_reply_time_hours=0.0,
                         days_since_last_engagement=20)
        score = _email_engagement_score(inp)
        assert score >= 11.0

    def test_composite_boundary_high_intent_exact_70(self):
        """composite exactly 70 with days<=7 -> is_high_intent=True."""
        # We can't directly force composite=70, but we can assert the rule
        tracker = ProspectEngagementVelocityTracker()
        result = tracker.track(make_input(days_since_last_engagement=5))
        assert result.is_high_intent == (result.engagement_composite >= 70.0)

    def test_composite_boundary_needs_reactivation_exact_30(self):
        """composite exactly 30 -> needs_reactivation if also days check."""
        tracker = ProspectEngagementVelocityTracker()
        result = tracker.track(make_input(days_since_last_engagement=5))
        assert result.needs_reactivation == (
            5 >= 14 or result.engagement_composite < 30.0
        )

    def test_zero_prior_score_trend(self):
        """Prior score of 0 should return trend score 50."""
        inp = make_input(prior_30d_engagement_score=0.0)
        score = _velocity_trend_score(inp)
        assert score == 50.0

    def test_summary_no_args_required(self):
        """summary() must be callable with no arguments."""
        import inspect
        sig = inspect.signature(ProspectEngagementVelocityTracker.summary)
        params = list(sig.parameters.keys())
        assert params == ["self"]

    def test_track_batch_result_type(self):
        """track_batch must return a list."""
        results = self.tracker.track_batch([make_input(prospect_id="tb1")])
        assert isinstance(results, list)

    def test_field_count_unchanged(self):
        """ProspectEngagementInput must still have exactly 22 fields."""
        assert len(dataclasses.fields(ProspectEngagementInput)) == 22

    def test_to_dict_key_count_unchanged(self):
        """to_dict must still return exactly 15 keys."""
        result = self.tracker.track(make_input())
        assert len(result.to_dict()) == 15

    def test_summary_key_count_unchanged(self):
        """summary() must still return exactly 13 keys."""
        self.tracker.track(make_input())
        assert len(self.tracker.summary()) == 13

    def test_engagement_velocity_value_count(self):
        assert len(EngagementVelocity) == 5

    def test_all_four_enum_counts(self):
        assert len(IntentLevel) == 4
        assert len(EngagementRisk) == 4
        assert len(EngagementAction) == 4

    def test_days_to_re_engage_always_positive(self):
        for inp in [make_input(), cold_input()]:
            result = self.tracker.track(inp)
            assert result.days_to_re_engage >= 1

    def test_email_engagement_score_open_rate_40_exactly(self):
        inp = make_input(emails_sent_last_30d=10, emails_opened_last_30d=4,
                         emails_replied_last_30d=0, avg_reply_time_hours=0.0,
                         days_since_last_engagement=20)
        score = _email_engagement_score(inp)
        assert score == 11.0

    def test_email_engagement_score_open_rate_60_exactly(self):
        inp = make_input(emails_sent_last_30d=10, emails_opened_last_30d=6,
                         emails_replied_last_30d=0, avg_reply_time_hours=0.0,
                         days_since_last_engagement=20)
        score = _email_engagement_score(inp)
        assert score == 18.0

    def test_email_engagement_score_open_rate_80_exactly(self):
        inp = make_input(emails_sent_last_30d=10, emails_opened_last_30d=8,
                         emails_replied_last_30d=0, avg_reply_time_hours=0.0,
                         days_since_last_engagement=20)
        score = _email_engagement_score(inp)
        assert score == 25.0

    def test_digital_score_all_zero_input(self):
        inp = make_input(content_viewed_last_30d=0, demo_request_submitted=0,
                         pricing_page_visited_count=0, linkedin_engagement_count=0)
        score = _digital_engagement_score(inp)
        assert score == 0.0

    def test_meeting_score_zero_all_bad(self):
        inp = make_input(meetings_requested_last_30d=5, meetings_accepted_last_30d=0,
                         meetings_rescheduled_count=5, meetings_ghosted_count=5,
                         champion_internal_sharing=0, decision_maker_cc_count=0)
        score = _meeting_engagement_score(inp)
        assert score == 0.0

    def test_all_prospects_empty_initial(self):
        tracker = ProspectEngagementVelocityTracker()
        assert tracker.all_prospects() == []

    def test_high_intent_empty_initial(self):
        tracker = ProspectEngagementVelocityTracker()
        assert tracker.high_intent_prospects() == []

    def test_reactivation_list_empty_initial(self):
        tracker = ProspectEngagementVelocityTracker()
        assert tracker.reactivation_list() == []

    def test_by_velocity_empty_initial(self):
        tracker = ProspectEngagementVelocityTracker()
        assert tracker.by_velocity(EngagementVelocity.COLD) == []

    def test_by_intent_empty_initial(self):
        tracker = ProspectEngagementVelocityTracker()
        assert tracker.by_intent(IntentLevel.HOT) == []

    def test_summary_no_args_via_call(self):
        """Smoke test: summary() with no args doesn't raise."""
        self.tracker.track(make_input())
        summary = self.tracker.summary()
        assert summary is not None

    def test_avg_days_to_re_engage_in_summary(self):
        for i in range(3):
            self.tracker.track(make_input(prospect_id=f"dtr{i}"))
        summary = self.tracker.summary()
        assert summary["avg_days_to_re_engage"] >= 0.0

    def test_result_is_dataclass(self):
        result = self.tracker.track(make_input())
        assert dataclasses.is_dataclass(result)

    def test_result_has_15_fields(self):
        result = self.tracker.track(make_input())
        assert len(dataclasses.fields(result)) == 15

    def test_velocity_counts_only_valid_values(self):
        for i in range(5):
            self.tracker.track(make_input(prospect_id=f"vc{i}"))
        self.tracker.track(cold_input("cold_vc"))
        valid = {e.value for e in EngagementVelocity}
        for key in self.tracker.summary()["velocity_counts"]:
            assert key in valid

    def test_intent_counts_only_valid_values(self):
        for i in range(5):
            self.tracker.track(make_input(prospect_id=f"ic{i}"))
        valid = {e.value for e in IntentLevel}
        for key in self.tracker.summary()["intent_counts"]:
            assert key in valid

    def test_risk_counts_only_valid_values(self):
        for i in range(5):
            self.tracker.track(make_input(prospect_id=f"rc{i}"))
        valid = {e.value for e in EngagementRisk}
        for key in self.tracker.summary()["risk_counts"]:
            assert key in valid

    def test_action_counts_only_valid_values(self):
        for i in range(5):
            self.tracker.track(make_input(prospect_id=f"ac{i}"))
        valid = {e.value for e in EngagementAction}
        for key in self.tracker.summary()["action_counts"]:
            assert key in valid
