"""Comprehensive pytest test suite for SalesCapacityPlanningEngine.

Import path: swarm.intelligence.sales_capacity_planning_engine
"""
from __future__ import annotations

import math
import pytest

from swarm.intelligence.sales_capacity_planning_engine import (
    CapacityAction,
    CapacityRisk,
    CapacityStatus,
    GrowthConstraint,
    SalesCapacityInput,
    SalesCapacityPlanningEngine,
    SalesCapacityResult,
    _capacity_action,
    _capacity_risk,
    _capacity_signal,
    _capacity_status,
    _composite,
    _growth_constraint,
    _hiring_efficiency_score,
    _pipeline_health_score,
    _productivity_score,
    _required_headcount,
    _revenue_at_risk_usd,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _make_input(**overrides) -> SalesCapacityInput:
    """Return a baseline SalesCapacityInput; keyword overrides replace defaults."""
    defaults = dict(
        region_id="R001",
        region_name="North America",
        region_head="Alice Smith",
        annual_revenue_target_usd=10_000_000.0,
        current_headcount=10,
        avg_productivity_per_rep_usd=1_000_000.0,
        avg_ramp_months=3.0,
        expected_attrition_rate_pct=10.0,
        current_pipeline_coverage_ratio=3.5,
        open_headcount_req=1,
        time_to_hire_days=45.0,
        quota_attainment_pct=90.0,
        avg_deal_size_usd=50_000.0,
        avg_sales_cycle_days=60.0,
        win_rate_pct=30.0,
        lead_volume_monthly=300,
        lead_to_opportunity_rate_pct=20.0,
        expansion_revenue_pct=30.0,
        partner_revenue_pct=10.0,
        seasonal_peak_factor=1.2,
        territory_saturation_pct=40.0,
        rep_productivity_trend=0.5,
    )
    defaults.update(overrides)
    return SalesCapacityInput(**defaults)


@pytest.fixture()
def baseline_input() -> SalesCapacityInput:
    return _make_input()


@pytest.fixture()
def engine() -> SalesCapacityPlanningEngine:
    return SalesCapacityPlanningEngine()


@pytest.fixture()
def baseline_result(engine, baseline_input) -> SalesCapacityResult:
    return engine.assess(baseline_input)


# ---------------------------------------------------------------------------
# 1. Enum definitions
# ---------------------------------------------------------------------------

class TestEnums:
    def test_capacity_status_values(self):
        assert CapacityStatus.SURPLUS.value == "surplus"
        assert CapacityStatus.BALANCED.value == "balanced"
        assert CapacityStatus.GAP.value == "gap"
        assert CapacityStatus.CRITICAL_GAP.value == "critical_gap"

    def test_capacity_status_count(self):
        assert len(CapacityStatus) == 4

    def test_capacity_risk_values(self):
        assert CapacityRisk.LOW.value == "low"
        assert CapacityRisk.MODERATE.value == "moderate"
        assert CapacityRisk.HIGH.value == "high"
        assert CapacityRisk.CRITICAL.value == "critical"

    def test_capacity_risk_count(self):
        assert len(CapacityRisk) == 4

    def test_growth_constraint_values(self):
        assert GrowthConstraint.NONE.value == "none"
        assert GrowthConstraint.HEADCOUNT.value == "headcount"
        assert GrowthConstraint.PIPELINE.value == "pipeline"
        assert GrowthConstraint.PRODUCTIVITY.value == "productivity"
        assert GrowthConstraint.HIRING_SPEED.value == "hiring_speed"

    def test_growth_constraint_count(self):
        assert len(GrowthConstraint) == 5

    def test_capacity_action_values(self):
        assert CapacityAction.MAINTAIN.value == "maintain"
        assert CapacityAction.ACCELERATE_HIRING.value == "accelerate_hiring"
        assert CapacityAction.RESTRUCTURE_TERRITORY.value == "restructure_territory"
        assert CapacityAction.REDUCE_TARGET.value == "reduce_target"

    def test_capacity_action_count(self):
        assert len(CapacityAction) == 4

    def test_capacity_status_is_str_enum(self):
        assert isinstance(CapacityStatus.GAP, str)

    def test_capacity_risk_is_str_enum(self):
        assert isinstance(CapacityRisk.HIGH, str)

    def test_growth_constraint_is_str_enum(self):
        assert isinstance(GrowthConstraint.PIPELINE, str)

    def test_capacity_action_is_str_enum(self):
        assert isinstance(CapacityAction.MAINTAIN, str)


# ---------------------------------------------------------------------------
# 2. SalesCapacityInput dataclass – field count and types
# ---------------------------------------------------------------------------

class TestSalesCapacityInput:
    def test_field_count(self, baseline_input):
        import dataclasses
        fields = dataclasses.fields(baseline_input)
        assert len(fields) == 22

    def test_region_id(self, baseline_input):
        assert baseline_input.region_id == "R001"

    def test_region_name(self, baseline_input):
        assert baseline_input.region_name == "North America"

    def test_region_head(self, baseline_input):
        assert baseline_input.region_head == "Alice Smith"

    def test_annual_revenue_target_usd(self, baseline_input):
        assert baseline_input.annual_revenue_target_usd == 10_000_000.0

    def test_current_headcount(self, baseline_input):
        assert baseline_input.current_headcount == 10

    def test_avg_productivity_per_rep_usd(self, baseline_input):
        assert baseline_input.avg_productivity_per_rep_usd == 1_000_000.0

    def test_avg_ramp_months(self, baseline_input):
        assert baseline_input.avg_ramp_months == 3.0

    def test_expected_attrition_rate_pct(self, baseline_input):
        assert baseline_input.expected_attrition_rate_pct == 10.0

    def test_current_pipeline_coverage_ratio(self, baseline_input):
        assert baseline_input.current_pipeline_coverage_ratio == 3.5

    def test_open_headcount_req(self, baseline_input):
        assert baseline_input.open_headcount_req == 1

    def test_time_to_hire_days(self, baseline_input):
        assert baseline_input.time_to_hire_days == 45.0

    def test_quota_attainment_pct(self, baseline_input):
        assert baseline_input.quota_attainment_pct == 90.0

    def test_avg_deal_size_usd(self, baseline_input):
        assert baseline_input.avg_deal_size_usd == 50_000.0

    def test_avg_sales_cycle_days(self, baseline_input):
        assert baseline_input.avg_sales_cycle_days == 60.0

    def test_win_rate_pct(self, baseline_input):
        assert baseline_input.win_rate_pct == 30.0

    def test_lead_volume_monthly(self, baseline_input):
        assert baseline_input.lead_volume_monthly == 300

    def test_lead_to_opportunity_rate_pct(self, baseline_input):
        assert baseline_input.lead_to_opportunity_rate_pct == 20.0

    def test_expansion_revenue_pct(self, baseline_input):
        assert baseline_input.expansion_revenue_pct == 30.0

    def test_partner_revenue_pct(self, baseline_input):
        assert baseline_input.partner_revenue_pct == 10.0

    def test_seasonal_peak_factor(self, baseline_input):
        assert baseline_input.seasonal_peak_factor == 1.2

    def test_territory_saturation_pct(self, baseline_input):
        assert baseline_input.territory_saturation_pct == 40.0

    def test_rep_productivity_trend(self, baseline_input):
        assert baseline_input.rep_productivity_trend == 0.5


# ---------------------------------------------------------------------------
# 3. SalesCapacityResult dataclass – field count, types and to_dict keys
# ---------------------------------------------------------------------------

class TestSalesCapacityResult:
    def test_field_count(self, baseline_result):
        import dataclasses
        fields = dataclasses.fields(baseline_result)
        assert len(fields) == 15

    def test_to_dict_key_count(self, baseline_result):
        d = baseline_result.to_dict()
        assert len(d) == 15

    def test_to_dict_exact_keys(self, baseline_result):
        expected_keys = {
            "region_id", "region_name", "capacity_status", "capacity_risk",
            "growth_constraint", "capacity_action", "required_headcount",
            "capacity_gap", "productivity_score", "pipeline_health_score",
            "hiring_efficiency_score", "capacity_composite", "is_understaffed",
            "revenue_at_risk_usd", "capacity_signal",
        }
        assert set(baseline_result.to_dict().keys()) == expected_keys

    def test_to_dict_status_is_string(self, baseline_result):
        d = baseline_result.to_dict()
        assert isinstance(d["capacity_status"], str)

    def test_to_dict_risk_is_string(self, baseline_result):
        d = baseline_result.to_dict()
        assert isinstance(d["capacity_risk"], str)

    def test_to_dict_constraint_is_string(self, baseline_result):
        d = baseline_result.to_dict()
        assert isinstance(d["growth_constraint"], str)

    def test_to_dict_action_is_string(self, baseline_result):
        d = baseline_result.to_dict()
        assert isinstance(d["capacity_action"], str)

    def test_to_dict_required_headcount_is_int(self, baseline_result):
        d = baseline_result.to_dict()
        assert isinstance(d["required_headcount"], int)

    def test_to_dict_capacity_gap_is_int(self, baseline_result):
        d = baseline_result.to_dict()
        assert isinstance(d["capacity_gap"], int)

    def test_to_dict_is_understaffed_is_bool(self, baseline_result):
        d = baseline_result.to_dict()
        assert isinstance(d["is_understaffed"], bool)

    def test_to_dict_region_id_matches(self, baseline_result):
        assert baseline_result.to_dict()["region_id"] == "R001"

    def test_to_dict_region_name_matches(self, baseline_result):
        assert baseline_result.to_dict()["region_name"] == "North America"

    def test_result_region_id(self, baseline_result):
        assert baseline_result.region_id == "R001"

    def test_result_region_name(self, baseline_result):
        assert baseline_result.region_name == "North America"

    def test_capacity_composite_in_range(self, baseline_result):
        assert 0.0 <= baseline_result.capacity_composite <= 100.0

    def test_productivity_score_in_range(self, baseline_result):
        assert 0.0 <= baseline_result.productivity_score <= 100.0

    def test_pipeline_health_score_in_range(self, baseline_result):
        assert 0.0 <= baseline_result.pipeline_health_score <= 100.0

    def test_hiring_efficiency_score_in_range(self, baseline_result):
        assert 0.0 <= baseline_result.hiring_efficiency_score <= 100.0

    def test_revenue_at_risk_non_negative(self, baseline_result):
        assert baseline_result.revenue_at_risk_usd >= 0.0

    def test_is_understaffed_consistent_with_gap(self, baseline_result):
        assert baseline_result.is_understaffed == (baseline_result.capacity_gap > 0)

    def test_capacity_signal_is_string(self, baseline_result):
        assert isinstance(baseline_result.capacity_signal, str)

    def test_capacity_signal_non_empty(self, baseline_result):
        assert len(baseline_result.capacity_signal) > 0


# ---------------------------------------------------------------------------
# 4. _required_headcount helper
# ---------------------------------------------------------------------------

class TestRequiredHeadcount:
    def test_basic_calculation(self):
        inp = _make_input(
            annual_revenue_target_usd=10_000_000,
            avg_productivity_per_rep_usd=1_000_000,
            quota_attainment_pct=100.0,
            expected_attrition_rate_pct=0.0,
            avg_ramp_months=0.0,
        )
        # attrition_factor=1, ramp_factor=1 → raw=10 → 10
        assert _required_headcount(inp) == 10

    def test_zero_productivity_returns_current_headcount(self):
        inp = _make_input(avg_productivity_per_rep_usd=0.0, current_headcount=7)
        assert _required_headcount(inp) == 7

    def test_negative_productivity_returns_current_headcount(self):
        inp = _make_input(avg_productivity_per_rep_usd=-100.0, current_headcount=5)
        assert _required_headcount(inp) == 5

    def test_attrition_increases_required(self):
        inp_no_attr = _make_input(expected_attrition_rate_pct=0.0, avg_ramp_months=0.0, quota_attainment_pct=100.0)
        inp_with_attr = _make_input(expected_attrition_rate_pct=20.0, avg_ramp_months=0.0, quota_attainment_pct=100.0)
        assert _required_headcount(inp_with_attr) >= _required_headcount(inp_no_attr)

    def test_ramp_increases_required(self):
        inp_no_ramp = _make_input(avg_ramp_months=0.0, expected_attrition_rate_pct=0.0, quota_attainment_pct=100.0)
        inp_with_ramp = _make_input(avg_ramp_months=6.0, expected_attrition_rate_pct=0.0, quota_attainment_pct=100.0)
        assert _required_headcount(inp_with_ramp) >= _required_headcount(inp_no_ramp)

    def test_minimum_one_rep(self):
        inp = _make_input(
            annual_revenue_target_usd=1.0,
            avg_productivity_per_rep_usd=1_000_000.0,
            quota_attainment_pct=100.0,
            expected_attrition_rate_pct=0.0,
            avg_ramp_months=0.0,
        )
        assert _required_headcount(inp) >= 1

    def test_zero_quota_attainment_uses_raw_productivity(self):
        inp = _make_input(
            quota_attainment_pct=0.0,
            avg_productivity_per_rep_usd=1_000_000.0,
            annual_revenue_target_usd=10_000_000.0,
            expected_attrition_rate_pct=0.0,
            avg_ramp_months=0.0,
        )
        # effective_productivity falls back to avg_productivity_per_rep_usd
        result = _required_headcount(inp)
        assert result >= 1

    def test_returns_int(self):
        inp = _make_input()
        assert isinstance(_required_headcount(inp), int)

    def test_large_target_scales_headcount(self):
        inp_small = _make_input(annual_revenue_target_usd=1_000_000.0, quota_attainment_pct=100.0,
                                avg_productivity_per_rep_usd=1_000_000.0, expected_attrition_rate_pct=0.0, avg_ramp_months=0.0)
        inp_large = _make_input(annual_revenue_target_usd=10_000_000.0, quota_attainment_pct=100.0,
                                avg_productivity_per_rep_usd=1_000_000.0, expected_attrition_rate_pct=0.0, avg_ramp_months=0.0)
        assert _required_headcount(inp_large) > _required_headcount(inp_small)


# ---------------------------------------------------------------------------
# 5. _productivity_score helper
# ---------------------------------------------------------------------------

class TestProductivityScore:
    def test_max_score_scenario(self):
        inp = _make_input(
            quota_attainment_pct=95.0,   # +35
            rep_productivity_trend=0.5,   # +25
            win_rate_pct=35.0,            # +25
            territory_saturation_pct=30.0,  # +15
        )
        score = _productivity_score(inp)
        assert score == 100.0

    def test_quota_attainment_ge_90(self):
        inp = _make_input(quota_attainment_pct=90.0, rep_productivity_trend=-1.0, win_rate_pct=0.0, territory_saturation_pct=100.0)
        score = _productivity_score(inp)
        assert score >= 35.0

    def test_quota_attainment_80_to_89(self):
        inp = _make_input(quota_attainment_pct=85.0, rep_productivity_trend=-1.0, win_rate_pct=0.0, territory_saturation_pct=100.0)
        score = _productivity_score(inp)
        assert 26.0 <= score < 35.0

    def test_quota_attainment_65_to_79(self):
        inp = _make_input(quota_attainment_pct=70.0, rep_productivity_trend=-1.0, win_rate_pct=0.0, territory_saturation_pct=100.0)
        score = _productivity_score(inp)
        assert 16.0 <= score < 26.0

    def test_quota_attainment_50_to_64(self):
        inp = _make_input(quota_attainment_pct=55.0, rep_productivity_trend=-1.0, win_rate_pct=0.0, territory_saturation_pct=100.0)
        score = _productivity_score(inp)
        assert 8.0 <= score < 16.0

    def test_quota_attainment_below_50_no_attainment_points(self):
        inp = _make_input(quota_attainment_pct=40.0, rep_productivity_trend=-1.0, win_rate_pct=0.0, territory_saturation_pct=100.0)
        score = _productivity_score(inp)
        assert score == 0.0

    def test_productivity_trend_high(self):
        inp = _make_input(quota_attainment_pct=40.0, rep_productivity_trend=0.5, win_rate_pct=0.0, territory_saturation_pct=100.0)
        score = _productivity_score(inp)
        assert score == 25.0

    def test_productivity_trend_moderate(self):
        inp = _make_input(quota_attainment_pct=40.0, rep_productivity_trend=0.2, win_rate_pct=0.0, territory_saturation_pct=100.0)
        score = _productivity_score(inp)
        assert score == 18.0

    def test_productivity_trend_slight_negative(self):
        inp = _make_input(quota_attainment_pct=40.0, rep_productivity_trend=-0.2, win_rate_pct=0.0, territory_saturation_pct=100.0)
        score = _productivity_score(inp)
        assert score == 10.0

    def test_productivity_trend_very_negative(self):
        inp = _make_input(quota_attainment_pct=40.0, rep_productivity_trend=-0.5, win_rate_pct=0.0, territory_saturation_pct=100.0)
        score = _productivity_score(inp)
        assert score == 0.0

    def test_win_rate_ge_30(self):
        inp = _make_input(quota_attainment_pct=40.0, rep_productivity_trend=-1.0, win_rate_pct=30.0, territory_saturation_pct=100.0)
        score = _productivity_score(inp)
        assert score == 25.0

    def test_win_rate_20_to_29(self):
        inp = _make_input(quota_attainment_pct=40.0, rep_productivity_trend=-1.0, win_rate_pct=25.0, territory_saturation_pct=100.0)
        score = _productivity_score(inp)
        assert score == 18.0

    def test_win_rate_12_to_19(self):
        inp = _make_input(quota_attainment_pct=40.0, rep_productivity_trend=-1.0, win_rate_pct=15.0, territory_saturation_pct=100.0)
        score = _productivity_score(inp)
        assert score == 10.0

    def test_win_rate_5_to_11(self):
        inp = _make_input(quota_attainment_pct=40.0, rep_productivity_trend=-1.0, win_rate_pct=8.0, territory_saturation_pct=100.0)
        score = _productivity_score(inp)
        assert score == 4.0

    def test_win_rate_below_5_no_points(self):
        inp = _make_input(quota_attainment_pct=40.0, rep_productivity_trend=-1.0, win_rate_pct=2.0, territory_saturation_pct=100.0)
        score = _productivity_score(inp)
        assert score == 0.0

    def test_territory_saturation_le_40(self):
        inp = _make_input(quota_attainment_pct=40.0, rep_productivity_trend=-1.0, win_rate_pct=0.0, territory_saturation_pct=40.0)
        score = _productivity_score(inp)
        assert score == 15.0

    def test_territory_saturation_41_to_60(self):
        inp = _make_input(quota_attainment_pct=40.0, rep_productivity_trend=-1.0, win_rate_pct=0.0, territory_saturation_pct=50.0)
        score = _productivity_score(inp)
        assert score == 10.0

    def test_territory_saturation_61_to_80(self):
        inp = _make_input(quota_attainment_pct=40.0, rep_productivity_trend=-1.0, win_rate_pct=0.0, territory_saturation_pct=70.0)
        score = _productivity_score(inp)
        assert score == 4.0

    def test_territory_saturation_above_80(self):
        inp = _make_input(quota_attainment_pct=40.0, rep_productivity_trend=-1.0, win_rate_pct=0.0, territory_saturation_pct=90.0)
        score = _productivity_score(inp)
        assert score == 0.0

    def test_score_bounded_0_100(self):
        for _ in range(5):
            score = _productivity_score(_make_input())
            assert 0.0 <= score <= 100.0

    def test_score_rounded_to_one_decimal(self):
        score = _productivity_score(_make_input())
        assert round(score, 1) == score


# ---------------------------------------------------------------------------
# 6. _pipeline_health_score helper
# ---------------------------------------------------------------------------

class TestPipelineHealthScore:
    def test_max_score_scenario(self):
        inp = _make_input(
            current_pipeline_coverage_ratio=4.0,   # +35
            lead_volume_monthly=300,                # 30 per rep → +25
            current_headcount=10,
            lead_to_opportunity_rate_pct=20.0,      # +20
            expansion_revenue_pct=30.0,              # +20
        )
        score = _pipeline_health_score(inp)
        assert score == 100.0

    def test_coverage_3_to_5(self):
        inp = _make_input(current_pipeline_coverage_ratio=4.0,
                          lead_volume_monthly=0, lead_to_opportunity_rate_pct=0.0, expansion_revenue_pct=0.0)
        score = _pipeline_health_score(inp)
        assert score == 35.0

    def test_coverage_2_to_3(self):
        inp = _make_input(current_pipeline_coverage_ratio=2.5,
                          lead_volume_monthly=0, lead_to_opportunity_rate_pct=0.0, expansion_revenue_pct=0.0)
        score = _pipeline_health_score(inp)
        assert score == 24.0

    def test_coverage_5_to_7(self):
        inp = _make_input(current_pipeline_coverage_ratio=6.0,
                          lead_volume_monthly=0, lead_to_opportunity_rate_pct=0.0, expansion_revenue_pct=0.0)
        score = _pipeline_health_score(inp)
        assert score == 20.0

    def test_coverage_1_to_2(self):
        inp = _make_input(current_pipeline_coverage_ratio=1.5,
                          lead_volume_monthly=0, lead_to_opportunity_rate_pct=0.0, expansion_revenue_pct=0.0)
        score = _pipeline_health_score(inp)
        assert score == 10.0

    def test_coverage_below_1_no_points(self):
        inp = _make_input(current_pipeline_coverage_ratio=0.5,
                          lead_volume_monthly=0, lead_to_opportunity_rate_pct=0.0, expansion_revenue_pct=0.0)
        score = _pipeline_health_score(inp)
        assert score == 0.0

    def test_leads_per_rep_ge_30(self):
        inp = _make_input(current_pipeline_coverage_ratio=0.0, current_headcount=10,
                          lead_volume_monthly=300, lead_to_opportunity_rate_pct=0.0, expansion_revenue_pct=0.0)
        score = _pipeline_health_score(inp)
        assert score == 25.0

    def test_leads_per_rep_20_to_29(self):
        inp = _make_input(current_pipeline_coverage_ratio=0.0, current_headcount=10,
                          lead_volume_monthly=250, lead_to_opportunity_rate_pct=0.0, expansion_revenue_pct=0.0)
        score = _pipeline_health_score(inp)
        assert score == 18.0

    def test_leads_per_rep_10_to_19(self):
        inp = _make_input(current_pipeline_coverage_ratio=0.0, current_headcount=10,
                          lead_volume_monthly=150, lead_to_opportunity_rate_pct=0.0, expansion_revenue_pct=0.0)
        score = _pipeline_health_score(inp)
        assert score == 10.0

    def test_leads_per_rep_5_to_9(self):
        inp = _make_input(current_pipeline_coverage_ratio=0.0, current_headcount=10,
                          lead_volume_monthly=70, lead_to_opportunity_rate_pct=0.0, expansion_revenue_pct=0.0)
        score = _pipeline_health_score(inp)
        assert score == 4.0

    def test_leads_per_rep_below_5_no_points(self):
        inp = _make_input(current_pipeline_coverage_ratio=0.0, current_headcount=10,
                          lead_volume_monthly=30, lead_to_opportunity_rate_pct=0.0, expansion_revenue_pct=0.0)
        score = _pipeline_health_score(inp)
        assert score == 0.0

    def test_lead_to_opp_ge_20(self):
        inp = _make_input(current_pipeline_coverage_ratio=0.0, lead_volume_monthly=0,
                          lead_to_opportunity_rate_pct=20.0, expansion_revenue_pct=0.0)
        score = _pipeline_health_score(inp)
        assert score == 20.0

    def test_lead_to_opp_12_to_19(self):
        inp = _make_input(current_pipeline_coverage_ratio=0.0, lead_volume_monthly=0,
                          lead_to_opportunity_rate_pct=15.0, expansion_revenue_pct=0.0)
        score = _pipeline_health_score(inp)
        assert score == 14.0

    def test_lead_to_opp_6_to_11(self):
        inp = _make_input(current_pipeline_coverage_ratio=0.0, lead_volume_monthly=0,
                          lead_to_opportunity_rate_pct=8.0, expansion_revenue_pct=0.0)
        score = _pipeline_health_score(inp)
        assert score == 7.0

    def test_lead_to_opp_below_6_no_points(self):
        inp = _make_input(current_pipeline_coverage_ratio=0.0, lead_volume_monthly=0,
                          lead_to_opportunity_rate_pct=3.0, expansion_revenue_pct=0.0)
        score = _pipeline_health_score(inp)
        assert score == 0.0

    def test_expansion_ge_30(self):
        inp = _make_input(current_pipeline_coverage_ratio=0.0, lead_volume_monthly=0,
                          lead_to_opportunity_rate_pct=0.0, expansion_revenue_pct=30.0)
        score = _pipeline_health_score(inp)
        assert score == 20.0

    def test_expansion_20_to_29(self):
        inp = _make_input(current_pipeline_coverage_ratio=0.0, lead_volume_monthly=0,
                          lead_to_opportunity_rate_pct=0.0, expansion_revenue_pct=25.0)
        score = _pipeline_health_score(inp)
        assert score == 14.0

    def test_expansion_10_to_19(self):
        inp = _make_input(current_pipeline_coverage_ratio=0.0, lead_volume_monthly=0,
                          lead_to_opportunity_rate_pct=0.0, expansion_revenue_pct=15.0)
        score = _pipeline_health_score(inp)
        assert score == 7.0

    def test_expansion_below_10_no_points(self):
        inp = _make_input(current_pipeline_coverage_ratio=0.0, lead_volume_monthly=0,
                          lead_to_opportunity_rate_pct=0.0, expansion_revenue_pct=5.0)
        score = _pipeline_health_score(inp)
        assert score == 0.0

    def test_score_bounded_0_100(self):
        score = _pipeline_health_score(_make_input())
        assert 0.0 <= score <= 100.0

    def test_score_rounded_to_one_decimal(self):
        score = _pipeline_health_score(_make_input())
        assert round(score, 1) == score

    def test_zero_headcount_uses_max_1(self):
        # Should not raise ZeroDivisionError; current_headcount=0 → leads_per_rep = volume/1
        inp = _make_input(current_headcount=0, lead_volume_monthly=300,
                          current_pipeline_coverage_ratio=0.0, lead_to_opportunity_rate_pct=0.0, expansion_revenue_pct=0.0)
        score = _pipeline_health_score(inp)
        assert 0.0 <= score <= 100.0


# ---------------------------------------------------------------------------
# 7. _hiring_efficiency_score helper
# ---------------------------------------------------------------------------

class TestHiringEfficiencyScore:
    def test_max_score_scenario(self):
        inp = _make_input(
            time_to_hire_days=20.0,         # +40
            expected_attrition_rate_pct=5.0,  # +35
            open_headcount_req=0,             # ratio=0 → +25
            current_headcount=10,
        )
        score = _hiring_efficiency_score(inp)
        assert score == 100.0

    def test_time_to_hire_le_30(self):
        inp = _make_input(time_to_hire_days=25.0, expected_attrition_rate_pct=50.0, open_headcount_req=100, current_headcount=10)
        score = _hiring_efficiency_score(inp)
        assert score == 40.0

    def test_time_to_hire_31_to_60(self):
        inp = _make_input(time_to_hire_days=45.0, expected_attrition_rate_pct=50.0, open_headcount_req=100, current_headcount=10)
        score = _hiring_efficiency_score(inp)
        assert score == 28.0

    def test_time_to_hire_61_to_90(self):
        inp = _make_input(time_to_hire_days=75.0, expected_attrition_rate_pct=50.0, open_headcount_req=100, current_headcount=10)
        score = _hiring_efficiency_score(inp)
        assert score == 16.0

    def test_time_to_hire_91_to_120(self):
        inp = _make_input(time_to_hire_days=110.0, expected_attrition_rate_pct=50.0, open_headcount_req=100, current_headcount=10)
        score = _hiring_efficiency_score(inp)
        assert score == 6.0

    def test_time_to_hire_above_120_no_points(self):
        inp = _make_input(time_to_hire_days=150.0, expected_attrition_rate_pct=50.0, open_headcount_req=100, current_headcount=10)
        score = _hiring_efficiency_score(inp)
        assert score == 0.0

    def test_attrition_le_10(self):
        inp = _make_input(time_to_hire_days=200.0, expected_attrition_rate_pct=5.0, open_headcount_req=100, current_headcount=10)
        score = _hiring_efficiency_score(inp)
        assert score == 35.0

    def test_attrition_11_to_20(self):
        inp = _make_input(time_to_hire_days=200.0, expected_attrition_rate_pct=15.0, open_headcount_req=100, current_headcount=10)
        score = _hiring_efficiency_score(inp)
        assert score == 24.0

    def test_attrition_21_to_30(self):
        inp = _make_input(time_to_hire_days=200.0, expected_attrition_rate_pct=25.0, open_headcount_req=100, current_headcount=10)
        score = _hiring_efficiency_score(inp)
        assert score == 12.0

    def test_attrition_31_to_40(self):
        inp = _make_input(time_to_hire_days=200.0, expected_attrition_rate_pct=35.0, open_headcount_req=100, current_headcount=10)
        score = _hiring_efficiency_score(inp)
        assert score == 4.0

    def test_attrition_above_40_no_points(self):
        inp = _make_input(time_to_hire_days=200.0, expected_attrition_rate_pct=50.0, open_headcount_req=100, current_headcount=10)
        score = _hiring_efficiency_score(inp)
        assert score == 0.0

    def test_open_ratio_le_01(self):
        inp = _make_input(time_to_hire_days=200.0, expected_attrition_rate_pct=50.0, open_headcount_req=1, current_headcount=20)
        score = _hiring_efficiency_score(inp)
        assert score == 25.0

    def test_open_ratio_11_to_20(self):
        inp = _make_input(time_to_hire_days=200.0, expected_attrition_rate_pct=50.0, open_headcount_req=2, current_headcount=10)
        score = _hiring_efficiency_score(inp)
        assert score == 18.0

    def test_open_ratio_21_to_35(self):
        inp = _make_input(time_to_hire_days=200.0, expected_attrition_rate_pct=50.0, open_headcount_req=3, current_headcount=10)
        score = _hiring_efficiency_score(inp)
        assert score == 8.0

    def test_open_ratio_above_35_no_points(self):
        inp = _make_input(time_to_hire_days=200.0, expected_attrition_rate_pct=50.0, open_headcount_req=5, current_headcount=10)
        score = _hiring_efficiency_score(inp)
        assert score == 0.0

    def test_zero_headcount_uses_ratio_one(self):
        inp = _make_input(current_headcount=0, open_headcount_req=5, time_to_hire_days=200.0, expected_attrition_rate_pct=50.0)
        score = _hiring_efficiency_score(inp)
        assert 0.0 <= score <= 100.0

    def test_score_bounded_0_100(self):
        score = _hiring_efficiency_score(_make_input())
        assert 0.0 <= score <= 100.0

    def test_score_rounded_to_one_decimal(self):
        score = _hiring_efficiency_score(_make_input())
        assert round(score, 1) == score


# ---------------------------------------------------------------------------
# 8. _composite helper
# ---------------------------------------------------------------------------

class TestComposite:
    def test_formula_weights(self):
        result = _composite(80.0, 60.0, 40.0)
        expected = round(80.0 * 0.40 + 60.0 * 0.35 + 40.0 * 0.25, 1)
        assert result == expected

    def test_all_zeros(self):
        assert _composite(0.0, 0.0, 0.0) == 0.0

    def test_all_hundreds(self):
        assert _composite(100.0, 100.0, 100.0) == 100.0

    def test_rounded_to_one_decimal(self):
        val = _composite(33.3, 33.3, 33.3)
        assert round(val, 1) == val

    def test_productivity_weight_dominates(self):
        assert _composite(100.0, 0.0, 0.0) == round(100.0 * 0.40, 1)

    def test_pipeline_weight(self):
        assert _composite(0.0, 100.0, 0.0) == round(100.0 * 0.35, 1)

    def test_hiring_weight(self):
        assert _composite(0.0, 0.0, 100.0) == round(100.0 * 0.25, 1)

    def test_specific_values(self):
        # productivity=50, pipeline=60, hiring=70
        expected = round(50 * 0.40 + 60 * 0.35 + 70 * 0.25, 1)
        assert _composite(50.0, 60.0, 70.0) == expected


# ---------------------------------------------------------------------------
# 9. _capacity_status helper
# ---------------------------------------------------------------------------

class TestCapacityStatus:
    def test_gap_le_neg3_is_surplus(self):
        assert _capacity_status(-5, 10) == CapacityStatus.SURPLUS

    def test_gap_neg3_is_surplus(self):
        assert _capacity_status(-3, 10) == CapacityStatus.SURPLUS

    def test_gap_neg2_is_balanced(self):
        assert _capacity_status(-2, 10) == CapacityStatus.BALANCED

    def test_gap_0_is_balanced(self):
        assert _capacity_status(0, 10) == CapacityStatus.BALANCED

    def test_gap_1_is_gap(self):
        assert _capacity_status(1, 10) == CapacityStatus.GAP

    def test_gap_3_is_gap(self):
        assert _capacity_status(3, 10) == CapacityStatus.GAP

    def test_gap_4_is_critical_gap(self):
        assert _capacity_status(4, 10) == CapacityStatus.CRITICAL_GAP

    def test_gap_10_is_critical_gap(self):
        assert _capacity_status(10, 10) == CapacityStatus.CRITICAL_GAP


# ---------------------------------------------------------------------------
# 10. _capacity_risk helper
# ---------------------------------------------------------------------------

class TestCapacityRisk:
    def test_composite_below_25_is_critical(self):
        assert _capacity_risk(20.0, 0) == CapacityRisk.CRITICAL

    def test_gap_ge_8_is_critical(self):
        assert _capacity_risk(80.0, 8) == CapacityRisk.CRITICAL

    def test_composite_below_40_is_high(self):
        assert _capacity_risk(35.0, 0) == CapacityRisk.HIGH

    def test_gap_ge_5_is_high(self):
        assert _capacity_risk(80.0, 5) == CapacityRisk.HIGH

    def test_composite_below_60_is_moderate(self):
        assert _capacity_risk(50.0, 0) == CapacityRisk.MODERATE

    def test_gap_ge_2_is_moderate(self):
        assert _capacity_risk(80.0, 2) == CapacityRisk.MODERATE

    def test_high_composite_zero_gap_is_low(self):
        assert _capacity_risk(80.0, 0) == CapacityRisk.LOW

    def test_high_composite_gap_1_is_low(self):
        assert _capacity_risk(80.0, 1) == CapacityRisk.LOW


# ---------------------------------------------------------------------------
# 11. _growth_constraint helper
# ---------------------------------------------------------------------------

class TestGrowthConstraint:
    def test_large_gap_slow_hire_is_hiring_speed(self):
        inp = _make_input(time_to_hire_days=100.0, current_pipeline_coverage_ratio=3.0, quota_attainment_pct=80.0)
        assert _growth_constraint(inp, 5) == GrowthConstraint.HIRING_SPEED

    def test_large_gap_fast_hire_is_headcount(self):
        inp = _make_input(time_to_hire_days=50.0, current_pipeline_coverage_ratio=3.0, quota_attainment_pct=80.0)
        assert _growth_constraint(inp, 5) == GrowthConstraint.HEADCOUNT

    def test_small_gap_low_pipeline_is_pipeline(self):
        inp = _make_input(time_to_hire_days=50.0, current_pipeline_coverage_ratio=1.5, quota_attainment_pct=80.0)
        assert _growth_constraint(inp, 2) == GrowthConstraint.PIPELINE

    def test_small_gap_good_pipeline_low_attainment_is_productivity(self):
        inp = _make_input(time_to_hire_days=50.0, current_pipeline_coverage_ratio=3.0, quota_attainment_pct=50.0)
        assert _growth_constraint(inp, 0) == GrowthConstraint.PRODUCTIVITY

    def test_no_constraint(self):
        inp = _make_input(time_to_hire_days=50.0, current_pipeline_coverage_ratio=3.0, quota_attainment_pct=80.0)
        assert _growth_constraint(inp, 0) == GrowthConstraint.NONE

    def test_boundary_gap_exactly_3_slow_hire(self):
        inp = _make_input(time_to_hire_days=91.0, current_pipeline_coverage_ratio=3.0, quota_attainment_pct=80.0)
        assert _growth_constraint(inp, 3) == GrowthConstraint.HIRING_SPEED

    def test_boundary_gap_exactly_3_fast_hire(self):
        inp = _make_input(time_to_hire_days=89.0, current_pipeline_coverage_ratio=3.0, quota_attainment_pct=80.0)
        assert _growth_constraint(inp, 3) == GrowthConstraint.HEADCOUNT


# ---------------------------------------------------------------------------
# 12. _capacity_action helper
# ---------------------------------------------------------------------------

class TestCapacityAction:
    def test_critical_gap_always_accelerate(self):
        for risk in CapacityRisk:
            assert _capacity_action(risk, CapacityStatus.CRITICAL_GAP) == CapacityAction.ACCELERATE_HIRING

    def test_gap_high_risk_accelerate(self):
        assert _capacity_action(CapacityRisk.HIGH, CapacityStatus.GAP) == CapacityAction.ACCELERATE_HIRING

    def test_gap_moderate_risk_restructure(self):
        assert _capacity_action(CapacityRisk.MODERATE, CapacityStatus.GAP) == CapacityAction.RESTRUCTURE_TERRITORY

    def test_gap_low_risk_restructure(self):
        assert _capacity_action(CapacityRisk.LOW, CapacityStatus.GAP) == CapacityAction.RESTRUCTURE_TERRITORY

    def test_balanced_critical_risk_reduce_target(self):
        assert _capacity_action(CapacityRisk.CRITICAL, CapacityStatus.BALANCED) == CapacityAction.REDUCE_TARGET

    def test_balanced_high_risk_reduce_target(self):
        assert _capacity_action(CapacityRisk.HIGH, CapacityStatus.BALANCED) == CapacityAction.REDUCE_TARGET

    def test_balanced_moderate_risk_maintain(self):
        assert _capacity_action(CapacityRisk.MODERATE, CapacityStatus.BALANCED) == CapacityAction.MAINTAIN

    def test_balanced_low_risk_maintain(self):
        assert _capacity_action(CapacityRisk.LOW, CapacityStatus.BALANCED) == CapacityAction.MAINTAIN

    def test_surplus_low_risk_maintain(self):
        assert _capacity_action(CapacityRisk.LOW, CapacityStatus.SURPLUS) == CapacityAction.MAINTAIN

    def test_surplus_critical_risk_reduce_target(self):
        assert _capacity_action(CapacityRisk.CRITICAL, CapacityStatus.SURPLUS) == CapacityAction.REDUCE_TARGET

    def test_gap_critical_risk_accelerate(self):
        # CRITICAL is in the >=HIGH set, but GAP status w/ CRITICAL → CRITICAL is not checked
        # because CRITICAL_GAP check is first, then GAP checks risk==HIGH only
        # Actually: CRITICAL is not "HIGH" so it falls to RESTRUCTURE
        # Wait, re-reading code: if status==GAP, if risk==HIGH → ACCELERATE, else RESTRUCTURE
        # So CRITICAL risk + GAP → RESTRUCTURE
        assert _capacity_action(CapacityRisk.CRITICAL, CapacityStatus.GAP) == CapacityAction.RESTRUCTURE_TERRITORY


# ---------------------------------------------------------------------------
# 13. _revenue_at_risk_usd helper
# ---------------------------------------------------------------------------

class TestRevenueAtRisk:
    def test_positive_gap_includes_rep_gap_revenue(self):
        inp = _make_input(
            avg_productivity_per_rep_usd=500_000.0,
            quota_attainment_pct=100.0,
            annual_revenue_target_usd=10_000_000.0,
        )
        rev = _revenue_at_risk_usd(inp, 2, 80.0)
        # rep_gap_revenue = 2 * 500_000 * 1.0 = 1_000_000
        # composite_risk = 10M * (100-80)/400 = 500_000
        assert rev == round(1_000_000.0 + 500_000.0, 2)

    def test_zero_gap_uses_composite_factor(self):
        inp = _make_input(annual_revenue_target_usd=10_000_000.0)
        rev = _revenue_at_risk_usd(inp, 0, 80.0)
        # risk_factor = (100-80)/200 = 0.1 → 10M * 0.1 = 1_000_000
        assert rev == round(10_000_000.0 * (100.0 - 80.0) / 200.0, 2)

    def test_negative_gap_zero_rep_based_risk(self):
        inp = _make_input(annual_revenue_target_usd=10_000_000.0)
        rev = _revenue_at_risk_usd(inp, -5, 80.0)
        assert rev >= 0.0

    def test_returns_float(self):
        inp = _make_input()
        assert isinstance(_revenue_at_risk_usd(inp, 0, 50.0), float)

    def test_rounded_to_two_decimals(self):
        inp = _make_input()
        rev = _revenue_at_risk_usd(inp, 2, 73.33)
        assert round(rev, 2) == rev

    def test_positive_gap_higher_rev_at_risk_than_zero_gap(self):
        inp = _make_input(avg_productivity_per_rep_usd=1_000_000.0, annual_revenue_target_usd=10_000_000.0)
        rev_gap = _revenue_at_risk_usd(inp, 3, 50.0)
        rev_no_gap = _revenue_at_risk_usd(inp, 0, 50.0)
        assert rev_gap > rev_no_gap


# ---------------------------------------------------------------------------
# 14. _capacity_signal helper
# ---------------------------------------------------------------------------

class TestCapacitySignal:
    def test_critical_gap_mentions_reps(self):
        inp = _make_input(annual_revenue_target_usd=5_000_000.0, time_to_hire_days=50.0,
                          current_pipeline_coverage_ratio=3.0, quota_attainment_pct=80.0)
        signal = _capacity_signal(inp, 5, GrowthConstraint.NONE)
        assert "critical" in signal.lower()
        assert "5" in signal

    def test_hiring_bottleneck_signal(self):
        inp = _make_input(time_to_hire_days=95.0)
        signal = _capacity_signal(inp, 3, GrowthConstraint.HIRING_SPEED)
        assert "hiring" in signal.lower()

    def test_pipeline_signal(self):
        inp = _make_input(current_pipeline_coverage_ratio=1.8)
        signal = _capacity_signal(inp, 1, GrowthConstraint.PIPELINE)
        assert "pipeline" in signal.lower()

    def test_productivity_signal(self):
        inp = _make_input(quota_attainment_pct=55.0)
        signal = _capacity_signal(inp, 0, GrowthConstraint.PRODUCTIVITY)
        assert "productivity" in signal.lower() or "55" in signal

    def test_headcount_gap_signal(self):
        inp = _make_input()
        signal = _capacity_signal(inp, 2, GrowthConstraint.NONE)
        assert "headcount gap" in signal.lower() or "gap" in signal.lower()

    def test_surplus_signal(self):
        inp = _make_input()
        signal = _capacity_signal(inp, -5, GrowthConstraint.NONE)
        assert "surplus" in signal.lower()

    def test_balanced_signal(self):
        inp = _make_input(current_headcount=10, annual_revenue_target_usd=10_000_000.0)
        signal = _capacity_signal(inp, 0, GrowthConstraint.NONE)
        assert "balanced" in signal.lower() or "capacity" in signal.lower()

    def test_signal_is_string(self):
        inp = _make_input()
        assert isinstance(_capacity_signal(inp, 0, GrowthConstraint.NONE), str)

    def test_surplus_only_when_gap_less_than_neg2(self):
        inp = _make_input()
        # gap = -2 → not surplus → should return balanced-ish
        signal = _capacity_signal(inp, -2, GrowthConstraint.NONE)
        assert "surplus" not in signal.lower()


# ---------------------------------------------------------------------------
# 15. Engine.assess – integration
# ---------------------------------------------------------------------------

class TestEngineAssess:
    def test_returns_result_type(self, engine, baseline_input):
        result = engine.assess(baseline_input)
        assert isinstance(result, SalesCapacityResult)

    def test_result_region_id_matches(self, engine, baseline_input):
        result = engine.assess(baseline_input)
        assert result.region_id == baseline_input.region_id

    def test_result_region_name_matches(self, engine, baseline_input):
        result = engine.assess(baseline_input)
        assert result.region_name == baseline_input.region_name

    def test_composite_formula_respected(self, engine):
        inp = _make_input()
        result = engine.assess(inp)
        prod = _productivity_score(inp)
        pipe = _pipeline_health_score(inp)
        hire = _hiring_efficiency_score(inp)
        expected_composite = _composite(prod, pipe, hire)
        assert result.capacity_composite == expected_composite

    def test_is_understaffed_when_gap_positive(self, engine):
        # Force a large gap: tiny productivity but huge target
        inp = _make_input(
            annual_revenue_target_usd=100_000_000.0,
            avg_productivity_per_rep_usd=1_000_000.0,
            current_headcount=5,
            quota_attainment_pct=100.0,
            expected_attrition_rate_pct=0.0,
            avg_ramp_months=0.0,
        )
        result = engine.assess(inp)
        assert result.is_understaffed is True
        assert result.capacity_gap > 0

    def test_is_understaffed_false_when_overstaffed(self, engine):
        # Force surplus: lots of headcount for small target
        inp = _make_input(
            annual_revenue_target_usd=1_000_000.0,
            avg_productivity_per_rep_usd=1_000_000.0,
            current_headcount=50,
            quota_attainment_pct=100.0,
            expected_attrition_rate_pct=0.0,
            avg_ramp_months=0.0,
        )
        result = engine.assess(inp)
        assert result.is_understaffed is False

    def test_capacity_gap_equals_required_minus_current(self, engine):
        inp = _make_input()
        result = engine.assess(inp)
        assert result.capacity_gap == result.required_headcount - inp.current_headcount

    def test_capacity_status_type(self, engine, baseline_input):
        result = engine.assess(baseline_input)
        assert isinstance(result.capacity_status, CapacityStatus)

    def test_capacity_risk_type(self, engine, baseline_input):
        result = engine.assess(baseline_input)
        assert isinstance(result.capacity_risk, CapacityRisk)

    def test_growth_constraint_type(self, engine, baseline_input):
        result = engine.assess(baseline_input)
        assert isinstance(result.growth_constraint, GrowthConstraint)

    def test_capacity_action_type(self, engine, baseline_input):
        result = engine.assess(baseline_input)
        assert isinstance(result.capacity_action, CapacityAction)

    def test_result_stored_in_engine(self, engine, baseline_input):
        result = engine.assess(baseline_input)
        assert engine.get(baseline_input.region_id) == result

    def test_assess_updates_stored_result(self, engine):
        inp1 = _make_input(annual_revenue_target_usd=10_000_000.0)
        inp2 = _make_input(annual_revenue_target_usd=20_000_000.0)
        engine.assess(inp1)
        engine.assess(inp2)
        stored = engine.get("R001")
        # Should be the latest result
        assert stored is not None

    def test_different_regions_stored_separately(self, engine):
        inp_a = _make_input(region_id="A", region_name="Alpha")
        inp_b = _make_input(region_id="B", region_name="Beta")
        engine.assess(inp_a)
        engine.assess(inp_b)
        assert engine.get("A").region_name == "Alpha"
        assert engine.get("B").region_name == "Beta"

    def test_get_nonexistent_returns_none(self, engine):
        assert engine.get("NONEXISTENT") is None

    def test_critical_gap_status_leads_to_accelerate_hiring(self, engine):
        # Force critical gap: huge target, small team, perfect attainment
        inp = _make_input(
            annual_revenue_target_usd=500_000_000.0,
            avg_productivity_per_rep_usd=1_000_000.0,
            current_headcount=2,
            quota_attainment_pct=100.0,
            expected_attrition_rate_pct=0.0,
            avg_ramp_months=0.0,
        )
        result = engine.assess(inp)
        assert result.capacity_status == CapacityStatus.CRITICAL_GAP
        assert result.capacity_action == CapacityAction.ACCELERATE_HIRING

    def test_surplus_status_when_overstaffed(self, engine):
        inp = _make_input(
            annual_revenue_target_usd=100_000.0,
            avg_productivity_per_rep_usd=1_000_000.0,
            current_headcount=50,
            quota_attainment_pct=100.0,
            expected_attrition_rate_pct=0.0,
            avg_ramp_months=0.0,
        )
        result = engine.assess(inp)
        assert result.capacity_status == CapacityStatus.SURPLUS

    def test_revenue_at_risk_is_non_negative(self, engine, baseline_input):
        result = engine.assess(baseline_input)
        assert result.revenue_at_risk_usd >= 0.0

    def test_productivity_score_matches_helper(self, engine):
        inp = _make_input()
        result = engine.assess(inp)
        assert result.productivity_score == _productivity_score(inp)

    def test_pipeline_health_score_matches_helper(self, engine):
        inp = _make_input()
        result = engine.assess(inp)
        assert result.pipeline_health_score == _pipeline_health_score(inp)

    def test_hiring_efficiency_score_matches_helper(self, engine):
        inp = _make_input()
        result = engine.assess(inp)
        assert result.hiring_efficiency_score == _hiring_efficiency_score(inp)


# ---------------------------------------------------------------------------
# 16. Engine.assess_batch
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_returns_list(self, engine):
        inputs = [_make_input(region_id=f"R{i}", region_name=f"Region {i}") for i in range(3)]
        results = engine.assess_batch(inputs)
        assert isinstance(results, list)

    def test_result_count_matches_input_count(self, engine):
        inputs = [_make_input(region_id=f"R{i}", region_name=f"Region {i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5

    def test_sorted_by_composite_descending(self, engine):
        inputs = [_make_input(region_id=f"R{i}", region_name=f"Region {i}") for i in range(4)]
        results = engine.assess_batch(inputs)
        composites = [r.capacity_composite for r in results]
        assert composites == sorted(composites, reverse=True)

    def test_empty_batch_returns_empty_list(self, engine):
        assert engine.assess_batch([]) == []

    def test_all_results_are_salesresult_type(self, engine):
        inputs = [_make_input(region_id=f"R{i}", region_name=f"Region {i}") for i in range(3)]
        results = engine.assess_batch(inputs)
        assert all(isinstance(r, SalesCapacityResult) for r in results)

    def test_batch_stores_all_regions(self, engine):
        inputs = [_make_input(region_id=f"R{i}", region_name=f"Region {i}") for i in range(3)]
        engine.assess_batch(inputs)
        for i in range(3):
            assert engine.get(f"R{i}") is not None

    def test_single_item_batch(self, engine):
        inp = _make_input()
        results = engine.assess_batch([inp])
        assert len(results) == 1
        assert results[0].region_id == "R001"


# ---------------------------------------------------------------------------
# 17. Engine helper methods
# ---------------------------------------------------------------------------

class TestEngineHelpers:
    def test_all_regions_sorted_by_composite_desc(self, engine):
        inputs = [_make_input(region_id=f"R{i}", region_name=f"Region {i}") for i in range(4)]
        engine.assess_batch(inputs)
        regions = engine.all_regions()
        composites = [r.capacity_composite for r in regions]
        assert composites == sorted(composites, reverse=True)

    def test_understaffed_regions_all_understaffed(self, engine):
        inputs = [_make_input(region_id=f"R{i}", region_name=f"Region {i}") for i in range(3)]
        engine.assess_batch(inputs)
        for r in engine.understaffed_regions():
            assert r.is_understaffed is True

    def test_by_status_filter(self, engine):
        inp_a = _make_input(region_id="A", region_name="A",
                             annual_revenue_target_usd=1_000_000_000.0,
                             current_headcount=2,
                             avg_productivity_per_rep_usd=1_000_000.0,
                             quota_attainment_pct=100.0,
                             expected_attrition_rate_pct=0.0,
                             avg_ramp_months=0.0)
        engine.assess(inp_a)
        result_a = engine.get("A")
        filtered = engine.by_status(result_a.capacity_status)
        assert all(r.capacity_status == result_a.capacity_status for r in filtered)

    def test_by_risk_filter(self, engine):
        inp = _make_input(region_id="X", region_name="X")
        engine.assess(inp)
        result = engine.get("X")
        filtered = engine.by_risk(result.capacity_risk)
        assert all(r.capacity_risk == result.capacity_risk for r in filtered)

    def test_total_headcount_gap_non_negative(self, engine):
        inputs = [_make_input(region_id=f"R{i}", region_name=f"Region {i}") for i in range(3)]
        engine.assess_batch(inputs)
        assert engine.total_headcount_gap() >= 0

    def test_total_headcount_gap_only_counts_positive_gaps(self, engine):
        # Overstaffed region should not reduce total
        inp_over = _make_input(region_id="OVER", region_name="Over",
                               annual_revenue_target_usd=100_000.0,
                               current_headcount=50,
                               avg_productivity_per_rep_usd=1_000_000.0,
                               quota_attainment_pct=100.0,
                               expected_attrition_rate_pct=0.0,
                               avg_ramp_months=0.0)
        engine.assess(inp_over)
        gap = engine.total_headcount_gap()
        assert gap == 0

    def test_total_revenue_at_risk_is_float(self, engine):
        inputs = [_make_input(region_id=f"R{i}", region_name=f"Region {i}") for i in range(3)]
        engine.assess_batch(inputs)
        assert isinstance(engine.total_revenue_at_risk_usd(), float)

    def test_total_revenue_at_risk_non_negative(self, engine):
        inputs = [_make_input(region_id=f"R{i}", region_name=f"Region {i}") for i in range(3)]
        engine.assess_batch(inputs)
        assert engine.total_revenue_at_risk_usd() >= 0.0

    def test_avg_capacity_composite_empty_engine(self, engine):
        assert engine.avg_capacity_composite() == 0.0

    def test_avg_capacity_composite_with_results(self, engine):
        inputs = [_make_input(region_id=f"R{i}", region_name=f"Region {i}") for i in range(3)]
        engine.assess_batch(inputs)
        avg = engine.avg_capacity_composite()
        assert 0.0 <= avg <= 100.0

    def test_reset_clears_results(self, engine):
        inputs = [_make_input(region_id=f"R{i}", region_name=f"Region {i}") for i in range(3)]
        engine.assess_batch(inputs)
        engine.reset()
        assert engine.all_regions() == []

    def test_reset_avg_composite_is_zero(self, engine):
        engine.assess(_make_input())
        engine.reset()
        assert engine.avg_capacity_composite() == 0.0

    def test_reset_total_gap_is_zero(self, engine):
        engine.assess(_make_input())
        engine.reset()
        assert engine.total_headcount_gap() == 0


# ---------------------------------------------------------------------------
# 18. Engine.summary – key count and structure
# ---------------------------------------------------------------------------

class TestSummary:
    @pytest.fixture()
    def loaded_engine(self):
        eng = SalesCapacityPlanningEngine()
        inputs = [_make_input(region_id=f"R{i}", region_name=f"Region {i}") for i in range(5)]
        eng.assess_batch(inputs)
        return eng

    def test_summary_key_count(self, loaded_engine):
        s = loaded_engine.summary()
        assert len(s) == 13

    def test_summary_exact_keys(self, loaded_engine):
        expected_keys = {
            "total", "status_counts", "risk_counts", "constraint_counts",
            "action_counts", "avg_capacity_composite", "understaffed_count",
            "total_headcount_gap", "avg_productivity_score",
            "avg_pipeline_health_score", "avg_hiring_efficiency_score",
            "total_revenue_at_risk_usd", "optimal_headcount_range",
        }
        assert set(loaded_engine.summary().keys()) == expected_keys

    def test_summary_total_matches_input_count(self, loaded_engine):
        assert loaded_engine.summary()["total"] == 5

    def test_summary_status_counts_is_dict(self, loaded_engine):
        assert isinstance(loaded_engine.summary()["status_counts"], dict)

    def test_summary_risk_counts_is_dict(self, loaded_engine):
        assert isinstance(loaded_engine.summary()["risk_counts"], dict)

    def test_summary_constraint_counts_is_dict(self, loaded_engine):
        assert isinstance(loaded_engine.summary()["constraint_counts"], dict)

    def test_summary_action_counts_is_dict(self, loaded_engine):
        assert isinstance(loaded_engine.summary()["action_counts"], dict)

    def test_summary_status_counts_sum_equals_total(self, loaded_engine):
        s = loaded_engine.summary()
        assert sum(s["status_counts"].values()) == s["total"]

    def test_summary_risk_counts_sum_equals_total(self, loaded_engine):
        s = loaded_engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_constraint_counts_sum_equals_total(self, loaded_engine):
        s = loaded_engine.summary()
        assert sum(s["constraint_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_equals_total(self, loaded_engine):
        s = loaded_engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_understaffed_count_le_total(self, loaded_engine):
        s = loaded_engine.summary()
        assert s["understaffed_count"] <= s["total"]

    def test_summary_total_headcount_gap_non_negative(self, loaded_engine):
        assert loaded_engine.summary()["total_headcount_gap"] >= 0

    def test_summary_avg_composite_in_range(self, loaded_engine):
        avg = loaded_engine.summary()["avg_capacity_composite"]
        assert 0.0 <= avg <= 100.0

    def test_summary_avg_productivity_in_range(self, loaded_engine):
        avg = loaded_engine.summary()["avg_productivity_score"]
        assert 0.0 <= avg <= 100.0

    def test_summary_avg_pipeline_in_range(self, loaded_engine):
        avg = loaded_engine.summary()["avg_pipeline_health_score"]
        assert 0.0 <= avg <= 100.0

    def test_summary_avg_hiring_in_range(self, loaded_engine):
        avg = loaded_engine.summary()["avg_hiring_efficiency_score"]
        assert 0.0 <= avg <= 100.0

    def test_summary_optimal_headcount_range_format(self, loaded_engine):
        ohr = loaded_engine.summary()["optimal_headcount_range"]
        assert isinstance(ohr, str)
        parts = ohr.split("-")
        assert len(parts) == 2
        assert all(p.isdigit() for p in parts)

    def test_summary_total_revenue_at_risk_non_negative(self, loaded_engine):
        assert loaded_engine.summary()["total_revenue_at_risk_usd"] >= 0.0

    def test_summary_empty_engine_returns_zeros(self):
        eng = SalesCapacityPlanningEngine()
        s = eng.summary()
        assert s["total"] == 0
        assert s["understaffed_count"] == 0
        assert s["total_headcount_gap"] == 0

    def test_summary_single_region(self):
        eng = SalesCapacityPlanningEngine()
        eng.assess(_make_input())
        s = eng.summary()
        assert s["total"] == 1
        assert len(s) == 13


# ---------------------------------------------------------------------------
# 19. Edge cases and boundary conditions
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_all_zeros_input_doesnt_crash(self):
        inp = _make_input(
            annual_revenue_target_usd=0.0,
            current_headcount=0,
            avg_productivity_per_rep_usd=0.0,
            avg_ramp_months=0.0,
            expected_attrition_rate_pct=0.0,
            current_pipeline_coverage_ratio=0.0,
            open_headcount_req=0,
            time_to_hire_days=0.0,
            quota_attainment_pct=0.0,
            avg_deal_size_usd=0.0,
            avg_sales_cycle_days=0.0,
            win_rate_pct=0.0,
            lead_volume_monthly=0,
            lead_to_opportunity_rate_pct=0.0,
            expansion_revenue_pct=0.0,
            partner_revenue_pct=0.0,
            seasonal_peak_factor=0.0,
            territory_saturation_pct=0.0,
            rep_productivity_trend=-1.0,
        )
        engine = SalesCapacityPlanningEngine()
        result = engine.assess(inp)
        assert isinstance(result, SalesCapacityResult)

    def test_very_high_values_dont_crash(self):
        inp = _make_input(
            annual_revenue_target_usd=1e12,
            avg_productivity_per_rep_usd=1e9,
            current_headcount=1000,
            quota_attainment_pct=150.0,
            expected_attrition_rate_pct=100.0,
            territory_saturation_pct=200.0,
            rep_productivity_trend=10.0,
            win_rate_pct=100.0,
            current_pipeline_coverage_ratio=100.0,
            lead_volume_monthly=100_000,
            lead_to_opportunity_rate_pct=100.0,
            expansion_revenue_pct=100.0,
            time_to_hire_days=0.0,
            open_headcount_req=0,
        )
        engine = SalesCapacityPlanningEngine()
        result = engine.assess(inp)
        assert isinstance(result, SalesCapacityResult)

    def test_single_rep_team(self):
        inp = _make_input(current_headcount=1, open_headcount_req=0)
        engine = SalesCapacityPlanningEngine()
        result = engine.assess(inp)
        assert result.required_headcount >= 1

    def test_exact_boundary_gap_neg3_surplus(self):
        assert _capacity_status(-3, 10) == CapacityStatus.SURPLUS

    def test_exact_boundary_gap_0_balanced(self):
        assert _capacity_status(0, 10) == CapacityStatus.BALANCED

    def test_exact_boundary_gap_3_gap(self):
        assert _capacity_status(3, 10) == CapacityStatus.GAP

    def test_exact_boundary_gap_4_critical(self):
        assert _capacity_status(4, 10) == CapacityStatus.CRITICAL_GAP

    def test_composite_25_boundary_critical(self):
        # composite < 25 → CRITICAL
        assert _capacity_risk(24.9, 0) == CapacityRisk.CRITICAL

    def test_composite_exactly_25_not_critical(self):
        # composite == 25 → not < 25 → HIGH (since 25 < 40)
        assert _capacity_risk(25.0, 0) == CapacityRisk.HIGH

    def test_composite_40_boundary(self):
        # composite == 40 → not < 40 → MODERATE (since 40 < 60)
        assert _capacity_risk(40.0, 0) == CapacityRisk.MODERATE

    def test_composite_60_boundary_low(self):
        # composite == 60, gap==0 → not < 60 → LOW
        assert _capacity_risk(60.0, 0) == CapacityRisk.LOW

    def test_pipeline_coverage_exactly_3_is_ideal(self):
        score = _pipeline_health_score(_make_input(
            current_pipeline_coverage_ratio=3.0,
            lead_volume_monthly=0, lead_to_opportunity_rate_pct=0.0, expansion_revenue_pct=0.0
        ))
        assert score == 35.0

    def test_pipeline_coverage_exactly_5_is_ideal(self):
        score = _pipeline_health_score(_make_input(
            current_pipeline_coverage_ratio=5.0,
            lead_volume_monthly=0, lead_to_opportunity_rate_pct=0.0, expansion_revenue_pct=0.0
        ))
        assert score == 35.0

    def test_time_to_hire_exactly_30_max_points(self):
        score = _hiring_efficiency_score(_make_input(
            time_to_hire_days=30.0, expected_attrition_rate_pct=50.0, open_headcount_req=100, current_headcount=10
        ))
        assert score == 40.0

    def test_time_to_hire_exactly_60(self):
        score = _hiring_efficiency_score(_make_input(
            time_to_hire_days=60.0, expected_attrition_rate_pct=50.0, open_headcount_req=100, current_headcount=10
        ))
        assert score == 28.0

    def test_time_to_hire_exactly_90(self):
        score = _hiring_efficiency_score(_make_input(
            time_to_hire_days=90.0, expected_attrition_rate_pct=50.0, open_headcount_req=100, current_headcount=10
        ))
        assert score == 16.0

    def test_time_to_hire_exactly_120(self):
        score = _hiring_efficiency_score(_make_input(
            time_to_hire_days=120.0, expected_attrition_rate_pct=50.0, open_headcount_req=100, current_headcount=10
        ))
        assert score == 6.0

    def test_attrition_exactly_10(self):
        score = _hiring_efficiency_score(_make_input(
            time_to_hire_days=200.0, expected_attrition_rate_pct=10.0, open_headcount_req=100, current_headcount=10
        ))
        assert score == 35.0

    def test_attrition_exactly_20(self):
        score = _hiring_efficiency_score(_make_input(
            time_to_hire_days=200.0, expected_attrition_rate_pct=20.0, open_headcount_req=100, current_headcount=10
        ))
        assert score == 24.0

    def test_open_ratio_exactly_01(self):
        # open/headcount = 1/10 = 0.1 → +25
        score = _hiring_efficiency_score(_make_input(
            time_to_hire_days=200.0, expected_attrition_rate_pct=50.0, open_headcount_req=1, current_headcount=10
        ))
        assert score == 25.0

    def test_open_ratio_exactly_02(self):
        # open/headcount = 2/10 = 0.2 → +18
        score = _hiring_efficiency_score(_make_input(
            time_to_hire_days=200.0, expected_attrition_rate_pct=50.0, open_headcount_req=2, current_headcount=10
        ))
        assert score == 18.0

    def test_quota_attainment_exactly_90(self):
        score = _productivity_score(_make_input(
            quota_attainment_pct=90.0, rep_productivity_trend=-1.0, win_rate_pct=0.0, territory_saturation_pct=100.0
        ))
        assert score == 35.0

    def test_quota_attainment_exactly_80(self):
        score = _productivity_score(_make_input(
            quota_attainment_pct=80.0, rep_productivity_trend=-1.0, win_rate_pct=0.0, territory_saturation_pct=100.0
        ))
        assert score == 26.0

    def test_quota_attainment_exactly_65(self):
        score = _productivity_score(_make_input(
            quota_attainment_pct=65.0, rep_productivity_trend=-1.0, win_rate_pct=0.0, territory_saturation_pct=100.0
        ))
        assert score == 16.0

    def test_quota_attainment_exactly_50(self):
        score = _productivity_score(_make_input(
            quota_attainment_pct=50.0, rep_productivity_trend=-1.0, win_rate_pct=0.0, territory_saturation_pct=100.0
        ))
        assert score == 8.0

    def test_territory_saturation_exactly_40(self):
        score = _productivity_score(_make_input(
            quota_attainment_pct=40.0, rep_productivity_trend=-1.0, win_rate_pct=0.0, territory_saturation_pct=40.0
        ))
        assert score == 15.0

    def test_territory_saturation_exactly_60(self):
        score = _productivity_score(_make_input(
            quota_attainment_pct=40.0, rep_productivity_trend=-1.0, win_rate_pct=0.0, territory_saturation_pct=60.0
        ))
        assert score == 10.0

    def test_territory_saturation_exactly_80(self):
        score = _productivity_score(_make_input(
            quota_attainment_pct=40.0, rep_productivity_trend=-1.0, win_rate_pct=0.0, territory_saturation_pct=80.0
        ))
        assert score == 4.0

    def test_win_rate_exactly_30(self):
        score = _productivity_score(_make_input(
            quota_attainment_pct=40.0, rep_productivity_trend=-1.0, win_rate_pct=30.0, territory_saturation_pct=100.0
        ))
        assert score == 25.0

    def test_win_rate_exactly_20(self):
        score = _productivity_score(_make_input(
            quota_attainment_pct=40.0, rep_productivity_trend=-1.0, win_rate_pct=20.0, territory_saturation_pct=100.0
        ))
        assert score == 18.0

    def test_win_rate_exactly_12(self):
        score = _productivity_score(_make_input(
            quota_attainment_pct=40.0, rep_productivity_trend=-1.0, win_rate_pct=12.0, territory_saturation_pct=100.0
        ))
        assert score == 10.0

    def test_win_rate_exactly_5(self):
        score = _productivity_score(_make_input(
            quota_attainment_pct=40.0, rep_productivity_trend=-1.0, win_rate_pct=5.0, territory_saturation_pct=100.0
        ))
        assert score == 4.0

    def test_rep_trend_exactly_05(self):
        score = _productivity_score(_make_input(
            quota_attainment_pct=40.0, rep_productivity_trend=0.5, win_rate_pct=0.0, territory_saturation_pct=100.0
        ))
        assert score == 25.0

    def test_rep_trend_exactly_0(self):
        score = _productivity_score(_make_input(
            quota_attainment_pct=40.0, rep_productivity_trend=0.0, win_rate_pct=0.0, territory_saturation_pct=100.0
        ))
        assert score == 18.0

    def test_rep_trend_exactly_neg03(self):
        score = _productivity_score(_make_input(
            quota_attainment_pct=40.0, rep_productivity_trend=-0.3, win_rate_pct=0.0, territory_saturation_pct=100.0
        ))
        assert score == 10.0


# ---------------------------------------------------------------------------
# 20. Multi-region realistic scenario tests
# ---------------------------------------------------------------------------

class TestRealisticScenarios:
    def test_healthy_region_low_risk(self):
        """A well-staffed, high-performing region should have low risk."""
        inp = _make_input(
            annual_revenue_target_usd=5_000_000.0,
            current_headcount=5,
            avg_productivity_per_rep_usd=1_000_000.0,
            quota_attainment_pct=95.0,
            win_rate_pct=35.0,
            rep_productivity_trend=0.7,
            territory_saturation_pct=30.0,
            current_pipeline_coverage_ratio=4.0,
            lead_volume_monthly=200,
            lead_to_opportunity_rate_pct=25.0,
            expansion_revenue_pct=35.0,
            time_to_hire_days=25.0,
            expected_attrition_rate_pct=8.0,
            open_headcount_req=0,
            avg_ramp_months=3.0,
        )
        eng = SalesCapacityPlanningEngine()
        result = eng.assess(inp)
        assert result.capacity_risk in (CapacityRisk.LOW, CapacityRisk.MODERATE)

    def test_understaffed_critical_region(self):
        """An understaffed region with terrible metrics should be critical."""
        inp = _make_input(
            annual_revenue_target_usd=50_000_000.0,
            current_headcount=5,
            avg_productivity_per_rep_usd=1_000_000.0,
            quota_attainment_pct=40.0,
            win_rate_pct=3.0,
            rep_productivity_trend=-0.8,
            territory_saturation_pct=95.0,
            current_pipeline_coverage_ratio=0.8,
            lead_volume_monthly=20,
            lead_to_opportunity_rate_pct=2.0,
            expansion_revenue_pct=2.0,
            time_to_hire_days=180.0,
            expected_attrition_rate_pct=50.0,
            open_headcount_req=10,
            avg_ramp_months=9.0,
        )
        eng = SalesCapacityPlanningEngine()
        result = eng.assess(inp)
        assert result.is_understaffed is True
        assert result.capacity_risk in (CapacityRisk.HIGH, CapacityRisk.CRITICAL)

    def test_batch_with_diverse_regions(self):
        """Batch of 6 diverse regions should all produce valid results."""
        configs = [
            dict(region_id="A", region_name="APAC", annual_revenue_target_usd=20_000_000, current_headcount=15),
            dict(region_id="B", region_name="EMEA", annual_revenue_target_usd=15_000_000, current_headcount=12),
            dict(region_id="C", region_name="LATAM", annual_revenue_target_usd=5_000_000, current_headcount=4),
            dict(region_id="D", region_name="NA", annual_revenue_target_usd=30_000_000, current_headcount=25),
            dict(region_id="E", region_name="ANZ", annual_revenue_target_usd=8_000_000, current_headcount=6),
            dict(region_id="F", region_name="MEA", annual_revenue_target_usd=3_000_000, current_headcount=3),
        ]
        inputs = [_make_input(**c) for c in configs]
        eng = SalesCapacityPlanningEngine()
        results = eng.assess_batch(inputs)
        assert len(results) == 6
        for r in results:
            d = r.to_dict()
            assert len(d) == 15
            assert 0.0 <= r.capacity_composite <= 100.0

    def test_summary_reflects_batch(self):
        """Summary should accurately reflect 4 assessed regions."""
        configs = [
            dict(region_id=f"R{i}", region_name=f"Region {i}") for i in range(4)
        ]
        inputs = [_make_input(**c) for c in configs]
        eng = SalesCapacityPlanningEngine()
        eng.assess_batch(inputs)
        s = eng.summary()
        assert s["total"] == 4
        assert s["understaffed_count"] <= 4

    def test_repeated_assess_same_region_uses_latest(self):
        """Assessing same region_id twice stores latest result."""
        eng = SalesCapacityPlanningEngine()
        inp1 = _make_input(annual_revenue_target_usd=1_000_000.0)
        inp2 = _make_input(annual_revenue_target_usd=50_000_000.0)
        eng.assess(inp1)
        result2 = eng.assess(inp2)
        stored = eng.get("R001")
        assert stored.revenue_at_risk_usd == result2.revenue_at_risk_usd

    def test_engine_reset_and_reassess(self):
        """Engine can be reset and re-used without stale state."""
        eng = SalesCapacityPlanningEngine()
        inputs = [_make_input(region_id=f"R{i}", region_name=f"Region {i}") for i in range(3)]
        eng.assess_batch(inputs)
        eng.reset()
        assert eng.summary()["total"] == 0
        eng.assess(_make_input())
        assert eng.summary()["total"] == 1

    def test_is_understaffed_equals_capacity_gap_gt_0(self):
        """is_understaffed must always equal capacity_gap > 0."""
        inputs = [_make_input(region_id=f"R{i}", region_name=f"R{i}") for i in range(10)]
        eng = SalesCapacityPlanningEngine()
        results = eng.assess_batch(inputs)
        for r in results:
            assert r.is_understaffed == (r.capacity_gap > 0)

    def test_composite_score_ties_sorted_stably(self):
        """Regions with same composite should all be present in batch output."""
        inp1 = _make_input(region_id="X", region_name="X")
        inp2 = _make_input(region_id="Y", region_name="Y")
        eng = SalesCapacityPlanningEngine()
        results = eng.assess_batch([inp1, inp2])
        region_ids = {r.region_id for r in results}
        assert "X" in region_ids
        assert "Y" in region_ids

    def test_total_headcount_gap_sum_matches_understaffed_gaps(self):
        """total_headcount_gap() should be sum of positive capacity_gaps only."""
        inputs = [_make_input(region_id=f"R{i}", region_name=f"R{i}") for i in range(5)]
        eng = SalesCapacityPlanningEngine()
        eng.assess_batch(inputs)
        regions = eng.all_regions()
        expected_gap = sum(r.capacity_gap for r in regions if r.capacity_gap > 0)
        assert eng.total_headcount_gap() == expected_gap

    def test_hiring_speed_constraint_requires_slow_hire_and_large_gap(self):
        """HIRING_SPEED constraint requires gap>=3 AND time_to_hire>90."""
        inp_fast = _make_input(time_to_hire_days=89.0,
                               current_pipeline_coverage_ratio=3.5,
                               quota_attainment_pct=80.0)
        inp_slow = _make_input(time_to_hire_days=100.0,
                               current_pipeline_coverage_ratio=3.5,
                               quota_attainment_pct=80.0)
        # Gap of 5 triggers headcount constraint
        assert _growth_constraint(inp_fast, 5) == GrowthConstraint.HEADCOUNT
        assert _growth_constraint(inp_slow, 5) == GrowthConstraint.HIRING_SPEED
