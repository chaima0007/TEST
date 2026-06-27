"""
Comprehensive pytest tests for swarm/intelligence/pipeline_gap_analyzer.py
Module 31 — Pipeline Gap Analyzer
"""
from __future__ import annotations

import pytest

from swarm.intelligence.pipeline_gap_analyzer import (
    GapSeverity,
    PipelineAction,
    QuotaRisk,
    CoverageHealth,
    PipelineInput,
    PipelineGapResult,
    PipelineGapAnalyzerEngine,
    _quota_remaining,
    _attainment_pct,
    _run_rate_pct,
    _expected_close_eur,
    _coverage_ratio,
    _coverage_health,
    _gap_eur,
    _gap_severity,
    _quota_risk,
    _pipeline_action,
    _pipeline_score,
    _gap_drivers,
    _gap_closers,
)


# ---------------------------------------------------------------------------
# Helpers / Fixtures
# ---------------------------------------------------------------------------

def make_input(
    rep_id: str = "R001",
    rep_name: str = "Alice Dupont",
    region: str = "EMEA",
    segment: str = "Mid-Market",
    quota_eur: float = 100_000.0,
    closed_won_eur: float = 30_000.0,
    days_elapsed: int = 45,
    days_remaining: int = 45,
    pipeline_total_eur: float = 200_000.0,
    stage_1_eur: float = 50_000.0,
    stage_2_eur: float = 80_000.0,
    stage_3_eur: float = 70_000.0,
    avg_deal_size_eur: float = 10_000.0,
    avg_sales_cycle_days: int = 60,
    win_rate_pct: float = 25.0,
    new_opps_created_30d: int = 5,
    demos_completed_30d: int = 4,
    proposals_sent_30d: int = 3,
    follow_up_rate_pct: float = 80.0,
) -> PipelineInput:
    return PipelineInput(
        rep_id=rep_id,
        rep_name=rep_name,
        region=region,
        segment=segment,
        quota_eur=quota_eur,
        closed_won_eur=closed_won_eur,
        days_elapsed=days_elapsed,
        days_remaining=days_remaining,
        pipeline_total_eur=pipeline_total_eur,
        stage_1_eur=stage_1_eur,
        stage_2_eur=stage_2_eur,
        stage_3_eur=stage_3_eur,
        avg_deal_size_eur=avg_deal_size_eur,
        avg_sales_cycle_days=avg_sales_cycle_days,
        win_rate_pct=win_rate_pct,
        new_opps_created_30d=new_opps_created_30d,
        demos_completed_30d=demos_completed_30d,
        proposals_sent_30d=proposals_sent_30d,
        follow_up_rate_pct=follow_up_rate_pct,
    )


@pytest.fixture()
def default_input() -> PipelineInput:
    return make_input()


@pytest.fixture()
def engine() -> PipelineGapAnalyzerEngine:
    return PipelineGapAnalyzerEngine()


# ---------------------------------------------------------------------------
# Class 1: Enum Values
# ---------------------------------------------------------------------------

class TestEnumValues:
    def test_gap_severity_values(self):
        assert GapSeverity.NONE.value == "none"
        assert GapSeverity.MINOR.value == "minor"
        assert GapSeverity.MODERATE.value == "moderate"
        assert GapSeverity.SEVERE.value == "severe"
        assert GapSeverity.CRITICAL.value == "critical"

    def test_pipeline_action_values(self):
        assert PipelineAction.MAINTAIN.value == "maintain"
        assert PipelineAction.BUILD.value == "build"
        assert PipelineAction.ACCELERATE.value == "accelerate"
        assert PipelineAction.EMERGENCY.value == "emergency"

    def test_quota_risk_values(self):
        assert QuotaRisk.ON_TRACK.value == "on_track"
        assert QuotaRisk.AT_RISK.value == "at_risk"
        assert QuotaRisk.BEHIND.value == "behind"
        assert QuotaRisk.CRITICAL.value == "critical"

    def test_coverage_health_values(self):
        assert CoverageHealth.HEALTHY.value == "healthy"
        assert CoverageHealth.ADEQUATE.value == "adequate"
        assert CoverageHealth.THIN.value == "thin"
        assert CoverageHealth.INSUFFICIENT.value == "insufficient"

    def test_enum_membership(self):
        assert len(list(GapSeverity)) == 5
        assert len(list(PipelineAction)) == 4
        assert len(list(QuotaRisk)) == 4
        assert len(list(CoverageHealth)) == 4

    def test_enums_are_str(self):
        # All enums inherit from str
        assert isinstance(GapSeverity.NONE, str)
        assert isinstance(PipelineAction.MAINTAIN, str)
        assert isinstance(QuotaRisk.ON_TRACK, str)
        assert isinstance(CoverageHealth.HEALTHY, str)


# ---------------------------------------------------------------------------
# Class 2: PipelineInput Dataclass
# ---------------------------------------------------------------------------

class TestPipelineInputDataclass:
    def test_instantiation(self, default_input):
        assert default_input.rep_id == "R001"
        assert default_input.rep_name == "Alice Dupont"
        assert default_input.region == "EMEA"
        assert default_input.segment == "Mid-Market"
        assert default_input.quota_eur == 100_000.0
        assert default_input.closed_won_eur == 30_000.0
        assert default_input.days_elapsed == 45
        assert default_input.days_remaining == 45
        assert default_input.pipeline_total_eur == 200_000.0
        assert default_input.stage_1_eur == 50_000.0
        assert default_input.stage_2_eur == 80_000.0
        assert default_input.stage_3_eur == 70_000.0
        assert default_input.avg_deal_size_eur == 10_000.0
        assert default_input.avg_sales_cycle_days == 60
        assert default_input.win_rate_pct == 25.0
        assert default_input.new_opps_created_30d == 5
        assert default_input.demos_completed_30d == 4
        assert default_input.proposals_sent_30d == 3
        assert default_input.follow_up_rate_pct == 80.0

    def test_field_count(self, default_input):
        # 19 fields defined in the spec
        from dataclasses import fields
        assert len(fields(default_input)) == 19

    def test_mutable_fields(self, default_input):
        default_input.closed_won_eur = 99_999.0
        assert default_input.closed_won_eur == 99_999.0


# ---------------------------------------------------------------------------
# Class 3: _quota_remaining
# ---------------------------------------------------------------------------

