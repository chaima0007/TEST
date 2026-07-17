"""Comprehensive tests for Module 23 — Lead Scoring Intelligence Engine."""
from __future__ import annotations

import pytest

from swarm.intelligence.lead_scoring_intelligence import (
    FitScore,
    IntentSignal,
    LeadAction,
    LeadProfile,
    LeadScoringIntelligenceEngine,
    LeadScoringResult,
    LeadTier,
    _action,
    _compute_lead_score,
    _disqualification_reasons,
    _engagement_score,
    _fit_score_label,
    _icp_score,
    _intent_signal,
    _qualification_score,
    _recommended_steps,
    _strengths,
    _tier,
    _weaknesses,
)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def make_lead(
    lead_id: str = "l1",
    company: str = "Acme",
    contact_name: str = "John Doe",
    segment: str = "enterprise",
    icp_industry_match: bool = True,
    icp_size_match: bool = True,
    icp_revenue_match: bool = True,
    icp_geography_match: bool = True,
    tech_stack_match: bool = True,
    website_visits: int = 10,
    email_opens: int = 5,
    email_clicks: int = 3,
    content_downloads: int = 2,
    demo_requested: bool = True,
    pricing_page_visits: int = 3,
    budget_confirmed: bool = True,
    authority_confirmed: bool = True,
    need_confirmed: bool = True,
    timeline_confirmed: bool = True,
    competitor_customer: bool = False,
    out_of_territory: bool = False,
    unsubscribed: bool = False,
    days_in_funnel: int = 30,
    lead_source: str = "inbound",
) -> LeadProfile:
    return LeadProfile(
        lead_id=lead_id,
        company=company,
        contact_name=contact_name,
        segment=segment,
        icp_industry_match=icp_industry_match,
        icp_size_match=icp_size_match,
        icp_revenue_match=icp_revenue_match,
        icp_geography_match=icp_geography_match,
        tech_stack_match=tech_stack_match,
        website_visits=website_visits,
        email_opens=email_opens,
        email_clicks=email_clicks,
        content_downloads=content_downloads,
        demo_requested=demo_requested,
        pricing_page_visits=pricing_page_visits,
        budget_confirmed=budget_confirmed,
        authority_confirmed=authority_confirmed,
        need_confirmed=need_confirmed,
        timeline_confirmed=timeline_confirmed,
        competitor_customer=competitor_customer,
        out_of_territory=out_of_territory,
        unsubscribed=unsubscribed,
        days_in_funnel=days_in_funnel,
        lead_source=lead_source,
    )


# ---------------------------------------------------------------------------
# Class 1: TestLeadTierEnum
# ---------------------------------------------------------------------------

class TestLeadTierEnum:
    def test_hot_value(self):
        assert LeadTier.HOT.value == "hot"

    def test_warm_value(self):
        assert LeadTier.WARM.value == "warm"

    def test_cold_value(self):
        assert LeadTier.COLD.value == "cold"

    def test_dead_value(self):
        assert LeadTier.DEAD.value == "dead"

    def test_four_members(self):
        assert len(LeadTier) == 4

    def test_is_str_enum(self):
        assert isinstance(LeadTier.HOT, str)

    def test_str_comparison_hot(self):
        assert LeadTier.HOT == "hot"

    def test_str_comparison_warm(self):
        assert LeadTier.WARM == "warm"

    def test_str_comparison_cold(self):
        assert LeadTier.COLD == "cold"

    def test_str_comparison_dead(self):
        assert LeadTier.DEAD == "dead"

    def test_membership(self):
        members = list(LeadTier)
        assert LeadTier.HOT in members
        assert LeadTier.WARM in members
        assert LeadTier.COLD in members
        assert LeadTier.DEAD in members

    def test_unique_values(self):
        values = [t.value for t in LeadTier]
        assert len(values) == len(set(values))


# ---------------------------------------------------------------------------
# Class 2: TestLeadActionEnum
# ---------------------------------------------------------------------------

class TestLeadActionEnum:
    def test_call_now_value(self):
        assert LeadAction.CALL_NOW.value == "call_now"

    def test_nurture_value(self):
        assert LeadAction.NURTURE.value == "nurture"

    def test_qualify_value(self):
        assert LeadAction.QUALIFY.value == "qualify"

    def test_disqualify_value(self):
        assert LeadAction.DISQUALIFY.value == "disqualify"

    def test_assign_ae_value(self):
        assert LeadAction.ASSIGN_AE.value == "assign_ae"

    def test_five_members(self):
        assert len(LeadAction) == 5

    def test_is_str_enum(self):
        assert isinstance(LeadAction.CALL_NOW, str)

    def test_str_comparison(self):
        assert LeadAction.NURTURE == "nurture"

    def test_unique_values(self):
        values = [a.value for a in LeadAction]
        assert len(values) == len(set(values))

    def test_membership(self):
        members = list(LeadAction)
        assert LeadAction.DISQUALIFY in members

    def test_str_comparison_assign_ae(self):
        assert LeadAction.ASSIGN_AE == "assign_ae"

    def test_str_comparison_qualify(self):
        assert LeadAction.QUALIFY == "qualify"


# ---------------------------------------------------------------------------
# Class 3: TestFitScoreEnum
# ---------------------------------------------------------------------------

class TestFitScoreEnum:
    def test_excellent_value(self):
        assert FitScore.EXCELLENT.value == "excellent"

    def test_good_value(self):
        assert FitScore.GOOD.value == "good"

    def test_fair_value(self):
        assert FitScore.FAIR.value == "fair"

    def test_poor_value(self):
        assert FitScore.POOR.value == "poor"

    def test_four_members(self):
        assert len(FitScore) == 4

    def test_is_str_enum(self):
        assert isinstance(FitScore.EXCELLENT, str)

    def test_str_comparison(self):
        assert FitScore.POOR == "poor"

    def test_unique_values(self):
        values = [f.value for f in FitScore]
        assert len(values) == len(set(values))

    def test_membership(self):
        assert FitScore.GOOD in list(FitScore)

    def test_str_comparison_fair(self):
        assert FitScore.FAIR == "fair"


# ---------------------------------------------------------------------------
# Class 4: TestIntentSignalEnum
# ---------------------------------------------------------------------------

class TestIntentSignalEnum:
    def test_high_intent_value(self):
        assert IntentSignal.HIGH_INTENT.value == "high_intent"

    def test_medium_intent_value(self):
        assert IntentSignal.MEDIUM_INTENT.value == "medium_intent"

    def test_low_intent_value(self):
        assert IntentSignal.LOW_INTENT.value == "low_intent"

    def test_no_intent_value(self):
        assert IntentSignal.NO_INTENT.value == "no_intent"

    def test_four_members(self):
        assert len(IntentSignal) == 4

    def test_is_str_enum(self):
        assert isinstance(IntentSignal.HIGH_INTENT, str)

    def test_str_comparison(self):
        assert IntentSignal.NO_INTENT == "no_intent"

    def test_unique_values(self):
        values = [i.value for i in IntentSignal]
        assert len(values) == len(set(values))

    def test_membership(self):
        assert IntentSignal.MEDIUM_INTENT in list(IntentSignal)

    def test_str_comparison_low(self):
        assert IntentSignal.LOW_INTENT == "low_intent"


# ---------------------------------------------------------------------------
# Class 5: TestLeadProfileDataclass
# ---------------------------------------------------------------------------

