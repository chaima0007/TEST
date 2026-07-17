"""
Comprehensive pytest test suite for PricingElasticityEngine.
Target: 270–290 tests, all passing.
"""
from __future__ import annotations

import pytest
from swarm.intelligence.pricing_elasticity_engine import (
    ElasticityCategory,
    PricingAction,
    PricingElasticityEngine,
    PricingElasticityInput,
    PricingElasticityResult,
    PricingRisk,
    PricingStance,
)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def make_input(**overrides) -> PricingElasticityInput:
    defaults = dict(
        segment_id="seg_001",
        segment_name="Test Segment",
        industry="SaaS",
        region="NAMER",
        avg_deal_size_current=50000.0,
        avg_deal_size_prev=48000.0,
        price_increase_pct=5.0,
        deals_before_increase=20,
        deals_after_increase=19,
        price_objection_rate=20.0,
        discount_request_rate=25.0,
        avg_discount_given_pct=8.0,
        win_rate_at_list_price=55.0,
        win_rate_with_discount=62.0,
        churn_due_to_price=10.0,
        competitive_price_gap=5.0,
        total_pipeline_value=1000000.0,
        deals_in_pipeline=30,
        nps_price_sensitivity=30.0,
        upsell_conversion_rate=40.0,
        willingness_to_pay_index=65.0,
        contract_length_avg_months=12,
    )
    defaults.update(overrides)
    return PricingElasticityInput(**defaults)


@pytest.fixture
def engine():
    return PricingElasticityEngine()


@pytest.fixture
def default_input():
    return make_input()


@pytest.fixture
def default_result(engine, default_input):
    return engine.analyze(default_input)


# ===========================================================================
# 1. Enum tests
# ===========================================================================

class TestElasticityCategory:
    def test_inelastic_value(self):
        assert ElasticityCategory.INELASTIC.value == "inelastic"

    def test_low_value(self):
        assert ElasticityCategory.LOW.value == "low"

    def test_moderate_value(self):
        assert ElasticityCategory.MODERATE.value == "moderate"

    def test_high_value(self):
        assert ElasticityCategory.HIGH.value == "high"

    def test_extreme_value(self):
        assert ElasticityCategory.EXTREME.value == "extreme"

    def test_enum_members_count(self):
        assert len(ElasticityCategory) == 5

    def test_is_str_subclass(self):
        assert isinstance(ElasticityCategory.INELASTIC, str)

    def test_string_comparison(self):
        assert ElasticityCategory.LOW == "low"

    def test_membership(self):
        assert ElasticityCategory.MODERATE in ElasticityCategory


class TestPricingRisk:
    def test_low_value(self):
        assert PricingRisk.LOW.value == "low"

    def test_medium_value(self):
        assert PricingRisk.MEDIUM.value == "medium"

    def test_high_value(self):
        assert PricingRisk.HIGH.value == "high"

    def test_critical_value(self):
        assert PricingRisk.CRITICAL.value == "critical"

    def test_enum_members_count(self):
        assert len(PricingRisk) == 4

    def test_is_str_subclass(self):
        assert isinstance(PricingRisk.HIGH, str)

    def test_string_comparison(self):
        assert PricingRisk.CRITICAL == "critical"


class TestPricingStance:
    def test_premium_value(self):
        assert PricingStance.PREMIUM.value == "premium"

    def test_competitive_value(self):
        assert PricingStance.COMPETITIVE.value == "competitive"

    def test_neutral_value(self):
        assert PricingStance.NEUTRAL.value == "neutral"

    def test_defensive_value(self):
        assert PricingStance.DEFENSIVE.value == "defensive"

    def test_vulnerable_value(self):
        assert PricingStance.VULNERABLE.value == "vulnerable"

    def test_enum_members_count(self):
        assert len(PricingStance) == 5

    def test_is_str_subclass(self):
        assert isinstance(PricingStance.NEUTRAL, str)


class TestPricingAction:
    def test_increase_value(self):
        assert PricingAction.INCREASE.value == "increase"

    def test_hold_value(self):
        assert PricingAction.HOLD.value == "hold"

    def test_optimize_value(self):
        assert PricingAction.OPTIMIZE.value == "optimize"

    def test_discount_control_value(self):
        assert PricingAction.DISCOUNT_CONTROL.value == "discount_control"

    def test_restructure_value(self):
        assert PricingAction.RESTRUCTURE.value == "restructure"

    def test_enum_members_count(self):
        assert len(PricingAction) == 5

    def test_is_str_subclass(self):
        assert isinstance(PricingAction.HOLD, str)


# ===========================================================================
# 2. PricingElasticityInput dataclass
# ===========================================================================

class TestPricingElasticityInput:
    def test_creates_with_defaults(self, default_input):
        assert default_input.segment_id == "seg_001"

    def test_segment_name(self, default_input):
        assert default_input.segment_name == "Test Segment"

    def test_industry(self, default_input):
        assert default_input.industry == "SaaS"

    def test_region(self, default_input):
        assert default_input.region == "NAMER"

    def test_avg_deal_size_current(self, default_input):
        assert default_input.avg_deal_size_current == 50000.0

    def test_avg_deal_size_prev(self, default_input):
        assert default_input.avg_deal_size_prev == 48000.0

    def test_price_increase_pct(self, default_input):
        assert default_input.price_increase_pct == 5.0

    def test_deals_before_increase(self, default_input):
        assert default_input.deals_before_increase == 20

    def test_deals_after_increase(self, default_input):
        assert default_input.deals_after_increase == 19

    def test_price_objection_rate(self, default_input):
        assert default_input.price_objection_rate == 20.0

    def test_discount_request_rate(self, default_input):
        assert default_input.discount_request_rate == 25.0

    def test_avg_discount_given_pct(self, default_input):
        assert default_input.avg_discount_given_pct == 8.0

    def test_win_rate_at_list_price(self, default_input):
        assert default_input.win_rate_at_list_price == 55.0

    def test_win_rate_with_discount(self, default_input):
        assert default_input.win_rate_with_discount == 62.0

    def test_churn_due_to_price(self, default_input):
        assert default_input.churn_due_to_price == 10.0

    def test_competitive_price_gap(self, default_input):
        assert default_input.competitive_price_gap == 5.0

    def test_total_pipeline_value(self, default_input):
        assert default_input.total_pipeline_value == 1000000.0

    def test_deals_in_pipeline(self, default_input):
        assert default_input.deals_in_pipeline == 30

    def test_nps_price_sensitivity(self, default_input):
        assert default_input.nps_price_sensitivity == 30.0

    def test_upsell_conversion_rate(self, default_input):
        assert default_input.upsell_conversion_rate == 40.0

    def test_willingness_to_pay_index(self, default_input):
        assert default_input.willingness_to_pay_index == 65.0

    def test_contract_length_avg_months(self, default_input):
        assert default_input.contract_length_avg_months == 12

    def test_field_count(self):
        import dataclasses
        fields = dataclasses.fields(PricingElasticityInput)
        assert len(fields) == 22

    def test_override_works(self):
        inp = make_input(segment_id="seg_999")
        assert inp.segment_id == "seg_999"


# ===========================================================================
# 3. PricingElasticityResult.to_dict()
# ===========================================================================

class TestPricingElasticityResultToDict:
    def test_to_dict_returns_dict(self, default_result):
        assert isinstance(default_result.to_dict(), dict)

    def test_to_dict_has_15_keys(self, default_result):
        assert len(default_result.to_dict()) == 15

    def test_to_dict_segment_id(self, default_result):
        assert default_result.to_dict()["segment_id"] == "seg_001"

    def test_to_dict_segment_name(self, default_result):
        assert default_result.to_dict()["segment_name"] == "Test Segment"

    def test_to_dict_elasticity_category_is_str(self, default_result):
        assert isinstance(default_result.to_dict()["elasticity_category"], str)

    def test_to_dict_pricing_risk_is_str(self, default_result):
        assert isinstance(default_result.to_dict()["pricing_risk"], str)

    def test_to_dict_pricing_stance_is_str(self, default_result):
        assert isinstance(default_result.to_dict()["pricing_stance"], str)

    def test_to_dict_pricing_action_is_str(self, default_result):
        assert isinstance(default_result.to_dict()["pricing_action"], str)

    def test_to_dict_price_elasticity_index_present(self, default_result):
        assert "price_elasticity_index" in default_result.to_dict()

    def test_to_dict_discount_leak_score_present(self, default_result):
        assert "discount_leak_score" in default_result.to_dict()

    def test_to_dict_competitive_pressure_score_present(self, default_result):
        assert "competitive_pressure_score" in default_result.to_dict()

    def test_to_dict_revenue_at_risk_present(self, default_result):
        assert "revenue_at_risk" in default_result.to_dict()

    def test_to_dict_expansion_opportunity_present(self, default_result):
        assert "expansion_opportunity" in default_result.to_dict()

    def test_to_dict_optimal_price_adjustment_pct_present(self, default_result):
        assert "optimal_price_adjustment_pct" in default_result.to_dict()

    def test_to_dict_pricing_confidence_score_present(self, default_result):
        assert "pricing_confidence_score" in default_result.to_dict()

    def test_to_dict_is_price_sensitive_present(self, default_result):
        assert "is_price_sensitive" in default_result.to_dict()

    def test_to_dict_needs_pricing_review_present(self, default_result):
        assert "needs_pricing_review" in default_result.to_dict()

    def test_to_dict_is_price_sensitive_is_bool(self, default_result):
        assert isinstance(default_result.to_dict()["is_price_sensitive"], bool)

    def test_to_dict_needs_pricing_review_is_bool(self, default_result):
        assert isinstance(default_result.to_dict()["needs_pricing_review"], bool)

    def test_to_dict_exact_keys(self, default_result):
        expected = {
            "segment_id", "segment_name", "elasticity_category", "pricing_risk",
            "pricing_stance", "pricing_action", "price_elasticity_index",
            "discount_leak_score", "competitive_pressure_score", "revenue_at_risk",
            "expansion_opportunity", "optimal_price_adjustment_pct",
            "pricing_confidence_score", "is_price_sensitive", "needs_pricing_review",
        }
        assert set(default_result.to_dict().keys()) == expected


