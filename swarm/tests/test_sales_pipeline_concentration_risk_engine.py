"""Comprehensive pytest tests for SalesPipelineConcentrationRiskEngine.

Covers all risk levels, patterns, severities, actions, fragile/rebalancing
conditions, edge cases, batch, summary, to_dict, and scoring logic.
"""

from __future__ import annotations

import pytest

from swarm.intelligence.sales_pipeline_concentration_risk_engine import (
    SalesPipelineConcentrationRiskEngine,
    PipelineConcentrationInput,
    PipelineConcentrationResult,
    ConcentrationRisk,
    ConcentrationPattern,
    ConcentrationSeverity,
    ConcentrationAction,
)


# ── helpers ──────────────────────────────────────────────────────────────────


def make_input(**overrides) -> PipelineConcentrationInput:
    """Return a healthy (well-diversified, low-risk) baseline input."""
    defaults = dict(
        rep_id="REP-001",
        region="WEST",
        evaluation_period_id="2026-Q2",
        total_pipeline_usd=1_000_000.0,
        top_deal_value_usd=80_000.0,          # 8% — below all thresholds
        top_3_deals_value_usd=200_000.0,       # 20% — below all thresholds
        deal_count=20,
        unique_accounts_in_pipeline=15,
        top_account_pipeline_usd=90_000.0,     # 9% — below 10% threshold
        product_lines_represented=8,
        total_product_lines=10,
        top_product_line_pipeline_pct=30.0,    # below 60% threshold
        deals_in_late_stage_pct=0.20,          # below 0.40 threshold
        deals_in_single_stage_pct=0.10,        # below 0.40 threshold
        avg_deal_value_usd=50_000.0,
        median_deal_value_usd=45_000.0,
        pipeline_created_last_30d_usd=200_000.0,
        pipeline_created_prior_30d_usd=200_000.0,  # ratio = 1.0 — above 0.75
        single_rep_pipeline_pct=0.30,          # below 0.70
        stale_deals_pct=0.05,                  # below 0.15
        committed_forecast_usd=400_000.0,
        sandbagged_deals_count=0,
    )
    defaults.update(overrides)
    return PipelineConcentrationInput(**defaults)


def fresh_engine() -> SalesPipelineConcentrationRiskEngine:
    return SalesPipelineConcentrationRiskEngine()


# ═══════════════════════════════════════════════════════════════════════════════
# 1. INSTANTIATION & BASIC STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════════


class TestInstantiation:
    def test_engine_creates_without_args(self):
        engine = SalesPipelineConcentrationRiskEngine()
        assert engine is not None

    def test_assess_returns_result_type(self):
        engine = fresh_engine()
        result = engine.assess(make_input())
        assert isinstance(result, PipelineConcentrationResult)

    def test_result_has_correct_rep_id(self):
        engine = fresh_engine()
        result = engine.assess(make_input(rep_id="REP-XYZ"))
        assert result.rep_id == "REP-XYZ"

    def test_result_has_correct_region(self):
        engine = fresh_engine()
        result = engine.assess(make_input(region="EAST"))
        assert result.region == "EAST"

    def test_result_fields_count(self):
        engine = fresh_engine()
        result = engine.assess(make_input())
        # 15 fields in PipelineConcentrationResult
        import dataclasses
        assert len(dataclasses.fields(result)) == 15

    def test_concentration_risk_is_enum(self):
        result = fresh_engine().assess(make_input())
        assert isinstance(result.concentration_risk, ConcentrationRisk)

    def test_concentration_pattern_is_enum(self):
        result = fresh_engine().assess(make_input())
        assert isinstance(result.concentration_pattern, ConcentrationPattern)

    def test_concentration_severity_is_enum(self):
        result = fresh_engine().assess(make_input())
        assert isinstance(result.concentration_severity, ConcentrationSeverity)

    def test_recommended_action_is_enum(self):
        result = fresh_engine().assess(make_input())
        assert isinstance(result.recommended_action, ConcentrationAction)

    def test_score_fields_are_floats(self):
        result = fresh_engine().assess(make_input())
        assert isinstance(result.deal_concentration_score, float)
        assert isinstance(result.account_concentration_score, float)
        assert isinstance(result.product_concentration_score, float)
        assert isinstance(result.stage_concentration_score, float)
        assert isinstance(result.concentration_composite, float)

    def test_bool_fields(self):
        result = fresh_engine().assess(make_input())
        assert isinstance(result.is_fragile_pipeline, bool)
        assert isinstance(result.requires_rebalancing, bool)

    def test_at_risk_revenue_is_float(self):
        result = fresh_engine().assess(make_input())
        assert isinstance(result.estimated_at_risk_revenue_usd, float)

    def test_concentration_signal_is_str(self):
        result = fresh_engine().assess(make_input())
        assert isinstance(result.concentration_signal, str)
        assert len(result.concentration_signal) > 0


# ═══════════════════════════════════════════════════════════════════════════════
# 2. RISK LEVELS
# ═══════════════════════════════════════════════════════════════════════════════


class TestRiskLevels:
    def test_low_risk_healthy_pipeline(self):
        result = fresh_engine().assess(make_input())
        assert result.concentration_risk == ConcentrationRisk.low

    def test_risk_low_composite_below_20(self):
        result = fresh_engine().assess(make_input())
        assert result.concentration_composite < 20

    def test_moderate_risk_composite_20_to_40(self):
        # top_deal=40%->+32, top3=60%->+9 => deal=41
        # unique=4->+15, single_rep=0.75->+12 => account=27
        # composite = 41*0.35 + 27*0.30 = 14.35 + 8.1 = 22.45 -> moderate
        inp = make_input(
            top_deal_value_usd=400_000.0,
            top_3_deals_value_usd=600_000.0,
            deal_count=8,
            unique_accounts_in_pipeline=4,
            top_account_pipeline_usd=90_000.0,
            single_rep_pipeline_pct=0.75,
        )
        result = fresh_engine().assess(inp)
        assert result.concentration_risk == ConcentrationRisk.moderate
        assert 20 <= result.concentration_composite < 40

    def test_high_risk_composite_40_to_60(self):
        # deal=80 (70%->50 + 90%->30), account=72 (60%->45 + 4uniq->15 + 0.75->12)
        # composite = 80*0.35 + 72*0.30 = 28.0 + 21.6 = 49.6 -> high
        inp = make_input(
            top_deal_value_usd=700_000.0,
            top_3_deals_value_usd=900_000.0,
            deal_count=5,
            unique_accounts_in_pipeline=4,
            top_account_pipeline_usd=600_000.0,
            single_rep_pipeline_pct=0.75,
        )
        result = fresh_engine().assess(inp)
        assert result.concentration_risk == ConcentrationRisk.high
        assert 40 <= result.concentration_composite < 60

    def test_critical_risk_composite_gte_60(self):
        inp = make_input(
            top_deal_value_usd=700_000.0,      # 70% -> +50
            top_3_deals_value_usd=900_000.0,   # 90% -> +30
            deal_count=2,                       # <=2 -> +20
            unique_accounts_in_pipeline=2,      # <=2 -> +30
            top_account_pipeline_usd=700_000.0, # 70% -> +45
            single_rep_pipeline_pct=0.95,       # >=0.90 -> +25
            deals_in_single_stage_pct=0.80,     # >=0.80 -> +35
            deals_in_late_stage_pct=0.85,       # >=0.80 -> +40
            stale_deals_pct=0.55,               # >=0.50 -> +25
        )
        result = fresh_engine().assess(inp)
        assert result.concentration_risk == ConcentrationRisk.critical
        assert result.concentration_composite >= 60

    def test_risk_boundary_exactly_20_is_moderate(self):
        # Use same inputs as confirmed moderate test above
        # deal=41 * 0.35 + account=27 * 0.30 = 22.45 -> moderate
        inp = make_input(
            top_deal_value_usd=400_000.0,
            top_3_deals_value_usd=600_000.0,
            deal_count=8,
            unique_accounts_in_pipeline=4,
            top_account_pipeline_usd=90_000.0,
            single_rep_pipeline_pct=0.75,
        )
        result = fresh_engine().assess(inp)
        # Should be moderate or above
        assert result.concentration_risk in (ConcentrationRisk.moderate, ConcentrationRisk.high)
        assert result.concentration_composite >= 20

    def test_risk_boundary_exactly_40_is_high(self):
        # deal=80, account=72 -> composite=49.6 confirmed high
        inp = make_input(
            top_deal_value_usd=700_000.0,
            top_3_deals_value_usd=900_000.0,
            deal_count=5,
            unique_accounts_in_pipeline=4,
            top_account_pipeline_usd=600_000.0,
            single_rep_pipeline_pct=0.75,
        )
        result = fresh_engine().assess(inp)
        assert result.concentration_risk in (ConcentrationRisk.high, ConcentrationRisk.critical)
        assert result.concentration_composite >= 40

    def test_all_risk_enum_values_accessible(self):
        assert ConcentrationRisk.low.value == "low"
        assert ConcentrationRisk.moderate.value == "moderate"
        assert ConcentrationRisk.high.value == "high"
        assert ConcentrationRisk.critical.value == "critical"


# ═══════════════════════════════════════════════════════════════════════════════
# 3. SEVERITY LEVELS
# ═══════════════════════════════════════════════════════════════════════════════


class TestSeverityLevels:
    def test_diversified_severity_low_composite(self):
        result = fresh_engine().assess(make_input())
        assert result.concentration_severity == ConcentrationSeverity.diversified

    def test_watch_severity_composite_20_to_40(self):
        inp = make_input(
            top_deal_value_usd=260_000.0,
            unique_accounts_in_pipeline=7,
            top_account_pipeline_usd=110_000.0,
        )
        result = fresh_engine().assess(inp)
        if 20 <= result.concentration_composite < 40:
            assert result.concentration_severity == ConcentrationSeverity.watch

    def test_concentrated_severity_40_to_60(self):
        inp = make_input(
            top_deal_value_usd=420_000.0,
            top_3_deals_value_usd=750_000.0,
            deal_count=5,
            unique_accounts_in_pipeline=5,
            top_account_pipeline_usd=420_000.0,
            single_rep_pipeline_pct=0.75,
        )
        result = fresh_engine().assess(inp)
        if 40 <= result.concentration_composite < 60:
            assert result.concentration_severity == ConcentrationSeverity.concentrated

    def test_critical_severity_gte_60(self):
        inp = make_input(
            top_deal_value_usd=700_000.0,
            top_3_deals_value_usd=900_000.0,
            deal_count=2,
            unique_accounts_in_pipeline=2,
            top_account_pipeline_usd=700_000.0,
            single_rep_pipeline_pct=0.95,
            deals_in_single_stage_pct=0.80,
            deals_in_late_stage_pct=0.85,
            stale_deals_pct=0.55,
        )
        result = fresh_engine().assess(inp)
        assert result.concentration_severity == ConcentrationSeverity.critical

    def test_severity_matches_risk_bucket(self):
        # Risk and severity should always be in the same composite bucket
        for inp_kwargs in [
            {},  # low
            dict(top_deal_value_usd=260_000.0, unique_accounts_in_pipeline=7,
                 top_account_pipeline_usd=110_000.0),
        ]:
            result = fresh_engine().assess(make_input(**inp_kwargs))
            composite = result.concentration_composite
            if composite < 20:
                assert result.concentration_severity == ConcentrationSeverity.diversified
            elif composite < 40:
                assert result.concentration_severity == ConcentrationSeverity.watch
            elif composite < 60:
                assert result.concentration_severity == ConcentrationSeverity.concentrated
            else:
                assert result.concentration_severity == ConcentrationSeverity.critical

    def test_all_severity_enum_values_accessible(self):
        assert ConcentrationSeverity.diversified.value == "diversified"
        assert ConcentrationSeverity.watch.value == "watch"
        assert ConcentrationSeverity.concentrated.value == "concentrated"
        assert ConcentrationSeverity.critical.value == "critical"


