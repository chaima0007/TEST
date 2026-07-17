"""Comprehensive pytest suite for SalesPipelineStageInflationCrmHygieneEngine."""
from __future__ import annotations
import pytest
from swarm.intelligence.sales_pipeline_stage_inflation_crm_hygiene_engine import (
    HygieneRisk, HygienePattern, HygieneSeverity, HygieneAction,
    HygieneInput, HygieneResult,
    SalesPipelineStageInflationCrmHygieneEngine,
)


# ── helpers ──────────────────────────────────────────────────────────────────

def make_input(**overrides) -> HygieneInput:
    """Return a zero/minimal HygieneInput with optional field overrides."""
    defaults = dict(
        rep_id="R1", region="NA", evaluation_period_id="Q1-2026",
        stage_advancement_without_exit_criteria_pct=0.0,
        deal_regression_rate_pct=0.0,
        avg_days_in_current_stage=0.0,
        stage_3_to_close_conversion_rate_pct=1.0,
        closed_won_below_forecast_pct=0.0,
        stage_skip_rate_pct=0.0,
        crm_update_latency_days=0.0,
        verified_next_step_in_crm_rate_pct=1.0,
        competitive_status_missing_rate_pct=0.0,
        decision_criteria_captured_rate_pct=1.0,
        technical_validation_complete_rate_pct=1.0,
        budget_verified_rate_pct=1.0,
        close_date_slip_rate_pct=0.0,
        pipeline_creation_to_close_ratio=1.0,
        opp_age_over_180_days_pct=0.0,
        discovery_to_proposal_ratio=1.0,
        data_completeness_score=1.0,
        manual_close_date_push_rate_pct=0.0,
        win_rate_vs_forecast_accuracy_delta=0.0,
        total_pipeline_deals=10,
        avg_deal_value_usd=1000.0,
    )
    defaults.update(overrides)
    return HygieneInput(**defaults)


@pytest.fixture
def engine():
    return SalesPipelineStageInflationCrmHygieneEngine()


# ── 1. Enum values ────────────────────────────────────────────────────────────

@pytest.mark.parametrize("member,value", [
    (HygieneRisk.low, "low"), (HygieneRisk.moderate, "moderate"),
    (HygieneRisk.high, "high"), (HygieneRisk.critical, "critical"),
])
def test_hygiene_risk_values(member, value):
    assert member.value == value


@pytest.mark.parametrize("member,value", [
    (HygienePattern.none, "none"),
    (HygienePattern.stage_inflation_stager, "stage_inflation_stager"),
    (HygienePattern.phantom_pipeline, "phantom_pipeline"),
    (HygienePattern.data_black_hole, "data_black_hole"),
    (HygienePattern.vanity_metrics_builder, "vanity_metrics_builder"),
    (HygienePattern.forecast_fudger, "forecast_fudger"),
])
def test_hygiene_pattern_values(member, value):
    assert member.value == value


@pytest.mark.parametrize("member,value", [
    (HygieneSeverity.clean, "clean"), (HygieneSeverity.drifting, "drifting"),
    (HygieneSeverity.degraded, "degraded"), (HygieneSeverity.corrupted, "corrupted"),
])
def test_hygiene_severity_values(member, value):
    assert member.value == value


@pytest.mark.parametrize("member,value", [
    (HygieneAction.no_action, "no_action"),
    (HygieneAction.crm_hygiene_coaching, "crm_hygiene_coaching"),
    (HygieneAction.pipeline_review_checkpoint, "pipeline_review_checkpoint"),
    (HygieneAction.stage_criteria_enforcement, "stage_criteria_enforcement"),
    (HygieneAction.data_quality_intervention, "data_quality_intervention"),
    (HygieneAction.pipeline_purge_facilitation, "pipeline_purge_facilitation"),
    (HygieneAction.forecast_integrity_audit, "forecast_integrity_audit"),
    (HygieneAction.crm_accuracy_reset, "crm_accuracy_reset"),
])
def test_hygiene_action_values(member, value):
    assert member.value == value


# ── 2. to_dict ────────────────────────────────────────────────────────────────

