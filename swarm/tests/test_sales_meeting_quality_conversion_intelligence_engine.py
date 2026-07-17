"""
First half of the comprehensive pytest test suite for
SalesMeetingQualityConversionIntelligenceEngine.

Covers:
  TestEnums
  TestMeetingInputFields
  TestMeetingResultFields
  TestConversionScore
  TestQualityScore
  TestExecutionScore
  TestAdvancementScore
  TestComposite
  TestPattern
  TestPatternPriority
  TestRisk
  TestSeverity
"""

import dataclasses
import pytest

from swarm.intelligence.sales_meeting_quality_conversion_intelligence_engine import (
    MeetingRisk,
    MeetingPattern,
    MeetingSeverity,
    MeetingAction,
    MeetingInput,
    MeetingResult,
    SalesMeetingQualityConversionIntelligenceEngine,
)


# ─── Helper ──────────────────────────────────────────────────────────────────

def make_input(**overrides) -> MeetingInput:
    defaults = dict(
        rep_id="rep-001",
        region="Northeast",
        evaluation_period_id="Q1-2026",
        meetings_to_opportunity_rate_pct=0.80,
        discovery_completion_rate_pct=0.90,
        next_step_confirmed_rate_pct=0.90,
        demo_to_proposal_rate_pct=0.80,
        proposal_to_close_rate_pct=0.50,
        avg_meeting_duration_minutes=45.0,
        no_show_rate_pct=0.03,
        reschedule_rate_pct=0.05,
        multi_stakeholder_meeting_rate_pct=0.60,
        pain_identified_rate_pct=0.80,
        budget_confirmed_in_meeting_rate_pct=0.70,
        decision_process_mapped_rate_pct=0.70,
        meeting_notes_completion_rate_pct=0.90,
        repeat_meeting_same_stage_rate_pct=0.05,
        meeting_to_pipeline_velocity_days=5.0,
        champion_identified_meeting_rate_pct=0.70,
        competitive_mentioned_rate_pct=0.30,
        executive_access_secured_rate_pct=0.40,
        total_meetings_held=10,
        avg_deal_value_usd=50000.0,
    )
    defaults.update(overrides)
    return MeetingInput(**defaults)


# ─── TestEnums ───────────────────────────────────────────────────────────────

class TestEnums:
    # MeetingRisk
    def test_meeting_risk_low_is_member(self):
        assert MeetingRisk.low in MeetingRisk

    def test_meeting_risk_moderate_is_member(self):
        assert MeetingRisk.moderate in MeetingRisk

    def test_meeting_risk_high_is_member(self):
        assert MeetingRisk.high in MeetingRisk

    def test_meeting_risk_critical_is_member(self):
        assert MeetingRisk.critical in MeetingRisk

    def test_meeting_risk_low_value(self):
        assert MeetingRisk.low.value == "low"

    def test_meeting_risk_moderate_value(self):
        assert MeetingRisk.moderate.value == "moderate"

    def test_meeting_risk_high_value(self):
        assert MeetingRisk.high.value == "high"

    def test_meeting_risk_critical_value(self):
        assert MeetingRisk.critical.value == "critical"

    def test_meeting_risk_is_str_enum(self):
        assert isinstance(MeetingRisk.low, str)

    def test_meeting_risk_has_exactly_4_members(self):
        assert len(MeetingRisk) == 4

    # MeetingPattern
    def test_meeting_pattern_none_is_member(self):
        assert MeetingPattern.none in MeetingPattern

    def test_meeting_pattern_calendar_stuffing_is_member(self):
        assert MeetingPattern.calendar_stuffing in MeetingPattern

    def test_meeting_pattern_discovery_skipper_is_member(self):
        assert MeetingPattern.discovery_skipper in MeetingPattern

    def test_meeting_pattern_next_step_avoider_is_member(self):
        assert MeetingPattern.next_step_avoider in MeetingPattern

    def test_meeting_pattern_phantom_meeting_maker_is_member(self):
        assert MeetingPattern.phantom_meeting_maker in MeetingPattern

    def test_meeting_pattern_demo_looper_is_member(self):
        assert MeetingPattern.demo_looper in MeetingPattern

    def test_meeting_pattern_none_value(self):
        assert MeetingPattern.none.value == "none"

    def test_meeting_pattern_calendar_stuffing_value(self):
        assert MeetingPattern.calendar_stuffing.value == "calendar_stuffing"

    def test_meeting_pattern_discovery_skipper_value(self):
        assert MeetingPattern.discovery_skipper.value == "discovery_skipper"

    def test_meeting_pattern_next_step_avoider_value(self):
        assert MeetingPattern.next_step_avoider.value == "next_step_avoider"

    def test_meeting_pattern_phantom_meeting_maker_value(self):
        assert MeetingPattern.phantom_meeting_maker.value == "phantom_meeting_maker"

    def test_meeting_pattern_demo_looper_value(self):
        assert MeetingPattern.demo_looper.value == "demo_looper"

    def test_meeting_pattern_is_str_enum(self):
        assert isinstance(MeetingPattern.calendar_stuffing, str)

    def test_meeting_pattern_has_exactly_6_members(self):
        assert len(MeetingPattern) == 6

    # MeetingSeverity
    def test_meeting_severity_converting_is_member(self):
        assert MeetingSeverity.converting in MeetingSeverity

    def test_meeting_severity_slipping_is_member(self):
        assert MeetingSeverity.slipping in MeetingSeverity

    def test_meeting_severity_stalling_is_member(self):
        assert MeetingSeverity.stalling in MeetingSeverity

    def test_meeting_severity_collapsing_is_member(self):
        assert MeetingSeverity.collapsing in MeetingSeverity

    def test_meeting_severity_converting_value(self):
        assert MeetingSeverity.converting.value == "converting"

    def test_meeting_severity_slipping_value(self):
        assert MeetingSeverity.slipping.value == "slipping"

    def test_meeting_severity_stalling_value(self):
        assert MeetingSeverity.stalling.value == "stalling"

    def test_meeting_severity_collapsing_value(self):
        assert MeetingSeverity.collapsing.value == "collapsing"

    def test_meeting_severity_is_str_enum(self):
        assert isinstance(MeetingSeverity.converting, str)

    def test_meeting_severity_has_exactly_4_members(self):
        assert len(MeetingSeverity) == 4

    # MeetingAction
    def test_meeting_action_no_action_is_member(self):
        assert MeetingAction.no_action in MeetingAction

    def test_meeting_action_meeting_quality_monitoring_is_member(self):
        assert MeetingAction.meeting_quality_monitoring in MeetingAction

    def test_meeting_action_discovery_coaching_is_member(self):
        assert MeetingAction.discovery_coaching in MeetingAction

    def test_meeting_action_next_step_discipline_coaching_is_member(self):
        assert MeetingAction.next_step_discipline_coaching in MeetingAction

    def test_meeting_action_pipeline_qualification_coaching_is_member(self):
        assert MeetingAction.pipeline_qualification_coaching in MeetingAction

    def test_meeting_action_meeting_audit_is_member(self):
        assert MeetingAction.meeting_audit in MeetingAction

    def test_meeting_action_full_pipeline_reset_is_member(self):
        assert MeetingAction.full_pipeline_reset in MeetingAction

    def test_meeting_action_no_action_value(self):
        assert MeetingAction.no_action.value == "no_action"

    def test_meeting_action_meeting_quality_monitoring_value(self):
        assert MeetingAction.meeting_quality_monitoring.value == "meeting_quality_monitoring"

    def test_meeting_action_discovery_coaching_value(self):
        assert MeetingAction.discovery_coaching.value == "discovery_coaching"

    def test_meeting_action_next_step_discipline_coaching_value(self):
        assert MeetingAction.next_step_discipline_coaching.value == "next_step_discipline_coaching"

    def test_meeting_action_pipeline_qualification_coaching_value(self):
        assert MeetingAction.pipeline_qualification_coaching.value == "pipeline_qualification_coaching"

    def test_meeting_action_meeting_audit_value(self):
        assert MeetingAction.meeting_audit.value == "meeting_audit"

    def test_meeting_action_full_pipeline_reset_value(self):
        assert MeetingAction.full_pipeline_reset.value == "full_pipeline_reset"

    def test_meeting_action_is_str_enum(self):
        assert isinstance(MeetingAction.no_action, str)

    def test_meeting_action_has_exactly_7_members(self):
        assert len(MeetingAction) == 7


# ─── TestMeetingInputFields ───────────────────────────────────────────────────

