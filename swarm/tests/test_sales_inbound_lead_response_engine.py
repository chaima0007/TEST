"""
Comprehensive pytest tests for swarm/intelligence/sales_inbound_lead_response_engine.py
"""
from __future__ import annotations

import pytest

from swarm.intelligence.sales_inbound_lead_response_engine import (
    LeadResponseRisk,
    LeadResponsePattern,
    LeadResponseSeverity,
    LeadResponseAction,
    InboundLeadResponseInput,
    InboundLeadResponseResult,
    SalesInboundLeadResponseEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(
    rep_id: str = "rep1",
    region: str = "East",
    evaluation_period_id: str = "Q1-2026",
    inbound_leads_assigned: int = 100,
    inbound_leads_contacted: int = 90,
    avg_first_response_hours: float = 1.0,
    leads_contacted_within_1h: int = 60,
    leads_contacted_within_5h: int = 80,
    leads_contacted_over_24h: int = 5,
    leads_never_contacted: int = 0,
    lead_to_qualified_conversion_rate_pct: float = 0.50,
    qualified_to_opportunity_conversion_rate_pct: float = 0.65,
    inbound_opportunity_close_rate_pct: float = 0.30,
    avg_lead_qualification_score: float = 7.0,
    high_icp_leads_received: int = 10,
    high_icp_leads_converted: int = 7,
    leads_disqualified_too_early: int = 0,
    leads_over_qualified_waste_count: int = 0,
    avg_response_quality_score: float = 7.0,
    crm_lead_entry_rate_pct: float = 0.95,
    avg_lead_revenue_potential_usd: float = 10_000.0,
    leads_lost_to_competitor_before_contact: int = 0,
) -> InboundLeadResponseInput:
    return InboundLeadResponseInput(
        rep_id=rep_id,
        region=region,
        evaluation_period_id=evaluation_period_id,
        inbound_leads_assigned=inbound_leads_assigned,
        inbound_leads_contacted=inbound_leads_contacted,
        avg_first_response_hours=avg_first_response_hours,
        leads_contacted_within_1h=leads_contacted_within_1h,
        leads_contacted_within_5h=leads_contacted_within_5h,
        leads_contacted_over_24h=leads_contacted_over_24h,
        leads_never_contacted=leads_never_contacted,
        lead_to_qualified_conversion_rate_pct=lead_to_qualified_conversion_rate_pct,
        qualified_to_opportunity_conversion_rate_pct=qualified_to_opportunity_conversion_rate_pct,
        inbound_opportunity_close_rate_pct=inbound_opportunity_close_rate_pct,
        avg_lead_qualification_score=avg_lead_qualification_score,
        high_icp_leads_received=high_icp_leads_received,
        high_icp_leads_converted=high_icp_leads_converted,
        leads_disqualified_too_early=leads_disqualified_too_early,
        leads_over_qualified_waste_count=leads_over_qualified_waste_count,
        avg_response_quality_score=avg_response_quality_score,
        crm_lead_entry_rate_pct=crm_lead_entry_rate_pct,
        avg_lead_revenue_potential_usd=avg_lead_revenue_potential_usd,
        leads_lost_to_competitor_before_contact=leads_lost_to_competitor_before_contact,
    )


def engine() -> SalesInboundLeadResponseEngine:
    return SalesInboundLeadResponseEngine()


# ===========================================================================
# 1. Enum tests
# ===========================================================================

class TestLeadResponseRiskEnum:
    def test_low_value(self):
        assert LeadResponseRisk.low.value == "low"

    def test_moderate_value(self):
        assert LeadResponseRisk.moderate.value == "moderate"

    def test_high_value(self):
        assert LeadResponseRisk.high.value == "high"

    def test_critical_value(self):
        assert LeadResponseRisk.critical.value == "critical"

    def test_all_members(self):
        members = {e.value for e in LeadResponseRisk}
        assert members == {"low", "moderate", "high", "critical"}

    def test_is_str(self):
        assert isinstance(LeadResponseRisk.low, str)

    def test_equality_with_string(self):
        assert LeadResponseRisk.low == "low"


class TestLeadResponsePatternEnum:
    def test_none_value(self):
        assert LeadResponsePattern.none.value == "none"

    def test_slow_response_value(self):
        assert LeadResponsePattern.slow_response.value == "slow_response"

    def test_poor_qualification_value(self):
        assert LeadResponsePattern.poor_qualification.value == "poor_qualification"

    def test_low_conversion_value(self):
        assert LeadResponsePattern.low_conversion.value == "low_conversion"

    def test_lead_neglect_value(self):
        assert LeadResponsePattern.lead_neglect.value == "lead_neglect"

    def test_icp_miss_value(self):
        assert LeadResponsePattern.icp_miss.value == "icp_miss"

    def test_all_members(self):
        members = {e.value for e in LeadResponsePattern}
        assert members == {
            "none", "slow_response", "poor_qualification",
            "low_conversion", "lead_neglect", "icp_miss"
        }

    def test_is_str(self):
        assert isinstance(LeadResponsePattern.none, str)

    def test_equality_with_string(self):
        assert LeadResponsePattern.slow_response == "slow_response"


class TestLeadResponseSeverityEnum:
    def test_responsive_value(self):
        assert LeadResponseSeverity.responsive.value == "responsive"

    def test_delayed_value(self):
        assert LeadResponseSeverity.delayed.value == "delayed"

    def test_lagging_value(self):
        assert LeadResponseSeverity.lagging.value == "lagging"

    def test_critical_value(self):
        assert LeadResponseSeverity.critical.value == "critical"

    def test_all_members(self):
        members = {e.value for e in LeadResponseSeverity}
        assert members == {"responsive", "delayed", "lagging", "critical"}

    def test_is_str(self):
        assert isinstance(LeadResponseSeverity.critical, str)


class TestLeadResponseActionEnum:
    def test_no_action_value(self):
        assert LeadResponseAction.no_action.value == "no_action"

    def test_response_time_coaching_value(self):
        assert LeadResponseAction.response_time_coaching.value == "response_time_coaching"

    def test_qualification_training_value(self):
        assert LeadResponseAction.qualification_training.value == "qualification_training"

    def test_lead_prioritization_value(self):
        assert LeadResponseAction.lead_prioritization.value == "lead_prioritization"

    def test_crm_discipline_value(self):
        assert LeadResponseAction.crm_discipline.value == "crm_discipline"

    def test_lead_cadence_reset_value(self):
        assert LeadResponseAction.lead_cadence_reset.value == "lead_cadence_reset"

    def test_all_members(self):
        members = {e.value for e in LeadResponseAction}
        assert members == {
            "no_action", "response_time_coaching", "qualification_training",
            "lead_prioritization", "crm_discipline", "lead_cadence_reset"
        }

    def test_is_str(self):
        assert isinstance(LeadResponseAction.no_action, str)


# ===========================================================================
# 2. _response_speed_score tests
# ===========================================================================

class TestResponseSpeedScore:
    """Score = avg_hours component + over_24_rate component + within_1h_rate component"""

    def _score(self, **kwargs) -> float:
        e = engine()
        return e._response_speed_score(make_input(**kwargs))

    # --- avg_first_response_hours component ---

    def test_avg_response_below_2_hours_zero_component(self):
        # < 2 h → 0 for that component
        s = self._score(avg_first_response_hours=1.0,
                        leads_contacted_over_24h=0,
                        leads_contacted_within_1h=100)
        assert s == 0.0

    def test_avg_response_exactly_2_hours_adds_10(self):
        s = self._score(avg_first_response_hours=2.0,
                        leads_contacted_over_24h=0,
                        leads_contacted_within_1h=100)
        assert s == 10.0

    def test_avg_response_just_below_8_hours_adds_10(self):
        s = self._score(avg_first_response_hours=7.99,
                        leads_contacted_over_24h=0,
                        leads_contacted_within_1h=100)
        assert s == 10.0

    def test_avg_response_exactly_8_hours_adds_25(self):
        s = self._score(avg_first_response_hours=8.0,
                        leads_contacted_over_24h=0,
                        leads_contacted_within_1h=100)
        assert s == 25.0

    def test_avg_response_just_below_24_hours_adds_25(self):
        s = self._score(avg_first_response_hours=23.99,
                        leads_contacted_over_24h=0,
                        leads_contacted_within_1h=100)
        assert s == 25.0

    def test_avg_response_exactly_24_hours_adds_45(self):
        s = self._score(avg_first_response_hours=24.0,
                        leads_contacted_over_24h=0,
                        leads_contacted_within_1h=100)
        assert s == 45.0

    def test_avg_response_above_24_hours_adds_45(self):
        s = self._score(avg_first_response_hours=48.0,
                        leads_contacted_over_24h=0,
                        leads_contacted_within_1h=100)
        assert s == 45.0

    # --- over_24_rate component ---

    def test_over24_rate_below_10pct_zero_component(self):
        # 5/100 = 0.05
        s = self._score(avg_first_response_hours=1.0,
                        inbound_leads_assigned=100,
                        leads_contacted_over_24h=5,
                        leads_contacted_within_1h=100)
        assert s == 0.0

    def test_over24_rate_exactly_10pct_adds_5(self):
        # 10/100 = 0.10
        s = self._score(avg_first_response_hours=1.0,
                        inbound_leads_assigned=100,
                        leads_contacted_over_24h=10,
                        leads_contacted_within_1h=100)
        assert s == 5.0

    def test_over24_rate_just_below_25pct_adds_5(self):
        # 24/100 = 0.24
        s = self._score(avg_first_response_hours=1.0,
                        inbound_leads_assigned=100,
                        leads_contacted_over_24h=24,
                        leads_contacted_within_1h=100)
        assert s == 5.0

    def test_over24_rate_exactly_25pct_adds_15(self):
        # 25/100 = 0.25
        s = self._score(avg_first_response_hours=1.0,
                        inbound_leads_assigned=100,
                        leads_contacted_over_24h=25,
                        leads_contacted_within_1h=100)
        assert s == 15.0

    def test_over24_rate_just_below_40pct_adds_15(self):
        # 39/100 = 0.39
        s = self._score(avg_first_response_hours=1.0,
                        inbound_leads_assigned=100,
                        leads_contacted_over_24h=39,
                        leads_contacted_within_1h=100)
        assert s == 15.0

    def test_over24_rate_exactly_40pct_adds_30(self):
        # 40/100 = 0.40
        s = self._score(avg_first_response_hours=1.0,
                        inbound_leads_assigned=100,
                        leads_contacted_over_24h=40,
                        leads_contacted_within_1h=100)
        assert s == 30.0

    def test_over24_rate_above_40pct_adds_30(self):
        # 60/100 = 0.60
        s = self._score(avg_first_response_hours=1.0,
                        inbound_leads_assigned=100,
                        leads_contacted_over_24h=60,
                        leads_contacted_within_1h=100)
        assert s == 30.0

    # --- within_1h_rate component ---

    def test_within1h_rate_above_40pct_zero_component(self):
        # 50/100 = 0.50
        s = self._score(avg_first_response_hours=1.0,
                        inbound_leads_assigned=100,
                        leads_contacted_over_24h=0,
                        leads_contacted_within_1h=50)
        assert s == 0.0

    def test_within1h_rate_exactly_40pct_zero_component(self):
        # 40/100 = 0.40 => NOT < 0.40 → 0
        s = self._score(avg_first_response_hours=1.0,
                        inbound_leads_assigned=100,
                        leads_contacted_over_24h=0,
                        leads_contacted_within_1h=40)
        assert s == 0.0

    def test_within1h_rate_just_below_40pct_adds_7(self):
        # 39/100 = 0.39 → adds 7
        s = self._score(avg_first_response_hours=1.0,
                        inbound_leads_assigned=100,
                        leads_contacted_over_24h=0,
                        leads_contacted_within_1h=39)
        assert s == 7.0

    def test_within1h_rate_exactly_20pct_adds_15(self):
        # 20/100 = 0.20 → NOT < 0.20 → adds 7
        s = self._score(avg_first_response_hours=1.0,
                        inbound_leads_assigned=100,
                        leads_contacted_over_24h=0,
                        leads_contacted_within_1h=20)
        assert s == 7.0

    def test_within1h_rate_just_below_20pct_adds_15(self):
        # 19/100 = 0.19 → < 0.20 → adds 15
        s = self._score(avg_first_response_hours=1.0,
                        inbound_leads_assigned=100,
                        leads_contacted_over_24h=0,
                        leads_contacted_within_1h=19)
        assert s == 15.0

    def test_within1h_rate_zero_adds_15(self):
        s = self._score(avg_first_response_hours=1.0,
                        inbound_leads_assigned=100,
                        leads_contacted_over_24h=0,
                        leads_contacted_within_1h=0)
        assert s == 15.0

    # --- max cap ---

    def test_score_capped_at_100(self):
        # 45 + 30 + 15 = 90 < 100, add more: avg>=24 (45) + over24>=40pct (30) + within1h<20pct (15) = 90
        s = self._score(avg_first_response_hours=24.0,
                        inbound_leads_assigned=100,
                        leads_contacted_over_24h=40,
                        leads_contacted_within_1h=0)
        assert s == 90.0

    def test_score_zero_minimum(self):
        s = self._score(avg_first_response_hours=0.5,
                        inbound_leads_assigned=100,
                        leads_contacted_over_24h=0,
                        leads_contacted_within_1h=50)
        assert s == 0.0

    def test_zero_leads_assigned_uses_1_as_denominator(self):
        # inbound_leads_assigned=0 → total=1
        # over_24h=0 → over_24_rate=0; within_1h=0 → within_1h_rate=0/1=0 → <0.20 → +15
        s = self._score(avg_first_response_hours=1.0,
                        inbound_leads_assigned=0,
                        leads_contacted_over_24h=0,
                        leads_contacted_within_1h=0)
        assert s == 15.0

    def test_combined_all_max_components(self):
        # avg>=24 (+45), over24>=40pct (+30), within1h<20pct (+15) = 90
        s = self._score(
            avg_first_response_hours=30.0,
            inbound_leads_assigned=100,
            leads_contacted_over_24h=50,
            leads_contacted_within_1h=10,
        )
        assert s == 90.0


# ===========================================================================
# 3. _qualification_quality_score tests
# ===========================================================================

class TestQualificationQualityScore:
    def _score(self, **kwargs) -> float:
        e = engine()
        return e._qualification_quality_score(make_input(**kwargs))

    # --- avg_lead_qualification_score component ---

    def test_avg_qual_score_below_4_adds_40(self):
        s = self._score(avg_lead_qualification_score=3.9,
                        avg_response_quality_score=7.0,
                        leads_disqualified_too_early=0)
        assert s == 40.0

    def test_avg_qual_score_exactly_4_adds_20(self):
        s = self._score(avg_lead_qualification_score=4.0,
                        avg_response_quality_score=7.0,
                        leads_disqualified_too_early=0)
        assert s == 20.0

    def test_avg_qual_score_just_below_6_adds_20(self):
        s = self._score(avg_lead_qualification_score=5.99,
                        avg_response_quality_score=7.0,
                        leads_disqualified_too_early=0)
        assert s == 20.0

    def test_avg_qual_score_exactly_6_adds_8(self):
        s = self._score(avg_lead_qualification_score=6.0,
                        avg_response_quality_score=7.0,
                        leads_disqualified_too_early=0)
        assert s == 8.0

    def test_avg_qual_score_just_below_7_5_adds_8(self):
        s = self._score(avg_lead_qualification_score=7.49,
                        avg_response_quality_score=7.0,
                        leads_disqualified_too_early=0)
        assert s == 8.0

    def test_avg_qual_score_exactly_7_5_adds_0(self):
        s = self._score(avg_lead_qualification_score=7.5,
                        avg_response_quality_score=7.0,
                        leads_disqualified_too_early=0)
        assert s == 0.0

    def test_avg_qual_score_above_7_5_adds_0(self):
        s = self._score(avg_lead_qualification_score=9.0,
                        avg_response_quality_score=7.0,
                        leads_disqualified_too_early=0)
        assert s == 0.0

    # --- avg_response_quality_score component ---

    def test_avg_resp_qual_below_4_adds_30(self):
        s = self._score(avg_lead_qualification_score=7.5,
                        avg_response_quality_score=3.9,
                        leads_disqualified_too_early=0)
        assert s == 30.0

    def test_avg_resp_qual_exactly_4_adds_15(self):
        s = self._score(avg_lead_qualification_score=7.5,
                        avg_response_quality_score=4.0,
                        leads_disqualified_too_early=0)
        assert s == 15.0

    def test_avg_resp_qual_just_below_6_adds_15(self):
        s = self._score(avg_lead_qualification_score=7.5,
                        avg_response_quality_score=5.99,
                        leads_disqualified_too_early=0)
        assert s == 15.0

    def test_avg_resp_qual_exactly_6_adds_0(self):
        s = self._score(avg_lead_qualification_score=7.5,
                        avg_response_quality_score=6.0,
                        leads_disqualified_too_early=0)
        assert s == 0.0

    def test_avg_resp_qual_above_6_adds_0(self):
        s = self._score(avg_lead_qualification_score=7.5,
                        avg_response_quality_score=8.0,
                        leads_disqualified_too_early=0)
        assert s == 0.0

    # --- disqualified_too_early component ---

    def test_disq_rate_below_10pct_zero_component(self):
        # 9/100 = 0.09
        s = self._score(avg_lead_qualification_score=7.5,
                        avg_response_quality_score=7.0,
                        inbound_leads_assigned=100,
                        leads_disqualified_too_early=9)
        assert s == 0.0

    def test_disq_rate_exactly_10pct_adds_10(self):
        # 10/100 = 0.10
        s = self._score(avg_lead_qualification_score=7.5,
                        avg_response_quality_score=7.0,
                        inbound_leads_assigned=100,
                        leads_disqualified_too_early=10)
        assert s == 10.0

    def test_disq_rate_just_below_20pct_adds_10(self):
        # 19/100 = 0.19
        s = self._score(avg_lead_qualification_score=7.5,
                        avg_response_quality_score=7.0,
                        inbound_leads_assigned=100,
                        leads_disqualified_too_early=19)
        assert s == 10.0

    def test_disq_rate_exactly_20pct_adds_20(self):
        # 20/100 = 0.20
        s = self._score(avg_lead_qualification_score=7.5,
                        avg_response_quality_score=7.0,
                        inbound_leads_assigned=100,
                        leads_disqualified_too_early=20)
        assert s == 20.0

    def test_disq_rate_above_20pct_adds_20(self):
        # 30/100 = 0.30
        s = self._score(avg_lead_qualification_score=7.5,
                        avg_response_quality_score=7.0,
                        inbound_leads_assigned=100,
                        leads_disqualified_too_early=30)
        assert s == 20.0

    # --- cap and zero ---

    def test_max_score_capped_at_100(self):
        # 40 + 30 + 20 = 90 < 100, but check cap logic works
        s = self._score(avg_lead_qualification_score=3.0,
                        avg_response_quality_score=3.0,
                        inbound_leads_assigned=100,
                        leads_disqualified_too_early=20)
        assert s == 90.0

    def test_zero_score_ideal_inputs(self):
        s = self._score(avg_lead_qualification_score=8.0,
                        avg_response_quality_score=7.0,
                        inbound_leads_assigned=100,
                        leads_disqualified_too_early=0)
        assert s == 0.0

    def test_zero_leads_uses_denominator_1(self):
        s = self._score(avg_lead_qualification_score=7.5,
                        avg_response_quality_score=7.0,
                        inbound_leads_assigned=0,
                        leads_disqualified_too_early=0)
        assert s == 0.0


# ===========================================================================
# 4. _lead_conversion_score tests
# ===========================================================================

class TestLeadConversionScore:
    def _score(self, **kwargs) -> float:
        e = engine()
        return e._lead_conversion_score(make_input(**kwargs))

    # --- lead_to_qualified_conversion_rate_pct component ---

    def test_l2q_below_20pct_adds_35(self):
        s = self._score(lead_to_qualified_conversion_rate_pct=0.19,
                        qualified_to_opportunity_conversion_rate_pct=0.65,
                        high_icp_leads_received=0)
        assert s == 35.0

    def test_l2q_exactly_20pct_adds_18(self):
        s = self._score(lead_to_qualified_conversion_rate_pct=0.20,
                        qualified_to_opportunity_conversion_rate_pct=0.65,
                        high_icp_leads_received=0)
        assert s == 18.0

    def test_l2q_just_below_35pct_adds_18(self):
        s = self._score(lead_to_qualified_conversion_rate_pct=0.34,
                        qualified_to_opportunity_conversion_rate_pct=0.65,
                        high_icp_leads_received=0)
        assert s == 18.0

    def test_l2q_exactly_35pct_adds_7(self):
        s = self._score(lead_to_qualified_conversion_rate_pct=0.35,
                        qualified_to_opportunity_conversion_rate_pct=0.65,
                        high_icp_leads_received=0)
        assert s == 7.0

    def test_l2q_just_below_50pct_adds_7(self):
        s = self._score(lead_to_qualified_conversion_rate_pct=0.49,
                        qualified_to_opportunity_conversion_rate_pct=0.65,
                        high_icp_leads_received=0)
        assert s == 7.0

    def test_l2q_exactly_50pct_adds_0(self):
        s = self._score(lead_to_qualified_conversion_rate_pct=0.50,
                        qualified_to_opportunity_conversion_rate_pct=0.65,
                        high_icp_leads_received=0)
        assert s == 0.0

    def test_l2q_above_50pct_adds_0(self):
        s = self._score(lead_to_qualified_conversion_rate_pct=0.80,
                        qualified_to_opportunity_conversion_rate_pct=0.65,
                        high_icp_leads_received=0)
        assert s == 0.0

    # --- qualified_to_opportunity_conversion_rate_pct component ---

    def test_q2o_below_40pct_adds_30(self):
        s = self._score(lead_to_qualified_conversion_rate_pct=0.50,
                        qualified_to_opportunity_conversion_rate_pct=0.39,
                        high_icp_leads_received=0)
        assert s == 30.0

    def test_q2o_exactly_40pct_adds_15(self):
        s = self._score(lead_to_qualified_conversion_rate_pct=0.50,
                        qualified_to_opportunity_conversion_rate_pct=0.40,
                        high_icp_leads_received=0)
        assert s == 15.0

    def test_q2o_just_below_60pct_adds_15(self):
        s = self._score(lead_to_qualified_conversion_rate_pct=0.50,
                        qualified_to_opportunity_conversion_rate_pct=0.59,
                        high_icp_leads_received=0)
        assert s == 15.0

    def test_q2o_exactly_60pct_adds_0(self):
        s = self._score(lead_to_qualified_conversion_rate_pct=0.50,
                        qualified_to_opportunity_conversion_rate_pct=0.60,
                        high_icp_leads_received=0)
        assert s == 0.0

    def test_q2o_above_60pct_adds_0(self):
        s = self._score(lead_to_qualified_conversion_rate_pct=0.50,
                        qualified_to_opportunity_conversion_rate_pct=0.80,
                        high_icp_leads_received=0)
        assert s == 0.0

    # --- icp_conversion component ---

    def test_icp_received_zero_no_component(self):
        s = self._score(lead_to_qualified_conversion_rate_pct=0.50,
                        qualified_to_opportunity_conversion_rate_pct=0.65,
                        high_icp_leads_received=0,
                        high_icp_leads_converted=0)
        assert s == 0.0

    def test_icp_conv_below_30pct_adds_25(self):
        # 2/10 = 0.20 < 0.30
        s = self._score(lead_to_qualified_conversion_rate_pct=0.50,
                        qualified_to_opportunity_conversion_rate_pct=0.65,
                        high_icp_leads_received=10,
                        high_icp_leads_converted=2)
        assert s == 25.0

    def test_icp_conv_exactly_30pct_adds_12(self):
        # 3/10 = 0.30 → NOT < 0.30 → check < 0.55
        s = self._score(lead_to_qualified_conversion_rate_pct=0.50,
                        qualified_to_opportunity_conversion_rate_pct=0.65,
                        high_icp_leads_received=10,
                        high_icp_leads_converted=3)
        assert s == 12.0

    def test_icp_conv_just_below_55pct_adds_12(self):
        # 5/10 = 0.50 < 0.55
        s = self._score(lead_to_qualified_conversion_rate_pct=0.50,
                        qualified_to_opportunity_conversion_rate_pct=0.65,
                        high_icp_leads_received=10,
                        high_icp_leads_converted=5)
        assert s == 12.0

    def test_icp_conv_exactly_55pct_adds_0(self):
        # 55/100 = 0.55
        s = self._score(lead_to_qualified_conversion_rate_pct=0.50,
                        qualified_to_opportunity_conversion_rate_pct=0.65,
                        high_icp_leads_received=100,
                        high_icp_leads_converted=55)
        assert s == 0.0

    def test_icp_conv_above_55pct_adds_0(self):
        s = self._score(lead_to_qualified_conversion_rate_pct=0.50,
                        qualified_to_opportunity_conversion_rate_pct=0.65,
                        high_icp_leads_received=10,
                        high_icp_leads_converted=8)
        assert s == 0.0

    def test_score_capped_at_100(self):
        # 35 + 30 + 25 = 90 < 100 but test cap anyway
        s = self._score(lead_to_qualified_conversion_rate_pct=0.10,
                        qualified_to_opportunity_conversion_rate_pct=0.30,
                        high_icp_leads_received=10,
                        high_icp_leads_converted=1)
        assert s == 90.0

    def test_ideal_inputs_zero_score(self):
        s = self._score(lead_to_qualified_conversion_rate_pct=0.60,
                        qualified_to_opportunity_conversion_rate_pct=0.70,
                        high_icp_leads_received=10,
                        high_icp_leads_converted=9)
        assert s == 0.0


# ===========================================================================
# 5. _lead_discipline_score tests
# ===========================================================================

class TestLeadDisciplineScore:
    def _score(self, **kwargs) -> float:
        e = engine()
        return e._lead_discipline_score(make_input(**kwargs))

    # --- never_rate component ---

    def test_never_rate_below_5pct_zero_component(self):
        # 4/100 = 0.04
        s = self._score(inbound_leads_assigned=100,
                        leads_never_contacted=4,
                        crm_lead_entry_rate_pct=1.0,
                        leads_lost_to_competitor_before_contact=0)
        assert s == 0.0

    def test_never_rate_exactly_5pct_adds_8(self):
        # 5/100 = 0.05
        s = self._score(inbound_leads_assigned=100,
                        leads_never_contacted=5,
                        crm_lead_entry_rate_pct=1.0,
                        leads_lost_to_competitor_before_contact=0)
        assert s == 8.0

    def test_never_rate_just_below_10pct_adds_8(self):
        # 9/100 = 0.09
        s = self._score(inbound_leads_assigned=100,
                        leads_never_contacted=9,
                        crm_lead_entry_rate_pct=1.0,
                        leads_lost_to_competitor_before_contact=0)
        assert s == 8.0

    def test_never_rate_exactly_10pct_adds_20(self):
        # 10/100 = 0.10
        s = self._score(inbound_leads_assigned=100,
                        leads_never_contacted=10,
                        crm_lead_entry_rate_pct=1.0,
                        leads_lost_to_competitor_before_contact=0)
        assert s == 20.0

    def test_never_rate_just_below_20pct_adds_20(self):
        # 19/100 = 0.19
        s = self._score(inbound_leads_assigned=100,
                        leads_never_contacted=19,
                        crm_lead_entry_rate_pct=1.0,
                        leads_lost_to_competitor_before_contact=0)
        assert s == 20.0

    def test_never_rate_exactly_20pct_adds_40(self):
        # 20/100 = 0.20
        s = self._score(inbound_leads_assigned=100,
                        leads_never_contacted=20,
                        crm_lead_entry_rate_pct=1.0,
                        leads_lost_to_competitor_before_contact=0)
        assert s == 40.0

    def test_never_rate_above_20pct_adds_40(self):
        # 50/100 = 0.50
        s = self._score(inbound_leads_assigned=100,
                        leads_never_contacted=50,
                        crm_lead_entry_rate_pct=1.0,
                        leads_lost_to_competitor_before_contact=0)
        assert s == 40.0

    # --- crm_lead_entry_rate_pct component ---

    def test_crm_rate_above_75pct_adds_0(self):
        s = self._score(inbound_leads_assigned=100,
                        leads_never_contacted=0,
                        crm_lead_entry_rate_pct=0.80,
                        leads_lost_to_competitor_before_contact=0)
        assert s == 0.0

    def test_crm_rate_exactly_75pct_adds_0(self):
        # NOT < 0.75 → 0
        s = self._score(inbound_leads_assigned=100,
                        leads_never_contacted=0,
                        crm_lead_entry_rate_pct=0.75,
                        leads_lost_to_competitor_before_contact=0)
        assert s == 0.0

    def test_crm_rate_just_below_75pct_adds_15(self):
        s = self._score(inbound_leads_assigned=100,
                        leads_never_contacted=0,
                        crm_lead_entry_rate_pct=0.74,
                        leads_lost_to_competitor_before_contact=0)
        assert s == 15.0

    def test_crm_rate_exactly_50pct_adds_15(self):
        # NOT < 0.50 → 15
        s = self._score(inbound_leads_assigned=100,
                        leads_never_contacted=0,
                        crm_lead_entry_rate_pct=0.50,
                        leads_lost_to_competitor_before_contact=0)
        assert s == 15.0

    def test_crm_rate_just_below_50pct_adds_30(self):
        s = self._score(inbound_leads_assigned=100,
                        leads_never_contacted=0,
                        crm_lead_entry_rate_pct=0.49,
                        leads_lost_to_competitor_before_contact=0)
        assert s == 30.0

    def test_crm_rate_zero_adds_30(self):
        s = self._score(inbound_leads_assigned=100,
                        leads_never_contacted=0,
                        crm_lead_entry_rate_pct=0.0,
                        leads_lost_to_competitor_before_contact=0)
        assert s == 30.0

    # --- leads_lost_to_competitor_before_contact component ---

    def test_lost_zero_adds_0(self):
        s = self._score(inbound_leads_assigned=100,
                        leads_never_contacted=0,
                        crm_lead_entry_rate_pct=1.0,
                        leads_lost_to_competitor_before_contact=0)
        assert s == 0.0

    def test_lost_exactly_1_adds_10(self):
        s = self._score(inbound_leads_assigned=100,
                        leads_never_contacted=0,
                        crm_lead_entry_rate_pct=1.0,
                        leads_lost_to_competitor_before_contact=1)
        assert s == 10.0

    def test_lost_exactly_2_adds_10(self):
        s = self._score(inbound_leads_assigned=100,
                        leads_never_contacted=0,
                        crm_lead_entry_rate_pct=1.0,
                        leads_lost_to_competitor_before_contact=2)
        assert s == 10.0

    def test_lost_exactly_3_adds_20(self):
        s = self._score(inbound_leads_assigned=100,
                        leads_never_contacted=0,
                        crm_lead_entry_rate_pct=1.0,
                        leads_lost_to_competitor_before_contact=3)
        assert s == 20.0

    def test_lost_above_3_adds_20(self):
        s = self._score(inbound_leads_assigned=100,
                        leads_never_contacted=0,
                        crm_lead_entry_rate_pct=1.0,
                        leads_lost_to_competitor_before_contact=10)
        assert s == 20.0

    def test_score_capped_at_100(self):
        # 40 + 30 + 20 = 90 < 100, max is capped at 100
        s = self._score(inbound_leads_assigned=100,
                        leads_never_contacted=20,
                        crm_lead_entry_rate_pct=0.0,
                        leads_lost_to_competitor_before_contact=5)
        assert s == 90.0

    def test_ideal_inputs_zero_score(self):
        s = self._score(inbound_leads_assigned=100,
                        leads_never_contacted=0,
                        crm_lead_entry_rate_pct=1.0,
                        leads_lost_to_competitor_before_contact=0)
        assert s == 0.0

    def test_zero_leads_assigned_uses_denominator_1(self):
        s = self._score(inbound_leads_assigned=0,
                        leads_never_contacted=0,
                        crm_lead_entry_rate_pct=1.0,
                        leads_lost_to_competitor_before_contact=0)
        assert s == 0.0


# ===========================================================================
# 6. _detect_pattern tests
# ===========================================================================

class TestDetectPattern:
    def _pattern(self, inp: InboundLeadResponseInput,
                 speed: float = 0.0, quality: float = 0.0,
                 conversion: float = 0.0, discipline: float = 0.0) -> LeadResponsePattern:
        e = engine()
        return e._detect_pattern(inp, speed, quality, conversion, discipline)

    # --- lead_neglect (highest priority) ---

    def test_lead_neglect_when_discipline_ge35_and_never_rate_ge15(self):
        inp = make_input(inbound_leads_assigned=100, leads_never_contacted=15)
        assert self._pattern(inp, discipline=35.0) == LeadResponsePattern.lead_neglect

    def test_lead_neglect_discipline_exactly_35_never_rate_exactly_15(self):
        inp = make_input(inbound_leads_assigned=100, leads_never_contacted=15)
        assert self._pattern(inp, discipline=35.0) == LeadResponsePattern.lead_neglect

    def test_lead_neglect_not_triggered_discipline_below_35(self):
        inp = make_input(inbound_leads_assigned=100, leads_never_contacted=15,
                         avg_first_response_hours=1.0,
                         lead_to_qualified_conversion_rate_pct=0.50,
                         avg_lead_qualification_score=8.0)
        result = self._pattern(inp, discipline=34.0)
        assert result != LeadResponsePattern.lead_neglect

    def test_lead_neglect_not_triggered_never_rate_below_15(self):
        inp = make_input(inbound_leads_assigned=100, leads_never_contacted=14,
                         avg_first_response_hours=1.0,
                         lead_to_qualified_conversion_rate_pct=0.50,
                         avg_lead_qualification_score=8.0)
        result = self._pattern(inp, discipline=40.0)
        assert result != LeadResponsePattern.lead_neglect

    def test_lead_neglect_priority_over_slow_response(self):
        # Conditions for both lead_neglect AND slow_response
        inp = make_input(inbound_leads_assigned=100, leads_never_contacted=20,
                         avg_first_response_hours=24.0)
        result = self._pattern(inp, speed=50.0, discipline=50.0)
        assert result == LeadResponsePattern.lead_neglect

    # --- slow_response (second priority) ---

    def test_slow_response_when_speed_ge35_and_avg_hours_ge12(self):
        inp = make_input(avg_first_response_hours=12.0, leads_never_contacted=0)
        result = self._pattern(inp, speed=35.0)
        assert result == LeadResponsePattern.slow_response

    def test_slow_response_speed_exactly_35(self):
        inp = make_input(avg_first_response_hours=12.0, leads_never_contacted=0)
        assert self._pattern(inp, speed=35.0) == LeadResponsePattern.slow_response

    def test_slow_response_not_triggered_speed_below_35(self):
        inp = make_input(avg_first_response_hours=12.0, leads_never_contacted=0,
                         lead_to_qualified_conversion_rate_pct=0.50,
                         avg_lead_qualification_score=8.0)
        result = self._pattern(inp, speed=34.0)
        assert result != LeadResponsePattern.slow_response

    def test_slow_response_not_triggered_hours_below_12(self):
        inp = make_input(avg_first_response_hours=11.0, leads_never_contacted=0,
                         lead_to_qualified_conversion_rate_pct=0.50,
                         avg_lead_qualification_score=8.0)
        result = self._pattern(inp, speed=50.0)
        assert result != LeadResponsePattern.slow_response

    # --- icp_miss (third priority) ---

    def test_icp_miss_when_conditions_met(self):
        inp = make_input(leads_never_contacted=0,
                         avg_first_response_hours=1.0,
                         high_icp_leads_received=5,
                         high_icp_leads_converted=1,  # 0.20 < 0.40
                         lead_to_qualified_conversion_rate_pct=0.50)
        result = self._pattern(inp, speed=0.0, conversion=30.0)
        assert result == LeadResponsePattern.icp_miss

    def test_icp_miss_conversion_exactly_30(self):
        inp = make_input(leads_never_contacted=0,
                         avg_first_response_hours=1.0,
                         high_icp_leads_received=5,
                         high_icp_leads_converted=1,
                         lead_to_qualified_conversion_rate_pct=0.50)
        assert self._pattern(inp, conversion=30.0) == LeadResponsePattern.icp_miss

    def test_icp_miss_not_triggered_not_enough_icp_leads(self):
        # high_icp_leads_received=2 < 3
        inp = make_input(leads_never_contacted=0,
                         avg_first_response_hours=1.0,
                         high_icp_leads_received=2,
                         high_icp_leads_converted=0,
                         lead_to_qualified_conversion_rate_pct=0.50,
                         avg_lead_qualification_score=8.0)
        result = self._pattern(inp, conversion=40.0)
        assert result != LeadResponsePattern.icp_miss

    def test_icp_miss_not_triggered_icp_conv_above_40(self):
        # 5/10 = 0.50 >= 0.40
        inp = make_input(leads_never_contacted=0,
                         avg_first_response_hours=1.0,
                         high_icp_leads_received=10,
                         high_icp_leads_converted=5,
                         lead_to_qualified_conversion_rate_pct=0.50,
                         avg_lead_qualification_score=8.0)
        result = self._pattern(inp, conversion=40.0)
        assert result != LeadResponsePattern.icp_miss

    # --- low_conversion (fourth priority) ---

    def test_low_conversion_when_conditions_met(self):
        inp = make_input(leads_never_contacted=0,
                         avg_first_response_hours=1.0,
                         high_icp_leads_received=0,
                         lead_to_qualified_conversion_rate_pct=0.25)
        result = self._pattern(inp, conversion=30.0)
        assert result == LeadResponsePattern.low_conversion

    def test_low_conversion_not_triggered_conversion_below_30(self):
        inp = make_input(leads_never_contacted=0,
                         avg_first_response_hours=1.0,
                         high_icp_leads_received=0,
                         lead_to_qualified_conversion_rate_pct=0.25,
                         avg_lead_qualification_score=8.0)
        result = self._pattern(inp, conversion=29.0)
        assert result != LeadResponsePattern.low_conversion

    def test_low_conversion_not_triggered_l2q_above_30pct(self):
        inp = make_input(leads_never_contacted=0,
                         avg_first_response_hours=1.0,
                         high_icp_leads_received=0,
                         lead_to_qualified_conversion_rate_pct=0.30,
                         avg_lead_qualification_score=8.0)
        result = self._pattern(inp, conversion=30.0)
        assert result != LeadResponsePattern.low_conversion

    # --- poor_qualification (fifth priority) ---

    def test_poor_qualification_when_conditions_met(self):
        inp = make_input(leads_never_contacted=0,
                         avg_first_response_hours=1.0,
                         high_icp_leads_received=0,
                         lead_to_qualified_conversion_rate_pct=0.50,
                         avg_lead_qualification_score=4.0)
        result = self._pattern(inp, quality=30.0)
        assert result == LeadResponsePattern.poor_qualification

    def test_poor_qualification_not_triggered_quality_below_30(self):
        inp = make_input(leads_never_contacted=0,
                         avg_first_response_hours=1.0,
                         high_icp_leads_received=0,
                         lead_to_qualified_conversion_rate_pct=0.50,
                         avg_lead_qualification_score=4.0)
        result = self._pattern(inp, quality=29.0)
        assert result == LeadResponsePattern.none

    def test_poor_qualification_not_triggered_qual_score_above_5_5(self):
        inp = make_input(leads_never_contacted=0,
                         avg_first_response_hours=1.0,
                         high_icp_leads_received=0,
                         lead_to_qualified_conversion_rate_pct=0.50,
                         avg_lead_qualification_score=5.5)
        result = self._pattern(inp, quality=40.0)
        assert result == LeadResponsePattern.none

    def test_poor_qualification_qual_score_exactly_5_5_not_triggered(self):
        # NOT < 5.5 → no poor_qualification
        inp = make_input(leads_never_contacted=0,
                         avg_first_response_hours=1.0,
                         high_icp_leads_received=0,
                         lead_to_qualified_conversion_rate_pct=0.50,
                         avg_lead_qualification_score=5.5)
        result = self._pattern(inp, quality=40.0)
        assert result == LeadResponsePattern.none

    # --- none (lowest priority) ---

    def test_none_when_all_conditions_unmet(self):
        inp = make_input(leads_never_contacted=0,
                         avg_first_response_hours=1.0,
                         high_icp_leads_received=0,
                         lead_to_qualified_conversion_rate_pct=0.50,
                         avg_lead_qualification_score=7.0)
        result = self._pattern(inp, speed=0.0, quality=0.0, conversion=0.0, discipline=0.0)
        assert result == LeadResponsePattern.none

    def test_none_at_boundary_just_below_each_threshold(self):
        inp = make_input(leads_never_contacted=14,
                         inbound_leads_assigned=100,
                         avg_first_response_hours=11.0,
                         high_icp_leads_received=0,
                         lead_to_qualified_conversion_rate_pct=0.50,
                         avg_lead_qualification_score=7.0)
        result = self._pattern(inp, speed=34.0, quality=29.0, conversion=29.0, discipline=34.0)
        assert result == LeadResponsePattern.none


# ===========================================================================
# 7. _risk_level and _severity boundary tests
# ===========================================================================

class TestRiskLevel:
    def _risk(self, composite: float) -> LeadResponseRisk:
        return engine()._risk_level(composite)

    def test_composite_0_is_low(self):
        assert self._risk(0.0) == LeadResponseRisk.low

    def test_composite_just_below_20_is_low(self):
        assert self._risk(19.9) == LeadResponseRisk.low

    def test_composite_exactly_20_is_moderate(self):
        assert self._risk(20.0) == LeadResponseRisk.moderate

    def test_composite_just_below_40_is_moderate(self):
        assert self._risk(39.9) == LeadResponseRisk.moderate

    def test_composite_exactly_40_is_high(self):
        assert self._risk(40.0) == LeadResponseRisk.high

    def test_composite_just_below_60_is_high(self):
        assert self._risk(59.9) == LeadResponseRisk.high

    def test_composite_exactly_60_is_critical(self):
        assert self._risk(60.0) == LeadResponseRisk.critical

    def test_composite_100_is_critical(self):
        assert self._risk(100.0) == LeadResponseRisk.critical

    def test_composite_30_is_moderate(self):
        assert self._risk(30.0) == LeadResponseRisk.moderate

    def test_composite_50_is_high(self):
        assert self._risk(50.0) == LeadResponseRisk.high

    def test_composite_70_is_critical(self):
        assert self._risk(70.0) == LeadResponseRisk.critical


class TestSeverity:
    def _severity(self, composite: float) -> LeadResponseSeverity:
        return engine()._severity(composite)

    def test_composite_0_is_responsive(self):
        assert self._severity(0.0) == LeadResponseSeverity.responsive

    def test_composite_just_below_20_is_responsive(self):
        assert self._severity(19.9) == LeadResponseSeverity.responsive

    def test_composite_exactly_20_is_delayed(self):
        assert self._severity(20.0) == LeadResponseSeverity.delayed

    def test_composite_just_below_40_is_delayed(self):
        assert self._severity(39.9) == LeadResponseSeverity.delayed

    def test_composite_exactly_40_is_lagging(self):
        assert self._severity(40.0) == LeadResponseSeverity.lagging

    def test_composite_just_below_60_is_lagging(self):
        assert self._severity(59.9) == LeadResponseSeverity.lagging

    def test_composite_exactly_60_is_critical(self):
        assert self._severity(60.0) == LeadResponseSeverity.critical

    def test_composite_100_is_critical(self):
        assert self._severity(100.0) == LeadResponseSeverity.critical

    def test_composite_25_is_delayed(self):
        assert self._severity(25.0) == LeadResponseSeverity.delayed

    def test_composite_45_is_lagging(self):
        assert self._severity(45.0) == LeadResponseSeverity.lagging

    def test_composite_80_is_critical(self):
        assert self._severity(80.0) == LeadResponseSeverity.critical


# ===========================================================================
# 8. _action tests for all risk + pattern combinations
# ===========================================================================

class TestAction:
    def _action(self, risk: LeadResponseRisk, pattern: LeadResponsePattern) -> LeadResponseAction:
        return engine()._action(risk, pattern)

    # --- critical risk ---

    def test_critical_lead_neglect_returns_lead_cadence_reset(self):
        assert self._action(LeadResponseRisk.critical, LeadResponsePattern.lead_neglect) == LeadResponseAction.lead_cadence_reset

    def test_critical_slow_response_returns_response_time_coaching(self):
        assert self._action(LeadResponseRisk.critical, LeadResponsePattern.slow_response) == LeadResponseAction.response_time_coaching

    def test_critical_none_returns_lead_prioritization(self):
        assert self._action(LeadResponseRisk.critical, LeadResponsePattern.none) == LeadResponseAction.lead_prioritization

    def test_critical_poor_qualification_returns_lead_prioritization(self):
        assert self._action(LeadResponseRisk.critical, LeadResponsePattern.poor_qualification) == LeadResponseAction.lead_prioritization

    def test_critical_low_conversion_returns_lead_prioritization(self):
        assert self._action(LeadResponseRisk.critical, LeadResponsePattern.low_conversion) == LeadResponseAction.lead_prioritization

    def test_critical_icp_miss_returns_lead_prioritization(self):
        assert self._action(LeadResponseRisk.critical, LeadResponsePattern.icp_miss) == LeadResponseAction.lead_prioritization

    # --- high risk ---

    def test_high_poor_qualification_returns_qualification_training(self):
        assert self._action(LeadResponseRisk.high, LeadResponsePattern.poor_qualification) == LeadResponseAction.qualification_training

    def test_high_icp_miss_returns_lead_prioritization(self):
        assert self._action(LeadResponseRisk.high, LeadResponsePattern.icp_miss) == LeadResponseAction.lead_prioritization

    def test_high_none_returns_crm_discipline(self):
        assert self._action(LeadResponseRisk.high, LeadResponsePattern.none) == LeadResponseAction.crm_discipline

    def test_high_slow_response_returns_crm_discipline(self):
        assert self._action(LeadResponseRisk.high, LeadResponsePattern.slow_response) == LeadResponseAction.crm_discipline

    def test_high_lead_neglect_returns_crm_discipline(self):
        assert self._action(LeadResponseRisk.high, LeadResponsePattern.lead_neglect) == LeadResponseAction.crm_discipline

    def test_high_low_conversion_returns_crm_discipline(self):
        assert self._action(LeadResponseRisk.high, LeadResponsePattern.low_conversion) == LeadResponseAction.crm_discipline

    # --- moderate risk ---

    def test_moderate_none_returns_response_time_coaching(self):
        assert self._action(LeadResponseRisk.moderate, LeadResponsePattern.none) == LeadResponseAction.response_time_coaching

    def test_moderate_slow_response_returns_response_time_coaching(self):
        assert self._action(LeadResponseRisk.moderate, LeadResponsePattern.slow_response) == LeadResponseAction.response_time_coaching

    def test_moderate_poor_qualification_returns_response_time_coaching(self):
        assert self._action(LeadResponseRisk.moderate, LeadResponsePattern.poor_qualification) == LeadResponseAction.response_time_coaching

    def test_moderate_low_conversion_returns_response_time_coaching(self):
        assert self._action(LeadResponseRisk.moderate, LeadResponsePattern.low_conversion) == LeadResponseAction.response_time_coaching

    def test_moderate_lead_neglect_returns_response_time_coaching(self):
        assert self._action(LeadResponseRisk.moderate, LeadResponsePattern.lead_neglect) == LeadResponseAction.response_time_coaching

    def test_moderate_icp_miss_returns_response_time_coaching(self):
        assert self._action(LeadResponseRisk.moderate, LeadResponsePattern.icp_miss) == LeadResponseAction.response_time_coaching

    # --- low risk ---

    def test_low_none_returns_no_action(self):
        assert self._action(LeadResponseRisk.low, LeadResponsePattern.none) == LeadResponseAction.no_action

    def test_low_slow_response_returns_no_action(self):
        assert self._action(LeadResponseRisk.low, LeadResponsePattern.slow_response) == LeadResponseAction.no_action

    def test_low_poor_qualification_returns_no_action(self):
        assert self._action(LeadResponseRisk.low, LeadResponsePattern.poor_qualification) == LeadResponseAction.no_action

    def test_low_low_conversion_returns_no_action(self):
        assert self._action(LeadResponseRisk.low, LeadResponsePattern.low_conversion) == LeadResponseAction.no_action

    def test_low_lead_neglect_returns_no_action(self):
        assert self._action(LeadResponseRisk.low, LeadResponsePattern.lead_neglect) == LeadResponseAction.no_action

    def test_low_icp_miss_returns_no_action(self):
        assert self._action(LeadResponseRisk.low, LeadResponsePattern.icp_miss) == LeadResponseAction.no_action


# ===========================================================================
# 9. _has_response_gap tests
# ===========================================================================

class TestHasResponseGap:
    def _gap(self, composite: float, **kwargs) -> bool:
        e = engine()
        inp = make_input(**kwargs)
        return e._has_response_gap(composite, inp)

    # composite >= 40 triggers

    def test_composite_40_triggers(self):
        assert self._gap(40.0) is True

    def test_composite_39_9_no_trigger_alone(self):
        # composite < 40, avg_first_response_hours=1.0, never_rate=0
        assert self._gap(39.9, avg_first_response_hours=1.0, leads_never_contacted=0) is False

    def test_composite_100_triggers(self):
        assert self._gap(100.0) is True

    def test_composite_0_no_trigger_alone(self):
        assert self._gap(0.0, avg_first_response_hours=1.0, leads_never_contacted=0) is False

    # avg_first_response_hours >= 12 triggers

    def test_avg_response_12_triggers(self):
        assert self._gap(0.0, avg_first_response_hours=12.0, leads_never_contacted=0) is True

    def test_avg_response_11_9_no_trigger_alone(self):
        assert self._gap(0.0, avg_first_response_hours=11.9, leads_never_contacted=0) is False

    def test_avg_response_24_triggers(self):
        assert self._gap(0.0, avg_first_response_hours=24.0, leads_never_contacted=0) is True

    def test_avg_response_0_no_trigger_alone(self):
        assert self._gap(0.0, avg_first_response_hours=0.0, leads_never_contacted=0) is False

    # never_rate >= 0.10 triggers

    def test_never_rate_10pct_triggers(self):
        # 10/100 = 0.10
        assert self._gap(0.0, inbound_leads_assigned=100, leads_never_contacted=10,
                         avg_first_response_hours=1.0) is True

    def test_never_rate_9pct_no_trigger_alone(self):
        # 9/100 = 0.09
        assert self._gap(0.0, inbound_leads_assigned=100, leads_never_contacted=9,
                         avg_first_response_hours=1.0) is False

    def test_never_rate_50pct_triggers(self):
        assert self._gap(0.0, inbound_leads_assigned=100, leads_never_contacted=50,
                         avg_first_response_hours=1.0) is True

    # OR logic: any one condition triggers

    def test_or_logic_only_composite(self):
        assert self._gap(40.0, avg_first_response_hours=1.0, leads_never_contacted=0) is True

    def test_or_logic_only_avg_hours(self):
        assert self._gap(0.0, avg_first_response_hours=12.0, leads_never_contacted=0) is True

    def test_or_logic_only_never_rate(self):
        assert self._gap(0.0, avg_first_response_hours=1.0,
                         inbound_leads_assigned=100, leads_never_contacted=10) is True

    def test_or_logic_all_false_returns_false(self):
        assert self._gap(0.0, avg_first_response_hours=1.0,
                         inbound_leads_assigned=100, leads_never_contacted=0) is False


# ===========================================================================
# 10. _requires_lead_coaching tests
# ===========================================================================

class TestRequiresLeadCoaching:
    def _coaching(self, composite: float, **kwargs) -> bool:
        e = engine()
        inp = make_input(**kwargs)
        return e._requires_lead_coaching(composite, inp)

    # composite >= 30 triggers

    def test_composite_30_triggers(self):
        assert self._coaching(30.0) is True

    def test_composite_29_9_no_trigger_alone(self):
        assert self._coaching(29.9, avg_lead_qualification_score=7.0,
                               lead_to_qualified_conversion_rate_pct=0.50) is False

    def test_composite_100_triggers(self):
        assert self._coaching(100.0) is True

    def test_composite_0_no_trigger_alone(self):
        assert self._coaching(0.0, avg_lead_qualification_score=7.0,
                               lead_to_qualified_conversion_rate_pct=0.50) is False

    # avg_lead_qualification_score < 5.0 triggers

    def test_qual_score_below_5_triggers(self):
        assert self._coaching(0.0, avg_lead_qualification_score=4.9,
                               lead_to_qualified_conversion_rate_pct=0.50) is True

    def test_qual_score_exactly_5_no_trigger_alone(self):
        assert self._coaching(0.0, avg_lead_qualification_score=5.0,
                               lead_to_qualified_conversion_rate_pct=0.50) is False

    def test_qual_score_above_5_no_trigger_alone(self):
        assert self._coaching(0.0, avg_lead_qualification_score=6.0,
                               lead_to_qualified_conversion_rate_pct=0.50) is False

    def test_qual_score_0_triggers(self):
        assert self._coaching(0.0, avg_lead_qualification_score=0.0,
                               lead_to_qualified_conversion_rate_pct=0.50) is True

    # lead_to_qualified_conversion_rate_pct < 0.30 triggers

    def test_l2q_below_30pct_triggers(self):
        assert self._coaching(0.0, avg_lead_qualification_score=7.0,
                               lead_to_qualified_conversion_rate_pct=0.29) is True

    def test_l2q_exactly_30pct_no_trigger_alone(self):
        assert self._coaching(0.0, avg_lead_qualification_score=7.0,
                               lead_to_qualified_conversion_rate_pct=0.30) is False

    def test_l2q_above_30pct_no_trigger_alone(self):
        assert self._coaching(0.0, avg_lead_qualification_score=7.0,
                               lead_to_qualified_conversion_rate_pct=0.50) is False

    def test_l2q_0_triggers(self):
        assert self._coaching(0.0, avg_lead_qualification_score=7.0,
                               lead_to_qualified_conversion_rate_pct=0.0) is True

    # OR logic

    def test_or_logic_only_composite(self):
        assert self._coaching(30.0, avg_lead_qualification_score=7.0,
                               lead_to_qualified_conversion_rate_pct=0.50) is True

    def test_or_logic_only_qual_score(self):
        assert self._coaching(0.0, avg_lead_qualification_score=4.0,
                               lead_to_qualified_conversion_rate_pct=0.50) is True

    def test_or_logic_only_l2q(self):
        assert self._coaching(0.0, avg_lead_qualification_score=7.0,
                               lead_to_qualified_conversion_rate_pct=0.20) is True

    def test_or_logic_all_false_returns_false(self):
        assert self._coaching(0.0, avg_lead_qualification_score=7.0,
                               lead_to_qualified_conversion_rate_pct=0.50) is False


# ===========================================================================
# 11. estimated_lost_pipeline tests
# ===========================================================================

class TestEstimatedLostPipeline:
    def _lost(self, **kwargs) -> float:
        e = engine()
        inp = make_input(**kwargs)
        composite = round(e._response_speed_score(inp) * 0.30 +
                          e._qualification_quality_score(inp) * 0.30 +
                          e._lead_conversion_score(inp) * 0.25 +
                          e._lead_discipline_score(inp) * 0.15, 1)
        return e._estimated_lost_pipeline(inp, composite)

    def _lost_direct(self, composite: float, **kwargs) -> float:
        e = engine()
        inp = make_input(**kwargs)
        return e._estimated_lost_pipeline(inp, composite)

    def test_zero_never_contacted_zero_lost(self):
        assert self._lost_direct(50.0, leads_never_contacted=0, avg_lead_revenue_potential_usd=10_000) == 0.0

    def test_formula_basic(self):
        # 10 * 5000 * (50/100) = 25000
        result = self._lost_direct(50.0,
                                    leads_never_contacted=10,
                                    avg_lead_revenue_potential_usd=5_000.0)
        assert result == 25_000.0

    def test_formula_composite_100(self):
        # 5 * 10000 * 1.0 = 50000
        result = self._lost_direct(100.0,
                                    leads_never_contacted=5,
                                    avg_lead_revenue_potential_usd=10_000.0)
        assert result == 50_000.0

    def test_formula_composite_0(self):
        # 5 * 10000 * 0.0 = 0
        result = self._lost_direct(0.0,
                                    leads_never_contacted=5,
                                    avg_lead_revenue_potential_usd=10_000.0)
        assert result == 0.0

    def test_formula_rounds_to_2_decimals(self):
        # 3 * 3333.33 * (33.0/100) = 3299.9967 → rounds to 3300.0
        result = self._lost_direct(33.0,
                                    leads_never_contacted=3,
                                    avg_lead_revenue_potential_usd=3333.33)
        assert result == round(3 * 3333.33 * 0.33, 2)

    def test_formula_fractional_revenue(self):
        result = self._lost_direct(50.0,
                                    leads_never_contacted=1,
                                    avg_lead_revenue_potential_usd=1.5)
        assert result == 0.75

    def test_zero_composite_zero_lost_regardless_of_leads(self):
        result = self._lost_direct(0.0,
                                    leads_never_contacted=100,
                                    avg_lead_revenue_potential_usd=50_000.0)
        assert result == 0.0


# ===========================================================================
# 12. _signal tests
# ===========================================================================

class TestSignal:
    def _signal(self, pattern: LeadResponsePattern, composite: float, **kwargs) -> str:
        e = engine()
        inp = make_input(**kwargs)
        return e._signal(inp, pattern, composite)

    def test_none_pattern_low_composite_returns_benchmark_message(self):
        sig = self._signal(LeadResponsePattern.none, 10.0)
        assert sig == "Inbound lead response rate and quality within benchmarks"

    def test_none_pattern_composite_exactly_20_not_benchmark(self):
        # composite=20 >= 20 → NOT benchmark
        sig = self._signal(LeadResponsePattern.none, 20.0)
        assert "within benchmarks" not in sig

    def test_non_none_pattern_low_composite_not_benchmark(self):
        sig = self._signal(LeadResponsePattern.slow_response, 5.0)
        assert "within benchmarks" not in sig

    def test_signal_includes_pattern_label(self):
        sig = self._signal(LeadResponsePattern.slow_response, 40.0,
                           leads_never_contacted=0,
                           avg_first_response_hours=1.0,
                           leads_lost_to_competitor_before_contact=0)
        assert "Slow response" in sig

    def test_signal_includes_lead_neglect_label(self):
        sig = self._signal(LeadResponsePattern.lead_neglect, 50.0,
                           leads_never_contacted=0,
                           avg_first_response_hours=1.0,
                           leads_lost_to_competitor_before_contact=0)
        assert "Lead neglect" in sig

    def test_signal_includes_icp_miss_label(self):
        sig = self._signal(LeadResponsePattern.icp_miss, 50.0,
                           leads_never_contacted=0,
                           avg_first_response_hours=1.0,
                           leads_lost_to_competitor_before_contact=0)
        assert "Icp miss" in sig

    def test_signal_includes_never_contacted_count(self):
        sig = self._signal(LeadResponsePattern.none, 25.0,
                           leads_never_contacted=5,
                           avg_first_response_hours=1.0,
                           leads_lost_to_competitor_before_contact=0)
        assert "5 leads never contacted" in sig

    def test_signal_includes_avg_response_time_when_ge4(self):
        sig = self._signal(LeadResponsePattern.none, 25.0,
                           leads_never_contacted=0,
                           avg_first_response_hours=8.0,
                           leads_lost_to_competitor_before_contact=0)
        assert "8h avg response time" in sig

    def test_signal_excludes_avg_response_time_when_below_4(self):
        sig = self._signal(LeadResponsePattern.none, 25.0,
                           leads_never_contacted=0,
                           avg_first_response_hours=3.9,
                           leads_lost_to_competitor_before_contact=0)
        assert "avg response time" not in sig

    def test_signal_includes_competitor_loss(self):
        sig = self._signal(LeadResponsePattern.none, 25.0,
                           leads_never_contacted=0,
                           avg_first_response_hours=1.0,
                           leads_lost_to_competitor_before_contact=3)
        assert "3 lost to competitor" in sig

    def test_signal_excludes_competitor_when_zero(self):
        sig = self._signal(LeadResponsePattern.none, 25.0,
                           leads_never_contacted=0,
                           avg_first_response_hours=1.0,
                           leads_lost_to_competitor_before_contact=0)
        assert "lost to competitor" not in sig

    def test_signal_includes_composite(self):
        sig = self._signal(LeadResponsePattern.none, 35.0,
                           leads_never_contacted=0,
                           avg_first_response_hours=1.0,
                           leads_lost_to_competitor_before_contact=0)
        assert "composite 35" in sig

    def test_signal_fallback_when_no_parts(self):
        sig = self._signal(LeadResponsePattern.none, 25.0,
                           leads_never_contacted=0,
                           avg_first_response_hours=1.0,
                           leads_lost_to_competitor_before_contact=0)
        assert "lead response quality degrading" in sig

    def test_signal_none_pattern_ge20_uses_lead_response_risk_label(self):
        sig = self._signal(LeadResponsePattern.none, 25.0,
                           leads_never_contacted=5,
                           avg_first_response_hours=1.0,
                           leads_lost_to_competitor_before_contact=0)
        assert "Lead response risk" in sig

    def test_signal_avg_response_exactly_4_included(self):
        sig = self._signal(LeadResponsePattern.none, 25.0,
                           leads_never_contacted=0,
                           avg_first_response_hours=4.0,
                           leads_lost_to_competitor_before_contact=0)
        assert "4h avg response time" in sig

    def test_signal_all_parts_combined(self):
        sig = self._signal(LeadResponsePattern.slow_response, 50.0,
                           leads_never_contacted=3,
                           avg_first_response_hours=12.0,
                           leads_lost_to_competitor_before_contact=2)
        assert "3 leads never contacted" in sig
        assert "12h avg response time" in sig
        assert "2 lost to competitor" in sig


# ===========================================================================
# 13. assess() full integration tests
# ===========================================================================

class TestAssess:
    def test_returns_inbound_lead_response_result(self):
        e = engine()
        result = e.assess(make_input())
        assert isinstance(result, InboundLeadResponseResult)

    def test_rep_id_preserved(self):
        e = engine()
        result = e.assess(make_input(rep_id="sales99"))
        assert result.rep_id == "sales99"

    def test_region_preserved(self):
        e = engine()
        result = e.assess(make_input(region="Pacific"))
        assert result.region == "Pacific"

    def test_to_dict_has_15_keys(self):
        e = engine()
        result = e.assess(make_input())
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_exact_keys(self):
        e = engine()
        result = e.assess(make_input())
        d = result.to_dict()
        expected_keys = {
            "rep_id", "region", "lead_response_risk", "lead_response_pattern",
            "lead_response_severity", "recommended_action", "response_speed_score",
            "qualification_quality_score", "lead_conversion_score", "lead_discipline_score",
            "lead_response_composite", "has_response_gap", "requires_lead_coaching",
            "estimated_lost_pipeline_usd", "lead_response_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enums_serialized_as_strings(self):
        e = engine()
        result = e.assess(make_input())
        d = result.to_dict()
        assert isinstance(d["lead_response_risk"], str)
        assert isinstance(d["lead_response_pattern"], str)
        assert isinstance(d["lead_response_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_composite_within_0_100(self):
        e = engine()
        result = e.assess(make_input())
        assert 0.0 <= result.lead_response_composite <= 100.0

    def test_sub_scores_within_0_100(self):
        e = engine()
        result = e.assess(make_input())
        assert 0.0 <= result.response_speed_score <= 100.0
        assert 0.0 <= result.qualification_quality_score <= 100.0
        assert 0.0 <= result.lead_conversion_score <= 100.0
        assert 0.0 <= result.lead_discipline_score <= 100.0

    def test_ideal_input_low_risk(self):
        e = engine()
        result = e.assess(make_input())
        assert result.lead_response_risk == LeadResponseRisk.low

    def test_ideal_input_no_pattern(self):
        e = engine()
        result = e.assess(make_input())
        assert result.lead_response_pattern == LeadResponsePattern.none

    def test_ideal_input_responsive_severity(self):
        e = engine()
        result = e.assess(make_input())
        assert result.lead_response_severity == LeadResponseSeverity.responsive

    def test_ideal_input_no_action(self):
        e = engine()
        result = e.assess(make_input())
        assert result.recommended_action == LeadResponseAction.no_action

    def test_ideal_input_no_response_gap(self):
        e = engine()
        result = e.assess(make_input())
        assert result.has_response_gap is False

    def test_ideal_input_no_coaching_required(self):
        e = engine()
        result = e.assess(make_input())
        assert result.requires_lead_coaching is False

    def test_ideal_input_zero_lost_pipeline(self):
        e = engine()
        result = e.assess(make_input(leads_never_contacted=0))
        assert result.estimated_lost_pipeline_usd == 0.0

    def test_result_stored_in_internal_list(self):
        e = engine()
        e.assess(make_input())
        assert len(e._results) == 1

    def test_multiple_assessments_stored(self):
        e = engine()
        e.assess(make_input(rep_id="r1"))
        e.assess(make_input(rep_id="r2"))
        e.assess(make_input(rep_id="r3"))
        assert len(e._results) == 3

    def test_poor_performer_critical_risk(self):
        inp = make_input(
            avg_first_response_hours=30.0,
            leads_contacted_over_24h=60,
            leads_contacted_within_1h=5,
            leads_never_contacted=25,
            lead_to_qualified_conversion_rate_pct=0.10,
            qualified_to_opportunity_conversion_rate_pct=0.20,
            avg_lead_qualification_score=3.0,
            avg_response_quality_score=3.0,
            leads_disqualified_too_early=25,
            crm_lead_entry_rate_pct=0.40,
            leads_lost_to_competitor_before_contact=5,
            high_icp_leads_received=5,
            high_icp_leads_converted=0,
            inbound_leads_assigned=100,
        )
        e = engine()
        result = e.assess(inp)
        assert result.lead_response_risk == LeadResponseRisk.critical
        assert result.has_response_gap is True
        assert result.requires_lead_coaching is True

    def test_composite_formula_correct(self):
        e = engine()
        inp = make_input()
        speed = e._response_speed_score(inp)
        quality = e._qualification_quality_score(inp)
        conversion = e._lead_conversion_score(inp)
        discipline = e._lead_discipline_score(inp)
        expected = round(speed * 0.30 + quality * 0.30 + conversion * 0.25 + discipline * 0.15, 1)
        result = e.assess(inp)
        assert result.lead_response_composite == min(expected, 100.0)

    def test_signal_is_string(self):
        e = engine()
        result = e.assess(make_input())
        assert isinstance(result.lead_response_signal, str)

    def test_estimated_lost_pipeline_positive_when_leads_never_contacted(self):
        e = engine()
        inp = make_input(leads_never_contacted=5, avg_lead_revenue_potential_usd=10_000.0,
                         avg_first_response_hours=24.0,
                         leads_contacted_over_24h=50,
                         lead_to_qualified_conversion_rate_pct=0.10)
        result = e.assess(inp)
        assert result.estimated_lost_pipeline_usd > 0.0


# ===========================================================================
# 14. to_dict content validation
# ===========================================================================

class TestToDict:
    def test_risk_value_in_dict(self):
        e = engine()
        result = e.assess(make_input())
        d = result.to_dict()
        assert d["lead_response_risk"] == result.lead_response_risk.value

    def test_pattern_value_in_dict(self):
        e = engine()
        result = e.assess(make_input())
        d = result.to_dict()
        assert d["lead_response_pattern"] == result.lead_response_pattern.value

    def test_severity_value_in_dict(self):
        e = engine()
        result = e.assess(make_input())
        d = result.to_dict()
        assert d["lead_response_severity"] == result.lead_response_severity.value

    def test_action_value_in_dict(self):
        e = engine()
        result = e.assess(make_input())
        d = result.to_dict()
        assert d["recommended_action"] == result.recommended_action.value

    def test_scores_in_dict_match_result(self):
        e = engine()
        result = e.assess(make_input())
        d = result.to_dict()
        assert d["response_speed_score"] == result.response_speed_score
        assert d["qualification_quality_score"] == result.qualification_quality_score
        assert d["lead_conversion_score"] == result.lead_conversion_score
        assert d["lead_discipline_score"] == result.lead_discipline_score

    def test_flags_in_dict_match_result(self):
        e = engine()
        result = e.assess(make_input())
        d = result.to_dict()
        assert d["has_response_gap"] == result.has_response_gap
        assert d["requires_lead_coaching"] == result.requires_lead_coaching

    def test_rep_id_and_region_in_dict(self):
        e = engine()
        result = e.assess(make_input(rep_id="xyz", region="North"))
        d = result.to_dict()
        assert d["rep_id"] == "xyz"
        assert d["region"] == "North"


# ===========================================================================
# 15. assess_batch tests
# ===========================================================================

class TestAssessBatch:
    def test_empty_batch_returns_empty_list(self):
        e = engine()
        result = e.assess_batch([])
        assert result == []

    def test_batch_returns_correct_count(self):
        e = engine()
        inputs = [make_input(rep_id=f"r{i}") for i in range(5)]
        results = e.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_all_results_are_correct_type(self):
        e = engine()
        inputs = [make_input(rep_id=f"r{i}") for i in range(3)]
        results = e.assess_batch(inputs)
        assert all(isinstance(r, InboundLeadResponseResult) for r in results)

    def test_batch_stores_all_in_internal_list(self):
        e = engine()
        inputs = [make_input(rep_id=f"r{i}") for i in range(4)]
        e.assess_batch(inputs)
        assert len(e._results) == 4

    def test_batch_rep_ids_match_inputs(self):
        e = engine()
        inputs = [make_input(rep_id=f"rep{i}") for i in range(3)]
        results = e.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"rep{i}"

    def test_batch_single_input(self):
        e = engine()
        result = e.assess_batch([make_input(rep_id="solo")])
        assert len(result) == 1
        assert result[0].rep_id == "solo"

    def test_batch_accumulates_across_calls(self):
        e = engine()
        e.assess_batch([make_input(rep_id="a"), make_input(rep_id="b")])
        e.assess_batch([make_input(rep_id="c")])
        assert len(e._results) == 3

    def test_batch_with_mixed_risk_levels(self):
        e = engine()
        good = make_input()
        bad = make_input(
            avg_first_response_hours=30.0,
            leads_contacted_over_24h=60,
            leads_contacted_within_1h=5,
            leads_never_contacted=25,
            lead_to_qualified_conversion_rate_pct=0.10,
            qualified_to_opportunity_conversion_rate_pct=0.20,
            avg_lead_qualification_score=3.0,
            avg_response_quality_score=3.0,
            leads_disqualified_too_early=25,
            crm_lead_entry_rate_pct=0.40,
            inbound_leads_assigned=100,
        )
        results = e.assess_batch([good, bad])
        assert results[0].lead_response_risk == LeadResponseRisk.low
        assert results[1].lead_response_risk == LeadResponseRisk.critical


# ===========================================================================
# 16. summary() tests
# ===========================================================================

class TestSummary:
    def test_empty_summary_has_13_keys(self):
        e = engine()
        s = e.summary()
        assert len(s) == 13

    def test_empty_summary_exact_keys(self):
        e = engine()
        s = e.summary()
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts", "action_counts",
            "avg_lead_response_composite", "response_gap_count", "lead_coaching_count",
            "avg_response_speed_score", "avg_qualification_quality_score",
            "avg_lead_conversion_score", "avg_lead_discipline_score",
            "total_estimated_lost_pipeline_usd",
        }
        assert set(s.keys()) == expected_keys

    def test_empty_summary_total_zero(self):
        e = engine()
        assert e.summary()["total"] == 0

    def test_empty_summary_counts_empty_dicts(self):
        e = engine()
        s = e.summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}

    def test_empty_summary_zero_averages(self):
        e = engine()
        s = e.summary()
        assert s["avg_lead_response_composite"] == 0.0
        assert s["avg_response_speed_score"] == 0.0
        assert s["avg_qualification_quality_score"] == 0.0
        assert s["avg_lead_conversion_score"] == 0.0
        assert s["avg_lead_discipline_score"] == 0.0

    def test_empty_summary_zero_counts(self):
        e = engine()
        s = e.summary()
        assert s["response_gap_count"] == 0
        assert s["lead_coaching_count"] == 0
        assert s["total_estimated_lost_pipeline_usd"] == 0.0

    def test_summary_after_one_assess_total_1(self):
        e = engine()
        e.assess(make_input())
        assert e.summary()["total"] == 1

    def test_summary_after_batch_total_correct(self):
        e = engine()
        e.assess_batch([make_input(rep_id=f"r{i}") for i in range(5)])
        assert e.summary()["total"] == 5

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
        assert "responsive" in s["severity_counts"]

    def test_summary_action_counts_populated(self):
        e = engine()
        e.assess(make_input())
        s = e.summary()
        assert "no_action" in s["action_counts"]

    def test_summary_avg_composite_correct(self):
        e = engine()
        r1 = e.assess(make_input(rep_id="r1"))
        r2 = e.assess(make_input(rep_id="r2"))
        expected = round((r1.lead_response_composite + r2.lead_response_composite) / 2, 1)
        assert e.summary()["avg_lead_response_composite"] == expected

    def test_summary_response_gap_count(self):
        e = engine()
        # Force a gap: avg_first_response_hours >= 12
        e.assess(make_input(avg_first_response_hours=12.0))
        e.assess(make_input(avg_first_response_hours=1.0, leads_never_contacted=0))
        s = e.summary()
        assert s["response_gap_count"] == 1

    def test_summary_lead_coaching_count(self):
        e = engine()
        e.assess(make_input(avg_lead_qualification_score=4.0))  # triggers coaching
        e.assess(make_input())  # no coaching
        s = e.summary()
        assert s["lead_coaching_count"] == 1

    def test_summary_total_estimated_lost_pipeline_sums_correctly(self):
        e = engine()
        r1 = e.assess(make_input(leads_never_contacted=5,
                                  avg_lead_revenue_potential_usd=10_000.0,
                                  avg_first_response_hours=24.0,
                                  leads_contacted_over_24h=50,
                                  lead_to_qualified_conversion_rate_pct=0.10))
        r2 = e.assess(make_input(leads_never_contacted=0))
        s = e.summary()
        assert s["total_estimated_lost_pipeline_usd"] == round(
            r1.estimated_lost_pipeline_usd + r2.estimated_lost_pipeline_usd, 2
        )

    def test_summary_has_13_keys_after_assessments(self):
        e = engine()
        e.assess(make_input())
        s = e.summary()
        assert len(s) == 13

    def test_summary_avg_speed_score_correct(self):
        e = engine()
        r1 = e.assess(make_input(rep_id="r1"))
        r2 = e.assess(make_input(rep_id="r2"))
        expected = round((r1.response_speed_score + r2.response_speed_score) / 2, 1)
        assert e.summary()["avg_response_speed_score"] == expected

    def test_summary_avg_qualification_score_correct(self):
        e = engine()
        r1 = e.assess(make_input(rep_id="r1"))
        r2 = e.assess(make_input(rep_id="r2"))
        expected = round((r1.qualification_quality_score + r2.qualification_quality_score) / 2, 1)
        assert e.summary()["avg_qualification_quality_score"] == expected

    def test_summary_avg_conversion_score_correct(self):
        e = engine()
        r1 = e.assess(make_input(rep_id="r1"))
        r2 = e.assess(make_input(rep_id="r2"))
        expected = round((r1.lead_conversion_score + r2.lead_conversion_score) / 2, 1)
        assert e.summary()["avg_lead_conversion_score"] == expected

    def test_summary_avg_discipline_score_correct(self):
        e = engine()
        r1 = e.assess(make_input(rep_id="r1"))
        r2 = e.assess(make_input(rep_id="r2"))
        expected = round((r1.lead_discipline_score + r2.lead_discipline_score) / 2, 1)
        assert e.summary()["avg_lead_discipline_score"] == expected

    def test_summary_multiple_risk_levels_counted(self):
        e = engine()
        # ideal = low
        e.assess(make_input())
        # bad = critical
        e.assess(make_input(
            avg_first_response_hours=30.0,
            leads_contacted_over_24h=60,
            leads_contacted_within_1h=5,
            leads_never_contacted=25,
            lead_to_qualified_conversion_rate_pct=0.10,
            qualified_to_opportunity_conversion_rate_pct=0.20,
            avg_lead_qualification_score=3.0,
            avg_response_quality_score=3.0,
            leads_disqualified_too_early=25,
            crm_lead_entry_rate_pct=0.40,
            inbound_leads_assigned=100,
        ))
        s = e.summary()
        assert s["risk_counts"].get("low", 0) >= 1
        assert s["risk_counts"].get("critical", 0) >= 1


# ===========================================================================
# 17. Edge cases and additional coverage
# ===========================================================================

class TestEdgeCases:
    def test_engine_initializes_empty_results(self):
        e = engine()
        assert e._results == []

    def test_inbound_lead_response_input_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(InboundLeadResponseInput)

    def test_inbound_lead_response_result_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(InboundLeadResponseResult)

    def test_assess_with_zero_leads_assigned(self):
        e = engine()
        inp = make_input(inbound_leads_assigned=0,
                         leads_contacted_over_24h=0,
                         leads_contacted_within_1h=0,
                         leads_never_contacted=0)
        result = e.assess(inp)
        assert isinstance(result, InboundLeadResponseResult)

    def test_assess_with_very_high_values(self):
        e = engine()
        inp = make_input(inbound_leads_assigned=10_000,
                         leads_contacted_over_24h=4_000,
                         leads_contacted_within_1h=500,
                         leads_never_contacted=1_000,
                         avg_first_response_hours=48.0)
        result = e.assess(inp)
        assert result.lead_response_composite <= 100.0

    def test_never_contacted_exceeds_assigned_uses_real_rate(self):
        # leads_never_contacted > inbound_leads_assigned is edge case
        e = engine()
        inp = make_input(inbound_leads_assigned=10,
                         leads_never_contacted=5,
                         avg_first_response_hours=1.0)
        result = e.assess(inp)
        # never_rate = 5/10 = 0.50 >= 0.20 → discipline score gets 40 component
        assert result.has_response_gap is True

    def test_rep_id_is_string(self):
        e = engine()
        result = e.assess(make_input(rep_id="test_rep"))
        assert result.rep_id == "test_rep"

    def test_multiple_engines_independent(self):
        e1 = SalesInboundLeadResponseEngine()
        e2 = SalesInboundLeadResponseEngine()
        e1.assess(make_input(rep_id="r1"))
        assert len(e1._results) == 1
        assert len(e2._results) == 0

    def test_assess_slow_response_pattern(self):
        e = engine()
        inp = make_input(
            avg_first_response_hours=15.0,
            leads_contacted_over_24h=40,
            leads_contacted_within_1h=5,
            leads_never_contacted=5,
            inbound_leads_assigned=100,
            lead_to_qualified_conversion_rate_pct=0.50,
            avg_lead_qualification_score=7.0,
        )
        result = e.assess(inp)
        assert result.lead_response_pattern == LeadResponsePattern.slow_response

    def test_assess_lead_neglect_pattern(self):
        e = engine()
        inp = make_input(
            inbound_leads_assigned=100,
            leads_never_contacted=20,
            avg_first_response_hours=1.0,
            crm_lead_entry_rate_pct=0.40,
            leads_lost_to_competitor_before_contact=5,
        )
        result = e.assess(inp)
        assert result.lead_response_pattern == LeadResponsePattern.lead_neglect

    def test_assess_icp_miss_pattern(self):
        e = engine()
        inp = make_input(
            leads_never_contacted=0,
            avg_first_response_hours=1.0,
            high_icp_leads_received=10,
            high_icp_leads_converted=1,  # 0.10 < 0.30
            lead_to_qualified_conversion_rate_pct=0.15,  # drives conversion score up
            qualified_to_opportunity_conversion_rate_pct=0.30,
        )
        result = e.assess(inp)
        assert result.lead_response_pattern == LeadResponsePattern.icp_miss

    def test_assess_poor_qualification_pattern(self):
        e = engine()
        inp = make_input(
            leads_never_contacted=0,
            avg_first_response_hours=1.0,
            leads_contacted_over_24h=0,
            leads_contacted_within_1h=60,
            high_icp_leads_received=0,
            avg_lead_qualification_score=3.0,
            avg_response_quality_score=3.0,
            leads_disqualified_too_early=20,
            lead_to_qualified_conversion_rate_pct=0.50,
            qualified_to_opportunity_conversion_rate_pct=0.65,
            crm_lead_entry_rate_pct=0.95,
            leads_lost_to_competitor_before_contact=0,
            inbound_leads_assigned=100,
        )
        result = e.assess(inp)
        assert result.lead_response_pattern == LeadResponsePattern.poor_qualification

    def test_assess_low_conversion_pattern(self):
        e = engine()
        inp = make_input(
            leads_never_contacted=0,
            avg_first_response_hours=1.0,
            leads_contacted_over_24h=0,
            leads_contacted_within_1h=60,
            high_icp_leads_received=0,
            avg_lead_qualification_score=7.0,
            avg_response_quality_score=7.0,
            leads_disqualified_too_early=0,
            lead_to_qualified_conversion_rate_pct=0.15,  # triggers conversion score
            qualified_to_opportunity_conversion_rate_pct=0.30,
            crm_lead_entry_rate_pct=0.95,
            leads_lost_to_competitor_before_contact=0,
            inbound_leads_assigned=100,
        )
        result = e.assess(inp)
        assert result.lead_response_pattern == LeadResponsePattern.low_conversion

    def test_assess_single_lead_assigned(self):
        e = engine()
        inp = make_input(inbound_leads_assigned=1,
                         leads_contacted_over_24h=0,
                         leads_contacted_within_1h=1,
                         leads_never_contacted=0)
        result = e.assess(inp)
        assert isinstance(result, InboundLeadResponseResult)

    def test_response_speed_score_is_rounded_to_1_decimal(self):
        e = engine()
        inp = make_input()
        score = e._response_speed_score(inp)
        result = e.assess(inp)
        assert result.response_speed_score == round(score, 1)

    def test_qualification_quality_score_is_rounded_to_1_decimal(self):
        e = engine()
        inp = make_input()
        score = e._qualification_quality_score(inp)
        result = e.assess(inp)
        assert result.qualification_quality_score == round(score, 1)

    def test_lead_conversion_score_is_rounded_to_1_decimal(self):
        e = engine()
        inp = make_input()
        score = e._lead_conversion_score(inp)
        result = e.assess(inp)
        assert result.lead_conversion_score == round(score, 1)

    def test_lead_discipline_score_is_rounded_to_1_decimal(self):
        e = engine()
        inp = make_input()
        score = e._lead_discipline_score(inp)
        result = e.assess(inp)
        assert result.lead_discipline_score == round(score, 1)

    def test_assess_with_all_leads_never_contacted(self):
        e = engine()
        inp = make_input(inbound_leads_assigned=100,
                         leads_never_contacted=100,
                         crm_lead_entry_rate_pct=0.0,
                         leads_lost_to_competitor_before_contact=5)
        result = e.assess(inp)
        assert result.estimated_lost_pipeline_usd > 0.0
        assert result.has_response_gap is True

    def test_assessment_signal_not_empty(self):
        e = engine()
        result = e.assess(make_input())
        assert len(result.lead_response_signal) > 0

    def test_risk_and_severity_consistent(self):
        """risk level names should align with severity names at same composite boundaries"""
        e = engine()
        for composite in [5.0, 25.0, 45.0, 65.0]:
            risk = e._risk_level(composite)
            sev = e._severity(composite)
            # Both use same thresholds — check they map consistently
            if composite < 20:
                assert risk == LeadResponseRisk.low
                assert sev == LeadResponseSeverity.responsive
            elif composite < 40:
                assert risk == LeadResponseRisk.moderate
                assert sev == LeadResponseSeverity.delayed
            elif composite < 60:
                assert risk == LeadResponseRisk.high
                assert sev == LeadResponseSeverity.lagging
            else:
                assert risk == LeadResponseRisk.critical
                assert sev == LeadResponseSeverity.critical