def test_to_dict_has_15_keys(engine):
    result = engine.assess(make_input())
    d = result.to_dict()
    assert len(d) == 15


def test_to_dict_enum_fields_are_strings(engine):
    result = engine.assess(make_input())
    d = result.to_dict()
    for key in ("hygiene_risk", "hygiene_pattern", "hygiene_severity", "recommended_action"):
        assert isinstance(d[key], str), f"{key} should be a string"


def test_to_dict_expected_keys(engine):
    result = engine.assess(make_input())
    d = result.to_dict()
    expected = {
        "rep_id", "region", "hygiene_risk", "hygiene_pattern", "hygiene_severity",
        "recommended_action", "accuracy_score", "hygiene_score", "velocity_score",
        "completeness_score", "hygiene_composite", "has_hygiene_gap",
        "requires_hygiene_coaching", "estimated_inflated_pipeline_usd", "hygiene_signal",
    }
    assert set(d.keys()) == expected


# ── 3. Sub-scores ─────────────────────────────────────────────────────────────

class TestAccuracyScore:
    @pytest.mark.parametrize("adv,expected_contrib", [
        (0.55, 40), (0.30, 22), (0.15, 8), (0.0, 0),
    ])
    def test_stage_advancement_tiers(self, engine, adv, expected_contrib):
        inp = make_input(stage_advancement_without_exit_criteria_pct=adv)
        assert engine._accuracy_score(inp) == expected_contrib

    @pytest.mark.parametrize("below,expected_contrib", [
        (0.45, 35), (0.25, 18), (0.0, 0),
    ])
    def test_closed_won_below_forecast_tiers(self, engine, below, expected_contrib):
        inp = make_input(closed_won_below_forecast_pct=below)
        assert engine._accuracy_score(inp) == expected_contrib

    @pytest.mark.parametrize("delta,expected_contrib", [
        (0.30, 25), (0.15, 12), (0.0, 0),
    ])
    def test_win_rate_delta_tiers(self, engine, delta, expected_contrib):
        inp = make_input(win_rate_vs_forecast_accuracy_delta=delta)
        assert engine._accuracy_score(inp) == expected_contrib

    def test_accuracy_cap_at_100(self, engine):
        inp = make_input(
            stage_advancement_without_exit_criteria_pct=0.60,
            closed_won_below_forecast_pct=0.50,
            win_rate_vs_forecast_accuracy_delta=0.35,
        )
        assert engine._accuracy_score(inp) == 100.0

    def test_accuracy_additive(self, engine):
        inp = make_input(
            stage_advancement_without_exit_criteria_pct=0.30,
            closed_won_below_forecast_pct=0.25,
            win_rate_vs_forecast_accuracy_delta=0.0,
        )
        assert engine._accuracy_score(inp) == 22 + 18


class TestHygieneScore:
    @pytest.mark.parametrize("latency,expected_contrib", [
        (10.0, 45), (5.0, 25), (2.5, 10), (0.0, 0),
    ])
    def test_latency_tiers(self, engine, latency, expected_contrib):
        inp = make_input(crm_update_latency_days=latency)
        assert engine._hygiene_score(inp) == expected_contrib

    @pytest.mark.parametrize("rate,expected_contrib", [
        (0.25, 30), (0.55, 15), (1.0, 0),
    ])
    def test_next_step_tiers(self, engine, rate, expected_contrib):
        inp = make_input(verified_next_step_in_crm_rate_pct=rate)
        assert engine._hygiene_score(inp) == expected_contrib

    @pytest.mark.parametrize("score,expected_contrib", [
        (0.25, 25), (0.55, 12), (1.0, 0),
    ])
    def test_data_completeness_tiers(self, engine, score, expected_contrib):
        inp = make_input(data_completeness_score=score)
        assert engine._hygiene_score(inp) == expected_contrib

    def test_hygiene_cap_at_100(self, engine):
        inp = make_input(
            crm_update_latency_days=15.0,
            verified_next_step_in_crm_rate_pct=0.10,
            data_completeness_score=0.10,
        )
        assert engine._hygiene_score(inp) == 100.0

    def test_hygiene_additive(self, engine):
        inp = make_input(
            crm_update_latency_days=5.0,
            verified_next_step_in_crm_rate_pct=0.55,
            data_completeness_score=1.0,
        )
        assert engine._hygiene_score(inp) == 25 + 15


