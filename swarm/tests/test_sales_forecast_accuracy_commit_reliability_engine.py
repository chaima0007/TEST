"""
Pytest tests for Module 217 — Sales Forecast Accuracy & Commit Reliability Engine.
"""
import pytest
from swarm.intelligence.sales_forecast_accuracy_commit_reliability_engine import (
    ForecastAction,
    ForecastInput,
    ForecastPattern,
    ForecastResult,
    ForecastRisk,
    ForecastSeverity,
    SalesForecastAccuracyCommitReliabilityEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> ForecastInput:
    defaults = dict(
        rep_id="REP-001", region="West", evaluation_period_id="2026-Q1",
        commit_vs_actual_variance_pct=0.05, overcommit_frequency_pct=0.10,
        undercommit_frequency_pct=0.10, forecast_miss_rate_pct=0.10,
        commit_category_accuracy_pct=0.90, best_case_to_close_conversion_pct=0.50,
        pipeline_to_commit_escalation_rate_pct=0.10, category_downgrade_rate_pct=0.05,
        last_week_close_rate_pct=0.10, pull_in_frequency_pct=0.05,
        push_out_frequency_pct=0.10, avg_days_in_commit_before_close=10.0,
        crm_forecast_update_frequency_days=2.0, deal_stage_accuracy_at_commit_pct=0.90,
        close_date_change_frequency=0.5, rolling_3q_forecast_accuracy_pct=0.90,
        upside_capture_rate_pct=0.60, total_commit_deals=10,
        avg_deal_value_usd=50_000.0, quota_attainment_pct=1.0,
    )
    defaults.update(overrides)
    return ForecastInput(**defaults)


def eng() -> SalesForecastAccuracyCommitReliabilityEngine:
    return SalesForecastAccuracyCommitReliabilityEngine()


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class TestEnums:
    def test_forecast_risk_values(self):
        assert {r.value for r in ForecastRisk} == {"low", "moderate", "high", "critical"}

    def test_forecast_pattern_values(self):
        assert {p.value for p in ForecastPattern} == {
            "none", "chronic_overcommit", "sandbagger",
            "commit_drifter", "late_push_abuser", "category_manipulator",
        }

    def test_forecast_severity_values(self):
        assert {s.value for s in ForecastSeverity} == {
            "accurate", "drifting", "unreliable", "blind_spot"
        }

    def test_forecast_action_count_and_values(self):
        assert len(ForecastAction) == 9
        assert {a.value for a in ForecastAction} == {
            "no_action", "forecast_monitoring", "commit_cadence_coaching",
            "pipeline_review_increase", "forecast_hygiene_training",
            "manager_forecast_alignment", "deal_by_deal_review",
            "forecast_process_reset", "executive_forecast_audit",
        }


# ---------------------------------------------------------------------------
# Result structure
# ---------------------------------------------------------------------------

class TestForecastResultStructure:
    def test_to_dict_has_15_keys_with_correct_names(self):
        d = eng().assess(make_input()).to_dict()
        assert set(d) == {
            "rep_id", "region", "forecast_risk", "forecast_pattern",
            "forecast_severity", "recommended_action", "accuracy_score",
            "discipline_score", "timing_score", "reliability_score",
            "forecast_composite", "has_forecast_gap", "requires_manager_review",
            "estimated_forecast_error_usd", "forecast_signal",
        }

    def test_result_passthrough_fields(self):
        r = eng().assess(make_input(rep_id="X", region="North"))
        assert r.rep_id == "X" and r.region == "North"

    def test_result_is_forecast_result_instance(self):
        assert isinstance(eng().assess(make_input()), ForecastResult)


# ---------------------------------------------------------------------------
# Accuracy sub-score (parametrized)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("variance,miss,rolling3q,expected", [
    (0.05, 0.0, 0.80, 0),    # nothing triggered
    (0.10, 0.0, 0.80, 8),    # variance tier 1
    (0.22, 0.0, 0.80, 22),   # variance tier 2
    (0.40, 0.0, 0.80, 40),   # variance tier 3
    (0.0,  0.20, 0.80, 6),   # miss tier 1
    (0.0,  0.40, 0.80, 18),  # miss tier 2
    (0.0,  0.60, 0.80, 35),  # miss tier 3
    (0.0,  0.0,  0.70, 12),  # rolling tier 1
    (0.0,  0.0,  0.55, 25),  # rolling tier 2
    (0.50, 0.70, 0.40, 100), # all max → capped at 100
])
def test_accuracy_score(variance, miss, rolling3q, expected):
    e = eng()
    s = e._accuracy_score(make_input(
        commit_vs_actual_variance_pct=variance,
        forecast_miss_rate_pct=miss,
        rolling_3q_forecast_accuracy_pct=rolling3q,
    ))
    assert s == expected


