"""Pytest test suite for SalesOnboardingRampIntelligenceEngine."""
from __future__ import annotations
import pytest
from swarm.intelligence.sales_onboarding_ramp_intelligence_engine import (
    SalesOnboardingRampIntelligenceEngine,
    RampInput, RampResult,
    RampRisk, RampPattern, RampSeverity, RampAction,
)


# ── helpers ────────────────────────────────────────────────────────────────────

def make_input(**overrides) -> RampInput:
    """Healthy baseline: composite ≈ 0, all flags False."""
    defaults = dict(
        rep_id="R1", region="NA",
        evaluation_period_id="Q1-2026",
        weeks_since_start=8,
        quota_attainment_vs_ramp_plan_pct=0.90,
        first_meeting_booked_days=5.0,
        first_opportunity_created_days=10.0,
        product_certification_completion_pct=0.95,
        training_module_completion_pct=0.95,
        call_shadowing_sessions_completed=5,
        manager_1on1_frequency_per_month=4.0,
        pipeline_coverage_ratio=3.5,
        avg_deal_size_vs_team_avg_pct=1.0,
        outbound_activity_vs_plan_pct=0.90,
        discovery_call_pass_rate_pct=0.80,
        demo_to_next_step_rate_pct=0.75,
        competitive_win_rate_ramp_pct=0.50,
        peer_buddy_engagement_score=0.90,
        onboarding_satisfaction_score=0.90,
        net_promoter_internal_score=0.90,
        tool_adoption_rate_pct=0.90,
        avg_deal_value_usd=10_000.0,
    )
    defaults.update(overrides)
    return RampInput(**defaults)


def engine() -> SalesOnboardingRampIntelligenceEngine:
    return SalesOnboardingRampIntelligenceEngine()


# ── 1. Enum membership ─────────────────────────────────────────────────────────

class TestEnums:
    def test_ramp_risk_values(self):
        vals = {e.value for e in RampRisk}
        assert vals == {"low", "moderate", "high", "critical"}

    def test_ramp_risk_count(self):
        assert len(RampRisk) == 4

    def test_ramp_pattern_values(self):
        vals = {e.value for e in RampPattern}
        assert vals == {"none", "slow_starter", "knowledge_gap_blocker",
                        "pipeline_builder_fail", "manager_orphan", "confidence_collapse"}

    def test_ramp_pattern_count(self):
        assert len(RampPattern) == 6

    def test_ramp_severity_values(self):
        vals = {e.value for e in RampSeverity}
        assert vals == {"on_track", "at_risk", "behind", "critical"}

    def test_ramp_severity_count(self):
        assert len(RampSeverity) == 4

    def test_ramp_action_values(self):
        vals = {e.value for e in RampAction}
        assert vals == {
            "no_action", "ramp_check_in", "product_knowledge_coaching",
            "pipeline_building_coaching", "manager_engagement_review",
            "structured_ramp_acceleration", "ramp_extension_or_reset",
        }

    def test_ramp_action_count(self):
        assert len(RampAction) == 7

    def test_enums_are_str_subclass(self):
        assert isinstance(RampRisk.low, str)
        assert isinstance(RampPattern.none, str)
        assert isinstance(RampSeverity.on_track, str)
        assert isinstance(RampAction.no_action, str)


# ── 2. RampInput field count ───────────────────────────────────────────────────

class TestRampInputFields:
    def test_field_count(self):
        import dataclasses
        assert len(dataclasses.fields(RampInput)) == 22

    def test_all_named_fields_present(self):
        inp = make_input()
        for attr in (
            "rep_id", "region", "evaluation_period_id", "weeks_since_start",
            "quota_attainment_vs_ramp_plan_pct", "first_meeting_booked_days",
            "first_opportunity_created_days", "product_certification_completion_pct",
            "training_module_completion_pct", "call_shadowing_sessions_completed",
            "manager_1on1_frequency_per_month", "pipeline_coverage_ratio",
            "avg_deal_size_vs_team_avg_pct", "outbound_activity_vs_plan_pct",
            "discovery_call_pass_rate_pct", "demo_to_next_step_rate_pct",
            "competitive_win_rate_ramp_pct", "peer_buddy_engagement_score",
            "onboarding_satisfaction_score", "net_promoter_internal_score",
            "tool_adoption_rate_pct", "avg_deal_value_usd",
        ):
            assert hasattr(inp, attr), f"Missing field: {attr}"


# ── 3. RampResult to_dict key count = 15 ──────────────────────────────────────

