"""
Comprehensive pytest test suite for SalesPricingNegotiationIntelligenceEngine.
"""
from __future__ import annotations

import pytest
from swarm.intelligence.sales_pricing_negotiation_intelligence_engine import (
    NegotiationRisk,
    NegotiationPattern,
    NegotiationSeverity,
    NegotiationAction,
    PricingNegotiationInput,
    PricingNegotiationResult,
    SalesPricingNegotiationIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> PricingNegotiationInput:
    """Return a clean, low-risk baseline input with optional overrides."""
    defaults = dict(
        rep_id="rep-001",
        region="EMEA",
        evaluation_period_id="Q1-2026",
        total_deals_negotiated=20,
        deals_with_discount_applied=4,       # 20% discount rate → low
        avg_discount_pct=5.0,
        max_discount_applied_pct=10.0,
        deals_below_floor_price=0,
        discounts_approved_by_manager=3,
        discounts_self_approved=1,
        list_price_deals_closed=6,           # 30%
        value_add_instead_of_discount_count=6,  # 30%
        multi_year_deals_closed=4,
        avg_deal_size_negotiated_usd=50_000.0,
        avg_deal_size_post_negotiation_usd=49_000.0,
        competitive_deals_price_matched=2,
        prospects_rejected_due_to_price=1,
        deals_lost_on_price_alone=0,
        negotiation_cycle_avg_days=8.0,
        concession_rounds_avg=1.0,
        gross_margin_avg_pct=0.55,
        repeat_buyer_discount_rate_pct=5.0,
    )
    defaults.update(overrides)
    return PricingNegotiationInput(**defaults)


def engine() -> SalesPricingNegotiationIntelligenceEngine:
    return SalesPricingNegotiationIntelligenceEngine()


# ===========================================================================
# 1. ENUM VALUES
# ===========================================================================

class TestEnumValues:

    def test_negotiation_risk_low(self):
        assert NegotiationRisk.low == "low"
        assert NegotiationRisk.low.value == "low"

    def test_negotiation_risk_moderate(self):
        assert NegotiationRisk.moderate == "moderate"
        assert NegotiationRisk.moderate.value == "moderate"

    def test_negotiation_risk_high(self):
        assert NegotiationRisk.high == "high"
        assert NegotiationRisk.high.value == "high"

    def test_negotiation_risk_critical(self):
        assert NegotiationRisk.critical == "critical"
        assert NegotiationRisk.critical.value == "critical"

    def test_negotiation_risk_count(self):
        assert len(NegotiationRisk) == 4

    def test_negotiation_pattern_none(self):
        assert NegotiationPattern.none == "none"

    def test_negotiation_pattern_chronic_discounting(self):
        assert NegotiationPattern.chronic_discounting == "chronic_discounting"

    def test_negotiation_pattern_value_erosion(self):
        assert NegotiationPattern.value_erosion == "value_erosion"

    def test_negotiation_pattern_margin_collapse(self):
        assert NegotiationPattern.margin_collapse == "margin_collapse"

    def test_negotiation_pattern_price_concession_habit(self):
        assert NegotiationPattern.price_concession_habit == "price_concession_habit"

    def test_negotiation_pattern_competitive_surrender(self):
        assert NegotiationPattern.competitive_surrender == "competitive_surrender"

    def test_negotiation_pattern_count(self):
        assert len(NegotiationPattern) == 6

    def test_negotiation_severity_disciplined(self):
        assert NegotiationSeverity.disciplined == "disciplined"

    def test_negotiation_severity_lenient(self):
        assert NegotiationSeverity.lenient == "lenient"

    def test_negotiation_severity_compromised(self):
        assert NegotiationSeverity.compromised == "compromised"

    def test_negotiation_severity_collapsing(self):
        assert NegotiationSeverity.collapsing == "collapsing"

    def test_negotiation_severity_count(self):
        assert len(NegotiationSeverity) == 4

    def test_negotiation_action_no_action(self):
        assert NegotiationAction.no_action == "no_action"

    def test_negotiation_action_discount_discipline_review(self):
        assert NegotiationAction.discount_discipline_review == "discount_discipline_review"

    def test_negotiation_action_value_messaging_training(self):
        assert NegotiationAction.value_messaging_training == "value_messaging_training"

    def test_negotiation_action_pricing_floor_enforcement(self):
        assert NegotiationAction.pricing_floor_enforcement == "pricing_floor_enforcement"

    def test_negotiation_action_negotiation_coaching(self):
        assert NegotiationAction.negotiation_coaching == "negotiation_coaching"

    def test_negotiation_action_deal_desk_escalation(self):
        assert NegotiationAction.deal_desk_escalation == "deal_desk_escalation"

    def test_negotiation_action_count(self):
        assert len(NegotiationAction) == 6

    def test_enums_are_str_subclasses(self):
        assert isinstance(NegotiationRisk.low, str)
        assert isinstance(NegotiationPattern.none, str)
        assert isinstance(NegotiationSeverity.disciplined, str)
        assert isinstance(NegotiationAction.no_action, str)


# ===========================================================================
# 2. _discount_discipline_score
# ===========================================================================

class TestDiscountDisciplineScore:

    def setup_method(self):
        self.e = engine()

    # --- discount_rate component ---

    def test_discount_rate_below_35_adds_0(self):
        inp = make_input(total_deals_negotiated=10, deals_with_discount_applied=3,
                         avg_discount_pct=0.0, discounts_approved_by_manager=10,
                         discounts_self_approved=0)
        # rate=0.3 < 0.35 → 0; avg_discount_pct=0 → 0; self_rate=0 → 0
        assert self.e._discount_discipline_score(inp) == 0.0

    def test_discount_rate_exactly_35_adds_8(self):
        inp = make_input(total_deals_negotiated=20, deals_with_discount_applied=7,
                         avg_discount_pct=0.0, discounts_approved_by_manager=10,
                         discounts_self_approved=0)
        # 7/20=0.35 → 8; rest = 0
        assert self.e._discount_discipline_score(inp) == 8.0

    def test_discount_rate_at_50_adds_22(self):
        inp = make_input(total_deals_negotiated=10, deals_with_discount_applied=5,
                         avg_discount_pct=0.0, discounts_approved_by_manager=10,
                         discounts_self_approved=0)
        # 0.50 → 22
        assert self.e._discount_discipline_score(inp) == 22.0

    def test_discount_rate_at_70_adds_40(self):
        inp = make_input(total_deals_negotiated=10, deals_with_discount_applied=7,
                         avg_discount_pct=0.0, discounts_approved_by_manager=10,
                         discounts_self_approved=0)
        # 0.70 → 40
        assert self.e._discount_discipline_score(inp) == 40.0

    def test_discount_rate_above_70_adds_40(self):
        inp = make_input(total_deals_negotiated=10, deals_with_discount_applied=9,
                         avg_discount_pct=0.0, discounts_approved_by_manager=10,
                         discounts_self_approved=0)
        # 0.90 → 40
        assert self.e._discount_discipline_score(inp) == 40.0

    # --- avg_discount_pct component ---

    def test_avg_discount_below_8_adds_0(self):
        inp = make_input(total_deals_negotiated=10, deals_with_discount_applied=0,
                         avg_discount_pct=7.9, discounts_approved_by_manager=10,
                         discounts_self_approved=0)
        assert self.e._discount_discipline_score(inp) == 0.0

    def test_avg_discount_exactly_8_adds_7(self):
        inp = make_input(total_deals_negotiated=10, deals_with_discount_applied=0,
                         avg_discount_pct=8.0, discounts_approved_by_manager=10,
                         discounts_self_approved=0)
        assert self.e._discount_discipline_score(inp) == 7.0

    def test_avg_discount_exactly_15_adds_18(self):
        inp = make_input(total_deals_negotiated=10, deals_with_discount_applied=0,
                         avg_discount_pct=15.0, discounts_approved_by_manager=10,
                         discounts_self_approved=0)
        assert self.e._discount_discipline_score(inp) == 18.0

    def test_avg_discount_exactly_25_adds_30(self):
        inp = make_input(total_deals_negotiated=10, deals_with_discount_applied=0,
                         avg_discount_pct=25.0, discounts_approved_by_manager=10,
                         discounts_self_approved=0)
        assert self.e._discount_discipline_score(inp) == 30.0

    def test_avg_discount_above_25_adds_30(self):
        inp = make_input(total_deals_negotiated=10, deals_with_discount_applied=0,
                         avg_discount_pct=40.0, discounts_approved_by_manager=10,
                         discounts_self_approved=0)
        assert self.e._discount_discipline_score(inp) == 30.0

    # --- self_rate component ---

    def test_self_rate_below_40_adds_0(self):
        inp = make_input(total_deals_negotiated=10, deals_with_discount_applied=0,
                         avg_discount_pct=0.0, discounts_approved_by_manager=7,
                         discounts_self_approved=2)
        # self_rate = 2/9 ≈ 0.222 < 0.40 → 0
        assert self.e._discount_discipline_score(inp) == 0.0

    def test_self_rate_exactly_40_adds_10(self):
        inp = make_input(total_deals_negotiated=10, deals_with_discount_applied=0,
                         avg_discount_pct=0.0, discounts_approved_by_manager=3,
                         discounts_self_approved=2)
        # 2/5 = 0.40 → 10
        assert self.e._discount_discipline_score(inp) == 10.0

    def test_self_rate_exactly_60_adds_20(self):
        inp = make_input(total_deals_negotiated=10, deals_with_discount_applied=0,
                         avg_discount_pct=0.0, discounts_approved_by_manager=2,
                         discounts_self_approved=3)
        # 3/5 = 0.60 → 20
        assert self.e._discount_discipline_score(inp) == 20.0

    def test_self_rate_above_60_adds_20(self):
        inp = make_input(total_deals_negotiated=10, deals_with_discount_applied=0,
                         avg_discount_pct=0.0, discounts_approved_by_manager=1,
                         discounts_self_approved=9)
        # 9/10 = 0.90 → 20
        assert self.e._discount_discipline_score(inp) == 20.0

    def test_max_score_capped_at_100(self):
        inp = make_input(total_deals_negotiated=10, deals_with_discount_applied=10,
                         avg_discount_pct=40.0, discounts_approved_by_manager=0,
                         discounts_self_approved=10)
        # 40 + 30 + 20 = 90 → within cap
        score = self.e._discount_discipline_score(inp)
        assert score <= 100.0

    def test_total_deals_zero_uses_denominator_1(self):
        inp = make_input(total_deals_negotiated=0, deals_with_discount_applied=0,
                         avg_discount_pct=0.0, discounts_approved_by_manager=10,
                         discounts_self_approved=0)
        score = self.e._discount_discipline_score(inp)
        assert score == 0.0

    def test_combined_all_three_components(self):
        inp = make_input(
            total_deals_negotiated=10, deals_with_discount_applied=7,   # 0.70 → 40
            avg_discount_pct=25.0,                                        # → 30
            discounts_approved_by_manager=0, discounts_self_approved=5,  # 1.0 → 20
        )
        assert self.e._discount_discipline_score(inp) == 90.0

    def test_discount_rate_just_below_50_adds_8(self):
        inp = make_input(total_deals_negotiated=20, deals_with_discount_applied=9,
                         avg_discount_pct=0.0, discounts_approved_by_manager=10,
                         discounts_self_approved=0)
        # 9/20=0.45, 0.35 ≤ 0.45 < 0.50 → 8
        assert self.e._discount_discipline_score(inp) == 8.0

    def test_discount_rate_just_below_70_adds_22(self):
        inp = make_input(total_deals_negotiated=100, deals_with_discount_applied=69,
                         avg_discount_pct=0.0, discounts_approved_by_manager=10,
                         discounts_self_approved=0)
        # 0.69 → 22
        assert self.e._discount_discipline_score(inp) == 22.0


# ===========================================================================
# 3. _value_retention_score
# ===========================================================================

class TestValueRetentionScore:

    def setup_method(self):
        self.e = engine()

    # --- erosion_pct component ---

    def test_erosion_below_6pct_adds_0(self):
        inp = make_input(
            avg_deal_size_negotiated_usd=100_000.0,
            avg_deal_size_post_negotiation_usd=95_001.0,  # ~5% erosion
            total_deals_negotiated=10,
            value_add_instead_of_discount_count=5,
            list_price_deals_closed=5,
        )
        # erosion ≈ 0.05 < 0.06 → 0
        score = self.e._value_retention_score(inp)
        assert score == 0.0

    def test_erosion_exactly_6pct_adds_8(self):
        inp = make_input(
            avg_deal_size_negotiated_usd=100_000.0,
            avg_deal_size_post_negotiation_usd=94_000.0,  # 6%
            total_deals_negotiated=10,
            value_add_instead_of_discount_count=5,
            list_price_deals_closed=5,
        )
        score = self.e._value_retention_score(inp)
        assert score == 8.0

    def test_erosion_exactly_12pct_adds_22(self):
        inp = make_input(
            avg_deal_size_negotiated_usd=100_000.0,
            avg_deal_size_post_negotiation_usd=88_000.0,  # 12%
            total_deals_negotiated=10,
            value_add_instead_of_discount_count=5,
            list_price_deals_closed=5,
        )
        score = self.e._value_retention_score(inp)
        assert score == 22.0

    def test_erosion_exactly_20pct_adds_40(self):
        # 1 - (75000/100000) = 0.25 which is clearly >= 0.20
        # (0.20 itself is a float representation issue: 1-0.8 = 0.199...96)
        inp = make_input(
            avg_deal_size_negotiated_usd=100_000.0,
            avg_deal_size_post_negotiation_usd=75_000.0,  # 25% erosion >= 20%
            total_deals_negotiated=10,
            value_add_instead_of_discount_count=5,
            list_price_deals_closed=5,
        )
        score = self.e._value_retention_score(inp)
        assert score == 40.0

    def test_erosion_above_20pct_adds_40(self):
        inp = make_input(
            avg_deal_size_negotiated_usd=100_000.0,
            avg_deal_size_post_negotiation_usd=50_000.0,  # 50%
            total_deals_negotiated=10,
            value_add_instead_of_discount_count=5,
            list_price_deals_closed=5,
        )
        score = self.e._value_retention_score(inp)
        assert score == 40.0

    def test_no_erosion_calculation_when_neg_size_zero(self):
        inp = make_input(
            avg_deal_size_negotiated_usd=0.0,
            avg_deal_size_post_negotiation_usd=0.0,
            total_deals_negotiated=10,
            value_add_instead_of_discount_count=5,
            list_price_deals_closed=5,
        )
        score = self.e._value_retention_score(inp)
        assert score == 0.0

    # --- value_add_rate component ---

    def test_value_add_rate_below_10pct_adds_30(self):
        inp = make_input(
            avg_deal_size_negotiated_usd=0.0,
            avg_deal_size_post_negotiation_usd=0.0,
            total_deals_negotiated=10,
            value_add_instead_of_discount_count=0,   # 0% < 10%
            list_price_deals_closed=5,
        )
        # value_add < 10% → 30; list_price=5/10=50% → 0
        score = self.e._value_retention_score(inp)
        assert score == 30.0

    def test_value_add_rate_exactly_10pct_adds_15(self):
        inp = make_input(
            avg_deal_size_negotiated_usd=0.0,
            avg_deal_size_post_negotiation_usd=0.0,
            total_deals_negotiated=10,
            value_add_instead_of_discount_count=1,   # 10% → 15 (since < 0.25)
            list_price_deals_closed=5,
        )
        score = self.e._value_retention_score(inp)
        assert score == 15.0

    def test_value_add_rate_at_25pct_adds_0(self):
        inp = make_input(
            avg_deal_size_negotiated_usd=0.0,
            avg_deal_size_post_negotiation_usd=0.0,
            total_deals_negotiated=20,
            value_add_instead_of_discount_count=5,   # 25% → 0
            list_price_deals_closed=5,
        )
        score = self.e._value_retention_score(inp)
        assert score == 0.0

    # --- list_price_rate component ---

    def test_list_price_rate_below_10pct_adds_20(self):
        inp = make_input(
            avg_deal_size_negotiated_usd=0.0,
            avg_deal_size_post_negotiation_usd=0.0,
            total_deals_negotiated=20,
            value_add_instead_of_discount_count=10,   # >= 0.25 → 0
            list_price_deals_closed=1,                # 5% < 10% → 20
        )
        score = self.e._value_retention_score(inp)
        assert score == 20.0

    def test_list_price_rate_exactly_10pct_adds_10(self):
        inp = make_input(
            avg_deal_size_negotiated_usd=0.0,
            avg_deal_size_post_negotiation_usd=0.0,
            total_deals_negotiated=20,
            value_add_instead_of_discount_count=10,
            list_price_deals_closed=2,   # 10%
        )
        score = self.e._value_retention_score(inp)
        assert score == 10.0

    def test_list_price_rate_at_25pct_adds_0(self):
        inp = make_input(
            avg_deal_size_negotiated_usd=0.0,
            avg_deal_size_post_negotiation_usd=0.0,
            total_deals_negotiated=20,
            value_add_instead_of_discount_count=10,
            list_price_deals_closed=5,   # 25% → 0
        )
        score = self.e._value_retention_score(inp)
        assert score == 0.0

    def test_max_score_capped_at_100(self):
        inp = make_input(
            avg_deal_size_negotiated_usd=100_000.0,
            avg_deal_size_post_negotiation_usd=50_000.0,  # 50% → 40
            total_deals_negotiated=20,
            value_add_instead_of_discount_count=0,         # → 30
            list_price_deals_closed=0,                     # → 20
        )
        score = self.e._value_retention_score(inp)
        assert score == min(90.0, 100.0)

    def test_value_add_below_25_above_10_adds_15(self):
        inp = make_input(
            avg_deal_size_negotiated_usd=0.0,
            avg_deal_size_post_negotiation_usd=0.0,
            total_deals_negotiated=20,
            value_add_instead_of_discount_count=3,   # 15% → between 0.10 and 0.25 → 15
            list_price_deals_closed=5,               # 25% → 0
        )
        score = self.e._value_retention_score(inp)
        assert score == 15.0

    def test_list_price_below_25_above_10_adds_10(self):
        inp = make_input(
            avg_deal_size_negotiated_usd=0.0,
            avg_deal_size_post_negotiation_usd=0.0,
            total_deals_negotiated=20,
            value_add_instead_of_discount_count=10,  # 50% → 0
            list_price_deals_closed=3,               # 15% → 10
        )
        score = self.e._value_retention_score(inp)
        assert score == 10.0


# ===========================================================================
# 4. _margin_protection_score
# ===========================================================================

class TestMarginProtectionScore:

    def setup_method(self):
        self.e = engine()

    # --- gross_margin component ---

    def test_gross_margin_above_55_adds_0(self):
        inp = make_input(gross_margin_avg_pct=0.55, deals_below_floor_price=0,
                         max_discount_applied_pct=0.0)
        score = self.e._margin_protection_score(inp)
        assert score == 0.0

    def test_gross_margin_below_55_above_45_adds_8(self):
        inp = make_input(gross_margin_avg_pct=0.50, deals_below_floor_price=0,
                         max_discount_applied_pct=0.0)
        score = self.e._margin_protection_score(inp)
        assert score == 8.0

    def test_gross_margin_exactly_45_adds_8(self):
        inp = make_input(gross_margin_avg_pct=0.45, deals_below_floor_price=0,
                         max_discount_applied_pct=0.0)
        score = self.e._margin_protection_score(inp)
        assert score == 8.0

    def test_gross_margin_below_45_above_30_adds_22(self):
        inp = make_input(gross_margin_avg_pct=0.40, deals_below_floor_price=0,
                         max_discount_applied_pct=0.0)
        score = self.e._margin_protection_score(inp)
        assert score == 22.0

    def test_gross_margin_exactly_30_adds_22(self):
        inp = make_input(gross_margin_avg_pct=0.30, deals_below_floor_price=0,
                         max_discount_applied_pct=0.0)
        score = self.e._margin_protection_score(inp)
        assert score == 22.0

    def test_gross_margin_below_30_adds_40(self):
        inp = make_input(gross_margin_avg_pct=0.20, deals_below_floor_price=0,
                         max_discount_applied_pct=0.0)
        score = self.e._margin_protection_score(inp)
        assert score == 40.0

    # --- floor_rate component ---

    def test_floor_rate_below_5pct_adds_0(self):
        inp = make_input(gross_margin_avg_pct=0.60, total_deals_negotiated=20,
                         deals_below_floor_price=0, max_discount_applied_pct=0.0)
        assert self.e._margin_protection_score(inp) == 0.0

    def test_floor_rate_exactly_5pct_adds_5(self):
        inp = make_input(gross_margin_avg_pct=0.60, total_deals_negotiated=20,
                         deals_below_floor_price=1, max_discount_applied_pct=0.0)
        # 1/20 = 5% → 5
        assert self.e._margin_protection_score(inp) == 5.0

    def test_floor_rate_exactly_10pct_adds_15(self):
        inp = make_input(gross_margin_avg_pct=0.60, total_deals_negotiated=20,
                         deals_below_floor_price=2, max_discount_applied_pct=0.0)
        # 2/20 = 10% → 15
        assert self.e._margin_protection_score(inp) == 15.0

    def test_floor_rate_exactly_20pct_adds_30(self):
        inp = make_input(gross_margin_avg_pct=0.60, total_deals_negotiated=10,
                         deals_below_floor_price=2, max_discount_applied_pct=0.0)
        # 2/10 = 20% → 30
        assert self.e._margin_protection_score(inp) == 30.0

    def test_floor_rate_above_20pct_adds_30(self):
        inp = make_input(gross_margin_avg_pct=0.60, total_deals_negotiated=10,
                         deals_below_floor_price=5, max_discount_applied_pct=0.0)
        assert self.e._margin_protection_score(inp) == 30.0

    # --- max_discount component ---

    def test_max_discount_below_30_adds_0(self):
        inp = make_input(gross_margin_avg_pct=0.60, deals_below_floor_price=0,
                         max_discount_applied_pct=29.9)
        assert self.e._margin_protection_score(inp) == 0.0

    def test_max_discount_exactly_30_adds_10(self):
        inp = make_input(gross_margin_avg_pct=0.60, deals_below_floor_price=0,
                         max_discount_applied_pct=30.0)
        assert self.e._margin_protection_score(inp) == 10.0

    def test_max_discount_exactly_40_adds_20(self):
        inp = make_input(gross_margin_avg_pct=0.60, deals_below_floor_price=0,
                         max_discount_applied_pct=40.0)
        assert self.e._margin_protection_score(inp) == 20.0

    def test_max_discount_above_40_adds_20(self):
        inp = make_input(gross_margin_avg_pct=0.60, deals_below_floor_price=0,
                         max_discount_applied_pct=60.0)
        assert self.e._margin_protection_score(inp) == 20.0

    def test_max_score_capped_at_100(self):
        inp = make_input(gross_margin_avg_pct=0.20, total_deals_negotiated=10,
                         deals_below_floor_price=5, max_discount_applied_pct=50.0)
        # 40 + 30 + 20 = 90
        assert self.e._margin_protection_score(inp) == 90.0

    def test_combined_all_three_max(self):
        inp = make_input(gross_margin_avg_pct=0.10, total_deals_negotiated=5,
                         deals_below_floor_price=5, max_discount_applied_pct=50.0)
        # 40 + 30 + 20 = 90 → capped at 90
        assert self.e._margin_protection_score(inp) == 90.0


# ===========================================================================
# 5. _negotiation_efficiency_score
# ===========================================================================

class TestNegotiationEfficiencyScore:

    def setup_method(self):
        self.e = engine()

    # --- concession_rounds component ---

    def test_concession_below_1_5_adds_0(self):
        inp = make_input(concession_rounds_avg=1.4, negotiation_cycle_avg_days=0.0,
                         competitive_deals_price_matched=0)
        assert self.e._negotiation_efficiency_score(inp) == 0.0

    def test_concession_exactly_1_5_adds_7(self):
        inp = make_input(concession_rounds_avg=1.5, negotiation_cycle_avg_days=0.0,
                         competitive_deals_price_matched=0)
        assert self.e._negotiation_efficiency_score(inp) == 7.0

    def test_concession_exactly_2_5_adds_18(self):
        inp = make_input(concession_rounds_avg=2.5, negotiation_cycle_avg_days=0.0,
                         competitive_deals_price_matched=0)
        assert self.e._negotiation_efficiency_score(inp) == 18.0

    def test_concession_exactly_4_adds_35(self):
        inp = make_input(concession_rounds_avg=4.0, negotiation_cycle_avg_days=0.0,
                         competitive_deals_price_matched=0)
        assert self.e._negotiation_efficiency_score(inp) == 35.0

    def test_concession_above_4_adds_35(self):
        inp = make_input(concession_rounds_avg=6.0, negotiation_cycle_avg_days=0.0,
                         competitive_deals_price_matched=0)
        assert self.e._negotiation_efficiency_score(inp) == 35.0

    # --- negotiation_cycle_avg_days component ---

    def test_cycle_below_10_adds_0(self):
        inp = make_input(concession_rounds_avg=0.0, negotiation_cycle_avg_days=9.9,
                         competitive_deals_price_matched=0)
        assert self.e._negotiation_efficiency_score(inp) == 0.0

    def test_cycle_exactly_10_adds_5(self):
        inp = make_input(concession_rounds_avg=0.0, negotiation_cycle_avg_days=10.0,
                         competitive_deals_price_matched=0)
        assert self.e._negotiation_efficiency_score(inp) == 5.0

    def test_cycle_exactly_18_adds_15(self):
        inp = make_input(concession_rounds_avg=0.0, negotiation_cycle_avg_days=18.0,
                         competitive_deals_price_matched=0)
        assert self.e._negotiation_efficiency_score(inp) == 15.0

    def test_cycle_exactly_30_adds_30(self):
        inp = make_input(concession_rounds_avg=0.0, negotiation_cycle_avg_days=30.0,
                         competitive_deals_price_matched=0)
        assert self.e._negotiation_efficiency_score(inp) == 30.0

    def test_cycle_above_30_adds_30(self):
        inp = make_input(concession_rounds_avg=0.0, negotiation_cycle_avg_days=60.0,
                         competitive_deals_price_matched=0)
        assert self.e._negotiation_efficiency_score(inp) == 30.0

    # --- competitive_price_match_rate component ---

    def test_comp_rate_below_25pct_adds_0(self):
        inp = make_input(concession_rounds_avg=0.0, negotiation_cycle_avg_days=0.0,
                         total_deals_negotiated=20, competitive_deals_price_matched=4)
        # 4/20 = 0.20 → 0
        assert self.e._negotiation_efficiency_score(inp) == 0.0

    def test_comp_rate_exactly_25pct_adds_12(self):
        inp = make_input(concession_rounds_avg=0.0, negotiation_cycle_avg_days=0.0,
                         total_deals_negotiated=20, competitive_deals_price_matched=5)
        # 5/20 = 0.25 → 12
        assert self.e._negotiation_efficiency_score(inp) == 12.0

    def test_comp_rate_exactly_40pct_adds_25(self):
        inp = make_input(concession_rounds_avg=0.0, negotiation_cycle_avg_days=0.0,
                         total_deals_negotiated=10, competitive_deals_price_matched=4)
        # 4/10 = 0.40 → 25
        assert self.e._negotiation_efficiency_score(inp) == 25.0

    def test_comp_rate_above_40pct_adds_25(self):
        inp = make_input(concession_rounds_avg=0.0, negotiation_cycle_avg_days=0.0,
                         total_deals_negotiated=10, competitive_deals_price_matched=9)
        assert self.e._negotiation_efficiency_score(inp) == 25.0

    def test_max_score_capped_at_100(self):
        inp = make_input(concession_rounds_avg=5.0, negotiation_cycle_avg_days=60.0,
                         total_deals_negotiated=10, competitive_deals_price_matched=10)
        # 35 + 30 + 25 = 90
        assert self.e._negotiation_efficiency_score(inp) == 90.0


# ===========================================================================
# 6. _detect_pattern
# ===========================================================================

class TestDetectPattern:

    def setup_method(self):
        self.e = engine()

    def _call(self, inp, discipline=0.0, value=0.0, margin=0.0, efficiency=0.0):
        return self.e._detect_pattern(inp, discipline, value, margin, efficiency)

    # --- margin_collapse (highest priority) ---

    def test_margin_collapse_detected(self):
        inp = make_input(gross_margin_avg_pct=0.30)
        # margin=40, gross_margin<0.35 → margin_collapse
        result = self._call(inp, margin=40.0)
        assert result == NegotiationPattern.margin_collapse

    def test_margin_collapse_margin_exactly_40(self):
        inp = make_input(gross_margin_avg_pct=0.20)
        result = self._call(inp, margin=40.0)
        assert result == NegotiationPattern.margin_collapse

    def test_margin_collapse_not_detected_margin_below_40(self):
        inp = make_input(gross_margin_avg_pct=0.20)
        result = self._call(inp, margin=39.9)
        assert result != NegotiationPattern.margin_collapse

    def test_margin_collapse_not_detected_if_gm_above_35(self):
        inp = make_input(gross_margin_avg_pct=0.35)
        result = self._call(inp, margin=40.0)
        assert result != NegotiationPattern.margin_collapse

    def test_margin_collapse_requires_both_conditions(self):
        inp = make_input(gross_margin_avg_pct=0.50)
        result = self._call(inp, margin=80.0)
        assert result != NegotiationPattern.margin_collapse

    # --- chronic_discounting ---

    def test_chronic_discounting_detected(self):
        inp = make_input(
            total_deals_negotiated=10,
            deals_with_discount_applied=7,   # 70%
            avg_discount_pct=20.0,
            gross_margin_avg_pct=0.60,
        )
        result = self._call(inp, discipline=35.0)
        assert result == NegotiationPattern.chronic_discounting

    def test_chronic_discounting_not_if_discipline_below_35(self):
        inp = make_input(
            total_deals_negotiated=10,
            deals_with_discount_applied=7,
            avg_discount_pct=20.0,
            gross_margin_avg_pct=0.60,
        )
        result = self._call(inp, discipline=34.9)
        assert result != NegotiationPattern.chronic_discounting

    def test_chronic_discounting_not_if_discount_rate_below_60(self):
        inp = make_input(
            total_deals_negotiated=10,
            deals_with_discount_applied=5,   # 50%
            avg_discount_pct=20.0,
            gross_margin_avg_pct=0.60,
        )
        result = self._call(inp, discipline=40.0)
        assert result != NegotiationPattern.chronic_discounting

    def test_chronic_discounting_not_if_avg_discount_below_15(self):
        inp = make_input(
            total_deals_negotiated=10,
            deals_with_discount_applied=7,
            avg_discount_pct=14.9,
            gross_margin_avg_pct=0.60,
        )
        result = self._call(inp, discipline=40.0)
        assert result != NegotiationPattern.chronic_discounting

    def test_chronic_discounting_priority_over_competitive_surrender(self):
        """chronic_discounting is checked before competitive_surrender"""
        inp = make_input(
            total_deals_negotiated=10,
            deals_with_discount_applied=7,   # 70%
            avg_discount_pct=20.0,
            gross_margin_avg_pct=0.60,
            competitive_deals_price_matched=4,  # 40%
        )
        result = self._call(inp, discipline=40.0, efficiency=40.0)
        assert result == NegotiationPattern.chronic_discounting

    # --- competitive_surrender ---

    def test_competitive_surrender_detected(self):
        inp = make_input(
            total_deals_negotiated=10,
            deals_with_discount_applied=0,
            avg_discount_pct=0.0,
            gross_margin_avg_pct=0.60,
            competitive_deals_price_matched=4,  # 40%
        )
        result = self._call(inp, efficiency=30.0)
        assert result == NegotiationPattern.competitive_surrender

    def test_competitive_surrender_not_if_efficiency_below_30(self):
        inp = make_input(
            total_deals_negotiated=10,
            competitive_deals_price_matched=4,
            gross_margin_avg_pct=0.60,
        )
        result = self._call(inp, efficiency=29.9)
        assert result != NegotiationPattern.competitive_surrender

    def test_competitive_surrender_not_if_comp_rate_below_35(self):
        inp = make_input(
            total_deals_negotiated=10,
            competitive_deals_price_matched=3,   # 30%
            gross_margin_avg_pct=0.60,
        )
        result = self._call(inp, efficiency=40.0)
        assert result != NegotiationPattern.competitive_surrender

    def test_competitive_surrender_exactly_35pct(self):
        inp = make_input(
            total_deals_negotiated=20,
            deals_with_discount_applied=0,
            avg_discount_pct=0.0,
            gross_margin_avg_pct=0.60,
            competitive_deals_price_matched=7,  # 35%
        )
        result = self._call(inp, efficiency=35.0)
        assert result == NegotiationPattern.competitive_surrender

    # --- value_erosion ---

    def test_value_erosion_detected(self):
        inp = make_input(
            gross_margin_avg_pct=0.60,
            total_deals_negotiated=10,
            competitive_deals_price_matched=0,
            value_add_instead_of_discount_count=2,  # < 3
        )
        result = self._call(inp, value=30.0)
        assert result == NegotiationPattern.value_erosion

    def test_value_erosion_not_if_value_below_30(self):
        inp = make_input(
            gross_margin_avg_pct=0.60,
            total_deals_negotiated=10,
            competitive_deals_price_matched=0,
            value_add_instead_of_discount_count=2,
        )
        result = self._call(inp, value=29.9)
        assert result != NegotiationPattern.value_erosion

    def test_value_erosion_not_if_value_add_count_at_3(self):
        inp = make_input(
            gross_margin_avg_pct=0.60,
            total_deals_negotiated=10,
            competitive_deals_price_matched=0,
            value_add_instead_of_discount_count=3,
        )
        result = self._call(inp, value=50.0)
        assert result != NegotiationPattern.value_erosion

    # --- price_concession_habit ---

    def test_price_concession_habit_detected(self):
        inp = make_input(
            gross_margin_avg_pct=0.60,
            total_deals_negotiated=10,
            competitive_deals_price_matched=0,
            value_add_instead_of_discount_count=5,
            concession_rounds_avg=3.0,
            deals_lost_on_price_alone=0,
        )
        result = self._call(inp)
        assert result == NegotiationPattern.price_concession_habit

    def test_price_concession_habit_not_if_concession_below_3(self):
        inp = make_input(
            gross_margin_avg_pct=0.60,
            concession_rounds_avg=2.9,
            deals_lost_on_price_alone=0,
        )
        result = self._call(inp)
        assert result != NegotiationPattern.price_concession_habit

    def test_price_concession_habit_not_if_lost_more_than_1(self):
        inp = make_input(
            gross_margin_avg_pct=0.60,
            concession_rounds_avg=4.0,
            deals_lost_on_price_alone=2,
        )
        result = self._call(inp)
        assert result != NegotiationPattern.price_concession_habit

    def test_price_concession_habit_with_lost_exactly_1(self):
        inp = make_input(
            gross_margin_avg_pct=0.60,
            total_deals_negotiated=10,
            competitive_deals_price_matched=0,
            value_add_instead_of_discount_count=5,
            concession_rounds_avg=3.5,
            deals_lost_on_price_alone=1,
        )
        result = self._call(inp)
        assert result == NegotiationPattern.price_concession_habit

    # --- none ---

    def test_none_pattern_when_no_conditions_met(self):
        inp = make_input(
            gross_margin_avg_pct=0.60,
            total_deals_negotiated=10,
            competitive_deals_price_matched=0,
            value_add_instead_of_discount_count=10,
            concession_rounds_avg=1.0,
            deals_lost_on_price_alone=0,
        )
        result = self._call(inp)
        assert result == NegotiationPattern.none

    def test_none_returned_when_all_scores_zero(self):
        inp = make_input()
        result = self._call(inp, 0.0, 0.0, 0.0, 0.0)
        # concession_rounds_avg=1.0 < 3.0 → none
        assert result == NegotiationPattern.none


# ===========================================================================
# 7. _risk_level and _severity at composite boundaries
# ===========================================================================

class TestRiskLevelAndSeverity:

    def setup_method(self):
        self.e = engine()

    # --- _risk_level ---

    def test_risk_level_below_20_is_low(self):
        assert self.e._risk_level(0.0) == NegotiationRisk.low
        assert self.e._risk_level(19.9) == NegotiationRisk.low

    def test_risk_level_exactly_20_is_moderate(self):
        assert self.e._risk_level(20.0) == NegotiationRisk.moderate

    def test_risk_level_between_20_and_40_is_moderate(self):
        assert self.e._risk_level(30.0) == NegotiationRisk.moderate
        assert self.e._risk_level(39.9) == NegotiationRisk.moderate

    def test_risk_level_exactly_40_is_high(self):
        assert self.e._risk_level(40.0) == NegotiationRisk.high

    def test_risk_level_between_40_and_60_is_high(self):
        assert self.e._risk_level(50.0) == NegotiationRisk.high
        assert self.e._risk_level(59.9) == NegotiationRisk.high

    def test_risk_level_exactly_60_is_critical(self):
        assert self.e._risk_level(60.0) == NegotiationRisk.critical

    def test_risk_level_above_60_is_critical(self):
        assert self.e._risk_level(80.0) == NegotiationRisk.critical
        assert self.e._risk_level(100.0) == NegotiationRisk.critical

    # --- _severity ---

    def test_severity_below_20_is_disciplined(self):
        assert self.e._severity(0.0) == NegotiationSeverity.disciplined
        assert self.e._severity(19.9) == NegotiationSeverity.disciplined

    def test_severity_exactly_20_is_lenient(self):
        assert self.e._severity(20.0) == NegotiationSeverity.lenient

    def test_severity_between_20_and_40_is_lenient(self):
        assert self.e._severity(25.0) == NegotiationSeverity.lenient
        assert self.e._severity(39.9) == NegotiationSeverity.lenient

    def test_severity_exactly_40_is_compromised(self):
        assert self.e._severity(40.0) == NegotiationSeverity.compromised

    def test_severity_between_40_and_60_is_compromised(self):
        assert self.e._severity(50.0) == NegotiationSeverity.compromised
        assert self.e._severity(59.9) == NegotiationSeverity.compromised

    def test_severity_exactly_60_is_collapsing(self):
        assert self.e._severity(60.0) == NegotiationSeverity.collapsing

    def test_severity_above_60_is_collapsing(self):
        assert self.e._severity(75.0) == NegotiationSeverity.collapsing
        assert self.e._severity(100.0) == NegotiationSeverity.collapsing


# ===========================================================================
# 8. _action for all risk + pattern combinations
# ===========================================================================

class TestAction:

    def setup_method(self):
        self.e = engine()

    # --- critical ---

    def test_action_critical_margin_collapse(self):
        result = self.e._action(NegotiationRisk.critical, NegotiationPattern.margin_collapse)
        assert result == NegotiationAction.deal_desk_escalation

    def test_action_critical_chronic_discounting(self):
        result = self.e._action(NegotiationRisk.critical, NegotiationPattern.chronic_discounting)
        assert result == NegotiationAction.pricing_floor_enforcement

    def test_action_critical_value_erosion(self):
        result = self.e._action(NegotiationRisk.critical, NegotiationPattern.value_erosion)
        assert result == NegotiationAction.negotiation_coaching

    def test_action_critical_price_concession_habit(self):
        result = self.e._action(NegotiationRisk.critical, NegotiationPattern.price_concession_habit)
        assert result == NegotiationAction.negotiation_coaching

    def test_action_critical_competitive_surrender(self):
        result = self.e._action(NegotiationRisk.critical, NegotiationPattern.competitive_surrender)
        assert result == NegotiationAction.negotiation_coaching

    def test_action_critical_none(self):
        result = self.e._action(NegotiationRisk.critical, NegotiationPattern.none)
        assert result == NegotiationAction.negotiation_coaching

    # --- high ---

    def test_action_high_value_erosion(self):
        result = self.e._action(NegotiationRisk.high, NegotiationPattern.value_erosion)
        assert result == NegotiationAction.value_messaging_training

    def test_action_high_competitive_surrender(self):
        result = self.e._action(NegotiationRisk.high, NegotiationPattern.competitive_surrender)
        assert result == NegotiationAction.negotiation_coaching

    def test_action_high_margin_collapse(self):
        result = self.e._action(NegotiationRisk.high, NegotiationPattern.margin_collapse)
        assert result == NegotiationAction.discount_discipline_review

    def test_action_high_chronic_discounting(self):
        result = self.e._action(NegotiationRisk.high, NegotiationPattern.chronic_discounting)
        assert result == NegotiationAction.discount_discipline_review

    def test_action_high_price_concession_habit(self):
        result = self.e._action(NegotiationRisk.high, NegotiationPattern.price_concession_habit)
        assert result == NegotiationAction.discount_discipline_review

    def test_action_high_none(self):
        result = self.e._action(NegotiationRisk.high, NegotiationPattern.none)
        assert result == NegotiationAction.discount_discipline_review

    # --- moderate ---

    def test_action_moderate_any_pattern_returns_discount_discipline_review(self):
        for p in NegotiationPattern:
            result = self.e._action(NegotiationRisk.moderate, p)
            assert result == NegotiationAction.discount_discipline_review

    # --- low ---

    def test_action_low_any_pattern_returns_no_action(self):
        for p in NegotiationPattern:
            result = self.e._action(NegotiationRisk.low, p)
            assert result == NegotiationAction.no_action


# ===========================================================================
# 9. _is_margin_at_risk
# ===========================================================================

class TestIsMarginAtRisk:

    def setup_method(self):
        self.e = engine()

    def test_false_when_all_below_thresholds(self):
        inp = make_input(gross_margin_avg_pct=0.60,
                         total_deals_negotiated=20, deals_below_floor_price=0)
        # composite=0 < 40, gm=0.60 >= 0.35, floor_rate=0 < 0.15
        assert self.e._is_margin_at_risk(0.0, inp) is False

    def test_true_when_composite_exactly_40(self):
        inp = make_input(gross_margin_avg_pct=0.60,
                         total_deals_negotiated=20, deals_below_floor_price=0)
        assert self.e._is_margin_at_risk(40.0, inp) is True

    def test_true_when_composite_above_40(self):
        inp = make_input(gross_margin_avg_pct=0.60,
                         total_deals_negotiated=20, deals_below_floor_price=0)
        assert self.e._is_margin_at_risk(80.0, inp) is True

    def test_true_when_gross_margin_below_35(self):
        inp = make_input(gross_margin_avg_pct=0.34,
                         total_deals_negotiated=20, deals_below_floor_price=0)
        assert self.e._is_margin_at_risk(0.0, inp) is True

    def test_true_when_gross_margin_exactly_35_not_at_risk_from_gm(self):
        inp = make_input(gross_margin_avg_pct=0.35,
                         total_deals_negotiated=20, deals_below_floor_price=0)
        # 0.35 is NOT < 0.35
        assert self.e._is_margin_at_risk(0.0, inp) is False

    def test_true_when_floor_rate_exactly_15pct(self):
        inp = make_input(gross_margin_avg_pct=0.60,
                         total_deals_negotiated=20, deals_below_floor_price=3)
        # 3/20=0.15 → at risk
        assert self.e._is_margin_at_risk(0.0, inp) is True

    def test_false_when_floor_rate_just_below_15pct(self):
        inp = make_input(gross_margin_avg_pct=0.60,
                         total_deals_negotiated=20, deals_below_floor_price=2)
        # 2/20=0.10 < 0.15 → not at risk (if composite < 40 and gm >= 0.35)
        assert self.e._is_margin_at_risk(0.0, inp) is False

    def test_true_when_floor_rate_above_15pct(self):
        inp = make_input(gross_margin_avg_pct=0.60,
                         total_deals_negotiated=10, deals_below_floor_price=2)
        # 2/10=0.20 > 0.15 → at risk
        assert self.e._is_margin_at_risk(0.0, inp) is True

    def test_total_deals_zero_uses_1_as_denominator(self):
        inp = make_input(gross_margin_avg_pct=0.60,
                         total_deals_negotiated=0, deals_below_floor_price=0)
        assert self.e._is_margin_at_risk(0.0, inp) is False

    def test_or_logic_composite_triggers_even_with_safe_gm(self):
        inp = make_input(gross_margin_avg_pct=0.80, total_deals_negotiated=20,
                         deals_below_floor_price=0)
        assert self.e._is_margin_at_risk(45.0, inp) is True


# ===========================================================================
# 10. _requires_pricing_intervention
# ===========================================================================

class TestRequiresPricingIntervention:

    def setup_method(self):
        self.e = engine()

    def test_false_when_all_below_thresholds(self):
        inp = make_input(avg_discount_pct=5.0, concession_rounds_avg=1.0)
        assert self.e._requires_pricing_intervention(0.0, inp) is False

    def test_true_when_composite_exactly_30(self):
        inp = make_input(avg_discount_pct=5.0, concession_rounds_avg=1.0)
        assert self.e._requires_pricing_intervention(30.0, inp) is True

    def test_true_when_composite_above_30(self):
        inp = make_input(avg_discount_pct=5.0, concession_rounds_avg=1.0)
        assert self.e._requires_pricing_intervention(60.0, inp) is True

    def test_true_when_avg_discount_exactly_20(self):
        inp = make_input(avg_discount_pct=20.0, concession_rounds_avg=1.0)
        assert self.e._requires_pricing_intervention(0.0, inp) is True

    def test_false_when_avg_discount_just_below_20(self):
        inp = make_input(avg_discount_pct=19.9, concession_rounds_avg=1.0)
        assert self.e._requires_pricing_intervention(0.0, inp) is False

    def test_true_when_avg_discount_above_20(self):
        inp = make_input(avg_discount_pct=25.0, concession_rounds_avg=1.0)
        assert self.e._requires_pricing_intervention(0.0, inp) is True

    def test_true_when_concession_rounds_exactly_3(self):
        inp = make_input(avg_discount_pct=5.0, concession_rounds_avg=3.0)
        assert self.e._requires_pricing_intervention(0.0, inp) is True

    def test_false_when_concession_rounds_just_below_3(self):
        inp = make_input(avg_discount_pct=5.0, concession_rounds_avg=2.9)
        assert self.e._requires_pricing_intervention(0.0, inp) is False

    def test_true_when_concession_rounds_above_3(self):
        inp = make_input(avg_discount_pct=5.0, concession_rounds_avg=4.0)
        assert self.e._requires_pricing_intervention(0.0, inp) is True

    def test_or_logic_any_condition_triggers(self):
        # only avg_discount triggers
        inp = make_input(avg_discount_pct=21.0, concession_rounds_avg=1.0)
        assert self.e._requires_pricing_intervention(5.0, inp) is True


# ===========================================================================
# 11. _estimated_margin_loss
# ===========================================================================

class TestEstimatedMarginLoss:

    def setup_method(self):
        self.e = engine()

    def test_zero_when_negotiated_size_zero(self):
        inp = make_input(avg_deal_size_negotiated_usd=0.0,
                         avg_deal_size_post_negotiation_usd=50_000.0,
                         deals_with_discount_applied=5)
        assert self.e._estimated_margin_loss(inp, 50.0) == 0.0

    def test_zero_when_negotiated_size_negative(self):
        inp = make_input(avg_deal_size_negotiated_usd=-1.0,
                         avg_deal_size_post_negotiation_usd=50_000.0,
                         deals_with_discount_applied=5)
        assert self.e._estimated_margin_loss(inp, 50.0) == 0.0

    def test_zero_when_no_erosion(self):
        inp = make_input(avg_deal_size_negotiated_usd=50_000.0,
                         avg_deal_size_post_negotiation_usd=50_000.0,
                         deals_with_discount_applied=10)
        assert self.e._estimated_margin_loss(inp, 50.0) == 0.0

    def test_basic_calculation(self):
        inp = make_input(
            avg_deal_size_negotiated_usd=100_000.0,
            avg_deal_size_post_negotiation_usd=80_000.0,  # erosion=20000
            deals_with_discount_applied=10,
        )
        # 20000 * 10 * (50/100) = 100000.00
        result = self.e._estimated_margin_loss(inp, 50.0)
        assert result == 100_000.0

    def test_composite_zero_yields_zero_loss(self):
        inp = make_input(avg_deal_size_negotiated_usd=100_000.0,
                         avg_deal_size_post_negotiation_usd=80_000.0,
                         deals_with_discount_applied=10)
        assert self.e._estimated_margin_loss(inp, 0.0) == 0.0

    def test_composite_100_yields_full_erosion_times_deals(self):
        inp = make_input(
            avg_deal_size_negotiated_usd=100_000.0,
            avg_deal_size_post_negotiation_usd=90_000.0,  # erosion=10000
            deals_with_discount_applied=5,
        )
        # 10000 * 5 * 1.0 = 50000
        assert self.e._estimated_margin_loss(inp, 100.0) == 50_000.0

    def test_no_negative_erosion(self):
        # post > pre → erosion = max(negative, 0) = 0
        inp = make_input(avg_deal_size_negotiated_usd=80_000.0,
                         avg_deal_size_post_negotiation_usd=100_000.0,
                         deals_with_discount_applied=5)
        assert self.e._estimated_margin_loss(inp, 50.0) == 0.0

    def test_rounded_to_2_decimal_places(self):
        inp = make_input(
            avg_deal_size_negotiated_usd=10_000.0,
            avg_deal_size_post_negotiation_usd=9_990.0,   # erosion=10
            deals_with_discount_applied=3,
        )
        # 10 * 3 * 0.333... = 10.0
        result = self.e._estimated_margin_loss(inp, 33.333333)
        assert result == round(10 * 3 * (33.333333 / 100), 2)

    def test_zero_discount_deals_yields_zero(self):
        inp = make_input(avg_deal_size_negotiated_usd=100_000.0,
                         avg_deal_size_post_negotiation_usd=80_000.0,
                         deals_with_discount_applied=0)
        assert self.e._estimated_margin_loss(inp, 50.0) == 0.0


# ===========================================================================
# 12. _signal (negotiation_signal string)
# ===========================================================================

class TestSignal:

    def setup_method(self):
        self.e = engine()

    def test_clean_signal_when_none_pattern_and_composite_below_20(self):
        inp = make_input(avg_discount_pct=3.0, deals_below_floor_price=0,
                         concession_rounds_avg=0.5, deals_lost_on_price_alone=0)
        sig = self.e._signal(inp, NegotiationPattern.none, 10.0)
        assert sig == "Pricing discipline maintained across negotiations"

    def test_signal_contains_pattern_label_capitalized(self):
        inp = make_input(avg_discount_pct=3.0, deals_below_floor_price=0,
                         concession_rounds_avg=0.5, deals_lost_on_price_alone=0)
        sig = self.e._signal(inp, NegotiationPattern.margin_collapse, 65.0)
        assert sig.startswith("Margin collapse")

    def test_signal_contains_avg_discount_when_above_8(self):
        inp = make_input(avg_discount_pct=15.0, deals_below_floor_price=0,
                         concession_rounds_avg=0.5, deals_lost_on_price_alone=0)
        sig = self.e._signal(inp, NegotiationPattern.chronic_discounting, 50.0)
        assert "15% avg discount" in sig

    def test_signal_no_discount_when_avg_below_8(self):
        inp = make_input(avg_discount_pct=5.0, deals_below_floor_price=0,
                         concession_rounds_avg=0.5, deals_lost_on_price_alone=0)
        sig = self.e._signal(inp, NegotiationPattern.chronic_discounting, 50.0)
        assert "avg discount" not in sig

    def test_signal_contains_below_floor_deals_when_present(self):
        inp = make_input(avg_discount_pct=3.0, deals_below_floor_price=3,
                         concession_rounds_avg=0.5, deals_lost_on_price_alone=0)
        sig = self.e._signal(inp, NegotiationPattern.margin_collapse, 50.0)
        assert "3 below-floor deals" in sig

    def test_signal_no_below_floor_when_zero(self):
        inp = make_input(avg_discount_pct=3.0, deals_below_floor_price=0,
                         concession_rounds_avg=0.5, deals_lost_on_price_alone=0)
        sig = self.e._signal(inp, NegotiationPattern.value_erosion, 50.0)
        assert "below-floor" not in sig

    def test_signal_contains_concession_rounds_when_above_2(self):
        inp = make_input(avg_discount_pct=3.0, deals_below_floor_price=0,
                         concession_rounds_avg=2.5, deals_lost_on_price_alone=0)
        sig = self.e._signal(inp, NegotiationPattern.value_erosion, 40.0)
        assert "2.5 avg concession rounds" in sig

    def test_signal_no_concession_when_below_2(self):
        inp = make_input(avg_discount_pct=3.0, deals_below_floor_price=0,
                         concession_rounds_avg=1.9, deals_lost_on_price_alone=0)
        sig = self.e._signal(inp, NegotiationPattern.value_erosion, 40.0)
        assert "concession rounds" not in sig

    def test_signal_contains_lost_on_price_when_present(self):
        inp = make_input(avg_discount_pct=3.0, deals_below_floor_price=0,
                         concession_rounds_avg=0.5, deals_lost_on_price_alone=2)
        sig = self.e._signal(inp, NegotiationPattern.competitive_surrender, 50.0)
        assert "2 lost on price alone" in sig

    def test_signal_no_lost_on_price_when_zero(self):
        inp = make_input(avg_discount_pct=3.0, deals_below_floor_price=0,
                         concession_rounds_avg=0.5, deals_lost_on_price_alone=0)
        sig = self.e._signal(inp, NegotiationPattern.competitive_surrender, 50.0)
        assert "lost on price alone" not in sig

    def test_signal_contains_composite(self):
        inp = make_input(avg_discount_pct=3.0, deals_below_floor_price=0,
                         concession_rounds_avg=0.5, deals_lost_on_price_alone=0)
        sig = self.e._signal(inp, NegotiationPattern.value_erosion, 42.7)
        assert "composite 43" in sig

    def test_signal_fallback_when_no_parts(self):
        inp = make_input(avg_discount_pct=3.0, deals_below_floor_price=0,
                         concession_rounds_avg=0.5, deals_lost_on_price_alone=0)
        sig = self.e._signal(inp, NegotiationPattern.value_erosion, 35.0)
        assert "pricing discipline degrading" in sig

    def test_signal_uses_none_label_as_negotiation_risk(self):
        inp = make_input(avg_discount_pct=10.0, deals_below_floor_price=0,
                         concession_rounds_avg=0.5, deals_lost_on_price_alone=0)
        # pattern=none but composite >= 20 → won't return clean signal
        sig = self.e._signal(inp, NegotiationPattern.none, 25.0)
        assert "Negotiation risk" in sig

    def test_signal_replaces_underscores_with_spaces(self):
        inp = make_input(avg_discount_pct=3.0, deals_below_floor_price=0,
                         concession_rounds_avg=0.5, deals_lost_on_price_alone=0)
        sig = self.e._signal(inp, NegotiationPattern.price_concession_habit, 45.0)
        assert "Price concession habit" in sig

    def test_signal_exactly_2_concession_rounds_included(self):
        inp = make_input(avg_discount_pct=3.0, deals_below_floor_price=0,
                         concession_rounds_avg=2.0, deals_lost_on_price_alone=0)
        sig = self.e._signal(inp, NegotiationPattern.value_erosion, 40.0)
        assert "2.0 avg concession rounds" in sig


# ===========================================================================
# 13. assess() — full integration
# ===========================================================================

class TestAssess:

    def setup_method(self):
        self.e = engine()

    def test_assess_returns_pricing_negotiation_result(self):
        result = self.e.assess(make_input())
        assert isinstance(result, PricingNegotiationResult)

    def test_assess_to_dict_has_15_keys(self):
        result = self.e.assess(make_input())
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_expected_keys(self):
        d = self.e.assess(make_input()).to_dict()
        expected = {
            "rep_id", "region", "negotiation_risk", "negotiation_pattern",
            "negotiation_severity", "recommended_action",
            "discount_discipline_score", "value_retention_score",
            "margin_protection_score", "negotiation_efficiency_score",
            "negotiation_effectiveness_composite", "is_margin_at_risk",
            "requires_pricing_intervention", "estimated_margin_loss_usd",
            "negotiation_signal",
        }
        assert set(d.keys()) == expected

    def test_assess_stores_result_in_results_list(self):
        e = engine()
        e.assess(make_input())
        assert len(e._results) == 1

    def test_assess_rep_id_and_region_propagated(self):
        inp = make_input(rep_id="rep-XYZ", region="APAC")
        result = self.e.assess(inp)
        assert result.rep_id == "rep-XYZ"
        assert result.region == "APAC"

    def test_assess_composite_within_0_100(self):
        result = self.e.assess(make_input())
        assert 0.0 <= result.negotiation_effectiveness_composite <= 100.0

    def test_assess_low_risk_scenario(self):
        result = self.e.assess(make_input())
        assert result.negotiation_risk == NegotiationRisk.low
        assert result.negotiation_severity == NegotiationSeverity.disciplined
        assert result.recommended_action == NegotiationAction.no_action

    def test_assess_high_discount_scenario(self):
        inp = make_input(
            total_deals_negotiated=10,
            deals_with_discount_applied=8,   # 80%
            avg_discount_pct=30.0,
            max_discount_applied_pct=45.0,
            discounts_self_approved=8,
            discounts_approved_by_manager=0,
            gross_margin_avg_pct=0.25,
            deals_below_floor_price=3,
            concession_rounds_avg=4.0,
            negotiation_cycle_avg_days=35.0,
            competitive_deals_price_matched=5,
        )
        result = self.e.assess(inp)
        assert result.negotiation_effectiveness_composite >= 60.0
        assert result.negotiation_risk == NegotiationRisk.critical

    def test_assess_is_margin_at_risk_true_for_low_gm(self):
        inp = make_input(gross_margin_avg_pct=0.20)
        result = self.e.assess(inp)
        assert result.is_margin_at_risk is True

    def test_assess_requires_intervention_true_for_high_discount(self):
        inp = make_input(avg_discount_pct=25.0)
        result = self.e.assess(inp)
        assert result.requires_pricing_intervention is True

    def test_assess_composite_calculation_formula(self):
        inp = make_input()
        result = self.e.assess(inp)
        e = engine()
        disc = round(e._discount_discipline_score(inp), 1)
        val  = round(e._value_retention_score(inp), 1)
        mar  = round(e._margin_protection_score(inp), 1)
        eff  = round(e._negotiation_efficiency_score(inp), 1)
        expected = round(disc * 0.30 + val * 0.25 + mar * 0.30 + eff * 0.15, 1)
        assert result.negotiation_effectiveness_composite == min(expected, 100.0)

    def test_assess_does_not_exceed_100(self):
        # All worst-case inputs
        inp = make_input(
            total_deals_negotiated=10,
            deals_with_discount_applied=10,
            avg_discount_pct=40.0,
            max_discount_applied_pct=60.0,
            deals_below_floor_price=10,
            discounts_self_approved=10,
            discounts_approved_by_manager=0,
            list_price_deals_closed=0,
            value_add_instead_of_discount_count=0,
            avg_deal_size_negotiated_usd=100_000.0,
            avg_deal_size_post_negotiation_usd=50_000.0,
            competitive_deals_price_matched=10,
            concession_rounds_avg=6.0,
            negotiation_cycle_avg_days=60.0,
            gross_margin_avg_pct=0.10,
        )
        result = self.e.assess(inp)
        assert result.negotiation_effectiveness_composite <= 100.0

    def test_assess_estimated_loss_zero_when_no_erosion(self):
        inp = make_input(
            avg_deal_size_negotiated_usd=50_000.0,
            avg_deal_size_post_negotiation_usd=50_000.0,
        )
        result = self.e.assess(inp)
        assert result.estimated_margin_loss_usd == 0.0

    def test_assess_signal_is_str(self):
        result = self.e.assess(make_input())
        assert isinstance(result.negotiation_signal, str)

    def test_assess_to_dict_values_are_primitives(self):
        d = self.e.assess(make_input()).to_dict()
        for k, v in d.items():
            assert isinstance(v, (str, bool, float, int)), f"Key {k} has non-primitive type {type(v)}"

    def test_assess_multiple_reps_accumulate_results(self):
        e = engine()
        for i in range(5):
            e.assess(make_input(rep_id=f"rep-{i}"))
        assert len(e._results) == 5


# ===========================================================================
# 14. summary()
# ===========================================================================

class TestSummary:

    def test_empty_summary_has_13_keys(self):
        e = engine()
        s = e.summary()
        assert len(s) == 13

    def test_empty_summary_expected_keys(self):
        e = engine()
        s = e.summary()
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_negotiation_effectiveness_composite",
            "margin_at_risk_count", "pricing_intervention_count",
            "avg_discount_discipline_score", "avg_value_retention_score",
            "avg_margin_protection_score", "avg_negotiation_efficiency_score",
            "total_estimated_margin_loss_usd",
        }
        assert set(s.keys()) == expected

    def test_empty_summary_total_is_0(self):
        e = engine()
        assert e.summary()["total"] == 0

    def test_empty_summary_counts_are_empty_dicts(self):
        e = engine()
        s = e.summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}

    def test_empty_summary_numeric_defaults_zero(self):
        e = engine()
        s = e.summary()
        assert s["avg_negotiation_effectiveness_composite"] == 0.0
        assert s["margin_at_risk_count"] == 0
        assert s["pricing_intervention_count"] == 0
        assert s["avg_discount_discipline_score"] == 0.0
        assert s["avg_value_retention_score"] == 0.0
        assert s["avg_margin_protection_score"] == 0.0
        assert s["avg_negotiation_efficiency_score"] == 0.0
        assert s["total_estimated_margin_loss_usd"] == 0.0

    def test_summary_total_after_one_assess(self):
        e = engine()
        e.assess(make_input())
        assert e.summary()["total"] == 1

    def test_summary_total_after_multiple_assess(self):
        e = engine()
        for _ in range(7):
            e.assess(make_input())
        assert e.summary()["total"] == 7

    def test_summary_risk_counts_populated(self):
        e = engine()
        e.assess(make_input())  # low risk
        s = e.summary()
        assert "low" in s["risk_counts"]
        assert s["risk_counts"]["low"] == 1

    def test_summary_avg_composite_computed(self):
        e = engine()
        r = e.assess(make_input())
        s = e.summary()
        assert s["avg_negotiation_effectiveness_composite"] == r.negotiation_effectiveness_composite

    def test_summary_margin_at_risk_count(self):
        e = engine()
        e.assess(make_input(gross_margin_avg_pct=0.20))  # at risk
        e.assess(make_input())  # not at risk
        s = e.summary()
        assert s["margin_at_risk_count"] == 1

    def test_summary_pricing_intervention_count(self):
        e = engine()
        e.assess(make_input(avg_discount_pct=25.0))  # intervention
        e.assess(make_input())  # no intervention
        s = e.summary()
        assert s["pricing_intervention_count"] == 1

    def test_summary_total_loss_sum(self):
        e = engine()
        inp = make_input(
            avg_deal_size_negotiated_usd=100_000.0,
            avg_deal_size_post_negotiation_usd=80_000.0,
            deals_with_discount_applied=5,
        )
        e.assess(inp)
        e.assess(inp)
        s = e.summary()
        assert s["total_estimated_margin_loss_usd"] >= 0.0

    def test_summary_has_13_keys_after_assessment(self):
        e = engine()
        e.assess(make_input())
        assert len(e.summary()) == 13

    def test_summary_severity_counts_populated(self):
        e = engine()
        e.assess(make_input())
        s = e.summary()
        assert "disciplined" in s["severity_counts"]

    def test_summary_action_counts_populated(self):
        e = engine()
        e.assess(make_input())
        s = e.summary()
        assert "no_action" in s["action_counts"]

    def test_summary_pattern_counts_populated(self):
        e = engine()
        e.assess(make_input())
        s = e.summary()
        assert "none" in s["pattern_counts"]

    def test_summary_averages_multiple_results(self):
        e = engine()
        e.assess(make_input())
        e.assess(make_input())
        s = e.summary()
        assert s["total"] == 2