# ---------------------------------------------------------------------------
# Discipline sub-score (parametrized)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("cat_acc,cat_dg,cdc,expected", [
    (0.90, 0.0, 0.0, 0),    # nothing triggered
    (0.75, 0.0, 0.0, 10),   # cat_acc tier 1
    (0.60, 0.0, 0.0, 25),   # cat_acc tier 2
    (0.40, 0.0, 0.0, 45),   # cat_acc tier 3
    (0.90, 0.20, 0.0, 15),  # downgrade tier 1
    (0.90, 0.35, 0.0, 30),  # downgrade tier 2
    (0.90, 0.0,  2.0, 12),  # cdc tier 1
    (0.90, 0.0,  3.0, 25),  # cdc tier 2
    (0.30, 0.50, 4.0, 100), # all max → capped
])
def test_discipline_score(cat_acc, cat_dg, cdc, expected):
    e = eng()
    s = e._discipline_score(make_input(
        commit_category_accuracy_pct=cat_acc,
        category_downgrade_rate_pct=cat_dg,
        close_date_change_frequency=cdc,
    ))
    assert s == expected


# ---------------------------------------------------------------------------
# Timing sub-score (parametrized)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("lwc,escalation,pushout,expected", [
    (0.10, 0.0,  0.0,  0),   # nothing triggered
    (0.20, 0.0,  0.0,  8),   # lwc tier 1
    (0.35, 0.0,  0.0,  22),  # lwc tier 2
    (0.55, 0.0,  0.0,  40),  # lwc tier 3
    (0.0,  0.25, 0.0,  18),  # escalation tier 1
    (0.0,  0.40, 0.0,  35),  # escalation tier 2
    (0.0,  0.0,  0.28, 12),  # pushout tier 1
    (0.0,  0.0,  0.45, 25),  # pushout tier 2
    (0.80, 0.80, 0.80, 100), # all max → capped
])
def test_timing_score(lwc, escalation, pushout, expected):
    e = eng()
    s = e._timing_score(make_input(
        last_week_close_rate_pct=lwc,
        pipeline_to_commit_escalation_rate_pct=escalation,
        push_out_frequency_pct=pushout,
    ))
    assert s == expected


# ---------------------------------------------------------------------------
# Reliability sub-score (parametrized)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("oc,uc,crm,expected", [
    (0.10, 0.0,  1.0, 0),   # nothing triggered
    (0.22, 0.0,  1.0, 8),   # oc tier 1
    (0.40, 0.0,  1.0, 22),  # oc tier 2
    (0.60, 0.0,  1.0, 40),  # oc tier 3
    (0.0,  0.35, 1.0, 18),  # uc tier 1
    (0.0,  0.55, 1.0, 35),  # uc tier 2
    (0.0,  0.0,  4.0, 12),  # crm tier 1
    (0.0,  0.0,  7.0, 25),  # crm tier 2
    (0.80, 0.80, 10.0, 100), # all max → capped
])
def test_reliability_score(oc, uc, crm, expected):
    e = eng()
    s = e._reliability_score(make_input(
        overcommit_frequency_pct=oc,
        undercommit_frequency_pct=uc,
        crm_forecast_update_frequency_days=crm,
    ))
    assert s == expected


# ---------------------------------------------------------------------------
# Composite
# ---------------------------------------------------------------------------

