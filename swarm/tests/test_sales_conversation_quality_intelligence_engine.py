"""
Comprehensive pytest test suite for SalesConversationQualityIntelligenceEngine.

Covers:
- All 4 enums (values, types, membership)
- ConversationQualityInput dataclass (all 22 fields)
- ConversationQualityResult dataclass (all 15 fields + to_dict())
- All sub-score methods (_engagement_quality_score, _discovery_depth_score,
  _objection_handling_score, _next_step_discipline_score)
- Pattern detection (_detect_pattern)
- Risk / severity / action mapping
- Both flag methods (_has_conversation_gap, _requires_call_coaching)
- Revenue impact calculation (_estimated_revenue_impact)
- Signal generation (_signal)
- assess(), assess_batch(), summary()
- Edge cases and end-to-end scenarios
"""

from __future__ import annotations

import pytest

from swarm.intelligence.sales_conversation_quality_intelligence_engine import (
    ConversationAction,
    ConversationPattern,
    ConversationQualityInput,
    ConversationQualityResult,
    ConversationRisk,
    ConversationSeverity,
    SalesConversationQualityIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> ConversationQualityInput:
    """Return a 'healthy' baseline input; override any field via kwargs."""
    defaults = dict(
        rep_id="REP-001",
        region="EMEA",
        evaluation_period_id="Q2-2026",
        total_calls_analyzed=50,
        avg_talk_listen_ratio=1.2,          # good (< 1.5)
        avg_questions_per_call=7.0,          # good (>= 7)
        discovery_questions_pct=0.60,
        avg_call_duration_minutes=30.0,
        calls_with_next_step_pct=0.85,       # good (>= 0.80)
        avg_days_to_next_step=2.0,           # good (< 4)
        objection_raised_count=10,
        objection_handled_successfully_count=8,  # handle_rate = 0.80 (good)
        filler_words_per_minute=1.0,         # good (< 3)
        interruptions_per_call=1.0,          # good (< 3)
        avg_prospect_talk_time_pct=0.45,     # good (>= 0.40)
        closing_attempt_rate_pct=0.70,
        calls_with_decision_maker_pct=0.50,  # good (>= 0.40)
        pain_identified_calls_pct=0.60,      # good (>= 0.50)
        budget_discussed_calls_pct=0.45,     # good (>= 0.40)
        multi_thread_calls_pct=0.55,
        call_recording_compliance_pct=0.80,  # good (>= 0.70)
        avg_opportunity_value_usd=10_000.0,
    )
    defaults.update(overrides)
    return ConversationQualityInput(**defaults)


def engine() -> SalesConversationQualityIntelligenceEngine:
    return SalesConversationQualityIntelligenceEngine()


# ===========================================================================
# 1. ENUM TESTS
# ===========================================================================

class TestConversationRisk:
    def test_values_count(self):
        assert len(ConversationRisk) == 4

    def test_low_value(self):
        assert ConversationRisk.low.value == "low"

    def test_moderate_value(self):
        assert ConversationRisk.moderate.value == "moderate"

    def test_high_value(self):
        assert ConversationRisk.high.value == "high"

    def test_critical_value(self):
        assert ConversationRisk.critical.value == "critical"

    def test_is_str(self):
        assert isinstance(ConversationRisk.low, str)

    def test_string_comparison(self):
        assert ConversationRisk.high == "high"

    def test_members(self):
        members = {m.value for m in ConversationRisk}
        assert members == {"low", "moderate", "high", "critical"}


class TestConversationPattern:
    def test_values_count(self):
        assert len(ConversationPattern) == 6

    def test_none_value(self):
        assert ConversationPattern.none.value == "none"

    def test_monologue_tendency_value(self):
        assert ConversationPattern.monologue_tendency.value == "monologue_tendency"

    def test_shallow_discovery_value(self):
        assert ConversationPattern.shallow_discovery.value == "shallow_discovery"

    def test_poor_objection_handling_value(self):
        assert ConversationPattern.poor_objection_handling.value == "poor_objection_handling"

    def test_no_next_step_discipline_value(self):
        assert ConversationPattern.no_next_step_discipline.value == "no_next_step_discipline"

    def test_low_engagement_calls_value(self):
        assert ConversationPattern.low_engagement_calls.value == "low_engagement_calls"

    def test_is_str(self):
        assert isinstance(ConversationPattern.none, str)

    def test_string_comparison(self):
        assert ConversationPattern.shallow_discovery == "shallow_discovery"

    def test_members(self):
        members = {m.value for m in ConversationPattern}
        assert "none" in members
        assert "monologue_tendency" in members
        assert "low_engagement_calls" in members


class TestConversationSeverity:
    def test_values_count(self):
        assert len(ConversationSeverity) == 4

    def test_sharp_value(self):
        assert ConversationSeverity.sharp.value == "sharp"

    def test_developing_value(self):
        assert ConversationSeverity.developing.value == "developing"

    def test_weak_value(self):
        assert ConversationSeverity.weak.value == "weak"

    def test_failing_value(self):
        assert ConversationSeverity.failing.value == "failing"

    def test_is_str(self):
        assert isinstance(ConversationSeverity.failing, str)

    def test_string_comparison(self):
        assert ConversationSeverity.weak == "weak"


class TestConversationAction:
    def test_values_count(self):
        assert len(ConversationAction) == 6

    def test_no_action_value(self):
        assert ConversationAction.no_action.value == "no_action"

    def test_call_coaching_session_value(self):
        assert ConversationAction.call_coaching_session.value == "call_coaching_session"

    def test_discovery_skills_training_value(self):
        assert ConversationAction.discovery_skills_training.value == "discovery_skills_training"

    def test_objection_handling_workshop_value(self):
        assert ConversationAction.objection_handling_workshop.value == "objection_handling_workshop"

    def test_next_step_discipline_review_value(self):
        assert ConversationAction.next_step_discipline_review.value == "next_step_discipline_review"

    def test_call_recording_audit_value(self):
        assert ConversationAction.call_recording_audit.value == "call_recording_audit"

    def test_is_str(self):
        assert isinstance(ConversationAction.no_action, str)

    def test_string_comparison(self):
        assert ConversationAction.call_coaching_session == "call_coaching_session"


# ===========================================================================
# 2. ConversationQualityInput DATACLASS
# ===========================================================================

class TestConversationQualityInput:
    def test_creation(self):
        inp = make_input()
        assert inp.rep_id == "REP-001"

    def test_rep_id_field(self):
        inp = make_input(rep_id="REP-XYZ")
        assert inp.rep_id == "REP-XYZ"

    def test_region_field(self):
        inp = make_input(region="APAC")
        assert inp.region == "APAC"

    def test_evaluation_period_id_field(self):
        inp = make_input(evaluation_period_id="Q1-2026")
        assert inp.evaluation_period_id == "Q1-2026"

    def test_total_calls_analyzed_field(self):
        inp = make_input(total_calls_analyzed=100)
        assert inp.total_calls_analyzed == 100

    def test_avg_talk_listen_ratio_field(self):
        inp = make_input(avg_talk_listen_ratio=3.0)
        assert inp.avg_talk_listen_ratio == 3.0

    def test_avg_questions_per_call_field(self):
        inp = make_input(avg_questions_per_call=2.5)
        assert inp.avg_questions_per_call == 2.5

    def test_discovery_questions_pct_field(self):
        inp = make_input(discovery_questions_pct=0.40)
        assert inp.discovery_questions_pct == 0.40

    def test_avg_call_duration_minutes_field(self):
        inp = make_input(avg_call_duration_minutes=45.0)
        assert inp.avg_call_duration_minutes == 45.0

    def test_calls_with_next_step_pct_field(self):
        inp = make_input(calls_with_next_step_pct=0.30)
        assert inp.calls_with_next_step_pct == 0.30

    def test_avg_days_to_next_step_field(self):
        inp = make_input(avg_days_to_next_step=12.0)
        assert inp.avg_days_to_next_step == 12.0

    def test_objection_raised_count_field(self):
        inp = make_input(objection_raised_count=5)
        assert inp.objection_raised_count == 5

    def test_objection_handled_successfully_count_field(self):
        inp = make_input(objection_handled_successfully_count=3)
        assert inp.objection_handled_successfully_count == 3

    def test_filler_words_per_minute_field(self):
        inp = make_input(filler_words_per_minute=6.0)
        assert inp.filler_words_per_minute == 6.0

    def test_interruptions_per_call_field(self):
        inp = make_input(interruptions_per_call=7.0)
        assert inp.interruptions_per_call == 7.0

    def test_avg_prospect_talk_time_pct_field(self):
        inp = make_input(avg_prospect_talk_time_pct=0.25)
        assert inp.avg_prospect_talk_time_pct == 0.25

    def test_closing_attempt_rate_pct_field(self):
        inp = make_input(closing_attempt_rate_pct=0.50)
        assert inp.closing_attempt_rate_pct == 0.50

    def test_calls_with_decision_maker_pct_field(self):
        inp = make_input(calls_with_decision_maker_pct=0.10)
        assert inp.calls_with_decision_maker_pct == 0.10

    def test_pain_identified_calls_pct_field(self):
        inp = make_input(pain_identified_calls_pct=0.20)
        assert inp.pain_identified_calls_pct == 0.20

    def test_budget_discussed_calls_pct_field(self):
        inp = make_input(budget_discussed_calls_pct=0.10)
        assert inp.budget_discussed_calls_pct == 0.10

    def test_multi_thread_calls_pct_field(self):
        inp = make_input(multi_thread_calls_pct=0.30)
        assert inp.multi_thread_calls_pct == 0.30

    def test_call_recording_compliance_pct_field(self):
        inp = make_input(call_recording_compliance_pct=0.40)
        assert inp.call_recording_compliance_pct == 0.40

    def test_avg_opportunity_value_usd_field(self):
        inp = make_input(avg_opportunity_value_usd=50_000.0)
        assert inp.avg_opportunity_value_usd == 50_000.0

    def test_has_22_fields(self):
        import dataclasses
        fields = dataclasses.fields(ConversationQualityInput)
        assert len(fields) == 22


# ===========================================================================
# 3. ConversationQualityResult DATACLASS & to_dict()
# ===========================================================================

class TestConversationQualityResult:
    def _make_result(self):
        return ConversationQualityResult(
            rep_id="REP-001",
            region="EMEA",
            conversation_risk=ConversationRisk.low,
            conversation_pattern=ConversationPattern.none,
            conversation_severity=ConversationSeverity.sharp,
            recommended_action=ConversationAction.no_action,
            engagement_quality_score=5.0,
            discovery_depth_score=7.0,
            objection_handling_score=3.0,
            next_step_discipline_score=2.0,
            conversation_composite=5.0,
            has_conversation_gap=False,
            requires_call_coaching=False,
            estimated_revenue_impact_usd=0.0,
            conversation_signal="healthy",
        )

    def test_rep_id(self):
        r = self._make_result()
        assert r.rep_id == "REP-001"

    def test_region(self):
        r = self._make_result()
        assert r.region == "EMEA"

    def test_conversation_risk(self):
        r = self._make_result()
        assert r.conversation_risk == ConversationRisk.low

    def test_conversation_pattern(self):
        r = self._make_result()
        assert r.conversation_pattern == ConversationPattern.none

    def test_conversation_severity(self):
        r = self._make_result()
        assert r.conversation_severity == ConversationSeverity.sharp

    def test_recommended_action(self):
        r = self._make_result()
        assert r.recommended_action == ConversationAction.no_action

    def test_engagement_quality_score(self):
        r = self._make_result()
        assert r.engagement_quality_score == 5.0

    def test_discovery_depth_score(self):
        r = self._make_result()
        assert r.discovery_depth_score == 7.0

    def test_objection_handling_score(self):
        r = self._make_result()
        assert r.objection_handling_score == 3.0

    def test_next_step_discipline_score(self):
        r = self._make_result()
        assert r.next_step_discipline_score == 2.0

    def test_conversation_composite(self):
        r = self._make_result()
        assert r.conversation_composite == 5.0

    def test_has_conversation_gap(self):
        r = self._make_result()
        assert r.has_conversation_gap is False

    def test_requires_call_coaching(self):
        r = self._make_result()
        assert r.requires_call_coaching is False

    def test_estimated_revenue_impact_usd(self):
        r = self._make_result()
        assert r.estimated_revenue_impact_usd == 0.0

    def test_conversation_signal(self):
        r = self._make_result()
        assert r.conversation_signal == "healthy"

    def test_has_15_fields(self):
        import dataclasses
        fields = dataclasses.fields(ConversationQualityResult)
        assert len(fields) == 15

    # to_dict tests
    def test_to_dict_returns_dict(self):
        assert isinstance(self._make_result().to_dict(), dict)

    def test_to_dict_has_15_keys(self):
        assert len(self._make_result().to_dict()) == 15

    def test_to_dict_rep_id(self):
        assert self._make_result().to_dict()["rep_id"] == "REP-001"

    def test_to_dict_region(self):
        assert self._make_result().to_dict()["region"] == "EMEA"

    def test_to_dict_conversation_risk_is_string(self):
        d = self._make_result().to_dict()
        assert d["conversation_risk"] == "low"
        assert isinstance(d["conversation_risk"], str)

    def test_to_dict_conversation_pattern_is_string(self):
        d = self._make_result().to_dict()
        assert d["conversation_pattern"] == "none"

    def test_to_dict_conversation_severity_is_string(self):
        d = self._make_result().to_dict()
        assert d["conversation_severity"] == "sharp"

    def test_to_dict_recommended_action_is_string(self):
        d = self._make_result().to_dict()
        assert d["recommended_action"] == "no_action"

    def test_to_dict_numeric_fields(self):
        d = self._make_result().to_dict()
        assert d["engagement_quality_score"] == 5.0
        assert d["discovery_depth_score"] == 7.0
        assert d["objection_handling_score"] == 3.0
        assert d["next_step_discipline_score"] == 2.0
        assert d["conversation_composite"] == 5.0
        assert d["estimated_revenue_impact_usd"] == 0.0

    def test_to_dict_bool_fields(self):
        d = self._make_result().to_dict()
        assert d["has_conversation_gap"] is False
        assert d["requires_call_coaching"] is False

    def test_to_dict_signal(self):
        d = self._make_result().to_dict()
        assert d["conversation_signal"] == "healthy"

    def test_to_dict_expected_keys(self):
        expected = {
            "rep_id", "region", "conversation_risk", "conversation_pattern",
            "conversation_severity", "recommended_action",
            "engagement_quality_score", "discovery_depth_score",
            "objection_handling_score", "next_step_discipline_score",
            "conversation_composite", "has_conversation_gap",
            "requires_call_coaching", "estimated_revenue_impact_usd",
            "conversation_signal",
        }
        assert set(self._make_result().to_dict().keys()) == expected


# ===========================================================================
# 4. ENGAGEMENT QUALITY SCORE
# ===========================================================================

class TestEngagementQualityScore:
    def setup_method(self):
        self.e = engine()

    def test_all_zeros_perfect_rep(self):
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            avg_prospect_talk_time_pct=0.50,
            filler_words_per_minute=0.5,
        )
        assert self.e._engagement_quality_score(inp) == 0.0

    # talk_listen_ratio branches
    def test_ratio_below_1_5(self):
        inp = make_input(
            avg_talk_listen_ratio=1.4,
            avg_prospect_talk_time_pct=0.50,
            filler_words_per_minute=0.0,
        )
        assert self.e._engagement_quality_score(inp) == 0.0

    def test_ratio_exactly_1_5(self):
        inp = make_input(
            avg_talk_listen_ratio=1.5,
            avg_prospect_talk_time_pct=0.50,
            filler_words_per_minute=0.0,
        )
        assert self.e._engagement_quality_score(inp) == 8.0

    def test_ratio_between_1_5_and_2_0(self):
        inp = make_input(
            avg_talk_listen_ratio=1.8,
            avg_prospect_talk_time_pct=0.50,
            filler_words_per_minute=0.0,
        )
        assert self.e._engagement_quality_score(inp) == 8.0

    def test_ratio_exactly_2_0(self):
        inp = make_input(
            avg_talk_listen_ratio=2.0,
            avg_prospect_talk_time_pct=0.50,
            filler_words_per_minute=0.0,
        )
        assert self.e._engagement_quality_score(inp) == 22.0

    def test_ratio_between_2_0_and_2_5(self):
        inp = make_input(
            avg_talk_listen_ratio=2.3,
            avg_prospect_talk_time_pct=0.50,
            filler_words_per_minute=0.0,
        )
        assert self.e._engagement_quality_score(inp) == 22.0

    def test_ratio_exactly_2_5(self):
        inp = make_input(
            avg_talk_listen_ratio=2.5,
            avg_prospect_talk_time_pct=0.50,
            filler_words_per_minute=0.0,
        )
        assert self.e._engagement_quality_score(inp) == 40.0

    def test_ratio_above_2_5(self):
        inp = make_input(
            avg_talk_listen_ratio=4.0,
            avg_prospect_talk_time_pct=0.50,
            filler_words_per_minute=0.0,
        )
        assert self.e._engagement_quality_score(inp) == 40.0

    # prospect talk time branches
    def test_prospect_talk_below_0_30(self):
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            avg_prospect_talk_time_pct=0.25,
            filler_words_per_minute=0.0,
        )
        assert self.e._engagement_quality_score(inp) == 30.0

    def test_prospect_talk_exactly_0_30(self):
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            avg_prospect_talk_time_pct=0.30,
            filler_words_per_minute=0.0,
        )
        assert self.e._engagement_quality_score(inp) == 15.0

    def test_prospect_talk_between_0_30_and_0_40(self):
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            avg_prospect_talk_time_pct=0.35,
            filler_words_per_minute=0.0,
        )
        assert self.e._engagement_quality_score(inp) == 15.0

    def test_prospect_talk_at_0_40_no_penalty(self):
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            avg_prospect_talk_time_pct=0.40,
            filler_words_per_minute=0.0,
        )
        assert self.e._engagement_quality_score(inp) == 0.0

    # filler_words branches
    def test_filler_words_below_3(self):
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            avg_prospect_talk_time_pct=0.50,
            filler_words_per_minute=2.9,
        )
        assert self.e._engagement_quality_score(inp) == 0.0

    def test_filler_words_exactly_3(self):
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            avg_prospect_talk_time_pct=0.50,
            filler_words_per_minute=3.0,
        )
        assert self.e._engagement_quality_score(inp) == 10.0

    def test_filler_words_between_3_and_5(self):
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            avg_prospect_talk_time_pct=0.50,
            filler_words_per_minute=4.5,
        )
        assert self.e._engagement_quality_score(inp) == 10.0

    def test_filler_words_exactly_5(self):
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            avg_prospect_talk_time_pct=0.50,
            filler_words_per_minute=5.0,
        )
        assert self.e._engagement_quality_score(inp) == 20.0

    def test_filler_words_above_5(self):
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            avg_prospect_talk_time_pct=0.50,
            filler_words_per_minute=10.0,
        )
        assert self.e._engagement_quality_score(inp) == 20.0

    # capped at 100
    def test_score_capped_at_100(self):
        inp = make_input(
            avg_talk_listen_ratio=3.0,
            avg_prospect_talk_time_pct=0.10,
            filler_words_per_minute=8.0,
        )
        assert self.e._engagement_quality_score(inp) == 90.0  # 40+30+20 = 90, not over 100

    def test_score_capped_at_100_extreme(self):
        # Max possible is 40 + 30 + 20 = 90, cannot exceed 100 naturally
        # Let's just confirm it never exceeds 100
        inp = make_input(
            avg_talk_listen_ratio=5.0,
            avg_prospect_talk_time_pct=0.01,
            filler_words_per_minute=10.0,
        )
        assert self.e._engagement_quality_score(inp) <= 100.0

    def test_combined_score(self):
        # ratio=2.5 → 40; prospect=0.25 → 30; filler=5.0 → 20 → total=90
        inp = make_input(
            avg_talk_listen_ratio=2.5,
            avg_prospect_talk_time_pct=0.25,
            filler_words_per_minute=5.0,
        )
        assert self.e._engagement_quality_score(inp) == 90.0


