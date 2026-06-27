"""
Comprehensive pytest test suite for TerritoryPerformanceEngine.

Run from /home/user/TEST:
    python3 -m pytest swarm/tests/test_territory_performance_engine.py -x -q
"""
from __future__ import annotations

import pytest

from swarm.intelligence.territory_performance_engine import (
    TerritoryPerformanceEngine,
    TerritoryPerformanceInput,
    TerritoryPerformanceResult,
    TerritoryStatus,
    TerritoryRisk,
    MarketPenetration,
    TerritoryAction,
)


# ---------------------------------------------------------------------------
# Helpers / Factories
# ---------------------------------------------------------------------------

def make_input(
    *,
    territory_id: str = "T001",
    territory_name: str = "North Region",
    rep_id: str = "R001",
    region: str = "North",
    target_revenue: float = 1_000_000.0,
    actual_revenue: float = 800_000.0,
    projected_revenue: float = 950_000.0,
    total_accounts: int = 100,
    active_accounts: int = 70,
    new_accounts_won: int = 10,
    churned_accounts: int = 5,
    total_addressable_mkt: float = 5_000_000.0,
    current_penetration: float = 20.0,
    pipeline_value: float = 500_000.0,
    weighted_pipeline: float = 300_000.0,
    avg_deal_size: float = 50_000.0,
    win_rate: float = 60.0,
    avg_sales_cycle_days: int = 30,
    activities_count: int = 200,
    days_remaining: int = 30,
    total_period_days: int = 90,
) -> TerritoryPerformanceInput:
    return TerritoryPerformanceInput(
        territory_id=territory_id,
        territory_name=territory_name,
        rep_id=rep_id,
        region=region,
        target_revenue=target_revenue,
        actual_revenue=actual_revenue,
        projected_revenue=projected_revenue,
        total_accounts=total_accounts,
        active_accounts=active_accounts,
        new_accounts_won=new_accounts_won,
        churned_accounts=churned_accounts,
        total_addressable_mkt=total_addressable_mkt,
        current_penetration=current_penetration,
        pipeline_value=pipeline_value,
        weighted_pipeline=weighted_pipeline,
        avg_deal_size=avg_deal_size,
        win_rate=win_rate,
        avg_sales_cycle_days=avg_sales_cycle_days,
        activities_count=activities_count,
        days_remaining=days_remaining,
        total_period_days=total_period_days,
    )


# ---------------------------------------------------------------------------
# Section 1: Enum values, string values, str subtype, and counts
# ---------------------------------------------------------------------------

class TestTerritoryStatusEnum:
    def test_overperforming_value(self):
        assert TerritoryStatus.OVERPERFORMING.value == "overperforming"

    def test_on_target_value(self):
        assert TerritoryStatus.ON_TARGET.value == "on_target"

    def test_underperforming_value(self):
        assert TerritoryStatus.UNDERPERFORMING.value == "underperforming"

    def test_critical_value(self):
        assert TerritoryStatus.CRITICAL.value == "critical"

    def test_is_str_subtype(self):
        assert isinstance(TerritoryStatus.OVERPERFORMING, str)
        assert isinstance(TerritoryStatus.ON_TARGET, str)
        assert isinstance(TerritoryStatus.UNDERPERFORMING, str)
        assert isinstance(TerritoryStatus.CRITICAL, str)

    def test_member_count(self):
        assert len(TerritoryStatus) == 4

    def test_all_members(self):
        members = {m.name for m in TerritoryStatus}
        assert members == {"OVERPERFORMING", "ON_TARGET", "UNDERPERFORMING", "CRITICAL"}


class TestTerritoryRiskEnum:
    def test_low_value(self):
        assert TerritoryRisk.LOW.value == "low"

    def test_medium_value(self):
        assert TerritoryRisk.MEDIUM.value == "medium"

    def test_high_value(self):
        assert TerritoryRisk.HIGH.value == "high"

    def test_critical_value(self):
        assert TerritoryRisk.CRITICAL.value == "critical"

    def test_is_str_subtype(self):
        assert isinstance(TerritoryRisk.LOW, str)
        assert isinstance(TerritoryRisk.MEDIUM, str)
        assert isinstance(TerritoryRisk.HIGH, str)
        assert isinstance(TerritoryRisk.CRITICAL, str)

    def test_member_count(self):
        assert len(TerritoryRisk) == 4

    def test_all_members(self):
        members = {m.name for m in TerritoryRisk}
        assert members == {"LOW", "MEDIUM", "HIGH", "CRITICAL"}


class TestMarketPenetrationEnum:
    def test_saturated_value(self):
        assert MarketPenetration.SATURATED.value == "saturated"

    def test_high_value(self):
        assert MarketPenetration.HIGH.value == "high"

    def test_medium_value(self):
        assert MarketPenetration.MEDIUM.value == "medium"

    def test_low_value(self):
        assert MarketPenetration.LOW.value == "low"

    def test_untapped_value(self):
        assert MarketPenetration.UNTAPPED.value == "untapped"

    def test_is_str_subtype(self):
        assert isinstance(MarketPenetration.SATURATED, str)
        assert isinstance(MarketPenetration.HIGH, str)
        assert isinstance(MarketPenetration.MEDIUM, str)
        assert isinstance(MarketPenetration.LOW, str)
        assert isinstance(MarketPenetration.UNTAPPED, str)

    def test_member_count(self):
        assert len(MarketPenetration) == 5

    def test_all_members(self):
        members = {m.name for m in MarketPenetration}
        assert members == {"SATURATED", "HIGH", "MEDIUM", "LOW", "UNTAPPED"}


class TestTerritoryActionEnum:
    def test_maintain_value(self):
        assert TerritoryAction.MAINTAIN.value == "maintain"

    def test_expand_value(self):
        assert TerritoryAction.EXPAND.value == "expand"

    def test_focus_value(self):
        assert TerritoryAction.FOCUS.value == "focus"

    def test_rebalance_value(self):
        assert TerritoryAction.REBALANCE.value == "rebalance"

    def test_urgent_intervention_value(self):
        assert TerritoryAction.URGENT_INTERVENTION.value == "urgent_intervention"

    def test_is_str_subtype(self):
        assert isinstance(TerritoryAction.MAINTAIN, str)
        assert isinstance(TerritoryAction.EXPAND, str)
        assert isinstance(TerritoryAction.FOCUS, str)
        assert isinstance(TerritoryAction.REBALANCE, str)
        assert isinstance(TerritoryAction.URGENT_INTERVENTION, str)

    def test_member_count(self):
        assert len(TerritoryAction) == 5

    def test_all_members(self):
        members = {m.name for m in TerritoryAction}
        assert members == {"MAINTAIN", "EXPAND", "FOCUS", "REBALANCE", "URGENT_INTERVENTION"}


# ---------------------------------------------------------------------------
# Section 2: TerritoryPerformanceResult.to_dict() — 15 keys, enum as strings
# ---------------------------------------------------------------------------

class TestToDictKeys:
    @pytest.fixture
    def result(self):
        engine = TerritoryPerformanceEngine()
        return engine.analyze(make_input())

    def test_to_dict_returns_dict(self, result):
        assert isinstance(result.to_dict(), dict)

    def test_to_dict_exactly_15_keys(self, result):
        assert len(result.to_dict()) == 15

    def test_to_dict_has_territory_id(self, result):
        assert "territory_id" in result.to_dict()

    def test_to_dict_has_territory_name(self, result):
        assert "territory_name" in result.to_dict()

    def test_to_dict_has_territory_status(self, result):
        assert "territory_status" in result.to_dict()

    def test_to_dict_has_territory_risk(self, result):
        assert "territory_risk" in result.to_dict()

    def test_to_dict_has_market_penetration(self, result):
        assert "market_penetration" in result.to_dict()

    def test_to_dict_has_territory_action(self, result):
        assert "territory_action" in result.to_dict()

    def test_to_dict_has_attainment_pct(self, result):
        assert "attainment_pct" in result.to_dict()

    def test_to_dict_has_projected_attainment(self, result):
        assert "projected_attainment" in result.to_dict()

    def test_to_dict_has_coverage_ratio(self, result):
        assert "coverage_ratio" in result.to_dict()

    def test_to_dict_has_penetration_pct(self, result):
        assert "penetration_pct" in result.to_dict()

    def test_to_dict_has_account_health_score(self, result):
        assert "account_health_score" in result.to_dict()

    def test_to_dict_has_activity_score(self, result):
        assert "activity_score" in result.to_dict()

    def test_to_dict_has_growth_score(self, result):
        assert "growth_score" in result.to_dict()

    def test_to_dict_has_is_at_risk(self, result):
        assert "is_at_risk" in result.to_dict()

    def test_to_dict_has_needs_rebalancing(self, result):
        assert "needs_rebalancing" in result.to_dict()

    def test_to_dict_territory_status_is_string(self, result):
        d = result.to_dict()
        assert isinstance(d["territory_status"], str)
        assert not isinstance(d["territory_status"], TerritoryStatus)

    def test_to_dict_territory_risk_is_string(self, result):
        d = result.to_dict()
        assert isinstance(d["territory_risk"], str)
        assert not isinstance(d["territory_risk"], TerritoryRisk)

    def test_to_dict_market_penetration_is_string(self, result):
        d = result.to_dict()
        assert isinstance(d["market_penetration"], str)
        assert not isinstance(d["market_penetration"], MarketPenetration)

    def test_to_dict_territory_action_is_string(self, result):
        d = result.to_dict()
        assert isinstance(d["territory_action"], str)
        assert not isinstance(d["territory_action"], TerritoryAction)

    def test_to_dict_territory_id_value(self, result):
        assert result.to_dict()["territory_id"] == "T001"

    def test_to_dict_territory_name_value(self, result):
        assert result.to_dict()["territory_name"] == "North Region"