class TestComposite:
    def test_formula(self):
        e = eng()
        assert e._composite(80, 60, 40, 20) == round(80*0.30 + 60*0.25 + 40*0.25 + 20*0.20, 2)

    def test_capped_at_100(self):
        assert eng()._composite(100, 100, 100, 100) == 100.0

    def test_all_zero(self):
        assert eng()._composite(0, 0, 0, 0) == 0.0


# ---------------------------------------------------------------------------
# Risk and Severity thresholds (parametrized)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("composite,expected_risk", [
    (0.0,  ForecastRisk.low),
    (19.9, ForecastRisk.low),
    (20.0, ForecastRisk.moderate),
    (39.9, ForecastRisk.moderate),
    (40.0, ForecastRisk.high),
    (59.9, ForecastRisk.high),
    (60.0, ForecastRisk.critical),
    (100.0, ForecastRisk.critical),
])
def test_risk_thresholds(composite, expected_risk):
    assert eng()._risk(composite) == expected_risk


@pytest.mark.parametrize("composite,expected_sev", [
    (0.0,  ForecastSeverity.accurate),
    (19.9, ForecastSeverity.accurate),
    (20.0, ForecastSeverity.drifting),
    (39.9, ForecastSeverity.drifting),
    (40.0, ForecastSeverity.unreliable),
    (59.9, ForecastSeverity.unreliable),
    (60.0, ForecastSeverity.blind_spot),
    (100.0, ForecastSeverity.blind_spot),
])
def test_severity_thresholds(composite, expected_sev):
    assert eng()._severity(composite) == expected_sev


# ---------------------------------------------------------------------------
# Pattern detection
# ---------------------------------------------------------------------------

class TestPattern:
    def _pat(self, **kw):
        return eng()._pattern(make_input(**kw))

    def test_chronic_overcommit(self):
        assert self._pat(overcommit_frequency_pct=0.55, commit_vs_actual_variance_pct=0.30) == ForecastPattern.chronic_overcommit

    def test_chronic_overcommit_requires_variance(self):
        assert self._pat(overcommit_frequency_pct=0.55, commit_vs_actual_variance_pct=0.29) != ForecastPattern.chronic_overcommit

    def test_sandbagger(self):
        assert self._pat(undercommit_frequency_pct=0.50, rolling_3q_forecast_accuracy_pct=0.80) == ForecastPattern.sandbagger

    def test_sandbagger_requires_undercommit(self):
        assert self._pat(undercommit_frequency_pct=0.49, rolling_3q_forecast_accuracy_pct=0.80) != ForecastPattern.sandbagger

    def test_commit_drifter(self):
        assert self._pat(push_out_frequency_pct=0.40, close_date_change_frequency=2.5) == ForecastPattern.commit_drifter

    def test_commit_drifter_requires_cdc(self):
        assert self._pat(push_out_frequency_pct=0.40, close_date_change_frequency=2.4) != ForecastPattern.commit_drifter

    def test_late_push_abuser(self):
        assert self._pat(last_week_close_rate_pct=0.50, pipeline_to_commit_escalation_rate_pct=0.35) == ForecastPattern.late_push_abuser

    def test_category_manipulator(self):
        assert self._pat(category_downgrade_rate_pct=0.30, commit_category_accuracy_pct=0.55) == ForecastPattern.category_manipulator

    def test_category_manipulator_boundary(self):
        assert self._pat(category_downgrade_rate_pct=0.30, commit_category_accuracy_pct=0.56) != ForecastPattern.category_manipulator

    def test_pattern_none(self):
        assert self._pat() == ForecastPattern.none

    def test_chronic_overcommit_beats_sandbagger(self):
        p = self._pat(
            overcommit_frequency_pct=0.55, commit_vs_actual_variance_pct=0.30,
            undercommit_frequency_pct=0.50, rolling_3q_forecast_accuracy_pct=0.80,
        )
        assert p == ForecastPattern.chronic_overcommit


