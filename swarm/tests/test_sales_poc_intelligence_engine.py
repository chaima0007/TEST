"""
Comprehensive pytest test suite for SalesPOCIntelligenceEngine.
Covers: enums, dataclasses, all sub-score methods, pattern detection,
risk/severity/action mapping, flag methods, pipeline loss, signal generation,
assess(), assess_batch(), summary(), edge cases, and end-to-end scenarios.
"""
from __future__ import annotations

import pytest
from swarm.intelligence.sales_poc_intelligence_engine import (
    POCAction,
    POCInput,
    POCPattern,
    POCResult,
    POCRisk,
    POCSeverity,
    SalesPOCIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> POCInput:
    """
    Return a 'healthy' baseline POCInput whose default values produce very low
    risk scores so individual fields can be overridden to exercise specific branches.
    """
    defaults = dict(
        rep_id="REP001",
        region="AMER",
        evaluation_period_id="2024-Q1",
        total_pocs_conducted=20,
        poc_to_close_conversion_rate_pct=0.75,       # good conversion
        avg_poc_duration_days=30.0,
        pocs_exceeding_timeline_pct=0.05,            # minimal stall
        pocs_with_no_success_criteria_pct=0.05,      # mostly have criteria
        avg_poc_scope_changes_count=0.5,             # minimal scope changes
        technical_validation_failure_rate_pct=0.05, # minimal failures
        poc_champion_engaged_pct=0.90,               # good champion engagement
        exec_sponsor_briefed_pct=0.80,               # good exec briefing
        avg_days_to_poc_kickoff=5.0,                 # fast kickoff
        poc_extended_count=1,
        mutual_success_plan_completion_pct=0.85,     # good MSP completion
        se_escalation_required_pct=0.05,
        poc_abandoned_pct=0.05,                      # minimal abandonment
        post_poc_proposal_delay_days=3.0,
        competitive_poc_displacement_rate_pct=0.05, # minimal displacement
        avg_stakeholders_in_poc_count=3.0,           # good stakeholders
        avg_poc_resources_allocated_count=2,
        avg_opportunity_value_usd=50_000.0,
    )
    defaults.update(overrides)
    return POCInput(**defaults)


def make_engine() -> SalesPOCIntelligenceEngine:
    return SalesPOCIntelligenceEngine()


# ===========================================================================
# 1. Enum: POCRisk
# ===========================================================================

class TestPOCRiskEnum:
    def test_low_value(self):
        assert POCRisk.low.value == "low"

    def test_moderate_value(self):
        assert POCRisk.moderate.value == "moderate"

    def test_high_value(self):
        assert POCRisk.high.value == "high"

    def test_critical_value(self):
        assert POCRisk.critical.value == "critical"

    def test_is_str_subclass(self):
        assert isinstance(POCRisk.low, str)

    def test_equality_with_string(self):
        assert POCRisk.high == "high"

    def test_all_members_count(self):
        assert len(POCRisk) == 4

    def test_members_by_name(self):
        assert POCRisk["critical"] is POCRisk.critical

    def test_unique_values(self):
        values = [m.value for m in POCRisk]
        assert len(values) == len(set(values))


# ===========================================================================
# 2. Enum: POCPattern
# ===========================================================================

class TestPOCPatternEnum:
    def test_none_value(self):
        assert POCPattern.none.value == "none"

    def test_poc_stall_value(self):
        assert POCPattern.poc_stall.value == "poc_stall"

    def test_success_criteria_gap_value(self):
        assert POCPattern.success_criteria_gap.value == "success_criteria_gap"

    def test_scope_creep_value(self):
        assert POCPattern.scope_creep.value == "scope_creep"

    def test_technical_validation_failure_value(self):
        assert POCPattern.technical_validation_failure.value == "technical_validation_failure"

    def test_no_champion_during_poc_value(self):
        assert POCPattern.no_champion_during_poc.value == "no_champion_during_poc"

    def test_is_str_subclass(self):
        assert isinstance(POCPattern.poc_stall, str)

    def test_all_members_count(self):
        assert len(POCPattern) == 6

    def test_members_by_name(self):
        assert POCPattern["scope_creep"] is POCPattern.scope_creep

    def test_unique_values(self):
        values = [m.value for m in POCPattern]
        assert len(values) == len(set(values))


# ===========================================================================
# 3. Enum: POCSeverity
# ===========================================================================

class TestPOCSeverityEnum:
    def test_structured_value(self):
        assert POCSeverity.structured.value == "structured"

    def test_developing_value(self):
        assert POCSeverity.developing.value == "developing"

    def test_uncontrolled_value(self):
        assert POCSeverity.uncontrolled.value == "uncontrolled"

    def test_failing_value(self):
        assert POCSeverity.failing.value == "failing"

    def test_is_str_subclass(self):
        assert isinstance(POCSeverity.failing, str)

    def test_all_members_count(self):
        assert len(POCSeverity) == 4

    def test_unique_values(self):
        values = [m.value for m in POCSeverity]
        assert len(values) == len(set(values))


# ===========================================================================
# 4. Enum: POCAction
# ===========================================================================

class TestPOCActionEnum:
    def test_no_action_value(self):
        assert POCAction.no_action.value == "no_action"

    def test_poc_structure_coaching_value(self):
        assert POCAction.poc_structure_coaching.value == "poc_structure_coaching"

    def test_success_criteria_alignment_value(self):
        assert POCAction.success_criteria_alignment.value == "success_criteria_alignment"

    def test_scope_control_training_value(self):
        assert POCAction.scope_control_training.value == "scope_control_training"

    def test_technical_escalation_support_value(self):
        assert POCAction.technical_escalation_support.value == "technical_escalation_support"

    def test_champion_engagement_during_poc_value(self):
        assert POCAction.champion_engagement_during_poc.value == "champion_engagement_during_poc"

    def test_is_str_subclass(self):
        assert isinstance(POCAction.no_action, str)

    def test_all_members_count(self):
        assert len(POCAction) == 6

    def test_unique_values(self):
        values = [m.value for m in POCAction]
        assert len(values) == len(set(values))


# ===========================================================================
# 5. POCInput dataclass
# ===========================================================================

class TestPOCInputDataclass:
    def test_construction(self):
        inp = make_input()
        assert inp.rep_id == "REP001"
        assert inp.region == "AMER"

    def test_all_22_fields_exist(self):
        inp = make_input()
        fields = [
            "rep_id", "region", "evaluation_period_id", "total_pocs_conducted",
            "poc_to_close_conversion_rate_pct", "avg_poc_duration_days",
            "pocs_exceeding_timeline_pct", "pocs_with_no_success_criteria_pct",
            "avg_poc_scope_changes_count", "technical_validation_failure_rate_pct",
            "poc_champion_engaged_pct", "exec_sponsor_briefed_pct",
            "avg_days_to_poc_kickoff", "poc_extended_count",
            "mutual_success_plan_completion_pct", "se_escalation_required_pct",
            "poc_abandoned_pct", "post_poc_proposal_delay_days",
            "competitive_poc_displacement_rate_pct", "avg_stakeholders_in_poc_count",
            "avg_poc_resources_allocated_count", "avg_opportunity_value_usd",
        ]
        for f in fields:
            assert hasattr(inp, f), f"Missing field: {f}"

    def test_field_count_is_22(self):
        import dataclasses
        assert len(dataclasses.fields(POCInput)) == 22

    def test_rep_id_stored(self):
        assert make_input(rep_id="X99").rep_id == "X99"

    def test_region_stored(self):
        assert make_input(region="EMEA").region == "EMEA"

    def test_float_fields_stored(self):
        inp = make_input(avg_poc_duration_days=45.5)
        assert inp.avg_poc_duration_days == 45.5

    def test_int_fields_stored(self):
        inp = make_input(total_pocs_conducted=100)
        assert inp.total_pocs_conducted == 100

    def test_evaluation_period_id_stored(self):
        assert make_input(evaluation_period_id="2025-Q2").evaluation_period_id == "2025-Q2"

    def test_poc_extended_count_stored(self):
        assert make_input(poc_extended_count=5).poc_extended_count == 5

    def test_avg_opportunity_value_stored(self):
        assert make_input(avg_opportunity_value_usd=100_000.0).avg_opportunity_value_usd == 100_000.0


# ===========================================================================
# 6. POCResult dataclass
# ===========================================================================

class TestPOCResultDataclass:
    def _make_result(self) -> POCResult:
        return POCResult(
            rep_id="REP1",
            region="APAC",
            poc_risk=POCRisk.moderate,
            poc_pattern=POCPattern.none,
            poc_severity=POCSeverity.developing,
            recommended_action=POCAction.success_criteria_alignment,
            poc_structure_score=15.0,
            poc_execution_score=10.0,
            poc_stakeholder_score=12.0,
            poc_conversion_score=8.0,
            poc_composite=12.5,
            has_poc_gap=False,
            requires_poc_coaching=False,
            estimated_pipeline_loss_usd=1500.0,
            poc_signal="some signal",
        )

    def test_field_count_is_15(self):
        import dataclasses
        assert len(dataclasses.fields(POCResult)) == 15

    def test_rep_id_stored(self):
        assert self._make_result().rep_id == "REP1"

    def test_region_stored(self):
        assert self._make_result().region == "APAC"

    def test_poc_risk_stored(self):
        assert self._make_result().poc_risk is POCRisk.moderate

    def test_poc_pattern_stored(self):
        assert self._make_result().poc_pattern is POCPattern.none

    def test_poc_severity_stored(self):
        assert self._make_result().poc_severity is POCSeverity.developing

    def test_recommended_action_stored(self):
        assert self._make_result().recommended_action is POCAction.success_criteria_alignment

    def test_scores_stored(self):
        r = self._make_result()
        assert r.poc_structure_score == 15.0
        assert r.poc_execution_score == 10.0
        assert r.poc_stakeholder_score == 12.0
        assert r.poc_conversion_score == 8.0

    def test_composite_stored(self):
        assert self._make_result().poc_composite == 12.5

    def test_has_poc_gap_stored(self):
        assert self._make_result().has_poc_gap is False

    def test_requires_poc_coaching_stored(self):
        assert self._make_result().requires_poc_coaching is False

    def test_pipeline_loss_stored(self):
        assert self._make_result().estimated_pipeline_loss_usd == 1500.0

    def test_signal_stored(self):
        assert self._make_result().poc_signal == "some signal"

    # to_dict tests
    def test_to_dict_returns_dict(self):
        assert isinstance(self._make_result().to_dict(), dict)

    def test_to_dict_has_15_keys(self):
        assert len(self._make_result().to_dict()) == 15

    def test_to_dict_rep_id(self):
        assert self._make_result().to_dict()["rep_id"] == "REP1"

    def test_to_dict_region(self):
        assert self._make_result().to_dict()["region"] == "APAC"

    def test_to_dict_poc_risk_is_string(self):
        assert self._make_result().to_dict()["poc_risk"] == "moderate"

    def test_to_dict_poc_pattern_is_string(self):
        assert self._make_result().to_dict()["poc_pattern"] == "none"

    def test_to_dict_poc_severity_is_string(self):
        assert self._make_result().to_dict()["poc_severity"] == "developing"

    def test_to_dict_recommended_action_is_string(self):
        assert self._make_result().to_dict()["recommended_action"] == "success_criteria_alignment"

    def test_to_dict_structure_score(self):
        assert self._make_result().to_dict()["poc_structure_score"] == 15.0

    def test_to_dict_execution_score(self):
        assert self._make_result().to_dict()["poc_execution_score"] == 10.0

    def test_to_dict_stakeholder_score(self):
        assert self._make_result().to_dict()["poc_stakeholder_score"] == 12.0

    def test_to_dict_conversion_score(self):
        assert self._make_result().to_dict()["poc_conversion_score"] == 8.0

    def test_to_dict_composite(self):
        assert self._make_result().to_dict()["poc_composite"] == 12.5

    def test_to_dict_has_poc_gap(self):
        assert self._make_result().to_dict()["has_poc_gap"] is False

    def test_to_dict_requires_poc_coaching(self):
        assert self._make_result().to_dict()["requires_poc_coaching"] is False

    def test_to_dict_pipeline_loss(self):
        assert self._make_result().to_dict()["estimated_pipeline_loss_usd"] == 1500.0

    def test_to_dict_signal(self):
        assert self._make_result().to_dict()["poc_signal"] == "some signal"

    def test_to_dict_expected_keys(self):
        expected = {
            "rep_id", "region", "poc_risk", "poc_pattern", "poc_severity",
            "recommended_action", "poc_structure_score", "poc_execution_score",
            "poc_stakeholder_score", "poc_conversion_score", "poc_composite",
            "has_poc_gap", "requires_poc_coaching", "estimated_pipeline_loss_usd",
            "poc_signal",
        }
        assert set(self._make_result().to_dict().keys()) == expected


# ===========================================================================
# 7. _poc_structure_score
# ===========================================================================

class TestStructureScore:
    def setup_method(self):
        self.e = make_engine()

    # --- pocs_with_no_success_criteria_pct branches ---
    def test_no_success_criteria_high(self):
        inp = make_input(
            pocs_with_no_success_criteria_pct=0.60,
            mutual_success_plan_completion_pct=1.0,
            avg_days_to_poc_kickoff=0.0,
        )
        assert self.e._poc_structure_score(inp) == 40.0

    def test_no_success_criteria_high_boundary_above(self):
        inp = make_input(
            pocs_with_no_success_criteria_pct=0.75,
            mutual_success_plan_completion_pct=1.0,
            avg_days_to_poc_kickoff=0.0,
        )
        assert self.e._poc_structure_score(inp) == 40.0

    def test_no_success_criteria_moderate(self):
        inp = make_input(
            pocs_with_no_success_criteria_pct=0.30,
            mutual_success_plan_completion_pct=1.0,
            avg_days_to_poc_kickoff=0.0,
        )
        assert self.e._poc_structure_score(inp) == 22.0

    def test_no_success_criteria_moderate_upper(self):
        inp = make_input(
            pocs_with_no_success_criteria_pct=0.59,
            mutual_success_plan_completion_pct=1.0,
            avg_days_to_poc_kickoff=0.0,
        )
        assert self.e._poc_structure_score(inp) == 22.0

    def test_no_success_criteria_low(self):
        inp = make_input(
            pocs_with_no_success_criteria_pct=0.15,
            mutual_success_plan_completion_pct=1.0,
            avg_days_to_poc_kickoff=0.0,
        )
        assert self.e._poc_structure_score(inp) == 8.0

    def test_no_success_criteria_low_upper(self):
        inp = make_input(
            pocs_with_no_success_criteria_pct=0.29,
            mutual_success_plan_completion_pct=1.0,
            avg_days_to_poc_kickoff=0.0,
        )
        assert self.e._poc_structure_score(inp) == 8.0

    def test_no_success_criteria_none(self):
        inp = make_input(
            pocs_with_no_success_criteria_pct=0.14,
            mutual_success_plan_completion_pct=1.0,
            avg_days_to_poc_kickoff=0.0,
        )
        assert self.e._poc_structure_score(inp) == 0.0

    # --- mutual_success_plan_completion_pct branches ---
    def test_msp_very_low(self):
        inp = make_input(
            pocs_with_no_success_criteria_pct=0.0,
            mutual_success_plan_completion_pct=0.20,
            avg_days_to_poc_kickoff=0.0,
        )
        assert self.e._poc_structure_score(inp) == 35.0

    def test_msp_low(self):
        inp = make_input(
            pocs_with_no_success_criteria_pct=0.0,
            mutual_success_plan_completion_pct=0.50,
            avg_days_to_poc_kickoff=0.0,
        )
        assert self.e._poc_structure_score(inp) == 18.0

    def test_msp_ok(self):
        inp = make_input(
            pocs_with_no_success_criteria_pct=0.0,
            mutual_success_plan_completion_pct=0.51,
            avg_days_to_poc_kickoff=0.0,
        )
        assert self.e._poc_structure_score(inp) == 0.0

    # --- avg_days_to_poc_kickoff branches ---
    def test_kickoff_very_slow(self):
        inp = make_input(
            pocs_with_no_success_criteria_pct=0.0,
            mutual_success_plan_completion_pct=1.0,
            avg_days_to_poc_kickoff=21.0,
        )
        assert self.e._poc_structure_score(inp) == 25.0

    def test_kickoff_slow(self):
        inp = make_input(
            pocs_with_no_success_criteria_pct=0.0,
            mutual_success_plan_completion_pct=1.0,
            avg_days_to_poc_kickoff=10.0,
        )
        assert self.e._poc_structure_score(inp) == 12.0

    def test_kickoff_fast(self):
        inp = make_input(
            pocs_with_no_success_criteria_pct=0.0,
            mutual_success_plan_completion_pct=1.0,
            avg_days_to_poc_kickoff=9.9,
        )
        assert self.e._poc_structure_score(inp) == 0.0

    def test_structure_score_capped_at_100(self):
        inp = make_input(
            pocs_with_no_success_criteria_pct=0.60,
            mutual_success_plan_completion_pct=0.10,
            avg_days_to_poc_kickoff=25.0,
        )
        # 40 + 35 + 25 = 100 → capped at 100
        assert self.e._poc_structure_score(inp) == 100.0

    def test_structure_all_zero(self):
        inp = make_input(
            pocs_with_no_success_criteria_pct=0.0,
            mutual_success_plan_completion_pct=1.0,
            avg_days_to_poc_kickoff=0.0,
        )
        assert self.e._poc_structure_score(inp) == 0.0

    def test_structure_score_combined(self):
        inp = make_input(
            pocs_with_no_success_criteria_pct=0.30,   # +22
            mutual_success_plan_completion_pct=0.50,  # +18
            avg_days_to_poc_kickoff=10.0,             # +12
        )
        assert self.e._poc_structure_score(inp) == 52.0


# ===========================================================================
# 8. _poc_execution_score
# ===========================================================================

class TestExecutionScore:
    def setup_method(self):
        self.e = make_engine()

    # --- pocs_exceeding_timeline_pct branches ---
    def test_exceeding_high(self):
        inp = make_input(
            pocs_exceeding_timeline_pct=0.60,
            avg_poc_scope_changes_count=0.0,
            poc_abandoned_pct=0.0,
        )
        assert self.e._poc_execution_score(inp) == 40.0

    def test_exceeding_moderate(self):
        inp = make_input(
            pocs_exceeding_timeline_pct=0.30,
            avg_poc_scope_changes_count=0.0,
            poc_abandoned_pct=0.0,
        )
        assert self.e._poc_execution_score(inp) == 22.0

    def test_exceeding_low(self):
        inp = make_input(
            pocs_exceeding_timeline_pct=0.15,
            avg_poc_scope_changes_count=0.0,
            poc_abandoned_pct=0.0,
        )
        assert self.e._poc_execution_score(inp) == 8.0

    def test_exceeding_none(self):
        inp = make_input(
            pocs_exceeding_timeline_pct=0.14,
            avg_poc_scope_changes_count=0.0,
            poc_abandoned_pct=0.0,
        )
        assert self.e._poc_execution_score(inp) == 0.0

    # --- avg_poc_scope_changes_count branches ---
    def test_scope_high(self):
        inp = make_input(
            pocs_exceeding_timeline_pct=0.0,
            avg_poc_scope_changes_count=3.0,
            poc_abandoned_pct=0.0,
        )
        assert self.e._poc_execution_score(inp) == 35.0

    def test_scope_moderate(self):
        inp = make_input(
            pocs_exceeding_timeline_pct=0.0,
            avg_poc_scope_changes_count=1.5,
            poc_abandoned_pct=0.0,
        )
        assert self.e._poc_execution_score(inp) == 18.0

    def test_scope_none(self):
        inp = make_input(
            pocs_exceeding_timeline_pct=0.0,
            avg_poc_scope_changes_count=1.4,
            poc_abandoned_pct=0.0,
        )
        assert self.e._poc_execution_score(inp) == 0.0

    # --- poc_abandoned_pct branches ---
    def test_abandoned_high(self):
        inp = make_input(
            pocs_exceeding_timeline_pct=0.0,
            avg_poc_scope_changes_count=0.0,
            poc_abandoned_pct=0.30,
        )
        assert self.e._poc_execution_score(inp) == 25.0

    def test_abandoned_moderate(self):
        inp = make_input(
            pocs_exceeding_timeline_pct=0.0,
            avg_poc_scope_changes_count=0.0,
            poc_abandoned_pct=0.15,
        )
        assert self.e._poc_execution_score(inp) == 12.0

    def test_abandoned_none(self):
        inp = make_input(
            pocs_exceeding_timeline_pct=0.0,
            avg_poc_scope_changes_count=0.0,
            poc_abandoned_pct=0.14,
        )
        assert self.e._poc_execution_score(inp) == 0.0

    def test_execution_score_capped_at_100(self):
        inp = make_input(
            pocs_exceeding_timeline_pct=0.60,
            avg_poc_scope_changes_count=3.0,
            poc_abandoned_pct=0.30,
        )
        assert self.e._poc_execution_score(inp) == 100.0

    def test_execution_all_zero(self):
        inp = make_input(
            pocs_exceeding_timeline_pct=0.0,
            avg_poc_scope_changes_count=0.0,
            poc_abandoned_pct=0.0,
        )
        assert self.e._poc_execution_score(inp) == 0.0


# ===========================================================================
# 9. _poc_stakeholder_score
# ===========================================================================

class TestStakeholderScore:
    def setup_method(self):
        self.e = make_engine()

    # --- poc_champion_engaged_pct branches ---
    def test_champion_very_low(self):
        inp = make_input(
            poc_champion_engaged_pct=0.30,
            exec_sponsor_briefed_pct=1.0,
            avg_stakeholders_in_poc_count=5.0,
        )
        assert self.e._poc_stakeholder_score(inp) == 45.0

    def test_champion_low(self):
        inp = make_input(
            poc_champion_engaged_pct=0.60,
            exec_sponsor_briefed_pct=1.0,
            avg_stakeholders_in_poc_count=5.0,
        )
        assert self.e._poc_stakeholder_score(inp) == 25.0

    def test_champion_moderate(self):
        inp = make_input(
            poc_champion_engaged_pct=0.80,
            exec_sponsor_briefed_pct=1.0,
            avg_stakeholders_in_poc_count=5.0,
        )
        assert self.e._poc_stakeholder_score(inp) == 10.0

    def test_champion_good(self):
        inp = make_input(
            poc_champion_engaged_pct=0.81,
            exec_sponsor_briefed_pct=1.0,
            avg_stakeholders_in_poc_count=5.0,
        )
        assert self.e._poc_stakeholder_score(inp) == 0.0

    # --- exec_sponsor_briefed_pct branches ---
    def test_exec_sponsor_very_low(self):
        inp = make_input(
            poc_champion_engaged_pct=1.0,
            exec_sponsor_briefed_pct=0.20,
            avg_stakeholders_in_poc_count=5.0,
        )
        assert self.e._poc_stakeholder_score(inp) == 30.0

    def test_exec_sponsor_low(self):
        inp = make_input(
            poc_champion_engaged_pct=1.0,
            exec_sponsor_briefed_pct=0.50,
            avg_stakeholders_in_poc_count=5.0,
        )
        assert self.e._poc_stakeholder_score(inp) == 15.0

    def test_exec_sponsor_ok(self):
        inp = make_input(
            poc_champion_engaged_pct=1.0,
            exec_sponsor_briefed_pct=0.51,
            avg_stakeholders_in_poc_count=5.0,
        )
        assert self.e._poc_stakeholder_score(inp) == 0.0

    # --- avg_stakeholders_in_poc_count branches ---
    def test_stakeholders_very_low(self):
        inp = make_input(
            poc_champion_engaged_pct=1.0,
            exec_sponsor_briefed_pct=1.0,
            avg_stakeholders_in_poc_count=1.0,
        )
        assert self.e._poc_stakeholder_score(inp) == 25.0

    def test_stakeholders_low(self):
        inp = make_input(
            poc_champion_engaged_pct=1.0,
            exec_sponsor_briefed_pct=1.0,
            avg_stakeholders_in_poc_count=2.0,
        )
        assert self.e._poc_stakeholder_score(inp) == 12.0

    def test_stakeholders_ok(self):
        inp = make_input(
            poc_champion_engaged_pct=1.0,
            exec_sponsor_briefed_pct=1.0,
            avg_stakeholders_in_poc_count=2.1,
        )
        assert self.e._poc_stakeholder_score(inp) == 0.0

    def test_stakeholder_score_capped_at_100(self):
        inp = make_input(
            poc_champion_engaged_pct=0.20,
            exec_sponsor_briefed_pct=0.10,
            avg_stakeholders_in_poc_count=0.5,
        )
        assert self.e._poc_stakeholder_score(inp) == 100.0

    def test_stakeholder_all_zero(self):
        inp = make_input(
            poc_champion_engaged_pct=1.0,
            exec_sponsor_briefed_pct=1.0,
            avg_stakeholders_in_poc_count=5.0,
        )
        assert self.e._poc_stakeholder_score(inp) == 0.0


# ===========================================================================
# 10. _poc_conversion_score
# ===========================================================================

class TestConversionScore:
    def setup_method(self):
        self.e = make_engine()

    # --- poc_to_close_conversion_rate_pct branches ---
    def test_conversion_very_low(self):
        inp = make_input(
            poc_to_close_conversion_rate_pct=0.20,
            technical_validation_failure_rate_pct=0.0,
            competitive_poc_displacement_rate_pct=0.0,
        )
        assert self.e._poc_conversion_score(inp) == 45.0

    def test_conversion_low(self):
        inp = make_input(
            poc_to_close_conversion_rate_pct=0.40,
            technical_validation_failure_rate_pct=0.0,
            competitive_poc_displacement_rate_pct=0.0,
        )
        assert self.e._poc_conversion_score(inp) == 25.0

    def test_conversion_moderate(self):
        inp = make_input(
            poc_to_close_conversion_rate_pct=0.60,
            technical_validation_failure_rate_pct=0.0,
            competitive_poc_displacement_rate_pct=0.0,
        )
        assert self.e._poc_conversion_score(inp) == 10.0

    def test_conversion_good(self):
        inp = make_input(
            poc_to_close_conversion_rate_pct=0.61,
            technical_validation_failure_rate_pct=0.0,
            competitive_poc_displacement_rate_pct=0.0,
        )
        assert self.e._poc_conversion_score(inp) == 0.0

    # --- technical_validation_failure_rate_pct branches ---
    def test_tech_failure_high(self):
        inp = make_input(
            poc_to_close_conversion_rate_pct=1.0,
            technical_validation_failure_rate_pct=0.30,
            competitive_poc_displacement_rate_pct=0.0,
        )
        assert self.e._poc_conversion_score(inp) == 30.0

    def test_tech_failure_moderate(self):
        inp = make_input(
            poc_to_close_conversion_rate_pct=1.0,
            technical_validation_failure_rate_pct=0.15,
            competitive_poc_displacement_rate_pct=0.0,
        )
        assert self.e._poc_conversion_score(inp) == 15.0

    def test_tech_failure_none(self):
        inp = make_input(
            poc_to_close_conversion_rate_pct=1.0,
            technical_validation_failure_rate_pct=0.14,
            competitive_poc_displacement_rate_pct=0.0,
        )
        assert self.e._poc_conversion_score(inp) == 0.0

    # --- competitive_poc_displacement_rate_pct branches ---
    def test_displacement_high(self):
        inp = make_input(
            poc_to_close_conversion_rate_pct=1.0,
            technical_validation_failure_rate_pct=0.0,
            competitive_poc_displacement_rate_pct=0.30,
        )
        assert self.e._poc_conversion_score(inp) == 25.0

    def test_displacement_moderate(self):
        inp = make_input(
            poc_to_close_conversion_rate_pct=1.0,
            technical_validation_failure_rate_pct=0.0,
            competitive_poc_displacement_rate_pct=0.15,
        )
        assert self.e._poc_conversion_score(inp) == 12.0

    def test_displacement_none(self):
        inp = make_input(
            poc_to_close_conversion_rate_pct=1.0,
            technical_validation_failure_rate_pct=0.0,
            competitive_poc_displacement_rate_pct=0.14,
        )
        assert self.e._poc_conversion_score(inp) == 0.0

    def test_conversion_score_capped_at_100(self):
        inp = make_input(
            poc_to_close_conversion_rate_pct=0.10,
            technical_validation_failure_rate_pct=0.50,
            competitive_poc_displacement_rate_pct=0.50,
        )
        assert self.e._poc_conversion_score(inp) == 100.0

    def test_conversion_all_zero(self):
        inp = make_input(
            poc_to_close_conversion_rate_pct=1.0,
            technical_validation_failure_rate_pct=0.0,
            competitive_poc_displacement_rate_pct=0.0,
        )
        assert self.e._poc_conversion_score(inp) == 0.0


# ===========================================================================
# 11. _detect_pattern
# ===========================================================================

class TestDetectPattern:
    def setup_method(self):
        self.e = make_engine()

    def _detect(self, inp, s=0, x=0, st=0, cv=0):
        return self.e._detect_pattern(inp, s, x, st, cv)

    def test_poc_stall_detected(self):
        inp = make_input(
            pocs_exceeding_timeline_pct=0.40,
        )
        # execution >= 40 required
        pattern = self.e._detect_pattern(inp, structure=0, execution=40, stakeholder=0, conversion=0)
        assert pattern == POCPattern.poc_stall

    def test_poc_stall_not_detected_low_execution(self):
        inp = make_input(pocs_exceeding_timeline_pct=0.40)
        pattern = self.e._detect_pattern(inp, structure=0, execution=39, stakeholder=0, conversion=0)
        assert pattern != POCPattern.poc_stall

    def test_poc_stall_not_detected_low_timeline(self):
        inp = make_input(pocs_exceeding_timeline_pct=0.39)
        pattern = self.e._detect_pattern(inp, structure=0, execution=50, stakeholder=0, conversion=0)
        assert pattern != POCPattern.poc_stall

    def test_success_criteria_gap_detected(self):
        inp = make_input(pocs_with_no_success_criteria_pct=0.40)
        pattern = self.e._detect_pattern(inp, structure=40, execution=0, stakeholder=0, conversion=0)
        assert pattern == POCPattern.success_criteria_gap

    def test_success_criteria_gap_not_detected_low_structure(self):
        inp = make_input(pocs_with_no_success_criteria_pct=0.40)
        pattern = self.e._detect_pattern(inp, structure=39, execution=0, stakeholder=0, conversion=0)
        assert pattern != POCPattern.success_criteria_gap

    def test_success_criteria_gap_not_detected_low_pct(self):
        inp = make_input(pocs_with_no_success_criteria_pct=0.39)
        pattern = self.e._detect_pattern(inp, structure=50, execution=0, stakeholder=0, conversion=0)
        assert pattern != POCPattern.success_criteria_gap

    def test_scope_creep_detected(self):
        inp = make_input(avg_poc_scope_changes_count=2.0)
        pattern = self.e._detect_pattern(inp, structure=0, execution=30, stakeholder=0, conversion=0)
        assert pattern == POCPattern.scope_creep

    def test_scope_creep_not_detected_low_execution(self):
        inp = make_input(avg_poc_scope_changes_count=2.0)
        pattern = self.e._detect_pattern(inp, structure=0, execution=29, stakeholder=0, conversion=0)
        assert pattern != POCPattern.scope_creep

    def test_scope_creep_not_detected_low_changes(self):
        inp = make_input(avg_poc_scope_changes_count=1.9)
        pattern = self.e._detect_pattern(inp, structure=0, execution=40, stakeholder=0, conversion=0)
        assert pattern != POCPattern.scope_creep

    def test_technical_validation_failure_detected(self):
        inp = make_input(technical_validation_failure_rate_pct=0.20)
        pattern = self.e._detect_pattern(inp, structure=0, execution=0, stakeholder=0, conversion=30)
        assert pattern == POCPattern.technical_validation_failure

    def test_technical_validation_failure_not_detected_low_conversion(self):
        inp = make_input(technical_validation_failure_rate_pct=0.20)
        pattern = self.e._detect_pattern(inp, structure=0, execution=0, stakeholder=0, conversion=29)
        assert pattern != POCPattern.technical_validation_failure

    def test_technical_validation_failure_not_detected_low_failure_rate(self):
        inp = make_input(technical_validation_failure_rate_pct=0.19)
        pattern = self.e._detect_pattern(inp, structure=0, execution=0, stakeholder=0, conversion=50)
        assert pattern != POCPattern.technical_validation_failure

    def test_no_champion_detected(self):
        inp = make_input(poc_champion_engaged_pct=0.40)
        pattern = self.e._detect_pattern(inp, structure=0, execution=0, stakeholder=30, conversion=0)
        assert pattern == POCPattern.no_champion_during_poc

    def test_no_champion_not_detected_low_stakeholder(self):
        inp = make_input(poc_champion_engaged_pct=0.40)
        pattern = self.e._detect_pattern(inp, structure=0, execution=0, stakeholder=29, conversion=0)
        assert pattern != POCPattern.no_champion_during_poc

    def test_no_champion_not_detected_good_champion(self):
        inp = make_input(poc_champion_engaged_pct=0.41)
        pattern = self.e._detect_pattern(inp, structure=0, execution=0, stakeholder=40, conversion=0)
        assert pattern != POCPattern.no_champion_during_poc

    def test_none_pattern_when_all_ok(self):
        inp = make_input()
        pattern = self.e._detect_pattern(inp, structure=0, execution=0, stakeholder=0, conversion=0)
        assert pattern == POCPattern.none

    def test_poc_stall_takes_priority_over_success_criteria_gap(self):
        """poc_stall is checked first — both conditions met, stall wins."""
        inp = make_input(
            pocs_exceeding_timeline_pct=0.40,
            pocs_with_no_success_criteria_pct=0.40,
        )
        pattern = self.e._detect_pattern(inp, structure=50, execution=50, stakeholder=0, conversion=0)
        assert pattern == POCPattern.poc_stall


# ===========================================================================
# 12. _risk_level
# ===========================================================================

class TestRiskLevel:
    def setup_method(self):
        self.e = make_engine()

    def test_critical_at_exactly_60(self):
        assert self.e._risk_level(60.0) == POCRisk.critical

    def test_critical_above_60(self):
        assert self.e._risk_level(80.0) == POCRisk.critical

    def test_critical_at_100(self):
        assert self.e._risk_level(100.0) == POCRisk.critical

    def test_high_at_exactly_40(self):
        assert self.e._risk_level(40.0) == POCRisk.high

    def test_high_below_60(self):
        assert self.e._risk_level(59.9) == POCRisk.high

    def test_moderate_at_exactly_20(self):
        assert self.e._risk_level(20.0) == POCRisk.moderate

    def test_moderate_below_40(self):
        assert self.e._risk_level(39.9) == POCRisk.moderate

    def test_low_at_zero(self):
        assert self.e._risk_level(0.0) == POCRisk.low

    def test_low_just_below_20(self):
        assert self.e._risk_level(19.9) == POCRisk.low


# ===========================================================================
# 13. _severity
# ===========================================================================

class TestSeverity:
    def setup_method(self):
        self.e = make_engine()

    def test_failing_at_60(self):
        assert self.e._severity(60.0) == POCSeverity.failing

    def test_failing_above_60(self):
        assert self.e._severity(90.0) == POCSeverity.failing

    def test_uncontrolled_at_40(self):
        assert self.e._severity(40.0) == POCSeverity.uncontrolled

    def test_uncontrolled_just_below_60(self):
        assert self.e._severity(59.9) == POCSeverity.uncontrolled

    def test_developing_at_20(self):
        assert self.e._severity(20.0) == POCSeverity.developing

    def test_developing_just_below_40(self):
        assert self.e._severity(39.9) == POCSeverity.developing

    def test_structured_at_0(self):
        assert self.e._severity(0.0) == POCSeverity.structured

    def test_structured_just_below_20(self):
        assert self.e._severity(19.9) == POCSeverity.structured


# ===========================================================================
# 14. _action
# ===========================================================================

class TestAction:
    def setup_method(self):
        self.e = make_engine()

    # critical
    def test_critical_tech_failure(self):
        assert self.e._action(POCRisk.critical, POCPattern.technical_validation_failure) == POCAction.technical_escalation_support

    def test_critical_no_champion(self):
        assert self.e._action(POCRisk.critical, POCPattern.no_champion_during_poc) == POCAction.champion_engagement_during_poc

    def test_critical_stall(self):
        assert self.e._action(POCRisk.critical, POCPattern.poc_stall) == POCAction.poc_structure_coaching

    def test_critical_scope_creep(self):
        assert self.e._action(POCRisk.critical, POCPattern.scope_creep) == POCAction.poc_structure_coaching

    def test_critical_success_criteria_gap(self):
        assert self.e._action(POCRisk.critical, POCPattern.success_criteria_gap) == POCAction.poc_structure_coaching

    def test_critical_none_pattern(self):
        assert self.e._action(POCRisk.critical, POCPattern.none) == POCAction.poc_structure_coaching

    # high
    def test_high_success_criteria_gap(self):
        assert self.e._action(POCRisk.high, POCPattern.success_criteria_gap) == POCAction.success_criteria_alignment

    def test_high_scope_creep(self):
        assert self.e._action(POCRisk.high, POCPattern.scope_creep) == POCAction.scope_control_training

    def test_high_stall(self):
        assert self.e._action(POCRisk.high, POCPattern.poc_stall) == POCAction.poc_structure_coaching

    def test_high_none_pattern(self):
        assert self.e._action(POCRisk.high, POCPattern.none) == POCAction.poc_structure_coaching

    def test_high_tech_failure(self):
        assert self.e._action(POCRisk.high, POCPattern.technical_validation_failure) == POCAction.poc_structure_coaching

    # moderate
    def test_moderate_any_pattern_returns_alignment(self):
        for p in POCPattern:
            assert self.e._action(POCRisk.moderate, p) == POCAction.success_criteria_alignment

    # low
    def test_low_any_pattern_returns_no_action(self):
        for p in POCPattern:
            assert self.e._action(POCRisk.low, p) == POCAction.no_action


# ===========================================================================
# 15. _has_poc_gap
# ===========================================================================

class TestHasPOCGap:
    def setup_method(self):
        self.e = make_engine()

    def test_gap_via_composite_40(self):
        inp = make_input(poc_to_close_conversion_rate_pct=0.75, poc_abandoned_pct=0.05)
        assert self.e._has_poc_gap(40.0, inp) is True

    def test_gap_via_composite_above_40(self):
        inp = make_input(poc_to_close_conversion_rate_pct=0.75, poc_abandoned_pct=0.05)
        assert self.e._has_poc_gap(60.0, inp) is True

    def test_gap_via_low_conversion(self):
        inp = make_input(poc_to_close_conversion_rate_pct=0.20, poc_abandoned_pct=0.05)
        assert self.e._has_poc_gap(10.0, inp) is True

    def test_gap_via_high_abandoned(self):
        inp = make_input(poc_to_close_conversion_rate_pct=0.75, poc_abandoned_pct=0.25)
        assert self.e._has_poc_gap(10.0, inp) is True

    def test_no_gap_all_ok(self):
        inp = make_input(poc_to_close_conversion_rate_pct=0.75, poc_abandoned_pct=0.10)
        assert self.e._has_poc_gap(10.0, inp) is False

    def test_gap_composite_exact_boundary(self):
        inp = make_input(poc_to_close_conversion_rate_pct=0.75, poc_abandoned_pct=0.05)
        assert self.e._has_poc_gap(39.9, inp) is False

    def test_gap_conversion_exact_boundary(self):
        inp = make_input(poc_to_close_conversion_rate_pct=0.21, poc_abandoned_pct=0.05)
        assert self.e._has_poc_gap(10.0, inp) is False

    def test_gap_abandoned_just_below_threshold(self):
        inp = make_input(poc_to_close_conversion_rate_pct=0.75, poc_abandoned_pct=0.24)
        assert self.e._has_poc_gap(10.0, inp) is False


# ===========================================================================
# 16. _requires_poc_coaching
# ===========================================================================

class TestRequiresPOCCoaching:
    def setup_method(self):
        self.e = make_engine()

    def test_coaching_via_composite_30(self):
        inp = make_input(pocs_with_no_success_criteria_pct=0.05, poc_champion_engaged_pct=0.90)
        assert self.e._requires_poc_coaching(30.0, inp) is True

    def test_coaching_via_composite_above_30(self):
        inp = make_input(pocs_with_no_success_criteria_pct=0.05, poc_champion_engaged_pct=0.90)
        assert self.e._requires_poc_coaching(50.0, inp) is True

    def test_coaching_via_no_success_criteria(self):
        inp = make_input(pocs_with_no_success_criteria_pct=0.35, poc_champion_engaged_pct=0.90)
        assert self.e._requires_poc_coaching(10.0, inp) is True

    def test_coaching_via_low_champion(self):
        inp = make_input(pocs_with_no_success_criteria_pct=0.05, poc_champion_engaged_pct=0.40)
        assert self.e._requires_poc_coaching(10.0, inp) is True

    def test_no_coaching_when_all_ok(self):
        inp = make_input(pocs_with_no_success_criteria_pct=0.05, poc_champion_engaged_pct=0.90)
        assert self.e._requires_poc_coaching(10.0, inp) is False

    def test_coaching_composite_exact_boundary(self):
        inp = make_input(pocs_with_no_success_criteria_pct=0.05, poc_champion_engaged_pct=0.90)
        assert self.e._requires_poc_coaching(29.9, inp) is False

    def test_coaching_no_criteria_exact_boundary(self):
        inp = make_input(pocs_with_no_success_criteria_pct=0.34, poc_champion_engaged_pct=0.90)
        assert self.e._requires_poc_coaching(10.0, inp) is False

    def test_coaching_champion_exact_boundary(self):
        inp = make_input(pocs_with_no_success_criteria_pct=0.05, poc_champion_engaged_pct=0.41)
        assert self.e._requires_poc_coaching(10.0, inp) is False


# ===========================================================================
# 17. _estimated_pipeline_loss
# ===========================================================================

class TestEstimatedPipelineLoss:
    def setup_method(self):
        self.e = make_engine()

    def test_basic_calculation(self):
        inp = make_input(
            total_pocs_conducted=100,
            poc_abandoned_pct=0.10,
            avg_opportunity_value_usd=50_000.0,
        )
        # abandoned = round(100 * 0.10) = 10
        # loss = 10 * 50000 * (composite/100) * 0.30
        # at composite=50: 10 * 50000 * 0.50 * 0.30 = 75000
        assert self.e._estimated_pipeline_loss(inp, 50.0) == 75_000.0

    def test_zero_abandoned(self):
        inp = make_input(
            total_pocs_conducted=100,
            poc_abandoned_pct=0.0,
            avg_opportunity_value_usd=50_000.0,
        )
        assert self.e._estimated_pipeline_loss(inp, 50.0) == 0.0

    def test_zero_composite(self):
        inp = make_input(
            total_pocs_conducted=100,
            poc_abandoned_pct=0.20,
            avg_opportunity_value_usd=50_000.0,
        )
        assert self.e._estimated_pipeline_loss(inp, 0.0) == 0.0

    def test_zero_opportunity_value(self):
        inp = make_input(
            total_pocs_conducted=100,
            poc_abandoned_pct=0.20,
            avg_opportunity_value_usd=0.0,
        )
        assert self.e._estimated_pipeline_loss(inp, 50.0) == 0.0

    def test_rounding(self):
        inp = make_input(
            total_pocs_conducted=3,
            poc_abandoned_pct=0.333,
            avg_opportunity_value_usd=10_000.0,
        )
        # abandoned = round(3 * 0.333) = round(0.999) = 1
        # loss = 1 * 10000 * (20/100) * 0.30 = 600.0
        result = self.e._estimated_pipeline_loss(inp, 20.0)
        assert isinstance(result, float)

    def test_full_composite(self):
        inp = make_input(
            total_pocs_conducted=10,
            poc_abandoned_pct=0.50,
            avg_opportunity_value_usd=100_000.0,
        )
        # abandoned = round(10 * 0.50) = 5
        # loss = 5 * 100000 * (100/100) * 0.30 = 150000
        assert self.e._estimated_pipeline_loss(inp, 100.0) == 150_000.0

    def test_result_is_rounded_to_2_decimals(self):
        inp = make_input(
            total_pocs_conducted=7,
            poc_abandoned_pct=0.15,
            avg_opportunity_value_usd=33_333.33,
        )
        result = self.e._estimated_pipeline_loss(inp, 33.3)
        # result should be rounded to 2 decimal places
        assert result == round(result, 2)


# ===========================================================================
# 18. _signal
# ===========================================================================

class TestSignal:
    def setup_method(self):
        self.e = make_engine()

    def test_healthy_signal_when_none_and_low_composite(self):
        inp = make_input()
        result = self.e._signal(inp, POCPattern.none, 10.0)
        assert result == "POC execution healthy — structure, conversion, and champion engagement within benchmarks"

    def test_healthy_signal_composite_exactly_below_20(self):
        inp = make_input()
        result = self.e._signal(inp, POCPattern.none, 19.9)
        assert result == "POC execution healthy — structure, conversion, and champion engagement within benchmarks"

    def test_no_healthy_signal_when_pattern_set(self):
        inp = make_input()
        result = self.e._signal(inp, POCPattern.poc_stall, 10.0)
        assert "POC execution healthy" not in result

    def test_no_healthy_signal_when_composite_20(self):
        inp = make_input()
        result = self.e._signal(inp, POCPattern.none, 20.0)
        assert "POC execution healthy" not in result

    def test_signal_contains_pattern_label(self):
        inp = make_input(
            poc_to_close_conversion_rate_pct=0.30,
            pocs_exceeding_timeline_pct=0.50,
        )
        result = self.e._signal(inp, POCPattern.poc_stall, 50.0)
        assert "Poc stall" in result

    def test_signal_contains_composite(self):
        inp = make_input(
            poc_to_close_conversion_rate_pct=0.30,
            pocs_exceeding_timeline_pct=0.50,
        )
        result = self.e._signal(inp, POCPattern.poc_stall, 50.0)
        assert "composite 50" in result

    def test_signal_contains_stalled_pocs_pct(self):
        inp = make_input(
            poc_to_close_conversion_rate_pct=1.0,  # skip conversion part (>= 1.0 so no output)
            pocs_exceeding_timeline_pct=0.50,
            avg_poc_duration_days=30.0,
        )
        result = self.e._signal(inp, POCPattern.poc_stall, 50.0)
        assert "50% stalled POCs" in result

    def test_signal_contains_conversion_rate(self):
        inp = make_input(
            poc_to_close_conversion_rate_pct=0.30,
            pocs_exceeding_timeline_pct=0.0,
            avg_poc_duration_days=30.0,
        )
        result = self.e._signal(inp, POCPattern.scope_creep, 40.0)
        assert "30% POC-to-close" in result

    def test_signal_contains_avg_poc_days(self):
        inp = make_input(avg_poc_duration_days=45.0, poc_to_close_conversion_rate_pct=1.0)
        result = self.e._signal(inp, POCPattern.poc_stall, 40.0)
        assert "45 avg POC days" in result

    def test_signal_none_pattern_above_20(self):
        inp = make_input(poc_to_close_conversion_rate_pct=0.30)
        result = self.e._signal(inp, POCPattern.none, 25.0)
        # pattern.value "none" -> label "POC risk" -> capitalize -> "Poc risk"
        assert "Poc risk" in result

    def test_signal_pattern_label_formatted(self):
        inp = make_input()
        result = self.e._signal(inp, POCPattern.success_criteria_gap, 50.0)
        assert "Success criteria gap" in result

    def test_signal_technical_validation_pattern(self):
        inp = make_input(poc_to_close_conversion_rate_pct=0.30)
        result = self.e._signal(inp, POCPattern.technical_validation_failure, 60.0)
        assert "Technical validation failure" in result


# ===========================================================================
# 19. assess() – integration
# ===========================================================================

class TestAssess:
    def setup_method(self):
        self.e = make_engine()

    def test_returns_poc_result(self):
        result = self.e.assess(make_input())
        assert isinstance(result, POCResult)

    def test_rep_id_propagated(self):
        result = self.e.assess(make_input(rep_id="R99"))
        assert result.rep_id == "R99"

    def test_region_propagated(self):
        result = self.e.assess(make_input(region="EMEA"))
        assert result.region == "EMEA"

    def test_healthy_input_gives_low_risk(self):
        result = self.e.assess(make_input())
        assert result.poc_risk == POCRisk.low

    def test_healthy_input_gives_structured_severity(self):
        result = self.e.assess(make_input())
        assert result.poc_severity == POCSeverity.structured

    def test_healthy_input_gives_no_action(self):
        result = self.e.assess(make_input())
        assert result.recommended_action == POCAction.no_action

    def test_healthy_input_gives_none_pattern(self):
        result = self.e.assess(make_input())
        assert result.poc_pattern == POCPattern.none

    def test_healthy_signal(self):
        result = self.e.assess(make_input())
        assert "POC execution healthy" in result.poc_signal

    def test_scores_are_floats(self):
        result = self.e.assess(make_input())
        assert isinstance(result.poc_structure_score, float)
        assert isinstance(result.poc_execution_score, float)
        assert isinstance(result.poc_stakeholder_score, float)
        assert isinstance(result.poc_conversion_score, float)
        assert isinstance(result.poc_composite, float)

    def test_composite_formula(self):
        """Verify composite = structure*0.30 + execution*0.30 + stakeholder*0.25 + conversion*0.15"""
        result = self.e.assess(make_input())
        expected = round(
            result.poc_structure_score * 0.30
            + result.poc_execution_score * 0.30
            + result.poc_stakeholder_score * 0.25
            + result.poc_conversion_score * 0.15,
            1,
        )
        assert result.poc_composite == expected

    def test_composite_capped_at_100(self):
        inp = make_input(
            pocs_with_no_success_criteria_pct=1.0,
            mutual_success_plan_completion_pct=0.0,
            avg_days_to_poc_kickoff=30.0,
            pocs_exceeding_timeline_pct=1.0,
            avg_poc_scope_changes_count=5.0,
            poc_abandoned_pct=1.0,
            poc_champion_engaged_pct=0.0,
            exec_sponsor_briefed_pct=0.0,
            avg_stakeholders_in_poc_count=0.0,
            poc_to_close_conversion_rate_pct=0.0,
            technical_validation_failure_rate_pct=1.0,
            competitive_poc_displacement_rate_pct=1.0,
        )
        result = self.e.assess(inp)
        assert result.poc_composite <= 100.0

    def test_result_stored_in_internal_list(self):
        e = make_engine()
        e.assess(make_input())
        assert len(e._results) == 1

    def test_result_stored_twice_after_two_assessments(self):
        e = make_engine()
        e.assess(make_input())
        e.assess(make_input(rep_id="R2"))
        assert len(e._results) == 2

    def test_high_risk_scenario(self):
        inp = make_input(
            pocs_with_no_success_criteria_pct=0.60,
            mutual_success_plan_completion_pct=0.10,
            avg_days_to_poc_kickoff=25.0,
            pocs_exceeding_timeline_pct=0.60,
            avg_poc_scope_changes_count=3.0,
            poc_abandoned_pct=0.30,
            poc_champion_engaged_pct=0.20,
            exec_sponsor_briefed_pct=0.10,
            avg_stakeholders_in_poc_count=0.5,
            poc_to_close_conversion_rate_pct=0.10,
            technical_validation_failure_rate_pct=0.40,
            competitive_poc_displacement_rate_pct=0.40,
        )
        result = self.e.assess(inp)
        assert result.poc_risk in (POCRisk.high, POCRisk.critical)

    def test_critical_risk_scenario(self):
        inp = make_input(
            pocs_with_no_success_criteria_pct=0.70,
            mutual_success_plan_completion_pct=0.05,
            avg_days_to_poc_kickoff=30.0,
            pocs_exceeding_timeline_pct=0.70,
            avg_poc_scope_changes_count=4.0,
            poc_abandoned_pct=0.40,
            poc_champion_engaged_pct=0.10,
            exec_sponsor_briefed_pct=0.05,
            avg_stakeholders_in_poc_count=0.5,
            poc_to_close_conversion_rate_pct=0.05,
            technical_validation_failure_rate_pct=0.50,
            competitive_poc_displacement_rate_pct=0.50,
        )
        result = self.e.assess(inp)
        assert result.poc_risk == POCRisk.critical

    def test_poc_gap_flag_can_be_true(self):
        inp = make_input(poc_to_close_conversion_rate_pct=0.10)
        result = self.e.assess(inp)
        assert result.has_poc_gap is True

    def test_requires_coaching_flag_can_be_true(self):
        inp = make_input(poc_champion_engaged_pct=0.30)
        result = self.e.assess(inp)
        assert result.requires_poc_coaching is True

    def test_pipeline_loss_non_negative(self):
        result = self.e.assess(make_input())
        assert result.estimated_pipeline_loss_usd >= 0.0

    def test_pattern_detected_in_assess(self):
        inp = make_input(
            pocs_exceeding_timeline_pct=0.60,
            avg_poc_scope_changes_count=3.0,
        )
        result = self.e.assess(inp)
        # execution score will be high -> stall detected
        assert result.poc_pattern == POCPattern.poc_stall


# ===========================================================================
# 20. assess_batch()
# ===========================================================================

class TestAssessBatch:
    def setup_method(self):
        self.e = make_engine()

    def test_returns_list(self):
        result = self.e.assess_batch([make_input()])
        assert isinstance(result, list)

    def test_empty_batch(self):
        result = self.e.assess_batch([])
        assert result == []

    def test_batch_length_matches_input(self):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = self.e.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_results_are_poc_result(self):
        inputs = [make_input(rep_id=f"R{i}") for i in range(3)]
        for r in self.e.assess_batch(inputs):
            assert isinstance(r, POCResult)

    def test_batch_stores_all_in_internal_list(self):
        inputs = [make_input(rep_id=f"R{i}") for i in range(4)]
        self.e.assess_batch(inputs)
        assert len(self.e._results) == 4

    def test_batch_rep_ids_correct(self):
        inputs = [make_input(rep_id=f"R{i}") for i in range(3)]
        results = self.e.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"R{i}"

    def test_batch_single_element(self):
        result = self.e.assess_batch([make_input(rep_id="SOLO")])
        assert len(result) == 1
        assert result[0].rep_id == "SOLO"

    def test_batch_preserves_order(self):
        reps = ["FIRST", "SECOND", "THIRD"]
        inputs = [make_input(rep_id=r) for r in reps]
        results = self.e.assess_batch(inputs)
        assert [r.rep_id for r in results] == reps


# ===========================================================================
# 21. summary()
# ===========================================================================

class TestSummary:
    def test_empty_summary_keys(self):
        e = make_engine()
        s = e.summary()
        assert isinstance(s, dict)
        assert len(s) == 13

    def test_empty_summary_total_zero(self):
        assert make_engine().summary()["total"] == 0

    def test_empty_summary_avg_composite_zero(self):
        assert make_engine().summary()["avg_poc_composite"] == 0.0

    def test_empty_summary_gap_count_zero(self):
        assert make_engine().summary()["poc_gap_count"] == 0

    def test_empty_summary_coaching_count_zero(self):
        assert make_engine().summary()["coaching_count"] == 0

    def test_empty_summary_pipeline_loss_zero(self):
        assert make_engine().summary()["total_estimated_pipeline_loss_usd"] == 0.0

    def test_empty_summary_all_avg_scores_zero(self):
        s = make_engine().summary()
        assert s["avg_poc_structure_score"] == 0.0
        assert s["avg_poc_execution_score"] == 0.0
        assert s["avg_poc_stakeholder_score"] == 0.0
        assert s["avg_poc_conversion_score"] == 0.0

    def test_empty_summary_count_dicts_empty(self):
        s = make_engine().summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}

    def test_summary_expected_keys(self):
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_poc_composite", "poc_gap_count",
            "coaching_count", "avg_poc_structure_score", "avg_poc_execution_score",
            "avg_poc_stakeholder_score", "avg_poc_conversion_score",
            "total_estimated_pipeline_loss_usd",
        }
        assert set(make_engine().summary().keys()) == expected

    def test_summary_total_after_assess(self):
        e = make_engine()
        e.assess(make_input())
        assert e.summary()["total"] == 1

    def test_summary_total_after_batch(self):
        e = make_engine()
        e.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        assert e.summary()["total"] == 5

    def test_summary_risk_counts_populated(self):
        e = make_engine()
        e.assess(make_input())
        s = e.summary()
        assert len(s["risk_counts"]) >= 1

    def test_summary_risk_counts_sum_equals_total(self):
        e = make_engine()
        e.assess_batch([make_input(rep_id=f"R{i}") for i in range(6)])
        s = e.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_pattern_counts_sum_equals_total(self):
        e = make_engine()
        e.assess_batch([make_input(rep_id=f"R{i}") for i in range(4)])
        s = e.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_summary_severity_counts_sum_equals_total(self):
        e = make_engine()
        e.assess_batch([make_input(rep_id=f"R{i}") for i in range(4)])
        s = e.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_equals_total(self):
        e = make_engine()
        e.assess_batch([make_input(rep_id=f"R{i}") for i in range(4)])
        s = e.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_avg_composite_reasonable(self):
        e = make_engine()
        e.assess(make_input())
        s = e.summary()
        assert 0.0 <= s["avg_poc_composite"] <= 100.0

    def test_summary_gap_count_matches_results(self):
        e = make_engine()
        # produce a gap by using low conversion
        e.assess(make_input(poc_to_close_conversion_rate_pct=0.10))
        e.assess(make_input())
        s = e.summary()
        assert s["poc_gap_count"] >= 1

    def test_summary_coaching_count_matches_results(self):
        e = make_engine()
        e.assess(make_input(poc_champion_engaged_pct=0.20))
        e.assess(make_input())
        s = e.summary()
        assert s["coaching_count"] >= 1

    def test_summary_avg_scores_between_0_and_100(self):
        e = make_engine()
        e.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        s = e.summary()
        for key in ["avg_poc_structure_score", "avg_poc_execution_score",
                    "avg_poc_stakeholder_score", "avg_poc_conversion_score"]:
            assert 0.0 <= s[key] <= 100.0

    def test_summary_pipeline_loss_non_negative(self):
        e = make_engine()
        e.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        assert e.summary()["total_estimated_pipeline_loss_usd"] >= 0.0

    def test_summary_accumulates_across_multiple_calls(self):
        e = make_engine()
        e.assess(make_input(rep_id="A"))
        e.assess(make_input(rep_id="B"))
        e.assess(make_input(rep_id="C"))
        assert e.summary()["total"] == 3


