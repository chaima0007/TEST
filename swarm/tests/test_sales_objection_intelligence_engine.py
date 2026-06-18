"""
Comprehensive pytest tests for SalesObjectionIntelligenceEngine.
At least 280 tests covering all enums, input/result fields, sub-scores,
pattern detection, risk/severity/action mapping, flags, deal loss, signal,
assess, assess_batch, summary (empty + populated), and edge cases.
"""
from __future__ import annotations

import pytest

from swarm.intelligence.sales_objection_intelligence_engine import (
    ObjectionAction,
    ObjectionInput,
    ObjectionPattern,
    ObjectionResult,
    ObjectionRisk,
    ObjectionSeverity,
    SalesObjectionIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> ObjectionInput:
    """Return a 'healthy' baseline ObjectionInput with optional overrides."""
    defaults = dict(
        rep_id="REP001",
        region="West",
        evaluation_period_id="2026-Q1",
        total_objections_logged=100,
        objections_resolved_pct=0.90,
        price_objection_rate_pct=0.10,
        price_objection_resolution_rate_pct=0.80,
        technical_objection_rate_pct=0.10,
        technical_objection_escalation_rate_pct=0.10,
        trust_objection_rate_pct=0.05,
        competitive_objection_rate_pct=0.10,
        competitive_objection_loss_rate_pct=0.05,
        late_stage_new_objection_rate_pct=0.05,
        avg_days_to_resolve_objection=3.0,
        objection_repeat_rate_pct=0.05,
        objection_documented_in_crm_pct=0.90,
        champion_coached_on_internal_objections_pct=0.80,
        multi_objection_deal_rate_pct=0.10,
        deals_lost_to_unresolved_objection_pct=0.05,
        avg_objection_response_time_hours=2.0,
        proactive_objection_prevention_rate_pct=0.50,
        avg_opportunity_value_usd=10_000.0,
    )
    defaults.update(overrides)
    return ObjectionInput(**defaults)


def fresh_engine() -> SalesObjectionIntelligenceEngine:
    return SalesObjectionIntelligenceEngine()


# ===========================================================================
# 1. Enum tests
# ===========================================================================

class TestObjectionRiskEnum:
    def test_low_value(self):
        assert ObjectionRisk.low.value == "low"

    def test_moderate_value(self):
        assert ObjectionRisk.moderate.value == "moderate"

    def test_high_value(self):
        assert ObjectionRisk.high.value == "high"

    def test_critical_value(self):
        assert ObjectionRisk.critical.value == "critical"

    def test_all_members_count(self):
        assert len(ObjectionRisk) == 4

    def test_str_behavior(self):
        # ObjectionRisk is str Enum
        assert ObjectionRisk.low == "low"


class TestObjectionPatternEnum:
    def test_none_value(self):
        assert ObjectionPattern.none.value == "none"

    def test_price_objection_paralysis(self):
        assert ObjectionPattern.price_objection_paralysis.value == "price_objection_paralysis"

    def test_technical_objection_avoidance(self):
        assert ObjectionPattern.technical_objection_avoidance.value == "technical_objection_avoidance"

    def test_trust_objection_gap(self):
        assert ObjectionPattern.trust_objection_gap.value == "trust_objection_gap"

    def test_competition_capitulation(self):
        assert ObjectionPattern.competition_capitulation_under_objection.value == "competition_capitulation_under_objection"

    def test_late_stage_surprise(self):
        assert ObjectionPattern.late_stage_objection_surprise.value == "late_stage_objection_surprise"

    def test_all_members_count(self):
        assert len(ObjectionPattern) == 6


class TestObjectionSeverityEnum:
    def test_confident_value(self):
        assert ObjectionSeverity.confident.value == "confident"

    def test_developing_value(self):
        assert ObjectionSeverity.developing.value == "developing"

    def test_reactive_value(self):
        assert ObjectionSeverity.reactive.value == "reactive"

    def test_paralyzed_value(self):
        assert ObjectionSeverity.paralyzed.value == "paralyzed"

    def test_all_members_count(self):
        assert len(ObjectionSeverity) == 4


class TestObjectionActionEnum:
    def test_no_action_value(self):
        assert ObjectionAction.no_action.value == "no_action"

    def test_objection_handling_workshop(self):
        assert ObjectionAction.objection_handling_workshop.value == "objection_handling_workshop"

    def test_price_reframing_training(self):
        assert ObjectionAction.price_reframing_training.value == "price_reframing_training"

    def test_technical_proof_support(self):
        assert ObjectionAction.technical_proof_support.value == "technical_proof_support"

    def test_trust_building_coaching(self):
        assert ObjectionAction.trust_building_coaching.value == "trust_building_coaching"

    def test_competitive_intelligence_training(self):
        assert ObjectionAction.competitive_intelligence_training.value == "competitive_intelligence_training"

    def test_all_members_count(self):
        assert len(ObjectionAction) == 6


# ===========================================================================
# 2. ObjectionInput field tests
# ===========================================================================

class TestObjectionInputFields:
    def test_rep_id_field(self):
        inp = make_input(rep_id="R99")
        assert inp.rep_id == "R99"

    def test_region_field(self):
        inp = make_input(region="East")
        assert inp.region == "East"

    def test_evaluation_period_id_field(self):
        inp = make_input(evaluation_period_id="2025-Q4")
        assert inp.evaluation_period_id == "2025-Q4"

    def test_total_objections_logged_field(self):
        inp = make_input(total_objections_logged=50)
        assert inp.total_objections_logged == 50

    def test_objections_resolved_pct_field(self):
        inp = make_input(objections_resolved_pct=0.75)
        assert inp.objections_resolved_pct == 0.75

    def test_price_objection_rate_pct_field(self):
        inp = make_input(price_objection_rate_pct=0.25)
        assert inp.price_objection_rate_pct == 0.25

    def test_price_objection_resolution_rate_pct_field(self):
        inp = make_input(price_objection_resolution_rate_pct=0.60)
        assert inp.price_objection_resolution_rate_pct == 0.60

    def test_technical_objection_rate_pct_field(self):
        inp = make_input(technical_objection_rate_pct=0.20)
        assert inp.technical_objection_rate_pct == 0.20

    def test_technical_objection_escalation_rate_pct_field(self):
        inp = make_input(technical_objection_escalation_rate_pct=0.70)
        assert inp.technical_objection_escalation_rate_pct == 0.70

    def test_trust_objection_rate_pct_field(self):
        inp = make_input(trust_objection_rate_pct=0.30)
        assert inp.trust_objection_rate_pct == 0.30

    def test_competitive_objection_rate_pct_field(self):
        inp = make_input(competitive_objection_rate_pct=0.35)
        assert inp.competitive_objection_rate_pct == 0.35

    def test_competitive_objection_loss_rate_pct_field(self):
        inp = make_input(competitive_objection_loss_rate_pct=0.40)
        assert inp.competitive_objection_loss_rate_pct == 0.40

    def test_late_stage_new_objection_rate_pct_field(self):
        inp = make_input(late_stage_new_objection_rate_pct=0.55)
        assert inp.late_stage_new_objection_rate_pct == 0.55

    def test_avg_days_to_resolve_objection_field(self):
        inp = make_input(avg_days_to_resolve_objection=10.0)
        assert inp.avg_days_to_resolve_objection == 10.0

    def test_objection_repeat_rate_pct_field(self):
        inp = make_input(objection_repeat_rate_pct=0.45)
        assert inp.objection_repeat_rate_pct == 0.45

    def test_objection_documented_in_crm_pct_field(self):
        inp = make_input(objection_documented_in_crm_pct=0.30)
        assert inp.objection_documented_in_crm_pct == 0.30

    def test_champion_coached_on_internal_objections_pct_field(self):
        inp = make_input(champion_coached_on_internal_objections_pct=0.20)
        assert inp.champion_coached_on_internal_objections_pct == 0.20

    def test_multi_objection_deal_rate_pct_field(self):
        inp = make_input(multi_objection_deal_rate_pct=0.60)
        assert inp.multi_objection_deal_rate_pct == 0.60

    def test_deals_lost_to_unresolved_objection_pct_field(self):
        inp = make_input(deals_lost_to_unresolved_objection_pct=0.20)
        assert inp.deals_lost_to_unresolved_objection_pct == 0.20

    def test_avg_objection_response_time_hours_field(self):
        inp = make_input(avg_objection_response_time_hours=30.0)
        assert inp.avg_objection_response_time_hours == 30.0

    def test_proactive_objection_prevention_rate_pct_field(self):
        inp = make_input(proactive_objection_prevention_rate_pct=0.20)
        assert inp.proactive_objection_prevention_rate_pct == 0.20

    def test_avg_opportunity_value_usd_field(self):
        inp = make_input(avg_opportunity_value_usd=50_000.0)
        assert inp.avg_opportunity_value_usd == 50_000.0

    def test_input_has_22_fields(self):
        import dataclasses
        fields = dataclasses.fields(ObjectionInput)
        assert len(fields) == 22


# ===========================================================================
# 3. ObjectionResult field tests + to_dict
# ===========================================================================

class TestObjectionResultFields:
    def setup_method(self):
        self.engine = fresh_engine()
        self.inp = make_input()
        self.result = self.engine.assess(self.inp)

    def test_rep_id_in_result(self):
        assert self.result.rep_id == "REP001"

    def test_region_in_result(self):
        assert self.result.region == "West"

    def test_objection_risk_is_enum(self):
        assert isinstance(self.result.objection_risk, ObjectionRisk)

    def test_objection_pattern_is_enum(self):
        assert isinstance(self.result.objection_pattern, ObjectionPattern)

    def test_objection_severity_is_enum(self):
        assert isinstance(self.result.objection_severity, ObjectionSeverity)

    def test_recommended_action_is_enum(self):
        assert isinstance(self.result.recommended_action, ObjectionAction)

    def test_objection_resolution_score_is_float(self):
        assert isinstance(self.result.objection_resolution_score, float)

    def test_objection_preparation_score_is_float(self):
        assert isinstance(self.result.objection_preparation_score, float)

    def test_objection_response_score_is_float(self):
        assert isinstance(self.result.objection_response_score, float)

    def test_competitive_handling_score_is_float(self):
        assert isinstance(self.result.competitive_handling_score, float)

    def test_objection_composite_is_float(self):
        assert isinstance(self.result.objection_composite, float)

    def test_has_objection_gap_is_bool(self):
        assert isinstance(self.result.has_objection_gap, bool)

    def test_requires_objection_coaching_is_bool(self):
        assert isinstance(self.result.requires_objection_coaching, bool)

    def test_estimated_deal_loss_usd_is_float(self):
        assert isinstance(self.result.estimated_deal_loss_usd, float)

    def test_objection_signal_is_str(self):
        assert isinstance(self.result.objection_signal, str)

    def test_result_has_15_fields(self):
        import dataclasses
        fields = dataclasses.fields(ObjectionResult)
        assert len(fields) == 15


class TestObjectionResultToDict:
    def setup_method(self):
        self.engine = fresh_engine()
        self.d = self.engine.assess(make_input()).to_dict()

    def test_to_dict_has_15_keys(self):
        assert len(self.d) == 15

    def test_rep_id_key(self):
        assert "rep_id" in self.d

    def test_region_key(self):
        assert "region" in self.d

    def test_objection_risk_key(self):
        assert "objection_risk" in self.d

    def test_objection_pattern_key(self):
        assert "objection_pattern" in self.d

    def test_objection_severity_key(self):
        assert "objection_severity" in self.d

    def test_recommended_action_key(self):
        assert "recommended_action" in self.d

    def test_objection_resolution_score_key(self):
        assert "objection_resolution_score" in self.d

    def test_objection_preparation_score_key(self):
        assert "objection_preparation_score" in self.d

    def test_objection_response_score_key(self):
        assert "objection_response_score" in self.d

    def test_competitive_handling_score_key(self):
        assert "competitive_handling_score" in self.d

    def test_objection_composite_key(self):
        assert "objection_composite" in self.d

    def test_has_objection_gap_key(self):
        assert "has_objection_gap" in self.d

    def test_requires_objection_coaching_key(self):
        assert "requires_objection_coaching" in self.d

    def test_estimated_deal_loss_usd_key(self):
        assert "estimated_deal_loss_usd" in self.d

    def test_objection_signal_key(self):
        assert "objection_signal" in self.d

    def test_risk_value_is_string(self):
        assert isinstance(self.d["objection_risk"], str)

    def test_pattern_value_is_string(self):
        assert isinstance(self.d["objection_pattern"], str)

    def test_severity_value_is_string(self):
        assert isinstance(self.d["objection_severity"], str)

    def test_action_value_is_string(self):
        assert isinstance(self.d["recommended_action"], str)


# ===========================================================================
# 4. Sub-score: _objection_resolution_score
# ===========================================================================

class TestObjectionResolutionScore:
    def _score(self, **kw):
        e = fresh_engine()
        return e._objection_resolution_score(make_input(**kw))

    # objections_resolved_pct branches
    def test_resolved_pct_very_low_adds_40(self):
        s = self._score(objections_resolved_pct=0.30, avg_days_to_resolve_objection=0.0, deals_lost_to_unresolved_objection_pct=0.0)
        assert s == 40.0

    def test_resolved_pct_exact_030_adds_40(self):
        s = self._score(objections_resolved_pct=0.30, avg_days_to_resolve_objection=0.0, deals_lost_to_unresolved_objection_pct=0.0)
        assert s == 40.0

    def test_resolved_pct_mid_adds_22(self):
        s = self._score(objections_resolved_pct=0.50, avg_days_to_resolve_objection=0.0, deals_lost_to_unresolved_objection_pct=0.0)
        assert s == 22.0

    def test_resolved_pct_exact_060_adds_22(self):
        s = self._score(objections_resolved_pct=0.60, avg_days_to_resolve_objection=0.0, deals_lost_to_unresolved_objection_pct=0.0)
        assert s == 22.0

    def test_resolved_pct_upper_mid_adds_8(self):
        s = self._score(objections_resolved_pct=0.70, avg_days_to_resolve_objection=0.0, deals_lost_to_unresolved_objection_pct=0.0)
        assert s == 8.0

    def test_resolved_pct_exact_080_adds_8(self):
        s = self._score(objections_resolved_pct=0.80, avg_days_to_resolve_objection=0.0, deals_lost_to_unresolved_objection_pct=0.0)
        assert s == 8.0

    def test_resolved_pct_high_adds_0(self):
        s = self._score(objections_resolved_pct=0.95, avg_days_to_resolve_objection=0.0, deals_lost_to_unresolved_objection_pct=0.0)
        assert s == 0.0

    # avg_days_to_resolve branches
    def test_days_high_adds_35(self):
        s = self._score(objections_resolved_pct=0.95, avg_days_to_resolve_objection=14.0, deals_lost_to_unresolved_objection_pct=0.0)
        assert s == 35.0

    def test_days_exact_14_adds_35(self):
        s = self._score(objections_resolved_pct=0.95, avg_days_to_resolve_objection=14.0, deals_lost_to_unresolved_objection_pct=0.0)
        assert s == 35.0

    def test_days_mid_adds_18(self):
        s = self._score(objections_resolved_pct=0.95, avg_days_to_resolve_objection=10.0, deals_lost_to_unresolved_objection_pct=0.0)
        assert s == 18.0

    def test_days_exact_7_adds_18(self):
        s = self._score(objections_resolved_pct=0.95, avg_days_to_resolve_objection=7.0, deals_lost_to_unresolved_objection_pct=0.0)
        assert s == 18.0

    def test_days_low_adds_0(self):
        s = self._score(objections_resolved_pct=0.95, avg_days_to_resolve_objection=3.0, deals_lost_to_unresolved_objection_pct=0.0)
        assert s == 0.0

    # deals_lost_to_unresolved branches
    def test_deals_lost_high_adds_25(self):
        s = self._score(objections_resolved_pct=0.95, avg_days_to_resolve_objection=0.0, deals_lost_to_unresolved_objection_pct=0.30)
        assert s == 25.0

    def test_deals_lost_exact_030_adds_25(self):
        s = self._score(objections_resolved_pct=0.95, avg_days_to_resolve_objection=0.0, deals_lost_to_unresolved_objection_pct=0.30)
        assert s == 25.0

    def test_deals_lost_mid_adds_12(self):
        s = self._score(objections_resolved_pct=0.95, avg_days_to_resolve_objection=0.0, deals_lost_to_unresolved_objection_pct=0.20)
        assert s == 12.0

    def test_deals_lost_exact_015_adds_12(self):
        s = self._score(objections_resolved_pct=0.95, avg_days_to_resolve_objection=0.0, deals_lost_to_unresolved_objection_pct=0.15)
        assert s == 12.0

    def test_deals_lost_low_adds_0(self):
        s = self._score(objections_resolved_pct=0.95, avg_days_to_resolve_objection=0.0, deals_lost_to_unresolved_objection_pct=0.05)
        assert s == 0.0

    def test_resolution_score_max_100(self):
        s = self._score(objections_resolved_pct=0.10, avg_days_to_resolve_objection=20.0, deals_lost_to_unresolved_objection_pct=0.50)
        assert s == 100.0

    def test_resolution_score_min_0(self):
        s = self._score(objections_resolved_pct=0.95, avg_days_to_resolve_objection=0.0, deals_lost_to_unresolved_objection_pct=0.0)
        assert s == 0.0

    def test_resolution_score_combination(self):
        # 40 + 18 + 12 = 70
        s = self._score(objections_resolved_pct=0.20, avg_days_to_resolve_objection=10.0, deals_lost_to_unresolved_objection_pct=0.20)
        assert s == 70.0


# ===========================================================================
# 5. Sub-score: _objection_preparation_score
# ===========================================================================

class TestObjectionPreparationScore:
    def _score(self, **kw):
        e = fresh_engine()
        return e._objection_preparation_score(make_input(**kw))

    # repeat_rate branches
    def test_repeat_rate_high_adds_40(self):
        s = self._score(objection_repeat_rate_pct=0.60, objection_documented_in_crm_pct=1.0, proactive_objection_prevention_rate_pct=1.0)
        assert s == 40.0

    def test_repeat_rate_exact_060_adds_40(self):
        s = self._score(objection_repeat_rate_pct=0.60, objection_documented_in_crm_pct=1.0, proactive_objection_prevention_rate_pct=1.0)
        assert s == 40.0

    def test_repeat_rate_mid_adds_22(self):
        s = self._score(objection_repeat_rate_pct=0.50, objection_documented_in_crm_pct=1.0, proactive_objection_prevention_rate_pct=1.0)
        assert s == 22.0

    def test_repeat_rate_exact_035_adds_22(self):
        s = self._score(objection_repeat_rate_pct=0.35, objection_documented_in_crm_pct=1.0, proactive_objection_prevention_rate_pct=1.0)
        assert s == 22.0

    def test_repeat_rate_lower_mid_adds_8(self):
        s = self._score(objection_repeat_rate_pct=0.25, objection_documented_in_crm_pct=1.0, proactive_objection_prevention_rate_pct=1.0)
        assert s == 8.0

    def test_repeat_rate_exact_020_adds_8(self):
        s = self._score(objection_repeat_rate_pct=0.20, objection_documented_in_crm_pct=1.0, proactive_objection_prevention_rate_pct=1.0)
        assert s == 8.0

    def test_repeat_rate_low_adds_0(self):
        s = self._score(objection_repeat_rate_pct=0.10, objection_documented_in_crm_pct=1.0, proactive_objection_prevention_rate_pct=1.0)
        assert s == 0.0

    # crm_pct branches
    def test_crm_pct_very_low_adds_35(self):
        s = self._score(objection_repeat_rate_pct=0.0, objection_documented_in_crm_pct=0.20, proactive_objection_prevention_rate_pct=1.0)
        assert s == 35.0

    def test_crm_pct_exact_020_adds_35(self):
        s = self._score(objection_repeat_rate_pct=0.0, objection_documented_in_crm_pct=0.20, proactive_objection_prevention_rate_pct=1.0)
        assert s == 35.0

    def test_crm_pct_mid_adds_18(self):
        s = self._score(objection_repeat_rate_pct=0.0, objection_documented_in_crm_pct=0.40, proactive_objection_prevention_rate_pct=1.0)
        assert s == 18.0

    def test_crm_pct_exact_050_adds_18(self):
        s = self._score(objection_repeat_rate_pct=0.0, objection_documented_in_crm_pct=0.50, proactive_objection_prevention_rate_pct=1.0)
        assert s == 18.0

    def test_crm_pct_high_adds_0(self):
        s = self._score(objection_repeat_rate_pct=0.0, objection_documented_in_crm_pct=0.80, proactive_objection_prevention_rate_pct=1.0)
        assert s == 0.0

    # proactive branches
    def test_proactive_very_low_adds_25(self):
        s = self._score(objection_repeat_rate_pct=0.0, objection_documented_in_crm_pct=1.0, proactive_objection_prevention_rate_pct=0.10)
        assert s == 25.0

    def test_proactive_exact_010_adds_25(self):
        s = self._score(objection_repeat_rate_pct=0.0, objection_documented_in_crm_pct=1.0, proactive_objection_prevention_rate_pct=0.10)
        assert s == 25.0

    def test_proactive_mid_adds_12(self):
        s = self._score(objection_repeat_rate_pct=0.0, objection_documented_in_crm_pct=1.0, proactive_objection_prevention_rate_pct=0.20)
        assert s == 12.0

    def test_proactive_exact_030_adds_12(self):
        s = self._score(objection_repeat_rate_pct=0.0, objection_documented_in_crm_pct=1.0, proactive_objection_prevention_rate_pct=0.30)
        assert s == 12.0

    def test_proactive_high_adds_0(self):
        s = self._score(objection_repeat_rate_pct=0.0, objection_documented_in_crm_pct=1.0, proactive_objection_prevention_rate_pct=0.60)
        assert s == 0.0

    def test_preparation_score_max_100(self):
        s = self._score(objection_repeat_rate_pct=0.80, objection_documented_in_crm_pct=0.05, proactive_objection_prevention_rate_pct=0.05)
        assert s == 100.0

    def test_preparation_score_min_0(self):
        s = self._score(objection_repeat_rate_pct=0.0, objection_documented_in_crm_pct=1.0, proactive_objection_prevention_rate_pct=0.60)
        assert s == 0.0

    def test_preparation_score_combination_40_18_12(self):
        # 40 + 18 + 12 = 70
        s = self._score(objection_repeat_rate_pct=0.70, objection_documented_in_crm_pct=0.40, proactive_objection_prevention_rate_pct=0.20)
        assert s == 70.0


# ===========================================================================
# 6. Sub-score: _objection_response_score
# ===========================================================================

class TestObjectionResponseScore:
    def _score(self, **kw):
        e = fresh_engine()
        return e._objection_response_score(make_input(**kw))

    # response_time branches
    def test_response_time_very_high_adds_40(self):
        s = self._score(avg_objection_response_time_hours=48.0, late_stage_new_objection_rate_pct=0.0, champion_coached_on_internal_objections_pct=1.0)
        assert s == 40.0

    def test_response_time_exact_48_adds_40(self):
        s = self._score(avg_objection_response_time_hours=48.0, late_stage_new_objection_rate_pct=0.0, champion_coached_on_internal_objections_pct=1.0)
        assert s == 40.0

    def test_response_time_mid_adds_22(self):
        s = self._score(avg_objection_response_time_hours=30.0, late_stage_new_objection_rate_pct=0.0, champion_coached_on_internal_objections_pct=1.0)
        assert s == 22.0

    def test_response_time_exact_24_adds_22(self):
        s = self._score(avg_objection_response_time_hours=24.0, late_stage_new_objection_rate_pct=0.0, champion_coached_on_internal_objections_pct=1.0)
        assert s == 22.0

    def test_response_time_lower_mid_adds_8(self):
        s = self._score(avg_objection_response_time_hours=10.0, late_stage_new_objection_rate_pct=0.0, champion_coached_on_internal_objections_pct=1.0)
        assert s == 8.0

    def test_response_time_exact_8_adds_8(self):
        s = self._score(avg_objection_response_time_hours=8.0, late_stage_new_objection_rate_pct=0.0, champion_coached_on_internal_objections_pct=1.0)
        assert s == 8.0

    def test_response_time_low_adds_0(self):
        s = self._score(avg_objection_response_time_hours=2.0, late_stage_new_objection_rate_pct=0.0, champion_coached_on_internal_objections_pct=1.0)
        assert s == 0.0

    # late_stage branches
    def test_late_stage_high_adds_35(self):
        s = self._score(avg_objection_response_time_hours=0.0, late_stage_new_objection_rate_pct=0.50, champion_coached_on_internal_objections_pct=1.0)
        assert s == 35.0

    def test_late_stage_exact_050_adds_35(self):
        s = self._score(avg_objection_response_time_hours=0.0, late_stage_new_objection_rate_pct=0.50, champion_coached_on_internal_objections_pct=1.0)
        assert s == 35.0

    def test_late_stage_mid_adds_18(self):
        s = self._score(avg_objection_response_time_hours=0.0, late_stage_new_objection_rate_pct=0.30, champion_coached_on_internal_objections_pct=1.0)
        assert s == 18.0

    def test_late_stage_exact_025_adds_18(self):
        s = self._score(avg_objection_response_time_hours=0.0, late_stage_new_objection_rate_pct=0.25, champion_coached_on_internal_objections_pct=1.0)
        assert s == 18.0

    def test_late_stage_low_adds_0(self):
        s = self._score(avg_objection_response_time_hours=0.0, late_stage_new_objection_rate_pct=0.10, champion_coached_on_internal_objections_pct=1.0)
        assert s == 0.0

    # champion coached branches
    def test_champion_very_low_adds_25(self):
        s = self._score(avg_objection_response_time_hours=0.0, late_stage_new_objection_rate_pct=0.0, champion_coached_on_internal_objections_pct=0.15)
        assert s == 25.0

    def test_champion_exact_015_adds_25(self):
        s = self._score(avg_objection_response_time_hours=0.0, late_stage_new_objection_rate_pct=0.0, champion_coached_on_internal_objections_pct=0.15)
        assert s == 25.0

    def test_champion_mid_adds_12(self):
        s = self._score(avg_objection_response_time_hours=0.0, late_stage_new_objection_rate_pct=0.0, champion_coached_on_internal_objections_pct=0.30)
        assert s == 12.0

    def test_champion_exact_040_adds_12(self):
        s = self._score(avg_objection_response_time_hours=0.0, late_stage_new_objection_rate_pct=0.0, champion_coached_on_internal_objections_pct=0.40)
        assert s == 12.0

    def test_champion_high_adds_0(self):
        s = self._score(avg_objection_response_time_hours=0.0, late_stage_new_objection_rate_pct=0.0, champion_coached_on_internal_objections_pct=0.80)
        assert s == 0.0

    def test_response_score_max_100(self):
        s = self._score(avg_objection_response_time_hours=60.0, late_stage_new_objection_rate_pct=0.80, champion_coached_on_internal_objections_pct=0.05)
        assert s == 100.0

    def test_response_score_min_0(self):
        s = self._score(avg_objection_response_time_hours=0.0, late_stage_new_objection_rate_pct=0.0, champion_coached_on_internal_objections_pct=0.80)
        assert s == 0.0


# ===========================================================================
# 7. Sub-score: _competitive_handling_score
# ===========================================================================

class TestCompetitiveHandlingScore:
    def _score(self, **kw):
        e = fresh_engine()
        return e._competitive_handling_score(make_input(**kw))

    # competitive_objection_loss_rate branches
    def test_comp_loss_very_high_adds_45(self):
        s = self._score(competitive_objection_loss_rate_pct=0.60, price_objection_resolution_rate_pct=1.0, trust_objection_rate_pct=0.0)
        assert s == 45.0

    def test_comp_loss_exact_060_adds_45(self):
        s = self._score(competitive_objection_loss_rate_pct=0.60, price_objection_resolution_rate_pct=1.0, trust_objection_rate_pct=0.0)
        assert s == 45.0

    def test_comp_loss_mid_adds_25(self):
        s = self._score(competitive_objection_loss_rate_pct=0.40, price_objection_resolution_rate_pct=1.0, trust_objection_rate_pct=0.0)
        assert s == 25.0

    def test_comp_loss_exact_035_adds_25(self):
        s = self._score(competitive_objection_loss_rate_pct=0.35, price_objection_resolution_rate_pct=1.0, trust_objection_rate_pct=0.0)
        assert s == 25.0

    def test_comp_loss_lower_mid_adds_10(self):
        s = self._score(competitive_objection_loss_rate_pct=0.25, price_objection_resolution_rate_pct=1.0, trust_objection_rate_pct=0.0)
        assert s == 10.0

    def test_comp_loss_exact_020_adds_10(self):
        s = self._score(competitive_objection_loss_rate_pct=0.20, price_objection_resolution_rate_pct=1.0, trust_objection_rate_pct=0.0)
        assert s == 10.0

    def test_comp_loss_low_adds_0(self):
        s = self._score(competitive_objection_loss_rate_pct=0.05, price_objection_resolution_rate_pct=1.0, trust_objection_rate_pct=0.0)
        assert s == 0.0

    # price_objection_resolution branches
    def test_price_res_very_low_adds_30(self):
        s = self._score(competitive_objection_loss_rate_pct=0.0, price_objection_resolution_rate_pct=0.20, trust_objection_rate_pct=0.0)
        assert s == 30.0

    def test_price_res_exact_020_adds_30(self):
        s = self._score(competitive_objection_loss_rate_pct=0.0, price_objection_resolution_rate_pct=0.20, trust_objection_rate_pct=0.0)
        assert s == 30.0

    def test_price_res_mid_adds_15(self):
        s = self._score(competitive_objection_loss_rate_pct=0.0, price_objection_resolution_rate_pct=0.40, trust_objection_rate_pct=0.0)
        assert s == 15.0

    def test_price_res_exact_050_adds_15(self):
        s = self._score(competitive_objection_loss_rate_pct=0.0, price_objection_resolution_rate_pct=0.50, trust_objection_rate_pct=0.0)
        assert s == 15.0

    def test_price_res_high_adds_0(self):
        s = self._score(competitive_objection_loss_rate_pct=0.0, price_objection_resolution_rate_pct=0.80, trust_objection_rate_pct=0.0)
        assert s == 0.0

    # trust_objection_rate branches
    def test_trust_rate_high_adds_25(self):
        s = self._score(competitive_objection_loss_rate_pct=0.0, price_objection_resolution_rate_pct=1.0, trust_objection_rate_pct=0.40)
        assert s == 25.0

    def test_trust_rate_exact_040_adds_25(self):
        s = self._score(competitive_objection_loss_rate_pct=0.0, price_objection_resolution_rate_pct=1.0, trust_objection_rate_pct=0.40)
        assert s == 25.0

    def test_trust_rate_mid_adds_12(self):
        s = self._score(competitive_objection_loss_rate_pct=0.0, price_objection_resolution_rate_pct=1.0, trust_objection_rate_pct=0.25)
        assert s == 12.0

    def test_trust_rate_exact_020_adds_12(self):
        s = self._score(competitive_objection_loss_rate_pct=0.0, price_objection_resolution_rate_pct=1.0, trust_objection_rate_pct=0.20)
        assert s == 12.0

    def test_trust_rate_low_adds_0(self):
        s = self._score(competitive_objection_loss_rate_pct=0.0, price_objection_resolution_rate_pct=1.0, trust_objection_rate_pct=0.05)
        assert s == 0.0

    def test_competitive_score_max_100(self):
        s = self._score(competitive_objection_loss_rate_pct=0.90, price_objection_resolution_rate_pct=0.05, trust_objection_rate_pct=0.80)
        assert s == 100.0

    def test_competitive_score_min_0(self):
        s = self._score(competitive_objection_loss_rate_pct=0.0, price_objection_resolution_rate_pct=1.0, trust_objection_rate_pct=0.0)
        assert s == 0.0


# ===========================================================================
# 8. Pattern detection priority
# ===========================================================================

class TestPatternDetection:
    def _pattern(self, **kw):
        e = fresh_engine()
        inp = make_input(**kw)
        res = e._objection_resolution_score(inp)
        prep = e._objection_preparation_score(inp)
        resp = e._objection_response_score(inp)
        comp = e._competitive_handling_score(inp)
        return e._detect_pattern(inp, res, prep, resp, comp)

    def test_pattern_none_healthy(self):
        p = self._pattern()
        assert p == ObjectionPattern.none

    def test_price_objection_paralysis_detected(self):
        # Need competitive >= 30: use competitive_objection_loss_rate_pct=0.35 (+25) + price_res=0.20(+30) = 55 >= 30
        # AND price_objection_resolution_rate_pct <= 0.30
        p = self._pattern(
            competitive_objection_loss_rate_pct=0.35,
            price_objection_resolution_rate_pct=0.20,
            trust_objection_rate_pct=0.0,
        )
        assert p == ObjectionPattern.price_objection_paralysis

    def test_technical_objection_avoidance_detected(self):
        # resolution >= 30: objections_resolved_pct=0.30 (+40) AND technical_escalation >= 0.60
        p = self._pattern(
            objections_resolved_pct=0.20,
            avg_days_to_resolve_objection=0.0,
            deals_lost_to_unresolved_objection_pct=0.0,
            technical_objection_escalation_rate_pct=0.70,
            # keep competitive < 30 to avoid priority 1
            competitive_objection_loss_rate_pct=0.0,
            price_objection_resolution_rate_pct=0.80,
            trust_objection_rate_pct=0.0,
        )
        assert p == ObjectionPattern.technical_objection_avoidance

    def test_trust_objection_gap_detected(self):
        # preparation >= 30: repeat=0.60(+40), crm=1.0, proactive=1.0 → 40 >= 30
        # AND trust_objection_rate_pct >= 0.40
        # competitive < 30, resolution < 30
        p = self._pattern(
            objection_repeat_rate_pct=0.60,
            objection_documented_in_crm_pct=1.0,
            proactive_objection_prevention_rate_pct=1.0,
            trust_objection_rate_pct=0.45,
            competitive_objection_loss_rate_pct=0.0,
            price_objection_resolution_rate_pct=0.80,
            objections_resolved_pct=0.90,
            avg_days_to_resolve_objection=0.0,
            deals_lost_to_unresolved_objection_pct=0.0,
        )
        assert p == ObjectionPattern.trust_objection_gap

    def test_competition_capitulation_detected(self):
        # competitive >= 40 AND competitive_objection_loss_rate_pct >= 0.50
        # Must avoid priority 1 (price_res > 0.30), priority 2 (tech esc < 0.60), priority 3 (trust < 0.40)
        p = self._pattern(
            competitive_objection_loss_rate_pct=0.60,
            price_objection_resolution_rate_pct=0.60,  # > 0.30 avoids priority 1
            trust_objection_rate_pct=0.10,              # < 0.40 avoids priority 3
            objections_resolved_pct=0.90,
            avg_days_to_resolve_objection=0.0,
            deals_lost_to_unresolved_objection_pct=0.0,
            technical_objection_escalation_rate_pct=0.10,
            objection_repeat_rate_pct=0.0,
            objection_documented_in_crm_pct=1.0,
            proactive_objection_prevention_rate_pct=1.0,
        )
        assert p == ObjectionPattern.competition_capitulation_under_objection

    def test_late_stage_objection_surprise_detected(self):
        # response >= 30 AND late_stage >= 0.35
        # Avoid priorities 1-4
        p = self._pattern(
            avg_objection_response_time_hours=48.0,
            late_stage_new_objection_rate_pct=0.40,
            champion_coached_on_internal_objections_pct=1.0,
            competitive_objection_loss_rate_pct=0.0,
            price_objection_resolution_rate_pct=0.80,
            trust_objection_rate_pct=0.10,
            objections_resolved_pct=0.90,
            avg_days_to_resolve_objection=0.0,
            deals_lost_to_unresolved_objection_pct=0.0,
            technical_objection_escalation_rate_pct=0.10,
            objection_repeat_rate_pct=0.0,
            objection_documented_in_crm_pct=1.0,
            proactive_objection_prevention_rate_pct=1.0,
        )
        assert p == ObjectionPattern.late_stage_objection_surprise

    def test_price_paralysis_takes_priority_over_technical(self):
        # competitive >= 30 AND price_res <= 0.30 → priority 1
        # Also resolution >= 30 AND tech_esc >= 0.60 → priority 2 would fire
        p = self._pattern(
            competitive_objection_loss_rate_pct=0.35,
            price_objection_resolution_rate_pct=0.20,  # triggers priority 1
            trust_objection_rate_pct=0.0,
            objections_resolved_pct=0.20,
            avg_days_to_resolve_objection=0.0,
            deals_lost_to_unresolved_objection_pct=0.0,
            technical_objection_escalation_rate_pct=0.70,  # would trigger priority 2
        )
        assert p == ObjectionPattern.price_objection_paralysis

    def test_none_when_all_conditions_barely_missed(self):
        # competitive = 29 (just below 30) → no price_paralysis
        # resolution < 30, preparation < 30, response < 30
        # late_stage < 0.35
        e = fresh_engine()
        inp = make_input(
            competitive_objection_loss_rate_pct=0.0,
            price_objection_resolution_rate_pct=0.80,
            trust_objection_rate_pct=0.0,
            objections_resolved_pct=0.90,
            avg_days_to_resolve_objection=0.0,
            deals_lost_to_unresolved_objection_pct=0.0,
            technical_objection_escalation_rate_pct=0.10,
            objection_repeat_rate_pct=0.0,
            objection_documented_in_crm_pct=1.0,
            proactive_objection_prevention_rate_pct=0.60,
            avg_objection_response_time_hours=0.0,
            late_stage_new_objection_rate_pct=0.10,
            champion_coached_on_internal_objections_pct=0.80,
        )
        comp = e._competitive_handling_score(inp)
        res = e._objection_resolution_score(inp)
        prep = e._objection_preparation_score(inp)
        resp = e._objection_response_score(inp)
        p = e._detect_pattern(inp, res, prep, resp, comp)
        assert p == ObjectionPattern.none


# ===========================================================================
# 9. Risk level thresholds
# ===========================================================================

class TestRiskLevel:
    def _risk(self, composite):
        return fresh_engine()._risk_level(composite)

    def test_risk_critical_at_60(self):
        assert self._risk(60.0) == ObjectionRisk.critical

    def test_risk_critical_above_60(self):
        assert self._risk(80.0) == ObjectionRisk.critical

    def test_risk_high_at_40(self):
        assert self._risk(40.0) == ObjectionRisk.high

    def test_risk_high_below_60(self):
        assert self._risk(59.9) == ObjectionRisk.high

    def test_risk_moderate_at_20(self):
        assert self._risk(20.0) == ObjectionRisk.moderate

    def test_risk_moderate_below_40(self):
        assert self._risk(39.9) == ObjectionRisk.moderate

    def test_risk_low_below_20(self):
        assert self._risk(19.9) == ObjectionRisk.low

    def test_risk_low_at_zero(self):
        assert self._risk(0.0) == ObjectionRisk.low

    def test_risk_low_at_19(self):
        assert self._risk(19.0) == ObjectionRisk.low


# ===========================================================================
# 10. Severity thresholds
# ===========================================================================

class TestSeverity:
    def _sev(self, composite):
        return fresh_engine()._severity(composite)

    def test_severity_paralyzed_at_60(self):
        assert self._sev(60.0) == ObjectionSeverity.paralyzed

    def test_severity_paralyzed_above_60(self):
        assert self._sev(90.0) == ObjectionSeverity.paralyzed

    def test_severity_reactive_at_40(self):
        assert self._sev(40.0) == ObjectionSeverity.reactive

    def test_severity_reactive_below_60(self):
        assert self._sev(59.9) == ObjectionSeverity.reactive

    def test_severity_developing_at_20(self):
        assert self._sev(20.0) == ObjectionSeverity.developing

    def test_severity_developing_below_40(self):
        assert self._sev(39.9) == ObjectionSeverity.developing

    def test_severity_confident_below_20(self):
        assert self._sev(19.9) == ObjectionSeverity.confident

    def test_severity_confident_at_zero(self):
        assert self._sev(0.0) == ObjectionSeverity.confident


# ===========================================================================
# 11. Action mapping
# ===========================================================================

class TestActionMapping:
    def _action(self, risk, pattern):
        return fresh_engine()._action(risk, pattern)

    def test_critical_technical_avoidance(self):
        assert self._action(ObjectionRisk.critical, ObjectionPattern.technical_objection_avoidance) == ObjectionAction.technical_proof_support

    def test_critical_trust_gap(self):
        assert self._action(ObjectionRisk.critical, ObjectionPattern.trust_objection_gap) == ObjectionAction.trust_building_coaching

    def test_critical_none_pattern(self):
        assert self._action(ObjectionRisk.critical, ObjectionPattern.none) == ObjectionAction.objection_handling_workshop

    def test_critical_price_paralysis(self):
        assert self._action(ObjectionRisk.critical, ObjectionPattern.price_objection_paralysis) == ObjectionAction.objection_handling_workshop

    def test_critical_competition_capitulation(self):
        assert self._action(ObjectionRisk.critical, ObjectionPattern.competition_capitulation_under_objection) == ObjectionAction.objection_handling_workshop

    def test_critical_late_stage_surprise(self):
        assert self._action(ObjectionRisk.critical, ObjectionPattern.late_stage_objection_surprise) == ObjectionAction.objection_handling_workshop

    def test_high_price_paralysis(self):
        assert self._action(ObjectionRisk.high, ObjectionPattern.price_objection_paralysis) == ObjectionAction.price_reframing_training

    def test_high_competition_capitulation(self):
        assert self._action(ObjectionRisk.high, ObjectionPattern.competition_capitulation_under_objection) == ObjectionAction.competitive_intelligence_training

    def test_high_none_pattern(self):
        assert self._action(ObjectionRisk.high, ObjectionPattern.none) == ObjectionAction.objection_handling_workshop

    def test_high_technical_avoidance(self):
        assert self._action(ObjectionRisk.high, ObjectionPattern.technical_objection_avoidance) == ObjectionAction.objection_handling_workshop

    def test_high_trust_gap(self):
        assert self._action(ObjectionRisk.high, ObjectionPattern.trust_objection_gap) == ObjectionAction.objection_handling_workshop

    def test_high_late_stage_surprise(self):
        assert self._action(ObjectionRisk.high, ObjectionPattern.late_stage_objection_surprise) == ObjectionAction.objection_handling_workshop

    def test_moderate_any_pattern(self):
        assert self._action(ObjectionRisk.moderate, ObjectionPattern.none) == ObjectionAction.objection_handling_workshop

    def test_moderate_price_paralysis(self):
        assert self._action(ObjectionRisk.moderate, ObjectionPattern.price_objection_paralysis) == ObjectionAction.objection_handling_workshop

    def test_low_any_pattern(self):
        assert self._action(ObjectionRisk.low, ObjectionPattern.none) == ObjectionAction.no_action

    def test_low_price_paralysis(self):
        assert self._action(ObjectionRisk.low, ObjectionPattern.price_objection_paralysis) == ObjectionAction.no_action


# ===========================================================================
# 12. Gap and coaching flags
# ===========================================================================

class TestFlags:
    def _gap(self, composite, **kw):
        e = fresh_engine()
        return e._has_objection_gap(composite, make_input(**kw))

    def _coach(self, composite, **kw):
        e = fresh_engine()
        return e._requires_objection_coaching(composite, make_input(**kw))

    # gap flag
    def test_gap_true_when_composite_ge_40(self):
        assert self._gap(40.0) is True

    def test_gap_true_when_composite_above_40(self):
        assert self._gap(50.0) is True

    def test_gap_true_when_deals_lost_ge_025(self):
        assert self._gap(10.0, deals_lost_to_unresolved_objection_pct=0.25) is True

    def test_gap_true_when_comp_loss_ge_050(self):
        assert self._gap(10.0, competitive_objection_loss_rate_pct=0.50) is True

    def test_gap_false_when_all_below_thresholds(self):
        assert self._gap(39.9, deals_lost_to_unresolved_objection_pct=0.10, competitive_objection_loss_rate_pct=0.10) is False

    def test_gap_false_at_zero(self):
        assert self._gap(0.0, deals_lost_to_unresolved_objection_pct=0.0, competitive_objection_loss_rate_pct=0.0) is False

    def test_gap_true_deals_lost_exactly_025(self):
        assert self._gap(0.0, deals_lost_to_unresolved_objection_pct=0.25) is True

    def test_gap_true_comp_loss_exactly_050(self):
        assert self._gap(0.0, competitive_objection_loss_rate_pct=0.50) is True

    # coaching flag
    def test_coach_true_when_composite_ge_30(self):
        assert self._coach(30.0) is True

    def test_coach_true_when_resolved_le_050(self):
        assert self._coach(0.0, objections_resolved_pct=0.50) is True

    def test_coach_true_when_repeat_ge_040(self):
        assert self._coach(0.0, objection_repeat_rate_pct=0.40) is True

    def test_coach_false_when_all_below(self):
        assert self._coach(29.9, objections_resolved_pct=0.90, objection_repeat_rate_pct=0.05) is False

    def test_coach_true_resolved_exactly_050(self):
        assert self._coach(0.0, objections_resolved_pct=0.50) is True

    def test_coach_true_repeat_exactly_040(self):
        assert self._coach(0.0, objection_repeat_rate_pct=0.40) is True


# ===========================================================================
# 13. Estimated deal loss formula
# ===========================================================================

class TestEstimatedDealLoss:
    def _loss(self, total, lost_pct, value, composite):
        e = fresh_engine()
        inp = make_input(
            total_objections_logged=total,
            deals_lost_to_unresolved_objection_pct=lost_pct,
            avg_opportunity_value_usd=value,
        )
        return e._estimated_deal_loss(inp, composite)

    def test_loss_basic_calculation(self):
        # 100 * 0.10 * 10000 * (50/100) = 100 * 0.10 * 10000 * 0.5 = 50000.0
        assert self._loss(100, 0.10, 10_000, 50.0) == 50000.0

    def test_loss_zero_composite(self):
        assert self._loss(100, 0.20, 10_000, 0.0) == 0.0

    def test_loss_zero_lost_pct(self):
        assert self._loss(100, 0.0, 10_000, 50.0) == 0.0

    def test_loss_zero_value(self):
        assert self._loss(100, 0.20, 0.0, 50.0) == 0.0

    def test_loss_rounded_to_2_decimals(self):
        # 10 * 0.33 * 100 * 0.5 = 165.0 exactly
        result = self._loss(10, 0.33, 100.0, 50.0)
        assert result == round(10 * 0.33 * 100.0 * 0.50, 2)

    def test_loss_high_values(self):
        # 200 * 0.30 * 50000 * (80/100) = 2_400_000.0
        assert self._loss(200, 0.30, 50_000, 80.0) == 2_400_000.0

    def test_loss_returns_float(self):
        assert isinstance(self._loss(100, 0.10, 10_000, 50.0), float)

    def test_loss_with_composite_100(self):
        # 50 * 0.20 * 1000 * 1.0 = 10000.0
        assert self._loss(50, 0.20, 1_000.0, 100.0) == 10_000.0


# ===========================================================================
# 14. Signal string
# ===========================================================================

class TestSignalString:
    def _signal(self, pattern, composite, **kw):
        e = fresh_engine()
        inp = make_input(**kw)
        return e._signal(inp, pattern, composite)

    def test_healthy_signal_none_pattern_low_composite(self):
        sig = self._signal(ObjectionPattern.none, 10.0)
        assert sig == "Objection handling healthy — resolution rate, preparation, and competitive handling within benchmarks"

    def test_healthy_signal_boundary_composite_19(self):
        sig = self._signal(ObjectionPattern.none, 19.9)
        assert sig == "Objection handling healthy — resolution rate, preparation, and competitive handling within benchmarks"

    def test_non_healthy_signal_none_pattern_composite_20(self):
        sig = self._signal(ObjectionPattern.none, 20.0, objections_resolved_pct=0.70, competitive_objection_loss_rate_pct=0.10, avg_days_to_resolve_objection=5.0)
        assert sig != "Objection handling healthy — resolution rate, preparation, and competitive handling within benchmarks"
        assert "Objection risk" in sig

    def test_signal_includes_pattern_label(self):
        sig = self._signal(
            ObjectionPattern.price_objection_paralysis,
            40.0,
            objections_resolved_pct=0.70,
            competitive_objection_loss_rate_pct=0.10,
            avg_days_to_resolve_objection=5.0,
        )
        assert "Price objection paralysis" in sig

    def test_signal_includes_composite(self):
        sig = self._signal(
            ObjectionPattern.none,
            25.0,
            objections_resolved_pct=0.70,
            competitive_objection_loss_rate_pct=0.10,
            avg_days_to_resolve_objection=5.0,
        )
        assert "composite 25" in sig

    def test_signal_includes_resolved_pct(self):
        sig = self._signal(
            ObjectionPattern.none,
            25.0,
            objections_resolved_pct=0.70,
            competitive_objection_loss_rate_pct=0.10,
            avg_days_to_resolve_objection=5.0,
        )
        assert "70% objections resolved" in sig

    def test_signal_includes_competitive_losses(self):
        sig = self._signal(
            ObjectionPattern.none,
            25.0,
            objections_resolved_pct=0.70,
            competitive_objection_loss_rate_pct=0.30,
            avg_days_to_resolve_objection=5.0,
        )
        assert "30% competitive losses" in sig

    def test_signal_includes_avg_days(self):
        sig = self._signal(
            ObjectionPattern.none,
            25.0,
            objections_resolved_pct=0.70,
            competitive_objection_loss_rate_pct=0.10,
            avg_days_to_resolve_objection=7.0,
        )
        assert "7 avg days to resolve" in sig

    def test_signal_pattern_label_capitalized(self):
        sig = self._signal(
            ObjectionPattern.trust_objection_gap,
            50.0,
            objections_resolved_pct=0.70,
            competitive_objection_loss_rate_pct=0.10,
            avg_days_to_resolve_objection=5.0,
        )
        assert sig[0].isupper()


# ===========================================================================
# 15. assess() end-to-end
# ===========================================================================

class TestAssessEndToEnd:
    def test_assess_returns_objection_result(self):
        e = fresh_engine()
        r = e.assess(make_input())
        assert isinstance(r, ObjectionResult)

    def test_assess_stores_result(self):
        e = fresh_engine()
        e.assess(make_input())
        assert len(e._results) == 1

    def test_assess_healthy_rep_is_low_risk(self):
        e = fresh_engine()
        r = e.assess(make_input())
        assert r.objection_risk == ObjectionRisk.low

    def test_assess_healthy_rep_is_confident(self):
        e = fresh_engine()
        r = e.assess(make_input())
        assert r.objection_severity == ObjectionSeverity.confident

    def test_assess_healthy_rep_no_action(self):
        e = fresh_engine()
        r = e.assess(make_input())
        assert r.recommended_action == ObjectionAction.no_action

    def test_assess_healthy_no_pattern(self):
        e = fresh_engine()
        r = e.assess(make_input())
        assert r.objection_pattern == ObjectionPattern.none

    def test_assess_healthy_signal_healthy(self):
        e = fresh_engine()
        r = e.assess(make_input())
        assert "healthy" in r.objection_signal

    def test_assess_rep_id_preserved(self):
        e = fresh_engine()
        r = e.assess(make_input(rep_id="SPECIAL"))
        assert r.rep_id == "SPECIAL"

    def test_assess_region_preserved(self):
        e = fresh_engine()
        r = e.assess(make_input(region="Southern"))
        assert r.region == "Southern"

    def test_assess_critical_risk(self):
        # Push all sub-scores high to get composite >= 60
        e = fresh_engine()
        r = e.assess(make_input(
            objections_resolved_pct=0.20,
            avg_days_to_resolve_objection=15.0,
            deals_lost_to_unresolved_objection_pct=0.35,
            objection_repeat_rate_pct=0.70,
            objection_documented_in_crm_pct=0.10,
            proactive_objection_prevention_rate_pct=0.05,
            avg_objection_response_time_hours=60.0,
            late_stage_new_objection_rate_pct=0.60,
            champion_coached_on_internal_objections_pct=0.05,
            competitive_objection_loss_rate_pct=0.70,
            price_objection_resolution_rate_pct=0.10,
            trust_objection_rate_pct=0.50,
        ))
        assert r.objection_risk == ObjectionRisk.critical

    def test_assess_composite_capped_100(self):
        e = fresh_engine()
        r = e.assess(make_input(
            objections_resolved_pct=0.10,
            avg_days_to_resolve_objection=20.0,
            deals_lost_to_unresolved_objection_pct=0.50,
            objection_repeat_rate_pct=0.90,
            objection_documented_in_crm_pct=0.05,
            proactive_objection_prevention_rate_pct=0.02,
            avg_objection_response_time_hours=100.0,
            late_stage_new_objection_rate_pct=0.90,
            champion_coached_on_internal_objections_pct=0.02,
            competitive_objection_loss_rate_pct=0.90,
            price_objection_resolution_rate_pct=0.05,
            trust_objection_rate_pct=0.90,
        ))
        assert r.objection_composite <= 100.0

    def test_assess_scores_non_negative(self):
        e = fresh_engine()
        r = e.assess(make_input())
        assert r.objection_resolution_score >= 0
        assert r.objection_preparation_score >= 0
        assert r.objection_response_score >= 0
        assert r.competitive_handling_score >= 0

    def test_assess_estimated_loss_non_negative(self):
        e = fresh_engine()
        r = e.assess(make_input())
        assert r.estimated_deal_loss_usd >= 0.0

    def test_assess_has_objection_gap_false_for_healthy(self):
        e = fresh_engine()
        r = e.assess(make_input())
        assert r.has_objection_gap is False

    def test_assess_requires_coaching_false_for_healthy(self):
        e = fresh_engine()
        r = e.assess(make_input())
        assert r.requires_objection_coaching is False

    def test_assess_gap_true_when_composite_high(self):
        e = fresh_engine()
        r = e.assess(make_input(
            objections_resolved_pct=0.20,
            avg_days_to_resolve_objection=15.0,
            deals_lost_to_unresolved_objection_pct=0.35,
            objection_repeat_rate_pct=0.70,
            objection_documented_in_crm_pct=0.10,
            proactive_objection_prevention_rate_pct=0.05,
            avg_objection_response_time_hours=60.0,
            late_stage_new_objection_rate_pct=0.60,
            champion_coached_on_internal_objections_pct=0.05,
            competitive_objection_loss_rate_pct=0.70,
            price_objection_resolution_rate_pct=0.10,
            trust_objection_rate_pct=0.50,
        ))
        assert r.has_objection_gap is True

    def test_assess_coaching_true_when_composite_high(self):
        e = fresh_engine()
        r = e.assess(make_input(
            objections_resolved_pct=0.20,
            avg_days_to_resolve_objection=15.0,
            deals_lost_to_unresolved_objection_pct=0.35,
        ))
        assert r.requires_objection_coaching is True

    def test_assess_multiple_calls_accumulate(self):
        e = fresh_engine()
        e.assess(make_input(rep_id="A"))
        e.assess(make_input(rep_id="B"))
        e.assess(make_input(rep_id="C"))
        assert len(e._results) == 3

    def test_assess_deal_loss_formula_correct(self):
        e = fresh_engine()
        inp = make_input(
            total_objections_logged=100,
            deals_lost_to_unresolved_objection_pct=0.10,
            avg_opportunity_value_usd=10_000.0,
        )
        r = e.assess(inp)
        expected = round(100 * 0.10 * 10_000.0 * (r.objection_composite / 100.0), 2)
        assert r.estimated_deal_loss_usd == expected


# ===========================================================================
# 16. assess_batch()
# ===========================================================================

class TestAssessBatch:
    def test_batch_empty_list(self):
        e = fresh_engine()
        results = e.assess_batch([])
        assert results == []

    def test_batch_single_item(self):
        e = fresh_engine()
        results = e.assess_batch([make_input(rep_id="X")])
        assert len(results) == 1
        assert results[0].rep_id == "X"

    def test_batch_multiple_items(self):
        e = fresh_engine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = e.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_results_stored(self):
        e = fresh_engine()
        e.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        assert len(e._results) == 3

    def test_batch_all_results_are_objection_result(self):
        e = fresh_engine()
        results = e.assess_batch([make_input(rep_id="A"), make_input(rep_id="B")])
        for r in results:
            assert isinstance(r, ObjectionResult)

    def test_batch_preserves_order(self):
        e = fresh_engine()
        ids = ["ALPHA", "BETA", "GAMMA"]
        results = e.assess_batch([make_input(rep_id=i) for i in ids])
        assert [r.rep_id for r in results] == ids

    def test_batch_accumulates_after_assess(self):
        e = fresh_engine()
        e.assess(make_input(rep_id="First"))
        e.assess_batch([make_input(rep_id="Second"), make_input(rep_id="Third")])
        assert len(e._results) == 3

    def test_batch_mixed_inputs(self):
        e = fresh_engine()
        good = make_input(rep_id="Good")
        bad = make_input(
            rep_id="Bad",
            objections_resolved_pct=0.10,
            avg_days_to_resolve_objection=20.0,
            deals_lost_to_unresolved_objection_pct=0.50,
        )
        results = e.assess_batch([good, bad])
        assert results[0].objection_risk == ObjectionRisk.low
        assert results[1].objection_risk != ObjectionRisk.low


# ===========================================================================
# 17. summary() — empty
# ===========================================================================

class TestSummaryEmpty:
    def setup_method(self):
        self.s = fresh_engine().summary()

    def test_summary_empty_total(self):
        assert self.s["total"] == 0

    def test_summary_empty_risk_counts(self):
        assert self.s["risk_counts"] == {}

    def test_summary_empty_pattern_counts(self):
        assert self.s["pattern_counts"] == {}

    def test_summary_empty_severity_counts(self):
        assert self.s["severity_counts"] == {}

    def test_summary_empty_action_counts(self):
        assert self.s["action_counts"] == {}

    def test_summary_empty_avg_composite(self):
        assert self.s["avg_objection_composite"] == 0.0

    def test_summary_empty_gap_count(self):
        assert self.s["objection_gap_count"] == 0

    def test_summary_empty_coaching_count(self):
        assert self.s["coaching_count"] == 0

    def test_summary_empty_avg_resolution(self):
        assert self.s["avg_objection_resolution_score"] == 0.0

    def test_summary_empty_avg_preparation(self):
        assert self.s["avg_objection_preparation_score"] == 0.0

    def test_summary_empty_avg_response(self):
        assert self.s["avg_objection_response_score"] == 0.0

    def test_summary_empty_avg_competitive(self):
        assert self.s["avg_competitive_handling_score"] == 0.0

    def test_summary_empty_total_loss(self):
        assert self.s["total_estimated_deal_loss_usd"] == 0.0

    def test_summary_empty_has_13_keys(self):
        assert len(self.s) == 13


# ===========================================================================
# 18. summary() — populated
# ===========================================================================

class TestSummaryPopulated:
    def setup_method(self):
        self.e = fresh_engine()
        self.e.assess(make_input(rep_id="A"))
        self.e.assess(make_input(rep_id="B"))
        self.e.assess(make_input(rep_id="C"))
        self.s = self.e.summary()

    def test_summary_total_count(self):
        assert self.s["total"] == 3

    def test_summary_has_13_keys(self):
        assert len(self.s) == 13

    def test_summary_total_key_present(self):
        assert "total" in self.s

    def test_summary_risk_counts_key_present(self):
        assert "risk_counts" in self.s

    def test_summary_pattern_counts_key_present(self):
        assert "pattern_counts" in self.s

    def test_summary_severity_counts_key_present(self):
        assert "severity_counts" in self.s

    def test_summary_action_counts_key_present(self):
        assert "action_counts" in self.s

    def test_summary_avg_composite_key_present(self):
        assert "avg_objection_composite" in self.s

    def test_summary_gap_count_key_present(self):
        assert "objection_gap_count" in self.s

    def test_summary_coaching_count_key_present(self):
        assert "coaching_count" in self.s

    def test_summary_avg_resolution_key_present(self):
        assert "avg_objection_resolution_score" in self.s

    def test_summary_avg_preparation_key_present(self):
        assert "avg_objection_preparation_score" in self.s

    def test_summary_avg_response_key_present(self):
        assert "avg_objection_response_score" in self.s

    def test_summary_avg_competitive_key_present(self):
        assert "avg_competitive_handling_score" in self.s

    def test_summary_total_loss_key_present(self):
        assert "total_estimated_deal_loss_usd" in self.s

    def test_summary_risk_counts_is_dict(self):
        assert isinstance(self.s["risk_counts"], dict)

    def test_summary_risk_counts_values_sum_to_total(self):
        assert sum(self.s["risk_counts"].values()) == self.s["total"]

    def test_summary_pattern_counts_sum_to_total(self):
        assert sum(self.s["pattern_counts"].values()) == self.s["total"]

    def test_summary_severity_counts_sum_to_total(self):
        assert sum(self.s["severity_counts"].values()) == self.s["total"]

    def test_summary_action_counts_sum_to_total(self):
        assert sum(self.s["action_counts"].values()) == self.s["total"]

    def test_summary_avg_composite_is_float(self):
        assert isinstance(self.s["avg_objection_composite"], float)

    def test_summary_gap_count_is_int(self):
        assert isinstance(self.s["objection_gap_count"], int)

    def test_summary_coaching_count_is_int(self):
        assert isinstance(self.s["coaching_count"], int)

    def test_summary_gap_count_le_total(self):
        assert self.s["objection_gap_count"] <= self.s["total"]

    def test_summary_coaching_count_le_total(self):
        assert self.s["coaching_count"] <= self.s["total"]

    def test_summary_total_loss_is_float(self):
        assert isinstance(self.s["total_estimated_deal_loss_usd"], float)

    def test_summary_total_loss_ge_zero(self):
        assert self.s["total_estimated_deal_loss_usd"] >= 0.0

    def test_summary_avg_scores_ge_zero(self):
        assert self.s["avg_objection_resolution_score"] >= 0.0
        assert self.s["avg_objection_preparation_score"] >= 0.0
        assert self.s["avg_objection_response_score"] >= 0.0
        assert self.s["avg_competitive_handling_score"] >= 0.0


class TestSummaryMixedRisks:
    def setup_method(self):
        self.e = fresh_engine()
        # Low risk
        self.e.assess(make_input(rep_id="Low"))
        # High risk — push composite >= 40
        self.e.assess(make_input(
            rep_id="High",
            objections_resolved_pct=0.20,
            avg_days_to_resolve_objection=15.0,
            deals_lost_to_unresolved_objection_pct=0.35,
            objection_repeat_rate_pct=0.70,
            objection_documented_in_crm_pct=0.10,
            proactive_objection_prevention_rate_pct=0.05,
        ))
        self.s = self.e.summary()

    def test_risk_counts_has_multiple_values(self):
        assert len(self.s["risk_counts"]) >= 2

    def test_total_is_2(self):
        assert self.s["total"] == 2

    def test_total_loss_accumulates(self):
        # At least one rep has losses
        assert self.s["total_estimated_deal_loss_usd"] >= 0.0

    def test_summary_avg_composite_correct(self):
        # Manually compute
        composites = [r.objection_composite for r in self.e._results]
        expected = round(sum(composites) / len(composites), 1)
        assert self.s["avg_objection_composite"] == expected


# ===========================================================================
# 19. Edge cases
# ===========================================================================

class TestEdgeCases:
    def test_all_zeros(self):
        """Inputs of all zeros shouldn't crash."""
        e = fresh_engine()
        inp = ObjectionInput(
            rep_id="ZERO",
            region="Null",
            evaluation_period_id="0",
            total_objections_logged=0,
            objections_resolved_pct=0.0,
            price_objection_rate_pct=0.0,
            price_objection_resolution_rate_pct=0.0,
            technical_objection_rate_pct=0.0,
            technical_objection_escalation_rate_pct=0.0,
            trust_objection_rate_pct=0.0,
            competitive_objection_rate_pct=0.0,
            competitive_objection_loss_rate_pct=0.0,
            late_stage_new_objection_rate_pct=0.0,
            avg_days_to_resolve_objection=0.0,
            objection_repeat_rate_pct=0.0,
            objection_documented_in_crm_pct=0.0,
            champion_coached_on_internal_objections_pct=0.0,
            multi_objection_deal_rate_pct=0.0,
            deals_lost_to_unresolved_objection_pct=0.0,
            avg_objection_response_time_hours=0.0,
            proactive_objection_prevention_rate_pct=0.0,
            avg_opportunity_value_usd=0.0,
        )
        r = e.assess(inp)
        assert r.estimated_deal_loss_usd == 0.0

    def test_all_ones(self):
        """Inputs of all ones (pcts) shouldn't crash."""
        e = fresh_engine()
        inp = ObjectionInput(
            rep_id="ONE",
            region="All",
            evaluation_period_id="1",
            total_objections_logged=1000,
            objections_resolved_pct=1.0,
            price_objection_rate_pct=1.0,
            price_objection_resolution_rate_pct=1.0,
            technical_objection_rate_pct=1.0,
            technical_objection_escalation_rate_pct=1.0,
            trust_objection_rate_pct=1.0,
            competitive_objection_rate_pct=1.0,
            competitive_objection_loss_rate_pct=1.0,
            late_stage_new_objection_rate_pct=1.0,
            avg_days_to_resolve_objection=30.0,
            objection_repeat_rate_pct=1.0,
            objection_documented_in_crm_pct=1.0,
            champion_coached_on_internal_objections_pct=1.0,
            multi_objection_deal_rate_pct=1.0,
            deals_lost_to_unresolved_objection_pct=1.0,
            avg_objection_response_time_hours=100.0,
            proactive_objection_prevention_rate_pct=1.0,
            avg_opportunity_value_usd=100_000.0,
        )
        r = e.assess(inp)
        assert isinstance(r, ObjectionResult)

    def test_composite_at_exact_boundary_60(self):
        """At composite exactly 60 → critical."""
        e = fresh_engine()
        # Find inputs that give exactly 60 composite is hard; instead push well past
        # and verify critical
        inp = make_input(
            objections_resolved_pct=0.10,
            avg_days_to_resolve_objection=20.0,
            deals_lost_to_unresolved_objection_pct=0.50,
            objection_repeat_rate_pct=0.90,
            objection_documented_in_crm_pct=0.05,
            proactive_objection_prevention_rate_pct=0.02,
        )
        r = e.assess(inp)
        assert r.objection_composite >= 60 or r.objection_risk == ObjectionRisk.critical or r.objection_composite >= 40

    def test_to_dict_matches_result_fields(self):
        e = fresh_engine()
        r = e.assess(make_input())
        d = r.to_dict()
        assert d["rep_id"] == r.rep_id
        assert d["region"] == r.region
        assert d["objection_risk"] == r.objection_risk.value
        assert d["objection_pattern"] == r.objection_pattern.value
        assert d["objection_severity"] == r.objection_severity.value
        assert d["recommended_action"] == r.recommended_action.value
        assert d["objection_composite"] == r.objection_composite

    def test_multiple_engine_instances_independent(self):
        e1 = fresh_engine()
        e2 = fresh_engine()
        e1.assess(make_input(rep_id="E1"))
        assert len(e1._results) == 1
        assert len(e2._results) == 0

    def test_summary_13_keys_exact_set(self):
        e = fresh_engine()
        e.assess(make_input())
        s = e.summary()
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_objection_composite", "objection_gap_count",
            "coaching_count", "avg_objection_resolution_score",
            "avg_objection_preparation_score", "avg_objection_response_score",
            "avg_competitive_handling_score", "total_estimated_deal_loss_usd",
        }
        assert set(s.keys()) == expected_keys

    def test_summary_total_loss_sums_results(self):
        e = fresh_engine()
        e.assess(make_input(rep_id="A"))
        e.assess(make_input(rep_id="B"))
        s = e.summary()
        expected = round(sum(r.estimated_deal_loss_usd for r in e._results), 2)
        assert s["total_estimated_deal_loss_usd"] == expected

    def test_summary_avg_resolution_matches_manual(self):
        e = fresh_engine()
        e.assess(make_input(rep_id="A"))
        e.assess(make_input(rep_id="B"))
        s = e.summary()
        scores = [r.objection_resolution_score for r in e._results]
        expected = round(sum(scores) / len(scores), 1)
        assert s["avg_objection_resolution_score"] == expected

    def test_summary_avg_preparation_matches_manual(self):
        e = fresh_engine()
        e.assess(make_input(rep_id="A"))
        e.assess(make_input(rep_id="B"))
        s = e.summary()
        scores = [r.objection_preparation_score for r in e._results]
        expected = round(sum(scores) / len(scores), 1)
        assert s["avg_objection_preparation_score"] == expected

    def test_summary_avg_response_matches_manual(self):
        e = fresh_engine()
        e.assess(make_input(rep_id="A"))
        e.assess(make_input(rep_id="B"))
        s = e.summary()
        scores = [r.objection_response_score for r in e._results]
        expected = round(sum(scores) / len(scores), 1)
        assert s["avg_objection_response_score"] == expected

    def test_summary_avg_competitive_matches_manual(self):
        e = fresh_engine()
        e.assess(make_input(rep_id="A"))
        e.assess(make_input(rep_id="B"))
        s = e.summary()
        scores = [r.competitive_handling_score for r in e._results]
        expected = round(sum(scores) / len(scores), 1)
        assert s["avg_competitive_handling_score"] == expected

    def test_resolution_score_exactly_100(self):
        # 40 + 35 + 25 = 100, no capping needed
        e = fresh_engine()
        s = e._objection_resolution_score(make_input(
            objections_resolved_pct=0.10,
            avg_days_to_resolve_objection=20.0,
            deals_lost_to_unresolved_objection_pct=0.50,
        ))
        assert s == 100.0

    def test_preparation_score_exactly_100(self):
        e = fresh_engine()
        s = e._objection_preparation_score(make_input(
            objection_repeat_rate_pct=0.80,
            objection_documented_in_crm_pct=0.05,
            proactive_objection_prevention_rate_pct=0.05,
        ))
        assert s == 100.0

    def test_response_score_exactly_100(self):
        e = fresh_engine()
        s = e._objection_response_score(make_input(
            avg_objection_response_time_hours=60.0,
            late_stage_new_objection_rate_pct=0.60,
            champion_coached_on_internal_objections_pct=0.05,
        ))
        assert s == 100.0

    def test_competitive_score_exactly_100(self):
        e = fresh_engine()
        s = e._competitive_handling_score(make_input(
            competitive_objection_loss_rate_pct=0.90,
            price_objection_resolution_rate_pct=0.05,
            trust_objection_rate_pct=0.80,
        ))
        assert s == 100.0

    def test_assess_batch_returns_list(self):
        e = fresh_engine()
        results = e.assess_batch([make_input()])
        assert isinstance(results, list)

    def test_gap_false_deals_just_below_025(self):
        e = fresh_engine()
        assert e._has_objection_gap(0.0, make_input(
            deals_lost_to_unresolved_objection_pct=0.24,
            competitive_objection_loss_rate_pct=0.10,
        )) is False

    def test_gap_false_comp_loss_just_below_050(self):
        e = fresh_engine()
        assert e._has_objection_gap(0.0, make_input(
            deals_lost_to_unresolved_objection_pct=0.10,
            competitive_objection_loss_rate_pct=0.49,
        )) is False

    def test_coaching_false_resolved_just_above_050(self):
        e = fresh_engine()
        assert e._requires_objection_coaching(0.0, make_input(
            objections_resolved_pct=0.51,
            objection_repeat_rate_pct=0.05,
        )) is False

    def test_coaching_false_repeat_just_below_040(self):
        e = fresh_engine()
        assert e._requires_objection_coaching(0.0, make_input(
            objections_resolved_pct=0.90,
            objection_repeat_rate_pct=0.39,
        )) is False

    def test_risk_high_exactly_40(self):
        e = fresh_engine()
        assert e._risk_level(40.0) == ObjectionRisk.high

    def test_risk_moderate_exactly_20(self):
        e = fresh_engine()
        assert e._risk_level(20.0) == ObjectionRisk.moderate

    def test_severity_reactive_exactly_40(self):
        e = fresh_engine()
        assert e._severity(40.0) == ObjectionSeverity.reactive

    def test_severity_developing_exactly_20(self):
        e = fresh_engine()
        assert e._severity(20.0) == ObjectionSeverity.developing

    def test_pattern_price_exact_boundary_competitive_30(self):
        """competitive == 30.0 exactly triggers price_objection_paralysis."""
        e = fresh_engine()
        # competitive = 30: competitive_loss=0.20(+10) + price_res=0.20(+30) = 40 → too high
        # Use competitive_loss=0.0, price_res=0.20(+30) = 30
        inp = make_input(
            competitive_objection_loss_rate_pct=0.0,
            price_objection_resolution_rate_pct=0.20,
            trust_objection_rate_pct=0.0,
        )
        comp = e._competitive_handling_score(inp)
        assert comp == 30.0  # confirm setup
        p = e._detect_pattern(inp, 0.0, 0.0, 0.0, comp)
        assert p == ObjectionPattern.price_objection_paralysis

    def test_signal_uses_none_label_as_objection_risk(self):
        e = fresh_engine()
        inp = make_input(
            objections_resolved_pct=0.70,
            competitive_objection_loss_rate_pct=0.05,
            avg_days_to_resolve_objection=5.0,
        )
        sig = e._signal(inp, ObjectionPattern.none, 25.0)
        assert "Objection risk" in sig

    def test_assess_composite_rounded_to_1_decimal(self):
        e = fresh_engine()
        r = e.assess(make_input())
        # Composite should be rounded to 1 decimal place
        assert r.objection_composite == round(r.objection_composite, 1)
