"""
Comprehensive pytest tests for PipelineCoverageEngine.
Run from /home/user/TEST:
    python3 -m pytest swarm/tests/test_pipeline_coverage_engine.py -v
"""
from __future__ import annotations

import pytest

from swarm.intelligence.pipeline_coverage_engine import (
    CoverageAction,
    CoverageStatus,
    GapSeverity,
    PipelineCoverageEngine,
    PipelineCoverageInput,
    PipelineCoverageResult,
    PipelineQuality,
)


# ---------------------------------------------------------------------------
# Helpers / Fixtures
# ---------------------------------------------------------------------------

def make_input(
    team_id: str = "T1",
    region: str = "EMEA",
    segment: str = "ENT",
    manager_id: str = "M1",
    quota_remaining: float = 1_000_000.0,
    current_pipeline: float = 2_000_000.0,
    weighted_pipeline: float = 2_000_000.0,
    stage1_value: float = 200_000.0,
    stage2_value: float = 300_000.0,
    stage3_value: float = 500_000.0,
    stage4_value: float = 600_000.0,
    stage5_value: float = 400_000.0,
    historical_win_rate: float = 50.0,
    avg_deal_size: float = 100_000.0,
    avg_sales_cycle_days: int = 90,
    days_remaining: int = 30,
    pipeline_added_qtd: float = 500_000.0,
    churned_pipeline_qtd: float = 100_000.0,
    stalled_deal_count: int = 2,
    avg_deal_health: float = 75.0,
    competitive_deal_pct: float = 20.0,
) -> PipelineCoverageInput:
    return PipelineCoverageInput(
        team_id=team_id,
        region=region,
        segment=segment,
        manager_id=manager_id,
        quota_remaining=quota_remaining,
        current_pipeline=current_pipeline,
        weighted_pipeline=weighted_pipeline,
        stage1_value=stage1_value,
        stage2_value=stage2_value,
        stage3_value=stage3_value,
        stage4_value=stage4_value,
        stage5_value=stage5_value,
        historical_win_rate=historical_win_rate,
        avg_deal_size=avg_deal_size,
        avg_sales_cycle_days=avg_sales_cycle_days,
        days_remaining=days_remaining,
        pipeline_added_qtd=pipeline_added_qtd,
        churned_pipeline_qtd=churned_pipeline_qtd,
        stalled_deal_count=stalled_deal_count,
        avg_deal_health=avg_deal_health,
        competitive_deal_pct=competitive_deal_pct,
    )


@pytest.fixture
def engine() -> PipelineCoverageEngine:
    return PipelineCoverageEngine()


@pytest.fixture
def adequate_input() -> PipelineCoverageInput:
    """coverage_ratio = 2_000_000 / 1_000_000 = 2.0 → ADEQUATE"""
    return make_input(current_pipeline=2_000_000, weighted_pipeline=2_000_000, quota_remaining=1_000_000)


@pytest.fixture
def over_covered_input() -> PipelineCoverageInput:
    """coverage_ratio = 3_500_000 / 1_000_000 = 3.5 → OVER_COVERED"""
    return make_input(current_pipeline=3_500_000, weighted_pipeline=3_500_000, quota_remaining=1_000_000)


@pytest.fixture
def under_covered_input() -> PipelineCoverageInput:
    """coverage_ratio = 1_000_000 / 1_000_000 = 1.0 → UNDER_COVERED"""
    return make_input(current_pipeline=1_000_000, weighted_pipeline=800_000, quota_remaining=1_000_000)


@pytest.fixture
def critical_gap_input() -> PipelineCoverageInput:
    """coverage_ratio = 500_000 / 1_000_000 = 0.5 → CRITICAL_GAP"""
    return make_input(current_pipeline=500_000, weighted_pipeline=300_000, quota_remaining=1_000_000)


# ===========================================================================
# 1. CoverageStatus enum values
# ===========================================================================

class TestCoverageStatusEnum:
    def test_over_covered_value(self):
        assert CoverageStatus.OVER_COVERED.value == "over_covered"

    def test_adequate_value(self):
        assert CoverageStatus.ADEQUATE.value == "adequate"

    def test_under_covered_value(self):
        assert CoverageStatus.UNDER_COVERED.value == "under_covered"

    def test_critical_gap_value(self):
        assert CoverageStatus.CRITICAL_GAP.value == "critical_gap"

    def test_all_four_statuses_exist(self):
        values = {s.value for s in CoverageStatus}
        assert values == {"over_covered", "adequate", "under_covered", "critical_gap"}

    def test_coverage_status_is_str_enum(self):
        assert isinstance(CoverageStatus.OVER_COVERED, str)

    def test_coverage_status_string_comparison(self):
        assert CoverageStatus.ADEQUATE == "adequate"

    def test_coverage_status_count(self):
        assert len(list(CoverageStatus)) == 4


# ===========================================================================
# 2. GapSeverity enum values
# ===========================================================================

class TestGapSeverityEnum:
    def test_none_value(self):
        assert GapSeverity.NONE.value == "none"

    def test_low_value(self):
        assert GapSeverity.LOW.value == "low"

    def test_medium_value(self):
        assert GapSeverity.MEDIUM.value == "medium"

    def test_high_value(self):
        assert GapSeverity.HIGH.value == "high"

    def test_critical_value(self):
        assert GapSeverity.CRITICAL.value == "critical"

    def test_all_five_severities_exist(self):
        values = {g.value for g in GapSeverity}
        assert values == {"none", "low", "medium", "high", "critical"}

    def test_gap_severity_is_str_enum(self):
        assert isinstance(GapSeverity.NONE, str)

    def test_gap_severity_count(self):
        assert len(list(GapSeverity)) == 5

    def test_gap_severity_string_comparison(self):
        assert GapSeverity.CRITICAL == "critical"


# ===========================================================================
# 3. PipelineQuality enum values
# ===========================================================================

class TestPipelineQualityEnum:
    def test_excellent_value(self):
        assert PipelineQuality.EXCELLENT.value == "excellent"

    def test_good_value(self):
        assert PipelineQuality.GOOD.value == "good"

    def test_fair_value(self):
        assert PipelineQuality.FAIR.value == "fair"

    def test_poor_value(self):
        assert PipelineQuality.POOR.value == "poor"

    def test_all_four_qualities_exist(self):
        values = {q.value for q in PipelineQuality}
        assert values == {"excellent", "good", "fair", "poor"}

    def test_pipeline_quality_is_str_enum(self):
        assert isinstance(PipelineQuality.GOOD, str)

    def test_pipeline_quality_count(self):
        assert len(list(PipelineQuality)) == 4

    def test_pipeline_quality_string_comparison(self):
        assert PipelineQuality.FAIR == "fair"


# ===========================================================================
# 4. CoverageAction enum values
# ===========================================================================

class TestCoverageActionEnum:
    def test_maintain_value(self):
        assert CoverageAction.MAINTAIN.value == "maintain"

    def test_accelerate_existing_value(self):
        assert CoverageAction.ACCELERATE_EXISTING.value == "accelerate_existing"

    def test_generate_pipeline_value(self):
        assert CoverageAction.GENERATE_PIPELINE.value == "generate_pipeline"

    def test_reallocate_value(self):
        assert CoverageAction.REALLOCATE.value == "reallocate"

    def test_expand_upmarket_value(self):
        assert CoverageAction.EXPAND_UPMARKET.value == "expand_upmarket"

    def test_strategic_review_value(self):
        assert CoverageAction.STRATEGIC_REVIEW.value == "strategic_review"

    def test_all_six_actions_exist(self):
        values = {a.value for a in CoverageAction}
        assert values == {
            "maintain", "accelerate_existing", "generate_pipeline",
            "reallocate", "expand_upmarket", "strategic_review"
        }

    def test_coverage_action_is_str_enum(self):
        assert isinstance(CoverageAction.MAINTAIN, str)

    def test_coverage_action_count(self):
        assert len(list(CoverageAction)) == 6

    def test_coverage_action_string_comparison(self):
        assert CoverageAction.REALLOCATE == "reallocate"


# ===========================================================================
# 5. to_dict() – exactly 15 keys, enum serialization as strings
# ===========================================================================

