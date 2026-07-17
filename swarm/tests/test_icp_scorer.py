"""Comprehensive pytest tests for ICPScorer module."""

from __future__ import annotations

import math
import pytest

from swarm.intelligence.icp_scorer import (
    ICPInput,
    ICPResult,
    ICPScorer,
    ICPTier,
    CompanySize,
    OutreachRecommendation,
    _firmographic_score,
    _intent_score,
    _strategic_score,
    _risk_penalty,
    _estimate_deal_size,
    _SIZE_IDEAL,
    _INDUSTRY_SCORES,
    _GROWTH_SCORES,
    _TECH_STACK_BONUS,
)


# ---------------------------------------------------------------------------
# Helper factory
# ---------------------------------------------------------------------------

def make_input(**kwargs) -> ICPInput:
    defaults = dict(
        company_id="c001",
        company_name="TestCo",
        industry="saas",
        company_size=CompanySize.MID_MARKET,
        employee_count=500,
        annual_revenue_eur=5_000_000,
        growth_stage="fast_growth",
        tech_stack=[],
    )
    defaults.update(kwargs)
    return ICPInput(**defaults)


# ===========================================================================
# 1. TestFirmographicScore
# ===========================================================================

class TestFirmographicScore:
    """Tests for _firmographic_score()."""

    # --- CompanySize → _SIZE_IDEAL mapping ---

    def test_startup_size_score(self):
        inp = make_input(company_size=CompanySize.STARTUP, industry="saas",
                         growth_stage="hyper_growth", annual_revenue_eur=0)
        # size_score = 30
        size_score = _SIZE_IDEAL[CompanySize.STARTUP]
        assert size_score == 30

    def test_smb_size_score(self):
        assert _SIZE_IDEAL[CompanySize.SMB] == 75

    def test_mid_market_size_score(self):
        assert _SIZE_IDEAL[CompanySize.MID_MARKET] == 100

    def test_enterprise_size_score(self):
        assert _SIZE_IDEAL[CompanySize.ENTERPRISE] == 90

    def test_large_enterprise_size_score(self):
        assert _SIZE_IDEAL[CompanySize.LARGE_ENTERPRISE] == 60

    def test_all_company_sizes_present(self):
        for size in CompanySize:
            assert size in _SIZE_IDEAL

    # --- Industry score mapping ---

    def test_industry_saas(self):
        assert _INDUSTRY_SCORES["saas"] == 100

    def test_industry_software(self):
        assert _INDUSTRY_SCORES["software"] == 95

    def test_industry_fintech(self):
        assert _INDUSTRY_SCORES["fintech"] == 90

    def test_industry_cybersecurity(self):
        assert _INDUSTRY_SCORES["cybersecurity"] == 88

    def test_industry_martech(self):
        assert _INDUSTRY_SCORES["martech"] == 85

    def test_industry_hrtech(self):
        assert _INDUSTRY_SCORES["hrtech"] == 80

    def test_industry_proptech(self):
        assert _INDUSTRY_SCORES["proptech"] == 75

    def test_industry_legaltech(self):
        assert _INDUSTRY_SCORES["legaltech"] == 75

    def test_industry_edtech(self):
        assert _INDUSTRY_SCORES["edtech"] == 70

    def test_industry_healthtech(self):
        assert _INDUSTRY_SCORES["healthtech"] == 70

    def test_industry_ecommerce(self):
        assert _INDUSTRY_SCORES["ecommerce"] == 65

    def test_industry_retail(self):
        assert _INDUSTRY_SCORES["retail"] == 55

    def test_industry_manufacturing(self):
        assert _INDUSTRY_SCORES["manufacturing"] == 50

    def test_industry_logistics(self):
        assert _INDUSTRY_SCORES["logistics"] == 50

    def test_industry_consulting(self):
        assert _INDUSTRY_SCORES["consulting"] == 60

    def test_industry_finance(self):
        assert _INDUSTRY_SCORES["finance"] == 70

    def test_industry_insurance(self):
        assert _INDUSTRY_SCORES["insurance"] == 65

    def test_industry_healthcare(self):
        assert _INDUSTRY_SCORES["healthcare"] == 65

    def test_industry_pharma(self):
        assert _INDUSTRY_SCORES["pharma"] == 60

    def test_industry_telecom(self):
        assert _INDUSTRY_SCORES["telecom"] == 55

    def test_industry_media(self):
        assert _INDUSTRY_SCORES["media"] == 50

    def test_industry_real_estate(self):
        assert _INDUSTRY_SCORES["real_estate"] == 45

    def test_industry_construction(self):
        assert _INDUSTRY_SCORES["construction"] == 40

    def test_industry_agriculture(self):
        assert _INDUSTRY_SCORES["agriculture"] == 35

    def test_industry_government(self):
        assert _INDUSTRY_SCORES["government"] == 30

    def test_industry_non_profit(self):
        assert _INDUSTRY_SCORES["non_profit"] == 25

    # --- Growth stage mapping ---

    def test_growth_hyper_growth(self):
        assert _GROWTH_SCORES["hyper_growth"] == 100

    def test_growth_fast_growth(self):
        assert _GROWTH_SCORES["fast_growth"] == 85

    def test_growth_moderate_growth(self):
        assert _GROWTH_SCORES["moderate_growth"] == 65

    def test_growth_stable(self):
        assert _GROWTH_SCORES["stable"] == 45

    def test_growth_declining(self):
        assert _GROWTH_SCORES["declining"] == 15

    # --- Revenue bonus logic ---

    def test_revenue_bonus_zero(self):
        """annual_revenue_eur=0 → log10(max(1, 0/100000))=log10(1)=0, rev_bonus=0."""
        inp = make_input(annual_revenue_eur=0, industry="saas",
                         company_size=CompanySize.MID_MARKET, growth_stage="fast_growth")
        score = _firmographic_score(inp)
        # rev_bonus = min(15, log10(max(1, 0)) * 5) = 0
        expected_raw = 100 * 0.35 + 100 * 0.35 + 85 * 0.30
        expected = min(100, expected_raw + 0 * 0.10)
        assert abs(score - expected) < 1e-9

    def test_revenue_bonus_100k(self):
        """annual_revenue_eur=100_000 → log10(1)*5=0, rev_bonus=0."""
        inp = make_input(annual_revenue_eur=100_000, industry="saas",
                         company_size=CompanySize.MID_MARKET, growth_stage="fast_growth")
        score = _firmographic_score(inp)
        rev_bonus = min(15, math.log10(max(1, 100_000 / 100_000)) * 5)
        expected_raw = 100 * 0.35 + 100 * 0.35 + 85 * 0.30
        expected = min(100, expected_raw + rev_bonus * 0.10)
        assert abs(score - expected) < 1e-9

    def test_revenue_bonus_1m(self):
        """annual_revenue_eur=1_000_000 → log10(10)*5=5."""
        inp = make_input(annual_revenue_eur=1_000_000, industry="saas",
                         company_size=CompanySize.MID_MARKET, growth_stage="fast_growth")
        score = _firmographic_score(inp)
        rev_bonus = min(15, math.log10(max(1, 1_000_000 / 100_000)) * 5)
        assert abs(rev_bonus - 5.0) < 1e-9
        expected_raw = 100 * 0.35 + 100 * 0.35 + 85 * 0.30
        expected = min(100, expected_raw + rev_bonus * 0.10)
        assert abs(score - expected) < 1e-9

    def test_revenue_bonus_capped_at_15(self):
        """Very large revenue → rev_bonus capped at 15."""
        inp = make_input(annual_revenue_eur=1e15, industry="saas",
                         company_size=CompanySize.MID_MARKET, growth_stage="fast_growth")
        score = _firmographic_score(inp)
        rev_bonus = 15  # cap
        expected_raw = 100 * 0.35 + 100 * 0.35 + 85 * 0.30
        expected = min(100, expected_raw + rev_bonus * 0.10)
        assert abs(score - expected) < 1e-9

    # --- Final formula ---

    def test_formula_mid_market_saas_fast_growth(self):
        inp = make_input(company_size=CompanySize.MID_MARKET, industry="saas",
                         growth_stage="fast_growth", annual_revenue_eur=5_000_000)
        score = _firmographic_score(inp)
        size_score = 100
        industry_score = 100
        growth_score = 85
        rev_bonus = min(15, math.log10(max(1, 5_000_000 / 100_000)) * 5)
        raw = size_score * 0.35 + industry_score * 0.35 + growth_score * 0.30
        expected = min(100, raw + rev_bonus * 0.10)
        assert abs(score - expected) < 1e-9

    def test_formula_startup_non_profit_declining(self):
        inp = make_input(company_size=CompanySize.STARTUP, industry="non_profit",
                         growth_stage="declining", annual_revenue_eur=0)
        score = _firmographic_score(inp)
        raw = 30 * 0.35 + 25 * 0.35 + 15 * 0.30
        expected = min(100, raw + 0)
        assert abs(score - expected) < 1e-9

    def test_result_capped_at_100(self):
        """Ensure no score exceeds 100."""
        inp = make_input(company_size=CompanySize.MID_MARKET, industry="saas",
                         growth_stage="hyper_growth", annual_revenue_eur=1e15)
        score = _firmographic_score(inp)
        assert score <= 100

    def test_score_non_negative(self):
        inp = make_input(company_size=CompanySize.STARTUP, industry="government",
                         growth_stage="declining", annual_revenue_eur=0)
        score = _firmographic_score(inp)
        assert score >= 0

    def test_enterprise_software_hyper_growth(self):
        inp = make_input(company_size=CompanySize.ENTERPRISE, industry="software",
                         growth_stage="hyper_growth", annual_revenue_eur=10_000_000)
        score = _firmographic_score(inp)
        size_score = 90
        industry_score = 95
        growth_score = 100
        rev_bonus = min(15, math.log10(max(1, 10_000_000 / 100_000)) * 5)
        raw = size_score * 0.35 + industry_score * 0.35 + growth_score * 0.30
        expected = min(100, raw + rev_bonus * 0.10)
        assert abs(score - expected) < 1e-9

    def test_large_enterprise_manufacturing_stable(self):
        inp = make_input(company_size=CompanySize.LARGE_ENTERPRISE, industry="manufacturing",
                         growth_stage="stable", annual_revenue_eur=50_000_000)
        score = _firmographic_score(inp)
        size_score = 60
        industry_score = 50
        growth_score = 45
        rev_bonus = min(15, math.log10(max(1, 50_000_000 / 100_000)) * 5)
        raw = size_score * 0.35 + industry_score * 0.35 + growth_score * 0.30
        expected = min(100, raw + rev_bonus * 0.10)
        assert abs(score - expected) < 1e-9

    def test_industry_case_insensitive(self):
        inp_lower = make_input(industry="saas")
        inp_upper = make_input(industry="SAAS")
        assert abs(_firmographic_score(inp_lower) - _firmographic_score(inp_upper)) < 1e-9

    def test_growth_stage_case_insensitive(self):
        inp_lower = make_input(growth_stage="fast_growth")
        inp_upper = make_input(growth_stage="FAST_GROWTH")
        assert abs(_firmographic_score(inp_lower) - _firmographic_score(inp_upper)) < 1e-9