class TestMeetingInputFields:
    def test_total_field_count_is_23(self):
        fields = dataclasses.fields(MeetingInput)
        assert len(fields) == 23

    def test_rep_id_field(self):
        inp = make_input(rep_id="rep-xyz")
        assert inp.rep_id == "rep-xyz"

    def test_region_field(self):
        inp = make_input(region="West")
        assert inp.region == "West"

    def test_evaluation_period_id_field(self):
        inp = make_input(evaluation_period_id="Q2-2026")
        assert inp.evaluation_period_id == "Q2-2026"

    def test_meetings_to_opportunity_rate_pct_field(self):
        inp = make_input(meetings_to_opportunity_rate_pct=0.35)
        assert inp.meetings_to_opportunity_rate_pct == 0.35

    def test_discovery_completion_rate_pct_field(self):
        inp = make_input(discovery_completion_rate_pct=0.45)
        assert inp.discovery_completion_rate_pct == 0.45

    def test_next_step_confirmed_rate_pct_field(self):
        inp = make_input(next_step_confirmed_rate_pct=0.65)
        assert inp.next_step_confirmed_rate_pct == 0.65

    def test_demo_to_proposal_rate_pct_field(self):
        inp = make_input(demo_to_proposal_rate_pct=0.40)
        assert inp.demo_to_proposal_rate_pct == 0.40

    def test_proposal_to_close_rate_pct_field(self):
        inp = make_input(proposal_to_close_rate_pct=0.20)
        assert inp.proposal_to_close_rate_pct == 0.20

    def test_avg_meeting_duration_minutes_field(self):
        inp = make_input(avg_meeting_duration_minutes=60.0)
        assert inp.avg_meeting_duration_minutes == 60.0

    def test_no_show_rate_pct_field(self):
        inp = make_input(no_show_rate_pct=0.10)
        assert inp.no_show_rate_pct == 0.10

    def test_reschedule_rate_pct_field(self):
        inp = make_input(reschedule_rate_pct=0.15)
        assert inp.reschedule_rate_pct == 0.15

    def test_multi_stakeholder_meeting_rate_pct_field(self):
        inp = make_input(multi_stakeholder_meeting_rate_pct=0.30)
        assert inp.multi_stakeholder_meeting_rate_pct == 0.30

    def test_pain_identified_rate_pct_field(self):
        inp = make_input(pain_identified_rate_pct=0.55)
        assert inp.pain_identified_rate_pct == 0.55

    def test_budget_confirmed_in_meeting_rate_pct_field(self):
        inp = make_input(budget_confirmed_in_meeting_rate_pct=0.50)
        assert inp.budget_confirmed_in_meeting_rate_pct == 0.50

    def test_decision_process_mapped_rate_pct_field(self):
        inp = make_input(decision_process_mapped_rate_pct=0.60)
        assert inp.decision_process_mapped_rate_pct == 0.60

    def test_meeting_notes_completion_rate_pct_field(self):
        inp = make_input(meeting_notes_completion_rate_pct=0.75)
        assert inp.meeting_notes_completion_rate_pct == 0.75

    def test_repeat_meeting_same_stage_rate_pct_field(self):
        inp = make_input(repeat_meeting_same_stage_rate_pct=0.20)
        assert inp.repeat_meeting_same_stage_rate_pct == 0.20

    def test_meeting_to_pipeline_velocity_days_field(self):
        inp = make_input(meeting_to_pipeline_velocity_days=14.0)
        assert inp.meeting_to_pipeline_velocity_days == 14.0

    def test_champion_identified_meeting_rate_pct_field(self):
        inp = make_input(champion_identified_meeting_rate_pct=0.55)
        assert inp.champion_identified_meeting_rate_pct == 0.55

    def test_competitive_mentioned_rate_pct_field(self):
        inp = make_input(competitive_mentioned_rate_pct=0.40)
        assert inp.competitive_mentioned_rate_pct == 0.40

    def test_executive_access_secured_rate_pct_field(self):
        inp = make_input(executive_access_secured_rate_pct=0.25)
        assert inp.executive_access_secured_rate_pct == 0.25

    def test_total_meetings_held_field(self):
        inp = make_input(total_meetings_held=25)
        assert inp.total_meetings_held == 25

    def test_avg_deal_value_usd_field(self):
        inp = make_input(avg_deal_value_usd=75000.0)
        assert inp.avg_deal_value_usd == 75000.0

    def test_rep_id_is_str(self):
        inp = make_input()
        assert isinstance(inp.rep_id, str)

    def test_total_meetings_held_is_int(self):
        inp = make_input()
        assert isinstance(inp.total_meetings_held, int)

    def test_meetings_to_opportunity_rate_pct_is_float(self):
        inp = make_input()
        assert isinstance(inp.meetings_to_opportunity_rate_pct, float)


# ─── TestMeetingResultFields ──────────────────────────────────────────────────

class TestMeetingResultFields:
    def setup_method(self):
        self.engine = SalesMeetingQualityConversionIntelligenceEngine()
        self.result = self.engine.assess(make_input())
        self.d = self.result.to_dict()

    def test_result_has_15_fields(self):
        fields = dataclasses.fields(MeetingResult)
        assert len(fields) == 15

    def test_to_dict_returns_exactly_15_keys(self):
        assert len(self.d) == 15

    def test_to_dict_has_rep_id(self):
        assert "rep_id" in self.d

    def test_to_dict_has_region(self):
        assert "region" in self.d

    def test_to_dict_has_meeting_risk(self):
        assert "meeting_risk" in self.d

    def test_to_dict_has_meeting_pattern(self):
        assert "meeting_pattern" in self.d

    def test_to_dict_has_meeting_severity(self):
        assert "meeting_severity" in self.d

    def test_to_dict_has_recommended_action(self):
        assert "recommended_action" in self.d

    def test_to_dict_has_conversion_score(self):
        assert "conversion_score" in self.d

    def test_to_dict_has_quality_score(self):
        assert "quality_score" in self.d

    def test_to_dict_has_execution_score(self):
        assert "execution_score" in self.d

    def test_to_dict_has_advancement_score(self):
        assert "advancement_score" in self.d

    def test_to_dict_has_meeting_composite(self):
        assert "meeting_composite" in self.d

    def test_to_dict_has_has_meeting_gap(self):
        assert "has_meeting_gap" in self.d

    def test_to_dict_has_requires_meeting_coaching(self):
        assert "requires_meeting_coaching" in self.d

    def test_to_dict_has_estimated_wasted_meeting_usd(self):
        assert "estimated_wasted_meeting_usd" in self.d

    def test_to_dict_has_meeting_signal(self):
        assert "meeting_signal" in self.d

    def test_to_dict_meeting_risk_is_string(self):
        assert isinstance(self.d["meeting_risk"], str)

    def test_to_dict_meeting_pattern_is_string(self):
        assert isinstance(self.d["meeting_pattern"], str)

    def test_to_dict_meeting_severity_is_string(self):
        assert isinstance(self.d["meeting_severity"], str)

    def test_to_dict_recommended_action_is_string(self):
        assert isinstance(self.d["recommended_action"], str)

    def test_to_dict_conversion_score_is_numeric(self):
        assert isinstance(self.d["conversion_score"], (int, float))

    def test_to_dict_quality_score_is_numeric(self):
        assert isinstance(self.d["quality_score"], (int, float))

    def test_to_dict_execution_score_is_numeric(self):
        assert isinstance(self.d["execution_score"], (int, float))

    def test_to_dict_advancement_score_is_numeric(self):
        assert isinstance(self.d["advancement_score"], (int, float))

    def test_to_dict_meeting_composite_is_numeric(self):
        assert isinstance(self.d["meeting_composite"], (int, float))

    def test_to_dict_has_meeting_gap_is_bool(self):
        assert isinstance(self.d["has_meeting_gap"], bool)

    def test_to_dict_requires_meeting_coaching_is_bool(self):
        assert isinstance(self.d["requires_meeting_coaching"], bool)

    def test_to_dict_meeting_signal_is_string(self):
        assert isinstance(self.d["meeting_signal"], str)

    def test_to_dict_rep_id_value_matches_input(self):
        engine = SalesMeetingQualityConversionIntelligenceEngine()
        result = engine.assess(make_input(rep_id="rep-ABC"))
        assert result.to_dict()["rep_id"] == "rep-ABC"

    def test_to_dict_region_value_matches_input(self):
        engine = SalesMeetingQualityConversionIntelligenceEngine()
        result = engine.assess(make_input(region="Southeast"))
        assert result.to_dict()["region"] == "Southeast"

    def test_to_dict_meeting_risk_is_valid_enum_value(self):
        valid = {e.value for e in MeetingRisk}
        assert self.d["meeting_risk"] in valid

    def test_to_dict_meeting_pattern_is_valid_enum_value(self):
        valid = {e.value for e in MeetingPattern}
        assert self.d["meeting_pattern"] in valid

    def test_to_dict_meeting_severity_is_valid_enum_value(self):
        valid = {e.value for e in MeetingSeverity}
        assert self.d["meeting_severity"] in valid

    def test_to_dict_recommended_action_is_valid_enum_value(self):
        valid = {e.value for e in MeetingAction}
        assert self.d["recommended_action"] in valid


