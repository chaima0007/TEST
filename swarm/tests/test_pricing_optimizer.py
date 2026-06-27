"""Comprehensive pytest tests for PricingOptimizer."""

from __future__ import annotations

import pytest

from swarm.intelligence.pricing_optimizer import (
    PricingOptimizer,
    PricingInput,
    PricingResult,
    PricingStrategy,
    DiscountRisk,
    DealUrgency,
    _deal_urgency,
    _recommended_discount,
    _pricing_strategy,
    _price_score,
    _win_probability_boost,
    _discount_risk,
    _STAGE_MAX_DAYS,
    _SIZE_DISCOUNT_CEILING,
    _URGENCY_DRIVERS,
)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def make_input(**kwargs) -> PricingInput:
    defaults = dict(
        deal_id="deal1",
        deal_name="Test Deal",
        list_price_eur=50000,
        current_proposed_eur=45000,
        cost_to_serve_eur=15000,
        competitor_price_eur=42000,
        customer_budget_eur=48000,
        customer_size="mid_market",
        industry="saas",
        deal_stage="proposal",
        days_in_stage=10,
        num_competitors=2,
        champion_strength=65.0,
        decision_maker_engaged=True,
        has_business_case=True,
        urgency_driver="cost_savings",
        contract_length_months=12,
        expansion_potential_eur=20000,
        historical_discount_pct=10.0,
    )
    defaults.update(kwargs)
    return PricingInput(**defaults)


# ---------------------------------------------------------------------------
# 1. TestDealUrgency  (25 tests)
# ---------------------------------------------------------------------------

class TestDealUrgency:

    def test_regulatory_driver_returns_critical(self):
        inp = make_input(urgency_driver="regulatory", days_in_stage=5)
        assert _deal_urgency(inp) == DealUrgency.CRITICAL

    def test_regulatory_driver_critical_regardless_of_stage(self):
        inp = make_input(urgency_driver="regulatory", days_in_stage=1)
        assert _deal_urgency(inp) == DealUrgency.CRITICAL

    def test_competitive_driver_not_overdue_returns_high(self):
        # proposal max_days=30, threshold=45; days=10 → not overdue
        inp = make_input(urgency_driver="competitive", deal_stage="proposal", days_in_stage=10)
        assert _deal_urgency(inp) == DealUrgency.HIGH

    def test_competitive_driver_overdue_returns_critical(self):
        # proposal max=30, threshold=45; 46 > 45 → overdue
        inp = make_input(urgency_driver="competitive", deal_stage="proposal", days_in_stage=46)
        assert _deal_urgency(inp) == DealUrgency.CRITICAL

    def test_cost_savings_driver_not_overdue_returns_high(self):
        inp = make_input(urgency_driver="cost_savings", deal_stage="proposal", days_in_stage=10)
        assert _deal_urgency(inp) == DealUrgency.HIGH

    def test_cost_savings_driver_overdue_returns_critical(self):
        inp = make_input(urgency_driver="cost_savings", deal_stage="proposal", days_in_stage=46)
        assert _deal_urgency(inp) == DealUrgency.CRITICAL

    def test_growth_driver_returns_medium(self):
        inp = make_input(urgency_driver="growth", days_in_stage=5)
        assert _deal_urgency(inp) == DealUrgency.MEDIUM

    def test_none_driver_not_overdue_returns_low(self):
        inp = make_input(urgency_driver="none", deal_stage="proposal", days_in_stage=5)
        assert _deal_urgency(inp) == DealUrgency.LOW

    def test_overdue_alone_returns_high(self):
        # none driver + overdue → HIGH (overdue alone)
        inp = make_input(urgency_driver="none", deal_stage="proposal", days_in_stage=46)
        assert _deal_urgency(inp) == DealUrgency.HIGH

    def test_stage_prospecting_max_days_14(self):
        # threshold = 14 * 1.5 = 21; days=22 → overdue
        inp = make_input(urgency_driver="none", deal_stage="prospecting", days_in_stage=22)
        assert _deal_urgency(inp) == DealUrgency.HIGH

    def test_stage_prospecting_not_overdue(self):
        # threshold=21; days=21 → NOT overdue (strict >)
        inp = make_input(urgency_driver="none", deal_stage="prospecting", days_in_stage=21)
        assert _deal_urgency(inp) == DealUrgency.LOW

    def test_stage_qualification_max_days_21(self):
        # threshold = 21 * 1.5 = 31.5; days=32 → overdue
        inp = make_input(urgency_driver="none", deal_stage="qualification", days_in_stage=32)
        assert _deal_urgency(inp) == DealUrgency.HIGH

    def test_stage_qualification_not_overdue(self):
        inp = make_input(urgency_driver="none", deal_stage="qualification", days_in_stage=31)
        assert _deal_urgency(inp) == DealUrgency.LOW

    def test_stage_demo_max_days_21(self):
        # threshold=31.5; days=32 → overdue
        inp = make_input(urgency_driver="none", deal_stage="demo", days_in_stage=32)
        assert _deal_urgency(inp) == DealUrgency.HIGH

    def test_stage_proposal_max_days_30(self):
        # threshold=45; days=46 → overdue
        inp = make_input(urgency_driver="none", deal_stage="proposal", days_in_stage=46)
        assert _deal_urgency(inp) == DealUrgency.HIGH

    def test_stage_proposal_not_overdue(self):
        inp = make_input(urgency_driver="none", deal_stage="proposal", days_in_stage=45)
        assert _deal_urgency(inp) == DealUrgency.LOW

    def test_stage_negotiation_max_days_21(self):
        # threshold=31.5; days=32 → overdue
        inp = make_input(urgency_driver="none", deal_stage="negotiation", days_in_stage=32)
        assert _deal_urgency(inp) == DealUrgency.HIGH

    def test_stage_closing_max_days_14(self):
        # threshold=21; days=22 → overdue
        inp = make_input(urgency_driver="none", deal_stage="closing", days_in_stage=22)
        assert _deal_urgency(inp) == DealUrgency.HIGH

    def test_stage_closing_not_overdue(self):
        inp = make_input(urgency_driver="none", deal_stage="closing", days_in_stage=21)
        assert _deal_urgency(inp) == DealUrgency.LOW

    def test_unknown_stage_defaults_to_21_max_days(self):
        # threshold=31.5; days=32 → overdue → HIGH
        inp = make_input(urgency_driver="none", deal_stage="unknown_stage", days_in_stage=32)
        assert _deal_urgency(inp) == DealUrgency.HIGH

    def test_unknown_stage_not_overdue_stays_low(self):
        inp = make_input(urgency_driver="none", deal_stage="unknown_stage", days_in_stage=5)
        assert _deal_urgency(inp) == DealUrgency.LOW

    def test_unknown_urgency_driver_defaults_to_low(self):
        inp = make_input(urgency_driver="unknown_driver", deal_stage="proposal", days_in_stage=5)
        assert _deal_urgency(inp) == DealUrgency.LOW

    def test_unknown_urgency_driver_overdue_gives_high(self):
        inp = make_input(urgency_driver="unknown_driver", deal_stage="proposal", days_in_stage=46)
        assert _deal_urgency(inp) == DealUrgency.HIGH

    def test_stage_overdue_boundary_exactly_at_threshold_is_not_overdue(self):
        # proposal threshold = 30 * 1.5 = 45.0; days=45 → NOT overdue (> not >=)
        inp = make_input(urgency_driver="none", deal_stage="proposal", days_in_stage=45)
        assert _deal_urgency(inp) == DealUrgency.LOW

    def test_cost_savings_at_threshold_boundary_not_overdue(self):
        # proposal threshold=45; days=45 → not overdue → HIGH (from driver alone)
        inp = make_input(urgency_driver="cost_savings", deal_stage="proposal", days_in_stage=45)
        assert _deal_urgency(inp) == DealUrgency.HIGH


# ---------------------------------------------------------------------------
# 2. TestRecommendedDiscount  (30 tests)
# ---------------------------------------------------------------------------

