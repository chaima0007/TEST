import pytest
from swarm.intelligence.meeting_intelligence_engine import (
    MeetingOutcome,
    MeetingQuality,
    BuyingSignalStrength,
    FollowUpUrgency,
    MeetingInput,
    MeetingResult,
    MeetingIntelligenceEngine,
)


# ─── Fixtures ────────────────────────────────────────────────────────────────

def make_input(**overrides) -> MeetingInput:
    defaults = dict(
        meeting_id="m1",
        deal_id="d1",
        rep_id="r1",
        rep_name="Alice",
        account_name="Acme Corp",
        meeting_type="demo",
        duration_minutes=60,
        attendees_count=3,
        decision_maker_present=True,
        exec_sponsor_present=False,
        prospect_asked_questions=True,
        prospect_requested_pricing=False,
        prospect_mentioned_timeline=True,
        prospect_mentioned_budget=False,
        competitor_mentioned=False,
        objections_raised=0,
        next_step_agreed=True,
        next_step_days_out=7,
        talk_ratio_pct=45.0,
        demo_shown=True,
        proposal_sent=False,
        references_offered=False,
        previous_meetings_count=0,
        days_since_last_meeting=7,
    )
    defaults.update(overrides)
    return MeetingInput(**defaults)


def make_engine(*inputs) -> MeetingIntelligenceEngine:
    engine = MeetingIntelligenceEngine()
    for inp in inputs:
        engine.analyze(inp)
    return engine


# ─── Test Enum Values ─────────────────────────────────────────────────────────

class TestMeetingOutcomeEnum:
    def test_advanced_value(self):
        assert MeetingOutcome.ADVANCED.value == "advanced"

    def test_maintained_value(self):
        assert MeetingOutcome.MAINTAINED.value == "maintained"

    def test_regressed_value(self):
        assert MeetingOutcome.REGRESSED.value == "regressed"

    def test_no_decision_value(self):
        assert MeetingOutcome.NO_DECISION.value == "no_decision"

    def test_all_four_members(self):
        assert len(MeetingOutcome) == 4

    def test_is_str_enum(self):
        assert isinstance(MeetingOutcome.ADVANCED, str)


class TestMeetingQualityEnum:
    def test_excellent_value(self):
        assert MeetingQuality.EXCELLENT.value == "excellent"

    def test_good_value(self):
        assert MeetingQuality.GOOD.value == "good"

    def test_average_value(self):
        assert MeetingQuality.AVERAGE.value == "average"

    def test_poor_value(self):
        assert MeetingQuality.POOR.value == "poor"

    def test_all_four_members(self):
        assert len(MeetingQuality) == 4

    def test_is_str_enum(self):
        assert isinstance(MeetingQuality.EXCELLENT, str)


class TestBuyingSignalStrengthEnum:
    def test_strong_value(self):
        assert BuyingSignalStrength.STRONG.value == "strong"

    def test_moderate_value(self):
        assert BuyingSignalStrength.MODERATE.value == "moderate"

    def test_weak_value(self):
        assert BuyingSignalStrength.WEAK.value == "weak"

    def test_negative_value(self):
        assert BuyingSignalStrength.NEGATIVE.value == "negative"

    def test_all_four_members(self):
        assert len(BuyingSignalStrength) == 4

    def test_is_str_enum(self):
        assert isinstance(BuyingSignalStrength.STRONG, str)


class TestFollowUpUrgencyEnum:
    def test_immediate_value(self):
        assert FollowUpUrgency.IMMEDIATE.value == "immediate"

    def test_same_week_value(self):
        assert FollowUpUrgency.SAME_WEEK.value == "same_week"

    def test_standard_value(self):
        assert FollowUpUrgency.STANDARD.value == "standard"

    def test_monitor_value(self):
        assert FollowUpUrgency.MONITOR.value == "monitor"

    def test_all_four_members(self):
        assert len(FollowUpUrgency) == 4

    def test_is_str_enum(self):
        assert isinstance(FollowUpUrgency.IMMEDIATE, str)


# ─── Test MeetingInput Fields ─────────────────────────────────────────────────

class TestMeetingInputFields:
    def test_meeting_id_field(self):
        inp = make_input(meeting_id="x")
        assert inp.meeting_id == "x"

    def test_deal_id_field(self):
        inp = make_input(deal_id="d99")
        assert inp.deal_id == "d99"

    def test_rep_id_field(self):
        inp = make_input(rep_id="r99")
        assert inp.rep_id == "r99"

    def test_rep_name_field(self):
        inp = make_input(rep_name="Bob")
        assert inp.rep_name == "Bob"

    def test_account_name_field(self):
        inp = make_input(account_name="BigCo")
        assert inp.account_name == "BigCo"

    def test_meeting_type_field(self):
        inp = make_input(meeting_type="discovery")
        assert inp.meeting_type == "discovery"

    def test_duration_minutes_field(self):
        inp = make_input(duration_minutes=45)
        assert inp.duration_minutes == 45

    def test_attendees_count_field(self):
        inp = make_input(attendees_count=5)
        assert inp.attendees_count == 5

    def test_decision_maker_present_field(self):
        inp = make_input(decision_maker_present=False)
        assert inp.decision_maker_present is False

    def test_exec_sponsor_present_field(self):
        inp = make_input(exec_sponsor_present=True)
        assert inp.exec_sponsor_present is True

    def test_prospect_asked_questions_field(self):
        inp = make_input(prospect_asked_questions=False)
        assert inp.prospect_asked_questions is False

    def test_prospect_requested_pricing_field(self):
        inp = make_input(prospect_requested_pricing=True)
        assert inp.prospect_requested_pricing is True

    def test_prospect_mentioned_timeline_field(self):
        inp = make_input(prospect_mentioned_timeline=False)
        assert inp.prospect_mentioned_timeline is False

    def test_prospect_mentioned_budget_field(self):
        inp = make_input(prospect_mentioned_budget=True)
        assert inp.prospect_mentioned_budget is True

    def test_competitor_mentioned_field(self):
        inp = make_input(competitor_mentioned=True)
        assert inp.competitor_mentioned is True

    def test_objections_raised_field(self):
        inp = make_input(objections_raised=3)
        assert inp.objections_raised == 3

    def test_next_step_agreed_field(self):
        inp = make_input(next_step_agreed=False)
        assert inp.next_step_agreed is False

    def test_next_step_days_out_field_none(self):
        inp = make_input(next_step_days_out=None)
        assert inp.next_step_days_out is None

    def test_next_step_days_out_field_value(self):
        inp = make_input(next_step_days_out=10)
        assert inp.next_step_days_out == 10

    def test_talk_ratio_pct_field(self):
        inp = make_input(talk_ratio_pct=60.0)
        assert inp.talk_ratio_pct == 60.0

    def test_demo_shown_field(self):
        inp = make_input(demo_shown=False)
        assert inp.demo_shown is False

    def test_proposal_sent_field(self):
        inp = make_input(proposal_sent=True)
        assert inp.proposal_sent is True

    def test_references_offered_field(self):
        inp = make_input(references_offered=True)
        assert inp.references_offered is True

    def test_previous_meetings_count_field(self):
        inp = make_input(previous_meetings_count=3)
        assert inp.previous_meetings_count == 3

    def test_days_since_last_meeting_field(self):
        inp = make_input(days_since_last_meeting=14)
        assert inp.days_since_last_meeting == 14

    def test_total_field_count(self):
        import dataclasses
        fields = dataclasses.fields(MeetingInput)
        assert len(fields) == 24


# ─── Test to_dict() ────────────────────────────────────────────────────────────

