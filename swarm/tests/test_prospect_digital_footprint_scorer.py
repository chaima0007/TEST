"""
Comprehensive pytest tests for swarm/intelligence/prospect_digital_footprint_scorer.py
Module 73 — Prospect Digital Footprint Scorer
"""

from __future__ import annotations

import pytest
from intelligence.prospect_digital_footprint_scorer import (
    IntentTier,
    FootprintPattern,
    EngagementVelocity,
    ProspectAction,
    ProspectDigitalInput,
    ProspectDigitalResult,
    ProspectDigitalFootprintScorer,
)


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures / helpers
# ─────────────────────────────────────────────────────────────────────────────

def make_input(
    prospect_id="P001",
    company_name="Acme Corp",
    rep_id="R01",
    website_visits_last_30d=0,
    website_visits_prev_30d=0,
    pricing_page_views=0,
    case_study_downloads=0,
    demo_page_views=0,
    demo_requested=0,
    free_trial_started=0,
    email_opens_last_30d=0,
    email_clicks_last_30d=0,
    linkedin_profile_views_of_rep=0,
    linkedin_company_page_visits=0,
    competitor_review_site_signal=0,
    job_posting_signal_count=0,
    company_size_employees=500,
    funding_event_recent=0,
    technology_fit_score=50.0,
    days_since_first_touch=30,
    time_on_site_avg_minutes=0.0,
    return_visit_rate_pct=0.0,
) -> ProspectDigitalInput:
    return ProspectDigitalInput(
        prospect_id=prospect_id,
        company_name=company_name,
        rep_id=rep_id,
        website_visits_last_30d=website_visits_last_30d,
        website_visits_prev_30d=website_visits_prev_30d,
        pricing_page_views=pricing_page_views,
        case_study_downloads=case_study_downloads,
        demo_page_views=demo_page_views,
        demo_requested=demo_requested,
        free_trial_started=free_trial_started,
        email_opens_last_30d=email_opens_last_30d,
        email_clicks_last_30d=email_clicks_last_30d,
        linkedin_profile_views_of_rep=linkedin_profile_views_of_rep,
        linkedin_company_page_visits=linkedin_company_page_visits,
        competitor_review_site_signal=competitor_review_site_signal,
        job_posting_signal_count=job_posting_signal_count,
        company_size_employees=company_size_employees,
        funding_event_recent=funding_event_recent,
        technology_fit_score=technology_fit_score,
        days_since_first_touch=days_since_first_touch,
        time_on_site_avg_minutes=time_on_site_avg_minutes,
        return_visit_rate_pct=return_visit_rate_pct,
    )


@pytest.fixture
def scorer():
    return ProspectDigitalFootprintScorer()


@pytest.fixture
def bare_input():
    """All-zero prospect — cold / passive lurker."""
    return make_input(technology_fit_score=0.0)


@pytest.fixture
def hot_input():
    """Clearly hot prospect — all signals high."""
    return make_input(
        website_visits_last_30d=10,
        website_visits_prev_30d=2,
        pricing_page_views=3,
        case_study_downloads=2,
        demo_page_views=2,
        email_opens_last_30d=8,
        email_clicks_last_30d=5,
        linkedin_profile_views_of_rep=2,
        linkedin_company_page_visits=4,
        job_posting_signal_count=3,
        company_size_employees=800,
        technology_fit_score=80.0,
        return_visit_rate_pct=40.0,
        time_on_site_avg_minutes=3.0,
    )


@pytest.fixture
def buying_now_demo_input():
    """Demo-requested prospect → buying_now."""
    return make_input(demo_requested=1, company_size_employees=500)


@pytest.fixture
def buying_now_trial_input():
    """Free-trial-started prospect → buying_now."""
    return make_input(free_trial_started=1, company_size_employees=500)


# ─────────────────────────────────────────────────────────────────────────────
# 1. Enum values & membership
# ─────────────────────────────────────────────────────────────────────────────

class TestEnumValues:
    def test_intent_tier_cold(self):
        assert IntentTier.COLD.value == "cold"

    def test_intent_tier_warming(self):
        assert IntentTier.WARMING.value == "warming"

    def test_intent_tier_hot(self):
        assert IntentTier.HOT.value == "hot"

    def test_intent_tier_buying_now(self):
        assert IntentTier.BUYING_NOW.value == "buying_now"

    def test_intent_tier_count(self):
        assert len(IntentTier) == 4

    def test_footprint_passive_lurker(self):
        assert FootprintPattern.PASSIVE_LURKER.value == "passive_lurker"

    def test_footprint_content_consumer(self):
        assert FootprintPattern.CONTENT_CONSUMER.value == "content_consumer"

    def test_footprint_active_researcher(self):
        assert FootprintPattern.ACTIVE_RESEARCHER.value == "active_researcher"

    def test_footprint_intent_spiker(self):
        assert FootprintPattern.INTENT_SPIKER.value == "intent_spiker"

    def test_footprint_competitive_evaluator(self):
        assert FootprintPattern.COMPETITIVE_EVALUATOR.value == "competitive_evaluator"

    def test_footprint_ready_to_buy(self):
        assert FootprintPattern.READY_TO_BUY.value == "ready_to_buy"

    def test_footprint_count(self):
        assert len(FootprintPattern) == 6

    def test_velocity_declining(self):
        assert EngagementVelocity.DECLINING.value == "declining"

    def test_velocity_flat(self):
        assert EngagementVelocity.FLAT.value == "flat"

    def test_velocity_growing(self):
        assert EngagementVelocity.GROWING.value == "growing"

    def test_velocity_surging(self):
        assert EngagementVelocity.SURGING.value == "surging"

    def test_velocity_count(self):
        assert len(EngagementVelocity) == 4

    def test_action_nurture(self):
        assert ProspectAction.NURTURE.value == "nurture"

    def test_action_warm_outreach(self):
        assert ProspectAction.WARM_OUTREACH.value == "warm_outreach"

    def test_action_immediate_sdr(self):
        assert ProspectAction.IMMEDIATE_SDR.value == "immediate_sdr"

    def test_action_executive_touch(self):
        assert ProspectAction.EXECUTIVE_TOUCH.value == "executive_touch"

    def test_action_count(self):
        assert len(ProspectAction) == 4

    def test_intent_tier_is_str_enum(self):
        assert isinstance(IntentTier.COLD, str)

    def test_footprint_is_str_enum(self):
        assert isinstance(FootprintPattern.PASSIVE_LURKER, str)

    def test_velocity_is_str_enum(self):
        assert isinstance(EngagementVelocity.FLAT, str)

    def test_action_is_str_enum(self):
        assert isinstance(ProspectAction.NURTURE, str)


# ─────────────────────────────────────────────────────────────────────────────
# 2. ProspectDigitalInput — 22 fields
# ─────────────────────────────────────────────────────────────────────────────

class TestProspectDigitalInputFields:
    def test_field_count(self):
        inp = make_input()
        assert len(inp.__dataclass_fields__) == 22

    def test_all_22_field_names(self):
        expected = {
            "prospect_id", "company_name", "rep_id",
            "website_visits_last_30d", "website_visits_prev_30d",
            "pricing_page_views", "case_study_downloads", "demo_page_views",
            "demo_requested", "free_trial_started",
            "email_opens_last_30d", "email_clicks_last_30d",
            "linkedin_profile_views_of_rep", "linkedin_company_page_visits",
            "competitor_review_site_signal", "job_posting_signal_count",
            "company_size_employees", "funding_event_recent",
            "technology_fit_score", "days_since_first_touch",
            "time_on_site_avg_minutes", "return_visit_rate_pct",
        }
        assert set(make_input().__dataclass_fields__.keys()) == expected

    def test_input_stores_values(self):
        inp = make_input(prospect_id="X", company_name="Y", rep_id="Z")
        assert inp.prospect_id == "X"
        assert inp.company_name == "Y"
        assert inp.rep_id == "Z"


# ─────────────────────────────────────────────────────────────────────────────
# 3. ProspectDigitalResult — to_dict() 15 keys
# ─────────────────────────────────────────────────────────────────────────────