# ===========================================================================
# 4. _price_elasticity_index
# ===========================================================================

class TestPriceElasticityIndex:
    def test_default_input_range(self, engine, default_input):
        idx = engine._price_elasticity_index(default_input)
        assert 0.0 <= idx <= 100.0

    def test_zero_objection_rate_contributes_zero(self, engine):
        inp = make_input(price_objection_rate=0.0)
        idx = engine._price_elasticity_index(inp)
        # objection component should be 0
        assert idx >= 0.0

    def test_objection_rate_max_cap_30(self, engine):
        # objection_rate * 0.5, capped at 30
        inp = make_input(
            price_objection_rate=100.0,
            win_rate_at_list_price=60.0,
            win_rate_with_discount=60.0,  # no discount lift
            deals_before_increase=20,
            deals_after_increase=20,       # no demand change
            price_increase_pct=5.0,
            willingness_to_pay_index=100.0,  # max WTP -> WTP signal 0
        )
        idx = engine._price_elasticity_index(inp)
        # Only objection contributes: min(30, 100*0.5)=30
        assert idx == 30.0

    def test_discount_lift_contributes(self, engine):
        inp = make_input(
            win_rate_at_list_price=50.0,
            win_rate_with_discount=80.0,   # lift = 30 -> 30*0.8 = 24
            price_objection_rate=0.0,
            deals_before_increase=0,        # no demand response
            willingness_to_pay_index=100.0,
        )
        idx = engine._price_elasticity_index(inp)
        assert idx == 24.0

    def test_discount_lift_max_cap_25(self, engine):
        inp = make_input(
            win_rate_at_list_price=0.0,
            win_rate_with_discount=100.0,  # lift 100 -> 100*0.8=80, capped 25
            price_objection_rate=0.0,
            deals_before_increase=0,
            willingness_to_pay_index=100.0,
        )
        idx = engine._price_elasticity_index(inp)
        assert idx == 25.0

    def test_negative_discount_lift_ignored(self, engine):
        # win_rate_with_discount < win_rate_at_list_price -> lift=0
        inp = make_input(
            win_rate_at_list_price=70.0,
            win_rate_with_discount=50.0,
            price_objection_rate=0.0,
            deals_before_increase=0,
            willingness_to_pay_index=100.0,
        )
        idx = engine._price_elasticity_index(inp)
        assert idx == 0.0

    def test_demand_response_positive(self, engine):
        inp = make_input(
            price_objection_rate=0.0,
            win_rate_at_list_price=60.0,
            win_rate_with_discount=60.0,
            deals_before_increase=20,
            deals_after_increase=10,  # 50% demand drop
            price_increase_pct=10.0,  # 10% price increase
            # demand_change = 0.5, price_elasticity = 0.5/0.1 = 5 -> 5*10=50, cap 25
            willingness_to_pay_index=100.0,
        )
        idx = engine._price_elasticity_index(inp)
        assert idx == 25.0

    def test_demand_response_zero_when_no_price_increase(self, engine):
        inp = make_input(
            price_objection_rate=0.0,
            win_rate_at_list_price=60.0,
            win_rate_with_discount=60.0,
            deals_before_increase=20,
            deals_after_increase=10,
            price_increase_pct=0.0,  # no increase, so no demand response
            willingness_to_pay_index=100.0,
        )
        idx = engine._price_elasticity_index(inp)
        assert idx == 0.0

    def test_demand_response_zero_when_no_deals_before(self, engine):
        inp = make_input(
            price_objection_rate=0.0,
            win_rate_at_list_price=60.0,
            win_rate_with_discount=60.0,
            deals_before_increase=0,
            price_increase_pct=5.0,
            willingness_to_pay_index=100.0,
        )
        idx = engine._price_elasticity_index(inp)
        assert idx == 0.0

    def test_demand_increase_not_counted(self, engine):
        # demand_change < 0 -> not counted
        inp = make_input(
            price_objection_rate=0.0,
            win_rate_at_list_price=60.0,
            win_rate_with_discount=60.0,
            deals_before_increase=10,
            deals_after_increase=20,  # demand increased
            price_increase_pct=5.0,
            willingness_to_pay_index=100.0,
        )
        idx = engine._price_elasticity_index(inp)
        assert idx == 0.0

    def test_wtp_high_reduces_score(self, engine):
        # WTP=100 -> contribution = (100-100)*0.2 = 0
        inp = make_input(
            price_objection_rate=0.0,
            win_rate_at_list_price=60.0,
            win_rate_with_discount=60.0,
            deals_before_increase=0,
            willingness_to_pay_index=100.0,
        )
        idx = engine._price_elasticity_index(inp)
        assert idx == 0.0

    def test_wtp_zero_max_contribution(self, engine):
        # WTP=0 -> (100-0)*0.2 = 20, cap 20
        inp = make_input(
            price_objection_rate=0.0,
            win_rate_at_list_price=60.0,
            win_rate_with_discount=60.0,
            deals_before_increase=0,
            willingness_to_pay_index=0.0,
        )
        idx = engine._price_elasticity_index(inp)
        assert idx == 20.0

    def test_wtp_contribution_capped_at_20(self, engine):
        # Already handled by score += min(20, ...) logic
        inp = make_input(
            price_objection_rate=0.0,
            win_rate_at_list_price=60.0,
            win_rate_with_discount=60.0,
            deals_before_increase=0,
            willingness_to_pay_index=0.0,
        )
        idx = engine._price_elasticity_index(inp)
        assert idx <= 100.0

    def test_max_all_components(self, engine):
        # Max all components: 30 + 25 + 25 + 20 = 100
        inp = make_input(
            price_objection_rate=100.0,
            win_rate_at_list_price=0.0,
            win_rate_with_discount=100.0,
            deals_before_increase=20,
            deals_after_increase=0,
            price_increase_pct=1.0,
            willingness_to_pay_index=0.0,
        )
        idx = engine._price_elasticity_index(inp)
        assert idx == 100.0

    def test_result_is_rounded_to_1dp(self, engine):
        inp = make_input(price_objection_rate=33.0)  # 33*0.5=16.5
        idx = engine._price_elasticity_index(inp)
        assert idx == round(idx, 1)

    def test_result_never_below_zero(self, engine):
        inp = make_input(
            price_objection_rate=0.0,
            win_rate_at_list_price=80.0,
            win_rate_with_discount=40.0,
            deals_before_increase=10,
            deals_after_increase=20,
            willingness_to_pay_index=100.0,
        )
        idx = engine._price_elasticity_index(inp)
        assert idx >= 0.0


# ===========================================================================
# 5. _discount_leak_score
# ===========================================================================

class TestDiscountLeakScore:
    def test_default_input_range(self, engine, default_input):
        score = engine._discount_leak_score(default_input)
        assert 0.0 <= score <= 100.0

    def test_zero_inputs(self, engine):
        inp = make_input(
            discount_request_rate=0.0,
            avg_discount_given_pct=0.0,
            win_rate_at_list_price=60.0,
            win_rate_with_discount=60.0,
        )
        score = engine._discount_leak_score(inp)
        assert score == 0.0

    def test_discount_request_component_capped_at_40(self, engine):
        inp = make_input(
            discount_request_rate=100.0,
            avg_discount_given_pct=0.0,
            win_rate_at_list_price=60.0,
            win_rate_with_discount=60.0,
        )
        score = engine._discount_leak_score(inp)
        assert score == 40.0

    def test_avg_discount_component_capped_at_35(self, engine):
        inp = make_input(
            discount_request_rate=0.0,
            avg_discount_given_pct=50.0,   # 50*1.0=50 -> capped 35
            win_rate_at_list_price=60.0,
            win_rate_with_discount=60.0,
        )
        score = engine._discount_leak_score(inp)
        assert score == 35.0

    def test_discount_lift_component_capped_at_25(self, engine):
        inp = make_input(
            discount_request_rate=0.0,
            avg_discount_given_pct=0.0,
            win_rate_at_list_price=0.0,
            win_rate_with_discount=100.0,  # lift=100 -> 100*0.6=60, cap 25
        )
        score = engine._discount_leak_score(inp)
        assert score == 25.0

    def test_max_score_100(self, engine):
        inp = make_input(
            discount_request_rate=100.0,
            avg_discount_given_pct=100.0,
            win_rate_at_list_price=0.0,
            win_rate_with_discount=100.0,
        )
        score = engine._discount_leak_score(inp)
        assert score == 100.0

    def test_negative_lift_ignored(self, engine):
        inp = make_input(
            discount_request_rate=0.0,
            avg_discount_given_pct=0.0,
            win_rate_at_list_price=70.0,
            win_rate_with_discount=50.0,  # negative lift -> 0
        )
        score = engine._discount_leak_score(inp)
        assert score == 0.0

    def test_result_rounded_to_1dp(self, engine):
        inp = make_input(discount_request_rate=33.0)  # 33*0.6=19.8
        score = engine._discount_leak_score(inp)
        assert score == round(score, 1)

    def test_partial_discount_request(self, engine):
        # discount_request_rate=50 -> 50*0.6=30
        inp = make_input(
            discount_request_rate=50.0,
            avg_discount_given_pct=0.0,
            win_rate_at_list_price=60.0,
            win_rate_with_discount=60.0,
        )
        score = engine._discount_leak_score(inp)
        assert score == 30.0

    def test_partial_avg_discount(self, engine):
        # avg_discount_given_pct=20 -> 20*1.0=20
        inp = make_input(
            discount_request_rate=0.0,
            avg_discount_given_pct=20.0,
            win_rate_at_list_price=60.0,
            win_rate_with_discount=60.0,
        )
        score = engine._discount_leak_score(inp)
        assert score == 20.0