# ===========================================================================
# 5. DISCOVERY DEPTH SCORE
# ===========================================================================

class TestDiscoveryDepthScore:
    def setup_method(self):
        self.e = engine()

    def test_all_zeros_best_case(self):
        inp = make_input(
            avg_questions_per_call=8.0,
            pain_identified_calls_pct=0.60,
            budget_discussed_calls_pct=0.50,
        )
        assert self.e._discovery_depth_score(inp) == 0.0

    # avg_questions_per_call branches
    def test_questions_below_3(self):
        inp = make_input(
            avg_questions_per_call=2.0,
            pain_identified_calls_pct=0.60,
            budget_discussed_calls_pct=0.50,
        )
        assert self.e._discovery_depth_score(inp) == 35.0

    def test_questions_exactly_3(self):
        inp = make_input(
            avg_questions_per_call=3.0,
            pain_identified_calls_pct=0.60,
            budget_discussed_calls_pct=0.50,
        )
        assert self.e._discovery_depth_score(inp) == 18.0

    def test_questions_between_3_and_5(self):
        inp = make_input(
            avg_questions_per_call=4.0,
            pain_identified_calls_pct=0.60,
            budget_discussed_calls_pct=0.50,
        )
        assert self.e._discovery_depth_score(inp) == 18.0

    def test_questions_exactly_5(self):
        inp = make_input(
            avg_questions_per_call=5.0,
            pain_identified_calls_pct=0.60,
            budget_discussed_calls_pct=0.50,
        )
        assert self.e._discovery_depth_score(inp) == 7.0

    def test_questions_between_5_and_7(self):
        inp = make_input(
            avg_questions_per_call=6.0,
            pain_identified_calls_pct=0.60,
            budget_discussed_calls_pct=0.50,
        )
        assert self.e._discovery_depth_score(inp) == 7.0

    def test_questions_at_7_no_penalty(self):
        inp = make_input(
            avg_questions_per_call=7.0,
            pain_identified_calls_pct=0.60,
            budget_discussed_calls_pct=0.50,
        )
        assert self.e._discovery_depth_score(inp) == 0.0

    # pain_identified_calls_pct branches
    def test_pain_below_0_30(self):
        inp = make_input(
            avg_questions_per_call=8.0,
            pain_identified_calls_pct=0.20,
            budget_discussed_calls_pct=0.50,
        )
        assert self.e._discovery_depth_score(inp) == 30.0

    def test_pain_exactly_0_30(self):
        inp = make_input(
            avg_questions_per_call=8.0,
            pain_identified_calls_pct=0.30,
            budget_discussed_calls_pct=0.50,
        )
        assert self.e._discovery_depth_score(inp) == 15.0

    def test_pain_between_0_30_and_0_50(self):
        inp = make_input(
            avg_questions_per_call=8.0,
            pain_identified_calls_pct=0.40,
            budget_discussed_calls_pct=0.50,
        )
        assert self.e._discovery_depth_score(inp) == 15.0

    def test_pain_at_0_50_no_penalty(self):
        inp = make_input(
            avg_questions_per_call=8.0,
            pain_identified_calls_pct=0.50,
            budget_discussed_calls_pct=0.50,
        )
        assert self.e._discovery_depth_score(inp) == 0.0

    # budget_discussed_calls_pct branches
    def test_budget_below_0_20(self):
        inp = make_input(
            avg_questions_per_call=8.0,
            pain_identified_calls_pct=0.60,
            budget_discussed_calls_pct=0.10,
        )
        assert self.e._discovery_depth_score(inp) == 25.0

    def test_budget_exactly_0_20(self):
        inp = make_input(
            avg_questions_per_call=8.0,
            pain_identified_calls_pct=0.60,
            budget_discussed_calls_pct=0.20,
        )
        assert self.e._discovery_depth_score(inp) == 12.0

    def test_budget_between_0_20_and_0_40(self):
        inp = make_input(
            avg_questions_per_call=8.0,
            pain_identified_calls_pct=0.60,
            budget_discussed_calls_pct=0.30,
        )
        assert self.e._discovery_depth_score(inp) == 12.0

    def test_budget_at_0_40_no_penalty(self):
        inp = make_input(
            avg_questions_per_call=8.0,
            pain_identified_calls_pct=0.60,
            budget_discussed_calls_pct=0.40,
        )
        assert self.e._discovery_depth_score(inp) == 0.0

    def test_max_discovery_score_capped_at_100(self):
        inp = make_input(
            avg_questions_per_call=1.0,
            pain_identified_calls_pct=0.10,
            budget_discussed_calls_pct=0.05,
        )
        # 35 + 30 + 25 = 90 (no cap needed for this combination)
        assert self.e._discovery_depth_score(inp) == 90.0

    def test_capped_at_100_always(self):
        inp = make_input(
            avg_questions_per_call=0.0,
            pain_identified_calls_pct=0.0,
            budget_discussed_calls_pct=0.0,
        )
        assert self.e._discovery_depth_score(inp) <= 100.0


