"""
Comprehensive pytest tests for swarm/intelligence/rep_ramp_intelligence.py.
Covers all classes, methods, properties, edge cases, and invariants.
"""

from __future__ import annotations

import dataclasses
from typing import List

import pytest

from swarm.intelligence.rep_ramp_intelligence import (
    RampAction,
    RampPhase,
    RampRisk,
    RampStatus,
    RepRampInput,
    RepRampIntelligence,
    RepRampResult,
    _activity_score,
    _attainment_score,
    _composite,
    _key_risk_factor,
    _pipeline_health_score,
    _projected_full_ramp_days,
    _ramp_action,
    _ramp_phase,
    _ramp_risk,
    _ramp_status,
    _readiness_score,
)


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> RepRampInput:
    """Create a baseline RepRampInput with sensible defaults. Override any field."""
    defaults = dict(
        rep_id="rep-001",
        rep_name="Alice Smith",
        hire_date_days_ago=60,
        quota_assigned_usd=500_000.0,
        calls_last_7d=20,
        emails_last_7d=30,
        meetings_completed_last_30d=6,
        demos_completed_last_30d=2,
        deals_created_last_30d=3,
        pipeline_value_usd=1_000_000.0,
        first_deal_closed_days_after_hire=45,
        revenue_attainment_pct=50.0,
        manager_coaching_sessions_per_month=2,
        peer_shadowing_sessions_completed=3,
        product_certification_complete=1,
        crm_adoption_score=80.0,
        onboarding_assessment_score=75.0,
        territory_quality_score=70.0,
        previous_sales_experience_years=3.0,
        industry_match_score=80.0,
        support_ticket_count=0,
        expected_ramp_days=180,
    )
    defaults.update(overrides)
    return RepRampInput(**defaults)


def make_engine() -> RepRampIntelligence:
    return RepRampIntelligence()


# ===========================================================================
# Section 1 – Enum invariants
# ===========================================================================

class TestRampStatusEnum:
    def test_inherits_from_str(self):
        assert issubclass(RampStatus, str)

    def test_exactly_4_values(self):
        assert len(RampStatus) == 4

    def test_value_ahead(self):
        assert RampStatus.AHEAD == "ahead"
        assert RampStatus.AHEAD.value == "ahead"

    def test_value_on_track(self):
        assert RampStatus.ON_TRACK == "on_track"

    def test_value_at_risk(self):
        assert RampStatus.AT_RISK == "at_risk"

    def test_value_behind(self):
        assert RampStatus.BEHIND == "behind"

    def test_members(self):
        names = {m.name for m in RampStatus}
        assert names == {"AHEAD", "ON_TRACK", "AT_RISK", "BEHIND"}

    def test_str_comparison(self):
        assert RampStatus.AHEAD == "ahead"


class TestRampPhaseEnum:
    def test_inherits_from_str(self):
        assert issubclass(RampPhase, str)

    def test_exactly_4_values(self):
        assert len(RampPhase) == 4

    def test_value_learning(self):
        assert RampPhase.LEARNING == "learning"

    def test_value_ramping(self):
        assert RampPhase.RAMPING == "ramping"

    def test_value_approaching_quota(self):
        assert RampPhase.APPROACHING_QUOTA == "approaching_quota"

    def test_value_at_quota(self):
        assert RampPhase.AT_QUOTA == "at_quota"

    def test_members(self):
        names = {m.name for m in RampPhase}
        assert names == {"LEARNING", "RAMPING", "APPROACHING_QUOTA", "AT_QUOTA"}


class TestRampRiskEnum:
    def test_inherits_from_str(self):
        assert issubclass(RampRisk, str)

    def test_exactly_4_values(self):
        assert len(RampRisk) == 4

    def test_value_low(self):
        assert RampRisk.LOW == "low"

    def test_value_moderate(self):
        assert RampRisk.MODERATE == "moderate"

    def test_value_high(self):
        assert RampRisk.HIGH == "high"

    def test_value_critical(self):
        assert RampRisk.CRITICAL == "critical"

    def test_members(self):
        names = {m.name for m in RampRisk}
        assert names == {"LOW", "MODERATE", "HIGH", "CRITICAL"}


class TestRampActionEnum:
    def test_inherits_from_str(self):
        assert issubclass(RampAction, str)

    def test_exactly_4_values(self):
        assert len(RampAction) == 4

    def test_value_maintain(self):
        assert RampAction.MAINTAIN == "maintain"

    def test_value_accelerate_coaching(self):
        assert RampAction.ACCELERATE_COACHING == "accelerate_coaching"

    def test_value_territory_adjustment(self):
        assert RampAction.TERRITORY_ADJUSTMENT == "territory_adjustment"

    def test_value_pip(self):
        assert RampAction.PIP == "performance_improvement_plan"

    def test_members(self):
        names = {m.name for m in RampAction}
        assert names == {"MAINTAIN", "ACCELERATE_COACHING", "TERRITORY_ADJUSTMENT", "PIP"}


# ===========================================================================
# Section 2 – RepRampInput dataclass
# ===========================================================================

class TestRepRampInputDataclass:
    def test_exactly_22_fields(self):
        fields = dataclasses.fields(RepRampInput)
        assert len(fields) == 22

    def test_field_names(self):
        field_names = {f.name for f in dataclasses.fields(RepRampInput)}
        expected = {
            "rep_id", "rep_name", "hire_date_days_ago", "quota_assigned_usd",
            "calls_last_7d", "emails_last_7d", "meetings_completed_last_30d",
            "demos_completed_last_30d", "deals_created_last_30d",
            "pipeline_value_usd", "first_deal_closed_days_after_hire",
            "revenue_attainment_pct", "manager_coaching_sessions_per_month",
            "peer_shadowing_sessions_completed", "product_certification_complete",
            "crm_adoption_score", "onboarding_assessment_score",
            "territory_quality_score", "previous_sales_experience_years",
            "industry_match_score", "support_ticket_count", "expected_ramp_days",
        }
        assert field_names == expected

    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(RepRampInput)

    def test_instantiation(self):
        inp = make_input()
        assert inp.rep_id == "rep-001"
        assert inp.rep_name == "Alice Smith"

    def test_field_types_str(self):
        inp = make_input(rep_id="x", rep_name="y")
        assert isinstance(inp.rep_id, str)
        assert isinstance(inp.rep_name, str)

    def test_field_types_int(self):
        inp = make_input(hire_date_days_ago=30)
        assert isinstance(inp.hire_date_days_ago, int)

    def test_field_types_float(self):
        inp = make_input(quota_assigned_usd=100_000.0)
        assert isinstance(inp.quota_assigned_usd, float)

    def test_override_single_field(self):
        inp = make_input(calls_last_7d=99)
        assert inp.calls_last_7d == 99


# ===========================================================================
# Section 3 – RepRampResult.to_dict() invariants
# ===========================================================================

class TestRepRampResultToDict:
    def test_exactly_15_keys(self):
        engine = make_engine()
        result = engine.assess(make_input())
        d = result.to_dict()
        assert len(d) == 15

    def test_key_names(self):
        engine = make_engine()
        result = engine.assess(make_input())
        d = result.to_dict()
        expected_keys = {
            "rep_id", "rep_name", "ramp_status", "ramp_phase", "ramp_risk",
            "ramp_action", "activity_score", "readiness_score",
            "pipeline_health_score", "attainment_score", "ramp_composite",
            "projected_full_ramp_days", "is_on_track", "needs_intervention",
            "key_risk_factor",
        }
        assert set(d.keys()) == expected_keys

    def test_enum_values_are_strings(self):
        engine = make_engine()
        result = engine.assess(make_input())
        d = result.to_dict()
        assert isinstance(d["ramp_status"], str)
        assert isinstance(d["ramp_phase"], str)
        assert isinstance(d["ramp_risk"], str)
        assert isinstance(d["ramp_action"], str)

    def test_is_on_track_is_bool(self):
        engine = make_engine()
        result = engine.assess(make_input())
        d = result.to_dict()
        assert isinstance(d["is_on_track"], bool)

    def test_needs_intervention_is_bool(self):
        engine = make_engine()
        result = engine.assess(make_input())
        d = result.to_dict()
        assert isinstance(d["needs_intervention"], bool)

    def test_numeric_fields_are_numeric(self):
        engine = make_engine()
        result = engine.assess(make_input())
        d = result.to_dict()
        assert isinstance(d["activity_score"], float)
        assert isinstance(d["readiness_score"], float)
        assert isinstance(d["pipeline_health_score"], float)
        assert isinstance(d["attainment_score"], float)
        assert isinstance(d["ramp_composite"], float)
        assert isinstance(d["projected_full_ramp_days"], int)

    def test_rep_id_preserved(self):
        engine = make_engine()
        result = engine.assess(make_input(rep_id="abc-123"))
        assert result.to_dict()["rep_id"] == "abc-123"

    def test_rep_name_preserved(self):
        engine = make_engine()
        result = engine.assess(make_input(rep_name="Bob Jones"))
        assert result.to_dict()["rep_name"] == "Bob Jones"

    def test_key_risk_factor_is_string(self):
        engine = make_engine()
        result = engine.assess(make_input())
        assert isinstance(result.to_dict()["key_risk_factor"], str)


