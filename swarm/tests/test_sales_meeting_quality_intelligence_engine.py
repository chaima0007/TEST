"""
Comprehensive pytest test suite for SalesMeetingQualityIntelligenceEngine.
~300 tests covering enums, sub-scores, pattern detection, risk/severity/action
classification, flag logic, revenue at risk, signal strings, to_dict, summary,
assess_batch, and edge cases.
"""
import pytest
from swarm.intelligence.sales_meeting_quality_intelligence_engine import (
    SalesMeetingQualityIntelligenceEngine,
    MeetingQualityInput,
    MeetingQualityResult,
    MeetingRisk,
    MeetingPattern,
    MeetingSeverity,
    MeetingAction,
)


# ---------------------------------------------------------------------------
# Helper factory
# ---------------------------------------------------------------------------

def make_input(**kwargs):
    defaults = dict(
        rep_id="rep_test",
        region="West",
        evaluation_period_id="Q1-2026",
        total_meetings_held=20,
        meetings_with_agenda_set=16,
        meetings_with_decision_maker=10,
        meetings_with_champion_only=4,
        meetings_resulting_in_next_step=15,
        meetings_with_follow_up_sent_24h=14,
        avg_meeting_prep_score=7.5,
        avg_attendees_per_meeting=2.8,
        executive_attendee_rate_pct=0.40,
        demo_meetings_count=5,
        demo_to_proposal_conversion_rate_pct=0.70,
        discovery_meetings_count=6,
        discovery_to_demo_conversion_rate_pct=0.65,
        meetings_cancelled_by_prospect=2,
        meetings_rescheduled_count=2,
        avg_deal_stage_advancement_per_meeting=0.35,
        multi_stakeholder_meetings_pct=0.60,
        avg_deal_size_in_meetings_usd=60000.0,
        meetings_leading_to_proposal_count=4,
    )
    defaults.update(kwargs)
    return MeetingQualityInput(**defaults)


@pytest.fixture
def engine():
    return SalesMeetingQualityIntelligenceEngine()


@pytest.fixture
def default_input():
    return make_input()


# ===========================================================================
# 1. Enum values
# ===========================================================================

class TestMeetingRiskEnum:
    def test_low_value(self):
        assert MeetingRisk.low == "low"

    def test_moderate_value(self):
        assert MeetingRisk.moderate == "moderate"

    def test_high_value(self):
        assert MeetingRisk.high == "high"

    def test_critical_value(self):
        assert MeetingRisk.critical == "critical"

    def test_is_str_enum(self):
        assert isinstance(MeetingRisk.low, str)

    def test_all_four_members(self):
        assert len(MeetingRisk) == 4

    def test_member_names(self):
        names = {m.name for m in MeetingRisk}
        assert names == {"low", "moderate", "high", "critical"}


class TestMeetingPatternEnum:
    def test_none_value(self):
        assert MeetingPattern.none == "none"

    def test_poor_preparation_value(self):
        assert MeetingPattern.poor_preparation == "poor_preparation"

    def test_no_deal_advancement_value(self):
        assert MeetingPattern.no_deal_advancement == "no_deal_advancement"

    def test_wrong_stakeholders_value(self):
        assert MeetingPattern.wrong_stakeholders == "wrong_stakeholders"

    def test_poor_follow_through_value(self):
        assert MeetingPattern.poor_follow_through == "poor_follow_through"

    def test_pipeline_stall_value(self):
        assert MeetingPattern.pipeline_stall == "pipeline_stall"

    def test_all_six_members(self):
        assert len(MeetingPattern) == 6

    def test_is_str_enum(self):
        assert isinstance(MeetingPattern.none, str)


class TestMeetingSeverityEnum:
    def test_effective_value(self):
        assert MeetingSeverity.effective == "effective"

    def test_developing_value(self):
        assert MeetingSeverity.developing == "developing"

    def test_ineffective_value(self):
        assert MeetingSeverity.ineffective == "ineffective"

    def test_detrimental_value(self):
        assert MeetingSeverity.detrimental == "detrimental"

    def test_all_four_members(self):
        assert len(MeetingSeverity) == 4

    def test_is_str_enum(self):
        assert isinstance(MeetingSeverity.effective, str)


class TestMeetingActionEnum:
    def test_no_action_value(self):
        assert MeetingAction.no_action == "no_action"

    def test_meeting_preparation_coaching_value(self):
        assert MeetingAction.meeting_preparation_coaching == "meeting_preparation_coaching"

    def test_deal_advancement_review_value(self):
        assert MeetingAction.deal_advancement_review == "deal_advancement_review"

    def test_stakeholder_strategy_value(self):
        assert MeetingAction.stakeholder_strategy == "stakeholder_strategy"

    def test_follow_through_training_value(self):
        assert MeetingAction.follow_through_training == "follow_through_training"

    def test_meeting_cadence_reset_value(self):
        assert MeetingAction.meeting_cadence_reset == "meeting_cadence_reset"

    def test_all_six_members(self):
        assert len(MeetingAction) == 6

    def test_is_str_enum(self):
        assert isinstance(MeetingAction.no_action, str)


# ===========================================================================
# 2. Sub-scores
# ===========================================================================

class TestMeetingPreparationScore:
    """_meeting_preparation_score: 0-100, higher = more risk."""

    def setup_method(self):
        self.engine = SalesMeetingQualityIntelligenceEngine()

    def _score(self, **kwargs):
        return self.engine._meeting_preparation_score(make_input(**kwargs))

    # agenda_rate thresholds
    def test_agenda_rate_zero_adds_40(self):
        s = self._score(meetings_with_agenda_set=0, total_meetings_held=20)
        assert s >= 40.0

    def test_agenda_rate_below_30_adds_40(self):
        # 5/20 = 0.25 < 0.30
        s = self._score(meetings_with_agenda_set=5, total_meetings_held=20)
        assert s >= 40.0

    def test_agenda_rate_exactly_30_adds_22(self):
        # 6/20 = 0.30, in [0.30, 0.55) → +22
        s = self._score(meetings_with_agenda_set=6, total_meetings_held=20)
        assert s >= 22.0

    def test_agenda_rate_between_30_and_55_adds_22(self):
        # 10/20 = 0.50
        s = self._score(meetings_with_agenda_set=10, total_meetings_held=20)
        assert s >= 22.0

    def test_agenda_rate_exactly_55_adds_8(self):
        # 11/20 = 0.55, in [0.55, 0.75) → +8
        s = self._score(meetings_with_agenda_set=11, total_meetings_held=20)
        assert s >= 8.0

    def test_agenda_rate_between_55_and_75_adds_8(self):
        # 14/20 = 0.70
        s = self._score(meetings_with_agenda_set=14, total_meetings_held=20)
        assert s >= 8.0

    def test_agenda_rate_exactly_75_adds_0(self):
        # 15/20 = 0.75 → 0
        base = self._score(meetings_with_agenda_set=15, total_meetings_held=20,
                           avg_meeting_prep_score=10.0, avg_attendees_per_meeting=3.0)
        assert base == 0.0

    def test_agenda_rate_100_adds_0(self):
        s = self._score(meetings_with_agenda_set=20, total_meetings_held=20,
                        avg_meeting_prep_score=10.0, avg_attendees_per_meeting=3.0)
        assert s == 0.0

    # prep score thresholds
    def test_prep_score_below_3_adds_35(self):
        s = self._score(avg_meeting_prep_score=2.9,
                        meetings_with_agenda_set=20, avg_attendees_per_meeting=3.0)
        assert s >= 35.0

    def test_prep_score_zero_adds_35(self):
        s = self._score(avg_meeting_prep_score=0.0,
                        meetings_with_agenda_set=20, avg_attendees_per_meeting=3.0)
        assert s >= 35.0

    def test_prep_score_exactly_3_adds_18(self):
        # 3.0 in [3.0, 5.0) → +18
        s = self._score(avg_meeting_prep_score=3.0,
                        meetings_with_agenda_set=20, avg_attendees_per_meeting=3.0)
        assert s >= 18.0

    def test_prep_score_between_3_and_5_adds_18(self):
        s = self._score(avg_meeting_prep_score=4.0,
                        meetings_with_agenda_set=20, avg_attendees_per_meeting=3.0)
        assert s >= 18.0

    def test_prep_score_exactly_5_adds_7(self):
        # 5.0 in [5.0, 7.0) → +7
        s = self._score(avg_meeting_prep_score=5.0,
                        meetings_with_agenda_set=20, avg_attendees_per_meeting=3.0)
        assert s >= 7.0

    def test_prep_score_between_5_and_7_adds_7(self):
        s = self._score(avg_meeting_prep_score=6.0,
                        meetings_with_agenda_set=20, avg_attendees_per_meeting=3.0)
        assert s >= 7.0

    def test_prep_score_exactly_7_adds_0(self):
        s = self._score(avg_meeting_prep_score=7.0,
                        meetings_with_agenda_set=20, avg_attendees_per_meeting=3.0)
        assert s == 0.0

    def test_prep_score_10_adds_0(self):
        s = self._score(avg_meeting_prep_score=10.0,
                        meetings_with_agenda_set=20, avg_attendees_per_meeting=3.0)
        assert s == 0.0

    # attendees thresholds
    def test_attendees_below_1_5_adds_15(self):
        s = self._score(avg_attendees_per_meeting=1.0,
                        meetings_with_agenda_set=20, avg_meeting_prep_score=10.0)
        assert s >= 15.0

    def test_attendees_exactly_1_5_adds_7(self):
        # 1.5 in [1.5, 2.0) → +7
        s = self._score(avg_attendees_per_meeting=1.5,
                        meetings_with_agenda_set=20, avg_meeting_prep_score=10.0)
        assert s >= 7.0

    def test_attendees_between_1_5_and_2_adds_7(self):
        s = self._score(avg_attendees_per_meeting=1.8,
                        meetings_with_agenda_set=20, avg_meeting_prep_score=10.0)
        assert s >= 7.0

    def test_attendees_exactly_2_adds_0(self):
        s = self._score(avg_attendees_per_meeting=2.0,
                        meetings_with_agenda_set=20, avg_meeting_prep_score=10.0)
        assert s == 0.0

    def test_score_capped_at_100(self):
        # worst case: all bad → max=40+35+15=90, still capped correctly
        s = self._score(
            meetings_with_agenda_set=0, avg_meeting_prep_score=0.0,
            avg_attendees_per_meeting=0.5, total_meetings_held=20
        )
        assert s == 90.0  # 40+35+15=90; cap is 100 but natural max is 90

    def test_zero_total_uses_max1(self):
        # total_meetings_held=0 → uses max(0,1)=1, agenda_set=0 → agenda_rate=0
        s = self._score(total_meetings_held=0, meetings_with_agenda_set=0,
                        avg_meeting_prep_score=10.0, avg_attendees_per_meeting=3.0)
        assert s >= 40.0

    def test_default_input_score_is_non_negative(self):
        s = self._score()
        assert s >= 0.0


