"""
Comprehensive pytest test suite for SalesCoachingReceptivityIntelligenceEngine.
Covers all enums, fields, sub-scores, composite, thresholds, patterns, flags,
waste formula, signal, assess, assess_batch, summary, and edge cases.
"""
from __future__ import annotations
import pytest
from swarm.intelligence.sales_coaching_receptivity_intelligence_engine import (
    CoachRisk,
    CoachPattern,
    CoachSeverity,
    CoachAction,
    CoachInput,
    CoachResult,
    SalesCoachingReceptivityIntelligenceEngine,
)


# ──────────────────────────────────────────────────────────────────────────────
# Helper
# ──────────────────────────────────────────────────────────────────────────────

def make_input(**overrides) -> CoachInput:
    """Return a minimal valid CoachInput with all scores producing a low composite."""
    defaults = dict(
        rep_id="REP-001",
        region="Northeast",
        evaluation_period_id="Q1-2026",
        # sub-score fields all set to "good" values (low resistance)
        feedback_implementation_rate_pct=0.90,   # high = good
        skill_improvement_after_coaching=0.60,   # high = good
        action_item_completion_rate_pct=0.90,    # high = good
        sessions_attended_rate_pct=0.95,         # high = good
        voluntary_coaching_requests=5,
        reversion_rate_pct=0.05,                 # low = good
        follow_through_score=0.90,               # high = good
        peer_learning_engagement_pct=0.80,       # high = good
        call_recording_review_rate_pct=0.80,     # high = good
        manager_satisfaction_score=0.90,         # high = good
        self_assessment_accuracy_pct=0.85,
        improvement_velocity=0.80,               # high = good
        prior_pip_count=0,
        coaching_hours_utilized_pct=0.90,        # high = good
        multi_modal_engagement_pct=0.80,
        challenge_question_rate_pct=0.05,        # low = good
        engagement_consistency_pct=0.90,
        total_coaching_sessions=10,
        avg_session_duration_minutes=45.0,
    )
    defaults.update(overrides)
    return CoachInput(**defaults)


def fresh_engine() -> SalesCoachingReceptivityIntelligenceEngine:
    return SalesCoachingReceptivityIntelligenceEngine()


# ══════════════════════════════════════════════════════════════════════════════
# 1. ENUM VALUES AND COUNTS
# ══════════════════════════════════════════════════════════════════════════════

class TestCoachRiskEnum:
    def test_count(self):
        assert len(CoachRisk) == 4

    def test_low(self):
        assert CoachRisk.low.value == "low"

    def test_moderate(self):
        assert CoachRisk.moderate.value == "moderate"

    def test_high(self):
        assert CoachRisk.high.value == "high"

    def test_critical(self):
        assert CoachRisk.critical.value == "critical"

    def test_is_str_enum(self):
        assert isinstance(CoachRisk.low, str)

    def test_all_values_unique(self):
        values = [r.value for r in CoachRisk]
        assert len(values) == len(set(values))

    def test_members(self):
        names = {r.name for r in CoachRisk}
        assert names == {"low", "moderate", "high", "critical"}


class TestCoachPatternEnum:
    def test_count(self):
        assert len(CoachPattern) == 6

    def test_none(self):
        assert CoachPattern.none.value == "none"

    def test_passive_resistor(self):
        assert CoachPattern.passive_resistor.value == "passive_resistor"

    def test_active_deflector(self):
        assert CoachPattern.active_deflector.value == "active_deflector"

    def test_habit_reverter(self):
        assert CoachPattern.habit_reverter.value == "habit_reverter"

    def test_selective_listener(self):
        assert CoachPattern.selective_listener.value == "selective_listener"

    def test_ghost_committor(self):
        assert CoachPattern.ghost_committor.value == "ghost_committor"

    def test_is_str_enum(self):
        assert isinstance(CoachPattern.none, str)

    def test_all_values_unique(self):
        values = [p.value for p in CoachPattern]
        assert len(values) == len(set(values))


class TestCoachSeverityEnum:
    def test_count(self):
        assert len(CoachSeverity) == 4

    def test_receptive(self):
        assert CoachSeverity.receptive.value == "receptive"

    def test_developing(self):
        assert CoachSeverity.developing.value == "developing"

    def test_resistant(self):
        assert CoachSeverity.resistant.value == "resistant"

    def test_unreachable(self):
        assert CoachSeverity.unreachable.value == "unreachable"

    def test_is_str_enum(self):
        assert isinstance(CoachSeverity.receptive, str)

    def test_all_values_unique(self):
        values = [s.value for s in CoachSeverity]
        assert len(values) == len(set(values))

    def test_members(self):
        names = {s.name for s in CoachSeverity}
        assert names == {"receptive", "developing", "resistant", "unreachable"}


class TestCoachActionEnum:
    def test_count(self):
        assert len(CoachAction) == 7

    def test_no_action(self):
        assert CoachAction.no_action.value == "no_action"

    def test_coaching_check_in(self):
        assert CoachAction.coaching_check_in.value == "coaching_check_in"

    def test_structured_feedback_plan(self):
        assert CoachAction.structured_feedback_plan.value == "structured_feedback_plan"

    def test_behavioral_change_coaching(self):
        assert CoachAction.behavioral_change_coaching.value == "behavioral_change_coaching"

    def test_manager_escalation(self):
        assert CoachAction.manager_escalation.value == "manager_escalation"

    def test_performance_improvement_plan(self):
        assert CoachAction.performance_improvement_plan.value == "performance_improvement_plan"

    def test_leadership_intervention(self):
        assert CoachAction.leadership_intervention.value == "leadership_intervention"

    def test_is_str_enum(self):
        assert isinstance(CoachAction.no_action, str)

    def test_all_values_unique(self):
        values = [a.value for a in CoachAction]
        assert len(values) == len(set(values))


# ══════════════════════════════════════════════════════════════════════════════
# 2. CoachInput FIELDS (22 fields)
# ══════════════════════════════════════════════════════════════════════════════

class TestCoachInputFields:
    def test_field_count(self):
        inp = make_input()
        assert len(inp.__dataclass_fields__) == 22

    def test_rep_id(self):
        inp = make_input(rep_id="X-99")
        assert inp.rep_id == "X-99"

    def test_region(self):
        inp = make_input(region="West")
        assert inp.region == "West"

    def test_evaluation_period_id(self):
        inp = make_input(evaluation_period_id="Q2-2026")
        assert inp.evaluation_period_id == "Q2-2026"

    def test_feedback_implementation_rate_pct(self):
        inp = make_input(feedback_implementation_rate_pct=0.75)
        assert inp.feedback_implementation_rate_pct == 0.75

    def test_skill_improvement_after_coaching(self):
        inp = make_input(skill_improvement_after_coaching=0.33)
        assert inp.skill_improvement_after_coaching == 0.33

    def test_action_item_completion_rate_pct(self):
        inp = make_input(action_item_completion_rate_pct=0.50)
        assert inp.action_item_completion_rate_pct == 0.50

    def test_sessions_attended_rate_pct(self):
        inp = make_input(sessions_attended_rate_pct=0.70)
        assert inp.sessions_attended_rate_pct == 0.70

    def test_voluntary_coaching_requests(self):
        inp = make_input(voluntary_coaching_requests=3)
        assert inp.voluntary_coaching_requests == 3

    def test_reversion_rate_pct(self):
        inp = make_input(reversion_rate_pct=0.20)
        assert inp.reversion_rate_pct == 0.20

    def test_follow_through_score(self):
        inp = make_input(follow_through_score=0.55)
        assert inp.follow_through_score == 0.55

    def test_peer_learning_engagement_pct(self):
        inp = make_input(peer_learning_engagement_pct=0.60)
        assert inp.peer_learning_engagement_pct == 0.60

    def test_call_recording_review_rate_pct(self):
        inp = make_input(call_recording_review_rate_pct=0.40)
        assert inp.call_recording_review_rate_pct == 0.40

    def test_manager_satisfaction_score(self):
        inp = make_input(manager_satisfaction_score=0.65)
        assert inp.manager_satisfaction_score == 0.65

    def test_self_assessment_accuracy_pct(self):
        inp = make_input(self_assessment_accuracy_pct=0.70)
        assert inp.self_assessment_accuracy_pct == 0.70

    def test_improvement_velocity(self):
        inp = make_input(improvement_velocity=0.40)
        assert inp.improvement_velocity == 0.40

    def test_prior_pip_count(self):
        inp = make_input(prior_pip_count=2)
        assert inp.prior_pip_count == 2

    def test_coaching_hours_utilized_pct(self):
        inp = make_input(coaching_hours_utilized_pct=0.55)
        assert inp.coaching_hours_utilized_pct == 0.55

    def test_multi_modal_engagement_pct(self):
        inp = make_input(multi_modal_engagement_pct=0.45)
        assert inp.multi_modal_engagement_pct == 0.45

    def test_challenge_question_rate_pct(self):
        inp = make_input(challenge_question_rate_pct=0.30)
        assert inp.challenge_question_rate_pct == 0.30

    def test_engagement_consistency_pct(self):
        inp = make_input(engagement_consistency_pct=0.75)
        assert inp.engagement_consistency_pct == 0.75

    def test_total_coaching_sessions(self):
        inp = make_input(total_coaching_sessions=20)
        assert inp.total_coaching_sessions == 20

    def test_avg_session_duration_minutes(self):
        inp = make_input(avg_session_duration_minutes=60.0)
        assert inp.avg_session_duration_minutes == 60.0


# ══════════════════════════════════════════════════════════════════════════════
# 3. CoachResult.to_dict() — exactly 15 keys, all serializable
# ══════════════════════════════════════════════════════════════════════════════