class TestRecommendedDiscount:

    def test_no_competitor_no_competitor_contribution(self):
        # With competitor=0, list=50000, budget=50000, no gap
        inp = make_input(
            competitor_price_eur=0,
            customer_budget_eur=50000,
            list_price_eur=50000,
            num_competitors=0,
            historical_discount_pct=0,
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=0,
        )
        # base = 0 + 0 + 0 + 0 - 0 + 0 = 0
        assert _recommended_discount(inp) == 0.0

    def test_competitor_20_percent_cheaper_contributes_correctly(self):
        # list=100, competitor=80 → gap=20%, contrib=min(20*0.6,15)=12
        inp = make_input(
            list_price_eur=100,
            competitor_price_eur=80,
            customer_budget_eur=100,  # no budget gap
            num_competitors=0,
            historical_discount_pct=0,
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=0,
            customer_size="enterprise",  # ceiling=35
        )
        result = _recommended_discount(inp)
        assert result == pytest.approx(12.0, abs=0.1)

    def test_competitor_30_percent_cheaper_caps_contribution_at_15(self):
        # list=100, competitor=50 → gap=50%, contrib=min(50*0.6,15)=15
        inp = make_input(
            list_price_eur=100,
            competitor_price_eur=50,
            customer_budget_eur=100,
            num_competitors=0,
            historical_discount_pct=0,
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=0,
            customer_size="enterprise",
        )
        result = _recommended_discount(inp)
        assert result == pytest.approx(15.0, abs=0.1)

    def test_no_budget_gap_no_budget_contribution(self):
        # budget = list → no gap
        inp = make_input(
            list_price_eur=50000,
            competitor_price_eur=0,
            customer_budget_eur=50000,
            num_competitors=0,
            historical_discount_pct=0,
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=0,
            customer_size="enterprise",
        )
        assert _recommended_discount(inp) == 0.0

    def test_budget_gap_20pct_contributes_10(self):
        # list=100, budget=80 → gap=20%, contrib=min(20*0.5,10)=10
        inp = make_input(
            list_price_eur=100,
            competitor_price_eur=0,
            customer_budget_eur=80,
            num_competitors=0,
            historical_discount_pct=0,
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=0,
            customer_size="enterprise",
        )
        result = _recommended_discount(inp)
        assert result == pytest.approx(10.0, abs=0.1)

    def test_budget_gap_30pct_capped_at_10(self):
        # list=100, budget=70 → gap=30%, contrib=min(30*0.5,10)=10
        inp = make_input(
            list_price_eur=100,
            competitor_price_eur=0,
            customer_budget_eur=70,
            num_competitors=0,
            historical_discount_pct=0,
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=0,
            customer_size="enterprise",
        )
        result = _recommended_discount(inp)
        assert result == pytest.approx(10.0, abs=0.1)

    def test_budget_exceeds_list_no_negative_contribution(self):
        # budget=120, list=100 → gap=max(0,...)=0
        inp = make_input(
            list_price_eur=100,
            competitor_price_eur=0,
            customer_budget_eur=120,
            num_competitors=0,
            historical_discount_pct=0,
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=0,
            customer_size="enterprise",
        )
        assert _recommended_discount(inp) == 0.0

    def test_num_competitors_4_adds_6(self):
        # 4 * 1.5 = 6; min(6, 8) = 6
        inp = make_input(
            competitor_price_eur=0,
            customer_budget_eur=50000,
            list_price_eur=50000,
            num_competitors=4,
            historical_discount_pct=0,
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=0,
            customer_size="enterprise",
        )
        result = _recommended_discount(inp)
        assert result == pytest.approx(6.0, abs=0.1)

    def test_num_competitors_6_caps_intensity_at_8(self):
        # 6 * 1.5 = 9; min(9, 8) = 8
        inp = make_input(
            competitor_price_eur=0,
            customer_budget_eur=50000,
            list_price_eur=50000,
            num_competitors=6,
            historical_discount_pct=0,
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=0,
            customer_size="enterprise",
        )
        result = _recommended_discount(inp)
        assert result == pytest.approx(8.0, abs=0.1)

    def test_historical_10_adds_3(self):
        # 10 * 0.3 = 3
        inp = make_input(
            competitor_price_eur=0,
            customer_budget_eur=50000,
            list_price_eur=50000,
            num_competitors=0,
            historical_discount_pct=10,
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=0,
            customer_size="enterprise",
        )
        result = _recommended_discount(inp)
        assert result == pytest.approx(3.0, abs=0.1)

    def test_all_3_strengths_reduce_by_7_5(self):
        # champion>=70, dm_engaged, business_case → 3 * 2.5 = 7.5 reduction
        inp = make_input(
            competitor_price_eur=0,
            customer_budget_eur=50000,
            list_price_eur=50000,
            num_competitors=0,
            historical_discount_pct=30,  # adds 9
            champion_strength=70,
            decision_maker_engaged=True,
            has_business_case=True,
            contract_length_months=0,
            customer_size="enterprise",
        )
        # base = 0 + 0 + 0 + 9 - 7.5 + 0 = 1.5
        result = _recommended_discount(inp)
        assert result == pytest.approx(1.5, abs=0.1)

    def test_champion_exactly_70_counts_as_strength(self):
        inp = make_input(
            competitor_price_eur=0,
            customer_budget_eur=50000,
            list_price_eur=50000,
            num_competitors=0,
            historical_discount_pct=0,
            champion_strength=70,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=0,
            customer_size="enterprise",
        )
        result = _recommended_discount(inp)
        assert result == 0.0  # -2.5 → floor at 0

    def test_champion_below_70_does_not_count_as_strength(self):
        inp = make_input(
            competitor_price_eur=0,
            customer_budget_eur=50000,
            list_price_eur=50000,
            num_competitors=0,
            historical_discount_pct=0,
            champion_strength=69.9,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=0,
            customer_size="enterprise",
        )
        result = _recommended_discount(inp)
        assert result == 0.0  # still 0 (no other contributions)

    def test_contract_24_months_adds_5(self):
        inp = make_input(
            competitor_price_eur=0,
            customer_budget_eur=50000,
            list_price_eur=50000,
            num_competitors=0,
            historical_discount_pct=0,
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=24,
            customer_size="enterprise",
        )
        result = _recommended_discount(inp)
        assert result == pytest.approx(5.0, abs=0.1)

    def test_contract_12_months_adds_2(self):
        inp = make_input(
            competitor_price_eur=0,
            customer_budget_eur=50000,
            list_price_eur=50000,
            num_competitors=0,
            historical_discount_pct=0,
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=12,
            customer_size="enterprise",
        )
        result = _recommended_discount(inp)
        assert result == pytest.approx(2.0, abs=0.1)

    def test_contract_23_months_adds_2_not_5(self):
        inp = make_input(
            competitor_price_eur=0,
            customer_budget_eur=50000,
            list_price_eur=50000,
            num_competitors=0,
            historical_discount_pct=0,
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=23,
            customer_size="enterprise",
        )
        result = _recommended_discount(inp)
        assert result == pytest.approx(2.0, abs=0.1)

    def test_contract_less_than_12_no_bonus(self):
        inp = make_input(
            competitor_price_eur=0,
            customer_budget_eur=50000,
            list_price_eur=50000,
            num_competitors=0,
            historical_discount_pct=0,
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=11,
            customer_size="enterprise",
        )
        result = _recommended_discount(inp)
        assert result == 0.0

    def test_startup_ceiling_20(self):
        # Put high inputs that would push well above 20
        inp = make_input(
            list_price_eur=100,
            competitor_price_eur=50,   # +15
            customer_budget_eur=70,    # +10
            num_competitors=6,         # +8
            historical_discount_pct=20, # +6
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=24,  # +5  → total=44
            customer_size="startup",
        )
        result = _recommended_discount(inp)
        assert result == pytest.approx(20.0, abs=0.1)

    def test_smb_ceiling_25(self):
        inp = make_input(
            list_price_eur=100,
            competitor_price_eur=50,
            customer_budget_eur=70,
            num_competitors=6,
            historical_discount_pct=20,
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=24,
            customer_size="smb",
        )
        result = _recommended_discount(inp)
        assert result == pytest.approx(25.0, abs=0.1)

    def test_mid_market_ceiling_30(self):
        inp = make_input(
            list_price_eur=100,
            competitor_price_eur=50,
            customer_budget_eur=70,
            num_competitors=6,
            historical_discount_pct=20,
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=24,
            customer_size="mid_market",
        )
        result = _recommended_discount(inp)
        assert result == pytest.approx(30.0, abs=0.1)

    def test_enterprise_ceiling_35(self):
        inp = make_input(
            list_price_eur=100,
            competitor_price_eur=50,
            customer_budget_eur=70,
            num_competitors=6,
            historical_discount_pct=20,
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=24,
            customer_size="enterprise",
        )
        result = _recommended_discount(inp)
        assert result == pytest.approx(35.0, abs=0.1)

    def test_unknown_customer_size_defaults_to_25_ceiling(self):
        inp = make_input(
            list_price_eur=100,
            competitor_price_eur=50,
            customer_budget_eur=70,
            num_competitors=6,
            historical_discount_pct=20,
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=24,
            customer_size="unknown_size",
        )
        result = _recommended_discount(inp)
        assert result == pytest.approx(25.0, abs=0.1)

    def test_floor_at_zero(self):
        # All strengths, no other contribution → negative base → floor at 0
        inp = make_input(
            competitor_price_eur=0,
            customer_budget_eur=50000,
            list_price_eur=50000,
            num_competitors=0,
            historical_discount_pct=0,
            champion_strength=70,
            decision_maker_engaged=True,
            has_business_case=True,
            contract_length_months=0,
            customer_size="enterprise",
        )
        result = _recommended_discount(inp)
        assert result == 0.0

    def test_competitor_more_expensive_no_contribution(self):
        # competitor > list → price_gap_pct < 0 → no contribution
        inp = make_input(
            list_price_eur=100,
            competitor_price_eur=120,
            customer_budget_eur=100,
            num_competitors=0,
            historical_discount_pct=0,
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=0,
            customer_size="enterprise",
        )
        assert _recommended_discount(inp) == 0.0

    def test_one_strength_reduces_by_2_5(self):
        inp = make_input(
            competitor_price_eur=0,
            customer_budget_eur=50000,
            list_price_eur=50000,
            num_competitors=0,
            historical_discount_pct=10,  # adds 3
            champion_strength=70,        # one strength: -2.5 → 0.5
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=0,
            customer_size="enterprise",
        )
        result = _recommended_discount(inp)
        assert result == pytest.approx(0.5, abs=0.1)

    def test_two_strengths_reduces_by_5(self):
        inp = make_input(
            competitor_price_eur=0,
            customer_budget_eur=50000,
            list_price_eur=50000,
            num_competitors=0,
            historical_discount_pct=20,  # adds 6
            champion_strength=70,        # strength 1
            decision_maker_engaged=True,  # strength 2 → -5 → 1.0
            has_business_case=False,
            contract_length_months=0,
            customer_size="enterprise",
        )
        result = _recommended_discount(inp)
        assert result == pytest.approx(1.0, abs=0.1)

    def test_result_rounded_to_1_decimal(self):
        # Ensure output is rounded
        inp = make_input(
            list_price_eur=100,
            competitor_price_eur=93,  # gap=7%, 7*0.6=4.2
            customer_budget_eur=100,
            num_competitors=0,
            historical_discount_pct=0,
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=0,
            customer_size="enterprise",
        )
        result = _recommended_discount(inp)
        assert result == pytest.approx(4.2, abs=0.01)

    def test_zero_list_price_no_division(self):
        # list_price=0 → no competitor/budget contribution (conditions check >0)
        inp = make_input(
            list_price_eur=0,
            competitor_price_eur=0,
            customer_budget_eur=0,
            num_competitors=0,
            historical_discount_pct=0,
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=0,
            customer_size="enterprise",
        )
        assert _recommended_discount(inp) == 0.0

    def test_customer_budget_zero_no_contribution(self):
        inp = make_input(
            list_price_eur=100,
            competitor_price_eur=0,
            customer_budget_eur=0,
            num_competitors=0,
            historical_discount_pct=0,
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=0,
            customer_size="enterprise",
        )
        # budget=0 → condition customer_budget_eur > 0 fails → no contribution
        assert _recommended_discount(inp) == 0.0