class TestQuotaRemaining:
    def test_normal_case(self):
        inp = make_input(quota_eur=100_000, closed_won_eur=30_000)
        assert _quota_remaining(inp) == 70_000.0

    def test_fully_attained(self):
        inp = make_input(quota_eur=100_000, closed_won_eur=100_000)
        assert _quota_remaining(inp) == 0.0

    def test_over_attainment_clamps_to_zero(self):
        inp = make_input(quota_eur=100_000, closed_won_eur=120_000)
        assert _quota_remaining(inp) == 0.0

    def test_zero_closed(self):
        inp = make_input(quota_eur=50_000, closed_won_eur=0)
        assert _quota_remaining(inp) == 50_000.0

    def test_zero_quota(self):
        inp = make_input(quota_eur=0, closed_won_eur=0)
        assert _quota_remaining(inp) == 0.0


# ---------------------------------------------------------------------------
# Class 4: _attainment_pct
# ---------------------------------------------------------------------------

class TestAttainmentPct:
    def test_normal_attainment(self):
        inp = make_input(quota_eur=100_000, closed_won_eur=30_000)
        assert _attainment_pct(inp) == 30.0

    def test_full_attainment(self):
        inp = make_input(quota_eur=100_000, closed_won_eur=100_000)
        assert _attainment_pct(inp) == 100.0

    def test_over_attainment(self):
        inp = make_input(quota_eur=100_000, closed_won_eur=150_000)
        assert _attainment_pct(inp) == 150.0

    def test_zero_quota_returns_zero(self):
        inp = make_input(quota_eur=0, closed_won_eur=50_000)
        assert _attainment_pct(inp) == 0.0

    def test_rounding(self):
        # 1/3 * 100 ≈ 33.3
        inp = make_input(quota_eur=3, closed_won_eur=1)
        result = _attainment_pct(inp)
        assert round(result, 1) == 33.3


# ---------------------------------------------------------------------------
# Class 5: _run_rate_pct
# ---------------------------------------------------------------------------

class TestRunRatePct:
    def test_on_pace(self):
        # 50% time elapsed, 50% quota closed → run rate = 100%
        inp = make_input(quota_eur=100_000, closed_won_eur=50_000,
                         days_elapsed=45, days_remaining=45)
        assert _run_rate_pct(inp) == 100.0

    def test_ahead_of_pace(self):
        inp = make_input(quota_eur=100_000, closed_won_eur=80_000,
                         days_elapsed=50, days_remaining=50)
        assert _run_rate_pct(inp) == 160.0

    def test_behind_pace(self):
        inp = make_input(quota_eur=100_000, closed_won_eur=10_000,
                         days_elapsed=50, days_remaining=50)
        assert _run_rate_pct(inp) == 20.0

    def test_zero_days_total(self):
        inp = make_input(days_elapsed=0, days_remaining=0)
        assert _run_rate_pct(inp) == 0.0

    def test_zero_quota(self):
        inp = make_input(quota_eur=0)
        assert _run_rate_pct(inp) == 0.0

    def test_zero_days_elapsed(self):
        # expected_at_pace = 0, so returns 0
        inp = make_input(days_elapsed=0, days_remaining=90)
        assert _run_rate_pct(inp) == 0.0

    def test_rounding_to_one_decimal(self):
        inp = make_input(quota_eur=300, closed_won_eur=100,
                         days_elapsed=100, days_remaining=200)
        # expected_at_pace = 300 * (100/300) = 100; run_rate = 100/100*100 = 100
        assert isinstance(_run_rate_pct(inp), float)


# ---------------------------------------------------------------------------
# Class 6: _expected_close_eur
# ---------------------------------------------------------------------------

class TestExpectedCloseEur:
    def test_basic_calculation(self):
        inp = make_input(win_rate_pct=20.0,
                         stage_3_eur=10_000, stage_2_eur=20_000, stage_1_eur=30_000)
        wr = 0.20
        expected = round(10_000 * wr + 20_000 * wr * 0.6 + 30_000 * wr * 0.3, 0)
        assert _expected_close_eur(inp) == expected

    def test_zero_win_rate(self):
        inp = make_input(win_rate_pct=0.0)
        assert _expected_close_eur(inp) == 0.0

    def test_100_win_rate(self):
        inp = make_input(win_rate_pct=100.0,
                         stage_3_eur=10_000, stage_2_eur=10_000, stage_1_eur=10_000)
        expected = round(10_000 * 1.0 + 10_000 * 1.0 * 0.6 + 10_000 * 1.0 * 0.3, 0)
        assert _expected_close_eur(inp) == expected

    def test_only_stage_3(self):
        inp = make_input(win_rate_pct=50.0, stage_3_eur=10_000,
                         stage_2_eur=0, stage_1_eur=0)
        assert _expected_close_eur(inp) == 5_000.0

    def test_stage_weights(self):
        # Stage 3 > stage 2 > stage 1 in terms of expected value per euro
        inp = make_input(win_rate_pct=50.0,
                         stage_3_eur=1, stage_2_eur=1, stage_1_eur=1)
        # 0.5*1 + 0.5*0.6*1 + 0.5*0.3*1 = 0.5 + 0.3 + 0.15 = 0.95
        assert _expected_close_eur(inp) == round(0.95, 0)


# ---------------------------------------------------------------------------
# Class 7: _coverage_ratio
# ---------------------------------------------------------------------------

class TestCoverageRatio:
    def test_normal_ratio(self):
        inp = make_input(quota_eur=100_000, closed_won_eur=30_000,
                         pipeline_total_eur=280_000)
        # remaining = 70_000, ratio = 280_000/70_000 = 4.0
        assert _coverage_ratio(inp) == 4.0

    def test_zero_remaining_returns_99(self):
        inp = make_input(quota_eur=100_000, closed_won_eur=100_000,
                         pipeline_total_eur=50_000)
        assert _coverage_ratio(inp) == 99.0

    def test_over_attained_returns_99(self):
        inp = make_input(quota_eur=100_000, closed_won_eur=150_000)
        assert _coverage_ratio(inp) == 99.0

    def test_ratio_rounding(self):
        inp = make_input(quota_eur=100_000, closed_won_eur=40_000,
                         pipeline_total_eur=100_000)
        # remaining = 60_000, ratio = 100_000/60_000 = 1.67
        result = _coverage_ratio(inp)
        assert result == round(100_000 / 60_000, 2)

    def test_thin_ratio(self):
        inp = make_input(quota_eur=100_000, closed_won_eur=0,
                         pipeline_total_eur=150_000)
        assert _coverage_ratio(inp) == 1.5


# ---------------------------------------------------------------------------
# Class 8: _coverage_health
# ---------------------------------------------------------------------------

