"""
Comprehensive tests for swarm/intelligence/sales_email_sequence_intelligence_engine.py
"""
from __future__ import annotations

import dataclasses
import pytest

from swarm.intelligence.sales_email_sequence_intelligence_engine import (
    EmailSequenceRisk,
    EmailSequencePattern,
    EmailSequenceSeverity,
    EmailSequenceAction,
    EmailSequenceInput,
    EmailSequenceResult,
    SalesEmailSequenceIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(
    rep_id: str = "rep_001",
    region: str = "West",
    evaluation_period_id: str = "Q1-2026",
    total_sequences_active: int = 100,
    avg_email_open_rate_pct: float = 0.30,
    avg_email_reply_rate_pct: float = 0.12,
    avg_click_through_rate_pct: float = 0.05,
    avg_bounce_rate_pct: float = 0.02,
    avg_unsubscribe_rate_pct: float = 0.01,
    avg_follow_up_attempts_per_prospect: float = 4.0,
    avg_days_between_touchpoints: float = 3.0,
    sequences_with_no_reply_pct: float = 0.30,
    avg_subject_line_length_chars: float = 50.0,
    avg_email_word_count: float = 150.0,
    personalization_rate_pct: float = 0.60,
    calls_to_action_per_email_avg: float = 1.5,
    avg_send_time_score: float = 0.75,
    template_vs_custom_ratio: float = 0.50,
    multi_touch_response_rate_pct: float = 0.20,
    prospect_meeting_booked_from_sequence_pct: float = 0.15,
    email_to_meeting_conversion_pct: float = 0.08,
    avg_opportunity_value_usd: float = 10_000.0,
) -> EmailSequenceInput:
    return EmailSequenceInput(
        rep_id=rep_id,
        region=region,
        evaluation_period_id=evaluation_period_id,
        total_sequences_active=total_sequences_active,
        avg_email_open_rate_pct=avg_email_open_rate_pct,
        avg_email_reply_rate_pct=avg_email_reply_rate_pct,
        avg_click_through_rate_pct=avg_click_through_rate_pct,
        avg_bounce_rate_pct=avg_bounce_rate_pct,
        avg_unsubscribe_rate_pct=avg_unsubscribe_rate_pct,
        avg_follow_up_attempts_per_prospect=avg_follow_up_attempts_per_prospect,
        avg_days_between_touchpoints=avg_days_between_touchpoints,
        sequences_with_no_reply_pct=sequences_with_no_reply_pct,
        avg_subject_line_length_chars=avg_subject_line_length_chars,
        avg_email_word_count=avg_email_word_count,
        personalization_rate_pct=personalization_rate_pct,
        calls_to_action_per_email_avg=calls_to_action_per_email_avg,
        avg_send_time_score=avg_send_time_score,
        template_vs_custom_ratio=template_vs_custom_ratio,
        multi_touch_response_rate_pct=multi_touch_response_rate_pct,
        prospect_meeting_booked_from_sequence_pct=prospect_meeting_booked_from_sequence_pct,
        email_to_meeting_conversion_pct=email_to_meeting_conversion_pct,
        avg_opportunity_value_usd=avg_opportunity_value_usd,
    )


def make_engine() -> SalesEmailSequenceIntelligenceEngine:
    return SalesEmailSequenceIntelligenceEngine()


# ===========================================================================
# 1. ENUM TESTS
# ===========================================================================

class TestEmailSequenceRiskEnum:
    def test_low_value(self):
        assert EmailSequenceRisk.low.value == "low"

    def test_moderate_value(self):
        assert EmailSequenceRisk.moderate.value == "moderate"

    def test_high_value(self):
        assert EmailSequenceRisk.high.value == "high"

    def test_critical_value(self):
        assert EmailSequenceRisk.critical.value == "critical"

    def test_is_str_enum(self):
        assert isinstance(EmailSequenceRisk.low, str)

    def test_all_members(self):
        members = {e.value for e in EmailSequenceRisk}
        assert members == {"low", "moderate", "high", "critical"}

    def test_member_count(self):
        assert len(EmailSequenceRisk) == 4

    def test_equality_with_string(self):
        assert EmailSequenceRisk.low == "low"

    def test_inequality(self):
        assert EmailSequenceRisk.low != EmailSequenceRisk.high


class TestEmailSequencePatternEnum:
    def test_none_value(self):
        assert EmailSequencePattern.none.value == "none"

    def test_low_open_rate_value(self):
        assert EmailSequencePattern.low_open_rate.value == "low_open_rate"

    def test_poor_personalization_value(self):
        assert EmailSequencePattern.poor_personalization.value == "poor_personalization"

    def test_email_fatigue_value(self):
        assert EmailSequencePattern.email_fatigue.value == "email_fatigue"

    def test_timing_failure_value(self):
        assert EmailSequencePattern.timing_failure.value == "timing_failure"

    def test_template_overuse_value(self):
        assert EmailSequencePattern.template_overuse.value == "template_overuse"

    def test_is_str_enum(self):
        assert isinstance(EmailSequencePattern.none, str)

    def test_all_members(self):
        members = {e.value for e in EmailSequencePattern}
        assert members == {
            "none", "low_open_rate", "poor_personalization",
            "email_fatigue", "timing_failure", "template_overuse"
        }

    def test_member_count(self):
        assert len(EmailSequencePattern) == 6


class TestEmailSequenceSeverityEnum:
    def test_strong_value(self):
        assert EmailSequenceSeverity.strong.value == "strong"

    def test_developing_value(self):
        assert EmailSequenceSeverity.developing.value == "developing"

    def test_weak_value(self):
        assert EmailSequenceSeverity.weak.value == "weak"

    def test_failing_value(self):
        assert EmailSequenceSeverity.failing.value == "failing"

    def test_is_str_enum(self):
        assert isinstance(EmailSequenceSeverity.strong, str)

    def test_all_members(self):
        members = {e.value for e in EmailSequenceSeverity}
        assert members == {"strong", "developing", "weak", "failing"}

    def test_member_count(self):
        assert len(EmailSequenceSeverity) == 4


class TestEmailSequenceActionEnum:
    def test_no_action_value(self):
        assert EmailSequenceAction.no_action.value == "no_action"

    def test_sequence_optimization_value(self):
        assert EmailSequenceAction.sequence_optimization.value == "sequence_optimization"

    def test_personalization_coaching_value(self):
        assert EmailSequenceAction.personalization_coaching.value == "personalization_coaching"

    def test_timing_recalibration_value(self):
        assert EmailSequenceAction.timing_recalibration.value == "timing_recalibration"

    def test_template_refresh_value(self):
        assert EmailSequenceAction.template_refresh.value == "template_refresh"

    def test_email_fatigue_intervention_value(self):
        assert EmailSequenceAction.email_fatigue_intervention.value == "email_fatigue_intervention"

    def test_is_str_enum(self):
        assert isinstance(EmailSequenceAction.no_action, str)

    def test_all_members(self):
        members = {e.value for e in EmailSequenceAction}
        assert members == {
            "no_action", "sequence_optimization", "personalization_coaching",
            "timing_recalibration", "template_refresh", "email_fatigue_intervention"
        }

    def test_member_count(self):
        assert len(EmailSequenceAction) == 6


# ===========================================================================
# 2. EmailSequenceInput DATACLASS TESTS
# ===========================================================================

class TestEmailSequenceInputDataclass:
    def test_creation(self):
        inp = make_input()
        assert inp.rep_id == "rep_001"

    def test_rep_id_field(self):
        inp = make_input(rep_id="xyz")
        assert inp.rep_id == "xyz"

    def test_region_field(self):
        inp = make_input(region="East")
        assert inp.region == "East"

    def test_evaluation_period_id_field(self):
        inp = make_input(evaluation_period_id="Q2-2026")
        assert inp.evaluation_period_id == "Q2-2026"

    def test_total_sequences_active_field(self):
        inp = make_input(total_sequences_active=50)
        assert inp.total_sequences_active == 50

    def test_avg_email_open_rate_pct_field(self):
        inp = make_input(avg_email_open_rate_pct=0.20)
        assert inp.avg_email_open_rate_pct == 0.20

    def test_avg_email_reply_rate_pct_field(self):
        inp = make_input(avg_email_reply_rate_pct=0.07)
        assert inp.avg_email_reply_rate_pct == 0.07

    def test_avg_click_through_rate_pct_field(self):
        inp = make_input(avg_click_through_rate_pct=0.03)
        assert inp.avg_click_through_rate_pct == 0.03

    def test_avg_bounce_rate_pct_field(self):
        inp = make_input(avg_bounce_rate_pct=0.08)
        assert inp.avg_bounce_rate_pct == 0.08

    def test_avg_unsubscribe_rate_pct_field(self):
        inp = make_input(avg_unsubscribe_rate_pct=0.03)
        assert inp.avg_unsubscribe_rate_pct == 0.03

    def test_avg_follow_up_attempts_field(self):
        inp = make_input(avg_follow_up_attempts_per_prospect=3.0)
        assert inp.avg_follow_up_attempts_per_prospect == 3.0

    def test_avg_days_between_touchpoints_field(self):
        inp = make_input(avg_days_between_touchpoints=5.0)
        assert inp.avg_days_between_touchpoints == 5.0

    def test_sequences_with_no_reply_pct_field(self):
        inp = make_input(sequences_with_no_reply_pct=0.60)
        assert inp.sequences_with_no_reply_pct == 0.60

    def test_avg_subject_line_length_chars_field(self):
        inp = make_input(avg_subject_line_length_chars=45.0)
        assert inp.avg_subject_line_length_chars == 45.0

    def test_avg_email_word_count_field(self):
        inp = make_input(avg_email_word_count=250.0)
        assert inp.avg_email_word_count == 250.0

    def test_personalization_rate_pct_field(self):
        inp = make_input(personalization_rate_pct=0.45)
        assert inp.personalization_rate_pct == 0.45

    def test_calls_to_action_per_email_avg_field(self):
        inp = make_input(calls_to_action_per_email_avg=2.5)
        assert inp.calls_to_action_per_email_avg == 2.5

    def test_avg_send_time_score_field(self):
        inp = make_input(avg_send_time_score=0.60)
        assert inp.avg_send_time_score == 0.60

    def test_template_vs_custom_ratio_field(self):
        inp = make_input(template_vs_custom_ratio=0.80)
        assert inp.template_vs_custom_ratio == 0.80

    def test_multi_touch_response_rate_pct_field(self):
        inp = make_input(multi_touch_response_rate_pct=0.25)
        assert inp.multi_touch_response_rate_pct == 0.25

    def test_prospect_meeting_booked_from_sequence_pct_field(self):
        inp = make_input(prospect_meeting_booked_from_sequence_pct=0.12)
        assert inp.prospect_meeting_booked_from_sequence_pct == 0.12

    def test_email_to_meeting_conversion_pct_field(self):
        inp = make_input(email_to_meeting_conversion_pct=0.05)
        assert inp.email_to_meeting_conversion_pct == 0.05

    def test_avg_opportunity_value_usd_field(self):
        inp = make_input(avg_opportunity_value_usd=20_000.0)
        assert inp.avg_opportunity_value_usd == 20_000.0

    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(EmailSequenceInput)

    def test_field_count(self):
        fields = dataclasses.fields(EmailSequenceInput)
        assert len(fields) == 22


# ===========================================================================
# 3. EmailSequenceResult DATACLASS TESTS
# ===========================================================================

class TestEmailSequenceResultDataclass:
    def _make_result(self, **kwargs) -> EmailSequenceResult:
        defaults = dict(
            rep_id="r1",
            region="West",
            email_sequence_risk=EmailSequenceRisk.low,
            email_sequence_pattern=EmailSequencePattern.none,
            email_sequence_severity=EmailSequenceSeverity.strong,
            recommended_action=EmailSequenceAction.no_action,
            engagement_decay_score=5.0,
            sequence_quality_score=5.0,
            timing_optimization_score=5.0,
            conversion_effectiveness_score=5.0,
            email_sequence_composite=5.0,
            has_sequence_gap=False,
            requires_sequence_coaching=False,
            estimated_pipeline_impact_usd=0.0,
            email_sequence_signal="healthy",
        )
        defaults.update(kwargs)
        return EmailSequenceResult(**defaults)

    def test_creation(self):
        r = self._make_result()
        assert r.rep_id == "r1"

    def test_rep_id_field(self):
        r = self._make_result(rep_id="xyz")
        assert r.rep_id == "xyz"

    def test_region_field(self):
        r = self._make_result(region="East")
        assert r.region == "East"

    def test_email_sequence_risk_field(self):
        r = self._make_result(email_sequence_risk=EmailSequenceRisk.high)
        assert r.email_sequence_risk == EmailSequenceRisk.high

    def test_email_sequence_pattern_field(self):
        r = self._make_result(email_sequence_pattern=EmailSequencePattern.email_fatigue)
        assert r.email_sequence_pattern == EmailSequencePattern.email_fatigue

    def test_email_sequence_severity_field(self):
        r = self._make_result(email_sequence_severity=EmailSequenceSeverity.failing)
        assert r.email_sequence_severity == EmailSequenceSeverity.failing

    def test_recommended_action_field(self):
        r = self._make_result(recommended_action=EmailSequenceAction.sequence_optimization)
        assert r.recommended_action == EmailSequenceAction.sequence_optimization

    def test_engagement_decay_score_field(self):
        r = self._make_result(engagement_decay_score=42.5)
        assert r.engagement_decay_score == 42.5

    def test_sequence_quality_score_field(self):
        r = self._make_result(sequence_quality_score=33.0)
        assert r.sequence_quality_score == 33.0

    def test_timing_optimization_score_field(self):
        r = self._make_result(timing_optimization_score=55.0)
        assert r.timing_optimization_score == 55.0

    def test_conversion_effectiveness_score_field(self):
        r = self._make_result(conversion_effectiveness_score=70.0)
        assert r.conversion_effectiveness_score == 70.0

    def test_email_sequence_composite_field(self):
        r = self._make_result(email_sequence_composite=48.5)
        assert r.email_sequence_composite == 48.5

    def test_has_sequence_gap_field(self):
        r = self._make_result(has_sequence_gap=True)
        assert r.has_sequence_gap is True

    def test_requires_sequence_coaching_field(self):
        r = self._make_result(requires_sequence_coaching=True)
        assert r.requires_sequence_coaching is True

    def test_estimated_pipeline_impact_usd_field(self):
        r = self._make_result(estimated_pipeline_impact_usd=12345.67)
        assert r.estimated_pipeline_impact_usd == 12345.67

    def test_email_sequence_signal_field(self):
        r = self._make_result(email_sequence_signal="test signal")
        assert r.email_sequence_signal == "test signal"

    def test_field_count(self):
        fields = dataclasses.fields(EmailSequenceResult)
        assert len(fields) == 15

    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(EmailSequenceResult)


# ===========================================================================
# 4. to_dict() TESTS
# ===========================================================================

class TestEmailSequenceResultToDict:
    def _make_result(self) -> EmailSequenceResult:
        engine = make_engine()
        return engine.assess(make_input())

    def test_to_dict_returns_dict(self):
        r = self._make_result()
        assert isinstance(r.to_dict(), dict)

    def test_to_dict_has_15_keys(self):
        r = self._make_result()
        assert len(r.to_dict()) == 15

    def test_to_dict_rep_id_key(self):
        r = self._make_result()
        assert "rep_id" in r.to_dict()

    def test_to_dict_region_key(self):
        r = self._make_result()
        assert "region" in r.to_dict()

    def test_to_dict_email_sequence_risk_key(self):
        r = self._make_result()
        assert "email_sequence_risk" in r.to_dict()

    def test_to_dict_email_sequence_pattern_key(self):
        r = self._make_result()
        assert "email_sequence_pattern" in r.to_dict()

    def test_to_dict_email_sequence_severity_key(self):
        r = self._make_result()
        assert "email_sequence_severity" in r.to_dict()

    def test_to_dict_recommended_action_key(self):
        r = self._make_result()
        assert "recommended_action" in r.to_dict()

    def test_to_dict_engagement_decay_score_key(self):
        r = self._make_result()
        assert "engagement_decay_score" in r.to_dict()

    def test_to_dict_sequence_quality_score_key(self):
        r = self._make_result()
        assert "sequence_quality_score" in r.to_dict()

    def test_to_dict_timing_optimization_score_key(self):
        r = self._make_result()
        assert "timing_optimization_score" in r.to_dict()

    def test_to_dict_conversion_effectiveness_score_key(self):
        r = self._make_result()
        assert "conversion_effectiveness_score" in r.to_dict()

    def test_to_dict_email_sequence_composite_key(self):
        r = self._make_result()
        assert "email_sequence_composite" in r.to_dict()

    def test_to_dict_has_sequence_gap_key(self):
        r = self._make_result()
        assert "has_sequence_gap" in r.to_dict()

    def test_to_dict_requires_sequence_coaching_key(self):
        r = self._make_result()
        assert "requires_sequence_coaching" in r.to_dict()

    def test_to_dict_estimated_pipeline_impact_usd_key(self):
        r = self._make_result()
        assert "estimated_pipeline_impact_usd" in r.to_dict()

    def test_to_dict_email_sequence_signal_key(self):
        r = self._make_result()
        assert "email_sequence_signal" in r.to_dict()

    def test_to_dict_risk_is_string(self):
        r = self._make_result()
        assert isinstance(r.to_dict()["email_sequence_risk"], str)

    def test_to_dict_pattern_is_string(self):
        r = self._make_result()
        assert isinstance(r.to_dict()["email_sequence_pattern"], str)

    def test_to_dict_severity_is_string(self):
        r = self._make_result()
        assert isinstance(r.to_dict()["email_sequence_severity"], str)

    def test_to_dict_action_is_string(self):
        r = self._make_result()
        assert isinstance(r.to_dict()["recommended_action"], str)

    def test_to_dict_rep_id_value(self):
        engine = make_engine()
        r = engine.assess(make_input(rep_id="abc123"))
        assert r.to_dict()["rep_id"] == "abc123"

    def test_to_dict_region_value(self):
        engine = make_engine()
        r = engine.assess(make_input(region="North"))
        assert r.to_dict()["region"] == "North"

    def test_to_dict_risk_value_matches_enum(self):
        r = self._make_result()
        assert r.to_dict()["email_sequence_risk"] == r.email_sequence_risk.value

    def test_to_dict_pattern_value_matches_enum(self):
        r = self._make_result()
        assert r.to_dict()["email_sequence_pattern"] == r.email_sequence_pattern.value

    def test_to_dict_severity_value_matches_enum(self):
        r = self._make_result()
        assert r.to_dict()["email_sequence_severity"] == r.email_sequence_severity.value


# ===========================================================================
# 5. ENGAGEMENT DECAY SCORE TESTS
# ===========================================================================

class TestEngagementDecayScore:
    def setup_method(self):
        self.engine = make_engine()

    def _score(self, **kwargs) -> float:
        return self.engine._engagement_decay_score(make_input(**kwargs))

    # Open rate thresholds
    def test_open_rate_very_low_adds_40(self):
        s = self._score(avg_email_open_rate_pct=0.10, avg_email_reply_rate_pct=0.20, avg_unsubscribe_rate_pct=0.00)
        assert s >= 40.0

    def test_open_rate_below_25_adds_20(self):
        s = self._score(avg_email_open_rate_pct=0.20, avg_email_reply_rate_pct=0.20, avg_unsubscribe_rate_pct=0.00)
        assert s >= 20.0

    def test_open_rate_below_35_adds_8(self):
        s = self._score(avg_email_open_rate_pct=0.30, avg_email_reply_rate_pct=0.20, avg_unsubscribe_rate_pct=0.00)
        assert s >= 8.0

    def test_open_rate_above_35_adds_0(self):
        s = self._score(avg_email_open_rate_pct=0.40, avg_email_reply_rate_pct=0.20, avg_unsubscribe_rate_pct=0.00)
        assert s == 0.0

    # Reply rate thresholds
    def test_reply_rate_below_05_adds_35(self):
        s = self._score(avg_email_open_rate_pct=0.40, avg_email_reply_rate_pct=0.02, avg_unsubscribe_rate_pct=0.00)
        assert s >= 35.0

    def test_reply_rate_below_10_adds_18(self):
        s = self._score(avg_email_open_rate_pct=0.40, avg_email_reply_rate_pct=0.07, avg_unsubscribe_rate_pct=0.00)
        assert s >= 18.0

    def test_reply_rate_below_15_adds_7(self):
        s = self._score(avg_email_open_rate_pct=0.40, avg_email_reply_rate_pct=0.12, avg_unsubscribe_rate_pct=0.00)
        assert s >= 7.0

    def test_reply_rate_above_15_adds_0(self):
        s = self._score(avg_email_open_rate_pct=0.40, avg_email_reply_rate_pct=0.20, avg_unsubscribe_rate_pct=0.00)
        assert s == 0.0

    # Unsubscribe rate thresholds
    def test_unsubscribe_above_05_adds_25(self):
        s = self._score(avg_email_open_rate_pct=0.40, avg_email_reply_rate_pct=0.20, avg_unsubscribe_rate_pct=0.06)
        assert s >= 25.0

    def test_unsubscribe_above_02_adds_12(self):
        s = self._score(avg_email_open_rate_pct=0.40, avg_email_reply_rate_pct=0.20, avg_unsubscribe_rate_pct=0.03)
        assert s >= 12.0

    def test_unsubscribe_below_02_adds_0(self):
        s = self._score(avg_email_open_rate_pct=0.40, avg_email_reply_rate_pct=0.20, avg_unsubscribe_rate_pct=0.01)
        assert s == 0.0

    # Capped at 100
    def test_capped_at_100(self):
        s = self._score(avg_email_open_rate_pct=0.01, avg_email_reply_rate_pct=0.01, avg_unsubscribe_rate_pct=0.10)
        assert s == 100.0

    # Zero case
    def test_all_healthy_returns_0(self):
        s = self._score(avg_email_open_rate_pct=0.40, avg_email_reply_rate_pct=0.20, avg_unsubscribe_rate_pct=0.01)
        assert s == 0.0

    # Boundary at exactly 0.15
    def test_open_rate_exact_015_adds_20(self):
        s = self._score(avg_email_open_rate_pct=0.15, avg_email_reply_rate_pct=0.20, avg_unsubscribe_rate_pct=0.00)
        assert s >= 20.0

    # Boundary at exactly 0.05 reply
    def test_reply_rate_exact_005_adds_18(self):
        s = self._score(avg_email_open_rate_pct=0.40, avg_email_reply_rate_pct=0.05, avg_unsubscribe_rate_pct=0.00)
        assert s >= 18.0


# ===========================================================================
# 6. SEQUENCE QUALITY SCORE TESTS
# ===========================================================================

class TestSequenceQualityScore:
    def setup_method(self):
        self.engine = make_engine()

    def _score(self, **kwargs) -> float:
        return self.engine._sequence_quality_score(make_input(**kwargs))

    # Personalization thresholds
    def test_personalization_below_20_adds_35(self):
        s = self._score(personalization_rate_pct=0.10, template_vs_custom_ratio=0.40,
                        avg_email_word_count=100.0, calls_to_action_per_email_avg=1.0)
        assert s >= 35.0

    def test_personalization_below_40_adds_18(self):
        s = self._score(personalization_rate_pct=0.30, template_vs_custom_ratio=0.40,
                        avg_email_word_count=100.0, calls_to_action_per_email_avg=1.0)
        assert s >= 18.0

    def test_personalization_below_60_adds_7(self):
        s = self._score(personalization_rate_pct=0.50, template_vs_custom_ratio=0.40,
                        avg_email_word_count=100.0, calls_to_action_per_email_avg=1.0)
        assert s >= 7.0

    def test_personalization_above_60_adds_0(self):
        s = self._score(personalization_rate_pct=0.70, template_vs_custom_ratio=0.40,
                        avg_email_word_count=100.0, calls_to_action_per_email_avg=1.0)
        assert s == 0.0

    # Template ratio thresholds
    def test_template_ratio_above_85_adds_30(self):
        s = self._score(personalization_rate_pct=0.70, template_vs_custom_ratio=0.90,
                        avg_email_word_count=100.0, calls_to_action_per_email_avg=1.0)
        assert s >= 30.0

    def test_template_ratio_above_70_adds_15(self):
        s = self._score(personalization_rate_pct=0.70, template_vs_custom_ratio=0.75,
                        avg_email_word_count=100.0, calls_to_action_per_email_avg=1.0)
        assert s >= 15.0

    def test_template_ratio_below_70_adds_0(self):
        s = self._score(personalization_rate_pct=0.70, template_vs_custom_ratio=0.50,
                        avg_email_word_count=100.0, calls_to_action_per_email_avg=1.0)
        assert s == 0.0

    # Word count thresholds
    def test_word_count_above_300_adds_20(self):
        s = self._score(personalization_rate_pct=0.70, template_vs_custom_ratio=0.40,
                        avg_email_word_count=350.0, calls_to_action_per_email_avg=1.0)
        assert s >= 20.0

    def test_word_count_above_200_adds_10(self):
        s = self._score(personalization_rate_pct=0.70, template_vs_custom_ratio=0.40,
                        avg_email_word_count=250.0, calls_to_action_per_email_avg=1.0)
        assert s >= 10.0

    def test_word_count_below_200_adds_0(self):
        s = self._score(personalization_rate_pct=0.70, template_vs_custom_ratio=0.40,
                        avg_email_word_count=100.0, calls_to_action_per_email_avg=1.0)
        assert s == 0.0

    # CTA thresholds
    def test_cta_above_3_adds_15(self):
        s = self._score(personalization_rate_pct=0.70, template_vs_custom_ratio=0.40,
                        avg_email_word_count=100.0, calls_to_action_per_email_avg=3.5)
        assert s >= 15.0

    def test_cta_above_2_adds_7(self):
        s = self._score(personalization_rate_pct=0.70, template_vs_custom_ratio=0.40,
                        avg_email_word_count=100.0, calls_to_action_per_email_avg=2.5)
        assert s >= 7.0

    def test_cta_below_2_adds_0(self):
        s = self._score(personalization_rate_pct=0.70, template_vs_custom_ratio=0.40,
                        avg_email_word_count=100.0, calls_to_action_per_email_avg=1.5)
        assert s == 0.0

    # Capped at 100
    def test_capped_at_100(self):
        s = self._score(personalization_rate_pct=0.05, template_vs_custom_ratio=0.95,
                        avg_email_word_count=400.0, calls_to_action_per_email_avg=5.0)
        assert s == 100.0

    # All clean
    def test_all_healthy_returns_0(self):
        s = self._score(personalization_rate_pct=0.70, template_vs_custom_ratio=0.40,
                        avg_email_word_count=100.0, calls_to_action_per_email_avg=1.0)
        assert s == 0.0


# ===========================================================================
# 7. TIMING OPTIMIZATION SCORE TESTS
# ===========================================================================

class TestTimingOptimizationScore:
    def setup_method(self):
        self.engine = make_engine()

    def _score(self, **kwargs) -> float:
        return self.engine._timing_optimization_score(make_input(**kwargs))

    # Send time thresholds
    def test_send_time_below_30_adds_40(self):
        s = self._score(avg_send_time_score=0.20, avg_days_between_touchpoints=3.0,
                        avg_follow_up_attempts_per_prospect=5.0)
        assert s >= 40.0

    def test_send_time_below_55_adds_20(self):
        s = self._score(avg_send_time_score=0.40, avg_days_between_touchpoints=3.0,
                        avg_follow_up_attempts_per_prospect=5.0)
        assert s >= 20.0

    def test_send_time_below_70_adds_8(self):
        s = self._score(avg_send_time_score=0.60, avg_days_between_touchpoints=3.0,
                        avg_follow_up_attempts_per_prospect=5.0)
        assert s >= 8.0

    def test_send_time_above_70_adds_0(self):
        s = self._score(avg_send_time_score=0.80, avg_days_between_touchpoints=3.0,
                        avg_follow_up_attempts_per_prospect=5.0)
        assert s == 0.0

    # Days between touchpoints thresholds
    def test_days_above_14_adds_35(self):
        s = self._score(avg_send_time_score=0.80, avg_days_between_touchpoints=15.0,
                        avg_follow_up_attempts_per_prospect=5.0)
        assert s >= 35.0

    def test_days_above_7_adds_18(self):
        s = self._score(avg_send_time_score=0.80, avg_days_between_touchpoints=10.0,
                        avg_follow_up_attempts_per_prospect=5.0)
        assert s >= 18.0

    def test_days_above_4_adds_7(self):
        s = self._score(avg_send_time_score=0.80, avg_days_between_touchpoints=5.0,
                        avg_follow_up_attempts_per_prospect=5.0)
        assert s >= 7.0

    def test_days_below_4_adds_0(self):
        s = self._score(avg_send_time_score=0.80, avg_days_between_touchpoints=2.0,
                        avg_follow_up_attempts_per_prospect=5.0)
        assert s == 0.0

    # Follow-up attempts thresholds
    def test_follow_up_below_2_adds_25(self):
        s = self._score(avg_send_time_score=0.80, avg_days_between_touchpoints=2.0,
                        avg_follow_up_attempts_per_prospect=1.5)
        assert s >= 25.0

    def test_follow_up_below_4_adds_10(self):
        s = self._score(avg_send_time_score=0.80, avg_days_between_touchpoints=2.0,
                        avg_follow_up_attempts_per_prospect=3.0)
        assert s >= 10.0

    def test_follow_up_above_4_adds_0(self):
        s = self._score(avg_send_time_score=0.80, avg_days_between_touchpoints=2.0,
                        avg_follow_up_attempts_per_prospect=5.0)
        assert s == 0.0

    # Capped at 100
    def test_capped_at_100(self):
        s = self._score(avg_send_time_score=0.10, avg_days_between_touchpoints=20.0,
                        avg_follow_up_attempts_per_prospect=1.0)
        assert s == 100.0

    # All healthy
    def test_all_healthy_returns_0(self):
        s = self._score(avg_send_time_score=0.80, avg_days_between_touchpoints=2.0,
                        avg_follow_up_attempts_per_prospect=5.0)
        assert s == 0.0


# ===========================================================================
# 8. CONVERSION EFFECTIVENESS SCORE TESTS
# ===========================================================================

class TestConversionEffectivenessScore:
    def setup_method(self):
        self.engine = make_engine()

    def _score(self, **kwargs) -> float:
        return self.engine._conversion_effectiveness_score(make_input(**kwargs))

    # Email-to-meeting conversion thresholds
    def test_conversion_below_03_adds_45(self):
        s = self._score(email_to_meeting_conversion_pct=0.01,
                        sequences_with_no_reply_pct=0.30, avg_bounce_rate_pct=0.01)
        assert s >= 45.0

    def test_conversion_below_06_adds_25(self):
        s = self._score(email_to_meeting_conversion_pct=0.04,
                        sequences_with_no_reply_pct=0.30, avg_bounce_rate_pct=0.01)
        assert s >= 25.0

    def test_conversion_below_10_adds_10(self):
        s = self._score(email_to_meeting_conversion_pct=0.08,
                        sequences_with_no_reply_pct=0.30, avg_bounce_rate_pct=0.01)
        assert s >= 10.0

    def test_conversion_above_10_adds_0(self):
        s = self._score(email_to_meeting_conversion_pct=0.15,
                        sequences_with_no_reply_pct=0.30, avg_bounce_rate_pct=0.01)
        assert s == 0.0

    # No-reply pct thresholds
    def test_no_reply_above_70_adds_30(self):
        s = self._score(email_to_meeting_conversion_pct=0.15,
                        sequences_with_no_reply_pct=0.75, avg_bounce_rate_pct=0.01)
        assert s >= 30.0

    def test_no_reply_above_50_adds_15(self):
        s = self._score(email_to_meeting_conversion_pct=0.15,
                        sequences_with_no_reply_pct=0.60, avg_bounce_rate_pct=0.01)
        assert s >= 15.0

    def test_no_reply_below_50_adds_0(self):
        s = self._score(email_to_meeting_conversion_pct=0.15,
                        sequences_with_no_reply_pct=0.30, avg_bounce_rate_pct=0.01)
        assert s == 0.0

    # Bounce rate thresholds
    def test_bounce_above_10_adds_25(self):
        s = self._score(email_to_meeting_conversion_pct=0.15,
                        sequences_with_no_reply_pct=0.30, avg_bounce_rate_pct=0.12)
        assert s >= 25.0

    def test_bounce_above_05_adds_12(self):
        s = self._score(email_to_meeting_conversion_pct=0.15,
                        sequences_with_no_reply_pct=0.30, avg_bounce_rate_pct=0.07)
        assert s >= 12.0

    def test_bounce_below_05_adds_0(self):
        s = self._score(email_to_meeting_conversion_pct=0.15,
                        sequences_with_no_reply_pct=0.30, avg_bounce_rate_pct=0.03)
        assert s == 0.0

    # Capped at 100
    def test_capped_at_100(self):
        s = self._score(email_to_meeting_conversion_pct=0.01,
                        sequences_with_no_reply_pct=0.80, avg_bounce_rate_pct=0.15)
        assert s == 100.0

    # All healthy
    def test_all_healthy_returns_0(self):
        s = self._score(email_to_meeting_conversion_pct=0.15,
                        sequences_with_no_reply_pct=0.30, avg_bounce_rate_pct=0.03)
        assert s == 0.0


# ===========================================================================
# 9. COMPOSITE SCORE TESTS
# ===========================================================================

class TestCompositeScore:
    def setup_method(self):
        self.engine = make_engine()

    def test_composite_weights_sum(self):
        # engagement*0.30 + quality*0.30 + timing*0.25 + conversion*0.15
        weights = 0.30 + 0.30 + 0.25 + 0.15
        assert abs(weights - 1.0) < 1e-9

    def test_composite_formula_zero(self):
        result = self.engine.assess(make_input())
        # all scores should be 0 with default healthy values
        assert result.email_sequence_composite >= 0.0

    def test_composite_capped_at_100(self):
        inp = make_input(
            avg_email_open_rate_pct=0.01,
            avg_email_reply_rate_pct=0.01,
            avg_unsubscribe_rate_pct=0.10,
            personalization_rate_pct=0.05,
            template_vs_custom_ratio=0.95,
            avg_email_word_count=400.0,
            calls_to_action_per_email_avg=5.0,
            avg_send_time_score=0.10,
            avg_days_between_touchpoints=20.0,
            avg_follow_up_attempts_per_prospect=1.0,
            email_to_meeting_conversion_pct=0.01,
            sequences_with_no_reply_pct=0.80,
            avg_bounce_rate_pct=0.15,
        )
        result = self.engine.assess(inp)
        assert result.email_sequence_composite <= 100.0

    def test_composite_is_rounded_to_1_decimal(self):
        result = self.engine.assess(make_input())
        val = result.email_sequence_composite
        assert round(val, 1) == val

    def test_composite_manual_calculation(self):
        # Use known inputs that produce known sub-scores
        # open_rate=0.40(+0), reply=0.20(+0), unsub=0.01(+0) => engagement=0
        # personalization=0.70(+0), template=0.40(+0), wc=100(+0), cta=1(+0) => quality=0
        # send_time=0.80(+0), days=2(+0), followup=5(+0) => timing=0
        # conversion=0.15(+0), no_reply=0.30(+0), bounce=0.01(+0) => conversion=0
        # composite = 0*0.30 + 0*0.30 + 0*0.25 + 0*0.15 = 0
        inp = make_input(
            avg_email_open_rate_pct=0.40,
            avg_email_reply_rate_pct=0.20,
            avg_unsubscribe_rate_pct=0.01,
            personalization_rate_pct=0.70,
            template_vs_custom_ratio=0.40,
            avg_email_word_count=100.0,
            calls_to_action_per_email_avg=1.0,
            avg_send_time_score=0.80,
            avg_days_between_touchpoints=2.0,
            avg_follow_up_attempts_per_prospect=5.0,
            email_to_meeting_conversion_pct=0.15,
            sequences_with_no_reply_pct=0.30,
            avg_bounce_rate_pct=0.01,
        )
        result = self.engine.assess(inp)
        assert result.email_sequence_composite == 0.0


# ===========================================================================
# 10. RISK LEVEL TESTS
# ===========================================================================

class TestRiskLevel:
    def setup_method(self):
        self.engine = make_engine()

    def _risk(self, composite: float) -> EmailSequenceRisk:
        return self.engine._risk_level(composite)

    def test_composite_0_is_low(self):
        assert self._risk(0.0) == EmailSequenceRisk.low

    def test_composite_19_is_low(self):
        assert self._risk(19.9) == EmailSequenceRisk.low

    def test_composite_20_is_moderate(self):
        assert self._risk(20.0) == EmailSequenceRisk.moderate

    def test_composite_39_is_moderate(self):
        assert self._risk(39.9) == EmailSequenceRisk.moderate

    def test_composite_40_is_high(self):
        assert self._risk(40.0) == EmailSequenceRisk.high

    def test_composite_59_is_high(self):
        assert self._risk(59.9) == EmailSequenceRisk.high

    def test_composite_60_is_critical(self):
        assert self._risk(60.0) == EmailSequenceRisk.critical

    def test_composite_100_is_critical(self):
        assert self._risk(100.0) == EmailSequenceRisk.critical

    def test_composite_80_is_critical(self):
        assert self._risk(80.0) == EmailSequenceRisk.critical


# ===========================================================================
# 11. SEVERITY TESTS
# ===========================================================================

class TestSeverity:
    def setup_method(self):
        self.engine = make_engine()

    def _sev(self, composite: float) -> EmailSequenceSeverity:
        return self.engine._severity(composite)

    def test_composite_0_is_strong(self):
        assert self._sev(0.0) == EmailSequenceSeverity.strong

    def test_composite_19_is_strong(self):
        assert self._sev(19.9) == EmailSequenceSeverity.strong

    def test_composite_20_is_developing(self):
        assert self._sev(20.0) == EmailSequenceSeverity.developing

    def test_composite_39_is_developing(self):
        assert self._sev(39.9) == EmailSequenceSeverity.developing

    def test_composite_40_is_weak(self):
        assert self._sev(40.0) == EmailSequenceSeverity.weak

    def test_composite_59_is_weak(self):
        assert self._sev(59.9) == EmailSequenceSeverity.weak

    def test_composite_60_is_failing(self):
        assert self._sev(60.0) == EmailSequenceSeverity.failing

    def test_composite_100_is_failing(self):
        assert self._sev(100.0) == EmailSequenceSeverity.failing

    def test_composite_75_is_failing(self):
        assert self._sev(75.0) == EmailSequenceSeverity.failing


# ===========================================================================
# 12. ACTION MAPPING TESTS
# ===========================================================================

class TestActionMapping:
    def setup_method(self):
        self.engine = make_engine()

    def _action(self, risk, pattern) -> EmailSequenceAction:
        return self.engine._action(risk, pattern)

    # Low risk => no_action for all patterns
    def test_low_risk_no_action(self):
        assert self._action(EmailSequenceRisk.low, EmailSequencePattern.none) == EmailSequenceAction.no_action

    def test_low_risk_with_low_open_rate_no_action(self):
        assert self._action(EmailSequenceRisk.low, EmailSequencePattern.low_open_rate) == EmailSequenceAction.no_action

    def test_low_risk_with_email_fatigue_no_action(self):
        assert self._action(EmailSequenceRisk.low, EmailSequencePattern.email_fatigue) == EmailSequenceAction.no_action

    # Moderate risk => sequence_optimization
    def test_moderate_risk_none_pattern(self):
        assert self._action(EmailSequenceRisk.moderate, EmailSequencePattern.none) == EmailSequenceAction.sequence_optimization

    def test_moderate_risk_low_open_rate(self):
        assert self._action(EmailSequenceRisk.moderate, EmailSequencePattern.low_open_rate) == EmailSequenceAction.sequence_optimization

    def test_moderate_risk_email_fatigue(self):
        assert self._action(EmailSequenceRisk.moderate, EmailSequencePattern.email_fatigue) == EmailSequenceAction.sequence_optimization

    def test_moderate_risk_timing_failure(self):
        assert self._action(EmailSequenceRisk.moderate, EmailSequencePattern.timing_failure) == EmailSequenceAction.sequence_optimization

    def test_moderate_risk_template_overuse(self):
        assert self._action(EmailSequenceRisk.moderate, EmailSequencePattern.template_overuse) == EmailSequenceAction.sequence_optimization

    def test_moderate_risk_poor_personalization(self):
        assert self._action(EmailSequenceRisk.moderate, EmailSequencePattern.poor_personalization) == EmailSequenceAction.sequence_optimization

    # High risk => timing_recalibration for timing_failure
    def test_high_risk_timing_failure(self):
        assert self._action(EmailSequenceRisk.high, EmailSequencePattern.timing_failure) == EmailSequenceAction.timing_recalibration

    # High risk => template_refresh for template_overuse
    def test_high_risk_template_overuse(self):
        assert self._action(EmailSequenceRisk.high, EmailSequencePattern.template_overuse) == EmailSequenceAction.template_refresh

    # High risk => sequence_optimization for other patterns
    def test_high_risk_none_pattern(self):
        assert self._action(EmailSequenceRisk.high, EmailSequencePattern.none) == EmailSequenceAction.sequence_optimization

    def test_high_risk_low_open_rate(self):
        assert self._action(EmailSequenceRisk.high, EmailSequencePattern.low_open_rate) == EmailSequenceAction.sequence_optimization

    def test_high_risk_email_fatigue(self):
        assert self._action(EmailSequenceRisk.high, EmailSequencePattern.email_fatigue) == EmailSequenceAction.sequence_optimization

    def test_high_risk_poor_personalization(self):
        assert self._action(EmailSequenceRisk.high, EmailSequencePattern.poor_personalization) == EmailSequenceAction.sequence_optimization

    # Critical risk => email_fatigue_intervention for email_fatigue
    def test_critical_risk_email_fatigue(self):
        assert self._action(EmailSequenceRisk.critical, EmailSequencePattern.email_fatigue) == EmailSequenceAction.email_fatigue_intervention

    # Critical risk => personalization_coaching for poor_personalization
    def test_critical_risk_poor_personalization(self):
        assert self._action(EmailSequenceRisk.critical, EmailSequencePattern.poor_personalization) == EmailSequenceAction.personalization_coaching

    # Critical risk => sequence_optimization for other patterns
    def test_critical_risk_none_pattern(self):
        assert self._action(EmailSequenceRisk.critical, EmailSequencePattern.none) == EmailSequenceAction.sequence_optimization

    def test_critical_risk_low_open_rate(self):
        assert self._action(EmailSequenceRisk.critical, EmailSequencePattern.low_open_rate) == EmailSequenceAction.sequence_optimization

    def test_critical_risk_timing_failure(self):
        assert self._action(EmailSequenceRisk.critical, EmailSequencePattern.timing_failure) == EmailSequenceAction.sequence_optimization

    def test_critical_risk_template_overuse(self):
        assert self._action(EmailSequenceRisk.critical, EmailSequencePattern.template_overuse) == EmailSequenceAction.sequence_optimization


# ===========================================================================
# 13. PATTERN DETECTION TESTS
# ===========================================================================

class TestPatternDetection:
    def setup_method(self):
        self.engine = make_engine()

    def _detect(self, engagement, quality, timing, conversion, **kwargs) -> EmailSequencePattern:
        inp = make_input(**kwargs)
        return self.engine._detect_pattern(inp, engagement, quality, timing, conversion)

    def test_low_open_rate_pattern(self):
        # engagement >= 35 AND open_rate < 0.20
        p = self._detect(35, 5, 5, 5, avg_email_open_rate_pct=0.10)
        assert p == EmailSequencePattern.low_open_rate

    def test_low_open_rate_engagement_exactly_35(self):
        p = self._detect(35, 5, 5, 5, avg_email_open_rate_pct=0.15)
        assert p == EmailSequencePattern.low_open_rate

    def test_no_low_open_rate_when_open_rate_high(self):
        p = self._detect(35, 5, 5, 5, avg_email_open_rate_pct=0.25)
        assert p != EmailSequencePattern.low_open_rate

    def test_no_low_open_rate_when_engagement_low(self):
        p = self._detect(30, 5, 5, 5, avg_email_open_rate_pct=0.10)
        assert p != EmailSequencePattern.low_open_rate

    def test_poor_personalization_pattern(self):
        # quality >= 30 AND personalization < 0.30
        p = self._detect(5, 30, 5, 5, personalization_rate_pct=0.20)
        assert p == EmailSequencePattern.poor_personalization

    def test_poor_personalization_quality_exactly_30(self):
        p = self._detect(5, 30, 5, 5, personalization_rate_pct=0.25)
        assert p == EmailSequencePattern.poor_personalization

    def test_no_poor_personalization_when_personalization_high(self):
        p = self._detect(5, 30, 5, 5, personalization_rate_pct=0.35)
        assert p != EmailSequencePattern.poor_personalization

    def test_email_fatigue_pattern(self):
        # engagement >= 25 AND unsubscribe >= 0.03
        p = self._detect(25, 5, 5, 5, avg_unsubscribe_rate_pct=0.04)
        assert p == EmailSequencePattern.email_fatigue

    def test_email_fatigue_engagement_exactly_25(self):
        p = self._detect(25, 5, 5, 5, avg_unsubscribe_rate_pct=0.05)
        assert p == EmailSequencePattern.email_fatigue

    def test_no_email_fatigue_when_engagement_low(self):
        p = self._detect(20, 5, 5, 5, avg_unsubscribe_rate_pct=0.05)
        assert p != EmailSequencePattern.email_fatigue

    def test_timing_failure_pattern(self):
        # timing >= 30 AND days_between >= 7
        p = self._detect(5, 5, 30, 5, avg_days_between_touchpoints=8.0)
        assert p == EmailSequencePattern.timing_failure

    def test_timing_failure_timing_exactly_30(self):
        p = self._detect(5, 5, 30, 5, avg_days_between_touchpoints=7.0)
        assert p == EmailSequencePattern.timing_failure

    def test_no_timing_failure_when_days_low(self):
        p = self._detect(5, 5, 30, 5, avg_days_between_touchpoints=5.0)
        assert p != EmailSequencePattern.timing_failure

    def test_template_overuse_pattern(self):
        # quality >= 20 AND template_ratio >= 0.75
        p = self._detect(5, 20, 5, 5, template_vs_custom_ratio=0.80)
        assert p == EmailSequencePattern.template_overuse

    def test_template_overuse_quality_exactly_20(self):
        p = self._detect(5, 20, 5, 5, template_vs_custom_ratio=0.75)
        assert p == EmailSequencePattern.template_overuse

    def test_no_template_overuse_when_ratio_low(self):
        p = self._detect(5, 20, 5, 5, template_vs_custom_ratio=0.70)
        assert p != EmailSequencePattern.template_overuse

    def test_none_pattern_all_clean(self):
        p = self._detect(5, 5, 5, 5,
                          avg_email_open_rate_pct=0.40,
                          personalization_rate_pct=0.60,
                          avg_unsubscribe_rate_pct=0.01,
                          avg_days_between_touchpoints=3.0,
                          template_vs_custom_ratio=0.50)
        assert p == EmailSequencePattern.none

    def test_low_open_rate_takes_priority_over_poor_personalization(self):
        # engagement >= 35 so low_open_rate fires first
        p = self._detect(35, 30, 5, 5,
                          avg_email_open_rate_pct=0.10,
                          personalization_rate_pct=0.20)
        assert p == EmailSequencePattern.low_open_rate


# ===========================================================================
# 14. HAS SEQUENCE GAP FLAG TESTS
# ===========================================================================

class TestHasSequenceGap:
    def setup_method(self):
        self.engine = make_engine()

    def _gap(self, composite: float, **kwargs) -> bool:
        return self.engine._has_sequence_gap(composite, make_input(**kwargs))

    def test_gap_composite_above_40(self):
        assert self._gap(40.0) is True

    def test_gap_composite_exactly_40(self):
        assert self._gap(40.0) is True

    def test_gap_composite_39_9_no_gap_from_composite(self):
        # only from composite, but check other conditions are False
        result = self._gap(39.9, email_to_meeting_conversion_pct=0.15, avg_unsubscribe_rate_pct=0.01)
        assert result is False

    def test_gap_from_conversion_below_03(self):
        assert self._gap(10.0, email_to_meeting_conversion_pct=0.02) is True

    def test_gap_from_conversion_exactly_03_no_gap(self):
        # 0.03 is NOT < 0.03, so no gap from conversion alone
        result = self._gap(10.0, email_to_meeting_conversion_pct=0.03, avg_unsubscribe_rate_pct=0.01)
        assert result is False

    def test_gap_from_unsubscribe_above_05(self):
        assert self._gap(10.0, avg_unsubscribe_rate_pct=0.05) is True

    def test_gap_from_unsubscribe_exactly_05(self):
        assert self._gap(10.0, avg_unsubscribe_rate_pct=0.05) is True

    def test_no_gap_all_clear(self):
        result = self._gap(10.0, email_to_meeting_conversion_pct=0.15, avg_unsubscribe_rate_pct=0.01)
        assert result is False

    def test_gap_any_condition_true(self):
        # composite < 40 but conversion triggers it
        assert self._gap(5.0, email_to_meeting_conversion_pct=0.01) is True


# ===========================================================================
# 15. REQUIRES SEQUENCE COACHING FLAG TESTS
# ===========================================================================

class TestRequiresSequenceCoaching:
    def setup_method(self):
        self.engine = make_engine()

    def _coach(self, composite: float, **kwargs) -> bool:
        return self.engine._requires_sequence_coaching(composite, make_input(**kwargs))

    def test_coaching_composite_above_30(self):
        assert self._coach(30.0) is True

    def test_coaching_composite_exactly_30(self):
        assert self._coach(30.0) is True

    def test_coaching_composite_29_9_no_coach_from_composite(self):
        result = self._coach(29.9, personalization_rate_pct=0.60, avg_email_reply_rate_pct=0.20)
        assert result is False

    def test_coaching_from_personalization_below_20(self):
        assert self._coach(10.0, personalization_rate_pct=0.10) is True

    def test_coaching_personalization_exactly_20_no_coach(self):
        result = self._coach(10.0, personalization_rate_pct=0.20, avg_email_reply_rate_pct=0.20)
        assert result is False

    def test_coaching_from_reply_below_05(self):
        assert self._coach(10.0, avg_email_reply_rate_pct=0.03) is True

    def test_coaching_reply_exactly_05_no_coach(self):
        result = self._coach(10.0, personalization_rate_pct=0.60, avg_email_reply_rate_pct=0.05)
        assert result is False

    def test_no_coaching_all_clear(self):
        result = self._coach(10.0, personalization_rate_pct=0.60, avg_email_reply_rate_pct=0.20)
        assert result is False

    def test_coaching_any_condition_true(self):
        assert self._coach(5.0, avg_email_reply_rate_pct=0.02) is True


# ===========================================================================
# 16. PIPELINE IMPACT TESTS
# ===========================================================================

class TestEstimatedPipelineImpact:
    def setup_method(self):
        self.engine = make_engine()

    def _impact(self, **kwargs) -> float:
        inp = make_input(**kwargs)
        composite = kwargs.pop("composite", 50.0)
        return self.engine._estimated_pipeline_impact(inp, composite)

    def test_impact_basic_calculation(self):
        # silent_sequences = round(100 * 0.30) = 30
        # impact = 30 * 10000 * (50/100) * 0.12 = 18000.0
        inp = make_input(total_sequences_active=100, sequences_with_no_reply_pct=0.30, avg_opportunity_value_usd=10000.0)
        impact = self.engine._estimated_pipeline_impact(inp, 50.0)
        assert impact == 18000.0

    def test_impact_zero_sequences(self):
        inp = make_input(total_sequences_active=0, sequences_with_no_reply_pct=0.50, avg_opportunity_value_usd=10000.0)
        impact = self.engine._estimated_pipeline_impact(inp, 50.0)
        assert impact == 0.0

    def test_impact_zero_opportunity_value(self):
        inp = make_input(total_sequences_active=100, sequences_with_no_reply_pct=0.50, avg_opportunity_value_usd=0.0)
        impact = self.engine._estimated_pipeline_impact(inp, 50.0)
        assert impact == 0.0

    def test_impact_zero_composite(self):
        inp = make_input(total_sequences_active=100, sequences_with_no_reply_pct=0.50, avg_opportunity_value_usd=10000.0)
        impact = self.engine._estimated_pipeline_impact(inp, 0.0)
        assert impact == 0.0

    def test_impact_full_no_reply(self):
        # silent = round(100 * 1.0) = 100
        # impact = 100 * 5000 * (100/100) * 0.12 = 60000.0
        inp = make_input(total_sequences_active=100, sequences_with_no_reply_pct=1.0, avg_opportunity_value_usd=5000.0)
        impact = self.engine._estimated_pipeline_impact(inp, 100.0)
        assert impact == 60000.0

    def test_impact_returns_float(self):
        inp = make_input()
        impact = self.engine._estimated_pipeline_impact(inp, 50.0)
        assert isinstance(impact, float)

    def test_impact_rounded_to_2_decimals(self):
        inp = make_input(total_sequences_active=100, sequences_with_no_reply_pct=0.30, avg_opportunity_value_usd=10000.0)
        impact = self.engine._estimated_pipeline_impact(inp, 50.0)
        assert round(impact, 2) == impact

    def test_impact_scales_with_composite(self):
        inp = make_input(total_sequences_active=100, sequences_with_no_reply_pct=0.30, avg_opportunity_value_usd=10000.0)
        impact_50 = self.engine._estimated_pipeline_impact(inp, 50.0)
        impact_100 = self.engine._estimated_pipeline_impact(inp, 100.0)
        assert impact_100 == pytest.approx(impact_50 * 2, rel=1e-5)


# ===========================================================================
# 17. SIGNAL STRING TESTS
# ===========================================================================

class TestSignalGeneration:
    def setup_method(self):
        self.engine = make_engine()

    def _signal(self, pattern, composite, **kwargs) -> str:
        inp = make_input(**kwargs)
        return self.engine._signal(inp, pattern, composite)

    def test_healthy_signal_none_pattern_below_20(self):
        sig = self._signal(EmailSequencePattern.none, 10.0)
        assert sig == "Email sequence performance healthy — engagement, personalization, and conversion within benchmarks"

    def test_healthy_signal_exact_boundary_composite_19_9(self):
        sig = self._signal(EmailSequencePattern.none, 19.9)
        assert "healthy" in sig

    def test_non_healthy_when_composite_20(self):
        sig = self._signal(EmailSequencePattern.none, 20.0,
                           avg_email_open_rate_pct=0.30,
                           avg_email_reply_rate_pct=0.12,
                           email_to_meeting_conversion_pct=0.08)
        assert "healthy" not in sig

    def test_non_healthy_when_pattern_not_none(self):
        sig = self._signal(EmailSequencePattern.low_open_rate, 10.0,
                           avg_email_open_rate_pct=0.30,
                           avg_email_reply_rate_pct=0.12,
                           email_to_meeting_conversion_pct=0.08)
        assert "healthy" not in sig

    def test_signal_contains_open_rate_pct(self):
        sig = self._signal(EmailSequencePattern.low_open_rate, 40.0,
                           avg_email_open_rate_pct=0.25,
                           avg_email_reply_rate_pct=0.12,
                           email_to_meeting_conversion_pct=0.08)
        assert "25% open rate" in sig

    def test_signal_contains_reply_rate_pct(self):
        sig = self._signal(EmailSequencePattern.low_open_rate, 40.0,
                           avg_email_open_rate_pct=0.25,
                           avg_email_reply_rate_pct=0.10,
                           email_to_meeting_conversion_pct=0.08)
        assert "10% reply rate" in sig

    def test_signal_contains_email_to_meeting(self):
        sig = self._signal(EmailSequencePattern.low_open_rate, 40.0,
                           avg_email_open_rate_pct=0.25,
                           avg_email_reply_rate_pct=0.10,
                           email_to_meeting_conversion_pct=0.05)
        assert "5.0% email-to-meeting" in sig

    def test_signal_contains_composite(self):
        sig = self._signal(EmailSequencePattern.low_open_rate, 45.0,
                           avg_email_open_rate_pct=0.25,
                           avg_email_reply_rate_pct=0.10,
                           email_to_meeting_conversion_pct=0.05)
        assert "composite 45" in sig

    def test_signal_pattern_label_low_open_rate(self):
        sig = self._signal(EmailSequencePattern.low_open_rate, 40.0,
                           avg_email_open_rate_pct=0.20,
                           avg_email_reply_rate_pct=0.10,
                           email_to_meeting_conversion_pct=0.05)
        assert sig.startswith("Low open rate")

    def test_signal_pattern_label_email_fatigue(self):
        sig = self._signal(EmailSequencePattern.email_fatigue, 40.0,
                           avg_email_open_rate_pct=0.20,
                           avg_email_reply_rate_pct=0.10,
                           email_to_meeting_conversion_pct=0.05)
        assert sig.startswith("Email fatigue")

    def test_signal_pattern_label_poor_personalization(self):
        sig = self._signal(EmailSequencePattern.poor_personalization, 40.0,
                           avg_email_open_rate_pct=0.20,
                           avg_email_reply_rate_pct=0.10,
                           email_to_meeting_conversion_pct=0.05)
        assert sig.startswith("Poor personalization")

    def test_signal_pattern_label_timing_failure(self):
        sig = self._signal(EmailSequencePattern.timing_failure, 40.0,
                           avg_email_open_rate_pct=0.20,
                           avg_email_reply_rate_pct=0.10,
                           email_to_meeting_conversion_pct=0.05)
        assert sig.startswith("Timing failure")

    def test_signal_pattern_label_template_overuse(self):
        sig = self._signal(EmailSequencePattern.template_overuse, 40.0,
                           avg_email_open_rate_pct=0.20,
                           avg_email_reply_rate_pct=0.10,
                           email_to_meeting_conversion_pct=0.05)
        assert sig.startswith("Template overuse")

    def test_signal_none_pattern_above_20_uses_email_sequence_risk(self):
        sig = self._signal(EmailSequencePattern.none, 30.0,
                           avg_email_open_rate_pct=0.20,
                           avg_email_reply_rate_pct=0.10,
                           email_to_meeting_conversion_pct=0.05)
        assert sig.startswith("Email sequence risk")

    def test_signal_returns_string(self):
        sig = self._signal(EmailSequencePattern.none, 5.0)
        assert isinstance(sig, str)


# ===========================================================================
# 18. ASSESS() TESTS
# ===========================================================================

class TestAssess:
    def setup_method(self):
        self.engine = make_engine()

    def test_assess_returns_result(self):
        result = self.engine.assess(make_input())
        assert isinstance(result, EmailSequenceResult)

    def test_assess_rep_id_propagated(self):
        result = self.engine.assess(make_input(rep_id="x123"))
        assert result.rep_id == "x123"

    def test_assess_region_propagated(self):
        result = self.engine.assess(make_input(region="South"))
        assert result.region == "South"

    def test_assess_risk_is_enum(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.email_sequence_risk, EmailSequenceRisk)

    def test_assess_pattern_is_enum(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.email_sequence_pattern, EmailSequencePattern)

    def test_assess_severity_is_enum(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.email_sequence_severity, EmailSequenceSeverity)

    def test_assess_action_is_enum(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.recommended_action, EmailSequenceAction)

    def test_assess_composite_is_float(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.email_sequence_composite, float)

    def test_assess_composite_between_0_and_100(self):
        result = self.engine.assess(make_input())
        assert 0.0 <= result.email_sequence_composite <= 100.0

    def test_assess_engagement_score_is_float(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.engagement_decay_score, float)

    def test_assess_quality_score_is_float(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.sequence_quality_score, float)

    def test_assess_timing_score_is_float(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.timing_optimization_score, float)

    def test_assess_conversion_score_is_float(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.conversion_effectiveness_score, float)

    def test_assess_gap_is_bool(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.has_sequence_gap, bool)

    def test_assess_coaching_is_bool(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.requires_sequence_coaching, bool)

    def test_assess_impact_is_float(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.estimated_pipeline_impact_usd, float)

    def test_assess_signal_is_string(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.email_sequence_signal, str)

    def test_assess_stores_result(self):
        self.engine.assess(make_input())
        assert len(self.engine._results) == 1

    def test_assess_multiple_calls_accumulate(self):
        self.engine.assess(make_input(rep_id="r1"))
        self.engine.assess(make_input(rep_id="r2"))
        assert len(self.engine._results) == 2

    def test_assess_healthy_scenario(self):
        inp = make_input(
            avg_email_open_rate_pct=0.40,
            avg_email_reply_rate_pct=0.20,
            avg_unsubscribe_rate_pct=0.01,
            personalization_rate_pct=0.70,
            template_vs_custom_ratio=0.40,
            avg_email_word_count=100.0,
            calls_to_action_per_email_avg=1.0,
            avg_send_time_score=0.80,
            avg_days_between_touchpoints=2.0,
            avg_follow_up_attempts_per_prospect=5.0,
            email_to_meeting_conversion_pct=0.15,
            sequences_with_no_reply_pct=0.30,
            avg_bounce_rate_pct=0.01,
        )
        result = self.engine.assess(inp)
        assert result.email_sequence_risk == EmailSequenceRisk.low
        assert result.email_sequence_severity == EmailSequenceSeverity.strong
        assert result.recommended_action == EmailSequenceAction.no_action
        assert "healthy" in result.email_sequence_signal

    def test_assess_critical_scenario(self):
        inp = make_input(
            avg_email_open_rate_pct=0.05,
            avg_email_reply_rate_pct=0.01,
            avg_unsubscribe_rate_pct=0.10,
            personalization_rate_pct=0.05,
            template_vs_custom_ratio=0.95,
            avg_email_word_count=400.0,
            calls_to_action_per_email_avg=5.0,
            avg_send_time_score=0.10,
            avg_days_between_touchpoints=20.0,
            avg_follow_up_attempts_per_prospect=1.0,
            email_to_meeting_conversion_pct=0.01,
            sequences_with_no_reply_pct=0.80,
            avg_bounce_rate_pct=0.15,
        )
        result = self.engine.assess(inp)
        assert result.email_sequence_risk == EmailSequenceRisk.critical
        assert result.email_sequence_severity == EmailSequenceSeverity.failing
        assert result.email_sequence_composite == 100.0

    def test_assess_scores_rounded_to_1_decimal(self):
        result = self.engine.assess(make_input())
        for score in [result.engagement_decay_score, result.sequence_quality_score,
                      result.timing_optimization_score, result.conversion_effectiveness_score,
                      result.email_sequence_composite]:
            assert round(score, 1) == score


# ===========================================================================
# 19. ASSESS_BATCH() TESTS
# ===========================================================================

class TestAssessBatch:
    def setup_method(self):
        self.engine = make_engine()

    def test_batch_empty_list(self):
        results = self.engine.assess_batch([])
        assert results == []

    def test_batch_single_item(self):
        results = self.engine.assess_batch([make_input()])
        assert len(results) == 1

    def test_batch_multiple_items(self):
        inputs = [make_input(rep_id=f"r{i}") for i in range(5)]
        results = self.engine.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_returns_list(self):
        results = self.engine.assess_batch([make_input()])
        assert isinstance(results, list)

    def test_batch_each_item_is_result(self):
        results = self.engine.assess_batch([make_input(rep_id="r1"), make_input(rep_id="r2")])
        for r in results:
            assert isinstance(r, EmailSequenceResult)

    def test_batch_preserves_rep_ids(self):
        inputs = [make_input(rep_id="A"), make_input(rep_id="B"), make_input(rep_id="C")]
        results = self.engine.assess_batch(inputs)
        assert [r.rep_id for r in results] == ["A", "B", "C"]

    def test_batch_accumulates_in_internal_results(self):
        self.engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        assert len(self.engine._results) == 3

    def test_batch_results_in_order(self):
        inputs = [make_input(rep_id=f"rep_{i}") for i in range(10)]
        results = self.engine.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"rep_{i}"

    def test_batch_mixed_scenarios(self):
        healthy = make_input(
            avg_email_open_rate_pct=0.40, avg_email_reply_rate_pct=0.20,
            avg_unsubscribe_rate_pct=0.01, email_to_meeting_conversion_pct=0.15,
            avg_bounce_rate_pct=0.01,
            personalization_rate_pct=0.70, template_vs_custom_ratio=0.40,
            avg_email_word_count=100.0, calls_to_action_per_email_avg=1.0,
            avg_send_time_score=0.80, avg_days_between_touchpoints=2.0,
            avg_follow_up_attempts_per_prospect=5.0, sequences_with_no_reply_pct=0.30,
        )
        risky = make_input(
            avg_email_open_rate_pct=0.05, avg_email_reply_rate_pct=0.01,
            avg_unsubscribe_rate_pct=0.10, email_to_meeting_conversion_pct=0.01,
            avg_bounce_rate_pct=0.15, personalization_rate_pct=0.05,
            template_vs_custom_ratio=0.95, avg_email_word_count=400.0,
            calls_to_action_per_email_avg=5.0, avg_send_time_score=0.10,
            avg_days_between_touchpoints=20.0, avg_follow_up_attempts_per_prospect=1.0,
            sequences_with_no_reply_pct=0.80,
        )
        results = self.engine.assess_batch([healthy, risky])
        assert results[0].email_sequence_risk == EmailSequenceRisk.low
        assert results[1].email_sequence_risk == EmailSequenceRisk.critical


# ===========================================================================
# 20. SUMMARY() TESTS
# ===========================================================================

class TestSummary:
    def test_empty_summary_returns_defaults(self):
        engine = make_engine()
        s = engine.summary()
        assert s["total"] == 0
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}
        assert s["avg_email_sequence_composite"] == 0.0
        assert s["sequence_gap_count"] == 0
        assert s["coaching_count"] == 0
        assert s["avg_engagement_decay_score"] == 0.0
        assert s["avg_sequence_quality_score"] == 0.0
        assert s["avg_timing_optimization_score"] == 0.0
        assert s["avg_conversion_effectiveness_score"] == 0.0
        assert s["total_estimated_pipeline_impact_usd"] == 0.0

    def test_empty_summary_has_13_keys(self):
        engine = make_engine()
        assert len(engine.summary()) == 13

    def test_summary_has_13_keys_after_assess(self):
        engine = make_engine()
        engine.assess(make_input())
        assert len(engine.summary()) == 13

    def test_summary_total_count(self):
        engine = make_engine()
        engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        assert engine.summary()["total"] == 3

    def test_summary_risk_counts_populated(self):
        engine = make_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert isinstance(s["risk_counts"], dict)
        assert sum(s["risk_counts"].values()) == 1

    def test_summary_pattern_counts_populated(self):
        engine = make_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert isinstance(s["pattern_counts"], dict)
        assert sum(s["pattern_counts"].values()) == 1

    def test_summary_severity_counts_populated(self):
        engine = make_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert isinstance(s["severity_counts"], dict)
        assert sum(s["severity_counts"].values()) == 1

    def test_summary_action_counts_populated(self):
        engine = make_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert isinstance(s["action_counts"], dict)
        assert sum(s["action_counts"].values()) == 1

    def test_summary_risk_counts_sum_equals_total(self):
        engine = make_engine()
        engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(5)])
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_severity_counts_sum_equals_total(self):
        engine = make_engine()
        engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(5)])
        s = engine.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_summary_avg_composite_is_float(self):
        engine = make_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert isinstance(s["avg_email_sequence_composite"], float)

    def test_summary_avg_composite_rounded_to_1(self):
        engine = make_engine()
        engine.assess(make_input())
        s = engine.summary()
        val = s["avg_email_sequence_composite"]
        assert round(val, 1) == val

    def test_summary_sequence_gap_count(self):
        engine = make_engine()
        # Force a gap with conversion below 0.03
        inp1 = make_input(email_to_meeting_conversion_pct=0.01)
        inp2 = make_input(email_to_meeting_conversion_pct=0.15, avg_unsubscribe_rate_pct=0.01)
        # inp2 with healthy conversion; ensure no gap from composite by using healthy input
        healthy = make_input(
            avg_email_open_rate_pct=0.40, avg_email_reply_rate_pct=0.20,
            avg_unsubscribe_rate_pct=0.01, email_to_meeting_conversion_pct=0.15,
            sequences_with_no_reply_pct=0.30, avg_bounce_rate_pct=0.01,
            personalization_rate_pct=0.70, template_vs_custom_ratio=0.40,
            avg_email_word_count=100.0, calls_to_action_per_email_avg=1.0,
            avg_send_time_score=0.80, avg_days_between_touchpoints=2.0,
            avg_follow_up_attempts_per_prospect=5.0,
        )
        engine.assess(inp1)
        engine.assess(healthy)
        s = engine.summary()
        assert s["sequence_gap_count"] == 1

    def test_summary_coaching_count(self):
        engine = make_engine()
        # Force coaching with reply below 0.05
        inp_coach = make_input(avg_email_reply_rate_pct=0.02)
        inp_no_coach = make_input(
            avg_email_open_rate_pct=0.40, avg_email_reply_rate_pct=0.20,
            avg_unsubscribe_rate_pct=0.01, email_to_meeting_conversion_pct=0.15,
            sequences_with_no_reply_pct=0.30, avg_bounce_rate_pct=0.01,
            personalization_rate_pct=0.70, template_vs_custom_ratio=0.40,
            avg_email_word_count=100.0, calls_to_action_per_email_avg=1.0,
            avg_send_time_score=0.80, avg_days_between_touchpoints=2.0,
            avg_follow_up_attempts_per_prospect=5.0,
        )
        engine.assess(inp_coach)
        engine.assess(inp_no_coach)
        s = engine.summary()
        assert s["coaching_count"] >= 1

    def test_summary_total_pipeline_impact(self):
        engine = make_engine()
        engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        s = engine.summary()
        assert isinstance(s["total_estimated_pipeline_impact_usd"], float)

    def test_summary_total_pipeline_impact_is_sum(self):
        engine = make_engine()
        inp1 = make_input(rep_id="r1")
        inp2 = make_input(rep_id="r2")
        r1 = engine.assess(inp1)
        r2 = engine.assess(inp2)
        expected = round(r1.estimated_pipeline_impact_usd + r2.estimated_pipeline_impact_usd, 2)
        assert engine.summary()["total_estimated_pipeline_impact_usd"] == pytest.approx(expected, rel=1e-5)

    def test_summary_avg_engagement_score(self):
        engine = make_engine()
        r1 = engine.assess(make_input(rep_id="r1"))
        r2 = engine.assess(make_input(rep_id="r2"))
        expected = round((r1.engagement_decay_score + r2.engagement_decay_score) / 2, 1)
        assert engine.summary()["avg_engagement_decay_score"] == expected

    def test_summary_avg_quality_score(self):
        engine = make_engine()
        r1 = engine.assess(make_input(rep_id="r1"))
        r2 = engine.assess(make_input(rep_id="r2"))
        expected = round((r1.sequence_quality_score + r2.sequence_quality_score) / 2, 1)
        assert engine.summary()["avg_sequence_quality_score"] == expected

    def test_summary_avg_timing_score(self):
        engine = make_engine()
        r1 = engine.assess(make_input(rep_id="r1"))
        r2 = engine.assess(make_input(rep_id="r2"))
        expected = round((r1.timing_optimization_score + r2.timing_optimization_score) / 2, 1)
        assert engine.summary()["avg_timing_optimization_score"] == expected

    def test_summary_avg_conversion_score(self):
        engine = make_engine()
        r1 = engine.assess(make_input(rep_id="r1"))
        r2 = engine.assess(make_input(rep_id="r2"))
        expected = round((r1.conversion_effectiveness_score + r2.conversion_effectiveness_score) / 2, 1)
        assert engine.summary()["avg_conversion_effectiveness_score"] == expected

    def test_summary_risk_counts_keys_are_strings(self):
        engine = make_engine()
        engine.assess(make_input())
        for key in engine.summary()["risk_counts"]:
            assert isinstance(key, str)

    def test_summary_pattern_counts_keys_are_strings(self):
        engine = make_engine()
        engine.assess(make_input())
        for key in engine.summary()["pattern_counts"]:
            assert isinstance(key, str)

    def test_summary_after_batch(self):
        engine = make_engine()
        engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(10)])
        s = engine.summary()
        assert s["total"] == 10


