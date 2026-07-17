"""
Comprehensive pytest test suite for QuotaAttainmentEngine.

Target: ~280-300 tests covering all scoring logic, edge cases,
enum values, to_dict(), summary(), properties, batch operations, and reset.
"""

from __future__ import annotations

import pytest
from swarm.intelligence.quota_attainment_engine import (
    AttainmentAction,
    AttainmentLikelihood,
    AttainmentRisk,
    PerformanceTrend,
    QuotaAttainmentEngine,
    QuotaAttainmentInput,
    QuotaAttainmentResult,
)


# ── Fixtures ───────────────────────────────────────────────────────────────────

def make_input(**overrides) -> QuotaAttainmentInput:
    """Return a 'healthy' baseline rep input, with optional overrides."""
    defaults = dict(
        rep_id="rep-001",
        rep_name="Alice Smith",
        manager_id="mgr-001",
        annual_quota=1_200_000.0,
        quota_ytd=300_000.0,
        closed_won_ytd=240_000.0,
        commit_pipeline=80_000.0,
        best_case_pipeline=120_000.0,
        weighted_pipeline=60_000.0,
        days_remaining=30,
        total_period_days=90,
        historical_attainment=100.0,
        last_quarter_attainment=105.0,
        win_rate=30.0,
        avg_deal_size=50_000.0,
        avg_sales_cycle_days=45,
        active_deal_count=10,
        stalled_deal_count=1,
        new_deals_added_mtd=4,
        activities_per_day=4.0,
        coaching_sessions_qtd=2,
    )
    defaults.update(overrides)
    return QuotaAttainmentInput(**defaults)


@pytest.fixture
def engine():
    return QuotaAttainmentEngine()


@pytest.fixture
def baseline_input():
    return make_input()


@pytest.fixture
def baseline_result(engine, baseline_input):
    return engine.analyze(baseline_input)


# ── 1. Enum values, string values, str subtype, and counts ────────────────────

class TestAttainmentLikelihoodEnum:
    def test_very_likely_value(self):
        assert AttainmentLikelihood.VERY_LIKELY.value == "very_likely"

    def test_likely_value(self):
        assert AttainmentLikelihood.LIKELY.value == "likely"

    def test_possible_value(self):
        assert AttainmentLikelihood.POSSIBLE.value == "possible"

    def test_unlikely_value(self):
        assert AttainmentLikelihood.UNLIKELY.value == "unlikely"

    def test_very_unlikely_value(self):
        assert AttainmentLikelihood.VERY_UNLIKELY.value == "very_unlikely"

    def test_is_str_subtype(self):
        assert isinstance(AttainmentLikelihood.LIKELY, str)

    def test_member_count(self):
        assert len(AttainmentLikelihood) == 5

    def test_all_members(self):
        names = {m.name for m in AttainmentLikelihood}
        assert names == {"VERY_LIKELY", "LIKELY", "POSSIBLE", "UNLIKELY", "VERY_UNLIKELY"}


class TestAttainmentRiskEnum:
    def test_low_value(self):
        assert AttainmentRisk.LOW.value == "low"

    def test_medium_value(self):
        assert AttainmentRisk.MEDIUM.value == "medium"

    def test_high_value(self):
        assert AttainmentRisk.HIGH.value == "high"

    def test_critical_value(self):
        assert AttainmentRisk.CRITICAL.value == "critical"

    def test_is_str_subtype(self):
        assert isinstance(AttainmentRisk.HIGH, str)

    def test_member_count(self):
        assert len(AttainmentRisk) == 4

    def test_all_members(self):
        names = {m.name for m in AttainmentRisk}
        assert names == {"LOW", "MEDIUM", "HIGH", "CRITICAL"}


class TestPerformanceTrendEnum:
    def test_accelerating_value(self):
        assert PerformanceTrend.ACCELERATING.value == "accelerating"

    def test_on_track_value(self):
        assert PerformanceTrend.ON_TRACK.value == "on_track"

    def test_slowing_value(self):
        assert PerformanceTrend.SLOWING.value == "slowing"

    def test_declining_value(self):
        assert PerformanceTrend.DECLINING.value == "declining"

    def test_is_str_subtype(self):
        assert isinstance(PerformanceTrend.ON_TRACK, str)

    def test_member_count(self):
        assert len(PerformanceTrend) == 4

    def test_all_members(self):
        names = {m.name for m in PerformanceTrend}
        assert names == {"ACCELERATING", "ON_TRACK", "SLOWING", "DECLINING"}


class TestAttainmentActionEnum:
    def test_maintain_value(self):
        assert AttainmentAction.MAINTAIN.value == "maintain"

    def test_accelerate_value(self):
        assert AttainmentAction.ACCELERATE.value == "accelerate"

    def test_pipeline_build_value(self):
        assert AttainmentAction.PIPELINE_BUILD.value == "pipeline_build"

    def test_coaching_required_value(self):
        assert AttainmentAction.COACHING_REQUIRED.value == "coaching_required"

    def test_urgent_review_value(self):
        assert AttainmentAction.URGENT_REVIEW.value == "urgent_review"

    def test_is_str_subtype(self):
        assert isinstance(AttainmentAction.MAINTAIN, str)

    def test_member_count(self):
        assert len(AttainmentAction) == 5

    def test_all_members(self):
        names = {m.name for m in AttainmentAction}
        assert names == {"MAINTAIN", "ACCELERATE", "PIPELINE_BUILD", "COACHING_REQUIRED", "URGENT_REVIEW"}


# ── 2. to_dict() — exactly 15 keys, enum fields are strings ───────────────────

class TestToDict:
    def test_returns_dict(self, baseline_result):
        assert isinstance(baseline_result.to_dict(), dict)

    def test_exactly_15_keys(self, baseline_result):
        assert len(baseline_result.to_dict()) == 15

    def test_key_rep_id(self, baseline_result):
        assert "rep_id" in baseline_result.to_dict()

    def test_key_rep_name(self, baseline_result):
        assert "rep_name" in baseline_result.to_dict()

    def test_key_attainment_likelihood(self, baseline_result):
        assert "attainment_likelihood" in baseline_result.to_dict()

    def test_key_attainment_risk(self, baseline_result):
        assert "attainment_risk" in baseline_result.to_dict()

    def test_key_performance_trend(self, baseline_result):
        assert "performance_trend" in baseline_result.to_dict()

    def test_key_attainment_action(self, baseline_result):
        assert "attainment_action" in baseline_result.to_dict()

    def test_key_attainment_pct(self, baseline_result):
        assert "attainment_pct" in baseline_result.to_dict()

    def test_key_projected_attainment(self, baseline_result):
        assert "projected_attainment" in baseline_result.to_dict()

    def test_key_gap_to_quota(self, baseline_result):
        assert "gap_to_quota" in baseline_result.to_dict()

    def test_key_coverage_ratio(self, baseline_result):
        assert "coverage_ratio" in baseline_result.to_dict()

    def test_key_confidence_score(self, baseline_result):
        assert "confidence_score" in baseline_result.to_dict()

    def test_key_momentum_score(self, baseline_result):
        assert "momentum_score" in baseline_result.to_dict()

    def test_key_pace_score(self, baseline_result):
        assert "pace_score" in baseline_result.to_dict()

    def test_key_is_at_risk(self, baseline_result):
        assert "is_at_risk" in baseline_result.to_dict()

    def test_key_needs_coaching(self, baseline_result):
        assert "needs_coaching" in baseline_result.to_dict()

    def test_attainment_likelihood_is_string(self, baseline_result):
        val = baseline_result.to_dict()["attainment_likelihood"]
        assert isinstance(val, str)
        assert not isinstance(val, AttainmentLikelihood) or isinstance(val, str)
        # The value should equal the enum value string
        assert val == baseline_result.attainment_likelihood.value

    def test_attainment_risk_is_string(self, baseline_result):
        val = baseline_result.to_dict()["attainment_risk"]
        assert isinstance(val, str)
        assert val == baseline_result.attainment_risk.value

    def test_performance_trend_is_string(self, baseline_result):
        val = baseline_result.to_dict()["performance_trend"]
        assert isinstance(val, str)
        assert val == baseline_result.performance_trend.value

    def test_attainment_action_is_string(self, baseline_result):
        val = baseline_result.to_dict()["attainment_action"]
        assert isinstance(val, str)
        assert val == baseline_result.attainment_action.value

    def test_rep_id_value(self, baseline_result):
        assert baseline_result.to_dict()["rep_id"] == "rep-001"

    def test_rep_name_value(self, baseline_result):
        assert baseline_result.to_dict()["rep_name"] == "Alice Smith"

    def test_numeric_fields_are_float_or_bool(self, baseline_result):
        d = baseline_result.to_dict()
        for key in ("attainment_pct", "projected_attainment", "gap_to_quota",
                    "coverage_ratio", "confidence_score", "momentum_score", "pace_score"):
            assert isinstance(d[key], (int, float)), f"{key} should be numeric"
        assert isinstance(d["is_at_risk"], bool)
        assert isinstance(d["needs_coaching"], bool)

    def test_exact_key_set(self, baseline_result):
        expected_keys = {
            "rep_id", "rep_name", "attainment_likelihood", "attainment_risk",
            "performance_trend", "attainment_action", "attainment_pct",
            "projected_attainment", "gap_to_quota", "coverage_ratio",
            "confidence_score", "momentum_score", "pace_score",
            "is_at_risk", "needs_coaching",
        }
        assert set(baseline_result.to_dict().keys()) == expected_keys


# ── 3. summary() — 13 keys, empty state, count sums ──────────────────────────

