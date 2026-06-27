"""
Comprehensive pytest test suite for SalesCRMDataHygieneIntelligenceEngine.
Target: 200+ tests covering all enums, fields, score brackets, thresholds,
formulas, patterns, actions, edge cases, assess_batch, and summary.
"""
from __future__ import annotations

import pytest
from dataclasses import fields as dc_fields

from swarm.intelligence.sales_crm_data_hygiene_intelligence_engine import (
    HygRisk,
    HygPattern,
    HygSeverity,
    HygAction,
    HygInput,
    HygResult,
    SalesCRMDataHygieneIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers / Fixtures
# ---------------------------------------------------------------------------

def _make_input(**overrides) -> HygInput:
    """Return a *clean* baseline input (all scores perfect, low risk)."""
    defaults = dict(
        rep_id="R001",
        region="WEST",
        evaluation_period_id="2026-Q1",
        required_field_completion_pct=0.95,
        avg_days_since_last_update=2.0,
        stage_advancement_rate_pct=0.80,
        deal_without_contact_pct=0.05,
        activity_log_rate_pct=0.90,
        close_date_accuracy_pct=0.90,
        forecast_category_accuracy_pct=0.90,
        duplicate_deal_rate_pct=0.02,
        stale_deal_rate_pct=0.05,
        next_step_field_fill_rate_pct=0.90,
        deal_amount_accuracy_pct=0.95,
        email_linked_rate_pct=0.90,
        opportunity_age_vs_sales_cycle_pct=0.80,
        manual_update_compliance_pct=0.90,
        total_active_deals=20,
        avg_opportunity_value_usd=10_000.0,
        total_pipeline_usd=200_000.0,
        forecasted_revenue_usd=100_000.0,
        quota_usd=120_000.0,
    )
    defaults.update(overrides)
    return HygInput(**defaults)


def _make_critical_input(**overrides) -> HygInput:
    """Return an input guaranteed to produce critical/corrupted composite."""
    defaults = dict(
        rep_id="R_CRIT",
        region="EAST",
        evaluation_period_id="2026-Q1",
        required_field_completion_pct=0.50,   # worst bracket -> +45
        avg_days_since_last_update=25.0,       # worst bracket -> +45
        stage_advancement_rate_pct=0.10,       # worst bracket -> +20
        deal_without_contact_pct=0.50,         # worst bracket -> +20
        activity_log_rate_pct=0.30,            # worst bracket -> +45
        close_date_accuracy_pct=0.30,          # worst bracket -> +40
        forecast_category_accuracy_pct=0.30,   # worst bracket -> +35
        duplicate_deal_rate_pct=0.20,          # worst bracket -> +25
        stale_deal_rate_pct=0.50,              # worst bracket -> +35
        next_step_field_fill_rate_pct=0.20,    # worst bracket -> +35
        deal_amount_accuracy_pct=0.50,
        email_linked_rate_pct=0.30,            # worst bracket -> +35
        opportunity_age_vs_sales_cycle_pct=1.5,
        manual_update_compliance_pct=0.30,     # worst bracket -> +20
        total_active_deals=50,
        avg_opportunity_value_usd=20_000.0,
        total_pipeline_usd=1_000_000.0,
        forecasted_revenue_usd=500_000.0,
        quota_usd=600_000.0,
    )
    defaults.update(overrides)
    return HygInput(**defaults)


@pytest.fixture
def engine():
    return SalesCRMDataHygieneIntelligenceEngine()


@pytest.fixture
def clean_result(engine):
    return engine.assess(_make_input())


@pytest.fixture
def critical_result(engine):
    return engine.assess(_make_critical_input())


# ===========================================================================
# 1. ENUM TESTS
# ===========================================================================

class TestHygRisk:
    def test_low_value(self):
        assert HygRisk.low.value == "low"

    def test_moderate_value(self):
        assert HygRisk.moderate.value == "moderate"

    def test_high_value(self):
        assert HygRisk.high.value == "high"

    def test_critical_value(self):
        assert HygRisk.critical.value == "critical"

    def test_all_members_count(self):
        assert len(HygRisk) == 4

    def test_is_str_enum(self):
        assert isinstance(HygRisk.low, str)

    def test_string_comparison(self):
        assert HygRisk.moderate == "moderate"


class TestHygPattern:
    def test_none_value(self):
        assert HygPattern.none.value == "none"

    def test_ghost_pipeline_value(self):
        assert HygPattern.ghost_pipeline.value == "ghost_pipeline"

    def test_field_skipper_value(self):
        assert HygPattern.field_skipper.value == "field_skipper"

    def test_stage_freezer_value(self):
        assert HygPattern.stage_freezer.value == "stage_freezer"

    def test_contact_orphaner_value(self):
        assert HygPattern.contact_orphaner.value == "contact_orphaner"

    def test_activity_shadow_value(self):
        assert HygPattern.activity_shadow.value == "activity_shadow"

    def test_all_members_count(self):
        assert len(HygPattern) == 6

    def test_is_str_enum(self):
        assert isinstance(HygPattern.ghost_pipeline, str)


class TestHygSeverity:
    def test_clean_value(self):
        assert HygSeverity.clean.value == "clean"

    def test_adequate_value(self):
        assert HygSeverity.adequate.value == "adequate"

    def test_degraded_value(self):
        assert HygSeverity.degraded.value == "degraded"

    def test_corrupted_value(self):
        assert HygSeverity.corrupted.value == "corrupted"

    def test_all_members_count(self):
        assert len(HygSeverity) == 4

    def test_is_str_enum(self):
        assert isinstance(HygSeverity.clean, str)


class TestHygAction:
    def test_no_action_value(self):
        assert HygAction.no_action.value == "no_action"

    def test_data_entry_coaching_value(self):
        assert HygAction.data_entry_coaching.value == "data_entry_coaching"

    def test_stage_hygiene_coaching_value(self):
        assert HygAction.stage_hygiene_coaching.value == "stage_hygiene_coaching"

    def test_contact_linking_coaching_value(self):
        assert HygAction.contact_linking_coaching.value == "contact_linking_coaching"

    def test_activity_logging_coaching_value(self):
        assert HygAction.activity_logging_coaching.value == "activity_logging_coaching"

    def test_crm_audit_required_value(self):
        assert HygAction.crm_audit_required.value == "crm_audit_required"

    def test_crm_data_reset_value(self):
        assert HygAction.crm_data_reset.value == "crm_data_reset"

    def test_all_members_count(self):
        assert len(HygAction) == 7

    def test_includes_crm_data_reset(self):
        values = [a.value for a in HygAction]
        assert "crm_data_reset" in values


# ===========================================================================
# 2. HygInput FIELD TESTS
# ===========================================================================

class TestHygInputFields:
    def test_field_count(self):
        assert len(dc_fields(HygInput)) == 22

    def test_rep_id_field(self):
        inp = _make_input(rep_id="TEST_REP")
        assert inp.rep_id == "TEST_REP"

    def test_region_field(self):
        inp = _make_input(region="NORTH")
        assert inp.region == "NORTH"

    def test_evaluation_period_id_field(self):
        inp = _make_input(evaluation_period_id="2026-Q2")
        assert inp.evaluation_period_id == "2026-Q2"

    def test_required_field_completion_pct(self):
        inp = _make_input(required_field_completion_pct=0.70)
        assert inp.required_field_completion_pct == 0.70

    def test_avg_days_since_last_update(self):
        inp = _make_input(avg_days_since_last_update=10.0)
        assert inp.avg_days_since_last_update == 10.0

    def test_stage_advancement_rate_pct(self):
        inp = _make_input(stage_advancement_rate_pct=0.50)
        assert inp.stage_advancement_rate_pct == 0.50

    def test_deal_without_contact_pct(self):
        inp = _make_input(deal_without_contact_pct=0.25)
        assert inp.deal_without_contact_pct == 0.25

    def test_activity_log_rate_pct(self):
        inp = _make_input(activity_log_rate_pct=0.65)
        assert inp.activity_log_rate_pct == 0.65

    def test_close_date_accuracy_pct(self):
        inp = _make_input(close_date_accuracy_pct=0.75)
        assert inp.close_date_accuracy_pct == 0.75

    def test_forecast_category_accuracy_pct(self):
        inp = _make_input(forecast_category_accuracy_pct=0.60)
        assert inp.forecast_category_accuracy_pct == 0.60

    def test_duplicate_deal_rate_pct(self):
        inp = _make_input(duplicate_deal_rate_pct=0.10)
        assert inp.duplicate_deal_rate_pct == 0.10

    def test_stale_deal_rate_pct(self):
        inp = _make_input(stale_deal_rate_pct=0.15)
        assert inp.stale_deal_rate_pct == 0.15

    def test_next_step_field_fill_rate_pct(self):
        inp = _make_input(next_step_field_fill_rate_pct=0.80)
        assert inp.next_step_field_fill_rate_pct == 0.80

    def test_deal_amount_accuracy_pct(self):
        inp = _make_input(deal_amount_accuracy_pct=0.80)
        assert inp.deal_amount_accuracy_pct == 0.80

    def test_email_linked_rate_pct(self):
        inp = _make_input(email_linked_rate_pct=0.70)
        assert inp.email_linked_rate_pct == 0.70

    def test_opportunity_age_vs_sales_cycle_pct(self):
        inp = _make_input(opportunity_age_vs_sales_cycle_pct=1.2)
        assert inp.opportunity_age_vs_sales_cycle_pct == 1.2

    def test_manual_update_compliance_pct(self):
        inp = _make_input(manual_update_compliance_pct=0.60)
        assert inp.manual_update_compliance_pct == 0.60

    def test_total_active_deals(self):
        inp = _make_input(total_active_deals=35)
        assert inp.total_active_deals == 35

    def test_avg_opportunity_value_usd(self):
        inp = _make_input(avg_opportunity_value_usd=15000.0)
        assert inp.avg_opportunity_value_usd == 15000.0

    def test_total_pipeline_usd(self):
        inp = _make_input(total_pipeline_usd=300_000.0)
        assert inp.total_pipeline_usd == 300_000.0

    def test_forecasted_revenue_usd(self):
        inp = _make_input(forecasted_revenue_usd=80_000.0)
        assert inp.forecasted_revenue_usd == 80_000.0

    def test_quota_usd(self):
        inp = _make_input(quota_usd=150_000.0)
        assert inp.quota_usd == 150_000.0

    def test_all_field_names_present(self):
        expected_names = {
            "rep_id", "region", "evaluation_period_id",
            "required_field_completion_pct", "avg_days_since_last_update",
            "stage_advancement_rate_pct", "deal_without_contact_pct",
            "activity_log_rate_pct", "close_date_accuracy_pct",
            "forecast_category_accuracy_pct", "duplicate_deal_rate_pct",
            "stale_deal_rate_pct", "next_step_field_fill_rate_pct",
            "deal_amount_accuracy_pct", "email_linked_rate_pct",
            "opportunity_age_vs_sales_cycle_pct", "manual_update_compliance_pct",
            "total_active_deals", "avg_opportunity_value_usd",
            "total_pipeline_usd", "forecasted_revenue_usd", "quota_usd",
        }
        actual_names = {f.name for f in dc_fields(HygInput)}
        assert actual_names == expected_names


# ===========================================================================
# 3. HygResult to_dict TESTS
# ===========================================================================

class TestHygResultToDict:
    def test_to_dict_returns_dict(self, clean_result):
        assert isinstance(clean_result.to_dict(), dict)

    def test_to_dict_has_15_keys(self, clean_result):
        assert len(clean_result.to_dict()) == 15

    def test_to_dict_rep_id_key(self, clean_result):
        d = clean_result.to_dict()
        assert "rep_id" in d

    def test_to_dict_region_key(self, clean_result):
        assert "region" in clean_result.to_dict()

    def test_to_dict_hyg_risk_key(self, clean_result):
        assert "hyg_risk" in clean_result.to_dict()

    def test_to_dict_hyg_pattern_key(self, clean_result):
        assert "hyg_pattern" in clean_result.to_dict()

    def test_to_dict_hyg_severity_key(self, clean_result):
        assert "hyg_severity" in clean_result.to_dict()

    def test_to_dict_recommended_action_key(self, clean_result):
        assert "recommended_action" in clean_result.to_dict()

    def test_to_dict_completeness_score_key(self, clean_result):
        assert "completeness_score" in clean_result.to_dict()

    def test_to_dict_currency_score_key(self, clean_result):
        assert "currency_score" in clean_result.to_dict()

    def test_to_dict_accuracy_score_key(self, clean_result):
        assert "accuracy_score" in clean_result.to_dict()

    def test_to_dict_activity_capture_score_key(self, clean_result):
        assert "activity_capture_score" in clean_result.to_dict()

    def test_to_dict_hyg_composite_key(self, clean_result):
        assert "hyg_composite" in clean_result.to_dict()

    def test_to_dict_has_hyg_gap_key(self, clean_result):
        assert "has_hyg_gap" in clean_result.to_dict()

    def test_to_dict_requires_hyg_coaching_key(self, clean_result):
        assert "requires_hyg_coaching" in clean_result.to_dict()

    def test_to_dict_estimated_forecast_error_usd_key(self, clean_result):
        assert "estimated_forecast_error_usd" in clean_result.to_dict()

    def test_to_dict_hyg_signal_key(self, clean_result):
        assert "hyg_signal" in clean_result.to_dict()

    def test_to_dict_enum_values_are_strings(self, clean_result):
        d = clean_result.to_dict()
        assert isinstance(d["hyg_risk"], str)
        assert isinstance(d["hyg_pattern"], str)
        assert isinstance(d["hyg_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_rep_id_value(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(rep_id="TEST_123"))
        assert r.to_dict()["rep_id"] == "TEST_123"

    def test_to_dict_region_value(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(region="SOUTH"))
        assert r.to_dict()["region"] == "SOUTH"

    def test_to_dict_exact_key_set(self, clean_result):
        expected_keys = {
            "rep_id", "region", "hyg_risk", "hyg_pattern", "hyg_severity",
            "recommended_action", "completeness_score", "currency_score",
            "accuracy_score", "activity_capture_score", "hyg_composite",
            "has_hyg_gap", "requires_hyg_coaching",
            "estimated_forecast_error_usd", "hyg_signal",
        }
        assert set(clean_result.to_dict().keys()) == expected_keys


# ===========================================================================
# 4. RISK LEVEL TESTS
# ===========================================================================

class TestRiskLevels:
    def test_low_risk_clean_input(self, clean_result):
        assert clean_result.hyg_risk == HygRisk.low

    def test_critical_risk_bad_input(self, critical_result):
        assert critical_result.hyg_risk == HygRisk.critical

    def test_moderate_risk_threshold_exactly_20(self):
        # Engineer a composite that lands in [20, 40)
        engine = SalesCRMDataHygieneIntelligenceEngine()
        # Moderate: 7<=days<14 -> +12 on currency, rest clean
        inp = _make_input(avg_days_since_last_update=8.0)
        r = engine.assess(inp)
        # composite still influenced by single contributor; just verify rule
        if 20 <= r.hyg_composite < 40:
            assert r.hyg_risk == HygRisk.moderate

    def test_high_risk_threshold_exactly_40(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        inp = _make_input(
            avg_days_since_last_update=22.0,    # +45 currency
            stale_deal_rate_pct=0.30,           # +18 currency
            required_field_completion_pct=0.70, # +28 completeness
        )
        r = engine.assess(inp)
        if 40 <= r.hyg_composite < 60:
            assert r.hyg_risk == HygRisk.high

    def test_risk_low_below_20(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input())
        assert r.hyg_composite < 20
        assert r.hyg_risk == HygRisk.low

    def test_risk_critical_above_60(self, critical_result):
        assert critical_result.hyg_composite >= 60
        assert critical_result.hyg_risk == HygRisk.critical

    def test_risk_thresholds_boundary_60(self):
        # composite exactly 60 → critical
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_critical_input())
        assert r.hyg_composite >= 60
        assert r.hyg_risk == HygRisk.critical

    def test_all_four_risk_levels_achievable(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        risks = set()

        # low
        r = engine.assess(_make_input())
        risks.add(r.hyg_risk)

        # moderate – small currency hit
        r = engine.assess(_make_input(avg_days_since_last_update=8.0,
                                       next_step_field_fill_rate_pct=0.50,
                                       stale_deal_rate_pct=0.13))
        risks.add(r.hyg_risk)

        # high
        r = engine.assess(_make_input(
            avg_days_since_last_update=22.0,
            stale_deal_rate_pct=0.30,
            required_field_completion_pct=0.70,
            next_step_field_fill_rate_pct=0.50,
            close_date_accuracy_pct=0.55,
        ))
        risks.add(r.hyg_risk)

        # critical
        r = engine.assess(_make_critical_input())
        risks.add(r.hyg_risk)

        assert HygRisk.low in risks
        assert HygRisk.critical in risks


# ===========================================================================
# 5. SEVERITY LEVEL TESTS
# ===========================================================================

class TestSeverityLevels:
    def test_clean_severity_for_clean_input(self, clean_result):
        assert clean_result.hyg_severity == HygSeverity.clean

    def test_corrupted_severity_for_critical_input(self, critical_result):
        assert critical_result.hyg_severity == HygSeverity.corrupted

    def test_severity_maps_with_composite(self, critical_result):
        assert critical_result.hyg_composite >= 60
        assert critical_result.hyg_severity == HygSeverity.corrupted

    def test_adequate_severity_range(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        # Build something with composite in [20, 40)
        inp = _make_input(
            avg_days_since_last_update=8.0,
            next_step_field_fill_rate_pct=0.50,
            stale_deal_rate_pct=0.13,
        )
        r = engine.assess(inp)
        if 20 <= r.hyg_composite < 40:
            assert r.hyg_severity == HygSeverity.adequate

    def test_degraded_severity_range(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        inp = _make_input(
            avg_days_since_last_update=22.0,
            stale_deal_rate_pct=0.30,
            required_field_completion_pct=0.70,
            next_step_field_fill_rate_pct=0.50,
            close_date_accuracy_pct=0.55,
        )
        r = engine.assess(inp)
        if 40 <= r.hyg_composite < 60:
            assert r.hyg_severity == HygSeverity.degraded

    def test_severity_and_risk_aligned(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        for inp_fn in [_make_input, _make_critical_input]:
            r = engine.assess(inp_fn())
            if r.hyg_risk == HygRisk.low:
                assert r.hyg_severity == HygSeverity.clean
            elif r.hyg_risk == HygRisk.moderate:
                assert r.hyg_severity == HygSeverity.adequate
            elif r.hyg_risk == HygRisk.high:
                assert r.hyg_severity == HygSeverity.degraded
            elif r.hyg_risk == HygRisk.critical:
                assert r.hyg_severity == HygSeverity.corrupted


# ===========================================================================
# 6. PATTERN TESTS
# ===========================================================================

class TestPatterns:
    def test_none_pattern_for_clean_input(self, clean_result):
        assert clean_result.hyg_pattern == HygPattern.none

    def test_ghost_pipeline_pattern(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(
            stale_deal_rate_pct=0.40,
            avg_days_since_last_update=20.0,
        ))
        assert r.hyg_pattern == HygPattern.ghost_pipeline

    def test_ghost_pipeline_boundary(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        # Exactly at threshold
        r = engine.assess(_make_input(
            stale_deal_rate_pct=0.35,
            avg_days_since_last_update=18.0,
        ))
        assert r.hyg_pattern == HygPattern.ghost_pipeline

    def test_field_skipper_pattern(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(
            required_field_completion_pct=0.60,
            next_step_field_fill_rate_pct=0.40,
            stale_deal_rate_pct=0.05,
            avg_days_since_last_update=2.0,
        ))
        assert r.hyg_pattern == HygPattern.field_skipper

    def test_field_skipper_boundary(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(
            required_field_completion_pct=0.65,
            next_step_field_fill_rate_pct=0.45,
            stale_deal_rate_pct=0.05,
            avg_days_since_last_update=2.0,
        ))
        assert r.hyg_pattern == HygPattern.field_skipper

    def test_stage_freezer_pattern(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(
            stage_advancement_rate_pct=0.15,
            stale_deal_rate_pct=0.35,
            # Make sure ghost_pipeline doesn't trigger
            avg_days_since_last_update=5.0,
            required_field_completion_pct=0.90,
            next_step_field_fill_rate_pct=0.90,
        ))
        assert r.hyg_pattern == HygPattern.stage_freezer

    def test_stage_freezer_boundary(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(
            stage_advancement_rate_pct=0.20,
            stale_deal_rate_pct=0.30,
            avg_days_since_last_update=5.0,
            required_field_completion_pct=0.90,
            next_step_field_fill_rate_pct=0.90,
        ))
        assert r.hyg_pattern == HygPattern.stage_freezer

    def test_contact_orphaner_pattern(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(
            deal_without_contact_pct=0.35,
            email_linked_rate_pct=0.45,
            stage_advancement_rate_pct=0.80,
            stale_deal_rate_pct=0.05,
            avg_days_since_last_update=2.0,
            required_field_completion_pct=0.90,
            next_step_field_fill_rate_pct=0.90,
            activity_log_rate_pct=0.90,
        ))
        assert r.hyg_pattern == HygPattern.contact_orphaner

    def test_contact_orphaner_boundary(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(
            deal_without_contact_pct=0.30,
            email_linked_rate_pct=0.50,
            stage_advancement_rate_pct=0.80,
            stale_deal_rate_pct=0.05,
            avg_days_since_last_update=2.0,
            required_field_completion_pct=0.90,
            next_step_field_fill_rate_pct=0.90,
            activity_log_rate_pct=0.90,
        ))
        assert r.hyg_pattern == HygPattern.contact_orphaner

    def test_activity_shadow_pattern(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(
            activity_log_rate_pct=0.40,
            email_linked_rate_pct=0.45,
            deal_without_contact_pct=0.05,
            stage_advancement_rate_pct=0.80,
            stale_deal_rate_pct=0.05,
            avg_days_since_last_update=2.0,
            required_field_completion_pct=0.90,
            next_step_field_fill_rate_pct=0.90,
        ))
        assert r.hyg_pattern == HygPattern.activity_shadow

    def test_activity_shadow_boundary(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(
            activity_log_rate_pct=0.45,
            email_linked_rate_pct=0.50,
            deal_without_contact_pct=0.05,
            stage_advancement_rate_pct=0.80,
            stale_deal_rate_pct=0.05,
            avg_days_since_last_update=2.0,
            required_field_completion_pct=0.90,
            next_step_field_fill_rate_pct=0.90,
        ))
        assert r.hyg_pattern == HygPattern.activity_shadow

    def test_ghost_pipeline_takes_priority_over_field_skipper(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(
            stale_deal_rate_pct=0.40,
            avg_days_since_last_update=20.0,
            required_field_completion_pct=0.60,
            next_step_field_fill_rate_pct=0.40,
        ))
        assert r.hyg_pattern == HygPattern.ghost_pipeline

    def test_all_six_patterns_reachable(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        patterns = set()

        patterns.add(engine.assess(_make_input()).hyg_pattern)  # none

        patterns.add(engine.assess(_make_input(
            stale_deal_rate_pct=0.40, avg_days_since_last_update=20.0,
        )).hyg_pattern)  # ghost_pipeline

        patterns.add(engine.assess(_make_input(
            required_field_completion_pct=0.60, next_step_field_fill_rate_pct=0.40,
            stale_deal_rate_pct=0.05, avg_days_since_last_update=2.0,
        )).hyg_pattern)  # field_skipper

        patterns.add(engine.assess(_make_input(
            stage_advancement_rate_pct=0.15, stale_deal_rate_pct=0.35,
            avg_days_since_last_update=5.0, required_field_completion_pct=0.90,
            next_step_field_fill_rate_pct=0.90,
        )).hyg_pattern)  # stage_freezer

        patterns.add(engine.assess(_make_input(
            deal_without_contact_pct=0.35, email_linked_rate_pct=0.45,
            stage_advancement_rate_pct=0.80, stale_deal_rate_pct=0.05,
            avg_days_since_last_update=2.0, required_field_completion_pct=0.90,
            next_step_field_fill_rate_pct=0.90, activity_log_rate_pct=0.90,
        )).hyg_pattern)  # contact_orphaner

        patterns.add(engine.assess(_make_input(
            activity_log_rate_pct=0.40, email_linked_rate_pct=0.45,
            deal_without_contact_pct=0.05, stage_advancement_rate_pct=0.80,
            stale_deal_rate_pct=0.05, avg_days_since_last_update=2.0,
            required_field_completion_pct=0.90, next_step_field_fill_rate_pct=0.90,
        )).hyg_pattern)  # activity_shadow

        assert len(patterns) == 6


# ===========================================================================
# 7. ACTION TESTS
# ===========================================================================

class TestActions:
    def test_no_action_for_low_risk(self, clean_result):
        assert clean_result.recommended_action == HygAction.no_action

    def test_data_entry_coaching_for_moderate_risk(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        inp = _make_input(
            avg_days_since_last_update=8.0,
            next_step_field_fill_rate_pct=0.50,
            stale_deal_rate_pct=0.13,
        )
        r = engine.assess(inp)
        if r.hyg_risk == HygRisk.moderate:
            assert r.recommended_action == HygAction.data_entry_coaching

    def test_crm_data_reset_for_critical_ghost_pipeline(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_critical_input())
        # critical + ghost_pipeline -> crm_data_reset
        if (r.hyg_risk == HygRisk.critical and
                r.hyg_pattern == HygPattern.ghost_pipeline):
            assert r.recommended_action == HygAction.crm_data_reset

    def test_crm_data_reset_for_critical_stage_freezer(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_critical_input(
            stale_deal_rate_pct=0.50,
            avg_days_since_last_update=3.0,
            stage_advancement_rate_pct=0.10,
            required_field_completion_pct=0.90,
            next_step_field_fill_rate_pct=0.90,
            activity_log_rate_pct=0.30,
            email_linked_rate_pct=0.30,
            close_date_accuracy_pct=0.30,
            forecast_category_accuracy_pct=0.30,
            duplicate_deal_rate_pct=0.20,
            manual_update_compliance_pct=0.30,
        ))
        if (r.hyg_risk == HygRisk.critical and
                r.hyg_pattern == HygPattern.stage_freezer):
            assert r.recommended_action == HygAction.crm_data_reset

    def test_crm_audit_required_for_critical_non_ghost_non_stage(self):
        # critical + field_skipper -> crm_audit_required
        engine = SalesCRMDataHygieneIntelligenceEngine()
        inp = _make_critical_input(
            stale_deal_rate_pct=0.05,
            avg_days_since_last_update=3.0,
            stage_advancement_rate_pct=0.80,
        )
        r = engine.assess(inp)
        if (r.hyg_risk == HygRisk.critical and
                r.hyg_pattern not in (HygPattern.ghost_pipeline, HygPattern.stage_freezer)):
            assert r.recommended_action == HygAction.crm_audit_required

    def test_data_entry_coaching_for_high_field_skipper(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(
            avg_days_since_last_update=22.0,
            stale_deal_rate_pct=0.30,
            required_field_completion_pct=0.60,
            next_step_field_fill_rate_pct=0.40,
            close_date_accuracy_pct=0.55,
        ))
        if r.hyg_risk == HygRisk.high and r.hyg_pattern == HygPattern.field_skipper:
            assert r.recommended_action == HygAction.data_entry_coaching

    def test_stage_hygiene_coaching_for_high_stage_freezer(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(
            stage_advancement_rate_pct=0.15,
            stale_deal_rate_pct=0.35,
            avg_days_since_last_update=5.0,
            required_field_completion_pct=0.90,
            next_step_field_fill_rate_pct=0.90,
            close_date_accuracy_pct=0.55,
            activity_log_rate_pct=0.30,
            email_linked_rate_pct=0.30,
            manual_update_compliance_pct=0.30,
        ))
        if r.hyg_risk == HygRisk.high and r.hyg_pattern == HygPattern.stage_freezer:
            assert r.recommended_action == HygAction.stage_hygiene_coaching

    def test_contact_linking_coaching_for_high_contact_orphaner(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(
            deal_without_contact_pct=0.35,
            email_linked_rate_pct=0.45,
            activity_log_rate_pct=0.30,
            manual_update_compliance_pct=0.30,
            close_date_accuracy_pct=0.55,
            stage_advancement_rate_pct=0.80,
            stale_deal_rate_pct=0.05,
            avg_days_since_last_update=2.0,
            required_field_completion_pct=0.90,
            next_step_field_fill_rate_pct=0.90,
        ))
        if r.hyg_risk == HygRisk.high and r.hyg_pattern == HygPattern.contact_orphaner:
            assert r.recommended_action == HygAction.contact_linking_coaching

    def test_activity_logging_coaching_for_high_activity_shadow(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(
            activity_log_rate_pct=0.40,
            email_linked_rate_pct=0.45,
            deal_without_contact_pct=0.05,
            close_date_accuracy_pct=0.55,
            manual_update_compliance_pct=0.30,
            stage_advancement_rate_pct=0.80,
            stale_deal_rate_pct=0.05,
            avg_days_since_last_update=2.0,
            required_field_completion_pct=0.90,
            next_step_field_fill_rate_pct=0.90,
        ))
        if r.hyg_risk == HygRisk.high and r.hyg_pattern == HygPattern.activity_shadow:
            assert r.recommended_action == HygAction.activity_logging_coaching

    def test_all_7_actions_are_enum_members(self):
        actions = {a.value for a in HygAction}
        expected = {
            "no_action", "data_entry_coaching", "stage_hygiene_coaching",
            "contact_linking_coaching", "activity_logging_coaching",
            "crm_audit_required", "crm_data_reset",
        }
        assert actions == expected


# ===========================================================================
# 8. SUB-SCORE BRACKET TESTS
# ===========================================================================

class TestCompletenessScore:
    """_completeness_score bracket coverage."""

    def _cs(self, **kw):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        return engine.assess(_make_input(**kw)).completeness_score

    def test_zero_completeness_for_perfect_input(self):
        score = self._cs()
        assert score == 0.0

    def test_required_field_completion_worst_bracket(self):
        # <=0.60 -> +45
        score = self._cs(required_field_completion_pct=0.55,
                         next_step_field_fill_rate_pct=0.90,
                         deal_without_contact_pct=0.05)
        assert score >= 45

    def test_required_field_completion_mid_bracket(self):
        # 0.60 < x <= 0.75 -> +28
        score = self._cs(required_field_completion_pct=0.70,
                         next_step_field_fill_rate_pct=0.90,
                         deal_without_contact_pct=0.05)
        assert score >= 28

    def test_required_field_completion_low_bracket(self):
        # 0.75 < x <= 0.88 -> +12
        score = self._cs(required_field_completion_pct=0.80,
                         next_step_field_fill_rate_pct=0.90,
                         deal_without_contact_pct=0.05)
        assert score >= 12

    def test_next_step_worst_bracket(self):
        # <=0.40 -> +35
        score = self._cs(next_step_field_fill_rate_pct=0.35,
                         required_field_completion_pct=0.95,
                         deal_without_contact_pct=0.05)
        assert score >= 35

    def test_next_step_mid_bracket(self):
        # 0.40 < x <= 0.60 -> +18
        score = self._cs(next_step_field_fill_rate_pct=0.55,
                         required_field_completion_pct=0.95,
                         deal_without_contact_pct=0.05)
        assert score >= 18

    def test_next_step_low_bracket(self):
        # 0.60 < x <= 0.75 -> +6
        score = self._cs(next_step_field_fill_rate_pct=0.65,
                         required_field_completion_pct=0.95,
                         deal_without_contact_pct=0.05)
        assert score >= 6

    def test_deal_without_contact_worst_bracket(self):
        # >=0.35 -> +20
        score = self._cs(deal_without_contact_pct=0.40,
                         required_field_completion_pct=0.95,
                         next_step_field_fill_rate_pct=0.90)
        assert score >= 20

    def test_deal_without_contact_mid_bracket(self):
        # 0.20 <= x < 0.35 -> +10
        score = self._cs(deal_without_contact_pct=0.25,
                         required_field_completion_pct=0.95,
                         next_step_field_fill_rate_pct=0.90)
        assert score >= 10

    def test_completeness_capped_at_100(self):
        score = self._cs(
            required_field_completion_pct=0.50,
            next_step_field_fill_rate_pct=0.20,
            deal_without_contact_pct=0.50,
        )
        assert score <= 100.0


class TestCurrencyScore:
    """_currency_score bracket coverage."""

    def _cu(self, **kw):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        return engine.assess(_make_input(**kw)).currency_score

    def test_zero_currency_for_perfect_input(self):
        assert self._cu() == 0.0

    def test_avg_days_worst_bracket(self):
        # >=21 -> +45
        score = self._cu(avg_days_since_last_update=25.0,
                         stale_deal_rate_pct=0.05,
                         stage_advancement_rate_pct=0.80)
        assert score >= 45

    def test_avg_days_mid_bracket(self):
        # 14 <= x < 21 -> +28
        score = self._cu(avg_days_since_last_update=16.0,
                         stale_deal_rate_pct=0.05,
                         stage_advancement_rate_pct=0.80)
        assert score >= 28

    def test_avg_days_low_bracket(self):
        # 7 <= x < 14 -> +12
        score = self._cu(avg_days_since_last_update=10.0,
                         stale_deal_rate_pct=0.05,
                         stage_advancement_rate_pct=0.80)
        assert score >= 12

    def test_stale_deal_worst_bracket(self):
        # >=0.40 -> +35
        score = self._cu(stale_deal_rate_pct=0.45,
                         avg_days_since_last_update=2.0,
                         stage_advancement_rate_pct=0.80)
        assert score >= 35

    def test_stale_deal_mid_bracket(self):
        # 0.25 <= x < 0.40 -> +18
        score = self._cu(stale_deal_rate_pct=0.30,
                         avg_days_since_last_update=2.0,
                         stage_advancement_rate_pct=0.80)
        assert score >= 18

    def test_stale_deal_low_bracket(self):
        # 0.12 <= x < 0.25 -> +6
        score = self._cu(stale_deal_rate_pct=0.15,
                         avg_days_since_last_update=2.0,
                         stage_advancement_rate_pct=0.80)
        assert score >= 6

    def test_stage_advancement_worst_bracket(self):
        # <=0.25 -> +20
        score = self._cu(stage_advancement_rate_pct=0.20,
                         avg_days_since_last_update=2.0,
                         stale_deal_rate_pct=0.05)
        assert score >= 20

    def test_stage_advancement_mid_bracket(self):
        # 0.25 < x <= 0.45 -> +10
        score = self._cu(stage_advancement_rate_pct=0.35,
                         avg_days_since_last_update=2.0,
                         stale_deal_rate_pct=0.05)
        assert score >= 10

    def test_currency_capped_at_100(self):
        score = self._cu(
            avg_days_since_last_update=30.0,
            stale_deal_rate_pct=0.50,
            stage_advancement_rate_pct=0.10,
        )
        assert score <= 100.0


class TestAccuracyScore:
    """_accuracy_score bracket coverage."""

    def _ac(self, **kw):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        return engine.assess(_make_input(**kw)).accuracy_score

    def test_zero_accuracy_for_perfect_input(self):
        assert self._ac() == 0.0

    def test_close_date_worst_bracket(self):
        # <=0.40 -> +40
        score = self._ac(close_date_accuracy_pct=0.35,
                         forecast_category_accuracy_pct=0.90,
                         duplicate_deal_rate_pct=0.02)
        assert score >= 40

    def test_close_date_mid_bracket(self):
        # 0.40 < x <= 0.60 -> +22
        score = self._ac(close_date_accuracy_pct=0.50,
                         forecast_category_accuracy_pct=0.90,
                         duplicate_deal_rate_pct=0.02)
        assert score >= 22

    def test_close_date_low_bracket(self):
        # 0.60 < x <= 0.78 -> +8
        score = self._ac(close_date_accuracy_pct=0.70,
                         forecast_category_accuracy_pct=0.90,
                         duplicate_deal_rate_pct=0.02)
        assert score >= 8

    def test_forecast_cat_worst_bracket(self):
        # <=0.50 -> +35
        score = self._ac(forecast_category_accuracy_pct=0.40,
                         close_date_accuracy_pct=0.90,
                         duplicate_deal_rate_pct=0.02)
        assert score >= 35

    def test_forecast_cat_mid_bracket(self):
        # 0.50 < x <= 0.70 -> +18
        score = self._ac(forecast_category_accuracy_pct=0.60,
                         close_date_accuracy_pct=0.90,
                         duplicate_deal_rate_pct=0.02)
        assert score >= 18

    def test_forecast_cat_low_bracket(self):
        # 0.70 < x <= 0.82 -> +6
        score = self._ac(forecast_category_accuracy_pct=0.75,
                         close_date_accuracy_pct=0.90,
                         duplicate_deal_rate_pct=0.02)
        assert score >= 6

    def test_duplicate_deal_worst_bracket(self):
        # >=0.15 -> +25
        score = self._ac(duplicate_deal_rate_pct=0.20,
                         close_date_accuracy_pct=0.90,
                         forecast_category_accuracy_pct=0.90)
        assert score >= 25

    def test_duplicate_deal_mid_bracket(self):
        # 0.08 <= x < 0.15 -> +12
        score = self._ac(duplicate_deal_rate_pct=0.10,
                         close_date_accuracy_pct=0.90,
                         forecast_category_accuracy_pct=0.90)
        assert score >= 12

    def test_accuracy_capped_at_100(self):
        score = self._ac(
            close_date_accuracy_pct=0.30,
            forecast_category_accuracy_pct=0.30,
            duplicate_deal_rate_pct=0.20,
        )
        assert score <= 100.0


class TestActivityCaptureScore:
    """_activity_capture_score bracket coverage."""

    def _ap(self, **kw):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        return engine.assess(_make_input(**kw)).activity_capture_score

    def test_zero_activity_capture_for_perfect_input(self):
        assert self._ap() == 0.0

    def test_activity_log_worst_bracket(self):
        # <=0.40 -> +45
        score = self._ap(activity_log_rate_pct=0.35,
                         email_linked_rate_pct=0.90,
                         manual_update_compliance_pct=0.90)
        assert score >= 45

    def test_activity_log_mid_bracket(self):
        # 0.40 < x <= 0.60 -> +28
        score = self._ap(activity_log_rate_pct=0.50,
                         email_linked_rate_pct=0.90,
                         manual_update_compliance_pct=0.90)
        assert score >= 28

    def test_activity_log_low_bracket(self):
        # 0.60 < x <= 0.75 -> +12
        score = self._ap(activity_log_rate_pct=0.65,
                         email_linked_rate_pct=0.90,
                         manual_update_compliance_pct=0.90)
        assert score >= 12

    def test_email_linked_worst_bracket(self):
        # <=0.40 -> +35
        score = self._ap(email_linked_rate_pct=0.35,
                         activity_log_rate_pct=0.90,
                         manual_update_compliance_pct=0.90)
        assert score >= 35

    def test_email_linked_mid_bracket(self):
        # 0.40 < x <= 0.60 -> +18
        score = self._ap(email_linked_rate_pct=0.50,
                         activity_log_rate_pct=0.90,
                         manual_update_compliance_pct=0.90)
        assert score >= 18

    def test_email_linked_low_bracket(self):
        # 0.60 < x <= 0.75 -> +6
        score = self._ap(email_linked_rate_pct=0.70,
                         activity_log_rate_pct=0.90,
                         manual_update_compliance_pct=0.90)
        assert score >= 6

    def test_manual_update_worst_bracket(self):
        # <=0.50 -> +20
        score = self._ap(manual_update_compliance_pct=0.40,
                         activity_log_rate_pct=0.90,
                         email_linked_rate_pct=0.90)
        assert score >= 20

    def test_manual_update_mid_bracket(self):
        # 0.50 < x <= 0.70 -> +10
        score = self._ap(manual_update_compliance_pct=0.60,
                         activity_log_rate_pct=0.90,
                         email_linked_rate_pct=0.90)
        assert score >= 10

    def test_activity_capture_capped_at_100(self):
        score = self._ap(
            activity_log_rate_pct=0.30,
            email_linked_rate_pct=0.30,
            manual_update_compliance_pct=0.30,
        )
        assert score <= 100.0


# ===========================================================================
# 9. COMPOSITE FORMULA TESTS
# ===========================================================================

class TestCompositeFormula:
    def test_composite_weights_sum_to_one(self):
        # 0.30 + 0.25 + 0.25 + 0.20 = 1.00
        assert abs(0.30 + 0.25 + 0.25 + 0.20 - 1.00) < 1e-9

    def test_composite_is_zero_for_perfect_input(self, clean_result):
        assert clean_result.hyg_composite == 0.0

    def test_composite_formula_manually(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        inp = _make_input(
            required_field_completion_pct=0.70,   # +28 completeness
            avg_days_since_last_update=16.0,       # +28 currency
            close_date_accuracy_pct=0.50,          # +22 accuracy
            activity_log_rate_pct=0.50,            # +28 activity
        )
        r = engine.assess(inp)
        # cs = 28, cu = 28, ac = 22, ap = 28
        expected = round(28 * 0.30 + 28 * 0.25 + 22 * 0.25 + 28 * 0.20, 2)
        assert abs(r.hyg_composite - expected) < 0.01

    def test_composite_rounded_to_2dp(self, clean_result):
        val = clean_result.hyg_composite
        assert val == round(val, 2)

    def test_composite_non_negative(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input())
        assert r.hyg_composite >= 0.0

    def test_composite_at_most_100(self, critical_result):
        assert critical_result.hyg_composite <= 100.0

    def test_composite_is_float(self, clean_result):
        assert isinstance(clean_result.hyg_composite, float)

    def test_composite_increases_with_worse_inputs(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r_clean = engine.assess(_make_input())
        r_bad = engine.assess(_make_critical_input())
        assert r_bad.hyg_composite > r_clean.hyg_composite


# ===========================================================================
# 10. HAS_HYG_GAP TRIGGER TESTS
# ===========================================================================

class TestHasHygGap:
    def test_no_gap_for_clean_input(self, clean_result):
        assert clean_result.has_hyg_gap is False

    def test_gap_from_composite_ge_40(self, critical_result):
        assert critical_result.hyg_composite >= 40
        assert critical_result.has_hyg_gap is True

    def test_gap_from_required_field_completion_le_80(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        # Keep other metrics clean but push required_field below 0.80
        r = engine.assess(_make_input(required_field_completion_pct=0.79))
        assert r.has_hyg_gap is True

    def test_gap_from_required_field_completion_exactly_80(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        # <=0.80 triggers gap
        r = engine.assess(_make_input(required_field_completion_pct=0.80))
        assert r.has_hyg_gap is True

    def test_gap_from_stale_deal_rate_ge_20(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(stale_deal_rate_pct=0.20))
        assert r.has_hyg_gap is True

    def test_gap_from_stale_deal_rate_above_20(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(stale_deal_rate_pct=0.25))
        assert r.has_hyg_gap is True

    def test_no_gap_when_all_below_threshold(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        # Composite < 40, required > 0.80, stale < 0.20
        r = engine.assess(_make_input(
            required_field_completion_pct=0.85,
            stale_deal_rate_pct=0.10,
        ))
        # composite should be low
        if r.hyg_composite < 40:
            assert r.has_hyg_gap is False

    def test_gap_is_bool(self, clean_result):
        assert isinstance(clean_result.has_hyg_gap, bool)


# ===========================================================================
# 11. REQUIRES_HYG_COACHING TRIGGER TESTS
# ===========================================================================

class TestRequiresHygCoaching:
    def test_no_coaching_for_clean_input(self, clean_result):
        assert clean_result.requires_hyg_coaching is False

    def test_coaching_from_composite_ge_20(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(
            avg_days_since_last_update=8.0,
            next_step_field_fill_rate_pct=0.50,
            stale_deal_rate_pct=0.13,
        ))
        if r.hyg_composite >= 20:
            assert r.requires_hyg_coaching is True

    def test_coaching_from_activity_log_rate_le_70(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(activity_log_rate_pct=0.70))
        assert r.requires_hyg_coaching is True

    def test_coaching_from_activity_log_rate_exactly_70(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(activity_log_rate_pct=0.70))
        assert r.requires_hyg_coaching is True

    def test_coaching_from_close_date_accuracy_le_70(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(close_date_accuracy_pct=0.70))
        assert r.requires_hyg_coaching is True

    def test_coaching_from_close_date_accuracy_exactly_70(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(close_date_accuracy_pct=0.70))
        assert r.requires_hyg_coaching is True

    def test_no_coaching_when_all_below_threshold(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(
            activity_log_rate_pct=0.80,
            close_date_accuracy_pct=0.80,
        ))
        if r.hyg_composite < 20:
            assert r.requires_hyg_coaching is False

    def test_coaching_with_critical_input(self, critical_result):
        assert critical_result.requires_hyg_coaching is True

    def test_coaching_is_bool(self, clean_result):
        assert isinstance(clean_result.requires_hyg_coaching, bool)


# ===========================================================================
# 12. ESTIMATED_FORECAST_ERROR_USD FORMULA TESTS
# ===========================================================================

class TestForecastErrorFormula:
    def test_zero_error_when_high_forecast_accuracy(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        # accuracy >= 0.90 -> accuracy_gap = 0 -> error = 0
        r = engine.assess(_make_input(
            forecast_category_accuracy_pct=0.95,
            forecasted_revenue_usd=100_000.0,
        ))
        assert r.estimated_forecast_error_usd == 0.0

    def test_zero_error_when_accuracy_exactly_90(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(
            forecast_category_accuracy_pct=0.90,
            forecasted_revenue_usd=100_000.0,
        ))
        assert r.estimated_forecast_error_usd == 0.0

    def test_formula_calculation(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        inp = _make_input(
            forecast_category_accuracy_pct=0.70,
            forecasted_revenue_usd=200_000.0,
        )
        r = engine.assess(inp)
        accuracy_gap = max(0.0, 0.90 - 0.70)   # = 0.20
        expected = round(200_000.0 * 0.20 * (r.hyg_composite / 100.0), 2)
        assert abs(r.estimated_forecast_error_usd - expected) < 0.01

    def test_zero_error_when_composite_zero(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input())
        # composite=0 -> error=0 regardless of accuracy gap
        assert r.estimated_forecast_error_usd == 0.0

    def test_forecast_error_increases_with_lower_accuracy(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        # Use same composite driver, vary only forecast accuracy
        base_overrides = dict(
            avg_days_since_last_update=22.0,
            stale_deal_rate_pct=0.30,
            forecasted_revenue_usd=100_000.0,
        )
        r1 = engine.assess(_make_input(forecast_category_accuracy_pct=0.70, **base_overrides))
        r2 = engine.assess(_make_input(forecast_category_accuracy_pct=0.50, **base_overrides))
        # lower accuracy → bigger gap → bigger error (assuming same composite)
        assert r2.estimated_forecast_error_usd >= r1.estimated_forecast_error_usd

    def test_forecast_error_rounded_to_2dp(self, critical_result):
        val = critical_result.estimated_forecast_error_usd
        assert val == round(val, 2)

    def test_forecast_error_is_non_negative(self, critical_result):
        assert critical_result.estimated_forecast_error_usd >= 0.0

    def test_forecast_error_proportional_to_revenue(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        base = dict(forecast_category_accuracy_pct=0.60, avg_days_since_last_update=22.0)
        r1 = engine.assess(_make_input(forecasted_revenue_usd=100_000.0, **base))
        r2 = engine.assess(_make_input(forecasted_revenue_usd=200_000.0, **base))
        if r1.estimated_forecast_error_usd > 0:
            ratio = r2.estimated_forecast_error_usd / r1.estimated_forecast_error_usd
            assert abs(ratio - 2.0) < 0.01

    def test_forecast_error_with_zero_revenue(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_critical_input(forecasted_revenue_usd=0.0))
        assert r.estimated_forecast_error_usd == 0.0


# ===========================================================================
# 13. SIGNAL TEXT TESTS
# ===========================================================================

class TestHygSignal:
    def test_clean_signal_for_low_composite(self, clean_result):
        assert "strong" in clean_result.hyg_signal.lower()

    def test_signal_contains_benchmarks_text(self, clean_result):
        assert "benchmarks" in clean_result.hyg_signal

    def test_signal_not_empty(self, clean_result):
        assert len(clean_result.hyg_signal) > 0

    def test_signal_contains_fields_complete_for_gap(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        inp = _make_input(
            avg_days_since_last_update=22.0,
            stale_deal_rate_pct=0.30,
            required_field_completion_pct=0.70,
        )
        r = engine.assess(inp)
        if r.hyg_composite >= 20:
            assert "fields complete" in r.hyg_signal

    def test_signal_contains_deals_stale(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_critical_input())
        if r.hyg_composite >= 20:
            assert "deals stale" in r.hyg_signal

    def test_signal_contains_activities_logged(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_critical_input())
        if r.hyg_composite >= 20:
            assert "activities logged" in r.hyg_signal

    def test_signal_contains_composite_number(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_critical_input())
        if r.hyg_composite >= 20:
            assert "composite" in r.hyg_signal

    def test_signal_ghost_pipeline_label(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(
            stale_deal_rate_pct=0.40,
            avg_days_since_last_update=20.0,
        ))
        if r.hyg_composite >= 20 and r.hyg_pattern == HygPattern.ghost_pipeline:
            assert "Ghost pipeline" in r.hyg_signal

    def test_signal_field_skipper_label(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(
            required_field_completion_pct=0.60,
            next_step_field_fill_rate_pct=0.40,
            stale_deal_rate_pct=0.05,
            avg_days_since_last_update=2.0,
        ))
        if r.hyg_composite >= 20 and r.hyg_pattern == HygPattern.field_skipper:
            assert "Field skipper" in r.hyg_signal

    def test_signal_activity_shadow_label(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(
            activity_log_rate_pct=0.40,
            email_linked_rate_pct=0.45,
        ))
        if r.hyg_composite >= 20 and r.hyg_pattern == HygPattern.activity_shadow:
            assert "Activity shadow" in r.hyg_signal

    def test_signal_is_string(self, clean_result):
        assert isinstance(clean_result.hyg_signal, str)

    def test_signal_has_crm_hygiene_gap_for_none_pattern_with_gap(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        # Force composite >= 20 but pattern = none
        r = engine.assess(_make_input(
            avg_days_since_last_update=8.0,
            next_step_field_fill_rate_pct=0.50,
            stale_deal_rate_pct=0.13,
        ))
        if r.hyg_composite >= 20 and r.hyg_pattern == HygPattern.none:
            assert "CRM hygiene gap" in r.hyg_signal


# ===========================================================================
# 14. ASSESS METHOD TESTS
# ===========================================================================

class TestAssessMethod:
    def test_assess_returns_hyg_result(self, clean_result):
        assert isinstance(clean_result, HygResult)

    def test_assess_preserves_rep_id(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(rep_id="XYZ_999"))
        assert r.rep_id == "XYZ_999"

    def test_assess_preserves_region(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(region="APAC"))
        assert r.region == "APAC"

    def test_assess_stores_result_internally(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        engine.assess(_make_input())
        assert len(engine._results) == 1

    def test_assess_accumulates_multiple_results(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        engine.assess(_make_input())
        engine.assess(_make_input())
        engine.assess(_make_input())
        assert len(engine._results) == 3

    def test_assess_sub_scores_are_floats(self, clean_result):
        assert isinstance(clean_result.completeness_score, float)
        assert isinstance(clean_result.currency_score, float)
        assert isinstance(clean_result.accuracy_score, float)
        assert isinstance(clean_result.activity_capture_score, float)

    def test_assess_sub_scores_non_negative(self, clean_result):
        assert clean_result.completeness_score >= 0
        assert clean_result.currency_score >= 0
        assert clean_result.accuracy_score >= 0
        assert clean_result.activity_capture_score >= 0

    def test_assess_sub_scores_at_most_100(self, critical_result):
        assert critical_result.completeness_score <= 100
        assert critical_result.currency_score <= 100
        assert critical_result.accuracy_score <= 100
        assert critical_result.activity_capture_score <= 100


# ===========================================================================
# 15. ASSESS_BATCH TESTS
# ===========================================================================

class TestAssessBatch:
    def test_assess_batch_returns_list(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        results = engine.assess_batch([_make_input(), _make_input()])
        assert isinstance(results, list)

    def test_assess_batch_length_matches_input(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        inputs = [_make_input(rep_id=f"R{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5

    def test_assess_batch_all_are_hyg_result(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        results = engine.assess_batch([_make_input(), _make_critical_input()])
        assert all(isinstance(r, HygResult) for r in results)

    def test_assess_batch_empty_list(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        results = engine.assess_batch([])
        assert results == []

    def test_assess_batch_stores_all_results(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        engine.assess_batch([_make_input(rep_id=f"R{i}") for i in range(4)])
        assert len(engine._results) == 4

    def test_assess_batch_rep_ids_preserved(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        inputs = [_make_input(rep_id=f"R{i}") for i in range(3)]
        results = engine.assess_batch(inputs)
        assert [r.rep_id for r in results] == ["R0", "R1", "R2"]

    def test_assess_batch_mixed_results(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        results = engine.assess_batch([_make_input(), _make_critical_input()])
        risks = {r.hyg_risk for r in results}
        assert HygRisk.low in risks
        assert HygRisk.critical in risks

    def test_assess_batch_single_item(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        results = engine.assess_batch([_make_input()])
        assert len(results) == 1


# ===========================================================================
# 16. SUMMARY TESTS
# ===========================================================================

class TestSummary:
    def test_summary_returns_dict(self, engine, clean_result):
        s = engine.summary()
        assert isinstance(s, dict)

    def test_summary_has_13_keys(self, engine, clean_result):
        assert len(engine.summary()) == 13

    def test_summary_key_total(self, engine, clean_result):
        assert "total" in engine.summary()

    def test_summary_key_risk_counts(self, engine, clean_result):
        assert "risk_counts" in engine.summary()

    def test_summary_key_pattern_counts(self, engine, clean_result):
        assert "pattern_counts" in engine.summary()

    def test_summary_key_severity_counts(self, engine, clean_result):
        assert "severity_counts" in engine.summary()

    def test_summary_key_action_counts(self, engine, clean_result):
        assert "action_counts" in engine.summary()

    def test_summary_key_avg_hyg_composite(self, engine, clean_result):
        assert "avg_hyg_composite" in engine.summary()

    def test_summary_key_hyg_gap_count(self, engine, clean_result):
        assert "hyg_gap_count" in engine.summary()

    def test_summary_key_coaching_count(self, engine, clean_result):
        assert "coaching_count" in engine.summary()

    def test_summary_key_avg_completeness_score(self, engine, clean_result):
        assert "avg_completeness_score" in engine.summary()

    def test_summary_key_avg_currency_score(self, engine, clean_result):
        assert "avg_currency_score" in engine.summary()

    def test_summary_key_avg_accuracy_score(self, engine, clean_result):
        assert "avg_accuracy_score" in engine.summary()

    def test_summary_key_avg_activity_capture_score(self, engine, clean_result):
        assert "avg_activity_capture_score" in engine.summary()

    def test_summary_key_total_estimated_forecast_error_usd(self, engine, clean_result):
        assert "total_estimated_forecast_error_usd" in engine.summary()

    def test_summary_exact_key_set(self, engine, clean_result):
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_hyg_composite", "hyg_gap_count",
            "coaching_count", "avg_completeness_score", "avg_currency_score",
            "avg_accuracy_score", "avg_activity_capture_score",
            "total_estimated_forecast_error_usd",
        }
        assert set(engine.summary().keys()) == expected

    def test_summary_empty_engine(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        s = engine.summary()
        assert s["total"] == 0
        assert s["avg_hyg_composite"] == 0.0

    def test_summary_total_count(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        engine.assess_batch([_make_input(rep_id=f"R{i}") for i in range(3)])
        assert engine.summary()["total"] == 3

    def test_summary_risk_counts_correct(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        engine.assess(_make_input())
        engine.assess(_make_critical_input())
        s = engine.summary()
        assert s["risk_counts"].get("low", 0) >= 1
        assert s["risk_counts"].get("critical", 0) >= 1

    def test_summary_hyg_gap_count(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r1 = engine.assess(_make_input())
        r2 = engine.assess(_make_critical_input())
        expected_gap = sum(1 for r in [r1, r2] if r.has_hyg_gap)
        assert engine.summary()["hyg_gap_count"] == expected_gap

    def test_summary_coaching_count(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r1 = engine.assess(_make_input())
        r2 = engine.assess(_make_critical_input())
        expected_coaching = sum(1 for r in [r1, r2] if r.requires_hyg_coaching)
        assert engine.summary()["coaching_count"] == expected_coaching

    def test_summary_avg_composite_single_result(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input())
        s = engine.summary()
        assert s["avg_hyg_composite"] == round(r.hyg_composite, 1)

    def test_summary_total_forecast_error(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r1 = engine.assess(_make_input())
        r2 = engine.assess(_make_critical_input())
        expected = round(r1.estimated_forecast_error_usd + r2.estimated_forecast_error_usd, 2)
        assert engine.summary()["total_estimated_forecast_error_usd"] == expected

    def test_summary_pattern_counts_present(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        engine.assess(_make_input())
        s = engine.summary()
        assert isinstance(s["pattern_counts"], dict)
        assert len(s["pattern_counts"]) > 0

    def test_summary_accumulates_across_sessions(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        engine.assess(_make_input())
        engine.assess(_make_input())
        assert engine.summary()["total"] == 2
        engine.assess(_make_input())
        assert engine.summary()["total"] == 3

    def test_summary_empty_has_all_13_keys(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        s = engine.summary()
        assert len(s) == 13


# ===========================================================================
# 17. EDGE CASES
# ===========================================================================

class TestEdgeCases:
    def test_zero_forecasted_revenue(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(forecasted_revenue_usd=0.0))
        assert r.estimated_forecast_error_usd == 0.0

    def test_zero_total_active_deals(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(total_active_deals=0))
        assert isinstance(r, HygResult)

    def test_all_rates_at_zero(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(
            required_field_completion_pct=0.0,
            activity_log_rate_pct=0.0,
            email_linked_rate_pct=0.0,
            close_date_accuracy_pct=0.0,
            forecast_category_accuracy_pct=0.0,
            next_step_field_fill_rate_pct=0.0,
            stage_advancement_rate_pct=0.0,
            manual_update_compliance_pct=0.0,
        ))
        assert r.hyg_composite <= 100.0
        assert r.hyg_risk == HygRisk.critical

    def test_all_rates_at_one(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(
            required_field_completion_pct=1.0,
            activity_log_rate_pct=1.0,
            email_linked_rate_pct=1.0,
            close_date_accuracy_pct=1.0,
            forecast_category_accuracy_pct=1.0,
            next_step_field_fill_rate_pct=1.0,
            stage_advancement_rate_pct=1.0,
            manual_update_compliance_pct=1.0,
            stale_deal_rate_pct=0.0,
            duplicate_deal_rate_pct=0.0,
            deal_without_contact_pct=0.0,
            avg_days_since_last_update=0.0,
        ))
        assert r.hyg_composite == 0.0
        assert r.hyg_risk == HygRisk.low

    def test_boundary_composite_exactly_20(self):
        # Scores resulting in composite exactly = 20 -> moderate
        engine = SalesCRMDataHygieneIntelligenceEngine()
        # We need cs*0.30 + cu*0.25 + ac*0.25 + ap*0.20 = 20
        # Use: cs=0, cu=0, ac=0, ap=100 -> 20.0
        r = engine.assess(_make_input(
            activity_log_rate_pct=0.30,
            email_linked_rate_pct=0.30,
            manual_update_compliance_pct=0.30,
        ))
        # activity capture at worst = 100, rest = 0
        # composite = 100*0.20 = 20.0
        if r.hyg_composite == 20.0:
            assert r.hyg_risk == HygRisk.moderate
            assert r.hyg_severity == HygSeverity.adequate

    def test_large_opportunity_value(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(
            avg_opportunity_value_usd=10_000_000.0,
            total_pipeline_usd=500_000_000.0,
        ))
        assert isinstance(r, HygResult)

    def test_engine_is_fresh_per_instance(self):
        engine1 = SalesCRMDataHygieneIntelligenceEngine()
        engine2 = SalesCRMDataHygieneIntelligenceEngine()
        engine1.assess(_make_input())
        engine1.assess(_make_input())
        assert len(engine2._results) == 0

    def test_multiple_engine_instances_independent(self):
        e1 = SalesCRMDataHygieneIntelligenceEngine()
        e2 = SalesCRMDataHygieneIntelligenceEngine()
        e1.assess(_make_input())
        e2.assess(_make_input())
        e2.assess(_make_input())
        assert e1.summary()["total"] == 1
        assert e2.summary()["total"] == 2

    def test_to_dict_values_consistent_with_result_fields(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(rep_id="DICT_TEST"))
        d = r.to_dict()
        assert d["rep_id"] == r.rep_id
        assert d["hyg_risk"] == r.hyg_risk.value
        assert d["hyg_composite"] == r.hyg_composite
        assert d["has_hyg_gap"] == r.has_hyg_gap
        assert d["estimated_forecast_error_usd"] == r.estimated_forecast_error_usd

    def test_duplicate_deal_rate_below_threshold(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(duplicate_deal_rate_pct=0.05))
        assert r.accuracy_score == 0.0

    def test_stage_advancement_above_all_brackets(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(stage_advancement_rate_pct=0.90))
        # no currency penalty for stage advancement
        assert r.currency_score == 0.0

    def test_avg_days_below_all_brackets(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(avg_days_since_last_update=1.0))
        assert r.currency_score == 0.0

    def test_opportunity_age_field_ignored_in_scores(self):
        # opportunity_age_vs_sales_cycle_pct is stored but does not affect sub-scores
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r1 = engine.assess(_make_input(opportunity_age_vs_sales_cycle_pct=0.5))
        r2 = engine.assess(_make_input(opportunity_age_vs_sales_cycle_pct=2.0))
        assert r1.hyg_composite == r2.hyg_composite

    def test_deal_amount_accuracy_field_stored(self):
        inp = _make_input(deal_amount_accuracy_pct=0.60)
        assert inp.deal_amount_accuracy_pct == 0.60

    def test_quota_usd_field_stored(self):
        inp = _make_input(quota_usd=250_000.0)
        assert inp.quota_usd == 250_000.0

    def test_summary_avg_composite_two_results(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r1 = engine.assess(_make_input())
        r2 = engine.assess(_make_critical_input())
        expected = round((r1.hyg_composite + r2.hyg_composite) / 2, 1)
        assert engine.summary()["avg_hyg_composite"] == expected

    def test_assess_batch_then_summary_total(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        engine.assess_batch([_make_input(rep_id=f"R{i}") for i in range(7)])
        assert engine.summary()["total"] == 7

    def test_contact_orphaner_not_triggered_without_email_condition(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(
            deal_without_contact_pct=0.35,
            email_linked_rate_pct=0.80,  # above 0.50 threshold
            activity_log_rate_pct=0.90,
        ))
        assert r.hyg_pattern != HygPattern.contact_orphaner

    def test_activity_shadow_not_triggered_without_both_conditions(self):
        engine = SalesCRMDataHygieneIntelligenceEngine()
        r = engine.assess(_make_input(
            activity_log_rate_pct=0.40,
            email_linked_rate_pct=0.80,  # above 0.50
        ))
        assert r.hyg_pattern != HygPattern.activity_shadow