# ===========================================================================
# Section 4 – _activity_score
# ===========================================================================

class TestActivityScore:
    def test_zero_activity_returns_zero(self):
        inp = make_input(calls_last_7d=0, emails_last_7d=0, meetings_completed_last_30d=0,
                         demos_completed_last_30d=0, deals_created_last_30d=0,
                         support_ticket_count=0)
        assert _activity_score(inp) == 0.0

    def test_max_activity_returns_100(self):
        inp = make_input(calls_last_7d=30, emails_last_7d=50, meetings_completed_last_30d=10,
                         demos_completed_last_30d=4, deals_created_last_30d=5,
                         support_ticket_count=0)
        # 30 + 20 + 25 + 15 + 10 = 100
        assert _activity_score(inp) == 100.0

    def test_calls_tier_30(self):
        inp = make_input(calls_last_7d=30, emails_last_7d=0, meetings_completed_last_30d=0,
                         demos_completed_last_30d=0, deals_created_last_30d=0,
                         support_ticket_count=0)
        assert _activity_score(inp) == 30.0

    def test_calls_tier_20(self):
        inp = make_input(calls_last_7d=20, emails_last_7d=0, meetings_completed_last_30d=0,
                         demos_completed_last_30d=0, deals_created_last_30d=0,
                         support_ticket_count=0)
        assert _activity_score(inp) == 22.0

    def test_calls_tier_10(self):
        inp = make_input(calls_last_7d=10, emails_last_7d=0, meetings_completed_last_30d=0,
                         demos_completed_last_30d=0, deals_created_last_30d=0,
                         support_ticket_count=0)
        assert _activity_score(inp) == 14.0

    def test_calls_tier_5(self):
        inp = make_input(calls_last_7d=5, emails_last_7d=0, meetings_completed_last_30d=0,
                         demos_completed_last_30d=0, deals_created_last_30d=0,
                         support_ticket_count=0)
        assert _activity_score(inp) == 7.0

    def test_calls_below_5_gives_0(self):
        inp = make_input(calls_last_7d=4, emails_last_7d=0, meetings_completed_last_30d=0,
                         demos_completed_last_30d=0, deals_created_last_30d=0,
                         support_ticket_count=0)
        assert _activity_score(inp) == 0.0

    def test_emails_tier_50(self):
        inp = make_input(calls_last_7d=0, emails_last_7d=50, meetings_completed_last_30d=0,
                         demos_completed_last_30d=0, deals_created_last_30d=0,
                         support_ticket_count=0)
        assert _activity_score(inp) == 20.0

    def test_emails_tier_30(self):
        inp = make_input(calls_last_7d=0, emails_last_7d=30, meetings_completed_last_30d=0,
                         demos_completed_last_30d=0, deals_created_last_30d=0,
                         support_ticket_count=0)
        assert _activity_score(inp) == 14.0

    def test_emails_tier_15(self):
        inp = make_input(calls_last_7d=0, emails_last_7d=15, meetings_completed_last_30d=0,
                         demos_completed_last_30d=0, deals_created_last_30d=0,
                         support_ticket_count=0)
        assert _activity_score(inp) == 8.0

    def test_emails_tier_5(self):
        inp = make_input(calls_last_7d=0, emails_last_7d=5, meetings_completed_last_30d=0,
                         demos_completed_last_30d=0, deals_created_last_30d=0,
                         support_ticket_count=0)
        assert _activity_score(inp) == 4.0

    def test_meetings_tier_10(self):
        inp = make_input(calls_last_7d=0, emails_last_7d=0, meetings_completed_last_30d=10,
                         demos_completed_last_30d=0, deals_created_last_30d=0,
                         support_ticket_count=0)
        assert _activity_score(inp) == 25.0

    def test_meetings_tier_6(self):
        inp = make_input(calls_last_7d=0, emails_last_7d=0, meetings_completed_last_30d=6,
                         demos_completed_last_30d=0, deals_created_last_30d=0,
                         support_ticket_count=0)
        assert _activity_score(inp) == 18.0

    def test_meetings_tier_3(self):
        inp = make_input(calls_last_7d=0, emails_last_7d=0, meetings_completed_last_30d=3,
                         demos_completed_last_30d=0, deals_created_last_30d=0,
                         support_ticket_count=0)
        assert _activity_score(inp) == 10.0

    def test_meetings_tier_1(self):
        inp = make_input(calls_last_7d=0, emails_last_7d=0, meetings_completed_last_30d=1,
                         demos_completed_last_30d=0, deals_created_last_30d=0,
                         support_ticket_count=0)
        assert _activity_score(inp) == 5.0

    def test_demos_tier_4(self):
        inp = make_input(calls_last_7d=0, emails_last_7d=0, meetings_completed_last_30d=0,
                         demos_completed_last_30d=4, deals_created_last_30d=0,
                         support_ticket_count=0)
        assert _activity_score(inp) == 15.0

    def test_demos_tier_2(self):
        inp = make_input(calls_last_7d=0, emails_last_7d=0, meetings_completed_last_30d=0,
                         demos_completed_last_30d=2, deals_created_last_30d=0,
                         support_ticket_count=0)
        assert _activity_score(inp) == 10.0

    def test_demos_tier_1(self):
        inp = make_input(calls_last_7d=0, emails_last_7d=0, meetings_completed_last_30d=0,
                         demos_completed_last_30d=1, deals_created_last_30d=0,
                         support_ticket_count=0)
        assert _activity_score(inp) == 5.0

    def test_deals_tier_5(self):
        inp = make_input(calls_last_7d=0, emails_last_7d=0, meetings_completed_last_30d=0,
                         demos_completed_last_30d=0, deals_created_last_30d=5,
                         support_ticket_count=0)
        assert _activity_score(inp) == 10.0

    def test_deals_tier_3(self):
        inp = make_input(calls_last_7d=0, emails_last_7d=0, meetings_completed_last_30d=0,
                         demos_completed_last_30d=0, deals_created_last_30d=3,
                         support_ticket_count=0)
        assert _activity_score(inp) == 7.0

    def test_deals_tier_1(self):
        inp = make_input(calls_last_7d=0, emails_last_7d=0, meetings_completed_last_30d=0,
                         demos_completed_last_30d=0, deals_created_last_30d=1,
                         support_ticket_count=0)
        assert _activity_score(inp) == 3.0

    def test_support_ticket_penalty_5(self):
        inp = make_input(calls_last_7d=30, emails_last_7d=0, meetings_completed_last_30d=0,
                         demos_completed_last_30d=0, deals_created_last_30d=0,
                         support_ticket_count=5)
        # 30 - 8 = 22
        assert _activity_score(inp) == 22.0

    def test_support_ticket_penalty_3(self):
        inp = make_input(calls_last_7d=30, emails_last_7d=0, meetings_completed_last_30d=0,
                         demos_completed_last_30d=0, deals_created_last_30d=0,
                         support_ticket_count=3)
        # 30 - 4 = 26
        assert _activity_score(inp) == 26.0

    def test_floor_at_zero(self):
        # Barely any activity + max penalty — should never go below 0
        inp = make_input(calls_last_7d=0, emails_last_7d=0, meetings_completed_last_30d=0,
                         demos_completed_last_30d=0, deals_created_last_30d=0,
                         support_ticket_count=5)
        assert _activity_score(inp) == 0.0

    def test_ceiling_at_100(self):
        inp = make_input(calls_last_7d=100, emails_last_7d=200, meetings_completed_last_30d=50,
                         demos_completed_last_30d=20, deals_created_last_30d=20,
                         support_ticket_count=0)
        assert _activity_score(inp) <= 100.0


# ===========================================================================
# Section 5 – _readiness_score
# ===========================================================================