class TestMeetingResultToDict:
    def setup_method(self):
        self.engine = MeetingIntelligenceEngine()
        self.inp = make_input()
        self.result = self.engine.analyze(self.inp)
        self.d = self.result.to_dict()

    def test_returns_exactly_20_keys(self):
        assert len(self.d) == 20

    def test_has_meeting_id(self):
        assert "meeting_id" in self.d

    def test_has_deal_id(self):
        assert "deal_id" in self.d

    def test_has_rep_id(self):
        assert "rep_id" in self.d

    def test_has_rep_name(self):
        assert "rep_name" in self.d

    def test_has_account_name(self):
        assert "account_name" in self.d

    def test_has_meeting_type(self):
        assert "meeting_type" in self.d

    def test_has_meeting_outcome(self):
        assert "meeting_outcome" in self.d

    def test_has_meeting_quality(self):
        assert "meeting_quality" in self.d

    def test_has_buying_signal_strength(self):
        assert "buying_signal_strength" in self.d

    def test_has_follow_up_urgency(self):
        assert "follow_up_urgency" in self.d

    def test_has_quality_score(self):
        assert "quality_score" in self.d

    def test_has_engagement_score(self):
        assert "engagement_score" in self.d

    def test_has_buying_signals_count(self):
        assert "buying_signals_count" in self.d

    def test_has_objections_count(self):
        assert "objections_count" in self.d

    def test_has_next_step_agreed(self):
        assert "next_step_agreed" in self.d

    def test_has_next_step_days_out(self):
        assert "next_step_days_out" in self.d

    def test_has_positive_signals(self):
        assert "positive_signals" in self.d

    def test_has_concerns(self):
        assert "concerns" in self.d

    def test_has_follow_up_actions(self):
        assert "follow_up_actions" in self.d

    def test_has_manager_alerts(self):
        assert "manager_alerts" in self.d

    def test_meeting_outcome_is_string(self):
        assert isinstance(self.d["meeting_outcome"], str)

    def test_meeting_quality_is_string(self):
        assert isinstance(self.d["meeting_quality"], str)

    def test_buying_signal_strength_is_string(self):
        assert isinstance(self.d["buying_signal_strength"], str)

    def test_follow_up_urgency_is_string(self):
        assert isinstance(self.d["follow_up_urgency"], str)

    def test_quality_score_is_numeric(self):
        assert isinstance(self.d["quality_score"], (int, float))

    def test_engagement_score_is_numeric(self):
        assert isinstance(self.d["engagement_score"], (int, float))

    def test_positive_signals_is_list(self):
        assert isinstance(self.d["positive_signals"], list)

    def test_concerns_is_list(self):
        assert isinstance(self.d["concerns"], list)

    def test_follow_up_actions_is_list(self):
        assert isinstance(self.d["follow_up_actions"], list)

    def test_manager_alerts_is_list(self):
        assert isinstance(self.d["manager_alerts"], list)

    def test_meeting_id_value(self):
        assert self.d["meeting_id"] == "m1"

    def test_meeting_outcome_raw_value(self):
        assert self.d["meeting_outcome"] in [e.value for e in MeetingOutcome]

    def test_meeting_quality_raw_value(self):
        assert self.d["meeting_quality"] in [e.value for e in MeetingQuality]


# ─── Test Engagement Score ────────────────────────────────────────────────────

class TestEngagementScore:
    def setup_method(self):
        self.engine = MeetingIntelligenceEngine()

    def _score(self, **overrides) -> float:
        inp = make_input(**overrides)
        result = self.engine.analyze(inp)
        self.engine.reset()
        return result.engagement_score

    def test_zero_engagement_no_signals_no_objections(self):
        score = self._score(
            prospect_asked_questions=False,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=0,
        )
        assert score == 0.0

    def test_max_engagement_all_signals_no_objections(self):
        score = self._score(
            prospect_asked_questions=True,
            prospect_requested_pricing=True,
            prospect_mentioned_timeline=True,
            prospect_mentioned_budget=True,
            decision_maker_present=True,
            exec_sponsor_present=True,
            objections_raised=0,
        )
        assert score == 90.0

    def test_questions_worth_20(self):
        score = self._score(
            prospect_asked_questions=True,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=0,
        )
        assert score == 20.0

    def test_pricing_worth_20(self):
        score = self._score(
            prospect_asked_questions=False,
            prospect_requested_pricing=True,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=0,
        )
        assert score == 20.0

    def test_timeline_worth_15(self):
        score = self._score(
            prospect_asked_questions=False,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=True,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=0,
        )
        assert score == 15.0

    def test_budget_worth_15(self):
        score = self._score(
            prospect_asked_questions=False,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=True,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=0,
        )
        assert score == 15.0

    def test_dm_present_worth_15(self):
        score = self._score(
            prospect_asked_questions=False,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=True,
            exec_sponsor_present=False,
            objections_raised=0,
        )
        assert score == 15.0

    def test_exec_sponsor_worth_5(self):
        score = self._score(
            prospect_asked_questions=False,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=True,
            objections_raised=0,
        )
        assert score == 5.0

    def test_one_objection_deducts_5(self):
        score = self._score(
            prospect_asked_questions=True,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=1,
        )
        assert score == 15.0

    def test_score_floored_at_zero(self):
        score = self._score(
            prospect_asked_questions=False,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=10,
        )
        assert score == 0.0

    def test_score_capped_at_100(self):
        score = self._score(
            prospect_asked_questions=True,
            prospect_requested_pricing=True,
            prospect_mentioned_timeline=True,
            prospect_mentioned_budget=True,
            decision_maker_present=True,
            exec_sponsor_present=True,
            objections_raised=0,
        )
        assert score <= 100.0

    def test_score_is_numeric(self):
        score = self._score()
        assert isinstance(score, (int, float))

    def test_four_objections_reduces_score(self):
        score = self._score(
            prospect_asked_questions=True,
            prospect_requested_pricing=True,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=4,
        )
        assert score == 20.0


# ─── Test Quality Score ────────────────────────────────────────────────────────

class TestQualityScore:
    def setup_method(self):
        self.engine = MeetingIntelligenceEngine()

    def _score(self, **overrides) -> float:
        inp = make_input(**overrides)
        result = self.engine.analyze(inp)
        self.engine.reset()
        return result.quality_score

    def test_quality_score_is_numeric(self):
        assert isinstance(self._score(), (int, float))

    def test_quality_score_gte_zero(self):
        score = self._score(
            prospect_asked_questions=False,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=10,
            next_step_agreed=False,
            next_step_days_out=None,
            talk_ratio_pct=80.0,
            demo_shown=False,
            proposal_sent=False,
            duration_minutes=10,
            attendees_count=1,
        )
        assert score >= 0.0

    def test_quality_score_lte_100(self):
        score = self._score(
            prospect_asked_questions=True,
            prospect_requested_pricing=True,
            prospect_mentioned_timeline=True,
            prospect_mentioned_budget=True,
            decision_maker_present=True,
            exec_sponsor_present=True,
            objections_raised=0,
            next_step_agreed=True,
            next_step_days_out=7,
            talk_ratio_pct=40.0,
            demo_shown=True,
            proposal_sent=True,
            duration_minutes=90,
            attendees_count=5,
        )
        assert score <= 100.0

    def test_next_step_agreed_adds_20(self):
        base = self._score(next_step_agreed=False, next_step_days_out=None)
        with_ns = self._score(next_step_agreed=True, next_step_days_out=7)
        assert with_ns > base

    def test_next_step_over_14_days_deducts_10(self):
        close = self._score(next_step_agreed=True, next_step_days_out=14)
        far = self._score(next_step_agreed=True, next_step_days_out=15)
        assert close > far

    def test_next_step_exactly_14_days_no_deduction(self):
        at14 = self._score(next_step_agreed=True, next_step_days_out=14)
        at7 = self._score(next_step_agreed=True, next_step_days_out=7)
        assert at14 == at7

    def test_talk_ratio_50_gets_10_pts(self):
        low = self._score(talk_ratio_pct=50.0)
        high = self._score(talk_ratio_pct=51.0)
        assert low > high

    def test_talk_ratio_exactly_50_gets_points(self):
        score_50 = self._score(talk_ratio_pct=50.0)
        score_49 = self._score(talk_ratio_pct=49.0)
        assert score_50 == score_49

    def test_demo_shown_adds_8(self):
        no_demo = self._score(demo_shown=False)
        with_demo = self._score(demo_shown=True)
        assert with_demo - no_demo == pytest.approx(8.0, abs=0.1)

    def test_proposal_sent_adds_7(self):
        no_prop = self._score(proposal_sent=False)
        with_prop = self._score(proposal_sent=True)
        assert with_prop - no_prop == pytest.approx(7.0, abs=0.1)

    def test_duration_30_adds_5(self):
        short = self._score(duration_minutes=29)
        at30 = self._score(duration_minutes=30)
        assert at30 - short == pytest.approx(5.0, abs=0.1)

    def test_duration_60_adds_additional_5(self):
        at30 = self._score(duration_minutes=30)
        at60 = self._score(duration_minutes=60)
        assert at60 - at30 == pytest.approx(5.0, abs=0.1)

    def test_attendees_2_adds_5(self):
        solo = self._score(attendees_count=1)
        multi = self._score(attendees_count=2)
        assert multi - solo == pytest.approx(5.0, abs=0.1)


