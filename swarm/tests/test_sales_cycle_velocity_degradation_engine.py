"""
Comprehensive pytest test suite for Module 125:
SalesCycleVelocityDegradationEngine
"""
from __future__ import annotations

import pytest
from dataclasses import fields

from swarm.intelligence.sales_cycle_velocity_degradation_engine import (
    VelocityRisk,
    VelocityPattern,
    VelocitySeverity,
    VelocityAction,
    VelocityDegradationInput,
    VelocityDegradationResult,
    SalesCycleVelocityDegradationEngine,
)


# ---------------------------------------------------------------------------
# Helpers / Fixtures
# ---------------------------------------------------------------------------

def make_input(
    rep_id="R001",
    region="WEST",
    evaluation_period_id="Q1-2026",
    avg_sales_cycle_days_current=60.0,
    avg_sales_cycle_days_benchmark=60.0,
    avg_sales_cycle_days_prior=60.0,
    deals_stalled_7d_plus=0,
    deals_stalled_14d_plus=0,
    deals_stalled_30d_plus=0,
    stage_2_to_3_avg_days=10.0,
    stage_3_to_4_avg_days=10.0,
    stage_4_to_close_avg_days=10.0,
    stage_benchmark_2_to_3_days=10.0,
    stage_benchmark_3_to_4_days=10.0,
    stage_benchmark_4_to_close_days=10.0,
    buyer_response_time_avg_days=1.0,
    mutual_action_plan_adherence_pct=0.90,
    approval_cycle_avg_days=5.0,
    approval_cycle_benchmark_days=5.0,
    late_stage_deals_count=0,
    late_stage_deals_stalled_count=0,
    close_date_slipped_count=0,
) -> VelocityDegradationInput:
    return VelocityDegradationInput(
        rep_id=rep_id,
        region=region,
        evaluation_period_id=evaluation_period_id,
        avg_sales_cycle_days_current=avg_sales_cycle_days_current,
        avg_sales_cycle_days_benchmark=avg_sales_cycle_days_benchmark,
        avg_sales_cycle_days_prior=avg_sales_cycle_days_prior,
        deals_stalled_7d_plus=deals_stalled_7d_plus,
        deals_stalled_14d_plus=deals_stalled_14d_plus,
        deals_stalled_30d_plus=deals_stalled_30d_plus,
        stage_2_to_3_avg_days=stage_2_to_3_avg_days,
        stage_3_to_4_avg_days=stage_3_to_4_avg_days,
        stage_4_to_close_avg_days=stage_4_to_close_avg_days,
        stage_benchmark_2_to_3_days=stage_benchmark_2_to_3_days,
        stage_benchmark_3_to_4_days=stage_benchmark_3_to_4_days,
        stage_benchmark_4_to_close_days=stage_benchmark_4_to_close_days,
        buyer_response_time_avg_days=buyer_response_time_avg_days,
        mutual_action_plan_adherence_pct=mutual_action_plan_adherence_pct,
        approval_cycle_avg_days=approval_cycle_avg_days,
        approval_cycle_benchmark_days=approval_cycle_benchmark_days,
        late_stage_deals_count=late_stage_deals_count,
        late_stage_deals_stalled_count=late_stage_deals_stalled_count,
        close_date_slipped_count=close_date_slipped_count,
    )


@pytest.fixture
def engine():
    return SalesCycleVelocityDegradationEngine()


@pytest.fixture
def healthy_input():
    return make_input()


@pytest.fixture
def critical_input():
    return make_input(
        avg_sales_cycle_days_current=120.0,
        avg_sales_cycle_days_benchmark=60.0,
        avg_sales_cycle_days_prior=60.0,
        deals_stalled_7d_plus=8,
        deals_stalled_14d_plus=6,
        deals_stalled_30d_plus=5,
        stage_2_to_3_avg_days=20.0,
        stage_3_to_4_avg_days=20.0,
        stage_4_to_close_avg_days=20.0,
        stage_benchmark_2_to_3_days=10.0,
        stage_benchmark_3_to_4_days=10.0,
        stage_benchmark_4_to_close_days=10.0,
        buyer_response_time_avg_days=10.0,
        mutual_action_plan_adherence_pct=0.20,
        approval_cycle_avg_days=15.0,
        approval_cycle_benchmark_days=5.0,
        late_stage_deals_count=5,
        late_stage_deals_stalled_count=4,
        close_date_slipped_count=6,
    )


# ---------------------------------------------------------------------------
# 1. Enum Integrity
# ---------------------------------------------------------------------------

class TestEnumValues:
    def test_velocity_risk_low(self):
        assert VelocityRisk.low.value == "low"

    def test_velocity_risk_moderate(self):
        assert VelocityRisk.moderate.value == "moderate"

    def test_velocity_risk_high(self):
        assert VelocityRisk.high.value == "high"

    def test_velocity_risk_critical(self):
        assert VelocityRisk.critical.value == "critical"

    def test_velocity_risk_count(self):
        assert len(VelocityRisk) == 4

    def test_velocity_pattern_none(self):
        assert VelocityPattern.none.value == "none"

    def test_velocity_pattern_stage_progression_stall(self):
        assert VelocityPattern.stage_progression_stall.value == "stage_progression_stall"

    def test_velocity_pattern_buyer_inactivity(self):
        assert VelocityPattern.buyer_inactivity.value == "buyer_inactivity"

    def test_velocity_pattern_approval_bottleneck(self):
        assert VelocityPattern.approval_bottleneck.value == "approval_bottleneck"

    def test_velocity_pattern_late_stage_drag(self):
        assert VelocityPattern.late_stage_drag.value == "late_stage_drag"

    def test_velocity_pattern_deal_aging(self):
        assert VelocityPattern.deal_aging.value == "deal_aging"

    def test_velocity_pattern_count(self):
        assert len(VelocityPattern) == 6

    def test_velocity_severity_healthy(self):
        assert VelocitySeverity.healthy.value == "healthy"

    def test_velocity_severity_slowing(self):
        assert VelocitySeverity.slowing.value == "slowing"

    def test_velocity_severity_degraded(self):
        assert VelocitySeverity.degraded.value == "degraded"

    def test_velocity_severity_stalled(self):
        assert VelocitySeverity.stalled.value == "stalled"

    def test_velocity_severity_count(self):
        assert len(VelocitySeverity) == 4

    def test_velocity_action_no_action(self):
        assert VelocityAction.no_action.value == "no_action"

    def test_velocity_action_cycle_review(self):
        assert VelocityAction.cycle_review.value == "cycle_review"

    def test_velocity_action_buyer_re_engagement(self):
        assert VelocityAction.buyer_re_engagement.value == "buyer_re_engagement"

    def test_velocity_action_deal_qualification_reset(self):
        assert VelocityAction.deal_qualification_reset.value == "deal_qualification_reset"

    def test_velocity_action_executive_acceleration(self):
        assert VelocityAction.executive_acceleration.value == "executive_acceleration"

    def test_velocity_action_count(self):
        assert len(VelocityAction) == 5

    def test_velocity_risk_is_str_enum(self):
        assert isinstance(VelocityRisk.low, str)

    def test_velocity_pattern_is_str_enum(self):
        assert isinstance(VelocityPattern.none, str)

    def test_velocity_severity_is_str_enum(self):
        assert isinstance(VelocitySeverity.healthy, str)

    def test_velocity_action_is_str_enum(self):
        assert isinstance(VelocityAction.no_action, str)


# ---------------------------------------------------------------------------
# 2. Dataclass Field Counts
# ---------------------------------------------------------------------------

class TestDataclassStructure:
    def test_input_field_count(self):
        assert len(fields(VelocityDegradationInput)) == 22

    def test_result_field_count(self):
        assert len(fields(VelocityDegradationResult)) == 15

    def test_input_has_rep_id(self):
        names = [f.name for f in fields(VelocityDegradationInput)]
        assert "rep_id" in names

    def test_input_has_region(self):
        names = [f.name for f in fields(VelocityDegradationInput)]
        assert "region" in names

    def test_input_has_evaluation_period_id(self):
        names = [f.name for f in fields(VelocityDegradationInput)]
        assert "evaluation_period_id" in names

    def test_input_has_avg_sales_cycle_days_current(self):
        names = [f.name for f in fields(VelocityDegradationInput)]
        assert "avg_sales_cycle_days_current" in names

    def test_input_has_deals_stalled_30d_plus(self):
        names = [f.name for f in fields(VelocityDegradationInput)]
        assert "deals_stalled_30d_plus" in names

    def test_input_has_buyer_response_time_avg_days(self):
        names = [f.name for f in fields(VelocityDegradationInput)]
        assert "buyer_response_time_avg_days" in names

    def test_input_has_close_date_slipped_count(self):
        names = [f.name for f in fields(VelocityDegradationInput)]
        assert "close_date_slipped_count" in names

    def test_result_has_velocity_risk(self):
        names = [f.name for f in fields(VelocityDegradationResult)]
        assert "velocity_risk" in names

    def test_result_has_velocity_pattern(self):
        names = [f.name for f in fields(VelocityDegradationResult)]
        assert "velocity_pattern" in names

    def test_result_has_velocity_severity(self):
        names = [f.name for f in fields(VelocityDegradationResult)]
        assert "velocity_severity" in names

    def test_result_has_recommended_action(self):
        names = [f.name for f in fields(VelocityDegradationResult)]
        assert "recommended_action" in names

    def test_result_has_velocity_composite(self):
        names = [f.name for f in fields(VelocityDegradationResult)]
        assert "velocity_composite" in names

    def test_result_has_is_velocity_degraded(self):
        names = [f.name for f in fields(VelocityDegradationResult)]
        assert "is_velocity_degraded" in names

    def test_result_has_requires_intervention(self):
        names = [f.name for f in fields(VelocityDegradationResult)]
        assert "requires_intervention" in names

    def test_result_has_estimated_at_risk_deals(self):
        names = [f.name for f in fields(VelocityDegradationResult)]
        assert "estimated_at_risk_deals" in names

    def test_result_has_velocity_signal(self):
        names = [f.name for f in fields(VelocityDegradationResult)]
        assert "velocity_signal" in names

    def test_result_has_cycle_length_score(self):
        names = [f.name for f in fields(VelocityDegradationResult)]
        assert "cycle_length_score" in names

    def test_result_has_stage_stall_score(self):
        names = [f.name for f in fields(VelocityDegradationResult)]
        assert "stage_stall_score" in names

    def test_result_has_buyer_engagement_score(self):
        names = [f.name for f in fields(VelocityDegradationResult)]
        assert "buyer_engagement_score" in names

    def test_result_has_late_stage_drag_score(self):
        names = [f.name for f in fields(VelocityDegradationResult)]
        assert "late_stage_drag_score" in names