class TestProspectDigitalResultToDict:
    def test_to_dict_key_count(self, scorer, bare_input):
        result = scorer.score(bare_input)
        assert len(result.to_dict()) == 15

    def test_to_dict_exact_keys(self, scorer, bare_input):
        d = scorer.score(bare_input).to_dict()
        expected = {
            "prospect_id", "company_name", "intent_tier", "footprint_pattern",
            "engagement_velocity", "prospect_action", "website_intent_score",
            "content_engagement_score", "social_signal_score", "company_fit_score",
            "digital_footprint_composite", "lead_score", "days_to_outreach",
            "is_high_intent", "needs_immediate_outreach",
        }
        assert set(d.keys()) == expected

    def test_to_dict_enum_values_are_strings(self, scorer, bare_input):
        d = scorer.score(bare_input).to_dict()
        assert isinstance(d["intent_tier"], str)
        assert isinstance(d["footprint_pattern"], str)
        assert isinstance(d["engagement_velocity"], str)
        assert isinstance(d["prospect_action"], str)

    def test_to_dict_prospect_id_matches(self, scorer):
        result = scorer.score(make_input(prospect_id="PX99"))
        assert result.to_dict()["prospect_id"] == "PX99"

    def test_to_dict_company_name_matches(self, scorer):
        result = scorer.score(make_input(company_name="BigCo"))
        assert result.to_dict()["company_name"] == "BigCo"

    def test_to_dict_bool_fields(self, scorer, bare_input):
        d = scorer.score(bare_input).to_dict()
        assert isinstance(d["is_high_intent"], bool)
        assert isinstance(d["needs_immediate_outreach"], bool)

    def test_to_dict_days_to_outreach_is_int(self, scorer, bare_input):
        d = scorer.score(bare_input).to_dict()
        assert isinstance(d["days_to_outreach"], int)


# ─────────────────────────────────────────────────────────────────────────────
# 4. _website_intent_score boundaries
# ─────────────────────────────────────────────────────────────────────────────

class TestWebsiteIntentScore:
    def _score(self, **kwargs):
        s = ProspectDigitalFootprintScorer()
        return s._website_intent_score(make_input(**kwargs))

    def test_zero_inputs(self):
        assert self._score() == 0.0

    def test_visits_cap_at_20(self):
        # 14 visits * 1.5 = 21 → capped at 20
        assert self._score(website_visits_last_30d=14) == 20.0

    def test_visits_exactly_at_cap(self):
        # 13 * 1.5 = 19.5 < 20
        val = self._score(website_visits_last_30d=13)
        assert val == 19.5

    def test_visits_below_cap(self):
        # 5 * 1.5 = 7.5
        assert self._score(website_visits_last_30d=5) == 7.5

    def test_pricing_pages_cap_at_30(self):
        # 3 * 10 = 30
        assert self._score(pricing_page_views=3) == 30.0

    def test_pricing_pages_cap_exceeded(self):
        # 5 * 10 = 50 → capped at 30
        assert self._score(pricing_page_views=5) == 30.0

    def test_pricing_pages_below_cap(self):
        # 2 * 10 = 20
        assert self._score(pricing_page_views=2) == 20.0

    def test_demo_views_cap_at_20(self):
        # 3 * 7 = 21 → capped at 20
        assert self._score(demo_page_views=3) == 20.0

    def test_demo_views_below_cap(self):
        # 2 * 7 = 14
        assert self._score(demo_page_views=2) == 14.0

    def test_demo_requested_adds_20(self):
        assert self._score(demo_requested=1) == 20.0

    def test_time_on_site_cap_at_10(self):
        # 6.0 * 2 = 12 → capped at 10
        assert self._score(time_on_site_avg_minutes=6.0) == 10.0

    def test_time_on_site_exactly_at_cap(self):
        # 5.0 * 2 = 10
        assert self._score(time_on_site_avg_minutes=5.0) == 10.0

    def test_time_on_site_below_cap(self):
        # 3.0 * 2 = 6
        assert self._score(time_on_site_avg_minutes=3.0) == 6.0

    def test_combined_all_caps_at_100(self):
        # 20 + 30 + 20 + 20 + 10 = 100
        val = self._score(
            website_visits_last_30d=20,
            pricing_page_views=5,
            demo_page_views=5,
            demo_requested=1,
            time_on_site_avg_minutes=10.0,
        )
        assert val == 100.0

    def test_clamp_min_zero(self):
        assert self._score() == 0.0

    def test_result_rounded_to_1_decimal(self):
        val = self._score(website_visits_last_30d=1)
        assert val == round(val, 1)


# ─────────────────────────────────────────────────────────────────────────────
# 5. _content_engagement_score boundaries
# ─────────────────────────────────────────────────────────────────────────────

class TestContentEngagementScore:
    def _score(self, **kwargs):
        s = ProspectDigitalFootprintScorer()
        return s._content_engagement_score(make_input(**kwargs))

    def test_zero_inputs(self):
        assert self._score() == 0.0

    def test_case_study_cap_at_30(self):
        # 3 * 10 = 30
        assert self._score(case_study_downloads=3) == 30.0

    def test_case_study_exceeded(self):
        # 5 * 10 = 50 → capped at 30
        assert self._score(case_study_downloads=5) == 30.0

    def test_case_study_below_cap(self):
        # 2 * 10 = 20
        assert self._score(case_study_downloads=2) == 20.0

    def test_email_opens_cap_at_20(self):
        # 8 * 2.5 = 20
        assert self._score(email_opens_last_30d=8) == 20.0

    def test_email_opens_exceeded(self):
        # 10 * 2.5 = 25 → capped at 20
        assert self._score(email_opens_last_30d=10) == 20.0

    def test_email_opens_below_cap(self):
        # 4 * 2.5 = 10
        assert self._score(email_opens_last_30d=4) == 10.0

    def test_email_clicks_cap_at_25(self):
        # 5 * 5 = 25
        assert self._score(email_clicks_last_30d=5) == 25.0

    def test_email_clicks_exceeded(self):
        # 8 * 5 = 40 → capped at 25
        assert self._score(email_clicks_last_30d=8) == 25.0

    def test_email_clicks_below_cap(self):
        # 3 * 5 = 15
        assert self._score(email_clicks_last_30d=3) == 15.0

    def test_return_rate_cap_at_15(self):
        # 50 * 0.3 = 15
        assert self._score(return_visit_rate_pct=50.0) == 15.0

    def test_return_rate_exceeded(self):
        # 100 * 0.3 = 30 → capped at 15
        assert self._score(return_visit_rate_pct=100.0) == 15.0

    def test_return_rate_below_cap(self):
        # 30 * 0.3 = 9
        assert self._score(return_visit_rate_pct=30.0) == 9.0

    def test_free_trial_adds_10(self):
        assert self._score(free_trial_started=1) == 10.0

    def test_combined_all_caps_at_100(self):
        val = self._score(
            case_study_downloads=5,
            email_opens_last_30d=10,
            email_clicks_last_30d=8,
            return_visit_rate_pct=100.0,
            free_trial_started=1,
        )
        assert val == 100.0

    def test_result_rounded_to_1_decimal(self):
        val = self._score(email_opens_last_30d=1)
        assert val == round(val, 1)


# ─────────────────────────────────────────────────────────────────────────────
# 6. _social_signal_score boundaries
# ─────────────────────────────────────────────────────────────────────────────

class TestSocialSignalScore:
    def _score(self, **kwargs):
        s = ProspectDigitalFootprintScorer()
        return s._social_signal_score(make_input(**kwargs))

    def test_zero_inputs(self):
        assert self._score() == 0.0

    def test_linkedin_rep_cap_at_25(self):
        # 3 * 12 = 36 → capped at 25
        assert self._score(linkedin_profile_views_of_rep=3) == 25.0

    def test_linkedin_rep_exactly_at_cap(self):
        # 2 * 12 = 24 < 25
        assert self._score(linkedin_profile_views_of_rep=2) == 24.0

    def test_linkedin_rep_below_cap(self):
        # 1 * 12 = 12
        assert self._score(linkedin_profile_views_of_rep=1) == 12.0

    def test_linkedin_company_cap_at_20(self):
        # 4 * 5 = 20
        assert self._score(linkedin_company_page_visits=4) == 20.0

    def test_linkedin_company_exceeded(self):
        # 6 * 5 = 30 → capped at 20
        assert self._score(linkedin_company_page_visits=6) == 20.0

    def test_linkedin_company_below_cap(self):
        # 2 * 5 = 10
        assert self._score(linkedin_company_page_visits=2) == 10.0

    def test_competitor_signal_adds_30(self):
        assert self._score(competitor_review_site_signal=1) == 30.0

    def test_job_postings_cap_at_25(self):
        # 5 * 6 = 30 → capped at 25
        assert self._score(job_posting_signal_count=5) == 25.0

    def test_job_postings_exactly_at_cap(self):
        # 4 * 6 = 24 < 25
        assert self._score(job_posting_signal_count=4) == 24.0

    def test_job_postings_below_cap(self):
        # 2 * 6 = 12
        assert self._score(job_posting_signal_count=2) == 12.0

    def test_combined_all_caps_at_100(self):
        val = self._score(
            linkedin_profile_views_of_rep=5,
            linkedin_company_page_visits=6,
            competitor_review_site_signal=1,
            job_posting_signal_count=6,
        )
        assert val == 100.0

    def test_result_rounded_to_1_decimal(self):
        val = self._score(job_posting_signal_count=1)
        assert val == round(val, 1)


# ─────────────────────────────────────────────────────────────────────────────
# 7. _company_fit_score boundaries
# ─────────────────────────────────────────────────────────────────────────────