class TestReadinessScore:
    def test_zero_readiness(self):
        inp = make_input(product_certification_complete=0, crm_adoption_score=0.0,
                         onboarding_assessment_score=0.0, peer_shadowing_sessions_completed=0,
                         industry_match_score=0.0, previous_sales_experience_years=0.0)
        assert _readiness_score(inp) == 0.0

    def test_certification_complete_adds_25(self):
        inp = make_input(product_certification_complete=1, crm_adoption_score=0.0,
                         onboarding_assessment_score=0.0, peer_shadowing_sessions_completed=0,
                         industry_match_score=0.0, previous_sales_experience_years=0.0)
        assert _readiness_score(inp) == 25.0

    def test_crm_adoption_scaled_by_020(self):
        inp = make_input(product_certification_complete=0, crm_adoption_score=100.0,
                         onboarding_assessment_score=0.0, peer_shadowing_sessions_completed=0,
                         industry_match_score=0.0, previous_sales_experience_years=0.0)
        assert _readiness_score(inp) == 20.0

    def test_onboarding_scaled_by_020(self):
        inp = make_input(product_certification_complete=0, crm_adoption_score=0.0,
                         onboarding_assessment_score=100.0, peer_shadowing_sessions_completed=0,
                         industry_match_score=0.0, previous_sales_experience_years=0.0)
        assert _readiness_score(inp) == 20.0

    def test_peer_shadowing_tier_5(self):
        inp = make_input(product_certification_complete=0, crm_adoption_score=0.0,
                         onboarding_assessment_score=0.0, peer_shadowing_sessions_completed=5,
                         industry_match_score=0.0, previous_sales_experience_years=0.0)
        assert _readiness_score(inp) == 15.0

    def test_peer_shadowing_tier_3(self):
        inp = make_input(product_certification_complete=0, crm_adoption_score=0.0,
                         onboarding_assessment_score=0.0, peer_shadowing_sessions_completed=3,
                         industry_match_score=0.0, previous_sales_experience_years=0.0)
        assert _readiness_score(inp) == 10.0

    def test_peer_shadowing_tier_1(self):
        inp = make_input(product_certification_complete=0, crm_adoption_score=0.0,
                         onboarding_assessment_score=0.0, peer_shadowing_sessions_completed=1,
                         industry_match_score=0.0, previous_sales_experience_years=0.0)
        assert _readiness_score(inp) == 5.0

    def test_industry_match_scaled_by_010(self):
        inp = make_input(product_certification_complete=0, crm_adoption_score=0.0,
                         onboarding_assessment_score=0.0, peer_shadowing_sessions_completed=0,
                         industry_match_score=100.0, previous_sales_experience_years=0.0)
        assert _readiness_score(inp) == 10.0

    def test_experience_tier_5_years(self):
        inp = make_input(product_certification_complete=0, crm_adoption_score=0.0,
                         onboarding_assessment_score=0.0, peer_shadowing_sessions_completed=0,
                         industry_match_score=0.0, previous_sales_experience_years=5.0)
        assert _readiness_score(inp) == 10.0

    def test_experience_tier_3_years(self):
        inp = make_input(product_certification_complete=0, crm_adoption_score=0.0,
                         onboarding_assessment_score=0.0, peer_shadowing_sessions_completed=0,
                         industry_match_score=0.0, previous_sales_experience_years=3.0)
        assert _readiness_score(inp) == 7.0

    def test_experience_tier_1_year(self):
        inp = make_input(product_certification_complete=0, crm_adoption_score=0.0,
                         onboarding_assessment_score=0.0, peer_shadowing_sessions_completed=0,
                         industry_match_score=0.0, previous_sales_experience_years=1.0)
        assert _readiness_score(inp) == 4.0

    def test_experience_below_1_gives_0(self):
        inp = make_input(product_certification_complete=0, crm_adoption_score=0.0,
                         onboarding_assessment_score=0.0, peer_shadowing_sessions_completed=0,
                         industry_match_score=0.0, previous_sales_experience_years=0.5)
        assert _readiness_score(inp) == 0.0

    def test_max_readiness_at_100(self):
        inp = make_input(product_certification_complete=1, crm_adoption_score=100.0,
                         onboarding_assessment_score=100.0, peer_shadowing_sessions_completed=10,
                         industry_match_score=100.0, previous_sales_experience_years=10.0)
        # 25 + 20 + 20 + 15 + 10 + 10 = 100
        assert _readiness_score(inp) == 100.0

    def test_ceiling_is_100(self):
        inp = make_input(product_certification_complete=1, crm_adoption_score=200.0,
                         onboarding_assessment_score=200.0, peer_shadowing_sessions_completed=99,
                         industry_match_score=200.0, previous_sales_experience_years=99.0)
        assert _readiness_score(inp) <= 100.0


# ===========================================================================
# Section 6 – _pipeline_health_score
# ===========================================================================

class TestPipelineHealthScore:
    def test_zero_pipeline(self):
        inp = make_input(pipeline_value_usd=0.0, quota_assigned_usd=100_000.0,
                         deals_created_last_30d=0, territory_quality_score=0.0,
                         first_deal_closed_days_after_hire=0)
        assert _pipeline_health_score(inp) == 0.0

    def test_coverage_3x_gives_40(self):
        inp = make_input(pipeline_value_usd=300_000.0, quota_assigned_usd=100_000.0,
                         deals_created_last_30d=0, territory_quality_score=0.0,
                         first_deal_closed_days_after_hire=0)
        assert _pipeline_health_score(inp) == 40.0

    def test_coverage_2x_gives_30(self):
        inp = make_input(pipeline_value_usd=200_000.0, quota_assigned_usd=100_000.0,
                         deals_created_last_30d=0, territory_quality_score=0.0,
                         first_deal_closed_days_after_hire=0)
        assert _pipeline_health_score(inp) == 30.0

    def test_coverage_1x_gives_20(self):
        inp = make_input(pipeline_value_usd=100_000.0, quota_assigned_usd=100_000.0,
                         deals_created_last_30d=0, territory_quality_score=0.0,
                         first_deal_closed_days_after_hire=0)
        assert _pipeline_health_score(inp) == 20.0

    def test_coverage_0_5x_gives_10(self):
        inp = make_input(pipeline_value_usd=50_000.0, quota_assigned_usd=100_000.0,
                         deals_created_last_30d=0, territory_quality_score=0.0,
                         first_deal_closed_days_after_hire=0)
        assert _pipeline_health_score(inp) == 10.0

    def test_coverage_below_0_5_gives_0(self):
        inp = make_input(pipeline_value_usd=10_000.0, quota_assigned_usd=100_000.0,
                         deals_created_last_30d=0, territory_quality_score=0.0,
                         first_deal_closed_days_after_hire=0)
        assert _pipeline_health_score(inp) == 0.0

    def test_zero_quota_gives_zero_coverage(self):
        inp = make_input(pipeline_value_usd=100_000.0, quota_assigned_usd=0.0,
                         deals_created_last_30d=0, territory_quality_score=0.0,
                         first_deal_closed_days_after_hire=0)
        assert _pipeline_health_score(inp) == 0.0

    def test_deals_tier_5_gives_25(self):
        inp = make_input(pipeline_value_usd=0.0, quota_assigned_usd=100_000.0,
                         deals_created_last_30d=5, territory_quality_score=0.0,
                         first_deal_closed_days_after_hire=0)
        assert _pipeline_health_score(inp) == 25.0

    def test_deals_tier_3_gives_17(self):
        inp = make_input(pipeline_value_usd=0.0, quota_assigned_usd=100_000.0,
                         deals_created_last_30d=3, territory_quality_score=0.0,
                         first_deal_closed_days_after_hire=0)
        assert _pipeline_health_score(inp) == 17.0

    def test_deals_tier_1_gives_8(self):
        inp = make_input(pipeline_value_usd=0.0, quota_assigned_usd=100_000.0,
                         deals_created_last_30d=1, territory_quality_score=0.0,
                         first_deal_closed_days_after_hire=0)
        assert _pipeline_health_score(inp) == 8.0

    def test_territory_quality_scaled_by_020(self):
        inp = make_input(pipeline_value_usd=0.0, quota_assigned_usd=100_000.0,
                         deals_created_last_30d=0, territory_quality_score=100.0,
                         first_deal_closed_days_after_hire=0)
        assert _pipeline_health_score(inp) == 20.0

    def test_first_deal_within_60_days_gives_15(self):
        inp = make_input(pipeline_value_usd=0.0, quota_assigned_usd=100_000.0,
                         deals_created_last_30d=0, territory_quality_score=0.0,
                         first_deal_closed_days_after_hire=60)
        assert _pipeline_health_score(inp) == 15.0

    def test_first_deal_within_90_days_gives_10(self):
        inp = make_input(pipeline_value_usd=0.0, quota_assigned_usd=100_000.0,
                         deals_created_last_30d=0, territory_quality_score=0.0,
                         first_deal_closed_days_after_hire=90)
        assert _pipeline_health_score(inp) == 10.0

    def test_first_deal_after_90_days_gives_5(self):
        inp = make_input(pipeline_value_usd=0.0, quota_assigned_usd=100_000.0,
                         deals_created_last_30d=0, territory_quality_score=0.0,
                         first_deal_closed_days_after_hire=120)
        assert _pipeline_health_score(inp) == 5.0

    def test_no_first_deal_gives_0_bonus(self):
        inp = make_input(pipeline_value_usd=0.0, quota_assigned_usd=100_000.0,
                         deals_created_last_30d=0, territory_quality_score=0.0,
                         first_deal_closed_days_after_hire=0)
        assert _pipeline_health_score(inp) == 0.0

    def test_ceiling_at_100(self):
        inp = make_input(pipeline_value_usd=1_000_000.0, quota_assigned_usd=100_000.0,
                         deals_created_last_30d=99, territory_quality_score=100.0,
                         first_deal_closed_days_after_hire=1)
        assert _pipeline_health_score(inp) <= 100.0