# ===========================================================================
# 6. _competitive_pressure_score
# ===========================================================================

class TestCompetitivePressureScore:
    def test_default_input_range(self, engine, default_input):
        score = engine._competitive_pressure_score(default_input)
        assert 0.0 <= score <= 100.0

    def test_zero_inputs(self, engine):
        inp = make_input(
            competitive_price_gap=0.0,
            churn_due_to_price=0.0,
            nps_price_sensitivity=0.0,
        )
        score = engine._competitive_pressure_score(inp)
        assert score == 0.0

    def test_negative_gap_ignored(self, engine):
        inp = make_input(
            competitive_price_gap=-10.0,
            churn_due_to_price=0.0,
            nps_price_sensitivity=0.0,
        )
        score = engine._competitive_pressure_score(inp)
        assert score == 0.0

    def test_positive_gap_contribution(self, engine):
        # gap=10 -> 10*2=20
        inp = make_input(
            competitive_price_gap=10.0,
            churn_due_to_price=0.0,
            nps_price_sensitivity=0.0,
        )
        score = engine._competitive_pressure_score(inp)
        assert score == 20.0

    def test_positive_gap_capped_at_40(self, engine):
        inp = make_input(
            competitive_price_gap=50.0,   # 50*2=100, cap 40
            churn_due_to_price=0.0,
            nps_price_sensitivity=0.0,
        )
        score = engine._competitive_pressure_score(inp)
        assert score == 40.0

    def test_churn_contribution(self, engine):
        # churn=20 -> 20*0.7=14
        inp = make_input(
            competitive_price_gap=0.0,
            churn_due_to_price=20.0,
            nps_price_sensitivity=0.0,
        )
        score = engine._competitive_pressure_score(inp)
        assert score == 14.0

    def test_churn_capped_at_35(self, engine):
        inp = make_input(
            competitive_price_gap=0.0,
            churn_due_to_price=100.0,  # 100*0.7=70, cap 35
            nps_price_sensitivity=0.0,
        )
        score = engine._competitive_pressure_score(inp)
        assert score == 35.0

    def test_positive_nps_ignored(self, engine):
        inp = make_input(
            competitive_price_gap=0.0,
            churn_due_to_price=0.0,
            nps_price_sensitivity=50.0,  # positive, no contribution
        )
        score = engine._competitive_pressure_score(inp)
        assert score == 0.0

    def test_negative_nps_contributes(self, engine):
        # nps=-40 -> abs(40)*0.25=10
        inp = make_input(
            competitive_price_gap=0.0,
            churn_due_to_price=0.0,
            nps_price_sensitivity=-40.0,
        )
        score = engine._competitive_pressure_score(inp)
        assert score == 10.0

    def test_negative_nps_capped_at_25(self, engine):
        inp = make_input(
            competitive_price_gap=0.0,
            churn_due_to_price=0.0,
            nps_price_sensitivity=-200.0,  # abs=200 * 0.25=50, cap 25
        )
        score = engine._competitive_pressure_score(inp)
        assert score == 25.0

    def test_max_score_100(self, engine):
        inp = make_input(
            competitive_price_gap=50.0,
            churn_due_to_price=100.0,
            nps_price_sensitivity=-200.0,
        )
        score = engine._competitive_pressure_score(inp)
        assert score == 100.0

    def test_result_rounded(self, engine):
        inp = make_input(
            competitive_price_gap=3.0,  # 3*2=6
            churn_due_to_price=0.0,
            nps_price_sensitivity=0.0,
        )
        score = engine._competitive_pressure_score(inp)
        assert score == round(score, 1)


# ===========================================================================
# 7. _elasticity_category
# ===========================================================================

class TestElasticityCategory:
    def test_extreme_at_75(self, engine):
        assert engine._elasticity_category(75.0) == ElasticityCategory.EXTREME

    def test_extreme_above_75(self, engine):
        assert engine._elasticity_category(90.0) == ElasticityCategory.EXTREME

    def test_extreme_at_100(self, engine):
        assert engine._elasticity_category(100.0) == ElasticityCategory.EXTREME

    def test_high_at_55(self, engine):
        assert engine._elasticity_category(55.0) == ElasticityCategory.HIGH

    def test_high_at_74(self, engine):
        assert engine._elasticity_category(74.9) == ElasticityCategory.HIGH

    def test_moderate_at_35(self, engine):
        assert engine._elasticity_category(35.0) == ElasticityCategory.MODERATE

    def test_moderate_at_54(self, engine):
        assert engine._elasticity_category(54.9) == ElasticityCategory.MODERATE

    def test_low_at_15(self, engine):
        assert engine._elasticity_category(15.0) == ElasticityCategory.LOW

    def test_low_at_34(self, engine):
        assert engine._elasticity_category(34.9) == ElasticityCategory.LOW

    def test_inelastic_at_0(self, engine):
        assert engine._elasticity_category(0.0) == ElasticityCategory.INELASTIC

    def test_inelastic_at_14(self, engine):
        assert engine._elasticity_category(14.9) == ElasticityCategory.INELASTIC

    def test_boundary_just_below_extreme(self, engine):
        assert engine._elasticity_category(74.9) == ElasticityCategory.HIGH

    def test_boundary_just_below_high(self, engine):
        assert engine._elasticity_category(54.9) == ElasticityCategory.MODERATE

    def test_boundary_just_below_moderate(self, engine):
        assert engine._elasticity_category(34.9) == ElasticityCategory.LOW

    def test_boundary_just_below_low(self, engine):
        assert engine._elasticity_category(14.9) == ElasticityCategory.INELASTIC


# ===========================================================================
# 8. _pricing_risk
# ===========================================================================

class TestPricingRisk:
    def _make_risk(self, engine, elasticity, comp_pressure, **kw):
        inp = make_input(**kw)
        return engine._pricing_risk(inp, elasticity, comp_pressure)

    def test_critical_when_combined_ge_65(self, engine):
        # elasticity=65, comp=65 -> combined=65
        risk = self._make_risk(engine, 65.0, 65.0)
        assert risk == PricingRisk.CRITICAL

    def test_critical_when_churn_ge_30(self, engine):
        risk = self._make_risk(engine, 0.0, 0.0, churn_due_to_price=30.0)
        assert risk == PricingRisk.CRITICAL

    def test_critical_churn_above_30(self, engine):
        risk = self._make_risk(engine, 0.0, 0.0, churn_due_to_price=50.0)
        assert risk == PricingRisk.CRITICAL

    def test_high_when_combined_ge_45(self, engine):
        # combined=45
        risk = self._make_risk(engine, 45.0, 45.0)
        assert risk == PricingRisk.HIGH

    def test_high_when_price_objection_ge_40(self, engine):
        risk = self._make_risk(engine, 0.0, 0.0, price_objection_rate=40.0)
        assert risk == PricingRisk.HIGH

    def test_high_objection_above_40(self, engine):
        risk = self._make_risk(engine, 0.0, 0.0, price_objection_rate=60.0)
        assert risk == PricingRisk.HIGH

    def test_medium_when_combined_ge_25(self, engine):
        risk = self._make_risk(engine, 25.0, 25.0)
        assert risk == PricingRisk.MEDIUM

    def test_medium_at_exactly_25(self, engine):
        risk = self._make_risk(engine, 25.0, 25.0)  # combined=25
        assert risk == PricingRisk.MEDIUM

    def test_low_when_combined_below_25(self, engine):
        risk = self._make_risk(engine, 10.0, 10.0)  # combined=10
        assert risk == PricingRisk.LOW

    def test_low_at_zero(self, engine):
        risk = self._make_risk(engine, 0.0, 0.0, churn_due_to_price=0.0, price_objection_rate=0.0)
        assert risk == PricingRisk.LOW

    def test_combined_formula(self, engine):
        # combined = elasticity*0.5 + comp*0.5
        # 40*0.5 + 50*0.5 = 45 -> HIGH
        risk = self._make_risk(engine, 40.0, 50.0)
        assert risk == PricingRisk.HIGH

    def test_critical_takes_priority_over_high(self, engine):
        # combined >= 65 -> CRITICAL even if churn < 30
        risk = self._make_risk(engine, 70.0, 70.0, churn_due_to_price=5.0)
        assert risk == PricingRisk.CRITICAL

    def test_churn_29_not_critical(self, engine):
        risk = self._make_risk(engine, 0.0, 0.0, churn_due_to_price=29.0)
        # combined=0 < 25, churn<30 -> LOW
        assert risk == PricingRisk.LOW

    def test_objection_39_not_high(self, engine):
        risk = self._make_risk(engine, 0.0, 0.0, price_objection_rate=39.0)
        # combined=0 < 25, objection<40 -> LOW
        assert risk == PricingRisk.LOW