# ─── TestConversionScore ──────────────────────────────────────────────────────

class TestConversionScore:
    def setup_method(self):
        self.engine = SalesMeetingQualityConversionIntelligenceEngine()

    # meetings_to_opportunity_rate_pct thresholds
    def test_mto_rate_0_20_exact_adds_40(self):
        score = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.20,
            demo_to_proposal_rate_pct=0.80,
            proposal_to_close_rate_pct=0.50,
        )).conversion_score
        assert score == 40.0

    def test_mto_rate_0_21_not_top_band(self):
        score = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.21,
            demo_to_proposal_rate_pct=0.80,
            proposal_to_close_rate_pct=0.50,
        )).conversion_score
        assert score < 40.0

    def test_mto_rate_0_40_adds_22(self):
        score = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.40,
            demo_to_proposal_rate_pct=0.80,
            proposal_to_close_rate_pct=0.50,
        )).conversion_score
        assert score == 22.0

    def test_mto_rate_0_41_not_middle_band(self):
        score = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.41,
            demo_to_proposal_rate_pct=0.80,
            proposal_to_close_rate_pct=0.50,
        )).conversion_score
        assert score < 22.0

    def test_mto_rate_0_60_adds_8(self):
        score = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.60,
            demo_to_proposal_rate_pct=0.80,
            proposal_to_close_rate_pct=0.50,
        )).conversion_score
        assert score == 8.0

    def test_mto_rate_0_61_adds_0(self):
        score = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.61,
            demo_to_proposal_rate_pct=0.80,
            proposal_to_close_rate_pct=0.50,
        )).conversion_score
        assert score == 0.0

    # demo_to_proposal_rate_pct thresholds
    def test_demo_to_proposal_0_25_adds_35(self):
        score = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.80,
            demo_to_proposal_rate_pct=0.25,
            proposal_to_close_rate_pct=0.50,
        )).conversion_score
        assert score == 35.0

    def test_demo_to_proposal_0_26_not_top_band(self):
        score = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.80,
            demo_to_proposal_rate_pct=0.26,
            proposal_to_close_rate_pct=0.50,
        )).conversion_score
        assert score < 35.0

    def test_demo_to_proposal_0_50_adds_18(self):
        score = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.80,
            demo_to_proposal_rate_pct=0.50,
            proposal_to_close_rate_pct=0.50,
        )).conversion_score
        assert score == 18.0

    def test_demo_to_proposal_0_51_adds_0(self):
        score = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.80,
            demo_to_proposal_rate_pct=0.51,
            proposal_to_close_rate_pct=0.50,
        )).conversion_score
        assert score == 0.0

    # proposal_to_close_rate_pct thresholds
    def test_proposal_to_close_0_15_adds_25(self):
        score = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.80,
            demo_to_proposal_rate_pct=0.80,
            proposal_to_close_rate_pct=0.15,
        )).conversion_score
        assert score == 25.0

    def test_proposal_to_close_0_16_not_top_band(self):
        score = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.80,
            demo_to_proposal_rate_pct=0.80,
            proposal_to_close_rate_pct=0.16,
        )).conversion_score
        assert score < 25.0

    def test_proposal_to_close_0_30_adds_12(self):
        score = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.80,
            demo_to_proposal_rate_pct=0.80,
            proposal_to_close_rate_pct=0.30,
        )).conversion_score
        assert score == 12.0

    def test_proposal_to_close_0_31_adds_0(self):
        score = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.80,
            demo_to_proposal_rate_pct=0.80,
            proposal_to_close_rate_pct=0.31,
        )).conversion_score
        assert score == 0.0

    # Exact boundary sum tests
    def test_all_top_bands_sums_to_100(self):
        score = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.20,
            demo_to_proposal_rate_pct=0.25,
            proposal_to_close_rate_pct=0.15,
        )).conversion_score
        assert score == 100.0

    def test_all_worst_inputs_produce_100(self):
        # 40+35+25=100 → capped at 100
        score = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.10,
            demo_to_proposal_rate_pct=0.10,
            proposal_to_close_rate_pct=0.10,
        )).conversion_score
        assert score == 100.0

    def test_conversion_score_never_exceeds_100(self):
        score = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.01,
            demo_to_proposal_rate_pct=0.01,
            proposal_to_close_rate_pct=0.01,
        )).conversion_score
        assert score <= 100.0

    def test_conversion_score_is_float(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.conversion_score, float)

    def test_mto_0_20_demo_0_50_close_0_30_equals_70(self):
        score = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.20,
            demo_to_proposal_rate_pct=0.50,
            proposal_to_close_rate_pct=0.30,
        )).conversion_score
        # 40 + 18 + 12 = 70
        assert score == 70.0

    def test_mto_0_40_demo_0_25_close_0_15_equals_82(self):
        score = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.40,
            demo_to_proposal_rate_pct=0.25,
            proposal_to_close_rate_pct=0.15,
        )).conversion_score
        # 22 + 35 + 25 = 82
        assert score == 82.0

    def test_all_good_rates_yield_0(self):
        score = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.80,
            demo_to_proposal_rate_pct=0.80,
            proposal_to_close_rate_pct=0.80,
        )).conversion_score
        assert score == 0.0


# ─── TestQualityScore ─────────────────────────────────────────────────────────

class TestQualityScore:
    def setup_method(self):
        self.engine = SalesMeetingQualityConversionIntelligenceEngine()

    # discovery_completion_rate_pct thresholds
    def test_discovery_completion_0_30_adds_40(self):
        score = self.engine.assess(make_input(
            discovery_completion_rate_pct=0.30,
            pain_identified_rate_pct=0.80,
            multi_stakeholder_meeting_rate_pct=0.80,
        )).quality_score
        assert score == 40.0

    def test_discovery_completion_0_31_not_top_band(self):
        score = self.engine.assess(make_input(
            discovery_completion_rate_pct=0.31,
            pain_identified_rate_pct=0.80,
            multi_stakeholder_meeting_rate_pct=0.80,
        )).quality_score
        assert score < 40.0

    def test_discovery_completion_0_55_adds_22(self):
        score = self.engine.assess(make_input(
            discovery_completion_rate_pct=0.55,
            pain_identified_rate_pct=0.80,
            multi_stakeholder_meeting_rate_pct=0.80,
        )).quality_score
        assert score == 22.0

    def test_discovery_completion_0_56_not_middle_band(self):
        score = self.engine.assess(make_input(
            discovery_completion_rate_pct=0.56,
            pain_identified_rate_pct=0.80,
            multi_stakeholder_meeting_rate_pct=0.80,
        )).quality_score
        assert score < 22.0

    def test_discovery_completion_0_75_adds_8(self):
        score = self.engine.assess(make_input(
            discovery_completion_rate_pct=0.75,
            pain_identified_rate_pct=0.80,
            multi_stakeholder_meeting_rate_pct=0.80,
        )).quality_score
        assert score == 8.0

    def test_discovery_completion_0_76_adds_0(self):
        score = self.engine.assess(make_input(
            discovery_completion_rate_pct=0.76,
            pain_identified_rate_pct=0.80,
            multi_stakeholder_meeting_rate_pct=0.80,
        )).quality_score
        assert score == 0.0

    # pain_identified_rate_pct thresholds
    def test_pain_identified_0_30_adds_35(self):
        score = self.engine.assess(make_input(
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.30,
            multi_stakeholder_meeting_rate_pct=0.80,
        )).quality_score
        assert score == 35.0

    def test_pain_identified_0_31_not_top_band(self):
        score = self.engine.assess(make_input(
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.31,
            multi_stakeholder_meeting_rate_pct=0.80,
        )).quality_score
        assert score < 35.0

    def test_pain_identified_0_55_adds_18(self):
        score = self.engine.assess(make_input(
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.55,
            multi_stakeholder_meeting_rate_pct=0.80,
        )).quality_score
        assert score == 18.0

    def test_pain_identified_0_56_adds_0(self):
        score = self.engine.assess(make_input(
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.56,
            multi_stakeholder_meeting_rate_pct=0.80,
        )).quality_score
        assert score == 0.0

    # multi_stakeholder_meeting_rate_pct thresholds
    def test_multi_stakeholder_0_20_adds_25(self):
        score = self.engine.assess(make_input(
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.90,
            multi_stakeholder_meeting_rate_pct=0.20,
        )).quality_score
        assert score == 25.0

    def test_multi_stakeholder_0_21_not_top_band(self):
        score = self.engine.assess(make_input(
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.90,
            multi_stakeholder_meeting_rate_pct=0.21,
        )).quality_score
        assert score < 25.0

    def test_multi_stakeholder_0_40_adds_12(self):
        score = self.engine.assess(make_input(
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.90,
            multi_stakeholder_meeting_rate_pct=0.40,
        )).quality_score
        assert score == 12.0

    def test_multi_stakeholder_0_41_adds_0(self):
        score = self.engine.assess(make_input(
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.90,
            multi_stakeholder_meeting_rate_pct=0.41,
        )).quality_score
        assert score == 0.0

    def test_all_worst_inputs_produce_100_quality(self):
        # 40+35+25=100 capped at 100
        score = self.engine.assess(make_input(
            discovery_completion_rate_pct=0.10,
            pain_identified_rate_pct=0.10,
            multi_stakeholder_meeting_rate_pct=0.10,
        )).quality_score
        assert score == 100.0

    def test_all_good_inputs_produce_0_quality(self):
        score = self.engine.assess(make_input(
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.90,
            multi_stakeholder_meeting_rate_pct=0.90,
        )).quality_score
        assert score == 0.0

    def test_quality_score_never_exceeds_100(self):
        score = self.engine.assess(make_input(
            discovery_completion_rate_pct=0.01,
            pain_identified_rate_pct=0.01,
            multi_stakeholder_meeting_rate_pct=0.01,
        )).quality_score
        assert score <= 100.0

    def test_quality_score_is_float(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.quality_score, float)

    def test_discovery_0_55_pain_0_55_multi_0_40_sums_to_52(self):
        score = self.engine.assess(make_input(
            discovery_completion_rate_pct=0.55,
            pain_identified_rate_pct=0.55,
            multi_stakeholder_meeting_rate_pct=0.40,
        )).quality_score
        # 22 + 18 + 12 = 52
        assert score == 52.0

    def test_discovery_0_30_pain_0_30_multi_0_40_sums_to_87(self):
        score = self.engine.assess(make_input(
            discovery_completion_rate_pct=0.30,
            pain_identified_rate_pct=0.30,
            multi_stakeholder_meeting_rate_pct=0.40,
        )).quality_score
        # 40 + 35 + 12 = 87
        assert score == 87.0