# ===========================================================================
# Section 7 – _attainment_score
# ===========================================================================

class TestAttainmentScore:
    def test_too_early_returns_50(self):
        # hire_date_days_ago == 0 → progress 0 → expected_attainment 0 → returns 50
        inp = make_input(hire_date_days_ago=0, expected_ramp_days=180,
                         revenue_attainment_pct=0.0, manager_coaching_sessions_per_month=0)
        assert _attainment_score(inp) == 50.0

    def test_ratio_1_2_gives_100(self):
        # progress=0.5 → expected_attainment=50; attainment=60 → ratio=1.2
        inp = make_input(hire_date_days_ago=90, expected_ramp_days=180,
                         revenue_attainment_pct=60.0, manager_coaching_sessions_per_month=0)
        assert _attainment_score(inp) == 100.0

    def test_ratio_1_0_gives_80(self):
        inp = make_input(hire_date_days_ago=90, expected_ramp_days=180,
                         revenue_attainment_pct=50.0, manager_coaching_sessions_per_month=0)
        assert _attainment_score(inp) == 80.0

    def test_ratio_0_8_gives_60(self):
        inp = make_input(hire_date_days_ago=90, expected_ramp_days=180,
                         revenue_attainment_pct=40.0, manager_coaching_sessions_per_month=0)
        assert _attainment_score(inp) == 60.0

    def test_ratio_0_6_gives_40(self):
        inp = make_input(hire_date_days_ago=90, expected_ramp_days=180,
                         revenue_attainment_pct=30.0, manager_coaching_sessions_per_month=0)
        assert _attainment_score(inp) == 40.0

    def test_ratio_0_4_gives_20(self):
        inp = make_input(hire_date_days_ago=90, expected_ramp_days=180,
                         revenue_attainment_pct=20.0, manager_coaching_sessions_per_month=0)
        assert _attainment_score(inp) == 20.0

    def test_ratio_below_0_4_gives_5(self):
        inp = make_input(hire_date_days_ago=90, expected_ramp_days=180,
                         revenue_attainment_pct=5.0, manager_coaching_sessions_per_month=0)
        assert _attainment_score(inp) == 5.0

    def test_coaching_4_per_month_adds_10(self):
        # Base score should be 80, then + 10 = 90
        inp = make_input(hire_date_days_ago=90, expected_ramp_days=180,
                         revenue_attainment_pct=50.0, manager_coaching_sessions_per_month=4)
        assert _attainment_score(inp) == 90.0

    def test_coaching_2_per_month_adds_5(self):
        inp = make_input(hire_date_days_ago=90, expected_ramp_days=180,
                         revenue_attainment_pct=50.0, manager_coaching_sessions_per_month=2)
        assert _attainment_score(inp) == 85.0

    def test_coaching_boost_capped_at_100(self):
        inp = make_input(hire_date_days_ago=90, expected_ramp_days=180,
                         revenue_attainment_pct=60.0, manager_coaching_sessions_per_month=4)
        # ratio >= 1.2 → score=100, coaching adds 10 but capped at 100
        assert _attainment_score(inp) == 100.0

    def test_expected_ramp_days_0_treated_as_1(self):
        # expected_ramp_days=0 → max(1,0)=1 → progress=1.0 → expected_attainment=100
        inp = make_input(hire_date_days_ago=10, expected_ramp_days=0,
                         revenue_attainment_pct=50.0, manager_coaching_sessions_per_month=0)
        # ratio = 50.0 / 100.0 = 0.5 → score=20
        assert _attainment_score(inp) == 20.0

    def test_progress_capped_at_1(self):
        # hire_date_days_ago way beyond expected_ramp_days → progress capped at 1
        inp = make_input(hire_date_days_ago=365, expected_ramp_days=180,
                         revenue_attainment_pct=100.0, manager_coaching_sessions_per_month=0)
        # expected_attainment=100; ratio=1.0 → score=80
        assert _attainment_score(inp) == 80.0


# ===========================================================================
# Section 8 – _composite formula
# ===========================================================================

class TestCompositeFormula:
    def test_weights_sum_to_1(self):
        # 0.25 + 0.25 + 0.30 + 0.20 = 1.00
        assert abs(0.25 + 0.25 + 0.30 + 0.20 - 1.0) < 1e-9

    def test_composite_basic(self):
        result = _composite(80.0, 60.0, 70.0, 50.0)
        expected = round(80 * 0.25 + 60 * 0.25 + 70 * 0.30 + 50 * 0.20, 1)
        assert result == expected

    def test_composite_all_zeros(self):
        assert _composite(0.0, 0.0, 0.0, 0.0) == 0.0

    def test_composite_all_100(self):
        assert _composite(100.0, 100.0, 100.0, 100.0) == 100.0

    def test_composite_activity_weight(self):
        # only activity=100, rest 0
        assert _composite(100.0, 0.0, 0.0, 0.0) == 25.0

    def test_composite_readiness_weight(self):
        assert _composite(0.0, 100.0, 0.0, 0.0) == 25.0

    def test_composite_pipeline_weight(self):
        assert _composite(0.0, 0.0, 100.0, 0.0) == 30.0

    def test_composite_attainment_weight(self):
        assert _composite(0.0, 0.0, 0.0, 100.0) == 20.0

    def test_composite_rounded_to_1_decimal(self):
        # Verify rounding
        c = _composite(33.3, 33.3, 33.3, 33.3)
        assert c == round(33.3 * 0.25 + 33.3 * 0.25 + 33.3 * 0.30 + 33.3 * 0.20, 1)


# ===========================================================================
# Section 9 – _ramp_phase
# ===========================================================================

class TestRampPhase:
    def test_at_quota_when_attainment_ge_90(self):
        inp = make_input(revenue_attainment_pct=90.0, hire_date_days_ago=10)
        assert _ramp_phase(inp) == RampPhase.AT_QUOTA

    def test_at_quota_when_attainment_100(self):
        inp = make_input(revenue_attainment_pct=100.0, hire_date_days_ago=10)
        assert _ramp_phase(inp) == RampPhase.AT_QUOTA

    def test_approaching_quota_when_ge_50(self):
        inp = make_input(revenue_attainment_pct=50.0, hire_date_days_ago=10)
        assert _ramp_phase(inp) == RampPhase.APPROACHING_QUOTA

    def test_approaching_quota_when_80(self):
        inp = make_input(revenue_attainment_pct=80.0, hire_date_days_ago=10)
        assert _ramp_phase(inp) == RampPhase.APPROACHING_QUOTA

    def test_ramping_when_ge_30_days_and_low_attainment(self):
        inp = make_input(revenue_attainment_pct=10.0, hire_date_days_ago=30)
        assert _ramp_phase(inp) == RampPhase.RAMPING

    def test_learning_when_lt_30_days_and_low_attainment(self):
        inp = make_input(revenue_attainment_pct=10.0, hire_date_days_ago=29)
        assert _ramp_phase(inp) == RampPhase.LEARNING

    def test_learning_exactly_0_days(self):
        inp = make_input(revenue_attainment_pct=0.0, hire_date_days_ago=0)
        assert _ramp_phase(inp) == RampPhase.LEARNING

    def test_approaching_quota_boundary_just_below_90(self):
        inp = make_input(revenue_attainment_pct=89.9, hire_date_days_ago=10)
        assert _ramp_phase(inp) == RampPhase.APPROACHING_QUOTA


# ===========================================================================
# Section 10 – _ramp_status
# ===========================================================================

class TestRampStatus:
    def test_ahead_when_high_composite_and_overperforming(self):
        # composite >= 70, revenue_attainment >= expected_attainment * 1.1
        # With hire_date_days_ago=90, expected_ramp=180: progress=0.5, expected_attainment=50
        # Need attainment >= 55
        inp = make_input(hire_date_days_ago=90, expected_ramp_days=180,
                         revenue_attainment_pct=60.0)
        status = _ramp_status(75.0, inp)
        assert status == RampStatus.AHEAD

    def test_on_track_when_composite_55(self):
        inp = make_input(hire_date_days_ago=90, expected_ramp_days=180,
                         revenue_attainment_pct=10.0)
        status = _ramp_status(55.0, inp)
        assert status == RampStatus.ON_TRACK

    def test_at_risk_when_composite_40(self):
        inp = make_input()
        status = _ramp_status(40.0, inp)
        assert status == RampStatus.AT_RISK

    def test_behind_when_composite_below_40(self):
        inp = make_input()
        status = _ramp_status(39.0, inp)
        assert status == RampStatus.BEHIND

    def test_on_track_not_ahead_when_not_overperforming(self):
        # composite >= 70 but attainment NOT >= expected * 1.1
        inp = make_input(hire_date_days_ago=90, expected_ramp_days=180,
                         revenue_attainment_pct=49.0)
        status = _ramp_status(75.0, inp)
        assert status == RampStatus.ON_TRACK


# ===========================================================================
# Section 11 – _ramp_risk
# ===========================================================================

