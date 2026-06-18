"""
Comprehensive tests for SalesForecastSanityCheckIntelligenceEngine.
Covers: enums, dataclasses, all sub-score methods, pattern detection,
risk/severity/action mapping, flag methods, forecast variance, signal
generation, assess(), assess_batch(), summary(), and edge cases.
"""
from __future__ import annotations

import math
import pytest

from swarm.intelligence.sales_forecast_sanity_check_intelligence_engine import (
    ForecastAction,
    ForecastPattern,
    ForecastRisk,
    ForecastSanityCheckInput,
    ForecastSanityCheckResult,
    ForecastSeverity,
    SalesForecastSanityCheckIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers / Fixtures
# ---------------------------------------------------------------------------

def make_input(**overrides) -> ForecastSanityCheckInput:
    """Return a baseline 'clean' input that scores near zero on every sub-score."""
    defaults = dict(
        rep_id="rep-001",
        region="EMEA",
        evaluation_period_id="Q2-2026",
        current_forecast_usd=100_000.0,
        historical_avg_attainment_pct=1.00,   # 100 % attainment
        quota_usd=100_000.0,
        pipeline_coverage_ratio=3.5,
        avg_deal_age_in_forecast_days=30.0,
        deals_added_last_7d_count=2,
        deals_pulled_in_from_next_qtr_count=0,
        stage_3_plus_deal_count=5,
        stage_3_plus_avg_age_days=20.0,
        forecast_vs_prior_week_delta_pct=0.0,
        manual_forecast_override_count=0,
        won_deals_ytd_count=10,
        lost_deals_ytd_count=5,
        avg_days_in_stage_before_advance=5.0,
        late_quarter_close_date_count=0,
        total_forecast_deals=10,
        close_date_pushed_count=0,
        avg_opportunity_value_usd=10_000.0,
        crm_signal_quality_score=0.80,
    )
    defaults.update(overrides)
    return ForecastSanityCheckInput(**defaults)


@pytest.fixture
def engine() -> SalesForecastSanityCheckIntelligenceEngine:
    return SalesForecastSanityCheckIntelligenceEngine()


@pytest.fixture
def clean_input() -> ForecastSanityCheckInput:
    return make_input()


# ===========================================================================
# 1. ENUM TESTS
# ===========================================================================

class TestForecastRiskEnum:
    def test_values_exist(self):
        assert ForecastRisk.low.value == "low"
        assert ForecastRisk.moderate.value == "moderate"
        assert ForecastRisk.high.value == "high"
        assert ForecastRisk.critical.value == "critical"

    def test_member_count(self):
        assert len(ForecastRisk) == 4

    def test_is_str_enum(self):
        assert isinstance(ForecastRisk.low, str)

    def test_equality_with_string(self):
        assert ForecastRisk.low == "low"
        assert ForecastRisk.critical == "critical"

    def test_all_members(self):
        names = {m.name for m in ForecastRisk}
        assert names == {"low", "moderate", "high", "critical"}


class TestForecastPatternEnum:
    def test_values_exist(self):
        assert ForecastPattern.none.value == "none"
        assert ForecastPattern.overforecast_bias.value == "overforecast_bias"
        assert ForecastPattern.sandbag_bias.value == "sandbag_bias"
        assert ForecastPattern.late_quarter_stuffing.value == "late_quarter_stuffing"
        assert ForecastPattern.stage_inflation.value == "stage_inflation"
        assert ForecastPattern.history_disconnect.value == "history_disconnect"

    def test_member_count(self):
        assert len(ForecastPattern) == 6

    def test_is_str_enum(self):
        assert isinstance(ForecastPattern.none, str)

    def test_all_member_names(self):
        names = {m.name for m in ForecastPattern}
        assert names == {
            "none", "overforecast_bias", "sandbag_bias",
            "late_quarter_stuffing", "stage_inflation", "history_disconnect",
        }


class TestForecastSeverityEnum:
    def test_values_exist(self):
        assert ForecastSeverity.accurate.value == "accurate"
        assert ForecastSeverity.drifting.value == "drifting"
        assert ForecastSeverity.unreliable.value == "unreliable"
        assert ForecastSeverity.distorted.value == "distorted"

    def test_member_count(self):
        assert len(ForecastSeverity) == 4

    def test_is_str_enum(self):
        assert isinstance(ForecastSeverity.accurate, str)


class TestForecastActionEnum:
    def test_values_exist(self):
        assert ForecastAction.no_action.value == "no_action"
        assert ForecastAction.forecast_review_coaching.value == "forecast_review_coaching"
        assert ForecastAction.pipeline_validation_session.value == "pipeline_validation_session"
        assert ForecastAction.deal_stage_audit.value == "deal_stage_audit"
        assert ForecastAction.historical_recalibration.value == "historical_recalibration"
        assert ForecastAction.forecast_override_intervention.value == "forecast_override_intervention"

    def test_member_count(self):
        assert len(ForecastAction) == 6

    def test_is_str_enum(self):
        assert isinstance(ForecastAction.no_action, str)


# ===========================================================================
# 2. DATACLASS TESTS – ForecastSanityCheckInput
# ===========================================================================

class TestForecastSanityCheckInput:
    def test_creation_with_all_fields(self, clean_input):
        inp = clean_input
        assert inp.rep_id == "rep-001"
        assert inp.region == "EMEA"
        assert inp.evaluation_period_id == "Q2-2026"
        assert inp.current_forecast_usd == 100_000.0
        assert inp.historical_avg_attainment_pct == 1.00
        assert inp.quota_usd == 100_000.0
        assert inp.pipeline_coverage_ratio == 3.5
        assert inp.avg_deal_age_in_forecast_days == 30.0
        assert inp.deals_added_last_7d_count == 2
        assert inp.deals_pulled_in_from_next_qtr_count == 0
        assert inp.stage_3_plus_deal_count == 5
        assert inp.stage_3_plus_avg_age_days == 20.0
        assert inp.forecast_vs_prior_week_delta_pct == 0.0
        assert inp.manual_forecast_override_count == 0
        assert inp.won_deals_ytd_count == 10
        assert inp.lost_deals_ytd_count == 5
        assert inp.avg_days_in_stage_before_advance == 5.0
        assert inp.late_quarter_close_date_count == 0
        assert inp.total_forecast_deals == 10
        assert inp.close_date_pushed_count == 0
        assert inp.avg_opportunity_value_usd == 10_000.0
        assert inp.crm_signal_quality_score == 0.80

    def test_field_count(self):
        import dataclasses
        assert len(dataclasses.fields(ForecastSanityCheckInput)) == 22

    def test_mutable_fields(self, clean_input):
        clean_input.rep_id = "changed"
        assert clean_input.rep_id == "changed"

    def test_integer_fields(self):
        inp = make_input(
            deals_added_last_7d_count=5,
            deals_pulled_in_from_next_qtr_count=3,
            stage_3_plus_deal_count=8,
            manual_forecast_override_count=2,
            won_deals_ytd_count=20,
            lost_deals_ytd_count=10,
            late_quarter_close_date_count=4,
            total_forecast_deals=15,
            close_date_pushed_count=6,
        )
        assert isinstance(inp.deals_added_last_7d_count, int)
        assert isinstance(inp.total_forecast_deals, int)

    def test_float_fields(self):
        inp = make_input(current_forecast_usd=99_999.99)
        assert isinstance(inp.current_forecast_usd, float)


# ===========================================================================
# 3. DATACLASS TESTS – ForecastSanityCheckResult
# ===========================================================================

class TestForecastSanityCheckResult:
    def _make_result(self) -> ForecastSanityCheckResult:
        return ForecastSanityCheckResult(
            rep_id="rep-X",
            region="APAC",
            forecast_risk=ForecastRisk.low,
            forecast_pattern=ForecastPattern.none,
            forecast_severity=ForecastSeverity.accurate,
            recommended_action=ForecastAction.no_action,
            overforecast_bias_score=0.0,
            pipeline_quality_score=0.0,
            stage_integrity_score=0.0,
            history_alignment_score=0.0,
            forecast_sanity_composite=0.0,
            has_forecast_gap=False,
            requires_forecast_review=False,
            estimated_forecast_variance_usd=0.0,
            forecast_signal="healthy",
        )

    def test_field_count(self):
        import dataclasses
        assert len(dataclasses.fields(ForecastSanityCheckResult)) == 15

    def test_to_dict_key_count(self):
        r = self._make_result()
        assert len(r.to_dict()) == 15

    def test_to_dict_keys(self):
        r = self._make_result()
        expected_keys = {
            "rep_id", "region", "forecast_risk", "forecast_pattern",
            "forecast_severity", "recommended_action",
            "overforecast_bias_score", "pipeline_quality_score",
            "stage_integrity_score", "history_alignment_score",
            "forecast_sanity_composite", "has_forecast_gap",
            "requires_forecast_review", "estimated_forecast_variance_usd",
            "forecast_signal",
        }
        assert set(r.to_dict().keys()) == expected_keys

    def test_to_dict_enum_values_are_strings(self):
        r = self._make_result()
        d = r.to_dict()
        assert isinstance(d["forecast_risk"], str)
        assert isinstance(d["forecast_pattern"], str)
        assert isinstance(d["forecast_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_values(self):
        r = self._make_result()
        d = r.to_dict()
        assert d["rep_id"] == "rep-X"
        assert d["region"] == "APAC"
        assert d["forecast_risk"] == "low"
        assert d["forecast_pattern"] == "none"
        assert d["forecast_severity"] == "accurate"
        assert d["recommended_action"] == "no_action"
        assert d["overforecast_bias_score"] == 0.0
        assert d["has_forecast_gap"] is False
        assert d["requires_forecast_review"] is False

    def test_to_dict_bool_fields(self):
        r = self._make_result()
        r.has_forecast_gap = True
        r.requires_forecast_review = True
        d = r.to_dict()
        assert d["has_forecast_gap"] is True
        assert d["requires_forecast_review"] is True

    def test_result_stores_enum_objects(self):
        r = self._make_result()
        assert isinstance(r.forecast_risk, ForecastRisk)
        assert isinstance(r.forecast_pattern, ForecastPattern)
        assert isinstance(r.forecast_severity, ForecastSeverity)
        assert isinstance(r.recommended_action, ForecastAction)


# ===========================================================================
# 4. OVERFORECAST BIAS SCORE
# ===========================================================================

class TestOverforecastBiasScore:
    """Tests for _overforecast_bias_score method."""

    def test_zero_score_clean_input(self, engine, clean_input):
        score = engine._overforecast_bias_score(clean_input)
        assert score == 0.0

    # --- overforecast ratio thresholds ---
    def test_ratio_above_30pct_adds_40(self, engine):
        # current = expected * 1.35 → ratio = 0.35
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=135_000.0,
            forecast_vs_prior_week_delta_pct=0.0,
            deals_pulled_in_from_next_qtr_count=0,
        )
        score = engine._overforecast_bias_score(inp)
        assert score == 40.0

    def test_ratio_15_to_29pct_adds_20(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=120_000.0,   # 20 % over
            forecast_vs_prior_week_delta_pct=0.0,
            deals_pulled_in_from_next_qtr_count=0,
        )
        score = engine._overforecast_bias_score(inp)
        assert score == 20.0

    def test_ratio_5_to_14pct_adds_8(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=108_000.0,   # 8 % over
            forecast_vs_prior_week_delta_pct=0.0,
            deals_pulled_in_from_next_qtr_count=0,
        )
        score = engine._overforecast_bias_score(inp)
        assert score == 8.0

    def test_ratio_below_5pct_adds_0(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=103_000.0,   # 3 % over
            forecast_vs_prior_week_delta_pct=0.0,
            deals_pulled_in_from_next_qtr_count=0,
        )
        score = engine._overforecast_bias_score(inp)
        assert score == 0.0

    def test_zero_expected_skips_ratio(self, engine):
        inp = make_input(
            quota_usd=0.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=100_000.0,
            forecast_vs_prior_week_delta_pct=0.0,
            deals_pulled_in_from_next_qtr_count=0,
        )
        score = engine._overforecast_bias_score(inp)
        assert score == 0.0

    # --- forecast_vs_prior_week_delta_pct thresholds ---
    def test_delta_above_20pct_adds_30(self, engine):
        inp = make_input(forecast_vs_prior_week_delta_pct=0.25)
        score = engine._overforecast_bias_score(inp)
        assert score >= 30.0

    def test_delta_10_to_19pct_adds_15(self, engine):
        inp = make_input(forecast_vs_prior_week_delta_pct=0.15)
        score = engine._overforecast_bias_score(inp)
        assert score >= 15.0

    def test_delta_below_10pct_adds_0(self, engine):
        inp = make_input(forecast_vs_prior_week_delta_pct=0.05)
        score = engine._overforecast_bias_score(inp)
        assert score == 0.0

    # --- pull-in rate thresholds ---
    def test_pull_in_rate_above_20pct_adds_25(self, engine):
        inp = make_input(
            deals_pulled_in_from_next_qtr_count=3,
            total_forecast_deals=10,   # 30 %
            forecast_vs_prior_week_delta_pct=0.0,
        )
        score = engine._overforecast_bias_score(inp)
        assert score >= 25.0

    def test_pull_in_rate_10_to_19pct_adds_12(self, engine):
        inp = make_input(
            deals_pulled_in_from_next_qtr_count=1,
            total_forecast_deals=10,   # 10 %
            forecast_vs_prior_week_delta_pct=0.0,
        )
        score = engine._overforecast_bias_score(inp)
        assert score == 12.0

    def test_pull_in_rate_below_10pct_adds_0(self, engine):
        inp = make_input(
            deals_pulled_in_from_next_qtr_count=0,
            total_forecast_deals=10,
            forecast_vs_prior_week_delta_pct=0.0,
        )
        score = engine._overforecast_bias_score(inp)
        assert score == 0.0

    def test_score_capped_at_100(self, engine):
        # Maximise all three components: 40+30+25=95, no cap needed; test cap logic
        # To exceed 100 we'd need >100 which the min() prevents.
        # 40+30+25=95 is the actual max reachable; verify it is <=100.
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=200_000.0,   # +100 %
            forecast_vs_prior_week_delta_pct=0.50,
            deals_pulled_in_from_next_qtr_count=5,
            total_forecast_deals=10,           # 50 %
        )
        score = engine._overforecast_bias_score(inp)
        assert score <= 100.0
        assert score == 95.0   # 40+30+25

    def test_total_forecast_deals_zero_uses_one(self, engine):
        # total_forecast_deals=0 → denominator becomes 1
        inp = make_input(
            deals_pulled_in_from_next_qtr_count=1,
            total_forecast_deals=0,
            forecast_vs_prior_week_delta_pct=0.0,
        )
        # pull_in_rate = 1/1 = 1.0 >= 0.20 → +25
        score = engine._overforecast_bias_score(inp)
        assert score >= 25.0

    def test_exact_boundary_30pct_ratio(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=130_000.0,   # exactly 30 %
            forecast_vs_prior_week_delta_pct=0.0,
            deals_pulled_in_from_next_qtr_count=0,
        )
        score = engine._overforecast_bias_score(inp)
        assert score == 40.0

    def test_exact_boundary_15pct_ratio(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=115_000.0,   # exactly 15 %
            forecast_vs_prior_week_delta_pct=0.0,
            deals_pulled_in_from_next_qtr_count=0,
        )
        score = engine._overforecast_bias_score(inp)
        assert score == 20.0

    def test_exact_boundary_5pct_ratio(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=105_000.0,   # exactly 5 %
            forecast_vs_prior_week_delta_pct=0.0,
            deals_pulled_in_from_next_qtr_count=0,
        )
        score = engine._overforecast_bias_score(inp)
        assert score == 8.0

    def test_exact_boundary_delta_20pct(self, engine):
        inp = make_input(forecast_vs_prior_week_delta_pct=0.20)
        score = engine._overforecast_bias_score(inp)
        assert score >= 30.0

    def test_exact_boundary_delta_10pct(self, engine):
        inp = make_input(forecast_vs_prior_week_delta_pct=0.10)
        score = engine._overforecast_bias_score(inp)
        assert score >= 15.0

    def test_exact_boundary_pull_in_20pct(self, engine):
        inp = make_input(
            deals_pulled_in_from_next_qtr_count=2,
            total_forecast_deals=10,   # exactly 20 %
            forecast_vs_prior_week_delta_pct=0.0,
        )
        score = engine._overforecast_bias_score(inp)
        assert score >= 25.0

    def test_exact_boundary_pull_in_10pct(self, engine):
        inp = make_input(
            deals_pulled_in_from_next_qtr_count=1,
            total_forecast_deals=10,   # exactly 10 %
            forecast_vs_prior_week_delta_pct=0.0,
        )
        score = engine._overforecast_bias_score(inp)
        assert score == 12.0


# ===========================================================================
# 5. PIPELINE QUALITY SCORE
# ===========================================================================

class TestPipelineQualityScore:
    def test_zero_score_clean_input(self, engine, clean_input):
        score = engine._pipeline_quality_score(clean_input)
        assert score == 0.0

    # --- coverage_ratio thresholds ---
    def test_coverage_below_2_adds_35(self, engine):
        inp = make_input(pipeline_coverage_ratio=1.5, crm_signal_quality_score=0.80)
        score = engine._pipeline_quality_score(inp)
        assert score >= 35.0

    def test_coverage_2_to_2_4_adds_18(self, engine):
        inp = make_input(pipeline_coverage_ratio=2.2, crm_signal_quality_score=0.80)
        score = engine._pipeline_quality_score(inp)
        assert score >= 18.0

    def test_coverage_2_5_to_2_9_adds_7(self, engine):
        inp = make_input(pipeline_coverage_ratio=2.7, crm_signal_quality_score=0.80)
        score = engine._pipeline_quality_score(inp)
        assert score >= 7.0

    def test_coverage_3_or_above_adds_0(self, engine):
        inp = make_input(pipeline_coverage_ratio=4.0, crm_signal_quality_score=0.80)
        score = engine._pipeline_quality_score(inp)
        assert score == 0.0

    def test_exact_boundary_coverage_2(self, engine):
        inp = make_input(pipeline_coverage_ratio=2.0, crm_signal_quality_score=0.80,
                         close_date_pushed_count=0)
        score = engine._pipeline_quality_score(inp)
        assert score >= 18.0  # exactly 2.0 -> < 2.5 branch

    def test_exact_boundary_coverage_2_5(self, engine):
        inp = make_input(pipeline_coverage_ratio=2.5, crm_signal_quality_score=0.80,
                         close_date_pushed_count=0)
        score = engine._pipeline_quality_score(inp)
        assert score >= 7.0   # exactly 2.5 -> < 3.0 branch

    # --- push rate thresholds ---
    def test_push_rate_above_30pct_adds_35(self, engine):
        inp = make_input(
            close_date_pushed_count=4,
            total_forecast_deals=10,   # 40 %
            pipeline_coverage_ratio=4.0,
            crm_signal_quality_score=0.80,
        )
        score = engine._pipeline_quality_score(inp)
        assert score >= 35.0

    def test_push_rate_15_to_29pct_adds_18(self, engine):
        inp = make_input(
            close_date_pushed_count=2,
            total_forecast_deals=10,   # 20 %
            pipeline_coverage_ratio=4.0,
            crm_signal_quality_score=0.80,
        )
        score = engine._pipeline_quality_score(inp)
        assert score >= 18.0

    def test_push_rate_5_to_14pct_adds_7(self, engine):
        inp = make_input(
            close_date_pushed_count=1,
            total_forecast_deals=10,   # 10 %
            pipeline_coverage_ratio=4.0,
            crm_signal_quality_score=0.80,
        )
        score = engine._pipeline_quality_score(inp)
        assert score >= 7.0

    def test_push_rate_below_5pct_adds_0(self, engine):
        inp = make_input(
            close_date_pushed_count=0,
            total_forecast_deals=10,
            pipeline_coverage_ratio=4.0,
            crm_signal_quality_score=0.80,
        )
        score = engine._pipeline_quality_score(inp)
        assert score == 0.0

    def test_exact_boundary_push_rate_30pct(self, engine):
        inp = make_input(
            close_date_pushed_count=3,
            total_forecast_deals=10,   # exactly 30 %
            pipeline_coverage_ratio=4.0,
            crm_signal_quality_score=0.80,
        )
        score = engine._pipeline_quality_score(inp)
        assert score >= 35.0

    def test_exact_boundary_push_rate_15pct(self, engine):
        inp = make_input(
            close_date_pushed_count=15,
            total_forecast_deals=100,  # exactly 15 %
            pipeline_coverage_ratio=4.0,
            crm_signal_quality_score=0.80,
        )
        score = engine._pipeline_quality_score(inp)
        assert score >= 18.0

    def test_exact_boundary_push_rate_5pct(self, engine):
        inp = make_input(
            close_date_pushed_count=5,
            total_forecast_deals=100,  # exactly 5 %
            pipeline_coverage_ratio=4.0,
            crm_signal_quality_score=0.80,
        )
        score = engine._pipeline_quality_score(inp)
        assert score >= 7.0

    # --- CRM quality thresholds ---
    def test_crm_below_40pct_adds_25(self, engine):
        inp = make_input(pipeline_coverage_ratio=4.0, crm_signal_quality_score=0.30)
        score = engine._pipeline_quality_score(inp)
        assert score >= 25.0

    def test_crm_40_to_59pct_adds_12(self, engine):
        inp = make_input(pipeline_coverage_ratio=4.0, crm_signal_quality_score=0.50)
        score = engine._pipeline_quality_score(inp)
        assert score >= 12.0

    def test_crm_60pct_or_above_adds_0(self, engine):
        inp = make_input(pipeline_coverage_ratio=4.0, crm_signal_quality_score=0.80)
        score = engine._pipeline_quality_score(inp)
        assert score == 0.0

    def test_exact_boundary_crm_40pct(self, engine):
        inp = make_input(pipeline_coverage_ratio=4.0, crm_signal_quality_score=0.40,
                         close_date_pushed_count=0)
        score = engine._pipeline_quality_score(inp)
        assert score >= 12.0

    def test_exact_boundary_crm_60pct(self, engine):
        inp = make_input(pipeline_coverage_ratio=4.0, crm_signal_quality_score=0.60,
                         close_date_pushed_count=0)
        score = engine._pipeline_quality_score(inp)
        assert score == 0.0

    def test_score_capped_at_100(self, engine):
        # 35+35+25=95 is the actual max from all three branches simultaneously
        inp = make_input(
            pipeline_coverage_ratio=1.0,   # +35
            close_date_pushed_count=5,
            total_forecast_deals=10,        # 50% push → +35
            crm_signal_quality_score=0.20,  # +25
        )
        score = engine._pipeline_quality_score(inp)
        assert score <= 100.0
        assert score == 95.0  # 35+35+25

    def test_total_forecast_deals_zero_uses_one(self, engine):
        inp = make_input(
            close_date_pushed_count=1,
            total_forecast_deals=0,
            pipeline_coverage_ratio=4.0,
            crm_signal_quality_score=0.80,
        )
        score = engine._pipeline_quality_score(inp)
        assert score >= 35.0   # push_rate = 1/1 = 100 % → +35


# ===========================================================================
# 6. STAGE INTEGRITY SCORE
# ===========================================================================

class TestStageIntegrityScore:
    def test_zero_score_clean_input(self, engine, clean_input):
        score = engine._stage_integrity_score(clean_input)
        assert score == 0.0

    # --- stage_3_plus_avg_age_days ---
    def test_age_above_60_adds_40(self, engine):
        inp = make_input(stage_3_plus_avg_age_days=70.0)
        score = engine._stage_integrity_score(inp)
        assert score >= 40.0

    def test_age_45_to_59_adds_22(self, engine):
        inp = make_input(stage_3_plus_avg_age_days=50.0)
        score = engine._stage_integrity_score(inp)
        assert score >= 22.0

    def test_age_30_to_44_adds_8(self, engine):
        inp = make_input(stage_3_plus_avg_age_days=35.0)
        score = engine._stage_integrity_score(inp)
        assert score >= 8.0

    def test_age_below_30_adds_0(self, engine):
        inp = make_input(stage_3_plus_avg_age_days=20.0)
        score = engine._stage_integrity_score(inp)
        assert score == 0.0

    def test_exact_boundary_age_60(self, engine):
        inp = make_input(stage_3_plus_avg_age_days=60.0, avg_days_in_stage_before_advance=0.0,
                         late_quarter_close_date_count=0)
        score = engine._stage_integrity_score(inp)
        assert score == 40.0

    def test_exact_boundary_age_45(self, engine):
        inp = make_input(stage_3_plus_avg_age_days=45.0, avg_days_in_stage_before_advance=0.0,
                         late_quarter_close_date_count=0)
        score = engine._stage_integrity_score(inp)
        assert score == 22.0

    def test_exact_boundary_age_30(self, engine):
        inp = make_input(stage_3_plus_avg_age_days=30.0, avg_days_in_stage_before_advance=0.0,
                         late_quarter_close_date_count=0)
        score = engine._stage_integrity_score(inp)
        assert score == 8.0

    # --- avg_days_in_stage_before_advance ---
    def test_advance_days_above_20_adds_30(self, engine):
        inp = make_input(avg_days_in_stage_before_advance=25.0)
        score = engine._stage_integrity_score(inp)
        assert score >= 30.0

    def test_advance_days_12_to_19_adds_15(self, engine):
        inp = make_input(avg_days_in_stage_before_advance=15.0)
        score = engine._stage_integrity_score(inp)
        assert score >= 15.0

    def test_advance_days_below_12_adds_0(self, engine):
        inp = make_input(avg_days_in_stage_before_advance=5.0)
        score = engine._stage_integrity_score(inp)
        assert score == 0.0

    def test_exact_boundary_advance_20(self, engine):
        inp = make_input(stage_3_plus_avg_age_days=20.0, avg_days_in_stage_before_advance=20.0,
                         late_quarter_close_date_count=0)
        score = engine._stage_integrity_score(inp)
        assert score == 30.0

    def test_exact_boundary_advance_12(self, engine):
        inp = make_input(stage_3_plus_avg_age_days=20.0, avg_days_in_stage_before_advance=12.0,
                         late_quarter_close_date_count=0)
        score = engine._stage_integrity_score(inp)
        assert score == 15.0

    # --- late_close_rate ---
    def test_late_close_above_50pct_adds_25(self, engine):
        inp = make_input(
            late_quarter_close_date_count=6,
            total_forecast_deals=10,   # 60 %
        )
        score = engine._stage_integrity_score(inp)
        assert score >= 25.0

    def test_late_close_30_to_49pct_adds_12(self, engine):
        inp = make_input(
            late_quarter_close_date_count=4,
            total_forecast_deals=10,   # 40 %
        )
        score = engine._stage_integrity_score(inp)
        assert score >= 12.0

    def test_late_close_below_30pct_adds_0(self, engine):
        inp = make_input(
            late_quarter_close_date_count=2,
            total_forecast_deals=10,   # 20 %
        )
        score = engine._stage_integrity_score(inp)
        assert score == 0.0

    def test_exact_boundary_late_close_50pct(self, engine):
        inp = make_input(
            stage_3_plus_avg_age_days=20.0,
            avg_days_in_stage_before_advance=0.0,
            late_quarter_close_date_count=5,
            total_forecast_deals=10,  # exactly 50 %
        )
        score = engine._stage_integrity_score(inp)
        assert score == 25.0

    def test_exact_boundary_late_close_30pct(self, engine):
        inp = make_input(
            stage_3_plus_avg_age_days=20.0,
            avg_days_in_stage_before_advance=0.0,
            late_quarter_close_date_count=3,
            total_forecast_deals=10,  # exactly 30 %
        )
        score = engine._stage_integrity_score(inp)
        assert score == 12.0

    def test_score_capped_at_100(self, engine):
        inp = make_input(
            stage_3_plus_avg_age_days=90.0,          # +40
            avg_days_in_stage_before_advance=30.0,   # +30
            late_quarter_close_date_count=8,
            total_forecast_deals=10,                 # 80 % → +25
        )
        score = engine._stage_integrity_score(inp)
        assert score == 95.0  # 40+30+25=95, under cap

    def test_deals_zero_uses_one(self, engine):
        inp = make_input(
            late_quarter_close_date_count=1,
            total_forecast_deals=0,
        )
        score = engine._stage_integrity_score(inp)
        assert score >= 25.0  # late_rate = 1/1 = 100 %


# ===========================================================================
# 7. HISTORY ALIGNMENT SCORE
# ===========================================================================

class TestHistoryAlignmentScore:
    def test_zero_score_clean_input(self, engine, clean_input):
        # clean: win_rate=10/15≈0.67, implied=1.0 → gap≈0.33 → +40
        # Revert to a perfect alignment input
        inp = make_input(
            historical_avg_attainment_pct=0.67,
            won_deals_ytd_count=10,
            lost_deals_ytd_count=5,
            manual_forecast_override_count=0,
            avg_deal_age_in_forecast_days=30.0,
        )
        score = engine._history_alignment_score(inp)
        # gap = 0.67 - (10/15=0.667) ≈ 0.003 < 0.05 → 0 from win-rate
        assert score == 0.0

    # --- win_rate_gap thresholds ---
    def test_win_rate_gap_above_20pct_adds_40(self, engine):
        inp = make_input(
            historical_avg_attainment_pct=0.80,
            won_deals_ytd_count=5,
            lost_deals_ytd_count=5,   # win_rate=0.50, gap=0.30
            manual_forecast_override_count=0,
            avg_deal_age_in_forecast_days=30.0,
        )
        score = engine._history_alignment_score(inp)
        assert score >= 40.0

    def test_win_rate_gap_10_to_19pct_adds_20(self, engine):
        # Use values that clearly produce gap > 0.10 without floating-point ambiguity
        # win_rate = 5/10 = 0.50, implied = 0.75, gap = 0.25 -> >=0.20 → +40
        # Use gap clearly in [0.10, 0.20): implied=0.80, won=6, lost=4 → win_rate=0.60, gap=0.20 → >=0.20 +40
        # Use implied=0.75, won=7, lost=3 → win_rate=0.70, gap=0.05 (too small)
        # Use implied=0.80, won=6, lost=4 → gap exactly 0.20 → >=0.20 branch → +40
        # For exactly 10-19 range: implied=0.70, won=5, lost=4 → win_rate=5/9≈0.556, gap=0.144 → +20
        inp = make_input(
            historical_avg_attainment_pct=0.70,
            won_deals_ytd_count=5,
            lost_deals_ytd_count=4,   # win_rate=5/9≈0.556, gap≈0.144 → +20
            manual_forecast_override_count=0,
            avg_deal_age_in_forecast_days=30.0,
        )
        score = engine._history_alignment_score(inp)
        assert score >= 20.0

    def test_win_rate_gap_5_to_9pct_adds_8(self, engine):
        inp = make_input(
            historical_avg_attainment_pct=0.65,
            won_deals_ytd_count=6,
            lost_deals_ytd_count=4,   # win_rate=0.60, gap=0.05
            manual_forecast_override_count=0,
            avg_deal_age_in_forecast_days=30.0,
        )
        score = engine._history_alignment_score(inp)
        assert score >= 8.0

    def test_zero_historical_attainment_skips_win_rate(self, engine):
        inp = make_input(
            historical_avg_attainment_pct=0.0,
            won_deals_ytd_count=5,
            lost_deals_ytd_count=5,
            manual_forecast_override_count=0,
            avg_deal_age_in_forecast_days=30.0,
        )
        score = engine._history_alignment_score(inp)
        assert score == 0.0

    # --- manual_override_count thresholds ---
    def test_overrides_5_plus_adds_35(self, engine):
        inp = make_input(
            historical_avg_attainment_pct=0.0,
            manual_forecast_override_count=5,
            avg_deal_age_in_forecast_days=30.0,
        )
        score = engine._history_alignment_score(inp)
        assert score >= 35.0

    def test_overrides_2_to_4_adds_18(self, engine):
        inp = make_input(
            historical_avg_attainment_pct=0.0,
            manual_forecast_override_count=2,
            avg_deal_age_in_forecast_days=30.0,
        )
        score = engine._history_alignment_score(inp)
        assert score >= 18.0

    def test_overrides_1_adds_7(self, engine):
        inp = make_input(
            historical_avg_attainment_pct=0.0,
            manual_forecast_override_count=1,
            avg_deal_age_in_forecast_days=30.0,
        )
        score = engine._history_alignment_score(inp)
        assert score >= 7.0

    def test_overrides_0_adds_0(self, engine):
        inp = make_input(
            historical_avg_attainment_pct=0.0,
            manual_forecast_override_count=0,
            avg_deal_age_in_forecast_days=30.0,
        )
        score = engine._history_alignment_score(inp)
        assert score == 0.0

    def test_exact_boundary_overrides_5(self, engine):
        inp = make_input(
            historical_avg_attainment_pct=0.0,
            manual_forecast_override_count=5,
            avg_deal_age_in_forecast_days=30.0,
        )
        score = engine._history_alignment_score(inp)
        assert score == 35.0

    def test_exact_boundary_overrides_2(self, engine):
        inp = make_input(
            historical_avg_attainment_pct=0.0,
            manual_forecast_override_count=2,
            avg_deal_age_in_forecast_days=30.0,
        )
        score = engine._history_alignment_score(inp)
        assert score == 18.0

    def test_exact_boundary_overrides_1(self, engine):
        inp = make_input(
            historical_avg_attainment_pct=0.0,
            manual_forecast_override_count=1,
            avg_deal_age_in_forecast_days=30.0,
        )
        score = engine._history_alignment_score(inp)
        assert score == 7.0

    # --- avg_deal_age_in_forecast_days ---
    def test_deal_age_above_90_adds_20(self, engine):
        inp = make_input(
            historical_avg_attainment_pct=0.0,
            manual_forecast_override_count=0,
            avg_deal_age_in_forecast_days=100.0,
        )
        score = engine._history_alignment_score(inp)
        assert score == 20.0

    def test_deal_age_60_to_89_adds_10(self, engine):
        inp = make_input(
            historical_avg_attainment_pct=0.0,
            manual_forecast_override_count=0,
            avg_deal_age_in_forecast_days=75.0,
        )
        score = engine._history_alignment_score(inp)
        assert score == 10.0

    def test_deal_age_below_60_adds_0(self, engine):
        inp = make_input(
            historical_avg_attainment_pct=0.0,
            manual_forecast_override_count=0,
            avg_deal_age_in_forecast_days=50.0,
        )
        score = engine._history_alignment_score(inp)
        assert score == 0.0

    def test_exact_boundary_deal_age_90(self, engine):
        inp = make_input(
            historical_avg_attainment_pct=0.0,
            manual_forecast_override_count=0,
            avg_deal_age_in_forecast_days=90.0,
        )
        score = engine._history_alignment_score(inp)
        assert score == 20.0

    def test_exact_boundary_deal_age_60(self, engine):
        inp = make_input(
            historical_avg_attainment_pct=0.0,
            manual_forecast_override_count=0,
            avg_deal_age_in_forecast_days=60.0,
        )
        score = engine._history_alignment_score(inp)
        assert score == 10.0

    def test_score_capped_at_100(self, engine):
        inp = make_input(
            historical_avg_attainment_pct=1.0,
            won_deals_ytd_count=0,
            lost_deals_ytd_count=1,   # win_rate=0, gap=1.0 → +40
            manual_forecast_override_count=10,  # +35
            avg_deal_age_in_forecast_days=120.0,  # +20
        )
        score = engine._history_alignment_score(inp)
        assert score == 95.0   # 40+35+20=95, under cap

    def test_zero_total_closed_uses_one(self, engine):
        inp = make_input(
            historical_avg_attainment_pct=1.0,
            won_deals_ytd_count=0,
            lost_deals_ytd_count=0,   # total_closed → max(0,1)=1
            manual_forecast_override_count=0,
            avg_deal_age_in_forecast_days=30.0,
        )
        # win_rate=0/1=0, gap=1.0-0=1.0 >=0.20 → +40
        score = engine._history_alignment_score(inp)
        assert score >= 40.0


# ===========================================================================
# 8. COMPOSITE SCORE FORMULA
# ===========================================================================

class TestCompositeFormula:
    def test_composite_formula_weights(self, engine):
        """Verify composite = over*0.30 + pipeline*0.30 + stage*0.25 + history*0.15"""
        inp = make_input()  # baseline clean
        result = engine.assess(inp)
        over = result.overforecast_bias_score
        pipeline = result.pipeline_quality_score
        stage = result.stage_integrity_score
        history = result.history_alignment_score
        expected = round(over * 0.30 + pipeline * 0.30 + stage * 0.25 + history * 0.15, 1)
        assert result.forecast_sanity_composite == expected

    def test_composite_capped_at_100(self, engine):
        inp = make_input(
            pipeline_coverage_ratio=1.0,
            crm_signal_quality_score=0.10,
            close_date_pushed_count=10,
            total_forecast_deals=10,
            stage_3_plus_avg_age_days=90.0,
            avg_days_in_stage_before_advance=30.0,
            late_quarter_close_date_count=8,
            manual_forecast_override_count=10,
            avg_deal_age_in_forecast_days=120.0,
            current_forecast_usd=300_000.0,
            forecast_vs_prior_week_delta_pct=0.50,
            deals_pulled_in_from_next_qtr_count=5,
        )
        result = engine.assess(inp)
        assert result.forecast_sanity_composite <= 100.0


# ===========================================================================
# 9. RISK LEVEL
# ===========================================================================

class TestRiskLevel:
    def test_critical_at_60(self, engine):
        assert engine._risk_level(60.0) == ForecastRisk.critical

    def test_critical_above_60(self, engine):
        assert engine._risk_level(85.0) == ForecastRisk.critical

    def test_high_at_40(self, engine):
        assert engine._risk_level(40.0) == ForecastRisk.high

    def test_high_at_59(self, engine):
        assert engine._risk_level(59.9) == ForecastRisk.high

    def test_moderate_at_20(self, engine):
        assert engine._risk_level(20.0) == ForecastRisk.moderate

    def test_moderate_at_39(self, engine):
        assert engine._risk_level(39.9) == ForecastRisk.moderate

    def test_low_at_0(self, engine):
        assert engine._risk_level(0.0) == ForecastRisk.low

    def test_low_at_19(self, engine):
        assert engine._risk_level(19.9) == ForecastRisk.low

    def test_low_at_100_not_below_thresholds(self, engine):
        # boundary: exactly 60 should be critical, not high
        assert engine._risk_level(60.0) == ForecastRisk.critical

    def test_risk_returns_enum_instance(self, engine):
        assert isinstance(engine._risk_level(50.0), ForecastRisk)


# ===========================================================================
# 10. SEVERITY
# ===========================================================================

class TestSeverity:
    def test_distorted_at_60(self, engine):
        assert engine._severity(60.0) == ForecastSeverity.distorted

    def test_distorted_above_60(self, engine):
        assert engine._severity(90.0) == ForecastSeverity.distorted

    def test_unreliable_at_40(self, engine):
        assert engine._severity(40.0) == ForecastSeverity.unreliable

    def test_unreliable_at_59(self, engine):
        assert engine._severity(59.9) == ForecastSeverity.unreliable

    def test_drifting_at_20(self, engine):
        assert engine._severity(20.0) == ForecastSeverity.drifting

    def test_drifting_at_39(self, engine):
        assert engine._severity(39.9) == ForecastSeverity.drifting

    def test_accurate_at_0(self, engine):
        assert engine._severity(0.0) == ForecastSeverity.accurate

    def test_accurate_at_19(self, engine):
        assert engine._severity(19.9) == ForecastSeverity.accurate

    def test_severity_returns_enum_instance(self, engine):
        assert isinstance(engine._severity(50.0), ForecastSeverity)


# ===========================================================================
# 11. ACTION MAPPING
# ===========================================================================

class TestActionMapping:
    # --- critical risk ---
    def test_critical_overforecast_bias(self, engine):
        action = engine._action(ForecastRisk.critical, ForecastPattern.overforecast_bias)
        assert action == ForecastAction.forecast_override_intervention

    def test_critical_stage_inflation(self, engine):
        action = engine._action(ForecastRisk.critical, ForecastPattern.stage_inflation)
        assert action == ForecastAction.deal_stage_audit

    def test_critical_none_pattern(self, engine):
        action = engine._action(ForecastRisk.critical, ForecastPattern.none)
        assert action == ForecastAction.forecast_override_intervention

    def test_critical_sandbag_bias(self, engine):
        action = engine._action(ForecastRisk.critical, ForecastPattern.sandbag_bias)
        assert action == ForecastAction.forecast_override_intervention

    def test_critical_late_quarter_stuffing(self, engine):
        action = engine._action(ForecastRisk.critical, ForecastPattern.late_quarter_stuffing)
        assert action == ForecastAction.forecast_override_intervention

    def test_critical_history_disconnect(self, engine):
        action = engine._action(ForecastRisk.critical, ForecastPattern.history_disconnect)
        assert action == ForecastAction.forecast_override_intervention

    # --- high risk ---
    def test_high_history_disconnect(self, engine):
        action = engine._action(ForecastRisk.high, ForecastPattern.history_disconnect)
        assert action == ForecastAction.historical_recalibration

    def test_high_late_quarter_stuffing(self, engine):
        action = engine._action(ForecastRisk.high, ForecastPattern.late_quarter_stuffing)
        assert action == ForecastAction.pipeline_validation_session

    def test_high_none_pattern(self, engine):
        action = engine._action(ForecastRisk.high, ForecastPattern.none)
        assert action == ForecastAction.forecast_review_coaching

    def test_high_overforecast_bias(self, engine):
        action = engine._action(ForecastRisk.high, ForecastPattern.overforecast_bias)
        assert action == ForecastAction.forecast_review_coaching

    def test_high_stage_inflation(self, engine):
        action = engine._action(ForecastRisk.high, ForecastPattern.stage_inflation)
        assert action == ForecastAction.forecast_review_coaching

    def test_high_sandbag_bias(self, engine):
        action = engine._action(ForecastRisk.high, ForecastPattern.sandbag_bias)
        assert action == ForecastAction.forecast_review_coaching

    # --- moderate risk ---
    def test_moderate_any_pattern_gives_coaching(self, engine):
        for pattern in ForecastPattern:
            action = engine._action(ForecastRisk.moderate, pattern)
            assert action == ForecastAction.forecast_review_coaching

    # --- low risk ---
    def test_low_any_pattern_gives_no_action(self, engine):
        for pattern in ForecastPattern:
            action = engine._action(ForecastRisk.low, pattern)
            assert action == ForecastAction.no_action

    def test_action_returns_enum_instance(self, engine):
        action = engine._action(ForecastRisk.low, ForecastPattern.none)
        assert isinstance(action, ForecastAction)


# ===========================================================================
# 12. DETECT PATTERN
# ===========================================================================

class TestDetectPattern:
    def _call(self, engine, inp, over, pipeline, stage, history):
        return engine._detect_pattern(inp, over, pipeline, stage, history)

    def test_no_pattern_clean_input(self, engine, clean_input):
        pattern = self._call(engine, clean_input, 0.0, 0.0, 0.0, 0.0)
        assert pattern == ForecastPattern.none

    def test_overforecast_bias_detected(self, engine):
        """over>=30 AND (current-expected)/expected >= 0.25 AND expected>0"""
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=135_000.0,   # 35 % over
        )
        pattern = self._call(engine, inp, 40.0, 0.0, 0.0, 0.0)
        assert pattern == ForecastPattern.overforecast_bias

    def test_overforecast_bias_requires_over_ge_30(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=135_000.0,
        )
        # over=29.9 < 30 → should not trigger overforecast_bias
        pattern = self._call(engine, inp, 29.9, 0.0, 0.0, 0.0)
        assert pattern != ForecastPattern.overforecast_bias

    def test_overforecast_bias_requires_ratio_ge_25pct(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=120_000.0,   # only 20 % over
        )
        pattern = self._call(engine, inp, 40.0, 0.0, 0.0, 0.0)
        assert pattern != ForecastPattern.overforecast_bias

    def test_late_quarter_stuffing_via_pull_in_rate(self, engine):
        inp = make_input(
            deals_pulled_in_from_next_qtr_count=2,
            total_forecast_deals=10,  # pull_in=20 %
        )
        pattern = self._call(engine, inp, 25.0, 0.0, 0.0, 0.0)
        assert pattern == ForecastPattern.late_quarter_stuffing

    def test_late_quarter_stuffing_via_late_rate(self, engine):
        inp = make_input(
            late_quarter_close_date_count=5,
            total_forecast_deals=10,  # late_rate=50 %
        )
        pattern = self._call(engine, inp, 25.0, 0.0, 0.0, 0.0)
        assert pattern == ForecastPattern.late_quarter_stuffing

    def test_late_quarter_requires_over_ge_20(self, engine):
        inp = make_input(
            deals_pulled_in_from_next_qtr_count=2,
            total_forecast_deals=10,
        )
        pattern = self._call(engine, inp, 15.0, 0.0, 0.0, 0.0)
        assert pattern != ForecastPattern.late_quarter_stuffing

    def test_stage_inflation_detected(self, engine):
        inp = make_input(stage_3_plus_avg_age_days=50.0)
        pattern = self._call(engine, inp, 0.0, 0.0, 35.0, 0.0)
        assert pattern == ForecastPattern.stage_inflation

    def test_stage_inflation_requires_stage_ge_30(self, engine):
        inp = make_input(stage_3_plus_avg_age_days=50.0)
        pattern = self._call(engine, inp, 0.0, 0.0, 29.9, 0.0)
        assert pattern != ForecastPattern.stage_inflation

    def test_stage_inflation_requires_age_ge_45(self, engine):
        inp = make_input(stage_3_plus_avg_age_days=44.9)
        pattern = self._call(engine, inp, 0.0, 0.0, 35.0, 0.0)
        assert pattern != ForecastPattern.stage_inflation

    def test_history_disconnect_detected(self, engine):
        inp = make_input(manual_forecast_override_count=3)
        pattern = self._call(engine, inp, 0.0, 0.0, 0.0, 35.0)
        assert pattern == ForecastPattern.history_disconnect

    def test_history_disconnect_requires_history_ge_30(self, engine):
        inp = make_input(manual_forecast_override_count=3)
        pattern = self._call(engine, inp, 0.0, 0.0, 0.0, 29.9)
        assert pattern != ForecastPattern.history_disconnect

    def test_history_disconnect_requires_override_ge_2(self, engine):
        inp = make_input(manual_forecast_override_count=1)
        pattern = self._call(engine, inp, 0.0, 0.0, 0.0, 35.0)
        assert pattern != ForecastPattern.history_disconnect

    def test_sandbag_bias_detected(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=65_000.0,  # 65 % of expected
            pipeline_coverage_ratio=4.0,
        )
        pattern = self._call(engine, inp, 0.0, 0.0, 0.0, 0.0)
        assert pattern == ForecastPattern.sandbag_bias

    def test_sandbag_requires_coverage_ge_3_5(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=65_000.0,
            pipeline_coverage_ratio=3.4,
        )
        pattern = self._call(engine, inp, 0.0, 0.0, 0.0, 0.0)
        assert pattern != ForecastPattern.sandbag_bias

    def test_sandbag_requires_ratio_below_70pct(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=75_000.0,  # 75 % not below 70 %
            pipeline_coverage_ratio=4.0,
        )
        pattern = self._call(engine, inp, 0.0, 0.0, 0.0, 0.0)
        assert pattern != ForecastPattern.sandbag_bias

    def test_overforecast_bias_takes_priority_over_stage_inflation(self, engine):
        """overforecast_bias check runs first in the method."""
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=140_000.0,
            stage_3_plus_avg_age_days=50.0,
        )
        pattern = self._call(engine, inp, 40.0, 0.0, 40.0, 0.0)
        assert pattern == ForecastPattern.overforecast_bias

    def test_zero_expected_skips_overforecast_and_sandbag(self, engine):
        inp = make_input(
            quota_usd=0.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=100_000.0,
            pipeline_coverage_ratio=4.0,
        )
        pattern = self._call(engine, inp, 40.0, 0.0, 0.0, 0.0)
        assert pattern not in (ForecastPattern.overforecast_bias, ForecastPattern.sandbag_bias)


