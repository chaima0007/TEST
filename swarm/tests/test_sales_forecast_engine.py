"""
Comprehensive pytest tests for SalesForecastEngine.
Import pattern: from swarm.intelligence.sales_forecast_engine import ...
Run: python -m pytest swarm/tests/test_sales_forecast_engine.py -v
"""
from __future__ import annotations

import pytest
from swarm.intelligence.sales_forecast_engine import (
    CallReliability,
    ForecastAccuracy,
    ForecastAction,
    ForecastBand,
    SalesForecastEngine,
    SalesForecastInput,
    SalesForecastResult,
)


# ──────────────────────────────────────────────────────────────────────────────
# Fixtures / helpers
# ──────────────────────────────────────────────────────────────────────────────

def make_input(
    rep_id="REP-001",
    rep_name="Alice Smith",
    manager_id="MGR-001",
    region="West",
    quota=100_000.0,
    submitted_commit=80_000.0,
    submitted_best_case=100_000.0,
    pipeline_value=200_000.0,
    closed_won_qtd=40_000.0,
    late_stage_pipeline=60_000.0,
    early_stage_pipeline=20_000.0,
    days_remaining=30,
    period_days=90,
    historical_accuracy_pct=80.0,
    historical_beat_pct=10.0,
    last_period_attainment=90.0,
    slipped_deals_count=0,
    new_pipeline_added_qtd=10_000.0,
    calls_made=5,
    calls_hit=4,
    nrr_contribution=5_000.0,
) -> SalesForecastInput:
    return SalesForecastInput(
        rep_id=rep_id,
        rep_name=rep_name,
        manager_id=manager_id,
        region=region,
        quota=quota,
        submitted_commit=submitted_commit,
        submitted_best_case=submitted_best_case,
        pipeline_value=pipeline_value,
        closed_won_qtd=closed_won_qtd,
        late_stage_pipeline=late_stage_pipeline,
        early_stage_pipeline=early_stage_pipeline,
        days_remaining=days_remaining,
        period_days=period_days,
        historical_accuracy_pct=historical_accuracy_pct,
        historical_beat_pct=historical_beat_pct,
        last_period_attainment=last_period_attainment,
        slipped_deals_count=slipped_deals_count,
        new_pipeline_added_qtd=new_pipeline_added_qtd,
        calls_made=calls_made,
        calls_hit=calls_hit,
        nrr_contribution=nrr_contribution,
    )


@pytest.fixture
def engine() -> SalesForecastEngine:
    return SalesForecastEngine()


@pytest.fixture
def standard_input() -> SalesForecastInput:
    return make_input()


# ──────────────────────────────────────────────────────────────────────────────
# Section 1 – Enum membership and values
# ──────────────────────────────────────────────────────────────────────────────

class TestForecastBandEnum:
    def test_best_case_value(self):
        assert ForecastBand.BEST_CASE.value == "best_case"

    def test_upside_value(self):
        assert ForecastBand.UPSIDE.value == "upside"

    def test_commit_value(self):
        assert ForecastBand.COMMIT.value == "commit"

    def test_likely_value(self):
        assert ForecastBand.LIKELY.value == "likely"

    def test_all_four_members(self):
        assert len(ForecastBand) == 4

    def test_is_str_enum(self):
        assert isinstance(ForecastBand.COMMIT, str)


class TestForecastAccuracyEnum:
    def test_excellent_value(self):
        assert ForecastAccuracy.EXCELLENT.value == "excellent"

    def test_good_value(self):
        assert ForecastAccuracy.GOOD.value == "good"

    def test_fair_value(self):
        assert ForecastAccuracy.FAIR.value == "fair"

    def test_poor_value(self):
        assert ForecastAccuracy.POOR.value == "poor"

    def test_all_four_members(self):
        assert len(ForecastAccuracy) == 4

    def test_is_str_enum(self):
        assert isinstance(ForecastAccuracy.GOOD, str)


class TestCallReliabilityEnum:
    def test_high_value(self):
        assert CallReliability.HIGH.value == "high"

    def test_medium_value(self):
        assert CallReliability.MEDIUM.value == "medium"

    def test_low_value(self):
        assert CallReliability.LOW.value == "low"

    def test_unreliable_value(self):
        assert CallReliability.UNRELIABLE.value == "unreliable"

    def test_all_four_members(self):
        assert len(CallReliability) == 4

    def test_is_str_enum(self):
        assert isinstance(CallReliability.HIGH, str)


class TestForecastActionEnum:
    def test_commit_as_is_value(self):
        assert ForecastAction.COMMIT_AS_IS.value == "commit_as_is"

    def test_adjust_up_value(self):
        assert ForecastAction.ADJUST_UP.value == "adjust_up"

    def test_adjust_down_value(self):
        assert ForecastAction.ADJUST_DOWN.value == "adjust_down"

    def test_investigate_value(self):
        assert ForecastAction.INVESTIGATE.value == "investigate"

    def test_escalate_value(self):
        assert ForecastAction.ESCALATE.value == "escalate"

    def test_all_five_members(self):
        assert len(ForecastAction) == 5

    def test_is_str_enum(self):
        assert isinstance(ForecastAction.ESCALATE, str)


# ──────────────────────────────────────────────────────────────────────────────
# Section 2 – SalesForecastInput dataclass
# ──────────────────────────────────────────────────────────────────────────────

class TestSalesForecastInput:
    def test_all_21_fields_accessible(self, standard_input):
        inp = standard_input
        assert inp.rep_id == "REP-001"
        assert inp.rep_name == "Alice Smith"
        assert inp.manager_id == "MGR-001"
        assert inp.region == "West"
        assert inp.quota == 100_000.0
        assert inp.submitted_commit == 80_000.0
        assert inp.submitted_best_case == 100_000.0
        assert inp.pipeline_value == 200_000.0
        assert inp.closed_won_qtd == 40_000.0
        assert inp.late_stage_pipeline == 60_000.0
        assert inp.early_stage_pipeline == 20_000.0
        assert inp.days_remaining == 30
        assert inp.period_days == 90
        assert inp.historical_accuracy_pct == 80.0
        assert inp.historical_beat_pct == 10.0
        assert inp.last_period_attainment == 90.0
        assert inp.slipped_deals_count == 0
        assert inp.new_pipeline_added_qtd == 10_000.0
        assert inp.calls_made == 5
        assert inp.calls_hit == 4
        assert inp.nrr_contribution == 5_000.0

    def test_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(SalesForecastInput)

    def test_field_count(self):
        import dataclasses
        fields = dataclasses.fields(SalesForecastInput)
        assert len(fields) == 21

    def test_mutable(self, standard_input):
        standard_input.quota = 999.0
        assert standard_input.quota == 999.0


# ──────────────────────────────────────────────────────────────────────────────
# Section 3 – SalesForecastResult.to_dict() invariants
# ──────────────────────────────────────────────────────────────────────────────

class TestSalesForecastResultToDict:
    def test_returns_exactly_15_keys(self, engine, standard_input):
        result = engine.analyze(standard_input)
        d = result.to_dict()
        assert len(d) == 15

    def test_exact_15_key_names(self, engine, standard_input):
        result = engine.analyze(standard_input)
        d = result.to_dict()
        expected_keys = {
            "rep_id", "rep_name", "manager_id", "forecast_band",
            "forecast_accuracy", "call_reliability", "forecast_action",
            "adjusted_forecast", "coverage_ratio", "sandbagging_score",
            "pipeline_health", "commit_vs_quota_pct", "upside_potential",
            "is_at_risk", "is_sandbagging",
        }
        assert set(d.keys()) == expected_keys

    def test_enum_fields_serialized_as_strings(self, engine, standard_input):
        result = engine.analyze(standard_input)
        d = result.to_dict()
        assert isinstance(d["forecast_band"], str)
        assert isinstance(d["forecast_accuracy"], str)
        assert isinstance(d["call_reliability"], str)
        assert isinstance(d["forecast_action"], str)

    def test_bool_fields_are_bool(self, engine, standard_input):
        result = engine.analyze(standard_input)
        d = result.to_dict()
        assert isinstance(d["is_at_risk"], bool)
        assert isinstance(d["is_sandbagging"], bool)

    def test_numeric_fields_are_float(self, engine, standard_input):
        result = engine.analyze(standard_input)
        d = result.to_dict()
        for key in ("adjusted_forecast", "coverage_ratio", "sandbagging_score",
                    "pipeline_health", "commit_vs_quota_pct", "upside_potential"):
            assert isinstance(d[key], (int, float)), f"{key} should be numeric"

    def test_rep_id_preserved(self, engine):
        inp = make_input(rep_id="MY-REP-42")
        result = engine.analyze(inp)
        assert result.to_dict()["rep_id"] == "MY-REP-42"

    def test_rep_name_preserved(self, engine):
        inp = make_input(rep_name="Bob Jones")
        result = engine.analyze(inp)
        assert result.to_dict()["rep_name"] == "Bob Jones"

    def test_manager_id_preserved(self, engine):
        inp = make_input(manager_id="MGR-XYZ")
        result = engine.analyze(inp)
        assert result.to_dict()["manager_id"] == "MGR-XYZ"


# ──────────────────────────────────────────────────────────────────────────────
# Section 4 – _coverage_ratio
# ──────────────────────────────────────────────────────────────────────────────

class TestCoverageRatio:
    def test_normal_case(self, engine):
        inp = make_input(pipeline_value=200_000.0, quota=100_000.0)
        result = engine.analyze(inp)
        assert result.coverage_ratio == 2.0

    def test_quota_zero_returns_zero(self, engine):
        inp = make_input(quota=0.0, submitted_commit=0.0)
        result = engine.analyze(inp)
        assert result.coverage_ratio == 0.0

    def test_quota_negative_returns_zero(self, engine):
        inp = make_input(quota=-1.0, submitted_commit=0.0)
        result = engine.analyze(inp)
        assert result.coverage_ratio == 0.0

    def test_rounded_to_2dp(self, engine):
        inp = make_input(pipeline_value=100_000.0, quota=300_000.0)
        result = engine.analyze(inp)
        assert result.coverage_ratio == round(100_000 / 300_000, 2)

    def test_pipeline_zero(self, engine):
        inp = make_input(pipeline_value=0.0, quota=100_000.0)
        result = engine.analyze(inp)
        assert result.coverage_ratio == 0.0

    def test_pipeline_equals_quota(self, engine):
        inp = make_input(pipeline_value=100_000.0, quota=100_000.0)
        result = engine.analyze(inp)
        assert result.coverage_ratio == 1.0

    def test_high_pipeline(self, engine):
        inp = make_input(pipeline_value=500_000.0, quota=100_000.0)
        result = engine.analyze(inp)
        assert result.coverage_ratio == 5.0

    def test_partial_coverage(self, engine):
        inp = make_input(pipeline_value=75_000.0, quota=100_000.0)
        result = engine.analyze(inp)
        assert result.coverage_ratio == 0.75


# ──────────────────────────────────────────────────────────────────────────────
# Section 5 – _sandbagging_score
# ──────────────────────────────────────────────────────────────────────────────