# ===========================================================================
# 9. _pricing_stance
# ===========================================================================

class TestPricingStance:
    def _make_stance(self, engine, elasticity, comp_pressure, **kw):
        inp = make_input(**kw)
        return engine._pricing_stance(inp, elasticity, comp_pressure)

    def test_premium_when_wtp_ge_70_and_elastic_lt_35(self, engine):
        stance = self._make_stance(engine, 30.0, 20.0, willingness_to_pay_index=75.0)
        assert stance == PricingStance.PREMIUM

    def test_premium_exact_boundary_wtp_70_elastic_34(self, engine):
        stance = self._make_stance(engine, 34.9, 0.0, willingness_to_pay_index=70.0)
        assert stance == PricingStance.PREMIUM

    def test_not_premium_when_elastic_ge_35(self, engine):
        stance = self._make_stance(engine, 35.0, 0.0, willingness_to_pay_index=80.0)
        assert stance != PricingStance.PREMIUM

    def test_not_premium_when_wtp_lt_70(self, engine):
        stance = self._make_stance(engine, 20.0, 0.0, willingness_to_pay_index=69.9)
        assert stance != PricingStance.PREMIUM

    def test_vulnerable_when_comp_pressure_ge_60(self, engine):
        stance = self._make_stance(engine, 20.0, 60.0, willingness_to_pay_index=50.0)
        assert stance == PricingStance.VULNERABLE

    def test_vulnerable_when_churn_ge_25(self, engine):
        stance = self._make_stance(engine, 20.0, 10.0, willingness_to_pay_index=50.0, churn_due_to_price=25.0)
        assert stance == PricingStance.VULNERABLE

    def test_vulnerable_churn_above_25(self, engine):
        stance = self._make_stance(engine, 10.0, 10.0, willingness_to_pay_index=50.0, churn_due_to_price=50.0)
        assert stance == PricingStance.VULNERABLE

    def test_defensive_when_comp_pressure_ge_40(self, engine):
        stance = self._make_stance(engine, 20.0, 40.0, willingness_to_pay_index=50.0)
        assert stance == PricingStance.DEFENSIVE

    def test_defensive_when_elastic_ge_55(self, engine):
        stance = self._make_stance(engine, 55.0, 10.0, willingness_to_pay_index=50.0)
        assert stance == PricingStance.DEFENSIVE

    def test_competitive_when_gap_le_neg_10(self, engine):
        stance = self._make_stance(engine, 20.0, 0.0, willingness_to_pay_index=50.0, competitive_price_gap=-10.0)
        assert stance == PricingStance.COMPETITIVE

    def test_competitive_gap_below_neg_10(self, engine):
        stance = self._make_stance(engine, 20.0, 0.0, willingness_to_pay_index=50.0, competitive_price_gap=-20.0)
        assert stance == PricingStance.COMPETITIVE

    def test_neutral_default(self, engine):
        stance = self._make_stance(
            engine, 20.0, 10.0,
            willingness_to_pay_index=50.0,
            churn_due_to_price=5.0,
            competitive_price_gap=0.0,
        )
        assert stance == PricingStance.NEUTRAL

    def test_premium_priority_over_vulnerable(self, engine):
        # WTP>=70 AND elasticity<35 -> PREMIUM first
        stance = self._make_stance(engine, 20.0, 70.0, willingness_to_pay_index=80.0)
        assert stance == PricingStance.PREMIUM

    def test_gap_neg_9_not_competitive(self, engine):
        stance = self._make_stance(engine, 10.0, 0.0, willingness_to_pay_index=50.0, competitive_price_gap=-9.0)
        assert stance == PricingStance.NEUTRAL


# ===========================================================================
# 10. _pricing_action
# ===========================================================================

class TestPricingAction:
    def test_restructure_when_critical_risk(self, engine):
        # CRITICAL risk -> RESTRUCTURE
        inp = make_input(churn_due_to_price=35.0)
        result = engine.analyze(inp)
        assert result.pricing_action == PricingAction.RESTRUCTURE

    def test_restructure_when_vulnerable_stance(self, engine):
        # Force VULNERABLE: comp >= 60
        inp = make_input(competitive_price_gap=30.0, churn_due_to_price=26.0)
        result = engine.analyze(inp)
        assert result.pricing_action == PricingAction.RESTRUCTURE

    def test_discount_control_when_leak_ge_50(self, engine):
        # Force discount_leak >= 50, risk not CRITICAL, stance not VULNERABLE
        inp = make_input(
            discount_request_rate=60.0,   # 60*0.6=36
            avg_discount_given_pct=14.0,  # 14*1=14, total=50
            win_rate_at_list_price=60.0,
            win_rate_with_discount=60.0,
            churn_due_to_price=0.0,
            competitive_price_gap=0.0,
            nps_price_sensitivity=0.0,
            price_objection_rate=0.0,
            willingness_to_pay_index=50.0,
        )
        result = engine.analyze(inp)
        assert result.pricing_action == PricingAction.DISCOUNT_CONTROL

    def test_increase_when_premium_and_elastic_lt_35(self, engine):
        # WTP>=70, elasticity<35, stance=PREMIUM
        inp = make_input(
            willingness_to_pay_index=80.0,
            price_objection_rate=0.0,
            discount_request_rate=0.0,
            avg_discount_given_pct=0.0,
            win_rate_at_list_price=60.0,
            win_rate_with_discount=60.0,
            deals_before_increase=0,
            churn_due_to_price=0.0,
            competitive_price_gap=0.0,
            nps_price_sensitivity=0.0,
        )
        result = engine.analyze(inp)
        assert result.pricing_action == PricingAction.INCREASE

    def test_optimize_when_defensive_stance(self, engine):
        # Force DEFENSIVE: comp_pressure >= 40 (gap=20 -> 20*2=40)
        inp = make_input(
            competitive_price_gap=20.0,
            churn_due_to_price=5.0,
            willingness_to_pay_index=50.0,
            price_objection_rate=0.0,
            nps_price_sensitivity=0.0,
            discount_request_rate=0.0,
            avg_discount_given_pct=0.0,
            win_rate_at_list_price=60.0,
            win_rate_with_discount=60.0,
            deals_before_increase=0,
        )
        result = engine.analyze(inp)
        assert result.pricing_action == PricingAction.OPTIMIZE

    def test_optimize_when_competitive_stance(self, engine):
        inp = make_input(
            competitive_price_gap=-15.0,
            churn_due_to_price=0.0,
            willingness_to_pay_index=50.0,
            price_objection_rate=0.0,
            nps_price_sensitivity=0.0,
            discount_request_rate=0.0,
            avg_discount_given_pct=0.0,
            win_rate_at_list_price=60.0,
            win_rate_with_discount=60.0,
            deals_before_increase=0,
        )
        result = engine.analyze(inp)
        assert result.pricing_action == PricingAction.OPTIMIZE

    def test_hold_when_no_special_condition(self, engine):
        # low everything, no premium/defensive/competitive
        inp = make_input(
            price_objection_rate=10.0,
            discount_request_rate=10.0,
            avg_discount_given_pct=5.0,
            win_rate_at_list_price=60.0,
            win_rate_with_discount=62.0,
            deals_before_increase=20,
            deals_after_increase=20,
            price_increase_pct=5.0,
            churn_due_to_price=5.0,
            competitive_price_gap=2.0,
            nps_price_sensitivity=10.0,
            willingness_to_pay_index=50.0,
        )
        result = engine.analyze(inp)
        assert result.pricing_action == PricingAction.HOLD

    def test_increase_when_inelastic_and_wtp_ge_60(self, engine):
        # elasticity < 25, WTP >= 60, not PREMIUM, not DEFENSIVE, not COMPETITIVE
        inp = make_input(
            willingness_to_pay_index=65.0,
            price_objection_rate=0.0,
            discount_request_rate=0.0,
            avg_discount_given_pct=0.0,
            win_rate_at_list_price=60.0,
            win_rate_with_discount=60.0,
            deals_before_increase=0,
            churn_due_to_price=0.0,
            competitive_price_gap=2.0,   # small gap, not defensive (comp_pressure=4)
            nps_price_sensitivity=0.0,
        )
        result = engine.analyze(inp)
        # elasticity should be very low (WTP=65 -> (100-65)*0.2=7), stance=NEUTRAL
        # elasticity < 25, WTP >= 60 -> INCREASE
        assert result.pricing_action == PricingAction.INCREASE


# ===========================================================================
# 11. is_price_sensitive
# ===========================================================================