class TestCoachResultToDict:
    def _result(self) -> CoachResult:
        engine = fresh_engine()
        return engine.assess(make_input())

    def test_to_dict_key_count(self):
        d = self._result().to_dict()
        assert len(d) == 15

    def test_to_dict_has_rep_id(self):
        d = self._result().to_dict()
        assert "rep_id" in d

    def test_to_dict_has_region(self):
        assert "region" in self._result().to_dict()

    def test_to_dict_has_coach_risk(self):
        assert "coach_risk" in self._result().to_dict()

    def test_to_dict_has_coach_pattern(self):
        assert "coach_pattern" in self._result().to_dict()

    def test_to_dict_has_coach_severity(self):
        assert "coach_severity" in self._result().to_dict()

    def test_to_dict_has_recommended_action(self):
        assert "recommended_action" in self._result().to_dict()

    def test_to_dict_has_receptivity_score(self):
        assert "receptivity_score" in self._result().to_dict()

    def test_to_dict_has_implementation_score(self):
        assert "implementation_score" in self._result().to_dict()

    def test_to_dict_has_engagement_score(self):
        assert "engagement_score" in self._result().to_dict()

    def test_to_dict_has_improvement_score(self):
        assert "improvement_score" in self._result().to_dict()

    def test_to_dict_has_coach_composite(self):
        assert "coach_composite" in self._result().to_dict()

    def test_to_dict_has_has_coach_gap(self):
        assert "has_coach_gap" in self._result().to_dict()

    def test_to_dict_has_requires_coach_intervention(self):
        assert "requires_coach_intervention" in self._result().to_dict()

    def test_to_dict_has_estimated_coaching_waste_usd(self):
        assert "estimated_coaching_waste_usd" in self._result().to_dict()

    def test_to_dict_has_coach_signal(self):
        assert "coach_signal" in self._result().to_dict()

    def test_coach_risk_is_string(self):
        d = self._result().to_dict()
        assert isinstance(d["coach_risk"], str)

    def test_coach_pattern_is_string(self):
        d = self._result().to_dict()
        assert isinstance(d["coach_pattern"], str)

    def test_coach_severity_is_string(self):
        d = self._result().to_dict()
        assert isinstance(d["coach_severity"], str)

    def test_recommended_action_is_string(self):
        d = self._result().to_dict()
        assert isinstance(d["recommended_action"], str)

    def test_receptivity_score_is_number(self):
        d = self._result().to_dict()
        assert isinstance(d["receptivity_score"], (int, float))

    def test_implementation_score_is_number(self):
        d = self._result().to_dict()
        assert isinstance(d["implementation_score"], (int, float))

    def test_engagement_score_is_number(self):
        d = self._result().to_dict()
        assert isinstance(d["engagement_score"], (int, float))

    def test_improvement_score_is_number(self):
        d = self._result().to_dict()
        assert isinstance(d["improvement_score"], (int, float))

    def test_coach_composite_is_number(self):
        d = self._result().to_dict()
        assert isinstance(d["coach_composite"], (int, float))

    def test_has_coach_gap_is_bool(self):
        d = self._result().to_dict()
        assert isinstance(d["has_coach_gap"], bool)

    def test_requires_coach_intervention_is_bool(self):
        d = self._result().to_dict()
        assert isinstance(d["requires_coach_intervention"], bool)

    def test_estimated_coaching_waste_usd_is_number(self):
        d = self._result().to_dict()
        assert isinstance(d["estimated_coaching_waste_usd"], (int, float))

    def test_coach_signal_is_string(self):
        d = self._result().to_dict()
        assert isinstance(d["coach_signal"], str)

    def test_coach_risk_value_is_plain_string_not_enum(self):
        d = self._result().to_dict()
        # should be a plain str, not CoachRisk instance
        assert type(d["coach_risk"]) is str

    def test_coach_pattern_value_is_plain_string(self):
        d = self._result().to_dict()
        assert type(d["coach_pattern"]) is str

    def test_rep_id_matches_input(self):
        engine = fresh_engine()
        inp = make_input(rep_id="TEST-42")
        d = engine.assess(inp).to_dict()
        assert d["rep_id"] == "TEST-42"

    def test_region_matches_input(self):
        engine = fresh_engine()
        inp = make_input(region="SouthWest")
        d = engine.assess(inp).to_dict()
        assert d["region"] == "SouthWest"


# ══════════════════════════════════════════════════════════════════════════════
# 4. Sub-score methods — all boundary conditions
# ══════════════════════════════════════════════════════════════════════════════

class TestReceptivityScore:
    """_receptivity_score: sessions_attended_rate_pct, challenge_question_rate_pct, manager_satisfaction_score"""

    def _score(self, **kw) -> float:
        engine = fresh_engine()
        inp = make_input(**kw)
        return engine._receptivity_score(inp)

    # sessions_attended_rate_pct bands
    def test_sessions_at_or_below_050_adds_40(self):
        s = self._score(sessions_attended_rate_pct=0.50, challenge_question_rate_pct=0.0, manager_satisfaction_score=1.0)
        assert s == 40.0

    def test_sessions_exactly_050(self):
        s = self._score(sessions_attended_rate_pct=0.50, challenge_question_rate_pct=0.0, manager_satisfaction_score=1.0)
        assert s == 40.0

    def test_sessions_below_050(self):
        s = self._score(sessions_attended_rate_pct=0.10, challenge_question_rate_pct=0.0, manager_satisfaction_score=1.0)
        assert s == 40.0

    def test_sessions_between_050_and_070_adds_22(self):
        # > 0.50, <= 0.70
        s = self._score(sessions_attended_rate_pct=0.70, challenge_question_rate_pct=0.0, manager_satisfaction_score=1.0)
        assert s == 22.0

    def test_sessions_just_above_050(self):
        s = self._score(sessions_attended_rate_pct=0.51, challenge_question_rate_pct=0.0, manager_satisfaction_score=1.0)
        assert s == 22.0

    def test_sessions_between_070_and_085_adds_8(self):
        s = self._score(sessions_attended_rate_pct=0.85, challenge_question_rate_pct=0.0, manager_satisfaction_score=1.0)
        assert s == 8.0

    def test_sessions_just_above_070(self):
        s = self._score(sessions_attended_rate_pct=0.71, challenge_question_rate_pct=0.0, manager_satisfaction_score=1.0)
        assert s == 8.0

    def test_sessions_above_085_adds_0(self):
        s = self._score(sessions_attended_rate_pct=0.90, challenge_question_rate_pct=0.0, manager_satisfaction_score=1.0)
        assert s == 0.0

    def test_sessions_exactly_086(self):
        s = self._score(sessions_attended_rate_pct=0.86, challenge_question_rate_pct=0.0, manager_satisfaction_score=1.0)
        assert s == 0.0

    # challenge_question_rate_pct bands
    def test_challenge_at_or_above_060_adds_35(self):
        s = self._score(sessions_attended_rate_pct=0.90, challenge_question_rate_pct=0.60, manager_satisfaction_score=1.0)
        assert s == 35.0

    def test_challenge_above_060_adds_35(self):
        s = self._score(sessions_attended_rate_pct=0.90, challenge_question_rate_pct=0.99, manager_satisfaction_score=1.0)
        assert s == 35.0

    def test_challenge_between_040_and_060_adds_18(self):
        s = self._score(sessions_attended_rate_pct=0.90, challenge_question_rate_pct=0.40, manager_satisfaction_score=1.0)
        assert s == 18.0

    def test_challenge_just_below_060(self):
        s = self._score(sessions_attended_rate_pct=0.90, challenge_question_rate_pct=0.59, manager_satisfaction_score=1.0)
        assert s == 18.0

    def test_challenge_below_040_adds_0(self):
        s = self._score(sessions_attended_rate_pct=0.90, challenge_question_rate_pct=0.39, manager_satisfaction_score=1.0)
        assert s == 0.0

    # manager_satisfaction_score bands
    def test_mgr_sat_at_or_below_035_adds_25(self):
        s = self._score(sessions_attended_rate_pct=0.90, challenge_question_rate_pct=0.0, manager_satisfaction_score=0.35)
        assert s == 25.0

    def test_mgr_sat_below_035_adds_25(self):
        s = self._score(sessions_attended_rate_pct=0.90, challenge_question_rate_pct=0.0, manager_satisfaction_score=0.10)
        assert s == 25.0

    def test_mgr_sat_between_035_and_055_adds_12(self):
        s = self._score(sessions_attended_rate_pct=0.90, challenge_question_rate_pct=0.0, manager_satisfaction_score=0.55)
        assert s == 12.0

    def test_mgr_sat_just_above_035(self):
        s = self._score(sessions_attended_rate_pct=0.90, challenge_question_rate_pct=0.0, manager_satisfaction_score=0.36)
        assert s == 12.0

    def test_mgr_sat_above_055_adds_0(self):
        s = self._score(sessions_attended_rate_pct=0.90, challenge_question_rate_pct=0.0, manager_satisfaction_score=0.56)
        assert s == 0.0

    # cap at 100
    def test_cap_at_100(self):
        s = self._score(sessions_attended_rate_pct=0.10, challenge_question_rate_pct=0.99, manager_satisfaction_score=0.10)
        # 40 + 35 + 25 = 100
        assert s == 100.0

    def test_above_cap_capped(self):
        # can't exceed 100 via these weights (max is exactly 100)
        s = self._score(sessions_attended_rate_pct=0.10, challenge_question_rate_pct=0.99, manager_satisfaction_score=0.10)
        assert s <= 100.0

    def test_all_best_values_give_zero(self):
        s = self._score(sessions_attended_rate_pct=1.0, challenge_question_rate_pct=0.0, manager_satisfaction_score=1.0)
        assert s == 0.0


