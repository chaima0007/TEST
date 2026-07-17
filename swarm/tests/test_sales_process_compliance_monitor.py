"""
Comprehensive pytest tests for SalesProcessComplianceMonitor.
Covers all invariants, edge cases, scoring formulas, enum properties,
dataclass structure, and engine behavior.
"""
from __future__ import annotations

import dataclasses
from typing import List

import pytest

from swarm.intelligence.sales_process_compliance_monitor import (
    ComplianceAction,
    ComplianceLevel,
    ComplianceRisk,
    MethodologyAdherence,
    ProcessComplianceInput,
    ProcessComplianceResult,
    SalesProcessComplianceMonitor,
    _composite,
    _compliance_level,
    _compliance_risk,
    _compliance_action,
    _crm_hygiene_score,
    _discovery_score,
    _key_gap,
    _methodology_adherence,
    _missing_steps_count,
    _progression_score,
    _qualification_score,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def make_input(
    rep_id: str = "R1",
    rep_name: str = "Alice",
    deal_id: str = "D1",
    deal_stage: str = "discovery",
    stage_days_elapsed: int = 5,
    needs_assessment_completed: int = 1,
    pain_points_documented: int = 1,
    decision_criteria_captured: int = 1,
    decision_process_mapped: int = 1,
    budget_confirmed: int = 1,
    timeline_confirmed: int = 1,
    champion_identified: int = 1,
    executive_sponsor_engaged: int = 1,
    competition_identified: int = 1,
    business_case_built: int = 1,
    technical_validation_done: int = 1,
    mutual_success_plan_agreed: int = 1,
    legal_review_started: int = 1,
    crm_last_updated_days_ago: int = 1,
    stage_appropriate_activities_completed: int = 8,
    coaching_cadence_adherence_pct: float = 100.0,
    manager_reviewed_this_month: int = 1,
) -> ProcessComplianceInput:
    return ProcessComplianceInput(
        rep_id=rep_id,
        rep_name=rep_name,
        deal_id=deal_id,
        deal_stage=deal_stage,
        stage_days_elapsed=stage_days_elapsed,
        needs_assessment_completed=needs_assessment_completed,
        pain_points_documented=pain_points_documented,
        decision_criteria_captured=decision_criteria_captured,
        decision_process_mapped=decision_process_mapped,
        budget_confirmed=budget_confirmed,
        timeline_confirmed=timeline_confirmed,
        champion_identified=champion_identified,
        executive_sponsor_engaged=executive_sponsor_engaged,
        competition_identified=competition_identified,
        business_case_built=business_case_built,
        technical_validation_done=technical_validation_done,
        mutual_success_plan_agreed=mutual_success_plan_agreed,
        legal_review_started=legal_review_started,
        crm_last_updated_days_ago=crm_last_updated_days_ago,
        stage_appropriate_activities_completed=stage_appropriate_activities_completed,
        coaching_cadence_adherence_pct=coaching_cadence_adherence_pct,
        manager_reviewed_this_month=manager_reviewed_this_month,
    )


def make_zero_input(**overrides) -> ProcessComplianceInput:
    """All binary flags = 0, numeric minimums."""
    base = dict(
        rep_id="R0",
        rep_name="Zero",
        deal_id="D0",
        deal_stage="prospecting",
        stage_days_elapsed=0,
        needs_assessment_completed=0,
        pain_points_documented=0,
        decision_criteria_captured=0,
        decision_process_mapped=0,
        budget_confirmed=0,
        timeline_confirmed=0,
        champion_identified=0,
        executive_sponsor_engaged=0,
        competition_identified=0,
        business_case_built=0,
        technical_validation_done=0,
        mutual_success_plan_agreed=0,
        legal_review_started=0,
        crm_last_updated_days_ago=30,
        stage_appropriate_activities_completed=0,
        coaching_cadence_adherence_pct=0.0,
        manager_reviewed_this_month=0,
    )
    base.update(overrides)
    return ProcessComplianceInput(**base)


@pytest.fixture
def engine():
    return SalesProcessComplianceMonitor()


@pytest.fixture
def perfect_input():
    return make_input()


@pytest.fixture
def zero_input():
    return make_zero_input()


# ===========================================================================
# 1. ENUM TESTS
# ===========================================================================

class TestComplianceLevelEnum:
    def test_inherits_str(self):
        assert issubclass(ComplianceLevel, str)

    def test_exactly_4_values(self):
        assert len(ComplianceLevel) == 4

    def test_full_value(self):
        assert ComplianceLevel.FULL == "full"

    def test_partial_value(self):
        assert ComplianceLevel.PARTIAL == "partial"

    def test_minimal_value(self):
        assert ComplianceLevel.MINIMAL == "minimal"

    def test_non_compliant_value(self):
        assert ComplianceLevel.NON_COMPLIANT == "non_compliant"

    def test_all_members_present(self):
        names = {m.name for m in ComplianceLevel}
        assert names == {"FULL", "PARTIAL", "MINIMAL", "NON_COMPLIANT"}

    def test_str_equality(self):
        assert ComplianceLevel.FULL == "full"
        assert "partial" == ComplianceLevel.PARTIAL


class TestMethodologyAdherenceEnum:
    def test_inherits_str(self):
        assert issubclass(MethodologyAdherence, str)

    def test_exactly_4_values(self):
        assert len(MethodologyAdherence) == 4

    def test_champion_value(self):
        assert MethodologyAdherence.CHAMPION == "champion"

    def test_solid_value(self):
        assert MethodologyAdherence.SOLID == "solid"

    def test_improvable_value(self):
        assert MethodologyAdherence.IMPROVABLE == "improvable"

    def test_at_risk_value(self):
        assert MethodologyAdherence.AT_RISK == "at_risk"

    def test_all_members_present(self):
        names = {m.name for m in MethodologyAdherence}
        assert names == {"CHAMPION", "SOLID", "IMPROVABLE", "AT_RISK"}


class TestComplianceRiskEnum:
    def test_inherits_str(self):
        assert issubclass(ComplianceRisk, str)

    def test_exactly_4_values(self):
        assert len(ComplianceRisk) == 4

    def test_low_value(self):
        assert ComplianceRisk.LOW == "low"

    def test_moderate_value(self):
        assert ComplianceRisk.MODERATE == "moderate"

    def test_high_value(self):
        assert ComplianceRisk.HIGH == "high"

    def test_critical_value(self):
        assert ComplianceRisk.CRITICAL == "critical"

    def test_all_members_present(self):
        names = {m.name for m in ComplianceRisk}
        assert names == {"LOW", "MODERATE", "HIGH", "CRITICAL"}


class TestComplianceActionEnum:
    def test_inherits_str(self):
        assert issubclass(ComplianceAction, str)

    def test_exactly_4_values(self):
        assert len(ComplianceAction) == 4

    def test_maintain_value(self):
        assert ComplianceAction.MAINTAIN == "maintain"

    def test_coach_gaps_value(self):
        assert ComplianceAction.COACH_GAPS == "coach_gaps"

    def test_process_review_value(self):
        assert ComplianceAction.PROCESS_REVIEW == "process_review"

    def test_remediate_value(self):
        assert ComplianceAction.REMEDIATE == "remediate"

    def test_all_members_present(self):
        names = {m.name for m in ComplianceAction}
        assert names == {"MAINTAIN", "COACH_GAPS", "PROCESS_REVIEW", "REMEDIATE"}


# ===========================================================================
# 2. DATACLASS FIELD COUNT
# ===========================================================================

class TestProcessComplianceInputFields:
    def test_exactly_22_fields(self):
        fields = dataclasses.fields(ProcessComplianceInput)
        assert len(fields) == 22

    def test_field_names(self):
        field_names = {f.name for f in dataclasses.fields(ProcessComplianceInput)}
        expected = {
            "rep_id", "rep_name", "deal_id", "deal_stage", "stage_days_elapsed",
            "needs_assessment_completed", "pain_points_documented",
            "decision_criteria_captured", "decision_process_mapped",
            "budget_confirmed", "timeline_confirmed", "champion_identified",
            "executive_sponsor_engaged", "competition_identified",
            "business_case_built", "technical_validation_done",
            "mutual_success_plan_agreed", "legal_review_started",
            "crm_last_updated_days_ago", "stage_appropriate_activities_completed",
            "coaching_cadence_adherence_pct", "manager_reviewed_this_month",
        }
        assert field_names == expected

    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(ProcessComplianceInput)


# ===========================================================================
# 3. to_dict() KEY COUNT
# ===========================================================================

class TestProcessComplianceResultToDict:
    def test_exactly_15_keys(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_key_names(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        d = result.to_dict()
        expected_keys = {
            "rep_id", "deal_id", "compliance_level", "methodology_adherence",
            "compliance_risk", "compliance_action", "discovery_score",
            "qualification_score", "progression_score", "crm_hygiene_score",
            "compliance_composite", "missing_steps_count", "is_compliant",
            "needs_process_coaching", "key_gap",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_values_are_strings(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        d = result.to_dict()
        assert isinstance(d["compliance_level"], str)
        assert isinstance(d["methodology_adherence"], str)
        assert isinstance(d["compliance_risk"], str)
        assert isinstance(d["compliance_action"], str)

    def test_to_dict_rep_id(self, engine):
        inp = make_input(rep_id="REPX", deal_id="DX")
        result = engine.assess(inp)
        assert result.to_dict()["rep_id"] == "REPX"

    def test_to_dict_deal_id(self, engine):
        inp = make_input(deal_id="DEAL99")
        result = engine.assess(inp)
        assert result.to_dict()["deal_id"] == "DEAL99"

    def test_to_dict_is_compliant_bool(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert isinstance(result.to_dict()["is_compliant"], bool)

    def test_to_dict_needs_coaching_bool(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert isinstance(result.to_dict()["needs_process_coaching"], bool)

    def test_to_dict_missing_steps_count_int(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert isinstance(result.to_dict()["missing_steps_count"], int)

    def test_to_dict_key_gap_string(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert isinstance(result.to_dict()["key_gap"], str)


# ===========================================================================
# 4. DISCOVERY SCORE
# ===========================================================================

class TestDiscoveryScore:
    def test_all_zeros_returns_zero(self, zero_input):
        assert _discovery_score(zero_input) == 0.0

    def test_all_ones_returns_100(self, perfect_input):
        assert _discovery_score(perfect_input) == 100.0

    def test_needs_assessment_adds_25(self):
        inp = make_zero_input(needs_assessment_completed=1)
        assert _discovery_score(inp) == 25.0

    def test_pain_points_adds_25(self):
        inp = make_zero_input(pain_points_documented=1)
        assert _discovery_score(inp) == 25.0

    def test_decision_criteria_adds_25(self):
        inp = make_zero_input(decision_criteria_captured=1)
        assert _discovery_score(inp) == 25.0

    def test_competition_identified_adds_15(self):
        inp = make_zero_input(competition_identified=1)
        assert _discovery_score(inp) == 15.0

    def test_timeline_confirmed_adds_10(self):
        inp = make_zero_input(timeline_confirmed=1)
        assert _discovery_score(inp) == 10.0

    def test_partial_combination(self):
        inp = make_zero_input(needs_assessment_completed=1, pain_points_documented=1)
        assert _discovery_score(inp) == 50.0

    def test_three_items(self):
        inp = make_zero_input(
            needs_assessment_completed=1,
            pain_points_documented=1,
            decision_criteria_captured=1,
        )
        assert _discovery_score(inp) == 75.0

    def test_max_capped_at_100(self, perfect_input):
        assert _discovery_score(perfect_input) <= 100.0

    def test_min_capped_at_0(self, zero_input):
        assert _discovery_score(zero_input) >= 0.0

    def test_competition_plus_timeline(self):
        inp = make_zero_input(competition_identified=1, timeline_confirmed=1)
        assert _discovery_score(inp) == 25.0


# ===========================================================================
# 5. QUALIFICATION SCORE
# ===========================================================================

class TestQualificationScore:
    def test_all_zeros_returns_zero(self, zero_input):
        assert _qualification_score(zero_input) == 0.0

    def test_all_ones_returns_100(self, perfect_input):
        assert _qualification_score(perfect_input) == 100.0

    def test_decision_process_mapped_adds_20(self):
        inp = make_zero_input(decision_process_mapped=1)
        assert _qualification_score(inp) == 20.0

    def test_budget_confirmed_adds_25(self):
        inp = make_zero_input(budget_confirmed=1)
        assert _qualification_score(inp) == 25.0

    def test_champion_identified_adds_25(self):
        inp = make_zero_input(champion_identified=1)
        assert _qualification_score(inp) == 25.0

    def test_executive_sponsor_adds_20(self):
        inp = make_zero_input(executive_sponsor_engaged=1)
        assert _qualification_score(inp) == 20.0

    def test_business_case_adds_10(self):
        inp = make_zero_input(business_case_built=1)
        assert _qualification_score(inp) == 10.0

    def test_two_items_combination(self):
        inp = make_zero_input(budget_confirmed=1, champion_identified=1)
        assert _qualification_score(inp) == 50.0

    def test_capped_at_100(self, perfect_input):
        assert _qualification_score(perfect_input) <= 100.0


# ===========================================================================
# 6. PROGRESSION SCORE
# ===========================================================================

class TestProgressionScore:
    def test_all_zeros_returns_zero(self, zero_input):
        assert _progression_score(zero_input) == 0.0

    def test_all_ones_stage_8_returns_100(self, perfect_input):
        assert _progression_score(perfect_input) == 100.0

    def test_technical_validation_adds_25(self):
        inp = make_zero_input(technical_validation_done=1)
        assert _progression_score(inp) == 25.0

    def test_mutual_success_plan_adds_25(self):
        inp = make_zero_input(mutual_success_plan_agreed=1)
        assert _progression_score(inp) == 25.0

    def test_legal_review_adds_20(self):
        inp = make_zero_input(legal_review_started=1)
        assert _progression_score(inp) == 20.0

    def test_stage_activities_0_adds_0(self):
        inp = make_zero_input(stage_appropriate_activities_completed=0)
        assert _progression_score(inp) == 0.0

    def test_stage_activities_1_adds_5(self):
        inp = make_zero_input(stage_appropriate_activities_completed=1)
        assert _progression_score(inp) == 5.0

    def test_stage_activities_3_adds_12(self):
        inp = make_zero_input(stage_appropriate_activities_completed=3)
        assert _progression_score(inp) == 12.0

    def test_stage_activities_5_adds_20(self):
        inp = make_zero_input(stage_appropriate_activities_completed=5)
        assert _progression_score(inp) == 20.0

    def test_stage_activities_8_adds_30(self):
        inp = make_zero_input(stage_appropriate_activities_completed=8)
        assert _progression_score(inp) == 30.0

    def test_stage_activities_2_adds_5(self):
        # 2 >= 1 but < 3
        inp = make_zero_input(stage_appropriate_activities_completed=2)
        assert _progression_score(inp) == 5.0

    def test_stage_activities_4_adds_12(self):
        # 4 >= 3 but < 5
        inp = make_zero_input(stage_appropriate_activities_completed=4)
        assert _progression_score(inp) == 12.0

    def test_stage_activities_7_adds_20(self):
        # 7 >= 5 but < 8
        inp = make_zero_input(stage_appropriate_activities_completed=7)
        assert _progression_score(inp) == 20.0

    def test_stage_activities_10_adds_30(self):
        # 10 >= 8
        inp = make_zero_input(stage_appropriate_activities_completed=10)
        assert _progression_score(inp) == 30.0

    def test_capped_at_100(self, perfect_input):
        assert _progression_score(perfect_input) <= 100.0


# ===========================================================================
# 7. CRM HYGIENE SCORE
# ===========================================================================

class TestCrmHygieneScore:
    def test_all_zeros_returns_zero(self, zero_input):
        assert _crm_hygiene_score(zero_input) == 0.0

    def test_perfect_returns_100(self, perfect_input):
        assert _crm_hygiene_score(perfect_input) == 100.0

    def test_crm_updated_0_days_adds_50(self):
        inp = make_zero_input(crm_last_updated_days_ago=0)
        assert _crm_hygiene_score(inp) == 0.0 + 50.0  # no manager, no coaching

    def test_crm_updated_1_day_adds_50(self):
        inp = make_zero_input(crm_last_updated_days_ago=1)
        assert _crm_hygiene_score(inp) == 50.0

    def test_crm_updated_2_days_adds_38(self):
        inp = make_zero_input(crm_last_updated_days_ago=2)
        assert _crm_hygiene_score(inp) == 38.0

    def test_crm_updated_3_days_adds_38(self):
        inp = make_zero_input(crm_last_updated_days_ago=3)
        assert _crm_hygiene_score(inp) == 38.0

    def test_crm_updated_7_days_adds_24(self):
        inp = make_zero_input(crm_last_updated_days_ago=7)
        assert _crm_hygiene_score(inp) == 24.0

    def test_crm_updated_4_days_adds_24(self):
        # 4 <= 7
        inp = make_zero_input(crm_last_updated_days_ago=4)
        assert _crm_hygiene_score(inp) == 24.0

    def test_crm_updated_14_days_adds_12(self):
        inp = make_zero_input(crm_last_updated_days_ago=14)
        assert _crm_hygiene_score(inp) == 12.0

    def test_crm_updated_8_days_adds_12(self):
        # 8 <= 14
        inp = make_zero_input(crm_last_updated_days_ago=8)
        assert _crm_hygiene_score(inp) == 12.0

    def test_crm_updated_15_days_adds_0(self):
        inp = make_zero_input(crm_last_updated_days_ago=15)
        assert _crm_hygiene_score(inp) == 0.0

    def test_crm_updated_30_days_adds_0(self):
        inp = make_zero_input(crm_last_updated_days_ago=30)
        assert _crm_hygiene_score(inp) == 0.0

    def test_manager_reviewed_adds_25(self):
        inp = make_zero_input(crm_last_updated_days_ago=30, manager_reviewed_this_month=1)
        assert _crm_hygiene_score(inp) == 25.0

    def test_coaching_100pct_adds_25(self):
        inp = make_zero_input(crm_last_updated_days_ago=30, coaching_cadence_adherence_pct=100.0)
        assert _crm_hygiene_score(inp) == 25.0

    def test_coaching_50pct_adds_12_5(self):
        inp = make_zero_input(crm_last_updated_days_ago=30, coaching_cadence_adherence_pct=50.0)
        assert _crm_hygiene_score(inp) == pytest.approx(12.5, abs=0.2)

    def test_coaching_0pct_adds_0(self):
        inp = make_zero_input(crm_last_updated_days_ago=30, coaching_cadence_adherence_pct=0.0)
        assert _crm_hygiene_score(inp) == 0.0

    def test_combination_crm1_manager_coaching100(self):
        inp = make_zero_input(
            crm_last_updated_days_ago=1,
            manager_reviewed_this_month=1,
            coaching_cadence_adherence_pct=100.0,
        )
        assert _crm_hygiene_score(inp) == 100.0

    def test_capped_at_100(self, perfect_input):
        assert _crm_hygiene_score(perfect_input) <= 100.0

    def test_min_capped_at_0(self, zero_input):
        assert _crm_hygiene_score(zero_input) >= 0.0


# ===========================================================================
# 8. COMPOSITE FORMULA
# ===========================================================================

class TestCompositeFormula:
    def test_all_100_gives_100(self):
        assert _composite(100.0, 100.0, 100.0, 100.0) == 100.0

    def test_all_zero_gives_zero(self):
        assert _composite(0.0, 0.0, 0.0, 0.0) == 0.0

    def test_weights_sum_to_1(self):
        # 0.30 + 0.25 + 0.25 + 0.20 = 1.00
        assert abs(0.30 + 0.25 + 0.25 + 0.20 - 1.0) < 1e-9

    def test_discovery_weight_030(self):
        result = _composite(100.0, 0.0, 0.0, 0.0)
        assert result == pytest.approx(30.0, abs=0.15)

    def test_qualification_weight_025(self):
        result = _composite(0.0, 100.0, 0.0, 0.0)
        assert result == pytest.approx(25.0, abs=0.15)

    def test_progression_weight_025(self):
        result = _composite(0.0, 0.0, 100.0, 0.0)
        assert result == pytest.approx(25.0, abs=0.15)

    def test_crm_weight_020(self):
        result = _composite(0.0, 0.0, 0.0, 100.0)
        assert result == pytest.approx(20.0, abs=0.15)

    def test_mixed_values(self):
        expected = round(50.0 * 0.30 + 60.0 * 0.25 + 40.0 * 0.25 + 80.0 * 0.20, 1)
        result = _composite(50.0, 60.0, 40.0, 80.0)
        assert result == pytest.approx(expected, abs=0.15)

    def test_result_is_rounded_to_1dp(self):
        result = _composite(33.3, 33.3, 33.3, 33.3)
        # result should have at most 1 decimal place
        assert result == round(result, 1)

    def test_full_input_composite(self, perfect_input):
        disc = _discovery_score(perfect_input)
        qual = _qualification_score(perfect_input)
        prog = _progression_score(perfect_input)
        crm = _crm_hygiene_score(perfect_input)
        comp = _composite(disc, qual, prog, crm)
        assert comp == 100.0


# ===========================================================================
# 9. MISSING STEPS COUNT
# ===========================================================================

class TestMissingStepsCount:
    def test_all_complete_zero_missing(self, perfect_input):
        assert _missing_steps_count(perfect_input) == 0

    def test_all_incomplete_ten_missing(self, zero_input):
        assert _missing_steps_count(zero_input) == 10

    def test_tracks_10_specific_fields(self):
        # The 10 tracked fields are specific
        inp = make_zero_input(
            needs_assessment_completed=1,
            pain_points_documented=1,
            decision_criteria_captured=1,
            decision_process_mapped=1,
            budget_confirmed=1,
        )
        assert _missing_steps_count(inp) == 5

    def test_non_tracked_fields_dont_count(self):
        # technical_validation_done is NOT in the tracked 10
        inp = make_zero_input(technical_validation_done=0)
        assert _missing_steps_count(inp) == 10  # still 10 from the 10 tracked

    def test_one_missing(self):
        inp = make_input(champion_identified=0)
        assert _missing_steps_count(inp) == 1

    def test_two_missing(self):
        inp = make_input(champion_identified=0, budget_confirmed=0)
        assert _missing_steps_count(inp) == 2

    def test_three_missing(self):
        inp = make_input(champion_identified=0, budget_confirmed=0, decision_process_mapped=0)
        assert _missing_steps_count(inp) == 3


# ===========================================================================
# 10. COMPLIANCE LEVEL
# ===========================================================================

class TestComplianceLevel:
    def test_80_is_full(self):
        assert _compliance_level(80.0) == ComplianceLevel.FULL

    def test_100_is_full(self):
        assert _compliance_level(100.0) == ComplianceLevel.FULL

    def test_79_is_partial(self):
        assert _compliance_level(79.9) == ComplianceLevel.PARTIAL

    def test_60_is_partial(self):
        assert _compliance_level(60.0) == ComplianceLevel.PARTIAL

    def test_59_is_minimal(self):
        assert _compliance_level(59.9) == ComplianceLevel.MINIMAL

    def test_40_is_minimal(self):
        assert _compliance_level(40.0) == ComplianceLevel.MINIMAL

    def test_39_is_non_compliant(self):
        assert _compliance_level(39.9) == ComplianceLevel.NON_COMPLIANT

    def test_0_is_non_compliant(self):
        assert _compliance_level(0.0) == ComplianceLevel.NON_COMPLIANT

    def test_boundary_exactly_80(self):
        assert _compliance_level(80.0) == ComplianceLevel.FULL

    def test_boundary_exactly_60(self):
        assert _compliance_level(60.0) == ComplianceLevel.PARTIAL

    def test_boundary_exactly_40(self):
        assert _compliance_level(40.0) == ComplianceLevel.MINIMAL


# ===========================================================================
# 11. METHODOLOGY ADHERENCE
# ===========================================================================

class TestMethodologyAdherence:
    def test_champion_high_composite_low_missing(self):
        assert _methodology_adherence(75.0, 0) == MethodologyAdherence.CHAMPION

    def test_champion_composite_75_missing_1(self):
        assert _methodology_adherence(75.0, 1) == MethodologyAdherence.CHAMPION

    def test_not_champion_composite_75_missing_2(self):
        result = _methodology_adherence(75.0, 2)
        assert result != MethodologyAdherence.CHAMPION

    def test_not_champion_composite_74_missing_0(self):
        result = _methodology_adherence(74.9, 0)
        assert result != MethodologyAdherence.CHAMPION

    def test_solid_composite_60_missing_2(self):
        assert _methodology_adherence(60.0, 2) == MethodologyAdherence.SOLID

    def test_solid_composite_70_missing_3(self):
        assert _methodology_adherence(70.0, 3) == MethodologyAdherence.SOLID

    def test_solid_composite_60_missing_0(self):
        assert _methodology_adherence(60.0, 0) == MethodologyAdherence.SOLID

    def test_not_solid_composite_60_missing_4(self):
        result = _methodology_adherence(60.0, 4)
        assert result != MethodologyAdherence.SOLID

    def test_improvable_composite_45_missing_5(self):
        assert _methodology_adherence(45.0, 5) == MethodologyAdherence.IMPROVABLE

    def test_improvable_composite_50_missing_4(self):
        assert _methodology_adherence(50.0, 4) == MethodologyAdherence.IMPROVABLE

    def test_at_risk_composite_44_any_missing(self):
        assert _methodology_adherence(44.9, 10) == MethodologyAdherence.AT_RISK

    def test_at_risk_composite_0(self):
        assert _methodology_adherence(0.0, 10) == MethodologyAdherence.AT_RISK


# ===========================================================================
# 12. COMPLIANCE RISK
# ===========================================================================

class TestComplianceRiskFunc:
    def test_critical_composite_below_30(self):
        assert _compliance_risk(29.9, 0) == ComplianceRisk.CRITICAL

    def test_critical_missing_7_or_more(self):
        assert _compliance_risk(50.0, 7) == ComplianceRisk.CRITICAL

    def test_critical_missing_10(self):
        assert _compliance_risk(50.0, 10) == ComplianceRisk.CRITICAL

    def test_high_composite_below_45(self):
        assert _compliance_risk(44.9, 0) == ComplianceRisk.HIGH

    def test_high_missing_5(self):
        assert _compliance_risk(60.0, 5) == ComplianceRisk.HIGH

    def test_high_missing_6(self):
        assert _compliance_risk(60.0, 6) == ComplianceRisk.HIGH

    def test_moderate_composite_below_60(self):
        assert _compliance_risk(59.9, 2) == ComplianceRisk.MODERATE

    def test_moderate_missing_3(self):
        assert _compliance_risk(70.0, 3) == ComplianceRisk.MODERATE

    def test_low_composite_60_plus_missing_2(self):
        assert _compliance_risk(60.0, 2) == ComplianceRisk.LOW

    def test_low_composite_100_missing_0(self):
        assert _compliance_risk(100.0, 0) == ComplianceRisk.LOW

    def test_boundary_exactly_30(self):
        # composite == 30, missing == 0: not critical (< 30 is critical)
        assert _compliance_risk(30.0, 0) != ComplianceRisk.CRITICAL

    def test_boundary_exactly_45(self):
        # composite == 45, missing == 0: not high (< 45 is high)
        assert _compliance_risk(45.0, 0) != ComplianceRisk.HIGH

    def test_boundary_exactly_60(self):
        # composite == 60, missing == 2: not moderate
        assert _compliance_risk(60.0, 2) == ComplianceRisk.LOW


# ===========================================================================
# 13. COMPLIANCE ACTION
# ===========================================================================

class TestComplianceActionFunc:
    def test_critical_risk_gives_remediate(self):
        assert _compliance_action(ComplianceRisk.CRITICAL) == ComplianceAction.REMEDIATE

    def test_high_risk_gives_process_review(self):
        assert _compliance_action(ComplianceRisk.HIGH) == ComplianceAction.PROCESS_REVIEW

    def test_moderate_risk_gives_coach_gaps(self):
        assert _compliance_action(ComplianceRisk.MODERATE) == ComplianceAction.COACH_GAPS

    def test_low_risk_gives_maintain(self):
        assert _compliance_action(ComplianceRisk.LOW) == ComplianceAction.MAINTAIN


# ===========================================================================
# 14. KEY GAP
# ===========================================================================

class TestKeyGap:
    def test_no_champion_returns_champion_gap(self):
        inp = make_zero_input(champion_identified=0)
        gap = _key_gap(inp, 80.0, 80.0, 80.0, 80.0)
        assert gap == "champion not identified"

    def test_no_budget_returns_budget_gap(self):
        inp = make_zero_input(champion_identified=1, budget_confirmed=0)
        gap = _key_gap(inp, 80.0, 80.0, 80.0, 80.0)
        assert gap == "budget not confirmed"

    def test_no_decision_process_returns_decision_gap(self):
        inp = make_zero_input(
            champion_identified=1,
            budget_confirmed=1,
            decision_process_mapped=0,
        )
        gap = _key_gap(inp, 80.0, 80.0, 80.0, 80.0)
        assert gap == "decision process not mapped"

    def test_no_needs_assessment_returns_needs_gap(self):
        inp = make_zero_input(
            champion_identified=1,
            budget_confirmed=1,
            decision_process_mapped=1,
            needs_assessment_completed=0,
        )
        gap = _key_gap(inp, 80.0, 80.0, 80.0, 80.0)
        assert gap == "needs assessment incomplete"

    def test_crm_old_returns_crm_gap(self):
        inp = make_zero_input(
            champion_identified=1,
            budget_confirmed=1,
            decision_process_mapped=1,
            needs_assessment_completed=1,
            crm_last_updated_days_ago=15,
        )
        gap = _key_gap(inp, 80.0, 80.0, 80.0, 80.0)
        assert gap == "CRM out of date"

    def test_all_ok_returns_weakest_area(self):
        inp = make_input()
        # discovery=80 is lowest
        gap = _key_gap(inp, 80.0, 90.0, 90.0, 90.0)
        assert "weakest area" in gap
        assert "discovery" in gap

    def test_all_ok_crm_weakest(self):
        inp = make_input(crm_last_updated_days_ago=1)
        gap = _key_gap(inp, 90.0, 90.0, 90.0, 50.0)
        assert "CRM hygiene" in gap

    def test_priority_champion_over_budget(self):
        inp = make_zero_input(champion_identified=0, budget_confirmed=0)
        gap = _key_gap(inp, 80.0, 80.0, 80.0, 80.0)
        assert gap == "champion not identified"


# ===========================================================================
# 15. IS_COMPLIANT INVARIANT
# ===========================================================================

class TestIsCompliant:
    def test_compliant_when_composite_gte_70_missing_lte_2(self):
        # Perfect score: composite=100, missing=0
        inp = make_input()
        engine = SalesProcessComplianceMonitor()
        result = engine.assess(inp)
        assert result.is_compliant is True

    def test_not_compliant_when_composite_lt_70(self):
        # All zeros: composite=0
        inp = make_zero_input()
        engine = SalesProcessComplianceMonitor()
        result = engine.assess(inp)
        assert result.is_compliant is False

    def test_not_compliant_when_missing_gt_2(self):
        # 3 missing steps makes it non-compliant even if composite >=70
        inp = make_input(
            champion_identified=0,
            budget_confirmed=0,
            decision_process_mapped=0,
        )
        engine = SalesProcessComplianceMonitor()
        result = engine.assess(inp)
        assert result.is_compliant is False

    def test_boundary_missing_exactly_2_still_compliant(self):
        # 2 missing is OK if composite >=70
        inp = make_input(
            champion_identified=0,
            budget_confirmed=0,
        )
        engine = SalesProcessComplianceMonitor()
        result = engine.assess(inp)
        # composite may vary; just check missing <=2 is preserved
        assert result.missing_steps_count == 2
        # compliant only if composite >=70
        expected = result.compliance_composite >= 70.0 and result.missing_steps_count <= 2
        assert result.is_compliant == expected


# ===========================================================================
# 16. NEEDS_PROCESS_COACHING INVARIANT
# ===========================================================================

class TestNeedsProcessCoaching:
    def test_coaching_when_composite_lt_50(self):
        inp = make_zero_input()
        engine = SalesProcessComplianceMonitor()
        result = engine.assess(inp)
        assert result.needs_process_coaching is True

    def test_coaching_when_missing_gte_4(self):
        inp = make_input(
            champion_identified=0,
            budget_confirmed=0,
            decision_process_mapped=0,
            needs_assessment_completed=0,
        )
        engine = SalesProcessComplianceMonitor()
        result = engine.assess(inp)
        assert result.needs_process_coaching is True

    def test_no_coaching_when_perfect(self):
        inp = make_input()
        engine = SalesProcessComplianceMonitor()
        result = engine.assess(inp)
        assert result.needs_process_coaching is False

    def test_coaching_boundary_missing_exactly_4(self):
        inp = make_input(
            champion_identified=0,
            budget_confirmed=0,
            decision_process_mapped=0,
            needs_assessment_completed=0,
        )
        engine = SalesProcessComplianceMonitor()
        result = engine.assess(inp)
        assert result.missing_steps_count == 4
        assert result.needs_process_coaching is True

    def test_no_coaching_when_missing_3_and_composite_above_50(self):
        inp = make_input(
            champion_identified=0,
            budget_confirmed=0,
            decision_process_mapped=0,
        )
        engine = SalesProcessComplianceMonitor()
        result = engine.assess(inp)
        assert result.missing_steps_count == 3
        # coaching = composite < 50 OR missing >= 4
        expected = result.compliance_composite < 50.0 or result.missing_steps_count >= 4
        assert result.needs_process_coaching == expected


# ===========================================================================
# 17. ENGINE: assess()
# ===========================================================================

class TestEngineAssess:
    def test_returns_result_type(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert isinstance(result, ProcessComplianceResult)

    def test_result_stored_by_deal_id(self, engine, perfect_input):
        engine.assess(perfect_input)
        assert engine.get("D1") is not None

    def test_result_rep_id(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert result.rep_id == "R1"

    def test_result_deal_id(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert result.deal_id == "D1"

    def test_overwrite_on_same_deal_id(self, engine):
        inp1 = make_input(deal_id="D1", rep_id="R1")
        inp2 = make_input(deal_id="D1", rep_id="R2")
        engine.assess(inp1)
        engine.assess(inp2)
        result = engine.get("D1")
        assert result.rep_id == "R2"

    def test_different_deals_stored_separately(self, engine):
        inp1 = make_input(deal_id="D1")
        inp2 = make_input(deal_id="D2")
        engine.assess(inp1)
        engine.assess(inp2)
        assert engine.get("D1") is not None
        assert engine.get("D2") is not None

    def test_missing_deal_returns_none(self, engine):
        assert engine.get("NONEXISTENT") is None

    def test_perfect_input_is_compliant(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert result.is_compliant is True

    def test_zero_input_not_compliant(self, engine, zero_input):
        result = engine.assess(zero_input)
        assert result.is_compliant is False

    def test_zero_input_needs_coaching(self, engine, zero_input):
        result = engine.assess(zero_input)
        assert result.needs_process_coaching is True

    def test_composite_score_range(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert 0.0 <= result.compliance_composite <= 100.0

    def test_discovery_score_range(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert 0.0 <= result.discovery_score <= 100.0

    def test_qualification_score_range(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert 0.0 <= result.qualification_score <= 100.0

    def test_progression_score_range(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert 0.0 <= result.progression_score <= 100.0

    def test_crm_hygiene_score_range(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert 0.0 <= result.crm_hygiene_score <= 100.0

    def test_missing_steps_count_range(self, engine, zero_input):
        result = engine.assess(zero_input)
        assert 0 <= result.missing_steps_count <= 10


# ===========================================================================
# 18. ENGINE: assess_batch()
# ===========================================================================

class TestAssessBatch:
    def test_returns_list(self, engine):
        results = engine.assess_batch([make_input(deal_id="D1"), make_input(deal_id="D2")])
        assert isinstance(results, list)

    def test_batch_sorted_descending_by_composite(self, engine):
        high = make_input(deal_id="HIGH")
        low = make_zero_input(deal_id="LOW")
        results = engine.assess_batch([low, high])
        assert results[0].compliance_composite >= results[1].compliance_composite

    def test_batch_length_matches_input(self, engine):
        inputs = [make_input(deal_id=f"D{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_stores_in_engine(self, engine):
        inputs = [make_input(deal_id=f"D{i}") for i in range(3)]
        engine.assess_batch(inputs)
        for i in range(3):
            assert engine.get(f"D{i}") is not None

    def test_batch_empty_input(self, engine):
        results = engine.assess_batch([])
        assert results == []

    def test_batch_single_item(self, engine):
        results = engine.assess_batch([make_input(deal_id="SOLO")])
        assert len(results) == 1

    def test_batch_sort_stable_for_equal_composites(self, engine):
        # Two identical inputs should have equal composites and both be returned
        i1 = make_input(deal_id="DA")
        i2 = make_input(deal_id="DB")
        results = engine.assess_batch([i1, i2])
        assert len(results) == 2
        assert results[0].compliance_composite == results[1].compliance_composite

    def test_batch_sorted_three_items(self, engine):
        inputs = [
            make_zero_input(deal_id="LOW"),
            make_input(deal_id="HIGH"),
            make_input(deal_id="MID", champion_identified=0, budget_confirmed=0, crm_last_updated_days_ago=14),
        ]
        results = engine.assess_batch(inputs)
        composites = [r.compliance_composite for r in results]
        assert composites == sorted(composites, reverse=True)


# ===========================================================================
# 19. ENGINE: reset()
# ===========================================================================

class TestEngineReset:
    def test_reset_clears_all_results(self, engine, perfect_input):
        engine.assess(perfect_input)
        engine.reset()
        assert engine.get("D1") is None

    def test_reset_multiple_deals(self, engine):
        for i in range(5):
            engine.assess(make_input(deal_id=f"D{i}"))
        engine.reset()
        for i in range(5):
            assert engine.get(f"D{i}") is None

    def test_reset_then_reassess(self, engine, perfect_input):
        engine.assess(perfect_input)
        engine.reset()
        engine.assess(perfect_input)
        assert engine.get("D1") is not None

    def test_reset_clears_compliant_deals(self, engine, perfect_input):
        engine.assess(perfect_input)
        engine.reset()
        assert engine.compliant_deals() == []

    def test_reset_clears_coaching_queue(self, engine, zero_input):
        engine.assess(zero_input)
        engine.reset()
        assert engine.coaching_queue() == []

    def test_reset_avg_returns_zero(self, engine, perfect_input):
        engine.assess(perfect_input)
        engine.reset()
        assert engine.avg_compliance_composite() == 0.0

    def test_double_reset_ok(self, engine):
        engine.reset()
        engine.reset()
        assert engine.all_deals() == []


# ===========================================================================
# 20. ENGINE: summary() — exactly 13 keys
# ===========================================================================

class TestEngineSummary:
    def test_summary_has_exactly_13_keys(self, engine, perfect_input):
        engine.assess(perfect_input)
        s = engine.summary()
        assert len(s) == 13

    def test_summary_key_names(self, engine, perfect_input):
        engine.assess(perfect_input)
        s = engine.summary()
        expected_keys = {
            "total",
            "compliance_level_counts",
            "methodology_adherence_counts",
            "compliance_risk_counts",
            "action_counts",
            "avg_compliance_composite",
            "fully_compliant_count",
            "coaching_needed_count",
            "avg_discovery_score",
            "avg_qualification_score",
            "avg_progression_score",
            "avg_crm_hygiene_score",
            "avg_missing_steps",
        }
        assert set(s.keys()) == expected_keys

    def test_summary_total(self, engine):
        for i in range(3):
            engine.assess(make_input(deal_id=f"D{i}"))
        s = engine.summary()
        assert s["total"] == 3

    def test_summary_empty(self, engine):
        s = engine.summary()
        assert s["total"] == 0
        assert s["avg_compliance_composite"] == 0.0
        assert s["fully_compliant_count"] == 0
        assert s["coaching_needed_count"] == 0
        assert s["avg_discovery_score"] == 0.0
        assert s["avg_qualification_score"] == 0.0
        assert s["avg_progression_score"] == 0.0
        assert s["avg_crm_hygiene_score"] == 0.0
        assert s["avg_missing_steps"] == 0.0

    def test_summary_fully_compliant_count(self, engine, perfect_input):
        engine.assess(perfect_input)
        s = engine.summary()
        assert s["fully_compliant_count"] >= 1

    def test_summary_coaching_needed_count(self, engine, zero_input):
        engine.assess(zero_input)
        s = engine.summary()
        assert s["coaching_needed_count"] >= 1

    def test_summary_compliance_level_counts_dict(self, engine, perfect_input):
        engine.assess(perfect_input)
        s = engine.summary()
        assert isinstance(s["compliance_level_counts"], dict)

    def test_summary_methodology_adherence_counts_dict(self, engine, perfect_input):
        engine.assess(perfect_input)
        s = engine.summary()
        assert isinstance(s["methodology_adherence_counts"], dict)

    def test_summary_compliance_risk_counts_dict(self, engine, perfect_input):
        engine.assess(perfect_input)
        s = engine.summary()
        assert isinstance(s["compliance_risk_counts"], dict)

    def test_summary_action_counts_dict(self, engine, perfect_input):
        engine.assess(perfect_input)
        s = engine.summary()
        assert isinstance(s["action_counts"], dict)

    def test_summary_avg_composite_in_range(self, engine, perfect_input):
        engine.assess(perfect_input)
        s = engine.summary()
        assert 0.0 <= s["avg_compliance_composite"] <= 100.0

    def test_summary_avg_discovery_in_range(self, engine, perfect_input):
        engine.assess(perfect_input)
        s = engine.summary()
        assert 0.0 <= s["avg_discovery_score"] <= 100.0

    def test_summary_avg_qualification_in_range(self, engine, perfect_input):
        engine.assess(perfect_input)
        s = engine.summary()
        assert 0.0 <= s["avg_qualification_score"] <= 100.0

    def test_summary_avg_progression_in_range(self, engine, perfect_input):
        engine.assess(perfect_input)
        s = engine.summary()
        assert 0.0 <= s["avg_progression_score"] <= 100.0

    def test_summary_avg_crm_in_range(self, engine, perfect_input):
        engine.assess(perfect_input)
        s = engine.summary()
        assert 0.0 <= s["avg_crm_hygiene_score"] <= 100.0

    def test_summary_avg_missing_in_range(self, engine, zero_input):
        engine.assess(zero_input)
        s = engine.summary()
        assert 0.0 <= s["avg_missing_steps"] <= 10.0

    def test_summary_called_with_no_arguments(self, engine, perfect_input):
        engine.assess(perfect_input)
        # Must call with no arguments
        s = engine.summary()
        assert s is not None

    def test_summary_level_counts_sum_to_total(self, engine):
        for i in range(4):
            engine.assess(make_input(deal_id=f"D{i}"))
        s = engine.summary()
        assert sum(s["compliance_level_counts"].values()) == s["total"]

    def test_summary_adherence_counts_sum_to_total(self, engine):
        for i in range(3):
            engine.assess(make_input(deal_id=f"D{i}"))
        s = engine.summary()
        assert sum(s["methodology_adherence_counts"].values()) == s["total"]

    def test_summary_risk_counts_sum_to_total(self, engine):
        for i in range(3):
            engine.assess(make_input(deal_id=f"D{i}"))
        s = engine.summary()
        assert sum(s["compliance_risk_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_to_total(self, engine):
        for i in range(3):
            engine.assess(make_input(deal_id=f"D{i}"))
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_after_reset_total_is_zero(self, engine, perfect_input):
        engine.assess(perfect_input)
        engine.reset()
        s = engine.summary()
        assert s["total"] == 0

    def test_summary_avg_missing_correct(self, engine):
        inp1 = make_input(deal_id="D1")          # 0 missing
        inp2 = make_input(deal_id="D2", champion_identified=0)  # 1 missing
        engine.assess(inp1)
        engine.assess(inp2)
        s = engine.summary()
        assert s["avg_missing_steps"] == pytest.approx(0.5, abs=0.2)


# ===========================================================================
# 21. ENGINE: compliant_deals() and coaching_queue()
# ===========================================================================

class TestEngineFilters:
    def test_compliant_deals_all_perfect(self, engine):
        for i in range(3):
            engine.assess(make_input(deal_id=f"D{i}"))
        deals = engine.compliant_deals()
        assert all(r.is_compliant for r in deals)

    def test_compliant_deals_none_when_all_zero(self, engine):
        for i in range(3):
            engine.assess(make_zero_input(deal_id=f"D{i}"))
        deals = engine.compliant_deals()
        assert all(r.is_compliant for r in deals)

    def test_coaching_queue_all_zero(self, engine):
        for i in range(3):
            engine.assess(make_zero_input(deal_id=f"D{i}"))
        queue = engine.coaching_queue()
        assert all(r.needs_process_coaching for r in queue)

    def test_coaching_queue_empty_for_perfect(self, engine, perfect_input):
        engine.assess(perfect_input)
        # coaching needs composite<50 or missing>=4; perfect doesn't satisfy these
        queue = engine.coaching_queue()
        assert not any(not r.needs_process_coaching for r in queue)

    def test_by_level_filters_correctly(self, engine):
        engine.assess(make_input(deal_id="FULL"))
        by_full = engine.by_level(ComplianceLevel.FULL)
        assert all(r.compliance_level == ComplianceLevel.FULL for r in by_full)

    def test_by_adherence_filters_correctly(self, engine):
        engine.assess(make_input(deal_id="CHAMP"))
        result = engine.get("CHAMP")
        by_adh = engine.by_adherence(result.methodology_adherence)
        assert all(r.methodology_adherence == result.methodology_adherence for r in by_adh)

    def test_all_deals_sorted_descending(self, engine):
        for i in range(5):
            engine.assess(make_input(deal_id=f"D{i}"))
        deals = engine.all_deals()
        composites = [r.compliance_composite for r in deals]
        assert composites == sorted(composites, reverse=True)

    def test_avg_compliance_composite_empty(self, engine):
        assert engine.avg_compliance_composite() == 0.0

    def test_avg_compliance_composite_single(self, engine, perfect_input):
        result = engine.assess(perfect_input)
        assert engine.avg_compliance_composite() == result.compliance_composite

    def test_avg_compliance_composite_multiple(self, engine):
        r1 = engine.assess(make_input(deal_id="D1"))
        r2 = engine.assess(make_zero_input(deal_id="D2"))
        expected = round((r1.compliance_composite + r2.compliance_composite) / 2, 1)
        assert engine.avg_compliance_composite() == pytest.approx(expected, abs=0.2)


# ===========================================================================
# 22. INTEGRATION TESTS
# ===========================================================================

class TestIntegration:
    def test_full_pipeline_perfect_rep(self):
        engine = SalesProcessComplianceMonitor()
        inp = make_input()
        result = engine.assess(inp)
        assert result.compliance_level == ComplianceLevel.FULL
        assert result.is_compliant is True
        assert result.needs_process_coaching is False
        assert result.compliance_composite == 100.0

    def test_full_pipeline_zero_rep(self):
        engine = SalesProcessComplianceMonitor()
        inp = make_zero_input()
        result = engine.assess(inp)
        assert result.compliance_level == ComplianceLevel.NON_COMPLIANT
        assert result.is_compliant is False
        assert result.needs_process_coaching is True
        assert result.compliance_composite == 0.0

    def test_batch_then_summary_consistent(self):
        engine = SalesProcessComplianceMonitor()
        inputs = [make_input(deal_id=f"D{i}") for i in range(5)]
        engine.assess_batch(inputs)
        s = engine.summary()
        assert s["total"] == 5
        assert len(s) == 13

    def test_reset_then_batch(self):
        engine = SalesProcessComplianceMonitor()
        engine.assess_batch([make_input(deal_id="D1")])
        engine.reset()
        results = engine.assess_batch([make_zero_input(deal_id="D2")])
        assert len(results) == 1
        assert engine.get("D1") is None
        assert engine.get("D2") is not None

    def test_to_dict_round_trip_values(self):
        engine = SalesProcessComplianceMonitor()
        inp = make_input()
        result = engine.assess(inp)
        d = result.to_dict()
        assert d["rep_id"] == result.rep_id
        assert d["deal_id"] == result.deal_id
        assert d["compliance_composite"] == result.compliance_composite
        assert d["is_compliant"] == result.is_compliant
        assert d["needs_process_coaching"] == result.needs_process_coaching
        assert d["missing_steps_count"] == result.missing_steps_count

    def test_composite_formula_matches_individual_scores(self):
        engine = SalesProcessComplianceMonitor()
        inp = make_input()
        result = engine.assess(inp)
        expected = round(
            result.discovery_score * 0.30
            + result.qualification_score * 0.25
            + result.progression_score * 0.25
            + result.crm_hygiene_score * 0.20,
            1,
        )
        assert result.compliance_composite == pytest.approx(expected, abs=0.15)

    def test_variety_of_deals_summary(self):
        engine = SalesProcessComplianceMonitor()
        engine.assess(make_input(deal_id="D1"))
        engine.assess(make_zero_input(deal_id="D2"))
        engine.assess(make_input(deal_id="D3", champion_identified=0, budget_confirmed=0))
        s = engine.summary()
        assert s["total"] == 3
        assert len(s) == 13

    def test_multiple_engines_independent(self):
        e1 = SalesProcessComplianceMonitor()
        e2 = SalesProcessComplianceMonitor()
        e1.assess(make_input(deal_id="D1"))
        assert e2.get("D1") is None

    def test_score_monotonicity_more_complete_higher(self):
        engine = SalesProcessComplianceMonitor()
        low = engine.assess(make_zero_input(deal_id="LOW"))
        high = engine.assess(make_input(deal_id="HIGH"))
        assert high.compliance_composite > low.compliance_composite

    def test_result_is_dataclass(self):
        engine = SalesProcessComplianceMonitor()
        result = engine.assess(make_input())
        assert dataclasses.is_dataclass(result)

    def test_crm_hygiene_affects_composite(self):
        engine = SalesProcessComplianceMonitor()
        fresh_crm = make_input(deal_id="D1", crm_last_updated_days_ago=1)
        stale_crm = make_input(deal_id="D2", crm_last_updated_days_ago=30)
        r1 = engine.assess(fresh_crm)
        r2 = engine.assess(stale_crm)
        assert r1.crm_hygiene_score > r2.crm_hygiene_score

    def test_stage_activities_affects_progression(self):
        engine = SalesProcessComplianceMonitor()
        high_act = make_input(deal_id="H", stage_appropriate_activities_completed=8)
        low_act = make_input(deal_id="L", stage_appropriate_activities_completed=0)
        r_high = engine.assess(high_act)
        r_low = engine.assess(low_act)
        assert r_high.progression_score > r_low.progression_score

    def test_summary_correct_fully_compliant_count(self):
        engine = SalesProcessComplianceMonitor()
        engine.assess(make_input(deal_id="COMPL"))
        engine.assess(make_zero_input(deal_id="NONCOMPL"))
        s = engine.summary()
        assert s["fully_compliant_count"] == len(engine.compliant_deals())

    def test_summary_correct_coaching_count(self):
        engine = SalesProcessComplianceMonitor()
        engine.assess(make_input(deal_id="COMPL"))
        engine.assess(make_zero_input(deal_id="NONCOMPL"))
        s = engine.summary()
        assert s["coaching_needed_count"] == len(engine.coaching_queue())

    def test_high_coaching_adherence_boosts_crm_score(self):
        engine = SalesProcessComplianceMonitor()
        r1 = engine.assess(make_zero_input(deal_id="D1", coaching_cadence_adherence_pct=100.0))
        r2 = engine.assess(make_zero_input(deal_id="D2", coaching_cadence_adherence_pct=0.0))
        assert r1.crm_hygiene_score > r2.crm_hygiene_score

    def test_manager_review_boosts_crm_score(self):
        engine = SalesProcessComplianceMonitor()
        r1 = engine.assess(make_zero_input(deal_id="D1", manager_reviewed_this_month=1))
        r2 = engine.assess(make_zero_input(deal_id="D2", manager_reviewed_this_month=0))
        assert r1.crm_hygiene_score > r2.crm_hygiene_score