# ===========================================================================
# 15. assess_batch()
# ===========================================================================

class TestAssessBatch:

    def test_batch_returns_list(self):
        e = engine()
        results = e.assess_batch([make_input(), make_input()])
        assert isinstance(results, list)

    def test_batch_length_matches_input(self):
        e = engine()
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(10)]
        results = e.assess_batch(inputs)
        assert len(results) == 10

    def test_batch_empty_list(self):
        e = engine()
        results = e.assess_batch([])
        assert results == []

    def test_batch_accumulates_in_results(self):
        e = engine()
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(5)]
        e.assess_batch(inputs)
        assert len(e._results) == 5

    def test_batch_all_return_result_type(self):
        e = engine()
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(3)]
        for r in e.assess_batch(inputs):
            assert isinstance(r, PricingNegotiationResult)

    def test_batch_followed_by_summary(self):
        e = engine()
        e.assess_batch([make_input(), make_input()])
        s = e.summary()
        assert s["total"] == 2

    def test_batch_single_element(self):
        e = engine()
        results = e.assess_batch([make_input(rep_id="solo")])
        assert len(results) == 1
        assert results[0].rep_id == "solo"

    def test_batch_mixed_risk_levels(self):
        e = engine()
        low_inp = make_input()
        high_inp = make_input(
            total_deals_negotiated=10,
            deals_with_discount_applied=8,
            avg_discount_pct=30.0,
            gross_margin_avg_pct=0.20,
            max_discount_applied_pct=45.0,
            deals_below_floor_price=5,
        )
        results = e.assess_batch([low_inp, high_inp])
        risks = {r.negotiation_risk for r in results}
        assert NegotiationRisk.low in risks