class TestImplementationScore:
    """_implementation_score: feedback_implementation_rate_pct, action_item_completion_rate_pct, reversion_rate_pct"""

    def _score(self, **kw) -> float:
        engine = fresh_engine()
        return engine._implementation_score(make_input(**kw))

    # feedback_implementation_rate_pct bands
    def test_feedback_at_or_below_030_adds_40(self):
        s = self._score(feedback_implementation_rate_pct=0.30, action_item_completion_rate_pct=1.0, reversion_rate_pct=0.0)
        assert s == 40.0

    def test_feedback_below_030_adds_40(self):
        s = self._score(feedback_implementation_rate_pct=0.10, action_item_completion_rate_pct=1.0, reversion_rate_pct=0.0)
        assert s == 40.0

    def test_feedback_between_030_and_055_adds_22(self):
        s = self._score(feedback_implementation_rate_pct=0.55, action_item_completion_rate_pct=1.0, reversion_rate_pct=0.0)
        assert s == 22.0

    def test_feedback_just_above_030(self):
        s = self._score(feedback_implementation_rate_pct=0.31, action_item_completion_rate_pct=1.0, reversion_rate_pct=0.0)
        assert s == 22.0

    def test_feedback_between_055_and_075_adds_8(self):
        s = self._score(feedback_implementation_rate_pct=0.75, action_item_completion_rate_pct=1.0, reversion_rate_pct=0.0)
        assert s == 8.0

    def test_feedback_just_above_055(self):
        s = self._score(feedback_implementation_rate_pct=0.56, action_item_completion_rate_pct=1.0, reversion_rate_pct=0.0)
        assert s == 8.0

    def test_feedback_above_075_adds_0(self):
        s = self._score(feedback_implementation_rate_pct=0.80, action_item_completion_rate_pct=1.0, reversion_rate_pct=0.0)
        assert s == 0.0

    def test_feedback_exactly_076(self):
        s = self._score(feedback_implementation_rate_pct=0.76, action_item_completion_rate_pct=1.0, reversion_rate_pct=0.0)
        assert s == 0.0

    # action_item_completion_rate_pct bands
    def test_action_at_or_below_040_adds_35(self):
        s = self._score(feedback_implementation_rate_pct=1.0, action_item_completion_rate_pct=0.40, reversion_rate_pct=0.0)
        assert s == 35.0

    def test_action_below_040_adds_35(self):
        s = self._score(feedback_implementation_rate_pct=1.0, action_item_completion_rate_pct=0.10, reversion_rate_pct=0.0)
        assert s == 35.0

    def test_action_between_040_and_065_adds_18(self):
        s = self._score(feedback_implementation_rate_pct=1.0, action_item_completion_rate_pct=0.65, reversion_rate_pct=0.0)
        assert s == 18.0

    def test_action_just_above_040(self):
        s = self._score(feedback_implementation_rate_pct=1.0, action_item_completion_rate_pct=0.41, reversion_rate_pct=0.0)
        assert s == 18.0

    def test_action_above_065_adds_0(self):
        s = self._score(feedback_implementation_rate_pct=1.0, action_item_completion_rate_pct=0.70, reversion_rate_pct=0.0)
        assert s == 0.0

    # reversion_rate_pct bands
    def test_reversion_at_or_above_050_adds_25(self):
        s = self._score(feedback_implementation_rate_pct=1.0, action_item_completion_rate_pct=1.0, reversion_rate_pct=0.50)
        assert s == 25.0

    def test_reversion_above_050_adds_25(self):
        s = self._score(feedback_implementation_rate_pct=1.0, action_item_completion_rate_pct=1.0, reversion_rate_pct=0.90)
        assert s == 25.0

    def test_reversion_between_030_and_050_adds_12(self):
        s = self._score(feedback_implementation_rate_pct=1.0, action_item_completion_rate_pct=1.0, reversion_rate_pct=0.30)
        assert s == 12.0

    def test_reversion_just_below_050(self):
        s = self._score(feedback_implementation_rate_pct=1.0, action_item_completion_rate_pct=1.0, reversion_rate_pct=0.49)
        assert s == 12.0

    def test_reversion_below_030_adds_0(self):
        s = self._score(feedback_implementation_rate_pct=1.0, action_item_completion_rate_pct=1.0, reversion_rate_pct=0.20)
        assert s == 0.0

    def test_cap_at_100(self):
        s = self._score(feedback_implementation_rate_pct=0.10, action_item_completion_rate_pct=0.10, reversion_rate_pct=0.90)
        # 40 + 35 + 25 = 100
        assert s == 100.0

    def test_all_best_gives_zero(self):
        s = self._score(feedback_implementation_rate_pct=1.0, action_item_completion_rate_pct=1.0, reversion_rate_pct=0.0)
        assert s == 0.0


class TestEngagementScore:
    """_engagement_score: coaching_hours_utilized_pct, call_recording_review_rate_pct, peer_learning_engagement_pct"""

    def _score(self, **kw) -> float:
        engine = fresh_engine()
        return engine._engagement_score(make_input(**kw))

    # coaching_hours_utilized_pct bands
    def test_hours_at_or_below_040_adds_40(self):
        s = self._score(coaching_hours_utilized_pct=0.40, call_recording_review_rate_pct=1.0, peer_learning_engagement_pct=1.0)
        assert s == 40.0

    def test_hours_below_040_adds_40(self):
        s = self._score(coaching_hours_utilized_pct=0.10, call_recording_review_rate_pct=1.0, peer_learning_engagement_pct=1.0)
        assert s == 40.0

    def test_hours_between_040_and_060_adds_22(self):
        s = self._score(coaching_hours_utilized_pct=0.60, call_recording_review_rate_pct=1.0, peer_learning_engagement_pct=1.0)
        assert s == 22.0

    def test_hours_just_above_040(self):
        s = self._score(coaching_hours_utilized_pct=0.41, call_recording_review_rate_pct=1.0, peer_learning_engagement_pct=1.0)
        assert s == 22.0

    def test_hours_between_060_and_080_adds_8(self):
        s = self._score(coaching_hours_utilized_pct=0.80, call_recording_review_rate_pct=1.0, peer_learning_engagement_pct=1.0)
        assert s == 8.0

    def test_hours_just_above_060(self):
        s = self._score(coaching_hours_utilized_pct=0.61, call_recording_review_rate_pct=1.0, peer_learning_engagement_pct=1.0)
        assert s == 8.0

    def test_hours_above_080_adds_0(self):
        s = self._score(coaching_hours_utilized_pct=0.85, call_recording_review_rate_pct=1.0, peer_learning_engagement_pct=1.0)
        assert s == 0.0

    # call_recording_review_rate_pct bands
    def test_recording_at_or_below_025_adds_35(self):
        s = self._score(coaching_hours_utilized_pct=1.0, call_recording_review_rate_pct=0.25, peer_learning_engagement_pct=1.0)
        assert s == 35.0

    def test_recording_below_025_adds_35(self):
        s = self._score(coaching_hours_utilized_pct=1.0, call_recording_review_rate_pct=0.10, peer_learning_engagement_pct=1.0)
        assert s == 35.0

    def test_recording_between_025_and_050_adds_18(self):
        s = self._score(coaching_hours_utilized_pct=1.0, call_recording_review_rate_pct=0.50, peer_learning_engagement_pct=1.0)
        assert s == 18.0

    def test_recording_just_above_025(self):
        s = self._score(coaching_hours_utilized_pct=1.0, call_recording_review_rate_pct=0.26, peer_learning_engagement_pct=1.0)
        assert s == 18.0

    def test_recording_above_050_adds_0(self):
        s = self._score(coaching_hours_utilized_pct=1.0, call_recording_review_rate_pct=0.55, peer_learning_engagement_pct=1.0)
        assert s == 0.0

    # peer_learning_engagement_pct bands
    def test_peer_at_or_below_020_adds_25(self):
        s = self._score(coaching_hours_utilized_pct=1.0, call_recording_review_rate_pct=1.0, peer_learning_engagement_pct=0.20)
        assert s == 25.0

    def test_peer_below_020_adds_25(self):
        s = self._score(coaching_hours_utilized_pct=1.0, call_recording_review_rate_pct=1.0, peer_learning_engagement_pct=0.05)
        assert s == 25.0

    def test_peer_between_020_and_045_adds_12(self):
        s = self._score(coaching_hours_utilized_pct=1.0, call_recording_review_rate_pct=1.0, peer_learning_engagement_pct=0.45)
        assert s == 12.0

    def test_peer_just_above_020(self):
        s = self._score(coaching_hours_utilized_pct=1.0, call_recording_review_rate_pct=1.0, peer_learning_engagement_pct=0.21)
        assert s == 12.0

    def test_peer_above_045_adds_0(self):
        s = self._score(coaching_hours_utilized_pct=1.0, call_recording_review_rate_pct=1.0, peer_learning_engagement_pct=0.50)
        assert s == 0.0

    def test_cap_at_100(self):
        s = self._score(coaching_hours_utilized_pct=0.10, call_recording_review_rate_pct=0.10, peer_learning_engagement_pct=0.10)
        # 40 + 35 + 25 = 100
        assert s == 100.0

    def test_all_best_gives_zero(self):
        s = self._score(coaching_hours_utilized_pct=1.0, call_recording_review_rate_pct=1.0, peer_learning_engagement_pct=1.0)
        assert s == 0.0


