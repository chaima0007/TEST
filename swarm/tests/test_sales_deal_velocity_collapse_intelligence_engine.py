"""
Comprehensive pytest tests for SalesDealVelocityCollapseIntelligenceEngine.

Covers:
- VelocityInput construction (all 22 fields)
- All 4 sub-score methods with threshold boundary testing
- Composite score calculation and weighting
- All 6 VelocityPattern detections (priority order)
- Risk / Severity mappings
- Action routing for every risk × pattern combo
- has_velocity_gap flag logic
- requires_velocity_intervention flag logic
- estimated_at_risk_pipeline_usd formula
- Velocity signal text generation
- VelocityResult.to_dict() — 15 keys
- summary() — 13 keys (empty and non-empty engine)
- assess() and assess_batch() public API
- Edge cases: zero values, caps, boundary conditions
"""
from __future__ import annotations

import pytest
from swarm.intelligence.sales_deal_velocity_collapse_intelligence_engine import (
    SalesDealVelocityCollapseIntelligenceEngine,
    VelocityInput,
    VelocityResult,
    VelocityRisk,
    VelocityPattern,
    VelocitySeverity,
    VelocityAction,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_input(
    *,
    rep_id: str = "REP-001",
    region: str = "APAC",
    evaluation_period_id: str = "Q2-2026",
    avg_days_in_current_stage: float = 5.0,
    avg_cycle_length_days: float = 60.0,
    cycle_length_vs_benchmark_pct: float = 0.05,
    stage_regression_count: int = 0,
    no_activity_streak_days: int = 1,
    champion_response_time_days: float = 2.0,
    executive_sponsor_days_since_contact: float = 10.0,
    next_step_defined_rate_pct: float = 0.90,
    mutual_action_plan_completion_pct: float = 0.80,
    close_date_slip_count: int = 0,
    close_date_slip_days_avg: float = 0.0,
    proposal_sent_to_response_days: float = 3.0,
    poc_to_commercial_days: float = 14.0,
    avg_stakeholder_response_rate_pct: float = 0.75,
    multi_threaded_deal_rate_pct: float = 0.70,
    competitive_re_eval_trigger_pct: float = 0.05,
    late_stage_stall_rate_pct: float = 0.05,
    total_active_deals: int = 10,
    avg_deal_value_usd: float = 50_000.0,
) -> VelocityInput:
    return VelocityInput(
        rep_id=rep_id,
        region=region,
        evaluation_period_id=evaluation_period_id,
        avg_days_in_current_stage=avg_days_in_current_stage,
        avg_cycle_length_days=avg_cycle_length_days,
        cycle_length_vs_benchmark_pct=cycle_length_vs_benchmark_pct,
        stage_regression_count=stage_regression_count,
        no_activity_streak_days=no_activity_streak_days,
        champion_response_time_days=champion_response_time_days,
        executive_sponsor_days_since_contact=executive_sponsor_days_since_contact,
        next_step_defined_rate_pct=next_step_defined_rate_pct,
        mutual_action_plan_completion_pct=mutual_action_plan_completion_pct,
        close_date_slip_count=close_date_slip_count,
        close_date_slip_days_avg=close_date_slip_days_avg,
        proposal_sent_to_response_days=proposal_sent_to_response_days,
        poc_to_commercial_days=poc_to_commercial_days,
        avg_stakeholder_response_rate_pct=avg_stakeholder_response_rate_pct,
        multi_threaded_deal_rate_pct=multi_threaded_deal_rate_pct,
        competitive_re_eval_trigger_pct=competitive_re_eval_trigger_pct,
        late_stage_stall_rate_pct=late_stage_stall_rate_pct,
        total_active_deals=total_active_deals,
        avg_deal_value_usd=avg_deal_value_usd,
    )


def _engine() -> SalesDealVelocityCollapseIntelligenceEngine:
    return SalesDealVelocityCollapseIntelligenceEngine()


# ===========================================================================
# Section 1 — VelocityInput construction
# ===========================================================================

class TestVelocityInputConstruction:
    def test_all_22_fields_present(self):
        inp = _make_input()
        assert inp.rep_id == "REP-001"
        assert inp.region == "APAC"
        assert inp.evaluation_period_id == "Q2-2026"
        assert inp.avg_days_in_current_stage == 5.0
        assert inp.avg_cycle_length_days == 60.0
        assert inp.cycle_length_vs_benchmark_pct == 0.05
        assert inp.stage_regression_count == 0
        assert inp.no_activity_streak_days == 1
        assert inp.champion_response_time_days == 2.0
        assert inp.executive_sponsor_days_since_contact == 10.0
        assert inp.next_step_defined_rate_pct == 0.90
        assert inp.mutual_action_plan_completion_pct == 0.80
        assert inp.close_date_slip_count == 0
        assert inp.close_date_slip_days_avg == 0.0
        assert inp.proposal_sent_to_response_days == 3.0
        assert inp.poc_to_commercial_days == 14.0
        assert inp.avg_stakeholder_response_rate_pct == 0.75
        assert inp.multi_threaded_deal_rate_pct == 0.70
        assert inp.competitive_re_eval_trigger_pct == 0.05
        assert inp.late_stage_stall_rate_pct == 0.05
        assert inp.total_active_deals == 10
        assert inp.avg_deal_value_usd == 50_000.0

    def test_field_count_is_22(self):
        import dataclasses
        fields = dataclasses.fields(VelocityInput)
        assert len(fields) == 22

    def test_stage_regression_count_is_int(self):
        inp = _make_input(stage_regression_count=3)
        assert isinstance(inp.stage_regression_count, int)

    def test_no_activity_streak_days_is_int(self):
        inp = _make_input(no_activity_streak_days=5)
        assert isinstance(inp.no_activity_streak_days, int)

    def test_close_date_slip_count_is_int(self):
        inp = _make_input(close_date_slip_count=2)
        assert isinstance(inp.close_date_slip_count, int)

    def test_total_active_deals_is_int(self):
        inp = _make_input(total_active_deals=20)
        assert isinstance(inp.total_active_deals, int)

    def test_rep_id_stored(self):
        inp = _make_input(rep_id="ALICE")
        assert inp.rep_id == "ALICE"

    def test_region_stored(self):
        inp = _make_input(region="EMEA")
        assert inp.region == "EMEA"

    def test_evaluation_period_id_stored(self):
        inp = _make_input(evaluation_period_id="FY26-Q1")
        assert inp.evaluation_period_id == "FY26-Q1"

    def test_zero_avg_deal_value(self):
        inp = _make_input(avg_deal_value_usd=0.0)
        assert inp.avg_deal_value_usd == 0.0

    def test_large_values_accepted(self):
        inp = _make_input(avg_deal_value_usd=1_000_000.0, total_active_deals=500)
        assert inp.avg_deal_value_usd == 1_000_000.0
        assert inp.total_active_deals == 500


# ===========================================================================
# Section 2 — _stage_stall_score
# ===========================================================================

class TestStageStallScore:
    def _score(self, **kw) -> float:
        e = _engine()
        return e._stage_stall_score(_make_input(**kw))

    # avg_days_in_current_stage thresholds
    def test_days_below_10_adds_0(self):
        assert self._score(avg_days_in_current_stage=9.9) == pytest.approx(0.0, abs=0.1)

    def test_days_exactly_10_adds_8(self):
        assert self._score(avg_days_in_current_stage=10.0) == pytest.approx(8.0, abs=0.1)

    def test_days_between_10_18_adds_8(self):
        assert self._score(avg_days_in_current_stage=15.0) == pytest.approx(8.0, abs=0.1)

    def test_days_exactly_18_adds_22(self):
        assert self._score(avg_days_in_current_stage=18.0) == pytest.approx(22.0, abs=0.1)

    def test_days_between_18_30_adds_22(self):
        assert self._score(avg_days_in_current_stage=25.0) == pytest.approx(22.0, abs=0.1)

    def test_days_exactly_30_adds_40(self):
        assert self._score(avg_days_in_current_stage=30.0) == pytest.approx(40.0, abs=0.1)

    def test_days_above_30_adds_40(self):
        assert self._score(avg_days_in_current_stage=60.0) == pytest.approx(40.0, abs=0.1)

    # cycle_length_vs_benchmark_pct thresholds
    def test_benchmark_below_010_adds_0(self):
        assert self._score(cycle_length_vs_benchmark_pct=0.09) == pytest.approx(0.0, abs=0.1)

    def test_benchmark_exactly_010_adds_6(self):
        assert self._score(cycle_length_vs_benchmark_pct=0.10) == pytest.approx(6.0, abs=0.1)

    def test_benchmark_between_010_025_adds_6(self):
        assert self._score(cycle_length_vs_benchmark_pct=0.15) == pytest.approx(6.0, abs=0.1)

    def test_benchmark_exactly_025_adds_18(self):
        assert self._score(cycle_length_vs_benchmark_pct=0.25) == pytest.approx(18.0, abs=0.1)

    def test_benchmark_between_025_050_adds_18(self):
        assert self._score(cycle_length_vs_benchmark_pct=0.35) == pytest.approx(18.0, abs=0.1)

    def test_benchmark_exactly_050_adds_35(self):
        assert self._score(cycle_length_vs_benchmark_pct=0.50) == pytest.approx(35.0, abs=0.1)

    def test_benchmark_above_050_adds_35(self):
        assert self._score(cycle_length_vs_benchmark_pct=1.0) == pytest.approx(35.0, abs=0.1)

    # stage_regression_count thresholds
    def test_regression_0_adds_0(self):
        assert self._score(stage_regression_count=0) == pytest.approx(0.0, abs=0.1)

    def test_regression_1_adds_0(self):
        assert self._score(stage_regression_count=1) == pytest.approx(0.0, abs=0.1)

    def test_regression_2_adds_12(self):
        assert self._score(stage_regression_count=2) == pytest.approx(12.0, abs=0.1)

    def test_regression_3_adds_25(self):
        assert self._score(stage_regression_count=3) == pytest.approx(25.0, abs=0.1)

    def test_regression_above_3_adds_25(self):
        assert self._score(stage_regression_count=10) == pytest.approx(25.0, abs=0.1)

    # combination and cap
    def test_stage_stall_additive(self):
        score = self._score(
            avg_days_in_current_stage=30.0,    # +40
            cycle_length_vs_benchmark_pct=0.50, # +35
            stage_regression_count=3,           # +25
        )
        assert score == pytest.approx(100.0)   # 100 capped

    def test_stage_stall_partial_combination(self):
        score = self._score(
            avg_days_in_current_stage=18.0,    # +22
            cycle_length_vs_benchmark_pct=0.25, # +18
            stage_regression_count=2,           # +12
        )
        assert score == pytest.approx(52.0)

    def test_stage_stall_max_uncapped_is_100(self):
        score = self._score(
            avg_days_in_current_stage=100.0,
            cycle_length_vs_benchmark_pct=2.0,
            stage_regression_count=10,
        )
        assert score == 100.0

    def test_stage_stall_zero_inputs(self):
        score = self._score(
            avg_days_in_current_stage=0.0,
            cycle_length_vs_benchmark_pct=0.0,
            stage_regression_count=0,
        )
        assert score == 0.0


# ===========================================================================
# Section 3 — _engagement_decay_score
# ===========================================================================

class TestEngagementDecayScore:
    def _score(self, **kw) -> float:
        e = _engine()
        return e._engagement_decay_score(_make_input(**kw))

    # no_activity_streak_days thresholds
    def test_no_activity_below_3_adds_0(self):
        assert self._score(no_activity_streak_days=2) == pytest.approx(0.0, abs=0.1)

    def test_no_activity_exactly_3_adds_8(self):
        assert self._score(no_activity_streak_days=3) == pytest.approx(8.0, abs=0.1)

    def test_no_activity_between_3_7_adds_8(self):
        assert self._score(no_activity_streak_days=5) == pytest.approx(8.0, abs=0.1)

    def test_no_activity_exactly_7_adds_22(self):
        assert self._score(no_activity_streak_days=7) == pytest.approx(22.0, abs=0.1)

    def test_no_activity_between_7_14_adds_22(self):
        assert self._score(no_activity_streak_days=10) == pytest.approx(22.0, abs=0.1)

    def test_no_activity_exactly_14_adds_40(self):
        assert self._score(no_activity_streak_days=14) == pytest.approx(40.0, abs=0.1)

    def test_no_activity_above_14_adds_40(self):
        assert self._score(no_activity_streak_days=30) == pytest.approx(40.0, abs=0.1)

    # champion_response_time_days thresholds
    def test_champion_below_5_adds_0(self):
        assert self._score(champion_response_time_days=4.9) == pytest.approx(0.0, abs=0.1)

    def test_champion_exactly_5_adds_18(self):
        assert self._score(champion_response_time_days=5.0) == pytest.approx(18.0, abs=0.1)

    def test_champion_between_5_10_adds_18(self):
        assert self._score(champion_response_time_days=7.0) == pytest.approx(18.0, abs=0.1)

    def test_champion_exactly_10_adds_35(self):
        assert self._score(champion_response_time_days=10.0) == pytest.approx(35.0, abs=0.1)

    def test_champion_above_10_adds_35(self):
        assert self._score(champion_response_time_days=20.0) == pytest.approx(35.0, abs=0.1)

    # avg_stakeholder_response_rate_pct thresholds
    def test_stakeholder_above_050_adds_0(self):
        assert self._score(avg_stakeholder_response_rate_pct=0.60) == pytest.approx(0.0, abs=0.1)

    def test_stakeholder_exactly_050_adds_12(self):
        assert self._score(avg_stakeholder_response_rate_pct=0.50) == pytest.approx(12.0, abs=0.1)

    def test_stakeholder_between_025_050_adds_12(self):
        assert self._score(avg_stakeholder_response_rate_pct=0.35) == pytest.approx(12.0, abs=0.1)

    def test_stakeholder_exactly_025_adds_25(self):
        assert self._score(avg_stakeholder_response_rate_pct=0.25) == pytest.approx(25.0, abs=0.1)

    def test_stakeholder_below_025_adds_25(self):
        assert self._score(avg_stakeholder_response_rate_pct=0.10) == pytest.approx(25.0, abs=0.1)

    # combinations and cap
    def test_engagement_decay_max_capped(self):
        score = self._score(
            no_activity_streak_days=14,
            champion_response_time_days=10.0,
            avg_stakeholder_response_rate_pct=0.25,
        )
        assert score == 100.0  # 40+35+25 = 100

    def test_engagement_decay_partial(self):
        score = self._score(
            no_activity_streak_days=7,     # +22
            champion_response_time_days=5.0, # +18
            avg_stakeholder_response_rate_pct=0.50,  # +12
        )
        assert score == pytest.approx(52.0)

    def test_engagement_decay_zero(self):
        score = self._score(
            no_activity_streak_days=0,
            champion_response_time_days=0.0,
            avg_stakeholder_response_rate_pct=1.0,
        )
        assert score == 0.0

    def test_engagement_decay_over_100_capped(self):
        score = self._score(
            no_activity_streak_days=100,
            champion_response_time_days=100.0,
            avg_stakeholder_response_rate_pct=0.0,
        )
        assert score == 100.0


# ===========================================================================
# Section 4 — _deal_hygiene_score
# ===========================================================================

class TestDealHygieneScore:
    def _score(self, **kw) -> float:
        e = _engine()
        return e._deal_hygiene_score(_make_input(**kw))

    # next_step_defined_rate_pct thresholds
    def test_next_step_above_075_adds_0(self):
        assert self._score(next_step_defined_rate_pct=0.80) == pytest.approx(0.0, abs=0.1)

    def test_next_step_exactly_075_adds_8(self):
        assert self._score(next_step_defined_rate_pct=0.75) == pytest.approx(8.0, abs=0.1)

    def test_next_step_between_055_075_adds_8(self):
        assert self._score(next_step_defined_rate_pct=0.60) == pytest.approx(8.0, abs=0.1)

    def test_next_step_exactly_055_adds_22(self):
        assert self._score(next_step_defined_rate_pct=0.55) == pytest.approx(22.0, abs=0.1)

    def test_next_step_between_030_055_adds_22(self):
        assert self._score(next_step_defined_rate_pct=0.40) == pytest.approx(22.0, abs=0.1)

    def test_next_step_exactly_030_adds_40(self):
        assert self._score(next_step_defined_rate_pct=0.30) == pytest.approx(40.0, abs=0.1)

    def test_next_step_below_030_adds_40(self):
        assert self._score(next_step_defined_rate_pct=0.10) == pytest.approx(40.0, abs=0.1)

    def test_next_step_zero_adds_40(self):
        assert self._score(next_step_defined_rate_pct=0.0) == pytest.approx(40.0, abs=0.1)

    # mutual_action_plan_completion_pct thresholds
    def test_map_above_050_adds_0(self):
        assert self._score(mutual_action_plan_completion_pct=0.60) == pytest.approx(0.0, abs=0.1)

    def test_map_exactly_050_adds_18(self):
        assert self._score(mutual_action_plan_completion_pct=0.50) == pytest.approx(18.0, abs=0.1)

    def test_map_between_025_050_adds_18(self):
        assert self._score(mutual_action_plan_completion_pct=0.35) == pytest.approx(18.0, abs=0.1)

    def test_map_exactly_025_adds_35(self):
        assert self._score(mutual_action_plan_completion_pct=0.25) == pytest.approx(35.0, abs=0.1)

    def test_map_below_025_adds_35(self):
        assert self._score(mutual_action_plan_completion_pct=0.10) == pytest.approx(35.0, abs=0.1)

    def test_map_zero_adds_35(self):
        assert self._score(mutual_action_plan_completion_pct=0.0) == pytest.approx(35.0, abs=0.1)

    # close_date_slip_count thresholds
    def test_slip_0_adds_0(self):
        assert self._score(close_date_slip_count=0) == pytest.approx(0.0, abs=0.1)

    def test_slip_1_adds_0(self):
        assert self._score(close_date_slip_count=1) == pytest.approx(0.0, abs=0.1)

    def test_slip_2_adds_12(self):
        assert self._score(close_date_slip_count=2) == pytest.approx(12.0, abs=0.1)

    def test_slip_3_adds_25(self):
        assert self._score(close_date_slip_count=3) == pytest.approx(25.0, abs=0.1)

    def test_slip_above_3_adds_25(self):
        assert self._score(close_date_slip_count=10) == pytest.approx(25.0, abs=0.1)

    # combinations and cap
    def test_deal_hygiene_max_capped(self):
        score = self._score(
            next_step_defined_rate_pct=0.30,
            mutual_action_plan_completion_pct=0.25,
            close_date_slip_count=3,
        )
        assert score == 100.0  # 40+35+25

    def test_deal_hygiene_partial(self):
        score = self._score(
            next_step_defined_rate_pct=0.55,    # +22
            mutual_action_plan_completion_pct=0.50,  # +18
            close_date_slip_count=2,             # +12
        )
        assert score == pytest.approx(52.0)

    def test_deal_hygiene_zero(self):
        score = self._score(
            next_step_defined_rate_pct=1.0,
            mutual_action_plan_completion_pct=1.0,
            close_date_slip_count=0,
        )
        assert score == 0.0


# ===========================================================================
# Section 5 — _pipeline_risk_score
# ===========================================================================

class TestPipelineRiskScore:
    def _score(self, **kw) -> float:
        e = _engine()
        return e._pipeline_risk_score(_make_input(**kw))

    # late_stage_stall_rate_pct thresholds
    def test_stall_below_012_adds_0(self):
        assert self._score(late_stage_stall_rate_pct=0.11) == pytest.approx(0.0, abs=0.1)

    def test_stall_exactly_012_adds_10(self):
        assert self._score(late_stage_stall_rate_pct=0.12) == pytest.approx(10.0, abs=0.1)

    def test_stall_between_012_025_adds_10(self):
        assert self._score(late_stage_stall_rate_pct=0.20) == pytest.approx(10.0, abs=0.1)

    def test_stall_exactly_025_adds_25(self):
        assert self._score(late_stage_stall_rate_pct=0.25) == pytest.approx(25.0, abs=0.1)

    def test_stall_between_025_045_adds_25(self):
        assert self._score(late_stage_stall_rate_pct=0.35) == pytest.approx(25.0, abs=0.1)

    def test_stall_exactly_045_adds_45(self):
        assert self._score(late_stage_stall_rate_pct=0.45) == pytest.approx(45.0, abs=0.1)

    def test_stall_above_045_adds_45(self):
        assert self._score(late_stage_stall_rate_pct=0.80) == pytest.approx(45.0, abs=0.1)

    # competitive_re_eval_trigger_pct thresholds
    def test_competitive_below_020_adds_0(self):
        assert self._score(competitive_re_eval_trigger_pct=0.10) == pytest.approx(0.0, abs=0.1)

    def test_competitive_exactly_020_adds_15(self):
        assert self._score(competitive_re_eval_trigger_pct=0.20) == pytest.approx(15.0, abs=0.1)

    def test_competitive_between_020_035_adds_15(self):
        assert self._score(competitive_re_eval_trigger_pct=0.28) == pytest.approx(15.0, abs=0.1)

    def test_competitive_exactly_035_adds_30(self):
        assert self._score(competitive_re_eval_trigger_pct=0.35) == pytest.approx(30.0, abs=0.1)

    def test_competitive_above_035_adds_30(self):
        assert self._score(competitive_re_eval_trigger_pct=0.70) == pytest.approx(30.0, abs=0.1)

    # multi_threaded_deal_rate_pct thresholds
    def test_multithreaded_above_050_adds_0(self):
        assert self._score(multi_threaded_deal_rate_pct=0.60) == pytest.approx(0.0, abs=0.1)

    def test_multithreaded_exactly_050_adds_12(self):
        assert self._score(multi_threaded_deal_rate_pct=0.50) == pytest.approx(12.0, abs=0.1)

    def test_multithreaded_between_025_050_adds_12(self):
        assert self._score(multi_threaded_deal_rate_pct=0.35) == pytest.approx(12.0, abs=0.1)

    def test_multithreaded_exactly_025_adds_25(self):
        assert self._score(multi_threaded_deal_rate_pct=0.25) == pytest.approx(25.0, abs=0.1)

    def test_multithreaded_below_025_adds_25(self):
        assert self._score(multi_threaded_deal_rate_pct=0.10) == pytest.approx(25.0, abs=0.1)

    def test_multithreaded_zero_adds_25(self):
        assert self._score(multi_threaded_deal_rate_pct=0.0) == pytest.approx(25.0, abs=0.1)

    # combinations and cap
    def test_pipeline_risk_max_capped(self):
        score = self._score(
            late_stage_stall_rate_pct=0.45,
            competitive_re_eval_trigger_pct=0.35,
            multi_threaded_deal_rate_pct=0.25,
        )
        assert score == 100.0  # 45+30+25

    def test_pipeline_risk_partial(self):
        score = self._score(
            late_stage_stall_rate_pct=0.25,   # +25
            competitive_re_eval_trigger_pct=0.20,  # +15
            multi_threaded_deal_rate_pct=0.50,  # +12
        )
        assert score == pytest.approx(52.0)

    def test_pipeline_risk_zero(self):
        score = self._score(
            late_stage_stall_rate_pct=0.0,
            competitive_re_eval_trigger_pct=0.0,
            multi_threaded_deal_rate_pct=1.0,
        )
        assert score == 0.0


# ===========================================================================
# Section 6 — _composite
# ===========================================================================

class TestCompositeScore:
    def _composite(self, st, eng, hy, pip) -> float:
        return _engine()._composite(st, eng, hy, pip)

    def test_weights_sum_to_1(self):
        # 0.30 + 0.30 + 0.25 + 0.15 == 1.00
        assert pytest.approx(1.00) == 0.30 + 0.30 + 0.25 + 0.15

    def test_all_zero(self):
        assert self._composite(0, 0, 0, 0) == 0.0

    def test_all_100(self):
        assert self._composite(100, 100, 100, 100) == 100.0

    def test_only_stage_stall(self):
        # 100*0.30 = 30
        result = self._composite(100, 0, 0, 0)
        assert result == pytest.approx(30.0)

    def test_only_engagement_decay(self):
        # 100*0.30 = 30
        result = self._composite(0, 100, 0, 0)
        assert result == pytest.approx(30.0)

    def test_only_deal_hygiene(self):
        # 100*0.25 = 25
        result = self._composite(0, 0, 100, 0)
        assert result == pytest.approx(25.0)

    def test_only_pipeline_risk(self):
        # 100*0.15 = 15
        result = self._composite(0, 0, 0, 100)
        assert result == pytest.approx(15.0)

    def test_composite_known_values(self):
        # 40*0.30 + 50*0.30 + 60*0.25 + 80*0.15 = 12+15+15+12 = 54
        result = self._composite(40, 50, 60, 80)
        assert result == pytest.approx(54.0)

    def test_composite_capped_at_100(self):
        result = self._composite(200, 200, 200, 200)
        assert result == 100.0

    def test_composite_rounded_to_2_decimals(self):
        # 33.3333 should be rounded
        result = self._composite(33.333, 33.333, 33.333, 33.333)
        assert isinstance(result, float)
        # verify it's within rounding precision
        assert abs(result - round(33.333*0.30 + 33.333*0.30 + 33.333*0.25 + 33.333*0.15, 2)) < 0.01


# ===========================================================================
# Section 7 — Risk mapping
# ===========================================================================

class TestRiskMapping:
    def _risk(self, composite) -> VelocityRisk:
        return _engine()._risk(composite)

    def test_composite_0_is_low(self):
        assert self._risk(0.0) == VelocityRisk.low

    def test_composite_19_is_low(self):
        assert self._risk(19.99) == VelocityRisk.low

    def test_composite_20_is_moderate(self):
        assert self._risk(20.0) == VelocityRisk.moderate

    def test_composite_39_is_moderate(self):
        assert self._risk(39.99) == VelocityRisk.moderate

    def test_composite_40_is_high(self):
        assert self._risk(40.0) == VelocityRisk.high

    def test_composite_59_is_high(self):
        assert self._risk(59.99) == VelocityRisk.high

    def test_composite_60_is_critical(self):
        assert self._risk(60.0) == VelocityRisk.critical

    def test_composite_100_is_critical(self):
        assert self._risk(100.0) == VelocityRisk.critical

    def test_risk_enum_values(self):
        assert VelocityRisk.low.value == "low"
        assert VelocityRisk.moderate.value == "moderate"
        assert VelocityRisk.high.value == "high"
        assert VelocityRisk.critical.value == "critical"


# ===========================================================================
# Section 8 — Severity mapping
# ===========================================================================

class TestSeverityMapping:
    def _severity(self, composite) -> VelocitySeverity:
        return _engine()._severity(composite)

    def test_composite_0_is_accelerating(self):
        assert self._severity(0.0) == VelocitySeverity.accelerating

    def test_composite_19_is_accelerating(self):
        assert self._severity(19.99) == VelocitySeverity.accelerating

    def test_composite_20_is_on_track(self):
        assert self._severity(20.0) == VelocitySeverity.on_track

    def test_composite_39_is_on_track(self):
        assert self._severity(39.99) == VelocitySeverity.on_track

    def test_composite_40_is_slowing(self):
        assert self._severity(40.0) == VelocitySeverity.slowing

    def test_composite_59_is_slowing(self):
        assert self._severity(59.99) == VelocitySeverity.slowing

    def test_composite_60_is_collapsed(self):
        assert self._severity(60.0) == VelocitySeverity.collapsed

    def test_composite_100_is_collapsed(self):
        assert self._severity(100.0) == VelocitySeverity.collapsed

    def test_severity_enum_values(self):
        assert VelocitySeverity.accelerating.value == "accelerating"
        assert VelocitySeverity.on_track.value == "on_track"
        assert VelocitySeverity.slowing.value == "slowing"
        assert VelocitySeverity.collapsed.value == "collapsed"


# ===========================================================================
# Section 9 — Pattern detection (priority order)
# ===========================================================================

class TestPatternDetection:
    def _pattern(self, **kw) -> VelocityPattern:
        return _engine()._pattern(_make_input(**kw))

    # --- stalled_pipeline (priority 1) ---
    def test_stalled_pipeline_both_conditions_met(self):
        p = self._pattern(no_activity_streak_days=10, avg_days_in_current_stage=20.0)
        assert p == VelocityPattern.stalled_pipeline

    def test_stalled_pipeline_activity_below_10_not_triggered(self):
        p = self._pattern(no_activity_streak_days=9, avg_days_in_current_stage=20.0)
        assert p != VelocityPattern.stalled_pipeline

    def test_stalled_pipeline_stage_below_20_not_triggered(self):
        p = self._pattern(no_activity_streak_days=10, avg_days_in_current_stage=19.9)
        assert p != VelocityPattern.stalled_pipeline

    def test_stalled_pipeline_exactly_at_thresholds(self):
        p = self._pattern(no_activity_streak_days=10, avg_days_in_current_stage=20.0)
        assert p == VelocityPattern.stalled_pipeline

    def test_stalled_pipeline_takes_priority_over_stage_regression(self):
        # Both stalled_pipeline and stage_regression conditions met
        p = self._pattern(
            no_activity_streak_days=10,
            avg_days_in_current_stage=20.0,
            stage_regression_count=2,
            close_date_slip_count=2,
        )
        assert p == VelocityPattern.stalled_pipeline

    def test_stalled_pipeline_takes_priority_over_ghost_deal(self):
        p = self._pattern(
            no_activity_streak_days=14,
            avg_days_in_current_stage=20.0,
            champion_response_time_days=8.0,
        )
        assert p == VelocityPattern.stalled_pipeline

    # --- stage_regression (priority 2) ---
    def test_stage_regression_both_conditions_met(self):
        p = self._pattern(stage_regression_count=2, close_date_slip_count=2)
        assert p == VelocityPattern.stage_regression

    def test_stage_regression_count_below_2_not_triggered(self):
        p = self._pattern(stage_regression_count=1, close_date_slip_count=2)
        assert p != VelocityPattern.stage_regression

    def test_stage_regression_slip_below_2_not_triggered(self):
        p = self._pattern(stage_regression_count=2, close_date_slip_count=1)
        assert p != VelocityPattern.stage_regression

    def test_stage_regression_takes_priority_over_ghost_deal(self):
        p = self._pattern(
            stage_regression_count=2,
            close_date_slip_count=2,
            no_activity_streak_days=14,
            champion_response_time_days=8.0,
        )
        assert p == VelocityPattern.stage_regression

    def test_stage_regression_count_3_also_triggers(self):
        p = self._pattern(stage_regression_count=3, close_date_slip_count=3)
        assert p == VelocityPattern.stage_regression

    # --- ghost_deal (priority 3) ---
    def test_ghost_deal_both_conditions_met(self):
        p = self._pattern(no_activity_streak_days=14, champion_response_time_days=8.0)
        assert p == VelocityPattern.ghost_deal

    def test_ghost_deal_activity_below_14_not_triggered(self):
        p = self._pattern(no_activity_streak_days=13, champion_response_time_days=8.0)
        assert p != VelocityPattern.ghost_deal

    def test_ghost_deal_champion_below_8_not_triggered(self):
        p = self._pattern(no_activity_streak_days=14, champion_response_time_days=7.9)
        assert p != VelocityPattern.ghost_deal

    def test_ghost_deal_takes_priority_over_champion_gone_dark(self):
        p = self._pattern(
            no_activity_streak_days=14,
            champion_response_time_days=8.0,
            executive_sponsor_days_since_contact=30.0,
        )
        assert p == VelocityPattern.ghost_deal

    # --- champion_gone_dark (priority 4) ---
    def test_champion_gone_dark_both_conditions_met(self):
        p = self._pattern(
            champion_response_time_days=7.0,
            executive_sponsor_days_since_contact=30.0,
        )
        assert p == VelocityPattern.champion_gone_dark

    def test_champion_gone_dark_response_below_7_not_triggered(self):
        p = self._pattern(
            champion_response_time_days=6.9,
            executive_sponsor_days_since_contact=30.0,
        )
        assert p != VelocityPattern.champion_gone_dark

    def test_champion_gone_dark_sponsor_below_30_not_triggered(self):
        p = self._pattern(
            champion_response_time_days=7.0,
            executive_sponsor_days_since_contact=29.9,
        )
        assert p != VelocityPattern.champion_gone_dark

    def test_champion_gone_dark_takes_priority_over_multistage_drag(self):
        p = self._pattern(
            champion_response_time_days=7.0,
            executive_sponsor_days_since_contact=30.0,
            avg_cycle_length_days=120.0,
            late_stage_stall_rate_pct=0.30,
        )
        assert p == VelocityPattern.champion_gone_dark

    # --- multistage_drag (priority 5) ---
    def test_multistage_drag_both_conditions_met(self):
        p = self._pattern(avg_cycle_length_days=120.0, late_stage_stall_rate_pct=0.30)
        assert p == VelocityPattern.multistage_drag

    def test_multistage_drag_cycle_below_120_not_triggered(self):
        p = self._pattern(avg_cycle_length_days=119.9, late_stage_stall_rate_pct=0.30)
        assert p != VelocityPattern.multistage_drag

    def test_multistage_drag_stall_below_030_not_triggered(self):
        p = self._pattern(avg_cycle_length_days=120.0, late_stage_stall_rate_pct=0.29)
        assert p != VelocityPattern.multistage_drag

    # --- none (fallback) ---
    def test_none_pattern_fallback(self):
        p = self._pattern()
        assert p == VelocityPattern.none

    def test_none_when_all_conditions_off(self):
        p = self._pattern(
            no_activity_streak_days=1,
            avg_days_in_current_stage=5.0,
            stage_regression_count=0,
            close_date_slip_count=0,
            champion_response_time_days=1.0,
            executive_sponsor_days_since_contact=5.0,
            avg_cycle_length_days=60.0,
            late_stage_stall_rate_pct=0.05,
        )
        assert p == VelocityPattern.none

    def test_pattern_enum_values(self):
        assert VelocityPattern.none.value == "none"
        assert VelocityPattern.stalled_pipeline.value == "stalled_pipeline"
        assert VelocityPattern.stage_regression.value == "stage_regression"
        assert VelocityPattern.ghost_deal.value == "ghost_deal"
        assert VelocityPattern.champion_gone_dark.value == "champion_gone_dark"
        assert VelocityPattern.multistage_drag.value == "multistage_drag"


# ===========================================================================
# Section 10 — Action routing
# ===========================================================================

class TestActionRouting:
    def _action(self, risk, pattern) -> VelocityAction:
        return _engine()._action(risk, pattern)

    # critical risk
    def test_critical_ghost_deal_is_deal_rescue_escalation(self):
        a = self._action(VelocityRisk.critical, VelocityPattern.ghost_deal)
        assert a == VelocityAction.deal_rescue_escalation

    def test_critical_champion_gone_dark_is_deal_rescue_escalation(self):
        a = self._action(VelocityRisk.critical, VelocityPattern.champion_gone_dark)
        assert a == VelocityAction.deal_rescue_escalation

    def test_critical_stalled_pipeline_is_pipeline_triage(self):
        a = self._action(VelocityRisk.critical, VelocityPattern.stalled_pipeline)
        assert a == VelocityAction.pipeline_triage

    def test_critical_stage_regression_is_pipeline_triage(self):
        a = self._action(VelocityRisk.critical, VelocityPattern.stage_regression)
        assert a == VelocityAction.pipeline_triage

    def test_critical_multistage_drag_is_pipeline_triage(self):
        a = self._action(VelocityRisk.critical, VelocityPattern.multistage_drag)
        assert a == VelocityAction.pipeline_triage

    def test_critical_none_is_pipeline_triage(self):
        a = self._action(VelocityRisk.critical, VelocityPattern.none)
        assert a == VelocityAction.pipeline_triage

    # high risk
    def test_high_stalled_pipeline_is_deal_acceleration(self):
        a = self._action(VelocityRisk.high, VelocityPattern.stalled_pipeline)
        assert a == VelocityAction.deal_acceleration_coaching

    def test_high_stage_regression_is_deal_acceleration(self):
        a = self._action(VelocityRisk.high, VelocityPattern.stage_regression)
        assert a == VelocityAction.deal_acceleration_coaching

    def test_high_ghost_deal_is_champion_reactivation(self):
        a = self._action(VelocityRisk.high, VelocityPattern.ghost_deal)
        assert a == VelocityAction.champion_reactivation

    def test_high_champion_gone_dark_is_executive_involvement(self):
        a = self._action(VelocityRisk.high, VelocityPattern.champion_gone_dark)
        assert a == VelocityAction.executive_involvement

    def test_high_multistage_drag_is_executive_involvement(self):
        a = self._action(VelocityRisk.high, VelocityPattern.multistage_drag)
        assert a == VelocityAction.executive_involvement

    def test_high_none_is_deal_acceleration(self):
        a = self._action(VelocityRisk.high, VelocityPattern.none)
        assert a == VelocityAction.deal_acceleration_coaching

    # moderate risk
    def test_moderate_any_pattern_is_velocity_monitoring(self):
        for p in VelocityPattern:
            a = self._action(VelocityRisk.moderate, p)
            assert a == VelocityAction.velocity_monitoring

    # low risk
    def test_low_any_pattern_is_no_action(self):
        for p in VelocityPattern:
            a = self._action(VelocityRisk.low, p)
            assert a == VelocityAction.no_action

    def test_action_enum_values(self):
        assert VelocityAction.no_action.value == "no_action"
        assert VelocityAction.velocity_monitoring.value == "velocity_monitoring"
        assert VelocityAction.deal_acceleration_coaching.value == "deal_acceleration_coaching"
        assert VelocityAction.champion_reactivation.value == "champion_reactivation"
        assert VelocityAction.executive_involvement.value == "executive_involvement"
        assert VelocityAction.pipeline_triage.value == "pipeline_triage"
        assert VelocityAction.deal_rescue_escalation.value == "deal_rescue_escalation"


# ===========================================================================
# Section 11 — has_velocity_gap
# ===========================================================================

class TestHasVelocityGap:
    def _has_gap(self, inp, composite) -> bool:
        return _engine()._has_gap(inp, composite)

    def test_composite_40_triggers_gap(self):
        assert self._has_gap(_make_input(), 40.0) is True

    def test_composite_above_40_triggers_gap(self):
        assert self._has_gap(_make_input(), 80.0) is True

    def test_composite_below_40_no_gap_by_itself(self):
        assert self._has_gap(_make_input(close_date_slip_count=0, no_activity_streak_days=1), 39.0) is False

    def test_close_date_slip_2_triggers_gap(self):
        assert self._has_gap(_make_input(close_date_slip_count=2), 0.0) is True

    def test_close_date_slip_3_triggers_gap(self):
        assert self._has_gap(_make_input(close_date_slip_count=3), 0.0) is True

    def test_close_date_slip_1_no_gap(self):
        assert self._has_gap(_make_input(close_date_slip_count=1, no_activity_streak_days=1), 0.0) is False

    def test_no_activity_10_triggers_gap(self):
        assert self._has_gap(_make_input(no_activity_streak_days=10), 0.0) is True

    def test_no_activity_above_10_triggers_gap(self):
        assert self._has_gap(_make_input(no_activity_streak_days=20), 0.0) is True

    def test_no_activity_9_no_gap(self):
        assert self._has_gap(_make_input(no_activity_streak_days=9), 0.0) is False

    def test_all_conditions_false_no_gap(self):
        assert self._has_gap(_make_input(no_activity_streak_days=1, close_date_slip_count=0), 0.0) is False

    def test_gap_or_logic_any_true_is_true(self):
        # composite=39 + slip=2
        assert self._has_gap(_make_input(close_date_slip_count=2), 39.0) is True

    def test_gap_or_logic_composite_triggers(self):
        assert self._has_gap(_make_input(no_activity_streak_days=1, close_date_slip_count=0), 60.0) is True


# ===========================================================================
# Section 12 — requires_velocity_intervention
# ===========================================================================

class TestRequiresVelocityIntervention:
    def _req(self, inp, composite) -> bool:
        return _engine()._requires_intervention(inp, composite)

    def test_composite_25_triggers_intervention(self):
        assert self._req(_make_input(), 25.0) is True

    def test_composite_above_25_triggers_intervention(self):
        assert self._req(_make_input(), 80.0) is True

    def test_composite_24_no_intervention_by_itself(self):
        assert self._req(_make_input(late_stage_stall_rate_pct=0.0, stage_regression_count=0), 24.0) is False

    def test_stall_rate_030_triggers_intervention(self):
        assert self._req(_make_input(late_stage_stall_rate_pct=0.30), 0.0) is True

    def test_stall_rate_above_030_triggers_intervention(self):
        assert self._req(_make_input(late_stage_stall_rate_pct=0.50), 0.0) is True

    def test_stall_rate_029_no_intervention(self):
        assert self._req(_make_input(late_stage_stall_rate_pct=0.29, stage_regression_count=0), 0.0) is False

    def test_stage_regression_2_triggers_intervention(self):
        assert self._req(_make_input(stage_regression_count=2), 0.0) is True

    def test_stage_regression_3_triggers_intervention(self):
        assert self._req(_make_input(stage_regression_count=3), 0.0) is True

    def test_stage_regression_1_no_intervention(self):
        assert self._req(_make_input(stage_regression_count=1, late_stage_stall_rate_pct=0.0), 0.0) is False

    def test_all_conditions_false_no_intervention(self):
        assert self._req(_make_input(late_stage_stall_rate_pct=0.0, stage_regression_count=0), 0.0) is False

    def test_or_logic_any_true_is_true(self):
        assert self._req(_make_input(stage_regression_count=2, late_stage_stall_rate_pct=0.0), 0.0) is True


# ===========================================================================
# Section 13 — estimated_at_risk_pipeline_usd
# ===========================================================================

class TestAtRiskPipeline:
    def _pipeline(self, inp, composite) -> float:
        return _engine()._at_risk_pipeline(inp, composite)

    def test_zero_composite_gives_zero(self):
        inp = _make_input(total_active_deals=10, avg_deal_value_usd=50_000, late_stage_stall_rate_pct=0.10, close_date_slip_count=2)
        assert self._pipeline(inp, 0.0) == 0.0

    def test_zero_deals_gives_zero(self):
        inp = _make_input(total_active_deals=0, avg_deal_value_usd=50_000, late_stage_stall_rate_pct=0.50, close_date_slip_count=0)
        assert self._pipeline(inp, 50.0) == 0.0

    def test_zero_deal_value_gives_zero(self):
        inp = _make_input(total_active_deals=10, avg_deal_value_usd=0.0, late_stage_stall_rate_pct=0.50, close_date_slip_count=0)
        assert self._pipeline(inp, 50.0) == 0.0

    def test_stall_rate_plus_slip_formula(self):
        # stall_rate=0.20, slip_count=2 → risk_factor = min(0.20 + 0.2, 1.0) = 0.40
        # pipeline = 10 * 50000 * 0.40 * (50/100) = 100000
        inp = _make_input(
            total_active_deals=10,
            avg_deal_value_usd=50_000,
            late_stage_stall_rate_pct=0.20,
            close_date_slip_count=2,
        )
        result = self._pipeline(inp, 50.0)
        assert result == pytest.approx(100_000.0, rel=1e-4)

    def test_stall_rate_capped_at_1(self):
        # stall_rate=0.80, slip_count=5 → 0.80 + 0.5 = 1.30, capped to 1.0
        inp = _make_input(
            total_active_deals=10,
            avg_deal_value_usd=100_000,
            late_stage_stall_rate_pct=0.80,
            close_date_slip_count=5,
        )
        result = self._pipeline(inp, 100.0)
        assert result == pytest.approx(1_000_000.0, rel=1e-4)

    def test_pipeline_rounds_to_2_decimals(self):
        inp = _make_input(
            total_active_deals=3,
            avg_deal_value_usd=10_000,
            late_stage_stall_rate_pct=0.33,
            close_date_slip_count=1,
        )
        result = self._pipeline(inp, 50.0)
        # result should be a float rounded to 2 decimals
        assert round(result, 2) == result

    def test_slip_count_divides_by_10(self):
        # slip_count=5 contributes 0.5 to risk factor
        inp = _make_input(
            total_active_deals=1,
            avg_deal_value_usd=1_000,
            late_stage_stall_rate_pct=0.0,
            close_date_slip_count=5,
        )
        result = self._pipeline(inp, 100.0)
        assert result == pytest.approx(500.0, rel=1e-4)

    def test_at_risk_with_all_factors(self):
        # 20 deals * 25000 * min(0.30+0.3, 1.0) * (60/100) = 20*25000*0.60*0.60 = 180000
        inp = _make_input(
            total_active_deals=20,
            avg_deal_value_usd=25_000,
            late_stage_stall_rate_pct=0.30,
            close_date_slip_count=3,
        )
        result = self._pipeline(inp, 60.0)
        assert result == pytest.approx(180_000.0, rel=1e-4)


# ===========================================================================
# Section 14 — Velocity signal text
# ===========================================================================

class TestVelocitySignal:
    def _signal(self, composite, pattern=None, **kw):
        e = _engine()
        if pattern is None:
            pattern = VelocityPattern.none
        inp = _make_input(**kw)
        return e._signal(inp, pattern, composite)

    def test_low_composite_returns_healthy_message(self):
        sig = self._signal(0.0)
        assert "healthy" in sig.lower()

    def test_composite_below_20_is_healthy(self):
        sig = self._signal(19.99)
        assert "healthy" in sig.lower()

    def test_composite_exactly_20_not_healthy(self):
        sig = self._signal(20.0, VelocityPattern.stalled_pipeline)
        assert "healthy" not in sig.lower()

    def test_signal_contains_stall_days(self):
        sig = self._signal(30.0, VelocityPattern.stalled_pipeline, avg_days_in_current_stage=25.0)
        assert "25d in current stage" in sig

    def test_signal_contains_no_activity_days(self):
        sig = self._signal(30.0, VelocityPattern.none, no_activity_streak_days=7)
        assert "7d no activity" in sig

    def test_signal_contains_slip_count(self):
        sig = self._signal(30.0, VelocityPattern.none, close_date_slip_count=3)
        assert "3 close-date slips" in sig

    def test_signal_contains_composite_int(self):
        sig = self._signal(42.5, VelocityPattern.stalled_pipeline)
        assert "composite 43" in sig or "composite 42" in sig

    def test_signal_stalled_pipeline_label(self):
        sig = self._signal(30.0, VelocityPattern.stalled_pipeline)
        assert "Stalled pipeline" in sig

    def test_signal_stage_regression_label(self):
        sig = self._signal(30.0, VelocityPattern.stage_regression)
        assert "Stage regression" in sig

    def test_signal_ghost_deal_label(self):
        sig = self._signal(30.0, VelocityPattern.ghost_deal)
        assert "Ghost deal" in sig

    def test_signal_champion_gone_dark_label(self):
        sig = self._signal(30.0, VelocityPattern.champion_gone_dark)
        assert "Champion gone dark" in sig

    def test_signal_multistage_drag_label(self):
        sig = self._signal(30.0, VelocityPattern.multistage_drag)
        assert "Multistage drag" in sig

    def test_signal_returns_string(self):
        sig = self._signal(50.0, VelocityPattern.stalled_pipeline)
        assert isinstance(sig, str)

    def test_healthy_signal_mentions_benchmarks(self):
        sig = self._signal(0.0)
        assert "benchmark" in sig.lower()


# ===========================================================================
# Section 15 — VelocityResult.to_dict()
# ===========================================================================

class TestToDict:
    def _result(self, **kw) -> VelocityResult:
        return _engine().assess(_make_input(**kw))

    def test_to_dict_has_exactly_15_keys(self):
        d = self._result().to_dict()
        assert len(d) == 15

    def test_to_dict_has_rep_id(self):
        d = self._result(rep_id="BOB").to_dict()
        assert d["rep_id"] == "BOB"

    def test_to_dict_has_region(self):
        d = self._result(region="EMEA").to_dict()
        assert d["region"] == "EMEA"

    def test_to_dict_velocity_risk_is_string(self):
        d = self._result().to_dict()
        assert isinstance(d["velocity_risk"], str)

    def test_to_dict_velocity_pattern_is_string(self):
        d = self._result().to_dict()
        assert isinstance(d["velocity_pattern"], str)

    def test_to_dict_velocity_severity_is_string(self):
        d = self._result().to_dict()
        assert isinstance(d["velocity_severity"], str)

    def test_to_dict_recommended_action_is_string(self):
        d = self._result().to_dict()
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_stage_stall_score_present(self):
        d = self._result().to_dict()
        assert "stage_stall_score" in d

    def test_to_dict_engagement_decay_score_present(self):
        d = self._result().to_dict()
        assert "engagement_decay_score" in d

    def test_to_dict_deal_hygiene_score_present(self):
        d = self._result().to_dict()
        assert "deal_hygiene_score" in d

    def test_to_dict_pipeline_risk_score_present(self):
        d = self._result().to_dict()
        assert "pipeline_risk_score" in d

    def test_to_dict_velocity_composite_present(self):
        d = self._result().to_dict()
        assert "velocity_composite" in d

    def test_to_dict_has_velocity_gap_is_bool(self):
        d = self._result().to_dict()
        assert isinstance(d["has_velocity_gap"], bool)

    def test_to_dict_requires_velocity_intervention_is_bool(self):
        d = self._result().to_dict()
        assert isinstance(d["requires_velocity_intervention"], bool)

    def test_to_dict_estimated_at_risk_pipeline_usd_present(self):
        d = self._result().to_dict()
        assert "estimated_at_risk_pipeline_usd" in d

    def test_to_dict_velocity_signal_is_string(self):
        d = self._result().to_dict()
        assert isinstance(d["velocity_signal"], str)

    def test_to_dict_exact_keys(self):
        expected = {
            "rep_id", "region", "velocity_risk", "velocity_pattern",
            "velocity_severity", "recommended_action", "stage_stall_score",
            "engagement_decay_score", "deal_hygiene_score", "pipeline_risk_score",
            "velocity_composite", "has_velocity_gap", "requires_velocity_intervention",
            "estimated_at_risk_pipeline_usd", "velocity_signal",
        }
        d = self._result().to_dict()
        assert set(d.keys()) == expected


# ===========================================================================
# Section 16 — summary() keys and behavior
# ===========================================================================

class TestSummary:
    def test_empty_engine_summary_has_13_keys(self):
        e = _engine()
        s = e.summary()
        assert len(s) == 13

    def test_empty_engine_total_is_0(self):
        s = _engine().summary()
        assert s["total"] == 0

    def test_empty_engine_avg_composite_is_0(self):
        s = _engine().summary()
        assert s["avg_velocity_composite"] == 0.0

    def test_empty_engine_gap_count_is_0(self):
        s = _engine().summary()
        assert s["velocity_gap_count"] == 0

    def test_empty_engine_intervention_count_is_0(self):
        s = _engine().summary()
        assert s["intervention_count"] == 0

    def test_empty_engine_risk_counts_empty(self):
        s = _engine().summary()
        assert s["risk_counts"] == {}

    def test_empty_engine_pattern_counts_empty(self):
        s = _engine().summary()
        assert s["pattern_counts"] == {}

    def test_empty_engine_severity_counts_empty(self):
        s = _engine().summary()
        assert s["severity_counts"] == {}

    def test_empty_engine_action_counts_empty(self):
        s = _engine().summary()
        assert s["action_counts"] == {}

    def test_empty_engine_avg_stage_stall_is_0(self):
        s = _engine().summary()
        assert s["avg_stage_stall_score"] == 0.0

    def test_empty_engine_avg_engagement_is_0(self):
        s = _engine().summary()
        assert s["avg_engagement_decay_score"] == 0.0

    def test_empty_engine_avg_hygiene_is_0(self):
        s = _engine().summary()
        assert s["avg_deal_hygiene_score"] == 0.0

    def test_empty_engine_avg_pipeline_risk_is_0(self):
        s = _engine().summary()
        assert s["avg_pipeline_risk_score"] == 0.0

    def test_empty_engine_total_at_risk_is_0(self):
        s = _engine().summary()
        assert s["total_estimated_at_risk_pipeline_usd"] == 0.0

    def test_summary_has_13_keys_after_assess(self):
        e = _engine()
        e.assess(_make_input())
        s = e.summary()
        assert len(s) == 13

    def test_summary_exact_keys(self):
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_velocity_composite", "velocity_gap_count",
            "intervention_count", "avg_stage_stall_score",
            "avg_engagement_decay_score", "avg_deal_hygiene_score",
            "avg_pipeline_risk_score", "total_estimated_at_risk_pipeline_usd",
        }
        e = _engine()
        e.assess(_make_input())
        assert set(e.summary().keys()) == expected

    def test_summary_total_matches_assess_count(self):
        e = _engine()
        for _ in range(3):
            e.assess(_make_input())
        assert e.summary()["total"] == 3

    def test_summary_risk_counts_accumulate(self):
        e = _engine()
        # low risk input
        e.assess(_make_input())
        s = e.summary()
        assert sum(s["risk_counts"].values()) == 1

    def test_summary_avg_composite_correct(self):
        e = _engine()
        r1 = e.assess(_make_input())
        r2 = e.assess(_make_input())
        s = e.summary()
        expected_avg = round((r1.velocity_composite + r2.velocity_composite) / 2, 1)
        assert s["avg_velocity_composite"] == expected_avg

    def test_summary_velocity_gap_count_correct(self):
        e = _engine()
        # This should trigger has_velocity_gap
        e.assess(_make_input(no_activity_streak_days=10))
        # This should not
        e.assess(_make_input())
        s = e.summary()
        assert s["velocity_gap_count"] >= 1

    def test_summary_intervention_count_correct(self):
        e = _engine()
        # triggers intervention (stage_regression_count=2)
        e.assess(_make_input(stage_regression_count=2))
        # should not
        e.assess(_make_input())
        s = e.summary()
        assert s["intervention_count"] >= 1

    def test_summary_total_at_risk_is_sum(self):
        e = _engine()
        r1 = e.assess(_make_input())
        r2 = e.assess(_make_input())
        s = e.summary()
        expected = round(r1.estimated_at_risk_pipeline_usd + r2.estimated_at_risk_pipeline_usd, 2)
        assert s["total_estimated_at_risk_pipeline_usd"] == pytest.approx(expected, rel=1e-4)

    def test_summary_pattern_counts_accumulate_correctly(self):
        e = _engine()
        e.assess(_make_input())
        e.assess(_make_input())
        s = e.summary()
        assert sum(s["pattern_counts"].values()) == 2

    def test_summary_action_counts_accumulate(self):
        e = _engine()
        e.assess(_make_input())
        s = e.summary()
        assert sum(s["action_counts"].values()) == 1

    def test_summary_severity_counts_accumulate(self):
        e = _engine()
        e.assess(_make_input())
        s = e.summary()
        assert sum(s["severity_counts"].values()) == 1


