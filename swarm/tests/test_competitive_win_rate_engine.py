"""Comprehensive pytest tests for CompetitiveWinRateEngine."""
from __future__ import annotations

import pytest

from swarm.intelligence.competitive_win_rate_engine import (
    CompetitiveAction,
    CompetitiveRisk,
    CompetitiveWinRateEngine,
    CompetitiveWinRateInput,
    CompetitiveWinRateResult,
    TrendDirection,
    WinRateCategory,
)

# ---------------------------------------------------------------------------
# Helpers / Factories
# ---------------------------------------------------------------------------


def make_input(
    matchup_id: str = "M001",
    our_product: str = "ProductA",
    competitor: str = "CompetitorX",
    segment: str = "enterprise",
    region: str = "EMEA",
    total_deals: int = 100,
    won_deals: int = 60,
    lost_deals: int = 40,
    avg_deal_size_won: float = 50_000.0,
    avg_deal_size_lost: float = 40_000.0,
    avg_sales_cycle_won: int = 60,
    avg_sales_cycle_lost: int = 90,
    win_rate_prev_period: float = 55.0,
    price_win_rate: float = 55.0,
    feature_win_rate: float = 60.0,
    relationship_win_rate: float = 70.0,
    deals_with_champion: int = 40,
    deals_without_champion: int = 60,
    exec_engagement_deals: int = 30,
    total_exec_opps: int = 50,
    technical_eval_wins: int = 20,
    technical_eval_total: int = 30,
) -> CompetitiveWinRateInput:
    return CompetitiveWinRateInput(
        matchup_id=matchup_id,
        our_product=our_product,
        competitor=competitor,
        segment=segment,
        region=region,
        total_deals=total_deals,
        won_deals=won_deals,
        lost_deals=lost_deals,
        avg_deal_size_won=avg_deal_size_won,
        avg_deal_size_lost=avg_deal_size_lost,
        avg_sales_cycle_won=avg_sales_cycle_won,
        avg_sales_cycle_lost=avg_sales_cycle_lost,
        win_rate_prev_period=win_rate_prev_period,
        price_win_rate=price_win_rate,
        feature_win_rate=feature_win_rate,
        relationship_win_rate=relationship_win_rate,
        deals_with_champion=deals_with_champion,
        deals_without_champion=deals_without_champion,
        exec_engagement_deals=exec_engagement_deals,
        total_exec_opps=total_exec_opps,
        technical_eval_wins=technical_eval_wins,
        technical_eval_total=technical_eval_total,
    )


# ---------------------------------------------------------------------------
# Section 1: Enum types, str subtype, counts
# ---------------------------------------------------------------------------


class TestEnums:
    def test_win_rate_category_is_str_subtype(self):
        assert isinstance(WinRateCategory.DOMINANT, str)

    def test_competitive_risk_is_str_subtype(self):
        assert isinstance(CompetitiveRisk.LOW, str)

    def test_trend_direction_is_str_subtype(self):
        assert isinstance(TrendDirection.IMPROVING, str)

    def test_competitive_action_is_str_subtype(self):
        assert isinstance(CompetitiveAction.LEVERAGE_STRENGTH, str)

    def test_win_rate_category_count(self):
        assert len(WinRateCategory) == 5

    def test_competitive_risk_count(self):
        assert len(CompetitiveRisk) == 4

    def test_trend_direction_count(self):
        assert len(TrendDirection) == 4

    def test_competitive_action_count(self):
        assert len(CompetitiveAction) == 5

    def test_win_rate_category_values(self):
        values = {e.value for e in WinRateCategory}
        assert values == {"dominant", "strong", "competitive", "weak", "critical"}

    def test_competitive_risk_values(self):
        values = {e.value for e in CompetitiveRisk}
        assert values == {"low", "medium", "high", "critical"}

    def test_trend_direction_values(self):
        values = {e.value for e in TrendDirection}
        assert values == {"improving", "stable", "declining", "volatile"}

    def test_competitive_action_values(self):
        values = {e.value for e in CompetitiveAction}
        assert values == {
            "leverage_strength",
            "reinforce",
            "differentiate",
            "battlecard_update",
            "strategic_review",
        }

    def test_win_rate_category_dominant_value(self):
        assert WinRateCategory.DOMINANT.value == "dominant"

    def test_win_rate_category_strong_value(self):
        assert WinRateCategory.STRONG.value == "strong"

    def test_win_rate_category_competitive_value(self):
        assert WinRateCategory.COMPETITIVE.value == "competitive"

    def test_win_rate_category_weak_value(self):
        assert WinRateCategory.WEAK.value == "weak"

    def test_win_rate_category_critical_value(self):
        assert WinRateCategory.CRITICAL.value == "critical"

    def test_competitive_risk_low_value(self):
        assert CompetitiveRisk.LOW.value == "low"

    def test_competitive_risk_medium_value(self):
        assert CompetitiveRisk.MEDIUM.value == "medium"

    def test_competitive_risk_high_value(self):
        assert CompetitiveRisk.HIGH.value == "high"

    def test_competitive_risk_critical_value(self):
        assert CompetitiveRisk.CRITICAL.value == "critical"

    def test_trend_direction_improving_value(self):
        assert TrendDirection.IMPROVING.value == "improving"

    def test_trend_direction_stable_value(self):
        assert TrendDirection.STABLE.value == "stable"

    def test_trend_direction_declining_value(self):
        assert TrendDirection.DECLINING.value == "declining"

    def test_trend_direction_volatile_value(self):
        assert TrendDirection.VOLATILE.value == "volatile"

    def test_competitive_action_leverage_value(self):
        assert CompetitiveAction.LEVERAGE_STRENGTH.value == "leverage_strength"

    def test_competitive_action_reinforce_value(self):
        assert CompetitiveAction.REINFORCE.value == "reinforce"

    def test_competitive_action_differentiate_value(self):
        assert CompetitiveAction.DIFFERENTIATE.value == "differentiate"

    def test_competitive_action_battlecard_value(self):
        assert CompetitiveAction.BATTLECARD_UPDATE.value == "battlecard_update"

    def test_competitive_action_strategic_review_value(self):
        assert CompetitiveAction.STRATEGIC_REVIEW.value == "strategic_review"


# ---------------------------------------------------------------------------
# Section 2: to_dict() - exactly 15 keys by name, enums as strings
# ---------------------------------------------------------------------------


class TestToDict:
    def setup_method(self):
        self.engine = CompetitiveWinRateEngine()
        self.result = self.engine.analyze(make_input())

    def test_to_dict_has_exactly_15_keys(self):
        d = self.result.to_dict()
        assert len(d) == 15

    def test_to_dict_has_matchup_id(self):
        assert "matchup_id" in self.result.to_dict()

    def test_to_dict_has_our_product(self):
        assert "our_product" in self.result.to_dict()

    def test_to_dict_has_competitor(self):
        assert "competitor" in self.result.to_dict()

    def test_to_dict_has_win_rate_category(self):
        assert "win_rate_category" in self.result.to_dict()

    def test_to_dict_has_competitive_risk(self):
        assert "competitive_risk" in self.result.to_dict()

    def test_to_dict_has_trend_direction(self):
        assert "trend_direction" in self.result.to_dict()

    def test_to_dict_has_competitive_action(self):
        assert "competitive_action" in self.result.to_dict()

    def test_to_dict_has_win_rate(self):
        assert "win_rate" in self.result.to_dict()

    def test_to_dict_has_win_rate_delta(self):
        assert "win_rate_delta" in self.result.to_dict()

    def test_to_dict_has_deal_size_advantage(self):
        assert "deal_size_advantage" in self.result.to_dict()

    def test_to_dict_has_cycle_efficiency(self):
        assert "cycle_efficiency" in self.result.to_dict()

    def test_to_dict_has_champion_lift(self):
        assert "champion_lift" in self.result.to_dict()

    def test_to_dict_has_competitive_score(self):
        assert "competitive_score" in self.result.to_dict()

    def test_to_dict_has_is_at_risk(self):
        assert "is_at_risk" in self.result.to_dict()

    def test_to_dict_has_needs_battlecard(self):
        assert "needs_battlecard" in self.result.to_dict()

    def test_to_dict_win_rate_category_is_string(self):
        d = self.result.to_dict()
        assert isinstance(d["win_rate_category"], str)

    def test_to_dict_competitive_risk_is_string(self):
        d = self.result.to_dict()
        assert isinstance(d["competitive_risk"], str)

    def test_to_dict_trend_direction_is_string(self):
        d = self.result.to_dict()
        assert isinstance(d["trend_direction"], str)

    def test_to_dict_competitive_action_is_string(self):
        d = self.result.to_dict()
        assert isinstance(d["competitive_action"], str)

    def test_to_dict_matchup_id_value(self):
        d = self.result.to_dict()
        assert d["matchup_id"] == "M001"

    def test_to_dict_our_product_value(self):
        d = self.result.to_dict()
        assert d["our_product"] == "ProductA"

    def test_to_dict_competitor_value(self):
        d = self.result.to_dict()
        assert d["competitor"] == "CompetitorX"

    def test_to_dict_win_rate_is_float(self):
        d = self.result.to_dict()
        assert isinstance(d["win_rate"], float)

    def test_to_dict_is_at_risk_is_bool(self):
        d = self.result.to_dict()
        assert isinstance(d["is_at_risk"], bool)

    def test_to_dict_needs_battlecard_is_bool(self):
        d = self.result.to_dict()
        assert isinstance(d["needs_battlecard"], bool)

    def test_to_dict_exact_key_set(self):
        expected_keys = {
            "matchup_id", "our_product", "competitor",
            "win_rate_category", "competitive_risk", "trend_direction",
            "competitive_action", "win_rate", "win_rate_delta",
            "deal_size_advantage", "cycle_efficiency", "champion_lift",
            "competitive_score", "is_at_risk", "needs_battlecard",
        }
        assert set(self.result.to_dict().keys()) == expected_keys


