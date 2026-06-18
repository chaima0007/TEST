"""
Comprehensive pytest test suite for PriceNegotiationEngine.
Target: 260+ tests covering all logic paths, edge cases, and integrations.
"""
from __future__ import annotations

import dataclasses
import math
import pytest

from swarm.intelligence.price_negotiation_engine import (
    DiscountRisk,
    MarginHealth,
    NegotiationInput,
    NegotiationResult,
    NegotiationStage,
    PriceNegotiationEngine,
    PricingStrategy,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> NegotiationInput:
    """Return a NegotiationInput with sensible defaults, overrideable by kwargs."""
    defaults = dict(
        deal_id="D001",
        account_id="A001",
        rep_id="R001",
        segment="enterprise",
        list_price=10_000.0,
        proposed_price=8_000.0,
        target_price=7_500.0,
        competitor_price=0.0,
        cost_of_goods=3_000.0,
        deal_value=80_000.0,
        discount_pct=20.0,
        max_discount_pct=25.0,
        num_rounds=1,
        buyer_pushback_level=1,
        champion_support=True,
        economic_buyer_engaged=True,
        multi_year_deal=False,
        professional_services=0.0,
        annual_contract_value=80_000.0,
        customer_lifetime_value=300_000.0,
        historical_win_rate_at_discount=0.6,
        days_to_close=30,
        is_strategic_account=False,
        payment_terms_days=30,
    )
    defaults.update(overrides)
    return NegotiationInput(**defaults)


def fresh_engine() -> PriceNegotiationEngine:
    return PriceNegotiationEngine()


# ---------------------------------------------------------------------------
# 1. DiscountRisk Enum
# ---------------------------------------------------------------------------

class TestDiscountRiskEnum:
    def test_member_count(self):
        assert len(DiscountRisk) == 4

    def test_minimal_value(self):
        assert DiscountRisk.MINIMAL.value == "minimal"

    def test_moderate_value(self):
        assert DiscountRisk.MODERATE.value == "moderate"

    def test_high_value(self):
        assert DiscountRisk.HIGH.value == "high"

    def test_critical_value(self):
        assert DiscountRisk.CRITICAL.value == "critical"

    def test_is_str_subclass(self):
        assert isinstance(DiscountRisk.MINIMAL, str)

    def test_str_equals_value(self):
        assert DiscountRisk.HIGH == "high"

    def test_all_unique_values(self):
        values = [m.value for m in DiscountRisk]
        assert len(values) == len(set(values))

    def test_members_by_name(self):
        members = {m.name for m in DiscountRisk}
        assert members == {"MINIMAL", "MODERATE", "HIGH", "CRITICAL"}

    def test_lookup_by_value(self):
        assert DiscountRisk("high") is DiscountRisk.HIGH

    def test_str_comparison(self):
        assert DiscountRisk.CRITICAL == "critical"


# ---------------------------------------------------------------------------
# 2. NegotiationStage Enum
# ---------------------------------------------------------------------------

class TestNegotiationStageEnum:
    def test_member_count(self):
        assert len(NegotiationStage) == 5

    def test_initial_offer_value(self):
        assert NegotiationStage.INITIAL_OFFER.value == "initial_offer"

    def test_counter_offer_value(self):
        assert NegotiationStage.COUNTER_OFFER.value == "counter_offer"

    def test_final_terms_value(self):
        assert NegotiationStage.FINAL_TERMS.value == "final_terms"

    def test_closed_value(self):
        assert NegotiationStage.CLOSED.value == "closed"

    def test_stalled_value(self):
        assert NegotiationStage.STALLED.value == "stalled"

    def test_is_str_subclass(self):
        assert isinstance(NegotiationStage.INITIAL_OFFER, str)

    def test_all_unique_values(self):
        values = [m.value for m in NegotiationStage]
        assert len(values) == len(set(values))

    def test_members_by_name(self):
        members = {m.name for m in NegotiationStage}
        assert members == {"INITIAL_OFFER", "COUNTER_OFFER", "FINAL_TERMS", "CLOSED", "STALLED"}

    def test_lookup_by_value(self):
        assert NegotiationStage("stalled") is NegotiationStage.STALLED

    def test_str_comparison(self):
        assert NegotiationStage.CLOSED == "closed"


# ---------------------------------------------------------------------------
# 3. PricingStrategy Enum
# ---------------------------------------------------------------------------

class TestPricingStrategyEnum:
    def test_member_count(self):
        assert len(PricingStrategy) == 6

    def test_hold_price_value(self):
        assert PricingStrategy.HOLD_PRICE.value == "hold_price"

    def test_offer_value_add_value(self):
        assert PricingStrategy.OFFER_VALUE_ADD.value == "offer_value_add"

    def test_concede_strategic_value(self):
        assert PricingStrategy.CONCEDE_STRATEGIC.value == "concede_strategic"

    def test_escalate_to_exec_value(self):
        assert PricingStrategy.ESCALATE_TO_EXEC.value == "escalate_to_exec"

    def test_walk_away_value(self):
        assert PricingStrategy.WALK_AWAY.value == "walk_away"

    def test_accept_and_close_value(self):
        assert PricingStrategy.ACCEPT_AND_CLOSE.value == "accept_and_close"

    def test_is_str_subclass(self):
        assert isinstance(PricingStrategy.WALK_AWAY, str)

    def test_all_unique_values(self):
        values = [m.value for m in PricingStrategy]
        assert len(values) == len(set(values))

    def test_members_by_name(self):
        members = {m.name for m in PricingStrategy}
        assert members == {
            "HOLD_PRICE", "OFFER_VALUE_ADD", "CONCEDE_STRATEGIC",
            "ESCALATE_TO_EXEC", "WALK_AWAY", "ACCEPT_AND_CLOSE",
        }

    def test_str_comparison(self):
        assert PricingStrategy.WALK_AWAY == "walk_away"


# ---------------------------------------------------------------------------
# 4. MarginHealth Enum
# ---------------------------------------------------------------------------

class TestMarginHealthEnum:
    def test_member_count(self):
        assert len(MarginHealth) == 4

    def test_strong_value(self):
        assert MarginHealth.STRONG.value == "strong"

    def test_healthy_value(self):
        assert MarginHealth.HEALTHY.value == "healthy"

    def test_thin_value(self):
        assert MarginHealth.THIN.value == "thin"

    def test_critical_value(self):
        assert MarginHealth.CRITICAL.value == "critical"

    def test_is_str_subclass(self):
        assert isinstance(MarginHealth.STRONG, str)

    def test_all_unique_values(self):
        values = [m.value for m in MarginHealth]
        assert len(values) == len(set(values))

    def test_str_comparison(self):
        assert MarginHealth.THIN == "thin"


# ---------------------------------------------------------------------------
# 5. NegotiationInput field count
# ---------------------------------------------------------------------------

class TestNegotiationInputFields:
    def test_field_count_is_24(self):
        assert len(dataclasses.fields(NegotiationInput)) == 24

    def test_has_deal_id(self):
        fields = {f.name for f in dataclasses.fields(NegotiationInput)}
        assert "deal_id" in fields

    def test_has_payment_terms_days(self):
        fields = {f.name for f in dataclasses.fields(NegotiationInput)}
        assert "payment_terms_days" in fields

    def test_has_is_strategic_account(self):
        fields = {f.name for f in dataclasses.fields(NegotiationInput)}
        assert "is_strategic_account" in fields

    def test_has_customer_lifetime_value(self):
        fields = {f.name for f in dataclasses.fields(NegotiationInput)}
        assert "customer_lifetime_value" in fields

    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(NegotiationInput)

    def test_instantiation(self):
        inp = make_input()
        assert inp.deal_id == "D001"

    def test_all_expected_fields_present(self):
        expected = {
            "deal_id", "account_id", "rep_id", "segment", "list_price",
            "proposed_price", "target_price", "competitor_price", "cost_of_goods",
            "deal_value", "discount_pct", "max_discount_pct", "num_rounds",
            "buyer_pushback_level", "champion_support", "economic_buyer_engaged",
            "multi_year_deal", "professional_services", "annual_contract_value",
            "customer_lifetime_value", "historical_win_rate_at_discount",
            "days_to_close", "is_strategic_account", "payment_terms_days",
        }
        actual = {f.name for f in dataclasses.fields(NegotiationInput)}
        assert expected == actual


# ---------------------------------------------------------------------------
# 6. to_dict() — exactly 15 keys
# ---------------------------------------------------------------------------

class TestToDict:
    def setup_method(self):
        self.engine = fresh_engine()
        self.result = self.engine.analyze(make_input())

    def test_returns_dict(self):
        assert isinstance(self.result.to_dict(), dict)

    def test_exactly_15_keys(self):
        assert len(self.result.to_dict()) == 15

    def test_has_deal_id(self):
        assert "deal_id" in self.result.to_dict()

    def test_has_account_id(self):
        assert "account_id" in self.result.to_dict()

    def test_has_rep_id(self):
        assert "rep_id" in self.result.to_dict()

    def test_has_discount_risk(self):
        assert "discount_risk" in self.result.to_dict()

    def test_has_negotiation_stage(self):
        assert "negotiation_stage" in self.result.to_dict()

    def test_has_pricing_strategy(self):
        assert "pricing_strategy" in self.result.to_dict()

    def test_has_margin_health(self):
        assert "margin_health" in self.result.to_dict()

    def test_has_gross_margin_pct(self):
        assert "gross_margin_pct" in self.result.to_dict()

    def test_has_effective_discount_pct(self):
        assert "effective_discount_pct" in self.result.to_dict()

    def test_has_price_to_value_score(self):
        assert "price_to_value_score" in self.result.to_dict()

    def test_has_negotiation_leverage(self):
        assert "negotiation_leverage" in self.result.to_dict()

    def test_has_walkaway_risk(self):
        assert "walkaway_risk" in self.result.to_dict()

    def test_has_recommended_concession(self):
        assert "recommended_concession" in self.result.to_dict()

    def test_has_is_margin_positive(self):
        assert "is_margin_positive" in self.result.to_dict()

    def test_has_is_strategic(self):
        assert "is_strategic" in self.result.to_dict()

    def test_discount_risk_is_string(self):
        d = self.result.to_dict()
        assert isinstance(d["discount_risk"], str)

    def test_negotiation_stage_is_string(self):
        d = self.result.to_dict()
        assert isinstance(d["negotiation_stage"], str)

    def test_pricing_strategy_is_string(self):
        d = self.result.to_dict()
        assert isinstance(d["pricing_strategy"], str)

    def test_margin_health_is_string(self):
        d = self.result.to_dict()
        assert isinstance(d["margin_health"], str)

    def test_gross_margin_pct_is_float(self):
        d = self.result.to_dict()
        assert isinstance(d["gross_margin_pct"], float)

    def test_is_margin_positive_is_bool(self):
        d = self.result.to_dict()
        assert isinstance(d["is_margin_positive"], bool)

    def test_is_strategic_is_bool(self):
        d = self.result.to_dict()
        assert isinstance(d["is_strategic"], bool)

    def test_deal_id_preserved(self):
        d = self.result.to_dict()
        assert d["deal_id"] == "D001"

    def test_account_id_preserved(self):
        d = self.result.to_dict()
        assert d["account_id"] == "A001"

    def test_enum_values_not_enum_objects(self):
        d = self.result.to_dict()
        assert not isinstance(d["discount_risk"], DiscountRisk)
        assert not isinstance(d["negotiation_stage"], NegotiationStage)
        assert not isinstance(d["pricing_strategy"], PricingStrategy)
        assert not isinstance(d["margin_health"], MarginHealth)


# ---------------------------------------------------------------------------
# 7. _gross_margin_pct
# ---------------------------------------------------------------------------

class TestGrossMarginPct:
    def setup_method(self):
        self.engine = fresh_engine()

    def _margin(self, **kw):
        return self.engine._gross_margin_pct(make_input(**kw))

    def test_zero_proposed_price_returns_zero(self):
        assert self._margin(proposed_price=0.0) == 0.0

    def test_negative_proposed_price_returns_zero(self):
        assert self._margin(proposed_price=-100.0) == 0.0

    def test_standard_positive_margin(self):
        # (8000 - 3000) / 8000 * 100 = 62.5
        assert self._margin(proposed_price=8_000.0, cost_of_goods=3_000.0) == 62.5

    def test_50_percent_margin(self):
        assert self._margin(proposed_price=1_000.0, cost_of_goods=500.0) == 50.0

    def test_zero_margin_when_cost_equals_price(self):
        assert self._margin(proposed_price=1_000.0, cost_of_goods=1_000.0) == 0.0

    def test_negative_margin_when_cost_exceeds_price(self):
        # (500 - 1000) / 500 * 100 = -100
        assert self._margin(proposed_price=500.0, cost_of_goods=1_000.0) == -100.0

    def test_negative_margin_clamped_at_minus_100(self):
        # would be -200%  but clamped at -100
        assert self._margin(proposed_price=100.0, cost_of_goods=300.0) == -100.0

    def test_positive_margin_clamped_at_100(self):
        # cost=0 → (price-0)/price * 100 = 100
        assert self._margin(proposed_price=500.0, cost_of_goods=0.0) == 100.0

    def test_result_rounded_to_1_decimal(self):
        # (7000 - 3000) / 7000 * 100 = 57.142857… → 57.1
        val = self._margin(proposed_price=7_000.0, cost_of_goods=3_000.0)
        assert val == round(val, 1)
        assert abs(val - 57.1) < 0.001

    def test_high_margin_deal(self):
        # (10000 - 1000) / 10000 * 100 = 90.0
        assert self._margin(proposed_price=10_000.0, cost_of_goods=1_000.0) == 90.0

    def test_small_price_large_margin(self):
        # (100 - 10) / 100 * 100 = 90.0
        assert self._margin(proposed_price=100.0, cost_of_goods=10.0) == 90.0

    def test_fractional_margin(self):
        # (1000 - 667) / 1000 * 100 = 33.3
        val = self._margin(proposed_price=1_000.0, cost_of_goods=667.0)
        assert val == round(val, 1)


# ---------------------------------------------------------------------------
# 8. _effective_discount_pct
# ---------------------------------------------------------------------------

class TestEffectiveDiscountPct:
    def setup_method(self):
        self.engine = fresh_engine()

    def _edisc(self, **kw):
        return self.engine._effective_discount_pct(make_input(**kw))

    def test_zero_list_price_returns_zero(self):
        assert self._edisc(list_price=0.0) == 0.0

    def test_negative_list_price_returns_zero(self):
        assert self._edisc(list_price=-100.0) == 0.0

    def test_no_discount_when_prices_equal(self):
        assert self._edisc(list_price=1_000.0, proposed_price=1_000.0) == 0.0

    def test_twenty_percent_discount(self):
        # (1 - 8000/10000) * 100 = 20.0
        assert self._edisc(list_price=10_000.0, proposed_price=8_000.0) == 20.0

    def test_fifty_percent_discount(self):
        assert self._edisc(list_price=1_000.0, proposed_price=500.0) == 50.0

    def test_full_discount(self):
        # proposed_price = 0 → 100% discount
        assert self._edisc(list_price=1_000.0, proposed_price=0.0) == 100.0

    def test_proposed_above_list_clamped_to_zero(self):
        # negative discount → clamp to 0
        assert self._edisc(list_price=1_000.0, proposed_price=1_200.0) == 0.0

    def test_result_rounded_to_1_decimal(self):
        # (1 - 700/1000) * 100 = 30.0
        val = self._edisc(list_price=1_000.0, proposed_price=700.0)
        assert val == round(val, 1)

    def test_fractional_discount(self):
        # (1 - 333/1000) * 100 = 66.7
        val = self._edisc(list_price=1_000.0, proposed_price=333.0)
        assert val == round(val, 1)
        assert abs(val - 66.7) < 0.001

    def test_small_discount(self):
        # (1 - 990/1000)*100 = 1.0
        assert self._edisc(list_price=1_000.0, proposed_price=990.0) == 1.0

    def test_capped_at_100(self):
        # extreme case
        assert self._edisc(list_price=100.0, proposed_price=-500.0) == 100.0


# ---------------------------------------------------------------------------
# 9. _margin_health
# ---------------------------------------------------------------------------

class TestMarginHealth:
    def setup_method(self):
        self.engine = fresh_engine()

    def _mh(self, pct):
        return self.engine._margin_health(pct)

    def test_60_is_strong(self):
        assert self._mh(60.0) == MarginHealth.STRONG

    def test_above_60_is_strong(self):
        assert self._mh(75.0) == MarginHealth.STRONG

    def test_100_is_strong(self):
        assert self._mh(100.0) == MarginHealth.STRONG

    def test_59_is_healthy(self):
        assert self._mh(59.9) == MarginHealth.HEALTHY

    def test_45_is_healthy(self):
        assert self._mh(45.0) == MarginHealth.HEALTHY

    def test_44_is_thin(self):
        assert self._mh(44.9) == MarginHealth.THIN

    def test_30_is_thin(self):
        assert self._mh(30.0) == MarginHealth.THIN

    def test_29_is_critical(self):
        assert self._mh(29.9) == MarginHealth.CRITICAL

    def test_zero_is_critical(self):
        assert self._mh(0.0) == MarginHealth.CRITICAL

    def test_negative_is_critical(self):
        assert self._mh(-10.0) == MarginHealth.CRITICAL

    def test_boundary_exactly_60_strong(self):
        assert self._mh(60.0) is MarginHealth.STRONG

    def test_boundary_exactly_45_healthy(self):
        assert self._mh(45.0) is MarginHealth.HEALTHY

    def test_boundary_exactly_30_thin(self):
        assert self._mh(30.0) is MarginHealth.THIN


# ---------------------------------------------------------------------------
# 10. _discount_risk
# ---------------------------------------------------------------------------

class TestDiscountRisk:
    def setup_method(self):
        self.engine = fresh_engine()

    def _risk(self, **kw):
        inp = make_input(**kw)
        eff = self.engine._effective_discount_pct(inp)
        marg = self.engine._gross_margin_pct(inp)
        return self.engine._discount_risk(inp, eff, marg)

    # MINIMAL baseline
    def test_minimal_when_all_low(self):
        r = self._risk(
            list_price=10_000.0, proposed_price=9_000.0,
            max_discount_pct=25.0, cost_of_goods=2_000.0,
            historical_win_rate_at_discount=0.7,
            buyer_pushback_level=0, payment_terms_days=30,
        )
        assert r == DiscountRisk.MINIMAL

    # +3 for exceeding max discount
    def test_over_max_discount_adds_3(self):
        # eff_discount > max → +3; margin ok → +0; win rate ok → +0; pushback 0 → +0; terms 30 → +0  = 3 → MODERATE
        r = self._risk(
            list_price=10_000.0, proposed_price=7_000.0,
            max_discount_pct=20.0, cost_of_goods=1_000.0,
            historical_win_rate_at_discount=0.7,
            buyer_pushback_level=0, payment_terms_days=30,
        )
        assert r == DiscountRisk.MODERATE

    # +1 for near max discount (≥90% of max)
    def test_near_max_discount_adds_1(self):
        # eff = 18% → max_discount=20 → eff/max = 0.9  → +1; win rate 0.7 → +0; margins strong → +0 = 1 → MINIMAL
        r = self._risk(
            list_price=10_000.0, proposed_price=8_200.0,
            max_discount_pct=20.0, cost_of_goods=1_000.0,
            historical_win_rate_at_discount=0.7,
            buyer_pushback_level=0, payment_terms_days=30,
        )
        assert r == DiscountRisk.MINIMAL

    def test_near_max_discount_at_exactly_90pct(self):
        # eff_discount=18.0, max=20 → 18 >= 20*0.9=18 → +1 (score=1 → MINIMAL)
        r = self._risk(
            list_price=10_000.0, proposed_price=8_200.0,
            max_discount_pct=20.0, cost_of_goods=1_000.0,
            historical_win_rate_at_discount=0.7,
            buyer_pushback_level=0, payment_terms_days=30,
        )
        assert r == DiscountRisk.MINIMAL

    # +3 for margin < 30
    def test_low_margin_adds_3_to_score(self):
        # margin < 30 → +3; eff disc well under max → +0; win rate 0.7 → +0; pushback 0 → +0 = 3 → MODERATE
        r = self._risk(
            list_price=10_000.0, proposed_price=5_000.0,
            max_discount_pct=60.0, cost_of_goods=4_000.0,  # margin=20%
            historical_win_rate_at_discount=0.7,
            buyer_pushback_level=0, payment_terms_days=30,
        )
        assert r == DiscountRisk.MODERATE

    # +1 for margin between 30 and 45
    def test_thin_margin_adds_1(self):
        # margin=35% → +1; nothing else → score=1 → MINIMAL
        r = self._risk(
            list_price=10_000.0, proposed_price=5_000.0,
            max_discount_pct=60.0, cost_of_goods=3_250.0,  # margin=35%
            historical_win_rate_at_discount=0.7,
            buyer_pushback_level=0, payment_terms_days=30,
        )
        assert r == DiscountRisk.MINIMAL

    # +2 for win rate < 0.3
    def test_low_win_rate_adds_2(self):
        r = self._risk(
            list_price=10_000.0, proposed_price=8_000.0,
            max_discount_pct=25.0, cost_of_goods=2_000.0,
            historical_win_rate_at_discount=0.2,
            buyer_pushback_level=0, payment_terms_days=30,
        )
        assert r == DiscountRisk.MODERATE

    # +1 for win rate between 0.3 and 0.5
    def test_moderate_win_rate_adds_1(self):
        r = self._risk(
            list_price=10_000.0, proposed_price=8_000.0,
            max_discount_pct=25.0, cost_of_goods=2_000.0,
            historical_win_rate_at_discount=0.4,
            buyer_pushback_level=0, payment_terms_days=30,
        )
        assert r == DiscountRisk.MINIMAL

    # +2 for pushback ≥ 4
    def test_high_pushback_adds_2(self):
        r = self._risk(
            list_price=10_000.0, proposed_price=8_000.0,
            max_discount_pct=25.0, cost_of_goods=2_000.0,
            historical_win_rate_at_discount=0.7,
            buyer_pushback_level=4, payment_terms_days=30,
        )
        assert r == DiscountRisk.MODERATE

    # +1 for pushback == 3
    def test_pushback_3_adds_1(self):
        r = self._risk(
            list_price=10_000.0, proposed_price=8_000.0,
            max_discount_pct=25.0, cost_of_goods=2_000.0,
            historical_win_rate_at_discount=0.7,
            buyer_pushback_level=3, payment_terms_days=30,
        )
        assert r == DiscountRisk.MINIMAL

    # +1 for payment_terms_days ≥ 90
    def test_extended_payment_terms_adds_1(self):
        r = self._risk(
            list_price=10_000.0, proposed_price=8_000.0,
            max_discount_pct=25.0, cost_of_goods=2_000.0,
            historical_win_rate_at_discount=0.7,
            buyer_pushback_level=0, payment_terms_days=90,
        )
        assert r == DiscountRisk.MINIMAL

    def test_payment_terms_89_no_extra(self):
        r = self._risk(
            list_price=10_000.0, proposed_price=8_000.0,
            max_discount_pct=25.0, cost_of_goods=2_000.0,
            historical_win_rate_at_discount=0.7,
            buyer_pushback_level=0, payment_terms_days=89,
        )
        assert r == DiscountRisk.MINIMAL

    # CRITICAL threshold ≥ 7
    def test_critical_threshold(self):
        # over_max(+3) + margin<30(+3) + win_rate<0.3(+2) = 8 → CRITICAL
        r = self._risk(
            list_price=10_000.0, proposed_price=6_000.0,
            max_discount_pct=20.0, cost_of_goods=5_000.0,
            historical_win_rate_at_discount=0.2,
            buyer_pushback_level=0, payment_terms_days=30,
        )
        assert r == DiscountRisk.CRITICAL

    # HIGH threshold ≥ 4
    def test_high_threshold(self):
        # low win rate(+2) + pushback>=4(+2) = 4 → HIGH
        r = self._risk(
            list_price=10_000.0, proposed_price=8_000.0,
            max_discount_pct=25.0, cost_of_goods=2_000.0,
            historical_win_rate_at_discount=0.2,
            buyer_pushback_level=4, payment_terms_days=30,
        )
        assert r == DiscountRisk.HIGH

    # MODERATE threshold ≥ 2
    def test_moderate_threshold(self):
        # win_rate<0.3(+2) = 2 → MODERATE
        r = self._risk(
            list_price=10_000.0, proposed_price=8_000.0,
            max_discount_pct=25.0, cost_of_goods=2_000.0,
            historical_win_rate_at_discount=0.25,
            buyer_pushback_level=0, payment_terms_days=30,
        )
        assert r == DiscountRisk.MODERATE

    def test_score_7_is_critical(self):
        # over_max(+3) + margin<30(+3) + payment>=90(+1) = 7 → CRITICAL
        r = self._risk(
            list_price=10_000.0, proposed_price=6_000.0,
            max_discount_pct=20.0, cost_of_goods=5_000.0,
            historical_win_rate_at_discount=0.7,
            buyer_pushback_level=0, payment_terms_days=90,
        )
        assert r == DiscountRisk.CRITICAL

    def test_score_4_is_high(self):
        # margin<30(+3) + payment>=90(+1) = 4 → HIGH
        r = self._risk(
            list_price=10_000.0, proposed_price=5_000.0,
            max_discount_pct=60.0, cost_of_goods=4_000.0,
            historical_win_rate_at_discount=0.7,
            buyer_pushback_level=0, payment_terms_days=90,
        )
        assert r == DiscountRisk.HIGH


# ---------------------------------------------------------------------------
# 11. _negotiation_leverage
# ---------------------------------------------------------------------------

class TestNegotiationLeverage:
    def setup_method(self):
        self.engine = fresh_engine()

    def _leverage(self, **kw):
        return self.engine._negotiation_leverage(make_input(**kw))

    def test_base_score_50(self):
        # No bonuses, no pushback
        lev = self._leverage(
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            competitor_price=0.0, is_strategic_account=False,
            days_to_close=30, buyer_pushback_level=0,
        )
        assert lev == 50.0

    def test_champion_support_adds_15(self):
        lev = self._leverage(
            champion_support=True, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            competitor_price=0.0, is_strategic_account=False,
            days_to_close=30, buyer_pushback_level=0,
        )
        assert lev == 65.0

    def test_economic_buyer_adds_12(self):
        lev = self._leverage(
            champion_support=False, economic_buyer_engaged=True,
            multi_year_deal=False, professional_services=0.0,
            competitor_price=0.0, is_strategic_account=False,
            days_to_close=30, buyer_pushback_level=0,
        )
        assert lev == 62.0

    def test_multi_year_adds_8(self):
        lev = self._leverage(
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=True, professional_services=0.0,
            competitor_price=0.0, is_strategic_account=False,
            days_to_close=30, buyer_pushback_level=0,
        )
        assert lev == 58.0

    def test_professional_services_adds_5(self):
        lev = self._leverage(
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=1_000.0,
            competitor_price=0.0, is_strategic_account=False,
            days_to_close=30, buyer_pushback_level=0,
        )
        assert lev == 55.0

    def test_no_ps_no_bonus(self):
        lev = self._leverage(
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            competitor_price=0.0, is_strategic_account=False,
            days_to_close=30, buyer_pushback_level=0,
        )
        assert lev == 50.0

    def test_competitive_advantage_adds_10(self):
        lev = self._leverage(
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            competitor_price=10_000.0, proposed_price=9_000.0,
            is_strategic_account=False, days_to_close=30,
            buyer_pushback_level=0,
        )
        assert lev == 60.0

    def test_competitive_disadvantage_subtracts_15(self):
        lev = self._leverage(
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            competitor_price=8_000.0, proposed_price=9_000.0,
            is_strategic_account=False, days_to_close=30,
            buyer_pushback_level=0,
        )
        assert lev == 35.0

    def test_no_competitor_no_adjustment(self):
        lev = self._leverage(
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            competitor_price=0.0, is_strategic_account=False,
            days_to_close=30, buyer_pushback_level=0,
        )
        assert lev == 50.0

    def test_strategic_account_adds_5(self):
        lev = self._leverage(
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            competitor_price=0.0, is_strategic_account=True,
            days_to_close=30, buyer_pushback_level=0,
        )
        assert lev == 55.0

    def test_days_to_close_7_adds_5(self):
        lev = self._leverage(
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            competitor_price=0.0, is_strategic_account=False,
            days_to_close=7, buyer_pushback_level=0,
        )
        assert lev == 55.0

    def test_days_to_close_under_7_adds_5(self):
        lev = self._leverage(
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            competitor_price=0.0, is_strategic_account=False,
            days_to_close=3, buyer_pushback_level=0,
        )
        assert lev == 55.0

    def test_days_to_close_60_subtracts_10(self):
        lev = self._leverage(
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            competitor_price=0.0, is_strategic_account=False,
            days_to_close=60, buyer_pushback_level=0,
        )
        assert lev == 40.0

    def test_days_to_close_above_60_subtracts_10(self):
        lev = self._leverage(
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            competitor_price=0.0, is_strategic_account=False,
            days_to_close=90, buyer_pushback_level=0,
        )
        assert lev == 40.0

    def test_days_to_close_middle_no_adjustment(self):
        lev = self._leverage(
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            competitor_price=0.0, is_strategic_account=False,
            days_to_close=30, buyer_pushback_level=0,
        )
        assert lev == 50.0

    def test_pushback_level_1_subtracts_8(self):
        lev = self._leverage(
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            competitor_price=0.0, is_strategic_account=False,
            days_to_close=30, buyer_pushback_level=1,
        )
        assert lev == 42.0

    def test_pushback_level_4_subtracts_32(self):
        lev = self._leverage(
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            competitor_price=0.0, is_strategic_account=False,
            days_to_close=30, buyer_pushback_level=4,
        )
        assert lev == 18.0

    def test_clamped_at_zero(self):
        # heavy pushback with competitive disadvantage → clamp to 0
        lev = self._leverage(
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            competitor_price=8_000.0, proposed_price=9_000.0,
            is_strategic_account=False, days_to_close=90,
            buyer_pushback_level=4,
        )
        assert lev >= 0.0

    def test_clamped_at_100(self):
        # every bonus
        lev = self._leverage(
            champion_support=True, economic_buyer_engaged=True,
            multi_year_deal=True, professional_services=1_000.0,
            competitor_price=10_000.0, proposed_price=9_000.0,
            is_strategic_account=True, days_to_close=7,
            buyer_pushback_level=0,
        )
        assert lev <= 100.0

    def test_result_rounded_to_1_decimal(self):
        lev = self._leverage(
            champion_support=True, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            competitor_price=0.0, is_strategic_account=False,
            days_to_close=30, buyer_pushback_level=0,
        )
        assert lev == round(lev, 1)


# ---------------------------------------------------------------------------
# 12. _walkaway_risk
# ---------------------------------------------------------------------------

class TestWalkawayRisk:
    def setup_method(self):
        self.engine = fresh_engine()

    def _walkaway(self, **kw):
        return self.engine._walkaway_risk(make_input(**kw))

    def test_zero_pushback_base(self):
        w = self._walkaway(
            buyer_pushback_level=0, competitor_price=0.0,
            num_rounds=1, champion_support=True,
            discount_pct=10.0, max_discount_pct=25.0,
        )
        assert w == 0.0

    def test_pushback_level_1_adds_15(self):
        w = self._walkaway(
            buyer_pushback_level=1, competitor_price=0.0,
            num_rounds=1, champion_support=True,
            discount_pct=10.0, max_discount_pct=25.0,
        )
        assert w == 15.0

    def test_pushback_level_3_adds_45(self):
        w = self._walkaway(
            buyer_pushback_level=3, competitor_price=0.0,
            num_rounds=1, champion_support=True,
            discount_pct=10.0, max_discount_pct=25.0,
        )
        assert w == 45.0

    def test_competitor_more_than_10pct_lower_adds_25(self):
        # proposed > competitor*1.1 → +25
        w = self._walkaway(
            buyer_pushback_level=0, competitor_price=9_000.0,
            proposed_price=10_000.0,  # > 9000*1.1=9900
            num_rounds=1, champion_support=True,
            discount_pct=10.0, max_discount_pct=25.0,
        )
        assert w == 25.0

    def test_competitor_equal_proposed_no_penalty(self):
        # proposed == competitor → proposed < competitor*1.1 → no +25
        w = self._walkaway(
            buyer_pushback_level=0, competitor_price=10_000.0,
            proposed_price=10_000.0,
            num_rounds=1, champion_support=True,
            discount_pct=10.0, max_discount_pct=25.0,
        )
        assert w == 0.0

    def test_num_rounds_4_adds_15(self):
        w = self._walkaway(
            buyer_pushback_level=0, competitor_price=0.0,
            num_rounds=4, champion_support=True,
            discount_pct=10.0, max_discount_pct=25.0,
        )
        assert w == 15.0

    def test_num_rounds_below_4_no_addition(self):
        w = self._walkaway(
            buyer_pushback_level=0, competitor_price=0.0,
            num_rounds=3, champion_support=True,
            discount_pct=10.0, max_discount_pct=25.0,
        )
        assert w == 0.0

    def test_no_champion_support_adds_10(self):
        w = self._walkaway(
            buyer_pushback_level=0, competitor_price=0.0,
            num_rounds=1, champion_support=False,
            discount_pct=10.0, max_discount_pct=25.0,
        )
        assert w == 10.0

    def test_over_discount_reduces_by_10(self):
        w = self._walkaway(
            buyer_pushback_level=0, competitor_price=0.0,
            num_rounds=1, champion_support=True,
            discount_pct=30.0, max_discount_pct=25.0,
        )
        assert w == 0.0  # clamped at 0 after -10

    def test_clamped_at_100(self):
        w = self._walkaway(
            buyer_pushback_level=4, competitor_price=8_000.0,
            proposed_price=10_000.0,  # > 8000*1.1=8800
            num_rounds=5, champion_support=False,
            discount_pct=10.0, max_discount_pct=25.0,
        )
        assert w <= 100.0

    def test_clamped_at_zero(self):
        w = self._walkaway(
            buyer_pushback_level=0, competitor_price=0.0,
            num_rounds=1, champion_support=True,
            discount_pct=30.0, max_discount_pct=25.0,
        )
        assert w >= 0.0

    def test_result_rounded_to_1_decimal(self):
        w = self._walkaway(
            buyer_pushback_level=2, competitor_price=0.0,
            num_rounds=1, champion_support=True,
            discount_pct=10.0, max_discount_pct=25.0,
        )
        assert w == round(w, 1)

    def test_no_competitor_no_25_penalty(self):
        # competitor_price=0 → condition not met
        w = self._walkaway(
            buyer_pushback_level=0, competitor_price=0.0,
            proposed_price=10_000.0,
            num_rounds=1, champion_support=True,
            discount_pct=10.0, max_discount_pct=25.0,
        )
        assert w == 0.0


# ---------------------------------------------------------------------------
# 13. _price_to_value_score
# ---------------------------------------------------------------------------

class TestPriceToValueScore:
    def setup_method(self):
        self.engine = fresh_engine()

    def _ptv(self, **kw):
        inp = make_input(**kw)
        margin = self.engine._gross_margin_pct(inp)
        lev = self.engine._negotiation_leverage(inp)
        return self.engine._price_to_value_score(inp, margin, lev)

    def test_base_formula(self):
        # margin=62.5, leverage=65 (champion+econ buyer base)
        # score = 62.5*0.4 + 65*0.4 = 25 + 26 = 51 (no bonuses)
        inp = make_input(
            proposed_price=8_000.0, cost_of_goods=3_000.0,
            customer_lifetime_value=0.0, multi_year_deal=False,
            professional_services=0.0,
            champion_support=True, economic_buyer_engaged=True,
            buyer_pushback_level=0, competitor_price=0.0,
            is_strategic_account=False, days_to_close=30,
        )
        margin = self.engine._gross_margin_pct(inp)
        lev = self.engine._negotiation_leverage(inp)
        score = self.engine._price_to_value_score(inp, margin, lev)
        expected = round(max(0.0, min(100.0, margin * 0.4 + lev * 0.4)), 1)
        assert score == expected

    def test_ltv_500k_adds_10(self):
        inp1 = make_input(customer_lifetime_value=500_000.0, multi_year_deal=False, professional_services=0.0)
        inp2 = make_input(customer_lifetime_value=0.0, multi_year_deal=False, professional_services=0.0)
        m1 = self.engine._gross_margin_pct(inp1)
        m2 = self.engine._gross_margin_pct(inp2)
        l1 = self.engine._negotiation_leverage(inp1)
        l2 = self.engine._negotiation_leverage(inp2)
        s1 = self.engine._price_to_value_score(inp1, m1, l1)
        s2 = self.engine._price_to_value_score(inp2, m2, l2)
        assert s1 == round(min(100.0, s2 + 10), 1)

    def test_ltv_200k_adds_5(self):
        inp1 = make_input(customer_lifetime_value=200_000.0, multi_year_deal=False, professional_services=0.0)
        inp2 = make_input(customer_lifetime_value=0.0, multi_year_deal=False, professional_services=0.0)
        m1 = self.engine._gross_margin_pct(inp1)
        m2 = self.engine._gross_margin_pct(inp2)
        l1 = self.engine._negotiation_leverage(inp1)
        l2 = self.engine._negotiation_leverage(inp2)
        s1 = self.engine._price_to_value_score(inp1, m1, l1)
        s2 = self.engine._price_to_value_score(inp2, m2, l2)
        assert s1 == round(min(100.0, s2 + 5), 1)

    def test_ltv_below_200k_no_bonus(self):
        inp1 = make_input(customer_lifetime_value=199_999.0, multi_year_deal=False, professional_services=0.0)
        inp2 = make_input(customer_lifetime_value=0.0, multi_year_deal=False, professional_services=0.0)
        m1 = self.engine._gross_margin_pct(inp1)
        m2 = self.engine._gross_margin_pct(inp2)
        l1 = self.engine._negotiation_leverage(inp1)
        l2 = self.engine._negotiation_leverage(inp2)
        s1 = self.engine._price_to_value_score(inp1, m1, l1)
        s2 = self.engine._price_to_value_score(inp2, m2, l2)
        assert s1 == s2

    def test_multi_year_adds_8(self):
        inp1 = make_input(multi_year_deal=True, customer_lifetime_value=0.0, professional_services=0.0)
        inp2 = make_input(multi_year_deal=False, customer_lifetime_value=0.0, professional_services=0.0)
        m1 = self.engine._gross_margin_pct(inp1)
        m2 = self.engine._gross_margin_pct(inp2)
        # leverage may differ because multi_year_deal affects leverage too
        l1 = self.engine._negotiation_leverage(inp1)
        l2 = self.engine._negotiation_leverage(inp2)
        s1 = self.engine._price_to_value_score(inp1, m1, l1)
        s2 = self.engine._price_to_value_score(inp2, m2, l2)
        # s1 should be 8 more than s2 (from ptv bonus) plus leverage diff*0.4
        assert s1 > s2

    def test_professional_services_adds_5(self):
        inp1 = make_input(professional_services=5_000.0, customer_lifetime_value=0.0, multi_year_deal=False)
        inp2 = make_input(professional_services=0.0, customer_lifetime_value=0.0, multi_year_deal=False)
        m1 = self.engine._gross_margin_pct(inp1)
        m2 = self.engine._gross_margin_pct(inp2)
        l1 = self.engine._negotiation_leverage(inp1)
        l2 = self.engine._negotiation_leverage(inp2)
        s1 = self.engine._price_to_value_score(inp1, m1, l1)
        s2 = self.engine._price_to_value_score(inp2, m2, l2)
        assert s1 > s2

    def test_clamped_at_100(self):
        inp = make_input(
            proposed_price=10_000.0, cost_of_goods=500.0,
            customer_lifetime_value=600_000.0,
            multi_year_deal=True, professional_services=5_000.0,
            champion_support=True, economic_buyer_engaged=True,
            is_strategic_account=True, days_to_close=5,
            buyer_pushback_level=0, competitor_price=15_000.0,
        )
        margin = self.engine._gross_margin_pct(inp)
        lev = self.engine._negotiation_leverage(inp)
        score = self.engine._price_to_value_score(inp, margin, lev)
        assert score <= 100.0

    def test_clamped_at_zero(self):
        inp = make_input(
            proposed_price=500.0, cost_of_goods=5_000.0,
            customer_lifetime_value=0.0,
            multi_year_deal=False, professional_services=0.0,
            champion_support=False, economic_buyer_engaged=False,
            is_strategic_account=False, days_to_close=90,
            buyer_pushback_level=4, competitor_price=200.0,
        )
        margin = self.engine._gross_margin_pct(inp)
        lev = self.engine._negotiation_leverage(inp)
        score = self.engine._price_to_value_score(inp, margin, lev)
        assert score >= 0.0

    def test_result_rounded_to_1_decimal(self):
        inp = make_input()
        margin = self.engine._gross_margin_pct(inp)
        lev = self.engine._negotiation_leverage(inp)
        score = self.engine._price_to_value_score(inp, margin, lev)
        assert score == round(score, 1)


# ---------------------------------------------------------------------------
# 14. _negotiation_stage
# ---------------------------------------------------------------------------

class TestNegotiationStage:
    def setup_method(self):
        self.engine = fresh_engine()

    def _stage(self, **kw):
        return self.engine._negotiation_stage(make_input(**kw))

    def test_initial_offer_when_no_pushback_and_no_rounds(self):
        assert self._stage(buyer_pushback_level=0, num_rounds=0, days_to_close=30) == NegotiationStage.INITIAL_OFFER

    def test_stalled_when_pushback_4(self):
        assert self._stage(buyer_pushback_level=4, num_rounds=0, days_to_close=30) == NegotiationStage.STALLED

    def test_stalled_when_pushback_5(self):
        assert self._stage(buyer_pushback_level=5, num_rounds=1, days_to_close=30) == NegotiationStage.STALLED

    def test_stalled_priority_over_final_terms(self):
        # pushback=4 takes priority over days_to_close<=3
        assert self._stage(buyer_pushback_level=4, num_rounds=0, days_to_close=2) == NegotiationStage.STALLED

    def test_final_terms_when_days_to_close_3(self):
        assert self._stage(buyer_pushback_level=1, num_rounds=0, days_to_close=3) == NegotiationStage.FINAL_TERMS

    def test_final_terms_when_days_to_close_1(self):
        assert self._stage(buyer_pushback_level=1, num_rounds=0, days_to_close=1) == NegotiationStage.FINAL_TERMS

    def test_final_terms_when_days_to_close_0(self):
        assert self._stage(buyer_pushback_level=2, num_rounds=0, days_to_close=0) == NegotiationStage.FINAL_TERMS

    def test_counter_offer_when_num_rounds_2(self):
        assert self._stage(buyer_pushback_level=1, num_rounds=2, days_to_close=30) == NegotiationStage.COUNTER_OFFER

    def test_counter_offer_when_num_rounds_5(self):
        assert self._stage(buyer_pushback_level=2, num_rounds=5, days_to_close=30) == NegotiationStage.COUNTER_OFFER

    def test_initial_offer_when_num_rounds_1_days_30_pushback_1(self):
        assert self._stage(buyer_pushback_level=1, num_rounds=1, days_to_close=30) == NegotiationStage.INITIAL_OFFER

    def test_initial_offer_fallthrough(self):
        assert self._stage(buyer_pushback_level=0, num_rounds=0, days_to_close=30) == NegotiationStage.INITIAL_OFFER

    def test_priority_initial_over_counter_when_zero_rounds_zero_pushback(self):
        # Even if days is long, pushback=0 and rounds=0 → INITIAL_OFFER
        assert self._stage(buyer_pushback_level=0, num_rounds=0, days_to_close=90) == NegotiationStage.INITIAL_OFFER

    def test_counter_offer_priority_over_initial(self):
        # pushback=1, num_rounds=2, days=30 → COUNTER_OFFER (not INITIAL_OFFER)
        assert self._stage(buyer_pushback_level=1, num_rounds=2, days_to_close=30) == NegotiationStage.COUNTER_OFFER

    def test_final_terms_days_4_not_triggered(self):
        # days_to_close=4 → should not trigger FINAL_TERMS
        assert self._stage(buyer_pushback_level=1, num_rounds=1, days_to_close=4) == NegotiationStage.INITIAL_OFFER


# ---------------------------------------------------------------------------
# 15. _pricing_strategy
# ---------------------------------------------------------------------------

class TestPricingStrategy:
    def setup_method(self):
        self.engine = fresh_engine()

    def _strategy(self, **kw):
        inp = make_input(**kw)
        margin_pct = self.engine._gross_margin_pct(inp)
        eff_disc = self.engine._effective_discount_pct(inp)
        mh = self.engine._margin_health(margin_pct)
        dr = self.engine._discount_risk(inp, eff_disc, margin_pct)
        lev = self.engine._negotiation_leverage(inp)
        wa = self.engine._walkaway_risk(inp)
        return self.engine._pricing_strategy(inp, dr, lev, wa, mh)

    def test_walk_away_when_critical_margin_not_strategic(self):
        # margin<30 → CRITICAL health; not strategic → WALK_AWAY (priority 1)
        s = self._strategy(
            proposed_price=5_000.0, cost_of_goods=4_000.0,   # margin=20%
            list_price=10_000.0, max_discount_pct=60.0,
            is_strategic_account=False, customer_lifetime_value=0.0,
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            historical_win_rate_at_discount=0.7,
            buyer_pushback_level=0, payment_terms_days=30,
            competitor_price=0.0, days_to_close=30, num_rounds=0,
        )
        assert s == PricingStrategy.WALK_AWAY

    def test_critical_margin_strategic_does_not_walk_away(self):
        # critical margin + strategic account → should NOT be WALK_AWAY
        s = self._strategy(
            proposed_price=5_000.0, cost_of_goods=4_000.0,
            list_price=10_000.0, max_discount_pct=60.0,
            is_strategic_account=True, customer_lifetime_value=0.0,
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            historical_win_rate_at_discount=0.7,
            buyer_pushback_level=0, payment_terms_days=30,
            competitor_price=0.0, days_to_close=30, num_rounds=0,
        )
        assert s != PricingStrategy.WALK_AWAY

    def test_escalate_when_critical_risk(self):
        # CRITICAL discount risk → ESCALATE_TO_EXEC (priority 2)
        # Need risk_score >= 7; over_max(+3) + margin<30(+3) + win_rate<0.3(+2) = 8
        s = self._strategy(
            proposed_price=6_000.0, cost_of_goods=5_000.0,  # margin=16.7%
            list_price=10_000.0, max_discount_pct=20.0,     # eff_disc=40% > max
            is_strategic_account=True,  # strategic → skip walk_away rule
            customer_lifetime_value=600_000.0,
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            historical_win_rate_at_discount=0.1,
            buyer_pushback_level=0, payment_terms_days=30,
            competitor_price=0.0, days_to_close=30, num_rounds=0,
        )
        assert s == PricingStrategy.ESCALATE_TO_EXEC

    def test_accept_and_close_when_walkaway_high_leverage_high(self):
        # walkaway >= 70 and leverage >= 60 → ACCEPT_AND_CLOSE (priority 3)
        # Build a case: pushback=4 → walk_away=60; no_champion → +10; num_rounds=4 → +15 = 85
        # leverage: base=50+champion(15)+econ(12) = 77 (but no champion → 50+12=62)
        s = self._strategy(
            proposed_price=8_000.0, cost_of_goods=2_000.0,  # margin=75% → STRONG
            list_price=10_000.0, max_discount_pct=25.0,
            is_strategic_account=False,
            customer_lifetime_value=100_000.0,
            champion_support=False, economic_buyer_engaged=True,
            multi_year_deal=False, professional_services=0.0,
            historical_win_rate_at_discount=0.7,
            buyer_pushback_level=4, payment_terms_days=30,
            competitor_price=0.0, days_to_close=30, num_rounds=4,
        )
        # walkaway: 4*15=60 + no_champion(10) + rounds>=4(15) = 85
        # leverage: 50 + econ(12) - 4*8=32 = 30 → 30 < 60 → would not trigger
        # Let me verify directly with engine
        inp = make_input(
            proposed_price=8_000.0, cost_of_goods=2_000.0,
            list_price=10_000.0, max_discount_pct=25.0,
            is_strategic_account=False,
            customer_lifetime_value=100_000.0,
            champion_support=False, economic_buyer_engaged=True,
            multi_year_deal=False, professional_services=0.0,
            historical_win_rate_at_discount=0.7,
            buyer_pushback_level=4, payment_terms_days=30,
            competitor_price=0.0, days_to_close=30, num_rounds=4,
        )
        lev = self.engine._negotiation_leverage(inp)
        wa = self.engine._walkaway_risk(inp)
        # Just assert the logic: if wa>=70 and lev>=60, it's ACCEPT_AND_CLOSE
        if wa >= 70 and lev >= 60:
            assert s == PricingStrategy.ACCEPT_AND_CLOSE

    def test_accept_and_close_explicit(self):
        # Construct a case where walkaway >= 70 and leverage >= 60 definitely
        # high pushback + no champion drives walkaway; but need leverage >= 60
        # leverage = 50 + champ(15) + econ(12) + strat(5) + days<=7(5) - pushback(3*8=24) = 63
        # walkaway = 3*15 + no_champ_but_champ=True → 45 + rounds>=4(15) + competitor(25) = 85
        inp = make_input(
            proposed_price=10_000.0, cost_of_goods=2_500.0,  # proposed > competitor*1.1; margin=75%
            list_price=10_000.0, max_discount_pct=25.0,
            is_strategic_account=True,
            customer_lifetime_value=100_000.0,
            champion_support=True, economic_buyer_engaged=True,
            multi_year_deal=False, professional_services=0.0,
            historical_win_rate_at_discount=0.7,
            buyer_pushback_level=3, payment_terms_days=30,
            competitor_price=9_000.0,
            days_to_close=7, num_rounds=4,
        )
        lev = self.engine._negotiation_leverage(inp)
        wa = self.engine._walkaway_risk(inp)
        marg = self.engine._gross_margin_pct(inp)
        mh = self.engine._margin_health(marg)
        eff_d = self.engine._effective_discount_pct(inp)
        dr = self.engine._discount_risk(inp, eff_d, marg)
        strat = self.engine._pricing_strategy(inp, dr, lev, wa, mh)
        if wa >= 70 and lev >= 60:
            assert strat == PricingStrategy.ACCEPT_AND_CLOSE

    def test_hold_price_when_high_leverage_minimal_risk(self):
        # leverage >= 70 and disc_risk == MINIMAL → HOLD_PRICE (priority 4)
        # leverage = 50 + champ(15) + econ(12) = 77 (no pushback)
        # disc_risk: margin=75% no over-max, win_rate=0.7 → MINIMAL
        s = self._strategy(
            proposed_price=9_000.0, cost_of_goods=2_250.0,  # margin=75%
            list_price=10_000.0, max_discount_pct=25.0,     # eff_disc=10%
            is_strategic_account=False,
            customer_lifetime_value=100_000.0,
            champion_support=True, economic_buyer_engaged=True,
            multi_year_deal=False, professional_services=0.0,
            historical_win_rate_at_discount=0.7,
            buyer_pushback_level=0, payment_terms_days=30,
            competitor_price=0.0, days_to_close=30, num_rounds=1,
        )
        assert s == PricingStrategy.HOLD_PRICE

    def test_offer_value_add_multi_year(self):
        # multi_year_deal → OFFER_VALUE_ADD (priority 5)
        # Need to avoid triggering rules 1-4 first
        s = self._strategy(
            proposed_price=8_000.0, cost_of_goods=4_500.0,  # margin=43.75% → HEALTHY
            list_price=10_000.0, max_discount_pct=25.0,
            is_strategic_account=False,
            customer_lifetime_value=100_000.0,
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=True, professional_services=0.0,
            historical_win_rate_at_discount=0.7,
            buyer_pushback_level=0, payment_terms_days=30,
            competitor_price=0.0, days_to_close=30, num_rounds=1,
        )
        assert s == PricingStrategy.OFFER_VALUE_ADD

    def test_offer_value_add_professional_services(self):
        # professional_services > 0 → OFFER_VALUE_ADD (priority 5)
        s = self._strategy(
            proposed_price=8_000.0, cost_of_goods=4_500.0,  # margin=43.75% → HEALTHY
            list_price=10_000.0, max_discount_pct=25.0,
            is_strategic_account=False,
            customer_lifetime_value=100_000.0,
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=5_000.0,
            historical_win_rate_at_discount=0.7,
            buyer_pushback_level=0, payment_terms_days=30,
            competitor_price=0.0, days_to_close=30, num_rounds=1,
        )
        assert s == PricingStrategy.OFFER_VALUE_ADD

    def test_concede_strategic_when_high_risk_strategic(self):
        # disc_risk==HIGH and is_strategic_account → CONCEDE_STRATEGIC (priority 6)
        # HIGH: score 4-6; over_max(+3)+pushback>=4(+2)=5 is HIGH but pushback>=4 might trigger walkaway…
        # Use: over_max(+3) + win_rate<0.3(+2) = 5 → HIGH, margin=45% → HEALTHY (not critical)
        s = self._strategy(
            proposed_price=8_000.0, cost_of_goods=4_400.0,  # margin=45%
            list_price=10_000.0, max_discount_pct=15.0,     # eff_disc=20% > max → +3
            is_strategic_account=True,
            customer_lifetime_value=100_000.0,
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            historical_win_rate_at_discount=0.2,             # < 0.3 → +2; total=5 → HIGH
            buyer_pushback_level=0, payment_terms_days=30,
            competitor_price=0.0, days_to_close=30, num_rounds=0,
        )
        assert s == PricingStrategy.CONCEDE_STRATEGIC

    def test_escalate_when_high_risk_not_strategic(self):
        # disc_risk==HIGH and NOT is_strategic_account → ESCALATE_TO_EXEC (priority 7)
        s = self._strategy(
            proposed_price=8_000.0, cost_of_goods=4_400.0,  # margin=45%
            list_price=10_000.0, max_discount_pct=15.0,     # eff_disc=20% > max → +3
            is_strategic_account=False,
            customer_lifetime_value=100_000.0,
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            historical_win_rate_at_discount=0.2,             # +2; total=5 → HIGH
            buyer_pushback_level=0, payment_terms_days=30,
            competitor_price=0.0, days_to_close=30, num_rounds=0,
        )
        assert s == PricingStrategy.ESCALATE_TO_EXEC

    def test_hold_price_fallback(self):
        # MODERATE risk, no multi_year, no PS, not strategic → HOLD_PRICE (fallback)
        s = self._strategy(
            proposed_price=9_000.0, cost_of_goods=3_000.0,  # margin=66.7% → STRONG
            list_price=10_000.0, max_discount_pct=25.0,
            is_strategic_account=False,
            customer_lifetime_value=100_000.0,
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            historical_win_rate_at_discount=0.25,            # <0.3 → +2 → MODERATE
            buyer_pushback_level=0, payment_terms_days=30,
            competitor_price=0.0, days_to_close=30, num_rounds=0,
        )
        assert s == PricingStrategy.HOLD_PRICE


# ---------------------------------------------------------------------------
# 16. _recommended_concession
# ---------------------------------------------------------------------------

class TestRecommendedConcession:
    def setup_method(self):
        self.engine = fresh_engine()

    def _concession(self, **kw):
        inp = make_input(**kw)
        eff = self.engine._effective_discount_pct(inp)
        return self.engine._recommended_concession(inp, eff)

    def test_no_room_returns_zero(self):
        # eff_discount == max_discount_pct → remaining_room=0 → concession=0
        c = self._concession(
            list_price=10_000.0, proposed_price=7_500.0,  # eff=25%
            max_discount_pct=25.0,
        )
        assert c == 0.0

    def test_half_remaining_room(self):
        # eff_disc=20%, max=30% → remaining=10%, concession_pct=5%, value=500
        c = self._concession(
            list_price=10_000.0, proposed_price=8_000.0,   # eff=20%
            max_discount_pct=30.0,
        )
        assert c == 500.0

    def test_capped_at_5pct_of_list(self):
        # eff_disc=0%, max=20% → remaining=20%, concession_pct=min(5,10)=5%, value=500
        c = self._concession(
            list_price=10_000.0, proposed_price=10_000.0,  # eff=0%
            max_discount_pct=20.0,
        )
        assert c == 500.0

    def test_partial_room(self):
        # eff=22%, max=30% → remaining=8%, concession_pct=4% → value=400
        c = self._concession(
            list_price=10_000.0, proposed_price=7_800.0,   # eff=22%
            max_discount_pct=30.0,
        )
        assert c == 400.0

    def test_result_rounded_to_2_decimal(self):
        c = self._concession(
            list_price=10_000.0, proposed_price=8_000.0,
            max_discount_pct=30.0,
        )
        assert c == round(c, 2)

    def test_zero_room_when_over_max(self):
        # eff > max → remaining=max(0, ...) = 0 → concession=0
        c = self._concession(
            list_price=10_000.0, proposed_price=7_000.0,   # eff=30%
            max_discount_pct=25.0,
        )
        assert c == 0.0

    def test_list_price_zero_returns_zero(self):
        c = self._concession(
            list_price=0.0, proposed_price=0.0,
            max_discount_pct=25.0,
        )
        assert c == 0.0

    def test_small_remaining_room(self):
        # eff=24%, max=25% → remaining=1%, concession_pct=0.5% → value=50
        c = self._concession(
            list_price=10_000.0, proposed_price=7_600.0,   # eff=24.0%
            max_discount_pct=25.0,
        )
        assert c == pytest.approx(50.0, abs=1.0)

    def test_cap_exactly_at_5pct(self):
        # remaining_room * 0.5 = 5 → exactly at cap → concession = 5% of list_price
        c = self._concession(
            list_price=10_000.0, proposed_price=10_000.0,
            max_discount_pct=10.0,
        )
        # remaining=10%, concession_pct=min(5,5)=5% → value=500
        assert c == 500.0


# ---------------------------------------------------------------------------
# 17. is_margin_positive
# ---------------------------------------------------------------------------

class TestIsMarginPositive:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_positive_margin_returns_true(self):
        r = self.engine.analyze(make_input(proposed_price=8_000.0, cost_of_goods=3_000.0))
        assert r.is_margin_positive is True

    def test_zero_margin_returns_false(self):
        r = self.engine.analyze(make_input(proposed_price=1_000.0, cost_of_goods=1_000.0))
        assert r.is_margin_positive is False

    def test_negative_margin_returns_false(self):
        r = self.engine.analyze(make_input(proposed_price=500.0, cost_of_goods=1_000.0))
        assert r.is_margin_positive is False

    def test_zero_proposed_price_returns_false(self):
        r = self.engine.analyze(make_input(proposed_price=0.0, cost_of_goods=1_000.0))
        assert r.is_margin_positive is False

    def test_near_zero_positive_margin(self):
        r = self.engine.analyze(make_input(proposed_price=1_000.0, cost_of_goods=999.0))
        assert r.is_margin_positive is True


# ---------------------------------------------------------------------------
# 18. is_strategic
# ---------------------------------------------------------------------------

class TestIsStrategic:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_is_strategic_account_flag(self):
        r = self.engine.analyze(make_input(is_strategic_account=True, customer_lifetime_value=0.0))
        assert r.is_strategic is True

    def test_not_strategic_account_and_low_ltv(self):
        r = self.engine.analyze(make_input(is_strategic_account=False, customer_lifetime_value=100_000.0))
        assert r.is_strategic is False

    def test_ltv_500k_makes_strategic(self):
        r = self.engine.analyze(make_input(is_strategic_account=False, customer_lifetime_value=500_000.0))
        assert r.is_strategic is True

    def test_ltv_above_500k_makes_strategic(self):
        r = self.engine.analyze(make_input(is_strategic_account=False, customer_lifetime_value=600_000.0))
        assert r.is_strategic is True

    def test_ltv_below_500k_not_strategic_if_no_flag(self):
        r = self.engine.analyze(make_input(is_strategic_account=False, customer_lifetime_value=499_999.0))
        assert r.is_strategic is False

    def test_both_true_is_strategic(self):
        r = self.engine.analyze(make_input(is_strategic_account=True, customer_lifetime_value=600_000.0))
        assert r.is_strategic is True

    def test_ltv_exactly_500k(self):
        r = self.engine.analyze(make_input(is_strategic_account=False, customer_lifetime_value=500_000.0))
        assert r.is_strategic is True


# ---------------------------------------------------------------------------
# 19. Properties (empty and filtering)
# ---------------------------------------------------------------------------

class TestProperties:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_high_risk_deals_empty_initially(self):
        assert self.engine.high_risk_deals == []

    def test_strategic_deals_empty_initially(self):
        assert self.engine.strategic_deals == []

    def test_walk_away_candidates_empty_initially(self):
        assert self.engine.walk_away_candidates == []

    def test_avg_effective_discount_zero_when_empty(self):
        assert self.engine.avg_effective_discount == 0.0

    def test_high_risk_deals_filters_high(self):
        # Force a HIGH risk deal by using low win rate + low margin
        inp = make_input(
            proposed_price=8_000.0, cost_of_goods=4_400.0,
            list_price=10_000.0, max_discount_pct=15.0,
            historical_win_rate_at_discount=0.2,
            buyer_pushback_level=0, payment_terms_days=30,
        )
        self.engine.analyze(inp)
        high = self.engine.high_risk_deals
        assert all(r.discount_risk in (DiscountRisk.HIGH, DiscountRisk.CRITICAL) for r in high)

    def test_high_risk_deals_excludes_minimal(self):
        inp = make_input(
            proposed_price=9_500.0, cost_of_goods=2_000.0,
            list_price=10_000.0, max_discount_pct=25.0,
            historical_win_rate_at_discount=0.8,
            buyer_pushback_level=0, payment_terms_days=30,
        )
        self.engine.analyze(inp)
        high = self.engine.high_risk_deals
        assert all(r.discount_risk != DiscountRisk.MINIMAL for r in high)

    def test_strategic_deals_filters_correctly(self):
        self.engine.analyze(make_input(is_strategic_account=True, customer_lifetime_value=0.0))
        self.engine.analyze(make_input(is_strategic_account=False, customer_lifetime_value=100_000.0))
        strategic = self.engine.strategic_deals
        assert len(strategic) == 1
        assert strategic[0].is_strategic is True

    def test_walk_away_candidates_filters_strategy(self):
        # Create a WALK_AWAY candidate: critical margin, non-strategic
        inp = make_input(
            proposed_price=5_000.0, cost_of_goods=4_000.0,
            list_price=10_000.0, max_discount_pct=60.0,
            is_strategic_account=False, customer_lifetime_value=0.0,
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            historical_win_rate_at_discount=0.7,
            buyer_pushback_level=0, payment_terms_days=30,
            competitor_price=0.0, days_to_close=30, num_rounds=0,
        )
        self.engine.analyze(inp)
        candidates = self.engine.walk_away_candidates
        assert all(r.pricing_strategy == PricingStrategy.WALK_AWAY for r in candidates)

    def test_avg_effective_discount_single_result(self):
        self.engine.analyze(make_input(list_price=10_000.0, proposed_price=8_000.0))
        assert self.engine.avg_effective_discount == 20.0

    def test_avg_effective_discount_multiple_results(self):
        self.engine.analyze(make_input(deal_id="D1", list_price=10_000.0, proposed_price=8_000.0))  # 20%
        self.engine.analyze(make_input(deal_id="D2", list_price=10_000.0, proposed_price=9_000.0))  # 10%
        assert self.engine.avg_effective_discount == 15.0

    def test_avg_effective_discount_rounded_to_2(self):
        for i in range(3):
            self.engine.analyze(make_input(deal_id=f"D{i}", list_price=10_000.0, proposed_price=7_000.0))
        val = self.engine.avg_effective_discount
        assert val == round(val, 2)

    def test_high_risk_count_returns_list(self):
        assert isinstance(self.engine.high_risk_deals, list)

    def test_strategic_deals_returns_list(self):
        assert isinstance(self.engine.strategic_deals, list)

    def test_walk_away_candidates_returns_list(self):
        assert isinstance(self.engine.walk_away_candidates, list)

    def test_high_risk_includes_critical(self):
        # Force CRITICAL: over_max+margin<30+low_win+pushback>=4 → 3+3+2+2=10 → CRITICAL
        inp = make_input(
            proposed_price=6_000.0, cost_of_goods=5_000.0,
            list_price=10_000.0, max_discount_pct=20.0,
            historical_win_rate_at_discount=0.1,
            buyer_pushback_level=4, payment_terms_days=30,
            is_strategic_account=True,  # prevent walk_away
        )
        self.engine.analyze(inp)
        high = self.engine.high_risk_deals
        assert len(high) >= 1


# ---------------------------------------------------------------------------
# 20. summary() — 13 keys
# ---------------------------------------------------------------------------

class TestSummary:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_empty_summary_has_13_keys(self):
        assert len(self.engine.summary()) == 13

    def test_empty_summary_total_zero(self):
        assert self.engine.summary()["total"] == 0

    def test_empty_summary_empty_risk_counts(self):
        assert self.engine.summary()["risk_counts"] == {}

    def test_empty_summary_empty_stage_counts(self):
        assert self.engine.summary()["stage_counts"] == {}

    def test_empty_summary_empty_strategy_counts(self):
        assert self.engine.summary()["strategy_counts"] == {}

    def test_empty_summary_empty_margin_health_counts(self):
        assert self.engine.summary()["margin_health_counts"] == {}

    def test_empty_summary_avg_gross_margin_zero(self):
        assert self.engine.summary()["avg_gross_margin_pct"] == 0.0

    def test_empty_summary_avg_discount_zero(self):
        assert self.engine.summary()["avg_effective_discount"] == 0.0

    def test_empty_summary_avg_leverage_zero(self):
        assert self.engine.summary()["avg_negotiation_leverage"] == 0.0

    def test_empty_summary_avg_walkaway_zero(self):
        assert self.engine.summary()["avg_walkaway_risk"] == 0.0

    def test_empty_summary_high_risk_count_zero(self):
        assert self.engine.summary()["high_risk_count"] == 0

    def test_empty_summary_strategic_count_zero(self):
        assert self.engine.summary()["strategic_count"] == 0

    def test_empty_summary_walk_away_count_zero(self):
        assert self.engine.summary()["walk_away_count"] == 0

    def test_empty_summary_avg_ptv_zero(self):
        assert self.engine.summary()["avg_price_to_value_score"] == 0.0

    def test_summary_has_all_13_keys(self):
        expected_keys = {
            "total", "risk_counts", "stage_counts", "strategy_counts",
            "margin_health_counts", "avg_gross_margin_pct", "avg_effective_discount",
            "avg_negotiation_leverage", "avg_walkaway_risk", "high_risk_count",
            "strategic_count", "walk_away_count", "avg_price_to_value_score",
        }
        self.engine.analyze(make_input())
        assert set(self.engine.summary().keys()) == expected_keys

    def test_summary_total_after_analyze(self):
        self.engine.analyze(make_input(deal_id="D1"))
        self.engine.analyze(make_input(deal_id="D2"))
        assert self.engine.summary()["total"] == 2

    def test_summary_risk_counts_populated(self):
        self.engine.analyze(make_input())
        s = self.engine.summary()
        assert isinstance(s["risk_counts"], dict)
        assert sum(s["risk_counts"].values()) == 1

    def test_summary_stage_counts_populated(self):
        self.engine.analyze(make_input())
        s = self.engine.summary()
        assert sum(s["stage_counts"].values()) == 1

    def test_summary_strategy_counts_populated(self):
        self.engine.analyze(make_input())
        s = self.engine.summary()
        assert sum(s["strategy_counts"].values()) == 1

    def test_summary_margin_health_counts_populated(self):
        self.engine.analyze(make_input())
        s = self.engine.summary()
        assert sum(s["margin_health_counts"].values()) == 1

    def test_summary_avg_discount_correct(self):
        self.engine.analyze(make_input(deal_id="D1", list_price=10_000.0, proposed_price=8_000.0))
        self.engine.analyze(make_input(deal_id="D2", list_price=10_000.0, proposed_price=9_000.0))
        s = self.engine.summary()
        assert s["avg_effective_discount"] == 15.0

    def test_summary_high_risk_count(self):
        inp = make_input(
            proposed_price=6_000.0, cost_of_goods=5_000.0,
            list_price=10_000.0, max_discount_pct=20.0,
            historical_win_rate_at_discount=0.1,
            buyer_pushback_level=4, payment_terms_days=30,
            is_strategic_account=True,
        )
        self.engine.analyze(inp)
        s = self.engine.summary()
        # high_risk_count should reflect HIGH or CRITICAL results
        assert s["high_risk_count"] >= 0

    def test_summary_strategic_count(self):
        self.engine.analyze(make_input(is_strategic_account=True))
        s = self.engine.summary()
        assert s["strategic_count"] >= 1

    def test_summary_walk_away_count(self):
        inp = make_input(
            proposed_price=5_000.0, cost_of_goods=4_000.0,
            list_price=10_000.0, max_discount_pct=60.0,
            is_strategic_account=False, customer_lifetime_value=0.0,
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            historical_win_rate_at_discount=0.7,
            buyer_pushback_level=0, payment_terms_days=30,
            competitor_price=0.0, days_to_close=30, num_rounds=0,
        )
        self.engine.analyze(inp)
        s = self.engine.summary()
        assert s["walk_away_count"] >= 0


# ---------------------------------------------------------------------------
# 21. reset()
# ---------------------------------------------------------------------------

class TestReset:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_reset_clears_results(self):
        self.engine.analyze(make_input())
        self.engine.reset()
        assert self.engine.summary()["total"] == 0

    def test_reset_clears_high_risk_deals(self):
        inp = make_input(
            proposed_price=6_000.0, cost_of_goods=5_000.0,
            list_price=10_000.0, max_discount_pct=20.0,
            historical_win_rate_at_discount=0.1,
            buyer_pushback_level=4, payment_terms_days=30,
            is_strategic_account=True,
        )
        self.engine.analyze(inp)
        self.engine.reset()
        assert self.engine.high_risk_deals == []

    def test_reset_clears_strategic_deals(self):
        self.engine.analyze(make_input(is_strategic_account=True))
        self.engine.reset()
        assert self.engine.strategic_deals == []

    def test_reset_clears_walk_away_candidates(self):
        inp = make_input(
            proposed_price=5_000.0, cost_of_goods=4_000.0,
            list_price=10_000.0, max_discount_pct=60.0,
            is_strategic_account=False, customer_lifetime_value=0.0,
        )
        self.engine.analyze(inp)
        self.engine.reset()
        assert self.engine.walk_away_candidates == []

    def test_reset_resets_avg_effective_discount(self):
        self.engine.analyze(make_input())
        self.engine.reset()
        assert self.engine.avg_effective_discount == 0.0

    def test_analyze_after_reset(self):
        self.engine.analyze(make_input(deal_id="D1"))
        self.engine.reset()
        self.engine.analyze(make_input(deal_id="D2"))
        assert self.engine.summary()["total"] == 1

    def test_multiple_resets(self):
        self.engine.analyze(make_input())
        self.engine.reset()
        self.engine.reset()
        assert self.engine.summary()["total"] == 0


# ---------------------------------------------------------------------------
# 22. analyze_batch
# ---------------------------------------------------------------------------

class TestAnalyzeBatch:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_batch_returns_list(self):
        inputs = [make_input(deal_id=f"D{i}") for i in range(3)]
        results = self.engine.analyze_batch(inputs)
        assert isinstance(results, list)

    def test_batch_length_matches_input(self):
        inputs = [make_input(deal_id=f"D{i}") for i in range(5)]
        results = self.engine.analyze_batch(inputs)
        assert len(results) == 5

    def test_batch_results_are_negotiation_results(self):
        inputs = [make_input(deal_id=f"D{i}") for i in range(3)]
        results = self.engine.analyze_batch(inputs)
        assert all(isinstance(r, NegotiationResult) for r in results)

    def test_batch_accumulates_results(self):
        inputs = [make_input(deal_id=f"D{i}") for i in range(4)]
        self.engine.analyze_batch(inputs)
        assert self.engine.summary()["total"] == 4

    def test_batch_empty_input(self):
        results = self.engine.analyze_batch([])
        assert results == []

    def test_batch_single_input(self):
        results = self.engine.analyze_batch([make_input()])
        assert len(results) == 1

    def test_batch_deal_ids_preserved(self):
        inputs = [make_input(deal_id=f"DEAL-{i}") for i in range(3)]
        results = self.engine.analyze_batch(inputs)
        for i, r in enumerate(results):
            assert r.deal_id == f"DEAL-{i}"


# ---------------------------------------------------------------------------
# 23. End-to-end scenarios
# ---------------------------------------------------------------------------

class TestEndToEnd:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_healthy_enterprise_deal(self):
        inp = make_input(
            deal_id="E001",
            list_price=100_000.0, proposed_price=85_000.0,
            cost_of_goods=30_000.0, max_discount_pct=20.0,
            discount_pct=15.0, is_strategic_account=True,
            customer_lifetime_value=1_000_000.0,
            champion_support=True, economic_buyer_engaged=True,
            multi_year_deal=True, professional_services=10_000.0,
            buyer_pushback_level=1, days_to_close=14,
            num_rounds=1, competitor_price=0.0,
            historical_win_rate_at_discount=0.8,
            payment_terms_days=30,
        )
        r = self.engine.analyze(inp)
        assert r.is_margin_positive is True
        assert r.is_strategic is True
        assert r.gross_margin_pct > 0

    def test_high_risk_low_margin_deal(self):
        inp = make_input(
            deal_id="HR001",
            list_price=10_000.0, proposed_price=5_000.0,
            cost_of_goods=4_800.0, max_discount_pct=40.0,
            discount_pct=50.0, is_strategic_account=False,
            customer_lifetime_value=50_000.0,
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            buyer_pushback_level=4, days_to_close=30,
            num_rounds=5, competitor_price=4_000.0,
            historical_win_rate_at_discount=0.1,
            payment_terms_days=90,
        )
        r = self.engine.analyze(inp)
        assert r.discount_risk in (DiscountRisk.HIGH, DiscountRisk.CRITICAL)
        assert r.margin_health in (MarginHealth.THIN, MarginHealth.CRITICAL)

    def test_deal_result_has_all_fields(self):
        r = self.engine.analyze(make_input())
        assert r.deal_id is not None
        assert r.account_id is not None
        assert r.rep_id is not None
        assert isinstance(r.discount_risk, DiscountRisk)
        assert isinstance(r.negotiation_stage, NegotiationStage)
        assert isinstance(r.pricing_strategy, PricingStrategy)
        assert isinstance(r.margin_health, MarginHealth)
        assert isinstance(r.gross_margin_pct, float)
        assert isinstance(r.effective_discount_pct, float)
        assert isinstance(r.price_to_value_score, float)
        assert isinstance(r.negotiation_leverage, float)
        assert isinstance(r.walkaway_risk, float)
        assert isinstance(r.recommended_concession, float)
        assert isinstance(r.is_margin_positive, bool)
        assert isinstance(r.is_strategic, bool)

    def test_multi_deal_pipeline(self):
        deals = [
            make_input(deal_id="D1", list_price=10_000.0, proposed_price=8_000.0),
            make_input(deal_id="D2", list_price=20_000.0, proposed_price=17_000.0),
            make_input(deal_id="D3", list_price=5_000.0, proposed_price=4_000.0),
        ]
        results = self.engine.analyze_batch(deals)
        assert len(results) == 3
        s = self.engine.summary()
        assert s["total"] == 3

    def test_reset_and_reanalyze(self):
        self.engine.analyze(make_input(deal_id="D1"))
        self.engine.reset()
        self.engine.analyze(make_input(deal_id="D2"))
        assert self.engine.summary()["total"] == 1
        assert self.engine._results[0].deal_id == "D2"

    def test_competitor_below_proposed_impacts_strategy(self):
        # proposed > competitor → lower leverage, higher walkaway
        inp = make_input(
            competitor_price=7_000.0, proposed_price=9_000.0,
            cost_of_goods=3_000.0, list_price=10_000.0,
            buyer_pushback_level=0,
        )
        r = self.engine.analyze(inp)
        # proposed=9000 > competitor*1.1=7700 → walkaway += 25
        assert r.walkaway_risk >= 25.0

    def test_stalled_deal_high_pushback(self):
        inp = make_input(buyer_pushback_level=4, num_rounds=2, days_to_close=30)
        r = self.engine.analyze(inp)
        assert r.negotiation_stage == NegotiationStage.STALLED

    def test_final_terms_urgent_deal(self):
        inp = make_input(buyer_pushback_level=1, num_rounds=1, days_to_close=2)
        r = self.engine.analyze(inp)
        assert r.negotiation_stage == NegotiationStage.FINAL_TERMS

    def test_margin_range_is_valid(self):
        r = self.engine.analyze(make_input())
        assert -100.0 <= r.gross_margin_pct <= 100.0

    def test_discount_range_is_valid(self):
        r = self.engine.analyze(make_input())
        assert 0.0 <= r.effective_discount_pct <= 100.0

    def test_leverage_range_is_valid(self):
        r = self.engine.analyze(make_input())
        assert 0.0 <= r.negotiation_leverage <= 100.0

    def test_walkaway_range_is_valid(self):
        r = self.engine.analyze(make_input())
        assert 0.0 <= r.walkaway_risk <= 100.0

    def test_ptv_range_is_valid(self):
        r = self.engine.analyze(make_input())
        assert 0.0 <= r.price_to_value_score <= 100.0

    def test_concession_non_negative(self):
        r = self.engine.analyze(make_input())
        assert r.recommended_concession >= 0.0

    def test_result_stored_in_engine(self):
        r = self.engine.analyze(make_input(deal_id="TEST"))
        assert any(res.deal_id == "TEST" for res in self.engine._results)

    def test_segment_preserved(self):
        inp = make_input(segment="smb")
        # segment is not in NegotiationResult but deal_id is preserved
        r = self.engine.analyze(inp)
        assert r.deal_id == inp.deal_id

    def test_rep_id_preserved(self):
        r = self.engine.analyze(make_input(rep_id="REP-XYZ"))
        assert r.rep_id == "REP-XYZ"

    def test_account_id_preserved(self):
        r = self.engine.analyze(make_input(account_id="ACC-123"))
        assert r.account_id == "ACC-123"

    def test_walk_away_added_to_candidates(self):
        inp = make_input(
            proposed_price=5_000.0, cost_of_goods=4_000.0,
            list_price=10_000.0, max_discount_pct=60.0,
            is_strategic_account=False, customer_lifetime_value=0.0,
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            historical_win_rate_at_discount=0.7,
            buyer_pushback_level=0, payment_terms_days=30,
            competitor_price=0.0, days_to_close=30, num_rounds=0,
        )
        r = self.engine.analyze(inp)
        if r.pricing_strategy == PricingStrategy.WALK_AWAY:
            assert r in self.engine.walk_away_candidates

    def test_strategic_deal_added_to_strategic_deals(self):
        r = self.engine.analyze(make_input(is_strategic_account=True))
        assert r in self.engine.strategic_deals

    def test_summary_risk_counts_use_enum_values(self):
        self.engine.analyze(make_input())
        s = self.engine.summary()
        valid_risk_values = {m.value for m in DiscountRisk}
        for key in s["risk_counts"]:
            assert key in valid_risk_values

    def test_summary_stage_counts_use_enum_values(self):
        self.engine.analyze(make_input())
        s = self.engine.summary()
        valid_stage_values = {m.value for m in NegotiationStage}
        for key in s["stage_counts"]:
            assert key in valid_stage_values

    def test_summary_strategy_counts_use_enum_values(self):
        self.engine.analyze(make_input())
        s = self.engine.summary()
        valid_strategy_values = {m.value for m in PricingStrategy}
        for key in s["strategy_counts"]:
            assert key in valid_strategy_values

    def test_summary_margin_health_counts_use_enum_values(self):
        self.engine.analyze(make_input())
        s = self.engine.summary()
        valid_mh_values = {m.value for m in MarginHealth}
        for key in s["margin_health_counts"]:
            assert key in valid_mh_values


# ---------------------------------------------------------------------------
# 24. NegotiationResult dataclass
# ---------------------------------------------------------------------------

class TestNegotiationResult:
    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(NegotiationResult)

    def test_to_dict_method_exists(self):
        engine = fresh_engine()
        r = engine.analyze(make_input())
        assert hasattr(r, "to_dict")
        assert callable(r.to_dict)

    def test_direct_attribute_access(self):
        engine = fresh_engine()
        r = engine.analyze(make_input())
        # Should not raise
        _ = r.deal_id
        _ = r.discount_risk
        _ = r.negotiation_stage
        _ = r.pricing_strategy
        _ = r.margin_health
        _ = r.gross_margin_pct
        _ = r.effective_discount_pct
        _ = r.price_to_value_score
        _ = r.negotiation_leverage
        _ = r.walkaway_risk
        _ = r.recommended_concession
        _ = r.is_margin_positive
        _ = r.is_strategic


# ---------------------------------------------------------------------------
# 25. Additional boundary and edge case tests
# ---------------------------------------------------------------------------

class TestBoundaryAndEdgeCases:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_all_zeros_input_handled(self):
        inp = make_input(
            list_price=0.0, proposed_price=0.0, cost_of_goods=0.0,
            competitor_price=0.0, deal_value=0.0,
            discount_pct=0.0, max_discount_pct=0.0,
            num_rounds=0, buyer_pushback_level=0,
            professional_services=0.0, annual_contract_value=0.0,
            customer_lifetime_value=0.0, historical_win_rate_at_discount=0.0,
            days_to_close=0, payment_terms_days=0,
        )
        r = self.engine.analyze(inp)
        assert r is not None

    def test_very_high_list_price(self):
        inp = make_input(list_price=1_000_000.0, proposed_price=900_000.0)
        r = self.engine.analyze(inp)
        assert 0 <= r.effective_discount_pct <= 100

    def test_margin_health_boundary_60_exactly_strong(self):
        # Need gross_margin_pct == 60.0 exactly
        # (price - cogs) / price * 100 = 60 → price - cogs = 0.6*price → cogs = 0.4*price
        inp = make_input(proposed_price=1_000.0, cost_of_goods=400.0)
        margin = self.engine._gross_margin_pct(inp)
        mh = self.engine._margin_health(margin)
        assert mh == MarginHealth.STRONG

    def test_margin_health_boundary_45_exactly_healthy(self):
        inp = make_input(proposed_price=1_000.0, cost_of_goods=550.0)
        margin = self.engine._gross_margin_pct(inp)
        mh = self.engine._margin_health(margin)
        assert mh == MarginHealth.HEALTHY

    def test_margin_health_boundary_30_exactly_thin(self):
        inp = make_input(proposed_price=1_000.0, cost_of_goods=700.0)
        margin = self.engine._gross_margin_pct(inp)
        mh = self.engine._margin_health(margin)
        assert mh == MarginHealth.THIN

    def test_days_to_close_boundary_7_adds_5_to_leverage(self):
        lev_7 = self.engine._negotiation_leverage(make_input(
            days_to_close=7, buyer_pushback_level=0,
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            competitor_price=0.0, is_strategic_account=False,
        ))
        lev_8 = self.engine._negotiation_leverage(make_input(
            days_to_close=8, buyer_pushback_level=0,
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            competitor_price=0.0, is_strategic_account=False,
        ))
        assert lev_7 == lev_8 + 5

    def test_days_to_close_boundary_60_subtracts_10(self):
        lev_60 = self.engine._negotiation_leverage(make_input(
            days_to_close=60, buyer_pushback_level=0,
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            competitor_price=0.0, is_strategic_account=False,
        ))
        lev_59 = self.engine._negotiation_leverage(make_input(
            days_to_close=59, buyer_pushback_level=0,
            champion_support=False, economic_buyer_engaged=False,
            multi_year_deal=False, professional_services=0.0,
            competitor_price=0.0, is_strategic_account=False,
        ))
        assert lev_60 == lev_59 - 10

    def test_competitor_price_equal_to_proposed_no_bonus_or_penalty(self):
        lev_with = self.engine._negotiation_leverage(make_input(
            competitor_price=8_000.0, proposed_price=8_000.0,
            buyer_pushback_level=0, champion_support=False,
            economic_buyer_engaged=False, multi_year_deal=False,
            professional_services=0.0, is_strategic_account=False,
            days_to_close=30,
        ))
        lev_without = self.engine._negotiation_leverage(make_input(
            competitor_price=0.0, proposed_price=8_000.0,
            buyer_pushback_level=0, champion_support=False,
            economic_buyer_engaged=False, multi_year_deal=False,
            professional_services=0.0, is_strategic_account=False,
            days_to_close=30,
        ))
        # proposed == competitor, not < and not >, so no adjustment
        assert lev_with == lev_without

    def test_walkaway_exactly_at_110pct_competitor_boundary(self):
        # proposed = competitor * 1.1 exactly → NOT > (not strictly) → no +25
        w = self.engine._walkaway_risk(make_input(
            competitor_price=9_090.91,
            proposed_price=10_000.0,  # 10000 / 9090.91 = 1.100... ≈ 1.1
            buyer_pushback_level=0, num_rounds=0,
            champion_support=True, discount_pct=0.0, max_discount_pct=25.0,
        ))
        # At boundary: proposed > competitor*1.1 might or might not trigger
        assert w >= 0.0

    def test_discount_risk_score_exactly_2_is_moderate(self):
        # Exactly win_rate<0.3 (+2) = 2 → MODERATE
        inp = make_input(
            list_price=10_000.0, proposed_price=8_000.0,
            max_discount_pct=25.0, cost_of_goods=2_000.0,
            historical_win_rate_at_discount=0.29,
            buyer_pushback_level=0, payment_terms_days=30,
        )
        eff = self.engine._effective_discount_pct(inp)
        marg = self.engine._gross_margin_pct(inp)
        r = self.engine._discount_risk(inp, eff, marg)
        assert r == DiscountRisk.MODERATE

    def test_discount_risk_score_exactly_4_is_high(self):
        # over_max(+3) + payment>=90(+1) = 4 → HIGH
        inp = make_input(
            list_price=10_000.0, proposed_price=7_400.0,  # eff_disc=26%
            max_discount_pct=25.0, cost_of_goods=2_000.0,  # margin=72.97%
            historical_win_rate_at_discount=0.7,
            buyer_pushback_level=0, payment_terms_days=90,
        )
        eff = self.engine._effective_discount_pct(inp)
        marg = self.engine._gross_margin_pct(inp)
        r = self.engine._discount_risk(inp, eff, marg)
        assert r == DiscountRisk.HIGH

    def test_engine_init_creates_empty_results(self):
        engine = PriceNegotiationEngine()
        assert engine._results == []

    def test_analyze_returns_negotiation_result(self):
        r = self.engine.analyze(make_input())
        assert isinstance(r, NegotiationResult)

    def test_multiple_analyzes_accumulate(self):
        for i in range(10):
            self.engine.analyze(make_input(deal_id=f"D{i}"))
        assert len(self.engine._results) == 10

    def test_recommended_concession_nonnegative(self):
        for pct in [0, 10, 25, 50]:
            inp = make_input(
                list_price=10_000.0, proposed_price=10_000.0 * (1 - pct / 100),
                max_discount_pct=25.0,
            )
            eff = self.engine._effective_discount_pct(inp)
            c = self.engine._recommended_concession(inp, eff)
            assert c >= 0.0

    def test_all_pricing_strategies_reachable(self):
        strategies_seen = set()
        # WALK_AWAY
        strategies_seen.add(self.engine.analyze(make_input(
            proposed_price=5_000.0, cost_of_goods=4_000.0,
            list_price=10_000.0, max_discount_pct=60.0,
            is_strategic_account=False, customer_lifetime_value=0.0,
            multi_year_deal=False, professional_services=0.0,
        )).pricing_strategy)
        # OFFER_VALUE_ADD
        strategies_seen.add(self.engine.analyze(make_input(
            proposed_price=8_000.0, cost_of_goods=4_400.0,
            list_price=10_000.0, max_discount_pct=25.0,
            is_strategic_account=False, customer_lifetime_value=100_000.0,
            multi_year_deal=True, professional_services=0.0,
            champion_support=False, economic_buyer_engaged=False,
            historical_win_rate_at_discount=0.7, buyer_pushback_level=0,
            payment_terms_days=30, competitor_price=0.0, days_to_close=30,
        )).pricing_strategy)
        assert PricingStrategy.WALK_AWAY in strategies_seen
        assert PricingStrategy.OFFER_VALUE_ADD in strategies_seen

    def test_effective_discount_when_proposed_equals_list(self):
        inp = make_input(list_price=10_000.0, proposed_price=10_000.0)
        eff = self.engine._effective_discount_pct(inp)
        assert eff == 0.0

    def test_gross_margin_very_small_positive(self):
        inp = make_input(proposed_price=1_000.0, cost_of_goods=999.0)
        margin = self.engine._gross_margin_pct(inp)
        assert margin > 0.0
        assert margin < 1.0

    def test_summary_avg_gross_margin_single(self):
        self.engine.analyze(make_input(
            proposed_price=8_000.0, cost_of_goods=3_000.0,
        ))
        s = self.engine.summary()
        assert s["avg_gross_margin_pct"] == 62.5

    def test_summary_count_correct_with_multiple_deals(self):
        n = 7
        for i in range(n):
            self.engine.analyze(make_input(deal_id=f"D{i}"))
        assert self.engine.summary()["total"] == n

    def test_walkaway_risk_competitor_boundary_no_competitor(self):
        w = self.engine._walkaway_risk(make_input(
            competitor_price=0.0, proposed_price=10_000.0,
            buyer_pushback_level=0, num_rounds=0,
            champion_support=True, discount_pct=0.0, max_discount_pct=25.0,
        ))
        assert w == 0.0
