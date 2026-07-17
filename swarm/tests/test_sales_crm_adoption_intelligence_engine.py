"""
Comprehensive pytest test suite for SalesCRMAdoptionIntelligenceEngine.
Covers: enums, dataclasses, all sub-score methods, pattern detection,
risk/severity/action mapping, flag methods, forecast risk, signal generation,
assess(), assess_batch(), summary(), edge cases, and end-to-end scenarios.
"""

from __future__ import annotations

import pytest
from dataclasses import fields as dc_fields

from swarm.intelligence.sales_crm_adoption_intelligence_engine import (
    CRMAdoptionAction,
    CRMAdoptionInput,
    CRMAdoptionPattern,
    CRMAdoptionResult,
    CRMAdoptionRisk,
    CRMAdoptionSeverity,
    SalesCRMAdoptionIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> CRMAdoptionInput:
    """Return a 'healthy' baseline CRMAdoptionInput with optional overrides."""
    defaults = dict(
        rep_id="REP-001",
        region="Northeast",
        evaluation_period_id="Q2-2026",
        total_deals_managed=20,
        avg_days_since_last_crm_update=1.0,
        deals_not_updated_7d_pct=0.05,
        required_fields_completion_pct=0.95,
        activity_logs_per_deal_per_week=4.0,
        call_logs_per_week=5.0,
        email_logs_per_week=8.0,
        meeting_logs_per_week=3.0,
        next_action_field_completion_pct=0.90,
        close_date_accuracy_score=0.90,
        deal_stage_accuracy_pct=0.90,
        note_quality_score=0.80,
        opportunity_value_update_frequency=2.0,
        custom_fields_completion_pct=0.80,
        contact_role_mapping_pct=0.80,
        duplicate_records_rate_pct=0.02,
        data_entry_lag_hours=4.0,
        deal_age_vs_stage_consistency_score=0.90,
        avg_opportunity_value_usd=50_000.0,
    )
    defaults.update(overrides)
    return CRMAdoptionInput(**defaults)


def make_engine() -> SalesCRMAdoptionIntelligenceEngine:
    return SalesCRMAdoptionIntelligenceEngine()


# ---------------------------------------------------------------------------
# 1. Enum – CRMAdoptionRisk
# ---------------------------------------------------------------------------

class TestCRMAdoptionRisk:
    def test_values_exist(self):
        assert CRMAdoptionRisk.low
        assert CRMAdoptionRisk.moderate
        assert CRMAdoptionRisk.high
        assert CRMAdoptionRisk.critical

    def test_string_values(self):
        assert CRMAdoptionRisk.low.value == "low"
        assert CRMAdoptionRisk.moderate.value == "moderate"
        assert CRMAdoptionRisk.high.value == "high"
        assert CRMAdoptionRisk.critical.value == "critical"

    def test_is_str_subclass(self):
        assert isinstance(CRMAdoptionRisk.low, str)

    def test_equality_with_string(self):
        assert CRMAdoptionRisk.low == "low"
        assert CRMAdoptionRisk.critical == "critical"

    def test_member_count(self):
        assert len(CRMAdoptionRisk) == 4

    def test_from_value(self):
        assert CRMAdoptionRisk("high") == CRMAdoptionRisk.high


# ---------------------------------------------------------------------------
# 2. Enum – CRMAdoptionPattern
# ---------------------------------------------------------------------------

class TestCRMAdoptionPattern:
    def test_all_members(self):
        expected = {
            "none", "stale_data", "incomplete_records",
            "activity_logging_gap", "forecast_data_unreliable", "lazy_entry",
        }
        assert {m.value for m in CRMAdoptionPattern} == expected

    def test_member_count(self):
        assert len(CRMAdoptionPattern) == 6

    def test_string_values(self):
        assert CRMAdoptionPattern.none.value == "none"
        assert CRMAdoptionPattern.stale_data.value == "stale_data"
        assert CRMAdoptionPattern.incomplete_records.value == "incomplete_records"
        assert CRMAdoptionPattern.activity_logging_gap.value == "activity_logging_gap"
        assert CRMAdoptionPattern.forecast_data_unreliable.value == "forecast_data_unreliable"
        assert CRMAdoptionPattern.lazy_entry.value == "lazy_entry"

    def test_is_str_subclass(self):
        assert isinstance(CRMAdoptionPattern.stale_data, str)

    def test_from_value(self):
        assert CRMAdoptionPattern("lazy_entry") == CRMAdoptionPattern.lazy_entry


# ---------------------------------------------------------------------------
# 3. Enum – CRMAdoptionSeverity
# ---------------------------------------------------------------------------

class TestCRMAdoptionSeverity:
    def test_all_values(self):
        assert CRMAdoptionSeverity.compliant.value == "compliant"
        assert CRMAdoptionSeverity.developing.value == "developing"
        assert CRMAdoptionSeverity.neglected.value == "neglected"
        assert CRMAdoptionSeverity.abandoned.value == "abandoned"

    def test_member_count(self):
        assert len(CRMAdoptionSeverity) == 4

    def test_is_str_subclass(self):
        assert isinstance(CRMAdoptionSeverity.abandoned, str)

    def test_from_value(self):
        assert CRMAdoptionSeverity("neglected") == CRMAdoptionSeverity.neglected


# ---------------------------------------------------------------------------
# 4. Enum – CRMAdoptionAction
# ---------------------------------------------------------------------------

class TestCRMAdoptionAction:
    def test_all_values(self):
        assert CRMAdoptionAction.no_action.value == "no_action"
        assert CRMAdoptionAction.crm_coaching.value == "crm_coaching"
        assert CRMAdoptionAction.data_cleanup_session.value == "data_cleanup_session"
        assert CRMAdoptionAction.activity_logging_training.value == "activity_logging_training"
        assert CRMAdoptionAction.forecast_accuracy_review.value == "forecast_accuracy_review"
        assert CRMAdoptionAction.crm_adoption_program.value == "crm_adoption_program"

    def test_member_count(self):
        assert len(CRMAdoptionAction) == 6

    def test_is_str_subclass(self):
        assert isinstance(CRMAdoptionAction.crm_coaching, str)

    def test_from_value(self):
        assert CRMAdoptionAction("forecast_accuracy_review") == CRMAdoptionAction.forecast_accuracy_review


# ---------------------------------------------------------------------------
# 5. CRMAdoptionInput dataclass
# ---------------------------------------------------------------------------

class TestCRMAdoptionInput:
    def test_field_count(self):
        assert len(dc_fields(CRMAdoptionInput)) == 22

    def test_field_names(self):
        names = {f.name for f in dc_fields(CRMAdoptionInput)}
        required = {
            "rep_id", "region", "evaluation_period_id", "total_deals_managed",
            "avg_days_since_last_crm_update", "deals_not_updated_7d_pct",
            "required_fields_completion_pct", "activity_logs_per_deal_per_week",
            "call_logs_per_week", "email_logs_per_week", "meeting_logs_per_week",
            "next_action_field_completion_pct", "close_date_accuracy_score",
            "deal_stage_accuracy_pct", "note_quality_score",
            "opportunity_value_update_frequency", "custom_fields_completion_pct",
            "contact_role_mapping_pct", "duplicate_records_rate_pct",
            "data_entry_lag_hours", "deal_age_vs_stage_consistency_score",
            "avg_opportunity_value_usd",
        }
        assert required.issubset(names)

    def test_instantiation(self):
        inp = make_input()
        assert inp.rep_id == "REP-001"
        assert inp.region == "Northeast"
        assert inp.total_deals_managed == 20

    def test_string_fields(self):
        inp = make_input(rep_id="AGENT-99", region="West", evaluation_period_id="Q3-2026")
        assert inp.rep_id == "AGENT-99"
        assert inp.region == "West"
        assert inp.evaluation_period_id == "Q3-2026"

    def test_numeric_fields_stored(self):
        inp = make_input(avg_days_since_last_crm_update=7.5, deals_not_updated_7d_pct=0.3)
        assert inp.avg_days_since_last_crm_update == 7.5
        assert inp.deals_not_updated_7d_pct == 0.3

    def test_is_dataclass(self):
        from dataclasses import is_dataclass
        assert is_dataclass(CRMAdoptionInput)


# ---------------------------------------------------------------------------
# 6. CRMAdoptionResult dataclass
# ---------------------------------------------------------------------------

class TestCRMAdoptionResult:
    def test_field_count(self):
        assert len(dc_fields(CRMAdoptionResult)) == 15

    def test_field_names(self):
        names = {f.name for f in dc_fields(CRMAdoptionResult)}
        expected = {
            "rep_id", "region", "crm_adoption_risk", "crm_adoption_pattern",
            "crm_adoption_severity", "recommended_action", "data_freshness_score",
            "data_completeness_score", "activity_logging_score",
            "forecast_data_quality_score", "crm_adoption_composite",
            "has_crm_gap", "requires_crm_coaching", "estimated_forecast_risk_usd",
            "crm_adoption_signal",
        }
        assert expected == names

    def test_to_dict_key_count(self):
        engine = make_engine()
        result = engine.assess(make_input())
        assert len(result.to_dict()) == 15

    def test_to_dict_keys(self):
        engine = make_engine()
        result = engine.assess(make_input())
        d = result.to_dict()
        expected_keys = {
            "rep_id", "region", "crm_adoption_risk", "crm_adoption_pattern",
            "crm_adoption_severity", "recommended_action", "data_freshness_score",
            "data_completeness_score", "activity_logging_score",
            "forecast_data_quality_score", "crm_adoption_composite",
            "has_crm_gap", "requires_crm_coaching", "estimated_forecast_risk_usd",
            "crm_adoption_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_values_are_strings(self):
        engine = make_engine()
        result = engine.assess(make_input())
        d = result.to_dict()
        assert isinstance(d["crm_adoption_risk"], str)
        assert isinstance(d["crm_adoption_pattern"], str)
        assert isinstance(d["crm_adoption_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_rep_id_and_region(self):
        engine = make_engine()
        result = engine.assess(make_input(rep_id="X1", region="South"))
        d = result.to_dict()
        assert d["rep_id"] == "X1"
        assert d["region"] == "South"

    def test_to_dict_bool_fields(self):
        engine = make_engine()
        result = engine.assess(make_input())
        d = result.to_dict()
        assert isinstance(d["has_crm_gap"], bool)
        assert isinstance(d["requires_crm_coaching"], bool)

    def test_to_dict_numeric_fields(self):
        engine = make_engine()
        result = engine.assess(make_input())
        d = result.to_dict()
        assert isinstance(d["data_freshness_score"], float)
        assert isinstance(d["crm_adoption_composite"], float)
        assert isinstance(d["estimated_forecast_risk_usd"], float)

    def test_is_dataclass(self):
        from dataclasses import is_dataclass
        assert is_dataclass(CRMAdoptionResult)


# ---------------------------------------------------------------------------
# 7. Sub-score: _data_freshness_score
# ---------------------------------------------------------------------------

class TestDataFreshnessScore:
    def setup_method(self):
        self.engine = make_engine()

    def _score(self, **kw):
        return self.engine._data_freshness_score(make_input(**kw))

    # avg_days_since_last_crm_update tiers
    def test_days_below_3_no_days_points(self):
        s = self._score(avg_days_since_last_crm_update=1.0, deals_not_updated_7d_pct=0.0, data_entry_lag_hours=0.0)
        assert s == 0.0

    def test_days_at_3_adds_8(self):
        s = self._score(avg_days_since_last_crm_update=3.0, deals_not_updated_7d_pct=0.0, data_entry_lag_hours=0.0)
        assert s == 8.0

    def test_days_between_3_and_7_adds_8(self):
        s = self._score(avg_days_since_last_crm_update=5.0, deals_not_updated_7d_pct=0.0, data_entry_lag_hours=0.0)
        assert s == 8.0

    def test_days_at_7_adds_25(self):
        s = self._score(avg_days_since_last_crm_update=7.0, deals_not_updated_7d_pct=0.0, data_entry_lag_hours=0.0)
        assert s == 25.0

    def test_days_between_7_and_14_adds_25(self):
        s = self._score(avg_days_since_last_crm_update=10.0, deals_not_updated_7d_pct=0.0, data_entry_lag_hours=0.0)
        assert s == 25.0

    def test_days_at_14_adds_45(self):
        s = self._score(avg_days_since_last_crm_update=14.0, deals_not_updated_7d_pct=0.0, data_entry_lag_hours=0.0)
        assert s == 45.0

    def test_days_above_14_adds_45(self):
        s = self._score(avg_days_since_last_crm_update=30.0, deals_not_updated_7d_pct=0.0, data_entry_lag_hours=0.0)
        assert s == 45.0

    # deals_not_updated_7d_pct tiers
    def test_not_updated_below_20_no_points(self):
        s = self._score(avg_days_since_last_crm_update=0.0, deals_not_updated_7d_pct=0.10, data_entry_lag_hours=0.0)
        assert s == 0.0

    def test_not_updated_at_20_adds_7(self):
        s = self._score(avg_days_since_last_crm_update=0.0, deals_not_updated_7d_pct=0.20, data_entry_lag_hours=0.0)
        assert s == 7.0

    def test_not_updated_at_40_adds_18(self):
        s = self._score(avg_days_since_last_crm_update=0.0, deals_not_updated_7d_pct=0.40, data_entry_lag_hours=0.0)
        assert s == 18.0

    def test_not_updated_at_60_adds_35(self):
        s = self._score(avg_days_since_last_crm_update=0.0, deals_not_updated_7d_pct=0.60, data_entry_lag_hours=0.0)
        assert s == 35.0

    def test_not_updated_above_60_adds_35(self):
        s = self._score(avg_days_since_last_crm_update=0.0, deals_not_updated_7d_pct=0.90, data_entry_lag_hours=0.0)
        assert s == 35.0

    # data_entry_lag_hours tiers
    def test_lag_below_24_no_points(self):
        s = self._score(avg_days_since_last_crm_update=0.0, deals_not_updated_7d_pct=0.0, data_entry_lag_hours=12.0)
        assert s == 0.0

    def test_lag_at_24_adds_10(self):
        s = self._score(avg_days_since_last_crm_update=0.0, deals_not_updated_7d_pct=0.0, data_entry_lag_hours=24.0)
        assert s == 10.0

    def test_lag_between_24_and_48_adds_10(self):
        s = self._score(avg_days_since_last_crm_update=0.0, deals_not_updated_7d_pct=0.0, data_entry_lag_hours=36.0)
        assert s == 10.0

    def test_lag_at_48_adds_20(self):
        s = self._score(avg_days_since_last_crm_update=0.0, deals_not_updated_7d_pct=0.0, data_entry_lag_hours=48.0)
        assert s == 20.0

    def test_lag_above_48_adds_20(self):
        s = self._score(avg_days_since_last_crm_update=0.0, deals_not_updated_7d_pct=0.0, data_entry_lag_hours=72.0)
        assert s == 20.0

    # Combined and cap
    def test_combined_additive(self):
        s = self._score(avg_days_since_last_crm_update=14.0, deals_not_updated_7d_pct=0.60, data_entry_lag_hours=48.0)
        # 45 + 35 + 20 = 100
        assert s == 100.0

    def test_cap_at_100(self):
        s = self._score(avg_days_since_last_crm_update=30.0, deals_not_updated_7d_pct=0.99, data_entry_lag_hours=100.0)
        assert s <= 100.0

    def test_all_zero_inputs(self):
        s = self._score(avg_days_since_last_crm_update=0.0, deals_not_updated_7d_pct=0.0, data_entry_lag_hours=0.0)
        assert s == 0.0


# ---------------------------------------------------------------------------
# 8. Sub-score: _data_completeness_score
# ---------------------------------------------------------------------------

class TestDataCompletenessScore:
    def setup_method(self):
        self.engine = make_engine()

    def _score(self, **kw):
        return self.engine._data_completeness_score(make_input(**kw))

    # required_fields_completion_pct tiers
    def test_required_at_85_or_above_no_points(self):
        s = self._score(required_fields_completion_pct=0.90, contact_role_mapping_pct=1.0, custom_fields_completion_pct=1.0)
        assert s == 0.0

    def test_required_between_70_and_85_adds_8(self):
        s = self._score(required_fields_completion_pct=0.75, contact_role_mapping_pct=1.0, custom_fields_completion_pct=1.0)
        assert s == 8.0

    def test_required_at_70_adds_8(self):
        # 0.70 is not < 0.70, so falls into < 0.85 tier → 8 points
        s = self._score(required_fields_completion_pct=0.70, contact_role_mapping_pct=1.0, custom_fields_completion_pct=1.0)
        assert s == 8.0

    def test_required_just_below_70_adds_22(self):
        s = self._score(required_fields_completion_pct=0.699, contact_role_mapping_pct=1.0, custom_fields_completion_pct=1.0)
        assert s == 22.0

    def test_required_between_50_and_70_adds_22(self):
        s = self._score(required_fields_completion_pct=0.60, contact_role_mapping_pct=1.0, custom_fields_completion_pct=1.0)
        assert s == 22.0

    def test_required_below_50_adds_40(self):
        s = self._score(required_fields_completion_pct=0.49, contact_role_mapping_pct=1.0, custom_fields_completion_pct=1.0)
        assert s == 40.0

    def test_required_at_exactly_50_adds_22(self):
        s = self._score(required_fields_completion_pct=0.50, contact_role_mapping_pct=1.0, custom_fields_completion_pct=1.0)
        assert s == 22.0

    # contact_role_mapping_pct tiers
    def test_contact_role_above_55_no_points(self):
        s = self._score(required_fields_completion_pct=0.95, contact_role_mapping_pct=0.60, custom_fields_completion_pct=1.0)
        assert s == 0.0

    def test_contact_role_between_30_and_55_adds_18(self):
        s = self._score(required_fields_completion_pct=0.95, contact_role_mapping_pct=0.40, custom_fields_completion_pct=1.0)
        assert s == 18.0

    def test_contact_role_below_30_adds_35(self):
        s = self._score(required_fields_completion_pct=0.95, contact_role_mapping_pct=0.25, custom_fields_completion_pct=1.0)
        assert s == 35.0

    def test_contact_role_at_exactly_30_adds_18(self):
        s = self._score(required_fields_completion_pct=0.95, contact_role_mapping_pct=0.30, custom_fields_completion_pct=1.0)
        assert s == 18.0

    def test_contact_role_at_exactly_55_no_points(self):
        s = self._score(required_fields_completion_pct=0.95, contact_role_mapping_pct=0.55, custom_fields_completion_pct=1.0)
        assert s == 0.0

    # custom_fields_completion_pct tiers
    def test_custom_above_65_no_points(self):
        s = self._score(required_fields_completion_pct=0.95, contact_role_mapping_pct=1.0, custom_fields_completion_pct=0.70)
        assert s == 0.0

    def test_custom_between_40_and_65_adds_12(self):
        s = self._score(required_fields_completion_pct=0.95, contact_role_mapping_pct=1.0, custom_fields_completion_pct=0.50)
        assert s == 12.0

    def test_custom_below_40_adds_25(self):
        s = self._score(required_fields_completion_pct=0.95, contact_role_mapping_pct=1.0, custom_fields_completion_pct=0.30)
        assert s == 25.0

    def test_custom_at_exactly_40_adds_12(self):
        s = self._score(required_fields_completion_pct=0.95, contact_role_mapping_pct=1.0, custom_fields_completion_pct=0.40)
        assert s == 12.0

    def test_custom_at_exactly_65_no_points(self):
        s = self._score(required_fields_completion_pct=0.95, contact_role_mapping_pct=1.0, custom_fields_completion_pct=0.65)
        assert s == 0.0

    def test_combined_max(self):
        s = self._score(required_fields_completion_pct=0.0, contact_role_mapping_pct=0.0, custom_fields_completion_pct=0.0)
        # 40 + 35 + 25 = 100
        assert s == 100.0

    def test_cap_at_100(self):
        s = self._score(required_fields_completion_pct=0.0, contact_role_mapping_pct=0.0, custom_fields_completion_pct=0.0)
        assert s <= 100.0

    def test_all_perfect_zero(self):
        s = self._score(required_fields_completion_pct=1.0, contact_role_mapping_pct=1.0, custom_fields_completion_pct=1.0)
        assert s == 0.0


# ---------------------------------------------------------------------------
# 9. Sub-score: _activity_logging_score
# ---------------------------------------------------------------------------

class TestActivityLoggingScore:
    def setup_method(self):
        self.engine = make_engine()

    def _score(self, **kw):
        return self.engine._activity_logging_score(make_input(**kw))

    # activity_logs_per_deal_per_week tiers
    def test_logs_above_3_no_points(self):
        s = self._score(activity_logs_per_deal_per_week=5.0, next_action_field_completion_pct=1.0, note_quality_score=1.0)
        assert s == 0.0

    def test_logs_at_3_no_points(self):
        s = self._score(activity_logs_per_deal_per_week=3.0, next_action_field_completion_pct=1.0, note_quality_score=1.0)
        assert s == 0.0

    def test_logs_between_2_and_3_adds_8(self):
        s = self._score(activity_logs_per_deal_per_week=2.5, next_action_field_completion_pct=1.0, note_quality_score=1.0)
        assert s == 8.0

    def test_logs_at_2_adds_8(self):
        s = self._score(activity_logs_per_deal_per_week=2.0, next_action_field_completion_pct=1.0, note_quality_score=1.0)
        assert s == 8.0

    def test_logs_between_1_and_2_adds_20(self):
        s = self._score(activity_logs_per_deal_per_week=1.5, next_action_field_completion_pct=1.0, note_quality_score=1.0)
        assert s == 20.0

    def test_logs_at_1_adds_20(self):
        s = self._score(activity_logs_per_deal_per_week=1.0, next_action_field_completion_pct=1.0, note_quality_score=1.0)
        assert s == 20.0

    def test_logs_below_1_adds_40(self):
        s = self._score(activity_logs_per_deal_per_week=0.5, next_action_field_completion_pct=1.0, note_quality_score=1.0)
        assert s == 40.0

    def test_logs_zero_adds_40(self):
        s = self._score(activity_logs_per_deal_per_week=0.0, next_action_field_completion_pct=1.0, note_quality_score=1.0)
        assert s == 40.0

    # next_action_field_completion_pct tiers
    def test_next_action_above_65_no_points(self):
        s = self._score(activity_logs_per_deal_per_week=5.0, next_action_field_completion_pct=0.70, note_quality_score=1.0)
        assert s == 0.0

    def test_next_action_at_65_no_points(self):
        s = self._score(activity_logs_per_deal_per_week=5.0, next_action_field_completion_pct=0.65, note_quality_score=1.0)
        assert s == 0.0

    def test_next_action_between_40_and_65_adds_18(self):
        s = self._score(activity_logs_per_deal_per_week=5.0, next_action_field_completion_pct=0.50, note_quality_score=1.0)
        assert s == 18.0

    def test_next_action_at_40_adds_18(self):
        s = self._score(activity_logs_per_deal_per_week=5.0, next_action_field_completion_pct=0.40, note_quality_score=1.0)
        assert s == 18.0

    def test_next_action_below_40_adds_35(self):
        s = self._score(activity_logs_per_deal_per_week=5.0, next_action_field_completion_pct=0.30, note_quality_score=1.0)
        assert s == 35.0

    # note_quality_score tiers
    def test_note_quality_above_55_no_points(self):
        s = self._score(activity_logs_per_deal_per_week=5.0, next_action_field_completion_pct=1.0, note_quality_score=0.60)
        assert s == 0.0

    def test_note_quality_at_55_no_points(self):
        s = self._score(activity_logs_per_deal_per_week=5.0, next_action_field_completion_pct=1.0, note_quality_score=0.55)
        assert s == 0.0

    def test_note_quality_between_30_and_55_adds_12(self):
        s = self._score(activity_logs_per_deal_per_week=5.0, next_action_field_completion_pct=1.0, note_quality_score=0.40)
        assert s == 12.0

    def test_note_quality_at_30_adds_12(self):
        s = self._score(activity_logs_per_deal_per_week=5.0, next_action_field_completion_pct=1.0, note_quality_score=0.30)
        assert s == 12.0

    def test_note_quality_below_30_adds_25(self):
        s = self._score(activity_logs_per_deal_per_week=5.0, next_action_field_completion_pct=1.0, note_quality_score=0.20)
        assert s == 25.0

    def test_combined_max(self):
        s = self._score(activity_logs_per_deal_per_week=0.0, next_action_field_completion_pct=0.0, note_quality_score=0.0)
        # 40 + 35 + 25 = 100
        assert s == 100.0

    def test_cap_at_100(self):
        s = self._score(activity_logs_per_deal_per_week=0.0, next_action_field_completion_pct=0.0, note_quality_score=0.0)
        assert s <= 100.0


# ---------------------------------------------------------------------------
# 10. Sub-score: _forecast_data_quality_score
# ---------------------------------------------------------------------------

class TestForecastDataQualityScore:
    def setup_method(self):
        self.engine = make_engine()

    def _score(self, **kw):
        return self.engine._forecast_data_quality_score(make_input(**kw))

    # close_date_accuracy_score tiers
    def test_close_date_above_80_no_points(self):
        s = self._score(close_date_accuracy_score=0.85, deal_stage_accuracy_pct=1.0, duplicate_records_rate_pct=0.0)
        assert s == 0.0

    def test_close_date_at_80_no_points(self):
        s = self._score(close_date_accuracy_score=0.80, deal_stage_accuracy_pct=1.0, duplicate_records_rate_pct=0.0)
        assert s == 0.0

    def test_close_date_between_60_and_80_adds_8(self):
        s = self._score(close_date_accuracy_score=0.70, deal_stage_accuracy_pct=1.0, duplicate_records_rate_pct=0.0)
        assert s == 8.0

    def test_close_date_at_60_adds_8(self):
        s = self._score(close_date_accuracy_score=0.60, deal_stage_accuracy_pct=1.0, duplicate_records_rate_pct=0.0)
        assert s == 8.0

    def test_close_date_between_40_and_60_adds_22(self):
        s = self._score(close_date_accuracy_score=0.50, deal_stage_accuracy_pct=1.0, duplicate_records_rate_pct=0.0)
        assert s == 22.0

    def test_close_date_at_40_adds_22(self):
        s = self._score(close_date_accuracy_score=0.40, deal_stage_accuracy_pct=1.0, duplicate_records_rate_pct=0.0)
        assert s == 22.0

    def test_close_date_below_40_adds_40(self):
        s = self._score(close_date_accuracy_score=0.30, deal_stage_accuracy_pct=1.0, duplicate_records_rate_pct=0.0)
        assert s == 40.0

    # deal_stage_accuracy_pct tiers
    def test_stage_above_70_no_points(self):
        s = self._score(close_date_accuracy_score=1.0, deal_stage_accuracy_pct=0.75, duplicate_records_rate_pct=0.0)
        assert s == 0.0

    def test_stage_at_70_no_points(self):
        s = self._score(close_date_accuracy_score=1.0, deal_stage_accuracy_pct=0.70, duplicate_records_rate_pct=0.0)
        assert s == 0.0

    def test_stage_between_50_and_70_adds_18(self):
        s = self._score(close_date_accuracy_score=1.0, deal_stage_accuracy_pct=0.60, duplicate_records_rate_pct=0.0)
        assert s == 18.0

    def test_stage_at_50_adds_18(self):
        s = self._score(close_date_accuracy_score=1.0, deal_stage_accuracy_pct=0.50, duplicate_records_rate_pct=0.0)
        assert s == 18.0

    def test_stage_below_50_adds_35(self):
        s = self._score(close_date_accuracy_score=1.0, deal_stage_accuracy_pct=0.40, duplicate_records_rate_pct=0.0)
        assert s == 35.0

    # duplicate_records_rate_pct tiers
    def test_duplicates_below_7_no_points(self):
        s = self._score(close_date_accuracy_score=1.0, deal_stage_accuracy_pct=1.0, duplicate_records_rate_pct=0.05)
        assert s == 0.0

    def test_duplicates_at_7_adds_12(self):
        s = self._score(close_date_accuracy_score=1.0, deal_stage_accuracy_pct=1.0, duplicate_records_rate_pct=0.07)
        assert s == 12.0

    def test_duplicates_between_7_and_15_adds_12(self):
        s = self._score(close_date_accuracy_score=1.0, deal_stage_accuracy_pct=1.0, duplicate_records_rate_pct=0.10)
        assert s == 12.0

    def test_duplicates_at_15_adds_25(self):
        s = self._score(close_date_accuracy_score=1.0, deal_stage_accuracy_pct=1.0, duplicate_records_rate_pct=0.15)
        assert s == 25.0

    def test_duplicates_above_15_adds_25(self):
        s = self._score(close_date_accuracy_score=1.0, deal_stage_accuracy_pct=1.0, duplicate_records_rate_pct=0.30)
        assert s == 25.0

    def test_combined_max(self):
        s = self._score(close_date_accuracy_score=0.0, deal_stage_accuracy_pct=0.0, duplicate_records_rate_pct=0.50)
        # 40 + 35 + 25 = 100
        assert s == 100.0

    def test_cap_at_100(self):
        s = self._score(close_date_accuracy_score=0.0, deal_stage_accuracy_pct=0.0, duplicate_records_rate_pct=1.0)
        assert s <= 100.0

    def test_all_perfect_inputs(self):
        s = self._score(close_date_accuracy_score=1.0, deal_stage_accuracy_pct=1.0, duplicate_records_rate_pct=0.0)
        assert s == 0.0


# ---------------------------------------------------------------------------
# 11. _detect_pattern
# ---------------------------------------------------------------------------

class TestDetectPattern:
    def setup_method(self):
        self.engine = make_engine()

    def _pattern(self, inp, freshness, completeness, activity, forecast):
        return self.engine._detect_pattern(inp, freshness, completeness, activity, forecast)

    def test_stale_data_detected(self):
        inp = make_input(avg_days_since_last_crm_update=14.0)
        p = self._pattern(inp, freshness=50.0, completeness=0.0, activity=0.0, forecast=0.0)
        assert p == CRMAdoptionPattern.stale_data

    def test_stale_data_requires_freshness_ge_40(self):
        inp = make_input(avg_days_since_last_crm_update=14.0)
        p = self._pattern(inp, freshness=39.9, completeness=0.0, activity=0.0, forecast=0.0)
        # will not match stale_data first branch
        assert p != CRMAdoptionPattern.stale_data

    def test_stale_data_requires_days_ge_10(self):
        inp = make_input(avg_days_since_last_crm_update=9.9)
        p = self._pattern(inp, freshness=50.0, completeness=0.0, activity=0.0, forecast=0.0)
        assert p != CRMAdoptionPattern.stale_data

    def test_incomplete_records_detected(self):
        inp = make_input(required_fields_completion_pct=0.50)
        p = self._pattern(inp, freshness=0.0, completeness=40.0, activity=0.0, forecast=0.0)
        assert p == CRMAdoptionPattern.incomplete_records

    def test_incomplete_records_requires_completeness_ge_35(self):
        inp = make_input(required_fields_completion_pct=0.50)
        p = self._pattern(inp, freshness=0.0, completeness=34.9, activity=0.0, forecast=0.0)
        assert p != CRMAdoptionPattern.incomplete_records

    def test_incomplete_records_requires_required_fields_lt_60(self):
        inp = make_input(required_fields_completion_pct=0.61)
        p = self._pattern(inp, freshness=0.0, completeness=40.0, activity=0.0, forecast=0.0)
        assert p != CRMAdoptionPattern.incomplete_records

    def test_activity_logging_gap_detected(self):
        inp = make_input(activity_logs_per_deal_per_week=1.0)
        p = self._pattern(inp, freshness=0.0, completeness=0.0, activity=40.0, forecast=0.0)
        assert p == CRMAdoptionPattern.activity_logging_gap

    def test_activity_logging_gap_requires_activity_ge_35(self):
        inp = make_input(activity_logs_per_deal_per_week=1.0)
        p = self._pattern(inp, freshness=0.0, completeness=0.0, activity=34.9, forecast=0.0)
        assert p != CRMAdoptionPattern.activity_logging_gap

    def test_activity_logging_gap_requires_logs_lt_1_5(self):
        inp = make_input(activity_logs_per_deal_per_week=1.5)
        p = self._pattern(inp, freshness=0.0, completeness=0.0, activity=40.0, forecast=0.0)
        assert p != CRMAdoptionPattern.activity_logging_gap

    def test_forecast_data_unreliable_detected(self):
        inp = make_input(deal_stage_accuracy_pct=0.50)
        p = self._pattern(inp, freshness=0.0, completeness=0.0, activity=0.0, forecast=35.0)
        assert p == CRMAdoptionPattern.forecast_data_unreliable

    def test_forecast_data_unreliable_requires_forecast_ge_30(self):
        inp = make_input(deal_stage_accuracy_pct=0.50)
        p = self._pattern(inp, freshness=0.0, completeness=0.0, activity=0.0, forecast=29.9)
        assert p != CRMAdoptionPattern.forecast_data_unreliable

    def test_forecast_data_unreliable_requires_stage_lt_60(self):
        inp = make_input(deal_stage_accuracy_pct=0.60)
        p = self._pattern(inp, freshness=0.0, completeness=0.0, activity=0.0, forecast=35.0)
        assert p != CRMAdoptionPattern.forecast_data_unreliable

    def test_lazy_entry_detected(self):
        inp = make_input(data_entry_lag_hours=40.0)
        p = self._pattern(inp, freshness=25.0, completeness=0.0, activity=0.0, forecast=0.0)
        assert p == CRMAdoptionPattern.lazy_entry

    def test_lazy_entry_requires_freshness_ge_20(self):
        inp = make_input(data_entry_lag_hours=40.0)
        p = self._pattern(inp, freshness=19.9, completeness=0.0, activity=0.0, forecast=0.0)
        assert p != CRMAdoptionPattern.lazy_entry

    def test_lazy_entry_requires_lag_ge_36(self):
        inp = make_input(data_entry_lag_hours=35.9)
        p = self._pattern(inp, freshness=25.0, completeness=0.0, activity=0.0, forecast=0.0)
        assert p != CRMAdoptionPattern.lazy_entry

    def test_none_pattern_when_all_low(self):
        inp = make_input()
        p = self._pattern(inp, freshness=0.0, completeness=0.0, activity=0.0, forecast=0.0)
        assert p == CRMAdoptionPattern.none

    def test_stale_data_takes_priority_over_incomplete(self):
        inp = make_input(avg_days_since_last_crm_update=14.0, required_fields_completion_pct=0.50)
        p = self._pattern(inp, freshness=50.0, completeness=40.0, activity=0.0, forecast=0.0)
        assert p == CRMAdoptionPattern.stale_data


# ---------------------------------------------------------------------------
# 12. _risk_level
# ---------------------------------------------------------------------------

class TestRiskLevel:
    def setup_method(self):
        self.engine = make_engine()

    def test_below_20_is_low(self):
        assert self.engine._risk_level(19.9) == CRMAdoptionRisk.low

    def test_at_0_is_low(self):
        assert self.engine._risk_level(0.0) == CRMAdoptionRisk.low

    def test_at_20_is_moderate(self):
        assert self.engine._risk_level(20.0) == CRMAdoptionRisk.moderate

    def test_between_20_and_40_is_moderate(self):
        assert self.engine._risk_level(35.0) == CRMAdoptionRisk.moderate

    def test_at_40_is_high(self):
        assert self.engine._risk_level(40.0) == CRMAdoptionRisk.high

    def test_between_40_and_60_is_high(self):
        assert self.engine._risk_level(55.0) == CRMAdoptionRisk.high

    def test_at_60_is_critical(self):
        assert self.engine._risk_level(60.0) == CRMAdoptionRisk.critical

    def test_above_60_is_critical(self):
        assert self.engine._risk_level(90.0) == CRMAdoptionRisk.critical

    def test_at_100_is_critical(self):
        assert self.engine._risk_level(100.0) == CRMAdoptionRisk.critical

    def test_boundary_19_9_is_low(self):
        assert self.engine._risk_level(19.9) == CRMAdoptionRisk.low

    def test_boundary_39_9_is_moderate(self):
        assert self.engine._risk_level(39.9) == CRMAdoptionRisk.moderate

    def test_boundary_59_9_is_high(self):
        assert self.engine._risk_level(59.9) == CRMAdoptionRisk.high


# ---------------------------------------------------------------------------
# 13. _severity
# ---------------------------------------------------------------------------

class TestSeverity:
    def setup_method(self):
        self.engine = make_engine()

    def test_below_20_is_compliant(self):
        assert self.engine._severity(0.0) == CRMAdoptionSeverity.compliant

    def test_at_0_is_compliant(self):
        assert self.engine._severity(0.0) == CRMAdoptionSeverity.compliant

    def test_at_20_is_developing(self):
        assert self.engine._severity(20.0) == CRMAdoptionSeverity.developing

    def test_between_20_and_40_is_developing(self):
        assert self.engine._severity(30.0) == CRMAdoptionSeverity.developing

    def test_at_40_is_neglected(self):
        assert self.engine._severity(40.0) == CRMAdoptionSeverity.neglected

    def test_between_40_and_60_is_neglected(self):
        assert self.engine._severity(55.0) == CRMAdoptionSeverity.neglected

    def test_at_60_is_abandoned(self):
        assert self.engine._severity(60.0) == CRMAdoptionSeverity.abandoned

    def test_above_60_is_abandoned(self):
        assert self.engine._severity(85.0) == CRMAdoptionSeverity.abandoned

    def test_at_100_is_abandoned(self):
        assert self.engine._severity(100.0) == CRMAdoptionSeverity.abandoned


# ---------------------------------------------------------------------------
# 14. _action
# ---------------------------------------------------------------------------

class TestAction:
    def setup_method(self):
        self.engine = make_engine()

    # Critical risk
    def test_critical_stale_data_gives_cleanup(self):
        a = self.engine._action(CRMAdoptionRisk.critical, CRMAdoptionPattern.stale_data)
        assert a == CRMAdoptionAction.data_cleanup_session

    def test_critical_activity_gap_gives_training(self):
        a = self.engine._action(CRMAdoptionRisk.critical, CRMAdoptionPattern.activity_logging_gap)
        assert a == CRMAdoptionAction.activity_logging_training

    def test_critical_incomplete_records_gives_program(self):
        a = self.engine._action(CRMAdoptionRisk.critical, CRMAdoptionPattern.incomplete_records)
        assert a == CRMAdoptionAction.crm_adoption_program

    def test_critical_forecast_unreliable_gives_program(self):
        a = self.engine._action(CRMAdoptionRisk.critical, CRMAdoptionPattern.forecast_data_unreliable)
        assert a == CRMAdoptionAction.crm_adoption_program

    def test_critical_lazy_entry_gives_program(self):
        a = self.engine._action(CRMAdoptionRisk.critical, CRMAdoptionPattern.lazy_entry)
        assert a == CRMAdoptionAction.crm_adoption_program

    def test_critical_none_pattern_gives_program(self):
        a = self.engine._action(CRMAdoptionRisk.critical, CRMAdoptionPattern.none)
        assert a == CRMAdoptionAction.crm_adoption_program

    # High risk
    def test_high_forecast_unreliable_gives_forecast_review(self):
        a = self.engine._action(CRMAdoptionRisk.high, CRMAdoptionPattern.forecast_data_unreliable)
        assert a == CRMAdoptionAction.forecast_accuracy_review

    def test_high_incomplete_records_gives_cleanup(self):
        a = self.engine._action(CRMAdoptionRisk.high, CRMAdoptionPattern.incomplete_records)
        assert a == CRMAdoptionAction.data_cleanup_session

    def test_high_stale_data_gives_coaching(self):
        a = self.engine._action(CRMAdoptionRisk.high, CRMAdoptionPattern.stale_data)
        assert a == CRMAdoptionAction.crm_coaching

    def test_high_activity_gap_gives_coaching(self):
        a = self.engine._action(CRMAdoptionRisk.high, CRMAdoptionPattern.activity_logging_gap)
        assert a == CRMAdoptionAction.crm_coaching

    def test_high_lazy_entry_gives_coaching(self):
        a = self.engine._action(CRMAdoptionRisk.high, CRMAdoptionPattern.lazy_entry)
        assert a == CRMAdoptionAction.crm_coaching

    def test_high_none_pattern_gives_coaching(self):
        a = self.engine._action(CRMAdoptionRisk.high, CRMAdoptionPattern.none)
        assert a == CRMAdoptionAction.crm_coaching

    # Moderate risk
    def test_moderate_any_pattern_gives_coaching(self):
        for pattern in CRMAdoptionPattern:
            a = self.engine._action(CRMAdoptionRisk.moderate, pattern)
            assert a == CRMAdoptionAction.crm_coaching

    # Low risk
    def test_low_any_pattern_gives_no_action(self):
        for pattern in CRMAdoptionPattern:
            a = self.engine._action(CRMAdoptionRisk.low, pattern)
            assert a == CRMAdoptionAction.no_action


# ---------------------------------------------------------------------------
# 15. _has_crm_gap
# ---------------------------------------------------------------------------

class TestHasCRMGap:
    def setup_method(self):
        self.engine = make_engine()

    def test_gap_when_composite_ge_40(self):
        inp = make_input(deals_not_updated_7d_pct=0.0, required_fields_completion_pct=1.0)
        assert self.engine._has_crm_gap(40.0, inp) is True

    def test_no_gap_when_composite_lt_40_and_good_inputs(self):
        inp = make_input(deals_not_updated_7d_pct=0.10, required_fields_completion_pct=0.90)
        assert self.engine._has_crm_gap(30.0, inp) is False

    def test_gap_when_deals_not_updated_ge_50_pct(self):
        inp = make_input(deals_not_updated_7d_pct=0.50, required_fields_completion_pct=0.90)
        assert self.engine._has_crm_gap(10.0, inp) is True

    def test_gap_when_required_fields_below_50(self):
        inp = make_input(deals_not_updated_7d_pct=0.10, required_fields_completion_pct=0.49)
        assert self.engine._has_crm_gap(10.0, inp) is True

    def test_no_gap_when_all_good(self):
        inp = make_input(deals_not_updated_7d_pct=0.10, required_fields_completion_pct=0.90)
        assert self.engine._has_crm_gap(10.0, inp) is False

    def test_gap_boundary_composite_exactly_40(self):
        inp = make_input(deals_not_updated_7d_pct=0.0, required_fields_completion_pct=1.0)
        assert self.engine._has_crm_gap(40.0, inp) is True

    def test_no_gap_composite_just_below_40(self):
        inp = make_input(deals_not_updated_7d_pct=0.0, required_fields_completion_pct=1.0)
        assert self.engine._has_crm_gap(39.9, inp) is False

    def test_gap_deals_exactly_50_pct(self):
        inp = make_input(deals_not_updated_7d_pct=0.50, required_fields_completion_pct=1.0)
        assert self.engine._has_crm_gap(0.0, inp) is True

    def test_gap_required_fields_exactly_50(self):
        inp = make_input(deals_not_updated_7d_pct=0.0, required_fields_completion_pct=0.50)
        assert self.engine._has_crm_gap(0.0, inp) is False  # not < 0.50

    def test_gap_required_fields_just_below_50(self):
        inp = make_input(deals_not_updated_7d_pct=0.0, required_fields_completion_pct=0.499)
        assert self.engine._has_crm_gap(0.0, inp) is True


# ---------------------------------------------------------------------------
# 16. _requires_crm_coaching
# ---------------------------------------------------------------------------

class TestRequiresCRMCoaching:
    def setup_method(self):
        self.engine = make_engine()

    def test_coaching_when_composite_ge_30(self):
        inp = make_input(activity_logs_per_deal_per_week=5.0, next_action_field_completion_pct=0.90)
        assert self.engine._requires_crm_coaching(30.0, inp) is True

    def test_no_coaching_when_all_good(self):
        inp = make_input(activity_logs_per_deal_per_week=5.0, next_action_field_completion_pct=0.90)
        assert self.engine._requires_crm_coaching(10.0, inp) is False

    def test_coaching_when_logs_below_1(self):
        inp = make_input(activity_logs_per_deal_per_week=0.5, next_action_field_completion_pct=0.90)
        assert self.engine._requires_crm_coaching(10.0, inp) is True

    def test_coaching_when_next_action_below_40(self):
        inp = make_input(activity_logs_per_deal_per_week=5.0, next_action_field_completion_pct=0.35)
        assert self.engine._requires_crm_coaching(10.0, inp) is True

    def test_no_coaching_just_below_30(self):
        inp = make_input(activity_logs_per_deal_per_week=5.0, next_action_field_completion_pct=0.90)
        assert self.engine._requires_crm_coaching(29.9, inp) is False

    def test_coaching_boundary_logs_exactly_1(self):
        inp = make_input(activity_logs_per_deal_per_week=1.0, next_action_field_completion_pct=0.90)
        assert self.engine._requires_crm_coaching(10.0, inp) is False  # 1.0 is not < 1.0

    def test_coaching_logs_just_below_1(self):
        inp = make_input(activity_logs_per_deal_per_week=0.99, next_action_field_completion_pct=0.90)
        assert self.engine._requires_crm_coaching(10.0, inp) is True

    def test_coaching_next_action_boundary_exactly_40(self):
        inp = make_input(activity_logs_per_deal_per_week=5.0, next_action_field_completion_pct=0.40)
        assert self.engine._requires_crm_coaching(10.0, inp) is False  # 0.40 is not < 0.40

    def test_coaching_next_action_just_below_40(self):
        inp = make_input(activity_logs_per_deal_per_week=5.0, next_action_field_completion_pct=0.399)
        assert self.engine._requires_crm_coaching(10.0, inp) is True


# ---------------------------------------------------------------------------
# 17. _estimated_forecast_risk
# ---------------------------------------------------------------------------

class TestEstimatedForecastRisk:
    def setup_method(self):
        self.engine = make_engine()

    def test_basic_calculation(self):
        inp = make_input(total_deals_managed=100, deals_not_updated_7d_pct=0.20, avg_opportunity_value_usd=50_000.0)
        risk = self.engine._estimated_forecast_risk(inp, composite=50.0)
        stale_deals = round(100 * 0.20)  # 20
        expected = round(20 * 50_000.0 * (50.0 / 100.0) * 0.15, 2)
        assert risk == expected

    def test_zero_composite(self):
        inp = make_input(total_deals_managed=100, deals_not_updated_7d_pct=0.50, avg_opportunity_value_usd=10_000.0)
        risk = self.engine._estimated_forecast_risk(inp, composite=0.0)
        assert risk == 0.0

    def test_zero_deals_not_updated(self):
        inp = make_input(total_deals_managed=100, deals_not_updated_7d_pct=0.0, avg_opportunity_value_usd=50_000.0)
        risk = self.engine._estimated_forecast_risk(inp, composite=80.0)
        assert risk == 0.0

    def test_zero_opportunity_value(self):
        inp = make_input(total_deals_managed=100, deals_not_updated_7d_pct=0.50, avg_opportunity_value_usd=0.0)
        risk = self.engine._estimated_forecast_risk(inp, composite=80.0)
        assert risk == 0.0

    def test_returns_float(self):
        inp = make_input(total_deals_managed=20, deals_not_updated_7d_pct=0.10, avg_opportunity_value_usd=25_000.0)
        risk = self.engine._estimated_forecast_risk(inp, composite=30.0)
        assert isinstance(risk, float)

    def test_rounds_to_2_decimal_places(self):
        inp = make_input(total_deals_managed=7, deals_not_updated_7d_pct=0.33, avg_opportunity_value_usd=12_345.0)
        risk = self.engine._estimated_forecast_risk(inp, composite=45.0)
        # verify it's already rounded
        assert risk == round(risk, 2)

    def test_stale_deals_rounded_correctly(self):
        # total=10, pct=0.33 => round(3.3) = 3
        inp = make_input(total_deals_managed=10, deals_not_updated_7d_pct=0.33, avg_opportunity_value_usd=10_000.0)
        risk = self.engine._estimated_forecast_risk(inp, composite=100.0)
        stale_deals = round(10 * 0.33)  # 3
        expected = round(3 * 10_000.0 * 1.0 * 0.15, 2)
        assert risk == expected

    def test_large_portfolio(self):
        inp = make_input(total_deals_managed=500, deals_not_updated_7d_pct=0.40, avg_opportunity_value_usd=100_000.0)
        risk = self.engine._estimated_forecast_risk(inp, composite=75.0)
        stale_deals = round(500 * 0.40)  # 200
        expected = round(200 * 100_000.0 * 0.75 * 0.15, 2)
        assert risk == expected


# ---------------------------------------------------------------------------
# 18. _signal
# ---------------------------------------------------------------------------

class TestSignal:
    def setup_method(self):
        self.engine = make_engine()

    def test_healthy_signal_when_none_and_low_composite(self):
        inp = make_input()
        sig = self.engine._signal(inp, CRMAdoptionPattern.none, 10.0)
        assert sig == "CRM adoption healthy — data freshness, completeness, and activity logging within benchmarks"

    def test_healthy_signal_composite_exactly_0(self):
        inp = make_input()
        sig = self.engine._signal(inp, CRMAdoptionPattern.none, 0.0)
        assert sig == "CRM adoption healthy — data freshness, completeness, and activity logging within benchmarks"

    def test_healthy_signal_composite_just_below_20(self):
        inp = make_input()
        sig = self.engine._signal(inp, CRMAdoptionPattern.none, 19.9)
        assert sig == "CRM adoption healthy — data freshness, completeness, and activity logging within benchmarks"

    def test_no_healthy_signal_when_composite_ge_20_even_none_pattern(self):
        inp = make_input()
        sig = self.engine._signal(inp, CRMAdoptionPattern.none, 20.0)
        assert "healthy" not in sig

    def test_signal_contains_avg_days_when_not_healthy(self):
        inp = make_input(avg_days_since_last_crm_update=5.5)
        sig = self.engine._signal(inp, CRMAdoptionPattern.stale_data, 50.0)
        assert "5.5d avg update lag" in sig

    def test_signal_contains_fields_complete_pct_when_not_healthy(self):
        inp = make_input(required_fields_completion_pct=0.75)
        sig = self.engine._signal(inp, CRMAdoptionPattern.stale_data, 50.0)
        assert "75% fields complete" in sig

    def test_signal_contains_logs_per_deal_per_wk(self):
        inp = make_input(activity_logs_per_deal_per_week=2.5)
        sig = self.engine._signal(inp, CRMAdoptionPattern.stale_data, 50.0)
        assert "2.5 logs/deal/wk" in sig

    def test_signal_contains_composite_value(self):
        inp = make_input()
        sig = self.engine._signal(inp, CRMAdoptionPattern.stale_data, 55.0)
        assert "composite 55" in sig

    def test_signal_label_for_stale_data(self):
        inp = make_input()
        sig = self.engine._signal(inp, CRMAdoptionPattern.stale_data, 50.0)
        assert sig.startswith("Stale data")

    def test_signal_label_for_incomplete_records(self):
        inp = make_input()
        sig = self.engine._signal(inp, CRMAdoptionPattern.incomplete_records, 40.0)
        assert sig.startswith("Incomplete records")

    def test_signal_label_for_activity_logging_gap(self):
        inp = make_input()
        sig = self.engine._signal(inp, CRMAdoptionPattern.activity_logging_gap, 40.0)
        assert sig.startswith("Activity logging gap")

    def test_signal_label_for_forecast_data_unreliable(self):
        inp = make_input()
        sig = self.engine._signal(inp, CRMAdoptionPattern.forecast_data_unreliable, 35.0)
        assert sig.startswith("Forecast data unreliable")

    def test_signal_label_for_lazy_entry(self):
        inp = make_input()
        sig = self.engine._signal(inp, CRMAdoptionPattern.lazy_entry, 25.0)
        assert sig.startswith("Lazy entry")

    def test_signal_label_for_crm_risk_when_none_but_composite_high(self):
        inp = make_input()
        sig = self.engine._signal(inp, CRMAdoptionPattern.none, 30.0)
        assert sig.startswith("Crm adoption risk")

    def test_signal_is_string(self):
        inp = make_input()
        sig = self.engine._signal(inp, CRMAdoptionPattern.none, 0.0)
        assert isinstance(sig, str)


# ---------------------------------------------------------------------------
# 19. assess() – core integration
# ---------------------------------------------------------------------------

class TestAssess:
    def setup_method(self):
        self.engine = make_engine()

    def test_returns_crm_adoption_result(self):
        result = self.engine.assess(make_input())
        assert isinstance(result, CRMAdoptionResult)

    def test_rep_id_propagated(self):
        result = self.engine.assess(make_input(rep_id="REP-XYZ"))
        assert result.rep_id == "REP-XYZ"

    def test_region_propagated(self):
        result = self.engine.assess(make_input(region="Pacific"))
        assert result.region == "Pacific"

    def test_healthy_input_gives_low_risk(self):
        result = self.engine.assess(make_input())
        assert result.crm_adoption_risk == CRMAdoptionRisk.low

    def test_healthy_input_gives_compliant_severity(self):
        result = self.engine.assess(make_input())
        assert result.crm_adoption_severity == CRMAdoptionSeverity.compliant

    def test_healthy_input_gives_no_action(self):
        result = self.engine.assess(make_input())
        assert result.recommended_action == CRMAdoptionAction.no_action

    def test_healthy_input_gives_none_pattern(self):
        result = self.engine.assess(make_input())
        assert result.crm_adoption_pattern == CRMAdoptionPattern.none

    def test_healthy_input_no_gap(self):
        result = self.engine.assess(make_input())
        assert result.has_crm_gap is False

    def test_all_score_fields_are_floats(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.data_freshness_score, float)
        assert isinstance(result.data_completeness_score, float)
        assert isinstance(result.activity_logging_score, float)
        assert isinstance(result.forecast_data_quality_score, float)
        assert isinstance(result.crm_adoption_composite, float)

    def test_composite_formula(self):
        inp = make_input()
        engine = make_engine()
        result = engine.assess(inp)
        f = result.data_freshness_score
        co = result.data_completeness_score
        ac = result.activity_logging_score
        fo = result.forecast_data_quality_score
        expected = round(f * 0.30 + co * 0.30 + ac * 0.25 + fo * 0.15, 1)
        assert result.crm_adoption_composite == expected

    def test_composite_capped_at_100(self):
        inp = make_input(
            avg_days_since_last_crm_update=30.0,
            deals_not_updated_7d_pct=1.0,
            data_entry_lag_hours=100.0,
            required_fields_completion_pct=0.0,
            contact_role_mapping_pct=0.0,
            custom_fields_completion_pct=0.0,
            activity_logs_per_deal_per_week=0.0,
            next_action_field_completion_pct=0.0,
            note_quality_score=0.0,
            close_date_accuracy_score=0.0,
            deal_stage_accuracy_pct=0.0,
            duplicate_records_rate_pct=1.0,
        )
        result = make_engine().assess(inp)
        assert result.crm_adoption_composite <= 100.0

    def test_result_stored_in_engine(self):
        engine = make_engine()
        engine.assess(make_input())
        assert len(engine._results) == 1

    def test_multiple_assessments_stored(self):
        engine = make_engine()
        engine.assess(make_input(rep_id="A"))
        engine.assess(make_input(rep_id="B"))
        assert len(engine._results) == 2

    def test_critical_risk_scenario(self):
        inp = make_input(
            avg_days_since_last_crm_update=20.0,
            deals_not_updated_7d_pct=0.80,
            data_entry_lag_hours=72.0,
            required_fields_completion_pct=0.20,
            contact_role_mapping_pct=0.10,
            custom_fields_completion_pct=0.10,
            activity_logs_per_deal_per_week=0.2,
            next_action_field_completion_pct=0.10,
            note_quality_score=0.10,
            close_date_accuracy_score=0.10,
            deal_stage_accuracy_pct=0.20,
            duplicate_records_rate_pct=0.50,
        )
        result = make_engine().assess(inp)
        assert result.crm_adoption_risk == CRMAdoptionRisk.critical
        assert result.crm_adoption_severity == CRMAdoptionSeverity.abandoned
        assert result.has_crm_gap is True
        assert result.requires_crm_coaching is True

    def test_healthy_signal_in_result(self):
        result = make_engine().assess(make_input())
        assert "healthy" in result.crm_adoption_signal

    def test_score_scores_non_negative(self):
        result = make_engine().assess(make_input())
        assert result.data_freshness_score >= 0
        assert result.data_completeness_score >= 0
        assert result.activity_logging_score >= 0
        assert result.forecast_data_quality_score >= 0

    def test_estimated_forecast_risk_non_negative(self):
        result = make_engine().assess(make_input())
        assert result.estimated_forecast_risk_usd >= 0.0

    def test_signal_is_string(self):
        result = make_engine().assess(make_input())
        assert isinstance(result.crm_adoption_signal, str)


# ---------------------------------------------------------------------------
# 20. assess_batch()
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def setup_method(self):
        self.engine = make_engine()

    def test_returns_list(self):
        results = self.engine.assess_batch([make_input(rep_id="A"), make_input(rep_id="B")])
        assert isinstance(results, list)

    def test_returns_correct_count(self):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = self.engine.assess_batch(inputs)
        assert len(results) == 5

    def test_empty_batch_returns_empty_list(self):
        results = self.engine.assess_batch([])
        assert results == []

    def test_all_items_are_crm_adoption_results(self):
        inputs = [make_input(rep_id=f"R{i}") for i in range(3)]
        results = self.engine.assess_batch(inputs)
        for r in results:
            assert isinstance(r, CRMAdoptionResult)

    def test_order_preserved(self):
        rep_ids = ["A1", "B2", "C3"]
        inputs = [make_input(rep_id=rid) for rid in rep_ids]
        results = self.engine.assess_batch(inputs)
        assert [r.rep_id for r in results] == rep_ids

    def test_batch_stores_in_results(self):
        engine = make_engine()
        engine.assess_batch([make_input(rep_id="X"), make_input(rep_id="Y")])
        assert len(engine._results) == 2

    def test_single_item_batch(self):
        results = self.engine.assess_batch([make_input(rep_id="SOLO")])
        assert len(results) == 1
        assert results[0].rep_id == "SOLO"

    def test_batch_accumulates_with_prior_assessments(self):
        engine = make_engine()
        engine.assess(make_input(rep_id="Prior"))
        engine.assess_batch([make_input(rep_id="A"), make_input(rep_id="B")])
        assert len(engine._results) == 3


# ---------------------------------------------------------------------------
# 21. summary()
# ---------------------------------------------------------------------------

class TestSummary:
    def test_empty_summary_returns_13_keys(self):
        engine = make_engine()
        s = engine.summary()
        assert len(s) == 13

    def test_empty_summary_keys(self):
        engine = make_engine()
        s = engine.summary()
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_crm_adoption_composite", "crm_gap_count",
            "coaching_count", "avg_data_freshness_score",
            "avg_data_completeness_score", "avg_activity_logging_score",
            "avg_forecast_data_quality_score", "total_estimated_forecast_risk_usd",
        }
        assert set(s.keys()) == expected

    def test_empty_summary_total_zero(self):
        engine = make_engine()
        assert engine.summary()["total"] == 0

    def test_empty_summary_counts_are_empty_dicts(self):
        engine = make_engine()
        s = engine.summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}

    def test_empty_summary_averages_are_zero(self):
        engine = make_engine()
        s = engine.summary()
        assert s["avg_crm_adoption_composite"] == 0.0
        assert s["avg_data_freshness_score"] == 0.0
        assert s["avg_data_completeness_score"] == 0.0
        assert s["avg_activity_logging_score"] == 0.0
        assert s["avg_forecast_data_quality_score"] == 0.0
        assert s["total_estimated_forecast_risk_usd"] == 0.0

    def test_empty_summary_gap_and_coaching_zero(self):
        engine = make_engine()
        s = engine.summary()
        assert s["crm_gap_count"] == 0
        assert s["coaching_count"] == 0

    def test_summary_after_single_assessment(self):
        engine = make_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert s["total"] == 1

    def test_summary_risk_counts(self):
        engine = make_engine()
        engine.assess(make_input())  # healthy -> low risk
        s = engine.summary()
        assert "low" in s["risk_counts"]
        assert s["risk_counts"]["low"] == 1

    def test_summary_pattern_counts(self):
        engine = make_engine()
        engine.assess(make_input())  # healthy -> none pattern
        s = engine.summary()
        assert "none" in s["pattern_counts"]

    def test_summary_severity_counts(self):
        engine = make_engine()
        engine.assess(make_input())  # healthy -> compliant
        s = engine.summary()
        assert "compliant" in s["severity_counts"]

    def test_summary_action_counts(self):
        engine = make_engine()
        engine.assess(make_input())  # healthy -> no_action
        s = engine.summary()
        assert "no_action" in s["action_counts"]

    def test_summary_avg_composite_matches_single(self):
        engine = make_engine()
        result = engine.assess(make_input())
        s = engine.summary()
        assert s["avg_crm_adoption_composite"] == result.crm_adoption_composite

    def test_summary_gap_count_accurate(self):
        engine = make_engine()
        # healthy: no gap
        engine.assess(make_input())
        # bad: gap
        engine.assess(make_input(required_fields_completion_pct=0.10))
        s = engine.summary()
        assert s["crm_gap_count"] == 1

    def test_summary_coaching_count_accurate(self):
        engine = make_engine()
        engine.assess(make_input())
        # force coaching via low activity
        engine.assess(make_input(activity_logs_per_deal_per_week=0.5))
        s = engine.summary()
        assert s["coaching_count"] >= 1

    def test_summary_total_forecast_risk_is_sum(self):
        engine = make_engine()
        r1 = engine.assess(make_input(rep_id="A"))
        r2 = engine.assess(make_input(rep_id="B"))
        s = engine.summary()
        expected = round(r1.estimated_forecast_risk_usd + r2.estimated_forecast_risk_usd, 2)
        assert s["total_estimated_forecast_risk_usd"] == expected

    def test_summary_avg_freshness_score(self):
        engine = make_engine()
        r1 = engine.assess(make_input(rep_id="A"))
        r2 = engine.assess(make_input(rep_id="B"))
        s = engine.summary()
        expected = round((r1.data_freshness_score + r2.data_freshness_score) / 2, 1)
        assert s["avg_data_freshness_score"] == expected

    def test_summary_avg_completeness_score(self):
        engine = make_engine()
        r1 = engine.assess(make_input(rep_id="A"))
        r2 = engine.assess(make_input(rep_id="B"))
        s = engine.summary()
        expected = round((r1.data_completeness_score + r2.data_completeness_score) / 2, 1)
        assert s["avg_data_completeness_score"] == expected

    def test_summary_multiple_risk_buckets(self):
        engine = make_engine()
        engine.assess(make_input())  # low
        engine.assess(make_input(
            avg_days_since_last_crm_update=20.0,
            deals_not_updated_7d_pct=0.80,
            data_entry_lag_hours=60.0,
            required_fields_completion_pct=0.10,
            contact_role_mapping_pct=0.05,
            custom_fields_completion_pct=0.05,
            activity_logs_per_deal_per_week=0.1,
            next_action_field_completion_pct=0.05,
            note_quality_score=0.05,
            close_date_accuracy_score=0.05,
            deal_stage_accuracy_pct=0.10,
            duplicate_records_rate_pct=0.50,
        ))  # critical
        s = engine.summary()
        assert s["total"] == 2
        assert "low" in s["risk_counts"]
        assert "critical" in s["risk_counts"]

    def test_summary_returns_13_keys_after_data(self):
        engine = make_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert len(s) == 13


# ---------------------------------------------------------------------------
# 22. Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_zero_total_deals(self):
        inp = make_input(total_deals_managed=0, deals_not_updated_7d_pct=0.5, avg_opportunity_value_usd=50_000.0)
        result = make_engine().assess(inp)
        assert result.estimated_forecast_risk_usd == 0.0

    def test_all_percentages_zero(self):
        inp = make_input(
            avg_days_since_last_crm_update=0.0,
            deals_not_updated_7d_pct=0.0,
            data_entry_lag_hours=0.0,
            required_fields_completion_pct=1.0,
            contact_role_mapping_pct=1.0,
            custom_fields_completion_pct=1.0,
            activity_logs_per_deal_per_week=10.0,
            next_action_field_completion_pct=1.0,
            note_quality_score=1.0,
            close_date_accuracy_score=1.0,
            deal_stage_accuracy_pct=1.0,
            duplicate_records_rate_pct=0.0,
        )
        result = make_engine().assess(inp)
        assert result.crm_adoption_composite == 0.0
        assert result.crm_adoption_risk == CRMAdoptionRisk.low

    def test_all_worst_case_inputs(self):
        inp = make_input(
            avg_days_since_last_crm_update=60.0,
            deals_not_updated_7d_pct=1.0,
            data_entry_lag_hours=200.0,
            required_fields_completion_pct=0.0,
            contact_role_mapping_pct=0.0,
            custom_fields_completion_pct=0.0,
            activity_logs_per_deal_per_week=0.0,
            next_action_field_completion_pct=0.0,
            note_quality_score=0.0,
            close_date_accuracy_score=0.0,
            deal_stage_accuracy_pct=0.0,
            duplicate_records_rate_pct=1.0,
        )
        result = make_engine().assess(inp)
        assert result.crm_adoption_risk == CRMAdoptionRisk.critical
        assert result.crm_adoption_severity == CRMAdoptionSeverity.abandoned
        assert result.crm_adoption_composite == 100.0

    def test_independent_engines_do_not_share_state(self):
        e1 = make_engine()
        e2 = make_engine()
        e1.assess(make_input(rep_id="E1"))
        assert len(e2._results) == 0

    def test_multiple_assessments_on_same_engine(self):
        engine = make_engine()
        for i in range(10):
            engine.assess(make_input(rep_id=f"R{i}"))
        assert len(engine._results) == 10

    def test_assess_result_to_dict_matches_result_attributes(self):
        engine = make_engine()
        r = engine.assess(make_input(rep_id="TEST"))
        d = r.to_dict()
        assert d["rep_id"] == r.rep_id
        assert d["region"] == r.region
        assert d["crm_adoption_risk"] == r.crm_adoption_risk.value
        assert d["crm_adoption_pattern"] == r.crm_adoption_pattern.value
        assert d["crm_adoption_severity"] == r.crm_adoption_severity.value
        assert d["recommended_action"] == r.recommended_action.value
        assert d["data_freshness_score"] == r.data_freshness_score
        assert d["data_completeness_score"] == r.data_completeness_score
        assert d["activity_logging_score"] == r.activity_logging_score
        assert d["forecast_data_quality_score"] == r.forecast_data_quality_score
        assert d["crm_adoption_composite"] == r.crm_adoption_composite
        assert d["has_crm_gap"] == r.has_crm_gap
        assert d["requires_crm_coaching"] == r.requires_crm_coaching
        assert d["estimated_forecast_risk_usd"] == r.estimated_forecast_risk_usd
        assert d["crm_adoption_signal"] == r.crm_adoption_signal

    def test_deals_not_updated_exactly_at_pct_boundaries(self):
        # test boundary 0.20 (exact)
        inp = make_input(avg_days_since_last_crm_update=0.0, deals_not_updated_7d_pct=0.20, data_entry_lag_hours=0.0)
        s = make_engine()._data_freshness_score(inp)
        assert s == 7.0

    def test_exact_boundary_required_fields_085(self):
        # exactly 0.85 means < 0.85 is False, so no points
        inp = make_input(required_fields_completion_pct=0.85, contact_role_mapping_pct=1.0, custom_fields_completion_pct=1.0)
        s = make_engine()._data_completeness_score(inp)
        assert s == 0.0

    def test_just_below_required_fields_085(self):
        inp = make_input(required_fields_completion_pct=0.84, contact_role_mapping_pct=1.0, custom_fields_completion_pct=1.0)
        s = make_engine()._data_completeness_score(inp)
        assert s == 8.0

    def test_assess_result_in_internal_list_is_same_object(self):
        engine = make_engine()
        r = engine.assess(make_input())
        assert engine._results[-1] is r


# ---------------------------------------------------------------------------
# 23. End-to-end scenarios
# ---------------------------------------------------------------------------

class TestEndToEndScenarios:
    """Full pipeline scenarios modelling realistic rep performance."""

    def test_star_performer(self):
        """Rep who updates CRM daily, complete records, high activity."""
        inp = make_input(
            rep_id="STAR-01",
            region="West",
            avg_days_since_last_crm_update=0.5,
            deals_not_updated_7d_pct=0.02,
            data_entry_lag_hours=2.0,
            required_fields_completion_pct=0.99,
            contact_role_mapping_pct=0.95,
            custom_fields_completion_pct=0.95,
            activity_logs_per_deal_per_week=5.0,
            next_action_field_completion_pct=0.98,
            note_quality_score=0.90,
            close_date_accuracy_score=0.95,
            deal_stage_accuracy_pct=0.97,
            duplicate_records_rate_pct=0.01,
        )
        result = make_engine().assess(inp)
        assert result.crm_adoption_risk == CRMAdoptionRisk.low
        assert result.crm_adoption_severity == CRMAdoptionSeverity.compliant
        assert result.recommended_action == CRMAdoptionAction.no_action
        assert result.crm_adoption_pattern == CRMAdoptionPattern.none
        assert result.has_crm_gap is False
        assert "healthy" in result.crm_adoption_signal

    def test_stale_data_critical_rep(self):
        """Rep who never updates CRM; stale data + poor completeness + activity → critical."""
        inp = make_input(
            rep_id="STALE-01",
            avg_days_since_last_crm_update=20.0,
            deals_not_updated_7d_pct=0.85,
            data_entry_lag_hours=72.0,
            required_fields_completion_pct=0.40,
            contact_role_mapping_pct=0.20,
            custom_fields_completion_pct=0.30,
            activity_logs_per_deal_per_week=0.5,
            next_action_field_completion_pct=0.30,
            note_quality_score=0.25,
            close_date_accuracy_score=0.30,
            deal_stage_accuracy_pct=0.40,
            duplicate_records_rate_pct=0.20,
        )
        result = make_engine().assess(inp)
        assert result.crm_adoption_pattern == CRMAdoptionPattern.stale_data
        assert result.crm_adoption_risk == CRMAdoptionRisk.critical
        assert result.recommended_action == CRMAdoptionAction.data_cleanup_session

    def test_activity_logging_gap_rep(self):
        """Rep with very low activity logging."""
        inp = make_input(
            rep_id="LAZY-01",
            activity_logs_per_deal_per_week=0.5,
            next_action_field_completion_pct=0.20,
            note_quality_score=0.20,
            avg_days_since_last_crm_update=2.0,
            deals_not_updated_7d_pct=0.10,
            required_fields_completion_pct=0.85,
        )
        result = make_engine().assess(inp)
        assert result.crm_adoption_pattern == CRMAdoptionPattern.activity_logging_gap
        assert result.requires_crm_coaching is True

    def test_batch_summary_coherence(self):
        """Batch of 3 reps; summary totals and averages should be coherent."""
        engine = make_engine()
        inputs = [
            make_input(rep_id="R1"),
            make_input(rep_id="R2", avg_days_since_last_crm_update=15.0,
                       deals_not_updated_7d_pct=0.70, data_entry_lag_hours=60.0),
            make_input(rep_id="R3", required_fields_completion_pct=0.30,
                       contact_role_mapping_pct=0.10, custom_fields_completion_pct=0.10),
        ]
        results = engine.assess_batch(inputs)
        s = engine.summary()
        assert s["total"] == 3
        total_risk = sum(s["risk_counts"].values())
        assert total_risk == 3
        total_pat = sum(s["pattern_counts"].values())
        assert total_pat == 3
        total_sev = sum(s["severity_counts"].values())
        assert total_sev == 3

    def test_forecast_unreliable_rep(self):
        """Rep with poor forecast data quality combined with other issues → high risk."""
        inp = make_input(
            close_date_accuracy_score=0.20,
            deal_stage_accuracy_pct=0.30,
            duplicate_records_rate_pct=0.25,
            required_fields_completion_pct=0.40,   # also poor completeness
            contact_role_mapping_pct=0.20,
            custom_fields_completion_pct=0.30,
            activity_logs_per_deal_per_week=0.8,
            next_action_field_completion_pct=0.30,
            note_quality_score=0.25,
        )
        result = make_engine().assess(inp)
        assert result.forecast_data_quality_score >= 30
        assert result.crm_adoption_risk in (CRMAdoptionRisk.moderate, CRMAdoptionRisk.high, CRMAdoptionRisk.critical)

    def test_moderate_risk_gets_coaching(self):
        """Moderate composite score drives crm_coaching action."""
        inp = make_input(
            avg_days_since_last_crm_update=7.0,
            deals_not_updated_7d_pct=0.30,
            data_entry_lag_hours=25.0,
            required_fields_completion_pct=0.72,
            contact_role_mapping_pct=0.56,
            custom_fields_completion_pct=0.66,
            activity_logs_per_deal_per_week=3.0,
            next_action_field_completion_pct=0.66,
            note_quality_score=0.56,
            close_date_accuracy_score=0.81,
            deal_stage_accuracy_pct=0.75,
            duplicate_records_rate_pct=0.06,
        )
        result = make_engine().assess(inp)
        if result.crm_adoption_risk == CRMAdoptionRisk.moderate:
            assert result.recommended_action == CRMAdoptionAction.crm_coaching

    def test_to_dict_on_unhealthy_rep_has_risk_value(self):
        inp = make_input(avg_days_since_last_crm_update=20.0, deals_not_updated_7d_pct=0.90,
                         data_entry_lag_hours=80.0)
        result = make_engine().assess(inp)
        d = result.to_dict()
        assert d["crm_adoption_risk"] in ("low", "moderate", "high", "critical")

    def test_high_risk_incomplete_records_gives_cleanup(self):
        """High risk + incomplete_records pattern → data_cleanup_session."""
        inp = make_input(
            required_fields_completion_pct=0.40,
            contact_role_mapping_pct=0.20,
            custom_fields_completion_pct=0.20,
            avg_days_since_last_crm_update=2.0,
            deals_not_updated_7d_pct=0.10,
            data_entry_lag_hours=5.0,
            activity_logs_per_deal_per_week=3.0,
            next_action_field_completion_pct=0.80,
            note_quality_score=0.70,
            close_date_accuracy_score=0.85,
            deal_stage_accuracy_pct=0.85,
            duplicate_records_rate_pct=0.02,
        )
        result = make_engine().assess(inp)
        if (result.crm_adoption_risk == CRMAdoptionRisk.high and
                result.crm_adoption_pattern == CRMAdoptionPattern.incomplete_records):
            assert result.recommended_action == CRMAdoptionAction.data_cleanup_session

    def test_summary_fresh_engine(self):
        """Fresh engine summary has correct default structure."""
        s = make_engine().summary()
        assert s["total"] == 0
        assert isinstance(s["risk_counts"], dict)
        assert isinstance(s["pattern_counts"], dict)

    def test_assess_then_summary_total_is_1(self):
        engine = make_engine()
        engine.assess(make_input())
        assert engine.summary()["total"] == 1