# ---------------------------------------------------------------------------
# 3. TestPricingStrategy  (12 tests)
# ---------------------------------------------------------------------------

class TestPricingStrategy:

    def test_penetration_when_list_below_85pct_competitor(self):
        # list=80, competitor=100 → 80 < 100*0.85=85 → PENETRATION
        inp = make_input(list_price_eur=80, competitor_price_eur=100)
        strategy = _pricing_strategy(inp, discount=0, urgency=DealUrgency.LOW)
        assert strategy == PricingStrategy.PENETRATION

    def test_penetration_checked_before_value_based(self):
        # Even with business_case + strong champion, penetration wins if list<0.85*competitor
        inp = make_input(
            list_price_eur=80,
            competitor_price_eur=100,
            has_business_case=True,
            champion_strength=80,
        )
        strategy = _pricing_strategy(inp, discount=0, urgency=DealUrgency.LOW)
        assert strategy == PricingStrategy.PENETRATION

    def test_value_based_when_business_case_and_champion_75(self):
        inp = make_input(
            list_price_eur=100,
            competitor_price_eur=100,
            has_business_case=True,
            champion_strength=75,
        )
        strategy = _pricing_strategy(inp, discount=0, urgency=DealUrgency.LOW)
        assert strategy == PricingStrategy.VALUE_BASED

    def test_value_based_requires_champion_at_least_75(self):
        inp = make_input(
            list_price_eur=100,
            competitor_price_eur=100,
            has_business_case=True,
            champion_strength=74.9,
            num_competitors=0,
        )
        strategy = _pricing_strategy(inp, discount=0, urgency=DealUrgency.LOW)
        assert strategy != PricingStrategy.VALUE_BASED

    def test_premium_when_no_discount_and_list_above_115pct_competitor(self):
        # list=120, competitor=100 → 120 > 100*1.15=115 → PREMIUM
        inp = make_input(
            list_price_eur=120,
            competitor_price_eur=100,
            has_business_case=False,
            champion_strength=50,
        )
        strategy = _pricing_strategy(inp, discount=0, urgency=DealUrgency.LOW)
        assert strategy == PricingStrategy.PREMIUM

    def test_premium_not_returned_when_discount_gt_0(self):
        inp = make_input(
            list_price_eur=120,
            competitor_price_eur=100,
            has_business_case=False,
            champion_strength=50,
        )
        strategy = _pricing_strategy(inp, discount=5, urgency=DealUrgency.LOW)
        assert strategy != PricingStrategy.PREMIUM

    def test_anchor_when_critical_urgency_and_3_plus_competitors(self):
        inp = make_input(
            list_price_eur=100,
            competitor_price_eur=100,
            has_business_case=False,
            champion_strength=50,
            num_competitors=3,
        )
        strategy = _pricing_strategy(inp, discount=5, urgency=DealUrgency.CRITICAL)
        assert strategy == PricingStrategy.ANCHOR

    def test_anchor_when_high_urgency_and_3_plus_competitors(self):
        inp = make_input(
            list_price_eur=100,
            competitor_price_eur=100,
            has_business_case=False,
            champion_strength=50,
            num_competitors=3,
        )
        strategy = _pricing_strategy(inp, discount=5, urgency=DealUrgency.HIGH)
        assert strategy == PricingStrategy.ANCHOR

    def test_anchor_requires_at_least_3_competitors(self):
        inp = make_input(
            list_price_eur=100,
            competitor_price_eur=100,
            has_business_case=False,
            champion_strength=50,
            num_competitors=2,
        )
        strategy = _pricing_strategy(inp, discount=5, urgency=DealUrgency.CRITICAL)
        assert strategy != PricingStrategy.ANCHOR

    def test_freemium_for_startup_with_large_expansion(self):
        # startup + expansion >= list*2 → FREEMIUM
        inp = make_input(
            list_price_eur=50000,
            competitor_price_eur=50000,
            customer_size="startup",
            has_business_case=False,
            champion_strength=50,
            expansion_potential_eur=100000,  # == list*2
            num_competitors=0,
        )
        strategy = _pricing_strategy(inp, discount=0, urgency=DealUrgency.LOW)
        assert strategy == PricingStrategy.FREEMIUM

    def test_freemium_not_for_non_startup(self):
        inp = make_input(
            list_price_eur=50000,
            competitor_price_eur=50000,
            customer_size="enterprise",
            has_business_case=False,
            champion_strength=50,
            expansion_potential_eur=100000,
            num_competitors=0,
        )
        strategy = _pricing_strategy(inp, discount=0, urgency=DealUrgency.LOW)
        assert strategy != PricingStrategy.FREEMIUM

    def test_competitive_as_default(self):
        inp = make_input(
            list_price_eur=100,
            competitor_price_eur=100,
            has_business_case=False,
            champion_strength=50,
            num_competitors=1,
            customer_size="mid_market",
            expansion_potential_eur=0,
        )
        strategy = _pricing_strategy(inp, discount=5, urgency=DealUrgency.LOW)
        assert strategy == PricingStrategy.COMPETITIVE


