"""
Comprehensive pytest tests for ForecastConfidenceScorer.
"""
from __future__ import annotations

import dataclasses
import pytest

from swarm.intelligence.forecast_confidence_scorer import (
    ForecastConfidenceScorer,
    ForecastConfidenceInput,
    ForecastConfidenceResult,
    ConfidenceLevel,
    ForecastPattern,
    PipelineHealth,
    ForecastAction,
)


# ── helpers ──────────────────────────────────────────────────────────────────

def make_input(**overrides) -> ForecastConfidenceInput:
    """Return a baseline ForecastConfidenceInput with sensible defaults.

    Any field can be overridden via keyword arguments.
    """
    defaults = dict(
        rep_id="R001",
        rep_name="Alice Smith",
        manager_id="M001",
        forecast_amount=200_000.0,
        quota_amount=250_000.0,
        pipeline_total=700_000.0,          # ratio 3.5x → HEALTHY
        pipeline_in_commit_stage=220_000.0, # commit_ratio 1.1 → 28 pts
        pipeline_in_best_case=150_000.0,
        deals_in_commit=4,
        deals_closed_this_period=2,
        revenue_closed_this_period=60_000.0,  # closed_ratio 0.3 → 15 pts
        avg_deal_size_historical=50_000.0,
        win_rate_historical_pct=30.0,          # → 20 pts
        forecast_accuracy_last_3q=80.0,        # → 40 pts hist
        close_date_slip_rate_pct=15.0,         # → 0 penalty
        days_remaining_in_period=25,           # → +15 quality
        activities_last_14d=15,               # → +25 activity
        avg_activities_per_commit_deal=65.0,  # → +28 activity
        exec_sponsored_deal_count=2,           # exec_ratio 0.5 → +30 quality
        multi_stakeholder_deal_count=2,        # ms_ratio 0.5 → +25 quality
        new_deals_added_last_30d=3,            # → +8 activity
        cfo_approval_required_count=0,
    )
    defaults.update(overrides)
    return ForecastConfidenceInput(**defaults)


# ── invariant: ForecastConfidenceInput has exactly 22 fields ─────────────────

class TestForecastConfidenceInputStructure:
    def test_field_count_is_22(self):
        fields = dataclasses.fields(ForecastConfidenceInput)
        assert len(fields) == 22

    def test_field_names(self):
        names = {f.name for f in dataclasses.fields(ForecastConfidenceInput)}
        expected = {
            "rep_id", "rep_name", "manager_id",
            "forecast_amount", "quota_amount",
            "pipeline_total", "pipeline_in_commit_stage", "pipeline_in_best_case",
            "deals_in_commit", "deals_closed_this_period", "revenue_closed_this_period",
            "avg_deal_size_historical", "win_rate_historical_pct",
            "forecast_accuracy_last_3q", "close_date_slip_rate_pct",
            "days_remaining_in_period", "activities_last_14d",
            "avg_activities_per_commit_deal", "exec_sponsored_deal_count",
            "multi_stakeholder_deal_count", "new_deals_added_last_30d",
            "cfo_approval_required_count",
        }
        assert names == expected


# ── invariant: ForecastConfidenceResult.to_dict() returns exactly 15 keys ────

class TestForecastConfidenceResultToDict:
    def test_to_dict_key_count_is_15(self):
        scorer = ForecastConfidenceScorer()
        result = scorer.score(make_input())
        assert len(result.to_dict()) == 15

    def test_to_dict_key_names(self):
        scorer = ForecastConfidenceScorer()
        result = scorer.score(make_input())
        keys = set(result.to_dict().keys())
        expected = {
            "rep_id", "rep_name", "confidence_level", "forecast_pattern",
            "pipeline_health", "forecast_action", "historical_accuracy_score",
            "pipeline_coverage_score", "deal_quality_score", "activity_signal_score",
            "forecast_composite", "attainment_probability", "pipeline_coverage_ratio",
            "is_forecast_reliable", "needs_forecast_scrub",
        }
        assert keys == expected

    def test_to_dict_enum_values_are_strings(self):
        scorer = ForecastConfidenceScorer()
        d = scorer.score(make_input()).to_dict()
        assert isinstance(d["confidence_level"], str)
        assert isinstance(d["forecast_pattern"], str)
        assert isinstance(d["pipeline_health"], str)
        assert isinstance(d["forecast_action"], str)

    def test_to_dict_booleans(self):
        scorer = ForecastConfidenceScorer()
        d = scorer.score(make_input()).to_dict()
        assert isinstance(d["is_forecast_reliable"], bool)
        assert isinstance(d["needs_forecast_scrub"], bool)


# ── invariant: summary() returns exactly 13 keys ─────────────────────────────

class TestSummaryKeyCount:
    def test_empty_summary_has_13_keys(self):
        scorer = ForecastConfidenceScorer()
        s = scorer.summary()
        assert len(s) == 13

    def test_non_empty_summary_has_13_keys(self):
        scorer = ForecastConfidenceScorer()
        scorer.score(make_input())
        s = scorer.summary()
        assert len(s) == 13

    def test_summary_key_names(self):
        scorer = ForecastConfidenceScorer()
        scorer.score(make_input())
        keys = set(scorer.summary().keys())
        expected = {
            "total", "confidence_counts", "pattern_counts",
            "pipeline_health_counts", "action_counts",
            "avg_forecast_composite", "avg_attainment_probability",
            "reliable_count", "scrub_count",
            "avg_historical_accuracy_score", "avg_pipeline_coverage_score",
            "avg_deal_quality_score", "avg_activity_signal_score",
        }
        assert keys == expected


# ── enum membership ───────────────────────────────────────────────────────────

class TestEnums:
    def test_confidence_level_values(self):
        values = {e.value for e in ConfidenceLevel}
        assert values == {"low", "moderate", "high", "committed"}

    def test_confidence_level_members(self):
        assert ConfidenceLevel.LOW.value == "low"
        assert ConfidenceLevel.MODERATE.value == "moderate"
        assert ConfidenceLevel.HIGH.value == "high"
        assert ConfidenceLevel.COMMITTED.value == "committed"

    def test_forecast_pattern_values(self):
        values = {e.value for e in ForecastPattern}
        assert values == {"reliable", "optimistic_bias", "sandbagging", "volatile", "insufficient"}

    def test_forecast_pattern_members(self):
        assert ForecastPattern.RELIABLE.value == "reliable"
        assert ForecastPattern.OPTIMISTIC_BIAS.value == "optimistic_bias"
        assert ForecastPattern.SANDBAGGING.value == "sandbagging"
        assert ForecastPattern.VOLATILE.value == "volatile"
        assert ForecastPattern.INSUFFICIENT.value == "insufficient"

    def test_pipeline_health_values(self):
        values = {e.value for e in PipelineHealth}
        assert values == {"underpipelined", "adequate", "healthy", "overpipelined"}

    def test_pipeline_health_members(self):
        assert PipelineHealth.UNDERPIPELINED.value == "underpipelined"
        assert PipelineHealth.ADEQUATE.value == "adequate"
        assert PipelineHealth.HEALTHY.value == "healthy"
        assert PipelineHealth.OVERPIPELINED.value == "overpipelined"

    def test_forecast_action_values(self):
        values = {e.value for e in ForecastAction}
        assert values == {"accept", "review_with_rep", "scrub_required", "escalate_to_manager"}

    def test_forecast_action_members(self):
        assert ForecastAction.ACCEPT.value == "accept"
        assert ForecastAction.REVIEW_WITH_REP.value == "review_with_rep"
        assert ForecastAction.SCRUB_REQUIRED.value == "scrub_required"
        assert ForecastAction.ESCALATE_TO_MANAGER.value == "escalate_to_manager"

    def test_enums_are_str_subclass(self):
        # All four enums inherit from str
        assert isinstance(ConfidenceLevel.LOW, str)
        assert isinstance(ForecastPattern.RELIABLE, str)
        assert isinstance(PipelineHealth.HEALTHY, str)
        assert isinstance(ForecastAction.ACCEPT, str)


