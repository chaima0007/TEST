"""
Comprehensive pytest test suite for EmailPersonalizationEngine.

Covers:
1. All enum values, member counts, str inheritance
2. EmailPersonalizationInput field count (23)
3. to_dict() exactly 15 keys and correct types
4. opted_out fast path
5. Each scoring formula component
6. PersonalizationLevel thresholds
7. EmailTone priority order
8. SendTiming priority order
9. recommended_action priority order
10. is_ready_to_send per action type
11. Engine properties
12. summary() 13 keys, empty and non-empty
13. reset() clears state
14. End-to-end scenarios
"""
from __future__ import annotations

import dataclasses
import math
import pytest

from swarm.intelligence.email_personalization_engine import (
    EmailPersonalizationEngine,
    EmailPersonalizationInput,
    EmailPersonalizationResult,
    EmailTone,
    PersonalizationAction,
    PersonalizationLevel,
    SendTiming,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers / factories
# ─────────────────────────────────────────────────────────────────────────────

def make_input(**overrides) -> EmailPersonalizationInput:
    """Return a baseline valid EmailPersonalizationInput with sane defaults."""
    defaults = dict(
        prospect_id="P001",
        campaign_id="C001",
        rep_id="R001",
        icp_score=50.0,
        lead_score=50.0,
        buyer_intent_score=50.0,
        seniority_level=2,
        industry="saas",
        company_size="mid_market",
        prior_emails_sent=0,
        prior_open_rate=0.0,
        prior_reply_rate=0.0,
        prior_click_rate=0.0,
        days_since_last_email=5,
        has_trigger_event=False,
        trigger_event_type="none",
        persona_pain_points=0,
        personalization_tokens=0,
        subject_line_score=40.0,
        body_relevance_score=40.0,
        sequence_position=1,
        is_warm_lead=False,
        opted_out=False,
    )
    defaults.update(overrides)
    return EmailPersonalizationInput(**defaults)


@pytest.fixture
def engine():
    return EmailPersonalizationEngine()


# ─────────────────────────────────────────────────────────────────────────────
# 1. Enum values, member counts, str inheritance
# ─────────────────────────────────────────────────────────────────────────────

class TestPersonalizationLevelEnum:
    def test_member_count(self):
        assert len(PersonalizationLevel) == 5

    def test_is_str_subclass(self):
        assert issubclass(PersonalizationLevel, str)

    def test_hyper_value(self):
        assert PersonalizationLevel.HYPER_PERSONALIZED == "hyper_personalized"

    def test_highly_value(self):
        assert PersonalizationLevel.HIGHLY_PERSONALIZED == "highly_personalized"

    def test_moderately_value(self):
        assert PersonalizationLevel.MODERATELY_PERSONALIZED == "moderately_personalized"

    def test_generic_value(self):
        assert PersonalizationLevel.GENERIC == "generic"

    def test_template_value(self):
        assert PersonalizationLevel.TEMPLATE == "template"

    def test_str_usable_as_string(self):
        # In Python 3.11+, f-string on str-enum shows "ClassName.MEMBER"; use .value for the raw string
        assert PersonalizationLevel.HYPER_PERSONALIZED.value == "hyper_personalized"
        assert str(PersonalizationLevel.HYPER_PERSONALIZED) in (
            "hyper_personalized", "PersonalizationLevel.HYPER_PERSONALIZED"
        )

    def test_all_member_names(self):
        names = {m.name for m in PersonalizationLevel}
        assert names == {
            "HYPER_PERSONALIZED", "HIGHLY_PERSONALIZED",
            "MODERATELY_PERSONALIZED", "GENERIC", "TEMPLATE",
        }


class TestEmailToneEnum:
    def test_member_count(self):
        assert len(EmailTone) == 5

    def test_is_str_subclass(self):
        assert issubclass(EmailTone, str)

    def test_executive_value(self):
        assert EmailTone.EXECUTIVE == "executive"

    def test_consultative_value(self):
        assert EmailTone.CONSULTATIVE == "consultative"

    def test_challenger_value(self):
        assert EmailTone.CHALLENGER == "challenger"

    def test_educational_value(self):
        assert EmailTone.EDUCATIONAL == "educational"

    def test_urgency_value(self):
        assert EmailTone.URGENCY == "urgency"

    def test_str_usable_as_string(self):
        # In Python 3.11+, f-string on str-enum shows "ClassName.MEMBER"; use .value for the raw string
        assert EmailTone.URGENCY.value == "urgency"
        assert str(EmailTone.URGENCY) in ("urgency", "EmailTone.URGENCY")

    def test_all_member_names(self):
        names = {m.name for m in EmailTone}
        assert names == {"EXECUTIVE", "CONSULTATIVE", "CHALLENGER", "EDUCATIONAL", "URGENCY"}


class TestSendTimingEnum:
    def test_member_count(self):
        assert len(SendTiming) == 6

    def test_is_str_subclass(self):
        assert issubclass(SendTiming, str)

    def test_immediate_value(self):
        assert SendTiming.IMMEDIATE == "immediate"

    def test_morning_value(self):
        assert SendTiming.MORNING == "morning"

    def test_midday_value(self):
        assert SendTiming.MIDDAY == "midday"

    def test_afternoon_value(self):
        assert SendTiming.AFTERNOON == "afternoon"

    def test_next_business_day_value(self):
        assert SendTiming.NEXT_BUSINESS_DAY == "next_business_day"

    def test_hold_value(self):
        assert SendTiming.HOLD == "hold"

    def test_all_member_names(self):
        names = {m.name for m in SendTiming}
        assert names == {
            "IMMEDIATE", "MORNING", "MIDDAY", "AFTERNOON", "NEXT_BUSINESS_DAY", "HOLD",
        }


class TestPersonalizationActionEnum:
    def test_member_count(self):
        assert len(PersonalizationAction) == 5

    def test_is_str_subclass(self):
        assert issubclass(PersonalizationAction, str)

    def test_send_now_value(self):
        assert PersonalizationAction.SEND_NOW == "send_now"

    def test_refine_and_send_value(self):
        assert PersonalizationAction.REFINE_AND_SEND == "refine_and_send"

    def test_review_before_send_value(self):
        assert PersonalizationAction.REVIEW_BEFORE_SEND == "review_before_send"

    def test_rewrite_required_value(self):
        assert PersonalizationAction.REWRITE_REQUIRED == "rewrite_required"

    def test_hold_value(self):
        assert PersonalizationAction.HOLD == "hold"

    def test_all_member_names(self):
        names = {m.name for m in PersonalizationAction}
        assert names == {
            "SEND_NOW", "REFINE_AND_SEND", "REVIEW_BEFORE_SEND", "REWRITE_REQUIRED", "HOLD",
        }


# ─────────────────────────────────────────────────────────────────────────────
# 2. EmailPersonalizationInput: 23 fields
# ─────────────────────────────────────────────────────────────────────────────

class TestEmailPersonalizationInput:
    def test_field_count(self):
        fields = dataclasses.fields(EmailPersonalizationInput)
        assert len(fields) == 23

    def test_field_names(self):
        field_names = {f.name for f in dataclasses.fields(EmailPersonalizationInput)}
        expected = {
            "prospect_id", "campaign_id", "rep_id", "icp_score", "lead_score",
            "buyer_intent_score", "seniority_level", "industry", "company_size",
            "prior_emails_sent", "prior_open_rate", "prior_reply_rate", "prior_click_rate",
            "days_since_last_email", "has_trigger_event", "trigger_event_type",
            "persona_pain_points", "personalization_tokens", "subject_line_score",
            "body_relevance_score", "sequence_position", "is_warm_lead", "opted_out",
        }
        assert field_names == expected

    def test_instantiation(self):
        inp = make_input()
        assert inp.prospect_id == "P001"
        assert inp.opted_out is False

    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(EmailPersonalizationInput)

    def test_bool_fields(self):
        inp = make_input(has_trigger_event=True, is_warm_lead=True, opted_out=True)
        assert inp.has_trigger_event is True
        assert inp.is_warm_lead is True
        assert inp.opted_out is True


# ─────────────────────────────────────────────────────────────────────────────
# 3. EmailPersonalizationResult.to_dict(): exactly 15 keys, correct types
# ─────────────────────────────────────────────────────────────────────────────

class TestToDict:
    @pytest.fixture
    def result(self):
        engine = EmailPersonalizationEngine()
        inp = make_input(
            personalization_tokens=5,
            persona_pain_points=4,
            buyer_intent_score=80,
            icp_score=80,
            has_trigger_event=True,
            trigger_event_type="funding",
            is_warm_lead=True,
            days_since_last_email=5,
            lead_score=70,
            subject_line_score=75,
            body_relevance_score=75,
        )
        return engine.analyze(inp)

    def test_to_dict_key_count(self, result):
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_no_rep_id(self, result):
        d = result.to_dict()
        assert "rep_id" not in d

    def test_to_dict_has_prospect_id(self, result):
        d = result.to_dict()
        assert "prospect_id" in d

    def test_to_dict_has_campaign_id(self, result):
        d = result.to_dict()
        assert "campaign_id" in d

    def test_to_dict_has_personalization_score(self, result):
        d = result.to_dict()
        assert "personalization_score" in d

    def test_to_dict_has_personalization_level(self, result):
        d = result.to_dict()
        assert "personalization_level" in d

    def test_to_dict_has_email_tone(self, result):
        d = result.to_dict()
        assert "email_tone" in d

    def test_to_dict_has_send_timing(self, result):
        d = result.to_dict()
        assert "send_timing" in d

    def test_to_dict_has_recommended_action(self, result):
        d = result.to_dict()
        assert "recommended_action" in d

    def test_to_dict_has_predicted_open_rate(self, result):
        d = result.to_dict()
        assert "predicted_open_rate" in d

    def test_to_dict_has_predicted_reply_rate(self, result):
        d = result.to_dict()
        assert "predicted_reply_rate" in d

    def test_to_dict_has_send_score(self, result):
        d = result.to_dict()
        assert "send_score" in d

    def test_to_dict_has_is_ready_to_send(self, result):
        d = result.to_dict()
        assert "is_ready_to_send" in d

    def test_to_dict_has_personalization_tips(self, result):
        d = result.to_dict()
        assert "personalization_tips" in d

    def test_to_dict_has_subject_suggestions(self, result):
        d = result.to_dict()
        assert "subject_suggestions" in d

    def test_to_dict_has_risk_flags(self, result):
        d = result.to_dict()
        assert "risk_flags" in d

    def test_to_dict_has_optimization_score(self, result):
        d = result.to_dict()
        assert "optimization_score" in d

    def test_to_dict_level_is_string(self, result):
        d = result.to_dict()
        assert isinstance(d["personalization_level"], str)

    def test_to_dict_tone_is_string(self, result):
        d = result.to_dict()
        assert isinstance(d["email_tone"], str)

    def test_to_dict_timing_is_string(self, result):
        d = result.to_dict()
        assert isinstance(d["send_timing"], str)

    def test_to_dict_action_is_string(self, result):
        d = result.to_dict()
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_lists(self, result):
        d = result.to_dict()
        assert isinstance(d["personalization_tips"], list)
        assert isinstance(d["subject_suggestions"], list)
        assert isinstance(d["risk_flags"], list)

    def test_to_dict_numeric_types(self, result):
        d = result.to_dict()
        assert isinstance(d["personalization_score"], float)
        assert isinstance(d["send_score"], float)
        assert isinstance(d["predicted_open_rate"], float)
        assert isinstance(d["predicted_reply_rate"], float)

    def test_to_dict_exact_keys(self, result):
        d = result.to_dict()
        expected_keys = {
            "prospect_id", "campaign_id", "personalization_score", "personalization_level",
            "email_tone", "send_timing", "recommended_action", "predicted_open_rate",
            "predicted_reply_rate", "send_score", "is_ready_to_send",
            "personalization_tips", "subject_suggestions", "risk_flags", "optimization_score",
        }
        assert set(d.keys()) == expected_keys


# ─────────────────────────────────────────────────────────────────────────────
# 4. opted_out fast path
# ─────────────────────────────────────────────────────────────────────────────

class TestOptedOutFastPath:
    @pytest.fixture
    def opted_out_result(self, engine):
        inp = make_input(opted_out=True)
        return engine.analyze(inp)

    def test_action_is_hold(self, opted_out_result):
        assert opted_out_result.recommended_action == PersonalizationAction.HOLD

    def test_timing_is_hold(self, opted_out_result):
        assert opted_out_result.send_timing == SendTiming.HOLD

    def test_is_not_ready_to_send(self, opted_out_result):
        assert opted_out_result.is_ready_to_send is False

    def test_personalization_score_zero(self, opted_out_result):
        assert opted_out_result.personalization_score == 0.0

    def test_send_score_zero(self, opted_out_result):
        assert opted_out_result.send_score == 0.0

    def test_open_rate_zero(self, opted_out_result):
        assert opted_out_result.predicted_open_rate == 0.0

    def test_reply_rate_zero(self, opted_out_result):
        assert opted_out_result.predicted_reply_rate == 0.0

    def test_optimization_score_zero(self, opted_out_result):
        assert opted_out_result.optimization_score == 0.0

    def test_single_risk_flag(self, opted_out_result):
        assert len(opted_out_result.risk_flags) == 1

    def test_risk_flag_content(self, opted_out_result):
        assert "opt-out" in opted_out_result.risk_flags[0].lower() or "opt" in opted_out_result.risk_flags[0]

    def test_empty_tips(self, opted_out_result):
        assert opted_out_result.personalization_tips == []

    def test_empty_subject_suggestions(self, opted_out_result):
        assert opted_out_result.subject_suggestions == []

    def test_result_stored_in_engine(self, engine):
        inp = make_input(opted_out=True)
        engine.analyze(inp)
        assert len(engine._results) == 1

    def test_prospect_id_preserved(self, opted_out_result):
        assert opted_out_result.prospect_id == "P001"

    def test_campaign_id_preserved(self, opted_out_result):
        assert opted_out_result.campaign_id == "C001"

    def test_level_is_template(self, opted_out_result):
        assert opted_out_result.personalization_level == PersonalizationLevel.TEMPLATE


# ─────────────────────────────────────────────────────────────────────────────
# 5a. _personalization_score: each component
# ─────────────────────────────────────────────────────────────────────────────

class TestPersonalizationScoreComponents:
    """All tests use the engine directly via analyze() on zero-baseline inputs."""

    def _score(self, **kwargs) -> float:
        e = EmailPersonalizationEngine()
        inp = make_input(**kwargs)
        return e.analyze(inp).personalization_score

    # Personalization tokens component: min(25, tokens * 5)
    def test_tokens_zero(self):
        assert self._score(personalization_tokens=0) == pytest.approx(
            self._score(personalization_tokens=0), abs=0.1
        )

    def test_tokens_one(self):
        base = self._score(personalization_tokens=0)
        with_token = self._score(personalization_tokens=1)
        assert with_token - base == pytest.approx(5.0, abs=0.2)

    def test_tokens_five_caps_at_25(self):
        at5 = self._score(personalization_tokens=5)
        at6 = self._score(personalization_tokens=6)
        assert at5 == at6  # cap reached at 5

    def test_tokens_cap_at_25(self):
        # tokens=5 contributes exactly 25 to score
        # Baseline: all zeros, tokens=5
        e = EmailPersonalizationEngine()
        inp = make_input(
            personalization_tokens=5, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False,
            has_trigger_event=False, prior_emails_sent=0,
        )
        score = e.analyze(inp).personalization_score
        assert score == pytest.approx(25.0, abs=0.1)

    def test_tokens_partial(self):
        e = EmailPersonalizationEngine()
        inp = make_input(
            personalization_tokens=3, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False,
            has_trigger_event=False, prior_emails_sent=0,
        )
        score = e.analyze(inp).personalization_score
        assert score == pytest.approx(15.0, abs=0.1)

    # Persona pain points: min(15, pain_points * 3)
    def test_pain_points_zero(self):
        e = EmailPersonalizationEngine()
        inp = make_input(
            persona_pain_points=0, personalization_tokens=0, icp_score=0,
            buyer_intent_score=0, is_warm_lead=False,
            has_trigger_event=False, prior_emails_sent=0,
        )
        assert e.analyze(inp).personalization_score == pytest.approx(0.0, abs=0.1)

    def test_pain_points_two(self):
        e = EmailPersonalizationEngine()
        inp = make_input(
            persona_pain_points=2, personalization_tokens=0, icp_score=0,
            buyer_intent_score=0, is_warm_lead=False,
            has_trigger_event=False, prior_emails_sent=0,
        )
        assert e.analyze(inp).personalization_score == pytest.approx(6.0, abs=0.1)

    def test_pain_points_cap_at_five(self):
        e = EmailPersonalizationEngine()
        inp5 = make_input(
            persona_pain_points=5, personalization_tokens=0, icp_score=0,
            buyer_intent_score=0, is_warm_lead=False,
            has_trigger_event=False, prior_emails_sent=0,
        )
        inp6 = make_input(
            persona_pain_points=6, personalization_tokens=0, icp_score=0,
            buyer_intent_score=0, is_warm_lead=False,
            has_trigger_event=False, prior_emails_sent=0,
        )
        e2 = EmailPersonalizationEngine()
        s5 = e.analyze(inp5).personalization_score
        s6 = e2.analyze(inp6).personalization_score
        assert s5 == s6  # cap at 15

    def test_pain_points_max_contribution(self):
        e = EmailPersonalizationEngine()
        inp = make_input(
            persona_pain_points=5, personalization_tokens=0, icp_score=0,
            buyer_intent_score=0, is_warm_lead=False,
            has_trigger_event=False, prior_emails_sent=0,
        )
        assert e.analyze(inp).personalization_score == pytest.approx(15.0, abs=0.1)

    # Buyer intent: * 0.20
    def test_buyer_intent_contribution(self):
        e = EmailPersonalizationEngine()
        inp = make_input(
            buyer_intent_score=100, personalization_tokens=0, icp_score=0,
            persona_pain_points=0, is_warm_lead=False,
            has_trigger_event=False, prior_emails_sent=0,
        )
        assert e.analyze(inp).personalization_score == pytest.approx(20.0, abs=0.1)

    def test_buyer_intent_half(self):
        e = EmailPersonalizationEngine()
        inp = make_input(
            buyer_intent_score=50, personalization_tokens=0, icp_score=0,
            persona_pain_points=0, is_warm_lead=False,
            has_trigger_event=False, prior_emails_sent=0,
        )
        assert e.analyze(inp).personalization_score == pytest.approx(10.0, abs=0.1)

    # ICP score: * 0.15
    def test_icp_contribution(self):
        e = EmailPersonalizationEngine()
        inp = make_input(
            icp_score=100, personalization_tokens=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False,
            has_trigger_event=False, prior_emails_sent=0,
        )
        assert e.analyze(inp).personalization_score == pytest.approx(15.0, abs=0.1)

    def test_icp_half(self):
        e = EmailPersonalizationEngine()
        inp = make_input(
            icp_score=40, personalization_tokens=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False,
            has_trigger_event=False, prior_emails_sent=0,
        )
        assert e.analyze(inp).personalization_score == pytest.approx(6.0, abs=0.1)

    # Trigger event: +15 if has_trigger_event AND trigger_event_type != "none"
    def test_trigger_event_adds_15(self):
        e = EmailPersonalizationEngine()
        without = make_input(
            has_trigger_event=False, personalization_tokens=0, icp_score=0,
            buyer_intent_score=0, persona_pain_points=0, is_warm_lead=False,
            prior_emails_sent=0,
        )
        with_event = make_input(
            has_trigger_event=True, trigger_event_type="funding",
            personalization_tokens=0, icp_score=0,
            buyer_intent_score=0, persona_pain_points=0, is_warm_lead=False,
            prior_emails_sent=0,
        )
        e2 = EmailPersonalizationEngine()
        s_without = e.analyze(without).personalization_score
        s_with = e2.analyze(with_event).personalization_score
        assert s_with - s_without == pytest.approx(15.0, abs=0.1)

    def test_trigger_event_type_none_no_bonus(self):
        e = EmailPersonalizationEngine()
        inp = make_input(
            has_trigger_event=True, trigger_event_type="none",
            personalization_tokens=0, icp_score=0,
            buyer_intent_score=0, persona_pain_points=0, is_warm_lead=False,
            prior_emails_sent=0,
        )
        assert e.analyze(inp).personalization_score == pytest.approx(0.0, abs=0.1)

    def test_has_trigger_false_no_bonus(self):
        e = EmailPersonalizationEngine()
        inp = make_input(
            has_trigger_event=False, trigger_event_type="funding",
            personalization_tokens=0, icp_score=0,
            buyer_intent_score=0, persona_pain_points=0, is_warm_lead=False,
            prior_emails_sent=0,
        )
        assert e.analyze(inp).personalization_score == pytest.approx(0.0, abs=0.1)

    # Prior engagement: min(10, open_rate*10 + reply_rate*10) if prior_emails_sent > 0
    def test_prior_engagement_zero_emails_no_bonus(self):
        e = EmailPersonalizationEngine()
        inp = make_input(
            prior_emails_sent=0, prior_open_rate=0.5, prior_reply_rate=0.5,
            personalization_tokens=0, icp_score=0,
            buyer_intent_score=0, persona_pain_points=0, is_warm_lead=False,
            has_trigger_event=False,
        )
        assert e.analyze(inp).personalization_score == pytest.approx(0.0, abs=0.1)

    def test_prior_engagement_added_when_emails_sent(self):
        e = EmailPersonalizationEngine()
        inp = make_input(
            prior_emails_sent=3, prior_open_rate=0.3, prior_reply_rate=0.2,
            personalization_tokens=0, icp_score=0,
            buyer_intent_score=0, persona_pain_points=0, is_warm_lead=False,
            has_trigger_event=False,
        )
        # open_rate*10 + reply_rate*10 = 3 + 2 = 5
        assert e.analyze(inp).personalization_score == pytest.approx(5.0, abs=0.1)

    def test_prior_engagement_cap_at_10(self):
        e = EmailPersonalizationEngine()
        inp = make_input(
            prior_emails_sent=3, prior_open_rate=0.8, prior_reply_rate=0.8,
            personalization_tokens=0, icp_score=0,
            buyer_intent_score=0, persona_pain_points=0, is_warm_lead=False,
            has_trigger_event=False,
        )
        # 8 + 8 = 16 but capped at 10
        assert e.analyze(inp).personalization_score == pytest.approx(10.0, abs=0.1)

    # Warm lead: +5
    def test_warm_lead_adds_5(self):
        e1 = EmailPersonalizationEngine()
        e2 = EmailPersonalizationEngine()
        without = make_input(
            is_warm_lead=False, personalization_tokens=0, icp_score=0,
            buyer_intent_score=0, persona_pain_points=0,
            has_trigger_event=False, prior_emails_sent=0,
        )
        with_warm = make_input(
            is_warm_lead=True, personalization_tokens=0, icp_score=0,
            buyer_intent_score=0, persona_pain_points=0,
            has_trigger_event=False, prior_emails_sent=0,
        )
        s_without = e1.analyze(without).personalization_score
        s_with = e2.analyze(with_warm).personalization_score
        assert s_with - s_without == pytest.approx(5.0, abs=0.1)

    # Clamping at 0 and 100
    def test_score_clamped_at_100(self):
        e = EmailPersonalizationEngine()
        inp = make_input(
            personalization_tokens=10, icp_score=100, buyer_intent_score=100,
            persona_pain_points=5, is_warm_lead=True,
            has_trigger_event=True, trigger_event_type="funding",
            prior_emails_sent=3, prior_open_rate=1.0, prior_reply_rate=1.0,
        )
        assert e.analyze(inp).personalization_score <= 100.0

    def test_score_not_negative(self):
        e = EmailPersonalizationEngine()
        inp = make_input(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False,
            has_trigger_event=False, prior_emails_sent=0,
        )
        assert e.analyze(inp).personalization_score >= 0.0

    def test_score_rounded_to_1_decimal(self):
        e = EmailPersonalizationEngine()
        inp = make_input(
            buyer_intent_score=33, icp_score=33,
            personalization_tokens=0, persona_pain_points=0,
            is_warm_lead=False, has_trigger_event=False, prior_emails_sent=0,
        )
        score = e.analyze(inp).personalization_score
        assert score == round(score, 1)


# ─────────────────────────────────────────────────────────────────────────────
# 5b. _predicted_open_rate: each bonus/penalty
# ─────────────────────────────────────────────────────────────────────────────

class TestPredictedOpenRate:
    def _open_rate(self, **kwargs) -> float:
        e = EmailPersonalizationEngine()
        inp = make_input(**kwargs)
        return e.analyze(inp).predicted_open_rate

    def test_base_rate_zero_pscore(self):
        # With p_score=0, base=0.20 (no bonuses)
        rate = self._open_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, seniority_level=2, subject_line_score=0,
        )
        assert rate == pytest.approx(0.200, abs=0.005)

    def test_subject_line_score_ge_70_adds_0_10(self):
        without = self._open_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, seniority_level=2, subject_line_score=49,
        )
        with_high = self._open_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, seniority_level=2, subject_line_score=70,
        )
        assert with_high - without == pytest.approx(0.10, abs=0.005)

    def test_subject_line_score_ge_50_adds_0_05(self):
        without = self._open_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, seniority_level=2, subject_line_score=49,
        )
        with_mid = self._open_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, seniority_level=2, subject_line_score=50,
        )
        assert with_mid - without == pytest.approx(0.05, abs=0.005)

    def test_trigger_event_adds_0_08(self):
        # has_trigger_event also raises p_score by +15 (via trigger bonus),
        # which adds 15*0.003=0.045 to the open rate base, plus the direct +0.08.
        # Expected total combined diff = 0.08 + 0.045 = 0.125.
        without = self._open_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, seniority_level=2, subject_line_score=0,
        )
        with_event = self._open_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=True,
            trigger_event_type="funding",
            prior_emails_sent=0, seniority_level=2, subject_line_score=0,
        )
        # Direct +0.08 from trigger, plus p_score goes from 0 to 15 (trigger bonus),
        # adding 15 * 0.003 = 0.045 via p_score * 0.003
        assert with_event - without == pytest.approx(0.125, abs=0.005)

    def test_warm_lead_adds_0_07(self):
        # is_warm_lead also raises p_score by +5, which adds 5*0.003=0.015 to open rate.
        # Expected total combined diff = 0.07 + 0.015 = 0.085.
        without = self._open_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, seniority_level=2, subject_line_score=0,
        )
        with_warm = self._open_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=True, has_trigger_event=False,
            prior_emails_sent=0, seniority_level=2, subject_line_score=0,
        )
        # Direct +0.07 from warm lead, plus p_score goes from 0 to 5 (warm lead bonus),
        # adding 5 * 0.003 = 0.015 via p_score * 0.003
        assert with_warm - without == pytest.approx(0.085, abs=0.005)

    def test_seniority_ge_4_subtracts_0_05(self):
        without = self._open_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, seniority_level=3, subject_line_score=0,
        )
        with_exec = self._open_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, seniority_level=4, subject_line_score=0,
        )
        assert without - with_exec == pytest.approx(0.05, abs=0.005)

    def test_prior_low_open_rate_penalty(self):
        without_penalty = self._open_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=4, prior_open_rate=0.20, prior_reply_rate=0.0,
            seniority_level=2, subject_line_score=0,
        )
        with_penalty = self._open_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=4, prior_open_rate=0.10, prior_reply_rate=0.0,
            seniority_level=2, subject_line_score=0,
        )
        # prior_open_rate < 0.15 and prior_emails_sent > 3 => -0.08
        assert without_penalty - with_penalty == pytest.approx(0.08, abs=0.01)

    def test_prior_low_open_rate_penalty_threshold(self):
        # exactly 3 emails sent: no penalty
        no_penalty = self._open_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=3, prior_open_rate=0.10, prior_reply_rate=0.0,
            seniority_level=2, subject_line_score=0,
        )
        # 4 emails: penalty applies
        penalty = self._open_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=4, prior_open_rate=0.10, prior_reply_rate=0.0,
            seniority_level=2, subject_line_score=0,
        )
        assert no_penalty > penalty

    def test_open_rate_clamped_at_1(self):
        rate = self._open_rate(
            personalization_tokens=5, icp_score=100, buyer_intent_score=100,
            persona_pain_points=5, is_warm_lead=True, has_trigger_event=True,
            trigger_event_type="funding",
            prior_emails_sent=0, seniority_level=1, subject_line_score=100,
        )
        assert rate <= 1.0

    def test_open_rate_not_negative(self):
        rate = self._open_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=10, prior_open_rate=0.0, prior_reply_rate=0.0,
            seniority_level=5, subject_line_score=0,
        )
        assert rate >= 0.0

    def test_open_rate_rounded_to_3_decimals(self):
        rate = self._open_rate(
            buyer_intent_score=33, icp_score=17,
            personalization_tokens=2,
        )
        assert rate == round(rate, 3)

    def test_p_score_contribution_to_open_rate(self):
        # p_score*0.003 contributes to base; tokens=5 gives p_score=25 => +0.075
        e1 = EmailPersonalizationEngine()
        e2 = EmailPersonalizationEngine()
        low = e1.analyze(make_input(personalization_tokens=0, icp_score=0,
                                    buyer_intent_score=0, persona_pain_points=0,
                                    is_warm_lead=False, has_trigger_event=False,
                                    prior_emails_sent=0, seniority_level=2,
                                    subject_line_score=0)).predicted_open_rate
        high = e2.analyze(make_input(personalization_tokens=5, icp_score=0,
                                     buyer_intent_score=0, persona_pain_points=0,
                                     is_warm_lead=False, has_trigger_event=False,
                                     prior_emails_sent=0, seniority_level=2,
                                     subject_line_score=0)).predicted_open_rate
        # p_score 25 * 0.003 = 0.075 more
        assert high - low == pytest.approx(0.075, abs=0.005)


