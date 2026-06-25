"""
Comprehensive tests for SalesCustomerSuccessHandoffQualityIntelligenceEngine.
"""
from __future__ import annotations

import pytest
from swarm.intelligence.sales_customer_success_handoff_quality_intelligence_engine import (
    HandoffAction,
    HandoffInput,
    HandoffPattern,
    HandoffResult,
    HandoffRisk,
    HandoffSeverity,
    SalesCustomerSuccessHandoffQualityIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_input(**overrides) -> HandoffInput:
    """Return a baseline HandoffInput that produces a *low* risk / *none* pattern result."""
    defaults = dict(
        rep_id="rep-001",
        region="AMER",
        evaluation_period_id="Q1-2026",
        # context fields – all high (low risk)
        implementation_plan_provided_pct=0.90,
        success_criteria_shared_with_cs_pct=0.85,
        deal_history_documented_pct=0.85,
        # expectation fields – all low risk
        customer_expectation_alignment_rate_pct=0.90,
        features_promised_not_delivered_pct=0.05,
        time_to_first_value_slip_rate_pct=0.10,
        # continuity fields – all low risk
        rep_involved_in_onboarding_pct=0.85,
        post_sale_check_in_rate_pct=0.80,
        escalations_requiring_rep_re_engagement_pct=0.05,
        # timing fields – all low risk
        days_between_close_and_handoff_avg=1.0,
        handoff_meeting_attended_pct=0.90,
        onboarding_start_delay_days_avg=2.0,
        # outcome fields (used for churn/flags but not sub-scores)
        customer_satisfaction_at_90d_pct=0.90,
        churn_within_12m_rate_pct=0.05,
        expansion_revenue_from_cs_handoffs_pct=0.20,
        nps_detractor_rate_pct=0.05,
        reference_willingness_rate_pct=0.80,
        total_deals_closed=10,
        avg_opportunity_value_usd=50_000.0,
    )
    defaults.update(overrides)
    return HandoffInput(**defaults)


def _engine() -> SalesCustomerSuccessHandoffQualityIntelligenceEngine:
    return SalesCustomerSuccessHandoffQualityIntelligenceEngine()


# ---------------------------------------------------------------------------
# 1. Enum values
# ---------------------------------------------------------------------------

class TestEnums:
    def test_handoff_risk_values(self):
        assert HandoffRisk.low.value == "low"
        assert HandoffRisk.moderate.value == "moderate"
        assert HandoffRisk.high.value == "high"
        assert HandoffRisk.critical.value == "critical"
        assert len(HandoffRisk) == 4

    def test_handoff_pattern_values(self):
        assert HandoffPattern.none.value == "none"
        assert HandoffPattern.oversell_setup.value == "oversell_setup"
        assert HandoffPattern.expectation_mismatch.value == "expectation_mismatch"
        assert HandoffPattern.incomplete_context_transfer.value == "incomplete_context_transfer"
        assert HandoffPattern.ghosting_at_handoff.value == "ghosting_at_handoff"
        assert HandoffPattern.late_handoff_timing.value == "late_handoff_timing"
        assert len(HandoffPattern) == 6

    def test_handoff_severity_values(self):
        assert HandoffSeverity.seamless.value == "seamless"
        assert HandoffSeverity.adequate.value == "adequate"
        assert HandoffSeverity.disruptive.value == "disruptive"
        assert HandoffSeverity.damaging.value == "damaging"
        assert len(HandoffSeverity) == 4

    def test_handoff_action_values(self):
        assert HandoffAction.no_action.value == "no_action"
        assert HandoffAction.handoff_process_coaching.value == "handoff_process_coaching"
        assert HandoffAction.expectation_alignment_coaching.value == "expectation_alignment_coaching"
        assert HandoffAction.customer_success_partnership_coaching.value == "customer_success_partnership_coaching"
        assert HandoffAction.post_sale_involvement_coaching.value == "post_sale_involvement_coaching"
        assert HandoffAction.handoff_reset_intervention.value == "handoff_reset_intervention"
        assert len(HandoffAction) == 6


# ---------------------------------------------------------------------------
# 2. HandoffInput fields
# ---------------------------------------------------------------------------

class TestHandoffInput:
    def test_all_22_fields_present(self):
        inp = _make_input()
        assert inp.rep_id == "rep-001"
        assert inp.region == "AMER"
        assert inp.evaluation_period_id == "Q1-2026"
        assert inp.implementation_plan_provided_pct == 0.90
        assert inp.success_criteria_shared_with_cs_pct == 0.85
        assert inp.deal_history_documented_pct == 0.85
        assert inp.customer_expectation_alignment_rate_pct == 0.90
        assert inp.features_promised_not_delivered_pct == 0.05
        assert inp.time_to_first_value_slip_rate_pct == 0.10
        assert inp.rep_involved_in_onboarding_pct == 0.85
        assert inp.post_sale_check_in_rate_pct == 0.80
        assert inp.escalations_requiring_rep_re_engagement_pct == 0.05
        assert inp.days_between_close_and_handoff_avg == 1.0
        assert inp.handoff_meeting_attended_pct == 0.90
        assert inp.onboarding_start_delay_days_avg == 2.0
        assert inp.customer_satisfaction_at_90d_pct == 0.90
        assert inp.churn_within_12m_rate_pct == 0.05
        assert inp.expansion_revenue_from_cs_handoffs_pct == 0.20
        assert inp.nps_detractor_rate_pct == 0.05
        assert inp.reference_willingness_rate_pct == 0.80
        assert inp.total_deals_closed == 10
        assert inp.avg_opportunity_value_usd == 50_000.0

    def test_field_count(self):
        assert len(vars(_make_input())) == 22


# ---------------------------------------------------------------------------
# 3. HandoffResult fields and to_dict()
# ---------------------------------------------------------------------------

class TestHandoffResult:
    def _result(self) -> HandoffResult:
        return _engine().assess(_make_input())

    def test_all_15_result_fields(self):
        r = self._result()
        assert hasattr(r, "rep_id")
        assert hasattr(r, "region")
        assert hasattr(r, "handoff_risk")
        assert hasattr(r, "handoff_pattern")
        assert hasattr(r, "handoff_severity")
        assert hasattr(r, "recommended_action")
        assert hasattr(r, "context_score")
        assert hasattr(r, "expectation_score")
        assert hasattr(r, "continuity_score")
        assert hasattr(r, "timing_score")
        assert hasattr(r, "handoff_composite")
        assert hasattr(r, "has_handoff_gap")
        assert hasattr(r, "requires_handoff_coaching")
        assert hasattr(r, "estimated_churn_risk_usd")
        assert hasattr(r, "handoff_signal")

    def test_to_dict_returns_15_keys(self):
        d = self._result().to_dict()
        assert len(d) == 15
        expected_keys = {
            "rep_id", "region", "handoff_risk", "handoff_pattern",
            "handoff_severity", "recommended_action", "context_score",
            "expectation_score", "continuity_score", "timing_score",
            "handoff_composite", "has_handoff_gap", "requires_handoff_coaching",
            "estimated_churn_risk_usd", "handoff_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_values_are_strings(self):
        d = self._result().to_dict()
        assert isinstance(d["handoff_risk"], str)
        assert isinstance(d["handoff_pattern"], str)
        assert isinstance(d["handoff_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_rep_id_region_passthrough(self):
        inp = _make_input(rep_id="test-rep", region="EMEA")
        d = _engine().assess(inp).to_dict()
        assert d["rep_id"] == "test-rep"
        assert d["region"] == "EMEA"

    def test_result_types(self):
        r = self._result()
        assert isinstance(r.rep_id, str)
        assert isinstance(r.region, str)
        assert isinstance(r.handoff_risk, HandoffRisk)
        assert isinstance(r.handoff_pattern, HandoffPattern)
        assert isinstance(r.handoff_severity, HandoffSeverity)
        assert isinstance(r.recommended_action, HandoffAction)
        assert isinstance(r.context_score, float)
        assert isinstance(r.expectation_score, float)
        assert isinstance(r.continuity_score, float)
        assert isinstance(r.timing_score, float)
        assert isinstance(r.handoff_composite, float)
        assert isinstance(r.has_handoff_gap, bool)
        assert isinstance(r.requires_handoff_coaching, bool)
        assert isinstance(r.estimated_churn_risk_usd, float)
        assert isinstance(r.handoff_signal, str)


# ---------------------------------------------------------------------------
# 4. _context_score branches
# ---------------------------------------------------------------------------

class TestContextScore:
    def _ctx(self, **kw) -> float:
        eng = _engine()
        inp = _make_input(**kw)
        return eng._context_score(inp)

    # implementation_plan_provided_pct
    def test_impl_plan_le_030_adds_40(self):
        score = self._ctx(
            implementation_plan_provided_pct=0.30,
            success_criteria_shared_with_cs_pct=0.90,
            deal_history_documented_pct=0.90,
        )
        assert score == 40.0

    def test_impl_plan_le_055_adds_22(self):
        score = self._ctx(
            implementation_plan_provided_pct=0.55,
            success_criteria_shared_with_cs_pct=0.90,
            deal_history_documented_pct=0.90,
        )
        assert score == 22.0

    def test_impl_plan_le_075_adds_8(self):
        score = self._ctx(
            implementation_plan_provided_pct=0.75,
            success_criteria_shared_with_cs_pct=0.90,
            deal_history_documented_pct=0.90,
        )
        assert score == 8.0

    def test_impl_plan_above_075_adds_0(self):
        score = self._ctx(
            implementation_plan_provided_pct=0.76,
            success_criteria_shared_with_cs_pct=0.90,
            deal_history_documented_pct=0.90,
        )
        assert score == 0.0

    # success_criteria_shared_with_cs_pct
    def test_success_criteria_le_035_adds_35(self):
        score = self._ctx(
            implementation_plan_provided_pct=0.90,
            success_criteria_shared_with_cs_pct=0.35,
            deal_history_documented_pct=0.90,
        )
        assert score == 35.0

    def test_success_criteria_le_060_adds_18(self):
        score = self._ctx(
            implementation_plan_provided_pct=0.90,
            success_criteria_shared_with_cs_pct=0.60,
            deal_history_documented_pct=0.90,
        )
        assert score == 18.0

    def test_success_criteria_above_060_adds_0(self):
        score = self._ctx(
            implementation_plan_provided_pct=0.90,
            success_criteria_shared_with_cs_pct=0.61,
            deal_history_documented_pct=0.90,
        )
        assert score == 0.0

    # deal_history_documented_pct
    def test_deal_history_le_040_adds_25(self):
        score = self._ctx(
            implementation_plan_provided_pct=0.90,
            success_criteria_shared_with_cs_pct=0.90,
            deal_history_documented_pct=0.40,
        )
        assert score == 25.0

    def test_deal_history_le_065_adds_12(self):
        score = self._ctx(
            implementation_plan_provided_pct=0.90,
            success_criteria_shared_with_cs_pct=0.90,
            deal_history_documented_pct=0.65,
        )
        assert score == 12.0

    def test_deal_history_above_065_adds_0(self):
        score = self._ctx(
            implementation_plan_provided_pct=0.90,
            success_criteria_shared_with_cs_pct=0.90,
            deal_history_documented_pct=0.66,
        )
        assert score == 0.0

    def test_context_score_capped_at_100(self):
        # All worst-case: 40+35+25 = 100
        score = self._ctx(
            implementation_plan_provided_pct=0.10,
            success_criteria_shared_with_cs_pct=0.10,
            deal_history_documented_pct=0.10,
        )
        assert score == 100.0

    def test_context_score_combined(self):
        # 22 + 18 + 12 = 52
        score = self._ctx(
            implementation_plan_provided_pct=0.50,
            success_criteria_shared_with_cs_pct=0.50,
            deal_history_documented_pct=0.55,
        )
        assert score == 52.0

    def test_context_score_zero_all_good(self):
        score = self._ctx(
            implementation_plan_provided_pct=0.95,
            success_criteria_shared_with_cs_pct=0.95,
            deal_history_documented_pct=0.95,
        )
        assert score == 0.0


# ---------------------------------------------------------------------------
# 5. _expectation_score branches
# ---------------------------------------------------------------------------

class TestExpectationScore:
    def _exp(self, **kw) -> float:
        eng = _engine()
        inp = _make_input(**kw)
        return eng._expectation_score(inp)

    # customer_expectation_alignment_rate_pct
    def test_alignment_le_050_adds_40(self):
        score = self._exp(
            customer_expectation_alignment_rate_pct=0.50,
            features_promised_not_delivered_pct=0.05,
            time_to_first_value_slip_rate_pct=0.10,
        )
        assert score == 40.0

    def test_alignment_le_070_adds_22(self):
        score = self._exp(
            customer_expectation_alignment_rate_pct=0.70,
            features_promised_not_delivered_pct=0.05,
            time_to_first_value_slip_rate_pct=0.10,
        )
        assert score == 22.0

    def test_alignment_le_085_adds_8(self):
        score = self._exp(
            customer_expectation_alignment_rate_pct=0.85,
            features_promised_not_delivered_pct=0.05,
            time_to_first_value_slip_rate_pct=0.10,
        )
        assert score == 8.0

    def test_alignment_above_085_adds_0(self):
        score = self._exp(
            customer_expectation_alignment_rate_pct=0.86,
            features_promised_not_delivered_pct=0.05,
            time_to_first_value_slip_rate_pct=0.10,
        )
        assert score == 0.0

    # features_promised_not_delivered_pct
    def test_features_ge_025_adds_35(self):
        score = self._exp(
            customer_expectation_alignment_rate_pct=0.90,
            features_promised_not_delivered_pct=0.25,
            time_to_first_value_slip_rate_pct=0.10,
        )
        assert score == 35.0

    def test_features_ge_015_adds_18(self):
        score = self._exp(
            customer_expectation_alignment_rate_pct=0.90,
            features_promised_not_delivered_pct=0.15,
            time_to_first_value_slip_rate_pct=0.10,
        )
        assert score == 18.0

    def test_features_below_015_adds_0(self):
        score = self._exp(
            customer_expectation_alignment_rate_pct=0.90,
            features_promised_not_delivered_pct=0.14,
            time_to_first_value_slip_rate_pct=0.10,
        )
        assert score == 0.0

    # time_to_first_value_slip_rate_pct
    def test_value_slip_ge_045_adds_25(self):
        score = self._exp(
            customer_expectation_alignment_rate_pct=0.90,
            features_promised_not_delivered_pct=0.05,
            time_to_first_value_slip_rate_pct=0.45,
        )
        assert score == 25.0

    def test_value_slip_ge_025_adds_12(self):
        score = self._exp(
            customer_expectation_alignment_rate_pct=0.90,
            features_promised_not_delivered_pct=0.05,
            time_to_first_value_slip_rate_pct=0.25,
        )
        assert score == 12.0

    def test_value_slip_below_025_adds_0(self):
        score = self._exp(
            customer_expectation_alignment_rate_pct=0.90,
            features_promised_not_delivered_pct=0.05,
            time_to_first_value_slip_rate_pct=0.24,
        )
        assert score == 0.0

    def test_expectation_score_capped_at_100(self):
        score = self._exp(
            customer_expectation_alignment_rate_pct=0.10,
            features_promised_not_delivered_pct=0.50,
            time_to_first_value_slip_rate_pct=0.90,
        )
        assert score == 100.0

    def test_expectation_score_combined(self):
        # 22 + 18 + 12 = 52
        score = self._exp(
            customer_expectation_alignment_rate_pct=0.65,
            features_promised_not_delivered_pct=0.20,
            time_to_first_value_slip_rate_pct=0.30,
        )
        assert score == 52.0

    def test_expectation_score_zero_all_good(self):
        score = self._exp(
            customer_expectation_alignment_rate_pct=0.95,
            features_promised_not_delivered_pct=0.05,
            time_to_first_value_slip_rate_pct=0.10,
        )
        assert score == 0.0


# ---------------------------------------------------------------------------
# 6. _continuity_score branches
# ---------------------------------------------------------------------------

class TestContinuityScore:
    def _con(self, **kw) -> float:
        eng = _engine()
        inp = _make_input(**kw)
        return eng._continuity_score(inp)

    # rep_involved_in_onboarding_pct
    def test_rep_onboarding_le_030_adds_45(self):
        score = self._con(
            rep_involved_in_onboarding_pct=0.30,
            post_sale_check_in_rate_pct=0.80,
            escalations_requiring_rep_re_engagement_pct=0.05,
        )
        assert score == 45.0

    def test_rep_onboarding_le_055_adds_25(self):
        score = self._con(
            rep_involved_in_onboarding_pct=0.55,
            post_sale_check_in_rate_pct=0.80,
            escalations_requiring_rep_re_engagement_pct=0.05,
        )
        assert score == 25.0

    def test_rep_onboarding_le_075_adds_10(self):
        score = self._con(
            rep_involved_in_onboarding_pct=0.75,
            post_sale_check_in_rate_pct=0.80,
            escalations_requiring_rep_re_engagement_pct=0.05,
        )
        assert score == 10.0

    def test_rep_onboarding_above_075_adds_0(self):
        score = self._con(
            rep_involved_in_onboarding_pct=0.76,
            post_sale_check_in_rate_pct=0.80,
            escalations_requiring_rep_re_engagement_pct=0.05,
        )
        assert score == 0.0

    # post_sale_check_in_rate_pct
    def test_post_sale_le_025_adds_30(self):
        score = self._con(
            rep_involved_in_onboarding_pct=0.90,
            post_sale_check_in_rate_pct=0.25,
            escalations_requiring_rep_re_engagement_pct=0.05,
        )
        assert score == 30.0

    def test_post_sale_le_050_adds_15(self):
        score = self._con(
            rep_involved_in_onboarding_pct=0.90,
            post_sale_check_in_rate_pct=0.50,
            escalations_requiring_rep_re_engagement_pct=0.05,
        )
        assert score == 15.0

    def test_post_sale_above_050_adds_0(self):
        score = self._con(
            rep_involved_in_onboarding_pct=0.90,
            post_sale_check_in_rate_pct=0.51,
            escalations_requiring_rep_re_engagement_pct=0.05,
        )
        assert score == 0.0

    # escalations_requiring_rep_re_engagement_pct
    def test_escalations_ge_040_adds_25(self):
        score = self._con(
            rep_involved_in_onboarding_pct=0.90,
            post_sale_check_in_rate_pct=0.80,
            escalations_requiring_rep_re_engagement_pct=0.40,
        )
        assert score == 25.0

    def test_escalations_ge_020_adds_12(self):
        score = self._con(
            rep_involved_in_onboarding_pct=0.90,
            post_sale_check_in_rate_pct=0.80,
            escalations_requiring_rep_re_engagement_pct=0.20,
        )
        assert score == 12.0

    def test_escalations_below_020_adds_0(self):
        score = self._con(
            rep_involved_in_onboarding_pct=0.90,
            post_sale_check_in_rate_pct=0.80,
            escalations_requiring_rep_re_engagement_pct=0.19,
        )
        assert score == 0.0

    def test_continuity_score_capped_at_100(self):
        score = self._con(
            rep_involved_in_onboarding_pct=0.10,
            post_sale_check_in_rate_pct=0.10,
            escalations_requiring_rep_re_engagement_pct=0.90,
        )
        assert score == 100.0

    def test_continuity_score_combined(self):
        # 25 + 15 + 12 = 52
        score = self._con(
            rep_involved_in_onboarding_pct=0.50,
            post_sale_check_in_rate_pct=0.40,
            escalations_requiring_rep_re_engagement_pct=0.25,
        )
        assert score == 52.0

    def test_continuity_score_zero_all_good(self):
        score = self._con(
            rep_involved_in_onboarding_pct=0.90,
            post_sale_check_in_rate_pct=0.90,
            escalations_requiring_rep_re_engagement_pct=0.05,
        )
        assert score == 0.0


# ---------------------------------------------------------------------------
# 7. _timing_score branches
# ---------------------------------------------------------------------------

class TestTimingScore:
    def _tim(self, **kw) -> float:
        eng = _engine()
        inp = _make_input(**kw)
        return eng._timing_score(inp)

    # days_between_close_and_handoff_avg
    def test_days_ge_14_adds_40(self):
        score = self._tim(
            days_between_close_and_handoff_avg=14.0,
            handoff_meeting_attended_pct=0.90,
            onboarding_start_delay_days_avg=2.0,
        )
        assert score == 40.0

    def test_days_ge_7_adds_22(self):
        score = self._tim(
            days_between_close_and_handoff_avg=7.0,
            handoff_meeting_attended_pct=0.90,
            onboarding_start_delay_days_avg=2.0,
        )
        assert score == 22.0

    def test_days_ge_3_adds_8(self):
        score = self._tim(
            days_between_close_and_handoff_avg=3.0,
            handoff_meeting_attended_pct=0.90,
            onboarding_start_delay_days_avg=2.0,
        )
        assert score == 8.0

    def test_days_below_3_adds_0(self):
        score = self._tim(
            days_between_close_and_handoff_avg=2.9,
            handoff_meeting_attended_pct=0.90,
            onboarding_start_delay_days_avg=2.0,
        )
        assert score == 0.0

    # handoff_meeting_attended_pct
    def test_meeting_le_040_adds_35(self):
        score = self._tim(
            days_between_close_and_handoff_avg=1.0,
            handoff_meeting_attended_pct=0.40,
            onboarding_start_delay_days_avg=2.0,
        )
        assert score == 35.0

    def test_meeting_le_065_adds_18(self):
        score = self._tim(
            days_between_close_and_handoff_avg=1.0,
            handoff_meeting_attended_pct=0.65,
            onboarding_start_delay_days_avg=2.0,
        )
        assert score == 18.0

    def test_meeting_above_065_adds_0(self):
        score = self._tim(
            days_between_close_and_handoff_avg=1.0,
            handoff_meeting_attended_pct=0.66,
            onboarding_start_delay_days_avg=2.0,
        )
        assert score == 0.0

    # onboarding_start_delay_days_avg
    def test_onboarding_delay_ge_21_adds_25(self):
        score = self._tim(
            days_between_close_and_handoff_avg=1.0,
            handoff_meeting_attended_pct=0.90,
            onboarding_start_delay_days_avg=21.0,
        )
        assert score == 25.0

    def test_onboarding_delay_ge_10_adds_12(self):
        score = self._tim(
            days_between_close_and_handoff_avg=1.0,
            handoff_meeting_attended_pct=0.90,
            onboarding_start_delay_days_avg=10.0,
        )
        assert score == 12.0

    def test_onboarding_delay_below_10_adds_0(self):
        score = self._tim(
            days_between_close_and_handoff_avg=1.0,
            handoff_meeting_attended_pct=0.90,
            onboarding_start_delay_days_avg=9.9,
        )
        assert score == 0.0

    def test_timing_score_capped_at_100(self):
        score = self._tim(
            days_between_close_and_handoff_avg=20.0,
            handoff_meeting_attended_pct=0.10,
            onboarding_start_delay_days_avg=30.0,
        )
        assert score == 100.0

    def test_timing_score_combined(self):
        # 22 + 18 + 12 = 52
        score = self._tim(
            days_between_close_and_handoff_avg=10.0,
            handoff_meeting_attended_pct=0.55,
            onboarding_start_delay_days_avg=15.0,
        )
        assert score == 52.0

    def test_timing_score_zero_all_good(self):
        score = self._tim(
            days_between_close_and_handoff_avg=1.0,
            handoff_meeting_attended_pct=0.90,
            onboarding_start_delay_days_avg=2.0,
        )
        assert score == 0.0


# ---------------------------------------------------------------------------
# 8. Composite formula weights
# ---------------------------------------------------------------------------

class TestCompositeFormula:
    def test_composite_uses_correct_weights(self):
        """
        Build an input where each sub-score is known and verify
        composite = context*0.30 + expectation*0.30 + continuity*0.25 + timing*0.15
        """
        eng = _engine()
        # context = 40 (impl<=0.30), expectation = 40 (alignment<=0.50),
        # continuity = 45 (rep_onb<=0.30), timing = 40 (days>=14)
        inp = _make_input(
            implementation_plan_provided_pct=0.20,
            success_criteria_shared_with_cs_pct=0.90,
            deal_history_documented_pct=0.90,
            customer_expectation_alignment_rate_pct=0.40,
            features_promised_not_delivered_pct=0.05,
            time_to_first_value_slip_rate_pct=0.10,
            rep_involved_in_onboarding_pct=0.20,
            post_sale_check_in_rate_pct=0.80,
            escalations_requiring_rep_re_engagement_pct=0.05,
            days_between_close_and_handoff_avg=14.0,
            handoff_meeting_attended_pct=0.90,
            onboarding_start_delay_days_avg=2.0,
        )
        ctx = eng._context_score(inp)   # 40
        exp = eng._expectation_score(inp)  # 40
        con = eng._continuity_score(inp)   # 45
        tim = eng._timing_score(inp)       # 40

        expected = round(ctx * 0.30 + exp * 0.30 + con * 0.25 + tim * 0.15, 1)
        result = eng.assess(inp)
        assert result.handoff_composite == expected

    def test_composite_weights_sum_to_one(self):
        assert abs(0.30 + 0.30 + 0.25 + 0.15 - 1.00) < 1e-9

    def test_composite_capped_at_100(self):
        eng = _engine()
        inp = _make_input(
            implementation_plan_provided_pct=0.10,
            success_criteria_shared_with_cs_pct=0.10,
            deal_history_documented_pct=0.10,
            customer_expectation_alignment_rate_pct=0.10,
            features_promised_not_delivered_pct=0.90,
            time_to_first_value_slip_rate_pct=0.90,
            rep_involved_in_onboarding_pct=0.10,
            post_sale_check_in_rate_pct=0.10,
            escalations_requiring_rep_re_engagement_pct=0.90,
            days_between_close_and_handoff_avg=20.0,
            handoff_meeting_attended_pct=0.10,
            onboarding_start_delay_days_avg=30.0,
        )
        result = eng.assess(inp)
        assert result.handoff_composite <= 100.0

    def test_composite_max_is_100_for_all_worst_case(self):
        eng = _engine()
        inp = _make_input(
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
        )
        result = eng.assess(inp)
        assert result.handoff_composite == 100.0

    def test_composite_zero_for_all_low_risk(self):
        eng = _engine()
        result = eng.assess(_make_input())
        assert result.handoff_composite == 0.0

    def test_composite_matches_subscores_formula(self):
        eng = _engine()
        inp = _make_input(
            implementation_plan_provided_pct=0.45,
            success_criteria_shared_with_cs_pct=0.50,
            deal_history_documented_pct=0.55,
            customer_expectation_alignment_rate_pct=0.65,
            features_promised_not_delivered_pct=0.20,
            time_to_first_value_slip_rate_pct=0.30,
            rep_involved_in_onboarding_pct=0.50,
            post_sale_check_in_rate_pct=0.40,
            escalations_requiring_rep_re_engagement_pct=0.25,
            days_between_close_and_handoff_avg=10.0,
            handoff_meeting_attended_pct=0.55,
            onboarding_start_delay_days_avg=15.0,
        )
        result = eng.assess(inp)
        expected = min(round(
            result.context_score * 0.30
            + result.expectation_score * 0.30
            + result.continuity_score * 0.25
            + result.timing_score * 0.15,
            1,
        ), 100.0)
        assert result.handoff_composite == expected


# ---------------------------------------------------------------------------
# 9. Pattern detection & priority ordering
# ---------------------------------------------------------------------------

class TestPatternDetection:
    def test_oversell_setup_detected(self):
        """features_promised_not_delivered>=0.20 AND expectation>=40"""
        eng = _engine()
        # expectation >= 40: alignment<=0.50 -> +40
        inp = _make_input(
            features_promised_not_delivered_pct=0.20,
            customer_expectation_alignment_rate_pct=0.40,
        )
        result = eng.assess(inp)
        assert result.handoff_pattern == HandoffPattern.oversell_setup

    def test_expectation_mismatch_detected(self):
        """alignment<=0.45 AND time_to_first_value_slip>=0.40, no oversell trigger"""
        eng = _engine()
        inp = _make_input(
            customer_expectation_alignment_rate_pct=0.45,
            time_to_first_value_slip_rate_pct=0.40,
            features_promised_not_delivered_pct=0.05,  # no oversell
        )
        result = eng.assess(inp)
        assert result.handoff_pattern == HandoffPattern.expectation_mismatch

    def test_incomplete_context_transfer_detected(self):
        """context>=40 AND impl_plan<=0.25, no oversell or expectation mismatch"""
        eng = _engine()
        inp = _make_input(
            implementation_plan_provided_pct=0.25,
            success_criteria_shared_with_cs_pct=0.90,
            deal_history_documented_pct=0.90,
            features_promised_not_delivered_pct=0.05,
            customer_expectation_alignment_rate_pct=0.90,
            time_to_first_value_slip_rate_pct=0.10,
        )
        result = eng.assess(inp)
        assert result.handoff_pattern == HandoffPattern.incomplete_context_transfer

    def test_ghosting_at_handoff_detected(self):
        """rep_involved<=0.25 AND continuity>=30, no higher priority"""
        eng = _engine()
        # continuity>=30: rep_onb<=0.25 -> +45
        inp = _make_input(
            rep_involved_in_onboarding_pct=0.25,
            post_sale_check_in_rate_pct=0.80,
            escalations_requiring_rep_re_engagement_pct=0.05,
            features_promised_not_delivered_pct=0.05,
            customer_expectation_alignment_rate_pct=0.90,
            time_to_first_value_slip_rate_pct=0.10,
            implementation_plan_provided_pct=0.90,
        )
        result = eng.assess(inp)
        assert result.handoff_pattern == HandoffPattern.ghosting_at_handoff

    def test_late_handoff_timing_detected(self):
        """days>=10 AND timing>=30, no higher priority"""
        eng = _engine()
        # timing>=30: days>=14 -> +40
        inp = _make_input(
            days_between_close_and_handoff_avg=14.0,
            handoff_meeting_attended_pct=0.90,
            onboarding_start_delay_days_avg=2.0,
            features_promised_not_delivered_pct=0.05,
            customer_expectation_alignment_rate_pct=0.90,
            time_to_first_value_slip_rate_pct=0.10,
            implementation_plan_provided_pct=0.90,
            rep_involved_in_onboarding_pct=0.85,
        )
        result = eng.assess(inp)
        assert result.handoff_pattern == HandoffPattern.late_handoff_timing

    def test_none_pattern_when_all_good(self):
        eng = _engine()
        result = eng.assess(_make_input())
        assert result.handoff_pattern == HandoffPattern.none

    def test_oversell_takes_priority_over_expectation_mismatch(self):
        """When both oversell and expectation_mismatch conditions are met, oversell wins."""
        eng = _engine()
        inp = _make_input(
            features_promised_not_delivered_pct=0.20,    # oversell trigger
            customer_expectation_alignment_rate_pct=0.45, # also expectation mismatch trigger
            time_to_first_value_slip_rate_pct=0.40,      # also expectation mismatch trigger
        )
        result = eng.assess(inp)
        assert result.handoff_pattern == HandoffPattern.oversell_setup

    def test_oversell_takes_priority_over_ghosting(self):
        """oversell wins over ghosting."""
        eng = _engine()
        inp = _make_input(
            features_promised_not_delivered_pct=0.20,
            customer_expectation_alignment_rate_pct=0.40,  # expectation>=40 via alignment
            rep_involved_in_onboarding_pct=0.25,
        )
        result = eng.assess(inp)
        assert result.handoff_pattern == HandoffPattern.oversell_setup

    def test_expectation_mismatch_beats_incomplete_context(self):
        """expectation_mismatch (#2) beats incomplete_context_transfer (#3)."""
        eng = _engine()
        inp = _make_input(
            features_promised_not_delivered_pct=0.05,          # no oversell
            customer_expectation_alignment_rate_pct=0.45,      # expectation_mismatch
            time_to_first_value_slip_rate_pct=0.40,            # expectation_mismatch
            implementation_plan_provided_pct=0.25,             # incomplete_context
            success_criteria_shared_with_cs_pct=0.90,
            deal_history_documented_pct=0.90,
        )
        result = eng.assess(inp)
        assert result.handoff_pattern == HandoffPattern.expectation_mismatch

    def test_incomplete_context_beats_ghosting(self):
        """incomplete_context_transfer (#3) beats ghosting_at_handoff (#4)."""
        eng = _engine()
        inp = _make_input(
            features_promised_not_delivered_pct=0.05,
            customer_expectation_alignment_rate_pct=0.90,
            time_to_first_value_slip_rate_pct=0.10,
            implementation_plan_provided_pct=0.25,         # incomplete_context trigger
            success_criteria_shared_with_cs_pct=0.90,
            deal_history_documented_pct=0.90,
            rep_involved_in_onboarding_pct=0.25,           # ghosting trigger too
            post_sale_check_in_rate_pct=0.80,
            escalations_requiring_rep_re_engagement_pct=0.05,
        )
        result = eng.assess(inp)
        assert result.handoff_pattern == HandoffPattern.incomplete_context_transfer

    def test_ghosting_beats_late_timing(self):
        """ghosting_at_handoff (#4) beats late_handoff_timing (#5)."""
        eng = _engine()
        inp = _make_input(
            features_promised_not_delivered_pct=0.05,
            customer_expectation_alignment_rate_pct=0.90,
            time_to_first_value_slip_rate_pct=0.10,
            implementation_plan_provided_pct=0.90,          # no incomplete_context
            rep_involved_in_onboarding_pct=0.25,            # ghosting trigger
            post_sale_check_in_rate_pct=0.80,
            escalations_requiring_rep_re_engagement_pct=0.05,
            days_between_close_and_handoff_avg=14.0,        # late timing trigger
            handoff_meeting_attended_pct=0.90,
            onboarding_start_delay_days_avg=2.0,
        )
        result = eng.assess(inp)
        assert result.handoff_pattern == HandoffPattern.ghosting_at_handoff

    def test_oversell_requires_expectation_ge_40(self):
        """oversell_setup needs BOTH features>=0.20 AND expectation>=40"""
        eng = _engine()
        # features>=0.20 but expectation score will be 0 (alignment=0.90, slip=0.10)
        inp = _make_input(
            features_promised_not_delivered_pct=0.20,
            customer_expectation_alignment_rate_pct=0.90,
            time_to_first_value_slip_rate_pct=0.10,
        )
        result = eng.assess(inp)
        # expectation = 18 (features=0.20>=0.15 -> +18, but <0.25 so not +35; align>0.85 -> 0; slip<0.25 -> 0) = 18
        # expectation_score=18 < 40 so oversell_setup NOT triggered
        assert result.handoff_pattern != HandoffPattern.oversell_setup

    def test_ghosting_requires_continuity_ge_30(self):
        """ghosting_at_handoff needs rep_onb<=0.25 AND continuity>=30"""
        eng = _engine()
        # rep_onb=0.25 but force continuity<30 by making post_sale high enough
        # rep_onb=0.25: continuity += 45; post_sale=0.90: 0; escalations=0.05: 0 => continuity=45>=30
        # So with rep_onb=0.26 (>0.25): ghosting NOT triggered regardless of continuity
        inp = _make_input(
            rep_involved_in_onboarding_pct=0.26,  # > 0.25, no ghosting trigger
            post_sale_check_in_rate_pct=0.10,
            escalations_requiring_rep_re_engagement_pct=0.50,
        )
        result = eng.assess(inp)
        assert result.handoff_pattern != HandoffPattern.ghosting_at_handoff

    def test_late_timing_requires_days_ge_10(self):
        """late_handoff_timing: days>=10 is required"""
        eng = _engine()
        # days=9.9 < 10 so late_timing NOT triggered even if timing score high
        inp = _make_input(
            days_between_close_and_handoff_avg=9.9,
            handoff_meeting_attended_pct=0.10,  # timing += 35
            onboarding_start_delay_days_avg=30.0,  # timing += 25
        )
        result = eng.assess(inp)
        assert result.handoff_pattern != HandoffPattern.late_handoff_timing


# ---------------------------------------------------------------------------
# 10. Risk / severity thresholds at exact boundaries
# ---------------------------------------------------------------------------

class TestRiskThresholds:
    def test_risk_critical_at_composite_60(self):
        eng = _engine()
        # ctx=100, exp=100, con=0, tim=0 => composite=60
        inp = _make_input(
            implementation_plan_provided_pct=0.10,
            success_criteria_shared_with_cs_pct=0.10,
            deal_history_documented_pct=0.10,
            customer_expectation_alignment_rate_pct=0.10,
            features_promised_not_delivered_pct=0.50,
            time_to_first_value_slip_rate_pct=0.90,
            rep_involved_in_onboarding_pct=0.90,
            post_sale_check_in_rate_pct=0.90,
            escalations_requiring_rep_re_engagement_pct=0.05,
            days_between_close_and_handoff_avg=1.0,
            handoff_meeting_attended_pct=0.90,
            onboarding_start_delay_days_avg=2.0,
        )
        result = eng.assess(inp)
        assert result.handoff_composite == 60.0
        assert result.handoff_risk == HandoffRisk.critical
        assert result.handoff_severity == HandoffSeverity.damaging

    def test_risk_high_at_composite_40(self):
        eng = _engine()
        # ctx=40, exp=40, con=40, tim=40 => composite=12+12+10+6=40
        inp = _make_input(
            implementation_plan_provided_pct=0.20,         # ctx: +40
            success_criteria_shared_with_cs_pct=0.90,
            deal_history_documented_pct=0.90,
            customer_expectation_alignment_rate_pct=0.40,  # exp: +40
            features_promised_not_delivered_pct=0.05,
            time_to_first_value_slip_rate_pct=0.10,
            rep_involved_in_onboarding_pct=0.40,           # con: +25
            post_sale_check_in_rate_pct=0.50,              # con: +15 => con=40
            escalations_requiring_rep_re_engagement_pct=0.05,
            days_between_close_and_handoff_avg=14.0,       # tim: +40
            handoff_meeting_attended_pct=0.90,
            onboarding_start_delay_days_avg=2.0,
        )
        result = eng.assess(inp)
        assert result.handoff_composite == 40.0
        assert result.handoff_risk == HandoffRisk.high
        assert result.handoff_severity == HandoffSeverity.disruptive

    def test_risk_moderate_in_range_20_to_40(self):
        eng = _engine()
        inp = _make_input(
            implementation_plan_provided_pct=0.45,   # ctx: +22
            success_criteria_shared_with_cs_pct=0.36, # ctx: +18 -> ctx=40
            deal_history_documented_pct=0.90,
            customer_expectation_alignment_rate_pct=0.65,  # exp: +22
            features_promised_not_delivered_pct=0.05,
            time_to_first_value_slip_rate_pct=0.10,
            rep_involved_in_onboarding_pct=0.40,     # con: +25
            post_sale_check_in_rate_pct=0.90,
            escalations_requiring_rep_re_engagement_pct=0.05,
            days_between_close_and_handoff_avg=8.0,  # tim: +22
            handoff_meeting_attended_pct=0.90,
            onboarding_start_delay_days_avg=2.0,
        )
        result = eng.assess(inp)
        # ctx=40, exp=22, con=25, tim=22 => 12+6.6+6.25+3.3=28.15
        assert 20 <= result.handoff_composite < 40
        assert result.handoff_risk == HandoffRisk.moderate
        assert result.handoff_severity == HandoffSeverity.adequate

    def test_risk_low_below_20(self):
        eng = _engine()
        result = eng.assess(_make_input())
        assert result.handoff_composite == 0.0
        assert result.handoff_risk == HandoffRisk.low
        assert result.handoff_severity == HandoffSeverity.seamless

    def test_risk_low_just_below_20(self):
        eng = _engine()
        # ctx=22 only => composite=22*0.30=6.6 <20 => low
        inp = _make_input(
            implementation_plan_provided_pct=0.45,   # ctx: +22
            success_criteria_shared_with_cs_pct=0.90,
            deal_history_documented_pct=0.90,
        )
        result = eng.assess(inp)
        assert result.handoff_composite < 20
        assert result.handoff_risk == HandoffRisk.low

    def test_severity_exact_60_is_damaging(self):
        eng = _engine()
        inp = _make_input(
            implementation_plan_provided_pct=0.10,
            success_criteria_shared_with_cs_pct=0.10,
            deal_history_documented_pct=0.10,
            customer_expectation_alignment_rate_pct=0.10,
            features_promised_not_delivered_pct=0.50,
            time_to_first_value_slip_rate_pct=0.90,
            rep_involved_in_onboarding_pct=0.90,
            post_sale_check_in_rate_pct=0.90,
            escalations_requiring_rep_re_engagement_pct=0.05,
            days_between_close_and_handoff_avg=1.0,
            handoff_meeting_attended_pct=0.90,
            onboarding_start_delay_days_avg=2.0,
        )
        result = eng.assess(inp)
        assert result.handoff_composite == 60.0
        assert result.handoff_severity == HandoffSeverity.damaging

    def test_severity_exact_40_is_disruptive(self):
        eng = _engine()
        inp = _make_input(
            implementation_plan_provided_pct=0.20,
            success_criteria_shared_with_cs_pct=0.90,
            deal_history_documented_pct=0.90,
            customer_expectation_alignment_rate_pct=0.40,
            features_promised_not_delivered_pct=0.05,
            time_to_first_value_slip_rate_pct=0.10,
            rep_involved_in_onboarding_pct=0.40,
            post_sale_check_in_rate_pct=0.50,
            escalations_requiring_rep_re_engagement_pct=0.05,
            days_between_close_and_handoff_avg=14.0,
            handoff_meeting_attended_pct=0.90,
            onboarding_start_delay_days_avg=2.0,
        )
        result = eng.assess(inp)
        assert result.handoff_composite == 40.0
        assert result.handoff_severity == HandoffSeverity.disruptive


# ---------------------------------------------------------------------------
# 11. Action mappings
# ---------------------------------------------------------------------------

class TestActionMappings:
    def test_critical_oversell_setup_action(self):
        eng = _engine()
        inp = _make_input(
            implementation_plan_provided_pct=0.10,
            success_criteria_shared_with_cs_pct=0.10,
            deal_history_documented_pct=0.10,
            customer_expectation_alignment_rate_pct=0.10,
            features_promised_not_delivered_pct=0.50,  # >=0.20 + exp>=40
            time_to_first_value_slip_rate_pct=0.90,
            rep_involved_in_onboarding_pct=0.90,
            post_sale_check_in_rate_pct=0.90,
            escalations_requiring_rep_re_engagement_pct=0.05,
            days_between_close_and_handoff_avg=1.0,
            handoff_meeting_attended_pct=0.90,
            onboarding_start_delay_days_avg=2.0,
        )
        result = eng.assess(inp)
        assert result.handoff_risk == HandoffRisk.critical
        assert result.handoff_pattern == HandoffPattern.oversell_setup
        assert result.recommended_action == HandoffAction.expectation_alignment_coaching

    def test_critical_expectation_mismatch_action(self):
        eng = _engine()
        # critical + expectation_mismatch: alignment<=0.45 AND slip>=0.40, no oversell
        # To reach composite>=60 we add continuity pressure too:
        # ctx=100, exp=65, con=65, tim=35 => 30+19.5+16.25+5.25=71 (critical)
        # alignment=0.45<=0.45 AND slip=0.90>=0.40 -> expectation_mismatch
        # features=0.05<0.20 -> no oversell
        inp = _make_input(
            implementation_plan_provided_pct=0.10,
            success_criteria_shared_with_cs_pct=0.10,
            deal_history_documented_pct=0.10,
            customer_expectation_alignment_rate_pct=0.45,  # <=0.45 expectation_mismatch trigger
            features_promised_not_delivered_pct=0.05,       # <0.20 no oversell
            time_to_first_value_slip_rate_pct=0.90,         # >=0.40 expectation_mismatch trigger
            rep_involved_in_onboarding_pct=0.56,            # con: +10 (<=0.75)
            post_sale_check_in_rate_pct=0.10,               # con: +30 (<=0.25)
            escalations_requiring_rep_re_engagement_pct=0.45, # con: +25 (>=0.40) => con=65
            days_between_close_and_handoff_avg=1.0,
            handoff_meeting_attended_pct=0.10,              # tim: +35 (<=0.40)
            onboarding_start_delay_days_avg=2.0,
        )
        result = eng.assess(inp)
        # ctx=100, exp=65, con=65, tim=35 => composite=30+19.5+16.25+5.25=71 -> critical
        assert result.handoff_risk == HandoffRisk.critical
        assert result.handoff_pattern == HandoffPattern.expectation_mismatch
        assert result.recommended_action == HandoffAction.expectation_alignment_coaching

    def test_critical_other_pattern_gives_reset_intervention(self):
        eng = _engine()
        # critical + none pattern -> handoff_reset_intervention
        # ctx=100 (impl=0.30, success=0.10, deal=0.10), exp high via slip
        # But: impl=0.30>0.25 so no incomplete_context, alignment=0.49>0.45 no expectation_mismatch
        # features<0.20 no oversell, rep_onb=0.90 no ghosting, days=1 no late_timing
        inp = _make_input(
            implementation_plan_provided_pct=0.30,   # ctx: +40 (<=0.30), but >0.25 so no incomplete_context
            success_criteria_shared_with_cs_pct=0.10,  # ctx: +35
            deal_history_documented_pct=0.10,           # ctx: +25 => ctx=100
            customer_expectation_alignment_rate_pct=0.49, # exp: +40 (<=0.50), but >0.45 no expectation_mismatch
            features_promised_not_delivered_pct=0.05,    # no oversell
            time_to_first_value_slip_rate_pct=0.90,      # exp: +25 => exp=65
            rep_involved_in_onboarding_pct=0.56,          # con: +10 (<=0.75)
            post_sale_check_in_rate_pct=0.10,             # con: +30
            escalations_requiring_rep_re_engagement_pct=0.45, # con: +25 => con=65
            days_between_close_and_handoff_avg=1.0,      # no late timing
            handoff_meeting_attended_pct=0.10,           # tim: +35
            onboarding_start_delay_days_avg=2.0,
        )
        result = eng.assess(inp)
        # ctx=100, exp=65, con=65, tim=35
        # composite=30+19.5+16.25+5.25=71.0 -> critical
        assert result.handoff_risk == HandoffRisk.critical
        assert result.handoff_pattern == HandoffPattern.none
        assert result.recommended_action == HandoffAction.handoff_reset_intervention

    def test_high_incomplete_context_transfer_action(self):
        eng = _engine()
        # high + incomplete_context_transfer -> handoff_process_coaching
        # ctx=40 (impl=0.25, s.c.=0.90, deal=0.90), exp=40 (alignment=0.40)
        # con=40 (rep_onb=0.40->+25, post=0.50->+15), tim=40 (days=14->+40)
        # composite=12+12+10+6=40 => high
        inp = _make_input(
            implementation_plan_provided_pct=0.25,   # ctx: +40, AND <=0.25 for pattern
            success_criteria_shared_with_cs_pct=0.90,
            deal_history_documented_pct=0.90,
            customer_expectation_alignment_rate_pct=0.40,   # exp: +40
            features_promised_not_delivered_pct=0.05,       # no oversell
            time_to_first_value_slip_rate_pct=0.10,         # slip<0.40 so no expectation_mismatch
            rep_involved_in_onboarding_pct=0.40,            # con: +25
            post_sale_check_in_rate_pct=0.50,               # con: +15
            escalations_requiring_rep_re_engagement_pct=0.05,
            days_between_close_and_handoff_avg=14.0,        # tim: +40
            handoff_meeting_attended_pct=0.90,
            onboarding_start_delay_days_avg=2.0,
        )
        result = eng.assess(inp)
        assert result.handoff_risk == HandoffRisk.high
        assert result.handoff_pattern == HandoffPattern.incomplete_context_transfer
        assert result.recommended_action == HandoffAction.handoff_process_coaching

    def test_high_ghosting_at_handoff_action(self):
        eng = _engine()
        # high + ghosting -> post_sale_involvement_coaching
        # Need: composite>=40, pattern=ghosting
        # impl=0.30>0.25 so no incomplete_context; features<0.20 no oversell
        # alignment=0.80 no expectation_mismatch; rep_onb=0.25 ghosting trigger
        inp = _make_input(
            implementation_plan_provided_pct=0.30,          # ctx: +40 (>0.25 no incomplete_context)
            success_criteria_shared_with_cs_pct=0.35,       # ctx: +35 => ctx=75
            deal_history_documented_pct=0.90,
            customer_expectation_alignment_rate_pct=0.80,   # exp: +8 (<=0.85)
            features_promised_not_delivered_pct=0.05,
            time_to_first_value_slip_rate_pct=0.10,
            rep_involved_in_onboarding_pct=0.25,            # ghosting trigger (<=0.25)
            post_sale_check_in_rate_pct=0.80,               # con: 0
            escalations_requiring_rep_re_engagement_pct=0.05, # con: 0 => con=45
            days_between_close_and_handoff_avg=14.0,        # tim: +40
            handoff_meeting_attended_pct=0.90,
            onboarding_start_delay_days_avg=2.0,
        )
        result = eng.assess(inp)
        # ctx=75, exp=8, con=45, tim=40
        # composite=22.5+2.4+11.25+6=42.15 -> high
        assert result.handoff_risk == HandoffRisk.high
        assert result.handoff_pattern == HandoffPattern.ghosting_at_handoff
        assert result.recommended_action == HandoffAction.post_sale_involvement_coaching

    def test_high_other_pattern_gives_customer_success_partnership(self):
        eng = _engine()
        # high + late_handoff_timing -> customer_success_partnership_coaching
        inp = _make_input(
            implementation_plan_provided_pct=0.30,       # ctx: +40 (>0.25 no incomplete_context)
            success_criteria_shared_with_cs_pct=0.35,   # ctx: +35 => ctx=75
            deal_history_documented_pct=0.90,
            customer_expectation_alignment_rate_pct=0.80, # exp: +8
            features_promised_not_delivered_pct=0.05,
            time_to_first_value_slip_rate_pct=0.10,
            rep_involved_in_onboarding_pct=0.40,         # con: +25 (>0.25 no ghosting)
            post_sale_check_in_rate_pct=0.40,            # con: +15
            escalations_requiring_rep_re_engagement_pct=0.25, # con: +12 => con=52
            days_between_close_and_handoff_avg=14.0,     # tim: +40, late_timing trigger (>=10)
            handoff_meeting_attended_pct=0.90,
            onboarding_start_delay_days_avg=2.0,
        )
        result = eng.assess(inp)
        # ctx=75, exp=8, con=52, tim=40
        # composite=22.5+2.4+13+6=43.9 -> high
        assert result.handoff_risk == HandoffRisk.high
        assert result.handoff_pattern == HandoffPattern.late_handoff_timing
        assert result.recommended_action == HandoffAction.customer_success_partnership_coaching

    def test_moderate_gives_handoff_process_coaching(self):
        eng = _engine()
        inp = _make_input(
            implementation_plan_provided_pct=0.45,
            success_criteria_shared_with_cs_pct=0.36,
            deal_history_documented_pct=0.90,
            customer_expectation_alignment_rate_pct=0.65,
            features_promised_not_delivered_pct=0.05,
            time_to_first_value_slip_rate_pct=0.10,
            rep_involved_in_onboarding_pct=0.40,
            post_sale_check_in_rate_pct=0.90,
            escalations_requiring_rep_re_engagement_pct=0.05,
            days_between_close_and_handoff_avg=8.0,
            handoff_meeting_attended_pct=0.90,
            onboarding_start_delay_days_avg=2.0,
        )
        result = eng.assess(inp)
        assert result.handoff_risk == HandoffRisk.moderate
        assert result.recommended_action == HandoffAction.handoff_process_coaching

    def test_low_gives_no_action(self):
        eng = _engine()
        result = eng.assess(_make_input())
        assert result.handoff_risk == HandoffRisk.low
        assert result.recommended_action == HandoffAction.no_action


# ---------------------------------------------------------------------------
# 12. Flag conditions
# ---------------------------------------------------------------------------

class TestFlagConditions:
    def test_has_handoff_gap_via_composite_ge_40(self):
        eng = _engine()
        # ctx=40, exp=40, con=40, tim=40 => composite=40
        inp = _make_input(
            implementation_plan_provided_pct=0.20,
            success_criteria_shared_with_cs_pct=0.90,
            deal_history_documented_pct=0.90,
            customer_expectation_alignment_rate_pct=0.90,   # >0.60 no gap via alignment
            features_promised_not_delivered_pct=0.05,
            time_to_first_value_slip_rate_pct=0.10,
            rep_involved_in_onboarding_pct=0.40,            # >0.35 no gap via rep_onb
            post_sale_check_in_rate_pct=0.50,
            escalations_requiring_rep_re_engagement_pct=0.05,
            days_between_close_and_handoff_avg=14.0,
            handoff_meeting_attended_pct=0.90,
            onboarding_start_delay_days_avg=2.0,
        )
        result = eng.assess(inp)
        # composite=12+0+10+6=28 < 40
        # Actually: exp=0 since alignment=0.90>0.85, features<0.15, slip<0.25
        # composite=40*0.30+0+40*0.25+40*0.15=12+0+10+6=28 <40
        # alignment=0.90>0.60, rep_onb=0.40>0.35 -> no gap
        assert result.has_handoff_gap is False

        # Now push composite>=40 without triggering other gap conditions
        inp2 = _make_input(
            implementation_plan_provided_pct=0.10,
            success_criteria_shared_with_cs_pct=0.10,
            deal_history_documented_pct=0.10,
            customer_expectation_alignment_rate_pct=0.90,
            features_promised_not_delivered_pct=0.50,
            time_to_first_value_slip_rate_pct=0.90,
            rep_involved_in_onboarding_pct=0.90,            # >0.35
            post_sale_check_in_rate_pct=0.90,
            escalations_requiring_rep_re_engagement_pct=0.05,
            days_between_close_and_handoff_avg=1.0,
            handoff_meeting_attended_pct=0.90,
            onboarding_start_delay_days_avg=2.0,
        )
        result2 = eng.assess(inp2)
        # ctx=100, exp=100, con=0, tim=0 => composite=60 >=40 -> gap!
        assert result2.has_handoff_gap is True

    def test_has_handoff_gap_via_low_alignment_exactly_060(self):
        eng = _engine()
        inp = _make_input(
            customer_expectation_alignment_rate_pct=0.60,
            rep_involved_in_onboarding_pct=0.90,
        )
        result = eng.assess(inp)
        assert result.has_handoff_gap is True

    def test_no_gap_alignment_just_above_060(self):
        eng = _engine()
        inp = _make_input(
            customer_expectation_alignment_rate_pct=0.61,
            rep_involved_in_onboarding_pct=0.90,
        )
        result = eng.assess(inp)
        # Only gap sources: composite<40 (exp=22 only -> composite=6.6), alignment>0.60, rep_onb>0.35
        assert result.has_handoff_gap is False

    def test_has_handoff_gap_via_low_rep_onboarding_exactly_035(self):
        eng = _engine()
        inp = _make_input(
            customer_expectation_alignment_rate_pct=0.90,
            rep_involved_in_onboarding_pct=0.35,
        )
        result = eng.assess(inp)
        assert result.has_handoff_gap is True

    def test_no_gap_rep_onboarding_just_above_035(self):
        eng = _engine()
        inp = _make_input(
            customer_expectation_alignment_rate_pct=0.90,
            rep_involved_in_onboarding_pct=0.36,
        )
        result = eng.assess(inp)
        # composite will be from con only: rep_onb=0.36<=0.55 -> +25 => composite=25*0.25=6.25 <40
        assert result.has_handoff_gap is False

    def test_no_handoff_gap_when_all_clear(self):
        eng = _engine()
        result = eng.assess(_make_input())
        assert result.has_handoff_gap is False

    def test_requires_coaching_via_composite_ge_30(self):
        eng = _engine()
        # ctx=52 (22+18+12=52 via 0.45/0.36/0.41), exp=22, con=25, tim=22
        # composite=15.6+6.6+6.25+3.3=31.75 >=30 -> coaching
        inp = _make_input(
            implementation_plan_provided_pct=0.46,          # ctx: +22 (<=0.55>0.30)
            success_criteria_shared_with_cs_pct=0.36,       # ctx: +18 (<=0.60>0.35) -> 40
            deal_history_documented_pct=0.41,               # ctx: +12 (<=0.65>0.40) => ctx=52
            customer_expectation_alignment_rate_pct=0.65,   # exp: +22
            features_promised_not_delivered_pct=0.14,       # <0.15 no coaching trigger
            time_to_first_value_slip_rate_pct=0.10,
            rep_involved_in_onboarding_pct=0.40,            # con: +25
            post_sale_check_in_rate_pct=0.90,
            escalations_requiring_rep_re_engagement_pct=0.05,
            days_between_close_and_handoff_avg=8.0,         # tim: +22
            handoff_meeting_attended_pct=0.90,
            onboarding_start_delay_days_avg=2.0,
        )
        result = eng.assess(inp)
        assert result.handoff_composite >= 30
        assert result.requires_handoff_coaching is True

    def test_requires_coaching_via_impl_plan_le_045(self):
        eng = _engine()
        inp = _make_input(implementation_plan_provided_pct=0.45)
        result = eng.assess(inp)
        assert result.requires_handoff_coaching is True

    def test_no_coaching_impl_plan_just_above_045(self):
        eng = _engine()
        # impl=0.46 (>0.45 no coaching), features=0.05 (<0.15 no coaching), composite~0
        inp = _make_input(
            implementation_plan_provided_pct=0.46,
            features_promised_not_delivered_pct=0.05,
        )
        # But ctx: impl=0.46<=0.55 -> +22 -> composite=22*0.30=6.6 <30
        result = eng.assess(inp)
        assert result.requires_handoff_coaching is False

    def test_requires_coaching_via_features_ge_015(self):
        eng = _engine()
        inp = _make_input(features_promised_not_delivered_pct=0.15)
        result = eng.assess(inp)
        assert result.requires_handoff_coaching is True

    def test_no_coaching_features_just_below_015(self):
        eng = _engine()
        inp = _make_input(
            features_promised_not_delivered_pct=0.14,
            implementation_plan_provided_pct=0.90,  # >0.45
        )
        result = eng.assess(inp)
        # composite=0 (all good), impl>0.45, features<0.15 -> no coaching
        assert result.requires_handoff_coaching is False

    def test_no_coaching_when_all_clear(self):
        eng = _engine()
        result = eng.assess(_make_input())
        assert result.requires_handoff_coaching is False


# ---------------------------------------------------------------------------
# 13. Churn risk formula
# ---------------------------------------------------------------------------

class TestChurnRiskFormula:
    def test_churn_risk_formula(self):
        eng = _engine()
        inp = _make_input(
            total_deals_closed=20,
            avg_opportunity_value_usd=100_000.0,
            customer_expectation_alignment_rate_pct=0.75,
        )
        result = eng.assess(inp)
        expected = round(
            20 * 100_000.0 * (1.0 - 0.75) * (result.handoff_composite / 100.0),
            2,
        )
        assert result.estimated_churn_risk_usd == expected

    def test_churn_risk_zero_when_composite_zero(self):
        eng = _engine()
        result = eng.assess(_make_input())
        assert result.estimated_churn_risk_usd == 0.0

    def test_churn_risk_zero_when_alignment_is_one(self):
        eng = _engine()
        inp = _make_input(
            customer_expectation_alignment_rate_pct=1.0,
            total_deals_closed=50,
            avg_opportunity_value_usd=200_000.0,
        )
        result = eng.assess(inp)
        assert result.estimated_churn_risk_usd == 0.0

    def test_churn_risk_rounded_to_2_decimals(self):
        eng = _engine()
        inp = _make_input(
            total_deals_closed=3,
            avg_opportunity_value_usd=33_333.33,
            customer_expectation_alignment_rate_pct=0.33,
            implementation_plan_provided_pct=0.20,
            success_criteria_shared_with_cs_pct=0.90,
            deal_history_documented_pct=0.90,
        )
        result = eng.assess(inp)
        assert isinstance(result.estimated_churn_risk_usd, float)
        assert round(result.estimated_churn_risk_usd, 2) == result.estimated_churn_risk_usd

    def test_churn_risk_uses_correct_fields(self):
        eng = _engine()
        inp = _make_input(
            total_deals_closed=5,
            avg_opportunity_value_usd=10_000.0,
            customer_expectation_alignment_rate_pct=0.80,
            implementation_plan_provided_pct=0.20,   # ctx: +40 -> composite=12
        )
        result = eng.assess(inp)
        # composite=40*0.30=12.0
        expected = round(5 * 10_000.0 * (1.0 - 0.80) * (result.handoff_composite / 100.0), 2)
        assert result.estimated_churn_risk_usd == expected

    def test_churn_risk_smoke_test_high_risk(self):
        eng = _engine()
        inp = _make_input(
            total_deals_closed=100,
            avg_opportunity_value_usd=50_000.0,
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
        )
        result = eng.assess(inp)
        expected = round(100 * 50_000.0 * (1.0 - 0.50) * (result.handoff_composite / 100.0), 2)
        assert result.estimated_churn_risk_usd == expected

    def test_churn_risk_nonneg(self):
        eng = _engine()
        result = eng.assess(_make_input())
        assert result.estimated_churn_risk_usd >= 0.0


# ---------------------------------------------------------------------------
# 14. Signal string
# ---------------------------------------------------------------------------

class TestSignalString:
    def test_signal_strong_when_none_pattern_and_composite_lt_20(self):
        eng = _engine()
        result = eng.assess(_make_input())
        assert result.handoff_signal == (
            "Customer handoff quality strong — context transfer, expectation alignment, "
            "and post-sale continuity within benchmarks"
        )

    def test_signal_with_named_pattern(self):
        eng = _engine()
        inp = _make_input(
            features_promised_not_delivered_pct=0.20,
            customer_expectation_alignment_rate_pct=0.40,
        )
        result = eng.assess(inp)
        assert result.handoff_pattern == HandoffPattern.oversell_setup
        impl_pct = int(round(inp.implementation_plan_provided_pct * 100))
        align_pct = int(round(inp.customer_expectation_alignment_rate_pct * 100))
        onb_pct = int(round(inp.rep_involved_in_onboarding_pct * 100))
        assert result.handoff_signal.startswith("Oversell setup — ")
        assert f"{impl_pct}% provide implementation plan" in result.handoff_signal
        assert f"{align_pct}% expectation alignment rate" in result.handoff_signal
        assert f"{onb_pct}% rep involved in onboarding" in result.handoff_signal
        assert f"composite {result.handoff_composite:.0f}" in result.handoff_signal

    def test_signal_with_none_pattern_but_composite_ge_20(self):
        """pattern==none but composite>=20 -> non-strong signal with 'Handoff risk' label."""
        eng = _engine()
        # ctx=40, exp=22, con=25, tim=22 => composite=12+6.6+6.25+3.3=28.15 >= 20
        # No pattern: impl=0.45 (>0.25 no incomplete_context), alignment=0.65 (>0.45 no exp_mismatch)
        #             features<0.20 no oversell, rep_onb=0.40 >0.25 no ghosting, days=8<10 no late_timing
        inp = _make_input(
            implementation_plan_provided_pct=0.45,    # ctx: +22 (<=0.55>0.30)
            success_criteria_shared_with_cs_pct=0.36, # ctx: +18
            deal_history_documented_pct=0.90,
            customer_expectation_alignment_rate_pct=0.65,  # exp: +22 (but >0.45 no expectation_mismatch)
            features_promised_not_delivered_pct=0.05,      # no oversell
            time_to_first_value_slip_rate_pct=0.10,        # no expectation_mismatch slip
            rep_involved_in_onboarding_pct=0.40,           # con: +25, >0.25 no ghosting
            post_sale_check_in_rate_pct=0.90,
            escalations_requiring_rep_re_engagement_pct=0.05,
            days_between_close_and_handoff_avg=8.0,        # tim: +22, <10 no late_timing
            handoff_meeting_attended_pct=0.90,
            onboarding_start_delay_days_avg=2.0,
        )
        result = eng.assess(inp)
        assert result.handoff_pattern == HandoffPattern.none
        assert result.handoff_composite >= 20
        assert "Handoff risk" in result.handoff_signal
        assert "composite" in result.handoff_signal

    def test_signal_contains_implementation_pct(self):
        eng = _engine()
        inp = _make_input(
            features_promised_not_delivered_pct=0.30,
            customer_expectation_alignment_rate_pct=0.10,
            time_to_first_value_slip_rate_pct=0.80,
        )
        result = eng.assess(inp)
        if result.handoff_pattern != HandoffPattern.none or result.handoff_composite >= 20:
            assert "provide implementation plan" in result.handoff_signal

    def test_signal_contains_alignment_rate(self):
        eng = _engine()
        inp = _make_input(
            features_promised_not_delivered_pct=0.30,
            customer_expectation_alignment_rate_pct=0.10,
            time_to_first_value_slip_rate_pct=0.80,
        )
        result = eng.assess(inp)
        if result.handoff_pattern != HandoffPattern.none:
            assert "expectation alignment rate" in result.handoff_signal

    def test_signal_contains_rep_involved_pct(self):
        eng = _engine()
        inp = _make_input(
            features_promised_not_delivered_pct=0.30,
            customer_expectation_alignment_rate_pct=0.10,
            time_to_first_value_slip_rate_pct=0.80,
        )
        result = eng.assess(inp)
        if result.handoff_pattern != HandoffPattern.none:
            assert "rep involved in onboarding" in result.handoff_signal

    def test_signal_not_empty(self):
        eng = _engine()
        result = eng.assess(_make_input())
        assert len(result.handoff_signal) > 0

    def test_signal_pattern_label_capitalized(self):
        eng = _engine()
        inp = _make_input(
            features_promised_not_delivered_pct=0.20,
            customer_expectation_alignment_rate_pct=0.40,
        )
        result = eng.assess(inp)
        assert result.handoff_pattern == HandoffPattern.oversell_setup
        # "oversell setup".capitalize() = "Oversell setup"
        assert result.handoff_signal.startswith("Oversell setup")

    def test_signal_late_handoff_timing_label(self):
        eng = _engine()
        inp = _make_input(
            days_between_close_and_handoff_avg=14.0,
            handoff_meeting_attended_pct=0.90,
            onboarding_start_delay_days_avg=2.0,
            features_promised_not_delivered_pct=0.05,
            customer_expectation_alignment_rate_pct=0.90,
            time_to_first_value_slip_rate_pct=0.10,
            implementation_plan_provided_pct=0.90,
            rep_involved_in_onboarding_pct=0.85,
        )
        result = eng.assess(inp)
        if result.handoff_pattern == HandoffPattern.late_handoff_timing:
            assert result.handoff_signal.startswith("Late handoff timing")


# ---------------------------------------------------------------------------
# 15. assess() end-to-end
# ---------------------------------------------------------------------------

class TestAssessEndToEnd:
    def test_assess_returns_handoff_result(self):
        eng = _engine()
        result = eng.assess(_make_input())
        assert isinstance(result, HandoffResult)

    def test_assess_stores_result_in_results_list(self):
        eng = _engine()
        assert len(eng._results) == 0
        eng.assess(_make_input())
        assert len(eng._results) == 1
        eng.assess(_make_input())
        assert len(eng._results) == 2

    def test_assess_rep_id_passthrough(self):
        eng = _engine()
        inp = _make_input(rep_id="xyz-789", region="APAC")
        result = eng.assess(inp)
        assert result.rep_id == "xyz-789"
        assert result.region == "APAC"

    def test_assess_subscores_non_negative(self):
        eng = _engine()
        result = eng.assess(_make_input())
        assert result.context_score >= 0
        assert result.expectation_score >= 0
        assert result.continuity_score >= 0
        assert result.timing_score >= 0

    def test_assess_subscores_at_most_100(self):
        eng = _engine()
        inp = _make_input(
            implementation_plan_provided_pct=0.0,
            success_criteria_shared_with_cs_pct=0.0,
            deal_history_documented_pct=0.0,
            customer_expectation_alignment_rate_pct=0.0,
            features_promised_not_delivered_pct=1.0,
            time_to_first_value_slip_rate_pct=1.0,
            rep_involved_in_onboarding_pct=0.0,
            post_sale_check_in_rate_pct=0.0,
            escalations_requiring_rep_re_engagement_pct=1.0,
            days_between_close_and_handoff_avg=30.0,
            handoff_meeting_attended_pct=0.0,
            onboarding_start_delay_days_avg=60.0,
        )
        result = eng.assess(inp)
        assert result.context_score <= 100
        assert result.expectation_score <= 100
        assert result.continuity_score <= 100
        assert result.timing_score <= 100
        assert result.handoff_composite <= 100

    def test_assess_signal_not_empty(self):
        eng = _engine()
        result = eng.assess(_make_input())
        assert result.handoff_signal != ""


# ---------------------------------------------------------------------------
# 16. assess_batch()
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_assess_batch_returns_list_of_results(self):
        eng = _engine()
        inputs = [_make_input(rep_id=f"rep-{i}") for i in range(5)]
        results = eng.assess_batch(inputs)
        assert len(results) == 5
        assert all(isinstance(r, HandoffResult) for r in results)

    def test_assess_batch_preserves_order(self):
        eng = _engine()
        inputs = [_make_input(rep_id=f"rep-{i}") for i in range(3)]
        results = eng.assess_batch(inputs)
        for i, result in enumerate(results):
            assert result.rep_id == f"rep-{i}"

    def test_assess_batch_accumulates_in_results(self):
        eng = _engine()
        eng.assess_batch([_make_input()] * 7)
        assert len(eng._results) == 7

    def test_assess_batch_empty_list(self):
        eng = _engine()
        results = eng.assess_batch([])
        assert results == []

    def test_assess_batch_mixed_risk_levels(self):
        eng = _engine()
        low_inp = _make_input(rep_id="low")
        high_inp = _make_input(
            rep_id="high",
            implementation_plan_provided_pct=0.20,
            customer_expectation_alignment_rate_pct=0.40,
            rep_involved_in_onboarding_pct=0.40,
            post_sale_check_in_rate_pct=0.50,
            days_between_close_and_handoff_avg=14.0,
        )
        results = eng.assess_batch([low_inp, high_inp])
        assert results[0].rep_id == "low"
        assert results[1].rep_id == "high"


# ---------------------------------------------------------------------------
# 17. summary() — empty
# ---------------------------------------------------------------------------

class TestSummaryEmpty:
    def test_empty_summary_has_13_keys(self):
        eng = _engine()
        s = eng.summary()
        assert len(s) == 13

    def test_empty_summary_all_keys_present(self):
        eng = _engine()
        s = eng.summary()
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_handoff_composite", "handoff_gap_count",
            "coaching_count", "avg_context_score", "avg_expectation_score",
            "avg_continuity_score", "avg_timing_score",
            "total_estimated_churn_risk_usd",
        }
        assert set(s.keys()) == expected_keys

    def test_empty_summary_total_is_zero(self):
        eng = _engine()
        assert eng.summary()["total"] == 0

    def test_empty_summary_counts_are_empty_dicts(self):
        eng = _engine()
        s = eng.summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}

    def test_empty_summary_numeric_defaults_are_zero(self):
        eng = _engine()
        s = eng.summary()
        assert s["avg_handoff_composite"] == 0.0
        assert s["handoff_gap_count"] == 0
        assert s["coaching_count"] == 0
        assert s["avg_context_score"] == 0.0
        assert s["avg_expectation_score"] == 0.0
        assert s["avg_continuity_score"] == 0.0
        assert s["avg_timing_score"] == 0.0
        assert s["total_estimated_churn_risk_usd"] == 0.0


# ---------------------------------------------------------------------------
# 18. summary() — populated
# ---------------------------------------------------------------------------

class TestSummaryPopulated:
    def test_populated_summary_has_13_keys(self):
        eng = _engine()
        eng.assess(_make_input())
        s = eng.summary()
        assert len(s) == 13

    def test_populated_summary_all_keys(self):
        eng = _engine()
        eng.assess(_make_input())
        s = eng.summary()
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_handoff_composite", "handoff_gap_count",
            "coaching_count", "avg_context_score", "avg_expectation_score",
            "avg_continuity_score", "avg_timing_score",
            "total_estimated_churn_risk_usd",
        }
        assert set(s.keys()) == expected_keys

    def test_populated_summary_total_correct(self):
        eng = _engine()
        for i in range(6):
            eng.assess(_make_input(rep_id=f"rep-{i}"))
        assert eng.summary()["total"] == 6

    def test_populated_summary_risk_counts(self):
        eng = _engine()
        eng.assess(_make_input())  # low
        s = eng.summary()
        assert s["risk_counts"].get("low", 0) == 1
        assert sum(s["risk_counts"].values()) == 1

    def test_populated_summary_pattern_counts(self):
        eng = _engine()
        eng.assess(_make_input())  # none
        s = eng.summary()
        assert s["pattern_counts"].get("none", 0) == 1
        assert sum(s["pattern_counts"].values()) == 1

    def test_populated_summary_severity_counts(self):
        eng = _engine()
        eng.assess(_make_input())  # seamless
        s = eng.summary()
        assert s["severity_counts"].get("seamless", 0) == 1
        assert sum(s["severity_counts"].values()) == 1

    def test_populated_summary_action_counts(self):
        eng = _engine()
        eng.assess(_make_input())  # no_action
        s = eng.summary()
        assert s["action_counts"].get("no_action", 0) == 1
        assert sum(s["action_counts"].values()) == 1

    def test_populated_summary_avg_composite(self):
        eng = _engine()
        inp1 = _make_input()         # composite = 0.0
        inp2 = _make_input(
            implementation_plan_provided_pct=0.20,  # ctx: +40 -> composite=12
        )
        eng.assess_batch([inp1, inp2])
        s = eng.summary()
        r1 = eng._results[0]
        r2 = eng._results[1]
        expected_avg = round((r1.handoff_composite + r2.handoff_composite) / 2, 1)
        assert s["avg_handoff_composite"] == expected_avg

    def test_populated_summary_gap_count(self):
        eng = _engine()
        inp_gap = _make_input(customer_expectation_alignment_rate_pct=0.60)  # <=0.60 -> gap
        inp_no_gap = _make_input()
        eng.assess_batch([inp_gap, inp_no_gap])
        s = eng.summary()
        assert s["handoff_gap_count"] == 1

    def test_populated_summary_coaching_count(self):
        eng = _engine()
        inp_coach = _make_input(implementation_plan_provided_pct=0.45)  # <=0.45 -> coaching
        inp_no_coach = _make_input()
        eng.assess_batch([inp_coach, inp_no_coach])
        s = eng.summary()
        assert s["coaching_count"] == 1

    def test_populated_summary_avg_subscores(self):
        eng = _engine()
        inp1 = _make_input()
        inp2 = _make_input(implementation_plan_provided_pct=0.20)  # ctx = 40
        eng.assess_batch([inp1, inp2])
        s = eng.summary()
        r1, r2 = eng._results
        expected_ctx = round((r1.context_score + r2.context_score) / 2, 1)
        expected_exp = round((r1.expectation_score + r2.expectation_score) / 2, 1)
        expected_con = round((r1.continuity_score + r2.continuity_score) / 2, 1)
        expected_tim = round((r1.timing_score + r2.timing_score) / 2, 1)
        assert s["avg_context_score"] == expected_ctx
        assert s["avg_expectation_score"] == expected_exp
        assert s["avg_continuity_score"] == expected_con
        assert s["avg_timing_score"] == expected_tim

    def test_populated_summary_total_churn_risk(self):
        eng = _engine()
        inp1 = _make_input()
        inp2 = _make_input(implementation_plan_provided_pct=0.20)
        eng.assess_batch([inp1, inp2])
        s = eng.summary()
        expected = round(
            eng._results[0].estimated_churn_risk_usd
            + eng._results[1].estimated_churn_risk_usd,
            2,
        )
        assert s["total_estimated_churn_risk_usd"] == expected

    def test_summary_reflects_all_assessed_results(self):
        eng = _engine()
        inputs = [_make_input(rep_id=f"r{i}") for i in range(10)]
        eng.assess_batch(inputs)
        s = eng.summary()
        assert s["total"] == 10

    def test_summary_independent_per_engine_instance(self):
        eng1 = _engine()
        eng2 = _engine()
        eng1.assess(_make_input())
        assert eng1.summary()["total"] == 1
        assert eng2.summary()["total"] == 0

    def test_summary_multiple_risk_levels(self):
        eng = _engine()
        eng.assess(_make_input(rep_id="A"))  # low
        eng.assess(_make_input(
            rep_id="B",
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
        ))  # critical
        s = eng.summary()
        assert s["total"] == 2
        assert "low" in s["risk_counts"]
        assert "critical" in s["risk_counts"]