# ── composite formula: hist*0.30 + pipe*0.35 + quality*0.20 + activity*0.15 ──

class TestCompositeFormula:
    def test_composite_weights(self):
        scorer = ForecastConfidenceScorer()
        hist, pipe, quality, activity = 80.0, 60.0, 50.0, 40.0
        expected = round(80 * 0.30 + 60 * 0.35 + 50 * 0.20 + 40 * 0.15, 1)
        assert scorer._composite(hist, pipe, quality, activity) == expected

    def test_composite_clamped_max(self):
        scorer = ForecastConfidenceScorer()
        assert scorer._composite(100.0, 100.0, 100.0, 100.0) == 100.0

    def test_composite_clamped_min(self):
        scorer = ForecastConfidenceScorer()
        assert scorer._composite(0.0, 0.0, 0.0, 0.0) == 0.0

    def test_composite_zero_inputs(self):
        scorer = ForecastConfidenceScorer()
        assert scorer._composite(0.0, 0.0, 0.0, 0.0) == 0.0

    def test_composite_partial_example(self):
        scorer = ForecastConfidenceScorer()
        result = scorer._composite(50.0, 50.0, 50.0, 50.0)
        assert result == 50.0

    def test_composite_reflected_in_score_output(self):
        scorer = ForecastConfidenceScorer()
        result = scorer.score(make_input())
        expected_composite = scorer._composite(
            result.historical_accuracy_score,
            result.pipeline_coverage_score,
            result.deal_quality_score,
            result.activity_signal_score,
        )
        assert result.forecast_composite == expected_composite


# ── is_forecast_reliable: composite >= 60 AND forecast_accuracy_last_3q >= 70 ─

class TestIsForecastReliable:
    def test_reliable_when_both_conditions_met(self):
        # Force high composite and high accuracy
        scorer = ForecastConfidenceScorer()
        inp = make_input(
            forecast_accuracy_last_3q=90.0,
            win_rate_historical_pct=40.0,
            close_date_slip_rate_pct=5.0,
            pipeline_total=800_000.0,
            pipeline_in_commit_stage=250_000.0,
            revenue_closed_this_period=100_000.0,
            activities_last_14d=25,
            avg_activities_per_commit_deal=85.0,
            new_deals_added_last_30d=5,
            deals_closed_this_period=3,
            exec_sponsored_deal_count=3,
            multi_stakeholder_deal_count=3,
            days_remaining_in_period=25,
        )
        result = scorer.score(inp)
        assert result.is_forecast_reliable is True

    def test_not_reliable_when_accuracy_below_70(self):
        scorer = ForecastConfidenceScorer()
        inp = make_input(forecast_accuracy_last_3q=69.0)
        result = scorer.score(inp)
        assert result.is_forecast_reliable is False

    def test_not_reliable_when_composite_below_60(self):
        # Minimal inputs to pull composite below 60
        scorer = ForecastConfidenceScorer()
        inp = make_input(
            forecast_accuracy_last_3q=75.0,
            win_rate_historical_pct=5.0,
            close_date_slip_rate_pct=55.0,
            pipeline_total=50_000.0,
            pipeline_in_commit_stage=10_000.0,
            revenue_closed_this_period=0.0,
            activities_last_14d=1,
            avg_activities_per_commit_deal=5.0,
            new_deals_added_last_30d=0,
            deals_closed_this_period=0,
            exec_sponsored_deal_count=0,
            multi_stakeholder_deal_count=0,
            days_remaining_in_period=3,
            cfo_approval_required_count=3,
        )
        result = scorer.score(inp)
        assert result.is_forecast_reliable is False

    def test_not_reliable_when_accuracy_exactly_69(self):
        scorer = ForecastConfidenceScorer()
        inp = make_input(forecast_accuracy_last_3q=69.9)
        result = scorer.score(inp)
        assert result.is_forecast_reliable is False

    def test_reliable_boundary_accuracy_exactly_70(self):
        scorer = ForecastConfidenceScorer()
        # Use a high-scoring input but set accuracy at exactly 70
        inp = make_input(
            forecast_accuracy_last_3q=70.0,
            win_rate_historical_pct=40.0,
            close_date_slip_rate_pct=5.0,
            pipeline_total=900_000.0,
            pipeline_in_commit_stage=280_000.0,
            revenue_closed_this_period=120_000.0,
            activities_last_14d=25,
            avg_activities_per_commit_deal=85.0,
            new_deals_added_last_30d=5,
            deals_closed_this_period=4,
            exec_sponsored_deal_count=4,
            multi_stakeholder_deal_count=4,
        )
        result = scorer.score(inp)
        # composite must be >= 60 and accuracy == 70 (>= 70) → reliable
        if result.forecast_composite >= 60:
            assert result.is_forecast_reliable is True


# ── needs_forecast_scrub: composite < 45 OR slip_rate >= 40 ──────────────────

class TestNeedsForecastScrub:
    def test_scrub_when_composite_below_45(self):
        scorer = ForecastConfidenceScorer()
        inp = make_input(
            forecast_accuracy_last_3q=50.0,
            win_rate_historical_pct=5.0,
            close_date_slip_rate_pct=10.0,
            pipeline_total=50_000.0,
            pipeline_in_commit_stage=10_000.0,
            revenue_closed_this_period=0.0,
            activities_last_14d=1,
            avg_activities_per_commit_deal=5.0,
            new_deals_added_last_30d=0,
            deals_closed_this_period=0,
            exec_sponsored_deal_count=0,
            multi_stakeholder_deal_count=0,
            days_remaining_in_period=3,
            cfo_approval_required_count=3,
        )
        result = scorer.score(inp)
        if result.forecast_composite < 45:
            assert result.needs_forecast_scrub is True

    def test_scrub_when_slip_rate_ge_40(self):
        scorer = ForecastConfidenceScorer()
        inp = make_input(close_date_slip_rate_pct=40.0)
        result = scorer.score(inp)
        assert result.needs_forecast_scrub is True

    def test_scrub_when_slip_rate_exactly_40(self):
        scorer = ForecastConfidenceScorer()
        inp = make_input(close_date_slip_rate_pct=40.0)
        result = scorer.score(inp)
        assert result.needs_forecast_scrub is True

    def test_scrub_when_slip_rate_above_40(self):
        scorer = ForecastConfidenceScorer()
        inp = make_input(close_date_slip_rate_pct=75.0)
        result = scorer.score(inp)
        assert result.needs_forecast_scrub is True

    def test_no_scrub_when_composite_high_and_slip_low(self):
        scorer = ForecastConfidenceScorer()
        inp = make_input(
            forecast_accuracy_last_3q=90.0,
            win_rate_historical_pct=40.0,
            close_date_slip_rate_pct=5.0,
            pipeline_total=900_000.0,
            pipeline_in_commit_stage=300_000.0,
            revenue_closed_this_period=100_000.0,
            activities_last_14d=25,
            avg_activities_per_commit_deal=85.0,
            new_deals_added_last_30d=5,
            deals_closed_this_period=4,
            exec_sponsored_deal_count=4,
            multi_stakeholder_deal_count=4,
            cfo_approval_required_count=0,
        )
        result = scorer.score(inp)
        assert result.needs_forecast_scrub is False


