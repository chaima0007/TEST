"""
Comprehensive pytest tests for SalesCapacityEngine.

Run with:
    python -m pytest swarm/tests/test_sales_capacity_engine.py -v
"""

from __future__ import annotations

import pytest

from swarm.intelligence.sales_capacity_engine import (
    CapacityAction,
    CapacityHealth,
    CapacityStatus,
    HiringUrgency,
    SalesCapacityEngine,
    SalesCapacityInput,
    SalesCapacityResult,
)


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> SalesCapacityInput:
    """Return a sensible baseline SalesCapacityInput, overridable per test."""
    defaults = dict(
        team_id="team-1",
        region="EMEA",
        segment="mid_market",
        manager_id="mgr-1",
        current_reps=10,
        target_reps=10,
        quota_per_rep=100_000.0,
        total_team_quota=1_000_000.0,
        avg_attainment_pct=100.0,
        new_hires_qtd=0,
        attrition_qtd=0,
        avg_ramp_months=3,
        ramping_reps=0,
        pipeline_coverage_ratio=3.0,
        avg_deal_size=20_000.0,
        avg_sales_cycle_days=45,
        historical_win_rate=0.25,
        target_growth_pct=10.0,
        days_remaining_period=60,
        productivity_score=80.0,
        open_headcount=0,
        voluntary_attrition_risk=0,
    )
    defaults.update(overrides)
    return SalesCapacityInput(**defaults)


def engine_with(*inputs: SalesCapacityInput) -> SalesCapacityEngine:
    eng = SalesCapacityEngine()
    for inp in inputs:
        eng.analyze(inp)
    return eng


# ===========================================================================
# 1.  ENUM TESTS
# ===========================================================================

class TestCapacityStatusEnum:
    def test_over_capacity_value(self):
        assert CapacityStatus.OVER_CAPACITY.value == "over_capacity"

    def test_at_capacity_value(self):
        assert CapacityStatus.AT_CAPACITY.value == "at_capacity"

    def test_under_capacity_value(self):
        assert CapacityStatus.UNDER_CAPACITY.value == "under_capacity"

    def test_critical_shortage_value(self):
        assert CapacityStatus.CRITICAL_SHORTAGE.value == "critical_shortage"

    def test_is_str_subclass(self):
        assert isinstance(CapacityStatus.OVER_CAPACITY, str)

    def test_member_count(self):
        assert len(CapacityStatus) == 4

    def test_string_comparison(self):
        assert CapacityStatus.AT_CAPACITY == "at_capacity"


class TestHiringUrgencyEnum:
    def test_immediate_value(self):
        assert HiringUrgency.IMMEDIATE.value == "immediate"

    def test_near_term_value(self):
        assert HiringUrgency.NEAR_TERM.value == "near_term"

    def test_planned_value(self):
        assert HiringUrgency.PLANNED.value == "planned"

    def test_monitor_value(self):
        assert HiringUrgency.MONITOR.value == "monitor"

    def test_member_count(self):
        assert len(HiringUrgency) == 4

    def test_is_str_subclass(self):
        assert isinstance(HiringUrgency.IMMEDIATE, str)


class TestCapacityHealthEnum:
    def test_healthy_value(self):
        assert CapacityHealth.HEALTHY.value == "healthy"

    def test_at_risk_value(self):
        assert CapacityHealth.AT_RISK.value == "at_risk"

    def test_constrained_value(self):
        assert CapacityHealth.CONSTRAINED.value == "constrained"

    def test_critical_value(self):
        assert CapacityHealth.CRITICAL.value == "critical"

    def test_member_count(self):
        assert len(CapacityHealth) == 4

    def test_is_str_subclass(self):
        assert isinstance(CapacityHealth.HEALTHY, str)


class TestCapacityActionEnum:
    def test_hire_immediately_value(self):
        assert CapacityAction.HIRE_IMMEDIATELY.value == "hire_immediately"

    def test_accelerate_ramp_value(self):
        assert CapacityAction.ACCELERATE_RAMP.value == "accelerate_ramp"

    def test_redistribute_quota_value(self):
        assert CapacityAction.REDISTRIBUTE_QUOTA.value == "redistribute_quota"

    def test_focus_productivity_value(self):
        assert CapacityAction.FOCUS_PRODUCTIVITY.value == "focus_productivity"

    def test_maintain_capacity_value(self):
        assert CapacityAction.MAINTAIN_CAPACITY.value == "maintain_capacity"

    def test_strategic_review_value(self):
        assert CapacityAction.STRATEGIC_REVIEW.value == "strategic_review"

    def test_member_count(self):
        assert len(CapacityAction) == 6

    def test_is_str_subclass(self):
        assert isinstance(CapacityAction.HIRE_IMMEDIATELY, str)


# ===========================================================================
# 2.  SalesCapacityInput DATACLASS TESTS
# ===========================================================================

class TestSalesCapacityInput:
    def test_creation_defaults(self):
        inp = make_input()
        assert inp.team_id == "team-1"
        assert inp.region == "EMEA"

    def test_all_22_fields_accessible(self):
        inp = make_input()
        fields = [
            "team_id", "region", "segment", "manager_id",
            "current_reps", "target_reps", "quota_per_rep",
            "total_team_quota", "avg_attainment_pct", "new_hires_qtd",
            "attrition_qtd", "avg_ramp_months", "ramping_reps",
            "pipeline_coverage_ratio", "avg_deal_size",
            "avg_sales_cycle_days", "historical_win_rate",
            "target_growth_pct", "days_remaining_period",
            "productivity_score", "open_headcount",
            "voluntary_attrition_risk",
        ]
        assert len(fields) == 22
        for f in fields:
            assert hasattr(inp, f)

    def test_field_types(self):
        inp = make_input()
        assert isinstance(inp.current_reps, int)
        assert isinstance(inp.quota_per_rep, float)
        assert isinstance(inp.team_id, str)

    def test_override_works(self):
        inp = make_input(current_reps=5, region="APAC")
        assert inp.current_reps == 5
        assert inp.region == "APAC"


# ===========================================================================
# 3.  SalesCapacityResult.to_dict() TESTS
# ===========================================================================

class TestSalesCapacityResultToDict:
    def _result(self, **overrides) -> SalesCapacityResult:
        eng = SalesCapacityEngine()
        return eng.analyze(make_input(**overrides))

    def test_to_dict_has_exactly_15_keys(self):
        d = self._result().to_dict()
        assert len(d) == 15

    def test_to_dict_exact_keys(self):
        expected_keys = {
            "team_id", "region", "capacity_status", "hiring_urgency",
            "capacity_health", "capacity_action", "effective_capacity_pct",
            "headcount_gap", "quota_at_risk", "pipeline_per_rep",
            "required_attainment", "ramp_impact", "productivity_index",
            "is_capacity_constrained", "needs_immediate_hire",
        }
        assert set(self._result().to_dict().keys()) == expected_keys

    def test_to_dict_enum_values_are_strings(self):
        d = self._result().to_dict()
        assert isinstance(d["capacity_status"], str)
        assert isinstance(d["hiring_urgency"], str)
        assert isinstance(d["capacity_health"], str)
        assert isinstance(d["capacity_action"], str)

    def test_to_dict_team_id_passthrough(self):
        d = self._result(team_id="my-team").to_dict()
        assert d["team_id"] == "my-team"

    def test_to_dict_region_passthrough(self):
        d = self._result(region="NA").to_dict()
        assert d["region"] == "NA"

    def test_to_dict_booleans(self):
        d = self._result().to_dict()
        assert isinstance(d["is_capacity_constrained"], bool)
        assert isinstance(d["needs_immediate_hire"], bool)

    def test_to_dict_numeric_fields_are_numbers(self):
        d = self._result().to_dict()
        for key in [
            "effective_capacity_pct", "quota_at_risk", "pipeline_per_rep",
            "required_attainment", "ramp_impact", "productivity_index",
        ]:
            assert isinstance(d[key], (int, float))

    def test_to_dict_headcount_gap_is_int(self):
        d = self._result().to_dict()
        assert isinstance(d["headcount_gap"], int)


# ===========================================================================
# 4.  _effective_capacity_pct TESTS
# ===========================================================================

class TestEffectiveCapacityPct:
    def _eff(self, **kw) -> float:
        eng = SalesCapacityEngine()
        return eng._effective_capacity_pct(make_input(**kw))

    def test_basic_full_capacity(self):
        # 10 reps, 0 ramping, 100% attainment, 10 target → 100%
        assert self._eff(current_reps=10, target_reps=10, ramping_reps=0,
                         avg_attainment_pct=100.0) == 100.0

    def test_ramping_reduces_capacity(self):
        # 10 reps, 2 ramping: effective = (10 - 2*0.6)/10 * 100 = (10-1.2)/10*100 = 88
        result = self._eff(current_reps=10, target_reps=10, ramping_reps=2,
                           avg_attainment_pct=100.0)
        assert result == pytest.approx(88.0, abs=0.11)

    def test_lower_attainment_scales_down(self):
        # 10 reps, 0 ramping, 80% attainment → 80%
        result = self._eff(current_reps=10, target_reps=10, ramping_reps=0,
                           avg_attainment_pct=80.0)
        assert result == pytest.approx(80.0, abs=0.11)

    def test_over_target_reps_gives_over_100(self):
        # 15 reps vs 10 target, 100% attainment → 150%
        result = self._eff(current_reps=15, target_reps=10, ramping_reps=0,
                           avg_attainment_pct=100.0)
        assert result == 150.0

    def test_clamped_at_150(self):
        # Would be 200 without clamp: 20 reps, 10 target, 100%
        result = self._eff(current_reps=20, target_reps=10, ramping_reps=0,
                           avg_attainment_pct=100.0)
        assert result == 150.0

    def test_clamped_at_zero_when_all_ramping(self):
        # All 10 reps are ramping: effective = 10 - 10*0.6 = 4
        # 4/10 * 100 = 40 → not zero
        result = self._eff(current_reps=10, target_reps=10, ramping_reps=10,
                           avg_attainment_pct=100.0)
        assert result == pytest.approx(40.0, abs=0.11)

    def test_zero_target_reps_returns_zero(self):
        result = self._eff(target_reps=0)
        assert result == 0.0

    def test_negative_effective_reps_clamped_to_zero(self):
        # ramping_reps > current_reps → effective_reps would be negative
        result = self._eff(current_reps=5, target_reps=10, ramping_reps=10,
                           avg_attainment_pct=100.0)
        assert result == 0.0

    def test_half_attainment_half_capacity(self):
        # 10 reps, 10 target, 50% attainment → 50%
        result = self._eff(current_reps=10, target_reps=10, ramping_reps=0,
                           avg_attainment_pct=50.0)
        assert result == pytest.approx(50.0, abs=0.11)

    def test_result_rounded_to_one_decimal(self):
        # 7 reps, 10 target, 100% attainment, 0 ramping → 70.0
        result = self._eff(current_reps=7, target_reps=10, ramping_reps=0,
                           avg_attainment_pct=100.0)
        assert result == 70.0

    def test_boundary_exactly_100(self):
        result = self._eff(current_reps=10, target_reps=10, ramping_reps=0,
                           avg_attainment_pct=100.0)
        assert result == 100.0

    def test_boundary_just_below_100(self):
        # 9 reps, 10 target, 100% attainment, 0 ramping → 90.0
        result = self._eff(current_reps=9, target_reps=10, ramping_reps=0,
                           avg_attainment_pct=100.0)
        assert result == 90.0

    def test_ramp_impact_calculation_precision(self):
        # 10 reps, 1 ramping, 100% attainment, 10 target
        # effective = (10 - 0.6) / 10 * 100 = 9.4/10*100 = 94.0
        result = self._eff(current_reps=10, target_reps=10, ramping_reps=1,
                           avg_attainment_pct=100.0)
        assert result == pytest.approx(94.0, abs=0.11)

    def test_zero_attainment_gives_zero(self):
        result = self._eff(current_reps=10, target_reps=10, ramping_reps=0,
                           avg_attainment_pct=0.0)
        assert result == 0.0

    def test_large_team_over_target(self):
        result = self._eff(current_reps=100, target_reps=10, ramping_reps=0,
                           avg_attainment_pct=100.0)
        assert result == 150.0  # clamped