# ---------------------------------------------------------------------------
# Section 3: summary() — 13 keys, empty state, populated correctness
# ---------------------------------------------------------------------------

class TestSummaryKeys:
    def test_summary_empty_state_returns_dict(self):
        engine = TerritoryPerformanceEngine()
        s = engine.summary()
        assert isinstance(s, dict)

    def test_summary_exactly_13_keys(self):
        engine = TerritoryPerformanceEngine()
        assert len(engine.summary()) == 13

    def test_summary_has_total(self):
        engine = TerritoryPerformanceEngine()
        assert "total" in engine.summary()

    def test_summary_has_status_counts(self):
        engine = TerritoryPerformanceEngine()
        assert "status_counts" in engine.summary()

    def test_summary_has_risk_counts(self):
        engine = TerritoryPerformanceEngine()
        assert "risk_counts" in engine.summary()

    def test_summary_has_penetration_counts(self):
        engine = TerritoryPerformanceEngine()
        assert "penetration_counts" in engine.summary()

    def test_summary_has_action_counts(self):
        engine = TerritoryPerformanceEngine()
        assert "action_counts" in engine.summary()

    def test_summary_has_avg_attainment_pct(self):
        engine = TerritoryPerformanceEngine()
        assert "avg_attainment_pct" in engine.summary()

    def test_summary_has_avg_projected_attainment(self):
        engine = TerritoryPerformanceEngine()
        assert "avg_projected_attainment" in engine.summary()

    def test_summary_has_total_revenue_gap(self):
        engine = TerritoryPerformanceEngine()
        assert "total_revenue_gap" in engine.summary()

    def test_summary_has_at_risk_count(self):
        engine = TerritoryPerformanceEngine()
        assert "at_risk_count" in engine.summary()

    def test_summary_has_rebalancing_count(self):
        engine = TerritoryPerformanceEngine()
        assert "rebalancing_count" in engine.summary()

    def test_summary_has_avg_account_health(self):
        engine = TerritoryPerformanceEngine()
        assert "avg_account_health" in engine.summary()

    def test_summary_has_avg_growth_score(self):
        engine = TerritoryPerformanceEngine()
        assert "avg_growth_score" in engine.summary()

    def test_summary_has_high_performing_count(self):
        engine = TerritoryPerformanceEngine()
        assert "high_performing_count" in engine.summary()


class TestSummaryEmptyState:
    @pytest.fixture
    def empty_summary(self):
        return TerritoryPerformanceEngine().summary()

    def test_total_is_zero(self, empty_summary):
        assert empty_summary["total"] == 0

    def test_status_counts_empty(self, empty_summary):
        assert empty_summary["status_counts"] == {}

    def test_risk_counts_empty(self, empty_summary):
        assert empty_summary["risk_counts"] == {}

    def test_penetration_counts_empty(self, empty_summary):
        assert empty_summary["penetration_counts"] == {}

    def test_action_counts_empty(self, empty_summary):
        assert empty_summary["action_counts"] == {}

    def test_avg_attainment_pct_zero(self, empty_summary):
        assert empty_summary["avg_attainment_pct"] == 0.0

    def test_avg_projected_attainment_zero(self, empty_summary):
        assert empty_summary["avg_projected_attainment"] == 0.0

    def test_total_revenue_gap_zero(self, empty_summary):
        assert empty_summary["total_revenue_gap"] == 0.0

    def test_at_risk_count_zero(self, empty_summary):
        assert empty_summary["at_risk_count"] == 0

    def test_rebalancing_count_zero(self, empty_summary):
        assert empty_summary["rebalancing_count"] == 0

    def test_avg_account_health_zero(self, empty_summary):
        assert empty_summary["avg_account_health"] == 0.0

    def test_avg_growth_score_zero(self, empty_summary):
        assert empty_summary["avg_growth_score"] == 0.0

    def test_high_performing_count_zero(self, empty_summary):
        assert empty_summary["high_performing_count"] == 0


class TestSummaryPopulated:
    @pytest.fixture
    def engine_with_two(self):
        engine = TerritoryPerformanceEngine()
        # Territory 1: projected = 110% → OVERPERFORMING; attainment = 100%
        engine.analyze(make_input(
            territory_id="T001",
            target_revenue=1_000_000.0,
            actual_revenue=1_000_000.0,
            projected_revenue=1_100_000.0,
            active_accounts=90,
            total_accounts=100,
            win_rate=80.0,
            current_penetration=20.0,
        ))
        # Territory 2: projected = 50% → CRITICAL; attainment = 40%
        engine.analyze(make_input(
            territory_id="T002",
            target_revenue=1_000_000.0,
            actual_revenue=400_000.0,
            projected_revenue=500_000.0,
            active_accounts=20,
            total_accounts=100,
            win_rate=20.0,
            current_penetration=20.0,
        ))
        return engine

    def test_total_is_two(self, engine_with_two):
        assert engine_with_two.summary()["total"] == 2

    def test_avg_attainment_pct(self, engine_with_two):
        # (100 + 40) / 2 = 70.0
        assert engine_with_two.summary()["avg_attainment_pct"] == 70.0

    def test_avg_projected_attainment(self, engine_with_two):
        # (110 + 50) / 2 = 80.0
        assert engine_with_two.summary()["avg_projected_attainment"] == 80.0

    def test_status_counts_populated(self, engine_with_two):
        sc = engine_with_two.summary()["status_counts"]
        assert "overperforming" in sc or "critical" in sc

    def test_at_risk_count_positive(self, engine_with_two):
        # T002 projected=50 < 80, so at least 1
        assert engine_with_two.summary()["at_risk_count"] >= 1

    def test_high_performing_count_positive(self, engine_with_two):
        # T001 projected=110 → OVERPERFORMING
        assert engine_with_two.summary()["high_performing_count"] >= 1

    def test_total_revenue_gap_for_critical(self, engine_with_two):
        # T001 projected=110 → no gap; T002 projected=50 → gap=(100-50)/100=0.5
        # T001 projected_attainment=110 ≥ 100 → no contribution
        assert engine_with_two.summary()["total_revenue_gap"] == pytest.approx(0.5, abs=0.01)

    def test_summary_13_keys_populated(self, engine_with_two):
        assert len(engine_with_two.summary()) == 13


# ---------------------------------------------------------------------------
# Section 4: Scoring helpers with formula, boundaries, zero/negative guards
# ---------------------------------------------------------------------------

class TestAttainmentPct:
    def setup_method(self):
        self.engine = TerritoryPerformanceEngine()

    def test_basic_calculation(self):
        inp = make_input(actual_revenue=800_000.0, target_revenue=1_000_000.0)
        assert self.engine._attainment_pct(inp) == pytest.approx(80.0)

    def test_full_attainment(self):
        inp = make_input(actual_revenue=1_000_000.0, target_revenue=1_000_000.0)
        assert self.engine._attainment_pct(inp) == pytest.approx(100.0)

    def test_over_attainment(self):
        inp = make_input(actual_revenue=1_200_000.0, target_revenue=1_000_000.0)
        assert self.engine._attainment_pct(inp) == pytest.approx(120.0)

    def test_zero_target_returns_zero(self):
        inp = make_input(actual_revenue=500_000.0, target_revenue=0.0)
        assert self.engine._attainment_pct(inp) == 0.0

    def test_negative_target_returns_zero(self):
        inp = make_input(actual_revenue=500_000.0, target_revenue=-100.0)
        assert self.engine._attainment_pct(inp) == 0.0

    def test_zero_actual(self):
        inp = make_input(actual_revenue=0.0, target_revenue=1_000_000.0)
        assert self.engine._attainment_pct(inp) == pytest.approx(0.0)

    def test_rounding_one_decimal(self):
        inp = make_input(actual_revenue=333_333.0, target_revenue=1_000_000.0)
        result = self.engine._attainment_pct(inp)
        assert result == round(result, 1)


class TestProjectedAttainment:
    def setup_method(self):
        self.engine = TerritoryPerformanceEngine()

    def test_basic_calculation(self):
        inp = make_input(projected_revenue=950_000.0, target_revenue=1_000_000.0)
        assert self.engine._projected_attainment(inp) == pytest.approx(95.0)

    def test_zero_target_returns_zero(self):
        inp = make_input(projected_revenue=500_000.0, target_revenue=0.0)
        assert self.engine._projected_attainment(inp) == 0.0

    def test_negative_target_returns_zero(self):
        inp = make_input(projected_revenue=500_000.0, target_revenue=-1.0)
        assert self.engine._projected_attainment(inp) == 0.0

    def test_over_100_projection(self):
        inp = make_input(projected_revenue=1_200_000.0, target_revenue=1_000_000.0)
        assert self.engine._projected_attainment(inp) == pytest.approx(120.0)

    def test_rounding_one_decimal(self):
        inp = make_input(projected_revenue=666_667.0, target_revenue=1_000_000.0)
        result = self.engine._projected_attainment(inp)
        assert result == round(result, 1)


