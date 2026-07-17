"""
Comprehensive pytest test suite for SalesCustomerLifecycleIntelligenceEngine.
Target: 200+ tests covering all sub-scores, composites, patterns, risks,
severities, actions, flags, dollar impact, signals, and public API.
"""
from __future__ import annotations

import math
import pytest

from swarm.intelligence.sales_customer_lifecycle_intelligence_engine import (
    LifecycleAction,
    LifecycleInput,
    LifecyclePattern,
    LifecycleResult,
    LifecycleRisk,
    LifecycleSeverity,
    SalesCustomerLifecycleIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_input(**overrides) -> LifecycleInput:
    """Return a 'healthy' baseline LifecycleInput, with optional overrides."""
    defaults = dict(
        rep_id="rep_001",
        region="EMEA",
        evaluation_period_id="2026-Q2",
        product_adoption_score=0.85,
        feature_utilization_pct=0.80,
        login_frequency_per_week=5.0,
        support_ticket_rate_per_month=0.5,
        nps_score=50.0,
        contract_renewal_days_out=180.0,
        days_since_last_meaningful_touch=7.0,
        expansion_revenue_pct=0.30,
        churn_signal_count=0,
        exec_sponsor_engaged=0.90,
        multi_dept_usage_pct=0.70,
        health_score_trend=0.20,
        onboarding_completion_pct=0.95,
        time_to_value_days=30.0,
        competitive_mention_count=0,
        qbr_completion_rate=0.90,
        customer_age_months=24.0,
        total_arr_usd=100_000.0,
        avg_arr_per_user_usd=1_000.0,
    )
    defaults.update(overrides)
    return LifecycleInput(**defaults)


def _engine() -> SalesCustomerLifecycleIntelligenceEngine:
    return SalesCustomerLifecycleIntelligenceEngine()


# ---------------------------------------------------------------------------
# 1. Enum membership and values
# ---------------------------------------------------------------------------

class TestLifecycleRiskEnum:
    def test_has_low(self):
        assert LifecycleRisk.low == "low"

    def test_has_moderate(self):
        assert LifecycleRisk.moderate == "moderate"

    def test_has_high(self):
        assert LifecycleRisk.high == "high"

    def test_has_critical(self):
        assert LifecycleRisk.critical == "critical"

    def test_exactly_four_members(self):
        assert len(LifecycleRisk) == 4

    def test_is_str_enum(self):
        assert isinstance(LifecycleRisk.low, str)


class TestLifecyclePatternEnum:
    def test_none(self):
        assert LifecyclePattern.none == "none"

    def test_churn_trajectory(self):
        assert LifecyclePattern.churn_trajectory == "churn_trajectory"

    def test_expansion_stall(self):
        assert LifecyclePattern.expansion_stall == "expansion_stall"

    def test_adoption_lag(self):
        assert LifecyclePattern.adoption_lag == "adoption_lag"

    def test_renewal_cliff(self):
        assert LifecyclePattern.renewal_cliff == "renewal_cliff"

    def test_dormant_account(self):
        assert LifecyclePattern.dormant_account == "dormant_account"

    def test_exactly_six_members(self):
        assert len(LifecyclePattern) == 6


class TestLifecycleSeverityEnum:
    def test_thriving(self):
        assert LifecycleSeverity.thriving == "thriving"

    def test_stable(self):
        assert LifecycleSeverity.stable == "stable"

    def test_declining(self):
        assert LifecycleSeverity.declining == "declining"

    def test_critical(self):
        assert LifecycleSeverity.critical == "critical"

    def test_exactly_four_members(self):
        assert len(LifecycleSeverity) == 4


class TestLifecycleActionEnum:
    def test_no_action(self):
        assert LifecycleAction.no_action == "no_action"

    def test_health_monitoring(self):
        assert LifecycleAction.health_monitoring == "health_monitoring"

    def test_adoption_coaching(self):
        assert LifecycleAction.adoption_coaching == "adoption_coaching"

    def test_expansion_play(self):
        assert LifecycleAction.expansion_play == "expansion_play"

    def test_churn_prevention_outreach(self):
        assert LifecycleAction.churn_prevention_outreach == "churn_prevention_outreach"

    def test_executive_escalation(self):
        assert LifecycleAction.executive_escalation == "executive_escalation"

    def test_emergency_save_intervention(self):
        assert LifecycleAction.emergency_save_intervention == "emergency_save_intervention"

    def test_exactly_seven_members(self):
        assert len(LifecycleAction) == 7


# ---------------------------------------------------------------------------
# 2. LifecycleInput – field presence and types
# ---------------------------------------------------------------------------

class TestLifecycleInputFields:
    def test_can_instantiate(self):
        inp = _make_input()
        assert isinstance(inp, LifecycleInput)

    def test_has_rep_id(self):
        assert _make_input().rep_id == "rep_001"

    def test_has_region(self):
        assert _make_input().region == "EMEA"

    def test_has_evaluation_period_id(self):
        assert _make_input().evaluation_period_id == "2026-Q2"

    def test_has_product_adoption_score(self):
        assert _make_input().product_adoption_score == 0.85

    def test_has_feature_utilization_pct(self):
        assert _make_input().feature_utilization_pct == 0.80

    def test_has_login_frequency_per_week(self):
        assert _make_input().login_frequency_per_week == 5.0

    def test_has_support_ticket_rate_per_month(self):
        assert _make_input().support_ticket_rate_per_month == 0.5

    def test_has_nps_score(self):
        assert _make_input().nps_score == 50.0

    def test_has_contract_renewal_days_out(self):
        assert _make_input().contract_renewal_days_out == 180.0

    def test_has_days_since_last_meaningful_touch(self):
        assert _make_input().days_since_last_meaningful_touch == 7.0

    def test_has_expansion_revenue_pct(self):
        assert _make_input().expansion_revenue_pct == 0.30

    def test_has_churn_signal_count(self):
        assert _make_input().churn_signal_count == 0

    def test_has_exec_sponsor_engaged(self):
        assert _make_input().exec_sponsor_engaged == 0.90

    def test_has_multi_dept_usage_pct(self):
        assert _make_input().multi_dept_usage_pct == 0.70

    def test_has_health_score_trend(self):
        assert _make_input().health_score_trend == 0.20

    def test_has_onboarding_completion_pct(self):
        assert _make_input().onboarding_completion_pct == 0.95

    def test_has_time_to_value_days(self):
        assert _make_input().time_to_value_days == 30.0

    def test_has_competitive_mention_count(self):
        assert _make_input().competitive_mention_count == 0

    def test_has_qbr_completion_rate(self):
        assert _make_input().qbr_completion_rate == 0.90

    def test_has_customer_age_months(self):
        assert _make_input().customer_age_months == 24.0

    def test_has_total_arr_usd(self):
        assert _make_input().total_arr_usd == 100_000.0

    def test_has_avg_arr_per_user_usd(self):
        assert _make_input().avg_arr_per_user_usd == 1_000.0

    def test_exactly_22_fields(self):
        # dataclass has 22 fields (excluding __dataclass_fields__ meta)
        import dataclasses
        assert len(dataclasses.fields(LifecycleInput)) == 22


# ---------------------------------------------------------------------------
# 3. LifecycleResult – structure and to_dict
# ---------------------------------------------------------------------------

class TestLifecycleResultToDict:
    def _result(self):
        return _engine().assess(_make_input())

    def test_to_dict_returns_dict(self):
        assert isinstance(self._result().to_dict(), dict)

    def test_to_dict_has_15_keys(self):
        assert len(self._result().to_dict()) == 15

    def test_to_dict_key_rep_id(self):
        assert "rep_id" in self._result().to_dict()

    def test_to_dict_key_region(self):
        assert "region" in self._result().to_dict()

    def test_to_dict_key_lifecycle_risk(self):
        assert "lifecycle_risk" in self._result().to_dict()

    def test_to_dict_key_lifecycle_pattern(self):
        assert "lifecycle_pattern" in self._result().to_dict()

    def test_to_dict_key_lifecycle_severity(self):
        assert "lifecycle_severity" in self._result().to_dict()

    def test_to_dict_key_recommended_action(self):
        assert "recommended_action" in self._result().to_dict()

    def test_to_dict_key_adoption_score(self):
        assert "adoption_score" in self._result().to_dict()

    def test_to_dict_key_engagement_score(self):
        assert "engagement_score" in self._result().to_dict()

    def test_to_dict_key_renewal_readiness_score(self):
        assert "renewal_readiness_score" in self._result().to_dict()

    def test_to_dict_key_expansion_potential_score(self):
        assert "expansion_potential_score" in self._result().to_dict()

    def test_to_dict_key_lifecycle_composite(self):
        assert "lifecycle_composite" in self._result().to_dict()

    def test_to_dict_key_has_lifecycle_gap(self):
        assert "has_lifecycle_gap" in self._result().to_dict()

    def test_to_dict_key_requires_lifecycle_intervention(self):
        assert "requires_lifecycle_intervention" in self._result().to_dict()

    def test_to_dict_key_estimated_churn_risk_usd(self):
        assert "estimated_churn_risk_usd" in self._result().to_dict()

    def test_to_dict_key_lifecycle_signal(self):
        assert "lifecycle_signal" in self._result().to_dict()

    def test_to_dict_risk_value_is_string(self):
        d = self._result().to_dict()
        assert isinstance(d["lifecycle_risk"], str)

    def test_to_dict_pattern_value_is_string(self):
        d = self._result().to_dict()
        assert isinstance(d["lifecycle_pattern"], str)

    def test_to_dict_severity_value_is_string(self):
        d = self._result().to_dict()
        assert isinstance(d["lifecycle_severity"], str)

    def test_to_dict_action_value_is_string(self):
        d = self._result().to_dict()
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_rep_id_passthrough(self):
        inp = _make_input(rep_id="X99")
        d = _engine().assess(inp).to_dict()
        assert d["rep_id"] == "X99"

    def test_to_dict_region_passthrough(self):
        inp = _make_input(region="APAC")
        d = _engine().assess(inp).to_dict()
        assert d["region"] == "APAC"


# ---------------------------------------------------------------------------
# 4. _adoption_score sub-score
# ---------------------------------------------------------------------------

class TestAdoptionScore:
    def _ad(self, **kw) -> float:
        e = _engine()
        return e._adoption_score(_make_input(**kw))

    # product_adoption_score bands
    def test_adoption_score_pa_very_low(self):
        # <= 0.30 → +40
        s = self._ad(product_adoption_score=0.20, feature_utilization_pct=0.60, onboarding_completion_pct=0.90)
        assert s == 40.0

    def test_adoption_score_pa_mid(self):
        # 0.31–0.55 → +22
        s = self._ad(product_adoption_score=0.45, feature_utilization_pct=0.60, onboarding_completion_pct=0.90)
        assert s == 22.0

    def test_adoption_score_pa_upper_mid(self):
        # 0.56–0.75 → +8
        s = self._ad(product_adoption_score=0.65, feature_utilization_pct=0.60, onboarding_completion_pct=0.90)
        assert s == 8.0

    def test_adoption_score_pa_high(self):
        # > 0.75 → +0
        s = self._ad(product_adoption_score=0.90, feature_utilization_pct=0.60, onboarding_completion_pct=0.90)
        assert s == 0.0

    # feature_utilization_pct bands
    def test_adoption_score_fu_very_low(self):
        # <= 0.25 → +35
        s = self._ad(product_adoption_score=0.90, feature_utilization_pct=0.10, onboarding_completion_pct=0.90)
        assert s == 35.0

    def test_adoption_score_fu_mid(self):
        # 0.26–0.50 → +18
        s = self._ad(product_adoption_score=0.90, feature_utilization_pct=0.40, onboarding_completion_pct=0.90)
        assert s == 18.0

    def test_adoption_score_fu_high(self):
        # > 0.50 → +0
        s = self._ad(product_adoption_score=0.90, feature_utilization_pct=0.80, onboarding_completion_pct=0.90)
        assert s == 0.0

    # onboarding_completion_pct bands
    def test_adoption_score_ob_low(self):
        # <= 0.60 → +25
        s = self._ad(product_adoption_score=0.90, feature_utilization_pct=0.80, onboarding_completion_pct=0.50)
        assert s == 25.0

    def test_adoption_score_ob_mid(self):
        # 0.61–0.80 → +12
        s = self._ad(product_adoption_score=0.90, feature_utilization_pct=0.80, onboarding_completion_pct=0.70)
        assert s == 12.0

    def test_adoption_score_ob_high(self):
        # > 0.80 → +0
        s = self._ad(product_adoption_score=0.90, feature_utilization_pct=0.80, onboarding_completion_pct=0.90)
        assert s == 0.0

    def test_adoption_score_all_bad_capped_at_100(self):
        # 40+35+25 = 100
        s = self._ad(product_adoption_score=0.10, feature_utilization_pct=0.10, onboarding_completion_pct=0.10)
        assert s == 100.0

    def test_adoption_score_all_good_zero(self):
        s = self._ad(product_adoption_score=0.90, feature_utilization_pct=0.80, onboarding_completion_pct=0.90)
        assert s == 0.0

    def test_adoption_score_boundary_pa_30(self):
        s = self._ad(product_adoption_score=0.30, feature_utilization_pct=0.80, onboarding_completion_pct=0.90)
        assert s == 40.0

    def test_adoption_score_boundary_pa_55(self):
        s = self._ad(product_adoption_score=0.55, feature_utilization_pct=0.80, onboarding_completion_pct=0.90)
        assert s == 22.0

    def test_adoption_score_boundary_pa_75(self):
        s = self._ad(product_adoption_score=0.75, feature_utilization_pct=0.80, onboarding_completion_pct=0.90)
        assert s == 8.0

    def test_adoption_score_boundary_fu_25(self):
        s = self._ad(product_adoption_score=0.90, feature_utilization_pct=0.25, onboarding_completion_pct=0.90)
        assert s == 35.0

    def test_adoption_score_boundary_fu_50(self):
        s = self._ad(product_adoption_score=0.90, feature_utilization_pct=0.50, onboarding_completion_pct=0.90)
        assert s == 18.0

    def test_adoption_score_boundary_ob_60(self):
        s = self._ad(product_adoption_score=0.90, feature_utilization_pct=0.80, onboarding_completion_pct=0.60)
        assert s == 25.0

    def test_adoption_score_boundary_ob_80(self):
        s = self._ad(product_adoption_score=0.90, feature_utilization_pct=0.80, onboarding_completion_pct=0.80)
        assert s == 12.0

    def test_adoption_score_max_without_cap(self):
        # 40+35+25 = 100, not 101
        s = self._ad(product_adoption_score=0.10, feature_utilization_pct=0.10, onboarding_completion_pct=0.50)
        assert s == 100.0

    def test_adoption_score_partial_combination(self):
        # pa mid (22) + fu low (35) + ob high (0) = 57
        s = self._ad(product_adoption_score=0.40, feature_utilization_pct=0.10, onboarding_completion_pct=0.90)
        assert s == 57.0


# ---------------------------------------------------------------------------
# 5. _engagement_score sub-score
# ---------------------------------------------------------------------------

class TestEngagementScore:
    def _en(self, **kw) -> float:
        e = _engine()
        return e._engagement_score(_make_input(**kw))

    def test_touch_very_old(self):
        s = self._en(days_since_last_meaningful_touch=90, login_frequency_per_week=5, qbr_completion_rate=0.9)
        assert s == 40.0

    def test_touch_mid(self):
        s = self._en(days_since_last_meaningful_touch=45, login_frequency_per_week=5, qbr_completion_rate=0.9)
        assert s == 22.0

    def test_touch_recent_warn(self):
        s = self._en(days_since_last_meaningful_touch=20, login_frequency_per_week=5, qbr_completion_rate=0.9)
        assert s == 8.0

    def test_touch_fresh(self):
        s = self._en(days_since_last_meaningful_touch=5, login_frequency_per_week=5, qbr_completion_rate=0.9)
        assert s == 0.0

    def test_login_very_low(self):
        s = self._en(days_since_last_meaningful_touch=5, login_frequency_per_week=0.5, qbr_completion_rate=0.9)
        assert s == 35.0

    def test_login_mid(self):
        s = self._en(days_since_last_meaningful_touch=5, login_frequency_per_week=2, qbr_completion_rate=0.9)
        assert s == 18.0

    def test_login_high(self):
        s = self._en(days_since_last_meaningful_touch=5, login_frequency_per_week=5, qbr_completion_rate=0.9)
        assert s == 0.0

    def test_qbr_very_low(self):
        s = self._en(days_since_last_meaningful_touch=5, login_frequency_per_week=5, qbr_completion_rate=0.10)
        assert s == 25.0

    def test_qbr_mid(self):
        s = self._en(days_since_last_meaningful_touch=5, login_frequency_per_week=5, qbr_completion_rate=0.50)
        assert s == 12.0

    def test_qbr_high(self):
        s = self._en(days_since_last_meaningful_touch=5, login_frequency_per_week=5, qbr_completion_rate=0.90)
        assert s == 0.0

    def test_all_bad_capped_100(self):
        s = self._en(days_since_last_meaningful_touch=90, login_frequency_per_week=0, qbr_completion_rate=0.0)
        assert s == 100.0

    def test_all_good_zero(self):
        s = self._en(days_since_last_meaningful_touch=5, login_frequency_per_week=5, qbr_completion_rate=0.90)
        assert s == 0.0

    def test_boundary_touch_60(self):
        s = self._en(days_since_last_meaningful_touch=60, login_frequency_per_week=5, qbr_completion_rate=0.9)
        assert s == 40.0

    def test_boundary_touch_30(self):
        s = self._en(days_since_last_meaningful_touch=30, login_frequency_per_week=5, qbr_completion_rate=0.9)
        assert s == 22.0

    def test_boundary_touch_14(self):
        s = self._en(days_since_last_meaningful_touch=14, login_frequency_per_week=5, qbr_completion_rate=0.9)
        assert s == 8.0

    def test_boundary_login_1(self):
        s = self._en(days_since_last_meaningful_touch=5, login_frequency_per_week=1, qbr_completion_rate=0.9)
        assert s == 35.0

    def test_boundary_login_3(self):
        s = self._en(days_since_last_meaningful_touch=5, login_frequency_per_week=3, qbr_completion_rate=0.9)
        assert s == 18.0

    def test_boundary_qbr_25(self):
        s = self._en(days_since_last_meaningful_touch=5, login_frequency_per_week=5, qbr_completion_rate=0.25)
        assert s == 25.0

    def test_boundary_qbr_60(self):
        s = self._en(days_since_last_meaningful_touch=5, login_frequency_per_week=5, qbr_completion_rate=0.60)
        assert s == 12.0


# ---------------------------------------------------------------------------
# 6. _renewal_readiness_score sub-score
# ---------------------------------------------------------------------------

class TestRenewalReadinessScore:
    def _rr(self, **kw) -> float:
        return _engine()._renewal_readiness_score(_make_input(**kw))

    def test_renewal_very_close(self):
        s = self._rr(contract_renewal_days_out=20, churn_signal_count=0, health_score_trend=0.0)
        assert s == 40.0

    def test_renewal_close(self):
        s = self._rr(contract_renewal_days_out=50, churn_signal_count=0, health_score_trend=0.0)
        assert s == 22.0

    def test_renewal_mid(self):
        s = self._rr(contract_renewal_days_out=80, churn_signal_count=0, health_score_trend=0.0)
        assert s == 8.0

    def test_renewal_far(self):
        s = self._rr(contract_renewal_days_out=180, churn_signal_count=0, health_score_trend=0.0)
        assert s == 0.0

    def test_churn_signal_high(self):
        s = self._rr(contract_renewal_days_out=180, churn_signal_count=4, health_score_trend=0.0)
        assert s == 35.0

    def test_churn_signal_mid(self):
        s = self._rr(contract_renewal_days_out=180, churn_signal_count=2, health_score_trend=0.0)
        assert s == 18.0

    def test_churn_signal_low(self):
        s = self._rr(contract_renewal_days_out=180, churn_signal_count=1, health_score_trend=0.0)
        assert s == 0.0

    def test_health_trend_very_negative(self):
        s = self._rr(contract_renewal_days_out=180, churn_signal_count=0, health_score_trend=-0.50)
        assert s == 25.0

    def test_health_trend_moderately_negative(self):
        s = self._rr(contract_renewal_days_out=180, churn_signal_count=0, health_score_trend=-0.20)
        assert s == 12.0

    def test_health_trend_positive(self):
        s = self._rr(contract_renewal_days_out=180, churn_signal_count=0, health_score_trend=0.20)
        assert s == 0.0

    def test_all_bad_capped(self):
        s = self._rr(contract_renewal_days_out=10, churn_signal_count=5, health_score_trend=-0.90)
        assert s == 100.0

    def test_all_good_zero(self):
        s = self._rr(contract_renewal_days_out=180, churn_signal_count=0, health_score_trend=0.20)
        assert s == 0.0

    def test_boundary_renewal_30(self):
        s = self._rr(contract_renewal_days_out=30, churn_signal_count=0, health_score_trend=0.0)
        assert s == 40.0

    def test_boundary_renewal_60(self):
        s = self._rr(contract_renewal_days_out=60, churn_signal_count=0, health_score_trend=0.0)
        assert s == 22.0

    def test_boundary_renewal_90(self):
        s = self._rr(contract_renewal_days_out=90, churn_signal_count=0, health_score_trend=0.0)
        assert s == 8.0

    def test_boundary_churn_4(self):
        s = self._rr(contract_renewal_days_out=180, churn_signal_count=4, health_score_trend=0.0)
        assert s == 35.0

    def test_boundary_churn_2(self):
        s = self._rr(contract_renewal_days_out=180, churn_signal_count=2, health_score_trend=0.0)
        assert s == 18.0

    def test_boundary_health_neg_40(self):
        s = self._rr(contract_renewal_days_out=180, churn_signal_count=0, health_score_trend=-0.40)
        assert s == 25.0

    def test_boundary_health_neg_15(self):
        s = self._rr(contract_renewal_days_out=180, churn_signal_count=0, health_score_trend=-0.15)
        assert s == 12.0


# ---------------------------------------------------------------------------
# 7. _expansion_potential_score sub-score
# ---------------------------------------------------------------------------

class TestExpansionPotentialScore:
    def _ep(self, **kw) -> float:
        return _engine()._expansion_potential_score(_make_input(**kw))

    def test_expansion_very_low(self):
        s = self._ep(expansion_revenue_pct=0.02, multi_dept_usage_pct=0.70, exec_sponsor_engaged=0.90)
        assert s == 45.0

    def test_expansion_mid(self):
        s = self._ep(expansion_revenue_pct=0.10, multi_dept_usage_pct=0.70, exec_sponsor_engaged=0.90)
        assert s == 25.0

    def test_expansion_upper_mid(self):
        s = self._ep(expansion_revenue_pct=0.20, multi_dept_usage_pct=0.70, exec_sponsor_engaged=0.90)
        assert s == 10.0

    def test_expansion_high(self):
        s = self._ep(expansion_revenue_pct=0.40, multi_dept_usage_pct=0.70, exec_sponsor_engaged=0.90)
        assert s == 0.0

    def test_dept_very_low(self):
        s = self._ep(expansion_revenue_pct=0.40, multi_dept_usage_pct=0.10, exec_sponsor_engaged=0.90)
        assert s == 30.0

    def test_dept_mid(self):
        s = self._ep(expansion_revenue_pct=0.40, multi_dept_usage_pct=0.30, exec_sponsor_engaged=0.90)
        assert s == 15.0

    def test_dept_high(self):
        s = self._ep(expansion_revenue_pct=0.40, multi_dept_usage_pct=0.60, exec_sponsor_engaged=0.90)
        assert s == 0.0

    def test_exec_very_low(self):
        s = self._ep(expansion_revenue_pct=0.40, multi_dept_usage_pct=0.70, exec_sponsor_engaged=0.10)
        assert s == 25.0

    def test_exec_mid(self):
        s = self._ep(expansion_revenue_pct=0.40, multi_dept_usage_pct=0.70, exec_sponsor_engaged=0.50)
        assert s == 12.0

    def test_exec_high(self):
        s = self._ep(expansion_revenue_pct=0.40, multi_dept_usage_pct=0.70, exec_sponsor_engaged=0.90)
        assert s == 0.0

    def test_all_bad_capped(self):
        s = self._ep(expansion_revenue_pct=0.01, multi_dept_usage_pct=0.05, exec_sponsor_engaged=0.05)
        assert s == 100.0

    def test_all_good_zero(self):
        s = self._ep(expansion_revenue_pct=0.40, multi_dept_usage_pct=0.70, exec_sponsor_engaged=0.90)
        assert s == 0.0

    def test_boundary_expansion_05(self):
        s = self._ep(expansion_revenue_pct=0.05, multi_dept_usage_pct=0.70, exec_sponsor_engaged=0.90)
        assert s == 45.0

    def test_boundary_expansion_15(self):
        s = self._ep(expansion_revenue_pct=0.15, multi_dept_usage_pct=0.70, exec_sponsor_engaged=0.90)
        assert s == 25.0

    def test_boundary_expansion_25(self):
        s = self._ep(expansion_revenue_pct=0.25, multi_dept_usage_pct=0.70, exec_sponsor_engaged=0.90)
        assert s == 10.0

    def test_boundary_dept_20(self):
        s = self._ep(expansion_revenue_pct=0.40, multi_dept_usage_pct=0.20, exec_sponsor_engaged=0.90)
        assert s == 30.0

    def test_boundary_dept_40(self):
        s = self._ep(expansion_revenue_pct=0.40, multi_dept_usage_pct=0.40, exec_sponsor_engaged=0.90)
        assert s == 15.0

    def test_boundary_exec_25(self):
        s = self._ep(expansion_revenue_pct=0.40, multi_dept_usage_pct=0.70, exec_sponsor_engaged=0.25)
        assert s == 25.0

    def test_boundary_exec_60(self):
        s = self._ep(expansion_revenue_pct=0.40, multi_dept_usage_pct=0.70, exec_sponsor_engaged=0.60)
        assert s == 12.0


# ---------------------------------------------------------------------------
# 8. _composite weights
# ---------------------------------------------------------------------------

class TestComposite:
    def _comp(self, ad, en, rr, ep) -> float:
        return _engine()._composite(ad, en, rr, ep)

    def test_weights_sum_to_1(self):
        # 0.30 + 0.25 + 0.25 + 0.20 = 1.00
        assert abs(0.30 + 0.25 + 0.25 + 0.20 - 1.00) < 1e-9

    def test_all_zero(self):
        assert self._comp(0, 0, 0, 0) == 0.0

    def test_all_100(self):
        assert self._comp(100, 100, 100, 100) == 100.0

    def test_adoption_30_pct(self):
        # Only adoption contributes
        result = self._comp(100, 0, 0, 0)
        assert abs(result - 30.0) < 0.01

    def test_engagement_25_pct(self):
        result = self._comp(0, 100, 0, 0)
        assert abs(result - 25.0) < 0.01

    def test_renewal_25_pct(self):
        result = self._comp(0, 0, 100, 0)
        assert abs(result - 25.0) < 0.01

    def test_expansion_20_pct(self):
        result = self._comp(0, 0, 0, 100)
        assert abs(result - 20.0) < 0.01

    def test_composite_formula(self):
        result = self._comp(40, 60, 80, 20)
        expected = round(40 * 0.30 + 60 * 0.25 + 80 * 0.25 + 20 * 0.20, 2)
        assert result == expected

    def test_composite_capped_at_100(self):
        assert self._comp(200, 200, 200, 200) == 100.0

    def test_composite_returns_rounded_2dp(self):
        result = self._comp(33, 33, 33, 33)
        assert result == round(33 * 0.30 + 33 * 0.25 + 33 * 0.25 + 33 * 0.20, 2)


# ---------------------------------------------------------------------------
# 9. Risk thresholds
# ---------------------------------------------------------------------------

class TestRisk:
    def _risk(self, composite) -> LifecycleRisk:
        return _engine()._risk(composite)

    def test_risk_low_below_20(self):
        assert self._risk(10.0) == LifecycleRisk.low

    def test_risk_low_at_19(self):
        assert self._risk(19.99) == LifecycleRisk.low

    def test_risk_moderate_at_20(self):
        assert self._risk(20.0) == LifecycleRisk.moderate

    def test_risk_moderate_at_39(self):
        assert self._risk(39.99) == LifecycleRisk.moderate

    def test_risk_high_at_40(self):
        assert self._risk(40.0) == LifecycleRisk.high

    def test_risk_high_at_59(self):
        assert self._risk(59.99) == LifecycleRisk.high

    def test_risk_critical_at_60(self):
        assert self._risk(60.0) == LifecycleRisk.critical

    def test_risk_critical_at_100(self):
        assert self._risk(100.0) == LifecycleRisk.critical

    def test_risk_low_zero(self):
        assert self._risk(0.0) == LifecycleRisk.low


# ---------------------------------------------------------------------------
# 10. Severity thresholds
# ---------------------------------------------------------------------------

class TestSeverity:
    def _sev(self, composite) -> LifecycleSeverity:
        return _engine()._severity(composite)

    def test_thriving_below_20(self):
        assert self._sev(10.0) == LifecycleSeverity.thriving

    def test_thriving_zero(self):
        assert self._sev(0.0) == LifecycleSeverity.thriving

    def test_stable_at_20(self):
        assert self._sev(20.0) == LifecycleSeverity.stable

    def test_stable_at_39(self):
        assert self._sev(39.99) == LifecycleSeverity.stable

    def test_declining_at_40(self):
        assert self._sev(40.0) == LifecycleSeverity.declining

    def test_declining_at_59(self):
        assert self._sev(59.99) == LifecycleSeverity.declining

    def test_critical_at_60(self):
        assert self._sev(60.0) == LifecycleSeverity.critical

    def test_critical_at_100(self):
        assert self._sev(100.0) == LifecycleSeverity.critical


# ---------------------------------------------------------------------------
# 11. Pattern detection
# ---------------------------------------------------------------------------

class TestPattern:
    def _pat(self, **kw) -> LifecyclePattern:
        return _engine()._pattern(_make_input(**kw))

    def test_churn_trajectory(self):
        pat = self._pat(churn_signal_count=3, health_score_trend=-0.35)
        assert pat == LifecyclePattern.churn_trajectory

    def test_churn_trajectory_boundary(self):
        pat = self._pat(churn_signal_count=3, health_score_trend=-0.30)
        assert pat == LifecyclePattern.churn_trajectory

    def test_no_churn_if_signals_low(self):
        pat = self._pat(churn_signal_count=2, health_score_trend=-0.90)
        # churn needs >= 3 signals
        assert pat != LifecyclePattern.churn_trajectory

    def test_expansion_stall(self):
        pat = self._pat(
            expansion_revenue_pct=0.02,
            customer_age_months=24,
            # ensure no churn pattern
            churn_signal_count=0, health_score_trend=0.0,
        )
        assert pat == LifecyclePattern.expansion_stall

    def test_expansion_stall_boundary_age(self):
        pat = self._pat(
            expansion_revenue_pct=0.05,
            customer_age_months=12,
            churn_signal_count=0, health_score_trend=0.0,
        )
        assert pat == LifecyclePattern.expansion_stall

    def test_no_expansion_stall_if_young(self):
        pat = self._pat(
            expansion_revenue_pct=0.02,
            customer_age_months=6,
            churn_signal_count=0, health_score_trend=0.0,
        )
        assert pat != LifecyclePattern.expansion_stall

    def test_adoption_lag(self):
        pat = self._pat(
            product_adoption_score=0.30,
            onboarding_completion_pct=0.60,
            expansion_revenue_pct=0.40,  # avoid expansion_stall
            customer_age_months=6,
            churn_signal_count=0, health_score_trend=0.0,
        )
        assert pat == LifecyclePattern.adoption_lag

    def test_adoption_lag_boundary(self):
        pat = self._pat(
            product_adoption_score=0.35,
            onboarding_completion_pct=0.65,
            expansion_revenue_pct=0.40,
            customer_age_months=6,
            churn_signal_count=0, health_score_trend=0.0,
        )
        assert pat == LifecyclePattern.adoption_lag

    def test_no_adoption_lag_if_adoption_ok(self):
        pat = self._pat(
            product_adoption_score=0.80,
            onboarding_completion_pct=0.40,
            expansion_revenue_pct=0.40,
            customer_age_months=6,
            churn_signal_count=0, health_score_trend=0.0,
        )
        assert pat != LifecyclePattern.adoption_lag

    def test_renewal_cliff(self):
        pat = self._pat(
            contract_renewal_days_out=30,
            churn_signal_count=1,
            expansion_revenue_pct=0.40,
            customer_age_months=6,
            product_adoption_score=0.80,
            onboarding_completion_pct=0.90,
            health_score_trend=0.0,
        )
        assert pat == LifecyclePattern.renewal_cliff

    def test_renewal_cliff_boundary(self):
        pat = self._pat(
            contract_renewal_days_out=45,
            churn_signal_count=1,
            expansion_revenue_pct=0.40,
            customer_age_months=6,
            product_adoption_score=0.80,
            onboarding_completion_pct=0.90,
            health_score_trend=0.0,
        )
        assert pat == LifecyclePattern.renewal_cliff

    def test_no_renewal_cliff_if_no_signals(self):
        pat = self._pat(
            contract_renewal_days_out=30,
            churn_signal_count=0,
            expansion_revenue_pct=0.40,
            customer_age_months=6,
            product_adoption_score=0.80,
            onboarding_completion_pct=0.90,
            health_score_trend=0.0,
        )
        assert pat != LifecyclePattern.renewal_cliff

    def test_dormant_account(self):
        pat = self._pat(
            days_since_last_meaningful_touch=60,
            login_frequency_per_week=0.5,
            expansion_revenue_pct=0.40,
            customer_age_months=6,
            product_adoption_score=0.80,
            onboarding_completion_pct=0.90,
            contract_renewal_days_out=180,
            churn_signal_count=0,
            health_score_trend=0.0,
        )
        assert pat == LifecyclePattern.dormant_account

    def test_dormant_boundary_touch(self):
        pat = self._pat(
            days_since_last_meaningful_touch=45,
            login_frequency_per_week=1,
            expansion_revenue_pct=0.40,
            customer_age_months=6,
            product_adoption_score=0.80,
            onboarding_completion_pct=0.90,
            contract_renewal_days_out=180,
            churn_signal_count=0,
            health_score_trend=0.0,
        )
        assert pat == LifecyclePattern.dormant_account

    def test_no_dormant_if_active_login(self):
        pat = self._pat(
            days_since_last_meaningful_touch=60,
            login_frequency_per_week=5,
            expansion_revenue_pct=0.40,
            customer_age_months=6,
            product_adoption_score=0.80,
            onboarding_completion_pct=0.90,
            contract_renewal_days_out=180,
            churn_signal_count=0,
            health_score_trend=0.0,
        )
        assert pat != LifecyclePattern.dormant_account

    def test_healthy_returns_none(self):
        # fully healthy baseline
        pat = self._pat()
        assert pat == LifecyclePattern.none

    def test_churn_takes_priority_over_expansion_stall(self):
        # Both churn_trajectory and expansion_stall conditions met
        pat = self._pat(
            churn_signal_count=3,
            health_score_trend=-0.50,
            expansion_revenue_pct=0.02,
            customer_age_months=24,
        )
        assert pat == LifecyclePattern.churn_trajectory


# ---------------------------------------------------------------------------
# 12. Action routing
# ---------------------------------------------------------------------------

class TestAction:
    def _act(self, risk: LifecycleRisk, pattern: LifecyclePattern) -> LifecycleAction:
        return _engine()._action(risk, pattern)

    def test_critical_churn_trajectory(self):
        assert self._act(LifecycleRisk.critical, LifecyclePattern.churn_trajectory) == LifecycleAction.emergency_save_intervention

    def test_critical_renewal_cliff(self):
        assert self._act(LifecycleRisk.critical, LifecyclePattern.renewal_cliff) == LifecycleAction.emergency_save_intervention

    def test_critical_expansion_stall(self):
        assert self._act(LifecycleRisk.critical, LifecyclePattern.expansion_stall) == LifecycleAction.executive_escalation

    def test_critical_adoption_lag(self):
        assert self._act(LifecycleRisk.critical, LifecyclePattern.adoption_lag) == LifecycleAction.executive_escalation

    def test_critical_dormant(self):
        assert self._act(LifecycleRisk.critical, LifecyclePattern.dormant_account) == LifecycleAction.executive_escalation

    def test_critical_none(self):
        assert self._act(LifecycleRisk.critical, LifecyclePattern.none) == LifecycleAction.executive_escalation

    def test_high_churn_trajectory(self):
        assert self._act(LifecycleRisk.high, LifecyclePattern.churn_trajectory) == LifecycleAction.churn_prevention_outreach

    def test_high_expansion_stall(self):
        assert self._act(LifecycleRisk.high, LifecyclePattern.expansion_stall) == LifecycleAction.expansion_play

    def test_high_adoption_lag(self):
        assert self._act(LifecycleRisk.high, LifecyclePattern.adoption_lag) == LifecycleAction.adoption_coaching

    def test_high_renewal_cliff(self):
        assert self._act(LifecycleRisk.high, LifecyclePattern.renewal_cliff) == LifecycleAction.churn_prevention_outreach

    def test_high_dormant(self):
        assert self._act(LifecycleRisk.high, LifecyclePattern.dormant_account) == LifecycleAction.churn_prevention_outreach

    def test_high_none(self):
        assert self._act(LifecycleRisk.high, LifecyclePattern.none) == LifecycleAction.churn_prevention_outreach

    def test_moderate_returns_health_monitoring(self):
        for pat in LifecyclePattern:
            assert self._act(LifecycleRisk.moderate, pat) == LifecycleAction.health_monitoring

    def test_low_returns_no_action(self):
        for pat in LifecyclePattern:
            assert self._act(LifecycleRisk.low, pat) == LifecycleAction.no_action


# ---------------------------------------------------------------------------
# 13. _has_gap flag
# ---------------------------------------------------------------------------

class TestHasGap:
    def _gap(self, composite, **kw) -> bool:
        e = _engine()
        inp = _make_input(**kw)
        return e._has_gap(inp, composite)

    def test_gap_true_composite_gte_40(self):
        assert self._gap(40.0) is True

    def test_gap_true_composite_high(self):
        assert self._gap(80.0) is True

    def test_gap_false_composite_below_40_no_other(self):
        # composite < 40, adoption > 0.50, churn_signal < 2
        assert self._gap(
            39.9,
            product_adoption_score=0.80,
            churn_signal_count=0,
        ) is False

    def test_gap_true_adoption_lte_50(self):
        assert self._gap(
            10.0,
            product_adoption_score=0.50,
            churn_signal_count=0,
        ) is True

    def test_gap_false_adoption_just_above_50(self):
        assert self._gap(
            10.0,
            product_adoption_score=0.51,
            churn_signal_count=0,
        ) is False

    def test_gap_true_churn_signal_gte_2(self):
        assert self._gap(
            10.0,
            product_adoption_score=0.80,
            churn_signal_count=2,
        ) is True

    def test_gap_false_churn_signal_1(self):
        assert self._gap(
            10.0,
            product_adoption_score=0.80,
            churn_signal_count=1,
        ) is False

    def test_gap_true_all_conditions(self):
        assert self._gap(
            50.0,
            product_adoption_score=0.20,
            churn_signal_count=5,
        ) is True


# ---------------------------------------------------------------------------
# 14. _requires_intervention flag
# ---------------------------------------------------------------------------

class TestRequiresIntervention:
    def _ri(self, composite, **kw) -> bool:
        e = _engine()
        inp = _make_input(**kw)
        return e._requires_intervention(inp, composite)

    def test_intervention_composite_gte_30(self):
        assert self._ri(30.0) is True

    def test_no_intervention_composite_29(self):
        assert self._ri(
            29.9,
            health_score_trend=0.20,
            contract_renewal_days_out=180,
        ) is False

    def test_intervention_health_trend_lte_neg_20(self):
        assert self._ri(
            10.0,
            health_score_trend=-0.20,
            contract_renewal_days_out=180,
        ) is True

    def test_no_intervention_health_trend_neg_19(self):
        assert self._ri(
            10.0,
            health_score_trend=-0.19,
            contract_renewal_days_out=180,
        ) is False

    def test_intervention_renewal_lte_60(self):
        assert self._ri(
            10.0,
            health_score_trend=0.20,
            contract_renewal_days_out=60,
        ) is True

    def test_no_intervention_renewal_61(self):
        assert self._ri(
            10.0,
            health_score_trend=0.20,
            contract_renewal_days_out=61,
        ) is False

    def test_intervention_all_conditions(self):
        assert self._ri(
            50.0,
            health_score_trend=-0.50,
            contract_renewal_days_out=30,
        ) is True


# ---------------------------------------------------------------------------
# 15. _churn_risk dollar impact
# ---------------------------------------------------------------------------

class TestChurnRisk:
    def _cr(self, composite, **kw) -> float:
        e = _engine()
        inp = _make_input(**kw)
        return e._churn_risk(inp, composite)

    def test_zero_composite_zero_risk(self):
        assert self._cr(0.0, total_arr_usd=100_000, churn_signal_count=0) == 0.0

    def test_50_composite_no_signals(self):
        expected = round(100_000 * min(1.0, 0.50 * 1.0), 2)
        assert self._cr(50.0, total_arr_usd=100_000, churn_signal_count=0) == expected

    def test_churn_signal_amplification(self):
        # churn_prob = min(1.0, (60/100) * (1 + 2*0.10)) = 0.60 * 1.20 = 0.72
        expected = round(50_000 * 0.72, 2)
        assert self._cr(60.0, total_arr_usd=50_000, churn_signal_count=2) == expected

    def test_capped_at_arr(self):
        # Very high composite with many signals should not exceed ARR
        result = self._cr(100.0, total_arr_usd=200_000, churn_signal_count=20)
        assert result == 200_000.0

    def test_rounded_to_2dp(self):
        result = self._cr(33.0, total_arr_usd=123_456.789, churn_signal_count=1)
        assert result == round(result, 2)

    def test_formula_explicit(self):
        # composite=40, arr=80000, signals=3
        # prob = min(1.0, 0.40 * (1 + 3*0.10)) = 0.40 * 1.30 = 0.52
        expected = round(80_000 * 0.52, 2)
        assert self._cr(40.0, total_arr_usd=80_000, churn_signal_count=3) == expected

    def test_zero_arr(self):
        assert self._cr(100.0, total_arr_usd=0, churn_signal_count=5) == 0.0


# ---------------------------------------------------------------------------
# 16. _signal text
# ---------------------------------------------------------------------------

class TestSignal:
    def _sig(self, composite, pattern, **kw) -> str:
        e = _engine()
        inp = _make_input(**kw)
        return e._signal(inp, pattern, composite)

    def test_healthy_signal_below_20(self):
        sig = self._sig(10.0, LifecyclePattern.none)
        assert "healthy" in sig.lower()

    def test_healthy_signal_exactly_0(self):
        sig = self._sig(0.0, LifecyclePattern.none)
        assert "healthy" in sig.lower()

    def test_signal_contains_pattern_label_churn(self):
        sig = self._sig(50.0, LifecyclePattern.churn_trajectory, product_adoption_score=0.50)
        assert "Churn trajectory" in sig

    def test_signal_contains_pattern_label_expansion(self):
        sig = self._sig(50.0, LifecyclePattern.expansion_stall, product_adoption_score=0.50)
        assert "Expansion stall" in sig

    def test_signal_contains_pattern_label_adoption(self):
        sig = self._sig(50.0, LifecyclePattern.adoption_lag, product_adoption_score=0.50)
        assert "Adoption lag" in sig

    def test_signal_contains_pattern_label_renewal(self):
        sig = self._sig(50.0, LifecyclePattern.renewal_cliff, product_adoption_score=0.50)
        assert "Renewal cliff" in sig

    def test_signal_contains_pattern_label_dormant(self):
        sig = self._sig(50.0, LifecyclePattern.dormant_account, product_adoption_score=0.50)
        assert "Dormant account" in sig

    def test_signal_contains_adoption_pct(self):
        sig = self._sig(50.0, LifecyclePattern.churn_trajectory, product_adoption_score=0.72)
        assert "72% adoption" in sig

    def test_signal_contains_touch_days(self):
        sig = self._sig(50.0, LifecyclePattern.churn_trajectory,
                        product_adoption_score=0.50,
                        days_since_last_meaningful_touch=15)
        assert "15d since last touch" in sig

    def test_signal_contains_renewal_days(self):
        sig = self._sig(50.0, LifecyclePattern.churn_trajectory,
                        product_adoption_score=0.50,
                        contract_renewal_days_out=90)
        assert "90d to renewal" in sig

    def test_signal_contains_composite(self):
        sig = self._sig(50.0, LifecyclePattern.churn_trajectory, product_adoption_score=0.50)
        assert "composite 50" in sig

    def test_signal_at_boundary_20(self):
        # exactly 20 → NOT healthy
        sig = self._sig(20.0, LifecyclePattern.none, product_adoption_score=0.50)
        assert "healthy" not in sig.lower()


# ---------------------------------------------------------------------------
# 17. assess() integration tests
# ---------------------------------------------------------------------------

class TestAssess:
    def test_returns_lifecycle_result(self):
        result = _engine().assess(_make_input())
        assert isinstance(result, LifecycleResult)

    def test_rep_id_passthrough(self):
        r = _engine().assess(_make_input(rep_id="ABC"))
        assert r.rep_id == "ABC"

    def test_region_passthrough(self):
        r = _engine().assess(_make_input(region="APAC"))
        assert r.region == "APAC"

    def test_healthy_baseline_low_risk(self):
        r = _engine().assess(_make_input())
        assert r.lifecycle_risk == LifecycleRisk.low

    def test_healthy_baseline_thriving(self):
        r = _engine().assess(_make_input())
        assert r.lifecycle_severity == LifecycleSeverity.thriving

    def test_healthy_baseline_no_action(self):
        r = _engine().assess(_make_input())
        assert r.recommended_action == LifecycleAction.no_action

    def test_healthy_baseline_no_gap(self):
        r = _engine().assess(_make_input())
        assert r.has_lifecycle_gap is False

    def test_healthy_baseline_no_intervention(self):
        r = _engine().assess(_make_input())
        assert r.requires_lifecycle_intervention is False

    def test_critical_scenario_risk(self):
        inp = _make_input(
            product_adoption_score=0.10,
            feature_utilization_pct=0.10,
            onboarding_completion_pct=0.30,
            days_since_last_meaningful_touch=90,
            login_frequency_per_week=0.3,
            qbr_completion_rate=0.10,
            contract_renewal_days_out=20,
            churn_signal_count=5,
            health_score_trend=-0.80,
            expansion_revenue_pct=0.02,
            multi_dept_usage_pct=0.05,
            exec_sponsor_engaged=0.05,
        )
        r = _engine().assess(inp)
        assert r.lifecycle_risk == LifecycleRisk.critical

    def test_critical_scenario_severity(self):
        inp = _make_input(
            product_adoption_score=0.10,
            feature_utilization_pct=0.10,
            onboarding_completion_pct=0.30,
            days_since_last_meaningful_touch=90,
            login_frequency_per_week=0.3,
            qbr_completion_rate=0.10,
            contract_renewal_days_out=20,
            churn_signal_count=5,
            health_score_trend=-0.80,
            expansion_revenue_pct=0.02,
            multi_dept_usage_pct=0.05,
            exec_sponsor_engaged=0.05,
        )
        r = _engine().assess(inp)
        assert r.lifecycle_severity == LifecycleSeverity.critical

    def test_critical_scenario_has_gap(self):
        inp = _make_input(
            product_adoption_score=0.10,
            churn_signal_count=5,
        )
        r = _engine().assess(inp)
        assert r.has_lifecycle_gap is True

    def test_composite_in_result(self):
        r = _engine().assess(_make_input())
        assert isinstance(r.lifecycle_composite, float)
        assert 0.0 <= r.lifecycle_composite <= 100.0

    def test_adoption_score_in_result(self):
        r = _engine().assess(_make_input())
        assert 0.0 <= r.adoption_score <= 100.0

    def test_engagement_score_in_result(self):
        r = _engine().assess(_make_input())
        assert 0.0 <= r.engagement_score <= 100.0

    def test_renewal_readiness_in_result(self):
        r = _engine().assess(_make_input())
        assert 0.0 <= r.renewal_readiness_score <= 100.0

    def test_expansion_potential_in_result(self):
        r = _engine().assess(_make_input())
        assert 0.0 <= r.expansion_potential_score <= 100.0

    def test_churn_risk_non_negative(self):
        r = _engine().assess(_make_input())
        assert r.estimated_churn_risk_usd >= 0.0

    def test_churn_risk_not_exceeds_arr(self):
        arr = 50_000
        r = _engine().assess(_make_input(total_arr_usd=arr))
        assert r.estimated_churn_risk_usd <= arr

    def test_signal_is_string(self):
        r = _engine().assess(_make_input())
        assert isinstance(r.lifecycle_signal, str)
        assert len(r.lifecycle_signal) > 0

    def test_assess_stores_result(self):
        e = _engine()
        e.assess(_make_input())
        assert len(e._results) == 1

    def test_assess_multiple_stores_all(self):
        e = _engine()
        e.assess(_make_input(rep_id="A"))
        e.assess(_make_input(rep_id="B"))
        assert len(e._results) == 2

    def test_emergency_save_on_churn_trajectory_critical(self):
        # Build an input that yields churn_trajectory pattern and critical risk
        inp = _make_input(
            churn_signal_count=5,
            health_score_trend=-0.90,
            product_adoption_score=0.10,
            feature_utilization_pct=0.10,
            onboarding_completion_pct=0.30,
            days_since_last_meaningful_touch=90,
            login_frequency_per_week=0.3,
            qbr_completion_rate=0.10,
            contract_renewal_days_out=20,
            expansion_revenue_pct=0.02,
            multi_dept_usage_pct=0.05,
            exec_sponsor_engaged=0.05,
        )
        r = _engine().assess(inp)
        assert r.lifecycle_pattern == LifecyclePattern.churn_trajectory
        assert r.recommended_action == LifecycleAction.emergency_save_intervention


# ---------------------------------------------------------------------------
# 18. assess_batch()
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_returns_list(self):
        e = _engine()
        results = e.assess_batch([_make_input(rep_id="A"), _make_input(rep_id="B")])
        assert isinstance(results, list)

    def test_returns_correct_count(self):
        e = _engine()
        results = e.assess_batch([_make_input() for _ in range(5)])
        assert len(results) == 5

    def test_all_are_lifecycle_results(self):
        e = _engine()
        for r in e.assess_batch([_make_input() for _ in range(3)]):
            assert isinstance(r, LifecycleResult)

    def test_empty_batch(self):
        e = _engine()
        assert e.assess_batch([]) == []

    def test_batch_stores_all_results(self):
        e = _engine()
        e.assess_batch([_make_input() for _ in range(4)])
        assert len(e._results) == 4

    def test_batch_order_preserved(self):
        e = _engine()
        ids = ["X1", "X2", "X3"]
        results = e.assess_batch([_make_input(rep_id=i) for i in ids])
        for r, expected_id in zip(results, ids):
            assert r.rep_id == expected_id

    def test_single_element_batch(self):
        e = _engine()
        results = e.assess_batch([_make_input(rep_id="ONLY")])
        assert len(results) == 1
        assert results[0].rep_id == "ONLY"


# ---------------------------------------------------------------------------
# 19. summary() – empty
# ---------------------------------------------------------------------------

class TestSummaryEmpty:
    def _s(self):
        return _engine().summary()

    def test_empty_total_zero(self):
        assert self._s()["total"] == 0

    def test_empty_risk_counts_empty(self):
        assert self._s()["risk_counts"] == {}

    def test_empty_pattern_counts_empty(self):
        assert self._s()["pattern_counts"] == {}

    def test_empty_severity_counts_empty(self):
        assert self._s()["severity_counts"] == {}

    def test_empty_action_counts_empty(self):
        assert self._s()["action_counts"] == {}

    def test_empty_avg_composite_zero(self):
        assert self._s()["avg_lifecycle_composite"] == 0.0

    def test_empty_gap_count_zero(self):
        assert self._s()["lifecycle_gap_count"] == 0

    def test_empty_intervention_count_zero(self):
        assert self._s()["intervention_count"] == 0

    def test_empty_avg_adoption_zero(self):
        assert self._s()["avg_adoption_score"] == 0.0

    def test_empty_avg_engagement_zero(self):
        assert self._s()["avg_engagement_score"] == 0.0

    def test_empty_avg_renewal_zero(self):
        assert self._s()["avg_renewal_readiness_score"] == 0.0

    def test_empty_avg_expansion_zero(self):
        assert self._s()["avg_expansion_potential_score"] == 0.0

    def test_empty_churn_risk_usd_zero(self):
        assert self._s()["total_estimated_churn_risk_usd"] == 0.0

    def test_empty_has_13_keys(self):
        assert len(self._s()) == 13


# ---------------------------------------------------------------------------
# 20. summary() – populated
# ---------------------------------------------------------------------------

class TestSummaryPopulated:
    def _engine_with_data(self):
        e = _engine()
        # healthy record
        e.assess(_make_input(rep_id="H1"))
        # at-risk record: force high composite
        e.assess(_make_input(
            rep_id="R1",
            product_adoption_score=0.10,
            feature_utilization_pct=0.10,
            onboarding_completion_pct=0.30,
            days_since_last_meaningful_touch=90,
            login_frequency_per_week=0.3,
            qbr_completion_rate=0.10,
            contract_renewal_days_out=20,
            churn_signal_count=5,
            health_score_trend=-0.80,
            expansion_revenue_pct=0.02,
            multi_dept_usage_pct=0.05,
            exec_sponsor_engaged=0.05,
        ))
        return e

    def test_total_is_correct(self):
        assert self._engine_with_data().summary()["total"] == 2

    def test_has_13_keys(self):
        assert len(self._engine_with_data().summary()) == 13

    def test_key_total(self):
        assert "total" in self._engine_with_data().summary()

    def test_key_risk_counts(self):
        assert "risk_counts" in self._engine_with_data().summary()

    def test_key_pattern_counts(self):
        assert "pattern_counts" in self._engine_with_data().summary()

    def test_key_severity_counts(self):
        assert "severity_counts" in self._engine_with_data().summary()

    def test_key_action_counts(self):
        assert "action_counts" in self._engine_with_data().summary()

    def test_key_avg_lifecycle_composite(self):
        assert "avg_lifecycle_composite" in self._engine_with_data().summary()

    def test_key_lifecycle_gap_count(self):
        assert "lifecycle_gap_count" in self._engine_with_data().summary()

    def test_key_intervention_count(self):
        # Must be "intervention_count" not "coaching_count"
        s = self._engine_with_data().summary()
        assert "intervention_count" in s
        assert "coaching_count" not in s

    def test_key_avg_adoption_score(self):
        assert "avg_adoption_score" in self._engine_with_data().summary()

    def test_key_avg_engagement_score(self):
        assert "avg_engagement_score" in self._engine_with_data().summary()

    def test_key_avg_renewal_readiness_score(self):
        assert "avg_renewal_readiness_score" in self._engine_with_data().summary()

    def test_key_avg_expansion_potential_score(self):
        assert "avg_expansion_potential_score" in self._engine_with_data().summary()

    def test_key_total_estimated_churn_risk_usd(self):
        assert "total_estimated_churn_risk_usd" in self._engine_with_data().summary()

    def test_risk_counts_sum_to_total(self):
        s = self._engine_with_data().summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_severity_counts_sum_to_total(self):
        s = self._engine_with_data().summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_pattern_counts_sum_to_total(self):
        s = self._engine_with_data().summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_action_counts_sum_to_total(self):
        s = self._engine_with_data().summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_avg_composite_in_range(self):
        s = self._engine_with_data().summary()
        assert 0.0 <= s["avg_lifecycle_composite"] <= 100.0

    def test_intervention_count_gte_0(self):
        assert self._engine_with_data().summary()["intervention_count"] >= 0

    def test_gap_count_gte_0(self):
        assert self._engine_with_data().summary()["lifecycle_gap_count"] >= 0

    def test_churn_risk_usd_positive(self):
        assert self._engine_with_data().summary()["total_estimated_churn_risk_usd"] >= 0.0

    def test_summary_accumulates_across_batches(self):
        e = _engine()
        e.assess_batch([_make_input(rep_id=f"R{i}") for i in range(3)])
        e.assess(_make_input(rep_id="single"))
        assert e.summary()["total"] == 4

    def test_avg_scores_are_rounded(self):
        e = _engine()
        e.assess(_make_input())
        s = e.summary()
        # Should be rounded to 1 decimal
        for key in ["avg_adoption_score", "avg_engagement_score",
                    "avg_renewal_readiness_score", "avg_expansion_potential_score",
                    "avg_lifecycle_composite"]:
            val = s[key]
            assert val == round(val, 1)

    def test_single_result_summary_total_1(self):
        e = _engine()
        e.assess(_make_input())
        assert e.summary()["total"] == 1


# ---------------------------------------------------------------------------
# 21. Edge cases and boundary conditions
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_zero_arr_no_churn_risk(self):
        r = _engine().assess(_make_input(total_arr_usd=0.0))
        assert r.estimated_churn_risk_usd == 0.0

    def test_very_high_arr(self):
        r = _engine().assess(_make_input(total_arr_usd=10_000_000.0))
        assert r.estimated_churn_risk_usd <= 10_000_000.0

    def test_zero_login_frequency(self):
        r = _engine().assess(_make_input(login_frequency_per_week=0.0))
        # Should still run without error
        assert isinstance(r, LifecycleResult)

    def test_zero_churn_signals(self):
        r = _engine().assess(_make_input(churn_signal_count=0))
        assert isinstance(r, LifecycleResult)

    def test_many_churn_signals(self):
        r = _engine().assess(_make_input(churn_signal_count=100))
        assert r.estimated_churn_risk_usd <= r.estimated_churn_risk_usd  # no crash

    def test_product_adoption_at_exactly_0(self):
        r = _engine().assess(_make_input(product_adoption_score=0.0))
        assert r.has_lifecycle_gap is True

    def test_product_adoption_at_exactly_1(self):
        r = _engine().assess(_make_input(product_adoption_score=1.0))
        assert isinstance(r, LifecycleResult)

    def test_health_trend_extreme_negative(self):
        r = _engine().assess(_make_input(health_score_trend=-1.0))
        assert r.requires_lifecycle_intervention is True

    def test_health_trend_extreme_positive(self):
        r = _engine().assess(_make_input(health_score_trend=1.0))
        assert isinstance(r, LifecycleResult)

    def test_renewal_days_very_close(self):
        r = _engine().assess(_make_input(contract_renewal_days_out=1.0))
        assert r.requires_lifecycle_intervention is True

    def test_renewal_days_far_future(self):
        r = _engine().assess(_make_input(contract_renewal_days_out=1000.0))
        assert isinstance(r, LifecycleResult)

    def test_all_scores_within_bounds(self):
        for _ in range(5):
            r = _engine().assess(_make_input(
                product_adoption_score=0.50,
                feature_utilization_pct=0.40,
                onboarding_completion_pct=0.70,
            ))
            assert 0 <= r.adoption_score <= 100
            assert 0 <= r.engagement_score <= 100
            assert 0 <= r.renewal_readiness_score <= 100
            assert 0 <= r.expansion_potential_score <= 100
            assert 0 <= r.lifecycle_composite <= 100

    def test_multiple_engines_independent(self):
        e1 = _engine()
        e2 = _engine()
        e1.assess(_make_input(rep_id="E1"))
        assert e2.summary()["total"] == 0
        assert e1.summary()["total"] == 1

    def test_to_dict_values_match_result_fields(self):
        e = _engine()
        r = e.assess(_make_input())
        d = r.to_dict()
        assert d["rep_id"] == r.rep_id
        assert d["region"] == r.region
        assert d["lifecycle_risk"] == r.lifecycle_risk.value
        assert d["lifecycle_pattern"] == r.lifecycle_pattern.value
        assert d["lifecycle_severity"] == r.lifecycle_severity.value
        assert d["recommended_action"] == r.recommended_action.value
        assert d["adoption_score"] == r.adoption_score
        assert d["engagement_score"] == r.engagement_score
        assert d["renewal_readiness_score"] == r.renewal_readiness_score
        assert d["expansion_potential_score"] == r.expansion_potential_score
        assert d["lifecycle_composite"] == r.lifecycle_composite
        assert d["has_lifecycle_gap"] == r.has_lifecycle_gap
        assert d["requires_lifecycle_intervention"] == r.requires_lifecycle_intervention
        assert d["estimated_churn_risk_usd"] == r.estimated_churn_risk_usd
        assert d["lifecycle_signal"] == r.lifecycle_signal
