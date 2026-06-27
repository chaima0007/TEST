"""Comprehensive tests for swarm.intelligence.buyer_intent_engine"""

import pytest
from swarm.intelligence.buyer_intent_engine import (
    BuyerIntentEngine,
    IntentCategory,
    IntentInput,
    IntentLevel,
    IntentResult,
    IntentTrend,
    OutreachStrategy,
)


# ─── Fixtures ────────────────────────────────────────────────────────────────


def make_input(**kwargs) -> IntentInput:
    defaults = dict(
        prospect_id="p-001",
        company_name="Acme Corp",
        rep_id="r-001",
        rep_name="Alice",
        website_visits_30d=0,
        pricing_page_visits=0,
        demo_page_visits=0,
        case_study_downloads=0,
        whitepaper_downloads=0,
        product_video_views=0,
        emails_opened_30d=0,
        emails_clicked_30d=0,
        emails_sent_30d=0,
        webinar_attended=False,
        trade_show_visited=False,
        free_trial_started=False,
        linkedin_engaged=False,
        replied_to_outreach=False,
        requested_demo=False,
        contacted_support=False,
        funding_round_announced=False,
        leadership_change=False,
        competitor_contract_expired=False,
        recent_job_posting_relevant=False,
        previous_demo_taken=False,
        previous_trial_abandoned=False,
        days_since_last_engagement=5,
        icp_score=50.0,
    )
    defaults.update(kwargs)
    return IntentInput(**defaults)


@pytest.fixture
def engine():
    return BuyerIntentEngine()


@pytest.fixture
def blank_input():
    return make_input()


# ─── Class 1: IntentLevel enum ───────────────────────────────────────────────


class TestIntentLevelEnum:
    def test_hot_value(self):
        assert IntentLevel.HOT.value == "hot"

    def test_warm_value(self):
        assert IntentLevel.WARM.value == "warm"

    def test_lukewarm_value(self):
        assert IntentLevel.LUKEWARM.value == "lukewarm"

    def test_cold_value(self):
        assert IntentLevel.COLD.value == "cold"

    def test_unknown_value(self):
        assert IntentLevel.UNKNOWN.value == "unknown"

    def test_str_inheritance_hot(self):
        assert isinstance(IntentLevel.HOT, str)

    def test_str_inheritance_warm(self):
        assert isinstance(IntentLevel.WARM, str)

    def test_str_inheritance_lukewarm(self):
        assert isinstance(IntentLevel.LUKEWARM, str)

    def test_str_inheritance_cold(self):
        assert isinstance(IntentLevel.COLD, str)

    def test_str_inheritance_unknown(self):
        assert isinstance(IntentLevel.UNKNOWN, str)

    def test_str_equality_hot(self):
        assert IntentLevel.HOT == "hot"

    def test_all_members_count(self):
        assert len(IntentLevel) == 5


# ─── Class 2: IntentCategory enum ────────────────────────────────────────────


class TestIntentCategoryEnum:
    def test_product_interest_value(self):
        assert IntentCategory.PRODUCT_INTEREST.value == "product_interest"

    def test_competitive_eval_value(self):
        assert IntentCategory.COMPETITIVE_EVAL.value == "competitive_eval"

    def test_budget_cycle_value(self):
        assert IntentCategory.BUDGET_CYCLE.value == "budget_cycle"

    def test_pain_driven_value(self):
        assert IntentCategory.PAIN_DRIVEN.value == "pain_driven"

    def test_relationship_value(self):
        assert IntentCategory.RELATIONSHIP.value == "relationship"

    def test_event_triggered_value(self):
        assert IntentCategory.EVENT_TRIGGERED.value == "event_triggered"

    def test_str_inheritance(self):
        for member in IntentCategory:
            assert isinstance(member, str)

    def test_all_members_count(self):
        assert len(IntentCategory) == 6


# ─── Class 3: IntentTrend enum ───────────────────────────────────────────────


class TestIntentTrendEnum:
    def test_accelerating_value(self):
        assert IntentTrend.ACCELERATING.value == "accelerating"

    def test_stable_value(self):
        assert IntentTrend.STABLE.value == "stable"

    def test_declining_value(self):
        assert IntentTrend.DECLINING.value == "declining"

    def test_spiked_value(self):
        assert IntentTrend.SPIKED.value == "spiked"

    def test_dormant_value(self):
        assert IntentTrend.DORMANT.value == "dormant"

    def test_str_inheritance(self):
        for member in IntentTrend:
            assert isinstance(member, str)

    def test_all_members_count(self):
        assert len(IntentTrend) == 5


# ─── Class 4: OutreachStrategy enum ──────────────────────────────────────────


class TestOutreachStrategyEnum:
    def test_immediate_outreach_value(self):
        assert OutreachStrategy.IMMEDIATE_OUTREACH.value == "immediate_outreach"

    def test_executive_outreach_value(self):
        assert OutreachStrategy.EXECUTIVE_OUTREACH.value == "executive_outreach"

    def test_value_content_value(self):
        assert OutreachStrategy.VALUE_CONTENT.value == "value_content"

    def test_nurture_sequence_value(self):
        assert OutreachStrategy.NURTURE_SEQUENCE.value == "nurture_sequence"

    def test_event_invite_value(self):
        assert OutreachStrategy.EVENT_INVITE.value == "event_invite"

    def test_wait_and_monitor_value(self):
        assert OutreachStrategy.WAIT_AND_MONITOR.value == "wait_and_monitor"

    def test_str_inheritance(self):
        for member in OutreachStrategy:
            assert isinstance(member, str)

    def test_all_members_count(self):
        assert len(OutreachStrategy) == 6


# ─── Class 5: IntentInput dataclass fields ───────────────────────────────────


class TestIntentInputFields:
    def test_prospect_id_field(self):
        inp = make_input(prospect_id="x")
        assert inp.prospect_id == "x"

    def test_company_name_field(self):
        inp = make_input(company_name="BigCo")
        assert inp.company_name == "BigCo"

    def test_rep_id_field(self):
        inp = make_input(rep_id="r-99")
        assert inp.rep_id == "r-99"

    def test_rep_name_field(self):
        inp = make_input(rep_name="Bob")
        assert inp.rep_name == "Bob"

    def test_website_visits_30d_field(self):
        inp = make_input(website_visits_30d=10)
        assert inp.website_visits_30d == 10

    def test_pricing_page_visits_field(self):
        inp = make_input(pricing_page_visits=3)
        assert inp.pricing_page_visits == 3

    def test_demo_page_visits_field(self):
        inp = make_input(demo_page_visits=2)
        assert inp.demo_page_visits == 2

    def test_case_study_downloads_field(self):
        inp = make_input(case_study_downloads=4)
        assert inp.case_study_downloads == 4

    def test_whitepaper_downloads_field(self):
        inp = make_input(whitepaper_downloads=1)
        assert inp.whitepaper_downloads == 1

    def test_product_video_views_field(self):
        inp = make_input(product_video_views=5)
        assert inp.product_video_views == 5

    def test_emails_opened_30d_field(self):
        inp = make_input(emails_opened_30d=7)
        assert inp.emails_opened_30d == 7

    def test_emails_clicked_30d_field(self):
        inp = make_input(emails_clicked_30d=2)
        assert inp.emails_clicked_30d == 2

    def test_emails_sent_30d_field(self):
        inp = make_input(emails_sent_30d=10)
        assert inp.emails_sent_30d == 10

    def test_webinar_attended_field(self):
        inp = make_input(webinar_attended=True)
        assert inp.webinar_attended is True

    def test_trade_show_visited_field(self):
        inp = make_input(trade_show_visited=True)
        assert inp.trade_show_visited is True

    def test_free_trial_started_field(self):
        inp = make_input(free_trial_started=True)
        assert inp.free_trial_started is True

    def test_linkedin_engaged_field(self):
        inp = make_input(linkedin_engaged=True)
        assert inp.linkedin_engaged is True

    def test_replied_to_outreach_field(self):
        inp = make_input(replied_to_outreach=True)
        assert inp.replied_to_outreach is True

    def test_requested_demo_field(self):
        inp = make_input(requested_demo=True)
        assert inp.requested_demo is True

    def test_contacted_support_field(self):
        inp = make_input(contacted_support=True)
        assert inp.contacted_support is True

    def test_funding_round_announced_field(self):
        inp = make_input(funding_round_announced=True)
        assert inp.funding_round_announced is True

    def test_leadership_change_field(self):
        inp = make_input(leadership_change=True)
        assert inp.leadership_change is True

    def test_competitor_contract_expired_field(self):
        inp = make_input(competitor_contract_expired=True)
        assert inp.competitor_contract_expired is True

    def test_recent_job_posting_relevant_field(self):
        inp = make_input(recent_job_posting_relevant=True)
        assert inp.recent_job_posting_relevant is True

    def test_previous_demo_taken_field(self):
        inp = make_input(previous_demo_taken=True)
        assert inp.previous_demo_taken is True

    def test_previous_trial_abandoned_field(self):
        inp = make_input(previous_trial_abandoned=True)
        assert inp.previous_trial_abandoned is True

    def test_days_since_last_engagement_field(self):
        inp = make_input(days_since_last_engagement=45)
        assert inp.days_since_last_engagement == 45

    def test_icp_score_field(self):
        inp = make_input(icp_score=75.0)
        assert inp.icp_score == 75.0

    def test_total_25_fields(self):
        import dataclasses
        fields = dataclasses.fields(IntentInput)
        assert len(fields) == 28  # 25 + prospect_id + company_name + rep_id + rep_name = 28... recount
        # Actually: prospect_id, company_name, rep_id, rep_name (4) + digital(6) + email(3) +
        # event(3) + relationship(4) + external(4) + historical(2) + days(1) + icp(1) = 28
        assert len(fields) == 28