class TestToDict:
    def test_to_dict_returns_15_keys(self, engine, adequate_input):
        result = engine.analyze(adequate_input)
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_exact_key_set(self, engine, adequate_input):
        d = engine.analyze(adequate_input).to_dict()
        expected_keys = {
            "team_id", "region", "coverage_status", "gap_severity",
            "pipeline_quality", "coverage_action", "coverage_ratio",
            "weighted_coverage_ratio", "gap_to_quota", "pipeline_velocity",
            "quality_score", "stage_mix_score", "coverage_trend",
            "is_at_risk", "needs_intervention",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_coverage_status_is_string(self, engine, adequate_input):
        d = engine.analyze(adequate_input).to_dict()
        assert isinstance(d["coverage_status"], str)
        assert not isinstance(d["coverage_status"], CoverageStatus)

    def test_to_dict_gap_severity_is_string(self, engine, adequate_input):
        d = engine.analyze(adequate_input).to_dict()
        assert isinstance(d["gap_severity"], str)

    def test_to_dict_pipeline_quality_is_string(self, engine, adequate_input):
        d = engine.analyze(adequate_input).to_dict()
        assert isinstance(d["pipeline_quality"], str)

    def test_to_dict_coverage_action_is_string(self, engine, adequate_input):
        d = engine.analyze(adequate_input).to_dict()
        assert isinstance(d["coverage_action"], str)

    def test_to_dict_coverage_status_correct_value(self, engine, adequate_input):
        d = engine.analyze(adequate_input).to_dict()
        assert d["coverage_status"] == "adequate"

    def test_to_dict_gap_severity_correct_value(self, engine):
        # weighted_pipeline >= quota_remaining → gap = 0 → NONE
        inp = make_input(weighted_pipeline=2_000_000, quota_remaining=1_000_000)
        d = engine.analyze(inp).to_dict()
        assert d["gap_severity"] == "none"

    def test_to_dict_team_id_preserved(self, engine):
        inp = make_input(team_id="XYZ")
        d = engine.analyze(inp).to_dict()
        assert d["team_id"] == "XYZ"

    def test_to_dict_region_preserved(self, engine):
        inp = make_input(region="APAC")
        d = engine.analyze(inp).to_dict()
        assert d["region"] == "APAC"

    def test_to_dict_is_at_risk_is_bool(self, engine, adequate_input):
        d = engine.analyze(adequate_input).to_dict()
        assert isinstance(d["is_at_risk"], bool)

    def test_to_dict_needs_intervention_is_bool(self, engine, adequate_input):
        d = engine.analyze(adequate_input).to_dict()
        assert isinstance(d["needs_intervention"], bool)

    def test_to_dict_coverage_ratio_is_numeric(self, engine, adequate_input):
        d = engine.analyze(adequate_input).to_dict()
        assert isinstance(d["coverage_ratio"], (int, float))

    def test_to_dict_gap_to_quota_is_numeric(self, engine, adequate_input):
        d = engine.analyze(adequate_input).to_dict()
        assert isinstance(d["gap_to_quota"], (int, float))

    def test_to_dict_quality_score_is_numeric(self, engine, adequate_input):
        d = engine.analyze(adequate_input).to_dict()
        assert isinstance(d["quality_score"], (int, float))

    def test_to_dict_pipeline_quality_not_enum_object(self, engine, adequate_input):
        d = engine.analyze(adequate_input).to_dict()
        assert d["pipeline_quality"] in {"excellent", "good", "fair", "poor"}

    def test_to_dict_coverage_action_not_enum_object(self, engine, adequate_input):
        d = engine.analyze(adequate_input).to_dict()
        assert d["coverage_action"] in {
            "maintain", "accelerate_existing", "generate_pipeline",
            "reallocate", "expand_upmarket", "strategic_review"
        }


# ===========================================================================
# 6. summary() – exactly 13 keys
# ===========================================================================

class TestSummary:
    EXPECTED_KEYS = {
        "total", "status_counts", "gap_severity_counts", "quality_counts",
        "action_counts", "avg_coverage_ratio", "avg_weighted_coverage",
        "total_gap_to_quota", "at_risk_count", "intervention_count",
        "avg_quality_score", "avg_stage_mix_score", "healthy_team_count",
    }

    def test_summary_empty_returns_13_keys(self, engine):
        s = engine.summary()
        assert len(s) == 13

    def test_summary_empty_exact_keys(self, engine):
        s = engine.summary()
        assert set(s.keys()) == self.EXPECTED_KEYS

    def test_summary_empty_total_zero(self, engine):
        assert engine.summary()["total"] == 0

    def test_summary_empty_at_risk_count_zero(self, engine):
        assert engine.summary()["at_risk_count"] == 0

    def test_summary_empty_intervention_count_zero(self, engine):
        assert engine.summary()["intervention_count"] == 0

    def test_summary_empty_avg_coverage_ratio_zero(self, engine):
        assert engine.summary()["avg_coverage_ratio"] == 0.0

    def test_summary_empty_avg_weighted_coverage_zero(self, engine):
        assert engine.summary()["avg_weighted_coverage"] == 0.0

    def test_summary_empty_total_gap_zero(self, engine):
        assert engine.summary()["total_gap_to_quota"] == 0.0

    def test_summary_empty_avg_quality_score_zero(self, engine):
        assert engine.summary()["avg_quality_score"] == 0.0

    def test_summary_empty_avg_stage_mix_zero(self, engine):
        assert engine.summary()["avg_stage_mix_score"] == 0.0

    def test_summary_empty_healthy_team_count_zero(self, engine):
        assert engine.summary()["healthy_team_count"] == 0

    def test_summary_empty_status_counts_empty_dict(self, engine):
        assert engine.summary()["status_counts"] == {}

    def test_summary_empty_gap_severity_counts_empty_dict(self, engine):
        assert engine.summary()["gap_severity_counts"] == {}

    def test_summary_with_results_returns_13_keys(self, engine, adequate_input):
        engine.analyze(adequate_input)
        s = engine.summary()
        assert len(s) == 13

    def test_summary_with_results_exact_keys(self, engine, adequate_input):
        engine.analyze(adequate_input)
        s = engine.summary()
        assert set(s.keys()) == self.EXPECTED_KEYS

    def test_summary_with_results_total_correct(self, engine, adequate_input):
        engine.analyze(adequate_input)
        engine.analyze(adequate_input)
        assert engine.summary()["total"] == 2

    def test_summary_status_counts_populated(self, engine, adequate_input):
        engine.analyze(adequate_input)
        s = engine.summary()
        assert "adequate" in s["status_counts"]

    def test_summary_gap_severity_counts_populated(self, engine, adequate_input):
        engine.analyze(adequate_input)
        s = engine.summary()
        assert isinstance(s["gap_severity_counts"], dict)
        assert len(s["gap_severity_counts"]) > 0

    def test_summary_quality_counts_populated(self, engine, adequate_input):
        engine.analyze(adequate_input)
        s = engine.summary()
        assert isinstance(s["quality_counts"], dict)
        assert len(s["quality_counts"]) > 0

    def test_summary_action_counts_populated(self, engine, adequate_input):
        engine.analyze(adequate_input)
        s = engine.summary()
        assert isinstance(s["action_counts"], dict)
        assert len(s["action_counts"]) > 0

    def test_summary_avg_coverage_ratio_nonzero_with_results(self, engine, adequate_input):
        engine.analyze(adequate_input)
        assert engine.summary()["avg_coverage_ratio"] > 0.0

    def test_summary_healthy_team_count_for_adequate(self, engine, adequate_input):
        engine.analyze(adequate_input)
        assert engine.summary()["healthy_team_count"] >= 1

    def test_summary_total_gap_matches_property(self, engine, critical_gap_input):
        engine.analyze(critical_gap_input)
        s = engine.summary()
        assert s["total_gap_to_quota"] == engine.total_gap_to_quota


# ===========================================================================
# 7. _coverage_ratio
# ===========================================================================

class TestCoverageRatio:
    def test_basic_coverage_ratio(self, engine):
        inp = make_input(current_pipeline=2_000_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.coverage_ratio == pytest.approx(2.0)

    def test_coverage_ratio_zero_when_quota_zero(self, engine):
        inp = make_input(current_pipeline=500_000, quota_remaining=0)
        result = engine.analyze(inp)
        assert result.coverage_ratio == 0.0

    def test_coverage_ratio_zero_when_quota_negative(self, engine):
        inp = make_input(current_pipeline=500_000, quota_remaining=-100)
        result = engine.analyze(inp)
        assert result.coverage_ratio == 0.0

    def test_coverage_ratio_less_than_one(self, engine):
        inp = make_input(current_pipeline=500_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.coverage_ratio == pytest.approx(0.5)

    def test_coverage_ratio_exactly_one(self, engine):
        inp = make_input(current_pipeline=1_000_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.coverage_ratio == pytest.approx(1.0)

    def test_coverage_ratio_three_point_five(self, engine):
        inp = make_input(current_pipeline=3_500_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.coverage_ratio == pytest.approx(3.5)

    def test_coverage_ratio_rounded_to_2dp(self, engine):
        inp = make_input(current_pipeline=1_000_000, quota_remaining=300_000)
        result = engine.analyze(inp)
        # 1000000/300000 = 3.3333... → 3.33
        assert result.coverage_ratio == pytest.approx(3.33)

    def test_coverage_ratio_positive_pipeline_zero_quota(self, engine):
        inp = make_input(current_pipeline=1_000_000, quota_remaining=0.0)
        result = engine.analyze(inp)
        assert result.coverage_ratio == 0.0


# ===========================================================================
# 8. _weighted_coverage_ratio
# ===========================================================================

class TestWeightedCoverageRatio:
    def test_basic_weighted_ratio(self, engine):
        inp = make_input(weighted_pipeline=2_000_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.weighted_coverage_ratio == pytest.approx(2.0)

    def test_weighted_ratio_zero_when_quota_zero(self, engine):
        inp = make_input(weighted_pipeline=500_000, quota_remaining=0)
        result = engine.analyze(inp)
        assert result.weighted_coverage_ratio == 0.0

    def test_weighted_ratio_zero_when_quota_negative(self, engine):
        inp = make_input(weighted_pipeline=500_000, quota_remaining=-1)
        result = engine.analyze(inp)
        assert result.weighted_coverage_ratio == 0.0

    def test_weighted_ratio_less_than_one(self, engine):
        inp = make_input(weighted_pipeline=400_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.weighted_coverage_ratio == pytest.approx(0.4)

    def test_weighted_ratio_can_exceed_one(self, engine):
        inp = make_input(weighted_pipeline=5_000_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.weighted_coverage_ratio == pytest.approx(5.0)

    def test_weighted_ratio_rounded_to_2dp(self, engine):
        inp = make_input(weighted_pipeline=1_000_000, quota_remaining=300_000)
        result = engine.analyze(inp)
        assert result.weighted_coverage_ratio == pytest.approx(3.33)

    def test_weighted_ratio_independent_of_current_pipeline(self, engine):
        inp = make_input(current_pipeline=5_000_000, weighted_pipeline=1_000_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.weighted_coverage_ratio == pytest.approx(1.0)


# ===========================================================================
# 9. _gap_to_quota
# ===========================================================================

class TestGapToQuota:
    def test_gap_to_quota_basic(self, engine):
        inp = make_input(weighted_pipeline=600_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.gap_to_quota == pytest.approx(400_000.0)

    def test_gap_to_quota_zero_when_fully_covered(self, engine):
        inp = make_input(weighted_pipeline=1_000_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.gap_to_quota == 0.0

    def test_gap_to_quota_zero_when_over_covered(self, engine):
        inp = make_input(weighted_pipeline=2_000_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.gap_to_quota == 0.0

    def test_gap_to_quota_never_negative(self, engine):
        inp = make_input(weighted_pipeline=9_999_999, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.gap_to_quota >= 0.0

    def test_gap_to_quota_zero_quota_remaining(self, engine):
        inp = make_input(weighted_pipeline=0, quota_remaining=0)
        result = engine.analyze(inp)
        # quota_remaining=0, weighted=0 → max(0, 0-0) = 0
        assert result.gap_to_quota == 0.0

    def test_gap_to_quota_partial_coverage(self, engine):
        inp = make_input(weighted_pipeline=300_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.gap_to_quota == pytest.approx(700_000.0)

    def test_gap_to_quota_full_gap_no_pipeline(self, engine):
        inp = make_input(
            weighted_pipeline=0,
            quota_remaining=500_000,
            current_pipeline=0,
            stage1_value=0, stage2_value=0, stage3_value=0,
            stage4_value=0, stage5_value=0,
        )
        result = engine.analyze(inp)
        assert result.gap_to_quota == pytest.approx(500_000.0)


# ===========================================================================
# 10. _pipeline_velocity
# ===========================================================================

class TestPipelineVelocity:
    def test_basic_velocity(self, engine):
        # elapsed = max(1, 90 - 30) = 60; velocity = 500000/60 ≈ 8333.33
        inp = make_input(
            pipeline_added_qtd=500_000,
            avg_sales_cycle_days=90,
            days_remaining=30,
        )
        result = engine.analyze(inp)
        assert result.pipeline_velocity == pytest.approx(500_000 / 60, rel=1e-2)

    def test_velocity_zero_when_days_remaining_zero(self, engine):
        inp = make_input(days_remaining=0)
        result = engine.analyze(inp)
        assert result.pipeline_velocity == 0.0

    def test_velocity_zero_when_days_remaining_negative(self, engine):
        inp = make_input(days_remaining=-5)
        result = engine.analyze(inp)
        assert result.pipeline_velocity == 0.0

    def test_velocity_min_elapsed_is_1(self, engine):
        # avg_sales_cycle = 10, days_remaining = 10 → elapsed = max(1, 0) = 1
        inp = make_input(
            pipeline_added_qtd=1_000,
            avg_sales_cycle_days=10,
            days_remaining=10,
        )
        result = engine.analyze(inp)
        assert result.pipeline_velocity == pytest.approx(1_000.0)

    def test_velocity_uses_pipeline_added_qtd(self, engine):
        inp = make_input(
            pipeline_added_qtd=120_000,
            avg_sales_cycle_days=90,
            days_remaining=30,
        )
        result = engine.analyze(inp)
        assert result.pipeline_velocity == pytest.approx(120_000 / 60, rel=1e-2)

    def test_velocity_rounded_to_2dp(self, engine):
        inp = make_input(
            pipeline_added_qtd=100_000,
            avg_sales_cycle_days=93,
            days_remaining=30,
        )
        # elapsed = 63
        expected = round(100_000 / 63, 2)
        result = engine.analyze(inp)
        assert result.pipeline_velocity == pytest.approx(expected)

    def test_velocity_larger_than_one_day(self, engine):
        inp = make_input(
            pipeline_added_qtd=1_000_000,
            avg_sales_cycle_days=90,
            days_remaining=1,
        )
        result = engine.analyze(inp)
        assert result.pipeline_velocity > 0


# ===========================================================================
# 11. _quality_score
# ===========================================================================

class TestQualityScore:
    def test_quality_score_formula(self, engine):
        # health*0.4 + win*0.3 - stall_rate*20 - min(10, competitive*0.10)
        inp = make_input(
            avg_deal_health=80,
            historical_win_rate=60,
            stalled_deal_count=0,
            competitive_deal_pct=0,
            current_pipeline=1_000_000,
            avg_deal_size=100_000,
        )
        # total_deals = max(1, 1000000/100000) = 10; stall_rate = 0
        expected = 80 * 0.40 + 60 * 0.30 - 0 - 0
        result = engine.analyze(inp)
        assert result.quality_score == pytest.approx(expected, rel=1e-2)

    def test_quality_score_clamped_max_100(self, engine):
        inp = make_input(
            avg_deal_health=100,
            historical_win_rate=100,
            stalled_deal_count=0,
            competitive_deal_pct=0,
        )
        result = engine.analyze(inp)
        assert result.quality_score <= 100.0

    def test_quality_score_clamped_min_0(self, engine):
        inp = make_input(
            avg_deal_health=0,
            historical_win_rate=0,
            stalled_deal_count=1000,
            competitive_deal_pct=100,
            current_pipeline=100,
            avg_deal_size=100,
        )
        result = engine.analyze(inp)
        assert result.quality_score >= 0.0

    def test_quality_score_stall_penalty(self, engine):
        # No stall vs high stall
        inp_no_stall = make_input(
            stalled_deal_count=0, current_pipeline=1_000_000, avg_deal_size=100_000,
            avg_deal_health=70, historical_win_rate=50, competitive_deal_pct=0,
        )
        inp_stall = make_input(
            stalled_deal_count=5, current_pipeline=1_000_000, avg_deal_size=100_000,
            avg_deal_health=70, historical_win_rate=50, competitive_deal_pct=0,
        )
        r1 = engine.analyze(inp_no_stall)
        r2 = engine.analyze(inp_stall)
        assert r1.quality_score > r2.quality_score

    def test_quality_score_competitive_penalty(self, engine):
        inp_low = make_input(competitive_deal_pct=0, avg_deal_health=70, historical_win_rate=50, stalled_deal_count=0)
        inp_high = make_input(competitive_deal_pct=100, avg_deal_health=70, historical_win_rate=50, stalled_deal_count=0)
        r1 = engine.analyze(inp_low)
        r2 = engine.analyze(inp_high)
        assert r1.quality_score > r2.quality_score

    def test_quality_score_competitive_capped_at_10(self, engine):
        # competitive_deal_pct=200 should not penalise more than 10
        inp_200 = make_input(competitive_deal_pct=200, avg_deal_health=80, historical_win_rate=60, stalled_deal_count=0)
        inp_100 = make_input(competitive_deal_pct=100, avg_deal_health=80, historical_win_rate=60, stalled_deal_count=0)
        r_200 = engine.analyze(inp_200)
        r_100 = engine.analyze(inp_100)
        assert r_200.quality_score == r_100.quality_score

    def test_quality_score_deal_health_contribution(self, engine):
        inp_lo = make_input(avg_deal_health=0, historical_win_rate=0, stalled_deal_count=0, competitive_deal_pct=0)
        inp_hi = make_input(avg_deal_health=100, historical_win_rate=0, stalled_deal_count=0, competitive_deal_pct=0)
        r_lo = engine.analyze(inp_lo)
        r_hi = engine.analyze(inp_hi)
        assert r_hi.quality_score - r_lo.quality_score == pytest.approx(40.0, rel=1e-2)

    def test_quality_score_win_rate_contribution(self, engine):
        inp_lo = make_input(avg_deal_health=0, historical_win_rate=0, stalled_deal_count=0, competitive_deal_pct=0)
        inp_hi = make_input(avg_deal_health=0, historical_win_rate=100, stalled_deal_count=0, competitive_deal_pct=0)
        r_lo = engine.analyze(inp_lo)
        r_hi = engine.analyze(inp_hi)
        assert r_hi.quality_score - r_lo.quality_score == pytest.approx(30.0, rel=1e-2)

    def test_quality_score_is_one_decimal(self, engine, adequate_input):
        result = engine.analyze(adequate_input)
        # rounded to 1 decimal
        assert result.quality_score == round(result.quality_score, 1)


# ===========================================================================
# 12. _stage_mix_score
# ===========================================================================

class TestStageMixScore:
    def test_all_late_stage_gives_60(self, engine):
        inp = make_input(
            current_pipeline=1_000_000,
            stage1_value=0, stage2_value=0, stage3_value=0,
            stage4_value=500_000, stage5_value=500_000,
        )
        result = engine.analyze(inp)
        assert result.stage_mix_score == pytest.approx(60.0)

    def test_all_mid_stage_gives_30(self, engine):
        inp = make_input(
            current_pipeline=1_000_000,
            stage1_value=0, stage2_value=0, stage3_value=1_000_000,
            stage4_value=0, stage5_value=0,
        )
        result = engine.analyze(inp)
        assert result.stage_mix_score == pytest.approx(30.0)

    def test_all_early_stage_gives_10(self, engine):
        inp = make_input(
            current_pipeline=1_000_000,
            stage1_value=500_000, stage2_value=500_000, stage3_value=0,
            stage4_value=0, stage5_value=0,
        )
        result = engine.analyze(inp)
        assert result.stage_mix_score == pytest.approx(10.0)

    def test_stage_mix_score_clamped_max_100(self, engine):
        inp = make_input(
            current_pipeline=1_000_000,
            stage1_value=0, stage2_value=0, stage3_value=0,
            stage4_value=1_000_000, stage5_value=0,
        )
        result = engine.analyze(inp)
        assert result.stage_mix_score <= 100.0

    def test_stage_mix_score_clamped_min_0(self, engine):
        inp = make_input(
            current_pipeline=0,
            stage1_value=0, stage2_value=0, stage3_value=0,
            stage4_value=0, stage5_value=0,
        )
        result = engine.analyze(inp)
        assert result.stage_mix_score >= 0.0

    def test_stage_mix_score_equal_distribution(self, engine):
        # each stage = 200k, total = 1000k
        inp = make_input(
            current_pipeline=1_000_000,
            stage1_value=200_000, stage2_value=200_000, stage3_value=200_000,
            stage4_value=200_000, stage5_value=200_000,
        )
        result = engine.analyze(inp)
        # (40%×60) + (20%×30) + (40%×10) = 24 + 6 + 4 = 34
        assert result.stage_mix_score == pytest.approx(34.0)

    def test_stage_mix_score_uses_max_1_floor(self, engine):
        # current_pipeline=0 → total=max(1,0)=1 → no division by zero
        inp = make_input(
            current_pipeline=0,
            stage1_value=0, stage2_value=0, stage3_value=0,
            stage4_value=0, stage5_value=0,
        )
        result = engine.analyze(inp)
        assert result.stage_mix_score == 0.0

    def test_stage_mix_score_100_all_late(self, engine):
        # 100% late stage → 1.0*60 = 60 (max possible is 60, not 100)
        inp = make_input(
            current_pipeline=1_000_000,
            stage1_value=0, stage2_value=0, stage3_value=0,
            stage4_value=1_000_000, stage5_value=0,
        )
        result = engine.analyze(inp)
        assert result.stage_mix_score == pytest.approx(60.0)

    def test_stage_mix_score_one_decimal(self, engine, adequate_input):
        result = engine.analyze(adequate_input)
        assert result.stage_mix_score == round(result.stage_mix_score, 1)


# ===========================================================================
# 13. _coverage_trend
# ===========================================================================

class TestCoverageTrend:
    def test_positive_trend(self, engine):
        inp = make_input(pipeline_added_qtd=600_000, churned_pipeline_qtd=100_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.coverage_trend == pytest.approx((500_000 / 1_000_000) * 100)

    def test_negative_trend(self, engine):
        inp = make_input(pipeline_added_qtd=100_000, churned_pipeline_qtd=600_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.coverage_trend == pytest.approx(-50.0)

    def test_trend_zero_when_quota_zero(self, engine):
        inp = make_input(pipeline_added_qtd=500_000, churned_pipeline_qtd=100_000, quota_remaining=0)
        result = engine.analyze(inp)
        assert result.coverage_trend == 0.0

    def test_trend_zero_when_added_equals_churned(self, engine):
        inp = make_input(pipeline_added_qtd=300_000, churned_pipeline_qtd=300_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.coverage_trend == pytest.approx(0.0)

    def test_trend_rounded_to_1dp(self, engine):
        inp = make_input(pipeline_added_qtd=100_000, churned_pipeline_qtd=0, quota_remaining=300_000)
        result = engine.analyze(inp)
        expected = round((100_000 / 300_000) * 100, 1)
        assert result.coverage_trend == pytest.approx(expected)

    def test_trend_100_percent(self, engine):
        inp = make_input(pipeline_added_qtd=1_000_000, churned_pipeline_qtd=0, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.coverage_trend == pytest.approx(100.0)


# ===========================================================================
# 14. _coverage_status thresholds
# ===========================================================================

class TestCoverageStatusThresholds:
    def test_exactly_3_5_is_over_covered(self, engine):
        inp = make_input(current_pipeline=3_500_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.coverage_status == CoverageStatus.OVER_COVERED

    def test_above_3_5_is_over_covered(self, engine):
        inp = make_input(current_pipeline=4_000_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.coverage_status == CoverageStatus.OVER_COVERED

    def test_exactly_2_0_is_adequate(self, engine):
        inp = make_input(current_pipeline=2_000_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.coverage_status == CoverageStatus.ADEQUATE

    def test_between_2_0_and_3_5_is_adequate(self, engine):
        inp = make_input(current_pipeline=2_500_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.coverage_status == CoverageStatus.ADEQUATE

    def test_just_below_3_5_is_adequate(self, engine):
        # 3_499_000 / 1_000_000 rounds to 3.5 at 2dp, use a value that rounds to 3.49
        inp = make_input(current_pipeline=3_494_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.coverage_status == CoverageStatus.ADEQUATE

    def test_exactly_1_0_is_under_covered(self, engine):
        inp = make_input(current_pipeline=1_000_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.coverage_status == CoverageStatus.UNDER_COVERED

    def test_between_1_0_and_2_0_is_under_covered(self, engine):
        inp = make_input(current_pipeline=1_500_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.coverage_status == CoverageStatus.UNDER_COVERED

    def test_just_below_2_0_is_under_covered(self, engine):
        # 1_999_000 / 1_000_000 rounds to 2.0 at 2dp, use a value that rounds to 1.99
        inp = make_input(current_pipeline=1_994_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.coverage_status == CoverageStatus.UNDER_COVERED

    def test_below_1_0_is_critical_gap(self, engine):
        inp = make_input(current_pipeline=500_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.coverage_status == CoverageStatus.CRITICAL_GAP

    def test_zero_pipeline_is_critical_gap(self, engine):
        inp = make_input(
            current_pipeline=0,
            quota_remaining=1_000_000,
            stage1_value=0, stage2_value=0, stage3_value=0,
            stage4_value=0, stage5_value=0,
        )
        result = engine.analyze(inp)
        assert result.coverage_status == CoverageStatus.CRITICAL_GAP

    def test_zero_quota_gives_critical_gap(self, engine):
        # coverage_ratio = 0.0 when quota = 0 → CRITICAL_GAP
        inp = make_input(current_pipeline=1_000_000, quota_remaining=0)
        result = engine.analyze(inp)
        assert result.coverage_status == CoverageStatus.CRITICAL_GAP

    def test_coverage_just_above_1_is_under_covered(self, engine):
        inp = make_input(current_pipeline=1_010_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.coverage_status == CoverageStatus.UNDER_COVERED


# ===========================================================================
# 15. _gap_severity thresholds
# ===========================================================================

class TestGapSeverityThresholds:
    def test_gap_zero_is_none(self, engine):
        inp = make_input(weighted_pipeline=1_000_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.gap_severity == GapSeverity.NONE

    def test_gap_negative_is_none(self, engine):
        inp = make_input(weighted_pipeline=2_000_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.gap_severity == GapSeverity.NONE

    def test_gap_just_under_20pct_is_low(self, engine):
        # gap = 190_000 → pct = 19% < 20 → LOW
        inp = make_input(weighted_pipeline=810_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.gap_severity == GapSeverity.LOW

    def test_gap_exactly_20pct_is_medium(self, engine):
        # gap = 200_000 → pct = 20% → MEDIUM
        inp = make_input(weighted_pipeline=800_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.gap_severity == GapSeverity.MEDIUM

    def test_gap_between_20_and_40pct_is_medium(self, engine):
        # gap = 300_000 → pct = 30%
        inp = make_input(weighted_pipeline=700_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.gap_severity == GapSeverity.MEDIUM

    def test_gap_exactly_40pct_is_high(self, engine):
        # gap = 400_000 → pct = 40%
        inp = make_input(weighted_pipeline=600_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.gap_severity == GapSeverity.HIGH

    def test_gap_between_40_and_60pct_is_high(self, engine):
        # gap = 500_000 → pct = 50%
        inp = make_input(weighted_pipeline=500_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.gap_severity == GapSeverity.HIGH

    def test_gap_exactly_60pct_is_critical(self, engine):
        # gap = 600_000 → pct = 60%
        inp = make_input(weighted_pipeline=400_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.gap_severity == GapSeverity.CRITICAL

    def test_gap_above_60pct_is_critical(self, engine):
        # gap = 800_000 → pct = 80%
        inp = make_input(weighted_pipeline=200_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.gap_severity == GapSeverity.CRITICAL

    def test_gap_100pct_is_critical(self, engine):
        inp = make_input(weighted_pipeline=0, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.gap_severity == GapSeverity.CRITICAL

    def test_gap_zero_quota_is_none(self, engine):
        # quota_remaining = 0 → gap = max(0, 0-500000) = 0 → NONE
        inp = make_input(weighted_pipeline=500_000, quota_remaining=0)
        result = engine.analyze(inp)
        assert result.gap_severity == GapSeverity.NONE

    def test_gap_just_above_zero_low(self, engine):
        # gap = 10_000 → pct = 1% → LOW
        inp = make_input(weighted_pipeline=990_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.gap_severity == GapSeverity.LOW


# ===========================================================================
# 16. _pipeline_quality thresholds
# ===========================================================================

class TestPipelineQualityThresholds:
    def _make_quality(self, score: float, engine) -> PipelineCoverageResult:
        """Drive quality score to an approximate target by tuning inputs."""
        # quality = health*0.4 + win_rate*0.3 - stall_penalty - competitive_penalty
        # We control health and win_rate, zero out penalties
        # score ≈ health*0.4 + win*0.3 with stall=0, competitive=0
        # set health = win = score / 0.7
        pct = min(100.0, score / 0.7)
        inp = make_input(
            avg_deal_health=pct,
            historical_win_rate=pct,
            stalled_deal_count=0,
            competitive_deal_pct=0,
        )
        return engine.analyze(inp)

    def test_quality_75_or_above_is_excellent(self, engine):
        # health=100, win=100 → 40+30=70 → clamp... need to find score >=75
        # Use health=100, win=100 → 70 max, can't reach 75 without >100 input
        # Actually max quality = 100*0.4 + 100*0.3 = 70 with zero penalties
        # Hmm, but score is clamped to [0,100]. Let's verify the threshold by
        # directly calling _pipeline_quality
        eng = PipelineCoverageEngine()
        assert eng._pipeline_quality(75.0) == PipelineQuality.EXCELLENT
        assert eng._pipeline_quality(100.0) == PipelineQuality.EXCELLENT
        assert eng._pipeline_quality(90.0) == PipelineQuality.EXCELLENT

    def test_quality_74_is_good(self, engine):
        eng = PipelineCoverageEngine()
        assert eng._pipeline_quality(74.9) == PipelineQuality.GOOD

    def test_quality_55_is_good(self, engine):
        eng = PipelineCoverageEngine()
        assert eng._pipeline_quality(55.0) == PipelineQuality.GOOD

    def test_quality_54_is_fair(self, engine):
        eng = PipelineCoverageEngine()
        assert eng._pipeline_quality(54.9) == PipelineQuality.FAIR

    def test_quality_35_is_fair(self, engine):
        eng = PipelineCoverageEngine()
        assert eng._pipeline_quality(35.0) == PipelineQuality.FAIR

    def test_quality_34_is_poor(self, engine):
        eng = PipelineCoverageEngine()
        assert eng._pipeline_quality(34.9) == PipelineQuality.POOR

    def test_quality_0_is_poor(self, engine):
        eng = PipelineCoverageEngine()
        assert eng._pipeline_quality(0.0) == PipelineQuality.POOR

    def test_quality_exactly_75_is_excellent(self, engine):
        eng = PipelineCoverageEngine()
        assert eng._pipeline_quality(75.0) == PipelineQuality.EXCELLENT

    def test_quality_exactly_55_is_good(self, engine):
        eng = PipelineCoverageEngine()
        assert eng._pipeline_quality(55.0) == PipelineQuality.GOOD

    def test_quality_exactly_35_is_fair(self, engine):
        eng = PipelineCoverageEngine()
        assert eng._pipeline_quality(35.0) == PipelineQuality.FAIR

    def test_quality_below_35_is_poor(self, engine):
        eng = PipelineCoverageEngine()
        assert eng._pipeline_quality(10.0) == PipelineQuality.POOR


# ===========================================================================
# 17. is_at_risk
# ===========================================================================

class TestIsAtRisk:
    def test_at_risk_when_weighted_coverage_below_1(self, engine):
        # weighted_pipeline < quota_remaining → w_coverage < 1 → at_risk
        inp = make_input(weighted_pipeline=500_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.is_at_risk is True

    def test_not_at_risk_when_weighted_coverage_equals_1(self, engine):
        # w_coverage = 1.0, gap = 0 → at_risk depends on gap_severity
        inp = make_input(weighted_pipeline=1_000_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        # gap = 0 → NONE → not high/critical → is_at_risk = False if w_coverage >= 1
        assert result.is_at_risk is False

    def test_at_risk_when_gap_severity_high(self, engine):
        # Force HIGH gap: gap = 400k → 40% of 1M
        inp = make_input(weighted_pipeline=600_000, quota_remaining=1_000_000,
                         current_pipeline=3_500_000)  # high coverage ratio so not critical_gap status
        result = engine.analyze(inp)
        assert result.gap_severity == GapSeverity.HIGH
        assert result.is_at_risk is True

    def test_at_risk_when_gap_severity_critical(self, engine):
        inp = make_input(weighted_pipeline=200_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.gap_severity == GapSeverity.CRITICAL
        assert result.is_at_risk is True

    def test_not_at_risk_when_well_covered_no_gap(self, engine):
        inp = make_input(
            weighted_pipeline=3_000_000,
            current_pipeline=3_500_000,
            quota_remaining=1_000_000,
        )
        result = engine.analyze(inp)
        assert result.is_at_risk is False

    def test_at_risk_when_weighted_coverage_zero(self, engine):
        inp = make_input(weighted_pipeline=0, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.is_at_risk is True

    def test_at_risk_medium_gap_but_covered(self, engine):
        # w_coverage >= 1 and gap_severity = MEDIUM → not at risk
        inp = make_input(weighted_pipeline=1_200_000, quota_remaining=1_000_000,
                         current_pipeline=2_500_000)
        result = engine.analyze(inp)
        # gap = 0 (covered), so not at risk
        assert result.is_at_risk is False

    def test_is_at_risk_type_bool(self, engine, adequate_input):
        result = engine.analyze(adequate_input)
        assert isinstance(result.is_at_risk, bool)


# ===========================================================================
# 18. needs_intervention
# ===========================================================================

class TestNeedsIntervention:
    def test_needs_intervention_when_critical_gap_status(self, engine):
        inp = make_input(current_pipeline=500_000, quota_remaining=1_000_000,
                         weighted_pipeline=500_000)
        result = engine.analyze(inp)
        assert result.coverage_status == CoverageStatus.CRITICAL_GAP
        assert result.needs_intervention is True

    def test_needs_intervention_when_gap_severity_critical(self, engine):
        # gap = 700k → 70% → CRITICAL severity
        inp = make_input(weighted_pipeline=300_000, quota_remaining=1_000_000,
                         current_pipeline=3_500_000)  # high ratio to avoid critical_gap status
        result = engine.analyze(inp)
        assert result.gap_severity == GapSeverity.CRITICAL
        assert result.needs_intervention is True

    def test_no_intervention_when_adequate_no_critical_gap(self, engine):
        inp = make_input(
            current_pipeline=2_000_000,
            weighted_pipeline=2_000_000,
            quota_remaining=1_000_000,
        )
        result = engine.analyze(inp)
        assert result.needs_intervention is False

    def test_no_intervention_when_over_covered(self, engine, over_covered_input):
        result = engine.analyze(over_covered_input)
        assert result.needs_intervention is False

    def test_no_intervention_when_under_covered_but_not_critical_gap(self, engine):
        # coverage = 1.5 → UNDER_COVERED; gap = 500k → gap_sev = HIGH (not CRITICAL)
        inp = make_input(
            current_pipeline=1_500_000,
            weighted_pipeline=500_000,
            quota_remaining=1_000_000,
        )
        result = engine.analyze(inp)
        # gap = 500_000 → pct = 50% → HIGH, not CRITICAL; status != CRITICAL_GAP
        assert result.needs_intervention is False

    def test_needs_intervention_type_bool(self, engine, adequate_input):
        result = engine.analyze(adequate_input)
        assert isinstance(result.needs_intervention, bool)

    def test_intervention_with_zero_pipeline_high_quota(self, engine):
        inp = make_input(
            current_pipeline=0,
            weighted_pipeline=0,
            quota_remaining=1_000_000,
            stage1_value=0, stage2_value=0, stage3_value=0,
            stage4_value=0, stage5_value=0,
        )
        result = engine.analyze(inp)
        assert result.needs_intervention is True


# ===========================================================================
# 19. Properties: at_risk_teams, intervention_teams, healthy_teams, total_gap_to_quota
# ===========================================================================

class TestProperties:
    def test_at_risk_teams_empty_initially(self, engine):
        assert engine.at_risk_teams == []

    def test_intervention_teams_empty_initially(self, engine):
        assert engine.intervention_teams == []

    def test_healthy_teams_empty_initially(self, engine):
        assert engine.healthy_teams == []

    def test_total_gap_to_quota_zero_initially(self, engine):
        assert engine.total_gap_to_quota == 0.0

    def test_at_risk_teams_populated(self, engine, critical_gap_input):
        engine.analyze(critical_gap_input)
        assert len(engine.at_risk_teams) >= 1

    def test_intervention_teams_populated(self, engine, critical_gap_input):
        engine.analyze(critical_gap_input)
        assert len(engine.intervention_teams) >= 1

    def test_healthy_teams_populated(self, engine, over_covered_input):
        engine.analyze(over_covered_input)
        assert len(engine.healthy_teams) >= 1

    def test_healthy_teams_adequate(self, engine, adequate_input):
        engine.analyze(adequate_input)
        assert len(engine.healthy_teams) >= 1

    def test_healthy_teams_excludes_under_covered(self, engine, under_covered_input):
        engine.analyze(under_covered_input)
        healthy = engine.healthy_teams
        for t in healthy:
            assert t.coverage_status in (CoverageStatus.OVER_COVERED, CoverageStatus.ADEQUATE)

    def test_total_gap_to_quota_accumulated(self, engine):
        inp1 = make_input(weighted_pipeline=600_000, quota_remaining=1_000_000)  # gap=400k
        inp2 = make_input(weighted_pipeline=700_000, quota_remaining=1_000_000)  # gap=300k
        engine.analyze(inp1)
        engine.analyze(inp2)
        assert engine.total_gap_to_quota == pytest.approx(700_000.0)

    def test_total_gap_to_quota_zero_when_covered(self, engine, over_covered_input):
        engine.analyze(over_covered_input)
        assert engine.total_gap_to_quota == 0.0

    def test_at_risk_teams_list_type(self, engine, adequate_input):
        engine.analyze(adequate_input)
        assert isinstance(engine.at_risk_teams, list)

    def test_intervention_teams_list_type(self, engine, adequate_input):
        engine.analyze(adequate_input)
        assert isinstance(engine.intervention_teams, list)

    def test_healthy_teams_list_type(self, engine, adequate_input):
        engine.analyze(adequate_input)
        assert isinstance(engine.healthy_teams, list)

    def test_at_risk_teams_all_have_is_at_risk_true(self, engine):
        for _ in range(3):
            engine.analyze(make_input(weighted_pipeline=500_000, quota_remaining=1_000_000))
        for t in engine.at_risk_teams:
            assert t.is_at_risk is True

    def test_intervention_teams_all_have_needs_intervention_true(self, engine):
        for _ in range(3):
            engine.analyze(make_input(weighted_pipeline=0, quota_remaining=1_000_000,
                                      current_pipeline=0, stage1_value=0, stage2_value=0,
                                      stage3_value=0, stage4_value=0, stage5_value=0))
        for t in engine.intervention_teams:
            assert t.needs_intervention is True

    def test_total_gap_rounded_to_2dp(self, engine):
        inp = make_input(weighted_pipeline=666_666, quota_remaining=1_000_000)
        engine.analyze(inp)
        # just check it's a float rounded to 2dp
        val = engine.total_gap_to_quota
        assert val == round(val, 2)


# ===========================================================================
# 20. analyze_batch() and reset()
# ===========================================================================

class TestAnalyzeBatchAndReset:
    def test_analyze_batch_returns_list(self, engine):
        inputs = [make_input(team_id=f"T{i}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        assert isinstance(results, list)

    def test_analyze_batch_length_matches_input(self, engine):
        inputs = [make_input(team_id=f"T{i}") for i in range(5)]
        results = engine.analyze_batch(inputs)
        assert len(results) == 5

    def test_analyze_batch_returns_result_objects(self, engine):
        inputs = [make_input(team_id=f"T{i}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        for r in results:
            assert isinstance(r, PipelineCoverageResult)

    def test_analyze_batch_accumulates_results(self, engine):
        inputs = [make_input(team_id=f"T{i}") for i in range(4)]
        engine.analyze_batch(inputs)
        assert len(engine._results) == 4

    def test_analyze_batch_empty_input(self, engine):
        results = engine.analyze_batch([])
        assert results == []

    def test_analyze_batch_team_ids_preserved(self, engine):
        inputs = [make_input(team_id=f"TEAM_{i}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        ids = [r.team_id for r in results]
        assert ids == ["TEAM_0", "TEAM_1", "TEAM_2"]

    def test_analyze_batch_single_item(self, engine, adequate_input):
        results = engine.analyze_batch([adequate_input])
        assert len(results) == 1

    def test_reset_clears_results(self, engine, adequate_input):
        engine.analyze(adequate_input)
        engine.analyze(adequate_input)
        engine.reset()
        assert len(engine._results) == 0

    def test_reset_clears_at_risk_teams(self, engine, critical_gap_input):
        engine.analyze(critical_gap_input)
        engine.reset()
        assert engine.at_risk_teams == []

    def test_reset_clears_intervention_teams(self, engine, critical_gap_input):
        engine.analyze(critical_gap_input)
        engine.reset()
        assert engine.intervention_teams == []

    def test_reset_clears_healthy_teams(self, engine, over_covered_input):
        engine.analyze(over_covered_input)
        engine.reset()
        assert engine.healthy_teams == []

    def test_reset_resets_total_gap(self, engine, critical_gap_input):
        engine.analyze(critical_gap_input)
        engine.reset()
        assert engine.total_gap_to_quota == 0.0

    def test_reset_allows_fresh_analysis(self, engine, adequate_input):
        engine.analyze(adequate_input)
        engine.reset()
        engine.analyze(adequate_input)
        assert len(engine._results) == 1

    def test_analyze_batch_after_reset(self, engine):
        inputs = [make_input(team_id=f"T{i}") for i in range(3)]
        engine.analyze_batch(inputs)
        engine.reset()
        engine.analyze_batch(inputs)
        assert len(engine._results) == 3

    def test_double_reset_is_safe(self, engine, adequate_input):
        engine.analyze(adequate_input)
        engine.reset()
        engine.reset()
        assert len(engine._results) == 0

    def test_analyze_batch_different_statuses(self, engine):
        inputs = [
            make_input(team_id="OVER", current_pipeline=3_500_000, quota_remaining=1_000_000),
            make_input(team_id="ADQ", current_pipeline=2_000_000, quota_remaining=1_000_000),
            make_input(team_id="CRIT", current_pipeline=500_000, quota_remaining=1_000_000),
        ]
        results = engine.analyze_batch(inputs)
        statuses = {r.team_id: r.coverage_status for r in results}
        assert statuses["OVER"] == CoverageStatus.OVER_COVERED
        assert statuses["ADQ"] == CoverageStatus.ADEQUATE
        assert statuses["CRIT"] == CoverageStatus.CRITICAL_GAP


# ===========================================================================
# 21. Edge cases
# ===========================================================================

class TestEdgeCases:
    def test_quota_remaining_zero_coverage_ratio(self, engine):
        inp = make_input(quota_remaining=0, current_pipeline=1_000_000)
        result = engine.analyze(inp)
        assert result.coverage_ratio == 0.0

    def test_quota_remaining_zero_weighted_coverage_ratio(self, engine):
        inp = make_input(quota_remaining=0, weighted_pipeline=1_000_000)
        result = engine.analyze(inp)
        assert result.weighted_coverage_ratio == 0.0

    def test_quota_remaining_zero_gap_to_quota_zero(self, engine):
        # max(0, 0 - 1_000_000) = 0
        inp = make_input(quota_remaining=0, weighted_pipeline=1_000_000)
        result = engine.analyze(inp)
        assert result.gap_to_quota == 0.0

    def test_quota_remaining_zero_trend_zero(self, engine):
        inp = make_input(quota_remaining=0, pipeline_added_qtd=500_000, churned_pipeline_qtd=100_000)
        result = engine.analyze(inp)
        assert result.coverage_trend == 0.0

    def test_all_pipeline_in_stage5(self, engine):
        inp = make_input(
            current_pipeline=1_000_000,
            stage1_value=0, stage2_value=0, stage3_value=0,
            stage4_value=0, stage5_value=1_000_000,
        )
        result = engine.analyze(inp)
        assert result.stage_mix_score == pytest.approx(60.0)

    def test_all_pipeline_in_stage4(self, engine):
        inp = make_input(
            current_pipeline=1_000_000,
            stage1_value=0, stage2_value=0, stage3_value=0,
            stage4_value=1_000_000, stage5_value=0,
        )
        result = engine.analyze(inp)
        assert result.stage_mix_score == pytest.approx(60.0)

    def test_all_pipeline_in_stage1(self, engine):
        inp = make_input(
            current_pipeline=1_000_000,
            stage1_value=1_000_000, stage2_value=0, stage3_value=0,
            stage4_value=0, stage5_value=0,
        )
        result = engine.analyze(inp)
        assert result.stage_mix_score == pytest.approx(10.0)

    def test_all_pipeline_in_stage2(self, engine):
        inp = make_input(
            current_pipeline=1_000_000,
            stage1_value=0, stage2_value=1_000_000, stage3_value=0,
            stage4_value=0, stage5_value=0,
        )
        result = engine.analyze(inp)
        assert result.stage_mix_score == pytest.approx(10.0)

    def test_all_pipeline_in_stage3(self, engine):
        inp = make_input(
            current_pipeline=1_000_000,
            stage1_value=0, stage2_value=0, stage3_value=1_000_000,
            stage4_value=0, stage5_value=0,
        )
        result = engine.analyze(inp)
        assert result.stage_mix_score == pytest.approx(30.0)

    def test_zero_stalled_deals(self, engine):
        inp = make_input(stalled_deal_count=0, current_pipeline=1_000_000, avg_deal_size=100_000)
        result = engine.analyze(inp)
        # stall_rate = 0 → no penalty
        assert result.quality_score >= 0.0

    def test_100_percent_competitive_penalty_capped(self, engine):
        inp = make_input(competitive_deal_pct=100, avg_deal_health=80, historical_win_rate=60, stalled_deal_count=0)
        expected_penalty = min(10.0, 100 * 0.10)
        base = 80 * 0.40 + 60 * 0.30
        expected = round(max(0.0, min(100.0, base - expected_penalty)), 1)
        result = engine.analyze(inp)
        assert result.quality_score == pytest.approx(expected)

    def test_very_large_values(self, engine):
        inp = make_input(
            current_pipeline=1e12,
            weighted_pipeline=1e12,
            quota_remaining=1e11,
        )
        result = engine.analyze(inp)
        assert result.coverage_ratio > 0

    def test_very_small_pipeline(self, engine):
        inp = make_input(
            current_pipeline=1.0,
            weighted_pipeline=1.0,
            quota_remaining=1_000_000,
        )
        result = engine.analyze(inp)
        assert result.coverage_ratio < 1.0
        assert result.coverage_status == CoverageStatus.CRITICAL_GAP

    def test_avg_deal_size_zero_no_crash(self, engine):
        # avg_deal_size=0 → total_deals = max(1, pipeline/max(1,0)) = max(1, pipeline/1)
        inp = make_input(avg_deal_size=0, current_pipeline=1_000_000, stalled_deal_count=2)
        result = engine.analyze(inp)
        assert result.quality_score >= 0.0

    def test_days_remaining_zero_velocity(self, engine):
        inp = make_input(days_remaining=0)
        result = engine.analyze(inp)
        assert result.pipeline_velocity == 0.0

    def test_no_pipeline_added_qtd(self, engine):
        inp = make_input(pipeline_added_qtd=0, churned_pipeline_qtd=0)
        result = engine.analyze(inp)
        assert result.pipeline_velocity == 0.0
        assert result.coverage_trend == 0.0


# ===========================================================================
# 22. CoverageAction logic
# ===========================================================================

class TestCoverageAction:
    def test_critical_gap_generates_pipeline(self, engine):
        inp = make_input(current_pipeline=500_000, quota_remaining=1_000_000,
                         weighted_pipeline=300_000)
        result = engine.analyze(inp)
        assert result.coverage_status == CoverageStatus.CRITICAL_GAP
        assert result.coverage_action == CoverageAction.GENERATE_PIPELINE

    def test_high_gap_low_velocity_reallocate(self, engine):
        # gap_severity HIGH, velocity < 1000
        inp = make_input(
            current_pipeline=3_500_000,  # OVER_COVERED status
            weighted_pipeline=600_000,   # gap = 400k → 40% → HIGH
            quota_remaining=1_000_000,
            pipeline_added_qtd=100,      # low velocity
            avg_sales_cycle_days=90,
            days_remaining=30,
        )
        result = engine.analyze(inp)
        assert result.gap_severity == GapSeverity.HIGH
        assert result.coverage_action == CoverageAction.REALLOCATE

    def test_high_gap_high_velocity_generate_pipeline(self, engine):
        # gap_severity HIGH, velocity >= 1000
        inp = make_input(
            current_pipeline=3_500_000,
            weighted_pipeline=600_000,
            quota_remaining=1_000_000,
            pipeline_added_qtd=100_000_000,  # very high → velocity > 1000
            avg_sales_cycle_days=90,
            days_remaining=30,
        )
        result = engine.analyze(inp)
        assert result.gap_severity == GapSeverity.HIGH
        assert result.coverage_action == CoverageAction.GENERATE_PIPELINE

    def test_under_covered_poor_quality_accelerate(self, engine):
        # status = UNDER_COVERED, quality < 50
        inp = make_input(
            current_pipeline=1_500_000,
            weighted_pipeline=1_500_000,
            quota_remaining=1_000_000,
            avg_deal_health=0,
            historical_win_rate=0,
            stalled_deal_count=100,
            competitive_deal_pct=100,
        )
        result = engine.analyze(inp)
        assert result.coverage_status == CoverageStatus.UNDER_COVERED
        assert result.quality_score < 50
        assert result.coverage_action == CoverageAction.ACCELERATE_EXISTING

    def test_adequate_status_maintain(self, engine):
        inp = make_input(
            current_pipeline=2_000_000,
            weighted_pipeline=2_000_000,
            quota_remaining=1_000_000,
            avg_deal_health=75,
            historical_win_rate=50,
            stalled_deal_count=0,
            competitive_deal_pct=0,
        )
        result = engine.analyze(inp)
        assert result.coverage_status == CoverageStatus.ADEQUATE
        assert result.coverage_action == CoverageAction.MAINTAIN

    def test_over_covered_small_deals_expand_upmarket(self, engine):
        # status = OVER_COVERED, avg_deal_size < quota_remaining * 0.05
        inp = make_input(
            current_pipeline=4_000_000,
            weighted_pipeline=4_000_000,
            quota_remaining=1_000_000,
            avg_deal_size=40_000,   # 40k < 1M * 0.05 = 50k
        )
        result = engine.analyze(inp)
        assert result.coverage_status == CoverageStatus.OVER_COVERED
        assert result.coverage_action == CoverageAction.EXPAND_UPMARKET

    def test_low_quality_strategic_review(self, engine):
        # status not CRITICAL_GAP, gap_sev not HIGH/CRITICAL
        # status UNDER_COVERED, quality >= 50 but then quality < 40 path needs status != UNDER_COVERED with quality<50 branch
        # Make OVER_COVERED with large deal size (no expand) and quality < 40
        inp = make_input(
            current_pipeline=4_000_000,
            weighted_pipeline=4_000_000,
            quota_remaining=1_000_000,
            avg_deal_size=100_000,   # 100k >= 1M * 0.05 = 50k → no expand_upmarket
            avg_deal_health=0,
            historical_win_rate=0,
            stalled_deal_count=100,
            competitive_deal_pct=100,
        )
        result = engine.analyze(inp)
        assert result.quality_score < 40
        assert result.coverage_action == CoverageAction.STRATEGIC_REVIEW

    def test_critical_gap_action_string_value(self, engine, critical_gap_input):
        result = engine.analyze(critical_gap_input)
        assert result.to_dict()["coverage_action"] == "generate_pipeline"

    def test_maintain_string_value(self, engine, adequate_input):
        result = engine.analyze(adequate_input)
        d = result.to_dict()
        assert d["coverage_action"] in {a.value for a in CoverageAction}


# ===========================================================================
# 23. PipelineCoverageResult dataclass fields
# ===========================================================================

class TestResultDataclass:
    def test_result_has_team_id(self, engine, adequate_input):
        result = engine.analyze(adequate_input)
        assert hasattr(result, "team_id")

    def test_result_has_region(self, engine, adequate_input):
        result = engine.analyze(adequate_input)
        assert hasattr(result, "region")

    def test_result_has_coverage_status(self, engine, adequate_input):
        result = engine.analyze(adequate_input)
        assert hasattr(result, "coverage_status")

    def test_result_has_gap_severity(self, engine, adequate_input):
        result = engine.analyze(adequate_input)
        assert hasattr(result, "gap_severity")

    def test_result_has_pipeline_quality(self, engine, adequate_input):
        result = engine.analyze(adequate_input)
        assert hasattr(result, "pipeline_quality")

    def test_result_has_coverage_action(self, engine, adequate_input):
        result = engine.analyze(adequate_input)
        assert hasattr(result, "coverage_action")

    def test_result_coverage_status_type(self, engine, adequate_input):
        result = engine.analyze(adequate_input)
        assert isinstance(result.coverage_status, CoverageStatus)

    def test_result_gap_severity_type(self, engine, adequate_input):
        result = engine.analyze(adequate_input)
        assert isinstance(result.gap_severity, GapSeverity)

    def test_result_pipeline_quality_type(self, engine, adequate_input):
        result = engine.analyze(adequate_input)
        assert isinstance(result.pipeline_quality, PipelineQuality)

    def test_result_coverage_action_type(self, engine, adequate_input):
        result = engine.analyze(adequate_input)
        assert isinstance(result.coverage_action, CoverageAction)

    def test_result_coverage_ratio_float(self, engine, adequate_input):
        result = engine.analyze(adequate_input)
        assert isinstance(result.coverage_ratio, float)

    def test_result_gap_to_quota_non_negative(self, engine, adequate_input):
        result = engine.analyze(adequate_input)
        assert result.gap_to_quota >= 0.0

    def test_result_quality_score_in_range(self, engine, adequate_input):
        result = engine.analyze(adequate_input)
        assert 0.0 <= result.quality_score <= 100.0

    def test_result_stage_mix_score_in_range(self, engine, adequate_input):
        result = engine.analyze(adequate_input)
        assert 0.0 <= result.stage_mix_score <= 100.0

    def test_result_stored_in_engine(self, engine, adequate_input):
        result = engine.analyze(adequate_input)
        assert result in engine._results


# ===========================================================================
# 24. Engine initialization
# ===========================================================================

class TestEngineInit:
    def test_engine_creates_empty_results(self):
        eng = PipelineCoverageEngine()
        assert eng._results == []

    def test_engine_multiple_instances_independent(self):
        eng1 = PipelineCoverageEngine()
        eng2 = PipelineCoverageEngine()
        eng1.analyze(make_input(team_id="T1"))
        assert len(eng1._results) == 1
        assert len(eng2._results) == 0

    def test_analyze_returns_result_object(self, engine, adequate_input):
        result = engine.analyze(adequate_input)
        assert isinstance(result, PipelineCoverageResult)

    def test_analyze_accumulates_across_calls(self, engine, adequate_input):
        engine.analyze(adequate_input)
        engine.analyze(adequate_input)
        engine.analyze(adequate_input)
        assert len(engine._results) == 3


# ===========================================================================
# 25. Additional boundary & integration tests
# ===========================================================================

class TestBoundaryAndIntegration:
    def test_coverage_status_exactly_at_boundary_3_5(self, engine):
        eng = PipelineCoverageEngine()
        assert eng._coverage_status(3.5) == CoverageStatus.OVER_COVERED

    def test_coverage_status_just_below_3_5(self, engine):
        eng = PipelineCoverageEngine()
        assert eng._coverage_status(3.499) == CoverageStatus.ADEQUATE

    def test_coverage_status_exactly_at_boundary_2_0(self, engine):
        eng = PipelineCoverageEngine()
        assert eng._coverage_status(2.0) == CoverageStatus.ADEQUATE

    def test_coverage_status_just_below_2_0(self, engine):
        eng = PipelineCoverageEngine()
        assert eng._coverage_status(1.999) == CoverageStatus.UNDER_COVERED

    def test_coverage_status_exactly_at_boundary_1_0(self, engine):
        eng = PipelineCoverageEngine()
        assert eng._coverage_status(1.0) == CoverageStatus.UNDER_COVERED

    def test_coverage_status_just_below_1_0(self, engine):
        eng = PipelineCoverageEngine()
        assert eng._coverage_status(0.999) == CoverageStatus.CRITICAL_GAP

    def test_coverage_status_zero(self, engine):
        eng = PipelineCoverageEngine()
        assert eng._coverage_status(0.0) == CoverageStatus.CRITICAL_GAP

    def test_gap_severity_boundary_20_pct(self, engine):
        eng = PipelineCoverageEngine()
        inp = make_input(weighted_pipeline=800_000, quota_remaining=1_000_000)
        # gap = 200k → pct = 20 → MEDIUM
        gap = eng._gap_to_quota(inp)
        sev = eng._gap_severity(gap, inp)
        assert sev == GapSeverity.MEDIUM

    def test_gap_severity_boundary_40_pct(self, engine):
        eng = PipelineCoverageEngine()
        inp = make_input(weighted_pipeline=600_000, quota_remaining=1_000_000)
        gap = eng._gap_to_quota(inp)
        sev = eng._gap_severity(gap, inp)
        assert sev == GapSeverity.HIGH

    def test_gap_severity_boundary_60_pct(self, engine):
        eng = PipelineCoverageEngine()
        inp = make_input(weighted_pipeline=400_000, quota_remaining=1_000_000)
        gap = eng._gap_to_quota(inp)
        sev = eng._gap_severity(gap, inp)
        assert sev == GapSeverity.CRITICAL

    def test_pipeline_quality_boundary_75(self, engine):
        eng = PipelineCoverageEngine()
        assert eng._pipeline_quality(75.0) == PipelineQuality.EXCELLENT
        assert eng._pipeline_quality(74.9) == PipelineQuality.GOOD

    def test_pipeline_quality_boundary_55(self, engine):
        eng = PipelineCoverageEngine()
        assert eng._pipeline_quality(55.0) == PipelineQuality.GOOD
        assert eng._pipeline_quality(54.9) == PipelineQuality.FAIR

    def test_pipeline_quality_boundary_35(self, engine):
        eng = PipelineCoverageEngine()
        assert eng._pipeline_quality(35.0) == PipelineQuality.FAIR
        assert eng._pipeline_quality(34.9) == PipelineQuality.POOR

    def test_full_pipeline_scenario_over_covered(self, engine):
        inp = make_input(
            team_id="OVER",
            current_pipeline=4_000_000,
            weighted_pipeline=4_000_000,
            quota_remaining=1_000_000,
        )
        r = engine.analyze(inp)
        assert r.coverage_status == CoverageStatus.OVER_COVERED
        assert r.gap_to_quota == 0.0
        assert r.gap_severity == GapSeverity.NONE

    def test_full_pipeline_scenario_critical(self, engine):
        inp = make_input(
            team_id="CRIT",
            current_pipeline=100_000,
            weighted_pipeline=100_000,
            quota_remaining=1_000_000,
        )
        r = engine.analyze(inp)
        assert r.coverage_status == CoverageStatus.CRITICAL_GAP
        assert r.needs_intervention is True
        assert r.is_at_risk is True

    def test_multiple_teams_summary_total(self, engine):
        for i in range(10):
            engine.analyze(make_input(team_id=f"T{i}"))
        assert engine.summary()["total"] == 10

    def test_stage_mix_score_with_no_pipeline(self, engine):
        inp = make_input(
            current_pipeline=0,
            stage1_value=0, stage2_value=0, stage3_value=0,
            stage4_value=0, stage5_value=0,
        )
        result = engine.analyze(inp)
        assert result.stage_mix_score == 0.0

    def test_weighted_coverage_ratio_stored_correctly(self, engine):
        inp = make_input(weighted_pipeline=2_500_000, quota_remaining=1_000_000)
        r = engine.analyze(inp)
        assert r.weighted_coverage_ratio == pytest.approx(2.5)

    def test_coverage_trend_large_churn(self, engine):
        inp = make_input(pipeline_added_qtd=0, churned_pipeline_qtd=1_000_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.coverage_trend == pytest.approx(-100.0)

    def test_summary_avg_coverage_ratio_computation(self, engine):
        # Two teams: ratio 2.0 and 3.0 → avg = 2.5
        inp1 = make_input(team_id="A", current_pipeline=2_000_000, quota_remaining=1_000_000)
        inp2 = make_input(team_id="B", current_pipeline=3_000_000, quota_remaining=1_000_000)
        engine.analyze(inp1)
        engine.analyze(inp2)
        s = engine.summary()
        assert s["avg_coverage_ratio"] == pytest.approx(2.5)

    def test_analyze_result_team_id(self, engine):
        inp = make_input(team_id="TEST123")
        result = engine.analyze(inp)
        assert result.team_id == "TEST123"

    def test_analyze_result_region(self, engine):
        inp = make_input(region="LATAM")
        result = engine.analyze(inp)
        assert result.region == "LATAM"

    def test_gap_severity_none_for_exactly_zero_gap(self, engine):
        inp = make_input(weighted_pipeline=1_000_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.gap_severity == GapSeverity.NONE

    def test_coverage_ratio_below_3_5_above_2_is_adequate(self, engine):
        inp = make_input(current_pipeline=3_000_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.coverage_status == CoverageStatus.ADEQUATE

    def test_quality_score_zero_health_zero_win_rate(self, engine):
        inp = make_input(avg_deal_health=0, historical_win_rate=0, stalled_deal_count=0, competitive_deal_pct=0)
        result = engine.analyze(inp)
        assert result.quality_score == 0.0

    def test_weighted_pipeline_zero_quota_zero_gap(self, engine):
        inp = make_input(weighted_pipeline=0, quota_remaining=0)
        result = engine.analyze(inp)
        # gap = max(0, 0-0) = 0
        assert result.gap_to_quota == 0.0

    def test_velocity_when_cycle_equals_days_remaining(self, engine):
        # elapsed = max(1, 30-30) = 1
        inp = make_input(
            pipeline_added_qtd=5_000,
            avg_sales_cycle_days=30,
            days_remaining=30,
        )
        result = engine.analyze(inp)
        assert result.pipeline_velocity == pytest.approx(5_000.0)

    def test_gap_severity_just_below_60_pct_is_high(self, engine):
        # gap = 599_000 → pct = 59.9% → HIGH
        inp = make_input(weighted_pipeline=401_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.gap_severity == GapSeverity.HIGH

    def test_gap_severity_just_below_40_pct_is_medium(self, engine):
        # gap = 399_000 → pct = 39.9% → MEDIUM
        inp = make_input(weighted_pipeline=601_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.gap_severity == GapSeverity.MEDIUM

    def test_gap_severity_just_below_20_pct_is_low(self, engine):
        # gap = 199_000 → pct = 19.9% → LOW
        inp = make_input(weighted_pipeline=801_000, quota_remaining=1_000_000)
        result = engine.analyze(inp)
        assert result.gap_severity == GapSeverity.LOW

    def test_healthy_teams_count_over_covered(self, engine):
        for i in range(3):
            engine.analyze(make_input(team_id=f"OC{i}", current_pipeline=4_000_000, quota_remaining=1_000_000))
        assert len(engine.healthy_teams) == 3

    def test_healthy_teams_count_mixed(self, engine):
        engine.analyze(make_input(team_id="OC", current_pipeline=4_000_000, quota_remaining=1_000_000))
        engine.analyze(make_input(team_id="AQ", current_pipeline=2_000_000, quota_remaining=1_000_000))
        engine.analyze(make_input(team_id="UC", current_pipeline=1_500_000, quota_remaining=1_000_000))
        engine.analyze(make_input(team_id="CG", current_pipeline=500_000, quota_remaining=1_000_000))
        assert len(engine.healthy_teams) == 2

    def test_summary_status_counts_sum_to_total(self, engine):
        for i in range(5):
            engine.analyze(make_input(team_id=f"T{i}"))
        s = engine.summary()
        assert sum(s["status_counts"].values()) == s["total"]

    def test_summary_gap_severity_counts_sum_to_total(self, engine):
        for i in range(5):
            engine.analyze(make_input(team_id=f"T{i}"))
        s = engine.summary()
        assert sum(s["gap_severity_counts"].values()) == s["total"]

    def test_summary_quality_counts_sum_to_total(self, engine):
        for i in range(5):
            engine.analyze(make_input(team_id=f"T{i}"))
        s = engine.summary()
        assert sum(s["quality_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_to_total(self, engine):
        for i in range(5):
            engine.analyze(make_input(team_id=f"T{i}"))
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]
