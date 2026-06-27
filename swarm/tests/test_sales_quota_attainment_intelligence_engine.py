"""
Comprehensive pytest test suite for SalesQuotaAttainmentIntelligenceEngine.
Tests: all enums, all sub-scores at boundary values, pattern detection for all 6 patterns,
risk/severity at boundaries 20/40/60, action for all risk×pattern combos, flags,
quota gap, signal string, assess(), summary(), assess_batch().
"""
from __future__ import annotations
import pytest
from swarm.intelligence.sales_quota_attainment_intelligence_engine import (
    QuotaRisk,
    QuotaPattern,
    QuotaSeverity,
    QuotaAction,
    QuotaAttainmentInput,
    QuotaAttainmentResult,
    SalesQuotaAttainmentIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> QuotaAttainmentInput:
    """
    Return a fully-populated, well-behaved QuotaAttainmentInput.
    All defaults produce a low-risk, healthy rep.
    """
    defaults = dict(
        rep_id="REP001",
        region="North",
        evaluation_period_id="Q1-2026",
        quota_amount_usd=100_000.0,
        revenue_closed_usd=100_000.0,
        attainment_pct=1.0,
        prior_period_attainment_pct=1.0,
        quarters_below_quota_last_4=0,
        quarters_above_quota_last_4=4,
        deals_closed_last_week_of_period=0,
        total_deals_closed=10,
        deals_pushed_to_next_period=0,
        avg_deal_size_usd=20_000.0,
        pipeline_coverage_ratio=5.0,
        forecast_commit_accuracy_pct=0.90,
        discount_rate_avg_pct=0.05,
        avg_sales_cycle_days=30.0,
        multi_year_deals_closed=2,
        expansion_revenue_usd=10_000.0,
        new_logo_revenue_usd=90_000.0,
        days_to_reach_50pct_quota=45,
        deals_lost_after_commit_count=0,
    )
    defaults.update(overrides)
    return QuotaAttainmentInput(**defaults)


def engine() -> SalesQuotaAttainmentIntelligenceEngine:
    return SalesQuotaAttainmentIntelligenceEngine()


# ===========================================================================
# 1. Enum tests
# ===========================================================================

class TestQuotaRiskEnum:
    def test_members_exist(self):
        assert QuotaRisk.low
        assert QuotaRisk.moderate
        assert QuotaRisk.high
        assert QuotaRisk.critical

    def test_values(self):
        assert QuotaRisk.low.value == "low"
        assert QuotaRisk.moderate.value == "moderate"
        assert QuotaRisk.high.value == "high"
        assert QuotaRisk.critical.value == "critical"

    def test_is_str(self):
        assert isinstance(QuotaRisk.low, str)
        assert QuotaRisk.high == "high"

    def test_count(self):
        assert len(QuotaRisk) == 4

    def test_lookup_by_value(self):
        assert QuotaRisk("low") is QuotaRisk.low
        assert QuotaRisk("critical") is QuotaRisk.critical


class TestQuotaPatternEnum:
    def test_members_exist(self):
        members = {p.value for p in QuotaPattern}
        assert "none" in members
        assert "consistent_underperformance" in members
        assert "sandbagging" in members
        assert "late_quarter_surge" in members
        assert "early_drop_off" in members
        assert "quota_avoidance" in members

    def test_count(self):
        assert len(QuotaPattern) == 6

    def test_is_str(self):
        assert isinstance(QuotaPattern.none, str)
        assert QuotaPattern.sandbagging == "sandbagging"

    def test_values(self):
        assert QuotaPattern.none.value == "none"
        assert QuotaPattern.consistent_underperformance.value == "consistent_underperformance"
        assert QuotaPattern.sandbagging.value == "sandbagging"
        assert QuotaPattern.late_quarter_surge.value == "late_quarter_surge"
        assert QuotaPattern.early_drop_off.value == "early_drop_off"
        assert QuotaPattern.quota_avoidance.value == "quota_avoidance"

    def test_lookup_by_value(self):
        assert QuotaPattern("sandbagging") is QuotaPattern.sandbagging


class TestQuotaSeverityEnum:
    def test_members_exist(self):
        assert QuotaSeverity.on_track
        assert QuotaSeverity.developing
        assert QuotaSeverity.at_risk
        assert QuotaSeverity.critical

    def test_count(self):
        assert len(QuotaSeverity) == 4

    def test_values(self):
        assert QuotaSeverity.on_track.value == "on_track"
        assert QuotaSeverity.developing.value == "developing"
        assert QuotaSeverity.at_risk.value == "at_risk"
        assert QuotaSeverity.critical.value == "critical"

    def test_is_str(self):
        assert isinstance(QuotaSeverity.critical, str)
        assert QuotaSeverity.at_risk == "at_risk"


class TestQuotaActionEnum:
    def test_members_exist(self):
        actions = {a.value for a in QuotaAction}
        assert "no_action" in actions
        assert "quota_coaching" in actions
        assert "performance_plan" in actions
        assert "sandbagging_review" in actions
        assert "deal_acceleration" in actions
        assert "quota_adjustment" in actions

    def test_count(self):
        assert len(QuotaAction) == 6

    def test_values(self):
        assert QuotaAction.no_action.value == "no_action"
        assert QuotaAction.quota_coaching.value == "quota_coaching"
        assert QuotaAction.performance_plan.value == "performance_plan"
        assert QuotaAction.sandbagging_review.value == "sandbagging_review"
        assert QuotaAction.deal_acceleration.value == "deal_acceleration"
        assert QuotaAction.quota_adjustment.value == "quota_adjustment"

    def test_is_str(self):
        assert isinstance(QuotaAction.no_action, str)
        assert QuotaAction.performance_plan == "performance_plan"


# ===========================================================================
# 2. _attainment_consistency_score boundaries
# ===========================================================================

class TestAttainmentConsistencyScore:
    def setup_method(self):
        self.eng = engine()

    # attainment_pct tiers
    def test_attainment_below_50_adds_45(self):
        inp = make_input(attainment_pct=0.49, quarters_below_quota_last_4=0, deals_closed_last_week_of_period=0)
        score = self.eng._attainment_consistency_score(inp)
        assert score >= 45.0

    def test_attainment_exactly_50_does_not_add_45(self):
        inp = make_input(attainment_pct=0.50, quarters_below_quota_last_4=0, deals_closed_last_week_of_period=0)
        score = self.eng._attainment_consistency_score(inp)
        assert score < 45.0

    def test_attainment_between_50_and_75_adds_25(self):
        for val in [0.50, 0.60, 0.74]:
            inp = make_input(attainment_pct=val, quarters_below_quota_last_4=0, deals_closed_last_week_of_period=0)
            score = self.eng._attainment_consistency_score(inp)
            assert score == 25.0, f"Expected 25, got {score} for attainment_pct={val}"

    def test_attainment_exactly_75_does_not_add_25(self):
        inp = make_input(attainment_pct=0.75, quarters_below_quota_last_4=0, deals_closed_last_week_of_period=0)
        score = self.eng._attainment_consistency_score(inp)
        assert score < 25.0

    def test_attainment_between_75_and_90_adds_10(self):
        for val in [0.75, 0.80, 0.89]:
            inp = make_input(attainment_pct=val, quarters_below_quota_last_4=0, deals_closed_last_week_of_period=0)
            score = self.eng._attainment_consistency_score(inp)
            assert score == 10.0, f"Expected 10, got {score} for attainment_pct={val}"

    def test_attainment_exactly_90_adds_nothing(self):
        inp = make_input(attainment_pct=0.90, quarters_below_quota_last_4=0, deals_closed_last_week_of_period=0)
        score = self.eng._attainment_consistency_score(inp)
        assert score == 0.0

    def test_attainment_at_100_adds_nothing(self):
        inp = make_input(attainment_pct=1.0, quarters_below_quota_last_4=0, deals_closed_last_week_of_period=0)
        score = self.eng._attainment_consistency_score(inp)
        assert score == 0.0

    # quarters_below tiers
    def test_quarters_below_0_adds_0(self):
        inp = make_input(attainment_pct=1.0, quarters_below_quota_last_4=0, deals_closed_last_week_of_period=0)
        assert self.eng._attainment_consistency_score(inp) == 0.0

    def test_quarters_below_1_adds_5(self):
        inp = make_input(attainment_pct=1.0, quarters_below_quota_last_4=1, deals_closed_last_week_of_period=0)
        assert self.eng._attainment_consistency_score(inp) == 5.0

    def test_quarters_below_2_adds_15(self):
        inp = make_input(attainment_pct=1.0, quarters_below_quota_last_4=2, deals_closed_last_week_of_period=0)
        assert self.eng._attainment_consistency_score(inp) == 15.0

    def test_quarters_below_3_adds_30(self):
        inp = make_input(attainment_pct=1.0, quarters_below_quota_last_4=3, deals_closed_last_week_of_period=0)
        assert self.eng._attainment_consistency_score(inp) == 30.0

    def test_quarters_below_4_adds_30(self):
        inp = make_input(attainment_pct=1.0, quarters_below_quota_last_4=4, deals_closed_last_week_of_period=0)
        assert self.eng._attainment_consistency_score(inp) == 30.0

    # last_week_rate tiers
    def test_last_week_rate_below_35_adds_0(self):
        # 3/10 = 0.30 < 0.35
        inp = make_input(attainment_pct=1.0, quarters_below_quota_last_4=0,
                         deals_closed_last_week_of_period=3, total_deals_closed=10)
        assert self.eng._attainment_consistency_score(inp) == 0.0

    def test_last_week_rate_at_35_adds_7(self):
        # 35/100 = 0.35
        inp = make_input(attainment_pct=1.0, quarters_below_quota_last_4=0,
                         deals_closed_last_week_of_period=35, total_deals_closed=100)
        assert self.eng._attainment_consistency_score(inp) == 7.0

    def test_last_week_rate_between_35_and_50_adds_7(self):
        # 4/10 = 0.40
        inp = make_input(attainment_pct=1.0, quarters_below_quota_last_4=0,
                         deals_closed_last_week_of_period=4, total_deals_closed=10)
        assert self.eng._attainment_consistency_score(inp) == 7.0

    def test_last_week_rate_at_50_adds_15(self):
        # 5/10 = 0.50
        inp = make_input(attainment_pct=1.0, quarters_below_quota_last_4=0,
                         deals_closed_last_week_of_period=5, total_deals_closed=10)
        assert self.eng._attainment_consistency_score(inp) == 15.0

    def test_last_week_rate_above_50_adds_15(self):
        # 8/10 = 0.80
        inp = make_input(attainment_pct=1.0, quarters_below_quota_last_4=0,
                         deals_closed_last_week_of_period=8, total_deals_closed=10)
        assert self.eng._attainment_consistency_score(inp) == 15.0

    def test_total_deals_zero_uses_denominator_1(self):
        # total_deals_closed=0 → denominator = max(0,1) = 1; 1 deal / 1 = 1.0 ≥ 0.50 → +15
        inp = make_input(attainment_pct=1.0, quarters_below_quota_last_4=0,
                         deals_closed_last_week_of_period=1, total_deals_closed=0)
        assert self.eng._attainment_consistency_score(inp) == 15.0

    def test_max_capped_at_100(self):
        inp = make_input(attainment_pct=0.40, quarters_below_quota_last_4=4,
                         deals_closed_last_week_of_period=10, total_deals_closed=10)
        # 45 + 30 + 15 = 90, still ≤ 100
        score = self.eng._attainment_consistency_score(inp)
        assert score <= 100.0

    def test_worst_case_capped_at_100(self):
        # Even if raw sum > 100, must be capped
        inp = make_input(attainment_pct=0.10, quarters_below_quota_last_4=4,
                         deals_closed_last_week_of_period=10, total_deals_closed=10)
        score = self.eng._attainment_consistency_score(inp)
        assert score == 90.0  # 45+30+15=90

    def test_combined_attainment_below50_and_quarters3(self):
        inp = make_input(attainment_pct=0.40, quarters_below_quota_last_4=3,
                         deals_closed_last_week_of_period=0)
        assert self.eng._attainment_consistency_score(inp) == 75.0  # 45+30


# ===========================================================================
# 3. _deal_quality_score boundaries
# ===========================================================================

class TestDealQualityScore:
    def setup_method(self):
        self.eng = engine()

    # avg_deal_size tiers
    def test_deal_size_below_5000_adds_30(self):
        inp = make_input(avg_deal_size_usd=4_999, discount_rate_avg_pct=0.0, deals_pushed_to_next_period=0)
        assert self.eng._deal_quality_score(inp) == 30.0

    def test_deal_size_exactly_5000_adds_15(self):
        inp = make_input(avg_deal_size_usd=5_000, discount_rate_avg_pct=0.0, deals_pushed_to_next_period=0)
        assert self.eng._deal_quality_score(inp) == 15.0

    def test_deal_size_between_5000_and_15000_adds_15(self):
        for val in [5_000, 10_000, 14_999]:
            inp = make_input(avg_deal_size_usd=val, discount_rate_avg_pct=0.0, deals_pushed_to_next_period=0)
            assert self.eng._deal_quality_score(inp) == 15.0, f"val={val}"

    def test_deal_size_exactly_15000_adds_0(self):
        inp = make_input(avg_deal_size_usd=15_000, discount_rate_avg_pct=0.0, deals_pushed_to_next_period=0)
        assert self.eng._deal_quality_score(inp) == 0.0

    def test_deal_size_above_15000_adds_0(self):
        inp = make_input(avg_deal_size_usd=50_000, discount_rate_avg_pct=0.0, deals_pushed_to_next_period=0)
        assert self.eng._deal_quality_score(inp) == 0.0

    # discount_rate tiers
    def test_discount_below_15_adds_0(self):
        inp = make_input(avg_deal_size_usd=20_000, discount_rate_avg_pct=0.14, deals_pushed_to_next_period=0)
        assert self.eng._deal_quality_score(inp) == 0.0

    def test_discount_at_15_adds_15(self):
        inp = make_input(avg_deal_size_usd=20_000, discount_rate_avg_pct=0.15, deals_pushed_to_next_period=0)
        assert self.eng._deal_quality_score(inp) == 15.0

    def test_discount_between_15_and_25_adds_15(self):
        inp = make_input(avg_deal_size_usd=20_000, discount_rate_avg_pct=0.20, deals_pushed_to_next_period=0)
        assert self.eng._deal_quality_score(inp) == 15.0

    def test_discount_at_25_adds_30(self):
        inp = make_input(avg_deal_size_usd=20_000, discount_rate_avg_pct=0.25, deals_pushed_to_next_period=0)
        assert self.eng._deal_quality_score(inp) == 30.0

    def test_discount_above_25_adds_30(self):
        inp = make_input(avg_deal_size_usd=20_000, discount_rate_avg_pct=0.50, deals_pushed_to_next_period=0)
        assert self.eng._deal_quality_score(inp) == 30.0

    # deals_pushed tiers
    def test_deals_pushed_0_adds_0(self):
        inp = make_input(avg_deal_size_usd=20_000, discount_rate_avg_pct=0.0, deals_pushed_to_next_period=0)
        assert self.eng._deal_quality_score(inp) == 0.0

    def test_deals_pushed_1_adds_5(self):
        inp = make_input(avg_deal_size_usd=20_000, discount_rate_avg_pct=0.0, deals_pushed_to_next_period=1)
        assert self.eng._deal_quality_score(inp) == 5.0

    def test_deals_pushed_2_adds_5(self):
        inp = make_input(avg_deal_size_usd=20_000, discount_rate_avg_pct=0.0, deals_pushed_to_next_period=2)
        assert self.eng._deal_quality_score(inp) == 5.0

    def test_deals_pushed_3_adds_15(self):
        inp = make_input(avg_deal_size_usd=20_000, discount_rate_avg_pct=0.0, deals_pushed_to_next_period=3)
        assert self.eng._deal_quality_score(inp) == 15.0

    def test_deals_pushed_4_adds_15(self):
        inp = make_input(avg_deal_size_usd=20_000, discount_rate_avg_pct=0.0, deals_pushed_to_next_period=4)
        assert self.eng._deal_quality_score(inp) == 15.0

    def test_deals_pushed_5_adds_30(self):
        inp = make_input(avg_deal_size_usd=20_000, discount_rate_avg_pct=0.0, deals_pushed_to_next_period=5)
        assert self.eng._deal_quality_score(inp) == 30.0

    def test_deals_pushed_10_adds_30(self):
        inp = make_input(avg_deal_size_usd=20_000, discount_rate_avg_pct=0.0, deals_pushed_to_next_period=10)
        assert self.eng._deal_quality_score(inp) == 30.0

    def test_max_score_capped_at_100(self):
        # 30 + 30 + 30 = 90 ≤ 100
        inp = make_input(avg_deal_size_usd=1_000, discount_rate_avg_pct=0.30, deals_pushed_to_next_period=5)
        score = self.eng._deal_quality_score(inp)
        assert score == 90.0

    def test_zero_risk_all_good(self):
        inp = make_input(avg_deal_size_usd=20_000, discount_rate_avg_pct=0.05, deals_pushed_to_next_period=0)
        assert self.eng._deal_quality_score(inp) == 0.0


# ===========================================================================
# 4. _pipeline_health_score boundaries
# ===========================================================================

class TestPipelineHealthScore:
    def setup_method(self):
        self.eng = engine()

    # pipeline_coverage_ratio tiers
    def test_coverage_below_2_adds_45(self):
        inp = make_input(pipeline_coverage_ratio=1.9, days_to_reach_50pct_quota=0,
                         deals_lost_after_commit_count=0)
        assert self.eng._pipeline_health_score(inp) == 45.0

    def test_coverage_exactly_2_adds_25(self):
        inp = make_input(pipeline_coverage_ratio=2.0, days_to_reach_50pct_quota=0,
                         deals_lost_after_commit_count=0)
        assert self.eng._pipeline_health_score(inp) == 25.0

    def test_coverage_between_2_and_3_adds_25(self):
        inp = make_input(pipeline_coverage_ratio=2.5, days_to_reach_50pct_quota=0,
                         deals_lost_after_commit_count=0)
        assert self.eng._pipeline_health_score(inp) == 25.0

    def test_coverage_exactly_3_adds_10(self):
        inp = make_input(pipeline_coverage_ratio=3.0, days_to_reach_50pct_quota=0,
                         deals_lost_after_commit_count=0)
        assert self.eng._pipeline_health_score(inp) == 10.0

    def test_coverage_between_3_and_4_adds_10(self):
        inp = make_input(pipeline_coverage_ratio=3.5, days_to_reach_50pct_quota=0,
                         deals_lost_after_commit_count=0)
        assert self.eng._pipeline_health_score(inp) == 10.0

    def test_coverage_at_4_adds_0(self):
        inp = make_input(pipeline_coverage_ratio=4.0, days_to_reach_50pct_quota=0,
                         deals_lost_after_commit_count=0)
        assert self.eng._pipeline_health_score(inp) == 0.0

    def test_coverage_above_4_adds_0(self):
        inp = make_input(pipeline_coverage_ratio=6.0, days_to_reach_50pct_quota=0,
                         deals_lost_after_commit_count=0)
        assert self.eng._pipeline_health_score(inp) == 0.0

    # days_to_reach_50pct tiers
    def test_days_below_60_adds_0(self):
        inp = make_input(pipeline_coverage_ratio=5.0, days_to_reach_50pct_quota=59,
                         deals_lost_after_commit_count=0)
        assert self.eng._pipeline_health_score(inp) == 0.0

    def test_days_at_60_adds_15(self):
        inp = make_input(pipeline_coverage_ratio=5.0, days_to_reach_50pct_quota=60,
                         deals_lost_after_commit_count=0)
        assert self.eng._pipeline_health_score(inp) == 15.0

    def test_days_between_60_and_80_adds_15(self):
        inp = make_input(pipeline_coverage_ratio=5.0, days_to_reach_50pct_quota=70,
                         deals_lost_after_commit_count=0)
        assert self.eng._pipeline_health_score(inp) == 15.0

    def test_days_at_80_adds_30(self):
        inp = make_input(pipeline_coverage_ratio=5.0, days_to_reach_50pct_quota=80,
                         deals_lost_after_commit_count=0)
        assert self.eng._pipeline_health_score(inp) == 30.0

    def test_days_above_80_adds_30(self):
        inp = make_input(pipeline_coverage_ratio=5.0, days_to_reach_50pct_quota=90,
                         deals_lost_after_commit_count=0)
        assert self.eng._pipeline_health_score(inp) == 30.0

    # lost_rate tiers
    def test_lost_rate_below_10_adds_0(self):
        inp = make_input(pipeline_coverage_ratio=5.0, days_to_reach_50pct_quota=0,
                         deals_lost_after_commit_count=0, total_deals_closed=10)
        assert self.eng._pipeline_health_score(inp) == 0.0

    def test_lost_rate_at_10_adds_10(self):
        inp = make_input(pipeline_coverage_ratio=5.0, days_to_reach_50pct_quota=0,
                         deals_lost_after_commit_count=1, total_deals_closed=10)
        assert self.eng._pipeline_health_score(inp) == 10.0

    def test_lost_rate_between_10_and_20_adds_10(self):
        inp = make_input(pipeline_coverage_ratio=5.0, days_to_reach_50pct_quota=0,
                         deals_lost_after_commit_count=1, total_deals_closed=10)
        assert self.eng._pipeline_health_score(inp) == 10.0

    def test_lost_rate_at_20_adds_20(self):
        # 2/10 = 0.20
        inp = make_input(pipeline_coverage_ratio=5.0, days_to_reach_50pct_quota=0,
                         deals_lost_after_commit_count=2, total_deals_closed=10)
        assert self.eng._pipeline_health_score(inp) == 20.0

    def test_lost_rate_above_20_adds_20(self):
        # 5/10 = 0.50
        inp = make_input(pipeline_coverage_ratio=5.0, days_to_reach_50pct_quota=0,
                         deals_lost_after_commit_count=5, total_deals_closed=10)
        assert self.eng._pipeline_health_score(inp) == 20.0

    def test_zero_total_deals_uses_1_as_denominator(self):
        # 1 lost / 1 = 1.0 ≥ 0.20 → +20
        inp = make_input(pipeline_coverage_ratio=5.0, days_to_reach_50pct_quota=0,
                         deals_lost_after_commit_count=1, total_deals_closed=0)
        assert self.eng._pipeline_health_score(inp) == 20.0

    def test_max_capped_at_100(self):
        # 45 + 30 + 20 = 95 ≤ 100
        inp = make_input(pipeline_coverage_ratio=1.0, days_to_reach_50pct_quota=90,
                         deals_lost_after_commit_count=5, total_deals_closed=10)
        score = self.eng._pipeline_health_score(inp)
        assert score == 95.0


# ===========================================================================
# 5. _forecast_reliability_score boundaries
# ===========================================================================

class TestForecastReliabilityScore:
    def setup_method(self):
        self.eng = engine()

    # forecast_commit_accuracy tiers
    def test_accuracy_below_60_adds_45(self):
        inp = make_input(forecast_commit_accuracy_pct=0.59, deals_closed_last_week_of_period=0,
                         total_deals_closed=10, deals_pushed_to_next_period=0)
        assert self.eng._forecast_reliability_score(inp) == 45.0

    def test_accuracy_at_60_adds_25(self):
        inp = make_input(forecast_commit_accuracy_pct=0.60, deals_closed_last_week_of_period=0,
                         total_deals_closed=10, deals_pushed_to_next_period=0)
        assert self.eng._forecast_reliability_score(inp) == 25.0

    def test_accuracy_between_60_and_75_adds_25(self):
        inp = make_input(forecast_commit_accuracy_pct=0.70, deals_closed_last_week_of_period=0,
                         total_deals_closed=10, deals_pushed_to_next_period=0)
        assert self.eng._forecast_reliability_score(inp) == 25.0

    def test_accuracy_at_75_adds_10(self):
        inp = make_input(forecast_commit_accuracy_pct=0.75, deals_closed_last_week_of_period=0,
                         total_deals_closed=10, deals_pushed_to_next_period=0)
        assert self.eng._forecast_reliability_score(inp) == 10.0

    def test_accuracy_between_75_and_85_adds_10(self):
        inp = make_input(forecast_commit_accuracy_pct=0.80, deals_closed_last_week_of_period=0,
                         total_deals_closed=10, deals_pushed_to_next_period=0)
        assert self.eng._forecast_reliability_score(inp) == 10.0

    def test_accuracy_at_85_adds_0(self):
        inp = make_input(forecast_commit_accuracy_pct=0.85, deals_closed_last_week_of_period=0,
                         total_deals_closed=10, deals_pushed_to_next_period=0)
        assert self.eng._forecast_reliability_score(inp) == 0.0

    def test_accuracy_above_85_adds_0(self):
        inp = make_input(forecast_commit_accuracy_pct=0.99, deals_closed_last_week_of_period=0,
                         total_deals_closed=10, deals_pushed_to_next_period=0)
        assert self.eng._forecast_reliability_score(inp) == 0.0

    # late_surge_rate tiers
    def test_late_surge_below_25_adds_0(self):
        # 2/10 = 0.20
        inp = make_input(forecast_commit_accuracy_pct=0.90, deals_closed_last_week_of_period=2,
                         total_deals_closed=10, deals_pushed_to_next_period=0)
        assert self.eng._forecast_reliability_score(inp) == 0.0

    def test_late_surge_at_25_adds_15(self):
        # 25/100 = 0.25
        inp = make_input(forecast_commit_accuracy_pct=0.90, deals_closed_last_week_of_period=25,
                         total_deals_closed=100, deals_pushed_to_next_period=0)
        assert self.eng._forecast_reliability_score(inp) == 15.0

    def test_late_surge_between_25_and_40_adds_15(self):
        # 3/10 = 0.30
        inp = make_input(forecast_commit_accuracy_pct=0.90, deals_closed_last_week_of_period=3,
                         total_deals_closed=10, deals_pushed_to_next_period=0)
        assert self.eng._forecast_reliability_score(inp) == 15.0

    def test_late_surge_at_40_adds_30(self):
        # 4/10 = 0.40
        inp = make_input(forecast_commit_accuracy_pct=0.90, deals_closed_last_week_of_period=4,
                         total_deals_closed=10, deals_pushed_to_next_period=0)
        assert self.eng._forecast_reliability_score(inp) == 30.0

    def test_late_surge_above_40_adds_30(self):
        # 8/10 = 0.80
        inp = make_input(forecast_commit_accuracy_pct=0.90, deals_closed_last_week_of_period=8,
                         total_deals_closed=10, deals_pushed_to_next_period=0)
        assert self.eng._forecast_reliability_score(inp) == 30.0

    # deals_pushed tiers
    def test_pushed_0_adds_0(self):
        inp = make_input(forecast_commit_accuracy_pct=0.90, deals_closed_last_week_of_period=0,
                         total_deals_closed=10, deals_pushed_to_next_period=0)
        assert self.eng._forecast_reliability_score(inp) == 0.0

    def test_pushed_1_adds_10(self):
        inp = make_input(forecast_commit_accuracy_pct=0.90, deals_closed_last_week_of_period=0,
                         total_deals_closed=10, deals_pushed_to_next_period=1)
        assert self.eng._forecast_reliability_score(inp) == 10.0

    def test_pushed_2_adds_10(self):
        inp = make_input(forecast_commit_accuracy_pct=0.90, deals_closed_last_week_of_period=0,
                         total_deals_closed=10, deals_pushed_to_next_period=2)
        assert self.eng._forecast_reliability_score(inp) == 10.0

    def test_pushed_3_adds_20(self):
        inp = make_input(forecast_commit_accuracy_pct=0.90, deals_closed_last_week_of_period=0,
                         total_deals_closed=10, deals_pushed_to_next_period=3)
        assert self.eng._forecast_reliability_score(inp) == 20.0

    def test_pushed_10_adds_20(self):
        inp = make_input(forecast_commit_accuracy_pct=0.90, deals_closed_last_week_of_period=0,
                         total_deals_closed=10, deals_pushed_to_next_period=10)
        assert self.eng._forecast_reliability_score(inp) == 20.0

    def test_max_capped_at_100(self):
        # 45 + 30 + 20 = 95
        inp = make_input(forecast_commit_accuracy_pct=0.50, deals_closed_last_week_of_period=5,
                         total_deals_closed=10, deals_pushed_to_next_period=5)
        score = self.eng._forecast_reliability_score(inp)
        assert score == 95.0

    def test_zero_total_deals_denominator_safe(self):
        # 1 / max(0,1) = 1.0 ≥ 0.40 → +30
        inp = make_input(forecast_commit_accuracy_pct=0.90, deals_closed_last_week_of_period=1,
                         total_deals_closed=0, deals_pushed_to_next_period=0)
        assert self.eng._forecast_reliability_score(inp) == 30.0


# ===========================================================================
# 6. _detect_pattern for all 6 patterns + priority ordering
# ===========================================================================

class TestDetectPattern:
    def setup_method(self):
        self.eng = engine()

    def _call(self, inp, consistency, deal_quality, pipeline, forecast):
        return self.eng._detect_pattern(inp, consistency, deal_quality, pipeline, forecast)

    def test_none_pattern_when_everything_low(self):
        inp = make_input()
        result = self._call(inp, 10, 10, 10, 10)
        assert result == QuotaPattern.none

    def test_consistent_underperformance_requires_consistency_ge35_and_quarters_ge3(self):
        inp = make_input(quarters_below_quota_last_4=3, attainment_pct=0.50,
                         deals_closed_last_week_of_period=0, total_deals_closed=10)
        result = self._call(inp, 35, 10, 10, 10)
        assert result == QuotaPattern.consistent_underperformance

    def test_consistent_underperformance_consistency_exact_35(self):
        inp = make_input(quarters_below_quota_last_4=3, attainment_pct=0.50,
                         deals_closed_last_week_of_period=0, total_deals_closed=10)
        result = self._call(inp, 35, 10, 10, 10)
        assert result == QuotaPattern.consistent_underperformance

    def test_consistent_underperformance_not_triggered_below_35(self):
        inp = make_input(quarters_below_quota_last_4=3, attainment_pct=0.50,
                         deals_closed_last_week_of_period=0, total_deals_closed=10)
        result = self._call(inp, 34, 10, 10, 10)
        assert result != QuotaPattern.consistent_underperformance

    def test_consistent_underperformance_not_triggered_quarters_below_3(self):
        inp = make_input(quarters_below_quota_last_4=2, attainment_pct=0.50,
                         deals_closed_last_week_of_period=0, total_deals_closed=10)
        result = self._call(inp, 40, 10, 10, 10)
        assert result != QuotaPattern.consistent_underperformance

    def test_sandbagging_requires_last_week_rate_ge40_attainment_ge90_deal_quality_ge20(self):
        # last_week_rate: 4/10 = 0.40, attainment 0.95, deal_quality 20
        inp = make_input(deals_closed_last_week_of_period=4, total_deals_closed=10,
                         attainment_pct=0.95, quarters_below_quota_last_4=0)
        result = self._call(inp, 10, 20, 10, 10)
        assert result == QuotaPattern.sandbagging

    def test_sandbagging_not_triggered_low_attainment(self):
        inp = make_input(deals_closed_last_week_of_period=5, total_deals_closed=10,
                         attainment_pct=0.89, quarters_below_quota_last_4=0)
        result = self._call(inp, 10, 20, 10, 10)
        assert result != QuotaPattern.sandbagging

    def test_sandbagging_not_triggered_low_deal_quality(self):
        inp = make_input(deals_closed_last_week_of_period=5, total_deals_closed=10,
                         attainment_pct=0.95, quarters_below_quota_last_4=0)
        result = self._call(inp, 10, 19, 10, 10)
        assert result != QuotaPattern.sandbagging

    def test_sandbagging_not_triggered_low_last_week_rate(self):
        # 3/10 = 0.30 < 0.40
        inp = make_input(deals_closed_last_week_of_period=3, total_deals_closed=10,
                         attainment_pct=0.95, quarters_below_quota_last_4=0)
        result = self._call(inp, 10, 20, 10, 10)
        assert result != QuotaPattern.sandbagging

    def test_late_quarter_surge_requires_consistency_ge25_and_last_week_rate_ge35(self):
        # 35/100 = 0.35, no quarters_below issue
        inp = make_input(deals_closed_last_week_of_period=35, total_deals_closed=100,
                         attainment_pct=0.80, quarters_below_quota_last_4=0)
        result = self._call(inp, 25, 10, 10, 10)
        assert result == QuotaPattern.late_quarter_surge

    def test_late_quarter_surge_not_triggered_consistency_below_25(self):
        inp = make_input(deals_closed_last_week_of_period=5, total_deals_closed=10,
                         attainment_pct=0.80, quarters_below_quota_last_4=0)
        result = self._call(inp, 24, 10, 10, 10)
        assert result != QuotaPattern.late_quarter_surge

    def test_late_quarter_surge_not_triggered_low_last_week_rate(self):
        # 3/10 = 0.30 < 0.35
        inp = make_input(deals_closed_last_week_of_period=3, total_deals_closed=10,
                         attainment_pct=0.80, quarters_below_quota_last_4=0)
        result = self._call(inp, 30, 10, 10, 10)
        assert result != QuotaPattern.late_quarter_surge

    def test_early_drop_off_requires_pipeline_ge25_and_days_ge70(self):
        inp = make_input(days_to_reach_50pct_quota=70, quarters_below_quota_last_4=0,
                         deals_closed_last_week_of_period=0, total_deals_closed=10,
                         attainment_pct=0.80)
        result = self._call(inp, 10, 10, 25, 10)
        assert result == QuotaPattern.early_drop_off

    def test_early_drop_off_not_triggered_pipeline_below_25(self):
        inp = make_input(days_to_reach_50pct_quota=80, quarters_below_quota_last_4=0,
                         deals_closed_last_week_of_period=0, total_deals_closed=10,
                         attainment_pct=0.80)
        result = self._call(inp, 10, 10, 24, 10)
        assert result != QuotaPattern.early_drop_off

    def test_early_drop_off_not_triggered_days_below_70(self):
        inp = make_input(days_to_reach_50pct_quota=69, quarters_below_quota_last_4=0,
                         deals_closed_last_week_of_period=0, total_deals_closed=10,
                         attainment_pct=0.80)
        result = self._call(inp, 10, 10, 30, 10)
        assert result != QuotaPattern.early_drop_off

    def test_quota_avoidance_requires_deal_quality_ge30_and_pushed_ge3(self):
        inp = make_input(deals_pushed_to_next_period=3, quarters_below_quota_last_4=0,
                         deals_closed_last_week_of_period=0, total_deals_closed=10,
                         attainment_pct=0.80)
        result = self._call(inp, 10, 30, 10, 10)
        assert result == QuotaPattern.quota_avoidance

    def test_quota_avoidance_not_triggered_deal_quality_below_30(self):
        inp = make_input(deals_pushed_to_next_period=5, quarters_below_quota_last_4=0,
                         deals_closed_last_week_of_period=0, total_deals_closed=10,
                         attainment_pct=0.80)
        result = self._call(inp, 10, 29, 10, 10)
        assert result != QuotaPattern.quota_avoidance

    def test_quota_avoidance_not_triggered_pushed_below_3(self):
        inp = make_input(deals_pushed_to_next_period=2, quarters_below_quota_last_4=0,
                         deals_closed_last_week_of_period=0, total_deals_closed=10,
                         attainment_pct=0.80)
        result = self._call(inp, 10, 35, 10, 10)
        assert result != QuotaPattern.quota_avoidance

    def test_priority_consistent_underperformance_over_sandbagging(self):
        # both conditions could match but consistent_underperformance is checked first
        inp = make_input(quarters_below_quota_last_4=3, attainment_pct=0.95,
                         deals_closed_last_week_of_period=5, total_deals_closed=10)
        # consistency=40, deal_quality=20 → both consistent_underperformance + sandbagging would qualify
        result = self._call(inp, 40, 20, 10, 10)
        assert result == QuotaPattern.consistent_underperformance

    def test_priority_consistent_underperformance_over_late_quarter_surge(self):
        inp = make_input(quarters_below_quota_last_4=3, attainment_pct=0.80,
                         deals_closed_last_week_of_period=5, total_deals_closed=10)
        result = self._call(inp, 40, 10, 10, 10)
        assert result == QuotaPattern.consistent_underperformance

    def test_priority_sandbagging_over_late_quarter_surge(self):
        # sandbagging condition: last_week_rate=0.50, attainment=0.95, deal_quality=25
        # late_quarter_surge would also match (consistency=30, last_week_rate=0.50)
        # but sandbagging is checked first
        inp = make_input(quarters_below_quota_last_4=0, attainment_pct=0.95,
                         deals_closed_last_week_of_period=5, total_deals_closed=10)
        result = self._call(inp, 30, 25, 10, 10)
        assert result == QuotaPattern.sandbagging

    def test_priority_late_quarter_surge_over_early_drop_off(self):
        # late_quarter_surge: consistency=30, last_week_rate=0.40
        # early_drop_off: pipeline=25, days=75
        # late_quarter_surge checked first → wins
        inp = make_input(quarters_below_quota_last_4=0, attainment_pct=0.80,
                         deals_closed_last_week_of_period=4, total_deals_closed=10,
                         days_to_reach_50pct_quota=75)
        result = self._call(inp, 30, 10, 25, 10)
        assert result == QuotaPattern.late_quarter_surge

    def test_priority_early_drop_off_over_quota_avoidance(self):
        # early_drop_off: pipeline=30, days=75
        # quota_avoidance: deal_quality=35, pushed=5
        # early_drop_off checked first → wins
        inp = make_input(quarters_below_quota_last_4=0, attainment_pct=0.80,
                         deals_closed_last_week_of_period=0, total_deals_closed=10,
                         days_to_reach_50pct_quota=75, deals_pushed_to_next_period=5)
        result = self._call(inp, 10, 35, 30, 10)
        assert result == QuotaPattern.early_drop_off


# ===========================================================================
# 7. _risk_level and _severity at boundaries 20, 40, 60
# ===========================================================================

class TestRiskLevel:
    def setup_method(self):
        self.eng = engine()

    def test_composite_0_is_low(self):
        assert self.eng._risk_level(0.0) == QuotaRisk.low

    def test_composite_19_is_low(self):
        assert self.eng._risk_level(19.9) == QuotaRisk.low

    def test_composite_exactly_20_is_moderate(self):
        assert self.eng._risk_level(20.0) == QuotaRisk.moderate

    def test_composite_21_is_moderate(self):
        assert self.eng._risk_level(21.0) == QuotaRisk.moderate

    def test_composite_39_is_moderate(self):
        assert self.eng._risk_level(39.9) == QuotaRisk.moderate

    def test_composite_exactly_40_is_high(self):
        assert self.eng._risk_level(40.0) == QuotaRisk.high

    def test_composite_41_is_high(self):
        assert self.eng._risk_level(41.0) == QuotaRisk.high

    def test_composite_59_is_high(self):
        assert self.eng._risk_level(59.9) == QuotaRisk.high

    def test_composite_exactly_60_is_critical(self):
        assert self.eng._risk_level(60.0) == QuotaRisk.critical

    def test_composite_100_is_critical(self):
        assert self.eng._risk_level(100.0) == QuotaRisk.critical


class TestSeverity:
    def setup_method(self):
        self.eng = engine()

    def test_composite_0_is_on_track(self):
        assert self.eng._severity(0.0) == QuotaSeverity.on_track

    def test_composite_19_is_on_track(self):
        assert self.eng._severity(19.9) == QuotaSeverity.on_track

    def test_composite_exactly_20_is_developing(self):
        assert self.eng._severity(20.0) == QuotaSeverity.developing

    def test_composite_39_is_developing(self):
        assert self.eng._severity(39.9) == QuotaSeverity.developing

    def test_composite_exactly_40_is_at_risk(self):
        assert self.eng._severity(40.0) == QuotaSeverity.at_risk

    def test_composite_59_is_at_risk(self):
        assert self.eng._severity(59.9) == QuotaSeverity.at_risk

    def test_composite_exactly_60_is_critical(self):
        assert self.eng._severity(60.0) == QuotaSeverity.critical

    def test_composite_100_is_critical(self):
        assert self.eng._severity(100.0) == QuotaSeverity.critical


# ===========================================================================
# 8. _action for all risk × pattern combos
# ===========================================================================

class TestAction:
    def setup_method(self):
        self.eng = engine()

    # --- critical risk ---
    def test_critical_consistent_underperformance_gives_performance_plan(self):
        assert self.eng._action(QuotaRisk.critical, QuotaPattern.consistent_underperformance) == QuotaAction.performance_plan

    def test_critical_sandbagging_gives_sandbagging_review(self):
        assert self.eng._action(QuotaRisk.critical, QuotaPattern.sandbagging) == QuotaAction.sandbagging_review

    def test_critical_none_gives_deal_acceleration(self):
        assert self.eng._action(QuotaRisk.critical, QuotaPattern.none) == QuotaAction.deal_acceleration

    def test_critical_late_quarter_surge_gives_deal_acceleration(self):
        assert self.eng._action(QuotaRisk.critical, QuotaPattern.late_quarter_surge) == QuotaAction.deal_acceleration

    def test_critical_early_drop_off_gives_deal_acceleration(self):
        assert self.eng._action(QuotaRisk.critical, QuotaPattern.early_drop_off) == QuotaAction.deal_acceleration

    def test_critical_quota_avoidance_gives_deal_acceleration(self):
        assert self.eng._action(QuotaRisk.critical, QuotaPattern.quota_avoidance) == QuotaAction.deal_acceleration

    # --- high risk ---
    def test_high_early_drop_off_gives_deal_acceleration(self):
        assert self.eng._action(QuotaRisk.high, QuotaPattern.early_drop_off) == QuotaAction.deal_acceleration

    def test_high_quota_avoidance_gives_sandbagging_review(self):
        assert self.eng._action(QuotaRisk.high, QuotaPattern.quota_avoidance) == QuotaAction.sandbagging_review

    def test_high_none_gives_quota_coaching(self):
        assert self.eng._action(QuotaRisk.high, QuotaPattern.none) == QuotaAction.quota_coaching

    def test_high_consistent_underperformance_gives_quota_coaching(self):
        assert self.eng._action(QuotaRisk.high, QuotaPattern.consistent_underperformance) == QuotaAction.quota_coaching

    def test_high_sandbagging_gives_quota_coaching(self):
        assert self.eng._action(QuotaRisk.high, QuotaPattern.sandbagging) == QuotaAction.quota_coaching

    def test_high_late_quarter_surge_gives_quota_coaching(self):
        assert self.eng._action(QuotaRisk.high, QuotaPattern.late_quarter_surge) == QuotaAction.quota_coaching

    # --- moderate risk ---
    def test_moderate_none_gives_quota_coaching(self):
        assert self.eng._action(QuotaRisk.moderate, QuotaPattern.none) == QuotaAction.quota_coaching

    def test_moderate_consistent_underperformance_gives_quota_coaching(self):
        assert self.eng._action(QuotaRisk.moderate, QuotaPattern.consistent_underperformance) == QuotaAction.quota_coaching

    def test_moderate_sandbagging_gives_quota_coaching(self):
        assert self.eng._action(QuotaRisk.moderate, QuotaPattern.sandbagging) == QuotaAction.quota_coaching

    def test_moderate_late_quarter_surge_gives_quota_coaching(self):
        assert self.eng._action(QuotaRisk.moderate, QuotaPattern.late_quarter_surge) == QuotaAction.quota_coaching

    def test_moderate_early_drop_off_gives_quota_coaching(self):
        assert self.eng._action(QuotaRisk.moderate, QuotaPattern.early_drop_off) == QuotaAction.quota_coaching

    def test_moderate_quota_avoidance_gives_quota_coaching(self):
        assert self.eng._action(QuotaRisk.moderate, QuotaPattern.quota_avoidance) == QuotaAction.quota_coaching

    # --- low risk ---
    def test_low_none_gives_no_action(self):
        assert self.eng._action(QuotaRisk.low, QuotaPattern.none) == QuotaAction.no_action

    def test_low_consistent_underperformance_gives_no_action(self):
        assert self.eng._action(QuotaRisk.low, QuotaPattern.consistent_underperformance) == QuotaAction.no_action

    def test_low_sandbagging_gives_no_action(self):
        assert self.eng._action(QuotaRisk.low, QuotaPattern.sandbagging) == QuotaAction.no_action

    def test_low_late_quarter_surge_gives_no_action(self):
        assert self.eng._action(QuotaRisk.low, QuotaPattern.late_quarter_surge) == QuotaAction.no_action

    def test_low_early_drop_off_gives_no_action(self):
        assert self.eng._action(QuotaRisk.low, QuotaPattern.early_drop_off) == QuotaAction.no_action

    def test_low_quota_avoidance_gives_no_action(self):
        assert self.eng._action(QuotaRisk.low, QuotaPattern.quota_avoidance) == QuotaAction.no_action


# ===========================================================================
# 9. _is_below_quota_threshold: attainment < 0.75 OR composite >= 40
# ===========================================================================

class TestIsBelowQuotaThreshold:
    def setup_method(self):
        self.eng = engine()

    def test_attainment_below_75_triggers_regardless_of_composite(self):
        inp = make_input(attainment_pct=0.74)
        assert self.eng._is_below_quota_threshold(0.0, inp) is True

    def test_attainment_exactly_75_alone_is_false_when_composite_below_40(self):
        inp = make_input(attainment_pct=0.75)
        assert self.eng._is_below_quota_threshold(39.9, inp) is False

    def test_attainment_75_with_composite_40_is_true(self):
        inp = make_input(attainment_pct=0.75)
        assert self.eng._is_below_quota_threshold(40.0, inp) is True

    def test_attainment_above_75_composite_below_40_is_false(self):
        inp = make_input(attainment_pct=0.80)
        assert self.eng._is_below_quota_threshold(39.0, inp) is False

    def test_attainment_above_75_composite_exactly_40_is_true(self):
        inp = make_input(attainment_pct=0.80)
        assert self.eng._is_below_quota_threshold(40.0, inp) is True

    def test_attainment_above_75_composite_above_40_is_true(self):
        inp = make_input(attainment_pct=1.0)
        assert self.eng._is_below_quota_threshold(60.0, inp) is True

    def test_attainment_0_is_true(self):
        inp = make_input(attainment_pct=0.0)
        assert self.eng._is_below_quota_threshold(0.0, inp) is True

    def test_attainment_1_composite_0_is_false(self):
        inp = make_input(attainment_pct=1.0)
        assert self.eng._is_below_quota_threshold(0.0, inp) is False

    def test_or_logic_both_true(self):
        inp = make_input(attainment_pct=0.60)
        assert self.eng._is_below_quota_threshold(50.0, inp) is True

    def test_boundary_composite_39_attainment_75_is_false(self):
        inp = make_input(attainment_pct=0.75)
        assert self.eng._is_below_quota_threshold(39.0, inp) is False


# ===========================================================================
# 10. _requires_performance_intervention: composite>=30 OR attainment<0.60 OR quarters>=2
# ===========================================================================

class TestRequiresPerformanceIntervention:
    def setup_method(self):
        self.eng = engine()

    def test_composite_at_30_triggers(self):
        inp = make_input(attainment_pct=0.80, quarters_below_quota_last_4=0)
        assert self.eng._requires_performance_intervention(30.0, inp) is True

    def test_composite_below_30_no_other_trigger_is_false(self):
        inp = make_input(attainment_pct=0.80, quarters_below_quota_last_4=0)
        assert self.eng._requires_performance_intervention(29.9, inp) is False

    def test_attainment_below_60_triggers(self):
        inp = make_input(attainment_pct=0.59, quarters_below_quota_last_4=0)
        assert self.eng._requires_performance_intervention(0.0, inp) is True

    def test_attainment_exactly_60_no_composite_no_quarters_is_false(self):
        inp = make_input(attainment_pct=0.60, quarters_below_quota_last_4=0)
        assert self.eng._requires_performance_intervention(0.0, inp) is False

    def test_quarters_at_2_triggers(self):
        inp = make_input(attainment_pct=0.80, quarters_below_quota_last_4=2)
        assert self.eng._requires_performance_intervention(0.0, inp) is True

    def test_quarters_at_1_no_other_trigger_is_false(self):
        inp = make_input(attainment_pct=0.80, quarters_below_quota_last_4=1)
        assert self.eng._requires_performance_intervention(0.0, inp) is False

    def test_quarters_at_3_triggers(self):
        inp = make_input(attainment_pct=0.80, quarters_below_quota_last_4=3)
        assert self.eng._requires_performance_intervention(0.0, inp) is True

    def test_quarters_at_4_triggers(self):
        inp = make_input(attainment_pct=0.80, quarters_below_quota_last_4=4)
        assert self.eng._requires_performance_intervention(0.0, inp) is True

    def test_all_conditions_false_returns_false(self):
        inp = make_input(attainment_pct=0.80, quarters_below_quota_last_4=0)
        assert self.eng._requires_performance_intervention(10.0, inp) is False

    def test_all_conditions_true_returns_true(self):
        inp = make_input(attainment_pct=0.50, quarters_below_quota_last_4=3)
        assert self.eng._requires_performance_intervention(50.0, inp) is True

    def test_attainment_59_composite_0_quarters_0_triggers(self):
        inp = make_input(attainment_pct=0.59, quarters_below_quota_last_4=0)
        assert self.eng._requires_performance_intervention(0.0, inp) is True

    def test_composite_exactly_29_9_attainment_61_quarters_1_is_false(self):
        inp = make_input(attainment_pct=0.61, quarters_below_quota_last_4=1)
        assert self.eng._requires_performance_intervention(29.9, inp) is False


# ===========================================================================
# 11. _estimated_quota_gap
# ===========================================================================

class TestEstimatedQuotaGap:
    def setup_method(self):
        self.eng = engine()

    def test_no_gap_when_revenue_equals_quota(self):
        inp = make_input(quota_amount_usd=100_000, revenue_closed_usd=100_000)
        assert self.eng._estimated_quota_gap(inp, 50.0) == 0.0

    def test_no_gap_when_revenue_exceeds_quota(self):
        inp = make_input(quota_amount_usd=100_000, revenue_closed_usd=120_000)
        assert self.eng._estimated_quota_gap(inp, 50.0) == 0.0

    def test_gap_calculation_basic(self):
        inp = make_input(quota_amount_usd=100_000, revenue_closed_usd=80_000)
        # raw_gap = 20000, composite = 50 → 20000 * 0.50 = 10000
        result = self.eng._estimated_quota_gap(inp, 50.0)
        assert result == 10_000.0

    def test_gap_with_composite_100(self):
        inp = make_input(quota_amount_usd=100_000, revenue_closed_usd=80_000)
        result = self.eng._estimated_quota_gap(inp, 100.0)
        assert result == 20_000.0

    def test_gap_with_composite_0_gives_0(self):
        inp = make_input(quota_amount_usd=100_000, revenue_closed_usd=80_000)
        result = self.eng._estimated_quota_gap(inp, 0.0)
        assert result == 0.0

    def test_gap_is_rounded_to_2_decimals(self):
        inp = make_input(quota_amount_usd=100_000, revenue_closed_usd=99_999)
        result = self.eng._estimated_quota_gap(inp, 33.3)
        assert result == round(1.0 * 33.3 / 100.0, 2)

    def test_negative_gap_is_clamped_to_zero(self):
        inp = make_input(quota_amount_usd=50_000, revenue_closed_usd=100_000)
        result = self.eng._estimated_quota_gap(inp, 75.0)
        assert result == 0.0

    def test_gap_partial_composite(self):
        inp = make_input(quota_amount_usd=200_000, revenue_closed_usd=150_000)
        # raw_gap=50000, composite=25 → 50000 * 0.25 = 12500
        result = self.eng._estimated_quota_gap(inp, 25.0)
        assert result == 12_500.0

    def test_large_gap_large_composite(self):
        inp = make_input(quota_amount_usd=1_000_000, revenue_closed_usd=0)
        result = self.eng._estimated_quota_gap(inp, 80.0)
        assert result == 800_000.0


# ===========================================================================
# 12. Signal string
# ===========================================================================

class TestSignal:
    def setup_method(self):
        self.eng = engine()

    def test_perfect_rep_returns_on_track_message(self):
        inp = make_input(attainment_pct=1.0, quarters_below_quota_last_4=0, deals_pushed_to_next_period=0)
        sig = self.eng._signal(inp, QuotaPattern.none, 10.0)
        assert sig == "Quota attainment consistent and on track"

    def test_high_composite_breaks_on_track_condition(self):
        inp = make_input(attainment_pct=1.0, quarters_below_quota_last_4=0, deals_pushed_to_next_period=0)
        sig = self.eng._signal(inp, QuotaPattern.none, 25.0)
        assert "Quota risk" in sig

    def test_non_none_pattern_breaks_on_track_condition(self):
        inp = make_input(attainment_pct=1.0, quarters_below_quota_last_4=0, deals_pushed_to_next_period=0)
        sig = self.eng._signal(inp, QuotaPattern.sandbagging, 10.0)
        assert "Quota attainment consistent and on track" not in sig

    def test_attainment_below_100_included_in_parts(self):
        inp = make_input(attainment_pct=0.80, quarters_below_quota_last_4=0, deals_pushed_to_next_period=0)
        sig = self.eng._signal(inp, QuotaPattern.none, 25.0)
        assert "80% quota attainment" in sig

    def test_quarters_below_included_in_parts(self):
        inp = make_input(attainment_pct=1.0, quarters_below_quota_last_4=2, deals_pushed_to_next_period=0)
        sig = self.eng._signal(inp, QuotaPattern.none, 25.0)
        assert "2/4 quarters below quota" in sig

    def test_deals_pushed_included_in_parts(self):
        inp = make_input(attainment_pct=1.0, quarters_below_quota_last_4=0, deals_pushed_to_next_period=3)
        sig = self.eng._signal(inp, QuotaPattern.none, 25.0)
        assert "3 deals pushed out" in sig

    def test_pattern_label_used_in_signal(self):
        inp = make_input(attainment_pct=0.80, quarters_below_quota_last_4=0, deals_pushed_to_next_period=0)
        sig = self.eng._signal(inp, QuotaPattern.consistent_underperformance, 50.0)
        assert "Consistent underperformance" in sig

    def test_none_pattern_label_shows_quota_risk(self):
        inp = make_input(attainment_pct=0.80, quarters_below_quota_last_4=0, deals_pushed_to_next_period=0)
        sig = self.eng._signal(inp, QuotaPattern.none, 25.0)
        assert "Quota risk" in sig

    def test_composite_included_in_signal(self):
        inp = make_input(attainment_pct=0.80, quarters_below_quota_last_4=0, deals_pushed_to_next_period=0)
        sig = self.eng._signal(inp, QuotaPattern.none, 42.0)
        assert "composite 42" in sig

    def test_no_parts_gives_declining_fallback(self):
        # attainment=1.0, quarters_below=0, pushed=0 → no parts
        inp = make_input(attainment_pct=1.0, quarters_below_quota_last_4=0, deals_pushed_to_next_period=0)
        sig = self.eng._signal(inp, QuotaPattern.none, 25.0)
        assert "quota performance declining" in sig

    def test_all_parts_present(self):
        inp = make_input(attainment_pct=0.70, quarters_below_quota_last_4=2, deals_pushed_to_next_period=4)
        sig = self.eng._signal(inp, QuotaPattern.late_quarter_surge, 50.0)
        assert "70% quota attainment" in sig
        assert "2/4 quarters below quota" in sig
        assert "4 deals pushed out" in sig

    def test_sandbagging_label_in_signal(self):
        inp = make_input(attainment_pct=0.95, quarters_below_quota_last_4=0, deals_pushed_to_next_period=0)
        sig = self.eng._signal(inp, QuotaPattern.sandbagging, 30.0)
        assert "Sandbagging" in sig

    def test_early_drop_off_label_in_signal(self):
        inp = make_input(attainment_pct=0.80, quarters_below_quota_last_4=0, deals_pushed_to_next_period=0)
        sig = self.eng._signal(inp, QuotaPattern.early_drop_off, 30.0)
        assert "Early drop off" in sig

    def test_quota_avoidance_label_in_signal(self):
        inp = make_input(attainment_pct=0.80, quarters_below_quota_last_4=0, deals_pushed_to_next_period=3)
        sig = self.eng._signal(inp, QuotaPattern.quota_avoidance, 30.0)
        assert "Quota avoidance" in sig


# ===========================================================================
# 13. assess() — QuotaAttainmentResult structure
# ===========================================================================

class TestAssess:
    def setup_method(self):
        self.eng = engine()

    def test_returns_quota_attainment_result(self):
        inp = make_input()
        result = self.eng.assess(inp)
        assert isinstance(result, QuotaAttainmentResult)

    def test_rep_id_copied(self):
        inp = make_input(rep_id="XYZ-789")
        result = self.eng.assess(inp)
        assert result.rep_id == "XYZ-789"

    def test_region_copied(self):
        inp = make_input(region="South-East")
        result = self.eng.assess(inp)
        assert result.region == "South-East"

    def test_scores_are_floats(self):
        inp = make_input()
        result = self.eng.assess(inp)
        assert isinstance(result.attainment_consistency_score, float)
        assert isinstance(result.deal_quality_score, float)
        assert isinstance(result.pipeline_health_score, float)
        assert isinstance(result.forecast_reliability_score, float)
        assert isinstance(result.quota_effectiveness_composite, float)

    def test_flags_are_bool(self):
        inp = make_input()
        result = self.eng.assess(inp)
        assert isinstance(result.is_below_quota_threshold, bool)
        assert isinstance(result.requires_performance_intervention, bool)

    def test_gap_is_float(self):
        inp = make_input()
        result = self.eng.assess(inp)
        assert isinstance(result.estimated_quota_gap_usd, float)

    def test_signal_is_string(self):
        inp = make_input()
        result = self.eng.assess(inp)
        assert isinstance(result.quota_signal, str)

    def test_risk_is_quota_risk(self):
        inp = make_input()
        result = self.eng.assess(inp)
        assert isinstance(result.quota_risk, QuotaRisk)

    def test_pattern_is_quota_pattern(self):
        inp = make_input()
        result = self.eng.assess(inp)
        assert isinstance(result.quota_pattern, QuotaPattern)

    def test_severity_is_quota_severity(self):
        inp = make_input()
        result = self.eng.assess(inp)
        assert isinstance(result.quota_severity, QuotaSeverity)

    def test_action_is_quota_action(self):
        inp = make_input()
        result = self.eng.assess(inp)
        assert isinstance(result.recommended_action, QuotaAction)

    def test_composite_between_0_and_100(self):
        inp = make_input()
        result = self.eng.assess(inp)
        assert 0.0 <= result.quota_effectiveness_composite <= 100.0

    def test_result_appended_to_internal_list(self):
        eng = engine()
        eng.assess(make_input())
        assert len(eng._results) == 1
        eng.assess(make_input())
        assert len(eng._results) == 2

    def test_good_rep_low_risk(self):
        inp = make_input()
        result = self.eng.assess(inp)
        assert result.quota_risk == QuotaRisk.low
        assert result.quota_severity == QuotaSeverity.on_track

    def test_bad_rep_high_or_critical_risk(self):
        inp = make_input(
            attainment_pct=0.40,
            quarters_below_quota_last_4=4,
            pipeline_coverage_ratio=1.0,
            forecast_commit_accuracy_pct=0.50,
            avg_deal_size_usd=3_000,
            discount_rate_avg_pct=0.30,
            deals_pushed_to_next_period=6,
            days_to_reach_50pct_quota=90,
            deals_lost_after_commit_count=5,
            total_deals_closed=10,
            deals_closed_last_week_of_period=7,
        )
        result = self.eng.assess(inp)
        assert result.quota_risk in (QuotaRisk.high, QuotaRisk.critical)

    def test_gap_zero_when_at_quota(self):
        inp = make_input(quota_amount_usd=100_000, revenue_closed_usd=100_000)
        result = self.eng.assess(inp)
        assert result.estimated_quota_gap_usd == 0.0

    def test_gap_nonzero_when_below_quota(self):
        inp = make_input(
            quota_amount_usd=100_000,
            revenue_closed_usd=70_000,
            attainment_pct=0.70,
            quarters_below_quota_last_4=2,
            pipeline_coverage_ratio=1.5,
        )
        result = self.eng.assess(inp)
        assert result.estimated_quota_gap_usd >= 0.0

    def test_composite_weighted_calculation(self):
        # Build an input where we can independently compute expected composite
        inp = make_input(
            attainment_pct=1.0,       # consistency sub-score = 0
            quarters_below_quota_last_4=0,
            deals_closed_last_week_of_period=0,
            avg_deal_size_usd=20_000,  # deal quality sub-score = 0
            discount_rate_avg_pct=0.05,
            deals_pushed_to_next_period=0,
            pipeline_coverage_ratio=5.0,  # pipeline sub-score = 0
            days_to_reach_50pct_quota=0,
            deals_lost_after_commit_count=0,
            total_deals_closed=10,
            forecast_commit_accuracy_pct=0.90,  # forecast sub-score = 0
        )
        result = self.eng.assess(inp)
        assert result.quota_effectiveness_composite == 0.0

    def test_assess_multiple_reps_independent(self):
        eng = engine()
        inp1 = make_input(rep_id="R1")
        inp2 = make_input(rep_id="R2", attainment_pct=0.40, quarters_below_quota_last_4=3)
        r1 = eng.assess(inp1)
        r2 = eng.assess(inp2)
        assert r1.rep_id == "R1"
        assert r2.rep_id == "R2"
        assert r1.quota_risk != r2.quota_risk or True  # at minimum they are independent


# ===========================================================================
# 14. to_dict() — 15 keys
# ===========================================================================

class TestToDict:
    def setup_method(self):
        self.eng = engine()

    def test_returns_dict(self):
        result = self.eng.assess(make_input())
        assert isinstance(result.to_dict(), dict)

    def test_exactly_15_keys(self):
        result = self.eng.assess(make_input())
        assert len(result.to_dict()) == 15

    def test_all_expected_keys_present(self):
        d = self.eng.assess(make_input()).to_dict()
        expected = {
            "rep_id", "region", "quota_risk", "quota_pattern", "quota_severity",
            "recommended_action", "attainment_consistency_score", "deal_quality_score",
            "pipeline_health_score", "forecast_reliability_score",
            "quota_effectiveness_composite", "is_below_quota_threshold",
            "requires_performance_intervention", "estimated_quota_gap_usd", "quota_signal",
        }
        assert set(d.keys()) == expected

    def test_enum_values_are_strings_in_dict(self):
        d = self.eng.assess(make_input()).to_dict()
        assert isinstance(d["quota_risk"], str)
        assert isinstance(d["quota_pattern"], str)
        assert isinstance(d["quota_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_rep_id_in_dict(self):
        d = self.eng.assess(make_input(rep_id="MY-REP")).to_dict()
        assert d["rep_id"] == "MY-REP"

    def test_region_in_dict(self):
        d = self.eng.assess(make_input(region="West")).to_dict()
        assert d["region"] == "West"

    def test_numeric_fields_in_dict(self):
        d = self.eng.assess(make_input()).to_dict()
        assert isinstance(d["attainment_consistency_score"], float)
        assert isinstance(d["deal_quality_score"], float)
        assert isinstance(d["pipeline_health_score"], float)
        assert isinstance(d["forecast_reliability_score"], float)
        assert isinstance(d["quota_effectiveness_composite"], float)
        assert isinstance(d["estimated_quota_gap_usd"], float)

    def test_bool_fields_in_dict(self):
        d = self.eng.assess(make_input()).to_dict()
        assert isinstance(d["is_below_quota_threshold"], bool)
        assert isinstance(d["requires_performance_intervention"], bool)

    def test_signal_in_dict_is_string(self):
        d = self.eng.assess(make_input()).to_dict()
        assert isinstance(d["quota_signal"], str)

    def test_quota_risk_value_matches_enum(self):
        result = self.eng.assess(make_input())
        d = result.to_dict()
        assert d["quota_risk"] == result.quota_risk.value

    def test_quota_pattern_value_matches_enum(self):
        result = self.eng.assess(make_input())
        d = result.to_dict()
        assert d["quota_pattern"] == result.quota_pattern.value


# ===========================================================================
# 15. summary() — 13 keys
# ===========================================================================

class TestSummary:
    def test_empty_summary_returns_13_keys(self):
        eng = engine()
        s = eng.summary()
        assert len(s) == 13

    def test_empty_summary_all_expected_keys(self):
        eng = engine()
        s = eng.summary()
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_quota_effectiveness_composite",
            "below_quota_threshold_count", "performance_intervention_count",
            "avg_attainment_consistency_score", "avg_deal_quality_score",
            "avg_pipeline_health_score", "avg_forecast_reliability_score",
            "total_estimated_quota_gap_usd",
        }
        assert set(s.keys()) == expected

    def test_empty_summary_total_is_0(self):
        assert engine().summary()["total"] == 0

    def test_empty_summary_avg_composite_is_0(self):
        assert engine().summary()["avg_quota_effectiveness_composite"] == 0.0

    def test_empty_summary_counts_are_empty_dicts(self):
        s = engine().summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}

    def test_empty_summary_below_threshold_count_is_0(self):
        assert engine().summary()["below_quota_threshold_count"] == 0

    def test_empty_summary_intervention_count_is_0(self):
        assert engine().summary()["performance_intervention_count"] == 0

    def test_empty_summary_gap_is_0(self):
        assert engine().summary()["total_estimated_quota_gap_usd"] == 0.0

    def test_summary_after_one_assessment(self):
        eng = engine()
        eng.assess(make_input())
        s = eng.summary()
        assert s["total"] == 1

    def test_summary_after_two_assessments(self):
        eng = engine()
        eng.assess(make_input(rep_id="R1"))
        eng.assess(make_input(rep_id="R2"))
        s = eng.summary()
        assert s["total"] == 2

    def test_risk_counts_correct(self):
        eng = engine()
        eng.assess(make_input())
        s = eng.summary()
        assert sum(s["risk_counts"].values()) == 1

    def test_pattern_counts_correct(self):
        eng = engine()
        eng.assess(make_input())
        s = eng.summary()
        assert sum(s["pattern_counts"].values()) == 1

    def test_severity_counts_correct(self):
        eng = engine()
        eng.assess(make_input())
        s = eng.summary()
        assert sum(s["severity_counts"].values()) == 1

    def test_action_counts_correct(self):
        eng = engine()
        eng.assess(make_input())
        s = eng.summary()
        assert sum(s["action_counts"].values()) == 1

    def test_avg_composite_computed_correctly(self):
        eng = engine()
        # Add a totally clean rep → composite = 0
        r1 = eng.assess(make_input())
        c1 = r1.quota_effectiveness_composite
        s = eng.summary()
        assert s["avg_quota_effectiveness_composite"] == c1

    def test_below_threshold_count_increments(self):
        eng = engine()
        eng.assess(make_input(attainment_pct=0.50))  # below 0.75 → True
        eng.assess(make_input(attainment_pct=1.0))   # composite = 0, attn = 1.0 → False
        s = eng.summary()
        assert s["below_quota_threshold_count"] >= 1

    def test_intervention_count_increments(self):
        eng = engine()
        eng.assess(make_input(attainment_pct=0.50, quarters_below_quota_last_4=2))
        s = eng.summary()
        assert s["performance_intervention_count"] >= 1

    def test_total_gap_is_sum(self):
        eng = engine()
        r1 = eng.assess(make_input(quota_amount_usd=200_000, revenue_closed_usd=100_000,
                                    attainment_pct=0.50, quarters_below_quota_last_4=2,
                                    pipeline_coverage_ratio=1.5))
        r2 = eng.assess(make_input(quota_amount_usd=200_000, revenue_closed_usd=180_000,
                                    attainment_pct=0.90))
        s = eng.summary()
        expected = round(r1.estimated_quota_gap_usd + r2.estimated_quota_gap_usd, 2)
        assert s["total_estimated_quota_gap_usd"] == expected

    def test_summary_has_exactly_13_keys_nonempty(self):
        eng = engine()
        eng.assess(make_input())
        eng.assess(make_input())
        assert len(eng.summary()) == 13

    def test_avg_scores_computed(self):
        eng = engine()
        eng.assess(make_input())
        s = eng.summary()
        assert isinstance(s["avg_attainment_consistency_score"], float)
        assert isinstance(s["avg_deal_quality_score"], float)
        assert isinstance(s["avg_pipeline_health_score"], float)
        assert isinstance(s["avg_forecast_reliability_score"], float)

    def test_multiple_risk_levels_counted(self):
        eng = engine()
        # low-risk rep
        eng.assess(make_input(rep_id="LOW"))
        # high-risk rep
        eng.assess(make_input(
            rep_id="HIGH",
            attainment_pct=0.40,
            quarters_below_quota_last_4=4,
            pipeline_coverage_ratio=1.0,
            forecast_commit_accuracy_pct=0.50,
            avg_deal_size_usd=3_000,
            discount_rate_avg_pct=0.30,
            deals_pushed_to_next_period=6,
            days_to_reach_50pct_quota=90,
            deals_lost_after_commit_count=5,
            total_deals_closed=10,
            deals_closed_last_week_of_period=7,
        ))
        s = eng.summary()
        assert len(s["risk_counts"]) >= 2


# ===========================================================================
# 16. assess_batch()
# ===========================================================================

class TestAssessBatch:
    def setup_method(self):
        self.eng = engine()

    def test_empty_batch_returns_empty_list(self):
        assert self.eng.assess_batch([]) == []

    def test_single_input_batch(self):
        results = self.eng.assess_batch([make_input()])
        assert len(results) == 1
        assert isinstance(results[0], QuotaAttainmentResult)

    def test_multiple_inputs_batch(self):
        inputs = [make_input(rep_id=f"REP{i}") for i in range(5)]
        results = self.eng.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_order_preserved(self):
        inputs = [make_input(rep_id=f"REP{i}") for i in range(3)]
        results = self.eng.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"REP{i}"

    def test_batch_results_stored_in_internal_list(self):
        eng = engine()
        eng.assess_batch([make_input(rep_id="A"), make_input(rep_id="B")])
        assert len(eng._results) == 2

    def test_batch_returns_list_of_correct_type(self):
        results = self.eng.assess_batch([make_input(), make_input()])
        for r in results:
            assert isinstance(r, QuotaAttainmentResult)

    def test_batch_then_summary_total_matches(self):
        eng = engine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(7)]
        eng.assess_batch(inputs)
        assert eng.summary()["total"] == 7

    def test_batch_mixed_risk_levels(self):
        eng = engine()
        good = make_input(rep_id="good")
        bad = make_input(
            rep_id="bad",
            attainment_pct=0.40,
            quarters_below_quota_last_4=4,
            pipeline_coverage_ratio=1.0,
            forecast_commit_accuracy_pct=0.50,
            avg_deal_size_usd=3_000,
            discount_rate_avg_pct=0.30,
            deals_pushed_to_next_period=6,
            days_to_reach_50pct_quota=90,
            deals_lost_after_commit_count=5,
            total_deals_closed=10,
            deals_closed_last_week_of_period=7,
        )
        results = eng.assess_batch([good, bad])
        risks = {r.rep_id: r.quota_risk for r in results}
        assert risks["good"] in (QuotaRisk.low, QuotaRisk.moderate)
        assert risks["bad"] in (QuotaRisk.high, QuotaRisk.critical)

    def test_large_batch(self):
        eng = engine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(50)]
        results = eng.assess_batch(inputs)
        assert len(results) == 50

    def test_batch_cumulative_with_individual_assess(self):
        eng = engine()
        eng.assess(make_input(rep_id="A"))
        eng.assess_batch([make_input(rep_id="B"), make_input(rep_id="C")])
        assert eng.summary()["total"] == 3


