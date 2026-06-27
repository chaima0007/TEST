"""
pytest suite for SalesRepBurnoutAttritionRiskIntelligenceEngine.
Target: 280-320 tests, file under 600 lines.
"""
from __future__ import annotations
import pytest
from swarm.intelligence.sales_rep_burnout_attrition_risk_intelligence_engine import (
    BurnoutRisk,
    BurnoutPattern,
    BurnoutSeverity,
    BurnoutAction,
    BurnoutInput,
    BurnoutResult,
    SalesRepBurnoutAttritionRiskIntelligenceEngine,
)


# ── helpers ──────────────────────────────────────────────────────────────────

def make_input(**overrides) -> BurnoutInput:
    """Baseline healthy rep; override any field for targeted testing."""
    defaults = dict(
        rep_id="R001", region="West", evaluation_period_id="Q1-2026",
        activity_volume_trend_pct=0.10, win_rate_trend_pct=0.05,
        pipeline_creation_trend_pct=0.05, avg_deal_size_trend_pct=0.02,
        pto_utilization_rate_pct=0.80, unplanned_absence_days=0,
        overtime_hours_per_week=2.0, after_hours_activity_rate_pct=0.10,
        manager_satisfaction_score=0.90, peer_collaboration_score=0.85,
        recognition_received_count=5, voluntary_task_completion_pct=0.90,
        training_participation_pct=0.80, internal_mobility_applications=0,
        tenure_months=24, consecutive_quota_miss_streak=0,
        comp_plan_satisfaction_score=0.80, career_path_clarity_score=0.80,
        exit_interview_signals=0, team_attrition_exposure_pct=0.10,
    )
    defaults.update(overrides)
    return BurnoutInput(**defaults)


def fresh_engine() -> SalesRepBurnoutAttritionRiskIntelligenceEngine:
    return SalesRepBurnoutAttritionRiskIntelligenceEngine()


def assess(engine=None, **overrides) -> BurnoutResult:
    e = engine or fresh_engine()
    return e.assess(make_input(**overrides))


# ── 1. Enum membership ────────────────────────────────────────────────────────

class TestEnums:
    def test_burnout_risk_low(self):       assert BurnoutRisk.low.value == "low"
    def test_burnout_risk_moderate(self):  assert BurnoutRisk.moderate.value == "moderate"
    def test_burnout_risk_high(self):      assert BurnoutRisk.high.value == "high"
    def test_burnout_risk_critical(self):  assert BurnoutRisk.critical.value == "critical"
    def test_burnout_risk_count(self):     assert len(BurnoutRisk) == 4

    def test_pattern_none(self):                  assert BurnoutPattern.none.value == "none"
    def test_pattern_gradual_disengagement(self): assert BurnoutPattern.gradual_disengagement.value == "gradual_disengagement"
    def test_pattern_quota_fatigue(self):          assert BurnoutPattern.quota_fatigue.value == "quota_fatigue"
    def test_pattern_manager_friction(self):       assert BurnoutPattern.manager_friction.value == "manager_friction"
    def test_pattern_peer_isolation(self):         assert BurnoutPattern.peer_isolation.value == "peer_isolation"
    def test_pattern_recognition_drought(self):    assert BurnoutPattern.recognition_drought.value == "recognition_drought"
    def test_pattern_count(self):                  assert len(BurnoutPattern) == 6

    def test_severity_thriving(self):    assert BurnoutSeverity.thriving.value == "thriving"
    def test_severity_straining(self):   assert BurnoutSeverity.straining.value == "straining"
    def test_severity_burning_out(self): assert BurnoutSeverity.burning_out.value == "burning_out"
    def test_severity_flight_risk(self): assert BurnoutSeverity.flight_risk.value == "flight_risk"
    def test_severity_count(self):       assert len(BurnoutSeverity) == 4

    def test_action_no_action(self):                    assert BurnoutAction.no_action.value == "no_action"
    def test_action_wellness_check_in(self):            assert BurnoutAction.wellness_check_in.value == "wellness_check_in"
    def test_action_workload_rebalancing(self):         assert BurnoutAction.workload_rebalancing.value == "workload_rebalancing"
    def test_action_recognition_intervention(self):     assert BurnoutAction.recognition_intervention.value == "recognition_intervention"
    def test_action_manager_mediation(self):            assert BurnoutAction.manager_mediation.value == "manager_mediation"
    def test_action_territory_reassignment(self):       assert BurnoutAction.territory_reassignment.value == "territory_reassignment"
    def test_action_retention_package_discussion(self): assert BurnoutAction.retention_package_discussion.value == "retention_package_discussion"
    def test_action_count(self):                        assert len(BurnoutAction) == 7


# ── 2. BurnoutInput field count ───────────────────────────────────────────────

class TestBurnoutInput:
    def test_field_count(self):
        import dataclasses
        assert len(dataclasses.fields(BurnoutInput)) == 23

    def test_str_fields(self):
        inp = make_input()
        assert inp.rep_id == "R001"
        assert inp.region == "West"
        assert inp.evaluation_period_id == "Q1-2026"

    def test_int_fields(self):
        inp = make_input(unplanned_absence_days=3, recognition_received_count=2,
                         internal_mobility_applications=1, tenure_months=12,
                         consecutive_quota_miss_streak=1, exit_interview_signals=0)
        assert isinstance(inp.unplanned_absence_days, int)
        assert isinstance(inp.recognition_received_count, int)
        assert isinstance(inp.internal_mobility_applications, int)
        assert isinstance(inp.tenure_months, int)
        assert isinstance(inp.consecutive_quota_miss_streak, int)
        assert isinstance(inp.exit_interview_signals, int)