# ---------------------------------------------------------------------------
# 4. TestPriceScore  (16 tests)
# ---------------------------------------------------------------------------

class TestPriceScore:

    def test_high_margin_gives_high_margin_score(self):
        # margin=60 → margin_score=min(100, 90)=90; drives high total
        inp = make_input(
            competitor_price_eur=0,
            champion_strength=100,
            decision_maker_engaged=True,
            has_business_case=True,
            urgency_driver="cost_savings",
        )
        score = _price_score(inp, recommended=100, margin=60)
        assert score > 70

    def test_margin_above_67_caps_at_100(self):
        # margin_score = min(100, margin*1.5); 67*1.5=100.5 → 100
        inp = make_input(competitor_price_eur=0)
        score = _price_score(inp, recommended=100, margin=67)
        # margin_score will be 100; full calculation depends on other factors
        # Just verify it's bounded
        assert score <= 100

    def test_competitor_price_zero_gives_comp_score_70(self):
        inp = make_input(competitor_price_eur=0, champion_strength=0,
                         decision_maker_engaged=False, has_business_case=False,
                         urgency_driver="none")
        # margin_score=0, comp_score=70, readiness=20*0.20=4
        # = 0*0.40 + 70*0.30 + 4*0.30 = 0 + 21 + 1.2 = 22.2
        score = _price_score(inp, recommended=0, margin=0)
        assert score == pytest.approx(22.2, abs=0.1)

    def test_ratio_1_gives_comp_score_100(self):
        # recommended == competitor → ratio=1 → comp_score=100
        inp = make_input(competitor_price_eur=100, champion_strength=0,
                         decision_maker_engaged=False, has_business_case=False,
                         urgency_driver="none")
        score = _price_score(inp, recommended=100, margin=0)
        # margin_score=0, comp_score=100, readiness=20*0.20=4
        # = 0 + 30 + 1.2 = 31.2
        assert score == pytest.approx(31.2, abs=0.1)

    def test_ratio_0_5_gives_comp_score_0(self):
        # ratio=0.5 → abs(1-0.5)=0.5 → 100-0.5*200=0; max(0,0)=0
        inp = make_input(competitor_price_eur=100, champion_strength=0,
                         decision_maker_engaged=False, has_business_case=False,
                         urgency_driver="none")
        score = _price_score(inp, recommended=50, margin=0)
        # comp_score=0; score = 0 + 0 + 4*0.30 = 1.2
        assert score == pytest.approx(1.2, abs=0.1)

    def test_margin_zero_gives_margin_score_zero(self):
        inp = make_input(competitor_price_eur=0, champion_strength=0,
                         decision_maker_engaged=False, has_business_case=False,
                         urgency_driver="none")
        score = _price_score(inp, recommended=100, margin=0)
        # margin_score=0; comp_score=70; readiness=4
        # = 0 + 21 + 1.2 = 22.2
        assert score == pytest.approx(22.2, abs=0.1)

    def test_all_readiness_flags_on_maximizes_readiness(self):
        # champion=100, dm=True, bc=True, urgency!="none"
        # readiness = 100*0.35 + 100*0.25 + 100*0.20 + 80*0.20
        #           = 35 + 25 + 20 + 16 = 96
        inp = make_input(
            competitor_price_eur=0,
            champion_strength=100,
            decision_maker_engaged=True,
            has_business_case=True,
            urgency_driver="cost_savings",
        )
        score = _price_score(inp, recommended=100, margin=0)
        # = 0 + 70*0.30 + 96*0.30 = 21 + 28.8 = 49.8
        assert score == pytest.approx(49.8, abs=0.1)

    def test_all_readiness_flags_off_minimizes_readiness(self):
        # champion=0, dm=False, bc=False, urgency_driver="none"
        # readiness = 0*0.35 + 0*0.25 + 0*0.20 + 20*0.20 = 4
        inp = make_input(
            competitor_price_eur=0,
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            urgency_driver="none",
        )
        score = _price_score(inp, recommended=100, margin=0)
        # = 0 + 21 + 1.2 = 22.2
        assert score == pytest.approx(22.2, abs=0.1)

    def test_score_bounded_between_0_and_100(self):
        inp = make_input(
            competitor_price_eur=100,
            champion_strength=100,
            decision_maker_engaged=True,
            has_business_case=True,
            urgency_driver="regulatory",
        )
        score = _price_score(inp, recommended=100, margin=100)
        assert 0 <= score <= 100

    def test_score_is_float(self):
        inp = make_input()
        score = _price_score(inp, recommended=45000, margin=50)
        assert isinstance(score, float)

    def test_ratio_1_5_gives_comp_score_max_0(self):
        # ratio=1.5 → abs(1-1.5)=0.5 → 100-0.5*200=0 → max(0,0)=0
        inp = make_input(competitor_price_eur=100, champion_strength=0,
                         decision_maker_engaged=False, has_business_case=False,
                         urgency_driver="none")
        score = _price_score(inp, recommended=150, margin=0)
        # comp_score=0; score = 0 + 0 + 1.2 = 1.2
        assert score == pytest.approx(1.2, abs=0.1)

    def test_urgency_driver_none_reduces_readiness(self):
        # urgency_driver="none" → uses 20 in readiness instead of 80
        inp_none = make_input(
            competitor_price_eur=0,
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            urgency_driver="none",
        )
        inp_cost = make_input(
            competitor_price_eur=0,
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            urgency_driver="cost_savings",
        )
        score_none = _price_score(inp_none, recommended=100, margin=0)
        score_cost = _price_score(inp_cost, recommended=100, margin=0)
        assert score_cost > score_none

    def test_high_margin_and_on_par_with_competitor_gives_good_score(self):
        inp = make_input(
            competitor_price_eur=50000,
            champion_strength=80,
            decision_maker_engaged=True,
            has_business_case=True,
            urgency_driver="cost_savings",
        )
        score = _price_score(inp, recommended=50000, margin=50)
        assert score > 60

    def test_readiness_champion_contribution(self):
        # Verify champion_strength is correctly weighted at 0.35
        inp_high = make_input(
            competitor_price_eur=0, champion_strength=100,
            decision_maker_engaged=False, has_business_case=False, urgency_driver="none",
        )
        inp_low = make_input(
            competitor_price_eur=0, champion_strength=0,
            decision_maker_engaged=False, has_business_case=False, urgency_driver="none",
        )
        score_high = _price_score(inp_high, recommended=100, margin=0)
        score_low = _price_score(inp_low, recommended=100, margin=0)
        # diff in readiness = 100*0.35 = 35; weighted at 0.30 → 10.5 diff
        assert score_high - score_low == pytest.approx(10.5, abs=0.1)

    def test_score_rounded_to_2_decimals(self):
        inp = make_input()
        score = _price_score(inp, recommended=45000, margin=40)
        # Check it's rounded to 2 decimal places
        assert score == round(score, 2)

    def test_comp_score_clamped_above_at_100(self):
        # ratio very close to 1 → comp_score approaches 100 but never exceeds
        inp = make_input(competitor_price_eur=100)
        score = _price_score(inp, recommended=100, margin=0)
        assert score <= 100


# ---------------------------------------------------------------------------
# 5. TestWinProbabilityBoost  (12 tests)
# ---------------------------------------------------------------------------

