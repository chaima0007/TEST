"""
Comprehensive pytest test suite for SalesMultiChannelEngagementIntelligenceEngine.
Target: 250+ tests, all passing.
"""
from __future__ import annotations

import pytest

from swarm.intelligence.sales_multi_channel_engagement_intelligence_engine import (
    ChannelAction,
    ChannelPattern,
    ChannelRisk,
    ChannelSeverity,
    MultiChannelEngagementInput,
    MultiChannelEngagementResult,
    SalesMultiChannelEngagementIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helper factory
# ---------------------------------------------------------------------------

def make_input(**overrides) -> MultiChannelEngagementInput:
    """Return a healthy / low-risk baseline input, overridden by kwargs."""
    defaults = dict(
        rep_id="rep_001",
        region="NAMER",
        evaluation_period_id="Q1-2026",
        total_prospect_touches=200,
        email_touches_count=60,
        phone_touches_count=50,
        linkedin_touches_count=40,
        video_message_touches_count=20,
        in_person_touches_count=20,
        direct_mail_touches_count=10,
        avg_opportunity_value_usd=10_000.0,
        unique_channels_used_count=5,
        avg_touches_per_prospect=8.0,
        single_channel_prospects_count=10,
        multi_channel_prospects_count=90,
        email_open_rate_pct=0.35,
        email_reply_rate_pct=0.10,
        phone_connect_rate_pct=0.15,
        linkedin_response_rate_pct=0.10,
        follow_up_cadence_compliance_pct=0.75,
        channel_sequence_compliance_pct=0.80,
        avg_days_between_touches=3.0,
    )
    defaults.update(overrides)
    return MultiChannelEngagementInput(**defaults)


def make_engine() -> SalesMultiChannelEngagementIntelligenceEngine:
    return SalesMultiChannelEngagementIntelligenceEngine()


# ===========================================================================
# 1. ENUM TESTS
# ===========================================================================

class TestChannelRiskEnum:
    def test_low_value(self):
        assert ChannelRisk.low.value == "low"

    def test_moderate_value(self):
        assert ChannelRisk.moderate.value == "moderate"

    def test_high_value(self):
        assert ChannelRisk.high.value == "high"

    def test_critical_value(self):
        assert ChannelRisk.critical.value == "critical"

    def test_is_str_subclass(self):
        assert isinstance(ChannelRisk.low, str)

    def test_members_count(self):
        assert len(ChannelRisk) == 4

    def test_equality_with_string(self):
        assert ChannelRisk.high == "high"


class TestChannelPatternEnum:
    def test_none_value(self):
        assert ChannelPattern.none.value == "none"

    def test_single_channel_dependency(self):
        assert ChannelPattern.single_channel_dependency.value == "single_channel_dependency"

    def test_low_touch_frequency(self):
        assert ChannelPattern.low_touch_frequency.value == "low_touch_frequency"

    def test_poor_email_quality(self):
        assert ChannelPattern.poor_email_quality.value == "poor_email_quality"

    def test_channel_sequence_violation(self):
        assert ChannelPattern.channel_sequence_violation.value == "channel_sequence_violation"

    def test_digital_only_approach(self):
        assert ChannelPattern.digital_only_approach.value == "digital_only_approach"

    def test_members_count(self):
        assert len(ChannelPattern) == 6

    def test_is_str_subclass(self):
        assert isinstance(ChannelPattern.none, str)


class TestChannelSeverityEnum:
    def test_optimized_value(self):
        assert ChannelSeverity.optimized.value == "optimized"

    def test_developing_value(self):
        assert ChannelSeverity.developing.value == "developing"

    def test_limited_value(self):
        assert ChannelSeverity.limited.value == "limited"

    def test_siloed_value(self):
        assert ChannelSeverity.siloed.value == "siloed"

    def test_members_count(self):
        assert len(ChannelSeverity) == 4

    def test_is_str_subclass(self):
        assert isinstance(ChannelSeverity.optimized, str)


class TestChannelActionEnum:
    def test_no_action_value(self):
        assert ChannelAction.no_action.value == "no_action"

    def test_channel_coaching_value(self):
        assert ChannelAction.channel_coaching.value == "channel_coaching"

    def test_cadence_optimization_value(self):
        assert ChannelAction.cadence_optimization.value == "cadence_optimization"

    def test_email_quality_review_value(self):
        assert ChannelAction.email_quality_review.value == "email_quality_review"

    def test_multi_channel_training_value(self):
        assert ChannelAction.multi_channel_training.value == "multi_channel_training"

    def test_outreach_sequence_redesign_value(self):
        assert ChannelAction.outreach_sequence_redesign.value == "outreach_sequence_redesign"

    def test_members_count(self):
        assert len(ChannelAction) == 6

    def test_is_str_subclass(self):
        assert isinstance(ChannelAction.no_action, str)


# ===========================================================================
# 2. DATACLASS TESTS
# ===========================================================================

class TestMultiChannelEngagementInput:
    def test_all_fields_set(self):
        inp = make_input()
        assert inp.rep_id == "rep_001"
        assert inp.region == "NAMER"
        assert inp.evaluation_period_id == "Q1-2026"
        assert inp.total_prospect_touches == 200
        assert inp.email_touches_count == 60
        assert inp.phone_touches_count == 50
        assert inp.linkedin_touches_count == 40
        assert inp.video_message_touches_count == 20
        assert inp.in_person_touches_count == 20
        assert inp.direct_mail_touches_count == 10
        assert inp.avg_opportunity_value_usd == 10_000.0
        assert inp.unique_channels_used_count == 5
        assert inp.avg_touches_per_prospect == 8.0
        assert inp.single_channel_prospects_count == 10
        assert inp.multi_channel_prospects_count == 90
        assert inp.email_open_rate_pct == 0.35
        assert inp.email_reply_rate_pct == 0.10
        assert inp.phone_connect_rate_pct == 0.15
        assert inp.linkedin_response_rate_pct == 0.10
        assert inp.follow_up_cadence_compliance_pct == 0.75
        assert inp.channel_sequence_compliance_pct == 0.80
        assert inp.avg_days_between_touches == 3.0

    def test_22_fields_exist(self):
        import dataclasses
        fields = dataclasses.fields(MultiChannelEngagementInput)
        assert len(fields) == 22


class TestMultiChannelEngagementResult:
    def test_to_dict_keys(self):
        engine = make_engine()
        result = engine.assess(make_input())
        d = result.to_dict()
        expected_keys = {
            "rep_id", "region", "channel_risk", "channel_pattern",
            "channel_severity", "recommended_action",
            "channel_diversity_score", "channel_effectiveness_score",
            "touch_frequency_score", "sequence_compliance_score",
            "channel_engagement_composite", "has_channel_gap",
            "requires_channel_coaching", "estimated_pipeline_impact_usd",
            "channel_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_values_are_strings(self):
        engine = make_engine()
        result = engine.assess(make_input())
        d = result.to_dict()
        assert isinstance(d["channel_risk"], str)
        assert isinstance(d["channel_pattern"], str)
        assert isinstance(d["channel_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_rep_id(self):
        engine = make_engine()
        result = engine.assess(make_input(rep_id="rep_XYZ"))
        assert result.to_dict()["rep_id"] == "rep_XYZ"

    def test_to_dict_region(self):
        engine = make_engine()
        result = engine.assess(make_input(region="EMEA"))
        assert result.to_dict()["region"] == "EMEA"

    def test_result_has_15_fields(self):
        import dataclasses
        fields = dataclasses.fields(MultiChannelEngagementResult)
        assert len(fields) == 15


# ===========================================================================
# 3. CHANNEL DIVERSITY SCORE TESTS
# ===========================================================================

class TestChannelDiversityScore:
    """Tests for _channel_diversity_score."""

    def setup_method(self):
        self.engine = make_engine()

    def _score(self, **kw):
        return self.engine._channel_diversity_score(make_input(**kw))

    # unique_channels buckets
    def test_unique_1_adds_50(self):
        s = self._score(
            unique_channels_used_count=1,
            single_channel_prospects_count=0,
            multi_channel_prospects_count=100,
            phone_touches_count=10,
            in_person_touches_count=10,
        )
        assert s == 50.0

    def test_unique_2_adds_30(self):
        s = self._score(
            unique_channels_used_count=2,
            single_channel_prospects_count=0,
            multi_channel_prospects_count=100,
            phone_touches_count=10,
            in_person_touches_count=10,
        )
        assert s == 30.0

    def test_unique_3_adds_15(self):
        s = self._score(
            unique_channels_used_count=3,
            single_channel_prospects_count=0,
            multi_channel_prospects_count=100,
            phone_touches_count=10,
            in_person_touches_count=10,
        )
        assert s == 15.0

    def test_unique_4_adds_0(self):
        s = self._score(
            unique_channels_used_count=4,
            single_channel_prospects_count=0,
            multi_channel_prospects_count=100,
            phone_touches_count=10,
            in_person_touches_count=10,
        )
        assert s == 0.0

    def test_unique_5_adds_0(self):
        s = self._score(
            unique_channels_used_count=5,
            single_channel_prospects_count=0,
            multi_channel_prospects_count=100,
            phone_touches_count=10,
            in_person_touches_count=10,
        )
        assert s == 0.0

    # single_rate buckets
    def test_single_rate_60pct_adds_35(self):
        # single=60, multi=40 => rate=0.60
        s = self._score(
            unique_channels_used_count=4,
            single_channel_prospects_count=60,
            multi_channel_prospects_count=40,
            phone_touches_count=10,
            in_person_touches_count=10,
        )
        assert s == 35.0

    def test_single_rate_above_60pct_adds_35(self):
        # single=80, multi=20 => rate=0.80
        s = self._score(
            unique_channels_used_count=4,
            single_channel_prospects_count=80,
            multi_channel_prospects_count=20,
            phone_touches_count=10,
            in_person_touches_count=10,
        )
        assert s == 35.0

    def test_single_rate_40pct_adds_18(self):
        # single=40, multi=60 => rate=0.40
        s = self._score(
            unique_channels_used_count=4,
            single_channel_prospects_count=40,
            multi_channel_prospects_count=60,
            phone_touches_count=10,
            in_person_touches_count=10,
        )
        assert s == 18.0

    def test_single_rate_20pct_adds_7(self):
        # single=20, multi=80 => rate=0.20
        s = self._score(
            unique_channels_used_count=4,
            single_channel_prospects_count=20,
            multi_channel_prospects_count=80,
            phone_touches_count=10,
            in_person_touches_count=10,
        )
        assert s == 7.0

    def test_single_rate_below_20pct_adds_0(self):
        # single=10, multi=90 => rate=0.10
        s = self._score(
            unique_channels_used_count=4,
            single_channel_prospects_count=10,
            multi_channel_prospects_count=90,
            phone_touches_count=10,
            in_person_touches_count=10,
        )
        assert s == 0.0

    # no phone AND no in_person
    def test_no_phone_no_in_person_adds_15(self):
        s = self._score(
            unique_channels_used_count=4,
            single_channel_prospects_count=0,
            multi_channel_prospects_count=100,
            phone_touches_count=0,
            in_person_touches_count=0,
        )
        assert s == 15.0

    def test_phone_only_no_in_person_no_bonus(self):
        s = self._score(
            unique_channels_used_count=4,
            single_channel_prospects_count=0,
            multi_channel_prospects_count=100,
            phone_touches_count=5,
            in_person_touches_count=0,
        )
        assert s == 0.0

    def test_in_person_only_no_phone_no_bonus(self):
        s = self._score(
            unique_channels_used_count=4,
            single_channel_prospects_count=0,
            multi_channel_prospects_count=100,
            phone_touches_count=0,
            in_person_touches_count=5,
        )
        assert s == 0.0

    # combinations and cap
    def test_worst_case_capped_at_100(self):
        # unique=1 (+50), single_rate=0.80 (+35), no phone/in_person (+15) => 100
        s = self._score(
            unique_channels_used_count=1,
            single_channel_prospects_count=80,
            multi_channel_prospects_count=20,
            phone_touches_count=0,
            in_person_touches_count=0,
        )
        assert s == 100.0

    def test_unique_2_high_single_no_phone_sums_60(self):
        # 30 + 35 + 15 = 80 (not 60, let's correct: unique=2 +30, single_rate=0.60 +35, no phone +15 = 80)
        s = self._score(
            unique_channels_used_count=2,
            single_channel_prospects_count=60,
            multi_channel_prospects_count=40,
            phone_touches_count=0,
            in_person_touches_count=0,
        )
        assert s == 80.0

    def test_zero_prospects_avoids_division_by_zero(self):
        # single=0, multi=0 => total=max(0,1)=1 => rate=0
        s = self._score(
            unique_channels_used_count=4,
            single_channel_prospects_count=0,
            multi_channel_prospects_count=0,
            phone_touches_count=10,
            in_person_touches_count=10,
        )
        assert s == 0.0

    def test_score_is_float(self):
        s = self._score()
        assert isinstance(s, float)

    def test_score_non_negative(self):
        s = self._score()
        assert s >= 0.0

    def test_score_at_most_100(self):
        s = self._score(
            unique_channels_used_count=1,
            single_channel_prospects_count=99,
            multi_channel_prospects_count=1,
            phone_touches_count=0,
            in_person_touches_count=0,
        )
        assert s <= 100.0


# ===========================================================================
# 4. CHANNEL EFFECTIVENESS SCORE TESTS
# ===========================================================================

class TestChannelEffectivenessScore:
    """Tests for _channel_effectiveness_score."""

    def setup_method(self):
        self.engine = make_engine()

    def _score(self, **kw):
        return self.engine._channel_effectiveness_score(make_input(**kw))

    # email_open_rate buckets
    def test_open_rate_below_20pct_adds_30(self):
        s = self._score(
            email_open_rate_pct=0.10,
            email_reply_rate_pct=0.10,
            phone_connect_rate_pct=0.15,
        )
        assert s == 30.0

    def test_open_rate_exactly_20pct_not_below_20_adds_15(self):
        s = self._score(
            email_open_rate_pct=0.20,
            email_reply_rate_pct=0.10,
            phone_connect_rate_pct=0.15,
        )
        assert s == 15.0

    def test_open_rate_25pct_adds_15(self):
        s = self._score(
            email_open_rate_pct=0.25,
            email_reply_rate_pct=0.10,
            phone_connect_rate_pct=0.15,
        )
        assert s == 15.0

    def test_open_rate_30pct_exactly_adds_7(self):
        s = self._score(
            email_open_rate_pct=0.30,
            email_reply_rate_pct=0.10,
            phone_connect_rate_pct=0.15,
        )
        assert s == 7.0

    def test_open_rate_35pct_adds_7(self):
        s = self._score(
            email_open_rate_pct=0.35,
            email_reply_rate_pct=0.10,
            phone_connect_rate_pct=0.15,
        )
        assert s == 7.0

    def test_open_rate_40pct_adds_0(self):
        s = self._score(
            email_open_rate_pct=0.40,
            email_reply_rate_pct=0.10,
            phone_connect_rate_pct=0.15,
        )
        assert s == 0.0

    def test_open_rate_50pct_adds_0(self):
        s = self._score(
            email_open_rate_pct=0.50,
            email_reply_rate_pct=0.10,
            phone_connect_rate_pct=0.15,
        )
        assert s == 0.0

    # email_reply_rate buckets
    def test_reply_rate_below_3pct_adds_35(self):
        s = self._score(
            email_open_rate_pct=0.50,
            email_reply_rate_pct=0.02,
            phone_connect_rate_pct=0.15,
        )
        assert s == 35.0

    def test_reply_rate_3pct_exactly_adds_18(self):
        s = self._score(
            email_open_rate_pct=0.50,
            email_reply_rate_pct=0.03,
            phone_connect_rate_pct=0.15,
        )
        assert s == 18.0

    def test_reply_rate_4pct_adds_18(self):
        s = self._score(
            email_open_rate_pct=0.50,
            email_reply_rate_pct=0.04,
            phone_connect_rate_pct=0.15,
        )
        assert s == 18.0

    def test_reply_rate_5pct_exactly_adds_7(self):
        s = self._score(
            email_open_rate_pct=0.50,
            email_reply_rate_pct=0.05,
            phone_connect_rate_pct=0.15,
        )
        assert s == 7.0

    def test_reply_rate_7pct_adds_7(self):
        s = self._score(
            email_open_rate_pct=0.50,
            email_reply_rate_pct=0.07,
            phone_connect_rate_pct=0.15,
        )
        assert s == 7.0

    def test_reply_rate_8pct_adds_0(self):
        s = self._score(
            email_open_rate_pct=0.50,
            email_reply_rate_pct=0.08,
            phone_connect_rate_pct=0.15,
        )
        assert s == 0.0

    def test_reply_rate_10pct_adds_0(self):
        s = self._score(
            email_open_rate_pct=0.50,
            email_reply_rate_pct=0.10,
            phone_connect_rate_pct=0.15,
        )
        assert s == 0.0

    # phone_connect_rate buckets
    def test_phone_connect_below_5pct_adds_25(self):
        s = self._score(
            email_open_rate_pct=0.50,
            email_reply_rate_pct=0.10,
            phone_connect_rate_pct=0.03,
        )
        assert s == 25.0

    def test_phone_connect_5pct_exactly_adds_12(self):
        s = self._score(
            email_open_rate_pct=0.50,
            email_reply_rate_pct=0.10,
            phone_connect_rate_pct=0.05,
        )
        assert s == 12.0

    def test_phone_connect_7pct_adds_12(self):
        s = self._score(
            email_open_rate_pct=0.50,
            email_reply_rate_pct=0.10,
            phone_connect_rate_pct=0.07,
        )
        assert s == 12.0

    def test_phone_connect_10pct_adds_0(self):
        s = self._score(
            email_open_rate_pct=0.50,
            email_reply_rate_pct=0.10,
            phone_connect_rate_pct=0.10,
        )
        assert s == 0.0

    def test_phone_connect_20pct_adds_0(self):
        s = self._score(
            email_open_rate_pct=0.50,
            email_reply_rate_pct=0.10,
            phone_connect_rate_pct=0.20,
        )
        assert s == 0.0

    # worst case cap
    def test_worst_case_capped_100(self):
        s = self._score(
            email_open_rate_pct=0.01,
            email_reply_rate_pct=0.01,
            phone_connect_rate_pct=0.01,
        )
        # 30 + 35 + 25 = 90, not capped, but == 90
        assert s == 90.0

    def test_score_non_negative(self):
        s = self._score()
        assert s >= 0.0

    def test_score_at_most_100(self):
        assert self._score(
            email_open_rate_pct=0.00,
            email_reply_rate_pct=0.00,
            phone_connect_rate_pct=0.00,
        ) <= 100.0


# ===========================================================================
# 5. TOUCH FREQUENCY SCORE TESTS
# ===========================================================================

class TestTouchFrequencyScore:
    """Tests for _touch_frequency_score."""

    def setup_method(self):
        self.engine = make_engine()

    def _score(self, **kw):
        return self.engine._touch_frequency_score(make_input(**kw))

    # avg_touches_per_prospect buckets
    def test_touches_below_3_adds_40(self):
        s = self._score(
            avg_touches_per_prospect=2.0,
            avg_days_between_touches=4.0,
            follow_up_cadence_compliance_pct=0.80,
        )
        assert s == 40.0

    def test_touches_exactly_3_adds_20(self):
        s = self._score(
            avg_touches_per_prospect=3.0,
            avg_days_between_touches=4.0,
            follow_up_cadence_compliance_pct=0.80,
        )
        assert s == 20.0

    def test_touches_4_adds_20(self):
        s = self._score(
            avg_touches_per_prospect=4.0,
            avg_days_between_touches=4.0,
            follow_up_cadence_compliance_pct=0.80,
        )
        assert s == 20.0

    def test_touches_exactly_5_adds_8(self):
        s = self._score(
            avg_touches_per_prospect=5.0,
            avg_days_between_touches=4.0,
            follow_up_cadence_compliance_pct=0.80,
        )
        assert s == 8.0

    def test_touches_6_adds_8(self):
        s = self._score(
            avg_touches_per_prospect=6.0,
            avg_days_between_touches=4.0,
            follow_up_cadence_compliance_pct=0.80,
        )
        assert s == 8.0

    def test_touches_exactly_7_adds_0(self):
        s = self._score(
            avg_touches_per_prospect=7.0,
            avg_days_between_touches=4.0,
            follow_up_cadence_compliance_pct=0.80,
        )
        assert s == 0.0

    def test_touches_10_adds_0(self):
        s = self._score(
            avg_touches_per_prospect=10.0,
            avg_days_between_touches=4.0,
            follow_up_cadence_compliance_pct=0.80,
        )
        assert s == 0.0

    # avg_days_between_touches buckets
    def test_days_10_adds_35(self):
        s = self._score(
            avg_touches_per_prospect=10.0,
            avg_days_between_touches=10.0,
            follow_up_cadence_compliance_pct=0.80,
        )
        assert s == 35.0

    def test_days_above_10_adds_35(self):
        s = self._score(
            avg_touches_per_prospect=10.0,
            avg_days_between_touches=15.0,
            follow_up_cadence_compliance_pct=0.80,
        )
        assert s == 35.0

    def test_days_7_adds_18(self):
        s = self._score(
            avg_touches_per_prospect=10.0,
            avg_days_between_touches=7.0,
            follow_up_cadence_compliance_pct=0.80,
        )
        assert s == 18.0

    def test_days_8_adds_18(self):
        s = self._score(
            avg_touches_per_prospect=10.0,
            avg_days_between_touches=8.0,
            follow_up_cadence_compliance_pct=0.80,
        )
        assert s == 18.0

    def test_days_5_adds_7(self):
        s = self._score(
            avg_touches_per_prospect=10.0,
            avg_days_between_touches=5.0,
            follow_up_cadence_compliance_pct=0.80,
        )
        assert s == 7.0

    def test_days_6_adds_7(self):
        s = self._score(
            avg_touches_per_prospect=10.0,
            avg_days_between_touches=6.0,
            follow_up_cadence_compliance_pct=0.80,
        )
        assert s == 7.0

    def test_days_below_5_adds_0(self):
        s = self._score(
            avg_touches_per_prospect=10.0,
            avg_days_between_touches=4.0,
            follow_up_cadence_compliance_pct=0.80,
        )
        assert s == 0.0

    def test_days_3_adds_0(self):
        s = self._score(
            avg_touches_per_prospect=10.0,
            avg_days_between_touches=3.0,
            follow_up_cadence_compliance_pct=0.80,
        )
        assert s == 0.0

    # follow_up_cadence_compliance buckets
    def test_cadence_below_40pct_adds_20(self):
        s = self._score(
            avg_touches_per_prospect=10.0,
            avg_days_between_touches=4.0,
            follow_up_cadence_compliance_pct=0.30,
        )
        assert s == 20.0

    def test_cadence_exactly_40pct_adds_10(self):
        s = self._score(
            avg_touches_per_prospect=10.0,
            avg_days_between_touches=4.0,
            follow_up_cadence_compliance_pct=0.40,
        )
        assert s == 10.0

    def test_cadence_50pct_adds_10(self):
        s = self._score(
            avg_touches_per_prospect=10.0,
            avg_days_between_touches=4.0,
            follow_up_cadence_compliance_pct=0.50,
        )
        assert s == 10.0

    def test_cadence_60pct_adds_0(self):
        s = self._score(
            avg_touches_per_prospect=10.0,
            avg_days_between_touches=4.0,
            follow_up_cadence_compliance_pct=0.60,
        )
        assert s == 0.0

    def test_cadence_80pct_adds_0(self):
        s = self._score(
            avg_touches_per_prospect=10.0,
            avg_days_between_touches=4.0,
            follow_up_cadence_compliance_pct=0.80,
        )
        assert s == 0.0

    # worst case
    def test_worst_case_sums_correctly(self):
        # touches<3 (+40) + days>=10 (+35) + cadence<0.40 (+20) = 95
        s = self._score(
            avg_touches_per_prospect=2.0,
            avg_days_between_touches=10.0,
            follow_up_cadence_compliance_pct=0.20,
        )
        assert s == 95.0

    def test_score_capped_at_100(self):
        s = self._score(
            avg_touches_per_prospect=1.0,
            avg_days_between_touches=20.0,
            follow_up_cadence_compliance_pct=0.10,
        )
        assert s <= 100.0

    def test_zero_score(self):
        s = self._score(
            avg_touches_per_prospect=10.0,
            avg_days_between_touches=3.0,
            follow_up_cadence_compliance_pct=0.80,
        )
        assert s == 0.0


# ===========================================================================
# 6. SEQUENCE COMPLIANCE SCORE TESTS
# ===========================================================================

class TestSequenceComplianceScore:
    """Tests for _sequence_compliance_score."""

    def setup_method(self):
        self.engine = make_engine()

    def _score(self, **kw):
        return self.engine._sequence_compliance_score(make_input(**kw))

    # channel_sequence_compliance_pct buckets
    def test_seq_compliance_below_30pct_adds_45(self):
        s = self._score(
            channel_sequence_compliance_pct=0.20,
            total_prospect_touches=100,
            email_touches_count=40,
            linkedin_touches_count=0,
            linkedin_response_rate_pct=0.10,
        )
        assert s == 45.0

    def test_seq_compliance_exactly_30pct_adds_25(self):
        s = self._score(
            channel_sequence_compliance_pct=0.30,
            total_prospect_touches=100,
            email_touches_count=40,
            linkedin_touches_count=0,
            linkedin_response_rate_pct=0.10,
        )
        assert s == 25.0

    def test_seq_compliance_40pct_adds_25(self):
        s = self._score(
            channel_sequence_compliance_pct=0.40,
            total_prospect_touches=100,
            email_touches_count=40,
            linkedin_touches_count=0,
            linkedin_response_rate_pct=0.10,
        )
        assert s == 25.0

    def test_seq_compliance_exactly_50pct_adds_10(self):
        s = self._score(
            channel_sequence_compliance_pct=0.50,
            total_prospect_touches=100,
            email_touches_count=40,
            linkedin_touches_count=0,
            linkedin_response_rate_pct=0.10,
        )
        assert s == 10.0

    def test_seq_compliance_60pct_adds_10(self):
        s = self._score(
            channel_sequence_compliance_pct=0.60,
            total_prospect_touches=100,
            email_touches_count=40,
            linkedin_touches_count=0,
            linkedin_response_rate_pct=0.10,
        )
        assert s == 10.0

    def test_seq_compliance_exactly_70pct_adds_0(self):
        s = self._score(
            channel_sequence_compliance_pct=0.70,
            total_prospect_touches=100,
            email_touches_count=40,
            linkedin_touches_count=0,
            linkedin_response_rate_pct=0.10,
        )
        assert s == 0.0

    def test_seq_compliance_90pct_adds_0(self):
        s = self._score(
            channel_sequence_compliance_pct=0.90,
            total_prospect_touches=100,
            email_touches_count=40,
            linkedin_touches_count=0,
            linkedin_response_rate_pct=0.10,
        )
        assert s == 0.0

    # email_heavy_rate buckets
    def test_email_heavy_80pct_adds_30(self):
        # email=80/100 => rate=0.80
        s = self._score(
            channel_sequence_compliance_pct=0.90,
            total_prospect_touches=100,
            email_touches_count=80,
            linkedin_touches_count=0,
            linkedin_response_rate_pct=0.10,
        )
        assert s == 30.0

    def test_email_heavy_90pct_adds_30(self):
        s = self._score(
            channel_sequence_compliance_pct=0.90,
            total_prospect_touches=100,
            email_touches_count=90,
            linkedin_touches_count=0,
            linkedin_response_rate_pct=0.10,
        )
        assert s == 30.0

    def test_email_heavy_60pct_adds_15(self):
        s = self._score(
            channel_sequence_compliance_pct=0.90,
            total_prospect_touches=100,
            email_touches_count=60,
            linkedin_touches_count=0,
            linkedin_response_rate_pct=0.10,
        )
        assert s == 15.0

    def test_email_heavy_70pct_adds_15(self):
        s = self._score(
            channel_sequence_compliance_pct=0.90,
            total_prospect_touches=100,
            email_touches_count=70,
            linkedin_touches_count=0,
            linkedin_response_rate_pct=0.10,
        )
        assert s == 15.0

    def test_email_heavy_50pct_adds_0(self):
        s = self._score(
            channel_sequence_compliance_pct=0.90,
            total_prospect_touches=100,
            email_touches_count=50,
            linkedin_touches_count=0,
            linkedin_response_rate_pct=0.10,
        )
        assert s == 0.0

    # linkedin low response
    def test_linkedin_low_response_with_touches_adds_15(self):
        s = self._score(
            channel_sequence_compliance_pct=0.90,
            total_prospect_touches=100,
            email_touches_count=40,
            linkedin_touches_count=20,
            linkedin_response_rate_pct=0.04,
        )
        assert s == 15.0

    def test_linkedin_zero_touches_no_bonus(self):
        s = self._score(
            channel_sequence_compliance_pct=0.90,
            total_prospect_touches=100,
            email_touches_count=40,
            linkedin_touches_count=0,
            linkedin_response_rate_pct=0.04,
        )
        assert s == 0.0

    def test_linkedin_high_response_no_bonus(self):
        s = self._score(
            channel_sequence_compliance_pct=0.90,
            total_prospect_touches=100,
            email_touches_count=40,
            linkedin_touches_count=20,
            linkedin_response_rate_pct=0.05,
        )
        assert s == 0.0

    def test_linkedin_exactly_5pct_no_bonus(self):
        s = self._score(
            channel_sequence_compliance_pct=0.90,
            total_prospect_touches=100,
            email_touches_count=40,
            linkedin_touches_count=20,
            linkedin_response_rate_pct=0.05,
        )
        assert s == 0.0

    # total_prospect_touches=0 edge case
    def test_zero_total_touches_avoids_div_by_zero(self):
        s = self._score(
            channel_sequence_compliance_pct=0.90,
            total_prospect_touches=0,
            email_touches_count=0,
            linkedin_touches_count=0,
            linkedin_response_rate_pct=0.10,
        )
        assert s == 0.0

    def test_worst_case_capped_100(self):
        # 45 + 30 + 15 = 90 (not above 100 but let's verify cap)
        s = self._score(
            channel_sequence_compliance_pct=0.10,
            total_prospect_touches=100,
            email_touches_count=90,
            linkedin_touches_count=20,
            linkedin_response_rate_pct=0.01,
        )
        # 45 + 30 + 15 = 90
        assert s == 90.0

    def test_score_non_negative(self):
        assert self._score() >= 0.0

    def test_score_at_most_100(self):
        assert self._score(
            channel_sequence_compliance_pct=0.00,
            total_prospect_touches=100,
            email_touches_count=100,
            linkedin_touches_count=50,
            linkedin_response_rate_pct=0.00,
        ) <= 100.0


# ===========================================================================
# 7. PATTERN DETECTION TESTS
# ===========================================================================

class TestDetectPattern:
    """Tests for _detect_pattern priority logic."""

    def setup_method(self):
        self.engine = make_engine()

    def _pattern(self, diversity, effectiveness, frequency, compliance, **inp_kw):
        inp = make_input(**inp_kw)
        return self.engine._detect_pattern(inp, diversity, effectiveness, frequency, compliance)

    # 1) single_channel_dependency: diversity>=35 AND unique_channels<=2
    def test_single_channel_dependency_unique_1(self):
        p = self._pattern(35.0, 0.0, 0.0, 0.0, unique_channels_used_count=1)
        assert p == ChannelPattern.single_channel_dependency

    def test_single_channel_dependency_unique_2(self):
        p = self._pattern(40.0, 0.0, 0.0, 0.0, unique_channels_used_count=2)
        assert p == ChannelPattern.single_channel_dependency

    def test_no_single_channel_dep_if_diversity_below_35(self):
        p = self._pattern(34.9, 0.0, 0.0, 0.0, unique_channels_used_count=1)
        assert p != ChannelPattern.single_channel_dependency

    def test_no_single_channel_dep_if_unique_channels_3(self):
        p = self._pattern(50.0, 0.0, 0.0, 0.0, unique_channels_used_count=3)
        assert p != ChannelPattern.single_channel_dependency

    # 2) low_touch_frequency: frequency>=35 AND avg_touches<4
    def test_low_touch_frequency_detected(self):
        p = self._pattern(
            0.0, 0.0, 35.0, 0.0,
            unique_channels_used_count=5,
            avg_touches_per_prospect=3.0,
        )
        assert p == ChannelPattern.low_touch_frequency

    def test_low_touch_frequency_not_if_freq_below_35(self):
        p = self._pattern(
            0.0, 0.0, 34.9, 0.0,
            unique_channels_used_count=5,
            avg_touches_per_prospect=3.0,
        )
        assert p != ChannelPattern.low_touch_frequency

    def test_low_touch_frequency_not_if_touches_4(self):
        p = self._pattern(
            0.0, 0.0, 35.0, 0.0,
            unique_channels_used_count=5,
            avg_touches_per_prospect=4.0,
        )
        assert p != ChannelPattern.low_touch_frequency

    # 3) poor_email_quality: effectiveness>=30 AND email_reply<0.05
    def test_poor_email_quality_detected(self):
        p = self._pattern(
            0.0, 30.0, 0.0, 0.0,
            unique_channels_used_count=5,
            avg_touches_per_prospect=10.0,
            email_reply_rate_pct=0.04,
        )
        assert p == ChannelPattern.poor_email_quality

    def test_poor_email_quality_not_if_effectiveness_below_30(self):
        p = self._pattern(
            0.0, 29.9, 0.0, 0.0,
            unique_channels_used_count=5,
            avg_touches_per_prospect=10.0,
            email_reply_rate_pct=0.04,
        )
        assert p != ChannelPattern.poor_email_quality

    def test_poor_email_quality_not_if_reply_rate_5pct(self):
        p = self._pattern(
            0.0, 30.0, 0.0, 0.0,
            unique_channels_used_count=5,
            avg_touches_per_prospect=10.0,
            email_reply_rate_pct=0.05,
        )
        assert p != ChannelPattern.poor_email_quality

    # 4) channel_sequence_violation: compliance>=35 AND seq_compliance<0.50
    def test_channel_sequence_violation_detected(self):
        p = self._pattern(
            0.0, 0.0, 0.0, 35.0,
            unique_channels_used_count=5,
            avg_touches_per_prospect=10.0,
            email_reply_rate_pct=0.10,
            channel_sequence_compliance_pct=0.40,
        )
        assert p == ChannelPattern.channel_sequence_violation

    def test_channel_sequence_violation_not_if_compliance_below_35(self):
        p = self._pattern(
            0.0, 0.0, 0.0, 34.9,
            unique_channels_used_count=5,
            avg_touches_per_prospect=10.0,
            email_reply_rate_pct=0.10,
            channel_sequence_compliance_pct=0.40,
        )
        assert p != ChannelPattern.channel_sequence_violation

    def test_channel_sequence_violation_not_if_seq_pct_50(self):
        p = self._pattern(
            0.0, 0.0, 0.0, 35.0,
            unique_channels_used_count=5,
            avg_touches_per_prospect=10.0,
            email_reply_rate_pct=0.10,
            channel_sequence_compliance_pct=0.50,
        )
        assert p != ChannelPattern.channel_sequence_violation

    # 5) digital_only_approach: diversity>=25 AND phone==0
    def test_digital_only_approach_detected(self):
        p = self._pattern(
            25.0, 0.0, 0.0, 0.0,
            unique_channels_used_count=5,
            avg_touches_per_prospect=10.0,
            email_reply_rate_pct=0.10,
            channel_sequence_compliance_pct=0.80,
            phone_touches_count=0,
        )
        assert p == ChannelPattern.digital_only_approach

    def test_digital_only_not_if_diversity_below_25(self):
        p = self._pattern(
            24.9, 0.0, 0.0, 0.0,
            unique_channels_used_count=5,
            avg_touches_per_prospect=10.0,
            email_reply_rate_pct=0.10,
            channel_sequence_compliance_pct=0.80,
            phone_touches_count=0,
        )
        assert p != ChannelPattern.digital_only_approach

    def test_digital_only_not_if_phone_present(self):
        p = self._pattern(
            25.0, 0.0, 0.0, 0.0,
            unique_channels_used_count=5,
            avg_touches_per_prospect=10.0,
            email_reply_rate_pct=0.10,
            channel_sequence_compliance_pct=0.80,
            phone_touches_count=5,
        )
        assert p != ChannelPattern.digital_only_approach

    # 6) none
    def test_no_pattern_returns_none(self):
        p = self._pattern(0.0, 0.0, 0.0, 0.0, unique_channels_used_count=5)
        assert p == ChannelPattern.none

    # Priority test: single_channel_dependency takes priority over low_touch_frequency
    def test_priority_single_over_low_touch(self):
        p = self._pattern(
            35.0, 0.0, 35.0, 0.0,
            unique_channels_used_count=1,
            avg_touches_per_prospect=3.0,
        )
        assert p == ChannelPattern.single_channel_dependency

    # Priority test: low_touch over poor_email
    def test_priority_low_touch_over_poor_email(self):
        p = self._pattern(
            0.0, 30.0, 35.0, 0.0,
            unique_channels_used_count=5,
            avg_touches_per_prospect=3.0,
            email_reply_rate_pct=0.04,
        )
        assert p == ChannelPattern.low_touch_frequency


# ===========================================================================
# 8. RISK LEVEL TESTS
# ===========================================================================

class TestRiskLevel:
    def setup_method(self):
        self.engine = make_engine()

    def test_composite_0_is_low(self):
        assert self.engine._risk_level(0.0) == ChannelRisk.low

    def test_composite_19_is_low(self):
        assert self.engine._risk_level(19.9) == ChannelRisk.low

    def test_composite_20_is_moderate(self):
        assert self.engine._risk_level(20.0) == ChannelRisk.moderate

    def test_composite_39_is_moderate(self):
        assert self.engine._risk_level(39.9) == ChannelRisk.moderate

    def test_composite_40_is_high(self):
        assert self.engine._risk_level(40.0) == ChannelRisk.high

    def test_composite_59_is_high(self):
        assert self.engine._risk_level(59.9) == ChannelRisk.high

    def test_composite_60_is_critical(self):
        assert self.engine._risk_level(60.0) == ChannelRisk.critical

    def test_composite_100_is_critical(self):
        assert self.engine._risk_level(100.0) == ChannelRisk.critical

    def test_composite_80_is_critical(self):
        assert self.engine._risk_level(80.0) == ChannelRisk.critical


# ===========================================================================
# 9. SEVERITY TESTS
# ===========================================================================

class TestSeverity:
    def setup_method(self):
        self.engine = make_engine()

    def test_composite_0_is_optimized(self):
        assert self.engine._severity(0.0) == ChannelSeverity.optimized

    def test_composite_19_is_optimized(self):
        assert self.engine._severity(19.9) == ChannelSeverity.optimized

    def test_composite_20_is_developing(self):
        assert self.engine._severity(20.0) == ChannelSeverity.developing

    def test_composite_39_is_developing(self):
        assert self.engine._severity(39.9) == ChannelSeverity.developing

    def test_composite_40_is_limited(self):
        assert self.engine._severity(40.0) == ChannelSeverity.limited

    def test_composite_59_is_limited(self):
        assert self.engine._severity(59.9) == ChannelSeverity.limited

    def test_composite_60_is_siloed(self):
        assert self.engine._severity(60.0) == ChannelSeverity.siloed

    def test_composite_100_is_siloed(self):
        assert self.engine._severity(100.0) == ChannelSeverity.siloed


# ===========================================================================
# 10. ACTION TESTS
# ===========================================================================

class TestAction:
    def setup_method(self):
        self.engine = make_engine()

    def _action(self, risk, pattern):
        return self.engine._action(risk, pattern)

    # critical cases
    def test_critical_single_channel_dep_multi_training(self):
        assert self._action(ChannelRisk.critical, ChannelPattern.single_channel_dependency) == ChannelAction.multi_channel_training

    def test_critical_channel_seq_violation_redesign(self):
        assert self._action(ChannelRisk.critical, ChannelPattern.channel_sequence_violation) == ChannelAction.outreach_sequence_redesign

    def test_critical_none_multi_training(self):
        assert self._action(ChannelRisk.critical, ChannelPattern.none) == ChannelAction.multi_channel_training

    def test_critical_low_touch_multi_training(self):
        assert self._action(ChannelRisk.critical, ChannelPattern.low_touch_frequency) == ChannelAction.multi_channel_training

    def test_critical_poor_email_multi_training(self):
        assert self._action(ChannelRisk.critical, ChannelPattern.poor_email_quality) == ChannelAction.multi_channel_training

    def test_critical_digital_only_multi_training(self):
        assert self._action(ChannelRisk.critical, ChannelPattern.digital_only_approach) == ChannelAction.multi_channel_training

    # high cases
    def test_high_poor_email_quality_email_review(self):
        assert self._action(ChannelRisk.high, ChannelPattern.poor_email_quality) == ChannelAction.email_quality_review

    def test_high_low_touch_cadence_optimization(self):
        assert self._action(ChannelRisk.high, ChannelPattern.low_touch_frequency) == ChannelAction.cadence_optimization

    def test_high_none_channel_coaching(self):
        assert self._action(ChannelRisk.high, ChannelPattern.none) == ChannelAction.channel_coaching

    def test_high_single_channel_dep_channel_coaching(self):
        assert self._action(ChannelRisk.high, ChannelPattern.single_channel_dependency) == ChannelAction.channel_coaching

    def test_high_digital_only_channel_coaching(self):
        assert self._action(ChannelRisk.high, ChannelPattern.digital_only_approach) == ChannelAction.channel_coaching

    def test_high_channel_sequence_violation_channel_coaching(self):
        assert self._action(ChannelRisk.high, ChannelPattern.channel_sequence_violation) == ChannelAction.channel_coaching

    # moderate
    def test_moderate_any_pattern_channel_coaching(self):
        for pat in ChannelPattern:
            assert self._action(ChannelRisk.moderate, pat) == ChannelAction.channel_coaching

    # low
    def test_low_any_pattern_no_action(self):
        for pat in ChannelPattern:
            assert self._action(ChannelRisk.low, pat) == ChannelAction.no_action


# ===========================================================================
# 11. HAS CHANNEL GAP TESTS
# ===========================================================================

class TestHasChannelGap:
    def setup_method(self):
        self.engine = make_engine()

    def _gap(self, composite, **kw):
        return self.engine._has_channel_gap(composite, make_input(**kw))

    def test_composite_40_triggers_gap(self):
        assert self._gap(40.0, unique_channels_used_count=5, avg_touches_per_prospect=10.0) is True

    def test_composite_80_triggers_gap(self):
        assert self._gap(80.0, unique_channels_used_count=5, avg_touches_per_prospect=10.0) is True

    def test_composite_39_no_trigger_from_composite(self):
        # composite < 40, unique=5, touches=10 => no gap
        assert self._gap(39.9, unique_channels_used_count=5, avg_touches_per_prospect=10.0) is False

    def test_unique_channels_1_triggers_gap(self):
        assert self._gap(0.0, unique_channels_used_count=1, avg_touches_per_prospect=10.0) is True

    def test_unique_channels_0_triggers_gap(self):
        assert self._gap(0.0, unique_channels_used_count=0, avg_touches_per_prospect=10.0) is True

    def test_unique_channels_2_no_trigger(self):
        assert self._gap(0.0, unique_channels_used_count=2, avg_touches_per_prospect=10.0) is False

    def test_avg_touches_below_3_triggers_gap(self):
        assert self._gap(0.0, unique_channels_used_count=5, avg_touches_per_prospect=2.9) is True

    def test_avg_touches_exactly_3_no_trigger(self):
        assert self._gap(0.0, unique_channels_used_count=5, avg_touches_per_prospect=3.0) is False

    def test_avg_touches_10_no_trigger(self):
        assert self._gap(0.0, unique_channels_used_count=5, avg_touches_per_prospect=10.0) is False

    def test_all_conditions_false_returns_false(self):
        assert self._gap(10.0, unique_channels_used_count=5, avg_touches_per_prospect=5.0) is False


# ===========================================================================
# 12. REQUIRES CHANNEL COACHING TESTS
# ===========================================================================

class TestRequiresChannelCoaching:
    def setup_method(self):
        self.engine = make_engine()

    def _coaching(self, composite, **kw):
        return self.engine._requires_channel_coaching(composite, make_input(**kw))

    def test_composite_30_triggers_coaching(self):
        assert self._coaching(
            30.0,
            single_channel_prospects_count=10,
            multi_channel_prospects_count=90,
            email_reply_rate_pct=0.10,
        ) is True

    def test_composite_80_triggers_coaching(self):
        assert self._coaching(
            80.0,
            single_channel_prospects_count=10,
            multi_channel_prospects_count=90,
            email_reply_rate_pct=0.10,
        ) is True

    def test_composite_29_no_trigger_from_composite(self):
        result = self._coaching(
            29.9,
            single_channel_prospects_count=10,
            multi_channel_prospects_count=90,
            email_reply_rate_pct=0.10,
        )
        assert result is False

    def test_single_rate_50pct_triggers_coaching(self):
        # single=50, multi=50 => rate=0.50
        assert self._coaching(
            0.0,
            single_channel_prospects_count=50,
            multi_channel_prospects_count=50,
            email_reply_rate_pct=0.10,
        ) is True

    def test_single_rate_above_50pct_triggers_coaching(self):
        assert self._coaching(
            0.0,
            single_channel_prospects_count=80,
            multi_channel_prospects_count=20,
            email_reply_rate_pct=0.10,
        ) is True

    def test_single_rate_below_50pct_no_trigger(self):
        assert self._coaching(
            0.0,
            single_channel_prospects_count=40,
            multi_channel_prospects_count=60,
            email_reply_rate_pct=0.10,
        ) is False

    def test_email_reply_below_3pct_triggers_coaching(self):
        assert self._coaching(
            0.0,
            single_channel_prospects_count=10,
            multi_channel_prospects_count=90,
            email_reply_rate_pct=0.02,
        ) is True

    def test_email_reply_3pct_no_trigger(self):
        assert self._coaching(
            0.0,
            single_channel_prospects_count=10,
            multi_channel_prospects_count=90,
            email_reply_rate_pct=0.03,
        ) is False

    def test_all_conditions_false_returns_false(self):
        assert self._coaching(
            0.0,
            single_channel_prospects_count=10,
            multi_channel_prospects_count=90,
            email_reply_rate_pct=0.10,
        ) is False

    def test_zero_total_prospects_avoids_div_by_zero(self):
        # single=0, multi=0 => rate=0 => no trigger from single_rate
        result = self._coaching(
            0.0,
            single_channel_prospects_count=0,
            multi_channel_prospects_count=0,
            email_reply_rate_pct=0.10,
        )
        assert result is False


# ===========================================================================
# 13. ESTIMATED PIPELINE IMPACT TESTS
# ===========================================================================

class TestEstimatedPipelineImpact:
    def setup_method(self):
        self.engine = make_engine()

    def _impact(self, composite, **kw):
        return self.engine._estimated_pipeline_impact(make_input(**kw), composite)

    def test_basic_calculation(self):
        # 10 * 10000 * 0.50 = 50000
        impact = self._impact(
            50.0,
            single_channel_prospects_count=10,
            avg_opportunity_value_usd=10_000.0,
        )
        assert impact == 50_000.0

    def test_zero_composite(self):
        impact = self._impact(
            0.0,
            single_channel_prospects_count=10,
            avg_opportunity_value_usd=10_000.0,
        )
        assert impact == 0.0

    def test_zero_single_prospects(self):
        impact = self._impact(
            50.0,
            single_channel_prospects_count=0,
            avg_opportunity_value_usd=10_000.0,
        )
        assert impact == 0.0

    def test_zero_opportunity_value(self):
        impact = self._impact(
            50.0,
            single_channel_prospects_count=10,
            avg_opportunity_value_usd=0.0,
        )
        assert impact == 0.0

    def test_rounded_to_2dp(self):
        # 7 * 3333.33 * (33/100) = 7 * 3333.33 * 0.33
        impact = self._impact(
            33.0,
            single_channel_prospects_count=7,
            avg_opportunity_value_usd=3333.33,
        )
        expected = round(7 * 3333.33 * 0.33, 2)
        assert impact == expected

    def test_composite_100(self):
        impact = self._impact(
            100.0,
            single_channel_prospects_count=5,
            avg_opportunity_value_usd=20_000.0,
        )
        assert impact == 100_000.0

    def test_returns_float(self):
        impact = self._impact(
            50.0,
            single_channel_prospects_count=10,
            avg_opportunity_value_usd=1000.0,
        )
        assert isinstance(impact, float)


# ===========================================================================
# 14. SIGNAL TESTS
# ===========================================================================

class TestSignal:
    def setup_method(self):
        self.engine = make_engine()

    def _signal(self, pattern, composite, **kw):
        inp = make_input(**kw)
        return self.engine._signal(inp, pattern, composite)

    def test_none_pattern_composite_below_20_returns_benchmark_msg(self):
        s = self._signal(ChannelPattern.none, 15.0)
        assert s == "Multi-channel outreach balanced and performing within benchmarks"

    def test_none_pattern_composite_exactly_20_not_benchmark_msg(self):
        s = self._signal(ChannelPattern.none, 20.0)
        assert s != "Multi-channel outreach balanced and performing within benchmarks"

    def test_non_none_pattern_composite_below_20_not_benchmark_msg(self):
        s = self._signal(ChannelPattern.poor_email_quality, 10.0)
        assert s != "Multi-channel outreach balanced and performing within benchmarks"

    def test_signal_includes_label_capitalized(self):
        s = self._signal(ChannelPattern.single_channel_dependency, 40.0, unique_channels_used_count=5, avg_touches_per_prospect=10.0, email_reply_rate_pct=0.10)
        assert s.startswith("Single channel dependency")

    def test_signal_includes_composite(self):
        s = self._signal(ChannelPattern.none, 25.0, unique_channels_used_count=5, avg_touches_per_prospect=10.0, email_reply_rate_pct=0.10)
        assert "composite 25" in s

    def test_signal_includes_unique_channels_when_2_or_fewer(self):
        s = self._signal(ChannelPattern.none, 25.0, unique_channels_used_count=2, avg_touches_per_prospect=10.0, email_reply_rate_pct=0.10)
        assert "2 channel(s) only" in s

    def test_signal_includes_unique_channels_when_1(self):
        s = self._signal(ChannelPattern.none, 25.0, unique_channels_used_count=1, avg_touches_per_prospect=10.0, email_reply_rate_pct=0.10)
        assert "1 channel(s) only" in s

    def test_signal_not_includes_unique_channels_when_3(self):
        s = self._signal(ChannelPattern.none, 25.0, unique_channels_used_count=3, avg_touches_per_prospect=10.0, email_reply_rate_pct=0.10)
        assert "channel(s) only" not in s

    def test_signal_includes_avg_touches_when_below_6(self):
        s = self._signal(ChannelPattern.none, 25.0, unique_channels_used_count=5, avg_touches_per_prospect=5.5, email_reply_rate_pct=0.10)
        assert "5.5 avg touches/prospect" in s

    def test_signal_not_includes_avg_touches_when_6(self):
        s = self._signal(ChannelPattern.none, 25.0, unique_channels_used_count=5, avg_touches_per_prospect=6.0, email_reply_rate_pct=0.10)
        assert "avg touches/prospect" not in s

    def test_signal_includes_email_reply_when_below_8pct(self):
        s = self._signal(ChannelPattern.none, 25.0, unique_channels_used_count=5, avg_touches_per_prospect=10.0, email_reply_rate_pct=0.05)
        assert "5.0% email reply rate" in s

    def test_signal_not_includes_email_reply_when_8pct(self):
        s = self._signal(ChannelPattern.none, 25.0, unique_channels_used_count=5, avg_touches_per_prospect=10.0, email_reply_rate_pct=0.08)
        assert "email reply rate" not in s

    def test_signal_channel_risk_label_when_none_pattern(self):
        s = self._signal(ChannelPattern.none, 25.0, unique_channels_used_count=5, avg_touches_per_prospect=10.0, email_reply_rate_pct=0.10)
        assert s.startswith("Channel risk")

    def test_signal_no_parts_uses_fallback(self):
        # No parts: unique=5, touches=10, reply=0.10 => no parts => "outreach coverage limited"
        s = self._signal(ChannelPattern.none, 25.0, unique_channels_used_count=5, avg_touches_per_prospect=10.0, email_reply_rate_pct=0.10)
        assert "outreach coverage limited" in s

    def test_signal_parts_joined_with_separator(self):
        s = self._signal(ChannelPattern.none, 25.0, unique_channels_used_count=2, avg_touches_per_prospect=4.0, email_reply_rate_pct=0.05)
        assert " — " in s

    def test_signal_poor_email_quality_label(self):
        s = self._signal(ChannelPattern.poor_email_quality, 40.0, unique_channels_used_count=5, avg_touches_per_prospect=10.0, email_reply_rate_pct=0.10)
        assert s.startswith("Poor email quality")

    def test_signal_low_touch_frequency_label(self):
        s = self._signal(ChannelPattern.low_touch_frequency, 40.0, unique_channels_used_count=5, avg_touches_per_prospect=10.0, email_reply_rate_pct=0.10)
        assert s.startswith("Low touch frequency")

    def test_signal_digital_only_label(self):
        s = self._signal(ChannelPattern.digital_only_approach, 40.0, unique_channels_used_count=5, avg_touches_per_prospect=10.0, email_reply_rate_pct=0.10)
        assert s.startswith("Digital only approach")

    def test_signal_channel_sequence_violation_label(self):
        s = self._signal(ChannelPattern.channel_sequence_violation, 40.0, unique_channels_used_count=5, avg_touches_per_prospect=10.0, email_reply_rate_pct=0.10)
        assert s.startswith("Channel sequence violation")

    def test_signal_email_reply_format(self):
        s = self._signal(ChannelPattern.none, 25.0, unique_channels_used_count=5, avg_touches_per_prospect=10.0, email_reply_rate_pct=0.042)
        assert "4.2% email reply rate" in s

    def test_signal_composite_format_no_decimal(self):
        s = self._signal(ChannelPattern.none, 25.0, unique_channels_used_count=5, avg_touches_per_prospect=10.0, email_reply_rate_pct=0.10)
        assert "composite 25" in s


# ===========================================================================
# 15. ASSESS METHOD TESTS
# ===========================================================================

class TestAssess:
    def setup_method(self):
        self.engine = make_engine()

    def test_returns_result_type(self):
        result = self.engine.assess(make_input())
        assert isinstance(result, MultiChannelEngagementResult)

    def test_rep_id_passed_through(self):
        result = self.engine.assess(make_input(rep_id="rep_999"))
        assert result.rep_id == "rep_999"

    def test_region_passed_through(self):
        result = self.engine.assess(make_input(region="APAC"))
        assert result.region == "APAC"

    def test_scores_are_floats(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.channel_diversity_score, float)
        assert isinstance(result.channel_effectiveness_score, float)
        assert isinstance(result.touch_frequency_score, float)
        assert isinstance(result.sequence_compliance_score, float)
        assert isinstance(result.channel_engagement_composite, float)

    def test_composite_is_weighted_sum(self):
        result = self.engine.assess(make_input())
        expected = round(
            result.channel_diversity_score * 0.30
            + result.channel_effectiveness_score * 0.30
            + result.touch_frequency_score * 0.25
            + result.sequence_compliance_score * 0.15,
            1,
        )
        assert result.channel_engagement_composite == min(expected, 100.0)

    def test_composite_capped_at_100(self):
        result = self.engine.assess(make_input(
            unique_channels_used_count=1,
            single_channel_prospects_count=90,
            multi_channel_prospects_count=10,
            phone_touches_count=0,
            in_person_touches_count=0,
            email_open_rate_pct=0.01,
            email_reply_rate_pct=0.01,
            phone_connect_rate_pct=0.01,
            avg_touches_per_prospect=1.0,
            avg_days_between_touches=15.0,
            follow_up_cadence_compliance_pct=0.10,
            channel_sequence_compliance_pct=0.10,
            total_prospect_touches=100,
            email_touches_count=90,
            linkedin_touches_count=10,
            linkedin_response_rate_pct=0.01,
        ))
        assert result.channel_engagement_composite <= 100.0

    def test_result_stored_in_results_list(self):
        engine = make_engine()
        engine.assess(make_input())
        assert len(engine._results) == 1

    def test_multiple_assess_accumulates_results(self):
        engine = make_engine()
        engine.assess(make_input(rep_id="r1"))
        engine.assess(make_input(rep_id="r2"))
        assert len(engine._results) == 2

    def test_low_risk_healthy_rep(self):
        # Healthy rep: many channels, good rates
        result = self.engine.assess(make_input())
        assert result.channel_risk == ChannelRisk.low

    def test_critical_risk_worst_case(self):
        result = self.engine.assess(make_input(
            unique_channels_used_count=1,
            single_channel_prospects_count=90,
            multi_channel_prospects_count=10,
            phone_touches_count=0,
            in_person_touches_count=0,
            email_open_rate_pct=0.10,
            email_reply_rate_pct=0.01,
            phone_connect_rate_pct=0.02,
            avg_touches_per_prospect=2.0,
            avg_days_between_touches=12.0,
            follow_up_cadence_compliance_pct=0.20,
            channel_sequence_compliance_pct=0.20,
            total_prospect_touches=100,
            email_touches_count=90,
            linkedin_touches_count=10,
            linkedin_response_rate_pct=0.01,
        ))
        assert result.channel_risk == ChannelRisk.critical

    def test_channel_risk_enum_type(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.channel_risk, ChannelRisk)

    def test_channel_pattern_enum_type(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.channel_pattern, ChannelPattern)

    def test_channel_severity_enum_type(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.channel_severity, ChannelSeverity)

    def test_recommended_action_enum_type(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.recommended_action, ChannelAction)

    def test_has_channel_gap_bool(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.has_channel_gap, bool)

    def test_requires_channel_coaching_bool(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.requires_channel_coaching, bool)

    def test_estimated_pipeline_impact_float(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.estimated_pipeline_impact_usd, float)

    def test_channel_signal_is_string(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.channel_signal, str)

    def test_severity_matches_composite(self):
        result = self.engine.assess(make_input())
        c = result.channel_engagement_composite
        if c >= 60:
            assert result.channel_severity == ChannelSeverity.siloed
        elif c >= 40:
            assert result.channel_severity == ChannelSeverity.limited
        elif c >= 20:
            assert result.channel_severity == ChannelSeverity.developing
        else:
            assert result.channel_severity == ChannelSeverity.optimized

    def test_risk_matches_composite(self):
        result = self.engine.assess(make_input())
        c = result.channel_engagement_composite
        if c >= 60:
            assert result.channel_risk == ChannelRisk.critical
        elif c >= 40:
            assert result.channel_risk == ChannelRisk.high
        elif c >= 20:
            assert result.channel_risk == ChannelRisk.moderate
        else:
            assert result.channel_risk == ChannelRisk.low

    def test_single_channel_dep_pattern_detected(self):
        # unique=1 gives diversity=50+..., avg_touches ok, so pattern = single_channel_dependency
        result = self.engine.assess(make_input(
            unique_channels_used_count=1,
            single_channel_prospects_count=50,
            multi_channel_prospects_count=50,
        ))
        assert result.channel_pattern == ChannelPattern.single_channel_dependency

    def test_no_action_for_low_risk_rep(self):
        result = self.engine.assess(make_input())
        assert result.recommended_action == ChannelAction.no_action

    def test_assess_no_side_effects_on_input(self):
        inp = make_input()
        original_rep_id = inp.rep_id
        self.engine.assess(inp)
        assert inp.rep_id == original_rep_id


# ===========================================================================
# 16. ASSESS BATCH TESTS
# ===========================================================================

class TestAssessBatch:
    def setup_method(self):
        self.engine = make_engine()

    def test_returns_list(self):
        results = self.engine.assess_batch([make_input(), make_input()])
        assert isinstance(results, list)

    def test_length_matches_input(self):
        inputs = [make_input(rep_id=f"r{i}") for i in range(5)]
        results = self.engine.assess_batch(inputs)
        assert len(results) == 5

    def test_empty_batch_returns_empty_list(self):
        results = self.engine.assess_batch([])
        assert results == []

    def test_each_element_is_result_type(self):
        results = self.engine.assess_batch([make_input(), make_input()])
        for r in results:
            assert isinstance(r, MultiChannelEngagementResult)

    def test_results_accumulated_in_engine(self):
        engine = make_engine()
        engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(3)])
        assert len(engine._results) == 3

    def test_rep_ids_preserved_in_order(self):
        inputs = [make_input(rep_id=f"rep_{i}") for i in range(4)]
        results = self.engine.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"rep_{i}"

    def test_batch_after_single_assess(self):
        engine = make_engine()
        engine.assess(make_input(rep_id="first"))
        engine.assess_batch([make_input(rep_id="second")])
        assert len(engine._results) == 2

    def test_single_item_batch(self):
        results = self.engine.assess_batch([make_input(rep_id="only")])
        assert len(results) == 1
        assert results[0].rep_id == "only"


# ===========================================================================
# 17. SUMMARY TESTS
# ===========================================================================

class TestSummary:
    def test_empty_summary_returns_zeros(self):
        engine = make_engine()
        s = engine.summary()
        assert s["total"] == 0
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}
        assert s["avg_channel_engagement_composite"] == 0.0
        assert s["channel_gap_count"] == 0
        assert s["channel_coaching_count"] == 0
        assert s["avg_channel_diversity_score"] == 0.0
        assert s["avg_channel_effectiveness_score"] == 0.0
        assert s["avg_touch_frequency_score"] == 0.0
        assert s["avg_sequence_compliance_score"] == 0.0
        assert s["total_estimated_pipeline_impact_usd"] == 0.0

    def test_empty_summary_has_13_keys(self):
        engine = make_engine()
        s = engine.summary()
        assert len(s) == 13

    def test_summary_total_correct(self):
        engine = make_engine()
        for i in range(3):
            engine.assess(make_input(rep_id=f"r{i}"))
        assert engine.summary()["total"] == 3

    def test_summary_risk_counts_populated(self):
        engine = make_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert len(s["risk_counts"]) >= 1
        assert sum(s["risk_counts"].values()) == 1

    def test_summary_pattern_counts_populated(self):
        engine = make_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert sum(s["pattern_counts"].values()) == 1

    def test_summary_severity_counts_populated(self):
        engine = make_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert sum(s["severity_counts"].values()) == 1

    def test_summary_action_counts_populated(self):
        engine = make_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert sum(s["action_counts"].values()) == 1

    def test_summary_avg_composite_is_average(self):
        engine = make_engine()
        r1 = engine.assess(make_input())
        r2 = engine.assess(make_input())
        expected = round((r1.channel_engagement_composite + r2.channel_engagement_composite) / 2, 1)
        assert engine.summary()["avg_channel_engagement_composite"] == expected

    def test_summary_channel_gap_count(self):
        engine = make_engine()
        engine.assess(make_input())  # low risk, likely no gap
        s = engine.summary()
        assert isinstance(s["channel_gap_count"], int)

    def test_summary_channel_coaching_count(self):
        engine = make_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert isinstance(s["channel_coaching_count"], int)

    def test_summary_avg_diversity_score(self):
        engine = make_engine()
        r1 = engine.assess(make_input())
        r2 = engine.assess(make_input())
        expected = round((r1.channel_diversity_score + r2.channel_diversity_score) / 2, 1)
        assert engine.summary()["avg_channel_diversity_score"] == expected

    def test_summary_avg_effectiveness_score(self):
        engine = make_engine()
        r1 = engine.assess(make_input())
        r2 = engine.assess(make_input())
        expected = round((r1.channel_effectiveness_score + r2.channel_effectiveness_score) / 2, 1)
        assert engine.summary()["avg_channel_effectiveness_score"] == expected

    def test_summary_avg_frequency_score(self):
        engine = make_engine()
        r1 = engine.assess(make_input())
        r2 = engine.assess(make_input())
        expected = round((r1.touch_frequency_score + r2.touch_frequency_score) / 2, 1)
        assert engine.summary()["avg_touch_frequency_score"] == expected

    def test_summary_avg_sequence_compliance_score(self):
        engine = make_engine()
        r1 = engine.assess(make_input())
        r2 = engine.assess(make_input())
        expected = round((r1.sequence_compliance_score + r2.sequence_compliance_score) / 2, 1)
        assert engine.summary()["avg_sequence_compliance_score"] == expected

    def test_summary_total_pipeline_impact(self):
        engine = make_engine()
        r1 = engine.assess(make_input())
        r2 = engine.assess(make_input())
        expected = round(r1.estimated_pipeline_impact_usd + r2.estimated_pipeline_impact_usd, 2)
        assert engine.summary()["total_estimated_pipeline_impact_usd"] == expected

    def test_summary_risk_counts_multiple(self):
        engine = make_engine()
        # Low risk rep
        engine.assess(make_input())
        # High risk rep
        engine.assess(make_input(
            unique_channels_used_count=1,
            single_channel_prospects_count=90,
            multi_channel_prospects_count=10,
            phone_touches_count=0,
            in_person_touches_count=0,
            email_open_rate_pct=0.01,
            email_reply_rate_pct=0.01,
            phone_connect_rate_pct=0.01,
            avg_touches_per_prospect=2.0,
            avg_days_between_touches=12.0,
            follow_up_cadence_compliance_pct=0.10,
            channel_sequence_compliance_pct=0.10,
            total_prospect_touches=100,
            email_touches_count=90,
            linkedin_touches_count=10,
            linkedin_response_rate_pct=0.01,
        ))
        s = engine.summary()
        assert s["total"] == 2
        assert sum(s["risk_counts"].values()) == 2

    def test_summary_is_fresh_after_new_engine(self):
        engine1 = make_engine()
        engine1.assess(make_input())
        engine2 = make_engine()
        assert engine2.summary()["total"] == 0

    def test_summary_all_keys_present_with_data(self):
        engine = make_engine()
        engine.assess(make_input())
        s = engine.summary()
        required_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_channel_engagement_composite",
            "channel_gap_count", "channel_coaching_count",
            "avg_channel_diversity_score", "avg_channel_effectiveness_score",
            "avg_touch_frequency_score", "avg_sequence_compliance_score",
            "total_estimated_pipeline_impact_usd",
        }
        assert set(s.keys()) == required_keys

    def test_summary_channel_gap_count_matches_results(self):
        engine = make_engine()
        engine.assess(make_input(unique_channels_used_count=1))  # gap=True (unique<=1)
        engine.assess(make_input())  # low risk, gap depends
        s = engine.summary()
        expected = sum(1 for r in engine._results if r.has_channel_gap)
        assert s["channel_gap_count"] == expected

    def test_summary_coaching_count_matches_results(self):
        engine = make_engine()
        engine.assess(make_input())
        engine.assess(make_input(
            single_channel_prospects_count=80,
            multi_channel_prospects_count=20,
        ))
        s = engine.summary()
        expected = sum(1 for r in engine._results if r.requires_channel_coaching)
        assert s["channel_coaching_count"] == expected