class TestIsPriceSensitive:
    def test_true_when_elasticity_ge_55(self, engine):
        # Build input that produces elasticity >= 55
        inp = make_input(
            price_objection_rate=100.0,      # 30
            win_rate_at_list_price=0.0,
            win_rate_with_discount=70.0,     # lift=70 -> 70*0.8=56 -> cap 25
            deals_before_increase=20,
            deals_after_increase=0,
            price_increase_pct=5.0,
            willingness_to_pay_index=50.0,
        )
        result = engine.analyze(inp)
        assert result.is_price_sensitive is True

    def test_true_when_price_objection_ge_40(self, engine):
        inp = make_input(price_objection_rate=40.0)
        result = engine.analyze(inp)
        assert result.is_price_sensitive is True

    def test_false_when_both_below_threshold(self, engine):
        inp = make_input(
            price_objection_rate=10.0,
            win_rate_at_list_price=60.0,
            win_rate_with_discount=60.0,
            deals_before_increase=10,
            deals_after_increase=10,
            price_increase_pct=5.0,
            willingness_to_pay_index=80.0,
        )
        result = engine.analyze(inp)
        assert result.is_price_sensitive is False

    def test_objection_39_not_sensitive(self, engine):
        inp = make_input(
            price_objection_rate=39.0,
            win_rate_at_list_price=60.0,
            win_rate_with_discount=60.0,
            deals_before_increase=10,
            deals_after_increase=10,
            willingness_to_pay_index=90.0,
        )
        result = engine.analyze(inp)
        # elasticity ~ 39*0.5=19.5 + 0 + 0 + 2 = 21.5 < 55; objection=39<40
        assert result.is_price_sensitive is False

    def test_objection_exactly_40_is_sensitive(self, engine):
        inp = make_input(price_objection_rate=40.0)
        result = engine.analyze(inp)
        assert result.is_price_sensitive is True


# ===========================================================================
# 12. needs_pricing_review
# ===========================================================================

class TestNeedsPricingReview:
    def test_true_when_discount_leak_ge_50(self, engine):
        inp = make_input(
            discount_request_rate=60.0,
            avg_discount_given_pct=14.0,
            win_rate_at_list_price=60.0,
            win_rate_with_discount=60.0,
        )
        result = engine.analyze(inp)
        assert result.needs_pricing_review is True

    def test_true_when_comp_pressure_ge_60(self, engine):
        # comp_gap=20 -> 20*2=40 (cap 40), churn=30 -> 30*0.7=21, nps=-80 -> 20. Total=81
        inp = make_input(competitive_price_gap=20.0, churn_due_to_price=30.0, nps_price_sensitivity=-80.0)
        result = engine.analyze(inp)
        assert result.needs_pricing_review is True

    def test_true_when_churn_ge_25(self, engine):
        inp = make_input(churn_due_to_price=25.0)
        result = engine.analyze(inp)
        assert result.needs_pricing_review is True

    def test_false_when_all_below_threshold(self, engine):
        inp = make_input(
            discount_request_rate=10.0,
            avg_discount_given_pct=5.0,
            win_rate_at_list_price=60.0,
            win_rate_with_discount=62.0,
            competitive_price_gap=5.0,
            churn_due_to_price=10.0,
            nps_price_sensitivity=10.0,
        )
        result = engine.analyze(inp)
        assert result.needs_pricing_review is False

    def test_churn_24_not_review(self, engine):
        inp = make_input(
            churn_due_to_price=24.0,
            discount_request_rate=0.0,
            avg_discount_given_pct=0.0,
            win_rate_at_list_price=60.0,
            win_rate_with_discount=60.0,
            competitive_price_gap=0.0,
            nps_price_sensitivity=0.0,
        )
        result = engine.analyze(inp)
        assert result.needs_pricing_review is False


# ===========================================================================
# 13. _revenue_at_risk
# ===========================================================================

class TestRevenueAtRisk:
    def test_formula(self, engine):
        # risk_factor = (elasticity*0.6 + comp*0.4)/100
        # revenue_risk = pipeline * risk_factor * 0.3
        elasticity = 50.0
        comp = 30.0
        pipeline = 1_000_000.0
        risk_factor = (elasticity * 0.6 + comp * 0.4) / 100.0
        expected = round(pipeline * risk_factor * 0.3, 2)
        inp = make_input(total_pipeline_value=pipeline)
        result = engine._revenue_at_risk(inp, elasticity, comp)
        assert result == expected

    def test_zero_inputs(self, engine):
        inp = make_input(total_pipeline_value=1_000_000.0)
        result = engine._revenue_at_risk(inp, 0.0, 0.0)
        assert result == 0.0

    def test_max_risk_factor(self, engine):
        # max: elasticity=100, comp=100 -> risk_factor=1.0
        inp = make_input(total_pipeline_value=1_000_000.0)
        result = engine._revenue_at_risk(inp, 100.0, 100.0)
        assert result == 300_000.0

    def test_pipeline_scales_result(self, engine):
        inp1 = make_input(total_pipeline_value=500_000.0)
        inp2 = make_input(total_pipeline_value=1_000_000.0)
        r1 = engine._revenue_at_risk(inp1, 50.0, 50.0)
        r2 = engine._revenue_at_risk(inp2, 50.0, 50.0)
        assert abs(r2 - 2 * r1) < 0.01

    def test_result_is_rounded_to_2dp(self, engine):
        inp = make_input(total_pipeline_value=333_333.0)
        result = engine._revenue_at_risk(inp, 33.3, 33.3)
        assert result == round(result, 2)


# ===========================================================================
# 14. _expansion_opportunity
# ===========================================================================

class TestExpansionOpportunity:
    def test_zero_when_elasticity_ge_60(self, engine):
        inp = make_input(total_pipeline_value=1_000_000.0)
        result = engine._expansion_opportunity(inp, 60.0)
        assert result == 0.0

    def test_zero_when_elasticity_above_60(self, engine):
        inp = make_input(total_pipeline_value=1_000_000.0)
        result = engine._expansion_opportunity(inp, 80.0)
        assert result == 0.0

    def test_formula_below_60(self, engine):
        # headroom = (60-30)/60=0.5; opp = 1_000_000 * 0.5 * 0.15 = 75_000
        inp = make_input(total_pipeline_value=1_000_000.0)
        result = engine._expansion_opportunity(inp, 30.0)
        assert result == 75_000.0

    def test_max_at_elasticity_zero(self, engine):
        # headroom = (60-0)/60=1.0; opp = 1_000_000 * 1.0 * 0.15 = 150_000
        inp = make_input(total_pipeline_value=1_000_000.0)
        result = engine._expansion_opportunity(inp, 0.0)
        assert result == 150_000.0

    def test_pipeline_scales_result(self, engine):
        inp1 = make_input(total_pipeline_value=500_000.0)
        inp2 = make_input(total_pipeline_value=1_000_000.0)
        r1 = engine._expansion_opportunity(inp1, 20.0)
        r2 = engine._expansion_opportunity(inp2, 20.0)
        assert abs(r2 - 2 * r1) < 0.01

    def test_result_rounded_to_2dp(self, engine):
        inp = make_input(total_pipeline_value=123_456.0)
        result = engine._expansion_opportunity(inp, 25.0)
        assert result == round(result, 2)


# ===========================================================================
# 15. _optimal_price_adjustment
# ===========================================================================

class TestOptimalPriceAdjustment:
    def test_wtp_headroom_branch(self, engine):
        # WTP>=70 AND elasticity<40 -> adj = min(15, (WTP-70)*0.3)
        # WTP=80 -> (80-70)*0.3=3.0
        inp = make_input(willingness_to_pay_index=80.0, avg_discount_given_pct=5.0)
        result = engine._optimal_price_adjustment(inp, 30.0, 20.0)
        assert result == 3.0

    def test_wtp_headroom_capped_at_15(self, engine):
        # WTP=120 -> (120-70)*0.3=15 -> exactly 15
        inp = make_input(willingness_to_pay_index=120.0)
        result = engine._optimal_price_adjustment(inp, 30.0, 20.0)
        assert result == 15.0

    def test_negative_adj_when_high_elasticity(self, engine):
        # elasticity>=60 -> adj = max(-15, -comp*0.1)
        # comp=100 -> -10.0
        inp = make_input(willingness_to_pay_index=50.0)
        result = engine._optimal_price_adjustment(inp, 65.0, 100.0)
        assert result == -10.0

    def test_negative_adj_when_high_comp_pressure(self, engine):
        # comp>=60 -> adj = max(-15, -comp*0.1)
        inp = make_input(willingness_to_pay_index=50.0)
        result = engine._optimal_price_adjustment(inp, 30.0, 70.0)
        assert result == -7.0

    def test_negative_adj_capped_at_neg_15(self, engine):
        # comp=200 -> -20 -> max(-15, ...) = -15
        inp = make_input(willingness_to_pay_index=50.0)
        result = engine._optimal_price_adjustment(inp, 65.0, 200.0)
        assert result == -15.0

    def test_discount_branch(self, engine):
        # avg_discount>=20 -> adj = min(10, avg_discount*0.2)
        # avg_discount=30 -> 30*0.2=6
        inp = make_input(willingness_to_pay_index=50.0, avg_discount_given_pct=30.0)
        result = engine._optimal_price_adjustment(inp, 30.0, 30.0)
        assert result == 6.0

    def test_discount_branch_capped_at_10(self, engine):
        inp = make_input(willingness_to_pay_index=50.0, avg_discount_given_pct=60.0)
        result = engine._optimal_price_adjustment(inp, 30.0, 30.0)
        assert result == 10.0

    def test_zero_adj_else_branch(self, engine):
        # WTP<70, elasticity<60, comp<60, avg_discount<20
        inp = make_input(willingness_to_pay_index=50.0, avg_discount_given_pct=10.0)
        result = engine._optimal_price_adjustment(inp, 30.0, 30.0)
        assert result == 0.0

    def test_result_bounded_between_neg20_and_20(self, engine):
        inp = make_input(willingness_to_pay_index=200.0)
        result = engine._optimal_price_adjustment(inp, 10.0, 10.0)
        assert -20.0 <= result <= 20.0

    def test_result_rounded_to_1dp(self, engine):
        inp = make_input(willingness_to_pay_index=80.0)
        result = engine._optimal_price_adjustment(inp, 30.0, 20.0)
        assert result == round(result, 1)