# ─── Test Buying Signal Strength ──────────────────────────────────────────────

class TestBuyingSignalStrength:
    def setup_method(self):
        self.engine = MeetingIntelligenceEngine()

    def _strength(self, **overrides) -> BuyingSignalStrength:
        inp = make_input(**overrides)
        result = self.engine.analyze(inp)
        self.engine.reset()
        return result.buying_signal_strength

    def test_negative_when_zero_signals_one_objection(self):
        strength = self._strength(
            prospect_asked_questions=False,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=1,
        )
        assert strength == BuyingSignalStrength.NEGATIVE

    def test_negative_when_zero_signals_multiple_objections(self):
        strength = self._strength(
            prospect_asked_questions=False,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=3,
        )
        assert strength == BuyingSignalStrength.NEGATIVE

    def test_negative_when_zero_signals_zero_objections(self):
        strength = self._strength(
            prospect_asked_questions=False,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=0,
        )
        assert strength == BuyingSignalStrength.NEGATIVE

    def test_strong_with_3_signals_zero_objections(self):
        strength = self._strength(
            prospect_asked_questions=True,
            prospect_requested_pricing=True,
            prospect_mentioned_timeline=True,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=0,
        )
        assert strength == BuyingSignalStrength.STRONG

    def test_strong_with_3_signals_one_objection(self):
        strength = self._strength(
            prospect_asked_questions=True,
            prospect_requested_pricing=True,
            prospect_mentioned_timeline=True,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=1,
        )
        assert strength == BuyingSignalStrength.STRONG

    def test_not_strong_with_3_signals_two_objections(self):
        strength = self._strength(
            prospect_asked_questions=True,
            prospect_requested_pricing=True,
            prospect_mentioned_timeline=True,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=2,
        )
        assert strength != BuyingSignalStrength.STRONG

    def test_strong_with_6_signals_zero_objections(self):
        strength = self._strength(
            prospect_asked_questions=True,
            prospect_requested_pricing=True,
            prospect_mentioned_timeline=True,
            prospect_mentioned_budget=True,
            decision_maker_present=True,
            exec_sponsor_present=True,
            objections_raised=0,
        )
        assert strength == BuyingSignalStrength.STRONG

    def test_moderate_with_1_signal_zero_objections(self):
        strength = self._strength(
            prospect_asked_questions=True,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=0,
        )
        assert strength == BuyingSignalStrength.MODERATE

    def test_moderate_with_2_signals_one_objection(self):
        strength = self._strength(
            prospect_asked_questions=True,
            prospect_requested_pricing=True,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=1,
        )
        assert strength == BuyingSignalStrength.MODERATE

    def test_weak_with_1_signal_equals_objections(self):
        strength = self._strength(
            prospect_asked_questions=True,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=1,
        )
        assert strength == BuyingSignalStrength.WEAK

    def test_weak_with_2_signals_more_objections(self):
        strength = self._strength(
            prospect_asked_questions=True,
            prospect_requested_pricing=True,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=3,
        )
        assert strength == BuyingSignalStrength.WEAK

    def test_buying_signals_count_correct(self):
        inp = make_input(
            prospect_asked_questions=True,
            prospect_requested_pricing=True,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=True,
            exec_sponsor_present=False,
        )
        result = self.engine.analyze(inp)
        self.engine.reset()
        assert result.buying_signals_count == 3

    def test_buying_signals_count_zero(self):
        inp = make_input(
            prospect_asked_questions=False,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
        )
        result = self.engine.analyze(inp)
        self.engine.reset()
        assert result.buying_signals_count == 0

    def test_buying_signals_count_max(self):
        inp = make_input(
            prospect_asked_questions=True,
            prospect_requested_pricing=True,
            prospect_mentioned_timeline=True,
            prospect_mentioned_budget=True,
            decision_maker_present=True,
            exec_sponsor_present=True,
        )
        result = self.engine.analyze(inp)
        self.engine.reset()
        assert result.buying_signals_count == 6


# ─── Test Meeting Outcome ────────────────────────────────────────────────────

class TestMeetingOutcome:
    def setup_method(self):
        self.engine = MeetingIntelligenceEngine()

    def _outcome(self, **overrides) -> MeetingOutcome:
        inp = make_input(**overrides)
        result = self.engine.analyze(inp)
        self.engine.reset()
        return result.meeting_outcome

    def test_regressed_when_no_next_step_and_no_signals(self):
        outcome = self._outcome(
            next_step_agreed=False,
            prospect_asked_questions=False,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=0,
        )
        assert outcome == MeetingOutcome.REGRESSED

    def test_regressed_when_no_next_step_and_3_objections(self):
        outcome = self._outcome(
            next_step_agreed=False,
            prospect_asked_questions=True,
            prospect_requested_pricing=True,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=3,
        )
        assert outcome == MeetingOutcome.REGRESSED

    def test_no_decision_when_no_next_step_some_signals(self):
        outcome = self._outcome(
            next_step_agreed=False,
            prospect_asked_questions=True,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=0,
        )
        assert outcome == MeetingOutcome.NO_DECISION

    def test_no_decision_boundary_2_objections_no_next_step(self):
        outcome = self._outcome(
            next_step_agreed=False,
            prospect_asked_questions=True,
            prospect_requested_pricing=True,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=2,
        )
        assert outcome == MeetingOutcome.NO_DECISION

    def test_advanced_with_next_step_and_2_signals_0_objections(self):
        outcome = self._outcome(
            next_step_agreed=True,
            prospect_asked_questions=True,
            prospect_requested_pricing=True,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=0,
        )
        assert outcome == MeetingOutcome.ADVANCED

    def test_advanced_with_next_step_and_2_signals_1_objection(self):
        outcome = self._outcome(
            next_step_agreed=True,
            prospect_asked_questions=True,
            prospect_requested_pricing=True,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=1,
        )
        assert outcome == MeetingOutcome.ADVANCED

    def test_maintained_with_next_step_only_1_signal(self):
        outcome = self._outcome(
            next_step_agreed=True,
            prospect_asked_questions=True,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=0,
        )
        assert outcome == MeetingOutcome.MAINTAINED

    def test_maintained_with_next_step_2_signals_2_objections(self):
        outcome = self._outcome(
            next_step_agreed=True,
            prospect_asked_questions=True,
            prospect_requested_pricing=True,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=2,
        )
        assert outcome == MeetingOutcome.MAINTAINED

    def test_not_advanced_with_2_signals_but_2_objections(self):
        outcome = self._outcome(
            next_step_agreed=True,
            prospect_asked_questions=True,
            prospect_requested_pricing=True,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=2,
        )
        assert outcome != MeetingOutcome.ADVANCED


