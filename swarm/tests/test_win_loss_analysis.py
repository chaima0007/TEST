"""Tests for WinLossAnalysisEngine"""
import pytest
from dataclasses import fields as dc_fields
from intelligence.win_loss_analysis_engine import (
    WinLossAnalysisEngine, WinLossInput, WinLossResult,
    WinLossRisk, WinLossPattern, WinLossSeverity, WinLossAction,
)


@pytest.fixture
def engine():
    return WinLossAnalysisEngine()


@pytest.fixture
def strong_input():
    return WinLossInput(
        total_deals_analyzed=50, won_deals=35,
        lost_to_price=3, lost_to_competitor=4, lost_to_no_decision=3,
        lost_product_fit=2, lost_relationship=1, lost_timing=2,
        avg_sales_cycle_won=40.0, avg_sales_cycle_lost=50.0,
        avg_deal_value_won=32000.0, avg_deal_value_lost=28000.0,
        competitor_mentioned_pct=25.0, top_competitor_win_rate_vs=60.0,
        discount_rate_won_avg=5.0, discount_rate_lost_avg=3.0,
        champion_present_won_pct=85.0, champion_present_lost_pct=25.0,
        executive_sponsor_won_pct=75.0, executive_sponsor_lost_pct=20.0,
        num_competitors_tracked=5, quarter="Q2",
    )


@pytest.fixture
def weak_input():
    return WinLossInput(
        total_deals_analyzed=50, won_deals=12,
        lost_to_price=18, lost_to_competitor=10, lost_to_no_decision=5,
        lost_product_fit=3, lost_relationship=1, lost_timing=1,
        avg_sales_cycle_won=55.0, avg_sales_cycle_lost=45.0,
        avg_deal_value_won=20000.0, avg_deal_value_lost=22000.0,
        competitor_mentioned_pct=70.0, top_competitor_win_rate_vs=30.0,
        discount_rate_won_avg=15.0, discount_rate_lost_avg=8.0,
        champion_present_won_pct=60.0, champion_present_lost_pct=40.0,
        executive_sponsor_won_pct=50.0, executive_sponsor_lost_pct=35.0,
        num_competitors_tracked=3, quarter="Q3",
    )


class TestResultStructure:
    def test_result_has_15_fields(self):
        assert len(dc_fields(WinLossResult)) == 15

    def test_to_dict_has_15_keys(self, engine, strong_input):
        assert len(engine.assess(strong_input).to_dict()) == 15

    def test_to_dict_keys(self, engine, strong_input):
        d = engine.assess(strong_input).to_dict()
        expected = {
            "composite_score", "risk", "pattern", "severity", "action",
            "win_rate_score", "competitive_score", "relationship_score",
            "process_efficiency_score", "win_rate_pct", "primary_loss_reason",
            "estimated_recoverable_revenue", "signal", "champion_impact_delta",
            "price_sensitivity_index",
        }
        assert set(d.keys()) == expected


class TestStrongPerformance:
    def test_strong_low_risk(self, engine, strong_input):
        r = engine.assess(strong_input)
        assert r.risk == WinLossRisk.low

    def test_strong_win_rate_pct(self, engine, strong_input):
        r = engine.assess(strong_input)
        assert r.win_rate_pct == 70.0

    def test_strong_signal_non_empty(self, engine, strong_input):
        r = engine.assess(strong_input)
        assert len(r.signal) > 10

    def test_strong_severity_strong(self, engine, strong_input):
        r = engine.assess(strong_input)
        assert r.severity == WinLossSeverity.strong


class TestWeakPerformance:
    def test_weak_returns_high_or_critical(self, engine, weak_input):
        r = engine.assess(weak_input)
        assert r.risk in (WinLossRisk.high, WinLossRisk.critical)

    def test_weak_win_rate_low(self, engine, weak_input):
        r = engine.assess(weak_input)
        assert r.win_rate_pct < 30

    def test_weak_recoverable_revenue_positive(self, engine, weak_input):
        r = engine.assess(weak_input)
        assert r.estimated_recoverable_revenue > 0


class TestScoreBoundaries:
    def test_composite_bounded(self, engine):
        for inp in [WinLossInput(), WinLossInput(total_deals_analyzed=0),
                    WinLossInput(won_deals=0)]:
            r = engine.assess(inp)
            assert 0 <= r.composite_score <= 100

    def test_sub_scores_bounded(self, engine, strong_input):
        r = engine.assess(strong_input)
        for s in [r.win_rate_score, r.competitive_score, r.relationship_score, r.process_efficiency_score]:
            assert 0 <= s <= 100


class TestPatternDetection:
    def test_price_sensitivity_detected(self, engine):
        inp = WinLossInput(total_deals_analyzed=50, won_deals=20,
                           lost_to_price=20, lost_to_competitor=3,
                           lost_to_no_decision=3, lost_product_fit=2,
                           lost_relationship=1, lost_timing=1)
        r = engine.assess(inp)
        assert r.pattern == WinLossPattern.price_sensitivity

    def test_competitive_displacement_detected(self, engine):
        inp = WinLossInput(total_deals_analyzed=50, won_deals=20,
                           lost_to_price=3, lost_to_competitor=16,
                           lost_to_no_decision=3, lost_product_fit=2,
                           lost_relationship=3, lost_timing=3)
        r = engine.assess(inp)
        assert r.pattern == WinLossPattern.competitive_displacement

    def test_action_matches_pattern(self, engine, weak_input):
        r = engine.assess(weak_input)
        action_map = {
            WinLossPattern.price_sensitivity: WinLossAction.pricing_review,
            WinLossPattern.competitive_displacement: WinLossAction.competitive_enablement,
            WinLossPattern.none: WinLossAction.maintain,
        }
        if r.pattern in action_map:
            assert r.action == action_map[r.pattern]


class TestBatchSummary:
    def test_batch_length(self, engine, strong_input, weak_input):
        assert len(engine.batch([strong_input, weak_input])) == 2

    def test_summary_13_keys(self, engine, strong_input, weak_input):
        results = engine.batch([strong_input, weak_input])
        assert len(engine.summary(results)) == 13

    def test_summary_empty(self, engine):
        assert engine.summary([]) == {}

    def test_summary_total_analyses(self, engine, strong_input, weak_input):
        results = engine.batch([strong_input, weak_input])
        assert engine.summary(results)["total_analyses"] == 2

    def test_champion_delta_positive_for_strong(self, engine, strong_input):
        r = engine.assess(strong_input)
        assert r.champion_impact_delta > 0