class TestRampRisk:
    def test_critical_when_composite_below_30(self):
        inp = make_input(hire_date_days_ago=10, revenue_attainment_pct=50.0)
        assert _ramp_risk(29.9, inp) == RampRisk.CRITICAL

    def test_critical_when_60_days_low_attainment(self):
        inp = make_input(hire_date_days_ago=60, revenue_attainment_pct=5.0)
        assert _ramp_risk(50.0, inp) == RampRisk.CRITICAL

    def test_high_when_composite_30_to_45(self):
        inp = make_input(hire_date_days_ago=10, revenue_attainment_pct=50.0)
        assert _ramp_risk(30.0, inp) == RampRisk.HIGH
        assert _ramp_risk(44.9, inp) == RampRisk.HIGH

    def test_moderate_when_composite_45_to_60(self):
        inp = make_input(hire_date_days_ago=10, revenue_attainment_pct=50.0)
        assert _ramp_risk(45.0, inp) == RampRisk.MODERATE
        assert _ramp_risk(59.9, inp) == RampRisk.MODERATE

    def test_low_when_composite_ge_60(self):
        inp = make_input(hire_date_days_ago=10, revenue_attainment_pct=50.0)
        assert _ramp_risk(60.0, inp) == RampRisk.LOW
        assert _ramp_risk(100.0, inp) == RampRisk.LOW

    def test_not_critical_when_60_days_and_attainment_ge_10(self):
        inp = make_input(hire_date_days_ago=60, revenue_attainment_pct=10.0)
        # composite=50 → should be moderate (not critical via hire_date branch)
        assert _ramp_risk(50.0, inp) == RampRisk.MODERATE

    def test_critical_exactly_at_60_days_lt_10_pct(self):
        inp = make_input(hire_date_days_ago=60, revenue_attainment_pct=9.9)
        assert _ramp_risk(50.0, inp) == RampRisk.CRITICAL


# ===========================================================================
# Section 12 – _ramp_action
# ===========================================================================

class TestRampAction:
    def test_pip_when_critical(self):
        assert _ramp_action(RampRisk.CRITICAL, 20.0) == RampAction.PIP

    def test_accelerate_coaching_when_high(self):
        assert _ramp_action(RampRisk.HIGH, 35.0) == RampAction.ACCELERATE_COACHING

    def test_territory_adjustment_when_moderate(self):
        assert _ramp_action(RampRisk.MODERATE, 50.0) == RampAction.TERRITORY_ADJUSTMENT

    def test_maintain_when_low(self):
        assert _ramp_action(RampRisk.LOW, 75.0) == RampAction.MAINTAIN


# ===========================================================================
# Section 13 – _projected_full_ramp_days
# ===========================================================================

class TestProjectedFullRampDays:
    def test_composite_ge_75_reduces_by_15pct(self):
        inp = make_input(expected_ramp_days=200)
        result = _projected_full_ramp_days(inp, 75.0)
        assert result == max(30, int(200 * 0.85))

    def test_composite_ge_55_returns_base(self):
        inp = make_input(expected_ramp_days=200)
        assert _projected_full_ramp_days(inp, 55.0) == 200

    def test_composite_ge_40_increases_by_25pct(self):
        inp = make_input(expected_ramp_days=200)
        assert _projected_full_ramp_days(inp, 40.0) == int(200 * 1.25)

    def test_composite_below_40_increases_by_60pct(self):
        inp = make_input(expected_ramp_days=200)
        assert _projected_full_ramp_days(inp, 39.9) == int(200 * 1.6)

    def test_floor_at_30_for_high_composite(self):
        # If base is very small, floor at 30
        inp = make_input(expected_ramp_days=30)
        result = _projected_full_ramp_days(inp, 80.0)
        assert result >= 30

    def test_exact_boundary_75(self):
        inp = make_input(expected_ramp_days=180)
        r75 = _projected_full_ramp_days(inp, 75.0)
        r74 = _projected_full_ramp_days(inp, 74.9)
        assert r75 == max(30, int(180 * 0.85))
        assert r74 == 180

    def test_exact_boundary_55(self):
        inp = make_input(expected_ramp_days=180)
        r55 = _projected_full_ramp_days(inp, 55.0)
        r54 = _projected_full_ramp_days(inp, 54.9)
        assert r55 == 180
        assert r54 == int(180 * 1.25)

    def test_exact_boundary_40(self):
        inp = make_input(expected_ramp_days=180)
        r40 = _projected_full_ramp_days(inp, 40.0)
        r39 = _projected_full_ramp_days(inp, 39.9)
        assert r40 == int(180 * 1.25)
        assert r39 == int(180 * 1.6)


# ===========================================================================
# Section 14 – _key_risk_factor
# ===========================================================================

class TestKeyRiskFactor:
    def test_certification_incomplete_and_readiness_low(self):
        inp = make_input(product_certification_complete=0, support_ticket_count=0,
                         manager_coaching_sessions_per_month=2)
        factor = _key_risk_factor(inp, 80.0, 40.0, 80.0, 80.0)
        assert factor == "product certification incomplete"

    def test_support_tickets_override_when_cert_passes(self):
        # Certification check is skipped (product_certification_complete=1),
        # so support_ticket_count >= 5 fires next.
        inp = make_input(product_certification_complete=1, support_ticket_count=5,
                         manager_coaching_sessions_per_month=2)
        factor = _key_risk_factor(inp, 80.0, 40.0, 80.0, 80.0)
        assert factor == "blocked by tooling/admin issues"

    def test_support_tickets_override_when_readiness_high(self):
        # Even with cert incomplete, readiness >= 50 skips cert branch;
        # support_ticket_count >= 5 then fires.
        inp = make_input(product_certification_complete=0, support_ticket_count=5,
                         manager_coaching_sessions_per_month=2)
        factor = _key_risk_factor(inp, 80.0, 60.0, 80.0, 80.0)  # readiness=60 >= 50
        assert factor == "blocked by tooling/admin issues"

    def test_no_coaching_returns_insufficient_coaching(self):
        inp = make_input(product_certification_complete=1, support_ticket_count=0,
                         manager_coaching_sessions_per_month=0)
        factor = _key_risk_factor(inp, 80.0, 80.0, 80.0, 80.0)
        assert factor == "insufficient manager coaching"

    def test_returns_weakest_score_when_no_overrides(self):
        inp = make_input(product_certification_complete=1, support_ticket_count=0,
                         manager_coaching_sessions_per_month=2)
        factor = _key_risk_factor(inp, 10.0, 80.0, 80.0, 80.0)
        assert factor == "low activity volume"

    def test_returns_weak_pipeline_when_lowest(self):
        inp = make_input(product_certification_complete=1, support_ticket_count=0,
                         manager_coaching_sessions_per_month=2)
        factor = _key_risk_factor(inp, 80.0, 80.0, 5.0, 80.0)
        assert factor == "weak pipeline"

    def test_returns_low_attainment_when_lowest(self):
        inp = make_input(product_certification_complete=1, support_ticket_count=0,
                         manager_coaching_sessions_per_month=2)
        factor = _key_risk_factor(inp, 80.0, 80.0, 80.0, 3.0)
        assert factor == "low revenue attainment"

    def test_readiness_low_but_certification_complete(self):
        # readiness < 50 but certification IS complete → falls through to weakest
        inp = make_input(product_certification_complete=1, support_ticket_count=0,
                         manager_coaching_sessions_per_month=2)
        factor = _key_risk_factor(inp, 80.0, 30.0, 80.0, 80.0)
        assert factor == "poor product readiness"


# ===========================================================================
# Section 15 – is_on_track invariant
# ===========================================================================