class TestSandbaggingScore:
    def test_zero_score_when_commit_exceeds_weighted(self, engine):
        # weighted = 0 + 0 + 0 = 0; commit = 100k → gap = 0 → score = historical_beat*0.4
        inp = make_input(
            closed_won_qtd=0.0, late_stage_pipeline=0.0, early_stage_pipeline=0.0,
            submitted_commit=100_000.0, historical_beat_pct=0.0,
        )
        result = engine.analyze(inp)
        assert result.sandbagging_score == 0.0

    def test_positive_gap_increases_score(self, engine):
        # weighted = 50k + 65k*0.65 + 0 = 50k + 42250 = 92250
        # gap = max(0, 92250 - 80000) = 12250; gap_ratio=(12250/80000)*100=15.3125
        # score=15.3125*0.6 + 0*0.4=9.1875 → 9.2
        inp = make_input(
            closed_won_qtd=50_000.0, late_stage_pipeline=65_000.0,
            early_stage_pipeline=0.0, submitted_commit=80_000.0,
            historical_beat_pct=0.0,
        )
        result = engine.analyze(inp)
        assert result.sandbagging_score > 0.0

    def test_clamped_at_100(self, engine):
        inp = make_input(
            closed_won_qtd=1_000_000.0, late_stage_pipeline=1_000_000.0,
            early_stage_pipeline=1_000_000.0, submitted_commit=1.0,
            historical_beat_pct=100.0,
        )
        result = engine.analyze(inp)
        assert result.sandbagging_score == 100.0

    def test_clamped_at_zero(self, engine):
        inp = make_input(
            closed_won_qtd=0.0, late_stage_pipeline=0.0, early_stage_pipeline=0.0,
            submitted_commit=100_000.0, historical_beat_pct=0.0,
        )
        result = engine.analyze(inp)
        assert result.sandbagging_score == 0.0

    def test_historical_beat_contributes(self, engine):
        # With same pipeline and commit, higher historical_beat_pct should raise score
        inp_low = make_input(
            closed_won_qtd=0.0, late_stage_pipeline=0.0, early_stage_pipeline=0.0,
            submitted_commit=100_000.0, historical_beat_pct=0.0,
        )
        inp_high = make_input(
            closed_won_qtd=0.0, late_stage_pipeline=0.0, early_stage_pipeline=0.0,
            submitted_commit=100_000.0, historical_beat_pct=50.0,
        )
        r_low = engine.analyze(inp_low)
        r_high = engine.analyze(inp_high)
        assert r_high.sandbagging_score > r_low.sandbagging_score

    def test_late_stage_weight_0_65(self, engine):
        # Only late_stage_pipeline; commit = 1 so max(1,1)=1
        # weighted = 0 + 100*0.65 + 0 = 65
        # gap = max(0, 65 - 1) = 64; gap_ratio = 64/1 * 100 = 6400
        # score = 6400*0.6 + 0*0.4 = 3840 clamped to 100
        inp = make_input(
            closed_won_qtd=0.0, late_stage_pipeline=100.0,
            early_stage_pipeline=0.0, submitted_commit=1.0, historical_beat_pct=0.0,
        )
        result = engine.analyze(inp)
        assert result.sandbagging_score == 100.0

    def test_early_stage_weight_0_25(self, engine):
        inp = make_input(
            closed_won_qtd=0.0, late_stage_pipeline=0.0,
            early_stage_pipeline=400.0, submitted_commit=1.0, historical_beat_pct=0.0,
        )
        result = engine.analyze(inp)
        # weighted=100; gap=99; gap_ratio=9900; score=5940 → clamped 100
        assert result.sandbagging_score == 100.0

    def test_rounded_to_1dp(self, engine):
        inp = make_input(
            closed_won_qtd=10_000.0, late_stage_pipeline=20_000.0,
            early_stage_pipeline=5_000.0, submitted_commit=50_000.0,
            historical_beat_pct=15.0,
        )
        result = engine.analyze(inp)
        # Verify it's a float with at most 1 decimal place
        assert result.sandbagging_score == round(result.sandbagging_score, 1)

    def test_min_commit_denominator_is_1(self, engine):
        # submitted_commit=0 → max(1, 0)=1
        inp = make_input(
            closed_won_qtd=10_000.0, late_stage_pipeline=0.0,
            early_stage_pipeline=0.0, submitted_commit=0.0, historical_beat_pct=0.0,
        )
        result = engine.analyze(inp)
        # gap=10000; gap_ratio=10000/1*100=1000000; score=600000 clamped 100
        assert result.sandbagging_score == 100.0


# ──────────────────────────────────────────────────────────────────────────────
# Section 6 – _pipeline_health
# ──────────────────────────────────────────────────────────────────────────────

class TestPipelineHealth:
    def test_clamped_at_100(self, engine):
        # coverage=100 → min(40,1000)=40; late_cov=10 → min(30,200)=30; calls=25; slip=0
        # 40+30+25=95 — need more. Use slippage=0 and boost by capping at 100
        # Actually need an input that sums > 100: add slippage=negative? No.
        # Max possible = 40+30+25 = 95; to reach 100 is impossible via normal math.
        # The test should verify the cap only triggers when raw > 100, which can't happen.
        # Instead test that health is ≤ 100 and verify perfect conditions give max score.
        inp = make_input(
            pipeline_value=1_000_000.0, quota=100_000.0,
            late_stage_pipeline=1_000_000.0, submitted_commit=100_000.0,
            calls_made=10, calls_hit=10, slipped_deals_count=0,
        )
        result = engine.analyze(inp)
        # coverage=10→40, late_cov=10→30, calls=25; total=95.0
        assert result.pipeline_health == 95.0
        assert result.pipeline_health <= 100.0

    def test_clamped_at_zero(self, engine):
        inp = make_input(
            pipeline_value=0.0, quota=1_000_000.0,
            late_stage_pipeline=0.0, submitted_commit=100_000.0,
            calls_made=10, calls_hit=0, slipped_deals_count=20,
        )
        result = engine.analyze(inp)
        assert result.pipeline_health == 0.0

    def test_no_calls_gives_neutral_12_5(self, engine):
        # coverage=1 → coverage*10=10 (max 40); late_cov=0.5 → 0.5*20=10 (max 30)
        # calls_made=0 → +12.5; slipped=0; total=10+10+12.5=32.5
        inp = make_input(
            pipeline_value=100_000.0, quota=100_000.0,
            late_stage_pipeline=50_000.0, submitted_commit=100_000.0,
            calls_made=0, calls_hit=0, slipped_deals_count=0,
        )
        result = engine.analyze(inp)
        assert result.pipeline_health == 32.5

    def test_slippage_penalty(self, engine):
        # Same as above but 1 slipped deal → 32.5 - 8 = 24.5
        inp = make_input(
            pipeline_value=100_000.0, quota=100_000.0,
            late_stage_pipeline=50_000.0, submitted_commit=100_000.0,
            calls_made=0, calls_hit=0, slipped_deals_count=1,
        )
        result = engine.analyze(inp)
        assert result.pipeline_health == 24.5

    def test_coverage_capped_at_40(self, engine):
        # coverage=10 → coverage*10=100 capped at 40
        inp = make_input(
            pipeline_value=1_000_000.0, quota=100_000.0,
            late_stage_pipeline=0.0, submitted_commit=100_000.0,
            calls_made=0, calls_hit=0, slipped_deals_count=0,
        )
        result = engine.analyze(inp)
        # 40 (coverage) + 0 (late) + 12.5 (no calls) = 52.5
        assert result.pipeline_health == 52.5

    def test_late_stage_capped_at_30(self, engine):
        inp = make_input(
            pipeline_value=0.0, quota=100_000.0,
            late_stage_pipeline=1_000_000.0, submitted_commit=100_000.0,
            calls_made=0, calls_hit=0, slipped_deals_count=0,
        )
        result = engine.analyze(inp)
        # coverage=0 → 0; late_cov=10 → 10*20=200 capped 30; no calls=12.5; total=42.5
        assert result.pipeline_health == 42.5

    def test_full_call_accuracy_gives_25(self, engine):
        # coverage=0, late=0, calls 5/5, no slip
        inp = make_input(
            pipeline_value=0.0, quota=100_000.0,
            late_stage_pipeline=0.0, submitted_commit=100_000.0,
            calls_made=5, calls_hit=5, slipped_deals_count=0,
        )
        result = engine.analyze(inp)
        # 0 + 0 + 25 = 25.0
        assert result.pipeline_health == 25.0

    def test_zero_call_accuracy_gives_zero_call_contribution(self, engine):
        inp = make_input(
            pipeline_value=0.0, quota=100_000.0,
            late_stage_pipeline=0.0, submitted_commit=100_000.0,
            calls_made=5, calls_hit=0, slipped_deals_count=0,
        )
        result = engine.analyze(inp)
        # 0 + 0 + 0 = 0.0
        assert result.pipeline_health == 0.0

    def test_rounded_to_1dp(self, engine, standard_input):
        result = engine.analyze(standard_input)
        assert result.pipeline_health == round(result.pipeline_health, 1)

    def test_zero_commit_skips_late_stage_ratio(self, engine):
        # submitted_commit=0 → late stage block skipped entirely
        inp = make_input(
            pipeline_value=100_000.0, quota=100_000.0,
            late_stage_pipeline=50_000.0, submitted_commit=0.0,
            calls_made=0, calls_hit=0, slipped_deals_count=0,
        )
        result = engine.analyze(inp)
        # coverage=1 → 10; no commit block; no calls=12.5; total=22.5
        assert result.pipeline_health == 22.5

    def test_multiple_slipped_deals_penalty(self, engine):
        inp = make_input(
            pipeline_value=1_000_000.0, quota=100_000.0,
            late_stage_pipeline=1_000_000.0, submitted_commit=100_000.0,
            calls_made=10, calls_hit=10, slipped_deals_count=5,
        )
        result = engine.analyze(inp)
        # 40+30+25 - 5*8 = 95-40=55 -> 55.0
        assert result.pipeline_health == 55.0


# ──────────────────────────────────────────────────────────────────────────────
# Section 7 – _adjusted_forecast
# ──────────────────────────────────────────────────────────────────────────────

class TestAdjustedForecast:
    def _compute_expected(self, inp: SalesForecastInput) -> float:
        base = (
            inp.closed_won_qtd
            + inp.late_stage_pipeline * 0.70
            + inp.early_stage_pipeline * 0.25
            + inp.nrr_contribution
        )
        acc_factor = max(0.5, inp.historical_accuracy_pct / 100.0)
        estimate = base * acc_factor
        floor = inp.submitted_commit * 0.80
        ceiling = inp.submitted_best_case
        return round(max(floor, min(ceiling, estimate)), 2)

    def test_standard_calculation(self, engine, standard_input):
        result = engine.analyze(standard_input)
        expected = self._compute_expected(standard_input)
        assert result.adjusted_forecast == expected

    def test_floor_applied(self, engine):
        # Make estimate tiny so floor (80% of commit) kicks in
        inp = make_input(
            closed_won_qtd=0.0, late_stage_pipeline=0.0, early_stage_pipeline=0.0,
            nrr_contribution=0.0, submitted_commit=100_000.0,
            submitted_best_case=200_000.0, historical_accuracy_pct=50.0,
        )
        # base=0; estimate=0; floor=80000 → adjusted=80000
        result = engine.analyze(inp)
        assert result.adjusted_forecast == 80_000.0

    def test_ceiling_applied(self, engine):
        # Make estimate huge so ceiling (best_case) kicks in
        inp = make_input(
            closed_won_qtd=1_000_000.0, late_stage_pipeline=1_000_000.0,
            early_stage_pipeline=1_000_000.0, nrr_contribution=1_000_000.0,
            submitted_commit=10_000.0, submitted_best_case=500_000.0,
            historical_accuracy_pct=100.0,
        )
        result = engine.analyze(inp)
        assert result.adjusted_forecast == 500_000.0

    def test_accuracy_factor_minimum_0_5(self, engine):
        # historical_accuracy_pct=0 → factor=0.5 (not 0)
        inp = make_input(
            closed_won_qtd=100_000.0, late_stage_pipeline=0.0, early_stage_pipeline=0.0,
            nrr_contribution=0.0, submitted_commit=1.0, submitted_best_case=500_000.0,
            historical_accuracy_pct=0.0,
        )
        # base=100000; factor=0.5; estimate=50000; floor=0.8; ceiling=500000
        result = engine.analyze(inp)
        assert result.adjusted_forecast == 50_000.0

    def test_rounded_to_2dp(self, engine):
        inp = make_input(
            closed_won_qtd=33_333.33, late_stage_pipeline=0.0, early_stage_pipeline=0.0,
            nrr_contribution=0.0, submitted_commit=1.0, submitted_best_case=500_000.0,
            historical_accuracy_pct=100.0,
        )
        result = engine.analyze(inp)
        assert result.adjusted_forecast == round(result.adjusted_forecast, 2)

    def test_nrr_included_in_base(self, engine):
        inp_no_nrr = make_input(
            closed_won_qtd=50_000.0, late_stage_pipeline=0.0, early_stage_pipeline=0.0,
            nrr_contribution=0.0, submitted_commit=1.0, submitted_best_case=500_000.0,
            historical_accuracy_pct=100.0,
        )
        inp_with_nrr = make_input(
            closed_won_qtd=50_000.0, late_stage_pipeline=0.0, early_stage_pipeline=0.0,
            nrr_contribution=10_000.0, submitted_commit=1.0, submitted_best_case=500_000.0,
            historical_accuracy_pct=100.0,
        )
        r_no = engine.analyze(inp_no_nrr)
        r_with = engine.analyze(inp_with_nrr)
        assert r_with.adjusted_forecast > r_no.adjusted_forecast

    def test_late_stage_weight_0_70(self, engine):
        inp = make_input(
            closed_won_qtd=0.0, late_stage_pipeline=100_000.0,
            early_stage_pipeline=0.0, nrr_contribution=0.0,
            submitted_commit=1.0, submitted_best_case=500_000.0,
            historical_accuracy_pct=100.0,
        )
        # base=70000; estimate=70000
        result = engine.analyze(inp)
        assert result.adjusted_forecast == 70_000.0

    def test_early_stage_weight_0_25(self, engine):
        inp = make_input(
            closed_won_qtd=0.0, late_stage_pipeline=0.0,
            early_stage_pipeline=100_000.0, nrr_contribution=0.0,
            submitted_commit=1.0, submitted_best_case=500_000.0,
            historical_accuracy_pct=100.0,
        )
        result = engine.analyze(inp)
        assert result.adjusted_forecast == 25_000.0


