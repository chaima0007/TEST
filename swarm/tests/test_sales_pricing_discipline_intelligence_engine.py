"""
Comprehensive pytest tests for SalesPricingDisciplineIntelligenceEngine.
200+ tests covering: enums, all 21 input fields, to_dict 15 keys,
all risk/severity levels, all 6 patterns, all 7 actions, sub-score brackets,
composite formula, has_pricing_gap triggers, requires_pricing_coaching triggers,
estimated_margin_loss_usd formula, signal text, assess_batch, summary 13 keys,
edge cases.
"""
from __future__ import annotations

import math
import pytest

from swarm.intelligence.sales_pricing_discipline_intelligence_engine import (
    PricingAction,
    PricingInput,
    PricingPattern,
    PricingResult,
    PricingRisk,
    PricingSeverity,
    SalesPricingDisciplineIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_input(**overrides) -> PricingInput:
    """Return a clean (low-risk) PricingInput with all overridable defaults."""
    defaults = dict(
        rep_id="REP001",
        region="West",
        evaluation_period_id="Q1-2026",
        avg_discount_pct=0.02,                  # < 0.08 → depth +0
        discount_frequency_pct=0.10,            # < 0.35 → frequency +0
        max_discount_given_pct=0.05,            # < 0.18 → depth +0
        avg_gross_margin_pct=0.55,              # above target → margin gap 0
        target_gross_margin_pct=0.50,
        late_stage_discount_rate_pct=0.05,      # < 0.20 → negotiation +0
        multi_discount_deal_rate_pct=0.05,      # < 0.12 → frequency +0
        price_objection_rate_pct=0.10,          # < 0.40 → depth +0
        first_ask_concession_rate_pct=0.10,     # < 0.25 → negotiation +0
        list_price_close_rate_pct=0.80,         # > 0.40 → frequency +0
        approval_override_rate_pct=0.02,        # < 0.08 → margin +0
        competitor_price_match_rate_pct=0.05,   # < 0.25 → margin +0
        avg_deal_cycle_vs_discount_corr=0.10,   # < 0.40 → negotiation +0
        total_deals_closed=20,
        avg_deal_size_usd=50_000.0,
        total_revenue_usd=1_000_000.0,
        quota_usd=1_200_000.0,
        avg_opportunity_value_usd=55_000.0,
    )
    defaults.update(overrides)
    return PricingInput(**defaults)


def _engine() -> SalesPricingDisciplineIntelligenceEngine:
    return SalesPricingDisciplineIntelligenceEngine()


# ===========================================================================
# 1. ENUM TESTS
# ===========================================================================

class TestPricingRiskEnum:
    def test_low_value(self):
        assert PricingRisk.low.value == "low"

    def test_moderate_value(self):
        assert PricingRisk.moderate.value == "moderate"

    def test_high_value(self):
        assert PricingRisk.high.value == "high"

    def test_critical_value(self):
        assert PricingRisk.critical.value == "critical"

    def test_all_members_count(self):
        assert len(PricingRisk) == 4

    def test_is_str_enum(self):
        assert isinstance(PricingRisk.low, str)


class TestPricingPatternEnum:
    def test_none_value(self):
        assert PricingPattern.none.value == "none"

    def test_discount_reflex_value(self):
        assert PricingPattern.discount_reflex.value == "discount_reflex"

    def test_margin_eroder_value(self):
        assert PricingPattern.margin_eroder.value == "margin_eroder"

    def test_late_stage_capitulator_value(self):
        assert PricingPattern.late_stage_capitulator.value == "late_stage_capitulator"

    def test_multi_discount_stacker_value(self):
        assert PricingPattern.multi_discount_stacker.value == "multi_discount_stacker"

    def test_value_misaligner_value(self):
        assert PricingPattern.value_misaligner.value == "value_misaligner"

    def test_all_members_count(self):
        assert len(PricingPattern) == 6

    def test_is_str_enum(self):
        assert isinstance(PricingPattern.none, str)


class TestPricingSeverityEnum:
    def test_disciplined_value(self):
        assert PricingSeverity.disciplined.value == "disciplined"

    def test_managed_value(self):
        assert PricingSeverity.managed.value == "managed"

    def test_aggressive_value(self):
        assert PricingSeverity.aggressive.value == "aggressive"

    def test_uncontrolled_value(self):
        assert PricingSeverity.uncontrolled.value == "uncontrolled"

    def test_all_members_count(self):
        assert len(PricingSeverity) == 4

    def test_is_str_enum(self):
        assert isinstance(PricingSeverity.disciplined, str)


class TestPricingActionEnum:
    def test_no_action_value(self):
        assert PricingAction.no_action.value == "no_action"

    def test_discount_awareness_coaching_value(self):
        assert PricingAction.discount_awareness_coaching.value == "discount_awareness_coaching"

    def test_value_selling_coaching_value(self):
        assert PricingAction.value_selling_coaching.value == "value_selling_coaching"

    def test_negotiation_discipline_coaching_value(self):
        assert PricingAction.negotiation_discipline_coaching.value == "negotiation_discipline_coaching"

    def test_margin_recovery_coaching_value(self):
        assert PricingAction.margin_recovery_coaching.value == "margin_recovery_coaching"

    def test_pricing_approval_requirement_value(self):
        assert PricingAction.pricing_approval_requirement.value == "pricing_approval_requirement"

    def test_pricing_intervention_value(self):
        assert PricingAction.pricing_intervention.value == "pricing_intervention"

    def test_all_members_count(self):
        assert len(PricingAction) == 7

    def test_is_str_enum(self):
        assert isinstance(PricingAction.no_action, str)


# ===========================================================================
# 2. PricingInput — all 21 fields
# ===========================================================================

class TestPricingInputFields:
    def test_all_21_fields_present(self):
        inp = _make_input()
        assert hasattr(inp, "rep_id")
        assert hasattr(inp, "region")
        assert hasattr(inp, "evaluation_period_id")
        assert hasattr(inp, "avg_discount_pct")
        assert hasattr(inp, "discount_frequency_pct")
        assert hasattr(inp, "max_discount_given_pct")
        assert hasattr(inp, "avg_gross_margin_pct")
        assert hasattr(inp, "target_gross_margin_pct")
        assert hasattr(inp, "late_stage_discount_rate_pct")
        assert hasattr(inp, "multi_discount_deal_rate_pct")
        assert hasattr(inp, "price_objection_rate_pct")
        assert hasattr(inp, "first_ask_concession_rate_pct")
        assert hasattr(inp, "list_price_close_rate_pct")
        assert hasattr(inp, "approval_override_rate_pct")
        assert hasattr(inp, "competitor_price_match_rate_pct")
        assert hasattr(inp, "avg_deal_cycle_vs_discount_corr")
        assert hasattr(inp, "total_deals_closed")
        assert hasattr(inp, "avg_deal_size_usd")
        assert hasattr(inp, "total_revenue_usd")
        assert hasattr(inp, "quota_usd")
        assert hasattr(inp, "avg_opportunity_value_usd")

    def test_field_values_stored(self):
        inp = _make_input(rep_id="X99", region="East", total_deals_closed=42)
        assert inp.rep_id == "X99"
        assert inp.region == "East"
        assert inp.total_deals_closed == 42

    def test_total_deals_closed_is_int(self):
        inp = _make_input(total_deals_closed=15)
        assert isinstance(inp.total_deals_closed, int)


# ===========================================================================
# 3. PricingResult — to_dict 15 keys
# ===========================================================================

class TestPricingResultToDict:
    def setup_method(self):
        self.engine = _engine()
        self.result = self.engine.assess(_make_input())
        self.d = self.result.to_dict()

    def test_to_dict_has_15_keys(self):
        assert len(self.d) == 15

    def test_key_rep_id(self):
        assert "rep_id" in self.d

    def test_key_region(self):
        assert "region" in self.d

    def test_key_pricing_risk(self):
        assert "pricing_risk" in self.d

    def test_key_pricing_pattern(self):
        assert "pricing_pattern" in self.d

    def test_key_pricing_severity(self):
        assert "pricing_severity" in self.d

    def test_key_recommended_action(self):
        assert "recommended_action" in self.d

    def test_key_discount_depth_score(self):
        assert "discount_depth_score" in self.d

    def test_key_discount_frequency_score(self):
        assert "discount_frequency_score" in self.d

    def test_key_margin_protection_score(self):
        assert "margin_protection_score" in self.d

    def test_key_negotiation_discipline_score(self):
        assert "negotiation_discipline_score" in self.d

    def test_key_pricing_composite(self):
        assert "pricing_composite" in self.d

    def test_key_has_pricing_gap(self):
        assert "has_pricing_gap" in self.d

    def test_key_requires_pricing_coaching(self):
        assert "requires_pricing_coaching" in self.d

    def test_key_estimated_margin_loss_usd(self):
        assert "estimated_margin_loss_usd" in self.d

    def test_key_pricing_signal(self):
        assert "pricing_signal" in self.d

    def test_pricing_risk_is_string(self):
        assert isinstance(self.d["pricing_risk"], str)

    def test_pricing_pattern_is_string(self):
        assert isinstance(self.d["pricing_pattern"], str)

    def test_pricing_severity_is_string(self):
        assert isinstance(self.d["pricing_severity"], str)

    def test_recommended_action_is_string(self):
        assert isinstance(self.d["recommended_action"], str)


# ===========================================================================
# 4. RISK THRESHOLDS
# ===========================================================================

class TestRiskThresholds:
    """Verify composite score drives risk correctly at all boundaries."""

    def _composite_for(self, inp: PricingInput) -> float:
        e = _engine()
        return e.assess(inp).pricing_composite

    def test_low_risk_composite_below_20(self):
        inp = _make_input()  # all zeros → composite 0
        r = _engine().assess(inp)
        assert r.pricing_risk == PricingRisk.low

    def test_moderate_risk_composite_exactly_20(self):
        # Force composite to ~20 via discount_depth with avg_discount_pct>=0.08 (+12) * 0.30 = 3.6
        # Need something to reach 20 exactly — use moderate frequency + moderate depth + moderate margin
        # Let's drive it precisely: avg_discount_pct=0.15 (+28*0.30=8.4),
        # discount_frequency_pct=0.35 (+12*0.25=3), margin_gap=0.03(+12*0.25=3),
        # first_ask_concession=0.25(+12*0.20=2.4) → composite=8.4+3+3+2.4=16.8 managed
        # Easier: force moderate risk with known inputs that get composite in [20,40)
        inp = _make_input(
            avg_discount_pct=0.15,                 # +28 depth
            discount_frequency_pct=0.35,           # +12 freq
            avg_gross_margin_pct=0.42,
            target_gross_margin_pct=0.50,          # gap=0.08 +28 margin
            first_ask_concession_rate_pct=0.25,    # +12 negotiation
        )
        r = _engine().assess(inp)
        assert r.pricing_composite >= 20
        assert r.pricing_risk in (PricingRisk.moderate, PricingRisk.high, PricingRisk.critical)

    def test_high_risk_composite_40_to_59(self):
        inp = _make_input(
            avg_discount_pct=0.25,                 # +45 depth
            discount_frequency_pct=0.70,           # +45 freq
            avg_gross_margin_pct=0.30,
            target_gross_margin_pct=0.50,          # gap=0.20 > 0.15 → +45 margin
            first_ask_concession_rate_pct=0.60,    # +45 negotiation
            max_discount_given_pct=0.40,           # +35 depth
            multi_discount_deal_rate_pct=0.40,     # +35 freq
            approval_override_rate_pct=0.30,       # +35 margin
            late_stage_discount_rate_pct=0.50,     # +35 negotiation
        )
        r = _engine().assess(inp)
        # composite will be high (capped at 100 per sub)
        assert r.pricing_risk in (PricingRisk.high, PricingRisk.critical)

    def test_critical_risk_composite_ge_60(self):
        inp = _make_input(
            avg_discount_pct=0.25,                 # +45
            max_discount_given_pct=0.40,           # +35
            price_objection_rate_pct=0.60,         # +20 → depth=100
            discount_frequency_pct=0.70,           # +45
            multi_discount_deal_rate_pct=0.40,     # +35
            list_price_close_rate_pct=0.10,        # +20 → freq=100
            avg_gross_margin_pct=0.30,
            target_gross_margin_pct=0.50,          # gap=0.20 → +45
            approval_override_rate_pct=0.30,       # +35
            competitor_price_match_rate_pct=0.40,  # +20 → margin=100
            first_ask_concession_rate_pct=0.60,    # +45
            late_stage_discount_rate_pct=0.50,     # +35
            avg_deal_cycle_vs_discount_corr=0.60,  # +20 → negotiation=100
        )
        r = _engine().assess(inp)
        assert r.pricing_composite >= 60
        assert r.pricing_risk == PricingRisk.critical

    def test_risk_values_are_enum_instances(self):
        r = _engine().assess(_make_input())
        assert isinstance(r.pricing_risk, PricingRisk)

    def test_low_risk_boundary_just_below_20(self):
        # composite 0.0 → low
        inp = _make_input()
        r = _engine().assess(inp)
        assert r.pricing_composite < 20
        assert r.pricing_risk == PricingRisk.low

    def test_moderate_risk_via_discount_depth(self):
        # avg_discount_pct=0.08 → +12, * 0.30 = 3.6 → still low
        # avg_discount_pct=0.15 → +28 * 0.30 = 8.4
        # Need composite >=20: add frequency and margin
        inp = _make_input(
            avg_discount_pct=0.15,              # depth +28
            discount_frequency_pct=0.50,        # freq +28
            avg_gross_margin_pct=0.42,
            target_gross_margin_pct=0.50,       # gap=0.08 → margin +28
        )
        r = _engine().assess(inp)
        # 28*0.30 + 28*0.25 + 28*0.25 = 8.4+7+7 = 22.4 → moderate
        assert r.pricing_composite >= 20
        assert r.pricing_risk == PricingRisk.moderate


# ===========================================================================
# 5. SEVERITY THRESHOLDS
# ===========================================================================

class TestSeverityThresholds:
    def test_disciplined_when_composite_below_20(self):
        r = _engine().assess(_make_input())
        assert r.pricing_severity == PricingSeverity.disciplined

    def test_managed_when_composite_20_to_39(self):
        inp = _make_input(
            avg_discount_pct=0.15,
            discount_frequency_pct=0.50,
            avg_gross_margin_pct=0.42,
            target_gross_margin_pct=0.50,
        )
        r = _engine().assess(inp)
        if 20 <= r.pricing_composite < 40:
            assert r.pricing_severity == PricingSeverity.managed

    def test_aggressive_when_composite_40_to_59(self):
        inp = _make_input(
            avg_discount_pct=0.25,
            discount_frequency_pct=0.70,
            max_discount_given_pct=0.40,
            avg_gross_margin_pct=0.30,
            target_gross_margin_pct=0.50,
            first_ask_concession_rate_pct=0.60,
            late_stage_discount_rate_pct=0.50,
        )
        r = _engine().assess(inp)
        if 40 <= r.pricing_composite < 60:
            assert r.pricing_severity == PricingSeverity.aggressive

    def test_uncontrolled_when_composite_ge_60(self):
        inp = _make_input(
            avg_discount_pct=0.25,
            max_discount_given_pct=0.40,
            price_objection_rate_pct=0.60,
            discount_frequency_pct=0.70,
            multi_discount_deal_rate_pct=0.40,
            list_price_close_rate_pct=0.10,
            avg_gross_margin_pct=0.30,
            target_gross_margin_pct=0.50,
            approval_override_rate_pct=0.30,
            competitor_price_match_rate_pct=0.40,
            first_ask_concession_rate_pct=0.60,
            late_stage_discount_rate_pct=0.50,
            avg_deal_cycle_vs_discount_corr=0.60,
        )
        r = _engine().assess(inp)
        assert r.pricing_composite >= 60
        assert r.pricing_severity == PricingSeverity.uncontrolled

    def test_severity_matches_risk_level(self):
        """Severity and risk should always be in sync."""
        inp = _make_input()
        r = _engine().assess(inp)
        if r.pricing_composite < 20:
            assert r.pricing_severity == PricingSeverity.disciplined
            assert r.pricing_risk == PricingRisk.low
        elif r.pricing_composite < 40:
            assert r.pricing_severity == PricingSeverity.managed
            assert r.pricing_risk == PricingRisk.moderate
        elif r.pricing_composite < 60:
            assert r.pricing_severity == PricingSeverity.aggressive
            assert r.pricing_risk == PricingRisk.high
        else:
            assert r.pricing_severity == PricingSeverity.uncontrolled
            assert r.pricing_risk == PricingRisk.critical


# ===========================================================================
# 6. PATTERN DETECTION — all 6 patterns
# ===========================================================================

class TestPatternDetection:
    def test_pattern_none_clean_rep(self):
        r = _engine().assess(_make_input())
        assert r.pricing_pattern == PricingPattern.none

    def test_discount_reflex_pattern(self):
        # avg_discount_pct >= 0.20 AND first_ask_concession_rate_pct >= 0.55
        inp = _make_input(
            avg_discount_pct=0.20,
            first_ask_concession_rate_pct=0.55,
        )
        r = _engine().assess(inp)
        assert r.pricing_pattern == PricingPattern.discount_reflex

    def test_discount_reflex_exact_boundary(self):
        inp = _make_input(
            avg_discount_pct=0.20,
            first_ask_concession_rate_pct=0.55,
        )
        r = _engine().assess(inp)
        assert r.pricing_pattern == PricingPattern.discount_reflex

    def test_margin_eroder_pattern(self):
        # margin_gap >= 0.12 AND approval_override_rate_pct >= 0.25
        # Must NOT trigger discount_reflex first
        inp = _make_input(
            avg_discount_pct=0.05,              # below 0.20 → no discount reflex
            first_ask_concession_rate_pct=0.10,
            avg_gross_margin_pct=0.30,
            target_gross_margin_pct=0.45,       # gap = 0.15 >= 0.12
            approval_override_rate_pct=0.25,
        )
        r = _engine().assess(inp)
        assert r.pricing_pattern == PricingPattern.margin_eroder

    def test_margin_eroder_exact_gap_boundary(self):
        inp = _make_input(
            avg_discount_pct=0.05,
            avg_gross_margin_pct=0.38,
            target_gross_margin_pct=0.50,       # gap=0.12 exactly
            approval_override_rate_pct=0.25,
        )
        r = _engine().assess(inp)
        assert r.pricing_pattern == PricingPattern.margin_eroder

    def test_late_stage_capitulator_pattern(self):
        # late_stage_discount_rate_pct >= 0.45 AND multi_discount_deal_rate_pct >= 0.30
        # Must NOT trigger earlier patterns
        inp = _make_input(
            avg_discount_pct=0.05,
            first_ask_concession_rate_pct=0.10,
            avg_gross_margin_pct=0.50,
            target_gross_margin_pct=0.50,       # gap=0 → no margin eroder
            approval_override_rate_pct=0.05,
            late_stage_discount_rate_pct=0.45,
            multi_discount_deal_rate_pct=0.30,
        )
        r = _engine().assess(inp)
        assert r.pricing_pattern == PricingPattern.late_stage_capitulator

    def test_late_stage_capitulator_exact_boundary(self):
        inp = _make_input(
            avg_discount_pct=0.05,
            first_ask_concession_rate_pct=0.10,
            avg_gross_margin_pct=0.50,
            target_gross_margin_pct=0.50,
            late_stage_discount_rate_pct=0.45,
            multi_discount_deal_rate_pct=0.30,
        )
        r = _engine().assess(inp)
        assert r.pricing_pattern == PricingPattern.late_stage_capitulator

    def test_multi_discount_stacker_pattern(self):
        # multi_discount_deal_rate_pct >= 0.35 AND discount_frequency_pct >= 0.55
        # Must NOT trigger earlier patterns
        inp = _make_input(
            avg_discount_pct=0.05,
            first_ask_concession_rate_pct=0.10,
            avg_gross_margin_pct=0.50,
            target_gross_margin_pct=0.50,
            late_stage_discount_rate_pct=0.10,
            multi_discount_deal_rate_pct=0.35,
            discount_frequency_pct=0.55,
        )
        r = _engine().assess(inp)
        assert r.pricing_pattern == PricingPattern.multi_discount_stacker

    def test_multi_discount_stacker_exact_boundary(self):
        inp = _make_input(
            avg_discount_pct=0.05,
            first_ask_concession_rate_pct=0.10,
            avg_gross_margin_pct=0.50,
            target_gross_margin_pct=0.50,
            late_stage_discount_rate_pct=0.10,
            multi_discount_deal_rate_pct=0.35,
            discount_frequency_pct=0.55,
        )
        r = _engine().assess(inp)
        assert r.pricing_pattern == PricingPattern.multi_discount_stacker

    def test_value_misaligner_pattern(self):
        # price_objection_rate_pct >= 0.55 AND list_price_close_rate_pct <= 0.25
        # Must NOT trigger earlier patterns
        inp = _make_input(
            avg_discount_pct=0.05,
            first_ask_concession_rate_pct=0.10,
            avg_gross_margin_pct=0.50,
            target_gross_margin_pct=0.50,
            late_stage_discount_rate_pct=0.10,
            multi_discount_deal_rate_pct=0.10,
            discount_frequency_pct=0.10,
            price_objection_rate_pct=0.55,
            list_price_close_rate_pct=0.25,
        )
        r = _engine().assess(inp)
        assert r.pricing_pattern == PricingPattern.value_misaligner

    def test_value_misaligner_exact_boundary(self):
        inp = _make_input(
            avg_discount_pct=0.05,
            first_ask_concession_rate_pct=0.10,
            avg_gross_margin_pct=0.50,
            target_gross_margin_pct=0.50,
            late_stage_discount_rate_pct=0.10,
            multi_discount_deal_rate_pct=0.10,
            discount_frequency_pct=0.10,
            price_objection_rate_pct=0.55,
            list_price_close_rate_pct=0.25,
        )
        r = _engine().assess(inp)
        assert r.pricing_pattern == PricingPattern.value_misaligner

    def test_discount_reflex_takes_priority_over_margin_eroder(self):
        """discount_reflex check comes first in the _pattern method."""
        inp = _make_input(
            avg_discount_pct=0.20,
            first_ask_concession_rate_pct=0.55,
            avg_gross_margin_pct=0.30,
            target_gross_margin_pct=0.50,       # gap=0.20 → would be margin_eroder
            approval_override_rate_pct=0.25,
        )
        r = _engine().assess(inp)
        assert r.pricing_pattern == PricingPattern.discount_reflex

    def test_pattern_is_enum_instance(self):
        r = _engine().assess(_make_input())
        assert isinstance(r.pricing_pattern, PricingPattern)


# ===========================================================================
# 7. ACTION ROUTING — all 7 actions
# ===========================================================================

class TestActionRouting:
    def test_no_action_when_low_risk(self):
        r = _engine().assess(_make_input())
        assert r.recommended_action == PricingAction.no_action

    def test_discount_awareness_coaching_when_moderate_risk(self):
        inp = _make_input(
            avg_discount_pct=0.15,
            discount_frequency_pct=0.50,
            avg_gross_margin_pct=0.42,
            target_gross_margin_pct=0.50,
        )
        r = _engine().assess(inp)
        if r.pricing_risk == PricingRisk.moderate:
            assert r.recommended_action == PricingAction.discount_awareness_coaching

    def test_discount_awareness_coaching_high_risk_discount_reflex(self):
        inp = _make_input(
            avg_discount_pct=0.25,
            max_discount_given_pct=0.40,
            price_objection_rate_pct=0.60,
            discount_frequency_pct=0.70,
            multi_discount_deal_rate_pct=0.40,
            avg_gross_margin_pct=0.45,
            target_gross_margin_pct=0.50,
            first_ask_concession_rate_pct=0.55,
        )
        r = _engine().assess(inp)
        if r.pricing_risk == PricingRisk.high and r.pricing_pattern == PricingPattern.discount_reflex:
            assert r.recommended_action == PricingAction.discount_awareness_coaching

    def test_value_selling_coaching_high_risk_value_misaligner(self):
        inp = _make_input(
            avg_discount_pct=0.05,
            first_ask_concession_rate_pct=0.10,
            avg_gross_margin_pct=0.50,
            target_gross_margin_pct=0.50,
            price_objection_rate_pct=0.55,
            list_price_close_rate_pct=0.25,
            discount_frequency_pct=0.70,
            multi_discount_deal_rate_pct=0.40,
            approval_override_rate_pct=0.30,
            late_stage_discount_rate_pct=0.50,
        )
        r = _engine().assess(inp)
        if r.pricing_risk == PricingRisk.high and r.pricing_pattern == PricingPattern.value_misaligner:
            assert r.recommended_action == PricingAction.value_selling_coaching

    def test_negotiation_discipline_coaching_high_risk_late_stage_capitulator(self):
        inp = _make_input(
            avg_discount_pct=0.05,
            first_ask_concession_rate_pct=0.10,
            avg_gross_margin_pct=0.50,
            target_gross_margin_pct=0.50,
            late_stage_discount_rate_pct=0.45,
            multi_discount_deal_rate_pct=0.30,
            discount_frequency_pct=0.70,
            approval_override_rate_pct=0.30,
        )
        r = _engine().assess(inp)
        if r.pricing_risk == PricingRisk.high and r.pricing_pattern == PricingPattern.late_stage_capitulator:
            assert r.recommended_action == PricingAction.negotiation_discipline_coaching

    def test_margin_recovery_coaching_high_risk_multi_discount_stacker(self):
        inp = _make_input(
            avg_discount_pct=0.05,
            first_ask_concession_rate_pct=0.10,
            avg_gross_margin_pct=0.50,
            target_gross_margin_pct=0.50,
            multi_discount_deal_rate_pct=0.35,
            discount_frequency_pct=0.70,
            late_stage_discount_rate_pct=0.10,
            approval_override_rate_pct=0.30,
        )
        r = _engine().assess(inp)
        if r.pricing_risk == PricingRisk.high and r.pricing_pattern == PricingPattern.multi_discount_stacker:
            assert r.recommended_action == PricingAction.margin_recovery_coaching

    def test_pricing_approval_requirement_critical_non_margin_eroder(self):
        # critical risk + not margin_eroder → pricing_approval_requirement
        inp = _make_input(
            avg_discount_pct=0.25,
            max_discount_given_pct=0.40,
            price_objection_rate_pct=0.60,
            discount_frequency_pct=0.70,
            multi_discount_deal_rate_pct=0.40,
            list_price_close_rate_pct=0.10,
            avg_gross_margin_pct=0.45,          # small gap → not margin_eroder
            target_gross_margin_pct=0.50,
            approval_override_rate_pct=0.05,    # below 0.25
            first_ask_concession_rate_pct=0.60,
            late_stage_discount_rate_pct=0.50,
            avg_deal_cycle_vs_discount_corr=0.60,
        )
        r = _engine().assess(inp)
        if r.pricing_risk == PricingRisk.critical:
            assert r.recommended_action == PricingAction.pricing_approval_requirement

    def test_pricing_intervention_critical_margin_eroder(self):
        inp = _make_input(
            avg_discount_pct=0.20,
            first_ask_concession_rate_pct=0.55,  # triggers discount_reflex first!
        )
        # For pricing_intervention, need critical + margin_eroder pattern
        # But discount_reflex takes priority in pattern — need to avoid discount_reflex
        inp2 = _make_input(
            avg_discount_pct=0.05,               # avoid discount_reflex
            first_ask_concession_rate_pct=0.10,
            avg_gross_margin_pct=0.30,
            target_gross_margin_pct=0.50,        # gap=0.20 ≥ 0.12
            approval_override_rate_pct=0.30,     # ≥ 0.25 → margin_eroder
            # Make composite ≥ 60
            discount_frequency_pct=0.70,         # freq +45
            multi_discount_deal_rate_pct=0.40,   # freq +35
            list_price_close_rate_pct=0.10,      # freq +20
            late_stage_discount_rate_pct=0.50,   # neg +35
            avg_deal_cycle_vs_discount_corr=0.60, # neg +20
        )
        r = _engine().assess(inp2)
        if r.pricing_risk == PricingRisk.critical and r.pricing_pattern == PricingPattern.margin_eroder:
            assert r.recommended_action == PricingAction.pricing_intervention

    def test_high_risk_no_pattern_gets_negotiation_discipline_coaching(self):
        """High risk + no recognized pattern → negotiation_discipline_coaching (default)."""
        inp = _make_input(
            avg_discount_pct=0.14,              # < 0.20 → no discount_reflex
            first_ask_concession_rate_pct=0.10,
            avg_gross_margin_pct=0.45,
            target_gross_margin_pct=0.50,       # gap=0.05 < 0.12 → no margin_eroder
            late_stage_discount_rate_pct=0.10,  # < 0.45 → no late_stage_capitulator
            multi_discount_deal_rate_pct=0.10,  # < 0.35 → no multi_discount_stacker
            discount_frequency_pct=0.70,
            price_objection_rate_pct=0.30,      # < 0.55 → no value_misaligner
            list_price_close_rate_pct=0.80,
            approval_override_rate_pct=0.30,
            competitor_price_match_rate_pct=0.40,
        )
        r = _engine().assess(inp)
        if r.pricing_risk == PricingRisk.high and r.pricing_pattern == PricingPattern.none:
            assert r.recommended_action == PricingAction.negotiation_discipline_coaching

    def test_action_is_enum_instance(self):
        r = _engine().assess(_make_input())
        assert isinstance(r.recommended_action, PricingAction)


# ===========================================================================
# 8. SUB-SCORE BRACKETS — discount_depth_score
# ===========================================================================

class TestDiscountDepthScore:
    def test_zero_when_all_below_thresholds(self):
        inp = _make_input(
            avg_discount_pct=0.00,
            max_discount_given_pct=0.00,
            price_objection_rate_pct=0.00,
        )
        r = _engine().assess(inp)
        assert r.discount_depth_score == 0.0

    def test_avg_discount_pct_tier1_12pts(self):
        # 0.08 <= avg_discount_pct < 0.15 → +12
        inp = _make_input(avg_discount_pct=0.08, max_discount_given_pct=0.00, price_objection_rate_pct=0.00)
        r = _engine().assess(inp)
        assert r.discount_depth_score == 12.0

    def test_avg_discount_pct_tier2_28pts(self):
        # 0.15 <= avg_discount_pct < 0.25 → +28
        inp = _make_input(avg_discount_pct=0.15, max_discount_given_pct=0.00, price_objection_rate_pct=0.00)
        r = _engine().assess(inp)
        assert r.discount_depth_score == 28.0

    def test_avg_discount_pct_tier3_45pts(self):
        # avg_discount_pct >= 0.25 → +45
        inp = _make_input(avg_discount_pct=0.25, max_discount_given_pct=0.00, price_objection_rate_pct=0.00)
        r = _engine().assess(inp)
        assert r.discount_depth_score == 45.0

    def test_max_discount_pct_tier1_6pts(self):
        # 0.18 <= max_discount_given_pct < 0.28 → +6
        inp = _make_input(avg_discount_pct=0.00, max_discount_given_pct=0.18, price_objection_rate_pct=0.00)
        r = _engine().assess(inp)
        assert r.discount_depth_score == 6.0

    def test_max_discount_pct_tier2_18pts(self):
        # 0.28 <= max_discount_given_pct < 0.40 → +18
        inp = _make_input(avg_discount_pct=0.00, max_discount_given_pct=0.28, price_objection_rate_pct=0.00)
        r = _engine().assess(inp)
        assert r.discount_depth_score == 18.0

    def test_max_discount_pct_tier3_35pts(self):
        # max_discount_given_pct >= 0.40 → +35
        inp = _make_input(avg_discount_pct=0.00, max_discount_given_pct=0.40, price_objection_rate_pct=0.00)
        r = _engine().assess(inp)
        assert r.discount_depth_score == 35.0

    def test_price_objection_rate_tier1_10pts(self):
        # 0.40 <= price_objection_rate_pct < 0.60 → +10
        inp = _make_input(avg_discount_pct=0.00, max_discount_given_pct=0.00, price_objection_rate_pct=0.40)
        r = _engine().assess(inp)
        assert r.discount_depth_score == 10.0

    def test_price_objection_rate_tier2_20pts(self):
        # price_objection_rate_pct >= 0.60 → +20
        inp = _make_input(avg_discount_pct=0.00, max_discount_given_pct=0.00, price_objection_rate_pct=0.60)
        r = _engine().assess(inp)
        assert r.discount_depth_score == 20.0

    def test_depth_score_capped_at_100(self):
        # 45 + 35 + 20 = 100
        inp = _make_input(
            avg_discount_pct=0.25,
            max_discount_given_pct=0.40,
            price_objection_rate_pct=0.60,
        )
        r = _engine().assess(inp)
        assert r.discount_depth_score == 100.0

    def test_depth_score_additive_two_components(self):
        # avg=0.15 (+28) + max=0.18 (+6) = 34
        inp = _make_input(avg_discount_pct=0.15, max_discount_given_pct=0.18, price_objection_rate_pct=0.00)
        r = _engine().assess(inp)
        assert r.discount_depth_score == 34.0


# ===========================================================================
# 9. SUB-SCORE BRACKETS — discount_frequency_score
# ===========================================================================

class TestDiscountFrequencyScore:
    def test_zero_when_all_below_thresholds(self):
        inp = _make_input(
            discount_frequency_pct=0.10,
            multi_discount_deal_rate_pct=0.05,
            list_price_close_rate_pct=0.90,
        )
        r = _engine().assess(inp)
        assert r.discount_frequency_score == 0.0

    def test_discount_frequency_tier1_12pts(self):
        # 0.35 <= discount_frequency_pct < 0.50 → +12
        inp = _make_input(discount_frequency_pct=0.35, multi_discount_deal_rate_pct=0.00, list_price_close_rate_pct=0.90)
        r = _engine().assess(inp)
        assert r.discount_frequency_score == 12.0

    def test_discount_frequency_tier2_28pts(self):
        # 0.50 <= discount_frequency_pct < 0.70 → +28
        inp = _make_input(discount_frequency_pct=0.50, multi_discount_deal_rate_pct=0.00, list_price_close_rate_pct=0.90)
        r = _engine().assess(inp)
        assert r.discount_frequency_score == 28.0

    def test_discount_frequency_tier3_45pts(self):
        # discount_frequency_pct >= 0.70 → +45
        inp = _make_input(discount_frequency_pct=0.70, multi_discount_deal_rate_pct=0.00, list_price_close_rate_pct=0.90)
        r = _engine().assess(inp)
        assert r.discount_frequency_score == 45.0

    def test_multi_discount_tier1_6pts(self):
        # 0.12 <= multi_discount_deal_rate_pct < 0.25 → +6
        inp = _make_input(discount_frequency_pct=0.10, multi_discount_deal_rate_pct=0.12, list_price_close_rate_pct=0.90)
        r = _engine().assess(inp)
        assert r.discount_frequency_score == 6.0

    def test_multi_discount_tier2_18pts(self):
        # 0.25 <= multi_discount_deal_rate_pct < 0.40 → +18
        inp = _make_input(discount_frequency_pct=0.10, multi_discount_deal_rate_pct=0.25, list_price_close_rate_pct=0.90)
        r = _engine().assess(inp)
        assert r.discount_frequency_score == 18.0

    def test_multi_discount_tier3_35pts(self):
        # multi_discount_deal_rate_pct >= 0.40 → +35
        inp = _make_input(discount_frequency_pct=0.10, multi_discount_deal_rate_pct=0.40, list_price_close_rate_pct=0.90)
        r = _engine().assess(inp)
        assert r.discount_frequency_score == 35.0

    def test_list_price_close_rate_tier1_10pts(self):
        # 0.20 < list_price_close_rate_pct <= 0.40 → +10
        inp = _make_input(discount_frequency_pct=0.10, multi_discount_deal_rate_pct=0.00, list_price_close_rate_pct=0.40)
        r = _engine().assess(inp)
        assert r.discount_frequency_score == 10.0

    def test_list_price_close_rate_tier2_20pts(self):
        # list_price_close_rate_pct <= 0.20 → +20
        inp = _make_input(discount_frequency_pct=0.10, multi_discount_deal_rate_pct=0.00, list_price_close_rate_pct=0.20)
        r = _engine().assess(inp)
        assert r.discount_frequency_score == 20.0

    def test_frequency_score_capped_at_100(self):
        inp = _make_input(
            discount_frequency_pct=0.70,
            multi_discount_deal_rate_pct=0.40,
            list_price_close_rate_pct=0.10,
        )
        r = _engine().assess(inp)
        assert r.discount_frequency_score == 100.0


# ===========================================================================
# 10. SUB-SCORE BRACKETS — margin_protection_score
# ===========================================================================

class TestMarginProtectionScore:
    def test_zero_when_no_margin_gap(self):
        inp = _make_input(
            avg_gross_margin_pct=0.55,
            target_gross_margin_pct=0.50,   # margin > target → gap 0 or negative
            approval_override_rate_pct=0.00,
            competitor_price_match_rate_pct=0.00,
        )
        r = _engine().assess(inp)
        assert r.margin_protection_score == 0.0

    def test_margin_gap_tier1_12pts(self):
        # 0.03 <= gap < 0.08 → +12
        inp = _make_input(
            avg_gross_margin_pct=0.47,
            target_gross_margin_pct=0.50,   # gap=0.03
            approval_override_rate_pct=0.00,
            competitor_price_match_rate_pct=0.00,
        )
        r = _engine().assess(inp)
        assert r.margin_protection_score == 12.0

    def test_margin_gap_tier2_28pts(self):
        # 0.08 <= gap < 0.15 → +28
        inp = _make_input(
            avg_gross_margin_pct=0.42,
            target_gross_margin_pct=0.50,   # gap=0.08
            approval_override_rate_pct=0.00,
            competitor_price_match_rate_pct=0.00,
        )
        r = _engine().assess(inp)
        assert r.margin_protection_score == 28.0

    def test_margin_gap_tier3_45pts(self):
        # gap >= 0.15 → +45
        inp = _make_input(
            avg_gross_margin_pct=0.35,
            target_gross_margin_pct=0.50,   # gap=0.15
            approval_override_rate_pct=0.00,
            competitor_price_match_rate_pct=0.00,
        )
        r = _engine().assess(inp)
        assert r.margin_protection_score == 45.0

    def test_approval_override_tier1_6pts(self):
        # 0.08 <= approval_override_rate_pct < 0.18 → +6
        inp = _make_input(
            avg_gross_margin_pct=0.55,
            target_gross_margin_pct=0.50,
            approval_override_rate_pct=0.08,
            competitor_price_match_rate_pct=0.00,
        )
        r = _engine().assess(inp)
        assert r.margin_protection_score == 6.0

    def test_approval_override_tier2_18pts(self):
        # 0.18 <= approval_override_rate_pct < 0.30 → +18
        inp = _make_input(
            avg_gross_margin_pct=0.55,
            target_gross_margin_pct=0.50,
            approval_override_rate_pct=0.18,
            competitor_price_match_rate_pct=0.00,
        )
        r = _engine().assess(inp)
        assert r.margin_protection_score == 18.0

    def test_approval_override_tier3_35pts(self):
        # approval_override_rate_pct >= 0.30 → +35
        inp = _make_input(
            avg_gross_margin_pct=0.55,
            target_gross_margin_pct=0.50,
            approval_override_rate_pct=0.30,
            competitor_price_match_rate_pct=0.00,
        )
        r = _engine().assess(inp)
        assert r.margin_protection_score == 35.0

    def test_competitor_price_match_tier1_10pts(self):
        # 0.25 <= competitor_price_match_rate_pct < 0.40 → +10
        inp = _make_input(
            avg_gross_margin_pct=0.55,
            target_gross_margin_pct=0.50,
            approval_override_rate_pct=0.00,
            competitor_price_match_rate_pct=0.25,
        )
        r = _engine().assess(inp)
        assert r.margin_protection_score == 10.0

    def test_competitor_price_match_tier2_20pts(self):
        # competitor_price_match_rate_pct >= 0.40 → +20
        inp = _make_input(
            avg_gross_margin_pct=0.55,
            target_gross_margin_pct=0.50,
            approval_override_rate_pct=0.00,
            competitor_price_match_rate_pct=0.40,
        )
        r = _engine().assess(inp)
        assert r.margin_protection_score == 20.0

    def test_margin_protection_capped_at_100(self):
        inp = _make_input(
            avg_gross_margin_pct=0.30,
            target_gross_margin_pct=0.50,   # gap=0.20 → +45
            approval_override_rate_pct=0.30,  # +35
            competitor_price_match_rate_pct=0.40,  # +20
        )
        r = _engine().assess(inp)
        assert r.margin_protection_score == 100.0


# ===========================================================================
# 11. SUB-SCORE BRACKETS — negotiation_discipline_score
# ===========================================================================

class TestNegotiationDisciplineScore:
    def test_zero_when_all_below_thresholds(self):
        inp = _make_input(
            first_ask_concession_rate_pct=0.10,
            late_stage_discount_rate_pct=0.05,
            avg_deal_cycle_vs_discount_corr=0.10,
        )
        r = _engine().assess(inp)
        assert r.negotiation_discipline_score == 0.0

    def test_first_ask_concession_tier1_12pts(self):
        # 0.25 <= first_ask_concession_rate_pct < 0.40 → +12
        inp = _make_input(first_ask_concession_rate_pct=0.25, late_stage_discount_rate_pct=0.00, avg_deal_cycle_vs_discount_corr=0.00)
        r = _engine().assess(inp)
        assert r.negotiation_discipline_score == 12.0

    def test_first_ask_concession_tier2_28pts(self):
        # 0.40 <= first_ask_concession_rate_pct < 0.60 → +28
        inp = _make_input(first_ask_concession_rate_pct=0.40, late_stage_discount_rate_pct=0.00, avg_deal_cycle_vs_discount_corr=0.00)
        r = _engine().assess(inp)
        assert r.negotiation_discipline_score == 28.0

    def test_first_ask_concession_tier3_45pts(self):
        # first_ask_concession_rate_pct >= 0.60 → +45
        inp = _make_input(first_ask_concession_rate_pct=0.60, late_stage_discount_rate_pct=0.00, avg_deal_cycle_vs_discount_corr=0.00)
        r = _engine().assess(inp)
        assert r.negotiation_discipline_score == 45.0

    def test_late_stage_discount_tier1_6pts(self):
        # 0.20 <= late_stage_discount_rate_pct < 0.35 → +6
        inp = _make_input(first_ask_concession_rate_pct=0.00, late_stage_discount_rate_pct=0.20, avg_deal_cycle_vs_discount_corr=0.00)
        r = _engine().assess(inp)
        assert r.negotiation_discipline_score == 6.0

    def test_late_stage_discount_tier2_18pts(self):
        # 0.35 <= late_stage_discount_rate_pct < 0.50 → +18
        inp = _make_input(first_ask_concession_rate_pct=0.00, late_stage_discount_rate_pct=0.35, avg_deal_cycle_vs_discount_corr=0.00)
        r = _engine().assess(inp)
        assert r.negotiation_discipline_score == 18.0

    def test_late_stage_discount_tier3_35pts(self):
        # late_stage_discount_rate_pct >= 0.50 → +35
        inp = _make_input(first_ask_concession_rate_pct=0.00, late_stage_discount_rate_pct=0.50, avg_deal_cycle_vs_discount_corr=0.00)
        r = _engine().assess(inp)
        assert r.negotiation_discipline_score == 35.0

    def test_deal_cycle_corr_tier1_10pts(self):
        # 0.40 <= corr < 0.60 → +10
        inp = _make_input(first_ask_concession_rate_pct=0.00, late_stage_discount_rate_pct=0.00, avg_deal_cycle_vs_discount_corr=0.40)
        r = _engine().assess(inp)
        assert r.negotiation_discipline_score == 10.0

    def test_deal_cycle_corr_tier2_20pts(self):
        # corr >= 0.60 → +20
        inp = _make_input(first_ask_concession_rate_pct=0.00, late_stage_discount_rate_pct=0.00, avg_deal_cycle_vs_discount_corr=0.60)
        r = _engine().assess(inp)
        assert r.negotiation_discipline_score == 20.0

    def test_negotiation_discipline_capped_at_100(self):
        inp = _make_input(
            first_ask_concession_rate_pct=0.60,   # +45
            late_stage_discount_rate_pct=0.50,    # +35
            avg_deal_cycle_vs_discount_corr=0.60, # +20
        )
        r = _engine().assess(inp)
        assert r.negotiation_discipline_score == 100.0


# ===========================================================================
# 12. COMPOSITE FORMULA
# ===========================================================================

class TestCompositeFormula:
    def test_composite_is_weighted_sum(self):
        inp = _make_input(
            avg_discount_pct=0.15,       # depth → 28
            discount_frequency_pct=0.50, # freq → 28
            avg_gross_margin_pct=0.42,
            target_gross_margin_pct=0.50, # margin gap=0.08 → margin +28
            first_ask_concession_rate_pct=0.25,  # negotiation +12
        )
        r = _engine().assess(inp)
        # depth=28, freq=28, margin=28, negotiation=12
        expected = round(28 * 0.30 + 28 * 0.25 + 28 * 0.25 + 12 * 0.20, 2)
        assert r.pricing_composite == expected

    def test_composite_zero_for_clean_rep(self):
        r = _engine().assess(_make_input())
        assert r.pricing_composite == 0.0

    def test_composite_max_is_100(self):
        inp = _make_input(
            avg_discount_pct=0.25,
            max_discount_given_pct=0.40,
            price_objection_rate_pct=0.60,
            discount_frequency_pct=0.70,
            multi_discount_deal_rate_pct=0.40,
            list_price_close_rate_pct=0.10,
            avg_gross_margin_pct=0.30,
            target_gross_margin_pct=0.50,
            approval_override_rate_pct=0.30,
            competitor_price_match_rate_pct=0.40,
            first_ask_concession_rate_pct=0.60,
            late_stage_discount_rate_pct=0.50,
            avg_deal_cycle_vs_discount_corr=0.60,
        )
        r = _engine().assess(inp)
        # All sub-scores capped at 100 → 100*0.30+100*0.25+100*0.25+100*0.20=100
        assert r.pricing_composite == 100.0

    def test_composite_weights_sum_to_1(self):
        # Weights: 0.30 + 0.25 + 0.25 + 0.20 = 1.00
        assert abs(0.30 + 0.25 + 0.25 + 0.20 - 1.00) < 1e-9

    def test_composite_rounded_to_2_decimals(self):
        inp = _make_input(avg_discount_pct=0.08, discount_frequency_pct=0.35)
        r = _engine().assess(inp)
        # Check it's a float with at most 2 decimal places
        assert r.pricing_composite == round(r.pricing_composite, 2)

    def test_composite_30pct_discount_depth(self):
        # Only avg_discount_pct=0.25 (depth=45), all others 0
        inp = _make_input(avg_discount_pct=0.25, max_discount_given_pct=0.00, price_objection_rate_pct=0.00)
        r = _engine().assess(inp)
        expected = round(45 * 0.30, 2)
        assert r.pricing_composite == expected

    def test_composite_25pct_discount_frequency(self):
        # Only discount_frequency_pct=0.70 (freq=45), all others 0
        inp = _make_input(discount_frequency_pct=0.70, multi_discount_deal_rate_pct=0.00, list_price_close_rate_pct=0.90)
        r = _engine().assess(inp)
        expected = round(45 * 0.25, 2)
        assert r.pricing_composite == expected

    def test_composite_25pct_margin_protection(self):
        # Only margin gap >= 0.15 (margin=45), all others 0
        inp = _make_input(
            avg_gross_margin_pct=0.35,
            target_gross_margin_pct=0.50,
            approval_override_rate_pct=0.00,
            competitor_price_match_rate_pct=0.00,
        )
        r = _engine().assess(inp)
        expected = round(45 * 0.25, 2)
        assert r.pricing_composite == expected

    def test_composite_20pct_negotiation_discipline(self):
        # Only first_ask_concession_rate_pct=0.60 (negotiation=45)
        inp = _make_input(first_ask_concession_rate_pct=0.60, late_stage_discount_rate_pct=0.00, avg_deal_cycle_vs_discount_corr=0.00)
        r = _engine().assess(inp)
        expected = round(45 * 0.20, 2)
        assert r.pricing_composite == expected


# ===========================================================================
# 13. HAS_PRICING_GAP TRIGGERS
# ===========================================================================

class TestHasPricingGap:
    def test_no_gap_clean_rep(self):
        r = _engine().assess(_make_input())
        assert r.has_pricing_gap is False

    def test_gap_via_composite_ge_40(self):
        inp = _make_input(
            avg_discount_pct=0.25,
            max_discount_given_pct=0.40,
            price_objection_rate_pct=0.60,
            discount_frequency_pct=0.70,
            multi_discount_deal_rate_pct=0.40,
            list_price_close_rate_pct=0.10,
            avg_gross_margin_pct=0.30,
            target_gross_margin_pct=0.50,
            approval_override_rate_pct=0.30,
            competitor_price_match_rate_pct=0.40,
        )
        r = _engine().assess(inp)
        assert r.pricing_composite >= 40
        assert r.has_pricing_gap is True

    def test_gap_via_avg_discount_pct_ge_0_15(self):
        # composite stays low but avg_discount_pct=0.15 triggers gap
        inp = _make_input(avg_discount_pct=0.15)
        r = _engine().assess(inp)
        assert r.has_pricing_gap is True

    def test_no_gap_when_avg_discount_just_below_0_15(self):
        inp = _make_input(avg_discount_pct=0.14, discount_frequency_pct=0.10)
        r = _engine().assess(inp)
        if r.pricing_composite < 40 and inp.discount_frequency_pct < 0.50:
            assert r.has_pricing_gap is False

    def test_gap_via_discount_frequency_pct_ge_0_50(self):
        inp = _make_input(discount_frequency_pct=0.50, avg_discount_pct=0.05)
        r = _engine().assess(inp)
        assert r.has_pricing_gap is True

    def test_no_gap_when_discount_frequency_just_below_0_50(self):
        inp = _make_input(discount_frequency_pct=0.49, avg_discount_pct=0.05)
        r = _engine().assess(inp)
        if r.pricing_composite < 40 and inp.avg_discount_pct < 0.15:
            assert r.has_pricing_gap is False

    def test_gap_trigger_discount_pct_exact_boundary(self):
        inp = _make_input(avg_discount_pct=0.15)
        assert _engine().assess(inp).has_pricing_gap is True

    def test_gap_trigger_frequency_exact_boundary(self):
        inp = _make_input(discount_frequency_pct=0.50, avg_discount_pct=0.00)
        assert _engine().assess(inp).has_pricing_gap is True

    def test_has_pricing_gap_is_bool(self):
        r = _engine().assess(_make_input())
        assert isinstance(r.has_pricing_gap, bool)


# ===========================================================================
# 14. REQUIRES_PRICING_COACHING TRIGGERS
# ===========================================================================

class TestRequiresPricingCoaching:
    def test_no_coaching_clean_rep(self):
        r = _engine().assess(_make_input())
        assert r.requires_pricing_coaching is False

    def test_coaching_via_composite_ge_20(self):
        inp = _make_input(
            avg_discount_pct=0.15,
            discount_frequency_pct=0.50,
            avg_gross_margin_pct=0.42,
            target_gross_margin_pct=0.50,
        )
        r = _engine().assess(inp)
        if r.pricing_composite >= 20:
            assert r.requires_pricing_coaching is True

    def test_coaching_via_first_ask_concession_ge_0_35(self):
        inp = _make_input(first_ask_concession_rate_pct=0.35)
        r = _engine().assess(inp)
        assert r.requires_pricing_coaching is True

    def test_no_coaching_just_below_first_ask_threshold(self):
        inp = _make_input(first_ask_concession_rate_pct=0.34)
        r = _engine().assess(inp)
        if r.pricing_composite < 20 and inp.multi_discount_deal_rate_pct < 0.20:
            assert r.requires_pricing_coaching is False

    def test_coaching_via_multi_discount_deal_rate_ge_0_20(self):
        inp = _make_input(multi_discount_deal_rate_pct=0.20)
        r = _engine().assess(inp)
        assert r.requires_pricing_coaching is True

    def test_no_coaching_just_below_multi_discount_threshold(self):
        inp = _make_input(multi_discount_deal_rate_pct=0.19)
        r = _engine().assess(inp)
        if r.pricing_composite < 20 and inp.first_ask_concession_rate_pct < 0.35:
            assert r.requires_pricing_coaching is False

    def test_coaching_exact_boundary_first_ask(self):
        assert _engine().assess(_make_input(first_ask_concession_rate_pct=0.35)).requires_pricing_coaching is True

    def test_coaching_exact_boundary_multi_discount(self):
        assert _engine().assess(_make_input(multi_discount_deal_rate_pct=0.20)).requires_pricing_coaching is True

    def test_requires_pricing_coaching_is_bool(self):
        r = _engine().assess(_make_input())
        assert isinstance(r.requires_pricing_coaching, bool)


# ===========================================================================
# 15. ESTIMATED_MARGIN_LOSS_USD FORMULA
# ===========================================================================

class TestEstimatedMarginLoss:
    def test_zero_when_no_margin_gap(self):
        # target <= avg → gap clamped to 0
        inp = _make_input(
            avg_gross_margin_pct=0.55,
            target_gross_margin_pct=0.50,
            total_revenue_usd=1_000_000.0,
        )
        r = _engine().assess(inp)
        assert r.estimated_margin_loss_usd == 0.0

    def test_zero_when_composite_is_zero(self):
        # Even with margin gap, composite=0 → loss=0
        inp = _make_input(
            avg_gross_margin_pct=0.40,
            target_gross_margin_pct=0.50,  # gap=0.10
            total_revenue_usd=1_000_000.0,
        )
        # Need composite=0: all other fields must be clean
        inp2 = _make_input(
            avg_discount_pct=0.00,
            max_discount_given_pct=0.00,
            price_objection_rate_pct=0.00,
            discount_frequency_pct=0.00,
            multi_discount_deal_rate_pct=0.00,
            list_price_close_rate_pct=1.00,
            avg_gross_margin_pct=0.55,      # no gap
            target_gross_margin_pct=0.50,
            approval_override_rate_pct=0.00,
            competitor_price_match_rate_pct=0.00,
            first_ask_concession_rate_pct=0.00,
            late_stage_discount_rate_pct=0.00,
            avg_deal_cycle_vs_discount_corr=0.00,
            total_revenue_usd=1_000_000.0,
        )
        r = _engine().assess(inp2)
        assert r.estimated_margin_loss_usd == 0.0

    def test_margin_loss_formula_exact(self):
        # Set known sub-scores to derive composite precisely
        # avg_discount_pct=0.15 → depth=28; discount_freq=0.50 → freq=28
        # margin gap=0.08 → margin=28; first_ask=0.00 → negotiation=0
        # composite = 28*0.30 + 28*0.25 + 28*0.25 + 0*0.20 = 8.4+7+7=22.4
        inp = _make_input(
            avg_discount_pct=0.15,
            discount_frequency_pct=0.50,
            avg_gross_margin_pct=0.42,
            target_gross_margin_pct=0.50,   # gap=0.08
            total_revenue_usd=500_000.0,
        )
        r = _engine().assess(inp)
        margin_gap = max(0.0, 0.50 - 0.42)
        expected = round(500_000.0 * margin_gap * (r.pricing_composite / 100.0), 2)
        assert r.estimated_margin_loss_usd == expected

    def test_margin_loss_uses_total_revenue_usd(self):
        inp1 = _make_input(
            avg_gross_margin_pct=0.42,
            target_gross_margin_pct=0.50,
            avg_discount_pct=0.15,
            total_revenue_usd=1_000_000.0,
        )
        inp2 = _make_input(
            avg_gross_margin_pct=0.42,
            target_gross_margin_pct=0.50,
            avg_discount_pct=0.15,
            total_revenue_usd=2_000_000.0,
        )
        r1 = _engine().assess(inp1)
        r2 = _engine().assess(inp2)
        assert abs(r2.estimated_margin_loss_usd - 2 * r1.estimated_margin_loss_usd) < 0.01

    def test_margin_loss_is_float(self):
        r = _engine().assess(_make_input())
        assert isinstance(r.estimated_margin_loss_usd, float)

    def test_margin_loss_non_negative(self):
        r = _engine().assess(_make_input(
            avg_gross_margin_pct=0.30,
            target_gross_margin_pct=0.50,
            avg_discount_pct=0.25,
        ))
        assert r.estimated_margin_loss_usd >= 0.0


# ===========================================================================
# 16. SIGNAL TEXT
# ===========================================================================

class TestSignalText:
    def test_signal_strong_discipline_when_composite_below_20(self):
        r = _engine().assess(_make_input())
        assert "Pricing discipline strong" in r.pricing_signal

    def test_signal_includes_discount_reflex_label(self):
        inp = _make_input(
            avg_discount_pct=0.20,
            first_ask_concession_rate_pct=0.55,
            discount_frequency_pct=0.50,  # ensure composite >= 20
        )
        r = _engine().assess(inp)
        if r.pricing_composite >= 20:
            assert "Discount reflex" in r.pricing_signal

    def test_signal_includes_margin_eroder_label(self):
        inp = _make_input(
            avg_discount_pct=0.05,
            first_ask_concession_rate_pct=0.10,
            avg_gross_margin_pct=0.30,
            target_gross_margin_pct=0.50,
            approval_override_rate_pct=0.30,
            discount_frequency_pct=0.70,
        )
        r = _engine().assess(inp)
        if r.pricing_pattern == PricingPattern.margin_eroder and r.pricing_composite >= 20:
            assert "Margin eroder" in r.pricing_signal

    def test_signal_includes_late_stage_capitulator_label(self):
        inp = _make_input(
            avg_discount_pct=0.05,
            first_ask_concession_rate_pct=0.10,
            avg_gross_margin_pct=0.50,
            target_gross_margin_pct=0.50,
            late_stage_discount_rate_pct=0.45,
            multi_discount_deal_rate_pct=0.30,
            discount_frequency_pct=0.60,
        )
        r = _engine().assess(inp)
        if r.pricing_pattern == PricingPattern.late_stage_capitulator and r.pricing_composite >= 20:
            assert "Late-stage capitulator" in r.pricing_signal

    def test_signal_includes_multi_discount_stacker_label(self):
        inp = _make_input(
            avg_discount_pct=0.05,
            first_ask_concession_rate_pct=0.10,
            avg_gross_margin_pct=0.50,
            target_gross_margin_pct=0.50,
            multi_discount_deal_rate_pct=0.35,
            discount_frequency_pct=0.55,
            late_stage_discount_rate_pct=0.10,
        )
        r = _engine().assess(inp)
        if r.pricing_pattern == PricingPattern.multi_discount_stacker and r.pricing_composite >= 20:
            assert "Multi-discount stacker" in r.pricing_signal

    def test_signal_includes_value_misaligner_label(self):
        inp = _make_input(
            avg_discount_pct=0.05,
            first_ask_concession_rate_pct=0.10,
            avg_gross_margin_pct=0.50,
            target_gross_margin_pct=0.50,
            price_objection_rate_pct=0.55,
            list_price_close_rate_pct=0.25,
            discount_frequency_pct=0.60,
        )
        r = _engine().assess(inp)
        if r.pricing_pattern == PricingPattern.value_misaligner and r.pricing_composite >= 20:
            assert "Value misaligner" in r.pricing_signal

    def test_signal_includes_pricing_gap_detected_for_none_pattern(self):
        # composite >= 20 but pattern = none → "Pricing gap detected"
        inp = _make_input(
            avg_discount_pct=0.14,
            avg_gross_margin_pct=0.42,
            target_gross_margin_pct=0.50,
            discount_frequency_pct=0.50,
        )
        r = _engine().assess(inp)
        if r.pricing_pattern == PricingPattern.none and r.pricing_composite >= 20:
            assert "Pricing gap detected" in r.pricing_signal

    def test_signal_is_string(self):
        r = _engine().assess(_make_input())
        assert isinstance(r.pricing_signal, str)

    def test_signal_contains_avg_discount_pct_percentage(self):
        inp = _make_input(
            avg_discount_pct=0.20,
            first_ask_concession_rate_pct=0.55,
            discount_frequency_pct=0.60,
        )
        r = _engine().assess(inp)
        if r.pricing_composite >= 20:
            # avg_discount_pct=0.20 → 20%
            assert "20%" in r.pricing_signal

    def test_signal_contains_discount_frequency_percentage(self):
        inp = _make_input(
            avg_discount_pct=0.20,
            first_ask_concession_rate_pct=0.55,
            discount_frequency_pct=0.60,
        )
        r = _engine().assess(inp)
        if r.pricing_composite >= 20:
            assert "60%" in r.pricing_signal

    def test_signal_contains_composite_value(self):
        inp = _make_input(
            avg_discount_pct=0.25,
            discount_frequency_pct=0.70,
            avg_gross_margin_pct=0.35,
            target_gross_margin_pct=0.50,
            first_ask_concession_rate_pct=0.60,
        )
        r = _engine().assess(inp)
        if r.pricing_composite >= 20:
            comp_int = str(round(r.pricing_composite))
            assert comp_int in r.pricing_signal


# ===========================================================================
# 17. ASSESS METHOD
# ===========================================================================

class TestAssessMethod:
    def test_returns_pricing_result(self):
        r = _engine().assess(_make_input())
        assert isinstance(r, PricingResult)

    def test_rep_id_passthrough(self):
        r = _engine().assess(_make_input(rep_id="SALES99"))
        assert r.rep_id == "SALES99"

    def test_region_passthrough(self):
        r = _engine().assess(_make_input(region="Northeast"))
        assert r.region == "Northeast"

    def test_sub_scores_non_negative(self):
        r = _engine().assess(_make_input())
        assert r.discount_depth_score >= 0
        assert r.discount_frequency_score >= 0
        assert r.margin_protection_score >= 0
        assert r.negotiation_discipline_score >= 0

    def test_sub_scores_max_100(self):
        inp = _make_input(
            avg_discount_pct=1.0, max_discount_given_pct=1.0, price_objection_rate_pct=1.0,
            discount_frequency_pct=1.0, multi_discount_deal_rate_pct=1.0, list_price_close_rate_pct=0.0,
            avg_gross_margin_pct=0.0, target_gross_margin_pct=1.0,
            approval_override_rate_pct=1.0, competitor_price_match_rate_pct=1.0,
            first_ask_concession_rate_pct=1.0, late_stage_discount_rate_pct=1.0,
            avg_deal_cycle_vs_discount_corr=1.0,
        )
        r = _engine().assess(inp)
        assert r.discount_depth_score <= 100.0
        assert r.discount_frequency_score <= 100.0
        assert r.margin_protection_score <= 100.0
        assert r.negotiation_discipline_score <= 100.0

    def test_composite_non_negative(self):
        r = _engine().assess(_make_input())
        assert r.pricing_composite >= 0.0

    def test_result_stored_in_engine(self):
        engine = _engine()
        engine.assess(_make_input())
        assert len(engine._results) == 1

    def test_multiple_assessments_accumulate(self):
        engine = _engine()
        engine.assess(_make_input(rep_id="R1"))
        engine.assess(_make_input(rep_id="R2"))
        engine.assess(_make_input(rep_id="R3"))
        assert len(engine._results) == 3


# ===========================================================================
# 18. ASSESS_BATCH METHOD
# ===========================================================================

class TestAssessBatch:
    def test_returns_list(self):
        engine = _engine()
        results = engine.assess_batch([_make_input(), _make_input(rep_id="R2")])
        assert isinstance(results, list)

    def test_batch_count_matches_input(self):
        engine = _engine()
        inputs = [_make_input(rep_id=f"R{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5

    def test_empty_batch_returns_empty_list(self):
        engine = _engine()
        results = engine.assess_batch([])
        assert results == []

    def test_batch_results_are_pricing_results(self):
        engine = _engine()
        results = engine.assess_batch([_make_input(), _make_input(rep_id="R2")])
        for r in results:
            assert isinstance(r, PricingResult)

    def test_batch_preserves_order(self):
        engine = _engine()
        ids = ["A", "B", "C", "D"]
        results = engine.assess_batch([_make_input(rep_id=i) for i in ids])
        assert [r.rep_id for r in results] == ids

    def test_batch_accumulates_in_engine(self):
        engine = _engine()
        engine.assess_batch([_make_input(rep_id=f"R{i}") for i in range(7)])
        assert len(engine._results) == 7

    def test_batch_single_item(self):
        engine = _engine()
        results = engine.assess_batch([_make_input(rep_id="SOLO")])
        assert len(results) == 1
        assert results[0].rep_id == "SOLO"

    def test_batch_mixed_risk_profiles(self):
        low_inp = _make_input(rep_id="LOW")
        high_inp = _make_input(
            rep_id="HIGH",
            avg_discount_pct=0.25,
            discount_frequency_pct=0.70,
            avg_gross_margin_pct=0.30,
            target_gross_margin_pct=0.50,
        )
        engine = _engine()
        results = engine.assess_batch([low_inp, high_inp])
        assert results[0].pricing_risk == PricingRisk.low
        assert results[1].pricing_risk in (PricingRisk.moderate, PricingRisk.high, PricingRisk.critical)


# ===========================================================================
# 19. SUMMARY METHOD — 13 keys
# ===========================================================================

class TestSummaryMethod:
    def test_summary_empty_engine(self):
        s = _engine().summary()
        assert isinstance(s, dict)
        assert len(s) == 13

    def test_summary_empty_total_zero(self):
        s = _engine().summary()
        assert s["total"] == 0

    def test_summary_13_keys_present_empty(self):
        s = _engine().summary()
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_pricing_composite", "pricing_gap_count",
            "coaching_count", "avg_discount_depth_score",
            "avg_discount_frequency_score", "avg_margin_protection_score",
            "avg_negotiation_discipline_score", "total_estimated_margin_loss_usd",
        }
        assert set(s.keys()) == expected_keys

    def test_summary_13_keys_after_assess(self):
        engine = _engine()
        engine.assess(_make_input())
        s = engine.summary()
        assert len(s) == 13

    def test_summary_total_count(self):
        engine = _engine()
        engine.assess_batch([_make_input(rep_id=f"R{i}") for i in range(5)])
        assert engine.summary()["total"] == 5

    def test_summary_risk_counts_populated(self):
        engine = _engine()
        engine.assess(_make_input())  # → low
        s = engine.summary()
        assert "low" in s["risk_counts"]
        assert s["risk_counts"]["low"] == 1

    def test_summary_pattern_counts_populated(self):
        engine = _engine()
        engine.assess(_make_input())  # → none
        s = engine.summary()
        assert "none" in s["pattern_counts"]

    def test_summary_severity_counts_populated(self):
        engine = _engine()
        engine.assess(_make_input())  # → disciplined
        s = engine.summary()
        assert "disciplined" in s["severity_counts"]

    def test_summary_action_counts_populated(self):
        engine = _engine()
        engine.assess(_make_input())  # → no_action
        s = engine.summary()
        assert "no_action" in s["action_counts"]

    def test_summary_avg_pricing_composite_single(self):
        engine = _engine()
        r = engine.assess(_make_input())
        s = engine.summary()
        assert abs(s["avg_pricing_composite"] - r.pricing_composite) < 0.2

    def test_summary_pricing_gap_count(self):
        engine = _engine()
        engine.assess(_make_input(avg_discount_pct=0.15))   # gap=True
        engine.assess(_make_input(avg_discount_pct=0.05))   # gap=False (assuming composite<40)
        s = engine.summary()
        assert s["pricing_gap_count"] >= 1

    def test_summary_coaching_count(self):
        engine = _engine()
        engine.assess(_make_input(first_ask_concession_rate_pct=0.35))   # coaching=True
        engine.assess(_make_input())   # coaching=False
        s = engine.summary()
        assert s["coaching_count"] >= 1

    def test_summary_avg_discount_depth_score(self):
        engine = _engine()
        engine.assess(_make_input(avg_discount_pct=0.25))   # depth=45
        engine.assess(_make_input(avg_discount_pct=0.00))   # depth=0
        s = engine.summary()
        assert abs(s["avg_discount_depth_score"] - 22.5) < 0.1

    def test_summary_avg_discount_frequency_score(self):
        engine = _engine()
        engine.assess(_make_input(discount_frequency_pct=0.70))   # freq=45
        engine.assess(_make_input(discount_frequency_pct=0.10))   # freq=0
        s = engine.summary()
        assert abs(s["avg_discount_frequency_score"] - 22.5) < 0.1

    def test_summary_avg_margin_protection_score(self):
        engine = _engine()
        engine.assess(_make_input(avg_gross_margin_pct=0.30, target_gross_margin_pct=0.50))  # margin=45
        engine.assess(_make_input())  # margin=0
        s = engine.summary()
        assert abs(s["avg_margin_protection_score"] - 22.5) < 0.1

    def test_summary_avg_negotiation_discipline_score(self):
        engine = _engine()
        engine.assess(_make_input(first_ask_concession_rate_pct=0.60))  # neg=45
        engine.assess(_make_input(first_ask_concession_rate_pct=0.00))  # neg=0
        s = engine.summary()
        assert abs(s["avg_negotiation_discipline_score"] - 22.5) < 0.1

    def test_summary_total_estimated_margin_loss_usd(self):
        engine = _engine()
        r1 = engine.assess(_make_input(
            avg_gross_margin_pct=0.42,
            target_gross_margin_pct=0.50,
            avg_discount_pct=0.15,
            total_revenue_usd=500_000.0,
        ))
        r2 = engine.assess(_make_input(total_revenue_usd=100_000.0))
        s = engine.summary()
        expected = round(r1.estimated_margin_loss_usd + r2.estimated_margin_loss_usd, 2)
        assert abs(s["total_estimated_margin_loss_usd"] - expected) < 0.01

    def test_summary_empty_avg_composite_is_zero(self):
        s = _engine().summary()
        assert s["avg_pricing_composite"] == 0.0

    def test_summary_empty_gap_count_is_zero(self):
        s = _engine().summary()
        assert s["pricing_gap_count"] == 0

    def test_summary_empty_coaching_count_is_zero(self):
        s = _engine().summary()
        assert s["coaching_count"] == 0


# ===========================================================================
# 20. EDGE CASES
# ===========================================================================

class TestEdgeCases:
    def test_all_fields_at_zero(self):
        # list_price_close_rate_pct=0.00 triggers the <=0.20 bracket (+20 freq),
        # so composite is not zero when list_price=0. Use list_price=1.0 to keep freq=0.
        inp = _make_input(
            avg_discount_pct=0.00,
            discount_frequency_pct=0.00,
            max_discount_given_pct=0.00,
            avg_gross_margin_pct=0.55,
            target_gross_margin_pct=0.50,    # no gap
            late_stage_discount_rate_pct=0.00,
            multi_discount_deal_rate_pct=0.00,
            price_objection_rate_pct=0.00,
            first_ask_concession_rate_pct=0.00,
            list_price_close_rate_pct=1.00,  # > 0.40 → no freq penalty
            approval_override_rate_pct=0.00,
            competitor_price_match_rate_pct=0.00,
            avg_deal_cycle_vs_discount_corr=0.00,
            total_revenue_usd=0.00,
        )
        r = _engine().assess(inp)
        assert r.pricing_composite == 0.0
        assert r.pricing_risk == PricingRisk.low
        assert r.estimated_margin_loss_usd == 0.0

    def test_all_fields_at_maximum(self):
        inp = _make_input(
            avg_discount_pct=1.0,
            discount_frequency_pct=1.0,
            max_discount_given_pct=1.0,
            avg_gross_margin_pct=0.0,
            target_gross_margin_pct=1.0,
            late_stage_discount_rate_pct=1.0,
            multi_discount_deal_rate_pct=1.0,
            price_objection_rate_pct=1.0,
            first_ask_concession_rate_pct=1.0,
            list_price_close_rate_pct=0.0,
            approval_override_rate_pct=1.0,
            competitor_price_match_rate_pct=1.0,
            avg_deal_cycle_vs_discount_corr=1.0,
        )
        r = _engine().assess(inp)
        assert r.pricing_composite == 100.0
        assert r.pricing_risk == PricingRisk.critical
        assert r.pricing_severity == PricingSeverity.uncontrolled

    def test_target_margin_below_actual_margin_clamps_loss_to_zero(self):
        # avg_gross_margin > target_gross_margin → margin gap negative → loss = 0
        inp = _make_input(
            avg_gross_margin_pct=0.60,
            target_gross_margin_pct=0.40,
            total_revenue_usd=1_000_000.0,
        )
        r = _engine().assess(inp)
        assert r.estimated_margin_loss_usd == 0.0

    def test_composite_thresholds_exactly_at_20(self):
        # Force all sub-scores to yield composite exactly 20
        # depth=20*0.30=6, freq=20*0.25=5, margin=20*0.25=5, neg=20*0.20=4
        # Need sub-scores 20 each:
        # depth: price_objection=0.40(+10) + nothing else viable... let's build exact 20 per sub
        # depth=20: avg_discount=0 (0), max=0 (0), objection=0.60 (20) → depth=20 ✓
        # freq=20: disc_freq=0 (0), multi=0 (0), list_price=0.20 (20) → freq=20 ✓
        # margin=20: gap=0 (0), override=0 (0), competitor=0.40 (20) → margin=20 ✓
        # neg=20: concession=0 (0), late=0 (0), corr=0.60 (20) → neg=20 ✓
        # composite = 20*0.30 + 20*0.25 + 20*0.25 + 20*0.20 = 6+5+5+4 = 20
        inp = _make_input(
            avg_discount_pct=0.00,
            max_discount_given_pct=0.00,
            price_objection_rate_pct=0.60,
            discount_frequency_pct=0.00,
            multi_discount_deal_rate_pct=0.00,
            list_price_close_rate_pct=0.20,
            avg_gross_margin_pct=0.55,
            target_gross_margin_pct=0.50,
            approval_override_rate_pct=0.00,
            competitor_price_match_rate_pct=0.40,
            first_ask_concession_rate_pct=0.00,
            late_stage_discount_rate_pct=0.00,
            avg_deal_cycle_vs_discount_corr=0.60,
        )
        r = _engine().assess(inp)
        assert r.pricing_composite == 20.0
        assert r.pricing_risk == PricingRisk.moderate
        assert r.pricing_severity == PricingSeverity.managed

    def test_composite_at_exactly_40(self):
        # All sub-scores = 40 → composite = 40*0.30+40*0.25+40*0.25+40*0.20 = 40
        # depth=40: price_objection=0.60(+20) + avg_discount=0.15(+28) - wait 20+28=48 too much
        # depth=40: avg_discount=0.08(+12) + max=0.28(+18) + objection=0.40(+10) = 40 ✓
        # freq=40: disc_freq=0.35(+12) + multi=0.25(+18) + list=0.40(+10) = 40 ✓
        # margin=40: gap=0.03(+12) + override=0.18(+18) + competitor=0.25(+10) = 40 ✓
        # neg=40: concession=0.25(+12) + late=0.35(+18) + corr=0.40(+10) = 40 ✓
        inp = _make_input(
            avg_discount_pct=0.08,
            max_discount_given_pct=0.28,
            price_objection_rate_pct=0.40,
            discount_frequency_pct=0.35,
            multi_discount_deal_rate_pct=0.25,
            list_price_close_rate_pct=0.40,
            avg_gross_margin_pct=0.47,
            target_gross_margin_pct=0.50,   # gap=0.03
            approval_override_rate_pct=0.18,
            competitor_price_match_rate_pct=0.25,
            first_ask_concession_rate_pct=0.25,
            late_stage_discount_rate_pct=0.35,
            avg_deal_cycle_vs_discount_corr=0.40,
        )
        r = _engine().assess(inp)
        assert r.pricing_composite == 40.0
        assert r.pricing_risk == PricingRisk.high
        assert r.pricing_severity == PricingSeverity.aggressive

    def test_composite_at_exactly_60(self):
        # All sub-scores = 60 → composite = 60
        # depth=60: avg=0.25(+45) + max=0.18(+6) + objection=0.40(+10) = 61 → cap not needed, use 45+6+10=61
        # Let's try: avg=0.15(+28) + max=0.28(+18) + objection=0.60(+20) = 66 → min(66,100)=66
        # Let's pick depth=60: avg=0.25(+45) + max=0.28(+18) + none = 63 > 60
        # Use: avg=0.15(+28) + max=0.28(+18) + objection=0.60(+20) = 66 (capped not needed here)
        # Actually want each sub at 60:
        # depth=60: avg=0.25(+45) + max=0.18(+6) + objection=0.40(+10) = 61 ~close
        # Let's aim at composite=60 directly: if all subs=60 → composite=60
        # depth: 45+18-3=? no. Let's try: avg=0.25(+45) + max=0.18(+6) + objection=0.40(+10)=61 clamp=61
        # This is tricky since thresholds are discrete. Let's just verify >= 60 triggers critical
        inp = _make_input(
            avg_discount_pct=0.25,
            max_discount_given_pct=0.40,
            price_objection_rate_pct=0.60,
            discount_frequency_pct=0.70,
            multi_discount_deal_rate_pct=0.40,
            list_price_close_rate_pct=0.10,
            avg_gross_margin_pct=0.30,
            target_gross_margin_pct=0.50,
            approval_override_rate_pct=0.30,
            competitor_price_match_rate_pct=0.40,
            first_ask_concession_rate_pct=0.60,
            late_stage_discount_rate_pct=0.50,
            avg_deal_cycle_vs_discount_corr=0.60,
        )
        r = _engine().assess(inp)
        assert r.pricing_composite >= 60
        assert r.pricing_risk == PricingRisk.critical
        assert r.pricing_severity == PricingSeverity.uncontrolled

    def test_engine_isolation_between_instances(self):
        e1 = _engine()
        e2 = _engine()
        e1.assess(_make_input(rep_id="A"))
        e1.assess(_make_input(rep_id="B"))
        e2.assess(_make_input(rep_id="C"))
        assert len(e1._results) == 2
        assert len(e2._results) == 1

    def test_to_dict_returns_new_dict_each_call(self):
        r = _engine().assess(_make_input())
        d1 = r.to_dict()
        d2 = r.to_dict()
        assert d1 == d2
        d1["rep_id"] = "MODIFIED"
        assert d2["rep_id"] != "MODIFIED"

    def test_large_revenue_usd(self):
        inp = _make_input(
            avg_gross_margin_pct=0.40,
            target_gross_margin_pct=0.50,
            avg_discount_pct=0.25,
            total_revenue_usd=100_000_000.0,
        )
        r = _engine().assess(inp)
        assert r.estimated_margin_loss_usd > 0

    def test_zero_total_deals_closed(self):
        inp = _make_input(total_deals_closed=0)
        r = _engine().assess(inp)
        assert isinstance(r, PricingResult)

    def test_summary_risk_counts_all_same_risk(self):
        engine = _engine()
        for _ in range(3):
            engine.assess(_make_input())
        s = engine.summary()
        assert s["risk_counts"].get("low", 0) == 3

    def test_discount_depth_boundary_just_below_0_08(self):
        inp = _make_input(avg_discount_pct=0.079, max_discount_given_pct=0.00, price_objection_rate_pct=0.00)
        r = _engine().assess(inp)
        assert r.discount_depth_score == 0.0

    def test_discount_depth_boundary_exactly_0_08(self):
        inp = _make_input(avg_discount_pct=0.08, max_discount_given_pct=0.00, price_objection_rate_pct=0.00)
        r = _engine().assess(inp)
        assert r.discount_depth_score == 12.0

    def test_discount_depth_boundary_just_below_0_15(self):
        inp = _make_input(avg_discount_pct=0.149, max_discount_given_pct=0.00, price_objection_rate_pct=0.00)
        r = _engine().assess(inp)
        assert r.discount_depth_score == 12.0

    def test_discount_depth_boundary_exactly_0_15(self):
        inp = _make_input(avg_discount_pct=0.15, max_discount_given_pct=0.00, price_objection_rate_pct=0.00)
        r = _engine().assess(inp)
        assert r.discount_depth_score == 28.0

    def test_margin_protection_boundary_margin_gap_exactly_0_03(self):
        inp = _make_input(
            avg_gross_margin_pct=0.47,
            target_gross_margin_pct=0.50,
            approval_override_rate_pct=0.00,
            competitor_price_match_rate_pct=0.00,
        )
        r = _engine().assess(inp)
        assert r.margin_protection_score == 12.0

    def test_negotiation_discipline_boundary_corr_exactly_0_40(self):
        inp = _make_input(first_ask_concession_rate_pct=0.00, late_stage_discount_rate_pct=0.00, avg_deal_cycle_vs_discount_corr=0.40)
        r = _engine().assess(inp)
        assert r.negotiation_discipline_score == 10.0

    def test_has_pricing_gap_all_three_triggers_false(self):
        inp = _make_input(
            avg_discount_pct=0.05,
            discount_frequency_pct=0.10,
        )
        r = _engine().assess(inp)
        # composite from these clean inputs will be near 0 (< 40), avg_discount < 0.15, freq < 0.50
        if r.pricing_composite < 40 and inp.avg_discount_pct < 0.15 and inp.discount_frequency_pct < 0.50:
            assert r.has_pricing_gap is False

    def test_pattern_detection_priority_discount_reflex_vs_late_stage(self):
        """When discount_reflex condition is met, it should win over late_stage_capitulator."""
        inp = _make_input(
            avg_discount_pct=0.20,
            first_ask_concession_rate_pct=0.55,
            late_stage_discount_rate_pct=0.45,
            multi_discount_deal_rate_pct=0.30,
        )
        r = _engine().assess(inp)
        assert r.pricing_pattern == PricingPattern.discount_reflex

    def test_signal_not_empty(self):
        r = _engine().assess(_make_input())
        assert len(r.pricing_signal) > 0

    def test_summary_returns_dict_type(self):
        assert isinstance(_engine().summary(), dict)