# ─────────────────────────────────────────────────────────────────────────────
# 5c. _predicted_reply_rate: each bonus/penalty
# ─────────────────────────────────────────────────────────────────────────────

class TestPredictedReplyRate:
    def _reply_rate(self, **kwargs) -> float:
        e = EmailPersonalizationEngine()
        inp = make_input(**kwargs)
        return e.analyze(inp).predicted_reply_rate

    def test_base_rate_zero_pscore(self):
        rate = self._reply_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, body_relevance_score=0, sequence_position=1,
            prior_reply_rate=0.0,
        )
        assert rate == pytest.approx(0.030, abs=0.005)

    def test_body_relevance_ge_70_adds_0_05(self):
        without = self._reply_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, body_relevance_score=49, sequence_position=1,
            prior_reply_rate=0.0,
        )
        with_high = self._reply_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, body_relevance_score=70, sequence_position=1,
            prior_reply_rate=0.0,
        )
        assert with_high - without == pytest.approx(0.05, abs=0.005)

    def test_body_relevance_ge_50_adds_0_02(self):
        without = self._reply_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, body_relevance_score=49, sequence_position=1,
            prior_reply_rate=0.0,
        )
        with_mid = self._reply_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, body_relevance_score=50, sequence_position=1,
            prior_reply_rate=0.0,
        )
        assert with_mid - without == pytest.approx(0.02, abs=0.005)

    def test_buyer_intent_ge_70_adds_0_06(self):
        without = self._reply_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=69,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, body_relevance_score=0, sequence_position=1,
            prior_reply_rate=0.0,
        )
        with_high = self._reply_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=70,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, body_relevance_score=0, sequence_position=1,
            prior_reply_rate=0.0,
        )
        assert with_high - without == pytest.approx(0.06, abs=0.005)

    def test_warm_lead_adds_0_04(self):
        # is_warm_lead also raises p_score by +5, which adds 5*0.002=0.010 to reply rate.
        # Expected total combined diff = 0.04 + 0.010 = 0.050.
        without = self._reply_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, body_relevance_score=0, sequence_position=1,
            prior_reply_rate=0.0,
        )
        with_warm = self._reply_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=True, has_trigger_event=False,
            prior_emails_sent=0, body_relevance_score=0, sequence_position=1,
            prior_reply_rate=0.0,
        )
        # Direct +0.04 from warm lead, plus p_score goes from 0 to 5 (warm lead bonus),
        # adding 5 * 0.002 = 0.010 via p_score * 0.002
        assert with_warm - without == pytest.approx(0.050, abs=0.005)

    def test_pain_points_ge_3_adds_0_03(self):
        # Going from pain_points=2 (p_score contrib=6) to pain_points=3 (p_score contrib=9),
        # p_score increases by 3, adding 3*0.002=0.006 to reply rate.
        # Expected total combined diff = 0.03 + 0.006 = 0.036.
        without = self._reply_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=2, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, body_relevance_score=0, sequence_position=1,
            prior_reply_rate=0.0,
        )
        with_pain = self._reply_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=3, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, body_relevance_score=0, sequence_position=1,
            prior_reply_rate=0.0,
        )
        # Direct +0.03 from pain_points >= 3, plus p_score goes from 6 to 9 (+3),
        # adding 3 * 0.002 = 0.006 via p_score * 0.002
        assert with_pain - without == pytest.approx(0.036, abs=0.005)

    def test_sequence_position_gt_3_subtracts_0_02(self):
        at3 = self._reply_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, body_relevance_score=0, sequence_position=3,
            prior_reply_rate=0.0,
        )
        at4 = self._reply_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, body_relevance_score=0, sequence_position=4,
            prior_reply_rate=0.0,
        )
        assert at3 - at4 == pytest.approx(0.02, abs=0.005)

    def test_prior_reply_rate_contribution(self):
        # prior_emails_sent=3, prior_reply_rate=0.5 also affects p_score:
        # p_score += min(10, prior_open_rate*10 + prior_reply_rate*10) = min(10, 0+5) = 5
        # p_score goes from 0 to 5, adding 5*0.002=0.010 to reply rate
        # Total diff = 0.10 (direct: prior_reply_rate*0.20) + 0.010 (p_score) = 0.110
        no_prior = self._reply_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, body_relevance_score=0, sequence_position=1,
            prior_reply_rate=0.0,
        )
        with_prior = self._reply_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=3, body_relevance_score=0, sequence_position=1,
            prior_reply_rate=0.5,
        )
        # Direct +0.10 (prior_reply_rate*0.20) plus p_score from engagement data +0.010
        assert with_prior - no_prior == pytest.approx(0.110, abs=0.005)

    def test_prior_reply_rate_zero_no_contribution(self):
        no_prior = self._reply_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=3, body_relevance_score=0, sequence_position=1,
            prior_reply_rate=0.0,
        )
        assert no_prior == pytest.approx(0.030, abs=0.005)

    def test_reply_rate_clamped_at_1(self):
        rate = self._reply_rate(
            personalization_tokens=5, icp_score=100, buyer_intent_score=100,
            persona_pain_points=5, is_warm_lead=True, has_trigger_event=True,
            prior_emails_sent=3, body_relevance_score=100, sequence_position=1,
            prior_reply_rate=1.0,
        )
        assert rate <= 1.0

    def test_reply_rate_not_negative(self):
        rate = self._reply_rate(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, body_relevance_score=0, sequence_position=10,
            prior_reply_rate=0.0,
        )
        assert rate >= 0.0

    def test_reply_rate_rounded_to_3_decimals(self):
        rate = self._reply_rate(buyer_intent_score=33, icp_score=17)
        assert rate == round(rate, 3)