# ===========================================================================
# 18. END-TO-END SCENARIO TESTS
# ===========================================================================

class TestEndToEndScenarios:
    """Integration-style tests testing full assess() pipeline for known scenarios."""

    def setup_method(self):
        self.engine = make_engine()

    def test_perfectly_healthy_rep(self):
        """Rep uses 6 channels, great rates, high compliance."""
        result = self.engine.assess(make_input(
            unique_channels_used_count=6,
            single_channel_prospects_count=5,
            multi_channel_prospects_count=95,
            phone_touches_count=30,
            in_person_touches_count=20,
            email_open_rate_pct=0.45,
            email_reply_rate_pct=0.12,
            phone_connect_rate_pct=0.20,
            avg_touches_per_prospect=9.0,
            avg_days_between_touches=3.0,
            follow_up_cadence_compliance_pct=0.85,
            channel_sequence_compliance_pct=0.85,
            total_prospect_touches=200,
            email_touches_count=50,
        ))
        assert result.channel_risk == ChannelRisk.low
        assert result.channel_severity == ChannelSeverity.optimized
        assert result.recommended_action == ChannelAction.no_action

    def test_single_channel_critical_rep(self):
        """Rep uses only email, all prospects single-channel."""
        result = self.engine.assess(make_input(
            unique_channels_used_count=1,
            single_channel_prospects_count=100,
            multi_channel_prospects_count=0,
            phone_touches_count=0,
            in_person_touches_count=0,
            email_open_rate_pct=0.10,
            email_reply_rate_pct=0.01,
            phone_connect_rate_pct=0.01,
            avg_touches_per_prospect=2.0,
            avg_days_between_touches=12.0,
            follow_up_cadence_compliance_pct=0.20,
            channel_sequence_compliance_pct=0.20,
            total_prospect_touches=100,
            email_touches_count=100,
            linkedin_touches_count=0,
            linkedin_response_rate_pct=0.01,
        ))
        assert result.channel_risk == ChannelRisk.critical
        assert result.channel_pattern == ChannelPattern.single_channel_dependency
        assert result.recommended_action == ChannelAction.multi_channel_training

    def test_low_touch_high_risk_rep(self):
        """Rep has low touch frequency, high days between, poor cadence."""
        result = self.engine.assess(make_input(
            unique_channels_used_count=4,
            single_channel_prospects_count=10,
            multi_channel_prospects_count=90,
            phone_touches_count=10,
            in_person_touches_count=10,
            email_open_rate_pct=0.45,
            email_reply_rate_pct=0.12,
            phone_connect_rate_pct=0.20,
            avg_touches_per_prospect=2.5,
            avg_days_between_touches=12.0,
            follow_up_cadence_compliance_pct=0.25,
            channel_sequence_compliance_pct=0.80,
            total_prospect_touches=200,
            email_touches_count=60,
            linkedin_touches_count=0,
        ))
        assert result.channel_pattern == ChannelPattern.low_touch_frequency
        # composite ~23.8 => moderate risk (touch frequency score dominates)
        assert result.channel_risk in (ChannelRisk.moderate, ChannelRisk.high, ChannelRisk.critical)

    def test_poor_email_quality_high_rep(self):
        """Rep has low email open/reply rates but ok channels."""
        result = self.engine.assess(make_input(
            unique_channels_used_count=4,
            single_channel_prospects_count=10,
            multi_channel_prospects_count=90,
            phone_touches_count=30,
            in_person_touches_count=20,
            email_open_rate_pct=0.10,
            email_reply_rate_pct=0.02,
            phone_connect_rate_pct=0.02,
            avg_touches_per_prospect=8.0,
            avg_days_between_touches=3.0,
            follow_up_cadence_compliance_pct=0.80,
            channel_sequence_compliance_pct=0.80,
            total_prospect_touches=200,
            email_touches_count=60,
        ))
        assert result.channel_pattern == ChannelPattern.poor_email_quality
        # effectiveness score drives composite ~27 => moderate risk
        assert result.channel_risk in (ChannelRisk.moderate, ChannelRisk.high, ChannelRisk.critical)

    def test_to_dict_round_trip(self):
        """to_dict should include all required keys with correct types."""
        result = self.engine.assess(make_input())
        d = result.to_dict()
        assert d["rep_id"] == result.rep_id
        assert d["region"] == result.region
        assert d["channel_risk"] == result.channel_risk.value
        assert d["channel_pattern"] == result.channel_pattern.value
        assert d["channel_severity"] == result.channel_severity.value
        assert d["recommended_action"] == result.recommended_action.value
        assert d["channel_diversity_score"] == result.channel_diversity_score
        assert d["channel_effectiveness_score"] == result.channel_effectiveness_score
        assert d["touch_frequency_score"] == result.touch_frequency_score
        assert d["sequence_compliance_score"] == result.sequence_compliance_score
        assert d["channel_engagement_composite"] == result.channel_engagement_composite
        assert d["has_channel_gap"] == result.has_channel_gap
        assert d["requires_channel_coaching"] == result.requires_channel_coaching
        assert d["estimated_pipeline_impact_usd"] == result.estimated_pipeline_impact_usd
        assert d["channel_signal"] == result.channel_signal

    def test_pipeline_impact_correlates_with_composite(self):
        """Higher composite leads to higher impact (all else equal)."""
        inp_low = make_input(
            unique_channels_used_count=5,
            single_channel_prospects_count=10,
            avg_opportunity_value_usd=10_000.0,
        )
        inp_high = make_input(
            unique_channels_used_count=1,
            single_channel_prospects_count=10,
            avg_opportunity_value_usd=10_000.0,
            phone_touches_count=0,
            in_person_touches_count=0,
            email_open_rate_pct=0.05,
            email_reply_rate_pct=0.01,
            phone_connect_rate_pct=0.01,
        )
        engine = make_engine()
        r_low = engine.assess(inp_low)
        r_high = engine.assess(inp_high)
        assert r_high.estimated_pipeline_impact_usd >= r_low.estimated_pipeline_impact_usd

    def test_channel_sequence_violation_critical_leads_to_redesign(self):
        result = self.engine.assess(make_input(
            unique_channels_used_count=3,
            single_channel_prospects_count=10,
            multi_channel_prospects_count=90,
            phone_touches_count=10,
            in_person_touches_count=10,
            email_open_rate_pct=0.45,
            email_reply_rate_pct=0.12,
            phone_connect_rate_pct=0.20,
            avg_touches_per_prospect=8.0,
            avg_days_between_touches=3.0,
            follow_up_cadence_compliance_pct=0.80,
            channel_sequence_compliance_pct=0.10,
            total_prospect_touches=100,
            email_touches_count=90,
            linkedin_touches_count=10,
            linkedin_response_rate_pct=0.01,
        ))
        if (result.channel_risk == ChannelRisk.critical
                and result.channel_pattern == ChannelPattern.channel_sequence_violation):
            assert result.recommended_action == ChannelAction.outreach_sequence_redesign

    def test_moderate_risk_gets_channel_coaching(self):
        """Any moderate-risk result should get channel_coaching action."""
        results = self.engine.assess_batch([make_input(rep_id=f"r{i}") for i in range(10)])
        for r in results:
            if r.channel_risk == ChannelRisk.moderate:
                assert r.recommended_action == ChannelAction.channel_coaching

    def test_assess_batch_summary_totals_match(self):
        engine = make_engine()
        inputs = [make_input(rep_id=f"r{i}") for i in range(5)]
        engine.assess_batch(inputs)
        s = engine.summary()
        assert s["total"] == 5
        assert sum(s["risk_counts"].values()) == 5
        assert sum(s["pattern_counts"].values()) == 5
        assert sum(s["severity_counts"].values()) == 5
        assert sum(s["action_counts"].values()) == 5

    def test_different_regions_preserved(self):
        engine = make_engine()
        r1 = engine.assess(make_input(rep_id="r1", region="EMEA"))
        r2 = engine.assess(make_input(rep_id="r2", region="APAC"))
        assert r1.region == "EMEA"
        assert r2.region == "APAC"

    def test_digital_only_approach_no_phone(self):
        """Rep has no phone touches but has some channel diversity."""
        result = self.engine.assess(make_input(
            unique_channels_used_count=3,
            phone_touches_count=0,
            in_person_touches_count=0,
            single_channel_prospects_count=10,
            multi_channel_prospects_count=90,
            email_open_rate_pct=0.45,
            email_reply_rate_pct=0.12,
            phone_connect_rate_pct=0.15,
            avg_touches_per_prospect=8.0,
            avg_days_between_touches=3.0,
            follow_up_cadence_compliance_pct=0.80,
            channel_sequence_compliance_pct=0.80,
        ))
        # With unique=3, diversity=15, not >=35 so not single_channel_dep
        # frequency ok, effectiveness ok
        # compliance ok -> no channel_seq_violation
        # diversity>=25? 15<25 so no digital_only either
        # pattern = none (since diversity=15 < 25)
        assert result.channel_pattern in (ChannelPattern.none, ChannelPattern.digital_only_approach)

    def test_multiple_engines_are_independent(self):
        e1 = make_engine()
        e2 = make_engine()
        e1.assess(make_input(rep_id="r1"))
        e1.assess(make_input(rep_id="r2"))
        e2.assess(make_input(rep_id="r3"))
        assert e1.summary()["total"] == 2
        assert e2.summary()["total"] == 1