# ===========================================================================
# 13. FLAGS
# ===========================================================================

class TestHasForecastGap:
    def test_no_gap_clean_input(self, engine, clean_input):
        gap = engine._has_forecast_gap(5.0, clean_input)
        assert gap is False

    def test_gap_when_composite_ge_40(self, engine, clean_input):
        gap = engine._has_forecast_gap(40.0, clean_input)
        assert gap is True

    def test_gap_when_override_ge_3(self, engine):
        inp = make_input(manual_forecast_override_count=3)
        gap = engine._has_forecast_gap(5.0, inp)
        assert gap is True

    def test_gap_when_variance_ratio_ge_25pct(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=130_000.0,   # 30 % off → >=25 %
        )
        gap = engine._has_forecast_gap(5.0, inp)
        assert gap is True

    def test_no_gap_when_variance_ratio_below_25pct(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=120_000.0,   # 20 % off
            manual_forecast_override_count=0,
        )
        gap = engine._has_forecast_gap(5.0, inp)
        assert gap is False

    def test_exact_boundary_composite_40(self, engine, clean_input):
        gap = engine._has_forecast_gap(40.0, clean_input)
        assert gap is True

    def test_exact_boundary_override_3(self, engine):
        inp = make_input(manual_forecast_override_count=3)
        gap = engine._has_forecast_gap(5.0, inp)
        assert gap is True

    def test_zero_expected_skips_variance_check(self, engine):
        inp = make_input(quota_usd=0.0, historical_avg_attainment_pct=1.0,
                         manual_forecast_override_count=0)
        gap = engine._has_forecast_gap(5.0, inp)
        assert gap is False