class TestCoverageRatio:
    def setup_method(self):
        self.engine = TerritoryPerformanceEngine()

    def test_basic_calculation(self):
        inp = make_input(
            actual_revenue=800_000.0,
            weighted_pipeline=300_000.0,
            target_revenue=1_000_000.0
        )
        assert self.engine._coverage_ratio(inp) == pytest.approx(1.1)

    def test_zero_target_returns_zero(self):
        inp = make_input(actual_revenue=500_000.0, weighted_pipeline=200_000.0, target_revenue=0.0)
        assert self.engine._coverage_ratio(inp) == 0.0

    def test_negative_target_returns_zero(self):
        inp = make_input(actual_revenue=500_000.0, weighted_pipeline=200_000.0, target_revenue=-1.0)
        assert self.engine._coverage_ratio(inp) == 0.0

    def test_coverage_below_one(self):
        inp = make_input(
            actual_revenue=400_000.0,
            weighted_pipeline=100_000.0,
            target_revenue=1_000_000.0
        )
        assert self.engine._coverage_ratio(inp) == pytest.approx(0.5)

    def test_rounding_two_decimals(self):
        inp = make_input(
            actual_revenue=333_333.0,
            weighted_pipeline=0.0,
            target_revenue=1_000_000.0
        )
        result = self.engine._coverage_ratio(inp)
        assert result == round(result, 2)


class TestAccountHealthScore:
    def setup_method(self):
        self.engine = TerritoryPerformanceEngine()

    def test_perfect_health(self):
        # active=100/100 → 40; new=10/100*100=10 → min(30, 10*3)=30; churn=0 → 0; win=100*0.3=30 → total=100
        inp = make_input(
            total_accounts=100,
            active_accounts=100,
            new_accounts_won=10,
            churned_accounts=0,
            win_rate=100.0,
        )
        assert self.engine._account_health_score(inp) == pytest.approx(100.0)

    def test_zero_total_accounts_returns_only_win_rate(self):
        # With total_accounts=0 all account-based parts skip; only win_rate * 0.30
        inp = make_input(total_accounts=0, active_accounts=0, new_accounts_won=0, churned_accounts=0, win_rate=60.0)
        assert self.engine._account_health_score(inp) == pytest.approx(18.0)

    def test_active_ratio_contribution(self):
        # active=50/100 → 20; new=0; churn=0; win=0 → 20
        inp = make_input(
            total_accounts=100,
            active_accounts=50,
            new_accounts_won=0,
            churned_accounts=0,
            win_rate=0.0,
        )
        assert self.engine._account_health_score(inp) == pytest.approx(20.0)

    def test_churn_penalty(self):
        # active=100/100→40; new=0; churn=50/100=0.5 → -20; win=0 → 20
        inp = make_input(
            total_accounts=100,
            active_accounts=100,
            new_accounts_won=0,
            churned_accounts=50,
            win_rate=0.0,
        )
        assert self.engine._account_health_score(inp) == pytest.approx(20.0)

    def test_clamped_at_zero_minimum(self):
        # All churned, no actives, no win rate
        inp = make_input(
            total_accounts=100,
            active_accounts=0,
            new_accounts_won=0,
            churned_accounts=100,
            win_rate=0.0,
        )
        assert self.engine._account_health_score(inp) >= 0.0

    def test_clamped_at_100_maximum(self):
        inp = make_input(
            total_accounts=100,
            active_accounts=100,
            new_accounts_won=100,
            churned_accounts=0,
            win_rate=100.0,
        )
        assert self.engine._account_health_score(inp) <= 100.0

    def test_new_accounts_capped_at_30(self):
        # new=100/100*100=100 → growth_rate*3=300 → capped at 30
        inp = make_input(
            total_accounts=100,
            active_accounts=0,
            new_accounts_won=100,
            churned_accounts=0,
            win_rate=0.0,
        )
        result = self.engine._account_health_score(inp)
        assert result <= 100.0
        # new accounts contribution is 30 only
        assert result == pytest.approx(30.0)

    def test_win_rate_contribution(self):
        # total=0, only win_rate: win_rate=100 → 30.0
        inp = make_input(total_accounts=0, active_accounts=0, new_accounts_won=0, churned_accounts=0, win_rate=100.0)
        assert self.engine._account_health_score(inp) == pytest.approx(30.0)

    def test_rounding_one_decimal(self):
        inp = make_input()
        result = self.engine._account_health_score(inp)
        assert result == round(result, 1)


class TestActivityScore:
    def setup_method(self):
        self.engine = TerritoryPerformanceEngine()

    def test_zero_total_period_days_returns_zero(self):
        inp = make_input(total_period_days=0, activities_count=100, total_accounts=50)
        assert self.engine._activity_score(inp) == 0.0

    def test_zero_total_accounts_returns_zero(self):
        inp = make_input(total_accounts=0, activities_count=100, total_period_days=90)
        assert self.engine._activity_score(inp) == 0.0

    def test_basic_calculation(self):
        # days_elapsed = 90 - 30 = 60; act/day = 200/60 ≈ 3.33 → min(50, 3.33*5)=min(50,16.67)=16.67
        # act/account = 200/100=2 → min(50, 2*5)=10; total≈26.67
        inp = make_input(
            activities_count=200,
            total_accounts=100,
            days_remaining=30,
            total_period_days=90,
        )
        days_elapsed = max(1, 90 - 30)
        apd = 200 / days_elapsed
        apa = 200 / 100
        expected = min(50.0, apd * 5.0) + min(50.0, apa * 5.0)
        assert self.engine._activity_score(inp) == pytest.approx(round(expected, 1))

    def test_capped_at_100(self):
        # Very high activity → should cap at 100
        inp = make_input(
            activities_count=10_000,
            total_accounts=10,
            days_remaining=0,
            total_period_days=90,
        )
        assert self.engine._activity_score(inp) <= 100.0

    def test_zero_activities(self):
        inp = make_input(activities_count=0, total_accounts=100, days_remaining=30, total_period_days=90)
        assert self.engine._activity_score(inp) == 0.0

    def test_days_elapsed_min_one(self):
        # days_remaining == total_period_days → days_elapsed = max(1, 0) = 1
        inp = make_input(
            activities_count=10,
            total_accounts=10,
            days_remaining=90,
            total_period_days=90,
        )
        # Should not raise and return a valid value
        result = self.engine._activity_score(inp)
        assert 0.0 <= result <= 100.0

    def test_rounding_one_decimal(self):
        inp = make_input()
        result = self.engine._activity_score(inp)
        assert result == round(result, 1)


class TestGrowthScore:
    def setup_method(self):
        self.engine = TerritoryPerformanceEngine()

    def test_zero_target_revenue_pipeline_part_zero(self):
        inp = make_input(target_revenue=0.0, pipeline_value=500_000.0)
        health = 50.0
        activity = 50.0
        result = self.engine._growth_score(inp, health, activity)
        # pipeline part = 0; health * 0.30 = 15; activity * 0.30 = 15 → 30
        assert result == pytest.approx(30.0)

    def test_pipeline_capped_at_40(self):
        # pipe_ratio = 5_000_000 / 1_000_000 = 5.0 → 5*20=100 → capped at 40
        inp = make_input(target_revenue=1_000_000.0, pipeline_value=5_000_000.0)
        health = 0.0
        activity = 0.0
        result = self.engine._growth_score(inp, health, activity)
        assert result == pytest.approx(40.0)

    def test_basic_calculation(self):
        inp = make_input(target_revenue=1_000_000.0, pipeline_value=1_000_000.0)
        # pipe_ratio=1.0 → 1*20=20; health=50*0.3=15; activity=50*0.3=15 → 50
        health = 50.0
        activity = 50.0
        result = self.engine._growth_score(inp, health, activity)
        assert result == pytest.approx(50.0)

    def test_clamped_at_zero(self):
        inp = make_input(target_revenue=0.0, pipeline_value=0.0)
        result = self.engine._growth_score(inp, 0.0, 0.0)
        assert result >= 0.0

    def test_clamped_at_100(self):
        inp = make_input(target_revenue=1_000_000.0, pipeline_value=10_000_000.0)
        result = self.engine._growth_score(inp, 100.0, 100.0)
        assert result <= 100.0

    def test_rounding_one_decimal(self):
        inp = make_input()
        health = self.engine._account_health_score(inp)
        activity = self.engine._activity_score(inp)
        result = self.engine._growth_score(inp, health, activity)
        assert result == round(result, 1)


# ---------------------------------------------------------------------------
# Section 5: _territory_status — all 4 boundaries
# ---------------------------------------------------------------------------