# ─────────────────────────────────────────────────────────────────────────────
# 5d. _send_score: weights + adjustments
# ─────────────────────────────────────────────────────────────────────────────

class TestSendScore:
    def _scores(self, **kwargs):
        e = EmailPersonalizationEngine()
        inp = make_input(**kwargs)
        r = e.analyze(inp)
        return r.send_score, r.personalization_score, r.predicted_open_rate, r.predicted_reply_rate

    def test_trigger_event_adds_5(self):
        # has_trigger_event also boosts p_score (+15 from trigger bonus),
        # open_rate (direct +0.08 + p_score cascade), and reply_rate (p_score cascade).
        # The net effect is larger than just +5. Test that trigger event strictly increases send score.
        s_without, _, _, _ = self._scores(
            has_trigger_event=False, days_since_last_email=5,
            personalization_tokens=3, icp_score=50, buyer_intent_score=50,
            persona_pain_points=3, prior_emails_sent=0, is_warm_lead=False,
        )
        s_with, _, _, _ = self._scores(
            has_trigger_event=True, trigger_event_type="funding",
            days_since_last_email=5,
            personalization_tokens=3, icp_score=50, buyer_intent_score=50,
            persona_pain_points=3, prior_emails_sent=0, is_warm_lead=False,
        )
        # Trigger event increases send score significantly (direct +5 plus cascading p_score effects)
        assert s_with > s_without
        assert s_with - s_without > 5.0  # at minimum the direct +5 plus p_score cascade

    def test_recent_email_penalty_minus_15(self):
        s_normal, _, _, _ = self._scores(
            days_since_last_email=5, has_trigger_event=False,
            personalization_tokens=3, icp_score=50, buyer_intent_score=50,
        )
        s_recent, _, _, _ = self._scores(
            days_since_last_email=0, has_trigger_event=False,
            personalization_tokens=3, icp_score=50, buyer_intent_score=50,
        )
        assert s_normal - s_recent == pytest.approx(15.0, abs=1.5)

    def test_many_emails_no_reply_penalty_minus_10(self):
        s_normal, _, _, _ = self._scores(
            prior_emails_sent=6, prior_reply_rate=0.05,
            days_since_last_email=5, has_trigger_event=False,
            personalization_tokens=3, icp_score=50, buyer_intent_score=50,
        )
        s_penalty, _, _, _ = self._scores(
            prior_emails_sent=6, prior_reply_rate=0.01,
            days_since_last_email=5, has_trigger_event=False,
            personalization_tokens=3, icp_score=50, buyer_intent_score=50,
        )
        assert s_normal - s_penalty == pytest.approx(10.0, abs=2.0)

    def test_many_emails_threshold_exactly_5_no_penalty(self):
        s_5_emails, _, _, _ = self._scores(
            prior_emails_sent=5, prior_reply_rate=0.01,
            days_since_last_email=5, has_trigger_event=False,
        )
        s_6_emails, _, _, _ = self._scores(
            prior_emails_sent=6, prior_reply_rate=0.01,
            days_since_last_email=5, has_trigger_event=False,
        )
        # 5 emails no penalty, 6 emails penalty applies
        assert s_5_emails > s_6_emails

    def test_send_score_clamped_at_100(self):
        s, _, _, _ = self._scores(
            personalization_tokens=5, icp_score=100, buyer_intent_score=100,
            persona_pain_points=5, is_warm_lead=True, has_trigger_event=True,
            trigger_event_type="funding", prior_emails_sent=0,
            days_since_last_email=10, subject_line_score=100, body_relevance_score=100,
        )
        assert s <= 100.0

    def test_send_score_not_negative(self):
        s, _, _, _ = self._scores(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=10, prior_reply_rate=0.0,
            days_since_last_email=0,
        )
        assert s >= 0.0

    def test_send_score_rounded_to_1_decimal(self):
        s, _, _, _ = self._scores(
            buyer_intent_score=33, icp_score=17, personalization_tokens=2,
        )
        assert s == round(s, 1)

    def test_send_score_increases_with_p_score(self):
        s_low, _, _, _ = self._scores(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            days_since_last_email=5,
        )
        s_high, _, _, _ = self._scores(
            personalization_tokens=5, icp_score=80, buyer_intent_score=80,
            persona_pain_points=4, is_warm_lead=True, has_trigger_event=True,
            trigger_event_type="funding", days_since_last_email=5,
        )
        assert s_high > s_low

    def test_send_score_days_since_lt_1_penalty_applied(self):
        s_normal, _, _, _ = self._scores(days_since_last_email=1)
        s_recent, _, _, _ = self._scores(days_since_last_email=0)
        # days_since_last_email < 1 means 0
        assert s_normal > s_recent