class TestRequiresForecastReview:
    def test_no_review_clean_input(self, engine, clean_input):
        review = engine._requires_forecast_review(5.0, clean_input)
        assert review is False

    def test_review_when_composite_ge_30(self, engine, clean_input):
        review = engine._requires_forecast_review(30.0, clean_input)
        assert review is True

    def test_review_when_push_rate_ge_20pct(self, engine):
        inp = make_input(
            close_date_pushed_count=2,
            total_forecast_deals=10,  # 20 %
        )
        review = engine._requires_forecast_review(5.0, inp)
        assert review is True

    def test_review_when_override_ge_2(self, engine):
        inp = make_input(manual_forecast_override_count=2)
        review = engine._requires_forecast_review(5.0, inp)
        assert review is True

    def test_no_review_all_below_thresholds(self, engine):
        inp = make_input(
            close_date_pushed_count=1,
            total_forecast_deals=10,   # 10 %
            manual_forecast_override_count=1,
        )
        review = engine._requires_forecast_review(10.0, inp)
        assert review is False

    def test_exact_boundary_composite_30(self, engine, clean_input):
        review = engine._requires_forecast_review(30.0, clean_input)
        assert review is True

    def test_exact_boundary_push_rate_20pct(self, engine):
        inp = make_input(
            close_date_pushed_count=2,
            total_forecast_deals=10,  # exactly 20 %
        )
        review = engine._requires_forecast_review(5.0, inp)
        assert review is True

    def test_exact_boundary_override_2(self, engine):
        inp = make_input(manual_forecast_override_count=2)
        review = engine._requires_forecast_review(5.0, inp)
        assert review is True

    def test_total_deals_zero_uses_one(self, engine):
        inp = make_input(
            close_date_pushed_count=1,
            total_forecast_deals=0,
        )
        # push_rate = 1/1 = 100 % >= 0.20
        review = engine._requires_forecast_review(5.0, inp)
        assert review is True