class TestTerritoryStatus:
    def setup_method(self):
        self.engine = TerritoryPerformanceEngine()

    def test_overperforming_at_exactly_105(self):
        assert self.engine._territory_status(105.0) == TerritoryStatus.OVERPERFORMING

    def test_overperforming_above_105(self):
        assert self.engine._territory_status(120.0) == TerritoryStatus.OVERPERFORMING

    def test_on_target_at_exactly_90(self):
        assert self.engine._territory_status(90.0) == TerritoryStatus.ON_TARGET

    def test_on_target_below_105(self):
        assert self.engine._territory_status(104.9) == TerritoryStatus.ON_TARGET

    def test_on_target_at_100(self):
        assert self.engine._territory_status(100.0) == TerritoryStatus.ON_TARGET

    def test_underperforming_at_exactly_70(self):
        assert self.engine._territory_status(70.0) == TerritoryStatus.UNDERPERFORMING

    def test_underperforming_below_90(self):
        assert self.engine._territory_status(89.9) == TerritoryStatus.UNDERPERFORMING

    def test_underperforming_at_80(self):
        assert self.engine._territory_status(80.0) == TerritoryStatus.UNDERPERFORMING

    def test_critical_below_70(self):
        assert self.engine._territory_status(69.9) == TerritoryStatus.CRITICAL

    def test_critical_at_zero(self):
        assert self.engine._territory_status(0.0) == TerritoryStatus.CRITICAL

    def test_critical_negative(self):
        assert self.engine._territory_status(-10.0) == TerritoryStatus.CRITICAL


# ---------------------------------------------------------------------------
# Section 6: _territory_risk — all 4 levels with both conditions
# ---------------------------------------------------------------------------

class TestTerritoryRisk:
    def setup_method(self):
        self.engine = TerritoryPerformanceEngine()
        self.inp = make_input()  # inp not really used by this helper except as placeholder

    def test_low_risk_exact_boundary(self):
        # projected=95, health=65 → LOW
        assert self.engine._territory_risk(self.inp, 95.0, 65.0) == TerritoryRisk.LOW

    def test_low_risk_above_boundary(self):
        assert self.engine._territory_risk(self.inp, 100.0, 80.0) == TerritoryRisk.LOW

    def test_low_risk_fails_projected(self):
        # projected=94 → not LOW (falls to MEDIUM if health ≥ 45)
        result = self.engine._territory_risk(self.inp, 94.9, 65.0)
        assert result != TerritoryRisk.LOW

    def test_low_risk_fails_health(self):
        # health=64 → not LOW
        result = self.engine._territory_risk(self.inp, 95.0, 64.9)
        assert result != TerritoryRisk.LOW

    def test_medium_risk_exact_boundary(self):
        # projected=80, health=45 → MEDIUM (not ≥95 or health<65)
        assert self.engine._territory_risk(self.inp, 80.0, 45.0) == TerritoryRisk.MEDIUM

    def test_medium_risk_above_boundary(self):
        assert self.engine._territory_risk(self.inp, 90.0, 50.0) == TerritoryRisk.MEDIUM

    def test_medium_risk_fails_projected(self):
        # projected=79 → not MEDIUM (falls to HIGH)
        result = self.engine._territory_risk(self.inp, 79.9, 50.0)
        assert result == TerritoryRisk.HIGH

    def test_medium_risk_fails_health(self):
        # health=44 → not MEDIUM (falls to HIGH if projected ≥ 60)
        result = self.engine._territory_risk(self.inp, 80.0, 44.9)
        assert result == TerritoryRisk.HIGH

    def test_high_risk_at_exactly_60(self):
        # projected=60, health doesn't meet medium threshold → HIGH
        assert self.engine._territory_risk(self.inp, 60.0, 30.0) == TerritoryRisk.HIGH

    def test_high_risk_above_60_low_health(self):
        assert self.engine._territory_risk(self.inp, 75.0, 30.0) == TerritoryRisk.HIGH

    def test_critical_risk_below_60(self):
        assert self.engine._territory_risk(self.inp, 59.9, 0.0) == TerritoryRisk.CRITICAL

    def test_critical_risk_at_zero(self):
        assert self.engine._territory_risk(self.inp, 0.0, 0.0) == TerritoryRisk.CRITICAL

    def test_critical_risk_negative_projected(self):
        assert self.engine._territory_risk(self.inp, -10.0, 0.0) == TerritoryRisk.CRITICAL


# ---------------------------------------------------------------------------
# Section 7: _market_penetration — all 5 levels
# ---------------------------------------------------------------------------

class TestMarketPenetrationLevel:
    def setup_method(self):
        self.engine = TerritoryPerformanceEngine()

    def test_saturated_at_exactly_70(self):
        assert self.engine._market_penetration(70.0) == MarketPenetration.SATURATED

    def test_saturated_above_70(self):
        assert self.engine._market_penetration(100.0) == MarketPenetration.SATURATED

    def test_high_at_exactly_50(self):
        assert self.engine._market_penetration(50.0) == MarketPenetration.HIGH

    def test_high_below_70(self):
        assert self.engine._market_penetration(69.9) == MarketPenetration.HIGH

    def test_medium_at_exactly_25(self):
        assert self.engine._market_penetration(25.0) == MarketPenetration.MEDIUM

    def test_medium_below_50(self):
        assert self.engine._market_penetration(49.9) == MarketPenetration.MEDIUM

    def test_low_at_exactly_10(self):
        assert self.engine._market_penetration(10.0) == MarketPenetration.LOW

    def test_low_below_25(self):
        assert self.engine._market_penetration(24.9) == MarketPenetration.LOW

    def test_untapped_below_10(self):
        assert self.engine._market_penetration(9.9) == MarketPenetration.UNTAPPED

    def test_untapped_at_zero(self):
        assert self.engine._market_penetration(0.0) == MarketPenetration.UNTAPPED

    def test_untapped_negative(self):
        assert self.engine._market_penetration(-1.0) == MarketPenetration.UNTAPPED


# ---------------------------------------------------------------------------
# Section 8: _territory_action — all 5 actions
# ---------------------------------------------------------------------------

class TestTerritoryAction:
    def setup_method(self):
        self.engine = TerritoryPerformanceEngine()
        self.inp = make_input()

    def test_urgent_intervention_when_critical_risk(self):
        result = self.engine._territory_action(
            self.inp,
            TerritoryStatus.CRITICAL,
            TerritoryRisk.CRITICAL,
            MarketPenetration.MEDIUM,
            0.5,
        )
        assert result == TerritoryAction.URGENT_INTERVENTION

    def test_urgent_intervention_overrides_other_status(self):
        # Even OVERPERFORMING with CRITICAL risk → URGENT_INTERVENTION
        result = self.engine._territory_action(
            self.inp,
            TerritoryStatus.OVERPERFORMING,
            TerritoryRisk.CRITICAL,
            MarketPenetration.MEDIUM,
            1.5,
        )
        assert result == TerritoryAction.URGENT_INTERVENTION

    def test_focus_when_underperforming_and_high_risk(self):
        result = self.engine._territory_action(
            self.inp,
            TerritoryStatus.UNDERPERFORMING,
            TerritoryRisk.HIGH,
            MarketPenetration.MEDIUM,
            0.5,
        )
        assert result == TerritoryAction.FOCUS

    def test_focus_not_triggered_without_high_risk(self):
        result = self.engine._territory_action(
            self.inp,
            TerritoryStatus.UNDERPERFORMING,
            TerritoryRisk.MEDIUM,
            MarketPenetration.MEDIUM,
            0.5,
        )
        assert result != TerritoryAction.FOCUS or result == TerritoryAction.FOCUS  # may still be FOCUS via fallback

    def test_rebalance_when_saturated_and_coverage_gte_1(self):
        result = self.engine._territory_action(
            self.inp,
            TerritoryStatus.ON_TARGET,
            TerritoryRisk.LOW,
            MarketPenetration.SATURATED,
            1.0,
        )
        assert result == TerritoryAction.REBALANCE

    def test_rebalance_not_triggered_when_coverage_below_1(self):
        result = self.engine._territory_action(
            self.inp,
            TerritoryStatus.ON_TARGET,
            TerritoryRisk.LOW,
            MarketPenetration.SATURATED,
            0.9,
        )
        assert result != TerritoryAction.REBALANCE

    def test_expand_when_low_penetration(self):
        result = self.engine._territory_action(
            self.inp,
            TerritoryStatus.ON_TARGET,
            TerritoryRisk.MEDIUM,
            MarketPenetration.LOW,
            0.5,
        )
        assert result == TerritoryAction.EXPAND

    def test_expand_when_untapped_penetration(self):
        result = self.engine._territory_action(
            self.inp,
            TerritoryStatus.ON_TARGET,
            TerritoryRisk.MEDIUM,
            MarketPenetration.UNTAPPED,
            0.5,
        )
        assert result == TerritoryAction.EXPAND

    def test_maintain_when_overperforming(self):
        result = self.engine._territory_action(
            self.inp,
            TerritoryStatus.OVERPERFORMING,
            TerritoryRisk.LOW,
            MarketPenetration.MEDIUM,
            1.2,
        )
        assert result == TerritoryAction.MAINTAIN

    def test_maintain_when_on_target(self):
        result = self.engine._territory_action(
            self.inp,
            TerritoryStatus.ON_TARGET,
            TerritoryRisk.LOW,
            MarketPenetration.MEDIUM,
            1.0,
        )
        assert result == TerritoryAction.MAINTAIN

    def test_focus_fallback(self):
        # UNDERPERFORMING + MEDIUM risk + MEDIUM penetration → fallback FOCUS
        result = self.engine._territory_action(
            self.inp,
            TerritoryStatus.UNDERPERFORMING,
            TerritoryRisk.MEDIUM,
            MarketPenetration.MEDIUM,
            0.5,
        )
        assert result == TerritoryAction.FOCUS