class TestMeetingOutcomeScore:
    """_meeting_outcome_score: 0-100."""

    def setup_method(self):
        self.engine = SalesMeetingQualityIntelligenceEngine()

    def _score(self, **kwargs):
        return self.engine._meeting_outcome_score(make_input(**kwargs))

    def test_next_step_rate_below_35_adds_40(self):
        # 6/20 = 0.30
        s = self._score(meetings_resulting_in_next_step=6)
        assert s >= 40.0

    def test_next_step_rate_exactly_35_adds_22(self):
        # 7/20 = 0.35
        s = self._score(meetings_resulting_in_next_step=7,
                        avg_deal_stage_advancement_per_meeting=0.50,
                        demo_meetings_count=0, discovery_meetings_count=0)
        assert s >= 22.0

    def test_next_step_rate_between_35_and_55_adds_22(self):
        # 10/20 = 0.50
        s = self._score(meetings_resulting_in_next_step=10,
                        avg_deal_stage_advancement_per_meeting=0.50,
                        demo_meetings_count=0, discovery_meetings_count=0)
        assert s >= 22.0

    def test_next_step_rate_exactly_55_adds_8(self):
        # 11/20 = 0.55
        s = self._score(meetings_resulting_in_next_step=11,
                        avg_deal_stage_advancement_per_meeting=0.50,
                        demo_meetings_count=0, discovery_meetings_count=0)
        assert s >= 8.0

    def test_next_step_rate_between_55_and_70_adds_8(self):
        # 13/20 = 0.65
        s = self._score(meetings_resulting_in_next_step=13,
                        avg_deal_stage_advancement_per_meeting=0.50,
                        demo_meetings_count=0, discovery_meetings_count=0)
        assert s >= 8.0

    def test_next_step_rate_at_70_adds_0(self):
        # 14/20 = 0.70
        s = self._score(meetings_resulting_in_next_step=14,
                        avg_deal_stage_advancement_per_meeting=0.50,
                        demo_meetings_count=0, discovery_meetings_count=0)
        assert s == 0.0

    def test_advancement_below_10_adds_30(self):
        s = self._score(avg_deal_stage_advancement_per_meeting=0.05,
                        meetings_resulting_in_next_step=20,
                        demo_meetings_count=0, discovery_meetings_count=0)
        assert s >= 30.0

    def test_advancement_exactly_10_adds_15(self):
        s = self._score(avg_deal_stage_advancement_per_meeting=0.10,
                        meetings_resulting_in_next_step=20,
                        demo_meetings_count=0, discovery_meetings_count=0)
        assert s >= 15.0

    def test_advancement_between_10_and_25_adds_15(self):
        s = self._score(avg_deal_stage_advancement_per_meeting=0.20,
                        meetings_resulting_in_next_step=20,
                        demo_meetings_count=0, discovery_meetings_count=0)
        assert s >= 15.0

    def test_advancement_at_25_adds_0(self):
        s = self._score(avg_deal_stage_advancement_per_meeting=0.25,
                        meetings_resulting_in_next_step=20,
                        demo_meetings_count=0, discovery_meetings_count=0)
        assert s == 0.0

    def test_demo_conversion_below_30_adds_20(self):
        s = self._score(demo_meetings_count=5,
                        demo_to_proposal_conversion_rate_pct=0.20,
                        meetings_resulting_in_next_step=20,
                        avg_deal_stage_advancement_per_meeting=0.50,
                        discovery_meetings_count=0)
        assert s >= 20.0

    def test_demo_conversion_exactly_30_adds_10(self):
        s = self._score(demo_meetings_count=5,
                        demo_to_proposal_conversion_rate_pct=0.30,
                        meetings_resulting_in_next_step=20,
                        avg_deal_stage_advancement_per_meeting=0.50,
                        discovery_meetings_count=0)
        assert s >= 10.0

    def test_demo_conversion_between_30_and_50_adds_10(self):
        s = self._score(demo_meetings_count=5,
                        demo_to_proposal_conversion_rate_pct=0.45,
                        meetings_resulting_in_next_step=20,
                        avg_deal_stage_advancement_per_meeting=0.50,
                        discovery_meetings_count=0)
        assert s >= 10.0

    def test_demo_conversion_at_50_adds_0(self):
        s = self._score(demo_meetings_count=5,
                        demo_to_proposal_conversion_rate_pct=0.50,
                        meetings_resulting_in_next_step=20,
                        avg_deal_stage_advancement_per_meeting=0.50,
                        discovery_meetings_count=0)
        assert s == 0.0

    def test_demo_count_zero_no_demo_penalty(self):
        # demo_meetings_count=0 → no penalty from demo conversion
        s_no_demo = self._score(demo_meetings_count=0,
                                demo_to_proposal_conversion_rate_pct=0.10,
                                meetings_resulting_in_next_step=20,
                                avg_deal_stage_advancement_per_meeting=0.50,
                                discovery_meetings_count=0)
        assert s_no_demo == 0.0

    def test_discovery_conversion_below_40_adds_10(self):
        s = self._score(discovery_meetings_count=5,
                        discovery_to_demo_conversion_rate_pct=0.30,
                        meetings_resulting_in_next_step=20,
                        avg_deal_stage_advancement_per_meeting=0.50,
                        demo_meetings_count=0)
        assert s >= 10.0

    def test_discovery_conversion_at_40_adds_0(self):
        s = self._score(discovery_meetings_count=5,
                        discovery_to_demo_conversion_rate_pct=0.40,
                        meetings_resulting_in_next_step=20,
                        avg_deal_stage_advancement_per_meeting=0.50,
                        demo_meetings_count=0)
        assert s == 0.0

    def test_discovery_count_zero_no_discovery_penalty(self):
        s = self._score(discovery_meetings_count=0,
                        discovery_to_demo_conversion_rate_pct=0.10,
                        meetings_resulting_in_next_step=20,
                        avg_deal_stage_advancement_per_meeting=0.50,
                        demo_meetings_count=0)
        assert s == 0.0

    def test_score_capped_at_100(self):
        s = self._score(
            meetings_resulting_in_next_step=0,
            avg_deal_stage_advancement_per_meeting=0.0,
            demo_meetings_count=5,
            demo_to_proposal_conversion_rate_pct=0.10,
            discovery_meetings_count=5,
            discovery_to_demo_conversion_rate_pct=0.10,
        )
        assert s == 100.0

    def test_perfect_outcome_score_zero(self):
        s = self._score(
            meetings_resulting_in_next_step=20,
            avg_deal_stage_advancement_per_meeting=0.50,
            demo_meetings_count=5,
            demo_to_proposal_conversion_rate_pct=1.0,
            discovery_meetings_count=5,
            discovery_to_demo_conversion_rate_pct=1.0,
        )
        assert s == 0.0