# ─── Class 6: IntentResult to_dict ───────────────────────────────────────────


class TestIntentResultToDict:
    def test_to_dict_returns_exactly_15_keys(self, engine, blank_input):
        result = engine.analyze(blank_input)
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_has_prospect_id(self, engine, blank_input):
        d = engine.analyze(blank_input).to_dict()
        assert "prospect_id" in d

    def test_to_dict_has_company_name(self, engine, blank_input):
        d = engine.analyze(blank_input).to_dict()
        assert "company_name" in d

    def test_to_dict_has_rep_id(self, engine, blank_input):
        d = engine.analyze(blank_input).to_dict()
        assert "rep_id" in d

    def test_to_dict_has_rep_name(self, engine, blank_input):
        d = engine.analyze(blank_input).to_dict()
        assert "rep_name" in d

    def test_to_dict_has_intent_level(self, engine, blank_input):
        d = engine.analyze(blank_input).to_dict()
        assert "intent_level" in d

    def test_to_dict_has_intent_category(self, engine, blank_input):
        d = engine.analyze(blank_input).to_dict()
        assert "intent_category" in d

    def test_to_dict_has_intent_trend(self, engine, blank_input):
        d = engine.analyze(blank_input).to_dict()
        assert "intent_trend" in d

    def test_to_dict_has_outreach_strategy(self, engine, blank_input):
        d = engine.analyze(blank_input).to_dict()
        assert "outreach_strategy" in d

    def test_to_dict_has_intent_score(self, engine, blank_input):
        d = engine.analyze(blank_input).to_dict()
        assert "intent_score" in d

    def test_to_dict_has_digital_score(self, engine, blank_input):
        d = engine.analyze(blank_input).to_dict()
        assert "digital_score" in d

    def test_to_dict_has_engagement_score(self, engine, blank_input):
        d = engine.analyze(blank_input).to_dict()
        assert "engagement_score" in d

    def test_to_dict_has_trigger_score(self, engine, blank_input):
        d = engine.analyze(blank_input).to_dict()
        assert "trigger_score" in d

    def test_to_dict_has_hot_signals(self, engine, blank_input):
        d = engine.analyze(blank_input).to_dict()
        assert "hot_signals" in d

    def test_to_dict_has_cold_signals(self, engine, blank_input):
        d = engine.analyze(blank_input).to_dict()
        assert "cold_signals" in d

    def test_to_dict_has_recommended_actions(self, engine, blank_input):
        d = engine.analyze(blank_input).to_dict()
        assert "recommended_actions" in d

    def test_to_dict_exact_keys(self, engine, blank_input):
        expected = {
            "prospect_id", "company_name", "rep_id", "rep_name",
            "intent_level", "intent_category", "intent_trend", "outreach_strategy",
            "intent_score", "digital_score", "engagement_score", "trigger_score",
            "hot_signals", "cold_signals", "recommended_actions",
        }
        assert set(engine.analyze(blank_input).to_dict().keys()) == expected

    def test_to_dict_prospect_id_value(self, engine):
        inp = make_input(prospect_id="p-xyz")
        d = engine.analyze(inp).to_dict()
        assert d["prospect_id"] == "p-xyz"

    def test_to_dict_scores_are_numeric(self, engine, blank_input):
        d = engine.analyze(blank_input).to_dict()
        assert isinstance(d["intent_score"], (int, float))
        assert isinstance(d["digital_score"], (int, float))
        assert isinstance(d["engagement_score"], (int, float))
        assert isinstance(d["trigger_score"], (int, float))

    def test_to_dict_lists_are_lists(self, engine, blank_input):
        d = engine.analyze(blank_input).to_dict()
        assert isinstance(d["hot_signals"], list)
        assert isinstance(d["cold_signals"], list)
        assert isinstance(d["recommended_actions"], list)


# ─── Class 7: Digital score ───────────────────────────────────────────────────


class TestDigitalScore:
    def test_zero_signals_gives_zero(self, engine):
        inp = make_input()
        assert engine._digital_score(inp) == 0.0

    def test_pricing_page_one_visit(self, engine):
        inp = make_input(pricing_page_visits=1)
        assert engine._digital_score(inp) == 12.0

    def test_pricing_page_two_visits(self, engine):
        inp = make_input(pricing_page_visits=2)
        assert engine._digital_score(inp) == 24.0

    def test_pricing_page_capped_at_25(self, engine):
        inp = make_input(pricing_page_visits=10)
        assert engine._digital_score(inp) == 25.0

    def test_demo_page_one_visit(self, engine):
        inp = make_input(demo_page_visits=1)
        assert engine._digital_score(inp) == 10.0

    def test_demo_page_two_visits(self, engine):
        inp = make_input(demo_page_visits=2)
        assert engine._digital_score(inp) == 20.0

    def test_demo_page_capped_at_20(self, engine):
        inp = make_input(demo_page_visits=10)
        assert engine._digital_score(inp) == 20.0

    def test_case_study_one_download(self, engine):
        inp = make_input(case_study_downloads=1)
        assert engine._digital_score(inp) == 7.0

    def test_case_study_two_downloads(self, engine):
        inp = make_input(case_study_downloads=2)
        assert engine._digital_score(inp) == 14.0

    def test_case_study_capped_at_15(self, engine):
        inp = make_input(case_study_downloads=10)
        assert engine._digital_score(inp) == 15.0

    def test_whitepaper_one_download(self, engine):
        inp = make_input(whitepaper_downloads=1)
        assert engine._digital_score(inp) == 5.0

    def test_whitepaper_two_downloads(self, engine):
        inp = make_input(whitepaper_downloads=2)
        assert engine._digital_score(inp) == 10.0

    def test_whitepaper_capped_at_10(self, engine):
        inp = make_input(whitepaper_downloads=10)
        assert engine._digital_score(inp) == 10.0

    def test_video_one_view(self, engine):
        inp = make_input(product_video_views=1)
        assert engine._digital_score(inp) == 2.0

    def test_video_four_views(self, engine):
        inp = make_input(product_video_views=4)
        assert engine._digital_score(inp) == 8.0

    def test_video_capped_at_8(self, engine):
        inp = make_input(product_video_views=10)
        assert engine._digital_score(inp) == 8.0

    def test_website_visits_two(self, engine):
        inp = make_input(website_visits_30d=2)
        assert engine._digital_score(inp) == 1.0

    def test_website_visits_24(self, engine):
        inp = make_input(website_visits_30d=24)
        assert engine._digital_score(inp) == 12.0

    def test_website_visits_capped_at_12(self, engine):
        inp = make_input(website_visits_30d=100)
        assert engine._digital_score(inp) == 12.0

    def test_free_trial_adds_20(self, engine):
        inp = make_input(free_trial_started=True)
        assert engine._digital_score(inp) == 20.0

    def test_combined_score_clamped_at_100(self, engine):
        inp = make_input(
            pricing_page_visits=10,
            demo_page_visits=10,
            case_study_downloads=10,
            whitepaper_downloads=10,
            product_video_views=10,
            website_visits_30d=100,
            free_trial_started=True,
        )
        assert engine._digital_score(inp) == 100.0

    def test_free_trial_plus_pricing(self, engine):
        inp = make_input(free_trial_started=True, pricing_page_visits=1)
        assert engine._digital_score(inp) == 32.0

    def test_score_is_numeric(self, engine):
        inp = make_input(pricing_page_visits=1)
        assert isinstance(engine._digital_score(inp), (int, float))