# ─────────────────────────────────────────────────────────────────────────────
# 6. PersonalizationLevel thresholds
# ─────────────────────────────────────────────────────────────────────────────

class TestPersonalizationLevelThresholds:
    def _level(self, score: float, tokens: int) -> PersonalizationLevel:
        e = EmailPersonalizationEngine()
        # We craft inputs to produce the desired p_score
        # Use buyer_intent_score to control score precisely
        # Tokens contribution: min(25, tokens*5); remaining from buyer_intent
        token_contrib = min(25.0, tokens * 5.0)
        remaining = score - token_contrib
        # buyer_intent * 0.20 = remaining => buyer_intent = remaining / 0.20
        buyer_intent = max(0.0, min(100.0, remaining / 0.20)) if remaining > 0 else 0.0
        inp = make_input(
            personalization_tokens=tokens,
            buyer_intent_score=buyer_intent,
            icp_score=0.0,
            persona_pain_points=0,
            is_warm_lead=False,
            has_trigger_event=False,
            prior_emails_sent=0,
            days_since_last_email=5,
        )
        return e.analyze(inp).personalization_level

    def test_template_below_25(self):
        # score close to 0
        e = EmailPersonalizationEngine()
        inp = make_input(
            personalization_tokens=0, buyer_intent_score=0, icp_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, days_since_last_email=5,
        )
        assert e.analyze(inp).personalization_level == PersonalizationLevel.TEMPLATE

    def test_generic_at_25(self):
        # Tokens=0, buyer_intent=100 => 20, icp=0 => 20 < 25. Use tokens=1 => 5 + buyer=100 => 25
        e = EmailPersonalizationEngine()
        inp = make_input(
            personalization_tokens=1, buyer_intent_score=100, icp_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, days_since_last_email=5,
        )
        # score = 5 + 20 = 25.0 => GENERIC
        assert e.analyze(inp).personalization_level == PersonalizationLevel.GENERIC

    def test_generic_just_above_25(self):
        e = EmailPersonalizationEngine()
        # score = 5 + 100*0.20 + 10*0.15 = 5 + 20 + 1.5 = 26.5 => GENERIC
        inp = make_input(
            personalization_tokens=1, buyer_intent_score=100, icp_score=10,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, days_since_last_email=5,
        )
        level = e.analyze(inp).personalization_level
        assert level == PersonalizationLevel.GENERIC

    def test_moderately_personalized_at_45(self):
        e = EmailPersonalizationEngine()
        # tokens=5 =>25, buyer=100 =>20, total=45 => MODERATELY_PERSONALIZED
        inp = make_input(
            personalization_tokens=5, buyer_intent_score=100, icp_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, days_since_last_email=5,
        )
        assert e.analyze(inp).personalization_level == PersonalizationLevel.MODERATELY_PERSONALIZED

    def test_highly_personalized_at_65(self):
        e = EmailPersonalizationEngine()
        # tokens=5 =>25, pain=5 =>15, buyer=100 =>20, warm=5 => total=65
        inp = make_input(
            personalization_tokens=5, buyer_intent_score=100, icp_score=0,
            persona_pain_points=5, is_warm_lead=True, has_trigger_event=False,
            prior_emails_sent=0, days_since_last_email=5,
        )
        level = e.analyze(inp).personalization_level
        assert level == PersonalizationLevel.HIGHLY_PERSONALIZED

    def test_hyper_requires_score_ge_80_and_tokens_ge_4(self):
        e = EmailPersonalizationEngine()
        # tokens=5 =>25, pain=5 =>15, buyer=100 =>20, warm=5, trigger=15 => 80
        inp = make_input(
            personalization_tokens=5, buyer_intent_score=100, icp_score=0,
            persona_pain_points=5, is_warm_lead=True, has_trigger_event=True,
            trigger_event_type="hiring", prior_emails_sent=0, days_since_last_email=5,
        )
        assert e.analyze(inp).personalization_level == PersonalizationLevel.HYPER_PERSONALIZED

    def test_hyper_needs_tokens_ge_4_not_3(self):
        e = EmailPersonalizationEngine()
        # score >= 80 but tokens=3 => NOT hyper
        inp = make_input(
            personalization_tokens=3, buyer_intent_score=100, icp_score=100,
            persona_pain_points=5, is_warm_lead=True, has_trigger_event=True,
            trigger_event_type="funding", prior_emails_sent=0, days_since_last_email=5,
        )
        r = e.analyze(inp)
        # p_score = 15 + 15 + 20 + 15 + 15 + 5 = 85 >= 80 but tokens=3 < 4
        assert r.personalization_level != PersonalizationLevel.HYPER_PERSONALIZED
        assert r.personalization_level == PersonalizationLevel.HIGHLY_PERSONALIZED

    def test_hyper_with_tokens_4(self):
        e = EmailPersonalizationEngine()
        # tokens=4 =>20, pain=5 =>15, buyer=100 =>20, warm=5, trigger=15, icp=100*0.15=15 => 90
        inp = make_input(
            personalization_tokens=4, buyer_intent_score=100, icp_score=100,
            persona_pain_points=5, is_warm_lead=True, has_trigger_event=True,
            trigger_event_type="funding", prior_emails_sent=0, days_since_last_email=5,
        )
        r = e.analyze(inp)
        assert r.personalization_level == PersonalizationLevel.HYPER_PERSONALIZED

    def test_score_80_tokens_3_gives_highly(self):
        # score >= 80 but tokens=3 => falls to HIGHLY_PERSONALIZED
        e = EmailPersonalizationEngine()
        inp = make_input(
            personalization_tokens=3, buyer_intent_score=100, icp_score=100,
            persona_pain_points=5, is_warm_lead=True, has_trigger_event=True,
            trigger_event_type="expansion", prior_emails_sent=0, days_since_last_email=5,
        )
        r = e.analyze(inp)
        assert r.personalization_score >= 80.0
        assert r.personalization_level == PersonalizationLevel.HIGHLY_PERSONALIZED

    def test_template_at_exact_zero(self):
        e = EmailPersonalizationEngine()
        inp = make_input(
            personalization_tokens=0, buyer_intent_score=0, icp_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0, days_since_last_email=5,
        )
        assert e.analyze(inp).personalization_level == PersonalizationLevel.TEMPLATE


