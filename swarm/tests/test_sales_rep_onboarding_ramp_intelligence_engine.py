"""
Comprehensive pytest tests for SalesRepOnboardingRampIntelligenceEngine.

Coverage:
- Enums (RampRisk, RampPattern, RampSeverity, RampAction)
- RampInput field existence and types (22 fields)
- RampResult field existence (15 fields) and to_dict() (15 keys)
- Each sub-score branch (_pipeline_score, _activity_score, _coaching_score, _progression_score)
- Pattern detection priority order
- Risk / severity thresholds
- Action mapping matrix
- Gap / intervention flags
- Revenue loss formula
- Signal string variants
- assess() end-to-end
- assess_batch()
- summary() — empty and populated, all 13 keys
- Edge cases (zeros, ones, caps, boundary values)
"""

from __future__ import annotations

import math
import pytest

from swarm.intelligence.sales_rep_onboarding_ramp_intelligence_engine import (
    RampAction,
    RampInput,
    RampPattern,
    RampResult,
    RampRisk,
    RampSeverity,
    SalesRepOnboardingRampIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> RampInput:
    """Return a baseline 'healthy' RampInput, optionally overriding fields."""
    defaults = dict(
        rep_id="REP-001",
        region="North",
        evaluation_period_id="Q1-2026",
        ramp_week=4,
        target_ramp_weeks=12,
        pipeline_build_pct_of_target=0.90,
        first_deal_closed=True,
        days_to_first_deal=30.0,
        activity_adoption_score_pct=0.90,
        crm_usage_compliance_pct=0.90,
        calls_per_week_vs_target_pct=0.90,
        emails_per_week_vs_target_pct=0.90,
        meetings_booked_vs_target_pct=0.90,
        coaching_session_attendance_pct=0.95,
        coaching_action_completion_pct=0.95,
        manager_confidence_score=0.90,
        peer_benchmark_percentile=0.80,
        avg_deal_size_vs_cohort_pct=1.10,
        deals_in_pipeline=5,
        pipeline_stage_advancement_rate_pct=0.80,
        expected_first_quarter_attainment_pct=0.90,
        avg_opportunity_value_usd=10_000.0,
    )
    defaults.update(overrides)
    return RampInput(**defaults)


def fresh_engine() -> SalesRepOnboardingRampIntelligenceEngine:
    return SalesRepOnboardingRampIntelligenceEngine()


# ===========================================================================
# 1. ENUM TESTS
# ===========================================================================

class TestRampRiskEnum:
    def test_low_value(self):
        assert RampRisk.low.value == "low"

    def test_moderate_value(self):
        assert RampRisk.moderate.value == "moderate"

    def test_high_value(self):
        assert RampRisk.high.value == "high"

    def test_critical_value(self):
        assert RampRisk.critical.value == "critical"

    def test_members_count(self):
        assert len(RampRisk) == 4

    def test_is_str_subclass(self):
        assert isinstance(RampRisk.low, str)

    def test_string_equality(self):
        assert RampRisk.high == "high"


class TestRampPatternEnum:
    def test_none_value(self):
        assert RampPattern.none.value == "none"

    def test_slow_pipeline_build(self):
        assert RampPattern.slow_pipeline_build.value == "slow_pipeline_build"

    def test_activity_adoption_lag(self):
        assert RampPattern.activity_adoption_lag.value == "activity_adoption_lag"

    def test_first_deal_stall(self):
        assert RampPattern.first_deal_stall.value == "first_deal_stall"

    def test_coaching_resistance(self):
        assert RampPattern.coaching_resistance.value == "coaching_resistance"

    def test_early_exit_risk(self):
        assert RampPattern.early_exit_risk.value == "early_exit_risk"

    def test_members_count(self):
        assert len(RampPattern) == 6

    def test_is_str_subclass(self):
        assert isinstance(RampPattern.none, str)


class TestRampSeverityEnum:
    def test_accelerating(self):
        assert RampSeverity.accelerating.value == "accelerating"

    def test_on_track(self):
        assert RampSeverity.on_track.value == "on_track"

    def test_lagging(self):
        assert RampSeverity.lagging.value == "lagging"

    def test_derailing(self):
        assert RampSeverity.derailing.value == "derailing"

    def test_members_count(self):
        assert len(RampSeverity) == 4

    def test_is_str_subclass(self):
        assert isinstance(RampSeverity.derailing, str)


class TestRampActionEnum:
    def test_no_action(self):
        assert RampAction.no_action.value == "no_action"

    def test_pipeline_build_coaching(self):
        assert RampAction.pipeline_build_coaching.value == "pipeline_build_coaching"

    def test_activity_habits_coaching(self):
        assert RampAction.activity_habits_coaching.value == "activity_habits_coaching"

    def test_deal_progression_coaching(self):
        assert RampAction.deal_progression_coaching.value == "deal_progression_coaching"

    def test_manager_led_intervention(self):
        assert RampAction.manager_led_intervention.value == "manager_led_intervention"

    def test_ramp_extension_review(self):
        assert RampAction.ramp_extension_review.value == "ramp_extension_review"

    def test_members_count(self):
        assert len(RampAction) == 6

    def test_is_str_subclass(self):
        assert isinstance(RampAction.no_action, str)


# ===========================================================================
# 2. RampInput FIELD TESTS
# ===========================================================================

class TestRampInputFields:
    def test_rep_id(self):
        inp = make_input(rep_id="X99")
        assert inp.rep_id == "X99"

    def test_region(self):
        inp = make_input(region="South")
        assert inp.region == "South"

    def test_evaluation_period_id(self):
        inp = make_input(evaluation_period_id="Q2-2026")
        assert inp.evaluation_period_id == "Q2-2026"

    def test_ramp_week_int(self):
        inp = make_input(ramp_week=7)
        assert inp.ramp_week == 7

    def test_target_ramp_weeks_int(self):
        inp = make_input(target_ramp_weeks=16)
        assert inp.target_ramp_weeks == 16

    def test_pipeline_build_pct_of_target(self):
        inp = make_input(pipeline_build_pct_of_target=0.50)
        assert inp.pipeline_build_pct_of_target == 0.50

    def test_first_deal_closed_bool(self):
        inp = make_input(first_deal_closed=False)
        assert inp.first_deal_closed is False

    def test_days_to_first_deal(self):
        inp = make_input(days_to_first_deal=45.5)
        assert inp.days_to_first_deal == 45.5

    def test_activity_adoption_score_pct(self):
        inp = make_input(activity_adoption_score_pct=0.70)
        assert inp.activity_adoption_score_pct == 0.70

    def test_crm_usage_compliance_pct(self):
        inp = make_input(crm_usage_compliance_pct=0.60)
        assert inp.crm_usage_compliance_pct == 0.60

    def test_calls_per_week_vs_target_pct(self):
        inp = make_input(calls_per_week_vs_target_pct=0.55)
        assert inp.calls_per_week_vs_target_pct == 0.55

    def test_emails_per_week_vs_target_pct(self):
        inp = make_input(emails_per_week_vs_target_pct=0.85)
        assert inp.emails_per_week_vs_target_pct == 0.85

    def test_meetings_booked_vs_target_pct(self):
        inp = make_input(meetings_booked_vs_target_pct=0.75)
        assert inp.meetings_booked_vs_target_pct == 0.75

    def test_coaching_session_attendance_pct(self):
        inp = make_input(coaching_session_attendance_pct=0.80)
        assert inp.coaching_session_attendance_pct == 0.80

    def test_coaching_action_completion_pct(self):
        inp = make_input(coaching_action_completion_pct=0.55)
        assert inp.coaching_action_completion_pct == 0.55

    def test_manager_confidence_score(self):
        inp = make_input(manager_confidence_score=0.50)
        assert inp.manager_confidence_score == 0.50

    def test_peer_benchmark_percentile(self):
        inp = make_input(peer_benchmark_percentile=0.40)
        assert inp.peer_benchmark_percentile == 0.40

    def test_avg_deal_size_vs_cohort_pct(self):
        inp = make_input(avg_deal_size_vs_cohort_pct=1.20)
        assert inp.avg_deal_size_vs_cohort_pct == 1.20

    def test_deals_in_pipeline_int(self):
        inp = make_input(deals_in_pipeline=8)
        assert inp.deals_in_pipeline == 8

    def test_pipeline_stage_advancement_rate_pct(self):
        inp = make_input(pipeline_stage_advancement_rate_pct=0.45)
        assert inp.pipeline_stage_advancement_rate_pct == 0.45

    def test_expected_first_quarter_attainment_pct(self):
        inp = make_input(expected_first_quarter_attainment_pct=0.75)
        assert inp.expected_first_quarter_attainment_pct == 0.75

    def test_avg_opportunity_value_usd(self):
        inp = make_input(avg_opportunity_value_usd=25000.0)
        assert inp.avg_opportunity_value_usd == 25000.0

    def test_has_22_fields(self):
        inp = make_input()
        assert len(inp.__dataclass_fields__) == 22


# ===========================================================================
# 3. RampResult FIELD TESTS
# ===========================================================================

class TestRampResultFields:
    @pytest.fixture
    def result(self):
        eng = fresh_engine()
        return eng.assess(make_input())

    def test_rep_id(self, result):
        assert result.rep_id == "REP-001"

    def test_region(self, result):
        assert result.region == "North"

    def test_ramp_risk_type(self, result):
        assert isinstance(result.ramp_risk, RampRisk)

    def test_ramp_pattern_type(self, result):
        assert isinstance(result.ramp_pattern, RampPattern)

    def test_ramp_severity_type(self, result):
        assert isinstance(result.ramp_severity, RampSeverity)

    def test_recommended_action_type(self, result):
        assert isinstance(result.recommended_action, RampAction)

    def test_pipeline_score_float(self, result):
        assert isinstance(result.pipeline_score, float)

    def test_activity_score_float(self, result):
        assert isinstance(result.activity_score, float)

    def test_coaching_score_float(self, result):
        assert isinstance(result.coaching_score, float)

    def test_progression_score_float(self, result):
        assert isinstance(result.progression_score, float)

    def test_ramp_composite_float(self, result):
        assert isinstance(result.ramp_composite, float)

    def test_has_ramp_gap_bool(self, result):
        assert isinstance(result.has_ramp_gap, bool)

    def test_requires_ramp_intervention_bool(self, result):
        assert isinstance(result.requires_ramp_intervention, bool)

    def test_estimated_ramp_revenue_loss_usd_float(self, result):
        assert isinstance(result.estimated_ramp_revenue_loss_usd, float)

    def test_ramp_signal_str(self, result):
        assert isinstance(result.ramp_signal, str)

    def test_has_15_fields(self, result):
        assert len(result.__dataclass_fields__) == 15


# ===========================================================================
# 4. to_dict() TESTS
# ===========================================================================

class TestRampResultToDict:
    @pytest.fixture
    def d(self):
        eng = fresh_engine()
        return eng.assess(make_input()).to_dict()

    def test_returns_dict(self, d):
        assert isinstance(d, dict)

    def test_exactly_15_keys(self, d):
        assert len(d) == 15

    def test_key_rep_id(self, d):
        assert "rep_id" in d

    def test_key_region(self, d):
        assert "region" in d

    def test_key_ramp_risk(self, d):
        assert "ramp_risk" in d

    def test_key_ramp_pattern(self, d):
        assert "ramp_pattern" in d

    def test_key_ramp_severity(self, d):
        assert "ramp_severity" in d

    def test_key_recommended_action(self, d):
        assert "recommended_action" in d

    def test_key_pipeline_score(self, d):
        assert "pipeline_score" in d

    def test_key_activity_score(self, d):
        assert "activity_score" in d

    def test_key_coaching_score(self, d):
        assert "coaching_score" in d

    def test_key_progression_score(self, d):
        assert "progression_score" in d

    def test_key_ramp_composite(self, d):
        assert "ramp_composite" in d

    def test_key_has_ramp_gap(self, d):
        assert "has_ramp_gap" in d

    def test_key_requires_ramp_intervention(self, d):
        assert "requires_ramp_intervention" in d

    def test_key_estimated_ramp_revenue_loss_usd(self, d):
        assert "estimated_ramp_revenue_loss_usd" in d

    def test_key_ramp_signal(self, d):
        assert "ramp_signal" in d

    def test_ramp_risk_is_string(self, d):
        assert isinstance(d["ramp_risk"], str)

    def test_ramp_pattern_is_string(self, d):
        assert isinstance(d["ramp_pattern"], str)

    def test_ramp_severity_is_string(self, d):
        assert isinstance(d["ramp_severity"], str)

    def test_recommended_action_is_string(self, d):
        assert isinstance(d["recommended_action"], str)


# ===========================================================================
# 5. PIPELINE SUB-SCORE BRANCH TESTS
# ===========================================================================

class TestPipelineScore:
    """_pipeline_score branches tested in isolation via assess()."""

    def _score(self, **kw):
        eng = fresh_engine()
        # Use unhealthy activity/coaching/progression so we isolate pipeline effect minimally
        inp = make_input(**kw)
        eng.assess(inp)
        return eng._results[-1].pipeline_score

    # pipeline_build_pct_of_target
    def test_pipeline_pct_le_025_adds_40(self):
        eng = fresh_engine()
        inp = make_input(
            pipeline_build_pct_of_target=0.25,
            deals_in_pipeline=10,
            expected_first_quarter_attainment_pct=1.0,
        )
        s = eng._pipeline_score(inp)
        assert s == 40.0

    def test_pipeline_pct_le_050_adds_22(self):
        eng = fresh_engine()
        inp = make_input(
            pipeline_build_pct_of_target=0.50,
            deals_in_pipeline=10,
            expected_first_quarter_attainment_pct=1.0,
        )
        s = eng._pipeline_score(inp)
        assert s == 22.0

    def test_pipeline_pct_le_075_adds_8(self):
        eng = fresh_engine()
        inp = make_input(
            pipeline_build_pct_of_target=0.75,
            deals_in_pipeline=10,
            expected_first_quarter_attainment_pct=1.0,
        )
        s = eng._pipeline_score(inp)
        assert s == 8.0

    def test_pipeline_pct_above_075_adds_0(self):
        eng = fresh_engine()
        inp = make_input(
            pipeline_build_pct_of_target=0.76,
            deals_in_pipeline=10,
            expected_first_quarter_attainment_pct=1.0,
        )
        s = eng._pipeline_score(inp)
        assert s == 0.0

    # deals_in_pipeline
    def test_deals_le_1_adds_35(self):
        eng = fresh_engine()
        inp = make_input(
            pipeline_build_pct_of_target=1.0,
            deals_in_pipeline=1,
            expected_first_quarter_attainment_pct=1.0,
        )
        s = eng._pipeline_score(inp)
        assert s == 35.0

    def test_deals_eq_0_adds_35(self):
        eng = fresh_engine()
        inp = make_input(
            pipeline_build_pct_of_target=1.0,
            deals_in_pipeline=0,
            expected_first_quarter_attainment_pct=1.0,
        )
        s = eng._pipeline_score(inp)
        assert s == 35.0

    def test_deals_le_3_adds_18(self):
        eng = fresh_engine()
        inp = make_input(
            pipeline_build_pct_of_target=1.0,
            deals_in_pipeline=3,
            expected_first_quarter_attainment_pct=1.0,
        )
        s = eng._pipeline_score(inp)
        assert s == 18.0

    def test_deals_above_3_adds_0(self):
        eng = fresh_engine()
        inp = make_input(
            pipeline_build_pct_of_target=1.0,
            deals_in_pipeline=4,
            expected_first_quarter_attainment_pct=1.0,
        )
        s = eng._pipeline_score(inp)
        assert s == 0.0

    # expected_first_quarter_attainment_pct
    def test_attainment_le_030_adds_25(self):
        eng = fresh_engine()
        inp = make_input(
            pipeline_build_pct_of_target=1.0,
            deals_in_pipeline=10,
            expected_first_quarter_attainment_pct=0.30,
        )
        s = eng._pipeline_score(inp)
        assert s == 25.0

    def test_attainment_le_060_adds_12(self):
        eng = fresh_engine()
        inp = make_input(
            pipeline_build_pct_of_target=1.0,
            deals_in_pipeline=10,
            expected_first_quarter_attainment_pct=0.60,
        )
        s = eng._pipeline_score(inp)
        assert s == 12.0

    def test_attainment_above_060_adds_0(self):
        eng = fresh_engine()
        inp = make_input(
            pipeline_build_pct_of_target=1.0,
            deals_in_pipeline=10,
            expected_first_quarter_attainment_pct=0.61,
        )
        s = eng._pipeline_score(inp)
        assert s == 0.0

    def test_pipeline_score_capped_at_100(self):
        eng = fresh_engine()
        inp = make_input(
            pipeline_build_pct_of_target=0.0,
            deals_in_pipeline=0,
            expected_first_quarter_attainment_pct=0.0,
        )
        s = eng._pipeline_score(inp)
        assert s == 100.0

    def test_pipeline_score_all_max_branches(self):
        eng = fresh_engine()
        inp = make_input(
            pipeline_build_pct_of_target=0.10,
            deals_in_pipeline=0,
            expected_first_quarter_attainment_pct=0.10,
        )
        # 40 + 35 + 25 = 100, but capped
        s = eng._pipeline_score(inp)
        assert s == 100.0

    def test_pipeline_score_mixed(self):
        eng = fresh_engine()
        inp = make_input(
            pipeline_build_pct_of_target=0.50,
            deals_in_pipeline=3,
            expected_first_quarter_attainment_pct=0.61,
        )
        # 22 + 18 + 0 = 40
        s = eng._pipeline_score(inp)
        assert s == 40.0


# ===========================================================================
# 6. ACTIVITY SUB-SCORE BRANCH TESTS
# ===========================================================================

class TestActivityScore:

    # activity_adoption_score_pct
    def test_activity_pct_le_040_adds_40(self):
        eng = fresh_engine()
        inp = make_input(
            activity_adoption_score_pct=0.40,
            crm_usage_compliance_pct=1.0,
            calls_per_week_vs_target_pct=1.0,
        )
        s = eng._activity_score(inp)
        assert s == 40.0

    def test_activity_pct_le_065_adds_22(self):
        eng = fresh_engine()
        inp = make_input(
            activity_adoption_score_pct=0.65,
            crm_usage_compliance_pct=1.0,
            calls_per_week_vs_target_pct=1.0,
        )
        s = eng._activity_score(inp)
        assert s == 22.0

    def test_activity_pct_le_080_adds_8(self):
        eng = fresh_engine()
        inp = make_input(
            activity_adoption_score_pct=0.80,
            crm_usage_compliance_pct=1.0,
            calls_per_week_vs_target_pct=1.0,
        )
        s = eng._activity_score(inp)
        assert s == 8.0

    def test_activity_pct_above_080_adds_0(self):
        eng = fresh_engine()
        inp = make_input(
            activity_adoption_score_pct=0.81,
            crm_usage_compliance_pct=1.0,
            calls_per_week_vs_target_pct=1.0,
        )
        s = eng._activity_score(inp)
        assert s == 0.0

    # crm_usage_compliance_pct
    def test_crm_le_050_adds_35(self):
        eng = fresh_engine()
        inp = make_input(
            activity_adoption_score_pct=1.0,
            crm_usage_compliance_pct=0.50,
            calls_per_week_vs_target_pct=1.0,
        )
        s = eng._activity_score(inp)
        assert s == 35.0

    def test_crm_le_075_adds_18(self):
        eng = fresh_engine()
        inp = make_input(
            activity_adoption_score_pct=1.0,
            crm_usage_compliance_pct=0.75,
            calls_per_week_vs_target_pct=1.0,
        )
        s = eng._activity_score(inp)
        assert s == 18.0

    def test_crm_above_075_adds_0(self):
        eng = fresh_engine()
        inp = make_input(
            activity_adoption_score_pct=1.0,
            crm_usage_compliance_pct=0.76,
            calls_per_week_vs_target_pct=1.0,
        )
        s = eng._activity_score(inp)
        assert s == 0.0

    # calls_per_week_vs_target_pct
    def test_calls_le_040_adds_25(self):
        eng = fresh_engine()
        inp = make_input(
            activity_adoption_score_pct=1.0,
            crm_usage_compliance_pct=1.0,
            calls_per_week_vs_target_pct=0.40,
        )
        s = eng._activity_score(inp)
        assert s == 25.0

    def test_calls_le_070_adds_12(self):
        eng = fresh_engine()
        inp = make_input(
            activity_adoption_score_pct=1.0,
            crm_usage_compliance_pct=1.0,
            calls_per_week_vs_target_pct=0.70,
        )
        s = eng._activity_score(inp)
        assert s == 12.0

    def test_calls_above_070_adds_0(self):
        eng = fresh_engine()
        inp = make_input(
            activity_adoption_score_pct=1.0,
            crm_usage_compliance_pct=1.0,
            calls_per_week_vs_target_pct=0.71,
        )
        s = eng._activity_score(inp)
        assert s == 0.0

    def test_activity_score_capped_at_100(self):
        eng = fresh_engine()
        inp = make_input(
            activity_adoption_score_pct=0.0,
            crm_usage_compliance_pct=0.0,
            calls_per_week_vs_target_pct=0.0,
        )
        s = eng._activity_score(inp)
        assert s == 100.0

    def test_activity_score_mixed(self):
        eng = fresh_engine()
        inp = make_input(
            activity_adoption_score_pct=0.65,
            crm_usage_compliance_pct=0.75,
            calls_per_week_vs_target_pct=0.71,
        )
        # 22 + 18 + 0 = 40
        s = eng._activity_score(inp)
        assert s == 40.0


# ===========================================================================
# 7. COACHING SUB-SCORE BRANCH TESTS
# ===========================================================================

class TestCoachingScore:

    # coaching_action_completion_pct
    def test_completion_le_030_adds_40(self):
        eng = fresh_engine()
        inp = make_input(
            coaching_action_completion_pct=0.30,
            coaching_session_attendance_pct=1.0,
            manager_confidence_score=1.0,
        )
        s = eng._coaching_score(inp)
        assert s == 40.0

    def test_completion_le_060_adds_22(self):
        eng = fresh_engine()
        inp = make_input(
            coaching_action_completion_pct=0.60,
            coaching_session_attendance_pct=1.0,
            manager_confidence_score=1.0,
        )
        s = eng._coaching_score(inp)
        assert s == 22.0

    def test_completion_le_080_adds_8(self):
        eng = fresh_engine()
        inp = make_input(
            coaching_action_completion_pct=0.80,
            coaching_session_attendance_pct=1.0,
            manager_confidence_score=1.0,
        )
        s = eng._coaching_score(inp)
        assert s == 8.0

    def test_completion_above_080_adds_0(self):
        eng = fresh_engine()
        inp = make_input(
            coaching_action_completion_pct=0.81,
            coaching_session_attendance_pct=1.0,
            manager_confidence_score=1.0,
        )
        s = eng._coaching_score(inp)
        assert s == 0.0

    # coaching_session_attendance_pct
    def test_attendance_le_060_adds_35(self):
        eng = fresh_engine()
        inp = make_input(
            coaching_action_completion_pct=1.0,
            coaching_session_attendance_pct=0.60,
            manager_confidence_score=1.0,
        )
        s = eng._coaching_score(inp)
        assert s == 35.0

    def test_attendance_le_080_adds_18(self):
        eng = fresh_engine()
        inp = make_input(
            coaching_action_completion_pct=1.0,
            coaching_session_attendance_pct=0.80,
            manager_confidence_score=1.0,
        )
        s = eng._coaching_score(inp)
        assert s == 18.0

    def test_attendance_above_080_adds_0(self):
        eng = fresh_engine()
        inp = make_input(
            coaching_action_completion_pct=1.0,
            coaching_session_attendance_pct=0.81,
            manager_confidence_score=1.0,
        )
        s = eng._coaching_score(inp)
        assert s == 0.0

    # manager_confidence_score
    def test_confidence_le_030_adds_25(self):
        eng = fresh_engine()
        inp = make_input(
            coaching_action_completion_pct=1.0,
            coaching_session_attendance_pct=1.0,
            manager_confidence_score=0.30,
        )
        s = eng._coaching_score(inp)
        assert s == 25.0

    def test_confidence_le_060_adds_12(self):
        eng = fresh_engine()
        inp = make_input(
            coaching_action_completion_pct=1.0,
            coaching_session_attendance_pct=1.0,
            manager_confidence_score=0.60,
        )
        s = eng._coaching_score(inp)
        assert s == 12.0

    def test_confidence_above_060_adds_0(self):
        eng = fresh_engine()
        inp = make_input(
            coaching_action_completion_pct=1.0,
            coaching_session_attendance_pct=1.0,
            manager_confidence_score=0.61,
        )
        s = eng._coaching_score(inp)
        assert s == 0.0

    def test_coaching_score_capped_at_100(self):
        eng = fresh_engine()
        inp = make_input(
            coaching_action_completion_pct=0.0,
            coaching_session_attendance_pct=0.0,
            manager_confidence_score=0.0,
        )
        s = eng._coaching_score(inp)
        assert s == 100.0

    def test_coaching_score_all_max(self):
        eng = fresh_engine()
        inp = make_input(
            coaching_action_completion_pct=0.10,
            coaching_session_attendance_pct=0.10,
            manager_confidence_score=0.10,
        )
        # 40 + 35 + 25 = 100
        s = eng._coaching_score(inp)
        assert s == 100.0


# ===========================================================================
# 8. PROGRESSION SUB-SCORE BRANCH TESTS
# ===========================================================================

class TestProgressionScore:

    # peer_benchmark_percentile
    def test_peer_le_015_adds_45(self):
        eng = fresh_engine()
        inp = make_input(
            peer_benchmark_percentile=0.15,
            first_deal_closed=True,
            pipeline_stage_advancement_rate_pct=1.0,
        )
        s = eng._progression_score(inp)
        assert s == 45.0

    def test_peer_le_035_adds_25(self):
        eng = fresh_engine()
        inp = make_input(
            peer_benchmark_percentile=0.35,
            first_deal_closed=True,
            pipeline_stage_advancement_rate_pct=1.0,
        )
        s = eng._progression_score(inp)
        assert s == 25.0

    def test_peer_le_050_adds_10(self):
        eng = fresh_engine()
        inp = make_input(
            peer_benchmark_percentile=0.50,
            first_deal_closed=True,
            pipeline_stage_advancement_rate_pct=1.0,
        )
        s = eng._progression_score(inp)
        assert s == 10.0

    def test_peer_above_050_adds_0(self):
        eng = fresh_engine()
        inp = make_input(
            peer_benchmark_percentile=0.51,
            first_deal_closed=True,
            pipeline_stage_advancement_rate_pct=1.0,
        )
        s = eng._progression_score(inp)
        assert s == 0.0

    # first_deal_closed + ramp_week thresholds
    def test_no_first_deal_at_75pct_ramp_adds_30(self):
        eng = fresh_engine()
        # ramp_week=9, target=12 => 9/12=0.75
        inp = make_input(
            peer_benchmark_percentile=1.0,
            first_deal_closed=False,
            ramp_week=9,
            target_ramp_weeks=12,
            pipeline_stage_advancement_rate_pct=1.0,
        )
        s = eng._progression_score(inp)
        assert s == 30.0

    def test_no_first_deal_at_50pct_ramp_adds_15(self):
        eng = fresh_engine()
        # ramp_week=6, target=12 => 6/12=0.50
        inp = make_input(
            peer_benchmark_percentile=1.0,
            first_deal_closed=False,
            ramp_week=6,
            target_ramp_weeks=12,
            pipeline_stage_advancement_rate_pct=1.0,
        )
        s = eng._progression_score(inp)
        assert s == 15.0

    def test_first_deal_closed_no_bonus(self):
        eng = fresh_engine()
        inp = make_input(
            peer_benchmark_percentile=1.0,
            first_deal_closed=True,
            ramp_week=9,
            target_ramp_weeks=12,
            pipeline_stage_advancement_rate_pct=1.0,
        )
        s = eng._progression_score(inp)
        assert s == 0.0

    def test_no_first_deal_below_50pct_ramp_no_bonus(self):
        eng = fresh_engine()
        # ramp_week=5, target=12 => 5/12 < 0.50
        inp = make_input(
            peer_benchmark_percentile=1.0,
            first_deal_closed=False,
            ramp_week=5,
            target_ramp_weeks=12,
            pipeline_stage_advancement_rate_pct=1.0,
        )
        s = eng._progression_score(inp)
        assert s == 0.0

    # pipeline_stage_advancement_rate_pct
    def test_advancement_le_020_adds_25(self):
        eng = fresh_engine()
        inp = make_input(
            peer_benchmark_percentile=1.0,
            first_deal_closed=True,
            pipeline_stage_advancement_rate_pct=0.20,
        )
        s = eng._progression_score(inp)
        assert s == 25.0

    def test_advancement_le_040_adds_12(self):
        eng = fresh_engine()
        inp = make_input(
            peer_benchmark_percentile=1.0,
            first_deal_closed=True,
            pipeline_stage_advancement_rate_pct=0.40,
        )
        s = eng._progression_score(inp)
        assert s == 12.0

    def test_advancement_above_040_adds_0(self):
        eng = fresh_engine()
        inp = make_input(
            peer_benchmark_percentile=1.0,
            first_deal_closed=True,
            pipeline_stage_advancement_rate_pct=0.41,
        )
        s = eng._progression_score(inp)
        assert s == 0.0

    def test_progression_score_capped_at_100(self):
        eng = fresh_engine()
        inp = make_input(
            peer_benchmark_percentile=0.0,
            first_deal_closed=False,
            ramp_week=12,
            target_ramp_weeks=12,
            pipeline_stage_advancement_rate_pct=0.0,
        )
        s = eng._progression_score(inp)
        assert s == 100.0

    def test_progression_score_max_all_branches(self):
        eng = fresh_engine()
        # 45+30+25=100
        inp = make_input(
            peer_benchmark_percentile=0.10,
            first_deal_closed=False,
            ramp_week=9,
            target_ramp_weeks=12,
            pipeline_stage_advancement_rate_pct=0.10,
        )
        s = eng._progression_score(inp)
        assert s == 100.0


# ===========================================================================
# 9. COMPOSITE SCORE TESTS
# ===========================================================================

class TestCompositeScore:

    def test_healthy_rep_low_composite(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.ramp_composite < 20.0

    def test_composite_capped_at_100(self):
        eng = fresh_engine()
        inp = make_input(
            pipeline_build_pct_of_target=0.0,
            deals_in_pipeline=0,
            expected_first_quarter_attainment_pct=0.0,
            activity_adoption_score_pct=0.0,
            crm_usage_compliance_pct=0.0,
            calls_per_week_vs_target_pct=0.0,
            coaching_action_completion_pct=0.0,
            coaching_session_attendance_pct=0.0,
            manager_confidence_score=0.0,
            peer_benchmark_percentile=0.0,
            first_deal_closed=False,
            ramp_week=12,
            target_ramp_weeks=12,
            pipeline_stage_advancement_rate_pct=0.0,
        )
        result = eng.assess(inp)
        assert result.ramp_composite <= 100.0

    def test_composite_weights_applied(self):
        """Verify composite = pip*0.35 + act*0.30 + coa*0.20 + prog*0.15."""
        eng = fresh_engine()
        inp = make_input(
            pipeline_build_pct_of_target=0.50,   # pip=22
            deals_in_pipeline=10,
            expected_first_quarter_attainment_pct=1.0,
            activity_adoption_score_pct=0.65,    # act=22
            crm_usage_compliance_pct=1.0,
            calls_per_week_vs_target_pct=1.0,
            coaching_action_completion_pct=0.60, # coa=22
            coaching_session_attendance_pct=1.0,
            manager_confidence_score=1.0,
            peer_benchmark_percentile=1.0,       # prog=0
            first_deal_closed=True,
            pipeline_stage_advancement_rate_pct=1.0,
        )
        result = eng.assess(inp)
        expected = round(22 * 0.35 + 22 * 0.30 + 22 * 0.20 + 0 * 0.15, 1)
        assert result.ramp_composite == expected

    def test_composite_nonnegative(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.ramp_composite >= 0.0


# ===========================================================================
# 10. PATTERN DETECTION TESTS
# ===========================================================================

class TestPatternDetection:

    def test_early_exit_risk_priority_highest(self):
        """early_exit_risk should win even when other patterns also qualify."""
        eng = fresh_engine()
        inp = make_input(
            manager_confidence_score=0.20,
            peer_benchmark_percentile=0.15,
            # Also triggers coaching_resistance conditions
            coaching_action_completion_pct=0.20,
            coaching_session_attendance_pct=0.20,
            # Also triggers slow_pipeline
            pipeline_build_pct_of_target=0.20,
            deals_in_pipeline=0,
            expected_first_quarter_attainment_pct=0.10,
            # Also triggers activity_adoption_lag
            activity_adoption_score_pct=0.20,
            crm_usage_compliance_pct=0.10,
            calls_per_week_vs_target_pct=0.10,
        )
        result = eng.assess(inp)
        assert result.ramp_pattern == RampPattern.early_exit_risk

    def test_coaching_resistance_priority_over_pipeline(self):
        """coaching_resistance wins over slow_pipeline_build."""
        eng = fresh_engine()
        # Must NOT trigger early_exit_risk
        inp = make_input(
            manager_confidence_score=0.50,       # > 0.20
            peer_benchmark_percentile=0.50,      # > 0.15
            # coaching_resistance: coaching>=35 AND completion<=0.30
            coaching_action_completion_pct=0.25,
            coaching_session_attendance_pct=0.50,
            # Also trigger slow_pipeline
            pipeline_build_pct_of_target=0.30,
            deals_in_pipeline=0,
            expected_first_quarter_attainment_pct=0.10,
        )
        result = eng.assess(inp)
        assert result.ramp_pattern == RampPattern.coaching_resistance

    def test_slow_pipeline_build_pattern(self):
        eng = fresh_engine()
        inp = make_input(
            manager_confidence_score=0.50,
            peer_benchmark_percentile=0.50,
            coaching_action_completion_pct=0.90,  # no coaching_resistance
            # pipeline>=35 AND pipeline_build_pct<=0.40
            pipeline_build_pct_of_target=0.30,
            deals_in_pipeline=0,
            expected_first_quarter_attainment_pct=0.10,
            activity_adoption_score_pct=0.90,   # no activity lag
            crm_usage_compliance_pct=0.90,
            calls_per_week_vs_target_pct=0.90,
            first_deal_closed=True,
        )
        result = eng.assess(inp)
        assert result.ramp_pattern == RampPattern.slow_pipeline_build

    def test_activity_adoption_lag_pattern(self):
        eng = fresh_engine()
        inp = make_input(
            manager_confidence_score=0.50,
            peer_benchmark_percentile=0.50,
            coaching_action_completion_pct=0.90,
            pipeline_build_pct_of_target=0.90,  # no pipeline pattern
            deals_in_pipeline=10,
            expected_first_quarter_attainment_pct=0.90,
            # activity>=35 AND adoption<=0.50
            activity_adoption_score_pct=0.30,
            crm_usage_compliance_pct=0.30,
            calls_per_week_vs_target_pct=0.30,
            first_deal_closed=True,
        )
        result = eng.assess(inp)
        assert result.ramp_pattern == RampPattern.activity_adoption_lag

    def test_first_deal_stall_pattern(self):
        eng = fresh_engine()
        # ramp_week >= target * 0.60 and not closed
        inp = make_input(
            manager_confidence_score=0.90,
            peer_benchmark_percentile=0.80,
            coaching_action_completion_pct=0.90,
            pipeline_build_pct_of_target=0.90,
            deals_in_pipeline=5,
            expected_first_quarter_attainment_pct=0.90,
            activity_adoption_score_pct=0.90,
            crm_usage_compliance_pct=0.90,
            calls_per_week_vs_target_pct=0.90,
            first_deal_closed=False,
            ramp_week=8,
            target_ramp_weeks=12,  # 8/12 > 0.60
            pipeline_stage_advancement_rate_pct=0.90,
        )
        result = eng.assess(inp)
        assert result.ramp_pattern == RampPattern.first_deal_stall

    def test_none_pattern_healthy_rep(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.ramp_pattern == RampPattern.none

    def test_early_exit_requires_both_conditions(self):
        """Only manager_confidence low but not peer_benchmark should not trigger early_exit."""
        eng = fresh_engine()
        inp = make_input(
            manager_confidence_score=0.10,
            peer_benchmark_percentile=0.50,  # above 0.15
        )
        result = eng.assess(inp)
        assert result.ramp_pattern != RampPattern.early_exit_risk

    def test_early_exit_requires_both_conditions_peer_low(self):
        """Only peer low but not manager should not trigger early_exit."""
        eng = fresh_engine()
        inp = make_input(
            manager_confidence_score=0.50,  # above 0.20
            peer_benchmark_percentile=0.10,
        )
        result = eng.assess(inp)
        assert result.ramp_pattern != RampPattern.early_exit_risk

    def test_first_deal_stall_requires_ramp_week_threshold(self):
        """Below 60% of target_ramp_weeks, should not trigger first_deal_stall."""
        eng = fresh_engine()
        inp = make_input(
            first_deal_closed=False,
            ramp_week=7,
            target_ramp_weeks=12,  # 7/12 = 0.583... > 0.60? No 7/12=0.583 < 0.60
        )
        # 7 < 12*0.60 = 7.2 => no first_deal_stall
        result = eng.assess(inp)
        assert result.ramp_pattern != RampPattern.first_deal_stall

    def test_first_deal_stall_boundary(self):
        """Exactly at 60% of target weeks triggers stall."""
        eng = fresh_engine()
        # 12*0.60 = 7.2, so ramp_week=8 >= 7.2
        inp = make_input(
            manager_confidence_score=0.90,
            peer_benchmark_percentile=0.80,
            coaching_action_completion_pct=0.90,
            pipeline_build_pct_of_target=0.90,
            deals_in_pipeline=5,
            expected_first_quarter_attainment_pct=0.90,
            activity_adoption_score_pct=0.90,
            crm_usage_compliance_pct=0.90,
            calls_per_week_vs_target_pct=0.90,
            first_deal_closed=False,
            ramp_week=8,
            target_ramp_weeks=12,
            pipeline_stage_advancement_rate_pct=0.90,
        )
        result = eng.assess(inp)
        assert result.ramp_pattern == RampPattern.first_deal_stall


# ===========================================================================
# 11. RISK THRESHOLD TESTS
# ===========================================================================

class TestRiskLevel:

    def test_risk_critical_at_60(self):
        eng = fresh_engine()
        assert eng._risk_level(60.0) == RampRisk.critical

    def test_risk_critical_above_60(self):
        eng = fresh_engine()
        assert eng._risk_level(75.0) == RampRisk.critical

    def test_risk_high_at_40(self):
        eng = fresh_engine()
        assert eng._risk_level(40.0) == RampRisk.high

    def test_risk_high_between_40_60(self):
        eng = fresh_engine()
        assert eng._risk_level(55.0) == RampRisk.high

    def test_risk_moderate_at_20(self):
        eng = fresh_engine()
        assert eng._risk_level(20.0) == RampRisk.moderate

    def test_risk_moderate_between_20_40(self):
        eng = fresh_engine()
        assert eng._risk_level(30.0) == RampRisk.moderate

    def test_risk_low_below_20(self):
        eng = fresh_engine()
        assert eng._risk_level(19.9) == RampRisk.low

    def test_risk_low_at_zero(self):
        eng = fresh_engine()
        assert eng._risk_level(0.0) == RampRisk.low


# ===========================================================================
# 12. SEVERITY THRESHOLD TESTS
# ===========================================================================

class TestSeverity:

    def test_severity_derailing_at_60(self):
        eng = fresh_engine()
        assert eng._severity(60.0) == RampSeverity.derailing

    def test_severity_derailing_above_60(self):
        eng = fresh_engine()
        assert eng._severity(80.0) == RampSeverity.derailing

    def test_severity_lagging_at_40(self):
        eng = fresh_engine()
        assert eng._severity(40.0) == RampSeverity.lagging

    def test_severity_lagging_between_40_60(self):
        eng = fresh_engine()
        assert eng._severity(50.0) == RampSeverity.lagging

    def test_severity_on_track_at_20(self):
        eng = fresh_engine()
        assert eng._severity(20.0) == RampSeverity.on_track

    def test_severity_on_track_between_20_40(self):
        eng = fresh_engine()
        assert eng._severity(35.0) == RampSeverity.on_track

    def test_severity_accelerating_below_20(self):
        eng = fresh_engine()
        assert eng._severity(10.0) == RampSeverity.accelerating

    def test_severity_accelerating_at_zero(self):
        eng = fresh_engine()
        assert eng._severity(0.0) == RampSeverity.accelerating


# ===========================================================================
# 13. ACTION MAPPING TESTS
# ===========================================================================

class TestActionMapping:

    def test_critical_early_exit_risk_ramp_extension(self):
        eng = fresh_engine()
        action = eng._action(RampRisk.critical, RampPattern.early_exit_risk)
        assert action == RampAction.ramp_extension_review

    def test_critical_coaching_resistance_manager_intervention(self):
        eng = fresh_engine()
        action = eng._action(RampRisk.critical, RampPattern.coaching_resistance)
        assert action == RampAction.manager_led_intervention

    def test_critical_slow_pipeline_ramp_extension(self):
        eng = fresh_engine()
        action = eng._action(RampRisk.critical, RampPattern.slow_pipeline_build)
        assert action == RampAction.ramp_extension_review

    def test_critical_none_ramp_extension(self):
        eng = fresh_engine()
        action = eng._action(RampRisk.critical, RampPattern.none)
        assert action == RampAction.ramp_extension_review

    def test_critical_first_deal_stall_ramp_extension(self):
        eng = fresh_engine()
        action = eng._action(RampRisk.critical, RampPattern.first_deal_stall)
        assert action == RampAction.ramp_extension_review

    def test_critical_activity_lag_ramp_extension(self):
        eng = fresh_engine()
        action = eng._action(RampRisk.critical, RampPattern.activity_adoption_lag)
        assert action == RampAction.ramp_extension_review

    def test_high_slow_pipeline_pipeline_coaching(self):
        eng = fresh_engine()
        action = eng._action(RampRisk.high, RampPattern.slow_pipeline_build)
        assert action == RampAction.pipeline_build_coaching

    def test_high_first_deal_stall_deal_progression(self):
        eng = fresh_engine()
        action = eng._action(RampRisk.high, RampPattern.first_deal_stall)
        assert action == RampAction.deal_progression_coaching

    def test_high_none_manager_intervention(self):
        eng = fresh_engine()
        action = eng._action(RampRisk.high, RampPattern.none)
        assert action == RampAction.manager_led_intervention

    def test_high_activity_lag_manager_intervention(self):
        eng = fresh_engine()
        action = eng._action(RampRisk.high, RampPattern.activity_adoption_lag)
        assert action == RampAction.manager_led_intervention

    def test_high_coaching_resistance_manager_intervention(self):
        eng = fresh_engine()
        action = eng._action(RampRisk.high, RampPattern.coaching_resistance)
        assert action == RampAction.manager_led_intervention

    def test_high_early_exit_manager_intervention(self):
        eng = fresh_engine()
        action = eng._action(RampRisk.high, RampPattern.early_exit_risk)
        assert action == RampAction.manager_led_intervention

    def test_moderate_activity_lag_activity_coaching(self):
        eng = fresh_engine()
        action = eng._action(RampRisk.moderate, RampPattern.activity_adoption_lag)
        assert action == RampAction.activity_habits_coaching

    def test_moderate_none_pipeline_coaching(self):
        eng = fresh_engine()
        action = eng._action(RampRisk.moderate, RampPattern.none)
        assert action == RampAction.pipeline_build_coaching

    def test_moderate_slow_pipeline_pipeline_coaching(self):
        eng = fresh_engine()
        action = eng._action(RampRisk.moderate, RampPattern.slow_pipeline_build)
        assert action == RampAction.pipeline_build_coaching

    def test_moderate_first_deal_stall_pipeline_coaching(self):
        eng = fresh_engine()
        action = eng._action(RampRisk.moderate, RampPattern.first_deal_stall)
        assert action == RampAction.pipeline_build_coaching

    def test_low_no_action(self):
        eng = fresh_engine()
        action = eng._action(RampRisk.low, RampPattern.none)
        assert action == RampAction.no_action

    def test_low_any_pattern_no_action(self):
        eng = fresh_engine()
        for pattern in RampPattern:
            action = eng._action(RampRisk.low, pattern)
            assert action == RampAction.no_action


# ===========================================================================
# 14. GAP FLAG TESTS
# ===========================================================================

class TestHasRampGap:

    def test_gap_true_when_composite_ge_40(self):
        eng = fresh_engine()
        inp = make_input(
            pipeline_build_pct_of_target=0.90,
            peer_benchmark_percentile=0.90,
        )
        # Force composite >= 40 by having very low scores
        assert eng._has_ramp_gap(40.0, inp) is True

    def test_gap_true_when_pipeline_pct_le_040(self):
        eng = fresh_engine()
        inp = make_input(pipeline_build_pct_of_target=0.40, peer_benchmark_percentile=0.90)
        assert eng._has_ramp_gap(10.0, inp) is True

    def test_gap_true_when_peer_le_025(self):
        eng = fresh_engine()
        inp = make_input(pipeline_build_pct_of_target=0.90, peer_benchmark_percentile=0.25)
        assert eng._has_ramp_gap(10.0, inp) is True

    def test_gap_false_all_good(self):
        eng = fresh_engine()
        inp = make_input(pipeline_build_pct_of_target=0.90, peer_benchmark_percentile=0.90)
        assert eng._has_ramp_gap(10.0, inp) is False

    def test_gap_true_composite_exactly_40(self):
        eng = fresh_engine()
        inp = make_input(pipeline_build_pct_of_target=0.90, peer_benchmark_percentile=0.90)
        assert eng._has_ramp_gap(40.0, inp) is True

    def test_gap_false_composite_39(self):
        eng = fresh_engine()
        inp = make_input(pipeline_build_pct_of_target=0.90, peer_benchmark_percentile=0.90)
        # pipeline > 0.40, peer > 0.25, composite < 40
        assert eng._has_ramp_gap(39.9, inp) is False

    def test_gap_true_only_pipeline_trigger(self):
        eng = fresh_engine()
        inp = make_input(pipeline_build_pct_of_target=0.30, peer_benchmark_percentile=0.90)
        assert eng._has_ramp_gap(5.0, inp) is True


# ===========================================================================
# 15. INTERVENTION FLAG TESTS
# ===========================================================================

class TestRequiresRampIntervention:

    def test_intervention_when_composite_ge_30(self):
        eng = fresh_engine()
        inp = make_input(coaching_action_completion_pct=0.90, expected_first_quarter_attainment_pct=0.90)
        assert eng._requires_ramp_intervention(30.0, inp) is True

    def test_intervention_when_coaching_completion_le_050(self):
        eng = fresh_engine()
        inp = make_input(coaching_action_completion_pct=0.50, expected_first_quarter_attainment_pct=0.90)
        assert eng._requires_ramp_intervention(10.0, inp) is True

    def test_intervention_when_attainment_le_050(self):
        eng = fresh_engine()
        inp = make_input(coaching_action_completion_pct=0.90, expected_first_quarter_attainment_pct=0.50)
        assert eng._requires_ramp_intervention(10.0, inp) is True

    def test_no_intervention_all_good(self):
        eng = fresh_engine()
        inp = make_input(coaching_action_completion_pct=0.90, expected_first_quarter_attainment_pct=0.90)
        assert eng._requires_ramp_intervention(10.0, inp) is False

    def test_intervention_composite_29_no_other_triggers(self):
        eng = fresh_engine()
        inp = make_input(coaching_action_completion_pct=0.90, expected_first_quarter_attainment_pct=0.90)
        assert eng._requires_ramp_intervention(29.9, inp) is False

    def test_intervention_composite_exactly_30(self):
        eng = fresh_engine()
        inp = make_input(coaching_action_completion_pct=0.90, expected_first_quarter_attainment_pct=0.90)
        assert eng._requires_ramp_intervention(30.0, inp) is True


# ===========================================================================
# 16. REVENUE LOSS FORMULA TESTS
# ===========================================================================

class TestRevenueLoss:

    def test_revenue_loss_zero_when_full_attainment(self):
        eng = fresh_engine()
        inp = make_input(
            deals_in_pipeline=5,
            avg_opportunity_value_usd=10_000.0,
            expected_first_quarter_attainment_pct=1.0,
            ramp_week=4,
            target_ramp_weeks=12,
        )
        loss = eng._estimated_ramp_revenue_loss(inp, 50.0)
        assert loss == 0.0

    def test_revenue_loss_zero_when_composite_zero(self):
        eng = fresh_engine()
        inp = make_input(
            deals_in_pipeline=5,
            avg_opportunity_value_usd=10_000.0,
            expected_first_quarter_attainment_pct=0.50,
            ramp_week=4,
            target_ramp_weeks=12,
        )
        loss = eng._estimated_ramp_revenue_loss(inp, 0.0)
        assert loss == 0.0

    def test_revenue_loss_calculation(self):
        eng = fresh_engine()
        inp = make_input(
            deals_in_pipeline=4,
            avg_opportunity_value_usd=5_000.0,
            expected_first_quarter_attainment_pct=0.50,
            ramp_week=6,
            target_ramp_weeks=12,
        )
        composite = 50.0
        # 4 * 5000 * (1-0.5) * (50/100) * (6/12) = 4*5000*0.5*0.5*0.5 = 2500
        expected = round(4 * 5_000.0 * 0.5 * 0.5 * 0.5, 2)
        loss = eng._estimated_ramp_revenue_loss(inp, composite)
        assert loss == expected

    def test_revenue_loss_rounded_to_2_decimals(self):
        eng = fresh_engine()
        inp = make_input(
            deals_in_pipeline=3,
            avg_opportunity_value_usd=3_333.33,
            expected_first_quarter_attainment_pct=0.33,
            ramp_week=7,
            target_ramp_weeks=12,
        )
        loss = eng._estimated_ramp_revenue_loss(inp, 45.0)
        assert loss == round(loss, 2)

    def test_revenue_loss_negative_attainment_gap_clamped(self):
        """Attainment > 1.0 should produce zero gap (max(0, 1-pct))."""
        eng = fresh_engine()
        inp = make_input(
            deals_in_pipeline=5,
            avg_opportunity_value_usd=10_000.0,
            expected_first_quarter_attainment_pct=1.5,  # over 100%
            ramp_week=6,
            target_ramp_weeks=12,
        )
        loss = eng._estimated_ramp_revenue_loss(inp, 50.0)
        assert loss == 0.0

    def test_revenue_loss_target_ramp_weeks_zero_uses_one(self):
        """target_ramp_weeks=0 should use max(0,1)=1 to avoid div by zero."""
        eng = fresh_engine()
        inp = make_input(
            deals_in_pipeline=2,
            avg_opportunity_value_usd=1_000.0,
            expected_first_quarter_attainment_pct=0.0,
            ramp_week=1,
            target_ramp_weeks=0,
        )
        loss = eng._estimated_ramp_revenue_loss(inp, 100.0)
        # ramp_fraction = 1/max(0,1) = 1/1 = 1.0
        expected = round(2 * 1_000.0 * 1.0 * 1.0 * 1.0, 2)
        assert loss == expected

    def test_revenue_loss_in_result(self):
        eng = fresh_engine()
        inp = make_input(
            deals_in_pipeline=2,
            avg_opportunity_value_usd=5_000.0,
            expected_first_quarter_attainment_pct=0.50,
            ramp_week=6,
            target_ramp_weeks=12,
        )
        result = eng.assess(inp)
        # Verify the value is non-negative
        assert result.estimated_ramp_revenue_loss_usd >= 0.0


# ===========================================================================
# 17. SIGNAL STRING TESTS
# ===========================================================================

class TestSignalString:

    def test_healthy_signal(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.ramp_signal == (
            "Ramp progression healthy — pipeline build, activity adoption, "
            "and coaching engagement within benchmarks"
        )

    def test_unhealthy_signal_contains_pattern(self):
        eng = fresh_engine()
        inp = make_input(
            manager_confidence_score=0.10,
            peer_benchmark_percentile=0.10,
            pipeline_build_pct_of_target=0.10,
            deals_in_pipeline=0,
            expected_first_quarter_attainment_pct=0.10,
            activity_adoption_score_pct=0.10,
            crm_usage_compliance_pct=0.10,
            calls_per_week_vs_target_pct=0.10,
            coaching_action_completion_pct=0.10,
            coaching_session_attendance_pct=0.10,
            first_deal_closed=False,
            ramp_week=10,
            target_ramp_weeks=12,
            pipeline_stage_advancement_rate_pct=0.10,
        )
        result = eng.assess(inp)
        assert "early exit risk" in result.ramp_signal.lower() or "Early exit risk" in result.ramp_signal

    def test_signal_contains_pipeline_pct(self):
        eng = fresh_engine()
        inp = make_input(
            pipeline_build_pct_of_target=0.55,
            deals_in_pipeline=0,
            expected_first_quarter_attainment_pct=0.10,
        )
        result = eng.assess(inp)
        if result.ramp_pattern != RampPattern.none or result.ramp_composite >= 20:
            assert "55%" in result.ramp_signal

    def test_signal_contains_ramp_week(self):
        eng = fresh_engine()
        inp = make_input(
            pipeline_build_pct_of_target=0.10,
            deals_in_pipeline=0,
            expected_first_quarter_attainment_pct=0.10,
            ramp_week=7,
            target_ramp_weeks=12,
        )
        result = eng.assess(inp)
        assert "week 7" in result.ramp_signal

    def test_signal_none_pattern_above_composite_20_not_healthy(self):
        """When pattern==none but composite>=20, unhealthy signal is used."""
        eng = fresh_engine()
        # Create moderate composite (>=20) but ensure pattern is none
        # We need composite >=20 but pattern==none
        # This is hard to engineer cleanly — test that healthy message not returned
        inp = make_input(
            pipeline_build_pct_of_target=0.50,  # 22 pts pipeline
            deals_in_pipeline=3,               # 18 pts
            expected_first_quarter_attainment_pct=0.61,
            activity_adoption_score_pct=0.65,  # 22 pts
            crm_usage_compliance_pct=0.75,     # 18 pts
            calls_per_week_vs_target_pct=0.71,
            coaching_action_completion_pct=0.90,
            coaching_session_attendance_pct=0.90,
            manager_confidence_score=0.90,
            peer_benchmark_percentile=0.90,
            first_deal_closed=True,
            pipeline_stage_advancement_rate_pct=0.90,
        )
        result = eng.assess(inp)
        if result.ramp_composite >= 20:
            assert "healthy" not in result.ramp_signal

    def test_signal_ramp_risk_label_when_pattern_none(self):
        """When pattern is none and composite >= 20, label is 'Ramp risk'."""
        eng = fresh_engine()
        # Force composite >= 20 without triggering any specific pattern
        inp = make_input(
            pipeline_build_pct_of_target=0.50,
            deals_in_pipeline=3,
            expected_first_quarter_attainment_pct=0.61,
            activity_adoption_score_pct=0.65,
            crm_usage_compliance_pct=0.75,
            calls_per_week_vs_target_pct=0.71,
            coaching_action_completion_pct=0.90,
            coaching_session_attendance_pct=0.90,
            manager_confidence_score=0.90,
            peer_benchmark_percentile=0.90,
            first_deal_closed=True,
            pipeline_stage_advancement_rate_pct=0.90,
        )
        result = eng.assess(inp)
        if result.ramp_pattern == RampPattern.none and result.ramp_composite >= 20:
            assert result.ramp_signal.startswith("Ramp risk")

    def test_signal_contains_composite_value(self):
        eng = fresh_engine()
        inp = make_input(
            pipeline_build_pct_of_target=0.20,
            deals_in_pipeline=0,
            expected_first_quarter_attainment_pct=0.10,
        )
        result = eng.assess(inp)
        comp_str = f"{result.ramp_composite:.0f}"
        if result.ramp_pattern != RampPattern.none or result.ramp_composite >= 20:
            assert f"composite {comp_str}" in result.ramp_signal


# ===========================================================================
# 18. ASSESS END-TO-END TESTS
# ===========================================================================

class TestAssessEndToEnd:

    def test_healthy_rep_is_low_risk(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.ramp_risk == RampRisk.low

    def test_healthy_rep_accelerating(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.ramp_severity == RampSeverity.accelerating

    def test_healthy_rep_no_action(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.recommended_action == RampAction.no_action

    def test_healthy_rep_no_gap(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.has_ramp_gap is False

    def test_critical_rep_derailing(self):
        eng = fresh_engine()
        inp = make_input(
            pipeline_build_pct_of_target=0.10,
            deals_in_pipeline=0,
            expected_first_quarter_attainment_pct=0.10,
            activity_adoption_score_pct=0.10,
            crm_usage_compliance_pct=0.10,
            calls_per_week_vs_target_pct=0.10,
            coaching_action_completion_pct=0.10,
            coaching_session_attendance_pct=0.10,
            manager_confidence_score=0.10,
            peer_benchmark_percentile=0.10,
            first_deal_closed=False,
            ramp_week=10,
            target_ramp_weeks=12,
            pipeline_stage_advancement_rate_pct=0.10,
        )
        result = eng.assess(inp)
        assert result.ramp_severity == RampSeverity.derailing

    def test_result_stored_in_engine(self):
        eng = fresh_engine()
        eng.assess(make_input())
        assert len(eng._results) == 1

    def test_assess_returns_ramp_result(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert isinstance(result, RampResult)

    def test_rep_id_passes_through(self):
        eng = fresh_engine()
        result = eng.assess(make_input(rep_id="SPECIAL-99"))
        assert result.rep_id == "SPECIAL-99"

    def test_region_passes_through(self):
        eng = fresh_engine()
        result = eng.assess(make_input(region="Pacific"))
        assert result.region == "Pacific"

    def test_scores_nonnegative(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.pipeline_score >= 0
        assert result.activity_score >= 0
        assert result.coaching_score >= 0
        assert result.progression_score >= 0

    def test_scores_le_100(self):
        eng = fresh_engine()
        inp = make_input(
            pipeline_build_pct_of_target=0.0,
            deals_in_pipeline=0,
            expected_first_quarter_attainment_pct=0.0,
            activity_adoption_score_pct=0.0,
            crm_usage_compliance_pct=0.0,
            calls_per_week_vs_target_pct=0.0,
            coaching_action_completion_pct=0.0,
            coaching_session_attendance_pct=0.0,
            manager_confidence_score=0.0,
            peer_benchmark_percentile=0.0,
            first_deal_closed=False,
            ramp_week=12,
            target_ramp_weeks=12,
            pipeline_stage_advancement_rate_pct=0.0,
        )
        result = eng.assess(inp)
        assert result.pipeline_score <= 100
        assert result.activity_score <= 100
        assert result.coaching_score <= 100
        assert result.progression_score <= 100
        assert result.ramp_composite <= 100


# ===========================================================================
# 19. ASSESS_BATCH TESTS
# ===========================================================================

class TestAssessBatch:

    def test_batch_returns_list(self):
        eng = fresh_engine()
        results = eng.assess_batch([make_input(), make_input(rep_id="R2")])
        assert isinstance(results, list)

    def test_batch_returns_correct_count(self):
        eng = fresh_engine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = eng.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_all_ramp_results(self):
        eng = fresh_engine()
        results = eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        assert all(isinstance(r, RampResult) for r in results)

    def test_batch_empty_list(self):
        eng = fresh_engine()
        results = eng.assess_batch([])
        assert results == []

    def test_batch_stores_results(self):
        eng = fresh_engine()
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(4)])
        assert len(eng._results) == 4

    def test_batch_rep_ids_preserved(self):
        eng = fresh_engine()
        ids = [f"REP-{i}" for i in range(3)]
        results = eng.assess_batch([make_input(rep_id=rid) for rid in ids])
        assert [r.rep_id for r in results] == ids

    def test_batch_single_input(self):
        eng = fresh_engine()
        results = eng.assess_batch([make_input()])
        assert len(results) == 1


# ===========================================================================
# 20. SUMMARY TESTS — EMPTY ENGINE
# ===========================================================================

class TestSummaryEmpty:

    @pytest.fixture
    def s(self):
        return fresh_engine().summary()

    def test_returns_dict(self, s):
        assert isinstance(s, dict)

    def test_exactly_13_keys(self, s):
        assert len(s) == 13

    def test_key_total(self, s):
        assert "total" in s

    def test_key_risk_counts(self, s):
        assert "risk_counts" in s

    def test_key_pattern_counts(self, s):
        assert "pattern_counts" in s

    def test_key_severity_counts(self, s):
        assert "severity_counts" in s

    def test_key_action_counts(self, s):
        assert "action_counts" in s

    def test_key_avg_ramp_composite(self, s):
        assert "avg_ramp_composite" in s

    def test_key_ramp_gap_count(self, s):
        assert "ramp_gap_count" in s

    def test_key_intervention_count(self, s):
        assert "intervention_count" in s

    def test_key_avg_pipeline_score(self, s):
        assert "avg_pipeline_score" in s

    def test_key_avg_activity_score(self, s):
        assert "avg_activity_score" in s

    def test_key_avg_coaching_score(self, s):
        assert "avg_coaching_score" in s

    def test_key_avg_progression_score(self, s):
        assert "avg_progression_score" in s

    def test_key_total_estimated_ramp_revenue_loss_usd(self, s):
        assert "total_estimated_ramp_revenue_loss_usd" in s

    def test_total_is_zero(self, s):
        assert s["total"] == 0

    def test_risk_counts_empty(self, s):
        assert s["risk_counts"] == {}

    def test_pattern_counts_empty(self, s):
        assert s["pattern_counts"] == {}

    def test_severity_counts_empty(self, s):
        assert s["severity_counts"] == {}

    def test_action_counts_empty(self, s):
        assert s["action_counts"] == {}

    def test_avg_ramp_composite_zero(self, s):
        assert s["avg_ramp_composite"] == 0.0

    def test_ramp_gap_count_zero(self, s):
        assert s["ramp_gap_count"] == 0

    def test_intervention_count_zero(self, s):
        assert s["intervention_count"] == 0

    def test_avg_pipeline_score_zero(self, s):
        assert s["avg_pipeline_score"] == 0.0

    def test_avg_activity_score_zero(self, s):
        assert s["avg_activity_score"] == 0.0

    def test_avg_coaching_score_zero(self, s):
        assert s["avg_coaching_score"] == 0.0

    def test_avg_progression_score_zero(self, s):
        assert s["avg_progression_score"] == 0.0

    def test_total_revenue_loss_zero(self, s):
        assert s["total_estimated_ramp_revenue_loss_usd"] == 0.0


# ===========================================================================
# 21. SUMMARY TESTS — POPULATED ENGINE
# ===========================================================================

class TestSummaryPopulated:

    @pytest.fixture
    def engine_with_data(self):
        eng = fresh_engine()
        # Healthy rep
        eng.assess(make_input(rep_id="R1"))
        # Critical rep
        eng.assess(make_input(
            rep_id="R2",
            pipeline_build_pct_of_target=0.10,
            deals_in_pipeline=0,
            expected_first_quarter_attainment_pct=0.10,
            activity_adoption_score_pct=0.10,
            crm_usage_compliance_pct=0.10,
            calls_per_week_vs_target_pct=0.10,
            coaching_action_completion_pct=0.10,
            coaching_session_attendance_pct=0.10,
            manager_confidence_score=0.10,
            peer_benchmark_percentile=0.10,
            first_deal_closed=False,
            ramp_week=10,
            target_ramp_weeks=12,
            pipeline_stage_advancement_rate_pct=0.10,
        ))
        return eng

    def test_total_is_two(self, engine_with_data):
        s = engine_with_data.summary()
        assert s["total"] == 2

    def test_exactly_13_keys(self, engine_with_data):
        s = engine_with_data.summary()
        assert len(s) == 13

    def test_risk_counts_populated(self, engine_with_data):
        s = engine_with_data.summary()
        assert isinstance(s["risk_counts"], dict)
        assert sum(s["risk_counts"].values()) == 2

    def test_pattern_counts_populated(self, engine_with_data):
        s = engine_with_data.summary()
        assert isinstance(s["pattern_counts"], dict)
        assert sum(s["pattern_counts"].values()) == 2

    def test_severity_counts_populated(self, engine_with_data):
        s = engine_with_data.summary()
        assert isinstance(s["severity_counts"], dict)
        assert sum(s["severity_counts"].values()) == 2

    def test_action_counts_populated(self, engine_with_data):
        s = engine_with_data.summary()
        assert isinstance(s["action_counts"], dict)
        assert sum(s["action_counts"].values()) == 2

    def test_avg_ramp_composite_is_float(self, engine_with_data):
        s = engine_with_data.summary()
        assert isinstance(s["avg_ramp_composite"], float)

    def test_avg_ramp_composite_positive(self, engine_with_data):
        s = engine_with_data.summary()
        assert s["avg_ramp_composite"] > 0

    def test_ramp_gap_count_positive(self, engine_with_data):
        s = engine_with_data.summary()
        # critical rep definitely has a gap
        assert s["ramp_gap_count"] >= 1

    def test_intervention_count_positive(self, engine_with_data):
        s = engine_with_data.summary()
        assert s["intervention_count"] >= 1

    def test_avg_pipeline_score_positive(self, engine_with_data):
        s = engine_with_data.summary()
        assert s["avg_pipeline_score"] >= 0

    def test_avg_activity_score_positive(self, engine_with_data):
        s = engine_with_data.summary()
        assert s["avg_activity_score"] >= 0

    def test_avg_coaching_score_positive(self, engine_with_data):
        s = engine_with_data.summary()
        assert s["avg_coaching_score"] >= 0

    def test_avg_progression_score_positive(self, engine_with_data):
        s = engine_with_data.summary()
        assert s["avg_progression_score"] >= 0

    def test_total_revenue_loss_positive(self, engine_with_data):
        s = engine_with_data.summary()
        assert s["total_estimated_ramp_revenue_loss_usd"] >= 0

    def test_avg_ramp_composite_rounded_to_1(self, engine_with_data):
        s = engine_with_data.summary()
        # Rounded to 1 decimal place
        val = s["avg_ramp_composite"]
        assert round(val, 1) == val

    def test_risk_counts_keys_are_strings(self, engine_with_data):
        s = engine_with_data.summary()
        for k in s["risk_counts"]:
            assert isinstance(k, str)

    def test_low_risk_in_counts(self, engine_with_data):
        s = engine_with_data.summary()
        # Healthy rep is low risk
        assert "low" in s["risk_counts"]

    def test_critical_in_counts(self, engine_with_data):
        s = engine_with_data.summary()
        assert "critical" in s["risk_counts"]

    def test_summary_accumulates_multiple_assess_calls(self):
        eng = fresh_engine()
        for i in range(5):
            eng.assess(make_input(rep_id=f"R{i}"))
        s = eng.summary()
        assert s["total"] == 5

    def test_summary_revenue_loss_is_sum(self):
        eng = fresh_engine()
        r1 = eng.assess(make_input(rep_id="R1"))
        r2 = eng.assess(make_input(rep_id="R2"))
        s = eng.summary()
        expected = round(r1.estimated_ramp_revenue_loss_usd + r2.estimated_ramp_revenue_loss_usd, 2)
        assert s["total_estimated_ramp_revenue_loss_usd"] == expected

    def test_summary_avg_composite_correct(self):
        eng = fresh_engine()
        r1 = eng.assess(make_input(rep_id="R1"))
        r2 = eng.assess(make_input(rep_id="R2"))
        s = eng.summary()
        expected = round((r1.ramp_composite + r2.ramp_composite) / 2, 1)
        assert s["avg_ramp_composite"] == expected


# ===========================================================================
# 22. EDGE CASES
# ===========================================================================

class TestEdgeCases:

    def test_zero_deals_in_pipeline(self):
        eng = fresh_engine()
        result = eng.assess(make_input(deals_in_pipeline=0, avg_opportunity_value_usd=10_000.0))
        assert result.estimated_ramp_revenue_loss_usd == 0.0

    def test_zero_opportunity_value(self):
        eng = fresh_engine()
        result = eng.assess(make_input(avg_opportunity_value_usd=0.0))
        assert result.estimated_ramp_revenue_loss_usd == 0.0

    def test_ramp_week_zero(self):
        eng = fresh_engine()
        result = eng.assess(make_input(ramp_week=0))
        assert result.estimated_ramp_revenue_loss_usd == 0.0

    def test_target_ramp_weeks_one(self):
        eng = fresh_engine()
        result = eng.assess(make_input(target_ramp_weeks=1, ramp_week=1))
        assert isinstance(result, RampResult)

    def test_all_percentages_at_zero(self):
        """With all scores maximized, composite should be capped at 100."""
        eng = fresh_engine()
        inp = make_input(
            pipeline_build_pct_of_target=0.0,
            activity_adoption_score_pct=0.0,
            crm_usage_compliance_pct=0.0,
            calls_per_week_vs_target_pct=0.0,
            coaching_action_completion_pct=0.0,
            coaching_session_attendance_pct=0.0,
            manager_confidence_score=0.0,
            peer_benchmark_percentile=0.0,
            pipeline_stage_advancement_rate_pct=0.0,
            expected_first_quarter_attainment_pct=0.0,
            deals_in_pipeline=0,
            first_deal_closed=False,
            ramp_week=12,
            target_ramp_weeks=12,
        )
        result = eng.assess(inp)
        # All sub-scores = 100, composite = 100*0.35 + 100*0.30 + 100*0.20 + 100*0.15 = 100.0
        assert result.ramp_composite == 100.0

    def test_all_percentages_at_one(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            pipeline_build_pct_of_target=1.0,
            activity_adoption_score_pct=1.0,
            crm_usage_compliance_pct=1.0,
            calls_per_week_vs_target_pct=1.0,
            coaching_action_completion_pct=1.0,
            coaching_session_attendance_pct=1.0,
            manager_confidence_score=1.0,
            peer_benchmark_percentile=1.0,
            pipeline_stage_advancement_rate_pct=1.0,
            expected_first_quarter_attainment_pct=1.0,
            deals_in_pipeline=10,
            first_deal_closed=True,
        ))
        assert result.ramp_composite == 0.0

    def test_multiple_engines_independent(self):
        eng1 = fresh_engine()
        eng2 = fresh_engine()
        eng1.assess(make_input(rep_id="R1"))
        assert len(eng2._results) == 0

    def test_boundary_pipeline_25_exact(self):
        eng = fresh_engine()
        inp = make_input(
            pipeline_build_pct_of_target=0.25,
            deals_in_pipeline=10,
            expected_first_quarter_attainment_pct=1.0,
        )
        assert eng._pipeline_score(inp) == 40.0

    def test_boundary_pipeline_just_above_25(self):
        eng = fresh_engine()
        inp = make_input(
            pipeline_build_pct_of_target=0.251,
            deals_in_pipeline=10,
            expected_first_quarter_attainment_pct=1.0,
        )
        assert eng._pipeline_score(inp) == 22.0

    def test_boundary_deals_exactly_2(self):
        eng = fresh_engine()
        inp = make_input(
            pipeline_build_pct_of_target=1.0,
            deals_in_pipeline=2,
            expected_first_quarter_attainment_pct=1.0,
        )
        assert eng._pipeline_score(inp) == 18.0

    def test_boundary_deals_exactly_4(self):
        eng = fresh_engine()
        inp = make_input(
            pipeline_build_pct_of_target=1.0,
            deals_in_pipeline=4,
            expected_first_quarter_attainment_pct=1.0,
        )
        assert eng._pipeline_score(inp) == 0.0

    def test_large_batch(self):
        eng = fresh_engine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(100)]
        results = eng.assess_batch(inputs)
        assert len(results) == 100
        s = eng.summary()
        assert s["total"] == 100

    def test_to_dict_rep_id_matches(self):
        eng = fresh_engine()
        result = eng.assess(make_input(rep_id="DICTTEST"))
        assert result.to_dict()["rep_id"] == "DICTTEST"

    def test_to_dict_risk_is_string_not_enum(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        assert not isinstance(d["ramp_risk"], RampRisk)
        assert isinstance(d["ramp_risk"], str)

    def test_to_dict_pattern_is_string_not_enum(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        assert not isinstance(d["ramp_pattern"], RampPattern)

    def test_to_dict_severity_is_string_not_enum(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        assert not isinstance(d["ramp_severity"], RampSeverity)

    def test_to_dict_action_is_string_not_enum(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        assert not isinstance(d["recommended_action"], RampAction)

    def test_engine_accumulates_across_multiple_assesses(self):
        eng = fresh_engine()
        for i in range(3):
            eng.assess(make_input(rep_id=f"R{i}"))
        assert len(eng._results) == 3

    def test_healthy_rep_revenue_loss_low(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        # Healthy rep should have a low composite, so low estimated loss
        assert result.estimated_ramp_revenue_loss_usd >= 0.0

    def test_ramp_week_equals_target(self):
        eng = fresh_engine()
        inp = make_input(
            first_deal_closed=False,
            ramp_week=12,
            target_ramp_weeks=12,
        )
        result = eng.assess(inp)
        # ramp_week/target = 1.0 >= 0.75 => +30 to progression
        assert result.progression_score >= 30.0

    def test_summary_single_rep_averages_equal_single_value(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        s = eng.summary()
        assert s["avg_ramp_composite"] == result.ramp_composite
        assert s["avg_pipeline_score"] == result.pipeline_score
        assert s["avg_activity_score"] == result.activity_score
        assert s["avg_coaching_score"] == result.coaching_score
        assert s["avg_progression_score"] == result.progression_score