class TestLeadProfileDataclass:
    def test_creates_with_all_fields(self):
        lead = make_lead()
        assert lead.lead_id == "l1"

    def test_company_field(self):
        lead = make_lead(company="Beta Corp")
        assert lead.company == "Beta Corp"

    def test_contact_name_field(self):
        lead = make_lead(contact_name="Jane Smith")
        assert lead.contact_name == "Jane Smith"

    def test_segment_field(self):
        lead = make_lead(segment="smb")
        assert lead.segment == "smb"

    def test_icp_industry_match_true(self):
        lead = make_lead(icp_industry_match=True)
        assert lead.icp_industry_match is True

    def test_icp_industry_match_false(self):
        lead = make_lead(icp_industry_match=False)
        assert lead.icp_industry_match is False

    def test_icp_size_match_field(self):
        lead = make_lead(icp_size_match=False)
        assert lead.icp_size_match is False

    def test_icp_revenue_match_field(self):
        lead = make_lead(icp_revenue_match=False)
        assert lead.icp_revenue_match is False

    def test_icp_geography_match_field(self):
        lead = make_lead(icp_geography_match=False)
        assert lead.icp_geography_match is False

    def test_tech_stack_match_field(self):
        lead = make_lead(tech_stack_match=False)
        assert lead.tech_stack_match is False

    def test_website_visits_field(self):
        lead = make_lead(website_visits=7)
        assert lead.website_visits == 7

    def test_email_opens_field(self):
        lead = make_lead(email_opens=3)
        assert lead.email_opens == 3

    def test_email_clicks_field(self):
        lead = make_lead(email_clicks=2)
        assert lead.email_clicks == 2

    def test_content_downloads_field(self):
        lead = make_lead(content_downloads=0)
        assert lead.content_downloads == 0

    def test_demo_requested_field(self):
        lead = make_lead(demo_requested=False)
        assert lead.demo_requested is False

    def test_pricing_page_visits_field(self):
        lead = make_lead(pricing_page_visits=5)
        assert lead.pricing_page_visits == 5

    def test_budget_confirmed_field(self):
        lead = make_lead(budget_confirmed=False)
        assert lead.budget_confirmed is False

    def test_authority_confirmed_field(self):
        lead = make_lead(authority_confirmed=False)
        assert lead.authority_confirmed is False

    def test_need_confirmed_field(self):
        lead = make_lead(need_confirmed=False)
        assert lead.need_confirmed is False

    def test_timeline_confirmed_field(self):
        lead = make_lead(timeline_confirmed=False)
        assert lead.timeline_confirmed is False

    def test_competitor_customer_field(self):
        lead = make_lead(competitor_customer=True)
        assert lead.competitor_customer is True

    def test_out_of_territory_field(self):
        lead = make_lead(out_of_territory=True)
        assert lead.out_of_territory is True

    def test_unsubscribed_field(self):
        lead = make_lead(unsubscribed=True)
        assert lead.unsubscribed is True

    def test_days_in_funnel_field(self):
        lead = make_lead(days_in_funnel=200)
        assert lead.days_in_funnel == 200

    def test_lead_source_field(self):
        lead = make_lead(lead_source="referral")
        assert lead.lead_source == "referral"


# ---------------------------------------------------------------------------
# Class 6: TestLeadScoringResultToDict
# ---------------------------------------------------------------------------

class TestLeadScoringResultToDict:
    def setup_method(self):
        self.engine = LeadScoringIntelligenceEngine()
        self.result = self.engine.score(make_lead())
        self.d = self.result.to_dict()

    def test_returns_dict(self):
        assert isinstance(self.d, dict)

    def test_lead_id_key(self):
        assert "lead_id" in self.d

    def test_company_key(self):
        assert "company" in self.d

    def test_contact_name_key(self):
        assert "contact_name" in self.d

    def test_segment_key(self):
        assert "segment" in self.d

    def test_lead_source_key(self):
        assert "lead_source" in self.d

    def test_lead_score_key(self):
        assert "lead_score" in self.d

    def test_fit_score_label_is_string(self):
        assert isinstance(self.d["fit_score_label"], str)
        assert not isinstance(self.d["fit_score_label"], FitScore)

    def test_intent_signal_is_string(self):
        assert isinstance(self.d["intent_signal"], str)
        assert not isinstance(self.d["intent_signal"], IntentSignal)

    def test_tier_is_string(self):
        assert isinstance(self.d["tier"], str)
        assert not isinstance(self.d["tier"], LeadTier)

    def test_action_is_string(self):
        assert isinstance(self.d["action"], str)
        assert not isinstance(self.d["action"], LeadAction)

    def test_fit_breakdown_key(self):
        assert "fit_breakdown" in self.d
        assert isinstance(self.d["fit_breakdown"], dict)

    def test_strengths_is_list(self):
        assert isinstance(self.d["strengths"], list)

    def test_weaknesses_is_list(self):
        assert isinstance(self.d["weaknesses"], list)

    def test_recommended_steps_is_list(self):
        assert isinstance(self.d["recommended_steps"], list)

    def test_disqualification_reasons_is_list(self):
        assert isinstance(self.d["disqualification_reasons"], list)

    def test_no_enum_objects_in_dict(self):
        from enum import Enum
        for val in self.d.values():
            assert not isinstance(val, Enum)

    def test_lead_id_value(self):
        assert self.d["lead_id"] == "l1"

    def test_company_value(self):
        assert self.d["company"] == "Acme"


# ---------------------------------------------------------------------------
# Class 7: TestICPScore
# ---------------------------------------------------------------------------

class TestICPScore:
    def test_all_true_gives_35(self):
        lead = make_lead()
        assert _icp_score(lead) == 35.0

    def test_industry_match_adds_10(self):
        lead_on = make_lead(icp_industry_match=True, icp_size_match=False,
                            icp_revenue_match=False, icp_geography_match=False,
                            tech_stack_match=False)
        lead_off = make_lead(icp_industry_match=False, icp_size_match=False,
                             icp_revenue_match=False, icp_geography_match=False,
                             tech_stack_match=False)
        assert _icp_score(lead_on) - _icp_score(lead_off) == 10

    def test_size_match_adds_8(self):
        lead_on = make_lead(icp_industry_match=False, icp_size_match=True,
                            icp_revenue_match=False, icp_geography_match=False,
                            tech_stack_match=False)
        lead_off = make_lead(icp_industry_match=False, icp_size_match=False,
                             icp_revenue_match=False, icp_geography_match=False,
                             tech_stack_match=False)
        assert _icp_score(lead_on) - _icp_score(lead_off) == 8

    def test_revenue_match_adds_8(self):
        lead_on = make_lead(icp_industry_match=False, icp_size_match=False,
                            icp_revenue_match=True, icp_geography_match=False,
                            tech_stack_match=False)
        lead_off = make_lead(icp_industry_match=False, icp_size_match=False,
                             icp_revenue_match=False, icp_geography_match=False,
                             tech_stack_match=False)
        assert _icp_score(lead_on) - _icp_score(lead_off) == 8

    def test_geography_match_adds_5(self):
        lead_on = make_lead(icp_industry_match=False, icp_size_match=False,
                            icp_revenue_match=False, icp_geography_match=True,
                            tech_stack_match=False)
        lead_off = make_lead(icp_industry_match=False, icp_size_match=False,
                             icp_revenue_match=False, icp_geography_match=False,
                             tech_stack_match=False)
        assert _icp_score(lead_on) - _icp_score(lead_off) == 5

    def test_tech_stack_match_adds_4(self):
        lead_on = make_lead(icp_industry_match=False, icp_size_match=False,
                            icp_revenue_match=False, icp_geography_match=False,
                            tech_stack_match=True)
        lead_off = make_lead(icp_industry_match=False, icp_size_match=False,
                             icp_revenue_match=False, icp_geography_match=False,
                             tech_stack_match=False)
        assert _icp_score(lead_on) - _icp_score(lead_off) == 4

    def test_all_false_gives_zero(self):
        lead = make_lead(icp_industry_match=False, icp_size_match=False,
                         icp_revenue_match=False, icp_geography_match=False,
                         tech_stack_match=False)
        assert _icp_score(lead) == 0.0

    def test_partial_industry_and_size(self):
        lead = make_lead(icp_industry_match=True, icp_size_match=True,
                         icp_revenue_match=False, icp_geography_match=False,
                         tech_stack_match=False)
        assert _icp_score(lead) == 18.0

    def test_additive_industry_revenue_geo(self):
        lead = make_lead(icp_industry_match=True, icp_size_match=False,
                         icp_revenue_match=True, icp_geography_match=True,
                         tech_stack_match=False)
        assert _icp_score(lead) == 23.0

    def test_returns_float(self):
        lead = make_lead()
        assert isinstance(_icp_score(lead), float)

    def test_only_tech_stack(self):
        lead = make_lead(icp_industry_match=False, icp_size_match=False,
                         icp_revenue_match=False, icp_geography_match=False,
                         tech_stack_match=True)
        assert _icp_score(lead) == 4.0

    def test_industry_plus_tech_stack(self):
        lead = make_lead(icp_industry_match=True, icp_size_match=False,
                         icp_revenue_match=False, icp_geography_match=False,
                         tech_stack_match=True)
        assert _icp_score(lead) == 14.0