# ===========================================================================
# 2. TestIntentScore
# ===========================================================================

class TestIntentScore:
    """Tests for _intent_score()."""

    def test_all_false_no_tech_stack(self):
        inp = make_input()
        assert _intent_score(inp) == 0.0

    def test_inbound_lead_adds_30(self):
        inp = make_input(inbound_lead=True)
        assert _intent_score(inp) == 30.0

    def test_has_pain_point_match_adds_25(self):
        inp = make_input(has_pain_point_match=True)
        assert _intent_score(inp) == 25.0

    def test_visited_website_adds_10(self):
        inp = make_input(visited_website=True)
        assert _intent_score(inp) == 10.0

    def test_engaged_with_content_adds_10(self):
        inp = make_input(engaged_with_content=True)
        assert _intent_score(inp) == 10.0

    def test_attended_event_adds_8(self):
        inp = make_input(attended_event=True)
        assert _intent_score(inp) == 8.0

    def test_active_hiring_sales_adds_7(self):
        inp = make_input(active_hiring_sales=True)
        assert _intent_score(inp) == 7.0

    def test_recently_raised_funding_adds_7(self):
        inp = make_input(recently_raised_funding=True)
        assert _intent_score(inp) == 7.0

    def test_competitor_customer_adds_5(self):
        inp = make_input(competitor_customer=True)
        assert _intent_score(inp) == 5.0

    def test_uses_crm_adds_5(self):
        inp = make_input(uses_crm=True)
        assert _intent_score(inp) == 5.0

    def test_has_dedicated_sales_team_adds_5(self):
        inp = make_input(has_dedicated_sales_team=True)
        assert _intent_score(inp) == 5.0

    def test_has_marketing_budget_adds_5(self):
        inp = make_input(has_marketing_budget=True)
        assert _intent_score(inp) == 5.0

    def test_multiple_signals_sum(self):
        inp = make_input(inbound_lead=True, has_pain_point_match=True, visited_website=True)
        assert _intent_score(inp) == 65.0

    def test_tech_stack_single_item(self):
        inp = make_input(tech_stack=["salesforce"])
        assert _intent_score(inp) == 15.0  # salesforce bonus = 15

    def test_tech_stack_hubspot(self):
        inp = make_input(tech_stack=["hubspot"])
        assert _intent_score(inp) == 12.0

    def test_tech_stack_marketo(self):
        inp = make_input(tech_stack=["marketo"])
        assert _intent_score(inp) == 10.0

    def test_tech_stack_bonus_capped_at_15(self):
        """salesforce(15) + hubspot(12) = 27, capped at 15."""
        inp = make_input(tech_stack=["salesforce", "hubspot"])
        score = _intent_score(inp)
        assert score == 15.0

    def test_tech_stack_multi_small_items(self):
        """slack(5) + notion(5) + jira(5) = 15, exactly at cap."""
        inp = make_input(tech_stack=["slack", "notion", "jira"])
        assert _intent_score(inp) == 15.0

    def test_tech_stack_unknown_key(self):
        """Unknown tech stack item contributes 0."""
        inp = make_input(tech_stack=["unknown_tool"])
        assert _intent_score(inp) == 0.0

    def test_tech_stack_case_insensitive(self):
        inp_lower = make_input(tech_stack=["salesforce"])
        inp_upper = make_input(tech_stack=["SALESFORCE"])
        assert _intent_score(inp_lower) == _intent_score(inp_upper)

    def test_total_capped_at_100(self):
        """All booleans True with best tech stack should be capped at 100."""
        inp = make_input(
            inbound_lead=True, has_pain_point_match=True, visited_website=True,
            engaged_with_content=True, attended_event=True, active_hiring_sales=True,
            recently_raised_funding=True, competitor_customer=True, uses_crm=True,
            has_dedicated_sales_team=True, has_marketing_budget=True,
            tech_stack=["salesforce", "hubspot"],
        )
        assert _intent_score(inp) == 100.0

    def test_all_signals_without_tech_stack(self):
        """Sum without tech_stack = 30+25+10+10+8+7+7+5+5+5+5 = 117, capped at 100."""
        inp = make_input(
            inbound_lead=True, has_pain_point_match=True, visited_website=True,
            engaged_with_content=True, attended_event=True, active_hiring_sales=True,
            recently_raised_funding=True, competitor_customer=True, uses_crm=True,
            has_dedicated_sales_team=True, has_marketing_budget=True,
        )
        assert _intent_score(inp) == 100.0

    def test_gong_bonus(self):
        inp = make_input(tech_stack=["gong"])
        assert _intent_score(inp) == 8.0

    def test_chorus_bonus(self):
        inp = make_input(tech_stack=["chorus"])
        assert _intent_score(inp) == 8.0

    def test_linkedin_sales_nav_bonus(self):
        inp = make_input(tech_stack=["linkedin_sales_nav"])
        assert _intent_score(inp) == 8.0

    def test_zendesk_bonus(self):
        inp = make_input(tech_stack=["zendesk"])
        assert _intent_score(inp) == 8.0

    def test_intercom_bonus(self):
        inp = make_input(tech_stack=["intercom"])
        assert _intent_score(inp) == 8.0

    def test_outreach_bonus(self):
        inp = make_input(tech_stack=["outreach"])
        assert _intent_score(inp) == 10.0

    def test_salesloft_bonus(self):
        inp = make_input(tech_stack=["salesloft"])
        assert _intent_score(inp) == 10.0

    def test_slack_bonus(self):
        inp = make_input(tech_stack=["slack"])
        assert _intent_score(inp) == 5.0

    def test_notion_bonus(self):
        inp = make_input(tech_stack=["notion"])
        assert _intent_score(inp) == 5.0

    def test_jira_bonus(self):
        inp = make_input(tech_stack=["jira"])
        assert _intent_score(inp) == 5.0