class TestCoverageHealth:
    def test_healthy_at_4(self):
        assert _coverage_health(4.0) == CoverageHealth.HEALTHY

    def test_healthy_above_4(self):
        assert _coverage_health(5.5) == CoverageHealth.HEALTHY

    def test_adequate_at_3(self):
        assert _coverage_health(3.0) == CoverageHealth.ADEQUATE

    def test_adequate_between_3_and_4(self):
        assert _coverage_health(3.5) == CoverageHealth.ADEQUATE

    def test_thin_at_2(self):
        assert _coverage_health(2.0) == CoverageHealth.THIN

    def test_thin_between_2_and_3(self):
        assert _coverage_health(2.9) == CoverageHealth.THIN

    def test_insufficient_below_2(self):
        assert _coverage_health(1.9) == CoverageHealth.INSUFFICIENT

    def test_insufficient_at_zero(self):
        assert _coverage_health(0.0) == CoverageHealth.INSUFFICIENT

    def test_boundary_just_below_healthy(self):
        assert _coverage_health(3.99) == CoverageHealth.ADEQUATE

    def test_boundary_just_below_adequate(self):
        assert _coverage_health(2.99) == CoverageHealth.THIN

    def test_boundary_just_below_thin(self):
        assert _coverage_health(1.99) == CoverageHealth.INSUFFICIENT


# ---------------------------------------------------------------------------
# Class 9: _gap_eur
# ---------------------------------------------------------------------------

class TestGapEur:
    def test_positive_gap(self):
        inp = make_input(quota_eur=100_000, closed_won_eur=0)
        # remaining = 100_000; expected_close must be computed elsewhere
        gap = _gap_eur(inp, 40_000.0)
        assert gap == 60_000.0

    def test_no_gap_when_expected_exceeds_remaining(self):
        inp = make_input(quota_eur=100_000, closed_won_eur=40_000)
        # remaining = 60_000; expected = 80_000 → gap = 0
        gap = _gap_eur(inp, 80_000.0)
        assert gap == 0.0

    def test_exact_coverage(self):
        inp = make_input(quota_eur=100_000, closed_won_eur=20_000)
        gap = _gap_eur(inp, 80_000.0)
        assert gap == 0.0

    def test_fully_attained_no_gap(self):
        inp = make_input(quota_eur=100_000, closed_won_eur=100_000)
        gap = _gap_eur(inp, 0.0)
        assert gap == 0.0

    def test_gap_rounding(self):
        inp = make_input(quota_eur=100_000, closed_won_eur=0)
        # remaining=100_000; expected=33_333.33 → gap = 66_666.67 → rounded = 66667
        gap = _gap_eur(inp, 33_333.33)
        assert gap == round(max(0.0, 100_000 - 33_333.33), 0)


# ---------------------------------------------------------------------------
# Class 10: _gap_severity
# ---------------------------------------------------------------------------

class TestGapSeverity:
    def test_none_severity(self):
        # gap/quota < 5%
        assert _gap_severity(4_000, 100_000) == GapSeverity.NONE

    def test_minor_severity_at_5pct(self):
        assert _gap_severity(5_000, 100_000) == GapSeverity.MINOR

    def test_minor_severity(self):
        assert _gap_severity(10_000, 100_000) == GapSeverity.MINOR

    def test_moderate_severity_at_15pct(self):
        assert _gap_severity(15_000, 100_000) == GapSeverity.MODERATE

    def test_moderate_severity(self):
        assert _gap_severity(20_000, 100_000) == GapSeverity.MODERATE

    def test_severe_severity_at_25pct(self):
        assert _gap_severity(25_000, 100_000) == GapSeverity.SEVERE

    def test_severe_severity(self):
        assert _gap_severity(30_000, 100_000) == GapSeverity.SEVERE

    def test_critical_severity_at_40pct(self):
        assert _gap_severity(40_000, 100_000) == GapSeverity.CRITICAL

    def test_critical_severity(self):
        assert _gap_severity(60_000, 100_000) == GapSeverity.CRITICAL

    def test_zero_quota_returns_none(self):
        assert _gap_severity(50_000, 0) == GapSeverity.NONE

    def test_zero_gap_returns_none(self):
        assert _gap_severity(0, 100_000) == GapSeverity.NONE

    def test_boundary_just_below_critical(self):
        # 39.99% → SEVERE
        assert _gap_severity(39_990, 100_000) == GapSeverity.SEVERE

    def test_boundary_just_below_severe(self):
        # 24.99% → MODERATE
        assert _gap_severity(24_990, 100_000) == GapSeverity.MODERATE

    def test_boundary_just_below_moderate(self):
        # 14.99% → MINOR
        assert _gap_severity(14_990, 100_000) == GapSeverity.MINOR

    def test_boundary_just_below_minor(self):
        # 4.99% → NONE
        assert _gap_severity(4_990, 100_000) == GapSeverity.NONE


# ---------------------------------------------------------------------------
# Class 11: _quota_risk
# ---------------------------------------------------------------------------

class TestQuotaRisk:
    def test_critical_when_gap_severity_critical(self):
        result = _quota_risk(80.0, 90.0, GapSeverity.CRITICAL)
        assert result == QuotaRisk.CRITICAL

    def test_critical_when_low_run_rate_and_low_attainment(self):
        # run_rate < 60 and attainment < 40
        result = _quota_risk(35.0, 55.0, GapSeverity.NONE)
        assert result == QuotaRisk.CRITICAL

    def test_not_critical_when_only_low_run_rate(self):
        # run_rate < 60 but attainment >= 40
        result = _quota_risk(50.0, 55.0, GapSeverity.NONE)
        # Not CRITICAL, check further
        assert result != QuotaRisk.CRITICAL

    def test_not_critical_when_only_low_attainment(self):
        # run_rate >= 60 but attainment < 40
        result = _quota_risk(30.0, 70.0, GapSeverity.NONE)
        assert result != QuotaRisk.CRITICAL

    def test_behind_when_gap_severity_severe(self):
        result = _quota_risk(80.0, 90.0, GapSeverity.SEVERE)
        assert result == QuotaRisk.BEHIND

    def test_behind_when_run_rate_below_75(self):
        result = _quota_risk(60.0, 70.0, GapSeverity.NONE)
        assert result == QuotaRisk.BEHIND

    def test_at_risk_when_gap_severity_moderate(self):
        result = _quota_risk(80.0, 90.0, GapSeverity.MODERATE)
        assert result == QuotaRisk.AT_RISK

    def test_at_risk_when_gap_severity_minor(self):
        result = _quota_risk(80.0, 90.0, GapSeverity.MINOR)
        assert result == QuotaRisk.AT_RISK

    def test_at_risk_when_run_rate_below_90(self):
        result = _quota_risk(80.0, 85.0, GapSeverity.NONE)
        assert result == QuotaRisk.AT_RISK

    def test_on_track_when_all_good(self):
        result = _quota_risk(80.0, 95.0, GapSeverity.NONE)
        assert result == QuotaRisk.ON_TRACK

    def test_critical_gap_overrides_good_run_rate(self):
        result = _quota_risk(90.0, 120.0, GapSeverity.CRITICAL)
        assert result == QuotaRisk.CRITICAL

    def test_boundary_run_rate_75_is_behind(self):
        # run_rate < 75 → BEHIND; at exactly 75 → not BEHIND from run_rate alone
        result_below = _quota_risk(60.0, 74.9, GapSeverity.NONE)
        assert result_below == QuotaRisk.BEHIND
        result_at = _quota_risk(60.0, 75.0, GapSeverity.NONE)
        assert result_at != QuotaRisk.BEHIND