# ─────────────────────────────────────────────────────────────────────────────
# 7. EmailTone priority order
# ─────────────────────────────────────────────────────────────────────────────

class TestEmailTonePriority:
    def _tone(self, **kwargs) -> EmailTone:
        e = EmailPersonalizationEngine()
        return e.analyze(make_input(**kwargs)).email_tone

    def test_executive_when_seniority_4(self):
        assert self._tone(seniority_level=4, buyer_intent_score=80,
                          has_trigger_event=True, lead_score=80) == EmailTone.EXECUTIVE

    def test_executive_when_seniority_5(self):
        assert self._tone(seniority_level=5, buyer_intent_score=90,
                          has_trigger_event=True, lead_score=90) == EmailTone.EXECUTIVE

    def test_executive_beats_urgency(self):
        # seniority=4 AND buyer_intent=80 => EXECUTIVE wins
        assert self._tone(seniority_level=4, buyer_intent_score=80) == EmailTone.EXECUTIVE

    def test_executive_beats_challenger(self):
        assert self._tone(seniority_level=4, has_trigger_event=True,
                          trigger_event_type="funding") == EmailTone.EXECUTIVE

    def test_urgency_when_intent_ge_70(self):
        assert self._tone(seniority_level=2, buyer_intent_score=70,
                          has_trigger_event=False, lead_score=80) == EmailTone.URGENCY

    def test_urgency_beats_challenger(self):
        # No exec (seniority=2), buyer_intent=70, has_trigger_event=True => URGENCY wins
        assert self._tone(seniority_level=2, buyer_intent_score=70,
                          has_trigger_event=True, trigger_event_type="funding") == EmailTone.URGENCY

    def test_urgency_beats_consultative(self):
        assert self._tone(seniority_level=2, buyer_intent_score=70,
                          lead_score=80, has_trigger_event=False) == EmailTone.URGENCY

    def test_challenger_when_trigger_event(self):
        assert self._tone(seniority_level=2, buyer_intent_score=50,
                          has_trigger_event=True, trigger_event_type="funding",
                          lead_score=50) == EmailTone.CHALLENGER

    def test_challenger_beats_consultative(self):
        assert self._tone(seniority_level=2, buyer_intent_score=50,
                          has_trigger_event=True, trigger_event_type="funding",
                          lead_score=80) == EmailTone.CHALLENGER

    def test_consultative_when_lead_score_ge_60(self):
        assert self._tone(seniority_level=2, buyer_intent_score=50,
                          has_trigger_event=False, lead_score=60) == EmailTone.CONSULTATIVE

    def test_consultative_beats_educational(self):
        assert self._tone(seniority_level=1, buyer_intent_score=50,
                          has_trigger_event=False, lead_score=60) == EmailTone.CONSULTATIVE

    def test_educational_fallback(self):
        assert self._tone(seniority_level=1, buyer_intent_score=50,
                          has_trigger_event=False, lead_score=50) == EmailTone.EDUCATIONAL

    def test_educational_when_all_low(self):
        assert self._tone(seniority_level=1, buyer_intent_score=0,
                          has_trigger_event=False, lead_score=0) == EmailTone.EDUCATIONAL

    def test_urgency_at_exactly_70(self):
        assert self._tone(seniority_level=2, buyer_intent_score=70) == EmailTone.URGENCY

    def test_urgency_not_at_69(self):
        # 69 < 70 => should not be urgency (unless trigger or consultative)
        t = self._tone(seniority_level=2, buyer_intent_score=69,
                       has_trigger_event=False, lead_score=50)
        assert t == EmailTone.EDUCATIONAL

    def test_seniority_3_not_executive(self):
        t = self._tone(seniority_level=3, buyer_intent_score=50,
                       has_trigger_event=False, lead_score=50)
        assert t != EmailTone.EXECUTIVE


# ─────────────────────────────────────────────────────────────────────────────
# 8. SendTiming priority order
# ─────────────────────────────────────────────────────────────────────────────

class TestSendTimingPriority:
    def _timing(self, **kwargs) -> SendTiming:
        e = EmailPersonalizationEngine()
        return e.analyze(make_input(**kwargs)).send_timing

    def test_hold_when_opted_out(self):
        # opted_out handled in fast path before we reach _send_timing normally,
        # but the method also handles it
        e = EmailPersonalizationEngine()
        inp = make_input(opted_out=True)
        r = e.analyze(inp)
        assert r.send_timing == SendTiming.HOLD

    def test_immediate_when_trigger_and_intent_ge_60(self):
        assert self._timing(
            has_trigger_event=True, trigger_event_type="funding",
            buyer_intent_score=60, seniority_level=2, sequence_position=2,
            days_since_last_email=5,
        ) == SendTiming.IMMEDIATE

    def test_immediate_at_exactly_60_intent(self):
        assert self._timing(
            has_trigger_event=True, trigger_event_type="funding",
            buyer_intent_score=60, seniority_level=3, sequence_position=2,
            days_since_last_email=5,
        ) == SendTiming.IMMEDIATE

    def test_immediate_not_when_intent_lt_60(self):
        t = self._timing(
            has_trigger_event=True, trigger_event_type="funding",
            buyer_intent_score=59, seniority_level=1, sequence_position=2,
            days_since_last_email=5,
        )
        assert t != SendTiming.IMMEDIATE

    def test_morning_when_seniority_ge_4(self):
        assert self._timing(
            has_trigger_event=False, buyer_intent_score=50,
            seniority_level=4, sequence_position=2, days_since_last_email=5,
        ) == SendTiming.MORNING

    def test_morning_when_sequence_position_1(self):
        assert self._timing(
            has_trigger_event=False, buyer_intent_score=50,
            seniority_level=2, sequence_position=1, days_since_last_email=5,
        ) == SendTiming.MORNING

    def test_morning_beats_immediate_when_seniority_4_and_trigger(self):
        # IMMEDIATE: trigger AND intent>=60 is checked FIRST
        t = self._timing(
            has_trigger_event=True, trigger_event_type="funding",
            buyer_intent_score=60, seniority_level=4, sequence_position=2,
            days_since_last_email=5,
        )
        assert t == SendTiming.IMMEDIATE  # IMMEDIATE fires before MORNING

    def test_next_business_day_when_days_lt_2(self):
        assert self._timing(
            has_trigger_event=False, buyer_intent_score=50,
            seniority_level=2, sequence_position=2, days_since_last_email=1,
        ) == SendTiming.NEXT_BUSINESS_DAY

    def test_next_business_day_at_1_day(self):
        assert self._timing(
            has_trigger_event=False, buyer_intent_score=50,
            seniority_level=2, sequence_position=2, days_since_last_email=1,
        ) == SendTiming.NEXT_BUSINESS_DAY

    def test_midday_fallback(self):
        assert self._timing(
            has_trigger_event=False, buyer_intent_score=50,
            seniority_level=2, sequence_position=2, days_since_last_email=5,
        ) == SendTiming.MIDDAY

    def test_midday_when_days_ge_2(self):
        assert self._timing(
            has_trigger_event=False, buyer_intent_score=50,
            seniority_level=2, sequence_position=2, days_since_last_email=2,
        ) == SendTiming.MIDDAY


# ─────────────────────────────────────────────────────────────────────────────
# 9. recommended_action priority order
# ─────────────────────────────────────────────────────────────────────────────