class TestVelocityScore:
    @pytest.mark.parametrize("slip,expected_contrib", [
        (0.60, 45), (0.35, 25), (0.18, 10), (0.0, 0),
    ])
    def test_close_date_slip_tiers(self, engine, slip, expected_contrib):
        inp = make_input(close_date_slip_rate_pct=slip)
        assert engine._velocity_score(inp) == expected_contrib

    @pytest.mark.parametrize("age,expected_contrib", [
        (0.40, 30), (0.20, 15), (0.0, 0),
    ])
    def test_opp_age_tiers(self, engine, age, expected_contrib):
        inp = make_input(opp_age_over_180_days_pct=age)
        assert engine._velocity_score(inp) == expected_contrib

    @pytest.mark.parametrize("reg,expected_contrib", [
        (0.35, 25), (0.18, 12), (0.0, 0),
    ])
    def test_regression_tiers(self, engine, reg, expected_contrib):
        inp = make_input(deal_regression_rate_pct=reg)
        assert engine._velocity_score(inp) == expected_contrib

    def test_velocity_cap_at_100(self, engine):
        inp = make_input(
            close_date_slip_rate_pct=0.80,
            opp_age_over_180_days_pct=0.60,
            deal_regression_rate_pct=0.50,
        )
        assert engine._velocity_score(inp) == 100.0

    def test_velocity_additive(self, engine):
        inp = make_input(
            close_date_slip_rate_pct=0.35,
            opp_age_over_180_days_pct=0.20,
            deal_regression_rate_pct=0.0,
        )
        assert engine._velocity_score(inp) == 25 + 15


class TestCompletenessScore:
    @pytest.mark.parametrize("dc,expected_contrib", [
        (0.20, 40), (0.45, 22), (0.65, 8), (1.0, 0),
    ])
    def test_decision_criteria_tiers(self, engine, dc, expected_contrib):
        inp = make_input(decision_criteria_captured_rate_pct=dc)
        assert engine._completeness_score(inp) == expected_contrib

    @pytest.mark.parametrize("bv,expected_contrib", [
        (0.25, 35), (0.50, 18), (1.0, 0),
    ])
    def test_budget_verified_tiers(self, engine, bv, expected_contrib):
        inp = make_input(budget_verified_rate_pct=bv)
        assert engine._completeness_score(inp) == expected_contrib

    @pytest.mark.parametrize("tv,expected_contrib", [
        (0.20, 25), (0.45, 12), (1.0, 0),
    ])
    def test_technical_validation_tiers(self, engine, tv, expected_contrib):
        inp = make_input(technical_validation_complete_rate_pct=tv)
        assert engine._completeness_score(inp) == expected_contrib

    def test_completeness_cap_at_100(self, engine):
        inp = make_input(
            decision_criteria_captured_rate_pct=0.10,
            budget_verified_rate_pct=0.10,
            technical_validation_complete_rate_pct=0.10,
        )
        assert engine._completeness_score(inp) == 100.0

    def test_completeness_additive(self, engine):
        inp = make_input(
            decision_criteria_captured_rate_pct=0.45,
            budget_verified_rate_pct=0.50,
            technical_validation_complete_rate_pct=1.0,
        )
        assert engine._completeness_score(inp) == 22 + 18


# ── 4. Composite formula ──────────────────────────────────────────────────────

def test_composite_weights(engine):
    # ac=100, hy=0, ve=0, co=0 → 30.0
    assert engine._composite(100, 0, 0, 0) == 30.0
    assert engine._composite(0, 100, 0, 0) == 25.0
    assert engine._composite(0, 0, 100, 0) == 25.0
    assert engine._composite(0, 0, 0, 100) == 20.0


def test_composite_weights_sum(engine):
    assert engine._composite(100, 100, 100, 100) == 100.0