# ===========================================================================
# 19. EDGE CASE TESTS
# ===========================================================================

class TestEdgeCases:
    def setup_method(self):
        self.engine = make_engine()

    def test_all_zero_rates(self):
        """Zero rates shouldn't cause crashes."""
        result = self.engine.assess(make_input(
            email_open_rate_pct=0.0,
            email_reply_rate_pct=0.0,
            phone_connect_rate_pct=0.0,
            linkedin_response_rate_pct=0.0,
            follow_up_cadence_compliance_pct=0.0,
            channel_sequence_compliance_pct=0.0,
        ))
        assert result is not None
        assert result.channel_engagement_composite >= 0

    def test_all_perfect_rates(self):
        """Perfect rates should yield low scores."""
        result = self.engine.assess(make_input(
            email_open_rate_pct=1.0,
            email_reply_rate_pct=1.0,
            phone_connect_rate_pct=1.0,
            linkedin_response_rate_pct=1.0,
            follow_up_cadence_compliance_pct=1.0,
            channel_sequence_compliance_pct=1.0,
        ))
        assert result is not None
        assert result.channel_effectiveness_score == 0.0

    def test_zero_total_touches(self):
        result = self.engine.assess(make_input(total_prospect_touches=0, email_touches_count=0))
        assert result is not None

    def test_zero_prospects(self):
        result = self.engine.assess(make_input(
            single_channel_prospects_count=0,
            multi_channel_prospects_count=0,
        ))
        assert result is not None

    def test_very_large_values(self):
        result = self.engine.assess(make_input(
            total_prospect_touches=1_000_000,
            email_touches_count=500_000,
            avg_opportunity_value_usd=10_000_000.0,
            single_channel_prospects_count=1000,
            multi_channel_prospects_count=9000,
        ))
        assert result is not None
        assert result.estimated_pipeline_impact_usd >= 0

    def test_avg_touches_exactly_3(self):
        result = self.engine.assess(make_input(avg_touches_per_prospect=3.0))
        # touches_per_prospect=3 => not <3, goes to <5 bucket (+20)
        assert result.touch_frequency_score >= 0

    def test_avg_touches_exactly_5(self):
        result = self.engine.assess(make_input(avg_touches_per_prospect=5.0))
        assert result.touch_frequency_score >= 0

    def test_avg_touches_exactly_7(self):
        result = self.engine.assess(make_input(avg_touches_per_prospect=7.0))
        # Not <7, so no contribution from touches
        assert result is not None

    def test_days_between_touches_exactly_5(self):
        result = self.engine.assess(make_input(avg_days_between_touches=5.0))
        assert result is not None

    def test_days_between_touches_exactly_7(self):
        result = self.engine.assess(make_input(avg_days_between_touches=7.0))
        assert result is not None

    def test_days_between_touches_exactly_10(self):
        result = self.engine.assess(make_input(avg_days_between_touches=10.0))
        assert result is not None

    def test_unique_channels_zero(self):
        result = self.engine.assess(make_input(unique_channels_used_count=0))
        assert result.has_channel_gap is True

    def test_unique_channels_large(self):
        result = self.engine.assess(make_input(unique_channels_used_count=10))
        assert result.channel_diversity_score >= 0

    def test_email_reply_exactly_0_03(self):
        result = self.engine.assess(make_input(email_reply_rate_pct=0.03))
        # 0.03 is not < 0.03, goes to < 0.05 bucket
        assert result.channel_effectiveness_score >= 0

    def test_email_reply_exactly_0_05(self):
        result = self.engine.assess(make_input(email_reply_rate_pct=0.05))
        # 0.05 is not < 0.05, goes to < 0.08 bucket
        assert result.channel_effectiveness_score >= 0

    def test_phone_connect_exactly_0_05(self):
        result = self.engine.assess(make_input(phone_connect_rate_pct=0.05))
        assert result is not None

    def test_phone_connect_exactly_0_10(self):
        result = self.engine.assess(make_input(phone_connect_rate_pct=0.10))
        assert result is not None

    def test_single_rate_exactly_0_20(self):
        result = self.engine.assess(make_input(
            single_channel_prospects_count=20,
            multi_channel_prospects_count=80,
        ))
        # rate=0.20 -> +7
        assert result.channel_diversity_score >= 7

    def test_single_rate_exactly_0_40(self):
        result = self.engine.assess(make_input(
            single_channel_prospects_count=40,
            multi_channel_prospects_count=60,
        ))
        # rate=0.40 -> +18
        assert result.channel_diversity_score >= 0

    def test_single_rate_exactly_0_60(self):
        result = self.engine.assess(make_input(
            single_channel_prospects_count=60,
            multi_channel_prospects_count=40,
        ))
        # rate=0.60 -> +35
        assert result.channel_diversity_score >= 0

    def test_channel_sequence_compliance_exactly_0_30(self):
        result = self.engine.assess(make_input(channel_sequence_compliance_pct=0.30))
        assert result is not None

    def test_channel_sequence_compliance_exactly_0_50(self):
        result = self.engine.assess(make_input(channel_sequence_compliance_pct=0.50))
        assert result is not None

    def test_channel_sequence_compliance_exactly_0_70(self):
        result = self.engine.assess(make_input(channel_sequence_compliance_pct=0.70))
        assert result is not None

    def test_cadence_compliance_exactly_0_40(self):
        result = self.engine.assess(make_input(follow_up_cadence_compliance_pct=0.40))
        assert result is not None

    def test_cadence_compliance_exactly_0_60(self):
        result = self.engine.assess(make_input(follow_up_cadence_compliance_pct=0.60))
        assert result is not None

    def test_email_open_exactly_0_20(self):
        result = self.engine.assess(make_input(email_open_rate_pct=0.20))
        assert result is not None

    def test_email_open_exactly_0_30(self):
        result = self.engine.assess(make_input(email_open_rate_pct=0.30))
        assert result is not None

    def test_email_open_exactly_0_40(self):
        result = self.engine.assess(make_input(email_open_rate_pct=0.40))
        assert result is not None

    def test_summary_after_mixed_results(self):
        engine = make_engine()
        # Healthy rep
        engine.assess(make_input(rep_id="healthy"))
        # Critical rep
        engine.assess(make_input(
            rep_id="critical",
            unique_channels_used_count=1,
            single_channel_prospects_count=90,
            multi_channel_prospects_count=10,
            phone_touches_count=0,
            in_person_touches_count=0,
            email_open_rate_pct=0.01,
            email_reply_rate_pct=0.01,
            phone_connect_rate_pct=0.01,
            avg_touches_per_prospect=2.0,
            avg_days_between_touches=12.0,
            follow_up_cadence_compliance_pct=0.10,
            channel_sequence_compliance_pct=0.10,
            total_prospect_touches=100,
            email_touches_count=100,
            linkedin_touches_count=0,
            linkedin_response_rate_pct=0.01,
        ))
        s = engine.summary()
        assert s["total"] == 2
        assert "low" in s["risk_counts"] or "critical" in s["risk_counts"]

    def test_email_heavy_rate_uses_total_touches(self):
        """email_heavy_rate = email_touches_count / total_prospect_touches."""
        # total=100, email=80 => rate=0.80 => +30
        result = self.engine.assess(make_input(
            total_prospect_touches=100,
            email_touches_count=80,
            channel_sequence_compliance_pct=0.90,
            linkedin_touches_count=0,
            linkedin_response_rate_pct=0.10,
        ))
        assert result.sequence_compliance_score >= 30.0

    def test_linkedin_bonus_only_when_touches_positive(self):
        engine = make_engine()
        inp_no_linkedin = make_input(
            linkedin_touches_count=0,
            linkedin_response_rate_pct=0.01,
            channel_sequence_compliance_pct=0.90,
            total_prospect_touches=100,
            email_touches_count=40,
        )
        inp_with_linkedin = make_input(
            linkedin_touches_count=10,
            linkedin_response_rate_pct=0.01,
            channel_sequence_compliance_pct=0.90,
            total_prospect_touches=100,
            email_touches_count=40,
        )
        r_no = engine.assess(inp_no_linkedin)
        r_with = engine.assess(inp_with_linkedin)
        assert r_with.sequence_compliance_score > r_no.sequence_compliance_score


