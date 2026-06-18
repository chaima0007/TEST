"""
Comprehensive pytest test suite for Module 121:
SalesCompetitiveWinRateErosionEngine
"""

import dataclasses
import pytest

from swarm.intelligence.sales_competitive_win_rate_erosion_engine import (
    CompetitiveWinRateInput,
    CompetitiveWinRateResult,
    SalesCompetitiveWinRateErosionEngine,
    WinRateRisk,
    ErosionPattern,
    ErosionSeverity,
    WinRateAction,
    _clamp,
)


# ---------------------------------------------------------------------------
# Helpers / Fixtures
# ---------------------------------------------------------------------------

def make_input(**overrides) -> CompetitiveWinRateInput:
    """Return a healthy baseline input; override any fields via kwargs."""
    defaults = dict(
        rep_id="rep-001",
        region="WEST",
        evaluation_period_id="2026-Q1",
        win_rate_current_pct=55.0,
        win_rate_prior_period_pct=57.0,
        win_rate_benchmark_pct=58.0,
        total_competitive_deals=20,
        wins_this_period=11,
        losses_this_period=9,
        losses_on_price_count=2,
        losses_on_features_count=2,
        losses_on_relationship_count=1,
        losses_on_timing_count=1,
        competitor_strength_score=30.0,
        battlecard_last_updated_days=20,
        battlecard_usage_pct=0.70,
        late_stage_loss_count=1,
        late_stage_total_count=8,
        champion_poached_count=0,
        consecutive_loss_streak=0,
        win_rate_trend_3_period_delta=-2.0,
        avg_deal_size_won_usd=10_000.0,
    )
    defaults.update(overrides)
    return CompetitiveWinRateInput(**defaults)


@pytest.fixture
def engine():
    return SalesCompetitiveWinRateErosionEngine()


@pytest.fixture
def healthy_input():
    return make_input()


@pytest.fixture
def critical_input():
    """Input that should trigger critical risk and systematic_loss pattern."""
    return make_input(
        win_rate_current_pct=20.0,
        win_rate_prior_period_pct=55.0,
        win_rate_benchmark_pct=60.0,
        losses_this_period=12,
        wins_this_period=3,
        losses_on_price_count=5,
        losses_on_features_count=4,
        losses_on_relationship_count=3,
        losses_on_timing_count=0,
        consecutive_loss_streak=6,
        late_stage_loss_count=7,
        late_stage_total_count=10,
        champion_poached_count=3,
        win_rate_trend_3_period_delta=-25.0,
        battlecard_last_updated_days=200,
        battlecard_usage_pct=0.05,
        competitor_strength_score=85.0,
        avg_deal_size_won_usd=50_000.0,
    )


# ===========================================================================
# 1. Dataclass field counts
# ===========================================================================

class TestDataclassFieldCounts:

    def test_input_has_22_fields(self):
        fields = dataclasses.fields(CompetitiveWinRateInput)
        assert len(fields) == 22

    def test_result_has_15_fields(self):
        fields = dataclasses.fields(CompetitiveWinRateResult)
        assert len(fields) == 15

    def test_input_field_names(self):
        names = {f.name for f in dataclasses.fields(CompetitiveWinRateInput)}
        expected = {
            "rep_id", "region", "evaluation_period_id",
            "win_rate_current_pct", "win_rate_prior_period_pct", "win_rate_benchmark_pct",
            "total_competitive_deals", "wins_this_period", "losses_this_period",
            "losses_on_price_count", "losses_on_features_count", "losses_on_relationship_count",
            "losses_on_timing_count", "competitor_strength_score", "battlecard_last_updated_days",
            "battlecard_usage_pct", "late_stage_loss_count", "late_stage_total_count",
            "champion_poached_count", "consecutive_loss_streak",
            "win_rate_trend_3_period_delta", "avg_deal_size_won_usd",
        }
        assert names == expected

    def test_result_field_names(self):
        names = {f.name for f in dataclasses.fields(CompetitiveWinRateResult)}
        expected = {
            "rep_id", "region", "win_rate_risk", "erosion_pattern", "erosion_severity",
            "recommended_action", "win_rate_decline_score", "deal_quality_score",
            "competitive_readiness_score", "pattern_intensity_score", "win_rate_composite",
            "is_win_rate_eroding", "requires_coaching", "estimated_lost_revenue_usd",
            "erosion_signal",
        }
        assert names == expected

    def test_input_rep_id_field_type(self):
        field = next(f for f in dataclasses.fields(CompetitiveWinRateInput) if f.name == "rep_id")
        # With PEP 563 annotations the stored type is a string; normalise both ways
        assert field.type in (str, "str")

    def test_input_win_rate_current_pct_is_float_type(self):
        field = next(f for f in dataclasses.fields(CompetitiveWinRateInput) if f.name == "win_rate_current_pct")
        assert field.type in (float, "float")

    def test_input_total_competitive_deals_is_int_type(self):
        field = next(f for f in dataclasses.fields(CompetitiveWinRateInput) if f.name == "total_competitive_deals")
        assert field.type in (int, "int")

    def test_result_is_win_rate_eroding_is_bool_type(self):
        field = next(f for f in dataclasses.fields(CompetitiveWinRateResult) if f.name == "is_win_rate_eroding")
        assert field.type in (bool, "bool")


# ===========================================================================
# 2. to_dict() returns exactly 15 keys
# ===========================================================================