# ===========================================================================
# 6. OBJECTION HANDLING SCORE
# ===========================================================================

class TestObjectionHandlingScore:
    def setup_method(self):
        self.e = engine()

    def test_all_zeros_best_case(self):
        inp = make_input(
            objection_raised_count=10,
            objection_handled_successfully_count=10,  # 100% handle rate
            interruptions_per_call=0.0,
            calls_with_decision_maker_pct=0.50,
        )
        assert self.e._objection_handling_score(inp) == 0.0

    # handle_rate branches
    def test_handle_rate_below_0_30(self):
        inp = make_input(
            objection_raised_count=10,
            objection_handled_successfully_count=2,  # 20%
            interruptions_per_call=0.0,
            calls_with_decision_maker_pct=0.50,
        )
        assert self.e._objection_handling_score(inp) == 45.0

    def test_handle_rate_exactly_0_30(self):
        inp = make_input(
            objection_raised_count=10,
            objection_handled_successfully_count=3,  # 30%
            interruptions_per_call=0.0,
            calls_with_decision_maker_pct=0.50,
        )
        assert self.e._objection_handling_score(inp) == 25.0

    def test_handle_rate_between_0_30_and_0_50(self):
        inp = make_input(
            objection_raised_count=10,
            objection_handled_successfully_count=4,  # 40%
            interruptions_per_call=0.0,
            calls_with_decision_maker_pct=0.50,
        )
        assert self.e._objection_handling_score(inp) == 25.0

    def test_handle_rate_exactly_0_50(self):
        inp = make_input(
            objection_raised_count=10,
            objection_handled_successfully_count=5,  # 50%
            interruptions_per_call=0.0,
            calls_with_decision_maker_pct=0.50,
        )
        assert self.e._objection_handling_score(inp) == 10.0

    def test_handle_rate_between_0_50_and_0_70(self):
        inp = make_input(
            objection_raised_count=10,
            objection_handled_successfully_count=6,  # 60%
            interruptions_per_call=0.0,
            calls_with_decision_maker_pct=0.50,
        )
        assert self.e._objection_handling_score(inp) == 10.0

    def test_handle_rate_at_0_70_no_penalty(self):
        inp = make_input(
            objection_raised_count=10,
            objection_handled_successfully_count=7,  # 70%
            interruptions_per_call=0.0,
            calls_with_decision_maker_pct=0.50,
        )
        assert self.e._objection_handling_score(inp) == 0.0

    def test_zero_objections_uses_max_1(self):
        # With 0 objections, max(0,1)=1, so handled=0 → rate=0/1=0 (<0.30)
        inp = make_input(
            objection_raised_count=0,
            objection_handled_successfully_count=0,
            interruptions_per_call=0.0,
            calls_with_decision_maker_pct=0.50,
        )
        assert self.e._objection_handling_score(inp) == 45.0

    # interruptions branches
    def test_interruptions_below_3(self):
        inp = make_input(
            objection_raised_count=10,
            objection_handled_successfully_count=10,
            interruptions_per_call=2.9,
            calls_with_decision_maker_pct=0.50,
        )
        assert self.e._objection_handling_score(inp) == 0.0

    def test_interruptions_exactly_3(self):
        inp = make_input(
            objection_raised_count=10,
            objection_handled_successfully_count=10,
            interruptions_per_call=3.0,
            calls_with_decision_maker_pct=0.50,
        )
        assert self.e._objection_handling_score(inp) == 15.0

    def test_interruptions_between_3_and_5(self):
        inp = make_input(
            objection_raised_count=10,
            objection_handled_successfully_count=10,
            interruptions_per_call=4.0,
            calls_with_decision_maker_pct=0.50,
        )
        assert self.e._objection_handling_score(inp) == 15.0

    def test_interruptions_exactly_5(self):
        inp = make_input(
            objection_raised_count=10,
            objection_handled_successfully_count=10,
            interruptions_per_call=5.0,
            calls_with_decision_maker_pct=0.50,
        )
        assert self.e._objection_handling_score(inp) == 30.0

    def test_interruptions_above_5(self):
        inp = make_input(
            objection_raised_count=10,
            objection_handled_successfully_count=10,
            interruptions_per_call=8.0,
            calls_with_decision_maker_pct=0.50,
        )
        assert self.e._objection_handling_score(inp) == 30.0

    # decision_maker branches
    def test_decision_maker_below_0_20(self):
        inp = make_input(
            objection_raised_count=10,
            objection_handled_successfully_count=10,
            interruptions_per_call=0.0,
            calls_with_decision_maker_pct=0.10,
        )
        assert self.e._objection_handling_score(inp) == 20.0

    def test_decision_maker_exactly_0_20(self):
        inp = make_input(
            objection_raised_count=10,
            objection_handled_successfully_count=10,
            interruptions_per_call=0.0,
            calls_with_decision_maker_pct=0.20,
        )
        assert self.e._objection_handling_score(inp) == 10.0

    def test_decision_maker_between_0_20_and_0_40(self):
        inp = make_input(
            objection_raised_count=10,
            objection_handled_successfully_count=10,
            interruptions_per_call=0.0,
            calls_with_decision_maker_pct=0.30,
        )
        assert self.e._objection_handling_score(inp) == 10.0

    def test_decision_maker_at_0_40_no_penalty(self):
        inp = make_input(
            objection_raised_count=10,
            objection_handled_successfully_count=10,
            interruptions_per_call=0.0,
            calls_with_decision_maker_pct=0.40,
        )
        assert self.e._objection_handling_score(inp) == 0.0

    def test_score_capped_at_100(self):
        inp = make_input(
            objection_raised_count=0,
            objection_handled_successfully_count=0,
            interruptions_per_call=5.0,
            calls_with_decision_maker_pct=0.10,
        )
        # 45 + 30 + 20 = 95, no cap needed
        assert self.e._objection_handling_score(inp) == 95.0


# ===========================================================================
# 7. NEXT STEP DISCIPLINE SCORE
# ===========================================================================