# ─── TestExecutionScore ───────────────────────────────────────────────────────

class TestExecutionScore:
    def setup_method(self):
        self.engine = SalesMeetingQualityConversionIntelligenceEngine()

    # no_show_rate_pct thresholds (>=, high is bad)
    def test_no_show_0_30_adds_40(self):
        score = self.engine.assess(make_input(
            no_show_rate_pct=0.30,
            reschedule_rate_pct=0.05,
            meeting_notes_completion_rate_pct=0.90,
        )).execution_score
        assert score == 40.0

    def test_no_show_0_29_not_top_band(self):
        score = self.engine.assess(make_input(
            no_show_rate_pct=0.29,
            reschedule_rate_pct=0.05,
            meeting_notes_completion_rate_pct=0.90,
        )).execution_score
        assert score < 40.0

    def test_no_show_0_18_adds_22(self):
        score = self.engine.assess(make_input(
            no_show_rate_pct=0.18,
            reschedule_rate_pct=0.05,
            meeting_notes_completion_rate_pct=0.90,
        )).execution_score
        assert score == 22.0

    def test_no_show_0_17_not_second_band(self):
        score = self.engine.assess(make_input(
            no_show_rate_pct=0.17,
            reschedule_rate_pct=0.05,
            meeting_notes_completion_rate_pct=0.90,
        )).execution_score
        assert score < 22.0

    def test_no_show_0_08_adds_8(self):
        score = self.engine.assess(make_input(
            no_show_rate_pct=0.08,
            reschedule_rate_pct=0.05,
            meeting_notes_completion_rate_pct=0.90,
        )).execution_score
        assert score == 8.0

    def test_no_show_0_07_adds_0(self):
        score = self.engine.assess(make_input(
            no_show_rate_pct=0.07,
            reschedule_rate_pct=0.05,
            meeting_notes_completion_rate_pct=0.90,
        )).execution_score
        assert score == 0.0

    # reschedule_rate_pct thresholds (>=)
    def test_reschedule_0_40_adds_35(self):
        score = self.engine.assess(make_input(
            no_show_rate_pct=0.01,
            reschedule_rate_pct=0.40,
            meeting_notes_completion_rate_pct=0.90,
        )).execution_score
        assert score == 35.0

    def test_reschedule_0_39_not_top_band(self):
        score = self.engine.assess(make_input(
            no_show_rate_pct=0.01,
            reschedule_rate_pct=0.39,
            meeting_notes_completion_rate_pct=0.90,
        )).execution_score
        assert score < 35.0

    def test_reschedule_0_22_adds_18(self):
        score = self.engine.assess(make_input(
            no_show_rate_pct=0.01,
            reschedule_rate_pct=0.22,
            meeting_notes_completion_rate_pct=0.90,
        )).execution_score
        assert score == 18.0

    def test_reschedule_0_21_adds_0(self):
        score = self.engine.assess(make_input(
            no_show_rate_pct=0.01,
            reschedule_rate_pct=0.21,
            meeting_notes_completion_rate_pct=0.90,
        )).execution_score
        assert score == 0.0

    # meeting_notes_completion_rate_pct thresholds (<=, low is bad)
    def test_notes_completion_0_30_adds_25(self):
        score = self.engine.assess(make_input(
            no_show_rate_pct=0.01,
            reschedule_rate_pct=0.05,
            meeting_notes_completion_rate_pct=0.30,
        )).execution_score
        assert score == 25.0

    def test_notes_completion_0_31_not_top_band(self):
        score = self.engine.assess(make_input(
            no_show_rate_pct=0.01,
            reschedule_rate_pct=0.05,
            meeting_notes_completion_rate_pct=0.31,
        )).execution_score
        assert score < 25.0

    def test_notes_completion_0_55_adds_12(self):
        score = self.engine.assess(make_input(
            no_show_rate_pct=0.01,
            reschedule_rate_pct=0.05,
            meeting_notes_completion_rate_pct=0.55,
        )).execution_score
        assert score == 12.0

    def test_notes_completion_0_56_adds_0(self):
        score = self.engine.assess(make_input(
            no_show_rate_pct=0.01,
            reschedule_rate_pct=0.05,
            meeting_notes_completion_rate_pct=0.56,
        )).execution_score
        assert score == 0.0

    def test_all_worst_inputs_produce_100_execution(self):
        # 40+35+25=100 capped at 100
        score = self.engine.assess(make_input(
            no_show_rate_pct=0.50,
            reschedule_rate_pct=0.60,
            meeting_notes_completion_rate_pct=0.10,
        )).execution_score
        assert score == 100.0

    def test_all_good_inputs_produce_0_execution(self):
        score = self.engine.assess(make_input(
            no_show_rate_pct=0.01,
            reschedule_rate_pct=0.01,
            meeting_notes_completion_rate_pct=0.99,
        )).execution_score
        assert score == 0.0

    def test_execution_score_never_exceeds_100(self):
        score = self.engine.assess(make_input(
            no_show_rate_pct=1.0,
            reschedule_rate_pct=1.0,
            meeting_notes_completion_rate_pct=0.0,
        )).execution_score
        assert score <= 100.0

    def test_execution_score_is_float(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.execution_score, float)

    def test_no_show_0_18_reschedule_0_22_notes_0_55_sums_to_52(self):
        score = self.engine.assess(make_input(
            no_show_rate_pct=0.18,
            reschedule_rate_pct=0.22,
            meeting_notes_completion_rate_pct=0.55,
        )).execution_score
        # 22 + 18 + 12 = 52
        assert score == 52.0

    def test_no_show_0_30_reschedule_0_40_notes_0_30_sums_to_100(self):
        score = self.engine.assess(make_input(
            no_show_rate_pct=0.30,
            reschedule_rate_pct=0.40,
            meeting_notes_completion_rate_pct=0.30,
        )).execution_score
        # 40 + 35 + 25 = 100
        assert score == 100.0


# ─── TestAdvancementScore ─────────────────────────────────────────────────────