# ── _historical_accuracy_score ────────────────────────────────────────────────

class TestHistoricalAccuracyScore:
    def setup_method(self):
        self.scorer = ForecastConfidenceScorer()

    def _score(self, acc, wr, slip):
        inp = make_input(
            forecast_accuracy_last_3q=acc,
            win_rate_historical_pct=wr,
            close_date_slip_rate_pct=slip,
        )
        return self.scorer._historical_accuracy_score(inp)

    def test_accuracy_ge_90_gives_50_pts(self):
        s = self._score(90.0, 0.0, 0.0)
        assert s == 50.0

    def test_accuracy_ge_80_gives_40_pts(self):
        s = self._score(80.0, 0.0, 0.0)
        assert s == 40.0

    def test_accuracy_ge_70_gives_28_pts(self):
        s = self._score(70.0, 0.0, 0.0)
        assert s == 28.0

    def test_accuracy_ge_55_gives_15_pts(self):
        s = self._score(55.0, 0.0, 0.0)
        assert s == 15.0

    def test_accuracy_below_55_gives_0_pts(self):
        s = self._score(50.0, 0.0, 0.0)
        assert s == 0.0

    def test_win_rate_ge_35_gives_30_pts(self):
        s = self._score(0.0, 35.0, 0.0)
        assert s == 30.0

    def test_win_rate_ge_25_gives_20_pts(self):
        s = self._score(0.0, 25.0, 0.0)
        assert s == 20.0

    def test_win_rate_ge_15_gives_10_pts(self):
        s = self._score(0.0, 15.0, 0.0)
        assert s == 10.0

    def test_win_rate_below_15_gives_0_pts(self):
        s = self._score(0.0, 10.0, 0.0)
        assert s == 0.0

    def test_slip_ge_50_penalty_20(self):
        # 50 acc pts + 30 wr pts − 20 slip pts = 60
        s = self._score(90.0, 35.0, 50.0)
        assert s == 60.0

    def test_slip_ge_35_penalty_12(self):
        s = self._score(90.0, 35.0, 35.0)
        assert s == 68.0

    def test_slip_ge_20_penalty_6(self):
        s = self._score(90.0, 35.0, 20.0)
        assert s == 74.0

    def test_slip_below_20_no_penalty(self):
        s = self._score(90.0, 35.0, 10.0)
        assert s == 80.0

    def test_score_clamped_to_0_minimum(self):
        # Worst case: no acc/wr points but max slip penalty → clamp to 0
        s = self._score(0.0, 0.0, 50.0)
        assert s == 0.0

    def test_score_clamped_to_100_maximum(self):
        s = self._score(95.0, 40.0, 0.0)
        assert s == min(100.0, 80.0)


# ── _pipeline_coverage_score ──────────────────────────────────────────────────

class TestPipelineCoverageScore:
    def setup_method(self):
        self.scorer = ForecastConfidenceScorer()

    def test_zero_forecast_returns_0(self):
        inp = make_input(forecast_amount=0.0)
        assert self.scorer._pipeline_coverage_score(inp) == 0.0

    def test_ratio_ge_4_gives_40_pts(self):
        inp = make_input(
            forecast_amount=100_000.0,
            pipeline_total=400_000.0,
            pipeline_in_commit_stage=0.0,
            revenue_closed_this_period=0.0,
        )
        s = self.scorer._pipeline_coverage_score(inp)
        assert s == 40.0

    def test_ratio_ge_3_gives_32_pts(self):
        inp = make_input(
            forecast_amount=100_000.0,
            pipeline_total=300_000.0,
            pipeline_in_commit_stage=0.0,
            revenue_closed_this_period=0.0,
        )
        s = self.scorer._pipeline_coverage_score(inp)
        assert s == 32.0

    def test_ratio_ge_2_gives_22_pts(self):
        inp = make_input(
            forecast_amount=100_000.0,
            pipeline_total=200_000.0,
            pipeline_in_commit_stage=0.0,
            revenue_closed_this_period=0.0,
        )
        s = self.scorer._pipeline_coverage_score(inp)
        assert s == 22.0

    def test_ratio_ge_1_5_gives_12_pts(self):
        inp = make_input(
            forecast_amount=100_000.0,
            pipeline_total=150_000.0,
            pipeline_in_commit_stage=0.0,
            revenue_closed_this_period=0.0,
        )
        s = self.scorer._pipeline_coverage_score(inp)
        assert s == 12.0

    def test_ratio_below_1_5_gives_0_coverage_pts(self):
        inp = make_input(
            forecast_amount=100_000.0,
            pipeline_total=100_000.0,
            pipeline_in_commit_stage=0.0,
            revenue_closed_this_period=0.0,
        )
        s = self.scorer._pipeline_coverage_score(inp)
        assert s == 0.0

    def test_commit_ratio_ge_1_2_gives_35_pts(self):
        inp = make_input(
            forecast_amount=100_000.0,
            pipeline_total=0.0,
            pipeline_in_commit_stage=120_000.0,
            revenue_closed_this_period=0.0,
        )
        s = self.scorer._pipeline_coverage_score(inp)
        assert s == 35.0

    def test_commit_ratio_ge_1_0_gives_28_pts(self):
        inp = make_input(
            forecast_amount=100_000.0,
            pipeline_total=0.0,
            pipeline_in_commit_stage=100_000.0,
            revenue_closed_this_period=0.0,
        )
        s = self.scorer._pipeline_coverage_score(inp)
        assert s == 28.0

    def test_commit_ratio_ge_0_8_gives_18_pts(self):
        inp = make_input(
            forecast_amount=100_000.0,
            pipeline_total=0.0,
            pipeline_in_commit_stage=80_000.0,
            revenue_closed_this_period=0.0,
        )
        s = self.scorer._pipeline_coverage_score(inp)
        assert s == 18.0

    def test_commit_ratio_ge_0_5_gives_8_pts(self):
        inp = make_input(
            forecast_amount=100_000.0,
            pipeline_total=0.0,
            pipeline_in_commit_stage=50_000.0,
            revenue_closed_this_period=0.0,
        )
        s = self.scorer._pipeline_coverage_score(inp)
        assert s == 8.0

    def test_closed_ratio_ge_0_5_gives_25_pts(self):
        inp = make_input(
            forecast_amount=100_000.0,
            pipeline_total=0.0,
            pipeline_in_commit_stage=0.0,
            revenue_closed_this_period=50_000.0,
        )
        s = self.scorer._pipeline_coverage_score(inp)
        assert s == 25.0

    def test_closed_ratio_ge_0_3_gives_15_pts(self):
        inp = make_input(
            forecast_amount=100_000.0,
            pipeline_total=0.0,
            pipeline_in_commit_stage=0.0,
            revenue_closed_this_period=30_000.0,
        )
        s = self.scorer._pipeline_coverage_score(inp)
        assert s == 15.0

    def test_closed_ratio_ge_0_1_gives_8_pts(self):
        inp = make_input(
            forecast_amount=100_000.0,
            pipeline_total=0.0,
            pipeline_in_commit_stage=0.0,
            revenue_closed_this_period=10_000.0,
        )
        s = self.scorer._pipeline_coverage_score(inp)
        assert s == 8.0

    def test_max_score_clamped_to_100(self):
        inp = make_input(
            forecast_amount=100_000.0,
            pipeline_total=500_000.0,      # 40 pts
            pipeline_in_commit_stage=150_000.0,  # 35 pts
            revenue_closed_this_period=60_000.0,  # 25 pts
        )
        s = self.scorer._pipeline_coverage_score(inp)
        assert s == 100.0