# ===========================================================================
# 5.  _headcount_gap TESTS
# ===========================================================================

class TestHeadcountGap:
    def _gap(self, **kw) -> int:
        return SalesCapacityEngine()._headcount_gap(make_input(**kw))

    def test_no_gap_when_at_target(self):
        assert self._gap(current_reps=10, target_reps=10) == 0

    def test_gap_when_under(self):
        assert self._gap(current_reps=7, target_reps=10) == 3

    def test_no_gap_when_over(self):
        assert self._gap(current_reps=12, target_reps=10) == 0

    def test_max_is_zero_not_negative(self):
        assert self._gap(current_reps=15, target_reps=10) == 0

    def test_gap_of_one(self):
        assert self._gap(current_reps=9, target_reps=10) == 1

    def test_gap_of_five(self):
        assert self._gap(current_reps=5, target_reps=10) == 5

    def test_zero_reps_zero_target(self):
        assert self._gap(current_reps=0, target_reps=0) == 0

    def test_zero_current_reps(self):
        assert self._gap(current_reps=0, target_reps=10) == 10

    def test_returns_int(self):
        result = self._gap(current_reps=8, target_reps=10)
        assert isinstance(result, int)


# ===========================================================================
# 6.  _quota_at_risk TESTS
# ===========================================================================

class TestQuotaAtRisk:
    def _risk(self, eff_cap: float, total_quota: float = 1_000_000.0) -> float:
        eng = SalesCapacityEngine()
        inp = make_input(total_team_quota=total_quota)
        return eng._quota_at_risk(inp, eff_cap)

    def test_no_risk_at_100_capacity(self):
        assert self._risk(100.0) == 0.0

    def test_no_risk_above_100_capacity(self):
        assert self._risk(120.0) == 0.0

    def test_50pct_capacity_half_at_risk(self):
        result = self._risk(50.0, 1_000_000.0)
        assert result == pytest.approx(500_000.0, abs=0.01)

    def test_zero_capacity_all_at_risk(self):
        result = self._risk(0.0, 1_000_000.0)
        assert result == 1_000_000.0

    def test_80pct_capacity_20pct_at_risk(self):
        result = self._risk(80.0, 1_000_000.0)
        assert result == pytest.approx(200_000.0, abs=0.01)

    def test_result_rounded_to_2_decimal_places(self):
        result = self._risk(33.33, 1_000.0)
        assert result == round(1_000.0 * max(0.0, 1 - 33.33 / 100), 2)

    def test_eff_cap_150_no_risk(self):
        assert self._risk(150.0) == 0.0

    def test_small_quota(self):
        result = self._risk(50.0, 100.0)
        assert result == pytest.approx(50.0, abs=0.01)


# ===========================================================================
# 7.  _pipeline_per_rep TESTS
# ===========================================================================

class TestPipelinePerRep:
    def _ppr(self, **kw) -> float:
        return SalesCapacityEngine()._pipeline_per_rep(make_input(**kw))

    def test_basic_calculation(self):
        # quota=1M, ratio=3, reps=10 → pipeline=3M, per rep=300k
        result = self._ppr(total_team_quota=1_000_000.0,
                           pipeline_coverage_ratio=3.0, current_reps=10)
        assert result == pytest.approx(300_000.0, abs=0.01)

    def test_zero_current_reps_uses_one(self):
        result = self._ppr(total_team_quota=1_000_000.0,
                           pipeline_coverage_ratio=2.0, current_reps=0)
        assert result == pytest.approx(2_000_000.0, abs=0.01)

    def test_one_rep(self):
        result = self._ppr(total_team_quota=500_000.0,
                           pipeline_coverage_ratio=2.0, current_reps=1)
        assert result == pytest.approx(1_000_000.0, abs=0.01)

    def test_result_rounded_to_2_decimals(self):
        result = self._ppr(total_team_quota=100_000.0,
                           pipeline_coverage_ratio=1.0, current_reps=3)
        assert result == round(100_000.0 / 3, 2)

    def test_pipeline_ratio_zero(self):
        result = self._ppr(total_team_quota=1_000_000.0,
                           pipeline_coverage_ratio=0.0, current_reps=5)
        assert result == 0.0

    def test_large_team(self):
        result = self._ppr(total_team_quota=1_000_000.0,
                           pipeline_coverage_ratio=2.0, current_reps=20)
        assert result == pytest.approx(100_000.0, abs=0.01)


# ===========================================================================
# 8.  _required_attainment TESTS
# ===========================================================================

class TestRequiredAttainment:
    def _req(self, **kw) -> float:
        return SalesCapacityEngine()._required_attainment(make_input(**kw))

    def test_basic_100pct(self):
        # quota=1M, 10 reps, 100k per rep → needed = 1M/1M * 100 = 100%
        result = self._req(total_team_quota=1_000_000.0, current_reps=10,
                           quota_per_rep=100_000.0)
        assert result == 100.0

    def test_requires_more_when_fewer_reps(self):
        # quota=1M, 5 reps, 100k per rep → needed = 1M/500k * 100 = 200%
        result = self._req(total_team_quota=1_000_000.0, current_reps=5,
                           quota_per_rep=100_000.0)
        assert result == 200.0  # clamped

    def test_clamped_at_200(self):
        result = self._req(total_team_quota=2_000_000.0, current_reps=1,
                           quota_per_rep=100_000.0)
        assert result == 200.0

    def test_zero_current_reps_returns_200(self):
        result = self._req(current_reps=0, quota_per_rep=100_000.0)
        assert result == 200.0

    def test_zero_quota_per_rep_returns_200(self):
        result = self._req(current_reps=10, quota_per_rep=0.0)
        assert result == 200.0

    def test_lower_quota_reduces_required_attainment(self):
        # quota=500k, 10 reps, 100k per rep → 50%
        result = self._req(total_team_quota=500_000.0, current_reps=10,
                           quota_per_rep=100_000.0)
        assert result == pytest.approx(50.0, abs=0.11)

    def test_result_rounded_to_one_decimal(self):
        # quota=333_333, 10 reps, 100k per rep
        result = self._req(total_team_quota=333_333.0, current_reps=10,
                           quota_per_rep=100_000.0)
        expected = round(min(200.0, 333_333.0 / (10 * 100_000.0) * 100), 1)
        assert result == expected

    def test_exactly_130_pct(self):
        result = self._req(total_team_quota=1_300_000.0, current_reps=10,
                           quota_per_rep=100_000.0)
        assert result == pytest.approx(130.0, abs=0.11)

    def test_exactly_110_pct(self):
        result = self._req(total_team_quota=1_100_000.0, current_reps=10,
                           quota_per_rep=100_000.0)
        assert result == pytest.approx(110.0, abs=0.11)


# ===========================================================================
# 9.  _ramp_impact TESTS
# ===========================================================================

class TestRampImpact:
    def _ri(self, **kw) -> float:
        return SalesCapacityEngine()._ramp_impact(make_input(**kw))

    def test_no_ramping_zero_impact(self):
        assert self._ri(current_reps=10, ramping_reps=0) == 0.0

    def test_half_team_ramping(self):
        result = self._ri(current_reps=10, ramping_reps=5)
        assert result == pytest.approx(50.0, abs=0.11)

    def test_all_ramping_100pct(self):
        result = self._ri(current_reps=10, ramping_reps=10)
        assert result == 100.0

    def test_over_100pct_clamped(self):
        # ramping_reps can technically exceed current_reps in bad data
        result = self._ri(current_reps=5, ramping_reps=10)
        assert result == 100.0

    def test_zero_current_reps_returns_zero(self):
        result = self._ri(current_reps=0, ramping_reps=0)
        assert result == 0.0

    def test_one_of_ten_ramping(self):
        result = self._ri(current_reps=10, ramping_reps=1)
        assert result == pytest.approx(10.0, abs=0.11)

    def test_result_rounded_to_one_decimal(self):
        result = self._ri(current_reps=7, ramping_reps=2)
        expected = round(min(100.0, 2 / 7 * 100), 1)
        assert result == expected

    def test_clamped_at_100(self):
        result = self._ri(current_reps=1, ramping_reps=100)
        assert result == 100.0


# ===========================================================================
# 10.  _productivity_index TESTS
# ===========================================================================