class TestToDict:
    def test_key_count(self):
        res = engine().assess(make_input())
        assert len(res.to_dict()) == 15

    def test_exact_keys(self):
        d = engine().assess(make_input()).to_dict()
        expected = {
            "rep_id", "region", "ramp_risk", "ramp_pattern", "ramp_severity",
            "recommended_action", "readiness_score", "activity_score",
            "pipeline_score", "manager_support_score", "ramp_composite",
            "has_ramp_gap", "requires_ramp_intervention",
            "estimated_ramp_revenue_risk_usd", "ramp_signal",
        }
        assert set(d.keys()) == expected

    def test_enum_values_are_strings(self):
        d = engine().assess(make_input()).to_dict()
        assert isinstance(d["ramp_risk"], str)
        assert isinstance(d["ramp_pattern"], str)
        assert isinstance(d["ramp_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_rep_id_region_passthrough(self):
        d = engine().assess(make_input(rep_id="X99", region="EMEA")).to_dict()
        assert d["rep_id"] == "X99"
        assert d["region"] == "EMEA"


# ── 4. summary() key count = 13 ───────────────────────────────────────────────

class TestSummaryKeys:
    def test_empty_summary_key_count(self):
        assert len(engine().summary()) == 13

    def test_non_empty_summary_key_count(self):
        eng = engine()
        eng.assess(make_input())
        assert len(eng.summary()) == 13

    def test_empty_summary_values(self):
        s = engine().summary()
        assert s["total"] == 0
        assert s["avg_ramp_composite"] == 0.0
        assert s["ramp_gap_count"] == 0
        assert s["intervention_count"] == 0

    def test_summary_exact_keys(self):
        s = engine().summary()
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_ramp_composite", "ramp_gap_count",
            "intervention_count", "avg_readiness_score", "avg_activity_score",
            "avg_pipeline_score", "avg_manager_support_score",
            "total_estimated_ramp_revenue_risk_usd",
        }
        assert set(s.keys()) == expected


# ── 5. Readiness sub-score ─────────────────────────────────────────────────────

class TestReadinessScore:
    def _re(self, **kw):
        return engine()._readiness_score(make_input(**kw))

    # cert bands
    def test_cert_le_030(self):
        assert self._re(product_certification_completion_pct=0.10) >= 40

    def test_cert_le_060(self):
        s = self._re(product_certification_completion_pct=0.45,
                     training_module_completion_pct=0.95,
                     tool_adoption_rate_pct=0.90)
        assert s == 22

    def test_cert_le_080(self):
        s = self._re(product_certification_completion_pct=0.70,
                     training_module_completion_pct=0.95,
                     tool_adoption_rate_pct=0.90)
        assert s == 8

    def test_cert_above_080(self):
        s = self._re(product_certification_completion_pct=0.90,
                     training_module_completion_pct=0.95,
                     tool_adoption_rate_pct=0.90)
        assert s == 0

    # training bands
    def test_training_le_030(self):
        s = self._re(product_certification_completion_pct=0.90,
                     training_module_completion_pct=0.20,
                     tool_adoption_rate_pct=0.90)
        assert s == 35

    def test_training_le_060(self):
        s = self._re(product_certification_completion_pct=0.90,
                     training_module_completion_pct=0.50,
                     tool_adoption_rate_pct=0.90)
        assert s == 18

    def test_training_above_060(self):
        s = self._re(product_certification_completion_pct=0.90,
                     training_module_completion_pct=0.90,
                     tool_adoption_rate_pct=0.90)
        assert s == 0

    # tool bands
    def test_tool_le_030(self):
        s = self._re(product_certification_completion_pct=0.90,
                     training_module_completion_pct=0.90,
                     tool_adoption_rate_pct=0.20)
        assert s == 25

    def test_tool_le_060(self):
        s = self._re(product_certification_completion_pct=0.90,
                     training_module_completion_pct=0.90,
                     tool_adoption_rate_pct=0.50)
        assert s == 12

    def test_tool_above_060(self):
        s = self._re(product_certification_completion_pct=0.90,
                     training_module_completion_pct=0.90,
                     tool_adoption_rate_pct=0.90)
        assert s == 0

    def test_readiness_capped_at_100(self):
        s = self._re(product_certification_completion_pct=0.10,
                     training_module_completion_pct=0.10,
                     tool_adoption_rate_pct=0.10)
        assert s == 100.0


# ── 6. Activity sub-score ──────────────────────────────────────────────────────

class TestActivityScore:
    def _ac(self, **kw):
        return engine()._activity_score(make_input(**kw))

    def test_outbound_le_040(self):
        s = self._ac(outbound_activity_vs_plan_pct=0.30,
                     first_meeting_booked_days=5.0,
                     discovery_call_pass_rate_pct=0.80)
        assert s == 45

    def test_outbound_le_065(self):
        s = self._ac(outbound_activity_vs_plan_pct=0.55,
                     first_meeting_booked_days=5.0,
                     discovery_call_pass_rate_pct=0.80)
        assert s == 25

    def test_outbound_le_085(self):
        s = self._ac(outbound_activity_vs_plan_pct=0.75,
                     first_meeting_booked_days=5.0,
                     discovery_call_pass_rate_pct=0.80)
        assert s == 10

    def test_outbound_above_085(self):
        s = self._ac(outbound_activity_vs_plan_pct=0.90,
                     first_meeting_booked_days=5.0,
                     discovery_call_pass_rate_pct=0.80)
        assert s == 0

    def test_first_meeting_ge_021(self):
        s = self._ac(outbound_activity_vs_plan_pct=0.90,
                     first_meeting_booked_days=25.0,
                     discovery_call_pass_rate_pct=0.80)
        assert s == 30

    def test_first_meeting_ge_012(self):
        s = self._ac(outbound_activity_vs_plan_pct=0.90,
                     first_meeting_booked_days=15.0,
                     discovery_call_pass_rate_pct=0.80)
        assert s == 15

    def test_first_meeting_below_012(self):
        s = self._ac(outbound_activity_vs_plan_pct=0.90,
                     first_meeting_booked_days=5.0,
                     discovery_call_pass_rate_pct=0.80)
        assert s == 0

    def test_discovery_le_025(self):
        s = self._ac(outbound_activity_vs_plan_pct=0.90,
                     first_meeting_booked_days=5.0,
                     discovery_call_pass_rate_pct=0.20)
        assert s == 25

    def test_discovery_le_050(self):
        s = self._ac(outbound_activity_vs_plan_pct=0.90,
                     first_meeting_booked_days=5.0,
                     discovery_call_pass_rate_pct=0.40)
        assert s == 12

    def test_discovery_above_050(self):
        s = self._ac(outbound_activity_vs_plan_pct=0.90,
                     first_meeting_booked_days=5.0,
                     discovery_call_pass_rate_pct=0.80)
        assert s == 0

    def test_activity_capped_at_100(self):
        s = self._ac(outbound_activity_vs_plan_pct=0.10,
                     first_meeting_booked_days=30.0,
                     discovery_call_pass_rate_pct=0.10)
        assert s == 100.0


# ── 7. Pipeline sub-score ──────────────────────────────────────────────────────

class TestPipelineScore:
    def _pi(self, **kw):
        return engine()._pipeline_score(make_input(**kw))

    def test_quota_le_030(self):
        s = self._pi(quota_attainment_vs_ramp_plan_pct=0.20,
                     pipeline_coverage_ratio=3.5,
                     first_opportunity_created_days=10.0)
        assert s == 40

    def test_quota_le_060(self):
        s = self._pi(quota_attainment_vs_ramp_plan_pct=0.50,
                     pipeline_coverage_ratio=3.5,
                     first_opportunity_created_days=10.0)
        assert s == 22

    def test_quota_le_085(self):
        s = self._pi(quota_attainment_vs_ramp_plan_pct=0.75,
                     pipeline_coverage_ratio=3.5,
                     first_opportunity_created_days=10.0)
        assert s == 8

    def test_quota_above_085(self):
        s = self._pi(quota_attainment_vs_ramp_plan_pct=0.90,
                     pipeline_coverage_ratio=3.5,
                     first_opportunity_created_days=10.0)
        assert s == 0

    def test_coverage_le_10(self):
        s = self._pi(quota_attainment_vs_ramp_plan_pct=0.90,
                     pipeline_coverage_ratio=0.8,
                     first_opportunity_created_days=10.0)
        assert s == 35

    def test_coverage_le_20(self):
        s = self._pi(quota_attainment_vs_ramp_plan_pct=0.90,
                     pipeline_coverage_ratio=1.5,
                     first_opportunity_created_days=10.0)
        assert s == 18

    def test_coverage_above_20(self):
        s = self._pi(quota_attainment_vs_ramp_plan_pct=0.90,
                     pipeline_coverage_ratio=3.5,
                     first_opportunity_created_days=10.0)
        assert s == 0

    def test_opp_created_ge_030(self):
        s = self._pi(quota_attainment_vs_ramp_plan_pct=0.90,
                     pipeline_coverage_ratio=3.5,
                     first_opportunity_created_days=35.0)
        assert s == 25

    def test_opp_created_ge_018(self):
        s = self._pi(quota_attainment_vs_ramp_plan_pct=0.90,
                     pipeline_coverage_ratio=3.5,
                     first_opportunity_created_days=20.0)
        assert s == 12

    def test_opp_created_below_018(self):
        s = self._pi(quota_attainment_vs_ramp_plan_pct=0.90,
                     pipeline_coverage_ratio=3.5,
                     first_opportunity_created_days=10.0)
        assert s == 0

    def test_pipeline_capped_at_100(self):
        s = self._pi(quota_attainment_vs_ramp_plan_pct=0.10,
                     pipeline_coverage_ratio=0.5,
                     first_opportunity_created_days=40.0)
        assert s == 100.0


# ── 8. Manager support sub-score ──────────────────────────────────────────────

class TestManagerSupportScore:
    def _ms(self, **kw):
        return engine()._manager_support_score(make_input(**kw))

    def test_1on1_le_10(self):
        s = self._ms(manager_1on1_frequency_per_month=0.5,
                     call_shadowing_sessions_completed=5,
                     peer_buddy_engagement_score=0.90)
        assert s == 45

    def test_1on1_le_20(self):
        s = self._ms(manager_1on1_frequency_per_month=1.5,
                     call_shadowing_sessions_completed=5,
                     peer_buddy_engagement_score=0.90)
        assert s == 25

    def test_1on1_le_30(self):
        s = self._ms(manager_1on1_frequency_per_month=2.5,
                     call_shadowing_sessions_completed=5,
                     peer_buddy_engagement_score=0.90)
        assert s == 10

    def test_1on1_above_30(self):
        s = self._ms(manager_1on1_frequency_per_month=4.0,
                     call_shadowing_sessions_completed=5,
                     peer_buddy_engagement_score=0.90)
        assert s == 0

    def test_shadowing_le_1(self):
        s = self._ms(manager_1on1_frequency_per_month=4.0,
                     call_shadowing_sessions_completed=1,
                     peer_buddy_engagement_score=0.90)
        assert s == 30

    def test_shadowing_le_3(self):
        s = self._ms(manager_1on1_frequency_per_month=4.0,
                     call_shadowing_sessions_completed=2,
                     peer_buddy_engagement_score=0.90)
        assert s == 15

    def test_shadowing_above_3(self):
        s = self._ms(manager_1on1_frequency_per_month=4.0,
                     call_shadowing_sessions_completed=5,
                     peer_buddy_engagement_score=0.90)
        assert s == 0

    def test_buddy_le_020(self):
        s = self._ms(manager_1on1_frequency_per_month=4.0,
                     call_shadowing_sessions_completed=5,
                     peer_buddy_engagement_score=0.10)
        assert s == 25

    def test_buddy_le_050(self):
        s = self._ms(manager_1on1_frequency_per_month=4.0,
                     call_shadowing_sessions_completed=5,
                     peer_buddy_engagement_score=0.35)
        assert s == 12

    def test_buddy_above_050(self):
        s = self._ms(manager_1on1_frequency_per_month=4.0,
                     call_shadowing_sessions_completed=5,
                     peer_buddy_engagement_score=0.90)
        assert s == 0

    def test_manager_support_capped_at_100(self):
        s = self._ms(manager_1on1_frequency_per_month=0.5,
                     call_shadowing_sessions_completed=0,
                     peer_buddy_engagement_score=0.05)
        assert s == 100.0


# ── 9. Composite weighting ─────────────────────────────────────────────────────

class TestComposite:
    def test_weights_sum(self):
        assert 0.25 + 0.30 + 0.30 + 0.15 == pytest.approx(1.0)

    def test_composite_formula(self):
        eng = engine()
        assert eng._composite(100, 0, 0, 0) == pytest.approx(25.0)
        assert eng._composite(0, 100, 0, 0) == pytest.approx(30.0)
        assert eng._composite(0, 0, 100, 0) == pytest.approx(30.0)
        assert eng._composite(0, 0, 0, 100) == pytest.approx(15.0)

    def test_composite_full_score(self):
        assert engine()._composite(100, 100, 100, 100) == pytest.approx(100.0)

    def test_composite_zero(self):
        assert engine()._composite(0, 0, 0, 0) == pytest.approx(0.0)

    def test_composite_capped_at_100(self):
        assert engine()._composite(200, 200, 200, 200) == 100.0

    def test_composite_rounded_to_2dp(self):
        c = engine()._composite(33, 33, 33, 33)
        assert c == round(33 * 0.25 + 33 * 0.30 + 33 * 0.30 + 33 * 0.15, 2)


# ── 10. Risk thresholds ────────────────────────────────────────────────────────

class TestRisk:
    def test_risk_critical(self):
        assert engine()._risk(60.0) == RampRisk.critical
        assert engine()._risk(100.0) == RampRisk.critical

    def test_risk_high(self):
        assert engine()._risk(40.0) == RampRisk.high
        assert engine()._risk(59.9) == RampRisk.high

    def test_risk_moderate(self):
        assert engine()._risk(20.0) == RampRisk.moderate
        assert engine()._risk(39.9) == RampRisk.moderate

    def test_risk_low(self):
        assert engine()._risk(0.0) == RampRisk.low
        assert engine()._risk(19.9) == RampRisk.low

    def test_risk_boundary_60(self):
        assert engine()._risk(60.0) == RampRisk.critical

    def test_risk_boundary_40(self):
        assert engine()._risk(40.0) == RampRisk.high

    def test_risk_boundary_20(self):
        assert engine()._risk(20.0) == RampRisk.moderate


# ── 11. Severity thresholds ───────────────────────────────────────────────────

class TestSeverity:
    def test_severity_critical(self):
        assert engine()._severity(60.0) == RampSeverity.critical
        assert engine()._severity(100.0) == RampSeverity.critical

    def test_severity_behind(self):
        assert engine()._severity(40.0) == RampSeverity.behind
        assert engine()._severity(59.9) == RampSeverity.behind

    def test_severity_at_risk(self):
        assert engine()._severity(20.0) == RampSeverity.at_risk
        assert engine()._severity(39.9) == RampSeverity.at_risk

    def test_severity_on_track(self):
        assert engine()._severity(0.0) == RampSeverity.on_track
        assert engine()._severity(19.9) == RampSeverity.on_track

    def test_severity_boundary_60(self):
        assert engine()._severity(60.0) == RampSeverity.critical

    def test_severity_boundary_40(self):
        assert engine()._severity(40.0) == RampSeverity.behind

    def test_severity_boundary_20(self):
        assert engine()._severity(20.0) == RampSeverity.at_risk


# ── 12. Action routing ────────────────────────────────────────────────────────

class TestAction:
    def _act(self, risk, pattern):
        return engine()._action(risk, pattern)

    # critical
    def test_critical_pipeline_fail(self):
        assert self._act(RampRisk.critical, RampPattern.pipeline_builder_fail) == RampAction.ramp_extension_or_reset

    def test_critical_slow_starter(self):
        assert self._act(RampRisk.critical, RampPattern.slow_starter) == RampAction.ramp_extension_or_reset

    def test_critical_knowledge_gap(self):
        assert self._act(RampRisk.critical, RampPattern.knowledge_gap_blocker) == RampAction.structured_ramp_acceleration

    def test_critical_manager_orphan(self):
        assert self._act(RampRisk.critical, RampPattern.manager_orphan) == RampAction.structured_ramp_acceleration

    def test_critical_confidence_collapse(self):
        assert self._act(RampRisk.critical, RampPattern.confidence_collapse) == RampAction.structured_ramp_acceleration

    def test_critical_none_pattern(self):
        assert self._act(RampRisk.critical, RampPattern.none) == RampAction.structured_ramp_acceleration

    # high
    def test_high_slow_starter(self):
        assert self._act(RampRisk.high, RampPattern.slow_starter) == RampAction.pipeline_building_coaching

    def test_high_knowledge_gap(self):
        assert self._act(RampRisk.high, RampPattern.knowledge_gap_blocker) == RampAction.product_knowledge_coaching

    def test_high_pipeline_fail(self):
        assert self._act(RampRisk.high, RampPattern.pipeline_builder_fail) == RampAction.pipeline_building_coaching

    def test_high_manager_orphan(self):
        assert self._act(RampRisk.high, RampPattern.manager_orphan) == RampAction.manager_engagement_review

    def test_high_confidence_collapse(self):
        assert self._act(RampRisk.high, RampPattern.confidence_collapse) == RampAction.structured_ramp_acceleration

    def test_high_none_pattern(self):
        assert self._act(RampRisk.high, RampPattern.none) == RampAction.pipeline_building_coaching

    # moderate
    def test_moderate_any_pattern(self):
        for p in RampPattern:
            assert self._act(RampRisk.moderate, p) == RampAction.ramp_check_in

    # low
    def test_low_any_pattern(self):
        for p in RampPattern:
            assert self._act(RampRisk.low, p) == RampAction.no_action


# ── 13. Pattern detection ─────────────────────────────────────────────────────

class TestPattern:
    def _pat(self, **kw):
        return engine()._pattern(make_input(**kw))

    def test_slow_starter(self):
        p = self._pat(outbound_activity_vs_plan_pct=0.30,
                      first_meeting_booked_days=25.0)
        assert p == RampPattern.slow_starter

    def test_knowledge_gap_blocker(self):
        p = self._pat(product_certification_completion_pct=0.30,
                      training_module_completion_pct=0.30)
        assert p == RampPattern.knowledge_gap_blocker

    def test_pipeline_builder_fail(self):
        p = self._pat(pipeline_coverage_ratio=0.8,
                      quota_attainment_vs_ramp_plan_pct=0.30)
        assert p == RampPattern.pipeline_builder_fail

    def test_manager_orphan(self):
        p = self._pat(manager_1on1_frequency_per_month=0.5,
                      call_shadowing_sessions_completed=2)
        assert p == RampPattern.manager_orphan

    def test_confidence_collapse(self):
        p = self._pat(onboarding_satisfaction_score=0.20,
                      net_promoter_internal_score=0.20)
        assert p == RampPattern.confidence_collapse

    def test_no_pattern_healthy(self):
        assert self._pat() == RampPattern.none

    # Priority: slow_starter beats knowledge_gap_blocker
    def test_slow_starter_priority_over_knowledge_gap(self):
        p = self._pat(
            outbound_activity_vs_plan_pct=0.30,
            first_meeting_booked_days=25.0,
            product_certification_completion_pct=0.30,
            training_module_completion_pct=0.30,
        )
        assert p == RampPattern.slow_starter

    # Priority: knowledge_gap_blocker beats pipeline_builder_fail
    def test_knowledge_gap_priority_over_pipeline_fail(self):
        p = self._pat(
            product_certification_completion_pct=0.30,
            training_module_completion_pct=0.30,
            pipeline_coverage_ratio=0.8,
            quota_attainment_vs_ramp_plan_pct=0.30,
        )
        assert p == RampPattern.knowledge_gap_blocker

    # Priority: pipeline_builder_fail beats manager_orphan
    def test_pipeline_fail_priority_over_manager_orphan(self):
        p = self._pat(
            pipeline_coverage_ratio=0.8,
            quota_attainment_vs_ramp_plan_pct=0.30,
            manager_1on1_frequency_per_month=0.5,
            call_shadowing_sessions_completed=2,
        )
        assert p == RampPattern.pipeline_builder_fail

    # Priority: manager_orphan beats confidence_collapse
    def test_manager_orphan_priority_over_confidence_collapse(self):
        p = self._pat(
            manager_1on1_frequency_per_month=0.5,
            call_shadowing_sessions_completed=2,
            onboarding_satisfaction_score=0.20,
            net_promoter_internal_score=0.20,
        )
        assert p == RampPattern.manager_orphan

    # Boundary: just above slow_starter threshold
    def test_slow_starter_boundary_not_triggered(self):
        p = self._pat(outbound_activity_vs_plan_pct=0.41,
                      first_meeting_booked_days=20.9)
        assert p == RampPattern.none

    # Exact boundary for manager_orphan (<=2 call_shadowing)
    def test_manager_orphan_shadowing_boundary(self):
        p = self._pat(manager_1on1_frequency_per_month=0.5,
                      call_shadowing_sessions_completed=2)
        assert p == RampPattern.manager_orphan

    def test_manager_orphan_shadowing_above_boundary(self):
        p = self._pat(manager_1on1_frequency_per_month=0.5,
                      call_shadowing_sessions_completed=3)
        # manager_1on1 still <=1 but shadowing >2, should not be manager_orphan
        assert p != RampPattern.manager_orphan


# ── 14. Flags ─────────────────────────────────────────────────────────────────

class TestFlags:
    def test_has_ramp_gap_via_composite(self):
        eng = engine()
        inp = make_input()
        assert eng._has_ramp_gap(inp, 40.0) is True

    def test_no_ramp_gap_clean(self):
        eng = engine()
        inp = make_input(quota_attainment_vs_ramp_plan_pct=0.90,
                         pipeline_coverage_ratio=3.5)
        assert eng._has_ramp_gap(inp, 10.0) is False

    def test_has_ramp_gap_via_quota(self):
        eng = engine()
        inp = make_input(quota_attainment_vs_ramp_plan_pct=0.60,
                         pipeline_coverage_ratio=3.5)
        assert eng._has_ramp_gap(inp, 10.0) is True

    def test_has_ramp_gap_via_coverage(self):
        eng = engine()
        inp = make_input(quota_attainment_vs_ramp_plan_pct=0.90,
                         pipeline_coverage_ratio=2.0)
        assert eng._has_ramp_gap(inp, 10.0) is True

    def test_requires_intervention_via_composite(self):
        eng = engine()
        inp = make_input(outbound_activity_vs_plan_pct=0.90,
                         product_certification_completion_pct=0.90)
        assert eng._requires_intervention(inp, 25.0) is True

    def test_no_intervention_clean(self):
        eng = engine()
        inp = make_input(outbound_activity_vs_plan_pct=0.90,
                         product_certification_completion_pct=0.90)
        assert eng._requires_intervention(inp, 10.0) is False

    def test_requires_intervention_via_activity(self):
        eng = engine()
        inp = make_input(outbound_activity_vs_plan_pct=0.65,
                         product_certification_completion_pct=0.90)
        assert eng._requires_intervention(inp, 10.0) is True

    def test_requires_intervention_via_cert(self):
        eng = engine()
        inp = make_input(outbound_activity_vs_plan_pct=0.90,
                         product_certification_completion_pct=0.60)
        assert eng._requires_intervention(inp, 10.0) is True


# ── 15. Revenue risk formula ──────────────────────────────────────────────────

class TestRevenueRisk:
    def test_zero_when_full_attainment(self):
        eng = engine()
        inp = make_input(quota_attainment_vs_ramp_plan_pct=1.0, avg_deal_value_usd=10_000.0)
        assert eng._ramp_revenue_risk(inp, 50.0) == 0.0

    def test_zero_when_composite_zero(self):
        eng = engine()
        inp = make_input(quota_attainment_vs_ramp_plan_pct=0.5, avg_deal_value_usd=10_000.0)
        assert eng._ramp_revenue_risk(inp, 0.0) == 0.0

    def test_formula_calculation(self):
        eng = engine()
        inp = make_input(quota_attainment_vs_ramp_plan_pct=0.5, avg_deal_value_usd=10_000.0)
        # 10000 * 4 * (1-0.5) * (50/100) = 40000 * 0.5 * 0.5 = 10000
        assert eng._ramp_revenue_risk(inp, 50.0) == 10_000.0

    def test_formula_rounded_to_2dp(self):
        eng = engine()
        inp = make_input(quota_attainment_vs_ramp_plan_pct=0.333, avg_deal_value_usd=10_000.0)
        result = eng._ramp_revenue_risk(inp, 33.33)
        expected = round(10_000 * 4 * max(0, 1 - 0.333) * (33.33 / 100), 2)
        assert result == expected

    def test_shortfall_clamped_at_zero(self):
        eng = engine()
        inp = make_input(quota_attainment_vs_ramp_plan_pct=1.5, avg_deal_value_usd=10_000.0)
        assert eng._ramp_revenue_risk(inp, 50.0) == 0.0

    def test_revenue_risk_in_result(self):
        inp = make_input(quota_attainment_vs_ramp_plan_pct=0.50,
                         avg_deal_value_usd=5_000.0)
        res = engine().assess(inp)
        assert res.estimated_ramp_revenue_risk_usd >= 0.0


# ── 16. Signal text ──────────────────────────────────────────────────────────

class TestSignal:
    def test_healthy_signal(self):
        res = engine().assess(make_input())
        assert "healthy" in res.ramp_signal.lower()

    def test_signal_contains_composite_when_risky(self):
        inp = make_input(
            outbound_activity_vs_plan_pct=0.10,
            first_meeting_booked_days=30.0,
            product_certification_completion_pct=0.10,
            training_module_completion_pct=0.10,
            quota_attainment_vs_ramp_plan_pct=0.10,
            pipeline_coverage_ratio=0.5,
            discovery_call_pass_rate_pct=0.10,
        )
        res = engine().assess(inp)
        assert "composite" in res.ramp_signal.lower()

    def test_signal_contains_attainment_pct(self):
        inp = make_input(
            quota_attainment_vs_ramp_plan_pct=0.50,
            outbound_activity_vs_plan_pct=0.30,
            first_meeting_booked_days=25.0,
        )
        res = engine().assess(inp)
        if res.ramp_composite >= 20:
            assert "50%" in res.ramp_signal

    def test_signal_contains_pattern_label(self):
        inp = make_input(
            outbound_activity_vs_plan_pct=0.30,
            first_meeting_booked_days=25.0,
        )
        res = engine().assess(inp)
        if res.ramp_pattern == RampPattern.slow_starter:
            assert "Slow starter" in res.ramp_signal


# ── 17. assess() round-trip ───────────────────────────────────────────────────

class TestAssess:
    def test_returns_ramp_result(self):
        res = engine().assess(make_input())
        assert isinstance(res, RampResult)

    def test_result_stored(self):
        eng = engine()
        eng.assess(make_input())
        assert len(eng._results) == 1

    def test_rep_id_preserved(self):
        res = engine().assess(make_input(rep_id="TEST123"))
        assert res.rep_id == "TEST123"

    def test_region_preserved(self):
        res = engine().assess(make_input(region="APAC"))
        assert res.region == "APAC"

    def test_healthy_rep_low_risk(self):
        res = engine().assess(make_input())
        assert res.ramp_risk == RampRisk.low
        assert res.ramp_severity == RampSeverity.on_track
        assert res.recommended_action == RampAction.no_action

    def test_worst_case_critical(self):
        inp = make_input(
            outbound_activity_vs_plan_pct=0.10,
            first_meeting_booked_days=30.0,
            product_certification_completion_pct=0.10,
            training_module_completion_pct=0.10,
            quota_attainment_vs_ramp_plan_pct=0.10,
            pipeline_coverage_ratio=0.5,
            manager_1on1_frequency_per_month=0.5,
            call_shadowing_sessions_completed=0,
            peer_buddy_engagement_score=0.05,
            discovery_call_pass_rate_pct=0.10,
            tool_adoption_rate_pct=0.10,
        )
        res = engine().assess(inp)
        assert res.ramp_risk == RampRisk.critical
        assert res.ramp_composite >= 60.0

    def test_all_result_fields_present(self):
        res = engine().assess(make_input())
        for attr in (
            "rep_id", "region", "ramp_risk", "ramp_pattern", "ramp_severity",
            "recommended_action", "readiness_score", "activity_score",
            "pipeline_score", "manager_support_score", "ramp_composite",
            "has_ramp_gap", "requires_ramp_intervention",
            "estimated_ramp_revenue_risk_usd", "ramp_signal",
        ):
            assert hasattr(res, attr)

    def test_composite_reflects_subscores(self):
        inp = make_input()
        eng = engine()
        res = eng.assess(inp)
        expected = eng._composite(
            res.readiness_score, res.activity_score,
            res.pipeline_score, res.manager_support_score
        )
        assert res.ramp_composite == pytest.approx(expected)


# ── 18. assess_batch() ────────────────────────────────────────────────────────

class TestAssessBatch:
    def test_returns_list(self):
        results = engine().assess_batch([make_input(), make_input(rep_id="R2")])
        assert isinstance(results, list)

    def test_correct_length(self):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = engine().assess_batch(inputs)
        assert len(results) == 5

    def test_each_result_is_ramp_result(self):
        for r in engine().assess_batch([make_input(), make_input(rep_id="R2")]):
            assert isinstance(r, RampResult)

    def test_results_accumulated(self):
        eng = engine()
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        assert len(eng._results) == 3

    def test_empty_batch(self):
        assert engine().assess_batch([]) == []

    def test_batch_order_preserved(self):
        inputs = [make_input(rep_id=f"REP{i}") for i in range(4)]
        results = engine().assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"REP{i}"


# ── 19. summary() aggregation ────────────────────────────────────────────────

class TestSummaryAggregation:
    def test_total_count(self):
        eng = engine()
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(7)])
        assert eng.summary()["total"] == 7

    def test_risk_counts_sum(self):
        eng = engine()
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        s = eng.summary()
        assert sum(s["risk_counts"].values()) == 5

    def test_pattern_counts_sum(self):
        eng = engine()
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        s = eng.summary()
        assert sum(s["pattern_counts"].values()) == 5

    def test_severity_counts_sum(self):
        eng = engine()
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        s = eng.summary()
        assert sum(s["severity_counts"].values()) == 5

    def test_action_counts_sum(self):
        eng = engine()
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        s = eng.summary()
        assert sum(s["action_counts"].values()) == 5

    def test_gap_count_tracking(self):
        eng = engine()
        # healthy rep: no gap
        eng.assess(make_input(quota_attainment_vs_ramp_plan_pct=0.90,
                               pipeline_coverage_ratio=3.5))
        # risky: gap
        eng.assess(make_input(quota_attainment_vs_ramp_plan_pct=0.50,
                               pipeline_coverage_ratio=1.5))
        s = eng.summary()
        assert s["ramp_gap_count"] >= 1

    def test_avg_composite_is_numeric(self):
        eng = engine()
        eng.assess(make_input())
        s = eng.summary()
        assert isinstance(s["avg_ramp_composite"], float)

    def test_total_revenue_risk_is_sum(self):
        eng = engine()
        r1 = eng.assess(make_input(avg_deal_value_usd=10_000.0,
                                    quota_attainment_vs_ramp_plan_pct=0.50))
        r2 = eng.assess(make_input(avg_deal_value_usd=5_000.0,
                                    quota_attainment_vs_ramp_plan_pct=0.50))
        s = eng.summary()
        expected = round(r1.estimated_ramp_revenue_risk_usd + r2.estimated_ramp_revenue_risk_usd, 2)
        assert s["total_estimated_ramp_revenue_risk_usd"] == pytest.approx(expected)

    def test_avg_subscores_computed(self):
        eng = engine()
        eng.assess(make_input())
        s = eng.summary()
        assert s["avg_readiness_score"] >= 0.0
        assert s["avg_activity_score"] >= 0.0
        assert s["avg_pipeline_score"] >= 0.0
        assert s["avg_manager_support_score"] >= 0.0