# ---------------------------------------------------------------------------
# Section 3: summary() - exactly 13 keys, empty state, populated correctness
# ---------------------------------------------------------------------------


class TestSummary:
    def test_summary_empty_has_13_keys(self):
        engine = CompetitiveWinRateEngine()
        s = engine.summary()
        assert len(s) == 13

    def test_summary_empty_total_is_zero(self):
        engine = CompetitiveWinRateEngine()
        assert engine.summary()["total"] == 0

    def test_summary_empty_category_counts_is_empty_dict(self):
        engine = CompetitiveWinRateEngine()
        assert engine.summary()["category_counts"] == {}

    def test_summary_empty_risk_counts_is_empty_dict(self):
        engine = CompetitiveWinRateEngine()
        assert engine.summary()["risk_counts"] == {}

    def test_summary_empty_trend_counts_is_empty_dict(self):
        engine = CompetitiveWinRateEngine()
        assert engine.summary()["trend_counts"] == {}

    def test_summary_empty_action_counts_is_empty_dict(self):
        engine = CompetitiveWinRateEngine()
        assert engine.summary()["action_counts"] == {}

    def test_summary_empty_avg_win_rate_is_zero(self):
        engine = CompetitiveWinRateEngine()
        assert engine.summary()["avg_win_rate"] == 0.0

    def test_summary_empty_avg_competitive_score_is_zero(self):
        engine = CompetitiveWinRateEngine()
        assert engine.summary()["avg_competitive_score"] == 0.0

    def test_summary_empty_avg_win_rate_delta_is_zero(self):
        engine = CompetitiveWinRateEngine()
        assert engine.summary()["avg_win_rate_delta"] == 0.0

    def test_summary_empty_at_risk_count_is_zero(self):
        engine = CompetitiveWinRateEngine()
        assert engine.summary()["at_risk_count"] == 0

    def test_summary_empty_battlecard_count_is_zero(self):
        engine = CompetitiveWinRateEngine()
        assert engine.summary()["battlecard_count"] == 0

    def test_summary_empty_avg_deal_size_advantage_is_zero(self):
        engine = CompetitiveWinRateEngine()
        assert engine.summary()["avg_deal_size_advantage"] == 0.0

    def test_summary_empty_avg_cycle_efficiency_is_zero(self):
        engine = CompetitiveWinRateEngine()
        assert engine.summary()["avg_cycle_efficiency"] == 0.0

    def test_summary_empty_dominant_count_is_zero(self):
        engine = CompetitiveWinRateEngine()
        assert engine.summary()["dominant_count"] == 0

    def test_summary_exact_key_set(self):
        engine = CompetitiveWinRateEngine()
        expected_keys = {
            "total", "category_counts", "risk_counts", "trend_counts",
            "action_counts", "avg_win_rate", "avg_competitive_score",
            "avg_win_rate_delta", "at_risk_count", "battlecard_count",
            "avg_deal_size_advantage", "avg_cycle_efficiency", "dominant_count",
        }
        assert set(engine.summary().keys()) == expected_keys

    def test_summary_populated_total(self):
        engine = CompetitiveWinRateEngine()
        engine.analyze(make_input(matchup_id="M001"))
        engine.analyze(make_input(matchup_id="M002"))
        assert engine.summary()["total"] == 2

    def test_summary_populated_category_counts_keys_are_strings(self):
        engine = CompetitiveWinRateEngine()
        engine.analyze(make_input())
        s = engine.summary()
        for k in s["category_counts"]:
            assert isinstance(k, str)

    def test_summary_populated_risk_counts_keys_are_strings(self):
        engine = CompetitiveWinRateEngine()
        engine.analyze(make_input())
        s = engine.summary()
        for k in s["risk_counts"]:
            assert isinstance(k, str)

    def test_summary_populated_trend_counts_keys_are_strings(self):
        engine = CompetitiveWinRateEngine()
        engine.analyze(make_input())
        s = engine.summary()
        for k in s["trend_counts"]:
            assert isinstance(k, str)

    def test_summary_populated_action_counts_keys_are_strings(self):
        engine = CompetitiveWinRateEngine()
        engine.analyze(make_input())
        s = engine.summary()
        for k in s["action_counts"]:
            assert isinstance(k, str)

    def test_summary_populated_avg_win_rate_correct(self):
        engine = CompetitiveWinRateEngine()
        # 60 wins / 100 deals = 60.0
        engine.analyze(make_input(total_deals=100, won_deals=60, win_rate_prev_period=60.0))
        s = engine.summary()
        assert s["avg_win_rate"] == 60.0

    def test_summary_populated_dominant_count(self):
        engine = CompetitiveWinRateEngine()
        # 75% win rate -> DOMINANT
        engine.analyze(make_input(total_deals=100, won_deals=75, win_rate_prev_period=60.0))
        s = engine.summary()
        assert s["dominant_count"] == 1

    def test_summary_at_risk_count(self):
        engine = CompetitiveWinRateEngine()
        # 20% win rate -> is_at_risk = True
        engine.analyze(make_input(total_deals=100, won_deals=20, win_rate_prev_period=20.0,
                                   price_win_rate=20.0, feature_win_rate=20.0))
        s = engine.summary()
        assert s["at_risk_count"] == 1

    def test_summary_battlecard_count(self):
        engine = CompetitiveWinRateEngine()
        # feature_win_rate=30 triggers needs_battlecard
        engine.analyze(make_input(feature_win_rate=30.0))
        s = engine.summary()
        assert s["battlecard_count"] == 1

    def test_summary_has_13_keys_populated(self):
        engine = CompetitiveWinRateEngine()
        engine.analyze(make_input())
        assert len(engine.summary()) == 13


# ---------------------------------------------------------------------------
# Section 4: Scoring helpers - formulas, zero guards, boundary inputs
# ---------------------------------------------------------------------------


class TestWinRateFormula:
    def test_win_rate_basic(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=100, won_deals=60)
        assert engine._win_rate(inp) == 60.0

    def test_win_rate_zero_total(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=0, won_deals=0)
        assert engine._win_rate(inp) == 0.0

    def test_win_rate_negative_total(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=-5, won_deals=0)
        assert engine._win_rate(inp) == 0.0

    def test_win_rate_100_percent(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=50, won_deals=50)
        assert engine._win_rate(inp) == 100.0

    def test_win_rate_zero_percent(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=50, won_deals=0)
        assert engine._win_rate(inp) == 0.0

    def test_win_rate_rounded(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=3, won_deals=1)
        # 1/3 * 100 = 33.333... -> 33.3
        assert engine._win_rate(inp) == round(100 / 3, 1)