class TestStakeholderCoverageScore:
    """_stakeholder_coverage_score: 0-100."""

    def setup_method(self):
        self.engine = SalesMeetingQualityIntelligenceEngine()

    def _score(self, **kwargs):
        return self.engine._stakeholder_coverage_score(make_input(**kwargs))

    def test_dm_rate_below_20_adds_40(self):
        # 3/20 = 0.15
        s = self._score(meetings_with_decision_maker=3,
                        executive_attendee_rate_pct=1.0,
                        multi_stakeholder_meetings_pct=1.0,
                        meetings_with_champion_only=0)
        assert s >= 40.0

    def test_dm_rate_exactly_20_adds_22(self):
        # 4/20 = 0.20
        s = self._score(meetings_with_decision_maker=4,
                        executive_attendee_rate_pct=1.0,
                        multi_stakeholder_meetings_pct=1.0,
                        meetings_with_champion_only=0)
        assert s >= 22.0

    def test_dm_rate_between_20_and_40_adds_22(self):
        # 7/20 = 0.35
        s = self._score(meetings_with_decision_maker=7,
                        executive_attendee_rate_pct=1.0,
                        multi_stakeholder_meetings_pct=1.0,
                        meetings_with_champion_only=0)
        assert s >= 22.0

    def test_dm_rate_exactly_40_adds_8(self):
        # 8/20 = 0.40
        s = self._score(meetings_with_decision_maker=8,
                        executive_attendee_rate_pct=1.0,
                        multi_stakeholder_meetings_pct=1.0,
                        meetings_with_champion_only=0)
        assert s >= 8.0

    def test_dm_rate_between_40_and_55_adds_8(self):
        # 9/20 = 0.45
        s = self._score(meetings_with_decision_maker=9,
                        executive_attendee_rate_pct=1.0,
                        multi_stakeholder_meetings_pct=1.0,
                        meetings_with_champion_only=0)
        assert s >= 8.0

    def test_dm_rate_at_55_adds_0(self):
        # 11/20 = 0.55
        s = self._score(meetings_with_decision_maker=11,
                        executive_attendee_rate_pct=1.0,
                        multi_stakeholder_meetings_pct=1.0,
                        meetings_with_champion_only=0)
        assert s == 0.0

    def test_exec_rate_below_15_adds_30(self):
        s = self._score(meetings_with_decision_maker=20,
                        executive_attendee_rate_pct=0.10,
                        multi_stakeholder_meetings_pct=1.0,
                        meetings_with_champion_only=0)
        assert s >= 30.0

    def test_exec_rate_exactly_15_adds_15(self):
        s = self._score(meetings_with_decision_maker=20,
                        executive_attendee_rate_pct=0.15,
                        multi_stakeholder_meetings_pct=1.0,
                        meetings_with_champion_only=0)
        assert s >= 15.0

    def test_exec_rate_between_15_and_30_adds_15(self):
        s = self._score(meetings_with_decision_maker=20,
                        executive_attendee_rate_pct=0.25,
                        multi_stakeholder_meetings_pct=1.0,
                        meetings_with_champion_only=0)
        assert s >= 15.0

    def test_exec_rate_at_30_adds_0(self):
        s = self._score(meetings_with_decision_maker=20,
                        executive_attendee_rate_pct=0.30,
                        multi_stakeholder_meetings_pct=1.0,
                        meetings_with_champion_only=0)
        assert s == 0.0

    def test_multi_stakeholder_below_25_adds_20(self):
        s = self._score(meetings_with_decision_maker=20,
                        executive_attendee_rate_pct=1.0,
                        multi_stakeholder_meetings_pct=0.20,
                        meetings_with_champion_only=0)
        assert s >= 20.0

    def test_multi_stakeholder_exactly_25_adds_10(self):
        s = self._score(meetings_with_decision_maker=20,
                        executive_attendee_rate_pct=1.0,
                        multi_stakeholder_meetings_pct=0.25,
                        meetings_with_champion_only=0)
        assert s >= 10.0

    def test_multi_stakeholder_between_25_and_45_adds_10(self):
        s = self._score(meetings_with_decision_maker=20,
                        executive_attendee_rate_pct=1.0,
                        multi_stakeholder_meetings_pct=0.35,
                        meetings_with_champion_only=0)
        assert s >= 10.0

    def test_multi_stakeholder_at_45_adds_0(self):
        s = self._score(meetings_with_decision_maker=20,
                        executive_attendee_rate_pct=1.0,
                        multi_stakeholder_meetings_pct=0.45,
                        meetings_with_champion_only=0)
        assert s == 0.0

    def test_champion_only_ratio_at_60_adds_10(self):
        # 12/20 = 0.60
        s = self._score(meetings_with_decision_maker=20,
                        executive_attendee_rate_pct=1.0,
                        multi_stakeholder_meetings_pct=1.0,
                        meetings_with_champion_only=12)
        assert s >= 10.0

    def test_champion_only_ratio_at_40_adds_5(self):
        # 8/20 = 0.40
        s = self._score(meetings_with_decision_maker=20,
                        executive_attendee_rate_pct=1.0,
                        multi_stakeholder_meetings_pct=1.0,
                        meetings_with_champion_only=8)
        assert s >= 5.0

    def test_champion_only_ratio_below_40_adds_0(self):
        # 7/20 = 0.35
        s = self._score(meetings_with_decision_maker=20,
                        executive_attendee_rate_pct=1.0,
                        multi_stakeholder_meetings_pct=1.0,
                        meetings_with_champion_only=7)
        assert s == 0.0

    def test_score_capped_at_100(self):
        s = self._score(
            meetings_with_decision_maker=0,
            executive_attendee_rate_pct=0.0,
            multi_stakeholder_meetings_pct=0.0,
            meetings_with_champion_only=20,
        )
        assert s == 100.0

    def test_perfect_stakeholder_score_zero(self):
        s = self._score(
            meetings_with_decision_maker=20,
            executive_attendee_rate_pct=1.0,
            multi_stakeholder_meetings_pct=1.0,
            meetings_with_champion_only=0,
        )
        assert s == 0.0


class TestMeetingDisciplineScore:
    """_meeting_discipline_score: 0-100."""

    def setup_method(self):
        self.engine = SalesMeetingQualityIntelligenceEngine()

    def _score(self, **kwargs):
        return self.engine._meeting_discipline_score(make_input(**kwargs))

    def test_follow_up_rate_below_30_adds_40(self):
        # 5/20 = 0.25
        s = self._score(meetings_with_follow_up_sent_24h=5,
                        meetings_cancelled_by_prospect=0,
                        meetings_rescheduled_count=0)
        assert s >= 40.0

    def test_follow_up_rate_exactly_30_adds_22(self):
        # 6/20 = 0.30
        s = self._score(meetings_with_follow_up_sent_24h=6,
                        meetings_cancelled_by_prospect=0,
                        meetings_rescheduled_count=0)
        assert s >= 22.0

    def test_follow_up_rate_between_30_and_55_adds_22(self):
        # 10/20 = 0.50
        s = self._score(meetings_with_follow_up_sent_24h=10,
                        meetings_cancelled_by_prospect=0,
                        meetings_rescheduled_count=0)
        assert s >= 22.0

    def test_follow_up_rate_exactly_55_adds_8(self):
        # 11/20 = 0.55
        s = self._score(meetings_with_follow_up_sent_24h=11,
                        meetings_cancelled_by_prospect=0,
                        meetings_rescheduled_count=0)
        assert s >= 8.0

    def test_follow_up_rate_between_55_and_75_adds_8(self):
        # 14/20 = 0.70
        s = self._score(meetings_with_follow_up_sent_24h=14,
                        meetings_cancelled_by_prospect=0,
                        meetings_rescheduled_count=0)
        assert s >= 8.0

    def test_follow_up_rate_at_75_adds_0(self):
        # 15/20 = 0.75
        s = self._score(meetings_with_follow_up_sent_24h=15,
                        meetings_cancelled_by_prospect=0,
                        meetings_rescheduled_count=0)
        assert s == 0.0

    def test_cancel_rate_at_30_adds_30(self):
        # 6/20 = 0.30
        s = self._score(meetings_with_follow_up_sent_24h=20,
                        meetings_cancelled_by_prospect=6,
                        meetings_rescheduled_count=0)
        assert s >= 30.0

    def test_cancel_rate_at_20_adds_15(self):
        # 4/20 = 0.20
        s = self._score(meetings_with_follow_up_sent_24h=20,
                        meetings_cancelled_by_prospect=4,
                        meetings_rescheduled_count=0)
        assert s >= 15.0

    def test_cancel_rate_at_10_adds_8(self):
        # 2/20 = 0.10
        s = self._score(meetings_with_follow_up_sent_24h=20,
                        meetings_cancelled_by_prospect=2,
                        meetings_rescheduled_count=0)
        assert s >= 8.0

    def test_cancel_rate_below_10_adds_0(self):
        # 1/20 = 0.05
        s = self._score(meetings_with_follow_up_sent_24h=20,
                        meetings_cancelled_by_prospect=1,
                        meetings_rescheduled_count=0)
        assert s == 0.0

    def test_reschedule_rate_at_30_adds_20(self):
        # 6/20 = 0.30
        s = self._score(meetings_with_follow_up_sent_24h=20,
                        meetings_cancelled_by_prospect=0,
                        meetings_rescheduled_count=6)
        assert s >= 20.0

    def test_reschedule_rate_at_15_adds_10(self):
        # 3/20 = 0.15
        s = self._score(meetings_with_follow_up_sent_24h=20,
                        meetings_cancelled_by_prospect=0,
                        meetings_rescheduled_count=3)
        assert s >= 10.0

    def test_reschedule_rate_below_15_adds_0(self):
        # 2/20 = 0.10
        s = self._score(meetings_with_follow_up_sent_24h=20,
                        meetings_cancelled_by_prospect=0,
                        meetings_rescheduled_count=2)
        assert s == 0.0

    def test_score_capped_at_100(self):
        # natural max: 40+30+20=90; still correctly below cap of 100
        s = self._score(
            meetings_with_follow_up_sent_24h=0,
            meetings_cancelled_by_prospect=20,
            meetings_rescheduled_count=20,
        )
        assert s == 90.0

    def test_perfect_discipline_score_zero(self):
        s = self._score(
            meetings_with_follow_up_sent_24h=20,
            meetings_cancelled_by_prospect=0,
            meetings_rescheduled_count=0,
        )
        assert s == 0.0