# ---------------------------------------------------------------------------
# Action logic (parametrized)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("risk,pat,expected_action", [
    (ForecastRisk.critical, ForecastPattern.chronic_overcommit, ForecastAction.executive_forecast_audit),
    (ForecastRisk.critical, ForecastPattern.sandbagger,         ForecastAction.executive_forecast_audit),
    (ForecastRisk.critical, ForecastPattern.commit_drifter,     ForecastAction.forecast_process_reset),
    (ForecastRisk.critical, ForecastPattern.late_push_abuser,   ForecastAction.forecast_process_reset),
    (ForecastRisk.critical, ForecastPattern.category_manipulator, ForecastAction.forecast_process_reset),
    (ForecastRisk.critical, ForecastPattern.none,               ForecastAction.forecast_process_reset),
    (ForecastRisk.high,     ForecastPattern.chronic_overcommit, ForecastAction.deal_by_deal_review),
    (ForecastRisk.high,     ForecastPattern.sandbagger,         ForecastAction.manager_forecast_alignment),
    (ForecastRisk.high,     ForecastPattern.commit_drifter,     ForecastAction.commit_cadence_coaching),
    (ForecastRisk.high,     ForecastPattern.late_push_abuser,   ForecastAction.pipeline_review_increase),
    (ForecastRisk.high,     ForecastPattern.category_manipulator, ForecastAction.forecast_hygiene_training),
    (ForecastRisk.high,     ForecastPattern.none,               ForecastAction.forecast_monitoring),
    (ForecastRisk.moderate, ForecastPattern.none,               ForecastAction.forecast_monitoring),
    (ForecastRisk.moderate, ForecastPattern.chronic_overcommit, ForecastAction.forecast_monitoring),
    (ForecastRisk.low,      ForecastPattern.none,               ForecastAction.no_action),
])
def test_action_logic(risk, pat, expected_action):
    assert eng()._action(risk, pat) == expected_action


# ---------------------------------------------------------------------------
# Flags
# ---------------------------------------------------------------------------

class TestFlags:
    def test_forecast_gap_true_when_composite_gte_40(self):
        i = make_input(
            commit_vs_actual_variance_pct=0.40, forecast_miss_rate_pct=0.60,
            rolling_3q_forecast_accuracy_pct=0.50, commit_category_accuracy_pct=0.35,
            category_downgrade_rate_pct=0.40, close_date_change_frequency=3.5,
            last_week_close_rate_pct=0.60, pipeline_to_commit_escalation_rate_pct=0.45,
            push_out_frequency_pct=0.50, overcommit_frequency_pct=0.65,
            undercommit_frequency_pct=0.10, crm_forecast_update_frequency_days=8.0,
        )
        r = eng().assess(i)
        assert r.forecast_composite >= 40
        assert r.has_forecast_gap is True

    def test_forecast_gap_true_when_miss_rate_gte_040(self):
        assert eng().assess(make_input(forecast_miss_rate_pct=0.40)).has_forecast_gap is True

    def test_forecast_gap_true_when_rolling_3q_lte_065(self):
        assert eng().assess(make_input(rolling_3q_forecast_accuracy_pct=0.65)).has_forecast_gap is True

    def test_forecast_gap_false_for_clean_rep(self):
        r = eng().assess(make_input(forecast_miss_rate_pct=0.05,
                                    rolling_3q_forecast_accuracy_pct=0.90))
        assert r.forecast_composite < 40
        assert r.has_forecast_gap is False

    def test_requires_manager_review_true_when_variance_gte_020(self):
        assert eng().assess(make_input(commit_vs_actual_variance_pct=0.20)).requires_manager_review is True

    def test_requires_manager_review_true_when_push_out_gte_030(self):
        assert eng().assess(make_input(push_out_frequency_pct=0.30)).requires_manager_review is True

    def test_requires_manager_review_false_for_clean_rep(self):
        assert eng().assess(make_input()).requires_manager_review is False


# ---------------------------------------------------------------------------
# Forecast error estimate
# ---------------------------------------------------------------------------