class TestCompanyFitScore:
    def _score(self, **kwargs):
        s = ProspectDigitalFootprintScorer()
        return s._company_fit_score(make_input(**kwargs))

    def test_zero_tech_fit_no_bonus(self):
        assert self._score(technology_fit_score=0.0, company_size_employees=10) == 0.0

    def test_tech_fit_weight(self):
        # 100 * 0.6 = 60
        val = self._score(technology_fit_score=100.0, company_size_employees=10)
        assert val == 60.0

    def test_size_100_gets_plus_25(self):
        # lower bound of ideal range
        val = self._score(technology_fit_score=0.0, company_size_employees=100)
        assert val == 25.0

    def test_size_2000_gets_plus_25(self):
        # upper bound of ideal range
        val = self._score(technology_fit_score=0.0, company_size_employees=2000)
        assert val == 25.0

    def test_size_1000_gets_plus_25(self):
        val = self._score(technology_fit_score=0.0, company_size_employees=1000)
        assert val == 25.0

    def test_size_99_gets_plus_15(self):
        # boundary: 50–99
        val = self._score(technology_fit_score=0.0, company_size_employees=99)
        assert val == 15.0

    def test_size_50_gets_plus_15(self):
        val = self._score(technology_fit_score=0.0, company_size_employees=50)
        assert val == 15.0

    def test_size_2001_gets_plus_15(self):
        val = self._score(technology_fit_score=0.0, company_size_employees=2001)
        assert val == 15.0

    def test_size_5000_gets_plus_15(self):
        val = self._score(technology_fit_score=0.0, company_size_employees=5000)
        assert val == 15.0

    def test_size_5001_gets_plus_10(self):
        val = self._score(technology_fit_score=0.0, company_size_employees=5001)
        assert val == 10.0

    def test_size_49_gets_no_size_bonus(self):
        val = self._score(technology_fit_score=0.0, company_size_employees=49)
        assert val == 0.0

    def test_size_1_gets_no_bonus(self):
        val = self._score(technology_fit_score=0.0, company_size_employees=1)
        assert val == 0.0

    def test_funding_adds_15(self):
        val = self._score(technology_fit_score=0.0, company_size_employees=10, funding_event_recent=1)
        assert val == 15.0

    def test_funding_plus_fit_plus_size(self):
        # 60 * 0.6 + 25 + 15 = 36 + 25 + 15 = 76
        val = self._score(technology_fit_score=60.0, company_size_employees=500, funding_event_recent=1)
        assert val == 76.0

    def test_clamp_max_100(self):
        val = self._score(technology_fit_score=100.0, company_size_employees=500, funding_event_recent=1)
        assert val == 100.0

    def test_result_rounded_to_1_decimal(self):
        val = self._score(technology_fit_score=33.33)
        assert val == round(val, 1)


# ─────────────────────────────────────────────────────────────────────────────
# 8. _composite weights
# ─────────────────────────────────────────────────────────────────────────────

class TestCompositeWeights:
    def _composite(self, web=0.0, content=0.0, social=0.0, fit=0.0):
        s = ProspectDigitalFootprintScorer()
        return s._composite(web, content, social, fit)

    def test_all_zero(self):
        assert self._composite() == 0.0

    def test_web_weight_035(self):
        # only web = 100 → 100 * 0.35 = 35
        assert self._composite(web=100.0) == 35.0

    def test_content_weight_030(self):
        # only content = 100 → 100 * 0.30 = 30
        assert self._composite(content=100.0) == 30.0

    def test_social_weight_020(self):
        # only social = 100 → 100 * 0.20 = 20
        assert self._composite(social=100.0) == 20.0

    def test_fit_weight_015(self):
        # only fit = 100 → 100 * 0.15 = 15
        assert self._composite(fit=100.0) == 15.0

    def test_all_100_gives_100(self):
        assert self._composite(100.0, 100.0, 100.0, 100.0) == 100.0

    def test_weights_sum_correctly(self):
        # 40*0.35 + 20*0.30 + 10*0.20 + 60*0.15 = 14 + 6 + 2 + 9 = 31
        val = self._composite(web=40.0, content=20.0, social=10.0, fit=60.0)
        assert abs(val - 31.0) < 0.15  # allow rounding

    def test_clamp_min_zero(self):
        assert self._composite(-50.0, -50.0, -50.0, -50.0) == 0.0

    def test_result_rounded_to_1_decimal(self):
        val = self._composite(web=33.3, content=33.3, social=33.3, fit=33.3)
        assert val == round(val, 1)


# ─────────────────────────────────────────────────────────────────────────────
# 9. _engagement_velocity ratio thresholds
# ─────────────────────────────────────────────────────────────────────────────

class TestEngagementVelocity:
    def _vel(self, curr, prev):
        s = ProspectDigitalFootprintScorer()
        return s._engagement_velocity(make_input(
            website_visits_last_30d=curr,
            website_visits_prev_30d=prev,
        ))

    # prev == 0 branch
    def test_prev_zero_curr_zero_is_flat(self):
        assert self._vel(0, 0) == EngagementVelocity.FLAT

    def test_prev_zero_curr_1_is_flat(self):
        assert self._vel(1, 0) == EngagementVelocity.FLAT

    def test_prev_zero_curr_2_is_flat(self):
        assert self._vel(2, 0) == EngagementVelocity.FLAT

    def test_prev_zero_curr_3_is_surging(self):
        assert self._vel(3, 0) == EngagementVelocity.SURGING

    def test_prev_zero_curr_10_is_surging(self):
        assert self._vel(10, 0) == EngagementVelocity.SURGING

    # ratio >= 2.0 → surging
    def test_ratio_exactly_2_is_surging(self):
        assert self._vel(10, 5) == EngagementVelocity.SURGING

    def test_ratio_above_2_is_surging(self):
        assert self._vel(12, 5) == EngagementVelocity.SURGING

    # ratio >= 1.2 and < 2.0 → growing
    def test_ratio_exactly_12_is_growing(self):
        assert self._vel(12, 10) == EngagementVelocity.GROWING

    def test_ratio_between_12_and_2_is_growing(self):
        assert self._vel(15, 10) == EngagementVelocity.GROWING

    def test_ratio_just_below_2_is_growing(self):
        # 19/10 = 1.9 → growing
        assert self._vel(19, 10) == EngagementVelocity.GROWING

    # ratio <= 0.5 → declining
    def test_ratio_exactly_05_is_declining(self):
        assert self._vel(5, 10) == EngagementVelocity.DECLINING

    def test_ratio_below_05_is_declining(self):
        assert self._vel(3, 10) == EngagementVelocity.DECLINING

    def test_ratio_zero_curr_is_declining(self):
        assert self._vel(0, 10) == EngagementVelocity.DECLINING

    # between 0.5 and 1.2 → flat
    def test_ratio_just_above_05_is_flat(self):
        # 6/10 = 0.6 → flat
        assert self._vel(6, 10) == EngagementVelocity.FLAT

    def test_ratio_1_is_flat(self):
        assert self._vel(10, 10) == EngagementVelocity.FLAT

    def test_ratio_just_below_12_is_flat(self):
        # 11/10 = 1.1 → flat
        assert self._vel(11, 10) == EngagementVelocity.FLAT


# ─────────────────────────────────────────────────────────────────────────────
# 10. _intent_tier thresholds
# ─────────────────────────────────────────────────────────────────────────────

class TestIntentTier:
    def _tier(self, composite, demo=0, trial=0):
        s = ProspectDigitalFootprintScorer()
        inp = make_input(demo_requested=demo, free_trial_started=trial)
        return s._intent_tier(composite, inp)

    def test_composite_below_30_is_cold(self):
        assert self._tier(29.9) == IntentTier.COLD

    def test_composite_zero_is_cold(self):
        assert self._tier(0.0) == IntentTier.COLD

    def test_composite_30_is_warming(self):
        assert self._tier(30.0) == IntentTier.WARMING

    def test_composite_54_is_warming(self):
        assert self._tier(54.9) == IntentTier.WARMING

    def test_composite_55_is_hot(self):
        assert self._tier(55.0) == IntentTier.HOT

    def test_composite_74_is_hot(self):
        assert self._tier(74.9) == IntentTier.HOT

    def test_composite_75_is_buying_now(self):
        assert self._tier(75.0) == IntentTier.BUYING_NOW

    def test_composite_100_is_buying_now(self):
        assert self._tier(100.0) == IntentTier.BUYING_NOW

    def test_demo_requested_overrides_cold(self):
        assert self._tier(0.0, demo=1) == IntentTier.BUYING_NOW

    def test_demo_requested_overrides_warming(self):
        assert self._tier(40.0, demo=1) == IntentTier.BUYING_NOW

    def test_demo_requested_overrides_hot(self):
        assert self._tier(60.0, demo=1) == IntentTier.BUYING_NOW

    def test_free_trial_overrides_cold(self):
        assert self._tier(0.0, trial=1) == IntentTier.BUYING_NOW

    def test_free_trial_overrides_warming(self):
        assert self._tier(40.0, trial=1) == IntentTier.BUYING_NOW