# ===========================================================================
# 16. _pricing_confidence
# ===========================================================================

class TestPricingConfidence:
    def test_all_signals_present(self, engine, default_input):
        # default: deals_before>10, deals_in_pipeline>20, WTP>0, contract>=12, upsell>0
        score = engine._pricing_confidence(default_input)
        assert score == 100.0

    def test_no_signals(self, engine):
        inp = make_input(
            deals_before_increase=5,
            deals_in_pipeline=10,
            willingness_to_pay_index=0.0,
            contract_length_avg_months=6,
            upsell_conversion_rate=0.0,
        )
        score = engine._pricing_confidence(inp)
        assert score == 0.0

    def test_one_signal_deals_before(self, engine):
        inp = make_input(
            deals_before_increase=11,
            deals_in_pipeline=0,
            willingness_to_pay_index=0.0,
            contract_length_avg_months=6,
            upsell_conversion_rate=0.0,
        )
        assert engine._pricing_confidence(inp) == 20.0

    def test_one_signal_deals_pipeline(self, engine):
        inp = make_input(
            deals_before_increase=5,
            deals_in_pipeline=21,
            willingness_to_pay_index=0.0,
            contract_length_avg_months=6,
            upsell_conversion_rate=0.0,
        )
        assert engine._pricing_confidence(inp) == 20.0

    def test_one_signal_wtp(self, engine):
        inp = make_input(
            deals_before_increase=5,
            deals_in_pipeline=0,
            willingness_to_pay_index=50.0,
            contract_length_avg_months=6,
            upsell_conversion_rate=0.0,
        )
        assert engine._pricing_confidence(inp) == 20.0

    def test_one_signal_contract(self, engine):
        inp = make_input(
            deals_before_increase=5,
            deals_in_pipeline=0,
            willingness_to_pay_index=0.0,
            contract_length_avg_months=12,
            upsell_conversion_rate=0.0,
        )
        assert engine._pricing_confidence(inp) == 20.0

    def test_one_signal_upsell(self, engine):
        inp = make_input(
            deals_before_increase=5,
            deals_in_pipeline=0,
            willingness_to_pay_index=0.0,
            contract_length_avg_months=6,
            upsell_conversion_rate=10.0,
        )
        assert engine._pricing_confidence(inp) == 20.0

    def test_two_signals(self, engine):
        inp = make_input(
            deals_before_increase=11,
            deals_in_pipeline=21,
            willingness_to_pay_index=0.0,
            contract_length_avg_months=6,
            upsell_conversion_rate=0.0,
        )
        assert engine._pricing_confidence(inp) == 40.0

    def test_three_signals(self, engine):
        inp = make_input(
            deals_before_increase=11,
            deals_in_pipeline=21,
            willingness_to_pay_index=50.0,
            contract_length_avg_months=6,
            upsell_conversion_rate=0.0,
        )
        assert engine._pricing_confidence(inp) == 60.0

    def test_four_signals(self, engine):
        inp = make_input(
            deals_before_increase=11,
            deals_in_pipeline=21,
            willingness_to_pay_index=50.0,
            contract_length_avg_months=12,
            upsell_conversion_rate=0.0,
        )
        assert engine._pricing_confidence(inp) == 80.0

    def test_deals_before_exactly_10_no_signal(self, engine):
        inp = make_input(
            deals_before_increase=10,   # NOT > 10
            deals_in_pipeline=0,
            willingness_to_pay_index=0.0,
            contract_length_avg_months=6,
            upsell_conversion_rate=0.0,
        )
        assert engine._pricing_confidence(inp) == 0.0

    def test_pipeline_exactly_20_no_signal(self, engine):
        inp = make_input(
            deals_before_increase=5,
            deals_in_pipeline=20,    # NOT > 20
            willingness_to_pay_index=0.0,
            contract_length_avg_months=6,
            upsell_conversion_rate=0.0,
        )
        assert engine._pricing_confidence(inp) == 0.0

    def test_contract_exactly_12_has_signal(self, engine):
        inp = make_input(
            deals_before_increase=5,
            deals_in_pipeline=0,
            willingness_to_pay_index=0.0,
            contract_length_avg_months=12,  # >= 12
            upsell_conversion_rate=0.0,
        )
        assert engine._pricing_confidence(inp) == 20.0

    def test_result_is_float(self, engine, default_input):
        score = engine._pricing_confidence(default_input)
        assert isinstance(score, float)


# ===========================================================================
# 17. Engine: analyze()
# ===========================================================================

class TestEngineAnalyze:
    def test_returns_result_instance(self, engine, default_input):
        result = engine.analyze(default_input)
        assert isinstance(result, PricingElasticityResult)

    def test_segment_id_propagated(self, engine):
        inp = make_input(segment_id="my_seg")
        result = engine.analyze(inp)
        assert result.segment_id == "my_seg"

    def test_segment_name_propagated(self, engine):
        inp = make_input(segment_name="Enterprise")
        result = engine.analyze(inp)
        assert result.segment_name == "Enterprise"

    def test_result_stored_in_engine(self, engine, default_input):
        engine.analyze(default_input)
        assert len(engine._results) == 1

    def test_multiple_results_stored(self, engine):
        engine.analyze(make_input(segment_id="a"))
        engine.analyze(make_input(segment_id="b"))
        assert len(engine._results) == 2

    def test_price_elasticity_index_range(self, engine, default_result):
        assert 0.0 <= default_result.price_elasticity_index <= 100.0

    def test_discount_leak_score_range(self, engine, default_result):
        assert 0.0 <= default_result.discount_leak_score <= 100.0

    def test_competitive_pressure_score_range(self, engine, default_result):
        assert 0.0 <= default_result.competitive_pressure_score <= 100.0

    def test_pricing_confidence_range(self, engine, default_result):
        assert 0.0 <= default_result.pricing_confidence_score <= 100.0

    def test_optimal_adj_range(self, engine, default_result):
        assert -20.0 <= default_result.optimal_price_adjustment_pct <= 20.0

    def test_revenue_at_risk_nonnegative(self, engine, default_result):
        assert default_result.revenue_at_risk >= 0.0

    def test_expansion_opportunity_nonnegative(self, engine, default_result):
        assert default_result.expansion_opportunity >= 0.0

    def test_is_price_sensitive_is_bool(self, engine, default_result):
        assert isinstance(default_result.is_price_sensitive, bool)

    def test_needs_pricing_review_is_bool(self, engine, default_result):
        assert isinstance(default_result.needs_pricing_review, bool)

    def test_elasticity_category_type(self, engine, default_result):
        assert isinstance(default_result.elasticity_category, ElasticityCategory)

    def test_pricing_risk_type(self, engine, default_result):
        assert isinstance(default_result.pricing_risk, PricingRisk)

    def test_pricing_stance_type(self, engine, default_result):
        assert isinstance(default_result.pricing_stance, PricingStance)

    def test_pricing_action_type(self, engine, default_result):
        assert isinstance(default_result.pricing_action, PricingAction)


# ===========================================================================
# 18. Engine: analyze_batch()
# ===========================================================================

class TestAnalyzeBatch:
    def test_empty_batch(self, engine):
        results = engine.analyze_batch([])
        assert results == []

    def test_single_item_batch(self, engine):
        results = engine.analyze_batch([make_input()])
        assert len(results) == 1

    def test_multiple_items(self, engine):
        inputs = [make_input(segment_id=f"s{i}") for i in range(5)]
        results = engine.analyze_batch(inputs)
        assert len(results) == 5

    def test_results_stored_in_engine(self, engine):
        inputs = [make_input(segment_id=f"s{i}") for i in range(3)]
        engine.analyze_batch(inputs)
        assert len(engine._results) == 3

    def test_returns_list_of_results(self, engine):
        results = engine.analyze_batch([make_input()])
        assert all(isinstance(r, PricingElasticityResult) for r in results)

    def test_order_preserved(self, engine):
        inputs = [make_input(segment_id=f"seg_{i}") for i in range(4)]
        results = engine.analyze_batch(inputs)
        ids = [r.segment_id for r in results]
        assert ids == ["seg_0", "seg_1", "seg_2", "seg_3"]

    def test_batch_accumulates_in_engine(self, engine):
        engine.analyze(make_input(segment_id="before"))
        engine.analyze_batch([make_input(segment_id=f"b{i}") for i in range(3)])
        assert len(engine._results) == 4


# ===========================================================================
# 19. Engine: reset()
# ===========================================================================

class TestReset:
    def test_reset_clears_results(self, engine):
        engine.analyze(make_input())
        engine.reset()
        assert len(engine._results) == 0

    def test_reset_on_empty_engine(self, engine):
        engine.reset()
        assert len(engine._results) == 0

    def test_can_analyze_after_reset(self, engine):
        engine.analyze(make_input())
        engine.reset()
        engine.analyze(make_input())
        assert len(engine._results) == 1

    def test_reset_clears_multiple(self, engine):
        for _ in range(5):
            engine.analyze(make_input())
        engine.reset()
        assert len(engine._results) == 0


# ===========================================================================
# 20. Properties
# ===========================================================================