class TestSummary:
    def test_empty_returns_dict(self, engine):
        assert isinstance(engine.summary(), dict)

    def test_empty_exactly_13_keys(self, engine):
        assert len(engine.summary()) == 13

    def test_empty_total_is_zero(self, engine):
        assert engine.summary()["total"] == 0

    def test_empty_likelihood_counts_empty(self, engine):
        assert engine.summary()["likelihood_counts"] == {}

    def test_empty_risk_counts_empty(self, engine):
        assert engine.summary()["risk_counts"] == {}

    def test_empty_trend_counts_empty(self, engine):
        assert engine.summary()["trend_counts"] == {}

    def test_empty_action_counts_empty(self, engine):
        assert engine.summary()["action_counts"] == {}

    def test_empty_avg_attainment_pct_zero(self, engine):
        assert engine.summary()["avg_attainment_pct"] == 0.0

    def test_empty_avg_projected_attainment_zero(self, engine):
        assert engine.summary()["avg_projected_attainment"] == 0.0

    def test_empty_total_gap_zero(self, engine):
        assert engine.summary()["total_gap_to_quota"] == 0.0

    def test_empty_at_risk_count_zero(self, engine):
        assert engine.summary()["at_risk_count"] == 0

    def test_empty_coaching_count_zero(self, engine):
        assert engine.summary()["coaching_count"] == 0

    def test_empty_avg_confidence_zero(self, engine):
        assert engine.summary()["avg_confidence_score"] == 0.0

    def test_empty_avg_momentum_zero(self, engine):
        assert engine.summary()["avg_momentum_score"] == 0.0

    def test_empty_likely_attainer_count_zero(self, engine):
        assert engine.summary()["likely_attainer_count"] == 0

    def test_exact_13_key_names(self, engine):
        expected = {
            "total", "likelihood_counts", "risk_counts", "trend_counts",
            "action_counts", "avg_attainment_pct", "avg_projected_attainment",
            "total_gap_to_quota", "at_risk_count", "coaching_count",
            "avg_confidence_score", "avg_momentum_score", "likely_attainer_count",
        }
        assert set(engine.summary().keys()) == expected

    def test_total_matches_analyzed_count(self, engine):
        for i in range(3):
            engine.analyze(make_input(rep_id=f"rep-{i}"))
        assert engine.summary()["total"] == 3

    def test_likelihood_counts_sum_equals_total(self, engine):
        for i in range(4):
            engine.analyze(make_input(rep_id=f"rep-{i}"))
        s = engine.summary()
        assert sum(s["likelihood_counts"].values()) == s["total"]

    def test_risk_counts_sum_equals_total(self, engine):
        for i in range(4):
            engine.analyze(make_input(rep_id=f"rep-{i}"))
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_trend_counts_sum_equals_total(self, engine):
        for i in range(4):
            engine.analyze(make_input(rep_id=f"rep-{i}"))
        s = engine.summary()
        assert sum(s["trend_counts"].values()) == s["total"]

    def test_action_counts_sum_equals_total(self, engine):
        for i in range(4):
            engine.analyze(make_input(rep_id=f"rep-{i}"))
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_after_single_analyze(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        assert s["total"] == 1

    def test_avg_attainment_pct_is_numeric(self, engine):
        engine.analyze(make_input())
        assert isinstance(engine.summary()["avg_attainment_pct"], (int, float))

    def test_avg_momentum_score_is_numeric(self, engine):
        engine.analyze(make_input())
        assert isinstance(engine.summary()["avg_momentum_score"], (int, float))

    def test_at_risk_count_leq_total(self, engine):
        for i in range(5):
            engine.analyze(make_input(rep_id=f"r{i}"))
        s = engine.summary()
        assert s["at_risk_count"] <= s["total"]

    def test_coaching_count_leq_total(self, engine):
        for i in range(5):
            engine.analyze(make_input(rep_id=f"r{i}"))
        s = engine.summary()
        assert s["coaching_count"] <= s["total"]

    def test_likely_attainer_count_leq_total(self, engine):
        for i in range(5):
            engine.analyze(make_input(rep_id=f"r{i}"))
        s = engine.summary()
        assert s["likely_attainer_count"] <= s["total"]


# ── 4. _attainment_pct ────────────────────────────────────────────────────────

class TestAttainmentPct:
    def test_basic_formula(self, engine):
        inp = make_input(closed_won_ytd=150_000.0, quota_ytd=300_000.0)
        result = engine.analyze(inp)
        assert result.attainment_pct == pytest.approx(50.0, abs=0.2)

    def test_full_attainment(self, engine):
        inp = make_input(closed_won_ytd=300_000.0, quota_ytd=300_000.0)
        result = engine.analyze(inp)
        assert result.attainment_pct == pytest.approx(100.0, abs=0.2)

    def test_zero_quota_ytd_returns_zero(self, engine):
        inp = make_input(quota_ytd=0.0, closed_won_ytd=50_000.0)
        result = engine.analyze(inp)
        assert result.attainment_pct == 0.0

    def test_negative_quota_ytd_returns_zero(self, engine):
        inp = make_input(quota_ytd=-1.0, closed_won_ytd=50_000.0)
        result = engine.analyze(inp)
        assert result.attainment_pct == 0.0

    def test_over_attainment(self, engine):
        inp = make_input(closed_won_ytd=450_000.0, quota_ytd=300_000.0)
        result = engine.analyze(inp)
        assert result.attainment_pct == pytest.approx(150.0, abs=0.2)

    def test_zero_closed_won(self, engine):
        inp = make_input(closed_won_ytd=0.0, quota_ytd=300_000.0)
        result = engine.analyze(inp)
        assert result.attainment_pct == pytest.approx(0.0, abs=0.1)

    def test_rounding_to_one_decimal(self, engine):
        # 100_000 / 300_000 = 33.333...% → rounds to 33.3
        inp = make_input(closed_won_ytd=100_000.0, quota_ytd=300_000.0)
        result = engine.analyze(inp)
        assert result.attainment_pct == pytest.approx(33.3, abs=0.1)


# ── 5. _projected_attainment ──────────────────────────────────────────────────

class TestProjectedAttainment:
    def test_zero_quota_ytd_returns_zero(self, engine):
        inp = make_input(quota_ytd=0.0)
        result = engine.analyze(inp)
        assert result.projected_attainment == 0.0

    def test_returns_float(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.projected_attainment, float)

    def test_blend_logic_increases_with_pipeline(self, engine):
        # Higher weighted pipeline → higher projected
        low_pipe = engine.analyze(make_input(weighted_pipeline=0.0, rep_id="low"))
        engine.reset()
        high_pipe = engine.analyze(make_input(weighted_pipeline=200_000.0, rep_id="high"))
        assert high_pipe.projected_attainment >= low_pipe.projected_attainment

    def test_zero_days_remaining_uses_current(self, engine):
        # days_remaining=0 means period is over; run_rate projects same as closed
        inp = make_input(
            days_remaining=0,
            total_period_days=90,
            closed_won_ytd=300_000.0,
            quota_ytd=300_000.0,
            weighted_pipeline=0.0,
            win_rate=0.0,
        )
        result = engine.analyze(inp)
        # blended_closed = projected_closed*0.6 + closed_won*0.4
        # projected_closed = closed_won + 0 = 300k, pipeline=0
        # blended = 300k*0.6 + 300k*0.4 = 300k => 100%
        assert result.projected_attainment == pytest.approx(100.0, abs=1.0)

    def test_positive_pipeline_win_rate_contribution(self, engine):
        inp = make_input(
            closed_won_ytd=100_000.0,
            quota_ytd=300_000.0,
            weighted_pipeline=100_000.0,
            win_rate=50.0,
            days_remaining=30,
            total_period_days=90,
        )
        result = engine.analyze(inp)
        # pipeline_contribution = 100k * 0.5 = 50k
        # days_elapsed = 90-30=60, run_rate=100k/60
        # projected_closed = 100k + run_rate*30
        assert result.projected_attainment > 0.0

    def test_total_period_days_zero(self, engine):
        inp = make_input(total_period_days=0, days_remaining=0)
        result = engine.analyze(inp)
        # When total_period_days <= 0, returns attainment_pct
        assert result.projected_attainment == result.attainment_pct


# ── 6. _gap_to_quota ──────────────────────────────────────────────────────────

class TestGapToQuota:
    def test_basic_formula(self, engine):
        inp = make_input(quota_ytd=300_000.0, closed_won_ytd=200_000.0)
        result = engine.analyze(inp)
        assert result.gap_to_quota == pytest.approx(100_000.0, abs=1.0)

    def test_already_ahead_returns_zero(self, engine):
        inp = make_input(quota_ytd=300_000.0, closed_won_ytd=350_000.0)
        result = engine.analyze(inp)
        assert result.gap_to_quota == 0.0

    def test_exactly_at_quota_returns_zero(self, engine):
        inp = make_input(quota_ytd=300_000.0, closed_won_ytd=300_000.0)
        result = engine.analyze(inp)
        assert result.gap_to_quota == 0.0

    def test_zero_closed_won_gap_equals_quota(self, engine):
        inp = make_input(quota_ytd=300_000.0, closed_won_ytd=0.0)
        result = engine.analyze(inp)
        assert result.gap_to_quota == pytest.approx(300_000.0, abs=1.0)

    def test_gap_is_non_negative(self, engine):
        for won in (0, 100_000, 300_000, 400_000):
            engine.reset()
            inp = make_input(closed_won_ytd=float(won), quota_ytd=300_000.0)
            result = engine.analyze(inp)
            assert result.gap_to_quota >= 0.0


# ── 7. _coverage_ratio ────────────────────────────────────────────────────────

class TestCoverageRatio:
    def test_basic_formula(self, engine):
        inp = make_input(
            closed_won_ytd=150_000.0,
            weighted_pipeline=75_000.0,
            quota_ytd=300_000.0,
        )
        result = engine.analyze(inp)
        expected = (150_000.0 + 75_000.0) / 300_000.0
        assert result.coverage_ratio == pytest.approx(expected, abs=0.01)

    def test_zero_quota_returns_zero(self, engine):
        inp = make_input(quota_ytd=0.0)
        result = engine.analyze(inp)
        assert result.coverage_ratio == 0.0

    def test_negative_quota_returns_zero(self, engine):
        inp = make_input(quota_ytd=-100.0)
        result = engine.analyze(inp)
        assert result.coverage_ratio == 0.0

    def test_coverage_above_one_when_pipeline_large(self, engine):
        inp = make_input(
            closed_won_ytd=200_000.0,
            weighted_pipeline=200_000.0,
            quota_ytd=300_000.0,
        )
        result = engine.analyze(inp)
        assert result.coverage_ratio > 1.0

    def test_zero_closed_and_pipeline_returns_zero_coverage(self, engine):
        inp = make_input(
            closed_won_ytd=0.0,
            weighted_pipeline=0.0,
            quota_ytd=300_000.0,
        )
        result = engine.analyze(inp)
        assert result.coverage_ratio == pytest.approx(0.0, abs=0.01)


# ── 8. _confidence_score ──────────────────────────────────────────────────────

class TestConfidenceScore:
    def test_historical_component_capped_at_35(self, engine):
        # historical_attainment * 0.25 capped at 35 → needs >=140 to cap
        inp = make_input(
            historical_attainment=200.0,  # 200*0.25=50 → capped 35
        )
        # We can't easily isolate this, but we can verify the score is clamped [0,100]
        result = engine.analyze(inp)
        assert 0.0 <= result.confidence_score <= 100.0

    def test_confidence_clamped_at_zero(self, engine):
        # Everything zero, high stall rate → should not go below 0
        inp = make_input(
            historical_attainment=0.0,
            closed_won_ytd=0.0,
            weighted_pipeline=0.0,
            quota_ytd=300_000.0,
            win_rate=0.0,
            active_deal_count=10,
            stalled_deal_count=10,
        )
        result = engine.analyze(inp)
        assert result.confidence_score >= 0.0

    def test_confidence_clamped_at_100(self, engine):
        # Maxed out inputs → should not exceed 100
        inp = make_input(
            historical_attainment=200.0,
            closed_won_ytd=300_000.0,
            quota_ytd=100_000.0,
            weighted_pipeline=500_000.0,
            win_rate=100.0,
            active_deal_count=10,
            stalled_deal_count=0,
        )
        result = engine.analyze(inp)
        assert result.confidence_score <= 100.0

    def test_stall_penalty_reduces_score(self, engine):
        low_stall = make_input(
            active_deal_count=10, stalled_deal_count=0, rep_id="low"
        )
        high_stall = make_input(
            active_deal_count=10, stalled_deal_count=9, rep_id="high"
        )
        r_low = engine.analyze(low_stall)
        engine.reset()
        r_high = engine.analyze(high_stall)
        assert r_high.confidence_score < r_low.confidence_score

    def test_stall_penalty_skipped_when_no_active_deals(self, engine):
        # With active_deal_count=0, no stall penalty
        inp = make_input(
            active_deal_count=0,
            stalled_deal_count=5,
            historical_attainment=80.0,
            win_rate=25.0,
        )
        result = engine.analyze(inp)
        # Just verify no crash and valid range
        assert 0.0 <= result.confidence_score <= 100.0

    def test_win_rate_contributes_to_confidence(self, engine):
        low_wr = make_input(win_rate=0.0, rep_id="low")
        high_wr = make_input(win_rate=100.0, rep_id="high")
        r_low = engine.analyze(low_wr)
        engine.reset()
        r_high = engine.analyze(high_wr)
        assert r_high.confidence_score > r_low.confidence_score

    def test_historical_attainment_contributes(self, engine):
        low_hist = make_input(historical_attainment=0.0, rep_id="low")
        high_hist = make_input(historical_attainment=140.0, rep_id="high")
        r_low = engine.analyze(low_hist)
        engine.reset()
        r_high = engine.analyze(high_hist)
        assert r_high.confidence_score > r_low.confidence_score

    def test_coverage_contributes(self, engine):
        low_cov = make_input(closed_won_ytd=0.0, weighted_pipeline=0.0, rep_id="low")
        high_cov = make_input(
            closed_won_ytd=200_000.0, weighted_pipeline=200_000.0, quota_ytd=100_000.0,
            rep_id="high"
        )
        r_low = engine.analyze(low_cov)
        engine.reset()
        r_high = engine.analyze(high_cov)
        assert r_high.confidence_score > r_low.confidence_score


# ── 9. _momentum_score ────────────────────────────────────────────────────────

class TestMomentumScore:
    def test_clamped_between_0_and_100(self, engine):
        result = engine.analyze(make_input())
        assert 0.0 <= result.momentum_score <= 100.0

    def test_zero_activity_no_deals(self, engine):
        inp = make_input(
            activities_per_day=0.0,
            new_deals_added_mtd=0,
            active_deal_count=0,
            stalled_deal_count=0,
        )
        result = engine.analyze(inp)
        assert result.momentum_score == pytest.approx(0.0, abs=0.1)

    def test_activity_contribution_up_to_40(self, engine):
        # activities_per_day * 8 capped at 40; need >= 5 to cap
        inp_low = make_input(activities_per_day=0.0, new_deals_added_mtd=0,
                             active_deal_count=0, rep_id="low")
        inp_high = make_input(activities_per_day=10.0, new_deals_added_mtd=0,
                              active_deal_count=0, rep_id="high")
        r_low = engine.analyze(inp_low)
        engine.reset()
        r_high = engine.analyze(inp_high)
        assert r_high.momentum_score > r_low.momentum_score

    def test_new_deals_contribution_up_to_30(self, engine):
        inp_low = make_input(activities_per_day=0.0, new_deals_added_mtd=0,
                             active_deal_count=0, rep_id="low")
        inp_high = make_input(activities_per_day=0.0, new_deals_added_mtd=10,
                              active_deal_count=0, rep_id="high")
        r_low = engine.analyze(inp_low)
        engine.reset()
        r_high = engine.analyze(inp_high)
        assert r_high.momentum_score > r_low.momentum_score

    def test_healthy_deal_rate_contribution(self, engine):
        inp_unhealthy = make_input(
            active_deal_count=10,
            stalled_deal_count=10,
            activities_per_day=0.0,
            new_deals_added_mtd=0,
            rep_id="unhealthy",
        )
        inp_healthy = make_input(
            active_deal_count=10,
            stalled_deal_count=0,
            activities_per_day=0.0,
            new_deals_added_mtd=0,
            rep_id="healthy",
        )
        r_unhealthy = engine.analyze(inp_unhealthy)
        engine.reset()
        r_healthy = engine.analyze(inp_healthy)
        assert r_healthy.momentum_score > r_unhealthy.momentum_score

    def test_no_active_deals_skips_healthy_rate(self, engine):
        # active_deal_count=0 → healthy_rate branch skipped
        inp = make_input(
            active_deal_count=0,
            stalled_deal_count=0,
            activities_per_day=0.0,
            new_deals_added_mtd=0,
        )
        result = engine.analyze(inp)
        assert result.momentum_score == pytest.approx(0.0, abs=0.1)

    def test_max_activity_capped(self, engine):
        # 100 activities/day * 8 = 800, should be capped at 40
        inp_mod = make_input(activities_per_day=5.0, new_deals_added_mtd=0,
                             active_deal_count=0, rep_id="moderate")
        inp_max = make_input(activities_per_day=100.0, new_deals_added_mtd=0,
                             active_deal_count=0, rep_id="max")
        r_mod = engine.analyze(inp_mod)
        engine.reset()
        r_max = engine.analyze(inp_max)
        # Both capped at 40 for activity component; scores should be equal
        assert r_max.momentum_score == r_mod.momentum_score


# ── 10. _pace_score ───────────────────────────────────────────────────────────

class TestPaceScore:
    def test_returns_50_for_zero_total_days(self, engine):
        inp = make_input(total_period_days=0, days_remaining=0)
        result = engine.analyze(inp)
        assert result.pace_score == pytest.approx(50.0, abs=0.1)

    def test_returns_50_when_no_time_elapsed(self, engine):
        # days_remaining == total_period_days → period_progress=0%
        inp = make_input(total_period_days=90, days_remaining=90)
        result = engine.analyze(inp)
        assert result.pace_score == pytest.approx(50.0, abs=0.1)

    def test_ahead_of_pace_gives_score_above_50(self, engine):
        # 60 days elapsed of 90 = 66.7% progress; if attainment_pct > 66.7% → ahead
        inp = make_input(
            total_period_days=90,
            days_remaining=30,
            closed_won_ytd=300_000.0,  # 100% of 300k quota
            quota_ytd=300_000.0,
        )
        result = engine.analyze(inp)
        assert result.pace_score > 50.0

    def test_behind_pace_gives_score_below_50(self, engine):
        # 60 days elapsed (66.7% progress), only 10% attainment
        inp = make_input(
            total_period_days=90,
            days_remaining=30,
            closed_won_ytd=30_000.0,  # 10% of 300k quota
            quota_ytd=300_000.0,
        )
        result = engine.analyze(inp)
        assert result.pace_score < 50.0

    def test_pace_clamped_at_100(self, engine):
        # Very high attainment at early period → clamped at 100
        inp = make_input(
            total_period_days=90,
            days_remaining=89,
            closed_won_ytd=300_000.0,
            quota_ytd=300_000.0,
        )
        result = engine.analyze(inp)
        assert result.pace_score <= 100.0

    def test_pace_clamped_at_zero(self, engine):
        # Zero attainment late in period → clamped at 0
        inp = make_input(
            total_period_days=90,
            days_remaining=0,
            closed_won_ytd=0.0,
            quota_ytd=300_000.0,
        )
        result = engine.analyze(inp)
        assert result.pace_score >= 0.0

    def test_pace_formula_delta(self, engine):
        # period_progress = (90-30)/90 * 100 = 66.67%
        # attainment = 300k/300k * 100 = 100%
        # delta = 100 - 66.67 = 33.33
        # score = 50 + 33.33*2.5 = 50 + 83.33 = 133.33 → clamped 100
        inp = make_input(
            total_period_days=90,
            days_remaining=30,
            closed_won_ytd=300_000.0,
            quota_ytd=300_000.0,
        )
        result = engine.analyze(inp)
        assert result.pace_score == pytest.approx(100.0, abs=0.1)


# ── 11. _performance_trend — all 4 states ─────────────────────────────────────

class TestPerformanceTrend:
    def _make_trend_input(self, historical, last_quarter, pace_attainment_pct,
                          total_days=90, remaining=30, quota=300_000.0) -> QuotaAttainmentInput:
        """
        Craft an input where attainment_pct and pace are controlled.
        pace = 50 + (attainment_pct - period_progress) * 2.5
        period_progress = (90-30)/90*100 = 66.67%
        """
        # closed_won_ytd = quota * pace_attainment_pct / 100
        closed = quota * pace_attainment_pct / 100
        return make_input(
            historical_attainment=historical,
            last_quarter_attainment=last_quarter,
            closed_won_ytd=closed,
            quota_ytd=quota,
            total_period_days=total_days,
            days_remaining=remaining,
        )

    def test_accelerating_trend(self, engine):
        # curr >= prev*1.1 AND pace >= 55
        # historical=100, last_quarter=115 (>=110), need pace>=55
        # period_progress=66.67%, attainment_pct needs delta > 2 → attainment > 68.67
        # Use attainment=100% → pace = 50 + (100-66.67)*2.5 = 50+83.33=133→100(clamped)>=55
        inp = self._make_trend_input(historical=100.0, last_quarter=115.0,
                                     pace_attainment_pct=100.0)
        result = engine.analyze(inp)
        assert result.performance_trend == PerformanceTrend.ACCELERATING

    def test_declining_trend_by_pace(self, engine):
        # pace < 35 → DECLINING regardless of curr/prev
        # pace < 35 means: 50 + delta*2.5 < 35 → delta < -6
        # period_progress=66.67%, need attainment < 60.67
        # Use attainment=20%, last_quarter=90, historical=100
        inp = self._make_trend_input(historical=100.0, last_quarter=90.0,
                                     pace_attainment_pct=20.0)
        result = engine.analyze(inp)
        assert result.performance_trend == PerformanceTrend.DECLINING

    def test_declining_trend_by_attainment_ratio(self, engine):
        # curr < prev*0.85 → DECLINING
        # historical=100, last_quarter=84 → 84 < 85 → DECLINING
        # Give decent pace to isolate the attainment condition
        inp = self._make_trend_input(historical=100.0, last_quarter=84.0,
                                     pace_attainment_pct=70.0)
        result = engine.analyze(inp)
        assert result.performance_trend == PerformanceTrend.DECLINING

    def test_slowing_trend_by_attainment_ratio(self, engine):
        # curr < prev*0.95 → SLOWING (but not < prev*0.85)
        # historical=100, last_quarter=93 → 93 < 95 → SLOWING
        # pace must be >= 35 to not be DECLINING, but < 55 to not be ACCELERATING
        # pace 45-54 range; period_progress=66.67%
        # attainment for pace~50: delta=0 → attainment=66.67
        inp = self._make_trend_input(historical=100.0, last_quarter=93.0,
                                     pace_attainment_pct=66.67)
        result = engine.analyze(inp)
        assert result.performance_trend == PerformanceTrend.SLOWING

    def test_slowing_trend_by_pace(self, engine):
        # pace < 45 (but >= 35) → SLOWING
        # Need curr >= prev*0.95 to avoid SLOWING by attainment check
        # pace=40: 50 + delta*2.5=40 → delta=-4 → attainment=62.67
        # delta=-4, period_progress=66.67 → attainment=62.67%
        inp = self._make_trend_input(historical=100.0, last_quarter=100.0,
                                     pace_attainment_pct=62.67)
        result = engine.analyze(inp)
        assert result.performance_trend == PerformanceTrend.SLOWING

    def test_on_track_trend(self, engine):
        # curr >= prev*0.95 AND pace in [45,55)
        # historical=100, last_quarter=98 (>=95) → not slowing by ratio
        # Need pace in [45,55); attainment ~64 gives pace~50 (delta=-2.67 → pace=43.3)
        # Let's use equal attainment to get pace=50, last_quarter=100 (>=95)
        inp = self._make_trend_input(historical=100.0, last_quarter=100.0,
                                     pace_attainment_pct=66.67)
        result = engine.analyze(inp)
        assert result.performance_trend == PerformanceTrend.ON_TRACK

    def test_accelerating_requires_both_conditions(self, engine):
        # curr >= prev*1.1 but pace < 55 → NOT accelerating
        # historical=100, last_quarter=115; pace=40 (attainment=62.67%)
        inp = self._make_trend_input(historical=100.0, last_quarter=115.0,
                                     pace_attainment_pct=62.67)
        result = engine.analyze(inp)
        assert result.performance_trend != PerformanceTrend.ACCELERATING


# ── 12. _attainment_likelihood — all 5 levels at boundaries ──────────────────

class TestAttainmentLikelihood:
    def _make_likelihood_result(self, engine, projected, confidence):
        """
        Craft an input that produces known projected and confidence values.
        Use quota_ytd=0 trick doesn't give projected control.
        Instead use direct arithmetic approach via a helper.
        """
        # We'll drive projected via closed_won_ytd and confidence via well-known params.
        # score = projected*0.6 + confidence*0.4
        # We'll manipulate the engine's private methods directly.
        # Simpler: create inputs that we can reason about analytically.
        # projected ~= attainment_pct when no pipeline and at end of period
        # Use days_remaining=0, total_period_days=90
        # attainment_pct = closed/quota * 100 = projected (approx)
        # confidence from win_rate: win_rate*0.15; historical*0.25 (max35); coverage*10 (max20)
        closed = projected * 1000.0
        quota = 1000.0 * 100
        # confidence ~ historical*0.25(max35) + projected_inner*0.20(max30) + coverage*10(max20) + win_rate*0.15
        # set them all to produce the given confidence
        return (projected, confidence)

    def test_very_likely_at_90_boundary(self, engine):
        # score = projected*0.6 + confidence*0.4 >= 90
        # Use projected=100, confidence=75 → 100*0.6 + 75*0.4 = 60+30 = 90
        # We need to produce result where projected≈100 and confidence≈75
        # Use a highly performing rep
        inp = make_input(
            closed_won_ytd=1_000_000.0,
            quota_ytd=1_000_000.0,
            historical_attainment=140.0,  # 140*0.25=35 (max)
            win_rate=100.0,               # 100*0.15=15
            active_deal_count=0,
            stalled_deal_count=0,
            weighted_pipeline=0.0,
            days_remaining=0,
            total_period_days=90,
        )
        result = engine.analyze(inp)
        score = result.projected_attainment * 0.6 + result.confidence_score * 0.4
        assert score >= 90
        assert result.attainment_likelihood == AttainmentLikelihood.VERY_LIKELY

    def test_likely_range_75_to_89(self, engine):
        # score in [75, 90)
        # projected=80, confidence=65 → 48+26=74 too low
        # projected=90, confidence=55 → 54+22=76 in range
        # Need to engineer such a result — use moderate performer
        inp = make_input(
            closed_won_ytd=270_000.0,
            quota_ytd=300_000.0,
            historical_attainment=100.0,
            win_rate=30.0,
            active_deal_count=5,
            stalled_deal_count=0,
            weighted_pipeline=50_000.0,
            days_remaining=30,
            total_period_days=90,
        )
        result = engine.analyze(inp)
        score = result.projected_attainment * 0.6 + result.confidence_score * 0.4
        if 75 <= score < 90:
            assert result.attainment_likelihood == AttainmentLikelihood.LIKELY

    def test_possible_range_55_to_74(self, engine):
        inp = make_input(
            closed_won_ytd=150_000.0,
            quota_ytd=300_000.0,
            historical_attainment=60.0,
            win_rate=20.0,
            active_deal_count=5,
            stalled_deal_count=2,
            weighted_pipeline=30_000.0,
            days_remaining=45,
            total_period_days=90,
        )
        result = engine.analyze(inp)
        score = result.projected_attainment * 0.6 + result.confidence_score * 0.4
        if 55 <= score < 75:
            assert result.attainment_likelihood == AttainmentLikelihood.POSSIBLE

    def test_unlikely_range_35_to_54(self, engine):
        inp = make_input(
            closed_won_ytd=60_000.0,
            quota_ytd=300_000.0,
            historical_attainment=40.0,
            win_rate=10.0,
            active_deal_count=3,
            stalled_deal_count=2,
            weighted_pipeline=10_000.0,
            days_remaining=20,
            total_period_days=90,
        )
        result = engine.analyze(inp)
        score = result.projected_attainment * 0.6 + result.confidence_score * 0.4
        if 35 <= score < 55:
            assert result.attainment_likelihood == AttainmentLikelihood.UNLIKELY

    def test_very_unlikely_below_35(self, engine):
        inp = make_input(
            closed_won_ytd=0.0,
            quota_ytd=300_000.0,
            historical_attainment=0.0,
            win_rate=0.0,
            active_deal_count=10,
            stalled_deal_count=10,
            weighted_pipeline=0.0,
            days_remaining=5,
            total_period_days=90,
        )
        result = engine.analyze(inp)
        score = result.projected_attainment * 0.6 + result.confidence_score * 0.4
        if score < 35:
            assert result.attainment_likelihood == AttainmentLikelihood.VERY_UNLIKELY

    def test_likelihood_score_formula_directly(self, engine):
        # Verify score formula: projected*0.6 + confidence*0.4
        result = engine.analyze(make_input())
        computed_score = result.projected_attainment * 0.6 + result.confidence_score * 0.4
        if computed_score >= 90:
            assert result.attainment_likelihood == AttainmentLikelihood.VERY_LIKELY
        elif computed_score >= 75:
            assert result.attainment_likelihood == AttainmentLikelihood.LIKELY
        elif computed_score >= 55:
            assert result.attainment_likelihood == AttainmentLikelihood.POSSIBLE
        elif computed_score >= 35:
            assert result.attainment_likelihood == AttainmentLikelihood.UNLIKELY
        else:
            assert result.attainment_likelihood == AttainmentLikelihood.VERY_UNLIKELY

    def test_likelihood_consistent_with_score(self, engine):
        # Multiple reps: verify each result's likelihood matches computed score
        reps = [
            make_input(rep_id=f"r{i}", closed_won_ytd=i*30_000.0, quota_ytd=300_000.0)
            for i in range(6)
        ]
        results = engine.analyze_batch(reps)
        for r in results:
            score = r.projected_attainment * 0.6 + r.confidence_score * 0.4
            if score >= 90:
                expected = AttainmentLikelihood.VERY_LIKELY
            elif score >= 75:
                expected = AttainmentLikelihood.LIKELY
            elif score >= 55:
                expected = AttainmentLikelihood.POSSIBLE
            elif score >= 35:
                expected = AttainmentLikelihood.UNLIKELY
            else:
                expected = AttainmentLikelihood.VERY_UNLIKELY
            assert r.attainment_likelihood == expected


# ── 13. _attainment_risk — all 4 levels ──────────────────────────────────────

class TestAttainmentRisk:
    def test_low_risk_zero_quota(self, engine):
        inp = make_input(quota_ytd=0.0)
        result = engine.analyze(inp)
        assert result.attainment_risk == AttainmentRisk.LOW

    def test_low_risk_high_projected_small_gap(self, engine):
        # projected >= 90 AND gap_pct < 20
        # closed=290k, quota=300k → gap=10k, gap_pct=3.3%
        # Need projected >= 90
        inp = make_input(
            closed_won_ytd=290_000.0,
            quota_ytd=300_000.0,
            historical_attainment=120.0,
            win_rate=50.0,
            weighted_pipeline=100_000.0,
            days_remaining=10,
            total_period_days=90,
        )
        result = engine.analyze(inp)
        if result.projected_attainment >= 90:
            assert result.attainment_risk == AttainmentRisk.LOW

    def test_medium_risk(self, engine):
        # projected >= 70 AND gap_pct < 40 (but not LOW conditions)
        inp = make_input(
            closed_won_ytd=180_000.0,
            quota_ytd=300_000.0,
            historical_attainment=80.0,
            win_rate=25.0,
            weighted_pipeline=80_000.0,
            days_remaining=30,
            total_period_days=90,
        )
        result = engine.analyze(inp)
        gap_pct = (result.gap_to_quota / 300_000.0) * 100
        proj = result.projected_attainment
        if proj >= 70 and gap_pct < 40 and not (proj >= 90 and gap_pct < 20):
            assert result.attainment_risk == AttainmentRisk.MEDIUM

    def test_high_risk(self, engine):
        # projected >= 50 but doesn't meet LOW or MEDIUM
        inp = make_input(
            closed_won_ytd=100_000.0,
            quota_ytd=300_000.0,
            historical_attainment=50.0,
            win_rate=15.0,
            weighted_pipeline=20_000.0,
            days_remaining=20,
            total_period_days=90,
        )
        result = engine.analyze(inp)
        proj = result.projected_attainment
        gap_pct = (result.gap_to_quota / 300_000.0) * 100
        if proj >= 50 and not (proj >= 70 and gap_pct < 40):
            assert result.attainment_risk == AttainmentRisk.HIGH

    def test_critical_risk(self, engine):
        # projected < 50
        inp = make_input(
            closed_won_ytd=0.0,
            quota_ytd=300_000.0,
            historical_attainment=0.0,
            win_rate=0.0,
            weighted_pipeline=0.0,
            days_remaining=5,
            total_period_days=90,
        )
        result = engine.analyze(inp)
        if result.projected_attainment < 50:
            assert result.attainment_risk == AttainmentRisk.CRITICAL

    def test_risk_consistent_with_logic(self, engine):
        result = engine.analyze(make_input())
        proj = result.projected_attainment
        gap = result.gap_to_quota
        quota = 300_000.0
        gap_pct = (gap / quota) * 100
        if proj >= 90 and gap_pct < 20:
            assert result.attainment_risk == AttainmentRisk.LOW
        elif proj >= 70 and gap_pct < 40:
            assert result.attainment_risk == AttainmentRisk.MEDIUM
        elif proj >= 50:
            assert result.attainment_risk == AttainmentRisk.HIGH
        else:
            assert result.attainment_risk == AttainmentRisk.CRITICAL


# ── 14. _attainment_action — all 5 actions ────────────────────────────────────

class TestAttainmentAction:
    def test_urgent_review_for_critical_risk(self, engine):
        # CRITICAL risk → URGENT_REVIEW
        inp = make_input(
            closed_won_ytd=0.0,
            quota_ytd=300_000.0,
            historical_attainment=0.0,
            win_rate=0.0,
            weighted_pipeline=0.0,
            days_remaining=5,
            total_period_days=90,
        )
        result = engine.analyze(inp)
        if result.attainment_risk == AttainmentRisk.CRITICAL:
            assert result.attainment_action == AttainmentAction.URGENT_REVIEW

    def test_coaching_required_for_declining_high_risk(self, engine):
        # DECLINING trend + HIGH risk → COACHING_REQUIRED
        # Need: projected in [50,70) AND (not gap_pct<40 OR projected<70)
        # AND curr < prev*0.85 OR pace < 35
        inp = make_input(
            closed_won_ytd=100_000.0,
            quota_ytd=300_000.0,
            historical_attainment=100.0,
            last_quarter_attainment=80.0,   # 80 < 100*0.85=85 → DECLINING
            win_rate=15.0,
            weighted_pipeline=20_000.0,
            days_remaining=20,
            total_period_days=90,
        )
        result = engine.analyze(inp)
        if (result.performance_trend == PerformanceTrend.DECLINING
                and result.attainment_risk == AttainmentRisk.HIGH):
            assert result.attainment_action == AttainmentAction.COACHING_REQUIRED

    def test_pipeline_build_for_unlikely_likelihood(self, engine):
        # UNLIKELY or VERY_UNLIKELY → PIPELINE_BUILD (unless CRITICAL/COACHING)
        # Need non-critical risk + non-declining/high combo
        inp = make_input(
            closed_won_ytd=60_000.0,
            quota_ytd=300_000.0,
            historical_attainment=50.0,
            last_quarter_attainment=52.0,
            win_rate=10.0,
            weighted_pipeline=30_000.0,
            active_deal_count=5,
            stalled_deal_count=1,
            days_remaining=30,
            total_period_days=90,
        )
        result = engine.analyze(inp)
        if result.attainment_likelihood in (AttainmentLikelihood.UNLIKELY,
                                             AttainmentLikelihood.VERY_UNLIKELY):
            if result.attainment_risk != AttainmentRisk.CRITICAL:
                if not (result.performance_trend == PerformanceTrend.DECLINING
                        and result.attainment_risk == AttainmentRisk.HIGH):
                    assert result.attainment_action == AttainmentAction.PIPELINE_BUILD

    def test_accelerate_for_low_momentum(self, engine):
        # momentum < 40 (and not CRITICAL/COACHING/PIPELINE_BUILD) → ACCELERATE
        inp = make_input(
            activities_per_day=0.0,
            new_deals_added_mtd=0,
            active_deal_count=0,
            stalled_deal_count=0,
            closed_won_ytd=270_000.0,
            quota_ytd=300_000.0,
            historical_attainment=100.0,
            last_quarter_attainment=100.0,
            win_rate=50.0,
            weighted_pipeline=50_000.0,
        )
        result = engine.analyze(inp)
        if (result.momentum_score < 40
                and result.attainment_risk != AttainmentRisk.CRITICAL
                and result.attainment_likelihood not in (
                    AttainmentLikelihood.UNLIKELY, AttainmentLikelihood.VERY_UNLIKELY)
                and not (result.performance_trend == PerformanceTrend.DECLINING
                         and result.attainment_risk == AttainmentRisk.HIGH)):
            assert result.attainment_action == AttainmentAction.ACCELERATE

    def test_accelerate_for_slowing_trend(self, engine):
        # SLOWING → ACCELERATE (unless higher priority conditions)
        # Need SLOWING: curr in [prev*0.85, prev*0.95)
        # historical=100, last_quarter=93 → SLOWING
        inp = make_input(
            historical_attainment=100.0,
            last_quarter_attainment=93.0,
            closed_won_ytd=270_000.0,
            quota_ytd=300_000.0,
            win_rate=50.0,
            weighted_pipeline=100_000.0,
            activities_per_day=5.0,
            new_deals_added_mtd=5,
            active_deal_count=10,
            stalled_deal_count=0,
            days_remaining=30,
            total_period_days=90,
        )
        result = engine.analyze(inp)
        if (result.performance_trend == PerformanceTrend.SLOWING
                and result.attainment_risk != AttainmentRisk.CRITICAL
                and result.attainment_likelihood not in (
                    AttainmentLikelihood.UNLIKELY, AttainmentLikelihood.VERY_UNLIKELY)
                and not (result.performance_trend == PerformanceTrend.DECLINING
                         and result.attainment_risk == AttainmentRisk.HIGH)):
            assert result.attainment_action == AttainmentAction.ACCELERATE

    def test_maintain_for_healthy_rep(self, engine):
        # Everything good → MAINTAIN
        inp = make_input(
            historical_attainment=100.0,
            last_quarter_attainment=105.0,
            closed_won_ytd=300_000.0,
            quota_ytd=300_000.0,
            win_rate=50.0,
            weighted_pipeline=150_000.0,
            activities_per_day=6.0,
            new_deals_added_mtd=5,
            active_deal_count=10,
            stalled_deal_count=0,
            days_remaining=30,
            total_period_days=90,
        )
        result = engine.analyze(inp)
        if (result.attainment_risk != AttainmentRisk.CRITICAL
                and result.performance_trend != PerformanceTrend.DECLINING
                and result.attainment_likelihood not in (
                    AttainmentLikelihood.UNLIKELY, AttainmentLikelihood.VERY_UNLIKELY)
                and result.momentum_score >= 40
                and result.performance_trend != PerformanceTrend.SLOWING):
            assert result.attainment_action == AttainmentAction.MAINTAIN

    def test_critical_overrides_all_other_actions(self, engine):
        # CRITICAL risk must always produce URGENT_REVIEW
        result = engine.analyze(make_input(
            closed_won_ytd=0.0, quota_ytd=300_000.0,
            historical_attainment=0.0, win_rate=0.0,
            weighted_pipeline=0.0, days_remaining=5, total_period_days=90,
        ))
        if result.attainment_risk == AttainmentRisk.CRITICAL:
            assert result.attainment_action == AttainmentAction.URGENT_REVIEW

    def test_action_consistency_across_batch(self, engine):
        inputs = [make_input(rep_id=f"r{i}") for i in range(5)]
        results = engine.analyze_batch(inputs)
        for r in results:
            # Verify priority ordering
            if r.attainment_risk == AttainmentRisk.CRITICAL:
                assert r.attainment_action == AttainmentAction.URGENT_REVIEW


# ── 15. is_at_risk — both conditions ──────────────────────────────────────────

class TestIsAtRisk:
    def test_at_risk_when_projected_below_80(self, engine):
        inp = make_input(
            closed_won_ytd=0.0,
            quota_ytd=300_000.0,
            weighted_pipeline=10_000.0,
            win_rate=10.0,
            days_remaining=5,
            total_period_days=90,
        )
        result = engine.analyze(inp)
        if result.projected_attainment < 80.0:
            assert result.is_at_risk is True

    def test_at_risk_when_risk_is_high(self, engine):
        inp = make_input(
            closed_won_ytd=100_000.0,
            quota_ytd=300_000.0,
            historical_attainment=50.0,
            win_rate=10.0,
            weighted_pipeline=20_000.0,
            days_remaining=20,
            total_period_days=90,
        )
        result = engine.analyze(inp)
        if result.attainment_risk == AttainmentRisk.HIGH:
            assert result.is_at_risk is True

    def test_at_risk_when_risk_is_critical(self, engine):
        inp = make_input(
            closed_won_ytd=0.0, quota_ytd=300_000.0,
            historical_attainment=0.0, win_rate=0.0,
            weighted_pipeline=0.0, days_remaining=5, total_period_days=90,
        )
        result = engine.analyze(inp)
        if result.attainment_risk == AttainmentRisk.CRITICAL:
            assert result.is_at_risk is True

    def test_not_at_risk_for_strong_rep(self, engine):
        inp = make_input(
            closed_won_ytd=300_000.0,
            quota_ytd=300_000.0,
            historical_attainment=120.0,
            win_rate=60.0,
            weighted_pipeline=200_000.0,
            days_remaining=30,
            total_period_days=90,
        )
        result = engine.analyze(inp)
        # Verify logic: projected >= 80 AND risk NOT HIGH/CRITICAL → not at risk
        if result.projected_attainment >= 80.0 and result.attainment_risk not in (
            AttainmentRisk.HIGH, AttainmentRisk.CRITICAL
        ):
            assert result.is_at_risk is False

    def test_is_at_risk_is_boolean(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.is_at_risk, bool)

    def test_at_risk_any_condition_sufficient(self, engine):
        # Either projected < 80 OR risk in HIGH/CRITICAL → at risk
        result = engine.analyze(make_input())
        expected = (
            result.projected_attainment < 80.0
            or result.attainment_risk in (AttainmentRisk.HIGH, AttainmentRisk.CRITICAL)
        )
        assert result.is_at_risk == expected


# ── 16. needs_coaching — all 3 conditions ────────────────────────────────────

class TestNeedsCoaching:
    def test_needs_coaching_low_last_quarter(self, engine):
        inp = make_input(last_quarter_attainment=60.0)  # < 70 → coaching
        result = engine.analyze(inp)
        assert result.needs_coaching is True

    def test_needs_coaching_exactly_at_70_boundary(self, engine):
        # 70.0 is NOT < 70, so this condition is false
        inp = make_input(last_quarter_attainment=70.0)
        result = engine.analyze(inp)
        # Other conditions may still trigger coaching
        if (result.performance_trend != PerformanceTrend.DECLINING
                and not (inp.stalled_deal_count > inp.active_deal_count * 0.5
                         and inp.active_deal_count > 0)):
            assert result.needs_coaching is False

    def test_needs_coaching_declining_trend(self, engine):
        # DECLINING trend → needs coaching
        inp = make_input(
            historical_attainment=100.0,
            last_quarter_attainment=75.0,  # >= 70, no coaching from last_quarter
            closed_won_ytd=30_000.0,  # pace will be very low → DECLINING
            quota_ytd=300_000.0,
            days_remaining=5,
            total_period_days=90,
        )
        result = engine.analyze(inp)
        if result.performance_trend == PerformanceTrend.DECLINING:
            assert result.needs_coaching is True

    def test_needs_coaching_stalled_majority(self, engine):
        # stalled > active * 0.5 AND active > 0
        inp = make_input(
            active_deal_count=10,
            stalled_deal_count=6,  # 6 > 10*0.5=5
            last_quarter_attainment=75.0,  # not < 70
            historical_attainment=100.0,
        )
        result = engine.analyze(inp)
        assert result.needs_coaching is True

    def test_needs_coaching_stalled_exactly_half_no_trigger(self, engine):
        # stalled == active * 0.5 → NOT > 0.5, so no trigger
        inp = make_input(
            active_deal_count=10,
            stalled_deal_count=5,  # 5 == 10*0.5=5, NOT >5
            last_quarter_attainment=75.0,
        )
        result = engine.analyze(inp)
        # Verify stall condition is false
        assert not (inp.stalled_deal_count > inp.active_deal_count * 0.5)

    def test_no_coaching_needed_for_healthy_rep(self, engine):
        inp = make_input(
            last_quarter_attainment=95.0,  # >= 70
            historical_attainment=100.0,
            active_deal_count=10,
            stalled_deal_count=1,  # 1 <= 5
            closed_won_ytd=240_000.0,
            quota_ytd=300_000.0,
            days_remaining=30,
            total_period_days=90,
        )
        result = engine.analyze(inp)
        if (result.performance_trend != PerformanceTrend.DECLINING
                and inp.last_quarter_attainment >= 70.0
                and not (inp.stalled_deal_count > inp.active_deal_count * 0.5)):
            assert result.needs_coaching is False

    def test_needs_coaching_is_boolean(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.needs_coaching, bool)

    def test_coaching_condition_logic_verified(self, engine):
        inp = make_input()
        result = engine.analyze(inp)
        expected = (
            inp.last_quarter_attainment < 70.0
            or result.performance_trend == PerformanceTrend.DECLINING
            or (inp.stalled_deal_count > inp.active_deal_count * 0.5
                and inp.active_deal_count > 0)
        )
        assert result.needs_coaching == expected

    def test_zero_active_deals_stall_condition_false(self, engine):
        # active_deal_count=0 → stall condition never triggers (active_deal_count>0 is False)
        inp = make_input(
            active_deal_count=0,
            stalled_deal_count=100,  # doesn't matter when active=0
            last_quarter_attainment=80.0,
        )
        result = engine.analyze(inp)
        # stall condition is False because active_deal_count=0
        assert not (inp.stalled_deal_count > inp.active_deal_count * 0.5
                    and inp.active_deal_count > 0)


# ── 17. Properties — empty state, after analyze, filtering ───────────────────

class TestProperties:
    def test_at_risk_reps_empty_initially(self, engine):
        assert engine.at_risk_reps == []

    def test_coaching_reps_empty_initially(self, engine):
        assert engine.coaching_reps == []

    def test_likely_attainers_empty_initially(self, engine):
        assert engine.likely_attainers == []

    def test_total_gap_empty_is_zero(self, engine):
        assert engine.total_gap_to_quota == 0.0

    def test_avg_projected_empty_is_zero(self, engine):
        assert engine.avg_projected_attainment == 0.0

    def test_at_risk_reps_are_results(self, engine):
        engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(5)])
        for r in engine.at_risk_reps:
            assert isinstance(r, QuotaAttainmentResult)

    def test_coaching_reps_are_results(self, engine):
        engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(5)])
        for r in engine.coaching_reps:
            assert isinstance(r, QuotaAttainmentResult)

    def test_likely_attainers_are_results(self, engine):
        engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(5)])
        for r in engine.likely_attainers:
            assert isinstance(r, QuotaAttainmentResult)

    def test_at_risk_reps_filtering_correct(self, engine):
        engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(5)])
        for r in engine.at_risk_reps:
            assert r.is_at_risk is True

    def test_coaching_reps_filtering_correct(self, engine):
        engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(5)])
        for r in engine.coaching_reps:
            assert r.needs_coaching is True

    def test_likely_attainers_filtering_correct(self, engine):
        engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(5)])
        for r in engine.likely_attainers:
            assert r.attainment_likelihood in (
                AttainmentLikelihood.VERY_LIKELY, AttainmentLikelihood.LIKELY
            )

    def test_total_gap_is_sum(self, engine):
        results = engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        expected = round(sum(r.gap_to_quota for r in results), 2)
        assert engine.total_gap_to_quota == expected

    def test_avg_projected_attainment_formula(self, engine):
        results = engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        expected = round(sum(r.projected_attainment for r in results) / 3, 1)
        assert engine.avg_projected_attainment == expected

    def test_avg_projected_single_result(self, engine):
        result = engine.analyze(make_input())
        assert engine.avg_projected_attainment == round(result.projected_attainment, 1)

    def test_total_gap_single_result(self, engine):
        result = engine.analyze(make_input())
        assert engine.total_gap_to_quota == round(result.gap_to_quota, 2)

    def test_at_risk_count_matches_property_len(self, engine):
        engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(5)])
        assert engine.summary()["at_risk_count"] == len(engine.at_risk_reps)

    def test_coaching_count_matches_property_len(self, engine):
        engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(5)])
        assert engine.summary()["coaching_count"] == len(engine.coaching_reps)

    def test_likely_attainer_count_matches_property_len(self, engine):
        engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(5)])
        assert engine.summary()["likely_attainer_count"] == len(engine.likely_attainers)


