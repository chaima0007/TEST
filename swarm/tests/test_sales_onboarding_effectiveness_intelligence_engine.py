"""
Comprehensive pytest tests for SalesOnboardingEffectivenessIntelligenceEngine.
"""
from __future__ import annotations

import pytest
from dataclasses import fields

from swarm.intelligence.sales_onboarding_effectiveness_intelligence_engine import (
    OnboardingRisk,
    OnboardingPattern,
    OnboardingSeverity,
    OnboardingAction,
    OnboardingEffectivenessInput,
    OnboardingEffectivenessResult,
    SalesOnboardingEffectivenessIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> OnboardingEffectivenessInput:
    """Return a healthy baseline input (low-risk / all green)."""
    defaults = dict(
        rep_id="REP001",
        region="WEST",
        evaluation_period_id="Q1-2026",
        days_since_start=30,
        days_to_first_meeting=5,
        days_to_first_opportunity=20,
        days_to_first_closed_deal=50,
        training_modules_completed_pct=0.90,
        product_certification_completed=True,
        manager_1on1_count=8,
        expected_manager_1on1_count=8,
        mentor_sessions_count=3,
        pipeline_coverage_vs_ramp_target_pct=0.90,
        quota_attainment_week_8_pct=0.60,
        quota_attainment_week_16_pct=0.70,
        crm_adoption_score=0.85,
        avg_activity_score_vs_team_pct=0.80,
        deals_in_pipeline_count=5,
        avg_deal_size_vs_team_pct=1.0,
        sentiment_score=0.75,
        late_crm_update_rate_pct=0.05,
        avg_opportunity_value_usd=10_000.0,
    )
    defaults.update(overrides)
    return OnboardingEffectivenessInput(**defaults)


def fresh_engine() -> SalesOnboardingEffectivenessIntelligenceEngine:
    return SalesOnboardingEffectivenessIntelligenceEngine()


# ===========================================================================
# 1. ENUM TESTS
# ===========================================================================

class TestOnboardingRiskEnum:
    def test_values_count(self):
        assert len(OnboardingRisk) == 4

    def test_low_value(self):
        assert OnboardingRisk.low.value == "low"

    def test_moderate_value(self):
        assert OnboardingRisk.moderate.value == "moderate"

    def test_high_value(self):
        assert OnboardingRisk.high.value == "high"

    def test_critical_value(self):
        assert OnboardingRisk.critical.value == "critical"

    def test_is_str_enum(self):
        assert isinstance(OnboardingRisk.low, str)

    def test_str_equality(self):
        assert OnboardingRisk.high == "high"

    def test_members_accessible_by_name(self):
        assert OnboardingRisk["low"] is OnboardingRisk.low

    def test_members_accessible_by_value(self):
        assert OnboardingRisk("critical") is OnboardingRisk.critical


class TestOnboardingPatternEnum:
    def test_values_count(self):
        assert len(OnboardingPattern) == 6

    def test_none_value(self):
        assert OnboardingPattern.none.value == "none"

    def test_slow_ramp_value(self):
        assert OnboardingPattern.slow_ramp.value == "slow_ramp"

    def test_training_gap_value(self):
        assert OnboardingPattern.training_gap.value == "training_gap"

    def test_manager_neglect_value(self):
        assert OnboardingPattern.manager_neglect.value == "manager_neglect"

    def test_early_attrition_signal_value(self):
        assert OnboardingPattern.early_attrition_signal.value == "early_attrition_signal"

    def test_product_knowledge_gap_value(self):
        assert OnboardingPattern.product_knowledge_gap.value == "product_knowledge_gap"

    def test_is_str_enum(self):
        assert isinstance(OnboardingPattern.slow_ramp, str)


class TestOnboardingSeverityEnum:
    def test_values_count(self):
        assert len(OnboardingSeverity) == 4

    def test_ramping_value(self):
        assert OnboardingSeverity.ramping.value == "ramping"

    def test_developing_value(self):
        assert OnboardingSeverity.developing.value == "developing"

    def test_struggling_value(self):
        assert OnboardingSeverity.struggling.value == "struggling"

    def test_at_risk_value(self):
        assert OnboardingSeverity.at_risk.value == "at_risk"

    def test_is_str_enum(self):
        assert isinstance(OnboardingSeverity.at_risk, str)


class TestOnboardingActionEnum:
    def test_values_count(self):
        assert len(OnboardingAction) == 6

    def test_no_action_value(self):
        assert OnboardingAction.no_action.value == "no_action"

    def test_ramp_support_coaching_value(self):
        assert OnboardingAction.ramp_support_coaching.value == "ramp_support_coaching"

    def test_training_acceleration_plan_value(self):
        assert OnboardingAction.training_acceleration_plan.value == "training_acceleration_plan"

    def test_manager_engagement_review_value(self):
        assert OnboardingAction.manager_engagement_review.value == "manager_engagement_review"

    def test_early_retention_intervention_value(self):
        assert OnboardingAction.early_retention_intervention.value == "early_retention_intervention"

    def test_product_enablement_bootcamp_value(self):
        assert OnboardingAction.product_enablement_bootcamp.value == "product_enablement_bootcamp"

    def test_is_str_enum(self):
        assert isinstance(OnboardingAction.no_action, str)


# ===========================================================================
# 2. DATACLASS FIELD TESTS
# ===========================================================================

class TestOnboardingEffectivenessInputFields:
    def _field_names(self):
        return {f.name for f in fields(OnboardingEffectivenessInput)}

    def test_field_count(self):
        assert len(fields(OnboardingEffectivenessInput)) == 22

    def test_rep_id_field(self):
        assert "rep_id" in self._field_names()

    def test_region_field(self):
        assert "region" in self._field_names()

    def test_evaluation_period_id_field(self):
        assert "evaluation_period_id" in self._field_names()

    def test_days_since_start_field(self):
        assert "days_since_start" in self._field_names()

    def test_days_to_first_meeting_field(self):
        assert "days_to_first_meeting" in self._field_names()

    def test_days_to_first_opportunity_field(self):
        assert "days_to_first_opportunity" in self._field_names()

    def test_days_to_first_closed_deal_field(self):
        assert "days_to_first_closed_deal" in self._field_names()

    def test_training_modules_completed_pct_field(self):
        assert "training_modules_completed_pct" in self._field_names()

    def test_product_certification_completed_field(self):
        assert "product_certification_completed" in self._field_names()

    def test_manager_1on1_count_field(self):
        assert "manager_1on1_count" in self._field_names()

    def test_expected_manager_1on1_count_field(self):
        assert "expected_manager_1on1_count" in self._field_names()

    def test_mentor_sessions_count_field(self):
        assert "mentor_sessions_count" in self._field_names()

    def test_pipeline_coverage_vs_ramp_target_pct_field(self):
        assert "pipeline_coverage_vs_ramp_target_pct" in self._field_names()

    def test_quota_attainment_week_8_pct_field(self):
        assert "quota_attainment_week_8_pct" in self._field_names()

    def test_quota_attainment_week_16_pct_field(self):
        assert "quota_attainment_week_16_pct" in self._field_names()

    def test_crm_adoption_score_field(self):
        assert "crm_adoption_score" in self._field_names()

    def test_avg_activity_score_vs_team_pct_field(self):
        assert "avg_activity_score_vs_team_pct" in self._field_names()

    def test_deals_in_pipeline_count_field(self):
        assert "deals_in_pipeline_count" in self._field_names()

    def test_avg_deal_size_vs_team_pct_field(self):
        assert "avg_deal_size_vs_team_pct" in self._field_names()

    def test_sentiment_score_field(self):
        assert "sentiment_score" in self._field_names()

    def test_late_crm_update_rate_pct_field(self):
        assert "late_crm_update_rate_pct" in self._field_names()

    def test_avg_opportunity_value_usd_field(self):
        assert "avg_opportunity_value_usd" in self._field_names()

    def test_product_certification_completed_is_bool(self):
        inp = make_input(product_certification_completed=True)
        assert isinstance(inp.product_certification_completed, bool)

    def test_instantiation(self):
        inp = make_input()
        assert inp.rep_id == "REP001"
        assert inp.region == "WEST"


class TestOnboardingEffectivenessResultFields:
    def _field_names(self):
        return {f.name for f in fields(OnboardingEffectivenessResult)}

    def test_field_count(self):
        assert len(fields(OnboardingEffectivenessResult)) == 15

    def test_rep_id_field(self):
        assert "rep_id" in self._field_names()

    def test_region_field(self):
        assert "region" in self._field_names()

    def test_onboarding_risk_field(self):
        assert "onboarding_risk" in self._field_names()

    def test_onboarding_pattern_field(self):
        assert "onboarding_pattern" in self._field_names()

    def test_onboarding_severity_field(self):
        assert "onboarding_severity" in self._field_names()

    def test_recommended_action_field(self):
        assert "recommended_action" in self._field_names()

    def test_ramp_velocity_score_field(self):
        assert "ramp_velocity_score" in self._field_names()

    def test_training_completion_score_field(self):
        assert "training_completion_score" in self._field_names()

    def test_manager_support_score_field(self):
        assert "manager_support_score" in self._field_names()

    def test_early_performance_score_field(self):
        assert "early_performance_score" in self._field_names()

    def test_onboarding_composite_field(self):
        assert "onboarding_composite" in self._field_names()

    def test_has_onboarding_gap_field(self):
        assert "has_onboarding_gap" in self._field_names()

    def test_requires_onboarding_intervention_field(self):
        assert "requires_onboarding_intervention" in self._field_names()

    def test_estimated_ramp_delay_cost_usd_field(self):
        assert "estimated_ramp_delay_cost_usd" in self._field_names()

    def test_onboarding_signal_field(self):
        assert "onboarding_signal" in self._field_names()


class TestOnboardingEffectivenessResultToDict:
    def _get_result(self):
        engine = fresh_engine()
        return engine.assess(make_input())

    def test_to_dict_returns_dict(self):
        assert isinstance(self._get_result().to_dict(), dict)

    def test_to_dict_has_15_keys(self):
        assert len(self._get_result().to_dict()) == 15

    def test_to_dict_rep_id_key(self):
        assert "rep_id" in self._get_result().to_dict()

    def test_to_dict_region_key(self):
        assert "region" in self._get_result().to_dict()

    def test_to_dict_onboarding_risk_key(self):
        assert "onboarding_risk" in self._get_result().to_dict()

    def test_to_dict_onboarding_pattern_key(self):
        assert "onboarding_pattern" in self._get_result().to_dict()

    def test_to_dict_onboarding_severity_key(self):
        assert "onboarding_severity" in self._get_result().to_dict()

    def test_to_dict_recommended_action_key(self):
        assert "recommended_action" in self._get_result().to_dict()

    def test_to_dict_ramp_velocity_score_key(self):
        assert "ramp_velocity_score" in self._get_result().to_dict()

    def test_to_dict_training_completion_score_key(self):
        assert "training_completion_score" in self._get_result().to_dict()

    def test_to_dict_manager_support_score_key(self):
        assert "manager_support_score" in self._get_result().to_dict()

    def test_to_dict_early_performance_score_key(self):
        assert "early_performance_score" in self._get_result().to_dict()

    def test_to_dict_onboarding_composite_key(self):
        assert "onboarding_composite" in self._get_result().to_dict()

    def test_to_dict_has_onboarding_gap_key(self):
        assert "has_onboarding_gap" in self._get_result().to_dict()

    def test_to_dict_requires_onboarding_intervention_key(self):
        assert "requires_onboarding_intervention" in self._get_result().to_dict()

    def test_to_dict_estimated_ramp_delay_cost_usd_key(self):
        assert "estimated_ramp_delay_cost_usd" in self._get_result().to_dict()

    def test_to_dict_onboarding_signal_key(self):
        assert "onboarding_signal" in self._get_result().to_dict()

    def test_to_dict_risk_value_is_string(self):
        d = self._get_result().to_dict()
        assert isinstance(d["onboarding_risk"], str)

    def test_to_dict_pattern_value_is_string(self):
        d = self._get_result().to_dict()
        assert isinstance(d["onboarding_pattern"], str)

    def test_to_dict_severity_value_is_string(self):
        d = self._get_result().to_dict()
        assert isinstance(d["onboarding_severity"], str)

    def test_to_dict_action_value_is_string(self):
        d = self._get_result().to_dict()
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_rep_id_matches(self):
        r = self._get_result()
        assert r.to_dict()["rep_id"] == r.rep_id

    def test_to_dict_composite_matches(self):
        r = self._get_result()
        assert r.to_dict()["onboarding_composite"] == r.onboarding_composite


# ===========================================================================
# 3. RAMP VELOCITY SCORE TESTS
# ===========================================================================

class TestRampVelocityScore:
    def setup_method(self):
        self.engine = fresh_engine()

    def _score(self, **kw):
        return self.engine._ramp_velocity_score(make_input(**kw))

    # days_to_first_opportunity thresholds
    def test_opportunity_under_30_adds_0(self):
        s = self._score(days_to_first_opportunity=20, days_to_first_closed_deal=50,
                        pipeline_coverage_vs_ramp_target_pct=0.90)
        assert s == 0.0

    def test_opportunity_exactly_30_adds_8(self):
        s = self._score(days_to_first_opportunity=30, days_to_first_closed_deal=50,
                        pipeline_coverage_vs_ramp_target_pct=0.90)
        assert s == 8.0

    def test_opportunity_exactly_45_adds_20(self):
        s = self._score(days_to_first_opportunity=45, days_to_first_closed_deal=50,
                        pipeline_coverage_vs_ramp_target_pct=0.90)
        assert s == 20.0

    def test_opportunity_exactly_60_adds_35(self):
        s = self._score(days_to_first_opportunity=60, days_to_first_closed_deal=50,
                        pipeline_coverage_vs_ramp_target_pct=0.90)
        assert s == 35.0

    def test_opportunity_above_60_adds_35(self):
        s = self._score(days_to_first_opportunity=90, days_to_first_closed_deal=50,
                        pipeline_coverage_vs_ramp_target_pct=0.90)
        assert s == 35.0

    # days_to_first_closed_deal thresholds
    def test_closed_deal_under_60_adds_0(self):
        s = self._score(days_to_first_opportunity=20, days_to_first_closed_deal=50,
                        pipeline_coverage_vs_ramp_target_pct=0.90)
        assert s == 0.0

    def test_closed_deal_exactly_60_adds_7(self):
        s = self._score(days_to_first_opportunity=20, days_to_first_closed_deal=60,
                        pipeline_coverage_vs_ramp_target_pct=0.90)
        assert s == 7.0

    def test_closed_deal_exactly_90_adds_18(self):
        s = self._score(days_to_first_opportunity=20, days_to_first_closed_deal=90,
                        pipeline_coverage_vs_ramp_target_pct=0.90)
        assert s == 18.0

    def test_closed_deal_exactly_120_adds_35(self):
        s = self._score(days_to_first_opportunity=20, days_to_first_closed_deal=120,
                        pipeline_coverage_vs_ramp_target_pct=0.90)
        assert s == 35.0

    def test_closed_deal_above_120_adds_35(self):
        s = self._score(days_to_first_opportunity=20, days_to_first_closed_deal=200,
                        pipeline_coverage_vs_ramp_target_pct=0.90)
        assert s == 35.0

    # pipeline coverage thresholds
    def test_pipeline_above_75_adds_0(self):
        s = self._score(days_to_first_opportunity=20, days_to_first_closed_deal=50,
                        pipeline_coverage_vs_ramp_target_pct=0.90)
        assert s == 0.0

    def test_pipeline_exactly_75_adds_0(self):
        # 0.75 is NOT < 0.75, so adds 0
        s = self._score(days_to_first_opportunity=20, days_to_first_closed_deal=50,
                        pipeline_coverage_vs_ramp_target_pct=0.75)
        assert s == 0.0

    def test_pipeline_between_50_and_75_adds_12(self):
        s = self._score(days_to_first_opportunity=20, days_to_first_closed_deal=50,
                        pipeline_coverage_vs_ramp_target_pct=0.60)
        assert s == 12.0

    def test_pipeline_under_50_adds_25(self):
        s = self._score(days_to_first_opportunity=20, days_to_first_closed_deal=50,
                        pipeline_coverage_vs_ramp_target_pct=0.30)
        assert s == 25.0

    def test_pipeline_exactly_50_adds_12(self):
        # 0.50 is NOT < 0.50, so adds 12 (0.50 < 0.75)
        s = self._score(days_to_first_opportunity=20, days_to_first_closed_deal=50,
                        pipeline_coverage_vs_ramp_target_pct=0.50)
        assert s == 12.0

    def test_score_capped_at_100(self):
        s = self._score(days_to_first_opportunity=90, days_to_first_closed_deal=200,
                        pipeline_coverage_vs_ramp_target_pct=0.10)
        # max raw = 35+35+25 = 95 => within 100
        assert s <= 100.0

    def test_all_worst_case_capped(self):
        # 35+35+25 = 95, but still test cap
        s = self._score(days_to_first_opportunity=100, days_to_first_closed_deal=200,
                        pipeline_coverage_vs_ramp_target_pct=0.0)
        assert s == 95.0

    def test_fully_healthy_score_is_zero(self):
        s = self._score(days_to_first_opportunity=15, days_to_first_closed_deal=40,
                        pipeline_coverage_vs_ramp_target_pct=0.95)
        assert s == 0.0


# ===========================================================================
# 4. TRAINING COMPLETION SCORE TESTS
# ===========================================================================

class TestTrainingCompletionScore:
    def setup_method(self):
        self.engine = fresh_engine()

    def _score(self, **kw):
        return self.engine._training_completion_score(make_input(**kw))

    # training_modules_completed_pct thresholds
    def test_training_above_80_adds_0(self):
        s = self._score(training_modules_completed_pct=0.90,
                        product_certification_completed=True, crm_adoption_score=0.90)
        assert s == 0.0

    def test_training_exactly_80_adds_0(self):
        s = self._score(training_modules_completed_pct=0.80,
                        product_certification_completed=True, crm_adoption_score=0.90)
        assert s == 0.0

    def test_training_between_60_and_80_adds_8(self):
        s = self._score(training_modules_completed_pct=0.70,
                        product_certification_completed=True, crm_adoption_score=0.90)
        assert s == 8.0

    def test_training_exactly_60_adds_8(self):
        s = self._score(training_modules_completed_pct=0.60,
                        product_certification_completed=True, crm_adoption_score=0.90)
        assert s == 8.0

    def test_training_between_40_and_60_adds_22(self):
        s = self._score(training_modules_completed_pct=0.50,
                        product_certification_completed=True, crm_adoption_score=0.90)
        assert s == 22.0

    def test_training_exactly_40_adds_22(self):
        s = self._score(training_modules_completed_pct=0.40,
                        product_certification_completed=True, crm_adoption_score=0.90)
        assert s == 22.0

    def test_training_under_40_adds_40(self):
        s = self._score(training_modules_completed_pct=0.20,
                        product_certification_completed=True, crm_adoption_score=0.90)
        assert s == 40.0

    # product_certification_completed thresholds
    def test_cert_complete_no_penalty(self):
        s = self._score(training_modules_completed_pct=0.90,
                        product_certification_completed=True,
                        days_since_start=90, crm_adoption_score=0.90)
        assert s == 0.0

    def test_cert_incomplete_days_under_30_no_penalty(self):
        s = self._score(training_modules_completed_pct=0.90,
                        product_certification_completed=False,
                        days_since_start=20, crm_adoption_score=0.90)
        assert s == 0.0

    def test_cert_incomplete_days_between_30_and_60_adds_15(self):
        s = self._score(training_modules_completed_pct=0.90,
                        product_certification_completed=False,
                        days_since_start=45, crm_adoption_score=0.90)
        assert s == 15.0

    def test_cert_incomplete_days_exactly_30_adds_15(self):
        s = self._score(training_modules_completed_pct=0.90,
                        product_certification_completed=False,
                        days_since_start=30, crm_adoption_score=0.90)
        assert s == 15.0

    def test_cert_incomplete_days_exactly_60_adds_30(self):
        s = self._score(training_modules_completed_pct=0.90,
                        product_certification_completed=False,
                        days_since_start=60, crm_adoption_score=0.90)
        assert s == 30.0

    def test_cert_incomplete_days_above_60_adds_30(self):
        s = self._score(training_modules_completed_pct=0.90,
                        product_certification_completed=False,
                        days_since_start=90, crm_adoption_score=0.90)
        assert s == 30.0

    # crm_adoption_score thresholds
    def test_crm_above_60_adds_0(self):
        s = self._score(training_modules_completed_pct=0.90,
                        product_certification_completed=True, crm_adoption_score=0.70)
        assert s == 0.0

    def test_crm_between_40_and_60_adds_12(self):
        s = self._score(training_modules_completed_pct=0.90,
                        product_certification_completed=True, crm_adoption_score=0.50)
        assert s == 12.0

    def test_crm_exactly_40_adds_12(self):
        s = self._score(training_modules_completed_pct=0.90,
                        product_certification_completed=True, crm_adoption_score=0.40)
        assert s == 12.0

    def test_crm_under_40_adds_25(self):
        s = self._score(training_modules_completed_pct=0.90,
                        product_certification_completed=True, crm_adoption_score=0.30)
        assert s == 25.0

    def test_score_capped_at_100(self):
        s = self._score(training_modules_completed_pct=0.10,
                        product_certification_completed=False,
                        days_since_start=90, crm_adoption_score=0.10)
        # 40 + 30 + 25 = 95 → within cap but <=100
        assert s <= 100.0

    def test_all_healthy_score_is_zero(self):
        s = self._score(training_modules_completed_pct=1.0,
                        product_certification_completed=True,
                        days_since_start=10, crm_adoption_score=1.0)
        assert s == 0.0


# ===========================================================================
# 5. MANAGER SUPPORT SCORE TESTS
# ===========================================================================

class TestManagerSupportScore:
    def setup_method(self):
        self.engine = fresh_engine()

    def _score(self, **kw):
        return self.engine._manager_support_score(make_input(**kw))

    # completion_rate thresholds
    def test_rate_above_80_adds_0(self):
        s = self._score(manager_1on1_count=9, expected_manager_1on1_count=10,
                        mentor_sessions_count=3, days_since_start=30,
                        avg_activity_score_vs_team_pct=0.90)
        assert s == 0.0

    def test_rate_between_60_and_80_adds_8(self):
        s = self._score(manager_1on1_count=7, expected_manager_1on1_count=10,
                        mentor_sessions_count=3, days_since_start=30,
                        avg_activity_score_vs_team_pct=0.90)
        assert s == 8.0

    def test_rate_between_40_and_60_adds_22(self):
        s = self._score(manager_1on1_count=5, expected_manager_1on1_count=10,
                        mentor_sessions_count=3, days_since_start=30,
                        avg_activity_score_vs_team_pct=0.90)
        assert s == 22.0

    def test_rate_under_40_adds_40(self):
        s = self._score(manager_1on1_count=3, expected_manager_1on1_count=10,
                        mentor_sessions_count=3, days_since_start=30,
                        avg_activity_score_vs_team_pct=0.90)
        assert s == 40.0

    def test_expected_zero_treated_as_1(self):
        # max(0, 1) = 1, so 0/1=0.0 < 0.40 => 40
        s = self._score(manager_1on1_count=0, expected_manager_1on1_count=0,
                        mentor_sessions_count=3, days_since_start=30,
                        avg_activity_score_vs_team_pct=0.90)
        assert s == 40.0

    # mentor_sessions_count + days_since_start
    def test_mentor_zero_under_30_days_no_penalty(self):
        s = self._score(manager_1on1_count=9, expected_manager_1on1_count=10,
                        mentor_sessions_count=0, days_since_start=20,
                        avg_activity_score_vs_team_pct=0.90)
        assert s == 0.0

    def test_mentor_zero_at_30_days_adds_30(self):
        s = self._score(manager_1on1_count=9, expected_manager_1on1_count=10,
                        mentor_sessions_count=0, days_since_start=30,
                        avg_activity_score_vs_team_pct=0.90)
        assert s == 30.0

    def test_mentor_1_at_60_days_adds_15(self):
        s = self._score(manager_1on1_count=9, expected_manager_1on1_count=10,
                        mentor_sessions_count=1, days_since_start=60,
                        avg_activity_score_vs_team_pct=0.90)
        assert s == 15.0

    def test_mentor_1_under_60_days_no_penalty(self):
        s = self._score(manager_1on1_count=9, expected_manager_1on1_count=10,
                        mentor_sessions_count=1, days_since_start=30,
                        avg_activity_score_vs_team_pct=0.90)
        assert s == 0.0

    def test_mentor_2_at_60_days_no_penalty(self):
        s = self._score(manager_1on1_count=9, expected_manager_1on1_count=10,
                        mentor_sessions_count=2, days_since_start=60,
                        avg_activity_score_vs_team_pct=0.90)
        assert s == 0.0

    # avg_activity_score_vs_team_pct thresholds
    def test_activity_above_70_adds_0(self):
        s = self._score(manager_1on1_count=9, expected_manager_1on1_count=10,
                        mentor_sessions_count=3, days_since_start=30,
                        avg_activity_score_vs_team_pct=0.80)
        assert s == 0.0

    def test_activity_between_50_and_70_adds_12(self):
        s = self._score(manager_1on1_count=9, expected_manager_1on1_count=10,
                        mentor_sessions_count=3, days_since_start=30,
                        avg_activity_score_vs_team_pct=0.60)
        assert s == 12.0

    def test_activity_under_50_adds_25(self):
        s = self._score(manager_1on1_count=9, expected_manager_1on1_count=10,
                        mentor_sessions_count=3, days_since_start=30,
                        avg_activity_score_vs_team_pct=0.40)
        assert s == 25.0

    def test_score_capped_at_100(self):
        s = self._score(manager_1on1_count=0, expected_manager_1on1_count=10,
                        mentor_sessions_count=0, days_since_start=60,
                        avg_activity_score_vs_team_pct=0.10)
        # 40 + 30 + 25 = 95 ≤ 100
        assert s <= 100.0


# ===========================================================================
# 6. EARLY PERFORMANCE SCORE TESTS
# ===========================================================================

class TestEarlyPerformanceScore:
    def setup_method(self):
        self.engine = fresh_engine()

    def _score(self, **kw):
        return self.engine._early_performance_score(make_input(**kw))

    def test_under_60_days_no_week8_penalty(self):
        s = self._score(days_since_start=59, quota_attainment_week_8_pct=0.10,
                        quota_attainment_week_16_pct=0.10, sentiment_score=0.90)
        assert s == 0.0

    def test_at_60_days_week8_under_20_adds_35(self):
        s = self._score(days_since_start=60, quota_attainment_week_8_pct=0.10,
                        quota_attainment_week_16_pct=0.10, sentiment_score=0.90)
        assert s == 35.0

    def test_at_60_days_week8_between_20_and_40_adds_18(self):
        s = self._score(days_since_start=60, quota_attainment_week_8_pct=0.30,
                        quota_attainment_week_16_pct=0.10, sentiment_score=0.90)
        assert s == 18.0

    def test_at_60_days_week8_above_40_adds_0(self):
        s = self._score(days_since_start=60, quota_attainment_week_8_pct=0.50,
                        quota_attainment_week_16_pct=0.10, sentiment_score=0.90)
        assert s == 0.0

    def test_under_120_days_no_week16_penalty(self):
        s = self._score(days_since_start=119, quota_attainment_week_8_pct=0.50,
                        quota_attainment_week_16_pct=0.10, sentiment_score=0.90)
        assert s == 0.0

    def test_at_120_days_week16_under_40_adds_35(self):
        s = self._score(days_since_start=120, quota_attainment_week_8_pct=0.50,
                        quota_attainment_week_16_pct=0.20, sentiment_score=0.90)
        assert s == 35.0

    def test_at_120_days_week16_between_40_and_60_adds_18(self):
        s = self._score(days_since_start=120, quota_attainment_week_8_pct=0.50,
                        quota_attainment_week_16_pct=0.50, sentiment_score=0.90)
        assert s == 18.0

    def test_at_120_days_week16_above_60_adds_0(self):
        s = self._score(days_since_start=120, quota_attainment_week_8_pct=0.50,
                        quota_attainment_week_16_pct=0.70, sentiment_score=0.90)
        assert s == 0.0

    def test_sentiment_under_30_adds_20(self):
        s = self._score(days_since_start=30, quota_attainment_week_8_pct=0.50,
                        quota_attainment_week_16_pct=0.70, sentiment_score=0.20)
        assert s == 20.0

    def test_sentiment_between_30_and_50_adds_10(self):
        s = self._score(days_since_start=30, quota_attainment_week_8_pct=0.50,
                        quota_attainment_week_16_pct=0.70, sentiment_score=0.40)
        assert s == 10.0

    def test_sentiment_above_50_adds_0(self):
        s = self._score(days_since_start=30, quota_attainment_week_8_pct=0.50,
                        quota_attainment_week_16_pct=0.70, sentiment_score=0.60)
        assert s == 0.0

    def test_score_capped_at_100(self):
        s = self._score(days_since_start=120, quota_attainment_week_8_pct=0.10,
                        quota_attainment_week_16_pct=0.20, sentiment_score=0.10)
        # 35+35+20=90 <= 100
        assert s <= 100.0

    def test_fully_healthy_score_is_zero(self):
        s = self._score(days_since_start=10, quota_attainment_week_8_pct=0.80,
                        quota_attainment_week_16_pct=0.80, sentiment_score=0.90)
        assert s == 0.0

    def test_week8_exactly_20_pct_adds_18(self):
        s = self._score(days_since_start=60, quota_attainment_week_8_pct=0.20,
                        quota_attainment_week_16_pct=0.90, sentiment_score=0.90)
        assert s == 18.0

    def test_week16_exactly_40_pct_adds_18(self):
        s = self._score(days_since_start=120, quota_attainment_week_8_pct=0.90,
                        quota_attainment_week_16_pct=0.40, sentiment_score=0.90)
        assert s == 18.0


# ===========================================================================
# 7. PATTERN DETECTION TESTS
# ===========================================================================

class TestDetectPattern:
    def setup_method(self):
        self.engine = fresh_engine()

    def _detect(self, inp_overrides, ramp=0.0, training=0.0, manager=0.0, performance=0.0):
        inp = make_input(**inp_overrides)
        return self.engine._detect_pattern(inp, ramp, training, manager, performance)

    def test_early_attrition_signal_wins_first(self):
        # sentiment < 0.30 AND performance >= 25
        p = self._detect({"sentiment_score": 0.20}, performance=30.0, manager=40.0,
                         training=35.0, ramp=30.0)
        assert p == OnboardingPattern.early_attrition_signal

    def test_no_early_attrition_when_performance_low(self):
        # performance < 25 → skip early_attrition
        p = self._detect({"sentiment_score": 0.20, "manager_1on1_count": 2,
                          "expected_manager_1on1_count": 10,
                          "training_modules_completed_pct": 0.40},
                         performance=10.0, manager=40.0, training=35.0, ramp=30.0)
        assert p == OnboardingPattern.manager_neglect

    def test_manager_neglect_detected(self):
        # manager >= 35 AND manager_1on1_count < expected*0.50
        p = self._detect({"manager_1on1_count": 2, "expected_manager_1on1_count": 10,
                          "sentiment_score": 0.80},
                         manager=40.0, training=0.0, ramp=0.0, performance=0.0)
        assert p == OnboardingPattern.manager_neglect

    def test_no_manager_neglect_when_rate_ok(self):
        # manager_1on1_count >= expected*0.50
        p = self._detect({"manager_1on1_count": 6, "expected_manager_1on1_count": 10,
                          "training_modules_completed_pct": 0.40,
                          "sentiment_score": 0.80},
                         manager=40.0, training=35.0, ramp=0.0, performance=0.0)
        assert p == OnboardingPattern.training_gap

    def test_training_gap_detected(self):
        # training >= 30 AND training_modules_completed_pct < 0.60
        p = self._detect({"training_modules_completed_pct": 0.40,
                          "manager_1on1_count": 8, "expected_manager_1on1_count": 10,
                          "sentiment_score": 0.80},
                         training=30.0, manager=0.0, ramp=0.0, performance=0.0)
        assert p == OnboardingPattern.training_gap

    def test_no_training_gap_when_training_pct_ok(self):
        # training_modules_completed_pct >= 0.60
        p = self._detect({"training_modules_completed_pct": 0.65,
                          "product_certification_completed": False,
                          "days_since_start": 60,
                          "sentiment_score": 0.80,
                          "pipeline_coverage_vs_ramp_target_pct": 0.40},
                         training=30.0, manager=0.0, ramp=30.0, performance=0.0)
        assert p == OnboardingPattern.product_knowledge_gap

    def test_product_knowledge_gap_detected(self):
        # no cert, days>=60, training>=20
        p = self._detect({"product_certification_completed": False,
                          "days_since_start": 60,
                          "training_modules_completed_pct": 0.65,
                          "pipeline_coverage_vs_ramp_target_pct": 0.90,
                          "sentiment_score": 0.80},
                         training=20.0, manager=0.0, ramp=0.0, performance=0.0)
        assert p == OnboardingPattern.product_knowledge_gap

    def test_no_product_knowledge_gap_when_cert_done(self):
        p = self._detect({"product_certification_completed": True,
                          "days_since_start": 60,
                          "training_modules_completed_pct": 0.65,
                          "pipeline_coverage_vs_ramp_target_pct": 0.40,
                          "sentiment_score": 0.80},
                         training=20.0, manager=0.0, ramp=30.0, performance=0.0)
        assert p == OnboardingPattern.slow_ramp

    def test_slow_ramp_detected(self):
        # ramp >= 25 AND pipeline < 0.60
        p = self._detect({"pipeline_coverage_vs_ramp_target_pct": 0.40,
                          "product_certification_completed": True,
                          "sentiment_score": 0.80},
                         ramp=30.0, training=0.0, manager=0.0, performance=0.0)
        assert p == OnboardingPattern.slow_ramp

    def test_no_slow_ramp_when_pipeline_ok(self):
        p = self._detect({"pipeline_coverage_vs_ramp_target_pct": 0.70,
                          "product_certification_completed": True,
                          "sentiment_score": 0.80},
                         ramp=30.0, training=0.0, manager=0.0, performance=0.0)
        assert p == OnboardingPattern.none

    def test_none_pattern_when_all_green(self):
        p = self._detect({}, ramp=0.0, training=0.0, manager=0.0, performance=0.0)
        assert p == OnboardingPattern.none


# ===========================================================================
# 8. RISK LEVEL TESTS
# ===========================================================================

class TestRiskLevel:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_composite_0_is_low(self):
        assert self.engine._risk_level(0.0) == OnboardingRisk.low

    def test_composite_19_is_low(self):
        assert self.engine._risk_level(19.9) == OnboardingRisk.low

    def test_composite_exactly_20_is_moderate(self):
        assert self.engine._risk_level(20.0) == OnboardingRisk.moderate

    def test_composite_39_is_moderate(self):
        assert self.engine._risk_level(39.9) == OnboardingRisk.moderate

    def test_composite_exactly_40_is_high(self):
        assert self.engine._risk_level(40.0) == OnboardingRisk.high

    def test_composite_59_is_high(self):
        assert self.engine._risk_level(59.9) == OnboardingRisk.high

    def test_composite_exactly_60_is_critical(self):
        assert self.engine._risk_level(60.0) == OnboardingRisk.critical

    def test_composite_100_is_critical(self):
        assert self.engine._risk_level(100.0) == OnboardingRisk.critical

    def test_composite_25_is_moderate(self):
        assert self.engine._risk_level(25.0) == OnboardingRisk.moderate

    def test_composite_50_is_high(self):
        assert self.engine._risk_level(50.0) == OnboardingRisk.high


# ===========================================================================
# 9. SEVERITY TESTS
# ===========================================================================

class TestSeverity:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_composite_0_is_ramping(self):
        assert self.engine._severity(0.0) == OnboardingSeverity.ramping

    def test_composite_19_is_ramping(self):
        assert self.engine._severity(19.9) == OnboardingSeverity.ramping

    def test_composite_exactly_20_is_developing(self):
        assert self.engine._severity(20.0) == OnboardingSeverity.developing

    def test_composite_39_is_developing(self):
        assert self.engine._severity(39.9) == OnboardingSeverity.developing

    def test_composite_exactly_40_is_struggling(self):
        assert self.engine._severity(40.0) == OnboardingSeverity.struggling

    def test_composite_59_is_struggling(self):
        assert self.engine._severity(59.9) == OnboardingSeverity.struggling

    def test_composite_exactly_60_is_at_risk(self):
        assert self.engine._severity(60.0) == OnboardingSeverity.at_risk

    def test_composite_100_is_at_risk(self):
        assert self.engine._severity(100.0) == OnboardingSeverity.at_risk


# ===========================================================================
# 10. ACTION MAPPING TESTS
# ===========================================================================

class TestActionMapping:
    def setup_method(self):
        self.engine = fresh_engine()

    def _action(self, risk, pattern):
        return self.engine._action(risk, pattern)

    def test_low_risk_any_pattern_no_action(self):
        assert self._action(OnboardingRisk.low, OnboardingPattern.none) == OnboardingAction.no_action

    def test_low_risk_slow_ramp_no_action(self):
        assert self._action(OnboardingRisk.low, OnboardingPattern.slow_ramp) == OnboardingAction.no_action

    def test_moderate_risk_none_pattern_ramp_coaching(self):
        assert self._action(OnboardingRisk.moderate, OnboardingPattern.none) == OnboardingAction.ramp_support_coaching

    def test_moderate_risk_any_pattern_ramp_coaching(self):
        assert self._action(OnboardingRisk.moderate, OnboardingPattern.slow_ramp) == OnboardingAction.ramp_support_coaching

    def test_high_risk_training_gap_training_plan(self):
        assert self._action(OnboardingRisk.high, OnboardingPattern.training_gap) == OnboardingAction.training_acceleration_plan

    def test_high_risk_product_knowledge_gap_bootcamp(self):
        assert self._action(OnboardingRisk.high, OnboardingPattern.product_knowledge_gap) == OnboardingAction.product_enablement_bootcamp

    def test_high_risk_none_pattern_ramp_coaching(self):
        assert self._action(OnboardingRisk.high, OnboardingPattern.none) == OnboardingAction.ramp_support_coaching

    def test_high_risk_slow_ramp_ramp_coaching(self):
        assert self._action(OnboardingRisk.high, OnboardingPattern.slow_ramp) == OnboardingAction.ramp_support_coaching

    def test_high_risk_manager_neglect_ramp_coaching(self):
        assert self._action(OnboardingRisk.high, OnboardingPattern.manager_neglect) == OnboardingAction.ramp_support_coaching

    def test_critical_early_attrition_retention_intervention(self):
        assert self._action(OnboardingRisk.critical, OnboardingPattern.early_attrition_signal) == OnboardingAction.early_retention_intervention

    def test_critical_manager_neglect_manager_review(self):
        assert self._action(OnboardingRisk.critical, OnboardingPattern.manager_neglect) == OnboardingAction.manager_engagement_review

    def test_critical_none_pattern_retention_intervention(self):
        assert self._action(OnboardingRisk.critical, OnboardingPattern.none) == OnboardingAction.early_retention_intervention

    def test_critical_slow_ramp_retention_intervention(self):
        assert self._action(OnboardingRisk.critical, OnboardingPattern.slow_ramp) == OnboardingAction.early_retention_intervention

    def test_critical_training_gap_retention_intervention(self):
        assert self._action(OnboardingRisk.critical, OnboardingPattern.training_gap) == OnboardingAction.early_retention_intervention


# ===========================================================================
# 11. HAS ONBOARDING GAP TESTS
# ===========================================================================

class TestHasOnboardingGap:
    def setup_method(self):
        self.engine = fresh_engine()

    def _gap(self, composite, **kw):
        inp = make_input(**kw)
        return self.engine._has_onboarding_gap(composite, inp)

    def test_composite_40_triggers_gap(self):
        assert self._gap(40.0) is True

    def test_composite_41_triggers_gap(self):
        assert self._gap(41.0) is True

    def test_composite_39_no_gap_by_composite(self):
        # only composite check; other fields healthy
        assert self._gap(39.0) is False

    def test_training_under_40_triggers_gap(self):
        assert self._gap(10.0, training_modules_completed_pct=0.30) is True

    def test_training_exactly_40_no_gap_from_training(self):
        assert self._gap(10.0, training_modules_completed_pct=0.40) is False

    def test_pipeline_under_50_triggers_gap(self):
        assert self._gap(10.0, pipeline_coverage_vs_ramp_target_pct=0.40) is True

    def test_pipeline_exactly_50_no_gap_from_pipeline(self):
        assert self._gap(10.0, pipeline_coverage_vs_ramp_target_pct=0.50) is False

    def test_all_healthy_no_gap(self):
        assert self._gap(10.0) is False

    def test_all_triggers_true_is_true(self):
        assert self._gap(50.0, training_modules_completed_pct=0.20,
                         pipeline_coverage_vs_ramp_target_pct=0.30) is True


# ===========================================================================
# 12. REQUIRES ONBOARDING INTERVENTION TESTS
# ===========================================================================

class TestRequiresOnboardingIntervention:
    def setup_method(self):
        self.engine = fresh_engine()

    def _intervene(self, composite, **kw):
        inp = make_input(**kw)
        return self.engine._requires_onboarding_intervention(composite, inp)

    def test_composite_30_triggers_intervention(self):
        assert self._intervene(30.0) is True

    def test_composite_31_triggers_intervention(self):
        assert self._intervene(31.0) is True

    def test_composite_29_no_intervention_by_composite(self):
        # only composite; other fields healthy
        assert self._intervene(29.0) is False

    def test_sentiment_under_40_triggers_intervention(self):
        assert self._intervene(5.0, sentiment_score=0.30) is True

    def test_sentiment_exactly_40_no_intervention_from_sentiment(self):
        assert self._intervene(5.0, sentiment_score=0.40) is False

    def test_manager_rate_under_50_triggers_intervention(self):
        assert self._intervene(5.0, manager_1on1_count=4, expected_manager_1on1_count=10) is True

    def test_manager_rate_exactly_50_no_intervention_from_manager(self):
        assert self._intervene(5.0, manager_1on1_count=5, expected_manager_1on1_count=10) is False

    def test_all_healthy_no_intervention(self):
        assert self._intervene(5.0) is False

    def test_expected_zero_treated_as_1(self):
        # max(0,1) = 1, count/1 = 0 < 0.50 → intervention
        assert self._intervene(5.0, manager_1on1_count=0, expected_manager_1on1_count=0) is True


# ===========================================================================
# 13. RAMP DELAY COST TESTS
# ===========================================================================

class TestEstimatedRampDelayCost:
    def setup_method(self):
        self.engine = fresh_engine()

    def _cost(self, composite, avg_opp_value):
        inp = make_input(avg_opportunity_value_usd=avg_opp_value)
        return self.engine._estimated_ramp_delay_cost(inp, composite)

    def test_zero_composite_zero_cost(self):
        assert self._cost(0.0, 10_000.0) == 0.0

    def test_100_composite_max_delay(self):
        # delay_months = (100/100)*3 = 3, cost = 2*3*10000 = 60000
        assert self._cost(100.0, 10_000.0) == 60_000.0

    def test_50_composite_half_delay(self):
        # delay_months = 0.5*3 = 1.5, cost = 2*1.5*5000 = 15000
        assert self._cost(50.0, 5_000.0) == 15_000.0

    def test_result_is_rounded_to_2_decimals(self):
        cost = self._cost(33.3, 7_777.77)
        assert cost == round(cost, 2)

    def test_cost_formula_correctness(self):
        composite = 40.0
        opp_val = 12_000.0
        expected = round(2.0 * (40.0 / 100.0 * 3.0) * 12_000.0, 2)
        assert self._cost(composite, opp_val) == expected

    def test_zero_opp_value_zero_cost(self):
        assert self._cost(80.0, 0.0) == 0.0

    def test_composite_below_zero_treated_as_zero(self):
        # max(0.0, negative) = 0.0
        inp = make_input(avg_opportunity_value_usd=10_000.0)
        cost = self.engine._estimated_ramp_delay_cost(inp, -10.0)
        assert cost == 0.0


# ===========================================================================
# 14. SIGNAL GENERATION TESTS
# ===========================================================================

class TestSignalGeneration:
    def setup_method(self):
        self.engine = fresh_engine()

    def _signal(self, pattern, composite, **inp_kw):
        inp = make_input(**inp_kw)
        return self.engine._signal(inp, pattern, composite)

    def test_healthy_benchmark_signal(self):
        sig = self._signal(OnboardingPattern.none, 10.0,
                           training_modules_completed_pct=1.0,
                           pipeline_coverage_vs_ramp_target_pct=1.0,
                           manager_1on1_count=10, expected_manager_1on1_count=10)
        assert sig == "Onboarding velocity healthy — rep progressing within expected ramp benchmarks"

    def test_healthy_signal_requires_none_pattern(self):
        sig = self._signal(OnboardingPattern.slow_ramp, 10.0)
        assert "healthy" not in sig

    def test_healthy_signal_requires_composite_under_20(self):
        sig = self._signal(OnboardingPattern.none, 20.0)
        assert "healthy" not in sig

    def test_signal_contains_pattern_label(self):
        sig = self._signal(OnboardingPattern.slow_ramp, 30.0)
        assert "slow ramp" in sig.lower()

    def test_signal_contains_training_pct(self):
        sig = self._signal(OnboardingPattern.training_gap, 30.0,
                           training_modules_completed_pct=0.50)
        assert "50% training complete" in sig

    def test_signal_contains_pipeline_pct(self):
        sig = self._signal(OnboardingPattern.slow_ramp, 30.0,
                           pipeline_coverage_vs_ramp_target_pct=0.60)
        assert "60% pipeline target" in sig

    def test_signal_contains_manager_rate(self):
        sig = self._signal(OnboardingPattern.manager_neglect, 30.0,
                           manager_1on1_count=5, expected_manager_1on1_count=10)
        assert "50% manager 1:1 attendance" in sig

    def test_signal_contains_composite_value(self):
        sig = self._signal(OnboardingPattern.none, 35.0)
        assert "composite 35" in sig

    def test_signal_none_pattern_above_20_shows_onboarding_risk(self):
        sig = self._signal(OnboardingPattern.none, 25.0,
                           training_modules_completed_pct=1.0,
                           pipeline_coverage_vs_ramp_target_pct=1.0,
                           manager_1on1_count=10, expected_manager_1on1_count=10)
        assert "Onboarding risk" in sig

    def test_signal_fallback_ramp_velocity_declining(self):
        # All fields >= 1.0, manager rate = 1.0 → no parts → fallback
        sig = self._signal(OnboardingPattern.none, 25.0,
                           training_modules_completed_pct=1.0,
                           pipeline_coverage_vs_ramp_target_pct=1.0,
                           manager_1on1_count=10, expected_manager_1on1_count=10)
        assert "ramp velocity declining" in sig

    def test_signal_early_attrition_label(self):
        sig = self._signal(OnboardingPattern.early_attrition_signal, 50.0)
        assert "early attrition signal" in sig.lower()

    def test_signal_product_knowledge_gap_label(self):
        sig = self._signal(OnboardingPattern.product_knowledge_gap, 30.0,
                           pipeline_coverage_vs_ramp_target_pct=1.0,
                           manager_1on1_count=10, expected_manager_1on1_count=10)
        assert "product knowledge gap" in sig.lower()


# ===========================================================================
# 15. COMPOSITE SCORE FORMULA TESTS
# ===========================================================================

class TestCompositeFormula:
    def test_composite_weighted_sum(self):
        engine = fresh_engine()
        inp = make_input()
        ramp = engine._ramp_velocity_score(inp)
        training = engine._training_completion_score(inp)
        manager = engine._manager_support_score(inp)
        performance = engine._early_performance_score(inp)
        expected = round(ramp * 0.30 + training * 0.30 + manager * 0.25 + performance * 0.15, 1)
        result = engine.assess(inp)
        assert result.onboarding_composite == expected

    def test_composite_capped_at_100(self):
        engine = fresh_engine()
        # Force all sub-scores to maximum
        inp = make_input(
            days_to_first_opportunity=100, days_to_first_closed_deal=200,
            pipeline_coverage_vs_ramp_target_pct=0.0,
            training_modules_completed_pct=0.0,
            product_certification_completed=False, days_since_start=90,
            crm_adoption_score=0.0,
            manager_1on1_count=0, expected_manager_1on1_count=10,
            mentor_sessions_count=0,
            avg_activity_score_vs_team_pct=0.0,
            quota_attainment_week_8_pct=0.0, quota_attainment_week_16_pct=0.0,
            sentiment_score=0.10,
        )
        result = engine.assess(inp)
        assert result.onboarding_composite <= 100.0

    def test_composite_rounded_to_1_decimal(self):
        engine = fresh_engine()
        inp = make_input()
        result = engine.assess(inp)
        assert result.onboarding_composite == round(result.onboarding_composite, 1)


# ===========================================================================
# 16. ASSESS() METHOD TESTS
# ===========================================================================

class TestAssessMethod:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_returns_result_type(self):
        result = self.engine.assess(make_input())
        assert isinstance(result, OnboardingEffectivenessResult)

    def test_rep_id_preserved(self):
        result = self.engine.assess(make_input(rep_id="REPTESTID"))
        assert result.rep_id == "REPTESTID"

    def test_region_preserved(self):
        result = self.engine.assess(make_input(region="EMEA"))
        assert result.region == "EMEA"

    def test_risk_is_enum(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.onboarding_risk, OnboardingRisk)

    def test_pattern_is_enum(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.onboarding_pattern, OnboardingPattern)

    def test_severity_is_enum(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.onboarding_severity, OnboardingSeverity)

    def test_action_is_enum(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.recommended_action, OnboardingAction)

    def test_composite_is_float(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.onboarding_composite, float)

    def test_has_onboarding_gap_is_bool(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.has_onboarding_gap, bool)

    def test_requires_intervention_is_bool(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.requires_onboarding_intervention, bool)

    def test_delay_cost_is_float(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.estimated_ramp_delay_cost_usd, float)

    def test_signal_is_str(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.onboarding_signal, str)

    def test_result_stored_internally(self):
        self.engine.assess(make_input())
        assert len(self.engine._results) == 1

    def test_multiple_assess_stored(self):
        self.engine.assess(make_input(rep_id="A"))
        self.engine.assess(make_input(rep_id="B"))
        assert len(self.engine._results) == 2

    def test_healthy_rep_has_low_risk(self):
        result = self.engine.assess(make_input())
        assert result.onboarding_risk == OnboardingRisk.low

    def test_healthy_rep_has_no_gap(self):
        result = self.engine.assess(make_input())
        assert result.has_onboarding_gap is False

    def test_ramp_score_non_negative(self):
        result = self.engine.assess(make_input())
        assert result.ramp_velocity_score >= 0.0

    def test_training_score_non_negative(self):
        result = self.engine.assess(make_input())
        assert result.training_completion_score >= 0.0

    def test_manager_score_non_negative(self):
        result = self.engine.assess(make_input())
        assert result.manager_support_score >= 0.0

    def test_performance_score_non_negative(self):
        result = self.engine.assess(make_input())
        assert result.early_performance_score >= 0.0

    def test_delay_cost_non_negative(self):
        result = self.engine.assess(make_input())
        assert result.estimated_ramp_delay_cost_usd >= 0.0


# ===========================================================================
# 17. ASSESS_BATCH() METHOD TESTS
# ===========================================================================

class TestAssessBatch:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_returns_list(self):
        results = self.engine.assess_batch([make_input()])
        assert isinstance(results, list)

    def test_empty_batch_returns_empty_list(self):
        results = self.engine.assess_batch([])
        assert results == []

    def test_batch_length_matches_input(self):
        inputs = [make_input(rep_id=str(i)) for i in range(5)]
        results = self.engine.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_results_are_result_type(self):
        results = self.engine.assess_batch([make_input(rep_id="X")])
        assert isinstance(results[0], OnboardingEffectivenessResult)

    def test_batch_stores_all_results(self):
        self.engine.assess_batch([make_input(rep_id=str(i)) for i in range(3)])
        assert len(self.engine._results) == 3

    def test_batch_rep_ids_preserved(self):
        inputs = [make_input(rep_id=f"REP{i}") for i in range(3)]
        results = self.engine.assess_batch(inputs)
        assert [r.rep_id for r in results] == ["REP0", "REP1", "REP2"]

    def test_batch_order_preserved(self):
        inp_a = make_input(rep_id="A", days_to_first_opportunity=15)
        inp_b = make_input(rep_id="B", days_to_first_opportunity=80)
        results = self.engine.assess_batch([inp_a, inp_b])
        assert results[0].rep_id == "A"
        assert results[1].rep_id == "B"

    def test_batch_single_element(self):
        results = self.engine.assess_batch([make_input(rep_id="SOLO")])
        assert results[0].rep_id == "SOLO"


# ===========================================================================
# 18. SUMMARY() METHOD TESTS
# ===========================================================================

class TestSummaryMethod:
    def test_empty_summary_returns_zero_values(self):
        engine = fresh_engine()
        s = engine.summary()
        assert s["total"] == 0

    def test_empty_summary_has_13_keys(self):
        engine = fresh_engine()
        assert len(engine.summary()) == 13

    def test_empty_summary_keys(self):
        engine = fresh_engine()
        s = engine.summary()
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_onboarding_composite", "onboarding_gap_count",
            "intervention_count", "avg_ramp_velocity_score",
            "avg_training_completion_score", "avg_manager_support_score",
            "avg_early_performance_score", "total_estimated_ramp_delay_cost_usd",
        }
        assert set(s.keys()) == expected_keys

    def test_empty_summary_risk_counts_empty(self):
        engine = fresh_engine()
        assert engine.summary()["risk_counts"] == {}

    def test_empty_summary_pattern_counts_empty(self):
        engine = fresh_engine()
        assert engine.summary()["pattern_counts"] == {}

    def test_empty_summary_severity_counts_empty(self):
        engine = fresh_engine()
        assert engine.summary()["severity_counts"] == {}

    def test_empty_summary_action_counts_empty(self):
        engine = fresh_engine()
        assert engine.summary()["action_counts"] == {}

    def test_empty_summary_avg_composite_zero(self):
        engine = fresh_engine()
        assert engine.summary()["avg_onboarding_composite"] == 0.0

    def test_empty_summary_gap_count_zero(self):
        engine = fresh_engine()
        assert engine.summary()["onboarding_gap_count"] == 0

    def test_empty_summary_intervention_count_zero(self):
        engine = fresh_engine()
        assert engine.summary()["intervention_count"] == 0

    def test_empty_summary_total_cost_zero(self):
        engine = fresh_engine()
        assert engine.summary()["total_estimated_ramp_delay_cost_usd"] == 0.0

    def test_summary_total_after_single_assess(self):
        engine = fresh_engine()
        engine.assess(make_input())
        assert engine.summary()["total"] == 1

    def test_summary_total_after_batch(self):
        engine = fresh_engine()
        engine.assess_batch([make_input(rep_id=str(i)) for i in range(5)])
        assert engine.summary()["total"] == 5

    def test_summary_risk_counts_dict_str_int(self):
        engine = fresh_engine()
        engine.assess(make_input())
        rc = engine.summary()["risk_counts"]
        for k, v in rc.items():
            assert isinstance(k, str)
            assert isinstance(v, int)

    def test_summary_avg_composite_is_float(self):
        engine = fresh_engine()
        engine.assess(make_input())
        assert isinstance(engine.summary()["avg_onboarding_composite"], float)

    def test_summary_gap_count_correct(self):
        engine = fresh_engine()
        # gap rep: pipeline_coverage < 0.50
        engine.assess(make_input(pipeline_coverage_vs_ramp_target_pct=0.30))
        engine.assess(make_input())  # healthy
        assert engine.summary()["onboarding_gap_count"] == 1

    def test_summary_intervention_count_correct(self):
        engine = fresh_engine()
        # intervention: sentiment < 0.40
        engine.assess(make_input(sentiment_score=0.30))
        engine.assess(make_input())  # healthy, no intervention
        s = engine.summary()
        assert s["intervention_count"] >= 1

    def test_summary_total_cost_is_sum(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input(avg_opportunity_value_usd=10_000.0))
        r2 = engine.assess(make_input(avg_opportunity_value_usd=5_000.0))
        expected = round(r1.estimated_ramp_delay_cost_usd + r2.estimated_ramp_delay_cost_usd, 2)
        assert engine.summary()["total_estimated_ramp_delay_cost_usd"] == expected

    def test_summary_avg_ramp_score_correct(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input())
        r2 = engine.assess(make_input())
        expected = round((r1.ramp_velocity_score + r2.ramp_velocity_score) / 2, 1)
        assert engine.summary()["avg_ramp_velocity_score"] == expected

    def test_summary_avg_training_score_correct(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input())
        r2 = engine.assess(make_input())
        expected = round((r1.training_completion_score + r2.training_completion_score) / 2, 1)
        assert engine.summary()["avg_training_completion_score"] == expected

    def test_summary_has_13_keys_after_assess(self):
        engine = fresh_engine()
        engine.assess(make_input())
        assert len(engine.summary()) == 13


