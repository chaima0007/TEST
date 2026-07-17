"""Tests for Module 216 — SalesRepBurnoutProductivityDecayEngine"""
import pytest
from swarm.intelligence.sales_rep_burnout_productivity_decay_engine import (
    BurnoutRisk, BurnoutPattern, BurnoutSeverity, BurnoutAction,
    BurnoutInput, BurnoutResult,
    SalesRepBurnoutProductivityDecayEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_DEFAULTS = dict(
    rep_id="REP-001", region="EMEA", evaluation_period_id="Q2-2026",
    outbound_activity_decay_rate_pct=0.05, meetings_booked_decay_rate_pct=0.05,
    pipeline_creation_decay_rate_pct=0.05, avg_response_time_increase_pct=0.05,
    proposal_error_rate_pct=0.03, crm_entry_accuracy_drop_pct=0.02,
    follow_up_timeliness_score=0.90, call_quality_score_decay_pct=0.02,
    manager_meeting_attendance_rate_pct=0.95, team_activity_participation_rate_pct=0.90,
    enablement_session_attendance_rate_pct=0.85, voluntary_overtime_rate_pct=0.05,
    weekend_work_frequency_pct=0.05, avg_daily_work_hours=7.5, vacation_utilization_pct=0.80,
    deal_abandonment_rate_pct=0.03, prospecting_avoidance_rate_pct=0.05,
    quota_attainment_trend=0.95, total_active_deals=10, avg_deal_value_usd=5000.0,
)

def make_input(**overrides) -> BurnoutInput:
    return BurnoutInput(**{**_DEFAULTS, **overrides})


@pytest.fixture
def engine():
    return SalesRepBurnoutProductivityDecayEngine()

# ---------------------------------------------------------------------------
# Enum completeness
# ---------------------------------------------------------------------------

class TestEnums:
    def test_burnout_risk_has_4_values(self):
        assert len(BurnoutRisk) == 4
        assert {r.value for r in BurnoutRisk} == {"low", "moderate", "high", "critical"}

    def test_burnout_pattern_has_6_values(self):
        assert len(BurnoutPattern) == 6
        expected = {"none", "activity_cliff", "quality_erosion",
                    "disengagement_spiral", "weekend_overload", "pipeline_withdrawal"}
        assert {p.value for p in BurnoutPattern} == expected

    def test_burnout_severity_has_4_values(self):
        assert {s.value for s in BurnoutSeverity} == {"thriving", "stressed", "fatigued", "burned_out"}

    def test_burnout_action_has_9_values(self):
        assert len(BurnoutAction) == 9
        expected = {"no_action", "productivity_monitoring", "workload_review_conversation",
                    "territory_rebalancing", "coaching_cadence_increase", "quota_relief_assessment",
                    "manager_wellbeing_check_in", "immediate_support_intervention",
                    "retention_risk_escalation"}
        assert {a.value for a in BurnoutAction} == expected

    def test_enums_are_str_subclass(self):
        assert isinstance(BurnoutRisk.low, str) and isinstance(BurnoutPattern.activity_cliff, str)
        assert isinstance(BurnoutSeverity.burned_out, str) and isinstance(BurnoutAction.no_action, str)


# ---------------------------------------------------------------------------
# Activity sub-score
# ---------------------------------------------------------------------------

class TestActivityScore:
    @pytest.mark.parametrize("outbound,pipeline,prosp,expected", [
        (0.00, 0.00, 0.00, 0),    # all below thresholds
        (0.10, 0.10, 0.10, 0),    # still below all thresholds
        (0.15, 0.00, 0.00, 8),    # outbound low tier
        (0.30, 0.00, 0.00, 22),   # outbound mid tier
        (0.50, 0.00, 0.00, 40),   # outbound high tier
        (0.00, 0.25, 0.00, 18),   # pipeline mid tier
        (0.00, 0.45, 0.00, 35),   # pipeline high tier
        (0.00, 0.00, 0.30, 12),   # prospecting mid tier
        (0.00, 0.00, 0.50, 25),   # prospecting high tier
    ])
    def test_activity_score_tiers(self, engine, outbound, pipeline, prosp, expected):
        i = make_input(outbound_activity_decay_rate_pct=outbound,
                       pipeline_creation_decay_rate_pct=pipeline,
                       prospecting_avoidance_rate_pct=prosp)
        assert engine._activity_score(i) == expected

    def test_activity_score_capped_at_100(self, engine):
        i = make_input(outbound_activity_decay_rate_pct=0.55,
                       pipeline_creation_decay_rate_pct=0.50,
                       prospecting_avoidance_rate_pct=0.55)
        assert engine._activity_score(i) == 100


# ---------------------------------------------------------------------------
# Quality sub-score
# ---------------------------------------------------------------------------

class TestQualityScore:
    @pytest.mark.parametrize("error,followup,abandon,expected", [
        (0.00, 1.00, 0.00, 0),   # all below thresholds
        (0.07, 1.00, 0.00, 8),   # proposal low tier
        (0.15, 1.00, 0.00, 22),  # proposal mid tier
        (0.30, 1.00, 0.00, 40),  # proposal high tier
        (0.00, 0.55, 0.00, 18),  # follow-up mid tier
        (0.00, 0.30, 0.00, 35),  # follow-up high tier
        (0.00, 1.00, 0.12, 12),  # deal abandonment mid tier
        (0.00, 1.00, 0.25, 25),  # deal abandonment high tier
    ])
    def test_quality_score_tiers(self, engine, error, followup, abandon, expected):
        i = make_input(proposal_error_rate_pct=error,
                       follow_up_timeliness_score=followup,
                       deal_abandonment_rate_pct=abandon)
        assert engine._quality_score(i) == expected

    def test_quality_score_capped_at_100(self, engine):
        i = make_input(proposal_error_rate_pct=0.35,
                       follow_up_timeliness_score=0.10,
                       deal_abandonment_rate_pct=0.30)
        assert engine._quality_score(i) == 100


# ---------------------------------------------------------------------------
# Engagement sub-score
# ---------------------------------------------------------------------------

class TestEngagementScore:
    @pytest.mark.parametrize("mgr,enable,vacation,expected", [
        (1.00, 1.00, 1.00, 0),   # all fine
        (0.88, 1.00, 1.00, 10),  # manager low tier
        (0.75, 1.00, 1.00, 25),  # manager mid tier
        (0.55, 1.00, 1.00, 45),  # manager high tier
        (1.00, 0.60, 1.00, 15),  # enablement mid tier
        (1.00, 0.35, 1.00, 30),  # enablement high tier
        (1.00, 1.00, 0.45, 12),  # vacation mid tier
        (1.00, 1.00, 0.20, 25),  # vacation high tier
    ])
    def test_engagement_score_tiers(self, engine, mgr, enable, vacation, expected):
        i = make_input(manager_meeting_attendance_rate_pct=mgr,
                       enablement_session_attendance_rate_pct=enable,
                       vacation_utilization_pct=vacation)
        assert engine._engagement_score(i) == expected

    def test_engagement_score_capped_at_100(self, engine):
        i = make_input(manager_meeting_attendance_rate_pct=0.40,
                       enablement_session_attendance_rate_pct=0.20,
                       vacation_utilization_pct=0.10)
        assert engine._engagement_score(i) == 100


# ---------------------------------------------------------------------------
# Stress sub-score
# ---------------------------------------------------------------------------

class TestStressScore:
    @pytest.mark.parametrize("weekend,hours,overtime,expected", [
        (0.00, 7.0, 0.00, 0),   # all fine
        (0.20, 7.0, 0.00, 10),  # weekend low tier
        (0.35, 7.0, 0.00, 25),  # weekend mid tier
        (0.55, 7.0, 0.00, 45),  # weekend high tier
        (0.00, 10.0, 0.00, 15), # hours mid tier
        (0.00, 12.0, 0.00, 30), # hours high tier
        (0.00, 7.0, 0.30, 12),  # overtime mid tier
        (0.00, 7.0, 0.50, 25),  # overtime high tier
    ])
    def test_stress_score_tiers(self, engine, weekend, hours, overtime, expected):
        i = make_input(weekend_work_frequency_pct=weekend,
                       avg_daily_work_hours=hours,
                       voluntary_overtime_rate_pct=overtime)
        assert engine._stress_score(i) == expected

    def test_stress_score_capped_at_100(self, engine):
        i = make_input(weekend_work_frequency_pct=0.60, avg_daily_work_hours=13.0,
                       voluntary_overtime_rate_pct=0.60)
        assert engine._stress_score(i) == 100


# ---------------------------------------------------------------------------
# Composite, Risk, Severity
# ---------------------------------------------------------------------------

class TestCompositeRiskSeverity:
    def test_composite_formula_and_weighting(self, engine):
        assert engine._composite(100.0, 0.0, 0.0, 0.0) == 30.0
        assert engine._composite(0.0, 100.0, 0.0, 0.0) == 25.0
        assert engine._composite(0.0, 0.0, 100.0, 0.0) == 25.0
        assert engine._composite(0.0, 0.0, 0.0, 100.0) == 20.0

    def test_composite_capped_at_100(self, engine):
        assert engine._composite(100.0, 100.0, 100.0, 100.0) == 100.0

    def test_composite_zero(self, engine):
        assert engine._composite(0.0, 0.0, 0.0, 0.0) == 0.0

    @pytest.mark.parametrize("comp,risk", [
        (0.0, BurnoutRisk.low), (19.99, BurnoutRisk.low),
        (20.0, BurnoutRisk.moderate), (39.99, BurnoutRisk.moderate),
        (40.0, BurnoutRisk.high), (59.99, BurnoutRisk.high),
        (60.0, BurnoutRisk.critical), (100.0, BurnoutRisk.critical),
    ])
    def test_risk_thresholds(self, engine, comp, risk):
        assert engine._risk(comp) == risk

    @pytest.mark.parametrize("comp,sev", [
        (0.0, BurnoutSeverity.thriving), (19.99, BurnoutSeverity.thriving),
        (20.0, BurnoutSeverity.stressed), (39.99, BurnoutSeverity.stressed),
        (40.0, BurnoutSeverity.fatigued), (59.99, BurnoutSeverity.fatigued),
        (60.0, BurnoutSeverity.burned_out), (100.0, BurnoutSeverity.burned_out),
    ])
    def test_severity_thresholds(self, engine, comp, sev):
        assert engine._severity(comp) == sev


# ---------------------------------------------------------------------------
# Pattern detection
# ---------------------------------------------------------------------------

class TestPattern:
    def test_no_pattern_for_healthy_rep(self, engine):
        assert engine._pattern(make_input()) == BurnoutPattern.none

    def test_activity_cliff_exact_boundary(self, engine):
        i = make_input(outbound_activity_decay_rate_pct=0.45,
                       pipeline_creation_decay_rate_pct=0.40)
        assert engine._pattern(i) == BurnoutPattern.activity_cliff

    def test_quality_erosion(self, engine):
        i = make_input(proposal_error_rate_pct=0.25, follow_up_timeliness_score=0.40)
        assert engine._pattern(i) == BurnoutPattern.quality_erosion

    def test_weekend_overload(self, engine):
        i = make_input(weekend_work_frequency_pct=0.50, avg_daily_work_hours=11.0)
        assert engine._pattern(i) == BurnoutPattern.weekend_overload

    def test_disengagement_spiral(self, engine):
        i = make_input(manager_meeting_attendance_rate_pct=0.60,
                       enablement_session_attendance_rate_pct=0.40)
        assert engine._pattern(i) == BurnoutPattern.disengagement_spiral

    def test_pipeline_withdrawal(self, engine):
        i = make_input(deal_abandonment_rate_pct=0.22,
                       prospecting_avoidance_rate_pct=0.35)
        assert engine._pattern(i) == BurnoutPattern.pipeline_withdrawal

    def test_priority_activity_cliff_over_quality_erosion(self, engine):
        i = make_input(outbound_activity_decay_rate_pct=0.45,
                       pipeline_creation_decay_rate_pct=0.40,
                       proposal_error_rate_pct=0.25, follow_up_timeliness_score=0.35)
        assert engine._pattern(i) == BurnoutPattern.activity_cliff

    def test_priority_quality_erosion_over_weekend_overload(self, engine):
        i = make_input(proposal_error_rate_pct=0.25, follow_up_timeliness_score=0.35,
                       weekend_work_frequency_pct=0.50, avg_daily_work_hours=11.0)
        assert engine._pattern(i) == BurnoutPattern.quality_erosion

    def test_priority_weekend_overload_over_disengagement(self, engine):
        i = make_input(weekend_work_frequency_pct=0.50, avg_daily_work_hours=11.0,
                       manager_meeting_attendance_rate_pct=0.55,
                       enablement_session_attendance_rate_pct=0.35)
        assert engine._pattern(i) == BurnoutPattern.weekend_overload

    def test_priority_disengagement_over_pipeline_withdrawal(self, engine):
        i = make_input(manager_meeting_attendance_rate_pct=0.55,
                       enablement_session_attendance_rate_pct=0.35,
                       deal_abandonment_rate_pct=0.22,
                       prospecting_avoidance_rate_pct=0.35)
        assert engine._pattern(i) == BurnoutPattern.disengagement_spiral

    def test_activity_cliff_just_below_boundary(self, engine):
        i = make_input(outbound_activity_decay_rate_pct=0.44,
                       pipeline_creation_decay_rate_pct=0.40)
        assert engine._pattern(i) != BurnoutPattern.activity_cliff


# ---------------------------------------------------------------------------
# Action logic
# ---------------------------------------------------------------------------

class TestAction:
    def test_low_risk_no_action(self, engine):
        assert engine._action(BurnoutRisk.low, BurnoutPattern.none) == BurnoutAction.no_action

    def test_moderate_always_productivity_monitoring(self, engine):
        for pat in BurnoutPattern:
            assert engine._action(BurnoutRisk.moderate, pat) == BurnoutAction.productivity_monitoring

    @pytest.mark.parametrize("pat,expected", [
        (BurnoutPattern.activity_cliff,       BurnoutAction.quota_relief_assessment),
        (BurnoutPattern.quality_erosion,      BurnoutAction.coaching_cadence_increase),
        (BurnoutPattern.weekend_overload,     BurnoutAction.territory_rebalancing),
        (BurnoutPattern.disengagement_spiral, BurnoutAction.manager_wellbeing_check_in),
        (BurnoutPattern.pipeline_withdrawal,  BurnoutAction.workload_review_conversation),
        (BurnoutPattern.none,                 BurnoutAction.productivity_monitoring),
    ])
    def test_high_risk_actions(self, engine, pat, expected):
        assert engine._action(BurnoutRisk.high, pat) == expected

    def test_critical_activity_cliff_retention_escalation(self, engine):
        assert engine._action(BurnoutRisk.critical, BurnoutPattern.activity_cliff) == BurnoutAction.retention_risk_escalation

    def test_critical_pipeline_withdrawal_retention_escalation(self, engine):
        assert engine._action(BurnoutRisk.critical, BurnoutPattern.pipeline_withdrawal) == BurnoutAction.retention_risk_escalation

    @pytest.mark.parametrize("pat", [
        BurnoutPattern.quality_erosion, BurnoutPattern.weekend_overload,
        BurnoutPattern.disengagement_spiral, BurnoutPattern.none,
    ])
    def test_critical_other_patterns_immediate_support(self, engine, pat):
        assert engine._action(BurnoutRisk.critical, pat) == BurnoutAction.immediate_support_intervention


# ---------------------------------------------------------------------------
# Signal string
# ---------------------------------------------------------------------------

class TestSignal:
    def test_healthy_signal_below_20(self, engine):
        result = engine._signal(make_input(), BurnoutPattern.none, 10.0)
        assert "healthy" in result
        assert "benchmark targets" in result

    def test_healthy_signal_at_19(self, engine):
        assert "healthy" in engine._signal(make_input(), BurnoutPattern.none, 19.9)

    def test_not_healthy_at_exactly_20(self, engine):
        i = make_input(outbound_activity_decay_rate_pct=0.10,
                       weekend_work_frequency_pct=0.05, quota_attainment_trend=0.90)
        result = engine._signal(i, BurnoutPattern.none, 20.0)
        assert "healthy" not in result

    @pytest.mark.parametrize("pat,label", [
        (BurnoutPattern.activity_cliff,       "Activity cliff"),
        (BurnoutPattern.quality_erosion,      "Quality erosion"),
        (BurnoutPattern.disengagement_spiral, "Disengagement spiral"),
        (BurnoutPattern.weekend_overload,     "Weekend overload"),
        (BurnoutPattern.pipeline_withdrawal,  "Pipeline withdrawal"),
    ])
    def test_pattern_labels(self, engine, pat, label):
        i = make_input(outbound_activity_decay_rate_pct=0.40,
                       weekend_work_frequency_pct=0.10, quota_attainment_trend=0.80)
        result = engine._signal(i, pat, 50.0)
        assert result.startswith(label)

    def test_signal_contains_metrics(self, engine):
        i = make_input(outbound_activity_decay_rate_pct=0.40,
                       weekend_work_frequency_pct=0.10, quota_attainment_trend=0.80)
        result = engine._signal(i, BurnoutPattern.activity_cliff, 50.0)
        assert "40% activity decay" in result
        assert "10% weekend work" in result
        assert "80% quota trend" in result
        assert "composite 50" in result


# ---------------------------------------------------------------------------
# Flags and productivity loss
# ---------------------------------------------------------------------------

class TestFlagsAndLoss:
    def test_has_burnout_signal_via_composite(self, engine):
        assert engine._has_burnout_signal(make_input(), 40.0) is True

    def test_has_burnout_signal_via_outbound_decay(self, engine):
        i = make_input(outbound_activity_decay_rate_pct=0.30)
        assert engine._has_burnout_signal(i, 5.0) is True

    def test_has_burnout_signal_via_quota_trend(self, engine):
        i = make_input(quota_attainment_trend=0.70)
        assert engine._has_burnout_signal(i, 5.0) is True

    def test_no_burnout_signal_healthy(self, engine):
        i = make_input(outbound_activity_decay_rate_pct=0.10, quota_attainment_trend=0.90)
        assert engine._has_burnout_signal(i, 10.0) is False

    def test_requires_manager_via_composite(self, engine):
        assert engine._requires_manager_action(make_input(), 25.0) is True

    def test_requires_manager_via_attendance(self, engine):
        i = make_input(manager_meeting_attendance_rate_pct=0.75)
        assert engine._requires_manager_action(i, 5.0) is True

    def test_requires_manager_via_weekend_work(self, engine):
        i = make_input(weekend_work_frequency_pct=0.30)
        assert engine._requires_manager_action(i, 5.0) is True

    def test_no_manager_action_healthy(self, engine):
        i = make_input(manager_meeting_attendance_rate_pct=0.95, weekend_work_frequency_pct=0.05)
        assert engine._requires_manager_action(i, 10.0) is False

    def test_productivity_loss_formula(self, engine):
        i = make_input(total_active_deals=10, avg_deal_value_usd=1000.0,
                       quota_attainment_trend=0.80)
        expected = round(10 * 1000.0 * 0.20 * 0.50, 2)
        assert engine._productivity_loss(i, 50.0) == expected

    def test_productivity_loss_zero_composite(self, engine):
        i = make_input(total_active_deals=20, avg_deal_value_usd=5000.0,
                       quota_attainment_trend=0.50)
        assert engine._productivity_loss(i, 0.0) == 0.0

    def test_productivity_loss_perfect_quota(self, engine):
        i = make_input(total_active_deals=10, avg_deal_value_usd=1000.0,
                       quota_attainment_trend=1.0)
        assert engine._productivity_loss(i, 80.0) == 0.0

    def test_productivity_loss_rounded_to_2_decimals(self, engine):
        i = make_input(total_active_deals=3, avg_deal_value_usd=333.33,
                       quota_attainment_trend=0.50)
        result = engine._productivity_loss(i, 33.33)
        assert result == round(3 * 333.33 * 0.50 * (33.33 / 100), 2)


# ---------------------------------------------------------------------------
# assess() integration
# ---------------------------------------------------------------------------

class TestAssess:
    def test_assess_returns_burnout_result(self, engine):
        assert isinstance(engine.assess(make_input()), BurnoutResult)

    def test_assess_healthy_rep(self, engine):
        result = engine.assess(make_input())
        assert result.burnout_risk == "low"
        assert result.burnout_severity == "thriving"
        assert result.burnout_pattern == "none"
        assert result.recommended_action == "no_action"

    def test_assess_propagates_rep_id_and_region(self, engine):
        result = engine.assess(make_input(rep_id="REP-XYZ", region="APAC"))
        assert result.rep_id == "REP-XYZ"
        assert result.region == "APAC"

    def test_assess_critical_activity_cliff(self, engine):
        i = make_input(
            outbound_activity_decay_rate_pct=0.55, pipeline_creation_decay_rate_pct=0.50,
            prospecting_avoidance_rate_pct=0.55, proposal_error_rate_pct=0.35,
            follow_up_timeliness_score=0.20, deal_abandonment_rate_pct=0.30,
            manager_meeting_attendance_rate_pct=0.40,
            enablement_session_attendance_rate_pct=0.25, vacation_utilization_pct=0.10,
            weekend_work_frequency_pct=0.60, avg_daily_work_hours=13.0,
            voluntary_overtime_rate_pct=0.60, quota_attainment_trend=0.50,
        )
        result = engine.assess(i)
        assert result.burnout_risk == "critical"
        assert result.burnout_pattern == "activity_cliff"
        assert result.recommended_action == "retention_risk_escalation"
        assert result.burnout_composite >= 60.0

    def test_assess_high_quality_erosion(self, engine):
        # activity_score=0, quality_score=100, engagement_score=100, stress_score=0
        # composite = 0*0.30 + 100*0.25 + 100*0.25 + 0*0.20 = 50 → high
        i = make_input(
            proposal_error_rate_pct=0.30, follow_up_timeliness_score=0.30,
            deal_abandonment_rate_pct=0.25, manager_meeting_attendance_rate_pct=0.50,
            enablement_session_attendance_rate_pct=0.30, vacation_utilization_pct=0.15,
            outbound_activity_decay_rate_pct=0.10, pipeline_creation_decay_rate_pct=0.10,
            prospecting_avoidance_rate_pct=0.10,
        )
        result = engine.assess(i)
        assert result.burnout_pattern == "quality_erosion"
        assert result.burnout_risk == "high"
        assert result.recommended_action == "coaching_cadence_increase"

    def test_assess_scores_within_bounds(self, engine):
        i = make_input(
            outbound_activity_decay_rate_pct=1.0, pipeline_creation_decay_rate_pct=1.0,
            prospecting_avoidance_rate_pct=1.0, proposal_error_rate_pct=1.0,
            follow_up_timeliness_score=0.0, deal_abandonment_rate_pct=1.0,
            manager_meeting_attendance_rate_pct=0.0,
            enablement_session_attendance_rate_pct=0.0, vacation_utilization_pct=0.0,
            weekend_work_frequency_pct=1.0, avg_daily_work_hours=24.0,
            voluntary_overtime_rate_pct=1.0,
        )
        result = engine.assess(i)
        for score in (result.activity_score, result.quality_score,
                      result.engagement_score, result.stress_score):
            assert 0 <= score <= 100
        assert 0.0 <= result.burnout_composite <= 100.0

    def test_assess_appends_to_internal_results(self, engine):
        engine.assess(make_input(rep_id="A"))
        engine.assess(make_input(rep_id="B"))
        assert len(engine._results) == 2

    def test_assess_has_burnout_signal(self, engine):
        result = engine.assess(make_input(quota_attainment_trend=0.50,
                                          outbound_activity_decay_rate_pct=0.35))
        assert result.has_burnout_signal is True

    def test_assess_requires_manager_action(self, engine):
        result = engine.assess(make_input(weekend_work_frequency_pct=0.35))
        assert result.requires_manager_action is True


# ---------------------------------------------------------------------------
# to_dict() and BurnoutResult
# ---------------------------------------------------------------------------

class TestToDict:
    def test_to_dict_has_15_keys(self, engine):
        d = engine.assess(make_input()).to_dict()
        assert len(d) == 15

    def test_to_dict_key_names(self, engine):
        d = engine.assess(make_input()).to_dict()
        expected = {
            "rep_id", "region", "burnout_risk", "burnout_pattern", "burnout_severity",
            "recommended_action", "activity_score", "quality_score", "engagement_score",
            "stress_score", "burnout_composite", "has_burnout_signal",
            "requires_manager_action", "estimated_productivity_loss_usd", "burnout_signal",
        }
        assert set(d.keys()) == expected

    def test_to_dict_values_match_result(self, engine):
        result = engine.assess(make_input(rep_id="REP-TEST", region="NA"))
        d = result.to_dict()
        assert d["rep_id"] == result.rep_id
        assert d["region"] == result.region
        assert d["burnout_composite"] == result.burnout_composite
        assert d["has_burnout_signal"] == result.has_burnout_signal
        assert d["estimated_productivity_loss_usd"] == result.estimated_productivity_loss_usd


# ---------------------------------------------------------------------------
# assess_batch() and summary()
# ---------------------------------------------------------------------------

class TestBatchAndSummary:
    def test_assess_batch_empty(self, engine):
        assert engine.assess_batch([]) == []

    def test_assess_batch_returns_correct_count(self, engine):
        results = engine.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        assert len(results) == 5
        assert all(isinstance(r, BurnoutResult) for r in results)

    def test_assess_batch_rep_ids_preserved(self, engine):
        ids = ["REP-A", "REP-B", "REP-C"]
        results = engine.assess_batch([make_input(rep_id=rid) for rid in ids])
        assert [r.rep_id for r in results] == ids

    def test_summary_empty_engine_returns_zeroes(self, engine):
        s = engine.summary()
        assert s["total"] == 0
        assert s["avg_burnout_composite"] == 0.0
        assert s["burnout_signal_count"] == 0
        assert s["total_estimated_productivity_loss_usd"] == 0.0

    def test_summary_has_13_keys(self, engine):
        assert len(engine.summary()) == 13

    def test_summary_key_names(self, engine):
        s = engine.summary()
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts", "action_counts",
            "avg_burnout_composite", "burnout_signal_count", "manager_action_count",
            "avg_activity_score", "avg_quality_score", "avg_engagement_score",
            "avg_stress_score", "total_estimated_productivity_loss_usd",
        }
        assert set(s.keys()) == expected

    def test_summary_total_count(self, engine):
        engine.assess_batch([make_input(rep_id=f"R{i}") for i in range(4)])
        assert engine.summary()["total"] == 4

    def test_summary_risk_counts(self, engine):
        engine.assess(make_input())
        s = engine.summary()
        assert s["risk_counts"].get("low", 0) == 1

    def test_summary_avg_composite_rounded_to_1_decimal(self, engine):
        engine.assess(make_input())
        avg = engine.summary()["avg_burnout_composite"]
        assert avg == round(avg, 1)

    def test_summary_burnout_signal_count(self, engine):
        engine.assess(make_input(quota_attainment_trend=0.50))
        assert engine.summary()["burnout_signal_count"] >= 1

    def test_summary_total_productivity_loss_is_sum(self, engine):
        i1 = make_input(total_active_deals=5, avg_deal_value_usd=1000.0,
                        quota_attainment_trend=0.80)
        i2 = make_input(total_active_deals=10, avg_deal_value_usd=2000.0,
                        quota_attainment_trend=0.90)
        r1 = engine.assess(i1)
        r2 = engine.assess(i2)
        s = engine.summary()
        expected = round(r1.estimated_productivity_loss_usd + r2.estimated_productivity_loss_usd, 2)
        assert s["total_estimated_productivity_loss_usd"] == expected

    def test_summary_pattern_counts_tracked(self, engine):
        engine.assess(make_input(outbound_activity_decay_rate_pct=0.50,
                                 pipeline_creation_decay_rate_pct=0.45))
        assert "activity_cliff" in engine.summary()["pattern_counts"]

    def test_independent_engines_do_not_share_state(self):
        e1 = SalesRepBurnoutProductivityDecayEngine()
        e2 = SalesRepBurnoutProductivityDecayEngine()
        e1.assess(make_input(rep_id="E1"))
        assert e2.summary()["total"] == 0
        assert e1.summary()["total"] == 1