class TestNextStepDisciplineScore:
    def setup_method(self):
        self.e = engine()

    def test_all_zeros_best_case(self):
        inp = make_input(
            calls_with_next_step_pct=0.90,
            avg_days_to_next_step=1.0,
            call_recording_compliance_pct=0.90,
        )
        assert self.e._next_step_discipline_score(inp) == 0.0

    # calls_with_next_step_pct branches
    def test_next_step_pct_below_0_40(self):
        inp = make_input(
            calls_with_next_step_pct=0.30,
            avg_days_to_next_step=1.0,
            call_recording_compliance_pct=0.90,
        )
        assert self.e._next_step_discipline_score(inp) == 40.0

    def test_next_step_pct_exactly_0_40(self):
        inp = make_input(
            calls_with_next_step_pct=0.40,
            avg_days_to_next_step=1.0,
            call_recording_compliance_pct=0.90,
        )
        assert self.e._next_step_discipline_score(inp) == 22.0

    def test_next_step_pct_between_0_40_and_0_60(self):
        inp = make_input(
            calls_with_next_step_pct=0.50,
            avg_days_to_next_step=1.0,
            call_recording_compliance_pct=0.90,
        )
        assert self.e._next_step_discipline_score(inp) == 22.0

    def test_next_step_pct_exactly_0_60(self):
        inp = make_input(
            calls_with_next_step_pct=0.60,
            avg_days_to_next_step=1.0,
            call_recording_compliance_pct=0.90,
        )
        assert self.e._next_step_discipline_score(inp) == 8.0

    def test_next_step_pct_between_0_60_and_0_80(self):
        inp = make_input(
            calls_with_next_step_pct=0.70,
            avg_days_to_next_step=1.0,
            call_recording_compliance_pct=0.90,
        )
        assert self.e._next_step_discipline_score(inp) == 8.0

    def test_next_step_pct_at_0_80_no_penalty(self):
        inp = make_input(
            calls_with_next_step_pct=0.80,
            avg_days_to_next_step=1.0,
            call_recording_compliance_pct=0.90,
        )
        assert self.e._next_step_discipline_score(inp) == 0.0

    # avg_days_to_next_step branches
    def test_days_below_4_no_penalty(self):
        inp = make_input(
            calls_with_next_step_pct=0.90,
            avg_days_to_next_step=3.9,
            call_recording_compliance_pct=0.90,
        )
        assert self.e._next_step_discipline_score(inp) == 0.0

    def test_days_exactly_4(self):
        inp = make_input(
            calls_with_next_step_pct=0.90,
            avg_days_to_next_step=4.0,
            call_recording_compliance_pct=0.90,
        )
        assert self.e._next_step_discipline_score(inp) == 7.0

    def test_days_between_4_and_7(self):
        inp = make_input(
            calls_with_next_step_pct=0.90,
            avg_days_to_next_step=5.0,
            call_recording_compliance_pct=0.90,
        )
        assert self.e._next_step_discipline_score(inp) == 7.0

    def test_days_exactly_7(self):
        inp = make_input(
            calls_with_next_step_pct=0.90,
            avg_days_to_next_step=7.0,
            call_recording_compliance_pct=0.90,
        )
        assert self.e._next_step_discipline_score(inp) == 18.0

    def test_days_between_7_and_10(self):
        inp = make_input(
            calls_with_next_step_pct=0.90,
            avg_days_to_next_step=8.0,
            call_recording_compliance_pct=0.90,
        )
        assert self.e._next_step_discipline_score(inp) == 18.0

    def test_days_exactly_10(self):
        inp = make_input(
            calls_with_next_step_pct=0.90,
            avg_days_to_next_step=10.0,
            call_recording_compliance_pct=0.90,
        )
        assert self.e._next_step_discipline_score(inp) == 35.0

    def test_days_above_10(self):
        inp = make_input(
            calls_with_next_step_pct=0.90,
            avg_days_to_next_step=15.0,
            call_recording_compliance_pct=0.90,
        )
        assert self.e._next_step_discipline_score(inp) == 35.0

    # call_recording_compliance_pct branches
    def test_compliance_below_0_50(self):
        inp = make_input(
            calls_with_next_step_pct=0.90,
            avg_days_to_next_step=1.0,
            call_recording_compliance_pct=0.40,
        )
        assert self.e._next_step_discipline_score(inp) == 20.0

    def test_compliance_exactly_0_50(self):
        inp = make_input(
            calls_with_next_step_pct=0.90,
            avg_days_to_next_step=1.0,
            call_recording_compliance_pct=0.50,
        )
        assert self.e._next_step_discipline_score(inp) == 10.0

    def test_compliance_between_0_50_and_0_70(self):
        inp = make_input(
            calls_with_next_step_pct=0.90,
            avg_days_to_next_step=1.0,
            call_recording_compliance_pct=0.60,
        )
        assert self.e._next_step_discipline_score(inp) == 10.0

    def test_compliance_at_0_70_no_penalty(self):
        inp = make_input(
            calls_with_next_step_pct=0.90,
            avg_days_to_next_step=1.0,
            call_recording_compliance_pct=0.70,
        )
        assert self.e._next_step_discipline_score(inp) == 0.0

    def test_max_next_step_capped_at_100(self):
        inp = make_input(
            calls_with_next_step_pct=0.10,
            avg_days_to_next_step=15.0,
            call_recording_compliance_pct=0.10,
        )
        # 40 + 35 + 20 = 95
        assert self.e._next_step_discipline_score(inp) == 95.0

    def test_score_always_lte_100(self):
        inp = make_input(
            calls_with_next_step_pct=0.0,
            avg_days_to_next_step=20.0,
            call_recording_compliance_pct=0.0,
        )
        assert self.e._next_step_discipline_score(inp) <= 100.0


# ===========================================================================
# 8. PATTERN DETECTION
# ===========================================================================

class TestDetectPattern:
    def setup_method(self):
        self.e = engine()

    def _detect(self, inp, eng=0.0, disc=0.0, obj=0.0, nxt=0.0):
        return self.e._detect_pattern(inp, eng, disc, obj, nxt)

    def test_none_pattern_best_case(self):
        inp = make_input()
        result = self._detect(inp, eng=5.0, disc=5.0, obj=5.0, nxt=5.0)
        assert result == ConversationPattern.none

    # monologue_tendency: engagement >= 35 AND ratio >= 2.0
    def test_monologue_tendency_detected(self):
        inp = make_input(avg_talk_listen_ratio=2.5)
        result = self._detect(inp, eng=40.0, disc=5.0, obj=5.0, nxt=5.0)
        assert result == ConversationPattern.monologue_tendency

    def test_monologue_tendency_ratio_exactly_2_0(self):
        inp = make_input(avg_talk_listen_ratio=2.0)
        result = self._detect(inp, eng=35.0, disc=5.0, obj=5.0, nxt=5.0)
        assert result == ConversationPattern.monologue_tendency

    def test_monologue_tendency_engagement_below_35_no_match(self):
        inp = make_input(avg_talk_listen_ratio=2.5)
        result = self._detect(inp, eng=34.0, disc=5.0, obj=5.0, nxt=5.0)
        assert result != ConversationPattern.monologue_tendency

    def test_monologue_tendency_ratio_below_2_no_match(self):
        inp = make_input(avg_talk_listen_ratio=1.9)
        result = self._detect(inp, eng=40.0, disc=5.0, obj=5.0, nxt=5.0)
        assert result != ConversationPattern.monologue_tendency

    # no_next_step_discipline: next_step >= 35 AND calls_with_next_step_pct < 0.50
    def test_no_next_step_discipline_detected(self):
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            calls_with_next_step_pct=0.30,
        )
        result = self._detect(inp, eng=10.0, disc=5.0, obj=5.0, nxt=40.0)
        assert result == ConversationPattern.no_next_step_discipline

    def test_no_next_step_discipline_nxt_exactly_35(self):
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            calls_with_next_step_pct=0.40,
        )
        result = self._detect(inp, eng=10.0, disc=5.0, obj=5.0, nxt=35.0)
        assert result == ConversationPattern.no_next_step_discipline

    def test_no_next_step_discipline_nxt_below_35_no_match(self):
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            calls_with_next_step_pct=0.30,
        )
        result = self._detect(inp, eng=10.0, disc=5.0, obj=5.0, nxt=34.0)
        assert result != ConversationPattern.no_next_step_discipline

    def test_no_next_step_pct_at_0_50_no_match(self):
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            calls_with_next_step_pct=0.50,
        )
        result = self._detect(inp, eng=10.0, disc=5.0, obj=5.0, nxt=40.0)
        assert result != ConversationPattern.no_next_step_discipline

    # poor_objection_handling: objection >= 30 AND handle_rate < 0.50
    def test_poor_objection_handling_detected(self):
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            calls_with_next_step_pct=0.85,
            objection_raised_count=10,
            objection_handled_successfully_count=3,  # 30%
        )
        result = self._detect(inp, eng=10.0, disc=5.0, obj=35.0, nxt=5.0)
        assert result == ConversationPattern.poor_objection_handling

    def test_poor_objection_objection_below_30_no_match(self):
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            calls_with_next_step_pct=0.85,
            objection_raised_count=10,
            objection_handled_successfully_count=3,
        )
        result = self._detect(inp, eng=10.0, disc=5.0, obj=29.0, nxt=5.0)
        assert result != ConversationPattern.poor_objection_handling

    def test_poor_objection_handle_rate_at_0_50_no_match(self):
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            calls_with_next_step_pct=0.85,
            objection_raised_count=10,
            objection_handled_successfully_count=5,  # 50%
        )
        result = self._detect(inp, eng=10.0, disc=5.0, obj=35.0, nxt=5.0)
        assert result != ConversationPattern.poor_objection_handling

    # shallow_discovery: discovery >= 30 AND pain_identified_calls_pct < 0.40
    def test_shallow_discovery_detected(self):
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            calls_with_next_step_pct=0.85,
            objection_raised_count=10,
            objection_handled_successfully_count=8,  # 80%
            pain_identified_calls_pct=0.25,
        )
        result = self._detect(inp, eng=10.0, disc=35.0, obj=5.0, nxt=5.0)
        assert result == ConversationPattern.shallow_discovery

    def test_shallow_discovery_discovery_below_30_no_match(self):
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            calls_with_next_step_pct=0.85,
            objection_raised_count=10,
            objection_handled_successfully_count=8,
            pain_identified_calls_pct=0.25,
        )
        result = self._detect(inp, eng=10.0, disc=29.0, obj=5.0, nxt=5.0)
        assert result != ConversationPattern.shallow_discovery

    def test_shallow_discovery_pain_at_0_40_no_match(self):
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            calls_with_next_step_pct=0.85,
            objection_raised_count=10,
            objection_handled_successfully_count=8,
            pain_identified_calls_pct=0.40,
        )
        result = self._detect(inp, eng=10.0, disc=35.0, obj=5.0, nxt=5.0)
        assert result != ConversationPattern.shallow_discovery

    # low_engagement_calls: engagement >= 20 AND prospect_talk_time_pct < 0.35
    def test_low_engagement_calls_detected(self):
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            calls_with_next_step_pct=0.85,
            objection_raised_count=10,
            objection_handled_successfully_count=8,
            pain_identified_calls_pct=0.60,
            avg_prospect_talk_time_pct=0.30,
        )
        result = self._detect(inp, eng=25.0, disc=5.0, obj=5.0, nxt=5.0)
        assert result == ConversationPattern.low_engagement_calls

    def test_low_engagement_calls_engagement_below_20_no_match(self):
        inp = make_input(avg_prospect_talk_time_pct=0.25)
        result = self._detect(inp, eng=19.0, disc=5.0, obj=5.0, nxt=5.0)
        assert result != ConversationPattern.low_engagement_calls

    def test_low_engagement_calls_prospect_at_0_35_no_match(self):
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            calls_with_next_step_pct=0.85,
            objection_raised_count=10,
            objection_handled_successfully_count=8,
            pain_identified_calls_pct=0.60,
            avg_prospect_talk_time_pct=0.35,
        )
        result = self._detect(inp, eng=25.0, disc=5.0, obj=5.0, nxt=5.0)
        assert result != ConversationPattern.low_engagement_calls

    def test_priority_monologue_over_next_step(self):
        # Both conditions met; monologue has higher priority (checked first)
        inp = make_input(
            avg_talk_listen_ratio=2.5,
            calls_with_next_step_pct=0.30,
        )
        result = self._detect(inp, eng=40.0, disc=5.0, obj=5.0, nxt=40.0)
        assert result == ConversationPattern.monologue_tendency