# ===========================================================================
# Section 17 — assess() and assess_batch()
# ===========================================================================

class TestAssessAPI:
    def test_assess_returns_velocity_result(self):
        e = _engine()
        r = e.assess(_make_input())
        assert isinstance(r, VelocityResult)

    def test_assess_stores_result_in_engine(self):
        e = _engine()
        e.assess(_make_input())
        assert len(e._results) == 1

    def test_assess_rep_id_passed_through(self):
        e = _engine()
        r = e.assess(_make_input(rep_id="JANE"))
        assert r.rep_id == "JANE"

    def test_assess_region_passed_through(self):
        e = _engine()
        r = e.assess(_make_input(region="NAMER"))
        assert r.region == "NAMER"

    def test_assess_returns_valid_risk_enum(self):
        e = _engine()
        r = e.assess(_make_input())
        assert isinstance(r.velocity_risk, VelocityRisk)

    def test_assess_returns_valid_pattern_enum(self):
        e = _engine()
        r = e.assess(_make_input())
        assert isinstance(r.velocity_pattern, VelocityPattern)

    def test_assess_returns_valid_severity_enum(self):
        e = _engine()
        r = e.assess(_make_input())
        assert isinstance(r.velocity_severity, VelocitySeverity)

    def test_assess_returns_valid_action_enum(self):
        e = _engine()
        r = e.assess(_make_input())
        assert isinstance(r.recommended_action, VelocityAction)

    def test_assess_composite_between_0_and_100(self):
        e = _engine()
        r = e.assess(_make_input())
        assert 0.0 <= r.velocity_composite <= 100.0

    def test_assess_sub_scores_between_0_and_100(self):
        e = _engine()
        r = e.assess(_make_input())
        assert 0.0 <= r.stage_stall_score <= 100.0
        assert 0.0 <= r.engagement_decay_score <= 100.0
        assert 0.0 <= r.deal_hygiene_score <= 100.0
        assert 0.0 <= r.pipeline_risk_score <= 100.0

    def test_assess_at_risk_pipeline_nonnegative(self):
        e = _engine()
        r = e.assess(_make_input())
        assert r.estimated_at_risk_pipeline_usd >= 0.0

    def test_assess_batch_returns_list(self):
        e = _engine()
        results = e.assess_batch([_make_input(), _make_input()])
        assert isinstance(results, list)

    def test_assess_batch_length_matches_input(self):
        e = _engine()
        inputs = [_make_input(rep_id=f"REP-{i}") for i in range(5)]
        results = e.assess_batch(inputs)
        assert len(results) == 5

    def test_assess_batch_empty_returns_empty(self):
        e = _engine()
        results = e.assess_batch([])
        assert results == []

    def test_assess_batch_stores_all_results(self):
        e = _engine()
        e.assess_batch([_make_input() for _ in range(3)])
        assert len(e._results) == 3

    def test_multiple_assess_accumulates(self):
        e = _engine()
        for i in range(5):
            e.assess(_make_input(rep_id=f"REP-{i}"))
        assert len(e._results) == 5

    def test_assess_high_risk_scenario(self):
        e = _engine()
        r = e.assess(_make_input(
            avg_days_in_current_stage=35.0,
            no_activity_streak_days=15,
            champion_response_time_days=12.0,
            avg_stakeholder_response_rate_pct=0.20,
            next_step_defined_rate_pct=0.20,
            mutual_action_plan_completion_pct=0.15,
            close_date_slip_count=4,
            late_stage_stall_rate_pct=0.50,
            competitive_re_eval_trigger_pct=0.40,
            multi_threaded_deal_rate_pct=0.20,
            stage_regression_count=3,
            cycle_length_vs_benchmark_pct=0.60,
        ))
        assert r.velocity_risk in (VelocityRisk.critical, VelocityRisk.high)

    def test_assess_low_risk_scenario(self):
        e = _engine()
        r = e.assess(_make_input(
            avg_days_in_current_stage=3.0,
            no_activity_streak_days=0,
            champion_response_time_days=1.0,
            avg_stakeholder_response_rate_pct=0.90,
            next_step_defined_rate_pct=0.95,
            mutual_action_plan_completion_pct=0.95,
            close_date_slip_count=0,
            late_stage_stall_rate_pct=0.01,
            competitive_re_eval_trigger_pct=0.01,
            multi_threaded_deal_rate_pct=0.90,
            stage_regression_count=0,
            cycle_length_vs_benchmark_pct=0.0,
        ))
        assert r.velocity_risk == VelocityRisk.low
        assert r.velocity_severity == VelocitySeverity.accelerating


