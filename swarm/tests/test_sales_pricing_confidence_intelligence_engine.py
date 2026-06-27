"""
Comprehensive pytest test suite for SalesPricingConfidenceIntelligenceEngine.
"""
import pytest
from swarm.intelligence.sales_pricing_confidence_intelligence_engine import (
    PricingRisk,
    PricingPattern,
    PricingSeverity,
    PricingAction,
    PricingInput,
    PricingResult,
    SalesPricingConfidenceIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(
    rep_id="R001",
    region="West",
    evaluation_period_id="Q1-2026",
    avg_initial_discount_offered_pct=0.05,
    discount_offered_before_asked_pct=0.05,
    full_price_close_rate_pct=0.50,
    avg_final_discount_pct=0.05,
    discount_escalation_to_manager_pct=0.10,
    price_objection_concession_rate_pct=0.20,
    roi_articulated_in_proposal_pct=0.90,
    value_proof_attached_pct=0.80,
    competitor_price_match_rate_pct=0.05,
    discount_without_concession_pct=0.05,
    time_to_first_discount_days=14.0,
    multi_product_bundle_rate_pct=0.30,
    price_increase_accepted_rate_pct=0.40,
    deals_closed_above_list_pct=0.10,
    avg_discount_negotiation_rounds=1.0,
    late_stage_price_re_open_pct=0.05,
    total_deals_evaluated=10,
    avg_deal_size_usd=50000.0,
    avg_opportunity_value_usd=50000.0,
) -> PricingInput:
    """Return a low-risk PricingInput with selective overrides."""
    return PricingInput(
        rep_id=rep_id,
        region=region,
        evaluation_period_id=evaluation_period_id,
        avg_initial_discount_offered_pct=avg_initial_discount_offered_pct,
        discount_offered_before_asked_pct=discount_offered_before_asked_pct,
        full_price_close_rate_pct=full_price_close_rate_pct,
        avg_final_discount_pct=avg_final_discount_pct,
        discount_escalation_to_manager_pct=discount_escalation_to_manager_pct,
        price_objection_concession_rate_pct=price_objection_concession_rate_pct,
        roi_articulated_in_proposal_pct=roi_articulated_in_proposal_pct,
        value_proof_attached_pct=value_proof_attached_pct,
        competitor_price_match_rate_pct=competitor_price_match_rate_pct,
        discount_without_concession_pct=discount_without_concession_pct,
        time_to_first_discount_days=time_to_first_discount_days,
        multi_product_bundle_rate_pct=multi_product_bundle_rate_pct,
        price_increase_accepted_rate_pct=price_increase_accepted_rate_pct,
        deals_closed_above_list_pct=deals_closed_above_list_pct,
        avg_discount_negotiation_rounds=avg_discount_negotiation_rounds,
        late_stage_price_re_open_pct=late_stage_price_re_open_pct,
        total_deals_evaluated=total_deals_evaluated,
        avg_deal_size_usd=avg_deal_size_usd,
        avg_opportunity_value_usd=avg_opportunity_value_usd,
    )


def fresh_engine() -> SalesPricingConfidenceIntelligenceEngine:
    return SalesPricingConfidenceIntelligenceEngine()


# ---------------------------------------------------------------------------
# 1. Enum values and counts
# ---------------------------------------------------------------------------

class TestEnums:
    def test_pricing_risk_values(self):
        assert PricingRisk.low.value == "low"
        assert PricingRisk.moderate.value == "moderate"
        assert PricingRisk.high.value == "high"
        assert PricingRisk.critical.value == "critical"

    def test_pricing_risk_count(self):
        assert len(PricingRisk) == 4

    def test_pricing_pattern_values(self):
        assert PricingPattern.none.value == "none"
        assert PricingPattern.preemptive_discounting.value == "preemptive_discounting"
        assert PricingPattern.anchor_too_low.value == "anchor_too_low"
        assert PricingPattern.value_articulation_gap.value == "value_articulation_gap"
        assert PricingPattern.approval_escalation_dependency.value == "approval_escalation_dependency"
        assert PricingPattern.competitor_price_panic.value == "competitor_price_panic"

    def test_pricing_pattern_count(self):
        assert len(PricingPattern) == 6

    def test_pricing_severity_values(self):
        assert PricingSeverity.confident.value == "confident"
        assert PricingSeverity.cautious.value == "cautious"
        assert PricingSeverity.hesitant.value == "hesitant"
        assert PricingSeverity.capitulating.value == "capitulating"

    def test_pricing_severity_count(self):
        assert len(PricingSeverity) == 4

    def test_pricing_action_values(self):
        assert PricingAction.no_action.value == "no_action"
        assert PricingAction.value_selling_coaching.value == "value_selling_coaching"
        assert PricingAction.pricing_anchoring_coaching.value == "pricing_anchoring_coaching"
        assert PricingAction.negotiation_confidence_coaching.value == "negotiation_confidence_coaching"
        assert PricingAction.approval_process_coaching.value == "approval_process_coaching"
        assert PricingAction.competitive_pricing_training.value == "competitive_pricing_training"

    def test_pricing_action_count(self):
        assert len(PricingAction) == 6

    def test_enums_are_str_subclass(self):
        assert isinstance(PricingRisk.low, str)
        assert isinstance(PricingPattern.none, str)
        assert isinstance(PricingSeverity.confident, str)
        assert isinstance(PricingAction.no_action, str)


# ---------------------------------------------------------------------------
# 2. PricingInput – all 22 fields
# ---------------------------------------------------------------------------

class TestPricingInput:
    def test_all_22_fields_stored(self):
        inp = make_input(rep_id="X", region="East", evaluation_period_id="Q2")
        assert inp.rep_id == "X"
        assert inp.region == "East"
        assert inp.evaluation_period_id == "Q2"
        assert inp.avg_initial_discount_offered_pct == 0.05
        assert inp.discount_offered_before_asked_pct == 0.05
        assert inp.full_price_close_rate_pct == 0.50
        assert inp.avg_final_discount_pct == 0.05
        assert inp.discount_escalation_to_manager_pct == 0.10
        assert inp.price_objection_concession_rate_pct == 0.20
        assert inp.roi_articulated_in_proposal_pct == 0.90
        assert inp.value_proof_attached_pct == 0.80
        assert inp.competitor_price_match_rate_pct == 0.05
        assert inp.discount_without_concession_pct == 0.05
        assert inp.time_to_first_discount_days == 14.0
        assert inp.multi_product_bundle_rate_pct == 0.30
        assert inp.price_increase_accepted_rate_pct == 0.40
        assert inp.deals_closed_above_list_pct == 0.10
        assert inp.avg_discount_negotiation_rounds == 1.0
        assert inp.late_stage_price_re_open_pct == 0.05
        assert inp.total_deals_evaluated == 10
        assert inp.avg_deal_size_usd == 50000.0
        assert inp.avg_opportunity_value_usd == 50000.0

    def test_field_count(self):
        import dataclasses
        assert len(dataclasses.fields(PricingInput)) == 22


# ---------------------------------------------------------------------------
# 3. PricingResult – 15 fields and to_dict returns exactly 15 keys
# ---------------------------------------------------------------------------

class TestPricingResult:
    def _make_result(self):
        eng = fresh_engine()
        return eng.assess(make_input())

    def test_result_has_15_fields(self):
        import dataclasses
        assert len(dataclasses.fields(PricingResult)) == 15

    def test_to_dict_has_15_keys(self):
        r = self._make_result()
        d = r.to_dict()
        assert len(d) == 15

    def test_to_dict_exact_keys(self):
        r = self._make_result()
        d = r.to_dict()
        expected = {
            "rep_id", "region", "pricing_risk", "pricing_pattern",
            "pricing_severity", "recommended_action", "confidence_score",
            "value_score", "discipline_score", "competitive_score",
            "pricing_composite", "has_pricing_gap", "requires_pricing_coaching",
            "estimated_margin_erosion_usd", "pricing_signal",
        }
        assert set(d.keys()) == expected

    def test_to_dict_enum_values_are_strings(self):
        r = self._make_result()
        d = r.to_dict()
        assert isinstance(d["pricing_risk"], str)
        assert isinstance(d["pricing_pattern"], str)
        assert isinstance(d["pricing_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_rep_id_and_region(self):
        inp = make_input(rep_id="REP-42", region="Northeast")
        r = fresh_engine().assess(inp)
        d = r.to_dict()
        assert d["rep_id"] == "REP-42"
        assert d["region"] == "Northeast"

    def test_result_types(self):
        r = self._make_result()
        assert isinstance(r.pricing_risk, PricingRisk)
        assert isinstance(r.pricing_pattern, PricingPattern)
        assert isinstance(r.pricing_severity, PricingSeverity)
        assert isinstance(r.recommended_action, PricingAction)
        assert isinstance(r.confidence_score, float)
        assert isinstance(r.value_score, float)
        assert isinstance(r.discipline_score, float)
        assert isinstance(r.competitive_score, float)
        assert isinstance(r.pricing_composite, float)
        assert isinstance(r.has_pricing_gap, bool)
        assert isinstance(r.requires_pricing_coaching, bool)
        assert isinstance(r.estimated_margin_erosion_usd, float)
        assert isinstance(r.pricing_signal, str)


# ---------------------------------------------------------------------------
# 4. Sub-score: _confidence_score
# ---------------------------------------------------------------------------

class TestConfidenceScore:
    def _score(self, **kw) -> float:
        eng = fresh_engine()
        return eng._confidence_score(make_input(**kw))

    # discount_offered_before_asked_pct branches
    def test_discount_before_asked_ge_50(self):
        s = self._score(discount_offered_before_asked_pct=0.50, time_to_first_discount_days=20.0, full_price_close_rate_pct=0.50)
        assert s == 40.0

    def test_discount_before_asked_ge_30(self):
        s = self._score(discount_offered_before_asked_pct=0.30, time_to_first_discount_days=20.0, full_price_close_rate_pct=0.50)
        assert s == 22.0

    def test_discount_before_asked_ge_15(self):
        s = self._score(discount_offered_before_asked_pct=0.15, time_to_first_discount_days=20.0, full_price_close_rate_pct=0.50)
        assert s == 8.0

    def test_discount_before_asked_below_15(self):
        s = self._score(discount_offered_before_asked_pct=0.10, time_to_first_discount_days=20.0, full_price_close_rate_pct=0.50)
        assert s == 0.0

    # time_to_first_discount_days branches
    def test_time_to_discount_le_3(self):
        s = self._score(discount_offered_before_asked_pct=0.0, time_to_first_discount_days=3.0, full_price_close_rate_pct=0.50)
        assert s == 35.0

    def test_time_to_discount_le_7(self):
        s = self._score(discount_offered_before_asked_pct=0.0, time_to_first_discount_days=7.0, full_price_close_rate_pct=0.50)
        assert s == 18.0

    def test_time_to_discount_above_7(self):
        s = self._score(discount_offered_before_asked_pct=0.0, time_to_first_discount_days=8.0, full_price_close_rate_pct=0.50)
        assert s == 0.0

    # full_price_close_rate_pct branches
    def test_full_price_close_le_10(self):
        s = self._score(discount_offered_before_asked_pct=0.0, time_to_first_discount_days=20.0, full_price_close_rate_pct=0.10)
        assert s == 25.0

    def test_full_price_close_le_25(self):
        s = self._score(discount_offered_before_asked_pct=0.0, time_to_first_discount_days=20.0, full_price_close_rate_pct=0.25)
        assert s == 12.0

    def test_full_price_close_above_25(self):
        s = self._score(discount_offered_before_asked_pct=0.0, time_to_first_discount_days=20.0, full_price_close_rate_pct=0.26)
        assert s == 0.0

    # cap at 100
    def test_cap_at_100(self):
        s = self._score(discount_offered_before_asked_pct=0.99, time_to_first_discount_days=1.0, full_price_close_rate_pct=0.05)
        assert s == 100.0

    # additive: 40 + 35 + 25 = 100
    def test_all_three_branches_max(self):
        s = self._score(discount_offered_before_asked_pct=0.50, time_to_first_discount_days=1.0, full_price_close_rate_pct=0.05)
        assert s == 100.0

    # additive: 22 + 18 + 12 = 52
    def test_mid_tier_all_three(self):
        s = self._score(discount_offered_before_asked_pct=0.30, time_to_first_discount_days=5.0, full_price_close_rate_pct=0.20)
        assert s == 52.0

    def test_zero_score(self):
        s = self._score(discount_offered_before_asked_pct=0.0, time_to_first_discount_days=20.0, full_price_close_rate_pct=0.99)
        assert s == 0.0


# ---------------------------------------------------------------------------
# 5. Sub-score: _value_score
# ---------------------------------------------------------------------------

class TestValueScore:
    def _score(self, **kw) -> float:
        eng = fresh_engine()
        return eng._value_score(make_input(**kw))

    # roi_articulated_in_proposal_pct branches
    def test_roi_le_25(self):
        s = self._score(roi_articulated_in_proposal_pct=0.25, value_proof_attached_pct=0.90, price_objection_concession_rate_pct=0.10)
        assert s == 40.0

    def test_roi_le_50(self):
        s = self._score(roi_articulated_in_proposal_pct=0.50, value_proof_attached_pct=0.90, price_objection_concession_rate_pct=0.10)
        assert s == 22.0

    def test_roi_le_75(self):
        s = self._score(roi_articulated_in_proposal_pct=0.75, value_proof_attached_pct=0.90, price_objection_concession_rate_pct=0.10)
        assert s == 8.0

    def test_roi_above_75(self):
        s = self._score(roi_articulated_in_proposal_pct=0.76, value_proof_attached_pct=0.90, price_objection_concession_rate_pct=0.10)
        assert s == 0.0

    # value_proof_attached_pct branches
    def test_value_proof_le_20(self):
        s = self._score(roi_articulated_in_proposal_pct=0.99, value_proof_attached_pct=0.20, price_objection_concession_rate_pct=0.10)
        assert s == 35.0

    def test_value_proof_le_50(self):
        s = self._score(roi_articulated_in_proposal_pct=0.99, value_proof_attached_pct=0.50, price_objection_concession_rate_pct=0.10)
        assert s == 18.0

    def test_value_proof_above_50(self):
        s = self._score(roi_articulated_in_proposal_pct=0.99, value_proof_attached_pct=0.51, price_objection_concession_rate_pct=0.10)
        assert s == 0.0

    # price_objection_concession_rate_pct branches
    def test_concession_ge_70(self):
        s = self._score(roi_articulated_in_proposal_pct=0.99, value_proof_attached_pct=0.90, price_objection_concession_rate_pct=0.70)
        assert s == 25.0

    def test_concession_ge_45(self):
        s = self._score(roi_articulated_in_proposal_pct=0.99, value_proof_attached_pct=0.90, price_objection_concession_rate_pct=0.45)
        assert s == 12.0

    def test_concession_below_45(self):
        s = self._score(roi_articulated_in_proposal_pct=0.99, value_proof_attached_pct=0.90, price_objection_concession_rate_pct=0.44)
        assert s == 0.0

    # cap
    def test_cap_at_100(self):
        s = self._score(roi_articulated_in_proposal_pct=0.10, value_proof_attached_pct=0.10, price_objection_concession_rate_pct=0.99)
        assert s == 100.0

    # additive: 40 + 35 + 25 = 100
    def test_max_branches(self):
        s = self._score(roi_articulated_in_proposal_pct=0.10, value_proof_attached_pct=0.10, price_objection_concession_rate_pct=0.80)
        assert s == 100.0

    # additive: 22 + 18 + 12 = 52
    def test_mid_tier_all_three(self):
        s = self._score(roi_articulated_in_proposal_pct=0.40, value_proof_attached_pct=0.30, price_objection_concession_rate_pct=0.55)
        assert s == 52.0

    def test_zero_score(self):
        s = self._score(roi_articulated_in_proposal_pct=0.99, value_proof_attached_pct=0.90, price_objection_concession_rate_pct=0.10)
        assert s == 0.0


# ---------------------------------------------------------------------------
# 6. Sub-score: _discipline_score
# ---------------------------------------------------------------------------

class TestDisciplineScore:
    def _score(self, **kw) -> float:
        eng = fresh_engine()
        return eng._discipline_score(make_input(**kw))

    # avg_initial_discount_offered_pct branches
    def test_initial_discount_ge_25(self):
        s = self._score(avg_initial_discount_offered_pct=0.25, avg_discount_negotiation_rounds=1.0, late_stage_price_re_open_pct=0.0)
        assert s == 40.0

    def test_initial_discount_ge_15(self):
        s = self._score(avg_initial_discount_offered_pct=0.15, avg_discount_negotiation_rounds=1.0, late_stage_price_re_open_pct=0.0)
        assert s == 22.0

    def test_initial_discount_ge_08(self):
        s = self._score(avg_initial_discount_offered_pct=0.08, avg_discount_negotiation_rounds=1.0, late_stage_price_re_open_pct=0.0)
        assert s == 8.0

    def test_initial_discount_below_08(self):
        s = self._score(avg_initial_discount_offered_pct=0.07, avg_discount_negotiation_rounds=1.0, late_stage_price_re_open_pct=0.0)
        assert s == 0.0

    # avg_discount_negotiation_rounds branches
    def test_negotiation_rounds_ge_4(self):
        s = self._score(avg_initial_discount_offered_pct=0.0, avg_discount_negotiation_rounds=4.0, late_stage_price_re_open_pct=0.0)
        assert s == 35.0

    def test_negotiation_rounds_ge_25(self):
        s = self._score(avg_initial_discount_offered_pct=0.0, avg_discount_negotiation_rounds=2.5, late_stage_price_re_open_pct=0.0)
        assert s == 18.0

    def test_negotiation_rounds_below_25(self):
        s = self._score(avg_initial_discount_offered_pct=0.0, avg_discount_negotiation_rounds=2.4, late_stage_price_re_open_pct=0.0)
        assert s == 0.0

    # late_stage_price_re_open_pct branches
    def test_late_stage_reopen_ge_40(self):
        s = self._score(avg_initial_discount_offered_pct=0.0, avg_discount_negotiation_rounds=1.0, late_stage_price_re_open_pct=0.40)
        assert s == 25.0

    def test_late_stage_reopen_ge_20(self):
        s = self._score(avg_initial_discount_offered_pct=0.0, avg_discount_negotiation_rounds=1.0, late_stage_price_re_open_pct=0.20)
        assert s == 12.0

    def test_late_stage_reopen_below_20(self):
        s = self._score(avg_initial_discount_offered_pct=0.0, avg_discount_negotiation_rounds=1.0, late_stage_price_re_open_pct=0.19)
        assert s == 0.0

    # cap
    def test_cap_at_100(self):
        s = self._score(avg_initial_discount_offered_pct=0.99, avg_discount_negotiation_rounds=5.0, late_stage_price_re_open_pct=0.99)
        assert s == 100.0

    # additive: 40 + 35 + 25 = 100
    def test_max_branches(self):
        s = self._score(avg_initial_discount_offered_pct=0.25, avg_discount_negotiation_rounds=4.0, late_stage_price_re_open_pct=0.40)
        assert s == 100.0

    # additive: 22 + 18 + 12 = 52
    def test_mid_tier_all_three(self):
        s = self._score(avg_initial_discount_offered_pct=0.15, avg_discount_negotiation_rounds=3.0, late_stage_price_re_open_pct=0.25)
        assert s == 52.0

    def test_zero_score(self):
        s = self._score(avg_initial_discount_offered_pct=0.0, avg_discount_negotiation_rounds=1.0, late_stage_price_re_open_pct=0.0)
        assert s == 0.0


# ---------------------------------------------------------------------------
# 7. Sub-score: _competitive_score
# ---------------------------------------------------------------------------

class TestCompetitiveScore:
    def _score(self, **kw) -> float:
        eng = fresh_engine()
        return eng._competitive_score(make_input(**kw))

    # competitor_price_match_rate_pct branches
    def test_comp_match_ge_60(self):
        s = self._score(competitor_price_match_rate_pct=0.60, discount_without_concession_pct=0.0, discount_escalation_to_manager_pct=0.0)
        assert s == 45.0

    def test_comp_match_ge_40(self):
        s = self._score(competitor_price_match_rate_pct=0.40, discount_without_concession_pct=0.0, discount_escalation_to_manager_pct=0.0)
        assert s == 25.0

    def test_comp_match_ge_20(self):
        s = self._score(competitor_price_match_rate_pct=0.20, discount_without_concession_pct=0.0, discount_escalation_to_manager_pct=0.0)
        assert s == 10.0

    def test_comp_match_below_20(self):
        s = self._score(competitor_price_match_rate_pct=0.19, discount_without_concession_pct=0.0, discount_escalation_to_manager_pct=0.0)
        assert s == 0.0

    # discount_without_concession_pct branches
    def test_discount_no_concession_ge_60(self):
        s = self._score(competitor_price_match_rate_pct=0.0, discount_without_concession_pct=0.60, discount_escalation_to_manager_pct=0.0)
        assert s == 30.0

    def test_discount_no_concession_ge_35(self):
        s = self._score(competitor_price_match_rate_pct=0.0, discount_without_concession_pct=0.35, discount_escalation_to_manager_pct=0.0)
        assert s == 15.0

    def test_discount_no_concession_below_35(self):
        s = self._score(competitor_price_match_rate_pct=0.0, discount_without_concession_pct=0.34, discount_escalation_to_manager_pct=0.0)
        assert s == 0.0

    # discount_escalation_to_manager_pct branches
    def test_escalation_ge_50(self):
        s = self._score(competitor_price_match_rate_pct=0.0, discount_without_concession_pct=0.0, discount_escalation_to_manager_pct=0.50)
        assert s == 25.0

    def test_escalation_ge_25(self):
        s = self._score(competitor_price_match_rate_pct=0.0, discount_without_concession_pct=0.0, discount_escalation_to_manager_pct=0.25)
        assert s == 12.0

    def test_escalation_below_25(self):
        s = self._score(competitor_price_match_rate_pct=0.0, discount_without_concession_pct=0.0, discount_escalation_to_manager_pct=0.24)
        assert s == 0.0

    # cap
    def test_cap_at_100(self):
        s = self._score(competitor_price_match_rate_pct=0.99, discount_without_concession_pct=0.99, discount_escalation_to_manager_pct=0.99)
        assert s == 100.0

    # additive: 45 + 30 + 25 = 100
    def test_max_branches(self):
        s = self._score(competitor_price_match_rate_pct=0.60, discount_without_concession_pct=0.60, discount_escalation_to_manager_pct=0.50)
        assert s == 100.0

    # additive: 25 + 15 + 12 = 52
    def test_mid_tier_all_three(self):
        s = self._score(competitor_price_match_rate_pct=0.40, discount_without_concession_pct=0.35, discount_escalation_to_manager_pct=0.25)
        assert s == 52.0

    def test_zero_score(self):
        s = self._score(competitor_price_match_rate_pct=0.0, discount_without_concession_pct=0.0, discount_escalation_to_manager_pct=0.0)
        assert s == 0.0


# ---------------------------------------------------------------------------
# 8. Composite formula and weights
# ---------------------------------------------------------------------------

class TestCompositeFormula:
    def test_composite_weights(self):
        """
        Force each sub-score to a known value by carefully constructing inputs,
        then verify composite = conf*0.30 + val*0.25 + disc*0.25 + comp*0.20.
        """
        eng = fresh_engine()
        # All sub-scores set to exactly 0 except confidence (=40)
        inp = make_input(
            # confidence: 40 (discount_before_asked>=0.50) + 0 + 0
            discount_offered_before_asked_pct=0.50,
            time_to_first_discount_days=20.0,
            full_price_close_rate_pct=0.30,
            # value: 0
            roi_articulated_in_proposal_pct=0.99,
            value_proof_attached_pct=0.90,
            price_objection_concession_rate_pct=0.10,
            # discipline: 0
            avg_initial_discount_offered_pct=0.01,
            avg_discount_negotiation_rounds=1.0,
            late_stage_price_re_open_pct=0.0,
            # competitive: 0
            competitor_price_match_rate_pct=0.0,
            discount_without_concession_pct=0.0,
            discount_escalation_to_manager_pct=0.0,
        )
        result = eng.assess(inp)
        # confidence=40, others=0 → composite = 40*0.30 = 12.0
        assert result.confidence_score == 40.0
        assert result.value_score == 0.0
        assert result.discipline_score == 0.0
        assert result.competitive_score == 0.0
        assert result.pricing_composite == pytest.approx(12.0, abs=0.1)

    def test_composite_all_weights(self):
        """
        All four sub-scores produce specific known totals; verify composite.
        confidence=22, value=22, discipline=22, competitive=25 =>
        22*0.30 + 22*0.25 + 22*0.25 + 25*0.20 = 6.6+5.5+5.5+5.0 = 22.6
        """
        eng = fresh_engine()
        inp = make_input(
            # confidence: 22 (discount_before_asked>=0.30)
            discount_offered_before_asked_pct=0.30,
            time_to_first_discount_days=20.0,
            full_price_close_rate_pct=0.30,
            # value: 22 (roi<=0.50)
            roi_articulated_in_proposal_pct=0.50,
            value_proof_attached_pct=0.90,
            price_objection_concession_rate_pct=0.10,
            # discipline: 22 (avg_initial>=0.15)
            avg_initial_discount_offered_pct=0.15,
            avg_discount_negotiation_rounds=1.0,
            late_stage_price_re_open_pct=0.0,
            # competitive: 25 (comp_match>=0.40)
            competitor_price_match_rate_pct=0.40,
            discount_without_concession_pct=0.0,
            discount_escalation_to_manager_pct=0.0,
        )
        result = eng.assess(inp)
        assert result.confidence_score == 22.0
        assert result.value_score == 22.0
        assert result.discipline_score == 22.0
        assert result.competitive_score == 25.0
        expected = round(22 * 0.30 + 22 * 0.25 + 22 * 0.25 + 25 * 0.20, 1)
        assert result.pricing_composite == pytest.approx(expected, abs=0.05)

    def test_composite_capped_at_100(self):
        eng = fresh_engine()
        inp = make_input(
            discount_offered_before_asked_pct=0.99,
            time_to_first_discount_days=1.0,
            full_price_close_rate_pct=0.01,
            roi_articulated_in_proposal_pct=0.01,
            value_proof_attached_pct=0.01,
            price_objection_concession_rate_pct=0.99,
            avg_initial_discount_offered_pct=0.99,
            avg_discount_negotiation_rounds=5.0,
            late_stage_price_re_open_pct=0.99,
            competitor_price_match_rate_pct=0.99,
            discount_without_concession_pct=0.99,
            discount_escalation_to_manager_pct=0.99,
        )
        result = eng.assess(inp)
        assert result.pricing_composite <= 100.0


# ---------------------------------------------------------------------------
# 9. Pattern detection – priority, all 6 patterns, boundaries
# ---------------------------------------------------------------------------

class TestPatternDetection:
    def _detect(self, **kw) -> PricingPattern:
        return fresh_engine().assess(make_input(**kw)).pricing_pattern

    def test_none_pattern_healthy(self):
        p = self._detect()
        assert p == PricingPattern.none

    # approval_escalation_dependency (highest priority)
    def test_approval_escalation_dependency(self):
        p = self._detect(
            discount_escalation_to_manager_pct=0.45,
            full_price_close_rate_pct=0.15,
            # ensure other conditions don't override, but these come first
        )
        assert p == PricingPattern.approval_escalation_dependency

    def test_approval_escalation_boundary_escalation_just_below(self):
        """escalation=0.44 → does not trigger approval_escalation"""
        p = self._detect(
            discount_escalation_to_manager_pct=0.44,
            full_price_close_rate_pct=0.15,
            competitor_price_match_rate_pct=0.0,
            discount_offered_before_asked_pct=0.0,
            roi_articulated_in_proposal_pct=0.99,
            avg_initial_discount_offered_pct=0.0,
        )
        assert p != PricingPattern.approval_escalation_dependency

    def test_approval_escalation_boundary_full_price_just_above(self):
        """full_price_close_rate=0.16 → does not trigger approval_escalation"""
        p = self._detect(
            discount_escalation_to_manager_pct=0.45,
            full_price_close_rate_pct=0.16,
            competitor_price_match_rate_pct=0.0,
            discount_offered_before_asked_pct=0.0,
            roi_articulated_in_proposal_pct=0.99,
            avg_initial_discount_offered_pct=0.0,
        )
        assert p != PricingPattern.approval_escalation_dependency

    # competitor_price_panic (2nd priority)
    def test_competitor_price_panic(self):
        # competitive>=35 and comp_match>=0.50
        # competitive: comp_match>=0.60 → +45, no_concession>=0.0 → 0, esc=0 → 0 → competitive=45
        # comp_match=0.60>=0.50 satisfies condition
        # Need escalation <0.45 or full_price >0.15 to avoid approval_escalation
        p = self._detect(
            competitor_price_match_rate_pct=0.60,
            discount_without_concession_pct=0.0,
            discount_escalation_to_manager_pct=0.0,
            full_price_close_rate_pct=0.50,
        )
        assert p == PricingPattern.competitor_price_panic

    def test_competitor_price_panic_boundary_comp_below_35(self):
        """competitive<35 → no competitor_price_panic"""
        # competitor_price_match_rate=0.19 → 0 pts → competitive=0
        p = self._detect(
            competitor_price_match_rate_pct=0.19,
            discount_without_concession_pct=0.0,
            discount_escalation_to_manager_pct=0.0,
            full_price_close_rate_pct=0.50,
            discount_offered_before_asked_pct=0.0,
            roi_articulated_in_proposal_pct=0.99,
            avg_initial_discount_offered_pct=0.0,
        )
        assert p != PricingPattern.competitor_price_panic

    # preemptive_discounting (3rd priority)
    def test_preemptive_discounting(self):
        # confidence>=35, discount_before_asked>=0.40
        # time_to_first_discount<=3 → +35, discount_before_asked>=0.40 → +22 → confidence=57
        # Ensure competitive<35, approval conditions not met
        p = self._detect(
            time_to_first_discount_days=3.0,
            discount_offered_before_asked_pct=0.40,
            full_price_close_rate_pct=0.50,
            competitor_price_match_rate_pct=0.0,
            discount_without_concession_pct=0.0,
            discount_escalation_to_manager_pct=0.0,
        )
        assert p == PricingPattern.preemptive_discounting

    def test_preemptive_discounting_discount_before_asked_boundary(self):
        """discount_before_asked=0.39 → no preemptive"""
        p = self._detect(
            time_to_first_discount_days=3.0,
            discount_offered_before_asked_pct=0.39,
            full_price_close_rate_pct=0.50,
            competitor_price_match_rate_pct=0.0,
            discount_without_concession_pct=0.0,
            discount_escalation_to_manager_pct=0.0,
            roi_articulated_in_proposal_pct=0.99,
            avg_initial_discount_offered_pct=0.0,
        )
        assert p != PricingPattern.preemptive_discounting

    # value_articulation_gap (4th priority)
    def test_value_articulation_gap(self):
        # value>=35: roi<=0.25 → +40 → value=40
        # roi<=0.35 satisfies condition
        # ensure competitive<35 and confidence<35 and no approval pattern
        p = self._detect(
            roi_articulated_in_proposal_pct=0.25,
            value_proof_attached_pct=0.90,
            price_objection_concession_rate_pct=0.10,
            competitor_price_match_rate_pct=0.0,
            discount_without_concession_pct=0.0,
            discount_escalation_to_manager_pct=0.0,
            discount_offered_before_asked_pct=0.0,
            time_to_first_discount_days=20.0,
            full_price_close_rate_pct=0.50,
            avg_initial_discount_offered_pct=0.0,
        )
        assert p == PricingPattern.value_articulation_gap

    def test_value_articulation_gap_roi_above_35(self):
        """roi=0.36 → no value_articulation_gap"""
        p = self._detect(
            roi_articulated_in_proposal_pct=0.36,
            value_proof_attached_pct=0.90,
            price_objection_concession_rate_pct=0.10,
            competitor_price_match_rate_pct=0.0,
            discount_without_concession_pct=0.0,
            discount_escalation_to_manager_pct=0.0,
            discount_offered_before_asked_pct=0.0,
            time_to_first_discount_days=20.0,
            full_price_close_rate_pct=0.50,
            avg_initial_discount_offered_pct=0.0,
        )
        assert p != PricingPattern.value_articulation_gap

    # anchor_too_low (5th priority)
    def test_anchor_too_low(self):
        # avg_initial_discount>=0.20 and discipline>=25
        # discipline: avg_initial>=0.20 (→ 22 pts since 0.20 < 0.25), rounds>=2.5 → +18 → discipline=40 >= 25
        # But also: avg_initial_discount_offered_pct=0.20 triggers discipline score
        # Let's use avg_initial=0.20, negotiation_rounds=3.0 → discipline=22+18=40
        p = self._detect(
            avg_initial_discount_offered_pct=0.20,
            avg_discount_negotiation_rounds=3.0,
            late_stage_price_re_open_pct=0.0,
            roi_articulated_in_proposal_pct=0.99,
            value_proof_attached_pct=0.90,
            price_objection_concession_rate_pct=0.10,
            competitor_price_match_rate_pct=0.0,
            discount_without_concession_pct=0.0,
            discount_escalation_to_manager_pct=0.0,
            discount_offered_before_asked_pct=0.0,
            time_to_first_discount_days=20.0,
            full_price_close_rate_pct=0.50,
        )
        assert p == PricingPattern.anchor_too_low

    def test_anchor_too_low_initial_discount_below_20(self):
        """avg_initial=0.19 → no anchor_too_low"""
        p = self._detect(
            avg_initial_discount_offered_pct=0.19,
            avg_discount_negotiation_rounds=3.0,
            late_stage_price_re_open_pct=0.0,
            roi_articulated_in_proposal_pct=0.99,
            value_proof_attached_pct=0.90,
            price_objection_concession_rate_pct=0.10,
            competitor_price_match_rate_pct=0.0,
            discount_without_concession_pct=0.0,
            discount_escalation_to_manager_pct=0.0,
            discount_offered_before_asked_pct=0.0,
            time_to_first_discount_days=20.0,
            full_price_close_rate_pct=0.50,
        )
        assert p != PricingPattern.anchor_too_low

    # Priority: approval beats competitor_price_panic
    def test_approval_escalation_beats_competitor_panic(self):
        p = self._detect(
            discount_escalation_to_manager_pct=0.45,
            full_price_close_rate_pct=0.15,
            competitor_price_match_rate_pct=0.60,
            discount_without_concession_pct=0.60,
        )
        assert p == PricingPattern.approval_escalation_dependency

    # Priority: competitor_price_panic beats preemptive_discounting
    def test_competitor_panic_beats_preemptive(self):
        # competitive>=35: comp_match=0.60 → +45 → competitive=45 >= 35
        # comp_match=0.60 >= 0.50 satisfies competitor_panic condition
        # confidence>=35: time<=3 → +35 → confidence=35, discount_before_asked>=0.40
        # approval condition not met (escalation=0.0)
        p = self._detect(
            discount_escalation_to_manager_pct=0.0,
            full_price_close_rate_pct=0.50,
            competitor_price_match_rate_pct=0.60,
            discount_without_concession_pct=0.0,
            time_to_first_discount_days=3.0,
            discount_offered_before_asked_pct=0.40,
        )
        assert p == PricingPattern.competitor_price_panic


# ---------------------------------------------------------------------------
# 10. Risk thresholds
# ---------------------------------------------------------------------------

class TestRiskLevel:
    def _risk(self, composite: float) -> PricingRisk:
        eng = fresh_engine()
        return eng._risk_level(composite)

    def test_low_below_20(self):
        assert self._risk(0.0) == PricingRisk.low
        assert self._risk(19.9) == PricingRisk.low

    def test_moderate_at_20(self):
        assert self._risk(20.0) == PricingRisk.moderate

    def test_moderate_below_40(self):
        assert self._risk(39.9) == PricingRisk.moderate

    def test_high_at_40(self):
        assert self._risk(40.0) == PricingRisk.high

    def test_high_below_60(self):
        assert self._risk(59.9) == PricingRisk.high

    def test_critical_at_60(self):
        assert self._risk(60.0) == PricingRisk.critical

    def test_critical_above_60(self):
        assert self._risk(100.0) == PricingRisk.critical


# ---------------------------------------------------------------------------
# 11. Severity thresholds
# ---------------------------------------------------------------------------

class TestSeverity:
    def _sev(self, composite: float) -> PricingSeverity:
        eng = fresh_engine()
        return eng._severity(composite)

    def test_confident_below_20(self):
        assert self._sev(0.0) == PricingSeverity.confident
        assert self._sev(19.9) == PricingSeverity.confident

    def test_cautious_at_20(self):
        assert self._sev(20.0) == PricingSeverity.cautious

    def test_cautious_below_40(self):
        assert self._sev(39.9) == PricingSeverity.cautious

    def test_hesitant_at_40(self):
        assert self._sev(40.0) == PricingSeverity.hesitant

    def test_hesitant_below_60(self):
        assert self._sev(59.9) == PricingSeverity.hesitant

    def test_capitulating_at_60(self):
        assert self._sev(60.0) == PricingSeverity.capitulating

    def test_capitulating_above_60(self):
        assert self._sev(100.0) == PricingSeverity.capitulating


# ---------------------------------------------------------------------------
# 12. Action mappings
# ---------------------------------------------------------------------------

class TestActionMapping:
    def _action(self, risk: PricingRisk, pattern: PricingPattern) -> PricingAction:
        return fresh_engine()._action(risk, pattern)

    def test_critical_competitor_price_panic(self):
        assert self._action(PricingRisk.critical, PricingPattern.competitor_price_panic) == PricingAction.competitive_pricing_training

    def test_critical_approval_escalation(self):
        assert self._action(PricingRisk.critical, PricingPattern.approval_escalation_dependency) == PricingAction.approval_process_coaching

    def test_critical_other_patterns(self):
        assert self._action(PricingRisk.critical, PricingPattern.none) == PricingAction.negotiation_confidence_coaching
        assert self._action(PricingRisk.critical, PricingPattern.preemptive_discounting) == PricingAction.negotiation_confidence_coaching
        assert self._action(PricingRisk.critical, PricingPattern.value_articulation_gap) == PricingAction.negotiation_confidence_coaching
        assert self._action(PricingRisk.critical, PricingPattern.anchor_too_low) == PricingAction.negotiation_confidence_coaching

    def test_high_value_articulation_gap(self):
        assert self._action(PricingRisk.high, PricingPattern.value_articulation_gap) == PricingAction.value_selling_coaching

    def test_high_anchor_too_low(self):
        assert self._action(PricingRisk.high, PricingPattern.anchor_too_low) == PricingAction.pricing_anchoring_coaching

    def test_high_other_patterns(self):
        assert self._action(PricingRisk.high, PricingPattern.none) == PricingAction.negotiation_confidence_coaching
        assert self._action(PricingRisk.high, PricingPattern.preemptive_discounting) == PricingAction.negotiation_confidence_coaching
        assert self._action(PricingRisk.high, PricingPattern.competitor_price_panic) == PricingAction.negotiation_confidence_coaching

    def test_moderate_any_pattern(self):
        for p in PricingPattern:
            assert self._action(PricingRisk.moderate, p) == PricingAction.value_selling_coaching

    def test_low_any_pattern(self):
        for p in PricingPattern:
            assert self._action(PricingRisk.low, p) == PricingAction.no_action


# ---------------------------------------------------------------------------
# 13. has_pricing_gap flag
# ---------------------------------------------------------------------------

class TestHasPricingGap:
    def _gap(self, composite, **kw) -> bool:
        # Use assess to get the flag
        inp = make_input(**kw)
        eng = fresh_engine()
        # Directly call the method
        return eng._has_pricing_gap(composite, inp)

    def test_gap_from_composite_ge_40(self):
        assert self._gap(40.0) is True

    def test_no_gap_composite_below_40(self):
        assert self._gap(
            39.9,
            avg_final_discount_pct=0.05,
            full_price_close_rate_pct=0.50,
        ) is False

    def test_gap_from_avg_final_discount_ge_20(self):
        assert self._gap(0.0, avg_final_discount_pct=0.20) is True

    def test_no_gap_avg_final_discount_below_20(self):
        assert self._gap(0.0, avg_final_discount_pct=0.19, full_price_close_rate_pct=0.50) is False

    def test_gap_from_full_price_close_le_15(self):
        assert self._gap(0.0, avg_final_discount_pct=0.05, full_price_close_rate_pct=0.15) is True

    def test_no_gap_full_price_close_above_15(self):
        assert self._gap(0.0, avg_final_discount_pct=0.05, full_price_close_rate_pct=0.16) is False

    def test_gap_all_conditions_false(self):
        assert self._gap(10.0, avg_final_discount_pct=0.10, full_price_close_rate_pct=0.50) is False


# ---------------------------------------------------------------------------
# 14. requires_pricing_coaching flag
# ---------------------------------------------------------------------------

class TestRequiresPricingCoaching:
    def _coaching(self, composite, **kw) -> bool:
        inp = make_input(**kw)
        return fresh_engine()._requires_pricing_coaching(composite, inp)

    def test_coaching_from_composite_ge_30(self):
        assert self._coaching(30.0) is True

    def test_no_coaching_composite_below_30(self):
        assert self._coaching(
            29.9,
            discount_offered_before_asked_pct=0.10,
            roi_articulated_in_proposal_pct=0.90,
        ) is False

    def test_coaching_from_discount_before_asked_ge_25(self):
        assert self._coaching(0.0, discount_offered_before_asked_pct=0.25, roi_articulated_in_proposal_pct=0.90) is True

    def test_no_coaching_discount_before_asked_below_25(self):
        assert self._coaching(0.0, discount_offered_before_asked_pct=0.24, roi_articulated_in_proposal_pct=0.90) is False

    def test_coaching_from_roi_le_40(self):
        assert self._coaching(0.0, discount_offered_before_asked_pct=0.10, roi_articulated_in_proposal_pct=0.40) is True

    def test_no_coaching_roi_above_40(self):
        assert self._coaching(0.0, discount_offered_before_asked_pct=0.10, roi_articulated_in_proposal_pct=0.41) is False

    def test_no_coaching_all_false(self):
        assert self._coaching(
            10.0,
            discount_offered_before_asked_pct=0.10,
            roi_articulated_in_proposal_pct=0.90,
        ) is False


# ---------------------------------------------------------------------------
# 15. Estimated margin erosion
# ---------------------------------------------------------------------------

class TestMarginErosion:
    def test_formula(self):
        inp = make_input(
            total_deals_evaluated=10,
            avg_opportunity_value_usd=100000.0,
            avg_final_discount_pct=0.15,
        )
        composite = 50.0
        result = fresh_engine()._estimated_margin_erosion(inp, composite)
        expected = round(10 * 100000.0 * 0.15 * (50.0 / 100.0), 2)
        assert result == expected

    def test_zero_composite_yields_zero(self):
        inp = make_input(total_deals_evaluated=100, avg_opportunity_value_usd=50000.0, avg_final_discount_pct=0.20)
        assert fresh_engine()._estimated_margin_erosion(inp, 0.0) == 0.0

    def test_rounding_to_2_decimal_places(self):
        inp = make_input(total_deals_evaluated=3, avg_opportunity_value_usd=33333.33, avg_final_discount_pct=0.10)
        result = fresh_engine()._estimated_margin_erosion(inp, 50.0)
        # check it's rounded to 2 decimals
        assert result == round(result, 2)

    def test_erosion_end_to_end(self):
        inp = make_input(
            total_deals_evaluated=20,
            avg_opportunity_value_usd=75000.0,
            avg_final_discount_pct=0.10,
        )
        eng = fresh_engine()
        result = eng.assess(inp)
        comp = result.pricing_composite
        expected = round(20 * 75000.0 * 0.10 * (comp / 100.0), 2)
        assert result.estimated_margin_erosion_usd == expected


# ---------------------------------------------------------------------------
# 16. Pricing signal string
# ---------------------------------------------------------------------------

class TestSignalString:
    def test_healthy_signal(self):
        """composite<20 and pattern=none → healthy message"""
        r = fresh_engine().assess(make_input())
        if r.pricing_pattern == PricingPattern.none and r.pricing_composite < 20:
            assert r.pricing_signal == (
                "Pricing confidence healthy — discount discipline, "
                "value articulation, and competitive positioning within benchmarks"
            )

    def test_signal_contains_avg_final_discount(self):
        inp = make_input(
            avg_final_discount_pct=0.12,
            time_to_first_discount_days=3.0,
            discount_offered_before_asked_pct=0.40,
            full_price_close_rate_pct=0.50,
        )
        r = fresh_engine().assess(inp)
        if r.pricing_composite >= 20 or r.pricing_pattern != PricingPattern.none:
            assert "12% avg final discount" in r.pricing_signal

    def test_signal_contains_preemptive_discounting_pct(self):
        inp = make_input(
            discount_offered_before_asked_pct=0.40,
            time_to_first_discount_days=3.0,
            full_price_close_rate_pct=0.50,
        )
        r = fresh_engine().assess(inp)
        if r.pricing_composite >= 20 or r.pricing_pattern != PricingPattern.none:
            assert "40% preemptive discounting" in r.pricing_signal

    def test_signal_contains_full_price_closes(self):
        inp = make_input(
            full_price_close_rate_pct=0.30,
            time_to_first_discount_days=3.0,
            discount_offered_before_asked_pct=0.40,
        )
        r = fresh_engine().assess(inp)
        if r.pricing_composite >= 20 or r.pricing_pattern != PricingPattern.none:
            assert "30% full-price closes" in r.pricing_signal

    def test_signal_contains_composite(self):
        inp = make_input(
            discount_offered_before_asked_pct=0.50,
            time_to_first_discount_days=3.0,
            full_price_close_rate_pct=0.10,
        )
        r = fresh_engine().assess(inp)
        if r.pricing_composite >= 20 or r.pricing_pattern != PricingPattern.none:
            assert f"composite {r.pricing_composite:.0f}" in r.pricing_signal

    def test_signal_pattern_label_formatted(self):
        """Pattern name should appear capitalized with underscores replaced."""
        inp = make_input(
            discount_offered_before_asked_pct=0.50,
            time_to_first_discount_days=3.0,
            full_price_close_rate_pct=0.50,
            competitor_price_match_rate_pct=0.0,
            discount_escalation_to_manager_pct=0.0,
        )
        r = fresh_engine().assess(inp)
        if r.pricing_pattern == PricingPattern.preemptive_discounting:
            assert "Preemptive discounting" in r.pricing_signal

    def test_signal_none_pattern_with_high_composite(self):
        """If pattern=none but composite>=20, should show 'Pricing risk' label."""
        # composite=12 for pure confidence=40 → composite=12 → healthy
        # Let's engineer composite between 20-39 with pattern=none
        # confidence=40 (discount_before=0.50), value=22(roi=0.50), disc=0, comp=0
        # composite = 40*0.3 + 22*0.25 = 12+5.5 = 17.5 → below 20
        # Need to get composite >= 20 with pattern=none
        # confidence=40(disc_before=0.50) + 35(time<=3) = 75, value=0, disc=0, comp=0
        # composite = 75*0.30 = 22.5 → moderate but pattern might trigger preemptive if disc_before>=0.40
        # So discount_before=0.50 and time<=3 → confidence=75, disc_before >= 0.40 → preemptive
        # Use just time<=3 → +35 confidence, disc_before=0.0 → confidence=35
        # composite = 35*0.30 = 10.5 → still low
        # Need value score: roi=0.25 → +40, value_proof=0.20 → +35 → value=75
        # composite = 35*0.30 + 75*0.25 = 10.5 + 18.75 = 29.25 → moderate
        # pattern: competitive<35, confidence>=35 BUT disc_before<0.40 → skip preemptive
        # value>=35 AND roi=0.25<=0.35 → value_articulation_gap!
        # Need roi > 0.35 to avoid value_articulation_gap
        # roi=0.36 → value: 22+35=57, composite=35*0.30+57*0.25=10.5+14.25=24.75 → moderate
        # pattern: value=57>=35 but roi=0.36 > 0.35 → no value_gap
        # avg_initial < 0.20 → no anchor_too_low → pattern=none
        inp = make_input(
            time_to_first_discount_days=3.0,
            discount_offered_before_asked_pct=0.0,
            full_price_close_rate_pct=0.30,
            roi_articulated_in_proposal_pct=0.36,
            value_proof_attached_pct=0.20,
            price_objection_concession_rate_pct=0.10,
            competitor_price_match_rate_pct=0.0,
            discount_without_concession_pct=0.0,
            discount_escalation_to_manager_pct=0.0,
            avg_initial_discount_offered_pct=0.0,
            avg_discount_negotiation_rounds=1.0,
            late_stage_price_re_open_pct=0.0,
        )
        r = fresh_engine().assess(inp)
        if r.pricing_pattern == PricingPattern.none and r.pricing_composite >= 20:
            assert "Pricing risk" in r.pricing_signal


# ---------------------------------------------------------------------------
# 17. assess() end-to-end
# ---------------------------------------------------------------------------

class TestAssessEndToEnd:
    def test_low_risk_all_fields(self):
        """Healthy rep → low risk, no pattern, confident, no action, no gap."""
        r = fresh_engine().assess(make_input())
        assert r.pricing_risk == PricingRisk.low
        assert r.pricing_severity == PricingSeverity.confident
        assert r.recommended_action == PricingAction.no_action
        assert r.pricing_pattern == PricingPattern.none
        assert r.has_pricing_gap is False

    def test_result_rep_id_and_region_propagated(self):
        inp = make_input(rep_id="TESTID", region="TESTREGION")
        r = fresh_engine().assess(inp)
        assert r.rep_id == "TESTID"
        assert r.region == "TESTREGION"

    def test_scores_in_0_100_range(self):
        r = fresh_engine().assess(make_input())
        assert 0.0 <= r.confidence_score <= 100.0
        assert 0.0 <= r.value_score <= 100.0
        assert 0.0 <= r.discipline_score <= 100.0
        assert 0.0 <= r.competitive_score <= 100.0
        assert 0.0 <= r.pricing_composite <= 100.0

    def test_critical_rep(self):
        inp = make_input(
            discount_offered_before_asked_pct=0.99,
            time_to_first_discount_days=1.0,
            full_price_close_rate_pct=0.05,
            roi_articulated_in_proposal_pct=0.05,
            value_proof_attached_pct=0.05,
            price_objection_concession_rate_pct=0.99,
            avg_initial_discount_offered_pct=0.99,
            avg_discount_negotiation_rounds=5.0,
            late_stage_price_re_open_pct=0.99,
            competitor_price_match_rate_pct=0.99,
            discount_without_concession_pct=0.99,
            discount_escalation_to_manager_pct=0.99,
            avg_final_discount_pct=0.40,
            total_deals_evaluated=50,
            avg_opportunity_value_usd=100000.0,
        )
        r = fresh_engine().assess(inp)
        assert r.pricing_risk == PricingRisk.critical
        assert r.pricing_severity == PricingSeverity.capitulating
        assert r.has_pricing_gap is True
        assert r.requires_pricing_coaching is True
        assert r.estimated_margin_erosion_usd > 0


# ---------------------------------------------------------------------------
# 18. assess_batch()
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_returns_list_of_results(self):
        inputs = [make_input(rep_id=f"R{i}") for i in range(3)]
        results = fresh_engine().assess_batch(inputs)
        assert len(results) == 3
        assert all(isinstance(r, PricingResult) for r in results)

    def test_rep_ids_preserved_in_order(self):
        inputs = [make_input(rep_id=f"REP{i}") for i in range(5)]
        results = fresh_engine().assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"REP{i}"

    def test_empty_batch(self):
        results = fresh_engine().assess_batch([])
        assert results == []

    def test_batch_accumulates_in_summary(self):
        eng = fresh_engine()
        inputs = [make_input(rep_id=f"X{i}") for i in range(4)]
        eng.assess_batch(inputs)
        s = eng.summary()
        assert s["total"] == 4


# ---------------------------------------------------------------------------
# 19. summary() – empty
# ---------------------------------------------------------------------------

class TestSummaryEmpty:
    def test_empty_engine_summary_has_13_keys(self):
        s = fresh_engine().summary()
        assert len(s) == 13

    def test_empty_summary_keys(self):
        s = fresh_engine().summary()
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_pricing_composite", "pricing_gap_count",
            "coaching_count", "avg_confidence_score", "avg_value_score",
            "avg_discipline_score", "avg_competitive_score",
            "total_estimated_margin_erosion_usd",
        }
        assert set(s.keys()) == expected

    def test_empty_summary_total_is_zero(self):
        assert fresh_engine().summary()["total"] == 0

    def test_empty_summary_counts_are_empty_dicts(self):
        s = fresh_engine().summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}

    def test_empty_summary_numeric_zeros(self):
        s = fresh_engine().summary()
        assert s["avg_pricing_composite"] == 0.0
        assert s["pricing_gap_count"] == 0
        assert s["coaching_count"] == 0
        assert s["avg_confidence_score"] == 0.0
        assert s["avg_value_score"] == 0.0
        assert s["avg_discipline_score"] == 0.0
        assert s["avg_competitive_score"] == 0.0
        assert s["total_estimated_margin_erosion_usd"] == 0.0


# ---------------------------------------------------------------------------
# 20. summary() – populated
# ---------------------------------------------------------------------------

class TestSummaryPopulated:
    def _build_engine(self):
        eng = fresh_engine()
        # Healthy rep
        eng.assess(make_input(rep_id="H1"))
        # High-risk rep with gap and coaching needed
        eng.assess(make_input(
            rep_id="H2",
            discount_offered_before_asked_pct=0.50,
            time_to_first_discount_days=3.0,
            full_price_close_rate_pct=0.10,
            roi_articulated_in_proposal_pct=0.25,
            value_proof_attached_pct=0.20,
            price_objection_concession_rate_pct=0.70,
            avg_initial_discount_offered_pct=0.25,
            avg_discount_negotiation_rounds=4.0,
            late_stage_price_re_open_pct=0.40,
            avg_final_discount_pct=0.30,
            total_deals_evaluated=10,
            avg_opportunity_value_usd=100000.0,
        ))
        return eng

    def test_summary_has_13_keys(self):
        s = self._build_engine().summary()
        assert len(s) == 13

    def test_summary_exact_keys(self):
        s = self._build_engine().summary()
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_pricing_composite", "pricing_gap_count",
            "coaching_count", "avg_confidence_score", "avg_value_score",
            "avg_discipline_score", "avg_competitive_score",
            "total_estimated_margin_erosion_usd",
        }
        assert set(s.keys()) == expected

    def test_summary_total_count(self):
        s = self._build_engine().summary()
        assert s["total"] == 2

    def test_summary_risk_counts_dict(self):
        s = self._build_engine().summary()
        assert isinstance(s["risk_counts"], dict)
        assert sum(s["risk_counts"].values()) == 2

    def test_summary_pattern_counts_dict(self):
        s = self._build_engine().summary()
        assert isinstance(s["pattern_counts"], dict)
        assert sum(s["pattern_counts"].values()) == 2

    def test_summary_severity_counts_dict(self):
        s = self._build_engine().summary()
        assert isinstance(s["severity_counts"], dict)
        assert sum(s["severity_counts"].values()) == 2

    def test_summary_action_counts_dict(self):
        s = self._build_engine().summary()
        assert isinstance(s["action_counts"], dict)
        assert sum(s["action_counts"].values()) == 2

    def test_summary_avg_pricing_composite_float(self):
        s = self._build_engine().summary()
        assert isinstance(s["avg_pricing_composite"], float)

    def test_summary_pricing_gap_count(self):
        s = self._build_engine().summary()
        # H2 has very high scores → gap should be True
        assert s["pricing_gap_count"] >= 1

    def test_summary_coaching_count(self):
        s = self._build_engine().summary()
        assert s["coaching_count"] >= 1

    def test_summary_avg_scores_are_floats(self):
        s = self._build_engine().summary()
        assert isinstance(s["avg_confidence_score"], float)
        assert isinstance(s["avg_value_score"], float)
        assert isinstance(s["avg_discipline_score"], float)
        assert isinstance(s["avg_competitive_score"], float)

    def test_summary_total_erosion_is_float(self):
        s = self._build_engine().summary()
        assert isinstance(s["total_estimated_margin_erosion_usd"], float)

    def test_summary_total_erosion_is_sum(self):
        eng = fresh_engine()
        r1 = eng.assess(make_input(rep_id="A", total_deals_evaluated=10, avg_opportunity_value_usd=50000.0, avg_final_discount_pct=0.10))
        r2 = eng.assess(make_input(rep_id="B", total_deals_evaluated=5, avg_opportunity_value_usd=80000.0, avg_final_discount_pct=0.15))
        s = eng.summary()
        expected = round(r1.estimated_margin_erosion_usd + r2.estimated_margin_erosion_usd, 2)
        assert s["total_estimated_margin_erosion_usd"] == pytest.approx(expected, abs=0.01)

    def test_summary_avg_composite_is_mean(self):
        eng = fresh_engine()
        r1 = eng.assess(make_input(rep_id="A"))
        r2 = eng.assess(make_input(rep_id="B"))
        s = eng.summary()
        expected = round((r1.pricing_composite + r2.pricing_composite) / 2, 1)
        assert s["avg_pricing_composite"] == pytest.approx(expected, abs=0.05)