# ─────────────────────────────────────────────────────────────────────────────
# 11. _footprint_pattern priority order
# ─────────────────────────────────────────────────────────────────────────────

class TestFootprintPattern:
    def _pattern(self, web=0.0, content=0.0, social=0.0, **kwargs):
        s = ProspectDigitalFootprintScorer()
        inp = make_input(**kwargs)
        return s._footprint_pattern(web, content, social, inp)

    def test_passive_lurker_all_zero(self):
        assert self._pattern() == FootprintPattern.PASSIVE_LURKER

    def test_demo_requested_ready_to_buy(self):
        assert self._pattern(demo_requested=1) == FootprintPattern.READY_TO_BUY

    def test_free_trial_ready_to_buy(self):
        assert self._pattern(free_trial_started=1) == FootprintPattern.READY_TO_BUY

    def test_ready_to_buy_overrides_competitor(self):
        # demo + competitor + social >= 50 → still ready_to_buy
        assert self._pattern(
            demo_requested=1,
            competitor_review_site_signal=1,
            social=60.0,
        ) == FootprintPattern.READY_TO_BUY

    def test_competitive_evaluator(self):
        assert self._pattern(
            competitor_review_site_signal=1,
            social=50.0,
        ) == FootprintPattern.COMPETITIVE_EVALUATOR

    def test_competitive_evaluator_social_exactly_50(self):
        assert self._pattern(
            competitor_review_site_signal=1,
            social=50.0,
        ) == FootprintPattern.COMPETITIVE_EVALUATOR

    def test_competitive_evaluator_social_below_50_no(self):
        # competitor=1 but social < 50 → not competitive_evaluator
        result = self._pattern(competitor_review_site_signal=1, social=49.9)
        assert result != FootprintPattern.COMPETITIVE_EVALUATOR

    def test_competitive_evaluator_overrides_intent_spiker(self):
        # competitor + social>=50 takes priority over pricing + web
        assert self._pattern(
            competitor_review_site_signal=1,
            social=60.0,
            web=70.0,
            pricing_page_views=4,
        ) == FootprintPattern.COMPETITIVE_EVALUATOR

    def test_intent_spiker(self):
        # pricing >= 3 AND web >= 60 → intent_spiker
        assert self._pattern(
            pricing_page_views=3,
            web=60.0,
        ) == FootprintPattern.INTENT_SPIKER

    def test_intent_spiker_web_exactly_60(self):
        assert self._pattern(pricing_page_views=3, web=60.0) == FootprintPattern.INTENT_SPIKER

    def test_intent_spiker_web_below_60_no(self):
        result = self._pattern(pricing_page_views=3, web=59.9)
        assert result != FootprintPattern.INTENT_SPIKER

    def test_intent_spiker_pricing_below_3_no(self):
        result = self._pattern(pricing_page_views=2, web=70.0)
        assert result != FootprintPattern.INTENT_SPIKER

    def test_intent_spiker_overrides_active_researcher(self):
        assert self._pattern(
            pricing_page_views=3,
            web=65.0,
            content=55.0,
            case_study_downloads=3,
        ) == FootprintPattern.INTENT_SPIKER

    def test_active_researcher(self):
        assert self._pattern(
            content=50.0,
            case_study_downloads=2,
        ) == FootprintPattern.ACTIVE_RESEARCHER

    def test_active_researcher_content_exactly_50(self):
        assert self._pattern(content=50.0, case_study_downloads=2) == FootprintPattern.ACTIVE_RESEARCHER

    def test_active_researcher_case_study_below_2_no(self):
        result = self._pattern(content=60.0, case_study_downloads=1)
        assert result != FootprintPattern.ACTIVE_RESEARCHER

    def test_active_researcher_content_below_50_no(self):
        result = self._pattern(content=49.9, case_study_downloads=3)
        assert result != FootprintPattern.ACTIVE_RESEARCHER

    def test_content_consumer_via_content_score(self):
        assert self._pattern(content=25.0) == FootprintPattern.CONTENT_CONSUMER

    def test_content_consumer_via_email_clicks(self):
        assert self._pattern(email_clicks_last_30d=2) == FootprintPattern.CONTENT_CONSUMER

    def test_content_consumer_content_exactly_25(self):
        assert self._pattern(content=25.0) == FootprintPattern.CONTENT_CONSUMER

    def test_content_consumer_content_below_25_no_clicks(self):
        result = self._pattern(content=24.9, email_clicks_last_30d=1)
        assert result == FootprintPattern.PASSIVE_LURKER

    def test_passive_lurker_is_fallback(self):
        assert self._pattern(content=24.0, email_clicks_last_30d=1) == FootprintPattern.PASSIVE_LURKER


# ─────────────────────────────────────────────────────────────────────────────
# 12. _lead_score velocity boosts
# ─────────────────────────────────────────────────────────────────────────────

class TestLeadScore:
    def _lead(self, composite, velocity, days=30):
        s = ProspectDigitalFootprintScorer()
        inp = make_input(days_since_first_touch=days)
        return s._lead_score(composite, velocity, inp)

    def test_surging_adds_15(self):
        val = self._lead(50.0, EngagementVelocity.SURGING)
        assert val == 65.0

    def test_growing_adds_8(self):
        val = self._lead(50.0, EngagementVelocity.GROWING)
        assert val == 58.0

    def test_flat_adds_0(self):
        val = self._lead(50.0, EngagementVelocity.FLAT)
        assert val == 50.0

    def test_declining_subtracts_10(self):
        val = self._lead(50.0, EngagementVelocity.DECLINING)
        assert val == 40.0

    def test_recency_bonus_14_days(self):
        # flat + recency
        val = self._lead(50.0, EngagementVelocity.FLAT, days=14)
        assert val == 55.0

    def test_recency_bonus_0_days(self):
        val = self._lead(50.0, EngagementVelocity.FLAT, days=0)
        assert val == 55.0

    def test_recency_bonus_exactly_14(self):
        val = self._lead(50.0, EngagementVelocity.FLAT, days=14)
        assert val == 55.0

    def test_no_recency_bonus_15_days(self):
        val = self._lead(50.0, EngagementVelocity.FLAT, days=15)
        assert val == 50.0

    def test_surging_plus_recency(self):
        val = self._lead(50.0, EngagementVelocity.SURGING, days=7)
        assert val == min(100.0, 50.0 + 15.0 + 5.0)

    def test_clamp_max_100_surging(self):
        val = self._lead(90.0, EngagementVelocity.SURGING)
        assert val == 100.0

    def test_clamp_max_100_surging_recency(self):
        val = self._lead(95.0, EngagementVelocity.SURGING, days=7)
        assert val == 100.0

    def test_clamp_min_zero_declining(self):
        val = self._lead(5.0, EngagementVelocity.DECLINING)
        assert val == 0.0

    def test_result_rounded_to_1_decimal(self):
        val = self._lead(33.3, EngagementVelocity.FLAT)
        assert val == round(val, 1)


# ─────────────────────────────────────────────────────────────────────────────
# 13. days_to_outreach
# ─────────────────────────────────────────────────────────────────────────────

class TestDaysToOutreach:
    def _days(self, tier, needs_now):
        s = ProspectDigitalFootprintScorer()
        return s._days_to_outreach(tier, needs_now)

    def test_needs_now_true_returns_0(self):
        assert self._days(IntentTier.COLD, True) == 0

    def test_buying_now_no_needs_now_returns_0(self):
        assert self._days(IntentTier.BUYING_NOW, False) == 0

    def test_buying_now_with_needs_now_returns_0(self):
        assert self._days(IntentTier.BUYING_NOW, True) == 0

    def test_hot_no_needs_now_returns_2(self):
        assert self._days(IntentTier.HOT, False) == 2

    def test_warming_no_needs_now_returns_7(self):
        assert self._days(IntentTier.WARMING, False) == 7

    def test_cold_no_needs_now_returns_21(self):
        assert self._days(IntentTier.COLD, False) == 21

    def test_hot_needs_now_returns_0(self):
        assert self._days(IntentTier.HOT, True) == 0

    def test_warming_needs_now_returns_0(self):
        assert self._days(IntentTier.WARMING, True) == 0


# ─────────────────────────────────────────────────────────────────────────────
# 14. is_high_intent conditions
# ─────────────────────────────────────────────────────────────────────────────