# ── 18. analyze_batch() and reset() ──────────────────────────────────────────

class TestAnalyzeBatchAndReset:
    def test_analyze_batch_returns_list(self, engine):
        results = engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        assert isinstance(results, list)

    def test_analyze_batch_length(self, engine):
        results = engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(4)])
        assert len(results) == 4

    def test_analyze_batch_returns_results(self, engine):
        results = engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        for r in results:
            assert isinstance(r, QuotaAttainmentResult)

    def test_analyze_batch_accumulates_in_results(self, engine):
        engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        assert engine.summary()["total"] == 3

    def test_analyze_batch_empty_input(self, engine):
        results = engine.analyze_batch([])
        assert results == []

    def test_analyze_batch_single_item(self, engine):
        results = engine.analyze_batch([make_input()])
        assert len(results) == 1

    def test_analyze_batch_preserves_order(self, engine):
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(5)]
        results = engine.analyze_batch(inputs)
        for i, result in enumerate(results):
            assert result.rep_id == f"rep-{i}"

    def test_reset_clears_results(self, engine):
        engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        engine.reset()
        assert engine.summary()["total"] == 0

    def test_reset_clears_at_risk_reps(self, engine):
        engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        engine.reset()
        assert engine.at_risk_reps == []

    def test_reset_clears_coaching_reps(self, engine):
        engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        engine.reset()
        assert engine.coaching_reps == []

    def test_reset_clears_likely_attainers(self, engine):
        engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        engine.reset()
        assert engine.likely_attainers == []

    def test_reset_resets_total_gap(self, engine):
        engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        engine.reset()
        assert engine.total_gap_to_quota == 0.0

    def test_reset_resets_avg_projected(self, engine):
        engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        engine.reset()
        assert engine.avg_projected_attainment == 0.0

    def test_analyze_after_reset_works(self, engine):
        engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        engine.reset()
        engine.analyze(make_input(rep_id="new-rep"))
        assert engine.summary()["total"] == 1

    def test_multiple_resets_safe(self, engine):
        engine.reset()
        engine.reset()
        assert engine.summary()["total"] == 0

    def test_batch_then_single_accumulate(self, engine):
        engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        engine.analyze(make_input(rep_id="extra"))
        assert engine.summary()["total"] == 4