class TestAdvancementScore:
    def setup_method(self):
        self.engine = SalesMeetingQualityConversionIntelligenceEngine()

    # next_step_confirmed_rate_pct thresholds (<=, low is bad)
    def test_next_step_0_30_adds_45(self):
        score = self.engine.assess(make_input(
            next_step_confirmed_rate_pct=0.30,
            repeat_meeting_same_stage_rate_pct=0.05,
            meeting_to_pipeline_velocity_days=1.0,
        )).advancement_score
        assert score == 45.0

    def test_next_step_0_31_not_top_band(self):
        score = self.engine.assess(make_input(
            next_step_confirmed_rate_pct=0.31,
            repeat_meeting_same_stage_rate_pct=0.05,
            meeting_to_pipeline_velocity_days=1.0,
        )).advancement_score
        assert score < 45.0

    def test_next_step_0_55_adds_25(self):
        score = self.engine.assess(make_input(
            next_step_confirmed_rate_pct=0.55,
            repeat_meeting_same_stage_rate_pct=0.05,
            meeting_to_pipeline_velocity_days=1.0,
        )).advancement_score
        assert score == 25.0

    def test_next_step_0_56_not_middle_band(self):
        score = self.engine.assess(make_input(
            next_step_confirmed_rate_pct=0.56,
            repeat_meeting_same_stage_rate_pct=0.05,
            meeting_to_pipeline_velocity_days=1.0,
        )).advancement_score
        assert score < 25.0

    def test_next_step_0_75_adds_10(self):
        score = self.engine.assess(make_input(
            next_step_confirmed_rate_pct=0.75,
            repeat_meeting_same_stage_rate_pct=0.05,
            meeting_to_pipeline_velocity_days=1.0,
        )).advancement_score
        assert score == 10.0

    def test_next_step_0_76_adds_0(self):
        score = self.engine.assess(make_input(
            next_step_confirmed_rate_pct=0.76,
            repeat_meeting_same_stage_rate_pct=0.05,
            meeting_to_pipeline_velocity_days=1.0,
        )).advancement_score
        assert score == 0.0

    # repeat_meeting_same_stage_rate_pct thresholds (>=, high is bad)
    def test_repeat_0_45_adds_30(self):
        score = self.engine.assess(make_input(
            next_step_confirmed_rate_pct=0.90,
            repeat_meeting_same_stage_rate_pct=0.45,
            meeting_to_pipeline_velocity_days=1.0,
        )).advancement_score
        assert score == 30.0

    def test_repeat_0_44_not_top_band(self):
        score = self.engine.assess(make_input(
            next_step_confirmed_rate_pct=0.90,
            repeat_meeting_same_stage_rate_pct=0.44,
            meeting_to_pipeline_velocity_days=1.0,
        )).advancement_score
        assert score < 30.0

    def test_repeat_0_25_adds_15(self):
        score = self.engine.assess(make_input(
            next_step_confirmed_rate_pct=0.90,
            repeat_meeting_same_stage_rate_pct=0.25,
            meeting_to_pipeline_velocity_days=1.0,
        )).advancement_score
        assert score == 15.0

    def test_repeat_0_24_adds_0(self):
        score = self.engine.assess(make_input(
            next_step_confirmed_rate_pct=0.90,
            repeat_meeting_same_stage_rate_pct=0.24,
            meeting_to_pipeline_velocity_days=1.0,
        )).advancement_score
        assert score == 0.0

    # meeting_to_pipeline_velocity_days thresholds (>=, slow is bad)
    def test_velocity_21_days_adds_25(self):
        score = self.engine.assess(make_input(
            next_step_confirmed_rate_pct=0.90,
            repeat_meeting_same_stage_rate_pct=0.05,
            meeting_to_pipeline_velocity_days=21.0,
        )).advancement_score
        assert score == 25.0

    def test_velocity_20_days_not_top_band(self):
        score = self.engine.assess(make_input(
            next_step_confirmed_rate_pct=0.90,
            repeat_meeting_same_stage_rate_pct=0.05,
            meeting_to_pipeline_velocity_days=20.0,
        )).advancement_score
        assert score < 25.0

    def test_velocity_12_days_adds_12(self):
        score = self.engine.assess(make_input(
            next_step_confirmed_rate_pct=0.90,
            repeat_meeting_same_stage_rate_pct=0.05,
            meeting_to_pipeline_velocity_days=12.0,
        )).advancement_score
        assert score == 12.0

    def test_velocity_11_days_adds_0(self):
        score = self.engine.assess(make_input(
            next_step_confirmed_rate_pct=0.90,
            repeat_meeting_same_stage_rate_pct=0.05,
            meeting_to_pipeline_velocity_days=11.0,
        )).advancement_score
        assert score == 0.0

    def test_all_worst_inputs_produce_100_advancement(self):
        # 45+30+25=100 capped at 100
        score = self.engine.assess(make_input(
            next_step_confirmed_rate_pct=0.10,
            repeat_meeting_same_stage_rate_pct=0.60,
            meeting_to_pipeline_velocity_days=30.0,
        )).advancement_score
        assert score == 100.0

    def test_all_good_inputs_produce_0_advancement(self):
        score = self.engine.assess(make_input(
            next_step_confirmed_rate_pct=0.90,
            repeat_meeting_same_stage_rate_pct=0.05,
            meeting_to_pipeline_velocity_days=1.0,
        )).advancement_score
        assert score == 0.0

    def test_advancement_score_never_exceeds_100(self):
        score = self.engine.assess(make_input(
            next_step_confirmed_rate_pct=0.01,
            repeat_meeting_same_stage_rate_pct=0.99,
            meeting_to_pipeline_velocity_days=99.0,
        )).advancement_score
        assert score <= 100.0

    def test_advancement_score_is_float(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.advancement_score, float)

    def test_next_step_0_55_repeat_0_25_velocity_12_sums_to_52(self):
        score = self.engine.assess(make_input(
            next_step_confirmed_rate_pct=0.55,
            repeat_meeting_same_stage_rate_pct=0.25,
            meeting_to_pipeline_velocity_days=12.0,
        )).advancement_score
        # 25 + 15 + 12 = 52
        assert score == 52.0

    def test_next_step_0_30_repeat_0_45_velocity_21_sums_to_100(self):
        score = self.engine.assess(make_input(
            next_step_confirmed_rate_pct=0.30,
            repeat_meeting_same_stage_rate_pct=0.45,
            meeting_to_pipeline_velocity_days=21.0,
        )).advancement_score
        # 45 + 30 + 25 = 100
        assert score == 100.0


# ─── TestComposite ────────────────────────────────────────────────────────────