class TestImprovementScore:
    """_improvement_score: skill_improvement_after_coaching, improvement_velocity, follow_through_score"""

    def _score(self, **kw) -> float:
        engine = fresh_engine()
        return engine._improvement_score(make_input(**kw))

    # skill_improvement_after_coaching bands
    def test_skill_at_or_below_010_adds_45(self):
        s = self._score(skill_improvement_after_coaching=0.10, improvement_velocity=1.0, follow_through_score=1.0)
        assert s == 45.0

    def test_skill_below_010_adds_45(self):
        s = self._score(skill_improvement_after_coaching=0.05, improvement_velocity=1.0, follow_through_score=1.0)
        assert s == 45.0

    def test_skill_between_010_and_025_adds_25(self):
        s = self._score(skill_improvement_after_coaching=0.25, improvement_velocity=1.0, follow_through_score=1.0)
        assert s == 25.0

    def test_skill_just_above_010(self):
        s = self._score(skill_improvement_after_coaching=0.11, improvement_velocity=1.0, follow_through_score=1.0)
        assert s == 25.0

    def test_skill_between_025_and_045_adds_10(self):
        s = self._score(skill_improvement_after_coaching=0.45, improvement_velocity=1.0, follow_through_score=1.0)
        assert s == 10.0

    def test_skill_just_above_025(self):
        s = self._score(skill_improvement_after_coaching=0.26, improvement_velocity=1.0, follow_through_score=1.0)
        assert s == 10.0

    def test_skill_above_045_adds_0(self):
        s = self._score(skill_improvement_after_coaching=0.60, improvement_velocity=1.0, follow_through_score=1.0)
        assert s == 0.0

    # improvement_velocity bands
    def test_velocity_at_or_below_010_adds_30(self):
        s = self._score(skill_improvement_after_coaching=1.0, improvement_velocity=0.10, follow_through_score=1.0)
        assert s == 30.0

    def test_velocity_below_010_adds_30(self):
        s = self._score(skill_improvement_after_coaching=1.0, improvement_velocity=0.05, follow_through_score=1.0)
        assert s == 30.0

    def test_velocity_between_010_and_025_adds_15(self):
        s = self._score(skill_improvement_after_coaching=1.0, improvement_velocity=0.25, follow_through_score=1.0)
        assert s == 15.0

    def test_velocity_just_above_010(self):
        s = self._score(skill_improvement_after_coaching=1.0, improvement_velocity=0.11, follow_through_score=1.0)
        assert s == 15.0

    def test_velocity_above_025_adds_0(self):
        s = self._score(skill_improvement_after_coaching=1.0, improvement_velocity=0.30, follow_through_score=1.0)
        assert s == 0.0

    # follow_through_score bands
    def test_follow_at_or_below_025_adds_25(self):
        s = self._score(skill_improvement_after_coaching=1.0, improvement_velocity=1.0, follow_through_score=0.25)
        assert s == 25.0

    def test_follow_below_025_adds_25(self):
        s = self._score(skill_improvement_after_coaching=1.0, improvement_velocity=1.0, follow_through_score=0.10)
        assert s == 25.0

    def test_follow_between_025_and_050_adds_12(self):
        s = self._score(skill_improvement_after_coaching=1.0, improvement_velocity=1.0, follow_through_score=0.50)
        assert s == 12.0

    def test_follow_just_above_025(self):
        s = self._score(skill_improvement_after_coaching=1.0, improvement_velocity=1.0, follow_through_score=0.26)
        assert s == 12.0

    def test_follow_above_050_adds_0(self):
        s = self._score(skill_improvement_after_coaching=1.0, improvement_velocity=1.0, follow_through_score=0.60)
        assert s == 0.0

    def test_cap_at_100(self):
        s = self._score(skill_improvement_after_coaching=0.0, improvement_velocity=0.0, follow_through_score=0.0)
        # 45 + 30 + 25 = 100
        assert s == 100.0

    def test_all_best_gives_zero(self):
        s = self._score(skill_improvement_after_coaching=1.0, improvement_velocity=1.0, follow_through_score=1.0)
        assert s == 0.0


# ══════════════════════════════════════════════════════════════════════════════
# 5. Composite formula — weights 0.30 + 0.30 + 0.20 + 0.20 = 1.00
# ══════════════════════════════════════════════════════════════════════════════

class TestComposite:
    def _engine(self):
        return fresh_engine()

    def test_weights_sum_to_one(self):
        assert 0.30 + 0.30 + 0.20 + 0.20 == pytest.approx(1.00)

    def test_all_zeros_gives_zero(self):
        e = self._engine()
        assert e._composite(0, 0, 0, 0) == 0.0

    def test_all_100_gives_100(self):
        e = self._engine()
        assert e._composite(100, 100, 100, 100) == 100.0

    def test_formula_exact(self):
        e = self._engine()
        result = e._composite(40, 60, 80, 20)
        expected = round(40 * 0.30 + 60 * 0.30 + 80 * 0.20 + 20 * 0.20, 2)
        assert result == expected

    def test_formula_re_weight(self):
        e = self._engine()
        # only receptivity non-zero: 50 * 0.30 = 15
        assert e._composite(50, 0, 0, 0) == 15.0

    def test_formula_im_weight(self):
        e = self._engine()
        # only implementation non-zero: 50 * 0.30 = 15
        assert e._composite(0, 50, 0, 0) == 15.0

    def test_formula_en_weight(self):
        e = self._engine()
        # only engagement non-zero: 50 * 0.20 = 10
        assert e._composite(0, 0, 50, 0) == 10.0

    def test_formula_ip_weight(self):
        e = self._engine()
        # only improvement non-zero: 50 * 0.20 = 10
        assert e._composite(0, 0, 0, 50) == 10.0

    def test_capped_at_100(self):
        e = self._engine()
        assert e._composite(200, 200, 200, 200) == 100.0

    def test_result_is_rounded_to_2dp(self):
        e = self._engine()
        val = e._composite(33, 33, 33, 33)
        # 33*0.30 + 33*0.30 + 33*0.20 + 33*0.20 = 33.0 exactly
        assert val == round(val, 2)

    def test_composite_non_negative(self):
        e = self._engine()
        assert e._composite(0, 0, 0, 0) >= 0.0


# ══════════════════════════════════════════════════════════════════════════════
# 6. Risk / Severity / Action thresholds
# ══════════════════════════════════════════════════════════════════════════════

class TestRiskThresholds:
    def _risk(self, composite):
        return fresh_engine()._risk(composite)

    def test_composite_0_is_low(self):
        assert self._risk(0) == CoachRisk.low

    def test_composite_19_is_low(self):
        assert self._risk(19) == CoachRisk.low

    def test_composite_19_99_is_low(self):
        assert self._risk(19.99) == CoachRisk.low

    def test_composite_20_is_moderate(self):
        assert self._risk(20) == CoachRisk.moderate

    def test_composite_39_is_moderate(self):
        assert self._risk(39) == CoachRisk.moderate

    def test_composite_39_99_is_moderate(self):
        assert self._risk(39.99) == CoachRisk.moderate

    def test_composite_40_is_high(self):
        assert self._risk(40) == CoachRisk.high

    def test_composite_59_is_high(self):
        assert self._risk(59) == CoachRisk.high

    def test_composite_59_99_is_high(self):
        assert self._risk(59.99) == CoachRisk.high

    def test_composite_60_is_critical(self):
        assert self._risk(60) == CoachRisk.critical

    def test_composite_100_is_critical(self):
        assert self._risk(100) == CoachRisk.critical


class TestSeverityThresholds:
    def _sev(self, composite):
        return fresh_engine()._severity(composite)

    def test_composite_0_is_receptive(self):
        assert self._sev(0) == CoachSeverity.receptive

    def test_composite_19_is_receptive(self):
        assert self._sev(19) == CoachSeverity.receptive

    def test_composite_20_is_developing(self):
        assert self._sev(20) == CoachSeverity.developing

    def test_composite_39_is_developing(self):
        assert self._sev(39) == CoachSeverity.developing

    def test_composite_40_is_resistant(self):
        assert self._sev(40) == CoachSeverity.resistant

    def test_composite_59_is_resistant(self):
        assert self._sev(59) == CoachSeverity.resistant

    def test_composite_60_is_unreachable(self):
        assert self._sev(60) == CoachSeverity.unreachable

    def test_composite_100_is_unreachable(self):
        assert self._sev(100) == CoachSeverity.unreachable

    def test_risk_and_severity_thresholds_aligned(self):
        # They share the same cut-points; verify symmetry
        e = fresh_engine()
        for val in [0, 19, 20, 39, 40, 59, 60, 100]:
            risk = e._risk(val)
            sev = e._severity(val)
            assert (risk == CoachRisk.low) == (sev == CoachSeverity.receptive)
            assert (risk == CoachRisk.moderate) == (sev == CoachSeverity.developing)
            assert (risk == CoachRisk.high) == (sev == CoachSeverity.resistant)
            assert (risk == CoachRisk.critical) == (sev == CoachSeverity.unreachable)


class TestActionThresholds:
    def _action(self, risk, pattern=CoachPattern.none):
        return fresh_engine()._action(risk, pattern)

    # low risk
    def test_low_risk_any_pattern_gives_no_action(self):
        assert self._action(CoachRisk.low) == CoachAction.no_action

    def test_low_risk_passive_resistor_gives_no_action(self):
        assert self._action(CoachRisk.low, CoachPattern.passive_resistor) == CoachAction.no_action

    # moderate risk
    def test_moderate_risk_gives_check_in(self):
        assert self._action(CoachRisk.moderate) == CoachAction.coaching_check_in

    def test_moderate_risk_passive_resistor_gives_check_in(self):
        assert self._action(CoachRisk.moderate, CoachPattern.passive_resistor) == CoachAction.coaching_check_in

    def test_moderate_risk_ghost_committor_gives_check_in(self):
        assert self._action(CoachRisk.moderate, CoachPattern.ghost_committor) == CoachAction.coaching_check_in

    # high risk
    def test_high_risk_passive_resistor_gives_manager_escalation(self):
        assert self._action(CoachRisk.high, CoachPattern.passive_resistor) == CoachAction.manager_escalation

    def test_high_risk_active_deflector_gives_behavioral_change(self):
        assert self._action(CoachRisk.high, CoachPattern.active_deflector) == CoachAction.behavioral_change_coaching

    def test_high_risk_habit_reverter_gives_structured_plan(self):
        assert self._action(CoachRisk.high, CoachPattern.habit_reverter) == CoachAction.structured_feedback_plan

    def test_high_risk_selective_listener_gives_structured_plan(self):
        assert self._action(CoachRisk.high, CoachPattern.selective_listener) == CoachAction.structured_feedback_plan

    def test_high_risk_ghost_committor_gives_manager_escalation(self):
        assert self._action(CoachRisk.high, CoachPattern.ghost_committor) == CoachAction.manager_escalation

    def test_high_risk_none_gives_behavioral_change(self):
        assert self._action(CoachRisk.high, CoachPattern.none) == CoachAction.behavioral_change_coaching

    # critical risk
    def test_critical_passive_resistor_gives_leadership_intervention(self):
        assert self._action(CoachRisk.critical, CoachPattern.passive_resistor) == CoachAction.leadership_intervention

    def test_critical_active_deflector_gives_leadership_intervention(self):
        assert self._action(CoachRisk.critical, CoachPattern.active_deflector) == CoachAction.leadership_intervention

    def test_critical_habit_reverter_gives_pip(self):
        assert self._action(CoachRisk.critical, CoachPattern.habit_reverter) == CoachAction.performance_improvement_plan

    def test_critical_selective_listener_gives_pip(self):
        assert self._action(CoachRisk.critical, CoachPattern.selective_listener) == CoachAction.performance_improvement_plan

    def test_critical_ghost_committor_gives_pip(self):
        assert self._action(CoachRisk.critical, CoachPattern.ghost_committor) == CoachAction.performance_improvement_plan

    def test_critical_none_gives_pip(self):
        assert self._action(CoachRisk.critical, CoachPattern.none) == CoachAction.performance_improvement_plan