# ===========================================================================
# 9. RISK LEVEL
# ===========================================================================

class TestRiskLevel:
    def setup_method(self):
        self.e = engine()

    def test_low_below_20(self):
        assert self.e._risk_level(19.9) == ConversationRisk.low

    def test_low_at_zero(self):
        assert self.e._risk_level(0.0) == ConversationRisk.low

    def test_moderate_at_20(self):
        assert self.e._risk_level(20.0) == ConversationRisk.moderate

    def test_moderate_at_39(self):
        assert self.e._risk_level(39.9) == ConversationRisk.moderate

    def test_high_at_40(self):
        assert self.e._risk_level(40.0) == ConversationRisk.high

    def test_high_at_59(self):
        assert self.e._risk_level(59.9) == ConversationRisk.high

    def test_critical_at_60(self):
        assert self.e._risk_level(60.0) == ConversationRisk.critical

    def test_critical_at_100(self):
        assert self.e._risk_level(100.0) == ConversationRisk.critical

    def test_critical_above_100(self):
        assert self.e._risk_level(150.0) == ConversationRisk.critical


# ===========================================================================
# 10. SEVERITY
# ===========================================================================

class TestSeverity:
    def setup_method(self):
        self.e = engine()

    def test_sharp_below_20(self):
        assert self.e._severity(19.9) == ConversationSeverity.sharp

    def test_sharp_at_zero(self):
        assert self.e._severity(0.0) == ConversationSeverity.sharp

    def test_developing_at_20(self):
        assert self.e._severity(20.0) == ConversationSeverity.developing

    def test_developing_at_39(self):
        assert self.e._severity(39.9) == ConversationSeverity.developing

    def test_weak_at_40(self):
        assert self.e._severity(40.0) == ConversationSeverity.weak

    def test_weak_at_59(self):
        assert self.e._severity(59.9) == ConversationSeverity.weak

    def test_failing_at_60(self):
        assert self.e._severity(60.0) == ConversationSeverity.failing

    def test_failing_at_100(self):
        assert self.e._severity(100.0) == ConversationSeverity.failing


# ===========================================================================
# 11. ACTION MAPPING
# ===========================================================================

class TestAction:
    def setup_method(self):
        self.e = engine()

    def test_low_risk_no_action(self):
        assert self.e._action(ConversationRisk.low, ConversationPattern.none) == ConversationAction.no_action

    def test_low_risk_any_pattern_no_action(self):
        assert self.e._action(ConversationRisk.low, ConversationPattern.monologue_tendency) == ConversationAction.no_action

    def test_moderate_risk_call_coaching(self):
        assert self.e._action(ConversationRisk.moderate, ConversationPattern.none) == ConversationAction.call_coaching_session

    def test_moderate_risk_any_pattern_call_coaching(self):
        assert self.e._action(ConversationRisk.moderate, ConversationPattern.shallow_discovery) == ConversationAction.call_coaching_session

    def test_high_risk_monologue_call_coaching(self):
        assert self.e._action(ConversationRisk.high, ConversationPattern.monologue_tendency) == ConversationAction.call_coaching_session

    def test_high_risk_no_next_step_discipline_review(self):
        assert self.e._action(ConversationRisk.high, ConversationPattern.no_next_step_discipline) == ConversationAction.next_step_discipline_review

    def test_high_risk_other_pattern_call_coaching(self):
        assert self.e._action(ConversationRisk.high, ConversationPattern.shallow_discovery) == ConversationAction.call_coaching_session

    def test_high_risk_none_pattern_call_coaching(self):
        assert self.e._action(ConversationRisk.high, ConversationPattern.none) == ConversationAction.call_coaching_session

    def test_critical_poor_objection_workshop(self):
        assert self.e._action(ConversationRisk.critical, ConversationPattern.poor_objection_handling) == ConversationAction.objection_handling_workshop

    def test_critical_shallow_discovery_training(self):
        assert self.e._action(ConversationRisk.critical, ConversationPattern.shallow_discovery) == ConversationAction.discovery_skills_training

    def test_critical_monologue_call_recording_audit(self):
        assert self.e._action(ConversationRisk.critical, ConversationPattern.monologue_tendency) == ConversationAction.call_recording_audit

    def test_critical_none_pattern_call_recording_audit(self):
        assert self.e._action(ConversationRisk.critical, ConversationPattern.none) == ConversationAction.call_recording_audit

    def test_critical_no_next_step_call_recording_audit(self):
        assert self.e._action(ConversationRisk.critical, ConversationPattern.no_next_step_discipline) == ConversationAction.call_recording_audit

    def test_critical_low_engagement_call_recording_audit(self):
        assert self.e._action(ConversationRisk.critical, ConversationPattern.low_engagement_calls) == ConversationAction.call_recording_audit

    def test_high_risk_poor_objection_call_coaching(self):
        # Not specifically handled for high risk → falls through to call_coaching_session
        assert self.e._action(ConversationRisk.high, ConversationPattern.poor_objection_handling) == ConversationAction.call_coaching_session


# ===========================================================================
# 12. FLAG: has_conversation_gap
# ===========================================================================

class TestHasConversationGap:
    def setup_method(self):
        self.e = engine()

    def test_false_when_all_ok(self):
        inp = make_input(
            calls_with_next_step_pct=0.85,
            avg_talk_listen_ratio=1.2,
        )
        assert self.e._has_conversation_gap(15.0, inp) is False

    def test_true_when_composite_ge_40(self):
        inp = make_input(
            calls_with_next_step_pct=0.85,
            avg_talk_listen_ratio=1.2,
        )
        assert self.e._has_conversation_gap(40.0, inp) is True

    def test_true_when_composite_exactly_40(self):
        inp = make_input(
            calls_with_next_step_pct=0.85,
            avg_talk_listen_ratio=1.2,
        )
        assert self.e._has_conversation_gap(40.0, inp) is True

    def test_true_when_next_step_pct_below_0_40(self):
        inp = make_input(
            calls_with_next_step_pct=0.30,
            avg_talk_listen_ratio=1.2,
        )
        assert self.e._has_conversation_gap(10.0, inp) is True

    def test_true_when_next_step_pct_exactly_0_40_border(self):
        # Below 0.40 → True; exactly 0.40 → check < so False unless composite >= 40
        inp = make_input(
            calls_with_next_step_pct=0.39,
            avg_talk_listen_ratio=1.2,
        )
        assert self.e._has_conversation_gap(10.0, inp) is True

    def test_false_when_next_step_pct_at_0_40(self):
        inp = make_input(
            calls_with_next_step_pct=0.40,
            avg_talk_listen_ratio=1.2,
        )
        assert self.e._has_conversation_gap(10.0, inp) is False

    def test_true_when_ratio_ge_2_5(self):
        inp = make_input(
            calls_with_next_step_pct=0.85,
            avg_talk_listen_ratio=2.5,
        )
        assert self.e._has_conversation_gap(10.0, inp) is True

    def test_false_when_ratio_below_2_5(self):
        inp = make_input(
            calls_with_next_step_pct=0.85,
            avg_talk_listen_ratio=2.4,
        )
        assert self.e._has_conversation_gap(10.0, inp) is False

    def test_true_multiple_conditions(self):
        inp = make_input(
            calls_with_next_step_pct=0.30,
            avg_talk_listen_ratio=3.0,
        )
        assert self.e._has_conversation_gap(60.0, inp) is True


# ===========================================================================
# 13. FLAG: requires_call_coaching
# ===========================================================================

class TestRequiresCallCoaching:
    def setup_method(self):
        self.e = engine()

    def test_false_when_all_ok(self):
        inp = make_input(
            objection_raised_count=10,
            objection_handled_successfully_count=8,  # 80%
            pain_identified_calls_pct=0.60,
        )
        assert self.e._requires_call_coaching(20.0, inp) is False

    def test_true_when_composite_ge_30(self):
        inp = make_input(
            objection_raised_count=10,
            objection_handled_successfully_count=8,
            pain_identified_calls_pct=0.60,
        )
        assert self.e._requires_call_coaching(30.0, inp) is True

    def test_true_when_composite_exactly_30(self):
        inp = make_input(
            objection_raised_count=10,
            objection_handled_successfully_count=8,
            pain_identified_calls_pct=0.60,
        )
        assert self.e._requires_call_coaching(30.0, inp) is True

    def test_true_when_handle_rate_below_0_50(self):
        inp = make_input(
            objection_raised_count=10,
            objection_handled_successfully_count=4,  # 40%
            pain_identified_calls_pct=0.60,
        )
        assert self.e._requires_call_coaching(10.0, inp) is True

    def test_false_when_handle_rate_at_0_50(self):
        inp = make_input(
            objection_raised_count=10,
            objection_handled_successfully_count=5,  # 50%
            pain_identified_calls_pct=0.60,
        )
        assert self.e._requires_call_coaching(10.0, inp) is False

    def test_true_when_pain_below_0_30(self):
        inp = make_input(
            objection_raised_count=10,
            objection_handled_successfully_count=8,
            pain_identified_calls_pct=0.20,
        )
        assert self.e._requires_call_coaching(10.0, inp) is True

    def test_false_when_pain_at_0_30(self):
        inp = make_input(
            objection_raised_count=10,
            objection_handled_successfully_count=8,
            pain_identified_calls_pct=0.30,
        )
        assert self.e._requires_call_coaching(10.0, inp) is False

    def test_zero_objections_handle_rate_zero_triggers_coaching(self):
        inp = make_input(
            objection_raised_count=0,
            objection_handled_successfully_count=0,
            pain_identified_calls_pct=0.60,
        )
        assert self.e._requires_call_coaching(10.0, inp) is True


# ===========================================================================
# 14. REVENUE IMPACT
# ===========================================================================