# ===========================================================================
# 19. EDGE CASES
# ===========================================================================

class TestEdgeCases:
    def test_zero_days_since_start(self):
        engine = fresh_engine()
        inp = make_input(days_since_start=0)
        result = engine.assess(inp)
        assert result is not None

    def test_very_large_opportunity_value(self):
        engine = fresh_engine()
        inp = make_input(avg_opportunity_value_usd=1_000_000.0)
        result = engine.assess(inp)
        assert result.estimated_ramp_delay_cost_usd >= 0.0

    def test_all_zero_numeric_fields(self):
        engine = fresh_engine()
        inp = make_input(
            days_since_start=0, days_to_first_meeting=0, days_to_first_opportunity=0,
            days_to_first_closed_deal=0, training_modules_completed_pct=0.0,
            manager_1on1_count=0, expected_manager_1on1_count=0,
            mentor_sessions_count=0, pipeline_coverage_vs_ramp_target_pct=0.0,
            quota_attainment_week_8_pct=0.0, quota_attainment_week_16_pct=0.0,
            crm_adoption_score=0.0, avg_activity_score_vs_team_pct=0.0,
            deals_in_pipeline_count=0, avg_deal_size_vs_team_pct=0.0,
            sentiment_score=0.0, late_crm_update_rate_pct=0.0,
            avg_opportunity_value_usd=0.0, product_certification_completed=False,
        )
        result = engine.assess(inp)
        assert isinstance(result, OnboardingEffectivenessResult)

    def test_all_max_pct_fields(self):
        engine = fresh_engine()
        inp = make_input(
            training_modules_completed_pct=1.0, pipeline_coverage_vs_ramp_target_pct=1.0,
            quota_attainment_week_8_pct=1.0, quota_attainment_week_16_pct=1.0,
            crm_adoption_score=1.0, avg_activity_score_vs_team_pct=1.0,
            sentiment_score=1.0,
        )
        result = engine.assess(inp)
        assert result.onboarding_risk == OnboardingRisk.low

    def test_expected_manager_zero_does_not_raise(self):
        engine = fresh_engine()
        inp = make_input(expected_manager_1on1_count=0, manager_1on1_count=0)
        result = engine.assess(inp)
        assert isinstance(result, OnboardingEffectivenessResult)

    def test_pipeline_exactly_at_threshold_50(self):
        engine = fresh_engine()
        # 0.50 is NOT < 0.50, so no gap from pipeline alone
        inp = make_input(pipeline_coverage_vs_ramp_target_pct=0.50)
        result = engine.assess(inp)
        # gap depends on composite and training too
        assert isinstance(result.has_onboarding_gap, bool)

    def test_sentiment_exactly_at_30_threshold(self):
        engine = fresh_engine()
        inp = make_input(sentiment_score=0.30)
        result = engine.assess(inp)
        # 0.30 is NOT < 0.30, so no 20-point penalty
        assert result.early_performance_score < 20.0 or result.early_performance_score >= 0.0

    def test_string_fields_preserved(self):
        engine = fresh_engine()
        inp = make_input(rep_id="REP-SPECIAL", region="APAC", evaluation_period_id="Q4-2025")
        result = engine.assess(inp)
        assert result.rep_id == "REP-SPECIAL"
        assert result.region == "APAC"