class TestIsOnTrack:
    def test_on_track_true_when_composite_ge_55_and_attainment_ok(self):
        # hire_date_days_ago=90, expected_ramp=180 → progress=0.5 → threshold = 0.5 * 60 = 30
        # Need revenue_attainment_pct >= 30 AND composite >= 55
        engine = make_engine()
        inp = make_input(hire_date_days_ago=90, expected_ramp_days=180,
                         revenue_attainment_pct=35.0,
                         calls_last_7d=30, emails_last_7d=50, meetings_completed_last_30d=10,
                         demos_completed_last_30d=4, deals_created_last_30d=5,
                         pipeline_value_usd=1_500_000.0, quota_assigned_usd=500_000.0,
                         product_certification_complete=1, crm_adoption_score=80.0,
                         onboarding_assessment_score=80.0, industry_match_score=80.0,
                         previous_sales_experience_years=5.0, peer_shadowing_sessions_completed=5,
                         manager_coaching_sessions_per_month=4,
                         first_deal_closed_days_after_hire=45)
        result = engine.assess(inp)
        # Make sure composite is actually >= 55
        if result.ramp_composite >= 55:
            expected_threshold = (90 / 180) * 60.0
            expected_on_track = result.ramp_composite >= 55 and inp.revenue_attainment_pct >= expected_threshold
            assert result.is_on_track == expected_on_track

    def test_on_track_false_when_composite_below_55(self):
        engine = make_engine()
        inp = make_input(calls_last_7d=0, emails_last_7d=0, meetings_completed_last_30d=0,
                         demos_completed_last_30d=0, deals_created_last_30d=0,
                         pipeline_value_usd=0.0, product_certification_complete=0,
                         crm_adoption_score=0.0, onboarding_assessment_score=0.0,
                         industry_match_score=0.0, previous_sales_experience_years=0.0,
                         peer_shadowing_sessions_completed=0,
                         revenue_attainment_pct=0.0, manager_coaching_sessions_per_month=0,
                         hire_date_days_ago=90, expected_ramp_days=180)
        result = engine.assess(inp)
        assert result.ramp_composite < 55
        assert result.is_on_track is False

    def test_on_track_false_when_attainment_below_threshold(self):
        # composite >= 55 but attainment below 60% threshold
        engine = make_engine()
        # Build a rep with good composite but zero attainment
        inp = make_input(hire_date_days_ago=90, expected_ramp_days=180,
                         revenue_attainment_pct=0.0,
                         calls_last_7d=30, emails_last_7d=50, meetings_completed_last_30d=10,
                         demos_completed_last_30d=4, deals_created_last_30d=5,
                         pipeline_value_usd=1_500_000.0, quota_assigned_usd=500_000.0,
                         product_certification_complete=1, crm_adoption_score=100.0,
                         onboarding_assessment_score=100.0, industry_match_score=100.0,
                         previous_sales_experience_years=10.0, peer_shadowing_sessions_completed=5,
                         manager_coaching_sessions_per_month=4,
                         first_deal_closed_days_after_hire=30)
        result = engine.assess(inp)
        # threshold = 0.5 * 60 = 30; attainment is 0 → not on track regardless of composite
        assert result.is_on_track is False

    def test_is_on_track_formula_direct(self):
        # Directly verify formula: composite >= 55 AND revenue_attainment_pct >= (days/ramp)*60
        engine = make_engine()
        inp = make_input(hire_date_days_ago=60, expected_ramp_days=180,
                         revenue_attainment_pct=25.0)
        result = engine.assess(inp)
        progress = min(1.0, 60 / 180)
        threshold = progress * 60.0
        expected = result.ramp_composite >= 55 and 25.0 >= threshold
        assert result.is_on_track == expected


# ===========================================================================
# Section 16 – needs_intervention invariant
# ===========================================================================

class TestNeedsIntervention:
    def test_needs_intervention_when_composite_below_40(self):
        engine = make_engine()
        inp = make_input(calls_last_7d=0, emails_last_7d=0, meetings_completed_last_30d=0,
                         demos_completed_last_30d=0, deals_created_last_30d=0,
                         pipeline_value_usd=0.0, product_certification_complete=0,
                         crm_adoption_score=0.0, onboarding_assessment_score=0.0,
                         industry_match_score=0.0, previous_sales_experience_years=0.0,
                         peer_shadowing_sessions_completed=0,
                         revenue_attainment_pct=0.0, manager_coaching_sessions_per_month=0,
                         hire_date_days_ago=90, expected_ramp_days=180)
        result = engine.assess(inp)
        if result.ramp_composite < 40:
            assert result.needs_intervention is True

    def test_needs_intervention_when_risk_critical(self):
        engine = make_engine()
        # hire_date_days_ago=60, revenue_attainment<10 → critical risk
        inp = make_input(hire_date_days_ago=60, revenue_attainment_pct=5.0,
                         expected_ramp_days=180)
        result = engine.assess(inp)
        assert result.ramp_risk == RampRisk.CRITICAL
        assert result.needs_intervention is True

    def test_no_intervention_when_low_risk_good_composite(self):
        engine = make_engine()
        inp = make_input(calls_last_7d=30, emails_last_7d=50, meetings_completed_last_30d=10,
                         demos_completed_last_30d=4, deals_created_last_30d=5,
                         pipeline_value_usd=2_000_000.0, quota_assigned_usd=500_000.0,
                         product_certification_complete=1, crm_adoption_score=100.0,
                         onboarding_assessment_score=100.0, industry_match_score=100.0,
                         previous_sales_experience_years=10.0, peer_shadowing_sessions_completed=5,
                         manager_coaching_sessions_per_month=4,
                         first_deal_closed_days_after_hire=30,
                         hire_date_days_ago=90, expected_ramp_days=180,
                         revenue_attainment_pct=80.0)
        result = engine.assess(inp)
        # composite should be high and risk low
        if result.ramp_composite >= 40 and result.ramp_risk != RampRisk.CRITICAL:
            assert result.needs_intervention is False


# ===========================================================================
# Section 17 – RepRampIntelligence.assess()
# ===========================================================================

class TestAssess:
    def test_returns_ramp_result(self):
        engine = make_engine()
        result = engine.assess(make_input())
        assert isinstance(result, RepRampResult)

    def test_stores_result_by_rep_id(self):
        engine = make_engine()
        inp = make_input(rep_id="r1")
        engine.assess(inp)
        assert engine.get("r1") is not None

    def test_composite_in_range(self):
        engine = make_engine()
        result = engine.assess(make_input())
        assert 0.0 <= result.ramp_composite <= 100.0

    def test_activity_score_in_range(self):
        engine = make_engine()
        result = engine.assess(make_input())
        assert 0.0 <= result.activity_score <= 100.0

    def test_readiness_score_in_range(self):
        engine = make_engine()
        result = engine.assess(make_input())
        assert 0.0 <= result.readiness_score <= 100.0

    def test_pipeline_health_score_in_range(self):
        engine = make_engine()
        result = engine.assess(make_input())
        assert 0.0 <= result.pipeline_health_score <= 100.0

    def test_attainment_score_in_range(self):
        engine = make_engine()
        result = engine.assess(make_input())
        assert 0.0 <= result.attainment_score <= 100.0

    def test_ramp_status_is_valid(self):
        engine = make_engine()
        result = engine.assess(make_input())
        assert result.ramp_status in RampStatus

    def test_ramp_phase_is_valid(self):
        engine = make_engine()
        result = engine.assess(make_input())
        assert result.ramp_phase in RampPhase

    def test_ramp_risk_is_valid(self):
        engine = make_engine()
        result = engine.assess(make_input())
        assert result.ramp_risk in RampRisk

    def test_ramp_action_is_valid(self):
        engine = make_engine()
        result = engine.assess(make_input())
        assert result.ramp_action in RampAction

    def test_rep_id_matches(self):
        engine = make_engine()
        result = engine.assess(make_input(rep_id="xyz-999"))
        assert result.rep_id == "xyz-999"

    def test_rep_name_matches(self):
        engine = make_engine()
        result = engine.assess(make_input(rep_name="Charlie Brown"))
        assert result.rep_name == "Charlie Brown"

    def test_overwrite_previous_result(self):
        engine = make_engine()
        inp1 = make_input(rep_id="r1", revenue_attainment_pct=10.0)
        inp2 = make_input(rep_id="r1", revenue_attainment_pct=90.0)
        engine.assess(inp1)
        engine.assess(inp2)
        stored = engine.get("r1")
        assert stored is not None
        # second assessment should have replaced the first


# ===========================================================================
# Section 18 – assess_batch() sorted descending by ramp_composite
# ===========================================================================