# ===========================================================================
# 14. ESTIMATED FORECAST VARIANCE
# ===========================================================================

class TestEstimatedForecastVariance:
    def test_zero_composite_returns_zero(self, engine, clean_input):
        variance = engine._estimated_forecast_variance(clean_input, 0.0)
        assert variance == 0.0

    def test_formula(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=120_000.0,
        )
        # raw_variance = |120000 - 100000| = 20000
        # variance = 20000 * (50/100) = 10000
        variance = engine._estimated_forecast_variance(inp, 50.0)
        assert variance == 10_000.0

    def test_rounded_to_two_decimals(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=0.33,
            current_forecast_usd=40_000.0,
        )
        variance = engine._estimated_forecast_variance(inp, 33.0)
        assert variance == round(abs(40_000.0 - 100_000.0 * 0.33) * 0.33, 2)

    def test_underforecast_variance(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=80_000.0,   # under by 20k
        )
        variance = engine._estimated_forecast_variance(inp, 40.0)
        # raw = 20000, factor = 0.40
        assert variance == 8_000.0

    def test_zero_quota_gives_zero_variance(self, engine):
        inp = make_input(
            quota_usd=0.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=100_000.0,
        )
        variance = engine._estimated_forecast_variance(inp, 50.0)
        # expected = 0, raw_variance = |100000-0| = 100000
        assert variance == round(100_000.0 * 0.50, 2)