# ---------------------------------------------------------------------------
# 21. Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_zero_composite_end_to_end(self):
        """All sub-scores at minimum → composite 0 → low risk, confident, no action."""
        inp = make_input(
            discount_offered_before_asked_pct=0.0,
            time_to_first_discount_days=100.0,
            full_price_close_rate_pct=1.0,
            roi_articulated_in_proposal_pct=1.0,
            value_proof_attached_pct=1.0,
            price_objection_concession_rate_pct=0.0,
            avg_initial_discount_offered_pct=0.0,
            avg_discount_negotiation_rounds=0.0,
            late_stage_price_re_open_pct=0.0,
            competitor_price_match_rate_pct=0.0,
            discount_without_concession_pct=0.0,
            discount_escalation_to_manager_pct=0.0,
            avg_final_discount_pct=0.10,
        )
        r = fresh_engine().assess(inp)
        assert r.pricing_composite == 0.0
        assert r.pricing_risk == PricingRisk.low
        assert r.pricing_severity == PricingSeverity.confident
        assert r.recommended_action == PricingAction.no_action

    def test_exact_boundary_composite_20(self):
        """Exact boundary: composite=20 → moderate, cautious."""
        # confidence: discount_before=0.30 → +22, time=20 → 0, full_price=0.30 → 0 → conf=22
        # value: roi=0.99 → 0, proof=0.90 → 0, concession=0.10 → 0 → value=0
        # discipline: initial=0.0 → 0, rounds=1.0 → 0, late=0.0 → 0 → disc=0
        # competitive: match=0.0, no_concession=0.0, esc=0.0 → comp=0
        # composite = 22*0.30 = 6.6 → not 20
        # Need to engineer composite=20 exactly
        # Simplest: confidence=0, value=0, discipline=0, competitive=100
        # composite = 100*0.20 = 20
        # competitive=100: match>=0.60(+45) + no_concession>=0.60(+30) + esc>=0.50(+25) = 100
        inp = make_input(
            discount_offered_before_asked_pct=0.0,
            time_to_first_discount_days=100.0,
            full_price_close_rate_pct=0.50,
            roi_articulated_in_proposal_pct=0.99,
            value_proof_attached_pct=0.90,
            price_objection_concession_rate_pct=0.10,
            avg_initial_discount_offered_pct=0.0,
            avg_discount_negotiation_rounds=1.0,
            late_stage_price_re_open_pct=0.0,
            competitor_price_match_rate_pct=0.60,
            discount_without_concession_pct=0.60,
            discount_escalation_to_manager_pct=0.50,
        )
        r = fresh_engine().assess(inp)
        assert r.pricing_composite == pytest.approx(20.0, abs=0.1)
        assert r.pricing_risk == PricingRisk.moderate
        assert r.pricing_severity == PricingSeverity.cautious

    def test_to_dict_values_are_correct_types(self):
        r = fresh_engine().assess(make_input())
        d = r.to_dict()
        assert isinstance(d["confidence_score"], float)
        assert isinstance(d["value_score"], float)
        assert isinstance(d["discipline_score"], float)
        assert isinstance(d["competitive_score"], float)
        assert isinstance(d["pricing_composite"], float)
        assert isinstance(d["has_pricing_gap"], bool)
        assert isinstance(d["requires_pricing_coaching"], bool)
        assert isinstance(d["estimated_margin_erosion_usd"], float)
        assert isinstance(d["pricing_signal"], str)

    def test_multiple_assess_calls_accumulate(self):
        eng = fresh_engine()
        for i in range(5):
            eng.assess(make_input(rep_id=f"R{i}"))
        assert eng.summary()["total"] == 5

    def test_score_isolation_confidence_only(self):
        """Changing only confidence inputs does not affect value/discipline/competitive."""
        eng = fresh_engine()
        r = eng.assess(make_input(
            discount_offered_before_asked_pct=0.50,
            time_to_first_discount_days=3.0,
            full_price_close_rate_pct=0.10,
            roi_articulated_in_proposal_pct=0.99,
            value_proof_attached_pct=0.90,
            price_objection_concession_rate_pct=0.10,
            avg_initial_discount_offered_pct=0.0,
            avg_discount_negotiation_rounds=1.0,
            late_stage_price_re_open_pct=0.0,
            competitor_price_match_rate_pct=0.0,
            discount_without_concession_pct=0.0,
            discount_escalation_to_manager_pct=0.0,
        ))
        assert r.confidence_score == 100.0
        assert r.value_score == 0.0
        assert r.discipline_score == 0.0
        assert r.competitive_score == 0.0

    def test_single_rep_summary_counts(self):
        eng = fresh_engine()
        r = eng.assess(make_input(rep_id="SOLO"))
        s = eng.summary()
        assert s["total"] == 1
        assert s["risk_counts"][r.pricing_risk.value] == 1
        assert s["pattern_counts"][r.pricing_pattern.value] == 1
        assert s["severity_counts"][r.pricing_severity.value] == 1
        assert s["action_counts"][r.recommended_action.value] == 1
        assert s["avg_pricing_composite"] == r.pricing_composite
        assert s["avg_confidence_score"] == r.confidence_score
        assert s["avg_value_score"] == r.value_score
        assert s["avg_discipline_score"] == r.discipline_score
        assert s["avg_competitive_score"] == r.competitive_score

    def test_result_is_pricing_result_instance(self):
        r = fresh_engine().assess(make_input())
        assert isinstance(r, PricingResult)

    def test_to_dict_pricing_risk_is_string_not_enum(self):
        r = fresh_engine().assess(make_input())
        d = r.to_dict()
        assert type(d["pricing_risk"]) is str
        assert type(d["pricing_pattern"]) is str
        assert type(d["pricing_severity"]) is str
        assert type(d["recommended_action"]) is str

    def test_assess_batch_single_item(self):
        eng = fresh_engine()
        results = eng.assess_batch([make_input(rep_id="SINGLE")])
        assert len(results) == 1
        assert results[0].rep_id == "SINGLE"

    def test_composite_rounding_to_1_decimal(self):
        """Composite should be rounded to 1 decimal place."""
        r = fresh_engine().assess(make_input(
            discount_offered_before_asked_pct=0.30,
            time_to_first_discount_days=5.0,
            full_price_close_rate_pct=0.20,
        ))
        # composite is rounded to 1 decimal
        assert r.pricing_composite == round(r.pricing_composite, 1)