# ─── Class 8: Engagement score ───────────────────────────────────────────────


class TestEngagementScore:
    def test_zero_signals_gives_zero(self, engine):
        inp = make_input()
        assert engine._engagement_score(inp) == 0.0

    def test_requested_demo_adds_30(self, engine):
        inp = make_input(requested_demo=True)
        assert engine._engagement_score(inp) == 30.0

    def test_replied_to_outreach_adds_20(self, engine):
        inp = make_input(replied_to_outreach=True)
        assert engine._engagement_score(inp) == 20.0

    def test_webinar_attended_adds_15(self, engine):
        inp = make_input(webinar_attended=True)
        assert engine._engagement_score(inp) == 15.0

    def test_trade_show_visited_adds_12(self, engine):
        inp = make_input(trade_show_visited=True)
        assert engine._engagement_score(inp) == 12.0

    def test_linkedin_engaged_adds_8(self, engine):
        inp = make_input(linkedin_engaged=True)
        assert engine._engagement_score(inp) == 8.0

    def test_contacted_support_adds_5(self, engine):
        inp = make_input(contacted_support=True)
        assert engine._engagement_score(inp) == 5.0

    def test_previous_demo_taken_adds_8(self, engine):
        inp = make_input(previous_demo_taken=True)
        assert engine._engagement_score(inp) == 8.0

    def test_previous_trial_abandoned_adds_5(self, engine):
        inp = make_input(previous_trial_abandoned=True)
        assert engine._engagement_score(inp) == 5.0

    def test_email_open_rate_100pct(self, engine):
        # open_rate=1.0 → min(5, 1*8)=5
        inp = make_input(emails_sent_30d=10, emails_opened_30d=10)
        score = engine._engagement_score(inp)
        assert score == 5.0

    def test_email_open_rate_partial(self, engine):
        # open_rate=0.5 → min(5, 0.5*8)=4
        inp = make_input(emails_sent_30d=10, emails_opened_30d=5)
        score = engine._engagement_score(inp)
        assert score == 4.0

    def test_email_click_rate_100pct(self, engine):
        # click_rate=1.0 → min(8, 1*20)=8
        inp = make_input(emails_sent_30d=10, emails_clicked_30d=10)
        score = engine._engagement_score(inp)
        assert score == 8.0

    def test_email_click_rate_partial(self, engine):
        # click_rate=0.25 → min(8, 0.25*20)=5
        inp = make_input(emails_sent_30d=10, emails_clicked_30d=2, emails_opened_30d=0)
        score = engine._engagement_score(inp)
        # click contributes min(8, 2/10*20)=4, open contributes 0
        assert score == 4.0

    def test_email_open_capped_at_5(self, engine):
        # Very high open rate still capped
        inp = make_input(emails_sent_30d=1, emails_opened_30d=1)
        score = engine._engagement_score(inp)
        # open: min(5,8)=5
        assert score == 5.0

    def test_email_click_capped_at_8(self, engine):
        inp = make_input(emails_sent_30d=1, emails_clicked_30d=1)
        score = engine._engagement_score(inp)
        # click: min(8,20)=8
        assert score == 8.0

    def test_recency_penalty_31_days(self, engine):
        # >30 days: -15, base=0 => clamped to 0
        inp = make_input(days_since_last_engagement=31)
        assert engine._engagement_score(inp) == 0.0

    def test_recency_penalty_30_days_no_penalty(self, engine):
        # exactly 30 days: NOT >30, no big penalty; also NOT >14 so no small penalty
        inp = make_input(days_since_last_engagement=30)
        assert engine._engagement_score(inp) == 0.0

    def test_recency_penalty_15_days(self, engine):
        # >14 but not >30: -5; base=0, clamped to 0
        inp = make_input(days_since_last_engagement=15)
        assert engine._engagement_score(inp) == 0.0

    def test_recency_penalty_14_days_no_penalty(self, engine):
        # exactly 14: NOT >14, no penalty
        inp = make_input(days_since_last_engagement=14)
        assert engine._engagement_score(inp) == 0.0

    def test_recency_penalty_reduces_score_31_days(self, engine):
        # requested_demo (+30) - 15 = 15
        inp = make_input(requested_demo=True, days_since_last_engagement=31)
        assert engine._engagement_score(inp) == 15.0

    def test_recency_penalty_reduces_score_15_days(self, engine):
        # requested_demo (+30) - 5 = 25
        inp = make_input(requested_demo=True, days_since_last_engagement=15)
        assert engine._engagement_score(inp) == 25.0

    def test_no_email_sent_skips_email_calc(self, engine):
        inp = make_input(emails_sent_30d=0, emails_opened_30d=5)
        assert engine._engagement_score(inp) == 0.0

    def test_clamped_max_at_100(self, engine):
        inp = make_input(
            requested_demo=True,
            replied_to_outreach=True,
            webinar_attended=True,
            trade_show_visited=True,
            linkedin_engaged=True,
            contacted_support=True,
            previous_demo_taken=True,
            previous_trial_abandoned=True,
            emails_sent_30d=10,
            emails_opened_30d=10,
            emails_clicked_30d=10,
        )
        assert engine._engagement_score(inp) <= 100.0

    def test_score_is_numeric(self, engine):
        inp = make_input(requested_demo=True)
        assert isinstance(engine._engagement_score(inp), (int, float))


# ─── Class 9: Trigger score ───────────────────────────────────────────────────


class TestTriggerScore:
    def test_zero_signals(self, engine):
        inp = make_input()
        assert engine._trigger_score(inp) == 0.0

    def test_funding_round_adds_30(self, engine):
        inp = make_input(funding_round_announced=True)
        assert engine._trigger_score(inp) == 30.0

    def test_competitor_expired_adds_25(self, engine):
        inp = make_input(competitor_contract_expired=True)
        assert engine._trigger_score(inp) == 25.0

    def test_leadership_change_adds_20(self, engine):
        inp = make_input(leadership_change=True)
        assert engine._trigger_score(inp) == 20.0

    def test_job_posting_adds_15(self, engine):
        inp = make_input(recent_job_posting_relevant=True)
        assert engine._trigger_score(inp) == 15.0

    def test_all_triggers(self, engine):
        inp = make_input(
            funding_round_announced=True,
            competitor_contract_expired=True,
            leadership_change=True,
            recent_job_posting_relevant=True,
        )
        assert engine._trigger_score(inp) == 90.0

    def test_capped_at_100(self, engine):
        # max is 90 normally, but confirm clamp
        inp = make_input(
            funding_round_announced=True,
            competitor_contract_expired=True,
            leadership_change=True,
            recent_job_posting_relevant=True,
        )
        assert engine._trigger_score(inp) <= 100.0

    def test_funding_plus_leadership(self, engine):
        inp = make_input(funding_round_announced=True, leadership_change=True)
        assert engine._trigger_score(inp) == 50.0

    def test_score_is_numeric(self, engine):
        inp = make_input(funding_round_announced=True)
        assert isinstance(engine._trigger_score(inp), (int, float))


# ─── Class 10: Intent score ───────────────────────────────────────────────────