# ---------------------------------------------------------------------------
# Class 8: TestEngagementScoreWebsite
# ---------------------------------------------------------------------------

class TestEngagementScoreWebsite:
    """Test website_visits thresholds in isolation (all other signals zeroed)."""

    def _base(self, visits: int) -> LeadProfile:
        return make_lead(
            website_visits=visits,
            email_opens=0, email_clicks=0,
            content_downloads=0, demo_requested=False,
            pricing_page_visits=0,
        )

    def test_visits_gte_10_gives_10(self):
        assert _engagement_score(self._base(10)) == 10

    def test_visits_15_gives_10(self):
        assert _engagement_score(self._base(15)) == 10

    def test_visits_exactly_5_gives_6(self):
        assert _engagement_score(self._base(5)) == 6

    def test_visits_7_gives_6(self):
        assert _engagement_score(self._base(7)) == 6

    def test_visits_exactly_2_gives_3(self):
        assert _engagement_score(self._base(2)) == 3

    def test_visits_4_gives_3(self):
        assert _engagement_score(self._base(4)) == 3

    def test_visits_1_gives_0(self):
        assert _engagement_score(self._base(1)) == 0

    def test_visits_0_gives_0(self):
        assert _engagement_score(self._base(0)) == 0

    def test_visits_9_gives_6(self):
        assert _engagement_score(self._base(9)) == 6

    def test_visits_10_exactly_at_boundary(self):
        assert _engagement_score(self._base(10)) == 10

    def test_visits_5_exactly_at_boundary(self):
        assert _engagement_score(self._base(5)) == 6

    def test_visits_2_exactly_at_boundary(self):
        assert _engagement_score(self._base(2)) == 3


# ---------------------------------------------------------------------------
# Class 9: TestEngagementScoreEmail
# ---------------------------------------------------------------------------

class TestEngagementScoreEmail:
    """Test email engagement thresholds (email_eng = opens + clicks*2)."""

    def _base(self, opens: int, clicks: int) -> LeadProfile:
        return make_lead(
            website_visits=0,
            email_opens=opens, email_clicks=clicks,
            content_downloads=0, demo_requested=False,
            pricing_page_visits=0,
        )

    def test_eng_gte_10_gives_8_via_opens(self):
        # opens=10 → eng=10
        assert _engagement_score(self._base(10, 0)) == 8

    def test_eng_gte_10_gives_8_via_clicks(self):
        # clicks=5 → eng=10
        assert _engagement_score(self._base(0, 5)) == 8

    def test_eng_gte_10_via_mixed(self):
        # opens=4, clicks=3 → eng=10
        assert _engagement_score(self._base(4, 3)) == 8

    def test_clicks_multiplier_is_2(self):
        # opens=0, clicks=3 → eng=6 → +5
        assert _engagement_score(self._base(0, 3)) == 5

    def test_eng_exactly_5_gives_5(self):
        # opens=5 → eng=5
        assert _engagement_score(self._base(5, 0)) == 5

    def test_eng_6_gives_5(self):
        # opens=6 → eng=6
        assert _engagement_score(self._base(6, 0)) == 5

    def test_eng_exactly_2_gives_2(self):
        # opens=2 → eng=2
        assert _engagement_score(self._base(2, 0)) == 2

    def test_eng_3_gives_2(self):
        # opens=3 → eng=3
        assert _engagement_score(self._base(3, 0)) == 2

    def test_eng_1_gives_0(self):
        # opens=1 → eng=1
        assert _engagement_score(self._base(1, 0)) == 0

    def test_eng_0_gives_0(self):
        assert _engagement_score(self._base(0, 0)) == 0

    def test_eng_gte_10_boundary(self):
        # opens=8, clicks=1 → eng=10
        assert _engagement_score(self._base(8, 1)) == 8

    def test_eng_9_gives_5(self):
        # opens=9 → eng=9
        assert _engagement_score(self._base(9, 0)) == 5


# ---------------------------------------------------------------------------
# Class 10: TestEngagementScoreContentDemo
# ---------------------------------------------------------------------------

class TestEngagementScoreContentDemo:
    """Test demo, content_downloads, and pricing_page thresholds."""

    def _base(self, **kwargs) -> LeadProfile:
        defaults = dict(website_visits=0, email_opens=0, email_clicks=0,
                        content_downloads=0, demo_requested=False, pricing_page_visits=0)
        defaults.update(kwargs)
        return make_lead(**defaults)

    def test_demo_requested_adds_6(self):
        with_demo = _engagement_score(self._base(demo_requested=True))
        without_demo = _engagement_score(self._base(demo_requested=False))
        assert with_demo - without_demo == 6

    def test_demo_requested_false_adds_0(self):
        assert _engagement_score(self._base(demo_requested=False)) == 0

    def test_content_downloads_2_adds_4(self):
        lead = self._base(content_downloads=2)
        assert _engagement_score(lead) == 4

    def test_content_downloads_3_adds_4(self):
        lead = self._base(content_downloads=3)
        assert _engagement_score(lead) == 4

    def test_content_downloads_1_adds_2(self):
        lead = self._base(content_downloads=1)
        assert _engagement_score(lead) == 2

    def test_content_downloads_0_adds_0(self):
        lead = self._base(content_downloads=0)
        assert _engagement_score(lead) == 0

    def test_pricing_page_visits_3_adds_7(self):
        lead = self._base(pricing_page_visits=3)
        assert _engagement_score(lead) == 7

    def test_pricing_page_visits_5_adds_7(self):
        lead = self._base(pricing_page_visits=5)
        assert _engagement_score(lead) == 7

    def test_pricing_page_visits_1_adds_4(self):
        lead = self._base(pricing_page_visits=1)
        assert _engagement_score(lead) == 4

    def test_pricing_page_visits_2_adds_4(self):
        lead = self._base(pricing_page_visits=2)
        assert _engagement_score(lead) == 4

    def test_pricing_page_visits_0_adds_0(self):
        lead = self._base(pricing_page_visits=0)
        assert _engagement_score(lead) == 0

    def test_demo_plus_pricing_3_plus_content_2(self):
        lead = self._base(demo_requested=True, pricing_page_visits=3, content_downloads=2)
        # 6 + 7 + 4 = 17
        assert _engagement_score(lead) == 17