# ─── Test Meeting Quality Thresholds ─────────────────────────────────────────

class TestMeetingQualityThresholds:
    def setup_method(self):
        self.engine = MeetingIntelligenceEngine()

    def _quality_for_score(self, score: float) -> MeetingQuality:
        return self.engine._meeting_quality(score)

    def test_excellent_at_75(self):
        assert self._quality_for_score(75.0) == MeetingQuality.EXCELLENT

    def test_excellent_at_100(self):
        assert self._quality_for_score(100.0) == MeetingQuality.EXCELLENT

    def test_excellent_at_80(self):
        assert self._quality_for_score(80.0) == MeetingQuality.EXCELLENT

    def test_good_at_55(self):
        assert self._quality_for_score(55.0) == MeetingQuality.GOOD

    def test_good_at_74(self):
        assert self._quality_for_score(74.9) == MeetingQuality.GOOD

    def test_good_at_60(self):
        assert self._quality_for_score(60.0) == MeetingQuality.GOOD

    def test_average_at_35(self):
        assert self._quality_for_score(35.0) == MeetingQuality.AVERAGE

    def test_average_at_54(self):
        assert self._quality_for_score(54.9) == MeetingQuality.AVERAGE

    def test_average_at_45(self):
        assert self._quality_for_score(45.0) == MeetingQuality.AVERAGE

    def test_poor_at_34(self):
        assert self._quality_for_score(34.9) == MeetingQuality.POOR

    def test_poor_at_0(self):
        assert self._quality_for_score(0.0) == MeetingQuality.POOR

    def test_poor_at_20(self):
        assert self._quality_for_score(20.0) == MeetingQuality.POOR

    def test_boundary_exactly_75_is_excellent(self):
        assert self._quality_for_score(75.0) == MeetingQuality.EXCELLENT

    def test_boundary_exactly_55_is_good(self):
        assert self._quality_for_score(55.0) == MeetingQuality.GOOD

    def test_boundary_exactly_35_is_average(self):
        assert self._quality_for_score(35.0) == MeetingQuality.AVERAGE


# ─── Test Follow-Up Urgency ───────────────────────────────────────────────────

class TestFollowUpUrgency:
    def setup_method(self):
        self.engine = MeetingIntelligenceEngine()

    def _urgency(self, **overrides) -> FollowUpUrgency:
        inp = make_input(**overrides)
        result = self.engine.analyze(inp)
        self.engine.reset()
        return result.follow_up_urgency

    def test_immediate_when_regressed(self):
        urgency = self._urgency(
            next_step_agreed=False,
            prospect_asked_questions=False,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=0,
        )
        assert urgency == FollowUpUrgency.IMMEDIATE

    def test_same_week_when_strong_signals(self):
        urgency = self._urgency(
            prospect_asked_questions=True,
            prospect_requested_pricing=True,
            prospect_mentioned_timeline=True,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=0,
            next_step_agreed=True,
            next_step_days_out=7,
        )
        assert urgency == FollowUpUrgency.SAME_WEEK

    def test_same_week_when_pricing_requested(self):
        urgency = self._urgency(
            prospect_asked_questions=False,
            prospect_requested_pricing=True,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=0,
            next_step_agreed=True,
            next_step_days_out=7,
        )
        assert urgency == FollowUpUrgency.SAME_WEEK

    def test_same_week_when_timeline_mentioned(self):
        urgency = self._urgency(
            prospect_asked_questions=False,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=True,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=0,
            next_step_agreed=True,
            next_step_days_out=7,
        )
        assert urgency == FollowUpUrgency.SAME_WEEK

    def test_same_week_maintained_with_2_objections(self):
        urgency = self._urgency(
            next_step_agreed=True,
            next_step_days_out=7,
            prospect_asked_questions=False,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=2,
        )
        assert urgency == FollowUpUrgency.SAME_WEEK

    def test_same_week_no_decision(self):
        urgency = self._urgency(
            next_step_agreed=False,
            prospect_asked_questions=True,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=0,
        )
        assert urgency == FollowUpUrgency.SAME_WEEK

    def test_standard_when_moderate_signals(self):
        urgency = self._urgency(
            prospect_asked_questions=True,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=0,
            next_step_agreed=True,
            next_step_days_out=7,
        )
        assert urgency == FollowUpUrgency.STANDARD

    def test_monitor_weak_or_negative_advanced(self):
        urgency = self._urgency(
            prospect_asked_questions=False,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=0,
            next_step_agreed=True,
            next_step_days_out=7,
            talk_ratio_pct=45.0,
        )
        assert urgency == FollowUpUrgency.MONITOR


# ─── Test Positive Signals Narrative ─────────────────────────────────────────

class TestPositiveSignals:
    def setup_method(self):
        self.engine = MeetingIntelligenceEngine()

    def _signals(self, **overrides) -> list:
        inp = make_input(**overrides)
        result = self.engine.analyze(inp)
        self.engine.reset()
        return result.positive_signals

    def test_empty_when_no_positive_flags(self):
        signals = self._signals(
            prospect_asked_questions=False,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            next_step_agreed=False,
            next_step_days_out=None,
        )
        assert signals == []

    def test_next_step_with_days_appears(self):
        signals = self._signals(next_step_agreed=True, next_step_days_out=5)
        assert any("5" in s for s in signals)

    def test_next_step_without_days_appears(self):
        signals = self._signals(next_step_agreed=True, next_step_days_out=None)
        assert any("étape" in s for s in signals)

    def test_all_signals_present(self):
        signals = self._signals(
            prospect_asked_questions=True,
            prospect_requested_pricing=True,
            prospect_mentioned_timeline=True,
            prospect_mentioned_budget=True,
            decision_maker_present=True,
            exec_sponsor_present=True,
            next_step_agreed=True,
            next_step_days_out=7,
        )
        assert len(signals) == 7

    def test_dm_present_in_signals(self):
        signals = self._signals(decision_maker_present=True, next_step_agreed=False)
        assert any("Décideur" in s for s in signals)

    def test_exec_sponsor_in_signals(self):
        signals = self._signals(exec_sponsor_present=True, next_step_agreed=False)
        assert any("Sponsor" in s or "exécutif" in s for s in signals)


# ─── Test Concerns Narrative ──────────────────────────────────────────────────

class TestConcerns:
    def setup_method(self):
        self.engine = MeetingIntelligenceEngine()

    def _concerns(self, **overrides) -> list:
        inp = make_input(**overrides)
        result = self.engine.analyze(inp)
        self.engine.reset()
        return result.concerns

    def test_no_concerns_baseline(self):
        concerns = self._concerns(
            objections_raised=0,
            talk_ratio_pct=45.0,
            next_step_agreed=True,
            next_step_days_out=7,
            competitor_mentioned=False,
            duration_minutes=60,
        )
        assert concerns == []

    def test_objection_concern_raised(self):
        concerns = self._concerns(objections_raised=2)
        assert any("objection" in c for c in concerns)

    def test_high_talk_ratio_concern(self):
        concerns = self._concerns(talk_ratio_pct=70.0)
        assert any("70" in c for c in concerns)

    def test_talk_ratio_66_triggers_concern(self):
        concerns = self._concerns(talk_ratio_pct=66.0)
        assert any("66" in c for c in concerns)

    def test_talk_ratio_65_no_concern(self):
        concerns = self._concerns(talk_ratio_pct=65.0)
        assert not any("parle" in c for c in concerns)

    def test_no_next_step_concern(self):
        concerns = self._concerns(next_step_agreed=False)
        assert any("prochaine étape" in c.lower() for c in concerns)

    def test_next_step_far_concern(self):
        concerns = self._concerns(next_step_agreed=True, next_step_days_out=15)
        assert any("15" in c for c in concerns)

    def test_next_step_14_no_far_concern(self):
        concerns = self._concerns(next_step_agreed=True, next_step_days_out=14)
        assert not any("14j" in c for c in concerns)

    def test_competitor_concern(self):
        concerns = self._concerns(competitor_mentioned=True)
        assert any("Concurrent" in c or "concurrent" in c for c in concerns)

    def test_short_meeting_concern(self):
        concerns = self._concerns(duration_minutes=15)
        assert any("15" in c for c in concerns)

    def test_duration_20_no_short_concern(self):
        concerns = self._concerns(duration_minutes=20)
        assert not any("courte" in c for c in concerns)

    def test_duration_19_triggers_concern(self):
        concerns = self._concerns(duration_minutes=19)
        assert any("courte" in c for c in concerns)