# ── 20. Engine isolation ──────────────────────────────────────────────────────

class TestEngineIsolation:
    def test_separate_engines_independent(self):
        e1, e2 = engine(), engine()
        e1.assess(make_input())
        assert len(e2._results) == 0

    def test_fresh_engine_empty_results(self):
        assert len(engine()._results) == 0

    def test_multiple_calls_accumulate(self):
        eng = engine()
        for i in range(10):
            eng.assess(make_input(rep_id=f"R{i}"))
        assert len(eng._results) == 10

    def test_summary_only_own_results(self):
        e1, e2 = engine(), engine()
        e1.assess(make_input())
        e1.assess(make_input(rep_id="R2"))
        e2.assess(make_input(rep_id="R3"))
        assert e1.summary()["total"] == 2
        assert e2.summary()["total"] == 1


# ── 21. Edge cases ────────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_quota_exactly_060_triggers_gap(self):
        eng = engine()
        inp = make_input(quota_attainment_vs_ramp_plan_pct=0.60,
                         pipeline_coverage_ratio=3.5)
        assert eng._has_ramp_gap(inp, 10.0) is True

    def test_quota_just_above_060_no_gap(self):
        eng = engine()
        inp = make_input(quota_attainment_vs_ramp_plan_pct=0.61,
                         pipeline_coverage_ratio=3.5)
        assert eng._has_ramp_gap(inp, 10.0) is False

    def test_coverage_exactly_20_triggers_gap(self):
        eng = engine()
        inp = make_input(quota_attainment_vs_ramp_plan_pct=0.90,
                         pipeline_coverage_ratio=2.0)
        assert eng._has_ramp_gap(inp, 10.0) is True

    def test_activity_exactly_065_triggers_intervention(self):
        eng = engine()
        inp = make_input(outbound_activity_vs_plan_pct=0.65,
                         product_certification_completion_pct=0.90)
        assert eng._requires_intervention(inp, 10.0) is True

    def test_cert_exactly_060_triggers_intervention(self):
        eng = engine()
        inp = make_input(outbound_activity_vs_plan_pct=0.90,
                         product_certification_completion_pct=0.60)
        assert eng._requires_intervention(inp, 10.0) is True

    def test_composite_exactly_25_triggers_intervention(self):
        eng = engine()
        inp = make_input(outbound_activity_vs_plan_pct=0.90,
                         product_certification_completion_pct=0.90)
        assert eng._requires_intervention(inp, 25.0) is True

    def test_zero_deal_value_zero_revenue_risk(self):
        res = engine().assess(make_input(avg_deal_value_usd=0.0))
        assert res.estimated_ramp_revenue_risk_usd == 0.0

    def test_single_batch_item(self):
        results = engine().assess_batch([make_input()])
        assert len(results) == 1

    def test_to_dict_booleans_type(self):
        d = engine().assess(make_input()).to_dict()
        assert isinstance(d["has_ramp_gap"], bool)
        assert isinstance(d["requires_ramp_intervention"], bool)

    def test_ramp_composite_non_negative(self):
        res = engine().assess(make_input())
        assert res.ramp_composite >= 0.0

    def test_subscores_non_negative(self):
        res = engine().assess(make_input())
        assert res.readiness_score >= 0.0
        assert res.activity_score >= 0.0
        assert res.pipeline_score >= 0.0
        assert res.manager_support_score >= 0.0