# ──────────────────────────────────────────────────────────────────────────────
# Section 8 – _commit_vs_quota_pct
# ──────────────────────────────────────────────────────────────────────────────

class TestCommitVsQuotaPct:
    def test_standard_case(self, engine):
        inp = make_input(submitted_commit=80_000.0, quota=100_000.0)
        result = engine.analyze(inp)
        assert result.commit_vs_quota_pct == 80.0

    def test_zero_quota_returns_zero(self, engine):
        inp = make_input(quota=0.0, submitted_commit=0.0)
        result = engine.analyze(inp)
        assert result.commit_vs_quota_pct == 0.0

    def test_negative_quota_returns_zero(self, engine):
        inp = make_input(quota=-100.0, submitted_commit=0.0)
        result = engine.analyze(inp)
        assert result.commit_vs_quota_pct == 0.0

    def test_100_percent_commit(self, engine):
        inp = make_input(submitted_commit=100_000.0, quota=100_000.0)
        result = engine.analyze(inp)
        assert result.commit_vs_quota_pct == 100.0

    def test_over_100_percent(self, engine):
        inp = make_input(submitted_commit=120_000.0, quota=100_000.0)
        result = engine.analyze(inp)
        assert result.commit_vs_quota_pct == 120.0

    def test_rounded_to_1dp(self, engine):
        inp = make_input(submitted_commit=100_000.0, quota=300_000.0)
        result = engine.analyze(inp)
        expected = round((100_000 / 300_000) * 100, 1)
        assert result.commit_vs_quota_pct == expected

    def test_zero_commit(self, engine):
        inp = make_input(submitted_commit=0.0, quota=100_000.0)
        result = engine.analyze(inp)
        assert result.commit_vs_quota_pct == 0.0


# ──────────────────────────────────────────────────────────────────────────────
# Section 9 – _upside_potential
# ──────────────────────────────────────────────────────────────────────────────

class TestUpsidePotential:
    def test_standard_case(self, engine):
        inp = make_input(submitted_best_case=100_000.0, submitted_commit=80_000.0)
        result = engine.analyze(inp)
        assert result.upside_potential == 20_000.0

    def test_zero_when_best_equals_commit(self, engine):
        inp = make_input(submitted_best_case=80_000.0, submitted_commit=80_000.0)
        result = engine.analyze(inp)
        assert result.upside_potential == 0.0

    def test_zero_when_best_below_commit(self, engine):
        inp = make_input(submitted_best_case=70_000.0, submitted_commit=80_000.0)
        result = engine.analyze(inp)
        assert result.upside_potential == 0.0

    def test_large_upside(self, engine):
        inp = make_input(submitted_best_case=500_000.0, submitted_commit=100_000.0)
        result = engine.analyze(inp)
        assert result.upside_potential == 400_000.0

    def test_rounded_to_2dp(self, engine):
        inp = make_input(submitted_best_case=100_001.005, submitted_commit=80_000.0)
        result = engine.analyze(inp)
        assert result.upside_potential == round(result.upside_potential, 2)


# ──────────────────────────────────────────────────────────────────────────────
# Section 10 – _forecast_accuracy
# ──────────────────────────────────────────────────────────────────────────────

class TestForecastAccuracy:
    def test_85_is_excellent(self, engine):
        inp = make_input(historical_accuracy_pct=85.0)
        assert engine.analyze(inp).forecast_accuracy == ForecastAccuracy.EXCELLENT

    def test_100_is_excellent(self, engine):
        inp = make_input(historical_accuracy_pct=100.0)
        assert engine.analyze(inp).forecast_accuracy == ForecastAccuracy.EXCELLENT

    def test_84_9_is_good(self, engine):
        inp = make_input(historical_accuracy_pct=84.9)
        assert engine.analyze(inp).forecast_accuracy == ForecastAccuracy.GOOD

    def test_70_is_good(self, engine):
        inp = make_input(historical_accuracy_pct=70.0)
        assert engine.analyze(inp).forecast_accuracy == ForecastAccuracy.GOOD

    def test_69_9_is_fair(self, engine):
        inp = make_input(historical_accuracy_pct=69.9)
        assert engine.analyze(inp).forecast_accuracy == ForecastAccuracy.FAIR

    def test_50_is_fair(self, engine):
        inp = make_input(historical_accuracy_pct=50.0)
        assert engine.analyze(inp).forecast_accuracy == ForecastAccuracy.FAIR

    def test_49_9_is_poor(self, engine):
        inp = make_input(historical_accuracy_pct=49.9)
        assert engine.analyze(inp).forecast_accuracy == ForecastAccuracy.POOR

    def test_0_is_poor(self, engine):
        inp = make_input(historical_accuracy_pct=0.0)
        assert engine.analyze(inp).forecast_accuracy == ForecastAccuracy.POOR

    def test_boundary_exactly_85(self, engine):
        inp = make_input(historical_accuracy_pct=85.0)
        assert engine.analyze(inp).forecast_accuracy == ForecastAccuracy.EXCELLENT

    def test_boundary_exactly_70(self, engine):
        inp = make_input(historical_accuracy_pct=70.0)
        assert engine.analyze(inp).forecast_accuracy == ForecastAccuracy.GOOD

    def test_boundary_exactly_50(self, engine):
        inp = make_input(historical_accuracy_pct=50.0)
        assert engine.analyze(inp).forecast_accuracy == ForecastAccuracy.FAIR


# ──────────────────────────────────────────────────────────────────────────────
# Section 11 – _call_reliability
# ──────────────────────────────────────────────────────────────────────────────

class TestCallReliability:
    def test_zero_calls_unreliable(self, engine):
        inp = make_input(calls_made=0, calls_hit=0)
        assert engine.analyze(inp).call_reliability == CallReliability.UNRELIABLE

    def test_negative_calls_unreliable(self, engine):
        inp = make_input(calls_made=-1, calls_hit=0)
        assert engine.analyze(inp).call_reliability == CallReliability.UNRELIABLE

    def test_high_reliability(self, engine):
        # call_acc=100, historical=80 → blended=100*0.60+80*0.40=60+32=92 ≥ 80
        inp = make_input(calls_made=5, calls_hit=5, historical_accuracy_pct=80.0)
        assert engine.analyze(inp).call_reliability == CallReliability.HIGH

    def test_medium_reliability(self, engine):
        # call_acc=60, historical=60 → blended=36+24=60 ≥ 60 → MEDIUM
        inp = make_input(calls_made=10, calls_hit=6, historical_accuracy_pct=60.0)
        assert engine.analyze(inp).call_reliability == CallReliability.MEDIUM

    def test_low_reliability(self, engine):
        # call_acc=40%, historical=40% → blended=24+16=40 ≥ 40 → LOW
        inp = make_input(calls_made=10, calls_hit=4, historical_accuracy_pct=40.0)
        assert engine.analyze(inp).call_reliability == CallReliability.LOW

    def test_unreliable_low_blended(self, engine):
        # call_acc=0, historical=0 → blended=0 < 40 → UNRELIABLE
        inp = make_input(calls_made=5, calls_hit=0, historical_accuracy_pct=0.0)
        assert engine.analyze(inp).call_reliability == CallReliability.UNRELIABLE

    def test_boundary_exactly_80_is_high(self, engine):
        # blended = call_acc*0.6 + hist*0.4 = 80
        # 100*0.6 + 50*0.4 = 60+20=80 → HIGH
        inp = make_input(calls_made=5, calls_hit=5, historical_accuracy_pct=50.0)
        assert engine.analyze(inp).call_reliability == CallReliability.HIGH

    def test_boundary_exactly_60_is_medium(self, engine):
        # 100*0.6 + 0*0.4=60 → MEDIUM
        inp = make_input(calls_made=5, calls_hit=5, historical_accuracy_pct=0.0)
        assert engine.analyze(inp).call_reliability == CallReliability.MEDIUM

    def test_boundary_exactly_40_is_low(self, engine):
        # 0*0.6 + 100*0.4=40 → LOW
        inp = make_input(calls_made=5, calls_hit=0, historical_accuracy_pct=100.0)
        assert engine.analyze(inp).call_reliability == CallReliability.LOW

    def test_calls_hit_capped_at_calls_made(self, engine):
        # calls_hit > calls_made → call_acc capped at 1.0
        inp = make_input(calls_made=5, calls_hit=10, historical_accuracy_pct=80.0)
        result = engine.analyze(inp)
        # call_acc=1.0; blended=60+32=92 → HIGH
        assert result.call_reliability == CallReliability.HIGH


# ──────────────────────────────────────────────────────────────────────────────
# Section 12 – _forecast_band
# ──────────────────────────────────────────────────────────────────────────────