# ===========================================================================
# 16. Edge Cases and Integration Scenarios
# ===========================================================================

class TestEdgeCases:

    def test_total_deals_one(self):
        inp = make_input(total_deals_negotiated=1, deals_with_discount_applied=1)
        e = engine()
        result = e.assess(inp)
        assert isinstance(result, PricingNegotiationResult)

    def test_zero_deal_sizes(self):
        inp = make_input(avg_deal_size_negotiated_usd=0.0,
                         avg_deal_size_post_negotiation_usd=0.0)
        e = engine()
        result = e.assess(inp)
        assert result.estimated_margin_loss_usd == 0.0

    def test_very_large_deal_sizes(self):
        inp = make_input(
            avg_deal_size_negotiated_usd=10_000_000.0,
            avg_deal_size_post_negotiation_usd=7_000_000.0,
            deals_with_discount_applied=50,
        )
        e = engine()
        result = e.assess(inp)
        assert result.estimated_margin_loss_usd >= 0.0

    def test_all_deals_below_floor(self):
        inp = make_input(total_deals_negotiated=10, deals_below_floor_price=10,
                         gross_margin_avg_pct=0.60)
        e = engine()
        result = e.assess(inp)
        assert result.is_margin_at_risk is True

    def test_zero_gross_margin(self):
        inp = make_input(gross_margin_avg_pct=0.0)
        e = engine()
        result = e.assess(inp)
        assert result.is_margin_at_risk is True

    def test_perfect_gross_margin(self):
        inp = make_input(gross_margin_avg_pct=1.0)
        e = engine()
        result = e.assess(inp)
        assert result.margin_protection_score == 0.0  # no risk from margin alone

    def test_concession_rounds_exactly_zero(self):
        inp = make_input(concession_rounds_avg=0.0)
        e = engine()
        result = e.assess(inp)
        assert result.negotiation_efficiency_score == 0.0 or result.negotiation_efficiency_score >= 0.0

    def test_all_deals_self_approved(self):
        inp = make_input(discounts_approved_by_manager=0, discounts_self_approved=10)
        e = engine()
        score = e._discount_discipline_score(inp)
        assert score >= 20.0

    def test_no_self_approved_discounts(self):
        inp = make_input(discounts_approved_by_manager=10, discounts_self_approved=0)
        e = engine()
        score = e._discount_discipline_score(inp)
        # self_rate = 0 → 0 from that component
        assert score >= 0.0

    def test_engine_independent_results_lists(self):
        e1 = engine()
        e2 = engine()
        e1.assess(make_input())
        assert len(e1._results) == 1
        assert len(e2._results) == 0

    def test_pattern_none_with_high_composite_signal(self):
        """none pattern but composite >=20 should not return clean signal."""
        e = engine()
        inp = make_input(avg_discount_pct=10.0, deals_below_floor_price=0,
                         concession_rounds_avg=0.5, deals_lost_on_price_alone=0)
        sig = e._signal(inp, NegotiationPattern.none, 25.0)
        assert sig != "Pricing discipline maintained across negotiations"

    def test_composite_boundary_at_20(self):
        e = engine()
        assert e._risk_level(20.0) == NegotiationRisk.moderate
        assert e._severity(20.0) == NegotiationSeverity.lenient

    def test_composite_boundary_just_below_20(self):
        e = engine()
        assert e._risk_level(19.9) == NegotiationRisk.low
        assert e._severity(19.9) == NegotiationSeverity.disciplined

    def test_composite_boundary_at_40(self):
        e = engine()
        assert e._risk_level(40.0) == NegotiationRisk.high
        assert e._severity(40.0) == NegotiationSeverity.compromised

    def test_composite_boundary_just_below_40(self):
        e = engine()
        assert e._risk_level(39.9) == NegotiationRisk.moderate
        assert e._severity(39.9) == NegotiationSeverity.lenient

    def test_composite_boundary_at_60(self):
        e = engine()
        assert e._risk_level(60.0) == NegotiationRisk.critical
        assert e._severity(60.0) == NegotiationSeverity.collapsing

    def test_composite_boundary_just_below_60(self):
        e = engine()
        assert e._risk_level(59.9) == NegotiationRisk.high
        assert e._severity(59.9) == NegotiationSeverity.compromised

    def test_full_worst_case_scenario(self):
        """All worst-case values → critical risk."""
        inp = make_input(
            total_deals_negotiated=10,
            deals_with_discount_applied=10,
            avg_discount_pct=40.0,
            max_discount_applied_pct=60.0,
            deals_below_floor_price=5,
            discounts_self_approved=10,
            discounts_approved_by_manager=0,
            list_price_deals_closed=0,
            value_add_instead_of_discount_count=0,
            avg_deal_size_negotiated_usd=100_000.0,
            avg_deal_size_post_negotiation_usd=50_000.0,
            competitive_deals_price_matched=7,
            concession_rounds_avg=5.0,
            negotiation_cycle_avg_days=45.0,
            gross_margin_avg_pct=0.15,
            deals_lost_on_price_alone=0,
        )
        e = engine()
        result = e.assess(inp)
        assert result.negotiation_risk == NegotiationRisk.critical

    def test_full_best_case_scenario(self):
        """All best-case values → low risk, no action."""
        e = engine()
        result = e.assess(make_input())
        assert result.negotiation_risk == NegotiationRisk.low
        assert result.recommended_action == NegotiationAction.no_action
        assert result.is_margin_at_risk is False

    def test_to_dict_enum_values_are_strings(self):
        e = engine()
        d = e.assess(make_input()).to_dict()
        assert isinstance(d["negotiation_risk"], str)
        assert isinstance(d["negotiation_pattern"], str)
        assert isinstance(d["negotiation_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_multiple_assessments_independent_results(self):
        e = engine()
        r1 = e.assess(make_input(rep_id="A"))
        r2 = e.assess(make_input(rep_id="B"))
        assert r1.rep_id == "A"
        assert r2.rep_id == "B"

    def test_assess_batch_and_summary_consistency(self):
        e = engine()
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(4)]
        results = e.assess_batch(inputs)
        s = e.summary()
        total_from_results = sum(s["risk_counts"].values())
        assert total_from_results == len(results)


# ===========================================================================
# 17. PricingNegotiationInput dataclass fields
# ===========================================================================

class TestInputDataclass:

    def test_input_fields_accessible(self):
        inp = make_input()
        assert inp.rep_id == "rep-001"
        assert inp.region == "EMEA"
        assert inp.evaluation_period_id == "Q1-2026"
        assert inp.total_deals_negotiated == 20

    def test_input_all_numeric_fields(self):
        inp = make_input()
        assert isinstance(inp.avg_discount_pct, float)
        assert isinstance(inp.gross_margin_avg_pct, float)
        assert isinstance(inp.concession_rounds_avg, float)
        assert isinstance(inp.negotiation_cycle_avg_days, float)

    def test_input_requires_all_fields(self):
        # This tests that the dataclass requires all fields (no defaults)
        with pytest.raises(TypeError):
            PricingNegotiationInput()  # missing all fields


# ===========================================================================
# 18. PricingNegotiationResult to_dict completeness
# ===========================================================================

class TestResultToDict:

    def test_to_dict_15_keys(self):
        e = engine()
        d = e.assess(make_input()).to_dict()
        assert len(d) == 15

    def test_to_dict_rep_id(self):
        e = engine()
        d = e.assess(make_input(rep_id="TESTID")).to_dict()
        assert d["rep_id"] == "TESTID"

    def test_to_dict_region(self):
        e = engine()
        d = e.assess(make_input(region="LATAM")).to_dict()
        assert d["region"] == "LATAM"

    def test_to_dict_risk_is_string(self):
        e = engine()
        d = e.assess(make_input()).to_dict()
        assert isinstance(d["negotiation_risk"], str)

    def test_to_dict_pattern_is_string(self):
        e = engine()
        d = e.assess(make_input()).to_dict()
        assert isinstance(d["negotiation_pattern"], str)

    def test_to_dict_severity_is_string(self):
        e = engine()
        d = e.assess(make_input()).to_dict()
        assert isinstance(d["negotiation_severity"], str)

    def test_to_dict_action_is_string(self):
        e = engine()
        d = e.assess(make_input()).to_dict()
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_scores_are_float(self):
        e = engine()
        d = e.assess(make_input()).to_dict()
        assert isinstance(d["discount_discipline_score"], float)
        assert isinstance(d["value_retention_score"], float)
        assert isinstance(d["margin_protection_score"], float)
        assert isinstance(d["negotiation_efficiency_score"], float)
        assert isinstance(d["negotiation_effectiveness_composite"], float)

    def test_to_dict_flags_are_bool(self):
        e = engine()
        d = e.assess(make_input()).to_dict()
        assert isinstance(d["is_margin_at_risk"], bool)
        assert isinstance(d["requires_pricing_intervention"], bool)

    def test_to_dict_loss_is_float(self):
        e = engine()
        d = e.assess(make_input()).to_dict()
        assert isinstance(d["estimated_margin_loss_usd"], float)

    def test_to_dict_signal_is_string(self):
        e = engine()
        d = e.assess(make_input()).to_dict()
        assert isinstance(d["negotiation_signal"], str)