def test_composite_cap_at_100(engine):
    # Artificial — cap guard
    assert engine._composite(200, 200, 200, 200) == 100.0


def test_composite_rounding(engine):
    result = engine._composite(33, 33, 33, 33)
    expected = round(33 * 0.30 + 33 * 0.25 + 33 * 0.25 + 33 * 0.20, 2)
    assert result == expected


# ── 5. Risk thresholds ────────────────────────────────────────────────────────

@pytest.mark.parametrize("composite,expected_risk", [
    (60.0, HygieneRisk.critical),
    (75.0, HygieneRisk.critical),
    (40.0, HygieneRisk.high),
    (59.9, HygieneRisk.high),
    (20.0, HygieneRisk.moderate),
    (39.9, HygieneRisk.moderate),
    (0.0,  HygieneRisk.low),
    (19.9, HygieneRisk.low),
])
def test_risk_thresholds(engine, composite, expected_risk):
    assert engine._risk(composite) == expected_risk


# ── 6. Severity thresholds ────────────────────────────────────────────────────

@pytest.mark.parametrize("composite,expected_sev", [
    (60.0, HygieneSeverity.corrupted),
    (80.0, HygieneSeverity.corrupted),
    (40.0, HygieneSeverity.degraded),
    (59.9, HygieneSeverity.degraded),
    (20.0, HygieneSeverity.drifting),
    (39.9, HygieneSeverity.drifting),
    (0.0,  HygieneSeverity.clean),
    (19.9, HygieneSeverity.clean),
])
def test_severity_thresholds(engine, composite, expected_sev):
    assert engine._severity(composite) == expected_sev


# ── 7. Pattern priority rules ─────────────────────────────────────────────────

def test_pattern_stage_inflation_stager(engine):
    inp = make_input(
        stage_advancement_without_exit_criteria_pct=0.50,
        deal_regression_rate_pct=0.30,
    )
    assert engine._pattern(inp) == HygienePattern.stage_inflation_stager


def test_pattern_phantom_pipeline(engine):
    inp = make_input(
        close_date_slip_rate_pct=0.55,
        opp_age_over_180_days_pct=0.35,
    )
    assert engine._pattern(inp) == HygienePattern.phantom_pipeline


def test_pattern_data_black_hole(engine):
    inp = make_input(
        data_completeness_score=0.30,
        crm_update_latency_days=7.0,
    )
    assert engine._pattern(inp) == HygienePattern.data_black_hole


def test_pattern_vanity_metrics_builder(engine):
    inp = make_input(
        stage_3_to_close_conversion_rate_pct=0.15,
        pipeline_creation_to_close_ratio=5.0,
    )
    assert engine._pattern(inp) == HygienePattern.vanity_metrics_builder


def test_pattern_forecast_fudger(engine):
    inp = make_input(
        win_rate_vs_forecast_accuracy_delta=0.25,
        closed_won_below_forecast_pct=0.40,
    )
    assert engine._pattern(inp) == HygienePattern.forecast_fudger


def test_pattern_none(engine):
    inp = make_input()
    assert engine._pattern(inp) == HygienePattern.none


def test_pattern_priority_inflation_over_phantom(engine):
    # Both stage_inflation_stager and phantom_pipeline conditions met; inflation is first
    inp = make_input(
        stage_advancement_without_exit_criteria_pct=0.50,
        deal_regression_rate_pct=0.30,
        close_date_slip_rate_pct=0.55,
        opp_age_over_180_days_pct=0.35,
    )
    assert engine._pattern(inp) == HygienePattern.stage_inflation_stager


# ── 8. Action rules ───────────────────────────────────────────────────────────

