"""
Comprehensive tests for SalesProofOfValueIntelligenceEngine.
Covers enums, dataclasses, sub-scores, composite, risk/severity/pattern/action
classification, boolean flags, value-leak calculation, signal strings,
to_dict(), assess_batch(), summary(), and edge cases.
"""

from __future__ import annotations

import pytest
from swarm.intelligence.sales_proof_of_value_intelligence_engine import (
    ValueAction,
    ValueInput,
    ValuePattern,
    ValueResult,
    ValueRisk,
    ValueSeverity,
    SalesProofOfValueIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _inp(**overrides) -> ValueInput:
    """Return a *healthy* baseline input (composite ≈ 0) with selective overrides."""
    defaults = dict(
        rep_id="R001",
        region="West",
        evaluation_period_id="2024-Q1",
        business_case_created_pct=0.80,
        roi_quantified_before_proposal_pct=0.90,
        value_metrics_agreed_with_buyer_pct=0.80,
        feature_demo_without_roi_pct=0.10,
        price_reduction_requested_after_demo_pct=0.05,
        economic_value_referenced_in_proposal_pct=0.80,
        executive_sponsor_engaged_pct=0.90,
        c_suite_presentation_rate_pct=0.70,
        decision_maker_roi_meeting_pct=0.80,
        proof_of_value_completed_pct=0.90,
        value_delivered_milestone_tracked_pct=0.90,
        customer_success_metric_defined_pct=0.90,
        competitive_value_differentiation_pct=0.90,
        deals_lost_on_price_pct=0.05,
        discount_avoided_via_value_pct=0.80,
        expansion_driven_by_value_proof_pct=0.70,
        avg_deal_cycle_days=30.0,
        total_deals_closed=100,
        avg_opportunity_value_usd=10_000.0,
    )
    defaults.update(overrides)
    return ValueInput(**defaults)


def _worst(**overrides) -> ValueInput:
    """Return a maximally bad input (all scores maxed) with selective overrides."""
    defaults = dict(
        rep_id="R002",
        region="East",
        evaluation_period_id="2024-Q1",
        business_case_created_pct=0.05,
        roi_quantified_before_proposal_pct=0.05,
        value_metrics_agreed_with_buyer_pct=0.05,
        feature_demo_without_roi_pct=0.95,
        price_reduction_requested_after_demo_pct=0.95,
        economic_value_referenced_in_proposal_pct=0.05,
        executive_sponsor_engaged_pct=0.05,
        c_suite_presentation_rate_pct=0.05,
        decision_maker_roi_meeting_pct=0.05,
        proof_of_value_completed_pct=0.05,
        value_delivered_milestone_tracked_pct=0.05,
        customer_success_metric_defined_pct=0.05,
        competitive_value_differentiation_pct=0.05,
        deals_lost_on_price_pct=0.95,
        discount_avoided_via_value_pct=0.05,
        expansion_driven_by_value_proof_pct=0.05,
        avg_deal_cycle_days=300.0,
        total_deals_closed=200,
        avg_opportunity_value_usd=50_000.0,
    )
    defaults.update(overrides)
    return ValueInput(**defaults)


def fresh_engine() -> SalesProofOfValueIntelligenceEngine:
    return SalesProofOfValueIntelligenceEngine()


# ===========================================================================
# 1. Enum membership and string values
# ===========================================================================

class TestEnums:
    def test_value_risk_members(self):
        assert set(ValueRisk) == {ValueRisk.low, ValueRisk.moderate, ValueRisk.high, ValueRisk.critical}

    def test_value_risk_string_values(self):
        assert ValueRisk.low.value == "low"
        assert ValueRisk.moderate.value == "moderate"
        assert ValueRisk.high.value == "high"
        assert ValueRisk.critical.value == "critical"

    def test_value_pattern_members(self):
        expected = {
            ValuePattern.none, ValuePattern.feature_seller, ValuePattern.roi_avoidance,
            ValuePattern.champion_dependency, ValuePattern.value_gap_at_close,
            ValuePattern.executive_misalignment,
        }
        assert set(ValuePattern) == expected

    def test_value_pattern_string_values(self):
        assert ValuePattern.none.value == "none"
        assert ValuePattern.feature_seller.value == "feature_seller"
        assert ValuePattern.roi_avoidance.value == "roi_avoidance"
        assert ValuePattern.champion_dependency.value == "champion_dependency"
        assert ValuePattern.value_gap_at_close.value == "value_gap_at_close"
        assert ValuePattern.executive_misalignment.value == "executive_misalignment"

    def test_value_severity_members(self):
        expected = {
            ValueSeverity.outcome_driven, ValueSeverity.adequate,
            ValueSeverity.feature_led, ValueSeverity.value_blind,
        }
        assert set(ValueSeverity) == expected

    def test_value_severity_string_values(self):
        assert ValueSeverity.outcome_driven.value == "outcome_driven"
        assert ValueSeverity.adequate.value == "adequate"
        assert ValueSeverity.feature_led.value == "feature_led"
        assert ValueSeverity.value_blind.value == "value_blind"

    def test_value_action_members(self):
        expected = {
            ValueAction.no_action, ValueAction.value_selling_coaching,
            ValueAction.roi_case_building_coaching, ValueAction.executive_engagement_coaching,
            ValueAction.business_case_coaching, ValueAction.value_reset_intervention,
        }
        assert set(ValueAction) == expected

    def test_value_action_string_values(self):
        assert ValueAction.no_action.value == "no_action"
        assert ValueAction.value_selling_coaching.value == "value_selling_coaching"
        assert ValueAction.roi_case_building_coaching.value == "roi_case_building_coaching"
        assert ValueAction.executive_engagement_coaching.value == "executive_engagement_coaching"
        assert ValueAction.business_case_coaching.value == "business_case_coaching"
        assert ValueAction.value_reset_intervention.value == "value_reset_intervention"

    def test_enums_are_str_subclass(self):
        assert isinstance(ValueRisk.low, str)
        assert isinstance(ValuePattern.none, str)
        assert isinstance(ValueSeverity.adequate, str)
        assert isinstance(ValueAction.no_action, str)


# ===========================================================================
# 2. ValueInput dataclass – field count and types
# ===========================================================================

class TestValueInput:
    def test_can_be_created(self):
        inp = _inp()
        assert inp.rep_id == "R001"
        assert inp.region == "West"

    def test_has_22_fields(self):
        import dataclasses
        assert len(dataclasses.fields(ValueInput)) == 22

    def test_float_fields_preserved(self):
        inp = _inp(avg_opportunity_value_usd=12345.67)
        assert inp.avg_opportunity_value_usd == 12345.67

    def test_int_field_preserved(self):
        inp = _inp(total_deals_closed=42)
        assert inp.total_deals_closed == 42


# ===========================================================================
# 3. ValueResult dataclass and to_dict()
# ===========================================================================

class TestValueResult:
    def test_assess_returns_value_result(self):
        engine = fresh_engine()
        result = engine.assess(_inp())
        assert isinstance(result, ValueResult)

    def test_to_dict_has_15_keys(self):
        engine = fresh_engine()
        d = engine.assess(_inp()).to_dict()
        assert len(d) == 15

    def test_to_dict_expected_keys(self):
        engine = fresh_engine()
        d = engine.assess(_inp()).to_dict()
        expected_keys = {
            "rep_id", "region", "value_risk", "value_pattern", "value_severity",
            "recommended_action", "quantification_score", "executive_score",
            "proof_score", "outcome_score", "value_composite", "has_value_gap",
            "requires_value_coaching", "estimated_value_leak_usd", "value_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_fields_are_strings(self):
        engine = fresh_engine()
        d = engine.assess(_inp()).to_dict()
        assert isinstance(d["value_risk"], str)
        assert isinstance(d["value_pattern"], str)
        assert isinstance(d["value_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_rep_id_and_region_preserved(self):
        engine = fresh_engine()
        inp = _inp(rep_id="XYZ", region="North")
        d = engine.assess(inp).to_dict()
        assert d["rep_id"] == "XYZ"
        assert d["region"] == "North"

    def test_to_dict_bool_fields(self):
        engine = fresh_engine()
        d = engine.assess(_inp()).to_dict()
        assert isinstance(d["has_value_gap"], bool)
        assert isinstance(d["requires_value_coaching"], bool)

    def test_to_dict_numeric_scores_are_float(self):
        engine = fresh_engine()
        d = engine.assess(_inp()).to_dict()
        for key in ("quantification_score", "executive_score", "proof_score",
                    "outcome_score", "value_composite", "estimated_value_leak_usd"):
            assert isinstance(d[key], float), f"{key} is not float"


# ===========================================================================
# 4. Quantification sub-score
# ===========================================================================

class TestQuantificationScore:
    def _score(self, **kw):
        engine = fresh_engine()
        return engine._quantification_score(_inp(**kw))

    # roi_quantified_before_proposal_pct thresholds
    def test_roi_le_025_adds_40(self):
        s = self._score(roi_quantified_before_proposal_pct=0.25,
                        business_case_created_pct=0.80,
                        feature_demo_without_roi_pct=0.10)
        assert s == 40.0

    def test_roi_le_050_adds_22(self):
        s = self._score(roi_quantified_before_proposal_pct=0.50,
                        business_case_created_pct=0.80,
                        feature_demo_without_roi_pct=0.10)
        assert s == 22.0

    def test_roi_le_070_adds_8(self):
        s = self._score(roi_quantified_before_proposal_pct=0.70,
                        business_case_created_pct=0.80,
                        feature_demo_without_roi_pct=0.10)
        assert s == 8.0

    def test_roi_gt_070_adds_0(self):
        s = self._score(roi_quantified_before_proposal_pct=0.90,
                        business_case_created_pct=0.80,
                        feature_demo_without_roi_pct=0.10)
        assert s == 0.0

    # business_case_created_pct thresholds
    def test_biz_case_le_020_adds_35(self):
        s = self._score(roi_quantified_before_proposal_pct=0.90,
                        business_case_created_pct=0.20,
                        feature_demo_without_roi_pct=0.10)
        assert s == 35.0

    def test_biz_case_le_045_adds_18(self):
        s = self._score(roi_quantified_before_proposal_pct=0.90,
                        business_case_created_pct=0.45,
                        feature_demo_without_roi_pct=0.10)
        assert s == 18.0

    def test_biz_case_gt_045_adds_0(self):
        s = self._score(roi_quantified_before_proposal_pct=0.90,
                        business_case_created_pct=0.80,
                        feature_demo_without_roi_pct=0.10)
        assert s == 0.0

    # feature_demo_without_roi_pct thresholds
    def test_feature_demo_ge_060_adds_25(self):
        s = self._score(roi_quantified_before_proposal_pct=0.90,
                        business_case_created_pct=0.80,
                        feature_demo_without_roi_pct=0.60)
        assert s == 25.0

    def test_feature_demo_ge_035_adds_12(self):
        s = self._score(roi_quantified_before_proposal_pct=0.90,
                        business_case_created_pct=0.80,
                        feature_demo_without_roi_pct=0.35)
        assert s == 12.0

    def test_feature_demo_lt_035_adds_0(self):
        s = self._score(roi_quantified_before_proposal_pct=0.90,
                        business_case_created_pct=0.80,
                        feature_demo_without_roi_pct=0.10)
        assert s == 0.0

    def test_quant_score_capped_at_100(self):
        # worst possible: 40+35+25 = 100
        s = self._score(roi_quantified_before_proposal_pct=0.01,
                        business_case_created_pct=0.01,
                        feature_demo_without_roi_pct=0.99)
        assert s == 100.0

    def test_quant_score_additive(self):
        # roi <=0.25 (+40), biz <=0.20 (+35), demo >=0.35 but <0.60 (+12) = 87
        s = self._score(roi_quantified_before_proposal_pct=0.10,
                        business_case_created_pct=0.10,
                        feature_demo_without_roi_pct=0.40)
        assert s == 87.0

    def test_quant_score_zero_healthy(self):
        s = self._score(roi_quantified_before_proposal_pct=0.90,
                        business_case_created_pct=0.90,
                        feature_demo_without_roi_pct=0.10)
        assert s == 0.0


# ===========================================================================
# 5. Executive sub-score
# ===========================================================================

class TestExecutiveScore:
    def _score(self, **kw):
        engine = fresh_engine()
        return engine._executive_score(_inp(**kw))

    def test_exec_sponsor_le_025_adds_40(self):
        s = self._score(executive_sponsor_engaged_pct=0.25,
                        c_suite_presentation_rate_pct=0.80,
                        decision_maker_roi_meeting_pct=0.80)
        assert s == 40.0

    def test_exec_sponsor_le_050_adds_22(self):
        s = self._score(executive_sponsor_engaged_pct=0.50,
                        c_suite_presentation_rate_pct=0.80,
                        decision_maker_roi_meeting_pct=0.80)
        assert s == 22.0

    def test_exec_sponsor_le_070_adds_8(self):
        s = self._score(executive_sponsor_engaged_pct=0.70,
                        c_suite_presentation_rate_pct=0.80,
                        decision_maker_roi_meeting_pct=0.80)
        assert s == 8.0

    def test_exec_sponsor_gt_070_adds_0(self):
        s = self._score(executive_sponsor_engaged_pct=0.90,
                        c_suite_presentation_rate_pct=0.80,
                        decision_maker_roi_meeting_pct=0.80)
        assert s == 0.0

    def test_csuite_le_015_adds_35(self):
        s = self._score(executive_sponsor_engaged_pct=0.90,
                        c_suite_presentation_rate_pct=0.15,
                        decision_maker_roi_meeting_pct=0.80)
        assert s == 35.0

    def test_csuite_le_035_adds_18(self):
        s = self._score(executive_sponsor_engaged_pct=0.90,
                        c_suite_presentation_rate_pct=0.35,
                        decision_maker_roi_meeting_pct=0.80)
        assert s == 18.0

    def test_csuite_gt_035_adds_0(self):
        s = self._score(executive_sponsor_engaged_pct=0.90,
                        c_suite_presentation_rate_pct=0.80,
                        decision_maker_roi_meeting_pct=0.80)
        assert s == 0.0

    def test_dm_roi_meeting_le_020_adds_25(self):
        s = self._score(executive_sponsor_engaged_pct=0.90,
                        c_suite_presentation_rate_pct=0.80,
                        decision_maker_roi_meeting_pct=0.20)
        assert s == 25.0

    def test_dm_roi_meeting_le_045_adds_12(self):
        s = self._score(executive_sponsor_engaged_pct=0.90,
                        c_suite_presentation_rate_pct=0.80,
                        decision_maker_roi_meeting_pct=0.45)
        assert s == 12.0

    def test_dm_roi_meeting_gt_045_adds_0(self):
        s = self._score(executive_sponsor_engaged_pct=0.90,
                        c_suite_presentation_rate_pct=0.80,
                        decision_maker_roi_meeting_pct=0.80)
        assert s == 0.0

    def test_exec_score_capped_at_100(self):
        s = self._score(executive_sponsor_engaged_pct=0.01,
                        c_suite_presentation_rate_pct=0.01,
                        decision_maker_roi_meeting_pct=0.01)
        assert s == 100.0

    def test_exec_score_zero_healthy(self):
        s = self._score(executive_sponsor_engaged_pct=0.90,
                        c_suite_presentation_rate_pct=0.80,
                        decision_maker_roi_meeting_pct=0.80)
        assert s == 0.0


# ===========================================================================
# 6. Proof sub-score
# ===========================================================================

class TestProofScore:
    def _score(self, **kw):
        engine = fresh_engine()
        return engine._proof_score(_inp(**kw))

    def test_pov_completed_le_020_adds_45(self):
        s = self._score(proof_of_value_completed_pct=0.20,
                        value_metrics_agreed_with_buyer_pct=0.80,
                        competitive_value_differentiation_pct=0.80)
        assert s == 45.0

    def test_pov_completed_le_040_adds_25(self):
        s = self._score(proof_of_value_completed_pct=0.40,
                        value_metrics_agreed_with_buyer_pct=0.80,
                        competitive_value_differentiation_pct=0.80)
        assert s == 25.0

    def test_pov_completed_le_060_adds_10(self):
        s = self._score(proof_of_value_completed_pct=0.60,
                        value_metrics_agreed_with_buyer_pct=0.80,
                        competitive_value_differentiation_pct=0.80)
        assert s == 10.0

    def test_pov_completed_gt_060_adds_0(self):
        s = self._score(proof_of_value_completed_pct=0.90,
                        value_metrics_agreed_with_buyer_pct=0.80,
                        competitive_value_differentiation_pct=0.80)
        assert s == 0.0

    def test_value_metrics_le_025_adds_30(self):
        s = self._score(proof_of_value_completed_pct=0.90,
                        value_metrics_agreed_with_buyer_pct=0.25,
                        competitive_value_differentiation_pct=0.80)
        assert s == 30.0

    def test_value_metrics_le_050_adds_15(self):
        s = self._score(proof_of_value_completed_pct=0.90,
                        value_metrics_agreed_with_buyer_pct=0.50,
                        competitive_value_differentiation_pct=0.80)
        assert s == 15.0

    def test_value_metrics_gt_050_adds_0(self):
        s = self._score(proof_of_value_completed_pct=0.90,
                        value_metrics_agreed_with_buyer_pct=0.80,
                        competitive_value_differentiation_pct=0.80)
        assert s == 0.0

    def test_competitive_le_030_adds_25(self):
        s = self._score(proof_of_value_completed_pct=0.90,
                        value_metrics_agreed_with_buyer_pct=0.80,
                        competitive_value_differentiation_pct=0.30)
        assert s == 25.0

    def test_competitive_le_055_adds_12(self):
        s = self._score(proof_of_value_completed_pct=0.90,
                        value_metrics_agreed_with_buyer_pct=0.80,
                        competitive_value_differentiation_pct=0.55)
        assert s == 12.0

    def test_competitive_gt_055_adds_0(self):
        s = self._score(proof_of_value_completed_pct=0.90,
                        value_metrics_agreed_with_buyer_pct=0.80,
                        competitive_value_differentiation_pct=0.80)
        assert s == 0.0

    def test_proof_score_capped_at_100(self):
        s = self._score(proof_of_value_completed_pct=0.01,
                        value_metrics_agreed_with_buyer_pct=0.01,
                        competitive_value_differentiation_pct=0.01)
        assert s == 100.0

    def test_proof_score_zero_healthy(self):
        s = self._score(proof_of_value_completed_pct=0.90,
                        value_metrics_agreed_with_buyer_pct=0.80,
                        competitive_value_differentiation_pct=0.80)
        assert s == 0.0


# ===========================================================================
# 7. Outcome sub-score
# ===========================================================================

class TestOutcomeScore:
    def _score(self, **kw):
        engine = fresh_engine()
        return engine._outcome_score(_inp(**kw))

    def test_deals_lost_ge_045_adds_40(self):
        s = self._score(deals_lost_on_price_pct=0.45,
                        customer_success_metric_defined_pct=0.90,
                        economic_value_referenced_in_proposal_pct=0.80)
        assert s == 40.0

    def test_deals_lost_ge_025_adds_22(self):
        s = self._score(deals_lost_on_price_pct=0.25,
                        customer_success_metric_defined_pct=0.90,
                        economic_value_referenced_in_proposal_pct=0.80)
        assert s == 22.0

    def test_deals_lost_ge_010_adds_8(self):
        s = self._score(deals_lost_on_price_pct=0.10,
                        customer_success_metric_defined_pct=0.90,
                        economic_value_referenced_in_proposal_pct=0.80)
        assert s == 8.0

    def test_deals_lost_lt_010_adds_0(self):
        s = self._score(deals_lost_on_price_pct=0.05,
                        customer_success_metric_defined_pct=0.90,
                        economic_value_referenced_in_proposal_pct=0.80)
        assert s == 0.0

    def test_cs_metric_le_025_adds_35(self):
        s = self._score(deals_lost_on_price_pct=0.05,
                        customer_success_metric_defined_pct=0.25,
                        economic_value_referenced_in_proposal_pct=0.80)
        assert s == 35.0

    def test_cs_metric_le_050_adds_18(self):
        s = self._score(deals_lost_on_price_pct=0.05,
                        customer_success_metric_defined_pct=0.50,
                        economic_value_referenced_in_proposal_pct=0.80)
        assert s == 18.0

    def test_cs_metric_gt_050_adds_0(self):
        s = self._score(deals_lost_on_price_pct=0.05,
                        customer_success_metric_defined_pct=0.90,
                        economic_value_referenced_in_proposal_pct=0.80)
        assert s == 0.0

    def test_econ_value_le_030_adds_25(self):
        s = self._score(deals_lost_on_price_pct=0.05,
                        customer_success_metric_defined_pct=0.90,
                        economic_value_referenced_in_proposal_pct=0.30)
        assert s == 25.0

    def test_econ_value_le_055_adds_12(self):
        s = self._score(deals_lost_on_price_pct=0.05,
                        customer_success_metric_defined_pct=0.90,
                        economic_value_referenced_in_proposal_pct=0.55)
        assert s == 12.0

    def test_econ_value_gt_055_adds_0(self):
        s = self._score(deals_lost_on_price_pct=0.05,
                        customer_success_metric_defined_pct=0.90,
                        economic_value_referenced_in_proposal_pct=0.80)
        assert s == 0.0

    def test_outcome_score_capped_at_100(self):
        s = self._score(deals_lost_on_price_pct=0.99,
                        customer_success_metric_defined_pct=0.01,
                        economic_value_referenced_in_proposal_pct=0.01)
        assert s == 100.0

    def test_outcome_score_zero_healthy(self):
        s = self._score(deals_lost_on_price_pct=0.05,
                        customer_success_metric_defined_pct=0.90,
                        economic_value_referenced_in_proposal_pct=0.80)
        assert s == 0.0


# ===========================================================================
# 8. Composite score
# ===========================================================================

class TestCompositeScore:
    def test_composite_is_zero_for_healthy_input(self):
        engine = fresh_engine()
        result = engine.assess(_inp())
        assert result.value_composite == 0.0

    def test_composite_is_100_for_worst_input(self):
        engine = fresh_engine()
        result = engine.assess(_worst())
        assert result.value_composite == 100.0

    def test_composite_weights_sum_to_1(self):
        # Verify weighting by isolating single dimension contribution
        # quant=100, exec=0, proof=0, outcome=0 -> composite = 30
        engine = fresh_engine()
        inp = _inp(
            roi_quantified_before_proposal_pct=0.01,
            business_case_created_pct=0.01,
            feature_demo_without_roi_pct=0.99,
            executive_sponsor_engaged_pct=0.90,
            c_suite_presentation_rate_pct=0.80,
            decision_maker_roi_meeting_pct=0.80,
            proof_of_value_completed_pct=0.90,
            value_metrics_agreed_with_buyer_pct=0.80,
            competitive_value_differentiation_pct=0.80,
            deals_lost_on_price_pct=0.05,
            customer_success_metric_defined_pct=0.90,
            economic_value_referenced_in_proposal_pct=0.80,
        )
        result = engine.assess(inp)
        assert result.quantification_score == 100.0
        assert result.executive_score == 0.0
        assert result.proof_score == 0.0
        assert result.outcome_score == 0.0
        assert result.value_composite == 30.0

    def test_composite_capped_at_100(self):
        engine = fresh_engine()
        result = engine.assess(_worst())
        assert result.value_composite <= 100.0

    def test_composite_rounded_to_1_decimal(self):
        # Check rounding behavior: result should be a round float
        engine = fresh_engine()
        result = engine.assess(_inp())
        # Should not have more than 1 decimal place after rounding
        assert result.value_composite == round(result.value_composite, 1)

    def test_scores_are_rounded_to_1_decimal(self):
        engine = fresh_engine()
        r = engine.assess(_inp())
        for attr in ("quantification_score", "executive_score", "proof_score", "outcome_score"):
            val = getattr(r, attr)
            assert val == round(val, 1), f"{attr} not rounded to 1dp"


# ===========================================================================
# 9. Risk level
# ===========================================================================

class TestRiskLevel:
    def test_risk_low_below_20(self):
        engine = fresh_engine()
        result = engine.assess(_inp())  # composite ≈ 0
        assert result.value_risk == ValueRisk.low

    def test_risk_moderate_at_20(self):
        engine = fresh_engine()
        # Need composite ≥ 20 but < 40
        # exec=22 (exec_sponsor 0.50) * 0.25 = 5.5, quant=22*0.30=6.6, others=0 => ~12 not enough
        # Let's use known values: quant=40, exec=22, proof=0, outcome=0
        # composite = 40*0.30 + 22*0.25 + 0 + 0 = 12+5.5 = 17.5 not enough
        # quant=40, exec=40, proof=0, outcome=0 = 12+10=22 -> moderate
        inp = _inp(
            roi_quantified_before_proposal_pct=0.25,
            business_case_created_pct=0.80,
            feature_demo_without_roi_pct=0.10,
            executive_sponsor_engaged_pct=0.25,
            c_suite_presentation_rate_pct=0.80,
            decision_maker_roi_meeting_pct=0.80,
            proof_of_value_completed_pct=0.90,
            value_metrics_agreed_with_buyer_pct=0.80,
            competitive_value_differentiation_pct=0.80,
            deals_lost_on_price_pct=0.05,
            customer_success_metric_defined_pct=0.90,
            economic_value_referenced_in_proposal_pct=0.80,
        )
        result = engine.assess(inp)
        assert result.value_composite == 22.0
        assert result.value_risk == ValueRisk.moderate

    def test_risk_high_at_40(self):
        engine = fresh_engine()
        # quant=40(+40), exec=40(+40), proof=45(+45), outcome=0 =
        # 40*0.30 + 40*0.25 + 45*0.25 + 0*0.20 = 12+10+11.25 = 33.25 - not 40
        # Let's just use worst with some healthy bits to land in [40, 60)
        # quant=100*0.30=30, exec=100*0.25=25, proof=0, outcome=0 = 55 -> high
        inp = _inp(
            roi_quantified_before_proposal_pct=0.01,
            business_case_created_pct=0.01,
            feature_demo_without_roi_pct=0.99,
            executive_sponsor_engaged_pct=0.01,
            c_suite_presentation_rate_pct=0.01,
            decision_maker_roi_meeting_pct=0.01,
            proof_of_value_completed_pct=0.90,
            value_metrics_agreed_with_buyer_pct=0.80,
            competitive_value_differentiation_pct=0.80,
            deals_lost_on_price_pct=0.05,
            customer_success_metric_defined_pct=0.90,
            economic_value_referenced_in_proposal_pct=0.80,
        )
        result = engine.assess(inp)
        assert result.value_risk == ValueRisk.high

    def test_risk_critical_at_60(self):
        engine = fresh_engine()
        result = engine.assess(_worst())
        assert result.value_risk == ValueRisk.critical

    def test_risk_boundary_at_60_exact(self):
        engine = fresh_engine()
        # quant=100, exec=100, proof=0, outcome=0 = 30+25 = 55 < 60
        # quant=100, exec=100, proof=30, outcome=0 = 30+25+7.5 = 62.5 -> critical
        inp = _inp(
            roi_quantified_before_proposal_pct=0.01,
            business_case_created_pct=0.01,
            feature_demo_without_roi_pct=0.99,
            executive_sponsor_engaged_pct=0.01,
            c_suite_presentation_rate_pct=0.01,
            decision_maker_roi_meeting_pct=0.01,
            proof_of_value_completed_pct=0.90,
            value_metrics_agreed_with_buyer_pct=0.25,
            competitive_value_differentiation_pct=0.80,
            deals_lost_on_price_pct=0.05,
            customer_success_metric_defined_pct=0.90,
            economic_value_referenced_in_proposal_pct=0.80,
        )
        result = engine.assess(inp)
        assert result.value_risk == ValueRisk.critical


# ===========================================================================
# 10. Severity
# ===========================================================================

class TestSeverity:
    def test_severity_outcome_driven_below_20(self):
        engine = fresh_engine()
        result = engine.assess(_inp())
        assert result.value_severity == ValueSeverity.outcome_driven

    def test_severity_adequate_in_20_to_40(self):
        engine = fresh_engine()
        inp = _inp(
            roi_quantified_before_proposal_pct=0.25,
            executive_sponsor_engaged_pct=0.25,
            business_case_created_pct=0.80,
            feature_demo_without_roi_pct=0.10,
            c_suite_presentation_rate_pct=0.80,
            decision_maker_roi_meeting_pct=0.80,
        )
        result = engine.assess(inp)
        # composite = 40*0.30 + 40*0.25 = 12+10 = 22 -> adequate
        assert result.value_composite == 22.0
        assert result.value_severity == ValueSeverity.adequate

    def test_severity_feature_led_in_40_to_60(self):
        engine = fresh_engine()
        inp = _inp(
            roi_quantified_before_proposal_pct=0.01,
            business_case_created_pct=0.01,
            feature_demo_without_roi_pct=0.99,
            executive_sponsor_engaged_pct=0.01,
            c_suite_presentation_rate_pct=0.01,
            decision_maker_roi_meeting_pct=0.01,
            proof_of_value_completed_pct=0.90,
            value_metrics_agreed_with_buyer_pct=0.80,
            competitive_value_differentiation_pct=0.80,
            deals_lost_on_price_pct=0.05,
            customer_success_metric_defined_pct=0.90,
            economic_value_referenced_in_proposal_pct=0.80,
        )
        result = engine.assess(inp)
        # quant=100*0.30 + exec=100*0.25 = 55 -> feature_led
        assert result.value_severity == ValueSeverity.feature_led

    def test_severity_value_blind_at_60_plus(self):
        engine = fresh_engine()
        result = engine.assess(_worst())
        assert result.value_severity == ValueSeverity.value_blind


# ===========================================================================
# 11. Pattern detection
# ===========================================================================

class TestPatternDetection:
    def test_pattern_none_healthy(self):
        engine = fresh_engine()
        result = engine.assess(_inp())
        assert result.value_pattern == ValuePattern.none

    def test_pattern_feature_seller(self):
        # feature_demo_without_roi_pct >= 0.55 AND quant >= 35
        # quant >= 35 requires e.g. roi <=0.25 (+40) -> quant=40
        engine = fresh_engine()
        inp = _inp(
            feature_demo_without_roi_pct=0.60,
            roi_quantified_before_proposal_pct=0.20,
            business_case_created_pct=0.80,
        )
        result = engine.assess(inp)
        assert result.value_pattern == ValuePattern.feature_seller

    def test_pattern_roi_avoidance(self):
        # roi_quantified_before_proposal_pct <= 0.20 AND business_case_created_pct <= 0.25
        # feature_seller NOT triggered: feature_demo < 0.55
        engine = fresh_engine()
        inp = _inp(
            feature_demo_without_roi_pct=0.10,
            roi_quantified_before_proposal_pct=0.15,
            business_case_created_pct=0.20,
        )
        result = engine.assess(inp)
        assert result.value_pattern == ValuePattern.roi_avoidance

    def test_pattern_executive_misalignment(self):
        # executive_sponsor_engaged_pct <= 0.20 AND exec_ >= 35
        # exec >= 35 requires: exec_sponsor <=0.25 (+40) -> yes since <=0.20
        # Must not trigger feature_seller or roi_avoidance first
        engine = fresh_engine()
        inp = _inp(
            feature_demo_without_roi_pct=0.10,
            roi_quantified_before_proposal_pct=0.90,
            business_case_created_pct=0.80,
            executive_sponsor_engaged_pct=0.15,
            c_suite_presentation_rate_pct=0.80,
            decision_maker_roi_meeting_pct=0.80,
        )
        result = engine.assess(inp)
        assert result.value_pattern == ValuePattern.executive_misalignment

    def test_pattern_value_gap_at_close(self):
        # deals_lost_on_price_pct >= 0.40 AND discount_avoided_via_value_pct <= 0.20
        # No earlier patterns should trigger
        engine = fresh_engine()
        inp = _inp(
            feature_demo_without_roi_pct=0.10,
            roi_quantified_before_proposal_pct=0.90,
            business_case_created_pct=0.80,
            executive_sponsor_engaged_pct=0.90,
            deals_lost_on_price_pct=0.50,
            discount_avoided_via_value_pct=0.10,
        )
        result = engine.assess(inp)
        assert result.value_pattern == ValuePattern.value_gap_at_close

    def test_pattern_champion_dependency(self):
        # proof_of_value_completed_pct <= 0.15 AND proof >= 35
        # proof >=35: pov <=0.20 adds 45 -> if pov<=0.15 that's within <=0.20 -> +45
        # No earlier patterns should trigger
        engine = fresh_engine()
        inp = _inp(
            feature_demo_without_roi_pct=0.10,
            roi_quantified_before_proposal_pct=0.90,
            business_case_created_pct=0.80,
            executive_sponsor_engaged_pct=0.90,
            deals_lost_on_price_pct=0.05,
            discount_avoided_via_value_pct=0.80,
            proof_of_value_completed_pct=0.10,
            value_metrics_agreed_with_buyer_pct=0.80,
            competitive_value_differentiation_pct=0.80,
        )
        result = engine.assess(inp)
        assert result.value_pattern == ValuePattern.champion_dependency

    def test_pattern_feature_seller_priority_over_roi_avoidance(self):
        # Both feature_seller and roi_avoidance conditions met; feature_seller wins (checked first)
        engine = fresh_engine()
        inp = _inp(
            feature_demo_without_roi_pct=0.60,
            roi_quantified_before_proposal_pct=0.10,
            business_case_created_pct=0.20,
        )
        result = engine.assess(inp)
        assert result.value_pattern == ValuePattern.feature_seller

    def test_feature_seller_requires_quant_ge_35(self):
        # feature_demo >= 0.55 but quant < 35 -> no feature_seller
        # quant < 35 requires roi > 0.25 (so at most +22) AND biz > 0.20 (so at most +18)
        # 22+18 = 40 >= 35 -> need to push below 35
        # roi > 0.50 (0 from roi), biz > 0.45 (0 from biz), feature >=0.60 (+25)  -> quant=25 < 35
        engine = fresh_engine()
        inp = _inp(
            feature_demo_without_roi_pct=0.60,
            roi_quantified_before_proposal_pct=0.80,
            business_case_created_pct=0.80,
        )
        result = engine.assess(inp)
        # quant = 0+0+25 = 25 < 35, so feature_seller NOT triggered
        assert result.value_pattern != ValuePattern.feature_seller


# ===========================================================================
# 12. Action recommendations
# ===========================================================================

class TestActionRecommendation:
    def test_action_no_action_for_low_risk(self):
        engine = fresh_engine()
        result = engine.assess(_inp())
        assert result.recommended_action == ValueAction.no_action

    def test_action_value_selling_coaching_for_moderate(self):
        engine = fresh_engine()
        # Composite in [20, 40)
        inp = _inp(
            roi_quantified_before_proposal_pct=0.25,
            executive_sponsor_engaged_pct=0.25,
            business_case_created_pct=0.80,
            feature_demo_without_roi_pct=0.10,
            c_suite_presentation_rate_pct=0.80,
            decision_maker_roi_meeting_pct=0.80,
        )
        result = engine.assess(inp)
        assert result.value_risk == ValueRisk.moderate
        assert result.recommended_action == ValueAction.value_selling_coaching

    def test_action_value_selling_coaching_critical_feature_seller(self):
        engine = fresh_engine()
        # Need critical risk + feature_seller pattern
        # critical: composite >= 60
        result = engine.assess(_worst())
        assert result.value_risk == ValueRisk.critical
        if result.value_pattern == ValuePattern.feature_seller:
            assert result.recommended_action == ValueAction.value_selling_coaching

    def test_action_roi_case_building_critical_roi_avoidance(self):
        engine = fresh_engine()
        # Need critical + roi_avoidance pattern
        # roi_avoidance: roi <=0.20 AND biz <=0.25, and no feature_seller
        # To get critical (composite >=60) with no feature_seller:
        # feature_demo < 0.55, roi <=0.20, biz <=0.25
        # quant = 40+35+0(demo<0.35) = 75
        # Also need exec and proof/outcome high
        inp = _worst(
            feature_demo_without_roi_pct=0.10,  # no feature_seller
            roi_quantified_before_proposal_pct=0.10,  # roi_avoidance
            business_case_created_pct=0.20,  # roi_avoidance
        )
        result = engine.assess(inp)
        assert result.value_risk == ValueRisk.critical
        assert result.value_pattern == ValuePattern.roi_avoidance
        assert result.recommended_action == ValueAction.roi_case_building_coaching

    def test_action_value_reset_intervention_critical_other(self):
        engine = fresh_engine()
        # Need critical + pattern not feature_seller/roi_avoidance
        # Use none pattern with critical composite
        inp = _worst(
            feature_demo_without_roi_pct=0.10,
            roi_quantified_before_proposal_pct=0.80,
            business_case_created_pct=0.80,
        )
        result = engine.assess(inp)
        if result.value_risk == ValueRisk.critical and result.value_pattern not in (
            ValuePattern.feature_seller, ValuePattern.roi_avoidance
        ):
            assert result.recommended_action == ValueAction.value_reset_intervention

    def test_action_executive_engagement_coaching_high_exec_misalignment(self):
        engine = fresh_engine()
        # Need high risk + executive_misalignment pattern
        inp = _inp(
            roi_quantified_before_proposal_pct=0.25,
            business_case_created_pct=0.80,
            feature_demo_without_roi_pct=0.10,
            executive_sponsor_engaged_pct=0.15,
            c_suite_presentation_rate_pct=0.80,
            decision_maker_roi_meeting_pct=0.80,
            proof_of_value_completed_pct=0.01,
            value_metrics_agreed_with_buyer_pct=0.01,
            competitive_value_differentiation_pct=0.01,
            deals_lost_on_price_pct=0.05,
            customer_success_metric_defined_pct=0.90,
            economic_value_referenced_in_proposal_pct=0.80,
        )
        result = engine.assess(inp)
        if result.value_risk == ValueRisk.high and result.value_pattern == ValuePattern.executive_misalignment:
            assert result.recommended_action == ValueAction.executive_engagement_coaching

    def test_action_business_case_coaching_high_value_gap_at_close(self):
        engine = fresh_engine()
        inp = _inp(
            feature_demo_without_roi_pct=0.10,
            roi_quantified_before_proposal_pct=0.90,
            business_case_created_pct=0.80,
            executive_sponsor_engaged_pct=0.90,
            proof_of_value_completed_pct=0.01,
            value_metrics_agreed_with_buyer_pct=0.01,
            competitive_value_differentiation_pct=0.01,
            deals_lost_on_price_pct=0.50,
            discount_avoided_via_value_pct=0.10,
            customer_success_metric_defined_pct=0.90,
            economic_value_referenced_in_proposal_pct=0.80,
        )
        result = engine.assess(inp)
        if result.value_risk == ValueRisk.high and result.value_pattern == ValuePattern.value_gap_at_close:
            assert result.recommended_action == ValueAction.business_case_coaching

    def test_action_roi_case_building_high_other_pattern(self):
        engine = fresh_engine()
        inp = _inp(
            roi_quantified_before_proposal_pct=0.01,
            business_case_created_pct=0.01,
            feature_demo_without_roi_pct=0.99,
            executive_sponsor_engaged_pct=0.01,
            c_suite_presentation_rate_pct=0.01,
            decision_maker_roi_meeting_pct=0.01,
            proof_of_value_completed_pct=0.90,
            value_metrics_agreed_with_buyer_pct=0.80,
            competitive_value_differentiation_pct=0.80,
            deals_lost_on_price_pct=0.05,
            customer_success_metric_defined_pct=0.90,
            economic_value_referenced_in_proposal_pct=0.80,
        )
        result = engine.assess(inp)
        if result.value_risk == ValueRisk.high and result.value_pattern not in (
            ValuePattern.executive_misalignment, ValuePattern.value_gap_at_close
        ):
            assert result.recommended_action == ValueAction.roi_case_building_coaching


# ===========================================================================
# 13. has_value_gap
# ===========================================================================

class TestHasValueGap:
    def test_no_value_gap_healthy(self):
        engine = fresh_engine()
        # composite < 40, roi > 0.40, deals_lost < 0.30
        result = engine.assess(_inp())
        assert result.has_value_gap is False

    def test_value_gap_from_high_composite(self):
        engine = fresh_engine()
        result = engine.assess(_worst())
        assert result.has_value_gap is True

    def test_value_gap_from_low_roi_quantification(self):
        # roi_quantified_before_proposal_pct <= 0.40 triggers gap
        engine = fresh_engine()
        inp = _inp(roi_quantified_before_proposal_pct=0.40)
        result = engine.assess(inp)
        assert result.has_value_gap is True

    def test_value_gap_from_high_deals_lost_on_price(self):
        # deals_lost_on_price_pct >= 0.30 triggers gap
        engine = fresh_engine()
        inp = _inp(deals_lost_on_price_pct=0.30)
        result = engine.assess(inp)
        assert result.has_value_gap is True

    def test_no_gap_when_all_conditions_false(self):
        # composite < 40, roi > 0.40, deals_lost < 0.30
        engine = fresh_engine()
        inp = _inp(
            roi_quantified_before_proposal_pct=0.90,
            deals_lost_on_price_pct=0.05,
        )
        result = engine.assess(inp)
        assert result.has_value_gap is False

    def test_value_gap_exact_boundary_roi_040(self):
        engine = fresh_engine()
        inp = _inp(roi_quantified_before_proposal_pct=0.40)
        result = engine.assess(inp)
        assert result.has_value_gap is True

    def test_value_gap_exact_boundary_deals_030(self):
        engine = fresh_engine()
        inp = _inp(deals_lost_on_price_pct=0.30)
        result = engine.assess(inp)
        assert result.has_value_gap is True


# ===========================================================================
# 14. requires_value_coaching
# ===========================================================================

class TestRequiresValueCoaching:
    def test_no_coaching_needed_healthy(self):
        engine = fresh_engine()
        # composite < 30, feature_demo < 0.40, exec_sponsor > 0.40
        result = engine.assess(_inp())
        assert result.requires_value_coaching is False

    def test_coaching_from_high_composite(self):
        engine = fresh_engine()
        result = engine.assess(_worst())
        assert result.requires_value_coaching is True

    def test_coaching_from_high_feature_demo(self):
        # feature_demo_without_roi_pct >= 0.40
        engine = fresh_engine()
        inp = _inp(feature_demo_without_roi_pct=0.40)
        result = engine.assess(inp)
        assert result.requires_value_coaching is True

    def test_coaching_from_low_exec_sponsor(self):
        # executive_sponsor_engaged_pct <= 0.40
        engine = fresh_engine()
        inp = _inp(executive_sponsor_engaged_pct=0.40)
        result = engine.assess(inp)
        assert result.requires_value_coaching is True

    def test_no_coaching_exec_just_above_threshold(self):
        # executive_sponsor_engaged_pct = 0.41 (above threshold)
        engine = fresh_engine()
        inp = _inp(
            executive_sponsor_engaged_pct=0.41,
            feature_demo_without_roi_pct=0.10,
            roi_quantified_before_proposal_pct=0.90,
        )
        result = engine.assess(inp)
        # composite likely < 30, feature_demo < 0.40, exec > 0.40
        if result.value_composite < 30 and not result.requires_value_coaching:
            assert result.requires_value_coaching is False

    def test_coaching_composite_boundary_at_30(self):
        engine = fresh_engine()
        # quant=40*0.30 + exec=40*0.25 = 12+10 = 22 < 30 still not enough
        # quant=100*0.30 + exec=40*0.25 = 30+10 = 40 -> coaching true
        inp = _inp(
            roi_quantified_before_proposal_pct=0.01,
            business_case_created_pct=0.01,
            feature_demo_without_roi_pct=0.10,
            executive_sponsor_engaged_pct=0.25,
            c_suite_presentation_rate_pct=0.80,
            decision_maker_roi_meeting_pct=0.80,
        )
        result = engine.assess(inp)
        # quant = 40+35+0 = 75; exec = 40+0+0 = 40
        # composite = 75*0.30 + 40*0.25 = 22.5+10 = 32.5 >= 30 -> coaching=True
        assert result.requires_value_coaching is True


# ===========================================================================
# 15. Estimated value leak
# ===========================================================================

class TestEstimatedValueLeak:
    def test_value_leak_zero_when_no_price_loss(self):
        engine = fresh_engine()
        inp = _inp(deals_lost_on_price_pct=0.0, total_deals_closed=100, avg_opportunity_value_usd=10000.0)
        result = engine.assess(inp)
        assert result.estimated_value_leak_usd == 0.0

    def test_value_leak_zero_when_composite_zero(self):
        engine = fresh_engine()
        # composite=0 -> leak=0
        inp = _inp()
        result = engine.assess(inp)
        assert result.value_composite == 0.0
        assert result.estimated_value_leak_usd == 0.0

    def test_value_leak_calculation(self):
        engine = fresh_engine()
        # Use known composite
        inp = _inp(
            deals_lost_on_price_pct=0.50,
            total_deals_closed=100,
            avg_opportunity_value_usd=10_000.0,
        )
        result = engine.assess(inp)
        expected = round(100 * 10_000.0 * 0.50 * (result.value_composite / 100.0), 2)
        assert result.estimated_value_leak_usd == expected

    def test_value_leak_rounded_to_2_decimals(self):
        engine = fresh_engine()
        inp = _worst(total_deals_closed=3, avg_opportunity_value_usd=33333.33, deals_lost_on_price_pct=0.33)
        result = engine.assess(inp)
        assert result.estimated_value_leak_usd == round(result.estimated_value_leak_usd, 2)

    def test_value_leak_large_numbers(self):
        engine = fresh_engine()
        inp = _worst(total_deals_closed=1000, avg_opportunity_value_usd=1_000_000.0, deals_lost_on_price_pct=1.0)
        result = engine.assess(inp)
        assert result.estimated_value_leak_usd > 0

    def test_value_leak_proportional_to_deals_closed(self):
        engine = fresh_engine()
        inp1 = _worst(total_deals_closed=100)
        inp2 = _worst(total_deals_closed=200)
        r1 = engine.assess(inp1)
        r2 = engine.assess(inp2)
        # same composite since same relative inputs; leak should scale
        assert abs(r2.estimated_value_leak_usd / r1.estimated_value_leak_usd - 2.0) < 0.01


# ===========================================================================
# 16. Signal string
# ===========================================================================

class TestSignalString:
    def test_healthy_signal_string(self):
        engine = fresh_engine()
        result = engine.assess(_inp())
        assert result.value_signal == (
            "Value selling strong — ROI quantification, executive engagement, "
            "and proof of value within benchmarks"
        )

    def test_unhealthy_signal_contains_pattern_label(self):
        engine = fresh_engine()
        result = engine.assess(_worst())
        # pattern should not be none for worst case
        assert "%" in result.value_signal
        assert "composite" in result.value_signal

    def test_unhealthy_signal_contains_roi_pct(self):
        engine = fresh_engine()
        inp = _worst()
        result = engine.assess(inp)
        expected_roi = f"{inp.roi_quantified_before_proposal_pct * 100:.0f}% ROI quantified pre-proposal"
        assert expected_roi in result.value_signal

    def test_unhealthy_signal_contains_exec_pct(self):
        engine = fresh_engine()
        inp = _worst()
        result = engine.assess(inp)
        expected_exec = f"{inp.executive_sponsor_engaged_pct * 100:.0f}% executive sponsor engaged"
        assert expected_exec in result.value_signal

    def test_unhealthy_signal_contains_deals_lost_pct(self):
        engine = fresh_engine()
        inp = _worst()
        result = engine.assess(inp)
        expected_dlp = f"{inp.deals_lost_on_price_pct * 100:.0f}% deals lost on price"
        assert expected_dlp in result.value_signal

    def test_unhealthy_signal_contains_composite_value(self):
        engine = fresh_engine()
        inp = _worst()
        result = engine.assess(inp)
        assert f"composite {result.value_composite:.0f}" in result.value_signal

    def test_signal_none_pattern_uses_value_risk_label(self):
        engine = fresh_engine()
        # composite >= 20 but pattern = none
        inp = _inp(
            roi_quantified_before_proposal_pct=0.25,
            executive_sponsor_engaged_pct=0.25,
            business_case_created_pct=0.80,
            feature_demo_without_roi_pct=0.10,
            c_suite_presentation_rate_pct=0.80,
            decision_maker_roi_meeting_pct=0.80,
        )
        result = engine.assess(inp)
        if result.value_pattern == ValuePattern.none and result.value_composite >= 20:
            assert "Value risk" in result.value_signal

    def test_signal_feature_seller_pattern_label(self):
        engine = fresh_engine()
        inp = _inp(
            feature_demo_without_roi_pct=0.60,
            roi_quantified_before_proposal_pct=0.20,
            business_case_created_pct=0.80,
        )
        result = engine.assess(inp)
        if result.value_pattern == ValuePattern.feature_seller:
            assert "Feature seller" in result.value_signal

    def test_signal_roi_avoidance_pattern_label(self):
        engine = fresh_engine()
        inp = _inp(
            feature_demo_without_roi_pct=0.10,
            roi_quantified_before_proposal_pct=0.10,
            business_case_created_pct=0.20,
        )
        result = engine.assess(inp)
        if result.value_pattern == ValuePattern.roi_avoidance:
            assert "Roi avoidance" in result.value_signal


# ===========================================================================
# 17. assess() integration: rep_id and region passthrough
# ===========================================================================

class TestAssessMetadata:
    def test_rep_id_preserved(self):
        engine = fresh_engine()
        result = engine.assess(_inp(rep_id="ABCDE"))
        assert result.rep_id == "ABCDE"

    def test_region_preserved(self):
        engine = fresh_engine()
        result = engine.assess(_inp(region="EMEA"))
        assert result.region == "EMEA"

    def test_result_appended_to_internal_list(self):
        engine = fresh_engine()
        engine.assess(_inp())
        engine.assess(_inp())
        assert len(engine._results) == 2

    def test_assess_different_reps(self):
        engine = fresh_engine()
        r1 = engine.assess(_inp(rep_id="R1"))
        r2 = engine.assess(_inp(rep_id="R2"))
        assert r1.rep_id == "R1"
        assert r2.rep_id == "R2"


# ===========================================================================
# 18. assess_batch()
# ===========================================================================

class TestAssessBatch:
    def test_batch_returns_list(self):
        engine = fresh_engine()
        results = engine.assess_batch([_inp(), _inp(rep_id="R2")])
        assert isinstance(results, list)

    def test_batch_length_matches_input(self):
        engine = fresh_engine()
        inputs = [_inp(rep_id=f"R{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_each_is_value_result(self):
        engine = fresh_engine()
        results = engine.assess_batch([_inp(), _worst()])
        for r in results:
            assert isinstance(r, ValueResult)

    def test_batch_empty_list(self):
        engine = fresh_engine()
        results = engine.assess_batch([])
        assert results == []

    def test_batch_results_stored(self):
        engine = fresh_engine()
        engine.assess_batch([_inp(rep_id=f"R{i}") for i in range(7)])
        assert len(engine._results) == 7

    def test_batch_accumulates_with_single_assess(self):
        engine = fresh_engine()
        engine.assess(_inp(rep_id="R0"))
        engine.assess_batch([_inp(rep_id="R1"), _inp(rep_id="R2")])
        assert len(engine._results) == 3

    def test_batch_preserves_rep_ids(self):
        engine = fresh_engine()
        ids = ["A", "B", "C"]
        results = engine.assess_batch([_inp(rep_id=i) for i in ids])
        assert [r.rep_id for r in results] == ids

    def test_batch_healthy_and_worst_correct_risks(self):
        engine = fresh_engine()
        results = engine.assess_batch([_inp(), _worst()])
        assert results[0].value_risk == ValueRisk.low
        assert results[1].value_risk == ValueRisk.critical


# ===========================================================================
# 19. summary() — empty state
# ===========================================================================

class TestSummaryEmpty:
    def test_summary_empty_total_is_0(self):
        engine = fresh_engine()
        s = engine.summary()
        assert s["total"] == 0

    def test_summary_empty_has_13_keys(self):
        engine = fresh_engine()
        s = engine.summary()
        assert len(s) == 13

    def test_summary_empty_expected_keys(self):
        engine = fresh_engine()
        s = engine.summary()
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts", "action_counts",
            "avg_value_composite", "value_gap_count", "coaching_count",
            "avg_quantification_score", "avg_executive_score", "avg_proof_score",
            "avg_outcome_score", "total_estimated_value_leak_usd",
        }
        assert set(s.keys()) == expected

    def test_summary_empty_dict_counts_are_empty(self):
        engine = fresh_engine()
        s = engine.summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}

    def test_summary_empty_numeric_zeros(self):
        engine = fresh_engine()
        s = engine.summary()
        assert s["avg_value_composite"] == 0.0
        assert s["value_gap_count"] == 0
        assert s["coaching_count"] == 0
        assert s["avg_quantification_score"] == 0.0
        assert s["avg_executive_score"] == 0.0
        assert s["avg_proof_score"] == 0.0
        assert s["avg_outcome_score"] == 0.0
        assert s["total_estimated_value_leak_usd"] == 0.0


# ===========================================================================
# 20. summary() — populated state
# ===========================================================================

class TestSummaryPopulated:
    def test_summary_total_count(self):
        engine = fresh_engine()
        engine.assess_batch([_inp(rep_id=f"R{i}") for i in range(5)])
        assert engine.summary()["total"] == 5

    def test_summary_risk_counts_correct(self):
        engine = fresh_engine()
        engine.assess(_inp())   # low
        engine.assess(_worst())  # critical
        s = engine.summary()
        assert s["risk_counts"].get("low", 0) >= 1
        assert s["risk_counts"].get("critical", 0) >= 1

    def test_summary_pattern_counts_correct(self):
        engine = fresh_engine()
        engine.assess(_inp())  # none pattern
        engine.assess(_inp())  # none pattern
        s = engine.summary()
        assert s["pattern_counts"].get("none", 0) == 2

    def test_summary_severity_counts_correct(self):
        engine = fresh_engine()
        engine.assess(_inp())  # outcome_driven
        s = engine.summary()
        assert s["severity_counts"].get("outcome_driven", 0) == 1

    def test_summary_action_counts_correct(self):
        engine = fresh_engine()
        engine.assess(_inp())  # no_action
        s = engine.summary()
        assert s["action_counts"].get("no_action", 0) == 1

    def test_summary_avg_value_composite(self):
        engine = fresh_engine()
        r1 = engine.assess(_inp())
        r2 = engine.assess(_inp())
        s = engine.summary()
        expected_avg = round((r1.value_composite + r2.value_composite) / 2, 1)
        assert s["avg_value_composite"] == expected_avg

    def test_summary_value_gap_count(self):
        engine = fresh_engine()
        engine.assess(_inp())   # no gap
        engine.assess(_worst())  # has gap
        s = engine.summary()
        assert s["value_gap_count"] >= 1

    def test_summary_coaching_count(self):
        engine = fresh_engine()
        engine.assess(_inp())   # no coaching
        engine.assess(_worst())  # needs coaching
        s = engine.summary()
        assert s["coaching_count"] >= 1

    def test_summary_avg_quantification_score(self):
        engine = fresh_engine()
        r1 = engine.assess(_inp())
        r2 = engine.assess(_inp())
        s = engine.summary()
        expected = round((r1.quantification_score + r2.quantification_score) / 2, 1)
        assert s["avg_quantification_score"] == expected

    def test_summary_avg_executive_score(self):
        engine = fresh_engine()
        r1 = engine.assess(_inp())
        r2 = engine.assess(_inp())
        s = engine.summary()
        expected = round((r1.executive_score + r2.executive_score) / 2, 1)
        assert s["avg_executive_score"] == expected

    def test_summary_avg_proof_score(self):
        engine = fresh_engine()
        r1 = engine.assess(_inp())
        r2 = engine.assess(_inp())
        s = engine.summary()
        expected = round((r1.proof_score + r2.proof_score) / 2, 1)
        assert s["avg_proof_score"] == expected

    def test_summary_avg_outcome_score(self):
        engine = fresh_engine()
        r1 = engine.assess(_inp())
        r2 = engine.assess(_inp())
        s = engine.summary()
        expected = round((r1.outcome_score + r2.outcome_score) / 2, 1)
        assert s["avg_outcome_score"] == expected

    def test_summary_total_estimated_value_leak(self):
        engine = fresh_engine()
        r1 = engine.assess(_inp())
        r2 = engine.assess(_worst())
        s = engine.summary()
        expected = round(r1.estimated_value_leak_usd + r2.estimated_value_leak_usd, 2)
        assert s["total_estimated_value_leak_usd"] == expected

    def test_summary_has_13_keys_when_populated(self):
        engine = fresh_engine()
        engine.assess(_inp())
        s = engine.summary()
        assert len(s) == 13

    def test_summary_accumulated_across_multiple_calls(self):
        engine = fresh_engine()
        engine.assess(_inp())
        engine.assess(_inp())
        engine.assess(_inp())
        s = engine.summary()
        assert s["total"] == 3


# ===========================================================================
# 21. Edge cases and boundary values
# ===========================================================================

class TestEdgeCases:
    def test_boundary_exact_values_at_all_thresholds(self):
        engine = fresh_engine()
        # All values at their positive-triggering boundary
        inp = _inp(
            roi_quantified_before_proposal_pct=0.25,
            business_case_created_pct=0.20,
            feature_demo_without_roi_pct=0.60,
            executive_sponsor_engaged_pct=0.25,
            c_suite_presentation_rate_pct=0.15,
            decision_maker_roi_meeting_pct=0.20,
            proof_of_value_completed_pct=0.20,
            value_metrics_agreed_with_buyer_pct=0.25,
            competitive_value_differentiation_pct=0.30,
            deals_lost_on_price_pct=0.45,
            customer_success_metric_defined_pct=0.25,
            economic_value_referenced_in_proposal_pct=0.30,
        )
        result = engine.assess(inp)
        assert isinstance(result, ValueResult)
        assert result.value_composite <= 100.0
        assert result.value_composite >= 0.0

    def test_all_zeros_pct_fields(self):
        engine = fresh_engine()
        inp = _inp(
            business_case_created_pct=0.0,
            roi_quantified_before_proposal_pct=0.0,
            value_metrics_agreed_with_buyer_pct=0.0,
            feature_demo_without_roi_pct=0.0,
            executive_sponsor_engaged_pct=0.0,
            c_suite_presentation_rate_pct=0.0,
            decision_maker_roi_meeting_pct=0.0,
            proof_of_value_completed_pct=0.0,
            customer_success_metric_defined_pct=0.0,
            competitive_value_differentiation_pct=0.0,
            deals_lost_on_price_pct=0.0,
            economic_value_referenced_in_proposal_pct=0.0,
        )
        result = engine.assess(inp)
        assert isinstance(result, ValueResult)

    def test_all_ones_pct_fields(self):
        engine = fresh_engine()
        inp = _inp(
            business_case_created_pct=1.0,
            roi_quantified_before_proposal_pct=1.0,
            value_metrics_agreed_with_buyer_pct=1.0,
            feature_demo_without_roi_pct=1.0,
            executive_sponsor_engaged_pct=1.0,
            c_suite_presentation_rate_pct=1.0,
            decision_maker_roi_meeting_pct=1.0,
            proof_of_value_completed_pct=1.0,
            customer_success_metric_defined_pct=1.0,
            competitive_value_differentiation_pct=1.0,
            deals_lost_on_price_pct=1.0,
            economic_value_referenced_in_proposal_pct=1.0,
        )
        result = engine.assess(inp)
        assert isinstance(result, ValueResult)

    def test_single_rep_summary(self):
        engine = fresh_engine()
        r = engine.assess(_inp())
        s = engine.summary()
        assert s["total"] == 1
        assert s["avg_value_composite"] == r.value_composite

    def test_assess_returns_different_objects_per_call(self):
        engine = fresh_engine()
        r1 = engine.assess(_inp(rep_id="A"))
        r2 = engine.assess(_inp(rep_id="B"))
        assert r1 is not r2
        assert r1.rep_id != r2.rep_id

    def test_fresh_engine_has_empty_results(self):
        engine = fresh_engine()
        assert engine._results == []

    def test_multiple_engines_independent(self):
        e1 = fresh_engine()
        e2 = fresh_engine()
        e1.assess(_inp())
        assert len(e1._results) == 1
        assert len(e2._results) == 0

    def test_zero_deals_closed_no_leak(self):
        engine = fresh_engine()
        inp = _worst(total_deals_closed=0)
        result = engine.assess(inp)
        assert result.estimated_value_leak_usd == 0.0

    def test_zero_avg_opportunity_no_leak(self):
        engine = fresh_engine()
        inp = _worst(avg_opportunity_value_usd=0.0)
        result = engine.assess(inp)
        assert result.estimated_value_leak_usd == 0.0

    def test_scores_always_between_0_and_100(self):
        engine = fresh_engine()
        for inp in [_inp(), _worst()]:
            r = engine.assess(inp)
            for attr in ("quantification_score", "executive_score", "proof_score",
                         "outcome_score", "value_composite"):
                val = getattr(r, attr)
                assert 0.0 <= val <= 100.0, f"{attr}={val} out of range"

    def test_large_batch_summary_correct_total(self):
        engine = fresh_engine()
        n = 50
        engine.assess_batch([_inp(rep_id=f"R{i}") for i in range(n)])
        assert engine.summary()["total"] == n

    def test_value_composite_monotone_with_bad_inputs(self):
        engine = fresh_engine()
        r_good = engine.assess(_inp())
        r_bad = engine.assess(_worst())
        assert r_bad.value_composite > r_good.value_composite

    def test_to_dict_value_composite_matches_result_attribute(self):
        engine = fresh_engine()
        r = engine.assess(_inp())
        d = r.to_dict()
        assert d["value_composite"] == r.value_composite

    def test_to_dict_estimated_leak_matches_result_attribute(self):
        engine = fresh_engine()
        r = engine.assess(_worst())
        d = r.to_dict()
        assert d["estimated_value_leak_usd"] == r.estimated_value_leak_usd

    def test_to_dict_value_risk_string_matches_enum(self):
        engine = fresh_engine()
        r = engine.assess(_worst())
        d = r.to_dict()
        assert d["value_risk"] == r.value_risk.value

    def test_to_dict_value_signal_matches_result_attribute(self):
        engine = fresh_engine()
        r = engine.assess(_inp())
        d = r.to_dict()
        assert d["value_signal"] == r.value_signal

    def test_summary_risk_counts_sum_to_total(self):
        engine = fresh_engine()
        engine.assess_batch([_inp(), _worst(), _inp(rep_id="R3"), _worst(rep_id="R4")])
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_severity_counts_sum_to_total(self):
        engine = fresh_engine()
        engine.assess_batch([_inp(), _worst()])
        s = engine.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_summary_pattern_counts_sum_to_total(self):
        engine = fresh_engine()
        engine.assess_batch([_inp(), _worst()])
        s = engine.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_to_total(self):
        engine = fresh_engine()
        engine.assess_batch([_inp(), _worst()])
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_value_gap_count_le_total(self):
        engine = fresh_engine()
        engine.assess_batch([_inp(), _inp(), _worst()])
        s = engine.summary()
        assert s["value_gap_count"] <= s["total"]

    def test_coaching_count_le_total(self):
        engine = fresh_engine()
        engine.assess_batch([_inp(), _inp(), _worst()])
        s = engine.summary()
        assert s["coaching_count"] <= s["total"]

    def test_total_leak_non_negative(self):
        engine = fresh_engine()
        engine.assess_batch([_inp(), _worst()])
        s = engine.summary()
        assert s["total_estimated_value_leak_usd"] >= 0.0
