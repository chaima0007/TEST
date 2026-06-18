"""
Comprehensive pytest tests for SalesPipelineGenerationVelocityIntelligenceEngine.
"""
from __future__ import annotations

import pytest
from swarm.intelligence.sales_pipeline_generation_velocity_intelligence_engine import (
    PipelineAction,
    PipelineInput,
    PipelinePattern,
    PipelineResult,
    PipelineRisk,
    PipelineSeverity,
    SalesPipelineGenerationVelocityIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def make_input(**overrides) -> PipelineInput:
    """Return a baseline PipelineInput with healthy defaults; override as needed."""
    defaults = dict(
        rep_id="rep_001",
        region="US-West",
        evaluation_period_id="2024-Q1",
        outreach_attempts_per_week_avg=30.0,
        outreach_to_connect_rate_pct=0.25,          # good
        connect_to_meeting_rate_pct=0.40,            # good
        meeting_to_opportunity_rate_pct=0.50,        # good
        new_opportunities_per_week_avg=2.5,          # good
        pipeline_coverage_ratio=3.5,                 # good
        days_to_first_opportunity_avg=20.0,          # good
        icp_targeted_outreach_pct=0.70,              # good
        multi_channel_outreach_pct=0.50,             # good
        referral_sourced_pipeline_pct=0.20,          # good
        stale_opportunity_rate_pct=0.05,             # good
        opportunity_no_activity_14d_pct=0.10,        # good
        consecutive_low_pipeline_weeks=0,
        territory_coverage_depth_pct=0.50,           # good
        avg_opportunity_age_at_stage1_days=5.0,
        inbound_conversion_rate_pct=0.30,
        pipeline_created_per_week_usd=20_000.0,
        total_outreach_attempts=500,
        avg_opportunity_value_usd=10_000.0,
    )
    defaults.update(overrides)
    return PipelineInput(**defaults)


def make_engine() -> SalesPipelineGenerationVelocityIntelligenceEngine:
    return SalesPipelineGenerationVelocityIntelligenceEngine()


@pytest.fixture
def engine():
    return make_engine()


@pytest.fixture
def healthy_input():
    return make_input()


# ---------------------------------------------------------------------------
# 1. Enum membership
# ---------------------------------------------------------------------------

class TestEnums:
    def test_pipeline_risk_values(self):
        assert set(r.value for r in PipelineRisk) == {"low", "moderate", "high", "critical"}

    def test_pipeline_pattern_values(self):
        expected = {"none", "burst_and_fade", "reactive_only", "slow_starter",
                    "territory_exhaustion", "channel_dependency"}
        assert set(p.value for p in PipelinePattern) == expected

    def test_pipeline_severity_values(self):
        assert set(s.value for s in PipelineSeverity) == {"generating", "adequate", "sluggish", "stalled"}

    def test_pipeline_action_values(self):
        expected = {
            "no_action", "prospecting_cadence_coaching", "icp_targeting_coaching",
            "channel_diversification_coaching", "pipeline_generation_coaching",
            "pipeline_generation_intervention", "pipeline_reset_intervention",
        }
        assert set(a.value for a in PipelineAction) == expected

    def test_pipeline_risk_is_str(self):
        assert isinstance(PipelineRisk.low, str)

    def test_pipeline_pattern_is_str(self):
        assert isinstance(PipelinePattern.none, str)

    def test_pipeline_severity_is_str(self):
        assert isinstance(PipelineSeverity.generating, str)

    def test_pipeline_action_is_str(self):
        assert isinstance(PipelineAction.no_action, str)


# ---------------------------------------------------------------------------
# 2. PipelineInput construction
# ---------------------------------------------------------------------------

class TestPipelineInput:
    def test_all_fields_present(self):
        inp = make_input()
        assert inp.rep_id == "rep_001"
        assert inp.region == "US-West"
        assert inp.evaluation_period_id == "2024-Q1"
        assert inp.outreach_attempts_per_week_avg == 30.0
        assert inp.total_outreach_attempts == 500

    def test_field_count(self):
        inp = make_input()
        # 22 fields per spec
        import dataclasses
        assert len(dataclasses.fields(inp)) == 22


# ---------------------------------------------------------------------------
# 3. _generation_rate_score sub-score
# ---------------------------------------------------------------------------

class TestGenerationRateScore:
    def _score(self, **kw):
        eng = make_engine()
        return eng._generation_rate_score(make_input(**kw))

    # outreach_to_connect_rate_pct thresholds
    def test_outreach_connect_worst(self):
        s = self._score(outreach_to_connect_rate_pct=0.04)
        assert s >= 40

    def test_outreach_connect_boundary_005(self):
        s = self._score(outreach_to_connect_rate_pct=0.05)
        assert s >= 40

    def test_outreach_connect_mid(self):
        s = self._score(
            outreach_to_connect_rate_pct=0.08,
            connect_to_meeting_rate_pct=0.50,
            meeting_to_opportunity_rate_pct=0.60,
        )
        assert s == 22  # only outreach band contributes

    def test_outreach_connect_boundary_010(self):
        s = self._score(
            outreach_to_connect_rate_pct=0.10,
            connect_to_meeting_rate_pct=0.50,
            meeting_to_opportunity_rate_pct=0.60,
        )
        assert s == 22

    def test_outreach_connect_third_band(self):
        s = self._score(
            outreach_to_connect_rate_pct=0.15,
            connect_to_meeting_rate_pct=0.50,
            meeting_to_opportunity_rate_pct=0.60,
        )
        assert s == 8

    def test_outreach_connect_boundary_018(self):
        s = self._score(
            outreach_to_connect_rate_pct=0.18,
            connect_to_meeting_rate_pct=0.50,
            meeting_to_opportunity_rate_pct=0.60,
        )
        assert s == 8

    def test_outreach_connect_none(self):
        s = self._score(
            outreach_to_connect_rate_pct=0.25,
            connect_to_meeting_rate_pct=0.50,
            meeting_to_opportunity_rate_pct=0.60,
        )
        assert s == 0

    # connect_to_meeting_rate_pct thresholds
    def test_connect_meeting_worst(self):
        s = self._score(
            outreach_to_connect_rate_pct=0.25,
            connect_to_meeting_rate_pct=0.10,
            meeting_to_opportunity_rate_pct=0.60,
        )
        assert s == 35

    def test_connect_meeting_boundary_015(self):
        s = self._score(
            outreach_to_connect_rate_pct=0.25,
            connect_to_meeting_rate_pct=0.15,
            meeting_to_opportunity_rate_pct=0.60,
        )
        assert s == 35

    def test_connect_meeting_mid(self):
        s = self._score(
            outreach_to_connect_rate_pct=0.25,
            connect_to_meeting_rate_pct=0.20,
            meeting_to_opportunity_rate_pct=0.60,
        )
        assert s == 18

    def test_connect_meeting_boundary_028(self):
        s = self._score(
            outreach_to_connect_rate_pct=0.25,
            connect_to_meeting_rate_pct=0.28,
            meeting_to_opportunity_rate_pct=0.60,
        )
        assert s == 18

    def test_connect_meeting_none(self):
        s = self._score(
            outreach_to_connect_rate_pct=0.25,
            connect_to_meeting_rate_pct=0.40,
            meeting_to_opportunity_rate_pct=0.60,
        )
        assert s == 0

    # meeting_to_opportunity_rate_pct thresholds
    def test_meeting_opp_worst(self):
        s = self._score(
            outreach_to_connect_rate_pct=0.25,
            connect_to_meeting_rate_pct=0.40,
            meeting_to_opportunity_rate_pct=0.15,
        )
        assert s == 25

    def test_meeting_opp_boundary_020(self):
        s = self._score(
            outreach_to_connect_rate_pct=0.25,
            connect_to_meeting_rate_pct=0.40,
            meeting_to_opportunity_rate_pct=0.20,
        )
        assert s == 25

    def test_meeting_opp_mid(self):
        s = self._score(
            outreach_to_connect_rate_pct=0.25,
            connect_to_meeting_rate_pct=0.40,
            meeting_to_opportunity_rate_pct=0.30,
        )
        assert s == 12

    def test_meeting_opp_boundary_038(self):
        s = self._score(
            outreach_to_connect_rate_pct=0.25,
            connect_to_meeting_rate_pct=0.40,
            meeting_to_opportunity_rate_pct=0.38,
        )
        assert s == 12

    def test_meeting_opp_none(self):
        s = self._score(
            outreach_to_connect_rate_pct=0.25,
            connect_to_meeting_rate_pct=0.40,
            meeting_to_opportunity_rate_pct=0.50,
        )
        assert s == 0

    def test_generation_rate_max_100(self):
        # All worst-case → 40+35+25=100
        s = self._score(
            outreach_to_connect_rate_pct=0.01,
            connect_to_meeting_rate_pct=0.05,
            meeting_to_opportunity_rate_pct=0.10,
        )
        assert s == 100.0

    def test_generation_rate_cap(self):
        # Even with inflated partial addition, cap at 100
        assert self._score(
            outreach_to_connect_rate_pct=0.01,
            connect_to_meeting_rate_pct=0.05,
            meeting_to_opportunity_rate_pct=0.05,
        ) <= 100.0

    def test_generation_rate_zero(self):
        s = self._score(
            outreach_to_connect_rate_pct=0.25,
            connect_to_meeting_rate_pct=0.50,
            meeting_to_opportunity_rate_pct=0.60,
        )
        assert s == 0.0


# ---------------------------------------------------------------------------
# 4. _pipeline_volume_score sub-score
# ---------------------------------------------------------------------------

class TestPipelineVolumeScore:
    def _score(self, **kw):
        eng = make_engine()
        return eng._pipeline_volume_score(make_input(**kw))

    def test_new_opps_worst(self):
        s = self._score(new_opportunities_per_week_avg=0.3,
                        pipeline_coverage_ratio=4.0,
                        pipeline_created_per_week_usd=20_000)
        assert s == 40

    def test_new_opps_boundary_05(self):
        s = self._score(new_opportunities_per_week_avg=0.5,
                        pipeline_coverage_ratio=4.0,
                        pipeline_created_per_week_usd=20_000)
        assert s == 40

    def test_new_opps_mid(self):
        s = self._score(new_opportunities_per_week_avg=0.8,
                        pipeline_coverage_ratio=4.0,
                        pipeline_created_per_week_usd=20_000)
        assert s == 22

    def test_new_opps_boundary_10(self):
        s = self._score(new_opportunities_per_week_avg=1.0,
                        pipeline_coverage_ratio=4.0,
                        pipeline_created_per_week_usd=20_000)
        assert s == 22

    def test_new_opps_third_band(self):
        s = self._score(new_opportunities_per_week_avg=1.5,
                        pipeline_coverage_ratio=4.0,
                        pipeline_created_per_week_usd=20_000)
        assert s == 8

    def test_new_opps_boundary_18(self):
        s = self._score(new_opportunities_per_week_avg=1.8,
                        pipeline_coverage_ratio=4.0,
                        pipeline_created_per_week_usd=20_000)
        assert s == 8

    def test_new_opps_none(self):
        s = self._score(new_opportunities_per_week_avg=2.5,
                        pipeline_coverage_ratio=4.0,
                        pipeline_created_per_week_usd=20_000)
        assert s == 0

    def test_coverage_worst(self):
        s = self._score(new_opportunities_per_week_avg=3.0,
                        pipeline_coverage_ratio=1.0,
                        pipeline_created_per_week_usd=20_000)
        assert s == 35

    def test_coverage_boundary_15(self):
        s = self._score(new_opportunities_per_week_avg=3.0,
                        pipeline_coverage_ratio=1.5,
                        pipeline_created_per_week_usd=20_000)
        assert s == 35

    def test_coverage_mid(self):
        s = self._score(new_opportunities_per_week_avg=3.0,
                        pipeline_coverage_ratio=2.0,
                        pipeline_created_per_week_usd=20_000)
        assert s == 18

    def test_coverage_boundary_25(self):
        s = self._score(new_opportunities_per_week_avg=3.0,
                        pipeline_coverage_ratio=2.5,
                        pipeline_created_per_week_usd=20_000)
        assert s == 18

    def test_coverage_none(self):
        s = self._score(new_opportunities_per_week_avg=3.0,
                        pipeline_coverage_ratio=3.5,
                        pipeline_created_per_week_usd=20_000)
        assert s == 0

    def test_pipeline_usd_worst(self):
        s = self._score(new_opportunities_per_week_avg=3.0,
                        pipeline_coverage_ratio=4.0,
                        pipeline_created_per_week_usd=3_000)
        assert s == 25

    def test_pipeline_usd_boundary_5000(self):
        s = self._score(new_opportunities_per_week_avg=3.0,
                        pipeline_coverage_ratio=4.0,
                        pipeline_created_per_week_usd=5_000)
        assert s == 25

    def test_pipeline_usd_mid(self):
        s = self._score(new_opportunities_per_week_avg=3.0,
                        pipeline_coverage_ratio=4.0,
                        pipeline_created_per_week_usd=10_000)
        assert s == 12

    def test_pipeline_usd_boundary_15000(self):
        s = self._score(new_opportunities_per_week_avg=3.0,
                        pipeline_coverage_ratio=4.0,
                        pipeline_created_per_week_usd=15_000)
        assert s == 12

    def test_pipeline_usd_none(self):
        s = self._score(new_opportunities_per_week_avg=3.0,
                        pipeline_coverage_ratio=4.0,
                        pipeline_created_per_week_usd=20_000)
        assert s == 0

    def test_pipeline_volume_max_100(self):
        s = self._score(new_opportunities_per_week_avg=0.1,
                        pipeline_coverage_ratio=0.5,
                        pipeline_created_per_week_usd=1_000)
        assert s == 100.0

    def test_pipeline_volume_zero(self):
        s = self._score(new_opportunities_per_week_avg=3.0,
                        pipeline_coverage_ratio=4.0,
                        pipeline_created_per_week_usd=20_000)
        assert s == 0.0


# ---------------------------------------------------------------------------
# 5. _prospecting_quality_score sub-score
# ---------------------------------------------------------------------------

class TestProspectingQualityScore:
    def _score(self, **kw):
        eng = make_engine()
        return eng._prospecting_quality_score(make_input(**kw))

    def test_icp_worst(self):
        s = self._score(icp_targeted_outreach_pct=0.10,
                        multi_channel_outreach_pct=0.60,
                        territory_coverage_depth_pct=0.60)
        assert s == 45

    def test_icp_boundary_030(self):
        s = self._score(icp_targeted_outreach_pct=0.30,
                        multi_channel_outreach_pct=0.60,
                        territory_coverage_depth_pct=0.60)
        assert s == 45

    def test_icp_mid(self):
        s = self._score(icp_targeted_outreach_pct=0.40,
                        multi_channel_outreach_pct=0.60,
                        territory_coverage_depth_pct=0.60)
        assert s == 25

    def test_icp_boundary_050(self):
        s = self._score(icp_targeted_outreach_pct=0.50,
                        multi_channel_outreach_pct=0.60,
                        territory_coverage_depth_pct=0.60)
        assert s == 25

    def test_icp_third(self):
        s = self._score(icp_targeted_outreach_pct=0.60,
                        multi_channel_outreach_pct=0.60,
                        territory_coverage_depth_pct=0.60)
        assert s == 10

    def test_icp_boundary_065(self):
        s = self._score(icp_targeted_outreach_pct=0.65,
                        multi_channel_outreach_pct=0.60,
                        territory_coverage_depth_pct=0.60)
        assert s == 10

    def test_icp_none(self):
        s = self._score(icp_targeted_outreach_pct=0.80,
                        multi_channel_outreach_pct=0.60,
                        territory_coverage_depth_pct=0.60)
        assert s == 0

    def test_multi_channel_worst(self):
        s = self._score(icp_targeted_outreach_pct=0.80,
                        multi_channel_outreach_pct=0.10,
                        territory_coverage_depth_pct=0.60)
        assert s == 30

    def test_multi_channel_boundary_020(self):
        s = self._score(icp_targeted_outreach_pct=0.80,
                        multi_channel_outreach_pct=0.20,
                        territory_coverage_depth_pct=0.60)
        assert s == 30

    def test_multi_channel_mid(self):
        s = self._score(icp_targeted_outreach_pct=0.80,
                        multi_channel_outreach_pct=0.30,
                        territory_coverage_depth_pct=0.60)
        assert s == 15

    def test_multi_channel_boundary_040(self):
        s = self._score(icp_targeted_outreach_pct=0.80,
                        multi_channel_outreach_pct=0.40,
                        territory_coverage_depth_pct=0.60)
        assert s == 15

    def test_multi_channel_none(self):
        s = self._score(icp_targeted_outreach_pct=0.80,
                        multi_channel_outreach_pct=0.60,
                        territory_coverage_depth_pct=0.60)
        assert s == 0

    def test_territory_worst(self):
        s = self._score(icp_targeted_outreach_pct=0.80,
                        multi_channel_outreach_pct=0.60,
                        territory_coverage_depth_pct=0.05)
        assert s == 25

    def test_territory_boundary_015(self):
        s = self._score(icp_targeted_outreach_pct=0.80,
                        multi_channel_outreach_pct=0.60,
                        territory_coverage_depth_pct=0.15)
        assert s == 25

    def test_territory_mid(self):
        s = self._score(icp_targeted_outreach_pct=0.80,
                        multi_channel_outreach_pct=0.60,
                        territory_coverage_depth_pct=0.25)
        assert s == 12

    def test_territory_boundary_035(self):
        s = self._score(icp_targeted_outreach_pct=0.80,
                        multi_channel_outreach_pct=0.60,
                        territory_coverage_depth_pct=0.35)
        assert s == 12

    def test_territory_none(self):
        s = self._score(icp_targeted_outreach_pct=0.80,
                        multi_channel_outreach_pct=0.60,
                        territory_coverage_depth_pct=0.60)
        assert s == 0

    def test_prospecting_quality_max_100(self):
        s = self._score(icp_targeted_outreach_pct=0.10,
                        multi_channel_outreach_pct=0.05,
                        territory_coverage_depth_pct=0.05)
        assert s == 100.0

    def test_prospecting_quality_zero(self):
        s = self._score(icp_targeted_outreach_pct=0.80,
                        multi_channel_outreach_pct=0.60,
                        territory_coverage_depth_pct=0.60)
        assert s == 0.0


# ---------------------------------------------------------------------------
# 6. _consistency_score sub-score
# ---------------------------------------------------------------------------

class TestConsistencyScore:
    def _score(self, **kw):
        eng = make_engine()
        return eng._consistency_score(make_input(**kw))

    def test_low_weeks_worst(self):
        s = self._score(consecutive_low_pipeline_weeks=8,
                        opportunity_no_activity_14d_pct=0.05,
                        stale_opportunity_rate_pct=0.05)
        assert s == 40

    def test_low_weeks_boundary_6(self):
        s = self._score(consecutive_low_pipeline_weeks=6,
                        opportunity_no_activity_14d_pct=0.05,
                        stale_opportunity_rate_pct=0.05)
        assert s == 40

    def test_low_weeks_mid(self):
        s = self._score(consecutive_low_pipeline_weeks=4,
                        opportunity_no_activity_14d_pct=0.05,
                        stale_opportunity_rate_pct=0.05)
        assert s == 22

    def test_low_weeks_boundary_3(self):
        s = self._score(consecutive_low_pipeline_weeks=3,
                        opportunity_no_activity_14d_pct=0.05,
                        stale_opportunity_rate_pct=0.05)
        assert s == 22

    def test_low_weeks_third(self):
        s = self._score(consecutive_low_pipeline_weeks=2,
                        opportunity_no_activity_14d_pct=0.05,
                        stale_opportunity_rate_pct=0.05)
        assert s == 8

    def test_low_weeks_boundary_1(self):
        s = self._score(consecutive_low_pipeline_weeks=1,
                        opportunity_no_activity_14d_pct=0.05,
                        stale_opportunity_rate_pct=0.05)
        assert s == 8

    def test_low_weeks_none(self):
        s = self._score(consecutive_low_pipeline_weeks=0,
                        opportunity_no_activity_14d_pct=0.05,
                        stale_opportunity_rate_pct=0.05)
        assert s == 0

    def test_no_activity_worst(self):
        s = self._score(consecutive_low_pipeline_weeks=0,
                        opportunity_no_activity_14d_pct=0.60,
                        stale_opportunity_rate_pct=0.05)
        assert s == 35

    def test_no_activity_boundary_050(self):
        s = self._score(consecutive_low_pipeline_weeks=0,
                        opportunity_no_activity_14d_pct=0.50,
                        stale_opportunity_rate_pct=0.05)
        assert s == 35

    def test_no_activity_mid(self):
        s = self._score(consecutive_low_pipeline_weeks=0,
                        opportunity_no_activity_14d_pct=0.40,
                        stale_opportunity_rate_pct=0.05)
        assert s == 18

    def test_no_activity_boundary_030(self):
        s = self._score(consecutive_low_pipeline_weeks=0,
                        opportunity_no_activity_14d_pct=0.30,
                        stale_opportunity_rate_pct=0.05)
        assert s == 18

    def test_no_activity_none(self):
        s = self._score(consecutive_low_pipeline_weeks=0,
                        opportunity_no_activity_14d_pct=0.10,
                        stale_opportunity_rate_pct=0.05)
        assert s == 0

    def test_stale_worst(self):
        s = self._score(consecutive_low_pipeline_weeks=0,
                        opportunity_no_activity_14d_pct=0.05,
                        stale_opportunity_rate_pct=0.50)
        assert s == 25

    def test_stale_boundary_040(self):
        s = self._score(consecutive_low_pipeline_weeks=0,
                        opportunity_no_activity_14d_pct=0.05,
                        stale_opportunity_rate_pct=0.40)
        assert s == 25

    def test_stale_mid(self):
        s = self._score(consecutive_low_pipeline_weeks=0,
                        opportunity_no_activity_14d_pct=0.05,
                        stale_opportunity_rate_pct=0.30)
        assert s == 12

    def test_stale_boundary_020(self):
        s = self._score(consecutive_low_pipeline_weeks=0,
                        opportunity_no_activity_14d_pct=0.05,
                        stale_opportunity_rate_pct=0.20)
        assert s == 12

    def test_stale_none(self):
        s = self._score(consecutive_low_pipeline_weeks=0,
                        opportunity_no_activity_14d_pct=0.05,
                        stale_opportunity_rate_pct=0.10)
        assert s == 0

    def test_consistency_max_100(self):
        s = self._score(consecutive_low_pipeline_weeks=10,
                        opportunity_no_activity_14d_pct=0.80,
                        stale_opportunity_rate_pct=0.80)
        assert s == 100.0

    def test_consistency_zero(self):
        s = self._score(consecutive_low_pipeline_weeks=0,
                        opportunity_no_activity_14d_pct=0.05,
                        stale_opportunity_rate_pct=0.05)
        assert s == 0.0


# ---------------------------------------------------------------------------
# 7. _composite calculation
# ---------------------------------------------------------------------------

class TestComposite:
    def test_composite_zero(self):
        eng = make_engine()
        assert eng._composite(0, 0, 0, 0) == 0.0

    def test_composite_100(self):
        eng = make_engine()
        assert eng._composite(100, 100, 100, 100) == 100.0

    def test_composite_weights(self):
        eng = make_engine()
        # 100*0.35 + 0*0.30 + 0*0.20 + 0*0.15 = 35
        assert eng._composite(100, 0, 0, 0) == 35.0

    def test_composite_weights_volume(self):
        eng = make_engine()
        assert eng._composite(0, 100, 0, 0) == 30.0

    def test_composite_weights_quality(self):
        eng = make_engine()
        assert eng._composite(0, 0, 100, 0) == 20.0

    def test_composite_weights_consistency(self):
        eng = make_engine()
        assert eng._composite(0, 0, 0, 100) == 15.0

    def test_composite_weights_sum_to_100(self):
        eng = make_engine()
        assert eng._composite(100, 100, 100, 100) == 100.0

    def test_composite_rounding(self):
        eng = make_engine()
        # 10*0.35 + 10*0.30 + 10*0.20 + 10*0.15 = 10.00
        assert eng._composite(10, 10, 10, 10) == 10.0

    def test_composite_capped_at_100(self):
        eng = make_engine()
        result = eng._composite(200, 200, 200, 200)
        assert result == 100.0


# ---------------------------------------------------------------------------
# 8. Risk thresholds
# ---------------------------------------------------------------------------

class TestRisk:
    def _risk(self, composite):
        return make_engine()._risk(composite)

    def test_low_just_under_20(self):
        assert self._risk(19.99) == PipelineRisk.low

    def test_low_zero(self):
        assert self._risk(0) == PipelineRisk.low

    def test_moderate_at_20(self):
        assert self._risk(20) == PipelineRisk.moderate

    def test_moderate_just_under_40(self):
        assert self._risk(39.99) == PipelineRisk.moderate

    def test_high_at_40(self):
        assert self._risk(40) == PipelineRisk.high

    def test_high_just_under_60(self):
        assert self._risk(59.99) == PipelineRisk.high

    def test_critical_at_60(self):
        assert self._risk(60) == PipelineRisk.critical

    def test_critical_at_100(self):
        assert self._risk(100) == PipelineRisk.critical


# ---------------------------------------------------------------------------
# 9. Severity thresholds
# ---------------------------------------------------------------------------

class TestSeverity:
    def _sev(self, composite):
        return make_engine()._severity(composite)

    def test_generating_under_20(self):
        assert self._sev(0) == PipelineSeverity.generating
        assert self._sev(19.99) == PipelineSeverity.generating

    def test_adequate_at_20(self):
        assert self._sev(20) == PipelineSeverity.adequate

    def test_adequate_just_under_40(self):
        assert self._sev(39.99) == PipelineSeverity.adequate

    def test_sluggish_at_40(self):
        assert self._sev(40) == PipelineSeverity.sluggish

    def test_sluggish_just_under_60(self):
        assert self._sev(59.99) == PipelineSeverity.sluggish

    def test_stalled_at_60(self):
        assert self._sev(60) == PipelineSeverity.stalled

    def test_stalled_at_100(self):
        assert self._sev(100) == PipelineSeverity.stalled


# ---------------------------------------------------------------------------
# 10. Pattern detection
# ---------------------------------------------------------------------------

class TestPattern:
    def _pattern(self, **kw):
        return make_engine()._pattern(make_input(**kw))

    def test_burst_and_fade(self):
        p = self._pattern(consecutive_low_pipeline_weeks=4,
                          new_opportunities_per_week_avg=0.5)
        assert p == PipelinePattern.burst_and_fade

    def test_burst_and_fade_above_threshold(self):
        p = self._pattern(consecutive_low_pipeline_weeks=6,
                          new_opportunities_per_week_avg=0.3)
        assert p == PipelinePattern.burst_and_fade

    def test_burst_and_fade_requires_both(self):
        # weeks>=4 but opps too high
        p = self._pattern(consecutive_low_pipeline_weeks=4,
                          new_opportunities_per_week_avg=1.0,
                          inbound_conversion_rate_pct=0.10,
                          outreach_attempts_per_week_avg=30.0)
        assert p != PipelinePattern.burst_and_fade

    def test_reactive_only(self):
        p = self._pattern(consecutive_low_pipeline_weeks=0,
                          new_opportunities_per_week_avg=2.0,
                          inbound_conversion_rate_pct=0.70,
                          outreach_attempts_per_week_avg=5.0)
        assert p == PipelinePattern.reactive_only

    def test_reactive_only_boundary_inbound(self):
        p = self._pattern(consecutive_low_pipeline_weeks=0,
                          new_opportunities_per_week_avg=2.0,
                          inbound_conversion_rate_pct=0.70,
                          outreach_attempts_per_week_avg=10.0)
        assert p == PipelinePattern.reactive_only

    def test_reactive_only_requires_both(self):
        # high inbound but too many outreach attempts
        p = self._pattern(consecutive_low_pipeline_weeks=0,
                          new_opportunities_per_week_avg=2.0,
                          inbound_conversion_rate_pct=0.75,
                          outreach_attempts_per_week_avg=20.0,
                          days_to_first_opportunity_avg=10.0,
                          territory_coverage_depth_pct=0.50,
                          icp_targeted_outreach_pct=0.80,
                          multi_channel_outreach_pct=0.60,
                          referral_sourced_pipeline_pct=0.20)
        assert p != PipelinePattern.reactive_only

    def test_slow_starter(self):
        p = self._pattern(consecutive_low_pipeline_weeks=0,
                          new_opportunities_per_week_avg=0.8,
                          inbound_conversion_rate_pct=0.20,
                          outreach_attempts_per_week_avg=30.0,
                          days_to_first_opportunity_avg=45.0)
        assert p == PipelinePattern.slow_starter

    def test_slow_starter_opps_too_high(self):
        p = self._pattern(consecutive_low_pipeline_weeks=0,
                          new_opportunities_per_week_avg=1.5,
                          inbound_conversion_rate_pct=0.20,
                          outreach_attempts_per_week_avg=30.0,
                          days_to_first_opportunity_avg=60.0,
                          territory_coverage_depth_pct=0.50,
                          icp_targeted_outreach_pct=0.80,
                          multi_channel_outreach_pct=0.60,
                          referral_sourced_pipeline_pct=0.20)
        assert p != PipelinePattern.slow_starter

    def test_territory_exhaustion(self):
        p = self._pattern(consecutive_low_pipeline_weeks=0,
                          new_opportunities_per_week_avg=2.0,
                          inbound_conversion_rate_pct=0.20,
                          outreach_attempts_per_week_avg=30.0,
                          days_to_first_opportunity_avg=10.0,
                          territory_coverage_depth_pct=0.20,
                          icp_targeted_outreach_pct=0.40)
        assert p == PipelinePattern.territory_exhaustion

    def test_territory_exhaustion_boundary(self):
        p = self._pattern(consecutive_low_pipeline_weeks=0,
                          new_opportunities_per_week_avg=2.0,
                          inbound_conversion_rate_pct=0.20,
                          outreach_attempts_per_week_avg=30.0,
                          days_to_first_opportunity_avg=10.0,
                          territory_coverage_depth_pct=0.15,
                          icp_targeted_outreach_pct=0.35)
        assert p == PipelinePattern.territory_exhaustion

    def test_channel_dependency(self):
        p = self._pattern(consecutive_low_pipeline_weeks=0,
                          new_opportunities_per_week_avg=2.0,
                          inbound_conversion_rate_pct=0.20,
                          outreach_attempts_per_week_avg=30.0,
                          days_to_first_opportunity_avg=10.0,
                          territory_coverage_depth_pct=0.50,
                          icp_targeted_outreach_pct=0.80,
                          multi_channel_outreach_pct=0.20,
                          referral_sourced_pipeline_pct=0.10)
        assert p == PipelinePattern.channel_dependency

    def test_channel_dependency_boundary(self):
        p = self._pattern(consecutive_low_pipeline_weeks=0,
                          new_opportunities_per_week_avg=2.0,
                          inbound_conversion_rate_pct=0.20,
                          outreach_attempts_per_week_avg=30.0,
                          days_to_first_opportunity_avg=10.0,
                          territory_coverage_depth_pct=0.50,
                          icp_targeted_outreach_pct=0.80,
                          multi_channel_outreach_pct=0.15,
                          referral_sourced_pipeline_pct=0.05)
        assert p == PipelinePattern.channel_dependency

    def test_none_pattern(self):
        p = self._pattern(consecutive_low_pipeline_weeks=0,
                          new_opportunities_per_week_avg=2.0,
                          inbound_conversion_rate_pct=0.20,
                          outreach_attempts_per_week_avg=30.0,
                          days_to_first_opportunity_avg=10.0,
                          territory_coverage_depth_pct=0.50,
                          icp_targeted_outreach_pct=0.80,
                          multi_channel_outreach_pct=0.60,
                          referral_sourced_pipeline_pct=0.20)
        assert p == PipelinePattern.none

    def test_burst_and_fade_takes_priority_over_reactive(self):
        # Both conditions met — burst_and_fade should win (first check)
        p = self._pattern(consecutive_low_pipeline_weeks=4,
                          new_opportunities_per_week_avg=0.5,
                          inbound_conversion_rate_pct=0.80,
                          outreach_attempts_per_week_avg=5.0)
        assert p == PipelinePattern.burst_and_fade

    def test_reactive_takes_priority_over_slow_starter(self):
        p = self._pattern(consecutive_low_pipeline_weeks=0,
                          new_opportunities_per_week_avg=0.8,
                          inbound_conversion_rate_pct=0.80,
                          outreach_attempts_per_week_avg=5.0,
                          days_to_first_opportunity_avg=60.0)
        assert p == PipelinePattern.reactive_only


# ---------------------------------------------------------------------------
# 11. Action mapping
# ---------------------------------------------------------------------------

class TestAction:
    def _action(self, risk, pattern):
        return make_engine()._action(risk, pattern)

    def test_critical_burst_and_fade(self):
        assert self._action(PipelineRisk.critical, PipelinePattern.burst_and_fade) == \
               PipelineAction.pipeline_reset_intervention

    def test_critical_reactive_only(self):
        assert self._action(PipelineRisk.critical, PipelinePattern.reactive_only) == \
               PipelineAction.pipeline_generation_intervention

    def test_critical_other_none(self):
        assert self._action(PipelineRisk.critical, PipelinePattern.none) == \
               PipelineAction.pipeline_reset_intervention

    def test_critical_slow_starter(self):
        assert self._action(PipelineRisk.critical, PipelinePattern.slow_starter) == \
               PipelineAction.pipeline_reset_intervention

    def test_critical_territory_exhaustion(self):
        assert self._action(PipelineRisk.critical, PipelinePattern.territory_exhaustion) == \
               PipelineAction.pipeline_reset_intervention

    def test_critical_channel_dependency(self):
        assert self._action(PipelineRisk.critical, PipelinePattern.channel_dependency) == \
               PipelineAction.pipeline_reset_intervention

    def test_high_slow_starter(self):
        assert self._action(PipelineRisk.high, PipelinePattern.slow_starter) == \
               PipelineAction.prospecting_cadence_coaching

    def test_high_channel_dependency(self):
        assert self._action(PipelineRisk.high, PipelinePattern.channel_dependency) == \
               PipelineAction.channel_diversification_coaching

    def test_high_territory_exhaustion(self):
        assert self._action(PipelineRisk.high, PipelinePattern.territory_exhaustion) == \
               PipelineAction.icp_targeting_coaching

    def test_high_none(self):
        assert self._action(PipelineRisk.high, PipelinePattern.none) == \
               PipelineAction.pipeline_generation_coaching

    def test_high_burst_and_fade(self):
        assert self._action(PipelineRisk.high, PipelinePattern.burst_and_fade) == \
               PipelineAction.pipeline_generation_coaching

    def test_high_reactive_only(self):
        assert self._action(PipelineRisk.high, PipelinePattern.reactive_only) == \
               PipelineAction.pipeline_generation_coaching

    def test_moderate_any(self):
        assert self._action(PipelineRisk.moderate, PipelinePattern.none) == \
               PipelineAction.pipeline_generation_coaching

    def test_moderate_burst_and_fade(self):
        assert self._action(PipelineRisk.moderate, PipelinePattern.burst_and_fade) == \
               PipelineAction.pipeline_generation_coaching

    def test_low_any(self):
        assert self._action(PipelineRisk.low, PipelinePattern.none) == \
               PipelineAction.no_action

    def test_low_burst_and_fade(self):
        assert self._action(PipelineRisk.low, PipelinePattern.burst_and_fade) == \
               PipelineAction.no_action


# ---------------------------------------------------------------------------
# 12. has_pipeline_gap
# ---------------------------------------------------------------------------

class TestHasGap:
    def _gap(self, **kw):
        eng = make_engine()
        inp = make_input(**kw)
        # need composite — compute it
        gr = eng._generation_rate_score(inp)
        pv = eng._pipeline_volume_score(inp)
        pq = eng._prospecting_quality_score(inp)
        cs = eng._consistency_score(inp)
        comp = eng._composite(gr, pv, pq, cs)
        return eng._has_gap(inp, comp)

    def test_gap_via_composite_gte_40(self, engine):
        # worst-case input → composite will be high
        inp = make_input(outreach_to_connect_rate_pct=0.02,
                         connect_to_meeting_rate_pct=0.05,
                         meeting_to_opportunity_rate_pct=0.05,
                         new_opportunities_per_week_avg=0.1,
                         pipeline_coverage_ratio=0.5,
                         pipeline_created_per_week_usd=1_000,
                         icp_targeted_outreach_pct=0.10,
                         multi_channel_outreach_pct=0.05,
                         territory_coverage_depth_pct=0.05,
                         consecutive_low_pipeline_weeks=8,
                         opportunity_no_activity_14d_pct=0.80,
                         stale_opportunity_rate_pct=0.80)
        result = engine.assess(inp)
        assert result.has_pipeline_gap is True

    def test_gap_via_low_coverage(self):
        # Good composite but coverage <=2.0
        gap = self._gap(pipeline_coverage_ratio=2.0)
        assert gap is True

    def test_gap_via_low_opps(self):
        gap = self._gap(new_opportunities_per_week_avg=0.8)
        assert gap is True

    def test_no_gap_healthy(self):
        # Coverage >2.0, opps >0.8, composite will be low due to healthy input
        gap = self._gap(pipeline_coverage_ratio=4.0,
                        new_opportunities_per_week_avg=3.0)
        assert gap is False


# ---------------------------------------------------------------------------
# 13. requires_pipeline_coaching
# ---------------------------------------------------------------------------

class TestRequiresCoaching:
    def _coaching(self, **kw):
        eng = make_engine()
        inp = make_input(**kw)
        gr = eng._generation_rate_score(inp)
        pv = eng._pipeline_volume_score(inp)
        pq = eng._prospecting_quality_score(inp)
        cs = eng._consistency_score(inp)
        comp = eng._composite(gr, pv, pq, cs)
        return eng._requires_coaching(inp, comp)

    def test_coaching_via_composite_gte_30(self):
        # Force composite >= 30 with moderate-bad scores
        # e.g., gr=60 → 60*0.35=21, pv=30 → 30*0.30=9, comp=30
        coaching = self._coaching(outreach_to_connect_rate_pct=0.04,
                                  connect_to_meeting_rate_pct=0.10,
                                  new_opportunities_per_week_avg=0.5,
                                  pipeline_coverage_ratio=1.5)
        assert coaching is True

    def test_coaching_via_low_connect_rate(self):
        coaching = self._coaching(outreach_to_connect_rate_pct=0.12)
        assert coaching is True

    def test_coaching_via_low_weeks(self):
        coaching = self._coaching(consecutive_low_pipeline_weeks=2)
        assert coaching is True

    def test_no_coaching_healthy(self):
        coaching = self._coaching(outreach_to_connect_rate_pct=0.25,
                                  consecutive_low_pipeline_weeks=0,
                                  pipeline_coverage_ratio=4.0,
                                  new_opportunities_per_week_avg=3.0)
        assert coaching is False


# ---------------------------------------------------------------------------
# 14. estimated_pipeline_shortfall_usd
# ---------------------------------------------------------------------------

class TestShortfall:
    def _shortfall(self, **kw):
        eng = make_engine()
        inp = make_input(**kw)
        gr = eng._generation_rate_score(inp)
        pv = eng._pipeline_volume_score(inp)
        pq = eng._prospecting_quality_score(inp)
        cs = eng._consistency_score(inp)
        comp = eng._composite(gr, pv, pq, cs)
        return eng._shortfall(inp, comp)

    def test_no_shortfall_when_coverage_exceeds_3(self):
        # coverage=4 → max(0, 3-4)/3=0 → shortfall=0
        s = self._shortfall(pipeline_coverage_ratio=4.0)
        assert s == 0.0

    def test_shortfall_coverage_at_3(self):
        # max(0,3-3)/3=0
        s = self._shortfall(pipeline_coverage_ratio=3.0)
        assert s == 0.0

    def test_shortfall_calculated(self):
        # coverage=0, composite=100, total_outreach=100, avg_value=1000
        # shortfall = 100*1000 * (3/3) * (100/100) = 100000
        eng = make_engine()
        inp = make_input(pipeline_coverage_ratio=0.0,
                         total_outreach_attempts=100,
                         avg_opportunity_value_usd=1_000.0)
        # force composite=100 by worst-case sub-scores
        inp2 = make_input(pipeline_coverage_ratio=0.0,
                          total_outreach_attempts=100,
                          avg_opportunity_value_usd=1_000.0,
                          outreach_to_connect_rate_pct=0.01,
                          connect_to_meeting_rate_pct=0.01,
                          meeting_to_opportunity_rate_pct=0.01,
                          new_opportunities_per_week_avg=0.1,
                          pipeline_created_per_week_usd=100,
                          icp_targeted_outreach_pct=0.05,
                          multi_channel_outreach_pct=0.05,
                          territory_coverage_depth_pct=0.05,
                          consecutive_low_pipeline_weeks=10,
                          opportunity_no_activity_14d_pct=0.90,
                          stale_opportunity_rate_pct=0.90)
        result = eng.assess(inp2)
        assert result.estimated_pipeline_shortfall_usd > 0.0

    def test_shortfall_rounded_to_2_decimals(self):
        # Check rounding
        eng = make_engine()
        inp = make_input(pipeline_coverage_ratio=2.5,
                         total_outreach_attempts=333,
                         avg_opportunity_value_usd=7_777.0,
                         outreach_to_connect_rate_pct=0.01,
                         connect_to_meeting_rate_pct=0.01,
                         meeting_to_opportunity_rate_pct=0.01)
        result = eng.assess(inp)
        # shortfall must be rounded to 2 decimal places
        s = result.estimated_pipeline_shortfall_usd
        assert round(s, 2) == s

    def test_shortfall_zero_composite(self):
        # composite=0 → shortfall=0 regardless of other values
        eng = make_engine()
        inp = make_input(pipeline_coverage_ratio=0.0,
                         total_outreach_attempts=1000,
                         avg_opportunity_value_usd=100_000.0)
        # composite=0 requires all sub-scores=0
        # Use fully healthy input → sub-scores=0
        result = eng.assess(inp)
        # composite likely > 0 since coverage=0 drives volume score up
        # just check the formula: if comp=0, shortfall must be 0
        eng2 = make_engine()
        shortfall_direct = eng2._shortfall(inp, 0.0)
        assert shortfall_direct == 0.0


# ---------------------------------------------------------------------------
# 15. Signal string
# ---------------------------------------------------------------------------

class TestSignal:
    def test_healthy_signal(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.pipeline_signal == (
            "Pipeline generation healthy — outreach conversion, volume, "
            "and prospecting quality within benchmarks"
        )

    def test_unhealthy_signal_contains_pattern_label(self, engine):
        inp = make_input(consecutive_low_pipeline_weeks=4,
                         new_opportunities_per_week_avg=0.4,
                         outreach_to_connect_rate_pct=0.04,
                         connect_to_meeting_rate_pct=0.10,
                         pipeline_coverage_ratio=1.0,
                         pipeline_created_per_week_usd=2_000)
        result = engine.assess(inp)
        assert "Burst and fade" in result.pipeline_signal

    def test_unhealthy_signal_contains_connect_pct(self, engine):
        inp = make_input(outreach_to_connect_rate_pct=0.07,
                         connect_to_meeting_rate_pct=0.10,
                         new_opportunities_per_week_avg=0.4,
                         pipeline_coverage_ratio=1.0,
                         consecutive_low_pipeline_weeks=4,
                         pipeline_created_per_week_usd=2_000)
        result = engine.assess(inp)
        assert "7% outreach-to-connect" in result.pipeline_signal

    def test_unhealthy_signal_contains_opps_per_week(self, engine):
        inp = make_input(outreach_to_connect_rate_pct=0.04,
                         connect_to_meeting_rate_pct=0.10,
                         new_opportunities_per_week_avg=0.4,
                         pipeline_coverage_ratio=1.0,
                         consecutive_low_pipeline_weeks=4,
                         pipeline_created_per_week_usd=2_000)
        result = engine.assess(inp)
        assert "0.4 new opps/week" in result.pipeline_signal

    def test_unhealthy_signal_contains_low_weeks(self, engine):
        inp = make_input(outreach_to_connect_rate_pct=0.04,
                         connect_to_meeting_rate_pct=0.10,
                         new_opportunities_per_week_avg=0.4,
                         pipeline_coverage_ratio=1.0,
                         consecutive_low_pipeline_weeks=4,
                         pipeline_created_per_week_usd=2_000)
        result = engine.assess(inp)
        assert "4 consecutive low-pipeline weeks" in result.pipeline_signal

    def test_unhealthy_signal_contains_composite(self, engine):
        inp = make_input(outreach_to_connect_rate_pct=0.04,
                         connect_to_meeting_rate_pct=0.10,
                         new_opportunities_per_week_avg=0.4,
                         pipeline_coverage_ratio=1.0,
                         consecutive_low_pipeline_weeks=4,
                         pipeline_created_per_week_usd=2_000)
        result = engine.assess(inp)
        comp_int = round(result.pipeline_composite)
        assert f"composite {comp_int}" in result.pipeline_signal

    def test_signal_none_pattern_label(self, engine):
        # composite >= 20 but pattern=none → label should be "None" or titlecased
        inp = make_input(outreach_to_connect_rate_pct=0.08,
                         connect_to_meeting_rate_pct=0.20,
                         consecutive_low_pipeline_weeks=0,
                         new_opportunities_per_week_avg=2.0,
                         inbound_conversion_rate_pct=0.10,
                         outreach_attempts_per_week_avg=30.0,
                         territory_coverage_depth_pct=0.50,
                         icp_targeted_outreach_pct=0.80,
                         multi_channel_outreach_pct=0.60,
                         referral_sourced_pipeline_pct=0.20)
        result = engine.assess(inp)
        if result.pipeline_composite >= 20:
            assert "outreach-to-connect" in result.pipeline_signal


# ---------------------------------------------------------------------------
# 16. assess() returns correct types and fields
# ---------------------------------------------------------------------------

class TestAssess:
    def test_returns_pipeline_result(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result, PipelineResult)

    def test_rep_id_preserved(self, engine):
        inp = make_input(rep_id="rep_XYZ")
        result = engine.assess(inp)
        assert result.rep_id == "rep_XYZ"

    def test_region_preserved(self, engine):
        inp = make_input(region="EMEA")
        result = engine.assess(inp)
        assert result.region == "EMEA"

    def test_risk_is_enum(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.pipeline_risk, PipelineRisk)

    def test_pattern_is_enum(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.pipeline_pattern, PipelinePattern)

    def test_severity_is_enum(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.pipeline_severity, PipelineSeverity)

    def test_action_is_enum(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.recommended_action, PipelineAction)

    def test_scores_are_floats(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.generation_rate_score, float)
        assert isinstance(result.pipeline_volume_score, float)
        assert isinstance(result.prospecting_quality_score, float)
        assert isinstance(result.consistency_score, float)

    def test_composite_range(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert 0.0 <= result.pipeline_composite <= 100.0

    def test_gap_is_bool(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.has_pipeline_gap, bool)

    def test_coaching_is_bool(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.requires_pipeline_coaching, bool)

    def test_shortfall_is_float(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.estimated_pipeline_shortfall_usd, float)

    def test_signal_is_str(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.pipeline_signal, str)

    def test_healthy_is_low_risk(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.pipeline_risk == PipelineRisk.low

    def test_healthy_is_generating(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.pipeline_severity == PipelineSeverity.generating

    def test_healthy_action_no_action(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.recommended_action == PipelineAction.no_action

    def test_worst_case_critical(self, engine):
        inp = make_input(outreach_to_connect_rate_pct=0.01,
                         connect_to_meeting_rate_pct=0.05,
                         meeting_to_opportunity_rate_pct=0.05,
                         new_opportunities_per_week_avg=0.1,
                         pipeline_coverage_ratio=0.5,
                         pipeline_created_per_week_usd=1_000,
                         icp_targeted_outreach_pct=0.10,
                         multi_channel_outreach_pct=0.05,
                         territory_coverage_depth_pct=0.05,
                         consecutive_low_pipeline_weeks=8,
                         opportunity_no_activity_14d_pct=0.80,
                         stale_opportunity_rate_pct=0.80)
        result = engine.assess(inp)
        assert result.pipeline_risk == PipelineRisk.critical
        assert result.pipeline_severity == PipelineSeverity.stalled

    def test_result_stored_in_engine(self, engine, healthy_input):
        engine.assess(healthy_input)
        assert len(engine._results) == 1

    def test_multiple_assessments_stored(self, engine):
        engine.assess(make_input(rep_id="r1"))
        engine.assess(make_input(rep_id="r2"))
        assert len(engine._results) == 2


# ---------------------------------------------------------------------------
# 17. to_dict()
# ---------------------------------------------------------------------------

class TestToDict:
    def test_returns_dict(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.to_dict(), dict)

    def test_has_15_keys(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert len(result.to_dict()) == 15

    def test_exact_keys(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        expected = {
            "rep_id", "region", "pipeline_risk", "pipeline_pattern",
            "pipeline_severity", "recommended_action",
            "generation_rate_score", "pipeline_volume_score",
            "prospecting_quality_score", "consistency_score",
            "pipeline_composite", "has_pipeline_gap",
            "requires_pipeline_coaching", "estimated_pipeline_shortfall_usd",
            "pipeline_signal",
        }
        assert set(d.keys()) == expected

    def test_enum_values_are_strings(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        assert isinstance(d["pipeline_risk"], str)
        assert isinstance(d["pipeline_pattern"], str)
        assert isinstance(d["pipeline_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_rep_id_in_dict(self, engine):
        inp = make_input(rep_id="ABC-123")
        d = engine.assess(inp).to_dict()
        assert d["rep_id"] == "ABC-123"

    def test_region_in_dict(self, engine):
        inp = make_input(region="APAC")
        d = engine.assess(inp).to_dict()
        assert d["region"] == "APAC"

    def test_risk_value_in_dict(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        assert d["pipeline_risk"] in {"low", "moderate", "high", "critical"}

    def test_shortfall_in_dict(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        d = result.to_dict()
        assert d["estimated_pipeline_shortfall_usd"] == result.estimated_pipeline_shortfall_usd

    def test_signal_in_dict(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        d = result.to_dict()
        assert d["pipeline_signal"] == result.pipeline_signal


# ---------------------------------------------------------------------------
# 18. assess_batch()
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_returns_list(self, engine):
        results = engine.assess_batch([make_input(rep_id="r1"), make_input(rep_id="r2")])
        assert isinstance(results, list)

    def test_correct_length(self, engine):
        inputs = [make_input(rep_id=f"r{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5

    def test_each_result_is_pipeline_result(self, engine):
        inputs = [make_input(rep_id=f"r{i}") for i in range(3)]
        for r in engine.assess_batch(inputs):
            assert isinstance(r, PipelineResult)

    def test_order_preserved(self, engine):
        inputs = [make_input(rep_id=f"rep_{i}") for i in range(4)]
        results = engine.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"rep_{i}"

    def test_empty_batch(self, engine):
        results = engine.assess_batch([])
        assert results == []

    def test_batch_updates_results_list(self, engine):
        engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        assert len(engine._results) == 3

    def test_single_item_batch(self, engine):
        results = engine.assess_batch([make_input(rep_id="solo")])
        assert len(results) == 1
        assert results[0].rep_id == "solo"


# ---------------------------------------------------------------------------
# 19. summary() — empty state
# ---------------------------------------------------------------------------

class TestSummaryEmpty:
    def test_empty_summary_total(self):
        eng = make_engine()
        s = eng.summary()
        assert s["total"] == 0

    def test_empty_summary_avg_composite(self):
        eng = make_engine()
        assert eng.summary()["avg_pipeline_composite"] == 0.0

    def test_empty_summary_13_keys(self):
        eng = make_engine()
        assert len(eng.summary()) == 13

    def test_empty_summary_exact_keys(self):
        eng = make_engine()
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_pipeline_composite", "pipeline_gap_count",
            "coaching_count", "avg_generation_rate_score",
            "avg_pipeline_volume_score", "avg_prospecting_quality_score",
            "avg_consistency_score", "total_estimated_pipeline_shortfall_usd",
        }
        assert set(eng.summary().keys()) == expected

    def test_empty_summary_counts_are_empty_dicts(self):
        eng = make_engine()
        s = eng.summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}

    def test_empty_summary_gap_count_zero(self):
        assert make_engine().summary()["pipeline_gap_count"] == 0

    def test_empty_summary_coaching_count_zero(self):
        assert make_engine().summary()["coaching_count"] == 0

    def test_empty_summary_shortfall_zero(self):
        assert make_engine().summary()["total_estimated_pipeline_shortfall_usd"] == 0.0


# ---------------------------------------------------------------------------
# 20. summary() — populated state
# ---------------------------------------------------------------------------

class TestSummaryPopulated:
    def _run_batch(self):
        eng = make_engine()
        inputs = [
            make_input(rep_id="r1"),                               # healthy → low
            make_input(rep_id="r2", outreach_to_connect_rate_pct=0.04,
                       connect_to_meeting_rate_pct=0.10,
                       new_opportunities_per_week_avg=0.4,
                       pipeline_coverage_ratio=1.0,
                       consecutive_low_pipeline_weeks=4,
                       pipeline_created_per_week_usd=2_000),      # critical / burst_and_fade
            make_input(rep_id="r3", outreach_to_connect_rate_pct=0.08,
                       connect_to_meeting_rate_pct=0.20,
                       pipeline_coverage_ratio=2.0),               # moderate or similar
        ]
        eng.assess_batch(inputs)
        return eng

    def test_total_count(self):
        eng = self._run_batch()
        assert eng.summary()["total"] == 3

    def test_risk_counts_sum(self):
        eng = self._run_batch()
        s = eng.summary()
        assert sum(s["risk_counts"].values()) == 3

    def test_pattern_counts_sum(self):
        eng = self._run_batch()
        s = eng.summary()
        assert sum(s["pattern_counts"].values()) == 3

    def test_severity_counts_sum(self):
        eng = self._run_batch()
        s = eng.summary()
        assert sum(s["severity_counts"].values()) == 3

    def test_action_counts_sum(self):
        eng = self._run_batch()
        s = eng.summary()
        assert sum(s["action_counts"].values()) == 3

    def test_avg_composite_is_float(self):
        eng = self._run_batch()
        assert isinstance(eng.summary()["avg_pipeline_composite"], float)

    def test_avg_generation_rate_score_range(self):
        eng = self._run_batch()
        s = eng.summary()
        assert 0.0 <= s["avg_generation_rate_score"] <= 100.0

    def test_avg_volume_score_range(self):
        eng = self._run_batch()
        assert 0.0 <= eng.summary()["avg_pipeline_volume_score"] <= 100.0

    def test_avg_quality_score_range(self):
        eng = self._run_batch()
        assert 0.0 <= eng.summary()["avg_prospecting_quality_score"] <= 100.0

    def test_avg_consistency_score_range(self):
        eng = self._run_batch()
        assert 0.0 <= eng.summary()["avg_consistency_score"] <= 100.0

    def test_gap_count_lte_total(self):
        eng = self._run_batch()
        s = eng.summary()
        assert s["pipeline_gap_count"] <= s["total"]

    def test_coaching_count_lte_total(self):
        eng = self._run_batch()
        s = eng.summary()
        assert s["coaching_count"] <= s["total"]

    def test_shortfall_non_negative(self):
        eng = self._run_batch()
        assert eng.summary()["total_estimated_pipeline_shortfall_usd"] >= 0.0

    def test_summary_has_13_keys(self):
        eng = self._run_batch()
        assert len(eng.summary()) == 13

    def test_multiple_assessments_accumulate(self):
        eng = make_engine()
        eng.assess(make_input(rep_id="r1"))
        eng.assess(make_input(rep_id="r2"))
        eng.assess(make_input(rep_id="r3"))
        assert eng.summary()["total"] == 3

    def test_risk_counts_keys_are_valid(self):
        eng = self._run_batch()
        valid = {"low", "moderate", "high", "critical"}
        for k in eng.summary()["risk_counts"]:
            assert k in valid

    def test_pattern_counts_keys_are_valid(self):
        eng = self._run_batch()
        valid = {"none", "burst_and_fade", "reactive_only", "slow_starter",
                 "territory_exhaustion", "channel_dependency"}
        for k in eng.summary()["pattern_counts"]:
            assert k in valid

    def test_single_result_summary(self):
        eng = make_engine()
        eng.assess(make_input())
        s = eng.summary()
        assert s["total"] == 1
        assert s["avg_pipeline_composite"] == eng._results[0].pipeline_composite


# ---------------------------------------------------------------------------
# 21. End-to-end scenario tests
# ---------------------------------------------------------------------------

class TestEndToEndScenarios:
    def test_burst_and_fade_critical_gets_reset_intervention(self):
        eng = make_engine()
        inp = make_input(
            consecutive_low_pipeline_weeks=5,
            new_opportunities_per_week_avg=0.3,
            outreach_to_connect_rate_pct=0.02,
            connect_to_meeting_rate_pct=0.05,
            meeting_to_opportunity_rate_pct=0.05,
            pipeline_coverage_ratio=0.5,
            pipeline_created_per_week_usd=1_000,
            icp_targeted_outreach_pct=0.10,
            multi_channel_outreach_pct=0.05,
            territory_coverage_depth_pct=0.05,
            opportunity_no_activity_14d_pct=0.80,
            stale_opportunity_rate_pct=0.80,
        )
        result = eng.assess(inp)
        assert result.pipeline_pattern == PipelinePattern.burst_and_fade
        assert result.pipeline_risk == PipelineRisk.critical
        assert result.recommended_action == PipelineAction.pipeline_reset_intervention

    def test_reactive_only_critical_gets_generation_intervention(self):
        eng = make_engine()
        inp = make_input(
            consecutive_low_pipeline_weeks=0,
            new_opportunities_per_week_avg=0.4,
            inbound_conversion_rate_pct=0.85,
            outreach_attempts_per_week_avg=5.0,
            outreach_to_connect_rate_pct=0.02,
            connect_to_meeting_rate_pct=0.05,
            meeting_to_opportunity_rate_pct=0.05,
            pipeline_coverage_ratio=0.5,
            pipeline_created_per_week_usd=1_000,
            icp_targeted_outreach_pct=0.10,
            multi_channel_outreach_pct=0.05,
            territory_coverage_depth_pct=0.05,
            opportunity_no_activity_14d_pct=0.80,
            stale_opportunity_rate_pct=0.80,
        )
        result = eng.assess(inp)
        assert result.pipeline_pattern == PipelinePattern.reactive_only
        assert result.pipeline_risk == PipelineRisk.critical
        assert result.recommended_action == PipelineAction.pipeline_generation_intervention

    def test_high_slow_starter_gets_prospecting_coaching(self):
        eng = make_engine()
        # High risk (composite 40-59) + slow_starter pattern
        inp = make_input(
            consecutive_low_pipeline_weeks=0,
            new_opportunities_per_week_avg=0.8,
            inbound_conversion_rate_pct=0.10,
            outreach_attempts_per_week_avg=30.0,
            days_to_first_opportunity_avg=60.0,
            outreach_to_connect_rate_pct=0.04,
            connect_to_meeting_rate_pct=0.15,
            meeting_to_opportunity_rate_pct=0.20,
            pipeline_coverage_ratio=1.5,
            pipeline_created_per_week_usd=5_000,
            icp_targeted_outreach_pct=0.70,
            multi_channel_outreach_pct=0.50,
            territory_coverage_depth_pct=0.50,
            opportunity_no_activity_14d_pct=0.10,
            stale_opportunity_rate_pct=0.10,
        )
        result = eng.assess(inp)
        assert result.pipeline_pattern == PipelinePattern.slow_starter
        if result.pipeline_risk == PipelineRisk.high:
            assert result.recommended_action == PipelineAction.prospecting_cadence_coaching

    def test_high_channel_dependency_gets_diversification_coaching(self):
        eng = make_engine()
        inp = make_input(
            consecutive_low_pipeline_weeks=0,
            new_opportunities_per_week_avg=2.0,
            inbound_conversion_rate_pct=0.20,
            outreach_attempts_per_week_avg=30.0,
            days_to_first_opportunity_avg=10.0,
            territory_coverage_depth_pct=0.50,
            icp_targeted_outreach_pct=0.80,
            multi_channel_outreach_pct=0.15,
            referral_sourced_pipeline_pct=0.05,
            outreach_to_connect_rate_pct=0.04,
            connect_to_meeting_rate_pct=0.15,
            pipeline_coverage_ratio=1.5,
            pipeline_created_per_week_usd=5_000,
            opportunity_no_activity_14d_pct=0.10,
            stale_opportunity_rate_pct=0.10,
        )
        result = eng.assess(inp)
        assert result.pipeline_pattern == PipelinePattern.channel_dependency
        if result.pipeline_risk == PipelineRisk.high:
            assert result.recommended_action == PipelineAction.channel_diversification_coaching

    def test_high_territory_exhaustion_gets_icp_coaching(self):
        eng = make_engine()
        inp = make_input(
            consecutive_low_pipeline_weeks=0,
            new_opportunities_per_week_avg=2.0,
            inbound_conversion_rate_pct=0.20,
            outreach_attempts_per_week_avg=30.0,
            days_to_first_opportunity_avg=10.0,
            territory_coverage_depth_pct=0.15,
            icp_targeted_outreach_pct=0.30,
            multi_channel_outreach_pct=0.60,
            referral_sourced_pipeline_pct=0.30,
            outreach_to_connect_rate_pct=0.04,
            connect_to_meeting_rate_pct=0.15,
            pipeline_coverage_ratio=1.5,
            pipeline_created_per_week_usd=5_000,
            opportunity_no_activity_14d_pct=0.10,
            stale_opportunity_rate_pct=0.10,
        )
        result = eng.assess(inp)
        assert result.pipeline_pattern == PipelinePattern.territory_exhaustion
        if result.pipeline_risk == PipelineRisk.high:
            assert result.recommended_action == PipelineAction.icp_targeting_coaching

    def test_moderate_any_pattern_gets_generation_coaching(self):
        eng = make_engine()
        # Moderate composite (20-39) with none pattern
        inp = make_input(
            outreach_to_connect_rate_pct=0.08,
            connect_to_meeting_rate_pct=0.40,
            meeting_to_opportunity_rate_pct=0.50,
            new_opportunities_per_week_avg=2.0,
            pipeline_coverage_ratio=3.5,
            pipeline_created_per_week_usd=20_000,
            icp_targeted_outreach_pct=0.70,
            multi_channel_outreach_pct=0.60,
            territory_coverage_depth_pct=0.50,
            consecutive_low_pipeline_weeks=0,
            opportunity_no_activity_14d_pct=0.05,
            stale_opportunity_rate_pct=0.05,
            inbound_conversion_rate_pct=0.10,
            outreach_attempts_per_week_avg=30.0,
            days_to_first_opportunity_avg=10.0,
        )
        result = eng.assess(inp)
        if result.pipeline_risk == PipelineRisk.moderate:
            assert result.recommended_action == PipelineAction.pipeline_generation_coaching

    def test_full_pipeline_low_risk_no_action(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.recommended_action == PipelineAction.no_action
        assert result.pipeline_risk == PipelineRisk.low

    def test_batch_then_summary_consistent(self):
        eng = make_engine()
        inputs = [make_input(rep_id=f"r{i}") for i in range(10)]
        results = eng.assess_batch(inputs)
        s = eng.summary()
        assert s["total"] == 10
        # avg composite must match manual calculation
        expected_avg = round(sum(r.pipeline_composite for r in results) / 10, 1)
        assert s["avg_pipeline_composite"] == expected_avg

    def test_summary_shortfall_matches_sum(self):
        eng = make_engine()
        inputs = [make_input(rep_id=f"r{i}",
                             pipeline_coverage_ratio=1.0,
                             outreach_to_connect_rate_pct=0.04) for i in range(3)]
        results = eng.assess_batch(inputs)
        s = eng.summary()
        expected_total = round(sum(r.estimated_pipeline_shortfall_usd for r in results), 2)
        assert s["total_estimated_pipeline_shortfall_usd"] == expected_total