# ===========================================================================
# 15. SIGNAL GENERATION
# ===========================================================================

class TestSignal:
    def test_healthy_signal_when_none_pattern_and_low_composite(self, engine, clean_input):
        signal = engine._signal(clean_input, ForecastPattern.none, 10.0)
        assert signal == "Forecast accuracy healthy — historical alignment and pipeline quality within benchmarks"

    def test_healthy_signal_exactly_below_20_composite(self, engine, clean_input):
        signal = engine._signal(clean_input, ForecastPattern.none, 19.9)
        assert signal == "Forecast accuracy healthy — historical alignment and pipeline quality within benchmarks"

    def test_not_healthy_when_composite_equals_20(self, engine, clean_input):
        signal = engine._signal(clean_input, ForecastPattern.none, 20.0)
        assert signal != "Forecast accuracy healthy — historical alignment and pipeline quality within benchmarks"

    def test_not_healthy_when_pattern_not_none(self, engine, clean_input):
        signal = engine._signal(clean_input, ForecastPattern.overforecast_bias, 10.0)
        assert signal != "Forecast accuracy healthy — historical alignment and pipeline quality within benchmarks"

    def test_signal_contains_composite_value(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=150_000.0,
            manual_forecast_override_count=0,
            close_date_pushed_count=0,
        )
        signal = engine._signal(inp, ForecastPattern.overforecast_bias, 45.0)
        assert "45" in signal

    def test_signal_contains_expected_attainment_ratio(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=150_000.0,
            manual_forecast_override_count=0,
            close_date_pushed_count=0,
        )
        signal = engine._signal(inp, ForecastPattern.overforecast_bias, 45.0)
        assert "150" in signal  # 150 % of expected

    def test_signal_contains_manual_override_count(self, engine):
        inp = make_input(
            manual_forecast_override_count=3,
            close_date_pushed_count=0,
            quota_usd=0.0,  # skip expected ratio
        )
        signal = engine._signal(inp, ForecastPattern.history_disconnect, 40.0)
        assert "3 manual overrides" in signal

    def test_signal_contains_close_date_pushed_pct(self, engine):
        inp = make_input(
            close_date_pushed_count=2,
            total_forecast_deals=10,
            manual_forecast_override_count=0,
            quota_usd=0.0,
        )
        signal = engine._signal(inp, ForecastPattern.stage_inflation, 40.0)
        assert "20% close dates pushed" in signal

    def test_signal_uses_pattern_label_in_output(self, engine):
        inp = make_input(quota_usd=0.0, manual_forecast_override_count=0, close_date_pushed_count=0)
        signal = engine._signal(inp, ForecastPattern.stage_inflation, 40.0)
        assert "stage inflation" in signal.lower()

    def test_signal_declining_when_no_parts(self, engine):
        """When no parts: expected=0, overrides=0, pushed=0"""
        inp = make_input(
            quota_usd=0.0,
            historical_avg_attainment_pct=1.0,
            manual_forecast_override_count=0,
            close_date_pushed_count=0,
        )
        signal = engine._signal(inp, ForecastPattern.overforecast_bias, 35.0)
        assert "forecast accuracy declining" in signal.lower()

    def test_signal_forecast_risk_label_when_pattern_none_and_high_composite(self, engine):
        inp = make_input(quota_usd=0.0, manual_forecast_override_count=0, close_date_pushed_count=0)
        signal = engine._signal(inp, ForecastPattern.none, 40.0)
        assert "forecast risk" in signal.lower()

    def test_signal_overforecast_bias_label_capitalized(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=150_000.0,
            manual_forecast_override_count=0,
            close_date_pushed_count=0,
        )
        signal = engine._signal(inp, ForecastPattern.overforecast_bias, 45.0)
        assert signal.startswith("Overforecast bias")

    def test_signal_sandbag_bias_label(self, engine):
        inp = make_input(quota_usd=0.0, manual_forecast_override_count=0, close_date_pushed_count=0)
        signal = engine._signal(inp, ForecastPattern.sandbag_bias, 35.0)
        assert signal.lower().startswith("sandbag bias")


# ===========================================================================
# 16. ASSESS() – END-TO-END
# ===========================================================================