# ===========================================================================
# 3. Pattern detection — priority order
# ===========================================================================

class TestPatternDetection:

    def setup_method(self):
        self.engine = SalesMeetingQualityIntelligenceEngine()

    def _pattern(self, **kwargs):
        inp = make_input(**kwargs)
        prep = self.engine._meeting_preparation_score(inp)
        outcome = self.engine._meeting_outcome_score(inp)
        stakeholder = self.engine._stakeholder_coverage_score(inp)
        discipline = self.engine._meeting_discipline_score(inp)
        return self.engine._detect_pattern(inp, prep, outcome, stakeholder, discipline)

    # no_deal_advancement
    def test_no_deal_advancement_detected(self):
        # outcome >= 35, next_step_rate < 0.40, advancement < 0.20
        p = self._pattern(
            meetings_resulting_in_next_step=6,   # 6/20=0.30 < 0.40
            avg_deal_stage_advancement_per_meeting=0.10,  # < 0.20
            # ensure outcome >= 35 by having bad outcome
            demo_meetings_count=5,
            demo_to_proposal_conversion_rate_pct=0.10,
            discovery_meetings_count=0,
        )
        assert p == MeetingPattern.no_deal_advancement

    def test_no_deal_advancement_requires_low_next_step_rate(self):
        # next_step_rate = 0.45 >= 0.40 → should NOT be no_deal_advancement
        p = self._pattern(
            meetings_resulting_in_next_step=9,   # 9/20=0.45
            avg_deal_stage_advancement_per_meeting=0.10,
        )
        assert p != MeetingPattern.no_deal_advancement

    def test_no_deal_advancement_requires_low_advancement(self):
        # advancement >= 0.20 → should NOT be no_deal_advancement
        p = self._pattern(
            meetings_resulting_in_next_step=6,
            avg_deal_stage_advancement_per_meeting=0.20,
        )
        assert p != MeetingPattern.no_deal_advancement

    # wrong_stakeholders
    def test_wrong_stakeholders_detected(self):
        # stakeholder >= 35, dm_rate < 0.30, exec_rate < 0.20
        p = self._pattern(
            meetings_with_decision_maker=4,      # 4/20=0.20 → dm_rate in [0.20,0.40)
            executive_attendee_rate_pct=0.10,    # < 0.20
            multi_stakeholder_meetings_pct=0.10, # adds to stakeholder score
            meetings_with_champion_only=15,      # ratio=0.75 ≥ 0.60 → +10
            # ensure no_deal_advancement does NOT trigger
            meetings_resulting_in_next_step=15,  # 0.75 >= 0.40
            avg_deal_stage_advancement_per_meeting=0.35,
        )
        assert p == MeetingPattern.wrong_stakeholders

    def test_wrong_stakeholders_requires_low_dm_rate(self):
        # dm_rate >= 0.30 → not wrong_stakeholders
        p = self._pattern(
            meetings_with_decision_maker=8,      # 8/20=0.40 ≥ 0.30
            executive_attendee_rate_pct=0.10,
            meetings_resulting_in_next_step=15,
            avg_deal_stage_advancement_per_meeting=0.35,
        )
        assert p != MeetingPattern.wrong_stakeholders

    def test_wrong_stakeholders_requires_low_exec_rate(self):
        # exec_rate >= 0.20 → not wrong_stakeholders
        p = self._pattern(
            meetings_with_decision_maker=4,
            executive_attendee_rate_pct=0.20,
            meetings_resulting_in_next_step=15,
            avg_deal_stage_advancement_per_meeting=0.35,
        )
        assert p != MeetingPattern.wrong_stakeholders

    # poor_follow_through
    def test_poor_follow_through_detected(self):
        # discipline >= 35, follow_up_rate < 0.40
        p = self._pattern(
            meetings_with_follow_up_sent_24h=7,   # 7/20=0.35 < 0.40
            meetings_cancelled_by_prospect=8,     # 8/20=0.40 ≥ 0.30 → +30 to discipline
            meetings_resulting_in_next_step=15,
            avg_deal_stage_advancement_per_meeting=0.35,
            meetings_with_decision_maker=15,
            executive_attendee_rate_pct=0.40,
            multi_stakeholder_meetings_pct=0.60,
            meetings_with_champion_only=0,
        )
        assert p == MeetingPattern.poor_follow_through

    def test_poor_follow_through_requires_low_follow_up_rate(self):
        # follow_up_rate >= 0.40 → not poor_follow_through
        p = self._pattern(
            meetings_with_follow_up_sent_24h=8,   # 8/20=0.40
            meetings_cancelled_by_prospect=8,
            meetings_resulting_in_next_step=15,
            avg_deal_stage_advancement_per_meeting=0.35,
        )
        assert p != MeetingPattern.poor_follow_through

    # poor_preparation
    def test_poor_preparation_detected(self):
        # prep >= 30, agenda_rate < 0.45
        p = self._pattern(
            meetings_with_agenda_set=8,          # 8/20=0.40 < 0.45
            avg_meeting_prep_score=2.0,          # < 3.0 → +35 → prep ≥ 30
            avg_attendees_per_meeting=3.0,
            meetings_resulting_in_next_step=15,
            avg_deal_stage_advancement_per_meeting=0.35,
            meetings_with_decision_maker=15,
            executive_attendee_rate_pct=0.40,
            multi_stakeholder_meetings_pct=0.60,
            meetings_with_champion_only=0,
            meetings_with_follow_up_sent_24h=20,
            meetings_cancelled_by_prospect=0,
            meetings_rescheduled_count=0,
        )
        assert p == MeetingPattern.poor_preparation

    def test_poor_preparation_requires_low_agenda_rate(self):
        # agenda_rate >= 0.45 → not poor_preparation
        p = self._pattern(
            meetings_with_agenda_set=9,          # 9/20=0.45
            avg_meeting_prep_score=2.0,
            avg_attendees_per_meeting=3.0,
            meetings_resulting_in_next_step=15,
            avg_deal_stage_advancement_per_meeting=0.35,
        )
        assert p != MeetingPattern.poor_preparation

    # pipeline_stall
    def test_pipeline_stall_detected(self):
        # demo > 0, meetings_leading_to_proposal_count == 0
        p = self._pattern(
            demo_meetings_count=5,
            meetings_leading_to_proposal_count=0,
            meetings_with_agenda_set=20,
            avg_meeting_prep_score=10.0,
            avg_attendees_per_meeting=3.0,
            meetings_resulting_in_next_step=20,
            avg_deal_stage_advancement_per_meeting=0.50,
            meetings_with_decision_maker=20,
            executive_attendee_rate_pct=0.50,
            multi_stakeholder_meetings_pct=0.80,
            meetings_with_champion_only=0,
            meetings_with_follow_up_sent_24h=20,
            meetings_cancelled_by_prospect=0,
            meetings_rescheduled_count=0,
        )
        assert p == MeetingPattern.pipeline_stall

    def test_pipeline_stall_no_demo_not_stall(self):
        p = self._pattern(
            demo_meetings_count=0,
            meetings_leading_to_proposal_count=0,
            meetings_with_agenda_set=20,
            avg_meeting_prep_score=10.0,
            avg_attendees_per_meeting=3.0,
            meetings_resulting_in_next_step=20,
            avg_deal_stage_advancement_per_meeting=0.50,
            meetings_with_decision_maker=20,
            executive_attendee_rate_pct=0.50,
            multi_stakeholder_meetings_pct=0.80,
            meetings_with_champion_only=0,
            meetings_with_follow_up_sent_24h=20,
            meetings_cancelled_by_prospect=0,
            meetings_rescheduled_count=0,
        )
        assert p == MeetingPattern.none

    def test_pipeline_stall_with_proposal_not_stall(self):
        p = self._pattern(
            demo_meetings_count=5,
            meetings_leading_to_proposal_count=1,
            meetings_with_agenda_set=20,
            avg_meeting_prep_score=10.0,
            avg_attendees_per_meeting=3.0,
            meetings_resulting_in_next_step=20,
            avg_deal_stage_advancement_per_meeting=0.50,
            meetings_with_decision_maker=20,
            executive_attendee_rate_pct=0.50,
            multi_stakeholder_meetings_pct=0.80,
            meetings_with_champion_only=0,
            meetings_with_follow_up_sent_24h=20,
            meetings_cancelled_by_prospect=0,
            meetings_rescheduled_count=0,
        )
        assert p == MeetingPattern.none

    # none
    def test_none_pattern_when_all_good(self):
        p = self._pattern(
            meetings_with_agenda_set=20,
            avg_meeting_prep_score=10.0,
            avg_attendees_per_meeting=3.0,
            meetings_resulting_in_next_step=20,
            avg_deal_stage_advancement_per_meeting=0.50,
            meetings_with_decision_maker=20,
            executive_attendee_rate_pct=0.50,
            multi_stakeholder_meetings_pct=0.80,
            meetings_with_champion_only=0,
            meetings_with_follow_up_sent_24h=20,
            meetings_cancelled_by_prospect=0,
            meetings_rescheduled_count=0,
            demo_meetings_count=5,
            meetings_leading_to_proposal_count=4,
        )
        assert p == MeetingPattern.none

    # priority: no_deal_advancement > wrong_stakeholders
    def test_no_deal_advancement_takes_priority_over_wrong_stakeholders(self):
        # Both conditions met, but no_deal_advancement is higher priority
        p = self._pattern(
            meetings_resulting_in_next_step=6,           # triggers no_deal_advancement
            avg_deal_stage_advancement_per_meeting=0.10,
            meetings_with_decision_maker=4,              # would trigger wrong_stakeholders
            executive_attendee_rate_pct=0.10,
            multi_stakeholder_meetings_pct=0.10,
            meetings_with_champion_only=15,
            demo_meetings_count=5,
            demo_to_proposal_conversion_rate_pct=0.10,
            discovery_meetings_count=0,
        )
        assert p == MeetingPattern.no_deal_advancement