# ---------------------------------------------------------------------------
# Class 12: _pipeline_action
# ---------------------------------------------------------------------------

class TestPipelineAction:
    def test_emergency_when_critical_risk(self):
        assert _pipeline_action(QuotaRisk.CRITICAL, CoverageHealth.HEALTHY) == PipelineAction.EMERGENCY

    def test_emergency_when_insufficient_coverage(self):
        assert _pipeline_action(QuotaRisk.ON_TRACK, CoverageHealth.INSUFFICIENT) == PipelineAction.EMERGENCY

    def test_emergency_both_critical_and_insufficient(self):
        assert _pipeline_action(QuotaRisk.CRITICAL, CoverageHealth.INSUFFICIENT) == PipelineAction.EMERGENCY

    def test_build_when_behind(self):
        assert _pipeline_action(QuotaRisk.BEHIND, CoverageHealth.ADEQUATE) == PipelineAction.BUILD

    def test_build_when_thin_coverage(self):
        assert _pipeline_action(QuotaRisk.ON_TRACK, CoverageHealth.THIN) == PipelineAction.BUILD

    def test_accelerate_when_at_risk(self):
        assert _pipeline_action(QuotaRisk.AT_RISK, CoverageHealth.ADEQUATE) == PipelineAction.ACCELERATE

    def test_accelerate_when_at_risk_healthy_coverage(self):
        assert _pipeline_action(QuotaRisk.AT_RISK, CoverageHealth.HEALTHY) == PipelineAction.ACCELERATE

    def test_maintain_when_on_track_healthy(self):
        assert _pipeline_action(QuotaRisk.ON_TRACK, CoverageHealth.HEALTHY) == PipelineAction.MAINTAIN

    def test_maintain_when_on_track_adequate(self):
        assert _pipeline_action(QuotaRisk.ON_TRACK, CoverageHealth.ADEQUATE) == PipelineAction.MAINTAIN

    def test_critical_risk_beats_healthy_coverage(self):
        # CRITICAL risk → EMERGENCY even with HEALTHY coverage
        result = _pipeline_action(QuotaRisk.CRITICAL, CoverageHealth.HEALTHY)
        assert result == PipelineAction.EMERGENCY


# ---------------------------------------------------------------------------
# Class 13: _pipeline_score
# ---------------------------------------------------------------------------

class TestPipelineScore:
    def test_score_in_range(self, default_input):
        run_rate = _run_rate_pct(default_input)
        ratio = _coverage_ratio(default_input)
        score = _pipeline_score(default_input, ratio, run_rate)
        assert 0.0 <= score <= 100.0

    def test_score_is_numeric(self, default_input):
        run_rate = _run_rate_pct(default_input)
        ratio = _coverage_ratio(default_input)
        score = _pipeline_score(default_input, ratio, run_rate)
        assert isinstance(score, (int, float))

    def test_high_coverage_adds_30_pts(self):
        # coverage >= 4 → +30 pts (coverage component)
        inp = make_input(new_opps_created_30d=0, demos_completed_30d=0,
                         proposals_sent_30d=0, follow_up_rate_pct=0,
                         win_rate_pct=0, stage_3_eur=0, stage_1_eur=0, stage_2_eur=0,
                         pipeline_total_eur=1)
        # run rate = 0 (no closed won relative to expected pace at 50% elapsed)
        score = _pipeline_score(inp, 4.0, 0.0)
        # Only coverage pts: 30
        assert score == 30.0

    def test_adequate_coverage_adds_22_pts(self):
        inp = make_input(new_opps_created_30d=0, demos_completed_30d=0,
                         proposals_sent_30d=0, follow_up_rate_pct=0,
                         win_rate_pct=0, stage_3_eur=0, stage_1_eur=0, stage_2_eur=0,
                         pipeline_total_eur=1)
        score = _pipeline_score(inp, 3.5, 0.0)
        assert score == 22.0

    def test_thin_coverage_adds_12_pts(self):
        inp = make_input(new_opps_created_30d=0, demos_completed_30d=0,
                         proposals_sent_30d=0, follow_up_rate_pct=0,
                         win_rate_pct=0, stage_3_eur=0, stage_1_eur=0, stage_2_eur=0,
                         pipeline_total_eur=1)
        score = _pipeline_score(inp, 2.5, 0.0)
        assert score == 12.0

    def test_low_coverage_adds_5_pts(self):
        inp = make_input(new_opps_created_30d=0, demos_completed_30d=0,
                         proposals_sent_30d=0, follow_up_rate_pct=0,
                         win_rate_pct=0, stage_3_eur=0, stage_1_eur=0, stage_2_eur=0,
                         pipeline_total_eur=1)
        score = _pipeline_score(inp, 1.5, 0.0)
        assert score == 5.0

    def test_run_rate_capped_at_25_pts(self):
        inp = make_input(new_opps_created_30d=0, demos_completed_30d=0,
                         proposals_sent_30d=0, follow_up_rate_pct=0,
                         win_rate_pct=0, stage_3_eur=0, stage_1_eur=0, stage_2_eur=0,
                         pipeline_total_eur=1)
        # run_rate = 200 → min(25, 200*0.25) = min(25, 50) = 25
        score = _pipeline_score(inp, 0.0, 200.0)
        assert score == 25.0

    def test_win_rate_bonus_25pct(self):
        inp = make_input(win_rate_pct=25.0, new_opps_created_30d=0,
                         demos_completed_30d=0, proposals_sent_30d=0,
                         follow_up_rate_pct=0, stage_3_eur=0, stage_1_eur=0, stage_2_eur=0,
                         pipeline_total_eur=1)
        score = _pipeline_score(inp, 0.0, 0.0)
        assert score == 6.0

    def test_win_rate_bonus_15pct(self):
        inp = make_input(win_rate_pct=15.0, new_opps_created_30d=0,
                         demos_completed_30d=0, proposals_sent_30d=0,
                         follow_up_rate_pct=0, stage_3_eur=0, stage_1_eur=0, stage_2_eur=0,
                         pipeline_total_eur=1)
        score = _pipeline_score(inp, 0.0, 0.0)
        assert score == 3.0

    def test_follow_up_rate_80pct_bonus(self):
        inp = make_input(win_rate_pct=0, new_opps_created_30d=0,
                         demos_completed_30d=0, proposals_sent_30d=0,
                         follow_up_rate_pct=80.0, stage_3_eur=0, stage_1_eur=0, stage_2_eur=0,
                         pipeline_total_eur=1)
        score = _pipeline_score(inp, 0.0, 0.0)
        assert score == 4.0

    def test_follow_up_rate_60pct_bonus(self):
        inp = make_input(win_rate_pct=0, new_opps_created_30d=0,
                         demos_completed_30d=0, proposals_sent_30d=0,
                         follow_up_rate_pct=60.0, stage_3_eur=0, stage_1_eur=0, stage_2_eur=0,
                         pipeline_total_eur=1)
        score = _pipeline_score(inp, 0.0, 0.0)
        assert score == 2.0

    def test_score_clamped_at_100(self):
        inp = make_input(win_rate_pct=100.0, new_opps_created_30d=100,
                         demos_completed_30d=100, proposals_sent_30d=100,
                         follow_up_rate_pct=100.0, stage_3_eur=1_000_000,
                         stage_1_eur=0, stage_2_eur=0,
                         pipeline_total_eur=1_000_000)
        score = _pipeline_score(inp, 10.0, 200.0)
        assert score == 100.0

    def test_score_clamped_at_0(self):
        inp = make_input(win_rate_pct=0, new_opps_created_30d=0,
                         demos_completed_30d=0, proposals_sent_30d=0,
                         follow_up_rate_pct=0, stage_3_eur=0, stage_1_eur=0, stage_2_eur=0,
                         pipeline_total_eur=1)
        score = _pipeline_score(inp, 0.0, 0.0)
        assert score == 0.0

    def test_activity_opps_capped_at_10(self):
        # 5 new opps * 2 = 10; 6 * 2 = 12 → capped at 10
        inp5 = make_input(new_opps_created_30d=5, demos_completed_30d=0,
                          proposals_sent_30d=0, follow_up_rate_pct=0, win_rate_pct=0,
                          stage_3_eur=0, stage_1_eur=0, stage_2_eur=0, pipeline_total_eur=1)
        inp6 = make_input(new_opps_created_30d=6, demos_completed_30d=0,
                          proposals_sent_30d=0, follow_up_rate_pct=0, win_rate_pct=0,
                          stage_3_eur=0, stage_1_eur=0, stage_2_eur=0, pipeline_total_eur=1)
        assert _pipeline_score(inp5, 0.0, 0.0) == _pipeline_score(inp6, 0.0, 0.0)


