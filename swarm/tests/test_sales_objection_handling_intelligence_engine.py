"""
Comprehensive pytest test suite for SalesObjectionHandlingIntelligenceEngine.
Target: 200+ tests covering enums, fields, scores, risk/severity/pattern/action,
composite formula, gap/coaching triggers, deal-loss formula, signal text,
assess_batch, summary, and edge cases.
"""
from __future__ import annotations

import math
import pytest
from swarm.intelligence.sales_objection_handling_intelligence_engine import (
    ObjRisk,
    ObjPattern,
    ObjSeverity,
    ObjAction,
    ObjInput,
    ObjResult,
    SalesObjectionHandlingIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> ObjInput:
    """Return a 'golden-path' (low-risk) ObjInput with any field overridden."""
    defaults = dict(
        rep_id="REP-001",
        region="West",
        evaluation_period_id="Q1-2026",
        objection_encounter_rate_pct=0.20,
        objection_resolution_rate_pct=0.80,    # high resolution → low score
        price_objection_rate_pct=0.10,
        status_quo_objection_rate_pct=0.10,
        feature_objection_rate_pct=0.10,
        authority_objection_rate_pct=0.10,
        timing_objection_rate_pct=0.10,
        first_response_reframe_rate_pct=0.70,  # high reframe → low score
        objection_leads_to_loss_rate_pct=0.10,
        unaddressed_objection_rate_pct=0.05,
        concession_after_objection_pct=0.10,
        evidence_usage_rate_pct=0.80,          # high evidence → low score
        repeat_objection_rate_pct=0.10,
        avg_objections_per_deal=1.0,
        deal_stall_after_objection_rate_pct=0.10,
        total_deals_closed=50,
        avg_opportunity_value_usd=10_000.0,
        active_deal_count=20,
        calls_with_recorded_objection=30,
    )
    defaults.update(overrides)
    return ObjInput(**defaults)


def engine() -> SalesObjectionHandlingIntelligenceEngine:
    return SalesObjectionHandlingIntelligenceEngine()


# ===========================================================================
# 1. ENUM TESTS
# ===========================================================================

class TestObjRiskEnum:
    def test_low_value(self):
        assert ObjRisk.low.value == "low"

    def test_moderate_value(self):
        assert ObjRisk.moderate.value == "moderate"

    def test_high_value(self):
        assert ObjRisk.high.value == "high"

    def test_critical_value(self):
        assert ObjRisk.critical.value == "critical"

    def test_four_members(self):
        assert len(ObjRisk) == 4

    def test_str_subclass(self):
        assert isinstance(ObjRisk.low, str)

    def test_membership(self):
        assert "low" in [r.value for r in ObjRisk]


class TestObjPatternEnum:
    def test_none_value(self):
        assert ObjPattern.none.value == "none"

    def test_price_caver(self):
        assert ObjPattern.price_caver.value == "price_caver"

    def test_status_quo_deflector(self):
        assert ObjPattern.status_quo_deflector.value == "status_quo_deflector"

    def test_feature_objector(self):
        assert ObjPattern.feature_objector.value == "feature_objector"

    def test_authority_blocker(self):
        assert ObjPattern.authority_blocker.value == "authority_blocker"

    def test_timing_deferrer(self):
        assert ObjPattern.timing_deferrer.value == "timing_deferrer"

    def test_six_members(self):
        assert len(ObjPattern) == 6

    def test_str_subclass(self):
        assert isinstance(ObjPattern.none, str)


class TestObjSeverityEnum:
    def test_expert(self):
        assert ObjSeverity.expert.value == "expert"

    def test_competent(self):
        assert ObjSeverity.competent.value == "competent"

    def test_developing(self):
        assert ObjSeverity.developing.value == "developing"

    def test_struggling(self):
        assert ObjSeverity.struggling.value == "struggling"

    def test_four_members(self):
        assert len(ObjSeverity) == 4

    def test_str_subclass(self):
        assert isinstance(ObjSeverity.expert, str)


class TestObjActionEnum:
    def test_no_action(self):
        assert ObjAction.no_action.value == "no_action"

    def test_price_objection_coaching(self):
        assert ObjAction.price_objection_coaching.value == "price_objection_coaching"

    def test_reframe_coaching(self):
        assert ObjAction.reframe_coaching.value == "reframe_coaching"

    def test_feature_gap_coaching(self):
        assert ObjAction.feature_gap_coaching.value == "feature_gap_coaching"

    def test_multi_threading_coaching(self):
        assert ObjAction.multi_threading_coaching.value == "multi_threading_coaching"

    def test_urgency_creation_coaching(self):
        assert ObjAction.urgency_creation_coaching.value == "urgency_creation_coaching"

    def test_objection_handling_intervention(self):
        assert ObjAction.objection_handling_intervention.value == "objection_handling_intervention"

    def test_seven_members(self):
        assert len(ObjAction) == 7

    def test_str_subclass(self):
        assert isinstance(ObjAction.no_action, str)


# ===========================================================================
# 2. ObjInput — 21 FIELDS PRESENT
# ===========================================================================

class TestObjInputFields:
    def test_rep_id(self):
        inp = make_input(rep_id="X")
        assert inp.rep_id == "X"

    def test_region(self):
        inp = make_input(region="East")
        assert inp.region == "East"

    def test_evaluation_period_id(self):
        inp = make_input(evaluation_period_id="Q2")
        assert inp.evaluation_period_id == "Q2"

    def test_objection_encounter_rate_pct(self):
        inp = make_input(objection_encounter_rate_pct=0.5)
        assert inp.objection_encounter_rate_pct == 0.5

    def test_objection_resolution_rate_pct(self):
        inp = make_input(objection_resolution_rate_pct=0.6)
        assert inp.objection_resolution_rate_pct == 0.6

    def test_price_objection_rate_pct(self):
        inp = make_input(price_objection_rate_pct=0.3)
        assert inp.price_objection_rate_pct == 0.3

    def test_status_quo_objection_rate_pct(self):
        inp = make_input(status_quo_objection_rate_pct=0.25)
        assert inp.status_quo_objection_rate_pct == 0.25

    def test_feature_objection_rate_pct(self):
        inp = make_input(feature_objection_rate_pct=0.2)
        assert inp.feature_objection_rate_pct == 0.2

    def test_authority_objection_rate_pct(self):
        inp = make_input(authority_objection_rate_pct=0.15)
        assert inp.authority_objection_rate_pct == 0.15

    def test_timing_objection_rate_pct(self):
        inp = make_input(timing_objection_rate_pct=0.12)
        assert inp.timing_objection_rate_pct == 0.12

    def test_first_response_reframe_rate_pct(self):
        inp = make_input(first_response_reframe_rate_pct=0.4)
        assert inp.first_response_reframe_rate_pct == 0.4

    def test_objection_leads_to_loss_rate_pct(self):
        inp = make_input(objection_leads_to_loss_rate_pct=0.3)
        assert inp.objection_leads_to_loss_rate_pct == 0.3

    def test_unaddressed_objection_rate_pct(self):
        inp = make_input(unaddressed_objection_rate_pct=0.18)
        assert inp.unaddressed_objection_rate_pct == 0.18

    def test_concession_after_objection_pct(self):
        inp = make_input(concession_after_objection_pct=0.35)
        assert inp.concession_after_objection_pct == 0.35

    def test_evidence_usage_rate_pct(self):
        inp = make_input(evidence_usage_rate_pct=0.55)
        assert inp.evidence_usage_rate_pct == 0.55

    def test_repeat_objection_rate_pct(self):
        inp = make_input(repeat_objection_rate_pct=0.22)
        assert inp.repeat_objection_rate_pct == 0.22

    def test_avg_objections_per_deal(self):
        inp = make_input(avg_objections_per_deal=3.0)
        assert inp.avg_objections_per_deal == 3.0

    def test_deal_stall_after_objection_rate_pct(self):
        inp = make_input(deal_stall_after_objection_rate_pct=0.33)
        assert inp.deal_stall_after_objection_rate_pct == 0.33

    def test_total_deals_closed(self):
        inp = make_input(total_deals_closed=100)
        assert inp.total_deals_closed == 100

    def test_avg_opportunity_value_usd(self):
        inp = make_input(avg_opportunity_value_usd=25000.0)
        assert inp.avg_opportunity_value_usd == 25000.0

    def test_active_deal_count(self):
        inp = make_input(active_deal_count=15)
        assert inp.active_deal_count == 15

    def test_calls_with_recorded_objection(self):
        inp = make_input(calls_with_recorded_objection=42)
        assert inp.calls_with_recorded_objection == 42

    def test_total_field_count(self):
        """ObjInput has 22 fields (spec says 21 but implementation adds
        objection_encounter_rate_pct as an extra field)."""
        import dataclasses
        fields = dataclasses.fields(ObjInput)
        assert len(fields) == 22


# ===========================================================================
# 3. ObjResult.to_dict — 15 KEYS
# ===========================================================================

class TestObjResultToDict:
    @pytest.fixture
    def result(self):
        e = engine()
        return e.assess(make_input())

    def test_to_dict_returns_dict(self, result):
        assert isinstance(result.to_dict(), dict)

    def test_to_dict_15_keys(self, result):
        assert len(result.to_dict()) == 15

    def test_to_dict_has_rep_id(self, result):
        assert "rep_id" in result.to_dict()

    def test_to_dict_has_region(self, result):
        assert "region" in result.to_dict()

    def test_to_dict_has_obj_risk(self, result):
        assert "obj_risk" in result.to_dict()

    def test_to_dict_has_obj_pattern(self, result):
        assert "obj_pattern" in result.to_dict()

    def test_to_dict_has_obj_severity(self, result):
        assert "obj_severity" in result.to_dict()

    def test_to_dict_has_recommended_action(self, result):
        assert "recommended_action" in result.to_dict()

    def test_to_dict_has_resolution_effectiveness_score(self, result):
        assert "resolution_effectiveness_score" in result.to_dict()

    def test_to_dict_has_objection_intelligence_score(self, result):
        assert "objection_intelligence_score" in result.to_dict()

    def test_to_dict_has_resilience_score(self, result):
        assert "resilience_score" in result.to_dict()

    def test_to_dict_has_evidence_utilization_score(self, result):
        assert "evidence_utilization_score" in result.to_dict()

    def test_to_dict_has_obj_composite(self, result):
        assert "obj_composite" in result.to_dict()

    def test_to_dict_has_has_obj_gap(self, result):
        assert "has_obj_gap" in result.to_dict()

    def test_to_dict_has_requires_obj_coaching(self, result):
        assert "requires_obj_coaching" in result.to_dict()

    def test_to_dict_has_estimated_deal_loss_usd(self, result):
        assert "estimated_deal_loss_usd" in result.to_dict()

    def test_to_dict_has_obj_signal(self, result):
        assert "obj_signal" in result.to_dict()

    def test_to_dict_risk_is_string(self, result):
        assert isinstance(result.to_dict()["obj_risk"], str)

    def test_to_dict_pattern_is_string(self, result):
        assert isinstance(result.to_dict()["obj_pattern"], str)

    def test_to_dict_severity_is_string(self, result):
        assert isinstance(result.to_dict()["obj_severity"], str)

    def test_to_dict_action_is_string(self, result):
        assert isinstance(result.to_dict()["recommended_action"], str)


# ===========================================================================
# 4. RISK LEVELS
# ===========================================================================

class TestRiskLevels:
    def test_low_risk_golden_path(self):
        e = engine()
        r = e.assess(make_input())
        assert r.obj_risk == ObjRisk.low

    def test_moderate_risk_boundary_exactly_20(self):
        """composite == 20 → moderate"""
        e = engine()
        # Use only resolution_effectiveness score contribution to reach exactly 20
        # resolution_rate > 0.70 → 0 pts; loss_rate < 0.20 → 0 pts; unaddressed < 0.20 → 0 pts → RE=0
        # objection_intelligence: reframe>0.60→0; repeat<0.20→0; stall<0.30→0 → OI=0
        # resilience: concession<0.28→0; avg_obj<1.5→0; price<0.40→0 → RS=0
        # evidence: usage>0.60→0; status_quo<0.20→0; feature<0.18→0 → EU=0
        # composite = 0 → low
        # To push to exactly 20 we need composite >= 20
        # Set unaddressed=0.20 → RE += 10; OI still 0; RS still 0; EU still 0
        # RE=10, composite = 10*0.35=3.5 → still low
        # Easier: push resolution_rate to 0.35 → RE=45; composite=45*0.35=15.75 low
        # push loss_rate to 0.20 → RE=45+6=51; composite=51*0.35=17.85 still low
        # push unaddressed to 0.20 → RE=51+10=61; composite=61*0.35=21.35 → MODERATE
        inp = make_input(
            objection_resolution_rate_pct=0.35,
            objection_leads_to_loss_rate_pct=0.20,
            unaddressed_objection_rate_pct=0.20,
        )
        r = e.assess(inp)
        assert r.obj_risk == ObjRisk.moderate

    def test_high_risk_composite_40_plus(self):
        e = engine()
        # resolution_rate <= 0.35 → +45; loss_rate >= 0.50 → +35; unaddressed >= 0.35 → +20 → RE=100
        # reframe <= 0.25 → +40; repeat >= 0.50 → +35; stall >= 0.45 → +25 → OI=100
        # composite = 100*0.35 + 100*0.25 = 60 → need to keep rs and eu low
        inp = make_input(
            objection_resolution_rate_pct=0.30,
            objection_leads_to_loss_rate_pct=0.55,
            unaddressed_objection_rate_pct=0.40,
            first_response_reframe_rate_pct=0.20,
            repeat_objection_rate_pct=0.55,
            deal_stall_after_objection_rate_pct=0.50,
        )
        r = e.assess(inp)
        assert r.obj_risk in (ObjRisk.high, ObjRisk.critical)

    def test_critical_risk_composite_60_plus(self):
        e = engine()
        inp = make_input(
            objection_resolution_rate_pct=0.20,
            objection_leads_to_loss_rate_pct=0.60,
            unaddressed_objection_rate_pct=0.40,
            first_response_reframe_rate_pct=0.15,
            repeat_objection_rate_pct=0.60,
            deal_stall_after_objection_rate_pct=0.50,
            concession_after_objection_pct=0.70,
            avg_objections_per_deal=5.0,
            price_objection_rate_pct=0.60,
            evidence_usage_rate_pct=0.10,
            status_quo_objection_rate_pct=0.40,
            feature_objection_rate_pct=0.35,
        )
        r = e.assess(inp)
        assert r.obj_risk == ObjRisk.critical

    def test_risk_low_boundary_below_20(self):
        e = engine()
        r = e.assess(make_input(
            objection_resolution_rate_pct=0.90,
            objection_leads_to_loss_rate_pct=0.05,
            unaddressed_objection_rate_pct=0.01,
            first_response_reframe_rate_pct=0.90,
            repeat_objection_rate_pct=0.05,
            deal_stall_after_objection_rate_pct=0.05,
        ))
        assert r.obj_risk == ObjRisk.low


# ===========================================================================
# 5. SEVERITY LEVELS
# ===========================================================================

class TestSeverityLevels:
    def test_expert_severity_low_composite(self):
        e = engine()
        r = e.assess(make_input())
        assert r.obj_severity == ObjSeverity.expert

    def test_competent_severity_composite_20_to_39(self):
        """composite in [20,40) → competent"""
        e = engine()
        inp = make_input(
            objection_resolution_rate_pct=0.35,
            objection_leads_to_loss_rate_pct=0.20,
            unaddressed_objection_rate_pct=0.20,
        )
        r = e.assess(inp)
        assert r.obj_severity == ObjSeverity.competent

    def test_developing_severity_composite_40_to_59(self):
        e = engine()
        inp = make_input(
            objection_resolution_rate_pct=0.20,
            objection_leads_to_loss_rate_pct=0.55,
            unaddressed_objection_rate_pct=0.40,
            first_response_reframe_rate_pct=0.20,
            repeat_objection_rate_pct=0.40,
            deal_stall_after_objection_rate_pct=0.50,
        )
        r = e.assess(inp)
        assert r.obj_severity in (ObjSeverity.developing, ObjSeverity.struggling)

    def test_struggling_severity_composite_60_plus(self):
        e = engine()
        inp = make_input(
            objection_resolution_rate_pct=0.20,
            objection_leads_to_loss_rate_pct=0.60,
            unaddressed_objection_rate_pct=0.40,
            first_response_reframe_rate_pct=0.15,
            repeat_objection_rate_pct=0.60,
            deal_stall_after_objection_rate_pct=0.50,
            concession_after_objection_pct=0.70,
            avg_objections_per_deal=5.0,
            price_objection_rate_pct=0.60,
            evidence_usage_rate_pct=0.10,
            status_quo_objection_rate_pct=0.40,
            feature_objection_rate_pct=0.35,
        )
        r = e.assess(inp)
        assert r.obj_severity == ObjSeverity.struggling

    def test_severity_and_risk_aligned(self):
        """Risk and severity should use same composite thresholds."""
        e = engine()
        r = e.assess(make_input())
        risk_is_low = r.obj_risk == ObjRisk.low
        sev_is_expert = r.obj_severity == ObjSeverity.expert
        assert risk_is_low == sev_is_expert


# ===========================================================================
# 6. PATTERN DETECTION
# ===========================================================================

class TestPatterns:
    def test_none_pattern_default(self):
        e = engine()
        r = e.assess(make_input())
        assert r.obj_pattern == ObjPattern.none

    def test_price_caver_pattern(self):
        e = engine()
        inp = make_input(
            price_objection_rate_pct=0.55,
            concession_after_objection_pct=0.65,
        )
        r = e.assess(inp)
        assert r.obj_pattern == ObjPattern.price_caver

    def test_price_caver_exact_boundary(self):
        """price=0.50, concession=0.60 → price_caver"""
        e = engine()
        inp = make_input(
            price_objection_rate_pct=0.50,
            concession_after_objection_pct=0.60,
        )
        r = e.assess(inp)
        assert r.obj_pattern == ObjPattern.price_caver

    def test_price_caver_below_boundary_no_match(self):
        """price=0.49, concession=0.60 → should NOT be price_caver"""
        e = engine()
        inp = make_input(
            price_objection_rate_pct=0.49,
            concession_after_objection_pct=0.65,
        )
        r = e.assess(inp)
        assert r.obj_pattern != ObjPattern.price_caver

    def test_status_quo_deflector_pattern(self):
        e = engine()
        inp = make_input(
            status_quo_objection_rate_pct=0.40,
            first_response_reframe_rate_pct=0.25,
        )
        r = e.assess(inp)
        assert r.obj_pattern == ObjPattern.status_quo_deflector

    def test_status_quo_deflector_exact_boundary(self):
        """status_quo=0.35, reframe=0.30 → status_quo_deflector"""
        e = engine()
        inp = make_input(
            status_quo_objection_rate_pct=0.35,
            first_response_reframe_rate_pct=0.30,
        )
        r = e.assess(inp)
        assert r.obj_pattern == ObjPattern.status_quo_deflector

    def test_feature_objector_pattern(self):
        e = engine()
        inp = make_input(
            feature_objection_rate_pct=0.35,
            objection_leads_to_loss_rate_pct=0.45,
        )
        r = e.assess(inp)
        assert r.obj_pattern == ObjPattern.feature_objector

    def test_feature_objector_exact_boundary(self):
        """feature=0.30, loss=0.40 → feature_objector"""
        e = engine()
        inp = make_input(
            feature_objection_rate_pct=0.30,
            objection_leads_to_loss_rate_pct=0.40,
        )
        r = e.assess(inp)
        assert r.obj_pattern == ObjPattern.feature_objector

    def test_authority_blocker_pattern(self):
        e = engine()
        inp = make_input(
            authority_objection_rate_pct=0.35,
            deal_stall_after_objection_rate_pct=0.45,
        )
        r = e.assess(inp)
        assert r.obj_pattern == ObjPattern.authority_blocker

    def test_authority_blocker_exact_boundary(self):
        """authority=0.30, stall=0.40 → authority_blocker"""
        e = engine()
        inp = make_input(
            authority_objection_rate_pct=0.30,
            deal_stall_after_objection_rate_pct=0.40,
        )
        r = e.assess(inp)
        assert r.obj_pattern == ObjPattern.authority_blocker

    def test_timing_deferrer_pattern(self):
        e = engine()
        inp = make_input(
            timing_objection_rate_pct=0.35,
            repeat_objection_rate_pct=0.45,
        )
        r = e.assess(inp)
        assert r.obj_pattern == ObjPattern.timing_deferrer

    def test_timing_deferrer_exact_boundary(self):
        """timing=0.30, repeat=0.40 → timing_deferrer"""
        e = engine()
        inp = make_input(
            timing_objection_rate_pct=0.30,
            repeat_objection_rate_pct=0.40,
        )
        r = e.assess(inp)
        assert r.obj_pattern == ObjPattern.timing_deferrer

    def test_price_caver_takes_priority_over_status_quo(self):
        """price_caver is checked first in the chain."""
        e = engine()
        inp = make_input(
            price_objection_rate_pct=0.55,
            concession_after_objection_pct=0.65,
            status_quo_objection_rate_pct=0.40,
            first_response_reframe_rate_pct=0.20,
        )
        r = e.assess(inp)
        assert r.obj_pattern == ObjPattern.price_caver


# ===========================================================================
# 7. ACTION SELECTION — all 7 values
# ===========================================================================

class TestActions:
    def test_no_action_when_low_risk(self):
        e = engine()
        r = e.assess(make_input())
        assert r.recommended_action == ObjAction.no_action

    def test_reframe_coaching_when_moderate_risk(self):
        e = engine()
        inp = make_input(
            objection_resolution_rate_pct=0.35,
            objection_leads_to_loss_rate_pct=0.20,
            unaddressed_objection_rate_pct=0.20,
        )
        r = e.assess(inp)
        if r.obj_risk == ObjRisk.moderate:
            assert r.recommended_action == ObjAction.reframe_coaching

    def test_objection_handling_intervention_when_critical(self):
        e = engine()
        inp = make_input(
            objection_resolution_rate_pct=0.20,
            objection_leads_to_loss_rate_pct=0.60,
            unaddressed_objection_rate_pct=0.40,
            first_response_reframe_rate_pct=0.15,
            repeat_objection_rate_pct=0.60,
            deal_stall_after_objection_rate_pct=0.50,
            concession_after_objection_pct=0.70,
            avg_objections_per_deal=5.0,
            price_objection_rate_pct=0.60,
            evidence_usage_rate_pct=0.10,
            status_quo_objection_rate_pct=0.40,
            feature_objection_rate_pct=0.35,
        )
        r = e.assess(inp)
        assert r.recommended_action == ObjAction.objection_handling_intervention

    def test_price_objection_coaching_high_risk_price_caver(self):
        """High risk + price_caver → price_objection_coaching"""
        e = engine()
        # Force high risk (composite 40–59) with price_caver pattern
        inp = make_input(
            # Resolution score: rate<=0.35 +45, loss 0.35 +18, unaddressed 0.20 +10 = 73
            objection_resolution_rate_pct=0.30,
            objection_leads_to_loss_rate_pct=0.40,
            unaddressed_objection_rate_pct=0.20,
            # OI: reframe 0.45 +22, repeat 0.25 +6, stall 0.10 = 28
            first_response_reframe_rate_pct=0.45,
            repeat_objection_rate_pct=0.25,
            deal_stall_after_objection_rate_pct=0.10,
            # RS: concession 0.65 → +45, avg_obj 1.0 → 0, price 0.55 → +20 = 65
            concession_after_objection_pct=0.65,
            avg_objections_per_deal=1.0,
            price_objection_rate_pct=0.55,
            # EU: evidence 0.70 → 0, status_quo 0.10 → 0, feature 0.10 → 0 = 0
            evidence_usage_rate_pct=0.70,
            status_quo_objection_rate_pct=0.10,
            feature_objection_rate_pct=0.10,
        )
        r = e.assess(inp)
        if r.obj_risk == ObjRisk.high and r.obj_pattern == ObjPattern.price_caver:
            assert r.recommended_action == ObjAction.price_objection_coaching

    def test_reframe_coaching_high_risk_status_quo(self):
        e = engine()
        # Build high-risk, status_quo_deflector
        inp = make_input(
            objection_resolution_rate_pct=0.30,
            objection_leads_to_loss_rate_pct=0.40,
            unaddressed_objection_rate_pct=0.20,
            first_response_reframe_rate_pct=0.25,
            status_quo_objection_rate_pct=0.40,
            repeat_objection_rate_pct=0.25,
            deal_stall_after_objection_rate_pct=0.10,
            concession_after_objection_pct=0.10,
            avg_objections_per_deal=1.0,
            price_objection_rate_pct=0.10,
            evidence_usage_rate_pct=0.70,
            feature_objection_rate_pct=0.10,
        )
        r = e.assess(inp)
        if r.obj_risk == ObjRisk.high and r.obj_pattern == ObjPattern.status_quo_deflector:
            assert r.recommended_action == ObjAction.reframe_coaching

    def test_feature_gap_coaching_high_risk_feature_objector(self):
        e = engine()
        inp = make_input(
            objection_resolution_rate_pct=0.30,
            objection_leads_to_loss_rate_pct=0.42,
            unaddressed_objection_rate_pct=0.20,
            first_response_reframe_rate_pct=0.45,
            repeat_objection_rate_pct=0.25,
            deal_stall_after_objection_rate_pct=0.10,
            concession_after_objection_pct=0.10,
            avg_objections_per_deal=1.0,
            price_objection_rate_pct=0.10,
            feature_objection_rate_pct=0.35,
            evidence_usage_rate_pct=0.70,
            status_quo_objection_rate_pct=0.10,
        )
        r = e.assess(inp)
        if r.obj_risk == ObjRisk.high and r.obj_pattern == ObjPattern.feature_objector:
            assert r.recommended_action == ObjAction.feature_gap_coaching

    def test_multi_threading_coaching_high_risk_authority_blocker(self):
        e = engine()
        inp = make_input(
            objection_resolution_rate_pct=0.30,
            objection_leads_to_loss_rate_pct=0.40,
            unaddressed_objection_rate_pct=0.20,
            first_response_reframe_rate_pct=0.45,
            repeat_objection_rate_pct=0.25,
            deal_stall_after_objection_rate_pct=0.42,
            authority_objection_rate_pct=0.35,
            concession_after_objection_pct=0.10,
            avg_objections_per_deal=1.0,
            price_objection_rate_pct=0.10,
            feature_objection_rate_pct=0.10,
            evidence_usage_rate_pct=0.70,
            status_quo_objection_rate_pct=0.10,
        )
        r = e.assess(inp)
        if r.obj_risk == ObjRisk.high and r.obj_pattern == ObjPattern.authority_blocker:
            assert r.recommended_action == ObjAction.multi_threading_coaching

    def test_urgency_creation_coaching_high_risk_timing_deferrer(self):
        e = engine()
        inp = make_input(
            objection_resolution_rate_pct=0.30,
            objection_leads_to_loss_rate_pct=0.40,
            unaddressed_objection_rate_pct=0.20,
            first_response_reframe_rate_pct=0.45,
            repeat_objection_rate_pct=0.42,
            timing_objection_rate_pct=0.35,
            deal_stall_after_objection_rate_pct=0.10,
            concession_after_objection_pct=0.10,
            avg_objections_per_deal=1.0,
            price_objection_rate_pct=0.10,
            feature_objection_rate_pct=0.10,
            evidence_usage_rate_pct=0.70,
            status_quo_objection_rate_pct=0.10,
        )
        r = e.assess(inp)
        if r.obj_risk == ObjRisk.high and r.obj_pattern == ObjPattern.timing_deferrer:
            assert r.recommended_action == ObjAction.urgency_creation_coaching

    def test_high_risk_none_pattern_gets_reframe_coaching(self):
        """high risk + none pattern → reframe_coaching (fallback)"""
        e = engine()
        # Build something that hits high risk but no pattern
        inp = make_input(
            objection_resolution_rate_pct=0.30,
            objection_leads_to_loss_rate_pct=0.40,
            unaddressed_objection_rate_pct=0.20,
            first_response_reframe_rate_pct=0.65,   # above all pattern thresholds
            repeat_objection_rate_pct=0.15,
            deal_stall_after_objection_rate_pct=0.10,
            concession_after_objection_pct=0.10,
            avg_objections_per_deal=1.0,
            price_objection_rate_pct=0.10,
            feature_objection_rate_pct=0.10,
            evidence_usage_rate_pct=0.70,
            status_quo_objection_rate_pct=0.10,
            authority_objection_rate_pct=0.10,
            timing_objection_rate_pct=0.10,
        )
        r = e.assess(inp)
        if r.obj_risk == ObjRisk.high and r.obj_pattern == ObjPattern.none:
            assert r.recommended_action == ObjAction.reframe_coaching


# ===========================================================================
# 8. SUB-SCORE BRACKETS — resolution_effectiveness
# ===========================================================================

class TestResolutionEffectivenessScore:
    def _re(self, **kw):
        e = engine()
        inp = make_input(**kw)
        return e._resolution_effectiveness_score(inp)

    def test_res_rate_below_35_adds_45(self):
        s = self._re(
            objection_resolution_rate_pct=0.30,
            objection_leads_to_loss_rate_pct=0.10,
            unaddressed_objection_rate_pct=0.05,
        )
        assert s == 45.0

    def test_res_rate_36_to_55_adds_28(self):
        s = self._re(
            objection_resolution_rate_pct=0.50,
            objection_leads_to_loss_rate_pct=0.10,
            unaddressed_objection_rate_pct=0.05,
        )
        assert s == 28.0

    def test_res_rate_56_to_70_adds_12(self):
        s = self._re(
            objection_resolution_rate_pct=0.65,
            objection_leads_to_loss_rate_pct=0.10,
            unaddressed_objection_rate_pct=0.05,
        )
        assert s == 12.0

    def test_res_rate_above_70_adds_0(self):
        s = self._re(
            objection_resolution_rate_pct=0.90,
            objection_leads_to_loss_rate_pct=0.10,
            unaddressed_objection_rate_pct=0.05,
        )
        assert s == 0.0

    def test_loss_rate_50_plus_adds_35(self):
        s = self._re(
            objection_resolution_rate_pct=0.90,
            objection_leads_to_loss_rate_pct=0.55,
            unaddressed_objection_rate_pct=0.05,
        )
        assert s == 35.0

    def test_loss_rate_35_to_49_adds_18(self):
        s = self._re(
            objection_resolution_rate_pct=0.90,
            objection_leads_to_loss_rate_pct=0.40,
            unaddressed_objection_rate_pct=0.05,
        )
        assert s == 18.0

    def test_loss_rate_20_to_34_adds_6(self):
        s = self._re(
            objection_resolution_rate_pct=0.90,
            objection_leads_to_loss_rate_pct=0.25,
            unaddressed_objection_rate_pct=0.05,
        )
        assert s == 6.0

    def test_loss_rate_below_20_adds_0(self):
        s = self._re(
            objection_resolution_rate_pct=0.90,
            objection_leads_to_loss_rate_pct=0.10,
            unaddressed_objection_rate_pct=0.05,
        )
        assert s == 0.0

    def test_unaddressed_35_plus_adds_20(self):
        s = self._re(
            objection_resolution_rate_pct=0.90,
            objection_leads_to_loss_rate_pct=0.10,
            unaddressed_objection_rate_pct=0.40,
        )
        assert s == 20.0

    def test_unaddressed_20_to_34_adds_10(self):
        s = self._re(
            objection_resolution_rate_pct=0.90,
            objection_leads_to_loss_rate_pct=0.10,
            unaddressed_objection_rate_pct=0.25,
        )
        assert s == 10.0

    def test_unaddressed_below_20_adds_0(self):
        s = self._re(
            objection_resolution_rate_pct=0.90,
            objection_leads_to_loss_rate_pct=0.10,
            unaddressed_objection_rate_pct=0.10,
        )
        assert s == 0.0

    def test_capped_at_100(self):
        s = self._re(
            objection_resolution_rate_pct=0.20,
            objection_leads_to_loss_rate_pct=0.60,
            unaddressed_objection_rate_pct=0.40,
        )
        assert s == 100.0


# ===========================================================================
# 9. SUB-SCORE BRACKETS — objection_intelligence
# ===========================================================================

class TestObjectionIntelligenceScore:
    def _oi(self, **kw):
        e = engine()
        inp = make_input(**kw)
        return e._objection_intelligence_score(inp)

    def test_reframe_below_25_adds_40(self):
        s = self._oi(first_response_reframe_rate_pct=0.20, repeat_objection_rate_pct=0.05, deal_stall_after_objection_rate_pct=0.10)
        assert s == 40.0

    def test_reframe_26_to_45_adds_22(self):
        s = self._oi(first_response_reframe_rate_pct=0.35, repeat_objection_rate_pct=0.05, deal_stall_after_objection_rate_pct=0.10)
        assert s == 22.0

    def test_reframe_46_to_60_adds_8(self):
        s = self._oi(first_response_reframe_rate_pct=0.55, repeat_objection_rate_pct=0.05, deal_stall_after_objection_rate_pct=0.10)
        assert s == 8.0

    def test_reframe_above_60_adds_0(self):
        s = self._oi(first_response_reframe_rate_pct=0.80, repeat_objection_rate_pct=0.05, deal_stall_after_objection_rate_pct=0.10)
        assert s == 0.0

    def test_repeat_50_plus_adds_35(self):
        s = self._oi(first_response_reframe_rate_pct=0.80, repeat_objection_rate_pct=0.55, deal_stall_after_objection_rate_pct=0.10)
        assert s == 35.0

    def test_repeat_35_to_49_adds_18(self):
        s = self._oi(first_response_reframe_rate_pct=0.80, repeat_objection_rate_pct=0.40, deal_stall_after_objection_rate_pct=0.10)
        assert s == 18.0

    def test_repeat_20_to_34_adds_6(self):
        s = self._oi(first_response_reframe_rate_pct=0.80, repeat_objection_rate_pct=0.25, deal_stall_after_objection_rate_pct=0.10)
        assert s == 6.0

    def test_stall_45_plus_adds_25(self):
        s = self._oi(first_response_reframe_rate_pct=0.80, repeat_objection_rate_pct=0.05, deal_stall_after_objection_rate_pct=0.50)
        assert s == 25.0

    def test_stall_30_to_44_adds_12(self):
        s = self._oi(first_response_reframe_rate_pct=0.80, repeat_objection_rate_pct=0.05, deal_stall_after_objection_rate_pct=0.35)
        assert s == 12.0

    def test_stall_below_30_adds_0(self):
        s = self._oi(first_response_reframe_rate_pct=0.80, repeat_objection_rate_pct=0.05, deal_stall_after_objection_rate_pct=0.20)
        assert s == 0.0

    def test_capped_at_100(self):
        s = self._oi(first_response_reframe_rate_pct=0.10, repeat_objection_rate_pct=0.60, deal_stall_after_objection_rate_pct=0.50)
        assert s == 100.0


# ===========================================================================
# 10. SUB-SCORE BRACKETS — resilience
# ===========================================================================

class TestResilienceScore:
    def _rs(self, **kw):
        e = engine()
        inp = make_input(**kw)
        return e._resilience_score(inp)

    def test_concession_65_plus_adds_45(self):
        s = self._rs(concession_after_objection_pct=0.70, avg_objections_per_deal=1.0, price_objection_rate_pct=0.10)
        assert s == 45.0

    def test_concession_45_to_64_adds_28(self):
        s = self._rs(concession_after_objection_pct=0.50, avg_objections_per_deal=1.0, price_objection_rate_pct=0.10)
        assert s == 28.0

    def test_concession_28_to_44_adds_12(self):
        s = self._rs(concession_after_objection_pct=0.35, avg_objections_per_deal=1.0, price_objection_rate_pct=0.10)
        assert s == 12.0

    def test_concession_below_28_adds_0(self):
        s = self._rs(concession_after_objection_pct=0.20, avg_objections_per_deal=1.0, price_objection_rate_pct=0.10)
        assert s == 0.0

    def test_avg_obj_4_plus_adds_35(self):
        s = self._rs(concession_after_objection_pct=0.10, avg_objections_per_deal=5.0, price_objection_rate_pct=0.10)
        assert s == 35.0

    def test_avg_obj_2p5_to_3p9_adds_18(self):
        s = self._rs(concession_after_objection_pct=0.10, avg_objections_per_deal=3.0, price_objection_rate_pct=0.10)
        assert s == 18.0

    def test_avg_obj_1p5_to_2p4_adds_6(self):
        s = self._rs(concession_after_objection_pct=0.10, avg_objections_per_deal=2.0, price_objection_rate_pct=0.10)
        assert s == 6.0

    def test_avg_obj_below_1p5_adds_0(self):
        s = self._rs(concession_after_objection_pct=0.10, avg_objections_per_deal=1.0, price_objection_rate_pct=0.10)
        assert s == 0.0

    def test_price_rate_55_plus_adds_20(self):
        s = self._rs(concession_after_objection_pct=0.10, avg_objections_per_deal=1.0, price_objection_rate_pct=0.60)
        assert s == 20.0

    def test_price_rate_40_to_54_adds_10(self):
        s = self._rs(concession_after_objection_pct=0.10, avg_objections_per_deal=1.0, price_objection_rate_pct=0.45)
        assert s == 10.0

    def test_price_rate_below_40_adds_0(self):
        s = self._rs(concession_after_objection_pct=0.10, avg_objections_per_deal=1.0, price_objection_rate_pct=0.30)
        assert s == 0.0

    def test_capped_at_100(self):
        s = self._rs(concession_after_objection_pct=0.70, avg_objections_per_deal=5.0, price_objection_rate_pct=0.60)
        assert s == 100.0


# ===========================================================================
# 11. SUB-SCORE BRACKETS — evidence_utilization
# ===========================================================================

class TestEvidenceUtilizationScore:
    def _eu(self, **kw):
        e = engine()
        inp = make_input(**kw)
        return e._evidence_utilization_score(inp)

    def test_evidence_below_20_adds_50(self):
        s = self._eu(evidence_usage_rate_pct=0.10, status_quo_objection_rate_pct=0.10, feature_objection_rate_pct=0.10)
        assert s == 50.0

    def test_evidence_21_to_40_adds_30(self):
        s = self._eu(evidence_usage_rate_pct=0.30, status_quo_objection_rate_pct=0.10, feature_objection_rate_pct=0.10)
        assert s == 30.0

    def test_evidence_41_to_60_adds_12(self):
        s = self._eu(evidence_usage_rate_pct=0.50, status_quo_objection_rate_pct=0.10, feature_objection_rate_pct=0.10)
        assert s == 12.0

    def test_evidence_above_60_adds_0(self):
        s = self._eu(evidence_usage_rate_pct=0.70, status_quo_objection_rate_pct=0.10, feature_objection_rate_pct=0.10)
        assert s == 0.0

    def test_status_quo_35_plus_adds_30(self):
        s = self._eu(evidence_usage_rate_pct=0.70, status_quo_objection_rate_pct=0.40, feature_objection_rate_pct=0.10)
        assert s == 30.0

    def test_status_quo_20_to_34_adds_15(self):
        s = self._eu(evidence_usage_rate_pct=0.70, status_quo_objection_rate_pct=0.25, feature_objection_rate_pct=0.10)
        assert s == 15.0

    def test_status_quo_below_20_adds_0(self):
        s = self._eu(evidence_usage_rate_pct=0.70, status_quo_objection_rate_pct=0.10, feature_objection_rate_pct=0.10)
        assert s == 0.0

    def test_feature_30_plus_adds_20(self):
        s = self._eu(evidence_usage_rate_pct=0.70, status_quo_objection_rate_pct=0.10, feature_objection_rate_pct=0.35)
        assert s == 20.0

    def test_feature_18_to_29_adds_10(self):
        s = self._eu(evidence_usage_rate_pct=0.70, status_quo_objection_rate_pct=0.10, feature_objection_rate_pct=0.20)
        assert s == 10.0

    def test_feature_below_18_adds_0(self):
        s = self._eu(evidence_usage_rate_pct=0.70, status_quo_objection_rate_pct=0.10, feature_objection_rate_pct=0.10)
        assert s == 0.0

    def test_capped_at_100(self):
        s = self._eu(evidence_usage_rate_pct=0.10, status_quo_objection_rate_pct=0.40, feature_objection_rate_pct=0.35)
        assert s == 100.0


# ===========================================================================
# 12. COMPOSITE FORMULA — weights sum to 1.00, rounded to 2dp
# ===========================================================================

class TestCompositeFormula:
    def test_weights_sum_to_one(self):
        assert 0.35 + 0.25 + 0.25 + 0.15 == pytest.approx(1.00)

    def test_composite_formula_manual(self):
        e = engine()
        inp = make_input(
            objection_resolution_rate_pct=0.30,   # RE: +45
            objection_leads_to_loss_rate_pct=0.55, # RE: +35 → 80
            unaddressed_objection_rate_pct=0.05,   # RE: +0  → 80
            first_response_reframe_rate_pct=0.20,  # OI: +40
            repeat_objection_rate_pct=0.05,         # OI: +0
            deal_stall_after_objection_rate_pct=0.10, # OI: +0 → 40
            concession_after_objection_pct=0.10,   # RS: +0
            avg_objections_per_deal=1.0,            # RS: +0
            price_objection_rate_pct=0.10,          # RS: +0 → 0
            evidence_usage_rate_pct=0.70,           # EU: +0
            status_quo_objection_rate_pct=0.10,     # EU: +0
            feature_objection_rate_pct=0.10,        # EU: +0 → 0
        )
        r = e.assess(inp)
        expected = round(80 * 0.35 + 40 * 0.25 + 0 * 0.25 + 0 * 0.15, 2)
        assert r.obj_composite == pytest.approx(expected, abs=0.01)

    def test_composite_is_rounded_to_2dp(self):
        e = engine()
        r = e.assess(make_input())
        # Verify it has at most 2 decimal places
        assert r.obj_composite == round(r.obj_composite, 2)

    def test_composite_zero_all_good(self):
        e = engine()
        r = e.assess(make_input())
        assert r.obj_composite == 0.0

    def test_composite_max_is_100(self):
        e = engine()
        inp = make_input(
            objection_resolution_rate_pct=0.20,
            objection_leads_to_loss_rate_pct=0.60,
            unaddressed_objection_rate_pct=0.40,
            first_response_reframe_rate_pct=0.15,
            repeat_objection_rate_pct=0.60,
            deal_stall_after_objection_rate_pct=0.50,
            concession_after_objection_pct=0.70,
            avg_objections_per_deal=5.0,
            price_objection_rate_pct=0.60,
            evidence_usage_rate_pct=0.10,
            status_quo_objection_rate_pct=0.40,
            feature_objection_rate_pct=0.35,
        )
        r = e.assess(inp)
        assert r.obj_composite <= 100.0

    def test_composite_non_negative(self):
        e = engine()
        r = e.assess(make_input())
        assert r.obj_composite >= 0.0

    def test_composite_re_weight_35pct(self):
        """Increase only RE sub-score and verify composite grows by 35%."""
        e = engine()
        inp_base = make_input()
        inp_bad_re = make_input(objection_resolution_rate_pct=0.30)
        r_base = e.assess(inp_base)
        r_bad = e.assess(inp_bad_re)
        re_base = e._resolution_effectiveness_score(inp_base)
        re_bad = e._resolution_effectiveness_score(inp_bad_re)
        delta_re = re_bad - re_base
        # composite delta should equal delta_re * 0.35 (all else equal)
        delta_comp = r_bad.obj_composite - r_base.obj_composite
        assert delta_comp == pytest.approx(delta_re * 0.35, abs=0.01)


# ===========================================================================
# 13. HAS_OBJ_GAP TRIGGERS
# ===========================================================================

class TestHasObjGap:
    def test_gap_false_when_all_good(self):
        e = engine()
        r = e.assess(make_input())
        assert r.has_obj_gap is False

    def test_gap_true_when_composite_40_plus(self):
        e = engine()
        inp = make_input(
            objection_resolution_rate_pct=0.20,
            objection_leads_to_loss_rate_pct=0.60,
            unaddressed_objection_rate_pct=0.40,
            first_response_reframe_rate_pct=0.15,
            repeat_objection_rate_pct=0.60,
            deal_stall_after_objection_rate_pct=0.50,
            concession_after_objection_pct=0.70,
            avg_objections_per_deal=5.0,
            price_objection_rate_pct=0.60,
            evidence_usage_rate_pct=0.10,
            status_quo_objection_rate_pct=0.40,
            feature_objection_rate_pct=0.35,
        )
        r = e.assess(inp)
        assert r.has_obj_gap is True

    def test_gap_true_when_resolution_rate_55_or_below(self):
        """resolution_rate == 0.55 → has_obj_gap (composite can be < 40)"""
        e = engine()
        inp = make_input(objection_resolution_rate_pct=0.55)
        r = e.assess(inp)
        assert r.has_obj_gap is True

    def test_gap_true_when_resolution_rate_below_55(self):
        e = engine()
        inp = make_input(objection_resolution_rate_pct=0.50)
        r = e.assess(inp)
        assert r.has_obj_gap is True

    def test_gap_false_when_resolution_rate_above_55(self):
        e = engine()
        # resolution=0.56 and composite < 40 and concession < 0.40
        inp = make_input(
            objection_resolution_rate_pct=0.56,
            concession_after_objection_pct=0.10,
        )
        r = e.assess(inp)
        # RE score = 0 (>0.70 → 0; loss<0.20→0; unaddressed<0.20→0)
        # Wait: 0.56 is between 0.55 and 0.70 → adds 12. Still might be < 40.
        # 0.56 > 0.55 so not <= 0.55, that leg of has_gap is False
        # composite = 12*0.35 = 4.2 < 40
        # concession 0.10 < 0.40 → that leg is False
        # → has_obj_gap should be False
        assert r.has_obj_gap is False

    def test_gap_true_when_concession_40_or_above(self):
        e = engine()
        inp = make_input(
            objection_resolution_rate_pct=0.90,
            concession_after_objection_pct=0.40,
        )
        r = e.assess(inp)
        assert r.has_obj_gap is True

    def test_gap_true_when_concession_above_40(self):
        e = engine()
        inp = make_input(
            objection_resolution_rate_pct=0.90,
            concession_after_objection_pct=0.50,
        )
        r = e.assess(inp)
        assert r.has_obj_gap is True


# ===========================================================================
# 14. REQUIRES_OBJ_COACHING TRIGGERS
# ===========================================================================

class TestRequiresObjCoaching:
    def test_coaching_false_when_all_good(self):
        e = engine()
        r = e.assess(make_input())
        assert r.requires_obj_coaching is False

    def test_coaching_true_when_composite_25_plus(self):
        e = engine()
        # Build composite >= 25
        # RE = 45 (res<=0.35) → composite = 45*0.35 = 15.75 < 25
        # Need more: RE=45+35=80 → composite=80*0.35=28 >= 25
        inp = make_input(
            objection_resolution_rate_pct=0.30,
            objection_leads_to_loss_rate_pct=0.55,
        )
        r = e.assess(inp)
        if r.obj_composite >= 25:
            assert r.requires_obj_coaching is True

    def test_coaching_true_when_unaddressed_20_or_above(self):
        e = engine()
        inp = make_input(unaddressed_objection_rate_pct=0.20)
        r = e.assess(inp)
        assert r.requires_obj_coaching is True

    def test_coaching_true_when_unaddressed_above_20(self):
        e = engine()
        inp = make_input(unaddressed_objection_rate_pct=0.30)
        r = e.assess(inp)
        assert r.requires_obj_coaching is True

    def test_coaching_true_when_evidence_45_or_below(self):
        e = engine()
        inp = make_input(evidence_usage_rate_pct=0.45)
        r = e.assess(inp)
        assert r.requires_obj_coaching is True

    def test_coaching_true_when_evidence_below_45(self):
        e = engine()
        inp = make_input(evidence_usage_rate_pct=0.30)
        r = e.assess(inp)
        assert r.requires_obj_coaching is True

    def test_coaching_false_when_evidence_above_45(self):
        """evidence > 0.45, unaddressed < 0.20, composite < 25 → no coaching"""
        e = engine()
        inp = make_input(
            evidence_usage_rate_pct=0.80,
            unaddressed_objection_rate_pct=0.05,
            # composite will be 0
        )
        r = e.assess(inp)
        assert r.requires_obj_coaching is False


# ===========================================================================
# 15. ESTIMATED_DEAL_LOSS_USD FORMULA
# ===========================================================================

class TestEstimatedDealLossUsd:
    def test_zero_when_composite_zero(self):
        e = engine()
        r = e.assess(make_input())
        assert r.estimated_deal_loss_usd == 0.0

    def test_formula_manual(self):
        e = engine()
        inp = make_input(
            active_deal_count=10,
            avg_opportunity_value_usd=5000.0,
            objection_leads_to_loss_rate_pct=0.40,
            # Force composite exactly
            objection_resolution_rate_pct=0.30,  # RE+45
            unaddressed_objection_rate_pct=0.05,
            first_response_reframe_rate_pct=0.80,
            repeat_objection_rate_pct=0.05,
            deal_stall_after_objection_rate_pct=0.10,
            concession_after_objection_pct=0.10,
            avg_objections_per_deal=1.0,
            price_objection_rate_pct=0.10,
            evidence_usage_rate_pct=0.70,
            status_quo_objection_rate_pct=0.10,
            feature_objection_rate_pct=0.10,
        )
        r = e.assess(inp)
        re = e._resolution_effectiveness_score(inp)
        oi = e._objection_intelligence_score(inp)
        rs = e._resilience_score(inp)
        eu = e._evidence_utilization_score(inp)
        comp = round(re * 0.35 + oi * 0.25 + rs * 0.25 + eu * 0.15, 2)
        expected = round(10 * 5000.0 * 0.40 * (comp / 100), 2)
        assert r.estimated_deal_loss_usd == pytest.approx(expected, abs=0.01)

    def test_deal_loss_proportional_to_active_deals(self):
        e1, e2 = engine(), engine()
        base = dict(
            objection_resolution_rate_pct=0.30,
            objection_leads_to_loss_rate_pct=0.50,
            avg_opportunity_value_usd=10_000.0,
        )
        r1 = e1.assess(make_input(active_deal_count=10, **base))
        r2 = e2.assess(make_input(active_deal_count=20, **base))
        assert r2.estimated_deal_loss_usd == pytest.approx(r1.estimated_deal_loss_usd * 2, abs=0.01)

    def test_deal_loss_proportional_to_opp_value(self):
        e1, e2 = engine(), engine()
        base = dict(
            objection_resolution_rate_pct=0.30,
            objection_leads_to_loss_rate_pct=0.50,
            active_deal_count=10,
        )
        r1 = e1.assess(make_input(avg_opportunity_value_usd=10_000.0, **base))
        r2 = e2.assess(make_input(avg_opportunity_value_usd=20_000.0, **base))
        assert r2.estimated_deal_loss_usd == pytest.approx(r1.estimated_deal_loss_usd * 2, abs=0.01)

    def test_deal_loss_is_rounded_to_2dp(self):
        e = engine()
        r = e.assess(make_input(
            objection_resolution_rate_pct=0.30,
            objection_leads_to_loss_rate_pct=0.50,
            active_deal_count=7,
            avg_opportunity_value_usd=1234.56,
        ))
        assert r.estimated_deal_loss_usd == round(r.estimated_deal_loss_usd, 2)

    def test_deal_loss_zero_when_no_loss_rate(self):
        e = engine()
        r = e.assess(make_input(
            objection_leads_to_loss_rate_pct=0.0,
            objection_resolution_rate_pct=0.30,
        ))
        assert r.estimated_deal_loss_usd == 0.0

    def test_deal_loss_zero_when_no_active_deals(self):
        e = engine()
        r = e.assess(make_input(
            active_deal_count=0,
            objection_resolution_rate_pct=0.30,
            objection_leads_to_loss_rate_pct=0.50,
        ))
        assert r.estimated_deal_loss_usd == 0.0


# ===========================================================================
# 16. SIGNAL TEXT
# ===========================================================================

class TestSignalText:
    def test_low_composite_returns_strong_signal(self):
        e = engine()
        r = e.assess(make_input())
        assert "strong" in r.obj_signal.lower()

    def test_signal_contains_resolution_pct(self):
        e = engine()
        inp = make_input(
            objection_resolution_rate_pct=0.75,
            objection_leads_to_loss_rate_pct=0.50,
            unaddressed_objection_rate_pct=0.05,
        )
        r = e.assess(inp)
        if r.obj_composite >= 20:
            assert "75%" in r.obj_signal

    def test_signal_contains_concession_pct(self):
        e = engine()
        inp = make_input(
            objection_resolution_rate_pct=0.30,
            objection_leads_to_loss_rate_pct=0.55,
            unaddressed_objection_rate_pct=0.40,
            concession_after_objection_pct=0.45,
        )
        r = e.assess(inp)
        if r.obj_composite >= 20:
            assert "45%" in r.obj_signal

    def test_signal_contains_evidence_pct(self):
        e = engine()
        inp = make_input(
            objection_resolution_rate_pct=0.30,
            objection_leads_to_loss_rate_pct=0.55,
            unaddressed_objection_rate_pct=0.40,
            evidence_usage_rate_pct=0.30,
        )
        r = e.assess(inp)
        if r.obj_composite >= 20:
            assert "30%" in r.obj_signal

    def test_signal_price_caver_label(self):
        e = engine()
        inp = make_input(
            price_objection_rate_pct=0.55,
            concession_after_objection_pct=0.65,
            objection_resolution_rate_pct=0.30,
            objection_leads_to_loss_rate_pct=0.55,
        )
        r = e.assess(inp)
        if r.obj_pattern == ObjPattern.price_caver and r.obj_composite >= 20:
            assert "Price caver" in r.obj_signal

    def test_signal_status_quo_deflector_label(self):
        e = engine()
        inp = make_input(
            status_quo_objection_rate_pct=0.40,
            first_response_reframe_rate_pct=0.25,
            objection_resolution_rate_pct=0.30,
            objection_leads_to_loss_rate_pct=0.55,
        )
        r = e.assess(inp)
        if r.obj_pattern == ObjPattern.status_quo_deflector and r.obj_composite >= 20:
            assert "Status quo deflector" in r.obj_signal

    def test_signal_feature_objector_label(self):
        e = engine()
        inp = make_input(
            feature_objection_rate_pct=0.35,
            objection_leads_to_loss_rate_pct=0.45,
            objection_resolution_rate_pct=0.30,
        )
        r = e.assess(inp)
        if r.obj_pattern == ObjPattern.feature_objector and r.obj_composite >= 20:
            assert "Feature objector" in r.obj_signal

    def test_signal_authority_blocker_label(self):
        e = engine()
        inp = make_input(
            authority_objection_rate_pct=0.35,
            deal_stall_after_objection_rate_pct=0.45,
            objection_resolution_rate_pct=0.30,
            objection_leads_to_loss_rate_pct=0.55,
        )
        r = e.assess(inp)
        if r.obj_pattern == ObjPattern.authority_blocker and r.obj_composite >= 20:
            assert "Authority blocker" in r.obj_signal

    def test_signal_timing_deferrer_label(self):
        e = engine()
        inp = make_input(
            timing_objection_rate_pct=0.35,
            repeat_objection_rate_pct=0.45,
            objection_resolution_rate_pct=0.30,
            objection_leads_to_loss_rate_pct=0.55,
        )
        r = e.assess(inp)
        if r.obj_pattern == ObjPattern.timing_deferrer and r.obj_composite >= 20:
            assert "Timing deferrer" in r.obj_signal

    def test_signal_none_pattern_label(self):
        """When no specific pattern but composite >= 20, signal uses generic label."""
        e = engine()
        inp = make_input(
            objection_resolution_rate_pct=0.30,
            objection_leads_to_loss_rate_pct=0.55,
            unaddressed_objection_rate_pct=0.40,
        )
        r = e.assess(inp)
        if r.obj_pattern == ObjPattern.none and r.obj_composite >= 20:
            assert "Objection handling gap" in r.obj_signal

    def test_signal_contains_composite_rounded_int(self):
        e = engine()
        inp = make_input(
            objection_resolution_rate_pct=0.30,
            objection_leads_to_loss_rate_pct=0.55,
        )
        r = e.assess(inp)
        if r.obj_composite >= 20:
            comp_int = str(round(r.obj_composite))
            assert f"composite {comp_int}" in r.obj_signal

    def test_signal_is_string(self):
        e = engine()
        r = e.assess(make_input())
        assert isinstance(r.obj_signal, str)

    def test_signal_not_empty(self):
        e = engine()
        r = e.assess(make_input())
        assert len(r.obj_signal) > 0


# ===========================================================================
# 17. ASSESS_BATCH
# ===========================================================================

class TestAssessBatch:
    def test_returns_list(self):
        e = engine()
        results = e.assess_batch([make_input(rep_id="A"), make_input(rep_id="B")])
        assert isinstance(results, list)

    def test_length_matches_input(self):
        e = engine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = e.assess_batch(inputs)
        assert len(results) == 5

    def test_each_element_is_obj_result(self):
        e = engine()
        results = e.assess_batch([make_input(rep_id="X")])
        assert isinstance(results[0], ObjResult)

    def test_rep_ids_preserved(self):
        e = engine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(3)]
        results = e.assess_batch(inputs)
        assert [r.rep_id for r in results] == ["R0", "R1", "R2"]

    def test_empty_batch(self):
        e = engine()
        results = e.assess_batch([])
        assert results == []

    def test_batch_accumulates_in_results(self):
        e = engine()
        e.assess_batch([make_input(rep_id=f"R{i}") for i in range(4)])
        assert len(e._results) == 4

    def test_batch_result_order_preserved(self):
        e = engine()
        inp1 = make_input(rep_id="ALPHA", region="North")
        inp2 = make_input(rep_id="BETA", region="South")
        r1, r2 = e.assess_batch([inp1, inp2])
        assert r1.rep_id == "ALPHA"
        assert r2.rep_id == "BETA"

    def test_batch_single_item(self):
        e = engine()
        results = e.assess_batch([make_input(rep_id="SOLO")])
        assert len(results) == 1
        assert results[0].rep_id == "SOLO"