# ---------------------------------------------------------------------------
# Class 11: TestEngagementScoreTotal
# ---------------------------------------------------------------------------

class TestEngagementScoreTotal:
    def test_maximum_35_points(self):
        # visits>=10(+10), email_eng>=10(+8), demo(+6), downloads>=2(+4), pricing>=3(+7) = 35
        lead = make_lead(
            website_visits=10, email_opens=10, email_clicks=0,
            content_downloads=2, demo_requested=True, pricing_page_visits=3,
        )
        assert _engagement_score(lead) == 35.0

    def test_zero_engagement(self):
        lead = make_lead(
            website_visits=0, email_opens=0, email_clicks=0,
            content_downloads=0, demo_requested=False, pricing_page_visits=0,
        )
        assert _engagement_score(lead) == 0

    def test_returns_float(self):
        lead = make_lead()
        assert isinstance(_engagement_score(lead), float)

    def test_partial_engagement(self):
        # visits=5(+6), email_eng=5(+5), demo=False, content=1(+2), pricing=1(+4) = 17
        lead = make_lead(
            website_visits=5, email_opens=5, email_clicks=0,
            content_downloads=1, demo_requested=False, pricing_page_visits=1,
        )
        assert _engagement_score(lead) == 17.0

    def test_capped_not_exceeded(self):
        lead = make_lead(
            website_visits=100, email_opens=100, email_clicks=100,
            content_downloads=100, demo_requested=True, pricing_page_visits=100,
        )
        # max is 35
        assert _engagement_score(lead) == 35.0

    def test_additive_no_double_count(self):
        lead = make_lead(
            website_visits=10, email_opens=0, email_clicks=0,
            content_downloads=0, demo_requested=True, pricing_page_visits=0,
        )
        # 10 (visits) + 6 (demo) = 16
        assert _engagement_score(lead) == 16.0

    def test_pricing_2_gives_4(self):
        lead = make_lead(
            website_visits=0, email_opens=0, email_clicks=0,
            content_downloads=0, demo_requested=False, pricing_page_visits=2,
        )
        assert _engagement_score(lead) == 4.0


# ---------------------------------------------------------------------------
# Class 12: TestQualificationScore
# ---------------------------------------------------------------------------

class TestQualificationScore:
    def test_all_confirmed_gives_30(self):
        lead = make_lead(budget_confirmed=True, authority_confirmed=True,
                         need_confirmed=True, timeline_confirmed=True)
        assert _qualification_score(lead) == 30.0

    def test_budget_confirmed_adds_10(self):
        on = _qualification_score(make_lead(budget_confirmed=True, authority_confirmed=False,
                                            need_confirmed=False, timeline_confirmed=False))
        off = _qualification_score(make_lead(budget_confirmed=False, authority_confirmed=False,
                                             need_confirmed=False, timeline_confirmed=False))
        assert on - off == 10

    def test_authority_confirmed_adds_8(self):
        on = _qualification_score(make_lead(budget_confirmed=False, authority_confirmed=True,
                                            need_confirmed=False, timeline_confirmed=False))
        off = _qualification_score(make_lead(budget_confirmed=False, authority_confirmed=False,
                                             need_confirmed=False, timeline_confirmed=False))
        assert on - off == 8

    def test_need_confirmed_adds_8(self):
        on = _qualification_score(make_lead(budget_confirmed=False, authority_confirmed=False,
                                            need_confirmed=True, timeline_confirmed=False))
        off = _qualification_score(make_lead(budget_confirmed=False, authority_confirmed=False,
                                             need_confirmed=False, timeline_confirmed=False))
        assert on - off == 8

    def test_timeline_confirmed_adds_4(self):
        on = _qualification_score(make_lead(budget_confirmed=False, authority_confirmed=False,
                                            need_confirmed=False, timeline_confirmed=True))
        off = _qualification_score(make_lead(budget_confirmed=False, authority_confirmed=False,
                                             need_confirmed=False, timeline_confirmed=False))
        assert on - off == 4

    def test_none_confirmed_gives_zero(self):
        lead = make_lead(budget_confirmed=False, authority_confirmed=False,
                         need_confirmed=False, timeline_confirmed=False)
        assert _qualification_score(lead) == 0.0

    def test_returns_float(self):
        lead = make_lead()
        assert isinstance(_qualification_score(lead), float)

    def test_budget_and_authority_gives_18(self):
        lead = make_lead(budget_confirmed=True, authority_confirmed=True,
                         need_confirmed=False, timeline_confirmed=False)
        assert _qualification_score(lead) == 18.0

    def test_need_and_timeline_gives_12(self):
        lead = make_lead(budget_confirmed=False, authority_confirmed=False,
                         need_confirmed=True, timeline_confirmed=True)
        assert _qualification_score(lead) == 12.0

    def test_bant_additive(self):
        # budget(10) + authority(8) + need(8) + timeline(4) = 30
        lead = make_lead(budget_confirmed=True, authority_confirmed=True,
                         need_confirmed=True, timeline_confirmed=True)
        assert _qualification_score(lead) == 30.0


# ---------------------------------------------------------------------------
# Class 13: TestNegativeDeductions
# ---------------------------------------------------------------------------