# ─── Test Follow-Up Actions ───────────────────────────────────────────────────

class TestFollowUpActions:
    def setup_method(self):
        self.engine = MeetingIntelligenceEngine()

    def _actions(self, **overrides) -> list:
        inp = make_input(**overrides)
        result = self.engine.analyze(inp)
        self.engine.reset()
        return result.follow_up_actions

    def test_default_thank_you_when_no_action(self):
        # All action triggers are off AND next_step IS agreed (so no "relancer" fallback)
        actions = self._actions(
            prospect_requested_pricing=False,
            next_step_agreed=True,
            next_step_days_out=None,
            objections_raised=0,
            competitor_mentioned=False,
            prospect_mentioned_budget=False,
            prospect_asked_questions=False,
            prospect_mentioned_timeline=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
        )
        assert any("remerciement" in a for a in actions)

    def test_pricing_action_when_requested_no_proposal(self):
        actions = self._actions(prospect_requested_pricing=True, proposal_sent=False)
        assert any("tarifaire" in a for a in actions)

    def test_no_pricing_action_when_proposal_already_sent(self):
        actions = self._actions(prospect_requested_pricing=True, proposal_sent=True)
        assert not any("tarifaire" in a for a in actions)

    def test_next_step_confirmation_action(self):
        actions = self._actions(next_step_agreed=True, next_step_days_out=5)
        assert any("5" in a for a in actions)

    def test_objection_action_when_raised(self):
        actions = self._actions(objections_raised=1)
        assert any("objection" in a.lower() for a in actions)

    def test_competitor_battlecard_action(self):
        actions = self._actions(competitor_mentioned=True)
        assert any("battlecard" in a.lower() or "compétiti" in a.lower() for a in actions)

    def test_budget_roi_action(self):
        actions = self._actions(prospect_mentioned_budget=True)
        assert any("ROI" in a for a in actions)

    def test_regressed_urgency_action(self):
        actions = self._actions(
            next_step_agreed=False,
            prospect_asked_questions=False,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=0,
        )
        assert any("urgence" in a.lower() or "blocage" in a.lower() for a in actions)

    def test_no_next_step_follow_up_action(self):
        actions = self._actions(
            next_step_agreed=False,
            prospect_asked_questions=True,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=0,
        )
        assert any("48h" in a for a in actions)

    def test_actions_never_empty(self):
        actions = self._actions()
        assert len(actions) >= 1


# ─── Test Manager Alerts ──────────────────────────────────────────────────────

class TestManagerAlerts:
    def setup_method(self):
        self.engine = MeetingIntelligenceEngine()

    def _alerts(self, **overrides) -> list:
        inp = make_input(**overrides)
        result = self.engine.analyze(inp)
        self.engine.reset()
        return result.manager_alerts

    def test_no_alerts_clean_meeting(self):
        alerts = self._alerts(
            prospect_asked_questions=True,
            prospect_requested_pricing=True,
            prospect_mentioned_timeline=True,
            objections_raised=0,
            talk_ratio_pct=45.0,
            next_step_agreed=True,
            next_step_days_out=7,
            competitor_mentioned=False,
            previous_meetings_count=0,
        )
        assert alerts == []

    def test_alert_for_regressed_deal(self):
        alerts = self._alerts(
            next_step_agreed=False,
            prospect_asked_questions=False,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=0,
        )
        assert any("régressé" in a for a in alerts)

    def test_alert_for_poor_quality_repeat_deal(self):
        alerts = self._alerts(
            previous_meetings_count=2,
            prospect_asked_questions=False,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=10,
            next_step_agreed=False,
            next_step_days_out=None,
            talk_ratio_pct=80.0,
            demo_shown=False,
            proposal_sent=False,
            duration_minutes=10,
            attendees_count=1,
        )
        assert any("médiocre" in a or "coaching" in a for a in alerts)

    def test_alert_for_high_talk_ratio_70(self):
        alerts = self._alerts(talk_ratio_pct=71.0)
        assert any("Ratio" in a or "ratio" in a or "parole" in a for a in alerts)

    def test_no_alert_talk_ratio_exactly_70(self):
        alerts = self._alerts(talk_ratio_pct=70.0)
        talk_alerts = [a for a in alerts if "parole" in a or "Ratio" in a]
        assert len(talk_alerts) == 0

    def test_alert_competitor_plus_multiple_objections(self):
        alerts = self._alerts(competitor_mentioned=True, objections_raised=2)
        assert any("Concurrent" in a or "danger" in a for a in alerts)

    def test_alert_no_next_step_after_second_meeting(self):
        alerts = self._alerts(
            next_step_agreed=False,
            previous_meetings_count=1,
            prospect_asked_questions=True,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=0,
        )
        assert any("bloqué" in a or "prochaine étape" in a for a in alerts)

    def test_no_next_step_alert_first_meeting(self):
        alerts = self._alerts(
            next_step_agreed=False,
            previous_meetings_count=0,
            prospect_asked_questions=True,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=0,
        )
        assert not any("bloqué" in a for a in alerts)


# ─── Test analyze() ───────────────────────────────────────────────────────────

class TestAnalyze:
    def setup_method(self):
        self.engine = MeetingIntelligenceEngine()

    def test_returns_meeting_result(self):
        inp = make_input()
        result = self.engine.analyze(inp)
        assert isinstance(result, MeetingResult)

    def test_result_stored_in_engine(self):
        inp = make_input()
        self.engine.analyze(inp)
        assert len(self.engine.all_meetings()) == 1

    def test_multiple_analyses_stored(self):
        for i in range(3):
            self.engine.analyze(make_input(meeting_id=f"m{i}"))
        assert len(self.engine.all_meetings()) == 3

    def test_result_meeting_id_matches(self):
        inp = make_input(meeting_id="unique123")
        result = self.engine.analyze(inp)
        assert result.meeting_id == "unique123"

    def test_result_deal_id_matches(self):
        inp = make_input(deal_id="deal99")
        result = self.engine.analyze(inp)
        assert result.deal_id == "deal99"

    def test_result_rep_name_matches(self):
        inp = make_input(rep_name="Charlie")
        result = self.engine.analyze(inp)
        assert result.rep_name == "Charlie"

    def test_result_account_name_matches(self):
        inp = make_input(account_name="Megacorp")
        result = self.engine.analyze(inp)
        assert result.account_name == "Megacorp"

    def test_result_meeting_type_matches(self):
        inp = make_input(meeting_type="negotiation")
        result = self.engine.analyze(inp)
        assert result.meeting_type == "negotiation"

    def test_objections_count_matches_input(self):
        inp = make_input(objections_raised=4)
        result = self.engine.analyze(inp)
        assert result.objections_count == 4

    def test_next_step_agreed_matches_input(self):
        inp = make_input(next_step_agreed=False)
        result = self.engine.analyze(inp)
        assert result.next_step_agreed is False

    def test_next_step_days_out_matches_input(self):
        inp = make_input(next_step_days_out=10)
        result = self.engine.analyze(inp)
        assert result.next_step_days_out == 10

    def test_quality_score_in_range(self):
        inp = make_input()
        result = self.engine.analyze(inp)
        assert 0.0 <= result.quality_score <= 100.0

    def test_engagement_score_in_range(self):
        inp = make_input()
        result = self.engine.analyze(inp)
        assert 0.0 <= result.engagement_score <= 100.0

    def test_meeting_outcome_is_enum(self):
        inp = make_input()
        result = self.engine.analyze(inp)
        assert isinstance(result.meeting_outcome, MeetingOutcome)

    def test_meeting_quality_is_enum(self):
        inp = make_input()
        result = self.engine.analyze(inp)
        assert isinstance(result.meeting_quality, MeetingQuality)

    def test_buying_signal_strength_is_enum(self):
        inp = make_input()
        result = self.engine.analyze(inp)
        assert isinstance(result.buying_signal_strength, BuyingSignalStrength)

    def test_follow_up_urgency_is_enum(self):
        inp = make_input()
        result = self.engine.analyze(inp)
        assert isinstance(result.follow_up_urgency, FollowUpUrgency)