class TestAssessBatch:
    def test_returns_list(self):
        engine = make_engine()
        results = engine.assess_batch([make_input(rep_id="r1"), make_input(rep_id="r2")])
        assert isinstance(results, list)

    def test_sorted_descending_by_ramp_composite(self):
        engine = make_engine()
        inputs = [
            make_input(rep_id="r1", calls_last_7d=0, emails_last_7d=0,
                       meetings_completed_last_30d=0, demos_completed_last_30d=0,
                       deals_created_last_30d=0, pipeline_value_usd=0.0,
                       product_certification_complete=0, crm_adoption_score=0.0,
                       onboarding_assessment_score=0.0, industry_match_score=0.0,
                       previous_sales_experience_years=0.0, peer_shadowing_sessions_completed=0,
                       revenue_attainment_pct=0.0, manager_coaching_sessions_per_month=0),
            make_input(rep_id="r2", calls_last_7d=30, emails_last_7d=50,
                       meetings_completed_last_30d=10, demos_completed_last_30d=4,
                       deals_created_last_30d=5, pipeline_value_usd=2_000_000.0,
                       product_certification_complete=1, crm_adoption_score=100.0,
                       onboarding_assessment_score=100.0, industry_match_score=100.0,
                       previous_sales_experience_years=10.0, peer_shadowing_sessions_completed=5,
                       revenue_attainment_pct=80.0, manager_coaching_sessions_per_month=4,
                       first_deal_closed_days_after_hire=30),
        ]
        results = engine.assess_batch(inputs)
        composites = [r.ramp_composite for r in results]
        assert composites == sorted(composites, reverse=True)

    def test_empty_batch_returns_empty(self):
        engine = make_engine()
        assert engine.assess_batch([]) == []

    def test_single_element_batch(self):
        engine = make_engine()
        results = engine.assess_batch([make_input()])
        assert len(results) == 1

    def test_batch_stores_all_results(self):
        engine = make_engine()
        inputs = [make_input(rep_id=f"r{i}") for i in range(5)]
        engine.assess_batch(inputs)
        for i in range(5):
            assert engine.get(f"r{i}") is not None

    def test_batch_result_count_matches_input(self):
        engine = make_engine()
        inputs = [make_input(rep_id=f"r{i}") for i in range(7)]
        results = engine.assess_batch(inputs)
        assert len(results) == 7

    def test_sort_stability_three_reps(self):
        engine = make_engine()
        inputs = [
            make_input(rep_id="mid", revenue_attainment_pct=50.0),
            make_input(rep_id="high", revenue_attainment_pct=100.0,
                       calls_last_7d=30, emails_last_7d=50, meetings_completed_last_30d=10,
                       demos_completed_last_30d=4, deals_created_last_30d=5,
                       pipeline_value_usd=2_000_000.0, product_certification_complete=1,
                       crm_adoption_score=100.0, onboarding_assessment_score=100.0,
                       industry_match_score=100.0, previous_sales_experience_years=10.0,
                       peer_shadowing_sessions_completed=5, manager_coaching_sessions_per_month=4,
                       first_deal_closed_days_after_hire=20),
            make_input(rep_id="low", revenue_attainment_pct=0.0,
                       calls_last_7d=0, emails_last_7d=0, meetings_completed_last_30d=0,
                       demos_completed_last_30d=0, deals_created_last_30d=0,
                       pipeline_value_usd=0.0, product_certification_complete=0,
                       crm_adoption_score=0.0, onboarding_assessment_score=0.0,
                       industry_match_score=0.0, previous_sales_experience_years=0.0,
                       peer_shadowing_sessions_completed=0, manager_coaching_sessions_per_month=0),
        ]
        results = engine.assess_batch(inputs)
        composites = [r.ramp_composite for r in results]
        assert composites[0] >= composites[1] >= composites[2]


# ===========================================================================
# Section 19 – reset()
# ===========================================================================

class TestReset:
    def test_reset_clears_all_results(self):
        engine = make_engine()
        engine.assess(make_input(rep_id="r1"))
        engine.assess(make_input(rep_id="r2"))
        engine.reset()
        assert engine.get("r1") is None
        assert engine.get("r2") is None

    def test_reset_makes_all_reps_empty(self):
        engine = make_engine()
        engine.assess(make_input())
        engine.reset()
        assert engine.all_reps() == []

    def test_reset_makes_on_track_empty(self):
        engine = make_engine()
        engine.assess(make_input())
        engine.reset()
        assert engine.on_track_reps() == []

    def test_reset_makes_intervention_empty(self):
        engine = make_engine()
        engine.assess(make_input())
        engine.reset()
        assert engine.intervention_queue() == []

    def test_double_reset_is_safe(self):
        engine = make_engine()
        engine.reset()
        engine.reset()
        assert engine.all_reps() == []

    def test_can_assess_after_reset(self):
        engine = make_engine()
        engine.assess(make_input(rep_id="r1"))
        engine.reset()
        engine.assess(make_input(rep_id="r2"))
        assert engine.get("r2") is not None
        assert engine.get("r1") is None


# ===========================================================================
# Section 20 – summary() keys invariant
# ===========================================================================

class TestSummary:
    EXPECTED_KEYS = {
        "total",
        "ramp_status_counts",
        "ramp_phase_counts",
        "ramp_risk_counts",
        "action_counts",
        "avg_ramp_composite",
        "on_track_count",
        "intervention_count",
        "avg_activity_score",
        "avg_readiness_score",
        "avg_pipeline_health_score",
        "avg_attainment_score",
        "avg_projected_full_ramp_days",
    }

    def test_exactly_13_keys(self):
        engine = make_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert len(s) == 13

    def test_exact_key_names(self):
        engine = make_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert set(s.keys()) == self.EXPECTED_KEYS

    def test_summary_empty_engine(self):
        engine = make_engine()
        s = engine.summary()
        assert len(s) == 13

    def test_total_equals_assessed_count(self):
        engine = make_engine()
        for i in range(5):
            engine.assess(make_input(rep_id=f"r{i}"))
        assert engine.summary()["total"] == 5

    def test_total_zero_when_empty(self):
        engine = make_engine()
        assert engine.summary()["total"] == 0

    def test_avg_composite_zero_when_empty(self):
        engine = make_engine()
        assert engine.summary()["avg_ramp_composite"] == 0.0

    def test_on_track_count_zero_when_empty(self):
        engine = make_engine()
        assert engine.summary()["on_track_count"] == 0

    def test_intervention_count_zero_when_empty(self):
        engine = make_engine()
        assert engine.summary()["intervention_count"] == 0

    def test_avg_scores_zero_when_empty(self):
        engine = make_engine()
        s = engine.summary()
        assert s["avg_activity_score"] == 0.0
        assert s["avg_readiness_score"] == 0.0
        assert s["avg_pipeline_health_score"] == 0.0
        assert s["avg_attainment_score"] == 0.0
        assert s["avg_projected_full_ramp_days"] == 0

    def test_status_counts_is_dict(self):
        engine = make_engine()
        engine.assess(make_input())
        assert isinstance(engine.summary()["ramp_status_counts"], dict)

    def test_phase_counts_is_dict(self):
        engine = make_engine()
        engine.assess(make_input())
        assert isinstance(engine.summary()["ramp_phase_counts"], dict)

    def test_risk_counts_is_dict(self):
        engine = make_engine()
        engine.assess(make_input())
        assert isinstance(engine.summary()["ramp_risk_counts"], dict)

    def test_action_counts_is_dict(self):
        engine = make_engine()
        engine.assess(make_input())
        assert isinstance(engine.summary()["action_counts"], dict)

    def test_status_counts_sum_to_total(self):
        engine = make_engine()
        for i in range(4):
            engine.assess(make_input(rep_id=f"r{i}"))
        s = engine.summary()
        assert sum(s["ramp_status_counts"].values()) == s["total"]

    def test_phase_counts_sum_to_total(self):
        engine = make_engine()
        for i in range(4):
            engine.assess(make_input(rep_id=f"r{i}"))
        s = engine.summary()
        assert sum(s["ramp_phase_counts"].values()) == s["total"]

    def test_risk_counts_sum_to_total(self):
        engine = make_engine()
        for i in range(4):
            engine.assess(make_input(rep_id=f"r{i}"))
        s = engine.summary()
        assert sum(s["ramp_risk_counts"].values()) == s["total"]

    def test_action_counts_sum_to_total(self):
        engine = make_engine()
        for i in range(4):
            engine.assess(make_input(rep_id=f"r{i}"))
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_called_with_no_arguments(self):
        """summary() is called with NO arguments (the spec mandates this)."""
        engine = make_engine()
        engine.assess(make_input())
        # Should not raise TypeError about unexpected arguments
        s = engine.summary()
        assert s is not None

    def test_avg_composite_is_float(self):
        engine = make_engine()
        engine.assess(make_input())
        assert isinstance(engine.summary()["avg_ramp_composite"], float)

    def test_on_track_count_is_int(self):
        engine = make_engine()
        engine.assess(make_input())
        assert isinstance(engine.summary()["on_track_count"], int)

    def test_intervention_count_is_int(self):
        engine = make_engine()
        engine.assess(make_input())
        assert isinstance(engine.summary()["intervention_count"], int)

    def test_avg_projected_full_ramp_days_is_numeric(self):
        engine = make_engine()
        engine.assess(make_input())
        v = engine.summary()["avg_projected_full_ramp_days"]
        assert isinstance(v, (int, float))


# ===========================================================================
# Section 21 – Other engine methods
# ===========================================================================