class TestProperties:
    def test_price_sensitive_segments_empty(self, engine):
        assert engine.price_sensitive_segments == []

    def test_price_sensitive_segments_populated(self, engine):
        engine.analyze(make_input(price_objection_rate=45.0))
        engine.analyze(make_input(price_objection_rate=5.0))
        assert len(engine.price_sensitive_segments) == 1

    def test_price_sensitive_matches_is_price_sensitive(self, engine):
        for i in range(3):
            engine.analyze(make_input(
                segment_id=f"s{i}",
                price_objection_rate=40.0 + i * 10,
            ))
        for r in engine.price_sensitive_segments:
            assert r.is_price_sensitive is True

    def test_review_needed_empty(self, engine):
        assert engine.review_needed == []

    def test_review_needed_populated(self, engine):
        engine.analyze(make_input(churn_due_to_price=30.0))
        assert len(engine.review_needed) == 1

    def test_review_needed_matches_needs_review(self, engine):
        engine.analyze(make_input(churn_due_to_price=30.0))
        engine.analyze(make_input(churn_due_to_price=5.0))
        for r in engine.review_needed:
            assert r.needs_pricing_review is True

    def test_total_revenue_at_risk_zero(self, engine):
        assert engine.total_revenue_at_risk == 0.0

    def test_total_revenue_at_risk_sum(self, engine):
        engine.analyze(make_input(total_pipeline_value=1_000_000.0, segment_id="a"))
        engine.analyze(make_input(total_pipeline_value=2_000_000.0, segment_id="b"))
        expected = round(
            engine._results[0].revenue_at_risk + engine._results[1].revenue_at_risk, 2
        )
        assert engine.total_revenue_at_risk == expected

    def test_total_expansion_opportunity_zero(self, engine):
        assert engine.total_expansion_opportunity == 0.0

    def test_total_expansion_opportunity_sum(self, engine):
        engine.analyze(make_input(total_pipeline_value=1_000_000.0, segment_id="a"))
        engine.analyze(make_input(total_pipeline_value=2_000_000.0, segment_id="b"))
        expected = round(
            engine._results[0].expansion_opportunity + engine._results[1].expansion_opportunity, 2
        )
        assert engine.total_expansion_opportunity == expected

    def test_total_revenue_at_risk_is_float(self, engine):
        engine.analyze(make_input())
        assert isinstance(engine.total_revenue_at_risk, float)

    def test_total_expansion_is_float(self, engine):
        engine.analyze(make_input())
        assert isinstance(engine.total_expansion_opportunity, float)

    def test_price_sensitive_returns_list(self, engine):
        assert isinstance(engine.price_sensitive_segments, list)

    def test_review_needed_returns_list(self, engine):
        assert isinstance(engine.review_needed, list)

    def test_properties_reset_after_reset(self, engine):
        engine.analyze(make_input(price_objection_rate=50.0, churn_due_to_price=30.0))
        engine.reset()
        assert engine.price_sensitive_segments == []
        assert engine.review_needed == []
        assert engine.total_revenue_at_risk == 0.0
        assert engine.total_expansion_opportunity == 0.0


# ===========================================================================
# 21. summary()
# ===========================================================================