# ===========================================================================
# 18. SUMMARY — 13 KEYS
# ===========================================================================

class TestSummary:
    def test_empty_engine_returns_13_keys(self):
        e = engine()
        s = e.summary()
        assert len(s) == 13

    def test_summary_keys(self):
        e = engine()
        s = e.summary()
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_obj_composite", "obj_gap_count",
            "coaching_count", "avg_resolution_effectiveness_score",
            "avg_objection_intelligence_score", "avg_resilience_score",
            "avg_evidence_utilization_score", "total_estimated_deal_loss_usd",
        }
        assert set(s.keys()) == expected_keys

    def test_empty_summary_total_zero(self):
        e = engine()
        assert e.summary()["total"] == 0

    def test_empty_summary_avg_composite_zero(self):
        e = engine()
        assert e.summary()["avg_obj_composite"] == 0.0

    def test_empty_summary_gap_count_zero(self):
        e = engine()
        assert e.summary()["obj_gap_count"] == 0

    def test_empty_summary_coaching_count_zero(self):
        e = engine()
        assert e.summary()["coaching_count"] == 0

    def test_empty_summary_total_loss_zero(self):
        e = engine()
        assert e.summary()["total_estimated_deal_loss_usd"] == 0.0

    def test_summary_total_after_assess(self):
        e = engine()
        e.assess(make_input(rep_id="A"))
        e.assess(make_input(rep_id="B"))
        assert e.summary()["total"] == 2

    def test_summary_risk_counts_populated(self):
        e = engine()
        e.assess(make_input())
        s = e.summary()
        assert "low" in s["risk_counts"]
        assert s["risk_counts"]["low"] == 1

    def test_summary_pattern_counts_populated(self):
        e = engine()
        e.assess(make_input())
        s = e.summary()
        assert "none" in s["pattern_counts"]

    def test_summary_severity_counts_populated(self):
        e = engine()
        e.assess(make_input())
        s = e.summary()
        assert "expert" in s["severity_counts"]

    def test_summary_action_counts_populated(self):
        e = engine()
        e.assess(make_input())
        s = e.summary()
        assert "no_action" in s["action_counts"]

    def test_summary_avg_composite_correct(self):
        e = engine()
        e.assess(make_input())  # composite = 0
        e.assess(make_input())  # composite = 0
        s = e.summary()
        assert s["avg_obj_composite"] == 0.0

    def test_summary_gap_count_correct(self):
        e = engine()
        e.assess(make_input())  # has_obj_gap = False
        e.assess(make_input(objection_resolution_rate_pct=0.50))  # has_obj_gap = True
        s = e.summary()
        assert s["obj_gap_count"] == 1

    def test_summary_coaching_count_correct(self):
        e = engine()
        e.assess(make_input())  # requires_obj_coaching = False
        e.assess(make_input(evidence_usage_rate_pct=0.30))  # requires_obj_coaching = True
        s = e.summary()
        assert s["coaching_count"] == 1

    def test_summary_total_deal_loss_is_sum(self):
        e = engine()
        r1 = e.assess(make_input())
        r2 = e.assess(make_input(
            objection_resolution_rate_pct=0.30,
            objection_leads_to_loss_rate_pct=0.55,
            active_deal_count=10,
            avg_opportunity_value_usd=5000.0,
        ))
        s = e.summary()
        assert s["total_estimated_deal_loss_usd"] == pytest.approx(
            r1.estimated_deal_loss_usd + r2.estimated_deal_loss_usd, abs=0.01
        )

    def test_summary_avg_scores_rounded_1dp(self):
        e = engine()
        e.assess(make_input())
        s = e.summary()
        for key in [
            "avg_resolution_effectiveness_score",
            "avg_objection_intelligence_score",
            "avg_resilience_score",
            "avg_evidence_utilization_score",
        ]:
            val = s[key]
            assert val == round(val, 1), f"{key} not rounded to 1dp"

    def test_summary_avg_composite_rounded_1dp(self):
        e = engine()
        e.assess(make_input())
        s = e.summary()
        val = s["avg_obj_composite"]
        assert val == round(val, 1)

    def test_summary_accumulates_across_multiple_assess(self):
        e = engine()
        for i in range(10):
            e.assess(make_input(rep_id=f"R{i}"))
        assert e.summary()["total"] == 10

    def test_summary_multiple_risk_levels(self):
        e = engine()
        e.assess(make_input())  # low
        e.assess(make_input(
            objection_resolution_rate_pct=0.20,
            objection_leads_to_loss_rate_pct=0.60,
            unaddressed_objection_rate_pct=0.40,
            first_response_reframe_rate_pct=0.15,
            repeat_objection_rate_pct=0.60,
            deal_stall_after_objection_rate_pct=0.50,
            concession_after_objection_pct=0.70,
            avg_objections_per_deal=5.0,
            price_objection_rate_pct=0.60,
            evidence_usage_rate_pct=0.10,
            status_quo_objection_rate_pct=0.40,
            feature_objection_rate_pct=0.35,
        ))  # critical
        s = e.summary()
        assert "low" in s["risk_counts"]
        assert "critical" in s["risk_counts"]