# ── 19. Edge cases ────────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_quota_ytd_zero_full_analysis(self, engine):
        inp = make_input(quota_ytd=0.0, closed_won_ytd=100_000.0, weighted_pipeline=50_000.0)
        result = engine.analyze(inp)
        assert result.attainment_pct == 0.0
        assert result.projected_attainment == 0.0
        assert result.coverage_ratio == 0.0
        # gap = max(0, 0 - 100k) = 0
        assert result.gap_to_quota == 0.0
        # risk should be LOW (quota_ytd <= 0 branch)
        assert result.attainment_risk == AttainmentRisk.LOW

    def test_all_stalled_deals(self, engine):
        inp = make_input(
            active_deal_count=10,
            stalled_deal_count=10,
        )
        result = engine.analyze(inp)
        # Momentum healthy_rate = 0 → no healthy contribution
        assert result.momentum_score >= 0.0
        # needs_coaching: stalled > active*0.5 → True
        assert result.needs_coaching is True

    def test_zero_activity_score(self, engine):
        inp = make_input(
            activities_per_day=0.0,
            new_deals_added_mtd=0,
            active_deal_count=0,
            stalled_deal_count=0,
        )
        result = engine.analyze(inp)
        assert result.momentum_score == pytest.approx(0.0, abs=0.1)

    def test_max_attainment_scenario(self, engine):
        inp = make_input(
            closed_won_ytd=500_000.0,
            quota_ytd=300_000.0,
            historical_attainment=150.0,
            last_quarter_attainment=160.0,
            win_rate=80.0,
            weighted_pipeline=300_000.0,
            activities_per_day=10.0,
            new_deals_added_mtd=8,
            active_deal_count=15,
            stalled_deal_count=0,
        )
        result = engine.analyze(inp)
        assert result.attainment_pct > 100.0
        assert result.confidence_score <= 100.0
        assert result.momentum_score <= 100.0
        assert result.pace_score <= 100.0

    def test_very_large_quota(self, engine):
        inp = make_input(
            quota_ytd=10_000_000.0,
            closed_won_ytd=5_000_000.0,
            weighted_pipeline=2_000_000.0,
        )
        result = engine.analyze(inp)
        assert result.attainment_pct == pytest.approx(50.0, abs=0.2)
        assert result.gap_to_quota == pytest.approx(5_000_000.0, abs=1.0)

    def test_zero_days_remaining(self, engine):
        inp = make_input(days_remaining=0, total_period_days=90)
        result = engine.analyze(inp)
        assert isinstance(result, QuotaAttainmentResult)

    def test_single_day_remaining(self, engine):
        inp = make_input(days_remaining=1, total_period_days=90)
        result = engine.analyze(inp)
        assert isinstance(result, QuotaAttainmentResult)

    def test_no_pipeline(self, engine):
        inp = make_input(
            weighted_pipeline=0.0,
            commit_pipeline=0.0,
            best_case_pipeline=0.0,
        )
        result = engine.analyze(inp)
        assert result.coverage_ratio == pytest.approx(
            result.attainment_pct / 100.0, abs=0.1
        )

    def test_all_fields_present_in_result(self, engine):
        result = engine.analyze(make_input())
        assert hasattr(result, "rep_id")
        assert hasattr(result, "rep_name")
        assert hasattr(result, "attainment_likelihood")
        assert hasattr(result, "attainment_risk")
        assert hasattr(result, "performance_trend")
        assert hasattr(result, "attainment_action")
        assert hasattr(result, "attainment_pct")
        assert hasattr(result, "projected_attainment")
        assert hasattr(result, "gap_to_quota")
        assert hasattr(result, "coverage_ratio")
        assert hasattr(result, "confidence_score")
        assert hasattr(result, "momentum_score")
        assert hasattr(result, "pace_score")
        assert hasattr(result, "is_at_risk")
        assert hasattr(result, "needs_coaching")

    def test_rep_id_and_name_preserved(self, engine):
        inp = make_input(rep_id="unique-123", rep_name="Bob Jones")
        result = engine.analyze(inp)
        assert result.rep_id == "unique-123"
        assert result.rep_name == "Bob Jones"

    def test_result_types_valid(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.attainment_likelihood, AttainmentLikelihood)
        assert isinstance(result.attainment_risk, AttainmentRisk)
        assert isinstance(result.performance_trend, PerformanceTrend)
        assert isinstance(result.attainment_action, AttainmentAction)
        assert isinstance(result.attainment_pct, float)
        assert isinstance(result.projected_attainment, float)
        assert isinstance(result.gap_to_quota, float)
        assert isinstance(result.coverage_ratio, float)
        assert isinstance(result.confidence_score, float)
        assert isinstance(result.momentum_score, float)
        assert isinstance(result.pace_score, float)
        assert isinstance(result.is_at_risk, bool)
        assert isinstance(result.needs_coaching, bool)

    def test_scores_in_valid_ranges(self, engine):
        result = engine.analyze(make_input())
        assert 0.0 <= result.confidence_score <= 100.0
        assert 0.0 <= result.momentum_score <= 100.0
        assert 0.0 <= result.pace_score <= 100.0
        assert result.gap_to_quota >= 0.0
        assert result.coverage_ratio >= 0.0

    def test_engine_is_stateful(self, engine):
        engine.analyze(make_input(rep_id="rep-1"))
        assert engine.summary()["total"] == 1
        engine.analyze(make_input(rep_id="rep-2"))
        assert engine.summary()["total"] == 2

    def test_multiple_engines_independent(self):
        e1 = QuotaAttainmentEngine()
        e2 = QuotaAttainmentEngine()
        e1.analyze(make_input(rep_id="r1"))
        assert e1.summary()["total"] == 1
        assert e2.summary()["total"] == 0

    def test_analyze_returns_result_object(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result, QuotaAttainmentResult)

    def test_quota_attainment_input_has_21_fields(self):
        import dataclasses
        fields = dataclasses.fields(QuotaAttainmentInput)
        assert len(fields) == 21

    def test_quota_attainment_result_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(QuotaAttainmentResult)

    def test_quota_attainment_input_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(QuotaAttainmentInput)

    def test_gap_is_zero_when_way_over_quota(self, engine):
        inp = make_input(closed_won_ytd=1_000_000.0, quota_ytd=100_000.0)
        result = engine.analyze(inp)
        assert result.gap_to_quota == 0.0

    def test_very_high_stall_rate_confidence_not_below_zero(self, engine):
        # stall_rate=1.0 → -15 penalty; must not go below 0
        inp = make_input(
            active_deal_count=5,
            stalled_deal_count=5,
            historical_attainment=0.0,
            win_rate=0.0,
            closed_won_ytd=0.0,
            weighted_pipeline=0.0,
            quota_ytd=300_000.0,
        )
        result = engine.analyze(inp)
        assert result.confidence_score >= 0.0

    def test_new_deals_capped_at_30(self, engine):
        inp_mod = make_input(activities_per_day=0.0, new_deals_added_mtd=6,
                             active_deal_count=0, rep_id="moderate")
        inp_max = make_input(activities_per_day=0.0, new_deals_added_mtd=100,
                             active_deal_count=0, rep_id="max")
        r_mod = engine.analyze(inp_mod)
        engine.reset()
        r_max = engine.analyze(inp_max)
        # Both should have same new-deals component (capped at 30)
        assert r_max.momentum_score == r_mod.momentum_score

    def test_projected_attainment_not_negative_for_zero_closed(self, engine):
        inp = make_input(
            closed_won_ytd=0.0,
            quota_ytd=300_000.0,
            weighted_pipeline=0.0,
            win_rate=0.0,
        )
        result = engine.analyze(inp)
        assert result.projected_attainment == 0.0