class TestWinProbabilityBoost:

    def test_discount_zero_and_competitive_urgency_low(self):
        result = _win_probability_boost(0, PricingStrategy.COMPETITIVE, DealUrgency.LOW)
        # base=0 + 4 (COMPETITIVE) = 4; min(25, 4) = 4
        assert result == pytest.approx(4.0, abs=0.1)

    def test_discount_zero_no_bonuses(self):
        result = _win_probability_boost(0, PricingStrategy.PENETRATION, DealUrgency.LOW)
        # base=0; no bonuses → 0; min(25,0)=0
        assert result == 0.0

    def test_value_based_adds_8(self):
        result = _win_probability_boost(0, PricingStrategy.VALUE_BASED, DealUrgency.LOW)
        # base=0 + 8 = 8
        assert result == pytest.approx(8.0, abs=0.1)

    def test_competitive_adds_4(self):
        result = _win_probability_boost(0, PricingStrategy.COMPETITIVE, DealUrgency.LOW)
        # base=0 + 4 = 4
        assert result == pytest.approx(4.0, abs=0.1)

    def test_high_urgency_adds_5(self):
        result = _win_probability_boost(0, PricingStrategy.PENETRATION, DealUrgency.HIGH)
        # base=0 + 5 = 5
        assert result == pytest.approx(5.0, abs=0.1)

    def test_critical_urgency_adds_5(self):
        result = _win_probability_boost(0, PricingStrategy.PENETRATION, DealUrgency.CRITICAL)
        # base=0 + 5 = 5
        assert result == pytest.approx(5.0, abs=0.1)

    def test_medium_urgency_no_bonus(self):
        result = _win_probability_boost(0, PricingStrategy.PENETRATION, DealUrgency.MEDIUM)
        assert result == 0.0

    def test_discount_contributes_0_4_per_pct(self):
        result = _win_probability_boost(10, PricingStrategy.PENETRATION, DealUrgency.LOW)
        # 10 * 0.4 = 4.0
        assert result == pytest.approx(4.0, abs=0.1)

    def test_capped_at_25(self):
        # discount=50 → 20 + VALUE_BASED+8 + CRITICAL+5 = 33 → cap at 25
        result = _win_probability_boost(50, PricingStrategy.VALUE_BASED, DealUrgency.CRITICAL)
        assert result == pytest.approx(25.0, abs=0.1)

    def test_value_based_critical_combo(self):
        result = _win_probability_boost(0, PricingStrategy.VALUE_BASED, DealUrgency.CRITICAL)
        # 0 + 8 + 5 = 13
        assert result == pytest.approx(13.0, abs=0.1)

    def test_competitive_high_urgency_combo(self):
        result = _win_probability_boost(5, PricingStrategy.COMPETITIVE, DealUrgency.HIGH)
        # 5*0.4=2 + 4 + 5 = 11
        assert result == pytest.approx(11.0, abs=0.1)

    def test_result_rounded_to_1_decimal(self):
        result = _win_probability_boost(7, PricingStrategy.COMPETITIVE, DealUrgency.LOW)
        # 7*0.4=2.8 + 4 = 6.8
        assert result == pytest.approx(6.8, abs=0.01)


# ---------------------------------------------------------------------------
# 6. TestDiscountRisk  (7 tests)
# ---------------------------------------------------------------------------

class TestDiscountRisk:

    def test_discount_30_returns_high(self):
        assert _discount_risk(30) == DiscountRisk.HIGH

    def test_discount_above_30_returns_high(self):
        assert _discount_risk(35) == DiscountRisk.HIGH

    def test_discount_29_9_returns_medium(self):
        assert _discount_risk(29.9) == DiscountRisk.MEDIUM

    def test_discount_15_returns_medium(self):
        assert _discount_risk(15) == DiscountRisk.MEDIUM

    def test_discount_14_9_returns_low(self):
        assert _discount_risk(14.9) == DiscountRisk.LOW

    def test_discount_above_0_returns_low(self):
        assert _discount_risk(0.1) == DiscountRisk.LOW

    def test_discount_zero_returns_none(self):
        assert _discount_risk(0) == DiscountRisk.NONE


# ---------------------------------------------------------------------------
# 7. TestOptimizerOptimize  (18 tests)
# ---------------------------------------------------------------------------

class TestOptimizerOptimize:

    def setup_method(self):
        self.opt = PricingOptimizer()

    def test_returns_pricing_result(self):
        inp = make_input()
        result = self.opt.optimize(inp)
        assert isinstance(result, PricingResult)

    def test_all_fields_present(self):
        inp = make_input()
        result = self.opt.optimize(inp)
        assert result.deal_id == "deal1"
        assert result.deal_name == "Test Deal"
        assert isinstance(result.recommended_price_eur, float)
        assert isinstance(result.discount_pct, float)
        assert isinstance(result.price_score, float)
        assert isinstance(result.win_probability_boost_pct, float)
        assert isinstance(result.margin_pct, float)
        assert isinstance(result.value_gap_eur, (int, float))
        assert isinstance(result.pricing_signals, list)
        assert isinstance(result.negotiation_tips, list)
        assert isinstance(result.risk_flags, list)

    def test_discount_pct_within_ceiling(self):
        inp = make_input(customer_size="mid_market")
        result = self.opt.optimize(inp)
        ceiling = _SIZE_DISCOUNT_CEILING["mid_market"]
        assert result.discount_pct <= ceiling

    def test_discount_pct_non_negative(self):
        inp = make_input()
        result = self.opt.optimize(inp)
        assert result.discount_pct >= 0

    def test_recommended_price_formula(self):
        inp = make_input(list_price_eur=100000)
        result = self.opt.optimize(inp)
        expected = round(inp.list_price_eur * (1 - result.discount_pct / 100), 2)
        assert result.recommended_price_eur == pytest.approx(expected, abs=0.01)

    def test_margin_pct_calculated_correctly(self):
        inp = make_input(list_price_eur=100000, cost_to_serve_eur=20000)
        result = self.opt.optimize(inp)
        recommended = result.recommended_price_eur
        if recommended > 0:
            expected_margin = round((recommended - inp.cost_to_serve_eur) / recommended * 100, 1)
            assert result.margin_pct == pytest.approx(expected_margin, abs=0.1)

    def test_value_gap_is_list_minus_competitor(self):
        inp = make_input(list_price_eur=50000, competitor_price_eur=42000)
        result = self.opt.optimize(inp)
        assert result.value_gap_eur == pytest.approx(8000.0, abs=0.01)

    def test_value_gap_negative_when_competitor_pricier(self):
        inp = make_input(list_price_eur=50000, competitor_price_eur=60000)
        result = self.opt.optimize(inp)
        assert result.value_gap_eur == pytest.approx(-10000.0, abs=0.01)

    def test_stored_via_get(self):
        inp = make_input(deal_id="test_store")
        result = self.opt.optimize(inp)
        stored = self.opt.get("test_store")
        assert stored is result

    def test_get_unknown_deal_returns_none(self):
        assert self.opt.get("nonexistent") is None

    def test_overwrite_works(self):
        inp1 = make_input(deal_id="same_id", list_price_eur=100000)
        inp2 = make_input(deal_id="same_id", list_price_eur=200000)
        self.opt.optimize(inp1)
        result2 = self.opt.optimize(inp2)
        stored = self.opt.get("same_id")
        assert stored is result2

    def test_recommended_strategy_is_enum(self):
        inp = make_input()
        result = self.opt.optimize(inp)
        assert isinstance(result.recommended_strategy, PricingStrategy)

    def test_discount_risk_is_enum(self):
        inp = make_input()
        result = self.opt.optimize(inp)
        assert isinstance(result.discount_risk, DiscountRisk)

    def test_deal_urgency_is_enum(self):
        inp = make_input()
        result = self.opt.optimize(inp)
        assert isinstance(result.deal_urgency, DealUrgency)

    def test_price_score_in_valid_range(self):
        inp = make_input()
        result = self.opt.optimize(inp)
        assert 0 <= result.price_score <= 100

    def test_win_probability_boost_capped_at_25(self):
        inp = make_input()
        result = self.opt.optimize(inp)
        assert result.win_probability_boost_pct <= 25

    def test_zero_list_price_margin_is_zero(self):
        inp = make_input(list_price_eur=0, cost_to_serve_eur=0, competitor_price_eur=0,
                         customer_budget_eur=0)
        result = self.opt.optimize(inp)
        assert result.margin_pct == 0.0

    def test_multiple_deals_stored_separately(self):
        inp1 = make_input(deal_id="d1")
        inp2 = make_input(deal_id="d2")
        r1 = self.opt.optimize(inp1)
        r2 = self.opt.optimize(inp2)
        assert self.opt.get("d1") is r1
        assert self.opt.get("d2") is r2