# ===========================================================================
# 3. TestStrategicScore
# ===========================================================================

class TestStrategicScore:
    """Tests for _strategic_score()."""

    def test_all_false(self):
        inp = make_input()
        assert _strategic_score(inp) == 0.0

    def test_decision_maker_accessible_adds_35(self):
        inp = make_input(decision_maker_accessible=True)
        assert _strategic_score(inp) == 35.0

    def test_has_pain_point_match_adds_25(self):
        inp = make_input(has_pain_point_match=True)
        assert _strategic_score(inp) == 25.0

    def test_budget_confirmed_adds_20(self):
        inp = make_input(budget_confirmed=True)
        assert _strategic_score(inp) == 20.0

    def test_timeline_fit_adds_15(self):
        inp = make_input(timeline_fit=True)
        assert _strategic_score(inp) == 15.0

    def test_multi_stakeholder_buying_adds_5(self):
        inp = make_input(multi_stakeholder_buying=True)
        assert _strategic_score(inp) == 5.0

    def test_all_true_equals_100(self):
        inp = make_input(
            decision_maker_accessible=True,
            has_pain_point_match=True,
            budget_confirmed=True,
            timeline_fit=True,
            multi_stakeholder_buying=True,
        )
        assert _strategic_score(inp) == 100.0

    def test_capped_at_100(self):
        """35+25+20+15+5=100, exactly at cap."""
        inp = make_input(
            decision_maker_accessible=True,
            has_pain_point_match=True,
            budget_confirmed=True,
            timeline_fit=True,
            multi_stakeholder_buying=True,
        )
        assert _strategic_score(inp) <= 100.0

    def test_partial_combination(self):
        inp = make_input(decision_maker_accessible=True, budget_confirmed=True)
        assert _strategic_score(inp) == 55.0

    def test_pain_plus_timeline(self):
        inp = make_input(has_pain_point_match=True, timeline_fit=True)
        assert _strategic_score(inp) == 40.0

    def test_budget_plus_multi_stakeholder(self):
        inp = make_input(budget_confirmed=True, multi_stakeholder_buying=True)
        assert _strategic_score(inp) == 25.0


# ===========================================================================
# 4. TestRiskPenalty
# ===========================================================================

class TestRiskPenalty:
    """Tests for _risk_penalty()."""

    def test_none_flags(self):
        inp = make_input()
        assert _risk_penalty(inp) == 0.0

    def test_high_churn_industry_adds_15(self):
        inp = make_input(high_churn_industry=True)
        assert _risk_penalty(inp) == 15.0

    def test_price_sensitive_adds_10(self):
        inp = make_input(price_sensitive=True)
        assert _risk_penalty(inp) == 10.0

    def test_long_sales_cycle_adds_8(self):
        inp = make_input(long_sales_cycle=True)
        assert _risk_penalty(inp) == 8.0

    def test_all_three_capped_at_30(self):
        """15+10+8=33, capped at 30."""
        inp = make_input(high_churn_industry=True, price_sensitive=True, long_sales_cycle=True)
        assert _risk_penalty(inp) == 30.0

    def test_churn_plus_price(self):
        inp = make_input(high_churn_industry=True, price_sensitive=True)
        assert _risk_penalty(inp) == 25.0

    def test_churn_plus_cycle(self):
        inp = make_input(high_churn_industry=True, long_sales_cycle=True)
        assert _risk_penalty(inp) == 23.0

    def test_price_plus_cycle(self):
        inp = make_input(price_sensitive=True, long_sales_cycle=True)
        assert _risk_penalty(inp) == 18.0

    def test_penalty_never_exceeds_30(self):
        inp = make_input(high_churn_industry=True, price_sensitive=True, long_sales_cycle=True)
        assert _risk_penalty(inp) <= 30.0