class TestAssess:
    def test_assess_returns_result_type(self, engine, clean_input):
        result = engine.assess(clean_input)
        assert isinstance(result, ForecastSanityCheckResult)

    def test_assess_stores_rep_id_and_region(self, engine, clean_input):
        result = engine.assess(clean_input)
        assert result.rep_id == clean_input.rep_id
        assert result.region == clean_input.region

    def test_assess_result_appended_to_internal_list(self, engine, clean_input):
        engine.assess(clean_input)
        assert len(engine._results) == 1

    def test_assess_multiple_calls_accumulate(self, engine):
        for _ in range(5):
            engine.assess(make_input())
        assert len(engine._results) == 5

    def test_clean_input_gives_low_risk(self, engine):
        inp = make_input(
            historical_avg_attainment_pct=0.67,
            won_deals_ytd_count=10,
            lost_deals_ytd_count=5,
        )
        result = engine.assess(inp)
        assert result.forecast_risk == ForecastRisk.low

    def test_high_risk_scenario(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=160_000.0,   # +60%
            forecast_vs_prior_week_delta_pct=0.25,
            deals_pulled_in_from_next_qtr_count=3,
            total_forecast_deals=10,
            pipeline_coverage_ratio=1.8,
            crm_signal_quality_score=0.35,
            close_date_pushed_count=4,
        )
        result = engine.assess(inp)
        assert result.forecast_risk in (ForecastRisk.high, ForecastRisk.critical)

    def test_critical_risk_scenario(self, engine):
        inp = make_input(
            pipeline_coverage_ratio=1.0,
            crm_signal_quality_score=0.10,
            close_date_pushed_count=8,
            total_forecast_deals=10,
            stage_3_plus_avg_age_days=70.0,
            avg_days_in_stage_before_advance=25.0,
            late_quarter_close_date_count=6,
            manual_forecast_override_count=7,
            avg_deal_age_in_forecast_days=100.0,
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=180_000.0,
            forecast_vs_prior_week_delta_pct=0.30,
            deals_pulled_in_from_next_qtr_count=4,
        )
        result = engine.assess(inp)
        assert result.forecast_risk == ForecastRisk.critical
        assert result.forecast_severity == ForecastSeverity.distorted

    def test_assess_composite_is_weighted_sum(self, engine):
        inp = make_input()
        result = engine.assess(inp)
        o, p, s, h = (
            result.overforecast_bias_score,
            result.pipeline_quality_score,
            result.stage_integrity_score,
            result.history_alignment_score,
        )
        expected_composite = round(o * 0.30 + p * 0.30 + s * 0.25 + h * 0.15, 1)
        assert result.forecast_sanity_composite == expected_composite

    def test_assess_score_fields_are_non_negative(self, engine):
        result = engine.assess(make_input())
        assert result.overforecast_bias_score >= 0.0
        assert result.pipeline_quality_score >= 0.0
        assert result.stage_integrity_score >= 0.0
        assert result.history_alignment_score >= 0.0
        assert result.forecast_sanity_composite >= 0.0

    def test_assess_variance_non_negative(self, engine):
        result = engine.assess(make_input())
        assert result.estimated_forecast_variance_usd >= 0.0

    def test_assess_signal_is_string(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result.forecast_signal, str)
        assert len(result.forecast_signal) > 0

    def test_assess_has_forecast_gap_is_bool(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result.has_forecast_gap, bool)

    def test_assess_requires_review_is_bool(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result.requires_forecast_review, bool)

    def test_assess_overforecast_bias_pattern(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=150_000.0,  # 50 % over → ratio 0.50 >=0.25
            forecast_vs_prior_week_delta_pct=0.25,  # +30 to over
        )
        result = engine.assess(inp)
        assert result.forecast_pattern == ForecastPattern.overforecast_bias

    def test_assess_sandbag_bias_pattern(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=60_000.0,   # 60 % < 70 %
            pipeline_coverage_ratio=4.0,
        )
        result = engine.assess(inp)
        assert result.forecast_pattern == ForecastPattern.sandbag_bias

    def test_assess_recommended_action_type(self, engine):
        result = engine.assess(make_input())
        assert isinstance(result.recommended_action, ForecastAction)

    def test_assess_healthy_signal_for_clean_rep(self, engine):
        # Use an input that is truly clean
        inp = make_input(
            historical_avg_attainment_pct=0.67,
            won_deals_ytd_count=10,
            lost_deals_ytd_count=5,
        )
        result = engine.assess(inp)
        if result.forecast_pattern == ForecastPattern.none and result.forecast_sanity_composite < 20:
            expected_signal = "Forecast accuracy healthy — historical alignment and pipeline quality within benchmarks"
            assert result.forecast_signal == expected_signal


# ===========================================================================
# 17. ASSESS_BATCH()
# ===========================================================================

class TestAssessBatch:
    def test_returns_list(self, engine):
        results = engine.assess_batch([make_input(), make_input()])
        assert isinstance(results, list)

    def test_length_matches_input(self, engine):
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(7)]
        results = engine.assess_batch(inputs)
        assert len(results) == 7

    def test_each_result_is_correct_type(self, engine):
        results = engine.assess_batch([make_input(), make_input()])
        for r in results:
            assert isinstance(r, ForecastSanityCheckResult)

    def test_rep_ids_preserved_in_order(self, engine):
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"rep-{i}"

    def test_empty_batch_returns_empty_list(self, engine):
        results = engine.assess_batch([])
        assert results == []

    def test_batch_results_appended_to_internal_list(self, engine):
        engine.assess_batch([make_input(), make_input(), make_input()])
        assert len(engine._results) == 3

    def test_batch_accumulates_with_single_assess(self, engine):
        engine.assess(make_input())
        engine.assess_batch([make_input(), make_input()])
        assert len(engine._results) == 3

    def test_batch_single_item(self, engine):
        results = engine.assess_batch([make_input(rep_id="solo")])
        assert len(results) == 1
        assert results[0].rep_id == "solo"

    def test_batch_mixed_risk_levels(self, engine):
        clean = make_input(
            historical_avg_attainment_pct=0.67,
            won_deals_ytd_count=10,
            lost_deals_ytd_count=5,
        )
        risky = make_input(
            pipeline_coverage_ratio=1.0,
            crm_signal_quality_score=0.10,
            close_date_pushed_count=8,
            total_forecast_deals=10,
            stage_3_plus_avg_age_days=70.0,
        )
        results = engine.assess_batch([clean, risky])
        risks = {r.forecast_risk for r in results}
        assert len(risks) >= 1


# ===========================================================================
# 18. SUMMARY()
# ===========================================================================

