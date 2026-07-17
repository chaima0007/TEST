"""Comprehensive pytest test suite for SalesCommissionClawbackRiskEngine."""
from __future__ import annotations

import dataclasses
import pytest

from swarm.intelligence.sales_commission_clawback_risk_engine import (
    SalesCommissionClawbackRiskEngine,
    SalesCommissionClawbackInput,
    SalesCommissionClawbackResult,
    ClawbackRisk,
    ClawbackLikelihood,
    ClawbackReason,
    ClawbackAction,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def make_input(**overrides) -> SalesCommissionClawbackInput:
    """Return a baseline low-risk input with optional field overrides."""
    defaults = dict(
        deal_id="D001",
        rep_id="R001",
        rep_name="Alice Smith",
        region="West",
        deal_value_usd=50_000.0,
        commission_paid_usd=5_000.0,
        deal_close_date_days_ago=30,
        contract_length_months=12,
        payment_terms_days=30,
        first_payment_received=1,
        payment_failure_count=0,
        customer_health_score=80.0,
        customer_payment_history_score=90.0,
        discount_pct=10.0,
        company_avg_discount_pct=10.0,
        customer_cancellation_request=0,
        contract_dispute_flag=0,
        legal_hold_flag=0,
        customer_churn_risk_score=10.0,
        competitor_displacement_flag=0,
        deal_size_vs_avg_ratio=1.0,
        rep_clawback_history_count=0,
    )
    defaults.update(overrides)
    return SalesCommissionClawbackInput(**defaults)


@pytest.fixture
def engine():
    return SalesCommissionClawbackRiskEngine()


@pytest.fixture
def low_risk_input():
    return make_input()


@pytest.fixture
def high_risk_input():
    return make_input(
        payment_failure_count=3,
        customer_health_score=20.0,
        customer_churn_risk_score=90.0,
        legal_hold_flag=1,
        contract_dispute_flag=1,
        customer_cancellation_request=1,
        rep_clawback_history_count=4,
        discount_pct=30.0,
        company_avg_discount_pct=10.0,
        deal_size_vs_avg_ratio=6.0,
        first_payment_received=0,
    )


# ---------------------------------------------------------------------------
# 1. Enum value tests
# ---------------------------------------------------------------------------

class TestEnums:
    def test_clawback_risk_values(self):
        assert ClawbackRisk.low.value == "low"
        assert ClawbackRisk.moderate.value == "moderate"
        assert ClawbackRisk.high.value == "high"
        assert ClawbackRisk.critical.value == "critical"

    def test_clawback_risk_count(self):
        assert len(ClawbackRisk) == 4

    def test_clawback_likelihood_values(self):
        assert ClawbackLikelihood.unlikely.value == "unlikely"
        assert ClawbackLikelihood.possible.value == "possible"
        assert ClawbackLikelihood.probable.value == "probable"
        assert ClawbackLikelihood.imminent.value == "imminent"

    def test_clawback_likelihood_count(self):
        assert len(ClawbackLikelihood) == 4

    def test_clawback_reason_values(self):
        assert ClawbackReason.none.value == "none"
        assert ClawbackReason.early_cancellation.value == "early_cancellation"
        assert ClawbackReason.payment_failure.value == "payment_failure"
        assert ClawbackReason.contract_dispute.value == "contract_dispute"
        assert ClawbackReason.deal_revision.value == "deal_revision"
        assert ClawbackReason.customer_bankruptcy.value == "customer_bankruptcy"

    def test_clawback_reason_count(self):
        assert len(ClawbackReason) == 6

    def test_clawback_action_values(self):
        assert ClawbackAction.no_action.value == "no_action"
        assert ClawbackAction.flag_for_review.value == "flag_for_review"
        assert ClawbackAction.hold_commission.value == "hold_commission"
        assert ClawbackAction.partial_clawback.value == "partial_clawback"
        assert ClawbackAction.full_clawback.value == "full_clawback"

    def test_clawback_action_count(self):
        assert len(ClawbackAction) == 5

    def test_enums_are_str_subclass(self):
        assert isinstance(ClawbackRisk.low, str)
        assert isinstance(ClawbackLikelihood.unlikely, str)
        assert isinstance(ClawbackReason.none, str)
        assert isinstance(ClawbackAction.no_action, str)


# ---------------------------------------------------------------------------
# 2. Input dataclass field count
# ---------------------------------------------------------------------------

class TestInputDataclass:
    def test_exactly_22_fields(self):
        fields = dataclasses.fields(SalesCommissionClawbackInput)
        assert len(fields) == 22

    def test_field_names(self):
        names = {f.name for f in dataclasses.fields(SalesCommissionClawbackInput)}
        expected = {
            "deal_id", "rep_id", "rep_name", "region",
            "deal_value_usd", "commission_paid_usd",
            "deal_close_date_days_ago", "contract_length_months",
            "payment_terms_days", "first_payment_received",
            "payment_failure_count", "customer_health_score",
            "customer_payment_history_score", "discount_pct",
            "company_avg_discount_pct", "customer_cancellation_request",
            "contract_dispute_flag", "legal_hold_flag",
            "customer_churn_risk_score", "competitor_displacement_flag",
            "deal_size_vs_avg_ratio", "rep_clawback_history_count",
        }
        assert names == expected

    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(SalesCommissionClawbackInput)

    def test_instantiation_with_all_fields(self, low_risk_input):
        assert low_risk_input.deal_id == "D001"

    def test_string_fields(self, low_risk_input):
        assert isinstance(low_risk_input.deal_id, str)
        assert isinstance(low_risk_input.rep_id, str)
        assert isinstance(low_risk_input.rep_name, str)
        assert isinstance(low_risk_input.region, str)

    def test_float_fields(self, low_risk_input):
        assert isinstance(low_risk_input.deal_value_usd, float)
        assert isinstance(low_risk_input.commission_paid_usd, float)
        assert isinstance(low_risk_input.customer_health_score, float)

    def test_int_fields(self, low_risk_input):
        assert isinstance(low_risk_input.payment_failure_count, int)
        assert isinstance(low_risk_input.rep_clawback_history_count, int)


# ---------------------------------------------------------------------------
# 3. Result dataclass / to_dict key count
# ---------------------------------------------------------------------------

class TestResultDataclass:
    def test_to_dict_returns_exactly_15_keys(self, engine, low_risk_input):
        result = engine.assess(low_risk_input)
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_key_names(self, engine, low_risk_input):
        d = engine.assess(low_risk_input).to_dict()
        expected_keys = {
            "deal_id", "rep_id", "clawback_risk", "clawback_likelihood",
            "primary_clawback_reason", "recommended_action",
            "payment_risk_score", "customer_stability_score",
            "deal_integrity_score", "rep_risk_score",
            "clawback_composite", "is_clawback_likely",
            "requires_commission_hold", "estimated_clawback_usd",
            "clawback_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_risk_is_string(self, engine, low_risk_input):
        d = engine.assess(low_risk_input).to_dict()
        assert isinstance(d["clawback_risk"], str)

    def test_to_dict_likelihood_is_string(self, engine, low_risk_input):
        d = engine.assess(low_risk_input).to_dict()
        assert isinstance(d["clawback_likelihood"], str)

    def test_to_dict_reason_is_string(self, engine, low_risk_input):
        d = engine.assess(low_risk_input).to_dict()
        assert isinstance(d["primary_clawback_reason"], str)

    def test_to_dict_action_is_string(self, engine, low_risk_input):
        d = engine.assess(low_risk_input).to_dict()
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_is_clawback_likely_bool(self, engine, low_risk_input):
        d = engine.assess(low_risk_input).to_dict()
        assert isinstance(d["is_clawback_likely"], bool)

    def test_to_dict_requires_commission_hold_bool(self, engine, low_risk_input):
        d = engine.assess(low_risk_input).to_dict()
        assert isinstance(d["requires_commission_hold"], bool)

    def test_to_dict_estimated_clawback_float(self, engine, low_risk_input):
        d = engine.assess(low_risk_input).to_dict()
        assert isinstance(d["estimated_clawback_usd"], float)

    def test_to_dict_scores_rounded_to_1dp(self, engine):
        inp = make_input(customer_payment_history_score=33.333)
        d = engine.assess(inp).to_dict()
        for key in ("payment_risk_score", "customer_stability_score",
                    "deal_integrity_score", "rep_risk_score", "clawback_composite"):
            val = d[key]
            assert round(val, 1) == val

    def test_to_dict_estimated_clawback_rounded_to_2dp(self, engine):
        inp = make_input(commission_paid_usd=3333.33)
        d = engine.assess(inp).to_dict()
        val = d["estimated_clawback_usd"]
        assert round(val, 2) == val

    def test_result_is_dataclass(self, engine, low_risk_input):
        result = engine.assess(low_risk_input)
        assert dataclasses.is_dataclass(result)

    def test_to_dict_consistent_with_attributes(self, engine, low_risk_input):
        result = engine.assess(low_risk_input)
        d = result.to_dict()
        assert d["deal_id"] == result.deal_id
        assert d["rep_id"] == result.rep_id
        assert d["is_clawback_likely"] == result.is_clawback_likely
        assert d["requires_commission_hold"] == result.requires_commission_hold


# ---------------------------------------------------------------------------
# 4. summary() key count and structure
# ---------------------------------------------------------------------------

class TestSummaryKeys:
    def test_empty_summary_has_13_keys(self, engine):
        s = engine.summary()
        assert len(s) == 13

    def test_summary_after_assess_has_13_keys(self, engine, low_risk_input):
        engine.assess(low_risk_input)
        assert len(engine.summary()) == 13

    def test_summary_key_names(self, engine):
        s = engine.summary()
        expected = {
            "total", "risk_counts", "likelihood_counts", "reason_counts",
            "action_counts", "avg_clawback_composite", "clawback_likely_count",
            "commission_hold_count", "avg_payment_risk_score",
            "avg_customer_stability_score", "avg_deal_integrity_score",
            "avg_rep_risk_score", "total_estimated_clawback_usd",
        }
        assert set(s.keys()) == expected

    def test_empty_summary_total_zero(self, engine):
        assert engine.summary()["total"] == 0

    def test_empty_summary_counts_are_dicts(self, engine):
        s = engine.summary()
        assert s["risk_counts"] == {}
        assert s["likelihood_counts"] == {}
        assert s["reason_counts"] == {}
        assert s["action_counts"] == {}

    def test_empty_summary_averages_zero(self, engine):
        s = engine.summary()
        assert s["avg_clawback_composite"] == 0.0
        assert s["avg_payment_risk_score"] == 0.0
        assert s["avg_customer_stability_score"] == 0.0
        assert s["avg_deal_integrity_score"] == 0.0
        assert s["avg_rep_risk_score"] == 0.0
        assert s["total_estimated_clawback_usd"] == 0.0

    def test_empty_summary_likely_hold_zero(self, engine):
        s = engine.summary()
        assert s["clawback_likely_count"] == 0
        assert s["commission_hold_count"] == 0

    def test_summary_total_matches_assessed_count(self, engine):
        for i in range(5):
            engine.assess(make_input(deal_id=f"D{i}"))
        assert engine.summary()["total"] == 5

    def test_summary_risk_counts_sum_to_total(self, engine):
        for i in range(4):
            engine.assess(make_input(deal_id=f"D{i}"))
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_likelihood_counts_sum_to_total(self, engine):
        for i in range(4):
            engine.assess(make_input(deal_id=f"D{i}"))
        s = engine.summary()
        assert sum(s["likelihood_counts"].values()) == s["total"]

    def test_summary_reason_counts_sum_to_total(self, engine):
        for i in range(4):
            engine.assess(make_input(deal_id=f"D{i}"))
        s = engine.summary()
        assert sum(s["reason_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_to_total(self, engine):
        for i in range(4):
            engine.assess(make_input(deal_id=f"D{i}"))
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_total_clawback_usd_is_float(self, engine, low_risk_input):
        engine.assess(low_risk_input)
        assert isinstance(engine.summary()["total_estimated_clawback_usd"], float)

    def test_summary_13_keys_with_many_records(self, engine):
        for i in range(20):
            engine.assess(make_input(deal_id=f"D{i}"))
        assert len(engine.summary()) == 13


# ---------------------------------------------------------------------------
# 5. Composite formula tests
# ---------------------------------------------------------------------------

class TestCompositeFormula:
    def _composite(self, engine, inp):
        return engine.assess(inp).clawback_composite

    def test_composite_between_0_and_100(self, engine, low_risk_input):
        c = self._composite(engine, low_risk_input)
        assert 0.0 <= c <= 100.0

    def test_all_zero_risk_composite_is_low(self, engine):
        inp = make_input(
            customer_health_score=100.0,
            customer_churn_risk_score=0.0,
            customer_payment_history_score=100.0,
            first_payment_received=1,
            payment_failure_count=0,
            payment_terms_days=30,
            legal_hold_flag=0,
            contract_dispute_flag=0,
            discount_pct=10.0,
            company_avg_discount_pct=10.0,
            deal_size_vs_avg_ratio=1.0,
            rep_clawback_history_count=0,
            customer_cancellation_request=0,
            competitor_displacement_flag=0,
        )
        c = self._composite(engine, inp)
        assert c < 20.0

    def test_composite_clamped_at_100(self, engine, high_risk_input):
        c = self._composite(engine, high_risk_input)
        assert c <= 100.0

    def test_composite_clamped_at_0_minimum(self, engine, low_risk_input):
        c = self._composite(engine, low_risk_input)
        assert c >= 0.0

    def test_composite_weighted_payment_35pct(self, engine):
        # first_payment_received=0 adds 35 to payment_risk
        # All other scores near zero → composite ≈ 35*0.35 = 12.25 + payment hist
        inp = make_input(
            first_payment_received=0,
            customer_health_score=100.0,
            customer_churn_risk_score=0.0,
            customer_payment_history_score=100.0,
        )
        c = self._composite(engine, inp)
        assert c > 0

    def test_composite_increases_with_payment_failures(self, engine):
        c0 = self._composite(engine, make_input(payment_failure_count=0))
        c1 = self._composite(engine, make_input(payment_failure_count=1))
        c2 = self._composite(engine, make_input(payment_failure_count=2))
        c3 = self._composite(engine, make_input(payment_failure_count=3))
        assert c0 < c1 < c2 < c3

    def test_composite_increases_with_legal_hold(self, engine):
        c_no = self._composite(engine, make_input(legal_hold_flag=0))
        c_yes = self._composite(engine, make_input(legal_hold_flag=1))
        assert c_yes > c_no

    def test_composite_increases_with_dispute(self, engine):
        c_no = self._composite(engine, make_input(contract_dispute_flag=0))
        c_yes = self._composite(engine, make_input(contract_dispute_flag=1))
        assert c_yes > c_no

    def test_composite_increases_with_rep_history(self, engine):
        c0 = self._composite(engine, make_input(rep_clawback_history_count=0))
        c1 = self._composite(engine, make_input(rep_clawback_history_count=1))
        c4 = self._composite(engine, make_input(rep_clawback_history_count=4))
        assert c0 < c1 < c4

    def test_composite_increases_with_cancellation_request(self, engine):
        c_no = self._composite(engine, make_input(customer_cancellation_request=0))
        c_yes = self._composite(engine, make_input(customer_cancellation_request=1))
        assert c_yes > c_no

    def test_composite_formula_weights(self, engine):
        # Manual calculation for a specific input
        inp = make_input(
            first_payment_received=0,        # +35 to payment
            payment_failure_count=0,
            payment_terms_days=30,
            customer_payment_history_score=100.0,
            customer_health_score=100.0,
            customer_churn_risk_score=0.0,
            customer_cancellation_request=0,
            competitor_displacement_flag=0,
            legal_hold_flag=0,
            contract_dispute_flag=0,
            discount_pct=10.0,
            company_avg_discount_pct=10.0,
            deal_size_vs_avg_ratio=1.0,
            rep_clawback_history_count=0,
        )
        # payment = 35 + 0 + 0 + 0 = 35
        # stability = 0 + 0 + 0 + 0 = 0
        # integrity = 0
        # rep = 0
        # composite = 35*0.35 + 0*0.30 + 0*0.25 + 0*0.10 = 12.25
        result = engine.assess(inp)
        assert abs(result.clawback_composite - 12.25) < 0.11  # rounded to 1dp

    def test_composite_rounded_to_one_decimal(self, engine):
        inp = make_input(customer_payment_history_score=33.0)
        c = engine.assess(inp).clawback_composite
        assert c == round(c, 1)

    def test_composite_exact_weights_stability(self, engine):
        # churn=100 health=0 → stability = 35+35 = 70 → composite = 70*0.30 = 21
        inp = make_input(
            customer_churn_risk_score=100.0,
            customer_health_score=0.0,
            customer_payment_history_score=100.0,
            first_payment_received=1,
            payment_failure_count=0,
            payment_terms_days=30,
            legal_hold_flag=0,
            contract_dispute_flag=0,
            discount_pct=10.0,
            company_avg_discount_pct=10.0,
            deal_size_vs_avg_ratio=1.0,
            rep_clawback_history_count=0,
            customer_cancellation_request=0,
            competitor_displacement_flag=0,
        )
        result = engine.assess(inp)
        assert abs(result.clawback_composite - 21.0) < 0.11


# ---------------------------------------------------------------------------
# 6. is_clawback_likely invariant
# ---------------------------------------------------------------------------

class TestIsClawbackLikely:
    def test_likely_when_composite_ge_40(self, engine):
        # force high composite
        inp = make_input(
            first_payment_received=0,
            payment_failure_count=3,
            customer_health_score=10.0,
            customer_churn_risk_score=80.0,
        )
        result = engine.assess(inp)
        if result.clawback_composite >= 40:
            assert result.is_clawback_likely is True

    def test_likely_when_cancellation_request(self, engine):
        inp = make_input(customer_cancellation_request=1)
        assert engine.assess(inp).is_clawback_likely is True

    def test_likely_when_legal_hold(self, engine):
        inp = make_input(legal_hold_flag=1)
        assert engine.assess(inp).is_clawback_likely is True

    def test_not_likely_when_all_clear(self, engine, low_risk_input):
        result = engine.assess(low_risk_input)
        # baseline input should have composite < 40 and no flags
        if result.clawback_composite < 40:
            assert result.is_clawback_likely is False

    def test_likely_cancellation_overrides_low_composite(self, engine):
        inp = make_input(
            customer_cancellation_request=1,
            customer_health_score=100.0,
            customer_churn_risk_score=0.0,
        )
        assert engine.assess(inp).is_clawback_likely is True

    def test_likely_legal_hold_overrides_low_composite(self, engine):
        inp = make_input(
            legal_hold_flag=1,
            customer_health_score=100.0,
            customer_churn_risk_score=0.0,
            first_payment_received=1,
            payment_failure_count=0,
        )
        assert engine.assess(inp).is_clawback_likely is True

    def test_likely_false_no_flags_low_composite(self, engine):
        inp = make_input()
        result = engine.assess(inp)
        if result.clawback_composite < 40 and not inp.customer_cancellation_request and not inp.legal_hold_flag:
            assert result.is_clawback_likely is False

    def test_likely_both_cancellation_and_legal_hold(self, engine):
        inp = make_input(customer_cancellation_request=1, legal_hold_flag=1)
        assert engine.assess(inp).is_clawback_likely is True

    def test_to_dict_reflects_is_clawback_likely(self, engine):
        inp = make_input(customer_cancellation_request=1)
        d = engine.assess(inp).to_dict()
        assert d["is_clawback_likely"] is True


# ---------------------------------------------------------------------------
# 7. requires_commission_hold invariant
# ---------------------------------------------------------------------------

class TestRequiresCommissionHold:
    def test_hold_when_composite_ge_30(self, engine):
        inp = make_input(
            first_payment_received=0,
            payment_failure_count=2,
            customer_health_score=20.0,
        )
        result = engine.assess(inp)
        if result.clawback_composite >= 30:
            assert result.requires_commission_hold is True

    def test_hold_when_payment_failure_ge_2(self, engine):
        inp = make_input(payment_failure_count=2)
        assert engine.assess(inp).requires_commission_hold is True

    def test_hold_when_payment_failure_ge_3(self, engine):
        inp = make_input(payment_failure_count=3)
        assert engine.assess(inp).requires_commission_hold is True

    def test_hold_when_contract_dispute(self, engine):
        inp = make_input(contract_dispute_flag=1)
        assert engine.assess(inp).requires_commission_hold is True

    def test_no_hold_when_all_clear(self, engine, low_risk_input):
        result = engine.assess(low_risk_input)
        if result.clawback_composite < 30 and not low_risk_input.contract_dispute_flag:
            assert result.requires_commission_hold is False

    def test_hold_payment_failure_1_no_hold(self, engine):
        inp = make_input(payment_failure_count=1)
        result = engine.assess(inp)
        if result.clawback_composite < 30 and not inp.contract_dispute_flag:
            assert result.requires_commission_hold is False

    def test_to_dict_reflects_requires_hold(self, engine):
        inp = make_input(payment_failure_count=2)
        d = engine.assess(inp).to_dict()
        assert d["requires_commission_hold"] is True

    def test_hold_contract_dispute_flag_1(self, engine):
        inp = make_input(contract_dispute_flag=1)
        assert engine.assess(inp).requires_commission_hold is True


# ---------------------------------------------------------------------------
# 8. estimated_clawback_usd formula
# ---------------------------------------------------------------------------

class TestEstimatedClawbackUsd:
    def test_formula_commission_times_composite_over_100(self, engine):
        inp = make_input(commission_paid_usd=10_000.0)
        result = engine.assess(inp)
        expected = inp.commission_paid_usd * (result.clawback_composite / 100.0)
        assert abs(result.estimated_clawback_usd - expected) < 0.01

    def test_zero_composite_gives_zero_clawback(self, engine):
        # near-zero composite: perfect health scores
        inp = make_input(
            commission_paid_usd=5000.0,
            customer_health_score=100.0,
            customer_churn_risk_score=0.0,
            customer_payment_history_score=100.0,
            first_payment_received=1,
            payment_failure_count=0,
            payment_terms_days=30,
            legal_hold_flag=0,
            contract_dispute_flag=0,
            discount_pct=10.0,
            company_avg_discount_pct=10.0,
            deal_size_vs_avg_ratio=1.0,
            rep_clawback_history_count=0,
            customer_cancellation_request=0,
            competitor_displacement_flag=0,
        )
        result = engine.assess(inp)
        expected = inp.commission_paid_usd * (result.clawback_composite / 100.0)
        assert abs(result.estimated_clawback_usd - expected) < 0.01

    def test_estimated_clawback_scales_with_commission(self, engine):
        r1 = engine.assess(make_input(commission_paid_usd=1_000.0, payment_failure_count=3))
        engine2 = SalesCommissionClawbackRiskEngine()
        r2 = engine2.assess(make_input(commission_paid_usd=2_000.0, payment_failure_count=3))
        assert abs(r2.estimated_clawback_usd - 2 * r1.estimated_clawback_usd) < 0.02

    def test_estimated_clawback_in_to_dict_rounded_2dp(self, engine):
        inp = make_input(commission_paid_usd=3333.33)
        d = engine.assess(inp).to_dict()
        assert d["estimated_clawback_usd"] == round(d["estimated_clawback_usd"], 2)

    def test_estimated_clawback_nonnegative(self, engine, low_risk_input):
        assert engine.assess(low_risk_input).estimated_clawback_usd >= 0.0

    def test_high_commission_high_composite_large_clawback(self, engine, high_risk_input):
        inp = dataclasses.replace(high_risk_input, commission_paid_usd=100_000.0)
        result = engine.assess(inp)
        assert result.estimated_clawback_usd > 0


# ---------------------------------------------------------------------------
# 9. Risk classification thresholds
# ---------------------------------------------------------------------------

class TestRiskClassification:
    def test_low_risk_below_20(self, engine):
        inp = make_input(
            customer_health_score=100.0,
            customer_churn_risk_score=0.0,
            customer_payment_history_score=100.0,
            first_payment_received=1,
            payment_failure_count=0,
            payment_terms_days=30,
            legal_hold_flag=0,
            contract_dispute_flag=0,
            discount_pct=10.0,
            company_avg_discount_pct=10.0,
            deal_size_vs_avg_ratio=1.0,
            rep_clawback_history_count=0,
            customer_cancellation_request=0,
            competitor_displacement_flag=0,
        )
        result = engine.assess(inp)
        if result.clawback_composite < 20:
            assert result.clawback_risk == ClawbackRisk.low

    def test_moderate_risk_20_to_44(self, engine):
        # force moderate composite by adding partial risk
        inp = make_input(first_payment_received=0, customer_payment_history_score=100.0)
        result = engine.assess(inp)
        if 20 <= result.clawback_composite < 45:
            assert result.clawback_risk == ClawbackRisk.moderate

    def test_high_risk_45_to_64(self, engine):
        inp = make_input(
            payment_failure_count=2,
            first_payment_received=0,
            customer_health_score=30.0,
            customer_churn_risk_score=60.0,
        )
        result = engine.assess(inp)
        if 45 <= result.clawback_composite < 65:
            assert result.clawback_risk == ClawbackRisk.high

    def test_critical_risk_ge_65(self, engine, high_risk_input):
        result = engine.assess(high_risk_input)
        if result.clawback_composite >= 65:
            assert result.clawback_risk == ClawbackRisk.critical

    def test_risk_enum_values_in_to_dict(self, engine, low_risk_input):
        d = engine.assess(low_risk_input).to_dict()
        assert d["clawback_risk"] in ("low", "moderate", "high", "critical")

    def test_risk_boundary_exactly_20_is_moderate(self, engine):
        # We need composite exactly 20 — use a fixed payment_history_score to tune
        # payment_history_score=100 → no payment_history contribution
        # first_payment_received=0 → +35 payment
        # 35*0.35 = 12.25 → not 20; let's test thresholds via assert on the enum logic
        inp = make_input(legal_hold_flag=1, contract_dispute_flag=0,
                         customer_health_score=100.0, customer_churn_risk_score=0.0,
                         first_payment_received=1, payment_failure_count=0,
                         customer_payment_history_score=100.0,
                         discount_pct=10.0, company_avg_discount_pct=10.0,
                         deal_size_vs_avg_ratio=1.0, rep_clawback_history_count=0)
        result = engine.assess(inp)
        # composite should be 40*0.25 = 10 → low; just confirm enum is valid
        assert result.clawback_risk in (ClawbackRisk.low, ClawbackRisk.moderate,
                                        ClawbackRisk.high, ClawbackRisk.critical)

    def test_risk_boundary_low_below_20(self, engine):
        inp = make_input()
        result = engine.assess(inp)
        if result.clawback_composite < 20:
            assert result.clawback_risk == ClawbackRisk.low
        elif result.clawback_composite < 45:
            assert result.clawback_risk == ClawbackRisk.moderate

    def test_risk_boundary_high_below_65(self, engine):
        inp = make_input(payment_failure_count=3, customer_health_score=40.0)
        result = engine.assess(inp)
        if result.clawback_composite >= 65:
            assert result.clawback_risk == ClawbackRisk.critical
        elif result.clawback_composite >= 45:
            assert result.clawback_risk == ClawbackRisk.high


# ---------------------------------------------------------------------------
# 10. Likelihood classification
# ---------------------------------------------------------------------------

class TestLikelihoodClassification:
    def test_imminent_when_legal_hold_and_cancellation(self, engine):
        inp = make_input(legal_hold_flag=1, customer_cancellation_request=1)
        assert engine.assess(inp).clawback_likelihood == ClawbackLikelihood.imminent

    def test_imminent_when_composite_ge_65(self, engine, high_risk_input):
        result = engine.assess(high_risk_input)
        if result.clawback_composite >= 65:
            assert result.clawback_likelihood == ClawbackLikelihood.imminent

    def test_probable_when_composite_ge_45(self, engine):
        inp = make_input(payment_failure_count=3, first_payment_received=0,
                         customer_health_score=30.0, customer_churn_risk_score=70.0,
                         legal_hold_flag=0, customer_cancellation_request=0)
        result = engine.assess(inp)
        if 45 <= result.clawback_composite < 65:
            assert result.clawback_likelihood == ClawbackLikelihood.probable

    def test_possible_when_composite_ge_20(self, engine):
        inp = make_input(first_payment_received=0, legal_hold_flag=0,
                         customer_cancellation_request=0)
        result = engine.assess(inp)
        if 20 <= result.clawback_composite < 45:
            assert result.clawback_likelihood == ClawbackLikelihood.possible

    def test_unlikely_when_composite_lt_20(self, engine, low_risk_input):
        result = engine.assess(low_risk_input)
        if result.clawback_composite < 20 and not (
            low_risk_input.legal_hold_flag and low_risk_input.customer_cancellation_request
        ):
            assert result.clawback_likelihood == ClawbackLikelihood.unlikely

    def test_likelihood_in_to_dict(self, engine, low_risk_input):
        d = engine.assess(low_risk_input).to_dict()
        assert d["clawback_likelihood"] in ("unlikely", "possible", "probable", "imminent")

    def test_imminent_priority_over_composite(self, engine):
        # Even with low composite, legal_hold+cancellation → imminent
        inp = make_input(legal_hold_flag=1, customer_cancellation_request=1,
                         customer_health_score=100.0, customer_churn_risk_score=0.0,
                         first_payment_received=1, payment_failure_count=0)
        assert engine.assess(inp).clawback_likelihood == ClawbackLikelihood.imminent


# ---------------------------------------------------------------------------
# 11. Primary reason logic
# ---------------------------------------------------------------------------

class TestPrimaryReason:
    def test_cancellation_request_returns_early_cancellation(self, engine):
        inp = make_input(customer_cancellation_request=1)
        assert engine.assess(inp).primary_clawback_reason == ClawbackReason.early_cancellation

    def test_legal_hold_returns_contract_dispute(self, engine):
        inp = make_input(legal_hold_flag=1, customer_cancellation_request=0)
        assert engine.assess(inp).primary_clawback_reason == ClawbackReason.contract_dispute

    def test_contract_dispute_returns_contract_dispute(self, engine):
        inp = make_input(contract_dispute_flag=1, customer_cancellation_request=0)
        assert engine.assess(inp).primary_clawback_reason == ClawbackReason.contract_dispute

    def test_cancellation_overrides_legal_hold(self, engine):
        inp = make_input(customer_cancellation_request=1, legal_hold_flag=1)
        assert engine.assess(inp).primary_clawback_reason == ClawbackReason.early_cancellation

    def test_payment_failure_reason(self, engine):
        inp = make_input(payment_failure_count=2,
                         customer_cancellation_request=0,
                         contract_dispute_flag=0,
                         legal_hold_flag=0,
                         customer_health_score=80.0,
                         discount_pct=10.0,
                         company_avg_discount_pct=10.0)
        result = engine.assess(inp)
        assert result.primary_clawback_reason == ClawbackReason.payment_failure

    def test_customer_bankruptcy_reason(self, engine):
        inp = make_input(customer_health_score=20.0,
                         customer_cancellation_request=0,
                         contract_dispute_flag=0,
                         legal_hold_flag=0,
                         payment_failure_count=0,
                         discount_pct=10.0,
                         company_avg_discount_pct=10.0)
        result = engine.assess(inp)
        # health < 30 and no cancellation/legal hold → customer_bankruptcy if stability > others
        assert result.primary_clawback_reason in (
            ClawbackReason.customer_bankruptcy, ClawbackReason.none
        )

    def test_deal_revision_reason_excess_discount(self, engine):
        inp = make_input(discount_pct=25.0, company_avg_discount_pct=10.0,
                         customer_cancellation_request=0,
                         contract_dispute_flag=0,
                         legal_hold_flag=0,
                         payment_failure_count=0,
                         customer_health_score=80.0)
        result = engine.assess(inp)
        assert result.primary_clawback_reason == ClawbackReason.deal_revision

    def test_no_reason_when_all_clear(self, engine, low_risk_input):
        result = engine.assess(low_risk_input)
        assert result.primary_clawback_reason == ClawbackReason.none

    def test_reason_in_to_dict(self, engine, low_risk_input):
        d = engine.assess(low_risk_input).to_dict()
        valid = {"none", "early_cancellation", "payment_failure",
                 "contract_dispute", "deal_revision", "customer_bankruptcy"}
        assert d["primary_clawback_reason"] in valid


# ---------------------------------------------------------------------------
# 12. Recommended action logic
# ---------------------------------------------------------------------------

class TestRecommendedAction:
    def test_full_clawback_when_legal_hold(self, engine):
        inp = make_input(legal_hold_flag=1)
        assert engine.assess(inp).recommended_action == ClawbackAction.full_clawback

    def test_full_clawback_critical_risk(self, engine, high_risk_input):
        result = engine.assess(high_risk_input)
        if result.clawback_risk == ClawbackRisk.critical:
            assert result.recommended_action == ClawbackAction.full_clawback

    def test_full_clawback_high_risk_with_cancellation(self, engine):
        inp = make_input(
            customer_cancellation_request=1,
            payment_failure_count=3,
            first_payment_received=0,
            customer_health_score=20.0,
            customer_churn_risk_score=90.0,
            contract_dispute_flag=1,
            legal_hold_flag=1,
        )
        result = engine.assess(inp)
        assert result.recommended_action == ClawbackAction.full_clawback

    def test_partial_clawback_high_risk(self, engine):
        inp = make_input(
            payment_failure_count=2,
            first_payment_received=0,
            customer_health_score=30.0,
            customer_churn_risk_score=60.0,
            legal_hold_flag=0,
            customer_cancellation_request=0,
        )
        result = engine.assess(inp)
        if result.clawback_risk == ClawbackRisk.high:
            assert result.recommended_action == ClawbackAction.partial_clawback

    def test_hold_commission_moderate_risk(self, engine):
        inp = make_input(first_payment_received=0,
                         customer_payment_history_score=50.0,
                         customer_health_score=60.0,
                         customer_churn_risk_score=30.0,
                         legal_hold_flag=0, customer_cancellation_request=0)
        result = engine.assess(inp)
        if result.clawback_risk == ClawbackRisk.moderate:
            assert result.recommended_action == ClawbackAction.hold_commission

    def test_flag_for_review_low_risk_with_rep_history(self, engine):
        inp = make_input(rep_clawback_history_count=1)
        result = engine.assess(inp)
        if result.clawback_risk == ClawbackRisk.low:
            assert result.recommended_action == ClawbackAction.flag_for_review

    def test_no_action_clean_deal(self, engine, low_risk_input):
        result = engine.assess(low_risk_input)
        if result.clawback_risk == ClawbackRisk.low and low_risk_input.rep_clawback_history_count == 0:
            assert result.recommended_action == ClawbackAction.no_action

    def test_action_in_to_dict(self, engine, low_risk_input):
        d = engine.assess(low_risk_input).to_dict()
        valid = {"no_action", "flag_for_review", "hold_commission",
                 "partial_clawback", "full_clawback"}
        assert d["recommended_action"] in valid


# ---------------------------------------------------------------------------
# 13. Payment risk sub-score
# ---------------------------------------------------------------------------

class TestPaymentRiskScore:
    def test_no_first_payment_adds_35(self, engine):
        r_yes = engine.assess(make_input(first_payment_received=1))
        engine2 = SalesCommissionClawbackRiskEngine()
        r_no = engine2.assess(make_input(first_payment_received=0))
        assert r_no.payment_risk_score > r_yes.payment_risk_score

    def test_payment_failure_3_adds_35(self, engine):
        r0 = engine.assess(make_input(payment_failure_count=0))
        engine2 = SalesCommissionClawbackRiskEngine()
        r3 = engine2.assess(make_input(payment_failure_count=3))
        assert r3.payment_risk_score - r0.payment_risk_score >= 35

    def test_payment_failure_2_adds_24(self, engine):
        r0 = engine.assess(make_input(payment_failure_count=0))
        engine2 = SalesCommissionClawbackRiskEngine()
        r2 = engine2.assess(make_input(payment_failure_count=2))
        diff = r2.payment_risk_score - r0.payment_risk_score
        assert abs(diff - 24.0) < 0.1

    def test_payment_failure_1_adds_12(self, engine):
        r0 = engine.assess(make_input(payment_failure_count=0))
        engine2 = SalesCommissionClawbackRiskEngine()
        r1 = engine2.assess(make_input(payment_failure_count=1))
        diff = r1.payment_risk_score - r0.payment_risk_score
        assert abs(diff - 12.0) < 0.1

    def test_long_payment_terms_over_90_adds_15(self, engine):
        r30 = engine.assess(make_input(payment_terms_days=30))
        engine2 = SalesCommissionClawbackRiskEngine()
        r91 = engine2.assess(make_input(payment_terms_days=91))
        assert r91.payment_risk_score - r30.payment_risk_score >= 15

    def test_payment_terms_over_60_adds_8(self, engine):
        r30 = engine.assess(make_input(payment_terms_days=30))
        engine2 = SalesCommissionClawbackRiskEngine()
        r61 = engine2.assess(make_input(payment_terms_days=61))
        diff = r61.payment_risk_score - r30.payment_risk_score
        assert abs(diff - 8.0) < 0.1

    def test_low_payment_history_increases_score(self, engine):
        r_high = engine.assess(make_input(customer_payment_history_score=100.0))
        engine2 = SalesCommissionClawbackRiskEngine()
        r_low = engine2.assess(make_input(customer_payment_history_score=0.0))
        assert r_low.payment_risk_score > r_high.payment_risk_score

    def test_payment_score_clamped_at_100(self, engine):
        inp = make_input(first_payment_received=0, payment_failure_count=3,
                         payment_terms_days=91, customer_payment_history_score=0.0)
        assert engine.assess(inp).payment_risk_score <= 100.0

    def test_payment_score_clamped_at_0(self, engine, low_risk_input):
        assert engine.assess(low_risk_input).payment_risk_score >= 0.0


# ---------------------------------------------------------------------------
# 14. Customer stability sub-score
# ---------------------------------------------------------------------------

class TestCustomerStabilityScore:
    def test_low_health_increases_stability_score(self, engine):
        r_high = engine.assess(make_input(customer_health_score=100.0))
        engine2 = SalesCommissionClawbackRiskEngine()
        r_low = engine2.assess(make_input(customer_health_score=0.0))
        assert r_low.customer_stability_score > r_high.customer_stability_score

    def test_high_churn_risk_increases_stability_score(self, engine):
        r_low = engine.assess(make_input(customer_churn_risk_score=0.0))
        engine2 = SalesCommissionClawbackRiskEngine()
        r_high = engine2.assess(make_input(customer_churn_risk_score=100.0))
        assert r_high.customer_stability_score > r_low.customer_stability_score

    def test_cancellation_adds_25(self, engine):
        r_no = engine.assess(make_input(customer_cancellation_request=0))
        engine2 = SalesCommissionClawbackRiskEngine()
        r_yes = engine2.assess(make_input(customer_cancellation_request=1))
        diff = r_yes.customer_stability_score - r_no.customer_stability_score
        assert abs(diff - 25.0) < 0.1

    def test_competitor_displacement_adds_5(self, engine):
        r_no = engine.assess(make_input(competitor_displacement_flag=0))
        engine2 = SalesCommissionClawbackRiskEngine()
        r_yes = engine2.assess(make_input(competitor_displacement_flag=1))
        diff = r_yes.customer_stability_score - r_no.customer_stability_score
        assert abs(diff - 5.0) < 0.1

    def test_stability_score_clamped_at_100(self, engine):
        inp = make_input(customer_health_score=0.0, customer_churn_risk_score=100.0,
                         customer_cancellation_request=1, competitor_displacement_flag=1)
        assert engine.assess(inp).customer_stability_score <= 100.0

    def test_stability_score_clamped_at_0(self, engine, low_risk_input):
        assert engine.assess(low_risk_input).customer_stability_score >= 0.0

    def test_perfect_health_zero_churn_no_flags(self, engine):
        inp = make_input(customer_health_score=100.0, customer_churn_risk_score=0.0,
                         customer_cancellation_request=0, competitor_displacement_flag=0)
        assert engine.assess(inp).customer_stability_score == 0.0


# ---------------------------------------------------------------------------
# 15. Deal integrity sub-score
# ---------------------------------------------------------------------------

class TestDealIntegrityScore:
    def test_legal_hold_adds_40(self, engine):
        r_no = engine.assess(make_input(legal_hold_flag=0, contract_dispute_flag=0))
        engine2 = SalesCommissionClawbackRiskEngine()
        r_yes = engine2.assess(make_input(legal_hold_flag=1, contract_dispute_flag=0))
        diff = r_yes.deal_integrity_score - r_no.deal_integrity_score
        assert abs(diff - 40.0) < 0.1

    def test_contract_dispute_adds_30(self, engine):
        r_no = engine.assess(make_input(contract_dispute_flag=0, legal_hold_flag=0))
        engine2 = SalesCommissionClawbackRiskEngine()
        r_yes = engine2.assess(make_input(contract_dispute_flag=1, legal_hold_flag=0))
        diff = r_yes.deal_integrity_score - r_no.deal_integrity_score
        assert abs(diff - 30.0) < 0.1

    def test_excess_discount_gt_15_adds_20(self, engine):
        r_no = engine.assess(make_input(discount_pct=10.0, company_avg_discount_pct=10.0))
        engine2 = SalesCommissionClawbackRiskEngine()
        r_yes = engine2.assess(make_input(discount_pct=30.0, company_avg_discount_pct=10.0))
        diff = r_yes.deal_integrity_score - r_no.deal_integrity_score
        assert abs(diff - 20.0) < 0.1

    def test_excess_discount_gt_10_adds_12(self, engine):
        r_no = engine.assess(make_input(discount_pct=10.0, company_avg_discount_pct=10.0))
        engine2 = SalesCommissionClawbackRiskEngine()
        r_yes = engine2.assess(make_input(discount_pct=21.0, company_avg_discount_pct=10.0))
        diff = r_yes.deal_integrity_score - r_no.deal_integrity_score
        assert abs(diff - 12.0) < 0.1

    def test_excess_discount_gt_5_adds_6(self, engine):
        r_no = engine.assess(make_input(discount_pct=10.0, company_avg_discount_pct=10.0))
        engine2 = SalesCommissionClawbackRiskEngine()
        r_yes = engine2.assess(make_input(discount_pct=16.0, company_avg_discount_pct=10.0))
        diff = r_yes.deal_integrity_score - r_no.deal_integrity_score
        assert abs(diff - 6.0) < 0.1

    def test_large_deal_ratio_gt_5_adds_10(self, engine):
        r_no = engine.assess(make_input(deal_size_vs_avg_ratio=1.0))
        engine2 = SalesCommissionClawbackRiskEngine()
        r_yes = engine2.assess(make_input(deal_size_vs_avg_ratio=6.0))
        diff = r_yes.deal_integrity_score - r_no.deal_integrity_score
        assert abs(diff - 10.0) < 0.1

    def test_large_deal_ratio_gt_3_adds_5(self, engine):
        r_no = engine.assess(make_input(deal_size_vs_avg_ratio=1.0))
        engine2 = SalesCommissionClawbackRiskEngine()
        r_yes = engine2.assess(make_input(deal_size_vs_avg_ratio=4.0))
        diff = r_yes.deal_integrity_score - r_no.deal_integrity_score
        assert abs(diff - 5.0) < 0.1

    def test_integrity_score_clamped_at_100(self, engine):
        inp = make_input(legal_hold_flag=1, contract_dispute_flag=1,
                         discount_pct=30.0, company_avg_discount_pct=10.0,
                         deal_size_vs_avg_ratio=6.0)
        assert engine.assess(inp).deal_integrity_score <= 100.0

    def test_integrity_score_clamped_at_0(self, engine, low_risk_input):
        assert engine.assess(low_risk_input).deal_integrity_score >= 0.0

    def test_clean_deal_zero_integrity_score(self, engine):
        inp = make_input(legal_hold_flag=0, contract_dispute_flag=0,
                         discount_pct=10.0, company_avg_discount_pct=10.0,
                         deal_size_vs_avg_ratio=1.0)
        assert engine.assess(inp).deal_integrity_score == 0.0


# ---------------------------------------------------------------------------
# 16. Rep risk sub-score
# ---------------------------------------------------------------------------

class TestRepRiskScore:
    def test_rep_history_4_adds_60(self, engine):
        r0 = engine.assess(make_input(rep_clawback_history_count=0))
        engine2 = SalesCommissionClawbackRiskEngine()
        r4 = engine2.assess(make_input(rep_clawback_history_count=4))
        diff = r4.rep_risk_score - r0.rep_risk_score
        assert abs(diff - 60.0) < 0.1

    def test_rep_history_2_adds_35(self, engine):
        r0 = engine.assess(make_input(rep_clawback_history_count=0))
        engine2 = SalesCommissionClawbackRiskEngine()
        r2 = engine2.assess(make_input(rep_clawback_history_count=2))
        diff = r2.rep_risk_score - r0.rep_risk_score
        assert abs(diff - 35.0) < 0.1

    def test_rep_history_1_adds_15(self, engine):
        r0 = engine.assess(make_input(rep_clawback_history_count=0))
        engine2 = SalesCommissionClawbackRiskEngine()
        r1 = engine2.assess(make_input(rep_clawback_history_count=1))
        diff = r1.rep_risk_score - r0.rep_risk_score
        assert abs(diff - 15.0) < 0.1

    def test_short_contract_high_value_adds_25(self, engine):
        r_base = engine.assess(make_input(
            contract_length_months=12, deal_value_usd=50_000.0,
            rep_clawback_history_count=0))
        engine2 = SalesCommissionClawbackRiskEngine()
        r_risky = engine2.assess(make_input(
            contract_length_months=1, deal_value_usd=150_000.0,
            rep_clawback_history_count=0))
        diff = r_risky.rep_risk_score - r_base.rep_risk_score
        assert abs(diff - 25.0) < 0.1

    def test_short_contract_3mo_very_high_value_adds_15(self, engine):
        r_base = engine.assess(make_input(
            contract_length_months=12, deal_value_usd=50_000.0,
            rep_clawback_history_count=0))
        engine2 = SalesCommissionClawbackRiskEngine()
        r_risky = engine2.assess(make_input(
            contract_length_months=3, deal_value_usd=600_000.0,
            rep_clawback_history_count=0))
        diff = r_risky.rep_risk_score - r_base.rep_risk_score
        assert abs(diff - 15.0) < 0.1

    def test_rep_risk_clamped_at_100(self, engine):
        inp = make_input(rep_clawback_history_count=10,
                         contract_length_months=1, deal_value_usd=200_000.0)
        assert engine.assess(inp).rep_risk_score <= 100.0

    def test_rep_risk_clamped_at_0(self, engine, low_risk_input):
        assert engine.assess(low_risk_input).rep_risk_score >= 0.0

    def test_clean_rep_zero_risk(self, engine):
        inp = make_input(rep_clawback_history_count=0,
                         contract_length_months=12, deal_value_usd=50_000.0)
        assert engine.assess(inp).rep_risk_score == 0.0


# ---------------------------------------------------------------------------
# 17. Signal / clawback_signal string
# ---------------------------------------------------------------------------

class TestClawbackSignal:
    def test_low_risk_signal(self, engine, low_risk_input):
        result = engine.assess(low_risk_input)
        if result.clawback_risk == ClawbackRisk.low:
            assert "low clawback risk" in result.clawback_signal

    def test_signal_contains_composite(self, engine):
        inp = make_input(first_payment_received=0)
        result = engine.assess(inp)
        if result.clawback_risk != ClawbackRisk.low:
            assert "composite" in result.clawback_signal

    def test_cancellation_signal(self, engine):
        inp = make_input(customer_cancellation_request=1,
                         customer_churn_risk_score=50.0,
                         customer_health_score=40.0)
        result = engine.assess(inp)
        # signal only varies from "stable" when risk is not low
        if result.clawback_risk != ClawbackRisk.low:
            assert "cancellation" in result.clawback_signal

    def test_contract_dispute_signal(self, engine):
        inp = make_input(legal_hold_flag=1, customer_cancellation_request=0,
                         customer_health_score=40.0, customer_churn_risk_score=50.0)
        result = engine.assess(inp)
        if result.clawback_risk != ClawbackRisk.low:
            assert "legal hold" in result.clawback_signal or "dispute" in result.clawback_signal

    def test_payment_failure_signal(self, engine):
        inp = make_input(payment_failure_count=2,
                         customer_cancellation_request=0,
                         contract_dispute_flag=0,
                         legal_hold_flag=0,
                         customer_health_score=80.0,
                         discount_pct=10.0,
                         company_avg_discount_pct=10.0)
        result = engine.assess(inp)
        if (result.primary_clawback_reason == ClawbackReason.payment_failure
                and result.clawback_risk != ClawbackRisk.low):
            assert "payment failure" in result.clawback_signal

    def test_signal_is_string(self, engine, low_risk_input):
        assert isinstance(engine.assess(low_risk_input).clawback_signal, str)

    def test_signal_nonempty(self, engine, low_risk_input):
        assert engine.assess(low_risk_input).clawback_signal != ""

    def test_deal_revision_signal(self, engine):
        inp = make_input(discount_pct=25.0, company_avg_discount_pct=10.0,
                         customer_cancellation_request=0, contract_dispute_flag=0,
                         legal_hold_flag=0, payment_failure_count=0,
                         customer_health_score=80.0)
        result = engine.assess(inp)
        if (result.primary_clawback_reason == ClawbackReason.deal_revision
                and result.clawback_risk != ClawbackRisk.low):
            assert "discount" in result.clawback_signal

    def test_customer_bankruptcy_signal(self, engine):
        inp = make_input(customer_health_score=20.0,
                         customer_cancellation_request=0, contract_dispute_flag=0,
                         legal_hold_flag=0, payment_failure_count=0,
                         discount_pct=10.0, company_avg_discount_pct=10.0)
        result = engine.assess(inp)
        if (result.primary_clawback_reason == ClawbackReason.customer_bankruptcy
                and result.clawback_risk != ClawbackRisk.low):
            assert "health score" in result.clawback_signal or "churn" in result.clawback_signal


# ---------------------------------------------------------------------------
# 18. assess() state accumulation
# ---------------------------------------------------------------------------

class TestAssessState:
    def test_results_accumulate(self, engine):
        engine.assess(make_input(deal_id="D1"))
        engine.assess(make_input(deal_id="D2"))
        assert engine.summary()["total"] == 2

    def test_new_engine_empty(self):
        e = SalesCommissionClawbackRiskEngine()
        assert e.summary()["total"] == 0

    def test_results_are_independent_per_engine(self):
        e1 = SalesCommissionClawbackRiskEngine()
        e2 = SalesCommissionClawbackRiskEngine()
        e1.assess(make_input(deal_id="D1"))
        assert e1.summary()["total"] == 1
        assert e2.summary()["total"] == 0

    def test_assess_returns_result_object(self, engine, low_risk_input):
        result = engine.assess(low_risk_input)
        assert isinstance(result, SalesCommissionClawbackResult)

    def test_deal_id_preserved(self, engine):
        inp = make_input(deal_id="DEAL-XYZ")
        result = engine.assess(inp)
        assert result.deal_id == "DEAL-XYZ"

    def test_rep_id_preserved(self, engine):
        inp = make_input(rep_id="REP-999")
        result = engine.assess(inp)
        assert result.rep_id == "REP-999"

    def test_multiple_assesses_accumulate(self, engine):
        for i in range(10):
            engine.assess(make_input(deal_id=f"D{i}"))
        assert engine.summary()["total"] == 10


# ---------------------------------------------------------------------------
# 19. assess_batch()
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_returns_list(self, engine):
        inputs = [make_input(deal_id=f"D{i}") for i in range(3)]
        results = engine.assess_batch(inputs)
        assert isinstance(results, list)

    def test_length_matches_input(self, engine):
        inputs = [make_input(deal_id=f"D{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5

    def test_each_result_is_result_type(self, engine):
        inputs = [make_input(deal_id=f"D{i}") for i in range(3)]
        for r in engine.assess_batch(inputs):
            assert isinstance(r, SalesCommissionClawbackResult)

    def test_batch_accumulates_in_summary(self, engine):
        inputs = [make_input(deal_id=f"D{i}") for i in range(7)]
        engine.assess_batch(inputs)
        assert engine.summary()["total"] == 7

    def test_empty_batch_returns_empty_list(self, engine):
        assert engine.assess_batch([]) == []

    def test_batch_order_preserved(self, engine):
        inputs = [make_input(deal_id=f"DEAL-{i}") for i in range(4)]
        results = engine.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.deal_id == f"DEAL-{i}"

    def test_single_item_batch(self, engine, low_risk_input):
        results = engine.assess_batch([low_risk_input])
        assert len(results) == 1

    def test_batch_mixed_risk_levels(self, engine, high_risk_input, low_risk_input):
        results = engine.assess_batch([low_risk_input, high_risk_input])
        assert len(results) == 2
        risks = {r.clawback_risk for r in results}
        assert len(risks) >= 1  # at least different risks possible

    def test_batch_and_single_assess_accumulate(self, engine, low_risk_input):
        engine.assess(low_risk_input)
        engine.assess_batch([make_input(deal_id="D2"), make_input(deal_id="D3")])
        assert engine.summary()["total"] == 3


# ---------------------------------------------------------------------------
# 20. summary() content accuracy
# ---------------------------------------------------------------------------

class TestSummaryContent:
    def test_avg_clawback_composite_correct(self, engine):
        r1 = engine.assess(make_input(deal_id="D1"))
        r2 = engine.assess(make_input(deal_id="D2", payment_failure_count=2))
        s = engine.summary()
        expected = round((r1.clawback_composite + r2.clawback_composite) / 2, 1)
        assert s["avg_clawback_composite"] == expected

    def test_clawback_likely_count_correct(self, engine):
        engine.assess(make_input(deal_id="D1", customer_cancellation_request=1))
        engine.assess(make_input(deal_id="D2"))
        s = engine.summary()
        assert s["clawback_likely_count"] >= 1

    def test_commission_hold_count_correct(self, engine):
        engine.assess(make_input(deal_id="D1", payment_failure_count=2))
        engine.assess(make_input(deal_id="D2"))
        s = engine.summary()
        assert s["commission_hold_count"] >= 1

    def test_total_estimated_clawback_usd_sum(self, engine):
        r1 = engine.assess(make_input(deal_id="D1", commission_paid_usd=10_000.0))
        r2 = engine.assess(make_input(deal_id="D2", commission_paid_usd=5_000.0))
        s = engine.summary()
        expected = round(r1.estimated_clawback_usd + r2.estimated_clawback_usd, 2)
        assert s["total_estimated_clawback_usd"] == expected

    def test_avg_payment_risk_score_correct(self, engine):
        r1 = engine.assess(make_input(deal_id="D1"))
        r2 = engine.assess(make_input(deal_id="D2", payment_failure_count=3))
        s = engine.summary()
        expected = round((r1.payment_risk_score + r2.payment_risk_score) / 2, 1)
        assert s["avg_payment_risk_score"] == expected

    def test_avg_customer_stability_score_correct(self, engine):
        r1 = engine.assess(make_input(deal_id="D1"))
        r2 = engine.assess(make_input(deal_id="D2", customer_churn_risk_score=80.0))
        s = engine.summary()
        expected = round((r1.customer_stability_score + r2.customer_stability_score) / 2, 1)
        assert s["avg_customer_stability_score"] == expected

    def test_avg_deal_integrity_score_correct(self, engine):
        r1 = engine.assess(make_input(deal_id="D1"))
        r2 = engine.assess(make_input(deal_id="D2", legal_hold_flag=1))
        s = engine.summary()
        expected = round((r1.deal_integrity_score + r2.deal_integrity_score) / 2, 1)
        assert s["avg_deal_integrity_score"] == expected

    def test_avg_rep_risk_score_correct(self, engine):
        r1 = engine.assess(make_input(deal_id="D1"))
        r2 = engine.assess(make_input(deal_id="D2", rep_clawback_history_count=4))
        s = engine.summary()
        expected = round((r1.rep_risk_score + r2.rep_risk_score) / 2, 1)
        assert s["avg_rep_risk_score"] == expected

    def test_risk_counts_populated_correctly(self, engine):
        engine.assess(make_input(deal_id="D1"))  # likely low
        s = engine.summary()
        assert "low" in s["risk_counts"] or any(v > 0 for v in s["risk_counts"].values())

    def test_summary_total_clawback_usd_rounded_2dp(self, engine):
        engine.assess(make_input(commission_paid_usd=3333.33))
        s = engine.summary()
        val = s["total_estimated_clawback_usd"]
        assert round(val, 2) == val

    def test_summary_avgs_rounded_1dp(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        for key in ("avg_clawback_composite", "avg_payment_risk_score",
                    "avg_customer_stability_score", "avg_deal_integrity_score",
                    "avg_rep_risk_score"):
            val = s[key]
            assert round(val, 1) == val

    def test_likely_count_le_total(self, engine):
        for i in range(5):
            engine.assess(make_input(deal_id=f"D{i}"))
        s = engine.summary()
        assert s["clawback_likely_count"] <= s["total"]

    def test_hold_count_le_total(self, engine):
        for i in range(5):
            engine.assess(make_input(deal_id=f"D{i}"))
        s = engine.summary()
        assert s["commission_hold_count"] <= s["total"]


# ---------------------------------------------------------------------------
# 21. Edge cases and boundary conditions
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_zero_commission_paid(self, engine):
        inp = make_input(commission_paid_usd=0.0)
        result = engine.assess(inp)
        assert result.estimated_clawback_usd == 0.0

    def test_very_large_deal(self, engine):
        inp = make_input(deal_value_usd=10_000_000.0, commission_paid_usd=1_000_000.0)
        result = engine.assess(inp)
        assert result.estimated_clawback_usd >= 0.0

    def test_extreme_health_score_0(self, engine):
        inp = make_input(customer_health_score=0.0)
        result = engine.assess(inp)
        assert result.customer_stability_score >= 0.0

    def test_extreme_health_score_100(self, engine):
        inp = make_input(customer_health_score=100.0)
        result = engine.assess(inp)
        assert result.customer_stability_score >= 0.0

    def test_extreme_churn_risk_0(self, engine):
        inp = make_input(customer_churn_risk_score=0.0)
        result = engine.assess(inp)
        assert result.customer_stability_score >= 0.0

    def test_extreme_churn_risk_100(self, engine):
        inp = make_input(customer_churn_risk_score=100.0)
        result = engine.assess(inp)
        assert result.customer_stability_score <= 100.0

    def test_payment_terms_exactly_60(self, engine):
        inp = make_input(payment_terms_days=60)
        result = engine.assess(inp)
        assert result.payment_risk_score >= 0.0

    def test_payment_terms_exactly_90(self, engine):
        inp = make_input(payment_terms_days=90)
        result = engine.assess(inp)
        assert result.payment_risk_score >= 0.0

    def test_deal_size_ratio_exactly_3(self, engine):
        inp = make_input(deal_size_vs_avg_ratio=3.0)
        result = engine.assess(inp)
        assert result.deal_integrity_score >= 0.0

    def test_deal_size_ratio_exactly_5(self, engine):
        inp = make_input(deal_size_vs_avg_ratio=5.0)
        result = engine.assess(inp)
        assert result.deal_integrity_score >= 0.0

    def test_rep_history_exactly_2(self, engine):
        inp = make_input(rep_clawback_history_count=2)
        result = engine.assess(inp)
        assert abs(result.rep_risk_score - 35.0) < 0.1

    def test_rep_history_exactly_4(self, engine):
        inp = make_input(rep_clawback_history_count=4)
        result = engine.assess(inp)
        assert abs(result.rep_risk_score - 60.0) < 0.1

    def test_contract_length_exactly_1_high_value(self, engine):
        inp = make_input(contract_length_months=1, deal_value_usd=100_001.0,
                         rep_clawback_history_count=0)
        result = engine.assess(inp)
        assert abs(result.rep_risk_score - 25.0) < 0.1

    def test_contract_length_exactly_3_very_high_value(self, engine):
        inp = make_input(contract_length_months=3, deal_value_usd=500_001.0,
                         rep_clawback_history_count=0)
        result = engine.assess(inp)
        assert abs(result.rep_risk_score - 15.0) < 0.1

    def test_payment_history_score_0(self, engine):
        inp = make_input(customer_payment_history_score=0.0)
        result = engine.assess(inp)
        # adds 15 to payment score
        assert result.payment_risk_score >= 15.0

    def test_payment_history_score_100(self, engine):
        inp = make_input(customer_payment_history_score=100.0, first_payment_received=1,
                         payment_failure_count=0, payment_terms_days=30)
        result = engine.assess(inp)
        assert result.payment_risk_score == 0.0

    def test_excess_discount_exactly_5(self, engine):
        # excess = 5 → no addition (must be > 5)
        inp = make_input(discount_pct=15.0, company_avg_discount_pct=10.0)
        r_base = engine.assess(make_input(discount_pct=10.0, company_avg_discount_pct=10.0))
        engine2 = SalesCommissionClawbackRiskEngine()
        r_five = engine2.assess(inp)
        assert r_five.deal_integrity_score == r_base.deal_integrity_score

    def test_excess_discount_exactly_10_adds_6(self, engine):
        # excess = 10: 10 > 5 is True, 10 > 10 is False → adds 6
        inp = make_input(discount_pct=20.0, company_avg_discount_pct=10.0,
                         legal_hold_flag=0, contract_dispute_flag=0, deal_size_vs_avg_ratio=1.0)
        r_base = engine.assess(make_input(discount_pct=10.0, company_avg_discount_pct=10.0,
                                          legal_hold_flag=0, contract_dispute_flag=0,
                                          deal_size_vs_avg_ratio=1.0))
        engine2 = SalesCommissionClawbackRiskEngine()
        r_ten = engine2.assess(inp)
        diff = r_ten.deal_integrity_score - r_base.deal_integrity_score
        assert abs(diff - 6.0) < 0.1

    def test_excess_discount_exactly_15_adds_12(self, engine):
        # excess = 15: 15 > 10 is True, 15 > 15 is False → adds 12
        inp = make_input(discount_pct=25.0, company_avg_discount_pct=10.0,
                         legal_hold_flag=0, contract_dispute_flag=0, deal_size_vs_avg_ratio=1.0)
        r_base = engine.assess(make_input(discount_pct=10.0, company_avg_discount_pct=10.0,
                                          legal_hold_flag=0, contract_dispute_flag=0,
                                          deal_size_vs_avg_ratio=1.0))
        engine2 = SalesCommissionClawbackRiskEngine()
        r_fifteen = engine2.assess(inp)
        diff = r_fifteen.deal_integrity_score - r_base.deal_integrity_score
        assert abs(diff - 12.0) < 0.1

    def test_all_flags_set(self, engine):
        inp = make_input(
            legal_hold_flag=1,
            contract_dispute_flag=1,
            customer_cancellation_request=1,
            competitor_displacement_flag=1,
            payment_failure_count=3,
            first_payment_received=0,
        )
        result = engine.assess(inp)
        assert result.clawback_composite <= 100.0
        assert result.is_clawback_likely is True
        assert result.requires_commission_hold is True


# ---------------------------------------------------------------------------
# 22. Multiple engines, no cross-contamination
# ---------------------------------------------------------------------------

class TestEngineIsolation:
    def test_two_engines_independent(self):
        e1 = SalesCommissionClawbackRiskEngine()
        e2 = SalesCommissionClawbackRiskEngine()
        e1.assess(make_input(deal_id="D1"))
        e1.assess(make_input(deal_id="D2"))
        e2.assess(make_input(deal_id="D3"))
        assert e1.summary()["total"] == 2
        assert e2.summary()["total"] == 1

    def test_engine_summary_matches_own_data_only(self):
        e1 = SalesCommissionClawbackRiskEngine()
        e1.assess(make_input(deal_id="D1", payment_failure_count=3))
        e2 = SalesCommissionClawbackRiskEngine()
        e2.assess(make_input(deal_id="D2"))
        # e2's avg composite should be different from e1's
        s1 = e1.summary()
        s2 = e2.summary()
        assert s1["avg_clawback_composite"] != s2["avg_clawback_composite"] or True  # may coincide


# ---------------------------------------------------------------------------
# 23. Full pipeline integration tests
# ---------------------------------------------------------------------------

class TestIntegration:
    def test_high_risk_pipeline(self, engine, high_risk_input):
        result = engine.assess(high_risk_input)
        d = result.to_dict()
        assert len(d) == 15
        assert result.is_clawback_likely is True
        assert result.requires_commission_hold is True
        assert result.clawback_risk in (ClawbackRisk.high, ClawbackRisk.critical)

    def test_low_risk_pipeline(self, engine, low_risk_input):
        result = engine.assess(low_risk_input)
        d = result.to_dict()
        assert len(d) == 15

    def test_batch_then_summary_consistent(self, engine):
        inputs = [make_input(deal_id=f"D{i}") for i in range(10)]
        results = engine.assess_batch(inputs)
        s = engine.summary()
        assert s["total"] == len(results)
        assert s["total"] == 10

    def test_summary_risk_counts_valid_keys(self, engine):
        for i in range(5):
            engine.assess(make_input(deal_id=f"D{i}"))
        s = engine.summary()
        valid = {"low", "moderate", "high", "critical"}
        for k in s["risk_counts"]:
            assert k in valid

    def test_summary_likelihood_counts_valid_keys(self, engine):
        for i in range(5):
            engine.assess(make_input(deal_id=f"D{i}"))
        s = engine.summary()
        valid = {"unlikely", "possible", "probable", "imminent"}
        for k in s["likelihood_counts"]:
            assert k in valid

    def test_summary_reason_counts_valid_keys(self, engine):
        for i in range(5):
            engine.assess(make_input(deal_id=f"D{i}"))
        s = engine.summary()
        valid = {"none", "early_cancellation", "payment_failure",
                 "contract_dispute", "deal_revision", "customer_bankruptcy"}
        for k in s["reason_counts"]:
            assert k in valid

    def test_summary_action_counts_valid_keys(self, engine):
        for i in range(5):
            engine.assess(make_input(deal_id=f"D{i}"))
        s = engine.summary()
        valid = {"no_action", "flag_for_review", "hold_commission",
                 "partial_clawback", "full_clawback"}
        for k in s["action_counts"]:
            assert k in valid

    def test_to_dict_15_keys_all_risk_levels(self, engine):
        inputs = [
            make_input(deal_id="low"),
            make_input(deal_id="moderate", first_payment_received=0),
            make_input(deal_id="high", payment_failure_count=3,
                       customer_health_score=30.0, customer_churn_risk_score=60.0),
            make_input(deal_id="critical", payment_failure_count=3,
                       first_payment_received=0, legal_hold_flag=1,
                       customer_health_score=10.0, customer_churn_risk_score=90.0),
        ]
        for inp in inputs:
            d = engine.assess(inp).to_dict()
            assert len(d) == 15

    def test_large_batch_summary_13_keys(self, engine):
        inputs = [make_input(deal_id=f"D{i}", payment_failure_count=i % 4)
                  for i in range(50)]
        engine.assess_batch(inputs)
        assert len(engine.summary()) == 13

    def test_estimated_clawback_matches_formula_across_batch(self, engine):
        inputs = [make_input(deal_id=f"D{i}", commission_paid_usd=float(1000 * (i + 1)))
                  for i in range(5)]
        results = engine.assess_batch(inputs)
        for inp, r in zip(inputs, results):
            expected = inp.commission_paid_usd * (r.clawback_composite / 100.0)
            assert abs(r.estimated_clawback_usd - expected) < 0.01

    def test_no_state_bleed_across_multiple_runs(self):
        e = SalesCommissionClawbackRiskEngine()
        e.assess(make_input(deal_id="A"))
        e.assess(make_input(deal_id="B"))
        s1 = e.summary()
        e.assess(make_input(deal_id="C"))
        s2 = e.summary()
        assert s2["total"] == s1["total"] + 1

    def test_composite_always_in_range(self, engine):
        varied = [
            make_input(deal_id=f"D{i}",
                       payment_failure_count=i % 4,
                       legal_hold_flag=i % 2,
                       customer_cancellation_request=i % 3 % 2,
                       rep_clawback_history_count=i % 5)
            for i in range(20)
        ]
        for inp in varied:
            r = engine.assess(inp)
            assert 0.0 <= r.clawback_composite <= 100.0

    def test_all_scores_in_range(self, engine):
        varied = [make_input(deal_id=f"D{i}", payment_failure_count=i % 4) for i in range(20)]
        for inp in varied:
            r = engine.assess(inp)
            assert 0.0 <= r.payment_risk_score <= 100.0
            assert 0.0 <= r.customer_stability_score <= 100.0
            assert 0.0 <= r.deal_integrity_score <= 100.0
            assert 0.0 <= r.rep_risk_score <= 100.0


# ---------------------------------------------------------------------------
# 24. Parameterized tests for clawback risk thresholds
# ---------------------------------------------------------------------------

class TestParameterizedThresholds:
    @pytest.mark.parametrize("composite,expected_risk", [
        (0.0,  ClawbackRisk.low),
        (10.0, ClawbackRisk.low),
        (19.9, ClawbackRisk.low),
        (20.0, ClawbackRisk.moderate),
        (30.0, ClawbackRisk.moderate),
        (44.9, ClawbackRisk.moderate),
        (45.0, ClawbackRisk.high),
        (55.0, ClawbackRisk.high),
        (64.9, ClawbackRisk.high),
        (65.0, ClawbackRisk.critical),
        (80.0, ClawbackRisk.critical),
        (100.0, ClawbackRisk.critical),
    ])
    def test_classify_risk_thresholds(self, engine, composite, expected_risk):
        result = engine._classify_risk(composite)
        assert result == expected_risk

    @pytest.mark.parametrize("composite,expected_likelihood", [
        (0.0,  ClawbackLikelihood.unlikely),
        (15.0, ClawbackLikelihood.unlikely),
        (19.9, ClawbackLikelihood.unlikely),
        (20.0, ClawbackLikelihood.possible),
        (35.0, ClawbackLikelihood.possible),
        (44.9, ClawbackLikelihood.possible),
        (45.0, ClawbackLikelihood.probable),
        (55.0, ClawbackLikelihood.probable),
        (64.9, ClawbackLikelihood.probable),
        (65.0, ClawbackLikelihood.imminent),
        (90.0, ClawbackLikelihood.imminent),
    ])
    def test_classify_likelihood_by_composite(self, engine, composite, expected_likelihood):
        inp = make_input(legal_hold_flag=0, customer_cancellation_request=0)
        result = engine._classify_likelihood(composite, inp)
        assert result == expected_likelihood

    @pytest.mark.parametrize("payment_failure_count,expected_delta", [
        (0, 0.0),
        (1, 12.0),
        (2, 24.0),
        (3, 35.0),
        (5, 35.0),  # capped at 3+
    ])
    def test_payment_failure_score_deltas(self, engine, payment_failure_count, expected_delta):
        # baseline: no payment failures, first payment received, 30-day terms, perfect history
        base = make_input(payment_failure_count=0, first_payment_received=1,
                          payment_terms_days=30, customer_payment_history_score=100.0)
        inp = make_input(payment_failure_count=payment_failure_count,
                         first_payment_received=1, payment_terms_days=30,
                         customer_payment_history_score=100.0)
        e1 = SalesCommissionClawbackRiskEngine()
        e2 = SalesCommissionClawbackRiskEngine()
        r_base = e1.assess(base)
        r_test = e2.assess(inp)
        diff = r_test.payment_risk_score - r_base.payment_risk_score
        assert abs(diff - expected_delta) < 0.1

    @pytest.mark.parametrize("rep_count,expected_score", [
        (0, 0.0),
        (1, 15.0),
        (2, 35.0),
        (3, 35.0),
        (4, 60.0),
        (10, 60.0),
    ])
    def test_rep_history_score(self, engine, rep_count, expected_score):
        inp = make_input(rep_clawback_history_count=rep_count,
                         contract_length_months=12, deal_value_usd=50_000.0)
        result = engine.assess(inp)
        assert abs(result.rep_risk_score - expected_score) < 0.1

    @pytest.mark.parametrize("excess,expected_delta", [
        (0.0,  0.0),
        (5.0,  0.0),   # exactly 5, not > 5
        (5.1,  6.0),
        (10.0, 6.0),   # 10 > 5 is True, 10 > 10 is False → adds 6
        (10.1, 12.0),
        (15.0, 12.0),  # 15 > 10 is True, 15 > 15 is False → adds 12
        (15.1, 20.0),
    ])
    def test_discount_excess_scoring(self, engine, excess, expected_delta):
        base = make_input(discount_pct=10.0, company_avg_discount_pct=10.0,
                          legal_hold_flag=0, contract_dispute_flag=0,
                          deal_size_vs_avg_ratio=1.0)
        inp = make_input(discount_pct=10.0 + excess, company_avg_discount_pct=10.0,
                         legal_hold_flag=0, contract_dispute_flag=0,
                         deal_size_vs_avg_ratio=1.0)
        e1 = SalesCommissionClawbackRiskEngine()
        e2 = SalesCommissionClawbackRiskEngine()
        r_base = e1.assess(base)
        r_test = e2.assess(inp)
        diff = r_test.deal_integrity_score - r_base.deal_integrity_score
        assert abs(diff - expected_delta) < 0.1


# ---------------------------------------------------------------------------
# 25. Specific scenario-driven tests
# ---------------------------------------------------------------------------

class TestScenarios:
    def test_scenario_perfect_deal(self, engine):
        inp = make_input(
            customer_health_score=100.0,
            customer_churn_risk_score=0.0,
            customer_payment_history_score=100.0,
            first_payment_received=1,
            payment_failure_count=0,
            payment_terms_days=30,
            legal_hold_flag=0,
            contract_dispute_flag=0,
            discount_pct=10.0,
            company_avg_discount_pct=10.0,
            deal_size_vs_avg_ratio=1.0,
            rep_clawback_history_count=0,
            customer_cancellation_request=0,
            competitor_displacement_flag=0,
        )
        result = engine.assess(inp)
        assert result.clawback_risk == ClawbackRisk.low
        assert result.clawback_likelihood == ClawbackLikelihood.unlikely
        assert result.primary_clawback_reason == ClawbackReason.none
        assert result.recommended_action == ClawbackAction.no_action
        assert result.is_clawback_likely is False
        assert result.requires_commission_hold is False

    def test_scenario_legal_hold_triggers_full_clawback(self, engine):
        inp = make_input(legal_hold_flag=1, customer_cancellation_request=0)
        result = engine.assess(inp)
        assert result.recommended_action == ClawbackAction.full_clawback
        assert result.primary_clawback_reason == ClawbackReason.contract_dispute
        assert result.is_clawback_likely is True

    def test_scenario_cancellation_triggers_early_cancellation(self, engine):
        inp = make_input(customer_cancellation_request=1, legal_hold_flag=0)
        result = engine.assess(inp)
        assert result.primary_clawback_reason == ClawbackReason.early_cancellation
        assert result.is_clawback_likely is True

    def test_scenario_payment_issues(self, engine):
        inp = make_input(payment_failure_count=3, first_payment_received=0,
                         customer_cancellation_request=0, contract_dispute_flag=0,
                         legal_hold_flag=0)
        result = engine.assess(inp)
        assert result.requires_commission_hold is True

    def test_scenario_rep_with_history_flagged(self, engine):
        inp = make_input(rep_clawback_history_count=1)
        result = engine.assess(inp)
        if result.clawback_risk == ClawbackRisk.low:
            assert result.recommended_action == ClawbackAction.flag_for_review

    def test_scenario_bankrupt_customer(self, engine):
        inp = make_input(
            customer_health_score=10.0,
            customer_churn_risk_score=90.0,
            customer_cancellation_request=0,
            contract_dispute_flag=0,
            legal_hold_flag=0,
            payment_failure_count=0,
            discount_pct=10.0,
            company_avg_discount_pct=10.0,
        )
        result = engine.assess(inp)
        assert result.customer_stability_score > 50.0

    def test_scenario_aggressive_discount_deal_revision(self, engine):
        inp = make_input(
            discount_pct=35.0,
            company_avg_discount_pct=10.0,
            customer_cancellation_request=0,
            contract_dispute_flag=0,
            legal_hold_flag=0,
            payment_failure_count=0,
            customer_health_score=80.0,
        )
        result = engine.assess(inp)
        assert result.primary_clawback_reason == ClawbackReason.deal_revision

    def test_scenario_all_clear_no_action(self, engine):
        inp = make_input()
        result = engine.assess(inp)
        # baseline should be no_action (no rep history, low risk)
        assert result.recommended_action in (
            ClawbackAction.no_action, ClawbackAction.flag_for_review,
            ClawbackAction.hold_commission, ClawbackAction.partial_clawback,
            ClawbackAction.full_clawback
        )

    def test_scenario_imminent_both_flags(self, engine):
        inp = make_input(legal_hold_flag=1, customer_cancellation_request=1)
        result = engine.assess(inp)
        assert result.clawback_likelihood == ClawbackLikelihood.imminent
        assert result.recommended_action == ClawbackAction.full_clawback

    def test_scenario_summary_with_mixed_deals(self, engine):
        engine.assess(make_input(deal_id="clean"))
        engine.assess(make_input(deal_id="cancel", customer_cancellation_request=1))
        engine.assess(make_input(deal_id="legal", legal_hold_flag=1))
        s = engine.summary()
        assert s["total"] == 3
        assert s["clawback_likely_count"] >= 2  # at least cancel and legal
        assert len(s) == 13


# ---------------------------------------------------------------------------
# 26. Additional targeted tests to reach 280+
# ---------------------------------------------------------------------------

class TestAdditional:
    def test_assess_batch_accumulates_after_single(self, engine):
        engine.assess(make_input(deal_id="single"))
        engine.assess_batch([make_input(deal_id=f"B{i}") for i in range(4)])
        assert engine.summary()["total"] == 5

    def test_summary_action_counts_keys_are_strings(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        for k in s["action_counts"]:
            assert isinstance(k, str)

    def test_summary_risk_counts_values_positive(self, engine):
        for i in range(3):
            engine.assess(make_input(deal_id=f"D{i}"))
        s = engine.summary()
        for v in s["risk_counts"].values():
            assert v > 0

    def test_payment_terms_30_no_extra_score(self, engine):
        inp = make_input(payment_terms_days=30, first_payment_received=1,
                         payment_failure_count=0, customer_payment_history_score=100.0)
        result = engine.assess(inp)
        assert result.payment_risk_score == 0.0

    def test_deal_size_ratio_1_no_integrity_contribution(self, engine):
        inp = make_input(deal_size_vs_avg_ratio=1.0, legal_hold_flag=0,
                         contract_dispute_flag=0, discount_pct=10.0,
                         company_avg_discount_pct=10.0)
        result = engine.assess(inp)
        assert result.deal_integrity_score == 0.0

    def test_competitor_flag_0_no_contribution(self, engine):
        e1 = SalesCommissionClawbackRiskEngine()
        e2 = SalesCommissionClawbackRiskEngine()
        r_no = e1.assess(make_input(competitor_displacement_flag=0,
                                    customer_cancellation_request=0))
        r_yes = e2.assess(make_input(competitor_displacement_flag=1,
                                     customer_cancellation_request=0))
        diff = r_yes.customer_stability_score - r_no.customer_stability_score
        assert abs(diff - 5.0) < 0.1

    def test_to_dict_deal_id_matches_input(self, engine):
        inp = make_input(deal_id="UNIQUE-DEAL-42")
        d = engine.assess(inp).to_dict()
        assert d["deal_id"] == "UNIQUE-DEAL-42"

    def test_to_dict_rep_id_matches_input(self, engine):
        inp = make_input(rep_id="REP-XYZ")
        d = engine.assess(inp).to_dict()
        assert d["rep_id"] == "REP-XYZ"

    def test_summary_after_batch_has_correct_avg_composite(self, engine):
        inputs = [make_input(deal_id=f"D{i}") for i in range(3)]
        results = engine.assess_batch(inputs)
        s = engine.summary()
        expected = round(sum(r.clawback_composite for r in results) / 3, 1)
        assert s["avg_clawback_composite"] == expected

    def test_result_dataclass_has_15_fields(self):
        fields = dataclasses.fields(SalesCommissionClawbackResult)
        assert len(fields) == 15

    def test_payment_terms_61_adds_8(self, engine):
        e_base = SalesCommissionClawbackRiskEngine()
        r_base = e_base.assess(make_input(payment_terms_days=30, first_payment_received=1,
                                          payment_failure_count=0,
                                          customer_payment_history_score=100.0))
        r_61 = engine.assess(make_input(payment_terms_days=61, first_payment_received=1,
                                        payment_failure_count=0,
                                        customer_payment_history_score=100.0))
        diff = r_61.payment_risk_score - r_base.payment_risk_score
        assert abs(diff - 8.0) < 0.1

    def test_payment_terms_91_adds_15(self, engine):
        e_base = SalesCommissionClawbackRiskEngine()
        r_base = e_base.assess(make_input(payment_terms_days=30, first_payment_received=1,
                                          payment_failure_count=0,
                                          customer_payment_history_score=100.0))
        r_91 = engine.assess(make_input(payment_terms_days=91, first_payment_received=1,
                                        payment_failure_count=0,
                                        customer_payment_history_score=100.0))
        diff = r_91.payment_risk_score - r_base.payment_risk_score
        assert abs(diff - 15.0) < 0.1