# ===========================================================================
# 4. Risk levels
# ===========================================================================

class TestRiskLevel:

    def setup_method(self):
        self.engine = SalesMeetingQualityIntelligenceEngine()

    def test_composite_below_20_is_low(self):
        assert self.engine._risk_level(0.0) == MeetingRisk.low
        assert self.engine._risk_level(10.0) == MeetingRisk.low
        assert self.engine._risk_level(19.9) == MeetingRisk.low

    def test_composite_exactly_20_is_moderate(self):
        assert self.engine._risk_level(20.0) == MeetingRisk.moderate

    def test_composite_between_20_and_40_is_moderate(self):
        assert self.engine._risk_level(25.0) == MeetingRisk.moderate
        assert self.engine._risk_level(39.9) == MeetingRisk.moderate

    def test_composite_exactly_40_is_high(self):
        assert self.engine._risk_level(40.0) == MeetingRisk.high

    def test_composite_between_40_and_60_is_high(self):
        assert self.engine._risk_level(50.0) == MeetingRisk.high
        assert self.engine._risk_level(59.9) == MeetingRisk.high

    def test_composite_exactly_60_is_critical(self):
        assert self.engine._risk_level(60.0) == MeetingRisk.critical

    def test_composite_above_60_is_critical(self):
        assert self.engine._risk_level(75.0) == MeetingRisk.critical
        assert self.engine._risk_level(100.0) == MeetingRisk.critical


# ===========================================================================
# 5. Severity levels
# ===========================================================================

class TestSeverityLevel:

    def setup_method(self):
        self.engine = SalesMeetingQualityIntelligenceEngine()

    def test_composite_below_20_is_effective(self):
        assert self.engine._severity(0.0) == MeetingSeverity.effective
        assert self.engine._severity(10.0) == MeetingSeverity.effective
        assert self.engine._severity(19.9) == MeetingSeverity.effective

    def test_composite_exactly_20_is_developing(self):
        assert self.engine._severity(20.0) == MeetingSeverity.developing

    def test_composite_between_20_and_40_is_developing(self):
        assert self.engine._severity(25.0) == MeetingSeverity.developing
        assert self.engine._severity(39.9) == MeetingSeverity.developing

    def test_composite_exactly_40_is_ineffective(self):
        assert self.engine._severity(40.0) == MeetingSeverity.ineffective

    def test_composite_between_40_and_60_is_ineffective(self):
        assert self.engine._severity(50.0) == MeetingSeverity.ineffective
        assert self.engine._severity(59.9) == MeetingSeverity.ineffective

    def test_composite_exactly_60_is_detrimental(self):
        assert self.engine._severity(60.0) == MeetingSeverity.detrimental

    def test_composite_above_60_is_detrimental(self):
        assert self.engine._severity(80.0) == MeetingSeverity.detrimental
        assert self.engine._severity(100.0) == MeetingSeverity.detrimental


# ===========================================================================
# 6. Actions
# ===========================================================================

class TestAction:

    def setup_method(self):
        self.engine = SalesMeetingQualityIntelligenceEngine()

    def _action(self, risk, pattern):
        return self.engine._action(risk, pattern)

    # critical risk
    def test_critical_no_deal_advancement(self):
        assert self._action(MeetingRisk.critical, MeetingPattern.no_deal_advancement) == MeetingAction.deal_advancement_review

    def test_critical_wrong_stakeholders(self):
        assert self._action(MeetingRisk.critical, MeetingPattern.wrong_stakeholders) == MeetingAction.stakeholder_strategy

    def test_critical_poor_follow_through(self):
        assert self._action(MeetingRisk.critical, MeetingPattern.poor_follow_through) == MeetingAction.meeting_cadence_reset

    def test_critical_poor_preparation(self):
        assert self._action(MeetingRisk.critical, MeetingPattern.poor_preparation) == MeetingAction.meeting_cadence_reset

    def test_critical_pipeline_stall(self):
        assert self._action(MeetingRisk.critical, MeetingPattern.pipeline_stall) == MeetingAction.meeting_cadence_reset

    def test_critical_none_pattern(self):
        assert self._action(MeetingRisk.critical, MeetingPattern.none) == MeetingAction.meeting_cadence_reset

    # high risk
    def test_high_poor_preparation(self):
        assert self._action(MeetingRisk.high, MeetingPattern.poor_preparation) == MeetingAction.meeting_preparation_coaching

    def test_high_poor_follow_through(self):
        assert self._action(MeetingRisk.high, MeetingPattern.poor_follow_through) == MeetingAction.follow_through_training

    def test_high_no_deal_advancement(self):
        assert self._action(MeetingRisk.high, MeetingPattern.no_deal_advancement) == MeetingAction.deal_advancement_review

    def test_high_wrong_stakeholders(self):
        assert self._action(MeetingRisk.high, MeetingPattern.wrong_stakeholders) == MeetingAction.deal_advancement_review

    def test_high_pipeline_stall(self):
        assert self._action(MeetingRisk.high, MeetingPattern.pipeline_stall) == MeetingAction.deal_advancement_review

    def test_high_none_pattern(self):
        assert self._action(MeetingRisk.high, MeetingPattern.none) == MeetingAction.deal_advancement_review

    # moderate risk
    def test_moderate_any_pattern(self):
        for pattern in MeetingPattern:
            assert self._action(MeetingRisk.moderate, pattern) == MeetingAction.meeting_preparation_coaching

    # low risk
    def test_low_any_pattern(self):
        for pattern in MeetingPattern:
            assert self._action(MeetingRisk.low, pattern) == MeetingAction.no_action


# ===========================================================================
# 7. has_meeting_effectiveness_gap flag
# ===========================================================================

class TestMeetingEffectivenessGap:

    def setup_method(self):
        self.engine = SalesMeetingQualityIntelligenceEngine()

    def _gap(self, composite, **kwargs):
        return self.engine._has_meeting_effectiveness_gap(composite, make_input(**kwargs))

    def test_composite_at_40_is_gap(self):
        assert self._gap(40.0) is True

    def test_composite_above_40_is_gap(self):
        assert self._gap(50.0) is True

    def test_composite_below_40_but_low_next_step_rate_is_gap(self):
        # next_step_rate = 7/20 = 0.35 < 0.40
        assert self._gap(10.0, meetings_resulting_in_next_step=7) is True

    def test_composite_below_40_but_low_exec_rate_is_gap(self):
        assert self._gap(10.0, executive_attendee_rate_pct=0.10) is True

    def test_composite_below_40_and_next_step_rate_at_40_no_gap_if_exec_ok(self):
        # 8/20 = 0.40 → NOT < 0.40
        assert self._gap(10.0, meetings_resulting_in_next_step=8,
                         executive_attendee_rate_pct=0.50) is False

    def test_no_gap_all_conditions_safe(self):
        # composite < 40, next_step_rate >= 0.40, exec_rate >= 0.15
        assert self._gap(19.9,
                         meetings_resulting_in_next_step=10,   # 10/20=0.50
                         executive_attendee_rate_pct=0.20) is False

    def test_exec_rate_exactly_15_is_gap(self):
        # < 0.15 is gap; 0.15 is NOT < 0.15
        assert self._gap(10.0, meetings_resulting_in_next_step=10,
                         executive_attendee_rate_pct=0.15) is False

    def test_exec_rate_just_below_15_is_gap(self):
        assert self._gap(10.0, meetings_resulting_in_next_step=10,
                         executive_attendee_rate_pct=0.14) is True

    def test_zero_meetings_uses_max1(self):
        # 0/1 = 0 < 0.40 → gap
        result = self.engine._has_meeting_effectiveness_gap(
            10.0,
            make_input(total_meetings_held=0,
                       meetings_resulting_in_next_step=0,
                       executive_attendee_rate_pct=0.50)
        )
        assert result is True


# ===========================================================================
# 8. requires_coaching_intervention flag
# ===========================================================================