class TestProductivityIndex:
    def _pi(self, **kw) -> float:
        eng = SalesCapacityEngine()
        inp = make_input(**kw)
        ramp_impact = eng._ramp_impact(inp)
        return eng._productivity_index(inp, ramp_impact)

    def test_no_penalties_equals_productivity_score(self):
        # No ramping, no attrition risk → index == productivity_score
        result = self._pi(productivity_score=80.0, ramping_reps=0,
                          voluntary_attrition_risk=0, current_reps=10)
        assert result == pytest.approx(80.0, abs=0.11)

    def test_ramp_penalty_applied(self):
        # 50% ramp impact → penalty = 50/200 = 0.25 → 80 * 0.75 = 60
        result = self._pi(productivity_score=80.0, current_reps=10,
                          ramping_reps=5, voluntary_attrition_risk=0)
        assert result == pytest.approx(60.0, abs=0.11)

    def test_attrition_risk_penalty(self):
        # No ramping, 1 attrition risk out of 10 reps
        # penalty = (1/10)*10 = 1 → 80 - 1 = 79
        result = self._pi(productivity_score=80.0, current_reps=10,
                          ramping_reps=0, voluntary_attrition_risk=1)
        assert result == pytest.approx(79.0, abs=0.11)

    def test_clamped_at_zero(self):
        # extreme penalties
        result = self._pi(productivity_score=0.0, current_reps=1,
                          ramping_reps=1, voluntary_attrition_risk=100)
        assert result == 0.0

    def test_clamped_at_100(self):
        # cannot exceed 100
        result = self._pi(productivity_score=100.0, current_reps=10,
                          ramping_reps=0, voluntary_attrition_risk=0)
        assert result == 100.0

    def test_both_penalties_combined(self):
        # productivity=80, 50% ramping (penalty=0.25), 1 of 10 attrition risk
        # ramp_impact = 50, idx = 80*(1-0.25) = 60, then 60 - (1/10)*10 = 59
        result = self._pi(productivity_score=80.0, current_reps=10,
                          ramping_reps=5, voluntary_attrition_risk=1)
        assert result == pytest.approx(59.0, abs=0.11)

    def test_zero_current_reps_no_attrition_penalty(self):
        # when current_reps=0, attrition risk penalty is skipped
        eng = SalesCapacityEngine()
        inp = make_input(productivity_score=70.0, current_reps=0,
                         ramping_reps=0, voluntary_attrition_risk=5)
        ri = eng._ramp_impact(inp)  # 0 because current=0
        result = eng._productivity_index(inp, ri)
        assert result == pytest.approx(70.0, abs=0.11)

    def test_result_rounded_to_one_decimal(self):
        eng = SalesCapacityEngine()
        inp = make_input(productivity_score=77.7, current_reps=7,
                         ramping_reps=1, voluntary_attrition_risk=0)
        ri = eng._ramp_impact(inp)
        result = eng._productivity_index(inp, ri)
        ramp_penalty = ri / 200.0
        expected = round(max(0.0, min(100.0, 77.7 * (1 - ramp_penalty))), 1)
        assert result == expected

    def test_high_attrition_risk_clamps_to_zero(self):
        result = self._pi(productivity_score=5.0, current_reps=1,
                          ramping_reps=0, voluntary_attrition_risk=10)
        assert result == 0.0


# ===========================================================================
# 11.  _capacity_status TESTS
# ===========================================================================

class TestCapacityStatus:
    def _status(self, eff_cap: float) -> CapacityStatus:
        return SalesCapacityEngine()._capacity_status(eff_cap)

    def test_100_is_over_capacity(self):
        assert self._status(100.0) == CapacityStatus.OVER_CAPACITY

    def test_150_is_over_capacity(self):
        assert self._status(150.0) == CapacityStatus.OVER_CAPACITY

    def test_100_1_is_over_capacity(self):
        assert self._status(100.1) == CapacityStatus.OVER_CAPACITY

    def test_99_9_is_at_capacity(self):
        assert self._status(99.9) == CapacityStatus.AT_CAPACITY

    def test_80_is_at_capacity(self):
        assert self._status(80.0) == CapacityStatus.AT_CAPACITY

    def test_79_9_is_under_capacity(self):
        assert self._status(79.9) == CapacityStatus.UNDER_CAPACITY

    def test_60_is_under_capacity(self):
        assert self._status(60.0) == CapacityStatus.UNDER_CAPACITY

    def test_59_9_is_critical_shortage(self):
        assert self._status(59.9) == CapacityStatus.CRITICAL_SHORTAGE

    def test_zero_is_critical_shortage(self):
        assert self._status(0.0) == CapacityStatus.CRITICAL_SHORTAGE

    def test_midpoint_90_is_at_capacity(self):
        assert self._status(90.0) == CapacityStatus.AT_CAPACITY

    def test_midpoint_70_is_under_capacity(self):
        assert self._status(70.0) == CapacityStatus.UNDER_CAPACITY

    def test_midpoint_30_is_critical_shortage(self):
        assert self._status(30.0) == CapacityStatus.CRITICAL_SHORTAGE


# ===========================================================================
# 12.  _hiring_urgency TESTS
# ===========================================================================

class TestHiringUrgency:
    def _urgency(self, status: CapacityStatus, gap: int) -> HiringUrgency:
        return SalesCapacityEngine()._hiring_urgency(status, gap)

    def test_critical_shortage_always_immediate(self):
        assert self._urgency(CapacityStatus.CRITICAL_SHORTAGE, 0) == HiringUrgency.IMMEDIATE

    def test_critical_shortage_with_gap_still_immediate(self):
        assert self._urgency(CapacityStatus.CRITICAL_SHORTAGE, 5) == HiringUrgency.IMMEDIATE

    def test_gap_3_near_term(self):
        assert self._urgency(CapacityStatus.AT_CAPACITY, 3) == HiringUrgency.NEAR_TERM

    def test_gap_5_near_term(self):
        assert self._urgency(CapacityStatus.AT_CAPACITY, 5) == HiringUrgency.NEAR_TERM

    def test_gap_2_planned(self):
        assert self._urgency(CapacityStatus.AT_CAPACITY, 2) == HiringUrgency.PLANNED

    def test_gap_1_planned(self):
        assert self._urgency(CapacityStatus.AT_CAPACITY, 1) == HiringUrgency.PLANNED

    def test_gap_0_monitor(self):
        assert self._urgency(CapacityStatus.AT_CAPACITY, 0) == HiringUrgency.MONITOR

    def test_over_capacity_no_gap_monitor(self):
        assert self._urgency(CapacityStatus.OVER_CAPACITY, 0) == HiringUrgency.MONITOR

    def test_under_capacity_gap_3_near_term(self):
        assert self._urgency(CapacityStatus.UNDER_CAPACITY, 3) == HiringUrgency.NEAR_TERM

    def test_under_capacity_gap_0_monitor(self):
        assert self._urgency(CapacityStatus.UNDER_CAPACITY, 0) == HiringUrgency.MONITOR

    def test_boundary_gap_exactly_3(self):
        assert self._urgency(CapacityStatus.OVER_CAPACITY, 3) == HiringUrgency.NEAR_TERM

    def test_boundary_gap_exactly_1(self):
        assert self._urgency(CapacityStatus.OVER_CAPACITY, 1) == HiringUrgency.PLANNED


# ===========================================================================
# 13.  _capacity_health TESTS
# ===========================================================================

class TestCapacityHealth:
    def _health(self, status: CapacityStatus, req: float, **kw) -> CapacityHealth:
        eng = SalesCapacityEngine()
        inp = make_input(**kw)
        return eng._capacity_health(inp, status, req)

    def test_critical_shortage_is_critical(self):
        assert self._health(CapacityStatus.CRITICAL_SHORTAGE, 100.0) == CapacityHealth.CRITICAL

    def test_req_above_130_is_critical(self):
        assert self._health(CapacityStatus.AT_CAPACITY, 131.0) == CapacityHealth.CRITICAL

    def test_req_exactly_130_not_critical(self):
        # req > 130 triggers CRITICAL, exactly 130 does not
        result = self._health(CapacityStatus.AT_CAPACITY, 130.0,
                              attrition_qtd=0, voluntary_attrition_risk=0)
        assert result != CapacityHealth.CRITICAL

    def test_under_capacity_is_constrained(self):
        assert self._health(CapacityStatus.UNDER_CAPACITY, 100.0,
                            attrition_qtd=0, voluntary_attrition_risk=0) == CapacityHealth.CONSTRAINED

    def test_req_above_110_is_constrained(self):
        assert self._health(CapacityStatus.AT_CAPACITY, 111.0,
                            attrition_qtd=0, voluntary_attrition_risk=0) == CapacityHealth.CONSTRAINED

    def test_req_exactly_110_not_constrained(self):
        result = self._health(CapacityStatus.AT_CAPACITY, 110.0,
                              attrition_qtd=0, voluntary_attrition_risk=0)
        assert result not in (CapacityHealth.CRITICAL, CapacityHealth.CONSTRAINED)

    def test_attrition_qtd_gives_at_risk(self):
        assert self._health(CapacityStatus.AT_CAPACITY, 90.0,
                            attrition_qtd=1, voluntary_attrition_risk=0) == CapacityHealth.AT_RISK

    def test_voluntary_attrition_risk_gives_at_risk(self):
        assert self._health(CapacityStatus.AT_CAPACITY, 90.0,
                            attrition_qtd=0, voluntary_attrition_risk=1) == CapacityHealth.AT_RISK

    def test_healthy_when_no_issues(self):
        assert self._health(CapacityStatus.AT_CAPACITY, 90.0,
                            attrition_qtd=0, voluntary_attrition_risk=0) == CapacityHealth.HEALTHY

    def test_healthy_over_capacity_no_attrition(self):
        assert self._health(CapacityStatus.OVER_CAPACITY, 80.0,
                            attrition_qtd=0, voluntary_attrition_risk=0) == CapacityHealth.HEALTHY

    def test_req_130_1_triggers_critical(self):
        assert self._health(CapacityStatus.AT_CAPACITY, 130.1,
                            attrition_qtd=0, voluntary_attrition_risk=0) == CapacityHealth.CRITICAL

    def test_req_110_1_triggers_constrained(self):
        assert self._health(CapacityStatus.AT_CAPACITY, 110.1,
                            attrition_qtd=0, voluntary_attrition_risk=0) == CapacityHealth.CONSTRAINED


# ===========================================================================
# 14.  _capacity_action TESTS
# ===========================================================================