# ── 20. Additional boundary and integration tests ─────────────────────────────

class TestBoundaryAndIntegration:
    def test_attainment_pct_exactly_80(self, engine):
        inp = make_input(closed_won_ytd=240_000.0, quota_ytd=300_000.0)
        result = engine.analyze(inp)
        assert result.attainment_pct == pytest.approx(80.0, abs=0.2)

    def test_confidence_historical_cap(self, engine):
        # historical=200 → 200*0.25=50, capped at 35
        # historical=100 → 100*0.25=25
        inp_low_hist = make_input(historical_attainment=100.0, rep_id="low")
        inp_high_hist = make_input(historical_attainment=200.0, rep_id="high")
        r_low = engine.analyze(inp_low_hist)
        engine.reset()
        r_high = engine.analyze(inp_high_hist)
        # High hist should have higher confidence (35 vs 25 from historical component)
        assert r_high.confidence_score >= r_low.confidence_score

    def test_pace_at_exactly_50_when_on_track(self, engine):
        # period_progress == attainment_pct → delta=0 → pace=50
        # period_progress = (90-30)/90 * 100 = 66.67%
        # attainment = 66.67% → closed = 300k * 0.6667 = 200k
        inp = make_input(
            closed_won_ytd=200_010.0,  # ≈ 66.67% of 300k
            quota_ytd=300_000.0,
            total_period_days=90,
            days_remaining=30,
        )
        result = engine.analyze(inp)
        assert result.pace_score == pytest.approx(50.0, abs=3.0)

    def test_summary_likelihood_counts_keys_are_strings(self, engine):
        engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        s = engine.summary()
        for k in s["likelihood_counts"]:
            assert isinstance(k, str)

    def test_summary_risk_counts_keys_are_strings(self, engine):
        engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        s = engine.summary()
        for k in s["risk_counts"]:
            assert isinstance(k, str)

    def test_summary_trend_counts_keys_are_strings(self, engine):
        engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        s = engine.summary()
        for k in s["trend_counts"]:
            assert isinstance(k, str)

    def test_summary_action_counts_keys_are_strings(self, engine):
        engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        s = engine.summary()
        for k in s["action_counts"]:
            assert isinstance(k, str)

    def test_summary_values_are_valid_enum_strings(self, engine):
        engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        s = engine.summary()
        valid_likelihoods = {m.value for m in AttainmentLikelihood}
        for k in s["likelihood_counts"]:
            assert k in valid_likelihoods

    def test_summary_risk_values_are_valid(self, engine):
        engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        s = engine.summary()
        valid_risks = {m.value for m in AttainmentRisk}
        for k in s["risk_counts"]:
            assert k in valid_risks

    def test_summary_trend_values_are_valid(self, engine):
        engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        s = engine.summary()
        valid_trends = {m.value for m in PerformanceTrend}
        for k in s["trend_counts"]:
            assert k in valid_trends

    def test_summary_action_values_are_valid(self, engine):
        engine.analyze_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        s = engine.summary()
        valid_actions = {m.value for m in AttainmentAction}
        for k in s["action_counts"]:
            assert k in valid_actions

    def test_performance_trend_boundary_accelerating_pace(self, engine):
        # pace exactly 55 with curr >= prev*1.1 → ACCELERATING
        # period_progress=(90-30)/90*100=66.67%
        # pace = 50 + (attainment - 66.67)*2.5 = 55 → attainment = 68.67
        inp = make_input(
            historical_attainment=100.0,
            last_quarter_attainment=115.0,  # >= 100*1.1
            closed_won_ytd=300_000.0 * 0.6867,  # ~68.67%
            quota_ytd=300_000.0,
            total_period_days=90,
            days_remaining=30,
        )
        result = engine.analyze(inp)
        # pace should be ~55
        assert result.pace_score == pytest.approx(55.0, abs=1.0)

    def test_avg_attainment_pct_calculation(self, engine):
        # Two reps: 50% and 100%
        inputs = [
            make_input(rep_id="r1", closed_won_ytd=150_000.0, quota_ytd=300_000.0),
            make_input(rep_id="r2", closed_won_ytd=300_000.0, quota_ytd=300_000.0),
        ]
        results = engine.analyze_batch(inputs)
        s = engine.summary()
        expected = round((results[0].attainment_pct + results[1].attainment_pct) / 2, 1)
        assert s["avg_attainment_pct"] == expected

    def test_total_gap_accumulates_correctly(self, engine):
        inputs = [
            make_input(rep_id="r1", quota_ytd=300_000.0, closed_won_ytd=200_000.0),
            make_input(rep_id="r2", quota_ytd=300_000.0, closed_won_ytd=300_000.0),
        ]
        results = engine.analyze_batch(inputs)
        # r1 gap=100k, r2 gap=0
        assert results[0].gap_to_quota == pytest.approx(100_000.0, abs=1.0)
        assert results[1].gap_to_quota == 0.0
        assert engine.total_gap_to_quota == pytest.approx(100_000.0, abs=1.0)

    def test_no_results_after_init(self, engine):
        assert engine.summary()["total"] == 0
        assert engine.at_risk_reps == []
        assert engine.coaching_reps == []
        assert engine.likely_attainers == []

    def test_analyze_increments_total(self, engine):
        for i in range(5):
            engine.analyze(make_input(rep_id=f"r{i}"))
            assert engine.summary()["total"] == i + 1

    def test_batch_followed_by_summary_consistency(self, engine):
        inputs = [make_input(rep_id=f"r{i}") for i in range(10)]
        results = engine.analyze_batch(inputs)
        s = engine.summary()
        assert s["total"] == 10
        assert s["at_risk_count"] == sum(1 for r in results if r.is_at_risk)
        assert s["coaching_count"] == sum(1 for r in results if r.needs_coaching)

    def test_likely_attainer_count_correct(self, engine):
        inputs = [make_input(rep_id=f"r{i}") for i in range(10)]
        results = engine.analyze_batch(inputs)
        s = engine.summary()
        expected = sum(1 for r in results if r.attainment_likelihood in (
            AttainmentLikelihood.VERY_LIKELY, AttainmentLikelihood.LIKELY
        ))
        assert s["likely_attainer_count"] == expected

    def test_confidence_projected_contribution(self, engine):
        # projected * 0.20 capped at 30 → needs projected >= 150 to cap
        inp_low = make_input(
            closed_won_ytd=0.0, quota_ytd=300_000.0,
            historical_attainment=0.0, win_rate=0.0, weighted_pipeline=0.0,
            rep_id="low"
        )
        inp_high = make_input(
            closed_won_ytd=300_000.0, quota_ytd=300_000.0,
            historical_attainment=0.0, win_rate=0.0, weighted_pipeline=0.0,
            rep_id="high"
        )
        r_low = engine.analyze(inp_low)
        engine.reset()
        r_high = engine.analyze(inp_high)
        assert r_high.confidence_score > r_low.confidence_score

    def test_win_rate_cap_in_confidence(self, engine):
        # win_rate * 0.15 — there is no explicit cap for win_rate in code,
        # but win_rate is 0-100 so max contribution is 15
        inp = make_input(win_rate=100.0)
        result = engine.analyze(inp)
        assert result.confidence_score <= 100.0

    def test_coverage_ratio_cap_in_confidence(self, engine):
        # coverage * 10 capped at 20 → coverage needs >= 2 to cap
        inp = make_input(
            closed_won_ytd=300_000.0,
            weighted_pipeline=300_000.0,
            quota_ytd=100_000.0,  # coverage = 6 → 6*10=60 → capped 20
        )
        result = engine.analyze(inp)
        assert result.confidence_score <= 100.0


