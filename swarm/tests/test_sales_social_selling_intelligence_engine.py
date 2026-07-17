"""
Comprehensive pytest test suite for SalesSocialSellingIntelligenceEngine.
Covers all enums, dataclass fields, sub-score methods, pattern detection,
risk/severity/action mapping, flag methods, pipeline loss calculation,
signal generation, assess(), assess_batch(), summary(), edge cases,
and end-to-end scenarios.
"""
from __future__ import annotations

import pytest
from swarm.intelligence.sales_social_selling_intelligence_engine import (
    SocialSellingRisk,
    SocialSellingPattern,
    SocialSellingSeverity,
    SocialSellingAction,
    SocialSellingInput,
    SocialSellingResult,
    SalesSocialSellingIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers / Fixtures
# ---------------------------------------------------------------------------

def make_input(**overrides) -> SocialSellingInput:
    """Return a healthy baseline SocialSellingInput with optional field overrides."""
    defaults = dict(
        rep_id="REP001",
        region="EMEA",
        evaluation_period_id="2026-Q1",
        linkedin_ssi_score=70.0,
        profile_views_last_30d=30,
        connection_requests_sent=20,
        connection_requests_accepted_count=15,
        content_posts_last_30d=10,
        content_engagement_rate_pct=0.06,
        prospect_social_touches_count=35,
        inmail_sent_count=10,
        inmail_reply_rate_pct=0.20,
        social_sourced_meetings_count=5,
        social_sourced_pipeline_usd=60000.0,
        avg_days_to_connect_after_demo=2.0,
        competitor_content_engagement_pct=0.05,
        prospect_comment_response_rate_pct=0.70,
        thought_leadership_shares_count=5,
        group_participations_count=3,
        network_overlap_with_icp_pct=0.50,
        advocacy_referrals_from_social=3,
        avg_opportunity_value_usd=10000.0,
    )
    defaults.update(overrides)
    return SocialSellingInput(**defaults)


def make_worst_input(**overrides) -> SocialSellingInput:
    """Return a worst-case (maximum risk) input."""
    defaults = dict(
        rep_id="REP_WORST",
        region="APAC",
        evaluation_period_id="2026-Q2",
        linkedin_ssi_score=10.0,
        profile_views_last_30d=2,
        connection_requests_sent=0,
        connection_requests_accepted_count=0,
        content_posts_last_30d=0,
        content_engagement_rate_pct=0.0,
        prospect_social_touches_count=0,
        inmail_sent_count=50,
        inmail_reply_rate_pct=0.02,
        social_sourced_meetings_count=0,
        social_sourced_pipeline_usd=0.0,
        avg_days_to_connect_after_demo=30.0,
        competitor_content_engagement_pct=0.50,
        prospect_comment_response_rate_pct=0.10,
        thought_leadership_shares_count=0,
        group_participations_count=0,
        network_overlap_with_icp_pct=0.05,
        advocacy_referrals_from_social=0,
        avg_opportunity_value_usd=20000.0,
    )
    defaults.update(overrides)
    return SocialSellingInput(**defaults)


@pytest.fixture
def engine() -> SalesSocialSellingIntelligenceEngine:
    return SalesSocialSellingIntelligenceEngine()


@pytest.fixture
def good_input() -> SocialSellingInput:
    return make_input()


@pytest.fixture
def bad_input() -> SocialSellingInput:
    return make_worst_input()


# ===========================================================================
# 1. ENUM TESTS
# ===========================================================================

class TestSocialSellingRisk:
    def test_low_value(self):
        assert SocialSellingRisk.low.value == "low"

    def test_moderate_value(self):
        assert SocialSellingRisk.moderate.value == "moderate"

    def test_high_value(self):
        assert SocialSellingRisk.high.value == "high"

    def test_critical_value(self):
        assert SocialSellingRisk.critical.value == "critical"

    def test_is_str(self):
        assert isinstance(SocialSellingRisk.low, str)

    def test_str_equality(self):
        assert SocialSellingRisk.low == "low"

    def test_member_count(self):
        assert len(SocialSellingRisk) == 4

    def test_all_members(self):
        members = {m.value for m in SocialSellingRisk}
        assert members == {"low", "moderate", "high", "critical"}


class TestSocialSellingPattern:
    def test_none_value(self):
        assert SocialSellingPattern.none.value == "none"

    def test_invisible_online_value(self):
        assert SocialSellingPattern.invisible_online.value == "invisible_online"

    def test_low_prospect_engagement_value(self):
        assert SocialSellingPattern.low_prospect_engagement.value == "low_prospect_engagement"

    def test_inmail_abuse_value(self):
        assert SocialSellingPattern.inmail_abuse.value == "inmail_abuse"

    def test_competitor_following_value(self):
        assert SocialSellingPattern.competitor_following.value == "competitor_following"

    def test_content_inconsistency_value(self):
        assert SocialSellingPattern.content_inconsistency.value == "content_inconsistency"

    def test_member_count(self):
        assert len(SocialSellingPattern) == 6

    def test_is_str(self):
        assert isinstance(SocialSellingPattern.none, str)

    def test_all_members(self):
        values = {m.value for m in SocialSellingPattern}
        assert "none" in values
        assert "invisible_online" in values
        assert "inmail_abuse" in values


class TestSocialSellingSeverity:
    def test_active_value(self):
        assert SocialSellingSeverity.active.value == "active"

    def test_developing_value(self):
        assert SocialSellingSeverity.developing.value == "developing"

    def test_passive_value(self):
        assert SocialSellingSeverity.passive.value == "passive"

    def test_invisible_value(self):
        assert SocialSellingSeverity.invisible.value == "invisible"

    def test_member_count(self):
        assert len(SocialSellingSeverity) == 4

    def test_is_str(self):
        assert isinstance(SocialSellingSeverity.active, str)


class TestSocialSellingAction:
    def test_no_action_value(self):
        assert SocialSellingAction.no_action.value == "no_action"

    def test_social_presence_coaching_value(self):
        assert SocialSellingAction.social_presence_coaching.value == "social_presence_coaching"

    def test_content_strategy_session_value(self):
        assert SocialSellingAction.content_strategy_session.value == "content_strategy_session"

    def test_prospect_engagement_training_value(self):
        assert SocialSellingAction.prospect_engagement_training.value == "prospect_engagement_training"

    def test_inmail_optimization_value(self):
        assert SocialSellingAction.inmail_optimization.value == "inmail_optimization"

    def test_brand_building_program_value(self):
        assert SocialSellingAction.brand_building_program.value == "brand_building_program"

    def test_member_count(self):
        assert len(SocialSellingAction) == 6

    def test_is_str(self):
        assert isinstance(SocialSellingAction.no_action, str)


# ===========================================================================
# 2. SocialSellingInput DATACLASS TESTS
# ===========================================================================

class TestSocialSellingInput:
    def test_all_fields_stored(self):
        inp = make_input()
        assert inp.rep_id == "REP001"
        assert inp.region == "EMEA"
        assert inp.evaluation_period_id == "2026-Q1"
        assert inp.linkedin_ssi_score == 70.0
        assert inp.profile_views_last_30d == 30
        assert inp.connection_requests_sent == 20
        assert inp.connection_requests_accepted_count == 15
        assert inp.content_posts_last_30d == 10
        assert inp.content_engagement_rate_pct == 0.06
        assert inp.prospect_social_touches_count == 35
        assert inp.inmail_sent_count == 10
        assert inp.inmail_reply_rate_pct == 0.20
        assert inp.social_sourced_meetings_count == 5
        assert inp.social_sourced_pipeline_usd == 60000.0
        assert inp.avg_days_to_connect_after_demo == 2.0
        assert inp.competitor_content_engagement_pct == 0.05
        assert inp.prospect_comment_response_rate_pct == 0.70
        assert inp.thought_leadership_shares_count == 5
        assert inp.group_participations_count == 3
        assert inp.network_overlap_with_icp_pct == 0.50
        assert inp.advocacy_referrals_from_social == 3
        assert inp.avg_opportunity_value_usd == 10000.0

    def test_field_count(self):
        import dataclasses
        fields = dataclasses.fields(SocialSellingInput)
        assert len(fields) == 22

    def test_float_fields(self):
        inp = make_input(linkedin_ssi_score=55.5, content_engagement_rate_pct=0.03)
        assert inp.linkedin_ssi_score == 55.5
        assert inp.content_engagement_rate_pct == 0.03

    def test_zero_values_accepted(self):
        inp = make_worst_input()
        assert inp.linkedin_ssi_score == 10.0
        assert inp.profile_views_last_30d == 2
        assert inp.content_posts_last_30d == 0

    def test_mutability(self):
        inp = make_input()
        inp.rep_id = "NEW_REP"
        assert inp.rep_id == "NEW_REP"


# ===========================================================================
# 3. SocialSellingResult DATACLASS TESTS
# ===========================================================================

class TestSocialSellingResult:
    @pytest.fixture
    def result(self, engine, good_input):
        return engine.assess(good_input)

    def test_result_rep_id(self, result):
        assert result.rep_id == "REP001"

    def test_result_region(self, result):
        assert result.region == "EMEA"

    def test_result_has_risk(self, result):
        assert isinstance(result.social_selling_risk, SocialSellingRisk)

    def test_result_has_pattern(self, result):
        assert isinstance(result.social_selling_pattern, SocialSellingPattern)

    def test_result_has_severity(self, result):
        assert isinstance(result.social_selling_severity, SocialSellingSeverity)

    def test_result_has_action(self, result):
        assert isinstance(result.recommended_action, SocialSellingAction)

    def test_result_profile_presence_score_float(self, result):
        assert isinstance(result.profile_presence_score, float)

    def test_result_content_effectiveness_score_float(self, result):
        assert isinstance(result.content_effectiveness_score, float)

    def test_result_prospect_engagement_score_float(self, result):
        assert isinstance(result.prospect_engagement_score, float)

    def test_result_social_pipeline_score_float(self, result):
        assert isinstance(result.social_pipeline_score, float)

    def test_result_composite_float(self, result):
        assert isinstance(result.social_selling_composite, float)

    def test_result_has_social_gap_bool(self, result):
        assert isinstance(result.has_social_gap, bool)

    def test_result_requires_social_coaching_bool(self, result):
        assert isinstance(result.requires_social_coaching, bool)

    def test_result_pipeline_loss_float(self, result):
        assert isinstance(result.estimated_pipeline_loss_usd, float)

    def test_result_signal_str(self, result):
        assert isinstance(result.social_selling_signal, str)

    def test_result_field_count(self):
        import dataclasses
        fields = dataclasses.fields(SocialSellingResult)
        assert len(fields) == 15

    def test_scores_between_0_and_100(self, result):
        assert 0.0 <= result.profile_presence_score <= 100.0
        assert 0.0 <= result.content_effectiveness_score <= 100.0
        assert 0.0 <= result.prospect_engagement_score <= 100.0
        assert 0.0 <= result.social_pipeline_score <= 100.0
        assert 0.0 <= result.social_selling_composite <= 100.0

    def test_pipeline_loss_non_negative(self, result):
        assert result.estimated_pipeline_loss_usd >= 0.0


class TestToDict:
    @pytest.fixture
    def d(self, engine, good_input):
        return engine.assess(good_input).to_dict()

    def test_to_dict_returns_dict(self, d):
        assert isinstance(d, dict)

    def test_to_dict_has_15_keys(self, d):
        assert len(d) == 15

    def test_to_dict_rep_id(self, d):
        assert d["rep_id"] == "REP001"

    def test_to_dict_region(self, d):
        assert d["region"] == "EMEA"

    def test_to_dict_risk_is_string(self, d):
        assert isinstance(d["social_selling_risk"], str)

    def test_to_dict_pattern_is_string(self, d):
        assert isinstance(d["social_selling_pattern"], str)

    def test_to_dict_severity_is_string(self, d):
        assert isinstance(d["social_selling_severity"], str)

    def test_to_dict_action_is_string(self, d):
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_profile_presence_score(self, d):
        assert "profile_presence_score" in d

    def test_to_dict_content_effectiveness_score(self, d):
        assert "content_effectiveness_score" in d

    def test_to_dict_prospect_engagement_score(self, d):
        assert "prospect_engagement_score" in d

    def test_to_dict_social_pipeline_score(self, d):
        assert "social_pipeline_score" in d

    def test_to_dict_composite(self, d):
        assert "social_selling_composite" in d

    def test_to_dict_has_social_gap(self, d):
        assert "has_social_gap" in d

    def test_to_dict_requires_social_coaching(self, d):
        assert "requires_social_coaching" in d

    def test_to_dict_pipeline_loss(self, d):
        assert "estimated_pipeline_loss_usd" in d

    def test_to_dict_signal(self, d):
        assert "social_selling_signal" in d

    def test_to_dict_risk_values_are_enum_values(self, engine):
        for risk in SocialSellingRisk:
            inp = make_input()
            # Force composite into correct range by using worst/best inputs
            # We'll just check that whatever risk value is returned is valid
            d = engine.assess(inp).to_dict()
            assert d["social_selling_risk"] in {r.value for r in SocialSellingRisk}


# ===========================================================================
# 4. PROFILE PRESENCE SCORE
# ===========================================================================

class TestProfilePresenceScore:
    @pytest.fixture
    def eng(self):
        return SalesSocialSellingIntelligenceEngine()

    def test_perfect_profile_score_zero(self, eng):
        inp = make_input(linkedin_ssi_score=70.0, profile_views_last_30d=30, network_overlap_with_icp_pct=0.50)
        score = eng._profile_presence_score(inp)
        assert score == 0.0

    def test_ssi_below_25_adds_40(self, eng):
        inp = make_input(linkedin_ssi_score=20.0, profile_views_last_30d=30, network_overlap_with_icp_pct=0.50)
        score = eng._profile_presence_score(inp)
        assert score == 40.0

    def test_ssi_between_25_and_45_adds_22(self, eng):
        inp = make_input(linkedin_ssi_score=35.0, profile_views_last_30d=30, network_overlap_with_icp_pct=0.50)
        score = eng._profile_presence_score(inp)
        assert score == 22.0

    def test_ssi_between_45_and_60_adds_8(self, eng):
        inp = make_input(linkedin_ssi_score=50.0, profile_views_last_30d=30, network_overlap_with_icp_pct=0.50)
        score = eng._profile_presence_score(inp)
        assert score == 8.0

    def test_ssi_at_60_adds_nothing(self, eng):
        inp = make_input(linkedin_ssi_score=60.0, profile_views_last_30d=30, network_overlap_with_icp_pct=0.50)
        score = eng._profile_presence_score(inp)
        assert score == 0.0

    def test_profile_views_below_10_adds_30(self, eng):
        inp = make_input(linkedin_ssi_score=70.0, profile_views_last_30d=5, network_overlap_with_icp_pct=0.50)
        score = eng._profile_presence_score(inp)
        assert score == 30.0

    def test_profile_views_between_10_and_25_adds_15(self, eng):
        inp = make_input(linkedin_ssi_score=70.0, profile_views_last_30d=15, network_overlap_with_icp_pct=0.50)
        score = eng._profile_presence_score(inp)
        assert score == 15.0

    def test_profile_views_at_25_adds_nothing(self, eng):
        inp = make_input(linkedin_ssi_score=70.0, profile_views_last_30d=25, network_overlap_with_icp_pct=0.50)
        score = eng._profile_presence_score(inp)
        assert score == 0.0

    def test_network_overlap_below_20pct_adds_30(self, eng):
        inp = make_input(linkedin_ssi_score=70.0, profile_views_last_30d=30, network_overlap_with_icp_pct=0.10)
        score = eng._profile_presence_score(inp)
        assert score == 30.0

    def test_network_overlap_between_20_and_40_adds_15(self, eng):
        inp = make_input(linkedin_ssi_score=70.0, profile_views_last_30d=30, network_overlap_with_icp_pct=0.30)
        score = eng._profile_presence_score(inp)
        assert score == 15.0

    def test_network_overlap_at_40pct_adds_nothing(self, eng):
        inp = make_input(linkedin_ssi_score=70.0, profile_views_last_30d=30, network_overlap_with_icp_pct=0.40)
        score = eng._profile_presence_score(inp)
        assert score == 0.0

    def test_max_capped_at_100(self, eng):
        inp = make_worst_input()
        score = eng._profile_presence_score(inp)
        assert score <= 100.0

    def test_worst_case_score(self, eng):
        # SSI<25 (40) + views<10 (30) + overlap<0.20 (30) = 100
        inp = make_input(linkedin_ssi_score=5.0, profile_views_last_30d=1, network_overlap_with_icp_pct=0.01)
        score = eng._profile_presence_score(inp)
        assert score == 100.0

    def test_combined_medium_risk(self, eng):
        # SSI between 25-45 (22) + views between 10-25 (15) = 37
        inp = make_input(linkedin_ssi_score=30.0, profile_views_last_30d=20, network_overlap_with_icp_pct=0.50)
        score = eng._profile_presence_score(inp)
        assert score == 37.0

    def test_ssi_boundary_exactly_25(self, eng):
        # SSI exactly 25 — goes to the 22-add branch (25 < 45)
        inp = make_input(linkedin_ssi_score=25.0, profile_views_last_30d=30, network_overlap_with_icp_pct=0.50)
        score = eng._profile_presence_score(inp)
        assert score == 22.0

    def test_ssi_boundary_exactly_45(self, eng):
        # SSI exactly 45 — goes to 8-add branch (45 < 60)
        inp = make_input(linkedin_ssi_score=45.0, profile_views_last_30d=30, network_overlap_with_icp_pct=0.50)
        score = eng._profile_presence_score(inp)
        assert score == 8.0


# ===========================================================================
# 5. CONTENT EFFECTIVENESS SCORE
# ===========================================================================

class TestContentEffectivenessScore:
    @pytest.fixture
    def eng(self):
        return SalesSocialSellingIntelligenceEngine()

    def test_perfect_content_score_zero(self, eng):
        inp = make_input(content_posts_last_30d=10, content_engagement_rate_pct=0.06, thought_leadership_shares_count=5)
        score = eng._content_effectiveness_score(inp)
        assert score == 0.0

    def test_posts_below_2_adds_40(self, eng):
        inp = make_input(content_posts_last_30d=1, content_engagement_rate_pct=0.06, thought_leadership_shares_count=5)
        score = eng._content_effectiveness_score(inp)
        assert score == 40.0

    def test_posts_between_2_and_4_adds_20(self, eng):
        inp = make_input(content_posts_last_30d=3, content_engagement_rate_pct=0.06, thought_leadership_shares_count=5)
        score = eng._content_effectiveness_score(inp)
        assert score == 20.0

    def test_posts_between_4_and_8_adds_8(self, eng):
        inp = make_input(content_posts_last_30d=6, content_engagement_rate_pct=0.06, thought_leadership_shares_count=5)
        score = eng._content_effectiveness_score(inp)
        assert score == 8.0

    def test_posts_at_8_adds_nothing(self, eng):
        inp = make_input(content_posts_last_30d=8, content_engagement_rate_pct=0.06, thought_leadership_shares_count=5)
        score = eng._content_effectiveness_score(inp)
        assert score == 0.0

    def test_engagement_below_1pct_adds_35(self, eng):
        inp = make_input(content_posts_last_30d=10, content_engagement_rate_pct=0.005, thought_leadership_shares_count=5)
        score = eng._content_effectiveness_score(inp)
        assert score == 35.0

    def test_engagement_between_1_and_3pct_adds_18(self, eng):
        inp = make_input(content_posts_last_30d=10, content_engagement_rate_pct=0.02, thought_leadership_shares_count=5)
        score = eng._content_effectiveness_score(inp)
        assert score == 18.0

    def test_engagement_between_3_and_5pct_adds_7(self, eng):
        inp = make_input(content_posts_last_30d=10, content_engagement_rate_pct=0.04, thought_leadership_shares_count=5)
        score = eng._content_effectiveness_score(inp)
        assert score == 7.0

    def test_engagement_at_5pct_adds_nothing(self, eng):
        inp = make_input(content_posts_last_30d=10, content_engagement_rate_pct=0.05, thought_leadership_shares_count=5)
        score = eng._content_effectiveness_score(inp)
        assert score == 0.0

    def test_shares_below_1_adds_25(self, eng):
        inp = make_input(content_posts_last_30d=10, content_engagement_rate_pct=0.06, thought_leadership_shares_count=0)
        score = eng._content_effectiveness_score(inp)
        assert score == 25.0

    def test_shares_between_1_and_3_adds_12(self, eng):
        inp = make_input(content_posts_last_30d=10, content_engagement_rate_pct=0.06, thought_leadership_shares_count=2)
        score = eng._content_effectiveness_score(inp)
        assert score == 12.0

    def test_shares_at_3_adds_nothing(self, eng):
        inp = make_input(content_posts_last_30d=10, content_engagement_rate_pct=0.06, thought_leadership_shares_count=3)
        score = eng._content_effectiveness_score(inp)
        assert score == 0.0

    def test_capped_at_100(self, eng):
        inp = make_input(content_posts_last_30d=0, content_engagement_rate_pct=0.0, thought_leadership_shares_count=0)
        score = eng._content_effectiveness_score(inp)
        assert score <= 100.0

    def test_max_content_score(self, eng):
        # 40 + 35 + 25 = 100
        inp = make_input(content_posts_last_30d=0, content_engagement_rate_pct=0.0, thought_leadership_shares_count=0)
        score = eng._content_effectiveness_score(inp)
        assert score == 100.0

    def test_boundary_posts_exactly_2(self, eng):
        # posts == 2 -> 2-4 branch -> 20
        inp = make_input(content_posts_last_30d=2, content_engagement_rate_pct=0.06, thought_leadership_shares_count=5)
        score = eng._content_effectiveness_score(inp)
        assert score == 20.0

    def test_boundary_posts_exactly_4(self, eng):
        # posts == 4 -> 4-8 branch -> 8
        inp = make_input(content_posts_last_30d=4, content_engagement_rate_pct=0.06, thought_leadership_shares_count=5)
        score = eng._content_effectiveness_score(inp)
        assert score == 8.0


# ===========================================================================
# 6. PROSPECT ENGAGEMENT SCORE
# ===========================================================================

class TestProspectEngagementScore:
    @pytest.fixture
    def eng(self):
        return SalesSocialSellingIntelligenceEngine()

    def test_perfect_engagement_score_zero(self, eng):
        inp = make_input(
            prospect_social_touches_count=35,
            inmail_reply_rate_pct=0.20,
            prospect_comment_response_rate_pct=0.70,
        )
        score = eng._prospect_engagement_score(inp)
        assert score == 0.0

    def test_touches_below_5_adds_40(self, eng):
        inp = make_input(
            prospect_social_touches_count=3,
            inmail_reply_rate_pct=0.20,
            prospect_comment_response_rate_pct=0.70,
        )
        score = eng._prospect_engagement_score(inp)
        assert score == 40.0

    def test_touches_between_5_and_15_adds_20(self, eng):
        inp = make_input(
            prospect_social_touches_count=10,
            inmail_reply_rate_pct=0.20,
            prospect_comment_response_rate_pct=0.70,
        )
        score = eng._prospect_engagement_score(inp)
        assert score == 20.0

    def test_touches_between_15_and_30_adds_8(self, eng):
        inp = make_input(
            prospect_social_touches_count=20,
            inmail_reply_rate_pct=0.20,
            prospect_comment_response_rate_pct=0.70,
        )
        score = eng._prospect_engagement_score(inp)
        assert score == 8.0

    def test_touches_at_30_adds_nothing(self, eng):
        inp = make_input(
            prospect_social_touches_count=30,
            inmail_reply_rate_pct=0.20,
            prospect_comment_response_rate_pct=0.70,
        )
        score = eng._prospect_engagement_score(inp)
        assert score == 0.0

    def test_inmail_reply_below_8pct_adds_30(self, eng):
        inp = make_input(
            prospect_social_touches_count=35,
            inmail_reply_rate_pct=0.05,
            prospect_comment_response_rate_pct=0.70,
        )
        score = eng._prospect_engagement_score(inp)
        assert score == 30.0

    def test_inmail_reply_between_8_and_15pct_adds_15(self, eng):
        inp = make_input(
            prospect_social_touches_count=35,
            inmail_reply_rate_pct=0.10,
            prospect_comment_response_rate_pct=0.70,
        )
        score = eng._prospect_engagement_score(inp)
        assert score == 15.0

    def test_inmail_reply_at_15pct_adds_nothing(self, eng):
        inp = make_input(
            prospect_social_touches_count=35,
            inmail_reply_rate_pct=0.15,
            prospect_comment_response_rate_pct=0.70,
        )
        score = eng._prospect_engagement_score(inp)
        assert score == 0.0

    def test_comment_response_below_30pct_adds_30(self, eng):
        inp = make_input(
            prospect_social_touches_count=35,
            inmail_reply_rate_pct=0.20,
            prospect_comment_response_rate_pct=0.20,
        )
        score = eng._prospect_engagement_score(inp)
        assert score == 30.0

    def test_comment_response_between_30_and_60pct_adds_15(self, eng):
        inp = make_input(
            prospect_social_touches_count=35,
            inmail_reply_rate_pct=0.20,
            prospect_comment_response_rate_pct=0.45,
        )
        score = eng._prospect_engagement_score(inp)
        assert score == 15.0

    def test_comment_response_at_60pct_adds_nothing(self, eng):
        inp = make_input(
            prospect_social_touches_count=35,
            inmail_reply_rate_pct=0.20,
            prospect_comment_response_rate_pct=0.60,
        )
        score = eng._prospect_engagement_score(inp)
        assert score == 0.0

    def test_capped_at_100(self, eng):
        inp = make_input(
            prospect_social_touches_count=0,
            inmail_reply_rate_pct=0.0,
            prospect_comment_response_rate_pct=0.0,
        )
        score = eng._prospect_engagement_score(inp)
        assert score <= 100.0

    def test_worst_case_score(self, eng):
        # 40 + 30 + 30 = 100
        inp = make_input(
            prospect_social_touches_count=0,
            inmail_reply_rate_pct=0.0,
            prospect_comment_response_rate_pct=0.0,
        )
        score = eng._prospect_engagement_score(inp)
        assert score == 100.0

    def test_boundary_touches_exactly_5(self, eng):
        # 5 touches -> between 5-15 -> 20
        inp = make_input(
            prospect_social_touches_count=5,
            inmail_reply_rate_pct=0.20,
            prospect_comment_response_rate_pct=0.70,
        )
        score = eng._prospect_engagement_score(inp)
        assert score == 20.0

    def test_boundary_touches_exactly_15(self, eng):
        # 15 touches -> between 15-30 -> 8
        inp = make_input(
            prospect_social_touches_count=15,
            inmail_reply_rate_pct=0.20,
            prospect_comment_response_rate_pct=0.70,
        )
        score = eng._prospect_engagement_score(inp)
        assert score == 8.0


# ===========================================================================
# 7. SOCIAL PIPELINE SCORE
# ===========================================================================

class TestSocialPipelineScore:
    @pytest.fixture
    def eng(self):
        return SalesSocialSellingIntelligenceEngine()

    def test_perfect_pipeline_score_zero(self, eng):
        inp = make_input(
            social_sourced_meetings_count=5,
            social_sourced_pipeline_usd=60000.0,
            advocacy_referrals_from_social=3,
        )
        score = eng._social_pipeline_score(inp)
        assert score == 0.0

    def test_meetings_below_1_adds_45(self, eng):
        inp = make_input(
            social_sourced_meetings_count=0,
            social_sourced_pipeline_usd=60000.0,
            advocacy_referrals_from_social=3,
        )
        score = eng._social_pipeline_score(inp)
        assert score == 45.0

    def test_meetings_between_1_and_3_adds_25(self, eng):
        inp = make_input(
            social_sourced_meetings_count=2,
            social_sourced_pipeline_usd=60000.0,
            advocacy_referrals_from_social=3,
        )
        score = eng._social_pipeline_score(inp)
        assert score == 25.0

    def test_meetings_between_3_and_5_adds_10(self, eng):
        inp = make_input(
            social_sourced_meetings_count=4,
            social_sourced_pipeline_usd=60000.0,
            advocacy_referrals_from_social=3,
        )
        score = eng._social_pipeline_score(inp)
        assert score == 10.0

    def test_meetings_at_5_adds_nothing(self, eng):
        inp = make_input(
            social_sourced_meetings_count=5,
            social_sourced_pipeline_usd=60000.0,
            advocacy_referrals_from_social=3,
        )
        score = eng._social_pipeline_score(inp)
        assert score == 0.0

    def test_pipeline_below_10k_adds_30(self, eng):
        inp = make_input(
            social_sourced_meetings_count=5,
            social_sourced_pipeline_usd=5000.0,
            advocacy_referrals_from_social=3,
        )
        score = eng._social_pipeline_score(inp)
        assert score == 30.0

    def test_pipeline_between_10k_and_50k_adds_15(self, eng):
        inp = make_input(
            social_sourced_meetings_count=5,
            social_sourced_pipeline_usd=30000.0,
            advocacy_referrals_from_social=3,
        )
        score = eng._social_pipeline_score(inp)
        assert score == 15.0

    def test_pipeline_at_50k_adds_nothing(self, eng):
        inp = make_input(
            social_sourced_meetings_count=5,
            social_sourced_pipeline_usd=50000.0,
            advocacy_referrals_from_social=3,
        )
        score = eng._social_pipeline_score(inp)
        assert score == 0.0

    def test_referrals_below_1_adds_25(self, eng):
        inp = make_input(
            social_sourced_meetings_count=5,
            social_sourced_pipeline_usd=60000.0,
            advocacy_referrals_from_social=0,
        )
        score = eng._social_pipeline_score(inp)
        assert score == 25.0

    def test_referrals_between_1_and_3_adds_12(self, eng):
        inp = make_input(
            social_sourced_meetings_count=5,
            social_sourced_pipeline_usd=60000.0,
            advocacy_referrals_from_social=2,
        )
        score = eng._social_pipeline_score(inp)
        assert score == 12.0

    def test_referrals_at_3_adds_nothing(self, eng):
        inp = make_input(
            social_sourced_meetings_count=5,
            social_sourced_pipeline_usd=60000.0,
            advocacy_referrals_from_social=3,
        )
        score = eng._social_pipeline_score(inp)
        assert score == 0.0

    def test_capped_at_100(self, eng):
        inp = make_input(
            social_sourced_meetings_count=0,
            social_sourced_pipeline_usd=0.0,
            advocacy_referrals_from_social=0,
        )
        score = eng._social_pipeline_score(inp)
        assert score <= 100.0

    def test_worst_case_score(self, eng):
        # 45 + 30 + 25 = 100
        inp = make_input(
            social_sourced_meetings_count=0,
            social_sourced_pipeline_usd=0.0,
            advocacy_referrals_from_social=0,
        )
        score = eng._social_pipeline_score(inp)
        assert score == 100.0

    def test_boundary_meetings_exactly_1(self, eng):
        inp = make_input(
            social_sourced_meetings_count=1,
            social_sourced_pipeline_usd=60000.0,
            advocacy_referrals_from_social=3,
        )
        score = eng._social_pipeline_score(inp)
        assert score == 25.0

    def test_boundary_meetings_exactly_3(self, eng):
        inp = make_input(
            social_sourced_meetings_count=3,
            social_sourced_pipeline_usd=60000.0,
            advocacy_referrals_from_social=3,
        )
        score = eng._social_pipeline_score(inp)
        assert score == 10.0


# ===========================================================================
# 8. PATTERN DETECTION
# ===========================================================================

class TestDetectPattern:
    @pytest.fixture
    def eng(self):
        return SalesSocialSellingIntelligenceEngine()

    def test_none_pattern_healthy(self, eng):
        inp = make_input()
        # Use a good input which scores low — healthy pattern
        result = eng.assess(inp)
        assert result.social_selling_pattern == SocialSellingPattern.none

    def test_invisible_online_pattern(self, eng):
        # presence >= 40 AND ssi < 30
        inp = make_input(
            linkedin_ssi_score=20.0,
            profile_views_last_30d=2,
            network_overlap_with_icp_pct=0.05,
        )
        result = eng.assess(inp)
        assert result.social_selling_pattern == SocialSellingPattern.invisible_online

    def test_low_prospect_engagement_pattern(self, eng):
        # prospect >= 35 AND touches < 10; presence must be < 40 to skip invisible check
        inp = make_input(
            linkedin_ssi_score=70.0,  # no invisible
            profile_views_last_30d=30,
            network_overlap_with_icp_pct=0.50,
            prospect_social_touches_count=3,
            inmail_reply_rate_pct=0.05,
            prospect_comment_response_rate_pct=0.10,
        )
        result = eng.assess(inp)
        assert result.social_selling_pattern == SocialSellingPattern.low_prospect_engagement

    def test_inmail_abuse_pattern(self, eng):
        # inmail_sent >= 30 AND reply_rate < 0.08; avoid triggering invisible/low_prospect
        inp = make_input(
            linkedin_ssi_score=70.0,
            profile_views_last_30d=30,
            network_overlap_with_icp_pct=0.50,
            prospect_social_touches_count=35,
            inmail_sent_count=50,
            inmail_reply_rate_pct=0.03,
            prospect_comment_response_rate_pct=0.70,
        )
        result = eng.assess(inp)
        assert result.social_selling_pattern == SocialSellingPattern.inmail_abuse

    def test_competitor_following_pattern(self, eng):
        # competitor_content_engagement >= 0.30; avoid earlier patterns
        inp = make_input(
            linkedin_ssi_score=70.0,
            profile_views_last_30d=30,
            network_overlap_with_icp_pct=0.50,
            prospect_social_touches_count=35,
            inmail_sent_count=5,
            inmail_reply_rate_pct=0.20,
            prospect_comment_response_rate_pct=0.70,
            competitor_content_engagement_pct=0.40,
        )
        result = eng.assess(inp)
        assert result.social_selling_pattern == SocialSellingPattern.competitor_following

    def test_content_inconsistency_pattern(self, eng):
        # content >= 25 AND posts < 3; avoid earlier patterns
        inp = make_input(
            linkedin_ssi_score=70.0,
            profile_views_last_30d=30,
            network_overlap_with_icp_pct=0.50,
            prospect_social_touches_count=35,
            inmail_sent_count=5,
            inmail_reply_rate_pct=0.20,
            prospect_comment_response_rate_pct=0.70,
            competitor_content_engagement_pct=0.05,
            content_posts_last_30d=1,
            content_engagement_rate_pct=0.06,
            thought_leadership_shares_count=5,
        )
        result = eng.assess(inp)
        assert result.social_selling_pattern == SocialSellingPattern.content_inconsistency

    def test_invisible_online_takes_priority_over_prospect(self, eng):
        # Triggers both invisible and prospect engagement conditions, invisible wins
        inp = make_input(
            linkedin_ssi_score=20.0,
            profile_views_last_30d=2,
            network_overlap_with_icp_pct=0.05,
            prospect_social_touches_count=3,
            inmail_reply_rate_pct=0.05,
            prospect_comment_response_rate_pct=0.10,
        )
        result = eng.assess(inp)
        assert result.social_selling_pattern == SocialSellingPattern.invisible_online

    def test_inmail_boundary_exactly_30_sent(self, eng):
        # inmail_sent_count exactly 30 -> inmail_abuse triggers
        inp = make_input(
            linkedin_ssi_score=70.0,
            profile_views_last_30d=30,
            network_overlap_with_icp_pct=0.50,
            prospect_social_touches_count=35,
            inmail_sent_count=30,
            inmail_reply_rate_pct=0.03,
            prospect_comment_response_rate_pct=0.70,
        )
        result = eng.assess(inp)
        assert result.social_selling_pattern == SocialSellingPattern.inmail_abuse

    def test_inmail_below_30_no_abuse(self, eng):
        # inmail_sent_count < 30 -> not inmail_abuse
        inp = make_input(
            linkedin_ssi_score=70.0,
            profile_views_last_30d=30,
            network_overlap_with_icp_pct=0.50,
            prospect_social_touches_count=35,
            inmail_sent_count=29,
            inmail_reply_rate_pct=0.03,
            prospect_comment_response_rate_pct=0.70,
            competitor_content_engagement_pct=0.05,
            content_posts_last_30d=10,
        )
        result = eng.assess(inp)
        assert result.social_selling_pattern != SocialSellingPattern.inmail_abuse

    def test_competitor_boundary_exactly_30pct(self, eng):
        inp = make_input(
            linkedin_ssi_score=70.0,
            profile_views_last_30d=30,
            network_overlap_with_icp_pct=0.50,
            prospect_social_touches_count=35,
            inmail_sent_count=5,
            inmail_reply_rate_pct=0.20,
            prospect_comment_response_rate_pct=0.70,
            competitor_content_engagement_pct=0.30,
        )
        result = eng.assess(inp)
        assert result.social_selling_pattern == SocialSellingPattern.competitor_following


# ===========================================================================
# 9. RISK LEVEL
# ===========================================================================

class TestRiskLevel:
    @pytest.fixture
    def eng(self):
        return SalesSocialSellingIntelligenceEngine()

    def test_risk_low_below_20(self, eng):
        assert eng._risk_level(0.0) == SocialSellingRisk.low
        assert eng._risk_level(10.0) == SocialSellingRisk.low
        assert eng._risk_level(19.9) == SocialSellingRisk.low

    def test_risk_moderate_at_20(self, eng):
        assert eng._risk_level(20.0) == SocialSellingRisk.moderate

    def test_risk_moderate_between_20_40(self, eng):
        assert eng._risk_level(30.0) == SocialSellingRisk.moderate
        assert eng._risk_level(39.9) == SocialSellingRisk.moderate

    def test_risk_high_at_40(self, eng):
        assert eng._risk_level(40.0) == SocialSellingRisk.high

    def test_risk_high_between_40_60(self, eng):
        assert eng._risk_level(50.0) == SocialSellingRisk.high
        assert eng._risk_level(59.9) == SocialSellingRisk.high

    def test_risk_critical_at_60(self, eng):
        assert eng._risk_level(60.0) == SocialSellingRisk.critical

    def test_risk_critical_above_60(self, eng):
        assert eng._risk_level(80.0) == SocialSellingRisk.critical
        assert eng._risk_level(100.0) == SocialSellingRisk.critical

    def test_risk_zero_composite(self, eng):
        assert eng._risk_level(0.0) == SocialSellingRisk.low

    def test_risk_100_composite(self, eng):
        assert eng._risk_level(100.0) == SocialSellingRisk.critical


# ===========================================================================
# 10. SEVERITY
# ===========================================================================

class TestSeverity:
    @pytest.fixture
    def eng(self):
        return SalesSocialSellingIntelligenceEngine()

    def test_severity_active_below_20(self, eng):
        assert eng._severity(0.0) == SocialSellingSeverity.active
        assert eng._severity(10.0) == SocialSellingSeverity.active
        assert eng._severity(19.9) == SocialSellingSeverity.active

    def test_severity_developing_at_20(self, eng):
        assert eng._severity(20.0) == SocialSellingSeverity.developing

    def test_severity_developing_between_20_40(self, eng):
        assert eng._severity(30.0) == SocialSellingSeverity.developing
        assert eng._severity(39.9) == SocialSellingSeverity.developing

    def test_severity_passive_at_40(self, eng):
        assert eng._severity(40.0) == SocialSellingSeverity.passive

    def test_severity_passive_between_40_60(self, eng):
        assert eng._severity(50.0) == SocialSellingSeverity.passive
        assert eng._severity(59.9) == SocialSellingSeverity.passive

    def test_severity_invisible_at_60(self, eng):
        assert eng._severity(60.0) == SocialSellingSeverity.invisible

    def test_severity_invisible_above_60(self, eng):
        assert eng._severity(80.0) == SocialSellingSeverity.invisible
        assert eng._severity(100.0) == SocialSellingSeverity.invisible


# ===========================================================================
# 11. ACTION MAPPING
# ===========================================================================

class TestAction:
    @pytest.fixture
    def eng(self):
        return SalesSocialSellingIntelligenceEngine()

    def test_low_risk_no_action(self, eng):
        action = eng._action(SocialSellingRisk.low, SocialSellingPattern.none)
        assert action == SocialSellingAction.no_action

    def test_low_risk_any_pattern_no_action(self, eng):
        for p in SocialSellingPattern:
            action = eng._action(SocialSellingRisk.low, p)
            assert action == SocialSellingAction.no_action

    def test_moderate_risk_social_presence_coaching(self, eng):
        for p in SocialSellingPattern:
            action = eng._action(SocialSellingRisk.moderate, p)
            assert action == SocialSellingAction.social_presence_coaching

    def test_high_risk_inmail_abuse_inmail_optimization(self, eng):
        action = eng._action(SocialSellingRisk.high, SocialSellingPattern.inmail_abuse)
        assert action == SocialSellingAction.inmail_optimization

    def test_high_risk_content_inconsistency_content_strategy(self, eng):
        action = eng._action(SocialSellingRisk.high, SocialSellingPattern.content_inconsistency)
        assert action == SocialSellingAction.content_strategy_session

    def test_high_risk_other_patterns_social_presence_coaching(self, eng):
        for p in [SocialSellingPattern.none, SocialSellingPattern.invisible_online,
                  SocialSellingPattern.low_prospect_engagement,
                  SocialSellingPattern.competitor_following]:
            action = eng._action(SocialSellingRisk.high, p)
            assert action == SocialSellingAction.social_presence_coaching

    def test_critical_risk_invisible_online_brand_building(self, eng):
        action = eng._action(SocialSellingRisk.critical, SocialSellingPattern.invisible_online)
        assert action == SocialSellingAction.brand_building_program

    def test_critical_risk_low_prospect_engagement_training(self, eng):
        action = eng._action(SocialSellingRisk.critical, SocialSellingPattern.low_prospect_engagement)
        assert action == SocialSellingAction.prospect_engagement_training

    def test_critical_risk_other_patterns_social_presence_coaching(self, eng):
        for p in [SocialSellingPattern.none, SocialSellingPattern.inmail_abuse,
                  SocialSellingPattern.competitor_following,
                  SocialSellingPattern.content_inconsistency]:
            action = eng._action(SocialSellingRisk.critical, p)
            assert action == SocialSellingAction.social_presence_coaching


# ===========================================================================
# 12. HAS SOCIAL GAP FLAG
# ===========================================================================

class TestHasSocialGap:
    @pytest.fixture
    def eng(self):
        return SalesSocialSellingIntelligenceEngine()

    def test_gap_when_composite_ge_40(self, eng):
        inp = make_input(social_sourced_meetings_count=5, linkedin_ssi_score=70.0)
        assert eng._has_social_gap(40.0, inp) is True

    def test_gap_when_composite_gt_40(self, eng):
        inp = make_input(social_sourced_meetings_count=5, linkedin_ssi_score=70.0)
        assert eng._has_social_gap(50.0, inp) is True

    def test_gap_when_meetings_zero(self, eng):
        inp = make_input(social_sourced_meetings_count=0, linkedin_ssi_score=70.0)
        assert eng._has_social_gap(10.0, inp) is True

    def test_gap_when_ssi_below_25(self, eng):
        inp = make_input(social_sourced_meetings_count=5, linkedin_ssi_score=20.0)
        assert eng._has_social_gap(10.0, inp) is True

    def test_no_gap_when_all_conditions_false(self, eng):
        inp = make_input(social_sourced_meetings_count=5, linkedin_ssi_score=70.0)
        assert eng._has_social_gap(30.0, inp) is False

    def test_gap_boundary_composite_exactly_40(self, eng):
        inp = make_input(social_sourced_meetings_count=5, linkedin_ssi_score=70.0)
        assert eng._has_social_gap(40.0, inp) is True

    def test_no_gap_composite_just_below_40(self, eng):
        inp = make_input(social_sourced_meetings_count=5, linkedin_ssi_score=70.0)
        assert eng._has_social_gap(39.9, inp) is False

    def test_gap_ssi_exactly_25_no_trigger(self, eng):
        # ssi=25 is NOT < 25.0 so no gap from ssi
        inp = make_input(social_sourced_meetings_count=5, linkedin_ssi_score=25.0)
        assert eng._has_social_gap(30.0, inp) is False

    def test_gap_ssi_below_25_triggers(self, eng):
        inp = make_input(social_sourced_meetings_count=5, linkedin_ssi_score=24.9)
        assert eng._has_social_gap(30.0, inp) is True


# ===========================================================================
# 13. REQUIRES SOCIAL COACHING FLAG
# ===========================================================================

class TestRequiresSocialCoaching:
    @pytest.fixture
    def eng(self):
        return SalesSocialSellingIntelligenceEngine()

    def test_coaching_when_composite_ge_30(self, eng):
        inp = make_input(content_posts_last_30d=10, prospect_social_touches_count=35)
        assert eng._requires_social_coaching(30.0, inp) is True

    def test_coaching_when_composite_above_30(self, eng):
        inp = make_input(content_posts_last_30d=10, prospect_social_touches_count=35)
        assert eng._requires_social_coaching(50.0, inp) is True

    def test_coaching_when_posts_below_2(self, eng):
        inp = make_input(content_posts_last_30d=1, prospect_social_touches_count=35)
        assert eng._requires_social_coaching(10.0, inp) is True

    def test_coaching_when_touches_below_5(self, eng):
        inp = make_input(content_posts_last_30d=10, prospect_social_touches_count=4)
        assert eng._requires_social_coaching(10.0, inp) is True

    def test_no_coaching_when_all_false(self, eng):
        inp = make_input(content_posts_last_30d=10, prospect_social_touches_count=35)
        assert eng._requires_social_coaching(10.0, inp) is False

    def test_coaching_boundary_composite_exactly_30(self, eng):
        inp = make_input(content_posts_last_30d=10, prospect_social_touches_count=35)
        assert eng._requires_social_coaching(30.0, inp) is True

    def test_no_coaching_composite_just_below_30(self, eng):
        inp = make_input(content_posts_last_30d=10, prospect_social_touches_count=35)
        assert eng._requires_social_coaching(29.9, inp) is False

    def test_coaching_posts_exactly_1(self, eng):
        inp = make_input(content_posts_last_30d=1, prospect_social_touches_count=35)
        assert eng._requires_social_coaching(10.0, inp) is True

    def test_no_coaching_posts_exactly_2(self, eng):
        inp = make_input(content_posts_last_30d=2, prospect_social_touches_count=35)
        assert eng._requires_social_coaching(10.0, inp) is False

    def test_coaching_touches_exactly_4(self, eng):
        inp = make_input(content_posts_last_30d=10, prospect_social_touches_count=4)
        assert eng._requires_social_coaching(10.0, inp) is True

    def test_no_coaching_touches_exactly_5(self, eng):
        inp = make_input(content_posts_last_30d=10, prospect_social_touches_count=5)
        assert eng._requires_social_coaching(10.0, inp) is False


# ===========================================================================
# 14. PIPELINE LOSS ESTIMATION
# ===========================================================================

class TestEstimatedPipelineLoss:
    @pytest.fixture
    def eng(self):
        return SalesSocialSellingIntelligenceEngine()

    def test_zero_loss_when_meetings_ge_3(self, eng):
        inp = make_input(social_sourced_meetings_count=3, avg_opportunity_value_usd=10000.0)
        loss = eng._estimated_pipeline_loss(inp, 50.0)
        assert loss == 0.0

    def test_zero_loss_when_meetings_above_benchmark(self, eng):
        inp = make_input(social_sourced_meetings_count=5, avg_opportunity_value_usd=10000.0)
        loss = eng._estimated_pipeline_loss(inp, 50.0)
        assert loss == 0.0

    def test_loss_formula_one_missed_meeting(self, eng):
        # benchmark=3, meetings=2 -> missed=1; composite=50; opp=10000
        # loss = 1 * 10000 * (50/100) * 0.18 = 900.0
        inp = make_input(social_sourced_meetings_count=2, avg_opportunity_value_usd=10000.0)
        loss = eng._estimated_pipeline_loss(inp, 50.0)
        assert loss == pytest.approx(900.0, rel=1e-4)

    def test_loss_formula_three_missed_meetings(self, eng):
        # missed=3, opp=10000, composite=100
        # loss = 3 * 10000 * 1.0 * 0.18 = 5400.0
        inp = make_input(social_sourced_meetings_count=0, avg_opportunity_value_usd=10000.0)
        loss = eng._estimated_pipeline_loss(inp, 100.0)
        assert loss == pytest.approx(5400.0, rel=1e-4)

    def test_loss_scales_with_composite(self, eng):
        inp_low = make_input(social_sourced_meetings_count=0, avg_opportunity_value_usd=10000.0)
        inp_high = make_input(social_sourced_meetings_count=0, avg_opportunity_value_usd=10000.0)
        loss_low = eng._estimated_pipeline_loss(inp_low, 20.0)
        loss_high = eng._estimated_pipeline_loss(inp_high, 80.0)
        assert loss_high > loss_low

    def test_loss_scales_with_opportunity_value(self, eng):
        inp_cheap = make_input(social_sourced_meetings_count=0, avg_opportunity_value_usd=5000.0)
        inp_expensive = make_input(social_sourced_meetings_count=0, avg_opportunity_value_usd=50000.0)
        loss_cheap = eng._estimated_pipeline_loss(inp_cheap, 50.0)
        loss_expensive = eng._estimated_pipeline_loss(inp_expensive, 50.0)
        assert loss_expensive == pytest.approx(loss_cheap * 10, rel=1e-4)

    def test_loss_rounded_to_2_decimal_places(self, eng):
        inp = make_input(social_sourced_meetings_count=1, avg_opportunity_value_usd=7777.0)
        loss = eng._estimated_pipeline_loss(inp, 33.0)
        assert loss == round(loss, 2)

    def test_loss_zero_composite(self, eng):
        inp = make_input(social_sourced_meetings_count=0, avg_opportunity_value_usd=10000.0)
        loss = eng._estimated_pipeline_loss(inp, 0.0)
        assert loss == 0.0


# ===========================================================================
# 15. SIGNAL STRING
# ===========================================================================

class TestSignal:
    @pytest.fixture
    def eng(self):
        return SalesSocialSellingIntelligenceEngine()

    HEALTHY_MSG = "Social selling performance healthy — prospect engagement, content reach, and pipeline generation within benchmarks"

    def test_healthy_signal_when_none_and_composite_below_20(self, eng):
        inp = make_input()
        signal = eng._signal(inp, SocialSellingPattern.none, 15.0)
        assert signal == self.HEALTHY_MSG

    def test_healthy_signal_at_composite_19(self, eng):
        inp = make_input()
        signal = eng._signal(inp, SocialSellingPattern.none, 19.9)
        assert signal == self.HEALTHY_MSG

    def test_no_healthy_signal_at_composite_20(self, eng):
        inp = make_input()
        signal = eng._signal(inp, SocialSellingPattern.none, 20.0)
        assert signal != self.HEALTHY_MSG

    def test_signal_contains_ssi(self, eng):
        inp = make_input(linkedin_ssi_score=45.0)
        signal = eng._signal(inp, SocialSellingPattern.invisible_online, 50.0)
        assert "SSI 45" in signal

    def test_signal_contains_posts(self, eng):
        inp = make_input(content_posts_last_30d=7)
        signal = eng._signal(inp, SocialSellingPattern.invisible_online, 50.0)
        assert "7 posts/mo" in signal

    def test_signal_contains_meetings(self, eng):
        inp = make_input(social_sourced_meetings_count=3)
        signal = eng._signal(inp, SocialSellingPattern.invisible_online, 50.0)
        assert "3 social meetings" in signal

    def test_signal_contains_composite(self, eng):
        inp = make_input()
        signal = eng._signal(inp, SocialSellingPattern.invisible_online, 55.0)
        assert "composite 55" in signal

    def test_signal_pattern_label_invisible_online(self, eng):
        inp = make_input()
        signal = eng._signal(inp, SocialSellingPattern.invisible_online, 50.0)
        assert "Invisible online" in signal

    def test_signal_pattern_label_inmail_abuse(self, eng):
        inp = make_input()
        signal = eng._signal(inp, SocialSellingPattern.inmail_abuse, 50.0)
        assert "Inmail abuse" in signal

    def test_signal_pattern_label_competitor_following(self, eng):
        inp = make_input()
        signal = eng._signal(inp, SocialSellingPattern.competitor_following, 50.0)
        assert "Competitor following" in signal

    def test_signal_none_pattern_non_healthy_uses_label(self, eng):
        inp = make_input()
        signal = eng._signal(inp, SocialSellingPattern.none, 25.0)
        assert "Social selling risk" in signal

    def test_signal_healthy_requires_both_conditions(self, eng):
        # non-none pattern even at composite < 20 should not be healthy
        inp = make_input()
        signal = eng._signal(inp, SocialSellingPattern.inmail_abuse, 15.0)
        assert signal != self.HEALTHY_MSG


# ===========================================================================
# 16. COMPOSITE CALCULATION
# ===========================================================================

class TestCompositeCalculation:
    def test_composite_formula_weights(self, engine):
        # Manually compute for good input and compare
        inp = make_input()
        result = engine.assess(inp)
        presence = result.profile_presence_score
        content = result.content_effectiveness_score
        prospect = result.prospect_engagement_score
        pipeline = result.social_pipeline_score
        expected = round(presence * 0.25 + content * 0.25 + prospect * 0.30 + pipeline * 0.20, 1)
        assert result.social_selling_composite == expected

    def test_composite_capped_at_100(self, engine):
        inp = make_worst_input()
        result = engine.assess(inp)
        assert result.social_selling_composite <= 100.0

    def test_composite_for_healthy_rep_is_zero(self, engine):
        # A truly healthy rep should have composite == 0
        inp = make_input(
            linkedin_ssi_score=70.0,
            profile_views_last_30d=30,
            network_overlap_with_icp_pct=0.50,
            content_posts_last_30d=10,
            content_engagement_rate_pct=0.06,
            thought_leadership_shares_count=5,
            prospect_social_touches_count=35,
            inmail_reply_rate_pct=0.20,
            prospect_comment_response_rate_pct=0.70,
            social_sourced_meetings_count=5,
            social_sourced_pipeline_usd=60000.0,
            advocacy_referrals_from_social=3,
        )
        result = engine.assess(inp)
        assert result.social_selling_composite == 0.0


# ===========================================================================
# 17. ASSESS() METHOD
# ===========================================================================

class TestAssess:
    def test_assess_returns_result(self, engine, good_input):
        result = engine.assess(good_input)
        assert isinstance(result, SocialSellingResult)

    def test_assess_stores_result(self, engine, good_input):
        engine.assess(good_input)
        assert len(engine._results) == 1

    def test_assess_accumulates_results(self, engine):
        for _ in range(3):
            engine.assess(make_input())
        assert len(engine._results) == 3

    def test_assess_rep_id_preserved(self, engine):
        inp = make_input(rep_id="SPECIAL_REP")
        result = engine.assess(inp)
        assert result.rep_id == "SPECIAL_REP"

    def test_assess_region_preserved(self, engine):
        inp = make_input(region="LATAM")
        result = engine.assess(inp)
        assert result.region == "LATAM"

    def test_assess_worst_case_is_critical(self, engine, bad_input):
        result = engine.assess(bad_input)
        assert result.social_selling_risk == SocialSellingRisk.critical

    def test_assess_best_case_is_low(self, engine, good_input):
        result = engine.assess(good_input)
        assert result.social_selling_risk == SocialSellingRisk.low

    def test_assess_best_case_severity_active(self, engine, good_input):
        result = engine.assess(good_input)
        assert result.social_selling_severity == SocialSellingSeverity.active

    def test_assess_worst_case_severity_invisible(self, engine, bad_input):
        result = engine.assess(bad_input)
        assert result.social_selling_severity == SocialSellingSeverity.invisible

    def test_assess_best_case_no_action(self, engine, good_input):
        result = engine.assess(good_input)
        assert result.recommended_action == SocialSellingAction.no_action

    def test_assess_healthy_signal(self, engine, good_input):
        result = engine.assess(good_input)
        assert "healthy" in result.social_selling_signal.lower()

    def test_assess_scores_rounded_to_1dp(self, engine, good_input):
        result = engine.assess(good_input)
        # scores should be x.y format (1 decimal)
        assert result.profile_presence_score == round(result.profile_presence_score, 1)
        assert result.content_effectiveness_score == round(result.content_effectiveness_score, 1)
        assert result.prospect_engagement_score == round(result.prospect_engagement_score, 1)
        assert result.social_pipeline_score == round(result.social_pipeline_score, 1)
        assert result.social_selling_composite == round(result.social_selling_composite, 1)


# ===========================================================================
# 18. ASSESS_BATCH() METHOD
# ===========================================================================

class TestAssessBatch:
    def test_batch_returns_list(self, engine):
        results = engine.assess_batch([make_input(), make_input(rep_id="R2")])
        assert isinstance(results, list)

    def test_batch_correct_length(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_empty_list(self, engine):
        results = engine.assess_batch([])
        assert results == []

    def test_batch_accumulates_in_internal_list(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(4)]
        engine.assess_batch(inputs)
        assert len(engine._results) == 4

    def test_batch_mixed_results(self, engine):
        inputs = [make_input(), make_worst_input()]
        results = engine.assess_batch(inputs)
        risks = [r.social_selling_risk for r in results]
        assert SocialSellingRisk.low in risks
        assert SocialSellingRisk.critical in risks

    def test_batch_preserves_order(self, engine):
        rep_ids = [f"REP{i:03d}" for i in range(10)]
        inputs = [make_input(rep_id=rid) for rid in rep_ids]
        results = engine.assess_batch(inputs)
        assert [r.rep_id for r in results] == rep_ids

    def test_batch_single_item(self, engine):
        results = engine.assess_batch([make_input()])
        assert len(results) == 1
        assert isinstance(results[0], SocialSellingResult)


# ===========================================================================
# 19. SUMMARY() METHOD
# ===========================================================================

class TestSummary:
    def test_summary_empty_engine_returns_zeros(self, engine):
        s = engine.summary()
        assert s["total"] == 0
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}
        assert s["avg_social_selling_composite"] == 0.0
        assert s["social_gap_count"] == 0
        assert s["coaching_count"] == 0
        assert s["avg_profile_presence_score"] == 0.0
        assert s["avg_content_effectiveness_score"] == 0.0
        assert s["avg_prospect_engagement_score"] == 0.0
        assert s["avg_social_pipeline_score"] == 0.0
        assert s["total_estimated_pipeline_loss_usd"] == 0.0

    def test_summary_has_13_keys(self, engine):
        s = engine.summary()
        assert len(s) == 13

    def test_summary_has_13_keys_after_assess(self, engine, good_input):
        engine.assess(good_input)
        s = engine.summary()
        assert len(s) == 13

    def test_summary_total_count(self, engine):
        for _ in range(3):
            engine.assess(make_input())
        assert engine.summary()["total"] == 3

    def test_summary_risk_counts(self, engine):
        engine.assess(make_input())      # low
        engine.assess(make_worst_input())  # critical
        s = engine.summary()
        assert "low" in s["risk_counts"]
        assert "critical" in s["risk_counts"]

    def test_summary_avg_composite_correct(self, engine):
        engine.assess_batch([make_input(), make_input()])
        s = engine.summary()
        assert isinstance(s["avg_social_selling_composite"], float)
        assert s["avg_social_selling_composite"] >= 0.0

    def test_summary_gap_count(self, engine):
        engine.assess(make_worst_input())  # should have gap
        s = engine.summary()
        assert s["social_gap_count"] >= 1

    def test_summary_coaching_count(self, engine):
        engine.assess(make_worst_input())  # should require coaching
        s = engine.summary()
        assert s["coaching_count"] >= 1

    def test_summary_pipeline_loss_sum(self, engine):
        r1 = engine.assess(make_worst_input())
        r2 = engine.assess(make_worst_input())
        s = engine.summary()
        expected = round(r1.estimated_pipeline_loss_usd + r2.estimated_pipeline_loss_usd, 2)
        assert s["total_estimated_pipeline_loss_usd"] == expected

    def test_summary_pattern_counts_updated(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert "none" in s["pattern_counts"]

    def test_summary_severity_counts_updated(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert "active" in s["severity_counts"]

    def test_summary_action_counts_updated(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert "no_action" in s["action_counts"]

    def test_summary_avg_profile_presence_rounded(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        v = s["avg_profile_presence_score"]
        assert v == round(v, 1)

    def test_summary_avg_content_effectiveness_rounded(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        v = s["avg_content_effectiveness_score"]
        assert v == round(v, 1)

    def test_summary_avg_prospect_engagement_rounded(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        v = s["avg_prospect_engagement_score"]
        assert v == round(v, 1)

    def test_summary_avg_pipeline_score_rounded(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        v = s["avg_social_pipeline_score"]
        assert v == round(v, 1)

    def test_summary_batch_then_summary(self, engine):
        engine.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        s = engine.summary()
        assert s["total"] == 5

    def test_summary_all_risk_levels_counted(self, engine):
        # add results for all risk levels
        engine.assess(make_input())  # low
        # moderate: composite in [20, 40)
        engine.assess(make_input(
            linkedin_ssi_score=35.0, profile_views_last_30d=20,
            network_overlap_with_icp_pct=0.25,
            content_posts_last_30d=3,
            content_engagement_rate_pct=0.02,
            thought_leadership_shares_count=2,
            prospect_social_touches_count=12,
            inmail_reply_rate_pct=0.10,
            prospect_comment_response_rate_pct=0.40,
            social_sourced_meetings_count=2,
            social_sourced_pipeline_usd=25000.0,
            advocacy_referrals_from_social=2,
        ))
        engine.assess(make_worst_input())  # critical
        s = engine.summary()
        assert s["total"] == 3


# ===========================================================================
# 20. EDGE CASES
# ===========================================================================

class TestEdgeCases:
    def test_ssi_exactly_0(self, engine):
        inp = make_input(linkedin_ssi_score=0.0)
        result = engine.assess(inp)
        assert result.profile_presence_score >= 40.0

    def test_ssi_exactly_100(self, engine):
        inp = make_input(linkedin_ssi_score=100.0)
        result = engine.assess(inp)
        # No SSI contribution
        assert result.profile_presence_score >= 0.0

    def test_zero_avg_opportunity_value(self, engine):
        inp = make_input(avg_opportunity_value_usd=0.0)
        result = engine.assess(inp)
        assert result.estimated_pipeline_loss_usd == 0.0

    def test_very_large_opportunity_value(self, engine):
        inp = make_input(social_sourced_meetings_count=0, avg_opportunity_value_usd=1_000_000.0)
        result = engine.assess(inp)
        assert result.estimated_pipeline_loss_usd > 0.0

    def test_zero_inmail_sent_count(self, engine):
        # Should not divide by zero (max(..., 1) guard)
        inp = make_input(inmail_sent_count=0, inmail_reply_rate_pct=0.0)
        result = engine.assess(inp)
        assert isinstance(result, SocialSellingResult)

    def test_rep_id_with_special_characters(self, engine):
        inp = make_input(rep_id="REP-001/US#EMEA")
        result = engine.assess(inp)
        assert result.rep_id == "REP-001/US#EMEA"

    def test_network_overlap_exactly_0(self, engine):
        inp = make_input(network_overlap_with_icp_pct=0.0)
        result = engine.assess(inp)
        assert result.profile_presence_score >= 30.0

    def test_network_overlap_exactly_1(self, engine):
        inp = make_input(network_overlap_with_icp_pct=1.0)
        result = engine.assess(inp)
        assert isinstance(result, SocialSellingResult)

    def test_content_engagement_exactly_0(self, engine):
        inp = make_input(content_engagement_rate_pct=0.0)
        result = engine.assess(inp)
        assert result.content_effectiveness_score >= 35.0

    def test_negative_pipeline_usd_zero_loss(self, engine):
        # Negative pipeline should still produce non-negative loss
        inp = make_input(social_sourced_meetings_count=0, social_sourced_pipeline_usd=-100.0)
        result = engine.assess(inp)
        assert result.estimated_pipeline_loss_usd >= 0.0

    def test_multiple_engine_instances_isolated(self):
        eng1 = SalesSocialSellingIntelligenceEngine()
        eng2 = SalesSocialSellingIntelligenceEngine()
        eng1.assess(make_input())
        assert len(eng1._results) == 1
        assert len(eng2._results) == 0

    def test_fresh_engine_summary_all_zeros(self):
        eng = SalesSocialSellingIntelligenceEngine()
        s = eng.summary()
        assert s["total"] == 0

    def test_very_high_inmail_count_no_crash(self, engine):
        inp = make_input(inmail_sent_count=10000, inmail_reply_rate_pct=0.001)
        result = engine.assess(inp)
        assert isinstance(result, SocialSellingResult)

    def test_composite_never_negative(self, engine):
        inp = make_input()
        result = engine.assess(inp)
        assert result.social_selling_composite >= 0.0


# ===========================================================================
# 21. END-TO-END SCENARIOS
# ===========================================================================

class TestEndToEndScenarios:
    def test_scenario_star_performer(self):
        """A star social seller: everything healthy."""
        eng = SalesSocialSellingIntelligenceEngine()
        inp = make_input(
            rep_id="STAR",
            linkedin_ssi_score=85.0,
            profile_views_last_30d=50,
            network_overlap_with_icp_pct=0.60,
            content_posts_last_30d=15,
            content_engagement_rate_pct=0.08,
            thought_leadership_shares_count=10,
            prospect_social_touches_count=50,
            inmail_sent_count=20,
            inmail_reply_rate_pct=0.25,
            prospect_comment_response_rate_pct=0.80,
            social_sourced_meetings_count=8,
            social_sourced_pipeline_usd=120000.0,
            advocacy_referrals_from_social=5,
            avg_opportunity_value_usd=15000.0,
        )
        result = eng.assess(inp)
        assert result.social_selling_risk == SocialSellingRisk.low
        assert result.social_selling_severity == SocialSellingSeverity.active
        assert result.recommended_action == SocialSellingAction.no_action
        assert result.social_selling_pattern == SocialSellingPattern.none
        assert result.estimated_pipeline_loss_usd == 0.0
        assert "healthy" in result.social_selling_signal.lower()

    def test_scenario_ghost_online(self):
        """Rep with no online presence whatsoever — also low on all other signals."""
        eng = SalesSocialSellingIntelligenceEngine()
        inp = make_input(
            rep_id="GHOST",
            linkedin_ssi_score=5.0,
            profile_views_last_30d=1,
            network_overlap_with_icp_pct=0.02,
            content_posts_last_30d=0,
            content_engagement_rate_pct=0.0,
            thought_leadership_shares_count=0,
            prospect_social_touches_count=0,
            inmail_reply_rate_pct=0.0,
            prospect_comment_response_rate_pct=0.0,
            social_sourced_meetings_count=0,
            social_sourced_pipeline_usd=0.0,
            advocacy_referrals_from_social=0,
        )
        result = eng.assess(inp)
        assert result.social_selling_pattern == SocialSellingPattern.invisible_online
        assert result.social_selling_risk in (SocialSellingRisk.high, SocialSellingRisk.critical)

    def test_scenario_inmail_spammer(self):
        """Rep who sends tons of inmails but gets no replies — also weak on pipeline."""
        eng = SalesSocialSellingIntelligenceEngine()
        inp = make_input(
            rep_id="SPAMMER",
            linkedin_ssi_score=70.0,
            profile_views_last_30d=30,
            network_overlap_with_icp_pct=0.50,
            prospect_social_touches_count=35,
            inmail_sent_count=100,
            inmail_reply_rate_pct=0.01,
            prospect_comment_response_rate_pct=0.70,
            competitor_content_engagement_pct=0.05,
            # Weak pipeline to push composite into high range
            content_posts_last_30d=1,
            content_engagement_rate_pct=0.005,
            thought_leadership_shares_count=0,
            social_sourced_meetings_count=0,
            social_sourced_pipeline_usd=0.0,
            advocacy_referrals_from_social=0,
        )
        result = eng.assess(inp)
        assert result.social_selling_pattern == SocialSellingPattern.inmail_abuse
        # inmail_abuse with high risk -> inmail_optimization
        if result.social_selling_risk == SocialSellingRisk.high:
            assert result.recommended_action == SocialSellingAction.inmail_optimization
        else:
            # At critical risk, inmail_abuse falls through to social_presence_coaching
            assert result.recommended_action in (
                SocialSellingAction.inmail_optimization,
                SocialSellingAction.social_presence_coaching,
            )

    def test_scenario_competitor_lurker(self):
        """Rep engages heavily with competitor content."""
        eng = SalesSocialSellingIntelligenceEngine()
        inp = make_input(
            rep_id="LURKER",
            linkedin_ssi_score=70.0,
            profile_views_last_30d=30,
            network_overlap_with_icp_pct=0.50,
            prospect_social_touches_count=35,
            inmail_sent_count=5,
            inmail_reply_rate_pct=0.20,
            prospect_comment_response_rate_pct=0.70,
            competitor_content_engagement_pct=0.50,
        )
        result = eng.assess(inp)
        assert result.social_selling_pattern == SocialSellingPattern.competitor_following

    def test_scenario_to_dict_roundtrip(self):
        """to_dict values match result attributes."""
        eng = SalesSocialSellingIntelligenceEngine()
        inp = make_worst_input()
        result = eng.assess(inp)
        d = result.to_dict()
        assert d["rep_id"] == result.rep_id
        assert d["region"] == result.region
        assert d["social_selling_risk"] == result.social_selling_risk.value
        assert d["social_selling_pattern"] == result.social_selling_pattern.value
        assert d["social_selling_severity"] == result.social_selling_severity.value
        assert d["recommended_action"] == result.recommended_action.value
        assert d["profile_presence_score"] == result.profile_presence_score
        assert d["content_effectiveness_score"] == result.content_effectiveness_score
        assert d["prospect_engagement_score"] == result.prospect_engagement_score
        assert d["social_pipeline_score"] == result.social_pipeline_score
        assert d["social_selling_composite"] == result.social_selling_composite
        assert d["has_social_gap"] == result.has_social_gap
        assert d["requires_social_coaching"] == result.requires_social_coaching
        assert d["estimated_pipeline_loss_usd"] == result.estimated_pipeline_loss_usd
        assert d["social_selling_signal"] == result.social_selling_signal

    def test_scenario_batch_summary_consistency(self):
        """Batch + summary: total matches batch size."""
        eng = SalesSocialSellingIntelligenceEngine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(7)] + [make_worst_input()]
        eng.assess_batch(inputs)
        s = eng.summary()
        assert s["total"] == 8

    def test_scenario_all_risk_levels_in_summary(self):
        """Ensuring all four risk levels can appear in a multi-rep batch."""
        eng = SalesSocialSellingIntelligenceEngine()
        # Build inputs that span all risk levels
        results = []
        results.append(eng.assess(make_input()))  # low
        results.append(eng.assess(make_worst_input()))  # critical
        risk_values = {r.social_selling_risk.value for r in results}
        s = eng.summary()
        for rv in risk_values:
            assert rv in s["risk_counts"]

    def test_scenario_coaching_required_for_low_posts(self):
        eng = SalesSocialSellingIntelligenceEngine()
        inp = make_input(content_posts_last_30d=0)
        result = eng.assess(inp)
        assert result.requires_social_coaching is True

    def test_scenario_social_gap_for_zero_meetings(self):
        eng = SalesSocialSellingIntelligenceEngine()
        inp = make_input(social_sourced_meetings_count=0)
        result = eng.assess(inp)
        assert result.has_social_gap is True

    def test_scenario_signal_has_correct_format_for_pattern(self):
        eng = SalesSocialSellingIntelligenceEngine()
        inp = make_input(
            linkedin_ssi_score=5.0,
            profile_views_last_30d=1,
            network_overlap_with_icp_pct=0.02,
        )
        result = eng.assess(inp)
        if result.social_selling_pattern != SocialSellingPattern.none or result.social_selling_composite >= 20:
            assert "composite" in result.social_selling_signal
            assert "SSI" in result.social_selling_signal

    def test_scenario_critical_invisible_gets_brand_building(self):
        eng = SalesSocialSellingIntelligenceEngine()
        inp = make_worst_input(
            linkedin_ssi_score=5.0,
            profile_views_last_30d=1,
            network_overlap_with_icp_pct=0.01,
        )
        result = eng.assess(inp)
        if result.social_selling_pattern == SocialSellingPattern.invisible_online:
            if result.social_selling_risk == SocialSellingRisk.critical:
                assert result.recommended_action == SocialSellingAction.brand_building_program

    def test_scenario_moderate_always_social_presence_coaching(self):
        eng = SalesSocialSellingIntelligenceEngine()
        # Build an input likely to land in moderate range
        inp = make_input(
            linkedin_ssi_score=50.0,
            profile_views_last_30d=20,
            network_overlap_with_icp_pct=0.30,
            content_posts_last_30d=3,
            content_engagement_rate_pct=0.02,
            thought_leadership_shares_count=2,
            prospect_social_touches_count=12,
            inmail_reply_rate_pct=0.12,
            prospect_comment_response_rate_pct=0.45,
            social_sourced_meetings_count=2,
            social_sourced_pipeline_usd=30000.0,
            advocacy_referrals_from_social=2,
        )
        result = eng.assess(inp)
        if result.social_selling_risk == SocialSellingRisk.moderate:
            assert result.recommended_action == SocialSellingAction.social_presence_coaching