class TestCapacityAction:
    def _action(self, status: CapacityStatus, urgency: HiringUrgency,
                ramp_impact: float, prod_idx: float, **kw) -> CapacityAction:
        eng = SalesCapacityEngine()
        inp = make_input(**kw)
        return eng._capacity_action(inp, status, urgency, ramp_impact, prod_idx)

    def test_critical_shortage_hire_immediately(self):
        result = self._action(CapacityStatus.CRITICAL_SHORTAGE, HiringUrgency.IMMEDIATE,
                              0.0, 80.0)
        assert result == CapacityAction.HIRE_IMMEDIATELY

    def test_critical_shortage_overrides_ramp_impact(self):
        # Even with ramp_impact > 50, CRITICAL_SHORTAGE → HIRE_IMMEDIATELY
        result = self._action(CapacityStatus.CRITICAL_SHORTAGE, HiringUrgency.IMMEDIATE,
                              60.0, 80.0)
        assert result == CapacityAction.HIRE_IMMEDIATELY

    def test_high_ramp_impact_accelerate_ramp(self):
        result = self._action(CapacityStatus.AT_CAPACITY, HiringUrgency.MONITOR,
                              51.0, 80.0)
        assert result == CapacityAction.ACCELERATE_RAMP

    def test_ramp_impact_exactly_50_not_accelerate(self):
        result = self._action(CapacityStatus.AT_CAPACITY, HiringUrgency.NEAR_TERM,
                              50.0, 80.0, pipeline_coverage_ratio=3.0)
        assert result != CapacityAction.ACCELERATE_RAMP

    def test_near_term_low_pipeline_redistribute(self):
        result = self._action(CapacityStatus.AT_CAPACITY, HiringUrgency.NEAR_TERM,
                              0.0, 80.0, pipeline_coverage_ratio=1.5)
        assert result == CapacityAction.REDISTRIBUTE_QUOTA

    def test_near_term_pipeline_exactly_2_not_redistribute(self):
        result = self._action(CapacityStatus.AT_CAPACITY, HiringUrgency.NEAR_TERM,
                              0.0, 80.0, pipeline_coverage_ratio=2.0)
        assert result != CapacityAction.REDISTRIBUTE_QUOTA

    def test_at_capacity_low_productivity_focus_productivity(self):
        result = self._action(CapacityStatus.AT_CAPACITY, HiringUrgency.MONITOR,
                              0.0, 69.9)
        assert result == CapacityAction.FOCUS_PRODUCTIVITY

    def test_at_capacity_productivity_exactly_70_not_focus(self):
        result = self._action(CapacityStatus.AT_CAPACITY, HiringUrgency.MONITOR,
                              0.0, 70.0)
        assert result != CapacityAction.FOCUS_PRODUCTIVITY

    def test_at_capacity_good_productivity_maintain(self):
        result = self._action(CapacityStatus.AT_CAPACITY, HiringUrgency.MONITOR,
                              0.0, 80.0, pipeline_coverage_ratio=3.0)
        assert result == CapacityAction.MAINTAIN_CAPACITY

    def test_over_capacity_maintain(self):
        result = self._action(CapacityStatus.OVER_CAPACITY, HiringUrgency.MONITOR,
                              0.0, 80.0)
        assert result == CapacityAction.MAINTAIN_CAPACITY

    def test_else_strategic_review(self):
        # UNDER_CAPACITY, no ramp issue, not near-term
        result = self._action(CapacityStatus.UNDER_CAPACITY, HiringUrgency.MONITOR,
                              0.0, 80.0)
        assert result == CapacityAction.STRATEGIC_REVIEW

    def test_near_term_high_pipeline_no_redistribute(self):
        # NEAR_TERM but pipeline >= 2.0, no critical/ramp → check next rule
        result = self._action(CapacityStatus.UNDER_CAPACITY, HiringUrgency.NEAR_TERM,
                              0.0, 80.0, pipeline_coverage_ratio=3.0)
        assert result == CapacityAction.STRATEGIC_REVIEW


# ===========================================================================
# 15.  is_capacity_constrained & needs_immediate_hire TESTS
# ===========================================================================

class TestBooleanFlags:
    def test_under_capacity_is_constrained(self):
        eng = SalesCapacityEngine()
        # Force UNDER_CAPACITY: eff_cap in [60, 80)
        result = eng.analyze(make_input(current_reps=7, target_reps=10,
                                        ramping_reps=0, avg_attainment_pct=100.0))
        assert result.is_capacity_constrained is True

    def test_critical_shortage_is_constrained(self):
        eng = SalesCapacityEngine()
        result = eng.analyze(make_input(current_reps=5, target_reps=10,
                                        ramping_reps=0, avg_attainment_pct=100.0))
        assert result.is_capacity_constrained is True

    def test_at_capacity_not_constrained(self):
        eng = SalesCapacityEngine()
        result = eng.analyze(make_input(current_reps=9, target_reps=10,
                                        ramping_reps=0, avg_attainment_pct=100.0))
        # 90% → AT_CAPACITY
        assert result.capacity_status == CapacityStatus.AT_CAPACITY
        assert result.is_capacity_constrained is False

    def test_over_capacity_not_constrained(self):
        eng = SalesCapacityEngine()
        result = eng.analyze(make_input(current_reps=10, target_reps=10,
                                        ramping_reps=0, avg_attainment_pct=100.0))
        assert result.capacity_status == CapacityStatus.OVER_CAPACITY
        assert result.is_capacity_constrained is False

    def test_immediate_urgency_needs_immediate_hire(self):
        eng = SalesCapacityEngine()
        # CRITICAL_SHORTAGE → IMMEDIATE
        result = eng.analyze(make_input(current_reps=5, target_reps=10,
                                        ramping_reps=0, avg_attainment_pct=100.0))
        assert result.needs_immediate_hire is True

    def test_non_immediate_does_not_need_hire(self):
        eng = SalesCapacityEngine()
        result = eng.analyze(make_input(current_reps=10, target_reps=10,
                                        ramping_reps=0, avg_attainment_pct=100.0))
        assert result.needs_immediate_hire is False

    def test_planned_urgency_no_immediate_hire(self):
        eng = SalesCapacityEngine()
        # AT_CAPACITY with gap=1 → PLANNED
        result = eng.analyze(make_input(current_reps=9, target_reps=10,
                                        ramping_reps=0, avg_attainment_pct=100.0))
        assert result.needs_immediate_hire is False


# ===========================================================================
# 16.  analyze() method TESTS
# ===========================================================================

class TestAnalyzeMethod:
    def test_analyze_returns_result_type(self):
        eng = SalesCapacityEngine()
        result = eng.analyze(make_input())
        assert isinstance(result, SalesCapacityResult)

    def test_analyze_stores_result(self):
        eng = SalesCapacityEngine()
        eng.analyze(make_input(team_id="t1"))
        assert len(eng._results) == 1

    def test_analyze_accumulates_results(self):
        eng = SalesCapacityEngine()
        eng.analyze(make_input(team_id="t1"))
        eng.analyze(make_input(team_id="t2"))
        assert len(eng._results) == 2

    def test_analyze_preserves_team_id(self):
        eng = SalesCapacityEngine()
        result = eng.analyze(make_input(team_id="special-team"))
        assert result.team_id == "special-team"

    def test_analyze_preserves_region(self):
        eng = SalesCapacityEngine()
        result = eng.analyze(make_input(region="LATAM"))
        assert result.region == "LATAM"

    def test_analyze_healthy_full_team(self):
        eng = SalesCapacityEngine()
        inp = make_input(current_reps=10, target_reps=10, ramping_reps=0,
                         avg_attainment_pct=100.0, attrition_qtd=0,
                         voluntary_attrition_risk=0)
        result = eng.analyze(inp)
        assert result.capacity_status == CapacityStatus.OVER_CAPACITY
        assert result.capacity_health == CapacityHealth.HEALTHY

    def test_analyze_critical_team(self):
        eng = SalesCapacityEngine()
        inp = make_input(current_reps=3, target_reps=10, ramping_reps=0,
                         avg_attainment_pct=100.0)
        result = eng.analyze(inp)
        assert result.capacity_status == CapacityStatus.CRITICAL_SHORTAGE

    def test_analyze_result_has_all_fields(self):
        eng = SalesCapacityEngine()
        result = eng.analyze(make_input())
        for attr in [
            "team_id", "region", "capacity_status", "hiring_urgency",
            "capacity_health", "capacity_action", "effective_capacity_pct",
            "headcount_gap", "quota_at_risk", "pipeline_per_rep",
            "required_attainment", "ramp_impact", "productivity_index",
            "is_capacity_constrained", "needs_immediate_hire",
        ]:
            assert hasattr(result, attr)


# ===========================================================================
# 17.  analyze_batch() TESTS
# ===========================================================================

class TestAnalyzeBatch:
    def test_batch_returns_list(self):
        eng = SalesCapacityEngine()
        results = eng.analyze_batch([make_input(team_id="t1"),
                                     make_input(team_id="t2")])
        assert isinstance(results, list)
        assert len(results) == 2

    def test_batch_stores_results(self):
        eng = SalesCapacityEngine()
        eng.analyze_batch([make_input(team_id="t1"), make_input(team_id="t2")])
        assert len(eng._results) == 2

    def test_batch_empty_list(self):
        eng = SalesCapacityEngine()
        results = eng.analyze_batch([])
        assert results == []

    def test_batch_order_preserved(self):
        eng = SalesCapacityEngine()
        results = eng.analyze_batch([make_input(team_id="a"), make_input(team_id="b")])
        assert results[0].team_id == "a"
        assert results[1].team_id == "b"

    def test_batch_single_item(self):
        eng = SalesCapacityEngine()
        results = eng.analyze_batch([make_input(team_id="solo")])
        assert len(results) == 1
        assert results[0].team_id == "solo"


# ===========================================================================
# 18.  reset() TESTS
# ===========================================================================

class TestReset:
    def test_reset_clears_results(self):
        eng = SalesCapacityEngine()
        eng.analyze(make_input())
        eng.reset()
        assert len(eng._results) == 0

    def test_reset_then_analyze(self):
        eng = SalesCapacityEngine()
        eng.analyze(make_input(team_id="old"))
        eng.reset()
        eng.analyze(make_input(team_id="new"))
        assert len(eng._results) == 1
        assert eng._results[0].team_id == "new"

    def test_reset_empty_engine(self):
        eng = SalesCapacityEngine()
        eng.reset()  # should not raise
        assert len(eng._results) == 0

    def test_reset_multiple_times(self):
        eng = SalesCapacityEngine()
        eng.analyze(make_input())
        eng.reset()
        eng.reset()
        assert len(eng._results) == 0


# ===========================================================================
# 19.  PROPERTIES TESTS
# ===========================================================================