class TestRequiresCoachingIntervention:

    def setup_method(self):
        self.engine = SalesMeetingQualityIntelligenceEngine()

    def _coaching(self, composite, **kwargs):
        return self.engine._requires_coaching_intervention(composite, make_input(**kwargs))

    def test_composite_at_30_is_coaching(self):
        assert self._coaching(30.0) is True

    def test_composite_above_30_is_coaching(self):
        assert self._coaching(50.0) is True

    def test_composite_below_30_but_low_agenda_rate_is_coaching(self):
        # 7/20 = 0.35 < 0.40
        assert self._coaching(10.0, meetings_with_agenda_set=7) is True

    def test_composite_below_30_but_low_prep_score_is_coaching(self):
        assert self._coaching(10.0, avg_meeting_prep_score=4.0) is True

    def test_no_coaching_all_conditions_safe(self):
        # composite < 30, agenda_rate >= 0.40, prep_score >= 5.0
        assert self._coaching(20.0,
                              meetings_with_agenda_set=8,  # 8/20=0.40
                              avg_meeting_prep_score=5.0) is False

    def test_agenda_rate_exactly_40_no_coaching_from_agenda(self):
        # 8/20 = 0.40 → NOT < 0.40
        assert self._coaching(20.0,
                              meetings_with_agenda_set=8,
                              avg_meeting_prep_score=5.0) is False

    def test_agenda_rate_just_below_40_is_coaching(self):
        # 7/20 = 0.35 < 0.40
        assert self._coaching(20.0, meetings_with_agenda_set=7,
                              avg_meeting_prep_score=5.0) is True

    def test_prep_score_exactly_5_no_coaching_from_prep(self):
        assert self._coaching(20.0, meetings_with_agenda_set=8,
                              avg_meeting_prep_score=5.0) is False

    def test_prep_score_just_below_5_is_coaching(self):
        assert self._coaching(20.0, meetings_with_agenda_set=8,
                              avg_meeting_prep_score=4.9) is True

    def test_zero_meetings_uses_max1(self):
        # agenda=0/1=0 < 0.40 → coaching
        result = self.engine._requires_coaching_intervention(
            20.0,
            make_input(total_meetings_held=0,
                       meetings_with_agenda_set=0,
                       avg_meeting_prep_score=7.0)
        )
        assert result is True


# ===========================================================================
# 9. estimated_revenue_at_risk_usd
# ===========================================================================

class TestRevenueAtRisk:

    def setup_method(self):
        self.engine = SalesMeetingQualityIntelligenceEngine()

    def _rev(self, composite, **kwargs):
        return self.engine._estimated_revenue_at_risk(make_input(**kwargs), composite)

    def test_basic_calculation(self):
        # stalled = 20 - 15 = 5; rev = 5 * 60000 * 0.20 = 60000.0
        result = self._rev(20.0)
        assert result == 60000.0

    def test_composite_zero_gives_zero_revenue(self):
        result = self._rev(0.0)
        assert result == 0.0

    def test_composite_100_full_risk(self):
        # stalled = 20-15 = 5; rev = 5 * 60000 * 1.0 = 300000.0
        result = self._rev(100.0)
        assert result == 300000.0

    def test_all_meetings_result_in_next_step(self):
        result = self._rev(50.0, meetings_resulting_in_next_step=20)
        assert result == 0.0

    def test_no_meetings_result_in_next_step(self):
        # stalled = 20-0 = 20; rev = 20 * 60000 * 0.50 = 600000.0
        result = self._rev(50.0, meetings_resulting_in_next_step=0)
        assert result == 600000.0

    def test_result_is_rounded_to_2_decimals(self):
        result = self._rev(33.3)
        assert result == round(result, 2)

    def test_zero_deal_size_gives_zero(self):
        result = self._rev(50.0, avg_deal_size_in_meetings_usd=0.0)
        assert result == 0.0

    def test_zero_meetings_uses_max1(self):
        # total=0 → uses 1; stalled=1-0=1; rev=1*60000*(0.5)=30000
        result = self._rev(50.0,
                           total_meetings_held=0,
                           meetings_resulting_in_next_step=0,
                           avg_deal_size_in_meetings_usd=60000.0)
        assert result == 30000.0

    def test_custom_values(self):
        result = self._rev(25.0,
                           total_meetings_held=10,
                           meetings_resulting_in_next_step=8,
                           avg_deal_size_in_meetings_usd=100000.0)
        # stalled=2; rev=2*100000*0.25=50000.0
        assert result == 50000.0


# ===========================================================================
# 10. Signal string
# ===========================================================================

class TestSignal:

    def setup_method(self):
        self.engine = SalesMeetingQualityIntelligenceEngine()

    def _signal(self, pattern, composite, **kwargs):
        inp = make_input(**kwargs)
        return self.engine._signal(inp, pattern, composite)

    def test_none_pattern_below_20_positive_signal(self):
        s = self._signal(MeetingPattern.none, 15.0)
        assert s == "Meeting quality driving strong deal progression"

    def test_none_pattern_exactly_20_not_positive(self):
        s = self._signal(MeetingPattern.none, 20.0)
        assert s != "Meeting quality driving strong deal progression"

    def test_non_none_pattern_below_20_not_positive(self):
        s = self._signal(MeetingPattern.pipeline_stall, 10.0)
        assert s != "Meeting quality driving strong deal progression"

    def test_signal_contains_pattern_label(self):
        s = self._signal(MeetingPattern.no_deal_advancement, 45.0,
                         meetings_resulting_in_next_step=5,
                         meetings_with_follow_up_sent_24h=18)
        assert "no deal advancement" in s.lower()

    def test_signal_contains_composite(self):
        s = self._signal(MeetingPattern.poor_preparation, 35.0,
                         meetings_resulting_in_next_step=15,
                         meetings_with_follow_up_sent_24h=18)
        assert "35" in s

    def test_signal_includes_meetings_without_next_step(self):
        # 20-5 = 15 meetings without next step ≥ 1
        s = self._signal(MeetingPattern.poor_preparation, 35.0,
                         meetings_resulting_in_next_step=5,
                         meetings_with_follow_up_sent_24h=18)
        assert "15 meetings without next step" in s

    def test_signal_includes_follow_up_when_2_or_more_missing(self):
        # 20-17 = 3 without follow-up ≥ 2
        s = self._signal(MeetingPattern.poor_preparation, 35.0,
                         meetings_resulting_in_next_step=15,
                         meetings_with_follow_up_sent_24h=17)
        assert "3 without 24h follow-up" in s

    def test_signal_omits_follow_up_when_only_1_missing(self):
        # 20-19 = 1 < 2
        s = self._signal(MeetingPattern.poor_preparation, 35.0,
                         meetings_resulting_in_next_step=15,
                         meetings_with_follow_up_sent_24h=19)
        assert "without 24h follow-up" not in s

    def test_signal_includes_cancellations_when_2_or_more(self):
        s = self._signal(MeetingPattern.poor_preparation, 35.0,
                         meetings_resulting_in_next_step=15,
                         meetings_with_follow_up_sent_24h=18,
                         meetings_cancelled_by_prospect=3)
        assert "3 prospect cancellations" in s

    def test_signal_omits_cancellations_when_less_than_2(self):
        s = self._signal(MeetingPattern.poor_preparation, 35.0,
                         meetings_resulting_in_next_step=15,
                         meetings_with_follow_up_sent_24h=18,
                         meetings_cancelled_by_prospect=1)
        assert "prospect cancellations" not in s

    def test_signal_none_pattern_non_positive_uses_meeting_quality_risk(self):
        s = self._signal(MeetingPattern.none, 25.0,
                         meetings_resulting_in_next_step=5,
                         meetings_with_follow_up_sent_24h=18)
        assert "Meeting quality risk" in s

    def test_signal_no_parts_uses_meeting_effectiveness_degrading(self):
        # all meetings have next step, all have follow-up, no cancellations, not positive
        s = self._signal(MeetingPattern.none, 25.0,
                         meetings_resulting_in_next_step=20,
                         meetings_with_follow_up_sent_24h=20,
                         meetings_cancelled_by_prospect=0)
        assert "meeting effectiveness degrading" in s


# ===========================================================================
# 11. to_dict() — exactly 15 keys
# ===========================================================================

class TestToDict:

    def setup_method(self):
        self.engine = SalesMeetingQualityIntelligenceEngine()

    def test_to_dict_returns_15_keys(self):
        result = self.engine.assess(make_input())
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_contains_rep_id(self):
        d = self.engine.assess(make_input()).to_dict()
        assert "rep_id" in d
        assert d["rep_id"] == "rep_test"

    def test_to_dict_contains_region(self):
        d = self.engine.assess(make_input()).to_dict()
        assert "region" in d
        assert d["region"] == "West"

    def test_to_dict_meeting_risk_is_string(self):
        d = self.engine.assess(make_input()).to_dict()
        assert isinstance(d["meeting_risk"], str)

    def test_to_dict_meeting_pattern_is_string(self):
        d = self.engine.assess(make_input()).to_dict()
        assert isinstance(d["meeting_pattern"], str)

    def test_to_dict_meeting_severity_is_string(self):
        d = self.engine.assess(make_input()).to_dict()
        assert isinstance(d["meeting_severity"], str)

    def test_to_dict_recommended_action_is_string(self):
        d = self.engine.assess(make_input()).to_dict()
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_scores_are_floats(self):
        d = self.engine.assess(make_input()).to_dict()
        for key in ("meeting_preparation_score", "meeting_outcome_score",
                    "stakeholder_coverage_score", "meeting_discipline_score",
                    "meeting_quality_composite"):
            assert isinstance(d[key], float), f"{key} should be float"

    def test_to_dict_flags_are_bools(self):
        d = self.engine.assess(make_input()).to_dict()
        assert isinstance(d["has_meeting_effectiveness_gap"], bool)
        assert isinstance(d["requires_coaching_intervention"], bool)

    def test_to_dict_revenue_is_float(self):
        d = self.engine.assess(make_input()).to_dict()
        assert isinstance(d["estimated_revenue_at_risk_usd"], float)

    def test_to_dict_signal_is_string(self):
        d = self.engine.assess(make_input()).to_dict()
        assert isinstance(d["meeting_signal"], str)

    def test_to_dict_exact_keys(self):
        d = self.engine.assess(make_input()).to_dict()
        expected_keys = {
            "rep_id", "region", "meeting_risk", "meeting_pattern",
            "meeting_severity", "recommended_action",
            "meeting_preparation_score", "meeting_outcome_score",
            "stakeholder_coverage_score", "meeting_discipline_score",
            "meeting_quality_composite", "has_meeting_effectiveness_gap",
            "requires_coaching_intervention", "estimated_revenue_at_risk_usd",
            "meeting_signal",
        }
        assert set(d.keys()) == expected_keys