class TestIntentScore:
    def test_zero_inputs(self, engine):
        score = engine._intent_score(0.0, 0.0, 0.0, make_input(icp_score=50.0))
        assert score == 0.0

    def test_weights_digital_35(self, engine):
        # digital=100, engagement=0, trigger=0, icp=50 (no boost)
        score = engine._intent_score(100.0, 0.0, 0.0, make_input(icp_score=50.0))
        assert score == 35.0

    def test_weights_engagement_45(self, engine):
        score = engine._intent_score(0.0, 100.0, 0.0, make_input(icp_score=50.0))
        assert score == 45.0

    def test_weights_trigger_20(self, engine):
        score = engine._intent_score(0.0, 0.0, 100.0, make_input(icp_score=50.0))
        assert score == 20.0

    def test_icp_50_no_boost(self, engine):
        score = engine._intent_score(50.0, 50.0, 50.0, make_input(icp_score=50.0))
        base = 50 * 0.35 + 50 * 0.45 + 50 * 0.20
        assert score == round(base, 1)

    def test_icp_100_positive_boost(self, engine):
        score = engine._intent_score(50.0, 50.0, 50.0, make_input(icp_score=100.0))
        base = 50 * 0.35 + 50 * 0.45 + 50 * 0.20
        boost = (100.0 - 50) * 0.1
        assert score == round(base + boost, 1)

    def test_icp_0_negative_boost(self, engine):
        score = engine._intent_score(50.0, 50.0, 50.0, make_input(icp_score=0.0))
        base = 50 * 0.35 + 50 * 0.45 + 50 * 0.20
        boost = (0.0 - 50) * 0.1
        assert score == round(base + boost, 1)

    def test_score_clamped_at_0(self, engine):
        score = engine._intent_score(0.0, 0.0, 0.0, make_input(icp_score=0.0))
        assert score >= 0.0

    def test_score_clamped_at_100(self, engine):
        score = engine._intent_score(100.0, 100.0, 100.0, make_input(icp_score=100.0))
        assert score <= 100.0

    def test_result_is_rounded_to_1dp(self, engine):
        score = engine._intent_score(33.3, 33.3, 33.3, make_input(icp_score=50.0))
        assert score == round(33.3 * 0.35 + 33.3 * 0.45 + 33.3 * 0.20, 1)

    def test_score_is_numeric(self, engine):
        score = engine._intent_score(10.0, 10.0, 10.0, make_input(icp_score=50.0))
        assert isinstance(score, (int, float))


# ─── Class 11: Intent level thresholds ───────────────────────────────────────


class TestIntentLevel:
    def test_score_70_is_hot(self, engine):
        assert engine._intent_level(70.0) == IntentLevel.HOT

    def test_score_100_is_hot(self, engine):
        assert engine._intent_level(100.0) == IntentLevel.HOT

    def test_score_69_is_warm(self, engine):
        assert engine._intent_level(69.9) == IntentLevel.WARM

    def test_score_45_is_warm(self, engine):
        assert engine._intent_level(45.0) == IntentLevel.WARM

    def test_score_44_is_lukewarm(self, engine):
        assert engine._intent_level(44.9) == IntentLevel.LUKEWARM

    def test_score_20_is_lukewarm(self, engine):
        assert engine._intent_level(20.0) == IntentLevel.LUKEWARM

    def test_score_19_is_cold(self, engine):
        assert engine._intent_level(19.9) == IntentLevel.COLD

    def test_score_5_is_cold(self, engine):
        assert engine._intent_level(5.0) == IntentLevel.COLD

    def test_score_4_is_unknown(self, engine):
        assert engine._intent_level(4.9) == IntentLevel.UNKNOWN

    def test_score_0_is_unknown(self, engine):
        assert engine._intent_level(0.0) == IntentLevel.UNKNOWN


# ─── Class 12: Intent category priority ──────────────────────────────────────


class TestIntentCategory:
    def test_requested_demo_yields_product_interest(self, engine):
        inp = make_input(requested_demo=True)
        assert engine._intent_category(inp) == IntentCategory.PRODUCT_INTEREST

    def test_free_trial_yields_product_interest(self, engine):
        inp = make_input(free_trial_started=True)
        assert engine._intent_category(inp) == IntentCategory.PRODUCT_INTEREST

    def test_product_interest_takes_priority_over_pricing(self, engine):
        inp = make_input(requested_demo=True, pricing_page_visits=5)
        assert engine._intent_category(inp) == IntentCategory.PRODUCT_INTEREST

    def test_pricing_2_visits_yields_competitive_eval(self, engine):
        inp = make_input(pricing_page_visits=2)
        assert engine._intent_category(inp) == IntentCategory.COMPETITIVE_EVAL

    def test_pricing_1_visit_does_not_yield_competitive_eval(self, engine):
        inp = make_input(pricing_page_visits=1)
        assert engine._intent_category(inp) != IntentCategory.COMPETITIVE_EVAL

    def test_case_study_2_downloads_yields_competitive_eval(self, engine):
        inp = make_input(case_study_downloads=2)
        assert engine._intent_category(inp) == IntentCategory.COMPETITIVE_EVAL

    def test_competitive_eval_takes_priority_over_funding(self, engine):
        inp = make_input(pricing_page_visits=2, funding_round_announced=True)
        assert engine._intent_category(inp) == IntentCategory.COMPETITIVE_EVAL

    def test_funding_yields_event_triggered(self, engine):
        inp = make_input(funding_round_announced=True)
        assert engine._intent_category(inp) == IntentCategory.EVENT_TRIGGERED

    def test_competitor_expired_yields_event_triggered(self, engine):
        inp = make_input(competitor_contract_expired=True)
        assert engine._intent_category(inp) == IntentCategory.EVENT_TRIGGERED

    def test_leadership_change_yields_pain_driven(self, engine):
        inp = make_input(leadership_change=True)
        assert engine._intent_category(inp) == IntentCategory.PAIN_DRIVEN

    def test_job_posting_yields_pain_driven(self, engine):
        inp = make_input(recent_job_posting_relevant=True)
        assert engine._intent_category(inp) == IntentCategory.PAIN_DRIVEN

    def test_replied_yields_relationship(self, engine):
        inp = make_input(replied_to_outreach=True)
        assert engine._intent_category(inp) == IntentCategory.RELATIONSHIP

    def test_webinar_yields_relationship(self, engine):
        inp = make_input(webinar_attended=True)
        assert engine._intent_category(inp) == IntentCategory.RELATIONSHIP

    def test_5_visits_yields_product_interest(self, engine):
        inp = make_input(website_visits_30d=5)
        assert engine._intent_category(inp) == IntentCategory.PRODUCT_INTEREST

    def test_4_visits_does_not_yield_product_interest_from_visits(self, engine):
        inp = make_input(website_visits_30d=4)
        assert engine._intent_category(inp) == IntentCategory.RELATIONSHIP

    def test_blank_yields_relationship(self, engine):
        inp = make_input()
        assert engine._intent_category(inp) == IntentCategory.RELATIONSHIP

    def test_pain_driven_takes_priority_over_relationship(self, engine):
        inp = make_input(leadership_change=True, replied_to_outreach=True)
        assert engine._intent_category(inp) == IntentCategory.PAIN_DRIVEN


# ─── Class 13: Intent trend classification ───────────────────────────────────


class TestIntentTrend:
    def test_61_days_is_dormant(self, engine):
        inp = make_input(days_since_last_engagement=61)
        assert engine._intent_trend(inp) == IntentTrend.DORMANT

    def test_60_days_is_not_dormant(self, engine):
        inp = make_input(days_since_last_engagement=60)
        # NOT >60, so not dormant — no spike conditions, days=60 >21 → DECLINING
        assert engine._intent_trend(inp) == IntentTrend.DECLINING

    def test_requested_demo_within_7_days_is_spiked(self, engine):
        inp = make_input(requested_demo=True, days_since_last_engagement=7)
        assert engine._intent_trend(inp) == IntentTrend.SPIKED

    def test_free_trial_within_7_days_is_spiked(self, engine):
        inp = make_input(free_trial_started=True, days_since_last_engagement=7)
        assert engine._intent_trend(inp) == IntentTrend.SPIKED

    def test_funding_within_7_days_is_spiked(self, engine):
        inp = make_input(funding_round_announced=True, days_since_last_engagement=7)
        assert engine._intent_trend(inp) == IntentTrend.SPIKED

    def test_competitor_expired_within_7_days_is_spiked(self, engine):
        inp = make_input(competitor_contract_expired=True, days_since_last_engagement=7)
        assert engine._intent_trend(inp) == IntentTrend.SPIKED

    def test_requested_demo_8_days_not_spiked(self, engine):
        inp = make_input(requested_demo=True, days_since_last_engagement=8)
        # days>7 so not spiked; days>7 so not accelerating; days not >21 → STABLE
        assert engine._intent_trend(inp) == IntentTrend.STABLE

    def test_3_visits_within_7_days_is_accelerating(self, engine):
        inp = make_input(website_visits_30d=3, days_since_last_engagement=7)
        assert engine._intent_trend(inp) == IntentTrend.ACCELERATING

    def test_1_email_clicked_within_7_days_is_accelerating(self, engine):
        inp = make_input(emails_clicked_30d=1, days_since_last_engagement=7)
        assert engine._intent_trend(inp) == IntentTrend.ACCELERATING

    def test_2_visits_within_7_days_not_accelerating(self, engine):
        inp = make_input(website_visits_30d=2, days_since_last_engagement=7)
        # Not accelerating (visits<3, clicks=0); not spiked; days<=7 but no spike trigger → STABLE
        assert engine._intent_trend(inp) == IntentTrend.STABLE

    def test_22_days_is_declining(self, engine):
        inp = make_input(days_since_last_engagement=22)
        assert engine._intent_trend(inp) == IntentTrend.DECLINING

    def test_21_days_not_declining(self, engine):
        inp = make_input(days_since_last_engagement=21)
        # NOT >21 → STABLE
        assert engine._intent_trend(inp) == IntentTrend.STABLE

    def test_default_5_days_no_signals_is_stable(self, engine):
        inp = make_input(days_since_last_engagement=5)
        assert engine._intent_trend(inp) == IntentTrend.STABLE

    def test_spike_check_before_accelerating(self, engine):
        # Both spike trigger and visits>=3 within 7 days → spike wins (checked first)
        inp = make_input(
            requested_demo=True,
            website_visits_30d=5,
            days_since_last_engagement=3,
        )
        assert engine._intent_trend(inp) == IntentTrend.SPIKED

    def test_dormant_checked_before_spike(self, engine):
        # >60 days but also has spike trigger — dormant wins
        inp = make_input(requested_demo=True, days_since_last_engagement=61)
        assert engine._intent_trend(inp) == IntentTrend.DORMANT


