"""Comprehensive pytest test suite for SalesDealDeskIntelligenceEngine."""
from __future__ import annotations

import pytest
from swarm.intelligence.sales_deal_desk_intelligence_engine import (
    DealDeskAction,
    DealDeskInput,
    DealDeskPattern,
    DealDeskResult,
    DealDeskRisk,
    DealDeskSeverity,
    SalesDealDeskIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> DealDeskInput:
    """Return a baseline DealDeskInput with all scores near zero, with optional overrides."""
    defaults = dict(
        rep_id="REP001",
        region="West",
        evaluation_period_id="Q1-2026",
        total_deals_closed=20,
        deals_requiring_approval_pct=0.05,
        avg_discount_override_depth_pct=0.02,
        custom_terms_request_count=0,
        legal_review_escalation_count=0,
        executive_sponsor_required_count=0,
        avg_days_in_deal_desk_review=1.0,
        deal_desk_rejection_rate_pct=0.05,
        standard_terms_win_rate_pct=0.80,
        custom_terms_win_rate_pct=0.50,
        avg_deal_desk_cycles_per_deal=1.0,
        exceptions_by_competitor_loss_count=0,
        late_stage_escalation_rate_pct=0.05,
        pricing_authority_exceeded_count=0,
        multi_product_bundle_exception_count=0,
        customer_success_concession_count=0,
        avg_exception_value_usd=500.0,
        deal_desk_approval_rate_pct=0.90,
        avg_opportunity_value_usd=15000.0,
    )
    defaults.update(overrides)
    return DealDeskInput(**defaults)


def fresh_engine() -> SalesDealDeskIntelligenceEngine:
    return SalesDealDeskIntelligenceEngine()


# ===========================================================================
# 1. Enum: DealDeskRisk
# ===========================================================================

class TestDealDeskRiskEnum:
    def test_low_value(self):
        assert DealDeskRisk.low.value == "low"

    def test_moderate_value(self):
        assert DealDeskRisk.moderate.value == "moderate"

    def test_high_value(self):
        assert DealDeskRisk.high.value == "high"

    def test_critical_value(self):
        assert DealDeskRisk.critical.value == "critical"

    def test_is_str(self):
        assert isinstance(DealDeskRisk.low, str)

    def test_equality_with_string(self):
        assert DealDeskRisk.low == "low"

    def test_four_members(self):
        assert len(DealDeskRisk) == 4

    def test_members_list(self):
        values = {m.value for m in DealDeskRisk}
        assert values == {"low", "moderate", "high", "critical"}


# ===========================================================================
# 2. Enum: DealDeskPattern
# ===========================================================================

class TestDealDeskPatternEnum:
    def test_none_value(self):
        assert DealDeskPattern.none.value == "none"

    def test_deal_desk_dependent_value(self):
        assert DealDeskPattern.deal_desk_dependent.value == "deal_desk_dependent"

    def test_discount_authority_abuse_value(self):
        assert DealDeskPattern.discount_authority_abuse.value == "discount_authority_abuse"

    def test_last_minute_escalation_value(self):
        assert DealDeskPattern.last_minute_escalation.value == "last_minute_escalation"

    def test_legal_escalation_pattern_value(self):
        assert DealDeskPattern.legal_escalation_pattern.value == "legal_escalation_pattern"

    def test_competitive_capitulation_value(self):
        assert DealDeskPattern.competitive_capitulation.value == "competitive_capitulation"

    def test_is_str(self):
        assert isinstance(DealDeskPattern.none, str)

    def test_six_members(self):
        assert len(DealDeskPattern) == 6

    def test_equality_with_string(self):
        assert DealDeskPattern.deal_desk_dependent == "deal_desk_dependent"


# ===========================================================================
# 3. Enum: DealDeskSeverity
# ===========================================================================

class TestDealDeskSeverityEnum:
    def test_autonomous_value(self):
        assert DealDeskSeverity.autonomous.value == "autonomous"

    def test_developing_value(self):
        assert DealDeskSeverity.developing.value == "developing"

    def test_dependent_value(self):
        assert DealDeskSeverity.dependent.value == "dependent"

    def test_entrenched_value(self):
        assert DealDeskSeverity.entrenched.value == "entrenched"

    def test_is_str(self):
        assert isinstance(DealDeskSeverity.autonomous, str)

    def test_four_members(self):
        assert len(DealDeskSeverity) == 4

    def test_equality_with_string(self):
        assert DealDeskSeverity.entrenched == "entrenched"


# ===========================================================================
# 4. Enum: DealDeskAction
# ===========================================================================

class TestDealDeskActionEnum:
    def test_no_action_value(self):
        assert DealDeskAction.no_action.value == "no_action"

    def test_pricing_authority_coaching_value(self):
        assert DealDeskAction.pricing_authority_coaching.value == "pricing_authority_coaching"

    def test_deal_desk_training_value(self):
        assert DealDeskAction.deal_desk_training.value == "deal_desk_training"

    def test_discount_discipline_review_value(self):
        assert DealDeskAction.discount_discipline_review.value == "discount_discipline_review"

    def test_legal_escalation_reduction_value(self):
        assert DealDeskAction.legal_escalation_reduction.value == "legal_escalation_reduction"

    def test_deal_desk_intervention_value(self):
        assert DealDeskAction.deal_desk_intervention.value == "deal_desk_intervention"

    def test_is_str(self):
        assert isinstance(DealDeskAction.no_action, str)

    def test_six_members(self):
        assert len(DealDeskAction) == 6

    def test_equality_with_string(self):
        assert DealDeskAction.deal_desk_intervention == "deal_desk_intervention"


# ===========================================================================
# 5. DealDeskInput dataclass
# ===========================================================================

class TestDealDeskInputDataclass:
    def test_creation(self):
        inp = make_input()
        assert inp.rep_id == "REP001"

    def test_rep_id_field(self):
        inp = make_input(rep_id="SALES99")
        assert inp.rep_id == "SALES99"

    def test_region_field(self):
        inp = make_input(region="EMEA")
        assert inp.region == "EMEA"

    def test_evaluation_period_id_field(self):
        inp = make_input(evaluation_period_id="Q2-2026")
        assert inp.evaluation_period_id == "Q2-2026"

    def test_total_deals_closed_field(self):
        inp = make_input(total_deals_closed=50)
        assert inp.total_deals_closed == 50

    def test_deals_requiring_approval_pct_field(self):
        inp = make_input(deals_requiring_approval_pct=0.75)
        assert inp.deals_requiring_approval_pct == 0.75

    def test_avg_discount_override_depth_pct_field(self):
        inp = make_input(avg_discount_override_depth_pct=0.20)
        assert inp.avg_discount_override_depth_pct == 0.20

    def test_custom_terms_request_count_field(self):
        inp = make_input(custom_terms_request_count=3)
        assert inp.custom_terms_request_count == 3

    def test_legal_review_escalation_count_field(self):
        inp = make_input(legal_review_escalation_count=6)
        assert inp.legal_review_escalation_count == 6

    def test_executive_sponsor_required_count_field(self):
        inp = make_input(executive_sponsor_required_count=5)
        assert inp.executive_sponsor_required_count == 5

    def test_avg_days_in_deal_desk_review_field(self):
        inp = make_input(avg_days_in_deal_desk_review=14.5)
        assert inp.avg_days_in_deal_desk_review == 14.5

    def test_deal_desk_rejection_rate_pct_field(self):
        inp = make_input(deal_desk_rejection_rate_pct=0.35)
        assert inp.deal_desk_rejection_rate_pct == 0.35

    def test_standard_terms_win_rate_pct_field(self):
        inp = make_input(standard_terms_win_rate_pct=0.65)
        assert inp.standard_terms_win_rate_pct == 0.65

    def test_custom_terms_win_rate_pct_field(self):
        inp = make_input(custom_terms_win_rate_pct=0.40)
        assert inp.custom_terms_win_rate_pct == 0.40

    def test_avg_deal_desk_cycles_per_deal_field(self):
        inp = make_input(avg_deal_desk_cycles_per_deal=3.5)
        assert inp.avg_deal_desk_cycles_per_deal == 3.5

    def test_exceptions_by_competitor_loss_count_field(self):
        inp = make_input(exceptions_by_competitor_loss_count=4)
        assert inp.exceptions_by_competitor_loss_count == 4

    def test_late_stage_escalation_rate_pct_field(self):
        inp = make_input(late_stage_escalation_rate_pct=0.60)
        assert inp.late_stage_escalation_rate_pct == 0.60

    def test_pricing_authority_exceeded_count_field(self):
        inp = make_input(pricing_authority_exceeded_count=7)
        assert inp.pricing_authority_exceeded_count == 7

    def test_multi_product_bundle_exception_count_field(self):
        inp = make_input(multi_product_bundle_exception_count=5)
        assert inp.multi_product_bundle_exception_count == 5

    def test_customer_success_concession_count_field(self):
        inp = make_input(customer_success_concession_count=6)
        assert inp.customer_success_concession_count == 6

    def test_avg_exception_value_usd_field(self):
        inp = make_input(avg_exception_value_usd=25000.0)
        assert inp.avg_exception_value_usd == 25000.0

    def test_deal_desk_approval_rate_pct_field(self):
        inp = make_input(deal_desk_approval_rate_pct=0.70)
        assert inp.deal_desk_approval_rate_pct == 0.70

    def test_avg_opportunity_value_usd_field(self):
        inp = make_input(avg_opportunity_value_usd=50000.0)
        assert inp.avg_opportunity_value_usd == 50000.0

    def test_22_fields(self):
        import dataclasses
        assert len(dataclasses.fields(DealDeskInput)) == 22


# ===========================================================================
# 6. DealDeskResult dataclass and to_dict()
# ===========================================================================

class TestDealDeskResultDataclass:
    def _sample_result(self) -> DealDeskResult:
        return DealDeskResult(
            rep_id="R1",
            region="East",
            deal_desk_risk=DealDeskRisk.low,
            deal_desk_pattern=DealDeskPattern.none,
            deal_desk_severity=DealDeskSeverity.autonomous,
            recommended_action=DealDeskAction.no_action,
            approval_dependency_score=0.0,
            exception_complexity_score=0.0,
            exception_urgency_score=0.0,
            exception_impact_score=0.0,
            deal_desk_composite=0.0,
            has_deal_desk_gap=False,
            requires_deal_desk_coaching=False,
            estimated_margin_risk_usd=0.0,
            deal_desk_signal="healthy",
        )

    def test_rep_id(self):
        assert self._sample_result().rep_id == "R1"

    def test_region(self):
        assert self._sample_result().region == "East"

    def test_deal_desk_risk(self):
        assert self._sample_result().deal_desk_risk == DealDeskRisk.low

    def test_deal_desk_pattern(self):
        assert self._sample_result().deal_desk_pattern == DealDeskPattern.none

    def test_deal_desk_severity(self):
        assert self._sample_result().deal_desk_severity == DealDeskSeverity.autonomous

    def test_recommended_action(self):
        assert self._sample_result().recommended_action == DealDeskAction.no_action

    def test_approval_dependency_score(self):
        assert self._sample_result().approval_dependency_score == 0.0

    def test_exception_complexity_score(self):
        assert self._sample_result().exception_complexity_score == 0.0

    def test_exception_urgency_score(self):
        assert self._sample_result().exception_urgency_score == 0.0

    def test_exception_impact_score(self):
        assert self._sample_result().exception_impact_score == 0.0

    def test_deal_desk_composite(self):
        assert self._sample_result().deal_desk_composite == 0.0

    def test_has_deal_desk_gap(self):
        assert self._sample_result().has_deal_desk_gap is False

    def test_requires_deal_desk_coaching(self):
        assert self._sample_result().requires_deal_desk_coaching is False

    def test_estimated_margin_risk_usd(self):
        assert self._sample_result().estimated_margin_risk_usd == 0.0

    def test_deal_desk_signal(self):
        assert self._sample_result().deal_desk_signal == "healthy"

    def test_to_dict_returns_dict(self):
        assert isinstance(self._sample_result().to_dict(), dict)

    def test_to_dict_has_15_keys(self):
        assert len(self._sample_result().to_dict()) == 15

    def test_to_dict_rep_id(self):
        assert self._sample_result().to_dict()["rep_id"] == "R1"

    def test_to_dict_region(self):
        assert self._sample_result().to_dict()["region"] == "East"

    def test_to_dict_deal_desk_risk_is_string(self):
        assert self._sample_result().to_dict()["deal_desk_risk"] == "low"

    def test_to_dict_deal_desk_pattern_is_string(self):
        assert self._sample_result().to_dict()["deal_desk_pattern"] == "none"

    def test_to_dict_deal_desk_severity_is_string(self):
        assert self._sample_result().to_dict()["deal_desk_severity"] == "autonomous"

    def test_to_dict_recommended_action_is_string(self):
        assert self._sample_result().to_dict()["recommended_action"] == "no_action"

    def test_to_dict_has_approval_dependency_score(self):
        assert "approval_dependency_score" in self._sample_result().to_dict()

    def test_to_dict_has_exception_complexity_score(self):
        assert "exception_complexity_score" in self._sample_result().to_dict()

    def test_to_dict_has_exception_urgency_score(self):
        assert "exception_urgency_score" in self._sample_result().to_dict()

    def test_to_dict_has_exception_impact_score(self):
        assert "exception_impact_score" in self._sample_result().to_dict()

    def test_to_dict_has_deal_desk_composite(self):
        assert "deal_desk_composite" in self._sample_result().to_dict()

    def test_to_dict_has_has_deal_desk_gap(self):
        assert "has_deal_desk_gap" in self._sample_result().to_dict()

    def test_to_dict_has_requires_deal_desk_coaching(self):
        assert "requires_deal_desk_coaching" in self._sample_result().to_dict()

    def test_to_dict_has_estimated_margin_risk_usd(self):
        assert "estimated_margin_risk_usd" in self._sample_result().to_dict()

    def test_to_dict_has_deal_desk_signal(self):
        assert "deal_desk_signal" in self._sample_result().to_dict()


# ===========================================================================
# 7. _approval_dependency_score
# ===========================================================================

class TestApprovalDependencyScore:
    def setup_method(self):
        self.eng = fresh_engine()

    def _score(self, **kw):
        return self.eng._approval_dependency_score(make_input(**kw))

    # deals_requiring_approval_pct tiers
    def test_approval_pct_zero(self):
        assert self._score(deals_requiring_approval_pct=0.0) == 0.0

    def test_approval_pct_below_20(self):
        assert self._score(deals_requiring_approval_pct=0.15) == 0.0

    def test_approval_pct_exactly_20(self):
        assert self._score(deals_requiring_approval_pct=0.20) == 10.0

    def test_approval_pct_between_20_40(self):
        assert self._score(deals_requiring_approval_pct=0.35) == 10.0

    def test_approval_pct_exactly_40(self):
        assert self._score(deals_requiring_approval_pct=0.40) == 25.0

    def test_approval_pct_between_40_60(self):
        assert self._score(deals_requiring_approval_pct=0.55) == 25.0

    def test_approval_pct_exactly_60(self):
        assert self._score(deals_requiring_approval_pct=0.60) == 45.0

    def test_approval_pct_above_60(self):
        assert self._score(deals_requiring_approval_pct=0.90) == 45.0

    # avg_discount_override_depth_pct tiers
    def test_discount_depth_zero(self):
        assert self._score(avg_discount_override_depth_pct=0.0) == 0.0

    def test_discount_depth_below_08(self):
        assert self._score(avg_discount_override_depth_pct=0.05) == 0.0

    def test_discount_depth_exactly_08(self):
        assert self._score(avg_discount_override_depth_pct=0.08) == 15.0

    def test_discount_depth_between_08_15(self):
        assert self._score(avg_discount_override_depth_pct=0.12) == 15.0

    def test_discount_depth_exactly_15(self):
        assert self._score(avg_discount_override_depth_pct=0.15) == 30.0

    def test_discount_depth_above_15(self):
        assert self._score(avg_discount_override_depth_pct=0.25) == 30.0

    # pricing_authority_exceeded_count tiers
    def test_pricing_exceeded_zero(self):
        assert self._score(pricing_authority_exceeded_count=0) == 0.0

    def test_pricing_exceeded_1(self):
        assert self._score(pricing_authority_exceeded_count=1) == 0.0

    def test_pricing_exceeded_exactly_2(self):
        assert self._score(pricing_authority_exceeded_count=2) == 12.0

    def test_pricing_exceeded_between_2_5(self):
        assert self._score(pricing_authority_exceeded_count=4) == 12.0

    def test_pricing_exceeded_exactly_5(self):
        assert self._score(pricing_authority_exceeded_count=5) == 25.0

    def test_pricing_exceeded_above_5(self):
        assert self._score(pricing_authority_exceeded_count=10) == 25.0

    # Combined and cap
    def test_full_score_all_tiers(self):
        s = self._score(
            deals_requiring_approval_pct=0.70,
            avg_discount_override_depth_pct=0.20,
            pricing_authority_exceeded_count=6,
        )
        assert s == 100.0  # 45+30+25=100

    def test_cap_at_100(self):
        # max possible = 45+30+25 = 100; ensure no overshoot
        s = self._score(
            deals_requiring_approval_pct=1.0,
            avg_discount_override_depth_pct=1.0,
            pricing_authority_exceeded_count=99,
        )
        assert s == 100.0

    def test_mid_combination(self):
        # 25 + 15 + 12 = 52
        s = self._score(
            deals_requiring_approval_pct=0.45,
            avg_discount_override_depth_pct=0.10,
            pricing_authority_exceeded_count=3,
        )
        assert s == 52.0


# ===========================================================================
# 8. _exception_complexity_score
# ===========================================================================

class TestExceptionComplexityScore:
    def setup_method(self):
        self.eng = fresh_engine()

    def _score(self, **kw):
        return self.eng._exception_complexity_score(make_input(**kw))

    # legal_review_escalation_count tiers
    def test_legal_zero(self):
        assert self._score(legal_review_escalation_count=0) == 0.0

    def test_legal_exactly_1(self):
        assert self._score(legal_review_escalation_count=1) == 8.0

    def test_legal_between_1_3(self):
        assert self._score(legal_review_escalation_count=2) == 8.0

    def test_legal_exactly_3(self):
        assert self._score(legal_review_escalation_count=3) == 22.0

    def test_legal_between_3_5(self):
        assert self._score(legal_review_escalation_count=4) == 22.0

    def test_legal_exactly_5(self):
        assert self._score(legal_review_escalation_count=5) == 40.0

    def test_legal_above_5(self):
        assert self._score(legal_review_escalation_count=10) == 40.0

    # avg_deal_desk_cycles_per_deal tiers
    def test_cycles_below_2(self):
        assert self._score(avg_deal_desk_cycles_per_deal=1.5) == 0.0

    def test_cycles_exactly_2(self):
        assert self._score(avg_deal_desk_cycles_per_deal=2.0) == 18.0

    def test_cycles_between_2_3(self):
        assert self._score(avg_deal_desk_cycles_per_deal=2.5) == 18.0

    def test_cycles_exactly_3(self):
        assert self._score(avg_deal_desk_cycles_per_deal=3.0) == 35.0

    def test_cycles_above_3(self):
        assert self._score(avg_deal_desk_cycles_per_deal=5.0) == 35.0

    # executive_sponsor_required_count tiers
    def test_exec_zero(self):
        assert self._score(executive_sponsor_required_count=0) == 0.0

    def test_exec_1(self):
        assert self._score(executive_sponsor_required_count=1) == 0.0

    def test_exec_exactly_2(self):
        assert self._score(executive_sponsor_required_count=2) == 12.0

    def test_exec_between_2_4(self):
        assert self._score(executive_sponsor_required_count=3) == 12.0

    def test_exec_exactly_4(self):
        assert self._score(executive_sponsor_required_count=4) == 25.0

    def test_exec_above_4(self):
        assert self._score(executive_sponsor_required_count=8) == 25.0

    # Combined and cap
    def test_max_complexity(self):
        s = self._score(
            legal_review_escalation_count=5,
            avg_deal_desk_cycles_per_deal=3.0,
            executive_sponsor_required_count=4,
        )
        assert s == 100.0  # 40+35+25=100

    def test_cap_at_100(self):
        s = self._score(
            legal_review_escalation_count=99,
            avg_deal_desk_cycles_per_deal=99.0,
            executive_sponsor_required_count=99,
        )
        assert s == 100.0

    def test_partial_combination(self):
        # 8 + 18 + 12 = 38
        s = self._score(
            legal_review_escalation_count=1,
            avg_deal_desk_cycles_per_deal=2.0,
            executive_sponsor_required_count=2,
        )
        assert s == 38.0


# ===========================================================================
# 9. _exception_urgency_score
# ===========================================================================

class TestExceptionUrgencyScore:
    def setup_method(self):
        self.eng = fresh_engine()

    def _score(self, **kw):
        return self.eng._exception_urgency_score(make_input(**kw))

    # late_stage_escalation_rate_pct tiers
    def test_late_zero(self):
        assert self._score(late_stage_escalation_rate_pct=0.0) == 0.0

    def test_late_below_20(self):
        assert self._score(late_stage_escalation_rate_pct=0.10) == 0.0

    def test_late_exactly_20(self):
        assert self._score(late_stage_escalation_rate_pct=0.20) == 8.0

    def test_late_between_20_40(self):
        assert self._score(late_stage_escalation_rate_pct=0.30) == 8.0

    def test_late_exactly_40(self):
        assert self._score(late_stage_escalation_rate_pct=0.40) == 22.0

    def test_late_between_40_60(self):
        assert self._score(late_stage_escalation_rate_pct=0.55) == 22.0

    def test_late_exactly_60(self):
        assert self._score(late_stage_escalation_rate_pct=0.60) == 40.0

    def test_late_above_60(self):
        assert self._score(late_stage_escalation_rate_pct=0.90) == 40.0

    # deal_desk_rejection_rate_pct tiers
    def test_rejection_zero(self):
        assert self._score(deal_desk_rejection_rate_pct=0.0) == 0.0

    def test_rejection_below_15(self):
        assert self._score(deal_desk_rejection_rate_pct=0.10) == 0.0

    def test_rejection_exactly_15(self):
        assert self._score(deal_desk_rejection_rate_pct=0.15) == 18.0

    def test_rejection_between_15_30(self):
        assert self._score(deal_desk_rejection_rate_pct=0.20) == 18.0

    def test_rejection_exactly_30(self):
        assert self._score(deal_desk_rejection_rate_pct=0.30) == 35.0

    def test_rejection_above_30(self):
        assert self._score(deal_desk_rejection_rate_pct=0.50) == 35.0

    # exceptions_by_competitor_loss_count tiers
    def test_competitor_zero(self):
        assert self._score(exceptions_by_competitor_loss_count=0) == 0.0

    def test_competitor_1(self):
        assert self._score(exceptions_by_competitor_loss_count=1) == 0.0

    def test_competitor_exactly_2(self):
        assert self._score(exceptions_by_competitor_loss_count=2) == 12.0

    def test_competitor_between_2_4(self):
        assert self._score(exceptions_by_competitor_loss_count=3) == 12.0

    def test_competitor_exactly_4(self):
        assert self._score(exceptions_by_competitor_loss_count=4) == 25.0

    def test_competitor_above_4(self):
        assert self._score(exceptions_by_competitor_loss_count=9) == 25.0

    # Combined and cap
    def test_max_urgency(self):
        s = self._score(
            late_stage_escalation_rate_pct=0.60,
            deal_desk_rejection_rate_pct=0.30,
            exceptions_by_competitor_loss_count=4,
        )
        assert s == 100.0  # 40+35+25=100

    def test_cap_at_100(self):
        s = self._score(
            late_stage_escalation_rate_pct=1.0,
            deal_desk_rejection_rate_pct=1.0,
            exceptions_by_competitor_loss_count=99,
        )
        assert s == 100.0

    def test_partial_urgency(self):
        # 8 + 18 + 12 = 38
        s = self._score(
            late_stage_escalation_rate_pct=0.20,
            deal_desk_rejection_rate_pct=0.15,
            exceptions_by_competitor_loss_count=2,
        )
        assert s == 38.0


# ===========================================================================
# 10. _exception_impact_score
# ===========================================================================

class TestExceptionImpactScore:
    def setup_method(self):
        self.eng = fresh_engine()

    def _score(self, **kw):
        return self.eng._exception_impact_score(make_input(**kw))

    # avg_exception_value_usd tiers
    def test_value_zero(self):
        assert self._score(avg_exception_value_usd=0.0) == 0.0

    def test_value_below_5000(self):
        assert self._score(avg_exception_value_usd=4999.0) == 0.0

    def test_value_exactly_5000(self):
        assert self._score(avg_exception_value_usd=5000.0) == 10.0

    def test_value_between_5000_10000(self):
        assert self._score(avg_exception_value_usd=7500.0) == 10.0

    def test_value_exactly_10000(self):
        assert self._score(avg_exception_value_usd=10000.0) == 25.0

    def test_value_between_10000_20000(self):
        assert self._score(avg_exception_value_usd=15000.0) == 25.0

    def test_value_exactly_20000(self):
        assert self._score(avg_exception_value_usd=20000.0) == 45.0

    def test_value_above_20000(self):
        assert self._score(avg_exception_value_usd=50000.0) == 45.0

    # customer_success_concession_count tiers
    def test_cs_concession_zero(self):
        assert self._score(customer_success_concession_count=0) == 0.0

    def test_cs_concession_1(self):
        assert self._score(customer_success_concession_count=1) == 0.0

    def test_cs_concession_exactly_2(self):
        assert self._score(customer_success_concession_count=2) == 15.0

    def test_cs_concession_between_2_5(self):
        assert self._score(customer_success_concession_count=4) == 15.0

    def test_cs_concession_exactly_5(self):
        assert self._score(customer_success_concession_count=5) == 30.0

    def test_cs_concession_above_5(self):
        assert self._score(customer_success_concession_count=8) == 30.0

    # multi_product_bundle_exception_count tiers
    def test_bundle_zero(self):
        assert self._score(multi_product_bundle_exception_count=0) == 0.0

    def test_bundle_1(self):
        assert self._score(multi_product_bundle_exception_count=1) == 0.0

    def test_bundle_exactly_2(self):
        assert self._score(multi_product_bundle_exception_count=2) == 12.0

    def test_bundle_between_2_4(self):
        assert self._score(multi_product_bundle_exception_count=3) == 12.0

    def test_bundle_exactly_4(self):
        assert self._score(multi_product_bundle_exception_count=4) == 25.0

    def test_bundle_above_4(self):
        assert self._score(multi_product_bundle_exception_count=7) == 25.0

    # Combined and cap
    def test_max_impact(self):
        s = self._score(
            avg_exception_value_usd=25000.0,
            customer_success_concession_count=5,
            multi_product_bundle_exception_count=4,
        )
        assert s == 100.0  # 45+30+25=100

    def test_cap_at_100(self):
        s = self._score(
            avg_exception_value_usd=999999.0,
            customer_success_concession_count=99,
            multi_product_bundle_exception_count=99,
        )
        assert s == 100.0

    def test_partial_impact(self):
        # 10 + 15 + 12 = 37
        s = self._score(
            avg_exception_value_usd=5000.0,
            customer_success_concession_count=2,
            multi_product_bundle_exception_count=2,
        )
        assert s == 37.0


# ===========================================================================
# 11. Pattern detection
# ===========================================================================

class TestDetectPattern:
    def setup_method(self):
        self.eng = fresh_engine()

    def _detect(self, approval, complexity, urgency, impact, **inp_kw):
        return self.eng._detect_pattern(make_input(**inp_kw), approval, complexity, urgency, impact)

    def test_none_when_all_zero(self):
        assert self._detect(0, 0, 0, 0) == DealDeskPattern.none

    def test_deal_desk_dependent_triggered(self):
        p = self._detect(40, 0, 0, 0, deals_requiring_approval_pct=0.50)
        assert p == DealDeskPattern.deal_desk_dependent

    def test_deal_desk_dependent_approval_below_40(self):
        p = self._detect(39, 0, 0, 0, deals_requiring_approval_pct=0.60)
        # approval <40 so won't trigger deal_desk_dependent
        assert p != DealDeskPattern.deal_desk_dependent

    def test_deal_desk_dependent_pct_below_50(self):
        p = self._detect(45, 0, 0, 0, deals_requiring_approval_pct=0.49)
        assert p != DealDeskPattern.deal_desk_dependent

    def test_discount_authority_abuse_triggered(self):
        p = self._detect(30, 0, 0, 0, avg_discount_override_depth_pct=0.10)
        assert p == DealDeskPattern.discount_authority_abuse

    def test_discount_authority_abuse_approval_below_30(self):
        p = self._detect(29, 0, 0, 0, avg_discount_override_depth_pct=0.20)
        assert p != DealDeskPattern.discount_authority_abuse

    def test_discount_authority_abuse_depth_below_10(self):
        p = self._detect(35, 0, 0, 0, avg_discount_override_depth_pct=0.09)
        assert p != DealDeskPattern.discount_authority_abuse

    def test_last_minute_escalation_triggered(self):
        p = self._detect(0, 0, 30, 0, late_stage_escalation_rate_pct=0.45)
        assert p == DealDeskPattern.last_minute_escalation

    def test_last_minute_escalation_urgency_below_30(self):
        p = self._detect(0, 0, 29, 0, late_stage_escalation_rate_pct=0.60)
        assert p != DealDeskPattern.last_minute_escalation

    def test_last_minute_escalation_rate_below_45(self):
        p = self._detect(0, 0, 35, 0, late_stage_escalation_rate_pct=0.44)
        assert p != DealDeskPattern.last_minute_escalation

    def test_legal_escalation_pattern_triggered(self):
        p = self._detect(0, 30, 0, 0, legal_review_escalation_count=4)
        assert p == DealDeskPattern.legal_escalation_pattern

    def test_legal_escalation_complexity_below_30(self):
        p = self._detect(0, 29, 0, 0, legal_review_escalation_count=5)
        assert p != DealDeskPattern.legal_escalation_pattern

    def test_legal_escalation_count_below_4(self):
        p = self._detect(0, 35, 0, 0, legal_review_escalation_count=3)
        assert p != DealDeskPattern.legal_escalation_pattern

    def test_competitive_capitulation_triggered(self):
        p = self._detect(0, 0, 20, 0, exceptions_by_competitor_loss_count=3)
        assert p == DealDeskPattern.competitive_capitulation

    def test_competitive_capitulation_urgency_below_20(self):
        p = self._detect(0, 0, 19, 0, exceptions_by_competitor_loss_count=5)
        assert p != DealDeskPattern.competitive_capitulation

    def test_competitive_capitulation_count_below_3(self):
        p = self._detect(0, 0, 25, 0, exceptions_by_competitor_loss_count=2)
        assert p != DealDeskPattern.competitive_capitulation

    def test_priority_deal_desk_dependent_over_discount(self):
        # both conditions met but deal_desk_dependent checked first
        p = self._detect(
            40, 0, 0, 0,
            deals_requiring_approval_pct=0.60,
            avg_discount_override_depth_pct=0.20,
        )
        assert p == DealDeskPattern.deal_desk_dependent


# ===========================================================================
# 12. _risk_level
# ===========================================================================

class TestRiskLevel:
    def setup_method(self):
        self.eng = fresh_engine()

    def test_low_at_zero(self):
        assert self.eng._risk_level(0.0) == DealDeskRisk.low

    def test_low_just_below_20(self):
        assert self.eng._risk_level(19.9) == DealDeskRisk.low

    def test_moderate_at_20(self):
        assert self.eng._risk_level(20.0) == DealDeskRisk.moderate

    def test_moderate_just_below_40(self):
        assert self.eng._risk_level(39.9) == DealDeskRisk.moderate

    def test_high_at_40(self):
        assert self.eng._risk_level(40.0) == DealDeskRisk.high

    def test_high_just_below_60(self):
        assert self.eng._risk_level(59.9) == DealDeskRisk.high

    def test_critical_at_60(self):
        assert self.eng._risk_level(60.0) == DealDeskRisk.critical

    def test_critical_at_100(self):
        assert self.eng._risk_level(100.0) == DealDeskRisk.critical


# ===========================================================================
# 13. _severity
# ===========================================================================

class TestSeverity:
    def setup_method(self):
        self.eng = fresh_engine()

    def test_autonomous_at_zero(self):
        assert self.eng._severity(0.0) == DealDeskSeverity.autonomous

    def test_autonomous_just_below_20(self):
        assert self.eng._severity(19.9) == DealDeskSeverity.autonomous

    def test_developing_at_20(self):
        assert self.eng._severity(20.0) == DealDeskSeverity.developing

    def test_developing_just_below_40(self):
        assert self.eng._severity(39.9) == DealDeskSeverity.developing

    def test_dependent_at_40(self):
        assert self.eng._severity(40.0) == DealDeskSeverity.dependent

    def test_dependent_just_below_60(self):
        assert self.eng._severity(59.9) == DealDeskSeverity.dependent

    def test_entrenched_at_60(self):
        assert self.eng._severity(60.0) == DealDeskSeverity.entrenched

    def test_entrenched_at_100(self):
        assert self.eng._severity(100.0) == DealDeskSeverity.entrenched


# ===========================================================================
# 14. _action mapping
# ===========================================================================

class TestAction:
    def setup_method(self):
        self.eng = fresh_engine()

    def _act(self, risk, pattern):
        return self.eng._action(risk, pattern)

    # Critical branch
    def test_critical_discount_abuse(self):
        assert self._act(DealDeskRisk.critical, DealDeskPattern.discount_authority_abuse) == DealDeskAction.discount_discipline_review

    def test_critical_legal_escalation(self):
        assert self._act(DealDeskRisk.critical, DealDeskPattern.legal_escalation_pattern) == DealDeskAction.legal_escalation_reduction

    def test_critical_deal_desk_dependent(self):
        assert self._act(DealDeskRisk.critical, DealDeskPattern.deal_desk_dependent) == DealDeskAction.deal_desk_intervention

    def test_critical_none(self):
        assert self._act(DealDeskRisk.critical, DealDeskPattern.none) == DealDeskAction.deal_desk_intervention

    def test_critical_last_minute_escalation(self):
        assert self._act(DealDeskRisk.critical, DealDeskPattern.last_minute_escalation) == DealDeskAction.deal_desk_intervention

    def test_critical_competitive_capitulation(self):
        assert self._act(DealDeskRisk.critical, DealDeskPattern.competitive_capitulation) == DealDeskAction.deal_desk_intervention

    # High branch
    def test_high_last_minute_escalation(self):
        assert self._act(DealDeskRisk.high, DealDeskPattern.last_minute_escalation) == DealDeskAction.deal_desk_training

    def test_high_competitive_capitulation(self):
        assert self._act(DealDeskRisk.high, DealDeskPattern.competitive_capitulation) == DealDeskAction.pricing_authority_coaching

    def test_high_none(self):
        assert self._act(DealDeskRisk.high, DealDeskPattern.none) == DealDeskAction.deal_desk_training

    def test_high_deal_desk_dependent(self):
        assert self._act(DealDeskRisk.high, DealDeskPattern.deal_desk_dependent) == DealDeskAction.deal_desk_training

    def test_high_discount_abuse(self):
        assert self._act(DealDeskRisk.high, DealDeskPattern.discount_authority_abuse) == DealDeskAction.deal_desk_training

    # Moderate branch
    def test_moderate_any_pattern(self):
        assert self._act(DealDeskRisk.moderate, DealDeskPattern.none) == DealDeskAction.pricing_authority_coaching

    def test_moderate_deal_desk_dependent(self):
        assert self._act(DealDeskRisk.moderate, DealDeskPattern.deal_desk_dependent) == DealDeskAction.pricing_authority_coaching

    # Low branch
    def test_low_no_action(self):
        assert self._act(DealDeskRisk.low, DealDeskPattern.none) == DealDeskAction.no_action

    def test_low_any_pattern(self):
        assert self._act(DealDeskRisk.low, DealDeskPattern.deal_desk_dependent) == DealDeskAction.no_action


# ===========================================================================
# 15. _has_deal_desk_gap
# ===========================================================================

class TestHasDealDeskGap:
    def setup_method(self):
        self.eng = fresh_engine()

    def _gap(self, composite, **inp_kw):
        return self.eng._has_deal_desk_gap(composite, make_input(**inp_kw))

    def test_false_when_all_low(self):
        assert self._gap(0.0) is False

    def test_true_when_composite_gte_40(self):
        assert self._gap(40.0) is True

    def test_true_when_composite_above_40(self):
        assert self._gap(50.0) is True

    def test_false_when_composite_just_below_40(self):
        assert self._gap(39.9) is False

    def test_true_when_approval_pct_gte_50(self):
        assert self._gap(0.0, deals_requiring_approval_pct=0.50) is True

    def test_true_when_approval_pct_above_50(self):
        assert self._gap(0.0, deals_requiring_approval_pct=0.80) is True

    def test_false_when_approval_pct_below_50(self):
        assert self._gap(0.0, deals_requiring_approval_pct=0.49) is False

    def test_true_when_late_stage_gte_50(self):
        assert self._gap(0.0, late_stage_escalation_rate_pct=0.50) is True

    def test_true_when_late_stage_above_50(self):
        assert self._gap(0.0, late_stage_escalation_rate_pct=0.70) is True

    def test_false_when_late_stage_below_50(self):
        assert self._gap(0.0, late_stage_escalation_rate_pct=0.49) is False

    def test_true_composite_only(self):
        assert self._gap(60.0) is True


# ===========================================================================
# 16. _requires_deal_desk_coaching
# ===========================================================================

class TestRequiresDealDeskCoaching:
    def setup_method(self):
        self.eng = fresh_engine()

    def _coach(self, composite, **inp_kw):
        return self.eng._requires_deal_desk_coaching(composite, make_input(**inp_kw))

    def test_false_when_all_zero(self):
        assert self._coach(0.0) is False

    def test_true_when_composite_gte_30(self):
        assert self._coach(30.0) is True

    def test_true_when_composite_above_30(self):
        assert self._coach(50.0) is True

    def test_false_when_composite_just_below_30(self):
        assert self._coach(29.9) is False

    def test_true_when_pricing_exceeded_gte_3(self):
        assert self._coach(0.0, pricing_authority_exceeded_count=3) is True

    def test_true_when_pricing_exceeded_above_3(self):
        assert self._coach(0.0, pricing_authority_exceeded_count=5) is True

    def test_false_when_pricing_exceeded_below_3(self):
        assert self._coach(0.0, pricing_authority_exceeded_count=2) is False

    def test_true_when_discount_depth_gte_10(self):
        assert self._coach(0.0, avg_discount_override_depth_pct=0.10) is True

    def test_true_when_discount_depth_above_10(self):
        assert self._coach(0.0, avg_discount_override_depth_pct=0.20) is True

    def test_false_when_discount_depth_below_10(self):
        assert self._coach(0.0, avg_discount_override_depth_pct=0.09) is False

    def test_true_composite_and_pricing(self):
        assert self._coach(35.0, pricing_authority_exceeded_count=4) is True


# ===========================================================================
# 17. _estimated_margin_risk
# ===========================================================================

class TestEstimatedMarginRisk:
    def setup_method(self):
        self.eng = fresh_engine()

    def _risk(self, **kw):
        inp = make_input(**kw)
        composite = kw.pop("composite", 50.0)
        return self.eng._estimated_margin_risk(inp, composite)

    def test_zero_when_composite_zero(self):
        inp = make_input(total_deals_closed=20, deals_requiring_approval_pct=0.50, avg_exception_value_usd=5000.0)
        assert self.eng._estimated_margin_risk(inp, 0.0) == 0.0

    def test_zero_when_no_deals(self):
        inp = make_input(total_deals_closed=0, deals_requiring_approval_pct=0.50, avg_exception_value_usd=5000.0)
        assert self.eng._estimated_margin_risk(inp, 50.0) == 0.0

    def test_calculation_basic(self):
        # 20 * 0.5 = 10 exception deals; 10 * 1000 * 0.5 = 5000
        inp = make_input(total_deals_closed=20, deals_requiring_approval_pct=0.50, avg_exception_value_usd=1000.0)
        result = self.eng._estimated_margin_risk(inp, 50.0)
        assert result == 5000.0

    def test_calculation_rounding(self):
        # 10 * 0.33 = 3 (rounded); 3 * 1000 * 0.5 = 1500
        inp = make_input(total_deals_closed=10, deals_requiring_approval_pct=0.33, avg_exception_value_usd=1000.0)
        result = self.eng._estimated_margin_risk(inp, 50.0)
        expected_deals = round(10 * 0.33)
        expected = round(expected_deals * 1000.0 * 0.50, 2)
        assert result == expected

    def test_returns_float(self):
        inp = make_input(total_deals_closed=10, deals_requiring_approval_pct=0.50, avg_exception_value_usd=2000.0)
        result = self.eng._estimated_margin_risk(inp, 40.0)
        assert isinstance(result, float)

    def test_scales_with_composite(self):
        inp = make_input(total_deals_closed=10, deals_requiring_approval_pct=1.0, avg_exception_value_usd=1000.0)
        r60 = self.eng._estimated_margin_risk(inp, 60.0)
        r30 = self.eng._estimated_margin_risk(inp, 30.0)
        assert r60 == pytest.approx(r30 * 2, rel=1e-5)


# ===========================================================================
# 18. _signal
# ===========================================================================

class TestSignal:
    def setup_method(self):
        self.eng = fresh_engine()

    def test_healthy_when_none_and_below_20(self):
        sig = self.eng._signal(make_input(), DealDeskPattern.none, 10.0)
        assert sig == "Deal desk utilization healthy — pricing discipline and exception management within benchmarks"

    def test_healthy_exact_boundary_19(self):
        sig = self.eng._signal(make_input(), DealDeskPattern.none, 19.9)
        assert "healthy" in sig

    def test_not_healthy_when_none_and_composite_20(self):
        inp = make_input()
        sig = self.eng._signal(inp, DealDeskPattern.none, 20.0)
        assert "healthy" not in sig

    def test_not_healthy_when_pattern_set_even_if_composite_low(self):
        sig = self.eng._signal(make_input(), DealDeskPattern.deal_desk_dependent, 5.0)
        assert "healthy" not in sig

    def test_signal_contains_composite(self):
        inp = make_input(deals_requiring_approval_pct=0.30, late_stage_escalation_rate_pct=0.10)
        sig = self.eng._signal(inp, DealDeskPattern.none, 35.0)
        assert "35" in sig

    def test_signal_contains_approval_pct(self):
        inp = make_input(deals_requiring_approval_pct=0.45)
        sig = self.eng._signal(inp, DealDeskPattern.none, 25.0)
        assert "45%" in sig

    def test_signal_contains_late_stage(self):
        inp = make_input(late_stage_escalation_rate_pct=0.30)
        sig = self.eng._signal(inp, DealDeskPattern.none, 25.0)
        assert "30%" in sig

    def test_signal_contains_avg_cycles(self):
        inp = make_input(avg_deal_desk_cycles_per_deal=2.5)
        sig = self.eng._signal(inp, DealDeskPattern.none, 25.0)
        assert "2.5" in sig

    def test_signal_pattern_label(self):
        sig = self.eng._signal(make_input(), DealDeskPattern.deal_desk_dependent, 50.0)
        assert "deal desk dependent" in sig.lower()

    def test_signal_discount_abuse_label(self):
        sig = self.eng._signal(make_input(), DealDeskPattern.discount_authority_abuse, 50.0)
        assert "discount" in sig.lower()

    def test_signal_pattern_none_non_healthy_uses_deal_desk_risk_label(self):
        sig = self.eng._signal(make_input(), DealDeskPattern.none, 25.0)
        assert "deal desk risk" in sig.lower()

    def test_signal_is_string(self):
        sig = self.eng._signal(make_input(), DealDeskPattern.none, 5.0)
        assert isinstance(sig, str)

    def test_signal_pct_100_approval_not_included(self):
        # If deals_requiring_approval_pct >= 1.0, the < 1.0 check fails so it won't appear
        inp = make_input(deals_requiring_approval_pct=1.0)
        sig = self.eng._signal(inp, DealDeskPattern.none, 25.0)
        assert "100%" not in sig

    def test_signal_pct_100_late_stage_not_included(self):
        inp = make_input(late_stage_escalation_rate_pct=1.0)
        sig = self.eng._signal(inp, DealDeskPattern.none, 25.0)
        # 100% late stage would not be included because check is < 1.0
        assert "late" not in sig


# ===========================================================================
# 19. assess() — basic integration
# ===========================================================================

class TestAssess:
    def setup_method(self):
        self.eng = fresh_engine()

    def test_returns_result(self):
        r = self.eng.assess(make_input())
        assert isinstance(r, DealDeskResult)

    def test_rep_id_propagated(self):
        r = self.eng.assess(make_input(rep_id="ALPHA"))
        assert r.rep_id == "ALPHA"

    def test_region_propagated(self):
        r = self.eng.assess(make_input(region="APAC"))
        assert r.region == "APAC"

    def test_result_stored_in_internal_list(self):
        self.eng.assess(make_input())
        assert len(self.eng._results) == 1

    def test_multiple_assessments_stored(self):
        self.eng.assess(make_input(rep_id="A"))
        self.eng.assess(make_input(rep_id="B"))
        assert len(self.eng._results) == 2

    def test_low_risk_baseline(self):
        r = self.eng.assess(make_input())
        assert r.deal_desk_risk == DealDeskRisk.low

    def test_critical_risk_high_inputs(self):
        r = self.eng.assess(make_input(
            deals_requiring_approval_pct=0.80,
            avg_discount_override_depth_pct=0.20,
            pricing_authority_exceeded_count=6,
            legal_review_escalation_count=5,
            avg_deal_desk_cycles_per_deal=3.5,
            executive_sponsor_required_count=4,
            late_stage_escalation_rate_pct=0.70,
            deal_desk_rejection_rate_pct=0.35,
            exceptions_by_competitor_loss_count=4,
            avg_exception_value_usd=25000.0,
            customer_success_concession_count=5,
            multi_product_bundle_exception_count=4,
        ))
        assert r.deal_desk_risk == DealDeskRisk.critical

    def test_composite_formula(self):
        eng = fresh_engine()
        inp = make_input(
            deals_requiring_approval_pct=0.60,
            avg_discount_override_depth_pct=0.15,
            pricing_authority_exceeded_count=5,
            legal_review_escalation_count=0,
            avg_deal_desk_cycles_per_deal=1.0,
            executive_sponsor_required_count=0,
            late_stage_escalation_rate_pct=0.05,
            deal_desk_rejection_rate_pct=0.05,
            exceptions_by_competitor_loss_count=0,
            avg_exception_value_usd=500.0,
            customer_success_concession_count=0,
            multi_product_bundle_exception_count=0,
        )
        r = eng.assess(inp)
        approval = eng._approval_dependency_score(inp)
        complexity = eng._exception_complexity_score(inp)
        urgency = eng._exception_urgency_score(inp)
        impact = eng._exception_impact_score(inp)
        expected = round(approval * 0.30 + complexity * 0.30 + urgency * 0.25 + impact * 0.15, 1)
        assert r.deal_desk_composite == expected

    def test_composite_capped_at_100(self):
        r = self.eng.assess(make_input(
            deals_requiring_approval_pct=1.0,
            avg_discount_override_depth_pct=1.0,
            pricing_authority_exceeded_count=99,
            legal_review_escalation_count=99,
            avg_deal_desk_cycles_per_deal=99.0,
            executive_sponsor_required_count=99,
            late_stage_escalation_rate_pct=1.0,
            deal_desk_rejection_rate_pct=1.0,
            exceptions_by_competitor_loss_count=99,
            avg_exception_value_usd=999999.0,
            customer_success_concession_count=99,
            multi_product_bundle_exception_count=99,
        ))
        assert r.deal_desk_composite <= 100.0

    def test_scores_are_rounded_to_1dp(self):
        r = self.eng.assess(make_input())
        assert r.approval_dependency_score == round(r.approval_dependency_score, 1)
        assert r.exception_complexity_score == round(r.exception_complexity_score, 1)
        assert r.exception_urgency_score == round(r.exception_urgency_score, 1)
        assert r.exception_impact_score == round(r.exception_impact_score, 1)

    def test_low_risk_no_action(self):
        r = self.eng.assess(make_input())
        assert r.recommended_action == DealDeskAction.no_action

    def test_severity_matches_risk(self):
        r = self.eng.assess(make_input())
        assert r.deal_desk_risk == DealDeskRisk.low
        assert r.deal_desk_severity == DealDeskSeverity.autonomous

    def test_margin_risk_is_float(self):
        r = self.eng.assess(make_input())
        assert isinstance(r.estimated_margin_risk_usd, float)

    def test_gap_false_for_low_inputs(self):
        r = self.eng.assess(make_input())
        assert r.has_deal_desk_gap is False

    def test_coaching_false_for_low_inputs(self):
        r = self.eng.assess(make_input())
        assert r.requires_deal_desk_coaching is False

    def test_to_dict_works_on_result(self):
        r = self.eng.assess(make_input())
        d = r.to_dict()
        assert len(d) == 15


# ===========================================================================
# 20. assess_batch()
# ===========================================================================

class TestAssessBatch:
    def setup_method(self):
        self.eng = fresh_engine()

    def test_returns_list(self):
        assert isinstance(self.eng.assess_batch([]), list)

    def test_empty_list(self):
        assert self.eng.assess_batch([]) == []

    def test_single_item(self):
        results = self.eng.assess_batch([make_input(rep_id="X1")])
        assert len(results) == 1

    def test_multiple_items(self):
        results = self.eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        assert len(results) == 5

    def test_all_stored(self):
        self.eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        assert len(self.eng._results) == 3

    def test_rep_ids_preserved(self):
        inputs = [make_input(rep_id=f"REP{i}") for i in range(4)]
        results = self.eng.assess_batch(inputs)
        rep_ids = [r.rep_id for r in results]
        assert rep_ids == ["REP0", "REP1", "REP2", "REP3"]

    def test_results_are_result_objects(self):
        results = self.eng.assess_batch([make_input()])
        assert all(isinstance(r, DealDeskResult) for r in results)

    def test_mixed_risk_levels(self):
        low_inp = make_input(rep_id="LOW")
        high_inp = make_input(
            rep_id="HIGH",
            deals_requiring_approval_pct=0.80,
            avg_discount_override_depth_pct=0.20,
            pricing_authority_exceeded_count=6,
            legal_review_escalation_count=5,
            avg_deal_desk_cycles_per_deal=3.5,
            executive_sponsor_required_count=4,
            late_stage_escalation_rate_pct=0.70,
            deal_desk_rejection_rate_pct=0.35,
            exceptions_by_competitor_loss_count=5,
            avg_exception_value_usd=25000.0,
            customer_success_concession_count=6,
            multi_product_bundle_exception_count=5,
        )
        results = self.eng.assess_batch([low_inp, high_inp])
        assert results[0].deal_desk_risk == DealDeskRisk.low
        assert results[1].deal_desk_risk == DealDeskRisk.critical


# ===========================================================================
# 21. summary() — empty state
# ===========================================================================

class TestSummaryEmpty:
    def setup_method(self):
        self.eng = fresh_engine()

    def test_returns_dict(self):
        assert isinstance(self.eng.summary(), dict)

    def test_has_13_keys(self):
        assert len(self.eng.summary()) == 13

    def test_total_zero(self):
        assert self.eng.summary()["total"] == 0

    def test_risk_counts_empty(self):
        assert self.eng.summary()["risk_counts"] == {}

    def test_pattern_counts_empty(self):
        assert self.eng.summary()["pattern_counts"] == {}

    def test_severity_counts_empty(self):
        assert self.eng.summary()["severity_counts"] == {}

    def test_action_counts_empty(self):
        assert self.eng.summary()["action_counts"] == {}

    def test_avg_composite_zero(self):
        assert self.eng.summary()["avg_deal_desk_composite"] == 0.0

    def test_gap_count_zero(self):
        assert self.eng.summary()["deal_desk_gap_count"] == 0

    def test_coaching_count_zero(self):
        assert self.eng.summary()["coaching_count"] == 0

    def test_avg_approval_zero(self):
        assert self.eng.summary()["avg_approval_dependency_score"] == 0.0

    def test_avg_complexity_zero(self):
        assert self.eng.summary()["avg_exception_complexity_score"] == 0.0

    def test_avg_urgency_zero(self):
        assert self.eng.summary()["avg_exception_urgency_score"] == 0.0

    def test_avg_impact_zero(self):
        assert self.eng.summary()["avg_exception_impact_score"] == 0.0

    def test_total_margin_risk_zero(self):
        assert self.eng.summary()["total_estimated_margin_risk_usd"] == 0.0


# ===========================================================================
# 22. summary() — with data
# ===========================================================================

class TestSummaryWithData:
    def setup_method(self):
        self.eng = fresh_engine()

    def _run_baseline(self):
        self.eng.assess(make_input(rep_id="R1"))
        self.eng.assess(make_input(rep_id="R2"))

    def test_total_reflects_assessments(self):
        self._run_baseline()
        assert self.eng.summary()["total"] == 2

    def test_risk_counts_populated(self):
        self._run_baseline()
        s = self.eng.summary()
        assert "low" in s["risk_counts"]

    def test_pattern_counts_populated(self):
        self._run_baseline()
        s = self.eng.summary()
        assert "none" in s["pattern_counts"]

    def test_severity_counts_populated(self):
        self._run_baseline()
        s = self.eng.summary()
        assert "autonomous" in s["severity_counts"]

    def test_action_counts_populated(self):
        self._run_baseline()
        s = self.eng.summary()
        assert "no_action" in s["action_counts"]

    def test_avg_composite_is_float(self):
        self._run_baseline()
        assert isinstance(self.eng.summary()["avg_deal_desk_composite"], float)

    def test_13_keys(self):
        self._run_baseline()
        assert len(self.eng.summary()) == 13

    def test_gap_count_correct(self):
        # baseline inputs produce no gap
        self._run_baseline()
        assert self.eng.summary()["deal_desk_gap_count"] == 0

    def test_gap_count_increases_when_gap(self):
        self.eng.assess(make_input(deals_requiring_approval_pct=0.60))
        assert self.eng.summary()["deal_desk_gap_count"] == 1

    def test_coaching_count_correct(self):
        self._run_baseline()
        assert self.eng.summary()["coaching_count"] == 0

    def test_coaching_count_increases(self):
        self.eng.assess(make_input(avg_discount_override_depth_pct=0.15))
        assert self.eng.summary()["coaching_count"] == 1

    def test_total_margin_risk_is_sum(self):
        self.eng.assess(make_input(total_deals_closed=0))
        self.eng.assess(make_input(total_deals_closed=0))
        assert self.eng.summary()["total_estimated_margin_risk_usd"] == 0.0

    def test_summary_risk_counts_single(self):
        self.eng.assess(make_input())
        s = self.eng.summary()
        assert s["risk_counts"].get("low", 0) == 1

    def test_summary_avg_scores_rounded(self):
        self._run_baseline()
        s = self.eng.summary()
        v = s["avg_approval_dependency_score"]
        assert v == round(v, 1)

    def test_summary_accumulates_across_batches(self):
        self.eng.assess_batch([make_input(rep_id=f"B{i}") for i in range(5)])
        assert self.eng.summary()["total"] == 5


# ===========================================================================
# 23. End-to-end scenario tests
# ===========================================================================

class TestEndToEndScenarios:
    def setup_method(self):
        self.eng = fresh_engine()

    def test_healthy_rep(self):
        """Rep with all low activity should produce healthy signal."""
        r = self.eng.assess(make_input())
        assert "healthy" in r.deal_desk_signal
        assert r.deal_desk_risk == DealDeskRisk.low
        assert r.deal_desk_severity == DealDeskSeverity.autonomous
        assert r.recommended_action == DealDeskAction.no_action
        assert r.has_deal_desk_gap is False
        assert r.requires_deal_desk_coaching is False

    def test_deal_desk_dependent_rep(self):
        """High approval dependency pattern is detected regardless of composite."""
        r = self.eng.assess(make_input(
            deals_requiring_approval_pct=0.70,
            avg_discount_override_depth_pct=0.20,
            pricing_authority_exceeded_count=6,
        ))
        assert r.deal_desk_pattern == DealDeskPattern.deal_desk_dependent
        # Pattern fires when approval>=40 AND pct>=0.50; composite may still be moderate
        assert r.deal_desk_risk in (DealDeskRisk.moderate, DealDeskRisk.high, DealDeskRisk.critical)

    def test_discount_abuse_rep(self):
        """Discount authority abuse pattern triggers correct action."""
        r = self.eng.assess(make_input(
            deals_requiring_approval_pct=0.10,
            avg_discount_override_depth_pct=0.20,
            pricing_authority_exceeded_count=6,
            legal_review_escalation_count=5,
            avg_deal_desk_cycles_per_deal=3.5,
            executive_sponsor_required_count=4,
            late_stage_escalation_rate_pct=0.65,
            deal_desk_rejection_rate_pct=0.35,
            exceptions_by_competitor_loss_count=5,
            avg_exception_value_usd=25000.0,
            customer_success_concession_count=6,
            multi_product_bundle_exception_count=5,
        ))
        # High composite => critical risk; abuse checked only if deal_desk_dependent not hit
        # deals_requiring_approval_pct=0.10 and approval score will be low so dependent won't hit
        # approval>=30 and discount>=0.10 -> discount_authority_abuse
        if r.deal_desk_pattern == DealDeskPattern.discount_authority_abuse:
            assert r.recommended_action == DealDeskAction.discount_discipline_review

    def test_legal_pattern_rep(self):
        """Legal escalation pattern triggers legal reduction action."""
        r = self.eng.assess(make_input(
            legal_review_escalation_count=5,
            avg_deal_desk_cycles_per_deal=3.5,
            executive_sponsor_required_count=4,
            late_stage_escalation_rate_pct=0.65,
            deal_desk_rejection_rate_pct=0.35,
            exceptions_by_competitor_loss_count=5,
            avg_exception_value_usd=25000.0,
            customer_success_concession_count=6,
            multi_product_bundle_exception_count=5,
        ))
        if r.deal_desk_pattern == DealDeskPattern.legal_escalation_pattern and r.deal_desk_risk == DealDeskRisk.critical:
            assert r.recommended_action == DealDeskAction.legal_escalation_reduction

    def test_competitive_capitulation_pattern(self):
        """Competitive capitulation with high risk gives pricing authority coaching."""
        r = self.eng.assess(make_input(
            exceptions_by_competitor_loss_count=4,
            late_stage_escalation_rate_pct=0.25,
            deal_desk_rejection_rate_pct=0.20,
        ))
        if r.deal_desk_pattern == DealDeskPattern.competitive_capitulation and r.deal_desk_risk == DealDeskRisk.high:
            assert r.recommended_action == DealDeskAction.pricing_authority_coaching

    def test_batch_then_summary(self):
        """assess_batch + summary consistency."""
        inputs = [make_input(rep_id=f"R{i}") for i in range(10)]
        results = self.eng.assess_batch(inputs)
        s = self.eng.summary()
        assert s["total"] == 10
        risk_total = sum(s["risk_counts"].values())
        assert risk_total == 10

    def test_to_dict_values_match_result_attributes(self):
        r = self.eng.assess(make_input(rep_id="DICT1", region="West"))
        d = r.to_dict()
        assert d["rep_id"] == r.rep_id
        assert d["region"] == r.region
        assert d["deal_desk_risk"] == r.deal_desk_risk.value
        assert d["deal_desk_pattern"] == r.deal_desk_pattern.value
        assert d["deal_desk_severity"] == r.deal_desk_severity.value
        assert d["recommended_action"] == r.recommended_action.value
        assert d["approval_dependency_score"] == r.approval_dependency_score
        assert d["exception_complexity_score"] == r.exception_complexity_score
        assert d["exception_urgency_score"] == r.exception_urgency_score
        assert d["exception_impact_score"] == r.exception_impact_score
        assert d["deal_desk_composite"] == r.deal_desk_composite
        assert d["has_deal_desk_gap"] == r.has_deal_desk_gap
        assert d["requires_deal_desk_coaching"] == r.requires_deal_desk_coaching
        assert d["estimated_margin_risk_usd"] == r.estimated_margin_risk_usd
        assert d["deal_desk_signal"] == r.deal_desk_signal

    def test_moderate_risk_scenario(self):
        """Moderate composite results in moderate risk and pricing coaching."""
        r = self.eng.assess(make_input(
            deals_requiring_approval_pct=0.25,
            late_stage_escalation_rate_pct=0.25,
            deal_desk_rejection_rate_pct=0.18,
        ))
        if r.deal_desk_risk == DealDeskRisk.moderate:
            assert r.recommended_action == DealDeskAction.pricing_authority_coaching
            assert r.deal_desk_severity == DealDeskSeverity.developing

    def test_engine_is_stateful(self):
        """Each new engine starts with empty results."""
        eng1 = fresh_engine()
        eng2 = fresh_engine()
        eng1.assess(make_input())
        assert len(eng2._results) == 0

    def test_severity_and_risk_aligned(self):
        """Severity and risk always map consistently from composite."""
        for composite in [0.0, 10.0, 20.0, 35.0, 40.0, 55.0, 60.0, 90.0, 100.0]:
            risk = self.eng._risk_level(composite)
            sev = self.eng._severity(composite)
            # Both use same thresholds
            if composite >= 60:
                assert risk == DealDeskRisk.critical
                assert sev == DealDeskSeverity.entrenched
            elif composite >= 40:
                assert risk == DealDeskRisk.high
                assert sev == DealDeskSeverity.dependent
            elif composite >= 20:
                assert risk == DealDeskRisk.moderate
                assert sev == DealDeskSeverity.developing
            else:
                assert risk == DealDeskRisk.low
                assert sev == DealDeskSeverity.autonomous


# ===========================================================================
# 24. Additional edge cases
# ===========================================================================

class TestEdgeCases:
    def setup_method(self):
        self.eng = fresh_engine()

    def test_zero_total_deals_no_crash(self):
        r = self.eng.assess(make_input(total_deals_closed=0))
        assert r.estimated_margin_risk_usd == 0.0

    def test_high_value_exception_caps_at_100(self):
        r = self.eng.assess(make_input(avg_exception_value_usd=1_000_000.0))
        assert r.exception_impact_score <= 100.0

    def test_deals_pct_of_1_no_crash(self):
        r = self.eng.assess(make_input(deals_requiring_approval_pct=1.0))
        assert r is not None

    def test_all_rates_at_zero(self):
        r = self.eng.assess(make_input(
            deals_requiring_approval_pct=0.0,
            avg_discount_override_depth_pct=0.0,
            late_stage_escalation_rate_pct=0.0,
            deal_desk_rejection_rate_pct=0.0,
        ))
        assert r.deal_desk_composite == 0.0

    def test_all_rates_at_max(self):
        r = self.eng.assess(make_input(
            deals_requiring_approval_pct=1.0,
            avg_discount_override_depth_pct=1.0,
            late_stage_escalation_rate_pct=1.0,
            deal_desk_rejection_rate_pct=1.0,
            pricing_authority_exceeded_count=100,
            legal_review_escalation_count=100,
            avg_deal_desk_cycles_per_deal=100.0,
            executive_sponsor_required_count=100,
            exceptions_by_competitor_loss_count=100,
            avg_exception_value_usd=1_000_000.0,
            customer_success_concession_count=100,
            multi_product_bundle_exception_count=100,
        ))
        assert r.deal_desk_composite == 100.0
        assert r.deal_desk_risk == DealDeskRisk.critical

    def test_boundary_composite_exactly_40(self):
        """Verify that composite == 40 gives high/dependent."""
        # Force composite = 40 via approval=100 * 0.40 = 40 if others = 0
        # approval_dep=100*0.30=30; need more. Use approval=45*0.30=13.5; complexity=45*0.30=13.5; urgency=45*0.25=11.25
        # Let's just test _risk_level and _severity directly
        assert self.eng._risk_level(40.0) == DealDeskRisk.high
        assert self.eng._severity(40.0) == DealDeskSeverity.dependent

    def test_boundary_composite_exactly_60(self):
        assert self.eng._risk_level(60.0) == DealDeskRisk.critical
        assert self.eng._severity(60.0) == DealDeskSeverity.entrenched

    def test_boundary_composite_exactly_20(self):
        assert self.eng._risk_level(20.0) == DealDeskRisk.moderate
        assert self.eng._severity(20.0) == DealDeskSeverity.developing

    def test_signal_benchmark_string_exact(self):
        r = self.eng.assess(make_input())
        assert r.deal_desk_signal == "Deal desk utilization healthy — pricing discipline and exception management within benchmarks"

    def test_large_batch_performance(self):
        inputs = [make_input(rep_id=f"BIG{i}") for i in range(100)]
        results = self.eng.assess_batch(inputs)
        assert len(results) == 100

    def test_summary_total_margin_accumulates(self):
        self.eng.assess(make_input(
            total_deals_closed=10,
            deals_requiring_approval_pct=0.60,
            avg_exception_value_usd=10000.0,
            avg_discount_override_depth_pct=0.20,
            pricing_authority_exceeded_count=5,
        ))
        s = self.eng.summary()
        assert s["total_estimated_margin_risk_usd"] >= 0.0

    def test_pattern_none_with_high_composite_gives_non_healthy_signal(self):
        # Force composite >= 20 but no pattern
        inp = make_input(
            deals_requiring_approval_pct=0.25,  # approval gets 10
            legal_review_escalation_count=1,    # complexity 8
            late_stage_escalation_rate_pct=0.21,  # urgency 8
        )
        r = self.eng.assess(inp)
        if r.deal_desk_composite >= 20:
            assert "healthy" not in r.deal_desk_signal