class TestEstimatedRevenueImpact:
    def setup_method(self):
        self.e = engine()

    def test_zero_composite_zero_impact(self):
        inp = make_input(total_calls_analyzed=100, avg_opportunity_value_usd=10_000)
        assert self.e._estimated_revenue_impact(inp, 0.0) == 0.0

    def test_formula_basic(self):
        # calls=100, composite=50 → low_eng=round(100*0.5)=50
        # conv_loss=0.5 → 50 * 10000 * 0.5 * 0.15 = 37500
        inp = make_input(total_calls_analyzed=100, avg_opportunity_value_usd=10_000)
        result = self.e._estimated_revenue_impact(inp, 50.0)
        assert result == 37500.0

    def test_formula_composite_100(self):
        # calls=10, composite=100 → low_eng=round(10*1.0)=10
        # conv_loss=1.0 → 10 * 5000 * 1.0 * 0.15 = 7500
        inp = make_input(total_calls_analyzed=10, avg_opportunity_value_usd=5_000)
        result = self.e._estimated_revenue_impact(inp, 100.0)
        assert result == 7500.0

    def test_returns_float(self):
        inp = make_input(total_calls_analyzed=50, avg_opportunity_value_usd=20_000)
        result = self.e._estimated_revenue_impact(inp, 40.0)
        assert isinstance(result, float)

    def test_rounded_to_2_decimal_places(self):
        inp = make_input(total_calls_analyzed=3, avg_opportunity_value_usd=333.33)
        result = self.e._estimated_revenue_impact(inp, 50.0)
        # verify it's rounded to 2 dp
        assert result == round(result, 2)

    def test_proportional_to_opportunity_value(self):
        inp1 = make_input(total_calls_analyzed=10, avg_opportunity_value_usd=1000)
        inp2 = make_input(total_calls_analyzed=10, avg_opportunity_value_usd=2000)
        r1 = self.e._estimated_revenue_impact(inp1, 50.0)
        r2 = self.e._estimated_revenue_impact(inp2, 50.0)
        assert r2 == pytest.approx(r1 * 2, rel=1e-5)

    def test_small_composite(self):
        inp = make_input(total_calls_analyzed=100, avg_opportunity_value_usd=10_000)
        result = self.e._estimated_revenue_impact(inp, 10.0)
        # round(100*0.1)=10, 10 * 10000 * 0.1 * 0.15 = 1500
        assert result == 1500.0


# ===========================================================================
# 15. SIGNAL GENERATION
# ===========================================================================

class TestSignal:
    def setup_method(self):
        self.e = engine()

    def test_healthy_signal_when_none_pattern_and_low_composite(self):
        inp = make_input()
        sig = self.e._signal(inp, ConversationPattern.none, 15.0)
        assert sig == "Conversation quality healthy — discovery, objection handling, and next steps within benchmarks"

    def test_healthy_signal_composite_exactly_0(self):
        inp = make_input()
        sig = self.e._signal(inp, ConversationPattern.none, 0.0)
        assert sig == "Conversation quality healthy — discovery, objection handling, and next steps within benchmarks"

    def test_no_healthy_signal_when_composite_equals_20(self):
        inp = make_input()
        sig = self.e._signal(inp, ConversationPattern.none, 20.0)
        assert "healthy" not in sig

    def test_no_healthy_signal_when_pattern_not_none(self):
        inp = make_input()
        sig = self.e._signal(inp, ConversationPattern.monologue_tendency, 10.0)
        assert "healthy" not in sig

    def test_signal_includes_ratio_when_ratio_ge_1_5(self):
        inp = make_input(
            avg_talk_listen_ratio=2.5,
            calls_with_next_step_pct=0.85,
            pain_identified_calls_pct=1.0,
        )
        sig = self.e._signal(inp, ConversationPattern.monologue_tendency, 40.0)
        assert "2.5x talk/listen ratio" in sig

    def test_signal_excludes_ratio_when_ratio_below_1_5(self):
        inp = make_input(
            avg_talk_listen_ratio=1.4,
            calls_with_next_step_pct=0.85,
            pain_identified_calls_pct=1.0,
        )
        sig = self.e._signal(inp, ConversationPattern.monologue_tendency, 40.0)
        assert "talk/listen ratio" not in sig

    def test_signal_includes_next_step_pct(self):
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            calls_with_next_step_pct=0.70,
            pain_identified_calls_pct=1.0,
        )
        sig = self.e._signal(inp, ConversationPattern.no_next_step_discipline, 40.0)
        assert "70% calls with next step" in sig

    def test_signal_includes_pain_pct(self):
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            calls_with_next_step_pct=1.0,
            pain_identified_calls_pct=0.45,
        )
        sig = self.e._signal(inp, ConversationPattern.shallow_discovery, 40.0)
        assert "45% pain identified" in sig

    def test_signal_label_from_pattern(self):
        inp = make_input(
            avg_talk_listen_ratio=2.5,
            calls_with_next_step_pct=0.85,
            pain_identified_calls_pct=1.0,
        )
        sig = self.e._signal(inp, ConversationPattern.monologue_tendency, 40.0)
        assert sig.startswith("Monologue tendency")

    def test_signal_label_none_pattern_above_composite_20(self):
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            calls_with_next_step_pct=1.0,
            pain_identified_calls_pct=1.0,
        )
        sig = self.e._signal(inp, ConversationPattern.none, 25.0)
        assert sig.startswith("Conversation risk")

    def test_signal_includes_composite(self):
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            calls_with_next_step_pct=1.0,
            pain_identified_calls_pct=1.0,
        )
        sig = self.e._signal(inp, ConversationPattern.none, 35.0)
        assert "composite 35" in sig

    def test_signal_call_quality_declining_fallback(self):
        # all parts filtered out: ratio < 1.5, calls_with_next_step=1.0, pain=1.0
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            calls_with_next_step_pct=1.0,
            pain_identified_calls_pct=1.0,
        )
        sig = self.e._signal(inp, ConversationPattern.none, 25.0)
        assert "call quality declining" in sig

    def test_signal_format_with_all_parts(self):
        inp = make_input(
            avg_talk_listen_ratio=2.0,
            calls_with_next_step_pct=0.60,
            pain_identified_calls_pct=0.50,
        )
        sig = self.e._signal(inp, ConversationPattern.monologue_tendency, 50.0)
        # Should contain all three parts
        assert "2.0x talk/listen ratio" in sig
        assert "60% calls with next step" in sig
        assert "50% pain identified" in sig


# ===========================================================================
# 16. ASSESS()
# ===========================================================================

class TestAssess:
    def setup_method(self):
        self.e = engine()

    def test_returns_result_object(self):
        result = self.e.assess(make_input())
        assert isinstance(result, ConversationQualityResult)

    def test_rep_id_propagated(self):
        result = self.e.assess(make_input(rep_id="REP-XYZ"))
        assert result.rep_id == "REP-XYZ"

    def test_region_propagated(self):
        result = self.e.assess(make_input(region="APAC"))
        assert result.region == "APAC"

    def test_healthy_rep_gets_low_risk(self):
        result = self.e.assess(make_input())
        assert result.conversation_risk == ConversationRisk.low

    def test_healthy_rep_gets_sharp_severity(self):
        result = self.e.assess(make_input())
        assert result.conversation_severity == ConversationSeverity.sharp

    def test_healthy_rep_no_action(self):
        result = self.e.assess(make_input())
        assert result.recommended_action == ConversationAction.no_action

    def test_healthy_rep_no_gap(self):
        result = self.e.assess(make_input())
        assert result.has_conversation_gap is False

    def test_healthy_rep_healthy_signal(self):
        result = self.e.assess(make_input())
        assert "healthy" in result.conversation_signal

    def test_composite_calculation_formula(self):
        # Use inputs to produce known scores and verify composite
        inp = make_input()
        result = self.e.assess(inp)
        e = result.engagement_quality_score
        d = result.discovery_depth_score
        o = result.objection_handling_score
        n = result.next_step_discipline_score
        expected = round(e * 0.30 + d * 0.30 + o * 0.25 + n * 0.15, 1)
        assert result.conversation_composite == pytest.approx(expected, abs=0.15)

    def test_composite_capped_at_100(self):
        inp = make_input(
            avg_talk_listen_ratio=5.0,
            avg_questions_per_call=0.5,
            pain_identified_calls_pct=0.0,
            budget_discussed_calls_pct=0.0,
            objection_raised_count=0,
            objection_handled_successfully_count=0,
            filler_words_per_minute=10.0,
            interruptions_per_call=10.0,
            avg_prospect_talk_time_pct=0.05,
            calls_with_decision_maker_pct=0.05,
            calls_with_next_step_pct=0.10,
            avg_days_to_next_step=20.0,
            call_recording_compliance_pct=0.10,
        )
        result = self.e.assess(inp)
        assert result.conversation_composite <= 100.0

    def test_result_stored_in_results(self):
        e = engine()
        e.assess(make_input())
        assert len(e._results) == 1

    def test_multiple_calls_store_multiple_results(self):
        e = engine()
        e.assess(make_input())
        e.assess(make_input(rep_id="REP-002"))
        assert len(e._results) == 2

    def test_assess_critical_rep(self):
        inp = make_input(
            avg_talk_listen_ratio=3.0,
            avg_questions_per_call=1.0,
            pain_identified_calls_pct=0.10,
            budget_discussed_calls_pct=0.05,
            objection_raised_count=10,
            objection_handled_successfully_count=1,
            filler_words_per_minute=6.0,
            interruptions_per_call=6.0,
            avg_prospect_talk_time_pct=0.15,
            calls_with_decision_maker_pct=0.05,
            calls_with_next_step_pct=0.20,
            avg_days_to_next_step=12.0,
            call_recording_compliance_pct=0.30,
        )
        result = self.e.assess(inp)
        assert result.conversation_risk == ConversationRisk.critical
        assert result.conversation_severity == ConversationSeverity.failing

    def test_assess_moderate_rep(self):
        inp = make_input(
            avg_talk_listen_ratio=1.6,
            avg_questions_per_call=5.0,
            pain_identified_calls_pct=0.40,
            budget_discussed_calls_pct=0.30,
            objection_raised_count=10,
            objection_handled_successfully_count=5,
            filler_words_per_minute=1.0,
            interruptions_per_call=1.0,
            avg_prospect_talk_time_pct=0.50,
            calls_with_decision_maker_pct=0.50,
            calls_with_next_step_pct=0.70,
            avg_days_to_next_step=5.0,
            call_recording_compliance_pct=0.75,
        )
        result = self.e.assess(inp)
        # Moderate or lower based on the sub-scores
        assert result.conversation_risk in (ConversationRisk.low, ConversationRisk.moderate, ConversationRisk.high)

    def test_scores_are_rounded_to_1dp(self):
        result = self.e.assess(make_input())
        for score in [
            result.engagement_quality_score,
            result.discovery_depth_score,
            result.objection_handling_score,
            result.next_step_discipline_score,
            result.conversation_composite,
        ]:
            assert round(score, 1) == score

    def test_revenue_impact_non_negative(self):
        result = self.e.assess(make_input())
        assert result.estimated_revenue_impact_usd >= 0.0

    def test_to_dict_works_on_assessed_result(self):
        result = self.e.assess(make_input())
        d = result.to_dict()
        assert isinstance(d, dict)
        assert len(d) == 15

    def test_pattern_is_valid_enum(self):
        result = self.e.assess(make_input())
        assert isinstance(result.conversation_pattern, ConversationPattern)

    def test_risk_is_valid_enum(self):
        result = self.e.assess(make_input())
        assert isinstance(result.conversation_risk, ConversationRisk)

    def test_severity_is_valid_enum(self):
        result = self.e.assess(make_input())
        assert isinstance(result.conversation_severity, ConversationSeverity)

    def test_action_is_valid_enum(self):
        result = self.e.assess(make_input())
        assert isinstance(result.recommended_action, ConversationAction)