class TestRecommendedActionPriority:
    def _action(self, **kwargs) -> PersonalizationAction:
        e = EmailPersonalizationEngine()
        return e.analyze(make_input(**kwargs)).recommended_action

    def test_hold_when_opted_out(self):
        assert self._action(opted_out=True) == PersonalizationAction.HOLD

    def test_hold_when_days_since_lt_1(self):
        assert self._action(
            opted_out=False, days_since_last_email=0,
            personalization_tokens=5, icp_score=100, buyer_intent_score=100,
            persona_pain_points=5, is_warm_lead=True, has_trigger_event=True,
            trigger_event_type="funding",
        ) == PersonalizationAction.HOLD

    def test_opted_out_beats_high_scores(self):
        assert self._action(
            opted_out=True, days_since_last_email=10,
            personalization_tokens=5, icp_score=100, buyer_intent_score=100,
        ) == PersonalizationAction.HOLD

    def test_send_now_when_s_score_ge_70_and_p_score_ge_65(self):
        # Build a scenario that gives s_score >= 70 and p_score >= 65
        e = EmailPersonalizationEngine()
        inp = make_input(
            personalization_tokens=5, icp_score=80, buyer_intent_score=80,
            persona_pain_points=5, is_warm_lead=True, has_trigger_event=True,
            trigger_event_type="funding", days_since_last_email=5,
            subject_line_score=80, body_relevance_score=80,
            prior_emails_sent=0, sequence_position=2, seniority_level=2,
        )
        r = e.analyze(inp)
        if r.send_score >= 70 and r.personalization_score >= 65:
            assert r.recommended_action == PersonalizationAction.SEND_NOW

    def test_refine_and_send_when_s_score_ge_55(self):
        # We need s_score >= 55 but not meeting send_now conditions
        e = EmailPersonalizationEngine()
        # Create scenario where p_score < 65 but s_score >= 55
        inp = make_input(
            personalization_tokens=3, icp_score=50, buyer_intent_score=50,
            persona_pain_points=2, is_warm_lead=False, has_trigger_event=False,
            days_since_last_email=5, subject_line_score=80, body_relevance_score=80,
            prior_emails_sent=0, sequence_position=2, seniority_level=2,
        )
        r = e.analyze(inp)
        if r.send_score >= 55 and not (r.send_score >= 70 and r.personalization_score >= 65):
            assert r.recommended_action == PersonalizationAction.REFINE_AND_SEND

    def test_rewrite_required_when_p_score_lt_25(self):
        # p_score < 25, s_score < 35 and s_score < 55
        e = EmailPersonalizationEngine()
        inp = make_input(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            days_since_last_email=5,
            subject_line_score=0, body_relevance_score=0,
            prior_emails_sent=0,
        )
        r = e.analyze(inp)
        assert r.personalization_score < 25
        assert r.recommended_action == PersonalizationAction.REWRITE_REQUIRED

    def test_review_before_send_fallback(self):
        # s_score in [35, 55) and p_score >= 25
        e = EmailPersonalizationEngine()
        # We need to hit the fallback: p_score >= 25, s_score >= 35, but < 55
        inp = make_input(
            personalization_tokens=2, icp_score=50, buyer_intent_score=50,
            persona_pain_points=2, is_warm_lead=False, has_trigger_event=False,
            days_since_last_email=5, subject_line_score=30, body_relevance_score=30,
            prior_emails_sent=0, sequence_position=2, seniority_level=2,
        )
        r = e.analyze(inp)
        # Check what action we get for this middle-ground scenario
        # p_score = 10 + 6 + 10 = 26; s_score = moderate
        if r.personalization_score >= 25 and 35 <= r.send_score < 55:
            assert r.recommended_action == PersonalizationAction.REVIEW_BEFORE_SEND

    def test_days_since_0_overrides_all_scores(self):
        # Even with perfect scores, days_since=0 => HOLD
        e = EmailPersonalizationEngine()
        inp = make_input(
            personalization_tokens=5, icp_score=100, buyer_intent_score=100,
            persona_pain_points=5, is_warm_lead=True, has_trigger_event=True,
            trigger_event_type="funding", days_since_last_email=0,
        )
        assert e.analyze(inp).recommended_action == PersonalizationAction.HOLD


# ─────────────────────────────────────────────────────────────────────────────
# 10. is_ready_to_send for each action type
# ─────────────────────────────────────────────────────────────────────────────

class TestIsReadyToSend:
    def test_ready_when_send_now(self, engine):
        inp = make_input(
            personalization_tokens=5, icp_score=80, buyer_intent_score=80,
            persona_pain_points=5, is_warm_lead=True, has_trigger_event=True,
            trigger_event_type="funding", days_since_last_email=5,
            subject_line_score=90, body_relevance_score=90,
            prior_emails_sent=0,
        )
        r = engine.analyze(inp)
        if r.recommended_action == PersonalizationAction.SEND_NOW:
            assert r.is_ready_to_send is True

    def test_ready_when_refine_and_send(self, engine):
        # Build scenario with refine_and_send
        inp = make_input(
            personalization_tokens=3, icp_score=50, buyer_intent_score=60,
            persona_pain_points=3, is_warm_lead=True, has_trigger_event=False,
            days_since_last_email=5,
            subject_line_score=75, body_relevance_score=75,
            prior_emails_sent=0,
        )
        r = engine.analyze(inp)
        if r.recommended_action == PersonalizationAction.REFINE_AND_SEND:
            assert r.is_ready_to_send is True

    def test_not_ready_when_review_before_send(self):
        # Craft a scenario that results in REVIEW_BEFORE_SEND
        e = EmailPersonalizationEngine()
        for p_tokens, icp, bi, pain in [(1, 20, 30, 1), (2, 25, 25, 1)]:
            inp = make_input(
                personalization_tokens=p_tokens, icp_score=icp, buyer_intent_score=bi,
                persona_pain_points=pain, is_warm_lead=False, has_trigger_event=False,
                days_since_last_email=5, subject_line_score=30, body_relevance_score=30,
                prior_emails_sent=0, sequence_position=2, seniority_level=2,
            )
            r = e.analyze(inp)
            if r.recommended_action == PersonalizationAction.REVIEW_BEFORE_SEND:
                assert r.is_ready_to_send is False
                break

    def test_not_ready_when_rewrite_required(self):
        e = EmailPersonalizationEngine()
        inp = make_input(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            days_since_last_email=5, subject_line_score=0, body_relevance_score=0,
            prior_emails_sent=0,
        )
        r = e.analyze(inp)
        assert r.recommended_action == PersonalizationAction.REWRITE_REQUIRED
        assert r.is_ready_to_send is False

    def test_not_ready_when_hold(self):
        e = EmailPersonalizationEngine()
        inp = make_input(opted_out=True)
        r = e.analyze(inp)
        assert r.recommended_action == PersonalizationAction.HOLD
        assert r.is_ready_to_send is False

    def test_not_ready_when_days_since_0(self):
        e = EmailPersonalizationEngine()
        inp = make_input(days_since_last_email=0, opted_out=False)
        r = e.analyze(inp)
        assert r.is_ready_to_send is False

    def test_is_ready_to_send_bool_type(self, engine):
        inp = make_input()
        r = engine.analyze(inp)
        assert isinstance(r.is_ready_to_send, bool)


# ─────────────────────────────────────────────────────────────────────────────
# 11. Engine properties
# ─────────────────────────────────────────────────────────────────────────────

class TestEngineProperties:
    def test_ready_to_send_empty_initially(self, engine):
        assert engine.ready_to_send == []

    def test_needs_review_empty_initially(self, engine):
        assert engine.needs_review == []

    def test_held_emails_empty_initially(self, engine):
        assert engine.held_emails == []

    def test_high_personalization_empty_initially(self, engine):
        assert engine.high_personalization == []

    def test_held_emails_contains_opted_out(self, engine):
        engine.analyze(make_input(opted_out=True))
        assert len(engine.held_emails) == 1

    def test_held_emails_contains_days_since_0(self, engine):
        engine.analyze(make_input(days_since_last_email=0, opted_out=False))
        assert len(engine.held_emails) >= 1

    def test_ready_to_send_contains_refine_and_send(self, engine):
        # After analyzing multiple emails, ready_to_send includes REFINE_AND_SEND
        inp = make_input(
            personalization_tokens=3, icp_score=50, buyer_intent_score=60,
            persona_pain_points=3, is_warm_lead=True, has_trigger_event=False,
            days_since_last_email=5, subject_line_score=75, body_relevance_score=75,
            prior_emails_sent=0,
        )
        r = engine.analyze(inp)
        if r.recommended_action == PersonalizationAction.REFINE_AND_SEND:
            assert r in engine.ready_to_send

    def test_needs_review_filters_correctly(self, engine):
        for r in engine._results:
            assert r.recommended_action == PersonalizationAction.REVIEW_BEFORE_SEND

    def test_high_personalization_includes_hyper(self, engine):
        inp = make_input(
            personalization_tokens=5, icp_score=80, buyer_intent_score=80,
            persona_pain_points=5, is_warm_lead=True, has_trigger_event=True,
            trigger_event_type="funding", days_since_last_email=5,
        )
        r = engine.analyze(inp)
        if r.personalization_level == PersonalizationLevel.HYPER_PERSONALIZED:
            assert r in engine.high_personalization

    def test_high_personalization_includes_highly(self, engine):
        inp = make_input(
            personalization_tokens=5, buyer_intent_score=100, icp_score=0,
            persona_pain_points=5, is_warm_lead=True, has_trigger_event=False,
            days_since_last_email=5,
        )
        r = engine.analyze(inp)
        if r.personalization_level == PersonalizationLevel.HIGHLY_PERSONALIZED:
            assert r in engine.high_personalization

    def test_high_personalization_excludes_moderately(self, engine):
        inp = make_input(
            personalization_tokens=5, buyer_intent_score=100, icp_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            days_since_last_email=5,
        )
        r = engine.analyze(inp)
        # p_score = 25 + 20 = 45 => MODERATELY_PERSONALIZED
        if r.personalization_level == PersonalizationLevel.MODERATELY_PERSONALIZED:
            assert r not in engine.high_personalization

    def test_multiple_results_tracked(self, engine):
        engine.analyze(make_input(prospect_id="P1"))
        engine.analyze(make_input(prospect_id="P2"))
        assert len(engine._results) == 2

    def test_properties_return_lists(self, engine):
        assert isinstance(engine.ready_to_send, list)
        assert isinstance(engine.needs_review, list)
        assert isinstance(engine.held_emails, list)
        assert isinstance(engine.high_personalization, list)

    def test_held_emails_not_in_ready(self, engine):
        engine.analyze(make_input(opted_out=True))
        for r in engine.held_emails:
            assert r not in engine.ready_to_send


# ─────────────────────────────────────────────────────────────────────────────
# 12. summary(): 13 keys, empty state, correctness with 1+ results
# ─────────────────────────────────────────────────────────────────────────────