class TestProperties:
    def test_constrained_teams_empty_initially(self):
        eng = SalesCapacityEngine()
        assert eng.constrained_teams == []

    def test_constrained_teams_filters_correctly(self):
        eng = SalesCapacityEngine()
        # CRITICAL_SHORTAGE → constrained
        eng.analyze(make_input(team_id="c", current_reps=3, target_reps=10,
                               ramping_reps=0, avg_attainment_pct=100.0))
        # OVER_CAPACITY → not constrained
        eng.analyze(make_input(team_id="f", current_reps=10, target_reps=10,
                               ramping_reps=0, avg_attainment_pct=100.0))
        constrained = eng.constrained_teams
        assert len(constrained) == 1
        assert constrained[0].team_id == "c"

    def test_immediate_hire_teams_filters(self):
        eng = SalesCapacityEngine()
        eng.analyze(make_input(team_id="crit", current_reps=3, target_reps=10,
                               ramping_reps=0, avg_attainment_pct=100.0))
        eng.analyze(make_input(team_id="ok", current_reps=10, target_reps=10,
                               ramping_reps=0, avg_attainment_pct=100.0))
        assert len(eng.immediate_hire_teams) == 1
        assert eng.immediate_hire_teams[0].team_id == "crit"

    def test_critical_teams_filters_by_health(self):
        eng = SalesCapacityEngine()
        # CRITICAL_SHORTAGE → CRITICAL health
        eng.analyze(make_input(team_id="bad", current_reps=2, target_reps=10,
                               ramping_reps=0, avg_attainment_pct=100.0))
        # healthy
        eng.analyze(make_input(team_id="good", current_reps=10, target_reps=10,
                               ramping_reps=0, avg_attainment_pct=100.0,
                               attrition_qtd=0, voluntary_attrition_risk=0))
        assert len(eng.critical_teams) == 1
        assert eng.critical_teams[0].team_id == "bad"

    def test_total_quota_at_risk_sum(self):
        eng = SalesCapacityEngine()
        r1 = eng.analyze(make_input(team_id="t1", total_team_quota=1_000_000.0,
                                    current_reps=5, target_reps=10,
                                    ramping_reps=0, avg_attainment_pct=100.0))
        r2 = eng.analyze(make_input(team_id="t2", total_team_quota=1_000_000.0,
                                    current_reps=10, target_reps=10,
                                    ramping_reps=0, avg_attainment_pct=100.0))
        expected = round(r1.quota_at_risk + r2.quota_at_risk, 2)
        assert eng.total_quota_at_risk == expected

    def test_total_quota_at_risk_zero_when_all_healthy(self):
        eng = SalesCapacityEngine()
        eng.analyze(make_input(current_reps=10, target_reps=10,
                               ramping_reps=0, avg_attainment_pct=100.0))
        assert eng.total_quota_at_risk == 0.0

    def test_total_headcount_gap_sum(self):
        eng = SalesCapacityEngine()
        eng.analyze(make_input(team_id="t1", current_reps=8, target_reps=10))
        eng.analyze(make_input(team_id="t2", current_reps=7, target_reps=10))
        assert eng.total_headcount_gap == 5

    def test_total_headcount_gap_zero_when_at_target(self):
        eng = SalesCapacityEngine()
        eng.analyze(make_input(current_reps=10, target_reps=10))
        assert eng.total_headcount_gap == 0

    def test_properties_reset_after_reset(self):
        eng = SalesCapacityEngine()
        eng.analyze(make_input(current_reps=3, target_reps=10,
                               ramping_reps=0, avg_attainment_pct=100.0))
        eng.reset()
        assert eng.constrained_teams == []
        assert eng.immediate_hire_teams == []
        assert eng.critical_teams == []
        assert eng.total_quota_at_risk == 0.0
        assert eng.total_headcount_gap == 0

    def test_total_quota_at_risk_rounded_to_2_decimals(self):
        eng = SalesCapacityEngine()
        eng.analyze(make_input(total_team_quota=333_333.33,
                               current_reps=7, target_reps=10,
                               ramping_reps=0, avg_attainment_pct=100.0))
        # Should be a float rounded to 2 decimals
        result = eng.total_quota_at_risk
        assert result == round(result, 2)


# ===========================================================================
# 20.  summary() TESTS — exactly 13 keys
# ===========================================================================

class TestSummary:
    EXPECTED_KEYS = {
        "total", "status_counts", "urgency_counts", "health_counts",
        "action_counts", "avg_effective_capacity", "avg_required_attainment",
        "total_quota_at_risk", "constrained_count", "immediate_hire_count",
        "critical_count", "avg_productivity_index", "total_headcount_gap",
    }

    def test_summary_empty_has_exactly_13_keys(self):
        eng = SalesCapacityEngine()
        s = eng.summary()
        assert len(s) == 13

    def test_summary_nonempty_has_exactly_13_keys(self):
        eng = engine_with(make_input())
        s = eng.summary()
        assert len(s) == 13

    def test_summary_exact_key_set_empty(self):
        eng = SalesCapacityEngine()
        assert set(eng.summary().keys()) == self.EXPECTED_KEYS

    def test_summary_exact_key_set_nonempty(self):
        eng = engine_with(make_input())
        assert set(eng.summary().keys()) == self.EXPECTED_KEYS

    def test_summary_empty_total_is_zero(self):
        eng = SalesCapacityEngine()
        assert eng.summary()["total"] == 0

    def test_summary_empty_counts_are_empty_dicts(self):
        eng = SalesCapacityEngine()
        s = eng.summary()
        assert s["status_counts"] == {}
        assert s["urgency_counts"] == {}
        assert s["health_counts"] == {}
        assert s["action_counts"] == {}

    def test_summary_empty_numeric_fields_are_zero(self):
        eng = SalesCapacityEngine()
        s = eng.summary()
        assert s["avg_effective_capacity"] == 0.0
        assert s["avg_required_attainment"] == 0.0
        assert s["total_quota_at_risk"] == 0.0
        assert s["constrained_count"] == 0
        assert s["immediate_hire_count"] == 0
        assert s["critical_count"] == 0
        assert s["avg_productivity_index"] == 0.0
        assert s["total_headcount_gap"] == 0

    def test_summary_total_count(self):
        eng = SalesCapacityEngine()
        eng.analyze_batch([make_input(team_id="a"), make_input(team_id="b"),
                           make_input(team_id="c")])
        assert eng.summary()["total"] == 3

    def test_summary_status_counts_accurate(self):
        eng = SalesCapacityEngine()
        # OVER_CAPACITY team
        eng.analyze(make_input(team_id="t1", current_reps=10, target_reps=10,
                               ramping_reps=0, avg_attainment_pct=100.0))
        # CRITICAL_SHORTAGE team
        eng.analyze(make_input(team_id="t2", current_reps=3, target_reps=10,
                               ramping_reps=0, avg_attainment_pct=100.0))
        s = eng.summary()
        assert s["status_counts"].get("over_capacity", 0) == 1
        assert s["status_counts"].get("critical_shortage", 0) == 1

    def test_summary_constrained_count(self):
        eng = SalesCapacityEngine()
        eng.analyze(make_input(current_reps=3, target_reps=10,
                               ramping_reps=0, avg_attainment_pct=100.0))
        eng.analyze(make_input(current_reps=10, target_reps=10,
                               ramping_reps=0, avg_attainment_pct=100.0))
        assert eng.summary()["constrained_count"] == 1

    def test_summary_immediate_hire_count(self):
        eng = SalesCapacityEngine()
        eng.analyze(make_input(current_reps=3, target_reps=10,
                               ramping_reps=0, avg_attainment_pct=100.0))
        assert eng.summary()["immediate_hire_count"] == 1

    def test_summary_critical_count(self):
        eng = SalesCapacityEngine()
        eng.analyze(make_input(current_reps=2, target_reps=10,
                               ramping_reps=0, avg_attainment_pct=100.0))
        assert eng.summary()["critical_count"] >= 1

    def test_summary_avg_effective_capacity(self):
        eng = SalesCapacityEngine()
        r1 = eng.analyze(make_input(team_id="t1", current_reps=10, target_reps=10,
                                    ramping_reps=0, avg_attainment_pct=100.0))
        r2 = eng.analyze(make_input(team_id="t2", current_reps=8, target_reps=10,
                                    ramping_reps=0, avg_attainment_pct=100.0))
        expected = round((r1.effective_capacity_pct + r2.effective_capacity_pct) / 2, 1)
        assert eng.summary()["avg_effective_capacity"] == expected

    def test_summary_avg_productivity_index(self):
        eng = SalesCapacityEngine()
        r1 = eng.analyze(make_input(team_id="t1", productivity_score=80.0,
                                    ramping_reps=0, voluntary_attrition_risk=0))
        r2 = eng.analyze(make_input(team_id="t2", productivity_score=60.0,
                                    ramping_reps=0, voluntary_attrition_risk=0))
        expected = round((r1.productivity_index + r2.productivity_index) / 2, 1)
        assert eng.summary()["avg_productivity_index"] == expected

    def test_summary_total_headcount_gap(self):
        eng = SalesCapacityEngine()
        eng.analyze(make_input(team_id="t1", current_reps=8, target_reps=10))
        eng.analyze(make_input(team_id="t2", current_reps=7, target_reps=10))
        assert eng.summary()["total_headcount_gap"] == 5

    def test_summary_total_quota_at_risk(self):
        eng = SalesCapacityEngine()
        r = eng.analyze(make_input(current_reps=5, target_reps=10,
                                   ramping_reps=0, avg_attainment_pct=100.0,
                                   total_team_quota=1_000_000.0))
        assert eng.summary()["total_quota_at_risk"] == round(r.quota_at_risk, 2)

    def test_summary_urgency_counts_keys_are_strings(self):
        eng = engine_with(make_input())
        for k in eng.summary()["urgency_counts"]:
            assert isinstance(k, str)

    def test_summary_action_counts_keys_are_strings(self):
        eng = engine_with(make_input())
        for k in eng.summary()["action_counts"]:
            assert isinstance(k, str)


# ===========================================================================
# 21.  END-TO-END SCENARIO TESTS
# ===========================================================================