# ---------------------------------------------------------------------------
# Class 14: _gap_drivers
# ---------------------------------------------------------------------------

class TestGapDrivers:
    def test_insufficient_coverage_driver(self):
        inp = make_input(pipeline_total_eur=10_000, quota_eur=100_000, closed_won_eur=0)
        drivers = _gap_drivers(inp, 90_000, CoverageHealth.INSUFFICIENT, 80.0)
        assert any("insuffisante" in d for d in drivers)

    def test_thin_coverage_driver(self):
        inp = make_input(pipeline_total_eur=150_000, quota_eur=100_000, closed_won_eur=0)
        drivers = _gap_drivers(inp, 50_000, CoverageHealth.THIN, 80.0)
        assert any("mince" in d for d in drivers)

    def test_low_run_rate_driver(self):
        inp = make_input()
        drivers = _gap_drivers(inp, 10_000, CoverageHealth.ADEQUATE, 60.0)
        assert any("pace" in d for d in drivers)

    def test_low_opps_driver(self):
        inp = make_input(new_opps_created_30d=2)
        drivers = _gap_drivers(inp, 10_000, CoverageHealth.ADEQUATE, 80.0)
        assert any("nouvelles opportunités" in d for d in drivers)

    def test_imbalanced_funnel_driver(self):
        # stage_1 > stage_2 + stage_3
        inp = make_input(stage_1_eur=200_000, stage_2_eur=50_000, stage_3_eur=50_000)
        drivers = _gap_drivers(inp, 10_000, CoverageHealth.ADEQUATE, 80.0)
        assert any("early stage" in d for d in drivers)

    def test_low_win_rate_driver(self):
        inp = make_input(win_rate_pct=10.0)
        drivers = _gap_drivers(inp, 10_000, CoverageHealth.ADEQUATE, 80.0)
        assert any("Taux de signature" in d for d in drivers)

    def test_long_cycle_vs_remaining_days_driver(self):
        inp = make_input(avg_sales_cycle_days=120, days_remaining=60)
        drivers = _gap_drivers(inp, 10_000, CoverageHealth.ADEQUATE, 80.0)
        assert any("Cycle de vente" in d for d in drivers)

    def test_low_follow_up_driver(self):
        inp = make_input(follow_up_rate_pct=40.0)
        drivers = _gap_drivers(inp, 10_000, CoverageHealth.ADEQUATE, 80.0)
        assert any("Suivi insuffisant" in d for d in drivers)

    def test_no_drivers_for_healthy_rep(self):
        inp = make_input(
            new_opps_created_30d=10,
            win_rate_pct=30.0,
            follow_up_rate_pct=90.0,
            avg_sales_cycle_days=30,
            days_remaining=90,
            stage_1_eur=10_000,
            stage_2_eur=50_000,
            stage_3_eur=100_000,
        )
        drivers = _gap_drivers(inp, 5_000, CoverageHealth.HEALTHY, 100.0)
        assert len(drivers) == 0

    def test_returns_list(self, default_input):
        drivers = _gap_drivers(default_input, 10_000, CoverageHealth.ADEQUATE, 80.0)
        assert isinstance(drivers, list)


# ---------------------------------------------------------------------------
# Class 15: _gap_closers
# ---------------------------------------------------------------------------