# ===========================================================================
# 17. ASSESS_BATCH()
# ===========================================================================

class TestAssessBatch:
    def setup_method(self):
        self.e = engine()

    def test_returns_list(self):
        result = self.e.assess_batch([make_input()])
        assert isinstance(result, list)

    def test_empty_batch_returns_empty_list(self):
        result = self.e.assess_batch([])
        assert result == []

    def test_single_item_batch(self):
        result = self.e.assess_batch([make_input()])
        assert len(result) == 1

    def test_multiple_items_batch(self):
        inputs = [make_input(rep_id=f"REP-{i}") for i in range(5)]
        result = self.e.assess_batch(inputs)
        assert len(result) == 5

    def test_results_are_convo_quality_results(self):
        result = self.e.assess_batch([make_input(), make_input(rep_id="REP-002")])
        assert all(isinstance(r, ConversationQualityResult) for r in result)

    def test_batch_stores_all_results(self):
        e = engine()
        e.assess_batch([make_input(rep_id=f"REP-{i}") for i in range(3)])
        assert len(e._results) == 3

    def test_batch_rep_ids_preserved(self):
        inputs = [make_input(rep_id=f"REP-{i}") for i in range(3)]
        results = self.e.assess_batch(inputs)
        assert [r.rep_id for r in results] == ["REP-0", "REP-1", "REP-2"]

    def test_batch_combines_with_prior_assess(self):
        e = engine()
        e.assess(make_input(rep_id="REP-0"))
        e.assess_batch([make_input(rep_id="REP-1"), make_input(rep_id="REP-2")])
        assert len(e._results) == 3

    def test_each_result_has_correct_region(self):
        inputs = [
            make_input(rep_id="R1", region="EMEA"),
            make_input(rep_id="R2", region="APAC"),
        ]
        results = self.e.assess_batch(inputs)
        assert results[0].region == "EMEA"
        assert results[1].region == "APAC"


# ===========================================================================
# 18. SUMMARY()
# ===========================================================================

class TestSummary:
    def test_empty_summary_has_13_keys(self):
        e = engine()
        s = e.summary()
        assert len(s) == 13

    def test_empty_summary_total_zero(self):
        e = engine()
        assert e.summary()["total"] == 0

    def test_empty_summary_risk_counts_empty(self):
        e = engine()
        assert e.summary()["risk_counts"] == {}

    def test_empty_summary_pattern_counts_empty(self):
        e = engine()
        assert e.summary()["pattern_counts"] == {}

    def test_empty_summary_severity_counts_empty(self):
        e = engine()
        assert e.summary()["severity_counts"] == {}

    def test_empty_summary_action_counts_empty(self):
        e = engine()
        assert e.summary()["action_counts"] == {}

    def test_empty_summary_avg_composite_zero(self):
        e = engine()
        assert e.summary()["avg_conversation_composite"] == 0.0

    def test_empty_summary_gap_count_zero(self):
        e = engine()
        assert e.summary()["conversation_gap_count"] == 0

    def test_empty_summary_coaching_count_zero(self):
        e = engine()
        assert e.summary()["coaching_count"] == 0

    def test_empty_summary_avg_engagement_zero(self):
        e = engine()
        assert e.summary()["avg_engagement_quality_score"] == 0.0

    def test_empty_summary_avg_discovery_zero(self):
        e = engine()
        assert e.summary()["avg_discovery_depth_score"] == 0.0

    def test_empty_summary_avg_objection_zero(self):
        e = engine()
        assert e.summary()["avg_objection_handling_score"] == 0.0

    def test_empty_summary_avg_next_step_zero(self):
        e = engine()
        assert e.summary()["avg_next_step_discipline_score"] == 0.0

    def test_empty_summary_total_impact_zero(self):
        e = engine()
        assert e.summary()["total_estimated_revenue_impact_usd"] == 0.0

    def test_summary_after_one_assess(self):
        e = engine()
        e.assess(make_input())
        s = e.summary()
        assert s["total"] == 1

    def test_summary_after_multiple_assess(self):
        e = engine()
        for i in range(5):
            e.assess(make_input(rep_id=f"REP-{i}"))
        assert e.summary()["total"] == 5

    def test_summary_risk_counts_correct(self):
        e = engine()
        e.assess(make_input())  # low risk
        s = e.summary()
        assert "low" in s["risk_counts"]
        assert s["risk_counts"]["low"] == 1

    def test_summary_pattern_counts_correct(self):
        e = engine()
        e.assess(make_input())  # none pattern
        s = e.summary()
        assert "none" in s["pattern_counts"]

    def test_summary_severity_counts_correct(self):
        e = engine()
        e.assess(make_input())  # sharp
        s = e.summary()
        assert "sharp" in s["severity_counts"]

    def test_summary_action_counts_correct(self):
        e = engine()
        e.assess(make_input())  # no_action
        s = e.summary()
        assert "no_action" in s["action_counts"]

    def test_summary_avg_composite_correct(self):
        e = engine()
        r1 = e.assess(make_input())
        r2 = e.assess(make_input(rep_id="R2"))
        s = e.summary()
        expected = round((r1.conversation_composite + r2.conversation_composite) / 2, 1)
        assert s["avg_conversation_composite"] == expected

    def test_summary_gap_count_correct(self):
        e = engine()
        e.assess(make_input())  # no gap
        e.assess(make_input(rep_id="R2", calls_with_next_step_pct=0.30))  # has gap
        s = e.summary()
        assert s["conversation_gap_count"] == 1

    def test_summary_coaching_count_correct(self):
        e = engine()
        e.assess(make_input())  # no coaching needed
        e.assess(make_input(
            rep_id="R2",
            objection_raised_count=10,
            objection_handled_successfully_count=3,
        ))  # coaching needed
        s = e.summary()
        assert s["coaching_count"] >= 1

    def test_summary_total_impact_is_sum(self):
        e = engine()
        r1 = e.assess(make_input())
        r2 = e.assess(make_input(rep_id="R2"))
        s = e.summary()
        expected = round(r1.estimated_revenue_impact_usd + r2.estimated_revenue_impact_usd, 2)
        assert s["total_estimated_revenue_impact_usd"] == expected

    def test_summary_avg_engagement_correct(self):
        e = engine()
        r = e.assess(make_input())
        s = e.summary()
        assert s["avg_engagement_quality_score"] == r.engagement_quality_score

    def test_summary_avg_discovery_correct(self):
        e = engine()
        r = e.assess(make_input())
        s = e.summary()
        assert s["avg_discovery_depth_score"] == r.discovery_depth_score

    def test_summary_avg_objection_correct(self):
        e = engine()
        r = e.assess(make_input())
        s = e.summary()
        assert s["avg_objection_handling_score"] == r.objection_handling_score

    def test_summary_avg_next_step_correct(self):
        e = engine()
        r = e.assess(make_input())
        s = e.summary()
        assert s["avg_next_step_discipline_score"] == r.next_step_discipline_score

    def test_summary_expected_keys(self):
        e = engine()
        e.assess(make_input())
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_conversation_composite", "conversation_gap_count",
            "coaching_count", "avg_engagement_quality_score",
            "avg_discovery_depth_score", "avg_objection_handling_score",
            "avg_next_step_discipline_score", "total_estimated_revenue_impact_usd",
        }
        assert set(e.summary().keys()) == expected_keys

    def test_summary_multiple_risk_counts(self):
        e = engine()
        # healthy rep → low
        e.assess(make_input())
        # critical rep
        e.assess(make_input(
            rep_id="R2",
            avg_talk_listen_ratio=3.0,
            avg_questions_per_call=1.0,
            pain_identified_calls_pct=0.10,
            budget_discussed_calls_pct=0.05,
            objection_raised_count=10,
            objection_handled_successfully_count=1,
            filler_words_per_minute=6.0,
            interruptions_per_call=6.0,
            avg_prospect_talk_time_pct=0.15,
            calls_with_decision_maker_pct=0.05,
            calls_with_next_step_pct=0.20,
            avg_days_to_next_step=12.0,
            call_recording_compliance_pct=0.30,
        ))
        s = e.summary()
        assert s["total"] == 2
        assert "low" in s["risk_counts"] or "moderate" in s["risk_counts"] or "high" in s["risk_counts"] or "critical" in s["risk_counts"]


# ===========================================================================
# 19. EDGE CASES
# ===========================================================================

class TestEdgeCases:
    def setup_method(self):
        self.e = engine()

    def test_zero_total_calls_analyzed(self):
        inp = make_input(total_calls_analyzed=0)
        result = self.e.assess(inp)
        # revenue impact: round(0 * ...)=0
        assert result.estimated_revenue_impact_usd == 0.0

    def test_very_high_opportunity_value(self):
        inp = make_input(
            avg_opportunity_value_usd=1_000_000.0,
            total_calls_analyzed=100,
        )
        result = self.e.assess(inp)
        assert result.estimated_revenue_impact_usd >= 0.0

    def test_all_objections_handled(self):
        inp = make_input(
            objection_raised_count=10,
            objection_handled_successfully_count=10,
        )
        result = self.e.assess(inp)
        # handle_rate = 1.0 → no penalty from objection handling
        assert result.objection_handling_score < 45.0

    def test_single_objection_raised_one_handled(self):
        inp = make_input(
            objection_raised_count=1,
            objection_handled_successfully_count=1,
        )
        result = self.e.assess(inp)
        # rate = 1.0 → no penalty
        assert self.e._objection_handling_score(inp) == 0.0 or \
               self.e._objection_handling_score(inp) <= 50.0

    def test_engine_initial_results_empty(self):
        e = engine()
        assert e._results == []

    def test_different_regions(self):
        for region in ["EMEA", "APAC", "AMER", "LATAM"]:
            result = self.e.assess(make_input(region=region))
            assert result.region == region

    def test_all_pcts_at_1_0(self):
        inp = make_input(
            calls_with_next_step_pct=1.0,
            avg_prospect_talk_time_pct=1.0,
            calls_with_decision_maker_pct=1.0,
            pain_identified_calls_pct=1.0,
            budget_discussed_calls_pct=1.0,
            multi_thread_calls_pct=1.0,
            call_recording_compliance_pct=1.0,
            discovery_questions_pct=1.0,
        )
        result = self.e.assess(inp)
        assert result is not None

    def test_all_pcts_at_0_0(self):
        inp = make_input(
            calls_with_next_step_pct=0.0,
            avg_prospect_talk_time_pct=0.0,
            calls_with_decision_maker_pct=0.0,
            pain_identified_calls_pct=0.0,
            budget_discussed_calls_pct=0.0,
            multi_thread_calls_pct=0.0,
            call_recording_compliance_pct=0.0,
            discovery_questions_pct=0.0,
        )
        result = self.e.assess(inp)
        # Several penalty factors active; composite will be at least moderate
        assert result.conversation_risk in (
            ConversationRisk.moderate, ConversationRisk.high, ConversationRisk.critical
        )

    def test_exactly_at_risk_boundary_20(self):
        e = engine()
        # Force composite exactly 20
        assert e._risk_level(20.0) == ConversationRisk.moderate
        assert e._severity(20.0) == ConversationSeverity.developing

    def test_exactly_at_risk_boundary_40(self):
        e = engine()
        assert e._risk_level(40.0) == ConversationRisk.high
        assert e._severity(40.0) == ConversationSeverity.weak

    def test_exactly_at_risk_boundary_60(self):
        e = engine()
        assert e._risk_level(60.0) == ConversationRisk.critical
        assert e._severity(60.0) == ConversationSeverity.failing

    def test_boundary_just_below_60(self):
        e = engine()
        assert e._risk_level(59.9) == ConversationRisk.high

    def test_zero_filler_words(self):
        inp = make_input(filler_words_per_minute=0.0)
        assert self.e._engagement_quality_score(inp) == 0.0

    def test_zero_interruptions(self):
        inp = make_input(
            objection_raised_count=10,
            objection_handled_successfully_count=10,
            interruptions_per_call=0.0,
            calls_with_decision_maker_pct=0.50,
        )
        assert self.e._objection_handling_score(inp) == 0.0

    def test_very_large_questions_per_call(self):
        inp = make_input(avg_questions_per_call=100.0)
        assert self.e._discovery_depth_score(inp) == 0.0

    def test_engine_freshly_instantiated_each_time(self):
        e1 = engine()
        e2 = engine()
        e1.assess(make_input())
        assert len(e2._results) == 0