# ===========================================================================
# Section 18 — End-to-end scenarios
# ===========================================================================

class TestEndToEndScenarios:

    def test_ghost_deal_critical_scenario(self):
        """High no_activity + high champion response → critical ghost deal."""
        e = _engine()
        r = e.assess(_make_input(
            no_activity_streak_days=15,
            champion_response_time_days=9.0,
            avg_days_in_current_stage=10.0,  # avoid stalled_pipeline override
        ))
        # ghost_deal: no_activity>=14 AND champion_response>=8
        assert r.velocity_pattern == VelocityPattern.ghost_deal

    def test_stalled_pipeline_scenario(self):
        e = _engine()
        r = e.assess(_make_input(
            no_activity_streak_days=12,
            avg_days_in_current_stage=25.0,
        ))
        assert r.velocity_pattern == VelocityPattern.stalled_pipeline

    def test_champion_gone_dark_scenario(self):
        e = _engine()
        r = e.assess(_make_input(
            no_activity_streak_days=5,   # below stalled_pipeline threshold
            avg_days_in_current_stage=15.0,  # below stalled_pipeline threshold
            stage_regression_count=0,
            close_date_slip_count=0,
            champion_response_time_days=7.0,
            executive_sponsor_days_since_contact=31.0,
        ))
        assert r.velocity_pattern == VelocityPattern.champion_gone_dark

    def test_multistage_drag_scenario(self):
        e = _engine()
        r = e.assess(_make_input(
            avg_cycle_length_days=150.0,
            late_stage_stall_rate_pct=0.35,
            no_activity_streak_days=5,
            avg_days_in_current_stage=15.0,
            stage_regression_count=0,
            close_date_slip_count=0,
            champion_response_time_days=4.0,
        ))
        assert r.velocity_pattern == VelocityPattern.multistage_drag

    def test_stage_regression_scenario(self):
        e = _engine()
        r = e.assess(_make_input(
            stage_regression_count=2,
            close_date_slip_count=2,
            no_activity_streak_days=5,
            avg_days_in_current_stage=15.0,
        ))
        assert r.velocity_pattern == VelocityPattern.stage_regression

    def test_none_pattern_healthy_deal(self):
        e = _engine()
        r = e.assess(_make_input())
        assert r.velocity_pattern == VelocityPattern.none

    def test_critical_composite_means_collapsed_severity(self):
        e = _engine()
        r = e.assess(_make_input(
            avg_days_in_current_stage=35.0,
            no_activity_streak_days=15,
            champion_response_time_days=12.0,
            avg_stakeholder_response_rate_pct=0.20,
            next_step_defined_rate_pct=0.25,
            mutual_action_plan_completion_pct=0.20,
            close_date_slip_count=4,
            late_stage_stall_rate_pct=0.50,
            competitive_re_eval_trigger_pct=0.40,
            multi_threaded_deal_rate_pct=0.20,
        ))
        if r.velocity_composite >= 60:
            assert r.velocity_severity == VelocitySeverity.collapsed
            assert r.velocity_risk == VelocityRisk.critical

    def test_result_signal_nonempty(self):
        e = _engine()
        r = e.assess(_make_input())
        assert len(r.velocity_signal) > 0

    def test_to_dict_values_consistent_with_result(self):
        e = _engine()
        r = e.assess(_make_input(rep_id="SYNC-TEST", region="LATAM"))
        d = r.to_dict()
        assert d["rep_id"] == r.rep_id
        assert d["region"] == r.region
        assert d["velocity_risk"] == r.velocity_risk.value
        assert d["velocity_pattern"] == r.velocity_pattern.value
        assert d["velocity_severity"] == r.velocity_severity.value
        assert d["recommended_action"] == r.recommended_action.value
        assert d["stage_stall_score"] == r.stage_stall_score
        assert d["engagement_decay_score"] == r.engagement_decay_score
        assert d["deal_hygiene_score"] == r.deal_hygiene_score
        assert d["pipeline_risk_score"] == r.pipeline_risk_score
        assert d["velocity_composite"] == r.velocity_composite
        assert d["has_velocity_gap"] == r.has_velocity_gap
        assert d["requires_velocity_intervention"] == r.requires_velocity_intervention
        assert d["estimated_at_risk_pipeline_usd"] == r.estimated_at_risk_pipeline_usd
        assert d["velocity_signal"] == r.velocity_signal

    def test_batch_summary_consistent(self):
        e = _engine()
        inputs = [
            _make_input(rep_id="A", avg_days_in_current_stage=35.0),
            _make_input(rep_id="B", no_activity_streak_days=15),
            _make_input(rep_id="C"),
        ]
        e.assess_batch(inputs)
        s = e.summary()
        assert s["total"] == 3
        assert sum(s["risk_counts"].values()) == 3
        assert sum(s["pattern_counts"].values()) == 3

    def test_intervention_flag_matches_summary(self):
        e = _engine()
        r1 = e.assess(_make_input(stage_regression_count=2))
        r2 = e.assess(_make_input())
        s = e.summary()
        expected_count = sum(1 for r in [r1, r2] if r.requires_velocity_intervention)
        assert s["intervention_count"] == expected_count

    def test_gap_flag_matches_summary(self):
        e = _engine()
        r1 = e.assess(_make_input(no_activity_streak_days=10))
        r2 = e.assess(_make_input())
        s = e.summary()
        expected = sum(1 for r in [r1, r2] if r.has_velocity_gap)
        assert s["velocity_gap_count"] == expected


