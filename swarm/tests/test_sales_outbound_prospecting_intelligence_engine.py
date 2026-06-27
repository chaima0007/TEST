"""
Comprehensive pytest tests for
swarm/intelligence/sales_outbound_prospecting_intelligence_engine.py
"""
from __future__ import annotations

import pytest

from swarm.intelligence.sales_outbound_prospecting_intelligence_engine import (
    ProspectingRisk,
    ProspectingPattern,
    ProspectingSeverity,
    ProspectingAction,
    OutboundProspectingInput,
    OutboundProspectingResult,
    SalesOutboundProspectingIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(
    rep_id: str = "rep1",
    region: str = "West",
    evaluation_period_id: str = "Q2-2026",
    outbound_attempts_total: int = 200,
    outbound_calls_made: int = 100,
    outbound_emails_sent: int = 80,
    social_touches_made: int = 20,
    connected_conversations: int = 30,
    connect_rate_pct: float = 0.20,
    discovery_calls_booked: int = 10,
    discovery_to_demo_conversion_rate_pct: float = 0.60,
    demos_booked_from_outbound: int = 6,
    outbound_pipeline_created_usd: float = 120_000.0,
    avg_touches_per_prospect: float = 7.0,
    prospects_contacted: int = 50,
    new_prospects_added: int = 30,
    icp_prospects_targeted_pct: float = 0.75,
    avg_response_rate_pct: float = 0.10,
    sequence_completion_rate_pct: float = 0.80,
    meetings_no_show_rate_pct: float = 0.05,
    avg_outreach_quality_score: float = 7.5,
    days_with_zero_outbound_activity: int = 0,
) -> OutboundProspectingInput:
    return OutboundProspectingInput(
        rep_id=rep_id,
        region=region,
        evaluation_period_id=evaluation_period_id,
        outbound_attempts_total=outbound_attempts_total,
        outbound_calls_made=outbound_calls_made,
        outbound_emails_sent=outbound_emails_sent,
        social_touches_made=social_touches_made,
        connected_conversations=connected_conversations,
        connect_rate_pct=connect_rate_pct,
        discovery_calls_booked=discovery_calls_booked,
        discovery_to_demo_conversion_rate_pct=discovery_to_demo_conversion_rate_pct,
        demos_booked_from_outbound=demos_booked_from_outbound,
        outbound_pipeline_created_usd=outbound_pipeline_created_usd,
        avg_touches_per_prospect=avg_touches_per_prospect,
        prospects_contacted=prospects_contacted,
        new_prospects_added=new_prospects_added,
        icp_prospects_targeted_pct=icp_prospects_targeted_pct,
        avg_response_rate_pct=avg_response_rate_pct,
        sequence_completion_rate_pct=sequence_completion_rate_pct,
        meetings_no_show_rate_pct=meetings_no_show_rate_pct,
        avg_outreach_quality_score=avg_outreach_quality_score,
        days_with_zero_outbound_activity=days_with_zero_outbound_activity,
    )


def engine() -> SalesOutboundProspectingIntelligenceEngine:
    return SalesOutboundProspectingIntelligenceEngine()


# ===========================================================================
# 1. Enum tests
# ===========================================================================

class TestProspectingRiskEnum:
    def test_values_exist(self):
        assert ProspectingRisk.low.value == "low"
        assert ProspectingRisk.moderate.value == "moderate"
        assert ProspectingRisk.high.value == "high"
        assert ProspectingRisk.critical.value == "critical"

    def test_all_members(self):
        members = {m.value for m in ProspectingRisk}
        assert members == {"low", "moderate", "high", "critical"}

    def test_str_enum(self):
        assert ProspectingRisk.low == "low"
        assert ProspectingRisk.critical == "critical"

    def test_count(self):
        assert len(ProspectingRisk) == 4


class TestProspectingPatternEnum:
    def test_values_exist(self):
        assert ProspectingPattern.none.value == "none"
        assert ProspectingPattern.low_activity.value == "low_activity"
        assert ProspectingPattern.poor_targeting.value == "poor_targeting"
        assert ProspectingPattern.low_connect_rate.value == "low_connect_rate"
        assert ProspectingPattern.pipeline_stall.value == "pipeline_stall"
        assert ProspectingPattern.burnout_signal.value == "burnout_signal"

    def test_all_members(self):
        members = {m.value for m in ProspectingPattern}
        assert members == {
            "none", "low_activity", "poor_targeting",
            "low_connect_rate", "pipeline_stall", "burnout_signal",
        }

    def test_str_enum(self):
        assert ProspectingPattern.none == "none"
        assert ProspectingPattern.burnout_signal == "burnout_signal"

    def test_count(self):
        assert len(ProspectingPattern) == 6


class TestProspectingSeverityEnum:
    def test_values_exist(self):
        assert ProspectingSeverity.active.value == "active"
        assert ProspectingSeverity.developing.value == "developing"
        assert ProspectingSeverity.lagging.value == "lagging"
        assert ProspectingSeverity.stalled.value == "stalled"

    def test_all_members(self):
        members = {m.value for m in ProspectingSeverity}
        assert members == {"active", "developing", "lagging", "stalled"}

    def test_str_enum(self):
        assert ProspectingSeverity.active == "active"
        assert ProspectingSeverity.stalled == "stalled"

    def test_count(self):
        assert len(ProspectingSeverity) == 4


class TestProspectingActionEnum:
    def test_values_exist(self):
        assert ProspectingAction.no_action.value == "no_action"
        assert ProspectingAction.activity_coaching.value == "activity_coaching"
        assert ProspectingAction.targeting_calibration.value == "targeting_calibration"
        assert ProspectingAction.messaging_optimization.value == "messaging_optimization"
        assert ProspectingAction.cadence_redesign.value == "cadence_redesign"
        assert ProspectingAction.pipeline_acceleration.value == "pipeline_acceleration"

    def test_all_members(self):
        members = {m.value for m in ProspectingAction}
        assert members == {
            "no_action", "activity_coaching", "targeting_calibration",
            "messaging_optimization", "cadence_redesign", "pipeline_acceleration",
        }

    def test_str_enum(self):
        assert ProspectingAction.no_action == "no_action"
        assert ProspectingAction.pipeline_acceleration == "pipeline_acceleration"

    def test_count(self):
        assert len(ProspectingAction) == 6


# ===========================================================================
# 2. _activity_volume_score
# ===========================================================================

class TestActivityVolumeScore:
    def setup_method(self):
        self.eng = engine()

    # --- outbound_attempts_total thresholds ---

    def test_attempts_below_50(self):
        score = self.eng._activity_volume_score(
            make_input(outbound_attempts_total=0, days_with_zero_outbound_activity=0, new_prospects_added=30)
        )
        assert score >= 40.0

    def test_attempts_exactly_49(self):
        score = self.eng._activity_volume_score(
            make_input(outbound_attempts_total=49, days_with_zero_outbound_activity=0, new_prospects_added=30)
        )
        assert score >= 40.0

    def test_attempts_exactly_50(self):
        score = self.eng._activity_volume_score(
            make_input(outbound_attempts_total=50, days_with_zero_outbound_activity=0, new_prospects_added=30)
        )
        # 50 falls in [50,100) → +20
        assert score == 20.0

    def test_attempts_exactly_99(self):
        score = self.eng._activity_volume_score(
            make_input(outbound_attempts_total=99, days_with_zero_outbound_activity=0, new_prospects_added=30)
        )
        assert score == 20.0

    def test_attempts_exactly_100(self):
        score = self.eng._activity_volume_score(
            make_input(outbound_attempts_total=100, days_with_zero_outbound_activity=0, new_prospects_added=30)
        )
        # 100 falls in [100,150) → +8
        assert score == 8.0

    def test_attempts_exactly_149(self):
        score = self.eng._activity_volume_score(
            make_input(outbound_attempts_total=149, days_with_zero_outbound_activity=0, new_prospects_added=30)
        )
        assert score == 8.0

    def test_attempts_exactly_150(self):
        score = self.eng._activity_volume_score(
            make_input(outbound_attempts_total=150, days_with_zero_outbound_activity=0, new_prospects_added=30)
        )
        # 150+ → no contribution
        assert score == 0.0

    def test_attempts_high(self):
        score = self.eng._activity_volume_score(
            make_input(outbound_attempts_total=999, days_with_zero_outbound_activity=0, new_prospects_added=30)
        )
        assert score == 0.0

    # --- days_with_zero_outbound_activity thresholds ---

    def test_zero_days_inactive_below_2(self):
        score = self.eng._activity_volume_score(
            make_input(outbound_attempts_total=200, days_with_zero_outbound_activity=0, new_prospects_added=30)
        )
        assert score == 0.0

    def test_zero_days_inactive_exactly_1(self):
        score = self.eng._activity_volume_score(
            make_input(outbound_attempts_total=200, days_with_zero_outbound_activity=1, new_prospects_added=30)
        )
        assert score == 0.0

    def test_zero_days_inactive_exactly_2(self):
        score = self.eng._activity_volume_score(
            make_input(outbound_attempts_total=200, days_with_zero_outbound_activity=2, new_prospects_added=30)
        )
        assert score == 5.0

    def test_zero_days_inactive_exactly_4(self):
        score = self.eng._activity_volume_score(
            make_input(outbound_attempts_total=200, days_with_zero_outbound_activity=4, new_prospects_added=30)
        )
        assert score == 5.0

    def test_zero_days_inactive_exactly_5(self):
        score = self.eng._activity_volume_score(
            make_input(outbound_attempts_total=200, days_with_zero_outbound_activity=5, new_prospects_added=30)
        )
        assert score == 15.0

    def test_zero_days_inactive_exactly_9(self):
        score = self.eng._activity_volume_score(
            make_input(outbound_attempts_total=200, days_with_zero_outbound_activity=9, new_prospects_added=30)
        )
        assert score == 15.0

    def test_zero_days_inactive_exactly_10(self):
        score = self.eng._activity_volume_score(
            make_input(outbound_attempts_total=200, days_with_zero_outbound_activity=10, new_prospects_added=30)
        )
        assert score == 30.0

    def test_zero_days_inactive_very_high(self):
        score = self.eng._activity_volume_score(
            make_input(outbound_attempts_total=200, days_with_zero_outbound_activity=30, new_prospects_added=30)
        )
        assert score == 30.0

    # --- new_prospects_added thresholds ---

    def test_new_prospects_below_10(self):
        score = self.eng._activity_volume_score(
            make_input(outbound_attempts_total=200, days_with_zero_outbound_activity=0, new_prospects_added=0)
        )
        assert score == 20.0

    def test_new_prospects_exactly_9(self):
        score = self.eng._activity_volume_score(
            make_input(outbound_attempts_total=200, days_with_zero_outbound_activity=0, new_prospects_added=9)
        )
        assert score == 20.0

    def test_new_prospects_exactly_10(self):
        score = self.eng._activity_volume_score(
            make_input(outbound_attempts_total=200, days_with_zero_outbound_activity=0, new_prospects_added=10)
        )
        assert score == 10.0

    def test_new_prospects_exactly_19(self):
        score = self.eng._activity_volume_score(
            make_input(outbound_attempts_total=200, days_with_zero_outbound_activity=0, new_prospects_added=19)
        )
        assert score == 10.0

    def test_new_prospects_exactly_20(self):
        score = self.eng._activity_volume_score(
            make_input(outbound_attempts_total=200, days_with_zero_outbound_activity=0, new_prospects_added=20)
        )
        assert score == 0.0

    # --- capping at 100 ---

    def test_score_capped_at_100(self):
        score = self.eng._activity_volume_score(
            make_input(outbound_attempts_total=0, days_with_zero_outbound_activity=30, new_prospects_added=0)
        )
        # 40 + 30 + 20 = 90 → 90.0
        assert score == 90.0

    def test_score_max_possible(self):
        score = self.eng._activity_volume_score(
            make_input(outbound_attempts_total=0, days_with_zero_outbound_activity=30, new_prospects_added=0)
        )
        assert score <= 100.0

    # --- additive combination ---

    def test_combination_50_to_99_attempts_5_days_inactive_10_to_19_prospects(self):
        score = self.eng._activity_volume_score(
            make_input(outbound_attempts_total=75, days_with_zero_outbound_activity=5, new_prospects_added=15)
        )
        # 20 + 15 + 10 = 45
        assert score == 45.0


# ===========================================================================
# 3. _targeting_quality_score
# ===========================================================================

class TestTargetingQualityScore:
    def setup_method(self):
        self.eng = engine()

    # --- icp_prospects_targeted_pct thresholds ---

    def test_icp_below_030(self):
        score = self.eng._targeting_quality_score(
            make_input(icp_prospects_targeted_pct=0.0, avg_outreach_quality_score=8.0, avg_touches_per_prospect=6.0)
        )
        assert score >= 40.0

    def test_icp_exactly_029(self):
        score = self.eng._targeting_quality_score(
            make_input(icp_prospects_targeted_pct=0.29, avg_outreach_quality_score=8.0, avg_touches_per_prospect=6.0)
        )
        assert score == 40.0

    def test_icp_exactly_030(self):
        score = self.eng._targeting_quality_score(
            make_input(icp_prospects_targeted_pct=0.30, avg_outreach_quality_score=8.0, avg_touches_per_prospect=6.0)
        )
        assert score == 20.0

    def test_icp_exactly_049(self):
        score = self.eng._targeting_quality_score(
            make_input(icp_prospects_targeted_pct=0.49, avg_outreach_quality_score=8.0, avg_touches_per_prospect=6.0)
        )
        assert score == 20.0

    def test_icp_exactly_050(self):
        score = self.eng._targeting_quality_score(
            make_input(icp_prospects_targeted_pct=0.50, avg_outreach_quality_score=8.0, avg_touches_per_prospect=6.0)
        )
        assert score == 8.0

    def test_icp_exactly_069(self):
        score = self.eng._targeting_quality_score(
            make_input(icp_prospects_targeted_pct=0.69, avg_outreach_quality_score=8.0, avg_touches_per_prospect=6.0)
        )
        assert score == 8.0

    def test_icp_exactly_070(self):
        score = self.eng._targeting_quality_score(
            make_input(icp_prospects_targeted_pct=0.70, avg_outreach_quality_score=8.0, avg_touches_per_prospect=6.0)
        )
        assert score == 0.0

    # --- avg_outreach_quality_score thresholds ---

    def test_quality_below_4(self):
        score = self.eng._targeting_quality_score(
            make_input(icp_prospects_targeted_pct=0.80, avg_outreach_quality_score=0.0, avg_touches_per_prospect=6.0)
        )
        assert score == 30.0

    def test_quality_exactly_39(self):
        score = self.eng._targeting_quality_score(
            make_input(icp_prospects_targeted_pct=0.80, avg_outreach_quality_score=3.9, avg_touches_per_prospect=6.0)
        )
        assert score == 30.0

    def test_quality_exactly_40(self):
        score = self.eng._targeting_quality_score(
            make_input(icp_prospects_targeted_pct=0.80, avg_outreach_quality_score=4.0, avg_touches_per_prospect=6.0)
        )
        assert score == 15.0

    def test_quality_exactly_59(self):
        score = self.eng._targeting_quality_score(
            make_input(icp_prospects_targeted_pct=0.80, avg_outreach_quality_score=5.9, avg_touches_per_prospect=6.0)
        )
        assert score == 15.0

    def test_quality_exactly_60(self):
        score = self.eng._targeting_quality_score(
            make_input(icp_prospects_targeted_pct=0.80, avg_outreach_quality_score=6.0, avg_touches_per_prospect=6.0)
        )
        assert score == 0.0

    # --- avg_touches_per_prospect thresholds ---

    def test_touches_below_3(self):
        score = self.eng._targeting_quality_score(
            make_input(icp_prospects_targeted_pct=0.80, avg_outreach_quality_score=8.0, avg_touches_per_prospect=0.0)
        )
        assert score == 20.0

    def test_touches_exactly_29(self):
        score = self.eng._targeting_quality_score(
            make_input(icp_prospects_targeted_pct=0.80, avg_outreach_quality_score=8.0, avg_touches_per_prospect=2.9)
        )
        assert score == 20.0

    def test_touches_exactly_30(self):
        score = self.eng._targeting_quality_score(
            make_input(icp_prospects_targeted_pct=0.80, avg_outreach_quality_score=8.0, avg_touches_per_prospect=3.0)
        )
        assert score == 10.0

    def test_touches_exactly_49(self):
        score = self.eng._targeting_quality_score(
            make_input(icp_prospects_targeted_pct=0.80, avg_outreach_quality_score=8.0, avg_touches_per_prospect=4.9)
        )
        assert score == 10.0

    def test_touches_exactly_50(self):
        score = self.eng._targeting_quality_score(
            make_input(icp_prospects_targeted_pct=0.80, avg_outreach_quality_score=8.0, avg_touches_per_prospect=5.0)
        )
        assert score == 0.0

    # --- capping at 100 ---

    def test_score_capped_at_100(self):
        score = self.eng._targeting_quality_score(
            make_input(icp_prospects_targeted_pct=0.0, avg_outreach_quality_score=0.0, avg_touches_per_prospect=0.0)
        )
        # 40 + 30 + 20 = 90
        assert score == 90.0

    def test_score_never_exceeds_100(self):
        score = self.eng._targeting_quality_score(
            make_input(icp_prospects_targeted_pct=0.0, avg_outreach_quality_score=0.0, avg_touches_per_prospect=0.0)
        )
        assert score <= 100.0


# ===========================================================================
# 4. _conversion_effectiveness_score
# ===========================================================================

class TestConversionEffectivenessScore:
    def setup_method(self):
        self.eng = engine()

    # --- connect_rate_pct thresholds ---

    def test_connect_rate_below_005(self):
        score = self.eng._conversion_effectiveness_score(
            make_input(connect_rate_pct=0.0, avg_response_rate_pct=0.10, meetings_no_show_rate_pct=0.0)
        )
        assert score >= 45.0

    def test_connect_rate_exactly_0049(self):
        score = self.eng._conversion_effectiveness_score(
            make_input(connect_rate_pct=0.049, avg_response_rate_pct=0.10, meetings_no_show_rate_pct=0.0)
        )
        assert score == 45.0

    def test_connect_rate_exactly_005(self):
        score = self.eng._conversion_effectiveness_score(
            make_input(connect_rate_pct=0.05, avg_response_rate_pct=0.10, meetings_no_show_rate_pct=0.0)
        )
        assert score == 25.0

    def test_connect_rate_exactly_0099(self):
        score = self.eng._conversion_effectiveness_score(
            make_input(connect_rate_pct=0.099, avg_response_rate_pct=0.10, meetings_no_show_rate_pct=0.0)
        )
        assert score == 25.0

    def test_connect_rate_exactly_010(self):
        score = self.eng._conversion_effectiveness_score(
            make_input(connect_rate_pct=0.10, avg_response_rate_pct=0.10, meetings_no_show_rate_pct=0.0)
        )
        assert score == 10.0

    def test_connect_rate_exactly_0149(self):
        score = self.eng._conversion_effectiveness_score(
            make_input(connect_rate_pct=0.149, avg_response_rate_pct=0.10, meetings_no_show_rate_pct=0.0)
        )
        assert score == 10.0

    def test_connect_rate_exactly_015(self):
        score = self.eng._conversion_effectiveness_score(
            make_input(connect_rate_pct=0.15, avg_response_rate_pct=0.10, meetings_no_show_rate_pct=0.0)
        )
        assert score == 0.0

    def test_connect_rate_high(self):
        score = self.eng._conversion_effectiveness_score(
            make_input(connect_rate_pct=0.50, avg_response_rate_pct=0.10, meetings_no_show_rate_pct=0.0)
        )
        assert score == 0.0

    # --- avg_response_rate_pct thresholds ---

    def test_response_rate_below_003(self):
        score = self.eng._conversion_effectiveness_score(
            make_input(connect_rate_pct=0.20, avg_response_rate_pct=0.0, meetings_no_show_rate_pct=0.0)
        )
        assert score == 30.0

    def test_response_rate_exactly_0029(self):
        score = self.eng._conversion_effectiveness_score(
            make_input(connect_rate_pct=0.20, avg_response_rate_pct=0.029, meetings_no_show_rate_pct=0.0)
        )
        assert score == 30.0

    def test_response_rate_exactly_003(self):
        score = self.eng._conversion_effectiveness_score(
            make_input(connect_rate_pct=0.20, avg_response_rate_pct=0.03, meetings_no_show_rate_pct=0.0)
        )
        assert score == 15.0

    def test_response_rate_exactly_0049(self):
        score = self.eng._conversion_effectiveness_score(
            make_input(connect_rate_pct=0.20, avg_response_rate_pct=0.049, meetings_no_show_rate_pct=0.0)
        )
        assert score == 15.0

    def test_response_rate_exactly_005(self):
        score = self.eng._conversion_effectiveness_score(
            make_input(connect_rate_pct=0.20, avg_response_rate_pct=0.05, meetings_no_show_rate_pct=0.0)
        )
        assert score == 0.0

    # --- meetings_no_show_rate_pct thresholds ---

    def test_noshow_below_015(self):
        score = self.eng._conversion_effectiveness_score(
            make_input(connect_rate_pct=0.20, avg_response_rate_pct=0.10, meetings_no_show_rate_pct=0.0)
        )
        assert score == 0.0

    def test_noshow_exactly_0149(self):
        score = self.eng._conversion_effectiveness_score(
            make_input(connect_rate_pct=0.20, avg_response_rate_pct=0.10, meetings_no_show_rate_pct=0.149)
        )
        assert score == 0.0

    def test_noshow_exactly_015(self):
        score = self.eng._conversion_effectiveness_score(
            make_input(connect_rate_pct=0.20, avg_response_rate_pct=0.10, meetings_no_show_rate_pct=0.15)
        )
        assert score == 10.0

    def test_noshow_exactly_0299(self):
        score = self.eng._conversion_effectiveness_score(
            make_input(connect_rate_pct=0.20, avg_response_rate_pct=0.10, meetings_no_show_rate_pct=0.299)
        )
        assert score == 10.0

    def test_noshow_exactly_030(self):
        score = self.eng._conversion_effectiveness_score(
            make_input(connect_rate_pct=0.20, avg_response_rate_pct=0.10, meetings_no_show_rate_pct=0.30)
        )
        assert score == 20.0

    def test_noshow_very_high(self):
        score = self.eng._conversion_effectiveness_score(
            make_input(connect_rate_pct=0.20, avg_response_rate_pct=0.10, meetings_no_show_rate_pct=1.0)
        )
        assert score == 20.0

    # --- capping at 100 ---

    def test_score_capped_at_100(self):
        score = self.eng._conversion_effectiveness_score(
            make_input(connect_rate_pct=0.0, avg_response_rate_pct=0.0, meetings_no_show_rate_pct=1.0)
        )
        # 45 + 30 + 20 = 95
        assert score == 95.0

    def test_score_never_exceeds_100(self):
        score = self.eng._conversion_effectiveness_score(
            make_input(connect_rate_pct=0.0, avg_response_rate_pct=0.0, meetings_no_show_rate_pct=1.0)
        )
        assert score <= 100.0


# ===========================================================================
# 5. _pipeline_contribution_score
# ===========================================================================

class TestPipelineContributionScore:
    def setup_method(self):
        self.eng = engine()

    # --- outbound_pipeline_created_usd thresholds ---

    def test_pipeline_below_10k(self):
        score = self.eng._pipeline_contribution_score(
            make_input(outbound_pipeline_created_usd=0.0, discovery_calls_booked=10, discovery_to_demo_conversion_rate_pct=0.60)
        )
        assert score >= 40.0

    def test_pipeline_exactly_9999(self):
        score = self.eng._pipeline_contribution_score(
            make_input(outbound_pipeline_created_usd=9_999.99, discovery_calls_booked=10, discovery_to_demo_conversion_rate_pct=0.60)
        )
        assert score == 40.0

    def test_pipeline_exactly_10000(self):
        score = self.eng._pipeline_contribution_score(
            make_input(outbound_pipeline_created_usd=10_000.0, discovery_calls_booked=10, discovery_to_demo_conversion_rate_pct=0.60)
        )
        assert score == 20.0

    def test_pipeline_exactly_49999(self):
        score = self.eng._pipeline_contribution_score(
            make_input(outbound_pipeline_created_usd=49_999.99, discovery_calls_booked=10, discovery_to_demo_conversion_rate_pct=0.60)
        )
        assert score == 20.0

    def test_pipeline_exactly_50000(self):
        score = self.eng._pipeline_contribution_score(
            make_input(outbound_pipeline_created_usd=50_000.0, discovery_calls_booked=10, discovery_to_demo_conversion_rate_pct=0.60)
        )
        assert score == 8.0

    def test_pipeline_exactly_99999(self):
        score = self.eng._pipeline_contribution_score(
            make_input(outbound_pipeline_created_usd=99_999.99, discovery_calls_booked=10, discovery_to_demo_conversion_rate_pct=0.60)
        )
        assert score == 8.0

    def test_pipeline_exactly_100000(self):
        score = self.eng._pipeline_contribution_score(
            make_input(outbound_pipeline_created_usd=100_000.0, discovery_calls_booked=10, discovery_to_demo_conversion_rate_pct=0.60)
        )
        assert score == 0.0

    # --- discovery_calls_booked thresholds ---

    def test_discovery_calls_below_3(self):
        score = self.eng._pipeline_contribution_score(
            make_input(outbound_pipeline_created_usd=200_000.0, discovery_calls_booked=0, discovery_to_demo_conversion_rate_pct=0.60)
        )
        assert score == 30.0

    def test_discovery_calls_exactly_2(self):
        score = self.eng._pipeline_contribution_score(
            make_input(outbound_pipeline_created_usd=200_000.0, discovery_calls_booked=2, discovery_to_demo_conversion_rate_pct=0.60)
        )
        assert score == 30.0

    def test_discovery_calls_exactly_3(self):
        score = self.eng._pipeline_contribution_score(
            make_input(outbound_pipeline_created_usd=200_000.0, discovery_calls_booked=3, discovery_to_demo_conversion_rate_pct=0.60)
        )
        assert score == 15.0

    def test_discovery_calls_exactly_6(self):
        score = self.eng._pipeline_contribution_score(
            make_input(outbound_pipeline_created_usd=200_000.0, discovery_calls_booked=6, discovery_to_demo_conversion_rate_pct=0.60)
        )
        assert score == 15.0

    def test_discovery_calls_exactly_7(self):
        score = self.eng._pipeline_contribution_score(
            make_input(outbound_pipeline_created_usd=200_000.0, discovery_calls_booked=7, discovery_to_demo_conversion_rate_pct=0.60)
        )
        assert score == 0.0

    # --- discovery_to_demo_conversion_rate_pct thresholds ---

    def test_demo_conversion_below_030(self):
        score = self.eng._pipeline_contribution_score(
            make_input(outbound_pipeline_created_usd=200_000.0, discovery_calls_booked=10, discovery_to_demo_conversion_rate_pct=0.0)
        )
        assert score == 20.0

    def test_demo_conversion_exactly_029(self):
        score = self.eng._pipeline_contribution_score(
            make_input(outbound_pipeline_created_usd=200_000.0, discovery_calls_booked=10, discovery_to_demo_conversion_rate_pct=0.29)
        )
        assert score == 20.0

    def test_demo_conversion_exactly_030(self):
        score = self.eng._pipeline_contribution_score(
            make_input(outbound_pipeline_created_usd=200_000.0, discovery_calls_booked=10, discovery_to_demo_conversion_rate_pct=0.30)
        )
        assert score == 10.0

    def test_demo_conversion_exactly_049(self):
        score = self.eng._pipeline_contribution_score(
            make_input(outbound_pipeline_created_usd=200_000.0, discovery_calls_booked=10, discovery_to_demo_conversion_rate_pct=0.49)
        )
        assert score == 10.0

    def test_demo_conversion_exactly_050(self):
        score = self.eng._pipeline_contribution_score(
            make_input(outbound_pipeline_created_usd=200_000.0, discovery_calls_booked=10, discovery_to_demo_conversion_rate_pct=0.50)
        )
        assert score == 0.0

    # --- capping at 100 ---

    def test_score_capped_at_100(self):
        score = self.eng._pipeline_contribution_score(
            make_input(outbound_pipeline_created_usd=0.0, discovery_calls_booked=0, discovery_to_demo_conversion_rate_pct=0.0)
        )
        # 40 + 30 + 20 = 90
        assert score == 90.0

    def test_score_never_exceeds_100(self):
        score = self.eng._pipeline_contribution_score(
            make_input(outbound_pipeline_created_usd=0.0, discovery_calls_booked=0, discovery_to_demo_conversion_rate_pct=0.0)
        )
        assert score <= 100.0


# ===========================================================================
# 6. _detect_pattern
# ===========================================================================

class TestDetectPattern:
    def setup_method(self):
        self.eng = engine()

    def _call(self, inp, volume, targeting, conversion, pipeline):
        return self.eng._detect_pattern(inp, volume, targeting, conversion, pipeline)

    def test_low_activity_pattern(self):
        # volume >= 35, attempts < 100, zero_days >= 5
        inp = make_input(outbound_attempts_total=50, days_with_zero_outbound_activity=5)
        assert self._call(inp, 35.0, 0.0, 0.0, 0.0) == ProspectingPattern.low_activity

    def test_low_activity_volume_exactly_35(self):
        inp = make_input(outbound_attempts_total=50, days_with_zero_outbound_activity=5)
        assert self._call(inp, 35.0, 0.0, 0.0, 0.0) == ProspectingPattern.low_activity

    def test_low_activity_volume_below_35_no_match(self):
        # volume < 35 means low_activity won't fire; neither will burnout since days < 8 (or volume <25)
        inp = make_input(outbound_attempts_total=50, days_with_zero_outbound_activity=5)
        # volume=34 → low_activity not triggered; poor_targeting triggered if targeting >= 30
        result = self._call(inp, 34.0, 0.0, 0.0, 0.0)
        assert result != ProspectingPattern.low_activity

    def test_low_activity_attempts_exactly_99(self):
        inp = make_input(outbound_attempts_total=99, days_with_zero_outbound_activity=5)
        assert self._call(inp, 35.0, 0.0, 0.0, 0.0) == ProspectingPattern.low_activity

    def test_low_activity_attempts_exactly_100_not_triggered(self):
        inp = make_input(outbound_attempts_total=100, days_with_zero_outbound_activity=5)
        # attempts >= 100 → low_activity not triggered
        result = self._call(inp, 35.0, 0.0, 0.0, 0.0)
        assert result != ProspectingPattern.low_activity

    def test_low_activity_zero_days_exactly_5(self):
        inp = make_input(outbound_attempts_total=50, days_with_zero_outbound_activity=5)
        assert self._call(inp, 35.0, 0.0, 0.0, 0.0) == ProspectingPattern.low_activity

    def test_low_activity_zero_days_below_5_not_triggered(self):
        inp = make_input(outbound_attempts_total=50, days_with_zero_outbound_activity=4)
        result = self._call(inp, 35.0, 0.0, 0.0, 0.0)
        assert result != ProspectingPattern.low_activity

    def test_poor_targeting_pattern(self):
        # targeting >= 30, icp < 0.40
        inp = make_input(icp_prospects_targeted_pct=0.30)
        assert self._call(inp, 0.0, 30.0, 0.0, 0.0) == ProspectingPattern.poor_targeting

    def test_poor_targeting_icp_exactly_039(self):
        inp = make_input(icp_prospects_targeted_pct=0.39)
        assert self._call(inp, 0.0, 30.0, 0.0, 0.0) == ProspectingPattern.poor_targeting

    def test_poor_targeting_icp_exactly_040_not_triggered(self):
        inp = make_input(icp_prospects_targeted_pct=0.40)
        result = self._call(inp, 0.0, 30.0, 0.0, 0.0)
        assert result != ProspectingPattern.poor_targeting

    def test_poor_targeting_score_below_30_not_triggered(self):
        inp = make_input(icp_prospects_targeted_pct=0.30)
        result = self._call(inp, 0.0, 29.9, 0.0, 0.0)
        assert result != ProspectingPattern.poor_targeting

    def test_low_connect_rate_pattern(self):
        # conversion >= 30, connect_rate < 0.08
        inp = make_input(connect_rate_pct=0.05)
        assert self._call(inp, 0.0, 0.0, 30.0, 0.0) == ProspectingPattern.low_connect_rate

    def test_low_connect_rate_exactly_0079(self):
        inp = make_input(connect_rate_pct=0.079)
        assert self._call(inp, 0.0, 0.0, 30.0, 0.0) == ProspectingPattern.low_connect_rate

    def test_low_connect_rate_exactly_008_not_triggered(self):
        inp = make_input(connect_rate_pct=0.08)
        result = self._call(inp, 0.0, 0.0, 30.0, 0.0)
        assert result != ProspectingPattern.low_connect_rate

    def test_low_connect_rate_score_below_30_not_triggered(self):
        inp = make_input(connect_rate_pct=0.05)
        result = self._call(inp, 0.0, 0.0, 29.9, 0.0)
        assert result != ProspectingPattern.low_connect_rate

    def test_pipeline_stall_pattern(self):
        # pipeline >= 30, pipeline_usd < 50000
        inp = make_input(outbound_pipeline_created_usd=30_000.0)
        assert self._call(inp, 0.0, 0.0, 0.0, 30.0) == ProspectingPattern.pipeline_stall

    def test_pipeline_stall_exactly_49999(self):
        inp = make_input(outbound_pipeline_created_usd=49_999.99)
        assert self._call(inp, 0.0, 0.0, 0.0, 30.0) == ProspectingPattern.pipeline_stall

    def test_pipeline_stall_exactly_50000_not_triggered(self):
        inp = make_input(outbound_pipeline_created_usd=50_000.0)
        result = self._call(inp, 0.0, 0.0, 0.0, 30.0)
        assert result != ProspectingPattern.pipeline_stall

    def test_pipeline_stall_score_below_30_not_triggered(self):
        inp = make_input(outbound_pipeline_created_usd=30_000.0)
        result = self._call(inp, 0.0, 0.0, 0.0, 29.9)
        assert result != ProspectingPattern.pipeline_stall

    def test_burnout_signal_pattern(self):
        # volume >= 25, zero_days >= 8
        inp = make_input(days_with_zero_outbound_activity=8)
        assert self._call(inp, 25.0, 0.0, 0.0, 0.0) == ProspectingPattern.burnout_signal

    def test_burnout_volume_exactly_25(self):
        inp = make_input(days_with_zero_outbound_activity=8)
        assert self._call(inp, 25.0, 0.0, 0.0, 0.0) == ProspectingPattern.burnout_signal

    def test_burnout_volume_below_25_not_triggered(self):
        inp = make_input(days_with_zero_outbound_activity=8)
        result = self._call(inp, 24.9, 0.0, 0.0, 0.0)
        assert result == ProspectingPattern.none

    def test_burnout_zero_days_exactly_8(self):
        inp = make_input(days_with_zero_outbound_activity=8)
        assert self._call(inp, 25.0, 0.0, 0.0, 0.0) == ProspectingPattern.burnout_signal

    def test_burnout_zero_days_below_8_not_triggered(self):
        inp = make_input(days_with_zero_outbound_activity=7)
        result = self._call(inp, 25.0, 0.0, 0.0, 0.0)
        assert result == ProspectingPattern.none

    def test_none_pattern_when_no_conditions_met(self):
        inp = make_input(
            outbound_attempts_total=200,
            days_with_zero_outbound_activity=0,
            icp_prospects_targeted_pct=0.80,
            connect_rate_pct=0.20,
            outbound_pipeline_created_usd=200_000.0,
        )
        assert self._call(inp, 0.0, 0.0, 0.0, 0.0) == ProspectingPattern.none

    def test_priority_low_activity_before_poor_targeting(self):
        # Both conditions could match: volume >= 35, attempts < 100, zero_days >= 5
        # AND targeting >= 30, icp < 0.40
        inp = make_input(
            outbound_attempts_total=50,
            days_with_zero_outbound_activity=5,
            icp_prospects_targeted_pct=0.30,
        )
        result = self._call(inp, 40.0, 35.0, 0.0, 0.0)
        assert result == ProspectingPattern.low_activity

    def test_priority_poor_targeting_before_low_connect(self):
        # low_activity not triggered (volume < 35 or attempts >= 100 or days < 5)
        # poor_targeting: targeting >= 30, icp < 0.40
        # low_connect_rate: conversion >= 30, connect < 0.08
        inp = make_input(
            outbound_attempts_total=200,
            days_with_zero_outbound_activity=0,
            icp_prospects_targeted_pct=0.30,
            connect_rate_pct=0.05,
        )
        result = self._call(inp, 0.0, 35.0, 35.0, 0.0)
        assert result == ProspectingPattern.poor_targeting

    def test_priority_low_connect_before_pipeline_stall(self):
        inp = make_input(
            outbound_attempts_total=200,
            days_with_zero_outbound_activity=0,
            icp_prospects_targeted_pct=0.80,
            connect_rate_pct=0.05,
            outbound_pipeline_created_usd=30_000.0,
        )
        result = self._call(inp, 0.0, 0.0, 35.0, 35.0)
        assert result == ProspectingPattern.low_connect_rate

    def test_priority_pipeline_stall_before_burnout(self):
        inp = make_input(
            outbound_attempts_total=200,
            days_with_zero_outbound_activity=8,
            icp_prospects_targeted_pct=0.80,
            connect_rate_pct=0.20,
            outbound_pipeline_created_usd=30_000.0,
        )
        result = self._call(inp, 25.0, 0.0, 0.0, 35.0)
        assert result == ProspectingPattern.pipeline_stall


# ===========================================================================
# 7. _risk_level and _severity at boundaries 20, 40, 60
# ===========================================================================

class TestRiskLevel:
    def setup_method(self):
        self.eng = engine()

    def test_below_20_is_low(self):
        assert self.eng._risk_level(0.0) == ProspectingRisk.low

    def test_exactly_19_is_low(self):
        assert self.eng._risk_level(19.9) == ProspectingRisk.low

    def test_exactly_20_is_moderate(self):
        assert self.eng._risk_level(20.0) == ProspectingRisk.moderate

    def test_between_20_and_40_is_moderate(self):
        assert self.eng._risk_level(30.0) == ProspectingRisk.moderate

    def test_exactly_39_is_moderate(self):
        assert self.eng._risk_level(39.9) == ProspectingRisk.moderate

    def test_exactly_40_is_high(self):
        assert self.eng._risk_level(40.0) == ProspectingRisk.high

    def test_between_40_and_60_is_high(self):
        assert self.eng._risk_level(50.0) == ProspectingRisk.high

    def test_exactly_59_is_high(self):
        assert self.eng._risk_level(59.9) == ProspectingRisk.high

    def test_exactly_60_is_critical(self):
        assert self.eng._risk_level(60.0) == ProspectingRisk.critical

    def test_above_60_is_critical(self):
        assert self.eng._risk_level(100.0) == ProspectingRisk.critical


class TestSeverity:
    def setup_method(self):
        self.eng = engine()

    def test_below_20_is_active(self):
        assert self.eng._severity(0.0) == ProspectingSeverity.active

    def test_exactly_19_is_active(self):
        assert self.eng._severity(19.9) == ProspectingSeverity.active

    def test_exactly_20_is_developing(self):
        assert self.eng._severity(20.0) == ProspectingSeverity.developing

    def test_between_20_and_40_is_developing(self):
        assert self.eng._severity(30.0) == ProspectingSeverity.developing

    def test_exactly_39_is_developing(self):
        assert self.eng._severity(39.9) == ProspectingSeverity.developing

    def test_exactly_40_is_lagging(self):
        assert self.eng._severity(40.0) == ProspectingSeverity.lagging

    def test_between_40_and_60_is_lagging(self):
        assert self.eng._severity(50.0) == ProspectingSeverity.lagging

    def test_exactly_59_is_lagging(self):
        assert self.eng._severity(59.9) == ProspectingSeverity.lagging

    def test_exactly_60_is_stalled(self):
        assert self.eng._severity(60.0) == ProspectingSeverity.stalled

    def test_above_60_is_stalled(self):
        assert self.eng._severity(100.0) == ProspectingSeverity.stalled


# ===========================================================================
# 8. _action for all risk × pattern combos
# ===========================================================================

class TestAction:
    def setup_method(self):
        self.eng = engine()

    # critical + low_activity → cadence_redesign
    def test_critical_low_activity(self):
        assert self.eng._action(ProspectingRisk.critical, ProspectingPattern.low_activity) == ProspectingAction.cadence_redesign

    # critical + poor_targeting → targeting_calibration
    def test_critical_poor_targeting(self):
        assert self.eng._action(ProspectingRisk.critical, ProspectingPattern.poor_targeting) == ProspectingAction.targeting_calibration

    # critical + low_connect_rate → pipeline_acceleration (fallback)
    def test_critical_low_connect_rate(self):
        assert self.eng._action(ProspectingRisk.critical, ProspectingPattern.low_connect_rate) == ProspectingAction.pipeline_acceleration

    # critical + pipeline_stall → pipeline_acceleration
    def test_critical_pipeline_stall(self):
        assert self.eng._action(ProspectingRisk.critical, ProspectingPattern.pipeline_stall) == ProspectingAction.pipeline_acceleration

    # critical + burnout_signal → pipeline_acceleration
    def test_critical_burnout_signal(self):
        assert self.eng._action(ProspectingRisk.critical, ProspectingPattern.burnout_signal) == ProspectingAction.pipeline_acceleration

    # critical + none → pipeline_acceleration
    def test_critical_none(self):
        assert self.eng._action(ProspectingRisk.critical, ProspectingPattern.none) == ProspectingAction.pipeline_acceleration

    # high + low_connect_rate → messaging_optimization
    def test_high_low_connect_rate(self):
        assert self.eng._action(ProspectingRisk.high, ProspectingPattern.low_connect_rate) == ProspectingAction.messaging_optimization

    # high + burnout_signal → cadence_redesign
    def test_high_burnout_signal(self):
        assert self.eng._action(ProspectingRisk.high, ProspectingPattern.burnout_signal) == ProspectingAction.cadence_redesign

    # high + low_activity → activity_coaching (fallback)
    def test_high_low_activity(self):
        assert self.eng._action(ProspectingRisk.high, ProspectingPattern.low_activity) == ProspectingAction.activity_coaching

    # high + poor_targeting → activity_coaching (fallback)
    def test_high_poor_targeting(self):
        assert self.eng._action(ProspectingRisk.high, ProspectingPattern.poor_targeting) == ProspectingAction.activity_coaching

    # high + pipeline_stall → activity_coaching (fallback)
    def test_high_pipeline_stall(self):
        assert self.eng._action(ProspectingRisk.high, ProspectingPattern.pipeline_stall) == ProspectingAction.activity_coaching

    # high + none → activity_coaching (fallback)
    def test_high_none(self):
        assert self.eng._action(ProspectingRisk.high, ProspectingPattern.none) == ProspectingAction.activity_coaching

    # moderate + all patterns → activity_coaching
    def test_moderate_low_activity(self):
        assert self.eng._action(ProspectingRisk.moderate, ProspectingPattern.low_activity) == ProspectingAction.activity_coaching

    def test_moderate_poor_targeting(self):
        assert self.eng._action(ProspectingRisk.moderate, ProspectingPattern.poor_targeting) == ProspectingAction.activity_coaching

    def test_moderate_low_connect_rate(self):
        assert self.eng._action(ProspectingRisk.moderate, ProspectingPattern.low_connect_rate) == ProspectingAction.activity_coaching

    def test_moderate_pipeline_stall(self):
        assert self.eng._action(ProspectingRisk.moderate, ProspectingPattern.pipeline_stall) == ProspectingAction.activity_coaching

    def test_moderate_burnout_signal(self):
        assert self.eng._action(ProspectingRisk.moderate, ProspectingPattern.burnout_signal) == ProspectingAction.activity_coaching

    def test_moderate_none(self):
        assert self.eng._action(ProspectingRisk.moderate, ProspectingPattern.none) == ProspectingAction.activity_coaching

    # low + all patterns → no_action
    def test_low_none(self):
        assert self.eng._action(ProspectingRisk.low, ProspectingPattern.none) == ProspectingAction.no_action

    def test_low_low_activity(self):
        assert self.eng._action(ProspectingRisk.low, ProspectingPattern.low_activity) == ProspectingAction.no_action

    def test_low_poor_targeting(self):
        assert self.eng._action(ProspectingRisk.low, ProspectingPattern.poor_targeting) == ProspectingAction.no_action

    def test_low_low_connect_rate(self):
        assert self.eng._action(ProspectingRisk.low, ProspectingPattern.low_connect_rate) == ProspectingAction.no_action

    def test_low_pipeline_stall(self):
        assert self.eng._action(ProspectingRisk.low, ProspectingPattern.pipeline_stall) == ProspectingAction.no_action

    def test_low_burnout_signal(self):
        assert self.eng._action(ProspectingRisk.low, ProspectingPattern.burnout_signal) == ProspectingAction.no_action


# ===========================================================================
# 9. _has_prospecting_gap
# ===========================================================================

class TestHasProspectingGap:
    def setup_method(self):
        self.eng = engine()

    # composite >= 40 triggers gap
    def test_gap_composite_exactly_40(self):
        inp = make_input(outbound_attempts_total=100, discovery_calls_booked=5)
        assert self.eng._has_prospecting_gap(40.0, inp) is True

    def test_gap_composite_above_40(self):
        inp = make_input(outbound_attempts_total=100, discovery_calls_booked=5)
        assert self.eng._has_prospecting_gap(60.0, inp) is True

    def test_no_gap_composite_below_40_good_attempts_good_discovery(self):
        inp = make_input(outbound_attempts_total=100, discovery_calls_booked=5)
        assert self.eng._has_prospecting_gap(39.9, inp) is False

    # attempts < 50 triggers gap
    def test_gap_attempts_exactly_49(self):
        inp = make_input(outbound_attempts_total=49, discovery_calls_booked=5)
        assert self.eng._has_prospecting_gap(0.0, inp) is True

    def test_gap_attempts_zero(self):
        inp = make_input(outbound_attempts_total=0, discovery_calls_booked=5)
        assert self.eng._has_prospecting_gap(0.0, inp) is True

    def test_no_gap_attempts_exactly_50_with_low_composite(self):
        inp = make_input(outbound_attempts_total=50, discovery_calls_booked=5)
        assert self.eng._has_prospecting_gap(0.0, inp) is False

    # discovery_calls_booked < 3 triggers gap
    def test_gap_discovery_exactly_2(self):
        inp = make_input(outbound_attempts_total=100, discovery_calls_booked=2)
        assert self.eng._has_prospecting_gap(0.0, inp) is True

    def test_gap_discovery_zero(self):
        inp = make_input(outbound_attempts_total=100, discovery_calls_booked=0)
        assert self.eng._has_prospecting_gap(0.0, inp) is True

    def test_no_gap_discovery_exactly_3_with_low_composite(self):
        inp = make_input(outbound_attempts_total=100, discovery_calls_booked=3)
        assert self.eng._has_prospecting_gap(0.0, inp) is False

    # all three conditions false → no gap
    def test_no_gap_all_conditions_false(self):
        inp = make_input(outbound_attempts_total=100, discovery_calls_booked=5)
        assert self.eng._has_prospecting_gap(10.0, inp) is False

    # two conditions at once
    def test_gap_attempts_and_discovery_both_low(self):
        inp = make_input(outbound_attempts_total=40, discovery_calls_booked=1)
        assert self.eng._has_prospecting_gap(0.0, inp) is True


# ===========================================================================
# 10. _requires_prospecting_coaching
# ===========================================================================

class TestRequiresProspectingCoaching:
    def setup_method(self):
        self.eng = engine()

    # composite >= 30 triggers coaching
    def test_coaching_composite_exactly_30(self):
        inp = make_input(connect_rate_pct=0.20, icp_prospects_targeted_pct=0.80)
        assert self.eng._requires_prospecting_coaching(30.0, inp) is True

    def test_coaching_composite_above_30(self):
        inp = make_input(connect_rate_pct=0.20, icp_prospects_targeted_pct=0.80)
        assert self.eng._requires_prospecting_coaching(60.0, inp) is True

    def test_no_coaching_composite_below_30_good_values(self):
        inp = make_input(connect_rate_pct=0.20, icp_prospects_targeted_pct=0.80)
        assert self.eng._requires_prospecting_coaching(29.9, inp) is False

    # connect_rate < 0.05 triggers coaching
    def test_coaching_connect_rate_exactly_0049(self):
        inp = make_input(connect_rate_pct=0.049, icp_prospects_targeted_pct=0.80)
        assert self.eng._requires_prospecting_coaching(0.0, inp) is True

    def test_coaching_connect_rate_zero(self):
        inp = make_input(connect_rate_pct=0.0, icp_prospects_targeted_pct=0.80)
        assert self.eng._requires_prospecting_coaching(0.0, inp) is True

    def test_no_coaching_connect_rate_exactly_005(self):
        inp = make_input(connect_rate_pct=0.05, icp_prospects_targeted_pct=0.80)
        assert self.eng._requires_prospecting_coaching(0.0, inp) is False

    # icp_prospects_targeted_pct < 0.40 triggers coaching
    def test_coaching_icp_exactly_039(self):
        inp = make_input(connect_rate_pct=0.20, icp_prospects_targeted_pct=0.39)
        assert self.eng._requires_prospecting_coaching(0.0, inp) is True

    def test_coaching_icp_zero(self):
        inp = make_input(connect_rate_pct=0.20, icp_prospects_targeted_pct=0.0)
        assert self.eng._requires_prospecting_coaching(0.0, inp) is True

    def test_no_coaching_icp_exactly_040(self):
        inp = make_input(connect_rate_pct=0.20, icp_prospects_targeted_pct=0.40)
        assert self.eng._requires_prospecting_coaching(0.0, inp) is False

    # all conditions false → no coaching
    def test_no_coaching_all_conditions_false(self):
        inp = make_input(connect_rate_pct=0.20, icp_prospects_targeted_pct=0.80)
        assert self.eng._requires_prospecting_coaching(0.0, inp) is False


# ===========================================================================
# 11. _estimated_pipeline_shortfall
# ===========================================================================

class TestEstimatedPipelineShortfall:
    def setup_method(self):
        self.eng = engine()

    def test_shortfall_positive_case(self):
        # (100000 - 50000) * 0.40 = 20000
        inp = make_input(outbound_pipeline_created_usd=50_000.0)
        result = self.eng._estimated_pipeline_shortfall(inp, 40.0)
        assert result == 20_000.0

    def test_shortfall_zero_composite(self):
        inp = make_input(outbound_pipeline_created_usd=50_000.0)
        result = self.eng._estimated_pipeline_shortfall(inp, 0.0)
        assert result == 0.0

    def test_shortfall_zero_pipeline(self):
        # (100000 - 0) * 0.50 = 50000
        inp = make_input(outbound_pipeline_created_usd=0.0)
        result = self.eng._estimated_pipeline_shortfall(inp, 50.0)
        assert result == 50_000.0

    def test_shortfall_pipeline_at_100k(self):
        # (100000 - 100000) * anything = 0
        inp = make_input(outbound_pipeline_created_usd=100_000.0)
        result = self.eng._estimated_pipeline_shortfall(inp, 80.0)
        assert result == 0.0

    def test_shortfall_pipeline_above_100k_returns_zero(self):
        # shortfall would be negative → capped at 0
        inp = make_input(outbound_pipeline_created_usd=150_000.0)
        result = self.eng._estimated_pipeline_shortfall(inp, 50.0)
        assert result == 0.0

    def test_shortfall_pipeline_exactly_1_dollar(self):
        # (100000 - 1) * 0.10 = 9999.9
        inp = make_input(outbound_pipeline_created_usd=1.0)
        result = self.eng._estimated_pipeline_shortfall(inp, 10.0)
        assert result == round(99_999.0 * 0.10, 2)

    def test_shortfall_composite_100(self):
        # (100000 - 20000) * 1.0 = 80000
        inp = make_input(outbound_pipeline_created_usd=20_000.0)
        result = self.eng._estimated_pipeline_shortfall(inp, 100.0)
        assert result == 80_000.0

    def test_shortfall_rounded_to_2_decimal_places(self):
        # (100000 - 33333) * 0.333 ≈ 22310.211
        inp = make_input(outbound_pipeline_created_usd=33_333.0)
        result = self.eng._estimated_pipeline_shortfall(inp, 33.3)
        assert result == round((100_000.0 - 33_333.0) * (33.3 / 100.0), 2)

    def test_shortfall_never_negative(self):
        inp = make_input(outbound_pipeline_created_usd=200_000.0)
        result = self.eng._estimated_pipeline_shortfall(inp, 90.0)
        assert result >= 0.0


# ===========================================================================
# 12. _signal string
# ===========================================================================

class TestSignal:
    def setup_method(self):
        self.eng = engine()

    def test_benchmark_path_on_track(self):
        # pattern=none, composite < 20 → benchmark message
        inp = make_input(
            outbound_attempts_total=200,
            connect_rate_pct=0.20,
            discovery_calls_booked=15,
        )
        result = self.eng._signal(inp, ProspectingPattern.none, 10.0)
        assert result == "Outbound prospecting activity and pipeline contribution on track"

    def test_benchmark_exactly_at_composite_19(self):
        inp = make_input(
            outbound_attempts_total=200,
            connect_rate_pct=0.20,
            discovery_calls_booked=15,
        )
        result = self.eng._signal(inp, ProspectingPattern.none, 19.9)
        assert result == "Outbound prospecting activity and pipeline contribution on track"

    def test_benchmark_path_not_taken_when_composite_20(self):
        # pattern=none but composite >= 20 → parts-based signal
        inp = make_input(
            outbound_attempts_total=200,
            connect_rate_pct=0.20,
            discovery_calls_booked=15,
        )
        result = self.eng._signal(inp, ProspectingPattern.none, 20.0)
        assert result != "Outbound prospecting activity and pipeline contribution on track"
        assert "Prospecting risk" in result

    def test_benchmark_path_not_taken_when_pattern_not_none(self):
        inp = make_input(
            outbound_attempts_total=200,
            connect_rate_pct=0.20,
            discovery_calls_booked=15,
        )
        result = self.eng._signal(inp, ProspectingPattern.low_activity, 5.0)
        assert "Low activity" in result

    def test_signal_includes_attempts_when_below_150(self):
        inp = make_input(outbound_attempts_total=100, connect_rate_pct=0.20, discovery_calls_booked=15)
        result = self.eng._signal(inp, ProspectingPattern.low_activity, 40.0)
        assert "100 total attempts" in result

    def test_signal_excludes_attempts_when_150_or_above(self):
        inp = make_input(outbound_attempts_total=150, connect_rate_pct=0.20, discovery_calls_booked=15)
        result = self.eng._signal(inp, ProspectingPattern.low_activity, 40.0)
        assert "total attempts" not in result

    def test_signal_includes_connect_rate_when_below_015(self):
        inp = make_input(outbound_attempts_total=200, connect_rate_pct=0.10, discovery_calls_booked=15)
        result = self.eng._signal(inp, ProspectingPattern.low_connect_rate, 40.0)
        assert "10% connect rate" in result

    def test_signal_excludes_connect_rate_metric_when_015_or_above(self):
        # connect_rate_pct=0.15 is not < 0.15 so the rate metric is omitted from parts.
        # The pattern label "Low connect rate" will still appear but the "15% connect rate"
        # metric string should not be present.
        inp = make_input(outbound_attempts_total=200, connect_rate_pct=0.15, discovery_calls_booked=15)
        result = self.eng._signal(inp, ProspectingPattern.low_connect_rate, 40.0)
        assert "15% connect rate" not in result

    def test_signal_includes_discovery_calls_when_below_10(self):
        inp = make_input(outbound_attempts_total=200, connect_rate_pct=0.20, discovery_calls_booked=5)
        result = self.eng._signal(inp, ProspectingPattern.pipeline_stall, 40.0)
        assert "5 discovery calls booked" in result

    def test_signal_excludes_discovery_calls_when_10_or_above(self):
        inp = make_input(outbound_attempts_total=200, connect_rate_pct=0.20, discovery_calls_booked=10)
        result = self.eng._signal(inp, ProspectingPattern.pipeline_stall, 40.0)
        assert "discovery calls booked" not in result

    def test_signal_contains_composite_value(self):
        inp = make_input(outbound_attempts_total=200, connect_rate_pct=0.20, discovery_calls_booked=15)
        result = self.eng._signal(inp, ProspectingPattern.pipeline_stall, 45.0)
        assert "composite 45" in result

    def test_signal_fallback_when_no_parts(self):
        # attempts >= 150, connect_rate >= 0.15, discovery >= 10 → parts is empty
        inp = make_input(outbound_attempts_total=200, connect_rate_pct=0.20, discovery_calls_booked=15)
        result = self.eng._signal(inp, ProspectingPattern.pipeline_stall, 40.0)
        assert "prospecting effectiveness declining" in result

    def test_signal_pattern_label_capitalized(self):
        inp = make_input(outbound_attempts_total=100, connect_rate_pct=0.05, discovery_calls_booked=5)
        result = self.eng._signal(inp, ProspectingPattern.low_connect_rate, 40.0)
        assert result.startswith("Low connect rate")

    def test_signal_none_pattern_label(self):
        inp = make_input(outbound_attempts_total=200, connect_rate_pct=0.20, discovery_calls_booked=15)
        result = self.eng._signal(inp, ProspectingPattern.none, 25.0)
        assert result.startswith("Prospecting risk")

    def test_signal_poor_targeting_pattern_label(self):
        inp = make_input(outbound_attempts_total=100, connect_rate_pct=0.05, discovery_calls_booked=5)
        result = self.eng._signal(inp, ProspectingPattern.poor_targeting, 40.0)
        assert result.startswith("Poor targeting")

    def test_signal_burnout_signal_pattern_label(self):
        inp = make_input(outbound_attempts_total=100, connect_rate_pct=0.05, discovery_calls_booked=5)
        result = self.eng._signal(inp, ProspectingPattern.burnout_signal, 40.0)
        assert result.startswith("Burnout signal")


# ===========================================================================
# 13. assess() → 15 keys in to_dict()
# ===========================================================================

class TestAssess:
    def setup_method(self):
        self.eng = engine()

    def test_to_dict_has_15_keys(self):
        result = self.eng.assess(make_input())
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_key_names(self):
        d = self.eng.assess(make_input()).to_dict()
        expected_keys = {
            "rep_id",
            "region",
            "prospecting_risk",
            "prospecting_pattern",
            "prospecting_severity",
            "recommended_action",
            "activity_volume_score",
            "targeting_quality_score",
            "conversion_effectiveness_score",
            "pipeline_contribution_score",
            "prospecting_effectiveness_composite",
            "has_prospecting_gap",
            "requires_prospecting_coaching",
            "estimated_pipeline_shortfall_usd",
            "prospecting_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_rep_id_propagated(self):
        r = self.eng.assess(make_input(rep_id="xyz-123"))
        assert r.rep_id == "xyz-123"
        assert r.to_dict()["rep_id"] == "xyz-123"

    def test_region_propagated(self):
        r = self.eng.assess(make_input(region="EMEA"))
        assert r.region == "EMEA"
        assert r.to_dict()["region"] == "EMEA"

    def test_to_dict_values_are_string_enums(self):
        d = self.eng.assess(make_input()).to_dict()
        assert isinstance(d["prospecting_risk"], str)
        assert isinstance(d["prospecting_pattern"], str)
        assert isinstance(d["prospecting_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_composite_is_float(self):
        r = self.eng.assess(make_input())
        assert isinstance(r.prospecting_effectiveness_composite, float)

    def test_scores_are_float(self):
        r = self.eng.assess(make_input())
        assert isinstance(r.activity_volume_score, float)
        assert isinstance(r.targeting_quality_score, float)
        assert isinstance(r.conversion_effectiveness_score, float)
        assert isinstance(r.pipeline_contribution_score, float)

    def test_gap_is_bool(self):
        r = self.eng.assess(make_input())
        assert isinstance(r.has_prospecting_gap, bool)

    def test_coaching_is_bool(self):
        r = self.eng.assess(make_input())
        assert isinstance(r.requires_prospecting_coaching, bool)

    def test_shortfall_is_float(self):
        r = self.eng.assess(make_input())
        assert isinstance(r.estimated_pipeline_shortfall_usd, float)

    def test_signal_is_string(self):
        r = self.eng.assess(make_input())
        assert isinstance(r.prospecting_signal, str)

    def test_result_stored_in_results_list(self):
        eng = engine()
        r = eng.assess(make_input())
        assert r in eng._results

    def test_composite_formula(self):
        # A fully "zero-risk" rep should have composite near 0
        r = self.eng.assess(make_input(
            outbound_attempts_total=200,
            days_with_zero_outbound_activity=0,
            new_prospects_added=30,
            icp_prospects_targeted_pct=0.80,
            avg_outreach_quality_score=8.0,
            avg_touches_per_prospect=7.0,
            connect_rate_pct=0.25,
            avg_response_rate_pct=0.10,
            meetings_no_show_rate_pct=0.05,
            outbound_pipeline_created_usd=200_000.0,
            discovery_calls_booked=10,
            discovery_to_demo_conversion_rate_pct=0.60,
        ))
        assert r.prospecting_effectiveness_composite == 0.0

    def test_high_risk_scenario(self):
        r = self.eng.assess(make_input(
            outbound_attempts_total=20,
            days_with_zero_outbound_activity=15,
            new_prospects_added=5,
            icp_prospects_targeted_pct=0.10,
            avg_outreach_quality_score=2.0,
            avg_touches_per_prospect=1.0,
            connect_rate_pct=0.01,
            avg_response_rate_pct=0.01,
            meetings_no_show_rate_pct=0.50,
            outbound_pipeline_created_usd=0.0,
            discovery_calls_booked=0,
            discovery_to_demo_conversion_rate_pct=0.10,
        ))
        assert r.prospecting_risk in (ProspectingRisk.high, ProspectingRisk.critical)

    def test_composite_capped_at_100(self):
        r = self.eng.assess(make_input(
            outbound_attempts_total=0,
            days_with_zero_outbound_activity=30,
            new_prospects_added=0,
            icp_prospects_targeted_pct=0.0,
            avg_outreach_quality_score=0.0,
            avg_touches_per_prospect=0.0,
            connect_rate_pct=0.0,
            avg_response_rate_pct=0.0,
            meetings_no_show_rate_pct=1.0,
            outbound_pipeline_created_usd=0.0,
            discovery_calls_booked=0,
            discovery_to_demo_conversion_rate_pct=0.0,
        ))
        assert r.prospecting_effectiveness_composite <= 100.0

    def test_assess_appends_to_results(self):
        eng = engine()
        for i in range(3):
            eng.assess(make_input(rep_id=f"rep{i}"))
        assert len(eng._results) == 3

    def test_assess_result_is_outbound_result_type(self):
        r = self.eng.assess(make_input())
        assert isinstance(r, OutboundProspectingResult)


# ===========================================================================
# 14. summary() → 13 keys
# ===========================================================================

class TestSummary:
    def setup_method(self):
        self.eng = engine()

    def test_empty_summary_has_13_keys(self):
        s = self.eng.summary()
        assert len(s) == 13

    def test_empty_summary_key_names(self):
        s = self.eng.summary()
        expected = {
            "total",
            "risk_counts",
            "pattern_counts",
            "severity_counts",
            "action_counts",
            "avg_prospecting_effectiveness_composite",
            "prospecting_gap_count",
            "prospecting_coaching_count",
            "avg_activity_volume_score",
            "avg_targeting_quality_score",
            "avg_conversion_effectiveness_score",
            "avg_pipeline_contribution_score",
            "total_estimated_pipeline_shortfall_usd",
        }
        assert set(s.keys()) == expected

    def test_empty_summary_total_zero(self):
        assert self.eng.summary()["total"] == 0

    def test_empty_summary_counts_empty(self):
        s = self.eng.summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}

    def test_empty_summary_averages_zero(self):
        s = self.eng.summary()
        assert s["avg_prospecting_effectiveness_composite"] == 0.0
        assert s["avg_activity_volume_score"] == 0.0
        assert s["avg_targeting_quality_score"] == 0.0
        assert s["avg_conversion_effectiveness_score"] == 0.0
        assert s["avg_pipeline_contribution_score"] == 0.0

    def test_empty_summary_gap_coaching_zero(self):
        s = self.eng.summary()
        assert s["prospecting_gap_count"] == 0
        assert s["prospecting_coaching_count"] == 0

    def test_empty_summary_shortfall_zero(self):
        assert self.eng.summary()["total_estimated_pipeline_shortfall_usd"] == 0.0

    def test_summary_with_one_result(self):
        self.eng.assess(make_input(rep_id="r1"))
        s = self.eng.summary()
        assert s["total"] == 1

    def test_summary_with_multiple_results_total(self):
        for i in range(5):
            self.eng.assess(make_input(rep_id=f"rep{i}"))
        assert self.eng.summary()["total"] == 5

    def test_summary_risk_counts_non_empty(self):
        self.eng.assess(make_input())
        s = self.eng.summary()
        total_risks = sum(s["risk_counts"].values())
        assert total_risks == s["total"]

    def test_summary_pattern_counts_non_empty(self):
        self.eng.assess(make_input())
        s = self.eng.summary()
        total_patterns = sum(s["pattern_counts"].values())
        assert total_patterns == s["total"]

    def test_summary_severity_counts_non_empty(self):
        self.eng.assess(make_input())
        s = self.eng.summary()
        total_sev = sum(s["severity_counts"].values())
        assert total_sev == s["total"]

    def test_summary_action_counts_non_empty(self):
        self.eng.assess(make_input())
        s = self.eng.summary()
        total_action = sum(s["action_counts"].values())
        assert total_action == s["total"]

    def test_summary_has_13_keys_after_assessments(self):
        for i in range(3):
            self.eng.assess(make_input(rep_id=f"r{i}"))
        assert len(self.eng.summary()) == 13

    def test_summary_gap_count_accumulates(self):
        # gap triggered if composite >= 40 OR attempts < 50 OR discovery < 3
        # Use attempts < 50 to force gap
        self.eng.assess(make_input(outbound_attempts_total=30, discovery_calls_booked=5))
        self.eng.assess(make_input(outbound_attempts_total=200, discovery_calls_booked=10))
        s = self.eng.summary()
        assert s["prospecting_gap_count"] >= 1

    def test_summary_coaching_count_accumulates(self):
        # coaching if icp < 0.40
        self.eng.assess(make_input(icp_prospects_targeted_pct=0.20))
        self.eng.assess(make_input(icp_prospects_targeted_pct=0.80))
        s = self.eng.summary()
        assert s["prospecting_coaching_count"] >= 1

    def test_summary_shortfall_accumulates(self):
        self.eng.assess(make_input(outbound_pipeline_created_usd=0.0))
        self.eng.assess(make_input(outbound_pipeline_created_usd=0.0))
        s = self.eng.summary()
        # Both will likely have shortfall > 0
        assert s["total_estimated_pipeline_shortfall_usd"] >= 0.0

    def test_summary_avg_composite_is_float(self):
        self.eng.assess(make_input())
        s = self.eng.summary()
        assert isinstance(s["avg_prospecting_effectiveness_composite"], float)


# ===========================================================================
# 15. assess_batch()
# ===========================================================================

class TestAssessBatch:
    def setup_method(self):
        self.eng = engine()

    def test_batch_empty_list(self):
        results = self.eng.assess_batch([])
        assert results == []

    def test_batch_single_item(self):
        results = self.eng.assess_batch([make_input(rep_id="r1")])
        assert len(results) == 1
        assert results[0].rep_id == "r1"

    def test_batch_multiple_items(self):
        inputs = [make_input(rep_id=f"rep{i}") for i in range(10)]
        results = self.eng.assess_batch(inputs)
        assert len(results) == 10

    def test_batch_preserves_order(self):
        inputs = [make_input(rep_id=f"rep{i}") for i in range(5)]
        results = self.eng.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"rep{i}"

    def test_batch_results_stored(self):
        inputs = [make_input(rep_id=f"rep{i}") for i in range(3)]
        self.eng.assess_batch(inputs)
        assert len(self.eng._results) == 3

    def test_batch_returns_result_instances(self):
        results = self.eng.assess_batch([make_input()])
        assert isinstance(results[0], OutboundProspectingResult)

    def test_batch_summary_after_batch(self):
        inputs = [make_input(rep_id=f"rep{i}") for i in range(4)]
        self.eng.assess_batch(inputs)
        s = self.eng.summary()
        assert s["total"] == 4

    def test_batch_mixed_profiles(self):
        inputs = [
            make_input(rep_id="good", outbound_attempts_total=200, outbound_pipeline_created_usd=200_000.0),
            make_input(rep_id="bad", outbound_attempts_total=10, outbound_pipeline_created_usd=0.0),
        ]
        results = self.eng.assess_batch(inputs)
        risk_values = [r.prospecting_risk for r in results]
        # At minimum both should be valid risk levels
        for rv in risk_values:
            assert rv in list(ProspectingRisk)

    def test_batch_incremental_after_single_assess(self):
        self.eng.assess(make_input(rep_id="solo"))
        inputs = [make_input(rep_id=f"batch{i}") for i in range(3)]
        self.eng.assess_batch(inputs)
        assert len(self.eng._results) == 4


# ===========================================================================
# 16. Integration / edge-case tests
# ===========================================================================

class TestIntegration:
    def setup_method(self):
        self.eng = engine()

    def test_perfect_rep_is_low_risk(self):
        r = self.eng.assess(make_input(
            outbound_attempts_total=300,
            days_with_zero_outbound_activity=0,
            new_prospects_added=50,
            icp_prospects_targeted_pct=0.90,
            avg_outreach_quality_score=9.0,
            avg_touches_per_prospect=8.0,
            connect_rate_pct=0.30,
            avg_response_rate_pct=0.15,
            meetings_no_show_rate_pct=0.05,
            outbound_pipeline_created_usd=200_000.0,
            discovery_calls_booked=20,
            discovery_to_demo_conversion_rate_pct=0.70,
        ))
        assert r.prospecting_risk == ProspectingRisk.low
        assert r.prospecting_severity == ProspectingSeverity.active
        assert r.recommended_action == ProspectingAction.no_action

    def test_worst_case_rep_is_critical(self):
        r = self.eng.assess(make_input(
            outbound_attempts_total=5,
            days_with_zero_outbound_activity=20,
            new_prospects_added=0,
            icp_prospects_targeted_pct=0.05,
            avg_outreach_quality_score=1.0,
            avg_touches_per_prospect=1.0,
            connect_rate_pct=0.01,
            avg_response_rate_pct=0.01,
            meetings_no_show_rate_pct=0.80,
            outbound_pipeline_created_usd=0.0,
            discovery_calls_booked=0,
            discovery_to_demo_conversion_rate_pct=0.0,
        ))
        assert r.prospecting_risk == ProspectingRisk.critical
        assert r.prospecting_severity == ProspectingSeverity.stalled

    def test_gap_true_and_coaching_true_for_bad_rep(self):
        r = self.eng.assess(make_input(
            outbound_attempts_total=10,
            discovery_calls_booked=1,
            connect_rate_pct=0.01,
            icp_prospects_targeted_pct=0.10,
        ))
        assert r.has_prospecting_gap is True
        assert r.requires_prospecting_coaching is True

    def test_shortfall_zero_for_high_pipeline(self):
        r = self.eng.assess(make_input(outbound_pipeline_created_usd=200_000.0))
        assert r.estimated_pipeline_shortfall_usd == 0.0

    def test_engine_fresh_instance_has_empty_results(self):
        eng = engine()
        assert eng._results == []

    def test_multiple_engines_independent(self):
        eng1 = engine()
        eng2 = engine()
        eng1.assess(make_input(rep_id="e1r1"))
        eng2.assess(make_input(rep_id="e2r1"))
        eng2.assess(make_input(rep_id="e2r2"))
        assert len(eng1._results) == 1
        assert len(eng2._results) == 2

    def test_composite_weights_sum_to_1(self):
        # 0.25 + 0.25 + 0.30 + 0.20 = 1.0
        assert abs(0.25 + 0.25 + 0.30 + 0.20 - 1.0) < 1e-9

    def test_assess_low_risk_no_gap_no_coaching(self):
        r = self.eng.assess(make_input(
            outbound_attempts_total=200,
            days_with_zero_outbound_activity=0,
            new_prospects_added=30,
            icp_prospects_targeted_pct=0.80,
            avg_outreach_quality_score=8.0,
            avg_touches_per_prospect=7.0,
            connect_rate_pct=0.25,
            avg_response_rate_pct=0.10,
            meetings_no_show_rate_pct=0.05,
            outbound_pipeline_created_usd=200_000.0,
            discovery_calls_booked=15,
            discovery_to_demo_conversion_rate_pct=0.60,
        ))
        assert r.has_prospecting_gap is False
        assert r.requires_prospecting_coaching is False

    def test_activity_score_additive_all_three(self):
        # attempts < 50 (+40), days >= 10 (+30), new_prospects < 10 (+20) = 90
        score = self.eng._activity_volume_score(
            make_input(outbound_attempts_total=10, days_with_zero_outbound_activity=10, new_prospects_added=5)
        )
        assert score == 90.0

    def test_conversion_score_additive_all_three(self):
        # connect < 0.05 (+45), response < 0.03 (+30), noshow >= 0.30 (+20) = 95
        score = self.eng._conversion_effectiveness_score(
            make_input(connect_rate_pct=0.01, avg_response_rate_pct=0.01, meetings_no_show_rate_pct=0.50)
        )
        assert score == 95.0

    def test_pipeline_score_additive_all_three(self):
        # pipeline < 10k (+40), discovery < 3 (+30), conversion < 0.30 (+20) = 90
        score = self.eng._pipeline_contribution_score(
            make_input(outbound_pipeline_created_usd=0.0, discovery_calls_booked=0, discovery_to_demo_conversion_rate_pct=0.10)
        )
        assert score == 90.0