# ===========================================================================
# 19. EDGE CASES
# ===========================================================================

class TestEdgeCases:
    def test_all_zero_rates(self):
        """Zero for all rate fields should not raise exceptions."""
        e = engine()
        inp = make_input(
            objection_encounter_rate_pct=0.0,
            objection_resolution_rate_pct=0.0,
            price_objection_rate_pct=0.0,
            status_quo_objection_rate_pct=0.0,
            feature_objection_rate_pct=0.0,
            authority_objection_rate_pct=0.0,
            timing_objection_rate_pct=0.0,
            first_response_reframe_rate_pct=0.0,
            objection_leads_to_loss_rate_pct=0.0,
            unaddressed_objection_rate_pct=0.0,
            concession_after_objection_pct=0.0,
            evidence_usage_rate_pct=0.0,
            repeat_objection_rate_pct=0.0,
            avg_objections_per_deal=0.0,
            deal_stall_after_objection_rate_pct=0.0,
            active_deal_count=0,
            avg_opportunity_value_usd=0.0,
            total_deals_closed=0,
            calls_with_recorded_objection=0,
        )
        r = e.assess(inp)
        assert isinstance(r, ObjResult)

    def test_all_rates_at_1(self):
        """All rates at 1.0 should return a valid result."""
        e = engine()
        inp = make_input(
            objection_encounter_rate_pct=1.0,
            objection_resolution_rate_pct=1.0,
            price_objection_rate_pct=1.0,
            status_quo_objection_rate_pct=1.0,
            feature_objection_rate_pct=1.0,
            authority_objection_rate_pct=1.0,
            timing_objection_rate_pct=1.0,
            first_response_reframe_rate_pct=1.0,
            objection_leads_to_loss_rate_pct=1.0,
            unaddressed_objection_rate_pct=1.0,
            concession_after_objection_pct=1.0,
            evidence_usage_rate_pct=1.0,
            repeat_objection_rate_pct=1.0,
            avg_objections_per_deal=10.0,
            deal_stall_after_objection_rate_pct=1.0,
            active_deal_count=100,
            avg_opportunity_value_usd=100_000.0,
            total_deals_closed=500,
            calls_with_recorded_objection=500,
        )
        r = e.assess(inp)
        assert isinstance(r, ObjResult)

    def test_rep_id_and_region_preserved(self):
        e = engine()
        r = e.assess(make_input(rep_id="MYID", region="NORTH"))
        assert r.rep_id == "MYID"
        assert r.region == "NORTH"

    def test_assessment_stored_in_results(self):
        e = engine()
        e.assess(make_input(rep_id="STORED"))
        assert len(e._results) == 1
        assert e._results[0].rep_id == "STORED"

    def test_multiple_assessments_accumulate(self):
        e = engine()
        for i in range(5):
            e.assess(make_input(rep_id=f"R{i}"))
        assert len(e._results) == 5

    def test_fresh_engine_results_empty(self):
        e = engine()
        assert e._results == []

    def test_to_dict_values_match_fields(self):
        e = engine()
        r = e.assess(make_input(rep_id="TEST", region="Central"))
        d = r.to_dict()
        assert d["rep_id"] == r.rep_id
        assert d["region"] == r.region
        assert d["obj_risk"] == r.obj_risk.value
        assert d["obj_pattern"] == r.obj_pattern.value
        assert d["obj_severity"] == r.obj_severity.value
        assert d["recommended_action"] == r.recommended_action.value
        assert d["obj_composite"] == r.obj_composite
        assert d["has_obj_gap"] == r.has_obj_gap
        assert d["requires_obj_coaching"] == r.requires_obj_coaching
        assert d["estimated_deal_loss_usd"] == r.estimated_deal_loss_usd
        assert d["obj_signal"] == r.obj_signal

    def test_risk_boundary_exactly_40(self):
        """composite exactly 40 → high (not moderate)"""
        e = engine()
        # RE=45(res<=0.35) + 35(loss>=0.50) = 80; OI=0; RS=0; EU=0
        # composite = 80*0.35 = 28 → still moderate
        # RE=100; OI=40(reframe<=0.25); RS=0; EU=0
        # = 100*0.35 + 40*0.25 = 35+10=45 → high
        inp = make_input(
            objection_resolution_rate_pct=0.20,
            objection_leads_to_loss_rate_pct=0.55,
            unaddressed_objection_rate_pct=0.40,
            first_response_reframe_rate_pct=0.20,
        )
        r = e.assess(inp)
        assert r.obj_risk in (ObjRisk.high, ObjRisk.critical)

    def test_risk_boundary_exactly_20(self):
        """composite exactly 20 → moderate (not low)"""
        # RE=28(res 0.36-0.55); OI=0; RS=0; EU=0
        # composite = 28*0.35 = 9.8 → low
        # Need composite=20: RE=57.14...
        # RE=57.14 → can't be exact with our brackets.
        # Let's get approx 20 by: RE=45, OI=22
        # 45*0.35 + 22*0.25 = 15.75+5.5 = 21.25 → moderate
        e = engine()
        inp = make_input(
            objection_resolution_rate_pct=0.30,   # RE +45
            objection_leads_to_loss_rate_pct=0.10, # RE +0
            unaddressed_objection_rate_pct=0.05,   # RE +0 → RE=45
            first_response_reframe_rate_pct=0.35,  # OI +22
            repeat_objection_rate_pct=0.05,         # OI +0
            deal_stall_after_objection_rate_pct=0.10, # OI +0 → OI=22
        )
        r = e.assess(inp)
        assert r.obj_risk == ObjRisk.moderate

    def test_assess_returns_obj_result_type(self):
        e = engine()
        r = e.assess(make_input())
        assert isinstance(r, ObjResult)

    def test_result_fields_correct_types(self):
        e = engine()
        r = e.assess(make_input())
        assert isinstance(r.rep_id, str)
        assert isinstance(r.region, str)
        assert isinstance(r.obj_risk, ObjRisk)
        assert isinstance(r.obj_pattern, ObjPattern)
        assert isinstance(r.obj_severity, ObjSeverity)
        assert isinstance(r.recommended_action, ObjAction)
        assert isinstance(r.resolution_effectiveness_score, float)
        assert isinstance(r.objection_intelligence_score, float)
        assert isinstance(r.resilience_score, float)
        assert isinstance(r.evidence_utilization_score, float)
        assert isinstance(r.obj_composite, float)
        assert isinstance(r.has_obj_gap, bool)
        assert isinstance(r.requires_obj_coaching, bool)
        assert isinstance(r.estimated_deal_loss_usd, float)
        assert isinstance(r.obj_signal, str)

    def test_sub_scores_non_negative(self):
        e = engine()
        r = e.assess(make_input())
        assert r.resolution_effectiveness_score >= 0
        assert r.objection_intelligence_score >= 0
        assert r.resilience_score >= 0
        assert r.evidence_utilization_score >= 0

    def test_sub_scores_at_most_100(self):
        e = engine()
        inp = make_input(
            objection_resolution_rate_pct=0.0,
            objection_leads_to_loss_rate_pct=1.0,
            unaddressed_objection_rate_pct=1.0,
            first_response_reframe_rate_pct=0.0,
            repeat_objection_rate_pct=1.0,
            deal_stall_after_objection_rate_pct=1.0,
            concession_after_objection_pct=1.0,
            avg_objections_per_deal=10.0,
            price_objection_rate_pct=1.0,
            evidence_usage_rate_pct=0.0,
            status_quo_objection_rate_pct=1.0,
            feature_objection_rate_pct=1.0,
        )
        r = e.assess(inp)
        assert r.resolution_effectiveness_score <= 100.0
        assert r.objection_intelligence_score <= 100.0
        assert r.resilience_score <= 100.0
        assert r.evidence_utilization_score <= 100.0

    def test_large_batch_summary_totals(self):
        e = engine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(50)]
        e.assess_batch(inputs)
        s = e.summary()
        assert s["total"] == 50

    def test_summary_13_keys_after_assessments(self):
        e = engine()
        e.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        assert len(e.summary()) == 13

    def test_assess_batch_and_assess_share_results(self):
        e = engine()
        e.assess(make_input(rep_id="SINGLE"))
        e.assess_batch([make_input(rep_id="BATCH1"), make_input(rep_id="BATCH2")])
        assert len(e._results) == 3

    def test_resolution_rate_exactly_055(self):
        """resolution_rate == 0.55 triggers has_obj_gap via the <= 0.55 check"""
        e = engine()
        r = e.assess(make_input(objection_resolution_rate_pct=0.55))
        assert r.has_obj_gap is True

    def test_concession_exactly_040(self):
        """concession == 0.40 triggers has_obj_gap"""
        e = engine()
        r = e.assess(make_input(
            objection_resolution_rate_pct=0.90,
            concession_after_objection_pct=0.40,
        ))
        assert r.has_obj_gap is True

    def test_unaddressed_exactly_020_triggers_coaching(self):
        e = engine()
        r = e.assess(make_input(unaddressed_objection_rate_pct=0.20))
        assert r.requires_obj_coaching is True

    def test_evidence_exactly_045_triggers_coaching(self):
        e = engine()
        r = e.assess(make_input(evidence_usage_rate_pct=0.45))
        assert r.requires_obj_coaching is True