@pytest.mark.parametrize("risk,pattern,expected_action", [
    # critical + stage_inflation_stager → crm_accuracy_reset
    (HygieneRisk.critical, HygienePattern.stage_inflation_stager, HygieneAction.crm_accuracy_reset),
    # critical + forecast_fudger → crm_accuracy_reset
    (HygieneRisk.critical, HygienePattern.forecast_fudger, HygieneAction.crm_accuracy_reset),
    # critical + other → forecast_integrity_audit
    (HygieneRisk.critical, HygienePattern.phantom_pipeline, HygieneAction.forecast_integrity_audit),
    (HygieneRisk.critical, HygienePattern.none, HygieneAction.forecast_integrity_audit),
    # high + each pattern
    (HygieneRisk.high, HygienePattern.stage_inflation_stager, HygieneAction.stage_criteria_enforcement),
    (HygieneRisk.high, HygienePattern.phantom_pipeline, HygieneAction.pipeline_purge_facilitation),
    (HygieneRisk.high, HygienePattern.data_black_hole, HygieneAction.data_quality_intervention),
    (HygieneRisk.high, HygienePattern.vanity_metrics_builder, HygieneAction.pipeline_review_checkpoint),
    (HygieneRisk.high, HygienePattern.forecast_fudger, HygieneAction.forecast_integrity_audit),
    (HygieneRisk.high, HygienePattern.none, HygieneAction.crm_hygiene_coaching),
    # moderate → crm_hygiene_coaching
    (HygieneRisk.moderate, HygienePattern.none, HygieneAction.crm_hygiene_coaching),
    (HygieneRisk.moderate, HygienePattern.forecast_fudger, HygieneAction.crm_hygiene_coaching),
    # low → no_action
    (HygieneRisk.low, HygienePattern.none, HygieneAction.no_action),
    (HygieneRisk.low, HygienePattern.stage_inflation_stager, HygieneAction.no_action),
])
def test_action_rules(engine, risk, pattern, expected_action):
    assert engine._action(risk, pattern) == expected_action


# ── 9. has_hygiene_gap ────────────────────────────────────────────────────────

def test_gap_triggered_by_composite(engine):
    # composite >= 40 should set gap
    inp = make_input(
        crm_update_latency_days=15.0,
        verified_next_step_in_crm_rate_pct=0.10,
        data_completeness_score=0.10,
        decision_criteria_captured_rate_pct=0.10,
        budget_verified_rate_pct=0.10,
        stage_advancement_without_exit_criteria_pct=0.0,
    )
    result = engine.assess(inp)
    assert result.hygiene_composite >= 40
    assert result.has_hygiene_gap is True


def test_gap_triggered_by_data_completeness(engine):
    inp = make_input(data_completeness_score=0.50)
    result = engine.assess(inp)
    assert result.has_hygiene_gap is True


def test_gap_triggered_by_stage_advancement(engine):
    inp = make_input(stage_advancement_without_exit_criteria_pct=0.30)
    result = engine.assess(inp)
    assert result.has_hygiene_gap is True


def test_gap_false_when_no_trigger(engine):
    # All clean: composite < 40, data_completeness > 0.50, advancement < 0.30
    inp = make_input(data_completeness_score=0.51, stage_advancement_without_exit_criteria_pct=0.0)
    result = engine.assess(inp)
    assert result.has_hygiene_gap is False


# ── 10. requires_hygiene_coaching ─────────────────────────────────────────────

def test_coaching_triggered_by_composite(engine):
    inp = make_input(
        crm_update_latency_days=15.0,
        verified_next_step_in_crm_rate_pct=0.10,
        data_completeness_score=0.10,
        decision_criteria_captured_rate_pct=0.10,
        budget_verified_rate_pct=0.10,
    )
    result = engine.assess(inp)
    assert result.hygiene_composite >= 25
    assert result.requires_hygiene_coaching is True


def test_coaching_triggered_by_latency(engine):
    inp = make_input(crm_update_latency_days=5.0)
    result = engine.assess(inp)
    assert result.requires_hygiene_coaching is True


def test_coaching_triggered_by_next_step_rate(engine):
    inp = make_input(verified_next_step_in_crm_rate_pct=0.60)
    result = engine.assess(inp)
    assert result.requires_hygiene_coaching is True


def test_coaching_false_when_no_trigger(engine):
    # composite < 25, latency < 5, next_step_rate > 0.60
    inp = make_input(
        crm_update_latency_days=1.0,
        verified_next_step_in_crm_rate_pct=0.61,
        data_completeness_score=1.0,
    )
    result = engine.assess(inp)
    assert result.requires_hygiene_coaching is False