# ===========================================================================
# 21. EDGE CASES AND BOUNDARY CONDITIONS
# ===========================================================================

class TestEdgeCases:
    def setup_method(self):
        self.engine = make_engine()

    def test_zero_open_rate(self):
        inp = make_input(avg_email_open_rate_pct=0.0)
        result = self.engine.assess(inp)
        assert result.engagement_decay_score >= 40.0

    def test_100_percent_open_rate(self):
        inp = make_input(avg_email_open_rate_pct=1.0)
        result = self.engine.assess(inp)
        assert result.engagement_decay_score >= 0.0

    def test_zero_sequences_active(self):
        inp = make_input(total_sequences_active=0)
        result = self.engine.assess(inp)
        assert result.estimated_pipeline_impact_usd == 0.0

    def test_zero_opportunity_value(self):
        inp = make_input(avg_opportunity_value_usd=0.0)
        result = self.engine.assess(inp)
        assert result.estimated_pipeline_impact_usd == 0.0

    def test_all_sequences_have_no_reply(self):
        inp = make_input(sequences_with_no_reply_pct=1.0)
        result = self.engine.assess(inp)
        assert result.estimated_pipeline_impact_usd >= 0.0

    def test_zero_conversion_rate(self):
        inp = make_input(email_to_meeting_conversion_pct=0.0)
        result = self.engine.assess(inp)
        assert result.has_sequence_gap is True

    def test_exact_threshold_open_rate_0_15(self):
        eng = self.engine._engagement_decay_score(make_input(
            avg_email_open_rate_pct=0.15,
            avg_email_reply_rate_pct=0.20,
            avg_unsubscribe_rate_pct=0.00
        ))
        assert eng >= 20.0

    def test_exact_threshold_open_rate_0_25(self):
        eng = self.engine._engagement_decay_score(make_input(
            avg_email_open_rate_pct=0.25,
            avg_email_reply_rate_pct=0.20,
            avg_unsubscribe_rate_pct=0.00
        ))
        assert eng >= 8.0

    def test_exact_threshold_reply_rate_0_05(self):
        eng = self.engine._engagement_decay_score(make_input(
            avg_email_open_rate_pct=0.40,
            avg_email_reply_rate_pct=0.05,
            avg_unsubscribe_rate_pct=0.00
        ))
        assert eng >= 18.0

    def test_exact_threshold_reply_rate_0_10(self):
        eng = self.engine._engagement_decay_score(make_input(
            avg_email_open_rate_pct=0.40,
            avg_email_reply_rate_pct=0.10,
            avg_unsubscribe_rate_pct=0.00
        ))
        assert eng >= 7.0

    def test_exact_threshold_unsubscribe_0_02(self):
        eng = self.engine._engagement_decay_score(make_input(
            avg_email_open_rate_pct=0.40,
            avg_email_reply_rate_pct=0.20,
            avg_unsubscribe_rate_pct=0.02
        ))
        assert eng >= 12.0

    def test_exact_threshold_unsubscribe_0_05(self):
        eng = self.engine._engagement_decay_score(make_input(
            avg_email_open_rate_pct=0.40,
            avg_email_reply_rate_pct=0.20,
            avg_unsubscribe_rate_pct=0.05
        ))
        assert eng >= 25.0

    def test_large_opportunity_value(self):
        inp = make_input(avg_opportunity_value_usd=1_000_000.0)
        result = self.engine.assess(inp)
        assert result.estimated_pipeline_impact_usd >= 0.0

    def test_high_sequences_active(self):
        inp = make_input(total_sequences_active=10_000)
        result = self.engine.assess(inp)
        assert result.estimated_pipeline_impact_usd >= 0.0

    def test_engine_initial_state(self):
        engine = SalesEmailSequenceIntelligenceEngine()
        assert engine._results == []

    def test_multiple_engines_independent(self):
        engine1 = make_engine()
        engine2 = make_engine()
        engine1.assess(make_input(rep_id="r1"))
        assert len(engine2._results) == 0

    def test_composite_boundary_exactly_20_is_moderate(self):
        # build input giving composite exactly 20
        # Need engagement*0.30 + quality*0.30 + timing*0.25 + conversion*0.15 = 20
        # Use known: engagement=0, quality=0, timing=0, conversion=0 -> 0
        # So use: engagement=40 (open<0.15), others 0 => 40*0.30=12 -> still not 20
        # This is hard to hit exactly; just test that risk boundary works via _risk_level
        engine = make_engine()
        assert engine._risk_level(20.0) == EmailSequenceRisk.moderate

    def test_composite_boundary_exactly_40_is_high(self):
        engine = make_engine()
        assert engine._risk_level(40.0) == EmailSequenceRisk.high

    def test_composite_boundary_exactly_60_is_critical(self):
        engine = make_engine()
        assert engine._risk_level(60.0) == EmailSequenceRisk.critical

    def test_severity_boundary_exactly_20_is_developing(self):
        engine = make_engine()
        assert engine._severity(20.0) == EmailSequenceSeverity.developing

    def test_severity_boundary_exactly_40_is_weak(self):
        engine = make_engine()
        assert engine._severity(40.0) == EmailSequenceSeverity.weak

    def test_severity_boundary_exactly_60_is_failing(self):
        engine = make_engine()
        assert engine._severity(60.0) == EmailSequenceSeverity.failing