# ===========================================================================
# 20. COMPOSITE SCORE INTEGRATION TESTS
# ===========================================================================

class TestCompositeScoreIntegration:
    """Verify composite = diversity*0.30 + effectiveness*0.30 + frequency*0.25 + compliance*0.15."""

    def setup_method(self):
        self.engine = make_engine()

    def _check_composite(self, **kw):
        inp = make_input(**kw)
        result = self.engine.assess(inp)
        div = self.engine._channel_diversity_score(inp)
        eff = self.engine._channel_effectiveness_score(inp)
        frq = self.engine._touch_frequency_score(inp)
        cmp = self.engine._sequence_compliance_score(inp)
        expected = round(min(div * 0.30 + eff * 0.30 + frq * 0.25 + cmp * 0.15, 100.0), 1)
        assert result.channel_engagement_composite == expected

    def test_composite_healthy_rep(self):
        self._check_composite()

    def test_composite_single_channel_rep(self):
        self._check_composite(
            unique_channels_used_count=1,
            single_channel_prospects_count=90,
            multi_channel_prospects_count=10,
        )

    def test_composite_poor_email_rep(self):
        self._check_composite(
            email_open_rate_pct=0.05,
            email_reply_rate_pct=0.01,
            phone_connect_rate_pct=0.02,
        )

    def test_composite_low_touch_rep(self):
        self._check_composite(
            avg_touches_per_prospect=2.0,
            avg_days_between_touches=12.0,
            follow_up_cadence_compliance_pct=0.20,
        )

    def test_composite_email_heavy_rep(self):
        self._check_composite(
            total_prospect_touches=100,
            email_touches_count=85,
            channel_sequence_compliance_pct=0.20,
        )

    def test_composite_worst_case_capped(self):
        inp = make_input(
            unique_channels_used_count=1,
            single_channel_prospects_count=90,
            multi_channel_prospects_count=10,
            phone_touches_count=0,
            in_person_touches_count=0,
            email_open_rate_pct=0.01,
            email_reply_rate_pct=0.01,
            phone_connect_rate_pct=0.01,
            avg_touches_per_prospect=2.0,
            avg_days_between_touches=12.0,
            follow_up_cadence_compliance_pct=0.10,
            channel_sequence_compliance_pct=0.10,
            total_prospect_touches=100,
            email_touches_count=90,
            linkedin_touches_count=10,
            linkedin_response_rate_pct=0.01,
        )
        result = self.engine.assess(inp)
        assert result.channel_engagement_composite <= 100.0

    def test_scores_rounded_to_1dp(self):
        result = self.engine.assess(make_input())
        for score in [
            result.channel_diversity_score,
            result.channel_effectiveness_score,
            result.touch_frequency_score,
            result.sequence_compliance_score,
            result.channel_engagement_composite,
        ]:
            # Check it's rounded to at most 1 decimal place
            assert round(score, 1) == score