class TestNegativeDeductions:
    def _perfect_lead(self, **kwargs) -> LeadProfile:
        """A lead with max ICP+engagement+qualification = 100 pts raw."""
        return make_lead(**kwargs)

    def test_competitor_customer_deducts_15(self):
        score_with, _ = _compute_lead_score(self._perfect_lead(competitor_customer=True))
        score_without, _ = _compute_lead_score(self._perfect_lead(competitor_customer=False))
        assert score_without - score_with == 15

    def test_out_of_territory_deducts_20(self):
        score_with, _ = _compute_lead_score(self._perfect_lead(out_of_territory=True))
        score_without, _ = _compute_lead_score(self._perfect_lead(out_of_territory=False))
        assert score_without - score_with == 20

    def test_unsubscribed_deducts_25(self):
        score_with, _ = _compute_lead_score(self._perfect_lead(unsubscribed=True))
        score_without, _ = _compute_lead_score(self._perfect_lead(unsubscribed=False))
        assert score_without - score_with == 25

    def test_days_in_funnel_gt_180_deducts_10(self):
        score_with, _ = _compute_lead_score(self._perfect_lead(days_in_funnel=181))
        score_without, _ = _compute_lead_score(self._perfect_lead(days_in_funnel=30))
        assert score_without - score_with == 10

    def test_days_in_funnel_gt_90_deducts_5(self):
        score_with, _ = _compute_lead_score(self._perfect_lead(days_in_funnel=91))
        score_without, _ = _compute_lead_score(self._perfect_lead(days_in_funnel=30))
        assert score_without - score_with == 5

    def test_days_in_funnel_180_exact_deducts_5(self):
        # exactly 180 → not > 180, but > 90 → -5
        score_with, _ = _compute_lead_score(self._perfect_lead(days_in_funnel=180))
        score_without, _ = _compute_lead_score(self._perfect_lead(days_in_funnel=30))
        assert score_without - score_with == 5

    def test_days_in_funnel_90_exact_no_deduction(self):
        # exactly 90 → not > 90 → 0 deduction
        score_with, _ = _compute_lead_score(self._perfect_lead(days_in_funnel=90))
        score_without, _ = _compute_lead_score(self._perfect_lead(days_in_funnel=30))
        assert score_without == score_with

    def test_all_negatives_combined_clamp_to_zero(self):
        lead = make_lead(
            icp_industry_match=False, icp_size_match=False,
            icp_revenue_match=False, icp_geography_match=False,
            tech_stack_match=False, website_visits=0, email_opens=0,
            email_clicks=0, content_downloads=0, demo_requested=False,
            pricing_page_visits=0, budget_confirmed=False, authority_confirmed=False,
            need_confirmed=False, timeline_confirmed=False,
            competitor_customer=True, out_of_territory=True, unsubscribed=True,
            days_in_funnel=200,
        )
        score, _ = _compute_lead_score(lead)
        assert score == 0.0

    def test_stale_180_boundary_not_double_penalised(self):
        # days=181 should trigger only the >180 rule (-10), not both
        score_181, _ = _compute_lead_score(self._perfect_lead(days_in_funnel=181))
        score_91, _ = _compute_lead_score(self._perfect_lead(days_in_funnel=91))
        # 181 deducts 10, 91 deducts 5
        assert score_91 - score_181 == 5

    def test_breakdown_contains_icp_engagement_qualification(self):
        _, breakdown = _compute_lead_score(make_lead())
        assert "icp" in breakdown
        assert "engagement" in breakdown
        assert "qualification" in breakdown


# ---------------------------------------------------------------------------
# Class 14: TestScoreClamping
# ---------------------------------------------------------------------------

class TestScoreClamping:
    def test_score_max_100(self):
        lead = make_lead()
        score, _ = _compute_lead_score(lead)
        assert score <= 100.0

    def test_score_min_0(self):
        lead = make_lead(
            icp_industry_match=False, icp_size_match=False,
            icp_revenue_match=False, icp_geography_match=False,
            tech_stack_match=False, website_visits=0, email_opens=0,
            email_clicks=0, content_downloads=0, demo_requested=False,
            pricing_page_visits=0, budget_confirmed=False, authority_confirmed=False,
            need_confirmed=False, timeline_confirmed=False,
            competitor_customer=True, out_of_territory=True, unsubscribed=True,
            days_in_funnel=200,
        )
        score, _ = _compute_lead_score(lead)
        assert score >= 0.0

    def test_score_is_numeric(self):
        lead = make_lead()
        score, _ = _compute_lead_score(lead)
        assert isinstance(score, (int, float))

    def test_score_rounded_to_1dp(self):
        lead = make_lead()
        score, _ = _compute_lead_score(lead)
        assert score == round(score, 1)

    def test_score_clamps_below_zero(self):
        lead = make_lead(
            competitor_customer=True, out_of_territory=True, unsubscribed=True,
            days_in_funnel=200, icp_industry_match=False, icp_size_match=False,
            icp_revenue_match=False, icp_geography_match=False, tech_stack_match=False,
            website_visits=0, email_opens=0, email_clicks=0, content_downloads=0,
            demo_requested=False, pricing_page_visits=0, budget_confirmed=False,
            authority_confirmed=False, need_confirmed=False, timeline_confirmed=False,
        )
        score, _ = _compute_lead_score(lead)
        assert score == 0.0

    def test_perfect_lead_score_is_100(self):
        lead = make_lead()
        score, _ = _compute_lead_score(lead)
        assert score == 100.0

    def test_score_is_float(self):
        # edge: zero score still numeric
        lead = make_lead(
            icp_industry_match=False, icp_size_match=False,
            icp_revenue_match=False, icp_geography_match=False,
            tech_stack_match=False, website_visits=0, email_opens=0,
            email_clicks=0, content_downloads=0, demo_requested=False,
            pricing_page_visits=0, budget_confirmed=False, authority_confirmed=False,
            need_confirmed=False, timeline_confirmed=False,
        )
        score, _ = _compute_lead_score(lead)
        assert isinstance(score, (int, float))


# ---------------------------------------------------------------------------
# Class 15: TestFitScoreLabel
# ---------------------------------------------------------------------------

class TestFitScoreLabel:
    def test_icp_35_is_excellent(self):
        assert _fit_score_label(35.0) == FitScore.EXCELLENT

    def test_icp_30_is_excellent(self):
        assert _fit_score_label(30.0) == FitScore.EXCELLENT

    def test_icp_29_is_good(self):
        assert _fit_score_label(29.0) == FitScore.GOOD

    def test_icp_20_is_good(self):
        assert _fit_score_label(20.0) == FitScore.GOOD

    def test_icp_19_is_fair(self):
        assert _fit_score_label(19.0) == FitScore.FAIR

    def test_icp_10_is_fair(self):
        assert _fit_score_label(10.0) == FitScore.FAIR

    def test_icp_9_is_poor(self):
        assert _fit_score_label(9.0) == FitScore.POOR

    def test_icp_0_is_poor(self):
        assert _fit_score_label(0.0) == FitScore.POOR

    def test_icp_31_is_excellent(self):
        assert _fit_score_label(31.0) == FitScore.EXCELLENT

    def test_icp_21_is_good(self):
        assert _fit_score_label(21.0) == FitScore.GOOD

    def test_icp_11_is_fair(self):
        assert _fit_score_label(11.0) == FitScore.FAIR

    def test_icp_1_is_poor(self):
        assert _fit_score_label(1.0) == FitScore.POOR


# ---------------------------------------------------------------------------
# Class 16: TestIntentSignalLogic
# ---------------------------------------------------------------------------

class TestIntentSignalLogic:
    def test_demo_requested_gives_high_intent(self):
        assert _intent_signal(0.0, True, 0) == IntentSignal.HIGH_INTENT

    def test_pricing_gte_3_gives_high_intent(self):
        assert _intent_signal(0.0, False, 3) == IntentSignal.HIGH_INTENT

    def test_pricing_5_gives_high_intent(self):
        assert _intent_signal(0.0, False, 5) == IntentSignal.HIGH_INTENT

    def test_eng_gte_25_gives_high_intent(self):
        assert _intent_signal(25.0, False, 0) == IntentSignal.HIGH_INTENT

    def test_eng_30_gives_high_intent(self):
        assert _intent_signal(30.0, False, 0) == IntentSignal.HIGH_INTENT

    def test_pricing_1_gives_medium_intent(self):
        assert _intent_signal(0.0, False, 1) == IntentSignal.MEDIUM_INTENT

    def test_pricing_2_gives_medium_intent(self):
        assert _intent_signal(0.0, False, 2) == IntentSignal.MEDIUM_INTENT

    def test_eng_12_gives_medium_intent(self):
        assert _intent_signal(12.0, False, 0) == IntentSignal.MEDIUM_INTENT

    def test_eng_20_gives_medium_intent(self):
        assert _intent_signal(20.0, False, 0) == IntentSignal.MEDIUM_INTENT

    def test_eng_5_gives_low_intent(self):
        assert _intent_signal(5.0, False, 0) == IntentSignal.LOW_INTENT

    def test_eng_11_gives_low_intent(self):
        assert _intent_signal(11.0, False, 0) == IntentSignal.LOW_INTENT

    def test_eng_0_pricing_0_no_demo_gives_no_intent(self):
        assert _intent_signal(0.0, False, 0) == IntentSignal.NO_INTENT

    def test_eng_4_gives_no_intent(self):
        assert _intent_signal(4.0, False, 0) == IntentSignal.NO_INTENT

    def test_demo_overrides_low_eng(self):
        # demo=True should give HIGH regardless of eng
        assert _intent_signal(0.0, True, 0) == IntentSignal.HIGH_INTENT

    def test_eng_24_gives_medium_intent(self):
        # 24 < 25, so MEDIUM (if pricing=0, no demo)
        assert _intent_signal(24.0, False, 0) == IntentSignal.MEDIUM_INTENT

    def test_eng_25_boundary_is_high(self):
        assert _intent_signal(25.0, False, 0) == IntentSignal.HIGH_INTENT


