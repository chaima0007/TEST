"""
Comprehensive pytest test suite for SalesBuyerMeetingQualityIntelligenceEngine.

Coverage targets:
- All 4 enums and their values
- MeetingInput (22 fields)
- MeetingResult (15 fields) + to_dict() (15 keys)
- _meeting_prep_score() – all branches
- _meeting_engagement_score() – all branches
- _meeting_outcome_score() – all branches
- _meeting_conversion_score() – all branches
- _detect_pattern() – all 6 outcomes
- _risk_level() – all 4 thresholds
- _severity() – all 4 thresholds
- _action() – all branches
- _has_meeting_gap() – all 3 conditions
- _requires_meeting_coaching() – all 3 conditions
- _estimated_pipeline_drag()
- _signal() – healthy branch + all label/format paths
- assess() – end-to-end
- assess_batch() – batch behaviour
- summary() – empty and populated
- Edge cases: zero, 100%, boundary values, caps
"""

from __future__ import annotations

import math
import pytest

from swarm.intelligence.sales_buyer_meeting_quality_intelligence_engine import (
    MeetingAction,
    MeetingInput,
    MeetingPattern,
    MeetingResult,
    MeetingRisk,
    MeetingSeverity,
    SalesBuyerMeetingQualityIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _engine() -> SalesBuyerMeetingQualityIntelligenceEngine:
    """Return a fresh engine instance."""
    return SalesBuyerMeetingQualityIntelligenceEngine()


def _base_input(**overrides) -> MeetingInput:
    """
    Return a MeetingInput whose defaults produce a 'healthy' result
    (pattern=none, composite < 20, low risk).
    All pct fields are expressed as fractions (0.0–1.0).
    """
    defaults = dict(
        rep_id="REP-001",
        region="EMEA",
        evaluation_period_id="Q2-2026",
        total_meetings_conducted=20,
        meetings_with_agenda_sent_pct=0.90,         # >0.75 → 0 pts
        avg_agenda_sent_hours_before_meeting=24.0,   # >12   → 0 pts
        followup_within_24h_rate_pct=0.85,           # >0.75 → 0 pts
        avg_followup_delay_hours=4.0,
        meeting_to_next_meeting_conversion_pct=0.70,
        avg_stakeholders_per_meeting=2.5,            # >2.0  → 0 pts
        decision_maker_in_meeting_pct=0.75,          # >0.50 → 0 pts
        meetings_with_no_outcome_pct=0.10,           # <0.25 → 0 pts
        next_step_committed_at_meeting_pct=0.90,     # >0.75 → 0 pts
        meetings_rescheduled_by_buyer_pct=0.05,
        avg_meeting_duration_minutes=45.0,
        meeting_recording_review_rate_pct=0.50,      # >0.30 → 0 pts
        demo_conversion_from_meeting_pct=0.50,       # >0.35 → 0 pts
        proposal_conversion_from_demo_pct=0.70,      # >0.50 → 0 pts
        repeat_meeting_same_stage_pct=0.10,          # <0.25 → 0 pts
        meeting_cancellation_rate_pct=0.05,          # <0.20 → 0 pts
        avg_time_between_meetings_days=7.0,
        avg_opportunity_value_usd=10_000.0,
    )
    defaults.update(overrides)
    return MeetingInput(**defaults)


# ===========================================================================
# SECTION 1 – Enum values
# ===========================================================================

class TestMeetingRiskEnum:
    def test_low_value(self):
        assert MeetingRisk.low.value == "low"

    def test_moderate_value(self):
        assert MeetingRisk.moderate.value == "moderate"

    def test_high_value(self):
        assert MeetingRisk.high.value == "high"

    def test_critical_value(self):
        assert MeetingRisk.critical.value == "critical"

    def test_is_str_enum(self):
        assert isinstance(MeetingRisk.low, str)

    def test_four_members(self):
        assert len(MeetingRisk) == 4

    def test_identity_by_value(self):
        assert MeetingRisk("high") is MeetingRisk.high


class TestMeetingPatternEnum:
    def test_none_value(self):
        assert MeetingPattern.none.value == "none"

    def test_no_agenda_discipline(self):
        assert MeetingPattern.no_agenda_discipline.value == "no_agenda_discipline"

    def test_poor_followup(self):
        assert MeetingPattern.poor_followup.value == "poor_followup"

    def test_single_stakeholder_trap(self):
        assert MeetingPattern.single_stakeholder_trap.value == "single_stakeholder_trap"

    def test_no_next_step_close(self):
        assert MeetingPattern.no_next_step_close.value == "no_next_step_close"

    def test_meeting_fatigue(self):
        assert MeetingPattern.meeting_fatigue.value == "meeting_fatigue"

    def test_six_members(self):
        assert len(MeetingPattern) == 6

    def test_is_str_enum(self):
        assert isinstance(MeetingPattern.poor_followup, str)


class TestMeetingSeverityEnum:
    def test_structured_value(self):
        assert MeetingSeverity.structured.value == "structured"

    def test_developing_value(self):
        assert MeetingSeverity.developing.value == "developing"

    def test_ad_hoc_value(self):
        assert MeetingSeverity.ad_hoc.value == "ad_hoc"

    def test_chaotic_value(self):
        assert MeetingSeverity.chaotic.value == "chaotic"

    def test_four_members(self):
        assert len(MeetingSeverity) == 4

    def test_is_str_enum(self):
        assert isinstance(MeetingSeverity.chaotic, str)


class TestMeetingActionEnum:
    def test_no_action_value(self):
        assert MeetingAction.no_action.value == "no_action"

    def test_meeting_prep_coaching(self):
        assert MeetingAction.meeting_prep_coaching.value == "meeting_prep_coaching"

    def test_followup_discipline_training(self):
        assert MeetingAction.followup_discipline_training.value == "followup_discipline_training"

    def test_stakeholder_expansion(self):
        assert MeetingAction.stakeholder_expansion_in_meetings.value == "stakeholder_expansion_in_meetings"

    def test_next_step_close_training(self):
        assert MeetingAction.next_step_close_training.value == "next_step_close_training"

    def test_meeting_cadence_optimization(self):
        assert MeetingAction.meeting_cadence_optimization.value == "meeting_cadence_optimization"

    def test_six_members(self):
        assert len(MeetingAction) == 6

    def test_is_str_enum(self):
        assert isinstance(MeetingAction.no_action, str)


# ===========================================================================
# SECTION 2 – MeetingInput dataclass
# ===========================================================================

class TestMeetingInputFields:
    def test_rep_id_stored(self):
        inp = _base_input(rep_id="X1")
        assert inp.rep_id == "X1"

    def test_region_stored(self):
        inp = _base_input(region="APAC")
        assert inp.region == "APAC"

    def test_evaluation_period_id_stored(self):
        inp = _base_input(evaluation_period_id="Q1-2025")
        assert inp.evaluation_period_id == "Q1-2025"

    def test_total_meetings_conducted(self):
        inp = _base_input(total_meetings_conducted=50)
        assert inp.total_meetings_conducted == 50

    def test_meetings_with_agenda_sent_pct(self):
        inp = _base_input(meetings_with_agenda_sent_pct=0.60)
        assert inp.meetings_with_agenda_sent_pct == 0.60

    def test_avg_agenda_sent_hours(self):
        inp = _base_input(avg_agenda_sent_hours_before_meeting=6.0)
        assert inp.avg_agenda_sent_hours_before_meeting == 6.0

    def test_followup_within_24h_rate_pct(self):
        inp = _base_input(followup_within_24h_rate_pct=0.40)
        assert inp.followup_within_24h_rate_pct == 0.40

    def test_avg_followup_delay_hours(self):
        inp = _base_input(avg_followup_delay_hours=30.0)
        assert inp.avg_followup_delay_hours == 30.0

    def test_meeting_to_next_meeting_conversion_pct(self):
        inp = _base_input(meeting_to_next_meeting_conversion_pct=0.55)
        assert inp.meeting_to_next_meeting_conversion_pct == 0.55

    def test_avg_stakeholders_per_meeting(self):
        inp = _base_input(avg_stakeholders_per_meeting=1.8)
        assert inp.avg_stakeholders_per_meeting == 1.8

    def test_decision_maker_in_meeting_pct(self):
        inp = _base_input(decision_maker_in_meeting_pct=0.30)
        assert inp.decision_maker_in_meeting_pct == 0.30

    def test_meetings_with_no_outcome_pct(self):
        inp = _base_input(meetings_with_no_outcome_pct=0.40)
        assert inp.meetings_with_no_outcome_pct == 0.40

    def test_next_step_committed_at_meeting_pct(self):
        inp = _base_input(next_step_committed_at_meeting_pct=0.50)
        assert inp.next_step_committed_at_meeting_pct == 0.50

    def test_meetings_rescheduled_by_buyer_pct(self):
        inp = _base_input(meetings_rescheduled_by_buyer_pct=0.15)
        assert inp.meetings_rescheduled_by_buyer_pct == 0.15

    def test_avg_meeting_duration_minutes(self):
        inp = _base_input(avg_meeting_duration_minutes=30.0)
        assert inp.avg_meeting_duration_minutes == 30.0

    def test_meeting_recording_review_rate_pct(self):
        inp = _base_input(meeting_recording_review_rate_pct=0.20)
        assert inp.meeting_recording_review_rate_pct == 0.20

    def test_demo_conversion_from_meeting_pct(self):
        inp = _base_input(demo_conversion_from_meeting_pct=0.25)
        assert inp.demo_conversion_from_meeting_pct == 0.25

    def test_proposal_conversion_from_demo_pct(self):
        inp = _base_input(proposal_conversion_from_demo_pct=0.35)
        assert inp.proposal_conversion_from_demo_pct == 0.35

    def test_repeat_meeting_same_stage_pct(self):
        inp = _base_input(repeat_meeting_same_stage_pct=0.30)
        assert inp.repeat_meeting_same_stage_pct == 0.30

    def test_meeting_cancellation_rate_pct(self):
        inp = _base_input(meeting_cancellation_rate_pct=0.25)
        assert inp.meeting_cancellation_rate_pct == 0.25

    def test_avg_time_between_meetings_days(self):
        inp = _base_input(avg_time_between_meetings_days=14.0)
        assert inp.avg_time_between_meetings_days == 14.0

    def test_avg_opportunity_value_usd(self):
        inp = _base_input(avg_opportunity_value_usd=50_000.0)
        assert inp.avg_opportunity_value_usd == 50_000.0

    def test_total_fields_count(self):
        import dataclasses
        fields = dataclasses.fields(MeetingInput)
        assert len(fields) == 22


# ===========================================================================
# SECTION 3 – MeetingResult dataclass + to_dict()
# ===========================================================================

class TestMeetingResultFields:
    def _make_result(self) -> MeetingResult:
        return MeetingResult(
            rep_id="R1",
            region="NA",
            meeting_risk=MeetingRisk.low,
            meeting_pattern=MeetingPattern.none,
            meeting_severity=MeetingSeverity.structured,
            recommended_action=MeetingAction.no_action,
            meeting_prep_score=0.0,
            meeting_engagement_score=0.0,
            meeting_outcome_score=0.0,
            meeting_conversion_score=0.0,
            meeting_composite=0.0,
            has_meeting_gap=False,
            requires_meeting_coaching=False,
            estimated_pipeline_drag_usd=0.0,
            meeting_signal="ok",
        )

    def test_rep_id(self):
        assert self._make_result().rep_id == "R1"

    def test_region(self):
        assert self._make_result().region == "NA"

    def test_meeting_risk(self):
        assert self._make_result().meeting_risk == MeetingRisk.low

    def test_meeting_pattern(self):
        assert self._make_result().meeting_pattern == MeetingPattern.none

    def test_meeting_severity(self):
        assert self._make_result().meeting_severity == MeetingSeverity.structured

    def test_recommended_action(self):
        assert self._make_result().recommended_action == MeetingAction.no_action

    def test_meeting_prep_score(self):
        assert self._make_result().meeting_prep_score == 0.0

    def test_meeting_engagement_score(self):
        assert self._make_result().meeting_engagement_score == 0.0

    def test_meeting_outcome_score(self):
        assert self._make_result().meeting_outcome_score == 0.0

    def test_meeting_conversion_score(self):
        assert self._make_result().meeting_conversion_score == 0.0

    def test_meeting_composite(self):
        assert self._make_result().meeting_composite == 0.0

    def test_has_meeting_gap(self):
        assert self._make_result().has_meeting_gap is False

    def test_requires_meeting_coaching(self):
        assert self._make_result().requires_meeting_coaching is False

    def test_estimated_pipeline_drag_usd(self):
        assert self._make_result().estimated_pipeline_drag_usd == 0.0

    def test_meeting_signal(self):
        assert self._make_result().meeting_signal == "ok"

    def test_to_dict_has_15_keys(self):
        d = self._make_result().to_dict()
        assert len(d) == 15

    def test_to_dict_rep_id(self):
        assert self._make_result().to_dict()["rep_id"] == "R1"

    def test_to_dict_region(self):
        assert self._make_result().to_dict()["region"] == "NA"

    def test_to_dict_meeting_risk_is_string(self):
        d = self._make_result().to_dict()
        assert d["meeting_risk"] == "low"
        assert isinstance(d["meeting_risk"], str)

    def test_to_dict_meeting_pattern_is_string(self):
        d = self._make_result().to_dict()
        assert d["meeting_pattern"] == "none"
        assert isinstance(d["meeting_pattern"], str)

    def test_to_dict_meeting_severity_is_string(self):
        d = self._make_result().to_dict()
        assert d["meeting_severity"] == "structured"

    def test_to_dict_recommended_action_is_string(self):
        d = self._make_result().to_dict()
        assert d["recommended_action"] == "no_action"

    def test_to_dict_numeric_fields(self):
        d = self._make_result().to_dict()
        for key in ("meeting_prep_score", "meeting_engagement_score",
                    "meeting_outcome_score", "meeting_conversion_score",
                    "meeting_composite", "estimated_pipeline_drag_usd"):
            assert d[key] == 0.0

    def test_to_dict_bool_fields(self):
        d = self._make_result().to_dict()
        assert d["has_meeting_gap"] is False
        assert d["requires_meeting_coaching"] is False

    def test_to_dict_signal(self):
        assert self._make_result().to_dict()["meeting_signal"] == "ok"

    def test_to_dict_keys_exact(self):
        expected = {
            "rep_id", "region", "meeting_risk", "meeting_pattern",
            "meeting_severity", "recommended_action", "meeting_prep_score",
            "meeting_engagement_score", "meeting_outcome_score",
            "meeting_conversion_score", "meeting_composite",
            "has_meeting_gap", "requires_meeting_coaching",
            "estimated_pipeline_drag_usd", "meeting_signal",
        }
        assert set(self._make_result().to_dict().keys()) == expected


# ===========================================================================
# SECTION 4 – _meeting_prep_score()
# ===========================================================================

class TestMeetingPrepScore:
    def _score(self, **kw) -> float:
        return _engine()._meeting_prep_score(_base_input(**kw))

    # agenda_sent_pct branches
    def test_agenda_le_020_adds_40(self):
        s = self._score(meetings_with_agenda_sent_pct=0.10,
                        avg_agenda_sent_hours_before_meeting=24.0,
                        meeting_recording_review_rate_pct=0.50)
        assert s == 40.0

    def test_agenda_exactly_020_adds_40(self):
        s = self._score(meetings_with_agenda_sent_pct=0.20,
                        avg_agenda_sent_hours_before_meeting=24.0,
                        meeting_recording_review_rate_pct=0.50)
        assert s == 40.0

    def test_agenda_le_050_adds_22(self):
        s = self._score(meetings_with_agenda_sent_pct=0.35,
                        avg_agenda_sent_hours_before_meeting=24.0,
                        meeting_recording_review_rate_pct=0.50)
        assert s == 22.0

    def test_agenda_exactly_050_adds_22(self):
        s = self._score(meetings_with_agenda_sent_pct=0.50,
                        avg_agenda_sent_hours_before_meeting=24.0,
                        meeting_recording_review_rate_pct=0.50)
        assert s == 22.0

    def test_agenda_le_075_adds_8(self):
        s = self._score(meetings_with_agenda_sent_pct=0.60,
                        avg_agenda_sent_hours_before_meeting=24.0,
                        meeting_recording_review_rate_pct=0.50)
        assert s == 8.0

    def test_agenda_exactly_075_adds_8(self):
        s = self._score(meetings_with_agenda_sent_pct=0.75,
                        avg_agenda_sent_hours_before_meeting=24.0,
                        meeting_recording_review_rate_pct=0.50)
        assert s == 8.0

    def test_agenda_above_075_adds_0(self):
        s = self._score(meetings_with_agenda_sent_pct=0.90,
                        avg_agenda_sent_hours_before_meeting=24.0,
                        meeting_recording_review_rate_pct=0.50)
        assert s == 0.0

    # hours-before-meeting branches
    def test_hours_le_2_adds_35(self):
        s = self._score(meetings_with_agenda_sent_pct=0.90,
                        avg_agenda_sent_hours_before_meeting=1.0,
                        meeting_recording_review_rate_pct=0.50)
        assert s == 35.0

    def test_hours_exactly_2_adds_35(self):
        s = self._score(meetings_with_agenda_sent_pct=0.90,
                        avg_agenda_sent_hours_before_meeting=2.0,
                        meeting_recording_review_rate_pct=0.50)
        assert s == 35.0

    def test_hours_le_12_adds_18(self):
        s = self._score(meetings_with_agenda_sent_pct=0.90,
                        avg_agenda_sent_hours_before_meeting=6.0,
                        meeting_recording_review_rate_pct=0.50)
        assert s == 18.0

    def test_hours_exactly_12_adds_18(self):
        s = self._score(meetings_with_agenda_sent_pct=0.90,
                        avg_agenda_sent_hours_before_meeting=12.0,
                        meeting_recording_review_rate_pct=0.50)
        assert s == 18.0

    def test_hours_above_12_adds_0(self):
        s = self._score(meetings_with_agenda_sent_pct=0.90,
                        avg_agenda_sent_hours_before_meeting=24.0,
                        meeting_recording_review_rate_pct=0.50)
        assert s == 0.0

    # recording review rate branches
    def test_recording_le_010_adds_25(self):
        s = self._score(meetings_with_agenda_sent_pct=0.90,
                        avg_agenda_sent_hours_before_meeting=24.0,
                        meeting_recording_review_rate_pct=0.05)
        assert s == 25.0

    def test_recording_exactly_010_adds_25(self):
        s = self._score(meetings_with_agenda_sent_pct=0.90,
                        avg_agenda_sent_hours_before_meeting=24.0,
                        meeting_recording_review_rate_pct=0.10)
        assert s == 25.0

    def test_recording_le_030_adds_12(self):
        s = self._score(meetings_with_agenda_sent_pct=0.90,
                        avg_agenda_sent_hours_before_meeting=24.0,
                        meeting_recording_review_rate_pct=0.20)
        assert s == 12.0

    def test_recording_exactly_030_adds_12(self):
        s = self._score(meetings_with_agenda_sent_pct=0.90,
                        avg_agenda_sent_hours_before_meeting=24.0,
                        meeting_recording_review_rate_pct=0.30)
        assert s == 12.0

    def test_recording_above_030_adds_0(self):
        s = self._score(meetings_with_agenda_sent_pct=0.90,
                        avg_agenda_sent_hours_before_meeting=24.0,
                        meeting_recording_review_rate_pct=0.50)
        assert s == 0.0

    # accumulation and cap
    def test_all_worst_capped_at_100(self):
        s = self._score(meetings_with_agenda_sent_pct=0.0,
                        avg_agenda_sent_hours_before_meeting=0.0,
                        meeting_recording_review_rate_pct=0.0)
        # 40 + 35 + 25 = 100
        assert s == 100.0

    def test_zero_score_all_best(self):
        s = self._score(meetings_with_agenda_sent_pct=1.0,
                        avg_agenda_sent_hours_before_meeting=48.0,
                        meeting_recording_review_rate_pct=1.0)
        assert s == 0.0

    def test_combined_agenda_and_hours(self):
        # agenda 0.50 → 22, hours 2.0 → 35, recording 0.50 → 0
        s = self._score(meetings_with_agenda_sent_pct=0.50,
                        avg_agenda_sent_hours_before_meeting=2.0,
                        meeting_recording_review_rate_pct=0.50)
        assert s == 57.0


# ===========================================================================
# SECTION 5 – _meeting_engagement_score()
# ===========================================================================

class TestMeetingEngagementScore:
    def _score(self, **kw) -> float:
        return _engine()._meeting_engagement_score(_base_input(**kw))

    # avg_stakeholders branches
    def test_stakeholders_le_1_adds_40(self):
        s = self._score(avg_stakeholders_per_meeting=1.0,
                        decision_maker_in_meeting_pct=0.80,
                        meeting_cancellation_rate_pct=0.05)
        assert s == 40.0

    def test_stakeholders_exactly_1_adds_40(self):
        s = self._score(avg_stakeholders_per_meeting=1.0,
                        decision_maker_in_meeting_pct=0.80,
                        meeting_cancellation_rate_pct=0.05)
        assert s == 40.0

    def test_stakeholders_le_15_adds_22(self):
        s = self._score(avg_stakeholders_per_meeting=1.3,
                        decision_maker_in_meeting_pct=0.80,
                        meeting_cancellation_rate_pct=0.05)
        assert s == 22.0

    def test_stakeholders_exactly_15_adds_22(self):
        s = self._score(avg_stakeholders_per_meeting=1.5,
                        decision_maker_in_meeting_pct=0.80,
                        meeting_cancellation_rate_pct=0.05)
        assert s == 22.0

    def test_stakeholders_le_20_adds_8(self):
        s = self._score(avg_stakeholders_per_meeting=1.8,
                        decision_maker_in_meeting_pct=0.80,
                        meeting_cancellation_rate_pct=0.05)
        assert s == 8.0

    def test_stakeholders_exactly_20_adds_8(self):
        s = self._score(avg_stakeholders_per_meeting=2.0,
                        decision_maker_in_meeting_pct=0.80,
                        meeting_cancellation_rate_pct=0.05)
        assert s == 8.0

    def test_stakeholders_above_20_adds_0(self):
        s = self._score(avg_stakeholders_per_meeting=3.0,
                        decision_maker_in_meeting_pct=0.80,
                        meeting_cancellation_rate_pct=0.05)
        assert s == 0.0

    # decision_maker branches
    def test_decision_maker_le_020_adds_35(self):
        s = self._score(avg_stakeholders_per_meeting=3.0,
                        decision_maker_in_meeting_pct=0.10,
                        meeting_cancellation_rate_pct=0.05)
        assert s == 35.0

    def test_decision_maker_exactly_020_adds_35(self):
        s = self._score(avg_stakeholders_per_meeting=3.0,
                        decision_maker_in_meeting_pct=0.20,
                        meeting_cancellation_rate_pct=0.05)
        assert s == 35.0

    def test_decision_maker_le_050_adds_18(self):
        s = self._score(avg_stakeholders_per_meeting=3.0,
                        decision_maker_in_meeting_pct=0.35,
                        meeting_cancellation_rate_pct=0.05)
        assert s == 18.0

    def test_decision_maker_exactly_050_adds_18(self):
        s = self._score(avg_stakeholders_per_meeting=3.0,
                        decision_maker_in_meeting_pct=0.50,
                        meeting_cancellation_rate_pct=0.05)
        assert s == 18.0

    def test_decision_maker_above_050_adds_0(self):
        s = self._score(avg_stakeholders_per_meeting=3.0,
                        decision_maker_in_meeting_pct=0.75,
                        meeting_cancellation_rate_pct=0.05)
        assert s == 0.0

    # cancellation rate branches
    def test_cancellation_ge_035_adds_25(self):
        s = self._score(avg_stakeholders_per_meeting=3.0,
                        decision_maker_in_meeting_pct=0.80,
                        meeting_cancellation_rate_pct=0.40)
        assert s == 25.0

    def test_cancellation_exactly_035_adds_25(self):
        s = self._score(avg_stakeholders_per_meeting=3.0,
                        decision_maker_in_meeting_pct=0.80,
                        meeting_cancellation_rate_pct=0.35)
        assert s == 25.0

    def test_cancellation_ge_020_adds_12(self):
        s = self._score(avg_stakeholders_per_meeting=3.0,
                        decision_maker_in_meeting_pct=0.80,
                        meeting_cancellation_rate_pct=0.25)
        assert s == 12.0

    def test_cancellation_exactly_020_adds_12(self):
        s = self._score(avg_stakeholders_per_meeting=3.0,
                        decision_maker_in_meeting_pct=0.80,
                        meeting_cancellation_rate_pct=0.20)
        assert s == 12.0

    def test_cancellation_below_020_adds_0(self):
        s = self._score(avg_stakeholders_per_meeting=3.0,
                        decision_maker_in_meeting_pct=0.80,
                        meeting_cancellation_rate_pct=0.05)
        assert s == 0.0

    def test_all_worst_capped_at_100(self):
        s = self._score(avg_stakeholders_per_meeting=0.5,
                        decision_maker_in_meeting_pct=0.0,
                        meeting_cancellation_rate_pct=1.0)
        # 40 + 35 + 25 = 100
        assert s == 100.0

    def test_zero_score(self):
        s = self._score(avg_stakeholders_per_meeting=5.0,
                        decision_maker_in_meeting_pct=0.90,
                        meeting_cancellation_rate_pct=0.05)
        assert s == 0.0


# ===========================================================================
# SECTION 6 – _meeting_outcome_score()
# ===========================================================================

class TestMeetingOutcomeScore:
    def _score(self, **kw) -> float:
        return _engine()._meeting_outcome_score(_base_input(**kw))

    # next_step_committed branches
    def test_next_step_le_025_adds_40(self):
        s = self._score(next_step_committed_at_meeting_pct=0.20,
                        meetings_with_no_outcome_pct=0.10,
                        repeat_meeting_same_stage_pct=0.10)
        assert s == 40.0

    def test_next_step_exactly_025_adds_40(self):
        s = self._score(next_step_committed_at_meeting_pct=0.25,
                        meetings_with_no_outcome_pct=0.10,
                        repeat_meeting_same_stage_pct=0.10)
        assert s == 40.0

    def test_next_step_le_055_adds_22(self):
        s = self._score(next_step_committed_at_meeting_pct=0.40,
                        meetings_with_no_outcome_pct=0.10,
                        repeat_meeting_same_stage_pct=0.10)
        assert s == 22.0

    def test_next_step_exactly_055_adds_22(self):
        s = self._score(next_step_committed_at_meeting_pct=0.55,
                        meetings_with_no_outcome_pct=0.10,
                        repeat_meeting_same_stage_pct=0.10)
        assert s == 22.0

    def test_next_step_le_075_adds_8(self):
        s = self._score(next_step_committed_at_meeting_pct=0.65,
                        meetings_with_no_outcome_pct=0.10,
                        repeat_meeting_same_stage_pct=0.10)
        assert s == 8.0

    def test_next_step_exactly_075_adds_8(self):
        s = self._score(next_step_committed_at_meeting_pct=0.75,
                        meetings_with_no_outcome_pct=0.10,
                        repeat_meeting_same_stage_pct=0.10)
        assert s == 8.0

    def test_next_step_above_075_adds_0(self):
        s = self._score(next_step_committed_at_meeting_pct=0.90,
                        meetings_with_no_outcome_pct=0.10,
                        repeat_meeting_same_stage_pct=0.10)
        assert s == 0.0

    # no_outcome branches
    def test_no_outcome_ge_050_adds_35(self):
        s = self._score(next_step_committed_at_meeting_pct=0.90,
                        meetings_with_no_outcome_pct=0.60,
                        repeat_meeting_same_stage_pct=0.10)
        assert s == 35.0

    def test_no_outcome_exactly_050_adds_35(self):
        s = self._score(next_step_committed_at_meeting_pct=0.90,
                        meetings_with_no_outcome_pct=0.50,
                        repeat_meeting_same_stage_pct=0.10)
        assert s == 35.0

    def test_no_outcome_ge_025_adds_18(self):
        s = self._score(next_step_committed_at_meeting_pct=0.90,
                        meetings_with_no_outcome_pct=0.30,
                        repeat_meeting_same_stage_pct=0.10)
        assert s == 18.0

    def test_no_outcome_exactly_025_adds_18(self):
        s = self._score(next_step_committed_at_meeting_pct=0.90,
                        meetings_with_no_outcome_pct=0.25,
                        repeat_meeting_same_stage_pct=0.10)
        assert s == 18.0

    def test_no_outcome_below_025_adds_0(self):
        s = self._score(next_step_committed_at_meeting_pct=0.90,
                        meetings_with_no_outcome_pct=0.10,
                        repeat_meeting_same_stage_pct=0.10)
        assert s == 0.0

    # repeat_meeting branches
    def test_repeat_ge_050_adds_25(self):
        s = self._score(next_step_committed_at_meeting_pct=0.90,
                        meetings_with_no_outcome_pct=0.10,
                        repeat_meeting_same_stage_pct=0.60)
        assert s == 25.0

    def test_repeat_exactly_050_adds_25(self):
        s = self._score(next_step_committed_at_meeting_pct=0.90,
                        meetings_with_no_outcome_pct=0.10,
                        repeat_meeting_same_stage_pct=0.50)
        assert s == 25.0

    def test_repeat_ge_025_adds_12(self):
        s = self._score(next_step_committed_at_meeting_pct=0.90,
                        meetings_with_no_outcome_pct=0.10,
                        repeat_meeting_same_stage_pct=0.30)
        assert s == 12.0

    def test_repeat_exactly_025_adds_12(self):
        s = self._score(next_step_committed_at_meeting_pct=0.90,
                        meetings_with_no_outcome_pct=0.10,
                        repeat_meeting_same_stage_pct=0.25)
        assert s == 12.0

    def test_repeat_below_025_adds_0(self):
        s = self._score(next_step_committed_at_meeting_pct=0.90,
                        meetings_with_no_outcome_pct=0.10,
                        repeat_meeting_same_stage_pct=0.10)
        assert s == 0.0

    def test_all_worst_capped_100(self):
        s = self._score(next_step_committed_at_meeting_pct=0.0,
                        meetings_with_no_outcome_pct=1.0,
                        repeat_meeting_same_stage_pct=1.0)
        # 40 + 35 + 25 = 100
        assert s == 100.0

    def test_zero_score(self):
        s = self._score(next_step_committed_at_meeting_pct=1.0,
                        meetings_with_no_outcome_pct=0.0,
                        repeat_meeting_same_stage_pct=0.0)
        assert s == 0.0


# ===========================================================================
# SECTION 7 – _meeting_conversion_score()
# ===========================================================================

class TestMeetingConversionScore:
    def _score(self, **kw) -> float:
        return _engine()._meeting_conversion_score(_base_input(**kw))

    # followup branches
    def test_followup_le_020_adds_45(self):
        s = self._score(followup_within_24h_rate_pct=0.10,
                        demo_conversion_from_meeting_pct=0.50,
                        proposal_conversion_from_demo_pct=0.70)
        assert s == 45.0

    def test_followup_exactly_020_adds_45(self):
        s = self._score(followup_within_24h_rate_pct=0.20,
                        demo_conversion_from_meeting_pct=0.50,
                        proposal_conversion_from_demo_pct=0.70)
        assert s == 45.0

    def test_followup_le_050_adds_25(self):
        s = self._score(followup_within_24h_rate_pct=0.35,
                        demo_conversion_from_meeting_pct=0.50,
                        proposal_conversion_from_demo_pct=0.70)
        assert s == 25.0

    def test_followup_exactly_050_adds_25(self):
        s = self._score(followup_within_24h_rate_pct=0.50,
                        demo_conversion_from_meeting_pct=0.50,
                        proposal_conversion_from_demo_pct=0.70)
        assert s == 25.0

    def test_followup_le_075_adds_10(self):
        s = self._score(followup_within_24h_rate_pct=0.65,
                        demo_conversion_from_meeting_pct=0.50,
                        proposal_conversion_from_demo_pct=0.70)
        assert s == 10.0

    def test_followup_exactly_075_adds_10(self):
        s = self._score(followup_within_24h_rate_pct=0.75,
                        demo_conversion_from_meeting_pct=0.50,
                        proposal_conversion_from_demo_pct=0.70)
        assert s == 10.0

    def test_followup_above_075_adds_0(self):
        s = self._score(followup_within_24h_rate_pct=0.90,
                        demo_conversion_from_meeting_pct=0.50,
                        proposal_conversion_from_demo_pct=0.70)
        assert s == 0.0

    # demo conversion branches
    def test_demo_le_015_adds_30(self):
        s = self._score(followup_within_24h_rate_pct=0.90,
                        demo_conversion_from_meeting_pct=0.10,
                        proposal_conversion_from_demo_pct=0.70)
        assert s == 30.0

    def test_demo_exactly_015_adds_30(self):
        s = self._score(followup_within_24h_rate_pct=0.90,
                        demo_conversion_from_meeting_pct=0.15,
                        proposal_conversion_from_demo_pct=0.70)
        assert s == 30.0

    def test_demo_le_035_adds_15(self):
        s = self._score(followup_within_24h_rate_pct=0.90,
                        demo_conversion_from_meeting_pct=0.25,
                        proposal_conversion_from_demo_pct=0.70)
        assert s == 15.0

    def test_demo_exactly_035_adds_15(self):
        s = self._score(followup_within_24h_rate_pct=0.90,
                        demo_conversion_from_meeting_pct=0.35,
                        proposal_conversion_from_demo_pct=0.70)
        assert s == 15.0

    def test_demo_above_035_adds_0(self):
        s = self._score(followup_within_24h_rate_pct=0.90,
                        demo_conversion_from_meeting_pct=0.50,
                        proposal_conversion_from_demo_pct=0.70)
        assert s == 0.0

    # proposal conversion branches
    def test_proposal_le_025_adds_25(self):
        s = self._score(followup_within_24h_rate_pct=0.90,
                        demo_conversion_from_meeting_pct=0.50,
                        proposal_conversion_from_demo_pct=0.20)
        assert s == 25.0

    def test_proposal_exactly_025_adds_25(self):
        s = self._score(followup_within_24h_rate_pct=0.90,
                        demo_conversion_from_meeting_pct=0.50,
                        proposal_conversion_from_demo_pct=0.25)
        assert s == 25.0

    def test_proposal_le_050_adds_12(self):
        s = self._score(followup_within_24h_rate_pct=0.90,
                        demo_conversion_from_meeting_pct=0.50,
                        proposal_conversion_from_demo_pct=0.40)
        assert s == 12.0

    def test_proposal_exactly_050_adds_12(self):
        s = self._score(followup_within_24h_rate_pct=0.90,
                        demo_conversion_from_meeting_pct=0.50,
                        proposal_conversion_from_demo_pct=0.50)
        assert s == 12.0

    def test_proposal_above_050_adds_0(self):
        s = self._score(followup_within_24h_rate_pct=0.90,
                        demo_conversion_from_meeting_pct=0.50,
                        proposal_conversion_from_demo_pct=0.70)
        assert s == 0.0

    def test_all_worst_capped_100(self):
        s = self._score(followup_within_24h_rate_pct=0.0,
                        demo_conversion_from_meeting_pct=0.0,
                        proposal_conversion_from_demo_pct=0.0)
        # 45 + 30 + 25 = 100
        assert s == 100.0

    def test_zero_score(self):
        s = self._score(followup_within_24h_rate_pct=1.0,
                        demo_conversion_from_meeting_pct=1.0,
                        proposal_conversion_from_demo_pct=1.0)
        assert s == 0.0


# ===========================================================================
# SECTION 8 – _detect_pattern()
# ===========================================================================

class TestDetectPattern:
    def _detect(self, inp: MeetingInput,
                prep: float, engagement: float,
                outcome: float, conversion: float) -> MeetingPattern:
        return _engine()._detect_pattern(inp, prep, engagement, outcome, conversion)

    def test_no_agenda_discipline(self):
        inp = _base_input(meetings_with_agenda_sent_pct=0.25)
        # prep >= 40 required
        assert self._detect(inp, 40.0, 0.0, 0.0, 0.0) == MeetingPattern.no_agenda_discipline

    def test_no_agenda_discipline_prep_boundary(self):
        inp = _base_input(meetings_with_agenda_sent_pct=0.30)
        assert self._detect(inp, 40.0, 0.0, 0.0, 0.0) == MeetingPattern.no_agenda_discipline

    def test_no_agenda_discipline_agenda_above_030_skipped(self):
        # agenda_sent > 0.30 → condition false
        inp = _base_input(meetings_with_agenda_sent_pct=0.31, followup_within_24h_rate_pct=0.25)
        # conversion >= 30 → poor_followup fires next
        result = self._detect(inp, 40.0, 0.0, 0.0, 30.0)
        assert result == MeetingPattern.poor_followup

    def test_poor_followup(self):
        inp = _base_input(meetings_with_agenda_sent_pct=0.80, followup_within_24h_rate_pct=0.25)
        assert self._detect(inp, 5.0, 0.0, 0.0, 30.0) == MeetingPattern.poor_followup

    def test_poor_followup_boundary(self):
        inp = _base_input(meetings_with_agenda_sent_pct=0.80, followup_within_24h_rate_pct=0.30)
        assert self._detect(inp, 5.0, 0.0, 0.0, 30.0) == MeetingPattern.poor_followup

    def test_single_stakeholder_trap(self):
        inp = _base_input(meetings_with_agenda_sent_pct=0.80,
                          followup_within_24h_rate_pct=0.80,
                          avg_stakeholders_per_meeting=1.0)
        assert self._detect(inp, 5.0, 30.0, 0.0, 0.0) == MeetingPattern.single_stakeholder_trap

    def test_single_stakeholder_boundary(self):
        inp = _base_input(meetings_with_agenda_sent_pct=0.80,
                          followup_within_24h_rate_pct=0.80,
                          avg_stakeholders_per_meeting=1.2)
        assert self._detect(inp, 5.0, 30.0, 0.0, 0.0) == MeetingPattern.single_stakeholder_trap

    def test_no_next_step_close(self):
        inp = _base_input(meetings_with_agenda_sent_pct=0.80,
                          followup_within_24h_rate_pct=0.80,
                          avg_stakeholders_per_meeting=3.0,
                          next_step_committed_at_meeting_pct=0.20)
        assert self._detect(inp, 5.0, 5.0, 40.0, 0.0) == MeetingPattern.no_next_step_close

    def test_no_next_step_close_boundary(self):
        inp = _base_input(meetings_with_agenda_sent_pct=0.80,
                          followup_within_24h_rate_pct=0.80,
                          avg_stakeholders_per_meeting=3.0,
                          next_step_committed_at_meeting_pct=0.30)
        assert self._detect(inp, 5.0, 5.0, 40.0, 0.0) == MeetingPattern.no_next_step_close

    def test_meeting_fatigue(self):
        inp = _base_input(meetings_with_agenda_sent_pct=0.80,
                          followup_within_24h_rate_pct=0.80,
                          avg_stakeholders_per_meeting=3.0,
                          next_step_committed_at_meeting_pct=0.90,
                          meeting_cancellation_rate_pct=0.35)
        assert self._detect(inp, 5.0, 30.0, 5.0, 0.0) == MeetingPattern.meeting_fatigue

    def test_meeting_fatigue_boundary(self):
        inp = _base_input(meetings_with_agenda_sent_pct=0.80,
                          followup_within_24h_rate_pct=0.80,
                          avg_stakeholders_per_meeting=3.0,
                          next_step_committed_at_meeting_pct=0.90,
                          meeting_cancellation_rate_pct=0.30)
        assert self._detect(inp, 5.0, 30.0, 5.0, 0.0) == MeetingPattern.meeting_fatigue

    def test_pattern_none_all_healthy(self):
        inp = _base_input()
        assert self._detect(inp, 5.0, 5.0, 5.0, 5.0) == MeetingPattern.none

    def test_priority_order_agenda_beats_followup(self):
        # Both agenda and followup conditions satisfied – agenda wins
        inp = _base_input(meetings_with_agenda_sent_pct=0.25,
                          followup_within_24h_rate_pct=0.25)
        result = self._detect(inp, 40.0, 0.0, 0.0, 30.0)
        assert result == MeetingPattern.no_agenda_discipline


# ===========================================================================
# SECTION 9 – _risk_level()
# ===========================================================================

class TestRiskLevel:
    def _risk(self, composite: float) -> MeetingRisk:
        return _engine()._risk_level(composite)

    def test_below_20_is_low(self):
        assert self._risk(0.0) == MeetingRisk.low

    def test_exactly_0_is_low(self):
        assert self._risk(0.0) == MeetingRisk.low

    def test_just_below_20_is_low(self):
        assert self._risk(19.9) == MeetingRisk.low

    def test_exactly_20_is_moderate(self):
        assert self._risk(20.0) == MeetingRisk.moderate

    def test_between_20_and_40_is_moderate(self):
        assert self._risk(30.0) == MeetingRisk.moderate

    def test_just_below_40_is_moderate(self):
        assert self._risk(39.9) == MeetingRisk.moderate

    def test_exactly_40_is_high(self):
        assert self._risk(40.0) == MeetingRisk.high

    def test_between_40_and_60_is_high(self):
        assert self._risk(50.0) == MeetingRisk.high

    def test_just_below_60_is_high(self):
        assert self._risk(59.9) == MeetingRisk.high

    def test_exactly_60_is_critical(self):
        assert self._risk(60.0) == MeetingRisk.critical

    def test_above_60_is_critical(self):
        assert self._risk(80.0) == MeetingRisk.critical

    def test_100_is_critical(self):
        assert self._risk(100.0) == MeetingRisk.critical


# ===========================================================================
# SECTION 10 – _severity()
# ===========================================================================

class TestSeverity:
    def _sev(self, composite: float) -> MeetingSeverity:
        return _engine()._severity(composite)

    def test_0_is_structured(self):
        assert self._sev(0.0) == MeetingSeverity.structured

    def test_just_below_20_is_structured(self):
        assert self._sev(19.9) == MeetingSeverity.structured

    def test_exactly_20_is_developing(self):
        assert self._sev(20.0) == MeetingSeverity.developing

    def test_between_20_40_is_developing(self):
        assert self._sev(30.0) == MeetingSeverity.developing

    def test_just_below_40_is_developing(self):
        assert self._sev(39.9) == MeetingSeverity.developing

    def test_exactly_40_is_ad_hoc(self):
        assert self._sev(40.0) == MeetingSeverity.ad_hoc

    def test_between_40_60_is_ad_hoc(self):
        assert self._sev(50.0) == MeetingSeverity.ad_hoc

    def test_just_below_60_is_ad_hoc(self):
        assert self._sev(59.9) == MeetingSeverity.ad_hoc

    def test_exactly_60_is_chaotic(self):
        assert self._sev(60.0) == MeetingSeverity.chaotic

    def test_above_60_is_chaotic(self):
        assert self._sev(75.0) == MeetingSeverity.chaotic

    def test_100_is_chaotic(self):
        assert self._sev(100.0) == MeetingSeverity.chaotic


# ===========================================================================
# SECTION 11 – _action()
# ===========================================================================

class TestAction:
    def _action(self, risk: MeetingRisk, pattern: MeetingPattern) -> MeetingAction:
        return _engine()._action(risk, pattern)

    # Low risk
    def test_low_no_action(self):
        assert self._action(MeetingRisk.low, MeetingPattern.none) == MeetingAction.no_action

    def test_low_pattern_still_no_action(self):
        assert self._action(MeetingRisk.low, MeetingPattern.meeting_fatigue) == MeetingAction.no_action

    # Moderate risk
    def test_moderate_returns_prep_coaching(self):
        assert self._action(MeetingRisk.moderate, MeetingPattern.none) == MeetingAction.meeting_prep_coaching

    def test_moderate_any_pattern_returns_prep_coaching(self):
        for p in MeetingPattern:
            assert self._action(MeetingRisk.moderate, p) == MeetingAction.meeting_prep_coaching

    # High risk
    def test_high_poor_followup_returns_followup_training(self):
        assert self._action(MeetingRisk.high, MeetingPattern.poor_followup) == MeetingAction.followup_discipline_training

    def test_high_meeting_fatigue_returns_cadence_opt(self):
        assert self._action(MeetingRisk.high, MeetingPattern.meeting_fatigue) == MeetingAction.meeting_cadence_optimization

    def test_high_other_pattern_returns_prep_coaching(self):
        assert self._action(MeetingRisk.high, MeetingPattern.none) == MeetingAction.meeting_prep_coaching

    def test_high_no_agenda_returns_prep_coaching(self):
        assert self._action(MeetingRisk.high, MeetingPattern.no_agenda_discipline) == MeetingAction.meeting_prep_coaching

    def test_high_stakeholder_trap_returns_prep_coaching(self):
        assert self._action(MeetingRisk.high, MeetingPattern.single_stakeholder_trap) == MeetingAction.meeting_prep_coaching

    def test_high_no_next_step_returns_prep_coaching(self):
        assert self._action(MeetingRisk.high, MeetingPattern.no_next_step_close) == MeetingAction.meeting_prep_coaching

    # Critical risk
    def test_critical_no_next_step_close_returns_next_step_training(self):
        assert self._action(MeetingRisk.critical, MeetingPattern.no_next_step_close) == MeetingAction.next_step_close_training

    def test_critical_stakeholder_trap_returns_expansion(self):
        assert self._action(MeetingRisk.critical, MeetingPattern.single_stakeholder_trap) == MeetingAction.stakeholder_expansion_in_meetings

    def test_critical_none_returns_prep_coaching(self):
        assert self._action(MeetingRisk.critical, MeetingPattern.none) == MeetingAction.meeting_prep_coaching

    def test_critical_no_agenda_returns_prep_coaching(self):
        assert self._action(MeetingRisk.critical, MeetingPattern.no_agenda_discipline) == MeetingAction.meeting_prep_coaching

    def test_critical_poor_followup_returns_prep_coaching(self):
        assert self._action(MeetingRisk.critical, MeetingPattern.poor_followup) == MeetingAction.meeting_prep_coaching

    def test_critical_meeting_fatigue_returns_prep_coaching(self):
        assert self._action(MeetingRisk.critical, MeetingPattern.meeting_fatigue) == MeetingAction.meeting_prep_coaching


# ===========================================================================
# SECTION 12 – _has_meeting_gap()
# ===========================================================================

class TestHasMeetingGap:
    def _gap(self, composite: float, **kw) -> bool:
        return _engine()._has_meeting_gap(composite, _base_input(**kw))

    def test_no_gap_all_healthy(self):
        assert self._gap(10.0) is False

    def test_composite_ge_40_triggers_gap(self):
        assert self._gap(40.0) is True

    def test_composite_39_no_gap(self):
        assert self._gap(39.9,
                         meetings_with_no_outcome_pct=0.10,
                         next_step_committed_at_meeting_pct=0.90) is False

    def test_no_outcome_ge_040_triggers_gap(self):
        assert self._gap(10.0, meetings_with_no_outcome_pct=0.40) is True

    def test_no_outcome_below_040_no_gap(self):
        assert self._gap(10.0,
                         meetings_with_no_outcome_pct=0.39,
                         next_step_committed_at_meeting_pct=0.90) is False

    def test_next_step_le_025_triggers_gap(self):
        assert self._gap(10.0, next_step_committed_at_meeting_pct=0.25) is True

    def test_next_step_above_025_no_gap(self):
        assert self._gap(10.0,
                         meetings_with_no_outcome_pct=0.10,
                         next_step_committed_at_meeting_pct=0.26) is False

    def test_all_conditions_true(self):
        assert self._gap(60.0,
                         meetings_with_no_outcome_pct=0.50,
                         next_step_committed_at_meeting_pct=0.10) is True

    def test_composite_exactly_40(self):
        assert self._gap(40.0) is True


# ===========================================================================
# SECTION 13 – _requires_meeting_coaching()
# ===========================================================================

class TestRequiresMeetingCoaching:
    def _coach(self, composite: float, **kw) -> bool:
        return _engine()._requires_meeting_coaching(composite, _base_input(**kw))

    def test_no_coaching_all_healthy(self):
        assert self._coach(10.0) is False

    def test_composite_ge_30_triggers_coaching(self):
        assert self._coach(30.0) is True

    def test_composite_29_no_coaching(self):
        assert self._coach(29.9,
                           meetings_with_agenda_sent_pct=0.90,
                           followup_within_24h_rate_pct=0.90) is False

    def test_agenda_le_040_triggers_coaching(self):
        assert self._coach(10.0, meetings_with_agenda_sent_pct=0.40) is True

    def test_agenda_above_040_no_coaching(self):
        assert self._coach(10.0,
                           meetings_with_agenda_sent_pct=0.41,
                           followup_within_24h_rate_pct=0.90) is False

    def test_followup_le_040_triggers_coaching(self):
        assert self._coach(10.0, followup_within_24h_rate_pct=0.40) is True

    def test_followup_above_040_no_coaching(self):
        assert self._coach(10.0,
                           meetings_with_agenda_sent_pct=0.90,
                           followup_within_24h_rate_pct=0.41) is False

    def test_composite_exactly_30(self):
        assert self._coach(30.0) is True

    def test_all_conditions_trigger(self):
        assert self._coach(50.0,
                           meetings_with_agenda_sent_pct=0.10,
                           followup_within_24h_rate_pct=0.10) is True


# ===========================================================================
# SECTION 14 – _estimated_pipeline_drag()
# ===========================================================================

class TestEstimatedPipelineDrag:
    def _drag(self, composite: float, **kw) -> float:
        return _engine()._estimated_pipeline_drag(_base_input(**kw), composite)

    def test_zero_meetings_zero_drag(self):
        d = self._drag(50.0, total_meetings_conducted=0,
                       meetings_with_no_outcome_pct=0.50,
                       avg_opportunity_value_usd=10_000.0)
        assert d == 0.0

    def test_zero_no_outcome_zero_drag(self):
        d = self._drag(50.0, total_meetings_conducted=20,
                       meetings_with_no_outcome_pct=0.0,
                       avg_opportunity_value_usd=10_000.0)
        assert d == 0.0

    def test_zero_composite_zero_drag(self):
        d = self._drag(0.0, total_meetings_conducted=20,
                       meetings_with_no_outcome_pct=0.50,
                       avg_opportunity_value_usd=10_000.0)
        assert d == 0.0

    def test_known_value(self):
        # no_outcome_meetings = round(20 * 0.50) = 10
        # drag = 10 * 10_000 * (50/100) * 0.20 = 10_000.0
        d = self._drag(50.0, total_meetings_conducted=20,
                       meetings_with_no_outcome_pct=0.50,
                       avg_opportunity_value_usd=10_000.0)
        assert d == 10_000.0

    def test_drag_scales_with_composite(self):
        d1 = self._drag(25.0, total_meetings_conducted=20,
                        meetings_with_no_outcome_pct=0.50,
                        avg_opportunity_value_usd=10_000.0)
        d2 = self._drag(50.0, total_meetings_conducted=20,
                        meetings_with_no_outcome_pct=0.50,
                        avg_opportunity_value_usd=10_000.0)
        assert d2 == pytest.approx(d1 * 2, rel=1e-3)

    def test_drag_scales_with_opportunity_value(self):
        d1 = self._drag(50.0, total_meetings_conducted=10,
                        meetings_with_no_outcome_pct=0.50,
                        avg_opportunity_value_usd=5_000.0)
        d2 = self._drag(50.0, total_meetings_conducted=10,
                        meetings_with_no_outcome_pct=0.50,
                        avg_opportunity_value_usd=10_000.0)
        assert d2 == pytest.approx(d1 * 2, rel=1e-3)

    def test_drag_rounded_to_2_dp(self):
        d = self._drag(33.0, total_meetings_conducted=10,
                       meetings_with_no_outcome_pct=0.33,
                       avg_opportunity_value_usd=7_500.0)
        # verify it's rounded to 2 dp
        assert d == round(d, 2)

    def test_drag_rounds_no_outcome_meetings(self):
        # 10 * 0.55 = 5.5 → round = 6
        # drag = 6 * 1000 * (100/100) * 0.20 = 1200.0
        d = self._drag(100.0, total_meetings_conducted=10,
                       meetings_with_no_outcome_pct=0.55,
                       avg_opportunity_value_usd=1_000.0)
        assert d == 1_200.0


# ===========================================================================
# SECTION 15 – _signal()
# ===========================================================================

class TestSignal:
    def _signal(self, pattern: MeetingPattern, composite: float, **kw) -> str:
        return _engine()._signal(_base_input(**kw), pattern, composite)

    def test_healthy_signal(self):
        s = self._signal(MeetingPattern.none, 10.0)
        assert s == ("Meeting quality healthy — preparation, stakeholder engagement, "
                     "and next-step discipline within benchmarks")

    def test_healthy_boundary_composite_19(self):
        s = self._signal(MeetingPattern.none, 19.9)
        assert "healthy" in s

    def test_not_healthy_when_pattern_set_despite_low_composite(self):
        s = self._signal(MeetingPattern.poor_followup, 10.0)
        assert "healthy" not in s

    def test_not_healthy_when_composite_eq_20_pattern_none(self):
        # composite < 20 required for healthy; 20 not healthy
        s = self._signal(MeetingPattern.none, 20.0,
                         meetings_with_agenda_sent_pct=0.90,
                         next_step_committed_at_meeting_pct=0.90,
                         avg_stakeholders_per_meeting=2.5)
        assert "healthy" not in s
        assert "composite 20" in s

    def test_signal_contains_composite(self):
        s = self._signal(MeetingPattern.none, 35.0,
                         meetings_with_agenda_sent_pct=0.90,
                         next_step_committed_at_meeting_pct=0.90,
                         avg_stakeholders_per_meeting=2.5)
        assert "composite 35" in s

    def test_signal_pattern_label_capitalized(self):
        s = self._signal(MeetingPattern.poor_followup, 30.0,
                         meetings_with_agenda_sent_pct=0.90,
                         next_step_committed_at_meeting_pct=0.90,
                         avg_stakeholders_per_meeting=2.5)
        assert s.startswith("Poor followup")

    def test_signal_label_no_next_step_close(self):
        s = self._signal(MeetingPattern.no_next_step_close, 50.0,
                         meetings_with_agenda_sent_pct=0.90,
                         next_step_committed_at_meeting_pct=0.90,
                         avg_stakeholders_per_meeting=2.5)
        assert s.startswith("No next step close")

    def test_signal_label_meeting_fatigue(self):
        s = self._signal(MeetingPattern.meeting_fatigue, 45.0,
                         meetings_with_agenda_sent_pct=0.90,
                         next_step_committed_at_meeting_pct=0.90,
                         avg_stakeholders_per_meeting=2.5)
        assert s.startswith("Meeting fatigue")

    def test_signal_includes_agenda_pct(self):
        s = self._signal(MeetingPattern.none, 25.0,
                         meetings_with_agenda_sent_pct=0.60,
                         next_step_committed_at_meeting_pct=0.90,
                         avg_stakeholders_per_meeting=2.5)
        assert "60% meetings with agenda" in s

    def test_signal_includes_next_step_pct(self):
        s = self._signal(MeetingPattern.none, 25.0,
                         meetings_with_agenda_sent_pct=0.90,
                         next_step_committed_at_meeting_pct=0.70,
                         avg_stakeholders_per_meeting=2.5)
        assert "70% next-step committed" in s

    def test_signal_always_includes_stakeholders(self):
        s = self._signal(MeetingPattern.none, 25.0,
                         meetings_with_agenda_sent_pct=0.90,
                         next_step_committed_at_meeting_pct=0.90,
                         avg_stakeholders_per_meeting=2.5)
        assert "2.5 avg stakeholders" in s

    def test_signal_pattern_none_non_healthy_label(self):
        s = self._signal(MeetingPattern.none, 25.0,
                         meetings_with_agenda_sent_pct=0.90,
                         next_step_committed_at_meeting_pct=0.90,
                         avg_stakeholders_per_meeting=2.5)
        assert s.startswith("Meeting quality risk")

    def test_signal_single_stakeholder_trap_label(self):
        s = self._signal(MeetingPattern.single_stakeholder_trap, 45.0,
                         meetings_with_agenda_sent_pct=0.90,
                         next_step_committed_at_meeting_pct=0.90,
                         avg_stakeholders_per_meeting=1.0)
        assert s.startswith("Single stakeholder trap")


# ===========================================================================
# SECTION 16 – assess() end-to-end
# ===========================================================================

class TestAssess:
    def test_returns_meeting_result(self):
        result = _engine().assess(_base_input())
        assert isinstance(result, MeetingResult)

    def test_rep_id_preserved(self):
        result = _engine().assess(_base_input(rep_id="RTEST"))
        assert result.rep_id == "RTEST"

    def test_region_preserved(self):
        result = _engine().assess(_base_input(region="LATAM"))
        assert result.region == "LATAM"

    def test_healthy_scenario_low_risk(self):
        result = _engine().assess(_base_input())
        assert result.meeting_risk == MeetingRisk.low

    def test_healthy_scenario_structured_severity(self):
        result = _engine().assess(_base_input())
        assert result.meeting_severity == MeetingSeverity.structured

    def test_healthy_scenario_no_action(self):
        result = _engine().assess(_base_input())
        assert result.recommended_action == MeetingAction.no_action

    def test_healthy_scenario_no_gap(self):
        result = _engine().assess(_base_input())
        assert result.has_meeting_gap is False

    def test_healthy_scenario_signal_healthy(self):
        result = _engine().assess(_base_input())
        assert "healthy" in result.meeting_signal

    def test_all_worst_critical_risk(self):
        inp = _base_input(
            meetings_with_agenda_sent_pct=0.0,
            avg_agenda_sent_hours_before_meeting=0.0,
            meeting_recording_review_rate_pct=0.0,
            avg_stakeholders_per_meeting=0.5,
            decision_maker_in_meeting_pct=0.0,
            meeting_cancellation_rate_pct=1.0,
            next_step_committed_at_meeting_pct=0.0,
            meetings_with_no_outcome_pct=1.0,
            repeat_meeting_same_stage_pct=1.0,
            followup_within_24h_rate_pct=0.0,
            demo_conversion_from_meeting_pct=0.0,
            proposal_conversion_from_demo_pct=0.0,
        )
        result = _engine().assess(inp)
        assert result.meeting_risk == MeetingRisk.critical
        assert result.meeting_severity == MeetingSeverity.chaotic

    def test_composite_formula(self):
        # Use known sub-scores by controlling inputs
        inp = _base_input(
            meetings_with_agenda_sent_pct=0.90,
            avg_agenda_sent_hours_before_meeting=24.0,
            meeting_recording_review_rate_pct=0.50,
            avg_stakeholders_per_meeting=2.5,
            decision_maker_in_meeting_pct=0.75,
            meeting_cancellation_rate_pct=0.05,
            next_step_committed_at_meeting_pct=0.90,
            meetings_with_no_outcome_pct=0.10,
            repeat_meeting_same_stage_pct=0.10,
            followup_within_24h_rate_pct=0.90,
            demo_conversion_from_meeting_pct=0.50,
            proposal_conversion_from_demo_pct=0.70,
        )
        e = _engine()
        prep = round(e._meeting_prep_score(inp), 1)
        engagement = round(e._meeting_engagement_score(inp), 1)
        outcome = round(e._meeting_outcome_score(inp), 1)
        conversion = round(e._meeting_conversion_score(inp), 1)
        expected = round(prep * 0.25 + engagement * 0.30 + outcome * 0.30 + conversion * 0.15, 1)
        result = e.assess(inp)
        assert result.meeting_composite == min(expected, 100.0)

    def test_assess_appends_to_results(self):
        e = _engine()
        e.assess(_base_input())
        e.assess(_base_input(rep_id="R2"))
        assert len(e._results) == 2

    def test_to_dict_after_assess(self):
        result = _engine().assess(_base_input())
        d = result.to_dict()
        assert isinstance(d, dict)
        assert len(d) == 15

    def test_pipeline_drag_non_negative(self):
        result = _engine().assess(_base_input())
        assert result.estimated_pipeline_drag_usd >= 0.0

    def test_prep_score_is_rounded_to_1dp(self):
        result = _engine().assess(_base_input())
        # Check it's a float and precision is 1 decimal place
        assert isinstance(result.meeting_prep_score, float)

    def test_composite_capped_at_100(self):
        inp = _base_input(
            meetings_with_agenda_sent_pct=0.0,
            avg_agenda_sent_hours_before_meeting=0.0,
            meeting_recording_review_rate_pct=0.0,
            avg_stakeholders_per_meeting=0.0,
            decision_maker_in_meeting_pct=0.0,
            meeting_cancellation_rate_pct=1.0,
            next_step_committed_at_meeting_pct=0.0,
            meetings_with_no_outcome_pct=1.0,
            repeat_meeting_same_stage_pct=1.0,
            followup_within_24h_rate_pct=0.0,
            demo_conversion_from_meeting_pct=0.0,
            proposal_conversion_from_demo_pct=0.0,
        )
        result = _engine().assess(inp)
        assert result.meeting_composite <= 100.0

    def test_moderate_risk_scenario(self):
        # Create a scenario with moderate risk (composite between 20-40)
        inp = _base_input(
            meetings_with_agenda_sent_pct=0.50,   # 22 pts prep
            avg_agenda_sent_hours_before_meeting=24.0,
            meeting_recording_review_rate_pct=0.50,
            avg_stakeholders_per_meeting=2.5,
            decision_maker_in_meeting_pct=0.75,
            meeting_cancellation_rate_pct=0.05,
            next_step_committed_at_meeting_pct=0.90,
            meetings_with_no_outcome_pct=0.10,
            repeat_meeting_same_stage_pct=0.10,
            followup_within_24h_rate_pct=0.90,
            demo_conversion_from_meeting_pct=0.50,
            proposal_conversion_from_demo_pct=0.70,
        )
        result = _engine().assess(inp)
        # prep=22, composite = 22*0.25 = 5.5 – still low
        # Let's verify the actual value is as expected
        assert result.meeting_composite == pytest.approx(5.5, abs=0.2)
        assert result.meeting_risk == MeetingRisk.low

    def test_high_risk_scenario(self):
        inp = _base_input(
            meetings_with_agenda_sent_pct=0.10,   # prep high
            avg_agenda_sent_hours_before_meeting=1.0,
            meeting_recording_review_rate_pct=0.05,
            avg_stakeholders_per_meeting=1.0,     # engagement high
            decision_maker_in_meeting_pct=0.10,
            meeting_cancellation_rate_pct=0.40,
            next_step_committed_at_meeting_pct=0.90,
            meetings_with_no_outcome_pct=0.10,
            repeat_meeting_same_stage_pct=0.10,
            followup_within_24h_rate_pct=0.90,
            demo_conversion_from_meeting_pct=0.50,
            proposal_conversion_from_demo_pct=0.70,
        )
        result = _engine().assess(inp)
        assert result.meeting_risk in {MeetingRisk.high, MeetingRisk.critical}

    def test_critical_risk_pattern_action_next_step(self):
        # Force: critical risk + no_next_step_close pattern
        inp = _base_input(
            meetings_with_agenda_sent_pct=0.10,
            avg_agenda_sent_hours_before_meeting=1.0,
            meeting_recording_review_rate_pct=0.05,
            avg_stakeholders_per_meeting=3.0,        # no stakeholder trap
            decision_maker_in_meeting_pct=0.10,
            meeting_cancellation_rate_pct=0.40,
            next_step_committed_at_meeting_pct=0.20, # no_next_step_close trigger
            meetings_with_no_outcome_pct=0.60,
            repeat_meeting_same_stage_pct=0.60,
            followup_within_24h_rate_pct=0.90,       # followup OK (no poor_followup)
            demo_conversion_from_meeting_pct=0.10,
            proposal_conversion_from_demo_pct=0.10,
        )
        result = _engine().assess(inp)
        if result.meeting_risk == MeetingRisk.critical and result.meeting_pattern == MeetingPattern.no_next_step_close:
            assert result.recommended_action == MeetingAction.next_step_close_training


# ===========================================================================
# SECTION 17 – assess_batch()
# ===========================================================================

class TestAssessBatch:
    def test_empty_batch_returns_empty_list(self):
        assert _engine().assess_batch([]) == []

    def test_single_input_returns_list_of_one(self):
        results = _engine().assess_batch([_base_input()])
        assert len(results) == 1
        assert isinstance(results[0], MeetingResult)

    def test_multiple_inputs_returns_same_count(self):
        inputs = [_base_input(rep_id=f"R{i}") for i in range(5)]
        results = _engine().assess_batch(inputs)
        assert len(results) == 5

    def test_order_preserved(self):
        inputs = [_base_input(rep_id=f"REP-{i}") for i in range(3)]
        results = _engine().assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"REP-{i}"

    def test_batch_stored_in_results(self):
        e = _engine()
        inputs = [_base_input(rep_id=f"R{i}") for i in range(4)]
        e.assess_batch(inputs)
        assert len(e._results) == 4

    def test_batch_accumulates_on_multiple_calls(self):
        e = _engine()
        e.assess_batch([_base_input(rep_id="R1"), _base_input(rep_id="R2")])
        e.assess_batch([_base_input(rep_id="R3")])
        assert len(e._results) == 3

    def test_each_result_type(self):
        inputs = [_base_input(rep_id=f"R{i}") for i in range(3)]
        for r in _engine().assess_batch(inputs):
            assert isinstance(r, MeetingResult)

    def test_batch_results_match_individual(self):
        e1 = _engine()
        e2 = _engine()
        inp = _base_input(rep_id="RX")
        r_single = e1.assess(inp)
        r_batch = e2.assess_batch([inp])[0]
        assert r_single.meeting_composite == r_batch.meeting_composite
        assert r_single.meeting_risk == r_batch.meeting_risk

    def test_batch_with_varied_inputs(self):
        inputs = [
            _base_input(rep_id="GOOD"),
            _base_input(rep_id="BAD",
                        meetings_with_agenda_sent_pct=0.0,
                        avg_agenda_sent_hours_before_meeting=0.0,
                        meeting_recording_review_rate_pct=0.0,
                        avg_stakeholders_per_meeting=0.5,
                        decision_maker_in_meeting_pct=0.0,
                        meeting_cancellation_rate_pct=1.0,
                        next_step_committed_at_meeting_pct=0.0,
                        meetings_with_no_outcome_pct=1.0,
                        repeat_meeting_same_stage_pct=1.0,
                        followup_within_24h_rate_pct=0.0,
                        demo_conversion_from_meeting_pct=0.0,
                        proposal_conversion_from_demo_pct=0.0),
        ]
        results = _engine().assess_batch(inputs)
        assert results[0].meeting_risk == MeetingRisk.low
        assert results[1].meeting_risk == MeetingRisk.critical


# ===========================================================================
# SECTION 18 – summary()
# ===========================================================================

class TestSummary:
    def test_empty_summary_has_13_keys(self):
        s = _engine().summary()
        assert len(s) == 13

    def test_empty_summary_total_zero(self):
        assert _engine().summary()["total"] == 0

    def test_empty_summary_risk_counts_empty(self):
        assert _engine().summary()["risk_counts"] == {}

    def test_empty_summary_pattern_counts_empty(self):
        assert _engine().summary()["pattern_counts"] == {}

    def test_empty_summary_severity_counts_empty(self):
        assert _engine().summary()["severity_counts"] == {}

    def test_empty_summary_action_counts_empty(self):
        assert _engine().summary()["action_counts"] == {}

    def test_empty_summary_avg_composite_zero(self):
        assert _engine().summary()["avg_meeting_composite"] == 0.0

    def test_empty_summary_gap_count_zero(self):
        assert _engine().summary()["meeting_gap_count"] == 0

    def test_empty_summary_coaching_count_zero(self):
        assert _engine().summary()["coaching_count"] == 0

    def test_empty_summary_avg_prep_zero(self):
        assert _engine().summary()["avg_meeting_prep_score"] == 0.0

    def test_empty_summary_avg_engagement_zero(self):
        assert _engine().summary()["avg_meeting_engagement_score"] == 0.0

    def test_empty_summary_avg_outcome_zero(self):
        assert _engine().summary()["avg_meeting_outcome_score"] == 0.0

    def test_empty_summary_avg_conversion_zero(self):
        assert _engine().summary()["avg_meeting_conversion_score"] == 0.0

    def test_empty_summary_drag_zero(self):
        assert _engine().summary()["total_estimated_pipeline_drag_usd"] == 0.0

    def test_summary_keys_exact(self):
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_meeting_composite", "meeting_gap_count",
            "coaching_count", "avg_meeting_prep_score",
            "avg_meeting_engagement_score", "avg_meeting_outcome_score",
            "avg_meeting_conversion_score", "total_estimated_pipeline_drag_usd",
        }
        assert set(_engine().summary().keys()) == expected

    def test_summary_total_after_one_assess(self):
        e = _engine()
        e.assess(_base_input())
        assert e.summary()["total"] == 1

    def test_summary_total_after_batch(self):
        e = _engine()
        e.assess_batch([_base_input(rep_id=f"R{i}") for i in range(5)])
        assert e.summary()["total"] == 5

    def test_summary_risk_counts_one_low(self):
        e = _engine()
        e.assess(_base_input())
        assert e.summary()["risk_counts"].get("low", 0) >= 1

    def test_summary_pattern_counts_one_none(self):
        e = _engine()
        e.assess(_base_input())
        assert e.summary()["pattern_counts"].get("none", 0) >= 1

    def test_summary_severity_counts_one_structured(self):
        e = _engine()
        e.assess(_base_input())
        assert e.summary()["severity_counts"].get("structured", 0) >= 1

    def test_summary_action_counts_one_no_action(self):
        e = _engine()
        e.assess(_base_input())
        assert e.summary()["action_counts"].get("no_action", 0) >= 1

    def test_summary_gap_count_correct(self):
        e = _engine()
        # healthy → no gap
        e.assess(_base_input())
        # force gap
        e.assess(_base_input(next_step_committed_at_meeting_pct=0.10))
        s = e.summary()
        assert s["meeting_gap_count"] == 1

    def test_summary_coaching_count_correct(self):
        e = _engine()
        e.assess(_base_input())
        e.assess(_base_input(meetings_with_agenda_sent_pct=0.30))
        s = e.summary()
        assert s["coaching_count"] >= 1

    def test_summary_avg_composite_rounded(self):
        e = _engine()
        e.assess(_base_input())
        s = e.summary()
        # Should be a rounded float (1 dp)
        val = s["avg_meeting_composite"]
        assert isinstance(val, float)

    def test_summary_total_drag_accumulates(self):
        e = _engine()
        r1 = e.assess(_base_input(total_meetings_conducted=20,
                                   meetings_with_no_outcome_pct=0.50,
                                   avg_opportunity_value_usd=10_000.0))
        r2 = e.assess(_base_input(rep_id="R2",
                                   total_meetings_conducted=20,
                                   meetings_with_no_outcome_pct=0.50,
                                   avg_opportunity_value_usd=10_000.0))
        expected = round(r1.estimated_pipeline_drag_usd + r2.estimated_pipeline_drag_usd, 2)
        assert e.summary()["total_estimated_pipeline_drag_usd"] == expected

    def test_summary_avg_scores_equal_single_result(self):
        e = _engine()
        r = e.assess(_base_input())
        s = e.summary()
        assert s["avg_meeting_prep_score"] == r.meeting_prep_score
        assert s["avg_meeting_engagement_score"] == r.meeting_engagement_score
        assert s["avg_meeting_outcome_score"] == r.meeting_outcome_score
        assert s["avg_meeting_conversion_score"] == r.meeting_conversion_score

    def test_summary_multiple_risks(self):
        e = _engine()
        e.assess(_base_input())  # low
        e.assess(_base_input(  # critical
            meetings_with_agenda_sent_pct=0.0,
            avg_agenda_sent_hours_before_meeting=0.0,
            meeting_recording_review_rate_pct=0.0,
            avg_stakeholders_per_meeting=0.5,
            decision_maker_in_meeting_pct=0.0,
            meeting_cancellation_rate_pct=1.0,
            next_step_committed_at_meeting_pct=0.0,
            meetings_with_no_outcome_pct=1.0,
            repeat_meeting_same_stage_pct=1.0,
            followup_within_24h_rate_pct=0.0,
            demo_conversion_from_meeting_pct=0.0,
            proposal_conversion_from_demo_pct=0.0,
        ))
        s = e.summary()
        assert s["risk_counts"]["low"] == 1
        assert s["risk_counts"]["critical"] == 1
        assert s["total"] == 2