class TestComposite:
    """
    composite = round(co*0.30 + qu*0.25 + ex*0.20 + ad*0.25, 2), capped at 100.
    """

    def setup_method(self):
        self.engine = SalesMeetingQualityConversionIntelligenceEngine()

    def test_conversion_weight_is_0_30(self):
        # co=100, qu=0, ex=0, ad=0 → composite = 100*0.30 = 30.0
        result = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.10,
            demo_to_proposal_rate_pct=0.10,
            proposal_to_close_rate_pct=0.10,
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.90,
            multi_stakeholder_meeting_rate_pct=0.90,
            no_show_rate_pct=0.01,
            reschedule_rate_pct=0.01,
            meeting_notes_completion_rate_pct=0.90,
            next_step_confirmed_rate_pct=0.90,
            repeat_meeting_same_stage_rate_pct=0.01,
            meeting_to_pipeline_velocity_days=1.0,
        ))
        assert result.conversion_score == 100.0
        assert result.quality_score == 0.0
        assert result.execution_score == 0.0
        assert result.advancement_score == 0.0
        assert result.meeting_composite == pytest.approx(30.0, abs=0.01)

    def test_quality_weight_is_0_25(self):
        # co=0, qu=100, ex=0, ad=0 → composite = 100*0.25 = 25.0
        result = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.90,
            demo_to_proposal_rate_pct=0.90,
            proposal_to_close_rate_pct=0.90,
            discovery_completion_rate_pct=0.10,
            pain_identified_rate_pct=0.10,
            multi_stakeholder_meeting_rate_pct=0.10,
            no_show_rate_pct=0.01,
            reschedule_rate_pct=0.01,
            meeting_notes_completion_rate_pct=0.90,
            next_step_confirmed_rate_pct=0.90,
            repeat_meeting_same_stage_rate_pct=0.01,
            meeting_to_pipeline_velocity_days=1.0,
        ))
        assert result.conversion_score == 0.0
        assert result.quality_score == 100.0
        assert result.execution_score == 0.0
        assert result.advancement_score == 0.0
        assert result.meeting_composite == pytest.approx(25.0, abs=0.01)

    def test_execution_weight_is_0_20(self):
        # co=0, qu=0, ex=100, ad=0 → composite = 100*0.20 = 20.0
        result = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.90,
            demo_to_proposal_rate_pct=0.90,
            proposal_to_close_rate_pct=0.90,
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.90,
            multi_stakeholder_meeting_rate_pct=0.90,
            no_show_rate_pct=0.50,
            reschedule_rate_pct=0.60,
            meeting_notes_completion_rate_pct=0.10,
            next_step_confirmed_rate_pct=0.90,
            repeat_meeting_same_stage_rate_pct=0.01,
            meeting_to_pipeline_velocity_days=1.0,
        ))
        assert result.conversion_score == 0.0
        assert result.quality_score == 0.0
        assert result.execution_score == 100.0
        assert result.advancement_score == 0.0
        assert result.meeting_composite == pytest.approx(20.0, abs=0.01)

    def test_advancement_weight_is_0_25(self):
        # co=0, qu=0, ex=0, ad=100 → composite = 100*0.25 = 25.0
        result = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.90,
            demo_to_proposal_rate_pct=0.90,
            proposal_to_close_rate_pct=0.90,
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.90,
            multi_stakeholder_meeting_rate_pct=0.90,
            no_show_rate_pct=0.01,
            reschedule_rate_pct=0.01,
            meeting_notes_completion_rate_pct=0.90,
            next_step_confirmed_rate_pct=0.10,
            repeat_meeting_same_stage_rate_pct=0.60,
            meeting_to_pipeline_velocity_days=30.0,
        ))
        assert result.conversion_score == 0.0
        assert result.quality_score == 0.0
        assert result.execution_score == 0.0
        assert result.advancement_score == 100.0
        assert result.meeting_composite == pytest.approx(25.0, abs=0.01)

    def test_all_100_produces_composite_100(self):
        result = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.10,
            demo_to_proposal_rate_pct=0.10,
            proposal_to_close_rate_pct=0.10,
            discovery_completion_rate_pct=0.10,
            pain_identified_rate_pct=0.10,
            multi_stakeholder_meeting_rate_pct=0.10,
            no_show_rate_pct=0.50,
            reschedule_rate_pct=0.60,
            meeting_notes_completion_rate_pct=0.10,
            next_step_confirmed_rate_pct=0.10,
            repeat_meeting_same_stage_rate_pct=0.60,
            meeting_to_pipeline_velocity_days=30.0,
        ))
        assert result.meeting_composite == pytest.approx(100.0, abs=0.01)

    def test_all_0_produces_composite_0(self):
        result = self.engine.assess(make_input())
        assert result.meeting_composite == pytest.approx(0.0, abs=0.01)

    def test_composite_co_40_weight_gives_12(self):
        # co=40 (mto=0.20 +40, demo>0.25, close>0.30 → +0+0 = 40), qu=0, ex=0, ad=0 → 40*0.30=12.0
        result = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.20,
            demo_to_proposal_rate_pct=0.80,
            proposal_to_close_rate_pct=0.50,
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.90,
            multi_stakeholder_meeting_rate_pct=0.90,
            no_show_rate_pct=0.01,
            reschedule_rate_pct=0.01,
            meeting_notes_completion_rate_pct=0.90,
            next_step_confirmed_rate_pct=0.90,
            repeat_meeting_same_stage_rate_pct=0.01,
            meeting_to_pipeline_velocity_days=1.0,
        ))
        assert result.conversion_score == 40.0
        assert result.meeting_composite == pytest.approx(12.0, abs=0.01)

    def test_composite_never_exceeds_100(self):
        result = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.01,
            demo_to_proposal_rate_pct=0.01,
            proposal_to_close_rate_pct=0.01,
            discovery_completion_rate_pct=0.01,
            pain_identified_rate_pct=0.01,
            multi_stakeholder_meeting_rate_pct=0.01,
            no_show_rate_pct=1.00,
            reschedule_rate_pct=1.00,
            meeting_notes_completion_rate_pct=0.01,
            next_step_confirmed_rate_pct=0.01,
            repeat_meeting_same_stage_rate_pct=1.00,
            meeting_to_pipeline_velocity_days=100.0,
        ))
        assert result.meeting_composite <= 100.0

    def test_composite_co_and_ad_both_100(self):
        # co=100 (weight 0.30) + ad=100 (weight 0.25) → 55.0, qu=0, ex=0
        result = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.10,
            demo_to_proposal_rate_pct=0.10,
            proposal_to_close_rate_pct=0.10,
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.90,
            multi_stakeholder_meeting_rate_pct=0.90,
            no_show_rate_pct=0.01,
            reschedule_rate_pct=0.01,
            meeting_notes_completion_rate_pct=0.90,
            next_step_confirmed_rate_pct=0.10,
            repeat_meeting_same_stage_rate_pct=0.60,
            meeting_to_pipeline_velocity_days=30.0,
        ))
        assert result.conversion_score == 100.0
        assert result.advancement_score == 100.0
        assert result.meeting_composite == pytest.approx(55.0, abs=0.01)

    def test_composite_is_float(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.meeting_composite, float)

    def test_composite_rounded_to_2_decimal_places(self):
        # Verify the rounded value equals round(..., 2)
        result = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.40,
            demo_to_proposal_rate_pct=0.50,
            proposal_to_close_rate_pct=0.30,
            discovery_completion_rate_pct=0.55,
            pain_identified_rate_pct=0.55,
            multi_stakeholder_meeting_rate_pct=0.40,
            no_show_rate_pct=0.18,
            reschedule_rate_pct=0.22,
            meeting_notes_completion_rate_pct=0.55,
            next_step_confirmed_rate_pct=0.55,
            repeat_meeting_same_stage_rate_pct=0.25,
            meeting_to_pipeline_velocity_days=12.0,
        ))
        # co=22+18+12=52, qu=22+18+12=52, ex=22+18+12=52, ad=25+15+12=52
        # composite = round(52*0.30 + 52*0.25 + 52*0.20 + 52*0.25, 2) = round(52.0, 2) = 52.0
        co, qu, ex, ad = 52.0, 52.0, 52.0, 52.0
        expected = round(co * 0.30 + qu * 0.25 + ex * 0.20 + ad * 0.25, 2)
        assert result.meeting_composite == pytest.approx(expected, abs=0.01)


# ─── TestPattern ──────────────────────────────────────────────────────────────

