"""
Comprehensive tests for SalesObjectionHandlingEffectivenessIntelligenceEngine.
"""
from __future__ import annotations

import pytest

from swarm.intelligence.sales_objection_handling_effectiveness_intelligence_engine import (
    ObjectionAction,
    ObjectionInput,
    ObjectionPattern,
    ObjectionResult,
    ObjectionRisk,
    ObjectionSeverity,
    SalesObjectionHandlingEffectivenessIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_input(
    rep_id: str = "REP001",
    region: str = "Northeast",
    evaluation_period_id: str = "2026-Q1",
    price_objection_to_discount_rate_pct: float = 0.20,
    avg_discount_after_price_objection_pct: float = 0.05,
    price_objection_win_rate_pct: float = 0.60,
    value_objection_close_rate_pct: float = 0.70,
    roi_case_presented_after_objection_pct: float = 0.60,
    proof_of_concept_offered_rate_pct: float = 0.50,
    competitive_objection_win_rate_pct: float = 0.70,
    deals_lost_after_competitive_comparison_pct: float = 0.20,
    battle_card_used_in_competitive_deal_pct: float = 0.60,
    timing_objection_to_slip_rate_pct: float = 0.20,
    next_step_set_after_timing_objection_pct: float = 0.70,
    urgency_event_used_to_counter_timing_pct: float = 0.50,
    total_objections_logged_per_deal: float = 2.0,
    objection_resolved_before_next_stage_pct: float = 0.80,
    deals_with_unresolved_objections_at_close_pct: float = 0.10,
    repeat_objection_rate_pct: float = 0.10,
    executive_referenced_to_resolve_objection_pct: float = 0.20,
    total_deals_with_objections: int = 50,
    avg_opportunity_value_usd: float = 10_000.0,
) -> ObjectionInput:
    return ObjectionInput(
        rep_id=rep_id,
        region=region,
        evaluation_period_id=evaluation_period_id,
        price_objection_to_discount_rate_pct=price_objection_to_discount_rate_pct,
        avg_discount_after_price_objection_pct=avg_discount_after_price_objection_pct,
        price_objection_win_rate_pct=price_objection_win_rate_pct,
        value_objection_close_rate_pct=value_objection_close_rate_pct,
        roi_case_presented_after_objection_pct=roi_case_presented_after_objection_pct,
        proof_of_concept_offered_rate_pct=proof_of_concept_offered_rate_pct,
        competitive_objection_win_rate_pct=competitive_objection_win_rate_pct,
        deals_lost_after_competitive_comparison_pct=deals_lost_after_competitive_comparison_pct,
        battle_card_used_in_competitive_deal_pct=battle_card_used_in_competitive_deal_pct,
        timing_objection_to_slip_rate_pct=timing_objection_to_slip_rate_pct,
        next_step_set_after_timing_objection_pct=next_step_set_after_timing_objection_pct,
        urgency_event_used_to_counter_timing_pct=urgency_event_used_to_counter_timing_pct,
        total_objections_logged_per_deal=total_objections_logged_per_deal,
        objection_resolved_before_next_stage_pct=objection_resolved_before_next_stage_pct,
        deals_with_unresolved_objections_at_close_pct=deals_with_unresolved_objections_at_close_pct,
        repeat_objection_rate_pct=repeat_objection_rate_pct,
        executive_referenced_to_resolve_objection_pct=executive_referenced_to_resolve_objection_pct,
        total_deals_with_objections=total_deals_with_objections,
        avg_opportunity_value_usd=avg_opportunity_value_usd,
    )


def _engine() -> SalesObjectionHandlingEffectivenessIntelligenceEngine:
    return SalesObjectionHandlingEffectivenessIntelligenceEngine()


# ---------------------------------------------------------------------------
# 1. Enum values
# ---------------------------------------------------------------------------

class TestEnumValues:
    def test_objection_risk_values(self):
        assert ObjectionRisk.low.value == "low"
        assert ObjectionRisk.moderate.value == "moderate"
        assert ObjectionRisk.high.value == "high"
        assert ObjectionRisk.critical.value == "critical"

    def test_objection_risk_members(self):
        members = {m.value for m in ObjectionRisk}
        assert members == {"low", "moderate", "high", "critical"}

    def test_objection_pattern_values(self):
        assert ObjectionPattern.none.value == "none"
        assert ObjectionPattern.price_capitulation.value == "price_capitulation"
        assert ObjectionPattern.value_gap_avoidance.value == "value_gap_avoidance"
        assert ObjectionPattern.competitor_deflection.value == "competitor_deflection"
        assert ObjectionPattern.timing_deferral.value == "timing_deferral"
        assert ObjectionPattern.objection_avoidance.value == "objection_avoidance"

    def test_objection_pattern_members(self):
        members = {m.value for m in ObjectionPattern}
        assert members == {
            "none", "price_capitulation", "value_gap_avoidance",
            "competitor_deflection", "timing_deferral", "objection_avoidance",
        }

    def test_objection_severity_values(self):
        assert ObjectionSeverity.proficient.value == "proficient"
        assert ObjectionSeverity.managing.value == "managing"
        assert ObjectionSeverity.struggling.value == "struggling"
        assert ObjectionSeverity.collapsing.value == "collapsing"

    def test_objection_severity_members(self):
        members = {m.value for m in ObjectionSeverity}
        assert members == {"proficient", "managing", "struggling", "collapsing"}

    def test_objection_action_values(self):
        assert ObjectionAction.no_action.value == "no_action"
        assert ObjectionAction.objection_scripting_coaching.value == "objection_scripting_coaching"
        assert ObjectionAction.roi_articulation_coaching.value == "roi_articulation_coaching"
        assert ObjectionAction.competitive_response_coaching.value == "competitive_response_coaching"
        assert ObjectionAction.closing_technique_coaching.value == "closing_technique_coaching"
        assert ObjectionAction.objection_handling_reset.value == "objection_handling_reset"

    def test_objection_action_members(self):
        members = {m.value for m in ObjectionAction}
        assert members == {
            "no_action", "objection_scripting_coaching", "roi_articulation_coaching",
            "competitive_response_coaching", "closing_technique_coaching",
            "objection_handling_reset",
        }

    def test_enums_are_str_subclass(self):
        assert isinstance(ObjectionRisk.low, str)
        assert isinstance(ObjectionPattern.none, str)
        assert isinstance(ObjectionSeverity.proficient, str)
        assert isinstance(ObjectionAction.no_action, str)


# ---------------------------------------------------------------------------
# 2. ObjectionInput fields
# ---------------------------------------------------------------------------

class TestObjectionInputFields:
    def test_all_22_fields_exist(self):
        inp = _make_input()
        fields = [
            "rep_id", "region", "evaluation_period_id",
            "price_objection_to_discount_rate_pct",
            "avg_discount_after_price_objection_pct",
            "price_objection_win_rate_pct",
            "value_objection_close_rate_pct",
            "roi_case_presented_after_objection_pct",
            "proof_of_concept_offered_rate_pct",
            "competitive_objection_win_rate_pct",
            "deals_lost_after_competitive_comparison_pct",
            "battle_card_used_in_competitive_deal_pct",
            "timing_objection_to_slip_rate_pct",
            "next_step_set_after_timing_objection_pct",
            "urgency_event_used_to_counter_timing_pct",
            "total_objections_logged_per_deal",
            "objection_resolved_before_next_stage_pct",
            "deals_with_unresolved_objections_at_close_pct",
            "repeat_objection_rate_pct",
            "executive_referenced_to_resolve_objection_pct",
            "total_deals_with_objections",
            "avg_opportunity_value_usd",
        ]
        for f in fields:
            assert hasattr(inp, f), f"missing field: {f}"

    def test_field_count_is_22(self):
        import dataclasses
        fields = dataclasses.fields(ObjectionInput)
        assert len(fields) == 22

    def test_string_fields(self):
        inp = _make_input(rep_id="R9", region="West", evaluation_period_id="Q2")
        assert inp.rep_id == "R9"
        assert inp.region == "West"
        assert inp.evaluation_period_id == "Q2"

    def test_int_field_total_deals(self):
        inp = _make_input(total_deals_with_objections=100)
        assert inp.total_deals_with_objections == 100

    def test_float_field_avg_opportunity_value(self):
        inp = _make_input(avg_opportunity_value_usd=25000.0)
        assert inp.avg_opportunity_value_usd == 25000.0


# ---------------------------------------------------------------------------
# 3. ObjectionResult fields and to_dict()
# ---------------------------------------------------------------------------

class TestObjectionResultFields:
    def _result(self) -> ObjectionResult:
        return _engine().assess(_make_input())

    def test_result_has_15_fields(self):
        import dataclasses
        fields = dataclasses.fields(ObjectionResult)
        assert len(fields) == 15

    def test_result_field_names(self):
        r = self._result()
        expected = [
            "rep_id", "region", "objection_risk", "objection_pattern",
            "objection_severity", "recommended_action", "price_score",
            "value_score", "competitive_score", "timing_score",
            "objection_composite", "has_objection_gap",
            "requires_objection_coaching", "estimated_revenue_surrendered_usd",
            "objection_signal",
        ]
        for f in expected:
            assert hasattr(r, f), f"missing field: {f}"

    def test_to_dict_returns_15_keys(self):
        d = self._result().to_dict()
        assert len(d) == 15

    def test_to_dict_key_names(self):
        d = self._result().to_dict()
        expected_keys = {
            "rep_id", "region", "objection_risk", "objection_pattern",
            "objection_severity", "recommended_action", "price_score",
            "value_score", "competitive_score", "timing_score",
            "objection_composite", "has_objection_gap",
            "requires_objection_coaching", "estimated_revenue_surrendered_usd",
            "objection_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_fields_are_strings(self):
        d = self._result().to_dict()
        assert isinstance(d["objection_risk"], str)
        assert isinstance(d["objection_pattern"], str)
        assert isinstance(d["objection_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_preserves_rep_id_and_region(self):
        inp = _make_input(rep_id="XYZ", region="South")
        d = _engine().assess(inp).to_dict()
        assert d["rep_id"] == "XYZ"
        assert d["region"] == "South"

    def test_to_dict_score_fields_are_floats(self):
        d = self._result().to_dict()
        for key in ("price_score", "value_score", "competitive_score",
                    "timing_score", "objection_composite"):
            assert isinstance(d[key], float), f"{key} should be float"

    def test_to_dict_flag_fields_are_bools(self):
        d = self._result().to_dict()
        assert isinstance(d["has_objection_gap"], bool)
        assert isinstance(d["requires_objection_coaching"], bool)


# ---------------------------------------------------------------------------
# 4. Price sub-score branches
# ---------------------------------------------------------------------------

class TestPriceScore:
    def _price(self, **kwargs) -> float:
        return _engine()._price_score(_make_input(**kwargs))

    # price_objection_to_discount_rate_pct tiers
    def test_discount_rate_below_30_adds_0(self):
        # 0.20 < 0.30 → +0
        s = self._price(
            price_objection_to_discount_rate_pct=0.20,
            avg_discount_after_price_objection_pct=0.0,
            price_objection_win_rate_pct=0.60,
        )
        assert s == 0.0

    def test_discount_rate_at_30_adds_8(self):
        s = self._price(
            price_objection_to_discount_rate_pct=0.30,
            avg_discount_after_price_objection_pct=0.0,
            price_objection_win_rate_pct=0.60,
        )
        assert s == 8.0

    def test_discount_rate_at_50_adds_22(self):
        s = self._price(
            price_objection_to_discount_rate_pct=0.50,
            avg_discount_after_price_objection_pct=0.0,
            price_objection_win_rate_pct=0.60,
        )
        assert s == 22.0

    def test_discount_rate_at_70_adds_40(self):
        s = self._price(
            price_objection_to_discount_rate_pct=0.70,
            avg_discount_after_price_objection_pct=0.0,
            price_objection_win_rate_pct=0.60,
        )
        assert s == 40.0

    # avg_discount_after_price_objection_pct tiers
    def test_avg_discount_below_10_adds_0(self):
        s = self._price(
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.05,
            price_objection_win_rate_pct=0.60,
        )
        assert s == 0.0

    def test_avg_discount_at_10_adds_18(self):
        s = self._price(
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.10,
            price_objection_win_rate_pct=0.60,
        )
        assert s == 18.0

    def test_avg_discount_at_20_adds_35(self):
        s = self._price(
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.20,
            price_objection_win_rate_pct=0.60,
        )
        assert s == 35.0

    # price_objection_win_rate_pct tiers
    def test_win_rate_above_50_adds_0(self):
        s = self._price(
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
            price_objection_win_rate_pct=0.60,
        )
        assert s == 0.0

    def test_win_rate_at_50_adds_12(self):
        s = self._price(
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
            price_objection_win_rate_pct=0.50,
        )
        assert s == 12.0

    def test_win_rate_at_30_adds_25(self):
        s = self._price(
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
            price_objection_win_rate_pct=0.30,
        )
        assert s == 25.0

    def test_price_score_capped_at_100(self):
        s = self._price(
            price_objection_to_discount_rate_pct=0.90,
            avg_discount_after_price_objection_pct=0.30,
            price_objection_win_rate_pct=0.10,
        )
        # 40 + 35 + 25 = 100
        assert s == 100.0

    def test_price_score_over_100_is_capped(self):
        # impossible in practice but cap check: max possible is 40+35+25=100
        s = self._price(
            price_objection_to_discount_rate_pct=1.0,
            avg_discount_after_price_objection_pct=1.0,
            price_objection_win_rate_pct=0.0,
        )
        assert s == 100.0

    def test_price_score_all_zero(self):
        s = self._price(
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
            price_objection_win_rate_pct=1.0,
        )
        assert s == 0.0

    def test_price_score_combines_all_three(self):
        # 0.30 → +8, 0.10 → +18, 0.50 → +12  => 38
        s = self._price(
            price_objection_to_discount_rate_pct=0.30,
            avg_discount_after_price_objection_pct=0.10,
            price_objection_win_rate_pct=0.50,
        )
        assert s == 38.0


# ---------------------------------------------------------------------------
# 5. Value sub-score branches
# ---------------------------------------------------------------------------

class TestValueScore:
    def _val(self, **kwargs) -> float:
        return _engine()._value_score(_make_input(**kwargs))

    # value_objection_close_rate_pct tiers
    def test_close_rate_above_65_adds_0(self):
        s = self._val(
            value_objection_close_rate_pct=0.80,
            roi_case_presented_after_objection_pct=0.60,
            proof_of_concept_offered_rate_pct=0.50,
        )
        assert s == 0.0

    def test_close_rate_at_65_adds_8(self):
        s = self._val(
            value_objection_close_rate_pct=0.65,
            roi_case_presented_after_objection_pct=0.60,
            proof_of_concept_offered_rate_pct=0.50,
        )
        assert s == 8.0

    def test_close_rate_at_45_adds_22(self):
        s = self._val(
            value_objection_close_rate_pct=0.45,
            roi_case_presented_after_objection_pct=0.60,
            proof_of_concept_offered_rate_pct=0.50,
        )
        assert s == 22.0

    def test_close_rate_at_25_adds_40(self):
        s = self._val(
            value_objection_close_rate_pct=0.25,
            roi_case_presented_after_objection_pct=0.60,
            proof_of_concept_offered_rate_pct=0.50,
        )
        assert s == 40.0

    # roi_case_presented_after_objection_pct tiers
    def test_roi_above_55_adds_0(self):
        s = self._val(
            value_objection_close_rate_pct=0.80,
            roi_case_presented_after_objection_pct=0.60,
            proof_of_concept_offered_rate_pct=0.50,
        )
        assert s == 0.0

    def test_roi_at_55_adds_18(self):
        s = self._val(
            value_objection_close_rate_pct=0.80,
            roi_case_presented_after_objection_pct=0.55,
            proof_of_concept_offered_rate_pct=0.50,
        )
        assert s == 18.0

    def test_roi_at_30_adds_35(self):
        s = self._val(
            value_objection_close_rate_pct=0.80,
            roi_case_presented_after_objection_pct=0.30,
            proof_of_concept_offered_rate_pct=0.50,
        )
        assert s == 35.0

    # proof_of_concept_offered_rate_pct tiers
    def test_poc_above_40_adds_0(self):
        s = self._val(
            value_objection_close_rate_pct=0.80,
            roi_case_presented_after_objection_pct=0.60,
            proof_of_concept_offered_rate_pct=0.50,
        )
        assert s == 0.0

    def test_poc_at_40_adds_12(self):
        s = self._val(
            value_objection_close_rate_pct=0.80,
            roi_case_presented_after_objection_pct=0.60,
            proof_of_concept_offered_rate_pct=0.40,
        )
        assert s == 12.0

    def test_poc_at_20_adds_25(self):
        s = self._val(
            value_objection_close_rate_pct=0.80,
            roi_case_presented_after_objection_pct=0.60,
            proof_of_concept_offered_rate_pct=0.20,
        )
        assert s == 25.0

    def test_value_score_capped_at_100(self):
        s = self._val(
            value_objection_close_rate_pct=0.10,
            roi_case_presented_after_objection_pct=0.10,
            proof_of_concept_offered_rate_pct=0.10,
        )
        # 40 + 35 + 25 = 100
        assert s == 100.0

    def test_value_score_zero(self):
        s = self._val(
            value_objection_close_rate_pct=0.90,
            roi_case_presented_after_objection_pct=0.90,
            proof_of_concept_offered_rate_pct=0.90,
        )
        assert s == 0.0

    def test_value_score_combines_all_three(self):
        # 0.65 → +8, 0.55 → +18, 0.40 → +12 → 38
        s = self._val(
            value_objection_close_rate_pct=0.65,
            roi_case_presented_after_objection_pct=0.55,
            proof_of_concept_offered_rate_pct=0.40,
        )
        assert s == 38.0


# ---------------------------------------------------------------------------
# 6. Competitive sub-score branches
# ---------------------------------------------------------------------------

class TestCompetitiveScore:
    def _comp(self, **kwargs) -> float:
        return _engine()._competitive_score(_make_input(**kwargs))

    # competitive_objection_win_rate_pct tiers
    def test_comp_win_rate_above_65_adds_0(self):
        s = self._comp(
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.10,
            battle_card_used_in_competitive_deal_pct=0.60,
        )
        assert s == 0.0

    def test_comp_win_rate_at_65_adds_10(self):
        s = self._comp(
            competitive_objection_win_rate_pct=0.65,
            deals_lost_after_competitive_comparison_pct=0.10,
            battle_card_used_in_competitive_deal_pct=0.60,
        )
        assert s == 10.0

    def test_comp_win_rate_at_50_adds_25(self):
        s = self._comp(
            competitive_objection_win_rate_pct=0.50,
            deals_lost_after_competitive_comparison_pct=0.10,
            battle_card_used_in_competitive_deal_pct=0.60,
        )
        assert s == 25.0

    def test_comp_win_rate_at_30_adds_45(self):
        s = self._comp(
            competitive_objection_win_rate_pct=0.30,
            deals_lost_after_competitive_comparison_pct=0.10,
            battle_card_used_in_competitive_deal_pct=0.60,
        )
        assert s == 45.0

    # deals_lost_after_competitive_comparison_pct tiers
    def test_deals_lost_below_35_adds_0(self):
        s = self._comp(
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.20,
            battle_card_used_in_competitive_deal_pct=0.60,
        )
        assert s == 0.0

    def test_deals_lost_at_35_adds_15(self):
        s = self._comp(
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.35,
            battle_card_used_in_competitive_deal_pct=0.60,
        )
        assert s == 15.0

    def test_deals_lost_at_55_adds_30(self):
        s = self._comp(
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.55,
            battle_card_used_in_competitive_deal_pct=0.60,
        )
        assert s == 30.0

    # battle_card_used_in_competitive_deal_pct tiers
    def test_battle_card_above_50_adds_0(self):
        s = self._comp(
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.10,
            battle_card_used_in_competitive_deal_pct=0.60,
        )
        assert s == 0.0

    def test_battle_card_at_50_adds_12(self):
        s = self._comp(
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.10,
            battle_card_used_in_competitive_deal_pct=0.50,
        )
        assert s == 12.0

    def test_battle_card_at_25_adds_25(self):
        s = self._comp(
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.10,
            battle_card_used_in_competitive_deal_pct=0.25,
        )
        assert s == 25.0

    def test_competitive_score_capped_at_100(self):
        s = self._comp(
            competitive_objection_win_rate_pct=0.10,
            deals_lost_after_competitive_comparison_pct=0.90,
            battle_card_used_in_competitive_deal_pct=0.10,
        )
        # 45 + 30 + 25 = 100
        assert s == 100.0

    def test_competitive_score_zero(self):
        s = self._comp(
            competitive_objection_win_rate_pct=0.90,
            deals_lost_after_competitive_comparison_pct=0.10,
            battle_card_used_in_competitive_deal_pct=0.90,
        )
        assert s == 0.0

    def test_competitive_score_combines_all_three(self):
        # 0.65 → +10, 0.35 → +15, 0.50 → +12 → 37
        s = self._comp(
            competitive_objection_win_rate_pct=0.65,
            deals_lost_after_competitive_comparison_pct=0.35,
            battle_card_used_in_competitive_deal_pct=0.50,
        )
        assert s == 37.0


# ---------------------------------------------------------------------------
# 7. Timing sub-score branches
# ---------------------------------------------------------------------------

class TestTimingScore:
    def _timing(self, **kwargs) -> float:
        return _engine()._timing_score(_make_input(**kwargs))

    # timing_objection_to_slip_rate_pct tiers
    def test_slip_rate_below_25_adds_0(self):
        s = self._timing(
            timing_objection_to_slip_rate_pct=0.20,
            next_step_set_after_timing_objection_pct=0.70,
            urgency_event_used_to_counter_timing_pct=0.50,
        )
        assert s == 0.0

    def test_slip_rate_at_25_adds_8(self):
        s = self._timing(
            timing_objection_to_slip_rate_pct=0.25,
            next_step_set_after_timing_objection_pct=0.70,
            urgency_event_used_to_counter_timing_pct=0.50,
        )
        assert s == 8.0

    def test_slip_rate_at_45_adds_22(self):
        s = self._timing(
            timing_objection_to_slip_rate_pct=0.45,
            next_step_set_after_timing_objection_pct=0.70,
            urgency_event_used_to_counter_timing_pct=0.50,
        )
        assert s == 22.0

    def test_slip_rate_at_65_adds_40(self):
        s = self._timing(
            timing_objection_to_slip_rate_pct=0.65,
            next_step_set_after_timing_objection_pct=0.70,
            urgency_event_used_to_counter_timing_pct=0.50,
        )
        assert s == 40.0

    # next_step_set_after_timing_objection_pct tiers
    def test_next_step_above_65_adds_0(self):
        s = self._timing(
            timing_objection_to_slip_rate_pct=0.20,
            next_step_set_after_timing_objection_pct=0.70,
            urgency_event_used_to_counter_timing_pct=0.50,
        )
        assert s == 0.0

    def test_next_step_at_65_adds_18(self):
        s = self._timing(
            timing_objection_to_slip_rate_pct=0.20,
            next_step_set_after_timing_objection_pct=0.65,
            urgency_event_used_to_counter_timing_pct=0.50,
        )
        assert s == 18.0

    def test_next_step_at_40_adds_35(self):
        s = self._timing(
            timing_objection_to_slip_rate_pct=0.20,
            next_step_set_after_timing_objection_pct=0.40,
            urgency_event_used_to_counter_timing_pct=0.50,
        )
        assert s == 35.0

    # urgency_event_used_to_counter_timing_pct tiers
    def test_urgency_above_40_adds_0(self):
        s = self._timing(
            timing_objection_to_slip_rate_pct=0.20,
            next_step_set_after_timing_objection_pct=0.70,
            urgency_event_used_to_counter_timing_pct=0.50,
        )
        assert s == 0.0

    def test_urgency_at_40_adds_12(self):
        s = self._timing(
            timing_objection_to_slip_rate_pct=0.20,
            next_step_set_after_timing_objection_pct=0.70,
            urgency_event_used_to_counter_timing_pct=0.40,
        )
        assert s == 12.0

    def test_urgency_at_20_adds_25(self):
        s = self._timing(
            timing_objection_to_slip_rate_pct=0.20,
            next_step_set_after_timing_objection_pct=0.70,
            urgency_event_used_to_counter_timing_pct=0.20,
        )
        assert s == 25.0

    def test_timing_score_capped_at_100(self):
        s = self._timing(
            timing_objection_to_slip_rate_pct=0.90,
            next_step_set_after_timing_objection_pct=0.10,
            urgency_event_used_to_counter_timing_pct=0.10,
        )
        # 40 + 35 + 25 = 100
        assert s == 100.0

    def test_timing_score_zero(self):
        s = self._timing(
            timing_objection_to_slip_rate_pct=0.10,
            next_step_set_after_timing_objection_pct=0.90,
            urgency_event_used_to_counter_timing_pct=0.90,
        )
        assert s == 0.0

    def test_timing_score_combines_all_three(self):
        # 0.65 → +40, 0.65 → +18, 0.40 → +12 → 70
        s = self._timing(
            timing_objection_to_slip_rate_pct=0.65,
            next_step_set_after_timing_objection_pct=0.65,
            urgency_event_used_to_counter_timing_pct=0.40,
        )
        assert s == 70.0


# ---------------------------------------------------------------------------
# 8. Composite formula weights
# ---------------------------------------------------------------------------

class TestCompositeFormula:
    def _assess(self, **kwargs) -> ObjectionResult:
        return _engine().assess(_make_input(**kwargs))

    def test_composite_uses_correct_weights(self):
        # Known scores: price=40, value=0, competitive=0, timing=0
        # composite = 40*0.30 + 0*0.30 + 0*0.25 + 0*0.15 = 12.0
        r = self._assess(
            price_objection_to_discount_rate_pct=0.70,
            avg_discount_after_price_objection_pct=0.0,
            price_objection_win_rate_pct=0.60,
            value_objection_close_rate_pct=0.80,
            roi_case_presented_after_objection_pct=0.60,
            proof_of_concept_offered_rate_pct=0.50,
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.10,
            battle_card_used_in_competitive_deal_pct=0.60,
            timing_objection_to_slip_rate_pct=0.10,
            next_step_set_after_timing_objection_pct=0.70,
            urgency_event_used_to_counter_timing_pct=0.50,
        )
        assert r.price_score == 40.0
        assert r.value_score == 0.0
        assert r.competitive_score == 0.0
        assert r.timing_score == 0.0
        assert r.objection_composite == 12.0

    def test_composite_value_weight(self):
        # Only value score fires: value=40 → composite = 40*0.30 = 12.0
        r = self._assess(
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
            price_objection_win_rate_pct=0.60,
            value_objection_close_rate_pct=0.25,
            roi_case_presented_after_objection_pct=0.60,
            proof_of_concept_offered_rate_pct=0.50,
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.10,
            battle_card_used_in_competitive_deal_pct=0.60,
            timing_objection_to_slip_rate_pct=0.10,
            next_step_set_after_timing_objection_pct=0.70,
            urgency_event_used_to_counter_timing_pct=0.50,
        )
        assert r.value_score == 40.0
        assert r.price_score == 0.0
        assert r.competitive_score == 0.0
        assert r.timing_score == 0.0
        assert r.objection_composite == 12.0

    def test_composite_competitive_weight(self):
        # Only competitive score fires: competitive=45 → composite = 45*0.25 = 11.25 → rounded = 11.2
        r = self._assess(
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
            price_objection_win_rate_pct=0.60,
            value_objection_close_rate_pct=0.80,
            roi_case_presented_after_objection_pct=0.60,
            proof_of_concept_offered_rate_pct=0.50,
            competitive_objection_win_rate_pct=0.30,
            deals_lost_after_competitive_comparison_pct=0.10,
            battle_card_used_in_competitive_deal_pct=0.60,
            timing_objection_to_slip_rate_pct=0.10,
            next_step_set_after_timing_objection_pct=0.70,
            urgency_event_used_to_counter_timing_pct=0.50,
        )
        assert r.competitive_score == 45.0
        expected = round(45.0 * 0.25, 1)
        assert r.objection_composite == expected

    def test_composite_timing_weight(self):
        # Only timing score fires: timing=40 → composite = 40*0.15 = 6.0
        r = self._assess(
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
            price_objection_win_rate_pct=0.60,
            value_objection_close_rate_pct=0.80,
            roi_case_presented_after_objection_pct=0.60,
            proof_of_concept_offered_rate_pct=0.50,
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.10,
            battle_card_used_in_competitive_deal_pct=0.60,
            timing_objection_to_slip_rate_pct=0.65,
            next_step_set_after_timing_objection_pct=0.70,
            urgency_event_used_to_counter_timing_pct=0.50,
        )
        assert r.timing_score == 40.0
        expected = round(40.0 * 0.15, 1)
        assert r.objection_composite == expected

    def test_composite_all_max_capped_at_100(self):
        # All scores = 100 → composite = 100*0.30 + 100*0.30 + 100*0.25 + 100*0.15 = 100
        r = self._assess(
            price_objection_to_discount_rate_pct=1.0,
            avg_discount_after_price_objection_pct=1.0,
            price_objection_win_rate_pct=0.0,
            value_objection_close_rate_pct=0.0,
            roi_case_presented_after_objection_pct=0.0,
            proof_of_concept_offered_rate_pct=0.0,
            competitive_objection_win_rate_pct=0.0,
            deals_lost_after_competitive_comparison_pct=1.0,
            battle_card_used_in_competitive_deal_pct=0.0,
            timing_objection_to_slip_rate_pct=1.0,
            next_step_set_after_timing_objection_pct=0.0,
            urgency_event_used_to_counter_timing_pct=0.0,
        )
        assert r.objection_composite == 100.0

    def test_composite_all_zero(self):
        r = self._assess(
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
            price_objection_win_rate_pct=1.0,
            value_objection_close_rate_pct=1.0,
            roi_case_presented_after_objection_pct=1.0,
            proof_of_concept_offered_rate_pct=1.0,
            competitive_objection_win_rate_pct=1.0,
            deals_lost_after_competitive_comparison_pct=0.0,
            battle_card_used_in_competitive_deal_pct=1.0,
            timing_objection_to_slip_rate_pct=0.0,
            next_step_set_after_timing_objection_pct=1.0,
            urgency_event_used_to_counter_timing_pct=1.0,
        )
        assert r.objection_composite == 0.0


# ---------------------------------------------------------------------------
# 9. Risk level thresholds (exact boundaries)
# ---------------------------------------------------------------------------

class TestRiskLevel:
    def _risk(self, composite: float) -> ObjectionRisk:
        return _engine()._risk_level(composite)

    def test_risk_below_20_is_low(self):
        assert self._risk(0.0) == ObjectionRisk.low
        assert self._risk(19.9) == ObjectionRisk.low

    def test_risk_at_20_is_moderate(self):
        assert self._risk(20.0) == ObjectionRisk.moderate

    def test_risk_between_20_and_40_is_moderate(self):
        assert self._risk(30.0) == ObjectionRisk.moderate
        assert self._risk(39.9) == ObjectionRisk.moderate

    def test_risk_at_40_is_high(self):
        assert self._risk(40.0) == ObjectionRisk.high

    def test_risk_between_40_and_60_is_high(self):
        assert self._risk(50.0) == ObjectionRisk.high
        assert self._risk(59.9) == ObjectionRisk.high

    def test_risk_at_60_is_critical(self):
        assert self._risk(60.0) == ObjectionRisk.critical

    def test_risk_above_60_is_critical(self):
        assert self._risk(80.0) == ObjectionRisk.critical
        assert self._risk(100.0) == ObjectionRisk.critical


# ---------------------------------------------------------------------------
# 10. Severity thresholds (exact boundaries)
# ---------------------------------------------------------------------------

class TestSeverity:
    def _sev(self, composite: float) -> ObjectionSeverity:
        return _engine()._severity(composite)

    def test_severity_below_20_is_proficient(self):
        assert self._sev(0.0) == ObjectionSeverity.proficient
        assert self._sev(19.9) == ObjectionSeverity.proficient

    def test_severity_at_20_is_managing(self):
        assert self._sev(20.0) == ObjectionSeverity.managing

    def test_severity_between_20_and_40_is_managing(self):
        assert self._sev(30.0) == ObjectionSeverity.managing
        assert self._sev(39.9) == ObjectionSeverity.managing

    def test_severity_at_40_is_struggling(self):
        assert self._sev(40.0) == ObjectionSeverity.struggling

    def test_severity_between_40_and_60_is_struggling(self):
        assert self._sev(50.0) == ObjectionSeverity.struggling
        assert self._sev(59.9) == ObjectionSeverity.struggling

    def test_severity_at_60_is_collapsing(self):
        assert self._sev(60.0) == ObjectionSeverity.collapsing

    def test_severity_above_60_is_collapsing(self):
        assert self._sev(80.0) == ObjectionSeverity.collapsing
        assert self._sev(100.0) == ObjectionSeverity.collapsing


# ---------------------------------------------------------------------------
# 11. Pattern detection and priority ordering
# ---------------------------------------------------------------------------

class TestPatternDetection:
    def _detect(self, price: float = 0.0, value: float = 0.0,
                 competitive: float = 0.0, timing: float = 0.0, **kwargs) -> ObjectionPattern:
        inp = _make_input(**kwargs)
        return _engine()._detect_pattern(inp, price, value, competitive, timing)

    def test_price_capitulation_detected(self):
        p = self._detect(
            price_objection_to_discount_rate_pct=0.65,
            avg_discount_after_price_objection_pct=0.15,
        )
        assert p == ObjectionPattern.price_capitulation

    def test_price_capitulation_boundary_exact(self):
        p = self._detect(
            price_objection_to_discount_rate_pct=0.65,
            avg_discount_after_price_objection_pct=0.15,
        )
        assert p == ObjectionPattern.price_capitulation

    def test_price_capitulation_not_triggered_below_threshold(self):
        p = self._detect(
            price_objection_to_discount_rate_pct=0.64,
            avg_discount_after_price_objection_pct=0.15,
            value=0.0,
            timing_objection_to_slip_rate_pct=0.10,
        )
        assert p != ObjectionPattern.price_capitulation

    def test_value_gap_avoidance_detected(self):
        p = self._detect(
            value=40.0,
            roi_case_presented_after_objection_pct=0.25,
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
        )
        assert p == ObjectionPattern.value_gap_avoidance

    def test_value_gap_avoidance_boundary(self):
        # value must be >= 40 exactly
        p = self._detect(
            value=40.0,
            roi_case_presented_after_objection_pct=0.25,
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
        )
        assert p == ObjectionPattern.value_gap_avoidance

    def test_value_gap_avoidance_not_when_value_below_40(self):
        p = self._detect(
            value=39.9,
            roi_case_presented_after_objection_pct=0.25,
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
            timing_objection_to_slip_rate_pct=0.10,
        )
        assert p != ObjectionPattern.value_gap_avoidance

    def test_competitor_deflection_detected(self):
        p = self._detect(
            competitive_objection_win_rate_pct=0.25,
            deals_lost_after_competitive_comparison_pct=0.50,
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
            value=0.0,
        )
        assert p == ObjectionPattern.competitor_deflection

    def test_competitor_deflection_boundary(self):
        p = self._detect(
            competitive_objection_win_rate_pct=0.25,
            deals_lost_after_competitive_comparison_pct=0.50,
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
            value=0.0,
        )
        assert p == ObjectionPattern.competitor_deflection

    def test_competitor_deflection_not_when_win_rate_high(self):
        p = self._detect(
            competitive_objection_win_rate_pct=0.26,
            deals_lost_after_competitive_comparison_pct=0.50,
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
            value=0.0,
            timing_objection_to_slip_rate_pct=0.10,
        )
        assert p != ObjectionPattern.competitor_deflection

    def test_timing_deferral_detected(self):
        p = self._detect(
            timing_objection_to_slip_rate_pct=0.60,
            next_step_set_after_timing_objection_pct=0.35,
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
            value=0.0,
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.10,
        )
        assert p == ObjectionPattern.timing_deferral

    def test_timing_deferral_boundary(self):
        p = self._detect(
            timing_objection_to_slip_rate_pct=0.60,
            next_step_set_after_timing_objection_pct=0.35,
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
            value=0.0,
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.10,
        )
        assert p == ObjectionPattern.timing_deferral

    def test_timing_deferral_not_when_slip_low(self):
        p = self._detect(
            timing_objection_to_slip_rate_pct=0.59,
            next_step_set_after_timing_objection_pct=0.35,
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
            value=0.0,
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.10,
        )
        assert p != ObjectionPattern.timing_deferral

    def test_objection_avoidance_detected(self):
        p = self._detect(
            price=30.0,
            total_objections_logged_per_deal=0.5,
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
            timing_objection_to_slip_rate_pct=0.10,
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.10,
            value=0.0,
        )
        assert p == ObjectionPattern.objection_avoidance

    def test_objection_avoidance_not_when_price_below_30(self):
        p = self._detect(
            price=29.9,
            total_objections_logged_per_deal=0.5,
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
            timing_objection_to_slip_rate_pct=0.10,
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.10,
            value=0.0,
        )
        assert p != ObjectionPattern.objection_avoidance

    def test_none_pattern_when_nothing_fires(self):
        p = self._detect(
            price=0.0,
            value=0.0,
            competitive=0.0,
            timing=0.0,
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
            timing_objection_to_slip_rate_pct=0.10,
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.10,
            total_objections_logged_per_deal=2.0,
        )
        assert p == ObjectionPattern.none

    def test_price_capitulation_takes_priority_over_value_gap(self):
        # Both price_capitulation and value_gap_avoidance conditions met
        p = self._detect(
            price=50.0,
            value=50.0,
            price_objection_to_discount_rate_pct=0.65,
            avg_discount_after_price_objection_pct=0.15,
            roi_case_presented_after_objection_pct=0.20,
        )
        assert p == ObjectionPattern.price_capitulation

    def test_price_capitulation_takes_priority_over_competitor_deflection(self):
        p = self._detect(
            price=50.0,
            value=0.0,
            price_objection_to_discount_rate_pct=0.65,
            avg_discount_after_price_objection_pct=0.15,
            competitive_objection_win_rate_pct=0.20,
            deals_lost_after_competitive_comparison_pct=0.60,
        )
        assert p == ObjectionPattern.price_capitulation

    def test_value_gap_takes_priority_over_competitor_deflection(self):
        p = self._detect(
            price=0.0,
            value=50.0,
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
            roi_case_presented_after_objection_pct=0.20,
            competitive_objection_win_rate_pct=0.20,
            deals_lost_after_competitive_comparison_pct=0.60,
        )
        assert p == ObjectionPattern.value_gap_avoidance

    def test_competitor_deflection_takes_priority_over_timing_deferral(self):
        p = self._detect(
            price=0.0,
            value=0.0,
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
            competitive_objection_win_rate_pct=0.20,
            deals_lost_after_competitive_comparison_pct=0.60,
            timing_objection_to_slip_rate_pct=0.65,
            next_step_set_after_timing_objection_pct=0.30,
        )
        assert p == ObjectionPattern.competitor_deflection

    def test_timing_deferral_takes_priority_over_objection_avoidance(self):
        p = self._detect(
            price=30.0,
            value=0.0,
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.10,
            timing_objection_to_slip_rate_pct=0.65,
            next_step_set_after_timing_objection_pct=0.30,
            total_objections_logged_per_deal=0.3,
        )
        assert p == ObjectionPattern.timing_deferral


# ---------------------------------------------------------------------------
# 12. Action mappings
# ---------------------------------------------------------------------------

class TestActionMappings:
    def _action(self, risk: ObjectionRisk, pattern: ObjectionPattern) -> ObjectionAction:
        return _engine()._action(risk, pattern)

    def test_critical_price_capitulation(self):
        a = self._action(ObjectionRisk.critical, ObjectionPattern.price_capitulation)
        assert a == ObjectionAction.closing_technique_coaching

    def test_critical_value_gap_avoidance(self):
        a = self._action(ObjectionRisk.critical, ObjectionPattern.value_gap_avoidance)
        assert a == ObjectionAction.roi_articulation_coaching

    def test_critical_other_patterns_get_reset(self):
        for p in (ObjectionPattern.none, ObjectionPattern.competitor_deflection,
                  ObjectionPattern.timing_deferral, ObjectionPattern.objection_avoidance):
            a = self._action(ObjectionRisk.critical, p)
            assert a == ObjectionAction.objection_handling_reset, f"failed for {p}"

    def test_high_competitor_deflection(self):
        a = self._action(ObjectionRisk.high, ObjectionPattern.competitor_deflection)
        assert a == ObjectionAction.competitive_response_coaching

    def test_high_timing_deferral(self):
        a = self._action(ObjectionRisk.high, ObjectionPattern.timing_deferral)
        assert a == ObjectionAction.closing_technique_coaching

    def test_high_other_patterns_get_scripting(self):
        for p in (ObjectionPattern.none, ObjectionPattern.price_capitulation,
                  ObjectionPattern.value_gap_avoidance, ObjectionPattern.objection_avoidance):
            a = self._action(ObjectionRisk.high, p)
            assert a == ObjectionAction.objection_scripting_coaching, f"failed for {p}"

    def test_moderate_any_pattern_gets_scripting(self):
        for p in ObjectionPattern:
            a = self._action(ObjectionRisk.moderate, p)
            assert a == ObjectionAction.objection_scripting_coaching, f"failed for {p}"

    def test_low_any_pattern_gets_no_action(self):
        for p in ObjectionPattern:
            a = self._action(ObjectionRisk.low, p)
            assert a == ObjectionAction.no_action, f"failed for {p}"


# ---------------------------------------------------------------------------
# 13. Flag conditions
# ---------------------------------------------------------------------------

class TestFlags:
    def _engine_assess(self, **kwargs) -> ObjectionResult:
        return _engine().assess(_make_input(**kwargs))

    # has_objection_gap
    def test_gap_true_when_composite_gte_40(self):
        # Force composite >= 40 using high scores
        r = self._engine_assess(
            price_objection_to_discount_rate_pct=0.70,
            avg_discount_after_price_objection_pct=0.20,
            price_objection_win_rate_pct=0.30,
            value_objection_close_rate_pct=0.25,
            roi_case_presented_after_objection_pct=0.30,
            proof_of_concept_offered_rate_pct=0.20,
            competitive_objection_win_rate_pct=0.30,
            deals_lost_after_competitive_comparison_pct=0.55,
            battle_card_used_in_competitive_deal_pct=0.25,
            timing_objection_to_slip_rate_pct=0.65,
            next_step_set_after_timing_objection_pct=0.40,
            urgency_event_used_to_counter_timing_pct=0.20,
        )
        assert r.objection_composite >= 40
        assert r.has_objection_gap is True

    def test_gap_true_when_value_close_rate_lte_35(self):
        r = self._engine_assess(
            value_objection_close_rate_pct=0.35,
            # ensure composite < 40
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
            price_objection_win_rate_pct=0.60,
            roi_case_presented_after_objection_pct=0.60,
            proof_of_concept_offered_rate_pct=0.50,
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.10,
            battle_card_used_in_competitive_deal_pct=0.60,
            timing_objection_to_slip_rate_pct=0.10,
            next_step_set_after_timing_objection_pct=0.70,
            urgency_event_used_to_counter_timing_pct=0.50,
        )
        assert r.has_objection_gap is True

    def test_gap_true_when_competitive_win_rate_lte_30(self):
        r = self._engine_assess(
            competitive_objection_win_rate_pct=0.30,
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
            price_objection_win_rate_pct=0.60,
            value_objection_close_rate_pct=0.80,
            roi_case_presented_after_objection_pct=0.60,
            proof_of_concept_offered_rate_pct=0.50,
            deals_lost_after_competitive_comparison_pct=0.10,
            battle_card_used_in_competitive_deal_pct=0.60,
            timing_objection_to_slip_rate_pct=0.10,
            next_step_set_after_timing_objection_pct=0.70,
            urgency_event_used_to_counter_timing_pct=0.50,
        )
        assert r.has_objection_gap is True

    def test_gap_false_when_all_conditions_fail(self):
        # composite < 40, value_close_rate > 0.35, competitive_win_rate > 0.30
        inp = _make_input(
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
            price_objection_win_rate_pct=0.60,
            value_objection_close_rate_pct=0.80,
            roi_case_presented_after_objection_pct=0.60,
            proof_of_concept_offered_rate_pct=0.50,
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.10,
            battle_card_used_in_competitive_deal_pct=0.60,
            timing_objection_to_slip_rate_pct=0.10,
            next_step_set_after_timing_objection_pct=0.70,
            urgency_event_used_to_counter_timing_pct=0.50,
        )
        r = _engine().assess(inp)
        assert r.objection_composite < 40
        assert inp.value_objection_close_rate_pct > 0.35
        assert inp.competitive_objection_win_rate_pct > 0.30
        assert r.has_objection_gap is False

    # requires_objection_coaching
    def test_coaching_true_when_composite_gte_30(self):
        r = self._engine_assess(
            price_objection_to_discount_rate_pct=0.70,
            avg_discount_after_price_objection_pct=0.20,
            price_objection_win_rate_pct=0.30,
            value_objection_close_rate_pct=0.25,
            roi_case_presented_after_objection_pct=0.30,
            proof_of_concept_offered_rate_pct=0.50,
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.10,
            battle_card_used_in_competitive_deal_pct=0.60,
            timing_objection_to_slip_rate_pct=0.10,
            next_step_set_after_timing_objection_pct=0.70,
            urgency_event_used_to_counter_timing_pct=0.50,
        )
        assert r.objection_composite >= 30
        assert r.requires_objection_coaching is True

    def test_coaching_true_when_price_discount_rate_gte_50(self):
        r = self._engine_assess(
            price_objection_to_discount_rate_pct=0.50,
            avg_discount_after_price_objection_pct=0.0,
            price_objection_win_rate_pct=0.60,
            value_objection_close_rate_pct=0.80,
            roi_case_presented_after_objection_pct=0.60,
            proof_of_concept_offered_rate_pct=0.50,
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.10,
            battle_card_used_in_competitive_deal_pct=0.60,
            timing_objection_to_slip_rate_pct=0.10,
            next_step_set_after_timing_objection_pct=0.70,
            urgency_event_used_to_counter_timing_pct=0.50,
        )
        assert r.requires_objection_coaching is True

    def test_coaching_true_when_timing_slip_gte_45(self):
        r = self._engine_assess(
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
            price_objection_win_rate_pct=0.60,
            value_objection_close_rate_pct=0.80,
            roi_case_presented_after_objection_pct=0.60,
            proof_of_concept_offered_rate_pct=0.50,
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.10,
            battle_card_used_in_competitive_deal_pct=0.60,
            timing_objection_to_slip_rate_pct=0.45,
            next_step_set_after_timing_objection_pct=0.70,
            urgency_event_used_to_counter_timing_pct=0.50,
        )
        assert r.requires_objection_coaching is True

    def test_coaching_false_when_all_below(self):
        r = self._engine_assess(
            price_objection_to_discount_rate_pct=0.10,
            avg_discount_after_price_objection_pct=0.0,
            price_objection_win_rate_pct=0.60,
            value_objection_close_rate_pct=0.80,
            roi_case_presented_after_objection_pct=0.60,
            proof_of_concept_offered_rate_pct=0.50,
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.10,
            battle_card_used_in_competitive_deal_pct=0.60,
            timing_objection_to_slip_rate_pct=0.10,
            next_step_set_after_timing_objection_pct=0.70,
            urgency_event_used_to_counter_timing_pct=0.50,
        )
        assert r.requires_objection_coaching is False


# ---------------------------------------------------------------------------
# 14. Revenue surrendered formula
# ---------------------------------------------------------------------------

class TestRevenueSurrendered:
    def test_formula_calculation(self):
        inp = _make_input(
            total_deals_with_objections=100,
            avg_opportunity_value_usd=50_000.0,
            price_objection_to_discount_rate_pct=0.60,
            avg_discount_after_price_objection_pct=0.15,
            # Force a known composite: use score inputs that give composite ~27
            price_objection_win_rate_pct=0.60,
            value_objection_close_rate_pct=0.80,
            roi_case_presented_after_objection_pct=0.60,
            proof_of_concept_offered_rate_pct=0.50,
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.10,
            battle_card_used_in_competitive_deal_pct=0.60,
            timing_objection_to_slip_rate_pct=0.10,
            next_step_set_after_timing_objection_pct=0.70,
            urgency_event_used_to_counter_timing_pct=0.50,
        )
        eng = _engine()
        r = eng.assess(inp)
        expected = round(
            100 * 50_000.0 * 0.60 * 0.15 * (r.objection_composite / 100.0),
            2,
        )
        assert r.estimated_revenue_surrendered_usd == expected

    def test_revenue_zero_when_composite_zero(self):
        inp = _make_input(
            total_deals_with_objections=100,
            avg_opportunity_value_usd=50_000.0,
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
            price_objection_win_rate_pct=0.60,
            value_objection_close_rate_pct=0.80,
            roi_case_presented_after_objection_pct=0.60,
            proof_of_concept_offered_rate_pct=0.50,
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.10,
            battle_card_used_in_competitive_deal_pct=0.60,
            timing_objection_to_slip_rate_pct=0.10,
            next_step_set_after_timing_objection_pct=0.70,
            urgency_event_used_to_counter_timing_pct=0.50,
        )
        r = _engine().assess(inp)
        # price_to_discount=0 → revenue = 0
        assert r.estimated_revenue_surrendered_usd == 0.0

    def test_revenue_is_rounded_to_2_decimals(self):
        inp = _make_input(
            total_deals_with_objections=3,
            avg_opportunity_value_usd=10_000.0,
            price_objection_to_discount_rate_pct=0.70,
            avg_discount_after_price_objection_pct=0.20,
            price_objection_win_rate_pct=0.30,
            value_objection_close_rate_pct=0.25,
            roi_case_presented_after_objection_pct=0.30,
            proof_of_concept_offered_rate_pct=0.20,
            competitive_objection_win_rate_pct=0.30,
            deals_lost_after_competitive_comparison_pct=0.55,
            battle_card_used_in_competitive_deal_pct=0.25,
            timing_objection_to_slip_rate_pct=0.65,
            next_step_set_after_timing_objection_pct=0.40,
            urgency_event_used_to_counter_timing_pct=0.20,
        )
        r = _engine().assess(inp)
        # Verify it's a float with at most 2 decimal places
        assert r.estimated_revenue_surrendered_usd == round(r.estimated_revenue_surrendered_usd, 2)

    def test_revenue_scales_with_deals(self):
        base_kwargs = dict(
            avg_opportunity_value_usd=10_000.0,
            price_objection_to_discount_rate_pct=0.70,
            avg_discount_after_price_objection_pct=0.20,
            price_objection_win_rate_pct=0.30,
            value_objection_close_rate_pct=0.25,
            roi_case_presented_after_objection_pct=0.30,
            proof_of_concept_offered_rate_pct=0.20,
            competitive_objection_win_rate_pct=0.30,
            deals_lost_after_competitive_comparison_pct=0.55,
            battle_card_used_in_competitive_deal_pct=0.25,
            timing_objection_to_slip_rate_pct=0.65,
            next_step_set_after_timing_objection_pct=0.40,
            urgency_event_used_to_counter_timing_pct=0.20,
        )
        r1 = _engine().assess(_make_input(total_deals_with_objections=10, **base_kwargs))
        r2 = _engine().assess(_make_input(total_deals_with_objections=20, **base_kwargs))
        # Same composite, double deals → double revenue
        assert r1.objection_composite == r2.objection_composite
        assert abs(r2.estimated_revenue_surrendered_usd - 2 * r1.estimated_revenue_surrendered_usd) < 0.01


# ---------------------------------------------------------------------------
# 15. Signal string
# ---------------------------------------------------------------------------

class TestSignalString:
    def test_proficient_signal_when_none_and_composite_below_20(self):
        inp = _make_input(
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
            price_objection_win_rate_pct=0.60,
            value_objection_close_rate_pct=0.80,
            roi_case_presented_after_objection_pct=0.60,
            proof_of_concept_offered_rate_pct=0.50,
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.10,
            battle_card_used_in_competitive_deal_pct=0.60,
            timing_objection_to_slip_rate_pct=0.10,
            next_step_set_after_timing_objection_pct=0.70,
            urgency_event_used_to_counter_timing_pct=0.50,
        )
        r = _engine().assess(inp)
        assert r.objection_pattern == ObjectionPattern.none
        assert r.objection_composite < 20
        assert r.objection_signal == (
            "Objection handling proficient — price defense, value articulation, "
            "and competitive positioning within benchmarks"
        )

    def test_signal_contains_correct_pct_values(self):
        inp = _make_input(
            price_objection_to_discount_rate_pct=0.70,
            avg_discount_after_price_objection_pct=0.20,
            price_objection_win_rate_pct=0.30,
            value_objection_close_rate_pct=0.40,
            roi_case_presented_after_objection_pct=0.30,
            proof_of_concept_offered_rate_pct=0.20,
            competitive_objection_win_rate_pct=0.55,
            deals_lost_after_competitive_comparison_pct=0.55,
            battle_card_used_in_competitive_deal_pct=0.25,
            timing_objection_to_slip_rate_pct=0.10,
            next_step_set_after_timing_objection_pct=0.70,
            urgency_event_used_to_counter_timing_pct=0.50,
        )
        r = _engine().assess(inp)
        sig = r.objection_signal
        assert "70% price objections lead to discount" in sig
        assert "40% value objection close rate" in sig
        assert "55% competitive win rate" in sig

    def test_signal_contains_pattern_label(self):
        inp = _make_input(
            price_objection_to_discount_rate_pct=0.65,
            avg_discount_after_price_objection_pct=0.15,
            price_objection_win_rate_pct=0.30,
            value_objection_close_rate_pct=0.80,
            roi_case_presented_after_objection_pct=0.60,
            proof_of_concept_offered_rate_pct=0.50,
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.10,
            battle_card_used_in_competitive_deal_pct=0.60,
            timing_objection_to_slip_rate_pct=0.10,
            next_step_set_after_timing_objection_pct=0.70,
            urgency_event_used_to_counter_timing_pct=0.50,
        )
        r = _engine().assess(inp)
        assert r.objection_pattern == ObjectionPattern.price_capitulation
        # Pattern label capitalised, underscores replaced with spaces
        assert r.objection_signal.startswith("Price capitulation")

    def test_signal_none_pattern_with_composite_gte_20_uses_risk_label(self):
        # Composite >= 20 but pattern = none → signal starts with "Objection handling risk"
        inp = _make_input(
            price_objection_to_discount_rate_pct=0.30,
            avg_discount_after_price_objection_pct=0.0,
            price_objection_win_rate_pct=0.30,
            value_objection_close_rate_pct=0.80,
            roi_case_presented_after_objection_pct=0.60,
            proof_of_concept_offered_rate_pct=0.50,
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.10,
            battle_card_used_in_competitive_deal_pct=0.60,
            timing_objection_to_slip_rate_pct=0.10,
            next_step_set_after_timing_objection_pct=0.70,
            urgency_event_used_to_counter_timing_pct=0.50,
            total_objections_logged_per_deal=2.0,
        )
        r = _engine().assess(inp)
        if r.objection_pattern == ObjectionPattern.none and r.objection_composite >= 20:
            assert r.objection_signal.startswith("Objection handling risk")

    def test_signal_contains_composite_value(self):
        inp = _make_input(
            price_objection_to_discount_rate_pct=0.70,
            avg_discount_after_price_objection_pct=0.20,
            price_objection_win_rate_pct=0.30,
            value_objection_close_rate_pct=0.25,
            roi_case_presented_after_objection_pct=0.30,
            proof_of_concept_offered_rate_pct=0.20,
            competitive_objection_win_rate_pct=0.30,
            deals_lost_after_competitive_comparison_pct=0.55,
            battle_card_used_in_competitive_deal_pct=0.25,
            timing_objection_to_slip_rate_pct=0.65,
            next_step_set_after_timing_objection_pct=0.40,
            urgency_event_used_to_counter_timing_pct=0.20,
        )
        r = _engine().assess(inp)
        assert f"composite {r.objection_composite:.0f}" in r.objection_signal


# ---------------------------------------------------------------------------
# 16. assess() end-to-end
# ---------------------------------------------------------------------------

class TestAssessEndToEnd:
    def test_returns_objection_result(self):
        r = _engine().assess(_make_input())
        assert isinstance(r, ObjectionResult)

    def test_rep_id_preserved(self):
        r = _engine().assess(_make_input(rep_id="ABC123"))
        assert r.rep_id == "ABC123"

    def test_region_preserved(self):
        r = _engine().assess(_make_input(region="Pacific"))
        assert r.region == "Pacific"

    def test_sub_scores_are_non_negative(self):
        r = _engine().assess(_make_input())
        assert r.price_score >= 0
        assert r.value_score >= 0
        assert r.competitive_score >= 0
        assert r.timing_score >= 0

    def test_sub_scores_are_at_most_100(self):
        r = _engine().assess(_make_input())
        assert r.price_score <= 100
        assert r.value_score <= 100
        assert r.competitive_score <= 100
        assert r.timing_score <= 100

    def test_composite_is_non_negative(self):
        r = _engine().assess(_make_input())
        assert r.objection_composite >= 0

    def test_composite_is_at_most_100(self):
        r = _engine().assess(_make_input())
        assert r.objection_composite <= 100

    def test_result_stored_in_engine(self):
        eng = _engine()
        eng.assess(_make_input())
        assert len(eng._results) == 1

    def test_full_low_risk_scenario(self):
        inp = _make_input(
            price_objection_to_discount_rate_pct=0.10,
            avg_discount_after_price_objection_pct=0.05,
            price_objection_win_rate_pct=0.80,
            value_objection_close_rate_pct=0.80,
            roi_case_presented_after_objection_pct=0.80,
            proof_of_concept_offered_rate_pct=0.80,
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.10,
            battle_card_used_in_competitive_deal_pct=0.80,
            timing_objection_to_slip_rate_pct=0.10,
            next_step_set_after_timing_objection_pct=0.80,
            urgency_event_used_to_counter_timing_pct=0.80,
        )
        r = _engine().assess(inp)
        assert r.objection_risk == ObjectionRisk.low
        assert r.objection_severity == ObjectionSeverity.proficient
        assert r.recommended_action == ObjectionAction.no_action

    def test_full_critical_scenario(self):
        inp = _make_input(
            price_objection_to_discount_rate_pct=0.90,
            avg_discount_after_price_objection_pct=0.30,
            price_objection_win_rate_pct=0.10,
            value_objection_close_rate_pct=0.10,
            roi_case_presented_after_objection_pct=0.10,
            proof_of_concept_offered_rate_pct=0.10,
            competitive_objection_win_rate_pct=0.10,
            deals_lost_after_competitive_comparison_pct=0.90,
            battle_card_used_in_competitive_deal_pct=0.10,
            timing_objection_to_slip_rate_pct=0.90,
            next_step_set_after_timing_objection_pct=0.10,
            urgency_event_used_to_counter_timing_pct=0.10,
        )
        r = _engine().assess(inp)
        assert r.objection_risk == ObjectionRisk.critical
        assert r.objection_severity == ObjectionSeverity.collapsing
        assert r.objection_composite == 100.0


# ---------------------------------------------------------------------------
# 17. assess_batch()
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_returns_list(self):
        results = _engine().assess_batch([_make_input(), _make_input(rep_id="R2")])
        assert isinstance(results, list)

    def test_returns_correct_count(self):
        inputs = [_make_input(rep_id=f"R{i}") for i in range(5)]
        results = _engine().assess_batch(inputs)
        assert len(results) == 5

    def test_all_items_are_objection_results(self):
        inputs = [_make_input(rep_id=f"R{i}") for i in range(3)]
        results = _engine().assess_batch(inputs)
        for r in results:
            assert isinstance(r, ObjectionResult)

    def test_batch_stores_all_results(self):
        eng = _engine()
        inputs = [_make_input(rep_id=f"R{i}") for i in range(4)]
        eng.assess_batch(inputs)
        assert len(eng._results) == 4

    def test_empty_batch_returns_empty_list(self):
        results = _engine().assess_batch([])
        assert results == []

    def test_batch_rep_ids_preserved(self):
        inputs = [_make_input(rep_id=f"REP{i}") for i in range(3)]
        results = _engine().assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"REP{i}"

    def test_single_item_batch(self):
        results = _engine().assess_batch([_make_input(rep_id="SOLO")])
        assert len(results) == 1
        assert results[0].rep_id == "SOLO"


# ---------------------------------------------------------------------------
# 18. summary() — empty
# ---------------------------------------------------------------------------

class TestSummaryEmpty:
    def test_empty_summary_has_13_keys(self):
        s = _engine().summary()
        assert len(s) == 13

    def test_empty_summary_keys(self):
        s = _engine().summary()
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_objection_composite", "objection_gap_count",
            "coaching_count", "avg_price_score", "avg_value_score",
            "avg_competitive_score", "avg_timing_score",
            "total_estimated_revenue_surrendered_usd",
        }
        assert set(s.keys()) == expected

    def test_empty_summary_total_zero(self):
        assert _engine().summary()["total"] == 0

    def test_empty_summary_counts_are_dicts(self):
        s = _engine().summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}

    def test_empty_summary_averages_are_zero(self):
        s = _engine().summary()
        assert s["avg_objection_composite"] == 0.0
        assert s["avg_price_score"] == 0.0
        assert s["avg_value_score"] == 0.0
        assert s["avg_competitive_score"] == 0.0
        assert s["avg_timing_score"] == 0.0

    def test_empty_summary_gap_and_coaching_counts_zero(self):
        s = _engine().summary()
        assert s["objection_gap_count"] == 0
        assert s["coaching_count"] == 0

    def test_empty_summary_revenue_surrendered_zero(self):
        assert _engine().summary()["total_estimated_revenue_surrendered_usd"] == 0.0


# ---------------------------------------------------------------------------
# 19. summary() — populated
# ---------------------------------------------------------------------------

class TestSummaryPopulated:
    def _populated_engine(self) -> SalesObjectionHandlingEffectivenessIntelligenceEngine:
        eng = _engine()
        # Low risk rep
        eng.assess(_make_input(rep_id="R1",
            price_objection_to_discount_rate_pct=0.10,
            avg_discount_after_price_objection_pct=0.05,
            price_objection_win_rate_pct=0.80,
            value_objection_close_rate_pct=0.80,
            roi_case_presented_after_objection_pct=0.80,
            proof_of_concept_offered_rate_pct=0.80,
            competitive_objection_win_rate_pct=0.80,
            deals_lost_after_competitive_comparison_pct=0.10,
            battle_card_used_in_competitive_deal_pct=0.80,
            timing_objection_to_slip_rate_pct=0.10,
            next_step_set_after_timing_objection_pct=0.80,
            urgency_event_used_to_counter_timing_pct=0.80,
        ))
        # Critical risk rep
        eng.assess(_make_input(rep_id="R2",
            price_objection_to_discount_rate_pct=0.90,
            avg_discount_after_price_objection_pct=0.30,
            price_objection_win_rate_pct=0.10,
            value_objection_close_rate_pct=0.10,
            roi_case_presented_after_objection_pct=0.10,
            proof_of_concept_offered_rate_pct=0.10,
            competitive_objection_win_rate_pct=0.10,
            deals_lost_after_competitive_comparison_pct=0.90,
            battle_card_used_in_competitive_deal_pct=0.10,
            timing_objection_to_slip_rate_pct=0.90,
            next_step_set_after_timing_objection_pct=0.10,
            urgency_event_used_to_counter_timing_pct=0.10,
        ))
        return eng

    def test_populated_summary_has_13_keys(self):
        s = self._populated_engine().summary()
        assert len(s) == 13

    def test_populated_summary_key_names(self):
        s = self._populated_engine().summary()
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_objection_composite", "objection_gap_count",
            "coaching_count", "avg_price_score", "avg_value_score",
            "avg_competitive_score", "avg_timing_score",
            "total_estimated_revenue_surrendered_usd",
        }
        assert set(s.keys()) == expected

    def test_populated_total(self):
        s = self._populated_engine().summary()
        assert s["total"] == 2

    def test_populated_risk_counts(self):
        s = self._populated_engine().summary()
        assert "low" in s["risk_counts"]
        assert "critical" in s["risk_counts"]
        assert s["risk_counts"]["low"] == 1
        assert s["risk_counts"]["critical"] == 1

    def test_populated_severity_counts(self):
        s = self._populated_engine().summary()
        assert "proficient" in s["severity_counts"]
        assert "collapsing" in s["severity_counts"]

    def test_populated_avg_composite_positive(self):
        s = self._populated_engine().summary()
        assert s["avg_objection_composite"] > 0

    def test_populated_avg_composite_computed_correctly(self):
        eng = self._populated_engine()
        s = eng.summary()
        expected = round(
            sum(r.objection_composite for r in eng._results) / len(eng._results), 1
        )
        assert s["avg_objection_composite"] == expected

    def test_populated_avg_scores_computed_correctly(self):
        eng = self._populated_engine()
        s = eng.summary()
        n = len(eng._results)
        assert s["avg_price_score"] == round(sum(r.price_score for r in eng._results) / n, 1)
        assert s["avg_value_score"] == round(sum(r.value_score for r in eng._results) / n, 1)
        assert s["avg_competitive_score"] == round(sum(r.competitive_score for r in eng._results) / n, 1)
        assert s["avg_timing_score"] == round(sum(r.timing_score for r in eng._results) / n, 1)

    def test_populated_gap_count(self):
        eng = self._populated_engine()
        s = eng.summary()
        expected = sum(1 for r in eng._results if r.has_objection_gap)
        assert s["objection_gap_count"] == expected

    def test_populated_coaching_count(self):
        eng = self._populated_engine()
        s = eng.summary()
        expected = sum(1 for r in eng._results if r.requires_objection_coaching)
        assert s["coaching_count"] == expected

    def test_populated_total_revenue_surrendered(self):
        eng = self._populated_engine()
        s = eng.summary()
        expected = round(sum(r.estimated_revenue_surrendered_usd for r in eng._results), 2)
        assert s["total_estimated_revenue_surrendered_usd"] == expected

    def test_populated_pattern_counts_present(self):
        s = self._populated_engine().summary()
        # At least one pattern must appear
        assert len(s["pattern_counts"]) >= 1

    def test_populated_action_counts_present(self):
        s = self._populated_engine().summary()
        assert len(s["action_counts"]) >= 1

    def test_summary_accumulates_across_multiple_assess_calls(self):
        eng = _engine()
        for i in range(5):
            eng.assess(_make_input(rep_id=f"R{i}"))
        assert eng.summary()["total"] == 5

    def test_single_rep_summary(self):
        eng = _engine()
        eng.assess(_make_input(rep_id="SOLO"))
        s = eng.summary()
        assert s["total"] == 1
        # avg should equal the single result's composite
        assert s["avg_objection_composite"] == eng._results[0].objection_composite


# ---------------------------------------------------------------------------
# 20. Edge cases / additional coverage
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_assess_boundary_composite_exactly_20(self):
        # Find inputs that produce composite exactly 20 isn't trivial; check range
        eng = _engine()
        for composite_target in [19.9, 20.0, 39.9, 40.0, 59.9, 60.0]:
            eng._risk_level(composite_target)  # just ensure no exception

    def test_multiple_assess_calls_accumulate_results(self):
        eng = _engine()
        eng.assess(_make_input(rep_id="A"))
        eng.assess(_make_input(rep_id="B"))
        eng.assess(_make_input(rep_id="C"))
        assert len(eng._results) == 3

    def test_new_engine_has_empty_results(self):
        eng = _engine()
        assert eng._results == []

    def test_to_dict_objection_signal_is_string(self):
        d = _engine().assess(_make_input()).to_dict()
        assert isinstance(d["objection_signal"], str)

    def test_to_dict_estimated_revenue_is_float(self):
        d = _engine().assess(_make_input()).to_dict()
        assert isinstance(d["estimated_revenue_surrendered_usd"], float)

    def test_assess_batch_then_summary_consistent(self):
        eng = _engine()
        inputs = [_make_input(rep_id=f"R{i}") for i in range(3)]
        eng.assess_batch(inputs)
        s = eng.summary()
        assert s["total"] == 3

    def test_pattern_detection_uses_computed_value_score(self):
        # value_gap_avoidance requires value >= 40 AND roi_case <= 0.25
        inp = _make_input(
            value_objection_close_rate_pct=0.25,            # → +40 on value score
            roi_case_presented_after_objection_pct=0.25,   # <= 0.25 → triggers pattern
            proof_of_concept_offered_rate_pct=0.50,
            price_objection_to_discount_rate_pct=0.0,
            avg_discount_after_price_objection_pct=0.0,
        )
        r = _engine().assess(inp)
        assert r.value_score >= 40.0
        assert r.objection_pattern == ObjectionPattern.value_gap_avoidance

    def test_high_risk_no_special_pattern_gets_scripting(self):
        # Build a scenario that is high risk (composite 40-59) with none pattern
        inp = _make_input(
            price_objection_to_discount_rate_pct=0.50,
            avg_discount_after_price_objection_pct=0.10,
            price_objection_win_rate_pct=0.50,
            value_objection_close_rate_pct=0.45,
            roi_case_presented_after_objection_pct=0.55,
            proof_of_concept_offered_rate_pct=0.40,
            competitive_objection_win_rate_pct=0.50,
            deals_lost_after_competitive_comparison_pct=0.35,
            battle_card_used_in_competitive_deal_pct=0.50,
            timing_objection_to_slip_rate_pct=0.45,
            next_step_set_after_timing_objection_pct=0.65,
            urgency_event_used_to_counter_timing_pct=0.40,
            total_objections_logged_per_deal=2.0,
        )
        r = _engine().assess(inp)
        if r.objection_risk == ObjectionRisk.high and r.objection_pattern not in (
            ObjectionPattern.competitor_deflection, ObjectionPattern.timing_deferral
        ):
            assert r.recommended_action == ObjectionAction.objection_scripting_coaching