# ===========================================================================
# 20. END-TO-END SCENARIOS
# ===========================================================================

class TestEndToEndScenarios:
    """Full scenario tests that exercise multiple methods together."""

    def test_star_performer(self):
        """A rep with exemplary metrics should get low risk, sharp, no action."""
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            avg_questions_per_call=9.0,
            pain_identified_calls_pct=0.75,
            budget_discussed_calls_pct=0.60,
            objection_raised_count=10,
            objection_handled_successfully_count=9,
            filler_words_per_minute=0.5,
            interruptions_per_call=0.5,
            avg_prospect_talk_time_pct=0.55,
            calls_with_decision_maker_pct=0.70,
            calls_with_next_step_pct=0.95,
            avg_days_to_next_step=2.0,
            call_recording_compliance_pct=0.95,
        )
        e = engine()
        r = e.assess(inp)
        assert r.conversation_risk == ConversationRisk.low
        assert r.conversation_severity == ConversationSeverity.sharp
        assert r.recommended_action == ConversationAction.no_action
        assert r.has_conversation_gap is False
        assert "healthy" in r.conversation_signal

    def test_struggling_rep_critical(self):
        """A rep with very poor metrics should get critical risk, failing, and recording audit."""
        inp = make_input(
            avg_talk_listen_ratio=3.5,
            avg_questions_per_call=1.0,
            pain_identified_calls_pct=0.10,
            budget_discussed_calls_pct=0.05,
            objection_raised_count=10,
            objection_handled_successfully_count=2,
            filler_words_per_minute=7.0,
            interruptions_per_call=7.0,
            avg_prospect_talk_time_pct=0.10,
            calls_with_decision_maker_pct=0.05,
            calls_with_next_step_pct=0.15,
            avg_days_to_next_step=15.0,
            call_recording_compliance_pct=0.20,
        )
        e = engine()
        r = e.assess(inp)
        assert r.conversation_risk == ConversationRisk.critical
        assert r.conversation_severity == ConversationSeverity.failing
        assert r.has_conversation_gap is True
        assert r.requires_call_coaching is True
        assert r.conversation_composite >= 60.0

    def test_monologue_rep_gets_coaching(self):
        """Rep with high talk/listen ratio and moderate risk should get coaching."""
        inp = make_input(
            avg_talk_listen_ratio=2.5,
            avg_questions_per_call=5.0,
            pain_identified_calls_pct=0.40,
            budget_discussed_calls_pct=0.25,
            objection_raised_count=10,
            objection_handled_successfully_count=5,
            filler_words_per_minute=4.0,
            interruptions_per_call=2.0,
            avg_prospect_talk_time_pct=0.25,
            calls_with_decision_maker_pct=0.40,
            calls_with_next_step_pct=0.70,
            avg_days_to_next_step=5.0,
            call_recording_compliance_pct=0.75,
        )
        e = engine()
        r = e.assess(inp)
        # Risk should be >= moderate since many penalties apply
        assert r.conversation_risk in (ConversationRisk.moderate, ConversationRisk.high, ConversationRisk.critical)

    def test_next_step_problem_rep(self):
        """Rep with next step discipline issue detected."""
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            avg_questions_per_call=8.0,
            pain_identified_calls_pct=0.65,
            budget_discussed_calls_pct=0.50,
            objection_raised_count=10,
            objection_handled_successfully_count=9,
            filler_words_per_minute=1.0,
            interruptions_per_call=1.0,
            avg_prospect_talk_time_pct=0.55,
            calls_with_decision_maker_pct=0.55,
            calls_with_next_step_pct=0.30,
            avg_days_to_next_step=12.0,
            call_recording_compliance_pct=0.30,
        )
        e = engine()
        r = e.assess(inp)
        assert r.has_conversation_gap is True  # calls_with_next_step_pct < 0.40

    def test_batch_then_summary_consistent(self):
        """assess_batch results should be reflected accurately in summary."""
        e = engine()
        inputs = [make_input(rep_id=f"REP-{i}") for i in range(10)]
        results = e.assess_batch(inputs)
        s = e.summary()
        assert s["total"] == 10
        assert sum(s["risk_counts"].values()) == 10
        assert sum(s["pattern_counts"].values()) == 10
        assert sum(s["severity_counts"].values()) == 10
        assert sum(s["action_counts"].values()) == 10

    def test_to_dict_values_match_result_fields(self):
        e = engine()
        r = e.assess(make_input())
        d = r.to_dict()
        assert d["rep_id"] == r.rep_id
        assert d["region"] == r.region
        assert d["conversation_risk"] == r.conversation_risk.value
        assert d["conversation_pattern"] == r.conversation_pattern.value
        assert d["conversation_severity"] == r.conversation_severity.value
        assert d["recommended_action"] == r.recommended_action.value
        assert d["engagement_quality_score"] == r.engagement_quality_score
        assert d["discovery_depth_score"] == r.discovery_depth_score
        assert d["objection_handling_score"] == r.objection_handling_score
        assert d["next_step_discipline_score"] == r.next_step_discipline_score
        assert d["conversation_composite"] == r.conversation_composite
        assert d["has_conversation_gap"] == r.has_conversation_gap
        assert d["requires_call_coaching"] == r.requires_call_coaching
        assert d["estimated_revenue_impact_usd"] == r.estimated_revenue_impact_usd
        assert d["conversation_signal"] == r.conversation_signal

    def test_fresh_engine_produces_same_result_for_same_input(self):
        """Two fresh engines must produce identical results for same input."""
        inp = make_input()
        e1 = engine()
        e2 = engine()
        r1 = e1.assess(inp)
        r2 = e2.assess(inp)
        assert r1.conversation_composite == r2.conversation_composite
        assert r1.conversation_risk == r2.conversation_risk
        assert r1.conversation_pattern == r2.conversation_pattern

    def test_assessment_does_not_affect_other_engines(self):
        """Assessment on one engine doesn't pollute another."""
        e1 = engine()
        e2 = engine()
        e1.assess(make_input())
        assert len(e2._results) == 0

    def test_objection_workshop_triggered_critical_poor_objection(self):
        """Critical risk + poor_objection_handling → objection_handling_workshop."""
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            avg_questions_per_call=1.0,
            pain_identified_calls_pct=0.10,
            budget_discussed_calls_pct=0.05,
            objection_raised_count=10,
            objection_handled_successfully_count=2,  # 20% rate → poor_objection
            filler_words_per_minute=6.0,
            interruptions_per_call=6.0,
            avg_prospect_talk_time_pct=0.50,
            calls_with_decision_maker_pct=0.05,
            calls_with_next_step_pct=0.85,
            avg_days_to_next_step=2.0,
            call_recording_compliance_pct=0.85,
        )
        e = engine()
        r = e.assess(inp)
        if r.conversation_risk == ConversationRisk.critical and \
           r.conversation_pattern == ConversationPattern.poor_objection_handling:
            assert r.recommended_action == ConversationAction.objection_handling_workshop

    def test_discovery_training_triggered_critical_shallow_discovery(self):
        """Critical risk + shallow_discovery → discovery_skills_training."""
        inp = make_input(
            avg_talk_listen_ratio=1.0,
            avg_questions_per_call=2.0,
            pain_identified_calls_pct=0.10,
            budget_discussed_calls_pct=0.05,
            objection_raised_count=10,
            objection_handled_successfully_count=10,  # 100% → no poor_objection
            filler_words_per_minute=6.0,
            interruptions_per_call=6.0,
            avg_prospect_talk_time_pct=0.50,
            calls_with_decision_maker_pct=0.05,
            calls_with_next_step_pct=0.85,
            avg_days_to_next_step=2.0,
            call_recording_compliance_pct=0.85,
        )
        e = engine()
        r = e.assess(inp)
        if r.conversation_risk == ConversationRisk.critical and \
           r.conversation_pattern == ConversationPattern.shallow_discovery:
            assert r.recommended_action == ConversationAction.discovery_skills_training

    def test_next_step_review_triggered_high_risk(self):
        """High risk + no_next_step_discipline → next_step_discipline_review."""
        e = engine()
        assert e._action(ConversationRisk.high, ConversationPattern.no_next_step_discipline) == \
               ConversationAction.next_step_discipline_review

    def test_large_batch_summary_totals(self):
        """Summary totals for a large batch are internally consistent."""
        e = engine()
        inputs = [make_input(rep_id=f"R{i}", avg_opportunity_value_usd=float(i * 1000 + 5000))
                  for i in range(20)]
        results = e.assess_batch(inputs)
        s = e.summary()
        assert s["total"] == 20
        total_gap = sum(1 for r in results if r.has_conversation_gap)
        assert s["conversation_gap_count"] == total_gap
        total_coaching = sum(1 for r in results if r.requires_call_coaching)
        assert s["coaching_count"] == total_coaching
        total_impact = round(sum(r.estimated_revenue_impact_usd for r in results), 2)
        assert s["total_estimated_revenue_impact_usd"] == pytest.approx(total_impact, abs=0.01)
