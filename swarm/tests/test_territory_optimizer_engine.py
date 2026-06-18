"""
Comprehensive tests for Module 32 — Territory Optimizer Engine.
Run from /home/user/TEST: python -m pytest swarm/tests/test_territory_optimizer_engine.py -v
"""
from __future__ import annotations

import pytest

from swarm.intelligence.territory_optimizer_engine import (
    CoverageGap,
    TerritoryAction,
    TerritoryHealth,
    TerritoryInput,
    TerritoryOptimizerEngine,
    TerritoryResult,
    WorkloadBalance,
    _coverage_gap,
    _coverage_pct,
    _icp_penetration_pct,
    _optimization_score,
    _territory_action,
    _territory_drivers,
    _territory_health,
    _territory_plays,
    _territory_score,
    _whitespace_opportunity,
    _workload_balance,
    _workload_ratio,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(
    rep_id: str = "R1",
    rep_name: str = "Alice",
    region: str = "EMEA",
    segment: str = "Enterprise",
    quota_eur: float = 500_000.0,
    attainment_pct: float = 80.0,
    total_accounts: int = 100,
    icp_accounts: int = 60,
    active_accounts: int = 50,
    dormant_accounts: int = 30,
    whitespace_accounts: int = 10,
    avg_accounts_per_rep_target: int = 100,
    deals_in_pipeline: int = 5,
    avg_deal_size_eur: float = 50_000.0,
    geographic_concentration_pct: float = 40.0,
    travel_days_per_month: int = 5,
    market_penetration_pct: float = 20.0,
    competitor_accounts: int = 10,
    expansion_signals: int = 3,
    outbound_activities_30d: int = 30,
    meetings_held_30d: int = 5,
    proposals_sent_30d: int = 3,
) -> TerritoryInput:
    """Factory with sensible defaults for a healthy territory."""
    return TerritoryInput(
        rep_id=rep_id,
        rep_name=rep_name,
        region=region,
        segment=segment,
        quota_eur=quota_eur,
        attainment_pct=attainment_pct,
        total_accounts=total_accounts,
        icp_accounts=icp_accounts,
        active_accounts=active_accounts,
        dormant_accounts=dormant_accounts,
        whitespace_accounts=whitespace_accounts,
        avg_accounts_per_rep_target=avg_accounts_per_rep_target,
        deals_in_pipeline=deals_in_pipeline,
        avg_deal_size_eur=avg_deal_size_eur,
        geographic_concentration_pct=geographic_concentration_pct,
        travel_days_per_month=travel_days_per_month,
        market_penetration_pct=market_penetration_pct,
        competitor_accounts=competitor_accounts,
        expansion_signals=expansion_signals,
        outbound_activities_30d=outbound_activities_30d,
        meetings_held_30d=meetings_held_30d,
        proposals_sent_30d=proposals_sent_30d,
    )


# ---------------------------------------------------------------------------
# Class 1 — Enum values
# ---------------------------------------------------------------------------

class TestEnumValues:
    def test_territory_health_values(self):
        assert TerritoryHealth.EXCELLENT.value == "excellent"
        assert TerritoryHealth.GOOD.value == "good"
        assert TerritoryHealth.FAIR.value == "fair"
        assert TerritoryHealth.POOR.value == "poor"

    def test_territory_action_values(self):
        assert TerritoryAction.OPTIMIZE.value == "optimize"
        assert TerritoryAction.EXPAND.value == "expand"
        assert TerritoryAction.REBALANCE.value == "rebalance"
        assert TerritoryAction.RESTRUCTURE.value == "restructure"

    def test_coverage_gap_values(self):
        assert CoverageGap.NONE.value == "none"
        assert CoverageGap.MINOR.value == "minor"
        assert CoverageGap.SIGNIFICANT.value == "significant"
        assert CoverageGap.CRITICAL.value == "critical"

    def test_workload_balance_values(self):
        assert WorkloadBalance.BALANCED.value == "balanced"
        assert WorkloadBalance.OVERLOADED.value == "overloaded"
        assert WorkloadBalance.UNDERLOADED.value == "underloaded"
        assert WorkloadBalance.SKEWED.value == "skewed"

    def test_enums_are_str_subclasses(self):
        assert isinstance(TerritoryHealth.EXCELLENT, str)
        assert isinstance(TerritoryAction.OPTIMIZE, str)
        assert isinstance(CoverageGap.NONE, str)
        assert isinstance(WorkloadBalance.BALANCED, str)

    def test_enum_counts(self):
        assert len(TerritoryHealth) == 4
        assert len(TerritoryAction) == 4
        assert len(CoverageGap) == 4
        assert len(WorkloadBalance) == 4


# ---------------------------------------------------------------------------
# Class 2 — TerritoryInput dataclass
# ---------------------------------------------------------------------------

class TestTerritoryInputDataclass:
    def test_all_fields_accessible(self):
        inp = make_input()
        assert inp.rep_id == "R1"
        assert inp.rep_name == "Alice"
        assert inp.region == "EMEA"
        assert inp.segment == "Enterprise"
        assert inp.quota_eur == 500_000.0
        assert inp.attainment_pct == 80.0
        assert inp.total_accounts == 100
        assert inp.icp_accounts == 60
        assert inp.active_accounts == 50
        assert inp.dormant_accounts == 30
        assert inp.whitespace_accounts == 10
        assert inp.avg_accounts_per_rep_target == 100
        assert inp.deals_in_pipeline == 5
        assert inp.avg_deal_size_eur == 50_000.0
        assert inp.geographic_concentration_pct == 40.0
        assert inp.travel_days_per_month == 5
        assert inp.market_penetration_pct == 20.0
        assert inp.competitor_accounts == 10
        assert inp.expansion_signals == 3
        assert inp.outbound_activities_30d == 30
        assert inp.meetings_held_30d == 5
        assert inp.proposals_sent_30d == 3

    def test_field_count(self):
        import dataclasses
        fields = dataclasses.fields(TerritoryInput)
        # The dataclass exposes 22 fields (4 identity + 2 quota/perf + 5 composition
        # + 3 workload + 2 geo + 4 market/activity signals + 2 extra activity)
        assert len(fields) == 22


# ---------------------------------------------------------------------------
# Class 3 — _coverage_pct
# ---------------------------------------------------------------------------

class TestCoveragePct:
    def test_normal(self):
        inp = make_input(active_accounts=50, total_accounts=100)
        assert _coverage_pct(inp) == 50.0

    def test_full_coverage(self):
        inp = make_input(active_accounts=100, total_accounts=100)
        assert _coverage_pct(inp) == 100.0

    def test_zero_active(self):
        inp = make_input(active_accounts=0, total_accounts=100)
        assert _coverage_pct(inp) == 0.0

    def test_zero_total(self):
        inp = make_input(active_accounts=0, total_accounts=0)
        assert _coverage_pct(inp) == 0.0

    def test_negative_total(self):
        inp = make_input(active_accounts=10, total_accounts=-5)
        assert _coverage_pct(inp) == 0.0

    def test_rounding_one_decimal(self):
        inp = make_input(active_accounts=1, total_accounts=3)
        result = _coverage_pct(inp)
        assert result == round(100 / 3, 1)

    def test_returns_float(self):
        inp = make_input(active_accounts=50, total_accounts=100)
        assert isinstance(_coverage_pct(inp), float)

    def test_partial_coverage(self):
        inp = make_input(active_accounts=25, total_accounts=80)
        assert _coverage_pct(inp) == round(25 / 80 * 100, 1)


# ---------------------------------------------------------------------------
# Class 4 — _icp_penetration_pct
# ---------------------------------------------------------------------------

class TestIcpPenetrationPct:
    def test_normal(self):
        inp = make_input(active_accounts=40, icp_accounts=60)
        assert _icp_penetration_pct(inp) == round(40 / 60 * 100, 1)

    def test_active_greater_than_icp_capped(self):
        # min(active, icp) / icp — if active > icp → 100%
        inp = make_input(active_accounts=80, icp_accounts=60)
        assert _icp_penetration_pct(inp) == 100.0

    def test_zero_icp(self):
        inp = make_input(active_accounts=50, icp_accounts=0)
        assert _icp_penetration_pct(inp) == 0.0

    def test_negative_icp(self):
        inp = make_input(active_accounts=50, icp_accounts=-1)
        assert _icp_penetration_pct(inp) == 0.0

    def test_zero_active(self):
        inp = make_input(active_accounts=0, icp_accounts=60)
        assert _icp_penetration_pct(inp) == 0.0

    def test_returns_float(self):
        inp = make_input(active_accounts=30, icp_accounts=60)
        assert isinstance(_icp_penetration_pct(inp), float)

    def test_full_penetration(self):
        inp = make_input(active_accounts=60, icp_accounts=60)
        assert _icp_penetration_pct(inp) == 100.0


# ---------------------------------------------------------------------------
# Class 5 — _whitespace_opportunity
# ---------------------------------------------------------------------------

class TestWhitespaceOpportunity:
    def test_normal(self):
        inp = make_input(whitespace_accounts=10, avg_deal_size_eur=50_000.0)
        assert _whitespace_opportunity(inp) == 500_000.0

    def test_zero_whitespace(self):
        inp = make_input(whitespace_accounts=0, avg_deal_size_eur=50_000.0)
        assert _whitespace_opportunity(inp) == 0.0

    def test_zero_deal_size(self):
        inp = make_input(whitespace_accounts=10, avg_deal_size_eur=0.0)
        assert _whitespace_opportunity(inp) == 0.0

    def test_large_values(self):
        inp = make_input(whitespace_accounts=500, avg_deal_size_eur=200_000.0)
        assert _whitespace_opportunity(inp) == 100_000_000.0

    def test_returns_numeric(self):
        inp = make_input(whitespace_accounts=5, avg_deal_size_eur=10_000.0)
        assert isinstance(_whitespace_opportunity(inp), (int, float))

    def test_rounded_to_zero_decimals(self):
        inp = make_input(whitespace_accounts=3, avg_deal_size_eur=33_333.33)
        result = _whitespace_opportunity(inp)
        assert result == round(3 * 33_333.33, 0)


# ---------------------------------------------------------------------------
# Class 6 — _workload_ratio
# ---------------------------------------------------------------------------

class TestWorkloadRatio:
    def test_normal(self):
        inp = make_input(total_accounts=100, avg_accounts_per_rep_target=100)
        assert _workload_ratio(inp) == 1.0

    def test_overloaded(self):
        inp = make_input(total_accounts=150, avg_accounts_per_rep_target=100)
        assert _workload_ratio(inp) == 1.5

    def test_underloaded(self):
        inp = make_input(total_accounts=50, avg_accounts_per_rep_target=100)
        assert _workload_ratio(inp) == 0.5

    def test_zero_target(self):
        inp = make_input(total_accounts=100, avg_accounts_per_rep_target=0)
        assert _workload_ratio(inp) == 1.0

    def test_negative_target(self):
        inp = make_input(total_accounts=100, avg_accounts_per_rep_target=-10)
        assert _workload_ratio(inp) == 1.0

    def test_returns_float(self):
        inp = make_input(total_accounts=75, avg_accounts_per_rep_target=100)
        assert isinstance(_workload_ratio(inp), float)

    def test_two_decimal_rounding(self):
        inp = make_input(total_accounts=10, avg_accounts_per_rep_target=3)
        assert _workload_ratio(inp) == round(10 / 3, 2)


# ---------------------------------------------------------------------------
# Class 7 — _workload_balance
# ---------------------------------------------------------------------------

class TestWorkloadBalance:
    def test_overloaded_above_1_3(self):
        assert _workload_balance(1.31) == WorkloadBalance.OVERLOADED

    def test_overloaded_exactly_above(self):
        assert _workload_balance(2.0) == WorkloadBalance.OVERLOADED

    def test_underloaded_below_0_7(self):
        assert _workload_balance(0.69) == WorkloadBalance.UNDERLOADED

    def test_underloaded_zero(self):
        assert _workload_balance(0.0) == WorkloadBalance.UNDERLOADED

    def test_balanced_at_1_0(self):
        assert _workload_balance(1.0) == WorkloadBalance.BALANCED

    def test_balanced_at_exactly_0_7(self):
        assert _workload_balance(0.7) == WorkloadBalance.BALANCED

    def test_balanced_at_exactly_1_3(self):
        assert _workload_balance(1.3) == WorkloadBalance.BALANCED

    def test_balanced_low_end(self):
        assert _workload_balance(0.85) == WorkloadBalance.BALANCED

    def test_balanced_high_end(self):
        assert _workload_balance(1.29) == WorkloadBalance.BALANCED


# ---------------------------------------------------------------------------
# Class 8 — _coverage_gap
# ---------------------------------------------------------------------------

class TestCoverageGap:
    def test_none_when_avg_ge_70(self):
        assert _coverage_gap(70.0, 70.0) == CoverageGap.NONE

    def test_none_above_70(self):
        assert _coverage_gap(80.0, 90.0) == CoverageGap.NONE

    def test_minor_avg_50_to_69(self):
        assert _coverage_gap(50.0, 50.0) == CoverageGap.MINOR

    def test_minor_boundary_50(self):
        assert _coverage_gap(50.0, 50.0) == CoverageGap.MINOR

    def test_significant_avg_30_to_49(self):
        assert _coverage_gap(30.0, 30.0) == CoverageGap.SIGNIFICANT

    def test_significant_boundary_30(self):
        assert _coverage_gap(30.0, 30.0) == CoverageGap.SIGNIFICANT

    def test_critical_avg_below_30(self):
        assert _coverage_gap(10.0, 10.0) == CoverageGap.CRITICAL

    def test_critical_zeros(self):
        assert _coverage_gap(0.0, 0.0) == CoverageGap.CRITICAL

    def test_mixed_avg(self):
        # avg of 60 and 80 = 70 → NONE
        assert _coverage_gap(60.0, 80.0) == CoverageGap.NONE

    def test_minor_asymmetric(self):
        # avg of 40 and 60 = 50 → MINOR
        assert _coverage_gap(40.0, 60.0) == CoverageGap.MINOR


# ---------------------------------------------------------------------------
# Class 9 — _territory_score
# ---------------------------------------------------------------------------

class TestTerritoryScore:
    def test_max_score_capped_at_100(self):
        inp = make_input(
            attainment_pct=100.0,
            market_penetration_pct=100.0,
            meetings_held_30d=10,
            proposals_sent_30d=10,
        )
        score = _territory_score(inp, 100.0, 100.0, 1.0)
        assert score == 100.0

    def test_min_score_at_zero(self):
        inp = make_input(
            attainment_pct=0.0,
            market_penetration_pct=0.0,
            meetings_held_30d=0,
            proposals_sent_30d=0,
        )
        score = _territory_score(inp, 0.0, 0.0, 0.0)
        assert score == 0.0

    def test_coverage_contributes_max_30(self):
        inp = make_input(attainment_pct=0.0, market_penetration_pct=0.0, meetings_held_30d=0, proposals_sent_30d=0)
        score = _territory_score(inp, 100.0, 0.0, 0.0)
        # coverage*0.3 = 30, no workload pts (ratio=0 < 0.5)
        assert score == 30.0

    def test_icp_contributes_max_25(self):
        inp = make_input(attainment_pct=0.0, market_penetration_pct=0.0, meetings_held_30d=0, proposals_sent_30d=0)
        score = _territory_score(inp, 0.0, 100.0, 0.0)
        assert score == 25.0

    def test_attainment_contributes_max_20(self):
        inp = make_input(attainment_pct=100.0, market_penetration_pct=0.0, meetings_held_30d=0, proposals_sent_30d=0)
        score = _territory_score(inp, 0.0, 0.0, 0.0)
        assert score == 20.0

    def test_workload_10_pts_for_ratio_0_85_to_1_15(self):
        inp = make_input(attainment_pct=0.0, market_penetration_pct=0.0, meetings_held_30d=0, proposals_sent_30d=0)
        score = _territory_score(inp, 0.0, 0.0, 1.0)
        assert score == 10.0

    def test_workload_6_pts_for_ratio_0_7_to_1_3(self):
        inp = make_input(attainment_pct=0.0, market_penetration_pct=0.0, meetings_held_30d=0, proposals_sent_30d=0)
        score = _territory_score(inp, 0.0, 0.0, 0.8)
        assert score == 6.0

    def test_workload_3_pts_for_ratio_0_5_to_1_5(self):
        inp = make_input(attainment_pct=0.0, market_penetration_pct=0.0, meetings_held_30d=0, proposals_sent_30d=0)
        score = _territory_score(inp, 0.0, 0.0, 0.6)
        assert score == 3.0

    def test_workload_0_pts_outside_range(self):
        inp = make_input(attainment_pct=0.0, market_penetration_pct=0.0, meetings_held_30d=0, proposals_sent_30d=0)
        score = _territory_score(inp, 0.0, 0.0, 2.0)
        assert score == 0.0

    def test_market_penetration_max_10(self):
        inp = make_input(attainment_pct=0.0, market_penetration_pct=100.0, meetings_held_30d=0, proposals_sent_30d=0)
        score = _territory_score(inp, 0.0, 0.0, 0.0)
        assert score == 10.0

    def test_meetings_max_2_5(self):
        inp = make_input(attainment_pct=0.0, market_penetration_pct=0.0, meetings_held_30d=100, proposals_sent_30d=0)
        score = _territory_score(inp, 0.0, 0.0, 0.0)
        assert score == 2.5

    def test_proposals_max_2_5(self):
        inp = make_input(attainment_pct=0.0, market_penetration_pct=0.0, meetings_held_30d=0, proposals_sent_30d=100)
        score = _territory_score(inp, 0.0, 0.0, 0.0)
        assert score == 2.5

    def test_returns_numeric(self):
        inp = make_input()
        score = _territory_score(inp, 50.0, 50.0, 1.0)
        assert isinstance(score, (int, float))

    def test_score_one_decimal(self):
        inp = make_input(attainment_pct=33.3, market_penetration_pct=0.0, meetings_held_30d=0, proposals_sent_30d=0)
        score = _territory_score(inp, 0.0, 0.0, 0.0)
        assert score == round(min(100.0, 33.3 * 0.2), 1)


# ---------------------------------------------------------------------------
# Class 10 — _territory_health
# ---------------------------------------------------------------------------

class TestTerritoryHealth:
    def test_excellent_at_75(self):
        assert _territory_health(75.0) == TerritoryHealth.EXCELLENT

    def test_excellent_above_75(self):
        assert _territory_health(99.0) == TerritoryHealth.EXCELLENT

    def test_good_at_55(self):
        assert _territory_health(55.0) == TerritoryHealth.GOOD

    def test_good_at_74(self):
        assert _territory_health(74.9) == TerritoryHealth.GOOD

    def test_fair_at_35(self):
        assert _territory_health(35.0) == TerritoryHealth.FAIR

    def test_fair_at_54(self):
        assert _territory_health(54.9) == TerritoryHealth.FAIR

    def test_poor_below_35(self):
        assert _territory_health(34.9) == TerritoryHealth.POOR

    def test_poor_at_zero(self):
        assert _territory_health(0.0) == TerritoryHealth.POOR


# ---------------------------------------------------------------------------
# Class 11 — _territory_action
# ---------------------------------------------------------------------------

class TestTerritoryAction:
    def test_restructure_for_poor_health(self):
        result = _territory_action(TerritoryHealth.POOR, CoverageGap.NONE, WorkloadBalance.BALANCED)
        assert result == TerritoryAction.RESTRUCTURE

    def test_restructure_for_critical_gap(self):
        result = _territory_action(TerritoryHealth.GOOD, CoverageGap.CRITICAL, WorkloadBalance.BALANCED)
        assert result == TerritoryAction.RESTRUCTURE

    def test_restructure_poor_plus_critical(self):
        result = _territory_action(TerritoryHealth.POOR, CoverageGap.CRITICAL, WorkloadBalance.OVERLOADED)
        assert result == TerritoryAction.RESTRUCTURE

    def test_rebalance_for_overloaded(self):
        result = _territory_action(TerritoryHealth.GOOD, CoverageGap.NONE, WorkloadBalance.OVERLOADED)
        assert result == TerritoryAction.REBALANCE

    def test_rebalance_for_underloaded(self):
        result = _territory_action(TerritoryHealth.GOOD, CoverageGap.NONE, WorkloadBalance.UNDERLOADED)
        assert result == TerritoryAction.REBALANCE

    def test_rebalance_for_significant_gap(self):
        result = _territory_action(TerritoryHealth.GOOD, CoverageGap.SIGNIFICANT, WorkloadBalance.BALANCED)
        assert result == TerritoryAction.REBALANCE

    def test_expand_for_fair_health(self):
        result = _territory_action(TerritoryHealth.FAIR, CoverageGap.NONE, WorkloadBalance.BALANCED)
        assert result == TerritoryAction.EXPAND

    def test_expand_for_minor_gap(self):
        result = _territory_action(TerritoryHealth.GOOD, CoverageGap.MINOR, WorkloadBalance.BALANCED)
        assert result == TerritoryAction.EXPAND

    def test_optimize_for_excellent(self):
        result = _territory_action(TerritoryHealth.EXCELLENT, CoverageGap.NONE, WorkloadBalance.BALANCED)
        assert result == TerritoryAction.OPTIMIZE

    def test_optimize_for_good_no_issues(self):
        result = _territory_action(TerritoryHealth.GOOD, CoverageGap.NONE, WorkloadBalance.BALANCED)
        assert result == TerritoryAction.OPTIMIZE


# ---------------------------------------------------------------------------
# Class 12 — _optimization_score
# ---------------------------------------------------------------------------

class TestOptimizationScore:
    def test_returns_numeric(self):
        inp = make_input()
        result = _optimization_score(inp, 50.0, 1.0)
        assert isinstance(result, (int, float))

    def test_score_in_0_to_100(self):
        inp = make_input()
        result = _optimization_score(inp, 50.0, 1.0)
        assert 0.0 <= result <= 100.0

    def test_perfect_optimization(self):
        # No whitespace (activated), no geo concentration, balanced workload,
        # many meetings per account, high proposals per meeting, full market penetration
        inp = make_input(
            whitespace_accounts=0,
            icp_accounts=10,
            geographic_concentration_pct=0.0,
            market_penetration_pct=50.0,
            meetings_held_30d=100,
            proposals_sent_30d=100,
            active_accounts=1,
        )
        result = _optimization_score(inp, 100.0, 1.0)
        assert result == 100.0

    def test_no_whitespace_gives_max_ws_component(self):
        inp = make_input(whitespace_accounts=0, icp_accounts=10)
        # ws_ratio = 1 - 0/10 = 1.0 → ws_score = 25
        result = _optimization_score(inp, 50.0, 1.0)
        # Just verify ws contributes fully when whitespace=0
        assert result > 0.0

    def test_all_whitespace_reduces_ws_component(self):
        inp_no_ws = make_input(whitespace_accounts=0, icp_accounts=20)
        inp_all_ws = make_input(whitespace_accounts=20, icp_accounts=20)
        score_no = _optimization_score(inp_no_ws, 50.0, 1.0)
        score_all = _optimization_score(inp_all_ws, 50.0, 1.0)
        assert score_no > score_all

    def test_high_geo_concentration_lowers_score(self):
        inp_low = make_input(geographic_concentration_pct=10.0)
        inp_high = make_input(geographic_concentration_pct=90.0)
        assert _optimization_score(inp_low, 50.0, 1.0) > _optimization_score(inp_high, 50.0, 1.0)

    def test_workload_at_1_gives_20_pts(self):
        inp = make_input(
            whitespace_accounts=0,
            icp_accounts=10,
            geographic_concentration_pct=100.0,
            market_penetration_pct=0.0,
            meetings_held_30d=0,
            proposals_sent_30d=0,
        )
        result = _optimization_score(inp, 0.0, 1.0)
        # ws=25, geo=0, workload=20 (deviation=0), activity=0, market=0 → 45
        assert result == 45.0

    def test_score_one_decimal(self):
        inp = make_input()
        result = _optimization_score(inp, 50.0, 1.0)
        assert result == round(result, 1)


# ---------------------------------------------------------------------------
# Class 13 — _territory_drivers
# ---------------------------------------------------------------------------

class TestTerritoryDrivers:
    def test_low_coverage_driver(self):
        inp = make_input(active_accounts=30, total_accounts=100)
        drivers = _territory_drivers(inp, 30.0, 50.0, 1.0, WorkloadBalance.BALANCED)
        assert any("Couverture" in d for d in drivers)

    def test_low_icp_penetration_driver(self):
        inp = make_input(active_accounts=20, icp_accounts=60)
        drivers = _territory_drivers(inp, 50.0, 30.0, 1.0, WorkloadBalance.BALANCED)
        assert any("ICP" in d for d in drivers)

    def test_whitespace_driver(self):
        inp = make_input(whitespace_accounts=20, icp_accounts=30)
        # 20 > 30*0.3=9 → trigger
        drivers = _territory_drivers(inp, 50.0, 50.0, 1.0, WorkloadBalance.BALANCED)
        assert any("whitespace" in d for d in drivers)

    def test_overloaded_driver(self):
        inp = make_input(total_accounts=150, avg_accounts_per_rep_target=100)
        drivers = _territory_drivers(inp, 50.0, 50.0, 1.5, WorkloadBalance.OVERLOADED)
        assert any("surchargé" in d for d in drivers)

    def test_underloaded_driver(self):
        inp = make_input(total_accounts=50, avg_accounts_per_rep_target=100)
        drivers = _territory_drivers(inp, 50.0, 50.0, 0.5, WorkloadBalance.UNDERLOADED)
        assert any("sous-chargé" in d for d in drivers)

    def test_geo_concentration_driver(self):
        inp = make_input(geographic_concentration_pct=80.0)
        drivers = _territory_drivers(inp, 50.0, 50.0, 1.0, WorkloadBalance.BALANCED)
        assert any("géographique" in d for d in drivers)

    def test_low_market_penetration_driver(self):
        inp = make_input(market_penetration_pct=10.0)
        drivers = _territory_drivers(inp, 50.0, 50.0, 1.0, WorkloadBalance.BALANCED)
        assert any("marché" in d.lower() for d in drivers)

    def test_dormant_exceeds_active_driver(self):
        inp = make_input(dormant_accounts=60, active_accounts=30)
        drivers = _territory_drivers(inp, 50.0, 50.0, 1.0, WorkloadBalance.BALANCED)
        assert any("dormants" in d for d in drivers)

    def test_competitor_driver(self):
        inp = make_input(competitor_accounts=40, active_accounts=50)
        # 40 > 50*0.5=25 → trigger
        drivers = _territory_drivers(inp, 50.0, 50.0, 1.0, WorkloadBalance.BALANCED)
        assert any("concurrentielle" in d or "concurrence" in d for d in drivers)

    def test_low_outbound_driver(self):
        inp = make_input(outbound_activities_30d=10)
        drivers = _territory_drivers(inp, 50.0, 50.0, 1.0, WorkloadBalance.BALANCED)
        assert any("outbound" in d.lower() for d in drivers)

    def test_no_drivers_for_healthy_territory(self):
        inp = make_input(
            active_accounts=80,
            total_accounts=100,
            icp_accounts=60,
            dormant_accounts=10,
            whitespace_accounts=5,
            competitor_accounts=5,
            geographic_concentration_pct=30.0,
            market_penetration_pct=25.0,
            outbound_activities_30d=30,
            avg_accounts_per_rep_target=100,
        )
        drivers = _territory_drivers(inp, 80.0, 80.0, 1.0, WorkloadBalance.BALANCED)
        assert drivers == []

    def test_returns_list(self):
        inp = make_input()
        drivers = _territory_drivers(inp, 50.0, 50.0, 1.0, WorkloadBalance.BALANCED)
        assert isinstance(drivers, list)


# ---------------------------------------------------------------------------
# Class 14 — _territory_plays
# ---------------------------------------------------------------------------

class TestTerritoryPlays:
    def test_restructure_plays_not_empty(self):
        inp = make_input()
        plays = _territory_plays(TerritoryAction.RESTRUCTURE, inp, CoverageGap.CRITICAL)
        assert len(plays) >= 3

    def test_restructure_includes_whitespace_play_when_enough(self):
        inp = make_input(whitespace_accounts=10)
        plays = _territory_plays(TerritoryAction.RESTRUCTURE, inp, CoverageGap.CRITICAL)
        assert any("whitespace" in p.lower() or "non contactés" in p for p in plays)

    def test_restructure_no_whitespace_play_when_few(self):
        inp = make_input(whitespace_accounts=3)
        plays = _territory_plays(TerritoryAction.RESTRUCTURE, inp, CoverageGap.CRITICAL)
        # whitespace_accounts=3 <= 5, so extra whitespace play should not be added
        whitespace_plays = [p for p in plays if "non contactés" in p or "whitespace" in p.lower()]
        assert len(whitespace_plays) == 0

    def test_rebalance_plays(self):
        inp = make_input()
        plays = _territory_plays(TerritoryAction.REBALANCE, inp, CoverageGap.SIGNIFICANT)
        assert len(plays) >= 3

    def test_expand_plays(self):
        inp = make_input()
        plays = _territory_plays(TerritoryAction.EXPAND, inp, CoverageGap.MINOR)
        assert len(plays) >= 3

    def test_expand_includes_expansion_signals_play(self):
        inp = make_input(expansion_signals=5)
        plays = _territory_plays(TerritoryAction.EXPAND, inp, CoverageGap.MINOR)
        assert any("5" in p for p in plays)

    def test_expand_no_signals_play_when_zero(self):
        inp = make_input(expansion_signals=0)
        plays = _territory_plays(TerritoryAction.EXPAND, inp, CoverageGap.MINOR)
        # no "signaux expansion" extra play when signals=0
        signal_plays = [p for p in plays if "signaux expansion" in p]
        assert len(signal_plays) == 0

    def test_optimize_plays(self):
        inp = make_input()
        plays = _territory_plays(TerritoryAction.OPTIMIZE, inp, CoverageGap.NONE)
        assert len(plays) >= 3

    def test_returns_list(self):
        inp = make_input()
        plays = _territory_plays(TerritoryAction.OPTIMIZE, inp, CoverageGap.NONE)
        assert isinstance(plays, list)


# ---------------------------------------------------------------------------
# Class 15 — TerritoryResult.to_dict
# ---------------------------------------------------------------------------

class TestTerritoryResultToDict:
    def _make_result(self) -> TerritoryResult:
        engine = TerritoryOptimizerEngine()
        return engine.analyze(make_input())

    def test_to_dict_returns_dict(self):
        result = self._make_result()
        assert isinstance(result.to_dict(), dict)

    def test_to_dict_has_all_keys(self):
        d = self._make_result().to_dict()
        expected_keys = {
            "rep_id", "rep_name", "region", "segment", "quota_eur",
            "territory_health", "territory_action", "coverage_gap",
            "workload_balance", "territory_score", "coverage_pct",
            "icp_penetration_pct", "whitespace_opportunity_eur",
            "workload_ratio", "market_penetration_pct",
            "territory_drivers", "territory_plays", "optimization_score",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_values_are_strings(self):
        d = self._make_result().to_dict()
        assert isinstance(d["territory_health"], str)
        assert isinstance(d["territory_action"], str)
        assert isinstance(d["coverage_gap"], str)
        assert isinstance(d["workload_balance"], str)

    def test_to_dict_health_value_is_enum_value(self):
        result = self._make_result()
        d = result.to_dict()
        assert d["territory_health"] == result.territory_health.value

    def test_to_dict_lists_are_lists(self):
        d = self._make_result().to_dict()
        assert isinstance(d["territory_drivers"], list)
        assert isinstance(d["territory_plays"], list)

    def test_to_dict_numeric_fields(self):
        d = self._make_result().to_dict()
        assert isinstance(d["territory_score"], (int, float))
        assert isinstance(d["coverage_pct"], (int, float))
        assert isinstance(d["icp_penetration_pct"], (int, float))
        assert isinstance(d["whitespace_opportunity_eur"], (int, float))
        assert isinstance(d["workload_ratio"], (int, float))
        assert isinstance(d["optimization_score"], (int, float))


# ---------------------------------------------------------------------------
# Class 16 — TerritoryOptimizerEngine.analyze basics
# ---------------------------------------------------------------------------

class TestEngineAnalyze:
    def test_returns_territory_result(self):
        engine = TerritoryOptimizerEngine()
        result = engine.analyze(make_input())
        assert isinstance(result, TerritoryResult)

    def test_rep_id_matches(self):
        engine = TerritoryOptimizerEngine()
        result = engine.analyze(make_input(rep_id="X99"))
        assert result.rep_id == "X99"

    def test_rep_name_matches(self):
        engine = TerritoryOptimizerEngine()
        result = engine.analyze(make_input(rep_name="Bob"))
        assert result.rep_name == "Bob"

    def test_region_matches(self):
        engine = TerritoryOptimizerEngine()
        result = engine.analyze(make_input(region="APAC"))
        assert result.region == "APAC"

    def test_quota_matches(self):
        engine = TerritoryOptimizerEngine()
        result = engine.analyze(make_input(quota_eur=999_999.0))
        assert result.quota_eur == 999_999.0

    def test_coverage_pct_correct(self):
        engine = TerritoryOptimizerEngine()
        result = engine.analyze(make_input(active_accounts=40, total_accounts=80))
        assert result.coverage_pct == 50.0

    def test_whitespace_opportunity_correct(self):
        engine = TerritoryOptimizerEngine()
        result = engine.analyze(make_input(whitespace_accounts=5, avg_deal_size_eur=20_000.0))
        assert result.whitespace_opportunity_eur == 100_000.0

    def test_workload_ratio_correct(self):
        engine = TerritoryOptimizerEngine()
        result = engine.analyze(make_input(total_accounts=80, avg_accounts_per_rep_target=100))
        assert result.workload_ratio == 0.8

    def test_territory_score_in_range(self):
        engine = TerritoryOptimizerEngine()
        result = engine.analyze(make_input())
        assert 0.0 <= result.territory_score <= 100.0

    def test_optimization_score_in_range(self):
        engine = TerritoryOptimizerEngine()
        result = engine.analyze(make_input())
        assert 0.0 <= result.optimization_score <= 100.0

    def test_result_stored_in_engine(self):
        engine = TerritoryOptimizerEngine()
        engine.analyze(make_input(rep_id="STORE_TEST"))
        assert "STORE_TEST" in engine._results

    def test_second_analyze_overwrites_same_rep(self):
        engine = TerritoryOptimizerEngine()
        engine.analyze(make_input(rep_id="OVER", attainment_pct=20.0))
        engine.analyze(make_input(rep_id="OVER", attainment_pct=80.0))
        assert len(engine._results) == 1

    def test_territory_plays_not_empty(self):
        engine = TerritoryOptimizerEngine()
        result = engine.analyze(make_input())
        assert len(result.territory_plays) > 0

    def test_market_penetration_pct_preserved(self):
        engine = TerritoryOptimizerEngine()
        result = engine.analyze(make_input(market_penetration_pct=33.3))
        assert result.market_penetration_pct == 33.3


# ---------------------------------------------------------------------------
# Class 17 — analyze_batch
# ---------------------------------------------------------------------------

class TestAnalyzeBatch:
    def test_returns_list(self):
        engine = TerritoryOptimizerEngine()
        results = engine.analyze_batch([make_input(rep_id="A"), make_input(rep_id="B")])
        assert isinstance(results, list)

    def test_sorted_ascending_by_territory_score(self):
        engine = TerritoryOptimizerEngine()
        poor = make_input(
            rep_id="POOR",
            attainment_pct=0.0,
            active_accounts=5,
            total_accounts=100,
            icp_accounts=60,
            market_penetration_pct=0.0,
            meetings_held_30d=0,
            proposals_sent_30d=0,
        )
        good = make_input(
            rep_id="GOOD",
            attainment_pct=100.0,
            active_accounts=90,
            total_accounts=100,
            icp_accounts=60,
            market_penetration_pct=50.0,
            meetings_held_30d=10,
            proposals_sent_30d=10,
        )
        results = engine.analyze_batch([good, poor])
        assert results[0].territory_score <= results[1].territory_score

    def test_batch_stores_all_results(self):
        engine = TerritoryOptimizerEngine()
        engine.analyze_batch([make_input(rep_id="X"), make_input(rep_id="Y"), make_input(rep_id="Z")])
        assert len(engine._results) == 3

    def test_empty_batch(self):
        engine = TerritoryOptimizerEngine()
        results = engine.analyze_batch([])
        assert results == []

    def test_single_item_batch(self):
        engine = TerritoryOptimizerEngine()
        results = engine.analyze_batch([make_input(rep_id="SOLO")])
        assert len(results) == 1
        assert results[0].rep_id == "SOLO"

    def test_batch_result_count(self):
        engine = TerritoryOptimizerEngine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = engine.analyze_batch(inputs)
        assert len(results) == 5


# ---------------------------------------------------------------------------
# Class 18 — by_health, by_action, by_coverage_gap
# ---------------------------------------------------------------------------

class TestFilterMethods:
    def setup_method(self):
        self.engine = TerritoryOptimizerEngine()
        # POOR territory
        self.engine.analyze(make_input(
            rep_id="POOR1",
            attainment_pct=0.0,
            active_accounts=5,
            total_accounts=100,
            icp_accounts=60,
            market_penetration_pct=0.0,
            meetings_held_30d=0,
            proposals_sent_30d=0,
        ))
        # Healthy territory
        self.engine.analyze(make_input(
            rep_id="GOOD1",
            attainment_pct=90.0,
            active_accounts=90,
            total_accounts=100,
            icp_accounts=60,
            market_penetration_pct=40.0,
            meetings_held_30d=10,
            proposals_sent_30d=10,
        ))

    def test_by_health_poor_returns_poor(self):
        results = self.engine.by_health(TerritoryHealth.POOR)
        assert all(r.territory_health == TerritoryHealth.POOR for r in results)

    def test_by_health_excellent_or_good(self):
        results = self.engine.by_health(TerritoryHealth.EXCELLENT) + self.engine.by_health(TerritoryHealth.GOOD)
        ids = {r.rep_id for r in results}
        assert "GOOD1" in ids

    def test_by_action_returns_correct(self):
        restructure = self.engine.by_action(TerritoryAction.RESTRUCTURE)
        assert all(r.territory_action == TerritoryAction.RESTRUCTURE for r in restructure)

    def test_by_coverage_gap_returns_correct(self):
        for gap in CoverageGap:
            results = self.engine.by_coverage_gap(gap)
            assert all(r.coverage_gap == gap for r in results)

    def test_by_health_returns_list(self):
        results = self.engine.by_health(TerritoryHealth.GOOD)
        assert isinstance(results, list)

    def test_by_action_returns_list(self):
        results = self.engine.by_action(TerritoryAction.OPTIMIZE)
        assert isinstance(results, list)


# ---------------------------------------------------------------------------
# Class 19 — poor_territories, needs_restructure, overloaded, underloaded, excellent
# ---------------------------------------------------------------------------

class TestConvenienceMethods:
    def setup_method(self):
        self.engine = TerritoryOptimizerEngine()

    def test_poor_territories_delegates_to_by_health(self):
        self.engine.analyze(make_input(
            rep_id="P1",
            attainment_pct=0.0,
            active_accounts=2,
            total_accounts=100,
            market_penetration_pct=0.0,
            meetings_held_30d=0,
            proposals_sent_30d=0,
        ))
        poor = self.engine.poor_territories()
        assert all(r.territory_health == TerritoryHealth.POOR for r in poor)

    def test_needs_restructure_delegates(self):
        results = self.engine.needs_restructure()
        assert all(r.territory_action == TerritoryAction.RESTRUCTURE for r in results)

    def test_overloaded_reps_found(self):
        self.engine.analyze(make_input(
            rep_id="OVER1",
            total_accounts=200,
            avg_accounts_per_rep_target=100,
        ))
        overloaded = self.engine.overloaded_reps()
        ids = {r.rep_id for r in overloaded}
        assert "OVER1" in ids

    def test_underloaded_reps_found(self):
        self.engine.analyze(make_input(
            rep_id="UNDER1",
            total_accounts=30,
            avg_accounts_per_rep_target=100,
        ))
        underloaded = self.engine.underloaded_reps()
        ids = {r.rep_id for r in underloaded}
        assert "UNDER1" in ids

    def test_excellent_territories(self):
        self.engine.analyze(make_input(
            rep_id="EXC1",
            attainment_pct=100.0,
            active_accounts=95,
            total_accounts=100,
            icp_accounts=60,
            market_penetration_pct=50.0,
            meetings_held_30d=10,
            proposals_sent_30d=10,
        ))
        excellent = self.engine.excellent_territories()
        assert all(r.territory_health == TerritoryHealth.EXCELLENT for r in excellent)

    def test_all_return_lists(self):
        assert isinstance(self.engine.poor_territories(), list)
        assert isinstance(self.engine.needs_restructure(), list)
        assert isinstance(self.engine.overloaded_reps(), list)
        assert isinstance(self.engine.underloaded_reps(), list)
        assert isinstance(self.engine.excellent_territories(), list)


# ---------------------------------------------------------------------------
# Class 20 — Aggregate metrics
# ---------------------------------------------------------------------------

class TestAggregateMetrics:
    def setup_method(self):
        self.engine = TerritoryOptimizerEngine()

    def test_total_whitespace_eur_empty(self):
        assert self.engine.total_whitespace_eur() == 0.0

    def test_total_whitespace_eur_sum(self):
        self.engine.analyze(make_input(rep_id="W1", whitespace_accounts=10, avg_deal_size_eur=10_000.0))
        self.engine.analyze(make_input(rep_id="W2", whitespace_accounts=5, avg_deal_size_eur=10_000.0))
        assert self.engine.total_whitespace_eur() == 150_000.0

    def test_avg_territory_score_empty(self):
        assert self.engine.avg_territory_score() == 0.0

    def test_avg_territory_score_single(self):
        self.engine.analyze(make_input(rep_id="S1"))
        score = self.engine.avg_territory_score()
        assert isinstance(score, (int, float))
        assert score >= 0.0

    def test_avg_coverage_pct_empty(self):
        assert self.engine.avg_coverage_pct() == 0.0

    def test_avg_coverage_pct_value(self):
        self.engine.analyze(make_input(rep_id="C1", active_accounts=80, total_accounts=100))
        self.engine.analyze(make_input(rep_id="C2", active_accounts=60, total_accounts=100))
        avg = self.engine.avg_coverage_pct()
        assert avg == 70.0

    def test_avg_optimization_score_empty(self):
        assert self.engine.avg_optimization_score() == 0.0

    def test_avg_optimization_score_returns_numeric(self):
        self.engine.analyze(make_input(rep_id="O1"))
        self.engine.analyze(make_input(rep_id="O2"))
        result = self.engine.avg_optimization_score()
        assert isinstance(result, (int, float))

    def test_totals_are_numeric(self):
        self.engine.analyze(make_input(rep_id="NUM1"))
        assert isinstance(self.engine.total_whitespace_eur(), (int, float))
        assert isinstance(self.engine.avg_territory_score(), (int, float))
        assert isinstance(self.engine.avg_coverage_pct(), (int, float))
        assert isinstance(self.engine.avg_optimization_score(), (int, float))


# ---------------------------------------------------------------------------
# Class 21 — summary
# ---------------------------------------------------------------------------

class TestSummary:
    def setup_method(self):
        self.engine = TerritoryOptimizerEngine()

    def test_summary_empty(self):
        s = self.engine.summary()
        assert s["total"] == 0
        assert s["poor_count"] == 0
        assert s["restructure_count"] == 0
        assert s["total_whitespace_eur"] == 0.0

    def test_summary_keys(self):
        s = self.engine.summary()
        expected = {
            "total", "health_counts", "action_counts", "coverage_gap_counts",
            "avg_territory_score", "avg_coverage_pct", "avg_optimization_score",
            "poor_count", "restructure_count", "total_whitespace_eur",
        }
        assert set(s.keys()) == expected

    def test_summary_total_count(self):
        self.engine.analyze(make_input(rep_id="S1"))
        self.engine.analyze(make_input(rep_id="S2"))
        assert self.engine.summary()["total"] == 2

    def test_summary_health_counts_all_health_keys(self):
        self.engine.analyze(make_input(rep_id="H1"))
        health_counts = self.engine.summary()["health_counts"]
        for h in TerritoryHealth:
            assert h.value in health_counts

    def test_summary_action_counts_all_action_keys(self):
        self.engine.analyze(make_input(rep_id="A1"))
        action_counts = self.engine.summary()["action_counts"]
        for a in TerritoryAction:
            assert a.value in action_counts

    def test_summary_coverage_gap_counts_all_gap_keys(self):
        self.engine.analyze(make_input(rep_id="G1"))
        gap_counts = self.engine.summary()["coverage_gap_counts"]
        for g in CoverageGap:
            assert g.value in gap_counts

    def test_summary_health_counts_sum_to_total(self):
        self.engine.analyze(make_input(rep_id="T1"))
        self.engine.analyze(make_input(rep_id="T2"))
        s = self.engine.summary()
        assert sum(s["health_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_to_total(self):
        self.engine.analyze(make_input(rep_id="T3"))
        s = self.engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_whitespace_eur(self):
        self.engine.analyze(make_input(rep_id="W1", whitespace_accounts=10, avg_deal_size_eur=5_000.0))
        assert self.engine.summary()["total_whitespace_eur"] == 50_000.0

    def test_summary_avg_scores_are_numeric(self):
        self.engine.analyze(make_input(rep_id="AVG1"))
        s = self.engine.summary()
        assert isinstance(s["avg_territory_score"], (int, float))
        assert isinstance(s["avg_coverage_pct"], (int, float))
        assert isinstance(s["avg_optimization_score"], (int, float))


# ---------------------------------------------------------------------------
# Class 22 — reset
# ---------------------------------------------------------------------------

class TestReset:
    def test_reset_clears_results(self):
        engine = TerritoryOptimizerEngine()
        engine.analyze(make_input(rep_id="CLR1"))
        engine.analyze(make_input(rep_id="CLR2"))
        engine.reset()
        assert len(engine._results) == 0

    def test_avg_territory_score_after_reset(self):
        engine = TerritoryOptimizerEngine()
        engine.analyze(make_input(rep_id="SC1"))
        engine.reset()
        assert engine.avg_territory_score() == 0.0

    def test_avg_coverage_pct_after_reset(self):
        engine = TerritoryOptimizerEngine()
        engine.analyze(make_input(rep_id="COV1"))
        engine.reset()
        assert engine.avg_coverage_pct() == 0.0

    def test_avg_optimization_score_after_reset(self):
        engine = TerritoryOptimizerEngine()
        engine.analyze(make_input(rep_id="OPT1"))
        engine.reset()
        assert engine.avg_optimization_score() == 0.0

    def test_total_whitespace_after_reset(self):
        engine = TerritoryOptimizerEngine()
        engine.analyze(make_input(rep_id="WS1", whitespace_accounts=10, avg_deal_size_eur=10_000.0))
        engine.reset()
        assert engine.total_whitespace_eur() == 0.0

    def test_summary_total_after_reset(self):
        engine = TerritoryOptimizerEngine()
        engine.analyze(make_input(rep_id="SUM1"))
        engine.reset()
        assert engine.summary()["total"] == 0

    def test_can_analyze_after_reset(self):
        engine = TerritoryOptimizerEngine()
        engine.analyze(make_input(rep_id="BEFORE"))
        engine.reset()
        result = engine.analyze(make_input(rep_id="AFTER"))
        assert result.rep_id == "AFTER"
        assert len(engine._results) == 1

    def test_reset_idempotent(self):
        engine = TerritoryOptimizerEngine()
        engine.reset()
        engine.reset()
        assert len(engine._results) == 0


# ---------------------------------------------------------------------------
# Class 23 — End-to-end scenario: poor territory
# ---------------------------------------------------------------------------

class TestPoorTerritoryScenario:
    def test_poor_territory_is_restructure(self):
        engine = TerritoryOptimizerEngine()
        result = engine.analyze(make_input(
            rep_id="POOR_E2E",
            attainment_pct=5.0,
            active_accounts=3,
            total_accounts=100,
            icp_accounts=60,
            market_penetration_pct=2.0,
            meetings_held_30d=0,
            proposals_sent_30d=0,
            whitespace_accounts=50,
            dormant_accounts=80,
            outbound_activities_30d=5,
        ))
        assert result.territory_health == TerritoryHealth.POOR
        assert result.territory_action == TerritoryAction.RESTRUCTURE
        assert result.territory_score < 35.0
        assert len(result.territory_drivers) > 0
        assert len(result.territory_plays) > 0

    def test_poor_territory_in_poor_territories(self):
        engine = TerritoryOptimizerEngine()
        engine.analyze(make_input(
            rep_id="POOR_E2E2",
            attainment_pct=0.0,
            active_accounts=1,
            total_accounts=100,
            icp_accounts=60,
            market_penetration_pct=0.0,
            meetings_held_30d=0,
            proposals_sent_30d=0,
        ))
        ids = {r.rep_id for r in engine.poor_territories()}
        assert "POOR_E2E2" in ids


# ---------------------------------------------------------------------------
# Class 24 — End-to-end scenario: excellent territory
# ---------------------------------------------------------------------------

class TestExcellentTerritoryScenario:
    def test_excellent_territory_is_optimize(self):
        engine = TerritoryOptimizerEngine()
        result = engine.analyze(make_input(
            rep_id="EXC_E2E",
            attainment_pct=100.0,
            active_accounts=95,
            total_accounts=100,
            icp_accounts=60,
            avg_accounts_per_rep_target=100,
            market_penetration_pct=50.0,
            meetings_held_30d=10,
            proposals_sent_30d=10,
            dormant_accounts=2,
            whitespace_accounts=2,
            outbound_activities_30d=50,
            competitor_accounts=5,
            geographic_concentration_pct=20.0,
        ))
        assert result.territory_health == TerritoryHealth.EXCELLENT
        assert result.territory_score >= 75.0
        assert result.territory_action == TerritoryAction.OPTIMIZE

    def test_excellent_territory_in_excellent(self):
        engine = TerritoryOptimizerEngine()
        engine.analyze(make_input(
            rep_id="EXC_E2E2",
            attainment_pct=100.0,
            active_accounts=95,
            total_accounts=100,
            icp_accounts=60,
            avg_accounts_per_rep_target=100,
            market_penetration_pct=50.0,
            meetings_held_30d=10,
            proposals_sent_30d=10,
        ))
        ids = {r.rep_id for r in engine.excellent_territories()}
        assert "EXC_E2E2" in ids