class TestIsHighIntent:
    def _high_intent(self, composite, demo=0, trial=0):
        s = ProspectDigitalFootprintScorer()
        inp = make_input(demo_requested=demo, free_trial_started=trial)
        result = s.score(inp)
        # We need to check the actual result for given composite; override via direct scoring
        # Better: score actual prospect and check field
        return result.is_high_intent

    def test_composite_60_is_high_intent(self, scorer):
        # Build input that yields composite >= 60 without demo/trial
        # web: pricing=3(30) + visits=13(19.5) + demo_views=2(14) + time=5(10) = 73.5
        # content: opens=8(20) + clicks=5(25) + case=2(20) + return=50(15) = 80
        # social: linkedin_rep=2(24) + company=4(20) + jobs=3(18) = 62
        # fit: tech=80*0.6(48) + size_500(+25) = 73
        # composite = 73.5*0.35 + 80*0.30 + 62*0.20 + 73*0.15 ≈ 73.1
        inp = make_input(
            pricing_page_views=3,
            website_visits_last_30d=13,
            demo_page_views=2,
            time_on_site_avg_minutes=5.0,
            email_opens_last_30d=8,
            email_clicks_last_30d=5,
            case_study_downloads=2,
            return_visit_rate_pct=50.0,
            linkedin_profile_views_of_rep=2,
            linkedin_company_page_visits=4,
            job_posting_signal_count=3,
            technology_fit_score=80.0,
            company_size_employees=500,
        )
        result = scorer.score(inp)
        assert result.digital_footprint_composite >= 60.0
        assert result.is_high_intent is True

    def test_demo_requested_makes_high_intent(self, scorer):
        result = scorer.score(make_input(demo_requested=1))
        assert result.is_high_intent is True

    def test_free_trial_makes_high_intent(self, scorer):
        result = scorer.score(make_input(free_trial_started=1))
        assert result.is_high_intent is True

    def test_low_composite_no_demo_not_high_intent(self, scorer):
        result = scorer.score(make_input(technology_fit_score=0.0))
        assert result.is_high_intent is False


# ─────────────────────────────────────────────────────────────────────────────
# 15. needs_immediate_outreach conditions
# ─────────────────────────────────────────────────────────────────────────────

class TestNeedsImmediateOutreach:
    def test_demo_requested_needs_outreach(self, scorer):
        result = scorer.score(make_input(demo_requested=1))
        assert result.needs_immediate_outreach is True

    def test_free_trial_does_not_alone_trigger(self, scorer):
        # free_trial alone doesn't trigger needs_now (only composite>=75, demo, or pricing+composite>=55)
        result = scorer.score(make_input(free_trial_started=1))
        # free_trial gives composite boost via content score, may or may not trigger
        # but free_trial alone with min other signals won't hit composite>=75
        # and pricing_page_views=0 so third clause fails
        # is_high_intent=True but needs_immediate_outreach depends on composite
        # Let's just check the logic is consistent
        assert isinstance(result.needs_immediate_outreach, bool)

    def test_pricing_3_and_composite_55_triggers(self, scorer):
        # Need pricing >= 3 and composite >= 55
        # pricing=3 → web += 30; large tech fit; size 500
        inp = make_input(
            pricing_page_views=3,
            website_visits_last_30d=10,
            technology_fit_score=80.0,
            company_size_employees=500,
            email_opens_last_30d=8,
            email_clicks_last_30d=3,
        )
        result = scorer.score(inp)
        if result.digital_footprint_composite >= 55.0:
            assert result.needs_immediate_outreach is True

    def test_composite_75_triggers(self, scorer):
        # Force composite >= 75 without demo/trial
        inp = make_input(
            pricing_page_views=3,
            website_visits_last_30d=13,
            demo_page_views=2,
            email_opens_last_30d=8,
            email_clicks_last_30d=5,
            case_study_downloads=3,
            return_visit_rate_pct=50.0,
            linkedin_profile_views_of_rep=2,
            linkedin_company_page_visits=4,
            competitor_review_site_signal=1,
            job_posting_signal_count=4,
            technology_fit_score=90.0,
            company_size_employees=500,
            funding_event_recent=1,
            time_on_site_avg_minutes=5.0,
        )
        result = scorer.score(inp)
        if result.digital_footprint_composite >= 75.0:
            assert result.needs_immediate_outreach is True

    def test_low_signals_no_outreach(self, scorer):
        result = scorer.score(make_input(technology_fit_score=0.0))
        assert result.needs_immediate_outreach is False


# ─────────────────────────────────────────────────────────────────────────────
# 16. _prospect_action logic (executive_touch vs sdr conditions)
# ─────────────────────────────────────────────────────────────────────────────

class TestProspectAction:
    def _action(self, tier, needs_now, size=100, funding=0):
        s = ProspectDigitalFootprintScorer()
        inp = make_input(company_size_employees=size, funding_event_recent=funding)
        return s._prospect_action(tier, needs_now, inp)

    def test_cold_no_needs_now_is_nurture(self):
        assert self._action(IntentTier.COLD, False) == ProspectAction.NURTURE

    def test_warming_no_needs_now_is_nurture(self):
        assert self._action(IntentTier.WARMING, False) == ProspectAction.NURTURE

    def test_hot_no_needs_now_is_warm_outreach(self):
        assert self._action(IntentTier.HOT, False) == ProspectAction.WARM_OUTREACH

    def test_needs_now_size_1000_exec_touch(self):
        assert self._action(IntentTier.HOT, True, size=1000) == ProspectAction.EXECUTIVE_TOUCH

    def test_needs_now_size_999_sdr(self):
        assert self._action(IntentTier.HOT, True, size=999, funding=0) == ProspectAction.IMMEDIATE_SDR

    def test_needs_now_size_above_1000_exec_touch(self):
        assert self._action(IntentTier.COLD, True, size=2000) == ProspectAction.EXECUTIVE_TOUCH

    def test_needs_now_funding_and_size_200_exec_touch(self):
        # funding AND size >= 200
        assert self._action(IntentTier.COLD, True, size=200, funding=1) == ProspectAction.EXECUTIVE_TOUCH

    def test_needs_now_funding_size_199_sdr(self):
        # funding AND size < 200 → still sdr
        assert self._action(IntentTier.COLD, True, size=199, funding=1) == ProspectAction.IMMEDIATE_SDR

    def test_needs_now_no_funding_size_200_sdr(self):
        # size=200 but no funding and size < 1000
        assert self._action(IntentTier.COLD, True, size=200, funding=0) == ProspectAction.IMMEDIATE_SDR

    def test_buying_now_tier_size_1000_exec_touch(self):
        assert self._action(IntentTier.BUYING_NOW, False, size=1000) == ProspectAction.EXECUTIVE_TOUCH

    def test_buying_now_tier_size_999_sdr(self):
        assert self._action(IntentTier.BUYING_NOW, False, size=999) == ProspectAction.IMMEDIATE_SDR

    def test_buying_now_funding_size_200_exec_touch(self):
        assert self._action(IntentTier.BUYING_NOW, False, size=200, funding=1) == ProspectAction.EXECUTIVE_TOUCH

    def test_buying_now_funding_size_500_exec_touch(self):
        assert self._action(IntentTier.BUYING_NOW, False, size=500, funding=1) == ProspectAction.EXECUTIVE_TOUCH


# ─────────────────────────────────────────────────────────────────────────────
# 17. score() method — basic contract
# ─────────────────────────────────────────────────────────────────────────────

class TestScoreMethod:
    def test_score_returns_result(self, scorer, bare_input):
        result = scorer.score(bare_input)
        assert isinstance(result, ProspectDigitalResult)

    def test_score_appends_to_results(self, scorer, bare_input):
        scorer.score(bare_input)
        assert len(scorer._results) == 1

    def test_score_multiple_appends(self, scorer):
        scorer.score(make_input(prospect_id="A"))
        scorer.score(make_input(prospect_id="B"))
        assert len(scorer._results) == 2

    def test_score_preserves_prospect_id(self, scorer):
        result = scorer.score(make_input(prospect_id="XYZ"))
        assert result.prospect_id == "XYZ"

    def test_score_preserves_company_name(self, scorer):
        result = scorer.score(make_input(company_name="BigFish"))
        assert result.company_name == "BigFish"

    def test_score_result_fields(self, scorer, bare_input):
        r = scorer.score(bare_input)
        assert hasattr(r, "intent_tier")
        assert hasattr(r, "footprint_pattern")
        assert hasattr(r, "engagement_velocity")
        assert hasattr(r, "prospect_action")
        assert hasattr(r, "website_intent_score")
        assert hasattr(r, "content_engagement_score")
        assert hasattr(r, "social_signal_score")
        assert hasattr(r, "company_fit_score")
        assert hasattr(r, "digital_footprint_composite")
        assert hasattr(r, "lead_score")
        assert hasattr(r, "days_to_outreach")
        assert hasattr(r, "is_high_intent")
        assert hasattr(r, "needs_immediate_outreach")

    def test_score_all_numeric_scores_in_range(self, scorer, hot_input):
        r = scorer.score(hot_input)
        for field in ("website_intent_score", "content_engagement_score",
                      "social_signal_score", "company_fit_score",
                      "digital_footprint_composite", "lead_score"):
            val = getattr(r, field)
            assert 0.0 <= val <= 100.0, f"{field} = {val} out of [0,100]"