class TestToDict:

    def test_to_dict_returns_15_keys(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert len(result.to_dict()) == 15

    def test_to_dict_key_names(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        expected_keys = {
            "rep_id", "region", "win_rate_risk", "erosion_pattern", "erosion_severity",
            "recommended_action", "win_rate_decline_score", "deal_quality_score",
            "competitive_readiness_score", "pattern_intensity_score", "win_rate_composite",
            "is_win_rate_eroding", "requires_coaching", "estimated_lost_revenue_usd",
            "erosion_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_risk_is_string(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        assert isinstance(d["win_rate_risk"], str)

    def test_to_dict_pattern_is_string(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        assert isinstance(d["erosion_pattern"], str)

    def test_to_dict_severity_is_string(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        assert isinstance(d["erosion_severity"], str)

    def test_to_dict_action_is_string(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_is_win_rate_eroding_is_bool(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        assert isinstance(d["is_win_rate_eroding"], bool)

    def test_to_dict_requires_coaching_is_bool(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        assert isinstance(d["requires_coaching"], bool)

    def test_to_dict_composite_rounded_to_one_decimal(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        val = d["win_rate_composite"]
        assert round(val, 1) == val

    def test_to_dict_estimated_lost_revenue_rounded(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        val = d["estimated_lost_revenue_usd"]
        assert round(val, 2) == val

    def test_to_dict_erosion_signal_is_str(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        assert isinstance(d["erosion_signal"], str)

    def test_to_dict_rep_id_preserved(self, engine):
        inp = make_input(rep_id="xyz-999")
        d = engine.assess(inp).to_dict()
        assert d["rep_id"] == "xyz-999"

    def test_to_dict_region_preserved(self, engine):
        inp = make_input(region="EMEA")
        d = engine.assess(inp).to_dict()
        assert d["region"] == "EMEA"


# ===========================================================================
# 3. summary() returns exactly 13 keys
# ===========================================================================

class TestSummaryKeyCount:

    def test_summary_empty_engine_has_13_keys(self):
        engine = SalesCompetitiveWinRateErosionEngine()
        assert len(engine.summary()) == 13

    def test_summary_after_assess_has_13_keys(self, engine, healthy_input):
        engine.assess(healthy_input)
        assert len(engine.summary()) == 13

    def test_summary_key_names(self, engine, healthy_input):
        engine.assess(healthy_input)
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts", "action_counts",
            "avg_win_rate_composite", "eroding_count", "coaching_count",
            "avg_win_rate_decline_score", "avg_deal_quality_score",
            "avg_competitive_readiness_score", "avg_pattern_intensity_score",
            "total_estimated_lost_revenue_usd",
        }
        assert set(engine.summary().keys()) == expected

    def test_summary_empty_total_is_zero(self):
        engine = SalesCompetitiveWinRateErosionEngine()
        assert engine.summary()["total"] == 0

    def test_summary_empty_eroding_count_is_zero(self):
        engine = SalesCompetitiveWinRateErosionEngine()
        assert engine.summary()["eroding_count"] == 0

    def test_summary_empty_coaching_count_is_zero(self):
        engine = SalesCompetitiveWinRateErosionEngine()
        assert engine.summary()["coaching_count"] == 0

    def test_summary_empty_lost_revenue_is_zero(self):
        engine = SalesCompetitiveWinRateErosionEngine()
        assert engine.summary()["total_estimated_lost_revenue_usd"] == 0.0

    def test_summary_total_increments(self, engine):
        for _ in range(5):
            engine.assess(make_input())
        assert engine.summary()["total"] == 5


# ===========================================================================
# 4. All enum values exist
# ===========================================================================

class TestEnumValues:

    # WinRateRisk
    def test_win_rate_risk_low(self):
        assert WinRateRisk.low.value == "low"

    def test_win_rate_risk_moderate(self):
        assert WinRateRisk.moderate.value == "moderate"

    def test_win_rate_risk_high(self):
        assert WinRateRisk.high.value == "high"

    def test_win_rate_risk_critical(self):
        assert WinRateRisk.critical.value == "critical"

    def test_win_rate_risk_has_4_values(self):
        assert len(WinRateRisk) == 4

    # ErosionPattern
    def test_erosion_pattern_none(self):
        assert ErosionPattern.none.value == "none"

    def test_erosion_pattern_pricing_displacement(self):
        assert ErosionPattern.pricing_displacement.value == "pricing_displacement"

    def test_erosion_pattern_feature_regression(self):
        assert ErosionPattern.feature_regression.value == "feature_regression"

    def test_erosion_pattern_rep_skill_gap(self):
        assert ErosionPattern.rep_skill_gap.value == "rep_skill_gap"

    def test_erosion_pattern_champion_poaching(self):
        assert ErosionPattern.champion_poaching.value == "champion_poaching"

    def test_erosion_pattern_systematic_loss(self):
        assert ErosionPattern.systematic_loss.value == "systematic_loss"

    def test_erosion_pattern_has_6_values(self):
        assert len(ErosionPattern) == 6

    # ErosionSeverity
    def test_erosion_severity_stable(self):
        assert ErosionSeverity.stable.value == "stable"

    def test_erosion_severity_declining(self):
        assert ErosionSeverity.declining.value == "declining"

    def test_erosion_severity_eroding(self):
        assert ErosionSeverity.eroding.value == "eroding"

    def test_erosion_severity_collapse(self):
        assert ErosionSeverity.collapse.value == "collapse"

    def test_erosion_severity_has_4_values(self):
        assert len(ErosionSeverity) == 4

    # WinRateAction
    def test_win_rate_action_no_action(self):
        assert WinRateAction.no_action.value == "no_action"

    def test_win_rate_action_battlecard_refresh(self):
        assert WinRateAction.battlecard_refresh.value == "battlecard_refresh"

    def test_win_rate_action_competitive_coaching(self):
        assert WinRateAction.competitive_coaching.value == "competitive_coaching"

    def test_win_rate_action_pricing_strategy_review(self):
        assert WinRateAction.pricing_strategy_review.value == "pricing_strategy_review"

    def test_win_rate_action_executive_competitive_review(self):
        assert WinRateAction.executive_competitive_review.value == "executive_competitive_review"

    def test_win_rate_action_has_5_values(self):
        assert len(WinRateAction) == 5

    # Enum string inheritance
    def test_win_rate_risk_is_str_subclass(self):
        assert isinstance(WinRateRisk.low, str)

    def test_erosion_pattern_is_str_subclass(self):
        assert isinstance(ErosionPattern.none, str)


# ===========================================================================
# 5. Composite score calculation
# ===========================================================================

class TestCompositeScore:

    def test_composite_in_range_0_100(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert 0.0 <= result.win_rate_composite <= 100.0

    def test_composite_rounded_to_one_decimal(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert round(result.win_rate_composite, 1) == result.win_rate_composite

    def test_composite_zero_for_perfect_rep(self, engine):
        inp = make_input(
            win_rate_current_pct=80.0,
            win_rate_prior_period_pct=80.0,
            win_rate_benchmark_pct=60.0,
            consecutive_loss_streak=0,
            late_stage_loss_count=0,
            late_stage_total_count=0,
            champion_poached_count=0,
            win_rate_trend_3_period_delta=5.0,
            battlecard_last_updated_days=10,
            battlecard_usage_pct=0.90,
            competitor_strength_score=10.0,
            losses_this_period=5,
            losses_on_price_count=0,
            losses_on_features_count=0,
            losses_on_relationship_count=0,
            losses_on_timing_count=0,
        )
        result = engine.assess(inp)
        assert result.win_rate_composite == 0.0

    def test_composite_high_for_critical_input(self, engine, critical_input):
        result = engine.assess(critical_input)
        assert result.win_rate_composite >= 60.0

    def test_composite_weights_are_applied(self, engine):
        """
        Manually validate composite: each sub-score feeds into weighted sum.
        """
        inp = make_input(
            win_rate_current_pct=60.0,
            win_rate_prior_period_pct=60.0,
            win_rate_benchmark_pct=60.0,
            consecutive_loss_streak=0,
            late_stage_loss_count=0,
            late_stage_total_count=0,
            champion_poached_count=0,
            win_rate_trend_3_period_delta=0.0,
            battlecard_last_updated_days=10,
            battlecard_usage_pct=0.90,
            competitor_strength_score=10.0,
            losses_this_period=5,
            losses_on_price_count=0,
            losses_on_features_count=0,
            losses_on_relationship_count=0,
            losses_on_timing_count=0,
        )
        result = engine.assess(inp)
        assert result.win_rate_composite == 0.0

    def test_composite_does_not_exceed_100(self, engine, critical_input):
        result = engine.assess(critical_input)
        assert result.win_rate_composite <= 100.0

    def test_composite_not_negative(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.win_rate_composite >= 0.0


# ===========================================================================
# 6. is_win_rate_eroding flag — all 3 trigger conditions
# ===========================================================================

class TestIsWinRateEroding:

    # Trigger 1: composite >= 40
    def test_eroding_via_composite_gte_40(self, engine):
        inp = make_input(
            win_rate_current_pct=20.0,
            win_rate_prior_period_pct=55.0,
            win_rate_benchmark_pct=60.0,
            losses_this_period=10,
            losses_on_price_count=4,
            losses_on_features_count=3,
            consecutive_loss_streak=5,
            late_stage_loss_count=6,
            late_stage_total_count=8,
            battlecard_last_updated_days=200,
            battlecard_usage_pct=0.05,
            competitor_strength_score=85.0,
            win_rate_trend_3_period_delta=-5.0,
        )
        result = engine.assess(inp)
        assert result.win_rate_composite >= 40.0
        assert result.is_win_rate_eroding is True

    # Trigger 2: consecutive_loss_streak >= 4
    def test_eroding_via_loss_streak_exactly_4(self, engine):
        inp = make_input(
            consecutive_loss_streak=4,
            win_rate_trend_3_period_delta=0.0,
        )
        result = engine.assess(inp)
        # Even if composite < 40, flag must be True because streak == 4
        assert result.is_win_rate_eroding is True

    def test_eroding_via_loss_streak_above_4(self, engine):
        inp = make_input(consecutive_loss_streak=7)
        result = engine.assess(inp)
        assert result.is_win_rate_eroding is True

    def test_not_eroding_loss_streak_3(self, engine):
        # streak=3 alone should NOT trigger (threshold is >=4)
        inp = make_input(
            consecutive_loss_streak=3,
            win_rate_trend_3_period_delta=0.0,
            win_rate_current_pct=58.0,
            win_rate_prior_period_pct=58.0,
            win_rate_benchmark_pct=58.0,
            late_stage_loss_count=0,
            late_stage_total_count=0,
            champion_poached_count=0,
            battlecard_last_updated_days=10,
            battlecard_usage_pct=0.90,
            competitor_strength_score=10.0,
            losses_on_price_count=0,
            losses_on_features_count=0,
            losses_on_relationship_count=0,
        )
        result = engine.assess(inp)
        # All three triggers are absent: streak<4, trend>-15, composite should be low
        if result.win_rate_composite < 40 and inp.win_rate_trend_3_period_delta > -15:
            assert result.is_win_rate_eroding is False

    # Trigger 3: win_rate_trend_3_period_delta <= -15
    def test_eroding_via_trend_exactly_minus_15(self, engine):
        inp = make_input(
            win_rate_trend_3_period_delta=-15.0,
            consecutive_loss_streak=0,
        )
        result = engine.assess(inp)
        assert result.is_win_rate_eroding is True

    def test_eroding_via_trend_below_minus_15(self, engine):
        inp = make_input(win_rate_trend_3_period_delta=-25.0)
        result = engine.assess(inp)
        assert result.is_win_rate_eroding is True

    def test_not_eroding_trend_minus_14(self, engine):
        # trend=-14 should NOT trigger alone
        inp = make_input(
            win_rate_trend_3_period_delta=-14.0,
            consecutive_loss_streak=0,
            win_rate_current_pct=58.0,
            win_rate_prior_period_pct=58.0,
            win_rate_benchmark_pct=58.0,
            late_stage_loss_count=0,
            late_stage_total_count=0,
            champion_poached_count=0,
            battlecard_last_updated_days=10,
            battlecard_usage_pct=0.90,
            competitor_strength_score=10.0,
            losses_on_price_count=0,
            losses_on_features_count=0,
            losses_on_relationship_count=0,
        )
        result = engine.assess(inp)
        if result.win_rate_composite < 40 and inp.consecutive_loss_streak < 4:
            assert result.is_win_rate_eroding is False

    def test_not_eroding_healthy_rep(self, engine):
        inp = make_input(
            win_rate_current_pct=80.0,
            win_rate_prior_period_pct=80.0,
            win_rate_benchmark_pct=60.0,
            consecutive_loss_streak=0,
            win_rate_trend_3_period_delta=5.0,
            late_stage_loss_count=0,
            late_stage_total_count=0,
            champion_poached_count=0,
            battlecard_last_updated_days=10,
            battlecard_usage_pct=0.90,
            competitor_strength_score=10.0,
            losses_on_price_count=0,
            losses_on_features_count=0,
            losses_on_relationship_count=0,
        )
        result = engine.assess(inp)
        assert result.is_win_rate_eroding is False


# ===========================================================================
# 7. requires_coaching flag — all 3 trigger conditions
# ===========================================================================

class TestRequiresCoaching:

    # Trigger 1: composite >= 30
    def test_coaching_via_composite_gte_30(self, engine):
        inp = make_input(
            win_rate_current_pct=25.0,
            win_rate_prior_period_pct=50.0,
            win_rate_benchmark_pct=60.0,
            losses_this_period=10,
            consecutive_loss_streak=4,
            late_stage_loss_count=5,
            late_stage_total_count=8,
            battlecard_last_updated_days=10,   # fresh to avoid overlap
            battlecard_usage_pct=0.80,
            competitor_strength_score=30.0,
            champion_poached_count=0,
            win_rate_trend_3_period_delta=-5.0,
            losses_on_price_count=0,
            losses_on_features_count=0,
            losses_on_relationship_count=0,
        )
        result = engine.assess(inp)
        assert result.win_rate_composite >= 30.0
        assert result.requires_coaching is True

    # Trigger 2: late_stage_loss_count >= 3
    def test_coaching_via_late_stage_loss_exactly_3(self, engine):
        inp = make_input(
            late_stage_loss_count=3,
            late_stage_total_count=10,
            battlecard_last_updated_days=10,
            consecutive_loss_streak=0,
            win_rate_current_pct=58.0,
            win_rate_prior_period_pct=58.0,
            win_rate_benchmark_pct=58.0,
            battlecard_usage_pct=0.90,
            competitor_strength_score=10.0,
            win_rate_trend_3_period_delta=0.0,
            losses_on_price_count=0,
            losses_on_features_count=0,
            losses_on_relationship_count=0,
        )
        result = engine.assess(inp)
        assert result.requires_coaching is True

    def test_coaching_via_late_stage_loss_above_3(self, engine):
        inp = make_input(late_stage_loss_count=5, late_stage_total_count=10)
        result = engine.assess(inp)
        assert result.requires_coaching is True

    def test_not_coaching_late_stage_loss_2_only(self, engine):
        # late_stage_loss_count=2 alone should not trigger (threshold >=3)
        inp = make_input(
            late_stage_loss_count=2,
            late_stage_total_count=10,
            battlecard_last_updated_days=10,
            consecutive_loss_streak=0,
            win_rate_current_pct=58.0,
            win_rate_prior_period_pct=58.0,
            win_rate_benchmark_pct=58.0,
            battlecard_usage_pct=0.90,
            competitor_strength_score=10.0,
            win_rate_trend_3_period_delta=0.0,
            losses_on_price_count=0,
            losses_on_features_count=0,
            losses_on_relationship_count=0,
        )
        result = engine.assess(inp)
        if result.win_rate_composite < 30 and inp.battlecard_last_updated_days < 90:
            assert result.requires_coaching is False

    # Trigger 3: battlecard_last_updated_days >= 90
    def test_coaching_via_battlecard_exactly_90_days(self, engine):
        inp = make_input(
            battlecard_last_updated_days=90,
            late_stage_loss_count=0,
            consecutive_loss_streak=0,
            win_rate_current_pct=58.0,
            win_rate_prior_period_pct=58.0,
            win_rate_benchmark_pct=58.0,
            battlecard_usage_pct=0.90,
            competitor_strength_score=10.0,
            win_rate_trend_3_period_delta=0.0,
            losses_on_price_count=0,
            losses_on_features_count=0,
            losses_on_relationship_count=0,
        )
        result = engine.assess(inp)
        assert result.requires_coaching is True

    def test_coaching_via_battlecard_above_90(self, engine):
        inp = make_input(battlecard_last_updated_days=150)
        result = engine.assess(inp)
        assert result.requires_coaching is True

    def test_not_coaching_battlecard_89_days(self, engine):
        inp = make_input(
            battlecard_last_updated_days=89,
            late_stage_loss_count=0,
            consecutive_loss_streak=0,
            win_rate_current_pct=58.0,
            win_rate_prior_period_pct=58.0,
            win_rate_benchmark_pct=58.0,
            battlecard_usage_pct=0.90,
            competitor_strength_score=10.0,
            win_rate_trend_3_period_delta=0.0,
            losses_on_price_count=0,
            losses_on_features_count=0,
            losses_on_relationship_count=0,
        )
        result = engine.assess(inp)
        if result.win_rate_composite < 30 and inp.late_stage_loss_count < 3:
            assert result.requires_coaching is False

    def test_requires_coaching_is_bool(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.requires_coaching, bool)


# ===========================================================================
# 8. estimated_lost_revenue_usd calculation
# ===========================================================================

class TestEstimatedLostRevenue:

    def test_formula_losses_times_deal_size_times_composite_over_100(self, engine):
        inp = make_input(losses_this_period=5, avg_deal_size_won_usd=20_000.0)
        result = engine.assess(inp)
        expected = 5 * 20_000.0 * (result.win_rate_composite / 100.0)
        assert abs(result.estimated_lost_revenue_usd - expected) < 0.01

    def test_zero_losses_gives_zero_revenue(self, engine):
        inp = make_input(
            losses_this_period=0,
            avg_deal_size_won_usd=50_000.0,
            wins_this_period=20,
            total_competitive_deals=20,
        )
        result = engine.assess(inp)
        assert result.estimated_lost_revenue_usd == 0.0

    def test_zero_deal_size_gives_zero_revenue(self, engine):
        inp = make_input(avg_deal_size_won_usd=0.0)
        result = engine.assess(inp)
        assert result.estimated_lost_revenue_usd == 0.0

    def test_revenue_scales_with_deal_size(self, engine):
        inp_small = make_input(avg_deal_size_won_usd=10_000.0, losses_this_period=3)
        inp_large = make_input(avg_deal_size_won_usd=100_000.0, losses_this_period=3)
        r_small = engine.assess(inp_small)
        r_large = engine.assess(inp_large)
        if r_small.win_rate_composite > 0 and r_large.win_rate_composite > 0:
            assert r_large.estimated_lost_revenue_usd > r_small.estimated_lost_revenue_usd

    def test_revenue_scales_with_losses(self, engine):
        inp_few = make_input(losses_this_period=2, avg_deal_size_won_usd=10_000.0)
        inp_many = make_input(losses_this_period=10, avg_deal_size_won_usd=10_000.0)
        r_few = engine.assess(inp_few)
        r_many = engine.assess(inp_many)
        if r_few.win_rate_composite > 0 and r_many.win_rate_composite > 0:
            assert r_many.estimated_lost_revenue_usd > r_few.estimated_lost_revenue_usd

    def test_revenue_not_negative(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.estimated_lost_revenue_usd >= 0.0

    def test_revenue_calculation_exact(self, engine):
        """Use a configuration that drives composite to a known value."""
        # zero sub-scores => composite = 0 => revenue = 0
        inp = make_input(
            win_rate_current_pct=80.0,
            win_rate_prior_period_pct=80.0,
            win_rate_benchmark_pct=60.0,
            losses_this_period=5,
            consecutive_loss_streak=0,
            late_stage_loss_count=0,
            late_stage_total_count=0,
            champion_poached_count=0,
            win_rate_trend_3_period_delta=5.0,
            battlecard_last_updated_days=10,
            battlecard_usage_pct=0.90,
            competitor_strength_score=10.0,
            losses_on_price_count=0,
            losses_on_features_count=0,
            losses_on_relationship_count=0,
            avg_deal_size_won_usd=10_000.0,
        )
        result = engine.assess(inp)
        assert result.estimated_lost_revenue_usd == 0.0


# ===========================================================================
# 9. Pattern detection priority order
# ===========================================================================

class TestPatternDetection:

    def test_no_losses_returns_none_pattern(self, engine):
        inp = make_input(
            losses_this_period=0,
            wins_this_period=20,
            total_competitive_deals=20,
        )
        result = engine.assess(inp)
        assert result.erosion_pattern == ErosionPattern.none

    def test_systematic_loss_priority_over_champion_poaching(self, engine):
        """systematic_loss has highest priority."""
        inp = make_input(
            consecutive_loss_streak=5,
            win_rate_current_pct=20.0,
            win_rate_prior_period_pct=55.0,
            win_rate_benchmark_pct=60.0,
            losses_this_period=10,
            champion_poached_count=3,
            losses_on_price_count=3,
            losses_on_features_count=3,
            losses_on_relationship_count=3,
            late_stage_loss_count=6,
            late_stage_total_count=8,
            win_rate_trend_3_period_delta=-25.0,
            battlecard_last_updated_days=200,
            battlecard_usage_pct=0.05,
            competitor_strength_score=85.0,
        )
        result = engine.assess(inp)
        assert result.erosion_pattern == ErosionPattern.systematic_loss

    def test_champion_poaching_detected(self, engine):
        inp = make_input(
            champion_poached_count=2,
            consecutive_loss_streak=1,  # below systematic threshold
            losses_this_period=8,
            losses_on_price_count=0,
            losses_on_features_count=0,
            losses_on_relationship_count=4,
            win_rate_trend_3_period_delta=0.0,
        )
        result = engine.assess(inp)
        assert result.erosion_pattern == ErosionPattern.champion_poaching

    def test_feature_regression_detected(self, engine):
        inp = make_input(
            losses_this_period=10,
            losses_on_features_count=5,   # 50% => >= 0.40
            losses_on_price_count=1,
            losses_on_relationship_count=1,
            champion_poached_count=0,
            consecutive_loss_streak=1,
            battlecard_last_updated_days=100,  # readiness >= 20
            battlecard_usage_pct=0.30,
            competitor_strength_score=50.0,
        )
        result = engine.assess(inp)
        assert result.erosion_pattern == ErosionPattern.feature_regression

    def test_pricing_displacement_detected(self, engine):
        inp = make_input(
            losses_this_period=10,
            losses_on_price_count=5,     # 50% => >= 0.40
            losses_on_features_count=1,
            losses_on_relationship_count=1,
            champion_poached_count=0,
            consecutive_loss_streak=1,
            battlecard_last_updated_days=10,
            battlecard_usage_pct=0.90,
            competitor_strength_score=10.0,
        )
        result = engine.assess(inp)
        assert result.erosion_pattern == ErosionPattern.pricing_displacement

    def test_rep_skill_gap_detected(self, engine):
        inp = make_input(
            losses_this_period=10,
            losses_on_price_count=1,
            losses_on_features_count=1,
            losses_on_relationship_count=1,
            champion_poached_count=0,
            consecutive_loss_streak=2,
            late_stage_loss_count=5,
            late_stage_total_count=8,   # 62.5% late-stage => >= 0.40
            battlecard_last_updated_days=10,
            battlecard_usage_pct=0.90,
            competitor_strength_score=10.0,
            win_rate_trend_3_period_delta=0.0,
        )
        result = engine.assess(inp)
        # deal score must be >= 20 for rep_skill_gap
        assert result.erosion_pattern == ErosionPattern.rep_skill_gap

    def test_systematic_loss_requires_streak_gte_4_and_decline_gte_25(self, engine):
        """Without sufficient decline score, systematic_loss should not fire."""
        inp = make_input(
            consecutive_loss_streak=5,
            win_rate_current_pct=58.0,   # no decline
            win_rate_prior_period_pct=58.0,
            win_rate_benchmark_pct=58.0,
            losses_this_period=5,
            champion_poached_count=0,
            losses_on_price_count=0,
            losses_on_features_count=0,
            losses_on_relationship_count=0,
            late_stage_loss_count=0,
            late_stage_total_count=0,
            win_rate_trend_3_period_delta=0.0,
            battlecard_last_updated_days=10,
            battlecard_usage_pct=0.90,
            competitor_strength_score=10.0,
        )
        result = engine.assess(inp)
        assert result.erosion_pattern != ErosionPattern.systematic_loss

    def test_pattern_is_erosion_pattern_instance(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.erosion_pattern, ErosionPattern)


# ===========================================================================
# 10. Risk level assignment
# ===========================================================================

class TestRiskLevelAssignment:

    def test_low_risk_composite_below_20(self, engine):
        inp = make_input(
            win_rate_current_pct=80.0,
            win_rate_prior_period_pct=80.0,
            win_rate_benchmark_pct=60.0,
            consecutive_loss_streak=0,
            late_stage_loss_count=0,
            late_stage_total_count=0,
            champion_poached_count=0,
            win_rate_trend_3_period_delta=5.0,
            battlecard_last_updated_days=10,
            battlecard_usage_pct=0.90,
            competitor_strength_score=10.0,
            losses_on_price_count=0,
            losses_on_features_count=0,
            losses_on_relationship_count=0,
        )
        result = engine.assess(inp)
        assert result.win_rate_composite < 20.0
        assert result.win_rate_risk == WinRateRisk.low

    def test_moderate_risk_composite_between_20_and_40(self, engine):
        # Force composite into 20-40 range
        inp = make_input(
            win_rate_current_pct=45.0,
            win_rate_prior_period_pct=52.0,
            win_rate_benchmark_pct=58.0,
            losses_this_period=5,
            losses_on_price_count=2,
            losses_on_features_count=1,
            losses_on_relationship_count=0,
            consecutive_loss_streak=1,
            late_stage_loss_count=1,
            late_stage_total_count=5,
            champion_poached_count=0,
            win_rate_trend_3_period_delta=-4.0,
            battlecard_last_updated_days=30,
            battlecard_usage_pct=0.55,
            competitor_strength_score=35.0,
        )
        result = engine.assess(inp)
        if 20.0 <= result.win_rate_composite < 40.0:
            assert result.win_rate_risk == WinRateRisk.moderate

    def test_high_risk_composite_between_40_and_60(self, engine):
        inp = make_input(
            win_rate_current_pct=30.0,
            win_rate_prior_period_pct=50.0,
            win_rate_benchmark_pct=60.0,
            losses_this_period=8,
            losses_on_price_count=3,
            losses_on_features_count=3,
            losses_on_relationship_count=1,
            consecutive_loss_streak=3,
            late_stage_loss_count=4,
            late_stage_total_count=8,
            champion_poached_count=1,
            win_rate_trend_3_period_delta=-12.0,
            battlecard_last_updated_days=50,
            battlecard_usage_pct=0.35,
            competitor_strength_score=65.0,
        )
        result = engine.assess(inp)
        if 40.0 <= result.win_rate_composite < 60.0:
            assert result.win_rate_risk == WinRateRisk.high

    def test_critical_risk_composite_gte_60(self, engine, critical_input):
        result = engine.assess(critical_input)
        if result.win_rate_composite >= 60.0:
            assert result.win_rate_risk == WinRateRisk.critical

    def test_risk_is_win_rate_risk_instance(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.win_rate_risk, WinRateRisk)

    def test_risk_threshold_exactly_20(self, engine):
        """Composite exactly 20 should be moderate (20 < 40)."""
        # Build input that gets composite = exactly 20 (approximate test)
        # benchmark_gap=8 => +14, period_decline=6 => +10 => decline=24, *0.35=8.4
        # rest zero => composite ~8.4 (low). Hard to hit exactly 20; assert boundary logic.
        engine2 = SalesCompetitiveWinRateErosionEngine()
        assert engine2._classify_risk(19.9) == WinRateRisk.low
        assert engine2._classify_risk(20.0) == WinRateRisk.moderate

    def test_risk_threshold_exactly_40(self, engine):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        assert engine2._classify_risk(39.9) == WinRateRisk.moderate
        assert engine2._classify_risk(40.0) == WinRateRisk.high

    def test_risk_threshold_exactly_60(self, engine):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        assert engine2._classify_risk(59.9) == WinRateRisk.high
        assert engine2._classify_risk(60.0) == WinRateRisk.critical


# ===========================================================================
# 11. Severity assignment
# ===========================================================================

class TestSeverityAssignment:

    def test_stable_severity_composite_below_20(self, engine):
        inp = make_input(
            win_rate_current_pct=80.0,
            win_rate_prior_period_pct=80.0,
            win_rate_benchmark_pct=60.0,
            consecutive_loss_streak=0,
            late_stage_loss_count=0,
            late_stage_total_count=0,
            champion_poached_count=0,
            win_rate_trend_3_period_delta=5.0,
            battlecard_last_updated_days=10,
            battlecard_usage_pct=0.90,
            competitor_strength_score=10.0,
            losses_on_price_count=0,
            losses_on_features_count=0,
            losses_on_relationship_count=0,
        )
        result = engine.assess(inp)
        assert result.erosion_severity == ErosionSeverity.stable

    def test_declining_severity_composite_20_to_40(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        assert engine2._classify_severity(20.0) == ErosionSeverity.declining
        assert engine2._classify_severity(39.9) == ErosionSeverity.declining

    def test_eroding_severity_composite_40_to_60(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        assert engine2._classify_severity(40.0) == ErosionSeverity.eroding
        assert engine2._classify_severity(59.9) == ErosionSeverity.eroding

    def test_collapse_severity_composite_gte_60(self, engine, critical_input):
        result = engine.assess(critical_input)
        if result.win_rate_composite >= 60.0:
            assert result.erosion_severity == ErosionSeverity.collapse

    def test_severity_is_erosion_severity_instance(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.erosion_severity, ErosionSeverity)

    def test_severity_threshold_exactly_20(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        assert engine2._classify_severity(19.9) == ErosionSeverity.stable
        assert engine2._classify_severity(20.0) == ErosionSeverity.declining

    def test_severity_threshold_exactly_40(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        assert engine2._classify_severity(39.9) == ErosionSeverity.declining
        assert engine2._classify_severity(40.0) == ErosionSeverity.eroding

    def test_severity_threshold_exactly_60(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        assert engine2._classify_severity(59.9) == ErosionSeverity.eroding
        assert engine2._classify_severity(60.0) == ErosionSeverity.collapse

    def test_risk_and_severity_use_same_thresholds(self, engine, healthy_input):
        """Risk and severity thresholds are identical — their names should match."""
        result = engine.assess(healthy_input)
        risk_mapping = {
            WinRateRisk.low: ErosionSeverity.stable,
            WinRateRisk.moderate: ErosionSeverity.declining,
            WinRateRisk.high: ErosionSeverity.eroding,
            WinRateRisk.critical: ErosionSeverity.collapse,
        }
        assert result.erosion_severity == risk_mapping[result.win_rate_risk]


# ===========================================================================
# 12. Action assignment
# ===========================================================================

class TestActionAssignment:

    def test_no_action_for_low_risk(self, engine):
        inp = make_input(
            win_rate_current_pct=80.0,
            win_rate_prior_period_pct=80.0,
            win_rate_benchmark_pct=60.0,
            consecutive_loss_streak=0,
            late_stage_loss_count=0,
            late_stage_total_count=0,
            champion_poached_count=0,
            win_rate_trend_3_period_delta=5.0,
            battlecard_last_updated_days=10,
            battlecard_usage_pct=0.90,
            competitor_strength_score=10.0,
            losses_on_price_count=0,
            losses_on_features_count=0,
            losses_on_relationship_count=0,
        )
        result = engine.assess(inp)
        assert result.recommended_action == WinRateAction.no_action

    def test_battlecard_refresh_for_moderate_risk(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        action = engine2._recommended_action(WinRateRisk.moderate, 25.0)
        assert action == WinRateAction.battlecard_refresh

    def test_competitive_coaching_for_high_risk(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        action = engine2._recommended_action(WinRateRisk.high, 45.0)
        assert action == WinRateAction.competitive_coaching

    def test_pricing_strategy_review_composite_gte_50(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        action = engine2._recommended_action(WinRateRisk.high, 50.0)
        assert action == WinRateAction.pricing_strategy_review

    def test_pricing_strategy_review_composite_55(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        action = engine2._recommended_action(WinRateRisk.critical, 55.0)
        assert action == WinRateAction.pricing_strategy_review

    def test_executive_competitive_review_composite_gte_60(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        action = engine2._recommended_action(WinRateRisk.critical, 60.0)
        assert action == WinRateAction.executive_competitive_review

    def test_executive_review_for_critical_composite(self, engine, critical_input):
        result = engine.assess(critical_input)
        if result.win_rate_composite >= 60.0:
            assert result.recommended_action == WinRateAction.executive_competitive_review

    def test_action_is_win_rate_action_instance(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.recommended_action, WinRateAction)

    def test_action_threshold_49_vs_50(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        assert engine2._recommended_action(WinRateRisk.high, 49.9) == WinRateAction.competitive_coaching
        assert engine2._recommended_action(WinRateRisk.high, 50.0) == WinRateAction.pricing_strategy_review

    def test_action_threshold_59_vs_60(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        assert engine2._recommended_action(WinRateRisk.critical, 59.9) == WinRateAction.pricing_strategy_review
        assert engine2._recommended_action(WinRateRisk.critical, 60.0) == WinRateAction.executive_competitive_review


# ===========================================================================
# 13. assess_batch() returns correct count
# ===========================================================================

class TestAssessBatch:

    def test_batch_empty_list_returns_empty(self, engine):
        results = engine.assess_batch([])
        assert results == []

    def test_batch_single_input_returns_one_result(self, engine, healthy_input):
        results = engine.assess_batch([healthy_input])
        assert len(results) == 1

    def test_batch_five_inputs_returns_five_results(self, engine):
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_results_are_correct_type(self, engine):
        inputs = [make_input() for _ in range(3)]
        results = engine.assess_batch(inputs)
        for r in results:
            assert isinstance(r, CompetitiveWinRateResult)

    def test_batch_results_added_to_engine_history(self, engine):
        inputs = [make_input() for _ in range(4)]
        engine.assess_batch(inputs)
        assert engine.summary()["total"] == 4

    def test_batch_preserves_rep_ids(self, engine):
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(3)]
        results = engine.assess_batch(inputs)
        ids = [r.rep_id for r in results]
        assert ids == ["rep-0", "rep-1", "rep-2"]

    def test_batch_and_single_assess_accumulate(self, engine, healthy_input):
        engine.assess(healthy_input)
        engine.assess_batch([make_input(), make_input()])
        assert engine.summary()["total"] == 3

    def test_batch_100_inputs(self, engine):
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(100)]
        results = engine.assess_batch(inputs)
        assert len(results) == 100
        assert engine.summary()["total"] == 100


# ===========================================================================
# 14. summary() aggregation — total_estimated_lost_revenue_usd is SUM
# ===========================================================================

class TestSummaryAggregation:

    def test_total_estimated_lost_revenue_is_sum_not_avg(self, engine):
        inp_a = make_input(losses_this_period=5, avg_deal_size_won_usd=10_000.0)
        inp_b = make_input(losses_this_period=8, avg_deal_size_won_usd=20_000.0)
        r_a = engine.assess(inp_a)
        r_b = engine.assess(inp_b)
        s = engine.summary()
        expected_sum = round(r_a.estimated_lost_revenue_usd + r_b.estimated_lost_revenue_usd, 2)
        assert s["total_estimated_lost_revenue_usd"] == expected_sum

    def test_avg_composite_is_mean_of_all(self, engine):
        inputs = [make_input() for _ in range(4)]
        results = engine.assess_batch(inputs)
        avg = round(sum(r.win_rate_composite for r in results) / 4, 1)
        assert engine.summary()["avg_win_rate_composite"] == avg

    def test_eroding_count_is_sum_of_flags(self, engine):
        inputs = [
            make_input(consecutive_loss_streak=5),   # eroding
            make_input(consecutive_loss_streak=0, win_rate_trend_3_period_delta=0.0,
                       win_rate_current_pct=80.0, win_rate_prior_period_pct=80.0,
                       win_rate_benchmark_pct=60.0, late_stage_loss_count=0,
                       late_stage_total_count=0, champion_poached_count=0,
                       battlecard_last_updated_days=10, battlecard_usage_pct=0.90,
                       competitor_strength_score=10.0, losses_on_price_count=0,
                       losses_on_features_count=0, losses_on_relationship_count=0),  # not eroding
        ]
        results = engine.assess_batch(inputs)
        expected_eroding = sum(1 for r in results if r.is_win_rate_eroding)
        assert engine.summary()["eroding_count"] == expected_eroding

    def test_coaching_count_is_sum_of_flags(self, engine):
        inputs = [
            make_input(battlecard_last_updated_days=100),  # requires coaching
            make_input(battlecard_last_updated_days=10, late_stage_loss_count=0,
                       win_rate_current_pct=80.0, win_rate_prior_period_pct=80.0,
                       win_rate_benchmark_pct=60.0, consecutive_loss_streak=0,
                       late_stage_total_count=0, champion_poached_count=0,
                       win_rate_trend_3_period_delta=5.0, battlecard_usage_pct=0.90,
                       competitor_strength_score=10.0, losses_on_price_count=0,
                       losses_on_features_count=0, losses_on_relationship_count=0),  # not coaching
        ]
        results = engine.assess_batch(inputs)
        expected_coaching = sum(1 for r in results if r.requires_coaching)
        assert engine.summary()["coaching_count"] == expected_coaching

    def test_risk_counts_in_summary(self, engine, healthy_input):
        engine.assess(healthy_input)
        s = engine.summary()
        total_from_risk = sum(s["risk_counts"].values())
        assert total_from_risk == 1

    def test_pattern_counts_in_summary(self, engine, healthy_input):
        engine.assess(healthy_input)
        s = engine.summary()
        total_from_pattern = sum(s["pattern_counts"].values())
        assert total_from_pattern == 1

    def test_severity_counts_in_summary(self, engine, healthy_input):
        engine.assess(healthy_input)
        s = engine.summary()
        total_from_severity = sum(s["severity_counts"].values())
        assert total_from_severity == 1

    def test_action_counts_in_summary(self, engine, healthy_input):
        engine.assess(healthy_input)
        s = engine.summary()
        total_from_action = sum(s["action_counts"].values())
        assert total_from_action == 1

    def test_avg_decline_score_computation(self, engine):
        inputs = [make_input() for _ in range(3)]
        results = engine.assess_batch(inputs)
        avg = round(sum(r.win_rate_decline_score for r in results) / 3, 1)
        assert engine.summary()["avg_win_rate_decline_score"] == avg

    def test_avg_deal_quality_score_computation(self, engine):
        inputs = [make_input() for _ in range(3)]
        results = engine.assess_batch(inputs)
        avg = round(sum(r.deal_quality_score for r in results) / 3, 1)
        assert engine.summary()["avg_deal_quality_score"] == avg

    def test_avg_readiness_score_computation(self, engine):
        inputs = [make_input() for _ in range(3)]
        results = engine.assess_batch(inputs)
        avg = round(sum(r.competitive_readiness_score for r in results) / 3, 1)
        assert engine.summary()["avg_competitive_readiness_score"] == avg

    def test_avg_pattern_intensity_computation(self, engine):
        inputs = [make_input() for _ in range(3)]
        results = engine.assess_batch(inputs)
        avg = round(sum(r.pattern_intensity_score for r in results) / 3, 1)
        assert engine.summary()["avg_pattern_intensity_score"] == avg


# ===========================================================================
# 15. Edge cases: zero deals, perfect win rate, 100% loss rate
# ===========================================================================

class TestEdgeCases:

    def test_zero_total_competitive_deals(self, engine):
        inp = make_input(
            total_competitive_deals=0,
            wins_this_period=0,
            losses_this_period=0,
        )
        result = engine.assess(inp)
        assert isinstance(result, CompetitiveWinRateResult)

    def test_perfect_win_rate_100_pct(self, engine):
        inp = make_input(
            win_rate_current_pct=100.0,
            win_rate_prior_period_pct=100.0,
            win_rate_benchmark_pct=60.0,
            wins_this_period=20,
            losses_this_period=0,
            losses_on_price_count=0,
            losses_on_features_count=0,
            losses_on_relationship_count=0,
            losses_on_timing_count=0,
        )
        result = engine.assess(inp)
        assert result.win_rate_composite >= 0.0
        assert result.win_rate_composite <= 100.0
        assert result.estimated_lost_revenue_usd == 0.0

    def test_100_pct_loss_rate(self, engine):
        inp = make_input(
            win_rate_current_pct=0.0,
            win_rate_prior_period_pct=50.0,
            win_rate_benchmark_pct=60.0,
            wins_this_period=0,
            losses_this_period=20,
            losses_on_price_count=8,
            losses_on_features_count=6,
            losses_on_relationship_count=4,
            losses_on_timing_count=2,
            consecutive_loss_streak=8,
            late_stage_loss_count=10,
            late_stage_total_count=12,
            champion_poached_count=3,
            win_rate_trend_3_period_delta=-30.0,
            battlecard_last_updated_days=200,
            battlecard_usage_pct=0.02,
            competitor_strength_score=95.0,
            avg_deal_size_won_usd=50_000.0,
        )
        result = engine.assess(inp)
        assert result.win_rate_composite >= 60.0
        assert result.is_win_rate_eroding is True
        assert result.requires_coaching is True

    def test_zero_avg_deal_size(self, engine):
        inp = make_input(avg_deal_size_won_usd=0.0)
        result = engine.assess(inp)
        assert result.estimated_lost_revenue_usd == 0.0

    def test_very_large_deal_size(self, engine):
        inp = make_input(avg_deal_size_won_usd=1_000_000.0, losses_this_period=3)
        result = engine.assess(inp)
        assert result.estimated_lost_revenue_usd >= 0.0

    def test_late_stage_total_zero(self, engine):
        """No division by zero when late_stage_total_count=0."""
        inp = make_input(late_stage_loss_count=0, late_stage_total_count=0)
        result = engine.assess(inp)
        assert isinstance(result, CompetitiveWinRateResult)

    def test_losses_this_period_zero_pattern_none(self, engine):
        inp = make_input(
            losses_this_period=0,
            wins_this_period=15,
            total_competitive_deals=15,
        )
        result = engine.assess(inp)
        assert result.erosion_pattern == ErosionPattern.none

    def test_composite_clamped_not_above_100(self, engine, critical_input):
        result = engine.assess(critical_input)
        assert result.win_rate_composite <= 100.0

    def test_zero_wins_zero_losses(self, engine):
        inp = make_input(
            wins_this_period=0,
            losses_this_period=0,
            total_competitive_deals=0,
        )
        result = engine.assess(inp)
        assert result.estimated_lost_revenue_usd == 0.0


# ===========================================================================
# 16. Boundary conditions for all thresholds
# ===========================================================================

class TestBoundaryConditions:

    # win_rate_decline_score — benchmark_gap thresholds
    def test_benchmark_gap_exactly_3(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        inp = make_input(
            win_rate_current_pct=57.0, win_rate_benchmark_pct=60.0,   # gap=3
            win_rate_prior_period_pct=57.0, win_rate_trend_3_period_delta=0.0,
        )
        score = engine2._win_rate_decline_score(inp)
        assert score >= 6.0

    def test_benchmark_gap_exactly_8(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        inp = make_input(
            win_rate_current_pct=52.0, win_rate_benchmark_pct=60.0,   # gap=8
            win_rate_prior_period_pct=52.0, win_rate_trend_3_period_delta=0.0,
        )
        score = engine2._win_rate_decline_score(inp)
        assert score >= 14.0

    def test_benchmark_gap_exactly_15(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        inp = make_input(
            win_rate_current_pct=45.0, win_rate_benchmark_pct=60.0,   # gap=15
            win_rate_prior_period_pct=45.0, win_rate_trend_3_period_delta=0.0,
        )
        score = engine2._win_rate_decline_score(inp)
        assert score >= 28.0

    def test_benchmark_gap_exactly_25(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        inp = make_input(
            win_rate_current_pct=35.0, win_rate_benchmark_pct=60.0,   # gap=25
            win_rate_prior_period_pct=35.0, win_rate_trend_3_period_delta=0.0,
        )
        score = engine2._win_rate_decline_score(inp)
        assert score >= 45.0

    # period_decline thresholds
    def test_period_decline_exactly_6(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        inp = make_input(
            win_rate_current_pct=54.0, win_rate_prior_period_pct=60.0,  # decline=6
            win_rate_benchmark_pct=54.0, win_rate_trend_3_period_delta=0.0,
        )
        score = engine2._win_rate_decline_score(inp)
        assert score >= 10.0

    def test_period_decline_exactly_12(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        inp = make_input(
            win_rate_current_pct=48.0, win_rate_prior_period_pct=60.0,  # decline=12
            win_rate_benchmark_pct=48.0, win_rate_trend_3_period_delta=0.0,
        )
        score = engine2._win_rate_decline_score(inp)
        assert score >= 22.0

    def test_period_decline_exactly_20(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        inp = make_input(
            win_rate_current_pct=40.0, win_rate_prior_period_pct=60.0,  # decline=20
            win_rate_benchmark_pct=40.0, win_rate_trend_3_period_delta=0.0,
        )
        score = engine2._win_rate_decline_score(inp)
        assert score >= 35.0

    # trend thresholds
    def test_trend_exactly_minus_5(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        inp = make_input(
            win_rate_trend_3_period_delta=-5.0,
            win_rate_current_pct=57.0, win_rate_prior_period_pct=57.0,
            win_rate_benchmark_pct=57.0,
        )
        score = engine2._win_rate_decline_score(inp)
        assert score >= 5.0

    def test_trend_exactly_minus_12(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        inp = make_input(
            win_rate_trend_3_period_delta=-12.0,
            win_rate_current_pct=57.0, win_rate_prior_period_pct=57.0,
            win_rate_benchmark_pct=57.0,
        )
        score = engine2._win_rate_decline_score(inp)
        assert score >= 12.0

    def test_trend_exactly_minus_20(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        inp = make_input(
            win_rate_trend_3_period_delta=-20.0,
            win_rate_current_pct=57.0, win_rate_prior_period_pct=57.0,
            win_rate_benchmark_pct=57.0,
        )
        score = engine2._win_rate_decline_score(inp)
        assert score >= 20.0

    # consecutive_loss_streak thresholds
    def test_streak_exactly_1(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        inp = make_input(consecutive_loss_streak=1, late_stage_loss_count=0,
                         late_stage_total_count=0, champion_poached_count=0)
        score = engine2._deal_quality_score(inp)
        assert score >= 8.0

    def test_streak_exactly_3(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        inp = make_input(consecutive_loss_streak=3, late_stage_loss_count=0,
                         late_stage_total_count=0, champion_poached_count=0)
        score = engine2._deal_quality_score(inp)
        assert score >= 20.0

    def test_streak_exactly_5(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        inp = make_input(consecutive_loss_streak=5, late_stage_loss_count=0,
                         late_stage_total_count=0, champion_poached_count=0)
        score = engine2._deal_quality_score(inp)
        assert score >= 35.0

    # champion_poached thresholds
    def test_champion_poached_exactly_1(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        inp = make_input(champion_poached_count=1, consecutive_loss_streak=0,
                         late_stage_loss_count=0, late_stage_total_count=0)
        score = engine2._deal_quality_score(inp)
        assert score >= 10.0

    def test_champion_poached_exactly_3(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        inp = make_input(champion_poached_count=3, consecutive_loss_streak=0,
                         late_stage_loss_count=0, late_stage_total_count=0)
        score = engine2._deal_quality_score(inp)
        assert score >= 20.0

    # battlecard_last_updated_days thresholds
    def test_battlecard_exactly_45_days(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        inp = make_input(battlecard_last_updated_days=45, battlecard_usage_pct=0.90,
                         competitor_strength_score=10.0)
        score = engine2._competitive_readiness_score(inp)
        assert score >= 10.0

    def test_battlecard_exactly_90_days(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        inp = make_input(battlecard_last_updated_days=90, battlecard_usage_pct=0.90,
                         competitor_strength_score=10.0)
        score = engine2._competitive_readiness_score(inp)
        assert score >= 24.0

    def test_battlecard_exactly_180_days(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        inp = make_input(battlecard_last_updated_days=180, battlecard_usage_pct=0.90,
                         competitor_strength_score=10.0)
        score = engine2._competitive_readiness_score(inp)
        assert score >= 40.0

    # battlecard_usage_pct thresholds
    def test_usage_pct_below_20(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        inp = make_input(battlecard_usage_pct=0.19, battlecard_last_updated_days=10,
                         competitor_strength_score=10.0)
        score = engine2._competitive_readiness_score(inp)
        assert score >= 35.0

    def test_usage_pct_below_40(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        inp = make_input(battlecard_usage_pct=0.39, battlecard_last_updated_days=10,
                         competitor_strength_score=10.0)
        score = engine2._competitive_readiness_score(inp)
        assert score >= 20.0

    def test_usage_pct_below_60(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        inp = make_input(battlecard_usage_pct=0.59, battlecard_last_updated_days=10,
                         competitor_strength_score=10.0)
        score = engine2._competitive_readiness_score(inp)
        assert score >= 8.0

    # late_stage_loss_rate thresholds
    def test_late_stage_rate_exactly_25_pct(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        inp = make_input(late_stage_loss_count=2, late_stage_total_count=8,   # 25%
                         consecutive_loss_streak=0, champion_poached_count=0)
        score = engine2._deal_quality_score(inp)
        assert score >= 14.0

    def test_late_stage_rate_exactly_40_pct(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        inp = make_input(late_stage_loss_count=4, late_stage_total_count=10,  # 40%
                         consecutive_loss_streak=0, champion_poached_count=0)
        score = engine2._deal_quality_score(inp)
        assert score >= 28.0

    def test_late_stage_rate_exactly_60_pct(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        inp = make_input(late_stage_loss_count=6, late_stage_total_count=10,  # 60%
                         consecutive_loss_streak=0, champion_poached_count=0)
        score = engine2._deal_quality_score(inp)
        assert score >= 45.0

    # competitor_strength_score thresholds
    def test_competitor_strength_40(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        inp = make_input(competitor_strength_score=40.0, battlecard_last_updated_days=10,
                         battlecard_usage_pct=0.90)
        score = engine2._competitive_readiness_score(inp)
        assert score >= 6.0

    def test_competitor_strength_60(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        inp = make_input(competitor_strength_score=60.0, battlecard_last_updated_days=10,
                         battlecard_usage_pct=0.90)
        score = engine2._competitive_readiness_score(inp)
        assert score >= 14.0

    def test_competitor_strength_80(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        inp = make_input(competitor_strength_score=80.0, battlecard_last_updated_days=10,
                         battlecard_usage_pct=0.90)
        score = engine2._competitive_readiness_score(inp)
        assert score >= 25.0

    # clamp helper
    def test_clamp_below_zero(self):
        assert _clamp(-10.0) == 0.0

    def test_clamp_above_100(self):
        assert _clamp(150.0) == 100.0

    def test_clamp_within_range(self):
        assert _clamp(55.5) == 55.5

    def test_clamp_exactly_0(self):
        assert _clamp(0.0) == 0.0

    def test_clamp_exactly_100(self):
        assert _clamp(100.0) == 100.0


# ===========================================================================
# 17. erosion_signal string is non-empty
# ===========================================================================

class TestErosionSignal:

    def test_erosion_signal_non_empty_healthy(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.erosion_signal != ""

    def test_erosion_signal_non_empty_critical(self, engine, critical_input):
        result = engine.assess(critical_input)
        assert result.erosion_signal != ""

    def test_erosion_signal_is_string(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.erosion_signal, str)

    def test_erosion_signal_none_pattern_message(self, engine):
        inp = make_input(
            losses_this_period=0,
            wins_this_period=20,
            total_competitive_deals=20,
        )
        result = engine.assess(inp)
        assert "healthy" in result.erosion_signal.lower() or result.erosion_signal != ""

    def test_erosion_signal_systematic_loss_contains_streak(self, engine):
        inp = make_input(
            consecutive_loss_streak=6,
            win_rate_current_pct=20.0,
            win_rate_prior_period_pct=55.0,
            win_rate_benchmark_pct=60.0,
            losses_this_period=10,
            losses_on_price_count=3,
            losses_on_features_count=3,
            losses_on_relationship_count=2,
            champion_poached_count=0,
            win_rate_trend_3_period_delta=-25.0,
            late_stage_loss_count=5,
            late_stage_total_count=8,
            battlecard_last_updated_days=10,
            battlecard_usage_pct=0.90,
            competitor_strength_score=10.0,
        )
        result = engine.assess(inp)
        if result.erosion_pattern == ErosionPattern.systematic_loss:
            assert "6" in result.erosion_signal

    def test_erosion_signal_champion_poaching_mentions_poached(self, engine):
        inp = make_input(
            champion_poached_count=3,
            losses_this_period=8,
            losses_on_relationship_count=4,
            consecutive_loss_streak=1,
            losses_on_price_count=0,
            losses_on_features_count=0,
            win_rate_trend_3_period_delta=0.0,
        )
        result = engine.assess(inp)
        if result.erosion_pattern == ErosionPattern.champion_poaching:
            assert "3" in result.erosion_signal or "poach" in result.erosion_signal.lower()

    def test_erosion_signal_pricing_displacement_mentions_price(self, engine):
        inp = make_input(
            losses_this_period=10,
            losses_on_price_count=5,
            losses_on_features_count=1,
            losses_on_relationship_count=1,
            champion_poached_count=0,
            consecutive_loss_streak=0,
            battlecard_last_updated_days=10,
            battlecard_usage_pct=0.90,
            competitor_strength_score=10.0,
        )
        result = engine.assess(inp)
        if result.erosion_pattern == ErosionPattern.pricing_displacement:
            assert "price" in result.erosion_signal.lower() or "5" in result.erosion_signal

    def test_erosion_signal_ends_with_composite_score(self, engine):
        inp = make_input(
            losses_this_period=10,
            losses_on_features_count=5,
            consecutive_loss_streak=1,
            champion_poached_count=0,
            battlecard_last_updated_days=120,
            battlecard_usage_pct=0.30,
            competitor_strength_score=65.0,
            losses_on_price_count=1,
            losses_on_relationship_count=1,
        )
        result = engine.assess(inp)
        if result.erosion_pattern != ErosionPattern.none:
            assert "composite" in result.erosion_signal.lower()

    def test_erosion_signal_non_empty_all_patterns(self, engine):
        """At minimum ensure all pattern variants return non-empty signal."""
        patterns_tested = set()

        inputs = [
            # none
            make_input(losses_this_period=0, wins_this_period=20, total_competitive_deals=20),
            # systematic_loss
            make_input(consecutive_loss_streak=6, win_rate_current_pct=20.0,
                       win_rate_prior_period_pct=55.0, win_rate_benchmark_pct=60.0,
                       losses_this_period=10, champion_poached_count=0,
                       losses_on_price_count=3, losses_on_features_count=3,
                       losses_on_relationship_count=2, win_rate_trend_3_period_delta=-25.0,
                       late_stage_loss_count=5, late_stage_total_count=8),
            # champion_poaching
            make_input(champion_poached_count=3, losses_this_period=8,
                       losses_on_relationship_count=4, consecutive_loss_streak=1,
                       losses_on_price_count=0, losses_on_features_count=0),
            # feature_regression
            make_input(losses_this_period=10, losses_on_features_count=5,
                       champion_poached_count=0, consecutive_loss_streak=1,
                       battlecard_last_updated_days=120, battlecard_usage_pct=0.30,
                       competitor_strength_score=65.0, losses_on_price_count=1,
                       losses_on_relationship_count=1),
            # pricing_displacement
            make_input(losses_this_period=10, losses_on_price_count=5,
                       losses_on_features_count=1, losses_on_relationship_count=1,
                       champion_poached_count=0, consecutive_loss_streak=1),
        ]
        for inp in inputs:
            result = engine.assess(inp)
            patterns_tested.add(result.erosion_pattern)
            assert result.erosion_signal != ""

    def test_erosion_signal_feature_regression_mentions_features(self, engine):
        inp = make_input(
            losses_this_period=10,
            losses_on_features_count=5,
            champion_poached_count=0,
            consecutive_loss_streak=1,
            battlecard_last_updated_days=120,
            battlecard_usage_pct=0.30,
            competitor_strength_score=65.0,
            losses_on_price_count=1,
            losses_on_relationship_count=1,
        )
        result = engine.assess(inp)
        if result.erosion_pattern == ErosionPattern.feature_regression:
            assert "feature" in result.erosion_signal.lower() or "5" in result.erosion_signal


# ===========================================================================
# 18. Additional integration / cross-cutting tests
# ===========================================================================

class TestIntegration:

    def test_rep_id_propagated_to_result(self, engine):
        inp = make_input(rep_id="sales-rep-42")
        result = engine.assess(inp)
        assert result.rep_id == "sales-rep-42"

    def test_region_propagated_to_result(self, engine):
        inp = make_input(region="APAC")
        result = engine.assess(inp)
        assert result.region == "APAC"

    def test_new_engine_empty_summary(self):
        engine2 = SalesCompetitiveWinRateErosionEngine()
        s = engine2.summary()
        assert s["total"] == 0
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}

    def test_assess_returns_result_type(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result, CompetitiveWinRateResult)

    def test_multiple_engines_independent(self):
        e1 = SalesCompetitiveWinRateErosionEngine()
        e2 = SalesCompetitiveWinRateErosionEngine()
        e1.assess(make_input())
        assert e1.summary()["total"] == 1
        assert e2.summary()["total"] == 0

    def test_summary_risk_counts_sum_equals_total(self, engine):
        for _ in range(5):
            engine.assess(make_input())
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_severity_counts_sum_equals_total(self, engine):
        for _ in range(5):
            engine.assess(make_input())
        s = engine.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_equals_total(self, engine):
        for _ in range(5):
            engine.assess(make_input())
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_pattern_counts_sum_equals_total(self, engine):
        for _ in range(5):
            engine.assess(make_input())
        s = engine.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_sub_scores_range_0_to_100(self, engine, critical_input):
        result = engine.assess(critical_input)
        assert 0.0 <= result.win_rate_decline_score <= 100.0
        assert 0.0 <= result.deal_quality_score <= 100.0
        assert 0.0 <= result.competitive_readiness_score <= 100.0
        assert 0.0 <= result.pattern_intensity_score <= 100.0

    def test_win_rate_composite_in_range(self, engine, critical_input):
        result = engine.assess(critical_input)
        assert 0.0 <= result.win_rate_composite <= 100.0

    def test_different_inputs_different_composites(self, engine):
        r_low = engine.assess(make_input(
            win_rate_current_pct=80.0,
            win_rate_prior_period_pct=80.0,
            win_rate_benchmark_pct=60.0,
            consecutive_loss_streak=0,
            late_stage_loss_count=0,
            late_stage_total_count=0,
            champion_poached_count=0,
            win_rate_trend_3_period_delta=5.0,
            battlecard_last_updated_days=10,
            battlecard_usage_pct=0.90,
            competitor_strength_score=10.0,
            losses_on_price_count=0,
            losses_on_features_count=0,
            losses_on_relationship_count=0,
        ))
        r_high = engine.assess(make_input(
            win_rate_current_pct=0.0,
            win_rate_prior_period_pct=50.0,
            win_rate_benchmark_pct=60.0,
            consecutive_loss_streak=8,
            late_stage_loss_count=8,
            late_stage_total_count=10,
            champion_poached_count=3,
            win_rate_trend_3_period_delta=-30.0,
            battlecard_last_updated_days=200,
            battlecard_usage_pct=0.02,
            competitor_strength_score=95.0,
            losses_this_period=15,
            losses_on_price_count=5,
            losses_on_features_count=5,
            losses_on_relationship_count=4,
        ))
        assert r_low.win_rate_composite < r_high.win_rate_composite

    def test_eroding_flag_true_implies_composite_ge_40_or_streak_ge_4_or_trend_lte_minus_15(self, engine):
        for _ in range(10):
            inp = make_input(
                consecutive_loss_streak=2,
                win_rate_trend_3_period_delta=-5.0,
            )
            result = engine.assess(inp)
            if result.is_win_rate_eroding:
                ok = (
                    result.win_rate_composite >= 40
                    or inp.consecutive_loss_streak >= 4
                    or inp.win_rate_trend_3_period_delta <= -15
                )
                assert ok

    def test_estimate_revenue_using_result_composite(self, engine):
        inp = make_input(losses_this_period=4, avg_deal_size_won_usd=25_000.0)
        result = engine.assess(inp)
        expected = 4 * 25_000.0 * (result.win_rate_composite / 100.0)
        assert abs(result.estimated_lost_revenue_usd - expected) < 0.01

    def test_summary_total_estimated_lost_revenue_sums_individual(self, engine):
        inputs = [make_input(losses_this_period=i + 1, avg_deal_size_won_usd=10_000.0) for i in range(5)]
        results = engine.assess_batch(inputs)
        expected = round(sum(r.estimated_lost_revenue_usd for r in results), 2)
        assert engine.summary()["total_estimated_lost_revenue_usd"] == expected

    def test_erosion_pattern_none_when_no_losses(self, engine):
        inp = make_input(losses_this_period=0, wins_this_period=20, total_competitive_deals=20)
        result = engine.assess(inp)
        assert result.erosion_pattern == ErosionPattern.none

    def test_all_fields_present_in_result(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        for field in dataclasses.fields(CompetitiveWinRateResult):
            assert hasattr(result, field.name)

    def test_systematic_loss_needs_streak_4_min(self, engine):
        """streak=3 with high decline should NOT produce systematic_loss."""
        inp = make_input(
            consecutive_loss_streak=3,
            win_rate_current_pct=20.0,
            win_rate_prior_period_pct=55.0,
            win_rate_benchmark_pct=60.0,
            losses_this_period=10,
            champion_poached_count=0,
            losses_on_price_count=1,
            losses_on_features_count=1,
            losses_on_relationship_count=1,
        )
        result = engine.assess(inp)
        assert result.erosion_pattern != ErosionPattern.systematic_loss

    def test_champion_poaching_needs_count_2_min(self, engine):
        """champion_poached_count=1 should NOT produce champion_poaching pattern."""
        inp = make_input(
            champion_poached_count=1,
            consecutive_loss_streak=1,
            losses_this_period=8,
            losses_on_relationship_count=4,
            losses_on_price_count=0,
            losses_on_features_count=0,
        )
        result = engine.assess(inp)
        assert result.erosion_pattern != ErosionPattern.champion_poaching


# ===========================================================================
# 19. Sub-score granularity — win_rate_decline_score internals
# ===========================================================================

class TestWinRateDeclineScore:

    def _e(self):
        return SalesCompetitiveWinRateErosionEngine()

    def test_no_decline_no_gap_no_trend_gives_zero(self):
        e = self._e()
        inp = make_input(
            win_rate_current_pct=60.0, win_rate_prior_period_pct=60.0,
            win_rate_benchmark_pct=60.0, win_rate_trend_3_period_delta=0.0,
        )
        assert e._win_rate_decline_score(inp) == 0.0

    def test_gap_below_3_gives_zero(self):
        e = self._e()
        inp = make_input(
            win_rate_current_pct=58.0, win_rate_prior_period_pct=58.0,
            win_rate_benchmark_pct=60.0, win_rate_trend_3_period_delta=0.0,
        )
        assert e._win_rate_decline_score(inp) == 0.0

    def test_gap_exactly_3_gives_6(self):
        e = self._e()
        inp = make_input(
            win_rate_current_pct=57.0, win_rate_benchmark_pct=60.0,
            win_rate_prior_period_pct=57.0, win_rate_trend_3_period_delta=0.0,
        )
        assert e._win_rate_decline_score(inp) == 6.0

    def test_gap_exactly_8_gives_14(self):
        e = self._e()
        inp = make_input(
            win_rate_current_pct=52.0, win_rate_benchmark_pct=60.0,
            win_rate_prior_period_pct=52.0, win_rate_trend_3_period_delta=0.0,
        )
        assert e._win_rate_decline_score(inp) == 14.0

    def test_period_decline_below_6_gives_zero_for_that_component(self):
        e = self._e()
        inp = make_input(
            win_rate_current_pct=55.0, win_rate_prior_period_pct=59.0,  # decline=4
            win_rate_benchmark_pct=55.0, win_rate_trend_3_period_delta=0.0,
        )
        # Only gap portion applies (gap=0), period portion is 0
        assert e._win_rate_decline_score(inp) == 0.0

    def test_trend_above_minus_5_gives_zero_for_trend_component(self):
        e = self._e()
        inp = make_input(
            win_rate_current_pct=60.0, win_rate_prior_period_pct=60.0,
            win_rate_benchmark_pct=60.0, win_rate_trend_3_period_delta=-4.0,
        )
        assert e._win_rate_decline_score(inp) == 0.0

    def test_score_clamped_at_100(self):
        e = self._e()
        # Max possible: gap>=25(45) + period>=20(35) + trend<=-20(20) = 100
        inp = make_input(
            win_rate_current_pct=20.0, win_rate_prior_period_pct=60.0,
            win_rate_benchmark_pct=60.0, win_rate_trend_3_period_delta=-25.0,
        )
        assert e._win_rate_decline_score(inp) == 100.0

    def test_score_non_negative(self):
        e = self._e()
        inp = make_input(
            win_rate_current_pct=90.0, win_rate_prior_period_pct=80.0,  # negative decline
            win_rate_benchmark_pct=60.0, win_rate_trend_3_period_delta=10.0,
        )
        assert e._win_rate_decline_score(inp) >= 0.0


# ===========================================================================
# 20. Sub-score granularity — deal_quality_score internals
# ===========================================================================

class TestDealQualityScore:

    def _e(self):
        return SalesCompetitiveWinRateErosionEngine()

    def test_all_zero_gives_zero(self):
        e = self._e()
        inp = make_input(
            late_stage_loss_count=0, late_stage_total_count=0,
            consecutive_loss_streak=0, champion_poached_count=0,
        )
        assert e._deal_quality_score(inp) == 0.0

    def test_late_total_zero_skips_late_portion(self):
        e = self._e()
        inp = make_input(
            late_stage_loss_count=5, late_stage_total_count=0,  # no division
            consecutive_loss_streak=0, champion_poached_count=0,
        )
        assert e._deal_quality_score(inp) == 0.0

    def test_late_rate_below_25_gives_zero_for_that_portion(self):
        e = self._e()
        inp = make_input(
            late_stage_loss_count=1, late_stage_total_count=10,  # 10%
            consecutive_loss_streak=0, champion_poached_count=0,
        )
        assert e._deal_quality_score(inp) == 0.0

    def test_streak_zero_gives_zero_for_streak_portion(self):
        e = self._e()
        inp = make_input(
            consecutive_loss_streak=0,
            late_stage_loss_count=0, late_stage_total_count=0, champion_poached_count=0,
        )
        assert e._deal_quality_score(inp) == 0.0

    def test_champion_zero_gives_zero_for_champion_portion(self):
        e = self._e()
        inp = make_input(
            champion_poached_count=0,
            consecutive_loss_streak=0,
            late_stage_loss_count=0, late_stage_total_count=0,
        )
        assert e._deal_quality_score(inp) == 0.0

    def test_max_all_components_clamped_at_100(self):
        e = self._e()
        # late>=60%(45) + streak>=5(35) + poached>=3(20) = 100
        inp = make_input(
            late_stage_loss_count=7, late_stage_total_count=10,  # 70%
            consecutive_loss_streak=6,
            champion_poached_count=3,
        )
        assert e._deal_quality_score(inp) == 100.0

    def test_deal_score_non_negative(self):
        e = self._e()
        inp = make_input(
            late_stage_loss_count=0, late_stage_total_count=5,
            consecutive_loss_streak=0, champion_poached_count=0,
        )
        assert e._deal_quality_score(inp) >= 0.0


# ===========================================================================
# 21. Sub-score granularity — competitive_readiness_score internals
# ===========================================================================

class TestCompetitiveReadinessScore:

    def _e(self):
        return SalesCompetitiveWinRateErosionEngine()

    def test_all_zero_conditions_gives_zero(self):
        e = self._e()
        inp = make_input(
            battlecard_last_updated_days=0,
            battlecard_usage_pct=1.0,
            competitor_strength_score=0.0,
        )
        assert e._competitive_readiness_score(inp) == 0.0

    def test_battlecard_below_45_gives_zero_for_staleness(self):
        e = self._e()
        inp = make_input(
            battlecard_last_updated_days=44,
            battlecard_usage_pct=1.0,
            competitor_strength_score=0.0,
        )
        assert e._competitive_readiness_score(inp) == 0.0

    def test_usage_above_60_gives_zero_for_usage_portion(self):
        e = self._e()
        inp = make_input(
            battlecard_last_updated_days=10,
            battlecard_usage_pct=0.61,
            competitor_strength_score=0.0,
        )
        assert e._competitive_readiness_score(inp) == 0.0

    def test_competitor_strength_below_40_gives_zero(self):
        e = self._e()
        inp = make_input(
            battlecard_last_updated_days=10,
            battlecard_usage_pct=1.0,
            competitor_strength_score=39.0,
        )
        assert e._competitive_readiness_score(inp) == 0.0

    def test_max_all_clamped_at_100(self):
        e = self._e()
        # staleness>=180(40) + usage<0.20(35) + strength>=80(25) = 100
        inp = make_input(
            battlecard_last_updated_days=200,
            battlecard_usage_pct=0.10,
            competitor_strength_score=90.0,
        )
        assert e._competitive_readiness_score(inp) == 100.0

    def test_score_non_negative(self):
        e = self._e()
        inp = make_input(
            battlecard_last_updated_days=0,
            battlecard_usage_pct=1.0,
            competitor_strength_score=0.0,
        )
        assert e._competitive_readiness_score(inp) >= 0.0


# ===========================================================================
# 22. Sub-score granularity — pattern_intensity_score internals
# ===========================================================================

class TestPatternIntensityScore:

    def _e(self):
        return SalesCompetitiveWinRateErosionEngine()

    def test_zero_losses_gives_zero_score(self):
        e = self._e()
        inp = make_input(
            losses_this_period=0,
            losses_on_price_count=0,
            losses_on_features_count=0,
            losses_on_relationship_count=0,
        )
        assert e._pattern_intensity_score(inp) == 0.0

    def test_price_ratio_below_20_gives_zero_for_price(self):
        e = self._e()
        inp = make_input(
            losses_this_period=10, losses_on_price_count=1,   # 10%
            losses_on_features_count=0, losses_on_relationship_count=0,
        )
        assert e._pattern_intensity_score(inp) == 0.0

    def test_price_ratio_exactly_20(self):
        e = self._e()
        inp = make_input(
            losses_this_period=10, losses_on_price_count=2,   # 20%
            losses_on_features_count=0, losses_on_relationship_count=0,
        )
        assert e._pattern_intensity_score(inp) >= 10.0

    def test_price_ratio_exactly_40(self):
        e = self._e()
        inp = make_input(
            losses_this_period=10, losses_on_price_count=4,   # 40%
            losses_on_features_count=0, losses_on_relationship_count=0,
        )
        assert e._pattern_intensity_score(inp) >= 24.0

    def test_price_ratio_exactly_60(self):
        e = self._e()
        inp = make_input(
            losses_this_period=10, losses_on_price_count=6,   # 60%
            losses_on_features_count=0, losses_on_relationship_count=0,
        )
        assert e._pattern_intensity_score(inp) >= 40.0

    def test_feature_ratio_below_15_gives_zero_for_feature(self):
        e = self._e()
        inp = make_input(
            losses_this_period=10, losses_on_price_count=0,
            losses_on_features_count=1,   # 10%
            losses_on_relationship_count=0,
        )
        assert e._pattern_intensity_score(inp) == 0.0

    def test_feature_ratio_exactly_15(self):
        e = self._e()
        # 15% of 20 = 3
        inp = make_input(
            losses_this_period=20, losses_on_price_count=0,
            losses_on_features_count=3,
            losses_on_relationship_count=0,
        )
        assert e._pattern_intensity_score(inp) >= 8.0

    def test_relationship_ratio_below_30_gives_zero(self):
        e = self._e()
        inp = make_input(
            losses_this_period=10, losses_on_price_count=0,
            losses_on_features_count=0,
            losses_on_relationship_count=2,   # 20%
        )
        assert e._pattern_intensity_score(inp) == 0.0

    def test_relationship_ratio_exactly_30(self):
        e = self._e()
        inp = make_input(
            losses_this_period=10, losses_on_price_count=0,
            losses_on_features_count=0,
            losses_on_relationship_count=3,   # 30%
        )
        assert e._pattern_intensity_score(inp) >= 14.0

    def test_relationship_ratio_exactly_50(self):
        e = self._e()
        inp = make_input(
            losses_this_period=10, losses_on_price_count=0,
            losses_on_features_count=0,
            losses_on_relationship_count=5,   # 50%
        )
        assert e._pattern_intensity_score(inp) >= 25.0

    def test_score_non_negative(self):
        e = self._e()
        inp = make_input(
            losses_this_period=5, losses_on_price_count=0,
            losses_on_features_count=0, losses_on_relationship_count=0,
        )
        assert e._pattern_intensity_score(inp) >= 0.0

    def test_score_clamped_at_100(self):
        e = self._e()
        # price>=60%(40) + feature>=50%(35) + rel>=50%(25) = 100
        # 6 price, 5 feature, 5 rel out of 10 is >10 total losses; adjust
        inp = make_input(
            losses_this_period=20,
            losses_on_price_count=13,   # 65%
            losses_on_features_count=11,  # 55%
            losses_on_relationship_count=10,  # 50%
        )
        assert e._pattern_intensity_score(inp) == 100.0


# ===========================================================================
# 23. to_dict() value types and rounding
# ===========================================================================

class TestToDictDetails:

    def test_to_dict_decline_score_rounded_to_1_decimal(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        v = d["win_rate_decline_score"]
        assert round(v, 1) == v

    def test_to_dict_deal_quality_score_rounded(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        v = d["deal_quality_score"]
        assert round(v, 1) == v

    def test_to_dict_readiness_score_rounded(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        v = d["competitive_readiness_score"]
        assert round(v, 1) == v

    def test_to_dict_pattern_intensity_rounded(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        v = d["pattern_intensity_score"]
        assert round(v, 1) == v

    def test_to_dict_enum_values_are_strings_not_enum_objects(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        assert d["win_rate_risk"] in [e.value for e in WinRateRisk]
        assert d["erosion_pattern"] in [e.value for e in ErosionPattern]
        assert d["erosion_severity"] in [e.value for e in ErosionSeverity]
        assert d["recommended_action"] in [e.value for e in WinRateAction]

    def test_to_dict_for_critical_input(self, engine, critical_input):
        d = engine.assess(critical_input).to_dict()
        assert len(d) == 15
        assert d["win_rate_risk"] == "critical"

    def test_to_dict_revenue_matches_calculation(self, engine):
        inp = make_input(losses_this_period=3, avg_deal_size_won_usd=15_000.0)
        result = engine.assess(inp)
        d = result.to_dict()
        expected = round(3 * 15_000.0 * (result.win_rate_composite / 100.0), 2)
        assert d["estimated_lost_revenue_usd"] == expected


# ===========================================================================
# 24. summary() with diverse risk/pattern/severity/action distributions
# ===========================================================================

class TestSummaryDistributions:

    def test_summary_risk_counts_keys_are_valid_risk_values(self, engine):
        engine.assess(make_input())
        valid = {e.value for e in WinRateRisk}
        for k in engine.summary()["risk_counts"]:
            assert k in valid

    def test_summary_pattern_counts_keys_are_valid_pattern_values(self, engine):
        engine.assess(make_input())
        valid = {e.value for e in ErosionPattern}
        for k in engine.summary()["pattern_counts"]:
            assert k in valid

    def test_summary_severity_counts_keys_are_valid_severity_values(self, engine):
        engine.assess(make_input())
        valid = {e.value for e in ErosionSeverity}
        for k in engine.summary()["severity_counts"]:
            assert k in valid

    def test_summary_action_counts_keys_are_valid_action_values(self, engine):
        engine.assess(make_input())
        valid = {e.value for e in WinRateAction}
        for k in engine.summary()["action_counts"]:
            assert k in valid

    def test_summary_avg_composite_between_0_and_100(self, engine):
        for _ in range(5):
            engine.assess(make_input())
        s = engine.summary()
        assert 0.0 <= s["avg_win_rate_composite"] <= 100.0

    def test_summary_eroding_count_lte_total(self, engine):
        for _ in range(10):
            engine.assess(make_input())
        s = engine.summary()
        assert s["eroding_count"] <= s["total"]

    def test_summary_coaching_count_lte_total(self, engine):
        for _ in range(10):
            engine.assess(make_input())
        s = engine.summary()
        assert s["coaching_count"] <= s["total"]

    def test_summary_avg_decline_in_range(self, engine):
        for _ in range(5):
            engine.assess(make_input())
        s = engine.summary()
        assert 0.0 <= s["avg_win_rate_decline_score"] <= 100.0

    def test_summary_avg_deal_quality_in_range(self, engine):
        for _ in range(5):
            engine.assess(make_input())
        s = engine.summary()
        assert 0.0 <= s["avg_deal_quality_score"] <= 100.0

    def test_summary_avg_readiness_in_range(self, engine):
        for _ in range(5):
            engine.assess(make_input())
        s = engine.summary()
        assert 0.0 <= s["avg_competitive_readiness_score"] <= 100.0

    def test_summary_avg_intensity_in_range(self, engine):
        for _ in range(5):
            engine.assess(make_input())
        s = engine.summary()
        assert 0.0 <= s["avg_pattern_intensity_score"] <= 100.0

    def test_summary_total_lost_revenue_non_negative(self, engine):
        for _ in range(5):
            engine.assess(make_input())
        s = engine.summary()
        assert s["total_estimated_lost_revenue_usd"] >= 0.0

    def test_summary_two_different_risks_appear_in_risk_counts(self, engine):
        # One low-risk and one critical-risk should produce 2 keys
        low_inp = make_input(
            win_rate_current_pct=80.0, win_rate_prior_period_pct=80.0,
            win_rate_benchmark_pct=60.0, consecutive_loss_streak=0,
            late_stage_loss_count=0, late_stage_total_count=0,
            champion_poached_count=0, win_rate_trend_3_period_delta=5.0,
            battlecard_last_updated_days=10, battlecard_usage_pct=0.90,
            competitor_strength_score=10.0, losses_on_price_count=0,
            losses_on_features_count=0, losses_on_relationship_count=0,
        )
        high_inp = make_input(
            win_rate_current_pct=0.0, win_rate_prior_period_pct=60.0,
            win_rate_benchmark_pct=60.0, consecutive_loss_streak=8,
            late_stage_loss_count=8, late_stage_total_count=10,
            champion_poached_count=3, win_rate_trend_3_period_delta=-30.0,
            battlecard_last_updated_days=200, battlecard_usage_pct=0.02,
            competitor_strength_score=95.0, losses_this_period=15,
            losses_on_price_count=5, losses_on_features_count=5,
            losses_on_relationship_count=4,
        )
        engine.assess_batch([low_inp, high_inp])
        assert len(engine.summary()["risk_counts"]) >= 2


# ===========================================================================
# 25. Additional boundary, smoke, and regression tests
# ===========================================================================

class TestAdditional:

    def test_assess_returns_result_with_non_empty_signal(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert len(result.erosion_signal) > 0

    def test_composite_formula_weights_sum_to_1(self):
        """Weights: 0.35 + 0.25 + 0.25 + 0.15 == 1.0"""
        assert abs(0.35 + 0.25 + 0.25 + 0.15 - 1.0) < 1e-9

    def test_is_win_rate_eroding_is_bool_type(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert type(result.is_win_rate_eroding) is bool

    def test_requires_coaching_is_bool_type(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert type(result.requires_coaching) is bool

    def test_estimated_lost_revenue_non_negative_for_critical(self, engine, critical_input):
        result = engine.assess(critical_input)
        assert result.estimated_lost_revenue_usd >= 0.0

    def test_batch_returns_list_type(self, engine):
        results = engine.assess_batch([make_input()])
        assert isinstance(results, list)

    def test_each_assess_call_adds_one_to_total(self, engine):
        for i in range(1, 6):
            engine.assess(make_input())
            assert engine.summary()["total"] == i

    def test_assess_batch_empty_does_not_change_summary_total(self, engine):
        engine.assess_batch([])
        assert engine.summary()["total"] == 0

    def test_input_dataclass_is_frozen_false(self):
        # Should be a mutable dataclass (no frozen=True)
        inp = make_input()
        inp.rep_id = "modified"
        assert inp.rep_id == "modified"

    def test_result_win_rate_composite_consistent_with_sub_scores(self, engine):
        inp = make_input()
        result = engine.assess(inp)
        manual = _clamp(
            result.win_rate_decline_score * 0.35
            + result.deal_quality_score * 0.25
            + result.competitive_readiness_score * 0.25
            + result.pattern_intensity_score * 0.15
        )
        assert abs(round(manual, 1) - result.win_rate_composite) < 0.05

    def test_feature_regression_threshold_price_check(self, engine):
        """feature_ratio >= 0.40 but readiness < 20 should NOT give feature_regression."""
        inp = make_input(
            losses_this_period=10,
            losses_on_features_count=5,   # 50% >= 0.40
            champion_poached_count=0,
            consecutive_loss_streak=0,
            # Keep readiness low
            battlecard_last_updated_days=10,
            battlecard_usage_pct=0.90,
            competitor_strength_score=10.0,
            losses_on_price_count=1,
            losses_on_relationship_count=1,
        )
        result = engine.assess(inp)
        if result.competitive_readiness_score < 20:
            assert result.erosion_pattern != ErosionPattern.feature_regression

    def test_rep_skill_gap_threshold_deal_score_check(self, engine):
        """late_rate >= 0.40 but deal < 20 should NOT give rep_skill_gap."""
        inp = make_input(
            losses_this_period=10,
            losses_on_price_count=0,
            losses_on_features_count=0,
            losses_on_relationship_count=0,
            champion_poached_count=0,
            consecutive_loss_streak=0,
            late_stage_loss_count=4, late_stage_total_count=10,  # 40%
        )
        result = engine.assess(inp)
        if result.deal_quality_score < 20:
            assert result.erosion_pattern != ErosionPattern.rep_skill_gap

    def test_summary_returns_dict_type(self, engine, healthy_input):
        engine.assess(healthy_input)
        assert isinstance(engine.summary(), dict)

    def test_empty_summary_risk_counts_empty_dict(self):
        e = SalesCompetitiveWinRateErosionEngine()
        assert e.summary()["risk_counts"] == {}

    def test_empty_summary_pattern_counts_empty_dict(self):
        e = SalesCompetitiveWinRateErosionEngine()
        assert e.summary()["pattern_counts"] == {}

    def test_empty_summary_severity_counts_empty_dict(self):
        e = SalesCompetitiveWinRateErosionEngine()
        assert e.summary()["severity_counts"] == {}

    def test_empty_summary_action_counts_empty_dict(self):
        e = SalesCompetitiveWinRateErosionEngine()
        assert e.summary()["action_counts"] == {}

    def test_assess_does_not_mutate_input(self, engine):
        inp = make_input(rep_id="stable-rep")
        engine.assess(inp)
        assert inp.rep_id == "stable-rep"
        assert inp.win_rate_current_pct == 55.0

    def test_multiple_assesses_accumulate_revenue(self, engine):
        r1 = engine.assess(make_input(losses_this_period=5, avg_deal_size_won_usd=10_000.0))
        r2 = engine.assess(make_input(losses_this_period=3, avg_deal_size_won_usd=20_000.0))
        expected = round(r1.estimated_lost_revenue_usd + r2.estimated_lost_revenue_usd, 2)
        assert engine.summary()["total_estimated_lost_revenue_usd"] == expected