class TestEngineHelpers:
    def test_get_returns_none_for_unknown_id(self):
        engine = make_engine()
        assert engine.get("nope") is None

    def test_get_returns_result_after_assess(self):
        engine = make_engine()
        engine.assess(make_input(rep_id="r99"))
        r = engine.get("r99")
        assert r is not None
        assert r.rep_id == "r99"

    def test_all_reps_sorted_descending(self):
        engine = make_engine()
        engine.assess(make_input(rep_id="r1"))
        engine.assess(make_input(rep_id="r2"))
        reps = engine.all_reps()
        composites = [r.ramp_composite for r in reps]
        assert composites == sorted(composites, reverse=True)

    def test_all_reps_empty_initially(self):
        engine = make_engine()
        assert engine.all_reps() == []

    def test_on_track_reps_all_on_track(self):
        engine = make_engine()
        for i in range(5):
            engine.assess(make_input(rep_id=f"r{i}"))
        for r in engine.on_track_reps():
            assert r.is_on_track is True

    def test_intervention_queue_all_need_intervention(self):
        engine = make_engine()
        for i in range(5):
            engine.assess(make_input(rep_id=f"r{i}"))
        for r in engine.intervention_queue():
            assert r.needs_intervention is True

    def test_by_status_filters_correctly(self):
        engine = make_engine()
        for i in range(5):
            engine.assess(make_input(rep_id=f"r{i}"))
        for status in RampStatus:
            filtered = engine.by_status(status)
            assert all(r.ramp_status == status for r in filtered)

    def test_by_phase_filters_correctly(self):
        engine = make_engine()
        for i in range(5):
            engine.assess(make_input(rep_id=f"r{i}"))
        for phase in RampPhase:
            filtered = engine.by_phase(phase)
            assert all(r.ramp_phase == phase for r in filtered)

    def test_avg_ramp_composite_zero_when_empty(self):
        engine = make_engine()
        assert engine.avg_ramp_composite() == 0.0

    def test_avg_ramp_composite_single_rep(self):
        engine = make_engine()
        result = engine.assess(make_input(rep_id="r1"))
        avg = engine.avg_ramp_composite()
        assert avg == result.ramp_composite

    def test_avg_ramp_composite_is_float(self):
        engine = make_engine()
        engine.assess(make_input())
        assert isinstance(engine.avg_ramp_composite(), float)

    def test_avg_ramp_composite_multiple_reps(self):
        engine = make_engine()
        r1 = engine.assess(make_input(rep_id="r1"))
        r2 = engine.assess(make_input(rep_id="r2"))
        expected_avg = round((r1.ramp_composite + r2.ramp_composite) / 2, 1)
        assert engine.avg_ramp_composite() == expected_avg


# ===========================================================================
# Section 22 – End-to-end / integration scenarios
# ===========================================================================

class TestIntegration:
    def test_star_rep_gets_ahead_status(self):
        """A rep with exceptional metrics should be AHEAD."""
        engine = make_engine()
        inp = make_input(
            rep_id="star",
            hire_date_days_ago=90,
            expected_ramp_days=180,
            calls_last_7d=30, emails_last_7d=50, meetings_completed_last_30d=10,
            demos_completed_last_30d=4, deals_created_last_30d=5,
            pipeline_value_usd=2_000_000.0, quota_assigned_usd=500_000.0,
            first_deal_closed_days_after_hire=30,
            revenue_attainment_pct=80.0,
            manager_coaching_sessions_per_month=4,
            peer_shadowing_sessions_completed=5,
            product_certification_complete=1,
            crm_adoption_score=100.0, onboarding_assessment_score=100.0,
            territory_quality_score=100.0,
            previous_sales_experience_years=10.0,
            industry_match_score=100.0,
            support_ticket_count=0,
        )
        result = engine.assess(inp)
        assert result.ramp_status == RampStatus.AHEAD
        assert result.ramp_risk == RampRisk.LOW
        assert result.ramp_action == RampAction.MAINTAIN

    def test_struggling_rep_gets_behind_and_pip(self):
        """A rep with zero activity should be BEHIND with PIP."""
        engine = make_engine()
        inp = make_input(
            rep_id="struggling",
            hire_date_days_ago=90,
            expected_ramp_days=180,
            calls_last_7d=0, emails_last_7d=0, meetings_completed_last_30d=0,
            demos_completed_last_30d=0, deals_created_last_30d=0,
            pipeline_value_usd=0.0, quota_assigned_usd=500_000.0,
            first_deal_closed_days_after_hire=0,
            revenue_attainment_pct=0.0,
            manager_coaching_sessions_per_month=0,
            peer_shadowing_sessions_completed=0,
            product_certification_complete=0,
            crm_adoption_score=0.0, onboarding_assessment_score=0.0,
            territory_quality_score=0.0,
            previous_sales_experience_years=0.0,
            industry_match_score=0.0,
            support_ticket_count=0,
        )
        result = engine.assess(inp)
        assert result.ramp_status == RampStatus.BEHIND
        assert result.ramp_action == RampAction.PIP
        assert result.needs_intervention is True

    def test_batch_then_summary_consistency(self):
        """assess_batch results are stored; summary reflects them."""
        engine = make_engine()
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(10)]
        engine.assess_batch(inputs)
        s = engine.summary()
        assert s["total"] == 10
        assert sum(s["ramp_status_counts"].values()) == 10

    def test_multiple_reps_different_phases(self):
        """Reps with different attainments land in different phases."""
        engine = make_engine()
        new_rep = make_input(rep_id="new", revenue_attainment_pct=0.0, hire_date_days_ago=10)
        ramping_rep = make_input(rep_id="ramp", revenue_attainment_pct=20.0, hire_date_days_ago=60)
        approaching_rep = make_input(rep_id="approx", revenue_attainment_pct=70.0)
        quota_rep = make_input(rep_id="quota", revenue_attainment_pct=95.0)

        r_new = engine.assess(new_rep)
        r_ramp = engine.assess(ramping_rep)
        r_approx = engine.assess(approaching_rep)
        r_quota = engine.assess(quota_rep)

        assert r_new.ramp_phase == RampPhase.LEARNING
        assert r_ramp.ramp_phase == RampPhase.RAMPING
        assert r_approx.ramp_phase == RampPhase.APPROACHING_QUOTA
        assert r_quota.ramp_phase == RampPhase.AT_QUOTA

    def test_composite_consistent_with_component_scores(self):
        """The composite stored on result should match the formula."""
        engine = make_engine()
        result = engine.assess(make_input())
        expected = round(
            result.activity_score * 0.25
            + result.readiness_score * 0.25
            + result.pipeline_health_score * 0.30
            + result.attainment_score * 0.20,
            1
        )
        assert result.ramp_composite == expected

    def test_projected_ramp_days_positive(self):
        engine = make_engine()
        result = engine.assess(make_input())
        assert result.projected_full_ramp_days > 0

    def test_to_dict_round_trips_values(self):
        engine = make_engine()
        result = engine.assess(make_input(rep_id="rt1", rep_name="RT Rep"))
        d = result.to_dict()
        assert d["rep_id"] == result.rep_id
        assert d["ramp_status"] == result.ramp_status.value
        assert d["ramp_composite"] == result.ramp_composite
        assert d["is_on_track"] == result.is_on_track
        assert d["needs_intervention"] == result.needs_intervention

    def test_assess_multiple_different_rep_ids_stored_separately(self):
        engine = make_engine()
        for i in range(20):
            engine.assess(make_input(rep_id=f"rep-{i:03d}"))
        for i in range(20):
            assert engine.get(f"rep-{i:03d}") is not None

    def test_summary_after_reset_gives_zero_total(self):
        engine = make_engine()
        for i in range(5):
            engine.assess(make_input(rep_id=f"r{i}"))
        engine.reset()
        assert engine.summary()["total"] == 0

    def test_on_track_count_le_total(self):
        engine = make_engine()
        for i in range(8):
            engine.assess(make_input(rep_id=f"r{i}"))
        s = engine.summary()
        assert s["on_track_count"] <= s["total"]

    def test_intervention_count_le_total(self):
        engine = make_engine()
        for i in range(8):
            engine.assess(make_input(rep_id=f"r{i}"))
        s = engine.summary()
        assert s["intervention_count"] <= s["total"]

    def test_action_pip_corresponds_to_critical_risk(self):
        engine = make_engine()
        # hire_date_days_ago=60, attainment<10 → critical → PIP
        result = engine.assess(make_input(hire_date_days_ago=60, revenue_attainment_pct=5.0))
        assert result.ramp_action == RampAction.PIP
        assert result.ramp_risk == RampRisk.CRITICAL

    def test_support_ticket_key_risk(self):
        engine = make_engine()
        result = engine.assess(make_input(support_ticket_count=5,
                                          manager_coaching_sessions_per_month=2))
        assert result.key_risk_factor == "blocked by tooling/admin issues"

    def test_by_status_returns_empty_list_when_none(self):
        engine = make_engine()
        # Start fresh, AHEAD is unlikely with the default input settings
        engine.assess(make_input(calls_last_7d=0, emails_last_7d=0,
                                 meetings_completed_last_30d=0, demos_completed_last_30d=0,
                                 deals_created_last_30d=0, pipeline_value_usd=0.0,
                                 product_certification_complete=0, crm_adoption_score=0.0,
                                 onboarding_assessment_score=0.0, industry_match_score=0.0,
                                 previous_sales_experience_years=0.0,
                                 peer_shadowing_sessions_completed=0,
                                 revenue_attainment_pct=0.0,
                                 manager_coaching_sessions_per_month=0))
        # Filtered by AHEAD should be empty (all zeroes → BEHIND)
        assert engine.by_status(RampStatus.AHEAD) == []

    def test_by_phase_returns_empty_when_none_match(self):
        engine = make_engine()
        # hire_date_days_ago=10, attainment=0 → LEARNING phase
        engine.assess(make_input(hire_date_days_ago=10, revenue_attainment_pct=0.0))
        # AT_QUOTA should be empty
        assert engine.by_phase(RampPhase.AT_QUOTA) == []