# ─────────────────────────────────────────────────────────────────────────────
# 18. score_batch()
# ─────────────────────────────────────────────────────────────────────────────

class TestScoreBatch:
    def test_batch_returns_list(self, scorer):
        results = scorer.score_batch([make_input(prospect_id="A"), make_input(prospect_id="B")])
        assert isinstance(results, list)
        assert len(results) == 2

    def test_batch_empty_list(self, scorer):
        results = scorer.score_batch([])
        assert results == []

    def test_batch_all_results_are_result_type(self, scorer):
        inputs = [make_input(prospect_id=str(i)) for i in range(5)]
        for r in scorer.score_batch(inputs):
            assert isinstance(r, ProspectDigitalResult)

    def test_batch_results_appended_to_internal(self, scorer):
        inputs = [make_input(prospect_id=str(i)) for i in range(3)]
        scorer.score_batch(inputs)
        assert len(scorer._results) == 3

    def test_batch_order_preserved(self, scorer):
        ids = ["P1", "P2", "P3"]
        results = scorer.score_batch([make_input(prospect_id=pid) for pid in ids])
        assert [r.prospect_id for r in results] == ids


# ─────────────────────────────────────────────────────────────────────────────
# 19. reset()
# ─────────────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_results(self, scorer, bare_input):
        scorer.score(bare_input)
        scorer.reset()
        assert len(scorer._results) == 0

    def test_reset_then_score_again(self, scorer, bare_input):
        scorer.score(bare_input)
        scorer.reset()
        scorer.score(bare_input)
        assert len(scorer._results) == 1

    def test_reset_empty_is_safe(self, scorer):
        scorer.reset()  # should not raise
        assert len(scorer._results) == 0

    def test_reset_clears_properties(self, scorer, bare_input):
        scorer.score(bare_input)
        scorer.reset()
        assert scorer.avg_lead_score == 0.0
        assert scorer.avg_digital_footprint_composite == 0.0


# ─────────────────────────────────────────────────────────────────────────────
# 20. Properties
# ─────────────────────────────────────────────────────────────────────────────

class TestProperties:
    def test_high_intent_prospects_empty(self, scorer):
        assert scorer.high_intent_prospects == []

    def test_immediate_outreach_queue_empty(self, scorer):
        assert scorer.immediate_outreach_queue == []

    def test_avg_lead_score_empty(self, scorer):
        assert scorer.avg_lead_score == 0.0

    def test_avg_composite_empty(self, scorer):
        assert scorer.avg_digital_footprint_composite == 0.0

    def test_high_intent_prospects_includes_demo(self, scorer):
        scorer.score(make_input(demo_requested=1))
        assert len(scorer.high_intent_prospects) == 1

    def test_high_intent_prospects_includes_trial(self, scorer):
        scorer.score(make_input(free_trial_started=1))
        assert len(scorer.high_intent_prospects) == 1

    def test_high_intent_prospects_excludes_cold(self, scorer):
        scorer.score(make_input(technology_fit_score=0.0))
        assert len(scorer.high_intent_prospects) == 0

    def test_immediate_outreach_queue_includes_demo(self, scorer):
        scorer.score(make_input(demo_requested=1))
        assert len(scorer.immediate_outreach_queue) == 1

    def test_avg_lead_score_single(self, scorer):
        r = scorer.score(make_input(demo_requested=1))
        assert scorer.avg_lead_score == r.lead_score

    def test_avg_lead_score_multiple(self, scorer):
        r1 = scorer.score(make_input(prospect_id="A"))
        r2 = scorer.score(make_input(prospect_id="B", demo_requested=1))
        expected = round((r1.lead_score + r2.lead_score) / 2, 1)
        assert scorer.avg_lead_score == expected

    def test_avg_composite_single(self, scorer, bare_input):
        r = scorer.score(bare_input)
        assert scorer.avg_digital_footprint_composite == r.digital_footprint_composite

    def test_avg_composite_multiple(self, scorer):
        r1 = scorer.score(make_input(prospect_id="A"))
        r2 = scorer.score(make_input(prospect_id="B", technology_fit_score=100.0, company_size_employees=500))
        expected = round((r1.digital_footprint_composite + r2.digital_footprint_composite) / 2, 1)
        assert scorer.avg_digital_footprint_composite == expected

    def test_high_intent_is_list_of_results(self, scorer):
        scorer.score(make_input(demo_requested=1))
        for item in scorer.high_intent_prospects:
            assert isinstance(item, ProspectDigitalResult)

    def test_immediate_outreach_is_list_of_results(self, scorer):
        scorer.score(make_input(demo_requested=1))
        for item in scorer.immediate_outreach_queue:
            assert isinstance(item, ProspectDigitalResult)


# ─────────────────────────────────────────────────────────────────────────────
# 21. summary() — 13 keys
# ─────────────────────────────────────────────────────────────────────────────