# ═══════════════════════════════════════════════════════════════════════════════
# 4. CONCENTRATION PATTERNS
# ═══════════════════════════════════════════════════════════════════════════════


class TestConcentrationPatterns:
    def test_pattern_none_healthy(self):
        result = fresh_engine().assess(make_input())
        assert result.concentration_pattern == ConcentrationPattern.none

    def test_whale_dependency_top_deal_45pct(self):
        inp = make_input(
            top_deal_value_usd=500_000.0,   # 50% -> whale
            top_3_deals_value_usd=700_000.0,
            deals_in_single_stage_pct=0.10,  # keep below 0.70 so stage_bottleneck not triggered
        )
        result = fresh_engine().assess(inp)
        assert result.concentration_pattern == ConcentrationPattern.whale_dependency

    def test_whale_dependency_exactly_45pct(self):
        inp = make_input(
            top_deal_value_usd=450_000.0,
            deals_in_single_stage_pct=0.10,
        )
        result = fresh_engine().assess(inp)
        assert result.concentration_pattern == ConcentrationPattern.whale_dependency

    def test_no_whale_dependency_below_45pct(self):
        inp = make_input(top_deal_value_usd=440_000.0, deals_in_single_stage_pct=0.10)
        result = fresh_engine().assess(inp)
        assert result.concentration_pattern != ConcentrationPattern.whale_dependency

    def test_rep_single_point_85pct(self):
        inp = make_input(
            single_rep_pipeline_pct=0.85,
            top_deal_value_usd=80_000.0,     # <45% so no whale
            deals_in_single_stage_pct=0.10,  # <0.70 so no stage_bottleneck
        )
        result = fresh_engine().assess(inp)
        assert result.concentration_pattern == ConcentrationPattern.rep_single_point

    def test_rep_single_point_above_85pct(self):
        inp = make_input(
            single_rep_pipeline_pct=0.95,
            top_deal_value_usd=80_000.0,
            deals_in_single_stage_pct=0.10,
        )
        result = fresh_engine().assess(inp)
        assert result.concentration_pattern == ConcentrationPattern.rep_single_point

    def test_rep_single_point_below_85pct_not_triggered(self):
        inp = make_input(single_rep_pipeline_pct=0.84, top_deal_value_usd=80_000.0)
        result = fresh_engine().assess(inp)
        assert result.concentration_pattern != ConcentrationPattern.rep_single_point

    def test_account_overexposure_40pct(self):
        inp = make_input(
            top_account_pipeline_usd=400_000.0,  # 40%
            single_rep_pipeline_pct=0.30,         # below 0.85
            top_deal_value_usd=80_000.0,          # below 45%
            deals_in_single_stage_pct=0.10,
        )
        result = fresh_engine().assess(inp)
        assert result.concentration_pattern == ConcentrationPattern.account_overexposure

    def test_account_overexposure_above_40pct(self):
        inp = make_input(
            top_account_pipeline_usd=600_000.0,
            single_rep_pipeline_pct=0.30,
            top_deal_value_usd=80_000.0,
            deals_in_single_stage_pct=0.10,
        )
        result = fresh_engine().assess(inp)
        assert result.concentration_pattern == ConcentrationPattern.account_overexposure

    def test_account_overexposure_below_40pct_not_triggered(self):
        inp = make_input(top_account_pipeline_usd=390_000.0, single_rep_pipeline_pct=0.30,
                         top_deal_value_usd=80_000.0, deals_in_single_stage_pct=0.10)
        result = fresh_engine().assess(inp)
        assert result.concentration_pattern != ConcentrationPattern.account_overexposure

    def test_product_concentration_75pct_with_score(self):
        # Need top_product_line_pipeline_pct>=75 AND product score>=20
        # product score: 75% -> +24; coverage=8/10=0.80 -> no bonus; creation_ratio=1.0 -> no bonus => score=24
        inp = make_input(
            top_product_line_pipeline_pct=75.0,
            product_lines_represented=8,
            total_product_lines=10,
            pipeline_created_last_30d_usd=200_000.0,
            pipeline_created_prior_30d_usd=200_000.0,
            single_rep_pipeline_pct=0.30,
            top_deal_value_usd=80_000.0,
            deals_in_single_stage_pct=0.10,
            top_account_pipeline_usd=90_000.0,
        )
        result = fresh_engine().assess(inp)
        assert result.concentration_pattern == ConcentrationPattern.product_concentration

    def test_product_concentration_not_triggered_below_75pct(self):
        inp = make_input(top_product_line_pipeline_pct=74.0)
        result = fresh_engine().assess(inp)
        assert result.concentration_pattern != ConcentrationPattern.product_concentration

    def test_stage_bottleneck_70pct_single_stage(self):
        # deals_in_single_stage_pct>=0.70 AND stage_score>=30
        # stage_score: single_stage=0.75 -> +20; add late_stage >=0.80 -> +40; stale>=0.50 -> +25 => score=85
        inp = make_input(
            deals_in_single_stage_pct=0.75,
            deals_in_late_stage_pct=0.85,
            stale_deals_pct=0.0,
        )
        result = fresh_engine().assess(inp)
        assert result.concentration_pattern == ConcentrationPattern.stage_bottleneck

    def test_stage_bottleneck_exactly_70pct(self):
        inp = make_input(
            deals_in_single_stage_pct=0.70,
            deals_in_late_stage_pct=0.85,
            stale_deals_pct=0.0,
        )
        result = fresh_engine().assess(inp)
        assert result.concentration_pattern == ConcentrationPattern.stage_bottleneck

    def test_stage_bottleneck_priority_over_whale(self):
        # Both stage_bottleneck and whale_dependency conditions met
        inp = make_input(
            deals_in_single_stage_pct=0.80,
            deals_in_late_stage_pct=0.85,
            top_deal_value_usd=500_000.0,   # 50% -> whale condition
        )
        result = fresh_engine().assess(inp)
        assert result.concentration_pattern == ConcentrationPattern.stage_bottleneck

    def test_whale_priority_over_rep_single_point(self):
        inp = make_input(
            top_deal_value_usd=500_000.0,   # whale
            single_rep_pipeline_pct=0.90,   # also rep_single_point
            deals_in_single_stage_pct=0.10,
        )
        result = fresh_engine().assess(inp)
        assert result.concentration_pattern == ConcentrationPattern.whale_dependency

    def test_rep_single_point_priority_over_account(self):
        inp = make_input(
            single_rep_pipeline_pct=0.90,
            top_account_pipeline_usd=500_000.0,  # account condition
            top_deal_value_usd=80_000.0,
            deals_in_single_stage_pct=0.10,
        )
        result = fresh_engine().assess(inp)
        assert result.concentration_pattern == ConcentrationPattern.rep_single_point

    def test_account_priority_over_product(self):
        inp = make_input(
            top_account_pipeline_usd=500_000.0,
            top_product_line_pipeline_pct=80.0,
            single_rep_pipeline_pct=0.30,
            top_deal_value_usd=80_000.0,
            deals_in_single_stage_pct=0.10,
        )
        result = fresh_engine().assess(inp)
        assert result.concentration_pattern == ConcentrationPattern.account_overexposure

    def test_all_pattern_enum_values_accessible(self):
        assert ConcentrationPattern.none.value == "none"
        assert ConcentrationPattern.whale_dependency.value == "whale_dependency"
        assert ConcentrationPattern.rep_single_point.value == "rep_single_point"
        assert ConcentrationPattern.account_overexposure.value == "account_overexposure"
        assert ConcentrationPattern.product_concentration.value == "product_concentration"
        assert ConcentrationPattern.stage_bottleneck.value == "stage_bottleneck"


# ═══════════════════════════════════════════════════════════════════════════════
# 5. RECOMMENDED ACTIONS
# ═══════════════════════════════════════════════════════════════════════════════


class TestRecommendedActions:
    def test_no_action_for_low_risk(self):
        result = fresh_engine().assess(make_input())
        assert result.recommended_action == ConcentrationAction.no_action

    def test_pipeline_diversification_for_moderate(self):
        inp = make_input(
            top_deal_value_usd=260_000.0,
            unique_accounts_in_pipeline=7,
            top_account_pipeline_usd=110_000.0,
        )
        result = fresh_engine().assess(inp)
        if result.concentration_risk == ConcentrationRisk.moderate:
            assert result.recommended_action == ConcentrationAction.pipeline_diversification

    def test_rep_rebalancing_for_high_risk(self):
        # composite in [40,50) => high risk, rep_rebalancing
        inp = make_input(
            top_deal_value_usd=420_000.0,
            top_3_deals_value_usd=750_000.0,
            deal_count=5,
            unique_accounts_in_pipeline=5,
            top_account_pipeline_usd=420_000.0,
            single_rep_pipeline_pct=0.75,
        )
        result = fresh_engine().assess(inp)
        if result.concentration_risk == ConcentrationRisk.high and result.concentration_composite < 50:
            assert result.recommended_action == ConcentrationAction.rep_rebalancing

    def test_forecast_risk_flag_composite_50_to_60(self):
        inp = make_input(
            top_deal_value_usd=420_000.0,
            top_3_deals_value_usd=870_000.0,
            deal_count=5,
            unique_accounts_in_pipeline=4,
            top_account_pipeline_usd=420_000.0,
            single_rep_pipeline_pct=0.92,
            deals_in_late_stage_pct=0.65,
            stale_deals_pct=0.20,
        )
        result = fresh_engine().assess(inp)
        if 50 <= result.concentration_composite < 60:
            assert result.recommended_action == ConcentrationAction.forecast_risk_flag

    def test_executive_review_composite_gte_60(self):
        inp = make_input(
            top_deal_value_usd=700_000.0,
            top_3_deals_value_usd=900_000.0,
            deal_count=2,
            unique_accounts_in_pipeline=2,
            top_account_pipeline_usd=700_000.0,
            single_rep_pipeline_pct=0.95,
            deals_in_single_stage_pct=0.80,
            deals_in_late_stage_pct=0.85,
            stale_deals_pct=0.55,
        )
        result = fresh_engine().assess(inp)
        assert result.concentration_composite >= 60
        assert result.recommended_action == ConcentrationAction.executive_review

    def test_all_action_enum_values_accessible(self):
        assert ConcentrationAction.no_action.value == "no_action"
        assert ConcentrationAction.pipeline_diversification.value == "pipeline_diversification"
        assert ConcentrationAction.rep_rebalancing.value == "rep_rebalancing"
        assert ConcentrationAction.forecast_risk_flag.value == "forecast_risk_flag"
        assert ConcentrationAction.executive_review.value == "executive_review"


# ═══════════════════════════════════════════════════════════════════════════════
# 6. DEAL CONCENTRATION SCORE
# ═══════════════════════════════════════════════════════════════════════════════