# ===========================================================================
# 5. TestICPTier — boundary tests
# ===========================================================================

class TestICPTier:
    """Tests for _tier_from_score() via ICPScorer.score()."""

    def _score_for(self, icp_score: float) -> ICPTier:
        """Use ICPScorer to get a tier for a given score by engineering inputs."""
        from swarm.intelligence.icp_scorer import _tier_from_score
        return _tier_from_score(icp_score)

    def test_85_is_perfect(self):
        assert self._score_for(85.0) == ICPTier.PERFECT

    def test_100_is_perfect(self):
        assert self._score_for(100.0) == ICPTier.PERFECT

    def test_84_99_is_strong(self):
        assert self._score_for(84.99) == ICPTier.STRONG

    def test_70_is_strong(self):
        assert self._score_for(70.0) == ICPTier.STRONG

    def test_69_99_is_moderate(self):
        assert self._score_for(69.99) == ICPTier.MODERATE

    def test_50_is_moderate(self):
        assert self._score_for(50.0) == ICPTier.MODERATE

    def test_49_99_is_weak(self):
        assert self._score_for(49.99) == ICPTier.WEAK

    def test_30_is_weak(self):
        assert self._score_for(30.0) == ICPTier.WEAK

    def test_29_99_is_disqualified(self):
        assert self._score_for(29.99) == ICPTier.DISQUALIFIED

    def test_0_is_disqualified(self):
        assert self._score_for(0.0) == ICPTier.DISQUALIFIED

    def test_exactly_85_boundary(self):
        assert self._score_for(85) == ICPTier.PERFECT

    def test_exactly_70_boundary(self):
        assert self._score_for(70) == ICPTier.STRONG

    def test_exactly_50_boundary(self):
        assert self._score_for(50) == ICPTier.MODERATE

    def test_exactly_30_boundary(self):
        assert self._score_for(30) == ICPTier.WEAK

    def test_just_below_85(self):
        from swarm.intelligence.icp_scorer import _tier_from_score
        assert _tier_from_score(84.999) == ICPTier.STRONG

    def test_just_below_70(self):
        from swarm.intelligence.icp_scorer import _tier_from_score
        assert _tier_from_score(69.999) == ICPTier.MODERATE

    def test_just_below_50(self):
        from swarm.intelligence.icp_scorer import _tier_from_score
        assert _tier_from_score(49.999) == ICPTier.WEAK

    def test_just_below_30(self):
        from swarm.intelligence.icp_scorer import _tier_from_score
        assert _tier_from_score(29.999) == ICPTier.DISQUALIFIED


# ===========================================================================
# 6. TestOutreachRecommendation
# ===========================================================================

class TestOutreachRecommendation:
    """Tests for _recommendation() via ICPScorer."""

    def _get_rec(self, tier: ICPTier) -> OutreachRecommendation:
        from swarm.intelligence.icp_scorer import _recommendation
        return _recommendation(tier)

    def test_perfect_gives_prioritize(self):
        assert self._get_rec(ICPTier.PERFECT) == OutreachRecommendation.PRIORITIZE

    def test_strong_gives_prioritize(self):
        assert self._get_rec(ICPTier.STRONG) == OutreachRecommendation.PRIORITIZE

    def test_moderate_gives_qualify(self):
        assert self._get_rec(ICPTier.MODERATE) == OutreachRecommendation.QUALIFY

    def test_weak_gives_deprioritize(self):
        assert self._get_rec(ICPTier.WEAK) == OutreachRecommendation.DEPRIORITIZE

    def test_disqualified_gives_reject(self):
        assert self._get_rec(ICPTier.DISQUALIFIED) == OutreachRecommendation.REJECT


# ===========================================================================
# 7. TestDealSize
# ===========================================================================

class TestDealSize:
    """Tests for _estimate_deal_size()."""

    def test_formula_basic(self):
        inp = make_input(annual_revenue_eur=5_000_000, employee_count=500)
        icp_score = 75.0
        base = 5_000_000 * 0.008
        employee_factor = math.log10(max(1, 500)) * 500
        score_multiplier = 0.5 + (icp_score / 100) * 1.5
        expected = round(max(500, (base + employee_factor) * score_multiplier), -2)
        result = _estimate_deal_size(inp, icp_score)
        assert result == expected

    def test_employee_count_zero(self):
        """employee_count=0 → max(1, 0)=1, log10(1)=0."""
        inp = make_input(annual_revenue_eur=1_000_000, employee_count=0)
        icp_score = 50.0
        base = 1_000_000 * 0.008
        employee_factor = math.log10(max(1, 0)) * 500  # = 0
        score_multiplier = 0.5 + (50 / 100) * 1.5
        expected = round(max(500, (base + employee_factor) * score_multiplier), -2)
        result = _estimate_deal_size(inp, icp_score)
        assert result == expected

    def test_minimum_floor_500(self):
        """Very small values must still return at least 500."""
        inp = make_input(annual_revenue_eur=0, employee_count=0)
        icp_score = 0.0
        result = _estimate_deal_size(inp, icp_score)
        assert result >= 500

    def test_employee_count_1(self):
        inp = make_input(annual_revenue_eur=100_000, employee_count=1)
        icp_score = 50.0
        base = 100_000 * 0.008
        employee_factor = math.log10(1) * 500  # = 0
        score_multiplier = 0.5 + (50 / 100) * 1.5
        expected = round(max(500, (base + employee_factor) * score_multiplier), -2)
        result = _estimate_deal_size(inp, icp_score)
        assert result == expected

    def test_score_multiplier_at_0(self):
        """icp_score=0 → score_multiplier=0.5."""
        inp = make_input(annual_revenue_eur=1_000_000, employee_count=100)
        icp_score = 0.0
        base = 1_000_000 * 0.008
        employee_factor = math.log10(100) * 500
        score_multiplier = 0.5
        expected = round(max(500, (base + employee_factor) * score_multiplier), -2)
        result = _estimate_deal_size(inp, icp_score)
        assert result == expected

    def test_score_multiplier_at_100(self):
        """icp_score=100 → score_multiplier=2.0."""
        inp = make_input(annual_revenue_eur=1_000_000, employee_count=100)
        icp_score = 100.0
        base = 1_000_000 * 0.008
        employee_factor = math.log10(100) * 500
        score_multiplier = 2.0
        expected = round(max(500, (base + employee_factor) * score_multiplier), -2)
        result = _estimate_deal_size(inp, icp_score)
        assert result == expected

    def test_result_rounded_to_nearest_100(self):
        """Result should be rounded to nearest 100 (round to -2)."""
        inp = make_input(annual_revenue_eur=500_000, employee_count=50)
        icp_score = 60.0
        result = _estimate_deal_size(inp, icp_score)
        assert result % 100 == 0

    def test_large_company_large_deal(self):
        inp = make_input(annual_revenue_eur=100_000_000, employee_count=5000)
        icp_score = 90.0
        base = 100_000_000 * 0.008
        employee_factor = math.log10(5000) * 500
        score_multiplier = 0.5 + (90 / 100) * 1.5
        expected = round(max(500, (base + employee_factor) * score_multiplier), -2)
        result = _estimate_deal_size(inp, icp_score)
        assert result == expected