# ─── Test analyze_batch() ────────────────────────────────────────────────────

class TestAnalyzeBatch:
    def setup_method(self):
        self.engine = MeetingIntelligenceEngine()

    def test_returns_list(self):
        results = self.engine.analyze_batch([make_input()])
        assert isinstance(results, list)

    def test_batch_sorted_desc_by_quality_score(self):
        inputs = [
            make_input(meeting_id="a", duration_minutes=10, demo_shown=False, proposal_sent=False,
                       next_step_agreed=False, next_step_days_out=None,
                       prospect_asked_questions=False, prospect_requested_pricing=False,
                       prospect_mentioned_timeline=False, prospect_mentioned_budget=False,
                       decision_maker_present=False, exec_sponsor_present=False),
            make_input(meeting_id="b", duration_minutes=90, demo_shown=True, proposal_sent=True,
                       next_step_agreed=True, next_step_days_out=7,
                       prospect_asked_questions=True, prospect_requested_pricing=True,
                       prospect_mentioned_timeline=True, prospect_mentioned_budget=True,
                       decision_maker_present=True, exec_sponsor_present=True,
                       objections_raised=0, talk_ratio_pct=40.0),
        ]
        results = self.engine.analyze_batch(inputs)
        assert results[0].quality_score >= results[1].quality_score

    def test_batch_all_stored_in_engine(self):
        inputs = [make_input(meeting_id=f"m{i}") for i in range(4)]
        self.engine.analyze_batch(inputs)
        assert len(self.engine.all_meetings()) == 4

    def test_batch_empty_list(self):
        results = self.engine.analyze_batch([])
        assert results == []

    def test_batch_single_item(self):
        results = self.engine.analyze_batch([make_input()])
        assert len(results) == 1

    def test_batch_three_items_sorted(self):
        inputs = [
            make_input(meeting_id="low", duration_minutes=10, demo_shown=False, proposal_sent=False,
                       next_step_agreed=False, talk_ratio_pct=80.0,
                       prospect_asked_questions=False, prospect_requested_pricing=False,
                       prospect_mentioned_timeline=False, prospect_mentioned_budget=False,
                       decision_maker_present=False, exec_sponsor_present=False,
                       attendees_count=1, objections_raised=5),
            make_input(meeting_id="mid", duration_minutes=30, demo_shown=False, proposal_sent=False,
                       next_step_agreed=True, next_step_days_out=7, talk_ratio_pct=50.0,
                       prospect_asked_questions=True, prospect_requested_pricing=False,
                       prospect_mentioned_timeline=False, prospect_mentioned_budget=False,
                       decision_maker_present=False, exec_sponsor_present=False,
                       attendees_count=2, objections_raised=0),
            make_input(meeting_id="high", duration_minutes=90, demo_shown=True, proposal_sent=True,
                       next_step_agreed=True, next_step_days_out=7, talk_ratio_pct=40.0,
                       prospect_asked_questions=True, prospect_requested_pricing=True,
                       prospect_mentioned_timeline=True, prospect_mentioned_budget=True,
                       decision_maker_present=True, exec_sponsor_present=True,
                       attendees_count=5, objections_raised=0),
        ]
        results = self.engine.analyze_batch(inputs)
        scores = [r.quality_score for r in results]
        assert scores == sorted(scores, reverse=True)


# ─── Test Filter Helpers ──────────────────────────────────────────────────────

class TestFilterHelpers:
    def setup_method(self):
        self.engine = MeetingIntelligenceEngine()

    def test_advanced_returns_only_advanced(self):
        self.engine.analyze(make_input(
            next_step_agreed=True,
            prospect_asked_questions=True, prospect_requested_pricing=True,
            prospect_mentioned_timeline=False, prospect_mentioned_budget=False,
            decision_maker_present=False, exec_sponsor_present=False,
            objections_raised=0,
        ))
        self.engine.analyze(make_input(
            next_step_agreed=False,
            prospect_asked_questions=False, prospect_requested_pricing=False,
            prospect_mentioned_timeline=False, prospect_mentioned_budget=False,
            decision_maker_present=False, exec_sponsor_present=False,
            objections_raised=0,
        ))
        advanced = self.engine.advanced_deals()
        assert all(r.meeting_outcome == MeetingOutcome.ADVANCED for r in advanced)

    def test_regressed_returns_only_regressed(self):
        self.engine.analyze(make_input(
            next_step_agreed=False,
            prospect_asked_questions=False, prospect_requested_pricing=False,
            prospect_mentioned_timeline=False, prospect_mentioned_budget=False,
            decision_maker_present=False, exec_sponsor_present=False,
            objections_raised=0,
        ))
        regressed = self.engine.regressed_deals()
        assert all(r.meeting_outcome == MeetingOutcome.REGRESSED for r in regressed)

    def test_needs_immediate_follow_up_returns_immediate_only(self):
        self.engine.analyze(make_input(
            next_step_agreed=False,
            prospect_asked_questions=False, prospect_requested_pricing=False,
            prospect_mentioned_timeline=False, prospect_mentioned_budget=False,
            decision_maker_present=False, exec_sponsor_present=False,
            objections_raised=0,
        ))
        immediate = self.engine.needs_immediate_follow_up()
        assert all(r.follow_up_urgency == FollowUpUrgency.IMMEDIATE for r in immediate)

    def test_with_manager_alerts_returns_only_results_with_alerts(self):
        self.engine.analyze(make_input(
            next_step_agreed=False,
            prospect_asked_questions=False, prospect_requested_pricing=False,
            prospect_mentioned_timeline=False, prospect_mentioned_budget=False,
            decision_maker_present=False, exec_sponsor_present=False,
            objections_raised=0,
        ))
        alerted = self.engine.with_manager_alerts()
        assert all(len(r.manager_alerts) > 0 for r in alerted)

    def test_strong_buying_signals_returns_only_strong(self):
        self.engine.analyze(make_input(
            prospect_asked_questions=True, prospect_requested_pricing=True,
            prospect_mentioned_timeline=True, prospect_mentioned_budget=False,
            decision_maker_present=False, exec_sponsor_present=False,
            objections_raised=0, next_step_agreed=True, next_step_days_out=7,
        ))
        strong = self.engine.strong_buying_signals()
        assert all(r.buying_signal_strength == BuyingSignalStrength.STRONG for r in strong)

    def test_advanced_empty_when_no_advanced(self):
        self.engine.analyze(make_input(
            next_step_agreed=False,
            prospect_asked_questions=False, prospect_requested_pricing=False,
            prospect_mentioned_timeline=False, prospect_mentioned_budget=False,
            decision_maker_present=False, exec_sponsor_present=False,
            objections_raised=0,
        ))
        assert self.engine.advanced_deals() == []

    def test_all_meetings_returns_all(self):
        for i in range(5):
            self.engine.analyze(make_input(meeting_id=f"m{i}"))
        assert len(self.engine.all_meetings()) == 5

    def test_by_outcome_filter(self):
        self.engine.analyze(make_input(
            next_step_agreed=False,
            prospect_asked_questions=True,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=0,
        ))
        no_decision = self.engine.by_outcome(MeetingOutcome.NO_DECISION)
        assert all(r.meeting_outcome == MeetingOutcome.NO_DECISION for r in no_decision)

    def test_by_quality_filter(self):
        self.engine.analyze(make_input(
            prospect_asked_questions=False, prospect_requested_pricing=False,
            prospect_mentioned_timeline=False, prospect_mentioned_budget=False,
            decision_maker_present=False, exec_sponsor_present=False,
            objections_raised=10, next_step_agreed=False,
            talk_ratio_pct=80.0, demo_shown=False, proposal_sent=False,
            duration_minutes=5, attendees_count=1,
        ))
        poor = self.engine.by_quality(MeetingQuality.POOR)
        assert all(r.meeting_quality == MeetingQuality.POOR for r in poor)

    def test_by_urgency_filter(self):
        self.engine.analyze(make_input(
            next_step_agreed=False,
            prospect_asked_questions=False, prospect_requested_pricing=False,
            prospect_mentioned_timeline=False, prospect_mentioned_budget=False,
            decision_maker_present=False, exec_sponsor_present=False,
            objections_raised=0,
        ))
        immediate = self.engine.by_urgency(FollowUpUrgency.IMMEDIATE)
        assert all(r.follow_up_urgency == FollowUpUrgency.IMMEDIATE for r in immediate)