class TestEndToEndScenarios:
    """Integration tests exercising full analyze() paths."""

    def test_scenario_perfect_team(self):
        """Full team, fully productive, no risk."""
        eng = SalesCapacityEngine()
        inp = make_input(
            current_reps=10, target_reps=10, ramping_reps=0,
            avg_attainment_pct=100.0, attrition_qtd=0,
            voluntary_attrition_risk=0, productivity_score=90.0,
            total_team_quota=1_000_000.0, quota_per_rep=100_000.0,
            pipeline_coverage_ratio=3.0,
        )
        result = eng.analyze(inp)
        assert result.capacity_status == CapacityStatus.OVER_CAPACITY
        assert result.capacity_health == CapacityHealth.HEALTHY
        assert result.needs_immediate_hire is False
        assert result.is_capacity_constrained is False
        assert result.headcount_gap == 0
        assert result.quota_at_risk == 0.0

    def test_scenario_critical_team(self):
        """Severely understaffed team needing immediate hires."""
        eng = SalesCapacityEngine()
        inp = make_input(
            current_reps=3, target_reps=10, ramping_reps=0,
            avg_attainment_pct=100.0, total_team_quota=1_000_000.0,
            quota_per_rep=100_000.0,
        )
        result = eng.analyze(inp)
        assert result.capacity_status == CapacityStatus.CRITICAL_SHORTAGE
        assert result.hiring_urgency == HiringUrgency.IMMEDIATE
        assert result.capacity_action == CapacityAction.HIRE_IMMEDIATELY
        assert result.needs_immediate_hire is True
        assert result.is_capacity_constrained is True
        assert result.headcount_gap == 7

    def test_scenario_heavy_ramp_period(self):
        """Team overstaffed on headcount but most reps still ramping."""
        eng = SalesCapacityEngine()
        # current=15, target=10, ramping=8, attainment=100%
        # eff_cap = (15 - 8*0.6)/10 * 100 = 102 → OVER_CAPACITY (not CRITICAL)
        # ramp_impact = 8/15 * 100 ≈ 53.3% > 50 → ACCELERATE_RAMP
        inp = make_input(
            current_reps=15, target_reps=10, ramping_reps=8,
            avg_attainment_pct=100.0,
        )
        result = eng.analyze(inp)
        assert result.ramp_impact > 50.0
        assert result.capacity_status != CapacityStatus.CRITICAL_SHORTAGE
        assert result.capacity_action == CapacityAction.ACCELERATE_RAMP

    def test_scenario_at_capacity_low_productivity(self):
        """AT_CAPACITY team with low productivity."""
        eng = SalesCapacityEngine()
        inp = make_input(
            current_reps=9, target_reps=10, ramping_reps=0,
            avg_attainment_pct=100.0, productivity_score=60.0,
            voluntary_attrition_risk=0, attrition_qtd=0,
            pipeline_coverage_ratio=3.0,
        )
        result = eng.analyze(inp)
        assert result.capacity_status == CapacityStatus.AT_CAPACITY
        assert result.capacity_action == CapacityAction.FOCUS_PRODUCTIVITY

    def test_scenario_near_term_gap_low_pipeline(self):
        """Gap of 3+ with thin pipeline → redistribute."""
        eng = SalesCapacityEngine()
        inp = make_input(
            current_reps=7, target_reps=10, ramping_reps=0,
            avg_attainment_pct=90.0,  # eff_cap = 63 → UNDER_CAPACITY, not critical
            pipeline_coverage_ratio=1.5,
        )
        result = eng.analyze(inp)
        # eff_cap = 7/10 * 90 = 63 → UNDER_CAPACITY → NOT critical → gap=3 → NEAR_TERM
        # ramp=0, pipeline<2 → REDISTRIBUTE_QUOTA
        assert result.hiring_urgency == HiringUrgency.NEAR_TERM
        assert result.capacity_action == CapacityAction.REDISTRIBUTE_QUOTA

    def test_scenario_at_risk_due_to_attrition(self):
        """AT_CAPACITY team with historical attrition."""
        eng = SalesCapacityEngine()
        inp = make_input(
            current_reps=9, target_reps=10, ramping_reps=0,
            avg_attainment_pct=100.0, attrition_qtd=1,
            voluntary_attrition_risk=0, productivity_score=80.0,
            total_team_quota=900_000.0, quota_per_rep=100_000.0,
        )
        result = eng.analyze(inp)
        assert result.capacity_health == CapacityHealth.AT_RISK

    def test_scenario_high_req_attainment_critical(self):
        """Required attainment > 130 triggers CRITICAL health."""
        eng = SalesCapacityEngine()
        inp = make_input(
            current_reps=6, target_reps=10, ramping_reps=0,
            avg_attainment_pct=100.0,
            total_team_quota=900_000.0, quota_per_rep=100_000.0,
            attrition_qtd=0, voluntary_attrition_risk=0,
        )
        result = eng.analyze(inp)
        # req = 900k / (6 * 100k) * 100 = 150 > 130 → CRITICAL health
        assert result.required_attainment > 130.0
        assert result.capacity_health == CapacityHealth.CRITICAL

    def test_scenario_maintain_over_capacity(self):
        """Over-capacity team should maintain."""
        eng = SalesCapacityEngine()
        inp = make_input(
            current_reps=12, target_reps=10, ramping_reps=0,
            avg_attainment_pct=100.0, productivity_score=85.0,
            voluntary_attrition_risk=0, attrition_qtd=0,
            pipeline_coverage_ratio=3.0,
        )
        result = eng.analyze(inp)
        assert result.capacity_status == CapacityStatus.OVER_CAPACITY
        assert result.capacity_action == CapacityAction.MAINTAIN_CAPACITY

    def test_scenario_strategic_review(self):
        """UNDER_CAPACITY, low gap, high pipeline → strategic review."""
        eng = SalesCapacityEngine()
        inp = make_input(
            current_reps=7, target_reps=7,   # gap=0
            ramping_reps=0, avg_attainment_pct=75.0,  # eff=75 → UNDER_CAPACITY
            pipeline_coverage_ratio=4.0,
        )
        result = eng.analyze(inp)
        assert result.capacity_status == CapacityStatus.UNDER_CAPACITY
        assert result.capacity_action == CapacityAction.STRATEGIC_REVIEW

    def test_to_dict_full_round_trip(self):
        eng = SalesCapacityEngine()
        inp = make_input(team_id="rt", region="NA")
        result = eng.analyze(inp)
        d = result.to_dict()
        assert d["team_id"] == "rt"
        assert d["region"] == "NA"
        assert d["capacity_status"] == result.capacity_status.value
        assert d["hiring_urgency"] == result.hiring_urgency.value
        assert d["capacity_health"] == result.capacity_health.value
        assert d["capacity_action"] == result.capacity_action.value
        assert d["effective_capacity_pct"] == result.effective_capacity_pct
        assert d["headcount_gap"] == result.headcount_gap
        assert d["quota_at_risk"] == result.quota_at_risk
        assert d["pipeline_per_rep"] == result.pipeline_per_rep
        assert d["required_attainment"] == result.required_attainment
        assert d["ramp_impact"] == result.ramp_impact
        assert d["productivity_index"] == result.productivity_index
        assert d["is_capacity_constrained"] == result.is_capacity_constrained
        assert d["needs_immediate_hire"] == result.needs_immediate_hire

    def test_multi_team_batch_summary(self):
        eng = SalesCapacityEngine()
        inputs = [
            make_input(team_id="t1", current_reps=10, target_reps=10,
                       ramping_reps=0, avg_attainment_pct=100.0,
                       attrition_qtd=0, voluntary_attrition_risk=0),
            make_input(team_id="t2", current_reps=3, target_reps=10,
                       ramping_reps=0, avg_attainment_pct=100.0),
            make_input(team_id="t3", current_reps=8, target_reps=10,
                       ramping_reps=0, avg_attainment_pct=100.0,
                       attrition_qtd=1, voluntary_attrition_risk=0),
        ]
        eng.analyze_batch(inputs)
        s = eng.summary()
        assert s["total"] == 3
        assert len(s) == 13
        assert s["constrained_count"] >= 1
        assert s["immediate_hire_count"] >= 1


# ===========================================================================
# 22.  BOUNDARY / EDGE CASE TESTS
# ===========================================================================

class TestBoundaryAndEdgeCases:
    def test_exactly_80_capacity_at_capacity_not_under(self):
        eng = SalesCapacityEngine()
        # 8 reps, 10 target, 100% attainment → 80% → AT_CAPACITY
        result = eng.analyze(make_input(current_reps=8, target_reps=10,
                                        ramping_reps=0, avg_attainment_pct=100.0))
        assert result.capacity_status == CapacityStatus.AT_CAPACITY

    def test_exactly_60_capacity_under_not_critical(self):
        eng = SalesCapacityEngine()
        # 6 reps, 10 target, 100% attainment → 60% → UNDER_CAPACITY
        result = eng.analyze(make_input(current_reps=6, target_reps=10,
                                        ramping_reps=0, avg_attainment_pct=100.0))
        assert result.capacity_status == CapacityStatus.UNDER_CAPACITY

    def test_just_below_60_is_critical(self):
        eng = SalesCapacityEngine()
        # eff_cap = 5.9 reps worth → need to craft: 59/100*100 = 59
        result = eng.analyze(make_input(current_reps=6, target_reps=10,
                                        ramping_reps=0, avg_attainment_pct=98.33))
        # 6/10 * 98.33 = 59.0 → CRITICAL_SHORTAGE
        assert result.capacity_status == CapacityStatus.CRITICAL_SHORTAGE

    def test_headcount_gap_never_negative(self):
        eng = SalesCapacityEngine()
        result = eng.analyze(make_input(current_reps=15, target_reps=10))
        assert result.headcount_gap >= 0

    def test_quota_at_risk_never_negative(self):
        eng = SalesCapacityEngine()
        result = eng.analyze(make_input(current_reps=10, target_reps=10,
                                        ramping_reps=0, avg_attainment_pct=150.0))
        assert result.quota_at_risk >= 0.0

    def test_ramp_impact_never_above_100(self):
        eng = SalesCapacityEngine()
        result = eng.analyze(make_input(current_reps=2, target_reps=10, ramping_reps=10))
        assert result.ramp_impact <= 100.0

    def test_productivity_index_in_range(self):
        eng = SalesCapacityEngine()
        result = eng.analyze(make_input(productivity_score=0.0, ramping_reps=10,
                                        current_reps=10, voluntary_attrition_risk=10))
        assert 0.0 <= result.productivity_index <= 100.0

    def test_effective_capacity_in_range(self):
        eng = SalesCapacityEngine()
        result = eng.analyze(make_input(current_reps=1000, target_reps=1,
                                        avg_attainment_pct=200.0))
        assert 0.0 <= result.effective_capacity_pct <= 150.0

    def test_required_attainment_never_above_200(self):
        eng = SalesCapacityEngine()
        result = eng.analyze(make_input(total_team_quota=99_999_999.0,
                                        current_reps=1, quota_per_rep=1.0))
        assert result.required_attainment <= 200.0

    def test_zero_pipeline_coverage_ratio(self):
        eng = SalesCapacityEngine()
        result = eng.analyze(make_input(pipeline_coverage_ratio=0.0))
        assert result.pipeline_per_rep == 0.0

    def test_large_team(self):
        eng = SalesCapacityEngine()
        result = eng.analyze(make_input(current_reps=1000, target_reps=1000,
                                        ramping_reps=0, avg_attainment_pct=100.0))
        assert result.capacity_status == CapacityStatus.OVER_CAPACITY

    def test_single_rep_team(self):
        eng = SalesCapacityEngine()
        result = eng.analyze(make_input(current_reps=1, target_reps=1,
                                        ramping_reps=0, avg_attainment_pct=100.0))
        assert result.capacity_status == CapacityStatus.OVER_CAPACITY

    def test_zero_total_quota_zero_risk(self):
        eng = SalesCapacityEngine()
        result = eng.analyze(make_input(total_team_quota=0.0, current_reps=5,
                                        target_reps=10))
        assert result.quota_at_risk == 0.0

    def test_high_win_rate_does_not_affect_engine_calc(self):
        """historical_win_rate is stored but not used in scoring; ensure no crash."""
        eng = SalesCapacityEngine()
        result = eng.analyze(make_input(historical_win_rate=0.99))
        assert result is not None

    def test_very_long_team_id(self):
        eng = SalesCapacityEngine()
        long_id = "x" * 500
        result = eng.analyze(make_input(team_id=long_id))
        assert result.team_id == long_id

    def test_multiple_resets_and_reuse(self):
        eng = SalesCapacityEngine()
        for _ in range(5):
            eng.analyze(make_input())
            eng.reset()
        assert len(eng._results) == 0

    def test_effective_capacity_not_negative_when_all_ramp(self):
        eng = SalesCapacityEngine()
        result = eng.analyze(make_input(current_reps=5, target_reps=10,
                                        ramping_reps=5, avg_attainment_pct=100.0))
        assert result.effective_capacity_pct >= 0.0

    def test_required_attainment_zero_quota(self):
        eng = SalesCapacityEngine()
        result = eng.analyze(make_input(total_team_quota=0.0, current_reps=10,
                                        quota_per_rep=100_000.0))
        assert result.required_attainment == 0.0

    def test_summary_single_team(self):
        eng = SalesCapacityEngine()
        eng.analyze(make_input(team_id="solo"))
        s = eng.summary()
        assert s["total"] == 1
        assert len(s) == 13

    def test_analyze_preserves_all_scalar_results(self):
        eng = SalesCapacityEngine()
        result = eng.analyze(make_input())
        assert isinstance(result.effective_capacity_pct, float)
        assert isinstance(result.headcount_gap, int)
        assert isinstance(result.quota_at_risk, float)
        assert isinstance(result.pipeline_per_rep, float)
        assert isinstance(result.required_attainment, float)
        assert isinstance(result.ramp_impact, float)
        assert isinstance(result.productivity_index, float)

    def test_capacity_status_enum_membership(self):
        eng = SalesCapacityEngine()
        result = eng.analyze(make_input())
        assert result.capacity_status in CapacityStatus

    def test_hiring_urgency_enum_membership(self):
        eng = SalesCapacityEngine()
        result = eng.analyze(make_input())
        assert result.hiring_urgency in HiringUrgency

    def test_capacity_health_enum_membership(self):
        eng = SalesCapacityEngine()
        result = eng.analyze(make_input())
        assert result.capacity_health in CapacityHealth

    def test_capacity_action_enum_membership(self):
        eng = SalesCapacityEngine()
        result = eng.analyze(make_input())
        assert result.capacity_action in CapacityAction