# ===========================================================================
# 12. summary() — exactly 13 keys
# ===========================================================================

class TestSummary:

    def setup_method(self):
        self.engine = SalesMeetingQualityIntelligenceEngine()

    def test_empty_summary_has_13_keys(self):
        s = self.engine.summary()
        assert len(s) == 13

    def test_empty_summary_zero_total(self):
        assert self.engine.summary()["total"] == 0

    def test_empty_summary_empty_dicts(self):
        s = self.engine.summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}

    def test_empty_summary_zero_averages(self):
        s = self.engine.summary()
        assert s["avg_meeting_quality_composite"] == 0.0
        assert s["avg_meeting_preparation_score"] == 0.0
        assert s["avg_meeting_outcome_score"] == 0.0
        assert s["avg_stakeholder_coverage_score"] == 0.0
        assert s["avg_meeting_discipline_score"] == 0.0

    def test_empty_summary_zero_counts(self):
        s = self.engine.summary()
        assert s["effectiveness_gap_count"] == 0
        assert s["coaching_intervention_count"] == 0
        assert s["total_estimated_revenue_at_risk_usd"] == 0.0

    def test_summary_after_one_assess_has_13_keys(self):
        self.engine.assess(make_input())
        s = self.engine.summary()
        assert len(s) == 13

    def test_summary_exact_keys(self):
        s = self.engine.summary()
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_meeting_quality_composite",
            "effectiveness_gap_count", "coaching_intervention_count",
            "avg_meeting_preparation_score", "avg_meeting_outcome_score",
            "avg_stakeholder_coverage_score", "avg_meeting_discipline_score",
            "total_estimated_revenue_at_risk_usd",
        }
        assert set(s.keys()) == expected_keys

    def test_summary_total_correct(self):
        self.engine.assess(make_input())
        self.engine.assess(make_input(rep_id="rep2"))
        assert self.engine.summary()["total"] == 2

    def test_summary_risk_counts_correct(self):
        self.engine.assess(make_input())
        s = self.engine.summary()
        assert sum(s["risk_counts"].values()) == 1

    def test_summary_revenue_is_sum(self):
        r1 = self.engine.assess(make_input())
        r2 = self.engine.assess(make_input(rep_id="rep2"))
        s = self.engine.summary()
        expected = round(r1.estimated_revenue_at_risk_usd + r2.estimated_revenue_at_risk_usd, 2)
        assert s["total_estimated_revenue_at_risk_usd"] == expected

    def test_summary_avg_composite_correct(self):
        r1 = self.engine.assess(make_input())
        r2 = self.engine.assess(make_input(rep_id="rep2"))
        s = self.engine.summary()
        expected = round((r1.meeting_quality_composite + r2.meeting_quality_composite) / 2, 1)
        assert s["avg_meeting_quality_composite"] == expected

    def test_summary_effectiveness_gap_count(self):
        # default input likely has a gap; just check it's between 0 and total
        self.engine.assess(make_input())
        self.engine.assess(make_input(rep_id="rep2"))
        s = self.engine.summary()
        assert 0 <= s["effectiveness_gap_count"] <= 2

    def test_summary_coaching_intervention_count(self):
        self.engine.assess(make_input())
        s = self.engine.summary()
        assert 0 <= s["coaching_intervention_count"] <= 1


# ===========================================================================
# 13. assess_batch()
# ===========================================================================

class TestAssessBatch:

    def setup_method(self):
        self.engine = SalesMeetingQualityIntelligenceEngine()

    def test_batch_returns_list(self):
        results = self.engine.assess_batch([make_input(), make_input(rep_id="r2")])
        assert isinstance(results, list)

    def test_batch_length_matches_input(self):
        inputs = [make_input(rep_id=f"rep{i}") for i in range(5)]
        results = self.engine.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_returns_meeting_quality_results(self):
        results = self.engine.assess_batch([make_input()])
        assert isinstance(results[0], MeetingQualityResult)

    def test_batch_empty_list(self):
        results = self.engine.assess_batch([])
        assert results == []

    def test_batch_accumulates_in_summary(self):
        inputs = [make_input(rep_id=f"r{i}") for i in range(3)]
        self.engine.assess_batch(inputs)
        assert self.engine.summary()["total"] == 3

    def test_batch_rep_ids_preserved(self):
        inputs = [make_input(rep_id=f"rep_{i}") for i in range(3)]
        results = self.engine.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"rep_{i}"

    def test_batch_single_element(self):
        results = self.engine.assess_batch([make_input()])
        assert len(results) == 1

    def test_batch_each_result_has_valid_risk(self):
        results = self.engine.assess_batch([make_input(), make_input(rep_id="r2")])
        for r in results:
            assert r.meeting_risk in list(MeetingRisk)


# ===========================================================================
# 14. assess() full integration
# ===========================================================================

class TestAssessIntegration:

    def setup_method(self):
        self.engine = SalesMeetingQualityIntelligenceEngine()

    def test_assess_returns_meeting_quality_result(self):
        result = self.engine.assess(make_input())
        assert isinstance(result, MeetingQualityResult)

    def test_assess_stores_result(self):
        self.engine.assess(make_input())
        assert len(self.engine._results) == 1

    def test_assess_rep_id_preserved(self):
        result = self.engine.assess(make_input(rep_id="my_rep"))
        assert result.rep_id == "my_rep"

    def test_assess_region_preserved(self):
        result = self.engine.assess(make_input(region="East"))
        assert result.region == "East"

    def test_assess_composite_is_weighted_sum(self):
        result = self.engine.assess(make_input())
        expected = round(
            result.meeting_preparation_score * 0.20
            + result.meeting_outcome_score * 0.35
            + result.stakeholder_coverage_score * 0.25
            + result.meeting_discipline_score * 0.20,
            1,
        )
        assert result.meeting_quality_composite == expected

    def test_assess_composite_capped_at_100(self):
        # pathological worst-case
        inp = make_input(
            meetings_with_agenda_set=0,
            avg_meeting_prep_score=0.0,
            avg_attendees_per_meeting=0.5,
            meetings_resulting_in_next_step=0,
            avg_deal_stage_advancement_per_meeting=0.0,
            demo_to_proposal_conversion_rate_pct=0.0,
            discovery_to_demo_conversion_rate_pct=0.0,
            meetings_with_decision_maker=0,
            executive_attendee_rate_pct=0.0,
            multi_stakeholder_meetings_pct=0.0,
            meetings_with_champion_only=20,
            meetings_with_follow_up_sent_24h=0,
            meetings_cancelled_by_prospect=20,
            meetings_rescheduled_count=20,
        )
        result = self.engine.assess(inp)
        assert result.meeting_quality_composite <= 100.0

    def test_assess_risk_consistency_with_composite(self):
        result = self.engine.assess(make_input())
        c = result.meeting_quality_composite
        if c >= 60:
            assert result.meeting_risk == MeetingRisk.critical
        elif c >= 40:
            assert result.meeting_risk == MeetingRisk.high
        elif c >= 20:
            assert result.meeting_risk == MeetingRisk.moderate
        else:
            assert result.meeting_risk == MeetingRisk.low

    def test_assess_severity_consistency_with_composite(self):
        result = self.engine.assess(make_input())
        c = result.meeting_quality_composite
        if c >= 60:
            assert result.meeting_severity == MeetingSeverity.detrimental
        elif c >= 40:
            assert result.meeting_severity == MeetingSeverity.ineffective
        elif c >= 20:
            assert result.meeting_severity == MeetingSeverity.developing
        else:
            assert result.meeting_severity == MeetingSeverity.effective

    def test_assess_multiple_reps_independent(self):
        r1 = self.engine.assess(make_input(rep_id="a"))
        r2 = self.engine.assess(make_input(rep_id="b", total_meetings_held=5,
                                           meetings_with_agenda_set=1,
                                           avg_meeting_prep_score=1.0))
        assert r1.rep_id != r2.rep_id
        assert r1.meeting_quality_composite != r2.meeting_quality_composite


# ===========================================================================
# 15. Edge cases
# ===========================================================================