# ══════════════════════════════════════════════════════════════════════════════
# 7. Pattern detection logic — all 6 patterns
# ══════════════════════════════════════════════════════════════════════════════

class TestPatternDetection:
    def _pattern(self, **kw) -> CoachPattern:
        engine = fresh_engine()
        return engine._pattern(make_input(**kw))

    # passive_resistor: sessions_attended_rate_pct <= 0.55 AND manager_satisfaction_score <= 0.40
    def test_passive_resistor_exact_boundary(self):
        p = self._pattern(sessions_attended_rate_pct=0.55, manager_satisfaction_score=0.40,
                          challenge_question_rate_pct=0.0, action_item_completion_rate_pct=1.0,
                          feedback_implementation_rate_pct=0.0, reversion_rate_pct=0.0,
                          skill_improvement_after_coaching=1.0, follow_through_score=1.0)
        assert p == CoachPattern.passive_resistor

    def test_passive_resistor_low_values(self):
        p = self._pattern(sessions_attended_rate_pct=0.30, manager_satisfaction_score=0.20,
                          challenge_question_rate_pct=0.0, action_item_completion_rate_pct=1.0,
                          feedback_implementation_rate_pct=0.0, reversion_rate_pct=0.0,
                          skill_improvement_after_coaching=1.0, follow_through_score=1.0)
        assert p == CoachPattern.passive_resistor

    def test_passive_resistor_fails_when_sessions_too_high(self):
        p = self._pattern(sessions_attended_rate_pct=0.56, manager_satisfaction_score=0.40,
                          challenge_question_rate_pct=0.0, action_item_completion_rate_pct=1.0,
                          feedback_implementation_rate_pct=0.0, reversion_rate_pct=0.0,
                          skill_improvement_after_coaching=1.0, follow_through_score=1.0)
        assert p != CoachPattern.passive_resistor

    def test_passive_resistor_fails_when_mgr_sat_too_high(self):
        p = self._pattern(sessions_attended_rate_pct=0.55, manager_satisfaction_score=0.41,
                          challenge_question_rate_pct=0.0, action_item_completion_rate_pct=1.0,
                          feedback_implementation_rate_pct=0.0, reversion_rate_pct=0.0,
                          skill_improvement_after_coaching=1.0, follow_through_score=1.0)
        assert p != CoachPattern.passive_resistor

    # active_deflector: challenge_question_rate_pct >= 0.55 AND action_item_completion_rate_pct <= 0.45
    def test_active_deflector_exact_boundary(self):
        p = self._pattern(sessions_attended_rate_pct=0.80, manager_satisfaction_score=0.80,
                          challenge_question_rate_pct=0.55, action_item_completion_rate_pct=0.45,
                          feedback_implementation_rate_pct=0.0, reversion_rate_pct=0.0,
                          skill_improvement_after_coaching=1.0, follow_through_score=1.0)
        assert p == CoachPattern.active_deflector

    def test_active_deflector_strong_values(self):
        p = self._pattern(sessions_attended_rate_pct=0.80, manager_satisfaction_score=0.80,
                          challenge_question_rate_pct=0.90, action_item_completion_rate_pct=0.20,
                          feedback_implementation_rate_pct=0.0, reversion_rate_pct=0.0,
                          skill_improvement_after_coaching=1.0, follow_through_score=1.0)
        assert p == CoachPattern.active_deflector

    def test_active_deflector_fails_when_challenge_too_low(self):
        p = self._pattern(sessions_attended_rate_pct=0.80, manager_satisfaction_score=0.80,
                          challenge_question_rate_pct=0.54, action_item_completion_rate_pct=0.45,
                          feedback_implementation_rate_pct=1.0, reversion_rate_pct=0.0,
                          skill_improvement_after_coaching=1.0, follow_through_score=1.0)
        # may be none or another pattern, but not active_deflector
        assert p != CoachPattern.active_deflector

    def test_active_deflector_fails_when_action_too_high(self):
        p = self._pattern(sessions_attended_rate_pct=0.80, manager_satisfaction_score=0.80,
                          challenge_question_rate_pct=0.55, action_item_completion_rate_pct=0.46,
                          feedback_implementation_rate_pct=1.0, reversion_rate_pct=0.0,
                          skill_improvement_after_coaching=1.0, follow_through_score=1.0)
        assert p != CoachPattern.active_deflector

    # habit_reverter: feedback_implementation_rate_pct >= 0.55 AND reversion_rate_pct >= 0.45
    def test_habit_reverter_exact_boundary(self):
        p = self._pattern(sessions_attended_rate_pct=0.80, manager_satisfaction_score=0.80,
                          challenge_question_rate_pct=0.0, action_item_completion_rate_pct=1.0,
                          feedback_implementation_rate_pct=0.55, reversion_rate_pct=0.45,
                          skill_improvement_after_coaching=1.0, follow_through_score=1.0)
        assert p == CoachPattern.habit_reverter

    def test_habit_reverter_strong_values(self):
        p = self._pattern(sessions_attended_rate_pct=0.80, manager_satisfaction_score=0.80,
                          challenge_question_rate_pct=0.0, action_item_completion_rate_pct=1.0,
                          feedback_implementation_rate_pct=0.90, reversion_rate_pct=0.80,
                          skill_improvement_after_coaching=1.0, follow_through_score=1.0)
        assert p == CoachPattern.habit_reverter

    def test_habit_reverter_fails_when_feedback_too_low(self):
        p = self._pattern(sessions_attended_rate_pct=0.80, manager_satisfaction_score=0.80,
                          challenge_question_rate_pct=0.0, action_item_completion_rate_pct=1.0,
                          feedback_implementation_rate_pct=0.54, reversion_rate_pct=0.90,
                          skill_improvement_after_coaching=1.0, follow_through_score=1.0)
        assert p != CoachPattern.habit_reverter

    def test_habit_reverter_fails_when_reversion_too_low(self):
        p = self._pattern(sessions_attended_rate_pct=0.80, manager_satisfaction_score=0.80,
                          challenge_question_rate_pct=0.0, action_item_completion_rate_pct=1.0,
                          feedback_implementation_rate_pct=0.90, reversion_rate_pct=0.44,
                          skill_improvement_after_coaching=1.0, follow_through_score=1.0)
        assert p != CoachPattern.habit_reverter

    # selective_listener: sessions_attended_rate_pct >= 0.80 AND skill_improvement_after_coaching <= 0.15
    def test_selective_listener_exact_boundary(self):
        p = self._pattern(sessions_attended_rate_pct=0.80, manager_satisfaction_score=0.80,
                          challenge_question_rate_pct=0.0, action_item_completion_rate_pct=1.0,
                          feedback_implementation_rate_pct=0.0, reversion_rate_pct=0.0,
                          skill_improvement_after_coaching=0.15, follow_through_score=1.0)
        assert p == CoachPattern.selective_listener

    def test_selective_listener_strong_values(self):
        p = self._pattern(sessions_attended_rate_pct=1.0, manager_satisfaction_score=0.80,
                          challenge_question_rate_pct=0.0, action_item_completion_rate_pct=1.0,
                          feedback_implementation_rate_pct=0.0, reversion_rate_pct=0.0,
                          skill_improvement_after_coaching=0.05, follow_through_score=1.0)
        assert p == CoachPattern.selective_listener

    def test_selective_listener_fails_when_sessions_too_low(self):
        p = self._pattern(sessions_attended_rate_pct=0.79, manager_satisfaction_score=0.80,
                          challenge_question_rate_pct=0.0, action_item_completion_rate_pct=1.0,
                          feedback_implementation_rate_pct=0.0, reversion_rate_pct=0.0,
                          skill_improvement_after_coaching=0.15, follow_through_score=1.0)
        assert p != CoachPattern.selective_listener

    def test_selective_listener_fails_when_skill_too_high(self):
        p = self._pattern(sessions_attended_rate_pct=0.80, manager_satisfaction_score=0.80,
                          challenge_question_rate_pct=0.0, action_item_completion_rate_pct=1.0,
                          feedback_implementation_rate_pct=0.0, reversion_rate_pct=0.0,
                          skill_improvement_after_coaching=0.16, follow_through_score=1.0)
        assert p != CoachPattern.selective_listener

    # ghost_committor: action_item_completion_rate_pct <= 0.30 AND follow_through_score <= 0.25
    def test_ghost_committor_exact_boundary(self):
        p = self._pattern(sessions_attended_rate_pct=0.80, manager_satisfaction_score=0.80,
                          challenge_question_rate_pct=0.0, action_item_completion_rate_pct=0.30,
                          feedback_implementation_rate_pct=1.0, reversion_rate_pct=0.0,
                          skill_improvement_after_coaching=1.0, follow_through_score=0.25)
        assert p == CoachPattern.ghost_committor

    def test_ghost_committor_strong_values(self):
        p = self._pattern(sessions_attended_rate_pct=0.80, manager_satisfaction_score=0.80,
                          challenge_question_rate_pct=0.0, action_item_completion_rate_pct=0.10,
                          feedback_implementation_rate_pct=1.0, reversion_rate_pct=0.0,
                          skill_improvement_after_coaching=1.0, follow_through_score=0.10)
        assert p == CoachPattern.ghost_committor

    def test_ghost_committor_fails_when_action_too_high(self):
        p = self._pattern(sessions_attended_rate_pct=0.80, manager_satisfaction_score=0.80,
                          challenge_question_rate_pct=0.0, action_item_completion_rate_pct=0.31,
                          feedback_implementation_rate_pct=1.0, reversion_rate_pct=0.0,
                          skill_improvement_after_coaching=1.0, follow_through_score=0.25)
        assert p != CoachPattern.ghost_committor

    def test_ghost_committor_fails_when_follow_too_high(self):
        p = self._pattern(sessions_attended_rate_pct=0.80, manager_satisfaction_score=0.80,
                          challenge_question_rate_pct=0.0, action_item_completion_rate_pct=0.30,
                          feedback_implementation_rate_pct=1.0, reversion_rate_pct=0.0,
                          skill_improvement_after_coaching=1.0, follow_through_score=0.26)
        assert p != CoachPattern.ghost_committor

    # none pattern
    def test_none_pattern_when_all_good(self):
        p = self._pattern()  # uses all-good defaults
        assert p == CoachPattern.none

    def test_none_pattern_priority_passive_resistor_wins(self):
        # Passive resistor conditions checked first
        p = self._pattern(sessions_attended_rate_pct=0.50, manager_satisfaction_score=0.35,
                          challenge_question_rate_pct=0.55, action_item_completion_rate_pct=0.45)
        assert p == CoachPattern.passive_resistor