# ===========================================================================
# 22. END-TO-END SCENARIOS
# ===========================================================================

class TestEndToEndScenarios:
    def setup_method(self):
        self.engine = make_engine()

    def test_scenario_healthy_rep(self):
        """A top performer — all metrics excellent."""
        inp = make_input(
            rep_id="top_rep",
            region="West",
            avg_email_open_rate_pct=0.45,
            avg_email_reply_rate_pct=0.20,
            avg_unsubscribe_rate_pct=0.005,
            avg_bounce_rate_pct=0.01,
            personalization_rate_pct=0.80,
            template_vs_custom_ratio=0.30,
            avg_email_word_count=120.0,
            calls_to_action_per_email_avg=1.2,
            avg_send_time_score=0.85,
            avg_days_between_touchpoints=2.5,
            avg_follow_up_attempts_per_prospect=5.0,
            email_to_meeting_conversion_pct=0.12,
            sequences_with_no_reply_pct=0.20,
        )
        result = self.engine.assess(inp)
        assert result.email_sequence_risk == EmailSequenceRisk.low
        assert result.email_sequence_severity == EmailSequenceSeverity.strong
        assert result.recommended_action == EmailSequenceAction.no_action
        assert "healthy" in result.email_sequence_signal
        assert result.has_sequence_gap is False
        assert result.requires_sequence_coaching is False

    def test_scenario_low_open_rate_risk(self):
        """Rep with low open rate — pattern detected and risk above low."""
        inp = make_input(
            rep_id="low_open",
            avg_email_open_rate_pct=0.08,
            avg_email_reply_rate_pct=0.02,
            avg_unsubscribe_rate_pct=0.01,
            personalization_rate_pct=0.50,
            template_vs_custom_ratio=0.50,
            avg_email_word_count=150.0,
            calls_to_action_per_email_avg=1.0,
            avg_send_time_score=0.80,
            avg_days_between_touchpoints=2.0,
            avg_follow_up_attempts_per_prospect=5.0,
            email_to_meeting_conversion_pct=0.05,
            sequences_with_no_reply_pct=0.30,
            avg_bounce_rate_pct=0.01,
        )
        result = self.engine.assess(inp)
        assert result.email_sequence_risk in {EmailSequenceRisk.moderate, EmailSequenceRisk.high, EmailSequenceRisk.critical}
        assert result.email_sequence_pattern == EmailSequencePattern.low_open_rate

    def test_scenario_email_fatigue_detected(self):
        """Email fatigue scenario — low open rate pattern fires first per priority order."""
        inp = make_input(
            rep_id="fatigue_rep",
            avg_email_open_rate_pct=0.12,
            avg_email_reply_rate_pct=0.03,
            avg_unsubscribe_rate_pct=0.07,
            email_to_meeting_conversion_pct=0.02,
            avg_bounce_rate_pct=0.03,
        )
        result = self.engine.assess(inp)
        # low_open_rate fires before email_fatigue in pattern detection
        assert result.email_sequence_pattern == EmailSequencePattern.low_open_rate
        assert result.email_sequence_risk in {EmailSequenceRisk.moderate, EmailSequenceRisk.high, EmailSequenceRisk.critical}

    def test_scenario_poor_personalization_high(self):
        """Poor personalization but moderate engagement."""
        inp = make_input(
            rep_id="poor_personal",
            avg_email_open_rate_pct=0.30,
            avg_email_reply_rate_pct=0.10,
            avg_unsubscribe_rate_pct=0.01,
            personalization_rate_pct=0.10,
            template_vs_custom_ratio=0.90,
            avg_email_word_count=100.0,
            calls_to_action_per_email_avg=1.0,
            avg_send_time_score=0.80,
            avg_days_between_touchpoints=2.0,
            avg_follow_up_attempts_per_prospect=5.0,
            email_to_meeting_conversion_pct=0.05,
            sequences_with_no_reply_pct=0.30,
            avg_bounce_rate_pct=0.02,
        )
        result = self.engine.assess(inp)
        assert result.email_sequence_pattern in {
            EmailSequencePattern.poor_personalization,
            EmailSequencePattern.low_open_rate,
        }

    def test_scenario_timing_failure(self):
        """Timing failure with too many days between touchpoints."""
        inp = make_input(
            rep_id="timing_fail",
            avg_email_open_rate_pct=0.40,
            avg_email_reply_rate_pct=0.20,
            avg_unsubscribe_rate_pct=0.01,
            personalization_rate_pct=0.70,
            template_vs_custom_ratio=0.40,
            avg_email_word_count=100.0,
            calls_to_action_per_email_avg=1.0,
            avg_send_time_score=0.10,
            avg_days_between_touchpoints=20.0,
            avg_follow_up_attempts_per_prospect=1.0,
            email_to_meeting_conversion_pct=0.12,
            sequences_with_no_reply_pct=0.30,
            avg_bounce_rate_pct=0.01,
        )
        result = self.engine.assess(inp)
        assert result.email_sequence_pattern == EmailSequencePattern.timing_failure
        # timing_recalibration only when risk==high; moderate gives sequence_optimization
        assert result.recommended_action in {
            EmailSequenceAction.timing_recalibration,
            EmailSequenceAction.sequence_optimization,
        }

    def test_scenario_template_overuse(self):
        """Template overuse with high ratio."""
        inp = make_input(
            rep_id="template_user",
            avg_email_open_rate_pct=0.40,
            avg_email_reply_rate_pct=0.20,
            avg_unsubscribe_rate_pct=0.01,
            personalization_rate_pct=0.65,
            template_vs_custom_ratio=0.90,
            avg_email_word_count=100.0,
            calls_to_action_per_email_avg=1.0,
            avg_send_time_score=0.80,
            avg_days_between_touchpoints=2.0,
            avg_follow_up_attempts_per_prospect=5.0,
            email_to_meeting_conversion_pct=0.08,
            sequences_with_no_reply_pct=0.30,
            avg_bounce_rate_pct=0.02,
        )
        result = self.engine.assess(inp)
        assert result.email_sequence_pattern == EmailSequencePattern.template_overuse
        # With low composite, risk may be low => no_action, or moderate/high => sequence_opt/template_refresh
        assert result.recommended_action in {
            EmailSequenceAction.no_action,
            EmailSequenceAction.template_refresh,
            EmailSequenceAction.sequence_optimization,
        }

    def test_scenario_to_dict_round_trip(self):
        """Full round-trip through assess and to_dict."""
        result = self.engine.assess(make_input(rep_id="round_trip", region="Central"))
        d = result.to_dict()
        assert d["rep_id"] == "round_trip"
        assert d["region"] == "Central"
        assert d["email_sequence_risk"] in {"low", "moderate", "high", "critical"}
        assert d["email_sequence_pattern"] in {
            "none", "low_open_rate", "poor_personalization",
            "email_fatigue", "timing_failure", "template_overuse"
        }
        assert d["email_sequence_severity"] in {"strong", "developing", "weak", "failing"}
        assert d["recommended_action"] in {
            "no_action", "sequence_optimization", "personalization_coaching",
            "timing_recalibration", "template_refresh", "email_fatigue_intervention"
        }
        assert isinstance(d["has_sequence_gap"], bool)
        assert isinstance(d["requires_sequence_coaching"], bool)

    def test_scenario_batch_summary_consistency(self):
        """Batch assess then summary — total matches."""
        inputs = [make_input(rep_id=f"r{i}") for i in range(7)]
        results = self.engine.assess_batch(inputs)
        s = self.engine.summary()
        assert s["total"] == 7
        assert sum(s["risk_counts"].values()) == 7
        assert sum(s["pattern_counts"].values()) == 7
        assert sum(s["severity_counts"].values()) == 7
        assert sum(s["action_counts"].values()) == 7

    def test_scenario_coaching_required_with_low_reply(self):
        """Rep with low reply rate needs coaching."""
        inp = make_input(avg_email_reply_rate_pct=0.02)
        result = self.engine.assess(inp)
        assert result.requires_sequence_coaching is True

    def test_scenario_gap_from_high_unsubscribe(self):
        """High unsubscribe rate triggers sequence gap."""
        inp = make_input(avg_unsubscribe_rate_pct=0.08, email_to_meeting_conversion_pct=0.10)
        result = self.engine.assess(inp)
        assert result.has_sequence_gap is True

    def test_scenario_pipeline_impact_positive_when_critical(self):
        """Critical composite should yield nonzero pipeline impact (unless opp value 0)."""
        inp = make_input(
            avg_email_open_rate_pct=0.05, avg_email_reply_rate_pct=0.01,
            avg_unsubscribe_rate_pct=0.10, email_to_meeting_conversion_pct=0.01,
            avg_bounce_rate_pct=0.15, personalization_rate_pct=0.05,
            template_vs_custom_ratio=0.95, avg_email_word_count=400.0,
            calls_to_action_per_email_avg=5.0, avg_send_time_score=0.10,
            avg_days_between_touchpoints=20.0, avg_follow_up_attempts_per_prospect=1.0,
            sequences_with_no_reply_pct=0.70, total_sequences_active=100,
            avg_opportunity_value_usd=10_000.0,
        )
        result = self.engine.assess(inp)
        assert result.estimated_pipeline_impact_usd > 0.0