# ── 3. to_dict: exactly 15 keys ───────────────────────────────────────────────

class TestToDict:
    EXPECTED_KEYS = {
        "rep_id", "region", "burnout_risk", "burnout_pattern", "burnout_severity",
        "recommended_action", "disengagement_score", "fatigue_score", "sentiment_score",
        "performance_erosion_score", "burnout_composite", "has_burnout_gap",
        "is_flight_risk", "estimated_replacement_cost_usd", "burnout_signal",
    }

    def test_key_count(self):
        d = assess().to_dict()
        assert len(d) == 15

    def test_exact_keys(self):
        d = assess().to_dict()
        assert set(d.keys()) == self.EXPECTED_KEYS

    def test_no_has_coach_gap(self):
        d = assess().to_dict()
        assert "has_coach_gap" not in d

    def test_has_burnout_gap_present(self):
        assert "has_burnout_gap" in assess().to_dict()

    def test_is_flight_risk_present(self):
        assert "is_flight_risk" in assess().to_dict()

    def test_string_enum_values(self):
        d = assess().to_dict()
        assert isinstance(d["burnout_risk"], str)
        assert isinstance(d["burnout_pattern"], str)
        assert isinstance(d["burnout_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_bool_flags(self):
        d = assess().to_dict()
        assert isinstance(d["has_burnout_gap"], bool)
        assert isinstance(d["is_flight_risk"], bool)

    def test_numeric_fields(self):
        d = assess().to_dict()
        for k in ("disengagement_score", "fatigue_score", "sentiment_score",
                   "performance_erosion_score", "burnout_composite",
                   "estimated_replacement_cost_usd"):
            assert isinstance(d[k], (int, float))


# ── 4. summary: exactly 13 keys ───────────────────────────────────────────────

class TestSummaryKeys:
    EXPECTED_KEYS = {
        "total", "risk_counts", "pattern_counts", "severity_counts", "action_counts",
        "avg_burnout_composite", "burnout_gap_count", "flight_risk_count",
        "avg_disengagement_score", "avg_fatigue_score", "avg_sentiment_score",
        "avg_performance_erosion_score", "total_estimated_replacement_cost_usd",
    }

    def test_empty_key_count(self):
        assert len(fresh_engine().summary()) == 13

    def test_empty_exact_keys(self):
        assert set(fresh_engine().summary().keys()) == self.EXPECTED_KEYS

    def test_populated_key_count(self):
        e = fresh_engine(); e.assess(make_input())
        assert len(e.summary()) == 13

    def test_populated_exact_keys(self):
        e = fresh_engine(); e.assess(make_input())
        assert set(e.summary().keys()) == self.EXPECTED_KEYS


# ── 5. Disengagement sub-score ────────────────────────────────────────────────

class TestDisengagementScore:
    def _score(self, **kw):
        e = fresh_engine()
        return e._disengagement_score(make_input(**kw))

    # activity_volume_trend_pct
    def test_activity_tier1(self):   assert self._score(activity_volume_trend_pct=-0.31) == pytest.approx(40, abs=0.01)
    def test_activity_tier1_exact(self): assert self._score(activity_volume_trend_pct=-0.30) == pytest.approx(40, abs=0.01)
    def test_activity_tier2(self):   assert self._score(activity_volume_trend_pct=-0.20) == pytest.approx(22, abs=0.01)
    def test_activity_tier2_exact(self): assert self._score(activity_volume_trend_pct=-0.15) == pytest.approx(22, abs=0.01)
    def test_activity_tier3(self):   assert self._score(activity_volume_trend_pct=-0.10) == pytest.approx(8, abs=0.01)
    def test_activity_tier3_exact(self): assert self._score(activity_volume_trend_pct=-0.05) == pytest.approx(8, abs=0.01)
    def test_activity_zero(self):    assert self._score(activity_volume_trend_pct=0.0) == pytest.approx(0, abs=0.01)

    # training_participation_pct
    def test_training_tier1(self):   assert self._score(training_participation_pct=0.20) == pytest.approx(35, abs=0.01)
    def test_training_tier1_exact(self): assert self._score(training_participation_pct=0.25) == pytest.approx(35, abs=0.01)
    def test_training_tier2(self):   assert self._score(training_participation_pct=0.40) == pytest.approx(18, abs=0.01)
    def test_training_tier2_exact(self): assert self._score(training_participation_pct=0.50) == pytest.approx(18, abs=0.01)
    def test_training_none(self):    assert self._score(training_participation_pct=0.80) == pytest.approx(0, abs=0.01)

    # voluntary_task_completion_pct
    def test_voluntary_tier1(self):  assert self._score(voluntary_task_completion_pct=0.30) == pytest.approx(25, abs=0.01)
    def test_voluntary_tier1_exact(self): assert self._score(voluntary_task_completion_pct=0.40) == pytest.approx(25, abs=0.01)
    def test_voluntary_tier2(self):  assert self._score(voluntary_task_completion_pct=0.55) == pytest.approx(12, abs=0.01)
    def test_voluntary_tier2_exact(self): assert self._score(voluntary_task_completion_pct=0.65) == pytest.approx(12, abs=0.01)
    def test_voluntary_none(self):   assert self._score(voluntary_task_completion_pct=0.90) == pytest.approx(0, abs=0.01)

    def test_max_cap(self):
        s = self._score(activity_volume_trend_pct=-0.50, training_participation_pct=0.10, voluntary_task_completion_pct=0.10)
        assert s == 100.0


# ── 6. Fatigue sub-score ──────────────────────────────────────────────────────

class TestFatigueScore:
    def _score(self, **kw):
        return fresh_engine()._fatigue_score(make_input(**kw))

    def test_overtime_tier1(self):   assert self._score(overtime_hours_per_week=21) == pytest.approx(40, abs=0.01)
    def test_overtime_tier1_exact(self): assert self._score(overtime_hours_per_week=20) == pytest.approx(40, abs=0.01)
    def test_overtime_tier2(self):   assert self._score(overtime_hours_per_week=15) == pytest.approx(22, abs=0.01)
    def test_overtime_tier2_exact(self): assert self._score(overtime_hours_per_week=12) == pytest.approx(22, abs=0.01)
    def test_overtime_tier3(self):   assert self._score(overtime_hours_per_week=8) == pytest.approx(8, abs=0.01)
    def test_overtime_tier3_exact(self): assert self._score(overtime_hours_per_week=6) == pytest.approx(8, abs=0.01)
    def test_overtime_zero(self):    assert self._score(overtime_hours_per_week=2) == pytest.approx(0, abs=0.01)

    def test_after_hours_tier1(self):  assert self._score(after_hours_activity_rate_pct=0.60) == pytest.approx(35, abs=0.01)
    def test_after_hours_tier1_exact(self): assert self._score(after_hours_activity_rate_pct=0.50) == pytest.approx(35, abs=0.01)
    def test_after_hours_tier2(self):  assert self._score(after_hours_activity_rate_pct=0.40) == pytest.approx(18, abs=0.01)
    def test_after_hours_tier2_exact(self): assert self._score(after_hours_activity_rate_pct=0.30) == pytest.approx(18, abs=0.01)
    def test_after_hours_none(self):   assert self._score(after_hours_activity_rate_pct=0.10) == pytest.approx(0, abs=0.01)

    def test_absence_tier1(self):    assert self._score(unplanned_absence_days=6) == pytest.approx(25, abs=0.01)
    def test_absence_tier1_exact(self): assert self._score(unplanned_absence_days=5) == pytest.approx(25, abs=0.01)
    def test_absence_tier2(self):    assert self._score(unplanned_absence_days=3) == pytest.approx(12, abs=0.01)
    def test_absence_tier2_exact(self): assert self._score(unplanned_absence_days=2) == pytest.approx(12, abs=0.01)
    def test_absence_none(self):     assert self._score(unplanned_absence_days=0) == pytest.approx(0, abs=0.01)

    def test_max_cap(self):
        s = self._score(overtime_hours_per_week=25, after_hours_activity_rate_pct=0.60, unplanned_absence_days=8)
        assert s == 100.0


# ── 7. Sentiment sub-score ────────────────────────────────────────────────────

class TestSentimentScore:
    def _score(self, **kw):
        return fresh_engine()._sentiment_score(make_input(**kw))

    def test_comp_tier1(self):   assert self._score(comp_plan_satisfaction_score=0.20) == pytest.approx(40, abs=0.01)
    def test_comp_tier1_exact(self): assert self._score(comp_plan_satisfaction_score=0.30) == pytest.approx(40, abs=0.01)
    def test_comp_tier2(self):   assert self._score(comp_plan_satisfaction_score=0.40) == pytest.approx(22, abs=0.01)
    def test_comp_tier2_exact(self): assert self._score(comp_plan_satisfaction_score=0.50) == pytest.approx(22, abs=0.01)
    def test_comp_tier3(self):   assert self._score(comp_plan_satisfaction_score=0.60) == pytest.approx(8, abs=0.01)
    def test_comp_tier3_exact(self): assert self._score(comp_plan_satisfaction_score=0.70) == pytest.approx(8, abs=0.01)
    def test_comp_none(self):    assert self._score(comp_plan_satisfaction_score=0.90) == pytest.approx(0, abs=0.01)

    def test_career_tier1(self): assert self._score(career_path_clarity_score=0.10) == pytest.approx(35, abs=0.01)
    def test_career_tier1_exact(self): assert self._score(career_path_clarity_score=0.25) == pytest.approx(35, abs=0.01)
    def test_career_tier2(self): assert self._score(career_path_clarity_score=0.40) == pytest.approx(18, abs=0.01)
    def test_career_tier2_exact(self): assert self._score(career_path_clarity_score=0.50) == pytest.approx(18, abs=0.01)
    def test_career_none(self):  assert self._score(career_path_clarity_score=0.80) == pytest.approx(0, abs=0.01)

    def test_mgr_tier1(self):    assert self._score(manager_satisfaction_score=0.20) == pytest.approx(25, abs=0.01)
    def test_mgr_tier1_exact(self): assert self._score(manager_satisfaction_score=0.30) == pytest.approx(25, abs=0.01)
    def test_mgr_tier2(self):    assert self._score(manager_satisfaction_score=0.40) == pytest.approx(12, abs=0.01)
    def test_mgr_tier2_exact(self): assert self._score(manager_satisfaction_score=0.50) == pytest.approx(12, abs=0.01)
    def test_mgr_none(self):     assert self._score(manager_satisfaction_score=0.90) == pytest.approx(0, abs=0.01)

    def test_max_cap(self):
        s = self._score(comp_plan_satisfaction_score=0.10, career_path_clarity_score=0.10, manager_satisfaction_score=0.10)
        assert s == 100.0


# ── 8. Performance erosion sub-score ─────────────────────────────────────────

class TestPerformanceErosionScore:
    def _score(self, **kw):
        return fresh_engine()._performance_erosion_score(make_input(**kw))

    def test_winrate_tier1(self):   assert self._score(win_rate_trend_pct=-0.30) == pytest.approx(45, abs=0.01)
    def test_winrate_tier1_exact(self): assert self._score(win_rate_trend_pct=-0.25) == pytest.approx(45, abs=0.01)
    def test_winrate_tier2(self):   assert self._score(win_rate_trend_pct=-0.15) == pytest.approx(25, abs=0.01)
    def test_winrate_tier2_exact(self): assert self._score(win_rate_trend_pct=-0.10) == pytest.approx(25, abs=0.01)
    def test_winrate_tier3(self):   assert self._score(win_rate_trend_pct=-0.05) == pytest.approx(10, abs=0.01)
    def test_winrate_tier3_exact(self): assert self._score(win_rate_trend_pct=-0.03) == pytest.approx(10, abs=0.01)
    def test_winrate_none(self):    assert self._score(win_rate_trend_pct=0.05) == pytest.approx(0, abs=0.01)

    def test_pipeline_tier1(self):  assert self._score(pipeline_creation_trend_pct=-0.30) == pytest.approx(30, abs=0.01)
    def test_pipeline_tier1_exact(self): assert self._score(pipeline_creation_trend_pct=-0.25) == pytest.approx(30, abs=0.01)
    def test_pipeline_tier2(self):  assert self._score(pipeline_creation_trend_pct=-0.15) == pytest.approx(15, abs=0.01)
    def test_pipeline_tier2_exact(self): assert self._score(pipeline_creation_trend_pct=-0.10) == pytest.approx(15, abs=0.01)
    def test_pipeline_none(self):   assert self._score(pipeline_creation_trend_pct=0.05) == pytest.approx(0, abs=0.01)

    def test_quota_miss_tier1(self): assert self._score(consecutive_quota_miss_streak=3) == pytest.approx(25, abs=0.01)
    def test_quota_miss_tier1_high(self): assert self._score(consecutive_quota_miss_streak=5) == pytest.approx(25, abs=0.01)
    def test_quota_miss_tier2(self): assert self._score(consecutive_quota_miss_streak=2) == pytest.approx(12, abs=0.01)
    def test_quota_miss_none(self):  assert self._score(consecutive_quota_miss_streak=0) == pytest.approx(0, abs=0.01)

    def test_max_cap(self):
        s = self._score(win_rate_trend_pct=-0.50, pipeline_creation_trend_pct=-0.50, consecutive_quota_miss_streak=5)
        assert s == 100.0


# ── 9. Composite weighting ────────────────────────────────────────────────────

class TestComposite:
    def test_weight_formula(self):
        e = fresh_engine()
        c = e._composite(100, 100, 100, 100)
        assert c == 100.0

    def test_weight_zero(self):
        assert fresh_engine()._composite(0, 0, 0, 0) == 0.0

    def test_dis_only(self):
        c = fresh_engine()._composite(100, 0, 0, 0)
        assert c == pytest.approx(30.0, abs=0.01)

    def test_fat_only(self):
        c = fresh_engine()._composite(0, 100, 0, 0)
        assert c == pytest.approx(25.0, abs=0.01)

    def test_sent_only(self):
        c = fresh_engine()._composite(0, 0, 100, 0)
        assert c == pytest.approx(30.0, abs=0.01)

    def test_perf_only(self):
        c = fresh_engine()._composite(0, 0, 0, 100)
        assert c == pytest.approx(15.0, abs=0.01)

    def test_weights_sum_to_one(self):
        assert 0.30 + 0.25 + 0.30 + 0.15 == pytest.approx(1.00)

    def test_composite_capped_at_100(self):
        assert fresh_engine()._composite(200, 200, 200, 200) == 100.0

    def test_partial_mix(self):
        c = fresh_engine()._composite(40, 60, 20, 80)
        expected = min(round(40*0.30 + 60*0.25 + 20*0.30 + 80*0.15, 2), 100.0)
        assert c == pytest.approx(expected, abs=0.01)


# ── 10. Risk thresholds ───────────────────────────────────────────────────────

class TestRisk:
    def _risk(self, c): return fresh_engine()._risk(c)

    def test_critical_at_60(self):    assert self._risk(60) == BurnoutRisk.critical
    def test_critical_above_60(self): assert self._risk(80) == BurnoutRisk.critical
    def test_high_at_40(self):        assert self._risk(40) == BurnoutRisk.high
    def test_high_59(self):           assert self._risk(59) == BurnoutRisk.high
    def test_moderate_at_20(self):    assert self._risk(20) == BurnoutRisk.moderate
    def test_moderate_39(self):       assert self._risk(39) == BurnoutRisk.moderate
    def test_low_at_19(self):         assert self._risk(19) == BurnoutRisk.low
    def test_low_at_0(self):          assert self._risk(0) == BurnoutRisk.low


# ── 11. Severity thresholds ───────────────────────────────────────────────────

class TestSeverity:
    def _sev(self, c): return fresh_engine()._severity(c)

    def test_flight_risk_at_60(self):   assert self._sev(60) == BurnoutSeverity.flight_risk
    def test_flight_risk_above(self):   assert self._sev(90) == BurnoutSeverity.flight_risk
    def test_burning_out_at_40(self):   assert self._sev(40) == BurnoutSeverity.burning_out
    def test_burning_out_59(self):      assert self._sev(59) == BurnoutSeverity.burning_out
    def test_straining_at_20(self):     assert self._sev(20) == BurnoutSeverity.straining
    def test_straining_39(self):        assert self._sev(39) == BurnoutSeverity.straining
    def test_thriving_at_19(self):      assert self._sev(19) == BurnoutSeverity.thriving
    def test_thriving_at_0(self):       assert self._sev(0) == BurnoutSeverity.thriving


# ── 12. Action mapping ────────────────────────────────────────────────────────

class TestAction:
    def _action(self, risk, pattern):
        return fresh_engine()._action(risk, pattern)

    def test_critical_any_returns_retention(self):
        for p in BurnoutPattern:
            assert self._action(BurnoutRisk.critical, p) == BurnoutAction.retention_package_discussion

    def test_high_gradual_disengagement(self):
        assert self._action(BurnoutRisk.high, BurnoutPattern.gradual_disengagement) == BurnoutAction.workload_rebalancing

    def test_high_quota_fatigue(self):
        assert self._action(BurnoutRisk.high, BurnoutPattern.quota_fatigue) == BurnoutAction.territory_reassignment

    def test_high_manager_friction(self):
        assert self._action(BurnoutRisk.high, BurnoutPattern.manager_friction) == BurnoutAction.manager_mediation

    def test_high_peer_isolation(self):
        assert self._action(BurnoutRisk.high, BurnoutPattern.peer_isolation) == BurnoutAction.recognition_intervention

    def test_high_recognition_drought(self):
        assert self._action(BurnoutRisk.high, BurnoutPattern.recognition_drought) == BurnoutAction.recognition_intervention

    def test_high_none_pattern(self):
        assert self._action(BurnoutRisk.high, BurnoutPattern.none) == BurnoutAction.workload_rebalancing

    def test_moderate_always_wellness(self):
        for p in BurnoutPattern:
            assert self._action(BurnoutRisk.moderate, p) == BurnoutAction.wellness_check_in

    def test_low_always_no_action(self):
        for p in BurnoutPattern:
            assert self._action(BurnoutRisk.low, p) == BurnoutAction.no_action


# ── 13. Pattern detection & priority ─────────────────────────────────────────

class TestPattern:
    def _pat(self, **kw): return fresh_engine()._pattern(make_input(**kw))

    def test_gradual_disengagement(self):
        p = self._pat(activity_volume_trend_pct=-0.25, training_participation_pct=0.30)
        assert p == BurnoutPattern.gradual_disengagement

    def test_gradual_disengagement_boundary(self):
        p = self._pat(activity_volume_trend_pct=-0.20, training_participation_pct=0.40)
        assert p == BurnoutPattern.gradual_disengagement

    def test_quota_fatigue(self):
        p = self._pat(consecutive_quota_miss_streak=2, comp_plan_satisfaction_score=0.40)
        assert p == BurnoutPattern.quota_fatigue

    def test_quota_fatigue_boundary(self):
        p = self._pat(consecutive_quota_miss_streak=2, comp_plan_satisfaction_score=0.45)
        assert p == BurnoutPattern.quota_fatigue

    def test_manager_friction(self):
        p = self._pat(manager_satisfaction_score=0.30, peer_collaboration_score=0.35)
        assert p == BurnoutPattern.manager_friction

    def test_manager_friction_boundary(self):
        p = self._pat(manager_satisfaction_score=0.35, peer_collaboration_score=0.40)
        assert p == BurnoutPattern.manager_friction

    def test_peer_isolation(self):
        p = self._pat(peer_collaboration_score=0.25, recognition_received_count=1)
        assert p == BurnoutPattern.peer_isolation

    def test_peer_isolation_boundary(self):
        p = self._pat(peer_collaboration_score=0.30, recognition_received_count=1)
        assert p == BurnoutPattern.peer_isolation

    def test_recognition_drought(self):
        p = self._pat(recognition_received_count=1, career_path_clarity_score=0.30)
        assert p == BurnoutPattern.recognition_drought

    def test_recognition_drought_boundary(self):
        p = self._pat(recognition_received_count=1, career_path_clarity_score=0.35)
        assert p == BurnoutPattern.recognition_drought

    def test_none_healthy(self):
        assert self._pat() == BurnoutPattern.none

    # Priority: gradual_disengagement beats quota_fatigue
    def test_priority_gradual_over_quota(self):
        p = self._pat(activity_volume_trend_pct=-0.25, training_participation_pct=0.30,
                      consecutive_quota_miss_streak=2, comp_plan_satisfaction_score=0.40)
        assert p == BurnoutPattern.gradual_disengagement

    # Priority: quota_fatigue beats manager_friction
    def test_priority_quota_over_manager(self):
        p = self._pat(consecutive_quota_miss_streak=2, comp_plan_satisfaction_score=0.40,
                      manager_satisfaction_score=0.30, peer_collaboration_score=0.35)
        assert p == BurnoutPattern.quota_fatigue


# ── 14. has_burnout_gap flag ──────────────────────────────────────────────────

class TestHasBurnoutGap:
    def test_gap_via_composite_40(self):
        # craft high composite: all scores maxed
        r = assess(activity_volume_trend_pct=-0.50, training_participation_pct=0.10,
                   voluntary_task_completion_pct=0.30, comp_plan_satisfaction_score=0.10,
                   career_path_clarity_score=0.10, manager_satisfaction_score=0.10,
                   overtime_hours_per_week=25, after_hours_activity_rate_pct=0.60,
                   unplanned_absence_days=8, win_rate_trend_pct=-0.50,
                   pipeline_creation_trend_pct=-0.50, consecutive_quota_miss_streak=5)
        assert r.burnout_composite >= 40
        assert r.has_burnout_gap is True

    def test_gap_via_activity_trend(self):
        r = assess(activity_volume_trend_pct=-0.20)
        assert r.has_burnout_gap is True

    def test_gap_via_activity_trend_below(self):
        r = assess(activity_volume_trend_pct=-0.30)
        assert r.has_burnout_gap is True

    def test_gap_via_quota_miss_streak_2(self):
        r = assess(consecutive_quota_miss_streak=2)
        assert r.has_burnout_gap is True

    def test_gap_via_quota_miss_streak_3(self):
        r = assess(consecutive_quota_miss_streak=3)
        assert r.has_burnout_gap is True

    def test_no_gap_healthy(self):
        r = assess()
        assert r.has_burnout_gap is False

    def test_no_gap_activity_just_above(self):
        r = assess(activity_volume_trend_pct=-0.19, consecutive_quota_miss_streak=0)
        assert r.has_burnout_gap is False


# ── 15. is_flight_risk flag ───────────────────────────────────────────────────

class TestIsFlightRisk:
    def test_flight_via_composite_25(self):
        # composite 25+: moderate disengagement + moderate sentiment
        r = assess(activity_volume_trend_pct=-0.30, training_participation_pct=0.20,
                   comp_plan_satisfaction_score=0.45, career_path_clarity_score=0.55)
        assert r.burnout_composite >= 25
        assert r.is_flight_risk is True

    def test_flight_via_internal_apps(self):
        r = assess(internal_mobility_applications=1)
        assert r.is_flight_risk is True

    def test_flight_via_internal_apps_many(self):
        r = assess(internal_mobility_applications=3)
        assert r.is_flight_risk is True

    def test_flight_via_comp_satisfaction_040(self):
        r = assess(comp_plan_satisfaction_score=0.40)
        assert r.is_flight_risk is True

    def test_flight_via_comp_satisfaction_below(self):
        r = assess(comp_plan_satisfaction_score=0.30)
        assert r.is_flight_risk is True

    def test_flight_via_exit_signals(self):
        r = assess(exit_interview_signals=1)
        assert r.is_flight_risk is True

    def test_not_flight_healthy(self):
        r = assess()
        assert r.is_flight_risk is False

    def test_comp_above_040_not_flight_alone(self):
        r = assess(comp_plan_satisfaction_score=0.41)
        # composite will be low, no apps, no exit signals — check is_flight_risk is False
        assert r.is_flight_risk is False


# ── 16. Replacement cost formula ─────────────────────────────────────────────

class TestReplacementCost:
    def test_formula_exact(self):
        e = fresh_engine()
        inp = make_input(tenure_months=24)
        comp = 50.0
        expected = round(85000 * (1.5 + 24/24 * 0.5) * (50/100), 2)
        assert e._replacement_cost(inp, comp) == pytest.approx(expected, abs=0.01)

    def test_formula_zero_tenure(self):
        e = fresh_engine()
        inp = make_input(tenure_months=0)
        comp = 100.0
        expected = round(85000 * 1.5 * 1.0, 2)
        assert e._replacement_cost(inp, comp) == pytest.approx(expected, abs=0.01)

    def test_formula_zero_composite(self):
        e = fresh_engine()
        inp = make_input(tenure_months=24)
        assert e._replacement_cost(inp, 0.0) == 0.0

    def test_cost_increases_with_tenure(self):
        e = fresh_engine()
        c1 = e._replacement_cost(make_input(tenure_months=12), 50.0)
        c2 = e._replacement_cost(make_input(tenure_months=48), 50.0)
        assert c2 > c1

    def test_cost_increases_with_composite(self):
        e = fresh_engine()
        c1 = e._replacement_cost(make_input(tenure_months=24), 30.0)
        c2 = e._replacement_cost(make_input(tenure_months=24), 80.0)
        assert c2 > c1

    def test_in_result(self):
        r = assess(tenure_months=24)
        assert r.estimated_replacement_cost_usd >= 0.0


# ── 17. Signal text ───────────────────────────────────────────────────────────

class TestSignal:
    def test_healthy_signal(self):
        r = assess()
        assert "healthy" in r.burnout_signal.lower()

    def test_signal_contains_pattern_label(self):
        # gradual_disengagement + enough score to push composite >= 20
        r = assess(activity_volume_trend_pct=-0.25, training_participation_pct=0.20,
                   voluntary_task_completion_pct=0.35, comp_plan_satisfaction_score=0.65,
                   career_path_clarity_score=0.55)
        assert r.burnout_composite >= 20
        assert "Gradual disengagement" in r.burnout_signal

    def test_signal_format_moderate_plus(self):
        # push comp+career+manager scores to get composite >= 20
        r = assess(comp_plan_satisfaction_score=0.30, career_path_clarity_score=0.25,
                   manager_satisfaction_score=0.30)
        assert r.burnout_composite >= 20
        assert "%" in r.burnout_signal
        assert "composite" in r.burnout_signal.lower()

    def test_signal_quota_fatigue_label(self):
        # quota_fatigue pattern + ensure composite >= 20
        r = assess(consecutive_quota_miss_streak=2, comp_plan_satisfaction_score=0.40,
                   win_rate_trend_pct=-0.25, career_path_clarity_score=0.30)
        assert r.burnout_composite >= 20
        assert r.burnout_pattern == BurnoutPattern.quota_fatigue
        assert "Quota fatigue" in r.burnout_signal

    def test_signal_below_20_healthy_message(self):
        e = fresh_engine()
        inp = make_input()
        sig = e._signal(inp, BurnoutPattern.none, 10.0)
        assert "healthy" in sig.lower()

    def test_signal_at_20_uses_label(self):
        e = fresh_engine()
        inp = make_input(activity_volume_trend_pct=-0.25, training_participation_pct=0.30)
        sig = e._signal(inp, BurnoutPattern.gradual_disengagement, 20.0)
        assert "Gradual disengagement" in sig


# ── 18. assess() public API ───────────────────────────────────────────────────

class TestAssess:
    def test_returns_burnout_result(self):
        assert isinstance(assess(), BurnoutResult)

    def test_rep_id_preserved(self):
        r = assess(rep_id="REP99")
        assert r.rep_id == "REP99"

    def test_region_preserved(self):
        r = assess(region="East")
        assert r.region == "East"

    def test_scores_non_negative(self):
        r = assess()
        assert r.disengagement_score >= 0
        assert r.fatigue_score >= 0
        assert r.sentiment_score >= 0
        assert r.performance_erosion_score >= 0

    def test_composite_non_negative(self):
        assert assess().burnout_composite >= 0

    def test_composite_max_100(self):
        r = assess(activity_volume_trend_pct=-1.0, training_participation_pct=0.0,
                   voluntary_task_completion_pct=0.0, overtime_hours_per_week=30,
                   after_hours_activity_rate_pct=1.0, unplanned_absence_days=10,
                   comp_plan_satisfaction_score=0.0, career_path_clarity_score=0.0,
                   manager_satisfaction_score=0.0, win_rate_trend_pct=-1.0,
                   pipeline_creation_trend_pct=-1.0, consecutive_quota_miss_streak=10)
        assert r.burnout_composite <= 100.0

    def test_result_stored(self):
        e = fresh_engine()
        e.assess(make_input())
        assert len(e._results) == 1

    def test_result_accumulated(self):
        e = fresh_engine()
        e.assess(make_input(rep_id="A"))
        e.assess(make_input(rep_id="B"))
        assert len(e._results) == 2

    def test_healthy_rep_low_risk(self):
        r = assess()
        assert r.burnout_risk == BurnoutRisk.low

    def test_healthy_rep_thriving(self):
        r = assess()
        assert r.burnout_severity == BurnoutSeverity.thriving

    def test_healthy_rep_no_action(self):
        r = assess()
        assert r.recommended_action == BurnoutAction.no_action


# ── 19. assess_batch() ────────────────────────────────────────────────────────

class TestAssessBatch:
    def test_returns_list(self):
        e = fresh_engine()
        results = e.assess_batch([make_input(rep_id="A"), make_input(rep_id="B")])
        assert isinstance(results, list)
        assert len(results) == 2

    def test_each_is_burnout_result(self):
        e = fresh_engine()
        for r in e.assess_batch([make_input(), make_input()]):
            assert isinstance(r, BurnoutResult)

    def test_stored_in_results(self):
        e = fresh_engine()
        e.assess_batch([make_input(rep_id="X"), make_input(rep_id="Y"), make_input(rep_id="Z")])
        assert len(e._results) == 3

    def test_empty_batch(self):
        e = fresh_engine()
        assert e.assess_batch([]) == []

    def test_order_preserved(self):
        e = fresh_engine()
        ids = ["R1", "R2", "R3"]
        results = e.assess_batch([make_input(rep_id=i) for i in ids])
        assert [r.rep_id for r in results] == ids


# ── 20. summary() aggregation ────────────────────────────────────────────────

class TestSummary:
    def test_empty_total(self):
        assert fresh_engine().summary()["total"] == 0

    def test_empty_avg_composite(self):
        assert fresh_engine().summary()["avg_burnout_composite"] == 0.0

    def test_empty_gap_count(self):
        assert fresh_engine().summary()["burnout_gap_count"] == 0

    def test_empty_flight_count(self):
        assert fresh_engine().summary()["flight_risk_count"] == 0

    def test_empty_replacement_cost(self):
        assert fresh_engine().summary()["total_estimated_replacement_cost_usd"] == 0.0

    def test_total_after_batch(self):
        e = fresh_engine()
        e.assess_batch([make_input(), make_input(), make_input()])
        assert e.summary()["total"] == 3

    def test_risk_counts_populated(self):
        e = fresh_engine(); e.assess(make_input())
        counts = e.summary()["risk_counts"]
        assert sum(counts.values()) == 1

    def test_pattern_counts_populated(self):
        e = fresh_engine(); e.assess(make_input())
        counts = e.summary()["pattern_counts"]
        assert sum(counts.values()) == 1

    def test_severity_counts_populated(self):
        e = fresh_engine(); e.assess(make_input())
        counts = e.summary()["severity_counts"]
        assert sum(counts.values()) == 1

    def test_action_counts_populated(self):
        e = fresh_engine(); e.assess(make_input())
        counts = e.summary()["action_counts"]
        assert sum(counts.values()) == 1

    def test_avg_composite_correct(self):
        e = fresh_engine()
        r1 = e.assess(make_input())
        r2 = e.assess(make_input())
        expected = round((r1.burnout_composite + r2.burnout_composite) / 2, 1)
        assert e.summary()["avg_burnout_composite"] == pytest.approx(expected, abs=0.05)

    def test_total_replacement_cost_sums(self):
        e = fresh_engine()
        r1 = e.assess(make_input(tenure_months=12))
        r2 = e.assess(make_input(tenure_months=48))
        expected = round(r1.estimated_replacement_cost_usd + r2.estimated_replacement_cost_usd, 2)
        assert e.summary()["total_estimated_replacement_cost_usd"] == pytest.approx(expected, abs=0.01)

    def test_flight_risk_count(self):
        e = fresh_engine()
        e.assess(make_input(exit_interview_signals=1))
        e.assess(make_input())
        assert e.summary()["flight_risk_count"] == 1

    def test_burnout_gap_count(self):
        e = fresh_engine()
        e.assess(make_input(consecutive_quota_miss_streak=2))
        e.assess(make_input())
        assert e.summary()["burnout_gap_count"] == 1


# ── 21. Engine isolation ──────────────────────────────────────────────────────

class TestEngineIsolation:
    def test_two_engines_independent(self):
        e1 = fresh_engine(); e2 = fresh_engine()
        e1.assess(make_input(rep_id="A"))
        assert e2.summary()["total"] == 0

    def test_results_not_shared(self):
        e1 = fresh_engine(); e2 = fresh_engine()
        e1.assess(make_input())
        e1.assess(make_input())
        e2.assess(make_input())
        assert e1.summary()["total"] == 2
        assert e2.summary()["total"] == 1

    def test_fresh_engine_empty_summary(self):
        e = fresh_engine()
        s = e.summary()
        assert s["total"] == 0
        assert s["risk_counts"] == {}


# ── 22. Edge & boundary cases ─────────────────────────────────────────────────

class TestEdgeCases:
    def test_zero_composite_thriving(self):
        r = assess()
        assert r.burnout_severity == BurnoutSeverity.thriving

    def test_all_fields_at_boundaries_no_crash(self):
        inp = make_input(
            activity_volume_trend_pct=-1.0, win_rate_trend_pct=-1.0,
            pipeline_creation_trend_pct=-1.0, avg_deal_size_trend_pct=-1.0,
            pto_utilization_rate_pct=0.0, unplanned_absence_days=30,
            overtime_hours_per_week=40.0, after_hours_activity_rate_pct=1.0,
            manager_satisfaction_score=0.0, peer_collaboration_score=0.0,
            recognition_received_count=0, voluntary_task_completion_pct=0.0,
            training_participation_pct=0.0, internal_mobility_applications=5,
            tenure_months=120, consecutive_quota_miss_streak=10,
            comp_plan_satisfaction_score=0.0, career_path_clarity_score=0.0,
            exit_interview_signals=1, team_attrition_exposure_pct=1.0,
        )
        r = fresh_engine().assess(inp)
        assert r.burnout_composite == 100.0
        assert r.burnout_risk == BurnoutRisk.critical
        assert r.is_flight_risk is True
        assert r.has_burnout_gap is True

    def test_exact_60_composite_critical(self):
        e = fresh_engine()
        assert e._risk(60.0) == BurnoutRisk.critical
        assert e._severity(60.0) == BurnoutSeverity.flight_risk

    def test_exact_40_composite_high(self):
        e = fresh_engine()
        assert e._risk(40.0) == BurnoutRisk.high
        assert e._severity(40.0) == BurnoutSeverity.burning_out

    def test_exact_20_composite_moderate(self):
        e = fresh_engine()
        assert e._risk(20.0) == BurnoutRisk.moderate
        assert e._severity(20.0) == BurnoutSeverity.straining

    def test_tenure_0_cost_nonnegative(self):
        r = assess(tenure_months=0)
        assert r.estimated_replacement_cost_usd >= 0.0

    def test_single_rep_summary_avg_equals_score(self):
        e = fresh_engine()
        r = e.assess(make_input())
        s = e.summary()
        assert s["avg_burnout_composite"] == pytest.approx(r.burnout_composite, abs=0.1)