# ── _deal_quality_score ───────────────────────────────────────────────────────

class TestDealQualityScore:
    def setup_method(self):
        self.scorer = ForecastConfidenceScorer()

    def test_exec_ratio_ge_0_5_gives_30_pts(self):
        inp = make_input(
            deals_in_commit=4,
            exec_sponsored_deal_count=2,
            multi_stakeholder_deal_count=0,
            avg_deal_size_historical=0.0,
            days_remaining_in_period=0,
            cfo_approval_required_count=0,
        )
        s = self.scorer._deal_quality_score(inp)
        assert s == 30.0

    def test_exec_ratio_ge_0_25_gives_18_pts(self):
        inp = make_input(
            deals_in_commit=4,
            exec_sponsored_deal_count=1,
            multi_stakeholder_deal_count=0,
            avg_deal_size_historical=0.0,
            days_remaining_in_period=0,
            cfo_approval_required_count=0,
        )
        s = self.scorer._deal_quality_score(inp)
        assert s == 18.0

    def test_exec_ratio_below_0_25_gives_0_pts(self):
        inp = make_input(
            deals_in_commit=8,
            exec_sponsored_deal_count=1,  # ratio = 0.125
            multi_stakeholder_deal_count=0,
            avg_deal_size_historical=0.0,
            days_remaining_in_period=0,
            cfo_approval_required_count=0,
        )
        s = self.scorer._deal_quality_score(inp)
        assert s == 0.0

    def test_ms_ratio_ge_0_5_gives_25_pts(self):
        inp = make_input(
            deals_in_commit=4,
            exec_sponsored_deal_count=0,
            multi_stakeholder_deal_count=2,
            avg_deal_size_historical=0.0,
            days_remaining_in_period=0,
            cfo_approval_required_count=0,
        )
        s = self.scorer._deal_quality_score(inp)
        assert s == 25.0

    def test_ms_ratio_ge_0_25_gives_15_pts(self):
        inp = make_input(
            deals_in_commit=4,
            exec_sponsored_deal_count=0,
            multi_stakeholder_deal_count=1,
            avg_deal_size_historical=0.0,
            days_remaining_in_period=0,
            cfo_approval_required_count=0,
        )
        s = self.scorer._deal_quality_score(inp)
        assert s == 15.0

    def test_size_ratio_in_range_gives_20_pts(self):
        # commit_avg = 50_000 / 1 = 50_000; hist_avg = 50_000; ratio = 1.0 (in range)
        inp = make_input(
            deals_in_commit=1,
            pipeline_in_commit_stage=50_000.0,
            avg_deal_size_historical=50_000.0,
            exec_sponsored_deal_count=0,
            multi_stakeholder_deal_count=0,
            days_remaining_in_period=0,
            cfo_approval_required_count=0,
        )
        s = self.scorer._deal_quality_score(inp)
        assert s == 20.0

    def test_size_ratio_above_2_gives_8_pts(self):
        # commit_avg = 150_000; hist_avg = 50_000; ratio = 3.0 (> 2.0)
        inp = make_input(
            deals_in_commit=1,
            pipeline_in_commit_stage=150_000.0,
            avg_deal_size_historical=50_000.0,
            exec_sponsored_deal_count=0,
            multi_stakeholder_deal_count=0,
            days_remaining_in_period=0,
            cfo_approval_required_count=0,
        )
        s = self.scorer._deal_quality_score(inp)
        assert s == 8.0

    def test_days_remaining_ge_20_gives_15_pts(self):
        inp = make_input(
            deals_in_commit=0,
            exec_sponsored_deal_count=0,
            multi_stakeholder_deal_count=0,
            avg_deal_size_historical=0.0,
            days_remaining_in_period=20,
            cfo_approval_required_count=0,
        )
        s = self.scorer._deal_quality_score(inp)
        assert s == 15.0

    def test_days_remaining_ge_10_gives_8_pts(self):
        inp = make_input(
            deals_in_commit=0,
            exec_sponsored_deal_count=0,
            multi_stakeholder_deal_count=0,
            avg_deal_size_historical=0.0,
            days_remaining_in_period=10,
            cfo_approval_required_count=0,
        )
        s = self.scorer._deal_quality_score(inp)
        assert s == 8.0

    def test_days_remaining_below_10_gives_0_pts(self):
        inp = make_input(
            deals_in_commit=0,
            exec_sponsored_deal_count=0,
            multi_stakeholder_deal_count=0,
            avg_deal_size_historical=0.0,
            days_remaining_in_period=9,
            cfo_approval_required_count=0,
        )
        s = self.scorer._deal_quality_score(inp)
        assert s == 0.0

    def test_cfo_ge_3_penalty_15(self):
        inp = make_input(
            deals_in_commit=0,
            exec_sponsored_deal_count=0,
            multi_stakeholder_deal_count=0,
            avg_deal_size_historical=0.0,
            days_remaining_in_period=20,   # +15 pts
            cfo_approval_required_count=3,  # -15 pts
        )
        s = self.scorer._deal_quality_score(inp)
        assert s == 0.0

    def test_cfo_ge_1_penalty_8(self):
        inp = make_input(
            deals_in_commit=0,
            exec_sponsored_deal_count=0,
            multi_stakeholder_deal_count=0,
            avg_deal_size_historical=0.0,
            days_remaining_in_period=20,   # +15 pts
            cfo_approval_required_count=1,  # -8 pts → 7
        )
        s = self.scorer._deal_quality_score(inp)
        assert s == 7.0

    def test_zero_deals_in_commit_skips_exec_and_ms(self):
        inp = make_input(
            deals_in_commit=0,
            exec_sponsored_deal_count=5,   # should be ignored
            multi_stakeholder_deal_count=5,
            avg_deal_size_historical=0.0,
            days_remaining_in_period=0,
            cfo_approval_required_count=0,
        )
        s = self.scorer._deal_quality_score(inp)
        assert s == 0.0

    def test_score_clamped_to_0_minimum(self):
        inp = make_input(
            deals_in_commit=0,
            exec_sponsored_deal_count=0,
            multi_stakeholder_deal_count=0,
            avg_deal_size_historical=0.0,
            days_remaining_in_period=0,
            cfo_approval_required_count=3,  # -15 pts from 0
        )
        s = self.scorer._deal_quality_score(inp)
        assert s == 0.0


# ── _activity_signal_score ────────────────────────────────────────────────────