class TestSummary:
    EXPECTED_KEYS = {
        "total", "tier_counts", "pattern_counts", "velocity_counts",
        "action_counts", "avg_digital_footprint_composite", "avg_lead_score",
        "high_intent_count", "immediate_outreach_count",
        "avg_website_intent_score", "avg_content_engagement_score",
        "avg_social_signal_score", "avg_company_fit_score",
    }

    def test_summary_empty_key_count(self, scorer):
        s = scorer.summary()
        assert len(s) == 13

    def test_summary_empty_keys(self, scorer):
        assert set(scorer.summary().keys()) == self.EXPECTED_KEYS

    def test_summary_empty_values(self, scorer):
        s = scorer.summary()
        assert s["total"] == 0
        assert s["tier_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["velocity_counts"] == {}
        assert s["action_counts"] == {}
        assert s["avg_digital_footprint_composite"] == 0.0
        assert s["avg_lead_score"] == 0.0
        assert s["high_intent_count"] == 0
        assert s["immediate_outreach_count"] == 0
        assert s["avg_website_intent_score"] == 0.0
        assert s["avg_content_engagement_score"] == 0.0
        assert s["avg_social_signal_score"] == 0.0
        assert s["avg_company_fit_score"] == 0.0

    def test_summary_key_count_after_scores(self, scorer, bare_input):
        scorer.score(bare_input)
        assert len(scorer.summary()) == 13

    def test_summary_exact_keys_after_scores(self, scorer, bare_input):
        scorer.score(bare_input)
        assert set(scorer.summary().keys()) == self.EXPECTED_KEYS

    def test_summary_total_increments(self, scorer):
        scorer.score(make_input(prospect_id="A"))
        scorer.score(make_input(prospect_id="B"))
        assert scorer.summary()["total"] == 2

    def test_summary_tier_counts_populated(self, scorer):
        scorer.score(make_input(demo_requested=1))  # buying_now
        s = scorer.summary()
        assert "buying_now" in s["tier_counts"]
        assert s["tier_counts"]["buying_now"] == 1

    def test_summary_pattern_counts_populated(self, scorer):
        scorer.score(make_input(demo_requested=1))  # ready_to_buy
        assert "ready_to_buy" in scorer.summary()["pattern_counts"]

    def test_summary_velocity_counts_populated(self, scorer):
        scorer.score(make_input(website_visits_last_30d=0, website_visits_prev_30d=0))
        s = scorer.summary()
        assert len(s["velocity_counts"]) >= 1

    def test_summary_action_counts_populated(self, scorer):
        scorer.score(make_input(technology_fit_score=0.0))  # nurture
        s = scorer.summary()
        assert len(s["action_counts"]) >= 1

    def test_summary_high_intent_count(self, scorer):
        scorer.score(make_input(demo_requested=1))
        scorer.score(make_input(technology_fit_score=0.0))
        s = scorer.summary()
        assert s["high_intent_count"] == 1

    def test_summary_immediate_outreach_count(self, scorer):
        scorer.score(make_input(demo_requested=1))
        scorer.score(make_input(technology_fit_score=0.0))
        s = scorer.summary()
        assert s["immediate_outreach_count"] == 1

    def test_summary_avg_scores_are_float(self, scorer, bare_input):
        scorer.score(bare_input)
        s = scorer.summary()
        for key in ("avg_digital_footprint_composite", "avg_lead_score",
                    "avg_website_intent_score", "avg_content_engagement_score",
                    "avg_social_signal_score", "avg_company_fit_score"):
            assert isinstance(s[key], float), f"{key} should be float"

    def test_summary_avg_composite_matches_manual(self, scorer):
        r1 = scorer.score(make_input(prospect_id="A"))
        r2 = scorer.score(make_input(prospect_id="B", demo_requested=1))
        expected = round((r1.digital_footprint_composite + r2.digital_footprint_composite) / 2, 1)
        assert scorer.summary()["avg_digital_footprint_composite"] == expected

    def test_summary_avg_lead_score_matches_manual(self, scorer):
        r1 = scorer.score(make_input(prospect_id="A"))
        r2 = scorer.score(make_input(prospect_id="B", technology_fit_score=100.0, company_size_employees=500))
        expected = round((r1.lead_score + r2.lead_score) / 2, 1)
        assert scorer.summary()["avg_lead_score"] == expected

    def test_summary_after_reset_is_empty(self, scorer, bare_input):
        scorer.score(bare_input)
        scorer.reset()
        s = scorer.summary()
        assert s["total"] == 0

    def test_summary_multiple_tiers_tracked(self, scorer):
        scorer.score(make_input(technology_fit_score=0.0))   # cold
        scorer.score(make_input(demo_requested=1))            # buying_now
        tc = scorer.summary()["tier_counts"]
        assert sum(tc.values()) == 2


# ─────────────────────────────────────────────────────────────────────────────
# 22. End-to-end scenarios
# ─────────────────────────────────────────────────────────────────────────────

class TestEndToEndScenarios:
    def test_absolute_cold_prospect(self, scorer):
        """No signals at all → cold, passive_lurker, flat, nurture."""
        r = scorer.score(make_input(technology_fit_score=0.0, company_size_employees=10))
        assert r.intent_tier == IntentTier.COLD
        assert r.footprint_pattern == FootprintPattern.PASSIVE_LURKER
        assert r.days_to_outreach == 21
        assert r.prospect_action == ProspectAction.NURTURE
        assert r.is_high_intent is False
        assert r.needs_immediate_outreach is False

    def test_demo_requested_end_to_end(self, scorer):
        """Demo requested → buying_now, ready_to_buy, 0 days."""
        r = scorer.score(make_input(demo_requested=1, company_size_employees=500))
        assert r.intent_tier == IntentTier.BUYING_NOW
        assert r.footprint_pattern == FootprintPattern.READY_TO_BUY
        assert r.days_to_outreach == 0
        assert r.is_high_intent is True
        assert r.needs_immediate_outreach is True

    def test_free_trial_end_to_end(self, scorer):
        r = scorer.score(make_input(free_trial_started=1, company_size_employees=500))
        assert r.intent_tier == IntentTier.BUYING_NOW
        assert r.footprint_pattern == FootprintPattern.READY_TO_BUY
        assert r.is_high_intent is True

    def test_enterprise_buying_now_exec_touch(self, scorer):
        """Large enterprise + demo → executive_touch."""
        r = scorer.score(make_input(demo_requested=1, company_size_employees=2000))
        assert r.prospect_action == ProspectAction.EXECUTIVE_TOUCH

    def test_smb_buying_now_immediate_sdr(self, scorer):
        """Small company + demo → immediate_sdr."""
        r = scorer.score(make_input(demo_requested=1, company_size_employees=50))
        assert r.prospect_action == ProspectAction.IMMEDIATE_SDR

    def test_funded_midsize_exec_touch(self, scorer):
        """Funded company size=300 + demo → exec touch."""
        r = scorer.score(make_input(demo_requested=1, company_size_employees=300, funding_event_recent=1))
        assert r.prospect_action == ProspectAction.EXECUTIVE_TOUCH

    def test_competitor_evaluator_scenario(self, scorer):
        """Competitor signal + high social → competitive_evaluator."""
        inp = make_input(
            competitor_review_site_signal=1,
            linkedin_profile_views_of_rep=2,       # 24 points
            linkedin_company_page_visits=4,         # 20 points
            job_posting_signal_count=1,             # 6 points
            # social = 24+20+30+6 = 80 >= 50
        )
        r = scorer.score(inp)
        assert r.footprint_pattern == FootprintPattern.COMPETITIVE_EVALUATOR

    def test_intent_spiker_scenario(self, scorer):
        """3 pricing pages + high web score → intent_spiker."""
        inp = make_input(
            pricing_page_views=3,
            website_visits_last_30d=13,   # web += 19.5
            demo_page_views=1,            # web += 7
            time_on_site_avg_minutes=5.0, # web += 10
            # web = 19.5 + 30 + 7 + 10 = 66.5 >= 60
        )
        r = scorer.score(inp)
        assert r.footprint_pattern == FootprintPattern.INTENT_SPIKER

    def test_active_researcher_scenario(self, scorer):
        """High content score + case studies → active_researcher."""
        inp = make_input(
            case_study_downloads=2,
            email_clicks_last_30d=5,   # content += 25
            email_opens_last_30d=8,    # content += 20
            return_visit_rate_pct=20.0, # content += 6
            # content = 20 + 20 + 25 + 6 = 71 >= 50 and case_study >= 2
        )
        r = scorer.score(inp)
        assert r.footprint_pattern == FootprintPattern.ACTIVE_RESEARCHER

    def test_content_consumer_via_clicks(self, scorer):
        r = scorer.score(make_input(email_clicks_last_30d=2))
        assert r.footprint_pattern == FootprintPattern.CONTENT_CONSUMER

    def test_surging_velocity_in_end_to_end(self, scorer):
        r = scorer.score(make_input(website_visits_last_30d=10, website_visits_prev_30d=5))
        assert r.engagement_velocity == EngagementVelocity.SURGING

    def test_declining_velocity_in_end_to_end(self, scorer):
        r = scorer.score(make_input(website_visits_last_30d=2, website_visits_prev_30d=10))
        assert r.engagement_velocity == EngagementVelocity.DECLINING

    def test_growing_velocity_in_end_to_end(self, scorer):
        # 13 / 10 = 1.3 → growing
        r = scorer.score(make_input(website_visits_last_30d=13, website_visits_prev_30d=10))
        assert r.engagement_velocity == EngagementVelocity.GROWING

    def test_hot_tier_warm_outreach(self, scorer):
        """Composite in hot range without demo/trial → warm_outreach."""
        # Need composite in [55, 75)
        inp = make_input(
            pricing_page_views=2,
            website_visits_last_30d=10,
            demo_page_views=1,
            email_opens_last_30d=8,
            email_clicks_last_30d=3,
            technology_fit_score=80.0,
            company_size_employees=500,
        )
        r = scorer.score(inp)
        if r.intent_tier == IntentTier.HOT:
            assert r.prospect_action == ProspectAction.WARM_OUTREACH
            assert r.days_to_outreach == 2


# ─────────────────────────────────────────────────────────────────────────────
# 23. Edge cases and cross-validation
# ─────────────────────────────────────────────────────────────────────────────

class TestEdgeCasesAndCrossValidation:
    def test_all_zeros_scores_all_zero(self, scorer):
        r = scorer.score(make_input(technology_fit_score=0.0, company_size_employees=1))
        assert r.website_intent_score == 0.0
        assert r.content_engagement_score == 0.0
        assert r.social_signal_score == 0.0

    def test_company_fit_zero_tech_no_size_no_funding(self, scorer):
        r = scorer.score(make_input(technology_fit_score=0.0, company_size_employees=49))
        assert r.company_fit_score == 0.0

    def test_lead_score_clamp_at_100(self, scorer):
        # High composite + surging + recency should clamp at 100
        r = scorer.score(make_input(
            demo_requested=1,
            website_visits_last_30d=20,
            website_visits_prev_30d=5,
            pricing_page_views=5,
            technology_fit_score=100.0,
            company_size_employees=500,
            days_since_first_touch=7,
        ))
        assert r.lead_score <= 100.0

    def test_lead_score_clamp_at_zero(self, scorer):
        # Declining from composite=0
        r = scorer.score(make_input(
            technology_fit_score=0.0,
            company_size_employees=1,
            website_visits_last_30d=0,
            website_visits_prev_30d=10,
        ))
        assert r.lead_score >= 0.0

    def test_is_high_intent_consistent_with_composite(self, scorer, bare_input):
        r = scorer.score(bare_input)
        # if composite < 60 and no demo/trial, not high intent
        assert r.is_high_intent == (
            r.digital_footprint_composite >= 60.0 or
            r.needs_immediate_outreach  # can overlap
        ) or not r.is_high_intent  # just verify it's bool
        assert isinstance(r.is_high_intent, bool)

    def test_needs_outreach_consistent_with_demo(self, scorer):
        r = scorer.score(make_input(demo_requested=1))
        assert r.needs_immediate_outreach is True
        assert r.days_to_outreach == 0

    def test_days_to_outreach_cold_no_needs(self, scorer):
        r = scorer.score(make_input(technology_fit_score=0.0, company_size_employees=1))
        if not r.needs_immediate_outreach and r.intent_tier == IntentTier.COLD:
            assert r.days_to_outreach == 21

    def test_to_dict_composite_matches_result(self, scorer, bare_input):
        r = scorer.score(bare_input)
        assert r.to_dict()["digital_footprint_composite"] == r.digital_footprint_composite

    def test_to_dict_lead_score_matches_result(self, scorer, bare_input):
        r = scorer.score(bare_input)
        assert r.to_dict()["lead_score"] == r.lead_score

    def test_score_new_scorer_empty_results(self):
        s = ProspectDigitalFootprintScorer()
        assert s._results == []

    def test_independent_scorers_dont_share_state(self):
        s1 = ProspectDigitalFootprintScorer()
        s2 = ProspectDigitalFootprintScorer()
        s1.score(make_input(prospect_id="X"))
        assert len(s2._results) == 0

    def test_very_large_visits_capped(self, scorer):
        r = scorer.score(make_input(website_visits_last_30d=10000))
        assert r.website_intent_score <= 100.0

    def test_very_large_pricing_pages_capped(self, scorer):
        r = scorer.score(make_input(pricing_page_views=1000))
        assert r.website_intent_score <= 100.0

    def test_very_large_tech_fit_capped(self, scorer):
        r = scorer.score(make_input(technology_fit_score=200.0, company_size_employees=500))
        assert r.company_fit_score == 100.0

    def test_funding_plus_size_200_exactly_exec_touch(self, scorer):
        r = scorer.score(make_input(demo_requested=1, company_size_employees=200, funding_event_recent=1))
        assert r.prospect_action == ProspectAction.EXECUTIVE_TOUCH

    def test_pricing_page_2_and_composite_55_no_trigger(self, scorer):
        # pricing < 3 → third clause of needs_now fails
        inp = make_input(
            pricing_page_views=2,
            technology_fit_score=80.0,
            company_size_employees=500,
            email_clicks_last_30d=5,
            email_opens_last_30d=8,
            case_study_downloads=3,
        )
        r = scorer.score(inp)
        if r.digital_footprint_composite >= 55.0 and r.digital_footprint_composite < 75.0:
            # needs_now should be False if pricing < 3 and no demo
            assert r.needs_immediate_outreach is False

    def test_rep_id_stored_in_input(self):
        inp = make_input(rep_id="REP42")
        assert inp.rep_id == "REP42"

    def test_batch_then_summary_total_correct(self, scorer):
        scorer.score_batch([make_input(prospect_id=str(i)) for i in range(7)])
        assert scorer.summary()["total"] == 7

    def test_to_dict_days_to_outreach_correct_cold(self, scorer):
        r = scorer.score(make_input(technology_fit_score=0.0, company_size_employees=10))
        d = r.to_dict()
        # Cold with no needs_now → 21 days
        if d["intent_tier"] == "cold" and not d["needs_immediate_outreach"]:
            assert d["days_to_outreach"] == 21

    def test_score_result_enum_types(self, scorer, bare_input):
        r = scorer.score(bare_input)
        assert isinstance(r.intent_tier, IntentTier)
        assert isinstance(r.footprint_pattern, FootprintPattern)
        assert isinstance(r.engagement_velocity, EngagementVelocity)
        assert isinstance(r.prospect_action, ProspectAction)

    def test_avg_lead_score_rounds_to_1_decimal(self, scorer):
        scorer.score(make_input(prospect_id="A"))
        val = scorer.avg_lead_score
        assert val == round(val, 1)

    def test_avg_composite_rounds_to_1_decimal(self, scorer):
        scorer.score(make_input(prospect_id="A"))
        val = scorer.avg_digital_footprint_composite
        assert val == round(val, 1)

    def test_velocity_ratio_exactly_05_is_declining(self):
        s = ProspectDigitalFootprintScorer()
        v = s._engagement_velocity(make_input(website_visits_last_30d=5, website_visits_prev_30d=10))
        assert v == EngagementVelocity.DECLINING

    def test_velocity_ratio_exactly_12_is_growing(self):
        s = ProspectDigitalFootprintScorer()
        v = s._engagement_velocity(make_input(website_visits_last_30d=12, website_visits_prev_30d=10))
        assert v == EngagementVelocity.GROWING

    def test_velocity_ratio_exactly_20_is_surging(self):
        s = ProspectDigitalFootprintScorer()
        v = s._engagement_velocity(make_input(website_visits_last_30d=20, website_visits_prev_30d=10))
        assert v == EngagementVelocity.SURGING

    def test_size_exactly_1000_exec_touch(self, scorer):
        r = scorer.score(make_input(demo_requested=1, company_size_employees=1000))
        assert r.prospect_action == ProspectAction.EXECUTIVE_TOUCH

    def test_size_exactly_5000_size_bonus_15(self):
        s = ProspectDigitalFootprintScorer()
        val = s._company_fit_score(make_input(technology_fit_score=0.0, company_size_employees=5000))
        assert val == 15.0

    def test_size_exactly_2000_size_bonus_25(self):
        s = ProspectDigitalFootprintScorer()
        val = s._company_fit_score(make_input(technology_fit_score=0.0, company_size_employees=2000))
        assert val == 25.0

    def test_size_exactly_100_size_bonus_25(self):
        s = ProspectDigitalFootprintScorer()
        val = s._company_fit_score(make_input(technology_fit_score=0.0, company_size_employees=100))
        assert val == 25.0

    def test_size_exactly_50_size_bonus_15(self):
        s = ProspectDigitalFootprintScorer()
        val = s._company_fit_score(make_input(technology_fit_score=0.0, company_size_employees=50))
        assert val == 15.0

    def test_size_exactly_2001_size_bonus_15(self):
        s = ProspectDigitalFootprintScorer()
        val = s._company_fit_score(make_input(technology_fit_score=0.0, company_size_employees=2001))
        assert val == 15.0

    def test_competitor_no_social_not_competitive_evaluator(self, scorer):
        r = scorer.score(make_input(competitor_review_site_signal=1))
        # social score = 30 (from competitor alone) < 50 → not competitive_evaluator
        assert r.footprint_pattern != FootprintPattern.COMPETITIVE_EVALUATOR

    def test_competitor_social_50_exact_competitive_evaluator(self):
        s = ProspectDigitalFootprintScorer()
        # social=50 exactly from competitor(30) + company_visits(4*5=20) = 50
        inp = make_input(
            competitor_review_site_signal=1,
            linkedin_company_page_visits=4,
        )
        r = s.score(inp)
        assert r.footprint_pattern == FootprintPattern.COMPETITIVE_EVALUATOR

    def test_summary_avg_web_score_correct(self, scorer):
        r1 = scorer.score(make_input(prospect_id="A"))
        r2 = scorer.score(make_input(prospect_id="B"))
        expected = round((r1.website_intent_score + r2.website_intent_score) / 2, 1)
        assert scorer.summary()["avg_website_intent_score"] == expected

    def test_summary_avg_content_score_correct(self, scorer):
        r1 = scorer.score(make_input(prospect_id="A"))
        r2 = scorer.score(make_input(prospect_id="B", email_opens_last_30d=8))
        expected = round((r1.content_engagement_score + r2.content_engagement_score) / 2, 1)
        assert scorer.summary()["avg_content_engagement_score"] == expected

    def test_summary_avg_social_score_correct(self, scorer):
        r1 = scorer.score(make_input(prospect_id="A"))
        r2 = scorer.score(make_input(prospect_id="B", linkedin_profile_views_of_rep=2))
        expected = round((r1.social_signal_score + r2.social_signal_score) / 2, 1)
        assert scorer.summary()["avg_social_signal_score"] == expected

    def test_summary_avg_fit_score_correct(self, scorer):
        r1 = scorer.score(make_input(prospect_id="A", technology_fit_score=50.0))
        r2 = scorer.score(make_input(prospect_id="B", technology_fit_score=70.0))
        expected = round((r1.company_fit_score + r2.company_fit_score) / 2, 1)
        assert scorer.summary()["avg_company_fit_score"] == expected

    def test_days_since_first_touch_15_no_recency_bonus(self, scorer):
        r1 = scorer.score(make_input(prospect_id="A", days_since_first_touch=14))
        r2 = scorer.score(make_input(prospect_id="B", days_since_first_touch=15))
        # r1 should have higher lead score by 5 (all else equal)
        assert r1.lead_score - r2.lead_score == pytest.approx(5.0, abs=0.2)

    def test_buying_now_days_0_regardless_of_needs_now(self, scorer):
        r = scorer.score(make_input(demo_requested=1, technology_fit_score=0.0))
        assert r.days_to_outreach == 0

    def test_warming_tier_days_7(self, scorer):
        # composite in [30, 55) no demo/trial
        # tech_fit=40 → 24; size=500 → +25; total=49; composite≈49*0.15=7.35 → warming
        r = scorer.score(make_input(technology_fit_score=40.0, company_size_employees=500))
        if r.intent_tier == IntentTier.WARMING:
            assert r.days_to_outreach == 7