class TestGapClosers:
    def test_emergency_action_closers(self):
        inp = make_input()
        closers = _gap_closers(inp, PipelineAction.EMERGENCY, 50_000, CoverageHealth.INSUFFICIENT)
        assert any("Prospection intensive" in c for c in closers)
        assert any("dormants" in c for c in closers)

    def test_emergency_with_stage3_adds_closing_closer(self):
        inp = make_input(stage_3_eur=10_000)
        closers = _gap_closers(inp, PipelineAction.EMERGENCY, 50_000, CoverageHealth.INSUFFICIENT)
        assert any("closing stage" in c for c in closers)

    def test_emergency_without_stage3_no_closing_closer(self):
        inp = make_input(stage_3_eur=0)
        closers = _gap_closers(inp, PipelineAction.EMERGENCY, 50_000, CoverageHealth.INSUFFICIENT)
        assert not any("closing stage" in c for c in closers)

    def test_build_action_closers(self):
        inp = make_input()
        closers = _gap_closers(inp, PipelineAction.BUILD, 30_000, CoverageHealth.THIN)
        assert any("génération de pipeline" in c for c in closers)
        assert any("outbound" in c for c in closers)

    def test_accelerate_action_closers(self):
        inp = make_input()
        closers = _gap_closers(inp, PipelineAction.ACCELERATE, 15_000, CoverageHealth.ADEQUATE)
        assert any("stage 2 et 3" in c for c in closers)
        assert any("CRM" in c for c in closers)

    def test_maintain_action_closers(self):
        inp = make_input()
        closers = _gap_closers(inp, PipelineAction.MAINTAIN, 0, CoverageHealth.HEALTHY)
        assert any("cadence" in c for c in closers)
        assert any("expansion" in c for c in closers)

    def test_returns_list(self, default_input):
        closers = _gap_closers(default_input, PipelineAction.MAINTAIN, 0, CoverageHealth.HEALTHY)
        assert isinstance(closers, list)
        assert len(closers) > 0


# ---------------------------------------------------------------------------
# Class 16: PipelineGapResult & to_dict
# ---------------------------------------------------------------------------