class TestForecastError:
    def test_calculation_matches_formula(self):
        i = make_input(total_commit_deals=10, avg_deal_value_usd=50_000.0,
                       commit_vs_actual_variance_pct=0.20)
        r = eng().assess(i)
        expected = round(10 * 50_000.0 * 0.20 * (r.forecast_composite / 100), 2)
        assert r.estimated_forecast_error_usd == expected

    def test_rounded_to_2_decimals(self):
        r = eng().assess(make_input(total_commit_deals=7, avg_deal_value_usd=33_333.33,
                                    commit_vs_actual_variance_pct=0.22))
        assert r.estimated_forecast_error_usd == round(r.estimated_forecast_error_usd, 2)


# ---------------------------------------------------------------------------
# Signal
# ---------------------------------------------------------------------------

class TestSignal:
    def test_signal_strong_below_composite_20(self):
        r = eng().assess(make_input())
        assert r.forecast_composite < 20
        assert r.forecast_signal == (
            "Forecast reliability strong — commit accuracy, category discipline, "
            "and timing patterns within benchmark targets"
        )

    def test_signal_chronic_overcommit_label(self):
        i = make_input(overcommit_frequency_pct=0.65, commit_vs_actual_variance_pct=0.50,
                       forecast_miss_rate_pct=0.70, rolling_3q_forecast_accuracy_pct=0.40,
                       commit_category_accuracy_pct=0.35, category_downgrade_rate_pct=0.40,
                       close_date_change_frequency=3.5, last_week_close_rate_pct=0.60,
                       pipeline_to_commit_escalation_rate_pct=0.50, push_out_frequency_pct=0.50,
                       crm_forecast_update_frequency_days=8.0)
        r = eng().assess(i)
        assert "Chronic overcommit" in r.forecast_signal

    def test_signal_contains_variance_miss_rate_3q_composite(self):
        i = make_input(overcommit_frequency_pct=0.65, commit_vs_actual_variance_pct=0.40,
                       forecast_miss_rate_pct=0.60, rolling_3q_forecast_accuracy_pct=0.50,
                       commit_category_accuracy_pct=0.35, category_downgrade_rate_pct=0.40,
                       close_date_change_frequency=3.5, last_week_close_rate_pct=0.60,
                       pipeline_to_commit_escalation_rate_pct=0.50, push_out_frequency_pct=0.50,
                       crm_forecast_update_frequency_days=8.0)
        r = eng().assess(i)
        assert f"{round(0.40*100)}% commit variance" in r.forecast_signal
        assert f"{round(0.60*100)}% miss rate" in r.forecast_signal
        assert f"{round(0.50*100)}% 3Q accuracy" in r.forecast_signal
        assert f"composite {round(r.forecast_composite)}" in r.forecast_signal

    def test_signal_sandbagger_label(self):
        i = make_input(undercommit_frequency_pct=0.55, rolling_3q_forecast_accuracy_pct=0.85,
                       commit_vs_actual_variance_pct=0.40, forecast_miss_rate_pct=0.60,
                       crm_forecast_update_frequency_days=8.0)
        r = eng().assess(i)
        if r.forecast_composite >= 20:
            assert "Sandbagger" in r.forecast_signal


# ---------------------------------------------------------------------------
# assess() end-to-end scenarios
# ---------------------------------------------------------------------------