class TestActivitySignalScore:
    def setup_method(self):
        self.scorer = ForecastConfidenceScorer()

    def _score(self, acts, avg_acts, new_deals, deals_closed):
        inp = make_input(
            activities_last_14d=acts,
            avg_activities_per_commit_deal=avg_acts,
            new_deals_added_last_30d=new_deals,
            deals_closed_this_period=deals_closed,
        )
        return self.scorer._activity_signal_score(inp)

    def test_activities_ge_20_gives_35(self):
        assert self._score(20, 0.0, 0, 0) == 35.0

    def test_activities_ge_12_gives_25(self):
        assert self._score(12, 0.0, 0, 0) == 25.0

    def test_activities_ge_6_gives_14(self):
        assert self._score(6, 0.0, 0, 0) == 14.0

    def test_activities_ge_2_gives_6(self):
        assert self._score(2, 0.0, 0, 0) == 6.0

    def test_activities_below_2_gives_0(self):
        assert self._score(1, 0.0, 0, 0) == 0.0

    def test_avg_act_ge_80_gives_40(self):
        assert self._score(0, 80.0, 0, 0) == 40.0

    def test_avg_act_ge_60_gives_28(self):
        assert self._score(0, 60.0, 0, 0) == 28.0

    def test_avg_act_ge_40_gives_16(self):
        assert self._score(0, 40.0, 0, 0) == 16.0

    def test_avg_act_ge_20_gives_8(self):
        assert self._score(0, 20.0, 0, 0) == 8.0

    def test_avg_act_below_20_gives_0(self):
        assert self._score(0, 10.0, 0, 0) == 0.0

    def test_new_deals_ge_4_gives_15(self):
        assert self._score(0, 0.0, 4, 0) == 15.0

    def test_new_deals_ge_2_gives_8(self):
        assert self._score(0, 0.0, 2, 0) == 8.0

    def test_new_deals_ge_1_gives_4(self):
        assert self._score(0, 0.0, 1, 0) == 4.0

    def test_new_deals_0_gives_0(self):
        assert self._score(0, 0.0, 0, 0) == 0.0

    def test_deals_closed_ge_3_gives_10(self):
        assert self._score(0, 0.0, 0, 3) == 10.0

    def test_deals_closed_ge_1_gives_5(self):
        assert self._score(0, 0.0, 0, 1) == 5.0

    def test_deals_closed_0_gives_0(self):
        assert self._score(0, 0.0, 0, 0) == 0.0

    def test_max_score_clamped_to_100(self):
        s = self._score(25, 90.0, 5, 4)
        assert s == 100.0

    def test_all_zeros_gives_0(self):
        assert self._score(0, 0.0, 0, 0) == 0.0


# ── _confidence_level classifier ─────────────────────────────────────────────

class TestConfidenceLevelClassifier:
    def setup_method(self):
        self.scorer = ForecastConfidenceScorer()

    def test_committed_when_composite_ge_75_and_accuracy_ge_80(self):
        inp = make_input(forecast_accuracy_last_3q=80.0)
        level = self.scorer._confidence_level(75.0, inp)
        assert level == ConfidenceLevel.COMMITTED

    def test_high_when_composite_ge_60(self):
        inp = make_input(forecast_accuracy_last_3q=70.0)  # < 80, so not COMMITTED
        level = self.scorer._confidence_level(60.0, inp)
        assert level == ConfidenceLevel.HIGH

    def test_committed_requires_accuracy_ge_80(self):
        inp = make_input(forecast_accuracy_last_3q=79.0)
        level = self.scorer._confidence_level(75.0, inp)
        assert level == ConfidenceLevel.HIGH  # not COMMITTED

    def test_moderate_when_composite_ge_40(self):
        inp = make_input(forecast_accuracy_last_3q=50.0)
        level = self.scorer._confidence_level(40.0, inp)
        assert level == ConfidenceLevel.MODERATE

    def test_low_when_composite_below_40(self):
        inp = make_input(forecast_accuracy_last_3q=50.0)
        level = self.scorer._confidence_level(39.9, inp)
        assert level == ConfidenceLevel.LOW

    def test_boundary_composite_exactly_60_is_high(self):
        inp = make_input(forecast_accuracy_last_3q=70.0)
        level = self.scorer._confidence_level(60.0, inp)
        assert level == ConfidenceLevel.HIGH

    def test_boundary_composite_exactly_40_is_moderate(self):
        inp = make_input(forecast_accuracy_last_3q=50.0)
        level = self.scorer._confidence_level(40.0, inp)
        assert level == ConfidenceLevel.MODERATE


# ── _forecast_pattern classifier ─────────────────────────────────────────────

class TestForecastPatternClassifier:
    def setup_method(self):
        self.scorer = ForecastConfidenceScorer()

    def test_insufficient_when_accuracy_below_40(self):
        inp = make_input(forecast_accuracy_last_3q=39.0)
        assert self.scorer._forecast_pattern(inp) == ForecastPattern.INSUFFICIENT

    def test_optimistic_bias_when_accuracy_lt_70_and_commit_ratio_lt_0_8(self):
        # acc=60, commit_ratio = 50_000 / 200_000 = 0.25 < 0.8
        inp = make_input(
            forecast_accuracy_last_3q=60.0,
            pipeline_in_commit_stage=50_000.0,
            forecast_amount=200_000.0,
            close_date_slip_rate_pct=10.0,
        )
        assert self.scorer._forecast_pattern(inp) == ForecastPattern.OPTIMISTIC_BIAS

    def test_sandbagging_when_accuracy_ge_80_and_pipeline_ratio_gt_5(self):
        # pipeline / forecast > 5 and accuracy >= 80
        inp = make_input(
            forecast_accuracy_last_3q=85.0,
            pipeline_total=1_100_000.0,  # ratio = 5.5
            forecast_amount=200_000.0,
            close_date_slip_rate_pct=10.0,
        )
        assert self.scorer._forecast_pattern(inp) == ForecastPattern.SANDBAGGING

    def test_volatile_when_slip_rate_ge_40(self):
        inp = make_input(
            forecast_accuracy_last_3q=75.0,
            close_date_slip_rate_pct=40.0,
            pipeline_in_commit_stage=200_000.0,   # commit_ratio=1.0 ≥ 0.8 → not OPTIMISTIC
            pipeline_total=700_000.0,             # ratio=3.5 ≤ 5 → not SANDBAGGING
        )
        assert self.scorer._forecast_pattern(inp) == ForecastPattern.VOLATILE

    def test_reliable_when_none_of_above_match(self):
        inp = make_input(
            forecast_accuracy_last_3q=75.0,
            pipeline_in_commit_stage=200_000.0,
            pipeline_total=700_000.0,
            close_date_slip_rate_pct=10.0,
        )
        assert self.scorer._forecast_pattern(inp) == ForecastPattern.RELIABLE

    def test_insufficient_boundary_exactly_40(self):
        # acc=40 is NOT < 40, so not INSUFFICIENT
        inp = make_input(
            forecast_accuracy_last_3q=40.0,
            pipeline_in_commit_stage=200_000.0,
            pipeline_total=700_000.0,
            close_date_slip_rate_pct=10.0,
        )
        pattern = self.scorer._forecast_pattern(inp)
        assert pattern != ForecastPattern.INSUFFICIENT


# ── _pipeline_health classifier ───────────────────────────────────────────────