# ===========================================================================
# 23.  ADDITIONAL COVERAGE TESTS (cross-check, precision, and misc)
# ===========================================================================

class TestAdditionalCoverage:
    """Extra tests to cross-verify scoring math and cover remaining paths."""

    # --- effective_capacity_pct cross-checks ---
    def test_eff_cap_with_3_ramps_out_of_10(self):
        # (10 - 3*0.6)/10 * 100 = 8.2/10 * 100 = 82.0
        result = SalesCapacityEngine()._effective_capacity_pct(
            make_input(current_reps=10, target_reps=10, ramping_reps=3,
                       avg_attainment_pct=100.0))
        assert result == pytest.approx(82.0, abs=0.11)

    def test_eff_cap_with_fractional_attainment(self):
        # (10-0)/10 * 77.5 = 77.5
        result = SalesCapacityEngine()._effective_capacity_pct(
            make_input(current_reps=10, target_reps=10, ramping_reps=0,
                       avg_attainment_pct=77.5))
        assert result == pytest.approx(77.5, abs=0.11)

    def test_eff_cap_target_reps_1(self):
        # 5 reps, 1 target, 100% → 500 → clamped to 150
        result = SalesCapacityEngine()._effective_capacity_pct(
            make_input(current_reps=5, target_reps=1, ramping_reps=0,
                       avg_attainment_pct=100.0))
        assert result == 150.0

    # --- headcount_gap cross-checks ---
    def test_hc_gap_exactly_zero_when_equal(self):
        assert SalesCapacityEngine()._headcount_gap(
            make_input(current_reps=5, target_reps=5)) == 0

    def test_hc_gap_large_deficit(self):
        assert SalesCapacityEngine()._headcount_gap(
            make_input(current_reps=0, target_reps=20)) == 20

    # --- quota_at_risk cross-checks ---
    def test_quota_at_risk_90pct_capacity(self):
        # shortfall = max(0, 1 - 90/100) = 0.1 → 100k risk from 1M
        result = SalesCapacityEngine()._quota_at_risk(
            make_input(total_team_quota=1_000_000.0), 90.0)
        assert result == pytest.approx(100_000.0, abs=0.01)

    def test_quota_at_risk_60pct_capacity(self):
        result = SalesCapacityEngine()._quota_at_risk(
            make_input(total_team_quota=1_000_000.0), 60.0)
        assert result == pytest.approx(400_000.0, abs=0.01)

    # --- pipeline_per_rep cross-checks ---
    def test_pipeline_per_rep_high_ratio(self):
        # 1M quota, 5x ratio, 10 reps → 500k
        result = SalesCapacityEngine()._pipeline_per_rep(
            make_input(total_team_quota=1_000_000.0, pipeline_coverage_ratio=5.0,
                       current_reps=10))
        assert result == pytest.approx(500_000.0, abs=0.01)

    def test_pipeline_per_rep_single_rep_protection(self):
        # current=0 → uses max(1,0)=1
        result = SalesCapacityEngine()._pipeline_per_rep(
            make_input(total_team_quota=500_000.0, pipeline_coverage_ratio=3.0,
                       current_reps=0))
        assert result == pytest.approx(1_500_000.0, abs=0.01)

    # --- required_attainment cross-checks ---
    def test_required_attainment_over_target(self):
        # 12 reps vs 10 quota worth → needed = 1M/(12*100k)*100 = 83.3
        result = SalesCapacityEngine()._required_attainment(
            make_input(total_team_quota=1_000_000.0, current_reps=12,
                       quota_per_rep=100_000.0))
        assert result == pytest.approx(83.3, abs=0.11)

    def test_required_attainment_exactly_200_clamp(self):
        # ensure clamp works at exactly 200
        result = SalesCapacityEngine()._required_attainment(
            make_input(total_team_quota=200_000.0, current_reps=1,
                       quota_per_rep=100_000.0))
        assert result == 200.0

    # --- ramp_impact cross-checks ---
    def test_ramp_impact_3_of_10(self):
        result = SalesCapacityEngine()._ramp_impact(
            make_input(current_reps=10, ramping_reps=3))
        assert result == pytest.approx(30.0, abs=0.11)

    def test_ramp_impact_100pct_with_equal_reps(self):
        result = SalesCapacityEngine()._ramp_impact(
            make_input(current_reps=5, ramping_reps=5))
        assert result == 100.0

    # --- productivity_index cross-checks ---
    def test_productivity_index_max_ramp_penalty(self):
        # ramp_impact = 100, penalty = 0.5 → 80 * 0.5 = 40
        eng = SalesCapacityEngine()
        inp = make_input(productivity_score=80.0, current_reps=10, ramping_reps=10,
                         voluntary_attrition_risk=0)
        ri = eng._ramp_impact(inp)  # 100
        result = eng._productivity_index(inp, ri)
        assert result == pytest.approx(40.0, abs=0.11)

    def test_productivity_index_attrition_risk_5_of_10(self):
        # ramp=0, attrition=5/10 → penalty = 5
        eng = SalesCapacityEngine()
        inp = make_input(productivity_score=80.0, current_reps=10, ramping_reps=0,
                         voluntary_attrition_risk=5)
        ri = eng._ramp_impact(inp)
        result = eng._productivity_index(inp, ri)
        assert result == pytest.approx(75.0, abs=0.11)

    # --- capacity_status boundary combos ---
    def test_capacity_status_99_at_capacity(self):
        eng = SalesCapacityEngine()
        assert eng._capacity_status(99.0) == CapacityStatus.AT_CAPACITY

    def test_capacity_status_61_under_capacity(self):
        eng = SalesCapacityEngine()
        assert eng._capacity_status(61.0) == CapacityStatus.UNDER_CAPACITY

    def test_capacity_status_0_1_critical(self):
        eng = SalesCapacityEngine()
        assert eng._capacity_status(0.1) == CapacityStatus.CRITICAL_SHORTAGE

    # --- hiring_urgency combos ---
    def test_hiring_urgency_under_capacity_gap_2_planned(self):
        eng = SalesCapacityEngine()
        result = eng._hiring_urgency(CapacityStatus.UNDER_CAPACITY, 2)
        assert result == HiringUrgency.PLANNED

    def test_hiring_urgency_over_capacity_gap_3_near_term(self):
        eng = SalesCapacityEngine()
        result = eng._hiring_urgency(CapacityStatus.OVER_CAPACITY, 3)
        assert result == HiringUrgency.NEAR_TERM

    # --- capacity_health full matrix ---
    def test_capacity_health_req_131_at_capacity(self):
        eng = SalesCapacityEngine()
        inp = make_input(attrition_qtd=0, voluntary_attrition_risk=0)
        result = eng._capacity_health(inp, CapacityStatus.AT_CAPACITY, 131.0)
        assert result == CapacityHealth.CRITICAL

    def test_capacity_health_critical_shortage_low_req(self):
        # Even with req=50, CRITICAL_SHORTAGE triggers CRITICAL
        eng = SalesCapacityEngine()
        inp = make_input(attrition_qtd=0, voluntary_attrition_risk=0)
        result = eng._capacity_health(inp, CapacityStatus.CRITICAL_SHORTAGE, 50.0)
        assert result == CapacityHealth.CRITICAL

    def test_capacity_health_under_capacity_req_90_constrained(self):
        eng = SalesCapacityEngine()
        inp = make_input(attrition_qtd=0, voluntary_attrition_risk=0)
        result = eng._capacity_health(inp, CapacityStatus.UNDER_CAPACITY, 90.0)
        assert result == CapacityHealth.CONSTRAINED

    def test_capacity_health_both_attrition_signals_at_risk(self):
        eng = SalesCapacityEngine()
        inp = make_input(attrition_qtd=2, voluntary_attrition_risk=3)
        result = eng._capacity_health(inp, CapacityStatus.AT_CAPACITY, 90.0)
        assert result == CapacityHealth.AT_RISK

    def test_capacity_health_zero_attrition_zero_risk_healthy(self):
        eng = SalesCapacityEngine()
        inp = make_input(attrition_qtd=0, voluntary_attrition_risk=0)
        result = eng._capacity_health(inp, CapacityStatus.OVER_CAPACITY, 70.0)
        assert result == CapacityHealth.HEALTHY

    # --- capacity_action combos ---
    def test_capacity_action_over_capacity_no_ramp_maintain(self):
        eng = SalesCapacityEngine()
        inp = make_input(pipeline_coverage_ratio=3.0)
        result = eng._capacity_action(inp, CapacityStatus.OVER_CAPACITY,
                                       HiringUrgency.MONITOR, 0.0, 80.0)
        assert result == CapacityAction.MAINTAIN_CAPACITY

    def test_capacity_action_under_capacity_no_ramp_no_near_term_review(self):
        eng = SalesCapacityEngine()
        inp = make_input(pipeline_coverage_ratio=3.0)
        result = eng._capacity_action(inp, CapacityStatus.UNDER_CAPACITY,
                                       HiringUrgency.PLANNED, 0.0, 80.0)
        assert result == CapacityAction.STRATEGIC_REVIEW

    def test_capacity_action_at_capacity_productivity_exactly_70_maintain(self):
        # prod_idx exactly 70 → NOT focus_productivity → check next: AT_CAPACITY → MAINTAIN
        eng = SalesCapacityEngine()
        inp = make_input(pipeline_coverage_ratio=3.0)
        result = eng._capacity_action(inp, CapacityStatus.AT_CAPACITY,
                                       HiringUrgency.MONITOR, 0.0, 70.0)
        assert result == CapacityAction.MAINTAIN_CAPACITY

    def test_capacity_action_ramp_50_1_percent_accelerate(self):
        eng = SalesCapacityEngine()
        inp = make_input(pipeline_coverage_ratio=3.0)
        result = eng._capacity_action(inp, CapacityStatus.AT_CAPACITY,
                                       HiringUrgency.MONITOR, 50.1, 80.0)
        assert result == CapacityAction.ACCELERATE_RAMP

    # --- full analyze consistency checks ---
    def test_analyze_is_constrained_matches_status(self):
        """is_capacity_constrained is derived purely from status."""
        eng = SalesCapacityEngine()
        for current, expected_constrained in [
            (10, False),   # OVER_CAPACITY
            (9, False),    # AT_CAPACITY
            (7, True),     # UNDER_CAPACITY (70%)
            (3, True),     # CRITICAL_SHORTAGE (30%)
        ]:
            result = eng.analyze(make_input(current_reps=current, target_reps=10,
                                             ramping_reps=0, avg_attainment_pct=100.0))
            assert result.is_capacity_constrained == expected_constrained, \
                f"current={current} expected constrained={expected_constrained}"
        eng.reset()

    def test_analyze_needs_immediate_hire_only_when_immediate(self):
        """needs_immediate_hire is True only when urgency is IMMEDIATE."""
        eng = SalesCapacityEngine()
        # CRITICAL_SHORTAGE → IMMEDIATE
        r = eng.analyze(make_input(current_reps=3, target_reps=10,
                                   ramping_reps=0, avg_attainment_pct=100.0))
        assert r.needs_immediate_hire == (r.hiring_urgency == HiringUrgency.IMMEDIATE)
        eng.reset()

    # --- summary edge cases ---
    def test_summary_after_reset_matches_empty(self):
        eng = SalesCapacityEngine()
        eng.analyze_batch([make_input(team_id=f"t{i}") for i in range(5)])
        eng.reset()
        s = eng.summary()
        assert s["total"] == 0
        assert s["constrained_count"] == 0

    def test_summary_counts_sum_to_total(self):
        eng = SalesCapacityEngine()
        inputs = [make_input(team_id=f"t{i}", current_reps=(3+i), target_reps=10,
                             ramping_reps=0, avg_attainment_pct=100.0)
                  for i in range(5)]
        eng.analyze_batch(inputs)
        s = eng.summary()
        assert sum(s["status_counts"].values()) == s["total"]
        assert sum(s["urgency_counts"].values()) == s["total"]
        assert sum(s["health_counts"].values()) == s["total"]
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_avg_required_attainment(self):
        eng = SalesCapacityEngine()
        r1 = eng.analyze(make_input(team_id="t1", total_team_quota=1_000_000.0,
                                    current_reps=10, quota_per_rep=100_000.0))
        r2 = eng.analyze(make_input(team_id="t2", total_team_quota=800_000.0,
                                    current_reps=10, quota_per_rep=100_000.0))
        expected = round((r1.required_attainment + r2.required_attainment) / 2, 1)
        assert eng.summary()["avg_required_attainment"] == expected

    def test_engine_initial_state(self):
        eng = SalesCapacityEngine()
        assert eng._results == []

    def test_batch_returns_same_as_sequential(self):
        eng1 = SalesCapacityEngine()
        eng2 = SalesCapacityEngine()
        inputs = [make_input(team_id=f"t{i}") for i in range(3)]
        batch = eng1.analyze_batch(inputs)
        sequential = [eng2.analyze(inp) for inp in inputs]
        for b, s in zip(batch, sequential):
            assert b.to_dict() == s.to_dict()

    def test_total_quota_at_risk_multiple_teams(self):
        eng = SalesCapacityEngine()
        r1 = eng.analyze(make_input(team_id="a", current_reps=5, target_reps=10,
                                    ramping_reps=0, avg_attainment_pct=100.0,
                                    total_team_quota=1_000_000.0))
        r2 = eng.analyze(make_input(team_id="b", current_reps=5, target_reps=10,
                                    ramping_reps=0, avg_attainment_pct=100.0,
                                    total_team_quota=2_000_000.0))
        assert eng.total_quota_at_risk == round(r1.quota_at_risk + r2.quota_at_risk, 2)

    def test_constrained_count_matches_constrained_teams_len(self):
        eng = SalesCapacityEngine()
        eng.analyze_batch([make_input(team_id=f"t{i}", current_reps=(3+i),
                                      target_reps=10, ramping_reps=0,
                                      avg_attainment_pct=100.0) for i in range(6)])
        s = eng.summary()
        assert s["constrained_count"] == len(eng.constrained_teams)

    def test_immediate_hire_count_matches_immediate_hire_teams_len(self):
        eng = SalesCapacityEngine()
        eng.analyze_batch([make_input(team_id=f"t{i}", current_reps=(3+i),
                                      target_reps=10, ramping_reps=0,
                                      avg_attainment_pct=100.0) for i in range(6)])
        s = eng.summary()
        assert s["immediate_hire_count"] == len(eng.immediate_hire_teams)

    def test_critical_count_matches_critical_teams_len(self):
        eng = SalesCapacityEngine()
        eng.analyze_batch([make_input(team_id=f"t{i}", current_reps=(2+i),
                                      target_reps=10, ramping_reps=0,
                                      avg_attainment_pct=100.0) for i in range(6)])
        s = eng.summary()
        assert s["critical_count"] == len(eng.critical_teams)

    def test_total_headcount_gap_matches_property(self):
        eng = SalesCapacityEngine()
        eng.analyze_batch([make_input(team_id=f"t{i}", current_reps=(5+i),
                                      target_reps=10) for i in range(4)])
        assert eng.summary()["total_headcount_gap"] == eng.total_headcount_gap

    def test_capacity_status_exactly_100_is_over(self):
        # eff_cap of exactly 100 → OVER_CAPACITY
        eng = SalesCapacityEngine()
        r = eng.analyze(make_input(current_reps=10, target_reps=10,
                                   ramping_reps=0, avg_attainment_pct=100.0))
        assert r.capacity_status == CapacityStatus.OVER_CAPACITY

    def test_under_capacity_results_in_constrained_health(self):
        eng = SalesCapacityEngine()
        r = eng.analyze(make_input(current_reps=7, target_reps=10,
                                   ramping_reps=0, avg_attainment_pct=100.0,
                                   attrition_qtd=0, voluntary_attrition_risk=0,
                                   total_team_quota=700_000.0, quota_per_rep=100_000.0))
        # req = 700k/(7*100k)*100 = 100, status=UNDER → health=CONSTRAINED
        assert r.capacity_health == CapacityHealth.CONSTRAINED

    def test_new_hires_qtd_field_stored(self):
        inp = make_input(new_hires_qtd=3)
        assert inp.new_hires_qtd == 3

    def test_avg_ramp_months_field_stored(self):
        inp = make_input(avg_ramp_months=6)
        assert inp.avg_ramp_months == 6

    def test_days_remaining_period_field_stored(self):
        inp = make_input(days_remaining_period=30)
        assert inp.days_remaining_period == 30

    def test_target_growth_pct_field_stored(self):
        inp = make_input(target_growth_pct=25.0)
        assert inp.target_growth_pct == 25.0

    def test_open_headcount_field_stored(self):
        inp = make_input(open_headcount=2)
        assert inp.open_headcount == 2

    def test_avg_sales_cycle_days_field_stored(self):
        inp = make_input(avg_sales_cycle_days=90)
        assert inp.avg_sales_cycle_days == 90

    def test_avg_deal_size_field_stored(self):
        inp = make_input(avg_deal_size=50_000.0)
        assert inp.avg_deal_size == 50_000.0

    def test_segment_field_stored(self):
        inp = make_input(segment="enterprise")
        assert inp.segment == "enterprise"

    def test_manager_id_field_stored(self):
        inp = make_input(manager_id="mgr-99")
        assert inp.manager_id == "mgr-99"

    def test_result_to_dict_capacity_status_value(self):
        eng = SalesCapacityEngine()
        r = eng.analyze(make_input(current_reps=3, target_reps=10,
                                   ramping_reps=0, avg_attainment_pct=100.0))
        assert r.to_dict()["capacity_status"] == "critical_shortage"

    def test_result_to_dict_hiring_urgency_value(self):
        eng = SalesCapacityEngine()
        r = eng.analyze(make_input(current_reps=10, target_reps=10,
                                   ramping_reps=0, avg_attainment_pct=100.0))
        assert r.to_dict()["hiring_urgency"] == "monitor"