class TestForecastBand:
    def _force_adjusted(self, engine, adjusted_val, commit=80_000.0, best_case=100_000.0):
        """Craft an input where adjusted_forecast == adjusted_val."""
        # Use: base*factor = adjusted_val → base=adjusted/factor; set factor=1.0 (acc=100%)
        # closed_won = adjusted_val (no late/early/nrr), commit small so floor<adjusted<ceiling
        inp = make_input(
            closed_won_qtd=adjusted_val,
            late_stage_pipeline=0.0,
            early_stage_pipeline=0.0,
            nrr_contribution=0.0,
            submitted_commit=commit,
            submitted_best_case=best_case,
            historical_accuracy_pct=100.0,
        )
        return engine.analyze(inp)

    def test_best_case_band(self, engine):
        # adjusted >= best_case * 0.95 → BEST_CASE
        # best_case=100k; 0.95*100k=95k; adjusted=95000
        result = self._force_adjusted(engine, 95_000.0, commit=80_000.0, best_case=100_000.0)
        assert result.forecast_band == ForecastBand.BEST_CASE

    def test_best_case_band_at_100_pct(self, engine):
        result = self._force_adjusted(engine, 100_000.0, commit=80_000.0, best_case=100_000.0)
        assert result.forecast_band == ForecastBand.BEST_CASE

    def test_upside_band(self, engine):
        # adjusted >= commit*1.10 but < best_case*0.95
        # commit=80k; 1.10*80k=88k; best_case=200k; 0.95*200k=190k
        # adjusted=89k → UPSIDE
        result = self._force_adjusted(engine, 89_000.0, commit=80_000.0, best_case=200_000.0)
        assert result.forecast_band == ForecastBand.UPSIDE

    def test_commit_band(self, engine):
        # adjusted >= commit*0.90 but < commit*1.10
        # commit=80k; 0.90*80k=72k; 1.10*80k=88k
        # adjusted=80k best_case=500k → 0.95*500k=475k > 80k → not best_case
        result = self._force_adjusted(engine, 80_000.0, commit=80_000.0, best_case=500_000.0)
        assert result.forecast_band == ForecastBand.COMMIT

    def test_likely_band(self, engine):
        # adjusted < commit*0.90
        # floor = commit*0.80, so adjusted must equal floor when estimate is low
        # commit=100k; floor=80k; best_case=200k
        # Use closed_won=0 to get floor=80k; 80k < 0.90*100k=90k → LIKELY
        inp = make_input(
            closed_won_qtd=0.0, late_stage_pipeline=0.0, early_stage_pipeline=0.0,
            nrr_contribution=0.0, submitted_commit=100_000.0,
            submitted_best_case=200_000.0, historical_accuracy_pct=100.0,
        )
        result = engine.analyze(inp)
        # adjusted = floor = 80k; 80k < 90k → LIKELY
        assert result.forecast_band == ForecastBand.LIKELY

    def test_best_case_boundary_exactly_0_95(self, engine):
        # adjusted == best_case * 0.95 exactly → BEST_CASE
        best_case = 100_000.0
        adjusted = best_case * 0.95  # 95000
        result = self._force_adjusted(engine, adjusted, commit=80_000.0, best_case=best_case)
        assert result.forecast_band == ForecastBand.BEST_CASE

    def test_upside_boundary_exactly_1_10(self, engine):
        # adjusted == commit*1.10 exactly; best_case large
        commit = 80_000.0
        adjusted = commit * 1.10  # 88000
        result = self._force_adjusted(engine, adjusted, commit=commit, best_case=200_000.0)
        assert result.forecast_band == ForecastBand.UPSIDE

    def test_commit_boundary_exactly_0_90(self, engine):
        # adjusted == commit*0.90 exactly
        commit = 100_000.0
        adjusted = commit * 0.90  # 90000; but floor=80k
        result = self._force_adjusted(engine, adjusted, commit=commit, best_case=500_000.0)
        assert result.forecast_band == ForecastBand.COMMIT


# ──────────────────────────────────────────────────────────────────────────────
# Section 13 – is_at_risk
# ──────────────────────────────────────────────────────────────────────────────

class TestIsAtRisk:
    def test_at_risk_low_coverage(self, engine):
        # coverage < 1.5 → at_risk
        inp = make_input(pipeline_value=100_000.0, quota=100_000.0,
                         last_period_attainment=100.0)
        result = engine.analyze(inp)
        assert result.is_at_risk is True

    def test_at_risk_low_attainment(self, engine):
        # coverage >= 1.5 but attainment < 70 → at_risk
        inp = make_input(pipeline_value=200_000.0, quota=100_000.0,
                         last_period_attainment=69.9)
        result = engine.analyze(inp)
        assert result.is_at_risk is True

    def test_not_at_risk(self, engine):
        # coverage >= 1.5 AND attainment >= 70
        inp = make_input(pipeline_value=200_000.0, quota=100_000.0,
                         last_period_attainment=70.0)
        result = engine.analyze(inp)
        assert result.is_at_risk is False

    def test_boundary_coverage_1_5(self, engine):
        # coverage = 1.5 exactly → NOT at_risk from coverage (need attainment <70 to be at_risk)
        inp = make_input(pipeline_value=150_000.0, quota=100_000.0,
                         last_period_attainment=100.0)
        result = engine.analyze(inp)
        assert result.is_at_risk is False

    def test_boundary_attainment_70(self, engine):
        inp = make_input(pipeline_value=200_000.0, quota=100_000.0,
                         last_period_attainment=70.0)
        result = engine.analyze(inp)
        assert result.is_at_risk is False

    def test_both_conditions_at_risk(self, engine):
        inp = make_input(pipeline_value=100_000.0, quota=100_000.0,
                         last_period_attainment=50.0)
        result = engine.analyze(inp)
        assert result.is_at_risk is True

    def test_zero_quota_at_risk(self, engine):
        # coverage=0 (quota=0) → coverage < 1.5 → at_risk
        inp = make_input(quota=0.0, submitted_commit=0.0, last_period_attainment=100.0)
        result = engine.analyze(inp)
        assert result.is_at_risk is True


# ──────────────────────────────────────────────────────────────────────────────
# Section 14 – is_sandbagging
# ──────────────────────────────────────────────────────────────────────────────

class TestIsSandbagging:
    def test_sandbagging_when_both_conditions_met(self, engine):
        # Need sandbagging_score >= 50 AND historical_beat_pct >= 20
        inp = make_input(
            closed_won_qtd=1_000_000.0, submitted_commit=1.0,
            historical_beat_pct=50.0,
        )
        result = engine.analyze(inp)
        assert result.sandbagging_score >= 50.0
        assert result.is_sandbagging is True

    def test_not_sandbagging_low_score(self, engine):
        inp = make_input(
            closed_won_qtd=0.0, late_stage_pipeline=0.0, early_stage_pipeline=0.0,
            submitted_commit=100_000.0, historical_beat_pct=50.0,
        )
        result = engine.analyze(inp)
        assert result.sandbagging_score < 50.0
        assert result.is_sandbagging is False

    def test_not_sandbagging_low_historical_beat(self, engine):
        inp = make_input(
            closed_won_qtd=1_000_000.0, submitted_commit=1.0,
            historical_beat_pct=19.9,
        )
        result = engine.analyze(inp)
        # score >= 50 but beat_pct < 20 → not sandbagging
        assert result.is_sandbagging is False

    def test_boundary_historical_beat_exactly_20(self, engine):
        inp = make_input(
            closed_won_qtd=1_000_000.0, submitted_commit=1.0,
            historical_beat_pct=20.0,
        )
        result = engine.analyze(inp)
        assert result.is_sandbagging is True

    def test_boundary_sandbagging_score_exactly_50(self, engine):
        # Design score=50 exactly: gap_ratio*0.6 + historical_beat*0.4=50
        # Set historical_beat=50 → 50*0.4=20; gap_ratio*0.6=30 → gap_ratio=50
        # gap_ratio=50 → gap=commit*0.5; commit=10000 → gap=5000
        # weighted=15000 → closed_won+late*0.65+early*0.25=15000
        # Use closed_won=15000, late=0, early=0, commit=10000
        inp = make_input(
            closed_won_qtd=15_000.0, late_stage_pipeline=0.0, early_stage_pipeline=0.0,
            submitted_commit=10_000.0, historical_beat_pct=50.0,
        )
        result = engine.analyze(inp)
        assert result.sandbagging_score == 50.0
        assert result.is_sandbagging is True


# ──────────────────────────────────────────────────────────────────────────────
# Section 15 – _forecast_action
# ──────────────────────────────────────────────────────────────────────────────

class TestForecastAction:
    def test_escalate_when_at_risk_and_low_coverage(self, engine):
        # at_risk=True AND coverage < 1.5 → ESCALATE
        inp = make_input(pipeline_value=100_000.0, quota=100_000.0,
                         last_period_attainment=50.0)
        result = engine.analyze(inp)
        assert result.forecast_action == ForecastAction.ESCALATE

    def test_investigate_when_at_risk_but_coverage_ok(self, engine):
        # at_risk due to low attainment but coverage >= 1.5 → INVESTIGATE
        inp = make_input(pipeline_value=200_000.0, quota=100_000.0,
                         last_period_attainment=50.0)
        result = engine.analyze(inp)
        assert result.forecast_action == ForecastAction.INVESTIGATE

    def test_adjust_up_sandbagging_upside(self, engine):
        # Not at_risk, sandbagging=True, band=UPSIDE → ADJUST_UP
        # Design: coverage>=1.5, attainment>=70, sandbagging_score>=50, band=UPSIDE
        # closed_won=89k, late=50k, commit=80k, best_case=200k, beat_pct=50
        # weighted=89k+50k*0.65=121.5k; gap=41.5k; gap_ratio=51.875
        # score=51.875*0.6+50*0.4=31.125+20=51.1 ≥ 50 ✓; beat_pct=50>=20 ✓ → sandbagging
        # adjusted=base*acc=(89k+50k*0.70)*1.0=124k; floor=64k; ceiling=200k→adj=124k
        # 124k >= 1.10*80k=88k and 124k < 0.95*200k=190k → UPSIDE ✓
        inp = make_input(
            pipeline_value=500_000.0, quota=100_000.0,
            last_period_attainment=90.0,
            closed_won_qtd=89_000.0,
            submitted_commit=80_000.0,
            submitted_best_case=200_000.0,
            historical_beat_pct=50.0,
            historical_accuracy_pct=100.0,
            late_stage_pipeline=50_000.0, early_stage_pipeline=0.0, nrr_contribution=0.0,
        )
        result = engine.analyze(inp)
        assert result.is_at_risk is False
        assert result.is_sandbagging is True
        assert result.forecast_band == ForecastBand.UPSIDE
        assert result.forecast_action == ForecastAction.ADJUST_UP

    def test_adjust_down_poor_accuracy_likely(self, engine):
        # Not at_risk, not sandbagging, accuracy=POOR, band=LIKELY → ADJUST_DOWN
        # coverage>=1.5, attainment>=70, accuracy<50, band=LIKELY
        # LIKELY: adjusted < commit*0.90; floor=commit*0.80; so adj=floor=commit*0.80
        # 0.80*commit < 0.90*commit → always LIKELY when estimate=floor
        inp = make_input(
            pipeline_value=500_000.0, quota=100_000.0,
            last_period_attainment=90.0,
            closed_won_qtd=0.0, late_stage_pipeline=0.0, early_stage_pipeline=0.0,
            nrr_contribution=0.0,
            submitted_commit=100_000.0, submitted_best_case=200_000.0,
            historical_accuracy_pct=30.0,  # POOR accuracy
            historical_beat_pct=0.0,
        )
        result = engine.analyze(inp)
        assert result.is_at_risk is False
        assert result.forecast_accuracy == ForecastAccuracy.POOR
        assert result.forecast_band == ForecastBand.LIKELY
        assert result.forecast_action == ForecastAction.ADJUST_DOWN

    def test_commit_as_is_default(self, engine):
        # Good coverage, good attainment, not sandbagging, not poor, not likely → COMMIT_AS_IS
        inp = make_input(
            pipeline_value=500_000.0, quota=100_000.0,
            last_period_attainment=90.0,
            historical_accuracy_pct=90.0,
            historical_beat_pct=5.0,
        )
        result = engine.analyze(inp)
        assert result.is_at_risk is False
        assert result.forecast_action == ForecastAction.COMMIT_AS_IS

    def test_escalate_priority_over_investigate(self, engine):
        # at_risk AND coverage < 1.5 → ESCALATE (not INVESTIGATE)
        inp = make_input(pipeline_value=50_000.0, quota=100_000.0,
                         last_period_attainment=50.0)
        result = engine.analyze(inp)
        assert result.forecast_action == ForecastAction.ESCALATE

    def test_investigate_not_escalate_when_coverage_ok(self, engine):
        # attainment<70 → at_risk, coverage>=1.5 → INVESTIGATE not ESCALATE
        inp = make_input(pipeline_value=200_000.0, quota=100_000.0,
                         last_period_attainment=60.0)
        result = engine.analyze(inp)
        assert result.forecast_action == ForecastAction.INVESTIGATE


