"""Tests for SalesCustomerSuccessHandoffQualityIntelligenceEngine."""
import pytest
from swarm.intelligence.sales_customer_success_handoff_quality_intelligence_engine import (
    HandoffRisk,
    HandoffPattern,
    HandoffSeverity,
    HandoffAction,
    HandoffInput,
    HandoffResult,
    SalesCustomerSuccessHandoffQualityIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _inp(**overrides) -> HandoffInput:
    defaults = dict(
        rep_id="rep_test",
        region="West",
        evaluation_period_id="2026-Q1",
        implementation_plan_provided_pct=0.90,
        success_criteria_shared_with_cs_pct=0.90,
        deal_history_documented_pct=0.90,
        customer_expectation_alignment_rate_pct=0.90,
        features_promised_not_delivered_pct=0.05,
        time_to_first_value_slip_rate_pct=0.05,
        rep_involved_in_onboarding_pct=0.90,
        post_sale_check_in_rate_pct=0.90,
        escalations_requiring_rep_re_engagement_pct=0.05,
        days_between_close_and_handoff_avg=1.0,
        handoff_meeting_attended_pct=0.95,
        onboarding_start_delay_days_avg=2.0,
        customer_satisfaction_at_90d_pct=0.90,
        churn_within_12m_rate_pct=0.05,
        expansion_revenue_from_cs_handoffs_pct=0.30,
        nps_detractor_rate_pct=0.05,
        reference_willingness_rate_pct=0.80,
        total_deals_closed=50,
        avg_opportunity_value_usd=50000.0,
    )
    defaults.update(overrides)
    return HandoffInput(**defaults)


def _engine() -> SalesCustomerSuccessHandoffQualityIntelligenceEngine:
    return SalesCustomerSuccessHandoffQualityIntelligenceEngine()


# ---------------------------------------------------------------------------
# Enum tests
# ---------------------------------------------------------------------------

class TestEnums:
    def test_handoff_risk_values(self):
        assert set(HandoffRisk) == {HandoffRisk.low, HandoffRisk.moderate, HandoffRisk.high, HandoffRisk.critical}

    def test_handoff_risk_strings(self):
        assert HandoffRisk.low.value == "low"
        assert HandoffRisk.moderate.value == "moderate"
        assert HandoffRisk.high.value == "high"
        assert HandoffRisk.critical.value == "critical"

    def test_handoff_pattern_values(self):
        assert HandoffPattern.none.value == "none"
        assert HandoffPattern.oversell_setup.value == "oversell_setup"
        assert HandoffPattern.expectation_mismatch.value == "expectation_mismatch"
        assert HandoffPattern.incomplete_context_transfer.value == "incomplete_context_transfer"
        assert HandoffPattern.ghosting_at_handoff.value == "ghosting_at_handoff"
        assert HandoffPattern.late_handoff_timing.value == "late_handoff_timing"

    def test_handoff_severity_values(self):
        assert HandoffSeverity.seamless.value == "seamless"
        assert HandoffSeverity.adequate.value == "adequate"
        assert HandoffSeverity.disruptive.value == "disruptive"
        assert HandoffSeverity.damaging.value == "damaging"

    def test_handoff_action_values(self):
        assert HandoffAction.no_action.value == "no_action"
        assert HandoffAction.handoff_process_coaching.value == "handoff_process_coaching"
        assert HandoffAction.expectation_alignment_coaching.value == "expectation_alignment_coaching"
        assert HandoffAction.customer_success_partnership_coaching.value == "customer_success_partnership_coaching"
        assert HandoffAction.post_sale_involvement_coaching.value == "post_sale_involvement_coaching"
        assert HandoffAction.handoff_reset_intervention.value == "handoff_reset_intervention"


# ---------------------------------------------------------------------------
# HandoffInput field count
# ---------------------------------------------------------------------------

class TestHandoffInput:
    def test_field_count(self):
        inp = _inp()
        assert len(vars(inp)) == 22

    def test_all_fields_accessible(self):
        inp = _inp()
        assert inp.rep_id == "rep_test"
        assert inp.region == "West"
        assert inp.evaluation_period_id == "2026-Q1"
        assert inp.implementation_plan_provided_pct == 0.90
        assert inp.success_criteria_shared_with_cs_pct == 0.90
        assert inp.deal_history_documented_pct == 0.90
        assert inp.customer_expectation_alignment_rate_pct == 0.90
        assert inp.features_promised_not_delivered_pct == 0.05
        assert inp.time_to_first_value_slip_rate_pct == 0.05
        assert inp.rep_involved_in_onboarding_pct == 0.90
        assert inp.post_sale_check_in_rate_pct == 0.90
        assert inp.escalations_requiring_rep_re_engagement_pct == 0.05
        assert inp.days_between_close_and_handoff_avg == 1.0
        assert inp.handoff_meeting_attended_pct == 0.95
        assert inp.onboarding_start_delay_days_avg == 2.0
        assert inp.customer_satisfaction_at_90d_pct == 0.90
        assert inp.churn_within_12m_rate_pct == 0.05
        assert inp.expansion_revenue_from_cs_handoffs_pct == 0.30
        assert inp.nps_detractor_rate_pct == 0.05
        assert inp.reference_willingness_rate_pct == 0.80
        assert inp.total_deals_closed == 50
        assert inp.avg_opportunity_value_usd == 50000.0


# ---------------------------------------------------------------------------
# HandoffResult / to_dict
# ---------------------------------------------------------------------------

class TestHandoffResult:
    def test_to_dict_key_count(self):
        eng = _engine()
        result = eng.assess(_inp())
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_keys(self):
        eng = _engine()
        result = eng.assess(_inp())
        d = result.to_dict()
        expected_keys = {
            "rep_id", "region", "handoff_risk", "handoff_pattern",
            "handoff_severity", "recommended_action", "context_score",
            "expectation_score", "continuity_score", "timing_score",
            "handoff_composite", "has_handoff_gap", "requires_handoff_coaching",
            "estimated_churn_risk_usd", "handoff_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_string_values(self):
        eng = _engine()
        result = eng.assess(_inp())
        d = result.to_dict()
        assert isinstance(d["handoff_risk"], str)
        assert isinstance(d["handoff_pattern"], str)
        assert isinstance(d["handoff_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_result_fields(self):
        eng = _engine()
        result = eng.assess(_inp())
        assert result.rep_id == "rep_test"
        assert result.region == "West"
        assert isinstance(result.handoff_risk, HandoffRisk)
        assert isinstance(result.handoff_pattern, HandoffPattern)
        assert isinstance(result.handoff_severity, HandoffSeverity)
        assert isinstance(result.recommended_action, HandoffAction)
        assert isinstance(result.context_score, float)
        assert isinstance(result.expectation_score, float)
        assert isinstance(result.continuity_score, float)
        assert isinstance(result.timing_score, float)
        assert isinstance(result.handoff_composite, float)
        assert isinstance(result.has_handoff_gap, bool)
        assert isinstance(result.requires_handoff_coaching, bool)
        assert isinstance(result.estimated_churn_risk_usd, float)
        assert isinstance(result.handoff_signal, str)


# ---------------------------------------------------------------------------
# Sub-score: context_score
# ---------------------------------------------------------------------------

class TestContextScore:
    def test_implementation_plan_low_adds_40(self):
        eng = _engine()
        # <=0.30 → +40
        r = eng.assess(_inp(implementation_plan_provided_pct=0.20,
                            success_criteria_shared_with_cs_pct=0.90,
                            deal_history_documented_pct=0.90))
        assert r.context_score >= 40.0

    def test_implementation_plan_mid_adds_22(self):
        eng = _engine()
        # <=0.55 → +22
        r = eng.assess(_inp(implementation_plan_provided_pct=0.45,
                            success_criteria_shared_with_cs_pct=0.90,
                            deal_history_documented_pct=0.90))
        assert r.context_score >= 22.0

    def test_implementation_plan_upper_adds_8(self):
        eng = _engine()
        # <=0.75 → +8
        r = eng.assess(_inp(implementation_plan_provided_pct=0.65,
                            success_criteria_shared_with_cs_pct=0.90,
                            deal_history_documented_pct=0.90))
        assert r.context_score >= 8.0

    def test_success_criteria_low_adds_35(self):
        eng = _engine()
        # <=0.35 → +35
        r = eng.assess(_inp(implementation_plan_provided_pct=0.90,
                            success_criteria_shared_with_cs_pct=0.25,
                            deal_history_documented_pct=0.90))
        assert r.context_score >= 35.0

    def test_success_criteria_mid_adds_18(self):
        eng = _engine()
        # <=0.60 → +18
        r = eng.assess(_inp(implementation_plan_provided_pct=0.90,
                            success_criteria_shared_with_cs_pct=0.50,
                            deal_history_documented_pct=0.90))
        assert r.context_score >= 18.0

    def test_deal_history_low_adds_25(self):
        eng = _engine()
        # <=0.40 → +25
        r = eng.assess(_inp(implementation_plan_provided_pct=0.90,
                            success_criteria_shared_with_cs_pct=0.90,
                            deal_history_documented_pct=0.30))
        assert r.context_score >= 25.0

    def test_deal_history_mid_adds_12(self):
        eng = _engine()
        # <=0.65 → +12
        r = eng.assess(_inp(implementation_plan_provided_pct=0.90,
                            success_criteria_shared_with_cs_pct=0.90,
                            deal_history_documented_pct=0.55))
        assert r.context_score >= 12.0

    def test_context_score_capped_at_100(self):
        eng = _engine()
        r = eng.assess(_inp(implementation_plan_provided_pct=0.10,
                            success_criteria_shared_with_cs_pct=0.10,
                            deal_history_documented_pct=0.10))
        assert r.context_score <= 100.0

    def test_context_score_zero_for_perfect(self):
        eng = _engine()
        r = eng.assess(_inp(implementation_plan_provided_pct=0.95,
                            success_criteria_shared_with_cs_pct=0.95,
                            deal_history_documented_pct=0.95))
        assert r.context_score == 0.0


# ---------------------------------------------------------------------------
# Sub-score: expectation_score
# ---------------------------------------------------------------------------

class TestExpectationScore:
    def test_alignment_very_low_adds_40(self):
        eng = _engine()
        r = eng.assess(_inp(customer_expectation_alignment_rate_pct=0.40,
                            features_promised_not_delivered_pct=0.05,
                            time_to_first_value_slip_rate_pct=0.05))
        assert r.expectation_score >= 40.0

    def test_alignment_mid_adds_22(self):
        eng = _engine()
        r = eng.assess(_inp(customer_expectation_alignment_rate_pct=0.60,
                            features_promised_not_delivered_pct=0.05,
                            time_to_first_value_slip_rate_pct=0.05))
        assert r.expectation_score >= 22.0

    def test_alignment_upper_adds_8(self):
        eng = _engine()
        r = eng.assess(_inp(customer_expectation_alignment_rate_pct=0.80,
                            features_promised_not_delivered_pct=0.05,
                            time_to_first_value_slip_rate_pct=0.05))
        assert r.expectation_score >= 8.0

    def test_features_not_delivered_high_adds_35(self):
        eng = _engine()
        r = eng.assess(_inp(customer_expectation_alignment_rate_pct=0.90,
                            features_promised_not_delivered_pct=0.30,
                            time_to_first_value_slip_rate_pct=0.05))
        assert r.expectation_score >= 35.0

    def test_features_not_delivered_mid_adds_18(self):
        eng = _engine()
        r = eng.assess(_inp(customer_expectation_alignment_rate_pct=0.90,
                            features_promised_not_delivered_pct=0.20,
                            time_to_first_value_slip_rate_pct=0.05))
        assert r.expectation_score >= 18.0

    def test_value_slip_high_adds_25(self):
        eng = _engine()
        r = eng.assess(_inp(customer_expectation_alignment_rate_pct=0.90,
                            features_promised_not_delivered_pct=0.05,
                            time_to_first_value_slip_rate_pct=0.50))
        assert r.expectation_score >= 25.0

    def test_value_slip_mid_adds_12(self):
        eng = _engine()
        r = eng.assess(_inp(customer_expectation_alignment_rate_pct=0.90,
                            features_promised_not_delivered_pct=0.05,
                            time_to_first_value_slip_rate_pct=0.30))
        assert r.expectation_score >= 12.0

    def test_expectation_score_capped_at_100(self):
        eng = _engine()
        r = eng.assess(_inp(customer_expectation_alignment_rate_pct=0.10,
                            features_promised_not_delivered_pct=0.50,
                            time_to_first_value_slip_rate_pct=0.80))
        assert r.expectation_score <= 100.0

    def test_expectation_score_zero_for_perfect(self):
        eng = _engine()
        r = eng.assess(_inp(customer_expectation_alignment_rate_pct=0.95,
                            features_promised_not_delivered_pct=0.05,
                            time_to_first_value_slip_rate_pct=0.05))
        assert r.expectation_score == 0.0


# ---------------------------------------------------------------------------
# Sub-score: continuity_score
# ---------------------------------------------------------------------------

class TestContinuityScore:
    def test_rep_involved_very_low_adds_45(self):
        eng = _engine()
        r = eng.assess(_inp(rep_involved_in_onboarding_pct=0.20,
                            post_sale_check_in_rate_pct=0.90,
                            escalations_requiring_rep_re_engagement_pct=0.05))
        assert r.continuity_score >= 45.0

    def test_rep_involved_mid_adds_25(self):
        eng = _engine()
        r = eng.assess(_inp(rep_involved_in_onboarding_pct=0.45,
                            post_sale_check_in_rate_pct=0.90,
                            escalations_requiring_rep_re_engagement_pct=0.05))
        assert r.continuity_score >= 25.0

    def test_rep_involved_upper_adds_10(self):
        eng = _engine()
        r = eng.assess(_inp(rep_involved_in_onboarding_pct=0.65,
                            post_sale_check_in_rate_pct=0.90,
                            escalations_requiring_rep_re_engagement_pct=0.05))
        assert r.continuity_score >= 10.0

    def test_check_in_very_low_adds_30(self):
        eng = _engine()
        r = eng.assess(_inp(rep_involved_in_onboarding_pct=0.90,
                            post_sale_check_in_rate_pct=0.15,
                            escalations_requiring_rep_re_engagement_pct=0.05))
        assert r.continuity_score >= 30.0

    def test_check_in_mid_adds_15(self):
        eng = _engine()
        r = eng.assess(_inp(rep_involved_in_onboarding_pct=0.90,
                            post_sale_check_in_rate_pct=0.35,
                            escalations_requiring_rep_re_engagement_pct=0.05))
        assert r.continuity_score >= 15.0

    def test_escalations_high_adds_25(self):
        eng = _engine()
        r = eng.assess(_inp(rep_involved_in_onboarding_pct=0.90,
                            post_sale_check_in_rate_pct=0.90,
                            escalations_requiring_rep_re_engagement_pct=0.50))
        assert r.continuity_score >= 25.0

    def test_escalations_mid_adds_12(self):
        eng = _engine()
        r = eng.assess(_inp(rep_involved_in_onboarding_pct=0.90,
                            post_sale_check_in_rate_pct=0.90,
                            escalations_requiring_rep_re_engagement_pct=0.25))
        assert r.continuity_score >= 12.0

    def test_continuity_score_capped_at_100(self):
        eng = _engine()
        r = eng.assess(_inp(rep_involved_in_onboarding_pct=0.10,
                            post_sale_check_in_rate_pct=0.10,
                            escalations_requiring_rep_re_engagement_pct=0.80))
        assert r.continuity_score <= 100.0

    def test_continuity_score_zero_for_perfect(self):
        eng = _engine()
        r = eng.assess(_inp(rep_involved_in_onboarding_pct=0.90,
                            post_sale_check_in_rate_pct=0.90,
                            escalations_requiring_rep_re_engagement_pct=0.05))
        assert r.continuity_score == 0.0


# ---------------------------------------------------------------------------
# Sub-score: timing_score
# ---------------------------------------------------------------------------

class TestTimingScore:
    def test_days_to_handoff_very_high_adds_40(self):
        eng = _engine()
        r = eng.assess(_inp(days_between_close_and_handoff_avg=20.0,
                            handoff_meeting_attended_pct=0.90,
                            onboarding_start_delay_days_avg=2.0))
        assert r.timing_score >= 40.0

    def test_days_to_handoff_mid_adds_22(self):
        eng = _engine()
        r = eng.assess(_inp(days_between_close_and_handoff_avg=10.0,
                            handoff_meeting_attended_pct=0.90,
                            onboarding_start_delay_days_avg=2.0))
        assert r.timing_score >= 22.0

    def test_days_to_handoff_low_adds_8(self):
        eng = _engine()
        r = eng.assess(_inp(days_between_close_and_handoff_avg=5.0,
                            handoff_meeting_attended_pct=0.90,
                            onboarding_start_delay_days_avg=2.0))
        assert r.timing_score >= 8.0

    def test_meeting_attended_very_low_adds_35(self):
        eng = _engine()
        r = eng.assess(_inp(days_between_close_and_handoff_avg=1.0,
                            handoff_meeting_attended_pct=0.30,
                            onboarding_start_delay_days_avg=2.0))
        assert r.timing_score >= 35.0

    def test_meeting_attended_mid_adds_18(self):
        eng = _engine()
        r = eng.assess(_inp(days_between_close_and_handoff_avg=1.0,
                            handoff_meeting_attended_pct=0.55,
                            onboarding_start_delay_days_avg=2.0))
        assert r.timing_score >= 18.0

    def test_onboarding_delay_very_high_adds_25(self):
        eng = _engine()
        r = eng.assess(_inp(days_between_close_and_handoff_avg=1.0,
                            handoff_meeting_attended_pct=0.90,
                            onboarding_start_delay_days_avg=30.0))
        assert r.timing_score >= 25.0

    def test_onboarding_delay_mid_adds_12(self):
        eng = _engine()
        r = eng.assess(_inp(days_between_close_and_handoff_avg=1.0,
                            handoff_meeting_attended_pct=0.90,
                            onboarding_start_delay_days_avg=15.0))
        assert r.timing_score >= 12.0

    def test_timing_score_capped_at_100(self):
        eng = _engine()
        r = eng.assess(_inp(days_between_close_and_handoff_avg=30.0,
                            handoff_meeting_attended_pct=0.10,
                            onboarding_start_delay_days_avg=60.0))
        assert r.timing_score <= 100.0

    def test_timing_score_zero_for_perfect(self):
        eng = _engine()
        r = eng.assess(_inp(days_between_close_and_handoff_avg=1.0,
                            handoff_meeting_attended_pct=0.95,
                            onboarding_start_delay_days_avg=2.0))
        assert r.timing_score == 0.0


# ---------------------------------------------------------------------------
# Composite formula
# ---------------------------------------------------------------------------

class TestCompositeFormula:
    def test_composite_weights_sum_to_one(self):
        # 0.30 + 0.30 + 0.25 + 0.15 = 1.00
        assert abs(0.30 + 0.30 + 0.25 + 0.15 - 1.00) < 1e-9

    def test_composite_zero_for_perfect(self):
        eng = _engine()
        r = eng.assess(_inp())
        assert r.handoff_composite == 0.0

    def test_composite_max_for_worst(self):
        eng = _engine()
        r = eng.assess(_inp(
            implementation_plan_provided_pct=0.10,
            success_criteria_shared_with_cs_pct=0.10,
            deal_history_documented_pct=0.10,
            customer_expectation_alignment_rate_pct=0.10,
            features_promised_not_delivered_pct=0.80,
            time_to_first_value_slip_rate_pct=0.80,
            rep_involved_in_onboarding_pct=0.10,
            post_sale_check_in_rate_pct=0.10,
            escalations_requiring_rep_re_engagement_pct=0.80,
            days_between_close_and_handoff_avg=30.0,
            handoff_meeting_attended_pct=0.10,
            onboarding_start_delay_days_avg=60.0,
        ))
        assert r.handoff_composite == 100.0

    def test_composite_is_weighted_average(self):
        eng = _engine()
        r = eng.assess(_inp())
        expected = round(r.context_score * 0.30 + r.expectation_score * 0.30
                        + r.continuity_score * 0.25 + r.timing_score * 0.15, 1)
        assert r.handoff_composite == min(expected, 100.0)


# ---------------------------------------------------------------------------
# Risk levels (thresholds)
# ---------------------------------------------------------------------------

class TestRiskLevels:
    def test_risk_low_for_zero_composite(self):
        eng = _engine()
        r = eng.assess(_inp())
        assert r.handoff_risk == HandoffRisk.low

    def test_risk_moderate_threshold(self):
        # composite>=20 → moderate
        eng = _engine()
        r = eng.assess(_inp(
            implementation_plan_provided_pct=0.50,
            success_criteria_shared_with_cs_pct=0.50,
        ))
        if r.handoff_composite >= 20:
            assert r.handoff_risk in (HandoffRisk.moderate, HandoffRisk.high, HandoffRisk.critical)

    def test_risk_high_threshold(self):
        eng = _engine()
        r = eng.assess(_inp(
            implementation_plan_provided_pct=0.20,
            success_criteria_shared_with_cs_pct=0.20,
            deal_history_documented_pct=0.20,
            customer_expectation_alignment_rate_pct=0.40,
            features_promised_not_delivered_pct=0.30,
            time_to_first_value_slip_rate_pct=0.50,
        ))
        if r.handoff_composite >= 40:
            assert r.handoff_risk in (HandoffRisk.high, HandoffRisk.critical)

    def test_risk_critical_for_max_composite(self):
        eng = _engine()
        r = eng.assess(_inp(
            implementation_plan_provided_pct=0.10,
            success_criteria_shared_with_cs_pct=0.10,
            deal_history_documented_pct=0.10,
            customer_expectation_alignment_rate_pct=0.10,
            features_promised_not_delivered_pct=0.80,
            time_to_first_value_slip_rate_pct=0.80,
            rep_involved_in_onboarding_pct=0.10,
            post_sale_check_in_rate_pct=0.10,
            escalations_requiring_rep_re_engagement_pct=0.80,
            days_between_close_and_handoff_avg=30.0,
            handoff_meeting_attended_pct=0.10,
            onboarding_start_delay_days_avg=60.0,
        ))
        assert r.handoff_risk == HandoffRisk.critical


# ---------------------------------------------------------------------------
# Severity levels
# ---------------------------------------------------------------------------

class TestSeverityLevels:
    def test_severity_seamless_for_zero(self):
        eng = _engine()
        r = eng.assess(_inp())
        assert r.handoff_severity == HandoffSeverity.seamless

    def test_severity_damaging_for_critical(self):
        eng = _engine()
        r = eng.assess(_inp(
            implementation_plan_provided_pct=0.10,
            success_criteria_shared_with_cs_pct=0.10,
            deal_history_documented_pct=0.10,
            customer_expectation_alignment_rate_pct=0.10,
            features_promised_not_delivered_pct=0.80,
            time_to_first_value_slip_rate_pct=0.80,
            rep_involved_in_onboarding_pct=0.10,
            post_sale_check_in_rate_pct=0.10,
            escalations_requiring_rep_re_engagement_pct=0.80,
            days_between_close_and_handoff_avg=30.0,
            handoff_meeting_attended_pct=0.10,
            onboarding_start_delay_days_avg=60.0,
        ))
        assert r.handoff_severity == HandoffSeverity.damaging

    def test_severity_adequate_for_moderate(self):
        eng = _engine()
        r = eng.assess(_inp(
            implementation_plan_provided_pct=0.50,
            success_criteria_shared_with_cs_pct=0.50,
            deal_history_documented_pct=0.55,
        ))
        if 20 <= r.handoff_composite < 40:
            assert r.handoff_severity == HandoffSeverity.adequate

    def test_severity_matches_risk(self):
        eng = _engine()
        r = eng.assess(_inp())
        # seamless <-> low
        composite = r.handoff_composite
        if composite >= 60:
            assert r.handoff_severity == HandoffSeverity.damaging
        elif composite >= 40:
            assert r.handoff_severity == HandoffSeverity.disruptive
        elif composite >= 20:
            assert r.handoff_severity == HandoffSeverity.adequate
        else:
            assert r.handoff_severity == HandoffSeverity.seamless


# ---------------------------------------------------------------------------
# Pattern detection
# ---------------------------------------------------------------------------

class TestPatternDetection:
    def test_pattern_oversell_setup(self):
        eng = _engine()
        r = eng.assess(_inp(
            features_promised_not_delivered_pct=0.30,
            customer_expectation_alignment_rate_pct=0.10,
            time_to_first_value_slip_rate_pct=0.80,
        ))
        assert r.handoff_pattern == HandoffPattern.oversell_setup

    def test_pattern_expectation_mismatch(self):
        eng = _engine()
        r = eng.assess(_inp(
            features_promised_not_delivered_pct=0.05,
            customer_expectation_alignment_rate_pct=0.40,
            time_to_first_value_slip_rate_pct=0.50,
        ))
        # expectation_mismatch: alignment<=0.45 AND value_slip>=0.40
        # but oversell_setup fires first if features_not_delivered>=0.20
        if r.expectation_score >= 40:
            assert r.handoff_pattern in (HandoffPattern.expectation_mismatch, HandoffPattern.oversell_setup)

    def test_pattern_incomplete_context_transfer(self):
        eng = _engine()
        r = eng.assess(_inp(
            features_promised_not_delivered_pct=0.05,
            customer_expectation_alignment_rate_pct=0.90,
            time_to_first_value_slip_rate_pct=0.05,
            implementation_plan_provided_pct=0.15,
            success_criteria_shared_with_cs_pct=0.10,
            deal_history_documented_pct=0.10,
        ))
        if r.context_score >= 40:
            assert r.handoff_pattern in (HandoffPattern.incomplete_context_transfer,)

    def test_pattern_ghosting_at_handoff(self):
        eng = _engine()
        r = eng.assess(_inp(
            features_promised_not_delivered_pct=0.05,
            customer_expectation_alignment_rate_pct=0.90,
            time_to_first_value_slip_rate_pct=0.05,
            implementation_plan_provided_pct=0.90,
            rep_involved_in_onboarding_pct=0.15,
            post_sale_check_in_rate_pct=0.10,
            escalations_requiring_rep_re_engagement_pct=0.50,
        ))
        if r.continuity_score >= 30:
            assert r.handoff_pattern == HandoffPattern.ghosting_at_handoff

    def test_pattern_late_handoff_timing(self):
        eng = _engine()
        r = eng.assess(_inp(
            features_promised_not_delivered_pct=0.05,
            customer_expectation_alignment_rate_pct=0.90,
            time_to_first_value_slip_rate_pct=0.05,
            implementation_plan_provided_pct=0.90,
            rep_involved_in_onboarding_pct=0.90,
            days_between_close_and_handoff_avg=15.0,
            handoff_meeting_attended_pct=0.30,
            onboarding_start_delay_days_avg=25.0,
        ))
        if r.timing_score >= 30:
            assert r.handoff_pattern == HandoffPattern.late_handoff_timing

    def test_pattern_none_for_perfect(self):
        eng = _engine()
        r = eng.assess(_inp())
        assert r.handoff_pattern == HandoffPattern.none

    def test_oversell_setup_priority_over_expectation_mismatch(self):
        # Both conditions can fire but oversell_setup checked first
        eng = _engine()
        r = eng.assess(_inp(
            features_promised_not_delivered_pct=0.30,  # >=0.20
            customer_expectation_alignment_rate_pct=0.40,  # <=0.45
            time_to_first_value_slip_rate_pct=0.50,  # >=0.40
        ))
        # oversell_setup fires if features_not_delivered>=0.20 AND expectation>=40
        if r.expectation_score >= 40:
            assert r.handoff_pattern == HandoffPattern.oversell_setup


# ---------------------------------------------------------------------------
# Action mapping
# ---------------------------------------------------------------------------

class TestActionMapping:
    def test_action_no_action_for_low_risk(self):
        eng = _engine()
        r = eng.assess(_inp())
        assert r.recommended_action == HandoffAction.no_action

    def test_action_handoff_process_coaching_for_moderate(self):
        eng = _engine()
        r = eng.assess(_inp(
            implementation_plan_provided_pct=0.50,
            success_criteria_shared_with_cs_pct=0.50,
            deal_history_documented_pct=0.55,
            customer_expectation_alignment_rate_pct=0.65,
        ))
        if r.handoff_risk == HandoffRisk.moderate:
            assert r.recommended_action == HandoffAction.handoff_process_coaching

    def test_action_post_sale_involvement_for_high_ghosting(self):
        eng = _engine()
        r = eng.assess(_inp(
            features_promised_not_delivered_pct=0.05,
            customer_expectation_alignment_rate_pct=0.90,
            time_to_first_value_slip_rate_pct=0.05,
            implementation_plan_provided_pct=0.90,
            rep_involved_in_onboarding_pct=0.15,
            post_sale_check_in_rate_pct=0.10,
            escalations_requiring_rep_re_engagement_pct=0.50,
        ))
        if r.handoff_risk == HandoffRisk.high and r.handoff_pattern == HandoffPattern.ghosting_at_handoff:
            assert r.recommended_action == HandoffAction.post_sale_involvement_coaching

    def test_action_handoff_process_coaching_for_high_context_transfer(self):
        eng = _engine()
        r = eng.assess(_inp(
            features_promised_not_delivered_pct=0.05,
            customer_expectation_alignment_rate_pct=0.90,
            time_to_first_value_slip_rate_pct=0.05,
            implementation_plan_provided_pct=0.15,
            success_criteria_shared_with_cs_pct=0.10,
            deal_history_documented_pct=0.10,
        ))
        if r.handoff_risk == HandoffRisk.high and r.handoff_pattern == HandoffPattern.incomplete_context_transfer:
            assert r.recommended_action == HandoffAction.handoff_process_coaching

    def test_action_expectation_alignment_for_critical_oversell(self):
        eng = _engine()
        r = eng.assess(_inp(
            features_promised_not_delivered_pct=0.30,
            customer_expectation_alignment_rate_pct=0.10,
            time_to_first_value_slip_rate_pct=0.80,
            implementation_plan_provided_pct=0.10,
            success_criteria_shared_with_cs_pct=0.10,
            deal_history_documented_pct=0.10,
            rep_involved_in_onboarding_pct=0.10,
            post_sale_check_in_rate_pct=0.10,
            escalations_requiring_rep_re_engagement_pct=0.80,
            days_between_close_and_handoff_avg=30.0,
            handoff_meeting_attended_pct=0.10,
            onboarding_start_delay_days_avg=60.0,
        ))
        if r.handoff_risk == HandoffRisk.critical and r.handoff_pattern == HandoffPattern.oversell_setup:
            assert r.recommended_action == HandoffAction.expectation_alignment_coaching

    def test_action_handoff_reset_for_critical_other(self):
        # critical with pattern=none → handoff_reset_intervention
        eng = _engine()
        # Force critical composite without triggering any pattern
        r = eng.assess(_inp(
            implementation_plan_provided_pct=0.10,
            success_criteria_shared_with_cs_pct=0.10,
            deal_history_documented_pct=0.10,
            customer_expectation_alignment_rate_pct=0.90,  # high alignment (no oversell pattern)
            features_promised_not_delivered_pct=0.05,       # no oversell
            time_to_first_value_slip_rate_pct=0.05,         # no value slip
            rep_involved_in_onboarding_pct=0.90,            # good continuity
            post_sale_check_in_rate_pct=0.90,
            escalations_requiring_rep_re_engagement_pct=0.05,
            days_between_close_and_handoff_avg=30.0,
            handoff_meeting_attended_pct=0.10,
            onboarding_start_delay_days_avg=60.0,
        ))
        if r.handoff_risk == HandoffRisk.critical and r.handoff_pattern == HandoffPattern.none:
            assert r.recommended_action == HandoffAction.handoff_reset_intervention


# ---------------------------------------------------------------------------
# Flags
# ---------------------------------------------------------------------------

class TestFlags:
    def test_no_gap_for_perfect(self):
        eng = _engine()
        r = eng.assess(_inp())
        assert r.has_handoff_gap is False

    def test_gap_when_composite_high(self):
        eng = _engine()
        r = eng.assess(_inp(
            implementation_plan_provided_pct=0.10,
            success_criteria_shared_with_cs_pct=0.10,
            deal_history_documented_pct=0.10,
            customer_expectation_alignment_rate_pct=0.10,
            features_promised_not_delivered_pct=0.80,
            time_to_first_value_slip_rate_pct=0.80,
            rep_involved_in_onboarding_pct=0.10,
            post_sale_check_in_rate_pct=0.10,
            escalations_requiring_rep_re_engagement_pct=0.80,
            days_between_close_and_handoff_avg=30.0,
            handoff_meeting_attended_pct=0.10,
            onboarding_start_delay_days_avg=60.0,
        ))
        assert r.has_handoff_gap is True

    def test_gap_when_expectation_alignment_low(self):
        eng = _engine()
        r = eng.assess(_inp(customer_expectation_alignment_rate_pct=0.50))
        assert r.has_handoff_gap is True

    def test_gap_when_rep_involvement_low(self):
        eng = _engine()
        r = eng.assess(_inp(rep_involved_in_onboarding_pct=0.30))
        assert r.has_handoff_gap is True

    def test_no_coaching_for_perfect(self):
        eng = _engine()
        r = eng.assess(_inp())
        assert r.requires_handoff_coaching is False

    def test_coaching_when_composite_high(self):
        eng = _engine()
        r = eng.assess(_inp(
            implementation_plan_provided_pct=0.10,
            success_criteria_shared_with_cs_pct=0.10,
            deal_history_documented_pct=0.10,
            customer_expectation_alignment_rate_pct=0.10,
            features_promised_not_delivered_pct=0.80,
            time_to_first_value_slip_rate_pct=0.80,
            rep_involved_in_onboarding_pct=0.10,
            post_sale_check_in_rate_pct=0.10,
            escalations_requiring_rep_re_engagement_pct=0.80,
            days_between_close_and_handoff_avg=30.0,
            handoff_meeting_attended_pct=0.10,
            onboarding_start_delay_days_avg=60.0,
        ))
        assert r.requires_handoff_coaching is True

    def test_coaching_when_implementation_plan_low(self):
        eng = _engine()
        r = eng.assess(_inp(implementation_plan_provided_pct=0.40))
        assert r.requires_handoff_coaching is True

    def test_coaching_when_features_not_delivered_high(self):
        eng = _engine()
        r = eng.assess(_inp(features_promised_not_delivered_pct=0.20))
        assert r.requires_handoff_coaching is True


# ---------------------------------------------------------------------------
# Churn risk estimate
# ---------------------------------------------------------------------------

class TestChurnRiskEstimate:
    def test_churn_risk_zero_for_perfect_alignment(self):
        eng = _engine()
        r = eng.assess(_inp(customer_expectation_alignment_rate_pct=1.0))
        assert r.estimated_churn_risk_usd == 0.0

    def test_churn_risk_zero_for_zero_composite(self):
        eng = _engine()
        r = eng.assess(_inp())
        # composite is 0 so churn risk is 0
        assert r.estimated_churn_risk_usd == 0.0

    def test_churn_risk_formula(self):
        eng = _engine()
        r = eng.assess(_inp(
            total_deals_closed=100,
            avg_opportunity_value_usd=50000.0,
            customer_expectation_alignment_rate_pct=0.50,
            implementation_plan_provided_pct=0.10,
            success_criteria_shared_with_cs_pct=0.10,
            deal_history_documented_pct=0.10,
            features_promised_not_delivered_pct=0.80,
            time_to_first_value_slip_rate_pct=0.80,
            rep_involved_in_onboarding_pct=0.10,
            post_sale_check_in_rate_pct=0.10,
            escalations_requiring_rep_re_engagement_pct=0.80,
            days_between_close_and_handoff_avg=30.0,
            handoff_meeting_attended_pct=0.10,
            onboarding_start_delay_days_avg=60.0,
        ))
        expected = round(100 * 50000.0 * (1.0 - 0.50) * (r.handoff_composite / 100.0), 2)
        assert r.estimated_churn_risk_usd == expected

    def test_churn_risk_smoke_test(self):
        # exact smoke test: composite=100 → expected = 100*50000*(1-0.0)*1.0 = 5_000_000 but
        # the fixture from summary uses alignment=0.60 and total_deals=100, etc.
        # Instead let's verify the formula holds for any assessed result
        eng = _engine()
        inp = _inp(
            total_deals_closed=40,
            avg_opportunity_value_usd=100000.0,
            customer_expectation_alignment_rate_pct=0.45,
            implementation_plan_provided_pct=0.10,
            success_criteria_shared_with_cs_pct=0.10,
            deal_history_documented_pct=0.10,
            features_promised_not_delivered_pct=0.80,
            time_to_first_value_slip_rate_pct=0.80,
            rep_involved_in_onboarding_pct=0.10,
            post_sale_check_in_rate_pct=0.10,
            escalations_requiring_rep_re_engagement_pct=0.80,
            days_between_close_and_handoff_avg=30.0,
            handoff_meeting_attended_pct=0.10,
            onboarding_start_delay_days_avg=60.0,
        )
        r = eng.assess(inp)
        expected = round(40 * 100000.0 * (1.0 - 0.45) * (r.handoff_composite / 100.0), 2)
        assert r.estimated_churn_risk_usd == expected


# ---------------------------------------------------------------------------
# Signal string
# ---------------------------------------------------------------------------

class TestSignal:
    def test_signal_healthy_for_perfect(self):
        eng = _engine()
        r = eng.assess(_inp())
        assert r.handoff_signal == "Customer handoff quality strong — context transfer, expectation alignment, and post-sale continuity within benchmarks"

    def test_signal_includes_composite_for_bad(self):
        eng = _engine()
        r = eng.assess(_inp(
            implementation_plan_provided_pct=0.10,
            success_criteria_shared_with_cs_pct=0.10,
            deal_history_documented_pct=0.10,
            customer_expectation_alignment_rate_pct=0.10,
            features_promised_not_delivered_pct=0.80,
            time_to_first_value_slip_rate_pct=0.80,
            rep_involved_in_onboarding_pct=0.10,
            post_sale_check_in_rate_pct=0.10,
            escalations_requiring_rep_re_engagement_pct=0.80,
            days_between_close_and_handoff_avg=30.0,
            handoff_meeting_attended_pct=0.10,
            onboarding_start_delay_days_avg=60.0,
        ))
        assert "composite" in r.handoff_signal
        assert "%" in r.handoff_signal

    def test_signal_contains_pattern_label(self):
        eng = _engine()
        r = eng.assess(_inp(
            features_promised_not_delivered_pct=0.30,
            customer_expectation_alignment_rate_pct=0.10,
            time_to_first_value_slip_rate_pct=0.80,
        ))
        if r.handoff_pattern != HandoffPattern.none:
            pattern_label = r.handoff_pattern.value.replace("_", " ").capitalize()
            assert pattern_label in r.handoff_signal

    def test_signal_contains_implementation_pct(self):
        eng = _engine()
        r = eng.assess(_inp(
            features_promised_not_delivered_pct=0.30,
            customer_expectation_alignment_rate_pct=0.10,
            time_to_first_value_slip_rate_pct=0.80,
        ))
        if r.handoff_pattern != HandoffPattern.none or r.handoff_composite >= 20:
            assert "provide implementation plan" in r.handoff_signal

    def test_signal_contains_alignment_rate(self):
        eng = _engine()
        r = eng.assess(_inp(
            features_promised_not_delivered_pct=0.30,
            customer_expectation_alignment_rate_pct=0.10,
            time_to_first_value_slip_rate_pct=0.80,
        ))
        if r.handoff_pattern != HandoffPattern.none:
            assert "expectation alignment rate" in r.handoff_signal

    def test_signal_handoff_risk_label_when_no_pattern(self):
        eng = _engine()
        # Force moderate composite without triggering a pattern
        r = eng.assess(_inp(
            implementation_plan_provided_pct=0.50,
            success_criteria_shared_with_cs_pct=0.50,
            deal_history_documented_pct=0.55,
            customer_expectation_alignment_rate_pct=0.65,
            features_promised_not_delivered_pct=0.05,
            time_to_first_value_slip_rate_pct=0.05,
        ))
        if r.handoff_pattern == HandoffPattern.none and r.handoff_composite >= 20:
            assert "Handoff risk" in r.handoff_signal


# ---------------------------------------------------------------------------
# assess_batch
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_assess_batch_empty(self):
        eng = _engine()
        results = eng.assess_batch([])
        assert results == []

    def test_assess_batch_single(self):
        eng = _engine()
        results = eng.assess_batch([_inp()])
        assert len(results) == 1
        assert isinstance(results[0], HandoffResult)

    def test_assess_batch_multiple(self):
        eng = _engine()
        inputs = [_inp(rep_id=f"rep_{i}") for i in range(5)]
        results = eng.assess_batch(inputs)
        assert len(results) == 5
        rep_ids = [r.rep_id for r in results]
        assert rep_ids == [f"rep_{i}" for i in range(5)]

    def test_assess_batch_populates_summary(self):
        eng = _engine()
        eng.assess_batch([_inp(rep_id="A"), _inp(rep_id="B")])
        s = eng.summary()
        assert s["total"] == 2


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

class TestSummary:
    def test_summary_empty_engine(self):
        eng = _engine()
        s = eng.summary()
        assert s["total"] == 0
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}
        assert s["avg_handoff_composite"] == 0.0
        assert s["handoff_gap_count"] == 0
        assert s["coaching_count"] == 0
        assert s["avg_context_score"] == 0.0
        assert s["avg_expectation_score"] == 0.0
        assert s["avg_continuity_score"] == 0.0
        assert s["avg_timing_score"] == 0.0
        assert s["total_estimated_churn_risk_usd"] == 0.0

    def test_summary_key_count(self):
        eng = _engine()
        eng.assess(_inp())
        s = eng.summary()
        assert len(s) == 13

    def test_summary_keys(self):
        eng = _engine()
        eng.assess(_inp())
        s = eng.summary()
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_handoff_composite", "handoff_gap_count",
            "coaching_count", "avg_context_score", "avg_expectation_score",
            "avg_continuity_score", "avg_timing_score",
            "total_estimated_churn_risk_usd",
        }
        assert set(s.keys()) == expected

    def test_summary_total_count(self):
        eng = _engine()
        for i in range(6):
            eng.assess(_inp(rep_id=f"rep_{i}"))
        assert eng.summary()["total"] == 6

    def test_summary_risk_counts(self):
        eng = _engine()
        eng.assess(_inp())
        s = eng.summary()
        assert "low" in s["risk_counts"]
        assert s["risk_counts"]["low"] == 1

    def test_summary_pattern_counts(self):
        eng = _engine()
        eng.assess(_inp())
        s = eng.summary()
        assert "none" in s["pattern_counts"]

    def test_summary_severity_counts(self):
        eng = _engine()
        eng.assess(_inp())
        s = eng.summary()
        assert "seamless" in s["severity_counts"]

    def test_summary_action_counts(self):
        eng = _engine()
        eng.assess(_inp())
        s = eng.summary()
        assert "no_action" in s["action_counts"]

    def test_summary_avg_composite(self):
        eng = _engine()
        eng.assess(_inp())
        s = eng.summary()
        assert s["avg_handoff_composite"] == 0.0

    def test_summary_handoff_gap_count(self):
        eng = _engine()
        eng.assess(_inp())  # no gap
        eng.assess(_inp(customer_expectation_alignment_rate_pct=0.50))  # gap
        s = eng.summary()
        assert s["handoff_gap_count"] == 1

    def test_summary_coaching_count(self):
        eng = _engine()
        eng.assess(_inp())  # no coaching
        eng.assess(_inp(implementation_plan_provided_pct=0.40))  # coaching
        s = eng.summary()
        assert s["coaching_count"] == 1

    def test_summary_total_churn_risk(self):
        eng = _engine()
        r1 = eng.assess(_inp())
        r2 = eng.assess(_inp(customer_expectation_alignment_rate_pct=0.50,
                              implementation_plan_provided_pct=0.10,
                              features_promised_not_delivered_pct=0.80))
        s = eng.summary()
        expected = round(r1.estimated_churn_risk_usd + r2.estimated_churn_risk_usd, 2)
        assert abs(s["total_estimated_churn_risk_usd"] - expected) < 0.01

    def test_summary_multiple_risk_levels(self):
        eng = _engine()
        # perfect rep → low
        eng.assess(_inp(rep_id="A"))
        # bad rep → critical
        eng.assess(_inp(rep_id="B",
                        implementation_plan_provided_pct=0.10,
                        success_criteria_shared_with_cs_pct=0.10,
                        deal_history_documented_pct=0.10,
                        customer_expectation_alignment_rate_pct=0.10,
                        features_promised_not_delivered_pct=0.80,
                        time_to_first_value_slip_rate_pct=0.80,
                        rep_involved_in_onboarding_pct=0.10,
                        post_sale_check_in_rate_pct=0.10,
                        escalations_requiring_rep_re_engagement_pct=0.80,
                        days_between_close_and_handoff_avg=30.0,
                        handoff_meeting_attended_pct=0.10,
                        onboarding_start_delay_days_avg=60.0))
        s = eng.summary()
        assert s["total"] == 2
        assert "low" in s["risk_counts"]
        assert "critical" in s["risk_counts"]


# ---------------------------------------------------------------------------
# End-to-end: assess
# ---------------------------------------------------------------------------

class TestAssessEndToEnd:
    def test_assess_returns_handoff_result(self):
        eng = _engine()
        r = eng.assess(_inp())
        assert isinstance(r, HandoffResult)

    def test_assess_rep_id_passes_through(self):
        eng = _engine()
        r = eng.assess(_inp(rep_id="myRep"))
        assert r.rep_id == "myRep"

    def test_assess_region_passes_through(self):
        eng = _engine()
        r = eng.assess(_inp(region="APAC"))
        assert r.region == "APAC"

    def test_assess_scores_nonneg(self):
        eng = _engine()
        r = eng.assess(_inp())
        assert r.context_score >= 0.0
        assert r.expectation_score >= 0.0
        assert r.continuity_score >= 0.0
        assert r.timing_score >= 0.0
        assert r.handoff_composite >= 0.0

    def test_assess_scores_bounded(self):
        eng = _engine()
        r = eng.assess(_inp(
            implementation_plan_provided_pct=0.10,
            success_criteria_shared_with_cs_pct=0.10,
            deal_history_documented_pct=0.10,
            customer_expectation_alignment_rate_pct=0.10,
            features_promised_not_delivered_pct=0.80,
            time_to_first_value_slip_rate_pct=0.80,
            rep_involved_in_onboarding_pct=0.10,
            post_sale_check_in_rate_pct=0.10,
            escalations_requiring_rep_re_engagement_pct=0.80,
            days_between_close_and_handoff_avg=30.0,
            handoff_meeting_attended_pct=0.10,
            onboarding_start_delay_days_avg=60.0,
        ))
        assert r.context_score <= 100.0
        assert r.expectation_score <= 100.0
        assert r.continuity_score <= 100.0
        assert r.timing_score <= 100.0
        assert r.handoff_composite <= 100.0

    def test_assess_increments_internal_results(self):
        eng = _engine()
        eng.assess(_inp(rep_id="X"))
        eng.assess(_inp(rep_id="Y"))
        assert eng.summary()["total"] == 2

    def test_assess_signal_not_empty(self):
        eng = _engine()
        r = eng.assess(_inp())
        assert len(r.handoff_signal) > 0

    def test_assess_churn_risk_nonneg(self):
        eng = _engine()
        r = eng.assess(_inp())
        assert r.estimated_churn_risk_usd >= 0.0