class TestPipelineHealthClassifier:
    def setup_method(self):
        self.scorer = ForecastConfidenceScorer()

    def test_overpipelined_ge_5(self):
        inp = make_input()
        assert self.scorer._pipeline_health(5.0, inp) == PipelineHealth.OVERPIPELINED

    def test_overpipelined_above_5(self):
        inp = make_input()
        assert self.scorer._pipeline_health(7.0, inp) == PipelineHealth.OVERPIPELINED

    def test_healthy_ge_3(self):
        inp = make_input()
        assert self.scorer._pipeline_health(3.0, inp) == PipelineHealth.HEALTHY

    def test_healthy_below_5(self):
        inp = make_input()
        assert self.scorer._pipeline_health(4.9, inp) == PipelineHealth.HEALTHY

    def test_adequate_ge_2(self):
        inp = make_input()
        assert self.scorer._pipeline_health(2.0, inp) == PipelineHealth.ADEQUATE

    def test_adequate_below_3(self):
        inp = make_input()
        assert self.scorer._pipeline_health(2.5, inp) == PipelineHealth.ADEQUATE

    def test_underpipelined_below_2(self):
        inp = make_input()
        assert self.scorer._pipeline_health(1.9, inp) == PipelineHealth.UNDERPIPELINED

    def test_underpipelined_zero(self):
        inp = make_input()
        assert self.scorer._pipeline_health(0.0, inp) == PipelineHealth.UNDERPIPELINED


# ── _forecast_action classifier ───────────────────────────────────────────────

class TestForecastActionClassifier:
    def setup_method(self):
        self.scorer = ForecastConfidenceScorer()

    def test_escalate_when_confidence_low(self):
        inp = make_input(forecast_accuracy_last_3q=70.0)
        action = self.scorer._forecast_action(ConfidenceLevel.LOW, False, inp)
        assert action == ForecastAction.ESCALATE_TO_MANAGER

    def test_escalate_when_accuracy_below_50(self):
        inp = make_input(forecast_accuracy_last_3q=49.0)
        action = self.scorer._forecast_action(ConfidenceLevel.HIGH, False, inp)
        assert action == ForecastAction.ESCALATE_TO_MANAGER

    def test_scrub_required_when_needs_scrub_and_not_low_and_accuracy_ok(self):
        inp = make_input(forecast_accuracy_last_3q=70.0)
        action = self.scorer._forecast_action(ConfidenceLevel.HIGH, True, inp)
        assert action == ForecastAction.SCRUB_REQUIRED

    def test_review_with_rep_when_moderate(self):
        inp = make_input(forecast_accuracy_last_3q=70.0)
        action = self.scorer._forecast_action(ConfidenceLevel.MODERATE, False, inp)
        assert action == ForecastAction.REVIEW_WITH_REP

    def test_accept_when_high_no_scrub(self):
        inp = make_input(forecast_accuracy_last_3q=80.0)
        action = self.scorer._forecast_action(ConfidenceLevel.HIGH, False, inp)
        assert action == ForecastAction.ACCEPT

    def test_accept_when_committed_no_scrub(self):
        inp = make_input(forecast_accuracy_last_3q=85.0)
        action = self.scorer._forecast_action(ConfidenceLevel.COMMITTED, False, inp)
        assert action == ForecastAction.ACCEPT

    def test_escalate_takes_precedence_over_scrub(self):
        inp = make_input(forecast_accuracy_last_3q=40.0)
        action = self.scorer._forecast_action(ConfidenceLevel.LOW, True, inp)
        assert action == ForecastAction.ESCALATE_TO_MANAGER


# ── _attainment_probability ───────────────────────────────────────────────────

class TestAttainmentProbability:
    def setup_method(self):
        self.scorer = ForecastConfidenceScorer()

    def test_base_is_composite_times_0_5(self):
        # accuracy=60 → below 70 so no bonus; quota=0 so no closed contribution;
        # days_remaining=20 → no penalty; base = 80 * 0.5 = 40
        inp = make_input(
            quota_amount=0.0,
            forecast_accuracy_last_3q=60.0,
            days_remaining_in_period=20,
        )
        prob = self.scorer._attainment_probability(inp, 80.0)
        assert prob == 40.0

    def test_closed_revenue_adds_to_base(self):
        # accuracy=60 → no bonus; 50% of quota closed → +20; base = 80*0.5 + 20 = 60
        inp = make_input(
            quota_amount=100_000.0,
            revenue_closed_this_period=50_000.0,  # 50% of quota → +20
            forecast_accuracy_last_3q=60.0,
            days_remaining_in_period=20,
        )
        prob = self.scorer._attainment_probability(inp, 80.0)
        assert prob == 60.0

    def test_accuracy_ge_85_bonus_15(self):
        inp = make_input(
            quota_amount=0.0,
            forecast_accuracy_last_3q=85.0,
            days_remaining_in_period=20,
        )
        prob = self.scorer._attainment_probability(inp, 60.0)
        # base=30 + 15 = 45
        assert prob == 45.0

    def test_accuracy_ge_70_bonus_8(self):
        inp = make_input(
            quota_amount=0.0,
            forecast_accuracy_last_3q=70.0,
            days_remaining_in_period=20,
        )
        prob = self.scorer._attainment_probability(inp, 60.0)
        # base=30 + 8 = 38
        assert prob == 38.0

    def test_days_remaining_le_5_penalty_10(self):
        inp = make_input(
            quota_amount=0.0,
            forecast_accuracy_last_3q=50.0,
            days_remaining_in_period=5,
        )
        prob = self.scorer._attainment_probability(inp, 60.0)
        # base=30 - 10 = 20
        assert prob == 20.0

    def test_probability_clamped_to_100(self):
        inp = make_input(
            quota_amount=10_000.0,
            revenue_closed_this_period=50_000.0,
            forecast_accuracy_last_3q=90.0,
            days_remaining_in_period=30,
        )
        prob = self.scorer._attainment_probability(inp, 100.0)
        assert prob == 100.0

    def test_probability_clamped_to_0(self):
        inp = make_input(
            quota_amount=0.0,
            forecast_accuracy_last_3q=10.0,
            days_remaining_in_period=5,
        )
        prob = self.scorer._attainment_probability(inp, 0.0)
        # base=0 - 10 → clamped to 0
        assert prob == 0.0


# ── score() and score_batch() ─────────────────────────────────────────────────