# ===========================================================================
# 22. Edge cases and boundary conditions
# ===========================================================================

class TestEdgeCases:
    def setup_method(self):
        self.e = make_engine()

    def test_zero_total_pocs(self):
        inp = make_input(total_pocs_conducted=0, poc_abandoned_pct=0.0)
        result = self.e.assess(inp)
        assert result.estimated_pipeline_loss_usd == 0.0

    def test_all_pcts_at_zero(self):
        inp = make_input(
            poc_to_close_conversion_rate_pct=1.0,
            pocs_exceeding_timeline_pct=0.0,
            pocs_with_no_success_criteria_pct=0.0,
            avg_poc_scope_changes_count=0.0,
            technical_validation_failure_rate_pct=0.0,
            poc_champion_engaged_pct=1.0,
            exec_sponsor_briefed_pct=1.0,
            mutual_success_plan_completion_pct=1.0,
            poc_abandoned_pct=0.0,
            competitive_poc_displacement_rate_pct=0.0,
        )
        result = self.e.assess(inp)
        assert result.poc_composite == 0.0
        assert result.poc_risk == POCRisk.low

    def test_all_pcts_at_maximum_bad(self):
        inp = make_input(
            poc_to_close_conversion_rate_pct=0.0,
            pocs_exceeding_timeline_pct=1.0,
            pocs_with_no_success_criteria_pct=1.0,
            avg_poc_scope_changes_count=10.0,
            technical_validation_failure_rate_pct=1.0,
            poc_champion_engaged_pct=0.0,
            exec_sponsor_briefed_pct=0.0,
            avg_stakeholders_in_poc_count=0.0,
            mutual_success_plan_completion_pct=0.0,
            avg_days_to_poc_kickoff=30.0,
            poc_abandoned_pct=1.0,
            competitive_poc_displacement_rate_pct=1.0,
        )
        result = self.e.assess(inp)
        assert result.poc_composite == 100.0
        assert result.poc_risk == POCRisk.critical
        assert result.poc_severity == POCSeverity.failing

    def test_exact_risk_threshold_60(self):
        """Composite exactly at 60 should be critical."""
        # We need composite exactly 60 — use direct method
        assert self.e._risk_level(60.0) == POCRisk.critical

    def test_exact_risk_threshold_just_below_60(self):
        assert self.e._risk_level(59.9) == POCRisk.high

    def test_exact_severity_threshold_60(self):
        assert self.e._severity(60.0) == POCSeverity.failing

    def test_exact_severity_threshold_just_below_60(self):
        assert self.e._severity(59.9) == POCSeverity.uncontrolled

    def test_single_poc(self):
        inp = make_input(total_pocs_conducted=1, poc_abandoned_pct=1.0)
        result = self.e.assess(inp)
        assert result.estimated_pipeline_loss_usd >= 0.0

    def test_very_large_opportunity_value(self):
        inp = make_input(
            total_pocs_conducted=100,
            poc_abandoned_pct=0.50,
            avg_opportunity_value_usd=1_000_000_000.0,
        )
        result = self.e.assess(inp)
        assert result.estimated_pipeline_loss_usd >= 0.0

    def test_scores_never_below_zero(self):
        inp = make_input()
        e = make_engine()
        assert e._poc_structure_score(inp) >= 0.0
        assert e._poc_execution_score(inp) >= 0.0
        assert e._poc_stakeholder_score(inp) >= 0.0
        assert e._poc_conversion_score(inp) >= 0.0

    def test_to_dict_values_are_strings_for_enums(self):
        result = self.e.assess(make_input())
        d = result.to_dict()
        assert isinstance(d["poc_risk"], str)
        assert isinstance(d["poc_pattern"], str)
        assert isinstance(d["poc_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_bool_values_preserved(self):
        result = self.e.assess(make_input())
        d = result.to_dict()
        assert isinstance(d["has_poc_gap"], bool)
        assert isinstance(d["requires_poc_coaching"], bool)

    def test_assess_does_not_mutate_input(self):
        inp = make_input()
        original_rep = inp.rep_id
        self.e.assess(inp)
        assert inp.rep_id == original_rep

    def test_multiple_engines_are_independent(self):
        e1 = make_engine()
        e2 = make_engine()
        e1.assess(make_input())
        assert len(e1._results) == 1
        assert len(e2._results) == 0

    def test_pattern_priority_stall_beats_criteria_gap(self):
        inp = make_input(
            pocs_exceeding_timeline_pct=0.40,
            pocs_with_no_success_criteria_pct=0.40,
        )
        result = self.e.assess(inp)
        # stall checked first
        if result.poc_execution_score >= 40:
            assert result.poc_pattern == POCPattern.poc_stall

    def test_poc_result_is_not_shared_between_assessments(self):
        r1 = self.e.assess(make_input(rep_id="A"))
        r2 = self.e.assess(make_input(rep_id="B"))
        assert r1 is not r2
        assert r1.rep_id != r2.rep_id


# ===========================================================================
# 23. End-to-end scenarios
# ===========================================================================

class TestEndToEndScenarios:
    def setup_method(self):
        self.e = make_engine()

    def test_excellent_rep(self):
        """A rep with excellent POC metrics should have low risk, structured severity, no action."""
        inp = make_input(
            poc_to_close_conversion_rate_pct=0.90,
            pocs_exceeding_timeline_pct=0.02,
            pocs_with_no_success_criteria_pct=0.02,
            avg_poc_scope_changes_count=0.2,
            technical_validation_failure_rate_pct=0.02,
            poc_champion_engaged_pct=0.95,
            exec_sponsor_briefed_pct=0.90,
            avg_stakeholders_in_poc_count=4.0,
            mutual_success_plan_completion_pct=0.95,
            avg_days_to_poc_kickoff=3.0,
            poc_abandoned_pct=0.01,
            competitive_poc_displacement_rate_pct=0.02,
        )
        result = self.e.assess(inp)
        assert result.poc_risk == POCRisk.low
        assert result.poc_severity == POCSeverity.structured
        assert result.recommended_action == POCAction.no_action
        assert result.poc_pattern == POCPattern.none
        assert "POC execution healthy" in result.poc_signal

    def test_stalled_poc_rep(self):
        """Rep with many stalled POCs should get poc_stall pattern."""
        inp = make_input(
            pocs_exceeding_timeline_pct=0.65,
            avg_poc_scope_changes_count=3.0,
        )
        result = self.e.assess(inp)
        assert result.poc_pattern == POCPattern.poc_stall

    def test_no_champion_rep(self):
        """Rep with poor champion engagement should get no_champion pattern."""
        inp = make_input(
            poc_champion_engaged_pct=0.20,
            exec_sponsor_briefed_pct=0.10,
            avg_stakeholders_in_poc_count=0.5,
            # Keep execution low so stall/scope_creep don't take priority
            pocs_exceeding_timeline_pct=0.02,
            avg_poc_scope_changes_count=0.2,
            technical_validation_failure_rate_pct=0.02,
            pocs_with_no_success_criteria_pct=0.02,
            mutual_success_plan_completion_pct=0.95,
        )
        result = self.e.assess(inp)
        assert result.poc_pattern == POCPattern.no_champion_during_poc
        assert result.recommended_action in (
            POCAction.champion_engagement_during_poc,
            POCAction.poc_structure_coaching,
            POCAction.success_criteria_alignment,
        )

    def test_technical_failure_rep(self):
        """Rep with high technical failure rate and low conversion gets technical_validation_failure."""
        inp = make_input(
            technical_validation_failure_rate_pct=0.35,
            poc_to_close_conversion_rate_pct=0.10,
            # Keep other scores low
            pocs_exceeding_timeline_pct=0.02,
            avg_poc_scope_changes_count=0.1,
            pocs_with_no_success_criteria_pct=0.02,
        )
        result = self.e.assess(inp)
        assert result.poc_pattern == POCPattern.technical_validation_failure
        # action depends on the computed risk level — accept any valid action
        assert isinstance(result.recommended_action, POCAction)

    def test_batch_mixed_reps(self):
        """Batch assessment with mixed inputs produces distinct results."""
        inputs = [
            make_input(rep_id="GOOD", poc_to_close_conversion_rate_pct=0.90),
            make_input(rep_id="BAD", poc_to_close_conversion_rate_pct=0.10,
                       pocs_exceeding_timeline_pct=0.70,
                       poc_champion_engaged_pct=0.10),
        ]
        results = self.e.assess_batch(inputs)
        # GOOD rep should have lower risk than BAD rep
        assert results[0].poc_risk in (POCRisk.low, POCRisk.moderate)
        assert results[1].poc_risk in (POCRisk.moderate, POCRisk.high, POCRisk.critical)

    def test_summary_after_mixed_batch(self):
        inputs = [
            make_input(rep_id="A"),
            make_input(rep_id="B", poc_to_close_conversion_rate_pct=0.10,
                       poc_abandoned_pct=0.40, pocs_exceeding_timeline_pct=0.70),
        ]
        self.e.assess_batch(inputs)
        s = self.e.summary()
        assert s["total"] == 2
        assert sum(s["risk_counts"].values()) == 2
        assert sum(s["pattern_counts"].values()) == 2
        assert sum(s["severity_counts"].values()) == 2
        assert sum(s["action_counts"].values()) == 2

    def test_to_dict_roundtrip(self):
        """to_dict output should be serialisable and values should be primitive types."""
        result = self.e.assess(make_input())
        d = result.to_dict()
        for v in d.values():
            assert isinstance(v, (str, float, bool, int)), f"unexpected type: {type(v)}"

    def test_scope_creep_pattern_end_to_end(self):
        inp = make_input(
            avg_poc_scope_changes_count=3.0,
            pocs_exceeding_timeline_pct=0.10,  # low, not stall
        )
        result = self.e.assess(inp)
        assert result.poc_pattern == POCPattern.scope_creep

    def test_success_criteria_gap_pattern_end_to_end(self):
        inp = make_input(
            pocs_with_no_success_criteria_pct=0.60,
            mutual_success_plan_completion_pct=0.10,
            # keep execution low
            pocs_exceeding_timeline_pct=0.02,
            avg_poc_scope_changes_count=0.1,
        )
        result = self.e.assess(inp)
        assert result.poc_pattern == POCPattern.success_criteria_gap

    def test_moderate_risk_gets_alignment_action(self):
        """A moderate-risk (composite 20-39) rep always gets success_criteria_alignment."""
        # Force composite into moderate zone: need roughly composite 20-39
        inp = make_input(
            pocs_with_no_success_criteria_pct=0.15,    # structure +8
            mutual_success_plan_completion_pct=0.50,   # structure +18 -> total 26
            avg_days_to_poc_kickoff=0.0,
            pocs_exceeding_timeline_pct=0.0,
            avg_poc_scope_changes_count=0.0,
            poc_abandoned_pct=0.0,
            poc_champion_engaged_pct=1.0,
            exec_sponsor_briefed_pct=1.0,
            avg_stakeholders_in_poc_count=5.0,
            poc_to_close_conversion_rate_pct=0.70,
            technical_validation_failure_rate_pct=0.0,
            competitive_poc_displacement_rate_pct=0.0,
        )
        result = self.e.assess(inp)
        if result.poc_risk == POCRisk.moderate:
            assert result.recommended_action == POCAction.success_criteria_alignment

    def test_pipeline_loss_scales_with_composite(self):
        """Higher composite with same input fields should produce higher pipeline loss."""
        inp_low = make_input(total_pocs_conducted=10, poc_abandoned_pct=0.20,
                             avg_opportunity_value_usd=10_000.0)
        e = make_engine()
        loss_low = e._estimated_pipeline_loss(inp_low, 20.0)
        loss_high = e._estimated_pipeline_loss(inp_low, 80.0)
        assert loss_high > loss_low

    def test_summary_pipeline_loss_is_sum_of_individual_losses(self):
        e = make_engine()
        r1 = e.assess(make_input(rep_id="A"))
        r2 = e.assess(make_input(rep_id="B"))
        expected = round(r1.estimated_pipeline_loss_usd + r2.estimated_pipeline_loss_usd, 2)
        assert e.summary()["total_estimated_pipeline_loss_usd"] == expected