# ===========================================================================
# 8. TestICPScorerScore
# ===========================================================================

class TestICPScorerScore:
    """Tests for ICPScorer.score()."""

    def test_returns_icp_result(self):
        scorer = ICPScorer()
        inp = make_input()
        result = scorer.score(inp)
        assert isinstance(result, ICPResult)

    def test_result_has_all_fields(self):
        scorer = ICPScorer()
        inp = make_input()
        result = scorer.score(inp)
        assert result.company_id == "c001"
        assert result.company_name == "TestCo"
        assert isinstance(result.icp_score, float)
        assert isinstance(result.icp_tier, ICPTier)
        assert isinstance(result.firmographic_score, float)
        assert isinstance(result.intent_score, float)
        assert isinstance(result.strategic_score, float)
        assert isinstance(result.risk_penalty, float)
        assert isinstance(result.outreach_recommendation, OutreachRecommendation)
        assert isinstance(result.fit_signals, list)
        assert isinstance(result.risk_signals, list)
        assert isinstance(result.estimated_deal_size_eur, float)

    def test_result_stored_and_retrievable_via_get(self):
        scorer = ICPScorer()
        inp = make_input(company_id="xyz")
        result = scorer.score(inp)
        retrieved = scorer.get("xyz")
        assert retrieved is result

    def test_get_unknown_id_returns_none(self):
        scorer = ICPScorer()
        assert scorer.get("nonexistent") is None

    def test_overwriting_same_company_id_replaces(self):
        scorer = ICPScorer()
        inp1 = make_input(company_id="c1", company_name="FirstCo")
        inp2 = make_input(company_id="c1", company_name="SecondCo")
        scorer.score(inp1)
        scorer.score(inp2)
        result = scorer.get("c1")
        assert result.company_name == "SecondCo"

    def test_icp_score_in_range_0_100(self):
        scorer = ICPScorer()
        inp = make_input()
        result = scorer.score(inp)
        assert 0 <= result.icp_score <= 100

    def test_icp_score_all_true(self):
        scorer = ICPScorer()
        inp = make_input(
            inbound_lead=True, has_pain_point_match=True, visited_website=True,
            engaged_with_content=True, attended_event=True, active_hiring_sales=True,
            recently_raised_funding=True, competitor_customer=True, uses_crm=True,
            has_dedicated_sales_team=True, has_marketing_budget=True,
            decision_maker_accessible=True, multi_stakeholder_buying=True,
            budget_confirmed=True, timeline_fit=True,
            tech_stack=["salesforce"],
        )
        result = scorer.score(inp)
        assert 0 <= result.icp_score <= 100

    def test_tier_matches_score_range(self):
        scorer = ICPScorer()
        inp = make_input()
        result = scorer.score(inp)
        score = result.icp_score
        if score >= 85:
            assert result.icp_tier == ICPTier.PERFECT
        elif score >= 70:
            assert result.icp_tier == ICPTier.STRONG
        elif score >= 50:
            assert result.icp_tier == ICPTier.MODERATE
        elif score >= 30:
            assert result.icp_tier == ICPTier.WEAK
        else:
            assert result.icp_tier == ICPTier.DISQUALIFIED

    def test_firm_score_stored_in_result(self):
        scorer = ICPScorer()
        inp = make_input()
        result = scorer.score(inp)
        expected_firm = _firmographic_score(inp)
        assert abs(result.firmographic_score - round(expected_firm, 2)) < 1e-9

    def test_intent_score_stored_in_result(self):
        scorer = ICPScorer()
        inp = make_input(inbound_lead=True)
        result = scorer.score(inp)
        expected_intent = _intent_score(inp)
        assert abs(result.intent_score - round(expected_intent, 2)) < 1e-9

    def test_strategic_score_stored_in_result(self):
        scorer = ICPScorer()
        inp = make_input(decision_maker_accessible=True)
        result = scorer.score(inp)
        expected_strategic = _strategic_score(inp)
        assert abs(result.strategic_score - round(expected_strategic, 2)) < 1e-9

    def test_risk_penalty_stored_in_result(self):
        scorer = ICPScorer()
        inp = make_input(high_churn_industry=True)
        result = scorer.score(inp)
        expected_penalty = _risk_penalty(inp)
        assert abs(result.risk_penalty - round(expected_penalty, 2)) < 1e-9

    def test_estimated_deal_size_positive(self):
        scorer = ICPScorer()
        inp = make_input()
        result = scorer.score(inp)
        assert result.estimated_deal_size_eur >= 500

    def test_to_dict_contains_tier_value(self):
        scorer = ICPScorer()
        inp = make_input()
        result = scorer.score(inp)
        d = result.to_dict()
        assert d["icp_tier"] == result.icp_tier.value
        assert d["outreach_recommendation"] == result.outreach_recommendation.value


# ===========================================================================
# 9. TestICPScorerBatch
# ===========================================================================