# ---------------------------------------------------------------------------
# Class 17: TestLeadTierLogic
# ---------------------------------------------------------------------------

class TestLeadTierLogic:
    def test_score_100_is_hot(self):
        assert _tier(100.0) == LeadTier.HOT

    def test_score_70_is_hot(self):
        assert _tier(70.0) == LeadTier.HOT

    def test_score_69_is_warm(self):
        assert _tier(69.0) == LeadTier.WARM

    def test_score_45_is_warm(self):
        assert _tier(45.0) == LeadTier.WARM

    def test_score_44_is_cold(self):
        assert _tier(44.0) == LeadTier.COLD

    def test_score_20_is_cold(self):
        assert _tier(20.0) == LeadTier.COLD

    def test_score_19_is_dead(self):
        assert _tier(19.0) == LeadTier.DEAD

    def test_score_0_is_dead(self):
        assert _tier(0.0) == LeadTier.DEAD

    def test_score_71_is_hot(self):
        assert _tier(71.0) == LeadTier.HOT

    def test_score_46_is_warm(self):
        assert _tier(46.0) == LeadTier.WARM

    def test_score_21_is_cold(self):
        assert _tier(21.0) == LeadTier.COLD

    def test_score_1_is_dead(self):
        assert _tier(1.0) == LeadTier.DEAD


# ---------------------------------------------------------------------------
# Class 18: TestLeadActionLogic
# ---------------------------------------------------------------------------

class TestLeadActionLogic:
    def test_out_of_territory_disqualifies(self):
        lead = make_lead(out_of_territory=True)
        assert _action(LeadTier.HOT, lead, IntentSignal.HIGH_INTENT) == LeadAction.DISQUALIFY

    def test_unsubscribed_disqualifies(self):
        lead = make_lead(unsubscribed=True)
        assert _action(LeadTier.HOT, lead, IntentSignal.HIGH_INTENT) == LeadAction.DISQUALIFY

    def test_dead_tier_disqualifies(self):
        lead = make_lead()
        assert _action(LeadTier.DEAD, lead, IntentSignal.LOW_INTENT) == LeadAction.DISQUALIFY

    def test_hot_high_intent_gives_call_now(self):
        lead = make_lead()
        assert _action(LeadTier.HOT, lead, IntentSignal.HIGH_INTENT) == LeadAction.CALL_NOW

    def test_hot_medium_intent_gives_assign_ae(self):
        lead = make_lead()
        assert _action(LeadTier.HOT, lead, IntentSignal.MEDIUM_INTENT) == LeadAction.ASSIGN_AE

    def test_hot_low_intent_gives_assign_ae(self):
        lead = make_lead()
        assert _action(LeadTier.HOT, lead, IntentSignal.LOW_INTENT) == LeadAction.ASSIGN_AE

    def test_hot_no_intent_gives_assign_ae(self):
        lead = make_lead()
        assert _action(LeadTier.HOT, lead, IntentSignal.NO_INTENT) == LeadAction.ASSIGN_AE

    def test_warm_with_budget_and_authority_gives_qualify(self):
        lead = make_lead(budget_confirmed=True, authority_confirmed=True)
        assert _action(LeadTier.WARM, lead, IntentSignal.MEDIUM_INTENT) == LeadAction.QUALIFY

    def test_warm_without_budget_gives_nurture(self):
        lead = make_lead(budget_confirmed=False, authority_confirmed=True)
        assert _action(LeadTier.WARM, lead, IntentSignal.HIGH_INTENT) == LeadAction.NURTURE

    def test_warm_without_authority_gives_nurture(self):
        lead = make_lead(budget_confirmed=True, authority_confirmed=False)
        assert _action(LeadTier.WARM, lead, IntentSignal.HIGH_INTENT) == LeadAction.NURTURE

    def test_cold_high_intent_gives_nurture(self):
        lead = make_lead()
        assert _action(LeadTier.COLD, lead, IntentSignal.HIGH_INTENT) == LeadAction.NURTURE

    def test_cold_medium_intent_gives_nurture(self):
        lead = make_lead()
        assert _action(LeadTier.COLD, lead, IntentSignal.MEDIUM_INTENT) == LeadAction.NURTURE

    def test_cold_low_intent_gives_disqualify(self):
        lead = make_lead()
        assert _action(LeadTier.COLD, lead, IntentSignal.LOW_INTENT) == LeadAction.DISQUALIFY

    def test_cold_no_intent_gives_disqualify(self):
        lead = make_lead()
        assert _action(LeadTier.COLD, lead, IntentSignal.NO_INTENT) == LeadAction.DISQUALIFY

    def test_out_of_territory_overrides_hot_high_intent(self):
        lead = make_lead(out_of_territory=True)
        result = _action(LeadTier.HOT, lead, IntentSignal.HIGH_INTENT)
        assert result == LeadAction.DISQUALIFY

    def test_unsubscribed_overrides_warm_qualify(self):
        lead = make_lead(unsubscribed=True, budget_confirmed=True, authority_confirmed=True)
        result = _action(LeadTier.WARM, lead, IntentSignal.HIGH_INTENT)
        assert result == LeadAction.DISQUALIFY


# ---------------------------------------------------------------------------
# Class 19: TestBuildStrengths
# ---------------------------------------------------------------------------