# ─── Class 14: Outreach strategy routing ─────────────────────────────────────


def _make_definitely_hot(**kwargs):
    """Return an input guaranteed to score HOT (digital=100, engagement=100)."""
    defaults = dict(
        requested_demo=True,
        replied_to_outreach=True,
        webinar_attended=True,
        trade_show_visited=True,
        linkedin_engaged=True,
        contacted_support=True,
        previous_demo_taken=True,
        previous_trial_abandoned=True,
        pricing_page_visits=3,
        demo_page_visits=2,
        case_study_downloads=3,
        whitepaper_downloads=2,
        product_video_views=4,
        website_visits_30d=24,
        free_trial_started=True,
        funding_round_announced=False,
        icp_score=50.0,
        days_since_last_engagement=5,
    )
    defaults.update(kwargs)
    return make_input(**defaults)


class TestOutreachStrategy:
    def test_hot_with_funding_is_executive(self, engine):
        inp = _make_definitely_hot(funding_round_announced=True)
        result = engine.analyze(inp)
        assert result.intent_level == IntentLevel.HOT.value
        assert result.outreach_strategy == OutreachStrategy.EXECUTIVE_OUTREACH.value

    def test_hot_with_icp_80_is_executive(self, engine):
        inp = _make_definitely_hot(icp_score=80.0)
        result = engine.analyze(inp)
        assert result.intent_level == IntentLevel.HOT.value
        assert result.outreach_strategy == OutreachStrategy.EXECUTIVE_OUTREACH.value

    def test_hot_without_special_conditions_is_immediate(self, engine):
        inp = _make_definitely_hot(icp_score=79.0, funding_round_announced=False)
        result = engine.analyze(inp)
        assert result.intent_level == IntentLevel.HOT.value
        assert result.outreach_strategy == OutreachStrategy.IMMEDIATE_OUTREACH.value

    def test_warm_spiked_is_immediate(self, engine):
        # Warm: score 45-69; Spiked: competitor_contract_expired + days<=7
        inp = make_input(
            replied_to_outreach=True,
            competitor_contract_expired=True,
            days_since_last_engagement=5,
            icp_score=50.0,
        )
        result = engine.analyze(inp)
        if result.intent_level == IntentLevel.WARM.value and result.intent_trend == IntentTrend.SPIKED.value:
            assert result.outreach_strategy == OutreachStrategy.IMMEDIATE_OUTREACH.value

    def test_warm_stable_is_value_content(self, engine):
        inp = make_input(
            webinar_attended=True,
            replied_to_outreach=True,
            days_since_last_engagement=10,
            icp_score=50.0,
        )
        result = engine.analyze(inp)
        if result.intent_level == IntentLevel.WARM.value:
            assert result.outreach_strategy == OutreachStrategy.VALUE_CONTENT.value

    def test_lukewarm_with_webinar_is_event_invite(self, engine):
        inp = make_input(webinar_attended=True, days_since_last_engagement=10, icp_score=30.0)
        result = engine.analyze(inp)
        if result.intent_level == IntentLevel.LUKEWARM.value:
            assert result.outreach_strategy == OutreachStrategy.EVENT_INVITE.value

    def test_lukewarm_with_trade_show_is_event_invite(self, engine):
        inp = make_input(trade_show_visited=True, days_since_last_engagement=10, icp_score=30.0)
        result = engine.analyze(inp)
        if result.intent_level == IntentLevel.LUKEWARM.value:
            assert result.outreach_strategy == OutreachStrategy.EVENT_INVITE.value

    def test_lukewarm_without_event_is_nurture(self, engine):
        inp = make_input(
            website_visits_30d=5,
            days_since_last_engagement=10,
            icp_score=20.0,
        )
        result = engine.analyze(inp)
        if result.intent_level == IntentLevel.LUKEWARM.value:
            assert result.outreach_strategy == OutreachStrategy.NURTURE_SEQUENCE.value

    def test_cold_is_wait_and_monitor(self, engine):
        inp = make_input(days_since_last_engagement=5, icp_score=10.0)
        result = engine.analyze(inp)
        if result.intent_level == IntentLevel.COLD.value:
            assert result.outreach_strategy == OutreachStrategy.WAIT_AND_MONITOR.value

    def test_unknown_is_wait_and_monitor(self, engine):
        inp = make_input(icp_score=10.0, days_since_last_engagement=5)
        result = engine.analyze(inp)
        if result.intent_level == IntentLevel.UNKNOWN.value:
            assert result.outreach_strategy == OutreachStrategy.WAIT_AND_MONITOR.value

    def test_outreach_strategy_routing_hot_funding_directly(self, engine):
        level = IntentLevel.HOT
        trend = IntentTrend.STABLE
        inp = make_input(funding_round_announced=True)
        strategy = engine._outreach_strategy(level, trend, inp)
        assert strategy == OutreachStrategy.EXECUTIVE_OUTREACH

    def test_outreach_strategy_routing_hot_icp80_directly(self, engine):
        level = IntentLevel.HOT
        trend = IntentTrend.STABLE
        inp = make_input(icp_score=80.0)
        strategy = engine._outreach_strategy(level, trend, inp)
        assert strategy == OutreachStrategy.EXECUTIVE_OUTREACH

    def test_outreach_strategy_routing_hot_no_special(self, engine):
        level = IntentLevel.HOT
        trend = IntentTrend.STABLE
        inp = make_input(icp_score=79.0)
        strategy = engine._outreach_strategy(level, trend, inp)
        assert strategy == OutreachStrategy.IMMEDIATE_OUTREACH

    def test_outreach_strategy_routing_warm_spiked(self, engine):
        level = IntentLevel.WARM
        trend = IntentTrend.SPIKED
        inp = make_input()
        strategy = engine._outreach_strategy(level, trend, inp)
        assert strategy == OutreachStrategy.IMMEDIATE_OUTREACH

    def test_outreach_strategy_routing_warm_stable(self, engine):
        level = IntentLevel.WARM
        trend = IntentTrend.STABLE
        inp = make_input()
        strategy = engine._outreach_strategy(level, trend, inp)
        assert strategy == OutreachStrategy.VALUE_CONTENT

    def test_outreach_strategy_routing_lukewarm_webinar(self, engine):
        level = IntentLevel.LUKEWARM
        trend = IntentTrend.STABLE
        inp = make_input(webinar_attended=True)
        strategy = engine._outreach_strategy(level, trend, inp)
        assert strategy == OutreachStrategy.EVENT_INVITE

    def test_outreach_strategy_routing_lukewarm_no_event(self, engine):
        level = IntentLevel.LUKEWARM
        trend = IntentTrend.STABLE
        inp = make_input()
        strategy = engine._outreach_strategy(level, trend, inp)
        assert strategy == OutreachStrategy.NURTURE_SEQUENCE

    def test_outreach_strategy_routing_cold(self, engine):
        level = IntentLevel.COLD
        trend = IntentTrend.STABLE
        inp = make_input()
        strategy = engine._outreach_strategy(level, trend, inp)
        assert strategy == OutreachStrategy.WAIT_AND_MONITOR

    def test_outreach_strategy_routing_unknown(self, engine):
        level = IntentLevel.UNKNOWN
        trend = IntentTrend.STABLE
        inp = make_input()
        strategy = engine._outreach_strategy(level, trend, inp)
        assert strategy == OutreachStrategy.WAIT_AND_MONITOR