# ─── Test Summary ─────────────────────────────────────────────────────────────

class TestSummary:
    def setup_method(self):
        self.engine = MeetingIntelligenceEngine()

    def test_summary_returns_exactly_10_keys(self):
        self.engine.analyze(make_input())
        s = self.engine.summary()
        assert len(s) == 10

    def test_summary_has_total(self):
        self.engine.analyze(make_input())
        s = self.engine.summary()
        assert "total" in s

    def test_summary_has_outcome_counts(self):
        s = self.engine.summary()
        assert "outcome_counts" in s

    def test_summary_has_quality_counts(self):
        s = self.engine.summary()
        assert "quality_counts" in s

    def test_summary_has_urgency_counts(self):
        s = self.engine.summary()
        assert "urgency_counts" in s

    def test_summary_has_signal_counts(self):
        s = self.engine.summary()
        assert "signal_counts" in s

    def test_summary_has_avg_quality_score(self):
        s = self.engine.summary()
        assert "avg_quality_score" in s

    def test_summary_has_avg_engagement_score(self):
        s = self.engine.summary()
        assert "avg_engagement_score" in s

    def test_summary_has_next_step_rate(self):
        s = self.engine.summary()
        assert "next_step_rate" in s

    def test_summary_has_advancement_rate(self):
        s = self.engine.summary()
        assert "advancement_rate" in s

    def test_summary_has_immediate_follow_up_count(self):
        s = self.engine.summary()
        assert "immediate_follow_up_count" in s

    def test_summary_total_zero_when_empty(self):
        s = self.engine.summary()
        assert s["total"] == 0

    def test_summary_total_correct(self):
        self.engine.analyze(make_input(meeting_id="a"))
        self.engine.analyze(make_input(meeting_id="b"))
        s = self.engine.summary()
        assert s["total"] == 2

    def test_summary_outcome_counts_correct(self):
        self.engine.analyze(make_input(
            next_step_agreed=False,
            prospect_asked_questions=False, prospect_requested_pricing=False,
            prospect_mentioned_timeline=False, prospect_mentioned_budget=False,
            decision_maker_present=False, exec_sponsor_present=False,
            objections_raised=0,
        ))
        s = self.engine.summary()
        assert s["outcome_counts"].get("regressed", 0) == 1

    def test_summary_quality_counts_is_dict(self):
        self.engine.analyze(make_input())
        s = self.engine.summary()
        assert isinstance(s["quality_counts"], dict)

    def test_summary_avg_quality_score_is_numeric(self):
        self.engine.analyze(make_input())
        s = self.engine.summary()
        assert isinstance(s["avg_quality_score"], (int, float))

    def test_summary_avg_engagement_score_is_numeric(self):
        self.engine.analyze(make_input())
        s = self.engine.summary()
        assert isinstance(s["avg_engagement_score"], (int, float))

    def test_summary_next_step_rate_100_when_all_agreed(self):
        self.engine.analyze(make_input(next_step_agreed=True, next_step_days_out=7))
        s = self.engine.summary()
        assert s["next_step_rate"] == 100.0

    def test_summary_next_step_rate_0_when_none_agreed(self):
        self.engine.analyze(make_input(
            next_step_agreed=False,
            prospect_asked_questions=True,
            prospect_requested_pricing=False,
            prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=0,
        ))
        s = self.engine.summary()
        assert s["next_step_rate"] == 0.0

    def test_summary_next_step_rate_50(self):
        self.engine.analyze(make_input(meeting_id="a", next_step_agreed=True, next_step_days_out=7))
        self.engine.analyze(make_input(
            meeting_id="b", next_step_agreed=False,
            prospect_asked_questions=True,
            prospect_requested_pricing=False, prospect_mentioned_timeline=False,
            prospect_mentioned_budget=False, decision_maker_present=False,
            exec_sponsor_present=False, objections_raised=0,
        ))
        s = self.engine.summary()
        assert s["next_step_rate"] == 50.0

    def test_summary_immediate_follow_up_count_correct(self):
        self.engine.analyze(make_input(
            next_step_agreed=False,
            prospect_asked_questions=False, prospect_requested_pricing=False,
            prospect_mentioned_timeline=False, prospect_mentioned_budget=False,
            decision_maker_present=False, exec_sponsor_present=False,
            objections_raised=0,
        ))
        s = self.engine.summary()
        assert s["immediate_follow_up_count"] >= 1

    def test_summary_advancement_rate_0_when_empty(self):
        s = self.engine.summary()
        assert s["advancement_rate"] == 0.0

    def test_summary_avg_quality_score_0_when_empty(self):
        s = self.engine.summary()
        assert s["avg_quality_score"] == 0.0

    def test_summary_avg_engagement_score_0_when_empty(self):
        s = self.engine.summary()
        assert s["avg_engagement_score"] == 0.0


# ─── Test reset() ─────────────────────────────────────────────────────────────