# ──────────────────────────────────────────────────────────────────────────────
# Section 16 – SalesForecastEngine.analyze()
# ──────────────────────────────────────────────────────────────────────────────

class TestAnalyze:
    def test_returns_sales_forecast_result(self, engine, standard_input):
        result = engine.analyze(standard_input)
        assert isinstance(result, SalesForecastResult)

    def test_result_stored_in_results(self, engine, standard_input):
        result = engine.analyze(standard_input)
        assert result in engine._results

    def test_multiple_analyzes_accumulate(self, engine):
        for i in range(5):
            inp = make_input(rep_id=f"REP-{i:03d}")
            engine.analyze(inp)
        assert len(engine._results) == 5

    def test_fields_correctly_transferred(self, engine, standard_input):
        result = engine.analyze(standard_input)
        assert result.rep_id == standard_input.rep_id
        assert result.rep_name == standard_input.rep_name
        assert result.manager_id == standard_input.manager_id


# ──────────────────────────────────────────────────────────────────────────────
# Section 17 – SalesForecastEngine.analyze_batch()
# ──────────────────────────────────────────────────────────────────────────────

class TestAnalyzeBatch:
    def test_returns_list(self, engine):
        inputs = [make_input(rep_id=f"REP-{i}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        assert isinstance(results, list)

    def test_correct_count(self, engine):
        inputs = [make_input(rep_id=f"REP-{i}") for i in range(5)]
        results = engine.analyze_batch(inputs)
        assert len(results) == 5

    def test_results_all_stored(self, engine):
        inputs = [make_input(rep_id=f"REP-{i}") for i in range(4)]
        engine.analyze_batch(inputs)
        assert len(engine._results) == 4

    def test_empty_batch(self, engine):
        results = engine.analyze_batch([])
        assert results == []

    def test_single_item_batch(self, engine, standard_input):
        results = engine.analyze_batch([standard_input])
        assert len(results) == 1
        assert isinstance(results[0], SalesForecastResult)

    def test_order_preserved(self, engine):
        rep_ids = [f"REP-{i:03d}" for i in range(5)]
        inputs = [make_input(rep_id=rid) for rid in rep_ids]
        results = engine.analyze_batch(inputs)
        for result, rid in zip(results, rep_ids):
            assert result.rep_id == rid


# ──────────────────────────────────────────────────────────────────────────────
# Section 18 – SalesForecastEngine.reset()
# ──────────────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_results(self, engine, standard_input):
        engine.analyze(standard_input)
        engine.reset()
        assert engine._results == []

    def test_reset_multiple_times(self, engine, standard_input):
        engine.analyze(standard_input)
        engine.reset()
        engine.reset()
        assert engine._results == []

    def test_can_analyze_after_reset(self, engine, standard_input):
        engine.analyze(standard_input)
        engine.reset()
        result = engine.analyze(standard_input)
        assert result is not None
        assert len(engine._results) == 1

    def test_reset_empty_engine_is_safe(self, engine):
        engine.reset()
        assert engine._results == []


# ──────────────────────────────────────────────────────────────────────────────
# Section 19 – Properties
# ──────────────────────────────────────────────────────────────────────────────

class TestAtRiskReps:
    def test_empty_when_no_results(self, engine):
        assert engine.at_risk_reps == []

    def test_returns_at_risk(self, engine):
        risky = make_input(pipeline_value=50_000.0, quota=100_000.0,
                           last_period_attainment=50.0, rep_id="RISK-1")
        safe = make_input(pipeline_value=300_000.0, quota=100_000.0,
                          last_period_attainment=90.0, rep_id="SAFE-1")
        engine.analyze_batch([risky, safe])
        at_risk = engine.at_risk_reps
        assert len(at_risk) == 1
        assert at_risk[0].rep_id == "RISK-1"

    def test_all_at_risk(self, engine):
        inputs = [
            make_input(rep_id=f"RISK-{i}", pipeline_value=50_000.0,
                       quota=100_000.0, last_period_attainment=50.0)
            for i in range(3)
        ]
        engine.analyze_batch(inputs)
        assert len(engine.at_risk_reps) == 3

    def test_none_at_risk(self, engine):
        inputs = [
            make_input(rep_id=f"SAFE-{i}", pipeline_value=300_000.0,
                       quota=100_000.0, last_period_attainment=90.0)
            for i in range(3)
        ]
        engine.analyze_batch(inputs)
        assert len(engine.at_risk_reps) == 0


class TestSandbaggingReps:
    def test_empty_when_no_results(self, engine):
        assert engine.sandbagging_reps == []

    def test_returns_sandbagging(self, engine):
        # closed_won=170k, commit=100k, beat_pct=20
        # weighted=170k; gap=70k; gap_ratio=70; score=70*0.6+20*0.4=42+8=50 ✓; beat>=20 ✓
        sdb = make_input(
            closed_won_qtd=170_000.0, submitted_commit=100_000.0,
            submitted_best_case=300_000.0, historical_beat_pct=20.0,
            pipeline_value=500_000.0, quota=100_000.0,
            last_period_attainment=90.0,
            late_stage_pipeline=0.0, early_stage_pipeline=0.0, nrr_contribution=0.0,
            historical_accuracy_pct=100.0, rep_id="SDB-1",
        )
        normal = make_input(
            closed_won_qtd=0.0, submitted_commit=80_000.0,
            historical_beat_pct=5.0, rep_id="NRM-1",
        )
        engine.analyze_batch([sdb, normal])
        sdb_reps = engine.sandbagging_reps
        ids = [r.rep_id for r in sdb_reps]
        assert "SDB-1" in ids

    def test_none_sandbagging(self, engine):
        inputs = [make_input(rep_id=f"N-{i}", historical_beat_pct=5.0) for i in range(3)]
        engine.analyze_batch(inputs)
        assert engine.sandbagging_reps == []


class TestHighReliabilityReps:
    def test_empty_when_no_results(self, engine):
        assert engine.high_reliability_reps == []

    def test_high_reliability_filtered(self, engine):
        high = make_input(calls_made=5, calls_hit=5, historical_accuracy_pct=80.0, rep_id="HIGH-1")
        low = make_input(calls_made=0, calls_hit=0, rep_id="LOW-1")
        engine.analyze_batch([high, low])
        hr_reps = engine.high_reliability_reps
        assert any(r.rep_id == "HIGH-1" for r in hr_reps)

    def test_none_high_reliability(self, engine):
        inputs = [make_input(rep_id=f"U-{i}", calls_made=0, calls_hit=0) for i in range(3)]
        engine.analyze_batch(inputs)
        assert engine.high_reliability_reps == []


class TestTotalAdjustedForecast:
    def test_zero_when_empty(self, engine):
        assert engine.total_adjusted_forecast == 0.0

    def test_sum_of_adjusted_forecasts(self, engine):
        inputs = [make_input(rep_id=f"REP-{i}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        expected = round(sum(r.adjusted_forecast for r in results), 2)
        assert engine.total_adjusted_forecast == expected

    def test_rounded_to_2dp(self, engine):
        inputs = [make_input(rep_id=f"REP-{i}", closed_won_qtd=33_333.333)
                  for i in range(3)]
        engine.analyze_batch(inputs)
        assert engine.total_adjusted_forecast == round(engine.total_adjusted_forecast, 2)


class TestTotalUpsidePotential:
    def test_zero_when_empty(self, engine):
        assert engine.total_upside_potential == 0.0

    def test_sum_of_upside_potentials(self, engine):
        inputs = [make_input(rep_id=f"REP-{i}", submitted_best_case=120_000.0,
                             submitted_commit=80_000.0) for i in range(3)]
        results = engine.analyze_batch(inputs)
        expected = round(sum(r.upside_potential for r in results), 2)
        assert engine.total_upside_potential == expected

    def test_rounded_to_2dp(self, engine):
        inputs = [make_input(rep_id=f"REP-{i}", submitted_best_case=100_000.333,
                             submitted_commit=80_000.0) for i in range(3)]
        engine.analyze_batch(inputs)
        assert engine.total_upside_potential == round(engine.total_upside_potential, 2)


# ──────────────────────────────────────────────────────────────────────────────
# Section 20 – summary() invariants
# ──────────────────────────────────────────────────────────────────────────────

class TestSummaryKeyCount:
    def test_empty_summary_has_13_keys(self, engine):
        s = engine.summary()
        assert len(s) == 13

    def test_nonempty_summary_has_13_keys(self, engine, standard_input):
        engine.analyze(standard_input)
        s = engine.summary()
        assert len(s) == 13

    def test_exact_13_key_names(self, engine, standard_input):
        engine.analyze(standard_input)
        s = engine.summary()
        expected_keys = {
            "total", "band_counts", "accuracy_counts", "reliability_counts",
            "action_counts", "avg_coverage_ratio", "avg_pipeline_health",
            "total_adjusted_forecast", "at_risk_count", "sandbagging_count",
            "high_reliability_count", "total_upside_potential", "avg_sandbagging_score",
        }
        assert set(s.keys()) == expected_keys


class TestSummaryEmpty:
    def test_total_is_zero(self, engine):
        assert engine.summary()["total"] == 0

    def test_band_counts_empty_dict(self, engine):
        assert engine.summary()["band_counts"] == {}

    def test_accuracy_counts_empty_dict(self, engine):
        assert engine.summary()["accuracy_counts"] == {}

    def test_reliability_counts_empty_dict(self, engine):
        assert engine.summary()["reliability_counts"] == {}

    def test_action_counts_empty_dict(self, engine):
        assert engine.summary()["action_counts"] == {}

    def test_avg_coverage_zero(self, engine):
        assert engine.summary()["avg_coverage_ratio"] == 0.0

    def test_avg_pipeline_health_zero(self, engine):
        assert engine.summary()["avg_pipeline_health"] == 0.0

    def test_total_adjusted_forecast_zero(self, engine):
        assert engine.summary()["total_adjusted_forecast"] == 0.0

    def test_at_risk_count_zero(self, engine):
        assert engine.summary()["at_risk_count"] == 0

    def test_sandbagging_count_zero(self, engine):
        assert engine.summary()["sandbagging_count"] == 0

    def test_high_reliability_count_zero(self, engine):
        assert engine.summary()["high_reliability_count"] == 0

    def test_total_upside_potential_zero(self, engine):
        assert engine.summary()["total_upside_potential"] == 0.0

    def test_avg_sandbagging_score_zero(self, engine):
        assert engine.summary()["avg_sandbagging_score"] == 0.0


class TestSummaryNonEmpty:
    def test_total_correct(self, engine):
        inputs = [make_input(rep_id=f"REP-{i}") for i in range(5)]
        engine.analyze_batch(inputs)
        assert engine.summary()["total"] == 5

    def test_band_counts_populated(self, engine, standard_input):
        engine.analyze(standard_input)
        s = engine.summary()
        assert len(s["band_counts"]) >= 1
        assert sum(s["band_counts"].values()) == 1

    def test_accuracy_counts_populated(self, engine, standard_input):
        engine.analyze(standard_input)
        s = engine.summary()
        assert sum(s["accuracy_counts"].values()) == 1

    def test_reliability_counts_populated(self, engine, standard_input):
        engine.analyze(standard_input)
        s = engine.summary()
        assert sum(s["reliability_counts"].values()) == 1

    def test_action_counts_populated(self, engine, standard_input):
        engine.analyze(standard_input)
        s = engine.summary()
        assert sum(s["action_counts"].values()) == 1

    def test_avg_coverage_ratio_correct(self, engine):
        inp1 = make_input(rep_id="R1", pipeline_value=200_000.0, quota=100_000.0)
        inp2 = make_input(rep_id="R2", pipeline_value=300_000.0, quota=100_000.0)
        engine.analyze_batch([inp1, inp2])
        # coverage: 2.0 and 3.0; avg=2.5
        s = engine.summary()
        assert s["avg_coverage_ratio"] == 2.5

    def test_avg_pipeline_health_correct(self, engine):
        inputs = [make_input(rep_id=f"REP-{i}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        expected_avg = round(sum(r.pipeline_health for r in results) / 3, 1)
        assert engine.summary()["avg_pipeline_health"] == expected_avg

    def test_total_adjusted_forecast_matches_property(self, engine, standard_input):
        engine.analyze(standard_input)
        s = engine.summary()
        assert s["total_adjusted_forecast"] == engine.total_adjusted_forecast

    def test_at_risk_count_correct(self, engine):
        risky = make_input(rep_id="RISK", pipeline_value=50_000.0, quota=100_000.0,
                           last_period_attainment=50.0)
        safe = make_input(rep_id="SAFE", pipeline_value=300_000.0, quota=100_000.0,
                          last_period_attainment=90.0)
        engine.analyze_batch([risky, safe])
        assert engine.summary()["at_risk_count"] == 1

    def test_high_reliability_count_correct(self, engine):
        high = make_input(rep_id="HIGH", calls_made=5, calls_hit=5,
                          historical_accuracy_pct=80.0)
        low = make_input(rep_id="LOW", calls_made=0, calls_hit=0)
        engine.analyze_batch([high, low])
        assert engine.summary()["high_reliability_count"] == 1

    def test_total_upside_potential_matches_property(self, engine, standard_input):
        engine.analyze(standard_input)
        s = engine.summary()
        assert s["total_upside_potential"] == engine.total_upside_potential

    def test_avg_sandbagging_score_correct(self, engine):
        inputs = [make_input(rep_id=f"REP-{i}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        expected = round(sum(r.sandbagging_score for r in results) / 3, 1)
        assert engine.summary()["avg_sandbagging_score"] == expected

    def test_band_counts_sum_equals_total(self, engine):
        inputs = [make_input(rep_id=f"REP-{i}") for i in range(7)]
        engine.analyze_batch(inputs)
        s = engine.summary()
        assert sum(s["band_counts"].values()) == s["total"]

    def test_accuracy_counts_sum_equals_total(self, engine):
        inputs = [make_input(rep_id=f"REP-{i}") for i in range(7)]
        engine.analyze_batch(inputs)
        s = engine.summary()
        assert sum(s["accuracy_counts"].values()) == s["total"]

    def test_reliability_counts_sum_equals_total(self, engine):
        inputs = [make_input(rep_id=f"REP-{i}") for i in range(7)]
        engine.analyze_batch(inputs)
        s = engine.summary()
        assert sum(s["reliability_counts"].values()) == s["total"]

    def test_action_counts_sum_equals_total(self, engine):
        inputs = [make_input(rep_id=f"REP-{i}") for i in range(7)]
        engine.analyze_batch(inputs)
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_13_keys_preserved_after_reset_and_reuse(self, engine, standard_input):
        engine.analyze(standard_input)
        engine.reset()
        engine.analyze(standard_input)
        s = engine.summary()
        assert len(s) == 13


# ──────────────────────────────────────────────────────────────────────────────
# Section 21 – End-to-end scenarios
# ──────────────────────────────────────────────────────────────────────────────

class TestEndToEndScenarios:
    def test_quota_buster_rep(self, engine):
        """Rep who exceeds quota in every dimension."""
        inp = make_input(
            rep_id="STAR-1", quota=100_000.0,
            submitted_commit=110_000.0, submitted_best_case=130_000.0,
            pipeline_value=500_000.0, closed_won_qtd=80_000.0,
            late_stage_pipeline=80_000.0, early_stage_pipeline=40_000.0,
            historical_accuracy_pct=95.0, historical_beat_pct=15.0,
            last_period_attainment=120.0,
            calls_made=10, calls_hit=9, slipped_deals_count=0,
            nrr_contribution=10_000.0,
        )
        result = engine.analyze(inp)
        assert result.is_at_risk is False
        assert result.forecast_accuracy == ForecastAccuracy.EXCELLENT
        assert result.call_reliability == CallReliability.HIGH
        assert result.commit_vs_quota_pct == 110.0

    def test_struggling_rep(self, engine):
        """Rep with poor pipeline and low attainment."""
        inp = make_input(
            rep_id="POOR-1", quota=100_000.0,
            submitted_commit=30_000.0, submitted_best_case=50_000.0,
            pipeline_value=40_000.0, closed_won_qtd=5_000.0,
            late_stage_pipeline=10_000.0, early_stage_pipeline=5_000.0,
            historical_accuracy_pct=40.0, historical_beat_pct=5.0,
            last_period_attainment=50.0,
            calls_made=2, calls_hit=0, slipped_deals_count=3,
            nrr_contribution=0.0,
        )
        result = engine.analyze(inp)
        assert result.is_at_risk is True
        assert result.forecast_accuracy == ForecastAccuracy.POOR
        assert result.forecast_action == ForecastAction.ESCALATE

    def test_sandbagging_superstar(self, engine):
        """Rep who consistently understates their commit.
        closed_won=170k, commit=80k, beat_pct=25
        gap=90k; gap_ratio=90k/80k*100=112.5; score=112.5*0.6+25*0.4=67.5+10=77.5 >=50 ✓
        beat_pct=25>=20 ✓ → is_sandbagging=True
        adjusted: base=170k*1.0=170k; floor=64k; ceiling=200k → adj=170k
        170k >= 1.10*80k=88k, 170k < 0.95*200k=190k → UPSIDE ✓
        """
        inp = make_input(
            rep_id="SDB-STAR", quota=100_000.0,
            submitted_commit=80_000.0, submitted_best_case=200_000.0,
            pipeline_value=500_000.0, closed_won_qtd=170_000.0,
            late_stage_pipeline=0.0, early_stage_pipeline=0.0,
            historical_accuracy_pct=100.0, historical_beat_pct=25.0,
            last_period_attainment=90.0,
            calls_made=5, calls_hit=5, slipped_deals_count=0,
            nrr_contribution=0.0,
        )
        result = engine.analyze(inp)
        assert result.is_sandbagging is True
        assert result.forecast_band == ForecastBand.UPSIDE
        assert result.forecast_action == ForecastAction.ADJUST_UP

    def test_multi_rep_team_summary(self, engine):
        """Team of 3 reps: verify summary aggregation."""
        inputs = [
            make_input(rep_id="REP-A", pipeline_value=300_000.0, quota=100_000.0,
                       last_period_attainment=90.0),
            make_input(rep_id="REP-B", pipeline_value=50_000.0, quota=100_000.0,
                       last_period_attainment=50.0),
            make_input(rep_id="REP-C", pipeline_value=400_000.0, quota=100_000.0,
                       last_period_attainment=80.0),
        ]
        engine.analyze_batch(inputs)
        s = engine.summary()
        assert s["total"] == 3
        assert s["at_risk_count"] == 1  # REP-B
        assert len(s) == 13

    def test_full_pipeline_to_summary_consistency(self, engine):
        """Properties match what summary reports."""
        inputs = [make_input(rep_id=f"REP-{i}") for i in range(10)]
        engine.analyze_batch(inputs)
        s = engine.summary()
        assert s["at_risk_count"] == len(engine.at_risk_reps)
        assert s["sandbagging_count"] == len(engine.sandbagging_reps)
        assert s["high_reliability_count"] == len(engine.high_reliability_reps)
        assert s["total_adjusted_forecast"] == engine.total_adjusted_forecast
        assert s["total_upside_potential"] == engine.total_upside_potential

    def test_reset_then_fresh_summary(self, engine, standard_input):
        engine.analyze(standard_input)
        engine.reset()
        s = engine.summary()
        assert s["total"] == 0
        assert s["band_counts"] == {}

    def test_incremental_analyze_vs_batch(self):
        """Batch and sequential analyze produce same results."""
        engine_seq = SalesForecastEngine()
        engine_bat = SalesForecastEngine()
        inputs = [make_input(rep_id=f"REP-{i}") for i in range(5)]
        for inp in inputs:
            engine_seq.analyze(inp)
        engine_bat.analyze_batch(inputs)
        assert engine_seq.total_adjusted_forecast == engine_bat.total_adjusted_forecast
        assert engine_seq.total_upside_potential == engine_bat.total_upside_potential

    def test_zero_pipeline_rep(self, engine):
        """Rep with no pipeline at all."""
        inp = make_input(
            pipeline_value=0.0, closed_won_qtd=0.0, late_stage_pipeline=0.0,
            early_stage_pipeline=0.0, nrr_contribution=0.0,
            submitted_commit=50_000.0, submitted_best_case=100_000.0,
            quota=100_000.0, last_period_attainment=90.0,
        )
        result = engine.analyze(inp)
        assert result.coverage_ratio == 0.0
        assert result.is_at_risk is True  # coverage < 1.5

    def test_nrr_heavy_rep(self, engine):
        """Rep whose revenue is mostly NRR."""
        inp = make_input(
            closed_won_qtd=0.0, late_stage_pipeline=0.0, early_stage_pipeline=0.0,
            nrr_contribution=200_000.0, submitted_commit=100_000.0,
            submitted_best_case=300_000.0, historical_accuracy_pct=90.0,
            pipeline_value=300_000.0, quota=100_000.0, last_period_attainment=90.0,
        )
        result = engine.analyze(inp)
        # base=200000; factor=0.9; estimate=180000; floor=80000; ceiling=300000
        assert result.adjusted_forecast == round(200_000.0 * 0.9, 2)

    def test_exact_boundary_coverage_1_5_at_risk_false(self, engine):
        inp = make_input(pipeline_value=150_000.0, quota=100_000.0,
                         last_period_attainment=90.0)
        result = engine.analyze(inp)
        assert result.coverage_ratio == 1.5
        assert result.is_at_risk is False

    def test_coverage_just_below_1_5_at_risk_true(self, engine):
        # 149000/100000 = 1.49 (rounds to 1.49 at 2dp) → coverage<1.5 → at_risk
        inp = make_input(pipeline_value=149_000.0, quota=100_000.0,
                         last_period_attainment=90.0)
        result = engine.analyze(inp)
        assert result.coverage_ratio < 1.5
        assert result.is_at_risk is True


# ──────────────────────────────────────────────────────────────────────────────
# Section 22 – Edge cases and corner conditions
# ──────────────────────────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_all_zeros_input(self, engine):
        inp = make_input(
            quota=0.0, submitted_commit=0.0, submitted_best_case=0.0,
            pipeline_value=0.0, closed_won_qtd=0.0, late_stage_pipeline=0.0,
            early_stage_pipeline=0.0, days_remaining=0, period_days=0,
            historical_accuracy_pct=0.0, historical_beat_pct=0.0,
            last_period_attainment=0.0, slipped_deals_count=0,
            new_pipeline_added_qtd=0.0, calls_made=0, calls_hit=0,
            nrr_contribution=0.0,
        )
        result = engine.analyze(inp)
        assert result.coverage_ratio == 0.0
        assert result.adjusted_forecast == 0.0
        assert result.upside_potential == 0.0
        assert result.commit_vs_quota_pct == 0.0

    def test_very_large_values_no_crash(self, engine):
        inp = make_input(
            quota=1e9, submitted_commit=1e9, submitted_best_case=2e9,
            pipeline_value=5e9, closed_won_qtd=1e9,
            late_stage_pipeline=2e9, early_stage_pipeline=1e9,
        )
        result = engine.analyze(inp)
        assert result.adjusted_forecast <= 2e9  # capped at best_case

    def test_calls_hit_gt_calls_made_handled(self, engine):
        """calls_hit > calls_made is capped via min(1, calls_hit/calls_made)."""
        inp = make_input(calls_made=5, calls_hit=10, historical_accuracy_pct=80.0)
        result = engine.analyze(inp)
        # Should not crash and reliability should be HIGH (capped at 1.0)
        assert result.call_reliability == CallReliability.HIGH

    def test_slipped_deals_drives_health_to_zero(self, engine):
        inp = make_input(
            pipeline_value=0.0, quota=100_000.0,
            late_stage_pipeline=0.0, submitted_commit=0.0,
            calls_made=5, calls_hit=0, slipped_deals_count=100,
        )
        result = engine.analyze(inp)
        assert result.pipeline_health == 0.0

    def test_string_identity_fields_preserved(self, engine):
        inp = make_input(rep_id="  spaces  ", rep_name="Name With Spaces",
                         manager_id="MGR 123")
        result = engine.analyze(inp)
        assert result.rep_id == "  spaces  "
        assert result.rep_name == "Name With Spaces"
        assert result.manager_id == "MGR 123"

    def test_forecast_band_values_are_valid_enum_strings(self, engine, standard_input):
        result = engine.analyze(standard_input)
        valid = {b.value for b in ForecastBand}
        assert result.to_dict()["forecast_band"] in valid

    def test_forecast_accuracy_values_are_valid_enum_strings(self, engine, standard_input):
        result = engine.analyze(standard_input)
        valid = {a.value for a in ForecastAccuracy}
        assert result.to_dict()["forecast_accuracy"] in valid

    def test_call_reliability_values_are_valid_enum_strings(self, engine, standard_input):
        result = engine.analyze(standard_input)
        valid = {c.value for c in CallReliability}
        assert result.to_dict()["call_reliability"] in valid

    def test_forecast_action_values_are_valid_enum_strings(self, engine, standard_input):
        result = engine.analyze(standard_input)
        valid = {a.value for a in ForecastAction}
        assert result.to_dict()["forecast_action"] in valid

    def test_independent_engine_instances(self):
        e1 = SalesForecastEngine()
        e2 = SalesForecastEngine()
        inp = make_input()
        e1.analyze(inp)
        assert len(e2._results) == 0

    def test_historical_accuracy_100_no_penalty(self, engine):
        inp = make_input(historical_accuracy_pct=100.0)
        result = engine.analyze(inp)
        # accuracy factor = 1.0, no penalty
        assert result.forecast_accuracy == ForecastAccuracy.EXCELLENT

    def test_quota_very_small(self, engine):
        inp = make_input(quota=0.01, submitted_commit=0.01, pipeline_value=0.02)
        result = engine.analyze(inp)
        assert result.coverage_ratio == round(0.02 / 0.01, 2)

    def test_single_slipped_deal_reduces_health(self, engine):
        inp_no_slip = make_input(
            pipeline_value=0.0, quota=100_000.0,
            late_stage_pipeline=0.0, submitted_commit=0.0,
            calls_made=0, calls_hit=0, slipped_deals_count=0,
        )
        inp_one_slip = make_input(
            pipeline_value=0.0, quota=100_000.0,
            late_stage_pipeline=0.0, submitted_commit=0.0,
            calls_made=0, calls_hit=0, slipped_deals_count=1,
        )
        r_no = engine.analyze(inp_no_slip)
        r_one = engine.analyze(inp_one_slip)
        assert r_one.pipeline_health < r_no.pipeline_health

    def test_upside_potential_cannot_be_negative(self, engine):
        inp = make_input(submitted_best_case=50_000.0, submitted_commit=80_000.0)
        result = engine.analyze(inp)
        assert result.upside_potential >= 0.0

    def test_sandbagging_score_cannot_exceed_100(self, engine):
        inp = make_input(
            closed_won_qtd=1e9, late_stage_pipeline=1e9, early_stage_pipeline=1e9,
            submitted_commit=1.0, historical_beat_pct=100.0,
        )
        result = engine.analyze(inp)
        assert result.sandbagging_score <= 100.0

    def test_sandbagging_score_cannot_be_negative(self, engine):
        inp = make_input(
            closed_won_qtd=0.0, late_stage_pipeline=0.0, early_stage_pipeline=0.0,
            submitted_commit=100_000.0, historical_beat_pct=0.0,
        )
        result = engine.analyze(inp)
        assert result.sandbagging_score >= 0.0

    def test_pipeline_health_cannot_exceed_100(self, engine):
        inp = make_input(
            pipeline_value=1e9, quota=1.0,
            late_stage_pipeline=1e9, submitted_commit=1.0,
            calls_made=100, calls_hit=100, slipped_deals_count=0,
        )
        result = engine.analyze(inp)
        assert result.pipeline_health <= 100.0

    def test_pipeline_health_cannot_be_negative(self, engine):
        inp = make_input(slipped_deals_count=1000)
        result = engine.analyze(inp)
        assert result.pipeline_health >= 0.0

    def test_coverage_ratio_cannot_be_negative(self, engine):
        inp = make_input(pipeline_value=0.0, quota=100_000.0)
        result = engine.analyze(inp)
        assert result.coverage_ratio >= 0.0


# ──────────────────────────────────────────────────────────────────────────────
# Section 23 – Precision/rounding spot checks
# ──────────────────────────────────────────────────────────────────────────────

class TestRoundingPrecision:
    def test_coverage_ratio_is_2dp(self, engine):
        inp = make_input(pipeline_value=100_000.0, quota=300_000.0)
        result = engine.analyze(inp)
        val = result.coverage_ratio
        assert round(val, 2) == val

    def test_sandbagging_score_is_1dp(self, engine, standard_input):
        result = engine.analyze(standard_input)
        val = result.sandbagging_score
        assert round(val, 1) == val

    def test_pipeline_health_is_1dp(self, engine, standard_input):
        result = engine.analyze(standard_input)
        val = result.pipeline_health
        assert round(val, 1) == val

    def test_adjusted_forecast_is_2dp(self, engine, standard_input):
        result = engine.analyze(standard_input)
        val = result.adjusted_forecast
        assert round(val, 2) == val

    def test_commit_vs_quota_pct_is_1dp(self, engine):
        inp = make_input(submitted_commit=100_000.0, quota=300_000.0)
        result = engine.analyze(inp)
        val = result.commit_vs_quota_pct
        assert round(val, 1) == val

    def test_upside_potential_is_2dp(self, engine):
        inp = make_input(submitted_best_case=100_000.005, submitted_commit=80_000.0)
        result = engine.analyze(inp)
        val = result.upside_potential
        assert round(val, 2) == val

    def test_avg_coverage_ratio_is_2dp_in_summary(self, engine):
        inputs = [make_input(rep_id=f"R{i}", pipeline_value=100_000.0 * (i + 1),
                             quota=300_000.0) for i in range(3)]
        engine.analyze_batch(inputs)
        val = engine.summary()["avg_coverage_ratio"]
        assert round(val, 2) == val

    def test_avg_pipeline_health_is_1dp_in_summary(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(3)]
        engine.analyze_batch(inputs)
        val = engine.summary()["avg_pipeline_health"]
        assert round(val, 1) == val

    def test_avg_sandbagging_score_is_1dp_in_summary(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(3)]
        engine.analyze_batch(inputs)
        val = engine.summary()["avg_sandbagging_score"]
        assert round(val, 1) == val


# ──────────────────────────────────────────────────────────────────────────────
# Section 24 – Boundary sweeps across all accuracy thresholds
# ──────────────────────────────────────────────────────────────────────────────

class TestAccuracyBoundarySweep:
    @pytest.mark.parametrize("pct,expected", [
        (100.0, ForecastAccuracy.EXCELLENT),
        (90.0,  ForecastAccuracy.EXCELLENT),
        (85.0,  ForecastAccuracy.EXCELLENT),
        (84.99, ForecastAccuracy.GOOD),
        (80.0,  ForecastAccuracy.GOOD),
        (70.0,  ForecastAccuracy.GOOD),
        (69.99, ForecastAccuracy.FAIR),
        (60.0,  ForecastAccuracy.FAIR),
        (50.0,  ForecastAccuracy.FAIR),
        (49.99, ForecastAccuracy.POOR),
        (25.0,  ForecastAccuracy.POOR),
        (0.0,   ForecastAccuracy.POOR),
    ])
    def test_accuracy_thresholds(self, engine, pct, expected):
        inp = make_input(historical_accuracy_pct=pct)
        result = engine.analyze(inp)
        assert result.forecast_accuracy == expected


# ──────────────────────────────────────────────────────────────────────────────
# Section 25 – Boundary sweeps for call_reliability
# ──────────────────────────────────────────────────────────────────────────────

class TestCallReliabilityBoundarySweep:
    @pytest.mark.parametrize("calls_made,calls_hit,hist_acc,expected", [
        (0, 0, 90.0, CallReliability.UNRELIABLE),   # no calls
        (5, 5, 80.0, CallReliability.HIGH),          # blended=92 ≥ 80
        (5, 5, 50.0, CallReliability.HIGH),          # blended=80 ≥ 80
        (5, 3, 60.0, CallReliability.MEDIUM),        # blended=36+24=60 ≥ 60
        (10, 4, 40.0, CallReliability.LOW),          # blended=24+16=40 ≥ 40
        (5, 0, 0.0,  CallReliability.UNRELIABLE),   # blended=0 < 40
        (5, 0, 95.0, CallReliability.UNRELIABLE),     # blended=0*0.6+95*0.4=38 < 40 → UNRELIABLE
    ])
    def test_call_reliability_thresholds(self, engine, calls_made, calls_hit, hist_acc, expected):
        inp = make_input(calls_made=calls_made, calls_hit=calls_hit,
                         historical_accuracy_pct=hist_acc)
        result = engine.analyze(inp)
        assert result.call_reliability == expected


# ──────────────────────────────────────────────────────────────────────────────
# Section 26 – Additional unit tests for _adjusted_forecast boundaries
# ──────────────────────────────────────────────────────────────────────────────

class TestAdjustedForecastBoundaries:
    def test_estimate_between_floor_and_ceiling(self, engine):
        # estimate=90k; floor=80k; ceiling=100k → adjusted=90k
        inp = make_input(
            closed_won_qtd=90_000.0, late_stage_pipeline=0.0, early_stage_pipeline=0.0,
            nrr_contribution=0.0, submitted_commit=100_000.0,
            submitted_best_case=100_000.0, historical_accuracy_pct=100.0,
        )
        result = engine.analyze(inp)
        assert result.adjusted_forecast == 90_000.0

    def test_accuracy_factor_0_5_minimum(self, engine):
        """historical_accuracy_pct=0 → factor=0.5, not 0"""
        inp = make_input(
            closed_won_qtd=200_000.0, late_stage_pipeline=0.0, early_stage_pipeline=0.0,
            nrr_contribution=0.0, submitted_commit=1.0,
            submitted_best_case=200_000.0, historical_accuracy_pct=0.0,
        )
        # base=200000; factor=0.5; estimate=100000; floor≈0.8; ceiling=200000 → adj=100000
        result = engine.analyze(inp)
        assert result.adjusted_forecast == 100_000.0

    def test_best_case_zero_forces_floor(self, engine):
        # If best_case=0 and commit=0, floor=0, ceiling=0, estimate=0 → 0.0
        inp = make_input(
            closed_won_qtd=0.0, late_stage_pipeline=0.0, early_stage_pipeline=0.0,
            nrr_contribution=0.0, submitted_commit=0.0,
            submitted_best_case=0.0, historical_accuracy_pct=100.0,
        )
        result = engine.analyze(inp)
        assert result.adjusted_forecast == 0.0


# ──────────────────────────────────────────────────────────────────────────────
# Section 27 – to_dict() values match result attributes
# ──────────────────────────────────────────────────────────────────────────────

class TestToDictValuesMatchAttributes:
    def test_adjusted_forecast_matches(self, engine, standard_input):
        result = engine.analyze(standard_input)
        assert result.to_dict()["adjusted_forecast"] == result.adjusted_forecast

    def test_coverage_ratio_matches(self, engine, standard_input):
        result = engine.analyze(standard_input)
        assert result.to_dict()["coverage_ratio"] == result.coverage_ratio

    def test_sandbagging_score_matches(self, engine, standard_input):
        result = engine.analyze(standard_input)
        assert result.to_dict()["sandbagging_score"] == result.sandbagging_score

    def test_pipeline_health_matches(self, engine, standard_input):
        result = engine.analyze(standard_input)
        assert result.to_dict()["pipeline_health"] == result.pipeline_health

    def test_commit_vs_quota_pct_matches(self, engine, standard_input):
        result = engine.analyze(standard_input)
        assert result.to_dict()["commit_vs_quota_pct"] == result.commit_vs_quota_pct

    def test_upside_potential_matches(self, engine, standard_input):
        result = engine.analyze(standard_input)
        assert result.to_dict()["upside_potential"] == result.upside_potential

    def test_is_at_risk_matches(self, engine, standard_input):
        result = engine.analyze(standard_input)
        assert result.to_dict()["is_at_risk"] == result.is_at_risk

    def test_is_sandbagging_matches(self, engine, standard_input):
        result = engine.analyze(standard_input)
        assert result.to_dict()["is_sandbagging"] == result.is_sandbagging

    def test_forecast_band_is_enum_value(self, engine, standard_input):
        result = engine.analyze(standard_input)
        assert result.to_dict()["forecast_band"] == result.forecast_band.value

    def test_forecast_accuracy_is_enum_value(self, engine, standard_input):
        result = engine.analyze(standard_input)
        assert result.to_dict()["forecast_accuracy"] == result.forecast_accuracy.value

    def test_call_reliability_is_enum_value(self, engine, standard_input):
        result = engine.analyze(standard_input)
        assert result.to_dict()["call_reliability"] == result.call_reliability.value

    def test_forecast_action_is_enum_value(self, engine, standard_input):
        result = engine.analyze(standard_input)
        assert result.to_dict()["forecast_action"] == result.forecast_action.value


# ──────────────────────────────────────────────────────────────────────────────
# Section 28 – Parametrized coverage ratio tests
# ──────────────────────────────────────────────────────────────────────────────

class TestCoverageRatioParametrized:
    @pytest.mark.parametrize("pipeline,quota,expected", [
        (0.0, 100_000.0, 0.0),
        (50_000.0, 100_000.0, 0.5),
        (100_000.0, 100_000.0, 1.0),
        (150_000.0, 100_000.0, 1.5),
        (200_000.0, 100_000.0, 2.0),
        (300_000.0, 100_000.0, 3.0),
        (100_000.0, 0.0, 0.0),
        (100_000.0, 300_000.0, round(1/3, 2)),
    ])
    def test_coverage_ratio(self, engine, pipeline, quota, expected):
        inp = make_input(pipeline_value=pipeline, quota=quota,
                         submitted_commit=max(0.0, quota * 0.8))
        result = engine.analyze(inp)
        assert result.coverage_ratio == expected


# ──────────────────────────────────────────────────────────────────────────────
# Section 29 – Parametrized at_risk tests
# ──────────────────────────────────────────────────────────────────────────────

class TestAtRiskParametrized:
    @pytest.mark.parametrize("pipeline,quota,attainment,expected_risk", [
        (200_000.0, 100_000.0, 90.0, False),   # coverage=2.0, att=90 → safe
        (100_000.0, 100_000.0, 90.0, True),    # coverage=1.0 < 1.5 → risk
        (200_000.0, 100_000.0, 69.0, True),    # att=69 < 70 → risk
        (200_000.0, 100_000.0, 70.0, False),   # att=70 → safe
        (150_000.0, 100_000.0, 90.0, False),   # coverage=1.5, att=90 → safe
        (149_000.0, 100_000.0, 90.0, True),    # coverage=1.49 < 1.5 → risk
        (0.0, 100_000.0, 100.0, True),          # coverage=0 → risk
    ])
    def test_at_risk_combinations(self, engine, pipeline, quota, attainment, expected_risk):
        inp = make_input(pipeline_value=pipeline, quota=quota,
                         last_period_attainment=attainment,
                         submitted_commit=quota * 0.8)
        result = engine.analyze(inp)
        assert result.is_at_risk is expected_risk


# ──────────────────────────────────────────────────────────────────────────────
# Section 30 – Additional summary validation tests
# ──────────────────────────────────────────────────────────────────────────────

class TestSummaryAdditional:
    def test_avg_coverage_rounded_to_2dp(self, engine):
        inputs = [make_input(rep_id=f"R{i}", pipeline_value=100_000.0 * (i + 1),
                             quota=300_000.0) for i in range(3)]
        engine.analyze_batch(inputs)
        val = engine.summary()["avg_coverage_ratio"]
        assert round(val, 2) == val

    def test_single_rep_summary(self, engine, standard_input):
        result = engine.analyze(standard_input)
        s = engine.summary()
        assert s["total"] == 1
        assert s["avg_coverage_ratio"] == result.coverage_ratio
        assert s["avg_pipeline_health"] == result.pipeline_health
        assert s["avg_sandbagging_score"] == result.sandbagging_score

    def test_summary_after_batch_has_correct_totals(self, engine):
        inputs = [
            make_input(rep_id="A", submitted_best_case=120_000.0, submitted_commit=80_000.0),
            make_input(rep_id="B", submitted_best_case=130_000.0, submitted_commit=90_000.0),
        ]
        results = engine.analyze_batch(inputs)
        s = engine.summary()
        assert s["total_upside_potential"] == engine.total_upside_potential

    def test_mixed_bands_in_band_counts(self, engine):
        """Ensure band_counts can hold multiple band types."""
        # Craft two reps with different bands
        # LIKELY band: estimate=floor < commit*0.90
        inp1 = make_input(
            rep_id="LIKELY-REP",
            closed_won_qtd=0.0, late_stage_pipeline=0.0, early_stage_pipeline=0.0,
            nrr_contribution=0.0, submitted_commit=100_000.0,
            submitted_best_case=200_000.0, historical_accuracy_pct=100.0,
            pipeline_value=500_000.0, quota=100_000.0, last_period_attainment=90.0,
        )
        # BEST_CASE band: estimate >= best_case*0.95
        inp2 = make_input(
            rep_id="BEST-REP",
            closed_won_qtd=200_000.0, late_stage_pipeline=0.0, early_stage_pipeline=0.0,
            nrr_contribution=0.0, submitted_commit=100_000.0,
            submitted_best_case=200_000.0, historical_accuracy_pct=100.0,
            pipeline_value=500_000.0, quota=100_000.0, last_period_attainment=90.0,
        )
        engine.analyze_batch([inp1, inp2])
        s = engine.summary()
        # Both bands should appear
        assert len(s["band_counts"]) == 2

    def test_summary_high_reliability_matches_property(self, engine):
        inp_hi = make_input(rep_id="HI", calls_made=5, calls_hit=5,
                            historical_accuracy_pct=80.0)
        inp_lo = make_input(rep_id="LO", calls_made=0, calls_hit=0)
        engine.analyze_batch([inp_hi, inp_lo])
        s = engine.summary()
        assert s["high_reliability_count"] == len(engine.high_reliability_reps)

    def test_summary_keys_are_strings(self, engine, standard_input):
        engine.analyze(standard_input)
        s = engine.summary()
        for key in s:
            assert isinstance(key, str)


# ──────────────────────────────────────────────────────────────────────────────
# Section 31 – Verify call_reliability=UNRELIABLE at boundary 39.9 blended
# ──────────────────────────────────────────────────────────────────────────────

class TestCallReliabilityUnreliableBoundary:
    def test_blended_39_9_is_unreliable(self, engine):
        # blended = call_acc*0.60 + hist*0.40 = 39.9
        # call_acc=0 → blended=hist*0.40; hist=99.75 → 39.9
        inp = make_input(calls_made=5, calls_hit=0, historical_accuracy_pct=99.75)
        result = engine.analyze(inp)
        # blended = 0*0.60 + 99.75*0.40 = 39.9 < 40 → UNRELIABLE
        assert result.call_reliability == CallReliability.UNRELIABLE

    def test_blended_40_is_low(self, engine):
        # blended = 0*0.6 + 100*0.4 = 40.0 → LOW
        inp = make_input(calls_made=5, calls_hit=0, historical_accuracy_pct=100.0)
        result = engine.analyze(inp)
        assert result.call_reliability == CallReliability.LOW


# ──────────────────────────────────────────────────────────────────────────────
# Section 32 – Verify SalesForecastResult is a dataclass
# ──────────────────────────────────────────────────────────────────────────────

class TestSalesForecastResultDataclass:
    def test_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(SalesForecastResult)

    def test_field_count(self):
        import dataclasses
        fields = dataclasses.fields(SalesForecastResult)
        assert len(fields) == 15

    def test_result_attributes_accessible(self, engine, standard_input):
        result = engine.analyze(standard_input)
        # Check all 15 attributes exist
        attrs = [
            "rep_id", "rep_name", "manager_id", "forecast_band",
            "forecast_accuracy", "call_reliability", "forecast_action",
            "adjusted_forecast", "coverage_ratio", "sandbagging_score",
            "pipeline_health", "commit_vs_quota_pct", "upside_potential",
            "is_at_risk", "is_sandbagging",
        ]
        for attr in attrs:
            assert hasattr(result, attr)


# ──────────────────────────────────────────────────────────────────────────────
# Section 33 – Engine initialization
# ──────────────────────────────────────────────────────────────────────────────

class TestEngineInitialization:
    def test_results_empty_at_init(self):
        engine = SalesForecastEngine()
        assert engine._results == []

    def test_multiple_engines_are_independent(self):
        e1 = SalesForecastEngine()
        e2 = SalesForecastEngine()
        e1.analyze(make_input(rep_id="ONLY-IN-E1"))
        assert len(e2._results) == 0

    def test_properties_return_empty_on_fresh_engine(self):
        engine = SalesForecastEngine()
        assert engine.at_risk_reps == []
        assert engine.sandbagging_reps == []
        assert engine.high_reliability_reps == []
        assert engine.total_adjusted_forecast == 0.0
        assert engine.total_upside_potential == 0.0


# ──────────────────────────────────────────────────────────────────────────────
# Section 34 – Consistency checks between summary and properties
# ──────────────────────────────────────────────────────────────────────────────

class TestSummaryPropertyConsistency:
    def test_at_risk_count_equals_property_len(self, engine):
        inputs = [make_input(rep_id=f"R{i}", pipeline_value=50_000.0 * (i % 3),
                             quota=100_000.0, last_period_attainment=90.0)
                  for i in range(6)]
        engine.analyze_batch(inputs)
        assert engine.summary()["at_risk_count"] == len(engine.at_risk_reps)

    def test_sandbagging_count_equals_property_len(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        engine.analyze_batch(inputs)
        assert engine.summary()["sandbagging_count"] == len(engine.sandbagging_reps)

    def test_high_reliability_count_equals_property_len(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        engine.analyze_batch(inputs)
        assert engine.summary()["high_reliability_count"] == len(engine.high_reliability_reps)

    def test_total_adjusted_matches_sum_of_results(self, engine):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = engine.analyze_batch(inputs)
        expected = round(sum(r.adjusted_forecast for r in results), 2)
        assert engine.total_adjusted_forecast == expected

    def test_total_upside_matches_sum_of_results(self, engine):
        inputs = [make_input(rep_id=f"R{i}", submitted_best_case=120_000.0,
                             submitted_commit=80_000.0) for i in range(5)]
        results = engine.analyze_batch(inputs)
        expected = round(sum(r.upside_potential for r in results), 2)
        assert engine.total_upside_potential == expected