# ── 11. estimated_inflated_pipeline_usd ───────────────────────────────────────

def test_inflated_pipeline_formula(engine):
    inp = make_input(
        total_pipeline_deals=50,
        avg_deal_value_usd=20000.0,
        stage_advancement_without_exit_criteria_pct=0.40,
        # drive composite to known value by setting all scores via sub-score levers
        crm_update_latency_days=10.0,   # hygiene += 45
        verified_next_step_in_crm_rate_pct=0.25,  # hygiene += 30
    )
    result = engine.assess(inp)
    comp = result.hygiene_composite
    expected = round(50 * 20000.0 * 0.40 * (comp / 100), 2)
    assert result.estimated_inflated_pipeline_usd == expected


def test_inflated_pipeline_zero_when_composite_zero(engine):
    inp = make_input(total_pipeline_deals=100, avg_deal_value_usd=5000.0)
    result = engine.assess(inp)
    # composite is 0 when all scores are 0
    assert result.estimated_inflated_pipeline_usd == 0.0


@pytest.mark.parametrize("deals,value,adv,comp,expected", [
    (10, 1000.0, 0.5, 50.0, round(10 * 1000.0 * 0.5 * 0.5, 2)),
    (0,  5000.0, 0.3, 30.0, 0.0),
    (5,  2000.0, 1.0, 100.0, round(5 * 2000.0 * 1.0 * 1.0, 2)),
])
def test_inflated_pipeline_parametrized(engine, deals, value, adv, comp, expected):
    result = engine._inflated_pipeline(
        make_input(total_pipeline_deals=deals, avg_deal_value_usd=value,
                   stage_advancement_without_exit_criteria_pct=adv),
        comp
    )
    assert result == expected


# ── 12. hygiene_signal ────────────────────────────────────────────────────────

def test_signal_stable_message_when_composite_below_20(engine):
    inp = make_input()
    result = engine.assess(inp)
    assert result.hygiene_composite < 20
    assert "healthy" in result.hygiene_signal
    assert "benchmark" in result.hygiene_signal


def test_signal_active_components_when_composite_above_20(engine):
    inp = make_input(
        crm_update_latency_days=10.0,
        verified_next_step_in_crm_rate_pct=0.10,
        data_completeness_score=0.20,
        stage_advancement_without_exit_criteria_pct=0.50,
        deal_regression_rate_pct=0.30,
        close_date_slip_rate_pct=0.70,
    )
    result = engine.assess(inp)
    assert result.hygiene_composite >= 20
    signal = result.hygiene_signal
    # Should contain pattern label, percentages, composite
    assert "%" in signal or "composite" in signal


def test_signal_contains_inflate_pct(engine):
    inp = make_input(
        crm_update_latency_days=10.0,
        verified_next_step_in_crm_rate_pct=0.10,
        stage_advancement_without_exit_criteria_pct=0.42,
        data_completeness_score=0.20,
    )
    result = engine.assess(inp)
    assert "42%" in result.hygiene_signal


# ── 13. assess(), assess_batch(), summary() ───────────────────────────────────

def test_assess_returns_hygiene_result(engine):
    result = engine.assess(make_input())
    assert isinstance(result, HygieneResult)


def test_assess_stores_result(engine):
    engine.assess(make_input(rep_id="A"))
    assert len(engine._results) == 1


def test_assess_batch_returns_list(engine):
    inputs = [make_input(rep_id=f"R{i}") for i in range(3)]
    results = engine.assess_batch(inputs)
    assert len(results) == 3
    assert all(isinstance(r, HygieneResult) for r in results)


def test_assess_batch_accumulates_results(engine):
    inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
    engine.assess_batch(inputs)
    assert len(engine._results) == 5


def test_summary_empty_engine():
    e = SalesPipelineStageInflationCrmHygieneEngine()
    s = e.summary()
    assert s["total"] == 0
    assert s["avg_hygiene_composite"] == 0.0


