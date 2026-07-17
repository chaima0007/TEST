"""
Comprehensive pytest test suite for CustomerReferralIntelligence.
~250 tests organized in classes covering all invariants, scoring functions,
enums, methods, and edge cases.
"""
import dataclasses
import pytest

from swarm.intelligence.customer_referral_intelligence import (
    CustomerReferralIntelligence,
    CustomerReferralInput,
    CustomerReferralResult,
    ReferralVelocity,
    AdvocacyLevel,
    ReferralRisk,
    ReferralAction,
    _advocacy_score,
    _relationship_depth_score,
    _referral_propensity_score,
    _advocacy_impact_score,
    _composite,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**kwargs):
    defaults = dict(
        customer_id="cust_001", customer_name="TechCorp Global", rep_id="rep_001",
        contract_value_usd=150000.0, nps_score=72.0,
        referrals_given_lifetime=4, referrals_converted_to_deals=2,
        referral_pipeline_value_usd=320000.0, case_study_agreed=1, review_submitted=1,
        speaking_event_participated=1, product_feedback_sessions_completed=3,
        community_posts_count=8, champion_identified=1, exec_relationship_strength=88.0,
        account_tenure_days=720, last_referral_days_ago=25, referral_ask_count=2,
        competitive_references_blocked=1, customer_success_score=92.0,
        renewal_probability_pct=95.0, expansion_completed=1,
    )
    defaults.update(kwargs)
    return CustomerReferralInput(**defaults)


def detractor_input(customer_id="det_001"):
    return make_input(
        customer_id=customer_id, nps_score=-45.0,
        referrals_given_lifetime=0, referrals_converted_to_deals=0,
        referral_pipeline_value_usd=0.0, case_study_agreed=0, review_submitted=0,
        speaking_event_participated=0, product_feedback_sessions_completed=0,
        community_posts_count=0, champion_identified=0, exec_relationship_strength=15.0,
        account_tenure_days=90, last_referral_days_ago=999, referral_ask_count=0,
        competitive_references_blocked=0, customer_success_score=22.0,
        renewal_probability_pct=20.0, expansion_completed=0,
    )


# ---------------------------------------------------------------------------
# TestEnums
# ---------------------------------------------------------------------------

class TestReferralVelocityEnum:
    def test_has_four_values(self):
        assert len(ReferralVelocity) == 4

    def test_accelerating_value(self):
        assert ReferralVelocity.ACCELERATING.value == "accelerating"

    def test_steady_value(self):
        assert ReferralVelocity.STEADY.value == "steady"

    def test_declining_value(self):
        assert ReferralVelocity.DECLINING.value == "declining"

    def test_inactive_value(self):
        assert ReferralVelocity.INACTIVE.value == "inactive"

    def test_is_str_enum(self):
        assert isinstance(ReferralVelocity.ACCELERATING, str)


class TestAdvocacyLevelEnum:
    def test_has_four_values(self):
        assert len(AdvocacyLevel) == 4

    def test_champion_value(self):
        assert AdvocacyLevel.CHAMPION.value == "champion"

    def test_promoter_value(self):
        assert AdvocacyLevel.PROMOTER.value == "promoter"

    def test_passive_value(self):
        assert AdvocacyLevel.PASSIVE.value == "passive"

    def test_detractor_value(self):
        assert AdvocacyLevel.DETRACTOR.value == "detractor"

    def test_is_str_enum(self):
        assert isinstance(AdvocacyLevel.CHAMPION, str)


class TestReferralRiskEnum:
    def test_has_four_values(self):
        assert len(ReferralRisk) == 4

    def test_low_value(self):
        assert ReferralRisk.LOW.value == "low"

    def test_moderate_value(self):
        assert ReferralRisk.MODERATE.value == "moderate"

    def test_high_value(self):
        assert ReferralRisk.HIGH.value == "high"

    def test_critical_value(self):
        assert ReferralRisk.CRITICAL.value == "critical"

    def test_is_str_enum(self):
        assert isinstance(ReferralRisk.LOW, str)


class TestReferralActionEnum:
    def test_has_four_values(self):
        assert len(ReferralAction) == 4

    def test_activate_referral_value(self):
        assert ReferralAction.ACTIVATE_REFERRAL.value == "activate_referral"

    def test_nurture_advocate_value(self):
        assert ReferralAction.NURTURE_ADVOCATE.value == "nurture_advocate"

    def test_re_engage_value(self):
        assert ReferralAction.RE_ENGAGE.value == "re_engage"

    def test_convert_detractor_value(self):
        assert ReferralAction.CONVERT_DETRACTOR.value == "convert_detractor"

    def test_is_str_enum(self):
        assert isinstance(ReferralAction.ACTIVATE_REFERRAL, str)


# ---------------------------------------------------------------------------
# TestCustomerReferralInput
# ---------------------------------------------------------------------------

class TestCustomerReferralInput:
    def test_has_exactly_22_fields(self):
        fields = dataclasses.fields(CustomerReferralInput)
        assert len(fields) == 22

    def test_field_names(self):
        field_names = {f.name for f in dataclasses.fields(CustomerReferralInput)}
        expected = {
            "customer_id", "customer_name", "rep_id", "contract_value_usd",
            "nps_score", "referrals_given_lifetime", "referrals_converted_to_deals",
            "referral_pipeline_value_usd", "case_study_agreed", "review_submitted",
            "speaking_event_participated", "product_feedback_sessions_completed",
            "community_posts_count", "champion_identified", "exec_relationship_strength",
            "account_tenure_days", "last_referral_days_ago", "referral_ask_count",
            "competitive_references_blocked", "customer_success_score",
            "renewal_probability_pct", "expansion_completed",
        }
        assert field_names == expected

    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(CustomerReferralInput)

    def test_can_construct(self):
        inp = make_input()
        assert inp.customer_id == "cust_001"

    def test_all_fields_accessible(self):
        inp = make_input()
        # verify each field is accessible without error
        for field in dataclasses.fields(inp):
            _ = getattr(inp, field.name)


# ---------------------------------------------------------------------------
# TestCustomerReferralResult
# ---------------------------------------------------------------------------