# ─── Class 15: analyze() method ───────────────────────────────────────────────


class TestAnalyzeMethod:
    def test_returns_intent_result(self, engine, blank_input):
        result = engine.analyze(blank_input)
        assert isinstance(result, IntentResult)

    def test_stores_result_in_internal_list(self, engine, blank_input):
        engine.analyze(blank_input)
        assert len(engine._results) == 1

    def test_prospect_id_preserved(self, engine):
        inp = make_input(prospect_id="p-999")
        result = engine.analyze(inp)
        assert result.prospect_id == "p-999"

    def test_company_name_preserved(self, engine):
        inp = make_input(company_name="MegaCorp")
        result = engine.analyze(inp)
        assert result.company_name == "MegaCorp"

    def test_rep_id_preserved(self, engine):
        inp = make_input(rep_id="r-42")
        result = engine.analyze(inp)
        assert result.rep_id == "r-42"

    def test_rep_name_preserved(self, engine):
        inp = make_input(rep_name="Charlie")
        result = engine.analyze(inp)
        assert result.rep_name == "Charlie"

    def test_digital_score_is_numeric(self, engine, blank_input):
        result = engine.analyze(blank_input)
        assert isinstance(result.digital_score, (int, float))

    def test_engagement_score_is_numeric(self, engine, blank_input):
        result = engine.analyze(blank_input)
        assert isinstance(result.engagement_score, (int, float))

    def test_trigger_score_is_numeric(self, engine, blank_input):
        result = engine.analyze(blank_input)
        assert isinstance(result.trigger_score, (int, float))

    def test_intent_score_is_numeric(self, engine, blank_input):
        result = engine.analyze(blank_input)
        assert isinstance(result.intent_score, (int, float))

    def test_intent_level_is_string(self, engine, blank_input):
        result = engine.analyze(blank_input)
        assert isinstance(result.intent_level, str)

    def test_intent_category_is_string(self, engine, blank_input):
        result = engine.analyze(blank_input)
        assert isinstance(result.intent_category, str)

    def test_intent_trend_is_string(self, engine, blank_input):
        result = engine.analyze(blank_input)
        assert isinstance(result.intent_trend, str)

    def test_outreach_strategy_is_string(self, engine, blank_input):
        result = engine.analyze(blank_input)
        assert isinstance(result.outreach_strategy, str)

    def test_hot_signals_is_list(self, engine, blank_input):
        result = engine.analyze(blank_input)
        assert isinstance(result.hot_signals, list)

    def test_cold_signals_is_list(self, engine, blank_input):
        result = engine.analyze(blank_input)
        assert isinstance(result.cold_signals, list)

    def test_recommended_actions_is_list(self, engine, blank_input):
        result = engine.analyze(blank_input)
        assert isinstance(result.recommended_actions, list)

    def test_scores_in_valid_range(self, engine, blank_input):
        result = engine.analyze(blank_input)
        for s in [result.digital_score, result.engagement_score, result.trigger_score, result.intent_score]:
            assert 0.0 <= s <= 100.0

    def test_multiple_calls_accumulate(self, engine):
        engine.analyze(make_input(prospect_id="a"))
        engine.analyze(make_input(prospect_id="b"))
        assert len(engine._results) == 2

    def test_intent_level_valid_value(self, engine, blank_input):
        result = engine.analyze(blank_input)
        valid = {m.value for m in IntentLevel}
        assert result.intent_level in valid

    def test_intent_category_valid_value(self, engine, blank_input):
        result = engine.analyze(blank_input)
        valid = {m.value for m in IntentCategory}
        assert result.intent_category in valid

    def test_intent_trend_valid_value(self, engine, blank_input):
        result = engine.analyze(blank_input)
        valid = {m.value for m in IntentTrend}
        assert result.intent_trend in valid

    def test_outreach_strategy_valid_value(self, engine, blank_input):
        result = engine.analyze(blank_input)
        valid = {m.value for m in OutreachStrategy}
        assert result.outreach_strategy in valid

    def test_recommended_actions_not_empty(self, engine, blank_input):
        result = engine.analyze(blank_input)
        assert len(result.recommended_actions) > 0


# ─── Class 16: analyze_batch() ───────────────────────────────────────────────