class TestBuildStrengths:
    def test_referral_source_in_strengths(self):
        lead = make_lead(lead_source="referral")
        strengths = _strengths(lead, {"icp": 35, "engagement": 35, "qualification": 30})
        assert any("recommandation" in s for s in strengths)

    def test_industry_match_in_strengths(self):
        lead = make_lead(icp_industry_match=True)
        strengths = _strengths(lead, {"icp": 35, "engagement": 35, "qualification": 30})
        assert any("Industrie" in s for s in strengths)

    def test_no_industry_match_not_in_strengths(self):
        lead = make_lead(icp_industry_match=False)
        strengths = _strengths(lead, {"icp": 25, "engagement": 35, "qualification": 30})
        assert not any("Industrie alignée" in s for s in strengths)

    def test_size_and_revenue_match_in_strengths(self):
        lead = make_lead(icp_size_match=True, icp_revenue_match=True)
        strengths = _strengths(lead, {"icp": 35, "engagement": 35, "qualification": 30})
        assert any("Taille et revenu" in s for s in strengths)

    def test_tech_stack_match_in_strengths(self):
        lead = make_lead(tech_stack_match=True)
        strengths = _strengths(lead, {"icp": 35, "engagement": 35, "qualification": 30})
        assert any("Stack" in s or "technologique" in s for s in strengths)

    def test_demo_requested_in_strengths(self):
        lead = make_lead(demo_requested=True)
        strengths = _strengths(lead, {"icp": 35, "engagement": 35, "qualification": 30})
        assert any("Demo" in s or "demo" in s for s in strengths)

    def test_pricing_3_in_strengths(self):
        lead = make_lead(pricing_page_visits=3)
        strengths = _strengths(lead, {"icp": 35, "engagement": 35, "qualification": 30})
        assert any("tarifs" in s for s in strengths)

    def test_pricing_2_not_in_strengths(self):
        lead = make_lead(pricing_page_visits=2)
        strengths = _strengths(lead, {"icp": 35, "engagement": 35, "qualification": 30})
        assert not any("tarifs" in s for s in strengths)

    def test_budget_confirmed_in_strengths(self):
        lead = make_lead(budget_confirmed=True)
        strengths = _strengths(lead, {"icp": 35, "engagement": 35, "qualification": 30})
        assert any("Budget" in s for s in strengths)

    def test_authority_confirmed_in_strengths(self):
        lead = make_lead(authority_confirmed=True)
        strengths = _strengths(lead, {"icp": 35, "engagement": 35, "qualification": 30})
        assert any("Décideur" in s for s in strengths)

    def test_need_and_timeline_in_strengths(self):
        lead = make_lead(need_confirmed=True, timeline_confirmed=True)
        strengths = _strengths(lead, {"icp": 35, "engagement": 35, "qualification": 30})
        assert any("Besoin" in s and "timeline" in s for s in strengths)

    def test_no_need_no_timeline_strength(self):
        lead = make_lead(need_confirmed=False, timeline_confirmed=False)
        strengths = _strengths(lead, {"icp": 35, "engagement": 35, "qualification": 30})
        assert not any("Besoin + timeline" in s for s in strengths)

    def test_inbound_source_not_referral_strength(self):
        lead = make_lead(lead_source="inbound")
        strengths = _strengths(lead, {"icp": 35, "engagement": 35, "qualification": 30})
        assert not any("recommandation" in s for s in strengths)

    def test_returns_list(self):
        lead = make_lead()
        strengths = _strengths(lead, {"icp": 35, "engagement": 35, "qualification": 30})
        assert isinstance(strengths, list)


# ---------------------------------------------------------------------------
# Class 20: TestBuildWeaknesses
# ---------------------------------------------------------------------------

class TestBuildWeaknesses:
    def test_no_industry_match_in_weaknesses(self):
        lead = make_lead(icp_industry_match=False)
        weaknesses = _weaknesses(lead, {"engagement": 10})
        assert any("hors ICP" in w or "Industrie" in w for w in weaknesses)

    def test_no_size_match_in_weaknesses(self):
        lead = make_lead(icp_size_match=False)
        weaknesses = _weaknesses(lead, {"engagement": 10})
        assert any("taille" in w.lower() or "revenu" in w.lower() for w in weaknesses)

    def test_no_revenue_match_in_weaknesses(self):
        lead = make_lead(icp_revenue_match=False)
        weaknesses = _weaknesses(lead, {"engagement": 10})
        assert any("revenu" in w.lower() or "taille" in w.lower() for w in weaknesses)

    def test_low_engagement_in_weaknesses(self):
        lead = make_lead(website_visits=0, email_opens=0, email_clicks=0,
                         content_downloads=0, demo_requested=False, pricing_page_visits=0)
        weaknesses = _weaknesses(lead, {"engagement": 0})
        assert any("Engagement" in w or "engagement" in w for w in weaknesses)

    def test_engagement_5_not_in_low_weaknesses(self):
        lead = make_lead()
        weaknesses = _weaknesses(lead, {"engagement": 5})
        assert not any("très faible" in w for w in weaknesses)

    def test_no_budget_in_weaknesses(self):
        lead = make_lead(budget_confirmed=False)
        weaknesses = _weaknesses(lead, {"engagement": 10})
        assert any("Budget" in w or "budget" in w for w in weaknesses)

    def test_no_authority_in_weaknesses(self):
        lead = make_lead(authority_confirmed=False)
        weaknesses = _weaknesses(lead, {"engagement": 10})
        assert any("Décideur" in w for w in weaknesses)

    def test_competitor_customer_in_weaknesses(self):
        lead = make_lead(competitor_customer=True)
        weaknesses = _weaknesses(lead, {"engagement": 10})
        assert any("concurrent" in w.lower() for w in weaknesses)

    def test_stale_lead_in_weaknesses(self):
        lead = make_lead(days_in_funnel=91)
        weaknesses = _weaknesses(lead, {"engagement": 10})
        assert any("90j" in w or "attrition" in w for w in weaknesses)

    def test_fresh_lead_not_stale_weakness(self):
        lead = make_lead(days_in_funnel=30)
        weaknesses = _weaknesses(lead, {"engagement": 10})
        assert not any("attrition" in w for w in weaknesses)

    def test_no_need_confirmed_in_weaknesses(self):
        lead = make_lead(need_confirmed=False)
        weaknesses = _weaknesses(lead, {"engagement": 10})
        assert any("Besoin" in w for w in weaknesses)

    def test_returns_list(self):
        lead = make_lead()
        weaknesses = _weaknesses(lead, {"engagement": 10})
        assert isinstance(weaknesses, list)

    def test_perfect_lead_has_few_weaknesses(self):
        # All ICP true, budget+authority confirmed, fresh, no competitor
        lead = make_lead()
        weaknesses = _weaknesses(lead, {"engagement": 30})
        # No industry, no size/revenue, no budget, no authority, no competitor, not stale, need confirmed
        assert not any("hors ICP" in w for w in weaknesses)

    def test_days_90_exact_not_stale(self):
        lead = make_lead(days_in_funnel=90)
        weaknesses = _weaknesses(lead, {"engagement": 10})
        assert not any("attrition" in w for w in weaknesses)


# ---------------------------------------------------------------------------
# Class 21: TestEngineScoreAndFilters
# ---------------------------------------------------------------------------