class TestPattern:
    def setup_method(self):
        self.engine = SalesMeetingQualityConversionIntelligenceEngine()

    def _pattern(self, **overrides) -> MeetingPattern:
        return self.engine.assess(make_input(**overrides)).meeting_pattern

    def test_calendar_stuffing_exact_boundary(self):
        pattern = self._pattern(
            meetings_to_opportunity_rate_pct=0.20,
            total_meetings_held=15,
        )
        assert pattern == MeetingPattern.calendar_stuffing

    def test_calendar_stuffing_low_rate_high_meetings(self):
        pattern = self._pattern(
            meetings_to_opportunity_rate_pct=0.10,
            total_meetings_held=20,
        )
        assert pattern == MeetingPattern.calendar_stuffing

    def test_calendar_stuffing_fails_if_rate_too_high(self):
        pattern = self._pattern(
            meetings_to_opportunity_rate_pct=0.21,
            total_meetings_held=20,
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.90,
            next_step_confirmed_rate_pct=0.90,
            repeat_meeting_same_stage_rate_pct=0.05,
            no_show_rate_pct=0.01,
            reschedule_rate_pct=0.01,
            demo_to_proposal_rate_pct=0.80,
        )
        assert pattern != MeetingPattern.calendar_stuffing

    def test_calendar_stuffing_fails_if_meetings_too_few(self):
        pattern = self._pattern(
            meetings_to_opportunity_rate_pct=0.10,
            total_meetings_held=14,
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.90,
            next_step_confirmed_rate_pct=0.90,
            repeat_meeting_same_stage_rate_pct=0.05,
            no_show_rate_pct=0.01,
            reschedule_rate_pct=0.01,
            demo_to_proposal_rate_pct=0.80,
        )
        assert pattern != MeetingPattern.calendar_stuffing

    def test_discovery_skipper_exact_boundary(self):
        pattern = self._pattern(
            meetings_to_opportunity_rate_pct=0.80,
            total_meetings_held=10,
            discovery_completion_rate_pct=0.30,
            pain_identified_rate_pct=0.35,
        )
        assert pattern == MeetingPattern.discovery_skipper

    def test_discovery_skipper_deep_in_range(self):
        pattern = self._pattern(
            meetings_to_opportunity_rate_pct=0.80,
            total_meetings_held=10,
            discovery_completion_rate_pct=0.10,
            pain_identified_rate_pct=0.10,
        )
        assert pattern == MeetingPattern.discovery_skipper

    def test_discovery_skipper_fails_if_discovery_too_high(self):
        pattern = self._pattern(
            meetings_to_opportunity_rate_pct=0.80,
            total_meetings_held=10,
            discovery_completion_rate_pct=0.31,
            pain_identified_rate_pct=0.30,
            next_step_confirmed_rate_pct=0.90,
            repeat_meeting_same_stage_rate_pct=0.05,
            no_show_rate_pct=0.01,
            reschedule_rate_pct=0.01,
            demo_to_proposal_rate_pct=0.80,
        )
        assert pattern != MeetingPattern.discovery_skipper

    def test_discovery_skipper_fails_if_pain_too_high(self):
        pattern = self._pattern(
            meetings_to_opportunity_rate_pct=0.80,
            total_meetings_held=10,
            discovery_completion_rate_pct=0.30,
            pain_identified_rate_pct=0.36,
            next_step_confirmed_rate_pct=0.90,
            repeat_meeting_same_stage_rate_pct=0.05,
            no_show_rate_pct=0.01,
            reschedule_rate_pct=0.01,
            demo_to_proposal_rate_pct=0.80,
        )
        assert pattern != MeetingPattern.discovery_skipper

    def test_next_step_avoider_exact_boundary(self):
        pattern = self._pattern(
            meetings_to_opportunity_rate_pct=0.80,
            total_meetings_held=10,
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.90,
            next_step_confirmed_rate_pct=0.25,
            repeat_meeting_same_stage_rate_pct=0.40,
        )
        assert pattern == MeetingPattern.next_step_avoider

    def test_next_step_avoider_fails_if_next_step_too_high(self):
        pattern = self._pattern(
            meetings_to_opportunity_rate_pct=0.80,
            total_meetings_held=10,
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.90,
            next_step_confirmed_rate_pct=0.26,
            repeat_meeting_same_stage_rate_pct=0.50,
            no_show_rate_pct=0.01,
            reschedule_rate_pct=0.01,
            demo_to_proposal_rate_pct=0.80,
        )
        assert pattern != MeetingPattern.next_step_avoider

    def test_next_step_avoider_fails_if_repeat_too_low(self):
        pattern = self._pattern(
            meetings_to_opportunity_rate_pct=0.80,
            total_meetings_held=10,
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.90,
            next_step_confirmed_rate_pct=0.25,
            repeat_meeting_same_stage_rate_pct=0.39,
            no_show_rate_pct=0.01,
            reschedule_rate_pct=0.01,
            demo_to_proposal_rate_pct=0.80,
        )
        assert pattern != MeetingPattern.next_step_avoider

    def test_phantom_meeting_maker_exact_boundary(self):
        pattern = self._pattern(
            meetings_to_opportunity_rate_pct=0.80,
            total_meetings_held=10,
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.90,
            next_step_confirmed_rate_pct=0.90,
            repeat_meeting_same_stage_rate_pct=0.05,
            no_show_rate_pct=0.25,
            reschedule_rate_pct=0.30,
        )
        assert pattern == MeetingPattern.phantom_meeting_maker

    def test_phantom_meeting_maker_fails_if_no_show_too_low(self):
        pattern = self._pattern(
            meetings_to_opportunity_rate_pct=0.80,
            total_meetings_held=10,
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.90,
            next_step_confirmed_rate_pct=0.90,
            repeat_meeting_same_stage_rate_pct=0.05,
            no_show_rate_pct=0.24,
            reschedule_rate_pct=0.50,
            demo_to_proposal_rate_pct=0.80,
        )
        assert pattern != MeetingPattern.phantom_meeting_maker

    def test_phantom_meeting_maker_fails_if_reschedule_too_low(self):
        pattern = self._pattern(
            meetings_to_opportunity_rate_pct=0.80,
            total_meetings_held=10,
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.90,
            next_step_confirmed_rate_pct=0.90,
            repeat_meeting_same_stage_rate_pct=0.05,
            no_show_rate_pct=0.30,
            reschedule_rate_pct=0.29,
            demo_to_proposal_rate_pct=0.80,
        )
        assert pattern != MeetingPattern.phantom_meeting_maker

    def test_demo_looper_exact_boundary(self):
        pattern = self._pattern(
            meetings_to_opportunity_rate_pct=0.80,
            total_meetings_held=10,
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.90,
            next_step_confirmed_rate_pct=0.90,
            repeat_meeting_same_stage_rate_pct=0.35,
            no_show_rate_pct=0.01,
            reschedule_rate_pct=0.01,
            demo_to_proposal_rate_pct=0.20,
        )
        assert pattern == MeetingPattern.demo_looper

    def test_demo_looper_fails_if_demo_rate_too_high(self):
        pattern = self._pattern(
            meetings_to_opportunity_rate_pct=0.80,
            total_meetings_held=10,
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.90,
            next_step_confirmed_rate_pct=0.90,
            repeat_meeting_same_stage_rate_pct=0.50,
            no_show_rate_pct=0.01,
            reschedule_rate_pct=0.01,
            demo_to_proposal_rate_pct=0.21,
        )
        assert pattern != MeetingPattern.demo_looper

    def test_demo_looper_fails_if_repeat_too_low(self):
        pattern = self._pattern(
            meetings_to_opportunity_rate_pct=0.80,
            total_meetings_held=10,
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.90,
            next_step_confirmed_rate_pct=0.90,
            repeat_meeting_same_stage_rate_pct=0.34,
            no_show_rate_pct=0.01,
            reschedule_rate_pct=0.01,
            demo_to_proposal_rate_pct=0.15,
        )
        assert pattern != MeetingPattern.demo_looper

    def test_none_when_no_conditions_met(self):
        pattern = self._pattern()
        assert pattern == MeetingPattern.none

    def test_pattern_is_meeting_pattern_instance(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.meeting_pattern, MeetingPattern)


# ─── TestPatternPriority ──────────────────────────────────────────────────────

class TestPatternPriority:
    """calendar_stuffing is checked first and wins when conditions overlap."""

    def setup_method(self):
        self.engine = SalesMeetingQualityConversionIntelligenceEngine()

    def test_calendar_stuffing_beats_discovery_skipper(self):
        result = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.20,
            total_meetings_held=15,
            discovery_completion_rate_pct=0.30,
            pain_identified_rate_pct=0.35,
        ))
        assert result.meeting_pattern == MeetingPattern.calendar_stuffing

    def test_calendar_stuffing_beats_next_step_avoider(self):
        result = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.20,
            total_meetings_held=15,
            next_step_confirmed_rate_pct=0.25,
            repeat_meeting_same_stage_rate_pct=0.40,
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.90,
        ))
        assert result.meeting_pattern == MeetingPattern.calendar_stuffing

    def test_calendar_stuffing_beats_phantom_meeting_maker(self):
        result = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.20,
            total_meetings_held=15,
            no_show_rate_pct=0.25,
            reschedule_rate_pct=0.30,
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.90,
            next_step_confirmed_rate_pct=0.90,
            repeat_meeting_same_stage_rate_pct=0.05,
        ))
        assert result.meeting_pattern == MeetingPattern.calendar_stuffing

    def test_calendar_stuffing_beats_demo_looper(self):
        result = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.20,
            total_meetings_held=15,
            demo_to_proposal_rate_pct=0.20,
            repeat_meeting_same_stage_rate_pct=0.35,
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.90,
            next_step_confirmed_rate_pct=0.90,
            no_show_rate_pct=0.01,
            reschedule_rate_pct=0.01,
        ))
        assert result.meeting_pattern == MeetingPattern.calendar_stuffing

    def test_discovery_skipper_beats_next_step_avoider(self):
        result = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.80,
            total_meetings_held=10,
            discovery_completion_rate_pct=0.30,
            pain_identified_rate_pct=0.35,
            next_step_confirmed_rate_pct=0.25,
            repeat_meeting_same_stage_rate_pct=0.40,
        ))
        assert result.meeting_pattern == MeetingPattern.discovery_skipper

    def test_discovery_skipper_beats_phantom_meeting_maker(self):
        result = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.80,
            total_meetings_held=10,
            discovery_completion_rate_pct=0.30,
            pain_identified_rate_pct=0.35,
            next_step_confirmed_rate_pct=0.90,
            repeat_meeting_same_stage_rate_pct=0.05,
            no_show_rate_pct=0.25,
            reschedule_rate_pct=0.30,
        ))
        assert result.meeting_pattern == MeetingPattern.discovery_skipper

    def test_discovery_skipper_beats_demo_looper(self):
        result = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.80,
            total_meetings_held=10,
            discovery_completion_rate_pct=0.30,
            pain_identified_rate_pct=0.35,
            next_step_confirmed_rate_pct=0.90,
            repeat_meeting_same_stage_rate_pct=0.35,
            no_show_rate_pct=0.01,
            reschedule_rate_pct=0.01,
            demo_to_proposal_rate_pct=0.20,
        ))
        assert result.meeting_pattern == MeetingPattern.discovery_skipper

    def test_next_step_avoider_beats_phantom_meeting_maker(self):
        result = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.80,
            total_meetings_held=10,
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.90,
            next_step_confirmed_rate_pct=0.25,
            repeat_meeting_same_stage_rate_pct=0.40,
            no_show_rate_pct=0.25,
            reschedule_rate_pct=0.30,
        ))
        assert result.meeting_pattern == MeetingPattern.next_step_avoider

    def test_next_step_avoider_beats_demo_looper(self):
        result = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.80,
            total_meetings_held=10,
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.90,
            next_step_confirmed_rate_pct=0.25,
            repeat_meeting_same_stage_rate_pct=0.40,
            no_show_rate_pct=0.01,
            reschedule_rate_pct=0.01,
            demo_to_proposal_rate_pct=0.20,
        ))
        assert result.meeting_pattern == MeetingPattern.next_step_avoider

    def test_phantom_meeting_maker_beats_demo_looper(self):
        result = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.80,
            total_meetings_held=10,
            discovery_completion_rate_pct=0.90,
            pain_identified_rate_pct=0.90,
            next_step_confirmed_rate_pct=0.90,
            repeat_meeting_same_stage_rate_pct=0.35,
            no_show_rate_pct=0.25,
            reschedule_rate_pct=0.30,
            demo_to_proposal_rate_pct=0.20,
        ))
        assert result.meeting_pattern == MeetingPattern.phantom_meeting_maker