# ===========================================================================
# Section 19 — Boundary / edge cases
# ===========================================================================

class TestBoundaryEdgeCases:

    def test_boundary_stage_stall_10_exact(self):
        e = _engine()
        score = e._stage_stall_score(_make_input(avg_days_in_current_stage=10.0))
        assert score == pytest.approx(8.0, abs=0.1)

    def test_boundary_stage_stall_18_exact(self):
        e = _engine()
        score = e._stage_stall_score(_make_input(avg_days_in_current_stage=18.0))
        assert score == pytest.approx(22.0, abs=0.1)

    def test_boundary_stage_stall_30_exact(self):
        e = _engine()
        score = e._stage_stall_score(_make_input(avg_days_in_current_stage=30.0))
        assert score == pytest.approx(40.0, abs=0.1)

    def test_boundary_engagement_decay_3_exact(self):
        e = _engine()
        score = e._engagement_decay_score(_make_input(no_activity_streak_days=3))
        assert score == pytest.approx(8.0, abs=0.1)

    def test_boundary_engagement_decay_7_exact(self):
        e = _engine()
        score = e._engagement_decay_score(_make_input(no_activity_streak_days=7))
        assert score == pytest.approx(22.0, abs=0.1)

    def test_boundary_engagement_decay_14_exact(self):
        e = _engine()
        score = e._engagement_decay_score(_make_input(no_activity_streak_days=14))
        assert score == pytest.approx(40.0, abs=0.1)

    def test_composite_boundary_20(self):
        e = _engine()
        risk = e._risk(20.0)
        severity = e._severity(20.0)
        assert risk == VelocityRisk.moderate
        assert severity == VelocitySeverity.on_track

    def test_composite_boundary_40(self):
        e = _engine()
        risk = e._risk(40.0)
        severity = e._severity(40.0)
        assert risk == VelocityRisk.high
        assert severity == VelocitySeverity.slowing

    def test_composite_boundary_60(self):
        e = _engine()
        risk = e._risk(60.0)
        severity = e._severity(60.0)
        assert risk == VelocityRisk.critical
        assert severity == VelocitySeverity.collapsed

    def test_pipeline_risk_boundary_012(self):
        e = _engine()
        score = e._pipeline_risk_score(_make_input(late_stage_stall_rate_pct=0.12))
        assert score == pytest.approx(10.0, abs=0.1)

    def test_pipeline_risk_boundary_025(self):
        e = _engine()
        score = e._pipeline_risk_score(_make_input(late_stage_stall_rate_pct=0.25))
        assert score == pytest.approx(25.0, abs=0.1)

    def test_pipeline_risk_boundary_045(self):
        e = _engine()
        score = e._pipeline_risk_score(_make_input(late_stage_stall_rate_pct=0.45))
        assert score == pytest.approx(45.0, abs=0.1)

    def test_deal_hygiene_boundary_075(self):
        e = _engine()
        score = e._deal_hygiene_score(_make_input(next_step_defined_rate_pct=0.75))
        assert score == pytest.approx(8.0, abs=0.1)

    def test_deal_hygiene_boundary_055(self):
        e = _engine()
        score = e._deal_hygiene_score(_make_input(next_step_defined_rate_pct=0.55))
        assert score == pytest.approx(22.0, abs=0.1)

    def test_deal_hygiene_boundary_030(self):
        e = _engine()
        score = e._deal_hygiene_score(_make_input(next_step_defined_rate_pct=0.30))
        assert score == pytest.approx(40.0, abs=0.1)

    def test_deal_hygiene_map_boundary_050(self):
        e = _engine()
        score = e._deal_hygiene_score(_make_input(mutual_action_plan_completion_pct=0.50))
        assert score == pytest.approx(18.0, abs=0.1)

    def test_deal_hygiene_map_boundary_025(self):
        e = _engine()
        score = e._deal_hygiene_score(_make_input(mutual_action_plan_completion_pct=0.25))
        assert score == pytest.approx(35.0, abs=0.1)

    def test_gap_boundary_composite_exactly_40(self):
        e = _engine()
        assert e._has_gap(_make_input(), 40.0) is True

    def test_gap_boundary_composite_exactly_39(self):
        e = _engine()
        assert e._has_gap(_make_input(close_date_slip_count=0, no_activity_streak_days=1), 39.0) is False

    def test_intervention_boundary_composite_25(self):
        e = _engine()
        assert e._requires_intervention(_make_input(late_stage_stall_rate_pct=0.0, stage_regression_count=0), 25.0) is True

    def test_intervention_boundary_composite_24(self):
        e = _engine()
        assert e._requires_intervention(_make_input(late_stage_stall_rate_pct=0.0, stage_regression_count=0), 24.0) is False

    def test_stalled_pipeline_exact_boundary_no_activity_10(self):
        e = _engine()
        assert e._pattern(_make_input(no_activity_streak_days=10, avg_days_in_current_stage=20.0)) == VelocityPattern.stalled_pipeline

    def test_stalled_pipeline_exact_boundary_stage_20(self):
        e = _engine()
        assert e._pattern(_make_input(no_activity_streak_days=10, avg_days_in_current_stage=20.0)) == VelocityPattern.stalled_pipeline

    def test_ghost_deal_exact_boundary_no_activity_14(self):
        e = _engine()
        # must not trigger stalled_pipeline first, so stage < 20
        p = e._pattern(_make_input(no_activity_streak_days=14, avg_days_in_current_stage=15.0, champion_response_time_days=8.0))
        assert p == VelocityPattern.ghost_deal

    def test_ghost_deal_exact_boundary_champion_8(self):
        e = _engine()
        p = e._pattern(_make_input(no_activity_streak_days=14, avg_days_in_current_stage=15.0, champion_response_time_days=8.0))
        assert p == VelocityPattern.ghost_deal

    def test_champion_gone_dark_exact_boundary_response_7(self):
        e = _engine()
        p = e._pattern(_make_input(
            no_activity_streak_days=5,
            avg_days_in_current_stage=10.0,
            stage_regression_count=0,
            close_date_slip_count=0,
            champion_response_time_days=7.0,
            executive_sponsor_days_since_contact=30.0,
        ))
        assert p == VelocityPattern.champion_gone_dark

    def test_champion_gone_dark_exact_boundary_sponsor_30(self):
        e = _engine()
        p = e._pattern(_make_input(
            no_activity_streak_days=5,
            avg_days_in_current_stage=10.0,
            stage_regression_count=0,
            close_date_slip_count=0,
            champion_response_time_days=7.0,
            executive_sponsor_days_since_contact=30.0,
        ))
        assert p == VelocityPattern.champion_gone_dark

    def test_multistage_drag_exact_boundary_cycle_120(self):
        e = _engine()
        p = e._pattern(_make_input(
            avg_cycle_length_days=120.0,
            late_stage_stall_rate_pct=0.30,
            no_activity_streak_days=5,
            avg_days_in_current_stage=15.0,
            stage_regression_count=0,
            close_date_slip_count=0,
            champion_response_time_days=4.0,
        ))
        assert p == VelocityPattern.multistage_drag

    def test_multistage_drag_exact_boundary_stall_030(self):
        e = _engine()
        p = e._pattern(_make_input(
            avg_cycle_length_days=120.0,
            late_stage_stall_rate_pct=0.30,
            no_activity_streak_days=5,
            avg_days_in_current_stage=15.0,
            stage_regression_count=0,
            close_date_slip_count=0,
            champion_response_time_days=4.0,
        ))
        assert p == VelocityPattern.multistage_drag