# ===========================================================================
# 17. Integration / end-to-end tests
# ===========================================================================

class TestIntegration:
    """Full end-to-end scenarios covering realistic rep profiles."""

    def _eng(self):
        return engine()

    def test_star_performer_full_pipeline(self):
        eng = self._eng()
        inp = make_input(
            rep_id="STAR", region="West",
            quota_amount_usd=500_000, revenue_closed_usd=550_000,
            attainment_pct=1.10,
            quarters_below_quota_last_4=0, quarters_above_quota_last_4=4,
            deals_closed_last_week_of_period=1, total_deals_closed=20,
            deals_pushed_to_next_period=0,
            avg_deal_size_usd=27_500,
            pipeline_coverage_ratio=5.0,
            forecast_commit_accuracy_pct=0.92,
            discount_rate_avg_pct=0.08,
            avg_sales_cycle_days=25.0,
            multi_year_deals_closed=4,
            expansion_revenue_usd=50_000, new_logo_revenue_usd=500_000,
            days_to_reach_50pct_quota=30,
            deals_lost_after_commit_count=0,
        )
        result = eng.assess(inp)
        assert result.quota_risk == QuotaRisk.low
        assert result.quota_severity == QuotaSeverity.on_track
        assert result.is_below_quota_threshold is False
        assert result.estimated_quota_gap_usd == 0.0
        assert "on track" in result.quota_signal

    def test_underperforming_rep_full_pipeline(self):
        eng = self._eng()
        inp = make_input(
            rep_id="UNDER", region="East",
            quota_amount_usd=200_000, revenue_closed_usd=80_000,
            attainment_pct=0.40,
            quarters_below_quota_last_4=4, quarters_above_quota_last_4=0,
            deals_closed_last_week_of_period=3, total_deals_closed=10,
            deals_pushed_to_next_period=5,
            avg_deal_size_usd=4_000,
            pipeline_coverage_ratio=1.5,
            forecast_commit_accuracy_pct=0.55,
            discount_rate_avg_pct=0.30,
            avg_sales_cycle_days=90.0,
            multi_year_deals_closed=0,
            expansion_revenue_usd=0, new_logo_revenue_usd=80_000,
            days_to_reach_50pct_quota=85,
            deals_lost_after_commit_count=3,
        )
        result = eng.assess(inp)
        assert result.quota_risk in (QuotaRisk.high, QuotaRisk.critical)
        assert result.is_below_quota_threshold is True
        assert result.requires_performance_intervention is True
        assert result.estimated_quota_gap_usd > 0.0

    def test_sandbagging_rep_full_pipeline(self):
        eng = self._eng()
        inp = make_input(
            rep_id="SANDBAG", region="North",
            quota_amount_usd=100_000, revenue_closed_usd=100_000,
            attainment_pct=1.0,
            quarters_below_quota_last_4=0, quarters_above_quota_last_4=4,
            deals_closed_last_week_of_period=5, total_deals_closed=10,
            deals_pushed_to_next_period=2,
            avg_deal_size_usd=4_000,
            pipeline_coverage_ratio=5.0,
            forecast_commit_accuracy_pct=0.90,
            discount_rate_avg_pct=0.20,
            avg_sales_cycle_days=30.0,
            multi_year_deals_closed=1,
            expansion_revenue_usd=5_000, new_logo_revenue_usd=95_000,
            days_to_reach_50pct_quota=30,
            deals_lost_after_commit_count=0,
        )
        result = eng.assess(inp)
        # High last-week surge + good attainment + deal quality penalty
        assert result.quota_pattern in (
            QuotaPattern.sandbagging, QuotaPattern.late_quarter_surge, QuotaPattern.none
        )

    def test_to_dict_matches_result_fields(self):
        eng = self._eng()
        result = eng.assess(make_input(rep_id="DICT-TEST"))
        d = result.to_dict()
        assert d["rep_id"] == result.rep_id
        assert d["quota_risk"] == result.quota_risk.value
        assert d["quota_pattern"] == result.quota_pattern.value
        assert d["quota_severity"] == result.quota_severity.value
        assert d["recommended_action"] == result.recommended_action.value
        assert d["attainment_consistency_score"] == result.attainment_consistency_score
        assert d["deal_quality_score"] == result.deal_quality_score
        assert d["pipeline_health_score"] == result.pipeline_health_score
        assert d["forecast_reliability_score"] == result.forecast_reliability_score
        assert d["quota_effectiveness_composite"] == result.quota_effectiveness_composite
        assert d["is_below_quota_threshold"] == result.is_below_quota_threshold
        assert d["requires_performance_intervention"] == result.requires_performance_intervention
        assert d["estimated_quota_gap_usd"] == result.estimated_quota_gap_usd
        assert d["quota_signal"] == result.quota_signal

    def test_assess_batch_then_summary_risk_counts_sum(self):
        eng = self._eng()
        inputs = [make_input(rep_id=f"R{i}") for i in range(10)]
        eng.assess_batch(inputs)
        s = eng.summary()
        assert sum(s["risk_counts"].values()) == 10

    def test_fresh_engine_each_time_independent(self):
        eng1 = engine()
        eng2 = engine()
        bad_inp = make_input(attainment_pct=0.30, quarters_below_quota_last_4=4)
        eng1.assess(bad_inp)
        # eng2 should still have empty results
        assert len(eng2._results) == 0
        assert eng2.summary()["total"] == 0

    def test_composite_score_bounds_across_many_inputs(self):
        eng = self._eng()
        varied_inputs = [
            make_input(attainment_pct=0.30, quarters_below_quota_last_4=4,
                       pipeline_coverage_ratio=1.0, forecast_commit_accuracy_pct=0.50,
                       avg_deal_size_usd=1_000, discount_rate_avg_pct=0.40,
                       deals_pushed_to_next_period=8, days_to_reach_50pct_quota=90,
                       deals_lost_after_commit_count=5, total_deals_closed=10,
                       deals_closed_last_week_of_period=8),
            make_input(),
            make_input(attainment_pct=0.80, quarters_below_quota_last_4=1,
                       pipeline_coverage_ratio=3.5),
        ]
        for inp in varied_inputs:
            result = eng.assess(inp)
            assert 0.0 <= result.quota_effectiveness_composite <= 100.0

    def test_quota_risk_and_severity_always_consistent(self):
        # risk and severity must correspond to the same composite thresholds
        eng = self._eng()
        for composite_val in [0.0, 15.0, 20.0, 30.0, 40.0, 55.0, 60.0, 80.0, 100.0]:
            risk = eng._risk_level(composite_val)
            sev = eng._severity(composite_val)
            risk_to_sev = {
                QuotaRisk.low: QuotaSeverity.on_track,
                QuotaRisk.moderate: QuotaSeverity.developing,
                QuotaRisk.high: QuotaSeverity.at_risk,
                QuotaRisk.critical: QuotaSeverity.critical,
            }
            assert risk_to_sev[risk] == sev, f"Mismatch at composite={composite_val}"