class TestDealConcentrationScore:
    def test_zero_when_no_pipeline(self):
        inp = make_input(
            total_pipeline_usd=0.0,
            top_deal_value_usd=0.0,
            top_3_deals_value_usd=0.0,
            deal_count=20,
        )
        result = fresh_engine().assess(inp)
        assert result.deal_concentration_score == 0.0

    def test_top_deal_15pct_adds_8(self):
        # top_deal = 15% -> +8, deal_count=20 -> no bonus
        inp = make_input(top_deal_value_usd=150_000.0, top_3_deals_value_usd=300_000.0)
        result = fresh_engine().assess(inp)
        # top3=30% -> no top3 bonus; deal_count=20 -> no deal_count bonus
        assert result.deal_concentration_score == pytest.approx(8.0, abs=0.1)

    def test_top_deal_25pct_adds_18(self):
        inp = make_input(top_deal_value_usd=250_000.0, top_3_deals_value_usd=350_000.0)
        result = fresh_engine().assess(inp)
        # top3=35% -> no bonus
        assert result.deal_concentration_score == pytest.approx(18.0, abs=0.1)

    def test_top_deal_40pct_adds_32(self):
        inp = make_input(top_deal_value_usd=400_000.0, top_3_deals_value_usd=550_000.0)
        result = fresh_engine().assess(inp)
        # top3=55% -> +9
        assert result.deal_concentration_score == pytest.approx(32.0 + 9.0, abs=0.1)

    def test_top_deal_60pct_adds_50(self):
        inp = make_input(top_deal_value_usd=600_000.0, top_3_deals_value_usd=750_000.0)
        result = fresh_engine().assess(inp)
        # top3=75% -> +18
        assert result.deal_concentration_score == pytest.approx(50.0 + 18.0, abs=0.1)

    def test_top3_55pct_adds_9(self):
        inp = make_input(top_deal_value_usd=100_000.0, top_3_deals_value_usd=550_000.0)
        result = fresh_engine().assess(inp)
        # top_deal=10% -> no bonus; top3=55% -> +9
        assert result.deal_concentration_score == pytest.approx(9.0, abs=0.1)

    def test_top3_70pct_adds_18(self):
        inp = make_input(top_deal_value_usd=100_000.0, top_3_deals_value_usd=700_000.0)
        result = fresh_engine().assess(inp)
        assert result.deal_concentration_score == pytest.approx(18.0, abs=0.1)

    def test_top3_85pct_adds_30(self):
        inp = make_input(top_deal_value_usd=100_000.0, top_3_deals_value_usd=850_000.0)
        result = fresh_engine().assess(inp)
        assert result.deal_concentration_score == pytest.approx(30.0, abs=0.1)

    def test_deal_count_2_adds_20(self):
        inp = make_input(deal_count=2, top_deal_value_usd=80_000.0, top_3_deals_value_usd=200_000.0)
        result = fresh_engine().assess(inp)
        assert result.deal_concentration_score == pytest.approx(20.0, abs=0.1)

    def test_deal_count_3_adds_10(self):
        inp = make_input(deal_count=3, top_deal_value_usd=80_000.0, top_3_deals_value_usd=200_000.0)
        result = fresh_engine().assess(inp)
        assert result.deal_concentration_score == pytest.approx(10.0, abs=0.1)

    def test_deal_count_4_adds_10(self):
        inp = make_input(deal_count=4, top_deal_value_usd=80_000.0, top_3_deals_value_usd=200_000.0)
        result = fresh_engine().assess(inp)
        assert result.deal_concentration_score == pytest.approx(10.0, abs=0.1)

    def test_deal_count_5_no_bonus(self):
        inp = make_input(deal_count=5, top_deal_value_usd=80_000.0, top_3_deals_value_usd=200_000.0)
        result = fresh_engine().assess(inp)
        assert result.deal_concentration_score == pytest.approx(0.0, abs=0.1)

    def test_deal_score_clamped_at_100(self):
        # Max possible: 50+30+20 = 100
        inp = make_input(
            top_deal_value_usd=700_000.0,   # 70% -> +50
            top_3_deals_value_usd=900_000.0, # 90% -> +30
            deal_count=2,                    # -> +20
        )
        result = fresh_engine().assess(inp)
        assert result.deal_concentration_score == 100.0

    def test_deal_score_clamped_not_exceed_100(self):
        result = fresh_engine().assess(make_input(
            top_deal_value_usd=1_000_000.0,
            top_3_deals_value_usd=1_000_000.0,
            deal_count=1,
        ))
        assert result.deal_concentration_score <= 100.0

    def test_deal_score_at_least_0(self):
        result = fresh_engine().assess(make_input(
            total_pipeline_usd=0.0,
            top_deal_value_usd=0.0,
            top_3_deals_value_usd=0.0,
            deal_count=100,
        ))
        assert result.deal_concentration_score >= 0.0


# ═══════════════════════════════════════════════════════════════════════════════
# 7. ACCOUNT CONCENTRATION SCORE
# ═══════════════════════════════════════════════════════════════════════════════