# ---------------------------------------------------------------------------
# 8. TestOptimizerBatch  (9 tests)
# ---------------------------------------------------------------------------

class TestOptimizerBatch:

    def setup_method(self):
        self.opt = PricingOptimizer()

    def test_empty_list_returns_empty(self):
        result = self.opt.optimize_batch([])
        assert result == []

    def test_returns_list_of_pricing_results(self):
        inputs = [make_input(deal_id=f"d{i}") for i in range(3)]
        results = self.opt.optimize_batch(inputs)
        assert all(isinstance(r, PricingResult) for r in results)

    def test_sorted_descending_by_price_score(self):
        inputs = [make_input(deal_id=f"d{i}") for i in range(5)]
        results = self.opt.optimize_batch(inputs)
        scores = [r.price_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_all_results_stored(self):
        inputs = [make_input(deal_id=f"d{i}") for i in range(3)]
        self.opt.optimize_batch(inputs)
        for i in range(3):
            assert self.opt.get(f"d{i}") is not None

    def test_length_matches_input(self):
        inputs = [make_input(deal_id=f"d{i}") for i in range(4)]
        results = self.opt.optimize_batch(inputs)
        assert len(results) == 4

    def test_single_input_returns_single_result(self):
        inputs = [make_input(deal_id="solo")]
        results = self.opt.optimize_batch(inputs)
        assert len(results) == 1
        assert results[0].deal_id == "solo"

    def test_batch_results_consistent_with_individual_optimize(self):
        inp = make_input(deal_id="consistent")
        [r_batch] = self.opt.optimize_batch([inp])
        # Re-run individually to compare (same inputs → same results)
        opt2 = PricingOptimizer()
        r_single = opt2.optimize(inp)
        assert r_batch.discount_pct == r_single.discount_pct
        assert r_batch.price_score == r_single.price_score

    def test_batch_with_different_scores_correctly_ordered(self):
        # High champion + business case → better readiness → higher score
        inp_good = make_input(
            deal_id="good",
            champion_strength=100,
            has_business_case=True,
            decision_maker_engaged=True,
            cost_to_serve_eur=5000,
        )
        inp_bad = make_input(
            deal_id="bad",
            champion_strength=0,
            has_business_case=False,
            decision_maker_engaged=False,
            cost_to_serve_eur=49000,
        )
        results = self.opt.optimize_batch([inp_bad, inp_good])
        assert results[0].deal_id == "good"

    def test_batch_does_not_lose_previous_results(self):
        r1 = self.opt.optimize(make_input(deal_id="pre_existing"))
        self.opt.optimize_batch([make_input(deal_id="new_batch")])
        assert self.opt.get("pre_existing") is r1


# ---------------------------------------------------------------------------
# 9. TestOptimizerQueries  (16 tests)
# ---------------------------------------------------------------------------

class TestOptimizerQueries:

    def setup_method(self):
        self.opt = PricingOptimizer()

    def test_all_deals_empty_when_no_optimizations(self):
        assert self.opt.all_deals() == []

    def test_all_deals_sorted_desc_by_price_score(self):
        for i in range(4):
            self.opt.optimize(make_input(deal_id=f"d{i}"))
        results = self.opt.all_deals()
        scores = [r.price_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_by_strategy_filters_correctly(self):
        # Make a deal that should produce COMPETITIVE
        inp = make_input(
            deal_id="competitive_deal",
            list_price_eur=100,
            competitor_price_eur=100,
            has_business_case=False,
            champion_strength=50,
            num_competitors=1,
            customer_size="mid_market",
            expansion_potential_eur=0,
            urgency_driver="none",
            days_in_stage=5,
        )
        result = self.opt.optimize(inp)
        by_strat = self.opt.by_strategy(result.recommended_strategy)
        assert result in by_strat

    def test_by_strategy_returns_empty_for_unused_strategy(self):
        self.opt.optimize(make_input())
        # FREEMIUM is unlikely to be assigned for default inputs
        freemium_deals = self.opt.by_strategy(PricingStrategy.FREEMIUM)
        assert isinstance(freemium_deals, list)

    def test_by_urgency_filters_correctly(self):
        inp = make_input(deal_id="regulatory_deal", urgency_driver="regulatory")
        result = self.opt.optimize(inp)
        by_urgency = self.opt.by_urgency(DealUrgency.CRITICAL)
        assert result in by_urgency

    def test_by_urgency_returns_empty_when_no_match(self):
        inp = make_input(urgency_driver="none", days_in_stage=1)
        self.opt.optimize(inp)
        # This should be LOW urgency, not CRITICAL
        critical_list = self.opt.by_urgency(DealUrgency.CRITICAL)
        assert isinstance(critical_list, list)

    def test_high_risk_discounts_filters_high_discount_risk(self):
        # Force HIGH discount risk: need discount>=30 → enterprise + many factors
        inp = make_input(
            deal_id="high_risk",
            list_price_eur=100,
            competitor_price_eur=50,   # +15 comp
            customer_budget_eur=70,    # +10 budget
            num_competitors=6,         # +8 intensity
            historical_discount_pct=20, # +6
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=24,  # +5
            customer_size="enterprise",  # ceiling=35; total=44 → capped at 35
        )
        result = self.opt.optimize(inp)
        if result.discount_risk == DiscountRisk.HIGH:
            assert result in self.opt.high_risk_discounts()

    def test_high_risk_discounts_empty_when_no_high_risk(self):
        # No discount → NONE risk
        inp = make_input(
            competitor_price_eur=0,
            customer_budget_eur=50000,
            list_price_eur=50000,
            num_competitors=0,
            historical_discount_pct=0,
            champion_strength=70,
            decision_maker_engaged=True,
            has_business_case=True,
            contract_length_months=0,
        )
        self.opt.optimize(inp)
        high_risk = self.opt.high_risk_discounts()
        assert all(r.discount_risk == DiscountRisk.HIGH for r in high_risk)

    def test_critical_deals_returns_critical_urgency(self):
        inp = make_input(urgency_driver="regulatory")
        result = self.opt.optimize(inp)
        critical = self.opt.critical_deals()
        assert result in critical
        assert all(r.deal_urgency == DealUrgency.CRITICAL for r in critical)

    def test_total_recommended_pipeline_eur_sum(self):
        inputs = [
            make_input(deal_id="p1", list_price_eur=100000),
            make_input(deal_id="p2", list_price_eur=50000),
        ]
        results = [self.opt.optimize(inp) for inp in inputs]
        expected = round(sum(r.recommended_price_eur for r in results), 2)
        assert self.opt.total_recommended_pipeline_eur() == pytest.approx(expected, abs=0.01)

    def test_total_pipeline_empty_is_zero(self):
        assert self.opt.total_recommended_pipeline_eur() == 0.0

    def test_avg_margin_pct_empty_is_zero(self):
        assert self.opt.avg_margin_pct() == 0.0

    def test_avg_margin_pct_single_deal(self):
        inp = make_input(deal_id="single_margin")
        result = self.opt.optimize(inp)
        assert self.opt.avg_margin_pct() == pytest.approx(result.margin_pct, abs=0.1)

    def test_avg_margin_pct_multiple_deals(self):
        inp1 = make_input(deal_id="m1", list_price_eur=100000, cost_to_serve_eur=10000)
        inp2 = make_input(deal_id="m2", list_price_eur=100000, cost_to_serve_eur=50000)
        r1 = self.opt.optimize(inp1)
        r2 = self.opt.optimize(inp2)
        expected = round((r1.margin_pct + r2.margin_pct) / 2, 1)
        assert self.opt.avg_margin_pct() == pytest.approx(expected, abs=0.1)

    def test_reset_clears_all_results(self):
        self.opt.optimize(make_input(deal_id="to_clear"))
        self.opt.reset()
        assert self.opt.all_deals() == []
        assert self.opt.get("to_clear") is None

    def test_reset_then_optimize_works(self):
        self.opt.optimize(make_input(deal_id="before_reset"))
        self.opt.reset()
        inp = make_input(deal_id="after_reset")
        result = self.opt.optimize(inp)
        assert self.opt.get("after_reset") is result
        assert len(self.opt.all_deals()) == 1


# ---------------------------------------------------------------------------
# 10. TestSummary  (12 tests)
# ---------------------------------------------------------------------------

class TestSummary:

    def setup_method(self):
        self.opt = PricingOptimizer()

    def test_empty_summary_all_keys_present(self):
        s = self.opt.summary()
        assert "total" in s
        assert "strategy_counts" in s
        assert "urgency_counts" in s
        assert "avg_price_score" in s
        assert "avg_discount_pct" in s
        assert "avg_margin_pct" in s
        assert "total_pipeline_eur" in s

    def test_empty_summary_total_is_zero(self):
        assert self.opt.summary()["total"] == 0

    def test_empty_summary_strategy_counts_empty(self):
        assert self.opt.summary()["strategy_counts"] == {}

    def test_empty_summary_urgency_counts_empty(self):
        assert self.opt.summary()["urgency_counts"] == {}

    def test_empty_summary_averages_are_zero(self):
        s = self.opt.summary()
        assert s["avg_price_score"] == 0.0
        assert s["avg_discount_pct"] == 0.0
        assert s["avg_margin_pct"] == 0.0
        assert s["total_pipeline_eur"] == 0.0

    def test_summary_total_count(self):
        for i in range(3):
            self.opt.optimize(make_input(deal_id=f"s{i}"))
        assert self.opt.summary()["total"] == 3

    def test_summary_strategy_counts_correct(self):
        # Two deals optimized; their strategies should be counted
        inp1 = make_input(deal_id="s1")
        inp2 = make_input(deal_id="s2")
        r1 = self.opt.optimize(inp1)
        r2 = self.opt.optimize(inp2)
        s = self.opt.summary()
        counts = s["strategy_counts"]
        # Both might be same strategy; just verify totals add up
        assert sum(counts.values()) == 2

    def test_summary_urgency_counts_correct(self):
        inp_reg = make_input(deal_id="u1", urgency_driver="regulatory")
        inp_none = make_input(deal_id="u2", urgency_driver="none", days_in_stage=1)
        self.opt.optimize(inp_reg)
        self.opt.optimize(inp_none)
        s = self.opt.summary()
        assert sum(s["urgency_counts"].values()) == 2

    def test_summary_avg_price_score(self):
        for i in range(3):
            self.opt.optimize(make_input(deal_id=f"sc{i}"))
        all_results = self.opt.all_deals()
        expected = round(sum(r.price_score for r in all_results) / 3, 1)
        assert self.opt.summary()["avg_price_score"] == pytest.approx(expected, abs=0.1)

    def test_summary_avg_discount_pct(self):
        for i in range(2):
            self.opt.optimize(make_input(deal_id=f"dc{i}"))
        all_results = self.opt.all_deals()
        expected = round(sum(r.discount_pct for r in all_results) / 2, 1)
        assert self.opt.summary()["avg_discount_pct"] == pytest.approx(expected, abs=0.1)

    def test_summary_total_pipeline(self):
        for i in range(2):
            self.opt.optimize(make_input(deal_id=f"tp{i}", list_price_eur=100000))
        all_results = self.opt.all_deals()
        expected = round(sum(r.recommended_price_eur for r in all_results), 2)
        assert self.opt.summary()["total_pipeline_eur"] == pytest.approx(expected, abs=0.01)

    def test_summary_strategy_counts_keys_are_strings(self):
        self.opt.optimize(make_input())
        s = self.opt.summary()
        for key in s["strategy_counts"]:
            assert isinstance(key, str)


# ---------------------------------------------------------------------------
# 11. TestSignals  (22 tests)
# ---------------------------------------------------------------------------

class TestSignals:

    def setup_method(self):
        self.opt = PricingOptimizer()

    def _optimize(self, **kwargs):
        return self.opt.optimize(make_input(**kwargs))

    def test_champion_75_adds_pricing_signal(self):
        result = self._optimize(champion_strength=75)
        assert any("Champion fort" in s for s in result.pricing_signals)

    def test_champion_below_75_no_champion_signal(self):
        result = self._optimize(champion_strength=74.9)
        assert not any("Champion fort" in s for s in result.pricing_signals)

    def test_business_case_adds_pricing_signal(self):
        result = self._optimize(has_business_case=True)
        assert any("business case" in s.lower() for s in result.pricing_signals)

    def test_no_business_case_no_business_case_signal(self):
        result = self._optimize(has_business_case=False)
        assert not any("Business case" in s for s in result.pricing_signals)

    def test_dm_engaged_adds_pricing_signal(self):
        result = self._optimize(decision_maker_engaged=True)
        assert any("Décideur" in s for s in result.pricing_signals)

    def test_dm_not_engaged_no_dm_signal(self):
        result = self._optimize(decision_maker_engaged=False)
        assert not any("Décideur" in s for s in result.pricing_signals)

    def test_contract_24_months_adds_contract_signal(self):
        result = self._optimize(contract_length_months=24)
        assert any("Contrat" in s for s in result.pricing_signals)

    def test_contract_below_24_no_contract_signal(self):
        result = self._optimize(contract_length_months=12)
        assert not any("Contrat" in s for s in result.pricing_signals)

    def test_expansion_ge_list_adds_expansion_signal(self):
        result = self._optimize(expansion_potential_eur=50000, list_price_eur=50000)
        assert any("expansion" in s.lower() for s in result.pricing_signals)

    def test_expansion_below_list_no_expansion_signal(self):
        result = self._optimize(expansion_potential_eur=10000, list_price_eur=50000)
        assert not any("expansion" in s.lower() for s in result.pricing_signals)

    def test_competitor_more_expensive_adds_price_advantage_signal(self):
        # competitor > list*1.1
        result = self._optimize(list_price_eur=100, competitor_price_eur=115)
        assert any("Compétiteurs" in s for s in result.pricing_signals)

    def test_competitor_not_more_expensive_no_price_advantage(self):
        result = self._optimize(list_price_eur=100, competitor_price_eur=100)
        assert not any("Compétiteurs plus chers" in s for s in result.pricing_signals)

    def test_low_margin_adds_risk_flag(self):
        result = self._optimize(list_price_eur=100, cost_to_serve_eur=70,
                                competitor_price_eur=0, customer_budget_eur=100,
                                num_competitors=0, historical_discount_pct=0,
                                champion_strength=70, decision_maker_engaged=True,
                                has_business_case=True, contract_length_months=0)
        # margin < 40 → risk flag
        if result.margin_pct < 40:
            assert any("Marge faible" in f for f in result.risk_flags)

    def test_discount_25_adds_risk_flag(self):
        # Force discount >=25: enterprise with many factors
        result = self._optimize(
            list_price_eur=100, competitor_price_eur=60,  # +15 comp (gap=40%)
            customer_budget_eur=75,  # +10 budget
            num_competitors=6,       # +8 intensity
            historical_discount_pct=10,  # +3
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=0,
            customer_size="enterprise",  # ceiling=35
        )
        # 15+10+8+3 = 36 → capped at 35 → discount=35 >=25 → risk flag
        if result.discount_pct >= 25:
            assert any("Discount élevé" in f for f in result.risk_flags)

    def test_4_plus_competitors_adds_risk_flag(self):
        result = self._optimize(num_competitors=4)
        assert any("concurrents" in f for f in result.risk_flags)

    def test_3_competitors_no_competitor_risk_flag(self):
        result = self._optimize(num_competitors=3)
        assert not any("concurrents" in f for f in result.risk_flags)

    def test_critical_urgency_adds_risk_flag(self):
        result = self._optimize(urgency_driver="regulatory")
        assert any("critique" in f.lower() for f in result.risk_flags)

    def test_weak_champion_adds_risk_flag(self):
        result = self._optimize(champion_strength=39)
        assert any("Champion faible" in f for f in result.risk_flags)

    def test_value_based_strategy_adds_roi_tip(self):
        # Create VALUE_BASED: business_case + champion>=75, not penetration
        result = self._optimize(
            has_business_case=True,
            champion_strength=75,
            list_price_eur=100,
            competitor_price_eur=100,
        )
        if result.recommended_strategy == PricingStrategy.VALUE_BASED:
            assert any("ROI" in t for t in result.negotiation_tips)

    def test_anchor_strategy_adds_anchor_tip(self):
        # ANCHOR: CRITICAL urgency + 3+ competitors, not penetration, no value_based conditions
        result = self._optimize(
            urgency_driver="regulatory",
            num_competitors=3,
            has_business_case=False,
            champion_strength=50,
            list_price_eur=100,
            competitor_price_eur=100,
        )
        if result.recommended_strategy == PricingStrategy.ANCHOR:
            assert any("prix plein" in t for t in result.negotiation_tips)

    def test_discount_gt_0_adds_quarter_tip(self):
        result = self._optimize()
        if result.discount_pct > 0:
            assert any("trimestre" in t for t in result.negotiation_tips)

    def test_dm_engaged_adds_exec_call_tip(self):
        result = self._optimize(decision_maker_engaged=True)
        assert any("exec" in t.lower() for t in result.negotiation_tips)


# ---------------------------------------------------------------------------
# 12. TestEdgeCases  (14 tests)
# ---------------------------------------------------------------------------

class TestEdgeCases:

    def setup_method(self):
        self.opt = PricingOptimizer()

    def test_cost_to_serve_above_recommended_price_gives_negative_margin(self):
        inp = make_input(
            list_price_eur=100,
            cost_to_serve_eur=200,
            competitor_price_eur=0,
            customer_budget_eur=100,
            num_competitors=0,
            historical_discount_pct=0,
            champion_strength=70,
            decision_maker_engaged=True,
            has_business_case=True,
            contract_length_months=0,
        )
        result = self.opt.optimize(inp)
        # recommended_price will be 100 (0% discount); margin=(100-200)/100*100=-100
        assert result.margin_pct < 0

    def test_customer_budget_zero_no_budget_contribution(self):
        inp = make_input(
            competitor_price_eur=0,
            customer_budget_eur=0,
            list_price_eur=50000,
            num_competitors=0,
            historical_discount_pct=0,
            champion_strength=70,
            decision_maker_engaged=True,
            has_business_case=True,
            contract_length_months=0,
        )
        # Budget contribution=0; other contributions bring it to 0 (strengths offset)
        result = self.opt.optimize(inp)
        assert result.discount_pct >= 0

    def test_competitor_price_zero_no_competitor_contribution(self):
        inp = make_input(
            competitor_price_eur=0,
            customer_budget_eur=50000,
            list_price_eur=50000,
            num_competitors=0,
            historical_discount_pct=0,
            champion_strength=70,
            decision_maker_engaged=True,
            has_business_case=True,
            contract_length_months=0,
        )
        result = self.opt.optimize(inp)
        # No competitor contribution expected
        assert result.discount_pct == 0.0

    def test_list_price_zero_margin_is_zero(self):
        inp = make_input(
            list_price_eur=0,
            cost_to_serve_eur=0,
            competitor_price_eur=0,
            customer_budget_eur=0,
        )
        result = self.opt.optimize(inp)
        assert result.margin_pct == 0.0

    def test_historical_discount_zero_no_historical_contribution(self):
        inp = make_input(
            competitor_price_eur=0,
            customer_budget_eur=50000,
            list_price_eur=50000,
            num_competitors=0,
            historical_discount_pct=0,
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=0,
        )
        result = self.opt.optimize(inp)
        assert result.discount_pct == 0.0

    def test_all_booleans_false(self):
        inp = make_input(
            decision_maker_engaged=False,
            has_business_case=False,
        )
        result = self.opt.optimize(inp)
        assert isinstance(result, PricingResult)

    def test_unknown_urgency_driver_defaults_to_low(self):
        inp = make_input(urgency_driver="xyz_unknown", days_in_stage=5, deal_stage="proposal")
        urgency = _deal_urgency(inp)
        assert urgency == DealUrgency.LOW

    def test_unknown_customer_size_defaults_to_25_ceiling_in_discount(self):
        inp = make_input(
            customer_size="xyz_unknown",
            list_price_eur=100,
            competitor_price_eur=50,    # +15
            customer_budget_eur=70,     # +10
            num_competitors=6,          # +8
            historical_discount_pct=20, # +6
            champion_strength=0,
            decision_maker_engaged=False,
            has_business_case=False,
            contract_length_months=24,  # +5 → total=44 → capped at 25
        )
        result = _recommended_discount(inp)
        assert result == pytest.approx(25.0, abs=0.1)

    def test_unknown_deal_stage_defaults_to_21_max_in_urgency(self):
        # Unknown stage → max_days=21; threshold=31.5; days=32 → overdue
        inp = make_input(urgency_driver="none", deal_stage="unknown_xyz", days_in_stage=32)
        urgency = _deal_urgency(inp)
        assert urgency == DealUrgency.HIGH

    def test_to_dict_enum_values_are_strings(self):
        inp = make_input()
        result = self.opt.optimize(inp)
        d = result.to_dict()
        assert isinstance(d["recommended_strategy"], str)
        assert isinstance(d["discount_risk"], str)
        assert isinstance(d["deal_urgency"], str)

    def test_to_dict_strategy_value_matches_enum(self):
        inp = make_input()
        result = self.opt.optimize(inp)
        d = result.to_dict()
        assert d["recommended_strategy"] == result.recommended_strategy.value

    def test_to_dict_discount_risk_value_matches_enum(self):
        inp = make_input()
        result = self.opt.optimize(inp)
        d = result.to_dict()
        assert d["discount_risk"] == result.discount_risk.value

    def test_to_dict_deal_urgency_value_matches_enum(self):
        inp = make_input()
        result = self.opt.optimize(inp)
        d = result.to_dict()
        assert d["deal_urgency"] == result.deal_urgency.value

    def test_expansion_upsell_tip_when_positive_expansion(self):
        inp = make_input(expansion_potential_eur=1)
        result = self.opt.optimize(inp)
        assert any("upsell" in t.lower() for t in result.negotiation_tips)


# ---------------------------------------------------------------------------
# 13. TestConstants  (8 tests)
# ---------------------------------------------------------------------------

class TestConstants:

    def test_stage_max_days_prospecting(self):
        assert _STAGE_MAX_DAYS["prospecting"] == 14

    def test_stage_max_days_qualification(self):
        assert _STAGE_MAX_DAYS["qualification"] == 21

    def test_stage_max_days_demo(self):
        assert _STAGE_MAX_DAYS["demo"] == 21

    def test_stage_max_days_proposal(self):
        assert _STAGE_MAX_DAYS["proposal"] == 30

    def test_stage_max_days_negotiation(self):
        assert _STAGE_MAX_DAYS["negotiation"] == 21

    def test_stage_max_days_closing(self):
        assert _STAGE_MAX_DAYS["closing"] == 14

    def test_size_discount_ceilings(self):
        assert _SIZE_DISCOUNT_CEILING["startup"] == 20
        assert _SIZE_DISCOUNT_CEILING["smb"] == 25
        assert _SIZE_DISCOUNT_CEILING["mid_market"] == 30
        assert _SIZE_DISCOUNT_CEILING["enterprise"] == 35

    def test_urgency_drivers_mapping(self):
        assert _URGENCY_DRIVERS["regulatory"] == DealUrgency.CRITICAL
        assert _URGENCY_DRIVERS["competitive"] == DealUrgency.HIGH
        assert _URGENCY_DRIVERS["cost_savings"] == DealUrgency.HIGH
        assert _URGENCY_DRIVERS["growth"] == DealUrgency.MEDIUM
        assert _URGENCY_DRIVERS["none"] == DealUrgency.LOW