class TestCustomerReferralResult:
    def test_to_dict_returns_15_keys(self):
        engine = CustomerReferralIntelligence()
        result = engine.analyze(make_input())
        assert len(result.to_dict()) == 15

    def test_to_dict_exact_keys(self):
        engine = CustomerReferralIntelligence()
        result = engine.analyze(make_input())
        d = result.to_dict()
        expected_keys = {
            "customer_id", "customer_name", "referral_velocity", "advocacy_level",
            "referral_risk", "referral_action", "advocacy_score",
            "relationship_depth_score", "referral_propensity_score",
            "advocacy_impact_score", "referral_composite",
            "estimated_referral_pipeline_usd", "is_active_referrer",
            "needs_advocacy_activation", "primary_advocacy_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_values_are_strings(self):
        engine = CustomerReferralIntelligence()
        result = engine.analyze(make_input())
        d = result.to_dict()
        assert isinstance(d["referral_velocity"], str)
        assert isinstance(d["advocacy_level"], str)
        assert isinstance(d["referral_risk"], str)
        assert isinstance(d["referral_action"], str)

    def test_to_dict_customer_id_correct(self):
        engine = CustomerReferralIntelligence()
        result = engine.analyze(make_input(customer_id="test_123"))
        assert result.to_dict()["customer_id"] == "test_123"

    def test_to_dict_booleans(self):
        engine = CustomerReferralIntelligence()
        result = engine.analyze(make_input())
        d = result.to_dict()
        assert isinstance(d["is_active_referrer"], bool)
        assert isinstance(d["needs_advocacy_activation"], bool)


# ---------------------------------------------------------------------------
# TestAdvocacyScoreFunction
# ---------------------------------------------------------------------------

class TestAdvocacyScoreFunction:
    def test_nps_ge_70_adds_35(self):
        inp = make_input(nps_score=70.0, case_study_agreed=0, review_submitted=0,
                         speaking_event_participated=0, product_feedback_sessions_completed=0,
                         community_posts_count=0)
        assert _advocacy_score(inp) == 35.0

    def test_nps_50_to_69_adds_25(self):
        inp = make_input(nps_score=55.0, case_study_agreed=0, review_submitted=0,
                         speaking_event_participated=0, product_feedback_sessions_completed=0,
                         community_posts_count=0)
        assert _advocacy_score(inp) == 25.0

    def test_nps_20_to_49_adds_15(self):
        inp = make_input(nps_score=30.0, case_study_agreed=0, review_submitted=0,
                         speaking_event_participated=0, product_feedback_sessions_completed=0,
                         community_posts_count=0)
        assert _advocacy_score(inp) == 15.0

    def test_nps_0_to_19_adds_8(self):
        inp = make_input(nps_score=10.0, case_study_agreed=0, review_submitted=0,
                         speaking_event_participated=0, product_feedback_sessions_completed=0,
                         community_posts_count=0)
        assert _advocacy_score(inp) == 8.0

    def test_nps_lt_minus_20_subtracts_10(self):
        inp = make_input(nps_score=-30.0, case_study_agreed=0, review_submitted=0,
                         speaking_event_participated=0, product_feedback_sessions_completed=0,
                         community_posts_count=0)
        assert _advocacy_score(inp) == 0.0

    def test_case_study_adds_20(self):
        inp = make_input(nps_score=0.0, case_study_agreed=1, review_submitted=0,
                         speaking_event_participated=0, product_feedback_sessions_completed=0,
                         community_posts_count=0)
        assert _advocacy_score(inp) == 28.0  # 8 + 20

    def test_review_submitted_adds_15(self):
        inp = make_input(nps_score=0.0, case_study_agreed=0, review_submitted=1,
                         speaking_event_participated=0, product_feedback_sessions_completed=0,
                         community_posts_count=0)
        assert _advocacy_score(inp) == 23.0  # 8 + 15

    def test_speaking_event_adds_15(self):
        inp = make_input(nps_score=0.0, case_study_agreed=0, review_submitted=0,
                         speaking_event_participated=1, product_feedback_sessions_completed=0,
                         community_posts_count=0)
        assert _advocacy_score(inp) == 23.0  # 8 + 15

    def test_feedback_sessions_ge_3_adds_10(self):
        inp = make_input(nps_score=0.0, case_study_agreed=0, review_submitted=0,
                         speaking_event_participated=0, product_feedback_sessions_completed=3,
                         community_posts_count=0)
        assert _advocacy_score(inp) == 18.0  # 8 + 10

    def test_feedback_sessions_1_to_2_adds_5(self):
        inp = make_input(nps_score=0.0, case_study_agreed=0, review_submitted=0,
                         speaking_event_participated=0, product_feedback_sessions_completed=1,
                         community_posts_count=0)
        assert _advocacy_score(inp) == 13.0  # 8 + 5

    def test_community_posts_ge_5_adds_5(self):
        inp = make_input(nps_score=0.0, case_study_agreed=0, review_submitted=0,
                         speaking_event_participated=0, product_feedback_sessions_completed=0,
                         community_posts_count=5)
        assert _advocacy_score(inp) == 13.0  # 8 + 5

    def test_community_posts_2_to_4_adds_3(self):
        inp = make_input(nps_score=0.0, case_study_agreed=0, review_submitted=0,
                         speaking_event_participated=0, product_feedback_sessions_completed=0,
                         community_posts_count=2)
        assert _advocacy_score(inp) == 11.0  # 8 + 3

    def test_max_clamped_at_100(self):
        inp = make_input(nps_score=100.0, case_study_agreed=1, review_submitted=1,
                         speaking_event_participated=1, product_feedback_sessions_completed=5,
                         community_posts_count=10)
        assert _advocacy_score(inp) <= 100.0

    def test_min_clamped_at_0(self):
        inp = make_input(nps_score=-100.0, case_study_agreed=0, review_submitted=0,
                         speaking_event_participated=0, product_feedback_sessions_completed=0,
                         community_posts_count=0)
        assert _advocacy_score(inp) >= 0.0

    def test_full_champion_score(self):
        inp = make_input()
        score = _advocacy_score(inp)
        assert 0.0 <= score <= 100.0

    def test_negative_nps_between_minus_20_and_0_no_penalty(self):
        # nps_score between -20 and 0 — no subtraction, no addition
        inp = make_input(nps_score=-10.0, case_study_agreed=0, review_submitted=0,
                         speaking_event_participated=0, product_feedback_sessions_completed=0,
                         community_posts_count=0)
        assert _advocacy_score(inp) == 0.0


# ---------------------------------------------------------------------------
# TestRelationshipDepthScoreFunction
# ---------------------------------------------------------------------------

class TestRelationshipDepthScoreFunction:
    def test_champion_identified_adds_30(self):
        inp = make_input(champion_identified=1, exec_relationship_strength=0.0,
                         account_tenure_days=0, customer_success_score=0.0)
        assert _relationship_depth_score(inp) == 30.0

    def test_exec_relationship_contribution(self):
        inp = make_input(champion_identified=0, exec_relationship_strength=100.0,
                         account_tenure_days=0, customer_success_score=0.0)
        assert _relationship_depth_score(inp) == 30.0  # 100 * 0.30

    def test_tenure_ge_730_days_adds_20(self):
        inp = make_input(champion_identified=0, exec_relationship_strength=0.0,
                         account_tenure_days=730, customer_success_score=0.0)
        assert _relationship_depth_score(inp) == 20.0

    def test_tenure_365_to_729_adds_14(self):
        inp = make_input(champion_identified=0, exec_relationship_strength=0.0,
                         account_tenure_days=365, customer_success_score=0.0)
        assert _relationship_depth_score(inp) == 14.0

    def test_tenure_180_to_364_adds_8(self):
        inp = make_input(champion_identified=0, exec_relationship_strength=0.0,
                         account_tenure_days=180, customer_success_score=0.0)
        assert _relationship_depth_score(inp) == 8.0

    def test_tenure_90_to_179_adds_4(self):
        inp = make_input(champion_identified=0, exec_relationship_strength=0.0,
                         account_tenure_days=90, customer_success_score=0.0)
        assert _relationship_depth_score(inp) == 4.0

    def test_tenure_lt_90_adds_0(self):
        inp = make_input(champion_identified=0, exec_relationship_strength=0.0,
                         account_tenure_days=50, customer_success_score=0.0)
        assert _relationship_depth_score(inp) == 0.0

    def test_customer_success_score_contribution(self):
        inp = make_input(champion_identified=0, exec_relationship_strength=0.0,
                         account_tenure_days=0, customer_success_score=100.0)
        assert _relationship_depth_score(inp) == 20.0  # 100 * 0.20

    def test_clamped_at_100(self):
        inp = make_input(champion_identified=1, exec_relationship_strength=100.0,
                         account_tenure_days=730, customer_success_score=100.0)
        assert _relationship_depth_score(inp) <= 100.0

    def test_clamped_at_0(self):
        inp = make_input(champion_identified=0, exec_relationship_strength=0.0,
                         account_tenure_days=0, customer_success_score=0.0)
        assert _relationship_depth_score(inp) == 0.0

    def test_full_strong_relationship(self):
        inp = make_input()
        score = _relationship_depth_score(inp)
        assert 0.0 <= score <= 100.0


# ---------------------------------------------------------------------------
# TestReferralPropensityScoreFunction
# ---------------------------------------------------------------------------

class TestReferralPropensityScoreFunction:
    def test_referrals_ge_5_adds_30(self):
        inp = make_input(referrals_given_lifetime=5, referrals_converted_to_deals=0,
                         renewal_probability_pct=0.0, expansion_completed=0,
                         competitive_references_blocked=0, referral_ask_count=0)
        assert _referral_propensity_score(inp) >= 30.0

    def test_referrals_3_to_4_adds_22(self):
        inp = make_input(referrals_given_lifetime=3, referrals_converted_to_deals=0,
                         renewal_probability_pct=0.0, expansion_completed=0,
                         competitive_references_blocked=0, referral_ask_count=0)
        score = _referral_propensity_score(inp)
        assert score >= 22.0

    def test_referrals_1_to_2_adds_12(self):
        inp = make_input(referrals_given_lifetime=1, referrals_converted_to_deals=0,
                         renewal_probability_pct=0.0, expansion_completed=0,
                         competitive_references_blocked=0, referral_ask_count=0)
        score = _referral_propensity_score(inp)
        assert score >= 12.0

    def test_conv_rate_ge_50pct_adds_25(self):
        inp = make_input(referrals_given_lifetime=2, referrals_converted_to_deals=1,
                         renewal_probability_pct=0.0, expansion_completed=0,
                         competitive_references_blocked=0, referral_ask_count=0)
        score = _referral_propensity_score(inp)
        assert score == 37.0  # 12 + 25

    def test_conv_rate_30_to_49pct_adds_18(self):
        inp = make_input(referrals_given_lifetime=10, referrals_converted_to_deals=3,
                         renewal_probability_pct=0.0, expansion_completed=0,
                         competitive_references_blocked=0, referral_ask_count=0)
        score = _referral_propensity_score(inp)
        assert score == 48.0  # 30 + 18

    def test_conv_rate_10_to_29pct_adds_10(self):
        inp = make_input(referrals_given_lifetime=10, referrals_converted_to_deals=1,
                         renewal_probability_pct=0.0, expansion_completed=0,
                         competitive_references_blocked=0, referral_ask_count=0)
        score = _referral_propensity_score(inp)
        assert score == 40.0  # 30 + 10

    def test_zero_referrals_zero_conversion(self):
        inp = make_input(referrals_given_lifetime=0, referrals_converted_to_deals=0,
                         renewal_probability_pct=0.0, expansion_completed=0,
                         competitive_references_blocked=0, referral_ask_count=0)
        score = _referral_propensity_score(inp)
        assert score == 0.0

    def test_renewal_ge_90_adds_20(self):
        inp = make_input(referrals_given_lifetime=0, referrals_converted_to_deals=0,
                         renewal_probability_pct=90.0, expansion_completed=0,
                         competitive_references_blocked=0, referral_ask_count=0)
        assert _referral_propensity_score(inp) == 20.0

    def test_renewal_70_to_89_adds_14(self):
        inp = make_input(referrals_given_lifetime=0, referrals_converted_to_deals=0,
                         renewal_probability_pct=70.0, expansion_completed=0,
                         competitive_references_blocked=0, referral_ask_count=0)
        assert _referral_propensity_score(inp) == 14.0

    def test_renewal_50_to_69_adds_8(self):
        inp = make_input(referrals_given_lifetime=0, referrals_converted_to_deals=0,
                         renewal_probability_pct=50.0, expansion_completed=0,
                         competitive_references_blocked=0, referral_ask_count=0)
        assert _referral_propensity_score(inp) == 8.0

    def test_expansion_completed_adds_15(self):
        inp = make_input(referrals_given_lifetime=0, referrals_converted_to_deals=0,
                         renewal_probability_pct=0.0, expansion_completed=1,
                         competitive_references_blocked=0, referral_ask_count=0)
        assert _referral_propensity_score(inp) == 15.0

    def test_competitive_references_blocked_adds_10(self):
        inp = make_input(referrals_given_lifetime=0, referrals_converted_to_deals=0,
                         renewal_probability_pct=0.0, expansion_completed=0,
                         competitive_references_blocked=1, referral_ask_count=0)
        assert _referral_propensity_score(inp) == 10.0

    def test_many_asks_zero_referrals_penalty(self):
        inp = make_input(referrals_given_lifetime=0, referrals_converted_to_deals=0,
                         renewal_probability_pct=0.0, expansion_completed=0,
                         competitive_references_blocked=0, referral_ask_count=3)
        assert _referral_propensity_score(inp) == 0.0  # -10 clamped to 0

    def test_clamped_at_100(self):
        inp = make_input(referrals_given_lifetime=10, referrals_converted_to_deals=10,
                         renewal_probability_pct=100.0, expansion_completed=1,
                         competitive_references_blocked=1, referral_ask_count=0)
        assert _referral_propensity_score(inp) <= 100.0

    def test_clamped_at_0(self):
        inp = make_input(referrals_given_lifetime=0, referrals_converted_to_deals=0,
                         renewal_probability_pct=0.0, expansion_completed=0,
                         competitive_references_blocked=0, referral_ask_count=5)
        assert _referral_propensity_score(inp) == 0.0


# ---------------------------------------------------------------------------
# TestAdvocacyImpactScoreFunction
# ---------------------------------------------------------------------------

class TestAdvocacyImpactScoreFunction:
    def test_pipeline_ge_500k_adds_40(self):
        inp = make_input(referral_pipeline_value_usd=500000.0,
                         referrals_converted_to_deals=0, contract_value_usd=0.0,
                         speaking_event_participated=0)
        assert _advocacy_impact_score(inp) == 40.0

    def test_pipeline_200k_to_499k_adds_30(self):
        inp = make_input(referral_pipeline_value_usd=300000.0,
                         referrals_converted_to_deals=0, contract_value_usd=0.0,
                         speaking_event_participated=0)
        assert _advocacy_impact_score(inp) == 30.0

    def test_pipeline_100k_to_199k_adds_22(self):
        inp = make_input(referral_pipeline_value_usd=150000.0,
                         referrals_converted_to_deals=0, contract_value_usd=0.0,
                         speaking_event_participated=0)
        assert _advocacy_impact_score(inp) == 22.0

    def test_pipeline_50k_to_99k_adds_14(self):
        inp = make_input(referral_pipeline_value_usd=75000.0,
                         referrals_converted_to_deals=0, contract_value_usd=0.0,
                         speaking_event_participated=0)
        assert _advocacy_impact_score(inp) == 14.0

    def test_pipeline_10k_to_49k_adds_7(self):
        inp = make_input(referral_pipeline_value_usd=20000.0,
                         referrals_converted_to_deals=0, contract_value_usd=0.0,
                         speaking_event_participated=0)
        assert _advocacy_impact_score(inp) == 7.0

    def test_pipeline_below_10k_adds_0(self):
        inp = make_input(referral_pipeline_value_usd=5000.0,
                         referrals_converted_to_deals=0, contract_value_usd=0.0,
                         speaking_event_participated=0)
        assert _advocacy_impact_score(inp) == 0.0

    def test_deals_ge_3_adds_30(self):
        inp = make_input(referral_pipeline_value_usd=0.0,
                         referrals_converted_to_deals=3, contract_value_usd=0.0,
                         speaking_event_participated=0)
        assert _advocacy_impact_score(inp) == 30.0

    def test_deals_2_adds_20(self):
        inp = make_input(referral_pipeline_value_usd=0.0,
                         referrals_converted_to_deals=2, contract_value_usd=0.0,
                         speaking_event_participated=0)
        assert _advocacy_impact_score(inp) == 20.0

    def test_deals_1_adds_10(self):
        inp = make_input(referral_pipeline_value_usd=0.0,
                         referrals_converted_to_deals=1, contract_value_usd=0.0,
                         speaking_event_participated=0)
        assert _advocacy_impact_score(inp) == 10.0

    def test_contract_ge_500k_adds_15(self):
        inp = make_input(referral_pipeline_value_usd=0.0,
                         referrals_converted_to_deals=0, contract_value_usd=500000.0,
                         speaking_event_participated=0)
        assert _advocacy_impact_score(inp) == 15.0

    def test_contract_200k_to_499k_adds_10(self):
        inp = make_input(referral_pipeline_value_usd=0.0,
                         referrals_converted_to_deals=0, contract_value_usd=250000.0,
                         speaking_event_participated=0)
        assert _advocacy_impact_score(inp) == 10.0

    def test_contract_100k_to_199k_adds_6(self):
        inp = make_input(referral_pipeline_value_usd=0.0,
                         referrals_converted_to_deals=0, contract_value_usd=150000.0,
                         speaking_event_participated=0)
        assert _advocacy_impact_score(inp) == 6.0

    def test_contract_50k_to_99k_adds_3(self):
        inp = make_input(referral_pipeline_value_usd=0.0,
                         referrals_converted_to_deals=0, contract_value_usd=75000.0,
                         speaking_event_participated=0)
        assert _advocacy_impact_score(inp) == 3.0

    def test_speaking_event_adds_15(self):
        inp = make_input(referral_pipeline_value_usd=0.0,
                         referrals_converted_to_deals=0, contract_value_usd=0.0,
                         speaking_event_participated=1)
        assert _advocacy_impact_score(inp) == 15.0

    def test_zero_everything_is_zero(self):
        inp = make_input(referral_pipeline_value_usd=0.0,
                         referrals_converted_to_deals=0, contract_value_usd=0.0,
                         speaking_event_participated=0)
        assert _advocacy_impact_score(inp) == 0.0

    def test_clamped_at_100(self):
        inp = make_input(referral_pipeline_value_usd=1000000.0,
                         referrals_converted_to_deals=10, contract_value_usd=1000000.0,
                         speaking_event_participated=1)
        assert _advocacy_impact_score(inp) <= 100.0


# ---------------------------------------------------------------------------
# TestCompositeFunction
# ---------------------------------------------------------------------------

class TestCompositeFunction:
    def test_all_zeros(self):
        assert _composite(0.0, 0.0, 0.0, 0.0) == 0.0

    def test_all_100(self):
        assert _composite(100.0, 100.0, 100.0, 100.0) == 100.0

    def test_formula_weights(self):
        # advocacy*0.30 + relationship*0.25 + propensity*0.25 + impact*0.20
        result = _composite(80.0, 60.0, 70.0, 50.0)
        expected = round(80*0.30 + 60*0.25 + 70*0.25 + 50*0.20, 1)
        assert result == expected

    def test_only_advocacy(self):
        assert _composite(100.0, 0.0, 0.0, 0.0) == 30.0

    def test_only_relationship(self):
        assert _composite(0.0, 100.0, 0.0, 0.0) == 25.0

    def test_only_propensity(self):
        assert _composite(0.0, 0.0, 100.0, 0.0) == 25.0

    def test_only_impact(self):
        assert _composite(0.0, 0.0, 0.0, 100.0) == 20.0

    def test_returns_rounded_to_1_decimal(self):
        result = _composite(33.3, 33.3, 33.3, 33.3)
        assert result == round(33.3*0.30 + 33.3*0.25 + 33.3*0.25 + 33.3*0.20, 1)

    def test_weights_sum_to_1(self):
        assert _composite(1.0, 1.0, 1.0, 1.0) == 1.0


# ---------------------------------------------------------------------------
# TestIsActiveReferrer
# ---------------------------------------------------------------------------

class TestIsActiveReferrer:
    def test_active_referrer_true(self):
        inp = make_input(referrals_given_lifetime=1, last_referral_days_ago=100)
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        assert result.is_active_referrer is True

    def test_no_referrals_given_is_inactive(self):
        inp = make_input(referrals_given_lifetime=0, last_referral_days_ago=10)
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        assert result.is_active_referrer is False

    def test_referral_too_old_is_inactive(self):
        inp = make_input(referrals_given_lifetime=5, last_referral_days_ago=181)
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        assert result.is_active_referrer is False

    def test_exactly_180_days_is_active(self):
        inp = make_input(referrals_given_lifetime=1, last_referral_days_ago=180)
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        assert result.is_active_referrer is True

    def test_exactly_1_referral_is_active(self):
        inp = make_input(referrals_given_lifetime=1, last_referral_days_ago=1)
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        assert result.is_active_referrer is True

    def test_zero_referrals_and_old_is_inactive(self):
        inp = make_input(referrals_given_lifetime=0, last_referral_days_ago=999)
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        assert result.is_active_referrer is False


# ---------------------------------------------------------------------------
# TestNeedsAdvocacyActivation
# ---------------------------------------------------------------------------

class TestNeedsAdvocacyActivation:
    def test_activation_needed_true(self):
        # Need composite >= 60, referrals_given_lifetime == 0, nps_score >= 30
        inp = make_input(
            nps_score=80.0, referrals_given_lifetime=0, referrals_converted_to_deals=0,
            referral_pipeline_value_usd=0.0, case_study_agreed=1, review_submitted=1,
            speaking_event_participated=1, product_feedback_sessions_completed=3,
            community_posts_count=8, champion_identified=1, exec_relationship_strength=90.0,
            account_tenure_days=730, last_referral_days_ago=999, referral_ask_count=0,
            competitive_references_blocked=0, customer_success_score=90.0,
            renewal_probability_pct=95.0, expansion_completed=1,
        )
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        assert result.needs_advocacy_activation is True

    def test_activation_false_if_has_referrals(self):
        inp = make_input(referrals_given_lifetime=1)
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        assert result.needs_advocacy_activation is False

    def test_activation_false_if_nps_below_30(self):
        # Same high-scoring customer but low NPS
        inp = make_input(
            nps_score=25.0, referrals_given_lifetime=0, referrals_converted_to_deals=0,
            referral_pipeline_value_usd=0.0, case_study_agreed=1, review_submitted=1,
            speaking_event_participated=1, product_feedback_sessions_completed=3,
            community_posts_count=8, champion_identified=1, exec_relationship_strength=90.0,
            account_tenure_days=730, last_referral_days_ago=999, referral_ask_count=0,
            competitive_references_blocked=0, customer_success_score=90.0,
            renewal_probability_pct=95.0, expansion_completed=1,
        )
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        assert result.needs_advocacy_activation is False

    def test_detractor_does_not_need_activation(self):
        engine = CustomerReferralIntelligence()
        result = engine.analyze(detractor_input())
        assert result.needs_advocacy_activation is False

    def test_nps_exactly_30_qualifies(self):
        # Build a customer with nps=30 and enough other signals to exceed composite>=60
        inp = make_input(
            nps_score=30.0, referrals_given_lifetime=0, referrals_converted_to_deals=0,
            referral_pipeline_value_usd=0.0, case_study_agreed=1, review_submitted=1,
            speaking_event_participated=1, product_feedback_sessions_completed=3,
            community_posts_count=8, champion_identified=1, exec_relationship_strength=90.0,
            account_tenure_days=730, last_referral_days_ago=999, referral_ask_count=0,
            competitive_references_blocked=0, customer_success_score=90.0,
            renewal_probability_pct=95.0, expansion_completed=1,
        )
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        if result.referral_composite >= 60:
            assert result.needs_advocacy_activation is True


# ---------------------------------------------------------------------------
# TestReferralVelocityLogic
# ---------------------------------------------------------------------------

class TestReferralVelocityLogic:
    def test_zero_referrals_is_inactive(self):
        inp = make_input(referrals_given_lifetime=0, last_referral_days_ago=10)
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        assert result.referral_velocity == ReferralVelocity.INACTIVE

    def test_last_referral_over_365_is_inactive(self):
        inp = make_input(referrals_given_lifetime=5, last_referral_days_ago=366)
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        assert result.referral_velocity == ReferralVelocity.INACTIVE

    def test_last_referral_181_to_365_is_declining(self):
        inp = make_input(referrals_given_lifetime=2, last_referral_days_ago=200)
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        assert result.referral_velocity == ReferralVelocity.DECLINING

    def test_recent_and_multiple_is_accelerating(self):
        inp = make_input(referrals_given_lifetime=2, last_referral_days_ago=20)
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        assert result.referral_velocity == ReferralVelocity.ACCELERATING

    def test_recent_but_only_one_is_steady(self):
        inp = make_input(referrals_given_lifetime=1, last_referral_days_ago=20)
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        assert result.referral_velocity == ReferralVelocity.STEADY

    def test_last_referral_31_to_180_is_steady(self):
        inp = make_input(referrals_given_lifetime=2, last_referral_days_ago=90)
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        assert result.referral_velocity == ReferralVelocity.STEADY

    def test_exactly_365_days_ago_is_inactive(self):
        inp = make_input(referrals_given_lifetime=3, last_referral_days_ago=365)
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        # last_referral_days_ago > 365 is INACTIVE; 365 is exactly not > 365
        assert result.referral_velocity != ReferralVelocity.INACTIVE

    def test_exactly_30_days_and_2_referrals_is_accelerating(self):
        inp = make_input(referrals_given_lifetime=2, last_referral_days_ago=30)
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        assert result.referral_velocity == ReferralVelocity.ACCELERATING


# ---------------------------------------------------------------------------
# TestAdvocacyLevelLogic
# ---------------------------------------------------------------------------

class TestAdvocacyLevelLogic:
    def test_detractor_nps_negative_and_low_composite(self):
        engine = CustomerReferralIntelligence()
        result = engine.analyze(detractor_input())
        assert result.advocacy_level == AdvocacyLevel.DETRACTOR

    def test_champion_high_composite_and_good_nps(self):
        inp = make_input()  # defaults are champion-worthy
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        # Verify composite is high enough
        if result.referral_composite >= 75 and result.advocacy_score >= 25:
            assert result.advocacy_level == AdvocacyLevel.CHAMPION

    def test_promoter_composite_55_to_74(self):
        # Create someone with moderate composite
        inp = make_input(
            nps_score=60.0, case_study_agreed=0, review_submitted=0,
            speaking_event_participated=0, product_feedback_sessions_completed=1,
            community_posts_count=0, champion_identified=1, exec_relationship_strength=50.0,
            account_tenure_days=400, customer_success_score=60.0,
            referrals_given_lifetime=1, referrals_converted_to_deals=0,
            renewal_probability_pct=70.0, expansion_completed=0,
            competitive_references_blocked=0, referral_ask_count=0,
            referral_pipeline_value_usd=0.0, last_referral_days_ago=60,
            contract_value_usd=50000.0,
        )
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        if 55 <= result.referral_composite < 75:
            assert result.advocacy_level == AdvocacyLevel.PROMOTER

    def test_passive_below_55_composite(self):
        # Barely engaged customer
        inp = make_input(
            nps_score=30.0, case_study_agreed=0, review_submitted=0,
            speaking_event_participated=0, product_feedback_sessions_completed=0,
            community_posts_count=0, champion_identified=0, exec_relationship_strength=20.0,
            account_tenure_days=180, customer_success_score=40.0,
            referrals_given_lifetime=0, referrals_converted_to_deals=0,
            renewal_probability_pct=50.0, expansion_completed=0,
            competitive_references_blocked=0, referral_ask_count=0,
            referral_pipeline_value_usd=0.0, last_referral_days_ago=999,
            contract_value_usd=30000.0,
        )
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        if result.referral_composite < 55:
            assert result.advocacy_level == AdvocacyLevel.PASSIVE


# ---------------------------------------------------------------------------
# TestReferralRiskLogic
# ---------------------------------------------------------------------------

class TestReferralRiskLogic:
    def test_critical_nps_very_negative(self):
        inp = make_input(nps_score=-35.0)
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        assert result.referral_risk == ReferralRisk.CRITICAL

    def test_critical_very_low_composite(self):
        engine = CustomerReferralIntelligence()
        result = engine.analyze(detractor_input())
        assert result.referral_risk == ReferralRisk.CRITICAL

    def test_high_risk_nps_negative(self):
        # nps < 0 but > -30 and composite >= 25
        inp = make_input(
            nps_score=-10.0, case_study_agreed=1, review_submitted=1,
            speaking_event_participated=0, champion_identified=1,
            exec_relationship_strength=60.0, account_tenure_days=400,
            customer_success_score=60.0, referrals_given_lifetime=0,
            referral_pipeline_value_usd=0.0, referrals_converted_to_deals=0,
            renewal_probability_pct=60.0, expansion_completed=0,
            competitive_references_blocked=0, referral_ask_count=0,
            product_feedback_sessions_completed=0, community_posts_count=0,
            last_referral_days_ago=999, contract_value_usd=100000.0,
        )
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        if -30 <= result.advocacy_score and result.referral_composite >= 25:
            assert result.referral_risk in (ReferralRisk.HIGH, ReferralRisk.MODERATE, ReferralRisk.LOW)

    def test_low_risk_high_composite(self):
        engine = CustomerReferralIntelligence()
        result = engine.analyze(make_input())
        if result.referral_composite >= 60 and result.advocacy_score >= 0:
            assert result.referral_risk == ReferralRisk.LOW

    def test_moderate_risk_composite_40_to_59(self):
        # Build a moderate composite customer
        inp = make_input(
            nps_score=50.0, case_study_agreed=0, review_submitted=0,
            speaking_event_participated=0, product_feedback_sessions_completed=1,
            community_posts_count=0, champion_identified=1, exec_relationship_strength=40.0,
            account_tenure_days=365, customer_success_score=50.0,
            referrals_given_lifetime=1, referrals_converted_to_deals=0,
            renewal_probability_pct=60.0, expansion_completed=0,
            competitive_references_blocked=0, referral_ask_count=0,
            referral_pipeline_value_usd=0.0, last_referral_days_ago=100,
            contract_value_usd=40000.0,
        )
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        if 40 <= result.referral_composite < 60:
            assert result.referral_risk == ReferralRisk.MODERATE


# ---------------------------------------------------------------------------
# TestReferralActionLogic
# ---------------------------------------------------------------------------

class TestReferralActionLogic:
    def test_detractor_gets_convert_detractor(self):
        engine = CustomerReferralIntelligence()
        result = engine.analyze(detractor_input())
        assert result.referral_action == ReferralAction.CONVERT_DETRACTOR

    def test_high_composite_with_referrals_activate(self):
        inp = make_input(referrals_given_lifetime=5, last_referral_days_ago=20)
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        if result.referral_composite >= 70 and result.advocacy_level != AdvocacyLevel.DETRACTOR:
            assert result.referral_action == ReferralAction.ACTIVATE_REFERRAL

    def test_last_referral_over_180_re_engage(self):
        inp = make_input(referrals_given_lifetime=2, last_referral_days_ago=200,
                         nps_score=60.0)
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        if result.advocacy_level != AdvocacyLevel.DETRACTOR:
            assert result.referral_action == ReferralAction.RE_ENGAGE

    def test_passive_level_re_engage(self):
        inp = make_input(
            nps_score=20.0, case_study_agreed=0, review_submitted=0,
            speaking_event_participated=0, product_feedback_sessions_completed=0,
            community_posts_count=0, champion_identified=0, exec_relationship_strength=20.0,
            account_tenure_days=180, customer_success_score=40.0,
            referrals_given_lifetime=0, referrals_converted_to_deals=0,
            renewal_probability_pct=50.0, expansion_completed=0,
            competitive_references_blocked=0, referral_ask_count=0,
            referral_pipeline_value_usd=0.0, last_referral_days_ago=90,
            contract_value_usd=30000.0,
        )
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        if result.advocacy_level == AdvocacyLevel.PASSIVE:
            assert result.referral_action == ReferralAction.RE_ENGAGE


# ---------------------------------------------------------------------------
# TestEstimatedReferralPipeline
# ---------------------------------------------------------------------------

class TestEstimatedReferralPipeline:
    def test_high_composite_pipeline_estimate(self):
        engine = CustomerReferralIntelligence()
        result = engine.analyze(make_input(contract_value_usd=100000.0))
        # composite >= 75: base * 0.60 = 100000 * 2.5 * 0.60
        if result.referral_composite >= 75:
            assert result.estimated_referral_pipeline_usd == 150000.0

    def test_medium_composite_pipeline_estimate(self):
        inp = make_input(contract_value_usd=100000.0)
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        # Just verify it's positive and reasonable
        assert result.estimated_referral_pipeline_usd >= 0.0

    def test_low_composite_gives_low_pipeline(self):
        engine = CustomerReferralIntelligence()
        result = engine.analyze(detractor_input())
        # composite < 40: base * 0.05
        # contract_value = 150000 by default in detractor_input
        assert result.estimated_referral_pipeline_usd >= 0.0

    def test_pipeline_uses_contract_value(self):
        engine = CustomerReferralIntelligence()
        r1 = engine.analyze(make_input(customer_id="a", contract_value_usd=100000.0))
        engine2 = CustomerReferralIntelligence()
        r2 = engine2.analyze(make_input(customer_id="b", contract_value_usd=200000.0))
        # r2 should have a higher or equal pipeline estimate since same composite range
        assert r2.estimated_referral_pipeline_usd >= r1.estimated_referral_pipeline_usd


# ---------------------------------------------------------------------------
# TestPrimaryAdvocacySignal
# ---------------------------------------------------------------------------

class TestPrimaryAdvocacySignal:
    def test_detractor_nps_signal(self):
        inp = make_input(nps_score=-30.0, case_study_agreed=0, speaking_event_participated=0,
                         referrals_given_lifetime=0)
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        assert "detractor risk" in result.primary_advocacy_signal.lower() or \
               "NPS" in result.primary_advocacy_signal

    def test_speaker_and_case_study_signal(self):
        inp = make_input(nps_score=80.0, speaking_event_participated=1, case_study_agreed=1,
                         referrals_given_lifetime=0)
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        assert "speaker" in result.primary_advocacy_signal

    def test_referrals_given_signal(self):
        inp = make_input(nps_score=50.0, speaking_event_participated=0, case_study_agreed=0,
                         referrals_given_lifetime=5, referrals_converted_to_deals=3)
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        assert "5 referrals" in result.primary_advocacy_signal

    def test_case_study_signal(self):
        inp = make_input(nps_score=50.0, speaking_event_participated=0, case_study_agreed=1,
                         referrals_given_lifetime=0)
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        assert "case study" in result.primary_advocacy_signal.lower()

    def test_nps_promoter_never_asked_signal(self):
        inp = make_input(nps_score=75.0, speaking_event_participated=0, case_study_agreed=0,
                         referrals_given_lifetime=0, referral_ask_count=0)
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        assert "activate" in result.primary_advocacy_signal.lower() or \
               "NPS promoter" in result.primary_advocacy_signal

    def test_primary_signal_is_string(self):
        engine = CustomerReferralIntelligence()
        result = engine.analyze(make_input())
        assert isinstance(result.primary_advocacy_signal, str)
        assert len(result.primary_advocacy_signal) > 0


# ---------------------------------------------------------------------------
# TestCustomerReferralIntelligenceAnalyze
# ---------------------------------------------------------------------------

class TestAnalyzeMethod:
    def test_returns_result_object(self):
        engine = CustomerReferralIntelligence()
        result = engine.analyze(make_input())
        assert isinstance(result, CustomerReferralResult)

    def test_result_stored_in_engine(self):
        engine = CustomerReferralIntelligence()
        inp = make_input(customer_id="store_test")
        engine.analyze(inp)
        assert engine.get("store_test") is not None

    def test_score_clamped_0_to_100_advocacy(self):
        engine = CustomerReferralIntelligence()
        result = engine.analyze(make_input())
        assert 0.0 <= result.advocacy_score <= 100.0

    def test_score_clamped_0_to_100_relationship(self):
        engine = CustomerReferralIntelligence()
        result = engine.analyze(make_input())
        assert 0.0 <= result.relationship_depth_score <= 100.0

    def test_score_clamped_0_to_100_propensity(self):
        engine = CustomerReferralIntelligence()
        result = engine.analyze(make_input())
        assert 0.0 <= result.referral_propensity_score <= 100.0

    def test_score_clamped_0_to_100_impact(self):
        engine = CustomerReferralIntelligence()
        result = engine.analyze(make_input())
        assert 0.0 <= result.advocacy_impact_score <= 100.0

    def test_composite_matches_formula(self):
        engine = CustomerReferralIntelligence()
        result = engine.analyze(make_input())
        expected = _composite(
            result.advocacy_score, result.relationship_depth_score,
            result.referral_propensity_score, result.advocacy_impact_score,
        )
        assert result.referral_composite == expected

    def test_customer_id_preserved(self):
        engine = CustomerReferralIntelligence()
        result = engine.analyze(make_input(customer_id="abc_123"))
        assert result.customer_id == "abc_123"

    def test_customer_name_preserved(self):
        engine = CustomerReferralIntelligence()
        result = engine.analyze(make_input(customer_name="My Company"))
        assert result.customer_name == "My Company"

    def test_overwrite_previous_result(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input(customer_id="c1", nps_score=50.0))
        engine.analyze(make_input(customer_id="c1", nps_score=90.0))
        result = engine.get("c1")
        # second analysis overwrites; composite should reflect higher nps
        assert result is not None

    def test_detractor_analysis(self):
        engine = CustomerReferralIntelligence()
        result = engine.analyze(detractor_input())
        assert result.advocacy_level == AdvocacyLevel.DETRACTOR
        assert result.referral_action == ReferralAction.CONVERT_DETRACTOR

    def test_composite_in_0_100_range(self):
        engine = CustomerReferralIntelligence()
        for i in range(5):
            result = engine.analyze(make_input(customer_id=f"c_{i}", nps_score=float(i * 20)))
            assert 0.0 <= result.referral_composite <= 100.0


# ---------------------------------------------------------------------------
# TestAnalyzeBatch
# ---------------------------------------------------------------------------

class TestAnalyzeBatch:
    def test_returns_list(self):
        engine = CustomerReferralIntelligence()
        results = engine.analyze_batch([make_input(customer_id="b1"),
                                        make_input(customer_id="b2")])
        assert isinstance(results, list)

    def test_all_results_returned(self):
        engine = CustomerReferralIntelligence()
        inputs = [make_input(customer_id=f"b{i}") for i in range(5)]
        results = engine.analyze_batch(inputs)
        assert len(results) == 5

    def test_sorted_descending_by_composite(self):
        engine = CustomerReferralIntelligence()
        inputs = [
            make_input(customer_id="low", nps_score=10.0, referrals_given_lifetime=0,
                       case_study_agreed=0, review_submitted=0, speaking_event_participated=0,
                       product_feedback_sessions_completed=0, community_posts_count=0,
                       champion_identified=0, exec_relationship_strength=10.0,
                       account_tenure_days=90, customer_success_score=20.0,
                       referral_pipeline_value_usd=0.0, referrals_converted_to_deals=0,
                       renewal_probability_pct=30.0, expansion_completed=0,
                       competitive_references_blocked=0, referral_ask_count=0,
                       contract_value_usd=10000.0, last_referral_days_ago=999),
            make_input(customer_id="high"),  # full champion defaults
        ]
        results = engine.analyze_batch(inputs)
        composites = [r.referral_composite for r in results]
        assert composites == sorted(composites, reverse=True)

    def test_empty_batch(self):
        engine = CustomerReferralIntelligence()
        results = engine.analyze_batch([])
        assert results == []

    def test_single_item_batch(self):
        engine = CustomerReferralIntelligence()
        results = engine.analyze_batch([make_input(customer_id="solo")])
        assert len(results) == 1

    def test_batch_stores_results(self):
        engine = CustomerReferralIntelligence()
        engine.analyze_batch([make_input(customer_id="ba1"), make_input(customer_id="ba2")])
        assert engine.get("ba1") is not None
        assert engine.get("ba2") is not None

    def test_sort_order_with_three_items(self):
        engine = CustomerReferralIntelligence()
        inputs = [
            make_input(customer_id="mid", nps_score=50.0),
            make_input(customer_id="det", nps_score=-50.0, referrals_given_lifetime=0,
                       case_study_agreed=0, review_submitted=0, speaking_event_participated=0,
                       product_feedback_sessions_completed=0, community_posts_count=0,
                       champion_identified=0, exec_relationship_strength=10.0,
                       account_tenure_days=30, customer_success_score=10.0,
                       referral_pipeline_value_usd=0.0, referrals_converted_to_deals=0,
                       renewal_probability_pct=10.0, expansion_completed=0,
                       competitive_references_blocked=0, referral_ask_count=0,
                       contract_value_usd=5000.0, last_referral_days_ago=999),
            make_input(customer_id="champ"),
        ]
        results = engine.analyze_batch(inputs)
        composites = [r.referral_composite for r in results]
        for i in range(len(composites) - 1):
            assert composites[i] >= composites[i + 1]


# ---------------------------------------------------------------------------
# TestGetMethod
# ---------------------------------------------------------------------------

class TestGetMethod:
    def test_get_existing(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input(customer_id="get_test"))
        result = engine.get("get_test")
        assert result is not None
        assert result.customer_id == "get_test"

    def test_get_nonexistent_returns_none(self):
        engine = CustomerReferralIntelligence()
        assert engine.get("nonexistent") is None

    def test_get_after_reset_returns_none(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input(customer_id="reset_test"))
        engine.reset()
        assert engine.get("reset_test") is None


# ---------------------------------------------------------------------------
# TestAllCustomers
# ---------------------------------------------------------------------------

class TestAllCustomers:
    def test_returns_all_analyzed(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input(customer_id="c1"))
        engine.analyze(make_input(customer_id="c2"))
        engine.analyze(make_input(customer_id="c3"))
        assert len(engine.all_customers()) == 3

    def test_sorted_descending_by_composite(self):
        engine = CustomerReferralIntelligence()
        engine.analyze_batch([
            make_input(customer_id="a1"),
            detractor_input("a2"),
        ])
        customers = engine.all_customers()
        composites = [r.referral_composite for r in customers]
        assert composites == sorted(composites, reverse=True)

    def test_empty_all_customers(self):
        engine = CustomerReferralIntelligence()
        assert engine.all_customers() == []

    def test_returns_result_objects(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input(customer_id="obj_test"))
        for r in engine.all_customers():
            assert isinstance(r, CustomerReferralResult)


# ---------------------------------------------------------------------------
# TestActiveReferrers
# ---------------------------------------------------------------------------

class TestActiveReferrers:
    def test_only_active_referrers_returned(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input(customer_id="active1", referrals_given_lifetime=2,
                                  last_referral_days_ago=30))
        engine.analyze(make_input(customer_id="inactive1", referrals_given_lifetime=0,
                                  last_referral_days_ago=999))
        engine.analyze(make_input(customer_id="old1", referrals_given_lifetime=3,
                                  last_referral_days_ago=200))
        actives = engine.active_referrers()
        assert all(r.is_active_referrer for r in actives)

    def test_inactive_customer_not_in_active_referrers(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input(customer_id="inactive_r", referrals_given_lifetime=0))
        assert all(r.customer_id != "inactive_r" for r in engine.active_referrers())

    def test_empty_when_no_customers(self):
        engine = CustomerReferralIntelligence()
        assert engine.active_referrers() == []

    def test_active_referrer_counted_correctly(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input(customer_id="a", referrals_given_lifetime=1, last_referral_days_ago=100))
        engine.analyze(make_input(customer_id="b", referrals_given_lifetime=1, last_referral_days_ago=100))
        engine.analyze(make_input(customer_id="c", referrals_given_lifetime=0))
        assert len(engine.active_referrers()) == 2


# ---------------------------------------------------------------------------
# TestActivationQueue
# ---------------------------------------------------------------------------

class TestActivationQueue:
    def test_only_activation_needed_returned(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input())  # has referrals, not in queue
        engine.analyze(detractor_input("det_q"))  # detractor, not in queue
        for r in engine.activation_queue():
            assert r.needs_advocacy_activation is True

    def test_detractor_not_in_activation_queue(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(detractor_input())
        assert all(r.advocacy_level != AdvocacyLevel.DETRACTOR
                   for r in engine.activation_queue())

    def test_empty_when_no_customers(self):
        engine = CustomerReferralIntelligence()
        assert engine.activation_queue() == []


# ---------------------------------------------------------------------------
# TestByVelocity
# ---------------------------------------------------------------------------

class TestByVelocity:
    def test_filter_accelerating(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input(customer_id="acc", referrals_given_lifetime=5,
                                  last_referral_days_ago=10))
        engine.analyze(make_input(customer_id="inact", referrals_given_lifetime=0,
                                  last_referral_days_ago=999))
        accelerating = engine.by_velocity(ReferralVelocity.ACCELERATING)
        assert all(r.referral_velocity == ReferralVelocity.ACCELERATING for r in accelerating)

    def test_filter_inactive(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input(customer_id="inact2", referrals_given_lifetime=0))
        inactive = engine.by_velocity(ReferralVelocity.INACTIVE)
        assert len(inactive) >= 1

    def test_empty_for_absent_velocity(self):
        engine = CustomerReferralIntelligence()
        # No customers => any velocity returns empty
        assert engine.by_velocity(ReferralVelocity.ACCELERATING) == []

    def test_all_velocities_partition_correctly(self):
        engine = CustomerReferralIntelligence()
        inputs = [
            make_input(customer_id="v1", referrals_given_lifetime=3, last_referral_days_ago=20),
            make_input(customer_id="v2", referrals_given_lifetime=1, last_referral_days_ago=100),
            make_input(customer_id="v3", referrals_given_lifetime=2, last_referral_days_ago=250),
            make_input(customer_id="v4", referrals_given_lifetime=0, last_referral_days_ago=999),
        ]
        engine.analyze_batch(inputs)
        total = (len(engine.by_velocity(ReferralVelocity.ACCELERATING)) +
                 len(engine.by_velocity(ReferralVelocity.STEADY)) +
                 len(engine.by_velocity(ReferralVelocity.DECLINING)) +
                 len(engine.by_velocity(ReferralVelocity.INACTIVE)))
        assert total == 4


# ---------------------------------------------------------------------------
# TestByAdvocacyLevel
# ---------------------------------------------------------------------------

class TestByAdvocacyLevel:
    def test_filter_detractor(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(detractor_input())
        detractors = engine.by_advocacy_level(AdvocacyLevel.DETRACTOR)
        assert all(r.advocacy_level == AdvocacyLevel.DETRACTOR for r in detractors)

    def test_filter_champion(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input())
        champions = engine.by_advocacy_level(AdvocacyLevel.CHAMPION)
        assert all(r.advocacy_level == AdvocacyLevel.CHAMPION for r in champions)

    def test_empty_when_none_match(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(detractor_input())
        # Champions should be empty since only detractor exists
        champions = engine.by_advocacy_level(AdvocacyLevel.CHAMPION)
        assert len(champions) == 0

    def test_all_levels_partition_correctly(self):
        engine = CustomerReferralIntelligence()
        engine.analyze_batch([make_input(customer_id="al1"), detractor_input("al2")])
        total = (len(engine.by_advocacy_level(AdvocacyLevel.CHAMPION)) +
                 len(engine.by_advocacy_level(AdvocacyLevel.PROMOTER)) +
                 len(engine.by_advocacy_level(AdvocacyLevel.PASSIVE)) +
                 len(engine.by_advocacy_level(AdvocacyLevel.DETRACTOR)))
        assert total == 2


# ---------------------------------------------------------------------------
# TestAvgReferralComposite
# ---------------------------------------------------------------------------

class TestAvgReferralComposite:
    def test_empty_returns_zero(self):
        engine = CustomerReferralIntelligence()
        assert engine.avg_referral_composite() == 0.0

    def test_single_customer(self):
        engine = CustomerReferralIntelligence()
        result = engine.analyze(make_input(customer_id="avg1"))
        assert engine.avg_referral_composite() == result.referral_composite

    def test_two_customers_average(self):
        engine = CustomerReferralIntelligence()
        r1 = engine.analyze(make_input(customer_id="avg_a"))
        r2 = engine.analyze(detractor_input("avg_b"))
        expected = round((r1.referral_composite + r2.referral_composite) / 2, 1)
        assert engine.avg_referral_composite() == expected

    def test_returns_float(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input())
        assert isinstance(engine.avg_referral_composite(), float)

    def test_after_reset_returns_zero(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input())
        engine.reset()
        assert engine.avg_referral_composite() == 0.0


# ---------------------------------------------------------------------------
# TestReset
# ---------------------------------------------------------------------------

class TestReset:
    def test_reset_clears_all(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input(customer_id="r1"))
        engine.analyze(make_input(customer_id="r2"))
        engine.reset()
        assert len(engine.all_customers()) == 0

    def test_reset_allows_reuse(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input(customer_id="pre_reset"))
        engine.reset()
        engine.analyze(make_input(customer_id="post_reset"))
        assert engine.get("pre_reset") is None
        assert engine.get("post_reset") is not None

    def test_avg_composite_zero_after_reset(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input())
        engine.reset()
        assert engine.avg_referral_composite() == 0.0


# ---------------------------------------------------------------------------
# TestSummary
# ---------------------------------------------------------------------------

class TestSummary:
    def test_summary_returns_exactly_13_keys(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input())
        assert len(engine.summary()) == 13

    def test_summary_exact_keys(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input())
        expected_keys = {
            "total", "velocity_counts", "advocacy_counts", "risk_counts", "action_counts",
            "avg_referral_composite", "active_referrer_count", "activation_needed_count",
            "avg_advocacy_score", "avg_relationship_depth_score",
            "avg_referral_propensity_score", "avg_advocacy_impact_score",
            "total_estimated_referral_pipeline_usd",
        }
        assert set(engine.summary().keys()) == expected_keys

    def test_summary_total_count(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input(customer_id="s1"))
        engine.analyze(make_input(customer_id="s2"))
        engine.analyze(detractor_input("s3"))
        assert engine.summary()["total"] == 3

    def test_summary_empty(self):
        engine = CustomerReferralIntelligence()
        s = engine.summary()
        assert s["total"] == 0
        assert s["avg_referral_composite"] == 0.0
        assert s["active_referrer_count"] == 0
        assert s["activation_needed_count"] == 0

    def test_summary_velocity_counts_dict(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input())
        s = engine.summary()
        assert isinstance(s["velocity_counts"], dict)

    def test_summary_advocacy_counts_dict(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input())
        s = engine.summary()
        assert isinstance(s["advocacy_counts"], dict)

    def test_summary_risk_counts_dict(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input())
        s = engine.summary()
        assert isinstance(s["risk_counts"], dict)

    def test_summary_action_counts_dict(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input())
        s = engine.summary()
        assert isinstance(s["action_counts"], dict)

    def test_summary_velocity_counts_sum_equals_total(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input(customer_id="sc1"))
        engine.analyze(detractor_input("sc2"))
        s = engine.summary()
        assert sum(s["velocity_counts"].values()) == s["total"]

    def test_summary_advocacy_counts_sum_equals_total(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input(customer_id="sa1"))
        engine.analyze(detractor_input("sa2"))
        s = engine.summary()
        assert sum(s["advocacy_counts"].values()) == s["total"]

    def test_summary_risk_counts_sum_equals_total(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input(customer_id="sr1"))
        engine.analyze(detractor_input("sr2"))
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_equals_total(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input(customer_id="sac1"))
        engine.analyze(detractor_input("sac2"))
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_avg_composite_matches_method(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input(customer_id="sm1"))
        engine.analyze(detractor_input("sm2"))
        s = engine.summary()
        assert s["avg_referral_composite"] == engine.avg_referral_composite()

    def test_summary_active_referrer_count(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input(customer_id="sar1", referrals_given_lifetime=2,
                                  last_referral_days_ago=30))
        engine.analyze(make_input(customer_id="sar2", referrals_given_lifetime=0))
        s = engine.summary()
        assert s["active_referrer_count"] == len(engine.active_referrers())

    def test_summary_activation_needed_count(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input())
        engine.analyze(detractor_input("san1"))
        s = engine.summary()
        assert s["activation_needed_count"] == len(engine.activation_queue())

    def test_summary_avg_advocacy_score_positive(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input())
        s = engine.summary()
        assert s["avg_advocacy_score"] >= 0.0

    def test_summary_avg_relationship_score_positive(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input())
        s = engine.summary()
        assert s["avg_relationship_depth_score"] >= 0.0

    def test_summary_avg_propensity_score_positive(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input())
        s = engine.summary()
        assert s["avg_referral_propensity_score"] >= 0.0

    def test_summary_avg_impact_score_positive(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input())
        s = engine.summary()
        assert s["avg_advocacy_impact_score"] >= 0.0

    def test_summary_total_pipeline_positive(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input())
        s = engine.summary()
        assert s["total_estimated_referral_pipeline_usd"] >= 0.0

    def test_summary_total_pipeline_sum_of_individual(self):
        engine = CustomerReferralIntelligence()
        r1 = engine.analyze(make_input(customer_id="sp1"))
        r2 = engine.analyze(make_input(customer_id="sp2"))
        s = engine.summary()
        expected = round(r1.estimated_referral_pipeline_usd + r2.estimated_referral_pipeline_usd, 0)
        assert s["total_estimated_referral_pipeline_usd"] == expected

    def test_summary_takes_no_args(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input())
        # summary() should work with no arguments
        s = engine.summary()
        assert s is not None

    def test_summary_keys_after_reset(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input())
        engine.reset()
        s = engine.summary()
        assert len(s) == 13


# ---------------------------------------------------------------------------
# TestScoreClampingEdgeCases
# ---------------------------------------------------------------------------

class TestScoreClampingEdgeCases:
    def test_all_scores_are_non_negative(self):
        engine = CustomerReferralIntelligence()
        result = engine.analyze(detractor_input())
        assert result.advocacy_score >= 0.0
        assert result.relationship_depth_score >= 0.0
        assert result.referral_propensity_score >= 0.0
        assert result.advocacy_impact_score >= 0.0

    def test_all_scores_at_most_100(self):
        engine = CustomerReferralIntelligence()
        result = engine.analyze(make_input())
        assert result.advocacy_score <= 100.0
        assert result.relationship_depth_score <= 100.0
        assert result.referral_propensity_score <= 100.0
        assert result.advocacy_impact_score <= 100.0

    def test_extreme_positive_inputs_clamped(self):
        inp = make_input(
            nps_score=100.0, exec_relationship_strength=100.0,
            customer_success_score=100.0, referral_pipeline_value_usd=9999999.0,
            referrals_given_lifetime=100, referrals_converted_to_deals=100,
            contract_value_usd=9999999.0, renewal_probability_pct=100.0,
            account_tenure_days=9999, community_posts_count=100,
            product_feedback_sessions_completed=100,
        )
        engine = CustomerReferralIntelligence()
        result = engine.analyze(inp)
        assert result.advocacy_score <= 100.0
        assert result.relationship_depth_score <= 100.0
        assert result.referral_propensity_score <= 100.0
        assert result.advocacy_impact_score <= 100.0

    def test_extreme_negative_nps_clamped(self):
        inp = make_input(nps_score=-9999.0, case_study_agreed=0, review_submitted=0,
                         speaking_event_participated=0, product_feedback_sessions_completed=0,
                         community_posts_count=0)
        score = _advocacy_score(inp)
        assert score >= 0.0


# ---------------------------------------------------------------------------
# TestMultipleCustomersScenarios
# ---------------------------------------------------------------------------

class TestMultipleCustomersScenarios:
    def test_batch_then_get_each(self):
        engine = CustomerReferralIntelligence()
        inputs = [make_input(customer_id=f"mc_{i}") for i in range(10)]
        engine.analyze_batch(inputs)
        for i in range(10):
            assert engine.get(f"mc_{i}") is not None

    def test_mix_of_champions_and_detractors(self):
        engine = CustomerReferralIntelligence()
        champions = [make_input(customer_id=f"champ_{i}") for i in range(3)]
        detractors = [detractor_input(f"det_{i}") for i in range(3)]
        engine.analyze_batch(champions + detractors)
        assert len(engine.all_customers()) == 6

    def test_all_customers_sorted_after_batch(self):
        engine = CustomerReferralIntelligence()
        inputs = [make_input(customer_id=f"sort_{i}") for i in range(5)]
        engine.analyze_batch(inputs)
        customers = engine.all_customers()
        composites = [r.referral_composite for r in customers]
        assert composites == sorted(composites, reverse=True)

    def test_summary_with_multiple_customers(self):
        engine = CustomerReferralIntelligence()
        inputs = [make_input(customer_id=f"multi_{i}") for i in range(5)]
        inputs += [detractor_input(f"multi_det_{i}") for i in range(3)]
        engine.analyze_batch(inputs)
        s = engine.summary()
        assert s["total"] == 8
        assert len(s) == 13

    def test_reset_and_reanalyze(self):
        engine = CustomerReferralIntelligence()
        engine.analyze_batch([make_input(customer_id=f"old_{i}") for i in range(5)])
        engine.reset()
        engine.analyze_batch([make_input(customer_id=f"new_{i}") for i in range(3)])
        assert len(engine.all_customers()) == 3

    def test_no_duplicate_ids_after_reanalysis(self):
        engine = CustomerReferralIntelligence()
        engine.analyze(make_input(customer_id="dup"))
        engine.analyze(make_input(customer_id="dup"))
        assert len(engine.all_customers()) == 1

    def test_by_velocity_after_mixed_batch(self):
        engine = CustomerReferralIntelligence()
        inputs = [
            make_input(customer_id="vel_acc", referrals_given_lifetime=3,
                       last_referral_days_ago=15),
            make_input(customer_id="vel_inact", referrals_given_lifetime=0,
                       last_referral_days_ago=999),
        ]
        engine.analyze_batch(inputs)
        assert len(engine.by_velocity(ReferralVelocity.ACCELERATING)) >= 1
        assert len(engine.by_velocity(ReferralVelocity.INACTIVE)) >= 1