# ══════════════════════════════════════════════════════════════════════════════
# 8. has_coach_gap flag (3 OR conditions)
# ══════════════════════════════════════════════════════════════════════════════

class TestHasCoachGap:
    def _gap(self, **kw) -> bool:
        engine = fresh_engine()
        inp = make_input(**kw)
        re  = engine._receptivity_score(inp)
        im  = engine._implementation_score(inp)
        en  = engine._engagement_score(inp)
        ip  = engine._improvement_score(inp)
        comp = engine._composite(re, im, en, ip)
        return engine._has_gap(inp, comp)

    def _gap_direct(self, composite, feedback_impl, action_item) -> bool:
        engine = fresh_engine()
        inp = make_input(
            feedback_implementation_rate_pct=feedback_impl,
            action_item_completion_rate_pct=action_item,
        )
        return engine._has_gap(inp, composite)

    # condition 1: composite >= 40
    def test_gap_true_when_composite_ge_40(self):
        assert self._gap_direct(40, 1.0, 1.0) is True

    def test_gap_true_when_composite_above_40(self):
        assert self._gap_direct(60, 1.0, 1.0) is True

    def test_gap_false_from_composite_when_below_40_and_others_high(self):
        # composite < 40, feedback > 0.60, action > 0.55 → False
        assert self._gap_direct(10, 0.80, 0.80) is False

    # condition 2: feedback_implementation_rate_pct <= 0.60
    def test_gap_true_when_feedback_impl_le_060(self):
        assert self._gap_direct(10, 0.60, 0.80) is True

    def test_gap_true_when_feedback_impl_below_060(self):
        assert self._gap_direct(10, 0.30, 0.80) is True

    def test_gap_false_when_feedback_impl_above_060(self):
        assert self._gap_direct(10, 0.61, 0.80) is False

    # condition 3: action_item_completion_rate_pct <= 0.55
    def test_gap_true_when_action_item_le_055(self):
        assert self._gap_direct(10, 0.80, 0.55) is True

    def test_gap_true_when_action_item_below_055(self):
        assert self._gap_direct(10, 0.80, 0.30) is True

    def test_gap_false_when_action_item_above_055(self):
        assert self._gap_direct(10, 0.80, 0.56) is False

    # all good → False
    def test_gap_false_when_all_conditions_unmet(self):
        assert self._gap_direct(10, 0.80, 0.80) is False

    # multiple conditions true → True
    def test_gap_true_when_all_three_conditions_met(self):
        assert self._gap_direct(50, 0.30, 0.30) is True


# ══════════════════════════════════════════════════════════════════════════════
# 9. requires_coach_intervention flag (3 OR conditions)
# ══════════════════════════════════════════════════════════════════════════════

class TestRequiresCoachIntervention:
    def _intervention_direct(self, composite, reversion, mgr_sat) -> bool:
        engine = fresh_engine()
        inp = make_input(reversion_rate_pct=reversion, manager_satisfaction_score=mgr_sat)
        return engine._requires_intervention(inp, composite)

    # condition 1: composite >= 25
    def test_intervention_true_when_composite_ge_25(self):
        assert self._intervention_direct(25, 0.0, 1.0) is True

    def test_intervention_true_when_composite_above_25(self):
        assert self._intervention_direct(50, 0.0, 1.0) is True

    def test_intervention_false_from_composite_alone_when_below_25(self):
        assert self._intervention_direct(10, 0.0, 1.0) is False

    # condition 2: reversion_rate_pct >= 0.30
    def test_intervention_true_when_reversion_ge_030(self):
        assert self._intervention_direct(10, 0.30, 1.0) is True

    def test_intervention_true_when_reversion_above_030(self):
        assert self._intervention_direct(10, 0.70, 1.0) is True

    def test_intervention_false_when_reversion_below_030(self):
        assert self._intervention_direct(10, 0.29, 1.0) is False

    # condition 3: manager_satisfaction_score <= 0.55
    def test_intervention_true_when_mgr_sat_le_055(self):
        assert self._intervention_direct(10, 0.0, 0.55) is True

    def test_intervention_true_when_mgr_sat_below_055(self):
        assert self._intervention_direct(10, 0.0, 0.20) is True

    def test_intervention_false_when_mgr_sat_above_055(self):
        assert self._intervention_direct(10, 0.0, 0.56) is False

    # all conditions unmet → False
    def test_intervention_false_when_all_conditions_unmet(self):
        assert self._intervention_direct(10, 0.10, 0.80) is False

    # multiple conditions → True
    def test_intervention_true_when_all_three_met(self):
        assert self._intervention_direct(30, 0.50, 0.30) is True


# ══════════════════════════════════════════════════════════════════════════════
# 10. estimated_coaching_waste_usd formula
# ══════════════════════════════════════════════════════════════════════════════

class TestCoachingWaste:
    AVG_COST = 500.0

    def _waste(self, sessions, composite, feedback_impl) -> float:
        engine = fresh_engine()
        inp = make_input(total_coaching_sessions=sessions,
                         feedback_implementation_rate_pct=feedback_impl)
        return engine._coaching_waste(inp, composite)

    def test_zero_sessions_gives_zero(self):
        assert self._waste(0, 50, 0.50) == 0.0

    def test_zero_composite_gives_zero(self):
        assert self._waste(10, 0, 0.50) == 0.0

    def test_full_implementation_gives_zero(self):
        # waste_rate = (comp/100) * (1 - 1.0) = 0
        assert self._waste(10, 50, 1.0) == 0.0

    def test_formula_exact_calculation(self):
        # sessions=10, composite=50, feedback_impl=0.50
        # waste_rate = (50/100) * (1 - 0.50) = 0.5 * 0.5 = 0.25
        # waste = 10 * 500 * 0.25 = 1250.0
        result = self._waste(10, 50, 0.50)
        assert result == pytest.approx(1250.0)

    def test_formula_another_case(self):
        # sessions=20, composite=60, feedback_impl=0.30
        # waste_rate = 0.60 * 0.70 = 0.42
        # waste = 20 * 500 * 0.42 = 4200.0
        result = self._waste(20, 60, 0.30)
        assert result == pytest.approx(4200.0)

    def test_result_is_rounded_to_2dp(self):
        result = self._waste(7, 33, 0.33)
        assert result == round(result, 2)

    def test_waste_non_negative(self):
        for sessions in [0, 1, 5, 20]:
            for comp in [0, 25, 50, 75, 100]:
                for impl in [0.0, 0.5, 1.0]:
                    assert self._waste(sessions, comp, impl) >= 0.0

    def test_high_sessions_high_composite_zero_impl(self):
        # sessions=100, composite=100, feedback_impl=0.0
        # waste_rate = 1.0 * 1.0 = 1.0
        # waste = 100 * 500 * 1.0 = 50000.0
        result = self._waste(100, 100, 0.0)
        assert result == pytest.approx(50000.0)

    def test_avg_cost_per_session_is_500(self):
        # Verified by formula: sessions=1, composite=100, impl=0.0 → 1 * 500 * 1.0 = 500
        result = self._waste(1, 100, 0.0)
        assert result == pytest.approx(500.0)


# ══════════════════════════════════════════════════════════════════════════════
# 11. _signal output for low and high composite
# ══════════════════════════════════════════════════════════════════════════════