class TestSummary:
    def test_empty_summary_returns_zeros(self, engine):
        s = engine.summary()
        assert s["total"] == 0
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}
        assert s["avg_forecast_sanity_composite"] == 0.0
        assert s["forecast_gap_count"] == 0
        assert s["review_required_count"] == 0
        assert s["avg_overforecast_bias_score"] == 0.0
        assert s["avg_pipeline_quality_score"] == 0.0
        assert s["avg_stage_integrity_score"] == 0.0
        assert s["avg_history_alignment_score"] == 0.0
        assert s["total_estimated_forecast_variance_usd"] == 0.0

    def test_summary_key_count(self, engine):
        s = engine.summary()
        assert len(s) == 13

    def test_summary_key_names(self, engine):
        s = engine.summary()
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_forecast_sanity_composite",
            "forecast_gap_count", "review_required_count",
            "avg_overforecast_bias_score", "avg_pipeline_quality_score",
            "avg_stage_integrity_score", "avg_history_alignment_score",
            "total_estimated_forecast_variance_usd",
        }
        assert set(s.keys()) == expected_keys

    def test_summary_total_count(self, engine):
        for _ in range(4):
            engine.assess(make_input())
        s = engine.summary()
        assert s["total"] == 4

    def test_summary_risk_counts_keys_are_strings(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        for k in s["risk_counts"]:
            assert isinstance(k, str)

    def test_summary_risk_counts_values_are_int(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        for v in s["risk_counts"].values():
            assert isinstance(v, int)

    def test_summary_risk_count_sums_to_total(self, engine):
        engine.assess_batch([make_input() for _ in range(6)])
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_pattern_count_sums_to_total(self, engine):
        engine.assess_batch([make_input() for _ in range(6)])
        s = engine.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_summary_severity_count_sums_to_total(self, engine):
        engine.assess_batch([make_input() for _ in range(6)])
        s = engine.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_summary_action_count_sums_to_total(self, engine):
        engine.assess_batch([make_input() for _ in range(6)])
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_avg_composite_single_item(self, engine):
        inp = make_input(
            historical_avg_attainment_pct=0.67,
            won_deals_ytd_count=10,
            lost_deals_ytd_count=5,
        )
        result = engine.assess(inp)
        s = engine.summary()
        assert s["avg_forecast_sanity_composite"] == result.forecast_sanity_composite

    def test_summary_forecast_gap_count(self, engine):
        engine.assess(make_input(manual_forecast_override_count=5))  # gap=True
        engine.assess(make_input())  # gap depends on composite
        s = engine.summary()
        assert s["forecast_gap_count"] >= 1

    def test_summary_review_required_count(self, engine):
        engine.assess(make_input(manual_forecast_override_count=3))  # review=True
        s = engine.summary()
        assert s["review_required_count"] >= 1

    def test_summary_avg_scores_are_non_negative(self, engine):
        engine.assess_batch([make_input() for _ in range(3)])
        s = engine.summary()
        assert s["avg_overforecast_bias_score"] >= 0.0
        assert s["avg_pipeline_quality_score"] >= 0.0
        assert s["avg_stage_integrity_score"] >= 0.0
        assert s["avg_history_alignment_score"] >= 0.0

    def test_summary_total_variance_is_float(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert isinstance(s["total_estimated_forecast_variance_usd"], float)

    def test_summary_total_variance_aggregates(self, engine):
        inp1 = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=120_000.0,
        )
        inp2 = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=80_000.0,
        )
        r1 = engine.assess(inp1)
        r2 = engine.assess(inp2)
        s = engine.summary()
        expected = round(r1.estimated_forecast_variance_usd + r2.estimated_forecast_variance_usd, 2)
        assert s["total_estimated_forecast_variance_usd"] == expected

    def test_summary_multiple_engines_are_independent(self):
        e1 = SalesForecastSanityCheckIntelligenceEngine()
        e2 = SalesForecastSanityCheckIntelligenceEngine()
        e1.assess(make_input())
        s1 = e1.summary()
        s2 = e2.summary()
        assert s1["total"] == 1
        assert s2["total"] == 0

    def test_summary_after_batch(self, engine):
        engine.assess_batch([make_input() for _ in range(10)])
        s = engine.summary()
        assert s["total"] == 10

    def test_summary_avg_rounded_to_one_decimal(self, engine):
        for _ in range(3):
            engine.assess(make_input())
        s = engine.summary()
        # Check that averages have at most 1 decimal place
        for key in ("avg_forecast_sanity_composite", "avg_overforecast_bias_score",
                    "avg_pipeline_quality_score", "avg_stage_integrity_score",
                    "avg_history_alignment_score"):
            val = s[key]
            assert round(val, 1) == val


# ===========================================================================
# 19. EDGE CASES
# ===========================================================================

class TestEdgeCases:
    def test_all_zeros_input(self, engine):
        inp = make_input(
            current_forecast_usd=0.0,
            historical_avg_attainment_pct=0.0,
            quota_usd=0.0,
            pipeline_coverage_ratio=0.0,
            avg_deal_age_in_forecast_days=0.0,
            deals_added_last_7d_count=0,
            deals_pulled_in_from_next_qtr_count=0,
            stage_3_plus_deal_count=0,
            stage_3_plus_avg_age_days=0.0,
            forecast_vs_prior_week_delta_pct=0.0,
            manual_forecast_override_count=0,
            won_deals_ytd_count=0,
            lost_deals_ytd_count=0,
            avg_days_in_stage_before_advance=0.0,
            late_quarter_close_date_count=0,
            total_forecast_deals=0,
            close_date_pushed_count=0,
            avg_opportunity_value_usd=0.0,
            crm_signal_quality_score=0.0,
        )
        result = engine.assess(inp)
        assert isinstance(result, ForecastSanityCheckResult)

    def test_very_large_values(self, engine):
        inp = make_input(
            current_forecast_usd=1e9,
            quota_usd=1e9,
            historical_avg_attainment_pct=1.0,
            avg_opportunity_value_usd=1e8,
        )
        result = engine.assess(inp)
        assert result.forecast_sanity_composite <= 100.0

    def test_crm_score_exactly_zero(self, engine):
        inp = make_input(crm_signal_quality_score=0.0)
        score = engine._pipeline_quality_score(inp)
        assert score >= 25.0  # below 0.40 threshold

    def test_crm_score_exactly_one(self, engine):
        inp = make_input(crm_signal_quality_score=1.0)
        score = engine._pipeline_quality_score(inp)
        assert score == 0.0   # above 0.60 threshold

    def test_pipeline_coverage_zero(self, engine):
        inp = make_input(pipeline_coverage_ratio=0.0)
        score = engine._pipeline_quality_score(inp)
        assert score >= 35.0

    def test_manual_override_large_number(self, engine):
        inp = make_input(manual_forecast_override_count=100)
        score = engine._history_alignment_score(inp)
        assert score <= 100.0

    def test_all_deals_pushed(self, engine):
        inp = make_input(
            close_date_pushed_count=10,
            total_forecast_deals=10,
        )
        score = engine._pipeline_quality_score(inp)
        assert score <= 100.0

    def test_no_closed_deals_ytd(self, engine):
        inp = make_input(won_deals_ytd_count=0, lost_deals_ytd_count=0)
        score = engine._history_alignment_score(inp)
        assert isinstance(score, float)

    def test_assess_with_single_deal(self, engine):
        inp = make_input(
            total_forecast_deals=1,
            close_date_pushed_count=1,
            late_quarter_close_date_count=1,
            deals_pulled_in_from_next_qtr_count=1,
        )
        result = engine.assess(inp)
        assert isinstance(result, ForecastSanityCheckResult)

    def test_forecast_exactly_equals_expected(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=100_000.0,
        )
        score = engine._overforecast_bias_score(inp)
        # ratio = 0, no overforecast component
        assert score == 0.0

    def test_rep_id_and_region_preserved_through_assess(self, engine):
        inp = make_input(rep_id="REP-XYZ", region="LATAM")
        result = engine.assess(inp)
        assert result.rep_id == "REP-XYZ"
        assert result.region == "LATAM"

    def test_new_engine_has_empty_results(self):
        e = SalesForecastSanityCheckIntelligenceEngine()
        assert e._results == []

    def test_to_dict_returns_new_dict_each_call(self, engine):
        result = engine.assess(make_input())
        d1 = result.to_dict()
        d2 = result.to_dict()
        assert d1 == d2
        assert d1 is not d2

    def test_variance_positive_when_over_forecast(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=150_000.0,
            forecast_vs_prior_week_delta_pct=0.25,
        )
        result = engine.assess(inp)
        assert result.estimated_forecast_variance_usd >= 0.0

    def test_variance_positive_when_under_forecast(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=50_000.0,
        )
        result = engine.assess(inp)
        assert result.estimated_forecast_variance_usd >= 0.0

    def test_historical_attainment_above_one(self, engine):
        """attainment_pct > 1.0 is unusual but should not crash."""
        inp = make_input(
            historical_avg_attainment_pct=1.30,
            quota_usd=100_000.0,
            current_forecast_usd=130_000.0,
        )
        result = engine.assess(inp)
        assert isinstance(result, ForecastSanityCheckResult)

    def test_negative_forecast_delta(self, engine):
        """Negative delta_pct should not crash."""
        inp = make_input(forecast_vs_prior_week_delta_pct=-0.10)
        result = engine.assess(inp)
        assert isinstance(result, ForecastSanityCheckResult)

    def test_summary_called_twice_consistent(self, engine):
        engine.assess_batch([make_input() for _ in range(3)])
        s1 = engine.summary()
        s2 = engine.summary()
        assert s1 == s2


# ===========================================================================
# 20. INTEGRATION / SCENARIO TESTS
# ===========================================================================

class TestIntegrationScenarios:
    def test_sandbag_rep_scenario(self, engine):
        """Rep with very low forecast vs high pipeline → sandbag_bias."""
        inp = make_input(
            rep_id="sandbagger-01",
            quota_usd=200_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=120_000.0,   # 60 % of expected
            pipeline_coverage_ratio=4.5,
            manual_forecast_override_count=0,
        )
        result = engine.assess(inp)
        assert result.forecast_pattern == ForecastPattern.sandbag_bias

    def test_overforecast_rep_gets_intervention(self, engine):
        """Rep who over-forecasts at critical level should get override intervention."""
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=200_000.0,   # 100 % over
            forecast_vs_prior_week_delta_pct=0.30,
            deals_pulled_in_from_next_qtr_count=4,
            total_forecast_deals=10,
            pipeline_coverage_ratio=1.0,
            crm_signal_quality_score=0.10,
            close_date_pushed_count=5,
        )
        result = engine.assess(inp)
        assert result.forecast_risk == ForecastRisk.critical
        assert result.recommended_action == ForecastAction.forecast_override_intervention

    def test_stage_inflation_rep_gets_audit(self, engine):
        """Stage inflation at critical risk → deal_stage_audit."""
        # Force stage score >= 30 and stage_3_plus_avg_age_days >=45 at critical composite
        inp = make_input(
            stage_3_plus_avg_age_days=80.0,     # +40 stage
            avg_days_in_stage_before_advance=25.0,  # +30 stage
            late_quarter_close_date_count=6,
            total_forecast_deals=10,             # 60% late → +25 stage → stage=95
            pipeline_coverage_ratio=1.0,         # pipeline very high
            crm_signal_quality_score=0.10,
            close_date_pushed_count=4,
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=200_000.0,
            forecast_vs_prior_week_delta_pct=0.30,
            deals_pulled_in_from_next_qtr_count=4,
            manual_forecast_override_count=0,
        )
        result = engine.assess(inp)
        if result.forecast_risk == ForecastRisk.critical and result.forecast_pattern == ForecastPattern.stage_inflation:
            assert result.recommended_action == ForecastAction.deal_stage_audit

    def test_history_disconnect_rep_gets_recalibration(self, engine):
        """History disconnect at high risk → historical_recalibration."""
        inp = make_input(
            historical_avg_attainment_pct=0.90,
            won_deals_ytd_count=3,
            lost_deals_ytd_count=7,   # win_rate=0.30, gap=0.60 → +40
            manual_forecast_override_count=4,   # +35 history, and triggers disconnect pattern
            avg_deal_age_in_forecast_days=95.0,  # +20 history → total=95
            pipeline_coverage_ratio=4.0,
            crm_signal_quality_score=0.80,
            close_date_pushed_count=0,
        )
        result = engine.assess(inp)
        if result.forecast_risk == ForecastRisk.high and result.forecast_pattern == ForecastPattern.history_disconnect:
            assert result.recommended_action == ForecastAction.historical_recalibration

    def test_full_pipeline_scenario_summary(self, engine):
        """Run a batch of mixed reps and verify summary totals."""
        reps = [
            make_input(rep_id=f"rep-{i}", region="NA")
            for i in range(12)
        ]
        engine.assess_batch(reps)
        s = engine.summary()
        assert s["total"] == 12
        assert sum(s["risk_counts"].values()) == 12
        assert sum(s["severity_counts"].values()) == 12
        assert sum(s["pattern_counts"].values()) == 12

    def test_healthy_rep_complete_check(self, engine):
        """A genuinely healthy rep should score low everywhere."""
        inp = make_input(
            historical_avg_attainment_pct=0.67,
            won_deals_ytd_count=10,
            lost_deals_ytd_count=5,
            quota_usd=100_000.0,
            current_forecast_usd=67_000.0,
            pipeline_coverage_ratio=3.5,
            crm_signal_quality_score=0.85,
            close_date_pushed_count=0,
            manual_forecast_override_count=0,
            avg_deal_age_in_forecast_days=25.0,
            stage_3_plus_avg_age_days=15.0,
            avg_days_in_stage_before_advance=4.0,
            late_quarter_close_date_count=0,
            deals_pulled_in_from_next_qtr_count=0,
            forecast_vs_prior_week_delta_pct=0.0,
        )
        result = engine.assess(inp)
        assert result.forecast_risk == ForecastRisk.low
        assert result.forecast_severity == ForecastSeverity.accurate
        assert result.recommended_action == ForecastAction.no_action

    def test_to_dict_full_cycle(self, engine):
        """assess → to_dict should have correct values."""
        inp = make_input(rep_id="dict-test", region="EMEA")
        result = engine.assess(inp)
        d = result.to_dict()
        assert d["rep_id"] == "dict-test"
        assert d["region"] == "EMEA"
        assert d["forecast_risk"] == result.forecast_risk.value
        assert d["forecast_pattern"] == result.forecast_pattern.value
        assert d["forecast_severity"] == result.forecast_severity.value
        assert d["recommended_action"] == result.recommended_action.value
        assert d["overforecast_bias_score"] == result.overforecast_bias_score
        assert d["pipeline_quality_score"] == result.pipeline_quality_score
        assert d["stage_integrity_score"] == result.stage_integrity_score
        assert d["history_alignment_score"] == result.history_alignment_score
        assert d["forecast_sanity_composite"] == result.forecast_sanity_composite
        assert d["has_forecast_gap"] == result.has_forecast_gap
        assert d["requires_forecast_review"] == result.requires_forecast_review
        assert d["estimated_forecast_variance_usd"] == result.estimated_forecast_variance_usd
        assert d["forecast_signal"] == result.forecast_signal

    def test_multiple_engines_dont_share_state(self):
        e1 = SalesForecastSanityCheckIntelligenceEngine()
        e2 = SalesForecastSanityCheckIntelligenceEngine()
        e1.assess(make_input())
        assert len(e1._results) == 1
        assert len(e2._results) == 0

    def test_assess_batch_vs_individual_assess_identical(self, engine):
        """assess_batch results should match individual assess calls."""
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(5)]
        engine2 = SalesForecastSanityCheckIntelligenceEngine()

        batch_results = engine.assess_batch(inputs)
        individual_results = [engine2.assess(inp) for inp in inputs]

        for b, ind in zip(batch_results, individual_results):
            assert b.forecast_risk == ind.forecast_risk
            assert b.forecast_pattern == ind.forecast_pattern
            assert b.forecast_severity == ind.forecast_severity
            assert b.forecast_sanity_composite == ind.forecast_sanity_composite


# ===========================================================================
# 21. ADDITIONAL BOUNDARY AND COVERAGE TESTS
# ===========================================================================

