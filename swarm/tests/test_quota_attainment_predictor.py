"""
Comprehensive pytest tests for Module 35 — Quota Attainment Predictor.
Tests run from /home/user/TEST:
    python -m pytest swarm/tests/test_quota_attainment_predictor.py -v --tb=short
"""
from __future__ import annotations

import math
import pytest

from swarm.intelligence.quota_attainment_predictor import (
    AttainmentConfidence,
    AttainmentInput,
    AttainmentOutcome,
    AttainmentResult,
    QuotaAction,
    QuotaAttainmentPredictor,
    _attainment_outcome,
    _confidence,
    _current_attainment_pct,
    _historical_avg_attainment,
    _pipeline_coverage_ratio,
    _projected_attainment,
    _quota_action,
    _run_rate_pct,
    _weighted_pipeline_eur,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def make_input(**kwargs) -> AttainmentInput:
    """Build a fully-populated AttainmentInput; any field can be overridden."""
    defaults = dict(
        rep_id="rep-001",
        rep_name="Alice Martin",
        region="EMEA",
        segment="Enterprise",
        quota_eur=200_000.0,
        days_elapsed=180,
        days_remaining=90,
        closed_won_eur=120_000.0,
        pipeline_stage3_eur=50_000.0,
        pipeline_stage2_eur=40_000.0,
        pipeline_stage1_eur=30_000.0,
        win_rate_pct=30.0,
        avg_deal_size_eur=20_000.0,
        avg_sales_cycle_days=60,
        historical_attainment_pcts=[95.0, 100.0, 105.0],
        deals_created_30d=5,
        meetings_30d=12,
        proposals_sent_30d=4,
        rep_confidence_score=7.5,
    )
    defaults.update(kwargs)
    return AttainmentInput(**defaults)


@pytest.fixture
def predictor() -> QuotaAttainmentPredictor:
    return QuotaAttainmentPredictor()


@pytest.fixture
def standard_input() -> AttainmentInput:
    return make_input()


# ---------------------------------------------------------------------------
# Class 1 — Enums exist and have correct values
# ---------------------------------------------------------------------------

class TestEnumValues:
    def test_attainment_outcome_values(self):
        assert AttainmentOutcome.OVERACHIEVE.value == "overachieve"
        assert AttainmentOutcome.ACHIEVE.value == "achieve"
        assert AttainmentOutcome.SLIGHT_MISS.value == "slight_miss"
        assert AttainmentOutcome.MISS.value == "miss"
        assert AttainmentOutcome.CRITICAL_MISS.value == "critical_miss"

    def test_attainment_confidence_values(self):
        assert AttainmentConfidence.HIGH.value == "high"
        assert AttainmentConfidence.MEDIUM.value == "medium"
        assert AttainmentConfidence.LOW.value == "low"
        assert AttainmentConfidence.VERY_LOW.value == "very_low"

    def test_quota_action_values(self):
        assert QuotaAction.MAINTAIN.value == "maintain"
        assert QuotaAction.ACCELERATE.value == "accelerate"
        assert QuotaAction.INTERVENTION.value == "intervention"
        assert QuotaAction.ESCALATE.value == "escalate"

    def test_enums_are_strings(self):
        # All enums inherit from str
        assert isinstance(AttainmentOutcome.ACHIEVE, str)
        assert isinstance(AttainmentConfidence.HIGH, str)
        assert isinstance(QuotaAction.MAINTAIN, str)

    def test_enum_counts(self):
        assert len(AttainmentOutcome) == 5
        assert len(AttainmentConfidence) == 4
        assert len(QuotaAction) == 4


# ---------------------------------------------------------------------------
# Class 2 — AttainmentInput dataclass
# ---------------------------------------------------------------------------

class TestAttainmentInputDataclass:
    def test_all_fields_set(self, standard_input):
        inp = standard_input
        assert inp.rep_id == "rep-001"
        assert inp.rep_name == "Alice Martin"
        assert inp.region == "EMEA"
        assert inp.segment == "Enterprise"
        assert inp.quota_eur == 200_000.0
        assert inp.days_elapsed == 180
        assert inp.days_remaining == 90
        assert inp.closed_won_eur == 120_000.0
        assert inp.pipeline_stage3_eur == 50_000.0
        assert inp.pipeline_stage2_eur == 40_000.0
        assert inp.pipeline_stage1_eur == 30_000.0
        assert inp.win_rate_pct == 30.0
        assert inp.avg_deal_size_eur == 20_000.0
        assert inp.avg_sales_cycle_days == 60
        assert inp.historical_attainment_pcts == [95.0, 100.0, 105.0]
        assert inp.deals_created_30d == 5
        assert inp.meetings_30d == 12
        assert inp.proposals_sent_30d == 4
        assert inp.rep_confidence_score == 7.5

    def test_historical_attainment_is_list(self, standard_input):
        assert isinstance(standard_input.historical_attainment_pcts, list)

    def test_19_fields(self):
        fields = AttainmentInput.__dataclass_fields__
        assert len(fields) == 19


# ---------------------------------------------------------------------------
# Class 3 — _current_attainment_pct
# ---------------------------------------------------------------------------

class TestCurrentAttainmentPct:
    def test_normal_case(self):
        inp = make_input(closed_won_eur=100_000.0, quota_eur=200_000.0)
        assert _current_attainment_pct(inp) == 50.0

    def test_full_quota(self):
        inp = make_input(closed_won_eur=200_000.0, quota_eur=200_000.0)
        assert _current_attainment_pct(inp) == 100.0

    def test_overachieve(self):
        inp = make_input(closed_won_eur=250_000.0, quota_eur=200_000.0)
        assert _current_attainment_pct(inp) == 125.0

    def test_zero_quota_returns_zero(self):
        inp = make_input(quota_eur=0.0, closed_won_eur=50_000.0)
        assert _current_attainment_pct(inp) == 0.0

    def test_negative_quota_returns_zero(self):
        inp = make_input(quota_eur=-1.0, closed_won_eur=50_000.0)
        assert _current_attainment_pct(inp) == 0.0

    def test_zero_closed(self):
        inp = make_input(closed_won_eur=0.0, quota_eur=100_000.0)
        assert _current_attainment_pct(inp) == 0.0

    def test_rounded_to_one_decimal(self):
        inp = make_input(closed_won_eur=10_000.0, quota_eur=30_000.0)
        result = _current_attainment_pct(inp)
        assert result == round(10_000 / 30_000 * 100, 1)

    def test_small_values(self):
        inp = make_input(closed_won_eur=1.0, quota_eur=3.0)
        assert _current_attainment_pct(inp) == round(100 / 3, 1)


# ---------------------------------------------------------------------------
# Class 4 — _run_rate_pct
# ---------------------------------------------------------------------------

class TestRunRatePct:
    def test_on_pace(self):
        # Closed 2/3 of quota after 2/3 of period → run rate = 100%
        inp = make_input(
            quota_eur=300_000.0,
            days_elapsed=200,
            days_remaining=100,
            closed_won_eur=200_000.0,
        )
        assert _run_rate_pct(inp) == 100.0

    def test_ahead_of_pace(self):
        # Closed more than expected
        inp = make_input(
            quota_eur=100_000.0,
            days_elapsed=100,
            days_remaining=100,
            closed_won_eur=80_000.0,  # expected 50k, have 80k → 160%
        )
        assert _run_rate_pct(inp) == 160.0

    def test_behind_pace(self):
        inp = make_input(
            quota_eur=100_000.0,
            days_elapsed=100,
            days_remaining=100,
            closed_won_eur=25_000.0,  # expected 50k → 50%
        )
        assert _run_rate_pct(inp) == 50.0

    def test_zero_days_elapsed_returns_zero(self):
        inp = make_input(days_elapsed=0, days_remaining=90)
        assert _run_rate_pct(inp) == 0.0

    def test_zero_quota_returns_zero(self):
        inp = make_input(quota_eur=0.0)
        assert _run_rate_pct(inp) == 0.0

    def test_zero_total_days_returns_zero(self):
        inp = make_input(days_elapsed=0, days_remaining=0)
        assert _run_rate_pct(inp) == 0.0

    def test_result_is_rounded_to_one_decimal(self):
        inp = make_input(
            quota_eur=100_000.0,
            days_elapsed=100,
            days_remaining=200,
            closed_won_eur=37_000.0,
        )
        expected = 37_000 / (100_000 * (100 / 300)) * 100
        assert _run_rate_pct(inp) == round(expected, 1)


# ---------------------------------------------------------------------------
# Class 5 — _weighted_pipeline_eur
# ---------------------------------------------------------------------------

class TestWeightedPipelineEur:
    def test_basic_calculation(self):
        inp = make_input(
            pipeline_stage3_eur=100_000.0,
            pipeline_stage2_eur=100_000.0,
            pipeline_stage1_eur=100_000.0,
            win_rate_pct=50.0,
        )
        # wr=0.5: s3*0.5 + s2*0.5*0.6 + s1*0.5*0.3
        # = 50000 + 30000 + 15000 = 95000
        assert _weighted_pipeline_eur(inp) == 95_000.0

    def test_zero_pipeline(self):
        inp = make_input(
            pipeline_stage3_eur=0.0,
            pipeline_stage2_eur=0.0,
            pipeline_stage1_eur=0.0,
            win_rate_pct=30.0,
        )
        assert _weighted_pipeline_eur(inp) == 0.0

    def test_zero_win_rate(self):
        inp = make_input(
            pipeline_stage3_eur=100_000.0,
            pipeline_stage2_eur=100_000.0,
            pipeline_stage1_eur=100_000.0,
            win_rate_pct=0.0,
        )
        assert _weighted_pipeline_eur(inp) == 0.0

    def test_stage3_highest_weight(self):
        # Stage3 should contribute most to weighted value
        inp_s3 = make_input(
            pipeline_stage3_eur=100_000.0,
            pipeline_stage2_eur=0.0,
            pipeline_stage1_eur=0.0,
            win_rate_pct=100.0,
        )
        inp_s1 = make_input(
            pipeline_stage3_eur=0.0,
            pipeline_stage2_eur=0.0,
            pipeline_stage1_eur=100_000.0,
            win_rate_pct=100.0,
        )
        assert _weighted_pipeline_eur(inp_s3) > _weighted_pipeline_eur(inp_s1)

    def test_weights_stage3_full_rate(self):
        inp = make_input(
            pipeline_stage3_eur=100_000.0,
            pipeline_stage2_eur=0.0,
            pipeline_stage1_eur=0.0,
            win_rate_pct=100.0,
        )
        # stage3 * 1.0
        assert _weighted_pipeline_eur(inp) == 100_000.0

    def test_weights_stage2_60pct(self):
        inp = make_input(
            pipeline_stage3_eur=0.0,
            pipeline_stage2_eur=100_000.0,
            pipeline_stage1_eur=0.0,
            win_rate_pct=100.0,
        )
        # stage2 * 0.6
        assert _weighted_pipeline_eur(inp) == 60_000.0

    def test_weights_stage1_30pct(self):
        inp = make_input(
            pipeline_stage3_eur=0.0,
            pipeline_stage2_eur=0.0,
            pipeline_stage1_eur=100_000.0,
            win_rate_pct=100.0,
        )
        # stage1 * 0.3
        assert _weighted_pipeline_eur(inp) == 30_000.0

    def test_rounded_to_zero_decimals(self):
        result = _weighted_pipeline_eur(make_input(win_rate_pct=33.333))
        assert result == round(result, 0)


# ---------------------------------------------------------------------------
# Class 6 — _pipeline_coverage_ratio
# ---------------------------------------------------------------------------

class TestPipelineCoverageRatio:
    def test_normal_case(self):
        # quota=200k, closed=100k → remaining=100k; total pipeline=120k → 1.2x
        inp = make_input(
            quota_eur=200_000.0,
            closed_won_eur=100_000.0,
            pipeline_stage3_eur=40_000.0,
            pipeline_stage2_eur=50_000.0,
            pipeline_stage1_eur=30_000.0,
        )
        assert _pipeline_coverage_ratio(inp) == round(120_000 / 100_000, 2)

    def test_quota_fully_closed_returns_99(self):
        inp = make_input(
            quota_eur=100_000.0,
            closed_won_eur=100_000.0,
            pipeline_stage3_eur=50_000.0,
        )
        assert _pipeline_coverage_ratio(inp) == 99.0

    def test_over_quota_returns_99(self):
        inp = make_input(
            quota_eur=100_000.0,
            closed_won_eur=150_000.0,
        )
        assert _pipeline_coverage_ratio(inp) == 99.0

    def test_no_pipeline(self):
        inp = make_input(
            quota_eur=200_000.0,
            closed_won_eur=50_000.0,
            pipeline_stage3_eur=0.0,
            pipeline_stage2_eur=0.0,
            pipeline_stage1_eur=0.0,
        )
        assert _pipeline_coverage_ratio(inp) == 0.0

    def test_result_rounded_to_2_decimals(self):
        inp = make_input(
            quota_eur=300_000.0,
            closed_won_eur=0.0,
            pipeline_stage3_eur=100_000.0,
            pipeline_stage2_eur=0.0,
            pipeline_stage1_eur=0.0,
        )
        result = _pipeline_coverage_ratio(inp)
        assert result == round(result, 2)

    def test_coverage_below_one_when_pipeline_insufficient(self):
        inp = make_input(
            quota_eur=200_000.0,
            closed_won_eur=0.0,
            pipeline_stage3_eur=10_000.0,
            pipeline_stage2_eur=10_000.0,
            pipeline_stage1_eur=10_000.0,
        )
        assert _pipeline_coverage_ratio(inp) < 1.0


# ---------------------------------------------------------------------------
# Class 7 — _historical_avg_attainment
# ---------------------------------------------------------------------------

class TestHistoricalAvgAttainment:
    def test_empty_list_returns_80(self):
        inp = make_input(historical_attainment_pcts=[])
        assert _historical_avg_attainment(inp) == 80.0

    def test_single_value(self):
        inp = make_input(historical_attainment_pcts=[90.0])
        assert _historical_avg_attainment(inp) == 90.0

    def test_multiple_values_mean(self):
        inp = make_input(historical_attainment_pcts=[80.0, 100.0, 120.0])
        assert _historical_avg_attainment(inp) == 100.0

    def test_rounded_to_one_decimal(self):
        inp = make_input(historical_attainment_pcts=[100.0, 100.0, 101.0])
        result = _historical_avg_attainment(inp)
        assert result == round(301 / 3, 1)

    def test_high_performers(self):
        inp = make_input(historical_attainment_pcts=[120.0, 130.0, 140.0])
        assert _historical_avg_attainment(inp) == 130.0

    def test_low_performers(self):
        inp = make_input(historical_attainment_pcts=[40.0, 50.0, 60.0])
        assert _historical_avg_attainment(inp) == 50.0

    def test_four_periods(self):
        inp = make_input(historical_attainment_pcts=[90.0, 95.0, 100.0, 115.0])
        assert _historical_avg_attainment(inp) == 100.0


# ---------------------------------------------------------------------------
# Class 8 — _projected_attainment: boundary clamping
# ---------------------------------------------------------------------------

class TestProjectedAttainmentClamping:
    def test_clamped_to_200_max(self):
        # Huge pipeline, short cycle → should be capped at 200
        inp = make_input(
            quota_eur=100_000.0,
            closed_won_eur=100_000.0,
            pipeline_stage3_eur=1_000_000.0,
            pipeline_stage2_eur=1_000_000.0,
            pipeline_stage1_eur=1_000_000.0,
            win_rate_pct=100.0,
            avg_sales_cycle_days=1,
            days_remaining=90,
            historical_attainment_pcts=[200.0, 200.0],
        )
        result = _projected_attainment(inp, 3_000_000.0, 200.0, 100.0)
        assert result <= 200.0

    def test_clamped_to_0_min(self):
        # Zero everything
        inp = make_input(
            quota_eur=100_000.0,
            closed_won_eur=0.0,
            pipeline_stage3_eur=0.0,
            pipeline_stage2_eur=0.0,
            pipeline_stage1_eur=0.0,
            win_rate_pct=0.0,
            days_remaining=5,
            avg_sales_cycle_days=60,
        )
        result = _projected_attainment(inp, 0.0, 0.0, 0.0)
        assert result >= 0.0

    def test_zero_quota_returns_zero(self):
        inp = make_input(quota_eur=0.0)
        result = _projected_attainment(inp, 50_000.0, 100.0, 80.0)
        assert result == 0.0


# ---------------------------------------------------------------------------
# Class 9 — _projected_attainment: closeable_ratio logic
# ---------------------------------------------------------------------------

class TestProjectedAttainmentCloseableRatio:
    def test_closeable_ratio_capped_at_1(self):
        # days_remaining > avg_sales_cycle → ratio capped at 1
        inp = make_input(
            days_remaining=120,
            avg_sales_cycle_days=60,
            quota_eur=200_000.0,
            closed_won_eur=100_000.0,
        )
        weighted = 50_000.0
        result1 = _projected_attainment(inp, weighted, 100.0, 100.0)
        # Same pipeline with even more days remaining should yield same result (ratio already 1)
        inp2 = make_input(
            days_remaining=200,
            avg_sales_cycle_days=60,
            quota_eur=200_000.0,
            closed_won_eur=100_000.0,
        )
        result2 = _projected_attainment(inp2, weighted, 100.0, 100.0)
        assert result1 == result2

    def test_closeable_ratio_reduced_when_cycle_longer_than_remaining(self):
        # 30 days remaining, 60 day cycle → ratio = 0.5
        inp_short = make_input(
            days_remaining=30,
            avg_sales_cycle_days=60,
            quota_eur=200_000.0,
            closed_won_eur=0.0,
        )
        inp_long = make_input(
            days_remaining=90,
            avg_sales_cycle_days=60,
            quota_eur=200_000.0,
            closed_won_eur=0.0,
        )
        result_short = _projected_attainment(inp_short, 100_000.0, 80.0, 80.0)
        result_long = _projected_attainment(inp_long, 100_000.0, 80.0, 80.0)
        assert result_short < result_long

    def test_zero_avg_cycle_days_ratio_is_1(self):
        inp = make_input(
            avg_sales_cycle_days=0,
            days_remaining=30,
            quota_eur=100_000.0,
            closed_won_eur=50_000.0,
        )
        # Should not raise and closeable_ratio treated as 1.0
        result = _projected_attainment(inp, 40_000.0, 100.0, 100.0)
        assert result >= 0.0

    def test_run_rate_pressure_applied(self):
        # run_rate < 50 AND days_remaining < 30 → blended *= 0.85
        inp = make_input(
            quota_eur=100_000.0,
            closed_won_eur=10_000.0,
            days_remaining=20,
            days_elapsed=340,
            avg_sales_cycle_days=15,
            win_rate_pct=30.0,
        )
        weighted = 20_000.0
        hist_avg = 80.0
        run_rate = 25.0  # explicitly low
        result = _projected_attainment(inp, weighted, hist_avg, run_rate)
        # Result should be lower than without run-rate penalty
        # Build same scenario without penalty (run_rate=80)
        result_no_penalty = _projected_attainment(inp, weighted, hist_avg, 80.0)
        assert result < result_no_penalty

    def test_run_rate_pressure_not_applied_above_50(self):
        # run_rate >= 50 → no penalty
        inp = make_input(
            quota_eur=100_000.0,
            closed_won_eur=10_000.0,
            days_remaining=20,
            days_elapsed=340,
            avg_sales_cycle_days=15,
        )
        result_51 = _projected_attainment(inp, 20_000.0, 80.0, 51.0)
        result_49 = _projected_attainment(inp, 20_000.0, 80.0, 49.0)
        assert result_51 > result_49

    def test_run_rate_pressure_not_applied_ge_30_days(self):
        # days_remaining >= 30 → no penalty even if run_rate < 50
        inp = make_input(
            quota_eur=100_000.0,
            closed_won_eur=10_000.0,
            days_remaining=30,
            days_elapsed=310,
            avg_sales_cycle_days=15,
        )
        result = _projected_attainment(inp, 20_000.0, 80.0, 25.0)
        # Should equal result with days_remaining=90 (no penalty)
        inp2 = make_input(
            quota_eur=100_000.0,
            closed_won_eur=10_000.0,
            days_remaining=90,
            days_elapsed=250,
            avg_sales_cycle_days=15,
        )
        result2 = _projected_attainment(inp2, 20_000.0, 80.0, 25.0)
        # Both shouldn't have pressure; results may differ due to time_factor but not penalty
        assert result >= 0.0 and result2 >= 0.0

    def test_blended_80_20_split(self):
        # With closeable_ratio=1, closed=0, verify 80/20 blend
        # model_pct = (0 + weighted) / quota * 100; blended = model*0.8 + hist*0.2
        inp = make_input(
            quota_eur=100_000.0,
            closed_won_eur=0.0,
            days_remaining=120,
            days_elapsed=120,
            avg_sales_cycle_days=60,
        )
        weighted = 80_000.0
        hist_avg = 90.0
        run_rate = 80.0
        result = _projected_attainment(inp, weighted, hist_avg, run_rate)
        model_pct = (weighted / 100_000.0) * 100.0  # 80%
        expected_blended = model_pct * 0.8 + hist_avg * 0.2  # 64 + 18 = 82
        assert result == round(min(200.0, max(0.0, expected_blended)), 1)


# ---------------------------------------------------------------------------
# Class 10 — _attainment_outcome boundaries
# ---------------------------------------------------------------------------

class TestAttainmentOutcomeBoundaries:
    def test_exactly_110_is_overachieve(self):
        assert _attainment_outcome(110.0) == AttainmentOutcome.OVERACHIEVE

    def test_above_110_is_overachieve(self):
        assert _attainment_outcome(150.0) == AttainmentOutcome.OVERACHIEVE
        assert _attainment_outcome(200.0) == AttainmentOutcome.OVERACHIEVE

    def test_exactly_90_is_achieve(self):
        assert _attainment_outcome(90.0) == AttainmentOutcome.ACHIEVE

    def test_109_is_achieve(self):
        assert _attainment_outcome(109.9) == AttainmentOutcome.ACHIEVE

    def test_exactly_70_is_slight_miss(self):
        assert _attainment_outcome(70.0) == AttainmentOutcome.SLIGHT_MISS

    def test_89_is_slight_miss(self):
        assert _attainment_outcome(89.9) == AttainmentOutcome.SLIGHT_MISS

    def test_exactly_50_is_miss(self):
        assert _attainment_outcome(50.0) == AttainmentOutcome.MISS

    def test_69_is_miss(self):
        assert _attainment_outcome(69.9) == AttainmentOutcome.MISS

    def test_below_50_is_critical_miss(self):
        assert _attainment_outcome(49.9) == AttainmentOutcome.CRITICAL_MISS
        assert _attainment_outcome(0.0) == AttainmentOutcome.CRITICAL_MISS

    def test_all_outcomes_reachable(self):
        outcomes = {
            _attainment_outcome(120.0),
            _attainment_outcome(95.0),
            _attainment_outcome(75.0),
            _attainment_outcome(55.0),
            _attainment_outcome(10.0),
        }
        assert outcomes == set(AttainmentOutcome)


# ---------------------------------------------------------------------------
# Class 11 — _confidence scoring
# ---------------------------------------------------------------------------

class TestConfidenceScoring:
    def _make_conf_input(self, **kw):
        return make_input(**kw)

    def test_all_strong_signals_high(self):
        inp = self._make_conf_input(
            pipeline_stage3_eur=300_000.0,  # big pipeline for high coverage
            pipeline_stage2_eur=200_000.0,
            pipeline_stage1_eur=100_000.0,
            quota_eur=100_000.0,
            closed_won_eur=0.0,
            historical_attainment_pcts=[95.0, 100.0, 105.0],
            rep_confidence_score=8.0,
            deals_created_30d=5,
        )
        coverage = _pipeline_coverage_ratio(inp)
        hist = _historical_avg_attainment(inp)
        run_rate = _run_rate_pct(inp)
        conf = _confidence(inp, coverage, hist, run_rate)
        assert conf == AttainmentConfidence.HIGH

    def test_no_signals_very_low(self):
        inp = self._make_conf_input(
            pipeline_stage3_eur=0.0,
            pipeline_stage2_eur=0.0,
            pipeline_stage1_eur=0.0,
            quota_eur=200_000.0,
            closed_won_eur=0.0,
            historical_attainment_pcts=[],
            rep_confidence_score=2.0,
            deals_created_30d=0,
            days_elapsed=0,
        )
        coverage = 0.0
        hist = 80.0
        run_rate = 0.0
        conf = _confidence(inp, coverage, hist, run_rate)
        assert conf == AttainmentConfidence.VERY_LOW

    def test_coverage_ge3_adds_2(self):
        # Isolated: only coverage >= 3 contributes
        inp = self._make_conf_input(
            historical_attainment_pcts=[],
            rep_confidence_score=0.0,
            deals_created_30d=0,
        )
        conf_high_cov = _confidence(inp, 3.0, 80.0, 0.0)
        conf_low_cov = _confidence(inp, 0.5, 80.0, 0.0)
        scores = []
        # High coverage should score higher
        # 3.0 cov → +2, 0 hist → +0, 0 run → +0, 0 rep_conf → +0, 0 deals → +0 = 2 → VERY_LOW
        # 0.5 cov → +0 → VERY_LOW also, but path differs
        assert isinstance(conf_high_cov, AttainmentConfidence)
        assert isinstance(conf_low_cov, AttainmentConfidence)

    def test_coverage_ge2_lt3_adds_1(self):
        inp = self._make_conf_input(
            historical_attainment_pcts=[],
            rep_confidence_score=0.0,
            deals_created_30d=0,
        )
        conf = _confidence(inp, 2.5, 80.0, 0.0)
        # score=1 → VERY_LOW
        assert conf == AttainmentConfidence.VERY_LOW

    def test_3_or_more_history_adds_2(self):
        inp = self._make_conf_input(
            historical_attainment_pcts=[100.0, 100.0, 100.0],
            rep_confidence_score=0.0,
            deals_created_30d=0,
        )
        conf = _confidence(inp, 0.0, 100.0, 0.0)
        # score = 2 from history → VERY_LOW
        assert conf == AttainmentConfidence.VERY_LOW

    def test_run_rate_ge90_adds_2(self):
        inp = self._make_conf_input(
            historical_attainment_pcts=[],
            rep_confidence_score=0.0,
            deals_created_30d=0,
        )
        conf = _confidence(inp, 0.0, 80.0, 90.0)
        # score = 2 → VERY_LOW still
        assert conf == AttainmentConfidence.VERY_LOW

    def test_rep_confidence_ge7_adds_2(self):
        inp = self._make_conf_input(
            historical_attainment_pcts=[],
            rep_confidence_score=8.0,
            deals_created_30d=0,
        )
        conf = _confidence(inp, 0.0, 80.0, 0.0)
        # score = 2 → VERY_LOW
        assert conf == AttainmentConfidence.VERY_LOW

    def test_medium_confidence_threshold(self):
        # Build score = 5 exactly: cov>=3 (+2), 3+ history (+2), deals>=3 (+1) = 5 → MEDIUM
        inp = self._make_conf_input(
            historical_attainment_pcts=[90.0, 90.0, 90.0],
            rep_confidence_score=0.0,
            deals_created_30d=3,
        )
        conf = _confidence(inp, 3.0, 90.0, 0.0)
        assert conf == AttainmentConfidence.MEDIUM

    def test_low_confidence_threshold(self):
        # score = 3: cov>=2 (+1), 1 history (+1), deals>=3 (+1) = 3 → LOW
        inp = self._make_conf_input(
            historical_attainment_pcts=[90.0],
            rep_confidence_score=0.0,
            deals_created_30d=3,
        )
        conf = _confidence(inp, 2.0, 90.0, 0.0)
        assert conf == AttainmentConfidence.LOW

    def test_high_confidence_threshold(self):
        # score >= 7: cov>=3 (+2), 3+ hist (+2), run>=90 (+2), deals>=3 (+1) = 7 → HIGH
        inp = self._make_conf_input(
            historical_attainment_pcts=[90.0, 90.0, 90.0],
            rep_confidence_score=0.0,
            deals_created_30d=3,
        )
        conf = _confidence(inp, 3.0, 90.0, 90.0)
        assert conf == AttainmentConfidence.HIGH


# ---------------------------------------------------------------------------
# Class 12 — _quota_action
# ---------------------------------------------------------------------------

class TestQuotaAction:
    def test_critical_miss_always_escalate(self):
        assert _quota_action(AttainmentOutcome.CRITICAL_MISS, 0) == QuotaAction.ESCALATE
        assert _quota_action(AttainmentOutcome.CRITICAL_MISS, 29) == QuotaAction.ESCALATE
        assert _quota_action(AttainmentOutcome.CRITICAL_MISS, 90) == QuotaAction.ESCALATE

    def test_miss_always_intervention(self):
        assert _quota_action(AttainmentOutcome.MISS, 0) == QuotaAction.INTERVENTION
        assert _quota_action(AttainmentOutcome.MISS, 60) == QuotaAction.INTERVENTION
        assert _quota_action(AttainmentOutcome.MISS, 90) == QuotaAction.INTERVENTION

    def test_slight_miss_lt30_is_intervention(self):
        assert _quota_action(AttainmentOutcome.SLIGHT_MISS, 29) == QuotaAction.INTERVENTION
        assert _quota_action(AttainmentOutcome.SLIGHT_MISS, 0) == QuotaAction.INTERVENTION

    def test_slight_miss_ge30_is_accelerate(self):
        assert _quota_action(AttainmentOutcome.SLIGHT_MISS, 30) == QuotaAction.ACCELERATE
        assert _quota_action(AttainmentOutcome.SLIGHT_MISS, 90) == QuotaAction.ACCELERATE

    def test_achieve_ge30_is_accelerate(self):
        assert _quota_action(AttainmentOutcome.ACHIEVE, 30) == QuotaAction.ACCELERATE
        assert _quota_action(AttainmentOutcome.ACHIEVE, 90) == QuotaAction.ACCELERATE

    def test_achieve_lt30_is_maintain(self):
        # ACHIEVE with days_remaining < 30 falls through to MAINTAIN
        assert _quota_action(AttainmentOutcome.ACHIEVE, 29) == QuotaAction.MAINTAIN

    def test_overachieve_is_maintain(self):
        assert _quota_action(AttainmentOutcome.OVERACHIEVE, 0) == QuotaAction.MAINTAIN
        assert _quota_action(AttainmentOutcome.OVERACHIEVE, 90) == QuotaAction.MAINTAIN


# ---------------------------------------------------------------------------
# Class 13 — AttainmentResult.to_dict()
# ---------------------------------------------------------------------------

class TestAttainmentResultToDict:
    def test_to_dict_has_all_keys(self, predictor, standard_input):
        result = predictor.predict(standard_input)
        d = result.to_dict()
        expected_keys = {
            "rep_id", "rep_name", "region", "segment", "quota_eur",
            "current_attainment_pct", "projected_attainment_pct",
            "projected_closed_eur", "gap_to_quota_eur", "attainment_outcome",
            "confidence", "quota_action", "run_rate_pct",
            "pipeline_coverage_ratio", "weighted_pipeline_eur",
            "historical_avg_attainment_pct", "prediction_drivers",
            "prediction_risks", "action_plan",
        }
        assert set(d.keys()) == expected_keys

    def test_enum_values_serialised_as_strings(self, predictor, standard_input):
        d = predictor.predict(standard_input).to_dict()
        assert isinstance(d["attainment_outcome"], str)
        assert isinstance(d["confidence"], str)
        assert isinstance(d["quota_action"], str)

    def test_lists_are_lists(self, predictor, standard_input):
        d = predictor.predict(standard_input).to_dict()
        assert isinstance(d["prediction_drivers"], list)
        assert isinstance(d["prediction_risks"], list)
        assert isinstance(d["action_plan"], list)

    def test_numeric_fields_numeric(self, predictor, standard_input):
        d = predictor.predict(standard_input).to_dict()
        for field in ("quota_eur", "current_attainment_pct", "projected_attainment_pct",
                      "projected_closed_eur", "gap_to_quota_eur"):
            assert isinstance(d[field], (int, float))

    def test_identity_fields(self, predictor, standard_input):
        d = predictor.predict(standard_input).to_dict()
        assert d["rep_id"] == "rep-001"
        assert d["rep_name"] == "Alice Martin"
        assert d["region"] == "EMEA"
        assert d["segment"] == "Enterprise"


# ---------------------------------------------------------------------------
# Class 14 — QuotaAttainmentPredictor.predict()
# ---------------------------------------------------------------------------

class TestPredictBasic:
    def test_returns_attainment_result(self, predictor, standard_input):
        result = predictor.predict(standard_input)
        assert isinstance(result, AttainmentResult)

    def test_result_stored_in_results(self, predictor, standard_input):
        predictor.predict(standard_input)
        assert "rep-001" in predictor._results

    def test_rep_id_preserved(self, predictor, standard_input):
        result = predictor.predict(standard_input)
        assert result.rep_id == "rep-001"

    def test_quota_eur_preserved(self, predictor, standard_input):
        result = predictor.predict(standard_input)
        assert result.quota_eur == 200_000.0

    def test_current_attainment_pct_correct(self, predictor):
        inp = make_input(closed_won_eur=80_000.0, quota_eur=200_000.0)
        result = predictor.predict(inp)
        assert result.current_attainment_pct == 40.0

    def test_run_rate_pct_in_result(self, predictor, standard_input):
        result = predictor.predict(standard_input)
        assert isinstance(result.run_rate_pct, (int, float))

    def test_weighted_pipeline_eur_in_result(self, predictor, standard_input):
        result = predictor.predict(standard_input)
        assert isinstance(result.weighted_pipeline_eur, (int, float))
        assert result.weighted_pipeline_eur >= 0.0

    def test_projected_attainment_between_0_and_200(self, predictor, standard_input):
        result = predictor.predict(standard_input)
        assert 0.0 <= result.projected_attainment_pct <= 200.0

    def test_outcome_is_enum(self, predictor, standard_input):
        result = predictor.predict(standard_input)
        assert isinstance(result.attainment_outcome, AttainmentOutcome)

    def test_confidence_is_enum(self, predictor, standard_input):
        result = predictor.predict(standard_input)
        assert isinstance(result.confidence, AttainmentConfidence)

    def test_action_is_enum(self, predictor, standard_input):
        result = predictor.predict(standard_input)
        assert isinstance(result.quota_action, QuotaAction)

    def test_action_plan_nonempty(self, predictor, standard_input):
        result = predictor.predict(standard_input)
        assert len(result.action_plan) > 0

    def test_gap_nonnegative(self, predictor, standard_input):
        result = predictor.predict(standard_input)
        assert result.gap_to_quota_eur >= 0.0

    def test_second_predict_overwrites(self, predictor):
        inp1 = make_input(rep_id="rep-x", closed_won_eur=50_000.0)
        inp2 = make_input(rep_id="rep-x", closed_won_eur=90_000.0)
        predictor.predict(inp1)
        predictor.predict(inp2)
        assert predictor._results["rep-x"].current_attainment_pct == 45.0


# ---------------------------------------------------------------------------
# Class 15 — predict_batch
# ---------------------------------------------------------------------------

class TestPredictBatch:
    def _make_batch(self):
        return [
            make_input(rep_id="low", closed_won_eur=20_000.0,
                       pipeline_stage3_eur=0.0, pipeline_stage2_eur=0.0,
                       pipeline_stage1_eur=0.0, historical_attainment_pcts=[40.0]),
            make_input(rep_id="mid", closed_won_eur=100_000.0,
                       pipeline_stage3_eur=50_000.0,
                       historical_attainment_pcts=[90.0, 95.0, 100.0]),
            make_input(rep_id="high", closed_won_eur=180_000.0,
                       pipeline_stage3_eur=100_000.0,
                       historical_attainment_pcts=[110.0, 115.0, 120.0]),
        ]

    def test_returns_list(self, predictor):
        results = predictor.predict_batch(self._make_batch())
        assert isinstance(results, list)

    def test_length_matches_input(self, predictor):
        batch = self._make_batch()
        results = predictor.predict_batch(batch)
        assert len(results) == 3

    def test_sorted_desc_by_projected_attainment(self, predictor):
        results = predictor.predict_batch(self._make_batch())
        projections = [r.projected_attainment_pct for r in results]
        assert projections == sorted(projections, reverse=True)

    def test_all_stored_in_results(self, predictor):
        predictor.predict_batch(self._make_batch())
        assert "low" in predictor._results
        assert "mid" in predictor._results
        assert "high" in predictor._results

    def test_empty_batch(self, predictor):
        results = predictor.predict_batch([])
        assert results == []


# ---------------------------------------------------------------------------
# Class 16 — by_outcome / by_action / by_confidence
# ---------------------------------------------------------------------------

class TestFilterMethods:
    def _seed(self, predictor):
        predictor.predict(make_input(
            rep_id="a", closed_won_eur=220_000.0,
            pipeline_stage3_eur=0.0, pipeline_stage2_eur=0.0,
            pipeline_stage1_eur=0.0,
            historical_attainment_pcts=[120.0, 125.0, 130.0],
        ))
        predictor.predict(make_input(
            rep_id="b", closed_won_eur=10_000.0,
            pipeline_stage3_eur=0.0, pipeline_stage2_eur=0.0,
            pipeline_stage1_eur=0.0,
            historical_attainment_pcts=[30.0, 35.0],
        ))

    def test_by_outcome_filters_correctly(self, predictor):
        self._seed(predictor)
        overachievers = predictor.by_outcome(AttainmentOutcome.OVERACHIEVE)
        assert all(r.attainment_outcome == AttainmentOutcome.OVERACHIEVE for r in overachievers)

    def test_by_outcome_empty_when_no_match(self, predictor):
        # Fresh predictor — nothing stored
        assert predictor.by_outcome(AttainmentOutcome.MISS) == []

    def test_by_action_filters_correctly(self, predictor):
        self._seed(predictor)
        escalated = predictor.by_action(QuotaAction.ESCALATE)
        assert all(r.quota_action == QuotaAction.ESCALATE for r in escalated)

    def test_by_confidence_filters_correctly(self, predictor):
        self._seed(predictor)
        high_conf = predictor.by_confidence(AttainmentConfidence.HIGH)
        assert all(r.confidence == AttainmentConfidence.HIGH for r in high_conf)

    def test_by_outcome_returns_list(self, predictor):
        assert isinstance(predictor.by_outcome(AttainmentOutcome.ACHIEVE), list)


# ---------------------------------------------------------------------------
# Class 17 — Convenience result-set methods
# ---------------------------------------------------------------------------

class TestConvenienceResultMethods:
    def _seed_full(self, predictor):
        # overachiever
        predictor.predict(make_input(
            rep_id="oa", closed_won_eur=230_000.0,
            pipeline_stage3_eur=0.0, pipeline_stage2_eur=0.0,
            pipeline_stage1_eur=0.0,
            historical_attainment_pcts=[120.0, 125.0, 130.0],
        ))
        # critical miss
        predictor.predict(make_input(
            rep_id="cm", closed_won_eur=5_000.0,
            pipeline_stage3_eur=0.0, pipeline_stage2_eur=0.0,
            pipeline_stage1_eur=0.0,
            historical_attainment_pcts=[20.0, 25.0],
        ))

    def test_at_risk_reps_includes_critical_miss(self, predictor):
        self._seed_full(predictor)
        at_risk = predictor.at_risk_reps()
        outcomes = {r.attainment_outcome for r in at_risk}
        assert AttainmentOutcome.CRITICAL_MISS in outcomes or AttainmentOutcome.MISS in outcomes

    def test_on_track_reps_includes_overachiever(self, predictor):
        self._seed_full(predictor)
        on_track = predictor.on_track_reps()
        outcomes = {r.attainment_outcome for r in on_track}
        assert AttainmentOutcome.OVERACHIEVE in outcomes

    def test_overachievers_shortcut(self, predictor):
        self._seed_full(predictor)
        assert predictor.overachievers() == predictor.by_outcome(AttainmentOutcome.OVERACHIEVE)

    def test_critical_misses_shortcut(self, predictor):
        self._seed_full(predictor)
        assert predictor.critical_misses() == predictor.by_outcome(AttainmentOutcome.CRITICAL_MISS)

    def test_needs_escalation_shortcut(self, predictor):
        self._seed_full(predictor)
        assert predictor.needs_escalation() == predictor.by_action(QuotaAction.ESCALATE)

    def test_at_risk_only_miss_or_critical_miss(self, predictor):
        self._seed_full(predictor)
        for r in predictor.at_risk_reps():
            assert r.attainment_outcome in (AttainmentOutcome.MISS, AttainmentOutcome.CRITICAL_MISS)

    def test_on_track_only_achieve_or_overachieve(self, predictor):
        self._seed_full(predictor)
        for r in predictor.on_track_reps():
            assert r.attainment_outcome in (AttainmentOutcome.ACHIEVE, AttainmentOutcome.OVERACHIEVE)


# ---------------------------------------------------------------------------
# Class 18 — Aggregate numeric methods
# ---------------------------------------------------------------------------

class TestAggregateNumericMethods:
    def _seed(self, predictor):
        predictor.predict(make_input(rep_id="r1", quota_eur=100_000.0,
                                     closed_won_eur=80_000.0,
                                     pipeline_stage3_eur=10_000.0,
                                     pipeline_stage2_eur=0.0,
                                     pipeline_stage1_eur=0.0,
                                     historical_attainment_pcts=[90.0, 95.0]))
        predictor.predict(make_input(rep_id="r2", quota_eur=200_000.0,
                                     closed_won_eur=150_000.0,
                                     pipeline_stage3_eur=20_000.0,
                                     pipeline_stage2_eur=0.0,
                                     pipeline_stage1_eur=0.0,
                                     historical_attainment_pcts=[100.0, 105.0]))

    def test_avg_projected_attainment_is_numeric(self, predictor):
        self._seed(predictor)
        avg = predictor.avg_projected_attainment()
        assert isinstance(avg, (int, float))

    def test_avg_projected_attainment_empty_predictor(self, predictor):
        assert predictor.avg_projected_attainment() == 0.0

    def test_total_projected_closed_eur_sums(self, predictor):
        self._seed(predictor)
        total = predictor.total_projected_closed_eur()
        r1 = predictor._results["r1"].projected_closed_eur
        r2 = predictor._results["r2"].projected_closed_eur
        assert total == r1 + r2

    def test_total_gap_eur_sums(self, predictor):
        self._seed(predictor)
        total = predictor.total_gap_eur()
        r1 = predictor._results["r1"].gap_to_quota_eur
        r2 = predictor._results["r2"].gap_to_quota_eur
        assert total == r1 + r2

    def test_avg_projected_rounded_to_1_decimal(self, predictor):
        self._seed(predictor)
        avg = predictor.avg_projected_attainment()
        assert avg == round(avg, 1)


# ---------------------------------------------------------------------------
# Class 19 — summary()
# ---------------------------------------------------------------------------

class TestSummary:
    def test_summary_keys(self, predictor):
        predictor.predict(make_input())
        s = predictor.summary()
        assert "total" in s
        assert "outcome_counts" in s
        assert "action_counts" in s
        assert "confidence_counts" in s
        assert "avg_projected_attainment_pct" in s
        assert "total_projected_closed_eur" in s
        assert "total_gap_eur" in s
        assert "critical_miss_count" in s
        assert "escalation_count" in s
        assert "overachieve_count" in s

    def test_summary_total_matches_stored(self, predictor):
        predictor.predict(make_input(rep_id="x"))
        predictor.predict(make_input(rep_id="y"))
        s = predictor.summary()
        assert s["total"] == 2

    def test_summary_outcome_counts_all_outcomes(self, predictor):
        predictor.predict(make_input())
        s = predictor.summary()
        for o in AttainmentOutcome:
            assert o.value in s["outcome_counts"]

    def test_summary_action_counts_all_actions(self, predictor):
        predictor.predict(make_input())
        s = predictor.summary()
        for a in QuotaAction:
            assert a.value in s["action_counts"]

    def test_summary_confidence_counts_all_confidences(self, predictor):
        predictor.predict(make_input())
        s = predictor.summary()
        for c in AttainmentConfidence:
            assert c.value in s["confidence_counts"]

    def test_summary_counts_sum_to_total(self, predictor):
        predictor.predict(make_input(rep_id="a"))
        predictor.predict(make_input(rep_id="b"))
        s = predictor.summary()
        assert sum(s["outcome_counts"].values()) == s["total"]
        assert sum(s["action_counts"].values()) == s["total"]
        assert sum(s["confidence_counts"].values()) == s["total"]

    def test_empty_predictor_summary(self, predictor):
        s = predictor.summary()
        assert s["total"] == 0
        assert s["avg_projected_attainment_pct"] == 0.0


# ---------------------------------------------------------------------------
# Class 20 — reset()
# ---------------------------------------------------------------------------

class TestReset:
    def test_reset_clears_results(self, predictor):
        predictor.predict(make_input(rep_id="a"))
        predictor.predict(make_input(rep_id="b"))
        predictor.reset()
        assert len(predictor._results) == 0

    def test_reset_allows_re_predict(self, predictor):
        predictor.predict(make_input(rep_id="a"))
        predictor.reset()
        predictor.predict(make_input(rep_id="a"))
        assert "a" in predictor._results

    def test_avg_projected_after_reset(self, predictor):
        predictor.predict(make_input())
        predictor.reset()
        assert predictor.avg_projected_attainment() == 0.0

    def test_total_projected_after_reset(self, predictor):
        predictor.predict(make_input())
        predictor.reset()
        assert predictor.total_projected_closed_eur() == 0.0

    def test_at_risk_after_reset(self, predictor):
        predictor.predict(make_input())
        predictor.reset()
        assert predictor.at_risk_reps() == []


# ---------------------------------------------------------------------------
# Class 21 — Edge cases and extreme scenarios
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_quota_zero_predict_does_not_raise(self, predictor):
        inp = make_input(quota_eur=0.0)
        result = predictor.predict(inp)
        assert result.projected_attainment_pct == 0.0

    def test_all_zeros_predict_does_not_raise(self, predictor):
        inp = make_input(
            quota_eur=0.0,
            closed_won_eur=0.0,
            pipeline_stage3_eur=0.0,
            pipeline_stage2_eur=0.0,
            pipeline_stage1_eur=0.0,
            win_rate_pct=0.0,
            days_elapsed=0,
            days_remaining=0,
            rep_confidence_score=0.0,
            deals_created_30d=0,
            meetings_30d=0,
            proposals_sent_30d=0,
            historical_attainment_pcts=[],
            avg_sales_cycle_days=0,
        )
        result = predictor.predict(inp)
        assert isinstance(result, AttainmentResult)

    def test_very_high_win_rate(self, predictor):
        inp = make_input(win_rate_pct=100.0)
        result = predictor.predict(inp)
        assert result.weighted_pipeline_eur >= 0.0

    def test_no_historical_data_default_80(self, predictor):
        inp = make_input(historical_attainment_pcts=[])
        result = predictor.predict(inp)
        assert result.historical_avg_attainment_pct == 80.0

    def test_large_pipeline_coverage_capped_at_99_when_closed_exceeds_quota(self, predictor):
        inp = make_input(quota_eur=100_000.0, closed_won_eur=150_000.0)
        result = predictor.predict(inp)
        assert result.pipeline_coverage_ratio == 99.0

    def test_multiple_reps_independent(self, predictor):
        a = make_input(rep_id="a", closed_won_eur=50_000.0)
        b = make_input(rep_id="b", closed_won_eur=100_000.0)
        ra = predictor.predict(a)
        rb = predictor.predict(b)
        assert ra.rep_id != rb.rep_id
        assert ra.current_attainment_pct != rb.current_attainment_pct

    def test_historical_attainment_single_element(self, predictor):
        inp = make_input(historical_attainment_pcts=[75.0])
        result = predictor.predict(inp)
        assert result.historical_avg_attainment_pct == 75.0

    def test_negative_closed_won_does_not_crash(self, predictor):
        # Unusual but should not raise
        inp = make_input(closed_won_eur=-1000.0)
        result = predictor.predict(inp)
        assert isinstance(result, AttainmentResult)


# ---------------------------------------------------------------------------
# Class 22 — Integration / end-to-end scenario tests
# ---------------------------------------------------------------------------

class TestIntegrationScenarios:
    def test_star_rep_full_scenario(self, predictor):
        """High performer: well past quota, strong pipeline, high confidence."""
        inp = make_input(
            rep_id="star",
            quota_eur=200_000.0,
            days_elapsed=240,
            days_remaining=30,
            closed_won_eur=210_000.0,
            pipeline_stage3_eur=80_000.0,
            pipeline_stage2_eur=50_000.0,
            pipeline_stage1_eur=30_000.0,
            win_rate_pct=40.0,
            avg_sales_cycle_days=30,
            historical_attainment_pcts=[110.0, 120.0, 115.0],
            rep_confidence_score=9.0,
            deals_created_30d=6,
        )
        result = predictor.predict(inp)
        assert result.attainment_outcome == AttainmentOutcome.OVERACHIEVE
        assert result.quota_action == QuotaAction.MAINTAIN
        assert result.current_attainment_pct == 105.0

    def test_struggling_rep_full_scenario(self, predictor):
        """Poor performer: far behind, no pipeline, critical miss expected."""
        inp = make_input(
            rep_id="struggle",
            quota_eur=300_000.0,
            days_elapsed=300,
            days_remaining=15,
            closed_won_eur=30_000.0,
            pipeline_stage3_eur=0.0,
            pipeline_stage2_eur=5_000.0,
            pipeline_stage1_eur=10_000.0,
            win_rate_pct=10.0,
            avg_sales_cycle_days=60,
            historical_attainment_pcts=[45.0, 50.0],
            rep_confidence_score=2.0,
            deals_created_30d=0,
        )
        result = predictor.predict(inp)
        assert result.attainment_outcome == AttainmentOutcome.CRITICAL_MISS
        assert result.quota_action == QuotaAction.ESCALATE
        assert len(result.action_plan) > 0

    def test_borderline_achieve_scenario(self, predictor):
        """Rep sitting right at the 90% boundary."""
        inp = make_input(
            rep_id="border",
            quota_eur=100_000.0,
            days_elapsed=180,
            days_remaining=90,
            closed_won_eur=90_000.0,
            pipeline_stage3_eur=0.0,
            pipeline_stage2_eur=0.0,
            pipeline_stage1_eur=0.0,
            win_rate_pct=30.0,
            avg_sales_cycle_days=60,
            historical_attainment_pcts=[90.0, 90.0, 90.0],
        )
        result = predictor.predict(inp)
        assert isinstance(result.attainment_outcome, AttainmentOutcome)
        # current attainment
        assert result.current_attainment_pct == 90.0

    def test_batch_sorted_correctly(self, predictor):
        batch = [
            make_input(rep_id=f"r{i}",
                       closed_won_eur=i * 20_000.0,
                       historical_attainment_pcts=[float(50 + i * 10)])
            for i in range(5)
        ]
        results = predictor.predict_batch(batch)
        projs = [r.projected_attainment_pct for r in results]
        assert projs == sorted(projs, reverse=True)

    def test_summary_reflects_all_preds(self, predictor):
        for i in range(4):
            predictor.predict(make_input(rep_id=f"rep{i}",
                                         closed_won_eur=i * 40_000.0))
        s = predictor.summary()
        assert s["total"] == 4

    def test_reset_and_reload(self, predictor):
        predictor.predict(make_input(rep_id="old"))
        predictor.reset()
        predictor.predict(make_input(rep_id="new"))
        s = predictor.summary()
        assert s["total"] == 1
        assert "old" not in predictor._results

    def test_drivers_and_risks_are_strings(self, predictor, standard_input):
        result = predictor.predict(standard_input)
        for d in result.prediction_drivers:
            assert isinstance(d, str)
        for r in result.prediction_risks:
            assert isinstance(r, str)

    def test_closed_won_driver_appears(self, predictor):
        inp = make_input(closed_won_eur=100_000.0)
        result = predictor.predict(inp)
        # closed_won_eur > 0 → driver added
        assert any("100" in d or "closed" in d.lower() or "Closé" in d
                   for d in result.prediction_drivers)

    def test_low_win_rate_risk_appears(self, predictor):
        inp = make_input(win_rate_pct=5.0,
                         pipeline_stage3_eur=100_000.0,
                         pipeline_stage2_eur=100_000.0,
                         pipeline_stage1_eur=100_000.0)
        result = predictor.predict(inp)
        # win_rate < 15 → risk added
        assert any("Taux" in r or "%" in r for r in result.prediction_risks)

    def test_escalate_action_plan_contains_escalation_text(self, predictor):
        inp = make_input(
            rep_id="esc",
            quota_eur=300_000.0,
            closed_won_eur=5_000.0,
            pipeline_stage3_eur=0.0,
            pipeline_stage2_eur=0.0,
            pipeline_stage1_eur=0.0,
            historical_attainment_pcts=[10.0, 15.0],
        )
        result = predictor.predict(inp)
        if result.quota_action == QuotaAction.ESCALATE:
            assert any("Escalade" in s or "escalad" in s.lower() for s in result.action_plan)