class TestAssessEndToEnd:
    def test_clean_rep(self):
        r = eng().assess(make_input())
        assert r.forecast_risk == "low"
        assert r.forecast_severity == "accurate"
        assert r.recommended_action == "no_action"
        assert r.forecast_pattern == "none"

    def test_critical_chronic_overcommit(self):
        i = make_input(
            overcommit_frequency_pct=0.70, commit_vs_actual_variance_pct=0.50,
            forecast_miss_rate_pct=0.70, rolling_3q_forecast_accuracy_pct=0.40,
            commit_category_accuracy_pct=0.35, category_downgrade_rate_pct=0.40,
            close_date_change_frequency=3.5, last_week_close_rate_pct=0.60,
            pipeline_to_commit_escalation_rate_pct=0.50, push_out_frequency_pct=0.50,
            crm_forecast_update_frequency_days=8.0, undercommit_frequency_pct=0.10,
        )
        r = eng().assess(i)
        assert r.forecast_risk == "critical"
        assert r.forecast_pattern == "chronic_overcommit"
        assert r.recommended_action == "executive_forecast_audit"
        assert r.forecast_severity == "blind_spot"

    def test_all_scores_clamped_between_0_and_100(self):
        i = make_input(
            commit_vs_actual_variance_pct=0.50, forecast_miss_rate_pct=0.80,
            rolling_3q_forecast_accuracy_pct=0.30, commit_category_accuracy_pct=0.20,
            category_downgrade_rate_pct=0.50, close_date_change_frequency=5.0,
            last_week_close_rate_pct=0.80, pipeline_to_commit_escalation_rate_pct=0.80,
            push_out_frequency_pct=0.80, overcommit_frequency_pct=0.80,
            undercommit_frequency_pct=0.80, crm_forecast_update_frequency_days=10.0,
        )
        r = eng().assess(i)
        for score in (r.accuracy_score, r.discipline_score, r.timing_score,
                      r.reliability_score, r.forecast_composite):
            assert 0 <= score <= 100


# ---------------------------------------------------------------------------
# assess_batch
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_batch_length_and_types(self):
        e = eng()
        results = e.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        assert len(results) == 5
        assert all(isinstance(r, ForecastResult) for r in results)

    def test_batch_accumulates_results(self):
        e = eng()
        e.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        assert len(e._results) == 3


# ---------------------------------------------------------------------------
# summary()
# ---------------------------------------------------------------------------

class TestSummary:
    def test_empty_summary_has_13_keys(self):
        assert len(eng().summary()) == 13

    def test_empty_summary_zero_values(self):
        s = eng().summary()
        assert s["total"] == 0
        assert s["avg_forecast_composite"] == 0.0
        assert s["forecast_gap_count"] == 0
        assert s["manager_review_count"] == 0
        assert s["total_estimated_forecast_error_usd"] == 0.0

    def test_summary_total_matches_count(self):
        e = eng()
        e.assess_batch([make_input(rep_id=f"R{i}") for i in range(4)])
        assert e.summary()["total"] == 4

    def test_count_dicts_sum_to_total(self):
        e = eng()
        e.assess_batch([make_input(rep_id=f"R{i}") for i in range(6)])
        s = e.summary()
        total = s["total"]
        for key in ("risk_counts", "pattern_counts", "severity_counts", "action_counts"):
            assert sum(s[key].values()) == total

    def test_summary_avg_composite_is_float(self):
        e = eng()
        e.assess(make_input())
        assert isinstance(e.summary()["avg_forecast_composite"], float)

    def test_summary_total_error_aggregates(self):
        e = eng()
        r1 = e.assess(make_input(rep_id="R1", total_commit_deals=5,
                                  avg_deal_value_usd=10_000.0,
                                  commit_vs_actual_variance_pct=0.30))
        r2 = e.assess(make_input(rep_id="R2", total_commit_deals=10,
                                  avg_deal_value_usd=20_000.0,
                                  commit_vs_actual_variance_pct=0.30))
        s = e.summary()
        assert s["total_estimated_forecast_error_usd"] == round(
            r1.estimated_forecast_error_usd + r2.estimated_forecast_error_usd, 2
        )

    def test_summary_gap_and_review_counts(self):
        e = eng()
        # gap: forecast_miss_rate_pct >= 0.40; no manager review (composite < 25, variance < 0.20, push_out < 0.30)
        e.assess(make_input(forecast_miss_rate_pct=0.50))
        # no gap; manager review: commit_vs_actual_variance_pct >= 0.20
        e.assess(make_input(commit_vs_actual_variance_pct=0.20))
        # neither
        e.assess(make_input())
        s = e.summary()
        assert s["forecast_gap_count"] == 1
        assert s["manager_review_count"] == 1

    def test_summary_13_keys_after_assessments(self):
        e = eng()
        e.assess(make_input())
        assert len(e.summary()) == 13