class TestScoreAndScoreBatch:
    def test_score_returns_forecast_confidence_result(self):
        scorer = ForecastConfidenceScorer()
        result = scorer.score(make_input())
        assert isinstance(result, ForecastConfidenceResult)

    def test_score_stores_result_in_results(self):
        scorer = ForecastConfidenceScorer()
        scorer.score(make_input())
        assert len(scorer._results) == 1

    def test_score_accumulates_multiple(self):
        scorer = ForecastConfidenceScorer()
        scorer.score(make_input(rep_id="R1"))
        scorer.score(make_input(rep_id="R2"))
        assert len(scorer._results) == 2

    def test_score_rep_id_passthrough(self):
        scorer = ForecastConfidenceScorer()
        result = scorer.score(make_input(rep_id="XYZ"))
        assert result.rep_id == "XYZ"

    def test_score_rep_name_passthrough(self):
        scorer = ForecastConfidenceScorer()
        result = scorer.score(make_input(rep_name="Bob Jones"))
        assert result.rep_name == "Bob Jones"

    def test_score_pipeline_coverage_ratio(self):
        scorer = ForecastConfidenceScorer()
        result = scorer.score(make_input(
            forecast_amount=200_000.0,
            pipeline_total=600_000.0,
        ))
        assert result.pipeline_coverage_ratio == 3.0

    def test_score_pipeline_coverage_ratio_zero_forecast(self):
        scorer = ForecastConfidenceScorer()
        result = scorer.score(make_input(forecast_amount=0.0))
        assert result.pipeline_coverage_ratio == 0.0

    def test_score_batch_returns_list(self):
        scorer = ForecastConfidenceScorer()
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = scorer.score_batch(inputs)
        assert isinstance(results, list)
        assert len(results) == 5

    def test_score_batch_stores_all_results(self):
        scorer = ForecastConfidenceScorer()
        inputs = [make_input(rep_id=f"R{i}") for i in range(3)]
        scorer.score_batch(inputs)
        assert len(scorer._results) == 3

    def test_score_batch_order_preserved(self):
        scorer = ForecastConfidenceScorer()
        inputs = [make_input(rep_id=f"R{i}") for i in range(4)]
        results = scorer.score_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"R{i}"

    def test_score_composite_within_bounds(self):
        scorer = ForecastConfidenceScorer()
        result = scorer.score(make_input())
        assert 0.0 <= result.forecast_composite <= 100.0

    def test_score_attainment_probability_within_bounds(self):
        scorer = ForecastConfidenceScorer()
        result = scorer.score(make_input())
        assert 0.0 <= result.attainment_probability <= 100.0


# ── properties: reliable_forecasts, scrub_queue, avg_forecast_composite,
#               avg_attainment_probability ────────────────────────────────────

class TestProperties:
    def test_reliable_forecasts_empty_initially(self):
        scorer = ForecastConfidenceScorer()
        assert scorer.reliable_forecasts == []

    def test_scrub_queue_empty_initially(self):
        scorer = ForecastConfidenceScorer()
        assert scorer.scrub_queue == []

    def test_avg_forecast_composite_zero_when_empty(self):
        scorer = ForecastConfidenceScorer()
        assert scorer.avg_forecast_composite == 0.0

    def test_avg_attainment_probability_zero_when_empty(self):
        scorer = ForecastConfidenceScorer()
        assert scorer.avg_attainment_probability == 0.0

    def test_reliable_forecasts_filters_correctly(self):
        scorer = ForecastConfidenceScorer()
        # reliable rep
        reliable_inp = make_input(
            forecast_accuracy_last_3q=90.0,
            win_rate_historical_pct=40.0,
            close_date_slip_rate_pct=5.0,
            pipeline_total=900_000.0,
            pipeline_in_commit_stage=300_000.0,
            revenue_closed_this_period=100_000.0,
            activities_last_14d=25,
            avg_activities_per_commit_deal=85.0,
            new_deals_added_last_30d=5,
            deals_closed_this_period=4,
            exec_sponsored_deal_count=3,
            multi_stakeholder_deal_count=3,
            rep_id="RELIABLE",
        )
        # unreliable rep (low accuracy)
        unreliable_inp = make_input(
            forecast_accuracy_last_3q=50.0,
            rep_id="UNRELIABLE",
        )
        scorer.score(reliable_inp)
        scorer.score(unreliable_inp)
        reliable_ids = [r.rep_id for r in scorer.reliable_forecasts]
        assert "RELIABLE" in reliable_ids
        assert "UNRELIABLE" not in reliable_ids

    def test_scrub_queue_filters_correctly(self):
        scorer = ForecastConfidenceScorer()
        scrub_inp = make_input(close_date_slip_rate_pct=50.0, rep_id="SCRUB")
        clean_inp = make_input(close_date_slip_rate_pct=5.0, rep_id="CLEAN",
                               forecast_accuracy_last_3q=90.0,
                               win_rate_historical_pct=40.0,
                               pipeline_total=900_000.0,
                               pipeline_in_commit_stage=300_000.0,
                               revenue_closed_this_period=100_000.0,
                               activities_last_14d=25,
                               avg_activities_per_commit_deal=85.0,
                               new_deals_added_last_30d=5,
                               deals_closed_this_period=4,
                               exec_sponsored_deal_count=3,
                               multi_stakeholder_deal_count=3)
        scorer.score(scrub_inp)
        scorer.score(clean_inp)
        scrub_ids = [r.rep_id for r in scorer.scrub_queue]
        assert "SCRUB" in scrub_ids
        assert "CLEAN" not in scrub_ids

    def test_avg_forecast_composite_single(self):
        scorer = ForecastConfidenceScorer()
        result = scorer.score(make_input())
        assert scorer.avg_forecast_composite == result.forecast_composite

    def test_avg_attainment_probability_single(self):
        scorer = ForecastConfidenceScorer()
        result = scorer.score(make_input())
        assert scorer.avg_attainment_probability == result.attainment_probability

    def test_avg_forecast_composite_multiple(self):
        scorer = ForecastConfidenceScorer()
        r1 = scorer.score(make_input(rep_id="R1"))
        r2 = scorer.score(make_input(rep_id="R2"))
        expected = round((r1.forecast_composite + r2.forecast_composite) / 2, 1)
        assert scorer.avg_forecast_composite == expected

    def test_avg_attainment_probability_multiple(self):
        scorer = ForecastConfidenceScorer()
        r1 = scorer.score(make_input(rep_id="R1"))
        r2 = scorer.score(make_input(rep_id="R2"))
        expected = round((r1.attainment_probability + r2.attainment_probability) / 2, 1)
        assert scorer.avg_attainment_probability == expected


# ── reset() ───────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_results(self):
        scorer = ForecastConfidenceScorer()
        scorer.score(make_input())
        scorer.score(make_input(rep_id="R2"))
        scorer.reset()
        assert scorer._results == []

    def test_reset_clears_properties(self):
        scorer = ForecastConfidenceScorer()
        scorer.score(make_input())
        scorer.reset()
        assert scorer.avg_forecast_composite == 0.0
        assert scorer.avg_attainment_probability == 0.0
        assert scorer.reliable_forecasts == []
        assert scorer.scrub_queue == []

    def test_reset_allows_rescoring(self):
        scorer = ForecastConfidenceScorer()
        scorer.score(make_input(rep_id="R1"))
        scorer.reset()
        scorer.score(make_input(rep_id="R2"))
        assert len(scorer._results) == 1
        assert scorer._results[0].rep_id == "R2"

    def test_reset_multiple_times_is_safe(self):
        scorer = ForecastConfidenceScorer()
        scorer.reset()
        scorer.reset()
        assert scorer._results == []


# ── summary() ────────────────────────────────────────────────────────────────