class TestReset:
    def setup_method(self):
        self.engine = MeetingIntelligenceEngine()

    def test_reset_clears_results(self):
        self.engine.analyze(make_input())
        self.engine.reset()
        assert len(self.engine.all_meetings()) == 0

    def test_reset_clears_multiple_results(self):
        for i in range(5):
            self.engine.analyze(make_input(meeting_id=f"m{i}"))
        self.engine.reset()
        assert len(self.engine.all_meetings()) == 0

    def test_reset_makes_summary_empty(self):
        self.engine.analyze(make_input())
        self.engine.reset()
        s = self.engine.summary()
        assert s["total"] == 0

    def test_reset_allows_fresh_analysis(self):
        self.engine.analyze(make_input(meeting_id="old"))
        self.engine.reset()
        self.engine.analyze(make_input(meeting_id="new"))
        meetings = self.engine.all_meetings()
        assert len(meetings) == 1
        assert meetings[0].meeting_id == "new"

    def test_reset_idempotent_on_empty_engine(self):
        self.engine.reset()
        self.engine.reset()
        assert len(self.engine.all_meetings()) == 0

    def test_advanced_empty_after_reset(self):
        self.engine.analyze(make_input(
            next_step_agreed=True,
            prospect_asked_questions=True, prospect_requested_pricing=True,
            prospect_mentioned_timeline=False, prospect_mentioned_budget=False,
            decision_maker_present=False, exec_sponsor_present=False,
            objections_raised=0,
        ))
        self.engine.reset()
        assert self.engine.advanced_deals() == []

    def test_avg_quality_score_zero_after_reset(self):
        self.engine.analyze(make_input())
        self.engine.reset()
        assert self.engine.avg_quality_score() == 0.0

    def test_next_step_rate_zero_after_reset(self):
        self.engine.analyze(make_input(next_step_agreed=True, next_step_days_out=7))
        self.engine.reset()
        assert self.engine.next_step_rate() == 0.0


# ─── Test Aggregate Methods ───────────────────────────────────────────────────

class TestAggregates:
    def setup_method(self):
        self.engine = MeetingIntelligenceEngine()

    def test_avg_quality_score_zero_when_empty(self):
        assert self.engine.avg_quality_score() == 0.0

    def test_avg_engagement_score_zero_when_empty(self):
        assert self.engine.avg_engagement_score() == 0.0

    def test_next_step_rate_zero_when_empty(self):
        assert self.engine.next_step_rate() == 0.0

    def test_advancement_rate_zero_when_empty(self):
        assert self.engine.advancement_rate() == 0.0

    def test_avg_quality_score_is_numeric(self):
        self.engine.analyze(make_input())
        assert isinstance(self.engine.avg_quality_score(), (int, float))

    def test_avg_engagement_score_is_numeric(self):
        self.engine.analyze(make_input())
        assert isinstance(self.engine.avg_engagement_score(), (int, float))

    def test_advancement_rate_100_when_all_advanced(self):
        self.engine.analyze(make_input(
            next_step_agreed=True,
            prospect_asked_questions=True, prospect_requested_pricing=True,
            prospect_mentioned_timeline=False, prospect_mentioned_budget=False,
            decision_maker_present=False, exec_sponsor_present=False,
            objections_raised=0,
        ))
        assert self.engine.advancement_rate() == 100.0

    def test_next_step_rate_100_when_all_agreed(self):
        self.engine.analyze(make_input(next_step_agreed=True, next_step_days_out=5))
        assert self.engine.next_step_rate() == 100.0

    def test_avg_quality_score_average_of_two(self):
        r1 = self.engine.analyze(make_input(meeting_id="a"))
        r2 = self.engine.analyze(make_input(meeting_id="b",
            prospect_asked_questions=False, prospect_requested_pricing=False,
            prospect_mentioned_timeline=False, prospect_mentioned_budget=False,
            decision_maker_present=False, exec_sponsor_present=False,
            objections_raised=5, next_step_agreed=False,
            talk_ratio_pct=80.0, demo_shown=False, proposal_sent=False,
            duration_minutes=5, attendees_count=1,
        ))
        expected = round((r1.quality_score + r2.quality_score) / 2, 1)
        assert self.engine.avg_quality_score() == expected


# ─── Test Edge Cases ──────────────────────────────────────────────────────────

class TestEdgeCases:
    def setup_method(self):
        self.engine = MeetingIntelligenceEngine()

    def test_next_step_days_out_none_when_not_agreed(self):
        inp = make_input(next_step_agreed=False, next_step_days_out=None)
        result = self.engine.analyze(inp)
        assert result.next_step_days_out is None

    def test_zero_duration_no_duration_pts(self):
        inp = make_input(duration_minutes=0, attendees_count=1,
                         next_step_agreed=False, demo_shown=False, proposal_sent=False,
                         prospect_asked_questions=False, prospect_requested_pricing=False,
                         prospect_mentioned_timeline=False, prospect_mentioned_budget=False,
                         decision_maker_present=False, exec_sponsor_present=False,
                         objections_raised=0, talk_ratio_pct=80.0)
        result = self.engine.analyze(inp)
        assert result.quality_score == 0.0

    def test_zero_objections_zero_signals_no_next_step_is_regressed(self):
        inp = make_input(
            next_step_agreed=False,
            prospect_asked_questions=False, prospect_requested_pricing=False,
            prospect_mentioned_timeline=False, prospect_mentioned_budget=False,
            decision_maker_present=False, exec_sponsor_present=False,
            objections_raised=0,
        )
        result = self.engine.analyze(inp)
        assert result.meeting_outcome == MeetingOutcome.REGRESSED

    def test_previous_meetings_count_zero_no_repeat_alert(self):
        inp = make_input(previous_meetings_count=0)
        result = self.engine.analyze(inp)
        assert not any("médiocre" in a for a in result.manager_alerts)

    def test_talk_ratio_exactly_50_gets_talk_pts(self):
        r_50 = self.engine.analyze(make_input(talk_ratio_pct=50.0,
            prospect_asked_questions=False, prospect_requested_pricing=False,
            prospect_mentioned_timeline=False, prospect_mentioned_budget=False,
            decision_maker_present=False, exec_sponsor_present=False,
            objections_raised=0, next_step_agreed=False, demo_shown=False,
            proposal_sent=False, duration_minutes=60, attendees_count=2))
        self.engine.reset()
        r_51 = self.engine.analyze(make_input(talk_ratio_pct=51.0,
            prospect_asked_questions=False, prospect_requested_pricing=False,
            prospect_mentioned_timeline=False, prospect_mentioned_budget=False,
            decision_maker_present=False, exec_sponsor_present=False,
            objections_raised=0, next_step_agreed=False, demo_shown=False,
            proposal_sent=False, duration_minutes=60, attendees_count=2))
        assert r_50.quality_score > r_51.quality_score

    def test_references_offered_field_stored_in_input(self):
        inp = make_input(references_offered=True)
        assert inp.references_offered is True

    def test_days_since_last_meeting_stored(self):
        inp = make_input(days_since_last_meeting=30)
        assert inp.days_since_last_meeting == 30

    def test_to_dict_enum_values_are_strings_not_enums(self):
        result = self.engine.analyze(make_input())
        d = result.to_dict()
        assert isinstance(d["meeting_outcome"], str)
        assert isinstance(d["meeting_quality"], str)
        assert isinstance(d["buying_signal_strength"], str)
        assert isinstance(d["follow_up_urgency"], str)

    def test_batch_returns_same_count_as_input(self):
        inputs = [make_input(meeting_id=f"m{i}") for i in range(7)]
        results = self.engine.analyze_batch(inputs)
        assert len(results) == 7

    def test_engine_initial_state_empty(self):
        fresh = MeetingIntelligenceEngine()
        assert len(fresh.all_meetings()) == 0
        assert fresh.avg_quality_score() == 0.0

    def test_strong_signal_but_2_objections_not_strong(self):
        inp = make_input(
            prospect_asked_questions=True,
            prospect_requested_pricing=True,
            prospect_mentioned_timeline=True,
            prospect_mentioned_budget=False,
            decision_maker_present=False,
            exec_sponsor_present=False,
            objections_raised=2,
        )
        result = self.engine.analyze(inp)
        assert result.buying_signal_strength != BuyingSignalStrength.STRONG

    def test_quality_score_exact_boundaries(self):
        score = self.engine._meeting_quality(74.9)
        assert score == MeetingQuality.GOOD
        self.engine.reset()
        score2 = self.engine._meeting_quality(75.0)
        assert score2 == MeetingQuality.EXCELLENT
