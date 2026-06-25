"""Tests for PipelineVelocityEngine"""
import pytest
from dataclasses import fields as dc_fields
from intelligence.pipeline_velocity_engine import (
    PipelineVelocityEngine, PipelineVelocityInput, PipelineVelocityResult,
    VelocityRisk, VelocityPattern, VelocitySeverity, VelocityAction,
)


@pytest.fixture
def engine():
    return PipelineVelocityEngine()


@pytest.fixture
def flowing_input():
    return PipelineVelocityInput(
        total_pipeline_value=1200000.0, deals_in_pipeline=40,
        avg_deal_value=30000.0, avg_sales_cycle_days=50.0,
        win_rate_pct=35.0,
        stage_1_count=12, stage_2_count=10, stage_3_count=10, stage_4_count=6, stage_5_count=2,
        stage_1_avg_days=9.0, stage_2_avg_days=11.0, stage_3_avg_days=12.0, stage_4_avg_days=13.0,
        deals_no_activity_14d=4, deals_past_expected_close=2,
        new_deals_added_30d=14, deals_closed_30d=7, deals_lost_30d=3,
        pipeline_coverage_ratio=3.0, quota=400000.0,
        historical_cycle_benchmark=50.0,
    )


@pytest.fixture
def blocked_input():
    return PipelineVelocityInput(
        total_pipeline_value=300000.0, deals_in_pipeline=30,
        avg_deal_value=10000.0, avg_sales_cycle_days=120.0,
        win_rate_pct=10.0,
        stage_1_count=2, stage_2_count=3, stage_3_count=5, stage_4_count=10, stage_5_count=10,
        stage_1_avg_days=25.0, stage_2_avg_days=35.0, stage_3_avg_days=40.0, stage_4_avg_days=50.0,
        deals_no_activity_14d=20, deals_past_expected_close=12,
        new_deals_added_30d=2, deals_closed_30d=1, deals_lost_30d=8,
        pipeline_coverage_ratio=0.75, quota=400000.0,
        historical_cycle_benchmark=50.0,
    )


class TestResultStructure:
    def test_result_has_15_fields(self):
        assert len(dc_fields(PipelineVelocityResult)) == 15

    def test_to_dict_has_15_keys(self, engine, flowing_input):
        assert len(engine.assess(flowing_input).to_dict()) == 15

    def test_to_dict_keys(self, engine, flowing_input):
        d = engine.assess(flowing_input).to_dict()
        expected = {
            "composite_score", "risk", "pattern", "severity", "action",
            "velocity_index", "stage_flow_score", "activity_score", "coverage_score",
            "pipeline_velocity_value", "bottleneck_stage", "stale_deal_pct",
            "projected_close_30d", "signal", "deals_at_risk_count",
        }
        assert set(d.keys()) == expected


class TestFlowingPipeline:
    def test_flowing_low_or_moderate_risk(self, engine, flowing_input):
        r = engine.assess(flowing_input)
        assert r.risk in (VelocityRisk.low, VelocityRisk.moderate)

    def test_flowing_coverage_score_high(self, engine, flowing_input):
        r = engine.assess(flowing_input)
        assert r.coverage_score >= 75

    def test_flowing_velocity_value_positive(self, engine, flowing_input):
        r = engine.assess(flowing_input)
        assert r.pipeline_velocity_value > 0

    def test_stale_pct_non_negative(self, engine, flowing_input):
        r = engine.assess(flowing_input)
        assert r.stale_deal_pct >= 0


class TestBlockedPipeline:
    def test_blocked_returns_high_or_critical(self, engine, blocked_input):
        r = engine.assess(blocked_input)
        assert r.risk in (VelocityRisk.high, VelocityRisk.critical)

    def test_blocked_severity_stalling_or_blocked(self, engine, blocked_input):
        r = engine.assess(blocked_input)
        assert r.severity in (VelocitySeverity.stalling, VelocitySeverity.blocked)

    def test_blocked_deals_at_risk_high(self, engine, blocked_input):
        r = engine.assess(blocked_input)
        assert r.deals_at_risk_count > 10


class TestScoreBoundaries:
    def test_composite_bounded(self, engine):
        for inp in [PipelineVelocityInput(), PipelineVelocityInput(deals_in_pipeline=0),
                    PipelineVelocityInput(pipeline_coverage_ratio=0.0)]:
            r = engine.assess(inp)
            assert 0 <= r.composite_score <= 100

    def test_sub_scores_bounded(self, engine, flowing_input):
        r = engine.assess(flowing_input)
        for s in [r.velocity_index, r.stage_flow_score, r.activity_score, r.coverage_score]:
            assert 0 <= s <= 100


class TestPatternDetection:
    def test_deal_evaporation_detected(self, engine):
        inp = PipelineVelocityInput(pipeline_coverage_ratio=0.5,
                                     deals_no_activity_14d=3, deals_in_pipeline=30)
        r = engine.assess(inp)
        assert r.pattern == VelocityPattern.deal_evaporation

    def test_velocity_collapse_detected(self, engine):
        inp = PipelineVelocityInput(deals_in_pipeline=20, deals_no_activity_14d=14,
                                     pipeline_coverage_ratio=2.0)
        r = engine.assess(inp)
        assert r.pattern == VelocityPattern.velocity_collapse

    def test_action_matches_pattern(self, engine, blocked_input):
        r = engine.assess(blocked_input)
        action_map = {
            VelocityPattern.deal_evaporation: VelocityAction.pipeline_purge,
            VelocityPattern.velocity_collapse: VelocityAction.full_velocity_intervention,
        }
        if r.pattern in action_map:
            assert r.action == action_map[r.pattern]


class TestBottleneckDetection:
    def test_bottleneck_stage_is_valid(self, engine, flowing_input):
        r = engine.assess(flowing_input)
        assert r.bottleneck_stage in (1, 2, 3, 4)


class TestBatchSummary:
    def test_batch_length(self, engine, flowing_input, blocked_input):
        assert len(engine.batch([flowing_input, blocked_input])) == 2

    def test_summary_13_keys(self, engine, flowing_input, blocked_input):
        results = engine.batch([flowing_input, blocked_input])
        assert len(engine.summary(results)) == 13

    def test_summary_empty(self, engine):
        assert engine.summary([]) == {}

    def test_summary_total_pipelines(self, engine, flowing_input, blocked_input):
        results = engine.batch([flowing_input, blocked_input])
        assert engine.summary(results)["total_pipelines"] == 2