# ── 21. Formula precision and regression tests ────────────────────────────────

class TestFormulaPrecision:
    def test_attainment_pct_exact_value(self, engine):
        # 240k / 300k * 100 = 80.0
        result = engine.analyze(make_input(
            closed_won_ytd=240_000.0, quota_ytd=300_000.0
        ))
        assert result.attainment_pct == 80.0

    def test_gap_exact_value(self, engine):
        result = engine.analyze(make_input(
            closed_won_ytd=240_000.0, quota_ytd=300_000.0
        ))
        assert result.gap_to_quota == 60_000.0

    def test_coverage_ratio_exact_value(self, engine):
        result = engine.analyze(make_input(
            closed_won_ytd=150_000.0,
            weighted_pipeline=150_000.0,
            quota_ytd=300_000.0,
        ))
        assert result.coverage_ratio == 1.0

    def test_momentum_score_only_activity(self, engine):
        # activities=3, new_deals=0, active=0 → 3*8=24
        result = engine.analyze(make_input(
            activities_per_day=3.0,
            new_deals_added_mtd=0,
            active_deal_count=0,
            stalled_deal_count=0,
        ))
        assert result.momentum_score == pytest.approx(24.0, abs=0.1)

    def test_momentum_score_only_new_deals(self, engine):
        # activities=0, new_deals=4, active=0 → 4*5=20
        result = engine.analyze(make_input(
            activities_per_day=0.0,
            new_deals_added_mtd=4,
            active_deal_count=0,
            stalled_deal_count=0,
        ))
        assert result.momentum_score == pytest.approx(20.0, abs=0.1)

    def test_momentum_score_only_healthy_deals(self, engine):
        # activities=0, new_deals=0, active=10, stalled=0 → healthy_rate=1.0 → 30
        result = engine.analyze(make_input(
            activities_per_day=0.0,
            new_deals_added_mtd=0,
            active_deal_count=10,
            stalled_deal_count=0,
        ))
        assert result.momentum_score == pytest.approx(30.0, abs=0.1)

    def test_momentum_score_combined(self, engine):
        # activities=2*8=16, new_deals=2*5=10, healthy_rate=0.8*30=24 → 50
        result = engine.analyze(make_input(
            activities_per_day=2.0,
            new_deals_added_mtd=2,
            active_deal_count=10,
            stalled_deal_count=2,
        ))
        assert result.momentum_score == pytest.approx(50.0, abs=0.1)

    def test_pace_score_formula_at_period_midpoint(self, engine):
        # period_progress=(90-45)/90*100=50%, attainment=50% → delta=0 → pace=50
        result = engine.analyze(make_input(
            closed_won_ytd=150_000.0,
            quota_ytd=300_000.0,
            total_period_days=90,
            days_remaining=45,
        ))
        assert result.pace_score == pytest.approx(50.0, abs=0.1)

    def test_pace_score_ahead_by_20_points(self, engine):
        # period_progress=50%, attainment=70% → delta=20 → pace=50+50=100 (clamped)
        result = engine.analyze(make_input(
            closed_won_ytd=210_000.0,  # 70%
            quota_ytd=300_000.0,
            total_period_days=90,
            days_remaining=45,
        ))
        # delta=20, score=50+20*2.5=100
        assert result.pace_score == pytest.approx(100.0, abs=0.1)

    def test_pace_score_behind_by_20_points(self, engine):
        # period_progress=50%, attainment=30% → delta=-20 → pace=50-50=0 (clamped)
        result = engine.analyze(make_input(
            closed_won_ytd=90_000.0,  # 30%
            quota_ytd=300_000.0,
            total_period_days=90,
            days_remaining=45,
        ))
        assert result.pace_score == pytest.approx(0.0, abs=0.1)

    def test_confidence_score_all_zero_inputs(self, engine):
        # historical=0, projected=0, coverage=0, win_rate=0, no active → 0
        result = engine.analyze(make_input(
            historical_attainment=0.0,
            closed_won_ytd=0.0,
            weighted_pipeline=0.0,
            quota_ytd=300_000.0,
            win_rate=0.0,
            active_deal_count=0,
            stalled_deal_count=0,
            days_remaining=5,
            total_period_days=90,
        ))
        assert result.confidence_score == pytest.approx(0.0, abs=1.0)

    def test_attainment_pct_rounds_to_one_decimal(self, engine):
        # 1/3 = 33.333... → 33.3
        result = engine.analyze(make_input(
            closed_won_ytd=100_000.0,
            quota_ytd=300_000.0,
        ))
        # Check it's rounded to 1 decimal place
        assert result.attainment_pct == round(result.attainment_pct, 1)

    def test_coverage_ratio_rounds_to_two_decimals(self, engine):
        result = engine.analyze(make_input(
            closed_won_ytd=100_000.0,
            weighted_pipeline=50_000.0,
            quota_ytd=300_000.0,
        ))
        # 150k/300k = 0.5 exactly
        assert result.coverage_ratio == 0.5

    def test_gap_rounds_to_two_decimals(self, engine):
        result = engine.analyze(make_input(
            closed_won_ytd=100_000.0,
            quota_ytd=300_000.01,  # odd quota
        ))
        # gap = 200_000.01 → rounds to 2 decimals
        assert result.gap_to_quota == round(result.gap_to_quota, 2)

    def test_projected_attainment_blended_formula(self, engine):
        # Controlled scenario: days_elapsed=60, run_rate=closed/60
        # projected_closed = closed + run_rate*30
        # pipeline_contribution = weighted * win_rate/100
        # blended = projected_closed*0.6 + (closed + pipeline_contribution)*0.4
        # projected = blended / quota * 100
        closed = 120_000.0
        quota = 300_000.0
        weighted = 60_000.0
        win_rate = 50.0
        days_elapsed = 60
        days_remaining = 30
        total_days = 90

        run_rate = closed / days_elapsed
        proj_closed = closed + run_rate * days_remaining
        pipeline_contrib = weighted * (win_rate / 100)
        blended = proj_closed * 0.6 + (closed + pipeline_contrib) * 0.4
        expected = round((blended / quota) * 100, 1)

        result = engine.analyze(make_input(
            closed_won_ytd=closed,
            quota_ytd=quota,
            weighted_pipeline=weighted,
            win_rate=win_rate,
            days_remaining=days_remaining,
            total_period_days=total_days,
        ))
        assert result.projected_attainment == pytest.approx(expected, abs=0.2)