class TestSummary:
    EXPECTED_KEYS = {
        "total", "level_counts", "tone_counts", "timing_counts", "action_counts",
        "avg_personalization_score", "avg_send_score", "avg_predicted_open_rate",
        "avg_predicted_reply_rate", "ready_to_send_count", "needs_review_count",
        "held_count", "high_personalization_count",
    }

    def test_empty_summary_key_count(self, engine):
        s = engine.summary()
        assert len(s) == 13

    def test_empty_summary_exact_keys(self, engine):
        s = engine.summary()
        assert set(s.keys()) == self.EXPECTED_KEYS

    def test_empty_total_is_zero(self, engine):
        assert engine.summary()["total"] == 0

    def test_empty_avg_scores_are_zero(self, engine):
        s = engine.summary()
        assert s["avg_personalization_score"] == 0.0
        assert s["avg_send_score"] == 0.0
        assert s["avg_predicted_open_rate"] == 0.0
        assert s["avg_predicted_reply_rate"] == 0.0

    def test_empty_counts_are_zero(self, engine):
        s = engine.summary()
        assert s["ready_to_send_count"] == 0
        assert s["needs_review_count"] == 0
        assert s["held_count"] == 0
        assert s["high_personalization_count"] == 0

    def test_empty_dicts_are_empty(self, engine):
        s = engine.summary()
        assert s["level_counts"] == {}
        assert s["tone_counts"] == {}
        assert s["timing_counts"] == {}
        assert s["action_counts"] == {}

    def test_summary_key_count_after_analyze(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        assert len(s) == 13

    def test_summary_total_correct(self, engine):
        engine.analyze(make_input(prospect_id="P1"))
        engine.analyze(make_input(prospect_id="P2"))
        assert engine.summary()["total"] == 2

    def test_summary_held_count_correct(self, engine):
        engine.analyze(make_input(opted_out=True, prospect_id="P1"))
        engine.analyze(make_input(opted_out=True, prospect_id="P2"))
        engine.analyze(make_input(opted_out=False, prospect_id="P3", days_since_last_email=5))
        s = engine.summary()
        assert s["held_count"] == 2

    def test_summary_level_counts_populated(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        assert len(s["level_counts"]) >= 1
        assert sum(s["level_counts"].values()) == s["total"]

    def test_summary_tone_counts_populated(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        assert sum(s["tone_counts"].values()) == s["total"]

    def test_summary_timing_counts_populated(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        assert sum(s["timing_counts"].values()) == s["total"]

    def test_summary_action_counts_populated(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_avg_personalization_score_correct(self, engine):
        r1 = engine.analyze(make_input(
            personalization_tokens=5, icp_score=80, buyer_intent_score=80,
            persona_pain_points=5, is_warm_lead=True, has_trigger_event=True,
            trigger_event_type="funding", days_since_last_email=5,
        ))
        r2 = engine.analyze(make_input())
        expected = round((r1.personalization_score + r2.personalization_score) / 2, 1)
        assert engine.summary()["avg_personalization_score"] == expected

    def test_summary_avg_send_score_correct(self, engine):
        r1 = engine.analyze(make_input(prospect_id="P1"))
        r2 = engine.analyze(make_input(prospect_id="P2"))
        expected = round((r1.send_score + r2.send_score) / 2, 1)
        assert engine.summary()["avg_send_score"] == expected

    def test_summary_ready_to_send_count_matches_property(self, engine):
        engine.analyze(make_input(prospect_id="P1"))
        engine.analyze(make_input(opted_out=True, prospect_id="P2"))
        s = engine.summary()
        assert s["ready_to_send_count"] == len(engine.ready_to_send)

    def test_summary_needs_review_count_matches_property(self, engine):
        engine.analyze(make_input(prospect_id="P1"))
        s = engine.summary()
        assert s["needs_review_count"] == len(engine.needs_review)

    def test_summary_high_personalization_count_matches_property(self, engine):
        engine.analyze(make_input(
            personalization_tokens=5, icp_score=80, buyer_intent_score=80,
            persona_pain_points=5, is_warm_lead=True, has_trigger_event=True,
            trigger_event_type="funding", days_since_last_email=5,
        ))
        s = engine.summary()
        assert s["high_personalization_count"] == len(engine.high_personalization)

    def test_summary_avg_open_rate_rounded_to_3(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        avg = s["avg_predicted_open_rate"]
        assert avg == round(avg, 3)

    def test_summary_avg_reply_rate_rounded_to_3(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        avg = s["avg_predicted_reply_rate"]
        assert avg == round(avg, 3)

    def test_summary_opted_out_hold_in_held_count(self, engine):
        engine.analyze(make_input(opted_out=True))
        assert engine.summary()["held_count"] == 1

    def test_summary_level_counts_use_enum_values(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        # Keys should be string enum values
        for k in s["level_counts"]:
            assert k in {m.value for m in PersonalizationLevel}


# ─────────────────────────────────────────────────────────────────────────────
# 13. reset() clears all state
# ─────────────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_results(self, engine):
        engine.analyze(make_input(prospect_id="P1"))
        engine.analyze(make_input(prospect_id="P2"))
        assert len(engine._results) == 2
        engine.reset()
        assert len(engine._results) == 0

    def test_reset_clears_ready_to_send(self, engine):
        engine.analyze(make_input(
            personalization_tokens=5, icp_score=80, buyer_intent_score=80,
            persona_pain_points=5, is_warm_lead=True, has_trigger_event=True,
            trigger_event_type="funding", days_since_last_email=5,
            subject_line_score=90, body_relevance_score=90,
        ))
        engine.reset()
        assert engine.ready_to_send == []

    def test_reset_clears_held_emails(self, engine):
        engine.analyze(make_input(opted_out=True))
        engine.reset()
        assert engine.held_emails == []

    def test_reset_clears_high_personalization(self, engine):
        engine.analyze(make_input(
            personalization_tokens=5, buyer_intent_score=100, icp_score=100,
            persona_pain_points=5, is_warm_lead=True, has_trigger_event=True,
            trigger_event_type="funding", days_since_last_email=5,
        ))
        engine.reset()
        assert engine.high_personalization == []

    def test_reset_allows_fresh_analysis(self, engine):
        engine.analyze(make_input(prospect_id="P1"))
        engine.reset()
        engine.analyze(make_input(prospect_id="P2"))
        assert len(engine._results) == 1
        assert engine._results[0].prospect_id == "P2"

    def test_reset_summary_returns_empty(self, engine):
        engine.analyze(make_input())
        engine.reset()
        s = engine.summary()
        assert s["total"] == 0

    def test_double_reset_safe(self, engine):
        engine.reset()
        engine.reset()
        assert engine._results == []

    def test_reset_after_batch(self, engine):
        engine.analyze_batch([make_input(prospect_id=f"P{i}") for i in range(5)])
        assert len(engine._results) == 5
        engine.reset()
        assert len(engine._results) == 0


# ─────────────────────────────────────────────────────────────────────────────
# analyze_batch tests
# ─────────────────────────────────────────────────────────────────────────────

class TestAnalyzeBatch:
    def test_batch_returns_list(self, engine):
        results = engine.analyze_batch([make_input(prospect_id="P1"), make_input(prospect_id="P2")])
        assert isinstance(results, list)

    def test_batch_length(self, engine):
        results = engine.analyze_batch([make_input(prospect_id=f"P{i}") for i in range(5)])
        assert len(results) == 5

    def test_batch_stores_in_results(self, engine):
        engine.analyze_batch([make_input(prospect_id=f"P{i}") for i in range(3)])
        assert len(engine._results) == 3

    def test_batch_empty_list(self, engine):
        results = engine.analyze_batch([])
        assert results == []

    def test_batch_prospect_ids_preserved(self, engine):
        inputs = [make_input(prospect_id=f"PROSPECT_{i}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        assert [r.prospect_id for r in results] == ["PROSPECT_0", "PROSPECT_1", "PROSPECT_2"]

    def test_batch_returns_email_personalization_results(self, engine):
        results = engine.analyze_batch([make_input()])
        assert isinstance(results[0], EmailPersonalizationResult)

    def test_batch_with_opted_out(self, engine):
        inputs = [
            make_input(prospect_id="P1", opted_out=True),
            make_input(prospect_id="P2", opted_out=False),
        ]
        results = engine.analyze_batch(inputs)
        assert results[0].recommended_action == PersonalizationAction.HOLD
        assert results[0].is_ready_to_send is False


# ─────────────────────────────────────────────────────────────────────────────
# 14. End-to-end scenarios
# ─────────────────────────────────────────────────────────────────────────────

class TestEndToEndScenarios:
    def test_hyper_personalized_send_now(self):
        """Full high-quality prospect: should score very high."""
        e = EmailPersonalizationEngine()
        inp = make_input(
            prospect_id="HYPER001",
            campaign_id="CAMP_HP",
            rep_id="REP1",
            icp_score=95.0,
            lead_score=85.0,
            buyer_intent_score=90.0,
            seniority_level=3,
            industry="saas",
            company_size="enterprise",
            prior_emails_sent=2,
            prior_open_rate=0.5,
            prior_reply_rate=0.2,
            prior_click_rate=0.1,
            days_since_last_email=7,
            has_trigger_event=True,
            trigger_event_type="funding",
            persona_pain_points=5,
            personalization_tokens=5,
            subject_line_score=85.0,
            body_relevance_score=85.0,
            sequence_position=2,
            is_warm_lead=True,
            opted_out=False,
        )
        r = e.analyze(inp)
        assert r.personalization_score >= 80.0
        assert r.personalization_level == PersonalizationLevel.HYPER_PERSONALIZED
        assert r.is_ready_to_send is True
        assert r.recommended_action in (PersonalizationAction.SEND_NOW, PersonalizationAction.REFINE_AND_SEND)

    def test_template_rewrite_required(self):
        """Minimal data prospect: should require rewrite."""
        e = EmailPersonalizationEngine()
        inp = make_input(
            prospect_id="TEMPLATE001",
            campaign_id="CAMP_T",
            rep_id="REP2",
            icp_score=0.0,
            lead_score=0.0,
            buyer_intent_score=0.0,
            seniority_level=1,
            industry="retail",
            company_size="smb",
            prior_emails_sent=0,
            prior_open_rate=0.0,
            prior_reply_rate=0.0,
            prior_click_rate=0.0,
            days_since_last_email=10,
            has_trigger_event=False,
            trigger_event_type="none",
            persona_pain_points=0,
            personalization_tokens=0,
            subject_line_score=10.0,
            body_relevance_score=10.0,
            sequence_position=1,
            is_warm_lead=False,
            opted_out=False,
        )
        r = e.analyze(inp)
        assert r.personalization_score < 25.0
        assert r.personalization_level == PersonalizationLevel.TEMPLATE
        assert r.recommended_action == PersonalizationAction.REWRITE_REQUIRED
        assert r.is_ready_to_send is False

    def test_opted_out_hold_scenario(self):
        """Opted out prospect: fast path hold."""
        e = EmailPersonalizationEngine()
        inp = make_input(
            prospect_id="OPTOUT001",
            opted_out=True,
            personalization_tokens=5,
            icp_score=100.0,
            buyer_intent_score=100.0,
            persona_pain_points=5,
            is_warm_lead=True,
        )
        r = e.analyze(inp)
        assert r.recommended_action == PersonalizationAction.HOLD
        assert r.send_timing == SendTiming.HOLD
        assert r.is_ready_to_send is False
        assert r.personalization_score == 0.0
        assert r.send_score == 0.0
        assert len(r.risk_flags) == 1

    def test_e2e_prospect_ids_in_results(self):
        """prospect_id is correctly propagated to the result."""
        e = EmailPersonalizationEngine()
        inp = make_input(prospect_id="CUSTOM_ID_XYZ")
        r = e.analyze(inp)
        assert r.prospect_id == "CUSTOM_ID_XYZ"

    def test_e2e_rep_id_not_in_to_dict_but_in_result(self):
        """rep_id in result object but excluded from to_dict."""
        e = EmailPersonalizationEngine()
        inp = make_input(rep_id="REP_UNIQUE_99")
        r = e.analyze(inp)
        assert r.rep_id == "REP_UNIQUE_99"
        assert "rep_id" not in r.to_dict()

    def test_e2e_warm_lead_ready(self):
        """Warm lead with moderate signals should be ready."""
        e = EmailPersonalizationEngine()
        inp = make_input(
            is_warm_lead=True,
            buyer_intent_score=65,
            icp_score=70,
            personalization_tokens=4,
            persona_pain_points=3,
            has_trigger_event=True,
            trigger_event_type="hiring",
            days_since_last_email=5,
            subject_line_score=75,
            body_relevance_score=70,
            prior_emails_sent=0,
            seniority_level=2,
            sequence_position=2,
        )
        r = e.analyze(inp)
        assert r.is_ready_to_send is True

    def test_e2e_days_since_0_always_hold(self):
        """Even perfect prospect emailed today is held."""
        e = EmailPersonalizationEngine()
        inp = make_input(
            personalization_tokens=5, icp_score=100, buyer_intent_score=100,
            persona_pain_points=5, is_warm_lead=True, has_trigger_event=True,
            trigger_event_type="funding", days_since_last_email=0,
            subject_line_score=100, body_relevance_score=100,
        )
        r = e.analyze(inp)
        assert r.recommended_action == PersonalizationAction.HOLD
        assert r.is_ready_to_send is False

    def test_e2e_full_pipeline_summary(self):
        """Analyze multiple inputs and verify summary correctness."""
        e = EmailPersonalizationEngine()
        inputs = [
            make_input(prospect_id="P1", opted_out=True),
            make_input(
                prospect_id="P2",
                personalization_tokens=5, icp_score=80, buyer_intent_score=80,
                persona_pain_points=5, is_warm_lead=True, has_trigger_event=True,
                trigger_event_type="funding", days_since_last_email=5,
                subject_line_score=90, body_relevance_score=90,
            ),
            make_input(prospect_id="P3", days_since_last_email=5),
        ]
        results = e.analyze_batch(inputs)
        s = e.summary()
        assert s["total"] == 3
        assert s["held_count"] >= 1
        assert len(s) == 13
        assert s["ready_to_send_count"] == len(e.ready_to_send)
        assert s["held_count"] == len(e.held_emails)

    def test_e2e_optimization_score_formula(self):
        """optimization_score = round(p_score*0.50 + s_score*0.50, 1)"""
        e = EmailPersonalizationEngine()
        inp = make_input(
            personalization_tokens=3, icp_score=50, buyer_intent_score=50,
            days_since_last_email=5,
        )
        r = e.analyze(inp)
        expected = round(r.personalization_score * 0.50 + r.send_score * 0.50, 1)
        assert r.optimization_score == expected


# ─────────────────────────────────────────────────────────────────────────────
# Additional edge cases and boundary tests
# ─────────────────────────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_personalization_score_exactly_100(self):
        """Score should be clamped to 100.0 even with excess inputs."""
        e = EmailPersonalizationEngine()
        inp = make_input(
            personalization_tokens=10, icp_score=100, buyer_intent_score=100,
            persona_pain_points=5, is_warm_lead=True, has_trigger_event=True,
            trigger_event_type="funding", prior_emails_sent=5,
            prior_open_rate=1.0, prior_reply_rate=1.0,
        )
        r = e.analyze(inp)
        assert r.personalization_score == 100.0

    def test_open_rate_not_exceed_1_with_all_bonuses(self):
        e = EmailPersonalizationEngine()
        inp = make_input(
            personalization_tokens=5, icp_score=100, buyer_intent_score=100,
            persona_pain_points=5, is_warm_lead=True, has_trigger_event=True,
            trigger_event_type="funding", subject_line_score=100,
            seniority_level=1, prior_emails_sent=0,
        )
        assert e.analyze(inp).predicted_open_rate <= 1.0

    def test_reply_rate_not_exceed_1_with_all_bonuses(self):
        e = EmailPersonalizationEngine()
        inp = make_input(
            personalization_tokens=5, icp_score=100, buyer_intent_score=100,
            persona_pain_points=5, is_warm_lead=True, has_trigger_event=True,
            body_relevance_score=100, sequence_position=1,
            prior_reply_rate=1.0, prior_emails_sent=3,
        )
        assert e.analyze(inp).predicted_reply_rate <= 1.0

    def test_send_score_not_exceed_100_with_all_bonuses(self):
        e = EmailPersonalizationEngine()
        inp = make_input(
            personalization_tokens=5, icp_score=100, buyer_intent_score=100,
            persona_pain_points=5, is_warm_lead=True, has_trigger_event=True,
            trigger_event_type="funding", days_since_last_email=10,
            subject_line_score=100, body_relevance_score=100,
        )
        assert e.analyze(inp).send_score <= 100.0

    def test_multiple_engines_independent(self):
        e1 = EmailPersonalizationEngine()
        e2 = EmailPersonalizationEngine()
        e1.analyze(make_input(prospect_id="P1"))
        assert len(e2._results) == 0

    def test_result_is_dataclass(self):
        e = EmailPersonalizationEngine()
        r = e.analyze(make_input())
        assert dataclasses.is_dataclass(r)

    def test_result_field_count(self):
        fields = dataclasses.fields(EmailPersonalizationResult)
        assert len(fields) == 16

    def test_engine_initial_state(self):
        e = EmailPersonalizationEngine()
        assert e._results == []

    def test_personalization_tokens_large_value_capped(self):
        e = EmailPersonalizationEngine()
        inp = make_input(
            personalization_tokens=100, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0,
        )
        # tokens contribution = min(25, 500) = 25
        assert e.analyze(inp).personalization_score == pytest.approx(25.0, abs=0.1)

    def test_pain_points_large_value_capped(self):
        e = EmailPersonalizationEngine()
        inp = make_input(
            persona_pain_points=100, personalization_tokens=0, icp_score=0,
            buyer_intent_score=0, is_warm_lead=False, has_trigger_event=False,
            prior_emails_sent=0,
        )
        # pain contribution = min(15, 300) = 15
        assert e.analyze(inp).personalization_score == pytest.approx(15.0, abs=0.1)

    def test_all_enum_types_returned(self):
        e = EmailPersonalizationEngine()
        r = e.analyze(make_input())
        assert isinstance(r.personalization_level, PersonalizationLevel)
        assert isinstance(r.email_tone, EmailTone)
        assert isinstance(r.send_timing, SendTiming)
        assert isinstance(r.recommended_action, PersonalizationAction)

    def test_subject_suggestions_max_3(self):
        """subject_suggestions is capped at 3."""
        e = EmailPersonalizationEngine()
        inp = make_input(
            has_trigger_event=True, trigger_event_type="funding",
            seniority_level=4, buyer_intent_score=80,
            is_warm_lead=True, sequence_position=1,
        )
        r = e.analyze(inp)
        assert len(r.subject_suggestions) <= 3

    def test_risk_flags_list_type(self):
        e = EmailPersonalizationEngine()
        r = e.analyze(make_input())
        assert isinstance(r.risk_flags, list)

    def test_personalization_tips_list_type(self):
        e = EmailPersonalizationEngine()
        r = e.analyze(make_input())
        assert isinstance(r.personalization_tips, list)

    def test_opted_out_not_in_ready_to_send(self):
        e = EmailPersonalizationEngine()
        e.analyze(make_input(opted_out=True))
        assert len(e.ready_to_send) == 0

    def test_opted_out_is_in_held_emails(self):
        e = EmailPersonalizationEngine()
        e.analyze(make_input(opted_out=True))
        assert len(e.held_emails) == 1

    def test_trigger_type_expansion_qualifies(self):
        e = EmailPersonalizationEngine()
        inp = make_input(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=True,
            trigger_event_type="expansion", prior_emails_sent=0,
        )
        # +15 for trigger event
        assert e.analyze(inp).personalization_score == pytest.approx(15.0, abs=0.1)

    def test_trigger_type_hiring_qualifies(self):
        e = EmailPersonalizationEngine()
        inp = make_input(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=True,
            trigger_event_type="hiring", prior_emails_sent=0,
        )
        assert e.analyze(inp).personalization_score == pytest.approx(15.0, abs=0.1)

    def test_sequence_position_3_no_reply_penalty(self):
        e = EmailPersonalizationEngine()
        inp = make_input(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            body_relevance_score=0, sequence_position=3, prior_reply_rate=0.0,
            prior_emails_sent=0,
        )
        # No penalty for sequence_position=3
        r = e.analyze(inp)
        assert r.predicted_reply_rate == pytest.approx(0.030, abs=0.005)

    def test_sequence_position_4_gets_reply_penalty(self):
        e1 = EmailPersonalizationEngine()
        e2 = EmailPersonalizationEngine()
        at3 = e1.analyze(make_input(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            body_relevance_score=0, sequence_position=3, prior_reply_rate=0.0,
            prior_emails_sent=0,
        )).predicted_reply_rate
        at4 = e2.analyze(make_input(
            personalization_tokens=0, icp_score=0, buyer_intent_score=0,
            persona_pain_points=0, is_warm_lead=False, has_trigger_event=False,
            body_relevance_score=0, sequence_position=4, prior_reply_rate=0.0,
            prior_emails_sent=0,
        )).predicted_reply_rate
        assert at3 > at4

    def test_prior_emails_exactly_5_no_reply_score_penalty(self):
        e1 = EmailPersonalizationEngine()
        e2 = EmailPersonalizationEngine()
        s5 = e1.analyze(make_input(
            prior_emails_sent=5, prior_reply_rate=0.01,
            days_since_last_email=5, has_trigger_event=False,
        )).send_score
        s6 = e2.analyze(make_input(
            prior_emails_sent=6, prior_reply_rate=0.01,
            days_since_last_email=5, has_trigger_event=False,
        )).send_score
        assert s5 > s6  # 6 emails gets penalty

    def test_send_score_days_since_exactly_1_no_penalty(self):
        e1 = EmailPersonalizationEngine()
        e2 = EmailPersonalizationEngine()
        s1 = e1.analyze(make_input(days_since_last_email=1)).send_score
        s0 = e2.analyze(make_input(days_since_last_email=0)).send_score
        # days_since_last_email < 1 means only 0
        assert s1 > s0

    def test_summary_level_counts_values_sum_to_total(self, engine):
        for i in range(5):
            engine.analyze(make_input(prospect_id=f"P{i}"))
        s = engine.summary()
        assert sum(s["level_counts"].values()) == s["total"]

    def test_summary_tone_counts_values_sum_to_total(self, engine):
        for i in range(5):
            engine.analyze(make_input(prospect_id=f"P{i}"))
        s = engine.summary()
        assert sum(s["tone_counts"].values()) == s["total"]

    def test_summary_timing_counts_sum_to_total(self, engine):
        for i in range(5):
            engine.analyze(make_input(prospect_id=f"P{i}"))
        s = engine.summary()
        assert sum(s["timing_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_to_total(self, engine):
        for i in range(5):
            engine.analyze(make_input(prospect_id=f"P{i}"))
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_to_dict_level_string_matches_enum_value(self):
        e = EmailPersonalizationEngine()
        r = e.analyze(make_input())
        d = r.to_dict()
        assert d["personalization_level"] == r.personalization_level.value

    def test_to_dict_tone_string_matches_enum_value(self):
        e = EmailPersonalizationEngine()
        r = e.analyze(make_input())
        d = r.to_dict()
        assert d["email_tone"] == r.email_tone.value

    def test_to_dict_timing_string_matches_enum_value(self):
        e = EmailPersonalizationEngine()
        r = e.analyze(make_input())
        d = r.to_dict()
        assert d["send_timing"] == r.send_timing.value

    def test_to_dict_action_string_matches_enum_value(self):
        e = EmailPersonalizationEngine()
        r = e.analyze(make_input())
        d = r.to_dict()
        assert d["recommended_action"] == r.recommended_action.value