# ─── TestRisk ─────────────────────────────────────────────────────────────────

class TestRisk:
    def setup_method(self):
        self.engine = SalesMeetingQualityConversionIntelligenceEngine()

    def test_risk_critical_at_exactly_60(self):
        assert self.engine._risk(60.0) == MeetingRisk.critical

    def test_risk_critical_above_60(self):
        assert self.engine._risk(75.0) == MeetingRisk.critical

    def test_risk_critical_at_100(self):
        assert self.engine._risk(100.0) == MeetingRisk.critical

    def test_risk_high_at_exactly_40(self):
        assert self.engine._risk(40.0) == MeetingRisk.high

    def test_risk_high_between_40_and_60(self):
        assert self.engine._risk(50.0) == MeetingRisk.high

    def test_risk_high_at_59(self):
        assert self.engine._risk(59.9) == MeetingRisk.high

    def test_risk_moderate_at_exactly_20(self):
        assert self.engine._risk(20.0) == MeetingRisk.moderate

    def test_risk_moderate_between_20_and_40(self):
        assert self.engine._risk(30.0) == MeetingRisk.moderate

    def test_risk_moderate_at_39(self):
        assert self.engine._risk(39.9) == MeetingRisk.moderate

    def test_risk_low_at_0(self):
        assert self.engine._risk(0.0) == MeetingRisk.low

    def test_risk_low_below_20(self):
        assert self.engine._risk(15.0) == MeetingRisk.low

    def test_risk_low_at_19(self):
        assert self.engine._risk(19.9) == MeetingRisk.low

    def test_assess_returns_correct_risk_low(self):
        result = self.engine.assess(make_input())
        assert result.meeting_risk == MeetingRisk.low

    def test_assess_returns_correct_risk_critical(self):
        result = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.10,
            demo_to_proposal_rate_pct=0.10,
            proposal_to_close_rate_pct=0.10,
            discovery_completion_rate_pct=0.10,
            pain_identified_rate_pct=0.10,
            multi_stakeholder_meeting_rate_pct=0.10,
            no_show_rate_pct=0.50,
            reschedule_rate_pct=0.60,
            meeting_notes_completion_rate_pct=0.10,
            next_step_confirmed_rate_pct=0.10,
            repeat_meeting_same_stage_rate_pct=0.60,
            meeting_to_pipeline_velocity_days=30.0,
        ))
        assert result.meeting_risk == MeetingRisk.critical

    def test_risk_is_meeting_risk_instance(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.meeting_risk, MeetingRisk)

    def test_boundary_just_below_60_is_high(self):
        assert self.engine._risk(59.99) == MeetingRisk.high

    def test_boundary_just_below_40_is_moderate(self):
        assert self.engine._risk(39.99) == MeetingRisk.moderate

    def test_boundary_just_below_20_is_low(self):
        assert self.engine._risk(19.99) == MeetingRisk.low


# ─── TestSeverity ─────────────────────────────────────────────────────────────

class TestSeverity:
    def setup_method(self):
        self.engine = SalesMeetingQualityConversionIntelligenceEngine()

    def test_severity_collapsing_at_exactly_60(self):
        assert self.engine._severity(60.0) == MeetingSeverity.collapsing

    def test_severity_collapsing_above_60(self):
        assert self.engine._severity(80.0) == MeetingSeverity.collapsing

    def test_severity_collapsing_at_100(self):
        assert self.engine._severity(100.0) == MeetingSeverity.collapsing

    def test_severity_stalling_at_exactly_40(self):
        assert self.engine._severity(40.0) == MeetingSeverity.stalling

    def test_severity_stalling_between_40_and_60(self):
        assert self.engine._severity(50.0) == MeetingSeverity.stalling

    def test_severity_stalling_at_59(self):
        assert self.engine._severity(59.9) == MeetingSeverity.stalling

    def test_severity_slipping_at_exactly_20(self):
        assert self.engine._severity(20.0) == MeetingSeverity.slipping

    def test_severity_slipping_between_20_and_40(self):
        assert self.engine._severity(30.0) == MeetingSeverity.slipping

    def test_severity_slipping_at_39(self):
        assert self.engine._severity(39.9) == MeetingSeverity.slipping

    def test_severity_converting_at_0(self):
        assert self.engine._severity(0.0) == MeetingSeverity.converting

    def test_severity_converting_below_20(self):
        assert self.engine._severity(10.0) == MeetingSeverity.converting

    def test_severity_converting_at_19(self):
        assert self.engine._severity(19.9) == MeetingSeverity.converting

    def test_assess_returns_converting_for_low_composite(self):
        result = self.engine.assess(make_input())
        assert result.meeting_severity == MeetingSeverity.converting

    def test_assess_returns_collapsing_for_high_composite(self):
        result = self.engine.assess(make_input(
            meetings_to_opportunity_rate_pct=0.10,
            demo_to_proposal_rate_pct=0.10,
            proposal_to_close_rate_pct=0.10,
            discovery_completion_rate_pct=0.10,
            pain_identified_rate_pct=0.10,
            multi_stakeholder_meeting_rate_pct=0.10,
            no_show_rate_pct=0.50,
            reschedule_rate_pct=0.60,
            meeting_notes_completion_rate_pct=0.10,
            next_step_confirmed_rate_pct=0.10,
            repeat_meeting_same_stage_rate_pct=0.60,
            meeting_to_pipeline_velocity_days=30.0,
        ))
        assert result.meeting_severity == MeetingSeverity.collapsing

    def test_severity_is_meeting_severity_instance(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.meeting_severity, MeetingSeverity)

    def test_boundary_just_below_60_is_stalling(self):
        assert self.engine._severity(59.99) == MeetingSeverity.stalling

    def test_boundary_just_below_40_is_slipping(self):
        assert self.engine._severity(39.99) == MeetingSeverity.slipping

    def test_boundary_just_below_20_is_converting(self):
        assert self.engine._severity(19.99) == MeetingSeverity.converting

    def test_risk_and_severity_thresholds_are_consistent(self):
        # Risk and severity share the same composite thresholds
        cases = [
            (0.0,   MeetingRisk.low,      MeetingSeverity.converting),
            (19.9,  MeetingRisk.low,      MeetingSeverity.converting),
            (20.0,  MeetingRisk.moderate, MeetingSeverity.slipping),
            (39.9,  MeetingRisk.moderate, MeetingSeverity.slipping),
            (40.0,  MeetingRisk.high,     MeetingSeverity.stalling),
            (59.9,  MeetingRisk.high,     MeetingSeverity.stalling),
            (60.0,  MeetingRisk.critical, MeetingSeverity.collapsing),
            (100.0, MeetingRisk.critical, MeetingSeverity.collapsing),
        ]
        for composite, expected_risk, expected_severity in cases:
            assert self.engine._risk(composite) == expected_risk, (
                f"risk mismatch at composite={composite}"
            )
            assert self.engine._severity(composite) == expected_severity, (
                f"severity mismatch at composite={composite}"
            )