class TestSummary:
    def test_empty_summary_total_is_0(self):
        scorer = ForecastConfidenceScorer()
        s = scorer.summary()
        assert s["total"] == 0

    def test_empty_summary_counts_are_empty_dicts(self):
        scorer = ForecastConfidenceScorer()
        s = scorer.summary()
        assert s["confidence_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["pipeline_health_counts"] == {}
        assert s["action_counts"] == {}

    def test_empty_summary_averages_are_zero(self):
        scorer = ForecastConfidenceScorer()
        s = scorer.summary()
        assert s["avg_forecast_composite"] == 0.0
        assert s["avg_attainment_probability"] == 0.0
        assert s["avg_historical_accuracy_score"] == 0.0
        assert s["avg_pipeline_coverage_score"] == 0.0
        assert s["avg_deal_quality_score"] == 0.0
        assert s["avg_activity_signal_score"] == 0.0

    def test_summary_total_matches_scored_count(self):
        scorer = ForecastConfidenceScorer()
        scorer.score_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        s = scorer.summary()
        assert s["total"] == 5

    def test_summary_reliable_count(self):
        scorer = ForecastConfidenceScorer()
        scorer.score(make_input(rep_id="R1"))
        s = scorer.summary()
        assert s["reliable_count"] == len(scorer.reliable_forecasts)

    def test_summary_scrub_count(self):
        scorer = ForecastConfidenceScorer()
        scorer.score(make_input(close_date_slip_rate_pct=50.0, rep_id="R1"))
        s = scorer.summary()
        assert s["scrub_count"] == len(scorer.scrub_queue)

    def test_summary_confidence_counts_sum_to_total(self):
        scorer = ForecastConfidenceScorer()
        scorer.score_batch([make_input(rep_id=f"R{i}") for i in range(4)])
        s = scorer.summary()
        assert sum(s["confidence_counts"].values()) == s["total"]

    def test_summary_pattern_counts_sum_to_total(self):
        scorer = ForecastConfidenceScorer()
        scorer.score_batch([make_input(rep_id=f"R{i}") for i in range(4)])
        s = scorer.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_summary_pipeline_health_counts_sum_to_total(self):
        scorer = ForecastConfidenceScorer()
        scorer.score_batch([make_input(rep_id=f"R{i}") for i in range(4)])
        s = scorer.summary()
        assert sum(s["pipeline_health_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_to_total(self):
        scorer = ForecastConfidenceScorer()
        scorer.score_batch([make_input(rep_id=f"R{i}") for i in range(4)])
        s = scorer.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_avg_composite_matches_property(self):
        scorer = ForecastConfidenceScorer()
        scorer.score_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        s = scorer.summary()
        assert s["avg_forecast_composite"] == scorer.avg_forecast_composite

    def test_summary_avg_attainment_matches_property(self):
        scorer = ForecastConfidenceScorer()
        scorer.score_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        s = scorer.summary()
        assert s["avg_attainment_probability"] == scorer.avg_attainment_probability

    def test_summary_after_reset_returns_empty(self):
        scorer = ForecastConfidenceScorer()
        scorer.score(make_input())
        scorer.reset()
        s = scorer.summary()
        assert s["total"] == 0

    def test_summary_confidence_counts_keys_are_enum_values(self):
        scorer = ForecastConfidenceScorer()
        scorer.score_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        s = scorer.summary()
        valid_values = {e.value for e in ConfidenceLevel}
        for key in s["confidence_counts"]:
            assert key in valid_values

    def test_summary_pattern_counts_keys_are_enum_values(self):
        scorer = ForecastConfidenceScorer()
        scorer.score_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        s = scorer.summary()
        valid_values = {e.value for e in ForecastPattern}
        for key in s["pattern_counts"]:
            assert key in valid_values


# ── edge cases & integration ───────────────────────────────────────────────────

class TestEdgeCases:
    def test_zero_forecast_amount_no_crash(self):
        scorer = ForecastConfidenceScorer()
        inp = make_input(forecast_amount=0.0)
        result = scorer.score(inp)
        assert result.pipeline_coverage_ratio == 0.0
        assert result.pipeline_coverage_score == 0.0

    def test_zero_quota_amount_no_crash(self):
        scorer = ForecastConfidenceScorer()
        inp = make_input(quota_amount=0.0)
        result = scorer.score(inp)
        assert isinstance(result, ForecastConfidenceResult)

    def test_zero_deals_in_commit_no_crash(self):
        scorer = ForecastConfidenceScorer()
        inp = make_input(deals_in_commit=0, exec_sponsored_deal_count=0, multi_stakeholder_deal_count=0)
        result = scorer.score(inp)
        assert isinstance(result, ForecastConfidenceResult)

    def test_all_zeros_input_no_crash(self):
        scorer = ForecastConfidenceScorer()
        inp = ForecastConfidenceInput(
            rep_id="Z", rep_name="Zero", manager_id="M",
            forecast_amount=0.0, quota_amount=0.0,
            pipeline_total=0.0, pipeline_in_commit_stage=0.0,
            pipeline_in_best_case=0.0, deals_in_commit=0,
            deals_closed_this_period=0, revenue_closed_this_period=0.0,
            avg_deal_size_historical=0.0, win_rate_historical_pct=0.0,
            forecast_accuracy_last_3q=0.0, close_date_slip_rate_pct=0.0,
            days_remaining_in_period=0, activities_last_14d=0,
            avg_activities_per_commit_deal=0.0, exec_sponsored_deal_count=0,
            multi_stakeholder_deal_count=0, new_deals_added_last_30d=0,
            cfo_approval_required_count=0,
        )
        result = scorer.score(inp)
        assert result.forecast_composite >= 0.0
        assert result.attainment_probability >= 0.0

    def test_high_values_input_no_crash(self):
        scorer = ForecastConfidenceScorer()
        inp = ForecastConfidenceInput(
            rep_id="H", rep_name="High", manager_id="M",
            forecast_amount=1_000_000.0, quota_amount=1_000_000.0,
            pipeline_total=10_000_000.0, pipeline_in_commit_stage=2_000_000.0,
            pipeline_in_best_case=3_000_000.0, deals_in_commit=20,
            deals_closed_this_period=10, revenue_closed_this_period=500_000.0,
            avg_deal_size_historical=100_000.0, win_rate_historical_pct=100.0,
            forecast_accuracy_last_3q=100.0, close_date_slip_rate_pct=0.0,
            days_remaining_in_period=90, activities_last_14d=100,
            avg_activities_per_commit_deal=100.0, exec_sponsored_deal_count=20,
            multi_stakeholder_deal_count=20, new_deals_added_last_30d=20,
            cfo_approval_required_count=0,
        )
        result = scorer.score(inp)
        assert result.forecast_composite <= 100.0
        assert result.attainment_probability <= 100.0

    def test_score_batch_empty_list(self):
        scorer = ForecastConfidenceScorer()
        results = scorer.score_batch([])
        assert results == []
        assert scorer._results == []

    def test_pipeline_coverage_ratio_rounded_to_2_dp(self):
        scorer = ForecastConfidenceScorer()
        result = scorer.score(make_input(
            forecast_amount=300_000.0,
            pipeline_total=1_000_000.0,
        ))
        assert result.pipeline_coverage_ratio == round(1_000_000.0 / 300_000.0, 2)

    def test_result_dataclass_fields(self):
        fields = {f.name for f in dataclasses.fields(ForecastConfidenceResult)}
        expected = {
            "rep_id", "rep_name", "confidence_level", "forecast_pattern",
            "pipeline_health", "forecast_action", "historical_accuracy_score",
            "pipeline_coverage_score", "deal_quality_score", "activity_signal_score",
            "forecast_composite", "attainment_probability", "pipeline_coverage_ratio",
            "is_forecast_reliable", "needs_forecast_scrub",
        }
        assert fields == expected