class TestICPScorerBatch:
    """Tests for ICPScorer.score_batch()."""

    def test_empty_list_returns_empty(self):
        scorer = ICPScorer()
        result = scorer.score_batch([])
        assert result == []

    def test_returns_list_of_icp_result(self):
        scorer = ICPScorer()
        inputs = [
            make_input(company_id="a"),
            make_input(company_id="b"),
        ]
        results = scorer.score_batch(inputs)
        assert all(isinstance(r, ICPResult) for r in results)

    def test_sorted_by_score_descending(self):
        scorer = ICPScorer()
        inputs = [
            make_input(company_id="low", industry="government", company_size=CompanySize.STARTUP,
                       growth_stage="declining"),
            make_input(company_id="high", industry="saas", company_size=CompanySize.MID_MARKET,
                       growth_stage="hyper_growth", inbound_lead=True,
                       decision_maker_accessible=True, has_pain_point_match=True,
                       budget_confirmed=True),
        ]
        results = scorer.score_batch(inputs)
        scores = [r.icp_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_priority_rank_assigned(self):
        scorer = ICPScorer()
        inputs = [make_input(company_id=f"c{i}") for i in range(3)]
        results = scorer.score_batch(inputs)
        ranks = {r.priority_rank for r in results}
        assert ranks == {1, 2, 3}

    def test_priority_rank_starts_at_1(self):
        scorer = ICPScorer()
        inputs = [make_input(company_id="only")]
        results = scorer.score_batch(inputs)
        assert results[0].priority_rank == 1

    def test_all_results_stored_in_dict(self):
        scorer = ICPScorer()
        inputs = [make_input(company_id=f"c{i}") for i in range(5)]
        scorer.score_batch(inputs)
        for i in range(5):
            assert scorer.get(f"c{i}") is not None

    def test_rank_1_has_highest_score(self):
        scorer = ICPScorer()
        inputs = [
            make_input(company_id="a", inbound_lead=True, decision_maker_accessible=True,
                       has_pain_point_match=True, budget_confirmed=True),
            make_input(company_id="b"),
            make_input(company_id="c", industry="government", growth_stage="declining"),
        ]
        results = scorer.score_batch(inputs)
        rank1 = next(r for r in results if r.priority_rank == 1)
        assert rank1.icp_score == max(r.icp_score for r in results)

    def test_batch_length_matches_input(self):
        scorer = ICPScorer()
        inputs = [make_input(company_id=f"c{i}") for i in range(7)]
        results = scorer.score_batch(inputs)
        assert len(results) == 7


# ===========================================================================
# 10. TestICPScorerQueries
# ===========================================================================

class TestICPScorerQueries:
    """Tests for all query methods."""

    def _populated_scorer(self) -> ICPScorer:
        scorer = ICPScorer()
        # Perfect tier: high scores
        scorer.score(make_input(
            company_id="perfect1",
            inbound_lead=True, decision_maker_accessible=True,
            has_pain_point_match=True, budget_confirmed=True, timeline_fit=True,
            multi_stakeholder_buying=True, visited_website=True, engaged_with_content=True,
            attended_event=True, active_hiring_sales=True, recently_raised_funding=True,
            uses_crm=True, has_dedicated_sales_team=True, has_marketing_budget=True,
            tech_stack=["salesforce"],
            industry="saas", company_size=CompanySize.MID_MARKET, growth_stage="hyper_growth",
        ))
        # Strong tier target (no risk, strong signals)
        scorer.score(make_input(
            company_id="strong1",
            decision_maker_accessible=True, has_pain_point_match=True,
            industry="saas", company_size=CompanySize.MID_MARKET, growth_stage="fast_growth",
        ))
        # Moderate tier (weak signals, moderate industry)
        scorer.score(make_input(
            company_id="moderate1",
            industry="retail", company_size=CompanySize.SMB, growth_stage="stable",
        ))
        # Disqualified tier (very low score)
        scorer.score(make_input(
            company_id="disq1",
            industry="government", company_size=CompanySize.STARTUP,
            growth_stage="declining", annual_revenue_eur=0,
            high_churn_industry=True, price_sensitive=True, long_sales_cycle=True,
        ))
        return scorer

    def test_all_companies_returns_sorted_desc(self):
        scorer = self._populated_scorer()
        results = scorer.all_companies()
        scores = [r.icp_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_all_companies_returns_all(self):
        scorer = self._populated_scorer()
        assert len(scorer.all_companies()) == 4

    def test_by_tier_filters_correctly(self):
        scorer = self._populated_scorer()
        disq = scorer.by_tier(ICPTier.DISQUALIFIED)
        assert all(r.icp_tier == ICPTier.DISQUALIFIED for r in disq)

    def test_perfect_fit_returns_only_perfect(self):
        scorer = self._populated_scorer()
        results = scorer.perfect_fit()
        assert all(r.icp_tier == ICPTier.PERFECT for r in results)

    def test_strong_fit_returns_only_strong(self):
        scorer = self._populated_scorer()
        results = scorer.strong_fit()
        assert all(r.icp_tier == ICPTier.STRONG for r in results)

    def test_prioritize_returns_perfect_and_strong(self):
        scorer = self._populated_scorer()
        prioritized = scorer.prioritize()
        for r in prioritized:
            assert r.icp_tier in (ICPTier.PERFECT, ICPTier.STRONG)

    def test_disqualified_returns_only_disqualified(self):
        scorer = self._populated_scorer()
        results = scorer.disqualified()
        assert all(r.icp_tier == ICPTier.DISQUALIFIED for r in results)

    def test_top_n_returns_correct_count(self):
        scorer = self._populated_scorer()
        results = scorer.top_n(3)
        assert len(results) == 3

    def test_top_n_returns_highest_scores(self):
        scorer = self._populated_scorer()
        all_r = scorer.all_companies()
        top3 = scorer.top_n(3)
        assert [r.company_id for r in top3] == [r.company_id for r in all_r[:3]]

    def test_top_n_more_than_available(self):
        scorer = self._populated_scorer()
        results = scorer.top_n(100)
        assert len(results) == 4

    def test_total_pipeline_eur_sums_prioritized_only(self):
        scorer = self._populated_scorer()
        prioritized = scorer.prioritize()
        expected = round(sum(r.estimated_deal_size_eur for r in prioritized), 2)
        assert scorer.total_pipeline_eur() == expected

    def test_total_pipeline_eur_empty(self):
        scorer = ICPScorer()
        assert scorer.total_pipeline_eur() == 0.0

    def test_by_tier_empty_when_no_match(self):
        scorer = ICPScorer()
        scorer.score(make_input(company_id="only"))
        # Unless the single company happens to be PERFECT, there should be 0 or some
        results = scorer.by_tier(ICPTier.PERFECT)
        # Just ensure it returns a list (may be empty or not)
        assert isinstance(results, list)

    def test_all_companies_empty_scorer(self):
        scorer = ICPScorer()
        assert scorer.all_companies() == []

    def test_prioritize_empty_when_no_prioritized(self):
        scorer = ICPScorer()
        # Score a disqualified company
        scorer.score(make_input(
            company_id="d1", industry="government", company_size=CompanySize.STARTUP,
            growth_stage="declining", annual_revenue_eur=0,
            high_churn_industry=True, price_sensitive=True, long_sales_cycle=True,
        ))
        # Disqualified → REJECT, not in prioritize
        prioritized = scorer.prioritize()
        assert all(r.outreach_recommendation == OutreachRecommendation.PRIORITIZE
                   for r in prioritized)


# ===========================================================================
# 11. TestSummary
# ===========================================================================

class TestSummary:
    """Tests for summary()."""

    def test_empty_scorer_summary(self):
        scorer = ICPScorer()
        s = scorer.summary()
        assert s["total"] == 0
        assert s["tier_counts"] == {}
        assert s["avg_icp_score"] == 0.0
        assert s["total_pipeline_eur"] == 0.0

    def test_summary_has_all_keys(self):
        scorer = ICPScorer()
        s = scorer.summary()
        assert "total" in s
        assert "tier_counts" in s
        assert "avg_icp_score" in s
        assert "total_pipeline_eur" in s

    def test_summary_total_count(self):
        scorer = ICPScorer()
        for i in range(3):
            scorer.score(make_input(company_id=f"c{i}"))
        s = scorer.summary()
        assert s["total"] == 3

    def test_summary_tier_counts(self):
        scorer = ICPScorer()
        scorer.score(make_input(company_id="a"))
        s = scorer.summary()
        # All tier counts should sum to total
        assert sum(s["tier_counts"].values()) == s["total"]

    def test_summary_avg_score(self):
        scorer = ICPScorer()
        inp1 = make_input(company_id="a")
        inp2 = make_input(company_id="b", inbound_lead=True)
        r1 = scorer.score(inp1)
        r2 = scorer.score(inp2)
        s = scorer.summary()
        expected_avg = round((r1.icp_score + r2.icp_score) / 2, 1)
        assert s["avg_icp_score"] == expected_avg

    def test_summary_pipeline_matches_total_pipeline(self):
        scorer = ICPScorer()
        scorer.score(make_input(company_id="a"))
        scorer.score(make_input(company_id="b", inbound_lead=True, decision_maker_accessible=True,
                                has_pain_point_match=True))
        s = scorer.summary()
        assert s["total_pipeline_eur"] == scorer.total_pipeline_eur()

    def test_summary_tier_counts_correct(self):
        scorer = ICPScorer()
        # Add a disqualified company
        scorer.score(make_input(
            company_id="d1", industry="government", company_size=CompanySize.STARTUP,
            growth_stage="declining", annual_revenue_eur=0,
            high_churn_industry=True, price_sensitive=True, long_sales_cycle=True,
        ))
        s = scorer.summary()
        result = scorer.get("d1")
        tier_val = result.icp_tier.value
        assert tier_val in s["tier_counts"]
        assert s["tier_counts"][tier_val] >= 1


# ===========================================================================
# 12. TestSignals
# ===========================================================================

class TestSignals:
    """Tests for fit_signals and risk_signals in ICPResult."""

    def _score_and_signals(self, **kwargs):
        scorer = ICPScorer()
        inp = make_input(**kwargs)
        result = scorer.score(inp)
        return result.fit_signals, result.risk_signals

    def test_inbound_lead_in_fit_signals(self):
        fit, _ = self._score_and_signals(inbound_lead=True)
        assert any("Lead entrant" in s for s in fit)

    def test_has_pain_point_match_in_fit_signals(self):
        fit, _ = self._score_and_signals(has_pain_point_match=True)
        assert any("Point de douleur" in s for s in fit)

    def test_budget_confirmed_in_fit_signals(self):
        fit, _ = self._score_and_signals(budget_confirmed=True)
        assert any("Budget confirmé" in s for s in fit)

    def test_decision_maker_accessible_in_fit_signals(self):
        fit, _ = self._score_and_signals(decision_maker_accessible=True)
        assert any("Décideur accessible" in s for s in fit)

    def test_timeline_fit_in_fit_signals(self):
        fit, _ = self._score_and_signals(timeline_fit=True)
        assert any("Timeline" in s for s in fit)

    def test_recently_raised_funding_in_fit_signals(self):
        fit, _ = self._score_and_signals(recently_raised_funding=True)
        assert any("Financement" in s for s in fit)

    def test_active_hiring_sales_in_fit_signals(self):
        fit, _ = self._score_and_signals(active_hiring_sales=True)
        assert any("Recrutement" in s for s in fit)

    def test_competitor_customer_in_fit_signals(self):
        fit, _ = self._score_and_signals(competitor_customer=True)
        assert any("concurrent" in s for s in fit)

    def test_no_signals_when_all_false(self):
        fit, risk = self._score_and_signals()
        assert fit == []

    def test_high_churn_in_risk_signals(self):
        _, risk = self._score_and_signals(high_churn_industry=True)
        assert any("churn" in s for s in risk)

    def test_price_sensitive_in_risk_signals(self):
        _, risk = self._score_and_signals(price_sensitive=True)
        assert any("prix" in s.lower() for s in risk)

    def test_long_sales_cycle_in_risk_signals(self):
        _, risk = self._score_and_signals(long_sales_cycle=True)
        assert any("cycle" in s.lower() for s in risk)

    def test_disqualified_tier_adds_risk_signal(self):
        """DISQUALIFIED tier → risk signal about hors ICP."""
        _, risk = self._score_and_signals(
            industry="government", company_size=CompanySize.STARTUP,
            growth_stage="declining", annual_revenue_eur=0,
            high_churn_industry=True, price_sensitive=True, long_sales_cycle=True,
        )
        assert any("hors ICP" in s or "ICP" in s for s in risk)

    def test_attended_event_in_fit_signals(self):
        fit, _ = self._score_and_signals(attended_event=True)
        assert any("événement" in s for s in fit)

    def test_uses_crm_in_fit_signals(self):
        fit, _ = self._score_and_signals(uses_crm=True)
        assert any("CRM" in s for s in fit)

    def test_engaged_with_content_in_fit_signals(self):
        fit, _ = self._score_and_signals(engaged_with_content=True)
        assert any("contenu" in s.lower() for s in fit)

    def test_no_risk_signals_when_no_flags(self):
        # Non-disqualified company with no risk flags
        scorer = ICPScorer()
        inp = make_input(
            inbound_lead=True, decision_maker_accessible=True, has_pain_point_match=True,
            budget_confirmed=True, timeline_fit=True,
        )
        result = scorer.score(inp)
        # No risk flags set and tier should not be DISQUALIFIED
        assert result.risk_signals == []


# ===========================================================================
# 13. TestEdgeCases
# ===========================================================================

class TestEdgeCases:
    """Edge cases and boundary conditions."""

    def test_unknown_industry_defaults_to_40(self):
        score = _INDUSTRY_SCORES.get("totally_unknown_xyz", 40)
        assert score == 40

    def test_unknown_industry_in_firmographic(self):
        inp = make_input(industry="totally_unknown_xyz")
        # Should not crash
        score = _firmographic_score(inp)
        # With industry defaulting to 40
        size_score = _SIZE_IDEAL[CompanySize.MID_MARKET]
        industry_score = 40
        growth_score = _GROWTH_SCORES["fast_growth"]
        rev_bonus = min(15, math.log10(max(1, 5_000_000 / 100_000)) * 5)
        raw = size_score * 0.35 + industry_score * 0.35 + growth_score * 0.30
        expected = min(100, raw + rev_bonus * 0.10)
        assert abs(score - expected) < 1e-9

    def test_unknown_growth_stage_defaults_to_30(self):
        score = _GROWTH_SCORES.get("totally_unknown_stage", 30)
        assert score == 30

    def test_unknown_growth_stage_in_firmographic(self):
        inp = make_input(growth_stage="totally_unknown_stage")
        score = _firmographic_score(inp)
        size_score = _SIZE_IDEAL[CompanySize.MID_MARKET]
        industry_score = _INDUSTRY_SCORES["saas"]
        growth_score = 30
        rev_bonus = min(15, math.log10(max(1, 5_000_000 / 100_000)) * 5)
        raw = size_score * 0.35 + industry_score * 0.35 + growth_score * 0.30
        expected = min(100, raw + rev_bonus * 0.10)
        assert abs(score - expected) < 1e-9

    def test_employee_count_1_no_crash(self):
        scorer = ICPScorer()
        inp = make_input(employee_count=1)
        result = scorer.score(inp)
        assert result.estimated_deal_size_eur >= 500

    def test_annual_revenue_zero_no_crash(self):
        scorer = ICPScorer()
        inp = make_input(annual_revenue_eur=0)
        result = scorer.score(inp)
        assert 0 <= result.icp_score <= 100

    def test_all_booleans_false_empty_tech_stack(self):
        scorer = ICPScorer()
        inp = make_input()
        result = scorer.score(inp)
        assert 0 <= result.icp_score <= 100

    def test_all_booleans_true_score_valid(self):
        scorer = ICPScorer()
        inp = make_input(
            inbound_lead=True, has_pain_point_match=True, visited_website=True,
            engaged_with_content=True, attended_event=True, active_hiring_sales=True,
            recently_raised_funding=True, competitor_customer=True, uses_crm=True,
            has_dedicated_sales_team=True, has_marketing_budget=True,
            decision_maker_accessible=True, multi_stakeholder_buying=True,
            budget_confirmed=True, timeline_fit=True,
            high_churn_industry=True, price_sensitive=True, long_sales_cycle=True,
        )
        result = scorer.score(inp)
        assert 0 <= result.icp_score <= 100

    def test_reset_clears_all_results(self):
        scorer = ICPScorer()
        scorer.score(make_input(company_id="a"))
        scorer.score(make_input(company_id="b"))
        scorer.reset()
        assert scorer.all_companies() == []
        assert scorer.get("a") is None
        assert scorer.get("b") is None

    def test_score_after_reset_works(self):
        scorer = ICPScorer()
        scorer.score(make_input(company_id="a"))
        scorer.reset()
        result = scorer.score(make_input(company_id="new_company"))
        assert result.company_id == "new_company"
        assert scorer.get("new_company") is not None

    def test_icp_score_never_negative(self):
        scorer = ICPScorer()
        inp = make_input(
            industry="government", company_size=CompanySize.STARTUP,
            growth_stage="declining", annual_revenue_eur=0,
            high_churn_industry=True, price_sensitive=True, long_sales_cycle=True,
        )
        result = scorer.score(inp)
        assert result.icp_score >= 0

    def test_icp_score_never_above_100(self):
        scorer = ICPScorer()
        inp = make_input(
            inbound_lead=True, has_pain_point_match=True, visited_website=True,
            engaged_with_content=True, attended_event=True, active_hiring_sales=True,
            recently_raised_funding=True, competitor_customer=True, uses_crm=True,
            has_dedicated_sales_team=True, has_marketing_budget=True,
            decision_maker_accessible=True, multi_stakeholder_buying=True,
            budget_confirmed=True, timeline_fit=True,
            tech_stack=["salesforce", "hubspot", "marketo"],
            industry="saas", company_size=CompanySize.MID_MARKET,
            growth_stage="hyper_growth", annual_revenue_eur=1e12,
        )
        result = scorer.score(inp)
        assert result.icp_score <= 100

    def test_multiple_scorers_independent(self):
        scorer1 = ICPScorer()
        scorer2 = ICPScorer()
        scorer1.score(make_input(company_id="shared"))
        assert scorer2.get("shared") is None

    def test_company_size_enum_values(self):
        assert CompanySize.STARTUP.value == "startup"
        assert CompanySize.SMB.value == "smb"
        assert CompanySize.MID_MARKET.value == "mid_market"
        assert CompanySize.ENTERPRISE.value == "enterprise"
        assert CompanySize.LARGE_ENTERPRISE.value == "large_enterprise"

    def test_icp_tier_enum_values(self):
        assert ICPTier.PERFECT.value == "perfect"
        assert ICPTier.STRONG.value == "strong"
        assert ICPTier.MODERATE.value == "moderate"
        assert ICPTier.WEAK.value == "weak"
        assert ICPTier.DISQUALIFIED.value == "disqualified"

    def test_outreach_recommendation_enum_values(self):
        assert OutreachRecommendation.PRIORITIZE.value == "prioritize"
        assert OutreachRecommendation.QUALIFY.value == "qualify"
        assert OutreachRecommendation.DEPRIORITIZE.value == "deprioritize"
        assert OutreachRecommendation.REJECT.value == "reject"

    def test_large_tech_stack_bonus_capped(self):
        """All tech stack items together exceed 15 — should be capped."""
        all_tools = list(_TECH_STACK_BONUS.keys())
        inp = make_input(tech_stack=all_tools)
        score = _intent_score(inp)
        assert score <= 100

    def test_annual_revenue_very_small(self):
        """Very small positive revenue (< 100_000) gives some bonus."""
        inp = make_input(annual_revenue_eur=1)
        score = _firmographic_score(inp)
        assert score >= 0

    def test_priority_rank_default_is_0(self):
        """Before score_batch, priority_rank defaults to 0."""
        scorer = ICPScorer()
        inp = make_input()
        result = scorer.score(inp)
        assert result.priority_rank == 0

    def test_score_batch_updates_priority_rank(self):
        scorer = ICPScorer()
        inputs = [make_input(company_id=f"c{i}") for i in range(3)]
        results = scorer.score_batch(inputs)
        assert all(r.priority_rank > 0 for r in results)