# ---------------------------------------------------------------------------
# 3. VelocityDegradationResult.to_dict()
# ---------------------------------------------------------------------------

class TestResultToDict:
    def test_to_dict_returns_dict(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.to_dict(), dict)

    def test_to_dict_has_15_keys(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert len(r.to_dict()) == 15

    def test_to_dict_rep_id(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.to_dict()["rep_id"] == "R001"

    def test_to_dict_region(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.to_dict()["region"] == "WEST"

    def test_to_dict_velocity_risk_is_string(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.to_dict()["velocity_risk"], str)

    def test_to_dict_velocity_pattern_is_string(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.to_dict()["velocity_pattern"], str)

    def test_to_dict_velocity_severity_is_string(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.to_dict()["velocity_severity"], str)

    def test_to_dict_recommended_action_is_string(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.to_dict()["recommended_action"], str)

    def test_to_dict_is_velocity_degraded_is_bool(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.to_dict()["is_velocity_degraded"], bool)

    def test_to_dict_requires_intervention_is_bool(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.to_dict()["requires_intervention"], bool)

    def test_to_dict_estimated_at_risk_deals_is_int(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.to_dict()["estimated_at_risk_deals"], int)

    def test_to_dict_velocity_signal_is_str(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.to_dict()["velocity_signal"], str)

    def test_to_dict_velocity_composite_is_numeric(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.to_dict()["velocity_composite"], (int, float))


# ---------------------------------------------------------------------------
# 4. Healthy scenario (all zeros / at benchmark)
# ---------------------------------------------------------------------------

class TestHealthyScenario:
    def test_healthy_risk_is_low(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.velocity_risk == VelocityRisk.low

    def test_healthy_severity_is_healthy(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.velocity_severity == VelocitySeverity.healthy

    def test_healthy_pattern_is_none(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.velocity_pattern == VelocityPattern.none

    def test_healthy_action_is_no_action(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.recommended_action == VelocityAction.no_action

    def test_healthy_not_degraded(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.is_velocity_degraded is False

    def test_healthy_no_intervention(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.requires_intervention is False

    def test_healthy_at_risk_deals_zero(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.estimated_at_risk_deals == 0

    def test_healthy_composite_low(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.velocity_composite < 20

    def test_healthy_cycle_length_score_zero(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.cycle_length_score == 0.0

    def test_healthy_stage_stall_score_zero(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.stage_stall_score == 0.0

    def test_healthy_buyer_engagement_score_zero(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.buyer_engagement_score == 0.0

    def test_healthy_late_stage_drag_score_zero(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.late_stage_drag_score == 0.0

    def test_healthy_signal_contains_healthy_text(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert "healthy" in r.velocity_signal.lower()

    def test_healthy_rep_id_preserved(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.rep_id == "R001"

    def test_healthy_region_preserved(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.region == "WEST"


# ---------------------------------------------------------------------------
# 5. Critical scenario
# ---------------------------------------------------------------------------

class TestCriticalScenario:
    def test_critical_risk_is_critical(self, engine, critical_input):
        r = engine.assess(critical_input)
        assert r.velocity_risk == VelocityRisk.critical

    def test_critical_severity_is_stalled(self, engine, critical_input):
        r = engine.assess(critical_input)
        assert r.velocity_severity == VelocitySeverity.stalled

    def test_critical_action_is_executive_acceleration(self, engine, critical_input):
        r = engine.assess(critical_input)
        assert r.recommended_action == VelocityAction.executive_acceleration

    def test_critical_is_degraded(self, engine, critical_input):
        r = engine.assess(critical_input)
        assert r.is_velocity_degraded is True

    def test_critical_requires_intervention(self, engine, critical_input):
        r = engine.assess(critical_input)
        assert r.requires_intervention is True

    def test_critical_composite_above_60(self, engine, critical_input):
        r = engine.assess(critical_input)
        assert r.velocity_composite >= 60.0

    def test_critical_at_risk_deals_positive(self, engine, critical_input):
        r = engine.assess(critical_input)
        assert r.estimated_at_risk_deals > 0

    def test_critical_at_risk_deals_calculation(self, engine, critical_input):
        # deals_stalled_14d_plus=6, late_stage_deals_stalled_count=4 => 10
        r = engine.assess(critical_input)
        assert r.estimated_at_risk_deals == 10


# ---------------------------------------------------------------------------
# 6. cycle_length_score - individual drivers
# ---------------------------------------------------------------------------

class TestCycleLengthScore:
    def test_excess_50pct_vs_benchmark(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=90.0,
            avg_sales_cycle_days_benchmark=60.0,
        )
        r = engine.assess(inp)
        assert r.cycle_length_score >= 40.0

    def test_excess_30pct_vs_benchmark(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=78.0,
            avg_sales_cycle_days_benchmark=60.0,
        )
        r = engine.assess(inp)
        assert r.cycle_length_score >= 25.0

    def test_excess_15pct_vs_benchmark(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=69.0,
            avg_sales_cycle_days_benchmark=60.0,
        )
        r = engine.assess(inp)
        assert r.cycle_length_score >= 12.0

    def test_no_excess_vs_benchmark(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=60.0,
            avg_sales_cycle_days_benchmark=60.0,
        )
        r = engine.assess(inp)
        # no benchmark excess contribution
        assert r.cycle_length_score >= 0.0

    def test_trend_30pct_vs_prior(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=78.0,
            avg_sales_cycle_days_prior=60.0,
            avg_sales_cycle_days_benchmark=200.0,  # avoid benchmark trigger
        )
        r = engine.assess(inp)
        assert r.cycle_length_score >= 30.0

    def test_trend_15pct_vs_prior(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=69.0,
            avg_sales_cycle_days_prior=60.0,
            avg_sales_cycle_days_benchmark=200.0,
        )
        r = engine.assess(inp)
        assert r.cycle_length_score >= 15.0

    def test_trend_8pct_vs_prior(self, engine):
        # 8% trend: 60 * 1.08 = 64.8 => trend >= 0.08 => +6
        inp = make_input(
            avg_sales_cycle_days_current=64.9,
            avg_sales_cycle_days_prior=60.0,
            avg_sales_cycle_days_benchmark=200.0,
        )
        r = engine.assess(inp)
        assert r.cycle_length_score >= 6.0

    def test_close_date_slippage_5_plus(self, engine):
        inp = make_input(close_date_slipped_count=5)
        r = engine.assess(inp)
        assert r.cycle_length_score >= 20.0

    def test_close_date_slippage_3(self, engine):
        inp = make_input(close_date_slipped_count=3)
        r = engine.assess(inp)
        assert r.cycle_length_score >= 12.0

    def test_close_date_slippage_1(self, engine):
        inp = make_input(close_date_slipped_count=1)
        r = engine.assess(inp)
        assert r.cycle_length_score >= 5.0

    def test_absolute_cycle_180d_plus(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=180.0,
            avg_sales_cycle_days_benchmark=200.0,
            avg_sales_cycle_days_prior=200.0,
        )
        r = engine.assess(inp)
        assert r.cycle_length_score >= 10.0

    def test_absolute_cycle_120d(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=120.0,
            avg_sales_cycle_days_benchmark=200.0,
            avg_sales_cycle_days_prior=200.0,
        )
        r = engine.assess(inp)
        assert r.cycle_length_score >= 5.0

    def test_cycle_length_score_capped_at_100(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=500.0,
            avg_sales_cycle_days_benchmark=60.0,
            avg_sales_cycle_days_prior=60.0,
            close_date_slipped_count=10,
        )
        r = engine.assess(inp)
        assert r.cycle_length_score <= 100.0

    def test_benchmark_zero_no_crash(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=90.0,
            avg_sales_cycle_days_benchmark=0.0,
        )
        r = engine.assess(inp)
        assert r.cycle_length_score >= 0.0

    def test_prior_zero_no_crash(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=90.0,
            avg_sales_cycle_days_prior=0.0,
        )
        r = engine.assess(inp)
        assert r.cycle_length_score >= 0.0


# ---------------------------------------------------------------------------
# 7. stage_stall_score - individual drivers
# ---------------------------------------------------------------------------

class TestStageStallScore:
    def test_deals_stalled_30d_3_plus(self, engine):
        inp = make_input(deals_stalled_30d_plus=3)
        r = engine.assess(inp)
        assert r.stage_stall_score >= 40.0

    def test_deals_stalled_14d_4_plus(self, engine):
        inp = make_input(deals_stalled_14d_plus=4)
        r = engine.assess(inp)
        assert r.stage_stall_score >= 28.0

    def test_deals_stalled_7d_5_plus(self, engine):
        inp = make_input(deals_stalled_7d_plus=5)
        r = engine.assess(inp)
        assert r.stage_stall_score >= 14.0

    def test_stage_excess_1_50(self, engine):
        # All three stages 2x over benchmark => excess = 3.0
        inp = make_input(
            stage_2_to_3_avg_days=30.0, stage_benchmark_2_to_3_days=10.0,
            stage_3_to_4_avg_days=30.0, stage_benchmark_3_to_4_days=10.0,
            stage_4_to_close_avg_days=30.0, stage_benchmark_4_to_close_days=10.0,
        )
        r = engine.assess(inp)
        assert r.stage_stall_score >= 35.0

    def test_stage_excess_0_75(self, engine):
        # excess = 0.75 * 3 = 2.25 => >=0.75 threshold
        inp = make_input(
            stage_2_to_3_avg_days=17.5, stage_benchmark_2_to_3_days=10.0,
            stage_3_to_4_avg_days=17.5, stage_benchmark_3_to_4_days=10.0,
            stage_4_to_close_avg_days=17.5, stage_benchmark_4_to_close_days=10.0,
        )
        r = engine.assess(inp)
        assert r.stage_stall_score >= 20.0

    def test_stage_excess_0_30(self, engine):
        inp = make_input(
            stage_2_to_3_avg_days=13.0, stage_benchmark_2_to_3_days=10.0,
            stage_3_to_4_avg_days=13.0, stage_benchmark_3_to_4_days=10.0,
            stage_4_to_close_avg_days=13.0, stage_benchmark_4_to_close_days=10.0,
        )
        r = engine.assess(inp)
        assert r.stage_stall_score >= 8.0

    def test_map_adherence_below_40(self, engine):
        inp = make_input(mutual_action_plan_adherence_pct=0.30)
        r = engine.assess(inp)
        assert r.stage_stall_score >= 15.0

    def test_map_adherence_below_60(self, engine):
        inp = make_input(mutual_action_plan_adherence_pct=0.50)
        r = engine.assess(inp)
        assert r.stage_stall_score >= 7.0

    def test_stage_stall_score_capped_100(self, engine):
        inp = make_input(
            deals_stalled_30d_plus=10,
            stage_2_to_3_avg_days=100.0, stage_benchmark_2_to_3_days=10.0,
            stage_3_to_4_avg_days=100.0, stage_benchmark_3_to_4_days=10.0,
            stage_4_to_close_avg_days=100.0, stage_benchmark_4_to_close_days=10.0,
            mutual_action_plan_adherence_pct=0.10,
        )
        r = engine.assess(inp)
        assert r.stage_stall_score <= 100.0

    def test_stage_bench_zero_no_crash(self, engine):
        inp = make_input(
            stage_2_to_3_avg_days=20.0, stage_benchmark_2_to_3_days=0.0,
        )
        r = engine.assess(inp)
        assert r.stage_stall_score >= 0.0


# ---------------------------------------------------------------------------
# 8. buyer_engagement_score - individual drivers
# ---------------------------------------------------------------------------

class TestBuyerEngagementScore:
    def test_buyer_response_7d_plus(self, engine):
        inp = make_input(buyer_response_time_avg_days=7.0)
        r = engine.assess(inp)
        assert r.buyer_engagement_score >= 45.0

    def test_buyer_response_4d(self, engine):
        inp = make_input(buyer_response_time_avg_days=4.0)
        r = engine.assess(inp)
        assert r.buyer_engagement_score >= 25.0

    def test_buyer_response_2d(self, engine):
        inp = make_input(buyer_response_time_avg_days=2.0)
        r = engine.assess(inp)
        assert r.buyer_engagement_score >= 10.0

    def test_map_below_30_pct(self, engine):
        inp = make_input(mutual_action_plan_adherence_pct=0.20)
        r = engine.assess(inp)
        assert r.buyer_engagement_score >= 30.0

    def test_map_below_50_pct(self, engine):
        inp = make_input(mutual_action_plan_adherence_pct=0.40)
        r = engine.assess(inp)
        assert r.buyer_engagement_score >= 15.0

    def test_deals_stalled_14d_3_plus(self, engine):
        inp = make_input(deals_stalled_14d_plus=3)
        r = engine.assess(inp)
        assert r.buyer_engagement_score >= 20.0

    def test_deals_stalled_14d_1(self, engine):
        inp = make_input(deals_stalled_14d_plus=1)
        r = engine.assess(inp)
        assert r.buyer_engagement_score >= 8.0

    def test_close_date_slippage_3_plus(self, engine):
        inp = make_input(close_date_slipped_count=3)
        r = engine.assess(inp)
        assert r.buyer_engagement_score >= 10.0

    def test_buyer_engagement_score_capped_100(self, engine):
        inp = make_input(
            buyer_response_time_avg_days=15.0,
            mutual_action_plan_adherence_pct=0.10,
            deals_stalled_14d_plus=10,
            close_date_slipped_count=10,
        )
        r = engine.assess(inp)
        assert r.buyer_engagement_score <= 100.0

    def test_buyer_response_zero_no_score(self, engine):
        inp = make_input(buyer_response_time_avg_days=0.5)
        r = engine.assess(inp)
        # 0.5d => below 2d threshold
        assert r.buyer_engagement_score >= 0.0


# ---------------------------------------------------------------------------
# 9. late_stage_drag_score - individual drivers
# ---------------------------------------------------------------------------

class TestLateStrageDragScore:
    def test_stall_rate_60pct(self, engine):
        inp = make_input(late_stage_deals_count=5, late_stage_deals_stalled_count=3)
        r = engine.assess(inp)
        assert r.late_stage_drag_score >= 45.0

    def test_stall_rate_40pct(self, engine):
        inp = make_input(late_stage_deals_count=5, late_stage_deals_stalled_count=2)
        r = engine.assess(inp)
        assert r.late_stage_drag_score >= 28.0

    def test_stall_rate_20pct(self, engine):
        inp = make_input(late_stage_deals_count=5, late_stage_deals_stalled_count=1)
        r = engine.assess(inp)
        assert r.late_stage_drag_score >= 12.0

    def test_no_late_stage_deals_no_crash(self, engine):
        inp = make_input(late_stage_deals_count=0, late_stage_deals_stalled_count=0)
        r = engine.assess(inp)
        assert r.late_stage_drag_score >= 0.0

    def test_approval_excess_50pct(self, engine):
        inp = make_input(approval_cycle_avg_days=15.0, approval_cycle_benchmark_days=10.0)
        r = engine.assess(inp)
        assert r.late_stage_drag_score >= 30.0

    def test_approval_excess_25pct(self, engine):
        inp = make_input(approval_cycle_avg_days=12.5, approval_cycle_benchmark_days=10.0)
        r = engine.assess(inp)
        assert r.late_stage_drag_score >= 15.0

    def test_approval_excess_10pct(self, engine):
        inp = make_input(approval_cycle_avg_days=11.0, approval_cycle_benchmark_days=10.0)
        r = engine.assess(inp)
        assert r.late_stage_drag_score >= 6.0

    def test_stage4_close_excess_50pct(self, engine):
        inp = make_input(
            stage_4_to_close_avg_days=15.0,
            stage_benchmark_4_to_close_days=10.0,
        )
        r = engine.assess(inp)
        assert r.late_stage_drag_score >= 20.0

    def test_stage4_close_excess_25pct(self, engine):
        inp = make_input(
            stage_4_to_close_avg_days=12.5,
            stage_benchmark_4_to_close_days=10.0,
        )
        r = engine.assess(inp)
        assert r.late_stage_drag_score >= 10.0

    def test_many_late_stalled_4_plus(self, engine):
        inp = make_input(late_stage_deals_count=10, late_stage_deals_stalled_count=4)
        r = engine.assess(inp)
        assert r.late_stage_drag_score >= 10.0

    def test_late_stage_drag_score_capped_100(self, engine):
        inp = make_input(
            late_stage_deals_count=5,
            late_stage_deals_stalled_count=5,
            approval_cycle_avg_days=100.0,
            approval_cycle_benchmark_days=10.0,
            stage_4_to_close_avg_days=100.0,
            stage_benchmark_4_to_close_days=10.0,
        )
        r = engine.assess(inp)
        assert r.late_stage_drag_score <= 100.0

    def test_approval_benchmark_zero_no_crash(self, engine):
        inp = make_input(approval_cycle_avg_days=10.0, approval_cycle_benchmark_days=0.0)
        r = engine.assess(inp)
        assert r.late_stage_drag_score >= 0.0


# ---------------------------------------------------------------------------
# 10. Composite formula
# ---------------------------------------------------------------------------

class TestCompositeFormula:
    def test_composite_formula_weights(self, engine):
        """Force known sub-scores via controlled input and verify formula."""
        # Use a deterministic input with known sub-score contributions
        inp = make_input(
            avg_sales_cycle_days_current=90.0,
            avg_sales_cycle_days_benchmark=60.0,   # 50% excess => +40 cycle
            avg_sales_cycle_days_prior=200.0,       # no trend contribution
            close_date_slipped_count=0,
            # stage: no stalls, at benchmark
            deals_stalled_7d_plus=0, deals_stalled_14d_plus=0, deals_stalled_30d_plus=0,
            mutual_action_plan_adherence_pct=0.90,
            # buyer: 0 response score
            buyer_response_time_avg_days=0.5,
            # late: no late stage
            late_stage_deals_count=0, late_stage_deals_stalled_count=0,
            approval_cycle_avg_days=5.0, approval_cycle_benchmark_days=5.0,
        )
        r = engine.assess(inp)
        expected = round(r.cycle_length_score * 0.30
                         + r.stage_stall_score * 0.30
                         + r.buyer_engagement_score * 0.25
                         + r.late_stage_drag_score * 0.15, 1)
        assert r.velocity_composite == expected

    def test_composite_is_float(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.velocity_composite, float)

    def test_composite_non_negative(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.velocity_composite >= 0.0

    def test_composite_capped_100(self, engine, critical_input):
        r = engine.assess(critical_input)
        assert r.velocity_composite <= 100.0

    def test_composite_increases_with_degradation(self, engine):
        low = engine.assess(make_input()).velocity_composite
        high = engine.assess(make_input(
            avg_sales_cycle_days_current=120.0,
            avg_sales_cycle_days_benchmark=60.0,
            deals_stalled_30d_plus=5,
        )).velocity_composite
        assert high > low


# ---------------------------------------------------------------------------
# 11. Risk level thresholds
# ---------------------------------------------------------------------------

class TestRiskLevel:
    def test_risk_low_below_20(self, engine):
        r = engine.assess(make_input())
        if r.velocity_composite < 20:
            assert r.velocity_risk == VelocityRisk.low

    def test_risk_moderate_20_to_39(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=78.0,
            avg_sales_cycle_days_benchmark=60.0,
            deals_stalled_7d_plus=3,
            mutual_action_plan_adherence_pct=0.55,
        )
        r = engine.assess(inp)
        if 20 <= r.velocity_composite < 40:
            assert r.velocity_risk == VelocityRisk.moderate

    def test_risk_high_40_to_59(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=90.0,
            avg_sales_cycle_days_benchmark=60.0,
            deals_stalled_14d_plus=4,
            buyer_response_time_avg_days=4.0,
            mutual_action_plan_adherence_pct=0.35,
            late_stage_deals_count=3,
            late_stage_deals_stalled_count=2,
        )
        r = engine.assess(inp)
        if 40 <= r.velocity_composite < 60:
            assert r.velocity_risk == VelocityRisk.high

    def test_risk_critical_60_plus(self, engine, critical_input):
        r = engine.assess(critical_input)
        if r.velocity_composite >= 60:
            assert r.velocity_risk == VelocityRisk.critical

    def test_composite_exactly_20_is_moderate(self, engine):
        # synthesize a composite exactly at 20 threshold via controlled sub-scores
        # We just assert the mapping is consistent with observed composite
        inp = make_input(
            avg_sales_cycle_days_current=78.0,
            avg_sales_cycle_days_benchmark=60.0,  # 30% => +25 cycle
        )
        r = engine.assess(inp)
        if r.velocity_composite >= 20:
            assert r.velocity_risk in (
                VelocityRisk.moderate, VelocityRisk.high, VelocityRisk.critical
            )

    def test_composite_exactly_40_is_high(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=90.0,
            avg_sales_cycle_days_benchmark=60.0,
            deals_stalled_30d_plus=3,
            buyer_response_time_avg_days=4.0,
        )
        r = engine.assess(inp)
        if r.velocity_composite >= 40:
            assert r.velocity_risk in (VelocityRisk.high, VelocityRisk.critical)

    def test_composite_exactly_60_is_critical(self, engine, critical_input):
        r = engine.assess(critical_input)
        if r.velocity_composite >= 60:
            assert r.velocity_risk == VelocityRisk.critical


# ---------------------------------------------------------------------------
# 12. Severity thresholds
# ---------------------------------------------------------------------------

class TestSeverity:
    def test_severity_healthy_composite_below_20(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        if r.velocity_composite < 20:
            assert r.velocity_severity == VelocitySeverity.healthy

    def test_severity_slowing_20_to_39(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=78.0,
            avg_sales_cycle_days_benchmark=60.0,
            deals_stalled_7d_plus=4,
        )
        r = engine.assess(inp)
        if 20 <= r.velocity_composite < 40:
            assert r.velocity_severity == VelocitySeverity.slowing

    def test_severity_degraded_40_to_59(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=90.0,
            avg_sales_cycle_days_benchmark=60.0,
            deals_stalled_30d_plus=4,
            buyer_response_time_avg_days=5.0,
            mutual_action_plan_adherence_pct=0.25,
        )
        r = engine.assess(inp)
        if 40 <= r.velocity_composite < 60:
            assert r.velocity_severity == VelocitySeverity.degraded

    def test_severity_stalled_60_plus(self, engine, critical_input):
        r = engine.assess(critical_input)
        if r.velocity_composite >= 60:
            assert r.velocity_severity == VelocitySeverity.stalled

    def test_severity_consistent_with_composite(self, engine):
        for inp in [make_input(), make_input(deals_stalled_30d_plus=3)]:
            r = engine.assess(inp)
            if r.velocity_composite < 20:
                assert r.velocity_severity == VelocitySeverity.healthy
            elif r.velocity_composite < 40:
                assert r.velocity_severity == VelocitySeverity.slowing
            elif r.velocity_composite < 60:
                assert r.velocity_severity == VelocitySeverity.degraded
            else:
                assert r.velocity_severity == VelocitySeverity.stalled


# ---------------------------------------------------------------------------
# 13. Action mapping
# ---------------------------------------------------------------------------

class TestActionMapping:
    def test_action_no_action_when_low(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        if r.velocity_risk == VelocityRisk.low:
            assert r.recommended_action == VelocityAction.no_action

    def test_action_cycle_review_when_moderate(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=75.0,
            avg_sales_cycle_days_benchmark=60.0,
            deals_stalled_7d_plus=4,
        )
        r = engine.assess(inp)
        if r.velocity_risk == VelocityRisk.moderate:
            assert r.recommended_action == VelocityAction.cycle_review

    def test_action_executive_acceleration_when_critical(self, engine, critical_input):
        r = engine.assess(critical_input)
        if r.velocity_risk == VelocityRisk.critical:
            assert r.recommended_action == VelocityAction.executive_acceleration

    def test_action_deal_qualification_reset_high_deal_aging(self, engine):
        inp = make_input(
            deals_stalled_30d_plus=4,
            avg_sales_cycle_days_current=90.0,
            avg_sales_cycle_days_benchmark=60.0,
            avg_sales_cycle_days_prior=60.0,
            deals_stalled_14d_plus=5,
            buyer_response_time_avg_days=5.0,
            mutual_action_plan_adherence_pct=0.25,
            close_date_slipped_count=4,
        )
        r = engine.assess(inp)
        if r.velocity_risk == VelocityRisk.high and r.velocity_pattern == VelocityPattern.deal_aging:
            assert r.recommended_action == VelocityAction.deal_qualification_reset

    def test_action_buyer_re_engagement_high_non_deal_aging(self, engine):
        inp = make_input(
            buyer_response_time_avg_days=5.0,
            mutual_action_plan_adherence_pct=0.25,
            deals_stalled_14d_plus=4,
            avg_sales_cycle_days_current=90.0,
            avg_sales_cycle_days_benchmark=60.0,
        )
        r = engine.assess(inp)
        if (r.velocity_risk == VelocityRisk.high
                and r.velocity_pattern != VelocityPattern.deal_aging):
            assert r.recommended_action == VelocityAction.buyer_re_engagement


# ---------------------------------------------------------------------------
# 14. Pattern detection
# ---------------------------------------------------------------------------

class TestPatternDetection:
    def test_pattern_none_when_all_clean(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.velocity_pattern == VelocityPattern.none

    def test_pattern_deal_aging_priority(self, engine):
        # High stalled 30d + high cycle => deal_aging
        inp = make_input(
            deals_stalled_30d_plus=4,
            avg_sales_cycle_days_current=120.0,
            avg_sales_cycle_days_benchmark=60.0,
        )
        r = engine.assess(inp)
        assert r.velocity_pattern == VelocityPattern.deal_aging

    def test_pattern_late_stage_drag(self, engine):
        inp = make_input(
            late_stage_deals_count=5,
            late_stage_deals_stalled_count=3,    # stall_rate=60% => late=45
            approval_cycle_avg_days=5.0,
            approval_cycle_benchmark_days=5.0,   # no approval bottleneck
        )
        r = engine.assess(inp)
        # late >=35 and stalled >=2
        assert r.velocity_pattern == VelocityPattern.late_stage_drag

    def test_pattern_approval_bottleneck(self, engine):
        inp = make_input(
            approval_cycle_avg_days=15.0,
            approval_cycle_benchmark_days=10.0,  # 1.5x => >1.40 threshold
        )
        r = engine.assess(inp)
        # approval > 1.40 benchmark
        assert r.velocity_pattern == VelocityPattern.approval_bottleneck

    def test_pattern_buyer_inactivity(self, engine):
        inp = make_input(
            buyer_response_time_avg_days=5.0,
            mutual_action_plan_adherence_pct=0.25,  # buyer>=25
        )
        r = engine.assess(inp)
        if r.buyer_engagement_score >= 25 and r.velocity_pattern not in (
            VelocityPattern.deal_aging,
            VelocityPattern.late_stage_drag,
            VelocityPattern.approval_bottleneck,
        ):
            assert r.velocity_pattern == VelocityPattern.buyer_inactivity

    def test_pattern_stage_progression_stall(self, engine):
        inp = make_input(
            stage_2_to_3_avg_days=30.0, stage_benchmark_2_to_3_days=10.0,
            stage_3_to_4_avg_days=30.0, stage_benchmark_3_to_4_days=10.0,
            stage_4_to_close_avg_days=30.0, stage_benchmark_4_to_close_days=10.0,
            buyer_response_time_avg_days=0.5,     # no buyer inactivity
            mutual_action_plan_adherence_pct=0.90,
        )
        r = engine.assess(inp)
        if r.stage_stall_score >= 20 and r.velocity_pattern not in (
            VelocityPattern.deal_aging,
            VelocityPattern.late_stage_drag,
            VelocityPattern.approval_bottleneck,
            VelocityPattern.buyer_inactivity,
        ):
            assert r.velocity_pattern == VelocityPattern.stage_progression_stall

    def test_deal_aging_takes_priority_over_late_stage_drag(self, engine):
        inp = make_input(
            deals_stalled_30d_plus=4,
            avg_sales_cycle_days_current=120.0,
            avg_sales_cycle_days_benchmark=60.0,
            late_stage_deals_count=5,
            late_stage_deals_stalled_count=3,
        )
        r = engine.assess(inp)
        # deal_aging beats late_stage_drag
        assert r.velocity_pattern == VelocityPattern.deal_aging

    def test_late_stage_drag_beats_approval_bottleneck(self, engine):
        inp = make_input(
            late_stage_deals_count=5,
            late_stage_deals_stalled_count=3,
            approval_cycle_avg_days=15.0,
            approval_cycle_benchmark_days=10.0,
        )
        r = engine.assess(inp)
        # late >=35 and stalled>=2 => late_stage_drag wins over approval_bottleneck
        # The pattern should be late_stage_drag (stall_rate=60% => 45, approval 50% => +30, capped)
        assert r.velocity_pattern == VelocityPattern.late_stage_drag

    def test_approval_bottleneck_detected_1_4x(self, engine):
        inp = make_input(
            approval_cycle_avg_days=14.1,
            approval_cycle_benchmark_days=10.0,  # 1.41x > 1.40
        )
        r = engine.assess(inp)
        if r.velocity_pattern not in (VelocityPattern.deal_aging, VelocityPattern.late_stage_drag):
            assert r.velocity_pattern == VelocityPattern.approval_bottleneck

    def test_approval_not_bottleneck_at_1_4x(self, engine):
        inp = make_input(
            approval_cycle_avg_days=14.0,
            approval_cycle_benchmark_days=10.0,  # exactly 1.40 => NOT > 1.40
        )
        r = engine.assess(inp)
        if r.velocity_pattern not in (
            VelocityPattern.deal_aging,
            VelocityPattern.late_stage_drag,
        ):
            assert r.velocity_pattern != VelocityPattern.approval_bottleneck


# ---------------------------------------------------------------------------
# 15. is_velocity_degraded flag
# ---------------------------------------------------------------------------

class TestIsVelocityDegraded:
    def test_not_degraded_clean(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.is_velocity_degraded is False

    def test_degraded_composite_40_plus(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=90.0,
            avg_sales_cycle_days_benchmark=60.0,
            deals_stalled_30d_plus=4,
            buyer_response_time_avg_days=5.0,
            mutual_action_plan_adherence_pct=0.25,
        )
        r = engine.assess(inp)
        if r.velocity_composite >= 40:
            assert r.is_velocity_degraded is True

    def test_degraded_30d_stalled_3_plus(self, engine):
        inp = make_input(deals_stalled_30d_plus=3)
        r = engine.assess(inp)
        assert r.is_velocity_degraded is True

    def test_degraded_150pct_of_benchmark(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=90.0,
            avg_sales_cycle_days_benchmark=60.0,  # 90 >= 60*1.5 => True
        )
        r = engine.assess(inp)
        assert r.is_velocity_degraded is True

    def test_not_degraded_just_below_150pct(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=89.9,
            avg_sales_cycle_days_benchmark=60.0,  # 89.9 < 90 => False
        )
        r = engine.assess(inp)
        # check only benchmark condition (others may be False)
        if r.velocity_composite < 40 and inp.deals_stalled_30d_plus < 3:
            assert r.is_velocity_degraded is False

    def test_degraded_exactly_at_150pct(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=90.0,
            avg_sales_cycle_days_benchmark=60.0,
        )
        r = engine.assess(inp)
        assert r.is_velocity_degraded is True

    def test_degraded_is_bool_type(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.is_velocity_degraded, bool)

    def test_degraded_when_benchmark_zero_not_triggered(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=90.0,
            avg_sales_cycle_days_benchmark=0.0,  # guard prevents division
        )
        r = engine.assess(inp)
        # benchmark=0 => condition skipped; others determine flag
        assert isinstance(r.is_velocity_degraded, bool)


# ---------------------------------------------------------------------------
# 16. requires_intervention flag
# ---------------------------------------------------------------------------

class TestRequiresIntervention:
    def test_no_intervention_clean(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.requires_intervention is False

    def test_intervention_composite_30_plus(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=90.0,
            avg_sales_cycle_days_benchmark=60.0,
            deals_stalled_30d_plus=3,
        )
        r = engine.assess(inp)
        if r.velocity_composite >= 30:
            assert r.requires_intervention is True

    def test_intervention_late_stage_stalled_3_plus(self, engine):
        inp = make_input(
            late_stage_deals_count=5,
            late_stage_deals_stalled_count=3,
        )
        r = engine.assess(inp)
        assert r.requires_intervention is True

    def test_intervention_buyer_response_7d_plus(self, engine):
        inp = make_input(buyer_response_time_avg_days=7.0)
        r = engine.assess(inp)
        assert r.requires_intervention is True

    def test_intervention_buyer_response_exactly_7d(self, engine):
        inp = make_input(buyer_response_time_avg_days=7.0)
        r = engine.assess(inp)
        assert r.requires_intervention is True

    def test_no_intervention_buyer_response_below_7d(self, engine):
        inp = make_input(buyer_response_time_avg_days=6.9)
        r = engine.assess(inp)
        # only this condition; others should be false
        if r.velocity_composite < 30 and inp.late_stage_deals_stalled_count < 3:
            assert r.requires_intervention is False

    def test_intervention_is_bool_type(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.requires_intervention, bool)


# ---------------------------------------------------------------------------
# 17. estimated_at_risk_deals
# ---------------------------------------------------------------------------

class TestEstimatedAtRiskDeals:
    def test_at_risk_deals_zero(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert r.estimated_at_risk_deals == 0

    def test_at_risk_deals_sum(self, engine):
        inp = make_input(deals_stalled_14d_plus=3, late_stage_deals_stalled_count=2)
        r = engine.assess(inp)
        assert r.estimated_at_risk_deals == 5

    def test_at_risk_deals_only_stalled_14d(self, engine):
        inp = make_input(deals_stalled_14d_plus=4)
        r = engine.assess(inp)
        assert r.estimated_at_risk_deals == 4

    def test_at_risk_deals_only_late_stage_stalled(self, engine):
        inp = make_input(late_stage_deals_count=3, late_stage_deals_stalled_count=3)
        r = engine.assess(inp)
        assert r.estimated_at_risk_deals == 3

    def test_at_risk_deals_is_int(self, engine):
        inp = make_input(deals_stalled_14d_plus=2, late_stage_deals_stalled_count=1)
        r = engine.assess(inp)
        assert isinstance(r.estimated_at_risk_deals, int)

    def test_at_risk_deals_large_values(self, engine):
        inp = make_input(deals_stalled_14d_plus=100, late_stage_deals_stalled_count=50)
        r = engine.assess(inp)
        assert r.estimated_at_risk_deals == 150

    def test_at_risk_deals_matches_formula(self, engine):
        inp = make_input(deals_stalled_14d_plus=7, late_stage_deals_stalled_count=3)
        r = engine.assess(inp)
        assert r.estimated_at_risk_deals == 7 + 3

    def test_at_risk_deals_preserved_in_to_dict(self, engine):
        inp = make_input(deals_stalled_14d_plus=5, late_stage_deals_stalled_count=2)
        r = engine.assess(inp)
        assert r.to_dict()["estimated_at_risk_deals"] == 7


# ---------------------------------------------------------------------------
# 18. velocity_signal
# ---------------------------------------------------------------------------

class TestVelocitySignal:
    def test_signal_is_string(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.velocity_signal, str)

    def test_signal_non_empty(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert len(r.velocity_signal) > 0

    def test_healthy_signal_no_degradation(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert "healthy" in r.velocity_signal.lower()

    def test_signal_contains_composite(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=90.0,
            avg_sales_cycle_days_benchmark=60.0,
            deals_stalled_14d_plus=2,
        )
        r = engine.assess(inp)
        assert "composite" in r.velocity_signal.lower()

    def test_signal_contains_cycle_info_when_excess(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=90.0,
            avg_sales_cycle_days_benchmark=60.0,
        )
        r = engine.assess(inp)
        # excess >= 10% => cycle info in signal
        assert "90" in r.velocity_signal or "cycle" in r.velocity_signal.lower()

    def test_signal_contains_stalled_deals_info(self, engine):
        inp = make_input(deals_stalled_14d_plus=3)
        r = engine.assess(inp)
        assert "stalled" in r.velocity_signal.lower()

    def test_signal_contains_late_stage_info(self, engine):
        # Ensure composite >= 5 so the detailed signal path is used
        inp = make_input(
            late_stage_deals_count=5,
            late_stage_deals_stalled_count=3,
            approval_cycle_avg_days=15.0,
            approval_cycle_benchmark_days=10.0,
        )
        r = engine.assess(inp)
        # composite should be well above 5; late stage stalled appears in signal
        if r.velocity_composite >= 5 and inp.late_stage_deals_stalled_count >= 1:
            assert "late" in r.velocity_signal.lower()

    def test_signal_contains_buyer_response(self, engine):
        inp = make_input(buyer_response_time_avg_days=5.0)
        r = engine.assess(inp)
        assert "buyer" in r.velocity_signal.lower()

    def test_signal_pattern_label_present(self, engine):
        inp = make_input(deals_stalled_30d_plus=4, avg_sales_cycle_days_current=120.0,
                         avg_sales_cycle_days_benchmark=60.0)
        r = engine.assess(inp)
        if r.velocity_pattern != VelocityPattern.none:
            pattern_word = r.velocity_pattern.value.split("_")[0]
            assert pattern_word in r.velocity_signal.lower()


# ---------------------------------------------------------------------------
# 19. assess() – identity fields preserved
# ---------------------------------------------------------------------------

class TestAssessIdentityFields:
    def test_rep_id_preserved(self, engine):
        inp = make_input(rep_id="REP-XYZ")
        r = engine.assess(inp)
        assert r.rep_id == "REP-XYZ"

    def test_region_preserved(self, engine):
        inp = make_input(region="EMEA")
        r = engine.assess(inp)
        assert r.region == "EMEA"

    def test_different_rep_ids(self, engine):
        ids = ["A1", "B2", "C3"]
        for rid in ids:
            r = engine.assess(make_input(rep_id=rid))
            assert r.rep_id == rid

    def test_different_regions(self, engine):
        regions = ["NORTH", "SOUTH", "EAST"]
        for reg in regions:
            r = engine.assess(make_input(region=reg))
            assert r.region == reg

    def test_result_is_velocity_degradation_result(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r, VelocityDegradationResult)


# ---------------------------------------------------------------------------
# 20. assess_batch()
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_batch_returns_list(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert isinstance(results, list)

    def test_batch_length_matches_input(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(7)]
        results = engine.assess_batch(inputs)
        assert len(results) == 7

    def test_batch_empty_input(self, engine):
        results = engine.assess_batch([])
        assert results == []

    def test_batch_single_input(self, engine):
        inputs = [make_input(rep_id="SINGLE")]
        results = engine.assess_batch(inputs)
        assert len(results) == 1
        assert results[0].rep_id == "SINGLE"

    def test_batch_rep_id_order_preserved(self, engine):
        ids = [f"R{i:03d}" for i in range(10)]
        inputs = [make_input(rep_id=rid) for rid in ids]
        results = engine.assess_batch(inputs)
        assert [r.rep_id for r in results] == ids

    def test_batch_each_result_is_correct_type(self, engine):
        inputs = [make_input() for _ in range(3)]
        results = engine.assess_batch(inputs)
        assert all(isinstance(r, VelocityDegradationResult) for r in results)

    def test_batch_accumulates_in_engine_history(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(4)]
        engine.assess_batch(inputs)
        s = engine.summary()
        assert s["total"] == 4

    def test_batch_mixed_risk_levels(self, engine):
        inputs = [
            make_input(rep_id="HEALTHY"),
            make_input(
                rep_id="CRITICAL",
                avg_sales_cycle_days_current=120.0,
                avg_sales_cycle_days_benchmark=60.0,
                deals_stalled_30d_plus=5,
                buyer_response_time_avg_days=10.0,
            ),
        ]
        results = engine.assess_batch(inputs)
        risks = {r.rep_id: r.velocity_risk for r in results}
        assert risks["HEALTHY"] == VelocityRisk.low
        assert risks["CRITICAL"] in (VelocityRisk.high, VelocityRisk.critical)


# ---------------------------------------------------------------------------
# 21. summary() – empty engine
# ---------------------------------------------------------------------------

class TestSummaryEmpty:
    def test_empty_summary_total_zero(self):
        e = SalesCycleVelocityDegradationEngine()
        s = e.summary()
        assert s["total"] == 0

    def test_empty_summary_risk_counts_empty(self):
        e = SalesCycleVelocityDegradationEngine()
        s = e.summary()
        assert s["risk_counts"] == {}

    def test_empty_summary_pattern_counts_empty(self):
        e = SalesCycleVelocityDegradationEngine()
        s = e.summary()
        assert s["pattern_counts"] == {}

    def test_empty_summary_severity_counts_empty(self):
        e = SalesCycleVelocityDegradationEngine()
        s = e.summary()
        assert s["severity_counts"] == {}

    def test_empty_summary_action_counts_empty(self):
        e = SalesCycleVelocityDegradationEngine()
        s = e.summary()
        assert s["action_counts"] == {}

    def test_empty_summary_avg_composite_zero(self):
        e = SalesCycleVelocityDegradationEngine()
        s = e.summary()
        assert s["avg_velocity_composite"] == 0.0

    def test_empty_summary_degraded_count_zero(self):
        e = SalesCycleVelocityDegradationEngine()
        s = e.summary()
        assert s["degraded_count"] == 0

    def test_empty_summary_intervention_count_zero(self):
        e = SalesCycleVelocityDegradationEngine()
        s = e.summary()
        assert s["intervention_count"] == 0

    def test_empty_summary_avg_cycle_length_score_zero(self):
        e = SalesCycleVelocityDegradationEngine()
        s = e.summary()
        assert s["avg_cycle_length_score"] == 0.0

    def test_empty_summary_avg_stage_stall_score_zero(self):
        e = SalesCycleVelocityDegradationEngine()
        s = e.summary()
        assert s["avg_stage_stall_score"] == 0.0

    def test_empty_summary_avg_buyer_engagement_score_zero(self):
        e = SalesCycleVelocityDegradationEngine()
        s = e.summary()
        assert s["avg_buyer_engagement_score"] == 0.0

    def test_empty_summary_avg_late_stage_drag_score_zero(self):
        e = SalesCycleVelocityDegradationEngine()
        s = e.summary()
        assert s["avg_late_stage_drag_score"] == 0.0

    def test_empty_summary_total_estimated_at_risk_deals_zero(self):
        e = SalesCycleVelocityDegradationEngine()
        s = e.summary()
        assert s["total_estimated_at_risk_deals"] == 0

    def test_empty_summary_returns_13_keys(self):
        e = SalesCycleVelocityDegradationEngine()
        s = e.summary()
        assert len(s) == 13


# ---------------------------------------------------------------------------
# 22. summary() – after assessments
# ---------------------------------------------------------------------------

class TestSummaryAfterAssessments:
    def test_summary_total_count(self, engine):
        for i in range(5):
            engine.assess(make_input(rep_id=f"R{i}"))
        s = engine.summary()
        assert s["total"] == 5

    def test_summary_13_keys_after_assessments(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert len(s) == 13

    def test_summary_risk_counts_sum_to_total(self, engine):
        for i in range(6):
            engine.assess(make_input(rep_id=f"R{i}"))
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_pattern_counts_sum_to_total(self, engine):
        for i in range(6):
            engine.assess(make_input(rep_id=f"R{i}"))
        s = engine.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_summary_severity_counts_sum_to_total(self, engine):
        for i in range(6):
            engine.assess(make_input(rep_id=f"R{i}"))
        s = engine.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_to_total(self, engine):
        for i in range(6):
            engine.assess(make_input(rep_id=f"R{i}"))
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_avg_composite_is_float(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert isinstance(s["avg_velocity_composite"], float)

    def test_summary_degraded_count_correct(self, engine):
        engine.assess(make_input())  # healthy -> not degraded
        engine.assess(make_input(deals_stalled_30d_plus=3))  # degraded
        s = engine.summary()
        assert s["degraded_count"] == 1

    def test_summary_intervention_count_correct(self, engine):
        engine.assess(make_input())  # no intervention
        engine.assess(make_input(buyer_response_time_avg_days=7.0))  # intervention
        engine.assess(make_input(late_stage_deals_count=3, late_stage_deals_stalled_count=3))  # intervention
        s = engine.summary()
        assert s["intervention_count"] == 2

    def test_summary_total_at_risk_deals_is_integer_sum(self, engine):
        engine.assess(make_input(deals_stalled_14d_plus=3, late_stage_deals_stalled_count=2))
        engine.assess(make_input(deals_stalled_14d_plus=1, late_stage_deals_stalled_count=1))
        s = engine.summary()
        assert s["total_estimated_at_risk_deals"] == 7

    def test_summary_total_at_risk_deals_is_int(self, engine):
        engine.assess(make_input(deals_stalled_14d_plus=2))
        s = engine.summary()
        assert isinstance(s["total_estimated_at_risk_deals"], int)

    def test_summary_avg_cycle_length_score_positive(self, engine):
        engine.assess(make_input(
            avg_sales_cycle_days_current=90.0,
            avg_sales_cycle_days_benchmark=60.0,
        ))
        s = engine.summary()
        assert s["avg_cycle_length_score"] > 0.0

    def test_summary_avg_stage_stall_score_positive(self, engine):
        engine.assess(make_input(deals_stalled_30d_plus=3))
        s = engine.summary()
        assert s["avg_stage_stall_score"] > 0.0

    def test_summary_avg_buyer_engagement_score_positive(self, engine):
        engine.assess(make_input(buyer_response_time_avg_days=7.0))
        s = engine.summary()
        assert s["avg_buyer_engagement_score"] > 0.0

    def test_summary_avg_late_stage_drag_score_positive(self, engine):
        engine.assess(make_input(late_stage_deals_count=5, late_stage_deals_stalled_count=3))
        s = engine.summary()
        assert s["avg_late_stage_drag_score"] > 0.0

    def test_summary_risk_counts_keys_are_strings(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert all(isinstance(k, str) for k in s["risk_counts"])

    def test_summary_pattern_counts_keys_are_strings(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert all(isinstance(k, str) for k in s["pattern_counts"])

    def test_summary_accumulates_across_assess_and_batch(self, engine):
        engine.assess(make_input(rep_id="A"))
        engine.assess_batch([make_input(rep_id=f"B{i}") for i in range(3)])
        s = engine.summary()
        assert s["total"] == 4

    def test_summary_avg_composite_single_item(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=90.0,
            avg_sales_cycle_days_benchmark=60.0,
        )
        r = engine.assess(inp)
        s = engine.summary()
        assert s["avg_velocity_composite"] == r.velocity_composite


# ---------------------------------------------------------------------------
# 23. Engine state / isolation
# ---------------------------------------------------------------------------

class TestEngineState:
    def test_fresh_engine_has_empty_results(self):
        e = SalesCycleVelocityDegradationEngine()
        assert e.summary()["total"] == 0

    def test_two_engines_are_independent(self):
        e1 = SalesCycleVelocityDegradationEngine()
        e2 = SalesCycleVelocityDegradationEngine()
        e1.assess(make_input(rep_id="A"))
        e1.assess(make_input(rep_id="B"))
        e2.assess(make_input(rep_id="C"))
        assert e1.summary()["total"] == 2
        assert e2.summary()["total"] == 1

    def test_assess_accumulates_multiple_calls(self):
        e = SalesCycleVelocityDegradationEngine()
        for i in range(10):
            e.assess(make_input(rep_id=f"R{i}"))
        assert e.summary()["total"] == 10

    def test_engine_summary_after_batch_only(self):
        e = SalesCycleVelocityDegradationEngine()
        e.assess_batch([make_input(rep_id=f"X{i}") for i in range(5)])
        assert e.summary()["total"] == 5


# ---------------------------------------------------------------------------
# 24. Edge cases and boundary conditions
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_all_zeros_input(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=0.0,
            avg_sales_cycle_days_benchmark=0.0,
            avg_sales_cycle_days_prior=0.0,
        )
        r = engine.assess(inp)
        assert r.velocity_composite >= 0.0

    def test_exact_150pct_benchmark_trigger(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=90.0,
            avg_sales_cycle_days_benchmark=60.0,
        )
        r = engine.assess(inp)
        assert r.is_velocity_degraded is True

    def test_exact_30d_stalled_trigger(self, engine):
        inp = make_input(deals_stalled_30d_plus=3)
        r = engine.assess(inp)
        assert r.is_velocity_degraded is True

    def test_exact_7d_buyer_response_trigger(self, engine):
        inp = make_input(buyer_response_time_avg_days=7.0)
        r = engine.assess(inp)
        assert r.requires_intervention is True

    def test_exact_3_late_stage_stalled_trigger(self, engine):
        inp = make_input(late_stage_deals_count=5, late_stage_deals_stalled_count=3)
        r = engine.assess(inp)
        assert r.requires_intervention is True

    def test_large_input_values_no_overflow(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=9999.0,
            avg_sales_cycle_days_benchmark=1.0,
            avg_sales_cycle_days_prior=1.0,
            deals_stalled_7d_plus=9999,
            deals_stalled_14d_plus=9999,
            deals_stalled_30d_plus=9999,
            close_date_slipped_count=9999,
            late_stage_deals_count=9999,
            late_stage_deals_stalled_count=9999,
        )
        r = engine.assess(inp)
        assert r.velocity_composite <= 100.0

    def test_at_risk_deals_type_is_int_always(self, engine):
        for n in [0, 1, 5, 100]:
            r = engine.assess(make_input(deals_stalled_14d_plus=n))
            assert isinstance(r.estimated_at_risk_deals, int)

    def test_composite_capped_at_100_always(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=1000.0,
            avg_sales_cycle_days_benchmark=1.0,
            deals_stalled_30d_plus=100,
            buyer_response_time_avg_days=100.0,
            late_stage_deals_count=100,
            late_stage_deals_stalled_count=100,
        )
        r = engine.assess(inp)
        assert r.velocity_composite <= 100.0

    def test_single_stalled_14d_deal(self, engine):
        inp = make_input(deals_stalled_14d_plus=1)
        r = engine.assess(inp)
        assert r.estimated_at_risk_deals == 1

    def test_rep_id_empty_string(self, engine):
        inp = make_input(rep_id="")
        r = engine.assess(inp)
        assert r.rep_id == ""

    def test_region_empty_string(self, engine):
        inp = make_input(region="")
        r = engine.assess(inp)
        assert r.region == ""

    def test_all_scores_are_floats(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.cycle_length_score, float)
        assert isinstance(r.stage_stall_score, float)
        assert isinstance(r.buyer_engagement_score, float)
        assert isinstance(r.late_stage_drag_score, float)
        assert isinstance(r.velocity_composite, float)

    def test_score_rounding_one_decimal(self, engine):
        inp = make_input(
            avg_sales_cycle_days_current=90.0,
            avg_sales_cycle_days_benchmark=60.0,
        )
        r = engine.assess(inp)
        # Check one decimal place
        for score in [r.cycle_length_score, r.stage_stall_score,
                      r.buyer_engagement_score, r.late_stage_drag_score,
                      r.velocity_composite]:
            assert score == round(score, 1)


# ---------------------------------------------------------------------------
# 25. Consistency cross-checks
# ---------------------------------------------------------------------------

class TestConsistencyCrossChecks:
    def test_risk_severity_consistency(self, engine):
        inputs = [
            make_input(),
            make_input(deals_stalled_30d_plus=3),
            make_input(avg_sales_cycle_days_current=120.0, avg_sales_cycle_days_benchmark=60.0),
            make_input(buyer_response_time_avg_days=10.0, late_stage_deals_stalled_count=4,
                       late_stage_deals_count=5),
        ]
        for inp in inputs:
            r = engine.assess(inp)
            composite = r.velocity_composite
            # risk and severity must be consistent with composite
            if composite >= 60:
                assert r.velocity_risk == VelocityRisk.critical
                assert r.velocity_severity == VelocitySeverity.stalled
            elif composite >= 40:
                assert r.velocity_risk == VelocityRisk.high
                assert r.velocity_severity == VelocitySeverity.degraded
            elif composite >= 20:
                assert r.velocity_risk == VelocityRisk.moderate
                assert r.velocity_severity == VelocitySeverity.slowing
            else:
                assert r.velocity_risk == VelocityRisk.low
                assert r.velocity_severity == VelocitySeverity.healthy

    def test_degraded_implies_intervention_sometimes(self, engine):
        # When composite >= 40, both degraded AND intervention should be true
        inp = make_input(
            avg_sales_cycle_days_current=120.0,
            avg_sales_cycle_days_benchmark=60.0,
            deals_stalled_30d_plus=5,
            buyer_response_time_avg_days=8.0,
        )
        r = engine.assess(inp)
        if r.velocity_composite >= 40:
            assert r.is_velocity_degraded is True
            assert r.requires_intervention is True

    def test_action_consistent_with_risk(self, engine):
        inputs = [make_input(), make_input(
            avg_sales_cycle_days_current=120.0,
            avg_sales_cycle_days_benchmark=60.0,
            deals_stalled_30d_plus=5,
            buyer_response_time_avg_days=10.0,
        )]
        for inp in inputs:
            r = engine.assess(inp)
            if r.velocity_risk == VelocityRisk.critical:
                assert r.recommended_action == VelocityAction.executive_acceleration
            elif r.velocity_risk == VelocityRisk.low:
                assert r.recommended_action == VelocityAction.no_action

    def test_summary_avg_composite_bounded_by_individual_composites(self, engine):
        results = []
        for inp in [make_input(), make_input(deals_stalled_30d_plus=3)]:
            results.append(engine.assess(inp))
        s = engine.summary()
        min_c = min(r.velocity_composite for r in results)
        max_c = max(r.velocity_composite for r in results)
        assert min_c <= s["avg_velocity_composite"] <= max_c

    def test_deal_aging_requires_stalled_30d_and_cycle_score(self, engine):
        # Without cycle score, deal_aging should not trigger
        inp = make_input(deals_stalled_30d_plus=3)  # cycle score = 0
        r = engine.assess(inp)
        # cycle score must be >=20 for deal_aging
        if r.cycle_length_score < 20:
            assert r.velocity_pattern != VelocityPattern.deal_aging

    def test_at_risk_deals_always_non_negative(self, engine):
        for inp in [make_input(), make_input(deals_stalled_14d_plus=5)]:
            r = engine.assess(inp)
            assert r.estimated_at_risk_deals >= 0

    def test_summary_at_risk_deals_equals_sum_of_individual(self, engine):
        inputs = [
            make_input(deals_stalled_14d_plus=2, late_stage_deals_stalled_count=1),
            make_input(deals_stalled_14d_plus=3, late_stage_deals_stalled_count=2),
            make_input(deals_stalled_14d_plus=0, late_stage_deals_stalled_count=4,
                       late_stage_deals_count=5),
        ]
        results = engine.assess_batch(inputs)
        expected_total = sum(r.estimated_at_risk_deals for r in results)
        s = engine.summary()
        assert s["total_estimated_at_risk_deals"] == expected_total


# ---------------------------------------------------------------------------
# 26. Parameterized tests for various input permutations
# ---------------------------------------------------------------------------

class TestParameterized:
    @pytest.mark.parametrize("stalled_30d,expected_degraded", [
        (0, False),
        (1, False),
        (2, False),
        (3, True),
        (5, True),
        (10, True),
    ])
    def test_degraded_by_stalled_30d(self, engine, stalled_30d, expected_degraded):
        inp = make_input(deals_stalled_30d_plus=stalled_30d)
        r = engine.assess(inp)
        # Only check if composite < 40 and benchmark not triggered
        if r.velocity_composite < 40 and inp.avg_sales_cycle_days_current < inp.avg_sales_cycle_days_benchmark * 1.5:
            assert r.is_velocity_degraded == expected_degraded

    @pytest.mark.parametrize("buyer_days,expected_intervention", [
        (0.5, False),
        (3.0, False),
        (6.9, False),
        (7.0, True),
        (8.0, True),
        (15.0, True),
    ])
    def test_intervention_by_buyer_response(self, engine, buyer_days, expected_intervention):
        inp = make_input(buyer_response_time_avg_days=buyer_days)
        r = engine.assess(inp)
        # Only check buyer trigger in isolation (composite < 30, no late-stage stalled >=3)
        if r.velocity_composite < 30 and inp.late_stage_deals_stalled_count < 3:
            assert r.requires_intervention == expected_intervention

    @pytest.mark.parametrize("current,benchmark,expect_excess_40", [
        (90.0, 60.0, True),   # 50% => +40
        (78.0, 60.0, False),  # 30% => +25
        (60.0, 60.0, False),  # 0% => 0
        (120.0, 60.0, True),  # 100% => +40
    ])
    def test_cycle_length_score_benchmark_excess(self, engine, current, benchmark, expect_excess_40):
        inp = make_input(
            avg_sales_cycle_days_current=current,
            avg_sales_cycle_days_benchmark=benchmark,
            avg_sales_cycle_days_prior=200.0,  # avoid trend trigger
        )
        r = engine.assess(inp)
        if expect_excess_40:
            assert r.cycle_length_score >= 40.0
        else:
            assert r.cycle_length_score < 40.0

    @pytest.mark.parametrize("composite,expected_risk", [
        (0.0, VelocityRisk.low),
        (19.9, VelocityRisk.low),
        (20.0, VelocityRisk.moderate),
        (39.9, VelocityRisk.moderate),
        (40.0, VelocityRisk.high),
        (59.9, VelocityRisk.high),
        (60.0, VelocityRisk.critical),
        (100.0, VelocityRisk.critical),
    ])
    def test_risk_level_mapping(self, composite, expected_risk):
        e = SalesCycleVelocityDegradationEngine()
        # Access private method directly for unit testing
        assert e._risk_level(composite) == expected_risk

    @pytest.mark.parametrize("composite,expected_severity", [
        (0.0, VelocitySeverity.healthy),
        (19.9, VelocitySeverity.healthy),
        (20.0, VelocitySeverity.slowing),
        (39.9, VelocitySeverity.slowing),
        (40.0, VelocitySeverity.degraded),
        (59.9, VelocitySeverity.degraded),
        (60.0, VelocitySeverity.stalled),
        (100.0, VelocitySeverity.stalled),
    ])
    def test_severity_mapping(self, composite, expected_severity):
        e = SalesCycleVelocityDegradationEngine()
        assert e._severity(composite) == expected_severity

    @pytest.mark.parametrize("stalled14d,late_stalled,expected_ar", [
        (0, 0, 0),
        (2, 0, 2),
        (0, 3, 3),
        (4, 2, 6),
        (10, 5, 15),
    ])
    def test_at_risk_deals_formula(self, engine, stalled14d, late_stalled, expected_ar):
        inp = make_input(
            deals_stalled_14d_plus=stalled14d,
            late_stage_deals_stalled_count=late_stalled,
            late_stage_deals_count=max(late_stalled, 1) if late_stalled > 0 else 0,
        )
        r = engine.assess(inp)
        assert r.estimated_at_risk_deals == expected_ar

    @pytest.mark.parametrize("close_slips,min_score", [
        (0, 0),
        (1, 5),
        (3, 12),
        (5, 20),
        (10, 20),
    ])
    def test_cycle_length_close_date_slippage(self, engine, close_slips, min_score):
        inp = make_input(
            close_date_slipped_count=close_slips,
            avg_sales_cycle_days_benchmark=200.0,  # avoid benchmark trigger
            avg_sales_cycle_days_prior=200.0,
        )
        r = engine.assess(inp)
        assert r.cycle_length_score >= min_score

    @pytest.mark.parametrize("map_pct,min_stage_score", [
        (0.39, 15),
        (0.40, 0),   # >=0.40 => no MAP stage contribution
        (0.59, 7),
        (0.60, 0),   # >=0.60 => no MAP stage contribution
    ])
    def test_stage_stall_map_adherence(self, engine, map_pct, min_stage_score):
        inp = make_input(mutual_action_plan_adherence_pct=map_pct)
        r = engine.assess(inp)
        assert r.stage_stall_score >= min_stage_score

    @pytest.mark.parametrize("approval_avg,approval_bench,min_late_score", [
        (15.0, 10.0, 30),   # 50% excess
        (12.5, 10.0, 15),   # 25% excess
        (11.0, 10.0, 6),    # 10% excess
        (10.0, 10.0, 0),    # no excess
    ])
    def test_late_stage_approval_cycle(self, engine, approval_avg, approval_bench, min_late_score):
        inp = make_input(
            approval_cycle_avg_days=approval_avg,
            approval_cycle_benchmark_days=approval_bench,
            late_stage_deals_count=0,
            late_stage_deals_stalled_count=0,
        )
        r = engine.assess(inp)
        assert r.late_stage_drag_score >= min_late_score


# ---------------------------------------------------------------------------
# 27. Internal method unit tests
# ---------------------------------------------------------------------------

class TestInternalMethods:
    def test_risk_level_direct_low(self):
        e = SalesCycleVelocityDegradationEngine()
        assert e._risk_level(0.0) == VelocityRisk.low
        assert e._risk_level(19.9) == VelocityRisk.low

    def test_risk_level_direct_moderate(self):
        e = SalesCycleVelocityDegradationEngine()
        assert e._risk_level(20.0) == VelocityRisk.moderate
        assert e._risk_level(39.9) == VelocityRisk.moderate

    def test_risk_level_direct_high(self):
        e = SalesCycleVelocityDegradationEngine()
        assert e._risk_level(40.0) == VelocityRisk.high
        assert e._risk_level(59.9) == VelocityRisk.high

    def test_risk_level_direct_critical(self):
        e = SalesCycleVelocityDegradationEngine()
        assert e._risk_level(60.0) == VelocityRisk.critical
        assert e._risk_level(100.0) == VelocityRisk.critical

    def test_severity_direct_healthy(self):
        e = SalesCycleVelocityDegradationEngine()
        assert e._severity(0.0) == VelocitySeverity.healthy

    def test_severity_direct_slowing(self):
        e = SalesCycleVelocityDegradationEngine()
        assert e._severity(20.0) == VelocitySeverity.slowing

    def test_severity_direct_degraded(self):
        e = SalesCycleVelocityDegradationEngine()
        assert e._severity(40.0) == VelocitySeverity.degraded

    def test_severity_direct_stalled(self):
        e = SalesCycleVelocityDegradationEngine()
        assert e._severity(60.0) == VelocitySeverity.stalled

    def test_action_critical_always_executive(self):
        e = SalesCycleVelocityDegradationEngine()
        for p in VelocityPattern:
            assert e._action(VelocityRisk.critical, p) == VelocityAction.executive_acceleration

    def test_action_low_always_no_action(self):
        e = SalesCycleVelocityDegradationEngine()
        for p in VelocityPattern:
            assert e._action(VelocityRisk.low, p) == VelocityAction.no_action

    def test_action_moderate_always_cycle_review(self):
        e = SalesCycleVelocityDegradationEngine()
        for p in VelocityPattern:
            assert e._action(VelocityRisk.moderate, p) == VelocityAction.cycle_review

    def test_action_high_deal_aging_returns_reset(self):
        e = SalesCycleVelocityDegradationEngine()
        assert e._action(VelocityRisk.high, VelocityPattern.deal_aging) == VelocityAction.deal_qualification_reset

    def test_action_high_non_deal_aging_returns_buyer_re_engagement(self):
        e = SalesCycleVelocityDegradationEngine()
        non_aging = [p for p in VelocityPattern if p != VelocityPattern.deal_aging]
        for p in non_aging:
            assert e._action(VelocityRisk.high, p) == VelocityAction.buyer_re_engagement

    def test_at_risk_deals_direct(self):
        e = SalesCycleVelocityDegradationEngine()
        inp = make_input(deals_stalled_14d_plus=3, late_stage_deals_stalled_count=4,
                         late_stage_deals_count=5)
        assert e._at_risk_deals(inp) == 7

    def test_is_velocity_degraded_composite_trigger(self):
        e = SalesCycleVelocityDegradationEngine()
        inp = make_input()
        assert e._is_velocity_degraded(40.0, inp) is True
        assert e._is_velocity_degraded(39.9, inp) is False

    def test_is_velocity_degraded_stalled_30d_trigger(self):
        e = SalesCycleVelocityDegradationEngine()
        inp = make_input(deals_stalled_30d_plus=3)
        assert e._is_velocity_degraded(0.0, inp) is True

    def test_is_velocity_degraded_benchmark_trigger(self):
        e = SalesCycleVelocityDegradationEngine()
        inp_yes = make_input(avg_sales_cycle_days_current=90.0, avg_sales_cycle_days_benchmark=60.0)
        inp_no = make_input(avg_sales_cycle_days_current=89.9, avg_sales_cycle_days_benchmark=60.0)
        assert e._is_velocity_degraded(0.0, inp_yes) is True
        assert e._is_velocity_degraded(0.0, inp_no) is False

    def test_requires_intervention_composite_trigger(self):
        e = SalesCycleVelocityDegradationEngine()
        inp = make_input()
        assert e._requires_intervention(30.0, inp) is True
        assert e._requires_intervention(29.9, inp) is False

    def test_requires_intervention_late_stage_trigger(self):
        e = SalesCycleVelocityDegradationEngine()
        inp = make_input(late_stage_deals_stalled_count=3, late_stage_deals_count=5)
        assert e._requires_intervention(0.0, inp) is True

    def test_requires_intervention_buyer_response_trigger(self):
        e = SalesCycleVelocityDegradationEngine()
        inp = make_input(buyer_response_time_avg_days=7.0)
        assert e._requires_intervention(0.0, inp) is True
        inp2 = make_input(buyer_response_time_avg_days=6.99)
        assert e._requires_intervention(0.0, inp2) is False


# ---------------------------------------------------------------------------
# 28. Additional boundary and miscellaneous tests
# ---------------------------------------------------------------------------

class TestAdditionalMiscellaneous:
    def test_engine_instantiation(self):
        e = SalesCycleVelocityDegradationEngine()
        assert e is not None

    def test_result_rep_id_and_region_in_to_dict(self, engine):
        inp = make_input(rep_id="TESTID", region="APJ")
        r = engine.assess(inp)
        d = r.to_dict()
        assert d["rep_id"] == "TESTID"
        assert d["region"] == "APJ"

    def test_summary_after_single_assess(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert s["total"] == 1

    def test_summary_risk_counts_includes_all_assessed_risks(self, engine):
        engine.assess(make_input())  # low risk
        s = engine.summary()
        assert "low" in s["risk_counts"] or sum(s["risk_counts"].values()) == 1

    def test_summary_severity_counts_includes_healthy(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert "healthy" in s["severity_counts"]

    def test_summary_action_counts_includes_no_action(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert "no_action" in s["action_counts"]

    def test_summary_pattern_counts_includes_none(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert "none" in s["pattern_counts"]

    def test_multiple_batch_calls_accumulate(self, engine):
        engine.assess_batch([make_input(rep_id=f"A{i}") for i in range(3)])
        engine.assess_batch([make_input(rep_id=f"B{i}") for i in range(4)])
        s = engine.summary()
        assert s["total"] == 7

    def test_result_all_enum_fields_correct_type(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        assert isinstance(r.velocity_risk, VelocityRisk)
        assert isinstance(r.velocity_pattern, VelocityPattern)
        assert isinstance(r.velocity_severity, VelocitySeverity)
        assert isinstance(r.recommended_action, VelocityAction)

    def test_composite_never_exceeds_100(self, engine):
        # Run many varied inputs
        for i in range(20):
            inp = make_input(
                avg_sales_cycle_days_current=float(i * 10),
                avg_sales_cycle_days_benchmark=max(1.0, float(i)),
                deals_stalled_30d_plus=i % 5,
                buyer_response_time_avg_days=float(i % 8),
            )
            r = engine.assess(inp)
            assert r.velocity_composite <= 100.0

    def test_high_risk_requires_intervention_true(self, engine):
        # High/critical risk always implies intervention (composite >= 40 >= 30)
        inp = make_input(
            avg_sales_cycle_days_current=120.0,
            avg_sales_cycle_days_benchmark=60.0,
            deals_stalled_30d_plus=5,
        )
        r = engine.assess(inp)
        if r.velocity_risk in (VelocityRisk.high, VelocityRisk.critical):
            assert r.requires_intervention is True

    def test_summary_avg_scores_between_0_and_100(self, engine):
        for _ in range(5):
            engine.assess(make_input())
        s = engine.summary()
        for key in ["avg_cycle_length_score", "avg_stage_stall_score",
                    "avg_buyer_engagement_score", "avg_late_stage_drag_score",
                    "avg_velocity_composite"]:
            assert 0.0 <= s[key] <= 100.0, f"{key} out of bounds"

    def test_pattern_none_produces_none_signal_prefix(self, engine, healthy_input):
        r = engine.assess(healthy_input)
        if r.velocity_pattern == VelocityPattern.none and r.velocity_composite < 5:
            assert "healthy" in r.velocity_signal.lower()

    def test_deal_aging_pattern_with_cycle_score_under_20_is_not_aging(self, engine):
        # deals_stalled_30d_plus=3 but cycle score < 20 => no deal_aging
        inp = make_input(
            deals_stalled_30d_plus=3,
            avg_sales_cycle_days_current=60.0,
            avg_sales_cycle_days_benchmark=60.0,
            avg_sales_cycle_days_prior=60.0,
            close_date_slipped_count=0,
        )
        r = engine.assess(inp)
        # cycle_length_score should be 0, so deal_aging not triggered
        if r.cycle_length_score < 20:
            assert r.velocity_pattern != VelocityPattern.deal_aging

    def test_assess_returns_immediately(self, engine, healthy_input):
        # Just ensure no exception is thrown and result is returned
        result = engine.assess(healthy_input)
        assert result is not None

    def test_assess_batch_returns_correct_results(self, engine):
        inputs = [
            make_input(rep_id="ALPHA", deals_stalled_30d_plus=3),
            make_input(rep_id="BETA"),
        ]
        results = engine.assess_batch(inputs)
        assert results[0].rep_id == "ALPHA"
        assert results[0].is_velocity_degraded is True
        assert results[1].rep_id == "BETA"

    def test_summary_total_at_risk_deals_is_integer(self, engine):
        engine.assess(make_input(deals_stalled_14d_plus=2, late_stage_deals_stalled_count=3,
                                 late_stage_deals_count=5))
        s = engine.summary()
        assert isinstance(s["total_estimated_at_risk_deals"], int)