class TestEngineScoreAndFilters:
    def setup_method(self):
        self.engine = LeadScoringIntelligenceEngine()

    def test_score_returns_result(self):
        lead = make_lead()
        result = self.engine.score(lead)
        assert isinstance(result, LeadScoringResult)

    def test_score_stores_lead(self):
        lead = make_lead()
        self.engine.score(lead)
        assert len(self.engine.all_leads()) == 1

    def test_score_batch_returns_sorted_desc(self):
        leads = [
            make_lead(lead_id="low", icp_industry_match=False, icp_size_match=False,
                      icp_revenue_match=False, icp_geography_match=False,
                      tech_stack_match=False, website_visits=0, email_opens=0,
                      email_clicks=0, content_downloads=0, demo_requested=False,
                      pricing_page_visits=0, budget_confirmed=False,
                      authority_confirmed=False, need_confirmed=False,
                      timeline_confirmed=False),
            make_lead(lead_id="high"),
        ]
        results = self.engine.score_batch(leads)
        assert results[0].lead_score >= results[1].lead_score

    def test_score_batch_all_leads_stored(self):
        leads = [make_lead(lead_id=f"l{i}") for i in range(3)]
        self.engine.score_batch(leads)
        assert len(self.engine.all_leads()) == 3

    def test_by_tier_hot_filters_correctly(self):
        self.engine.score(make_lead(lead_id="hot"))
        results = self.engine.by_tier(LeadTier.HOT)
        assert all(r.tier == LeadTier.HOT for r in results)

    def test_by_tier_dead_filters_correctly(self):
        dead_lead = make_lead(
            lead_id="dead",
            icp_industry_match=False, icp_size_match=False,
            icp_revenue_match=False, icp_geography_match=False,
            tech_stack_match=False, website_visits=0, email_opens=0,
            email_clicks=0, content_downloads=0, demo_requested=False,
            pricing_page_visits=0, budget_confirmed=False,
            authority_confirmed=False, need_confirmed=False,
            timeline_confirmed=False,
        )
        self.engine.score(dead_lead)
        results = self.engine.by_tier(LeadTier.DEAD)
        assert all(r.tier == LeadTier.DEAD for r in results)

    def test_by_action_disqualify_filters_correctly(self):
        lead = make_lead(lead_id="disq", out_of_territory=True)
        self.engine.score(lead)
        results = self.engine.by_action(LeadAction.DISQUALIFY)
        assert any(r.lead_id == "disq" for r in results)

    def test_by_action_call_now_filters_correctly(self):
        self.engine.score(make_lead(lead_id="cn"))
        results = self.engine.by_action(LeadAction.CALL_NOW)
        assert all(r.action == LeadAction.CALL_NOW for r in results)

    def test_by_intent_high_intent_filters(self):
        self.engine.score(make_lead(lead_id="hi"))
        results = self.engine.by_intent(IntentSignal.HIGH_INTENT)
        assert all(r.intent_signal == IntentSignal.HIGH_INTENT for r in results)

    def test_hot_leads_convenience(self):
        self.engine.score(make_lead(lead_id="hot2"))
        hot = self.engine.hot_leads()
        assert all(r.tier == LeadTier.HOT for r in hot)

    def test_disqualified_convenience(self):
        lead = make_lead(lead_id="dq", unsubscribed=True)
        self.engine.score(lead)
        disq = self.engine.disqualified()
        assert all(r.action == LeadAction.DISQUALIFY for r in disq)

    def test_call_now_convenience(self):
        self.engine.score(make_lead(lead_id="cn2"))
        cn = self.engine.call_now()
        assert all(r.action == LeadAction.CALL_NOW for r in cn)

    def test_high_intent_convenience(self):
        self.engine.score(make_lead(lead_id="hi2"))
        hi = self.engine.high_intent()
        assert all(r.intent_signal == IntentSignal.HIGH_INTENT for r in hi)

    def test_all_leads_sorted_desc(self):
        leads = [make_lead(lead_id=f"l{i}") for i in range(3)]
        self.engine.score_batch(leads)
        all_leads = self.engine.all_leads()
        scores = [r.lead_score for r in all_leads]
        assert scores == sorted(scores, reverse=True)

    def test_score_overwrite_same_lead_id(self):
        self.engine.score(make_lead(lead_id="dup"))
        self.engine.score(make_lead(lead_id="dup"))
        assert len(self.engine.all_leads()) == 1

    def test_by_tier_returns_empty_if_none(self):
        results = self.engine.by_tier(LeadTier.WARM)
        assert results == []


# ---------------------------------------------------------------------------
# Class 22: TestEngineAggregates
# ---------------------------------------------------------------------------

class TestEngineAggregates:
    def setup_method(self):
        self.engine = LeadScoringIntelligenceEngine()

    def test_avg_lead_score_empty(self):
        assert self.engine.avg_lead_score() == 0.0

    def test_hot_rate_empty(self):
        assert self.engine.hot_rate() == 0.0

    def test_avg_lead_score_single_lead(self):
        self.engine.score(make_lead())
        avg = self.engine.avg_lead_score()
        assert isinstance(avg, (int, float))
        assert avg > 0

    def test_avg_lead_score_math(self):
        lead1 = make_lead(lead_id="a")
        lead2 = make_lead(lead_id="b",
                          icp_industry_match=False, icp_size_match=False,
                          icp_revenue_match=False, icp_geography_match=False,
                          tech_stack_match=False, website_visits=0, email_opens=0,
                          email_clicks=0, content_downloads=0, demo_requested=False,
                          pricing_page_visits=0, budget_confirmed=False,
                          authority_confirmed=False, need_confirmed=False,
                          timeline_confirmed=False)
        r1 = self.engine.score(lead1)
        r2 = self.engine.score(lead2)
        expected = round((r1.lead_score + r2.lead_score) / 2, 1)
        assert self.engine.avg_lead_score() == expected

    def test_hot_rate_all_hot(self):
        for i in range(3):
            self.engine.score(make_lead(lead_id=f"hot{i}"))
        assert self.engine.hot_rate() == 100.0

    def test_hot_rate_none_hot(self):
        dead = make_lead(
            lead_id="dead",
            icp_industry_match=False, icp_size_match=False,
            icp_revenue_match=False, icp_geography_match=False,
            tech_stack_match=False, website_visits=0, email_opens=0,
            email_clicks=0, content_downloads=0, demo_requested=False,
            pricing_page_visits=0, budget_confirmed=False,
            authority_confirmed=False, need_confirmed=False,
            timeline_confirmed=False,
        )
        self.engine.score(dead)
        assert self.engine.hot_rate() == 0.0

    def test_summary_returns_dict(self):
        self.engine.score(make_lead())
        s = self.engine.summary()
        assert isinstance(s, dict)

    def test_summary_total_key(self):
        self.engine.score(make_lead())
        assert "total" in self.engine.summary()

    def test_summary_tier_counts_key(self):
        self.engine.score(make_lead())
        assert "tier_counts" in self.engine.summary()

    def test_summary_action_counts_key(self):
        self.engine.score(make_lead())
        assert "action_counts" in self.engine.summary()

    def test_summary_intent_counts_key(self):
        self.engine.score(make_lead())
        assert "intent_counts" in self.engine.summary()

    def test_summary_fit_counts_key(self):
        self.engine.score(make_lead())
        assert "fit_counts" in self.engine.summary()

    def test_summary_avg_lead_score_key(self):
        self.engine.score(make_lead())
        assert "avg_lead_score" in self.engine.summary()

    def test_summary_hot_rate_pct_key(self):
        self.engine.score(make_lead())
        assert "hot_rate_pct" in self.engine.summary()

    def test_summary_hot_count_key(self):
        self.engine.score(make_lead())
        assert "hot_count" in self.engine.summary()

    def test_summary_call_now_count_key(self):
        self.engine.score(make_lead())
        assert "call_now_count" in self.engine.summary()

    def test_summary_disqualified_count_key(self):
        self.engine.score(make_lead())
        assert "disqualified_count" in self.engine.summary()

    def test_reset_clears_all_leads(self):
        self.engine.score(make_lead())
        self.engine.reset()
        assert len(self.engine.all_leads()) == 0

    def test_reset_resets_avg(self):
        self.engine.score(make_lead())
        self.engine.reset()
        assert self.engine.avg_lead_score() == 0.0

    def test_reset_resets_hot_rate(self):
        self.engine.score(make_lead())
        self.engine.reset()
        assert self.engine.hot_rate() == 0.0

    def test_summary_total_matches_scored(self):
        for i in range(4):
            self.engine.score(make_lead(lead_id=f"x{i}"))
        assert self.engine.summary()["total"] == 4

    def test_summary_empty_engine(self):
        s = self.engine.summary()
        assert s["total"] == 0
        assert s["avg_lead_score"] == 0.0