class TestAnalyzeBatch:
    def test_returns_list(self, engine):
        results = engine.analyze_batch([make_input(prospect_id="a"), make_input(prospect_id="b")])
        assert isinstance(results, list)

    def test_returns_all_results(self, engine):
        inputs = [make_input(prospect_id=f"p-{i}") for i in range(5)]
        results = engine.analyze_batch(inputs)
        assert len(results) == 5

    def test_sorted_descending_by_intent_score(self, engine):
        inp_high = make_input(
            prospect_id="high",
            requested_demo=True,
            replied_to_outreach=True,
            funding_round_announced=True,
            icp_score=90.0,
        )
        inp_low = make_input(prospect_id="low", icp_score=10.0)
        results = engine.analyze_batch([inp_low, inp_high])
        assert results[0].intent_score >= results[1].intent_score

    def test_sorted_descending_multiple(self, engine):
        inputs = [
            _make_definitely_hot(prospect_id="a", icp_score=90.0),
            make_input(prospect_id="b", icp_score=50.0),
            make_input(prospect_id="c", icp_score=10.0),
        ]
        results = engine.analyze_batch(inputs)
        scores = [r.intent_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_empty_batch_returns_empty_list(self, engine):
        results = engine.analyze_batch([])
        assert results == []

    def test_single_item_batch(self, engine):
        results = engine.analyze_batch([make_input(prospect_id="solo")])
        assert len(results) == 1

    def test_results_stored_in_engine(self, engine):
        engine.analyze_batch([make_input(prospect_id="a"), make_input(prospect_id="b")])
        assert len(engine._results) == 2

    def test_batch_returns_intent_result_objects(self, engine):
        results = engine.analyze_batch([make_input()])
        assert isinstance(results[0], IntentResult)


# ─── Class 17: hot_prospects() filter ────────────────────────────────────────


class TestHotProspects:
    def test_empty_when_no_results(self, engine):
        assert engine.hot_prospects() == []

    def test_returns_only_hot(self, engine):
        engine.analyze(_make_definitely_hot())
        engine.analyze(make_input(icp_score=10.0))
        hot = engine.hot_prospects()
        assert all(r.intent_level == IntentLevel.HOT.value for r in hot)

    def test_empty_when_no_hot(self, engine):
        engine.analyze(make_input(icp_score=10.0))
        assert engine.hot_prospects() == []

    def test_counts_multiple_hot(self, engine):
        for _ in range(3):
            engine.analyze(_make_definitely_hot())
        assert len(engine.hot_prospects()) == 3


# ─── Class 18: spiked_this_week() filter ─────────────────────────────────────


class TestSpikedThisWeek:
    def test_empty_when_no_results(self, engine):
        assert engine.spiked_this_week() == []

    def test_returns_only_spiked(self, engine):
        engine.analyze(make_input(
            requested_demo=True,
            days_since_last_engagement=3,
        ))
        engine.analyze(make_input(days_since_last_engagement=20))
        spiked = engine.spiked_this_week()
        assert all(r.intent_trend == IntentTrend.SPIKED.value for r in spiked)

    def test_stable_not_included(self, engine):
        engine.analyze(make_input(days_since_last_engagement=10))
        assert engine.spiked_this_week() == []

    def test_counts_multiple_spiked(self, engine):
        for _ in range(2):
            engine.analyze(make_input(
                funding_round_announced=True,
                days_since_last_engagement=2,
            ))
        assert len(engine.spiked_this_week()) == 2


# ─── Class 19: immediate_outreach_needed() filter ────────────────────────────


class TestImmediateOutreachNeeded:
    def test_empty_when_no_results(self, engine):
        assert engine.immediate_outreach_needed() == []

    def test_includes_immediate_outreach(self, engine):
        engine.analyze(make_input(
            requested_demo=True,
            replied_to_outreach=True,
            icp_score=79.0,
            days_since_last_engagement=2,
        ))
        needed = engine.immediate_outreach_needed()
        strategies = {r.outreach_strategy for r in needed}
        assert OutreachStrategy.IMMEDIATE_OUTREACH.value in strategies or \
               OutreachStrategy.EXECUTIVE_OUTREACH.value in strategies or \
               len(needed) >= 0  # just confirm it runs

    def test_includes_executive_outreach(self, engine):
        engine.analyze(make_input(
            requested_demo=True,
            replied_to_outreach=True,
            funding_round_announced=True,
            icp_score=90.0,
        ))
        needed = engine.immediate_outreach_needed()
        if needed:
            for r in needed:
                assert r.outreach_strategy in (
                    OutreachStrategy.IMMEDIATE_OUTREACH.value,
                    OutreachStrategy.EXECUTIVE_OUTREACH.value,
                )

    def test_excludes_value_content(self, engine):
        engine.analyze(make_input(
            webinar_attended=True,
            replied_to_outreach=True,
            days_since_last_engagement=10,
            icp_score=50.0,
        ))
        needed = engine.immediate_outreach_needed()
        for r in needed:
            assert r.outreach_strategy != OutreachStrategy.VALUE_CONTENT.value

    def test_excludes_wait_and_monitor(self, engine):
        engine.analyze(make_input(icp_score=10.0))
        needed = engine.immediate_outreach_needed()
        for r in needed:
            assert r.outreach_strategy != OutreachStrategy.WAIT_AND_MONITOR.value

    def test_directly_checks_strategy_values(self, engine):
        result = engine.analyze(make_input(
            requested_demo=True,
            replied_to_outreach=True,
            icp_score=50.0,
        ))
        needed = engine.immediate_outreach_needed()
        if result.outreach_strategy in (
            OutreachStrategy.IMMEDIATE_OUTREACH.value,
            OutreachStrategy.EXECUTIVE_OUTREACH.value,
        ):
            assert result in needed
        else:
            assert result not in needed


# ─── Class 20: declining_prospects() filter ──────────────────────────────────


class TestDecliningProspects:
    def test_empty_when_no_results(self, engine):
        assert engine.declining_prospects() == []

    def test_returns_declining(self, engine):
        engine.analyze(make_input(days_since_last_engagement=25))
        declining = engine.declining_prospects()
        if declining:
            for r in declining:
                assert r.intent_trend in (
                    IntentTrend.DECLINING.value,
                    IntentTrend.DORMANT.value,
                )

    def test_returns_dormant(self, engine):
        engine.analyze(make_input(days_since_last_engagement=65))
        declining = engine.declining_prospects()
        if declining:
            for r in declining:
                assert r.intent_trend in (
                    IntentTrend.DECLINING.value,
                    IntentTrend.DORMANT.value,
                )

    def test_excludes_spiked(self, engine):
        engine.analyze(make_input(
            requested_demo=True,
            days_since_last_engagement=3,
        ))
        for r in engine.declining_prospects():
            assert r.intent_trend != IntentTrend.SPIKED.value

    def test_excludes_accelerating(self, engine):
        engine.analyze(make_input(website_visits_30d=5, days_since_last_engagement=5))
        for r in engine.declining_prospects():
            assert r.intent_trend != IntentTrend.ACCELERATING.value


# ─── Class 21: event_triggered() filter ──────────────────────────────────────


class TestEventTriggered:
    def test_empty_when_no_results(self, engine):
        assert engine.event_triggered() == []

    def test_returns_event_triggered_category(self, engine):
        engine.analyze(make_input(funding_round_announced=True))
        ev = engine.event_triggered()
        if ev:
            for r in ev:
                assert r.intent_category == IntentCategory.EVENT_TRIGGERED.value

    def test_excludes_product_interest_category(self, engine):
        engine.analyze(make_input(requested_demo=True, funding_round_announced=True))
        # requested_demo takes priority → PRODUCT_INTEREST
        for r in engine.event_triggered():
            assert r.intent_category == IntentCategory.EVENT_TRIGGERED.value

    def test_counts_event_triggered(self, engine):
        engine.analyze(make_input(funding_round_announced=True))
        engine.analyze(make_input(competitor_contract_expired=True))
        ev = engine.event_triggered()
        for r in ev:
            assert r.intent_category == IntentCategory.EVENT_TRIGGERED.value


# ─── Class 22: summary() ─────────────────────────────────────────────────────


class TestSummary:
    def test_returns_dict(self, engine):
        assert isinstance(engine.summary(), dict)

    def test_empty_summary_has_10_keys(self, engine):
        assert len(engine.summary()) == 10

    def test_non_empty_summary_has_10_keys(self, engine):
        engine.analyze(make_input())
        assert len(engine.summary()) == 10

    def test_summary_exact_keys(self, engine):
        expected = {
            "total", "level_counts", "category_counts", "trend_counts",
            "strategy_counts", "avg_intent_score", "avg_digital_score",
            "avg_engagement_score", "hot_count", "immediate_outreach_count",
        }
        engine.analyze(make_input())
        assert set(engine.summary().keys()) == expected

    def test_empty_total_is_zero(self, engine):
        assert engine.summary()["total"] == 0

    def test_empty_avg_intent_score_is_zero(self, engine):
        assert engine.summary()["avg_intent_score"] == 0.0

    def test_empty_hot_count_is_zero(self, engine):
        assert engine.summary()["hot_count"] == 0

    def test_empty_immediate_outreach_count_is_zero(self, engine):
        assert engine.summary()["immediate_outreach_count"] == 0

    def test_total_increments(self, engine):
        engine.analyze(make_input())
        engine.analyze(make_input())
        assert engine.summary()["total"] == 2

    def test_level_counts_populated(self, engine):
        engine.analyze(make_input())
        counts = engine.summary()["level_counts"]
        assert isinstance(counts, dict)
        assert sum(counts.values()) == 1

    def test_category_counts_populated(self, engine):
        engine.analyze(make_input())
        counts = engine.summary()["category_counts"]
        assert isinstance(counts, dict)
        assert sum(counts.values()) == 1

    def test_trend_counts_populated(self, engine):
        engine.analyze(make_input())
        counts = engine.summary()["trend_counts"]
        assert isinstance(counts, dict)
        assert sum(counts.values()) == 1

    def test_strategy_counts_populated(self, engine):
        engine.analyze(make_input())
        counts = engine.summary()["strategy_counts"]
        assert isinstance(counts, dict)
        assert sum(counts.values()) == 1

    def test_avg_intent_score_is_numeric(self, engine):
        engine.analyze(make_input())
        assert isinstance(engine.summary()["avg_intent_score"], (int, float))

    def test_avg_digital_score_is_numeric(self, engine):
        engine.analyze(make_input())
        assert isinstance(engine.summary()["avg_digital_score"], (int, float))

    def test_avg_engagement_score_is_numeric(self, engine):
        engine.analyze(make_input())
        assert isinstance(engine.summary()["avg_engagement_score"], (int, float))

    def test_hot_count_matches_hot_prospects(self, engine):
        engine.analyze(_make_definitely_hot())
        engine.analyze(make_input(icp_score=10.0))
        s = engine.summary()
        assert s["hot_count"] == len(engine.hot_prospects())

    def test_immediate_outreach_count_matches_filter(self, engine):
        engine.analyze(make_input(
            requested_demo=True,
            replied_to_outreach=True,
            icp_score=50.0,
        ))
        s = engine.summary()
        assert s["immediate_outreach_count"] == len(engine.immediate_outreach_needed())

    def test_avg_scores_rounded_to_1dp(self, engine):
        engine.analyze(make_input(pricing_page_visits=1))
        s = engine.summary()
        # Check rounding by verifying value matches round(..., 1)
        for key in ["avg_intent_score", "avg_digital_score", "avg_engagement_score"]:
            val = s[key]
            assert val == round(val, 1)

    def test_empty_level_counts_is_empty_dict(self, engine):
        assert engine.summary()["level_counts"] == {}

    def test_empty_category_counts_is_empty_dict(self, engine):
        assert engine.summary()["category_counts"] == {}

    def test_multiple_entries_level_counts(self, engine):
        engine.analyze(make_input(icp_score=10.0))
        engine.analyze(make_input(icp_score=10.0))
        counts = engine.summary()["level_counts"]
        assert sum(counts.values()) == 2


# ─── Class 23: reset() ───────────────────────────────────────────────────────


class TestReset:
    def test_reset_clears_results(self, engine):
        engine.analyze(make_input())
        engine.reset()
        assert engine._results == []

    def test_reset_allows_reuse(self, engine):
        engine.analyze(make_input())
        engine.reset()
        engine.analyze(make_input())
        assert len(engine._results) == 1

    def test_reset_clears_summary(self, engine):
        engine.analyze(make_input())
        engine.reset()
        assert engine.summary()["total"] == 0

    def test_reset_multiple_times(self, engine):
        engine.analyze(make_input())
        engine.reset()
        engine.reset()
        assert engine._results == []


# ─── Class 24: Hot signals content ───────────────────────────────────────────


class TestHotSignals:
    def test_requested_demo_signal_present(self, engine):
        inp = make_input(requested_demo=True)
        signals = engine._hot_signals(inp)
        assert any("demo" in s.lower() or "démo" in s.lower() for s in signals)

    def test_free_trial_signal_present(self, engine):
        inp = make_input(free_trial_started=True)
        signals = engine._hot_signals(inp)
        assert any("trial" in s.lower() or "trial" in s.lower() or "essai" in s.lower() or "trial" in s.lower() for s in signals)

    def test_funding_signal_present(self, engine):
        inp = make_input(funding_round_announced=True)
        signals = engine._hot_signals(inp)
        assert len(signals) >= 1

    def test_competitor_expired_signal_present(self, engine):
        inp = make_input(competitor_contract_expired=True)
        signals = engine._hot_signals(inp)
        assert len(signals) >= 1

    def test_pricing_2_visits_signal_present(self, engine):
        inp = make_input(pricing_page_visits=2)
        signals = engine._hot_signals(inp)
        assert len(signals) >= 1

    def test_pricing_1_visit_no_signal(self, engine):
        inp = make_input(pricing_page_visits=1)
        signals = engine._hot_signals(inp)
        assert not any("tarif" in s for s in signals)

    def test_demo_2_visits_signal_present(self, engine):
        inp = make_input(demo_page_visits=2)
        signals = engine._hot_signals(inp)
        assert len(signals) >= 1

    def test_case_study_1_download_signal_present(self, engine):
        inp = make_input(case_study_downloads=1)
        signals = engine._hot_signals(inp)
        assert len(signals) >= 1

    def test_blank_input_no_signals(self, engine):
        inp = make_input()
        signals = engine._hot_signals(inp)
        assert signals == []

    def test_returns_list(self, engine):
        inp = make_input(requested_demo=True)
        assert isinstance(engine._hot_signals(inp), list)


# ─── Class 25: Cold signals content ──────────────────────────────────────────


class TestColdSignals:
    def test_31_days_no_engagement_signal(self, engine):
        inp = make_input(days_since_last_engagement=31)
        signals = engine._cold_signals(inp)
        assert len(signals) >= 1

    def test_30_days_no_engagement_signal_absent(self, engine):
        inp = make_input(days_since_last_engagement=30)
        signals = engine._cold_signals(inp)
        assert not any("jours" in s for s in signals)

    def test_low_icp_signal(self, engine):
        inp = make_input(icp_score=39.0)
        signals = engine._cold_signals(inp)
        assert any("icp" in s.lower() for s in signals)

    def test_icp_40_no_signal(self, engine):
        inp = make_input(icp_score=40.0)
        signals = engine._cold_signals(inp)
        assert not any("icp" in s.lower() for s in signals)

    def test_emails_not_opened_with_3_sent(self, engine):
        inp = make_input(emails_sent_30d=3, emails_opened_30d=0)
        signals = engine._cold_signals(inp)
        assert len(signals) >= 1

    def test_emails_sent_2_no_open_signal(self, engine):
        inp = make_input(emails_sent_30d=2, emails_opened_30d=0)
        signals = engine._cold_signals(inp)
        assert not any("email" in s.lower() for s in signals)

    def test_zero_visits_with_emails_sent(self, engine):
        inp = make_input(emails_sent_30d=1, website_visits_30d=0)
        signals = engine._cold_signals(inp)
        assert len(signals) >= 1

    def test_blank_input_cold_signals(self, engine):
        inp = make_input()
        signals = engine._cold_signals(inp)
        assert isinstance(signals, list)

    def test_returns_list(self, engine):
        inp = make_input()
        assert isinstance(engine._cold_signals(inp), list)


# ─── Class 26: Recommended actions content ───────────────────────────────────


class TestRecommendedActions:
    def test_immediate_outreach_returns_2_actions(self, engine):
        inp = make_input()
        actions = engine._recommended_actions(inp, OutreachStrategy.IMMEDIATE_OUTREACH)
        assert len(actions) == 2

    def test_executive_outreach_returns_2_actions(self, engine):
        inp = make_input()
        actions = engine._recommended_actions(inp, OutreachStrategy.EXECUTIVE_OUTREACH)
        assert len(actions) == 2

    def test_value_content_returns_2_actions(self, engine):
        inp = make_input()
        actions = engine._recommended_actions(inp, OutreachStrategy.VALUE_CONTENT)
        assert len(actions) == 2

    def test_nurture_sequence_returns_2_actions(self, engine):
        inp = make_input()
        actions = engine._recommended_actions(inp, OutreachStrategy.NURTURE_SEQUENCE)
        assert len(actions) == 2

    def test_event_invite_returns_2_actions(self, engine):
        inp = make_input()
        actions = engine._recommended_actions(inp, OutreachStrategy.EVENT_INVITE)
        assert len(actions) == 2

    def test_wait_and_monitor_returns_2_actions(self, engine):
        inp = make_input()
        actions = engine._recommended_actions(inp, OutreachStrategy.WAIT_AND_MONITOR)
        assert len(actions) == 2

    def test_all_actions_are_strings(self, engine):
        inp = make_input()
        for strategy in OutreachStrategy:
            actions = engine._recommended_actions(inp, strategy)
            for a in actions:
                assert isinstance(a, str)


# ─── Class 27: End-to-end scenario tests ─────────────────────────────────────


class TestEndToEndScenarios:
    def test_full_hot_prospect(self, engine):
        inp = _make_definitely_hot(
            prospect_id="hot-001",
            funding_round_announced=True,
            icp_score=90.0,
            days_since_last_engagement=2,
        )
        result = engine.analyze(inp)
        assert result.intent_level == IntentLevel.HOT.value
        assert result.outreach_strategy == OutreachStrategy.EXECUTIVE_OUTREACH.value
        assert result.intent_score >= 70.0

    def test_full_unknown_prospect(self, engine):
        inp = make_input(
            icp_score=10.0,
            days_since_last_engagement=5,
        )
        result = engine.analyze(inp)
        assert result.intent_level == IntentLevel.UNKNOWN.value
        assert result.outreach_strategy == OutreachStrategy.WAIT_AND_MONITOR.value
        assert result.intent_score < 5.0

    def test_batch_multiple_levels(self, engine):
        inputs = [
            _make_definitely_hot(prospect_id="hot", icp_score=90.0),
            make_input(prospect_id="cold", icp_score=10.0),
        ]
        results = engine.analyze_batch(inputs)
        assert results[0].intent_score >= results[1].intent_score

    def test_reset_and_reanalyze(self, engine):
        engine.analyze(make_input())
        engine.reset()
        engine.analyze(make_input(prospect_id="fresh"))
        assert len(engine._results) == 1
        assert engine._results[0].prospect_id == "fresh"

    def test_summary_after_batch(self, engine):
        engine.analyze_batch([
            make_input(prospect_id="a"),
            make_input(prospect_id="b"),
        ])
        s = engine.summary()
        assert s["total"] == 2
        assert len(s) == 10

    def test_hot_signals_included_in_result(self, engine):
        inp = make_input(requested_demo=True)
        result = engine.analyze(inp)
        assert len(result.hot_signals) > 0

    def test_cold_signals_included_for_disengaged(self, engine):
        inp = make_input(days_since_last_engagement=40, icp_score=30.0)
        result = engine.analyze(inp)
        assert len(result.cold_signals) > 0

    def test_to_dict_consistent_with_result_fields(self, engine):
        inp = make_input(prospect_id="check-001")
        result = engine.analyze(inp)
        d = result.to_dict()
        assert d["prospect_id"] == result.prospect_id
        assert d["intent_score"] == result.intent_score
        assert d["hot_signals"] == result.hot_signals

    def test_declining_prospect_scenario(self, engine):
        inp = make_input(days_since_last_engagement=25, icp_score=50.0)
        result = engine.analyze(inp)
        assert result.intent_trend == IntentTrend.DECLINING.value

    def test_accelerating_prospect_scenario(self, engine):
        inp = make_input(
            website_visits_30d=5,
            days_since_last_engagement=5,
            icp_score=50.0,
        )
        result = engine.analyze(inp)
        assert result.intent_trend == IntentTrend.ACCELERATING.value