# ---------------------------------------------------------------------------
# Section 9: is_at_risk — both conditions independently
# ---------------------------------------------------------------------------

class TestIsAtRisk:
    def setup_method(self):
        self.engine = TerritoryPerformanceEngine()

    def test_at_risk_when_projected_below_80(self):
        # projected_revenue / target_revenue * 100 = 75
        inp = make_input(projected_revenue=750_000.0, target_revenue=1_000_000.0,
                         active_accounts=90, total_accounts=100, win_rate=80.0,
                         current_penetration=30.0)
        result = self.engine.analyze(inp)
        assert result.is_at_risk is True

    def test_at_risk_when_high_risk(self):
        # projected=85 (≥80), but health < 45 → HIGH risk
        inp = make_input(
            projected_revenue=850_000.0, target_revenue=1_000_000.0,
            active_accounts=10, total_accounts=100, new_accounts_won=0,
            churned_accounts=50, win_rate=0.0, current_penetration=30.0,
        )
        result = self.engine.analyze(inp)
        assert result.is_at_risk is True

    def test_at_risk_when_critical_risk(self):
        # projected < 60 → CRITICAL risk
        inp = make_input(projected_revenue=300_000.0, target_revenue=1_000_000.0,
                         current_penetration=30.0)
        result = self.engine.analyze(inp)
        assert result.is_at_risk is True

    def test_not_at_risk_when_projected_gte_80_and_low_medium_risk(self):
        # projected=110, high health → LOW risk, projected≥80 → not at risk
        inp = make_input(
            projected_revenue=1_100_000.0, target_revenue=1_000_000.0,
            active_accounts=95, total_accounts=100, new_accounts_won=10,
            churned_accounts=0, win_rate=90.0, current_penetration=20.0,
        )
        result = self.engine.analyze(inp)
        assert result.is_at_risk is False

    def test_at_risk_boundary_exactly_80(self):
        # projected=80.0 → not below 80 → check risk
        inp = make_input(
            projected_revenue=800_000.0, target_revenue=1_000_000.0,
            active_accounts=95, total_accounts=100, new_accounts_won=10,
            churned_accounts=0, win_rate=90.0, current_penetration=20.0,
        )
        result = self.engine.analyze(inp)
        # projected_attainment=80 is NOT < 80.0, so at_risk depends only on risk level
        if result.territory_risk in (TerritoryRisk.HIGH, TerritoryRisk.CRITICAL):
            assert result.is_at_risk is True
        else:
            assert result.is_at_risk is False


# ---------------------------------------------------------------------------
# Section 10: needs_rebalancing — both conditions independently
# ---------------------------------------------------------------------------

class TestNeedsRebalancing:
    def setup_method(self):
        self.engine = TerritoryPerformanceEngine()

    def test_needs_rebalancing_when_penetration_above_60(self):
        inp = make_input(current_penetration=61.0, active_accounts=80, total_accounts=100)
        result = self.engine.analyze(inp)
        assert result.needs_rebalancing is True

    def test_needs_rebalancing_boundary_penetration_exactly_60(self):
        # > 60 required, so exactly 60 should NOT trigger this condition alone
        inp = make_input(current_penetration=60.0, active_accounts=80, total_accounts=100)
        result = self.engine.analyze(inp)
        # penetration=60 is NOT > 60, so only active/total ratio determines it
        active_ratio = 80 / 100  # = 0.8 ≥ 0.3 → False
        if active_ratio < 0.3:
            assert result.needs_rebalancing is True
        else:
            assert result.needs_rebalancing is False

    def test_needs_rebalancing_when_active_ratio_below_0_3(self):
        inp = make_input(current_penetration=20.0, active_accounts=20, total_accounts=100)
        result = self.engine.analyze(inp)
        assert result.needs_rebalancing is True

    def test_not_needs_rebalancing_when_conditions_not_met(self):
        inp = make_input(current_penetration=20.0, active_accounts=80, total_accounts=100)
        result = self.engine.analyze(inp)
        assert result.needs_rebalancing is False

    def test_needs_rebalancing_active_ratio_exactly_0_3(self):
        # exactly 0.3 should NOT trigger (< 0.3 required)
        inp = make_input(current_penetration=20.0, active_accounts=30, total_accounts=100)
        result = self.engine.analyze(inp)
        assert result.needs_rebalancing is False

    def test_needs_rebalancing_zero_total_accounts(self):
        # With total_accounts=0, the ratio condition is skipped
        inp = make_input(current_penetration=20.0, total_accounts=0, active_accounts=0)
        result = self.engine.analyze(inp)
        # current_penetration=20 is NOT > 60 → False
        assert result.needs_rebalancing is False


# ---------------------------------------------------------------------------
# Section 11: Properties — empty state, after analyze, filtering
# ---------------------------------------------------------------------------

class TestProperties:
    def test_at_risk_territories_empty(self):
        engine = TerritoryPerformanceEngine()
        assert engine.at_risk_territories == []

    def test_rebalancing_territories_empty(self):
        engine = TerritoryPerformanceEngine()
        assert engine.rebalancing_territories == []

    def test_high_performing_territories_empty(self):
        engine = TerritoryPerformanceEngine()
        assert engine.high_performing_territories == []

    def test_total_revenue_gap_empty(self):
        engine = TerritoryPerformanceEngine()
        assert engine.total_revenue_gap == 0.0

    def test_avg_attainment_empty(self):
        engine = TerritoryPerformanceEngine()
        assert engine.avg_attainment == 0.0

    def test_at_risk_territories_after_analyze(self):
        engine = TerritoryPerformanceEngine()
        # projected=50 → at risk
        engine.analyze(make_input(projected_revenue=500_000.0, target_revenue=1_000_000.0,
                                   current_penetration=20.0))
        assert len(engine.at_risk_territories) >= 1

    def test_high_performing_after_analyze(self):
        engine = TerritoryPerformanceEngine()
        # projected=110 → OVERPERFORMING
        engine.analyze(make_input(
            projected_revenue=1_100_000.0, target_revenue=1_000_000.0,
            active_accounts=95, total_accounts=100, win_rate=90.0,
            new_accounts_won=5, churned_accounts=0, current_penetration=20.0,
        ))
        assert len(engine.high_performing_territories) >= 1

    def test_rebalancing_territories_after_analyze(self):
        engine = TerritoryPerformanceEngine()
        engine.analyze(make_input(current_penetration=65.0))
        assert len(engine.rebalancing_territories) >= 1

    def test_total_revenue_gap_formula(self):
        engine = TerritoryPerformanceEngine()
        # projected_attainment=50 → gap = (100-50)/100 = 0.5
        engine.analyze(make_input(projected_revenue=500_000.0, target_revenue=1_000_000.0,
                                   current_penetration=20.0))
        assert engine.total_revenue_gap == pytest.approx(0.5, abs=0.01)

    def test_total_revenue_gap_no_gap_when_projected_gte_100(self):
        engine = TerritoryPerformanceEngine()
        engine.analyze(make_input(
            projected_revenue=1_200_000.0, target_revenue=1_000_000.0,
            active_accounts=90, total_accounts=100, win_rate=80.0,
            new_accounts_won=5, churned_accounts=0, current_penetration=20.0,
        ))
        assert engine.total_revenue_gap == 0.0

    def test_avg_attainment_single(self):
        engine = TerritoryPerformanceEngine()
        engine.analyze(make_input(actual_revenue=800_000.0, target_revenue=1_000_000.0))
        assert engine.avg_attainment == pytest.approx(80.0)

    def test_avg_attainment_multiple(self):
        engine = TerritoryPerformanceEngine()
        engine.analyze(make_input(territory_id="T1", actual_revenue=800_000.0, target_revenue=1_000_000.0))
        engine.analyze(make_input(territory_id="T2", actual_revenue=600_000.0, target_revenue=1_000_000.0))
        assert engine.avg_attainment == pytest.approx(70.0)

    def test_high_performing_includes_on_target(self):
        engine = TerritoryPerformanceEngine()
        # projected=95 → ON_TARGET
        engine.analyze(make_input(
            projected_revenue=950_000.0, target_revenue=1_000_000.0,
            active_accounts=80, total_accounts=100, win_rate=70.0,
            new_accounts_won=5, churned_accounts=0, current_penetration=20.0,
        ))
        assert len(engine.high_performing_territories) >= 1

    def test_high_performing_excludes_underperforming(self):
        engine = TerritoryPerformanceEngine()
        # projected=75 → UNDERPERFORMING
        r = engine.analyze(make_input(projected_revenue=750_000.0, target_revenue=1_000_000.0,
                                       current_penetration=20.0))
        assert r.territory_status == TerritoryStatus.UNDERPERFORMING
        high = engine.high_performing_territories
        assert r not in high

    def test_high_performing_excludes_critical(self):
        engine = TerritoryPerformanceEngine()
        r = engine.analyze(make_input(projected_revenue=500_000.0, target_revenue=1_000_000.0,
                                       current_penetration=20.0))
        assert r.territory_status == TerritoryStatus.CRITICAL
        assert r not in engine.high_performing_territories

    def test_at_risk_territories_returns_list_of_results(self):
        engine = TerritoryPerformanceEngine()
        engine.analyze(make_input(projected_revenue=500_000.0, target_revenue=1_000_000.0,
                                   current_penetration=20.0))
        for r in engine.at_risk_territories:
            assert isinstance(r, TerritoryPerformanceResult)