class TestPipelineGapResult:
    def test_to_dict_keys(self, engine, default_input):
        result = engine.analyze(default_input)
        d = result.to_dict()
        expected_keys = {
            "rep_id", "rep_name", "region", "segment", "quota_eur",
            "gap_eur", "gap_severity", "pipeline_action", "quota_risk",
            "coverage_health", "coverage_ratio", "expected_close_eur",
            "quota_remaining_eur", "attainment_pct", "run_rate_pct",
            "gap_drivers", "gap_closers", "pipeline_score",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_values_are_strings(self, engine, default_input):
        result = engine.analyze(default_input)
        d = result.to_dict()
        assert isinstance(d["gap_severity"], str)
        assert isinstance(d["pipeline_action"], str)
        assert isinstance(d["quota_risk"], str)
        assert isinstance(d["coverage_health"], str)

    def test_to_dict_lists(self, engine, default_input):
        result = engine.analyze(default_input)
        d = result.to_dict()
        assert isinstance(d["gap_drivers"], list)
        assert isinstance(d["gap_closers"], list)

    def test_to_dict_numeric_fields(self, engine, default_input):
        result = engine.analyze(default_input)
        d = result.to_dict()
        assert isinstance(d["gap_eur"], (int, float))
        assert isinstance(d["coverage_ratio"], (int, float))
        assert isinstance(d["pipeline_score"], (int, float))
        assert isinstance(d["attainment_pct"], (int, float))
        assert isinstance(d["run_rate_pct"], (int, float))

    def test_to_dict_rep_fields(self, engine, default_input):
        result = engine.analyze(default_input)
        d = result.to_dict()
        assert d["rep_id"] == "R001"
        assert d["rep_name"] == "Alice Dupont"
        assert d["region"] == "EMEA"
        assert d["segment"] == "Mid-Market"


# ---------------------------------------------------------------------------
# Class 17: PipelineGapAnalyzerEngine.analyze — basic flow
# ---------------------------------------------------------------------------

class TestEngineAnalyze:
    def test_returns_pipeline_gap_result(self, engine, default_input):
        result = engine.analyze(default_input)
        assert isinstance(result, PipelineGapResult)

    def test_result_stored_in_engine(self, engine, default_input):
        engine.analyze(default_input)
        assert "R001" in engine._results

    def test_overwrite_same_rep(self, engine):
        inp1 = make_input(closed_won_eur=10_000)
        inp2 = make_input(closed_won_eur=90_000)
        engine.analyze(inp1)
        engine.analyze(inp2)
        assert len(engine._results) == 1
        assert engine._results["R001"].attainment_pct == 90.0

    def test_result_quota_remaining(self, engine):
        inp = make_input(quota_eur=100_000, closed_won_eur=30_000)
        result = engine.analyze(inp)
        assert result.quota_remaining_eur == 70_000.0

    def test_result_attainment(self, engine):
        inp = make_input(quota_eur=100_000, closed_won_eur=40_000)
        result = engine.analyze(inp)
        assert result.attainment_pct == 40.0

    def test_result_gap_non_negative(self, engine, default_input):
        result = engine.analyze(default_input)
        assert result.gap_eur >= 0.0

    def test_result_score_in_range(self, engine, default_input):
        result = engine.analyze(default_input)
        assert isinstance(result.pipeline_score, (int, float))
        assert 0.0 <= result.pipeline_score <= 100.0

    def test_result_coverage_ratio_positive(self, engine, default_input):
        result = engine.analyze(default_input)
        assert result.coverage_ratio > 0

    def test_result_severity_is_enum(self, engine, default_input):
        result = engine.analyze(default_input)
        assert isinstance(result.gap_severity, GapSeverity)

    def test_result_action_is_enum(self, engine, default_input):
        result = engine.analyze(default_input)
        assert isinstance(result.pipeline_action, PipelineAction)

    def test_result_risk_is_enum(self, engine, default_input):
        result = engine.analyze(default_input)
        assert isinstance(result.quota_risk, QuotaRisk)

    def test_result_coverage_health_is_enum(self, engine, default_input):
        result = engine.analyze(default_input)
        assert isinstance(result.coverage_health, CoverageHealth)


# ---------------------------------------------------------------------------
# Class 18: analyze_batch
# ---------------------------------------------------------------------------

class TestAnalyzeBatch:
    def test_returns_list(self, engine):
        inputs = [make_input(rep_id=f"R{i:03d}", rep_name=f"Rep {i}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        assert isinstance(results, list)
        assert len(results) == 3

    def test_sorted_by_gap_descending(self, engine):
        inp1 = make_input(rep_id="R001", rep_name="Rep1",
                          quota_eur=100_000, closed_won_eur=90_000, pipeline_total_eur=50_000,
                          stage_1_eur=20_000, stage_2_eur=15_000, stage_3_eur=15_000)
        inp2 = make_input(rep_id="R002", rep_name="Rep2",
                          quota_eur=200_000, closed_won_eur=10_000, pipeline_total_eur=50_000,
                          stage_1_eur=20_000, stage_2_eur=15_000, stage_3_eur=15_000)
        results = engine.analyze_batch([inp1, inp2])
        assert results[0].gap_eur >= results[1].gap_eur

    def test_all_stored_in_engine(self, engine):
        inputs = [make_input(rep_id=f"R{i:03d}", rep_name=f"Rep {i}") for i in range(5)]
        engine.analyze_batch(inputs)
        assert len(engine._results) == 5

    def test_empty_batch(self, engine):
        results = engine.analyze_batch([])
        assert results == []


# ---------------------------------------------------------------------------
# Class 19: Engine filter methods
# ---------------------------------------------------------------------------

class TestEngineFilterMethods:
    def _setup_mixed(self, engine):
        # Critical rep
        critical = make_input(
            rep_id="R001", rep_name="Critical Rep",
            quota_eur=100_000, closed_won_eur=0,
            pipeline_total_eur=10_000,
            stage_1_eur=5_000, stage_2_eur=3_000, stage_3_eur=2_000,
            win_rate_pct=10.0, days_elapsed=70, days_remaining=20,
            new_opps_created_30d=1, follow_up_rate_pct=20.0,
        )
        # Healthy rep
        healthy = make_input(
            rep_id="R002", rep_name="Healthy Rep",
            quota_eur=100_000, closed_won_eur=95_000,
            pipeline_total_eur=200_000,
            stage_1_eur=50_000, stage_2_eur=80_000, stage_3_eur=70_000,
            win_rate_pct=30.0, days_elapsed=80, days_remaining=10,
            new_opps_created_30d=8, follow_up_rate_pct=90.0,
        )
        engine.analyze_batch([critical, healthy])
        return critical, healthy

    def test_by_severity_returns_correct(self, engine):
        self._setup_mixed(engine)
        criticals = engine.by_severity(GapSeverity.CRITICAL)
        for r in criticals:
            assert r.gap_severity == GapSeverity.CRITICAL

    def test_by_action_returns_correct(self, engine):
        self._setup_mixed(engine)
        emergency = engine.by_action(PipelineAction.EMERGENCY)
        for r in emergency:
            assert r.pipeline_action == PipelineAction.EMERGENCY

    def test_by_quota_risk_returns_correct(self, engine):
        self._setup_mixed(engine)
        on_track = engine.by_quota_risk(QuotaRisk.ON_TRACK)
        for r in on_track:
            assert r.quota_risk == QuotaRisk.ON_TRACK

    def test_critical_gaps_delegates(self, engine):
        self._setup_mixed(engine)
        cg = engine.critical_gaps()
        assert cg == engine.by_severity(GapSeverity.CRITICAL)

    def test_needs_emergency_delegates(self, engine):
        self._setup_mixed(engine)
        ne = engine.needs_emergency()
        assert ne == engine.by_action(PipelineAction.EMERGENCY)

    def test_at_risk_reps_includes_behind_and_critical(self, engine):
        self._setup_mixed(engine)
        at_risk = engine.at_risk_reps()
        for r in at_risk:
            assert r.quota_risk in (QuotaRisk.BEHIND, QuotaRisk.CRITICAL)

    def test_on_track_reps(self, engine):
        self._setup_mixed(engine)
        on_track = engine.on_track_reps()
        for r in on_track:
            assert r.quota_risk == QuotaRisk.ON_TRACK


# ---------------------------------------------------------------------------
# Class 20: Engine aggregate methods
# ---------------------------------------------------------------------------

class TestEngineAggregates:
    def test_avg_coverage_ratio_empty(self, engine):
        assert engine.avg_coverage_ratio() == 0.0

    def test_avg_pipeline_score_empty(self, engine):
        assert engine.avg_pipeline_score() == 0.0

    def test_total_gap_eur_empty(self, engine):
        assert engine.total_gap_eur() == 0.0

    def test_total_pipeline_eur_empty(self, engine):
        assert engine.total_pipeline_eur() == 0.0

    def test_avg_coverage_ratio_excludes_99(self, engine):
        # Rep with closed_won >= quota gets coverage_ratio = 99, excluded from avg
        inp1 = make_input(rep_id="R001", rep_name="Over attained",
                          quota_eur=100_000, closed_won_eur=110_000)
        inp2 = make_input(rep_id="R002", rep_name="Normal",
                          quota_eur=100_000, closed_won_eur=0,
                          pipeline_total_eur=300_000)
        engine.analyze_batch([inp1, inp2])
        avg = engine.avg_coverage_ratio()
        # Only R002 is included (R001 has ratio=99, excluded)
        assert avg == engine._results["R002"].coverage_ratio

    def test_avg_pipeline_score_correct(self, engine):
        inp1 = make_input(rep_id="R001", rep_name="Rep1")
        inp2 = make_input(rep_id="R002", rep_name="Rep2")
        engine.analyze_batch([inp1, inp2])
        expected = round(
            (engine._results["R001"].pipeline_score + engine._results["R002"].pipeline_score) / 2,
            1
        )
        assert engine.avg_pipeline_score() == expected

    def test_total_gap_eur_sums(self, engine):
        inp1 = make_input(rep_id="R001", rep_name="Rep1")
        inp2 = make_input(rep_id="R002", rep_name="Rep2")
        engine.analyze_batch([inp1, inp2])
        expected = engine._results["R001"].gap_eur + engine._results["R002"].gap_eur
        assert engine.total_gap_eur() == expected

    def test_total_pipeline_eur_sums_quotas(self, engine):
        inp1 = make_input(rep_id="R001", rep_name="Rep1", quota_eur=100_000)
        inp2 = make_input(rep_id="R002", rep_name="Rep2", quota_eur=200_000)
        engine.analyze_batch([inp1, inp2])
        assert engine.total_pipeline_eur() == 300_000.0


# ---------------------------------------------------------------------------
# Class 21: Engine summary
# ---------------------------------------------------------------------------

class TestEngineSummary:
    def test_summary_keys(self, engine, default_input):
        engine.analyze(default_input)
        s = engine.summary()
        assert "total" in s
        assert "severity_counts" in s
        assert "action_counts" in s
        assert "risk_counts" in s
        assert "avg_pipeline_score" in s
        assert "avg_coverage_ratio" in s
        assert "critical_count" in s
        assert "emergency_count" in s
        assert "total_gap_eur" in s

    def test_summary_total_count(self, engine):
        inputs = [make_input(rep_id=f"R{i:03d}", rep_name=f"Rep {i}") for i in range(4)]
        engine.analyze_batch(inputs)
        s = engine.summary()
        assert s["total"] == 4

    def test_summary_severity_counts_cover_all(self, engine, default_input):
        engine.analyze(default_input)
        s = engine.summary()
        assert set(s["severity_counts"].keys()) == {sev.value for sev in GapSeverity}

    def test_summary_action_counts_cover_all(self, engine, default_input):
        engine.analyze(default_input)
        s = engine.summary()
        assert set(s["action_counts"].keys()) == {a.value for a in PipelineAction}

    def test_summary_risk_counts_cover_all(self, engine, default_input):
        engine.analyze(default_input)
        s = engine.summary()
        assert set(s["risk_counts"].keys()) == {r.value for r in QuotaRisk}

    def test_summary_counts_sum_to_total(self, engine):
        inputs = [make_input(rep_id=f"R{i:03d}", rep_name=f"Rep {i}") for i in range(6)]
        engine.analyze_batch(inputs)
        s = engine.summary()
        assert sum(s["severity_counts"].values()) == s["total"]
        assert sum(s["action_counts"].values()) == s["total"]
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_total_gap_eur(self, engine, default_input):
        engine.analyze(default_input)
        s = engine.summary()
        assert s["total_gap_eur"] == engine.total_gap_eur()

    def test_summary_empty_engine(self, engine):
        s = engine.summary()
        assert s["total"] == 0
        assert s["critical_count"] == 0
        assert s["emergency_count"] == 0
        assert s["total_gap_eur"] == 0.0


# ---------------------------------------------------------------------------
# Class 22: Engine reset
# ---------------------------------------------------------------------------

class TestEngineReset:
    def test_reset_clears_results(self, engine):
        inputs = [make_input(rep_id=f"R{i:03d}", rep_name=f"Rep {i}") for i in range(3)]
        engine.analyze_batch(inputs)
        assert len(engine._results) == 3
        engine.reset()
        assert len(engine._results) == 0

    def test_reset_then_reanalyze(self, engine, default_input):
        engine.analyze(default_input)
        engine.reset()
        result = engine.analyze(default_input)
        assert isinstance(result, PipelineGapResult)
        assert len(engine._results) == 1

    def test_aggregates_after_reset(self, engine, default_input):
        engine.analyze(default_input)
        engine.reset()
        assert engine.avg_coverage_ratio() == 0.0
        assert engine.avg_pipeline_score() == 0.0
        assert engine.total_gap_eur() == 0.0
        assert engine.total_pipeline_eur() == 0.0

    def test_reset_empties_filter_methods(self, engine, default_input):
        engine.analyze(default_input)
        engine.reset()
        assert engine.critical_gaps() == []
        assert engine.needs_emergency() == []
        assert engine.at_risk_reps() == []
        assert engine.on_track_reps() == []

    def test_reset_summary_shows_zeros(self, engine, default_input):
        engine.analyze(default_input)
        engine.reset()
        s = engine.summary()
        assert s["total"] == 0


# ---------------------------------------------------------------------------
# Class 23: End-to-end scenario tests
# ---------------------------------------------------------------------------

class TestEndToEndScenarios:
    def test_critical_scenario_end_to_end(self, engine):
        """Rep with no pipeline, no closings, late in period → CRITICAL everywhere."""
        inp = make_input(
            rep_id="CRIT01",
            rep_name="Crisis Rep",
            quota_eur=200_000,
            closed_won_eur=5_000,
            days_elapsed=80,
            days_remaining=10,
            pipeline_total_eur=20_000,
            stage_1_eur=15_000,
            stage_2_eur=5_000,
            stage_3_eur=0,
            win_rate_pct=10.0,
            new_opps_created_30d=1,
            follow_up_rate_pct=20.0,
        )
        result = engine.analyze(inp)
        assert result.gap_severity == GapSeverity.CRITICAL
        assert result.pipeline_action == PipelineAction.EMERGENCY
        assert result.quota_risk == QuotaRisk.CRITICAL
        assert result.gap_eur > 0
        assert len(result.gap_drivers) > 0
        assert len(result.gap_closers) > 0

    def test_healthy_scenario_end_to_end(self, engine):
        """Rep over quota with massive pipeline → everything healthy."""
        inp = make_input(
            rep_id="HLTH01",
            rep_name="Star Rep",
            quota_eur=100_000,
            closed_won_eur=95_000,
            days_elapsed=80,
            days_remaining=10,
            pipeline_total_eur=400_000,
            stage_1_eur=100_000,
            stage_2_eur=150_000,
            stage_3_eur=150_000,
            win_rate_pct=40.0,
            new_opps_created_30d=8,
            follow_up_rate_pct=90.0,
        )
        result = engine.analyze(inp)
        # Nearly done → quota remaining minimal
        assert result.quota_remaining_eur == 5_000.0
        assert result.attainment_pct == 95.0
        # remaining = 5_000, pipeline = 400_000 → ratio = 80 (not 99 sentinel)
        assert result.coverage_ratio == round(400_000 / 5_000, 2)
        assert result.gap_eur == 0.0
        assert result.gap_severity == GapSeverity.NONE
        assert result.pipeline_action == PipelineAction.MAINTAIN

    def test_moderate_scenario(self, engine):
        """Rep behind pace, moderate gap."""
        inp = make_input(
            rep_id="MOD01",
            rep_name="Moderate Rep",
            quota_eur=100_000,
            closed_won_eur=20_000,
            days_elapsed=60,
            days_remaining=30,
            pipeline_total_eur=150_000,
            stage_1_eur=60_000,
            stage_2_eur=60_000,
            stage_3_eur=30_000,
            win_rate_pct=20.0,
            new_opps_created_30d=4,
            follow_up_rate_pct=65.0,
        )
        result = engine.analyze(inp)
        assert result.quota_remaining_eur == 80_000.0
        assert result.gap_eur >= 0.0
        assert isinstance(result.pipeline_score, (int, float))
        assert 0.0 <= result.pipeline_score <= 100.0

    def test_batch_sorting(self, engine):
        """analyze_batch result sorted by gap_eur descending."""
        inputs = [
            make_input(rep_id=f"R{i:03d}", rep_name=f"Rep {i}",
                       quota_eur=100_000 * (i + 1),
                       closed_won_eur=1_000,
                       pipeline_total_eur=10_000,
                       stage_1_eur=5_000, stage_2_eur=3_000, stage_3_eur=2_000,
                       win_rate_pct=10.0)
            for i in range(5)
        ]
        results = engine.analyze_batch(inputs)
        gaps = [r.gap_eur for r in results]
        assert gaps == sorted(gaps, reverse=True)

    def test_multiple_reps_summary_consistent(self, engine):
        inputs = [make_input(rep_id=f"R{i:03d}", rep_name=f"Rep {i}") for i in range(10)]
        engine.analyze_batch(inputs)
        s = engine.summary()
        assert s["total"] == 10
        assert s["critical_count"] == len(engine.critical_gaps())
        assert s["emergency_count"] == len(engine.needs_emergency())
        assert sum(s["severity_counts"].values()) == 10