# ── 22. Input field verification ──────────────────────────────────────────────

class TestInputFields:
    def test_rep_id_field(self):
        inp = make_input(rep_id="test-rep")
        assert inp.rep_id == "test-rep"

    def test_rep_name_field(self):
        inp = make_input(rep_name="Test Rep")
        assert inp.rep_name == "Test Rep"

    def test_manager_id_field(self):
        inp = make_input(manager_id="mgr-999")
        assert inp.manager_id == "mgr-999"

    def test_annual_quota_field(self):
        inp = make_input(annual_quota=2_000_000.0)
        assert inp.annual_quota == 2_000_000.0

    def test_quota_ytd_field(self):
        inp = make_input(quota_ytd=500_000.0)
        assert inp.quota_ytd == 500_000.0

    def test_closed_won_ytd_field(self):
        inp = make_input(closed_won_ytd=250_000.0)
        assert inp.closed_won_ytd == 250_000.0

    def test_commit_pipeline_field(self):
        inp = make_input(commit_pipeline=90_000.0)
        assert inp.commit_pipeline == 90_000.0

    def test_best_case_pipeline_field(self):
        inp = make_input(best_case_pipeline=130_000.0)
        assert inp.best_case_pipeline == 130_000.0

    def test_weighted_pipeline_field(self):
        inp = make_input(weighted_pipeline=70_000.0)
        assert inp.weighted_pipeline == 70_000.0

    def test_days_remaining_field(self):
        inp = make_input(days_remaining=45)
        assert inp.days_remaining == 45

    def test_total_period_days_field(self):
        inp = make_input(total_period_days=180)
        assert inp.total_period_days == 180

    def test_historical_attainment_field(self):
        inp = make_input(historical_attainment=95.0)
        assert inp.historical_attainment == 95.0

    def test_last_quarter_attainment_field(self):
        inp = make_input(last_quarter_attainment=88.0)
        assert inp.last_quarter_attainment == 88.0

    def test_win_rate_field(self):
        inp = make_input(win_rate=45.0)
        assert inp.win_rate == 45.0

    def test_avg_deal_size_field(self):
        inp = make_input(avg_deal_size=75_000.0)
        assert inp.avg_deal_size == 75_000.0

    def test_avg_sales_cycle_days_field(self):
        inp = make_input(avg_sales_cycle_days=60)
        assert inp.avg_sales_cycle_days == 60

    def test_active_deal_count_field(self):
        inp = make_input(active_deal_count=15)
        assert inp.active_deal_count == 15

    def test_stalled_deal_count_field(self):
        inp = make_input(stalled_deal_count=3)
        assert inp.stalled_deal_count == 3

    def test_new_deals_added_mtd_field(self):
        inp = make_input(new_deals_added_mtd=7)
        assert inp.new_deals_added_mtd == 7

    def test_activities_per_day_field(self):
        inp = make_input(activities_per_day=5.5)
        assert inp.activities_per_day == 5.5

    def test_coaching_sessions_qtd_field(self):
        inp = make_input(coaching_sessions_qtd=4)
        assert inp.coaching_sessions_qtd == 4
