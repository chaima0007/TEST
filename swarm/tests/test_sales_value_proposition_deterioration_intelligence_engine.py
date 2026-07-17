"""
Comprehensive pytest tests for SalesValuePropositionDeteriorationIntelligenceEngine.
~300+ tests across multiple classes.
"""
from __future__ import annotations
import pytest
from swarm.intelligence.sales_value_proposition_deterioration_intelligence_engine import (
    ValueRisk,
    ValuePattern,
    ValueSeverity,
    ValueAction,
    ValueInput,
    ValueResult,
    SalesValuePropositionDeteriorationIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> ValueInput:
    """Return a baseline ValueInput (all-zero / minimal) with optional overrides."""
    defaults = dict(
        rep_id="REP-001",
        region="WEST",
        evaluation_period_id="2026-Q2",
        value_message_consistency_score=0.80,
        pricing_objection_rate_pct=0.10,
        roi_challenge_rate_pct=0.10,
        value_prop_adoption_rate_pct=0.80,
        executive_engagement_on_value_pct=0.80,
        reference_request_rate_pct=0.10,
        competitive_loss_on_value_pct=0.05,
        discount_to_close_rate_pct=0.10,
        avg_discount_depth_pct=0.05,
        value_story_usage_rate_pct=0.80,
        business_case_creation_rate_pct=0.80,
        quantified_roi_presented_pct=0.80,
        persona_message_alignment_score=0.80,
        industry_vertical_win_rate=0.60,
        late_stage_value_reframe_pct=0.10,
        value_champion_development_rate=0.70,
        price_sensitivity_trigger_rate=0.10,
        total_closed_deals=10,
        avg_deal_value_usd=10_000.0,
    )
    defaults.update(overrides)
    return ValueInput(**defaults)


def make_zero_input(**overrides) -> ValueInput:
    """All numeric fields zero — worst-case for scoring (triggers no score points)."""
    defaults = dict(
        rep_id="REP-ZERO",
        region="EAST",
        evaluation_period_id="2026-Q1",
        value_message_consistency_score=0.0,
        pricing_objection_rate_pct=0.0,
        roi_challenge_rate_pct=0.0,
        value_prop_adoption_rate_pct=0.0,
        executive_engagement_on_value_pct=0.0,
        reference_request_rate_pct=0.0,
        competitive_loss_on_value_pct=0.0,
        discount_to_close_rate_pct=0.0,
        avg_discount_depth_pct=0.0,
        value_story_usage_rate_pct=0.0,
        business_case_creation_rate_pct=0.0,
        quantified_roi_presented_pct=0.0,
        persona_message_alignment_score=0.0,
        industry_vertical_win_rate=0.0,
        late_stage_value_reframe_pct=0.0,
        value_champion_development_rate=0.0,
        price_sensitivity_trigger_rate=0.0,
        total_closed_deals=0,
        avg_deal_value_usd=0.0,
    )
    defaults.update(overrides)
    return ValueInput(**defaults)


def engine() -> SalesValuePropositionDeteriorationIntelligenceEngine:
    return SalesValuePropositionDeteriorationIntelligenceEngine()


# ===========================================================================
# 1. Enum – str inheritance and membership
# ===========================================================================

class TestValueRiskEnum:
    def test_is_str(self):
        assert isinstance(ValueRisk.low, str)

    def test_low_value(self):
        assert ValueRisk.low == "low"

    def test_moderate_value(self):
        assert ValueRisk.moderate == "moderate"

    def test_high_value(self):
        assert ValueRisk.high == "high"

    def test_critical_value(self):
        assert ValueRisk.critical == "critical"

    def test_all_members(self):
        names = {m.name for m in ValueRisk}
        assert names == {"low", "moderate", "high", "critical"}

    def test_from_string(self):
        assert ValueRisk("high") is ValueRisk.high

    def test_str_comparison(self):
        assert ValueRisk.low == "low"


class TestValuePatternEnum:
    def test_is_str(self):
        assert isinstance(ValuePattern.none, str)

    def test_none_value(self):
        assert ValuePattern.none == "none"

    def test_value_vacuum(self):
        assert ValuePattern.value_vacuum == "value_vacuum"

    def test_price_before_value(self):
        assert ValuePattern.price_before_value == "price_before_value"

    def test_proof_dependent(self):
        assert ValuePattern.proof_dependent == "proof_dependent"

    def test_roi_ambiguity(self):
        assert ValuePattern.roi_ambiguity == "roi_ambiguity"

    def test_executive_disconnect(self):
        assert ValuePattern.executive_disconnect == "executive_disconnect"

    def test_all_six_members(self):
        names = {m.name for m in ValuePattern}
        assert names == {
            "none", "value_vacuum", "price_before_value",
            "proof_dependent", "roi_ambiguity", "executive_disconnect",
        }


class TestValueSeverityEnum:
    def test_is_str(self):
        assert isinstance(ValueSeverity.compelling, str)

    def test_compelling_value(self):
        assert ValueSeverity.compelling == "compelling"

    def test_adequate_value(self):
        assert ValueSeverity.adequate == "adequate"

    def test_deteriorating_value(self):
        assert ValueSeverity.deteriorating == "deteriorating"

    def test_failing_value(self):
        assert ValueSeverity.failing == "failing"

    def test_all_members(self):
        names = {m.name for m in ValueSeverity}
        assert names == {"compelling", "adequate", "deteriorating", "failing"}


class TestValueActionEnum:
    def test_is_str(self):
        assert isinstance(ValueAction.no_action, str)

    def test_no_action_value(self):
        assert ValueAction.no_action == "no_action"

    def test_value_message_refresh(self):
        assert ValueAction.value_message_refresh == "value_message_refresh"

    def test_roi_quantification_coaching(self):
        assert ValueAction.roi_quantification_coaching == "roi_quantification_coaching"

    def test_proof_strategy_coaching(self):
        assert ValueAction.proof_strategy_coaching == "proof_strategy_coaching"

    def test_executive_value_coaching(self):
        assert ValueAction.executive_value_coaching == "executive_value_coaching"

    def test_value_repositioning_program(self):
        assert ValueAction.value_repositioning_program == "value_repositioning_program"

    def test_commercial_reset(self):
        assert ValueAction.commercial_reset == "commercial_reset"

    def test_all_seven_members(self):
        names = {m.name for m in ValueAction}
        assert names == {
            "no_action", "value_message_refresh", "roi_quantification_coaching",
            "proof_strategy_coaching", "executive_value_coaching",
            "value_repositioning_program", "commercial_reset",
        }


# ===========================================================================
# 2. ValueInput – field existence and type
# ===========================================================================

class TestValueInputFields:
    def test_rep_id(self):
        inp = make_input(rep_id="X")
        assert inp.rep_id == "X"

    def test_region(self):
        inp = make_input(region="NORTH")
        assert inp.region == "NORTH"

    def test_evaluation_period_id(self):
        inp = make_input(evaluation_period_id="2026-Q3")
        assert inp.evaluation_period_id == "2026-Q3"

    def test_value_message_consistency_score(self):
        inp = make_input(value_message_consistency_score=0.5)
        assert inp.value_message_consistency_score == 0.5

    def test_pricing_objection_rate_pct(self):
        inp = make_input(pricing_objection_rate_pct=0.3)
        assert inp.pricing_objection_rate_pct == 0.3

    def test_roi_challenge_rate_pct(self):
        inp = make_input(roi_challenge_rate_pct=0.4)
        assert inp.roi_challenge_rate_pct == 0.4

    def test_value_prop_adoption_rate_pct(self):
        inp = make_input(value_prop_adoption_rate_pct=0.55)
        assert inp.value_prop_adoption_rate_pct == 0.55

    def test_executive_engagement_on_value_pct(self):
        inp = make_input(executive_engagement_on_value_pct=0.20)
        assert inp.executive_engagement_on_value_pct == 0.20

    def test_reference_request_rate_pct(self):
        inp = make_input(reference_request_rate_pct=0.55)
        assert inp.reference_request_rate_pct == 0.55

    def test_competitive_loss_on_value_pct(self):
        inp = make_input(competitive_loss_on_value_pct=0.40)
        assert inp.competitive_loss_on_value_pct == 0.40

    def test_discount_to_close_rate_pct(self):
        inp = make_input(discount_to_close_rate_pct=0.65)
        assert inp.discount_to_close_rate_pct == 0.65

    def test_avg_discount_depth_pct(self):
        inp = make_input(avg_discount_depth_pct=0.30)
        assert inp.avg_discount_depth_pct == 0.30

    def test_value_story_usage_rate_pct(self):
        inp = make_input(value_story_usage_rate_pct=0.70)
        assert inp.value_story_usage_rate_pct == 0.70

    def test_business_case_creation_rate_pct(self):
        inp = make_input(business_case_creation_rate_pct=0.15)
        assert inp.business_case_creation_rate_pct == 0.15

    def test_quantified_roi_presented_pct(self):
        inp = make_input(quantified_roi_presented_pct=0.20)
        assert inp.quantified_roi_presented_pct == 0.20

    def test_persona_message_alignment_score(self):
        inp = make_input(persona_message_alignment_score=0.25)
        assert inp.persona_message_alignment_score == 0.25

    def test_industry_vertical_win_rate(self):
        inp = make_input(industry_vertical_win_rate=0.45)
        assert inp.industry_vertical_win_rate == 0.45

    def test_late_stage_value_reframe_pct(self):
        inp = make_input(late_stage_value_reframe_pct=0.50)
        assert inp.late_stage_value_reframe_pct == 0.50

    def test_value_champion_development_rate(self):
        inp = make_input(value_champion_development_rate=0.30)
        assert inp.value_champion_development_rate == 0.30

    def test_price_sensitivity_trigger_rate(self):
        inp = make_input(price_sensitivity_trigger_rate=0.60)
        assert inp.price_sensitivity_trigger_rate == 0.60

    def test_total_closed_deals_int(self):
        inp = make_input(total_closed_deals=42)
        assert inp.total_closed_deals == 42

    def test_avg_deal_value_usd(self):
        inp = make_input(avg_deal_value_usd=50_000.0)
        assert inp.avg_deal_value_usd == 50_000.0


# ===========================================================================
# 3. to_dict() – exact 15-key contract
# ===========================================================================

class TestToDictContract:
    EXPECTED_KEYS = {
        "rep_id", "region", "value_risk", "value_pattern", "value_severity",
        "recommended_action", "message_quality_score", "value_defense_score",
        "proof_score", "deal_economics_score", "value_composite",
        "has_value_gap", "requires_value_coaching",
        "estimated_lost_revenue_usd", "value_signal",
    }

    def _result(self):
        return engine().assess(make_input())

    def test_key_count(self):
        d = self._result().to_dict()
        assert len(d) == 15

    def test_exact_keys(self):
        d = self._result().to_dict()
        assert set(d.keys()) == self.EXPECTED_KEYS

    def test_rep_id_in_dict(self):
        d = engine().assess(make_input(rep_id="REP-42")).to_dict()
        assert d["rep_id"] == "REP-42"

    def test_region_in_dict(self):
        d = engine().assess(make_input(region="SOUTH")).to_dict()
        assert d["region"] == "SOUTH"

    def test_value_risk_is_string(self):
        d = self._result().to_dict()
        assert isinstance(d["value_risk"], str)

    def test_value_pattern_is_string(self):
        d = self._result().to_dict()
        assert isinstance(d["value_pattern"], str)

    def test_value_severity_is_string(self):
        d = self._result().to_dict()
        assert isinstance(d["value_severity"], str)

    def test_recommended_action_is_string(self):
        d = self._result().to_dict()
        assert isinstance(d["recommended_action"], str)

    def test_message_quality_score_float(self):
        d = self._result().to_dict()
        assert isinstance(d["message_quality_score"], float)

    def test_value_defense_score_float(self):
        d = self._result().to_dict()
        assert isinstance(d["value_defense_score"], float)

    def test_proof_score_float(self):
        d = self._result().to_dict()
        assert isinstance(d["proof_score"], float)

    def test_deal_economics_score_float(self):
        d = self._result().to_dict()
        assert isinstance(d["deal_economics_score"], float)

    def test_value_composite_float(self):
        d = self._result().to_dict()
        assert isinstance(d["value_composite"], float)

    def test_has_value_gap_bool(self):
        d = self._result().to_dict()
        assert isinstance(d["has_value_gap"], bool)

    def test_requires_value_coaching_bool(self):
        d = self._result().to_dict()
        assert isinstance(d["requires_value_coaching"], bool)

    def test_estimated_lost_revenue_float(self):
        d = self._result().to_dict()
        assert isinstance(d["estimated_lost_revenue_usd"], float)

    def test_value_signal_str(self):
        d = self._result().to_dict()
        assert isinstance(d["value_signal"], str)

    def test_enum_values_are_raw_strings(self):
        d = self._result().to_dict()
        # Must not be enum objects
        for key in ("value_risk", "value_pattern", "value_severity", "recommended_action"):
            assert type(d[key]) is str


# ===========================================================================
# 4. _message_quality_score branches and thresholds
# ===========================================================================

class TestMessageQualityScore:
    def setup_method(self):
        self.eng = engine()

    # value_message_consistency_score branches
    def test_consistency_at_030_adds_40(self):
        inp = make_input(value_message_consistency_score=0.30,
                         value_prop_adoption_rate_pct=0.80,
                         persona_message_alignment_score=0.80)
        assert self.eng._message_quality_score(inp) == 40.0

    def test_consistency_just_below_055_adds_22(self):
        inp = make_input(value_message_consistency_score=0.55,
                         value_prop_adoption_rate_pct=0.80,
                         persona_message_alignment_score=0.80)
        assert self.eng._message_quality_score(inp) == 22.0

    def test_consistency_at_075_adds_8(self):
        inp = make_input(value_message_consistency_score=0.75,
                         value_prop_adoption_rate_pct=0.80,
                         persona_message_alignment_score=0.80)
        assert self.eng._message_quality_score(inp) == 8.0

    def test_consistency_above_075_adds_0(self):
        inp = make_input(value_message_consistency_score=0.76,
                         value_prop_adoption_rate_pct=0.80,
                         persona_message_alignment_score=0.80)
        assert self.eng._message_quality_score(inp) == 0.0

    # value_prop_adoption_rate_pct branches
    def test_adoption_at_040_adds_35(self):
        inp = make_input(value_message_consistency_score=0.80,
                         value_prop_adoption_rate_pct=0.40,
                         persona_message_alignment_score=0.80)
        assert self.eng._message_quality_score(inp) == 35.0

    def test_adoption_at_060_adds_18(self):
        inp = make_input(value_message_consistency_score=0.80,
                         value_prop_adoption_rate_pct=0.60,
                         persona_message_alignment_score=0.80)
        assert self.eng._message_quality_score(inp) == 18.0

    def test_adoption_above_060_adds_0(self):
        inp = make_input(value_message_consistency_score=0.80,
                         value_prop_adoption_rate_pct=0.61,
                         persona_message_alignment_score=0.80)
        assert self.eng._message_quality_score(inp) == 0.0

    # persona_message_alignment_score branches
    def test_persona_at_030_adds_25(self):
        inp = make_input(value_message_consistency_score=0.80,
                         value_prop_adoption_rate_pct=0.80,
                         persona_message_alignment_score=0.30)
        assert self.eng._message_quality_score(inp) == 25.0

    def test_persona_at_055_adds_12(self):
        inp = make_input(value_message_consistency_score=0.80,
                         value_prop_adoption_rate_pct=0.80,
                         persona_message_alignment_score=0.55)
        assert self.eng._message_quality_score(inp) == 12.0

    def test_persona_above_055_adds_0(self):
        inp = make_input(value_message_consistency_score=0.80,
                         value_prop_adoption_rate_pct=0.80,
                         persona_message_alignment_score=0.56)
        assert self.eng._message_quality_score(inp) == 0.0

    # cap at 100
    def test_capped_at_100(self):
        inp = make_input(value_message_consistency_score=0.30,
                         value_prop_adoption_rate_pct=0.40,
                         persona_message_alignment_score=0.30)
        # 40 + 35 + 25 = 100
        assert self.eng._message_quality_score(inp) == 100.0

    def test_would_exceed_100_is_capped(self):
        # 40 + 35 + 25 = 100 already; nothing exceeds
        inp = make_input(value_message_consistency_score=0.20,
                         value_prop_adoption_rate_pct=0.20,
                         persona_message_alignment_score=0.20)
        assert self.eng._message_quality_score(inp) == 100.0

    def test_zero_all_components(self):
        inp = make_input(value_message_consistency_score=0.80,
                         value_prop_adoption_rate_pct=0.80,
                         persona_message_alignment_score=0.80)
        assert self.eng._message_quality_score(inp) == 0.0

    def test_combined_two_branches(self):
        inp = make_input(value_message_consistency_score=0.30,  # +40
                         value_prop_adoption_rate_pct=0.40,     # +35
                         persona_message_alignment_score=0.80)  # +0
        assert self.eng._message_quality_score(inp) == 75.0


# ===========================================================================
# 5. _value_defense_score branches and thresholds
# ===========================================================================

class TestValueDefenseScore:
    def setup_method(self):
        self.eng = engine()

    # pricing_objection_rate_pct
    def test_objection_at_055_adds_40(self):
        inp = make_input(pricing_objection_rate_pct=0.55,
                         late_stage_value_reframe_pct=0.10,
                         roi_challenge_rate_pct=0.10)
        assert self.eng._value_defense_score(inp) == 40.0

    def test_objection_at_035_adds_22(self):
        inp = make_input(pricing_objection_rate_pct=0.35,
                         late_stage_value_reframe_pct=0.10,
                         roi_challenge_rate_pct=0.10)
        assert self.eng._value_defense_score(inp) == 22.0

    def test_objection_at_020_adds_8(self):
        inp = make_input(pricing_objection_rate_pct=0.20,
                         late_stage_value_reframe_pct=0.10,
                         roi_challenge_rate_pct=0.10)
        assert self.eng._value_defense_score(inp) == 8.0

    def test_objection_below_020_adds_0(self):
        inp = make_input(pricing_objection_rate_pct=0.19,
                         late_stage_value_reframe_pct=0.10,
                         roi_challenge_rate_pct=0.10)
        assert self.eng._value_defense_score(inp) == 0.0

    # late_stage_value_reframe_pct
    def test_reframe_at_045_adds_35(self):
        inp = make_input(pricing_objection_rate_pct=0.10,
                         late_stage_value_reframe_pct=0.45,
                         roi_challenge_rate_pct=0.10)
        assert self.eng._value_defense_score(inp) == 35.0

    def test_reframe_at_025_adds_18(self):
        inp = make_input(pricing_objection_rate_pct=0.10,
                         late_stage_value_reframe_pct=0.25,
                         roi_challenge_rate_pct=0.10)
        assert self.eng._value_defense_score(inp) == 18.0

    def test_reframe_below_025_adds_0(self):
        inp = make_input(pricing_objection_rate_pct=0.10,
                         late_stage_value_reframe_pct=0.24,
                         roi_challenge_rate_pct=0.10)
        assert self.eng._value_defense_score(inp) == 0.0

    # roi_challenge_rate_pct
    def test_roi_challenge_at_040_adds_25(self):
        inp = make_input(pricing_objection_rate_pct=0.10,
                         late_stage_value_reframe_pct=0.10,
                         roi_challenge_rate_pct=0.40)
        assert self.eng._value_defense_score(inp) == 25.0

    def test_roi_challenge_at_025_adds_12(self):
        inp = make_input(pricing_objection_rate_pct=0.10,
                         late_stage_value_reframe_pct=0.10,
                         roi_challenge_rate_pct=0.25)
        assert self.eng._value_defense_score(inp) == 12.0

    def test_roi_challenge_below_025_adds_0(self):
        inp = make_input(pricing_objection_rate_pct=0.10,
                         late_stage_value_reframe_pct=0.10,
                         roi_challenge_rate_pct=0.24)
        assert self.eng._value_defense_score(inp) == 0.0

    def test_capped_at_100(self):
        inp = make_input(pricing_objection_rate_pct=0.55,   # +40
                         late_stage_value_reframe_pct=0.45, # +35
                         roi_challenge_rate_pct=0.40)       # +25 → 100
        assert self.eng._value_defense_score(inp) == 100.0

    def test_zero_defense(self):
        inp = make_input(pricing_objection_rate_pct=0.10,
                         late_stage_value_reframe_pct=0.10,
                         roi_challenge_rate_pct=0.10)
        assert self.eng._value_defense_score(inp) == 0.0


# ===========================================================================
# 6. _proof_score branches and thresholds
# ===========================================================================

class TestProofScore:
    def setup_method(self):
        self.eng = engine()

    # quantified_roi_presented_pct
    def test_roi_presented_at_025_adds_40(self):
        inp = make_input(quantified_roi_presented_pct=0.25,
                         business_case_creation_rate_pct=0.80,
                         reference_request_rate_pct=0.10)
        assert self.eng._proof_score(inp) == 40.0

    def test_roi_presented_at_050_adds_22(self):
        inp = make_input(quantified_roi_presented_pct=0.50,
                         business_case_creation_rate_pct=0.80,
                         reference_request_rate_pct=0.10)
        assert self.eng._proof_score(inp) == 22.0

    def test_roi_presented_at_070_adds_8(self):
        inp = make_input(quantified_roi_presented_pct=0.70,
                         business_case_creation_rate_pct=0.80,
                         reference_request_rate_pct=0.10)
        assert self.eng._proof_score(inp) == 8.0

    def test_roi_presented_above_070_adds_0(self):
        inp = make_input(quantified_roi_presented_pct=0.71,
                         business_case_creation_rate_pct=0.80,
                         reference_request_rate_pct=0.10)
        assert self.eng._proof_score(inp) == 0.0

    # business_case_creation_rate_pct
    def test_biz_case_at_020_adds_35(self):
        inp = make_input(quantified_roi_presented_pct=0.80,
                         business_case_creation_rate_pct=0.20,
                         reference_request_rate_pct=0.10)
        assert self.eng._proof_score(inp) == 35.0

    def test_biz_case_at_045_adds_18(self):
        inp = make_input(quantified_roi_presented_pct=0.80,
                         business_case_creation_rate_pct=0.45,
                         reference_request_rate_pct=0.10)
        assert self.eng._proof_score(inp) == 18.0

    def test_biz_case_above_045_adds_0(self):
        inp = make_input(quantified_roi_presented_pct=0.80,
                         business_case_creation_rate_pct=0.46,
                         reference_request_rate_pct=0.10)
        assert self.eng._proof_score(inp) == 0.0

    # reference_request_rate_pct
    def test_ref_request_at_050_adds_25(self):
        inp = make_input(quantified_roi_presented_pct=0.80,
                         business_case_creation_rate_pct=0.80,
                         reference_request_rate_pct=0.50)
        assert self.eng._proof_score(inp) == 25.0

    def test_ref_request_at_030_adds_12(self):
        inp = make_input(quantified_roi_presented_pct=0.80,
                         business_case_creation_rate_pct=0.80,
                         reference_request_rate_pct=0.30)
        assert self.eng._proof_score(inp) == 12.0

    def test_ref_request_below_030_adds_0(self):
        inp = make_input(quantified_roi_presented_pct=0.80,
                         business_case_creation_rate_pct=0.80,
                         reference_request_rate_pct=0.29)
        assert self.eng._proof_score(inp) == 0.0

    def test_proof_capped_at_100(self):
        inp = make_input(quantified_roi_presented_pct=0.25,   # +40
                         business_case_creation_rate_pct=0.20,# +35
                         reference_request_rate_pct=0.50)     # +25 → 100
        assert self.eng._proof_score(inp) == 100.0

    def test_zero_proof(self):
        inp = make_input(quantified_roi_presented_pct=0.80,
                         business_case_creation_rate_pct=0.80,
                         reference_request_rate_pct=0.10)
        assert self.eng._proof_score(inp) == 0.0


# ===========================================================================
# 7. _deal_economics_score branches and thresholds
# ===========================================================================

class TestDealEconomicsScore:
    def setup_method(self):
        self.eng = engine()

    # discount_to_close_rate_pct
    def test_discount_at_060_adds_45(self):
        inp = make_input(discount_to_close_rate_pct=0.60,
                         avg_discount_depth_pct=0.05,
                         price_sensitivity_trigger_rate=0.10)
        assert self.eng._deal_economics_score(inp) == 45.0

    def test_discount_at_040_adds_25(self):
        inp = make_input(discount_to_close_rate_pct=0.40,
                         avg_discount_depth_pct=0.05,
                         price_sensitivity_trigger_rate=0.10)
        assert self.eng._deal_economics_score(inp) == 25.0

    def test_discount_at_025_adds_10(self):
        inp = make_input(discount_to_close_rate_pct=0.25,
                         avg_discount_depth_pct=0.05,
                         price_sensitivity_trigger_rate=0.10)
        assert self.eng._deal_economics_score(inp) == 10.0

    def test_discount_below_025_adds_0(self):
        inp = make_input(discount_to_close_rate_pct=0.24,
                         avg_discount_depth_pct=0.05,
                         price_sensitivity_trigger_rate=0.10)
        assert self.eng._deal_economics_score(inp) == 0.0

    # avg_discount_depth_pct
    def test_depth_at_025_adds_30(self):
        inp = make_input(discount_to_close_rate_pct=0.10,
                         avg_discount_depth_pct=0.25,
                         price_sensitivity_trigger_rate=0.10)
        assert self.eng._deal_economics_score(inp) == 30.0

    def test_depth_at_015_adds_15(self):
        inp = make_input(discount_to_close_rate_pct=0.10,
                         avg_discount_depth_pct=0.15,
                         price_sensitivity_trigger_rate=0.10)
        assert self.eng._deal_economics_score(inp) == 15.0

    def test_depth_below_015_adds_0(self):
        inp = make_input(discount_to_close_rate_pct=0.10,
                         avg_discount_depth_pct=0.14,
                         price_sensitivity_trigger_rate=0.10)
        assert self.eng._deal_economics_score(inp) == 0.0

    # price_sensitivity_trigger_rate
    def test_trigger_at_055_adds_25(self):
        inp = make_input(discount_to_close_rate_pct=0.10,
                         avg_discount_depth_pct=0.05,
                         price_sensitivity_trigger_rate=0.55)
        assert self.eng._deal_economics_score(inp) == 25.0

    def test_trigger_at_035_adds_10(self):
        inp = make_input(discount_to_close_rate_pct=0.10,
                         avg_discount_depth_pct=0.05,
                         price_sensitivity_trigger_rate=0.35)
        assert self.eng._deal_economics_score(inp) == 10.0

    def test_trigger_below_035_adds_0(self):
        inp = make_input(discount_to_close_rate_pct=0.10,
                         avg_discount_depth_pct=0.05,
                         price_sensitivity_trigger_rate=0.34)
        assert self.eng._deal_economics_score(inp) == 0.0

    def test_deal_econ_capped_at_100(self):
        inp = make_input(discount_to_close_rate_pct=0.60,  # +45
                         avg_discount_depth_pct=0.25,       # +30
                         price_sensitivity_trigger_rate=0.55)# +25 → 100
        assert self.eng._deal_economics_score(inp) == 100.0

    def test_zero_deal_economics(self):
        inp = make_input(discount_to_close_rate_pct=0.10,
                         avg_discount_depth_pct=0.05,
                         price_sensitivity_trigger_rate=0.10)
        assert self.eng._deal_economics_score(inp) == 0.0


# ===========================================================================
# 8. Composite formula weights sum to 1.0
# ===========================================================================

class TestCompositeWeights:
    def setup_method(self):
        self.eng = engine()

    def test_weights_sum_to_1(self):
        assert abs(0.30 + 0.30 + 0.25 + 0.15 - 1.00) < 1e-10

    def test_composite_formula_correct(self):
        m, v, p, d = 80.0, 60.0, 40.0, 20.0
        expected = round(80*0.30 + 60*0.30 + 40*0.25 + 20*0.15, 2)
        assert self.eng._composite(m, v, p, d) == expected

    def test_composite_all_zero(self):
        assert self.eng._composite(0, 0, 0, 0) == 0.0

    def test_composite_all_100(self):
        assert self.eng._composite(100, 100, 100, 100) == 100.0

    def test_composite_capped_at_100(self):
        assert self.eng._composite(200, 200, 200, 200) == 100.0

    def test_composite_message_weight(self):
        # Only m contributes: 100*0.30 = 30
        assert self.eng._composite(100, 0, 0, 0) == 30.0

    def test_composite_defense_weight(self):
        # Only v contributes: 100*0.30 = 30
        assert self.eng._composite(0, 100, 0, 0) == 30.0

    def test_composite_proof_weight(self):
        # Only p contributes: 100*0.25 = 25
        assert self.eng._composite(0, 0, 100, 0) == 25.0

    def test_composite_deal_weight(self):
        # Only d contributes: 100*0.15 = 15
        assert self.eng._composite(0, 0, 0, 100) == 15.0

    def test_composite_rounding(self):
        result = self.eng._composite(33.0, 33.0, 33.0, 33.0)
        assert result == round(33*0.30 + 33*0.30 + 33*0.25 + 33*0.15, 2)


# ===========================================================================
# 9. Risk thresholds
# ===========================================================================

class TestRiskThresholds:
    def setup_method(self):
        self.eng = engine()

    def test_critical_at_60(self):
        assert self.eng._risk(60.0) == ValueRisk.critical

    def test_critical_above_60(self):
        assert self.eng._risk(99.9) == ValueRisk.critical

    def test_critical_at_100(self):
        assert self.eng._risk(100.0) == ValueRisk.critical

    def test_high_at_40(self):
        assert self.eng._risk(40.0) == ValueRisk.high

    def test_high_at_59(self):
        assert self.eng._risk(59.9) == ValueRisk.high

    def test_moderate_at_20(self):
        assert self.eng._risk(20.0) == ValueRisk.moderate

    def test_moderate_at_39(self):
        assert self.eng._risk(39.9) == ValueRisk.moderate

    def test_low_at_0(self):
        assert self.eng._risk(0.0) == ValueRisk.low

    def test_low_at_19(self):
        assert self.eng._risk(19.9) == ValueRisk.low

    def test_boundary_just_below_60(self):
        assert self.eng._risk(59.99) == ValueRisk.high

    def test_boundary_just_below_40(self):
        assert self.eng._risk(39.99) == ValueRisk.moderate

    def test_boundary_just_below_20(self):
        assert self.eng._risk(19.99) == ValueRisk.low


# ===========================================================================
# 10. Severity thresholds
# ===========================================================================

class TestSeverityThresholds:
    def setup_method(self):
        self.eng = engine()

    def test_failing_at_60(self):
        assert self.eng._severity(60.0) == ValueSeverity.failing

    def test_failing_at_100(self):
        assert self.eng._severity(100.0) == ValueSeverity.failing

    def test_deteriorating_at_40(self):
        assert self.eng._severity(40.0) == ValueSeverity.deteriorating

    def test_deteriorating_at_59(self):
        assert self.eng._severity(59.9) == ValueSeverity.deteriorating

    def test_adequate_at_20(self):
        assert self.eng._severity(20.0) == ValueSeverity.adequate

    def test_adequate_at_39(self):
        assert self.eng._severity(39.9) == ValueSeverity.adequate

    def test_compelling_at_0(self):
        assert self.eng._severity(0.0) == ValueSeverity.compelling

    def test_compelling_at_19(self):
        assert self.eng._severity(19.9) == ValueSeverity.compelling


# ===========================================================================
# 11. Pattern detection – all 5 patterns + none
# ===========================================================================

class TestPatternDetection:
    def setup_method(self):
        self.eng = engine()

    # value_vacuum: consistency <= 0.35 AND competitive_loss >= 0.35
    def test_value_vacuum_detected(self):
        inp = make_input(value_message_consistency_score=0.35,
                         competitive_loss_on_value_pct=0.35,
                         price_sensitivity_trigger_rate=0.10,
                         discount_to_close_rate_pct=0.10,
                         reference_request_rate_pct=0.10,
                         business_case_creation_rate_pct=0.80,
                         roi_challenge_rate_pct=0.10,
                         quantified_roi_presented_pct=0.80,
                         executive_engagement_on_value_pct=0.80,
                         late_stage_value_reframe_pct=0.10)
        assert self.eng._pattern(inp) == ValuePattern.value_vacuum

    def test_value_vacuum_just_misses_consistency(self):
        inp = make_input(value_message_consistency_score=0.36,
                         competitive_loss_on_value_pct=0.35,
                         price_sensitivity_trigger_rate=0.10,
                         discount_to_close_rate_pct=0.10,
                         reference_request_rate_pct=0.10,
                         business_case_creation_rate_pct=0.80,
                         roi_challenge_rate_pct=0.10,
                         quantified_roi_presented_pct=0.80,
                         executive_engagement_on_value_pct=0.80,
                         late_stage_value_reframe_pct=0.10)
        assert self.eng._pattern(inp) != ValuePattern.value_vacuum

    def test_value_vacuum_just_misses_loss(self):
        inp = make_input(value_message_consistency_score=0.35,
                         competitive_loss_on_value_pct=0.34,
                         price_sensitivity_trigger_rate=0.10,
                         discount_to_close_rate_pct=0.10,
                         reference_request_rate_pct=0.10,
                         business_case_creation_rate_pct=0.80,
                         roi_challenge_rate_pct=0.10,
                         quantified_roi_presented_pct=0.80,
                         executive_engagement_on_value_pct=0.80,
                         late_stage_value_reframe_pct=0.10)
        assert self.eng._pattern(inp) != ValuePattern.value_vacuum

    # price_before_value: trigger >= 0.45 AND discount_to_close >= 0.45
    def test_price_before_value_detected(self):
        inp = make_input(value_message_consistency_score=0.80,
                         competitive_loss_on_value_pct=0.10,
                         price_sensitivity_trigger_rate=0.45,
                         discount_to_close_rate_pct=0.45,
                         reference_request_rate_pct=0.10,
                         business_case_creation_rate_pct=0.80,
                         roi_challenge_rate_pct=0.10,
                         quantified_roi_presented_pct=0.80,
                         executive_engagement_on_value_pct=0.80,
                         late_stage_value_reframe_pct=0.10)
        assert self.eng._pattern(inp) == ValuePattern.price_before_value

    def test_price_before_value_misses_trigger(self):
        inp = make_input(value_message_consistency_score=0.80,
                         competitive_loss_on_value_pct=0.10,
                         price_sensitivity_trigger_rate=0.44,
                         discount_to_close_rate_pct=0.45,
                         reference_request_rate_pct=0.10,
                         business_case_creation_rate_pct=0.80,
                         roi_challenge_rate_pct=0.10,
                         quantified_roi_presented_pct=0.80,
                         executive_engagement_on_value_pct=0.80,
                         late_stage_value_reframe_pct=0.10)
        assert self.eng._pattern(inp) != ValuePattern.price_before_value

    def test_price_before_value_misses_discount(self):
        inp = make_input(value_message_consistency_score=0.80,
                         competitive_loss_on_value_pct=0.10,
                         price_sensitivity_trigger_rate=0.45,
                         discount_to_close_rate_pct=0.44,
                         reference_request_rate_pct=0.10,
                         business_case_creation_rate_pct=0.80,
                         roi_challenge_rate_pct=0.10,
                         quantified_roi_presented_pct=0.80,
                         executive_engagement_on_value_pct=0.80,
                         late_stage_value_reframe_pct=0.10)
        assert self.eng._pattern(inp) != ValuePattern.price_before_value

    # proof_dependent: ref_request >= 0.40 AND biz_case <= 0.30
    def test_proof_dependent_detected(self):
        inp = make_input(value_message_consistency_score=0.80,
                         competitive_loss_on_value_pct=0.10,
                         price_sensitivity_trigger_rate=0.10,
                         discount_to_close_rate_pct=0.10,
                         reference_request_rate_pct=0.40,
                         business_case_creation_rate_pct=0.30,
                         roi_challenge_rate_pct=0.10,
                         quantified_roi_presented_pct=0.80,
                         executive_engagement_on_value_pct=0.80,
                         late_stage_value_reframe_pct=0.10)
        assert self.eng._pattern(inp) == ValuePattern.proof_dependent

    def test_proof_dependent_misses_ref_request(self):
        inp = make_input(value_message_consistency_score=0.80,
                         competitive_loss_on_value_pct=0.10,
                         price_sensitivity_trigger_rate=0.10,
                         discount_to_close_rate_pct=0.10,
                         reference_request_rate_pct=0.39,
                         business_case_creation_rate_pct=0.30,
                         roi_challenge_rate_pct=0.10,
                         quantified_roi_presented_pct=0.80,
                         executive_engagement_on_value_pct=0.80,
                         late_stage_value_reframe_pct=0.10)
        assert self.eng._pattern(inp) != ValuePattern.proof_dependent

    def test_proof_dependent_misses_biz_case(self):
        inp = make_input(value_message_consistency_score=0.80,
                         competitive_loss_on_value_pct=0.10,
                         price_sensitivity_trigger_rate=0.10,
                         discount_to_close_rate_pct=0.10,
                         reference_request_rate_pct=0.40,
                         business_case_creation_rate_pct=0.31,
                         roi_challenge_rate_pct=0.10,
                         quantified_roi_presented_pct=0.80,
                         executive_engagement_on_value_pct=0.80,
                         late_stage_value_reframe_pct=0.10)
        assert self.eng._pattern(inp) != ValuePattern.proof_dependent

    # roi_ambiguity: roi_challenge >= 0.35 AND roi_presented <= 0.35
    def test_roi_ambiguity_detected(self):
        inp = make_input(value_message_consistency_score=0.80,
                         competitive_loss_on_value_pct=0.10,
                         price_sensitivity_trigger_rate=0.10,
                         discount_to_close_rate_pct=0.10,
                         reference_request_rate_pct=0.10,
                         business_case_creation_rate_pct=0.80,
                         roi_challenge_rate_pct=0.35,
                         quantified_roi_presented_pct=0.35,
                         executive_engagement_on_value_pct=0.80,
                         late_stage_value_reframe_pct=0.10)
        assert self.eng._pattern(inp) == ValuePattern.roi_ambiguity

    def test_roi_ambiguity_misses_challenge(self):
        inp = make_input(value_message_consistency_score=0.80,
                         competitive_loss_on_value_pct=0.10,
                         price_sensitivity_trigger_rate=0.10,
                         discount_to_close_rate_pct=0.10,
                         reference_request_rate_pct=0.10,
                         business_case_creation_rate_pct=0.80,
                         roi_challenge_rate_pct=0.34,
                         quantified_roi_presented_pct=0.35,
                         executive_engagement_on_value_pct=0.80,
                         late_stage_value_reframe_pct=0.10)
        assert self.eng._pattern(inp) != ValuePattern.roi_ambiguity

    def test_roi_ambiguity_misses_presented(self):
        inp = make_input(value_message_consistency_score=0.80,
                         competitive_loss_on_value_pct=0.10,
                         price_sensitivity_trigger_rate=0.10,
                         discount_to_close_rate_pct=0.10,
                         reference_request_rate_pct=0.10,
                         business_case_creation_rate_pct=0.80,
                         roi_challenge_rate_pct=0.35,
                         quantified_roi_presented_pct=0.36,
                         executive_engagement_on_value_pct=0.80,
                         late_stage_value_reframe_pct=0.10)
        assert self.eng._pattern(inp) != ValuePattern.roi_ambiguity

    # executive_disconnect: exec_engagement <= 0.25 AND reframe >= 0.35
    def test_executive_disconnect_detected(self):
        inp = make_input(value_message_consistency_score=0.80,
                         competitive_loss_on_value_pct=0.10,
                         price_sensitivity_trigger_rate=0.10,
                         discount_to_close_rate_pct=0.10,
                         reference_request_rate_pct=0.10,
                         business_case_creation_rate_pct=0.80,
                         roi_challenge_rate_pct=0.10,
                         quantified_roi_presented_pct=0.80,
                         executive_engagement_on_value_pct=0.25,
                         late_stage_value_reframe_pct=0.35)
        assert self.eng._pattern(inp) == ValuePattern.executive_disconnect

    def test_executive_disconnect_misses_engagement(self):
        inp = make_input(value_message_consistency_score=0.80,
                         competitive_loss_on_value_pct=0.10,
                         price_sensitivity_trigger_rate=0.10,
                         discount_to_close_rate_pct=0.10,
                         reference_request_rate_pct=0.10,
                         business_case_creation_rate_pct=0.80,
                         roi_challenge_rate_pct=0.10,
                         quantified_roi_presented_pct=0.80,
                         executive_engagement_on_value_pct=0.26,
                         late_stage_value_reframe_pct=0.35)
        assert self.eng._pattern(inp) != ValuePattern.executive_disconnect

    def test_executive_disconnect_misses_reframe(self):
        inp = make_input(value_message_consistency_score=0.80,
                         competitive_loss_on_value_pct=0.10,
                         price_sensitivity_trigger_rate=0.10,
                         discount_to_close_rate_pct=0.10,
                         reference_request_rate_pct=0.10,
                         business_case_creation_rate_pct=0.80,
                         roi_challenge_rate_pct=0.10,
                         quantified_roi_presented_pct=0.80,
                         executive_engagement_on_value_pct=0.25,
                         late_stage_value_reframe_pct=0.34)
        assert self.eng._pattern(inp) != ValuePattern.executive_disconnect

    # none
    def test_none_pattern_when_no_conditions_met(self):
        inp = make_input()  # baseline all healthy
        assert self.eng._pattern(inp) == ValuePattern.none

    # pattern priority: value_vacuum before price_before_value
    def test_value_vacuum_priority_over_price_before_value(self):
        inp = make_input(value_message_consistency_score=0.35,
                         competitive_loss_on_value_pct=0.35,
                         price_sensitivity_trigger_rate=0.45,
                         discount_to_close_rate_pct=0.45,
                         reference_request_rate_pct=0.10,
                         business_case_creation_rate_pct=0.80,
                         roi_challenge_rate_pct=0.10,
                         quantified_roi_presented_pct=0.80,
                         executive_engagement_on_value_pct=0.80,
                         late_stage_value_reframe_pct=0.10)
        assert self.eng._pattern(inp) == ValuePattern.value_vacuum


# ===========================================================================
# 12. Action routing – all risk × pattern combos
# ===========================================================================

class TestActionRouting:
    def setup_method(self):
        self.eng = engine()

    # critical risk
    def test_critical_value_vacuum_commercial_reset(self):
        assert self.eng._action(ValueRisk.critical, ValuePattern.value_vacuum) == ValueAction.commercial_reset

    def test_critical_price_before_value_commercial_reset(self):
        assert self.eng._action(ValueRisk.critical, ValuePattern.price_before_value) == ValueAction.commercial_reset

    def test_critical_proof_dependent_repositioning(self):
        assert self.eng._action(ValueRisk.critical, ValuePattern.proof_dependent) == ValueAction.value_repositioning_program

    def test_critical_roi_ambiguity_repositioning(self):
        assert self.eng._action(ValueRisk.critical, ValuePattern.roi_ambiguity) == ValueAction.value_repositioning_program

    def test_critical_executive_disconnect_repositioning(self):
        assert self.eng._action(ValueRisk.critical, ValuePattern.executive_disconnect) == ValueAction.value_repositioning_program

    def test_critical_none_repositioning(self):
        assert self.eng._action(ValueRisk.critical, ValuePattern.none) == ValueAction.value_repositioning_program

    # high risk
    def test_high_value_vacuum_repositioning(self):
        assert self.eng._action(ValueRisk.high, ValuePattern.value_vacuum) == ValueAction.value_repositioning_program

    def test_high_price_before_value_roi_coaching(self):
        assert self.eng._action(ValueRisk.high, ValuePattern.price_before_value) == ValueAction.roi_quantification_coaching

    def test_high_proof_dependent_proof_coaching(self):
        assert self.eng._action(ValueRisk.high, ValuePattern.proof_dependent) == ValueAction.proof_strategy_coaching

    def test_high_roi_ambiguity_roi_coaching(self):
        assert self.eng._action(ValueRisk.high, ValuePattern.roi_ambiguity) == ValueAction.roi_quantification_coaching

    def test_high_executive_disconnect_exec_coaching(self):
        assert self.eng._action(ValueRisk.high, ValuePattern.executive_disconnect) == ValueAction.executive_value_coaching

    def test_high_none_message_refresh(self):
        assert self.eng._action(ValueRisk.high, ValuePattern.none) == ValueAction.value_message_refresh

    # moderate risk
    def test_moderate_value_vacuum_message_refresh(self):
        assert self.eng._action(ValueRisk.moderate, ValuePattern.value_vacuum) == ValueAction.value_message_refresh

    def test_moderate_price_before_value_message_refresh(self):
        assert self.eng._action(ValueRisk.moderate, ValuePattern.price_before_value) == ValueAction.value_message_refresh

    def test_moderate_none_message_refresh(self):
        assert self.eng._action(ValueRisk.moderate, ValuePattern.none) == ValueAction.value_message_refresh

    # low risk
    def test_low_value_vacuum_no_action(self):
        assert self.eng._action(ValueRisk.low, ValuePattern.value_vacuum) == ValueAction.no_action

    def test_low_none_no_action(self):
        assert self.eng._action(ValueRisk.low, ValuePattern.none) == ValueAction.no_action

    def test_low_all_patterns_no_action(self):
        for p in ValuePattern:
            assert self.eng._action(ValueRisk.low, p) == ValueAction.no_action


# ===========================================================================
# 13. has_value_gap flag
# ===========================================================================

class TestHasValueGap:
    def setup_method(self):
        self.eng = engine()

    def test_gap_true_when_composite_gte_40(self):
        inp = make_input()
        assert self.eng._has_gap(inp, 40.0) is True

    def test_gap_true_when_composite_gte_60(self):
        inp = make_input()
        assert self.eng._has_gap(inp, 60.0) is True

    def test_gap_true_when_pricing_objection_gte_035(self):
        inp = make_input(pricing_objection_rate_pct=0.35)
        assert self.eng._has_gap(inp, 10.0) is True

    def test_gap_true_when_discount_to_close_gte_040(self):
        inp = make_input(discount_to_close_rate_pct=0.40)
        assert self.eng._has_gap(inp, 10.0) is True

    def test_gap_false_when_all_below(self):
        inp = make_input(pricing_objection_rate_pct=0.34,
                         discount_to_close_rate_pct=0.39)
        assert self.eng._has_gap(inp, 39.0) is False

    def test_gap_true_pricing_objection_at_boundary(self):
        inp = make_input(pricing_objection_rate_pct=0.35,
                         discount_to_close_rate_pct=0.10)
        assert self.eng._has_gap(inp, 10.0) is True

    def test_gap_false_just_under_all_thresholds(self):
        inp = make_input(pricing_objection_rate_pct=0.34,
                         discount_to_close_rate_pct=0.39)
        assert self.eng._has_gap(inp, 39.9) is False


# ===========================================================================
# 14. requires_value_coaching flag
# ===========================================================================

class TestRequiresValueCoaching:
    def setup_method(self):
        self.eng = engine()

    def test_coaching_true_when_composite_gte_25(self):
        inp = make_input()
        assert self.eng._requires_coaching(inp, 25.0) is True

    def test_coaching_true_when_roi_presented_lte_050(self):
        inp = make_input(quantified_roi_presented_pct=0.50,
                         value_message_consistency_score=0.80)
        assert self.eng._requires_coaching(inp, 10.0) is True

    def test_coaching_true_when_consistency_lte_060(self):
        inp = make_input(quantified_roi_presented_pct=0.80,
                         value_message_consistency_score=0.60)
        assert self.eng._requires_coaching(inp, 10.0) is True

    def test_coaching_false_when_all_below(self):
        inp = make_input(quantified_roi_presented_pct=0.51,
                         value_message_consistency_score=0.61)
        assert self.eng._requires_coaching(inp, 24.0) is False

    def test_coaching_true_composite_at_boundary(self):
        inp = make_input(quantified_roi_presented_pct=0.80,
                         value_message_consistency_score=0.80)
        assert self.eng._requires_coaching(inp, 25.0) is True

    def test_coaching_false_just_under_all(self):
        inp = make_input(quantified_roi_presented_pct=0.51,
                         value_message_consistency_score=0.61)
        assert self.eng._requires_coaching(inp, 24.9) is False


# ===========================================================================
# 15. estimated_lost_revenue_usd formula
# ===========================================================================

class TestEstimatedLostRevenue:
    def setup_method(self):
        self.eng = engine()

    def test_zero_deals_gives_zero(self):
        inp = make_input(total_closed_deals=0, avg_deal_value_usd=10000.0,
                         competitive_loss_on_value_pct=0.5,
                         discount_to_close_rate_pct=0.5,
                         avg_discount_depth_pct=0.5)
        assert self.eng._lost_revenue(inp, 50.0) == 0.0

    def test_zero_composite_gives_zero(self):
        inp = make_input(total_closed_deals=10, avg_deal_value_usd=10000.0,
                         competitive_loss_on_value_pct=0.5,
                         discount_to_close_rate_pct=0.5,
                         avg_discount_depth_pct=0.5)
        assert self.eng._lost_revenue(inp, 0.0) == 0.0

    def test_zero_avg_deal_value_gives_zero(self):
        inp = make_input(total_closed_deals=10, avg_deal_value_usd=0.0,
                         competitive_loss_on_value_pct=0.5,
                         discount_to_close_rate_pct=0.5,
                         avg_discount_depth_pct=0.5)
        assert self.eng._lost_revenue(inp, 50.0) == 0.0

    def test_manual_calculation(self):
        inp = make_input(total_closed_deals=10,
                         avg_deal_value_usd=100_000.0,
                         competitive_loss_on_value_pct=0.20,
                         discount_to_close_rate_pct=0.50,
                         avg_discount_depth_pct=0.20)
        composite = 50.0
        # value_loss_rate = min(1.0, 0.20 + 0.50*0.20) = min(1.0, 0.30) = 0.30
        # lost = 10 * 100000 * 0.30 * 0.50 = 150000.0
        expected = round(10 * 100_000 * 0.30 * 0.50, 2)
        assert self.eng._lost_revenue(inp, composite) == expected

    def test_value_loss_rate_capped_at_1(self):
        inp = make_input(total_closed_deals=1,
                         avg_deal_value_usd=100.0,
                         competitive_loss_on_value_pct=1.0,
                         discount_to_close_rate_pct=1.0,
                         avg_discount_depth_pct=1.0)
        # min(1.0, 1.0 + 1.0*1.0) = 1.0
        # lost = 1 * 100 * 1.0 * (50/100) = 50.0
        assert self.eng._lost_revenue(inp, 50.0) == 50.0

    def test_result_is_rounded_to_2dp(self):
        inp = make_input(total_closed_deals=3,
                         avg_deal_value_usd=1000.0,
                         competitive_loss_on_value_pct=0.10,
                         discount_to_close_rate_pct=0.30,
                         avg_discount_depth_pct=0.10)
        result = self.eng._lost_revenue(inp, 33.33)
        # Should be rounded to 2 dp
        assert result == round(result, 2)


# ===========================================================================
# 16. Signal string content
# ===========================================================================

class TestSignalString:
    def setup_method(self):
        self.eng = engine()

    def test_low_composite_returns_strong_message(self):
        inp = make_input()
        sig = self.eng._signal(inp, ValuePattern.none, 10.0)
        assert "Value proposition strong" in sig

    def test_composite_exactly_20_is_not_strong(self):
        inp = make_input(pricing_objection_rate_pct=0.50,
                         discount_to_close_rate_pct=0.50,
                         quantified_roi_presented_pct=0.10)
        sig = self.eng._signal(inp, ValuePattern.value_vacuum, 20.0)
        assert "Value proposition strong" not in sig

    def test_signal_contains_pattern_label_value_vacuum(self):
        inp = make_input(pricing_objection_rate_pct=0.30)
        sig = self.eng._signal(inp, ValuePattern.value_vacuum, 30.0)
        assert "Value vacuum" in sig

    def test_signal_contains_pattern_label_price_before_value(self):
        inp = make_input(pricing_objection_rate_pct=0.30)
        sig = self.eng._signal(inp, ValuePattern.price_before_value, 30.0)
        assert "Price before value" in sig

    def test_signal_contains_pattern_label_proof_dependent(self):
        inp = make_input(pricing_objection_rate_pct=0.30)
        sig = self.eng._signal(inp, ValuePattern.proof_dependent, 30.0)
        assert "Proof dependent" in sig

    def test_signal_contains_pattern_label_roi_ambiguity(self):
        inp = make_input(pricing_objection_rate_pct=0.30)
        sig = self.eng._signal(inp, ValuePattern.roi_ambiguity, 30.0)
        assert "ROI ambiguity" in sig

    def test_signal_contains_pattern_label_executive_disconnect(self):
        inp = make_input(pricing_objection_rate_pct=0.30)
        sig = self.eng._signal(inp, ValuePattern.executive_disconnect, 30.0)
        assert "Executive disconnect" in sig

    def test_signal_contains_pricing_objection_pct(self):
        inp = make_input(pricing_objection_rate_pct=0.37,
                         discount_to_close_rate_pct=0.20,
                         quantified_roi_presented_pct=0.60)
        sig = self.eng._signal(inp, ValuePattern.none, 25.0)
        assert "37%" in sig

    def test_signal_contains_discount_pct(self):
        inp = make_input(pricing_objection_rate_pct=0.30,
                         discount_to_close_rate_pct=0.45,
                         quantified_roi_presented_pct=0.60)
        sig = self.eng._signal(inp, ValuePattern.none, 25.0)
        assert "45%" in sig

    def test_signal_contains_roi_pct(self):
        inp = make_input(pricing_objection_rate_pct=0.30,
                         discount_to_close_rate_pct=0.20,
                         quantified_roi_presented_pct=0.72)
        sig = self.eng._signal(inp, ValuePattern.none, 25.0)
        assert "72%" in sig

    def test_signal_contains_composite_int(self):
        inp = make_input(pricing_objection_rate_pct=0.30,
                         discount_to_close_rate_pct=0.20,
                         quantified_roi_presented_pct=0.60)
        sig = self.eng._signal(inp, ValuePattern.none, 35.7)
        assert "composite 36" in sig

    def test_signal_none_pattern_in_high_composite(self):
        inp = make_input(pricing_objection_rate_pct=0.30,
                         discount_to_close_rate_pct=0.20,
                         quantified_roi_presented_pct=0.60)
        sig = self.eng._signal(inp, ValuePattern.none, 25.0)
        assert "None" in sig or "none" in sig.lower()


# ===========================================================================
# 17. assess() end-to-end integration
# ===========================================================================

class TestAssessEndToEnd:
    def setup_method(self):
        self.eng = engine()

    def test_returns_value_result(self):
        result = self.eng.assess(make_input())
        assert isinstance(result, ValueResult)

    def test_rep_id_propagated(self):
        result = self.eng.assess(make_input(rep_id="REP-X99"))
        assert result.rep_id == "REP-X99"

    def test_region_propagated(self):
        result = self.eng.assess(make_input(region="APAC"))
        assert result.region == "APAC"

    def test_risk_is_valid_enum(self):
        result = self.eng.assess(make_input())
        assert isinstance(result.value_risk, ValueRisk)

    def test_pattern_is_valid_enum(self):
        result = self.eng.assess(make_input())
        assert isinstance(result.value_pattern, ValuePattern)

    def test_severity_is_valid_enum(self):
        result = self.eng.assess(make_input())
        assert isinstance(result.value_severity, ValueSeverity)

    def test_action_is_valid_enum(self):
        result = self.eng.assess(make_input())
        assert isinstance(result.recommended_action, ValueAction)

    def test_scores_are_floats(self):
        r = self.eng.assess(make_input())
        assert isinstance(r.message_quality_score, float)
        assert isinstance(r.value_defense_score, float)
        assert isinstance(r.proof_score, float)
        assert isinstance(r.deal_economics_score, float)

    def test_composite_within_0_100(self):
        r = self.eng.assess(make_input())
        assert 0.0 <= r.value_composite <= 100.0

    def test_has_value_gap_is_bool(self):
        r = self.eng.assess(make_input())
        assert isinstance(r.has_value_gap, bool)

    def test_requires_value_coaching_is_bool(self):
        r = self.eng.assess(make_input())
        assert isinstance(r.requires_value_coaching, bool)

    def test_estimated_lost_revenue_is_nonnegative(self):
        r = self.eng.assess(make_input())
        assert r.estimated_lost_revenue_usd >= 0.0

    def test_value_signal_is_str(self):
        r = self.eng.assess(make_input())
        assert isinstance(r.value_signal, str)

    def test_assess_stores_in_results(self):
        eng = engine()
        eng.assess(make_input(rep_id="A"))
        eng.assess(make_input(rep_id="B"))
        assert len(eng._results) == 2

    def test_healthy_rep_gets_low_risk(self):
        r = self.eng.assess(make_input())
        assert r.value_risk == ValueRisk.low

    def test_healthy_rep_gets_compelling_severity(self):
        r = self.eng.assess(make_input())
        assert r.value_severity == ValueSeverity.compelling

    def test_healthy_rep_gets_no_action(self):
        r = self.eng.assess(make_input())
        assert r.recommended_action == ValueAction.no_action

    def test_all_bad_rep_gets_critical_risk(self):
        inp = make_input(
            value_message_consistency_score=0.20,
            value_prop_adoption_rate_pct=0.20,
            persona_message_alignment_score=0.20,
            pricing_objection_rate_pct=0.70,
            late_stage_value_reframe_pct=0.60,
            roi_challenge_rate_pct=0.60,
            quantified_roi_presented_pct=0.10,
            business_case_creation_rate_pct=0.10,
            reference_request_rate_pct=0.70,
            discount_to_close_rate_pct=0.80,
            avg_discount_depth_pct=0.40,
            price_sensitivity_trigger_rate=0.70,
        )
        r = self.eng.assess(inp)
        assert r.value_risk == ValueRisk.critical

    def test_all_bad_rep_gets_failing_severity(self):
        inp = make_input(
            value_message_consistency_score=0.20,
            value_prop_adoption_rate_pct=0.20,
            persona_message_alignment_score=0.20,
            pricing_objection_rate_pct=0.70,
            late_stage_value_reframe_pct=0.60,
            roi_challenge_rate_pct=0.60,
            quantified_roi_presented_pct=0.10,
            business_case_creation_rate_pct=0.10,
            reference_request_rate_pct=0.70,
            discount_to_close_rate_pct=0.80,
            avg_discount_depth_pct=0.40,
            price_sensitivity_trigger_rate=0.70,
        )
        r = self.eng.assess(inp)
        assert r.value_severity == ValueSeverity.failing

    def test_composite_matches_formula(self):
        inp = make_input()
        r = self.eng.assess(inp)
        m = self.eng._message_quality_score(inp)
        v = self.eng._value_defense_score(inp)
        p = self.eng._proof_score(inp)
        d = self.eng._deal_economics_score(inp)
        expected = min(round(m*0.30 + v*0.30 + p*0.25 + d*0.15, 2), 100.0)
        assert r.value_composite == expected


# ===========================================================================
# 18. assess_batch()
# ===========================================================================

class TestAssessBatch:
    def setup_method(self):
        self.eng = engine()

    def test_empty_batch_returns_empty_list(self):
        assert self.eng.assess_batch([]) == []

    def test_batch_returns_same_count(self):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = self.eng.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_order_preserved(self):
        ids = ["A", "B", "C"]
        inputs = [make_input(rep_id=i) for i in ids]
        results = self.eng.assess_batch(inputs)
        assert [r.rep_id for r in results] == ids

    def test_batch_all_stored_in_results(self):
        inputs = [make_input(rep_id=f"R{i}") for i in range(7)]
        self.eng.assess_batch(inputs)
        assert len(self.eng._results) == 7

    def test_batch_returns_value_result_instances(self):
        results = self.eng.assess_batch([make_input(), make_input()])
        for r in results:
            assert isinstance(r, ValueResult)

    def test_batch_single_item(self):
        results = self.eng.assess_batch([make_input(rep_id="SOLO")])
        assert len(results) == 1
        assert results[0].rep_id == "SOLO"

    def test_batch_accumulates_with_prior_assess(self):
        self.eng.assess(make_input(rep_id="FIRST"))
        self.eng.assess_batch([make_input(rep_id="A"), make_input(rep_id="B")])
        assert len(self.eng._results) == 3


# ===========================================================================
# 19. summary() – empty state (all 13 keys)
# ===========================================================================

class TestSummaryEmpty:
    EXPECTED_KEYS = {
        "total", "risk_counts", "pattern_counts", "severity_counts",
        "action_counts", "avg_value_composite", "value_gap_count",
        "coaching_count", "avg_message_quality_score",
        "avg_value_defense_score", "avg_proof_score",
        "avg_deal_economics_score", "total_estimated_lost_revenue_usd",
    }

    def setup_method(self):
        self.eng = engine()

    def test_empty_summary_key_count(self):
        s = self.eng.summary()
        assert len(s) == 13

    def test_empty_summary_exact_keys(self):
        s = self.eng.summary()
        assert set(s.keys()) == self.EXPECTED_KEYS

    def test_total_is_zero(self):
        assert self.eng.summary()["total"] == 0

    def test_risk_counts_empty(self):
        assert self.eng.summary()["risk_counts"] == {}

    def test_pattern_counts_empty(self):
        assert self.eng.summary()["pattern_counts"] == {}

    def test_severity_counts_empty(self):
        assert self.eng.summary()["severity_counts"] == {}

    def test_action_counts_empty(self):
        assert self.eng.summary()["action_counts"] == {}

    def test_avg_value_composite_zero(self):
        assert self.eng.summary()["avg_value_composite"] == 0.0

    def test_value_gap_count_zero(self):
        assert self.eng.summary()["value_gap_count"] == 0

    def test_coaching_count_zero(self):
        assert self.eng.summary()["coaching_count"] == 0

    def test_avg_message_quality_score_zero(self):
        assert self.eng.summary()["avg_message_quality_score"] == 0.0

    def test_avg_value_defense_score_zero(self):
        assert self.eng.summary()["avg_value_defense_score"] == 0.0

    def test_avg_proof_score_zero(self):
        assert self.eng.summary()["avg_proof_score"] == 0.0

    def test_avg_deal_economics_score_zero(self):
        assert self.eng.summary()["avg_deal_economics_score"] == 0.0

    def test_total_estimated_lost_revenue_zero(self):
        assert self.eng.summary()["total_estimated_lost_revenue_usd"] == 0.0


# ===========================================================================
# 20. summary() – populated state
# ===========================================================================

class TestSummaryPopulated:
    def setup_method(self):
        self.eng = engine()
        self.eng.assess(make_input(rep_id="R1"))
        self.eng.assess(make_input(rep_id="R2"))
        self.s = self.eng.summary()

    def test_total_is_2(self):
        assert self.s["total"] == 2

    def test_risk_counts_not_empty(self):
        assert len(self.s["risk_counts"]) > 0

    def test_pattern_counts_not_empty(self):
        assert len(self.s["pattern_counts"]) > 0

    def test_severity_counts_not_empty(self):
        assert len(self.s["severity_counts"]) > 0

    def test_action_counts_not_empty(self):
        assert len(self.s["action_counts"]) > 0

    def test_risk_counts_sum_equals_total(self):
        assert sum(self.s["risk_counts"].values()) == self.s["total"]

    def test_pattern_counts_sum_equals_total(self):
        assert sum(self.s["pattern_counts"].values()) == self.s["total"]

    def test_severity_counts_sum_equals_total(self):
        assert sum(self.s["severity_counts"].values()) == self.s["total"]

    def test_action_counts_sum_equals_total(self):
        assert sum(self.s["action_counts"].values()) == self.s["total"]

    def test_avg_composite_is_float(self):
        assert isinstance(self.s["avg_value_composite"], float)

    def test_coaching_count_gte_zero(self):
        assert self.s["coaching_count"] >= 0

    def test_gap_count_gte_zero(self):
        assert self.s["value_gap_count"] >= 0

    def test_total_lost_revenue_gte_zero(self):
        assert self.s["total_estimated_lost_revenue_usd"] >= 0.0

    def test_avg_scores_are_floats(self):
        assert isinstance(self.s["avg_message_quality_score"], float)
        assert isinstance(self.s["avg_value_defense_score"], float)
        assert isinstance(self.s["avg_proof_score"], float)
        assert isinstance(self.s["avg_deal_economics_score"], float)

    def test_risk_counts_keys_are_valid_risk_values(self):
        valid = {r.value for r in ValueRisk}
        for k in self.s["risk_counts"]:
            assert k in valid

    def test_pattern_counts_keys_are_valid_pattern_values(self):
        valid = {p.value for p in ValuePattern}
        for k in self.s["pattern_counts"]:
            assert k in valid

    def test_severity_counts_keys_are_valid_severity_values(self):
        valid = {s.value for s in ValueSeverity}
        for k in self.s["severity_counts"]:
            assert k in valid

    def test_action_counts_keys_are_valid_action_values(self):
        valid = {a.value for a in ValueAction}
        for k in self.s["action_counts"]:
            assert k in valid

    def test_avg_composite_is_1dp(self):
        # round(..., 1)
        val = self.s["avg_value_composite"]
        assert round(val, 1) == val

    def test_total_lost_revenue_is_2dp(self):
        val = self.s["total_estimated_lost_revenue_usd"]
        assert round(val, 2) == val

    def test_gap_count_leq_total(self):
        assert self.s["value_gap_count"] <= self.s["total"]

    def test_coaching_count_leq_total(self):
        assert self.s["coaching_count"] <= self.s["total"]

    def test_summary_with_mixed_risks(self):
        eng2 = engine()
        # force a high-risk record
        eng2.assess(make_input(
            pricing_objection_rate_pct=0.70,
            late_stage_value_reframe_pct=0.60,
            roi_challenge_rate_pct=0.60,
            value_message_consistency_score=0.20,
            value_prop_adoption_rate_pct=0.20,
            persona_message_alignment_score=0.20,
            quantified_roi_presented_pct=0.10,
            business_case_creation_rate_pct=0.10,
            reference_request_rate_pct=0.70,
            discount_to_close_rate_pct=0.80,
            avg_discount_depth_pct=0.40,
            price_sensitivity_trigger_rate=0.70,
        ))
        eng2.assess(make_input())  # healthy
        s = eng2.summary()
        assert s["total"] == 2
        assert sum(s["risk_counts"].values()) == 2


# ===========================================================================
# 21. Engine isolation – separate instances do not share state
# ===========================================================================

class TestEngineIsolation:
    def test_two_engines_independent(self):
        e1 = engine()
        e2 = engine()
        e1.assess(make_input(rep_id="A"))
        e1.assess(make_input(rep_id="B"))
        e2.assess(make_input(rep_id="C"))
        assert len(e1._results) == 2
        assert len(e2._results) == 1

    def test_summaries_are_independent(self):
        e1 = engine()
        e2 = engine()
        e1.assess(make_input())
        s1 = e1.summary()
        s2 = e2.summary()
        assert s1["total"] == 1
        assert s2["total"] == 0

    def test_fresh_engine_has_empty_results(self):
        e = engine()
        assert e._results == []

    def test_fresh_engine_summary_is_empty(self):
        e = engine()
        assert e.summary()["total"] == 0

    def test_results_list_grows_per_assess(self):
        e = engine()
        for i in range(5):
            e.assess(make_input(rep_id=f"R{i}"))
        assert len(e._results) == 5


# ===========================================================================
# 22. Edge cases – all-zero inputs, boundary values
# ===========================================================================

class TestEdgeCases:
    def setup_method(self):
        self.eng = engine()

    def test_all_zero_input_assess_succeeds(self):
        """Zero inputs should not raise and produce a result."""
        result = self.eng.assess(make_zero_input())
        assert isinstance(result, ValueResult)

    def test_all_zero_message_quality_score(self):
        # consistency=0 → +40; adoption=0 → +35; persona=0 → +25 = 100
        inp = make_zero_input()
        assert self.eng._message_quality_score(inp) == 100.0

    def test_all_zero_value_defense_score(self):
        # pricing_objection=0 → 0; reframe=0 → 0; roi_challenge=0 → 0 = 0
        inp = make_zero_input()
        assert self.eng._value_defense_score(inp) == 0.0

    def test_all_zero_proof_score(self):
        # roi_presented=0 → +40; biz_case=0 → +35; ref_request=0 → 0 = 75
        inp = make_zero_input()
        assert self.eng._proof_score(inp) == 75.0

    def test_all_zero_deal_economics_score(self):
        # discount=0 → 0; depth=0 → 0; trigger=0 → 0 = 0
        inp = make_zero_input()
        assert self.eng._deal_economics_score(inp) == 0.0

    def test_all_zero_composite(self):
        inp = make_zero_input()
        m = self.eng._message_quality_score(inp)
        v = self.eng._value_defense_score(inp)
        p = self.eng._proof_score(inp)
        d = self.eng._deal_economics_score(inp)
        expected = min(round(m*0.30 + v*0.30 + p*0.25 + d*0.15, 2), 100.0)
        r = self.eng.assess(inp)
        assert r.value_composite == expected

    def test_all_zero_lost_revenue_is_zero(self):
        inp = make_zero_input()
        r = self.eng.assess(inp)
        assert r.estimated_lost_revenue_usd == 0.0

    def test_boundary_composite_exactly_60_is_critical(self):
        # Build a composite of exactly 60
        # Need: m*0.30 + v*0.30 + p*0.25 + d*0.15 = 60
        # Simple: m=100, v=100, p=100, d=100 → 100; need 60
        # m=60, v=60, p=60, d=60 → 60
        result = self.eng._composite(60.0, 60.0, 60.0, 60.0)
        assert result == 60.0
        assert self.eng._risk(result) == ValueRisk.critical

    def test_boundary_composite_exactly_40_is_high(self):
        result = self.eng._composite(40.0, 40.0, 40.0, 40.0)
        assert result == 40.0
        assert self.eng._risk(result) == ValueRisk.high

    def test_boundary_composite_exactly_20_is_moderate(self):
        result = self.eng._composite(20.0, 20.0, 20.0, 20.0)
        assert result == 20.0
        assert self.eng._risk(result) == ValueRisk.moderate

    def test_boundary_composite_just_below_60_is_high(self):
        assert self.eng._risk(59.99) == ValueRisk.high

    def test_boundary_composite_just_below_40_is_moderate(self):
        assert self.eng._risk(39.99) == ValueRisk.moderate

    def test_boundary_composite_just_below_20_is_low(self):
        assert self.eng._risk(19.99) == ValueRisk.low

    def test_very_large_deal_values(self):
        inp = make_input(total_closed_deals=1000, avg_deal_value_usd=1_000_000.0,
                         competitive_loss_on_value_pct=0.50,
                         discount_to_close_rate_pct=0.50,
                         avg_discount_depth_pct=0.50)
        r = self.eng.assess(inp)
        assert r.estimated_lost_revenue_usd >= 0.0

    def test_all_ones_input(self):
        """All float fields = 1.0 should not crash."""
        inp = make_input(
            value_message_consistency_score=1.0,
            pricing_objection_rate_pct=1.0,
            roi_challenge_rate_pct=1.0,
            value_prop_adoption_rate_pct=1.0,
            executive_engagement_on_value_pct=1.0,
            reference_request_rate_pct=1.0,
            competitive_loss_on_value_pct=1.0,
            discount_to_close_rate_pct=1.0,
            avg_discount_depth_pct=1.0,
            value_story_usage_rate_pct=1.0,
            business_case_creation_rate_pct=1.0,
            quantified_roi_presented_pct=1.0,
            persona_message_alignment_score=1.0,
            industry_vertical_win_rate=1.0,
            late_stage_value_reframe_pct=1.0,
            value_champion_development_rate=1.0,
            price_sensitivity_trigger_rate=1.0,
        )
        r = self.eng.assess(inp)
        assert isinstance(r, ValueResult)

    def test_rep_id_empty_string(self):
        r = self.eng.assess(make_input(rep_id=""))
        assert r.rep_id == ""

    def test_single_closed_deal(self):
        r = self.eng.assess(make_input(total_closed_deals=1, avg_deal_value_usd=500.0))
        assert isinstance(r, ValueResult)

    def test_many_batch_items(self):
        inputs = [make_input(rep_id=f"R{i}") for i in range(50)]
        results = self.eng.assess_batch(inputs)
        assert len(results) == 50


# ===========================================================================
# 23. Comprehensive score integration tests
# ===========================================================================

class TestIntegrationScenarios:
    def setup_method(self):
        self.eng = engine()

    def test_value_vacuum_scenario_end_to_end(self):
        """Rep with value vacuum pattern should get relevant action."""
        inp = make_input(
            value_message_consistency_score=0.25,  # very low
            competitive_loss_on_value_pct=0.50,    # high competitive loss on value
            pricing_objection_rate_pct=0.60,
            late_stage_value_reframe_pct=0.50,
            roi_challenge_rate_pct=0.50,
        )
        r = self.eng.assess(inp)
        assert r.value_pattern == ValuePattern.value_vacuum
        # Critical or high risk with this input → commercial_reset or repositioning
        assert r.recommended_action in (
            ValueAction.commercial_reset,
            ValueAction.value_repositioning_program,
        )

    def test_price_before_value_scenario(self):
        inp = make_input(
            price_sensitivity_trigger_rate=0.50,
            discount_to_close_rate_pct=0.50,
            value_message_consistency_score=0.80,
            competitive_loss_on_value_pct=0.10,
        )
        r = self.eng.assess(inp)
        assert r.value_pattern == ValuePattern.price_before_value

    def test_proof_dependent_scenario(self):
        inp = make_input(
            reference_request_rate_pct=0.50,
            business_case_creation_rate_pct=0.20,
            value_message_consistency_score=0.80,
            competitive_loss_on_value_pct=0.10,
            price_sensitivity_trigger_rate=0.10,
            discount_to_close_rate_pct=0.10,
        )
        r = self.eng.assess(inp)
        assert r.value_pattern == ValuePattern.proof_dependent

    def test_roi_ambiguity_scenario(self):
        inp = make_input(
            roi_challenge_rate_pct=0.40,
            quantified_roi_presented_pct=0.30,
            value_message_consistency_score=0.80,
            competitive_loss_on_value_pct=0.10,
            price_sensitivity_trigger_rate=0.10,
            discount_to_close_rate_pct=0.10,
            reference_request_rate_pct=0.10,
            business_case_creation_rate_pct=0.80,
        )
        r = self.eng.assess(inp)
        assert r.value_pattern == ValuePattern.roi_ambiguity

    def test_executive_disconnect_scenario(self):
        inp = make_input(
            executive_engagement_on_value_pct=0.20,
            late_stage_value_reframe_pct=0.40,
            value_message_consistency_score=0.80,
            competitive_loss_on_value_pct=0.10,
            price_sensitivity_trigger_rate=0.10,
            discount_to_close_rate_pct=0.10,
            reference_request_rate_pct=0.10,
            business_case_creation_rate_pct=0.80,
            roi_challenge_rate_pct=0.10,
            quantified_roi_presented_pct=0.80,
        )
        r = self.eng.assess(inp)
        assert r.value_pattern == ValuePattern.executive_disconnect

    def test_to_dict_round_trip_consistency(self):
        r = self.eng.assess(make_input())
        d = r.to_dict()
        assert d["value_risk"] == r.value_risk.value
        assert d["value_pattern"] == r.value_pattern.value
        assert d["value_severity"] == r.value_severity.value
        assert d["recommended_action"] == r.recommended_action.value
        assert d["message_quality_score"] == r.message_quality_score
        assert d["value_composite"] == r.value_composite
        assert d["has_value_gap"] == r.has_value_gap
        assert d["requires_value_coaching"] == r.requires_value_coaching
        assert d["estimated_lost_revenue_usd"] == r.estimated_lost_revenue_usd
        assert d["value_signal"] == r.value_signal

    def test_summary_total_lost_revenue_sum(self):
        eng2 = engine()
        results = eng2.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        expected_total = round(sum(r.estimated_lost_revenue_usd for r in results), 2)
        s = eng2.summary()
        assert s["total_estimated_lost_revenue_usd"] == expected_total

    def test_summary_coaching_count_accurate(self):
        eng2 = engine()
        results = eng2.assess_batch([make_input(rep_id=f"R{i}") for i in range(4)])
        expected_coaching = sum(1 for r in results if r.requires_value_coaching)
        assert eng2.summary()["coaching_count"] == expected_coaching

    def test_summary_gap_count_accurate(self):
        eng2 = engine()
        results = eng2.assess_batch([make_input(rep_id=f"R{i}") for i in range(4)])
        expected_gap = sum(1 for r in results if r.has_value_gap)
        assert eng2.summary()["value_gap_count"] == expected_gap

    def test_summary_avg_composite_accurate(self):
        eng2 = engine()
        results = eng2.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        expected = round(sum(r.value_composite for r in results) / 3, 1)
        assert eng2.summary()["avg_value_composite"] == expected

    def test_summary_avg_message_quality_accurate(self):
        eng2 = engine()
        results = eng2.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        expected = round(sum(r.message_quality_score for r in results) / 3, 1)
        assert eng2.summary()["avg_message_quality_score"] == expected