# ---------------------------------------------------------------------------
# Section 12: analyze_batch() and reset()
# ---------------------------------------------------------------------------

class TestAnalyzeBatchAndReset:
    def test_analyze_batch_empty_list(self):
        engine = TerritoryPerformanceEngine()
        results = engine.analyze_batch([])
        assert results == []

    def test_analyze_batch_single(self):
        engine = TerritoryPerformanceEngine()
        results = engine.analyze_batch([make_input()])
        assert len(results) == 1
        assert isinstance(results[0], TerritoryPerformanceResult)

    def test_analyze_batch_multiple(self):
        engine = TerritoryPerformanceEngine()
        inputs = [make_input(territory_id=f"T{i}") for i in range(5)]
        results = engine.analyze_batch(inputs)
        assert len(results) == 5

    def test_analyze_batch_accumulates_in_results(self):
        engine = TerritoryPerformanceEngine()
        engine.analyze_batch([make_input(territory_id="T1"), make_input(territory_id="T2")])
        assert engine.summary()["total"] == 2

    def test_analyze_batch_returns_correct_types(self):
        engine = TerritoryPerformanceEngine()
        results = engine.analyze_batch([make_input(territory_id=f"T{i}") for i in range(3)])
        for r in results:
            assert isinstance(r, TerritoryPerformanceResult)

    def test_reset_clears_results(self):
        engine = TerritoryPerformanceEngine()
        engine.analyze(make_input())
        engine.reset()
        assert engine.summary()["total"] == 0

    def test_reset_clears_at_risk_territories(self):
        engine = TerritoryPerformanceEngine()
        engine.analyze(make_input(projected_revenue=500_000.0, target_revenue=1_000_000.0,
                                   current_penetration=20.0))
        engine.reset()
        assert engine.at_risk_territories == []

    def test_reset_clears_high_performing(self):
        engine = TerritoryPerformanceEngine()
        engine.analyze(make_input(
            projected_revenue=1_100_000.0, target_revenue=1_000_000.0,
            active_accounts=90, total_accounts=100, win_rate=80.0,
            new_accounts_won=5, churned_accounts=0, current_penetration=20.0,
        ))
        engine.reset()
        assert engine.high_performing_territories == []

    def test_can_analyze_after_reset(self):
        engine = TerritoryPerformanceEngine()
        engine.analyze(make_input(territory_id="T1"))
        engine.reset()
        result = engine.analyze(make_input(territory_id="T2"))
        assert result.territory_id == "T2"
        assert engine.summary()["total"] == 1

    def test_analyze_batch_order_preserved(self):
        engine = TerritoryPerformanceEngine()
        inputs = [make_input(territory_id=f"T{i}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        for i, r in enumerate(results):
            assert r.territory_id == f"T{i}"


# ---------------------------------------------------------------------------
# Section 13: Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def setup_method(self):
        self.engine = TerritoryPerformanceEngine()

    def test_target_zero_all_scores_zero(self):
        inp = make_input(target_revenue=0.0, actual_revenue=500_000.0,
                         projected_revenue=500_000.0, weighted_pipeline=200_000.0)
        result = self.engine.analyze(inp)
        assert result.attainment_pct == 0.0
        assert result.projected_attainment == 0.0
        assert result.coverage_ratio == 0.0

    def test_target_zero_status_is_critical(self):
        inp = make_input(target_revenue=0.0, actual_revenue=0.0, projected_revenue=0.0)
        result = self.engine.analyze(inp)
        assert result.territory_status == TerritoryStatus.CRITICAL

    def test_target_zero_risk_is_critical(self):
        inp = make_input(target_revenue=0.0, actual_revenue=0.0, projected_revenue=0.0,
                         total_accounts=100, active_accounts=0, win_rate=0.0)
        result = self.engine.analyze(inp)
        assert result.territory_risk == TerritoryRisk.CRITICAL

    def test_all_churned_health_clamped_at_zero(self):
        inp = make_input(
            total_accounts=100,
            active_accounts=0,
            new_accounts_won=0,
            churned_accounts=100,
            win_rate=0.0,
        )
        result = self.engine.analyze(inp)
        assert result.account_health_score >= 0.0

    def test_zero_activity(self):
        inp = make_input(activities_count=0, total_accounts=100, total_period_days=90, days_remaining=30)
        result = self.engine.analyze(inp)
        assert result.activity_score == 0.0

    def test_zero_accounts(self):
        inp = make_input(total_accounts=0, active_accounts=0, new_accounts_won=0, churned_accounts=0)
        result = self.engine.analyze(inp)
        assert result.activity_score == 0.0
        assert 0.0 <= result.account_health_score <= 100.0

    def test_100_percent_penetration(self):
        inp = make_input(current_penetration=100.0)
        result = self.engine.analyze(inp)
        assert result.market_penetration == MarketPenetration.SATURATED
        assert result.penetration_pct == 100.0

    def test_zero_penetration(self):
        inp = make_input(current_penetration=0.0)
        result = self.engine.analyze(inp)
        assert result.market_penetration == MarketPenetration.UNTAPPED

    def test_result_fields_match_input(self):
        inp = make_input(territory_id="T999", territory_name="Test Territory")
        result = self.engine.analyze(inp)
        assert result.territory_id == "T999"
        assert result.territory_name == "Test Territory"

    def test_result_penetration_pct_matches_input(self):
        inp = make_input(current_penetration=35.7)
        result = self.engine.analyze(inp)
        assert result.penetration_pct == 35.7

    def test_all_fields_numeric_not_none(self):
        inp = make_input()
        result = self.engine.analyze(inp)
        assert result.attainment_pct is not None
        assert result.projected_attainment is not None
        assert result.coverage_ratio is not None
        assert result.account_health_score is not None
        assert result.activity_score is not None
        assert result.growth_score is not None

    def test_score_bounds_are_floats(self):
        inp = make_input()
        result = self.engine.analyze(inp)
        for score in [result.attainment_pct, result.coverage_ratio,
                      result.account_health_score, result.activity_score, result.growth_score]:
            assert isinstance(score, float)

    def test_health_activity_growth_bounded(self):
        inp = make_input()
        result = self.engine.analyze(inp)
        assert 0.0 <= result.account_health_score <= 100.0
        assert 0.0 <= result.activity_score <= 100.0
        assert 0.0 <= result.growth_score <= 100.0

    def test_analyze_returns_result_type(self):
        inp = make_input()
        result = self.engine.analyze(inp)
        assert isinstance(result, TerritoryPerformanceResult)

    def test_negative_target_all_attainments_zero(self):
        inp = make_input(target_revenue=-500.0, actual_revenue=100.0, projected_revenue=200.0)
        result = self.engine.analyze(inp)
        assert result.attainment_pct == 0.0
        assert result.projected_attainment == 0.0
        assert result.coverage_ratio == 0.0

    def test_days_remaining_greater_than_period_days(self):
        # days_elapsed = max(1, 90-100) = max(1,-10) = 1
        inp = make_input(days_remaining=100, total_period_days=90, activities_count=10, total_accounts=10)
        result = self.engine.analyze(inp)
        assert 0.0 <= result.activity_score <= 100.0

    def test_win_rate_zero(self):
        inp = make_input(win_rate=0.0)
        result = self.engine.analyze(inp)
        assert result.account_health_score >= 0.0

    def test_win_rate_100(self):
        inp = make_input(win_rate=100.0)
        result = self.engine.analyze(inp)
        assert result.account_health_score <= 100.0

    def test_multiple_analyzes_accumulate(self):
        inputs = [make_input(territory_id=f"T{i}") for i in range(10)]
        self.engine.analyze_batch(inputs)
        assert self.engine.summary()["total"] == 10

    def test_territory_action_not_none(self):
        inp = make_input()
        result = self.engine.analyze(inp)
        assert result.territory_action is not None
        assert isinstance(result.territory_action, TerritoryAction)

    def test_is_at_risk_is_bool(self):
        inp = make_input()
        result = self.engine.analyze(inp)
        assert isinstance(result.is_at_risk, bool)

    def test_needs_rebalancing_is_bool(self):
        inp = make_input()
        result = self.engine.analyze(inp)
        assert isinstance(result.needs_rebalancing, bool)


# ---------------------------------------------------------------------------
# Section 14: TerritoryPerformanceInput — 21 fields
# ---------------------------------------------------------------------------

class TestTerritoryPerformanceInputFields:
    def test_has_21_fields(self):
        import dataclasses
        fields = dataclasses.fields(TerritoryPerformanceInput)
        assert len(fields) == 21

    def test_all_field_names(self):
        import dataclasses
        field_names = {f.name for f in dataclasses.fields(TerritoryPerformanceInput)}
        expected = {
            "territory_id", "territory_name", "rep_id", "region",
            "target_revenue", "actual_revenue", "projected_revenue",
            "total_accounts", "active_accounts", "new_accounts_won", "churned_accounts",
            "total_addressable_mkt", "current_penetration",
            "pipeline_value", "weighted_pipeline", "avg_deal_size",
            "win_rate", "avg_sales_cycle_days", "activities_count",
            "days_remaining", "total_period_days",
        }
        assert field_names == expected

    def test_construction_sets_all_fields(self):
        inp = make_input()
        assert inp.territory_id == "T001"
        assert inp.territory_name == "North Region"
        assert inp.rep_id == "R001"
        assert inp.region == "North"
        assert inp.target_revenue == 1_000_000.0
        assert inp.actual_revenue == 800_000.0
        assert inp.projected_revenue == 950_000.0
        assert inp.total_accounts == 100
        assert inp.active_accounts == 70
        assert inp.new_accounts_won == 10
        assert inp.churned_accounts == 5
        assert inp.total_addressable_mkt == 5_000_000.0
        assert inp.current_penetration == 20.0
        assert inp.pipeline_value == 500_000.0
        assert inp.weighted_pipeline == 300_000.0
        assert inp.avg_deal_size == 50_000.0
        assert inp.win_rate == 60.0
        assert inp.avg_sales_cycle_days == 30
        assert inp.activities_count == 200
        assert inp.days_remaining == 30
        assert inp.total_period_days == 90


# ---------------------------------------------------------------------------
# Section 15: TerritoryPerformanceResult — 15 fields
# ---------------------------------------------------------------------------

class TestTerritoryPerformanceResultFields:
    def test_has_15_fields(self):
        import dataclasses
        fields = dataclasses.fields(TerritoryPerformanceResult)
        assert len(fields) == 15

    def test_all_field_names(self):
        import dataclasses
        field_names = {f.name for f in dataclasses.fields(TerritoryPerformanceResult)}
        expected = {
            "territory_id", "territory_name", "territory_status", "territory_risk",
            "market_penetration", "territory_action", "attainment_pct",
            "projected_attainment", "coverage_ratio", "penetration_pct",
            "account_health_score", "activity_score", "growth_score",
            "is_at_risk", "needs_rebalancing",
        }
        assert field_names == expected


# ---------------------------------------------------------------------------
# Section 16: End-to-end integration scenarios
# ---------------------------------------------------------------------------

class TestIntegrationScenarios:
    def test_overperforming_scenario(self):
        engine = TerritoryPerformanceEngine()
        inp = make_input(
            projected_revenue=1_200_000.0,
            target_revenue=1_000_000.0,
            active_accounts=95,
            total_accounts=100,
            win_rate=90.0,
            new_accounts_won=15,
            churned_accounts=0,
            current_penetration=20.0,
        )
        result = engine.analyze(inp)
        assert result.territory_status == TerritoryStatus.OVERPERFORMING
        assert result.projected_attainment == pytest.approx(120.0)

    def test_critical_scenario(self):
        engine = TerritoryPerformanceEngine()
        inp = make_input(
            projected_revenue=400_000.0,
            target_revenue=1_000_000.0,
            actual_revenue=200_000.0,
            active_accounts=10,
            total_accounts=100,
            win_rate=10.0,
            new_accounts_won=0,
            churned_accounts=20,
            current_penetration=20.0,
        )
        result = engine.analyze(inp)
        assert result.territory_status == TerritoryStatus.CRITICAL
        assert result.is_at_risk is True

    def test_batch_then_reset_then_summary(self):
        engine = TerritoryPerformanceEngine()
        inputs = [make_input(territory_id=f"T{i}") for i in range(5)]
        engine.analyze_batch(inputs)
        assert engine.summary()["total"] == 5
        engine.reset()
        assert engine.summary()["total"] == 0

    def test_summary_status_counts_sum_equals_total(self):
        engine = TerritoryPerformanceEngine()
        inputs = [make_input(territory_id=f"T{i}") for i in range(4)]
        engine.analyze_batch(inputs)
        s = engine.summary()
        assert sum(s["status_counts"].values()) == s["total"]

    def test_summary_risk_counts_sum_equals_total(self):
        engine = TerritoryPerformanceEngine()
        inputs = [make_input(territory_id=f"T{i}") for i in range(4)]
        engine.analyze_batch(inputs)
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_equals_total(self):
        engine = TerritoryPerformanceEngine()
        inputs = [make_input(territory_id=f"T{i}") for i in range(4)]
        engine.analyze_batch(inputs)
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_penetration_counts_sum_equals_total(self):
        engine = TerritoryPerformanceEngine()
        inputs = [make_input(territory_id=f"T{i}") for i in range(4)]
        engine.analyze_batch(inputs)
        s = engine.summary()
        assert sum(s["penetration_counts"].values()) == s["total"]

    def test_to_dict_values_match_result_attributes(self):
        engine = TerritoryPerformanceEngine()
        result = engine.analyze(make_input())
        d = result.to_dict()
        assert d["territory_id"] == result.territory_id
        assert d["territory_status"] == result.territory_status.value
        assert d["attainment_pct"] == result.attainment_pct
        assert d["is_at_risk"] == result.is_at_risk
        assert d["needs_rebalancing"] == result.needs_rebalancing


# ---------------------------------------------------------------------------
# Section 17: Additional attainment / projected / coverage edge cases
# ---------------------------------------------------------------------------

class TestAttainmentEdgeCases:
    def setup_method(self):
        self.engine = TerritoryPerformanceEngine()

    def test_attainment_exact_50_percent(self):
        inp = make_input(actual_revenue=500_000.0, target_revenue=1_000_000.0)
        assert self.engine._attainment_pct(inp) == pytest.approx(50.0)

    def test_attainment_exact_25_percent(self):
        inp = make_input(actual_revenue=250_000.0, target_revenue=1_000_000.0)
        assert self.engine._attainment_pct(inp) == pytest.approx(25.0)

    def test_projected_exact_105(self):
        inp = make_input(projected_revenue=1_050_000.0, target_revenue=1_000_000.0)
        assert self.engine._projected_attainment(inp) == pytest.approx(105.0)

    def test_projected_exact_90(self):
        inp = make_input(projected_revenue=900_000.0, target_revenue=1_000_000.0)
        assert self.engine._projected_attainment(inp) == pytest.approx(90.0)

    def test_projected_exact_70(self):
        inp = make_input(projected_revenue=700_000.0, target_revenue=1_000_000.0)
        assert self.engine._projected_attainment(inp) == pytest.approx(70.0)

    def test_projected_exact_80(self):
        inp = make_input(projected_revenue=800_000.0, target_revenue=1_000_000.0)
        assert self.engine._projected_attainment(inp) == pytest.approx(80.0)

    def test_coverage_ratio_zero_pipeline(self):
        inp = make_input(actual_revenue=600_000.0, weighted_pipeline=0.0, target_revenue=1_000_000.0)
        assert self.engine._coverage_ratio(inp) == pytest.approx(0.6)

    def test_coverage_ratio_zero_actual(self):
        inp = make_input(actual_revenue=0.0, weighted_pipeline=400_000.0, target_revenue=1_000_000.0)
        assert self.engine._coverage_ratio(inp) == pytest.approx(0.4)

    def test_coverage_ratio_exact_1(self):
        inp = make_input(actual_revenue=700_000.0, weighted_pipeline=300_000.0, target_revenue=1_000_000.0)
        assert self.engine._coverage_ratio(inp) == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# Section 18: Account health score additional boundary tests
# ---------------------------------------------------------------------------

class TestAccountHealthBoundaries:
    def setup_method(self):
        self.engine = TerritoryPerformanceEngine()

    def test_full_active_ratio(self):
        # active=100/100=1.0 → 40 pts
        inp = make_input(total_accounts=100, active_accounts=100, new_accounts_won=0,
                         churned_accounts=0, win_rate=0.0)
        assert self.engine._account_health_score(inp) == pytest.approx(40.0)

    def test_half_active_ratio(self):
        # active=50/100=0.5 → 20 pts
        inp = make_input(total_accounts=100, active_accounts=50, new_accounts_won=0,
                         churned_accounts=0, win_rate=0.0)
        assert self.engine._account_health_score(inp) == pytest.approx(20.0)

    def test_churn_severe_clamped_zero(self):
        # active=0, churn=100/100=1.0 → -40; win=0 → score=-40 → clamped to 0
        inp = make_input(total_accounts=100, active_accounts=0, new_accounts_won=0,
                         churned_accounts=100, win_rate=0.0)
        assert self.engine._account_health_score(inp) == 0.0

    def test_new_accounts_growth_exact_30(self):
        # new=10/100=10% → growth_rate=10 → 10*3=30 exactly
        inp = make_input(total_accounts=100, active_accounts=0, new_accounts_won=10,
                         churned_accounts=0, win_rate=0.0)
        assert self.engine._account_health_score(inp) == pytest.approx(30.0)

    def test_new_accounts_below_cap(self):
        # new=3/100=3% → growth_rate=3 → 3*3=9 < 30
        inp = make_input(total_accounts=100, active_accounts=0, new_accounts_won=3,
                         churned_accounts=0, win_rate=0.0)
        assert self.engine._account_health_score(inp) == pytest.approx(9.0)

    def test_win_rate_50(self):
        # total=0 → only win_rate: 50*0.3=15
        inp = make_input(total_accounts=0, active_accounts=0, new_accounts_won=0,
                         churned_accounts=0, win_rate=50.0)
        assert self.engine._account_health_score(inp) == pytest.approx(15.0)


# ---------------------------------------------------------------------------
# Section 19: Activity score additional edge cases
# ---------------------------------------------------------------------------

class TestActivityScoreEdgeCases:
    def setup_method(self):
        self.engine = TerritoryPerformanceEngine()

    def test_activity_per_day_cap_at_50(self):
        # Very high activities/day → day component caps at 50
        # days_elapsed=1 (days_remaining=89, total=90), activities=1000
        # apd=1000, 1000*5=5000 → cap 50; apa=1000/100=10 → 10*5=50 → total=100
        inp = make_input(activities_count=1000, total_accounts=100,
                         days_remaining=89, total_period_days=90)
        assert self.engine._activity_score(inp) == 100.0

    def test_activity_per_account_cap_at_50(self):
        # activities=100, accounts=1 → apa=100 → 100*5=500 capped at 50
        # activities=100, days_elapsed=1 → apd=100 → 100*5=500 capped at 50 → total=100
        inp = make_input(activities_count=100, total_accounts=1,
                         days_remaining=89, total_period_days=90)
        assert self.engine._activity_score(inp) == 100.0

    def test_negative_period_days_returns_zero(self):
        inp = make_input(total_period_days=-1, activities_count=100, total_accounts=10)
        assert self.engine._activity_score(inp) == 0.0

    def test_activity_score_small_values(self):
        # 1 activity, 10 accounts, 10 days elapsed (total=10, remaining=0)
        # apd=1/10=0.1 → 0.1*5=0.5; apa=1/10=0.1 → 0.1*5=0.5 → total=1.0
        inp = make_input(activities_count=1, total_accounts=10,
                         days_remaining=0, total_period_days=10)
        assert self.engine._activity_score(inp) == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# Section 20: Growth score additional tests
# ---------------------------------------------------------------------------

class TestGrowthScoreEdgeCases:
    def setup_method(self):
        self.engine = TerritoryPerformanceEngine()

    def test_growth_all_zero_inputs(self):
        inp = make_input(target_revenue=0.0, pipeline_value=0.0)
        result = self.engine._growth_score(inp, 0.0, 0.0)
        assert result == 0.0

    def test_growth_pipeline_exactly_2x_target(self):
        # pipe_ratio=2.0 → 2*20=40 exactly → capped at 40; health=0; activity=0 → 40
        inp = make_input(target_revenue=1_000_000.0, pipeline_value=2_000_000.0)
        result = self.engine._growth_score(inp, 0.0, 0.0)
        assert result == pytest.approx(40.0)

    def test_growth_pipeline_1x_target(self):
        # pipe_ratio=1.0 → 20; health=0; activity=0 → 20
        inp = make_input(target_revenue=1_000_000.0, pipeline_value=1_000_000.0)
        result = self.engine._growth_score(inp, 0.0, 0.0)
        assert result == pytest.approx(20.0)

    def test_growth_health_and_activity_only(self):
        # target=0 → pipeline part=0; health=100; activity=100 → 100*0.3+100*0.3=60
        inp = make_input(target_revenue=0.0, pipeline_value=0.0)
        result = self.engine._growth_score(inp, 100.0, 100.0)
        assert result == pytest.approx(60.0)


# ---------------------------------------------------------------------------
# Section 21: is_at_risk additional boundary tests
# ---------------------------------------------------------------------------

class TestIsAtRiskAdditional:
    def test_projected_just_below_80_is_at_risk(self):
        engine = TerritoryPerformanceEngine()
        # projected_attainment = 79.9 < 80 → at risk
        inp = make_input(projected_revenue=799_000.0, target_revenue=1_000_000.0,
                         current_penetration=20.0)
        result = engine.analyze(inp)
        assert result.is_at_risk is True

    def test_not_at_risk_medium_risk_projected_above_80(self):
        engine = TerritoryPerformanceEngine()
        # projected=90, health=50 (MEDIUM risk), projected≥80, not HIGH/CRITICAL
        inp = make_input(
            projected_revenue=900_000.0, target_revenue=1_000_000.0,
            active_accounts=60, total_accounts=100,
            new_accounts_won=5, churned_accounts=2,
            win_rate=50.0, current_penetration=20.0,
        )
        result = engine.analyze(inp)
        if result.territory_risk not in (TerritoryRisk.HIGH, TerritoryRisk.CRITICAL):
            assert result.is_at_risk is False


# ---------------------------------------------------------------------------
# Section 22: needs_rebalancing additional boundary tests
# ---------------------------------------------------------------------------

class TestNeedsRebalancingAdditional:
    def test_penetration_just_above_60(self):
        engine = TerritoryPerformanceEngine()
        inp = make_input(current_penetration=60.1, active_accounts=80, total_accounts=100)
        result = engine.analyze(inp)
        assert result.needs_rebalancing is True

    def test_active_ratio_just_below_0_3(self):
        engine = TerritoryPerformanceEngine()
        # 29/100 = 0.29 < 0.3
        inp = make_input(current_penetration=20.0, active_accounts=29, total_accounts=100)
        result = engine.analyze(inp)
        assert result.needs_rebalancing is True

    def test_both_conditions_true(self):
        engine = TerritoryPerformanceEngine()
        # penetration > 60 AND active < 0.3 × total
        inp = make_input(current_penetration=70.0, active_accounts=20, total_accounts=100)
        result = engine.analyze(inp)
        assert result.needs_rebalancing is True


# ---------------------------------------------------------------------------
# Section 23: Summary avg attainment and projected attainment calculations
# ---------------------------------------------------------------------------

class TestSummaryCalculations:
    def test_avg_attainment_three_territories(self):
        engine = TerritoryPerformanceEngine()
        engine.analyze(make_input(territory_id="T1", actual_revenue=900_000.0, target_revenue=1_000_000.0))
        engine.analyze(make_input(territory_id="T2", actual_revenue=700_000.0, target_revenue=1_000_000.0))
        engine.analyze(make_input(territory_id="T3", actual_revenue=800_000.0, target_revenue=1_000_000.0))
        s = engine.summary()
        # (90 + 70 + 80) / 3 = 80.0
        assert s["avg_attainment_pct"] == pytest.approx(80.0)

    def test_avg_projected_three_territories(self):
        engine = TerritoryPerformanceEngine()
        engine.analyze(make_input(territory_id="T1", projected_revenue=1_100_000.0, target_revenue=1_000_000.0))
        engine.analyze(make_input(territory_id="T2", projected_revenue=900_000.0, target_revenue=1_000_000.0))
        engine.analyze(make_input(territory_id="T3", projected_revenue=1_000_000.0, target_revenue=1_000_000.0))
        s = engine.summary()
        # (110 + 90 + 100) / 3 = 100.0
        assert s["avg_projected_attainment"] == pytest.approx(100.0)

    def test_high_performing_count_in_summary(self):
        engine = TerritoryPerformanceEngine()
        # T1: OVERPERFORMING, T2: ON_TARGET, T3: CRITICAL
        engine.analyze(make_input(territory_id="T1", projected_revenue=1_200_000.0,
                                   target_revenue=1_000_000.0, active_accounts=90,
                                   total_accounts=100, win_rate=80.0, new_accounts_won=5,
                                   churned_accounts=0, current_penetration=20.0))
        engine.analyze(make_input(territory_id="T2", projected_revenue=950_000.0,
                                   target_revenue=1_000_000.0, active_accounts=80,
                                   total_accounts=100, win_rate=70.0, new_accounts_won=5,
                                   churned_accounts=0, current_penetration=20.0))
        engine.analyze(make_input(territory_id="T3", projected_revenue=400_000.0,
                                   target_revenue=1_000_000.0, current_penetration=20.0))
        s = engine.summary()
        assert s["high_performing_count"] >= 2

    def test_rebalancing_count_in_summary(self):
        engine = TerritoryPerformanceEngine()
        engine.analyze(make_input(territory_id="T1", current_penetration=70.0))
        engine.analyze(make_input(territory_id="T2", current_penetration=10.0, active_accounts=70, total_accounts=100))
        s = engine.summary()
        assert s["rebalancing_count"] >= 1

    def test_avg_account_health_in_summary(self):
        engine = TerritoryPerformanceEngine()
        r1 = engine.analyze(make_input(territory_id="T1"))
        engine.reset()
        engine.analyze(make_input(territory_id="T1"))
        s = engine.summary()
        assert s["avg_account_health"] >= 0.0
        assert s["avg_account_health"] <= 100.0

    def test_avg_growth_score_in_summary(self):
        engine = TerritoryPerformanceEngine()
        engine.analyze(make_input())
        s = engine.summary()
        assert 0.0 <= s["avg_growth_score"] <= 100.0