class TestSignal:
    def _signal(self, pattern: CoachPattern, composite: float, **inp_kw) -> str:
        engine = fresh_engine()
        inp = make_input(**inp_kw)
        return engine._signal(inp, pattern, composite)

    def test_low_composite_returns_strong_signal(self):
        sig = self._signal(CoachPattern.none, 10.0)
        assert "strong" in sig.lower()

    def test_low_composite_mentions_implementation(self):
        sig = self._signal(CoachPattern.none, 0.0)
        assert "implementation" in sig.lower()

    def test_low_composite_mentions_engagement(self):
        sig = self._signal(CoachPattern.none, 19.99)
        assert "engagement" in sig.lower()

    def test_low_composite_threshold_exactly_19(self):
        sig = self._signal(CoachPattern.none, 19.0)
        assert "strong" in sig.lower()

    def test_low_composite_at_0(self):
        sig = self._signal(CoachPattern.none, 0.0)
        assert "Coaching receptivity strong" in sig

    def test_high_composite_contains_label(self):
        sig = self._signal(CoachPattern.passive_resistor, 50.0)
        assert "Passive resistor" in sig

    def test_high_composite_active_deflector_label(self):
        sig = self._signal(CoachPattern.active_deflector, 50.0)
        assert "Active deflector" in sig

    def test_high_composite_habit_reverter_label(self):
        sig = self._signal(CoachPattern.habit_reverter, 50.0)
        assert "Habit reverter" in sig

    def test_high_composite_selective_listener_label(self):
        sig = self._signal(CoachPattern.selective_listener, 50.0)
        assert "Selective listener" in sig

    def test_high_composite_ghost_committor_label(self):
        sig = self._signal(CoachPattern.ghost_committor, 50.0)
        assert "Ghost committor" in sig

    def test_high_composite_contains_feedback_pct(self):
        sig = self._signal(CoachPattern.passive_resistor, 50.0,
                           feedback_implementation_rate_pct=0.75)
        assert "75%" in sig

    def test_high_composite_contains_sessions_pct(self):
        sig = self._signal(CoachPattern.passive_resistor, 50.0,
                           sessions_attended_rate_pct=0.80)
        assert "80%" in sig

    def test_high_composite_contains_reversion_pct(self):
        sig = self._signal(CoachPattern.passive_resistor, 50.0,
                           reversion_rate_pct=0.30)
        assert "30%" in sig

    def test_high_composite_contains_composite_int(self):
        sig = self._signal(CoachPattern.passive_resistor, 42.6)
        assert "43" in sig

    def test_exactly_at_20_triggers_high_signal(self):
        sig = self._signal(CoachPattern.none, 20.0)
        # composite >= 20, so NOT the "strong" message
        assert "strong" not in sig.lower()

    def test_none_pattern_at_high_composite_uses_none_value(self):
        sig = self._signal(CoachPattern.none, 30.0)
        # Not in _PATTERN_LABELS, uses .value.replace("_"," ").title() → "None"
        assert "None" in sig


# ══════════════════════════════════════════════════════════════════════════════
# 12. assess() integration test
# ══════════════════════════════════════════════════════════════════════════════

class TestAssessIntegration:
    def test_assess_returns_coach_result(self):
        engine = fresh_engine()
        result = engine.assess(make_input())
        assert isinstance(result, CoachResult)

    def test_assess_rep_id_propagated(self):
        engine = fresh_engine()
        result = engine.assess(make_input(rep_id="Z-77"))
        assert result.rep_id == "Z-77"

    def test_assess_region_propagated(self):
        engine = fresh_engine()
        result = engine.assess(make_input(region="Pacific"))
        assert result.region == "Pacific"

    def test_assess_low_risk_scenario(self):
        engine = fresh_engine()
        result = engine.assess(make_input())  # all-good defaults
        assert result.coach_risk == CoachRisk.low

    def test_assess_low_severity_scenario(self):
        engine = fresh_engine()
        result = engine.assess(make_input())
        assert result.coach_severity == CoachSeverity.receptive

    def test_assess_low_action_scenario(self):
        engine = fresh_engine()
        result = engine.assess(make_input())
        assert result.recommended_action == CoachAction.no_action

    def test_assess_high_risk_scenario(self):
        engine = fresh_engine()
        inp = make_input(
            sessions_attended_rate_pct=0.30,
            challenge_question_rate_pct=0.70,
            manager_satisfaction_score=0.20,
            feedback_implementation_rate_pct=0.10,
            action_item_completion_rate_pct=0.20,
            reversion_rate_pct=0.80,
            coaching_hours_utilized_pct=0.10,
            call_recording_review_rate_pct=0.05,
            peer_learning_engagement_pct=0.05,
            skill_improvement_after_coaching=0.05,
            improvement_velocity=0.05,
            follow_through_score=0.10,
        )
        result = engine.assess(inp)
        assert result.coach_risk in (CoachRisk.high, CoachRisk.critical)

    def test_assess_appends_to_results(self):
        engine = fresh_engine()
        engine.assess(make_input())
        engine.assess(make_input(rep_id="R2"))
        assert len(engine._results) == 2

    def test_assess_composite_in_range(self):
        engine = fresh_engine()
        result = engine.assess(make_input())
        assert 0.0 <= result.coach_composite <= 100.0

    def test_assess_all_score_fields_non_negative(self):
        engine = fresh_engine()
        result = engine.assess(make_input())
        assert result.receptivity_score >= 0.0
        assert result.implementation_score >= 0.0
        assert result.engagement_score >= 0.0
        assert result.improvement_score >= 0.0

    def test_assess_coach_signal_non_empty(self):
        engine = fresh_engine()
        result = engine.assess(make_input())
        assert len(result.coach_signal) > 0

    def test_assess_waste_non_negative(self):
        engine = fresh_engine()
        result = engine.assess(make_input())
        assert result.estimated_coaching_waste_usd >= 0.0

    def test_assess_critical_composite_scenario(self):
        engine = fresh_engine()
        inp = make_input(
            sessions_attended_rate_pct=0.10,
            challenge_question_rate_pct=0.99,
            manager_satisfaction_score=0.10,
            feedback_implementation_rate_pct=0.10,
            action_item_completion_rate_pct=0.10,
            reversion_rate_pct=0.90,
            coaching_hours_utilized_pct=0.10,
            call_recording_review_rate_pct=0.10,
            peer_learning_engagement_pct=0.10,
            skill_improvement_after_coaching=0.05,
            improvement_velocity=0.05,
            follow_through_score=0.10,
        )
        result = engine.assess(inp)
        assert result.coach_composite >= 60.0
        assert result.coach_risk == CoachRisk.critical
        assert result.coach_severity == CoachSeverity.unreachable

    def test_assess_passive_resistor_integration(self):
        engine = fresh_engine()
        inp = make_input(
            sessions_attended_rate_pct=0.40,
            manager_satisfaction_score=0.30,
            challenge_question_rate_pct=0.0,
            action_item_completion_rate_pct=1.0,
            feedback_implementation_rate_pct=1.0,
            reversion_rate_pct=0.0,
            skill_improvement_after_coaching=1.0,
            follow_through_score=1.0,
        )
        result = engine.assess(inp)
        assert result.coach_pattern == CoachPattern.passive_resistor


# ══════════════════════════════════════════════════════════════════════════════
# 13. assess_batch()
# ══════════════════════════════════════════════════════════════════════════════

class TestAssessBatch:
    def test_batch_empty_list(self):
        engine = fresh_engine()
        results = engine.assess_batch([])
        assert results == []

    def test_batch_single_item(self):
        engine = fresh_engine()
        results = engine.assess_batch([make_input()])
        assert len(results) == 1
        assert isinstance(results[0], CoachResult)

    def test_batch_multiple_items(self):
        engine = fresh_engine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_preserves_rep_ids(self):
        engine = fresh_engine()
        inputs = [make_input(rep_id=f"REP-{i}") for i in range(3)]
        results = engine.assess_batch(inputs)
        ids = [r.rep_id for r in results]
        assert ids == ["REP-0", "REP-1", "REP-2"]

    def test_batch_all_results_are_coach_result(self):
        engine = fresh_engine()
        inputs = [make_input(rep_id=f"X{i}") for i in range(4)]
        results = engine.assess_batch(inputs)
        assert all(isinstance(r, CoachResult) for r in results)

    def test_batch_appends_to_results_list(self):
        engine = fresh_engine()
        engine.assess_batch([make_input(rep_id=f"A{i}") for i in range(3)])
        assert len(engine._results) == 3

    def test_batch_after_single_assess(self):
        engine = fresh_engine()
        engine.assess(make_input(rep_id="SINGLE"))
        engine.assess_batch([make_input(rep_id=f"B{i}") for i in range(2)])
        assert len(engine._results) == 3

    def test_batch_returns_list(self):
        engine = fresh_engine()
        result = engine.assess_batch([make_input()])
        assert isinstance(result, list)


# ══════════════════════════════════════════════════════════════════════════════
# 14. summary() — empty (returns 13 keys) and populated
# ══════════════════════════════════════════════════════════════════════════════

class TestSummaryEmpty:
    def _summary(self):
        return fresh_engine().summary()

    def test_empty_summary_key_count(self):
        s = self._summary()
        assert len(s) == 13

    def test_empty_total_is_zero(self):
        assert self._summary()["total"] == 0

    def test_empty_risk_counts_is_empty_dict(self):
        assert self._summary()["risk_counts"] == {}

    def test_empty_pattern_counts_is_empty_dict(self):
        assert self._summary()["pattern_counts"] == {}

    def test_empty_severity_counts_is_empty_dict(self):
        assert self._summary()["severity_counts"] == {}

    def test_empty_action_counts_is_empty_dict(self):
        assert self._summary()["action_counts"] == {}

    def test_empty_avg_coach_composite_is_zero(self):
        assert self._summary()["avg_coach_composite"] == 0.0

    def test_empty_coach_gap_count_is_zero(self):
        assert self._summary()["coach_gap_count"] == 0

    def test_empty_intervention_count_is_zero(self):
        assert self._summary()["intervention_count"] == 0

    def test_empty_avg_receptivity_score_is_zero(self):
        assert self._summary()["avg_receptivity_score"] == 0.0

    def test_empty_avg_implementation_score_is_zero(self):
        assert self._summary()["avg_implementation_score"] == 0.0

    def test_empty_avg_engagement_score_is_zero(self):
        assert self._summary()["avg_engagement_score"] == 0.0

    def test_empty_avg_improvement_score_is_zero(self):
        assert self._summary()["avg_improvement_score"] == 0.0

    def test_empty_total_estimated_coaching_waste_is_zero(self):
        assert self._summary()["total_estimated_coaching_waste_usd"] == 0.0

    def test_empty_has_all_expected_keys(self):
        keys = set(self._summary().keys())
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_coach_composite", "coach_gap_count",
            "intervention_count", "avg_receptivity_score",
            "avg_implementation_score", "avg_engagement_score",
            "avg_improvement_score", "total_estimated_coaching_waste_usd",
        }
        assert keys == expected