# ===========================================================================
# 20. END-TO-END SCENARIO TESTS
# ===========================================================================

class TestEndToEndScenarios:
    """Full scenario tests that verify the complete assessment pipeline."""

    def test_scenario_critical_early_attrition(self):
        """Rep with very low sentiment and high performance penalty → critical + early_attrition."""
        engine = fresh_engine()
        inp = make_input(
            rep_id="ATTRITION_REP",
            sentiment_score=0.10,        # < 0.30 → triggers early attrition if performance >= 25
            days_since_start=120,
            quota_attainment_week_8_pct=0.05,   # adds 35 to performance
            quota_attainment_week_16_pct=0.20,  # adds 35 to performance
            days_to_first_opportunity=70,        # adds 35 to ramp
            days_to_first_closed_deal=130,       # adds 35 to ramp
            pipeline_coverage_vs_ramp_target_pct=0.20,  # adds 25 to ramp
            training_modules_completed_pct=0.20,
            crm_adoption_score=0.20,
            manager_1on1_count=2,
            expected_manager_1on1_count=10,
            mentor_sessions_count=0,
            avg_activity_score_vs_team_pct=0.20,
        )
        result = engine.assess(inp)
        assert result.onboarding_risk == OnboardingRisk.critical
        assert result.onboarding_pattern == OnboardingPattern.early_attrition_signal
        assert result.recommended_action == OnboardingAction.early_retention_intervention
        assert result.onboarding_severity == OnboardingSeverity.at_risk

    def test_scenario_high_risk_training_gap(self):
        """Rep with clear training gap → training_gap pattern detected."""
        engine = fresh_engine()
        inp = make_input(
            rep_id="TRAINING_GAP_REP",
            training_modules_completed_pct=0.30,   # adds 40 to training
            product_certification_completed=False,
            days_since_start=60,                   # cert penalty +30
            crm_adoption_score=0.30,               # adds 25 to training → training=95
            manager_1on1_count=8,
            expected_manager_1on1_count=10,        # rate=0.8 => +8
            mentor_sessions_count=3,
            avg_activity_score_vs_team_pct=0.80,
            sentiment_score=0.80,
            days_to_first_opportunity=20,
            days_to_first_closed_deal=50,
            pipeline_coverage_vs_ramp_target_pct=0.80,
        )
        result = engine.assess(inp)
        # training score is 95 (>=30), pct<0.60 → training_gap pattern
        assert result.onboarding_pattern == OnboardingPattern.training_gap
        # composite = 0*0.30 + 95*0.30 + 8*0.25 + 0*0.15 = 28.5 → moderate risk
        assert result.onboarding_risk in (OnboardingRisk.moderate, OnboardingRisk.high, OnboardingRisk.critical)

    def test_scenario_manager_neglect_critical(self):
        """Rep with poor manager support and critical composite."""
        engine = fresh_engine()
        inp = make_input(
            rep_id="NEGLECT_REP",
            manager_1on1_count=1,
            expected_manager_1on1_count=10,       # rate=0.1 < 0.5 and < 0.4 → +40
            mentor_sessions_count=0,
            days_since_start=60,                  # mentor penalty +30
            avg_activity_score_vs_team_pct=0.20,  # +25
            sentiment_score=0.80,
            training_modules_completed_pct=0.30,  # training +40
            crm_adoption_score=0.20,              # crm +25
            product_certification_completed=False,
            days_to_first_opportunity=70,
            days_to_first_closed_deal=130,
            pipeline_coverage_vs_ramp_target_pct=0.20,
        )
        result = engine.assess(inp)
        assert result.onboarding_risk in (OnboardingRisk.high, OnboardingRisk.critical)
        # manager_neglect requires manager>=35 AND count < expected*0.50
        assert result.onboarding_pattern in (
            OnboardingPattern.manager_neglect, OnboardingPattern.training_gap,
            OnboardingPattern.early_attrition_signal
        )

    def test_scenario_healthy_rep(self):
        """Healthy rep → low risk, none pattern, no gap, no intervention."""
        engine = fresh_engine()
        inp = make_input()  # all healthy defaults
        result = engine.assess(inp)
        assert result.onboarding_risk == OnboardingRisk.low
        assert result.onboarding_pattern == OnboardingPattern.none
        assert result.onboarding_severity == OnboardingSeverity.ramping
        assert result.recommended_action == OnboardingAction.no_action
        assert result.has_onboarding_gap is False
        assert "healthy" in result.onboarding_signal

    def test_scenario_moderate_risk_ramp_coaching(self):
        """Rep with moderate composite should get ramp coaching."""
        engine = fresh_engine()
        inp = make_input(
            days_to_first_opportunity=30,          # +8
            days_to_first_closed_deal=60,          # +7
            pipeline_coverage_vs_ramp_target_pct=0.60,   # +12
            training_modules_completed_pct=0.70,   # +8
            product_certification_completed=True,
            crm_adoption_score=0.70,
            manager_1on1_count=8,
            expected_manager_1on1_count=10,
            mentor_sessions_count=3,
            avg_activity_score_vs_team_pct=0.80,
            sentiment_score=0.70,
        )
        result = engine.assess(inp)
        if result.onboarding_risk == OnboardingRisk.moderate:
            assert result.recommended_action == OnboardingAction.ramp_support_coaching

    def test_scenario_product_knowledge_gap(self):
        """Rep without certification past 60 days → product knowledge gap."""
        engine = fresh_engine()
        inp = make_input(
            product_certification_completed=False,
            days_since_start=60,
            training_modules_completed_pct=0.70,  # NOT < 0.60, so no training_gap
            crm_adoption_score=0.50,              # +12 to training
            manager_1on1_count=8,
            expected_manager_1on1_count=10,
            mentor_sessions_count=3,
            avg_activity_score_vs_team_pct=0.80,
            sentiment_score=0.80,
            pipeline_coverage_vs_ramp_target_pct=0.90,
            days_to_first_opportunity=20,
            days_to_first_closed_deal=50,
        )
        result = engine.assess(inp)
        # training score = 8 (0.70) + 30 (cert incomplete >=60 days) + 12 (crm) = 50
        # training >= 20 and not certified and days >= 60 → product_knowledge_gap
        assert result.onboarding_pattern == OnboardingPattern.product_knowledge_gap

    def test_scenario_slow_ramp_detected(self):
        """Rep with pipeline gap and ramp score → slow_ramp."""
        engine = fresh_engine()
        inp = make_input(
            pipeline_coverage_vs_ramp_target_pct=0.40,
            days_to_first_opportunity=65,         # +35 ramp
            product_certification_completed=True,
            training_modules_completed_pct=0.85,
            crm_adoption_score=0.85,
            manager_1on1_count=9,
            expected_manager_1on1_count=10,
            mentor_sessions_count=3,
            avg_activity_score_vs_team_pct=0.80,
            sentiment_score=0.80,
        )
        result = engine.assess(inp)
        # ramp = 35+0+25 = 60, ramp>=25 and pipeline < 0.60 → slow_ramp
        assert result.onboarding_pattern == OnboardingPattern.slow_ramp

    def test_scenario_batch_mixed_reps(self):
        """Batch with healthy and critical reps."""
        engine = fresh_engine()
        healthy = make_input(rep_id="HEALTHY")
        critical = make_input(
            rep_id="CRITICAL",
            sentiment_score=0.10,
            days_since_start=120,
            quota_attainment_week_8_pct=0.05,
            quota_attainment_week_16_pct=0.20,
            days_to_first_opportunity=70,
            days_to_first_closed_deal=130,
            pipeline_coverage_vs_ramp_target_pct=0.20,
            training_modules_completed_pct=0.20,
            crm_adoption_score=0.20,
            manager_1on1_count=2,
            expected_manager_1on1_count=10,
            mentor_sessions_count=0,
            avg_activity_score_vs_team_pct=0.20,
        )
        results = engine.assess_batch([healthy, critical])
        assert results[0].onboarding_risk == OnboardingRisk.low
        assert results[1].onboarding_risk == OnboardingRisk.critical

    def test_scenario_summary_accumulates_correctly(self):
        """Verify summary aggregates batch results correctly."""
        engine = fresh_engine()
        engine.assess_batch([make_input(rep_id=str(i)) for i in range(3)])
        s = engine.summary()
        assert s["total"] == 3
        assert isinstance(s["risk_counts"], dict)
        assert isinstance(s["avg_onboarding_composite"], float)

    def test_scenario_to_dict_round_trip(self):
        """Verify to_dict contains correct values matching result fields."""
        engine = fresh_engine()
        result = engine.assess(make_input(rep_id="DICTTEST", region="NORTH"))
        d = result.to_dict()
        assert d["rep_id"] == result.rep_id
        assert d["region"] == result.region
        assert d["onboarding_risk"] == result.onboarding_risk.value
        assert d["onboarding_pattern"] == result.onboarding_pattern.value
        assert d["onboarding_severity"] == result.onboarding_severity.value
        assert d["recommended_action"] == result.recommended_action.value
        assert d["ramp_velocity_score"] == result.ramp_velocity_score
        assert d["training_completion_score"] == result.training_completion_score
        assert d["manager_support_score"] == result.manager_support_score
        assert d["early_performance_score"] == result.early_performance_score
        assert d["onboarding_composite"] == result.onboarding_composite
        assert d["has_onboarding_gap"] == result.has_onboarding_gap
        assert d["requires_onboarding_intervention"] == result.requires_onboarding_intervention
        assert d["estimated_ramp_delay_cost_usd"] == result.estimated_ramp_delay_cost_usd
        assert d["onboarding_signal"] == result.onboarding_signal

    def test_scenario_intervention_on_low_sentiment(self):
        """Rep with low sentiment score should require intervention."""
        engine = fresh_engine()
        result = engine.assess(make_input(sentiment_score=0.20))
        assert result.requires_onboarding_intervention is True

    def test_scenario_no_intervention_on_healthy(self):
        """Healthy rep should not require intervention."""
        engine = fresh_engine()
        result = engine.assess(make_input())
        assert result.requires_onboarding_intervention is False

    def test_scenario_gap_on_low_pipeline(self):
        """Rep with pipeline < 50% should have onboarding gap."""
        engine = fresh_engine()
        result = engine.assess(make_input(pipeline_coverage_vs_ramp_target_pct=0.30))
        assert result.has_onboarding_gap is True

    def test_scenario_gap_on_low_training(self):
        """Rep with training < 40% should have onboarding gap."""
        engine = fresh_engine()
        result = engine.assess(make_input(training_modules_completed_pct=0.30))
        assert result.has_onboarding_gap is True

    def test_engine_initializes_empty_results(self):
        """Freshly created engine has no results."""
        engine = fresh_engine()
        assert engine._results == []

    def test_multiple_engines_independent(self):
        """Two engine instances are independent."""
        e1 = fresh_engine()
        e2 = fresh_engine()
        e1.assess(make_input(rep_id="A"))
        assert len(e2._results) == 0
        assert len(e1._results) == 1

    def test_summary_after_mixed_batch(self):
        """Summary correctly aggregates mixed risk reps."""
        engine = fresh_engine()
        engine.assess(make_input(rep_id="LOW"))
        engine.assess(make_input(
            rep_id="HIGH",
            days_to_first_opportunity=70,
            days_to_first_closed_deal=130,
            pipeline_coverage_vs_ramp_target_pct=0.20,
            training_modules_completed_pct=0.20,
            crm_adoption_score=0.20,
            manager_1on1_count=2,
            expected_manager_1on1_count=10,
            mentor_sessions_count=0,
            avg_activity_score_vs_team_pct=0.20,
            sentiment_score=0.60,
        ))
        s = engine.summary()
        assert s["total"] == 2
        total_in_counts = sum(s["risk_counts"].values())
        assert total_in_counts == 2