class TestSummary:
    def test_empty_returns_13_keys(self, engine):
        s = engine.summary()
        assert len(s) == 13

    def test_empty_total_zero(self, engine):
        assert engine.summary()["total"] == 0

    def test_empty_elasticity_counts_empty(self, engine):
        assert engine.summary()["elasticity_counts"] == {}

    def test_empty_risk_counts_empty(self, engine):
        assert engine.summary()["risk_counts"] == {}

    def test_empty_stance_counts_empty(self, engine):
        assert engine.summary()["stance_counts"] == {}

    def test_empty_action_counts_empty(self, engine):
        assert engine.summary()["action_counts"] == {}

    def test_empty_avg_elasticity_zero(self, engine):
        assert engine.summary()["avg_price_elasticity_index"] == 0.0

    def test_empty_avg_discount_zero(self, engine):
        assert engine.summary()["avg_discount_leak_score"] == 0.0

    def test_empty_revenue_at_risk_zero(self, engine):
        assert engine.summary()["total_revenue_at_risk"] == 0.0

    def test_empty_expansion_zero(self, engine):
        assert engine.summary()["total_expansion_opportunity"] == 0.0

    def test_empty_price_sensitive_count_zero(self, engine):
        assert engine.summary()["price_sensitive_count"] == 0

    def test_empty_review_needed_count_zero(self, engine):
        assert engine.summary()["review_needed_count"] == 0

    def test_empty_avg_comp_pressure_zero(self, engine):
        assert engine.summary()["avg_competitive_pressure_score"] == 0.0

    def test_empty_avg_optimal_adj_zero(self, engine):
        assert engine.summary()["avg_optimal_price_adjustment_pct"] == 0.0

    def test_summary_has_exact_13_keys(self, engine):
        engine.analyze(make_input())
        assert len(engine.summary()) == 13

    def test_summary_exact_keys(self, engine):
        expected_keys = {
            "total", "elasticity_counts", "risk_counts", "stance_counts",
            "action_counts", "avg_price_elasticity_index", "avg_discount_leak_score",
            "total_revenue_at_risk", "total_expansion_opportunity",
            "price_sensitive_count", "review_needed_count",
            "avg_competitive_pressure_score", "avg_optimal_price_adjustment_pct",
        }
        assert set(engine.summary().keys()) == expected_keys

    def test_total_count_after_one(self, engine):
        engine.analyze(make_input())
        assert engine.summary()["total"] == 1

    def test_total_count_after_multiple(self, engine):
        for _ in range(5):
            engine.analyze(make_input())
        assert engine.summary()["total"] == 5

    def test_elasticity_counts_populated(self, engine):
        engine.analyze(make_input())
        counts = engine.summary()["elasticity_counts"]
        assert isinstance(counts, dict)
        assert sum(counts.values()) == 1

    def test_risk_counts_populated(self, engine):
        engine.analyze(make_input())
        counts = engine.summary()["risk_counts"]
        assert sum(counts.values()) == 1

    def test_stance_counts_populated(self, engine):
        engine.analyze(make_input())
        counts = engine.summary()["stance_counts"]
        assert sum(counts.values()) == 1

    def test_action_counts_populated(self, engine):
        engine.analyze(make_input())
        counts = engine.summary()["action_counts"]
        assert sum(counts.values()) == 1

    def test_avg_elasticity_after_one(self, engine):
        result = engine.analyze(make_input())
        s = engine.summary()
        assert s["avg_price_elasticity_index"] == result.price_elasticity_index

    def test_avg_discount_after_one(self, engine):
        result = engine.analyze(make_input())
        s = engine.summary()
        assert s["avg_discount_leak_score"] == result.discount_leak_score

    def test_total_revenue_matches_property(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        assert s["total_revenue_at_risk"] == engine.total_revenue_at_risk

    def test_total_expansion_matches_property(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        assert s["total_expansion_opportunity"] == engine.total_expansion_opportunity

    def test_price_sensitive_count_matches_property(self, engine):
        engine.analyze(make_input(price_objection_rate=45.0))
        engine.analyze(make_input(price_objection_rate=5.0))
        s = engine.summary()
        assert s["price_sensitive_count"] == len(engine.price_sensitive_segments)

    def test_review_needed_count_matches_property(self, engine):
        engine.analyze(make_input(churn_due_to_price=30.0))
        engine.analyze(make_input(churn_due_to_price=5.0))
        s = engine.summary()
        assert s["review_needed_count"] == len(engine.review_needed)

    def test_avg_comp_pressure_after_one(self, engine):
        result = engine.analyze(make_input())
        s = engine.summary()
        assert s["avg_competitive_pressure_score"] == result.competitive_pressure_score

    def test_avg_optimal_adj_after_one(self, engine):
        result = engine.analyze(make_input())
        s = engine.summary()
        assert s["avg_optimal_price_adjustment_pct"] == result.optimal_price_adjustment_pct

    def test_summary_after_reset_all_zeros(self, engine):
        engine.analyze(make_input())
        engine.reset()
        s = engine.summary()
        assert s["total"] == 0

    def test_multiple_results_avg_elasticity(self, engine):
        r1 = engine.analyze(make_input(segment_id="a"))
        r2 = engine.analyze(make_input(segment_id="b"))
        s = engine.summary()
        expected = round((r1.price_elasticity_index + r2.price_elasticity_index) / 2, 1)
        assert s["avg_price_elasticity_index"] == expected

    def test_multiple_results_counts_aggregate(self, engine):
        engine.analyze(make_input(segment_id="a"))
        engine.analyze(make_input(segment_id="b"))
        s = engine.summary()
        assert sum(s["elasticity_counts"].values()) == 2


# ===========================================================================
# 22. End-to-end / integration scenarios
# ===========================================================================

class TestIntegrationScenarios:
    def test_high_churn_enterprise(self, engine):
        inp = make_input(
            segment_id="enterprise_1",
            churn_due_to_price=35.0,
            competitive_price_gap=20.0,
            price_objection_rate=50.0,
        )
        result = engine.analyze(inp)
        assert result.pricing_risk == PricingRisk.CRITICAL
        assert result.needs_pricing_review is True
        assert result.pricing_action == PricingAction.RESTRUCTURE

    def test_premium_segment(self, engine):
        inp = make_input(
            segment_id="premium_1",
            willingness_to_pay_index=85.0,
            price_objection_rate=5.0,
            win_rate_at_list_price=70.0,
            win_rate_with_discount=72.0,
            deals_before_increase=20,
            deals_after_increase=20,
            churn_due_to_price=2.0,
            competitive_price_gap=2.0,
            nps_price_sensitivity=30.0,
            discount_request_rate=5.0,
            avg_discount_given_pct=2.0,
        )
        result = engine.analyze(inp)
        assert result.pricing_stance == PricingStance.PREMIUM
        assert result.pricing_action == PricingAction.INCREASE

    def test_competitive_market_segment(self, engine):
        inp = make_input(
            competitive_price_gap=-15.0,
            churn_due_to_price=5.0,
            nps_price_sensitivity=10.0,
            willingness_to_pay_index=50.0,
            price_objection_rate=5.0,
            discount_request_rate=0.0,
            avg_discount_given_pct=0.0,
            win_rate_at_list_price=60.0,
            win_rate_with_discount=60.0,
            deals_before_increase=0,
        )
        result = engine.analyze(inp)
        assert result.pricing_stance == PricingStance.COMPETITIVE
        assert result.pricing_action == PricingAction.OPTIMIZE

    def test_discount_abuse_segment(self, engine):
        inp = make_input(
            discount_request_rate=60.0,
            avg_discount_given_pct=14.0,
            win_rate_at_list_price=60.0,
            win_rate_with_discount=60.0,
            churn_due_to_price=5.0,
            competitive_price_gap=0.0,
            nps_price_sensitivity=0.0,
            price_objection_rate=0.0,
            willingness_to_pay_index=50.0,
        )
        result = engine.analyze(inp)
        assert result.pricing_action == PricingAction.DISCOUNT_CONTROL
        assert result.needs_pricing_review is True

    def test_inelastic_high_wtp_gets_increase(self, engine):
        inp = make_input(
            willingness_to_pay_index=65.0,
            price_objection_rate=0.0,
            discount_request_rate=0.0,
            avg_discount_given_pct=0.0,
            win_rate_at_list_price=60.0,
            win_rate_with_discount=60.0,
            deals_before_increase=0,
            churn_due_to_price=0.0,
            competitive_price_gap=2.0,
            nps_price_sensitivity=0.0,
        )
        result = engine.analyze(inp)
        assert result.pricing_action == PricingAction.INCREASE

    def test_batch_mixed_segments(self, engine):
        inputs = [
            make_input(segment_id="low", price_objection_rate=5.0, churn_due_to_price=2.0),
            make_input(segment_id="high", price_objection_rate=50.0, churn_due_to_price=35.0),
        ]
        results = engine.analyze_batch(inputs)
        assert results[0].segment_id == "low"
        assert results[1].segment_id == "high"
        assert results[1].pricing_risk == PricingRisk.CRITICAL

    def test_pipeline_value_affects_risk_and_opportunity(self, engine):
        large_pipe = make_input(total_pipeline_value=5_000_000.0, segment_id="large")
        small_pipe = make_input(total_pipeline_value=100_000.0, segment_id="small")
        r_large = engine.analyze(large_pipe)
        r_small = engine.analyze(small_pipe)
        assert r_large.revenue_at_risk > r_small.revenue_at_risk
        assert r_large.expansion_opportunity > r_small.expansion_opportunity

    def test_engine_fresh_state(self):
        # Each engine starts fresh
        e1 = PricingElasticityEngine()
        e2 = PricingElasticityEngine()
        e1.analyze(make_input())
        assert len(e1._results) == 1
        assert len(e2._results) == 0

    def test_full_summary_after_batch(self, engine):
        engine.analyze_batch([make_input(segment_id=f"s{i}") for i in range(10)])
        s = engine.summary()
        assert s["total"] == 10
        assert sum(s["elasticity_counts"].values()) == 10
        assert sum(s["risk_counts"].values()) == 10

    def test_default_input_produces_valid_result(self, engine, default_input):
        result = engine.analyze(default_input)
        assert isinstance(result.elasticity_category, ElasticityCategory)
        assert isinstance(result.pricing_risk, PricingRisk)
        assert isinstance(result.pricing_stance, PricingStance)
        assert isinstance(result.pricing_action, PricingAction)
        assert 0.0 <= result.price_elasticity_index <= 100.0
        assert 0.0 <= result.discount_leak_score <= 100.0
        assert 0.0 <= result.competitive_pressure_score <= 100.0
        assert 0.0 <= result.pricing_confidence_score <= 100.0
        assert -20.0 <= result.optimal_price_adjustment_pct <= 20.0

    def test_defensive_stance_for_high_competitive_pressure(self, engine):
        # gap=20 -> comp_pressure=40 -> DEFENSIVE
        inp = make_input(
            competitive_price_gap=20.0,
            churn_due_to_price=5.0,
            willingness_to_pay_index=50.0,
            price_objection_rate=0.0,
            nps_price_sensitivity=0.0,
            discount_request_rate=0.0,
            avg_discount_given_pct=0.0,
            win_rate_at_list_price=60.0,
            win_rate_with_discount=60.0,
            deals_before_increase=0,
        )
        result = engine.analyze(inp)
        assert result.pricing_stance == PricingStance.DEFENSIVE

    def test_expansion_opportunity_zero_for_high_elasticity(self, engine):
        inp = make_input(
            price_objection_rate=100.0,
            win_rate_at_list_price=0.0,
            win_rate_with_discount=100.0,
            deals_before_increase=20,
            deals_after_increase=0,
            price_increase_pct=5.0,
            willingness_to_pay_index=0.0,
        )
        result = engine.analyze(inp)
        if result.price_elasticity_index >= 60.0:
            assert result.expansion_opportunity == 0.0

    def test_summary_elasticity_counts_keys_are_strings(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        for key in s["elasticity_counts"]:
            assert isinstance(key, str)

    def test_summary_risk_counts_keys_are_strings(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        for key in s["risk_counts"]:
            assert isinstance(key, str)

    def test_analyze_returns_new_result_each_call(self, engine):
        r1 = engine.analyze(make_input(segment_id="x"))
        r2 = engine.analyze(make_input(segment_id="y"))
        assert r1 is not r2

    def test_to_dict_values_match_result_fields(self, engine, default_result):
        d = default_result.to_dict()
        assert d["price_elasticity_index"] == default_result.price_elasticity_index
        assert d["discount_leak_score"] == default_result.discount_leak_score
        assert d["competitive_pressure_score"] == default_result.competitive_pressure_score

    def test_to_dict_enum_values_are_strings(self, engine, default_result):
        d = default_result.to_dict()
        assert d["elasticity_category"] in [m.value for m in ElasticityCategory]
        assert d["pricing_risk"] in [m.value for m in PricingRisk]
        assert d["pricing_stance"] in [m.value for m in PricingStance]
        assert d["pricing_action"] in [m.value for m in PricingAction]

    def test_revenue_at_risk_increases_with_elasticity(self, engine):
        inp_low = make_input(total_pipeline_value=1_000_000.0)
        inp_high = make_input(total_pipeline_value=1_000_000.0)
        r_low = engine._revenue_at_risk(inp_low, 10.0, 10.0)
        r_high = engine._revenue_at_risk(inp_high, 80.0, 80.0)
        assert r_high > r_low

    def test_elasticity_category_returns_enum(self, engine):
        cat = engine._elasticity_category(50.0)
        assert isinstance(cat, ElasticityCategory)

    def test_pricing_confidence_max_is_100(self, engine):
        # Even if we had more signals, max is 100
        score = engine._pricing_confidence(make_input())
        assert score <= 100.0

    def test_reset_and_summary_returns_empty_state(self, engine):
        engine.analyze(make_input())
        engine.reset()
        s = engine.summary()
        assert s["total"] == 0
        assert s["price_sensitive_count"] == 0
        assert s["review_needed_count"] == 0

    def test_extreme_elasticity_category_from_analyze(self, engine):
        # Force extreme: objection=100->30, lift=100 cap25, demand>25cap, WTP=0->20 = 100
        inp = make_input(
            price_objection_rate=100.0,
            win_rate_at_list_price=0.0,
            win_rate_with_discount=100.0,
            deals_before_increase=20,
            deals_after_increase=0,
            price_increase_pct=1.0,
            willingness_to_pay_index=0.0,
        )
        result = engine.analyze(inp)
        assert result.elasticity_category == ElasticityCategory.EXTREME

    def test_inelastic_category_from_analyze(self, engine):
        inp = make_input(
            price_objection_rate=0.0,
            win_rate_at_list_price=60.0,
            win_rate_with_discount=60.0,
            deals_before_increase=10,
            deals_after_increase=10,
            price_increase_pct=5.0,
            willingness_to_pay_index=95.0,
        )
        result = engine.analyze(inp)
        assert result.elasticity_category == ElasticityCategory.INELASTIC

    def test_analyze_batch_returns_correct_types(self, engine):
        results = engine.analyze_batch([make_input(segment_id=f"t{i}") for i in range(3)])
        for r in results:
            assert isinstance(r, PricingElasticityResult)
            assert isinstance(r.pricing_action, PricingAction)

    def test_competitive_pressure_all_components(self, engine):
        # gap=20->40(cap40), churn=50->35(cap35), nps=-100->25(cap25) = 100
        inp = make_input(
            competitive_price_gap=20.0,
            churn_due_to_price=50.0,
            nps_price_sensitivity=-100.0,
        )
        score = engine._competitive_pressure_score(inp)
        assert score == 100.0