class TestEdgeCases:

    def setup_method(self):
        self.engine = SalesMeetingQualityIntelligenceEngine()

    def test_zero_total_meetings_no_division_error(self):
        inp = make_input(total_meetings_held=0,
                         meetings_with_agenda_set=0,
                         meetings_with_decision_maker=0,
                         meetings_with_champion_only=0,
                         meetings_resulting_in_next_step=0,
                         meetings_with_follow_up_sent_24h=0,
                         meetings_cancelled_by_prospect=0,
                         meetings_rescheduled_count=0)
        result = self.engine.assess(inp)
        assert isinstance(result, MeetingQualityResult)

    def test_all_meetings_have_next_step(self):
        inp = make_input(meetings_resulting_in_next_step=20)
        result = self.engine.assess(inp)
        assert result.estimated_revenue_at_risk_usd == 0.0

    def test_100_percent_next_step_rate_reduces_risk(self):
        inp = make_input(
            meetings_resulting_in_next_step=20,
            avg_deal_stage_advancement_per_meeting=0.50,
        )
        result = self.engine.assess(inp)
        # outcome score should not have next_step penalty
        assert result.meeting_outcome_score < 40.0

    def test_single_meeting(self):
        inp = make_input(
            total_meetings_held=1,
            meetings_with_agenda_set=1,
            meetings_with_decision_maker=1,
            meetings_with_champion_only=0,
            meetings_resulting_in_next_step=1,
            meetings_with_follow_up_sent_24h=1,
            meetings_cancelled_by_prospect=0,
            meetings_rescheduled_count=0,
        )
        result = self.engine.assess(inp)
        assert isinstance(result, MeetingQualityResult)

    def test_very_large_meeting_count(self):
        inp = make_input(
            total_meetings_held=10000,
            meetings_with_agenda_set=8000,
            meetings_with_decision_maker=5000,
            meetings_with_champion_only=1000,
            meetings_resulting_in_next_step=8000,
            meetings_with_follow_up_sent_24h=8000,
            meetings_cancelled_by_prospect=500,
            meetings_rescheduled_count=500,
        )
        result = self.engine.assess(inp)
        assert isinstance(result, MeetingQualityResult)
        assert 0.0 <= result.meeting_quality_composite <= 100.0

    def test_zero_avg_deal_size_zero_revenue(self):
        result = self.engine.assess(make_input(avg_deal_size_in_meetings_usd=0.0))
        assert result.estimated_revenue_at_risk_usd == 0.0

    def test_high_prep_score_10(self):
        result = self.engine.assess(make_input(avg_meeting_prep_score=10.0))
        assert result.meeting_preparation_score >= 0.0

    def test_prep_score_boundary_7_0(self):
        e = SalesMeetingQualityIntelligenceEngine()
        s = e._meeting_preparation_score(make_input(
            avg_meeting_prep_score=7.0,
            meetings_with_agenda_set=20,
            avg_attendees_per_meeting=3.0
        ))
        assert s == 0.0

    def test_prep_score_boundary_6_99(self):
        e = SalesMeetingQualityIntelligenceEngine()
        s = e._meeting_preparation_score(make_input(
            avg_meeting_prep_score=6.99,
            meetings_with_agenda_set=20,
            avg_attendees_per_meeting=3.0
        ))
        assert s >= 7.0

    def test_engine_starts_with_empty_results(self):
        e = SalesMeetingQualityIntelligenceEngine()
        assert e._results == []

    def test_new_engine_per_test_independent(self):
        e1 = SalesMeetingQualityIntelligenceEngine()
        e2 = SalesMeetingQualityIntelligenceEngine()
        e1.assess(make_input())
        assert len(e1._results) == 1
        assert len(e2._results) == 0

    def test_composite_is_float(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.meeting_quality_composite, float)

    def test_all_scores_non_negative(self):
        result = self.engine.assess(make_input())
        assert result.meeting_preparation_score >= 0.0
        assert result.meeting_outcome_score >= 0.0
        assert result.stakeholder_coverage_score >= 0.0
        assert result.meeting_discipline_score >= 0.0

    def test_all_scores_at_most_100(self):
        result = self.engine.assess(make_input())
        assert result.meeting_preparation_score <= 100.0
        assert result.meeting_outcome_score <= 100.0
        assert result.stakeholder_coverage_score <= 100.0
        assert result.meeting_discipline_score <= 100.0

    def test_result_dataclass_fields(self):
        result = self.engine.assess(make_input())
        assert hasattr(result, "rep_id")
        assert hasattr(result, "region")
        assert hasattr(result, "meeting_risk")
        assert hasattr(result, "meeting_pattern")
        assert hasattr(result, "meeting_severity")
        assert hasattr(result, "recommended_action")
        assert hasattr(result, "meeting_quality_composite")
        assert hasattr(result, "has_meeting_effectiveness_gap")
        assert hasattr(result, "requires_coaching_intervention")
        assert hasattr(result, "estimated_revenue_at_risk_usd")
        assert hasattr(result, "meeting_signal")


# ===========================================================================
# 16. Composite score boundary scenarios
# ===========================================================================

class TestCompositeScenarios:

    def setup_method(self):
        self.engine = SalesMeetingQualityIntelligenceEngine()

    def test_ideal_rep_low_risk(self):
        """All metrics excellent → composite < 20 → low risk."""
        inp = make_input(
            meetings_with_agenda_set=20,
            avg_meeting_prep_score=9.0,
            avg_attendees_per_meeting=3.0,
            meetings_resulting_in_next_step=18,
            avg_deal_stage_advancement_per_meeting=0.50,
            demo_to_proposal_conversion_rate_pct=0.90,
            discovery_to_demo_conversion_rate_pct=0.90,
            meetings_with_decision_maker=15,
            executive_attendee_rate_pct=0.50,
            multi_stakeholder_meetings_pct=0.80,
            meetings_with_champion_only=2,
            meetings_with_follow_up_sent_24h=19,
            meetings_cancelled_by_prospect=0,
            meetings_rescheduled_count=1,
            meetings_leading_to_proposal_count=4,
        )
        result = self.engine.assess(inp)
        assert result.meeting_risk == MeetingRisk.low
        assert result.meeting_severity == MeetingSeverity.effective
        assert result.recommended_action == MeetingAction.no_action

    def test_struggling_rep_critical_risk(self):
        """Worst metrics → composite >= 60 → critical risk."""
        inp = make_input(
            meetings_with_agenda_set=2,
            avg_meeting_prep_score=1.0,
            avg_attendees_per_meeting=1.0,
            meetings_resulting_in_next_step=4,
            avg_deal_stage_advancement_per_meeting=0.05,
            demo_to_proposal_conversion_rate_pct=0.10,
            discovery_to_demo_conversion_rate_pct=0.10,
            meetings_with_decision_maker=2,
            executive_attendee_rate_pct=0.05,
            multi_stakeholder_meetings_pct=0.10,
            meetings_with_champion_only=15,
            meetings_with_follow_up_sent_24h=3,
            meetings_cancelled_by_prospect=8,
            meetings_rescheduled_count=8,
        )
        result = self.engine.assess(inp)
        assert result.meeting_risk == MeetingRisk.critical
        assert result.meeting_severity == MeetingSeverity.detrimental

    def test_moderate_risk_range(self):
        """Craft inputs to land in moderate (20-39) range.
        outcome=55 (next_step 6/20=0.30 → +40, advancement 0.15 → +15)
        disc=40 (follow_up 5/20=0.25 < 0.30 → +40)
        composite = 0*0.20 + 55*0.35 + 0*0.25 + 40*0.20 = 19.25+8 = 27.25
        """
        inp = make_input(
            meetings_with_agenda_set=20,
            avg_meeting_prep_score=9.0,
            avg_attendees_per_meeting=3.0,
            meetings_resulting_in_next_step=6,   # 6/20=0.30 < 0.35 → +40 outcome
            avg_deal_stage_advancement_per_meeting=0.15,  # [0.10,0.25) → +15 outcome
            demo_to_proposal_conversion_rate_pct=0.80,
            discovery_to_demo_conversion_rate_pct=0.80,
            meetings_with_decision_maker=15,
            executive_attendee_rate_pct=0.50,
            multi_stakeholder_meetings_pct=0.70,
            meetings_with_champion_only=2,
            meetings_with_follow_up_sent_24h=5,  # 5/20=0.25 < 0.30 → +40 disc
            meetings_cancelled_by_prospect=0,
            meetings_rescheduled_count=1,
        )
        result = self.engine.assess(inp)
        assert 20.0 <= result.meeting_quality_composite < 40.0
        assert result.meeting_risk == MeetingRisk.moderate
        assert result.meeting_severity == MeetingSeverity.developing

    def test_high_risk_range(self):
        """Craft inputs to land in high (40-59) risk range.
        outcome=100, stk=22 (dm_rate 7/20=0.35 → +22), disc=40 (follow_up 5/20=0.25 → +40)
        composite = 0*0.20 + 100*0.35 + 22*0.25 + 40*0.20 = 35+5.5+8 = 48.5
        """
        inp = make_input(
            meetings_with_agenda_set=20,
            avg_meeting_prep_score=9.0,
            avg_attendees_per_meeting=3.0,
            meetings_resulting_in_next_step=4,   # 4/20=0.20 < 0.35 → +40 outcome
            avg_deal_stage_advancement_per_meeting=0.05,  # < 0.10 → +30 outcome
            demo_to_proposal_conversion_rate_pct=0.10,   # < 0.30 → +20 outcome
            discovery_to_demo_conversion_rate_pct=0.10,  # < 0.40 → +10 outcome
            meetings_with_decision_maker=7,   # 7/20=0.35 in [0.20,0.40) → +22 stk
            executive_attendee_rate_pct=0.35,
            multi_stakeholder_meetings_pct=0.50,
            meetings_with_champion_only=2,
            meetings_with_follow_up_sent_24h=5,  # 5/20=0.25 < 0.30 → +40 disc
            meetings_cancelled_by_prospect=0,
            meetings_rescheduled_count=1,
        )
        result = self.engine.assess(inp)
        assert 40.0 <= result.meeting_quality_composite < 60.0
        assert result.meeting_risk == MeetingRisk.high
        assert result.meeting_severity == MeetingSeverity.ineffective