def test_summary_has_13_keys(engine):
    engine.assess(make_input())
    s = engine.summary()
    assert len(s) == 13


def test_summary_keys(engine):
    engine.assess(make_input())
    s = engine.summary()
    expected_keys = {
        "total", "risk_counts", "pattern_counts", "severity_counts", "action_counts",
        "avg_hygiene_composite", "hygiene_gap_count", "coaching_count",
        "avg_accuracy_score", "avg_hygiene_score", "avg_velocity_score",
        "avg_completeness_score", "total_estimated_inflated_pipeline_usd",
    }
    assert set(s.keys()) == expected_keys


def test_summary_counts_and_totals(engine):
    inp_low = make_input(rep_id="L")
    inp_high = make_input(
        rep_id="H",
        crm_update_latency_days=10.0,
        verified_next_step_in_crm_rate_pct=0.10,
        data_completeness_score=0.10,
        decision_criteria_captured_rate_pct=0.10,
        budget_verified_rate_pct=0.10,
    )
    engine.assess_batch([inp_low, inp_high])
    s = engine.summary()
    assert s["total"] == 2
    assert sum(s["risk_counts"].values()) == 2
    assert sum(s["severity_counts"].values()) == 2


def test_summary_avg_composite(engine):
    # Two reps with composites that we can reason about
    engine.assess(make_input(rep_id="A"))
    engine.assess(make_input(rep_id="B"))
    s = engine.summary()
    # Both zeros → avg 0.0
    assert s["avg_hygiene_composite"] == 0.0


# ── 14. Edge cases ────────────────────────────────────────────────────────────

def test_all_zero_input(engine):
    inp = make_input(
        stage_advancement_without_exit_criteria_pct=0.0,
        deal_regression_rate_pct=0.0,
        closed_won_below_forecast_pct=0.0,
        win_rate_vs_forecast_accuracy_delta=0.0,
        crm_update_latency_days=0.0,
        verified_next_step_in_crm_rate_pct=1.0,
        data_completeness_score=1.0,
        close_date_slip_rate_pct=0.0,
        opp_age_over_180_days_pct=0.0,
        decision_criteria_captured_rate_pct=1.0,
        budget_verified_rate_pct=1.0,
        technical_validation_complete_rate_pct=1.0,
        total_pipeline_deals=0,
        avg_deal_value_usd=0.0,
    )
    result = engine.assess(inp)
    assert result.hygiene_composite == 0.0
    assert result.hygiene_risk == HygieneRisk.low
    assert result.hygiene_severity == HygieneSeverity.clean
    assert result.estimated_inflated_pipeline_usd == 0.0


def test_max_input_caps_composite(engine):
    inp = make_input(
        stage_advancement_without_exit_criteria_pct=1.0,
        deal_regression_rate_pct=1.0,
        closed_won_below_forecast_pct=1.0,
        win_rate_vs_forecast_accuracy_delta=1.0,
        crm_update_latency_days=100.0,
        verified_next_step_in_crm_rate_pct=0.0,
        data_completeness_score=0.0,
        close_date_slip_rate_pct=1.0,
        opp_age_over_180_days_pct=1.0,
        decision_criteria_captured_rate_pct=0.0,
        budget_verified_rate_pct=0.0,
        technical_validation_complete_rate_pct=0.0,
    )
    result = engine.assess(inp)
    assert result.hygiene_composite == 100.0
    assert result.hygiene_risk == HygieneRisk.critical
    assert result.hygiene_severity == HygieneSeverity.corrupted


def test_engine_isolation():
    """Two engines must not share state."""
    e1 = SalesPipelineStageInflationCrmHygieneEngine()
    e2 = SalesPipelineStageInflationCrmHygieneEngine()
    e1.assess(make_input(rep_id="X"))
    assert len(e2._results) == 0


def test_result_rep_id_and_region_passthrough(engine):
    inp = make_input(rep_id="REP99", region="EMEA")
    result = engine.assess(inp)
    assert result.rep_id == "REP99"
    assert result.region == "EMEA"
    d = result.to_dict()
    assert d["rep_id"] == "REP99"
    assert d["region"] == "EMEA"