class TestWinRateDelta:
    def test_delta_positive(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(win_rate_prev_period=50.0)
        assert engine._win_rate_delta(inp, 60.0) == 10.0

    def test_delta_negative(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(win_rate_prev_period=70.0)
        assert engine._win_rate_delta(inp, 60.0) == -10.0

    def test_delta_zero(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(win_rate_prev_period=60.0)
        assert engine._win_rate_delta(inp, 60.0) == 0.0

    def test_delta_rounded(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(win_rate_prev_period=50.5)
        result = engine._win_rate_delta(inp, 60.0)
        assert result == round(60.0 - 50.5, 1)


class TestDealSizeAdvantage:
    def test_deal_size_advantage_basic(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(avg_deal_size_won=50_000.0, avg_deal_size_lost=40_000.0)
        assert engine._deal_size_advantage(inp) == round(50_000.0 / 40_000.0, 2)

    def test_deal_size_advantage_zero_lost(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(avg_deal_size_won=50_000.0, avg_deal_size_lost=0.0)
        assert engine._deal_size_advantage(inp) == 1.0

    def test_deal_size_advantage_negative_lost(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(avg_deal_size_won=50_000.0, avg_deal_size_lost=-1.0)
        assert engine._deal_size_advantage(inp) == 1.0

    def test_deal_size_advantage_equal(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(avg_deal_size_won=50_000.0, avg_deal_size_lost=50_000.0)
        assert engine._deal_size_advantage(inp) == 1.0

    def test_deal_size_advantage_won_smaller(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(avg_deal_size_won=30_000.0, avg_deal_size_lost=50_000.0)
        assert engine._deal_size_advantage(inp) == round(30_000.0 / 50_000.0, 2)


class TestCycleEfficiency:
    def test_cycle_efficiency_basic(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(avg_sales_cycle_won=60, avg_sales_cycle_lost=90)
        assert engine._cycle_efficiency(inp) == round(90 / 60, 2)

    def test_cycle_efficiency_zero_won(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(avg_sales_cycle_won=0, avg_sales_cycle_lost=90)
        assert engine._cycle_efficiency(inp) == 1.0

    def test_cycle_efficiency_negative_won(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(avg_sales_cycle_won=-1, avg_sales_cycle_lost=90)
        assert engine._cycle_efficiency(inp) == 1.0

    def test_cycle_efficiency_equal(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(avg_sales_cycle_won=60, avg_sales_cycle_lost=60)
        assert engine._cycle_efficiency(inp) == 1.0

    def test_cycle_efficiency_lost_shorter(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(avg_sales_cycle_won=90, avg_sales_cycle_lost=60)
        assert engine._cycle_efficiency(inp) == round(60 / 90, 2)


class TestChampionLift:
    def test_champion_lift_both_zero(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(deals_with_champion=0, deals_without_champion=0)
        assert engine._champion_lift(inp) == 0.0

    def test_champion_lift_clamped_upper(self):
        engine = CompetitiveWinRateEngine()
        # All deals have champion => champion_rate=1, no_champion_rate=0
        # lift = (1 * 1.35 - 0 * 0.65) * 100 = 135 -> clamped to 50
        inp = make_input(deals_with_champion=100, deals_without_champion=0)
        result = engine._champion_lift(inp)
        assert result == 50.0

    def test_champion_lift_clamped_lower(self):
        engine = CompetitiveWinRateEngine()
        # All deals have no champion => champion_rate=0, no_champion_rate=1
        # lift = (0 * 1.35 - 1 * 0.65) * 100 = -65 -> clamped to -50
        inp = make_input(deals_with_champion=0, deals_without_champion=100)
        result = engine._champion_lift(inp)
        assert result == -50.0

    def test_champion_lift_balanced(self):
        engine = CompetitiveWinRateEngine()
        # equal split: champion_rate=0.5, no_champion_rate=0.5
        # lift = (0.5*1.35 - 0.5*0.65) * 100 = (0.675 - 0.325) * 100 = 35.0
        inp = make_input(deals_with_champion=50, deals_without_champion=50)
        result = engine._champion_lift(inp)
        assert result == round(max(-50.0, min(50.0, 35.0)), 1)

    def test_champion_lift_returns_float(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(deals_with_champion=40, deals_without_champion=60)
        assert isinstance(engine._champion_lift(inp), float)


class TestCompetitiveScore:
    def test_competitive_score_clamped_minimum(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(price_win_rate=0.0, technical_eval_wins=0, technical_eval_total=1)
        score = engine._competitive_score(inp, 0.0, 0.0, 0.0, 0.0)
        assert score >= 0.0

    def test_competitive_score_clamped_maximum(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(price_win_rate=100.0, technical_eval_wins=100, technical_eval_total=100)
        score = engine._competitive_score(inp, 100.0, 5.0, 5.0, 50.0)
        assert score <= 100.0

    def test_competitive_score_win_rate_component_max_40(self):
        # win_rate 100 => 100 * 0.4 = 40 (but min(40, ...) = 40)
        engine = CompetitiveWinRateEngine()
        inp = make_input(price_win_rate=0.0, technical_eval_wins=0, technical_eval_total=0)
        score = engine._competitive_score(inp, 100.0, 1.0, 1.0, 0.0)
        # win_rate=40 + (1-1)*20+10=10 + (1-1)*20+10=10 + 0 (no tech) + 0 = 60
        assert score == pytest.approx(60.0, abs=0.1)

    def test_competitive_score_deal_advantage_component(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(price_win_rate=0.0, technical_eval_wins=0, technical_eval_total=0)
        # deal_advantage=2.0 => (2-1)*20+10 = 30 -> capped at 20
        score = engine._competitive_score(inp, 0.0, 2.0, 1.0, 0.0)
        # 0 + 20 + 10 = 30
        assert score == pytest.approx(30.0, abs=0.1)

    def test_competitive_score_cycle_efficiency_component(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(price_win_rate=0.0, technical_eval_wins=0, technical_eval_total=0)
        # cycle_eff=2.0 => (2-1)*20+10 = 30 -> capped at 20
        score = engine._competitive_score(inp, 0.0, 1.0, 2.0, 0.0)
        # 0 + 10 + 20 = 30
        assert score == pytest.approx(30.0, abs=0.1)

    def test_competitive_score_tech_rate_component(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(price_win_rate=0.0, technical_eval_wins=100, technical_eval_total=100)
        # tech_rate=100 => min(10, 100*0.1) = 10
        score = engine._competitive_score(inp, 0.0, 1.0, 1.0, 0.0)
        # 0 + 10 + 10 + 10 = 30
        assert score == pytest.approx(30.0, abs=0.1)

    def test_competitive_score_price_win_rate_component(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(price_win_rate=100.0, technical_eval_wins=0, technical_eval_total=0)
        # price_win_rate=100 => min(10, 100*0.1) = 10
        score = engine._competitive_score(inp, 0.0, 1.0, 1.0, 0.0)
        # 0 + 10 + 10 + 0 + 10 = 30
        assert score == pytest.approx(30.0, abs=0.1)

    def test_competitive_score_no_tech_evals(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(price_win_rate=0.0, technical_eval_wins=0, technical_eval_total=0)
        score = engine._competitive_score(inp, 0.0, 1.0, 1.0, 0.0)
        # 0 + 10 + 10 + 0 + 0 = 20
        assert score == pytest.approx(20.0, abs=0.1)

    def test_competitive_score_is_float(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input()
        score = engine._competitive_score(inp, 60.0, 1.25, 1.5, 20.0)
        assert isinstance(score, float)


# ---------------------------------------------------------------------------
# Section 5: _win_rate_category - all 5 boundaries
# ---------------------------------------------------------------------------


class TestWinRateCategory:
    def test_category_dominant_at_70(self):
        engine = CompetitiveWinRateEngine()
        assert engine._win_rate_category(70.0) == WinRateCategory.DOMINANT

    def test_category_dominant_above_70(self):
        engine = CompetitiveWinRateEngine()
        assert engine._win_rate_category(85.0) == WinRateCategory.DOMINANT

    def test_category_dominant_at_100(self):
        engine = CompetitiveWinRateEngine()
        assert engine._win_rate_category(100.0) == WinRateCategory.DOMINANT

    def test_category_strong_at_55(self):
        engine = CompetitiveWinRateEngine()
        assert engine._win_rate_category(55.0) == WinRateCategory.STRONG

    def test_category_strong_just_below_70(self):
        engine = CompetitiveWinRateEngine()
        assert engine._win_rate_category(69.9) == WinRateCategory.STRONG

    def test_category_competitive_at_40(self):
        engine = CompetitiveWinRateEngine()
        assert engine._win_rate_category(40.0) == WinRateCategory.COMPETITIVE

    def test_category_competitive_just_below_55(self):
        engine = CompetitiveWinRateEngine()
        assert engine._win_rate_category(54.9) == WinRateCategory.COMPETITIVE

    def test_category_weak_at_25(self):
        engine = CompetitiveWinRateEngine()
        assert engine._win_rate_category(25.0) == WinRateCategory.WEAK

    def test_category_weak_just_below_40(self):
        engine = CompetitiveWinRateEngine()
        assert engine._win_rate_category(39.9) == WinRateCategory.WEAK

    def test_category_critical_just_below_25(self):
        engine = CompetitiveWinRateEngine()
        assert engine._win_rate_category(24.9) == WinRateCategory.CRITICAL

    def test_category_critical_at_zero(self):
        engine = CompetitiveWinRateEngine()
        assert engine._win_rate_category(0.0) == WinRateCategory.CRITICAL

    def test_category_critical_at_10(self):
        engine = CompetitiveWinRateEngine()
        assert engine._win_rate_category(10.0) == WinRateCategory.CRITICAL


# ---------------------------------------------------------------------------
# Section 6: _competitive_risk - all 4 levels with both conditions
# ---------------------------------------------------------------------------


class TestCompetitiveRisk:
    def test_risk_low_both_conditions_met(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input()
        # wr >= 60 AND delta >= -5 => LOW
        assert engine._competitive_risk(inp, 60.0, 0.0) == CompetitiveRisk.LOW

    def test_risk_low_wr_exactly_60_delta_exactly_neg5(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input()
        assert engine._competitive_risk(inp, 60.0, -5.0) == CompetitiveRisk.LOW

    def test_risk_low_wr_above_60(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input()
        assert engine._competitive_risk(inp, 80.0, 5.0) == CompetitiveRisk.LOW

    def test_risk_not_low_wr_below_60(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input()
        result = engine._competitive_risk(inp, 59.0, 0.0)
        assert result != CompetitiveRisk.LOW

    def test_risk_not_low_delta_below_neg5(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input()
        result = engine._competitive_risk(inp, 65.0, -6.0)
        assert result != CompetitiveRisk.LOW

    def test_risk_medium_wr_exactly_45_delta_neg15(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input()
        # wr>=45 AND delta>=-15 (but not LOW conditions) => MEDIUM
        assert engine._competitive_risk(inp, 45.0, -15.0) == CompetitiveRisk.MEDIUM

    def test_risk_medium_wr_above_45_delta_neg6(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input()
        # wr=59 (not >=60), delta=-6 (not >=-5), but wr>=45 AND delta>=-15 => MEDIUM
        assert engine._competitive_risk(inp, 59.0, -6.0) == CompetitiveRisk.MEDIUM

    def test_risk_medium_wr_50_delta_neg10(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input()
        assert engine._competitive_risk(inp, 50.0, -10.0) == CompetitiveRisk.MEDIUM

    def test_risk_not_medium_delta_below_neg15(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input()
        result = engine._competitive_risk(inp, 45.0, -16.0)
        assert result != CompetitiveRisk.MEDIUM

    def test_risk_high_wr_exactly_30(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input()
        # wr>=30 but not LOW or MEDIUM conditions
        assert engine._competitive_risk(inp, 30.0, -20.0) == CompetitiveRisk.HIGH

    def test_risk_high_wr_between_30_45(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input()
        assert engine._competitive_risk(inp, 38.0, -20.0) == CompetitiveRisk.HIGH

    def test_risk_high_wr_30_delta_large_negative(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input()
        assert engine._competitive_risk(inp, 30.0, -50.0) == CompetitiveRisk.HIGH

    def test_risk_critical_wr_below_30(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input()
        assert engine._competitive_risk(inp, 29.9, -20.0) == CompetitiveRisk.CRITICAL

    def test_risk_critical_wr_zero(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input()
        assert engine._competitive_risk(inp, 0.0, -50.0) == CompetitiveRisk.CRITICAL

    def test_risk_critical_wr_20(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input()
        assert engine._competitive_risk(inp, 20.0, -30.0) == CompetitiveRisk.CRITICAL


# ---------------------------------------------------------------------------
# Section 7: _trend_direction - all 4 states
# ---------------------------------------------------------------------------


class TestTrendDirection:
    def test_trend_improving_at_8(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(win_rate_prev_period=50.0, price_win_rate=50.0)
        assert engine._trend_direction(8.0, inp) == TrendDirection.IMPROVING

    def test_trend_improving_above_8(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(win_rate_prev_period=50.0, price_win_rate=50.0)
        assert engine._trend_direction(15.0, inp) == TrendDirection.IMPROVING

    def test_trend_declining_at_neg8(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(win_rate_prev_period=50.0, price_win_rate=50.0)
        assert engine._trend_direction(-8.0, inp) == TrendDirection.DECLINING

    def test_trend_declining_below_neg8(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(win_rate_prev_period=50.0, price_win_rate=50.0)
        assert engine._trend_direction(-15.0, inp) == TrendDirection.DECLINING

    def test_trend_stable_requires_both_conditions(self):
        engine = CompetitiveWinRateEngine()
        # delta <= 3 AND |prev - price_wr| < 15 => STABLE
        inp = make_input(win_rate_prev_period=50.0, price_win_rate=55.0)
        # |50 - 55| = 5 < 15; delta=2 (within ±3)
        assert engine._trend_direction(2.0, inp) == TrendDirection.STABLE

    def test_trend_stable_exact_boundaries(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(win_rate_prev_period=50.0, price_win_rate=64.9)
        # |50 - 64.9| = 14.9 < 15; delta=3 (=3) => STABLE
        assert engine._trend_direction(3.0, inp) == TrendDirection.STABLE

    def test_trend_stable_negative_delta_boundary(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(win_rate_prev_period=50.0, price_win_rate=55.0)
        # delta=-3 (abs=3 <=3); |50-55|=5 < 15 => STABLE
        assert engine._trend_direction(-3.0, inp) == TrendDirection.STABLE

    def test_trend_volatile_large_price_diff(self):
        engine = CompetitiveWinRateEngine()
        # delta=2 (within ±3) but |prev - price_wr| >= 15 => VOLATILE
        inp = make_input(win_rate_prev_period=50.0, price_win_rate=65.0)
        # |50 - 65| = 15, not < 15, so not STABLE => VOLATILE
        assert engine._trend_direction(2.0, inp) == TrendDirection.VOLATILE

    def test_trend_volatile_delta_in_range_but_price_diff_large(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(win_rate_prev_period=50.0, price_win_rate=70.0)
        # |50-70|=20 >= 15 => not STABLE => VOLATILE
        assert engine._trend_direction(1.0, inp) == TrendDirection.VOLATILE

    def test_trend_volatile_delta_between_3_and_8(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(win_rate_prev_period=50.0, price_win_rate=51.0)
        # delta=5, not >=8, not <=-8, not <=3 => VOLATILE
        assert engine._trend_direction(5.0, inp) == TrendDirection.VOLATILE

    def test_trend_stable_not_met_when_delta_above_3(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(win_rate_prev_period=50.0, price_win_rate=51.0)
        # delta=4, abs > 3 => not STABLE (but price diff is 1 < 15)
        assert engine._trend_direction(4.0, inp) == TrendDirection.VOLATILE


# ---------------------------------------------------------------------------
# Section 8: _competitive_action - all 5 actions, priority ordering
# ---------------------------------------------------------------------------


class TestCompetitiveAction:
    def test_action_strategic_review_critical_risk_priority(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(feature_win_rate=60.0)
        # CRITICAL risk => STRATEGIC_REVIEW (top priority)
        action = engine._competitive_action(
            inp, WinRateCategory.DOMINANT, CompetitiveRisk.CRITICAL,
            TrendDirection.STABLE, 80.0
        )
        assert action == CompetitiveAction.STRATEGIC_REVIEW

    def test_action_strategic_review_overrides_dominant(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(feature_win_rate=60.0)
        # CRITICAL risk takes priority over DOMINANT category
        action = engine._competitive_action(
            inp, WinRateCategory.DOMINANT, CompetitiveRisk.CRITICAL,
            TrendDirection.STABLE, 90.0
        )
        assert action == CompetitiveAction.STRATEGIC_REVIEW

    def test_action_battlecard_update_declining_high_risk(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(feature_win_rate=60.0)
        action = engine._competitive_action(
            inp, WinRateCategory.WEAK, CompetitiveRisk.HIGH,
            TrendDirection.DECLINING, 30.0
        )
        assert action == CompetitiveAction.BATTLECARD_UPDATE

    def test_action_battlecard_not_triggered_if_not_declining(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(feature_win_rate=60.0)
        action = engine._competitive_action(
            inp, WinRateCategory.WEAK, CompetitiveRisk.HIGH,
            TrendDirection.STABLE, 50.0
        )
        assert action != CompetitiveAction.BATTLECARD_UPDATE or action == CompetitiveAction.DIFFERENTIATE

    def test_action_leverage_strength_dominant(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(feature_win_rate=60.0)
        action = engine._competitive_action(
            inp, WinRateCategory.DOMINANT, CompetitiveRisk.LOW,
            TrendDirection.STABLE, 80.0
        )
        assert action == CompetitiveAction.LEVERAGE_STRENGTH

    def test_action_differentiate_strong_feature_wr_below_50(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(feature_win_rate=40.0)
        action = engine._competitive_action(
            inp, WinRateCategory.STRONG, CompetitiveRisk.LOW,
            TrendDirection.STABLE, 70.0
        )
        assert action == CompetitiveAction.DIFFERENTIATE

    def test_action_differentiate_competitive_feature_wr_below_50(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(feature_win_rate=49.0)
        action = engine._competitive_action(
            inp, WinRateCategory.COMPETITIVE, CompetitiveRisk.MEDIUM,
            TrendDirection.STABLE, 60.0
        )
        assert action == CompetitiveAction.DIFFERENTIATE

    def test_action_reinforce_strong_feature_wr_at_50(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(feature_win_rate=50.0)
        action = engine._competitive_action(
            inp, WinRateCategory.STRONG, CompetitiveRisk.LOW,
            TrendDirection.STABLE, 70.0
        )
        assert action == CompetitiveAction.REINFORCE

    def test_action_reinforce_competitive_feature_wr_above_50(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(feature_win_rate=70.0)
        action = engine._competitive_action(
            inp, WinRateCategory.COMPETITIVE, CompetitiveRisk.MEDIUM,
            TrendDirection.STABLE, 60.0
        )
        assert action == CompetitiveAction.REINFORCE

    def test_action_battlecard_update_low_score(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(feature_win_rate=60.0)
        # WEAK category, LOW risk, not declining -> falls to score<40 check
        action = engine._competitive_action(
            inp, WinRateCategory.WEAK, CompetitiveRisk.LOW,
            TrendDirection.STABLE, 35.0
        )
        assert action == CompetitiveAction.BATTLECARD_UPDATE

    def test_action_differentiate_fallback(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(feature_win_rate=60.0)
        # WEAK category, LOW risk, not declining, score>=40 => DIFFERENTIATE
        action = engine._competitive_action(
            inp, WinRateCategory.WEAK, CompetitiveRisk.LOW,
            TrendDirection.STABLE, 50.0
        )
        assert action == CompetitiveAction.DIFFERENTIATE

    def test_action_critical_risk_wins_over_declining_high(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(feature_win_rate=60.0)
        # CRITICAL risk, DECLINING trend, HIGH risk - CRITICAL takes priority
        action = engine._competitive_action(
            inp, WinRateCategory.WEAK, CompetitiveRisk.CRITICAL,
            TrendDirection.DECLINING, 20.0
        )
        assert action == CompetitiveAction.STRATEGIC_REVIEW

    def test_action_battlecard_update_declining_high_wins_over_dominant(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(feature_win_rate=60.0)
        # HIGH risk + DECLINING -> BATTLECARD_UPDATE (before DOMINANT check)
        action = engine._competitive_action(
            inp, WinRateCategory.DOMINANT, CompetitiveRisk.HIGH,
            TrendDirection.DECLINING, 80.0
        )
        assert action == CompetitiveAction.BATTLECARD_UPDATE


# ---------------------------------------------------------------------------
# Section 9: is_at_risk - both conditions independently
# ---------------------------------------------------------------------------


class TestIsAtRisk:
    def test_is_at_risk_win_rate_below_40(self):
        engine = CompetitiveWinRateEngine()
        # 39% win rate < 40.0 => at_risk
        inp = make_input(total_deals=100, won_deals=39, win_rate_prev_period=39.0,
                          price_win_rate=39.0, feature_win_rate=60.0)
        result = engine.analyze(inp)
        assert result.is_at_risk is True

    def test_is_at_risk_win_rate_exactly_40_not_at_risk_by_wr(self):
        engine = CompetitiveWinRateEngine()
        # 40% win rate -> not triggered by wr condition (need risk check)
        inp = make_input(total_deals=100, won_deals=40, win_rate_prev_period=40.0,
                          price_win_rate=40.0, feature_win_rate=60.0)
        result = engine.analyze(inp)
        # wr=40, not < 40; check if risk is LOW or MEDIUM to confirm no risk
        # wr=40 < 45 => not MEDIUM; wr=40 >=30 => HIGH => at_risk = True
        # So in this case it IS at_risk via HIGH risk
        assert result.is_at_risk is True  # HIGH risk because wr<45

    def test_is_at_risk_due_to_high_risk(self):
        engine = CompetitiveWinRateEngine()
        # wr=45, delta=-20 => MEDIUM (wr>=45 but delta<-15 = nope -> HIGH)
        # wr=45, delta=-20: wr>=60 AND delta>=-5? No. wr>=45 AND delta>=-15? No.
        # wr>=30? Yes => HIGH => is_at_risk = True
        inp = make_input(total_deals=100, won_deals=45, win_rate_prev_period=65.0,
                          price_win_rate=50.0, feature_win_rate=60.0)
        result = engine.analyze(inp)
        assert result.is_at_risk is True

    def test_is_at_risk_due_to_critical_risk(self):
        engine = CompetitiveWinRateEngine()
        # wr=20% => CRITICAL risk => at_risk
        inp = make_input(total_deals=100, won_deals=20, win_rate_prev_period=20.0,
                          price_win_rate=20.0, feature_win_rate=60.0)
        result = engine.analyze(inp)
        assert result.is_at_risk is True

    def test_not_at_risk_win_rate_above_40_low_risk(self):
        engine = CompetitiveWinRateEngine()
        # wr=65, delta=5 => LOW risk => not at_risk
        inp = make_input(total_deals=100, won_deals=65, win_rate_prev_period=60.0,
                          price_win_rate=60.0, feature_win_rate=60.0)
        result = engine.analyze(inp)
        assert result.is_at_risk is False

    def test_not_at_risk_medium_risk_win_rate_above_40(self):
        engine = CompetitiveWinRateEngine()
        # wr=50, delta=-8 => MEDIUM (wr>=45, delta>=-15); wr>=40, MEDIUM => not at_risk
        inp = make_input(total_deals=100, won_deals=50, win_rate_prev_period=58.0,
                          price_win_rate=50.0, feature_win_rate=60.0)
        result = engine.analyze(inp)
        assert result.is_at_risk is False


# ---------------------------------------------------------------------------
# Section 10: needs_battlecard - all 3 conditions independently
# ---------------------------------------------------------------------------


class TestNeedsBattlecard:
    def test_needs_battlecard_delta_below_neg10(self):
        engine = CompetitiveWinRateEngine()
        # delta < -10 triggers needs_battlecard
        inp = make_input(total_deals=100, won_deals=50, win_rate_prev_period=62.0,
                          price_win_rate=50.0, feature_win_rate=60.0)
        result = engine.analyze(inp)
        # win_rate=50, prev=62 => delta=-12 => needs_battlecard
        assert result.needs_battlecard is True

    def test_needs_battlecard_delta_exactly_neg10_no(self):
        engine = CompetitiveWinRateEngine()
        # delta = -10.0 => NOT < -10, so this condition alone won't trigger
        inp = make_input(total_deals=100, won_deals=50, win_rate_prev_period=60.0,
                          price_win_rate=55.0, feature_win_rate=60.0)
        result = engine.analyze(inp)
        # win_rate=50, prev=60 => delta=-10 (not < -10)
        # win_rate=50 >= 35, feature_wr=60 >= 40 => no
        assert result.needs_battlecard is False

    def test_needs_battlecard_win_rate_below_35(self):
        engine = CompetitiveWinRateEngine()
        # win_rate < 35 triggers needs_battlecard
        inp = make_input(total_deals=100, won_deals=34, win_rate_prev_period=34.0,
                          price_win_rate=40.0, feature_win_rate=60.0)
        result = engine.analyze(inp)
        assert result.needs_battlecard is True

    def test_needs_battlecard_win_rate_exactly_35_no(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=100, won_deals=35, win_rate_prev_period=35.0,
                          price_win_rate=40.0, feature_win_rate=60.0)
        result = engine.analyze(inp)
        # win_rate=35 (not < 35), delta=0, feature_wr=60 => no
        assert result.needs_battlecard is False

    def test_needs_battlecard_feature_win_rate_below_40(self):
        engine = CompetitiveWinRateEngine()
        # feature_win_rate < 40 triggers needs_battlecard
        inp = make_input(total_deals=100, won_deals=60, win_rate_prev_period=60.0,
                          price_win_rate=50.0, feature_win_rate=39.0)
        result = engine.analyze(inp)
        assert result.needs_battlecard is True

    def test_needs_battlecard_feature_win_rate_exactly_40_no(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=100, won_deals=60, win_rate_prev_period=60.0,
                          price_win_rate=55.0, feature_win_rate=40.0)
        result = engine.analyze(inp)
        # delta=0, win_rate=60, feature_wr=40 => no
        assert result.needs_battlecard is False

    def test_no_battlecard_when_all_conditions_ok(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=100, won_deals=65, win_rate_prev_period=60.0,
                          price_win_rate=60.0, feature_win_rate=60.0)
        result = engine.analyze(inp)
        # delta=5, win_rate=65, feature_wr=60 => all false
        assert result.needs_battlecard is False


# ---------------------------------------------------------------------------
# Section 11: Properties - empty/populated
# ---------------------------------------------------------------------------


class TestProperties:
    def test_at_risk_matchups_empty(self):
        engine = CompetitiveWinRateEngine()
        assert engine.at_risk_matchups == []

    def test_battlecard_needed_empty(self):
        engine = CompetitiveWinRateEngine()
        assert engine.battlecard_needed == []

    def test_dominant_matchups_empty(self):
        engine = CompetitiveWinRateEngine()
        assert engine.dominant_matchups == []

    def test_avg_win_rate_empty(self):
        engine = CompetitiveWinRateEngine()
        assert engine.avg_win_rate == 0.0

    def test_avg_competitive_score_empty(self):
        engine = CompetitiveWinRateEngine()
        assert engine.avg_competitive_score == 0.0

    def test_at_risk_matchups_populated(self):
        engine = CompetitiveWinRateEngine()
        # 20% win rate => at_risk
        inp = make_input(total_deals=100, won_deals=20, win_rate_prev_period=20.0,
                          price_win_rate=20.0, feature_win_rate=60.0)
        engine.analyze(inp)
        assert len(engine.at_risk_matchups) == 1

    def test_at_risk_matchups_filters_correctly(self):
        engine = CompetitiveWinRateEngine()
        # Add one at-risk and one not at-risk
        engine.analyze(make_input(matchup_id="M001", total_deals=100, won_deals=20,
                                   win_rate_prev_period=20.0, price_win_rate=20.0,
                                   feature_win_rate=60.0))
        engine.analyze(make_input(matchup_id="M002", total_deals=100, won_deals=65,
                                   win_rate_prev_period=60.0, price_win_rate=60.0,
                                   feature_win_rate=60.0))
        assert len(engine.at_risk_matchups) == 1
        assert engine.at_risk_matchups[0].matchup_id == "M001"

    def test_battlecard_needed_populated(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(feature_win_rate=30.0)
        engine.analyze(inp)
        assert len(engine.battlecard_needed) == 1

    def test_dominant_matchups_populated(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=100, won_deals=75, win_rate_prev_period=70.0)
        engine.analyze(inp)
        assert len(engine.dominant_matchups) == 1

    def test_dominant_matchups_category_filter(self):
        engine = CompetitiveWinRateEngine()
        engine.analyze(make_input(matchup_id="M001", total_deals=100, won_deals=75,
                                   win_rate_prev_period=70.0))
        engine.analyze(make_input(matchup_id="M002", total_deals=100, won_deals=50,
                                   win_rate_prev_period=50.0))
        assert len(engine.dominant_matchups) == 1
        assert engine.dominant_matchups[0].matchup_id == "M001"

    def test_avg_win_rate_populated_single(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=100, won_deals=60, win_rate_prev_period=60.0)
        engine.analyze(inp)
        assert engine.avg_win_rate == 60.0

    def test_avg_win_rate_populated_multiple(self):
        engine = CompetitiveWinRateEngine()
        engine.analyze(make_input(matchup_id="M001", total_deals=100, won_deals=60,
                                   win_rate_prev_period=60.0))
        engine.analyze(make_input(matchup_id="M002", total_deals=100, won_deals=80,
                                   win_rate_prev_period=70.0))
        # avg = (60 + 80) / 2 = 70.0
        assert engine.avg_win_rate == 70.0

    def test_avg_competitive_score_populated(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=100, won_deals=60, win_rate_prev_period=60.0)
        result = engine.analyze(inp)
        assert engine.avg_competitive_score == result.competitive_score

    def test_avg_win_rate_rounded_to_1_decimal(self):
        engine = CompetitiveWinRateEngine()
        engine.analyze(make_input(matchup_id="M001", total_deals=3, won_deals=1,
                                   win_rate_prev_period=33.3))
        engine.analyze(make_input(matchup_id="M002", total_deals=3, won_deals=2,
                                   win_rate_prev_period=66.7))
        # Check it's a float rounded to 1 decimal
        avg = engine.avg_win_rate
        assert isinstance(avg, float)
        assert avg == round(avg, 1)


# ---------------------------------------------------------------------------
# Section 12: analyze_batch and reset
# ---------------------------------------------------------------------------


class TestAnalyzeBatchAndReset:
    def test_analyze_batch_returns_list(self):
        engine = CompetitiveWinRateEngine()
        inputs = [make_input(matchup_id=f"M{i:03d}") for i in range(5)]
        results = engine.analyze_batch(inputs)
        assert isinstance(results, list)

    def test_analyze_batch_correct_count(self):
        engine = CompetitiveWinRateEngine()
        inputs = [make_input(matchup_id=f"M{i:03d}") for i in range(5)]
        results = engine.analyze_batch(inputs)
        assert len(results) == 5

    def test_analyze_batch_each_result_is_correct_type(self):
        engine = CompetitiveWinRateEngine()
        inputs = [make_input(matchup_id=f"M{i:03d}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        for r in results:
            assert isinstance(r, CompetitiveWinRateResult)

    def test_analyze_batch_stores_results(self):
        engine = CompetitiveWinRateEngine()
        inputs = [make_input(matchup_id=f"M{i:03d}") for i in range(5)]
        engine.analyze_batch(inputs)
        assert engine.summary()["total"] == 5

    def test_analyze_batch_empty(self):
        engine = CompetitiveWinRateEngine()
        results = engine.analyze_batch([])
        assert results == []

    def test_analyze_batch_single(self):
        engine = CompetitiveWinRateEngine()
        results = engine.analyze_batch([make_input()])
        assert len(results) == 1

    def test_analyze_batch_preserves_order(self):
        engine = CompetitiveWinRateEngine()
        inputs = [make_input(matchup_id=f"M{i:03d}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        for i, result in enumerate(results):
            assert result.matchup_id == f"M{i:03d}"

    def test_reset_clears_results(self):
        engine = CompetitiveWinRateEngine()
        engine.analyze(make_input())
        engine.reset()
        assert engine.summary()["total"] == 0

    def test_reset_clears_at_risk(self):
        engine = CompetitiveWinRateEngine()
        engine.analyze(make_input(total_deals=100, won_deals=20, win_rate_prev_period=20.0,
                                   price_win_rate=20.0, feature_win_rate=60.0))
        engine.reset()
        assert len(engine.at_risk_matchups) == 0

    def test_reset_clears_dominant(self):
        engine = CompetitiveWinRateEngine()
        engine.analyze(make_input(total_deals=100, won_deals=75, win_rate_prev_period=70.0))
        engine.reset()
        assert len(engine.dominant_matchups) == 0

    def test_reset_allows_reuse(self):
        engine = CompetitiveWinRateEngine()
        engine.analyze(make_input(matchup_id="M001"))
        engine.reset()
        engine.analyze(make_input(matchup_id="M002"))
        assert engine.summary()["total"] == 1

    def test_analyze_accumulates_results(self):
        engine = CompetitiveWinRateEngine()
        engine.analyze(make_input(matchup_id="M001"))
        engine.analyze(make_input(matchup_id="M002"))
        engine.analyze(make_input(matchup_id="M003"))
        assert engine.summary()["total"] == 3


# ---------------------------------------------------------------------------
# Section 13: Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_total_deals_zero_win_rate(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=0, won_deals=0)
        result = engine.analyze(inp)
        assert result.win_rate == 0.0

    def test_total_deals_zero_category_critical(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=0, won_deals=0)
        result = engine.analyze(inp)
        assert result.win_rate_category == WinRateCategory.CRITICAL

    def test_avg_deal_size_lost_zero_advantage(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(avg_deal_size_won=100_000.0, avg_deal_size_lost=0.0)
        result = engine.analyze(inp)
        assert result.deal_size_advantage == 1.0

    def test_avg_sales_cycle_won_zero_efficiency(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(avg_sales_cycle_won=0, avg_sales_cycle_lost=90)
        result = engine.analyze(inp)
        assert result.cycle_efficiency == 1.0

    def test_zero_exec_opps_exec_rate(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_exec_opps=0, exec_engagement_deals=10)
        # exec_rate should be 0.0, but it doesn't affect the result directly
        result = engine.analyze(inp)
        assert isinstance(result, CompetitiveWinRateResult)

    def test_champion_both_zero_lift(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(deals_with_champion=0, deals_without_champion=0)
        result = engine.analyze(inp)
        assert result.champion_lift == 0.0

    def test_technical_eval_total_zero_no_tech_score(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(technical_eval_wins=5, technical_eval_total=0)
        # Should not add tech score
        result = engine.analyze(inp)
        assert result.competitive_score >= 0.0

    def test_all_deals_won(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=50, won_deals=50)
        result = engine.analyze(inp)
        assert result.win_rate == 100.0
        assert result.win_rate_category == WinRateCategory.DOMINANT

    def test_all_deals_lost(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=50, won_deals=0, win_rate_prev_period=0.0,
                          price_win_rate=0.0)
        result = engine.analyze(inp)
        assert result.win_rate == 0.0
        assert result.win_rate_category == WinRateCategory.CRITICAL

    def test_result_matchup_id_preserved(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(matchup_id="SPECIAL_ID_123")
        result = engine.analyze(inp)
        assert result.matchup_id == "SPECIAL_ID_123"

    def test_result_our_product_preserved(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(our_product="MyProduct")
        result = engine.analyze(inp)
        assert result.our_product == "MyProduct"

    def test_result_competitor_preserved(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(competitor="BigCompetitor")
        result = engine.analyze(inp)
        assert result.competitor == "BigCompetitor"

    def test_competitive_score_non_negative(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=0, won_deals=0, avg_deal_size_won=0.0,
                          avg_deal_size_lost=0.0, avg_sales_cycle_won=0,
                          avg_sales_cycle_lost=0, price_win_rate=0.0,
                          technical_eval_wins=0, technical_eval_total=0)
        result = engine.analyze(inp)
        assert result.competitive_score >= 0.0

    def test_competitive_score_at_most_100(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=100, won_deals=100, avg_deal_size_won=1_000_000.0,
                          avg_deal_size_lost=1.0, avg_sales_cycle_won=1,
                          avg_sales_cycle_lost=1000, price_win_rate=100.0,
                          technical_eval_wins=100, technical_eval_total=100)
        result = engine.analyze(inp)
        assert result.competitive_score <= 100.0

    def test_is_at_risk_false_type(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=100, won_deals=65, win_rate_prev_period=60.0,
                          price_win_rate=60.0, feature_win_rate=60.0)
        result = engine.analyze(inp)
        assert isinstance(result.is_at_risk, bool)

    def test_needs_battlecard_false_type(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=100, won_deals=65, win_rate_prev_period=60.0,
                          price_win_rate=60.0, feature_win_rate=60.0)
        result = engine.analyze(inp)
        assert isinstance(result.needs_battlecard, bool)

    def test_large_batch(self):
        engine = CompetitiveWinRateEngine()
        inputs = [make_input(matchup_id=f"M{i:04d}") for i in range(50)]
        results = engine.analyze_batch(inputs)
        assert len(results) == 50
        assert engine.summary()["total"] == 50

    def test_analyze_returns_competitive_win_rate_result(self):
        engine = CompetitiveWinRateEngine()
        result = engine.analyze(make_input())
        assert isinstance(result, CompetitiveWinRateResult)

    def test_win_rate_delta_boundary_exactly_8(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(win_rate_prev_period=50.0, price_win_rate=50.0)
        # current = 58.0, prev = 50.0, delta = 8.0 => IMPROVING
        assert engine._trend_direction(8.0, inp) == TrendDirection.IMPROVING

    def test_win_rate_delta_boundary_exactly_neg8(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(win_rate_prev_period=50.0, price_win_rate=50.0)
        assert engine._trend_direction(-8.0, inp) == TrendDirection.DECLINING

    def test_summary_counts_add_up(self):
        engine = CompetitiveWinRateEngine()
        for i in range(5):
            engine.analyze(make_input(matchup_id=f"M{i:03d}"))
        s = engine.summary()
        assert sum(s["category_counts"].values()) == 5

    def test_summary_risk_counts_add_up(self):
        engine = CompetitiveWinRateEngine()
        for i in range(5):
            engine.analyze(make_input(matchup_id=f"M{i:03d}"))
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == 5

    def test_summary_trend_counts_add_up(self):
        engine = CompetitiveWinRateEngine()
        for i in range(5):
            engine.analyze(make_input(matchup_id=f"M{i:03d}"))
        s = engine.summary()
        assert sum(s["trend_counts"].values()) == 5

    def test_summary_action_counts_add_up(self):
        engine = CompetitiveWinRateEngine()
        for i in range(5):
            engine.analyze(make_input(matchup_id=f"M{i:03d}"))
        s = engine.summary()
        assert sum(s["action_counts"].values()) == 5

    def test_multiple_engines_independent(self):
        engine1 = CompetitiveWinRateEngine()
        engine2 = CompetitiveWinRateEngine()
        engine1.analyze(make_input(matchup_id="M001"))
        engine1.analyze(make_input(matchup_id="M002"))
        engine2.analyze(make_input(matchup_id="M003"))
        assert engine1.summary()["total"] == 2
        assert engine2.summary()["total"] == 1

    def test_reset_then_summary_empty(self):
        engine = CompetitiveWinRateEngine()
        for i in range(5):
            engine.analyze(make_input(matchup_id=f"M{i:03d}"))
        engine.reset()
        s = engine.summary()
        assert s["total"] == 0
        assert s["category_counts"] == {}

    def test_win_rate_1_deal_won(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=1, won_deals=1)
        assert engine._win_rate(inp) == 100.0

    def test_win_rate_1_deal_lost(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=1, won_deals=0)
        assert engine._win_rate(inp) == 0.0

    def test_champion_lift_only_with_champion(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(deals_with_champion=50, deals_without_champion=0)
        result = engine._champion_lift(inp)
        # champion_rate=1, no_champion_rate=0 => (1*1.35 - 0*0.65)*100 = 135 -> 50
        assert result == 50.0

    def test_champion_lift_only_without_champion(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(deals_with_champion=0, deals_without_champion=50)
        result = engine._champion_lift(inp)
        # champion_rate=0, no_champion_rate=1 => (0*1.35 - 1*0.65)*100 = -65 -> -50
        assert result == -50.0

    def test_exec_engagement_rate_populated(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(exec_engagement_deals=30, total_exec_opps=50)
        result = engine._exec_engagement_rate(inp)
        assert result == round(30 / 50 * 100, 1)

    def test_exec_engagement_rate_zero_opps(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(exec_engagement_deals=10, total_exec_opps=0)
        result = engine._exec_engagement_rate(inp)
        assert result == 0.0

    def test_to_dict_win_rate_category_equals_enum_value(self):
        engine = CompetitiveWinRateEngine()
        # 75% => DOMINANT
        result = engine.analyze(make_input(total_deals=100, won_deals=75,
                                            win_rate_prev_period=70.0))
        d = result.to_dict()
        assert d["win_rate_category"] == WinRateCategory.DOMINANT.value

    def test_to_dict_competitive_risk_equals_enum_value(self):
        engine = CompetitiveWinRateEngine()
        result = engine.analyze(make_input(total_deals=100, won_deals=65,
                                            win_rate_prev_period=60.0,
                                            price_win_rate=60.0))
        d = result.to_dict()
        assert d["competitive_risk"] == result.competitive_risk.value

    def test_category_weak_above_25_below_40(self):
        engine = CompetitiveWinRateEngine()
        assert engine._win_rate_category(32.0) == WinRateCategory.WEAK

    def test_category_strong_exact(self):
        engine = CompetitiveWinRateEngine()
        assert engine._win_rate_category(62.0) == WinRateCategory.STRONG

    def test_category_competitive_exact(self):
        engine = CompetitiveWinRateEngine()
        assert engine._win_rate_category(47.0) == WinRateCategory.COMPETITIVE


# ---------------------------------------------------------------------------
# Section 14: CompetitiveWinRateInput dataclass field validation
# ---------------------------------------------------------------------------


class TestInputDataclass:
    def test_input_has_22_fields(self):
        import dataclasses
        fields = dataclasses.fields(CompetitiveWinRateInput)
        assert len(fields) == 22

    def test_input_matchup_id_field(self):
        inp = make_input(matchup_id="TEST")
        assert inp.matchup_id == "TEST"

    def test_input_segment_field(self):
        inp = make_input(segment="smb")
        assert inp.segment == "smb"

    def test_input_region_field(self):
        inp = make_input(region="APAC")
        assert inp.region == "APAC"

    def test_input_total_deals_field(self):
        inp = make_input(total_deals=42)
        assert inp.total_deals == 42

    def test_input_won_deals_field(self):
        inp = make_input(won_deals=20)
        assert inp.won_deals == 20

    def test_input_lost_deals_field(self):
        inp = make_input(lost_deals=22)
        assert inp.lost_deals == 22

    def test_input_avg_deal_size_won_field(self):
        inp = make_input(avg_deal_size_won=99_999.0)
        assert inp.avg_deal_size_won == 99_999.0

    def test_input_avg_deal_size_lost_field(self):
        inp = make_input(avg_deal_size_lost=55_000.0)
        assert inp.avg_deal_size_lost == 55_000.0

    def test_input_win_rate_prev_period_field(self):
        inp = make_input(win_rate_prev_period=42.5)
        assert inp.win_rate_prev_period == 42.5

    def test_input_feature_win_rate_field(self):
        inp = make_input(feature_win_rate=75.0)
        assert inp.feature_win_rate == 75.0


# ---------------------------------------------------------------------------
# Section 15: CompetitiveWinRateResult dataclass and result correctness
# ---------------------------------------------------------------------------


class TestResultDataclass:
    def test_result_has_all_fields(self):
        import dataclasses
        fields = {f.name for f in dataclasses.fields(CompetitiveWinRateResult)}
        expected = {
            "matchup_id", "our_product", "competitor",
            "win_rate_category", "competitive_risk", "trend_direction",
            "competitive_action", "win_rate", "win_rate_delta",
            "deal_size_advantage", "cycle_efficiency", "champion_lift",
            "competitive_score", "is_at_risk", "needs_battlecard",
        }
        assert fields == expected

    def test_result_win_rate_matches_formula(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=100, won_deals=67)
        result = engine.analyze(inp)
        assert result.win_rate == round(67 / 100 * 100, 1)

    def test_result_delta_matches_formula(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=100, won_deals=60, win_rate_prev_period=55.0)
        result = engine.analyze(inp)
        assert result.win_rate_delta == round(60.0 - 55.0, 1)

    def test_result_deal_size_advantage_matches_formula(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(avg_deal_size_won=75_000.0, avg_deal_size_lost=50_000.0)
        result = engine.analyze(inp)
        assert result.deal_size_advantage == round(75_000.0 / 50_000.0, 2)

    def test_result_cycle_efficiency_matches_formula(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(avg_sales_cycle_won=45, avg_sales_cycle_lost=90)
        result = engine.analyze(inp)
        assert result.cycle_efficiency == round(90 / 45, 2)

    def test_result_category_consistent_with_win_rate(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=100, won_deals=75, win_rate_prev_period=70.0)
        result = engine.analyze(inp)
        assert result.win_rate == 75.0
        assert result.win_rate_category == WinRateCategory.DOMINANT

    def test_result_risk_consistent_with_win_rate_and_delta(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=100, won_deals=65, win_rate_prev_period=60.0,
                          price_win_rate=60.0)
        result = engine.analyze(inp)
        # wr=65 >= 60, delta=5 >= -5 => LOW
        assert result.competitive_risk == CompetitiveRisk.LOW


# ---------------------------------------------------------------------------
# Section 16: Additional boundary and integration tests
# ---------------------------------------------------------------------------


class TestAdditionalBoundaries:
    def test_risk_low_exact_boundary_wr_60_delta_neg5(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input()
        assert engine._competitive_risk(inp, 60.0, -5.0) == CompetitiveRisk.LOW

    def test_risk_medium_exact_wr_45_delta_neg15(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input()
        assert engine._competitive_risk(inp, 45.0, -15.0) == CompetitiveRisk.MEDIUM

    def test_risk_high_wr_44_9_delta_neg16(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input()
        # wr=44.9 not >=45, delta=-16 not >=-15 -> not MEDIUM; wr>=30 -> HIGH
        assert engine._competitive_risk(inp, 44.9, -16.0) == CompetitiveRisk.HIGH

    def test_trend_stable_zero_delta_zero_price_diff(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(win_rate_prev_period=50.0, price_win_rate=50.0)
        assert engine._trend_direction(0.0, inp) == TrendDirection.STABLE

    def test_action_reinforce_competitive_category(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(feature_win_rate=55.0)
        action = engine._competitive_action(
            inp, WinRateCategory.COMPETITIVE, CompetitiveRisk.MEDIUM,
            TrendDirection.STABLE, 60.0
        )
        assert action == CompetitiveAction.REINFORCE

    def test_score_deal_advantage_less_than_1(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(price_win_rate=0.0, technical_eval_wins=0, technical_eval_total=0)
        # deal_advantage=0.5 => (0.5-1)*20+10 = -10+10 = 0 -> max(0, ...)
        score = engine._competitive_score(inp, 0.0, 0.5, 1.0, 0.0)
        # 0 + max(0 capped via min(20,...)) = but min(20, 0) = 0
        # 0 + 0 + 10 + 0 + 0 = 10
        assert score == pytest.approx(10.0, abs=0.1)

    def test_score_cycle_less_than_1(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(price_win_rate=0.0, technical_eval_wins=0, technical_eval_total=0)
        # cycle_eff=0.5 => (0.5-1)*20+10 = -10+10 = 0
        score = engine._competitive_score(inp, 0.0, 1.0, 0.5, 0.0)
        # 0 + 10 + 0 + 0 + 0 = 10
        assert score == pytest.approx(10.0, abs=0.1)

    def test_win_rate_exactly_69_9_strong(self):
        engine = CompetitiveWinRateEngine()
        assert engine._win_rate_category(69.9) == WinRateCategory.STRONG

    def test_win_rate_exactly_54_9_competitive(self):
        engine = CompetitiveWinRateEngine()
        assert engine._win_rate_category(54.9) == WinRateCategory.COMPETITIVE

    def test_win_rate_exactly_39_9_weak(self):
        engine = CompetitiveWinRateEngine()
        assert engine._win_rate_category(39.9) == WinRateCategory.WEAK

    def test_win_rate_exactly_24_9_critical(self):
        engine = CompetitiveWinRateEngine()
        assert engine._win_rate_category(24.9) == WinRateCategory.CRITICAL

    def test_analyze_stores_result_in_internal_list(self):
        engine = CompetitiveWinRateEngine()
        engine.analyze(make_input(matchup_id="M001"))
        engine.analyze(make_input(matchup_id="M002"))
        assert engine.summary()["total"] == 2

    def test_avg_competitive_score_multiple(self):
        engine = CompetitiveWinRateEngine()
        r1 = engine.analyze(make_input(matchup_id="M001"))
        r2 = engine.analyze(make_input(matchup_id="M002"))
        expected = round((r1.competitive_score + r2.competitive_score) / 2, 1)
        assert engine.avg_competitive_score == expected

    def test_battlecard_needed_returns_list(self):
        engine = CompetitiveWinRateEngine()
        assert isinstance(engine.battlecard_needed, list)

    def test_dominant_matchups_returns_list(self):
        engine = CompetitiveWinRateEngine()
        assert isinstance(engine.dominant_matchups, list)

    def test_at_risk_matchups_returns_list(self):
        engine = CompetitiveWinRateEngine()
        assert isinstance(engine.at_risk_matchups, list)

    def test_summary_avg_deal_size_advantage(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(avg_deal_size_won=60_000.0, avg_deal_size_lost=40_000.0)
        result = engine.analyze(inp)
        s = engine.summary()
        assert s["avg_deal_size_advantage"] == result.deal_size_advantage

    def test_summary_avg_cycle_efficiency(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(avg_sales_cycle_won=60, avg_sales_cycle_lost=90)
        result = engine.analyze(inp)
        s = engine.summary()
        assert s["avg_cycle_efficiency"] == result.cycle_efficiency

    def test_summary_avg_win_rate_delta_positive(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=100, won_deals=60, win_rate_prev_period=50.0)
        engine.analyze(inp)
        s = engine.summary()
        assert s["avg_win_rate_delta"] == 10.0

    def test_summary_avg_win_rate_delta_negative(self):
        engine = CompetitiveWinRateEngine()
        inp = make_input(total_deals=100, won_deals=50, win_rate_prev_period=60.0,
                          price_win_rate=55.0)
        engine.analyze(inp)
        s = engine.summary()
        assert s["avg_win_rate_delta"] == -10.0