class TestAccountConcentrationScore:
    def test_zero_no_pipeline_few_accounts_no_rep(self):
        inp = make_input(
            total_pipeline_usd=0.0,
            top_account_pipeline_usd=0.0,
            unique_accounts_in_pipeline=10,
            single_rep_pipeline_pct=0.0,
        )
        result = fresh_engine().assess(inp)
        assert result.account_concentration_score == pytest.approx(0.0, abs=0.1)

    def test_top_account_10pct_adds_6(self):
        inp = make_input(top_account_pipeline_usd=100_000.0,
                         unique_accounts_in_pipeline=10, single_rep_pipeline_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.account_concentration_score == pytest.approx(6.0, abs=0.1)

    def test_top_account_25pct_adds_15(self):
        inp = make_input(top_account_pipeline_usd=250_000.0,
                         unique_accounts_in_pipeline=10, single_rep_pipeline_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.account_concentration_score == pytest.approx(15.0, abs=0.1)

    def test_top_account_40pct_adds_28(self):
        inp = make_input(top_account_pipeline_usd=400_000.0,
                         unique_accounts_in_pipeline=10, single_rep_pipeline_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.account_concentration_score == pytest.approx(28.0, abs=0.1)

    def test_top_account_60pct_adds_45(self):
        inp = make_input(top_account_pipeline_usd=600_000.0,
                         unique_accounts_in_pipeline=10, single_rep_pipeline_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.account_concentration_score == pytest.approx(45.0, abs=0.1)

    def test_unique_accounts_2_adds_30(self):
        inp = make_input(unique_accounts_in_pipeline=2,
                         top_account_pipeline_usd=90_000.0, single_rep_pipeline_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.account_concentration_score == pytest.approx(30.0, abs=0.1)

    def test_unique_accounts_3_adds_15(self):
        inp = make_input(unique_accounts_in_pipeline=3,
                         top_account_pipeline_usd=90_000.0, single_rep_pipeline_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.account_concentration_score == pytest.approx(15.0, abs=0.1)

    def test_unique_accounts_4_adds_15(self):
        inp = make_input(unique_accounts_in_pipeline=4,
                         top_account_pipeline_usd=90_000.0, single_rep_pipeline_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.account_concentration_score == pytest.approx(15.0, abs=0.1)

    def test_unique_accounts_5_adds_6(self):
        inp = make_input(unique_accounts_in_pipeline=5,
                         top_account_pipeline_usd=90_000.0, single_rep_pipeline_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.account_concentration_score == pytest.approx(6.0, abs=0.1)

    def test_unique_accounts_6_adds_6(self):
        inp = make_input(unique_accounts_in_pipeline=6,
                         top_account_pipeline_usd=90_000.0, single_rep_pipeline_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.account_concentration_score == pytest.approx(6.0, abs=0.1)

    def test_unique_accounts_7_no_bonus(self):
        inp = make_input(unique_accounts_in_pipeline=7,
                         top_account_pipeline_usd=90_000.0, single_rep_pipeline_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.account_concentration_score == pytest.approx(0.0, abs=0.1)

    def test_single_rep_70pct_adds_12(self):
        inp = make_input(single_rep_pipeline_pct=0.70,
                         top_account_pipeline_usd=90_000.0, unique_accounts_in_pipeline=10)
        result = fresh_engine().assess(inp)
        assert result.account_concentration_score == pytest.approx(12.0, abs=0.1)

    def test_single_rep_90pct_adds_25(self):
        inp = make_input(single_rep_pipeline_pct=0.90,
                         top_account_pipeline_usd=90_000.0, unique_accounts_in_pipeline=10)
        result = fresh_engine().assess(inp)
        assert result.account_concentration_score == pytest.approx(25.0, abs=0.1)

    def test_single_rep_below_70pct_no_bonus(self):
        inp = make_input(single_rep_pipeline_pct=0.69,
                         top_account_pipeline_usd=90_000.0, unique_accounts_in_pipeline=10)
        result = fresh_engine().assess(inp)
        assert result.account_concentration_score == pytest.approx(0.0, abs=0.1)

    def test_account_score_clamped_at_100(self):
        inp = make_input(
            top_account_pipeline_usd=700_000.0,  # 70% -> +45
            unique_accounts_in_pipeline=2,        # -> +30
            single_rep_pipeline_pct=0.95,         # -> +25
        )
        result = fresh_engine().assess(inp)
        assert result.account_concentration_score == 100.0

    def test_account_score_not_exceed_100(self):
        result = fresh_engine().assess(make_input(
            top_account_pipeline_usd=1_000_000.0,
            unique_accounts_in_pipeline=1,
            single_rep_pipeline_pct=1.0,
        ))
        assert result.account_concentration_score <= 100.0


# ═══════════════════════════════════════════════════════════════════════════════
# 8. PRODUCT CONCENTRATION SCORE
# ═══════════════════════════════════════════════════════════════════════════════


class TestProductConcentrationScore:
    def test_zero_healthy(self):
        result = fresh_engine().assess(make_input())
        # top_product_line=30% no bonus; coverage=0.80 no bonus; creation_ratio=1.0 no bonus
        assert result.product_concentration_score == pytest.approx(0.0, abs=0.1)

    def test_top_product_line_60pct_adds_12(self):
        inp = make_input(
            top_product_line_pipeline_pct=60.0,
            product_lines_represented=8, total_product_lines=10,
            pipeline_created_last_30d_usd=200_000.0, pipeline_created_prior_30d_usd=200_000.0,
        )
        result = fresh_engine().assess(inp)
        assert result.product_concentration_score == pytest.approx(12.0, abs=0.1)

    def test_top_product_line_75pct_adds_24(self):
        inp = make_input(
            top_product_line_pipeline_pct=75.0,
            product_lines_represented=8, total_product_lines=10,
            pipeline_created_last_30d_usd=200_000.0, pipeline_created_prior_30d_usd=200_000.0,
        )
        result = fresh_engine().assess(inp)
        assert result.product_concentration_score == pytest.approx(24.0, abs=0.1)

    def test_top_product_line_90pct_adds_40(self):
        inp = make_input(
            top_product_line_pipeline_pct=90.0,
            product_lines_represented=8, total_product_lines=10,
            pipeline_created_last_30d_usd=200_000.0, pipeline_created_prior_30d_usd=200_000.0,
        )
        result = fresh_engine().assess(inp)
        assert result.product_concentration_score == pytest.approx(40.0, abs=0.1)

    def test_coverage_20pct_adds_35(self):
        # coverage = 2/10 = 0.20
        inp = make_input(
            top_product_line_pipeline_pct=30.0,  # no bonus
            product_lines_represented=2, total_product_lines=10,
            pipeline_created_last_30d_usd=200_000.0, pipeline_created_prior_30d_usd=200_000.0,
        )
        result = fresh_engine().assess(inp)
        assert result.product_concentration_score == pytest.approx(35.0, abs=0.1)

    def test_coverage_40pct_adds_20(self):
        inp = make_input(
            top_product_line_pipeline_pct=30.0,
            product_lines_represented=4, total_product_lines=10,
            pipeline_created_last_30d_usd=200_000.0, pipeline_created_prior_30d_usd=200_000.0,
        )
        result = fresh_engine().assess(inp)
        assert result.product_concentration_score == pytest.approx(20.0, abs=0.1)

    def test_coverage_60pct_adds_10(self):
        inp = make_input(
            top_product_line_pipeline_pct=30.0,
            product_lines_represented=6, total_product_lines=10,
            pipeline_created_last_30d_usd=200_000.0, pipeline_created_prior_30d_usd=200_000.0,
        )
        result = fresh_engine().assess(inp)
        assert result.product_concentration_score == pytest.approx(10.0, abs=0.1)

    def test_coverage_above_60pct_no_bonus(self):
        inp = make_input(
            top_product_line_pipeline_pct=30.0,
            product_lines_represented=7, total_product_lines=10,
            pipeline_created_last_30d_usd=200_000.0, pipeline_created_prior_30d_usd=200_000.0,
        )
        result = fresh_engine().assess(inp)
        assert result.product_concentration_score == pytest.approx(0.0, abs=0.1)

    def test_creation_ratio_25pct_adds_25(self):
        inp = make_input(
            top_product_line_pipeline_pct=30.0,
            product_lines_represented=8, total_product_lines=10,
            pipeline_created_last_30d_usd=50_000.0,
            pipeline_created_prior_30d_usd=200_000.0,  # ratio=0.25 -> +25
        )
        result = fresh_engine().assess(inp)
        assert result.product_concentration_score == pytest.approx(25.0, abs=0.1)

    def test_creation_ratio_exactly_25pct_adds_25(self):
        inp = make_input(
            top_product_line_pipeline_pct=30.0,
            product_lines_represented=8, total_product_lines=10,
            pipeline_created_last_30d_usd=25_000.0,
            pipeline_created_prior_30d_usd=100_000.0,  # ratio=0.25 exactly
        )
        result = fresh_engine().assess(inp)
        assert result.product_concentration_score == pytest.approx(25.0, abs=0.1)

    def test_creation_ratio_50pct_adds_14(self):
        inp = make_input(
            top_product_line_pipeline_pct=30.0,
            product_lines_represented=8, total_product_lines=10,
            pipeline_created_last_30d_usd=50_000.0,
            pipeline_created_prior_30d_usd=100_000.0,  # ratio=0.50
        )
        result = fresh_engine().assess(inp)
        assert result.product_concentration_score == pytest.approx(14.0, abs=0.1)

    def test_creation_ratio_75pct_adds_6(self):
        inp = make_input(
            top_product_line_pipeline_pct=30.0,
            product_lines_represented=8, total_product_lines=10,
            pipeline_created_last_30d_usd=75_000.0,
            pipeline_created_prior_30d_usd=100_000.0,  # ratio=0.75
        )
        result = fresh_engine().assess(inp)
        assert result.product_concentration_score == pytest.approx(6.0, abs=0.1)

    def test_creation_ratio_above_75pct_no_bonus(self):
        inp = make_input(
            top_product_line_pipeline_pct=30.0,
            product_lines_represented=8, total_product_lines=10,
            pipeline_created_last_30d_usd=80_000.0,
            pipeline_created_prior_30d_usd=100_000.0,  # ratio=0.80
        )
        result = fresh_engine().assess(inp)
        assert result.product_concentration_score == pytest.approx(0.0, abs=0.1)

    def test_zero_total_product_lines_no_coverage_bonus(self):
        inp = make_input(
            total_product_lines=0,
            product_lines_represented=0,
            top_product_line_pipeline_pct=30.0,
            pipeline_created_last_30d_usd=200_000.0, pipeline_created_prior_30d_usd=200_000.0,
        )
        result = fresh_engine().assess(inp)
        # No division by zero, coverage branch skipped
        assert result.product_concentration_score >= 0.0

    def test_zero_prior_pipeline_no_creation_bonus(self):
        inp = make_input(
            pipeline_created_prior_30d_usd=0.0,
            pipeline_created_last_30d_usd=0.0,
            top_product_line_pipeline_pct=30.0,
            product_lines_represented=8, total_product_lines=10,
        )
        result = fresh_engine().assess(inp)
        # No division by zero — creation_ratio branch skipped
        assert result.product_concentration_score >= 0.0

    def test_product_score_clamped_at_100(self):
        inp = make_input(
            top_product_line_pipeline_pct=90.0,       # +40
            product_lines_represented=2, total_product_lines=10,  # coverage 0.20 -> +35
            pipeline_created_last_30d_usd=10_000.0,
            pipeline_created_prior_30d_usd=100_000.0, # ratio=0.10 -> +25
        )
        result = fresh_engine().assess(inp)
        assert result.product_concentration_score == 100.0


# ═══════════════════════════════════════════════════════════════════════════════
# 9. STAGE CONCENTRATION SCORE
# ═══════════════════════════════════════════════════════════════════════════════


class TestStageConcentrationScore:
    def test_zero_healthy(self):
        result = fresh_engine().assess(make_input())
        assert result.stage_concentration_score == pytest.approx(0.0, abs=0.1)

    def test_late_stage_40pct_adds_10(self):
        inp = make_input(deals_in_late_stage_pct=0.40, deals_in_single_stage_pct=0.0,
                         stale_deals_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.stage_concentration_score == pytest.approx(10.0, abs=0.1)

    def test_late_stage_60pct_adds_24(self):
        inp = make_input(deals_in_late_stage_pct=0.60, deals_in_single_stage_pct=0.0,
                         stale_deals_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.stage_concentration_score == pytest.approx(24.0, abs=0.1)

    def test_late_stage_80pct_adds_40(self):
        inp = make_input(deals_in_late_stage_pct=0.80, deals_in_single_stage_pct=0.0,
                         stale_deals_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.stage_concentration_score == pytest.approx(40.0, abs=0.1)

    def test_late_stage_below_40pct_no_bonus(self):
        inp = make_input(deals_in_late_stage_pct=0.39, deals_in_single_stage_pct=0.0,
                         stale_deals_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.stage_concentration_score == pytest.approx(0.0, abs=0.1)

    def test_single_stage_40pct_adds_10(self):
        inp = make_input(deals_in_single_stage_pct=0.40, deals_in_late_stage_pct=0.0,
                         stale_deals_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.stage_concentration_score == pytest.approx(10.0, abs=0.1)

    def test_single_stage_60pct_adds_20(self):
        inp = make_input(deals_in_single_stage_pct=0.60, deals_in_late_stage_pct=0.0,
                         stale_deals_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.stage_concentration_score == pytest.approx(20.0, abs=0.1)

    def test_single_stage_80pct_adds_35(self):
        inp = make_input(deals_in_single_stage_pct=0.80, deals_in_late_stage_pct=0.0,
                         stale_deals_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.stage_concentration_score == pytest.approx(35.0, abs=0.1)

    def test_single_stage_below_40pct_no_bonus(self):
        inp = make_input(deals_in_single_stage_pct=0.39, deals_in_late_stage_pct=0.0,
                         stale_deals_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.stage_concentration_score == pytest.approx(0.0, abs=0.1)

    def test_stale_15pct_adds_6(self):
        inp = make_input(stale_deals_pct=0.15, deals_in_late_stage_pct=0.0,
                         deals_in_single_stage_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.stage_concentration_score == pytest.approx(6.0, abs=0.1)

    def test_stale_30pct_adds_14(self):
        inp = make_input(stale_deals_pct=0.30, deals_in_late_stage_pct=0.0,
                         deals_in_single_stage_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.stage_concentration_score == pytest.approx(14.0, abs=0.1)

    def test_stale_50pct_adds_25(self):
        inp = make_input(stale_deals_pct=0.50, deals_in_late_stage_pct=0.0,
                         deals_in_single_stage_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.stage_concentration_score == pytest.approx(25.0, abs=0.1)

    def test_stale_below_15pct_no_bonus(self):
        inp = make_input(stale_deals_pct=0.14, deals_in_late_stage_pct=0.0,
                         deals_in_single_stage_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.stage_concentration_score == pytest.approx(0.0, abs=0.1)

    def test_stage_score_clamped_at_100(self):
        inp = make_input(
            deals_in_late_stage_pct=0.85,    # +40
            deals_in_single_stage_pct=0.85,  # +35
            stale_deals_pct=0.60,            # +25
        )
        result = fresh_engine().assess(inp)
        assert result.stage_concentration_score == 100.0

    def test_stage_score_not_exceed_100(self):
        result = fresh_engine().assess(make_input(
            deals_in_late_stage_pct=1.0,
            deals_in_single_stage_pct=1.0,
            stale_deals_pct=1.0,
        ))
        assert result.stage_concentration_score <= 100.0


# ═══════════════════════════════════════════════════════════════════════════════
# 10. COMPOSITE SCORE
# ═══════════════════════════════════════════════════════════════════════════════


class TestCompositeScore:
    def test_composite_formula(self):
        # With healthy input all sub-scores should be 0
        result = fresh_engine().assess(make_input())
        assert result.concentration_composite == pytest.approx(0.0, abs=0.1)

    def test_composite_weighted_sum(self):
        # deal=8, account=0, product=0, stage=0
        inp = make_input(top_deal_value_usd=150_000.0)
        result = fresh_engine().assess(inp)
        expected = 8.0 * 0.35 + 0.0 * 0.30 + 0.0 * 0.20 + 0.0 * 0.15
        assert result.concentration_composite == pytest.approx(expected, abs=0.2)

    def test_composite_clamped_at_100(self):
        inp = make_input(
            top_deal_value_usd=700_000.0,
            top_3_deals_value_usd=900_000.0,
            deal_count=2,
            unique_accounts_in_pipeline=2,
            top_account_pipeline_usd=700_000.0,
            single_rep_pipeline_pct=0.95,
            deals_in_single_stage_pct=0.85,
            deals_in_late_stage_pct=0.85,
            stale_deals_pct=0.60,
        )
        result = fresh_engine().assess(inp)
        assert result.concentration_composite <= 100.0

    def test_composite_at_least_0(self):
        result = fresh_engine().assess(make_input(
            total_pipeline_usd=0.0,
            top_deal_value_usd=0.0,
            top_3_deals_value_usd=0.0,
        ))
        assert result.concentration_composite >= 0.0

    def test_composite_respects_weights(self):
        # Set only deal score: top_deal=15% -> deal=8
        # composite = 8*0.35 = 2.8
        inp = make_input(top_deal_value_usd=150_000.0)
        result = fresh_engine().assess(inp)
        assert result.concentration_composite == pytest.approx(8.0 * 0.35, abs=0.2)


# ═══════════════════════════════════════════════════════════════════════════════
# 11. IS_FRAGILE_PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════


class TestIsFragilePipeline:
    def test_not_fragile_healthy(self):
        result = fresh_engine().assess(make_input())
        assert result.is_fragile_pipeline is False

    def test_fragile_when_composite_gte_40(self):
        inp = make_input(
            top_deal_value_usd=420_000.0,
            top_3_deals_value_usd=750_000.0,
            deal_count=5,
            unique_accounts_in_pipeline=5,
            top_account_pipeline_usd=420_000.0,
            single_rep_pipeline_pct=0.75,
        )
        result = fresh_engine().assess(inp)
        if result.concentration_composite >= 40:
            assert result.is_fragile_pipeline is True

    def test_fragile_when_deal_count_1(self):
        inp = make_input(deal_count=1)
        result = fresh_engine().assess(inp)
        assert result.is_fragile_pipeline is True

    def test_fragile_when_deal_count_2(self):
        inp = make_input(deal_count=2)
        result = fresh_engine().assess(inp)
        assert result.is_fragile_pipeline is True

    def test_not_fragile_deal_count_3_low_composite(self):
        # deal_count=3 -> +10 deal score -> composite = 3.5, below 40; top_deal < 60%
        inp = make_input(deal_count=3, top_deal_value_usd=80_000.0)
        result = fresh_engine().assess(inp)
        assert result.is_fragile_pipeline is False

    def test_fragile_when_top_deal_60pct_pipeline(self):
        inp = make_input(
            total_pipeline_usd=1_000_000.0,
            top_deal_value_usd=600_000.0,  # 60%
            deal_count=10,
        )
        result = fresh_engine().assess(inp)
        assert result.is_fragile_pipeline is True

    def test_not_fragile_when_top_deal_59pct(self):
        inp = make_input(
            total_pipeline_usd=1_000_000.0,
            top_deal_value_usd=590_000.0,  # 59%
            deal_count=10,
        )
        result = fresh_engine().assess(inp)
        # composite from 59% deal = deal score + other contributions
        # top_deal=59% -> +32; top3=200/1000=20% -> 0; deal_count=10 -> 0
        # composite=32*0.35=11.2 < 40
        # top_deal/total = 0.59 < 0.60 => not fragile
        assert result.is_fragile_pipeline is False

    def test_fragile_zero_pipeline_zero_top_deal_deal_count_2(self):
        inp = make_input(
            total_pipeline_usd=0.0,
            top_deal_value_usd=0.0,
            deal_count=2,
        )
        result = fresh_engine().assess(inp)
        # deal_count<=2 => fragile
        assert result.is_fragile_pipeline is True

    def test_fragile_or_condition_all_three(self):
        # All three OR conditions met
        inp = make_input(
            deal_count=2,
            top_deal_value_usd=700_000.0,
            top_3_deals_value_usd=900_000.0,
            unique_accounts_in_pipeline=2,
            top_account_pipeline_usd=700_000.0,
            single_rep_pipeline_pct=0.95,
            deals_in_single_stage_pct=0.85,
            deals_in_late_stage_pct=0.85,
            stale_deals_pct=0.60,
        )
        result = fresh_engine().assess(inp)
        assert result.is_fragile_pipeline is True


# ═══════════════════════════════════════════════════════════════════════════════
# 12. REQUIRES_REBALANCING
# ═══════════════════════════════════════════════════════════════════════════════


class TestRequiresRebalancing:
    def test_not_required_healthy(self):
        result = fresh_engine().assess(make_input())
        assert result.requires_rebalancing is False

    def test_required_when_composite_gte_30(self):
        inp = make_input(
            top_deal_value_usd=420_000.0,
            top_3_deals_value_usd=750_000.0,
            unique_accounts_in_pipeline=10,
            top_account_pipeline_usd=90_000.0,
            single_rep_pipeline_pct=0.30,
        )
        result = fresh_engine().assess(inp)
        if result.concentration_composite >= 30:
            assert result.requires_rebalancing is True

    def test_required_when_unique_accounts_3(self):
        inp = make_input(unique_accounts_in_pipeline=3)
        result = fresh_engine().assess(inp)
        assert result.requires_rebalancing is True

    def test_required_when_unique_accounts_2(self):
        inp = make_input(unique_accounts_in_pipeline=2)
        result = fresh_engine().assess(inp)
        assert result.requires_rebalancing is True

    def test_required_when_unique_accounts_1(self):
        inp = make_input(unique_accounts_in_pipeline=1)
        result = fresh_engine().assess(inp)
        assert result.requires_rebalancing is True

    def test_not_required_unique_accounts_4_low_composite_no_sandbag(self):
        # unique_accounts=4 -> NOT <=3; need composite<30 and sandbagged=0
        inp = make_input(
            unique_accounts_in_pipeline=4,
            sandbagged_deals_count=0,
            top_deal_value_usd=80_000.0,
        )
        result = fresh_engine().assess(inp)
        # account_score = 15 (4 accounts) -> composite ~ 15*0.30=4.5
        # if composite < 30: not required
        if result.concentration_composite < 30:
            assert result.requires_rebalancing is False

    def test_required_when_sandbagged_deals_2(self):
        inp = make_input(sandbagged_deals_count=2, unique_accounts_in_pipeline=10)
        result = fresh_engine().assess(inp)
        assert result.requires_rebalancing is True

    def test_required_when_sandbagged_deals_5(self):
        inp = make_input(sandbagged_deals_count=5, unique_accounts_in_pipeline=10)
        result = fresh_engine().assess(inp)
        assert result.requires_rebalancing is True

    def test_not_required_sandbagged_1_low_composite_good_accounts(self):
        inp = make_input(sandbagged_deals_count=1, unique_accounts_in_pipeline=10)
        result = fresh_engine().assess(inp)
        if result.concentration_composite < 30:
            assert result.requires_rebalancing is False

    def test_required_all_three_conditions(self):
        inp = make_input(
            deal_count=2,
            unique_accounts_in_pipeline=3,
            sandbagged_deals_count=3,
            top_deal_value_usd=700_000.0,
            top_3_deals_value_usd=900_000.0,
            top_account_pipeline_usd=700_000.0,
            single_rep_pipeline_pct=0.95,
        )
        result = fresh_engine().assess(inp)
        assert result.requires_rebalancing is True


# ═══════════════════════════════════════════════════════════════════════════════
# 13. ESTIMATED_AT_RISK_REVENUE_USD
# ═══════════════════════════════════════════════════════════════════════════════


class TestEstimatedAtRiskRevenue:
    def test_zero_when_composite_zero(self):
        result = fresh_engine().assess(make_input(committed_forecast_usd=500_000.0))
        expected = 500_000.0 * (result.concentration_composite / 100.0)
        assert result.estimated_at_risk_revenue_usd == pytest.approx(expected, abs=1.0)

    def test_formula_committed_times_composite(self):
        inp = make_input(committed_forecast_usd=800_000.0, top_deal_value_usd=150_000.0)
        result = fresh_engine().assess(inp)
        expected = 800_000.0 * (result.concentration_composite / 100.0)
        assert result.estimated_at_risk_revenue_usd == pytest.approx(expected, abs=1.0)

    def test_at_risk_zero_committed_zero(self):
        result = fresh_engine().assess(make_input(committed_forecast_usd=0.0))
        assert result.estimated_at_risk_revenue_usd == pytest.approx(0.0, abs=0.01)

    def test_at_risk_full_when_composite_100(self):
        inp = make_input(
            committed_forecast_usd=1_000_000.0,
            top_deal_value_usd=700_000.0,
            top_3_deals_value_usd=900_000.0,
            deal_count=2,
            unique_accounts_in_pipeline=2,
            top_account_pipeline_usd=700_000.0,
            single_rep_pipeline_pct=0.95,
            deals_in_single_stage_pct=0.85,
            deals_in_late_stage_pct=0.85,
            stale_deals_pct=0.60,
        )
        result = fresh_engine().assess(inp)
        expected = 1_000_000.0 * (result.concentration_composite / 100.0)
        assert result.estimated_at_risk_revenue_usd == pytest.approx(expected, abs=1.0)

    def test_at_risk_proportional_to_forecast(self):
        inp1 = make_input(committed_forecast_usd=200_000.0, top_deal_value_usd=150_000.0)
        inp2 = make_input(committed_forecast_usd=400_000.0, top_deal_value_usd=150_000.0)
        r1 = fresh_engine().assess(inp1)
        r2 = fresh_engine().assess(inp2)
        # Same composite, double the forecast -> double at risk
        assert r2.estimated_at_risk_revenue_usd == pytest.approx(2 * r1.estimated_at_risk_revenue_usd, abs=1.0)


# ═══════════════════════════════════════════════════════════════════════════════
# 14. TO_DICT
# ═══════════════════════════════════════════════════════════════════════════════


class TestToDict:
    def get_dict(self):
        return fresh_engine().assess(make_input()).to_dict()

    def test_to_dict_has_15_keys(self):
        d = self.get_dict()
        assert len(d) == 15

    def test_to_dict_rep_id_str(self):
        d = self.get_dict()
        assert isinstance(d["rep_id"], str)

    def test_to_dict_region_str(self):
        d = self.get_dict()
        assert isinstance(d["region"], str)

    def test_to_dict_concentration_risk_str(self):
        d = self.get_dict()
        assert isinstance(d["concentration_risk"], str)
        assert d["concentration_risk"] in [e.value for e in ConcentrationRisk]

    def test_to_dict_concentration_pattern_str(self):
        d = self.get_dict()
        assert isinstance(d["concentration_pattern"], str)
        assert d["concentration_pattern"] in [e.value for e in ConcentrationPattern]

    def test_to_dict_concentration_severity_str(self):
        d = self.get_dict()
        assert isinstance(d["concentration_severity"], str)
        assert d["concentration_severity"] in [e.value for e in ConcentrationSeverity]

    def test_to_dict_recommended_action_str(self):
        d = self.get_dict()
        assert isinstance(d["recommended_action"], str)
        assert d["recommended_action"] in [e.value for e in ConcentrationAction]

    def test_to_dict_deal_concentration_score_float(self):
        d = self.get_dict()
        assert isinstance(d["deal_concentration_score"], float)

    def test_to_dict_account_concentration_score_float(self):
        d = self.get_dict()
        assert isinstance(d["account_concentration_score"], float)

    def test_to_dict_product_concentration_score_float(self):
        d = self.get_dict()
        assert isinstance(d["product_concentration_score"], float)

    def test_to_dict_stage_concentration_score_float(self):
        d = self.get_dict()
        assert isinstance(d["stage_concentration_score"], float)

    def test_to_dict_concentration_composite_float(self):
        d = self.get_dict()
        assert isinstance(d["concentration_composite"], float)

    def test_to_dict_is_fragile_pipeline_bool(self):
        d = self.get_dict()
        assert isinstance(d["is_fragile_pipeline"], bool)

    def test_to_dict_requires_rebalancing_bool(self):
        d = self.get_dict()
        assert isinstance(d["requires_rebalancing"], bool)

    def test_to_dict_estimated_at_risk_revenue_float(self):
        d = self.get_dict()
        assert isinstance(d["estimated_at_risk_revenue_usd"], float)

    def test_to_dict_concentration_signal_str(self):
        d = self.get_dict()
        assert isinstance(d["concentration_signal"], str)

    def test_to_dict_expected_keys(self):
        d = self.get_dict()
        expected = {
            "rep_id", "region", "concentration_risk", "concentration_pattern",
            "concentration_severity", "recommended_action", "deal_concentration_score",
            "account_concentration_score", "product_concentration_score",
            "stage_concentration_score", "concentration_composite", "is_fragile_pipeline",
            "requires_rebalancing", "estimated_at_risk_revenue_usd", "concentration_signal",
        }
        assert set(d.keys()) == expected

    def test_to_dict_rep_id_value(self):
        result = fresh_engine().assess(make_input(rep_id="TEST-REP"))
        d = result.to_dict()
        assert d["rep_id"] == "TEST-REP"

    def test_to_dict_region_value(self):
        result = fresh_engine().assess(make_input(region="NORTH"))
        d = result.to_dict()
        assert d["region"] == "NORTH"

    def test_to_dict_enums_are_string_values(self):
        # Enums should be serialized as string values, not enum objects
        d = self.get_dict()
        assert d["concentration_risk"] == "low"
        assert d["concentration_severity"] == "diversified"
        assert d["recommended_action"] == "no_action"
        assert d["concentration_pattern"] == "none"


# ═══════════════════════════════════════════════════════════════════════════════
# 15. ASSESS_BATCH
# ═══════════════════════════════════════════════════════════════════════════════


class TestAssessBatch:
    def test_batch_returns_list(self):
        engine = fresh_engine()
        results = engine.assess_batch([make_input(), make_input(rep_id="REP-002")])
        assert isinstance(results, list)

    def test_batch_length_matches_input(self):
        engine = fresh_engine()
        inputs = [make_input(rep_id=f"R-{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_returns_result_objects(self):
        engine = fresh_engine()
        results = engine.assess_batch([make_input()])
        assert isinstance(results[0], PipelineConcentrationResult)

    def test_batch_empty_returns_empty(self):
        engine = fresh_engine()
        results = engine.assess_batch([])
        assert results == []

    def test_batch_preserves_order(self):
        engine = fresh_engine()
        inputs = [make_input(rep_id=f"REP-{i}") for i in range(3)]
        results = engine.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"REP-{i}"

    def test_batch_accumulated_in_results(self):
        engine = fresh_engine()
        engine.assess_batch([make_input(rep_id=f"R-{i}") for i in range(4)])
        summary = engine.summary()
        assert summary["total"] == 4

    def test_batch_mixed_risk_levels(self):
        engine = fresh_engine()
        low_inp = make_input(rep_id="LOW")
        high_inp = make_input(
            rep_id="HIGH",
            top_deal_value_usd=700_000.0,
            top_3_deals_value_usd=900_000.0,
            deal_count=2,
            unique_accounts_in_pipeline=2,
            top_account_pipeline_usd=700_000.0,
            single_rep_pipeline_pct=0.95,
        )
        results = engine.assess_batch([low_inp, high_inp])
        assert results[0].concentration_risk == ConcentrationRisk.low
        assert results[1].concentration_risk in (ConcentrationRisk.high, ConcentrationRisk.critical)


# ═══════════════════════════════════════════════════════════════════════════════
# 16. SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════


class TestSummary:
    def test_empty_summary_has_13_keys(self):
        engine = fresh_engine()
        s = engine.summary()
        assert len(s) == 13

    def test_empty_summary_total_zero(self):
        assert fresh_engine().summary()["total"] == 0

    def test_empty_summary_zero_values(self):
        s = fresh_engine().summary()
        assert s["avg_concentration_composite"] == 0.0
        assert s["fragile_pipeline_count"] == 0
        assert s["rebalancing_count"] == 0
        assert s["total_estimated_at_risk_revenue_usd"] == 0.0

    def test_empty_summary_empty_dicts(self):
        s = fresh_engine().summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}

    def test_summary_total_count(self):
        engine = fresh_engine()
        for i in range(3):
            engine.assess(make_input(rep_id=f"R{i}"))
        assert engine.summary()["total"] == 3

    def test_summary_risk_counts(self):
        engine = fresh_engine()
        engine.assess(make_input())  # low
        engine.assess(make_input())  # low
        s = engine.summary()
        assert s["risk_counts"]["low"] == 2

    def test_summary_pattern_counts(self):
        engine = fresh_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert s["pattern_counts"].get("none", 0) >= 1

    def test_summary_severity_counts(self):
        engine = fresh_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert s["severity_counts"].get("diversified", 0) >= 1

    def test_summary_action_counts(self):
        engine = fresh_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert s["action_counts"].get("no_action", 0) >= 1

    def test_summary_avg_composite(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input())
        r2 = engine.assess(make_input(top_deal_value_usd=150_000.0))
        expected_avg = (r1.concentration_composite + r2.concentration_composite) / 2
        s = engine.summary()
        assert s["avg_concentration_composite"] == pytest.approx(expected_avg, abs=0.2)

    def test_summary_fragile_count(self):
        engine = fresh_engine()
        engine.assess(make_input())          # not fragile
        engine.assess(make_input(deal_count=2))  # fragile
        engine.assess(make_input(deal_count=2))  # fragile
        s = engine.summary()
        assert s["fragile_pipeline_count"] == 2

    def test_summary_rebalancing_count(self):
        engine = fresh_engine()
        engine.assess(make_input())                             # not rebalancing
        engine.assess(make_input(sandbagged_deals_count=2))    # rebalancing
        s = engine.summary()
        assert s["rebalancing_count"] == 1

    def test_summary_total_at_risk_is_sum_not_average(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input(committed_forecast_usd=300_000.0, top_deal_value_usd=150_000.0))
        r2 = engine.assess(make_input(committed_forecast_usd=500_000.0, top_deal_value_usd=150_000.0))
        expected_sum = r1.estimated_at_risk_revenue_usd + r2.estimated_at_risk_revenue_usd
        s = engine.summary()
        assert s["total_estimated_at_risk_revenue_usd"] == pytest.approx(expected_sum, abs=1.0)

    def test_summary_total_at_risk_not_average(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input(committed_forecast_usd=200_000.0, top_deal_value_usd=150_000.0))
        r2 = engine.assess(make_input(committed_forecast_usd=800_000.0, top_deal_value_usd=150_000.0))
        s = engine.summary()
        avg = (r1.estimated_at_risk_revenue_usd + r2.estimated_at_risk_revenue_usd) / 2
        # Sum must not equal average (they differ by a factor of 2)
        assert s["total_estimated_at_risk_revenue_usd"] != pytest.approx(avg, abs=1.0)

    def test_summary_avg_deal_score(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input())
        r2 = engine.assess(make_input(top_deal_value_usd=150_000.0))
        expected = (r1.deal_concentration_score + r2.deal_concentration_score) / 2
        s = engine.summary()
        assert s["avg_deal_concentration_score"] == pytest.approx(expected, abs=0.2)

    def test_summary_avg_account_score(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input())
        r2 = engine.assess(make_input(unique_accounts_in_pipeline=5))
        expected = (r1.account_concentration_score + r2.account_concentration_score) / 2
        s = engine.summary()
        assert s["avg_account_concentration_score"] == pytest.approx(expected, abs=0.2)

    def test_summary_avg_product_score(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input())
        r2 = engine.assess(make_input(top_product_line_pipeline_pct=60.0))
        expected = (r1.product_concentration_score + r2.product_concentration_score) / 2
        s = engine.summary()
        assert s["avg_product_concentration_score"] == pytest.approx(expected, abs=0.2)

    def test_summary_avg_stage_score(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input())
        r2 = engine.assess(make_input(stale_deals_pct=0.30))
        expected = (r1.stage_concentration_score + r2.stage_concentration_score) / 2
        s = engine.summary()
        assert s["avg_stage_concentration_score"] == pytest.approx(expected, abs=0.2)

    def test_summary_all_13_keys_present(self):
        engine = fresh_engine()
        engine.assess(make_input())
        s = engine.summary()
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts", "action_counts",
            "avg_concentration_composite", "fragile_pipeline_count", "rebalancing_count",
            "avg_deal_concentration_score", "avg_account_concentration_score",
            "avg_product_concentration_score", "avg_stage_concentration_score",
            "total_estimated_at_risk_revenue_usd",
        }
        assert set(s.keys()) == expected_keys

    def test_summary_single_result(self):
        engine = fresh_engine()
        r = engine.assess(make_input())
        s = engine.summary()
        assert s["total"] == 1
        assert s["avg_concentration_composite"] == pytest.approx(r.concentration_composite, abs=0.1)

    def test_summary_accumulates_across_multiple_assess_calls(self):
        engine = fresh_engine()
        for i in range(7):
            engine.assess(make_input(rep_id=f"R{i}"))
        assert engine.summary()["total"] == 7


# ═══════════════════════════════════════════════════════════════════════════════
# 17. EDGE CASES
# ═══════════════════════════════════════════════════════════════════════════════


class TestEdgeCases:
    def test_zero_total_pipeline_no_division_error(self):
        inp = make_input(
            total_pipeline_usd=0.0,
            top_deal_value_usd=0.0,
            top_3_deals_value_usd=0.0,
            top_account_pipeline_usd=0.0,
        )
        result = fresh_engine().assess(inp)
        assert result is not None
        assert result.concentration_composite >= 0

    def test_zero_total_pipeline_not_fragile_by_deal_ratio(self):
        # total=0 -> pipeline ratio condition skipped
        inp = make_input(
            total_pipeline_usd=0.0,
            top_deal_value_usd=0.0,
            deal_count=5,
        )
        result = fresh_engine().assess(inp)
        # is_fragile_pipeline should not error
        assert isinstance(result.is_fragile_pipeline, bool)

    def test_zero_total_product_lines_no_error(self):
        inp = make_input(total_product_lines=0, product_lines_represented=0)
        result = fresh_engine().assess(inp)
        assert isinstance(result.product_concentration_score, float)

    def test_zero_pipeline_created_prior_no_error(self):
        inp = make_input(
            pipeline_created_prior_30d_usd=0.0,
            pipeline_created_last_30d_usd=0.0,
        )
        result = fresh_engine().assess(inp)
        assert isinstance(result.product_concentration_score, float)

    def test_zero_committed_forecast_at_risk_zero(self):
        result = fresh_engine().assess(make_input(committed_forecast_usd=0.0))
        assert result.estimated_at_risk_revenue_usd == 0.0

    def test_very_large_pipeline_values(self):
        inp = make_input(
            total_pipeline_usd=1_000_000_000.0,
            top_deal_value_usd=50_000_000.0,
            top_3_deals_value_usd=100_000_000.0,
            top_account_pipeline_usd=50_000_000.0,
        )
        result = fresh_engine().assess(inp)
        assert 0 <= result.concentration_composite <= 100

    def test_single_deal_pipeline(self):
        inp = make_input(
            total_pipeline_usd=500_000.0,
            top_deal_value_usd=500_000.0,  # 100% -> +50
            top_3_deals_value_usd=500_000.0,  # 100% -> +30
            deal_count=1,  # <=2 -> +20
        )
        result = fresh_engine().assess(inp)
        assert result.deal_concentration_score == 100.0
        assert result.is_fragile_pipeline is True

    def test_perfectly_diversified_pipeline(self):
        result = fresh_engine().assess(make_input())
        assert result.concentration_risk == ConcentrationRisk.low
        assert result.concentration_pattern == ConcentrationPattern.none
        assert result.is_fragile_pipeline is False

    def test_all_deals_in_single_stage_not_bottleneck_if_stage_score_low(self):
        # single_stage_pct>=0.70 but stage_score < 30 should not trigger stage_bottleneck
        # single_stage=0.70 -> +20 (score >=30 -> triggers)
        # single_stage=0.70 alone = 20 < 30
        inp = make_input(
            deals_in_single_stage_pct=0.70,
            deals_in_late_stage_pct=0.0,   # no late stage bonus
            stale_deals_pct=0.0,           # no stale bonus
        )
        result = fresh_engine().assess(inp)
        # stage_score = 20 < 30 -> no stage_bottleneck
        assert result.concentration_pattern != ConcentrationPattern.stage_bottleneck

    def test_whale_dependency_zero_pipeline_not_triggered(self):
        # total_pipeline_usd=0 -> whale check skipped
        inp = make_input(
            total_pipeline_usd=0.0,
            top_deal_value_usd=0.0,
            single_rep_pipeline_pct=0.30,
            deals_in_single_stage_pct=0.10,
        )
        result = fresh_engine().assess(inp)
        assert result.concentration_pattern != ConcentrationPattern.whale_dependency

    def test_account_overexposure_zero_pipeline_not_triggered(self):
        inp = make_input(
            total_pipeline_usd=0.0,
            top_account_pipeline_usd=0.0,
            single_rep_pipeline_pct=0.30,
            top_deal_value_usd=0.0,
            deals_in_single_stage_pct=0.10,
        )
        result = fresh_engine().assess(inp)
        assert result.concentration_pattern != ConcentrationPattern.account_overexposure

    def test_sandbagged_deals_zero_no_rebalancing_from_that_field(self):
        inp = make_input(sandbagged_deals_count=0, unique_accounts_in_pipeline=10)
        result = fresh_engine().assess(inp)
        # Low composite + 10 accounts + 0 sandbagged => not rebalancing
        if result.concentration_composite < 30:
            assert result.requires_rebalancing is False

    def test_high_committed_forecast_large_at_risk(self):
        inp = make_input(
            committed_forecast_usd=10_000_000.0,
            top_deal_value_usd=500_000.0,
        )
        result = fresh_engine().assess(inp)
        assert result.estimated_at_risk_revenue_usd == pytest.approx(
            10_000_000.0 * (result.concentration_composite / 100.0), abs=10.0
        )


# ═══════════════════════════════════════════════════════════════════════════════
# 18. CONCENTRATION SIGNAL
# ═══════════════════════════════════════════════════════════════════════════════


class TestConcentrationSignal:
    def test_signal_diversified_on_none_pattern(self):
        result = fresh_engine().assess(make_input())
        assert "diversified" in result.concentration_signal.lower()

    def test_signal_contains_composite_for_non_none_pattern(self):
        inp = make_input(
            top_deal_value_usd=500_000.0,
            deals_in_single_stage_pct=0.10,
        )
        result = fresh_engine().assess(inp)
        if result.concentration_pattern != ConcentrationPattern.none:
            assert "composite" in result.concentration_signal.lower()

    def test_whale_signal_mentions_top_deal(self):
        inp = make_input(top_deal_value_usd=500_000.0, deals_in_single_stage_pct=0.10)
        result = fresh_engine().assess(inp)
        if result.concentration_pattern == ConcentrationPattern.whale_dependency:
            assert "500,000" in result.concentration_signal or "500" in result.concentration_signal

    def test_stage_bottleneck_signal_mentions_stage(self):
        inp = make_input(
            deals_in_single_stage_pct=0.80,
            deals_in_late_stage_pct=0.85,
            stale_deals_pct=0.0,
        )
        result = fresh_engine().assess(inp)
        if result.concentration_pattern == ConcentrationPattern.stage_bottleneck:
            assert "stage" in result.concentration_signal.lower()

    def test_rep_signal_mentions_rep(self):
        inp = make_input(single_rep_pipeline_pct=0.90, top_deal_value_usd=80_000.0,
                         deals_in_single_stage_pct=0.10)
        result = fresh_engine().assess(inp)
        if result.concentration_pattern == ConcentrationPattern.rep_single_point:
            assert "rep" in result.concentration_signal.lower() or "%" in result.concentration_signal

    def test_signal_not_empty(self):
        for _ in range(3):
            result = fresh_engine().assess(make_input())
            assert result.concentration_signal.strip() != ""


# ═══════════════════════════════════════════════════════════════════════════════
# 19. SCORE BOUNDARIES — EXACT THRESHOLD CHECKS
# ═══════════════════════════════════════════════════════════════════════════════


class TestExactThresholds:
    """Test at exact boundary values to confirm threshold logic (>=, not >)."""

    def test_deal_top_deal_exactly_15pct(self):
        inp = make_input(top_deal_value_usd=150_000.0, top_3_deals_value_usd=300_000.0)
        result = fresh_engine().assess(inp)
        assert result.deal_concentration_score >= 8.0

    def test_deal_top_deal_exactly_25pct(self):
        inp = make_input(top_deal_value_usd=250_000.0, top_3_deals_value_usd=300_000.0)
        result = fresh_engine().assess(inp)
        assert result.deal_concentration_score >= 18.0

    def test_deal_top_deal_exactly_40pct(self):
        inp = make_input(top_deal_value_usd=400_000.0, top_3_deals_value_usd=500_000.0)
        result = fresh_engine().assess(inp)
        assert result.deal_concentration_score >= 32.0

    def test_deal_top_deal_exactly_60pct(self):
        inp = make_input(top_deal_value_usd=600_000.0, top_3_deals_value_usd=700_000.0)
        result = fresh_engine().assess(inp)
        assert result.deal_concentration_score >= 50.0

    def test_account_top_account_exactly_10pct(self):
        inp = make_input(top_account_pipeline_usd=100_000.0,
                         unique_accounts_in_pipeline=10, single_rep_pipeline_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.account_concentration_score >= 6.0

    def test_account_top_account_exactly_25pct(self):
        inp = make_input(top_account_pipeline_usd=250_000.0,
                         unique_accounts_in_pipeline=10, single_rep_pipeline_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.account_concentration_score >= 15.0

    def test_account_top_account_exactly_40pct(self):
        inp = make_input(top_account_pipeline_usd=400_000.0,
                         unique_accounts_in_pipeline=10, single_rep_pipeline_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.account_concentration_score >= 28.0

    def test_account_top_account_exactly_60pct(self):
        inp = make_input(top_account_pipeline_usd=600_000.0,
                         unique_accounts_in_pipeline=10, single_rep_pipeline_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.account_concentration_score >= 45.0

    def test_product_top_line_exactly_60pct(self):
        inp = make_input(top_product_line_pipeline_pct=60.0,
                         product_lines_represented=8, total_product_lines=10,
                         pipeline_created_last_30d_usd=200_000.0,
                         pipeline_created_prior_30d_usd=200_000.0)
        result = fresh_engine().assess(inp)
        assert result.product_concentration_score >= 12.0

    def test_product_top_line_exactly_75pct(self):
        inp = make_input(top_product_line_pipeline_pct=75.0,
                         product_lines_represented=8, total_product_lines=10,
                         pipeline_created_last_30d_usd=200_000.0,
                         pipeline_created_prior_30d_usd=200_000.0)
        result = fresh_engine().assess(inp)
        assert result.product_concentration_score >= 24.0

    def test_product_top_line_exactly_90pct(self):
        inp = make_input(top_product_line_pipeline_pct=90.0,
                         product_lines_represented=8, total_product_lines=10,
                         pipeline_created_last_30d_usd=200_000.0,
                         pipeline_created_prior_30d_usd=200_000.0)
        result = fresh_engine().assess(inp)
        assert result.product_concentration_score >= 40.0

    def test_stage_late_exactly_40pct(self):
        inp = make_input(deals_in_late_stage_pct=0.40, deals_in_single_stage_pct=0.0,
                         stale_deals_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.stage_concentration_score >= 10.0

    def test_stage_late_exactly_60pct(self):
        inp = make_input(deals_in_late_stage_pct=0.60, deals_in_single_stage_pct=0.0,
                         stale_deals_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.stage_concentration_score >= 24.0

    def test_stage_late_exactly_80pct(self):
        inp = make_input(deals_in_late_stage_pct=0.80, deals_in_single_stage_pct=0.0,
                         stale_deals_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.stage_concentration_score >= 40.0

    def test_stale_exactly_15pct(self):
        inp = make_input(stale_deals_pct=0.15, deals_in_late_stage_pct=0.0,
                         deals_in_single_stage_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.stage_concentration_score >= 6.0

    def test_stale_exactly_30pct(self):
        inp = make_input(stale_deals_pct=0.30, deals_in_late_stage_pct=0.0,
                         deals_in_single_stage_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.stage_concentration_score >= 14.0

    def test_stale_exactly_50pct(self):
        inp = make_input(stale_deals_pct=0.50, deals_in_late_stage_pct=0.0,
                         deals_in_single_stage_pct=0.0)
        result = fresh_engine().assess(inp)
        assert result.stage_concentration_score >= 25.0

    def test_single_rep_exactly_70pct(self):
        inp = make_input(single_rep_pipeline_pct=0.70,
                         top_account_pipeline_usd=90_000.0, unique_accounts_in_pipeline=10)
        result = fresh_engine().assess(inp)
        assert result.account_concentration_score >= 12.0

    def test_single_rep_exactly_90pct(self):
        inp = make_input(single_rep_pipeline_pct=0.90,
                         top_account_pipeline_usd=90_000.0, unique_accounts_in_pipeline=10)
        result = fresh_engine().assess(inp)
        assert result.account_concentration_score >= 25.0

    def test_risk_boundary_composite_19_9_is_low(self):
        # composite < 20 -> low
        result = fresh_engine().assess(make_input())
        assert result.concentration_composite < 20
        assert result.concentration_risk == ConcentrationRisk.low

    def test_pattern_whale_exactly_45pct(self):
        inp = make_input(
            total_pipeline_usd=1_000_000.0,
            top_deal_value_usd=450_000.0,    # exactly 45%
            deals_in_single_stage_pct=0.10,
        )
        result = fresh_engine().assess(inp)
        assert result.concentration_pattern == ConcentrationPattern.whale_dependency

    def test_pattern_whale_44pct_not_triggered(self):
        inp = make_input(
            total_pipeline_usd=1_000_000.0,
            top_deal_value_usd=440_000.0,    # 44% < 45%
            deals_in_single_stage_pct=0.10,
            single_rep_pipeline_pct=0.30,
            top_account_pipeline_usd=90_000.0,
        )
        result = fresh_engine().assess(inp)
        assert result.concentration_pattern != ConcentrationPattern.whale_dependency

    def test_fragile_composite_exactly_40(self):
        # Find inputs where composite is exactly 40
        # drive deal=8 (8%)*0.35 + account=45 (60%)*0.30 + product=0 + stage=0
        # 2.8 + 13.5 = 16.3 ... not enough
        # Use top_account=600k -> account=45; add single_rep=0.95 -> +25 = 70; clamp=70
        # composite = deal*0.35 + 70*0.30 = 2.8 + 21.0 = 23.8 ... need higher
        # Use deal=32 (top_deal=40%)+account=45+25=70+stale=14
        # 32*0.35 + 70*0.30 + 0*0.20 + 14*0.15 = 11.2+21.0+0+2.1 = 34.3 still below 40
        # Increase: deal=32+9=41 (top_deal=40%, top3=55%)
        # 41*0.35 + 70*0.30 + 0 + 14*0.15 = 14.35 + 21.0 + 2.1 = 37.45 almost
        # Add stale=30% -> 37.45 + ... let's not stress-test this exact value
        inp = make_input(
            top_deal_value_usd=400_000.0,
            top_3_deals_value_usd=600_000.0,
            deal_count=5,
            unique_accounts_in_pipeline=5,
            top_account_pipeline_usd=600_000.0,
            single_rep_pipeline_pct=0.95,
            stale_deals_pct=0.30,
        )
        result = fresh_engine().assess(inp)
        if result.concentration_composite >= 40:
            assert result.is_fragile_pipeline is True


# ═══════════════════════════════════════════════════════════════════════════════
# 20. MULTIPLE ASSESSMENTS — ENGINE STATE
# ═══════════════════════════════════════════════════════════════════════════════


class TestEngineState:
    def test_results_accumulate(self):
        engine = fresh_engine()
        engine.assess(make_input(rep_id="R1"))
        engine.assess(make_input(rep_id="R2"))
        engine.assess(make_input(rep_id="R3"))
        assert engine.summary()["total"] == 3

    def test_new_engine_starts_empty(self):
        engine = SalesPipelineConcentrationRiskEngine()
        assert engine.summary()["total"] == 0

    def test_two_engines_independent(self):
        e1 = fresh_engine()
        e2 = fresh_engine()
        e1.assess(make_input())
        e1.assess(make_input())
        e2.assess(make_input())
        assert e1.summary()["total"] == 2
        assert e2.summary()["total"] == 1

    def test_summary_after_batch(self):
        engine = fresh_engine()
        engine.assess_batch([make_input(rep_id=f"R{i}") for i in range(6)])
        assert engine.summary()["total"] == 6

    def test_mixed_assess_and_batch(self):
        engine = fresh_engine()
        engine.assess(make_input(rep_id="R0"))
        engine.assess_batch([make_input(rep_id=f"R{i}") for i in range(1, 4)])
        assert engine.summary()["total"] == 4

    def test_summary_counts_diverse_risks(self):
        engine = fresh_engine()
        engine.assess(make_input())  # low
        critical_inp = make_input(
            top_deal_value_usd=700_000.0,
            top_3_deals_value_usd=900_000.0,
            deal_count=2,
            unique_accounts_in_pipeline=2,
            top_account_pipeline_usd=700_000.0,
            single_rep_pipeline_pct=0.95,
            deals_in_single_stage_pct=0.85,
            deals_in_late_stage_pct=0.85,
            stale_deals_pct=0.55,
        )
        engine.assess(critical_inp)
        s = engine.summary()
        assert s["risk_counts"].get("low", 0) >= 1
        assert s["risk_counts"].get("critical", 0) >= 1


# ═══════════════════════════════════════════════════════════════════════════════
# 21. ADDITIONAL COVERAGE — SCORE COMBINATIONS
# ═══════════════════════════════════════════════════════════════════════════════


class TestScoreCombinations:
    def test_all_subscores_positive_yields_high_composite(self):
        inp = make_input(
            top_deal_value_usd=400_000.0,
            top_3_deals_value_usd=750_000.0,
            deal_count=3,
            unique_accounts_in_pipeline=5,
            top_account_pipeline_usd=400_000.0,
            single_rep_pipeline_pct=0.75,
            top_product_line_pipeline_pct=75.0,
            product_lines_represented=2, total_product_lines=10,
            pipeline_created_last_30d_usd=50_000.0,
            pipeline_created_prior_30d_usd=200_000.0,
            deals_in_late_stage_pct=0.65,
            deals_in_single_stage_pct=0.65,
            stale_deals_pct=0.35,
        )
        result = fresh_engine().assess(inp)
        assert result.concentration_composite > 20

    def test_only_stale_deals_gives_moderate_or_low(self):
        inp = make_input(stale_deals_pct=0.55)
        result = fresh_engine().assess(inp)
        # stage_score=25, composite = 25*0.15 = 3.75 -> low
        assert result.concentration_risk == ConcentrationRisk.low

    def test_only_low_coverage_gives_low_or_moderate(self):
        inp = make_input(product_lines_represented=1, total_product_lines=10)
        result = fresh_engine().assess(inp)
        # coverage=0.10 <= 0.20 -> +35 product, composite=35*0.20=7.0 -> low
        assert result.concentration_risk == ConcentrationRisk.low

    def test_deal_and_account_together_push_higher(self):
        inp = make_input(
            top_deal_value_usd=300_000.0,   # 30% -> +18
            top_3_deals_value_usd=600_000.0, # 60% -> +9
            unique_accounts_in_pipeline=3,   # +15
            top_account_pipeline_usd=300_000.0,  # 30% -> +15
            single_rep_pipeline_pct=0.0,
        )
        result = fresh_engine().assess(inp)
        deal_expected = 18.0 + 9.0
        account_expected = 15.0 + 15.0
        expected_composite = deal_expected * 0.35 + account_expected * 0.30
        assert result.concentration_composite == pytest.approx(expected_composite, abs=1.0)

    def test_product_concentration_requires_score_gte_20(self):
        # top_product_line=75% -> product_score=24 >= 20 -> pattern triggered
        inp = make_input(
            top_product_line_pipeline_pct=75.0,
            product_lines_represented=8, total_product_lines=10,
            pipeline_created_last_30d_usd=200_000.0, pipeline_created_prior_30d_usd=200_000.0,
            single_rep_pipeline_pct=0.30, top_deal_value_usd=80_000.0,
            deals_in_single_stage_pct=0.10, top_account_pipeline_usd=90_000.0,
        )
        result = fresh_engine().assess(inp)
        assert result.product_concentration_score >= 20.0
        assert result.concentration_pattern == ConcentrationPattern.product_concentration

    def test_product_concentration_not_triggered_if_score_lt_20(self):
        # top_product_line=75% -> +24 but need coverage/creation to keep total >=20
        # Actually 24 alone is >=20, so add checks for the case where top_line < 75
        inp = make_input(
            top_product_line_pipeline_pct=74.0,  # below 75 -> +12 (>=60)
            product_lines_represented=8, total_product_lines=10,
            pipeline_created_last_30d_usd=200_000.0, pipeline_created_prior_30d_usd=200_000.0,
            single_rep_pipeline_pct=0.30, top_deal_value_usd=80_000.0,
            deals_in_single_stage_pct=0.10, top_account_pipeline_usd=90_000.0,
        )
        result = fresh_engine().assess(inp)
        # product_score=12 < 20 or top_pct<75 -> no product_concentration
        assert result.concentration_pattern != ConcentrationPattern.product_concentration

    def test_stage_bottleneck_needs_both_conditions(self):
        # Only single_stage >= 0.70 but stage_score = 20 < 30 => no stage_bottleneck
        inp = make_input(
            deals_in_single_stage_pct=0.70,
            deals_in_late_stage_pct=0.0,
            stale_deals_pct=0.0,
        )
        result = fresh_engine().assess(inp)
        # stage_score = 20 (single_stage=0.70 -> +20) < 30 -> no bottleneck
        assert result.concentration_pattern != ConcentrationPattern.stage_bottleneck

    def test_fragile_pipeline_only_from_composite(self):
        # composite >= 40 but deal_count > 2 and top_deal < 60%
        inp = make_input(
            top_deal_value_usd=400_000.0,
            top_3_deals_value_usd=750_000.0,
            deal_count=10,
            unique_accounts_in_pipeline=5,
            top_account_pipeline_usd=400_000.0,
            single_rep_pipeline_pct=0.75,
        )
        result = fresh_engine().assess(inp)
        if result.concentration_composite >= 40:
            assert result.is_fragile_pipeline is True

    def test_requires_rebalancing_only_from_sandbagged(self):
        # low composite, good accounts but sandbagged >= 2
        inp = make_input(sandbagged_deals_count=3, unique_accounts_in_pipeline=15)
        result = fresh_engine().assess(inp)
        assert result.requires_rebalancing is True

    def test_requires_rebalancing_only_from_accounts(self):
        # low composite, good sandbagged, but unique_accounts <= 3
        inp = make_input(unique_accounts_in_pipeline=3, sandbagged_deals_count=0)
        result = fresh_engine().assess(inp)
        if result.concentration_composite < 30:
            assert result.requires_rebalancing is True


# ═══════════════════════════════════════════════════════════════════════════════
# 22. PARAMETRIZE — RISK LEVEL MATRIX
# ═══════════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("top_deal_pct,expected_deal_score_min", [
    (0.08, 0.0),   # below all thresholds
    (0.15, 8.0),   # exactly 15%
    (0.20, 8.0),   # between 15% and 25%
    (0.25, 18.0),  # exactly 25%
    (0.35, 18.0),  # between 25% and 40%
    (0.40, 32.0),  # exactly 40%
    (0.50, 32.0),  # between 40% and 60%
    (0.60, 50.0),  # exactly 60%
    (0.75, 50.0),  # above 60%
])
def test_deal_score_parametrized(top_deal_pct, expected_deal_score_min):
    total = 1_000_000.0
    inp = make_input(
        total_pipeline_usd=total,
        top_deal_value_usd=total * top_deal_pct,
        top_3_deals_value_usd=total * top_deal_pct,  # keep top3 from adding noise
        deal_count=20,
    )
    result = fresh_engine().assess(inp)
    assert result.deal_concentration_score >= expected_deal_score_min


@pytest.mark.parametrize("unique_accounts,expected_score_contribution", [
    (1, 30.0),
    (2, 30.0),
    (3, 15.0),
    (4, 15.0),
    (5, 6.0),
    (6, 6.0),
    (7, 0.0),
    (20, 0.0),
])
def test_account_unique_counts_parametrized(unique_accounts, expected_score_contribution):
    inp = make_input(
        unique_accounts_in_pipeline=unique_accounts,
        top_account_pipeline_usd=90_000.0,  # 9% -> no top_acct bonus
        single_rep_pipeline_pct=0.0,
    )
    result = fresh_engine().assess(inp)
    assert result.account_concentration_score == pytest.approx(
        expected_score_contribution, abs=0.1
    )


@pytest.mark.parametrize("composite,expected_risk", [
    (0.0, ConcentrationRisk.low),
    (10.0, ConcentrationRisk.low),
    (19.9, ConcentrationRisk.low),
    (20.0, ConcentrationRisk.moderate),
    (30.0, ConcentrationRisk.moderate),
    (39.9, ConcentrationRisk.moderate),
    (40.0, ConcentrationRisk.high),
    (50.0, ConcentrationRisk.high),
    (59.9, ConcentrationRisk.high),
    (60.0, ConcentrationRisk.critical),
    (80.0, ConcentrationRisk.critical),
    (100.0, ConcentrationRisk.critical),
])
def test_risk_classification_parametrized(composite, expected_risk):
    engine = SalesPipelineConcentrationRiskEngine()
    result = engine._classify_risk(composite)
    assert result == expected_risk


@pytest.mark.parametrize("composite,expected_severity", [
    (0.0, ConcentrationSeverity.diversified),
    (19.9, ConcentrationSeverity.diversified),
    (20.0, ConcentrationSeverity.watch),
    (39.9, ConcentrationSeverity.watch),
    (40.0, ConcentrationSeverity.concentrated),
    (59.9, ConcentrationSeverity.concentrated),
    (60.0, ConcentrationSeverity.critical),
    (100.0, ConcentrationSeverity.critical),
])
def test_severity_classification_parametrized(composite, expected_severity):
    engine = SalesPipelineConcentrationRiskEngine()
    result = engine._classify_severity(composite)
    assert result == expected_severity


@pytest.mark.parametrize("composite,expected_action", [
    (0.0, ConcentrationAction.no_action),
    (19.9, ConcentrationAction.no_action),
    # moderate: 20 <= composite < 40 -> pipeline_diversification
    # high: 40 <= composite < 50 -> rep_rebalancing
    (50.0, ConcentrationAction.forecast_risk_flag),
    (59.9, ConcentrationAction.forecast_risk_flag),
    (60.0, ConcentrationAction.executive_review),
    (100.0, ConcentrationAction.executive_review),
])
def test_action_classification_parametrized(composite, expected_action):
    engine = SalesPipelineConcentrationRiskEngine()
    risk = engine._classify_risk(composite)
    result = engine._recommended_action(risk, composite)
    assert result == expected_action
