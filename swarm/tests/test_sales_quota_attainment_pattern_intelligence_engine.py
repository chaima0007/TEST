"""
Comprehensive pytest tests for SalesQuotaAttainmentPatternIntelligenceEngine.
Coverage: enums, dataclass fields, sub-scores, pattern detection, risk/severity,
action mapping, flags, revenue-at-risk, signal strings, assess, assess_batch, summary.
"""
from __future__ import annotations

import pytest

from swarm.intelligence.sales_quota_attainment_pattern_intelligence_engine import (
    QuotaAction,
    QuotaInput,
    QuotaPattern,
    QuotaResult,
    QuotaRisk,
    QuotaSeverity,
    SalesQuotaAttainmentPatternIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_input(**overrides) -> QuotaInput:
    """Return a baseline QuotaInput that sits in the low-risk zone."""
    defaults = dict(
        rep_id="REP-001",
        region="EMEA",
        evaluation_period_id="Q1-2026",
        quota_attainment_pct=1.05,
        prior_quarter_attainment_pct=1.10,
        attainment_variance_pct=0.05,
        pct_quota_achieved_by_month1_end=0.35,
        pct_quota_achieved_by_month2_end=0.70,
        pct_deals_closed_in_final_2_weeks_pct=0.15,
        avg_monthly_bookings_variance_pct=0.10,
        forecast_accuracy_pct=0.92,
        commit_to_close_rate_pct=0.85,
        pipeline_coverage_ratio=5.0,
        avg_deal_size_usd=50_000.0,
        total_deals_closed=10,
        deals_pushed_to_next_quarter_pct=0.05,
        discount_rate_avg_pct=0.10,
        new_logo_pct=0.40,
        expansion_revenue_pct=0.30,
        avg_sales_cycle_days=45.0,
        quarters_above_quota_last_4=4,
        avg_opportunity_value_usd=55_000.0,
    )
    defaults.update(overrides)
    return QuotaInput(**defaults)


def _engine() -> SalesQuotaAttainmentPatternIntelligenceEngine:
    return SalesQuotaAttainmentPatternIntelligenceEngine()


# ===========================================================================
# 1. Enum Tests
# ===========================================================================

class TestQuotaRiskEnum:
    def test_members_count(self):
        assert len(QuotaRisk) == 4

    def test_low_value(self):
        assert QuotaRisk.low.value == "low"

    def test_moderate_value(self):
        assert QuotaRisk.moderate.value == "moderate"

    def test_high_value(self):
        assert QuotaRisk.high.value == "high"

    def test_critical_value(self):
        assert QuotaRisk.critical.value == "critical"

    def test_is_str_subclass(self):
        assert isinstance(QuotaRisk.low, str)

    def test_string_comparison(self):
        assert QuotaRisk.low == "low"


class TestQuotaPatternEnum:
    def test_members_count(self):
        assert len(QuotaPattern) == 6

    def test_none_value(self):
        assert QuotaPattern.none.value == "none"

    def test_sandbagging_value(self):
        assert QuotaPattern.sandbagging.value == "sandbagging"

    def test_feast_or_famine_value(self):
        assert QuotaPattern.feast_or_famine.value == "feast_or_famine"

    def test_late_quarter_cliff_value(self):
        assert QuotaPattern.late_quarter_cliff.value == "late_quarter_cliff"

    def test_early_coasting_value(self):
        assert QuotaPattern.early_coasting.value == "early_coasting"

    def test_consistent_underperformance_value(self):
        assert QuotaPattern.consistent_underperformance.value == "consistent_underperformance"

    def test_is_str_subclass(self):
        assert isinstance(QuotaPattern.none, str)


class TestQuotaSeverityEnum:
    def test_members_count(self):
        assert len(QuotaSeverity) == 4

    def test_disciplined_value(self):
        assert QuotaSeverity.disciplined.value == "disciplined"

    def test_developing_value(self):
        assert QuotaSeverity.developing.value == "developing"

    def test_inconsistent_value(self):
        assert QuotaSeverity.inconsistent.value == "inconsistent"

    def test_at_risk_value(self):
        assert QuotaSeverity.at_risk.value == "at_risk"

    def test_is_str_subclass(self):
        assert isinstance(QuotaSeverity.disciplined, str)


class TestQuotaActionEnum:
    def test_members_count(self):
        assert len(QuotaAction) == 6

    def test_no_action_value(self):
        assert QuotaAction.no_action.value == "no_action"

    def test_pipeline_pacing_coaching_value(self):
        assert QuotaAction.pipeline_pacing_coaching.value == "pipeline_pacing_coaching"

    def test_activity_rhythm_coaching_value(self):
        assert QuotaAction.activity_rhythm_coaching.value == "activity_rhythm_coaching"

    def test_forecast_accuracy_training_value(self):
        assert QuotaAction.forecast_accuracy_training.value == "forecast_accuracy_training"

    def test_performance_improvement_plan_value(self):
        assert QuotaAction.performance_improvement_plan.value == "performance_improvement_plan"

    def test_quota_reset_review_value(self):
        assert QuotaAction.quota_reset_review.value == "quota_reset_review"

    def test_is_str_subclass(self):
        assert isinstance(QuotaAction.no_action, str)


# ===========================================================================
# 2. QuotaInput Dataclass – field existence & types
# ===========================================================================

class TestQuotaInputFields:
    def test_rep_id_field(self):
        inp = _make_input(rep_id="X")
        assert inp.rep_id == "X"

    def test_region_field(self):
        inp = _make_input(region="APAC")
        assert inp.region == "APAC"

    def test_evaluation_period_id_field(self):
        inp = _make_input(evaluation_period_id="Q2-2026")
        assert inp.evaluation_period_id == "Q2-2026"

    def test_quota_attainment_pct_field(self):
        inp = _make_input(quota_attainment_pct=0.75)
        assert inp.quota_attainment_pct == 0.75

    def test_prior_quarter_attainment_pct_field(self):
        inp = _make_input(prior_quarter_attainment_pct=0.90)
        assert inp.prior_quarter_attainment_pct == 0.90

    def test_attainment_variance_pct_field(self):
        inp = _make_input(attainment_variance_pct=0.20)
        assert inp.attainment_variance_pct == 0.20

    def test_pct_quota_achieved_by_month1_end_field(self):
        inp = _make_input(pct_quota_achieved_by_month1_end=0.10)
        assert inp.pct_quota_achieved_by_month1_end == 0.10

    def test_pct_quota_achieved_by_month2_end_field(self):
        inp = _make_input(pct_quota_achieved_by_month2_end=0.55)
        assert inp.pct_quota_achieved_by_month2_end == 0.55

    def test_pct_deals_closed_in_final_2_weeks_pct_field(self):
        inp = _make_input(pct_deals_closed_in_final_2_weeks_pct=0.70)
        assert inp.pct_deals_closed_in_final_2_weeks_pct == 0.70

    def test_avg_monthly_bookings_variance_pct_field(self):
        inp = _make_input(avg_monthly_bookings_variance_pct=0.45)
        assert inp.avg_monthly_bookings_variance_pct == 0.45

    def test_forecast_accuracy_pct_field(self):
        inp = _make_input(forecast_accuracy_pct=0.65)
        assert inp.forecast_accuracy_pct == 0.65

    def test_commit_to_close_rate_pct_field(self):
        inp = _make_input(commit_to_close_rate_pct=0.60)
        assert inp.commit_to_close_rate_pct == 0.60

    def test_pipeline_coverage_ratio_field(self):
        inp = _make_input(pipeline_coverage_ratio=2.5)
        assert inp.pipeline_coverage_ratio == 2.5

    def test_avg_deal_size_usd_field(self):
        inp = _make_input(avg_deal_size_usd=100_000.0)
        assert inp.avg_deal_size_usd == 100_000.0

    def test_total_deals_closed_field(self):
        inp = _make_input(total_deals_closed=20)
        assert inp.total_deals_closed == 20

    def test_deals_pushed_to_next_quarter_pct_field(self):
        inp = _make_input(deals_pushed_to_next_quarter_pct=0.40)
        assert inp.deals_pushed_to_next_quarter_pct == 0.40

    def test_discount_rate_avg_pct_field(self):
        inp = _make_input(discount_rate_avg_pct=0.25)
        assert inp.discount_rate_avg_pct == 0.25

    def test_new_logo_pct_field(self):
        inp = _make_input(new_logo_pct=0.05)
        assert inp.new_logo_pct == 0.05

    def test_expansion_revenue_pct_field(self):
        inp = _make_input(expansion_revenue_pct=0.50)
        assert inp.expansion_revenue_pct == 0.50

    def test_avg_sales_cycle_days_field(self):
        inp = _make_input(avg_sales_cycle_days=90.0)
        assert inp.avg_sales_cycle_days == 90.0

    def test_quarters_above_quota_last_4_field(self):
        inp = _make_input(quarters_above_quota_last_4=2)
        assert inp.quarters_above_quota_last_4 == 2

    def test_avg_opportunity_value_usd_field(self):
        inp = _make_input(avg_opportunity_value_usd=75_000.0)
        assert inp.avg_opportunity_value_usd == 75_000.0

    def test_total_field_count(self):
        import dataclasses
        assert len(dataclasses.fields(QuotaInput)) == 22


# ===========================================================================
# 3. QuotaResult – fields and to_dict
# ===========================================================================

class TestQuotaResultFields:
    def _make_result(self) -> QuotaResult:
        return QuotaResult(
            rep_id="R1",
            region="NA",
            quota_risk=QuotaRisk.low,
            quota_pattern=QuotaPattern.none,
            quota_severity=QuotaSeverity.disciplined,
            recommended_action=QuotaAction.no_action,
            pacing_score=5.0,
            consistency_score=3.0,
            forecast_score=2.0,
            pipeline_health_score=4.0,
            quota_composite=3.0,
            has_quota_gap=False,
            requires_quota_coaching=False,
            estimated_revenue_at_risk_usd=0.0,
            quota_signal="Quota attainment healthy — pacing, consistency, and forecast accuracy within benchmarks",
        )

    def test_rep_id(self):
        r = self._make_result()
        assert r.rep_id == "R1"

    def test_region(self):
        r = self._make_result()
        assert r.region == "NA"

    def test_quota_risk(self):
        r = self._make_result()
        assert r.quota_risk == QuotaRisk.low

    def test_quota_pattern(self):
        r = self._make_result()
        assert r.quota_pattern == QuotaPattern.none

    def test_quota_severity(self):
        r = self._make_result()
        assert r.quota_severity == QuotaSeverity.disciplined

    def test_recommended_action(self):
        r = self._make_result()
        assert r.recommended_action == QuotaAction.no_action

    def test_pacing_score(self):
        r = self._make_result()
        assert r.pacing_score == 5.0

    def test_consistency_score(self):
        r = self._make_result()
        assert r.consistency_score == 3.0

    def test_forecast_score(self):
        r = self._make_result()
        assert r.forecast_score == 2.0

    def test_pipeline_health_score(self):
        r = self._make_result()
        assert r.pipeline_health_score == 4.0

    def test_quota_composite(self):
        r = self._make_result()
        assert r.quota_composite == 3.0

    def test_has_quota_gap(self):
        r = self._make_result()
        assert r.has_quota_gap is False

    def test_requires_quota_coaching(self):
        r = self._make_result()
        assert r.requires_quota_coaching is False

    def test_estimated_revenue_at_risk_usd(self):
        r = self._make_result()
        assert r.estimated_revenue_at_risk_usd == 0.0

    def test_quota_signal(self):
        r = self._make_result()
        assert "healthy" in r.quota_signal

    def test_to_dict_returns_15_keys(self):
        r = self._make_result()
        d = r.to_dict()
        assert len(d) == 15

    def test_to_dict_key_rep_id(self):
        r = self._make_result()
        assert "rep_id" in r.to_dict()

    def test_to_dict_key_region(self):
        r = self._make_result()
        assert "region" in r.to_dict()

    def test_to_dict_key_quota_risk(self):
        r = self._make_result()
        assert "quota_risk" in r.to_dict()

    def test_to_dict_key_quota_pattern(self):
        r = self._make_result()
        assert "quota_pattern" in r.to_dict()

    def test_to_dict_key_quota_severity(self):
        r = self._make_result()
        assert "quota_severity" in r.to_dict()

    def test_to_dict_key_recommended_action(self):
        r = self._make_result()
        assert "recommended_action" in r.to_dict()

    def test_to_dict_key_pacing_score(self):
        r = self._make_result()
        assert "pacing_score" in r.to_dict()

    def test_to_dict_key_consistency_score(self):
        r = self._make_result()
        assert "consistency_score" in r.to_dict()

    def test_to_dict_key_forecast_score(self):
        r = self._make_result()
        assert "forecast_score" in r.to_dict()

    def test_to_dict_key_pipeline_health_score(self):
        r = self._make_result()
        assert "pipeline_health_score" in r.to_dict()

    def test_to_dict_key_quota_composite(self):
        r = self._make_result()
        assert "quota_composite" in r.to_dict()

    def test_to_dict_key_has_quota_gap(self):
        r = self._make_result()
        assert "has_quota_gap" in r.to_dict()

    def test_to_dict_key_requires_quota_coaching(self):
        r = self._make_result()
        assert "requires_quota_coaching" in r.to_dict()

    def test_to_dict_key_estimated_revenue_at_risk_usd(self):
        r = self._make_result()
        assert "estimated_revenue_at_risk_usd" in r.to_dict()

    def test_to_dict_key_quota_signal(self):
        r = self._make_result()
        assert "quota_signal" in r.to_dict()

    def test_to_dict_enum_values_are_strings(self):
        r = self._make_result()
        d = r.to_dict()
        assert isinstance(d["quota_risk"], str)
        assert isinstance(d["quota_pattern"], str)
        assert isinstance(d["quota_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_values_match(self):
        r = self._make_result()
        d = r.to_dict()
        assert d["rep_id"] == "R1"
        assert d["quota_risk"] == "low"
        assert d["quota_pattern"] == "none"


# ===========================================================================
# 4. _pacing_score branches
# ===========================================================================

class TestPacingScore:
    def _score(self, **overrides) -> float:
        engine = _engine()
        inp = _make_input(**overrides)
        return engine._pacing_score(inp)

    # pct_deals_closed_in_final_2_weeks_pct branches
    def test_final_2_weeks_zero_adds_nothing(self):
        s = self._score(pct_deals_closed_in_final_2_weeks_pct=0.0)
        assert s == pytest.approx(0.0, abs=1.0)  # no contribution from this branch

    def test_final_2_weeks_exactly_025_adds_8(self):
        # Only the >=0.25 branch fires (no month1 or pushed deals contribution)
        s = self._score(
            pct_deals_closed_in_final_2_weeks_pct=0.25,
            pct_quota_achieved_by_month1_end=0.50,  # no month1 contribution
            deals_pushed_to_next_quarter_pct=0.05,  # no pushed contribution
        )
        assert s == pytest.approx(8.0)

    def test_final_2_weeks_above_040_adds_22(self):
        s = self._score(
            pct_deals_closed_in_final_2_weeks_pct=0.40,
            pct_quota_achieved_by_month1_end=0.50,
            deals_pushed_to_next_quarter_pct=0.05,
        )
        assert s == pytest.approx(22.0)

    def test_final_2_weeks_above_060_adds_40(self):
        s = self._score(
            pct_deals_closed_in_final_2_weeks_pct=0.60,
            pct_quota_achieved_by_month1_end=0.50,
            deals_pushed_to_next_quarter_pct=0.05,
        )
        assert s == pytest.approx(40.0)

    def test_final_2_weeks_below_025_adds_0(self):
        s = self._score(
            pct_deals_closed_in_final_2_weeks_pct=0.10,
            pct_quota_achieved_by_month1_end=0.50,
            deals_pushed_to_next_quarter_pct=0.05,
        )
        assert s == pytest.approx(0.0)

    # pct_quota_achieved_by_month1_end branches
    def test_month1_015_or_less_adds_35(self):
        s = self._score(
            pct_deals_closed_in_final_2_weeks_pct=0.0,
            pct_quota_achieved_by_month1_end=0.15,
            deals_pushed_to_next_quarter_pct=0.05,
        )
        assert s == pytest.approx(35.0)

    def test_month1_exactly_015_adds_35(self):
        s = self._score(
            pct_deals_closed_in_final_2_weeks_pct=0.0,
            pct_quota_achieved_by_month1_end=0.15,
            deals_pushed_to_next_quarter_pct=0.05,
        )
        assert s == pytest.approx(35.0)

    def test_month1_between_015_030_adds_18(self):
        s = self._score(
            pct_deals_closed_in_final_2_weeks_pct=0.0,
            pct_quota_achieved_by_month1_end=0.20,
            deals_pushed_to_next_quarter_pct=0.05,
        )
        assert s == pytest.approx(18.0)

    def test_month1_exactly_030_adds_18(self):
        s = self._score(
            pct_deals_closed_in_final_2_weeks_pct=0.0,
            pct_quota_achieved_by_month1_end=0.30,
            deals_pushed_to_next_quarter_pct=0.05,
        )
        assert s == pytest.approx(18.0)

    def test_month1_above_030_adds_0(self):
        s = self._score(
            pct_deals_closed_in_final_2_weeks_pct=0.0,
            pct_quota_achieved_by_month1_end=0.50,
            deals_pushed_to_next_quarter_pct=0.05,
        )
        assert s == pytest.approx(0.0)

    # deals_pushed_to_next_quarter_pct branches
    def test_pushed_above_035_adds_25(self):
        s = self._score(
            pct_deals_closed_in_final_2_weeks_pct=0.0,
            pct_quota_achieved_by_month1_end=0.50,
            deals_pushed_to_next_quarter_pct=0.35,
        )
        assert s == pytest.approx(25.0)

    def test_pushed_between_020_035_adds_12(self):
        s = self._score(
            pct_deals_closed_in_final_2_weeks_pct=0.0,
            pct_quota_achieved_by_month1_end=0.50,
            deals_pushed_to_next_quarter_pct=0.25,
        )
        assert s == pytest.approx(12.0)

    def test_pushed_exactly_020_adds_12(self):
        s = self._score(
            pct_deals_closed_in_final_2_weeks_pct=0.0,
            pct_quota_achieved_by_month1_end=0.50,
            deals_pushed_to_next_quarter_pct=0.20,
        )
        assert s == pytest.approx(12.0)

    def test_pushed_below_020_adds_0(self):
        s = self._score(
            pct_deals_closed_in_final_2_weeks_pct=0.0,
            pct_quota_achieved_by_month1_end=0.50,
            deals_pushed_to_next_quarter_pct=0.10,
        )
        assert s == pytest.approx(0.0)

    # Accumulation & cap
    def test_pacing_score_capped_at_100(self):
        s = self._score(
            pct_deals_closed_in_final_2_weeks_pct=1.0,   # +40
            pct_quota_achieved_by_month1_end=0.0,         # +35
            deals_pushed_to_next_quarter_pct=1.0,         # +25
        )
        assert s == pytest.approx(100.0)

    def test_pacing_score_accumulates_all_three(self):
        s = self._score(
            pct_deals_closed_in_final_2_weeks_pct=0.50,  # +22
            pct_quota_achieved_by_month1_end=0.25,        # +18
            deals_pushed_to_next_quarter_pct=0.25,        # +12
        )
        assert s == pytest.approx(52.0)

    def test_pacing_score_non_negative(self):
        s = self._score(
            pct_deals_closed_in_final_2_weeks_pct=0.0,
            pct_quota_achieved_by_month1_end=1.0,
            deals_pushed_to_next_quarter_pct=0.0,
        )
        assert s >= 0.0


# ===========================================================================
# 5. _consistency_score branches
# ===========================================================================

class TestConsistencyScore:
    def _score(self, **overrides) -> float:
        engine = _engine()
        inp = _make_input(**overrides)
        return engine._consistency_score(inp)

    # attainment_variance_pct branches
    def test_variance_above_050_adds_40(self):
        s = self._score(
            attainment_variance_pct=0.50,
            avg_monthly_bookings_variance_pct=0.0,
            quarters_above_quota_last_4=4,
        )
        assert s == pytest.approx(40.0)

    def test_variance_between_030_050_adds_22(self):
        s = self._score(
            attainment_variance_pct=0.40,
            avg_monthly_bookings_variance_pct=0.0,
            quarters_above_quota_last_4=4,
        )
        assert s == pytest.approx(22.0)

    def test_variance_exactly_030_adds_22(self):
        s = self._score(
            attainment_variance_pct=0.30,
            avg_monthly_bookings_variance_pct=0.0,
            quarters_above_quota_last_4=4,
        )
        assert s == pytest.approx(22.0)

    def test_variance_between_015_030_adds_8(self):
        s = self._score(
            attainment_variance_pct=0.20,
            avg_monthly_bookings_variance_pct=0.0,
            quarters_above_quota_last_4=4,
        )
        assert s == pytest.approx(8.0)

    def test_variance_exactly_015_adds_8(self):
        s = self._score(
            attainment_variance_pct=0.15,
            avg_monthly_bookings_variance_pct=0.0,
            quarters_above_quota_last_4=4,
        )
        assert s == pytest.approx(8.0)

    def test_variance_below_015_adds_0(self):
        s = self._score(
            attainment_variance_pct=0.05,
            avg_monthly_bookings_variance_pct=0.0,
            quarters_above_quota_last_4=4,
        )
        assert s == pytest.approx(0.0)

    # avg_monthly_bookings_variance_pct branches
    def test_monthly_variance_above_060_adds_35(self):
        s = self._score(
            attainment_variance_pct=0.0,
            avg_monthly_bookings_variance_pct=0.60,
            quarters_above_quota_last_4=4,
        )
        assert s == pytest.approx(35.0)

    def test_monthly_variance_between_035_060_adds_18(self):
        s = self._score(
            attainment_variance_pct=0.0,
            avg_monthly_bookings_variance_pct=0.50,
            quarters_above_quota_last_4=4,
        )
        assert s == pytest.approx(18.0)

    def test_monthly_variance_exactly_035_adds_18(self):
        s = self._score(
            attainment_variance_pct=0.0,
            avg_monthly_bookings_variance_pct=0.35,
            quarters_above_quota_last_4=4,
        )
        assert s == pytest.approx(18.0)

    def test_monthly_variance_below_035_adds_0(self):
        s = self._score(
            attainment_variance_pct=0.0,
            avg_monthly_bookings_variance_pct=0.10,
            quarters_above_quota_last_4=4,
        )
        assert s == pytest.approx(0.0)

    # quarters_above_quota_last_4 branches
    def test_quarters_1_adds_25(self):
        s = self._score(
            attainment_variance_pct=0.0,
            avg_monthly_bookings_variance_pct=0.0,
            quarters_above_quota_last_4=1,
        )
        assert s == pytest.approx(25.0)

    def test_quarters_0_adds_25(self):
        s = self._score(
            attainment_variance_pct=0.0,
            avg_monthly_bookings_variance_pct=0.0,
            quarters_above_quota_last_4=0,
        )
        assert s == pytest.approx(25.0)

    def test_quarters_2_adds_12(self):
        s = self._score(
            attainment_variance_pct=0.0,
            avg_monthly_bookings_variance_pct=0.0,
            quarters_above_quota_last_4=2,
        )
        assert s == pytest.approx(12.0)

    def test_quarters_3_adds_0(self):
        s = self._score(
            attainment_variance_pct=0.0,
            avg_monthly_bookings_variance_pct=0.0,
            quarters_above_quota_last_4=3,
        )
        assert s == pytest.approx(0.0)

    def test_quarters_4_adds_0(self):
        s = self._score(
            attainment_variance_pct=0.0,
            avg_monthly_bookings_variance_pct=0.0,
            quarters_above_quota_last_4=4,
        )
        assert s == pytest.approx(0.0)

    def test_consistency_score_capped_at_100(self):
        s = self._score(
            attainment_variance_pct=1.0,      # +40
            avg_monthly_bookings_variance_pct=1.0,  # +35
            quarters_above_quota_last_4=0,    # +25
        )
        assert s == pytest.approx(100.0)

    def test_consistency_score_accumulates(self):
        s = self._score(
            attainment_variance_pct=0.30,     # +22
            avg_monthly_bookings_variance_pct=0.35,  # +18
            quarters_above_quota_last_4=2,    # +12
        )
        assert s == pytest.approx(52.0)


# ===========================================================================
# 6. _forecast_score branches
# ===========================================================================

class TestForecastScore:
    def _score(self, **overrides) -> float:
        engine = _engine()
        inp = _make_input(**overrides)
        return engine._forecast_score(inp)

    # forecast_accuracy_pct branches
    def test_forecast_accuracy_above_085_adds_0(self):
        s = self._score(
            forecast_accuracy_pct=0.90,
            commit_to_close_rate_pct=1.0,
            prior_quarter_attainment_pct=1.10,
        )
        assert s == pytest.approx(0.0)

    def test_forecast_accuracy_exactly_085_adds_8(self):
        s = self._score(
            forecast_accuracy_pct=0.85,
            commit_to_close_rate_pct=1.0,
            prior_quarter_attainment_pct=1.10,
        )
        assert s == pytest.approx(8.0)

    def test_forecast_accuracy_between_075_085_adds_8(self):
        s = self._score(
            forecast_accuracy_pct=0.80,
            commit_to_close_rate_pct=1.0,
            prior_quarter_attainment_pct=1.10,
        )
        assert s == pytest.approx(8.0)

    def test_forecast_accuracy_exactly_075_adds_22(self):
        s = self._score(
            forecast_accuracy_pct=0.75,
            commit_to_close_rate_pct=1.0,
            prior_quarter_attainment_pct=1.10,
        )
        assert s == pytest.approx(22.0)

    def test_forecast_accuracy_between_060_075_adds_22(self):
        s = self._score(
            forecast_accuracy_pct=0.70,
            commit_to_close_rate_pct=1.0,
            prior_quarter_attainment_pct=1.10,
        )
        assert s == pytest.approx(22.0)

    def test_forecast_accuracy_exactly_060_adds_40(self):
        s = self._score(
            forecast_accuracy_pct=0.60,
            commit_to_close_rate_pct=1.0,
            prior_quarter_attainment_pct=1.10,
        )
        assert s == pytest.approx(40.0)

    def test_forecast_accuracy_below_060_adds_40(self):
        s = self._score(
            forecast_accuracy_pct=0.50,
            commit_to_close_rate_pct=1.0,
            prior_quarter_attainment_pct=1.10,
        )
        assert s == pytest.approx(40.0)

    # commit_to_close_rate_pct branches
    def test_commit_above_070_adds_0(self):
        s = self._score(
            forecast_accuracy_pct=0.90,
            commit_to_close_rate_pct=0.80,
            prior_quarter_attainment_pct=1.10,
        )
        assert s == pytest.approx(0.0)

    def test_commit_exactly_070_adds_18(self):
        s = self._score(
            forecast_accuracy_pct=0.90,
            commit_to_close_rate_pct=0.70,
            prior_quarter_attainment_pct=1.10,
        )
        assert s == pytest.approx(18.0)

    def test_commit_between_050_070_adds_18(self):
        s = self._score(
            forecast_accuracy_pct=0.90,
            commit_to_close_rate_pct=0.60,
            prior_quarter_attainment_pct=1.10,
        )
        assert s == pytest.approx(18.0)

    def test_commit_exactly_050_adds_35(self):
        s = self._score(
            forecast_accuracy_pct=0.90,
            commit_to_close_rate_pct=0.50,
            prior_quarter_attainment_pct=1.10,
        )
        assert s == pytest.approx(35.0)

    def test_commit_below_050_adds_35(self):
        s = self._score(
            forecast_accuracy_pct=0.90,
            commit_to_close_rate_pct=0.30,
            prior_quarter_attainment_pct=1.10,
        )
        assert s == pytest.approx(35.0)

    # prior_quarter_attainment_pct branches
    def test_prior_above_100_adds_0(self):
        s = self._score(
            forecast_accuracy_pct=0.90,
            commit_to_close_rate_pct=1.0,
            prior_quarter_attainment_pct=1.10,
        )
        assert s == pytest.approx(0.0)

    def test_prior_exactly_100_adds_0(self):
        # Not < 1.00 and not < 0.80, so 0
        s = self._score(
            forecast_accuracy_pct=0.90,
            commit_to_close_rate_pct=1.0,
            prior_quarter_attainment_pct=1.00,
        )
        assert s == pytest.approx(0.0)

    def test_prior_between_080_100_adds_12(self):
        s = self._score(
            forecast_accuracy_pct=0.90,
            commit_to_close_rate_pct=1.0,
            prior_quarter_attainment_pct=0.90,
        )
        assert s == pytest.approx(12.0)

    def test_prior_below_080_adds_25(self):
        s = self._score(
            forecast_accuracy_pct=0.90,
            commit_to_close_rate_pct=1.0,
            prior_quarter_attainment_pct=0.70,
        )
        assert s == pytest.approx(25.0)

    def test_forecast_score_capped_at_100(self):
        s = self._score(
            forecast_accuracy_pct=0.0,    # +40
            commit_to_close_rate_pct=0.0, # +35
            prior_quarter_attainment_pct=0.0,  # +25
        )
        assert s == pytest.approx(100.0)

    def test_forecast_score_accumulates(self):
        s = self._score(
            forecast_accuracy_pct=0.75,   # +22
            commit_to_close_rate_pct=0.60, # +18
            prior_quarter_attainment_pct=0.90,  # +12
        )
        assert s == pytest.approx(52.0)


# ===========================================================================
# 7. _pipeline_health_score branches
# ===========================================================================

class TestPipelineHealthScore:
    def _score(self, **overrides) -> float:
        engine = _engine()
        inp = _make_input(**overrides)
        return engine._pipeline_health_score(inp)

    # pipeline_coverage_ratio branches
    def test_coverage_above_4_adds_0(self):
        s = self._score(
            pipeline_coverage_ratio=5.0,
            discount_rate_avg_pct=0.0,
            new_logo_pct=0.50,
        )
        assert s == pytest.approx(0.0)

    def test_coverage_exactly_4_adds_10(self):
        s = self._score(
            pipeline_coverage_ratio=4.0,
            discount_rate_avg_pct=0.0,
            new_logo_pct=0.50,
        )
        assert s == pytest.approx(10.0)

    def test_coverage_between_3_4_adds_10(self):
        s = self._score(
            pipeline_coverage_ratio=3.5,
            discount_rate_avg_pct=0.0,
            new_logo_pct=0.50,
        )
        assert s == pytest.approx(10.0)

    def test_coverage_exactly_3_adds_25(self):
        s = self._score(
            pipeline_coverage_ratio=3.0,
            discount_rate_avg_pct=0.0,
            new_logo_pct=0.50,
        )
        assert s == pytest.approx(25.0)

    def test_coverage_between_2_3_adds_25(self):
        s = self._score(
            pipeline_coverage_ratio=2.5,
            discount_rate_avg_pct=0.0,
            new_logo_pct=0.50,
        )
        assert s == pytest.approx(25.0)

    def test_coverage_exactly_2_adds_45(self):
        s = self._score(
            pipeline_coverage_ratio=2.0,
            discount_rate_avg_pct=0.0,
            new_logo_pct=0.50,
        )
        assert s == pytest.approx(45.0)

    def test_coverage_below_2_adds_45(self):
        s = self._score(
            pipeline_coverage_ratio=1.0,
            discount_rate_avg_pct=0.0,
            new_logo_pct=0.50,
        )
        assert s == pytest.approx(45.0)

    # discount_rate_avg_pct branches
    def test_discount_above_030_adds_30(self):
        s = self._score(
            pipeline_coverage_ratio=5.0,
            discount_rate_avg_pct=0.30,
            new_logo_pct=0.50,
        )
        assert s == pytest.approx(30.0)

    def test_discount_above_030_strictly(self):
        s = self._score(
            pipeline_coverage_ratio=5.0,
            discount_rate_avg_pct=0.40,
            new_logo_pct=0.50,
        )
        assert s == pytest.approx(30.0)

    def test_discount_exactly_020_adds_15(self):
        s = self._score(
            pipeline_coverage_ratio=5.0,
            discount_rate_avg_pct=0.20,
            new_logo_pct=0.50,
        )
        assert s == pytest.approx(15.0)

    def test_discount_between_020_030_adds_15(self):
        s = self._score(
            pipeline_coverage_ratio=5.0,
            discount_rate_avg_pct=0.25,
            new_logo_pct=0.50,
        )
        assert s == pytest.approx(15.0)

    def test_discount_below_020_adds_0(self):
        s = self._score(
            pipeline_coverage_ratio=5.0,
            discount_rate_avg_pct=0.10,
            new_logo_pct=0.50,
        )
        assert s == pytest.approx(0.0)

    # new_logo_pct branches
    def test_new_logo_above_025_adds_0(self):
        s = self._score(
            pipeline_coverage_ratio=5.0,
            discount_rate_avg_pct=0.0,
            new_logo_pct=0.40,
        )
        assert s == pytest.approx(0.0)

    def test_new_logo_exactly_025_adds_12(self):
        s = self._score(
            pipeline_coverage_ratio=5.0,
            discount_rate_avg_pct=0.0,
            new_logo_pct=0.25,
        )
        assert s == pytest.approx(12.0)

    def test_new_logo_between_010_025_adds_12(self):
        s = self._score(
            pipeline_coverage_ratio=5.0,
            discount_rate_avg_pct=0.0,
            new_logo_pct=0.15,
        )
        assert s == pytest.approx(12.0)

    def test_new_logo_exactly_010_adds_25(self):
        s = self._score(
            pipeline_coverage_ratio=5.0,
            discount_rate_avg_pct=0.0,
            new_logo_pct=0.10,
        )
        assert s == pytest.approx(25.0)

    def test_new_logo_below_010_adds_25(self):
        s = self._score(
            pipeline_coverage_ratio=5.0,
            discount_rate_avg_pct=0.0,
            new_logo_pct=0.05,
        )
        assert s == pytest.approx(25.0)

    def test_pipeline_health_score_capped_at_100(self):
        s = self._score(
            pipeline_coverage_ratio=1.0,   # +45
            discount_rate_avg_pct=0.50,    # +30
            new_logo_pct=0.0,             # +25
        )
        assert s == pytest.approx(100.0)

    def test_pipeline_health_score_accumulates(self):
        s = self._score(
            pipeline_coverage_ratio=2.5,   # +25
            discount_rate_avg_pct=0.25,    # +15
            new_logo_pct=0.15,            # +12
        )
        assert s == pytest.approx(52.0)


# ===========================================================================
# 8. Composite score calculation
# ===========================================================================

class TestCompositeScore:
    def test_all_zero_sub_scores_gives_zero_composite(self):
        engine = _engine()
        inp = _make_input(
            pct_deals_closed_in_final_2_weeks_pct=0.0,
            pct_quota_achieved_by_month1_end=0.50,
            deals_pushed_to_next_quarter_pct=0.0,
            attainment_variance_pct=0.0,
            avg_monthly_bookings_variance_pct=0.0,
            quarters_above_quota_last_4=4,
            forecast_accuracy_pct=0.90,
            commit_to_close_rate_pct=1.0,
            prior_quarter_attainment_pct=1.10,
            pipeline_coverage_ratio=5.0,
            discount_rate_avg_pct=0.0,
            new_logo_pct=0.50,
        )
        result = engine.assess(inp)
        assert result.quota_composite == pytest.approx(0.0)

    def test_composite_weights_are_applied(self):
        engine = _engine()
        # Craft exact sub-scores: pacing=40, consistency=0, forecast=0, pipeline=0
        inp = _make_input(
            pct_deals_closed_in_final_2_weeks_pct=0.60,  # +40 pacing
            pct_quota_achieved_by_month1_end=0.50,       # no pacing contribution
            deals_pushed_to_next_quarter_pct=0.0,        # no pacing
            attainment_variance_pct=0.0,
            avg_monthly_bookings_variance_pct=0.0,
            quarters_above_quota_last_4=4,
            forecast_accuracy_pct=0.90,
            commit_to_close_rate_pct=1.0,
            prior_quarter_attainment_pct=1.10,
            pipeline_coverage_ratio=5.0,
            discount_rate_avg_pct=0.0,
            new_logo_pct=0.50,
        )
        result = engine.assess(inp)
        # pacing=40, others≈0 → composite ≈ 40 * 0.30 = 12.0
        assert result.pacing_score == pytest.approx(40.0)
        assert result.quota_composite == pytest.approx(12.0)

    def test_composite_capped_at_100(self):
        engine = _engine()
        inp = _make_input(
            pct_deals_closed_in_final_2_weeks_pct=1.0,
            pct_quota_achieved_by_month1_end=0.0,
            deals_pushed_to_next_quarter_pct=1.0,
            attainment_variance_pct=1.0,
            avg_monthly_bookings_variance_pct=1.0,
            quarters_above_quota_last_4=0,
            forecast_accuracy_pct=0.0,
            commit_to_close_rate_pct=0.0,
            prior_quarter_attainment_pct=0.0,
            pipeline_coverage_ratio=1.0,
            discount_rate_avg_pct=1.0,
            new_logo_pct=0.0,
        )
        result = engine.assess(inp)
        assert result.quota_composite <= 100.0


# ===========================================================================
# 9. Pattern Detection – priority order
# ===========================================================================

class TestPatternDetection:
    def _detect(self, **overrides) -> QuotaPattern:
        engine = _engine()
        inp = _make_input(**overrides)
        result = engine.assess(inp)
        return result.quota_pattern

    def test_consistent_underperformance_highest_priority(self):
        # quarters_above_quota_last_4<=1 AND high forecast score → triggers first
        # Also set sandbagging conditions, but consistent_underperformance should win
        pattern = self._detect(
            quarters_above_quota_last_4=1,
            forecast_accuracy_pct=0.50,   # low accuracy → high forecast score
            commit_to_close_rate_pct=0.90,  # would trigger sandbagging
            deals_pushed_to_next_quarter_pct=0.35,  # would trigger sandbagging
        )
        assert pattern == QuotaPattern.consistent_underperformance

    def test_consistent_underperformance_requires_quarters_le_1(self):
        # quarters=2 means no consistent_underperformance
        pattern = self._detect(
            quarters_above_quota_last_4=2,
            forecast_accuracy_pct=0.50,
            commit_to_close_rate_pct=1.0,
            deals_pushed_to_next_quarter_pct=0.05,
            avg_monthly_bookings_variance_pct=0.0,
            attainment_variance_pct=0.0,
        )
        assert pattern != QuotaPattern.consistent_underperformance

    def test_consistent_underperformance_requires_forecast_ge_30(self):
        # quarters<=1 but forecast score low (high forecast_accuracy) → no trigger
        pattern = self._detect(
            quarters_above_quota_last_4=1,
            forecast_accuracy_pct=0.95,
            commit_to_close_rate_pct=1.0,
            prior_quarter_attainment_pct=1.05,
            deals_pushed_to_next_quarter_pct=0.05,
        )
        # With quarters=1, consistency_score gets +25 → that doesn't affect forecast_score
        # forecast_accuracy_pct=0.95 → +0; commit=1.0→+0; prior=1.05→+0 → forecast=0
        assert pattern != QuotaPattern.consistent_underperformance

    def test_sandbagging_detected(self):
        pattern = self._detect(
            quarters_above_quota_last_4=4,
            commit_to_close_rate_pct=0.85,
            deals_pushed_to_next_quarter_pct=0.30,
            avg_monthly_bookings_variance_pct=0.0,
            attainment_variance_pct=0.0,
            forecast_accuracy_pct=0.95,
            prior_quarter_attainment_pct=1.10,
        )
        assert pattern == QuotaPattern.sandbagging

    def test_sandbagging_requires_commit_ge_085(self):
        pattern = self._detect(
            quarters_above_quota_last_4=4,
            commit_to_close_rate_pct=0.84,
            deals_pushed_to_next_quarter_pct=0.35,
            avg_monthly_bookings_variance_pct=0.0,
            attainment_variance_pct=0.0,
            forecast_accuracy_pct=0.95,
            prior_quarter_attainment_pct=1.10,
        )
        assert pattern != QuotaPattern.sandbagging

    def test_sandbagging_requires_pushed_ge_030(self):
        pattern = self._detect(
            quarters_above_quota_last_4=4,
            commit_to_close_rate_pct=0.90,
            deals_pushed_to_next_quarter_pct=0.29,
            avg_monthly_bookings_variance_pct=0.0,
            attainment_variance_pct=0.0,
            forecast_accuracy_pct=0.95,
            prior_quarter_attainment_pct=1.10,
        )
        assert pattern != QuotaPattern.sandbagging

    def test_feast_or_famine_detected(self):
        pattern = self._detect(
            quarters_above_quota_last_4=4,
            attainment_variance_pct=0.50,   # consistency score >=35
            avg_monthly_bookings_variance_pct=0.60,  # both conditions
            commit_to_close_rate_pct=0.75,
            deals_pushed_to_next_quarter_pct=0.10,
            forecast_accuracy_pct=0.95,
            prior_quarter_attainment_pct=1.10,
        )
        assert pattern == QuotaPattern.feast_or_famine

    def test_feast_or_famine_requires_consistency_ge_35(self):
        # Low consistency score
        pattern = self._detect(
            quarters_above_quota_last_4=4,
            attainment_variance_pct=0.0,
            avg_monthly_bookings_variance_pct=0.60,
            commit_to_close_rate_pct=0.75,
            deals_pushed_to_next_quarter_pct=0.10,
            forecast_accuracy_pct=0.95,
            prior_quarter_attainment_pct=1.10,
        )
        # consistency: 0+35+0=35, monthly=0.60→+35 but attainment=0→+0, quarters=4→+0
        # Consistency=35 which is >=35, and monthly=0.60>=0.50 → feast_or_famine
        # Let me force consistency < 35 by having low everything
        pattern2 = self._detect(
            quarters_above_quota_last_4=4,
            attainment_variance_pct=0.0,
            avg_monthly_bookings_variance_pct=0.10,  # only 0 added → consistency=0
            commit_to_close_rate_pct=0.75,
            deals_pushed_to_next_quarter_pct=0.10,
            forecast_accuracy_pct=0.95,
            prior_quarter_attainment_pct=1.10,
        )
        assert pattern2 != QuotaPattern.feast_or_famine

    def test_feast_or_famine_requires_monthly_variance_ge_050(self):
        pattern = self._detect(
            quarters_above_quota_last_4=4,
            attainment_variance_pct=0.50,
            avg_monthly_bookings_variance_pct=0.49,  # just below 0.50
            commit_to_close_rate_pct=0.75,
            deals_pushed_to_next_quarter_pct=0.10,
            forecast_accuracy_pct=0.95,
            prior_quarter_attainment_pct=1.10,
        )
        assert pattern != QuotaPattern.feast_or_famine

    def test_late_quarter_cliff_detected(self):
        pattern = self._detect(
            quarters_above_quota_last_4=4,
            pct_deals_closed_in_final_2_weeks_pct=0.60,  # pacing score >=30 AND >=0.50
            pct_quota_achieved_by_month1_end=0.50,
            deals_pushed_to_next_quarter_pct=0.05,
            attainment_variance_pct=0.0,
            avg_monthly_bookings_variance_pct=0.0,
            commit_to_close_rate_pct=0.75,
            forecast_accuracy_pct=0.95,
            prior_quarter_attainment_pct=1.10,
        )
        assert pattern == QuotaPattern.late_quarter_cliff

    def test_late_quarter_cliff_requires_final2weeks_ge_050(self):
        pattern = self._detect(
            quarters_above_quota_last_4=4,
            pct_deals_closed_in_final_2_weeks_pct=0.49,
            pct_quota_achieved_by_month1_end=0.50,
            deals_pushed_to_next_quarter_pct=0.05,
            attainment_variance_pct=0.0,
            avg_monthly_bookings_variance_pct=0.0,
            commit_to_close_rate_pct=0.75,
            forecast_accuracy_pct=0.95,
            prior_quarter_attainment_pct=1.10,
        )
        assert pattern != QuotaPattern.late_quarter_cliff

    def test_early_coasting_detected(self):
        pattern = self._detect(
            quarters_above_quota_last_4=4,
            pct_quota_achieved_by_month1_end=0.55,  # >=0.50
            pct_quota_achieved_by_month2_end=0.60,  # <=0.65
            pct_deals_closed_in_final_2_weeks_pct=0.10,  # low pacing
            deals_pushed_to_next_quarter_pct=0.05,
            attainment_variance_pct=0.0,
            avg_monthly_bookings_variance_pct=0.0,
            commit_to_close_rate_pct=0.75,
            forecast_accuracy_pct=0.95,
            prior_quarter_attainment_pct=1.10,
        )
        assert pattern == QuotaPattern.early_coasting

    def test_early_coasting_requires_month1_ge_050(self):
        pattern = self._detect(
            quarters_above_quota_last_4=4,
            pct_quota_achieved_by_month1_end=0.49,
            pct_quota_achieved_by_month2_end=0.60,
            pct_deals_closed_in_final_2_weeks_pct=0.10,
            deals_pushed_to_next_quarter_pct=0.05,
            attainment_variance_pct=0.0,
            avg_monthly_bookings_variance_pct=0.0,
            commit_to_close_rate_pct=0.75,
            forecast_accuracy_pct=0.95,
            prior_quarter_attainment_pct=1.10,
        )
        assert pattern != QuotaPattern.early_coasting

    def test_early_coasting_requires_month2_le_065(self):
        pattern = self._detect(
            quarters_above_quota_last_4=4,
            pct_quota_achieved_by_month1_end=0.55,
            pct_quota_achieved_by_month2_end=0.70,  # > 0.65
            pct_deals_closed_in_final_2_weeks_pct=0.10,
            deals_pushed_to_next_quarter_pct=0.05,
            attainment_variance_pct=0.0,
            avg_monthly_bookings_variance_pct=0.0,
            commit_to_close_rate_pct=0.75,
            forecast_accuracy_pct=0.95,
            prior_quarter_attainment_pct=1.10,
        )
        assert pattern != QuotaPattern.early_coasting

    def test_none_pattern_when_no_conditions_met(self):
        pattern = self._detect()  # baseline = low risk, no patterns
        assert pattern == QuotaPattern.none


# ===========================================================================
# 10. Risk Level Thresholds
# ===========================================================================

class TestRiskLevel:
    def _risk(self, composite: float) -> QuotaRisk:
        engine = _engine()
        return engine._risk_level(composite)

    def test_composite_0_is_low(self):
        assert self._risk(0.0) == QuotaRisk.low

    def test_composite_19_is_low(self):
        assert self._risk(19.9) == QuotaRisk.low

    def test_composite_20_is_moderate(self):
        assert self._risk(20.0) == QuotaRisk.moderate

    def test_composite_39_is_moderate(self):
        assert self._risk(39.9) == QuotaRisk.moderate

    def test_composite_40_is_high(self):
        assert self._risk(40.0) == QuotaRisk.high

    def test_composite_59_is_high(self):
        assert self._risk(59.9) == QuotaRisk.high

    def test_composite_60_is_critical(self):
        assert self._risk(60.0) == QuotaRisk.critical

    def test_composite_100_is_critical(self):
        assert self._risk(100.0) == QuotaRisk.critical


# ===========================================================================
# 11. Severity Thresholds
# ===========================================================================

class TestSeverity:
    def _severity(self, composite: float) -> QuotaSeverity:
        engine = _engine()
        return engine._severity(composite)

    def test_composite_0_is_disciplined(self):
        assert self._severity(0.0) == QuotaSeverity.disciplined

    def test_composite_19_is_disciplined(self):
        assert self._severity(19.9) == QuotaSeverity.disciplined

    def test_composite_20_is_developing(self):
        assert self._severity(20.0) == QuotaSeverity.developing

    def test_composite_39_is_developing(self):
        assert self._severity(39.9) == QuotaSeverity.developing

    def test_composite_40_is_inconsistent(self):
        assert self._severity(40.0) == QuotaSeverity.inconsistent

    def test_composite_59_is_inconsistent(self):
        assert self._severity(59.9) == QuotaSeverity.inconsistent

    def test_composite_60_is_at_risk(self):
        assert self._severity(60.0) == QuotaSeverity.at_risk

    def test_composite_100_is_at_risk(self):
        assert self._severity(100.0) == QuotaSeverity.at_risk


# ===========================================================================
# 12. Action Mapping
# ===========================================================================

class TestActionMapping:
    def _action(self, risk: QuotaRisk, pattern: QuotaPattern) -> QuotaAction:
        engine = _engine()
        return engine._action(risk, pattern)

    def test_critical_consistent_underperformance(self):
        assert self._action(
            QuotaRisk.critical, QuotaPattern.consistent_underperformance
        ) == QuotaAction.performance_improvement_plan

    def test_critical_sandbagging(self):
        assert self._action(
            QuotaRisk.critical, QuotaPattern.sandbagging
        ) == QuotaAction.forecast_accuracy_training

    def test_critical_feast_or_famine(self):
        assert self._action(
            QuotaRisk.critical, QuotaPattern.feast_or_famine
        ) == QuotaAction.quota_reset_review

    def test_critical_late_quarter_cliff(self):
        assert self._action(
            QuotaRisk.critical, QuotaPattern.late_quarter_cliff
        ) == QuotaAction.quota_reset_review

    def test_critical_early_coasting(self):
        assert self._action(
            QuotaRisk.critical, QuotaPattern.early_coasting
        ) == QuotaAction.quota_reset_review

    def test_critical_none(self):
        assert self._action(
            QuotaRisk.critical, QuotaPattern.none
        ) == QuotaAction.quota_reset_review

    def test_high_feast_or_famine(self):
        assert self._action(
            QuotaRisk.high, QuotaPattern.feast_or_famine
        ) == QuotaAction.activity_rhythm_coaching

    def test_high_late_quarter_cliff(self):
        assert self._action(
            QuotaRisk.high, QuotaPattern.late_quarter_cliff
        ) == QuotaAction.pipeline_pacing_coaching

    def test_high_none(self):
        assert self._action(
            QuotaRisk.high, QuotaPattern.none
        ) == QuotaAction.pipeline_pacing_coaching

    def test_high_sandbagging(self):
        assert self._action(
            QuotaRisk.high, QuotaPattern.sandbagging
        ) == QuotaAction.pipeline_pacing_coaching

    def test_high_consistent_underperformance(self):
        assert self._action(
            QuotaRisk.high, QuotaPattern.consistent_underperformance
        ) == QuotaAction.pipeline_pacing_coaching

    def test_moderate_any_pattern(self):
        assert self._action(
            QuotaRisk.moderate, QuotaPattern.none
        ) == QuotaAction.pipeline_pacing_coaching

    def test_moderate_sandbagging(self):
        assert self._action(
            QuotaRisk.moderate, QuotaPattern.sandbagging
        ) == QuotaAction.pipeline_pacing_coaching

    def test_low_any_pattern(self):
        assert self._action(
            QuotaRisk.low, QuotaPattern.none
        ) == QuotaAction.no_action

    def test_low_feast_or_famine(self):
        assert self._action(
            QuotaRisk.low, QuotaPattern.feast_or_famine
        ) == QuotaAction.no_action


# ===========================================================================
# 13. has_quota_gap flag
# ===========================================================================

class TestHasQuotaGap:
    def _gap(self, composite: float, **overrides) -> bool:
        engine = _engine()
        inp = _make_input(**overrides)
        return engine._has_quota_gap(composite, inp)

    def test_composite_40_triggers_gap(self):
        assert self._gap(40.0) is True

    def test_composite_39_no_composite_trigger(self):
        # Other fields from baseline are fine (quota>=0.80, quarters=4>1)
        assert self._gap(39.9, quota_attainment_pct=0.90, quarters_above_quota_last_4=4) is False

    def test_quota_attainment_below_080_triggers_gap(self):
        assert self._gap(0.0, quota_attainment_pct=0.79) is True

    def test_quota_attainment_exactly_080_no_trigger(self):
        assert self._gap(0.0, quota_attainment_pct=0.80, quarters_above_quota_last_4=4) is False

    def test_quarters_1_triggers_gap(self):
        assert self._gap(0.0, quota_attainment_pct=1.0, quarters_above_quota_last_4=1) is True

    def test_quarters_0_triggers_gap(self):
        assert self._gap(0.0, quota_attainment_pct=1.0, quarters_above_quota_last_4=0) is True

    def test_quarters_2_no_trigger(self):
        assert self._gap(0.0, quota_attainment_pct=1.0, quarters_above_quota_last_4=2) is False

    def test_no_gap_when_all_fine(self):
        assert self._gap(0.0, quota_attainment_pct=1.0, quarters_above_quota_last_4=4) is False

    def test_gap_or_logic_composite_dominates(self):
        # All individually pass but composite is high
        assert self._gap(60.0, quota_attainment_pct=1.0, quarters_above_quota_last_4=4) is True


# ===========================================================================
# 14. requires_quota_coaching flag
# ===========================================================================

class TestRequiresQuotaCoaching:
    def _coach(self, composite: float, **overrides) -> bool:
        engine = _engine()
        inp = _make_input(**overrides)
        return engine._requires_quota_coaching(composite, inp)

    def test_composite_30_triggers_coaching(self):
        assert self._coach(30.0) is True

    def test_composite_29_no_composite_trigger(self):
        assert self._coach(
            29.9,
            forecast_accuracy_pct=0.90,
            deals_pushed_to_next_quarter_pct=0.10,
        ) is False

    def test_forecast_below_075_triggers_coaching(self):
        assert self._coach(0.0, forecast_accuracy_pct=0.74) is True

    def test_forecast_exactly_075_no_trigger(self):
        assert self._coach(
            0.0,
            forecast_accuracy_pct=0.75,
            deals_pushed_to_next_quarter_pct=0.10,
        ) is False

    def test_pushed_ge_025_triggers_coaching(self):
        assert self._coach(0.0, deals_pushed_to_next_quarter_pct=0.25, forecast_accuracy_pct=0.90) is True

    def test_pushed_below_025_no_trigger(self):
        assert self._coach(
            0.0,
            deals_pushed_to_next_quarter_pct=0.24,
            forecast_accuracy_pct=0.90,
        ) is False

    def test_no_coaching_when_all_fine(self):
        assert self._coach(
            0.0,
            forecast_accuracy_pct=0.95,
            deals_pushed_to_next_quarter_pct=0.05,
        ) is False


# ===========================================================================
# 15. Estimated Revenue at Risk Formula
# ===========================================================================

class TestEstimatedRevenueAtRisk:
    def _revenue(self, total_deals: int, avg_opp_value: float,
                 quota_attainment: float, composite: float) -> float:
        engine = _engine()
        inp = _make_input(
            total_deals_closed=total_deals,
            avg_opportunity_value_usd=avg_opp_value,
            quota_attainment_pct=quota_attainment,
        )
        return engine._estimated_revenue_at_risk(inp, composite)

    def test_zero_composite_gives_zero_revenue(self):
        assert self._revenue(10, 50_000.0, 0.80, 0.0) == pytest.approx(0.0)

    def test_full_attainment_gives_zero_revenue(self):
        assert self._revenue(10, 50_000.0, 1.0, 50.0) == pytest.approx(0.0)

    def test_formula_basic(self):
        # 10 * 50000 * (1 - 0.80) * (50/100) = 10 * 50000 * 0.20 * 0.50 = 50000.0
        result = self._revenue(10, 50_000.0, 0.80, 50.0)
        assert result == pytest.approx(50_000.0)

    def test_formula_rounded_to_2_decimals(self):
        result = self._revenue(3, 33_333.33, 0.80, 50.0)
        expected = round(3 * 33_333.33 * 0.20 * 0.50, 2)
        assert result == pytest.approx(expected)

    def test_zero_deals_gives_zero_revenue(self):
        assert self._revenue(0, 50_000.0, 0.80, 50.0) == pytest.approx(0.0)

    def test_revenue_at_risk_with_over_attainment(self):
        # quota_attainment_pct > 1.0 gives negative revenue
        result = self._revenue(10, 50_000.0, 1.10, 50.0)
        expected = round(10 * 50_000.0 * (1.0 - 1.10) * 0.50, 2)
        assert result == pytest.approx(expected)

    def test_revenue_formula_uses_composite_divided_by_100(self):
        result = self._revenue(5, 100_000.0, 0.50, 100.0)
        expected = round(5 * 100_000.0 * 0.50 * 1.0, 2)
        assert result == pytest.approx(expected)


# ===========================================================================
# 16. Signal String
# ===========================================================================

class TestSignalString:
    def _signal(self, pattern: QuotaPattern, composite: float, **overrides) -> str:
        engine = _engine()
        inp = _make_input(**overrides)
        return engine._signal(inp, pattern, composite)

    def test_healthy_signal_when_none_and_below_20(self):
        s = self._signal(QuotaPattern.none, 15.0)
        assert s == "Quota attainment healthy — pacing, consistency, and forecast accuracy within benchmarks"

    def test_healthy_signal_when_none_and_exactly_0(self):
        s = self._signal(QuotaPattern.none, 0.0)
        assert s == "Quota attainment healthy — pacing, consistency, and forecast accuracy within benchmarks"

    def test_non_healthy_when_none_and_composite_ge_20(self):
        s = self._signal(QuotaPattern.none, 20.0)
        assert "Quota risk" in s or "healthy" not in s

    def test_non_healthy_when_pattern_set_composite_below_20(self):
        s = self._signal(QuotaPattern.sandbagging, 10.0)
        assert "healthy" not in s

    def test_signal_contains_quota_attainment_pct(self):
        s = self._signal(QuotaPattern.sandbagging, 50.0, quota_attainment_pct=0.85)
        assert "85% quota attained" in s

    def test_signal_contains_final_2_weeks(self):
        s = self._signal(QuotaPattern.sandbagging, 50.0,
                         pct_deals_closed_in_final_2_weeks_pct=0.40)
        assert "40% deals in final 2 weeks" in s

    def test_signal_contains_forecast_accuracy(self):
        s = self._signal(QuotaPattern.sandbagging, 50.0,
                         forecast_accuracy_pct=0.88)
        assert "88% forecast accuracy" in s

    def test_signal_contains_composite(self):
        s = self._signal(QuotaPattern.sandbagging, 55.0)
        assert "composite 55" in s

    def test_signal_pattern_label_capitalized(self):
        s = self._signal(QuotaPattern.feast_or_famine, 50.0)
        assert s.startswith("Feast or famine")

    def test_signal_late_quarter_cliff_label(self):
        s = self._signal(QuotaPattern.late_quarter_cliff, 50.0)
        assert s.startswith("Late quarter cliff")

    def test_signal_consistent_underperformance_label(self):
        s = self._signal(QuotaPattern.consistent_underperformance, 50.0)
        assert s.startswith("Consistent underperformance")

    def test_signal_early_coasting_label(self):
        s = self._signal(QuotaPattern.early_coasting, 50.0)
        assert s.startswith("Early coasting")

    def test_signal_none_pattern_with_high_composite_uses_quota_risk(self):
        s = self._signal(QuotaPattern.none, 50.0)
        assert s.startswith("Quota risk")

    def test_signal_separators_present(self):
        s = self._signal(QuotaPattern.sandbagging, 50.0)
        assert s.count(" — ") >= 3


# ===========================================================================
# 17. End-to-end assess() Tests
# ===========================================================================

class TestAssessEndToEnd:
    def test_returns_quota_result_instance(self):
        engine = _engine()
        inp = _make_input()
        result = engine.assess(inp)
        assert isinstance(result, QuotaResult)

    def test_result_rep_id_propagated(self):
        engine = _engine()
        inp = _make_input(rep_id="SALES-42")
        result = engine.assess(inp)
        assert result.rep_id == "SALES-42"

    def test_result_region_propagated(self):
        engine = _engine()
        inp = _make_input(region="LATAM")
        result = engine.assess(inp)
        assert result.region == "LATAM"

    def test_low_risk_baseline(self):
        engine = _engine()
        result = engine.assess(_make_input())
        assert result.quota_risk == QuotaRisk.low

    def test_low_severity_baseline(self):
        engine = _engine()
        result = engine.assess(_make_input())
        assert result.quota_severity == QuotaSeverity.disciplined

    def test_no_action_baseline(self):
        engine = _engine()
        result = engine.assess(_make_input())
        assert result.recommended_action == QuotaAction.no_action

    def test_pacing_score_in_result(self):
        engine = _engine()
        result = engine.assess(_make_input())
        assert isinstance(result.pacing_score, float)

    def test_consistency_score_in_result(self):
        engine = _engine()
        result = engine.assess(_make_input())
        assert isinstance(result.consistency_score, float)

    def test_forecast_score_in_result(self):
        engine = _engine()
        result = engine.assess(_make_input())
        assert isinstance(result.forecast_score, float)

    def test_pipeline_health_score_in_result(self):
        engine = _engine()
        result = engine.assess(_make_input())
        assert isinstance(result.pipeline_health_score, float)

    def test_quota_composite_non_negative(self):
        engine = _engine()
        result = engine.assess(_make_input())
        assert result.quota_composite >= 0.0

    def test_quota_composite_max_100(self):
        engine = _engine()
        inp = _make_input(
            pct_deals_closed_in_final_2_weeks_pct=1.0,
            pct_quota_achieved_by_month1_end=0.0,
            deals_pushed_to_next_quarter_pct=1.0,
            attainment_variance_pct=1.0,
            avg_monthly_bookings_variance_pct=1.0,
            quarters_above_quota_last_4=0,
            forecast_accuracy_pct=0.0,
            commit_to_close_rate_pct=0.0,
            prior_quarter_attainment_pct=0.0,
            pipeline_coverage_ratio=1.0,
            discount_rate_avg_pct=1.0,
            new_logo_pct=0.0,
        )
        result = engine.assess(inp)
        assert result.quota_composite <= 100.0

    def test_stored_in_results_list(self):
        engine = _engine()
        inp = _make_input()
        engine.assess(inp)
        assert len(engine._results) == 1

    def test_multiple_assesses_accumulate(self):
        engine = _engine()
        engine.assess(_make_input(rep_id="A"))
        engine.assess(_make_input(rep_id="B"))
        assert len(engine._results) == 2

    def test_critical_risk_high_all_scores(self):
        engine = _engine()
        inp = _make_input(
            pct_deals_closed_in_final_2_weeks_pct=1.0,
            pct_quota_achieved_by_month1_end=0.0,
            deals_pushed_to_next_quarter_pct=1.0,
            attainment_variance_pct=1.0,
            avg_monthly_bookings_variance_pct=1.0,
            quarters_above_quota_last_4=0,
            forecast_accuracy_pct=0.0,
            commit_to_close_rate_pct=0.0,
            prior_quarter_attainment_pct=0.0,
            pipeline_coverage_ratio=1.0,
            discount_rate_avg_pct=1.0,
            new_logo_pct=0.0,
        )
        result = engine.assess(inp)
        assert result.quota_risk == QuotaRisk.critical
        assert result.quota_severity == QuotaSeverity.at_risk

    def test_has_quota_gap_in_result_is_bool(self):
        engine = _engine()
        result = engine.assess(_make_input())
        assert isinstance(result.has_quota_gap, bool)

    def test_requires_quota_coaching_in_result_is_bool(self):
        engine = _engine()
        result = engine.assess(_make_input())
        assert isinstance(result.requires_quota_coaching, bool)

    def test_estimated_revenue_at_risk_is_float(self):
        engine = _engine()
        result = engine.assess(_make_input())
        assert isinstance(result.estimated_revenue_at_risk_usd, float)

    def test_quota_signal_is_str(self):
        engine = _engine()
        result = engine.assess(_make_input())
        assert isinstance(result.quota_signal, str)

    def test_assess_with_critical_consistent_underperformance(self):
        engine = _engine()
        inp = _make_input(
            quarters_above_quota_last_4=0,
            forecast_accuracy_pct=0.50,
            commit_to_close_rate_pct=0.40,
            prior_quarter_attainment_pct=0.60,
            attainment_variance_pct=0.60,
            avg_monthly_bookings_variance_pct=0.70,
            pipeline_coverage_ratio=1.5,
            discount_rate_avg_pct=0.35,
            new_logo_pct=0.05,
            pct_deals_closed_in_final_2_weeks_pct=0.70,
            pct_quota_achieved_by_month1_end=0.10,
            deals_pushed_to_next_quarter_pct=0.40,
        )
        result = engine.assess(inp)
        assert result.quota_pattern == QuotaPattern.consistent_underperformance
        assert result.recommended_action == QuotaAction.performance_improvement_plan


# ===========================================================================
# 18. assess_batch() Tests
# ===========================================================================

class TestAssessBatch:
    def test_empty_list_returns_empty(self):
        engine = _engine()
        results = engine.assess_batch([])
        assert results == []

    def test_single_item_batch(self):
        engine = _engine()
        results = engine.assess_batch([_make_input(rep_id="X")])
        assert len(results) == 1
        assert results[0].rep_id == "X"

    def test_multiple_items_batch(self):
        engine = _engine()
        inputs = [_make_input(rep_id=f"REP-{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_order_preserved(self):
        engine = _engine()
        inputs = [_make_input(rep_id=f"R{i}") for i in range(3)]
        results = engine.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"R{i}"

    def test_batch_all_added_to_results_list(self):
        engine = _engine()
        engine.assess_batch([_make_input(rep_id=f"R{i}") for i in range(4)])
        assert len(engine._results) == 4

    def test_batch_returns_quota_result_instances(self):
        engine = _engine()
        results = engine.assess_batch([_make_input()])
        assert all(isinstance(r, QuotaResult) for r in results)

    def test_batch_accumulates_with_prior_assess(self):
        engine = _engine()
        engine.assess(_make_input(rep_id="FIRST"))
        engine.assess_batch([_make_input(rep_id="BATCH1"), _make_input(rep_id="BATCH2")])
        assert len(engine._results) == 3

    def test_batch_with_varied_inputs(self):
        engine = _engine()
        inputs = [
            _make_input(rep_id="LOW", quota_attainment_pct=1.10),
            _make_input(
                rep_id="HIGH",
                quarters_above_quota_last_4=0,
                forecast_accuracy_pct=0.50,
            ),
        ]
        results = engine.assess_batch(inputs)
        assert results[0].rep_id == "LOW"
        assert results[1].rep_id == "HIGH"


# ===========================================================================
# 19. summary() Tests – empty
# ===========================================================================

class TestSummaryEmpty:
    def test_empty_summary_total_0(self):
        engine = _engine()
        s = engine.summary()
        assert s["total"] == 0

    def test_empty_summary_returns_13_keys(self):
        engine = _engine()
        s = engine.summary()
        assert len(s) == 13

    def test_empty_summary_risk_counts_empty_dict(self):
        engine = _engine()
        assert engine.summary()["risk_counts"] == {}

    def test_empty_summary_pattern_counts_empty_dict(self):
        engine = _engine()
        assert engine.summary()["pattern_counts"] == {}

    def test_empty_summary_severity_counts_empty_dict(self):
        engine = _engine()
        assert engine.summary()["severity_counts"] == {}

    def test_empty_summary_action_counts_empty_dict(self):
        engine = _engine()
        assert engine.summary()["action_counts"] == {}

    def test_empty_summary_avg_quota_composite_0(self):
        engine = _engine()
        assert engine.summary()["avg_quota_composite"] == 0.0

    def test_empty_summary_quota_gap_count_0(self):
        engine = _engine()
        assert engine.summary()["quota_gap_count"] == 0

    def test_empty_summary_coaching_count_0(self):
        engine = _engine()
        assert engine.summary()["coaching_count"] == 0

    def test_empty_summary_avg_pacing_score_0(self):
        engine = _engine()
        assert engine.summary()["avg_pacing_score"] == 0.0

    def test_empty_summary_avg_consistency_score_0(self):
        engine = _engine()
        assert engine.summary()["avg_consistency_score"] == 0.0

    def test_empty_summary_avg_forecast_score_0(self):
        engine = _engine()
        assert engine.summary()["avg_forecast_score"] == 0.0

    def test_empty_summary_avg_pipeline_health_score_0(self):
        engine = _engine()
        assert engine.summary()["avg_pipeline_health_score"] == 0.0

    def test_empty_summary_total_estimated_revenue_at_risk_0(self):
        engine = _engine()
        assert engine.summary()["total_estimated_revenue_at_risk_usd"] == 0.0


# ===========================================================================
# 20. summary() Tests – populated
# ===========================================================================

class TestSummaryPopulated:
    def _populated_engine(self) -> SalesQuotaAttainmentPatternIntelligenceEngine:
        engine = _engine()
        engine.assess(_make_input(rep_id="A"))
        engine.assess(_make_input(rep_id="B"))
        return engine

    def test_summary_total_correct(self):
        engine = self._populated_engine()
        assert engine.summary()["total"] == 2

    def test_summary_returns_13_keys(self):
        engine = self._populated_engine()
        assert len(engine.summary()) == 13

    def test_summary_key_total(self):
        engine = self._populated_engine()
        assert "total" in engine.summary()

    def test_summary_key_risk_counts(self):
        engine = self._populated_engine()
        assert "risk_counts" in engine.summary()

    def test_summary_key_pattern_counts(self):
        engine = self._populated_engine()
        assert "pattern_counts" in engine.summary()

    def test_summary_key_severity_counts(self):
        engine = self._populated_engine()
        assert "severity_counts" in engine.summary()

    def test_summary_key_action_counts(self):
        engine = self._populated_engine()
        assert "action_counts" in engine.summary()

    def test_summary_key_avg_quota_composite(self):
        engine = self._populated_engine()
        assert "avg_quota_composite" in engine.summary()

    def test_summary_key_quota_gap_count(self):
        engine = self._populated_engine()
        assert "quota_gap_count" in engine.summary()

    def test_summary_key_coaching_count(self):
        engine = self._populated_engine()
        assert "coaching_count" in engine.summary()

    def test_summary_key_avg_pacing_score(self):
        engine = self._populated_engine()
        assert "avg_pacing_score" in engine.summary()

    def test_summary_key_avg_consistency_score(self):
        engine = self._populated_engine()
        assert "avg_consistency_score" in engine.summary()

    def test_summary_key_avg_forecast_score(self):
        engine = self._populated_engine()
        assert "avg_forecast_score" in engine.summary()

    def test_summary_key_avg_pipeline_health_score(self):
        engine = self._populated_engine()
        assert "avg_pipeline_health_score" in engine.summary()

    def test_summary_key_total_estimated_revenue_at_risk_usd(self):
        engine = self._populated_engine()
        assert "total_estimated_revenue_at_risk_usd" in engine.summary()

    def test_summary_risk_counts_dict_non_empty(self):
        engine = self._populated_engine()
        assert len(engine.summary()["risk_counts"]) > 0

    def test_summary_risk_counts_sum_equals_total(self):
        engine = self._populated_engine()
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_pattern_counts_sum_equals_total(self):
        engine = self._populated_engine()
        s = engine.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_summary_severity_counts_sum_equals_total(self):
        engine = self._populated_engine()
        s = engine.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_equals_total(self):
        engine = self._populated_engine()
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_avg_composite_is_float(self):
        engine = self._populated_engine()
        assert isinstance(engine.summary()["avg_quota_composite"], float)

    def test_summary_avg_pacing_is_float(self):
        engine = self._populated_engine()
        assert isinstance(engine.summary()["avg_pacing_score"], float)

    def test_summary_avg_consistency_is_float(self):
        engine = self._populated_engine()
        assert isinstance(engine.summary()["avg_consistency_score"], float)

    def test_summary_avg_forecast_is_float(self):
        engine = self._populated_engine()
        assert isinstance(engine.summary()["avg_forecast_score"], float)

    def test_summary_avg_pipeline_is_float(self):
        engine = self._populated_engine()
        assert isinstance(engine.summary()["avg_pipeline_health_score"], float)

    def test_summary_total_revenue_at_risk_is_float(self):
        engine = self._populated_engine()
        assert isinstance(engine.summary()["total_estimated_revenue_at_risk_usd"], float)

    def test_summary_quota_gap_count_correct(self):
        engine = _engine()
        engine.assess(_make_input(quota_attainment_pct=0.70))  # gap → True
        engine.assess(_make_input(quota_attainment_pct=1.10, quarters_above_quota_last_4=4))  # gap → False
        s = engine.summary()
        assert s["quota_gap_count"] == 1

    def test_summary_coaching_count_correct(self):
        engine = _engine()
        engine.assess(_make_input(forecast_accuracy_pct=0.70))  # coaching → True
        engine.assess(_make_input(forecast_accuracy_pct=0.95, deals_pushed_to_next_quarter_pct=0.05))  # coaching → False
        s = engine.summary()
        assert s["coaching_count"] == 1

    def test_summary_total_revenue_sums(self):
        engine = _engine()
        # Use zero composite => 0 revenue each
        engine.assess(_make_input(
            pct_deals_closed_in_final_2_weeks_pct=0.0,
            pct_quota_achieved_by_month1_end=0.50,
            deals_pushed_to_next_quarter_pct=0.0,
            attainment_variance_pct=0.0,
            avg_monthly_bookings_variance_pct=0.0,
            quarters_above_quota_last_4=4,
            forecast_accuracy_pct=0.90,
            commit_to_close_rate_pct=1.0,
            prior_quarter_attainment_pct=1.10,
            pipeline_coverage_ratio=5.0,
            discount_rate_avg_pct=0.0,
            new_logo_pct=0.50,
        ))
        s = engine.summary()
        assert s["total_estimated_revenue_at_risk_usd"] == pytest.approx(0.0)

    def test_summary_after_batch(self):
        engine = _engine()
        engine.assess_batch([_make_input(rep_id=f"R{i}") for i in range(5)])
        assert engine.summary()["total"] == 5

    def test_summary_avg_composite_makes_sense(self):
        engine = _engine()
        engine.assess(_make_input())
        s = engine.summary()
        assert 0.0 <= s["avg_quota_composite"] <= 100.0


# ===========================================================================
# 21. Edge Cases
# ===========================================================================

class TestEdgeCases:
    def test_quota_attainment_exactly_080_boundary(self):
        engine = _engine()
        result = engine.assess(_make_input(
            quota_attainment_pct=0.80,
            quarters_above_quota_last_4=4,
        ))
        # 0.80 is NOT < 0.80 so no gap from that condition alone
        # composite is 0 and quarters=4 → no gap
        assert result.has_quota_gap is False

    def test_quota_attainment_just_below_080_triggers_gap(self):
        engine = _engine()
        result = engine.assess(_make_input(quota_attainment_pct=0.799, quarters_above_quota_last_4=4))
        assert result.has_quota_gap is True

    def test_pacing_exactly_at_025_boundary(self):
        engine = _engine()
        inp = _make_input(
            pct_deals_closed_in_final_2_weeks_pct=0.25,
            pct_quota_achieved_by_month1_end=0.50,
            deals_pushed_to_next_quarter_pct=0.05,
        )
        assert engine._pacing_score(inp) == pytest.approx(8.0)

    def test_pacing_just_below_025_boundary(self):
        engine = _engine()
        inp = _make_input(
            pct_deals_closed_in_final_2_weeks_pct=0.249,
            pct_quota_achieved_by_month1_end=0.50,
            deals_pushed_to_next_quarter_pct=0.05,
        )
        assert engine._pacing_score(inp) == pytest.approx(0.0)

    def test_pipeline_coverage_exactly_2_boundary(self):
        engine = _engine()
        inp = _make_input(pipeline_coverage_ratio=2.0, discount_rate_avg_pct=0.0, new_logo_pct=0.50)
        assert engine._pipeline_health_score(inp) == pytest.approx(45.0)

    def test_pipeline_coverage_just_above_2_boundary(self):
        engine = _engine()
        inp = _make_input(pipeline_coverage_ratio=2.01, discount_rate_avg_pct=0.0, new_logo_pct=0.50)
        assert engine._pipeline_health_score(inp) == pytest.approx(25.0)

    def test_forecast_exactly_at_085_boundary(self):
        engine = _engine()
        inp = _make_input(
            forecast_accuracy_pct=0.85,
            commit_to_close_rate_pct=1.0,
            prior_quarter_attainment_pct=1.10,
        )
        assert engine._forecast_score(inp) == pytest.approx(8.0)

    def test_forecast_just_above_085_boundary(self):
        engine = _engine()
        inp = _make_input(
            forecast_accuracy_pct=0.86,
            commit_to_close_rate_pct=1.0,
            prior_quarter_attainment_pct=1.10,
        )
        assert engine._forecast_score(inp) == pytest.approx(0.0)

    def test_prior_quarter_exactly_080_adds_12_not_25(self):
        engine = _engine()
        inp = _make_input(
            forecast_accuracy_pct=0.90,
            commit_to_close_rate_pct=1.0,
            prior_quarter_attainment_pct=0.80,
        )
        # 0.80 is NOT < 0.80, but it IS < 1.00 → +12
        assert engine._forecast_score(inp) == pytest.approx(12.0)

    def test_new_engine_has_empty_results(self):
        engine = _engine()
        assert engine._results == []

    def test_each_engine_instance_is_independent(self):
        e1 = _engine()
        e2 = _engine()
        e1.assess(_make_input(rep_id="E1"))
        assert len(e2._results) == 0

    def test_assess_result_type_is_quota_result(self):
        engine = _engine()
        result = engine.assess(_make_input())
        assert type(result).__name__ == "QuotaResult"

    def test_to_dict_with_critical_result(self):
        engine = _engine()
        inp = _make_input(
            quarters_above_quota_last_4=0,
            forecast_accuracy_pct=0.50,
            commit_to_close_rate_pct=0.30,
            prior_quarter_attainment_pct=0.60,
            attainment_variance_pct=0.60,
            avg_monthly_bookings_variance_pct=0.70,
            pipeline_coverage_ratio=1.5,
            pct_deals_closed_in_final_2_weeks_pct=0.70,
            pct_quota_achieved_by_month1_end=0.10,
            deals_pushed_to_next_quarter_pct=0.40,
        )
        result = engine.assess(inp)
        d = result.to_dict()
        assert d["quota_risk"] == "critical"
        assert d["quota_severity"] == "at_risk"

    def test_summary_after_single_assess(self):
        engine = _engine()
        engine.assess(_make_input())
        s = engine.summary()
        assert s["total"] == 1
        assert len(s) == 13

    def test_consistency_score_exactly_35_qualifies_for_feast_or_famine(self):
        # attainment_variance=0.50→+40, monthly=0.0→+0, quarters=4→+0 → consistency=40
        # monthly>=0.50 for feast_or_famine pattern
        engine = _engine()
        inp = _make_input(
            quarters_above_quota_last_4=4,
            attainment_variance_pct=0.50,    # +40 consistency
            avg_monthly_bookings_variance_pct=0.60,  # +35 and >=0.50 condition
            commit_to_close_rate_pct=0.75,
            deals_pushed_to_next_quarter_pct=0.10,
            forecast_accuracy_pct=0.95,
            prior_quarter_attainment_pct=1.10,
            pct_deals_closed_in_final_2_weeks_pct=0.10,
        )
        result = engine.assess(inp)
        assert result.quota_pattern == QuotaPattern.feast_or_famine

    def test_sandbagging_exactly_at_boundary(self):
        engine = _engine()
        inp = _make_input(
            quarters_above_quota_last_4=4,
            commit_to_close_rate_pct=0.85,
            deals_pushed_to_next_quarter_pct=0.30,
            avg_monthly_bookings_variance_pct=0.0,
            attainment_variance_pct=0.0,
            forecast_accuracy_pct=0.95,
            prior_quarter_attainment_pct=1.10,
        )
        result = engine.assess(inp)
        assert result.quota_pattern == QuotaPattern.sandbagging

    def test_revenue_rounded_to_2_decimal_places(self):
        engine = _engine()
        inp = _make_input(
            total_deals_closed=7,
            avg_opportunity_value_usd=33_333.33,
            quota_attainment_pct=0.80,
            pct_deals_closed_in_final_2_weeks_pct=0.60,
            pct_quota_achieved_by_month1_end=0.10,
            deals_pushed_to_next_quarter_pct=0.40,
        )
        result = engine.assess(inp)
        # Revenue should have at most 2 decimal places
        assert round(result.estimated_revenue_at_risk_usd, 2) == result.estimated_revenue_at_risk_usd

    def test_signal_string_format_separators(self):
        engine = _engine()
        inp = _make_input(
            quota_attainment_pct=0.75,
            pct_deals_closed_in_final_2_weeks_pct=0.65,
            forecast_accuracy_pct=0.70,
            quarters_above_quota_last_4=0,
        )
        result = engine.assess(inp)
        assert " — " in result.quota_signal

    def test_composite_weighted_formula_precision(self):
        engine = _engine()
        inp = _make_input(
            pct_deals_closed_in_final_2_weeks_pct=0.60,  # pacing+40
            pct_quota_achieved_by_month1_end=0.50,
            deals_pushed_to_next_quarter_pct=0.05,
            attainment_variance_pct=0.30,  # consistency+22
            avg_monthly_bookings_variance_pct=0.0,
            quarters_above_quota_last_4=4,
            forecast_accuracy_pct=0.85,  # forecast+8
            commit_to_close_rate_pct=1.0,
            prior_quarter_attainment_pct=1.10,
            pipeline_coverage_ratio=5.0,
            discount_rate_avg_pct=0.0,
            new_logo_pct=0.50,
        )
        result = engine.assess(inp)
        # pacing=40, consistency=22, forecast=8, pipeline=0
        # composite = 40*0.30 + 22*0.30 + 8*0.25 + 0*0.15 = 12 + 6.6 + 2 = 20.6
        assert result.pacing_score == pytest.approx(40.0)
        assert result.consistency_score == pytest.approx(22.0)
        assert result.forecast_score == pytest.approx(8.0)
        assert result.pipeline_health_score == pytest.approx(0.0)
        assert result.quota_composite == pytest.approx(20.6)