class TestSummaryPopulated:
    def _engine_with_data(self, count=3):
        engine = fresh_engine()
        for i in range(count):
            engine.assess(make_input(rep_id=f"R{i}"))
        return engine

    def test_populated_total_correct(self):
        engine = self._engine_with_data(3)
        assert engine.summary()["total"] == 3

    def test_populated_risk_counts_not_empty(self):
        engine = self._engine_with_data(2)
        assert len(engine.summary()["risk_counts"]) > 0

    def test_populated_pattern_counts_not_empty(self):
        engine = self._engine_with_data(2)
        assert len(engine.summary()["pattern_counts"]) > 0

    def test_populated_severity_counts_not_empty(self):
        engine = self._engine_with_data(2)
        assert len(engine.summary()["severity_counts"]) > 0

    def test_populated_action_counts_not_empty(self):
        engine = self._engine_with_data(2)
        assert len(engine.summary()["action_counts"]) > 0

    def test_populated_avg_composite_is_float(self):
        engine = self._engine_with_data(2)
        assert isinstance(engine.summary()["avg_coach_composite"], float)

    def test_populated_avg_composite_non_negative(self):
        engine = self._engine_with_data(2)
        assert engine.summary()["avg_coach_composite"] >= 0.0

    def test_populated_risk_counts_sum_equals_total(self):
        engine = self._engine_with_data(4)
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_populated_pattern_counts_sum_equals_total(self):
        engine = self._engine_with_data(4)
        s = engine.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_populated_severity_counts_sum_equals_total(self):
        engine = self._engine_with_data(4)
        s = engine.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_populated_action_counts_sum_equals_total(self):
        engine = self._engine_with_data(4)
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_populated_coach_gap_count_le_total(self):
        engine = self._engine_with_data(3)
        s = engine.summary()
        assert s["coach_gap_count"] <= s["total"]

    def test_populated_intervention_count_le_total(self):
        engine = self._engine_with_data(3)
        s = engine.summary()
        assert s["intervention_count"] <= s["total"]

    def test_populated_total_waste_non_negative(self):
        engine = self._engine_with_data(3)
        assert engine.summary()["total_estimated_coaching_waste_usd"] >= 0.0

    def test_populated_key_count_is_13(self):
        engine = self._engine_with_data(2)
        assert len(engine.summary()) == 13

    def test_populated_with_mixed_inputs(self):
        engine = fresh_engine()
        # good rep
        engine.assess(make_input(rep_id="GOOD"))
        # bad rep
        bad = make_input(
            rep_id="BAD",
            sessions_attended_rate_pct=0.10,
            challenge_question_rate_pct=0.90,
            manager_satisfaction_score=0.10,
            feedback_implementation_rate_pct=0.10,
            action_item_completion_rate_pct=0.10,
            reversion_rate_pct=0.90,
            coaching_hours_utilized_pct=0.10,
            call_recording_review_rate_pct=0.10,
            peer_learning_engagement_pct=0.10,
            skill_improvement_after_coaching=0.05,
            improvement_velocity=0.05,
            follow_through_score=0.10,
        )
        engine.assess(bad)
        s = engine.summary()
        assert s["total"] == 2
        assert len(s["risk_counts"]) >= 1

    def test_populated_avg_scores_rounded_to_1dp(self):
        engine = self._engine_with_data(3)
        s = engine.summary()
        for key in ["avg_receptivity_score", "avg_implementation_score",
                    "avg_engagement_score", "avg_improvement_score",
                    "avg_coach_composite"]:
            val = s[key]
            assert val == round(val, 1)


# ══════════════════════════════════════════════════════════════════════════════
# 15. Edge cases (zero values, boundary values, max values)
# ══════════════════════════════════════════════════════════════════════════════

class TestEdgeCases:
    def test_all_zero_pct_fields(self):
        engine = fresh_engine()
        inp = make_input(
            feedback_implementation_rate_pct=0.0,
            skill_improvement_after_coaching=0.0,
            action_item_completion_rate_pct=0.0,
            sessions_attended_rate_pct=0.0,
            voluntary_coaching_requests=0,
            reversion_rate_pct=0.0,
            follow_through_score=0.0,
            peer_learning_engagement_pct=0.0,
            call_recording_review_rate_pct=0.0,
            manager_satisfaction_score=0.0,
            self_assessment_accuracy_pct=0.0,
            improvement_velocity=0.0,
            prior_pip_count=0,
            coaching_hours_utilized_pct=0.0,
            multi_modal_engagement_pct=0.0,
            challenge_question_rate_pct=0.0,
            engagement_consistency_pct=0.0,
            total_coaching_sessions=0,
            avg_session_duration_minutes=0.0,
        )
        result = engine.assess(inp)
        assert isinstance(result, CoachResult)

    def test_all_max_pct_fields(self):
        engine = fresh_engine()
        inp = make_input(
            feedback_implementation_rate_pct=1.0,
            skill_improvement_after_coaching=1.0,
            action_item_completion_rate_pct=1.0,
            sessions_attended_rate_pct=1.0,
            voluntary_coaching_requests=100,
            reversion_rate_pct=1.0,
            follow_through_score=1.0,
            peer_learning_engagement_pct=1.0,
            call_recording_review_rate_pct=1.0,
            manager_satisfaction_score=1.0,
            self_assessment_accuracy_pct=1.0,
            improvement_velocity=1.0,
            prior_pip_count=10,
            coaching_hours_utilized_pct=1.0,
            multi_modal_engagement_pct=1.0,
            challenge_question_rate_pct=1.0,
            engagement_consistency_pct=1.0,
            total_coaching_sessions=100,
            avg_session_duration_minutes=120.0,
        )
        result = engine.assess(inp)
        assert isinstance(result, CoachResult)

    def test_composite_never_exceeds_100(self):
        engine = fresh_engine()
        for _ in range(5):
            inp = make_input(
                sessions_attended_rate_pct=0.0,
                challenge_question_rate_pct=1.0,
                manager_satisfaction_score=0.0,
                feedback_implementation_rate_pct=0.0,
                action_item_completion_rate_pct=0.0,
                reversion_rate_pct=1.0,
                coaching_hours_utilized_pct=0.0,
                call_recording_review_rate_pct=0.0,
                peer_learning_engagement_pct=0.0,
                skill_improvement_after_coaching=0.0,
                improvement_velocity=0.0,
                follow_through_score=0.0,
            )
            result = engine.assess(inp)
            assert result.coach_composite <= 100.0

    def test_receptivity_score_never_exceeds_100(self):
        engine = fresh_engine()
        inp = make_input(sessions_attended_rate_pct=0.0, challenge_question_rate_pct=1.0,
                         manager_satisfaction_score=0.0)
        assert engine._receptivity_score(inp) <= 100.0

    def test_implementation_score_never_exceeds_100(self):
        engine = fresh_engine()
        inp = make_input(feedback_implementation_rate_pct=0.0,
                         action_item_completion_rate_pct=0.0,
                         reversion_rate_pct=1.0)
        assert engine._implementation_score(inp) <= 100.0

    def test_engagement_score_never_exceeds_100(self):
        engine = fresh_engine()
        inp = make_input(coaching_hours_utilized_pct=0.0,
                         call_recording_review_rate_pct=0.0,
                         peer_learning_engagement_pct=0.0)
        assert engine._engagement_score(inp) <= 100.0

    def test_improvement_score_never_exceeds_100(self):
        engine = fresh_engine()
        inp = make_input(skill_improvement_after_coaching=0.0,
                         improvement_velocity=0.0,
                         follow_through_score=0.0)
        assert engine._improvement_score(inp) <= 100.0

    def test_zero_sessions_waste_is_zero(self):
        engine = fresh_engine()
        inp = make_input(total_coaching_sessions=0,
                         feedback_implementation_rate_pct=0.0)
        waste = engine._coaching_waste(inp, 100.0)
        assert waste == 0.0

    def test_single_session_waste_calculation(self):
        engine = fresh_engine()
        inp = make_input(total_coaching_sessions=1,
                         feedback_implementation_rate_pct=0.0)
        # waste = 1 * 500 * (1.0 * 1.0) = 500
        waste = engine._coaching_waste(inp, 100.0)
        assert waste == pytest.approx(500.0)

    def test_boundary_composite_exactly_20_is_moderate(self):
        engine = fresh_engine()
        assert engine._risk(20.0) == CoachRisk.moderate
        assert engine._severity(20.0) == CoachSeverity.developing

    def test_boundary_composite_exactly_40_is_high(self):
        engine = fresh_engine()
        assert engine._risk(40.0) == CoachRisk.high
        assert engine._severity(40.0) == CoachSeverity.resistant

    def test_boundary_composite_exactly_60_is_critical(self):
        engine = fresh_engine()
        assert engine._risk(60.0) == CoachRisk.critical
        assert engine._severity(60.0) == CoachSeverity.unreachable

    def test_multiple_assessments_accumulate(self):
        engine = fresh_engine()
        for i in range(10):
            engine.assess(make_input(rep_id=f"REP-{i}"))
        assert len(engine._results) == 10

    def test_to_dict_all_values_json_serializable(self):
        import json
        engine = fresh_engine()
        result = engine.assess(make_input())
        d = result.to_dict()
        # should not raise
        serialized = json.dumps(d)
        assert len(serialized) > 0

    def test_assess_batch_empty_does_not_affect_summary(self):
        engine = fresh_engine()
        engine.assess_batch([])
        s = engine.summary()
        assert s["total"] == 0

    def test_assess_stores_result_with_correct_rep_id(self):
        engine = fresh_engine()
        engine.assess(make_input(rep_id="STORED"))
        assert engine._results[0].rep_id == "STORED"

    def test_ghost_committor_boundary_both_exact(self):
        engine = fresh_engine()
        p = engine._pattern(make_input(
            sessions_attended_rate_pct=0.80,
            manager_satisfaction_score=0.80,
            challenge_question_rate_pct=0.0,
            action_item_completion_rate_pct=0.30,
            feedback_implementation_rate_pct=1.0,
            reversion_rate_pct=0.0,
            skill_improvement_after_coaching=1.0,
            follow_through_score=0.25,
        ))
        assert p == CoachPattern.ghost_committor

    def test_engine_can_be_reused_across_many_batches(self):
        engine = fresh_engine()
        for _ in range(3):
            engine.assess_batch([make_input(rep_id="X")])
        assert len(engine._results) == 3