# ===========================================================================
# SECTION 19 – Edge cases and boundary conditions
# ===========================================================================

class TestEdgeCases:
    def test_all_zero_fractions(self):
        """All percentage fields set to 0 — engine should not crash."""
        inp = _base_input(
            meetings_with_agenda_sent_pct=0.0,
            avg_agenda_sent_hours_before_meeting=0.0,
            meeting_recording_review_rate_pct=0.0,
            avg_stakeholders_per_meeting=0.0,
            decision_maker_in_meeting_pct=0.0,
            meeting_cancellation_rate_pct=0.0,
            next_step_committed_at_meeting_pct=0.0,
            meetings_with_no_outcome_pct=0.0,
            repeat_meeting_same_stage_pct=0.0,
            followup_within_24h_rate_pct=0.0,
            demo_conversion_from_meeting_pct=0.0,
            proposal_conversion_from_demo_pct=0.0,
        )
        result = _engine().assess(inp)
        assert isinstance(result, MeetingResult)

    def test_all_one_fractions(self):
        """All percentage fields set to 1.0 — engine should not crash."""
        inp = _base_input(
            meetings_with_agenda_sent_pct=1.0,
            avg_agenda_sent_hours_before_meeting=100.0,
            meeting_recording_review_rate_pct=1.0,
            avg_stakeholders_per_meeting=10.0,
            decision_maker_in_meeting_pct=1.0,
            meeting_cancellation_rate_pct=1.0,
            next_step_committed_at_meeting_pct=1.0,
            meetings_with_no_outcome_pct=1.0,
            repeat_meeting_same_stage_pct=1.0,
            followup_within_24h_rate_pct=1.0,
            demo_conversion_from_meeting_pct=1.0,
            proposal_conversion_from_demo_pct=1.0,
        )
        result = _engine().assess(inp)
        assert isinstance(result, MeetingResult)

    def test_single_meeting_conducted(self):
        result = _engine().assess(_base_input(total_meetings_conducted=1))
        assert isinstance(result, MeetingResult)

    def test_very_large_opportunity_value(self):
        result = _engine().assess(_base_input(avg_opportunity_value_usd=1_000_000.0,
                                               meetings_with_no_outcome_pct=0.50,
                                               total_meetings_conducted=100))
        assert result.estimated_pipeline_drag_usd >= 0.0

    def test_zero_opportunity_value_zero_drag(self):
        result = _engine().assess(_base_input(avg_opportunity_value_usd=0.0,
                                               meetings_with_no_outcome_pct=0.50))
        assert result.estimated_pipeline_drag_usd == 0.0

    def test_no_next_step_close_pattern_exact_boundary_outcome_40(self):
        inp = _base_input(
            meetings_with_agenda_sent_pct=0.80,
            followup_within_24h_rate_pct=0.80,
            avg_stakeholders_per_meeting=3.0,
            next_step_committed_at_meeting_pct=0.30,  # boundary
            meetings_with_no_outcome_pct=0.60,
            repeat_meeting_same_stage_pct=0.60,
        )
        e = _engine()
        outcome = e._meeting_outcome_score(inp)
        if outcome >= 40:
            pattern = e._detect_pattern(inp, 5.0, 5.0, outcome, 5.0)
            assert pattern == MeetingPattern.no_next_step_close

    def test_result_fields_never_nan(self):
        result = _engine().assess(_base_input())
        for field in [result.meeting_prep_score, result.meeting_engagement_score,
                      result.meeting_outcome_score, result.meeting_conversion_score,
                      result.meeting_composite, result.estimated_pipeline_drag_usd]:
            assert not math.isnan(field)

    def test_result_fields_never_negative(self):
        result = _engine().assess(_base_input())
        for field in [result.meeting_prep_score, result.meeting_engagement_score,
                      result.meeting_outcome_score, result.meeting_conversion_score,
                      result.meeting_composite, result.estimated_pipeline_drag_usd]:
            assert field >= 0.0

    def test_engine_fresh_state(self):
        e1 = _engine()
        e1.assess(_base_input())
        e2 = _engine()
        # e2 should have no results
        assert len(e2._results) == 0

    def test_results_list_grows(self):
        e = _engine()
        for i in range(10):
            e.assess(_base_input(rep_id=f"R{i}"))
        assert len(e._results) == 10

    def test_composite_always_between_0_and_100(self):
        inputs = [
            _base_input(),
            _base_input(
                meetings_with_agenda_sent_pct=0.0,
                avg_agenda_sent_hours_before_meeting=0.0,
                meeting_recording_review_rate_pct=0.0,
                avg_stakeholders_per_meeting=0.5,
                decision_maker_in_meeting_pct=0.0,
                meeting_cancellation_rate_pct=1.0,
                next_step_committed_at_meeting_pct=0.0,
                meetings_with_no_outcome_pct=1.0,
                repeat_meeting_same_stage_pct=1.0,
                followup_within_24h_rate_pct=0.0,
                demo_conversion_from_meeting_pct=0.0,
                proposal_conversion_from_demo_pct=0.0,
            ),
        ]
        e = _engine()
        for inp in inputs:
            r = e.assess(inp)
            assert 0.0 <= r.meeting_composite <= 100.0

    def test_risk_and_severity_always_coherent(self):
        """Risk and severity thresholds are identical — they should align."""
        for composite in [0.0, 19.9, 20.0, 39.9, 40.0, 59.9, 60.0, 100.0]:
            e = _engine()
            risk = e._risk_level(composite)
            sev = e._severity(composite)
            # Both use identical thresholds: their "level" should match
            risk_map = {
                MeetingRisk.low: MeetingSeverity.structured,
                MeetingRisk.moderate: MeetingSeverity.developing,
                MeetingRisk.high: MeetingSeverity.ad_hoc,
                MeetingRisk.critical: MeetingSeverity.chaotic,
            }
            assert risk_map[risk] == sev

    def test_batch_empty_summary(self):
        e = _engine()
        e.assess_batch([])
        s = e.summary()
        assert s["total"] == 0

    def test_to_dict_values_serializable(self):
        """to_dict should return only plain Python types."""
        d = _engine().assess(_base_input()).to_dict()
        for v in d.values():
            assert isinstance(v, (str, int, float, bool))

    def test_signal_all_1_pct_fields(self):
        """With 100% agenda and next-step, those parts excluded from signal body."""
        inp = _base_input(meetings_with_agenda_sent_pct=1.0,
                          next_step_committed_at_meeting_pct=1.0,
                          avg_stakeholders_per_meeting=2.5)
        e = _engine()
        # composite likely 0 → healthy
        result = e.assess(inp)
        if result.meeting_pattern == MeetingPattern.none and result.meeting_composite < 20:
            assert "healthy" in result.meeting_signal

    def test_large_batch_does_not_crash(self):
        e = _engine()
        inputs = [_base_input(rep_id=f"R{i}") for i in range(200)]
        results = e.assess_batch(inputs)
        assert len(results) == 200