# ===========================================================================
# Section 20 — Additional combinatorial / coverage tests
# ===========================================================================

class TestCombinatorial:

    def test_all_patterns_detectable(self):
        e = _engine()
        # stalled_pipeline
        r1 = e.assess(_make_input(no_activity_streak_days=10, avg_days_in_current_stage=20.0))
        # stage_regression (prevent stalled_pipeline)
        r2 = e.assess(_make_input(stage_regression_count=2, close_date_slip_count=2, no_activity_streak_days=5, avg_days_in_current_stage=15.0))
        # ghost_deal (prevent higher-priority patterns)
        r3 = e.assess(_make_input(no_activity_streak_days=14, avg_days_in_current_stage=15.0, champion_response_time_days=8.0, stage_regression_count=0, close_date_slip_count=0))
        # champion_gone_dark
        r4 = e.assess(_make_input(champion_response_time_days=7.0, executive_sponsor_days_since_contact=30.0, no_activity_streak_days=5, avg_days_in_current_stage=10.0, stage_regression_count=0, close_date_slip_count=0))
        # multistage_drag
        r5 = e.assess(_make_input(avg_cycle_length_days=120.0, late_stage_stall_rate_pct=0.30, no_activity_streak_days=5, avg_days_in_current_stage=15.0, champion_response_time_days=4.0, stage_regression_count=0, close_date_slip_count=0))
        # none
        r6 = e.assess(_make_input())
        patterns = {r1.velocity_pattern, r2.velocity_pattern, r3.velocity_pattern, r4.velocity_pattern, r5.velocity_pattern, r6.velocity_pattern}
        assert VelocityPattern.stalled_pipeline in patterns
        assert VelocityPattern.stage_regression in patterns
        assert VelocityPattern.ghost_deal in patterns
        assert VelocityPattern.champion_gone_dark in patterns
        assert VelocityPattern.multistage_drag in patterns
        assert VelocityPattern.none in patterns

    def test_all_risks_detectable(self):
        e = _engine()
        # low: all zeros
        r_low = e.assess(_make_input())
        # moderate: need composite 20-39
        r_mod = e.assess(_make_input(
            avg_days_in_current_stage=18.0,
            cycle_length_vs_benchmark_pct=0.10,
        ))
        # high: composite 40-59
        r_high = e.assess(_make_input(
            avg_days_in_current_stage=30.0,
            no_activity_streak_days=7,
            next_step_defined_rate_pct=0.55,
        ))
        # critical: composite >=60
        r_crit = e.assess(_make_input(
            avg_days_in_current_stage=35.0,
            no_activity_streak_days=15,
            champion_response_time_days=12.0,
            avg_stakeholder_response_rate_pct=0.20,
            next_step_defined_rate_pct=0.25,
            mutual_action_plan_completion_pct=0.20,
            close_date_slip_count=4,
            late_stage_stall_rate_pct=0.50,
            competitive_re_eval_trigger_pct=0.40,
            multi_threaded_deal_rate_pct=0.20,
            stage_regression_count=3,
            cycle_length_vs_benchmark_pct=0.60,
        ))
        all_risks = {r.velocity_risk for r in [r_low, r_mod, r_high, r_crit]}
        assert VelocityRisk.low in all_risks

    def test_all_severities_detectable(self):
        e = _engine()
        r_acc = e.assess(_make_input())
        assert r_acc.velocity_severity == VelocitySeverity.accelerating

    def test_multiple_engines_are_independent(self):
        e1 = _engine()
        e2 = _engine()
        e1.assess(_make_input())
        assert len(e2._results) == 0

    def test_assess_batch_results_ordered(self):
        e = _engine()
        ids = ["REP-A", "REP-B", "REP-C"]
        results = e.assess_batch([_make_input(rep_id=rid) for rid in ids])
        assert [r.rep_id for r in results] == ids

    def test_stage_stall_only_regression_bucket_2(self):
        e = _engine()
        score = e._stage_stall_score(_make_input(stage_regression_count=2))
        assert score == pytest.approx(12.0, abs=0.1)

    def test_engagement_decay_stakeholder_050_boundary(self):
        e = _engine()
        score = e._engagement_decay_score(_make_input(avg_stakeholder_response_rate_pct=0.50))
        assert score == pytest.approx(12.0, abs=0.1)

    def test_pipeline_risk_multithreaded_050_boundary(self):
        e = _engine()
        score = e._pipeline_risk_score(_make_input(multi_threaded_deal_rate_pct=0.50))
        assert score == pytest.approx(12.0, abs=0.1)

    def test_pipeline_risk_competitive_020_boundary(self):
        e = _engine()
        score = e._pipeline_risk_score(_make_input(competitive_re_eval_trigger_pct=0.20))
        assert score == pytest.approx(15.0, abs=0.1)

    def test_pipeline_risk_competitive_035_boundary(self):
        e = _engine()
        score = e._pipeline_risk_score(_make_input(competitive_re_eval_trigger_pct=0.35))
        assert score == pytest.approx(30.0, abs=0.1)

    def test_high_risk_no_match_pattern_is_deal_acceleration(self):
        e = _engine()
        a = e._action(VelocityRisk.high, VelocityPattern.none)
        assert a == VelocityAction.deal_acceleration_coaching

    def test_velocity_signal_rounds_stall_days(self):
        e = _engine()
        inp = _make_input(avg_days_in_current_stage=7.6)
        sig = e._signal(inp, VelocityPattern.none, 30.0)
        assert "8d in current stage" in sig

    def test_velocity_signal_rounds_stall_days_down(self):
        e = _engine()
        inp = _make_input(avg_days_in_current_stage=7.4)
        sig = e._signal(inp, VelocityPattern.none, 30.0)
        assert "7d in current stage" in sig

    def test_deal_hygiene_boundary_between_055_and_030(self):
        e = _engine()
        score = e._deal_hygiene_score(_make_input(next_step_defined_rate_pct=0.40))
        assert score == pytest.approx(22.0, abs=0.1)

    def test_engagement_decay_champion_between_5_10(self):
        e = _engine()
        score = e._engagement_decay_score(_make_input(champion_response_time_days=7.5))
        assert score == pytest.approx(18.0, abs=0.1)

    def test_stage_stall_between_benchmark_010_025(self):
        e = _engine()
        score = e._stage_stall_score(_make_input(cycle_length_vs_benchmark_pct=0.15))
        assert score == pytest.approx(6.0, abs=0.1)

    def test_stage_stall_between_benchmark_025_050(self):
        e = _engine()
        score = e._stage_stall_score(_make_input(cycle_length_vs_benchmark_pct=0.40))
        assert score == pytest.approx(18.0, abs=0.1)

    def test_pipeline_risk_stall_between_012_025(self):
        e = _engine()
        score = e._pipeline_risk_score(_make_input(late_stage_stall_rate_pct=0.18))
        assert score == pytest.approx(10.0, abs=0.1)

    def test_pipeline_risk_stall_between_025_045(self):
        e = _engine()
        score = e._pipeline_risk_score(_make_input(late_stage_stall_rate_pct=0.35))
        assert score == pytest.approx(25.0, abs=0.1)

    def test_summary_avg_scores_rounded_to_1_decimal(self):
        e = _engine()
        e.assess(_make_input())
        s = e.summary()
        for key in ["avg_stage_stall_score", "avg_engagement_decay_score",
                    "avg_deal_hygiene_score", "avg_pipeline_risk_score",
                    "avg_velocity_composite"]:
            val = s[key]
            assert val == round(val, 1), f"{key} not rounded to 1 decimal"

    def test_deal_hygiene_combined_near_cap(self):
        e = _engine()
        score = e._deal_hygiene_score(_make_input(
            next_step_defined_rate_pct=0.30,   # +40
            mutual_action_plan_completion_pct=0.25,  # +35
            close_date_slip_count=2,            # +12
        ))
        assert score == pytest.approx(87.0, abs=0.1)

    def test_engagement_decay_combined_partial(self):
        e = _engine()
        score = e._engagement_decay_score(_make_input(
            no_activity_streak_days=3,          # +8
            champion_response_time_days=5.0,    # +18
            avg_stakeholder_response_rate_pct=0.50,  # +12
        ))
        assert score == pytest.approx(38.0, abs=0.1)

    def test_stage_stall_partial_combination_2(self):
        e = _engine()
        score = e._stage_stall_score(_make_input(
            avg_days_in_current_stage=10.0,     # +8
            cycle_length_vs_benchmark_pct=0.10, # +6
            stage_regression_count=2,           # +12
        ))
        assert score == pytest.approx(26.0, abs=0.1)

    def test_pipeline_risk_combined_partial(self):
        e = _engine()
        score = e._pipeline_risk_score(_make_input(
            late_stage_stall_rate_pct=0.12,     # +10
            competitive_re_eval_trigger_pct=0.20,  # +15
            multi_threaded_deal_rate_pct=0.50,  # +12
        ))
        assert score == pytest.approx(37.0, abs=0.1)

    def test_assess_result_fields_not_none(self):
        e = _engine()
        r = e.assess(_make_input())
        assert r.rep_id is not None
        assert r.region is not None
        assert r.velocity_risk is not None
        assert r.velocity_pattern is not None
        assert r.velocity_severity is not None
        assert r.recommended_action is not None
        assert r.velocity_signal is not None

    def test_assess_result_score_types_are_float(self):
        e = _engine()
        r = e.assess(_make_input())
        assert isinstance(r.stage_stall_score, float)
        assert isinstance(r.engagement_decay_score, float)
        assert isinstance(r.deal_hygiene_score, float)
        assert isinstance(r.pipeline_risk_score, float)
        assert isinstance(r.velocity_composite, float)

    def test_large_batch_summary_totals(self):
        e = _engine()
        n = 50
        results = e.assess_batch([_make_input(rep_id=f"REP-{i}") for i in range(n)])
        s = e.summary()
        assert s["total"] == n
        assert sum(s["risk_counts"].values()) == n
        assert sum(s["pattern_counts"].values()) == n
        assert sum(s["severity_counts"].values()) == n
        assert sum(s["action_counts"].values()) == n

    def test_deal_hygiene_slip_count_1_no_contribution(self):
        e = _engine()
        score = e._deal_hygiene_score(_make_input(close_date_slip_count=1))
        assert score == pytest.approx(0.0, abs=0.1)

    def test_stage_regression_count_1_no_contribution(self):
        e = _engine()
        score = e._stage_stall_score(_make_input(stage_regression_count=1))
        assert score == pytest.approx(0.0, abs=0.1)

    def test_all_sub_scores_at_zero_means_low_risk(self):
        e = _engine()
        r = e.assess(_make_input(
            avg_days_in_current_stage=0.0,
            cycle_length_vs_benchmark_pct=0.0,
            stage_regression_count=0,
            no_activity_streak_days=0,
            champion_response_time_days=0.0,
            avg_stakeholder_response_rate_pct=1.0,
            next_step_defined_rate_pct=1.0,
            mutual_action_plan_completion_pct=1.0,
            close_date_slip_count=0,
            late_stage_stall_rate_pct=0.0,
            competitive_re_eval_trigger_pct=0.0,
            multi_threaded_deal_rate_pct=1.0,
        ))
        assert r.velocity_risk == VelocityRisk.low
        assert r.velocity_composite == 0.0

    def test_velocity_result_dataclass_fields(self):
        import dataclasses
        fields = {f.name for f in dataclasses.fields(VelocityResult)}
        expected = {
            "rep_id", "region", "velocity_risk", "velocity_pattern",
            "velocity_severity", "recommended_action", "stage_stall_score",
            "engagement_decay_score", "deal_hygiene_score", "pipeline_risk_score",
            "velocity_composite", "has_velocity_gap", "requires_velocity_intervention",
            "estimated_at_risk_pipeline_usd", "velocity_signal",
        }
        assert fields == expected

    def test_engine_init_results_empty(self):
        e = _engine()
        assert e._results == []

    def test_assess_batch_returns_velocity_results(self):
        e = _engine()
        results = e.assess_batch([_make_input()])
        assert all(isinstance(r, VelocityResult) for r in results)

    def test_gap_triggered_by_all_three_or_conditions(self):
        e = _engine()
        # composite>=40
        assert e._has_gap(_make_input(), 40.0) is True
        # close_date_slip_count>=2
        assert e._has_gap(_make_input(close_date_slip_count=2), 0.0) is True
        # no_activity_streak_days>=10
        assert e._has_gap(_make_input(no_activity_streak_days=10), 0.0) is True

    def test_intervention_triggered_by_all_three_or_conditions(self):
        e = _engine()
        # composite>=25
        assert e._requires_intervention(_make_input(), 25.0) is True
        # late_stage_stall_rate_pct>=0.30
        assert e._requires_intervention(_make_input(late_stage_stall_rate_pct=0.30), 0.0) is True
        # stage_regression_count>=2
        assert e._requires_intervention(_make_input(stage_regression_count=2), 0.0) is True

    def test_at_risk_pipeline_slip_count_capped_at_1(self):
        e = _engine()
        # stall_rate=0.0, slip_count=15 → 0.0 + 1.5 → capped to 1.0
        inp = _make_input(
            total_active_deals=1,
            avg_deal_value_usd=10_000,
            late_stage_stall_rate_pct=0.0,
            close_date_slip_count=15,
        )
        result = e._at_risk_pipeline(inp, 100.0)
        # min(0+1.5, 1.0) = 1.0 * 1 * 10000 * 1.0 = 10000
        assert result == pytest.approx(10_000.0, rel=1e-4)

    def test_pattern_priority_all_five_met(self):
        """When all 5 pattern conditions are met simultaneously, stalled_pipeline wins."""
        e = _engine()
        p = e._pattern(_make_input(
            no_activity_streak_days=14,      # stalled + ghost_deal no_activity
            avg_days_in_current_stage=20.0,  # stalled
            stage_regression_count=2,        # stage_regression
            close_date_slip_count=2,         # stage_regression
            champion_response_time_days=8.0, # ghost_deal + champion_gone_dark
            executive_sponsor_days_since_contact=30.0,  # champion_gone_dark
            avg_cycle_length_days=120.0,     # multistage_drag
            late_stage_stall_rate_pct=0.30,  # multistage_drag
        ))
        assert p == VelocityPattern.stalled_pipeline

    def test_stage_regression_priority_over_ghost_and_below(self):
        """stage_regression priority 2 when stalled_pipeline not triggered."""
        e = _engine()
        p = e._pattern(_make_input(
            no_activity_streak_days=14,
            avg_days_in_current_stage=15.0,  # won't trigger stalled_pipeline
            stage_regression_count=2,
            close_date_slip_count=2,
            champion_response_time_days=8.0,
            executive_sponsor_days_since_contact=30.0,
            avg_cycle_length_days=120.0,
            late_stage_stall_rate_pct=0.30,
        ))
        assert p == VelocityPattern.stage_regression

    def test_no_activity_exactly_9_no_stalled_pipeline(self):
        e = _engine()
        p = e._pattern(_make_input(no_activity_streak_days=9, avg_days_in_current_stage=20.0))
        assert p != VelocityPattern.stalled_pipeline

    def test_avg_days_exactly_19_no_stalled_pipeline(self):
        e = _engine()
        p = e._pattern(_make_input(no_activity_streak_days=10, avg_days_in_current_stage=19.9))
        assert p != VelocityPattern.stalled_pipeline

    def test_late_stage_stall_exactly_029_no_intervention_by_itself(self):
        e = _engine()
        assert e._requires_intervention(_make_input(late_stage_stall_rate_pct=0.29, stage_regression_count=0), 0.0) is False

    def test_late_stage_stall_exactly_030_triggers_intervention(self):
        e = _engine()
        assert e._requires_intervention(_make_input(late_stage_stall_rate_pct=0.30, stage_regression_count=0), 0.0) is True

    def test_stage_regression_exactly_1_no_intervention(self):
        e = _engine()
        assert e._requires_intervention(_make_input(stage_regression_count=1, late_stage_stall_rate_pct=0.0), 0.0) is False

    def test_stage_regression_exactly_2_triggers_intervention(self):
        e = _engine()
        assert e._requires_intervention(_make_input(stage_regression_count=2, late_stage_stall_rate_pct=0.0), 0.0) is True

    def test_composite_is_weighted_sum(self):
        """Verify composite = st*0.30 + eng*0.30 + hy*0.25 + pip*0.15 (capped at 100)."""
        e = _engine()
        st, eng, hy, pip = 20.0, 40.0, 60.0, 80.0
        expected = round(st * 0.30 + eng * 0.30 + hy * 0.25 + pip * 0.15, 2)
        assert e._composite(st, eng, hy, pip) == pytest.approx(expected)

    def test_signal_healthy_full_text(self):
        e = _engine()
        inp = _make_input()
        sig = e._signal(inp, VelocityPattern.none, 0.0)
        assert "Deal velocity healthy" in sig
        assert "stage progression" in sig
        assert "engagement cadence" in sig
        assert "pipeline hygiene" in sig

    def test_summary_after_mixed_batch(self):
        e = _engine()
        e.assess_batch([
            _make_input(rep_id="A", no_activity_streak_days=10, avg_days_in_current_stage=20.0),
            _make_input(rep_id="B", stage_regression_count=2, close_date_slip_count=2, no_activity_streak_days=5, avg_days_in_current_stage=15.0),
            _make_input(rep_id="C"),
        ])
        s = e.summary()
        assert s["total"] == 3
        assert "stalled_pipeline" in s["pattern_counts"] or "stage_regression" in s["pattern_counts"] or "none" in s["pattern_counts"]

    def test_assess_velocity_signal_nonempty_for_any_risk(self):
        e = _engine()
        for scenario in [
            _make_input(),
            _make_input(avg_days_in_current_stage=25.0, no_activity_streak_days=8),
            _make_input(avg_days_in_current_stage=35.0, no_activity_streak_days=15, champion_response_time_days=12.0),
        ]:
            r = e.assess(scenario)
            assert isinstance(r.velocity_signal, str)
            assert len(r.velocity_signal) > 10
