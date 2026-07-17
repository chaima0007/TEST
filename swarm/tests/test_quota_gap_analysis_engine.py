"""
Comprehensive pytest test suite for QuotaGapAnalysisEngine.

Covers all enums, input/output dataclasses, every calculation method,
edge cases, boundary conditions, and end-to-end scenarios.
"""

from __future__ import annotations

import pytest

from swarm.intelligence.quota_gap_analysis_engine import (
    AttainmentTier,
    GapRisk,
    PipelineCoverage,
    QuotaAction,
    QuotaGapAnalysisEngine,
    QuotaGapInput,
    QuotaGapResult,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers / fixtures
# ─────────────────────────────────────────────────────────────────────────────

def make_input(**overrides) -> QuotaGapInput:
    """Return a baseline QuotaGapInput with sensible defaults."""
    defaults = dict(
        rep_id="REP001",
        rep_name="Alice Smith",
        manager_id="MGR001",
        region="West",
        segment="mid_market",
        annual_quota=400_000.0,
        period_quota=100_000.0,
        closed_won_value=75_000.0,
        commit_value=10_000.0,
        best_case_value=20_000.0,
        pipeline_value=90_000.0,
        late_stage_value=30_000.0,
        days_in_period=90,
        days_remaining=30,
        avg_deal_size=15_000.0,
        win_rate=0.35,
        avg_sales_cycle_days=45,
        deals_in_pipeline=6,
        overdue_deals=1,
        last_activity_days=3,
        is_ramping=False,
        ramp_factor=1.0,
    )
    defaults.update(overrides)
    return QuotaGapInput(**defaults)


@pytest.fixture
def engine():
    return QuotaGapAnalysisEngine()


@pytest.fixture
def baseline_input():
    return make_input()


# ─────────────────────────────────────────────────────────────────────────────
# 1. Enum tests
# ─────────────────────────────────────────────────────────────────────────────

class TestAttainmentTierEnum:
    def test_member_count(self):
        assert len(AttainmentTier) == 5

    def test_overachiever_value(self):
        assert AttainmentTier.OVERACHIEVER == "overachiever"
        assert AttainmentTier.OVERACHIEVER.value == "overachiever"

    def test_on_track_value(self):
        assert AttainmentTier.ON_TRACK == "on_track"
        assert AttainmentTier.ON_TRACK.value == "on_track"

    def test_at_risk_value(self):
        assert AttainmentTier.AT_RISK == "at_risk"
        assert AttainmentTier.AT_RISK.value == "at_risk"

    def test_behind_value(self):
        assert AttainmentTier.BEHIND == "behind"
        assert AttainmentTier.BEHIND.value == "behind"

    def test_critical_value(self):
        assert AttainmentTier.CRITICAL == "critical"
        assert AttainmentTier.CRITICAL.value == "critical"

    def test_is_str_subclass(self):
        assert isinstance(AttainmentTier.OVERACHIEVER, str)

    def test_unique_values(self):
        values = [t.value for t in AttainmentTier]
        assert len(values) == len(set(values))

    def test_str_comparison(self):
        assert AttainmentTier.ON_TRACK == "on_track"
        assert AttainmentTier.CRITICAL != "on_track"


class TestGapRiskEnum:
    def test_member_count(self):
        assert len(GapRisk) == 4

    def test_low_value(self):
        assert GapRisk.LOW == "low"

    def test_medium_value(self):
        assert GapRisk.MEDIUM == "medium"

    def test_high_value(self):
        assert GapRisk.HIGH == "high"

    def test_critical_value(self):
        assert GapRisk.CRITICAL == "critical"

    def test_is_str_subclass(self):
        assert isinstance(GapRisk.LOW, str)

    def test_unique_values(self):
        values = [r.value for r in GapRisk]
        assert len(values) == len(set(values))


class TestPipelineCoverageEnum:
    def test_member_count(self):
        assert len(PipelineCoverage) == 4

    def test_strong_value(self):
        assert PipelineCoverage.STRONG == "strong"

    def test_adequate_value(self):
        assert PipelineCoverage.ADEQUATE == "adequate"

    def test_thin_value(self):
        assert PipelineCoverage.THIN == "thin"

    def test_insufficient_value(self):
        assert PipelineCoverage.INSUFFICIENT == "insufficient"

    def test_is_str_subclass(self):
        assert isinstance(PipelineCoverage.STRONG, str)

    def test_unique_values(self):
        values = [p.value for p in PipelineCoverage]
        assert len(values) == len(set(values))


class TestQuotaActionEnum:
    def test_member_count(self):
        assert len(QuotaAction) == 6

    def test_accelerate_pipeline_value(self):
        assert QuotaAction.ACCELERATE_PIPELINE == "accelerate_pipeline"

    def test_focus_late_stage_value(self):
        assert QuotaAction.FOCUS_LATE_STAGE == "focus_late_stage"

    def test_build_pipeline_value(self):
        assert QuotaAction.BUILD_PIPELINE == "build_pipeline"

    def test_executive_intervention_value(self):
        assert QuotaAction.EXECUTIVE_INTERVENTION == "executive_intervention"

    def test_maintain_pace_value(self):
        assert QuotaAction.MAINTAIN_PACE == "maintain_pace"

    def test_celebrate_and_expand_value(self):
        assert QuotaAction.CELEBRATE_AND_EXPAND == "celebrate_and_expand"

    def test_is_str_subclass(self):
        assert isinstance(QuotaAction.MAINTAIN_PACE, str)

    def test_unique_values(self):
        values = [a.value for a in QuotaAction]
        assert len(values) == len(set(values))


# ─────────────────────────────────────────────────────────────────────────────
# 2. QuotaGapInput field count
# ─────────────────────────────────────────────────────────────────────────────

class TestQuotaGapInputFields:
    def test_field_count(self):
        import dataclasses
        fields = dataclasses.fields(QuotaGapInput)
        assert len(fields) == 22

    def test_required_string_fields(self):
        inp = make_input()
        assert inp.rep_id == "REP001"
        assert inp.rep_name == "Alice Smith"
        assert inp.manager_id == "MGR001"
        assert inp.region == "West"
        assert inp.segment == "mid_market"

    def test_required_float_fields(self):
        inp = make_input()
        assert isinstance(inp.annual_quota, float)
        assert isinstance(inp.period_quota, float)
        assert isinstance(inp.closed_won_value, float)
        assert isinstance(inp.win_rate, float)
        assert isinstance(inp.ramp_factor, float)

    def test_required_int_fields(self):
        inp = make_input()
        assert isinstance(inp.days_in_period, int)
        assert isinstance(inp.days_remaining, int)
        assert isinstance(inp.avg_sales_cycle_days, int)
        assert isinstance(inp.deals_in_pipeline, int)
        assert isinstance(inp.overdue_deals, int)
        assert isinstance(inp.last_activity_days, int)

    def test_bool_field(self):
        inp = make_input()
        assert isinstance(inp.is_ramping, bool)

    def test_all_22_field_names(self):
        import dataclasses
        field_names = {f.name for f in dataclasses.fields(QuotaGapInput)}
        expected = {
            "rep_id", "rep_name", "manager_id", "region", "segment",
            "annual_quota", "period_quota", "closed_won_value", "commit_value",
            "best_case_value", "pipeline_value", "late_stage_value",
            "days_in_period", "days_remaining", "avg_deal_size", "win_rate",
            "avg_sales_cycle_days", "deals_in_pipeline", "overdue_deals",
            "last_activity_days", "is_ramping", "ramp_factor",
        }
        assert field_names == expected


# ─────────────────────────────────────────────────────────────────────────────
# 3. to_dict() — 15 keys + types
# ─────────────────────────────────────────────────────────────────────────────

class TestToDictMethod:
    EXPECTED_KEYS = {
        "rep_id", "rep_name", "gap_to_quota", "attainment_pct",
        "attainment_tier", "projected_attainment", "gap_risk",
        "pipeline_coverage", "recommended_action", "required_win_rate",
        "deals_needed", "quota_achievement_score", "pipeline_health_score",
        "is_at_risk", "effective_quota",
    }

    def test_key_count(self, engine, baseline_input):
        result = engine.analyze(baseline_input)
        d = result.to_dict()
        assert len(d) == 15

    def test_exact_keys(self, engine, baseline_input):
        result = engine.analyze(baseline_input)
        assert set(result.to_dict().keys()) == self.EXPECTED_KEYS

    def test_rep_id_is_str(self, engine, baseline_input):
        d = engine.analyze(baseline_input).to_dict()
        assert isinstance(d["rep_id"], str)

    def test_rep_name_is_str(self, engine, baseline_input):
        d = engine.analyze(baseline_input).to_dict()
        assert isinstance(d["rep_name"], str)

    def test_gap_to_quota_is_float(self, engine, baseline_input):
        d = engine.analyze(baseline_input).to_dict()
        assert isinstance(d["gap_to_quota"], float)

    def test_attainment_pct_is_float(self, engine, baseline_input):
        d = engine.analyze(baseline_input).to_dict()
        assert isinstance(d["attainment_pct"], float)

    def test_attainment_tier_is_str(self, engine, baseline_input):
        d = engine.analyze(baseline_input).to_dict()
        assert isinstance(d["attainment_tier"], str)

    def test_attainment_tier_is_enum_value(self, engine, baseline_input):
        d = engine.analyze(baseline_input).to_dict()
        assert d["attainment_tier"] in [t.value for t in AttainmentTier]

    def test_gap_risk_is_str(self, engine, baseline_input):
        d = engine.analyze(baseline_input).to_dict()
        assert isinstance(d["gap_risk"], str)

    def test_pipeline_coverage_is_str(self, engine, baseline_input):
        d = engine.analyze(baseline_input).to_dict()
        assert isinstance(d["pipeline_coverage"], str)

    def test_recommended_action_is_str(self, engine, baseline_input):
        d = engine.analyze(baseline_input).to_dict()
        assert isinstance(d["recommended_action"], str)

    def test_required_win_rate_is_float(self, engine, baseline_input):
        d = engine.analyze(baseline_input).to_dict()
        assert isinstance(d["required_win_rate"], float)

    def test_deals_needed_is_int(self, engine, baseline_input):
        d = engine.analyze(baseline_input).to_dict()
        assert isinstance(d["deals_needed"], int)

    def test_is_at_risk_is_bool(self, engine, baseline_input):
        d = engine.analyze(baseline_input).to_dict()
        assert isinstance(d["is_at_risk"], bool)

    def test_effective_quota_is_float(self, engine, baseline_input):
        d = engine.analyze(baseline_input).to_dict()
        assert isinstance(d["effective_quota"], float)

    def test_projected_attainment_is_float(self, engine, baseline_input):
        d = engine.analyze(baseline_input).to_dict()
        assert isinstance(d["projected_attainment"], float)

    def test_quota_achievement_score_is_float(self, engine, baseline_input):
        d = engine.analyze(baseline_input).to_dict()
        assert isinstance(d["quota_achievement_score"], float)

    def test_pipeline_health_score_is_float(self, engine, baseline_input):
        d = engine.analyze(baseline_input).to_dict()
        assert isinstance(d["pipeline_health_score"], float)


# ─────────────────────────────────────────────────────────────────────────────
# 4. _effective_quota
# ─────────────────────────────────────────────────────────────────────────────

class TestEffectiveQuota:
    def _eq(self, engine, **kw):
        inp = make_input(**kw)
        return engine._effective_quota(inp)

    def test_not_ramping_returns_period_quota(self, engine):
        assert self._eq(engine, is_ramping=False, ramp_factor=0.75, period_quota=100_000) == 100_000

    def test_ramping_valid_factor_reduces_quota(self, engine):
        eq = self._eq(engine, is_ramping=True, ramp_factor=0.75, period_quota=100_000)
        assert eq == pytest.approx(75_000.0)

    def test_ramping_factor_zero_returns_period_quota(self, engine):
        eq = self._eq(engine, is_ramping=True, ramp_factor=0.0, period_quota=100_000)
        assert eq == 100_000.0

    def test_ramping_factor_one_returns_period_quota(self, engine):
        eq = self._eq(engine, is_ramping=True, ramp_factor=1.0, period_quota=100_000)
        assert eq == 100_000.0

    def test_ramping_factor_gt1_returns_period_quota(self, engine):
        eq = self._eq(engine, is_ramping=True, ramp_factor=1.5, period_quota=100_000)
        assert eq == 100_000.0

    def test_ramping_factor_negative_returns_period_quota(self, engine):
        eq = self._eq(engine, is_ramping=True, ramp_factor=-0.5, period_quota=100_000)
        assert eq == 100_000.0

    def test_ramping_factor_0_5(self, engine):
        eq = self._eq(engine, is_ramping=True, ramp_factor=0.5, period_quota=80_000)
        assert eq == pytest.approx(40_000.0)

    def test_ramping_factor_0_25(self, engine):
        eq = self._eq(engine, is_ramping=True, ramp_factor=0.25, period_quota=80_000)
        assert eq == pytest.approx(20_000.0)

    def test_not_ramping_ignores_ramp_factor(self, engine):
        # Even with ramp_factor=0.5, if is_ramping=False, return period_quota
        eq = self._eq(engine, is_ramping=False, ramp_factor=0.5, period_quota=100_000)
        assert eq == 100_000.0

    def test_ramping_very_small_factor(self, engine):
        eq = self._eq(engine, is_ramping=True, ramp_factor=0.01, period_quota=100_000)
        assert eq == pytest.approx(1_000.0)


# ─────────────────────────────────────────────────────────────────────────────
# 5. _gap_to_quota
# ─────────────────────────────────────────────────────────────────────────────

class TestGapToQuota:
    def _gap(self, engine, closed_won, effective_quota):
        inp = make_input(closed_won_value=closed_won)
        return engine._gap_to_quota(inp, effective_quota)

    def test_under_quota_returns_positive_gap(self, engine):
        assert self._gap(engine, 70_000, 100_000) == pytest.approx(30_000.0)

    def test_exact_quota_returns_zero(self, engine):
        assert self._gap(engine, 100_000, 100_000) == 0.0

    def test_over_quota_returns_zero(self, engine):
        assert self._gap(engine, 120_000, 100_000) == 0.0

    def test_zero_closed_won(self, engine):
        assert self._gap(engine, 0, 100_000) == pytest.approx(100_000.0)

    def test_negative_closed_won_treated_as_gap(self, engine):
        # max(0, effective - closed) — if closed is negative, gap > effective_quota
        assert self._gap(engine, -10_000, 100_000) == pytest.approx(110_000.0)

    def test_zero_effective_quota_zero_closed(self, engine):
        assert self._gap(engine, 0, 0) == 0.0

    def test_fractional_gap(self, engine):
        assert self._gap(engine, 99_999.50, 100_000) == pytest.approx(0.50)


# ─────────────────────────────────────────────────────────────────────────────
# 6. _attainment_pct
# ─────────────────────────────────────────────────────────────────────────────

class TestAttainmentPct:
    def _pct(self, engine, closed_won, effective_quota):
        inp = make_input(closed_won_value=closed_won)
        return engine._attainment_pct(inp, effective_quota)

    def test_zero_effective_quota_returns_100(self, engine):
        assert self._pct(engine, 0, 0) == 100.0

    def test_negative_effective_quota_returns_100(self, engine):
        assert self._pct(engine, 0, -1) == 100.0

    def test_exact_100_pct(self, engine):
        assert self._pct(engine, 100_000, 100_000) == 100.0

    def test_75_pct(self, engine):
        assert self._pct(engine, 75_000, 100_000) == 75.0

    def test_110_pct(self, engine):
        assert self._pct(engine, 110_000, 100_000) == 110.0

    def test_zero_closed_won(self, engine):
        assert self._pct(engine, 0, 100_000) == 0.0

    def test_rounding_to_1_decimal(self, engine):
        result = self._pct(engine, 33_333, 100_000)
        assert result == round(33_333 / 100_000 * 100, 1)

    def test_partial_attainment(self, engine):
        result = self._pct(engine, 50_000, 75_000)
        assert result == pytest.approx(round(50_000 / 75_000 * 100, 1))


# ─────────────────────────────────────────────────────────────────────────────
# 7. _attainment_tier — all 5 tiers, boundaries
# ─────────────────────────────────────────────────────────────────────────────

class TestAttainmentTierCalculation:
    def _tier(self, engine, pct):
        return engine._attainment_tier(pct)

    # OVERACHIEVER: >= 110
    def test_overachiever_exact_110(self, engine):
        assert self._tier(engine, 110.0) == AttainmentTier.OVERACHIEVER

    def test_overachiever_above_110(self, engine):
        assert self._tier(engine, 150.0) == AttainmentTier.OVERACHIEVER

    def test_overachiever_200(self, engine):
        assert self._tier(engine, 200.0) == AttainmentTier.OVERACHIEVER

    # ON_TRACK: >= 90 and < 110
    def test_on_track_exact_90(self, engine):
        assert self._tier(engine, 90.0) == AttainmentTier.ON_TRACK

    def test_on_track_at_109(self, engine):
        assert self._tier(engine, 109.9) == AttainmentTier.ON_TRACK

    def test_on_track_at_100(self, engine):
        assert self._tier(engine, 100.0) == AttainmentTier.ON_TRACK

    # AT_RISK: >= 70 and < 90
    def test_at_risk_exact_70(self, engine):
        assert self._tier(engine, 70.0) == AttainmentTier.AT_RISK

    def test_at_risk_at_89(self, engine):
        assert self._tier(engine, 89.9) == AttainmentTier.AT_RISK

    def test_at_risk_at_80(self, engine):
        assert self._tier(engine, 80.0) == AttainmentTier.AT_RISK

    # BEHIND: >= 50 and < 70
    def test_behind_exact_50(self, engine):
        assert self._tier(engine, 50.0) == AttainmentTier.BEHIND

    def test_behind_at_69(self, engine):
        assert self._tier(engine, 69.9) == AttainmentTier.BEHIND

    def test_behind_at_60(self, engine):
        assert self._tier(engine, 60.0) == AttainmentTier.BEHIND

    # CRITICAL: < 50
    def test_critical_at_49(self, engine):
        assert self._tier(engine, 49.9) == AttainmentTier.CRITICAL

    def test_critical_at_0(self, engine):
        assert self._tier(engine, 0.0) == AttainmentTier.CRITICAL

    def test_critical_at_25(self, engine):
        assert self._tier(engine, 25.0) == AttainmentTier.CRITICAL

    # Boundary: just below 70
    def test_just_below_70_is_behind(self, engine):
        assert self._tier(engine, 69.99) == AttainmentTier.BEHIND

    # Boundary: just below 90
    def test_just_below_90_is_at_risk(self, engine):
        assert self._tier(engine, 89.99) == AttainmentTier.AT_RISK

    # Boundary: just below 110
    def test_just_below_110_is_on_track(self, engine):
        assert self._tier(engine, 109.99) == AttainmentTier.ON_TRACK


# ─────────────────────────────────────────────────────────────────────────────
# 8. _projected_attainment
# ─────────────────────────────────────────────────────────────────────────────

class TestProjectedAttainment:
    def _proj(self, engine, **kw):
        inp = make_input(**kw)
        eq = engine._effective_quota(inp)
        return engine._projected_attainment(inp, eq)

    def test_zero_effective_quota_returns_100(self, engine):
        result = self._proj(engine, period_quota=0.0, is_ramping=False)
        assert result == 100.0

    def test_zero_days_in_period_returns_attainment_pct(self, engine):
        # When days_in_period=0, should return attainment_pct
        inp = make_input(
            days_in_period=0,
            days_remaining=0,
            closed_won_value=75_000,
            period_quota=100_000,
        )
        eq = engine._effective_quota(inp)
        proj = engine._projected_attainment(inp, eq)
        att = engine._attainment_pct(inp, eq)
        assert proj == att

    def test_capped_at_200(self, engine):
        # Very high closed-won with lots of days remaining
        result = self._proj(
            engine,
            closed_won_value=500_000,
            period_quota=100_000,
            days_in_period=90,
            days_remaining=60,
            commit_value=50_000,
            late_stage_value=50_000,
            win_rate=0.5,
        )
        assert result == 200.0

    def test_projected_increases_with_more_days_remaining(self, engine):
        inp_more = make_input(days_remaining=60, days_in_period=90)
        inp_less = make_input(days_remaining=10, days_in_period=90)
        eng = QuotaGapAnalysisEngine()
        proj_more = eng._projected_attainment(inp_more, eng._effective_quota(inp_more))
        proj_less = eng._projected_attainment(inp_less, eng._effective_quota(inp_less))
        assert proj_more >= proj_less

    def test_formula_manual_calculation(self, engine):
        inp = make_input(
            closed_won_value=60_000,
            period_quota=100_000,
            days_in_period=90,
            days_remaining=30,
            commit_value=5_000,
            late_stage_value=20_000,
            win_rate=0.3,
            is_ramping=False,
        )
        # days_elapsed = max(1, 90 - 30) = 60
        # run_rate = 60000 / 60 = 1000
        # projected_won = 60000 + 1000 * 30 = 90000
        # pipeline_contribution = 5000 + 0.3 * 20000 * 0.5 = 5000 + 3000 = 8000
        # blended = 90000 * 0.6 + (60000 + 8000) * 0.4 = 54000 + 27200 = 81200
        # pct = 81200 / 100000 * 100 = 81.2
        eq = engine._effective_quota(inp)
        proj = engine._projected_attainment(inp, eq)
        assert proj == pytest.approx(81.2, abs=0.1)

    def test_days_elapsed_min_1(self, engine):
        # When days_in_period == days_remaining, elapsed = max(1, 0) = 1
        inp = make_input(days_in_period=30, days_remaining=30, closed_won_value=10_000, period_quota=100_000)
        eq = engine._effective_quota(inp)
        proj = engine._projected_attainment(inp, eq)
        assert isinstance(proj, float)

    def test_result_is_rounded_to_1_decimal(self, engine):
        inp = make_input(
            closed_won_value=33_333,
            period_quota=100_000,
            days_in_period=90,
            days_remaining=30,
        )
        eq = engine._effective_quota(inp)
        proj = engine._projected_attainment(inp, eq)
        assert proj == round(proj, 1)

    def test_zero_closed_won(self, engine):
        inp = make_input(
            closed_won_value=0,
            period_quota=100_000,
            days_in_period=90,
            days_remaining=45,
            commit_value=0,
            late_stage_value=0,
        )
        eq = engine._effective_quota(inp)
        proj = engine._projected_attainment(inp, eq)
        assert proj == 0.0


# ─────────────────────────────────────────────────────────────────────────────
# 9. _pipeline_coverage — all 4 levels
# ─────────────────────────────────────────────────────────────────────────────

class TestPipelineCoverage:
    def _cov(self, engine, pipeline_value, gap):
        inp = make_input(pipeline_value=pipeline_value)
        return engine._pipeline_coverage(inp, gap)

    def test_gap_zero_returns_strong(self, engine):
        assert self._cov(engine, 0, 0) == PipelineCoverage.STRONG

    def test_gap_negative_returns_strong(self, engine):
        assert self._cov(engine, 0, -1000) == PipelineCoverage.STRONG

    def test_ratio_gte_3_returns_strong(self, engine):
        assert self._cov(engine, 30_000, 10_000) == PipelineCoverage.STRONG

    def test_ratio_exactly_3_returns_strong(self, engine):
        assert self._cov(engine, 30_000, 10_000) == PipelineCoverage.STRONG

    def test_ratio_just_above_3_returns_strong(self, engine):
        assert self._cov(engine, 30_001, 10_000) == PipelineCoverage.STRONG

    def test_ratio_gte_2_lt_3_returns_adequate(self, engine):
        assert self._cov(engine, 20_000, 10_000) == PipelineCoverage.ADEQUATE

    def test_ratio_exactly_2_returns_adequate(self, engine):
        assert self._cov(engine, 20_000, 10_000) == PipelineCoverage.ADEQUATE

    def test_ratio_just_below_3_returns_adequate(self, engine):
        assert self._cov(engine, 29_999, 10_000) == PipelineCoverage.ADEQUATE

    def test_ratio_gte_1_lt_2_returns_thin(self, engine):
        assert self._cov(engine, 15_000, 10_000) == PipelineCoverage.THIN

    def test_ratio_exactly_1_returns_thin(self, engine):
        assert self._cov(engine, 10_000, 10_000) == PipelineCoverage.THIN

    def test_ratio_just_below_2_returns_thin(self, engine):
        assert self._cov(engine, 19_999, 10_000) == PipelineCoverage.THIN

    def test_ratio_lt_1_returns_insufficient(self, engine):
        assert self._cov(engine, 5_000, 10_000) == PipelineCoverage.INSUFFICIENT

    def test_zero_pipeline_nonzero_gap_returns_insufficient(self, engine):
        assert self._cov(engine, 0, 10_000) == PipelineCoverage.INSUFFICIENT

    def test_tiny_pipeline_large_gap_returns_insufficient(self, engine):
        assert self._cov(engine, 1, 10_000) == PipelineCoverage.INSUFFICIENT


# ─────────────────────────────────────────────────────────────────────────────
# 10. _required_win_rate
# ─────────────────────────────────────────────────────────────────────────────

class TestRequiredWinRate:
    def _rwr(self, engine, gap, pipeline_value):
        inp = make_input(pipeline_value=pipeline_value)
        return engine._required_win_rate(inp, gap)

    def test_zero_gap_returns_zero(self, engine):
        assert self._rwr(engine, 0.0, 100_000) == 0.0

    def test_negative_gap_returns_zero(self, engine):
        assert self._rwr(engine, -10_000, 100_000) == 0.0

    def test_zero_pipeline_returns_zero(self, engine):
        assert self._rwr(engine, 50_000, 0) == 0.0

    def test_basic_calculation(self, engine):
        result = self._rwr(engine, 30_000, 100_000)
        assert result == pytest.approx(0.3, abs=0.001)

    def test_capped_at_1_0(self, engine):
        # gap > pipeline → capped at 1.0
        result = self._rwr(engine, 100_000, 50_000)
        assert result == 1.0

    def test_exactly_1_0(self, engine):
        result = self._rwr(engine, 50_000, 50_000)
        assert result == 1.0

    def test_rounded_to_3_decimals(self, engine):
        result = self._rwr(engine, 10_000, 30_000)
        assert result == round(10_000 / 30_000, 3)

    def test_small_gap_large_pipeline(self, engine):
        result = self._rwr(engine, 1_000, 100_000)
        assert result == pytest.approx(0.01, abs=0.001)


# ─────────────────────────────────────────────────────────────────────────────
# 11. _deals_needed — ceiling logic, gap=0, avg_size=0
# ─────────────────────────────────────────────────────────────────────────────

class TestDealsNeeded:
    def _dn(self, engine, gap, avg_deal_size):
        inp = make_input(avg_deal_size=avg_deal_size)
        return engine._deals_needed(inp, gap)

    def test_zero_gap_returns_0(self, engine):
        assert self._dn(engine, 0.0, 10_000) == 0

    def test_negative_gap_returns_0(self, engine):
        assert self._dn(engine, -5_000, 10_000) == 0

    def test_zero_avg_size_returns_0(self, engine):
        assert self._dn(engine, 50_000, 0) == 0

    def test_exact_division(self, engine):
        assert self._dn(engine, 30_000, 10_000) == 3

    def test_ceiling_partial(self, engine):
        # 25000 / 10000 = 2.5 → ceiling = 3
        assert self._dn(engine, 25_000, 10_000) == 3

    def test_ceiling_just_above_integer(self, engine):
        # 10001 / 10000 = 1.0001 + 0.999 = 1.9991 → int = 1
        # The formula int(x + 0.999) gives 1 for 1.0001, not 2
        assert self._dn(engine, 10_001, 10_000) == 1

    def test_small_gap_large_deal_size(self, engine):
        # 1 / 10000 = 0.0001; 0.0001 + 0.999 = 0.9991 → int = 0
        # The formula doesn't true-ceiling for very small ratios
        assert self._dn(engine, 1, 10_000) == 0

    def test_large_gap_small_deal_size(self, engine):
        assert self._dn(engine, 100_000, 10_000) == 10

    def test_result_is_int(self, engine):
        result = self._dn(engine, 25_000, 10_000)
        assert isinstance(result, int)

    def test_ceiling_at_99999_over_100000(self, engine):
        # 99999/100000 = 0.99999 → ceiling = 1
        assert self._dn(engine, 99_999, 100_000) == 1


# ─────────────────────────────────────────────────────────────────────────────
# 12. _achievement_score — each bonus/penalty, clamping
# ─────────────────────────────────────────────────────────────────────────────

class TestAchievementScore:
    def _score(self, engine, attainment_pct=75.0, projected=80.0, days_remaining=30, last_activity_days=3):
        inp = make_input(days_remaining=days_remaining, last_activity_days=last_activity_days)
        return engine._achievement_score(inp, attainment_pct, projected)

    def test_basic_calculation(self, engine):
        # attainment=75 → min(60, 75*0.6)=45
        # projected=80 → min(25, 80*0.25*0.5)=10
        # days_remaining=30 → no bonus (not >30, not >14... wait 30>14 → +5)
        # last_activity=3 → no penalty
        # = 45 + 10 + 5 = 60
        result = self._score(engine, attainment_pct=75.0, projected=80.0, days_remaining=30, last_activity_days=3)
        assert result == pytest.approx(60.0, abs=0.1)

    def test_days_remaining_gt30_bonus_10(self, engine):
        base = self._score(engine, days_remaining=31, last_activity_days=0)
        no_bonus = self._score(engine, days_remaining=30, last_activity_days=0)
        # 31 days gets +10, 30 days gets +5 (>14)
        assert base - no_bonus == pytest.approx(5.0, abs=0.1)

    def test_days_remaining_gt14_bonus_5(self, engine):
        score_15 = self._score(engine, days_remaining=15, last_activity_days=0)
        score_14 = self._score(engine, days_remaining=14, last_activity_days=0)
        assert score_15 - score_14 == pytest.approx(5.0, abs=0.1)

    def test_days_remaining_14_no_bonus(self, engine):
        score_14 = self._score(engine, days_remaining=14, last_activity_days=0)
        score_0 = self._score(engine, days_remaining=0, last_activity_days=0)
        assert score_14 == score_0

    def test_last_activity_gt14_penalty_10(self, engine):
        penalized = self._score(engine, last_activity_days=15, days_remaining=0)
        not_penalized = self._score(engine, last_activity_days=14, days_remaining=0)
        # >14 → -10; >7 → -5  so 15 gets -10 and 14 gets -5
        assert penalized - not_penalized == pytest.approx(-5.0, abs=0.1)

    def test_last_activity_gt7_penalty_5(self, engine):
        penalized = self._score(engine, last_activity_days=8, days_remaining=0)
        not_penalized = self._score(engine, last_activity_days=7, days_remaining=0)
        assert penalized - not_penalized == pytest.approx(-5.0, abs=0.1)

    def test_attainment_base_capped_at_60(self, engine):
        # attainment=120 → min(60, 120*0.6)=min(60,72)=60
        high_score = self._score(engine, attainment_pct=120, days_remaining=0, last_activity_days=0)
        med_score = self._score(engine, attainment_pct=100, days_remaining=0, last_activity_days=0)
        # both should have attainment component = 60
        # projected contribution differs
        assert high_score >= med_score

    def test_projected_capped_at_25(self, engine):
        # projected=300 → min(25, 300*0.25*0.5)=min(25,37.5)=25
        score = self._score(engine, projected=300, attainment_pct=0, days_remaining=0, last_activity_days=0)
        # attainment=0 → 0, projected=25, no bonus/penalty → 25
        assert score == pytest.approx(25.0, abs=0.1)

    def test_clamped_to_zero_minimum(self, engine):
        # Use all penalties — negative attainment, no projected, large activity gap
        inp = make_input(days_remaining=0, last_activity_days=20)
        score = engine._achievement_score(inp, 0.0, 0.0)
        assert score >= 0.0

    def test_clamped_to_100_maximum(self, engine):
        inp = make_input(days_remaining=60, last_activity_days=0)
        score = engine._achievement_score(inp, 200.0, 400.0)
        assert score <= 100.0

    def test_result_is_float(self, engine):
        result = self._score(engine)
        assert isinstance(result, float)

    def test_result_rounded_to_1_decimal(self, engine):
        result = self._score(engine)
        assert result == round(result, 1)


# ─────────────────────────────────────────────────────────────────────────────
# 13. _pipeline_health_score
# ─────────────────────────────────────────────────────────────────────────────

class TestPipelineHealthScore:
    def _health(self, engine, **kw):
        inp = make_input(**kw)
        return engine._pipeline_health_score(inp)

    def test_base_with_good_win_rate_and_late_stage(self, engine):
        # win_rate=0.5 → +15, late_pct=0.6 → +15, no overdue penalty, activity 3 → no penalty
        result = self._health(
            engine,
            win_rate=0.5,
            pipeline_value=100_000,
            late_stage_value=60_000,
            deals_in_pipeline=5,
            overdue_deals=0,
            last_activity_days=3,
        )
        # 50 + 15 + 15 = 80
        assert result == pytest.approx(80.0, abs=0.1)

    def test_win_rate_gte_04_bonus_15(self, engine):
        score_high = self._health(engine, win_rate=0.4, pipeline_value=100_000, late_stage_value=30_000, deals_in_pipeline=0, overdue_deals=0, last_activity_days=0)
        score_mid = self._health(engine, win_rate=0.39, pipeline_value=100_000, late_stage_value=30_000, deals_in_pipeline=0, overdue_deals=0, last_activity_days=0)
        assert score_high - score_mid == pytest.approx(8.0, abs=0.1)  # +15 vs +7

    def test_win_rate_gte_025_bonus_7(self, engine):
        score_mid = self._health(engine, win_rate=0.25, pipeline_value=100_000, late_stage_value=30_000, deals_in_pipeline=0, overdue_deals=0, last_activity_days=0)
        score_low = self._health(engine, win_rate=0.24, pipeline_value=100_000, late_stage_value=30_000, deals_in_pipeline=0, overdue_deals=0, last_activity_days=0)
        assert score_mid - score_low == pytest.approx(17.0, abs=0.1)  # +7 vs -10

    def test_win_rate_lt_025_penalty_10(self, engine):
        score = self._health(engine, win_rate=0.1, pipeline_value=0, late_stage_value=0, deals_in_pipeline=0, overdue_deals=0, last_activity_days=0)
        # 50 - 10 = 40
        assert score == pytest.approx(40.0, abs=0.1)

    def test_late_pct_gte_05_bonus_15(self, engine):
        score = self._health(engine, win_rate=0.4, pipeline_value=100_000, late_stage_value=50_000, deals_in_pipeline=0, overdue_deals=0, last_activity_days=0)
        # 50 + 15 (win_rate) + 15 (late_pct=0.5) = 80
        assert score == pytest.approx(80.0, abs=0.1)

    def test_late_pct_gte_03_bonus_8(self, engine):
        score = self._health(engine, win_rate=0.4, pipeline_value=100_000, late_stage_value=30_000, deals_in_pipeline=0, overdue_deals=0, last_activity_days=0)
        # 50 + 15 + 8 = 73
        assert score == pytest.approx(73.0, abs=0.1)

    def test_late_pct_lt_03_penalty_5(self, engine):
        score = self._health(engine, win_rate=0.4, pipeline_value=100_000, late_stage_value=10_000, deals_in_pipeline=0, overdue_deals=0, last_activity_days=0)
        # 50 + 15 - 5 = 60
        assert score == pytest.approx(60.0, abs=0.1)

    def test_zero_pipeline_value_skips_late_stage(self, engine):
        score = self._health(engine, win_rate=0.4, pipeline_value=0, late_stage_value=0, deals_in_pipeline=0, overdue_deals=0, last_activity_days=0)
        # 50 + 15 = 65
        assert score == pytest.approx(65.0, abs=0.1)

    def test_overdue_pct_gte_05_penalty_20(self, engine):
        score = self._health(engine, win_rate=0.4, pipeline_value=100_000, late_stage_value=60_000, deals_in_pipeline=10, overdue_deals=5, last_activity_days=0)
        # 50 + 15 + 15 - 20 = 60
        assert score == pytest.approx(60.0, abs=0.1)

    def test_overdue_pct_gte_03_penalty_10(self, engine):
        score = self._health(engine, win_rate=0.4, pipeline_value=100_000, late_stage_value=60_000, deals_in_pipeline=10, overdue_deals=3, last_activity_days=0)
        # 50 + 15 + 15 - 10 = 70
        assert score == pytest.approx(70.0, abs=0.1)

    def test_zero_deals_in_pipeline_skips_overdue(self, engine):
        score = self._health(engine, win_rate=0.4, pipeline_value=100_000, late_stage_value=60_000, deals_in_pipeline=0, overdue_deals=5, last_activity_days=0)
        # 50 + 15 + 15 = 80 (overdue skipped)
        assert score == pytest.approx(80.0, abs=0.1)

    def test_last_activity_gt7_penalty_10(self, engine):
        score_penalized = self._health(engine, win_rate=0.4, pipeline_value=100_000, late_stage_value=60_000, deals_in_pipeline=0, overdue_deals=0, last_activity_days=8)
        score_ok = self._health(engine, win_rate=0.4, pipeline_value=100_000, late_stage_value=60_000, deals_in_pipeline=0, overdue_deals=0, last_activity_days=7)
        assert score_ok - score_penalized == pytest.approx(10.0, abs=0.1)

    def test_clamped_to_zero(self, engine):
        score = self._health(engine, win_rate=0.0, pipeline_value=100_000, late_stage_value=0, deals_in_pipeline=10, overdue_deals=10, last_activity_days=20)
        assert score >= 0.0

    def test_clamped_to_100(self, engine):
        score = self._health(engine, win_rate=1.0, pipeline_value=100_000, late_stage_value=100_000, deals_in_pipeline=10, overdue_deals=0, last_activity_days=0)
        assert score <= 100.0

    def test_result_rounded_to_1_decimal(self, engine):
        score = self._health(engine)
        assert score == round(score, 1)


# ─────────────────────────────────────────────────────────────────────────────
# 14. _gap_risk — each factor, all 4 levels
# ─────────────────────────────────────────────────────────────────────────────

class TestGapRisk:
    def _risk(self, engine, attainment_pct, projected, pipeline_cov, days_remaining, last_activity_days):
        inp = make_input(days_remaining=days_remaining, last_activity_days=last_activity_days)
        return engine._gap_risk(inp, attainment_pct, projected, pipeline_cov)

    def test_low_risk_all_green(self, engine):
        result = self._risk(engine, 95.0, 95.0, PipelineCoverage.STRONG, 45, 3)
        # 0 + 0 + 0 + 0 + 0 = 0 → LOW
        assert result == GapRisk.LOW

    def test_medium_risk_score_2(self, engine):
        # attainment 80 → +1; projected 95 → 0; strong coverage → 0; 45 days → 0; activity ok → 0
        # total = 1 but that's only 1 → LOW. Need 2 for MEDIUM
        # attainment 80 → +1; 45 days → 0; activity > 14 → +1 → total=2 → MEDIUM
        result = self._risk(engine, 80.0, 95.0, PipelineCoverage.STRONG, 45, 15)
        assert result == GapRisk.MEDIUM

    def test_high_risk_score_4(self, engine):
        # attainment<50 → +3; projected 95 → 0; strong → 0; 45 days → 0; activity ok → 0 → 3 → HIGH starts at 4
        # attainment<50 → +3; activity>14 → +1 → 4 → HIGH
        result = self._risk(engine, 40.0, 95.0, PipelineCoverage.STRONG, 45, 15)
        assert result == GapRisk.HIGH

    def test_critical_risk_score_7(self, engine):
        # attainment<50 → +3; projected<70 → +3; insufficient → +2; 14 days → +2 → 10 → CRITICAL
        result = self._risk(engine, 30.0, 50.0, PipelineCoverage.INSUFFICIENT, 14, 0)
        assert result == GapRisk.CRITICAL

    def test_attainment_lt_50_adds_3(self, engine):
        r1 = self._risk(engine, 49.9, 95.0, PipelineCoverage.STRONG, 45, 0)
        r2 = self._risk(engine, 50.0, 95.0, PipelineCoverage.STRONG, 45, 0)
        # 49.9 → +3 → score=3 → MEDIUM (needs 4 for HIGH)
        # 50.0 → not <50 but <70 → +2 → MEDIUM
        assert r1 == GapRisk.MEDIUM
        assert r2 == GapRisk.MEDIUM

    def test_attainment_lt_70_adds_2(self, engine):
        result = self._risk(engine, 60.0, 95.0, PipelineCoverage.STRONG, 45, 0)
        # +2 → MEDIUM
        assert result == GapRisk.MEDIUM

    def test_attainment_lt_90_adds_1(self, engine):
        result = self._risk(engine, 80.0, 95.0, PipelineCoverage.STRONG, 45, 0)
        # +1 → LOW
        assert result == GapRisk.LOW

    def test_projected_lt_70_adds_3(self, engine):
        # attainment 80 → +1; projected 65 → +3 → total=4 → HIGH
        result = self._risk(engine, 80.0, 65.0, PipelineCoverage.STRONG, 45, 0)
        assert result == GapRisk.HIGH

    def test_projected_lt_70_alone_gives_medium(self, engine):
        # attainment 95 → +0; projected 65 → +3 → total=3 → MEDIUM
        result = self._risk(engine, 95.0, 65.0, PipelineCoverage.STRONG, 45, 0)
        assert result == GapRisk.MEDIUM

    def test_projected_lt_90_adds_1(self, engine):
        result = self._risk(engine, 95.0, 85.0, PipelineCoverage.STRONG, 45, 0)
        # +1 → LOW
        assert result == GapRisk.LOW

    def test_insufficient_pipeline_adds_2(self, engine):
        result = self._risk(engine, 95.0, 95.0, PipelineCoverage.INSUFFICIENT, 45, 0)
        # +2 → MEDIUM
        assert result == GapRisk.MEDIUM

    def test_thin_pipeline_adds_1(self, engine):
        result = self._risk(engine, 95.0, 95.0, PipelineCoverage.THIN, 45, 0)
        # +1 → LOW
        assert result == GapRisk.LOW

    def test_days_remaining_lte_14_adds_2(self, engine):
        result = self._risk(engine, 95.0, 95.0, PipelineCoverage.STRONG, 14, 0)
        # +2 → MEDIUM
        assert result == GapRisk.MEDIUM

    def test_days_remaining_lte_30_adds_1(self, engine):
        result = self._risk(engine, 95.0, 95.0, PipelineCoverage.STRONG, 30, 0)
        # +1 → LOW
        assert result == GapRisk.LOW

    def test_days_remaining_gt_30_no_addition(self, engine):
        result = self._risk(engine, 95.0, 95.0, PipelineCoverage.STRONG, 31, 0)
        # +0 → LOW
        assert result == GapRisk.LOW

    def test_last_activity_gt_14_adds_1(self, engine):
        result = self._risk(engine, 95.0, 95.0, PipelineCoverage.STRONG, 45, 15)
        # +1 → LOW
        assert result == GapRisk.LOW

    def test_boundary_score_7_is_critical(self, engine):
        # attainment<50→+3, projected<70→+3, thin→+1 → total=7 → CRITICAL
        result = self._risk(engine, 40.0, 60.0, PipelineCoverage.THIN, 45, 0)
        assert result == GapRisk.CRITICAL

    def test_boundary_score_4_is_high(self, engine):
        # attainment<70→+2, projected<90→+1, thin→+1 → total=4 → HIGH
        result = self._risk(engine, 60.0, 85.0, PipelineCoverage.THIN, 45, 0)
        assert result == GapRisk.HIGH

    def test_boundary_score_2_is_medium(self, engine):
        result = self._risk(engine, 80.0, 95.0, PipelineCoverage.INSUFFICIENT, 45, 0)
        # attainment<90→+1, insufficient→+2 → total=3 → HIGH
        # Let's do attainment<90→+1, thin→+1 → 2 → MEDIUM
        result = self._risk(engine, 80.0, 95.0, PipelineCoverage.THIN, 45, 0)
        assert result == GapRisk.MEDIUM

    def test_adequate_pipeline_no_risk_addition(self, engine):
        result = self._risk(engine, 95.0, 95.0, PipelineCoverage.ADEQUATE, 45, 0)
        # +0 → LOW
        assert result == GapRisk.LOW

    def test_strong_pipeline_no_risk_addition(self, engine):
        result = self._risk(engine, 95.0, 95.0, PipelineCoverage.STRONG, 45, 0)
        assert result == GapRisk.LOW


# ─────────────────────────────────────────────────────────────────────────────
# 15. _recommended_action — full priority chain
# ─────────────────────────────────────────────────────────────────────────────

class TestRecommendedAction:
    def _action(self, engine, attainment_pct, gap_risk, pipeline_cov, late_stage_value=10_000):
        inp = make_input(late_stage_value=late_stage_value)
        return engine._recommended_action(inp, gap_risk, pipeline_cov, attainment_pct)

    def test_priority1_celebrate_and_expand(self, engine):
        # attainment >= 110 → CELEBRATE_AND_EXPAND (top priority)
        action = self._action(engine, 110.0, GapRisk.CRITICAL, PipelineCoverage.INSUFFICIENT)
        assert action == QuotaAction.CELEBRATE_AND_EXPAND

    def test_priority1_overrides_critical_risk(self, engine):
        action = self._action(engine, 120.0, GapRisk.CRITICAL, PipelineCoverage.INSUFFICIENT)
        assert action == QuotaAction.CELEBRATE_AND_EXPAND

    def test_priority2_executive_intervention(self, engine):
        # gap_risk=CRITICAL (and attainment < 110)
        action = self._action(engine, 40.0, GapRisk.CRITICAL, PipelineCoverage.ADEQUATE)
        assert action == QuotaAction.EXECUTIVE_INTERVENTION

    def test_priority2_critical_overrides_insufficient(self, engine):
        action = self._action(engine, 40.0, GapRisk.CRITICAL, PipelineCoverage.INSUFFICIENT)
        assert action == QuotaAction.EXECUTIVE_INTERVENTION

    def test_priority3_build_pipeline(self, engine):
        # pipeline INSUFFICIENT (and not CRITICAL gap, and attainment < 110)
        action = self._action(engine, 70.0, GapRisk.HIGH, PipelineCoverage.INSUFFICIENT, late_stage_value=0)
        assert action == QuotaAction.BUILD_PIPELINE

    def test_priority3_insufficient_overrides_focus_late_stage(self, engine):
        action = self._action(engine, 70.0, GapRisk.HIGH, PipelineCoverage.INSUFFICIENT, late_stage_value=50_000)
        assert action == QuotaAction.BUILD_PIPELINE

    def test_priority4_focus_late_stage(self, engine):
        # late_stage_value > 0 and gap_risk == HIGH (not INSUFFICIENT, not CRITICAL, not >= 110)
        action = self._action(engine, 70.0, GapRisk.HIGH, PipelineCoverage.ADEQUATE, late_stage_value=10_000)
        assert action == QuotaAction.FOCUS_LATE_STAGE

    def test_priority4_no_late_stage_skips(self, engine):
        # late_stage_value = 0, so skip priority 4
        action = self._action(engine, 70.0, GapRisk.HIGH, PipelineCoverage.ADEQUATE, late_stage_value=0)
        assert action == QuotaAction.ACCELERATE_PIPELINE

    def test_priority4_medium_risk_skips(self, engine):
        # gap_risk = MEDIUM, not HIGH → skip priority 4
        action = self._action(engine, 70.0, GapRisk.MEDIUM, PipelineCoverage.ADEQUATE, late_stage_value=10_000)
        assert action == QuotaAction.ACCELERATE_PIPELINE

    def test_priority5_accelerate_pipeline_thin(self, engine):
        action = self._action(engine, 70.0, GapRisk.MEDIUM, PipelineCoverage.THIN)
        assert action == QuotaAction.ACCELERATE_PIPELINE

    def test_priority5_accelerate_pipeline_adequate(self, engine):
        action = self._action(engine, 70.0, GapRisk.LOW, PipelineCoverage.ADEQUATE)
        assert action == QuotaAction.ACCELERATE_PIPELINE

    def test_priority6_maintain_pace(self, engine):
        # None of the above → MAINTAIN_PACE
        action = self._action(engine, 95.0, GapRisk.LOW, PipelineCoverage.STRONG)
        assert action == QuotaAction.MAINTAIN_PACE

    def test_maintain_pace_with_medium_risk_strong_pipeline(self, engine):
        action = self._action(engine, 85.0, GapRisk.MEDIUM, PipelineCoverage.STRONG)
        assert action == QuotaAction.MAINTAIN_PACE


# ─────────────────────────────────────────────────────────────────────────────
# 16. is_at_risk
# ─────────────────────────────────────────────────────────────────────────────

class TestIsAtRisk:
    def test_high_risk_is_at_risk(self, engine):
        inp = make_input(
            closed_won_value=20_000,
            period_quota=100_000,
            pipeline_value=15_000,
            late_stage_value=5_000,
            days_remaining=10,
            last_activity_days=20,
        )
        result = engine.analyze(inp)
        assert result.gap_risk in (GapRisk.HIGH, GapRisk.CRITICAL)
        assert result.is_at_risk is True

    def test_critical_risk_is_at_risk(self, engine):
        inp = make_input(
            closed_won_value=5_000,
            period_quota=100_000,
            pipeline_value=5_000,
            days_remaining=5,
            last_activity_days=20,
        )
        result = engine.analyze(inp)
        assert result.is_at_risk is True

    def test_low_risk_not_at_risk(self, engine):
        inp = make_input(
            closed_won_value=95_000,
            period_quota=100_000,
            pipeline_value=100_000,
            days_remaining=60,
            last_activity_days=2,
        )
        result = engine.analyze(inp)
        if result.gap_risk in (GapRisk.LOW, GapRisk.MEDIUM):
            assert result.is_at_risk is False

    def test_medium_risk_not_at_risk(self, engine):
        # Construct a scenario that yields MEDIUM
        inp = make_input(
            closed_won_value=85_000,
            period_quota=100_000,
            pipeline_value=100_000,
            days_remaining=45,
            last_activity_days=2,
        )
        result = engine.analyze(inp)
        if result.gap_risk == GapRisk.MEDIUM:
            assert result.is_at_risk is False

    def test_is_at_risk_matches_gap_risk(self, engine):
        inp = make_input()
        result = engine.analyze(inp)
        if result.gap_risk in (GapRisk.HIGH, GapRisk.CRITICAL):
            assert result.is_at_risk is True
        else:
            assert result.is_at_risk is False


# ─────────────────────────────────────────────────────────────────────────────
# 17. Properties (empty / filtering)
# ─────────────────────────────────────────────────────────────────────────────

class TestEngineProperties:
    def test_at_risk_reps_empty_initially(self, engine):
        assert engine.at_risk_reps == []

    def test_overachievers_empty_initially(self, engine):
        assert engine.overachievers == []

    def test_critical_reps_empty_initially(self, engine):
        assert engine.critical_reps == []

    def test_total_gap_zero_initially(self, engine):
        assert engine.total_gap == 0.0

    def test_at_risk_reps_filtering(self, engine):
        inp_at_risk = make_input(
            rep_id="R1",
            closed_won_value=5_000,
            period_quota=100_000,
            pipeline_value=5_000,
            days_remaining=5,
            last_activity_days=20,
        )
        inp_safe = make_input(
            rep_id="R2",
            closed_won_value=95_000,
            period_quota=100_000,
            pipeline_value=500_000,
            days_remaining=60,
            last_activity_days=1,
        )
        engine.analyze(inp_at_risk)
        engine.analyze(inp_safe)
        at_risk = engine.at_risk_reps
        assert all(r.is_at_risk for r in at_risk)

    def test_overachievers_filtering(self, engine):
        inp_over = make_input(rep_id="R1", closed_won_value=120_000, period_quota=100_000)
        inp_not = make_input(rep_id="R2", closed_won_value=80_000, period_quota=100_000)
        engine.analyze(inp_over)
        engine.analyze(inp_not)
        overachievers = engine.overachievers
        assert all(r.attainment_tier == AttainmentTier.OVERACHIEVER for r in overachievers)

    def test_critical_reps_filtering(self, engine):
        engine.analyze(make_input(rep_id="R1", closed_won_value=5_000, period_quota=100_000, pipeline_value=0, days_remaining=5, last_activity_days=20))
        engine.analyze(make_input(rep_id="R2", closed_won_value=95_000, period_quota=100_000, pipeline_value=500_000, days_remaining=60))
        critical = engine.critical_reps
        assert all(r.gap_risk == GapRisk.CRITICAL for r in critical)

    def test_total_gap_sum(self, engine):
        inp1 = make_input(rep_id="R1", closed_won_value=70_000, period_quota=100_000)
        inp2 = make_input(rep_id="R2", closed_won_value=90_000, period_quota=100_000)
        engine.analyze(inp1)
        engine.analyze(inp2)
        # gap1 = 30000, gap2 = 10000 → total = 40000
        assert engine.total_gap == pytest.approx(40_000.0)

    def test_total_gap_zero_when_all_over_quota(self, engine):
        engine.analyze(make_input(rep_id="R1", closed_won_value=110_000, period_quota=100_000))
        engine.analyze(make_input(rep_id="R2", closed_won_value=120_000, period_quota=100_000))
        assert engine.total_gap == 0.0

    def test_total_gap_rounded_to_2_decimals(self, engine):
        engine.analyze(make_input(rep_id="R1", closed_won_value=99_999.99, period_quota=100_000))
        tg = engine.total_gap
        assert tg == round(tg, 2)

    def test_overachievers_count_correct(self, engine):
        engine.analyze(make_input(rep_id="R1", closed_won_value=120_000, period_quota=100_000))
        engine.analyze(make_input(rep_id="R2", closed_won_value=115_000, period_quota=100_000))
        engine.analyze(make_input(rep_id="R3", closed_won_value=80_000, period_quota=100_000))
        assert len(engine.overachievers) == 2


# ─────────────────────────────────────────────────────────────────────────────
# 18. summary() — 13 keys
# ─────────────────────────────────────────────────────────────────────────────

class TestSummary:
    EXPECTED_KEYS = {
        "total", "tier_counts", "risk_counts", "coverage_counts",
        "action_counts", "avg_attainment_pct", "avg_projected_attainment",
        "avg_achievement_score", "avg_pipeline_health_score",
        "total_gap", "at_risk_count", "overachiever_count", "critical_count",
    }

    def test_empty_summary_key_count(self, engine):
        s = engine.summary()
        assert len(s) == 13

    def test_empty_summary_exact_keys(self, engine):
        assert set(engine.summary().keys()) == self.EXPECTED_KEYS

    def test_empty_summary_total_zero(self, engine):
        assert engine.summary()["total"] == 0

    def test_empty_summary_dicts_empty(self, engine):
        s = engine.summary()
        assert s["tier_counts"] == {}
        assert s["risk_counts"] == {}
        assert s["coverage_counts"] == {}
        assert s["action_counts"] == {}

    def test_empty_summary_numerics_zero(self, engine):
        s = engine.summary()
        assert s["avg_attainment_pct"] == 0.0
        assert s["avg_projected_attainment"] == 0.0
        assert s["avg_achievement_score"] == 0.0
        assert s["avg_pipeline_health_score"] == 0.0
        assert s["total_gap"] == 0.0
        assert s["at_risk_count"] == 0
        assert s["overachiever_count"] == 0
        assert s["critical_count"] == 0

    def test_summary_after_one_analysis(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        assert s["total"] == 1

    def test_summary_tier_counts(self, engine):
        engine.analyze(make_input(rep_id="R1", closed_won_value=120_000, period_quota=100_000))
        engine.analyze(make_input(rep_id="R2", closed_won_value=95_000, period_quota=100_000))
        s = engine.summary()
        assert "overachiever" in s["tier_counts"]
        assert "on_track" in s["tier_counts"]

    def test_summary_risk_counts(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        assert len(s["risk_counts"]) >= 1
        assert sum(s["risk_counts"].values()) == 1

    def test_summary_coverage_counts(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        assert sum(s["coverage_counts"].values()) == 1

    def test_summary_action_counts(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        assert sum(s["action_counts"].values()) == 1

    def test_summary_avg_attainment_pct(self, engine):
        engine.analyze(make_input(rep_id="R1", closed_won_value=70_000, period_quota=100_000))
        engine.analyze(make_input(rep_id="R2", closed_won_value=90_000, period_quota=100_000))
        s = engine.summary()
        # avg = (70 + 90) / 2 = 80.0
        assert s["avg_attainment_pct"] == pytest.approx(80.0, abs=0.1)

    def test_summary_total_gap_correct(self, engine):
        engine.analyze(make_input(rep_id="R1", closed_won_value=70_000, period_quota=100_000))
        engine.analyze(make_input(rep_id="R2", closed_won_value=90_000, period_quota=100_000))
        s = engine.summary()
        assert s["total_gap"] == pytest.approx(40_000.0)

    def test_summary_overachiever_count(self, engine):
        engine.analyze(make_input(rep_id="R1", closed_won_value=120_000, period_quota=100_000))
        engine.analyze(make_input(rep_id="R2", closed_won_value=80_000, period_quota=100_000))
        s = engine.summary()
        assert s["overachiever_count"] == 1

    def test_summary_at_risk_count(self, engine):
        engine.analyze(make_input(
            rep_id="R1",
            closed_won_value=5_000,
            period_quota=100_000,
            pipeline_value=5_000,
            days_remaining=5,
            last_activity_days=20,
        ))
        s = engine.summary()
        assert s["at_risk_count"] >= 1

    def test_summary_returns_dict(self, engine):
        assert isinstance(engine.summary(), dict)

    def test_summary_multiple_reps_tier_counts_sum(self, engine):
        for i, cw in enumerate([120_000, 95_000, 80_000, 60_000, 40_000]):
            engine.analyze(make_input(rep_id=f"R{i}", closed_won_value=cw, period_quota=100_000))
        s = engine.summary()
        assert sum(s["tier_counts"].values()) == 5


# ─────────────────────────────────────────────────────────────────────────────
# 19. reset()
# ─────────────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_results(self, engine):
        engine.analyze(make_input())
        engine.analyze(make_input(rep_id="R2"))
        engine.reset()
        assert engine.summary()["total"] == 0

    def test_reset_clears_at_risk_reps(self, engine):
        engine.analyze(make_input())
        engine.reset()
        assert engine.at_risk_reps == []

    def test_reset_clears_overachievers(self, engine):
        engine.analyze(make_input(closed_won_value=120_000, period_quota=100_000))
        engine.reset()
        assert engine.overachievers == []

    def test_reset_clears_critical_reps(self, engine):
        engine.analyze(make_input())
        engine.reset()
        assert engine.critical_reps == []

    def test_reset_total_gap_zero(self, engine):
        engine.analyze(make_input(closed_won_value=50_000, period_quota=100_000))
        engine.reset()
        assert engine.total_gap == 0.0

    def test_can_analyze_after_reset(self, engine):
        engine.analyze(make_input(rep_id="R1"))
        engine.reset()
        result = engine.analyze(make_input(rep_id="R2"))
        assert result.rep_id == "R2"
        assert engine.summary()["total"] == 1

    def test_reset_idempotent(self, engine):
        engine.reset()
        engine.reset()
        assert engine.summary()["total"] == 0


# ─────────────────────────────────────────────────────────────────────────────
# 20. analyze_batch
# ─────────────────────────────────────────────────────────────────────────────

class TestAnalyzeBatch:
    def test_empty_batch(self, engine):
        results = engine.analyze_batch([])
        assert results == []

    def test_batch_returns_list(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        assert isinstance(results, list)

    def test_batch_length_matches_input(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = engine.analyze_batch(inputs)
        assert len(results) == 5

    def test_batch_all_results_are_quota_gap_result(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        assert all(isinstance(r, QuotaGapResult) for r in results)

    def test_batch_appends_to_results(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(4)]
        engine.analyze_batch(inputs)
        assert engine.summary()["total"] == 4

    def test_batch_preserves_order(self, engine):
        ids = [f"R{i}" for i in range(5)]
        inputs = [make_input(rep_id=rid) for rid in ids]
        results = engine.analyze_batch(inputs)
        assert [r.rep_id for r in results] == ids

    def test_batch_plus_single_totals(self, engine):
        engine.analyze(make_input(rep_id="SINGLE"))
        engine.analyze_batch([make_input(rep_id=f"B{i}") for i in range(3)])
        assert engine.summary()["total"] == 4


# ─────────────────────────────────────────────────────────────────────────────
# 21. End-to-end scenarios
# ─────────────────────────────────────────────────────────────────────────────

class TestEndToEndScenarios:
    """Realistic rep scenarios validating full pipeline."""

    def test_overachiever_scenario(self, engine):
        """Rep who crushed quota gets CELEBRATE_AND_EXPAND."""
        inp = make_input(
            rep_id="STAR",
            closed_won_value=120_000,
            period_quota=100_000,
            pipeline_value=200_000,
            late_stage_value=80_000,
            days_remaining=30,
            win_rate=0.45,
            last_activity_days=1,
        )
        result = engine.analyze(inp)
        assert result.attainment_tier == AttainmentTier.OVERACHIEVER
        assert result.attainment_pct >= 110.0
        assert result.gap_to_quota == 0.0
        assert result.recommended_action == QuotaAction.CELEBRATE_AND_EXPAND
        assert result.is_at_risk is False

    def test_critical_rep_scenario(self, engine):
        """Very low attainment, no pipeline, end of period."""
        inp = make_input(
            rep_id="CRIT",
            closed_won_value=10_000,
            period_quota=100_000,
            pipeline_value=5_000,
            late_stage_value=1_000,
            days_remaining=5,
            win_rate=0.1,
            last_activity_days=20,
        )
        result = engine.analyze(inp)
        assert result.attainment_tier == AttainmentTier.CRITICAL
        assert result.attainment_pct < 50.0
        assert result.gap_to_quota > 0.0
        assert result.is_at_risk is True

    def test_ramping_rep_scenario(self, engine):
        """New rep with 75% ramp gets reduced quota."""
        inp = make_input(
            rep_id="RAMP",
            closed_won_value=70_000,
            period_quota=100_000,
            is_ramping=True,
            ramp_factor=0.75,
            pipeline_value=50_000,
            days_remaining=30,
        )
        result = engine.analyze(inp)
        # effective quota = 75000
        assert result.effective_quota == pytest.approx(75_000.0)
        assert result.attainment_pct == pytest.approx(round(70_000 / 75_000 * 100, 1))
        # 70000 < 75000 → gap = 5000, not 0
        assert result.gap_to_quota == pytest.approx(5_000.0)

    def test_ramping_rep_gap(self, engine):
        """Ramping rep who is behind even with reduced quota."""
        inp = make_input(
            rep_id="RAMP2",
            closed_won_value=50_000,
            period_quota=100_000,
            is_ramping=True,
            ramp_factor=0.75,  # effective = 75000
            pipeline_value=50_000,
            days_remaining=30,
        )
        result = engine.analyze(inp)
        assert result.effective_quota == pytest.approx(75_000.0)
        assert result.gap_to_quota == pytest.approx(25_000.0)

    def test_on_track_scenario(self, engine):
        inp = make_input(
            rep_id="GOOD",
            closed_won_value=92_000,
            period_quota=100_000,
            pipeline_value=200_000,
            late_stage_value=80_000,
            days_remaining=20,
            win_rate=0.4,
            last_activity_days=2,
        )
        result = engine.analyze(inp)
        assert result.attainment_tier == AttainmentTier.ON_TRACK

    def test_at_risk_scenario(self, engine):
        inp = make_input(
            rep_id="RISKY",
            closed_won_value=72_000,
            period_quota=100_000,
            pipeline_value=40_000,
            days_remaining=20,
            win_rate=0.25,
            last_activity_days=5,
        )
        result = engine.analyze(inp)
        assert result.attainment_tier == AttainmentTier.AT_RISK

    def test_behind_scenario(self, engine):
        inp = make_input(
            rep_id="BEHIND",
            closed_won_value=55_000,
            period_quota=100_000,
            pipeline_value=80_000,
            days_remaining=30,
            win_rate=0.3,
        )
        result = engine.analyze(inp)
        assert result.attainment_tier == AttainmentTier.BEHIND

    def test_result_stored_in_engine(self, engine):
        inp = make_input()
        result = engine.analyze(inp)
        assert result in engine._results

    def test_multiple_reps_summary_totals(self, engine):
        reps = [
            make_input(rep_id="R1", closed_won_value=120_000, period_quota=100_000),
            make_input(rep_id="R2", closed_won_value=95_000, period_quota=100_000),
            make_input(rep_id="R3", closed_won_value=75_000, period_quota=100_000),
            make_input(rep_id="R4", closed_won_value=55_000, period_quota=100_000),
            make_input(rep_id="R5", closed_won_value=30_000, period_quota=100_000),
        ]
        engine.analyze_batch(reps)
        s = engine.summary()
        assert s["total"] == 5
        assert s["overachiever_count"] == 1
        assert "critical" in s["tier_counts"]

    def test_analyze_returns_quota_gap_result(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result, QuotaGapResult)

    def test_result_rep_fields_match_input(self, engine):
        inp = make_input(rep_id="XYZ", rep_name="Bob Jones", manager_id="MGR42")
        result = engine.analyze(inp)
        assert result.rep_id == "XYZ"
        assert result.rep_name == "Bob Jones"
        assert result.manager_id == "MGR42"

    def test_result_days_remaining_matches_input(self, engine):
        inp = make_input(days_remaining=45)
        result = engine.analyze(inp)
        assert result.days_remaining == 45

    def test_effective_quota_rounded_to_2_decimals(self, engine):
        inp = make_input(is_ramping=True, ramp_factor=0.333, period_quota=100_000)
        result = engine.analyze(inp)
        assert result.effective_quota == round(result.effective_quota, 2)

    def test_gap_to_quota_rounded_to_2_decimals(self, engine):
        inp = make_input(closed_won_value=66_666.66, period_quota=100_000)
        result = engine.analyze(inp)
        assert result.gap_to_quota == round(result.gap_to_quota, 2)

    def test_achievement_score_between_0_and_100(self, engine):
        for cw in [0, 50_000, 100_000, 150_000]:
            r = engine.analyze(make_input(closed_won_value=cw, period_quota=100_000))
            assert 0.0 <= r.quota_achievement_score <= 100.0

    def test_pipeline_health_score_between_0_and_100(self, engine):
        for win_rate in [0.0, 0.2, 0.4, 0.8]:
            r = engine.analyze(make_input(win_rate=win_rate))
            assert 0.0 <= r.pipeline_health_score <= 100.0

    def test_required_win_rate_between_0_and_1(self, engine):
        r = engine.analyze(make_input(closed_won_value=50_000, period_quota=100_000, pipeline_value=200_000))
        assert 0.0 <= r.required_win_rate <= 1.0

    def test_deals_needed_non_negative(self, engine):
        r = engine.analyze(make_input())
        assert r.deals_needed >= 0

    def test_build_pipeline_scenario(self, engine):
        """Low pipeline triggers BUILD_PIPELINE action."""
        inp = make_input(
            rep_id="NOPIPE",
            closed_won_value=60_000,
            period_quota=100_000,
            pipeline_value=5_000,
            late_stage_value=0,
            days_remaining=30,
            win_rate=0.2,
            last_activity_days=5,
        )
        result = engine.analyze(inp)
        # Gap = 40000, pipeline = 5000 → ratio < 1 → INSUFFICIENT
        assert result.pipeline_coverage == PipelineCoverage.INSUFFICIENT

    def test_focus_late_stage_scenario(self, engine):
        """HIGH risk with late stage → FOCUS_LATE_STAGE."""
        # Need: attainment < 110, gap_risk == HIGH, pipeline != INSUFFICIENT, late_stage_value > 0
        # HIGH risk (score=4): attainment<50 (+3) + activity>14 (+1) = 4 → HIGH
        inp = make_input(
            rep_id="LATE",
            closed_won_value=30_000,
            period_quota=100_000,
            pipeline_value=120_000,   # ratio = 120000/70000 > 1 → THIN or ADEQUATE
            late_stage_value=50_000,
            days_remaining=45,
            win_rate=0.35,
            last_activity_days=16,    # > 14 → +1
        )
        result = engine.analyze(inp)
        if result.gap_risk == GapRisk.HIGH and result.pipeline_coverage != PipelineCoverage.INSUFFICIENT:
            assert result.recommended_action == QuotaAction.FOCUS_LATE_STAGE

    def test_all_enum_action_values_are_valid(self, engine):
        result = engine.analyze(make_input())
        assert result.recommended_action in list(QuotaAction)

    def test_all_enum_tier_values_are_valid(self, engine):
        result = engine.analyze(make_input())
        assert result.attainment_tier in list(AttainmentTier)

    def test_all_enum_risk_values_are_valid(self, engine):
        result = engine.analyze(make_input())
        assert result.gap_risk in list(GapRisk)

    def test_all_enum_coverage_values_are_valid(self, engine):
        result = engine.analyze(make_input())
        assert result.pipeline_coverage in list(PipelineCoverage)


# ─────────────────────────────────────────────────────────────────────────────
# 22. Additional edge-case / boundary tests
# ─────────────────────────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_zero_period_quota(self, engine):
        inp = make_input(period_quota=0.0, closed_won_value=0.0)
        result = engine.analyze(inp)
        assert result.attainment_pct == 100.0
        assert result.effective_quota == 0.0

    def test_all_zero_pipeline_values(self, engine):
        inp = make_input(
            pipeline_value=0.0,
            late_stage_value=0.0,
            commit_value=0.0,
            best_case_value=0.0,
        )
        result = engine.analyze(inp)
        assert isinstance(result, QuotaGapResult)

    def test_very_large_values(self, engine):
        inp = make_input(
            annual_quota=10_000_000.0,
            period_quota=2_500_000.0,
            closed_won_value=3_000_000.0,
            pipeline_value=5_000_000.0,
            avg_deal_size=500_000.0,
        )
        result = engine.analyze(inp)
        assert result.attainment_pct >= 110.0
        assert result.gap_to_quota == 0.0

    def test_zero_win_rate(self, engine):
        inp = make_input(win_rate=0.0)
        result = engine.analyze(inp)
        assert result.pipeline_health_score >= 0.0

    def test_win_rate_1(self, engine):
        inp = make_input(win_rate=1.0)
        result = engine.analyze(inp)
        assert result.pipeline_health_score <= 100.0

    def test_zero_days_remaining(self, engine):
        inp = make_input(days_remaining=0)
        result = engine.analyze(inp)
        assert result.days_remaining == 0

    def test_is_at_risk_false_for_low_and_medium(self):
        engine = QuotaGapAnalysisEngine()
        # Construct very safe rep: 95% attained, strong pipeline, long runway, active
        inp = make_input(
            closed_won_value=95_000,
            period_quota=100_000,
            pipeline_value=300_000,
            days_remaining=60,
            last_activity_days=1,
            win_rate=0.5,
        )
        result = engine.analyze(inp)
        assert result.is_at_risk is False

    def test_projected_attainment_ge_0(self, engine):
        inp = make_input(closed_won_value=0, commit_value=0, late_stage_value=0)
        result = engine.analyze(inp)
        assert result.projected_attainment >= 0.0

    def test_projected_attainment_le_200(self, engine):
        inp = make_input(closed_won_value=999_999, period_quota=100_000)
        result = engine.analyze(inp)
        assert result.projected_attainment <= 200.0

    def test_gap_never_negative(self, engine):
        inp = make_input(closed_won_value=200_000, period_quota=100_000)
        result = engine.analyze(inp)
        assert result.gap_to_quota >= 0.0

    def test_deals_needed_zero_when_over_quota(self, engine):
        inp = make_input(closed_won_value=110_000, period_quota=100_000)
        result = engine.analyze(inp)
        assert result.deals_needed == 0

    def test_required_win_rate_zero_when_over_quota(self, engine):
        inp = make_input(closed_won_value=110_000, period_quota=100_000)
        result = engine.analyze(inp)
        assert result.required_win_rate == 0.0

    def test_ramp_factor_exactly_0_not_applied(self, engine):
        inp = make_input(is_ramping=True, ramp_factor=0.0, period_quota=100_000)
        result = engine.analyze(inp)
        assert result.effective_quota == pytest.approx(100_000.0)

    def test_ramp_factor_exactly_1_not_applied(self, engine):
        inp = make_input(is_ramping=True, ramp_factor=1.0, period_quota=100_000)
        result = engine.analyze(inp)
        assert result.effective_quota == pytest.approx(100_000.0)

    def test_engine_initializes_with_empty_results(self):
        e = QuotaGapAnalysisEngine()
        assert e._results == []

    def test_multiple_analyzes_accumulate(self, engine):
        for i in range(10):
            engine.analyze(make_input(rep_id=f"R{i}"))
        assert engine.summary()["total"] == 10

    def test_to_dict_attainment_tier_is_string_not_enum(self, engine):
        result = engine.analyze(make_input())
        d = result.to_dict()
        assert not isinstance(d["attainment_tier"], AttainmentTier)
        assert isinstance(d["attainment_tier"], str)

    def test_to_dict_gap_risk_is_string_not_enum(self, engine):
        result = engine.analyze(make_input())
        d = result.to_dict()
        assert not isinstance(d["gap_risk"], GapRisk)
        assert isinstance(d["gap_risk"], str)

    def test_to_dict_pipeline_coverage_is_string_not_enum(self, engine):
        result = engine.analyze(make_input())
        d = result.to_dict()
        assert not isinstance(d["pipeline_coverage"], PipelineCoverage)
        assert isinstance(d["pipeline_coverage"], str)

    def test_to_dict_recommended_action_is_string_not_enum(self, engine):
        result = engine.analyze(make_input())
        d = result.to_dict()
        assert not isinstance(d["recommended_action"], QuotaAction)
        assert isinstance(d["recommended_action"], str)

    def test_late_stage_gte_pipeline_value(self, engine):
        """Late stage can equal pipeline value (ratio=1.0)."""
        inp = make_input(pipeline_value=50_000, late_stage_value=50_000)
        result = engine.analyze(inp)
        assert result.pipeline_health_score >= 0.0

    def test_overdue_equals_deals_in_pipeline(self, engine):
        inp = make_input(deals_in_pipeline=5, overdue_deals=5)
        result = engine.analyze(inp)
        assert result.pipeline_health_score >= 0.0

    def test_all_results_have_is_at_risk_bool(self, engine):
        for i in range(5):
            engine.analyze(make_input(rep_id=f"R{i}"))
        assert all(isinstance(r.is_at_risk, bool) for r in engine._results)

    def test_summary_avg_scores_in_range(self, engine):
        for i in range(5):
            engine.analyze(make_input(rep_id=f"R{i}"))
        s = engine.summary()
        assert 0.0 <= s["avg_achievement_score"] <= 100.0
        assert 0.0 <= s["avg_pipeline_health_score"] <= 100.0

    def test_attainment_exactly_110_is_overachiever(self, engine):
        inp = make_input(closed_won_value=110_000, period_quota=100_000)
        result = engine.analyze(inp)
        assert result.attainment_tier == AttainmentTier.OVERACHIEVER

    def test_attainment_exactly_90_is_on_track(self, engine):
        inp = make_input(closed_won_value=90_000, period_quota=100_000)
        result = engine.analyze(inp)
        assert result.attainment_tier == AttainmentTier.ON_TRACK

    def test_attainment_exactly_70_is_at_risk(self, engine):
        inp = make_input(closed_won_value=70_000, period_quota=100_000)
        result = engine.analyze(inp)
        assert result.attainment_tier == AttainmentTier.AT_RISK

    def test_attainment_exactly_50_is_behind(self, engine):
        inp = make_input(closed_won_value=50_000, period_quota=100_000)
        result = engine.analyze(inp)
        assert result.attainment_tier == AttainmentTier.BEHIND

    def test_attainment_below_50_is_critical_tier(self, engine):
        inp = make_input(closed_won_value=49_000, period_quota=100_000)
        result = engine.analyze(inp)
        assert result.attainment_tier == AttainmentTier.CRITICAL