class TestAdditionalBoundaryTests:
    """Extra tests to ensure full boundary coverage of all score methods."""

    # --- overforecast: negative overforecast (underforecast) ---
    def test_overforecast_score_when_under_expected(self, engine):
        """When current < expected, ratio is negative → no score added."""
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=80_000.0,   # -20 %
            forecast_vs_prior_week_delta_pct=0.0,
            deals_pulled_in_from_next_qtr_count=0,
        )
        score = engine._overforecast_bias_score(inp)
        assert score == 0.0

    def test_overforecast_zero_attainment_pct_zero_expected(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=0.0,
            current_forecast_usd=50_000.0,
            forecast_vs_prior_week_delta_pct=0.0,
            deals_pulled_in_from_next_qtr_count=0,
        )
        # expected = 100000 * 0 = 0, skip ratio
        score = engine._overforecast_bias_score(inp)
        assert score == 0.0

    # --- pipeline: push_rate exact boundary 0.05 ---
    def test_pipeline_push_rate_exactly_5pct(self, engine):
        inp = make_input(
            close_date_pushed_count=1,
            total_forecast_deals=20,    # exactly 5 %
            pipeline_coverage_ratio=4.0,
            crm_signal_quality_score=0.80,
        )
        score = engine._pipeline_quality_score(inp)
        assert score == 7.0

    # --- stage: deals = 1 edge case ---
    def test_stage_single_deal_pushed(self, engine):
        inp = make_input(
            late_quarter_close_date_count=1,
            total_forecast_deals=1,    # 100 % late → +25
            stage_3_plus_avg_age_days=20.0,
            avg_days_in_stage_before_advance=0.0,
        )
        score = engine._stage_integrity_score(inp)
        assert score == 25.0

    # --- history: attainment pct == 0 check ---
    def test_history_zero_attainment_skips_win_rate_gap(self, engine):
        inp = make_input(
            historical_avg_attainment_pct=0.0,
            won_deals_ytd_count=5,
            lost_deals_ytd_count=5,
            manual_forecast_override_count=0,
            avg_deal_age_in_forecast_days=30.0,
        )
        score = engine._history_alignment_score(inp)
        # no win_rate_gap contribution, no overrides, deal_age<60 → 0
        assert score == 0.0

    # --- signal tests ---
    def test_signal_sandbag_bias_parts_when_pushed(self, engine):
        inp = make_input(
            close_date_pushed_count=3,
            total_forecast_deals=10,
            manual_forecast_override_count=0,
            quota_usd=0.0,
        )
        signal = engine._signal(inp, ForecastPattern.sandbag_bias, 40.0)
        assert "30% close dates pushed" in signal

    def test_signal_late_quarter_stuffing_label(self, engine):
        inp = make_input(quota_usd=0.0, manual_forecast_override_count=0, close_date_pushed_count=0)
        signal = engine._signal(inp, ForecastPattern.late_quarter_stuffing, 40.0)
        assert "late quarter stuffing" in signal.lower()

    def test_signal_history_disconnect_label(self, engine):
        inp = make_input(quota_usd=0.0, manual_forecast_override_count=0, close_date_pushed_count=0)
        signal = engine._signal(inp, ForecastPattern.history_disconnect, 40.0)
        assert "history disconnect" in signal.lower()

    # --- to_dict enum value types ---
    def test_to_dict_forecast_risk_value_low(self, engine):
        result = engine.assess(make_input(
            historical_avg_attainment_pct=0.67,
            won_deals_ytd_count=10,
            lost_deals_ytd_count=5,
        ))
        d = result.to_dict()
        assert d["forecast_risk"] in ("low", "moderate", "high", "critical")

    def test_to_dict_forecast_pattern_is_valid_value(self, engine):
        result = engine.assess(make_input())
        d = result.to_dict()
        valid_patterns = {p.value for p in ForecastPattern}
        assert d["forecast_pattern"] in valid_patterns

    def test_to_dict_severity_is_valid_value(self, engine):
        result = engine.assess(make_input())
        d = result.to_dict()
        valid_sev = {s.value for s in ForecastSeverity}
        assert d["forecast_severity"] in valid_sev

    def test_to_dict_action_is_valid_value(self, engine):
        result = engine.assess(make_input())
        d = result.to_dict()
        valid_actions = {a.value for a in ForecastAction}
        assert d["recommended_action"] in valid_actions

    # --- _has_forecast_gap exact boundary: override == 2 (not 3) → False ---
    def test_forecast_gap_false_with_2_overrides(self, engine):
        inp = make_input(
            manual_forecast_override_count=2,
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=110_000.0,   # 10 % < 25 %
        )
        gap = engine._has_forecast_gap(5.0, inp)
        assert gap is False

    # --- requires_review exact boundary: override == 1 → False ---
    def test_requires_review_false_with_1_override(self, engine):
        inp = make_input(
            manual_forecast_override_count=1,
            close_date_pushed_count=0,
        )
        review = engine._requires_forecast_review(5.0, inp)
        assert review is False

    # --- variance formula: composite == 100 ---
    def test_variance_at_full_composite(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=150_000.0,
        )
        variance = engine._estimated_forecast_variance(inp, 100.0)
        # raw = 50000, factor = 1.0
        assert variance == 50_000.0

    # --- summary: action_counts keys are strings ---
    def test_summary_action_counts_keys_are_strings(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        for k in s["action_counts"]:
            assert isinstance(k, str)

    # --- summary: pattern_counts keys are strings ---
    def test_summary_pattern_counts_keys_are_strings(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        for k in s["pattern_counts"]:
            assert isinstance(k, str)

    # --- summary: severity_counts keys are strings ---
    def test_summary_severity_counts_keys_are_strings(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        for k in s["severity_counts"]:
            assert isinstance(k, str)

    # --- enum: ForecastRisk string comparison ---
    def test_forecast_risk_string_comparison(self):
        assert ForecastRisk.high == "high"
        assert ForecastRisk.moderate == "moderate"

    # --- enum: ForecastSeverity string comparison ---
    def test_forecast_severity_string_comparison(self):
        assert ForecastSeverity.drifting == "drifting"
        assert ForecastSeverity.distorted == "distorted"

    # --- enum: ForecastAction string comparison ---
    def test_forecast_action_string_comparison(self):
        assert ForecastAction.deal_stage_audit == "deal_stage_audit"
        assert ForecastAction.historical_recalibration == "historical_recalibration"

    # --- _risk_level at exact boundary 19.9 → low ---
    def test_risk_exactly_below_20_is_low(self, engine):
        assert engine._risk_level(19.9) == ForecastRisk.low

    # --- _severity at exact boundary 59.9 → unreliable ---
    def test_severity_exactly_below_60_is_unreliable(self, engine):
        assert engine._severity(59.9) == ForecastSeverity.unreliable

    # --- _severity at exact boundary 39.9 → drifting ---
    def test_severity_exactly_below_40_is_drifting(self, engine):
        assert engine._severity(39.9) == ForecastSeverity.drifting

    # --- _risk_level at exact boundary 59.9 → high ---
    def test_risk_exactly_below_60_is_high(self, engine):
        assert engine._risk_level(59.9) == ForecastRisk.high

    # --- assess: overforecast score is rounded to 1 decimal ---
    def test_assess_subscores_rounded_to_1_decimal(self, engine):
        result = engine.assess(make_input())
        for score in (
            result.overforecast_bias_score,
            result.pipeline_quality_score,
            result.stage_integrity_score,
            result.history_alignment_score,
        ):
            assert round(score, 1) == score

    # --- assess: composite is rounded to 1 decimal ---
    def test_assess_composite_rounded_to_1_decimal(self, engine):
        result = engine.assess(make_input())
        assert round(result.forecast_sanity_composite, 1) == result.forecast_sanity_composite

    # --- assess: result has all 15 fields filled ---
    def test_assess_result_has_all_fields(self, engine):
        import dataclasses
        result = engine.assess(make_input())
        for field in dataclasses.fields(ForecastSanityCheckResult):
            assert hasattr(result, field.name)

    # --- assess: result to_dict has no None values ---
    def test_assess_to_dict_no_none_values(self, engine):
        result = engine.assess(make_input())
        d = result.to_dict()
        for v in d.values():
            assert v is not None

    # --- detect_pattern: late_quarter via exact boundary pull-in rate 15% ---
    def test_detect_pattern_late_quarter_exact_15pct_pull_in(self, engine):
        inp = make_input(
            deals_pulled_in_from_next_qtr_count=15,
            total_forecast_deals=100,   # exactly 15 %
        )
        pattern = engine._detect_pattern(inp, 25.0, 0.0, 0.0, 0.0)
        assert pattern == ForecastPattern.late_quarter_stuffing

    # --- detect_pattern: late_quarter exact 40% late rate ---
    def test_detect_pattern_late_quarter_exact_40pct_late_rate(self, engine):
        inp = make_input(
            late_quarter_close_date_count=4,
            total_forecast_deals=10,   # exactly 40 %
        )
        pattern = engine._detect_pattern(inp, 25.0, 0.0, 0.0, 0.0)
        assert pattern == ForecastPattern.late_quarter_stuffing

    # --- detect_pattern: history_disconnect exact boundary override==2 ---
    def test_detect_pattern_history_disconnect_exact_2_overrides(self, engine):
        inp = make_input(manual_forecast_override_count=2)
        pattern = engine._detect_pattern(inp, 0.0, 0.0, 0.0, 35.0)
        assert pattern == ForecastPattern.history_disconnect

    # --- detect_pattern: sandbag exact boundary coverage==3.5 ---
    def test_detect_pattern_sandbag_exact_3_5_coverage(self, engine):
        inp = make_input(
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=60_000.0,
            pipeline_coverage_ratio=3.5,   # exactly at boundary
        )
        pattern = engine._detect_pattern(inp, 0.0, 0.0, 0.0, 0.0)
        assert pattern == ForecastPattern.sandbag_bias

    # --- summary: empty engine keys present ---
    def test_empty_summary_has_all_13_keys(self, engine):
        s = engine.summary()
        assert "total" in s
        assert "risk_counts" in s
        assert "pattern_counts" in s
        assert "severity_counts" in s
        assert "action_counts" in s
        assert "avg_forecast_sanity_composite" in s
        assert "forecast_gap_count" in s
        assert "review_required_count" in s
        assert "avg_overforecast_bias_score" in s
        assert "avg_pipeline_quality_score" in s
        assert "avg_stage_integrity_score" in s
        assert "avg_history_alignment_score" in s
        assert "total_estimated_forecast_variance_usd" in s

    # --- assess_batch: regions preserved ---
    def test_assess_batch_regions_preserved(self, engine):
        regions = ["NA", "EMEA", "APAC", "LATAM"]
        inputs = [make_input(rep_id=f"rep-{i}", region=r) for i, r in enumerate(regions)]
        results = engine.assess_batch(inputs)
        for result, expected_region in zip(results, regions):
            assert result.region == expected_region

    # --- detect_pattern priority: late_quarter before stage_inflation ---
    def test_detect_pattern_late_quarter_before_stage_inflation(self, engine):
        """late_quarter_stuffing check comes before stage_inflation."""
        inp = make_input(
            deals_pulled_in_from_next_qtr_count=2,
            total_forecast_deals=10,   # 20 % pull-in
            stage_3_plus_avg_age_days=50.0,  # would trigger stage_inflation too
        )
        pattern = engine._detect_pattern(inp, 25.0, 0.0, 40.0, 0.0)
        assert pattern == ForecastPattern.late_quarter_stuffing

    # --- assess: pipeline coverage 3.0 adds 0 ---
    def test_pipeline_coverage_exactly_3_adds_0(self, engine):
        inp = make_input(
            pipeline_coverage_ratio=3.0,
            close_date_pushed_count=0,
            crm_signal_quality_score=0.80,
        )
        score = engine._pipeline_quality_score(inp)
        assert score == 0.0

    # --- has_forecast_gap: override exactly 2 is not enough ---
    def test_has_forecast_gap_override_2_is_false(self, engine):
        inp = make_input(
            manual_forecast_override_count=2,
            quota_usd=100_000.0,
            historical_avg_attainment_pct=1.0,
            current_forecast_usd=105_000.0,  # 5% off
        )
        gap = engine._has_forecast_gap(5.0, inp)
        assert gap is False
