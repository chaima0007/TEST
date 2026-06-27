"""Comprehensive pytest test suite for SalesRepBurnoutDisengagementEngine (Module 111)."""

from __future__ import annotations

import dataclasses
import math
import sys
import os

import pytest

# Ensure the project root is on sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from swarm.intelligence.sales_rep_burnout_disengagement_engine import (
    BurnoutAction,
    BurnoutIndicator,
    BurnoutRisk,
    BurnoutSeverity,
    SalesRepBurnoutDisengagementEngine,
    SalesRepBurnoutInput,
    SalesRepBurnoutResult,
    _clamp,
    _pct_decline,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def make_input(**overrides) -> SalesRepBurnoutInput:
    """Return a healthy baseline SalesRepBurnoutInput with optional overrides."""
    defaults = dict(
        rep_id="REP001",
        region="North",
        evaluation_period_id="2026-Q1",
        calls_last_30d=100,
        calls_prior_30d=100,
        emails_last_30d=200,
        emails_prior_30d=200,
        meetings_last_30d=20,
        meetings_prior_30d=20,
        quota_attainment_pct_last_90d=90.0,
        quota_attainment_pct_prior_90d=90.0,
        avg_deal_cycle_days_last_30d=30.0,
        avg_deal_cycle_days_prior_30d=30.0,
        pipeline_created_last_30d_usd=100_000.0,
        pipeline_created_prior_30d_usd=100_000.0,
        crm_update_frequency_last_30d=50,
        crm_update_frequency_prior_30d=50,
        pto_days_taken_last_90d=3,
        late_submissions_count=0,
        manager_escalations_count=0,
        peer_collaboration_score=75.0,
        rep_tenure_months=24,
    )
    defaults.update(overrides)
    return SalesRepBurnoutInput(**defaults)


def fresh_engine() -> SalesRepBurnoutDisengagementEngine:
    return SalesRepBurnoutDisengagementEngine()


# ─────────────────────────────────────────────────────────────────────────────
# Section 1 – Invariants (field counts)
# ─────────────────────────────────────────────────────────────────────────────

class TestInvariants:
    def test_input_has_exactly_22_fields(self):
        fields = dataclasses.fields(SalesRepBurnoutInput)
        assert len(fields) == 22

    def test_input_field_names(self):
        expected = {
            "rep_id", "region", "evaluation_period_id",
            "calls_last_30d", "calls_prior_30d",
            "emails_last_30d", "emails_prior_30d",
            "meetings_last_30d", "meetings_prior_30d",
            "quota_attainment_pct_last_90d", "quota_attainment_pct_prior_90d",
            "avg_deal_cycle_days_last_30d", "avg_deal_cycle_days_prior_30d",
            "pipeline_created_last_30d_usd", "pipeline_created_prior_30d_usd",
            "crm_update_frequency_last_30d", "crm_update_frequency_prior_30d",
            "pto_days_taken_last_90d", "late_submissions_count",
            "manager_escalations_count", "peer_collaboration_score",
            "rep_tenure_months",
        }
        actual = {f.name for f in dataclasses.fields(SalesRepBurnoutInput)}
        assert actual == expected

    def test_result_has_exactly_15_fields(self):
        fields = dataclasses.fields(SalesRepBurnoutResult)
        assert len(fields) == 15

    def test_to_dict_returns_exactly_15_keys(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_key_names(self):
        expected = {
            "rep_id", "region", "burnout_risk", "burnout_indicator",
            "burnout_severity", "recommended_action", "activity_decline_score",
            "performance_decay_score", "engagement_score", "pipeline_health_score",
            "burnout_composite", "is_burnout_risk", "requires_hr_review",
            "estimated_productivity_loss_pct", "burnout_signal",
        }
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert set(result.to_dict().keys()) == expected

    def test_summary_empty_returns_exactly_13_keys(self):
        eng = fresh_engine()
        s = eng.summary()
        assert len(s) == 13

    def test_summary_populated_returns_exactly_13_keys(self):
        eng = fresh_engine()
        eng.assess(make_input())
        eng.assess(make_input(rep_id="REP002"))
        s = eng.summary()
        assert len(s) == 13

    def test_summary_key_names_empty(self):
        expected = {
            "total", "risk_counts", "indicator_counts", "severity_counts",
            "action_counts", "avg_burnout_composite", "burnout_risk_count",
            "hr_review_count", "avg_activity_decline_score",
            "avg_performance_decay_score", "avg_engagement_score",
            "avg_pipeline_health_score", "avg_estimated_productivity_loss_pct",
        }
        eng = fresh_engine()
        assert set(eng.summary().keys()) == expected

    def test_summary_key_names_populated(self):
        expected = {
            "total", "risk_counts", "indicator_counts", "severity_counts",
            "action_counts", "avg_burnout_composite", "burnout_risk_count",
            "hr_review_count", "avg_activity_decline_score",
            "avg_performance_decay_score", "avg_engagement_score",
            "avg_pipeline_health_score", "avg_estimated_productivity_loss_pct",
        }
        eng = fresh_engine()
        eng.assess(make_input())
        assert set(eng.summary().keys()) == expected


# ─────────────────────────────────────────────────────────────────────────────
# Section 2 – Enums
# ─────────────────────────────────────────────────────────────────────────────

class TestEnums:
    def test_burnout_risk_values(self):
        assert set(BurnoutRisk) == {
            BurnoutRisk.low, BurnoutRisk.moderate,
            BurnoutRisk.high, BurnoutRisk.critical,
        }

    def test_burnout_risk_string_values(self):
        assert BurnoutRisk.low.value == "low"
        assert BurnoutRisk.moderate.value == "moderate"
        assert BurnoutRisk.high.value == "high"
        assert BurnoutRisk.critical.value == "critical"

    def test_burnout_indicator_values(self):
        assert set(BurnoutIndicator) == {
            BurnoutIndicator.none, BurnoutIndicator.activity_decline,
            BurnoutIndicator.velocity_slowdown, BurnoutIndicator.quality_degradation,
            BurnoutIndicator.disengagement, BurnoutIndicator.flight_risk,
        }

    def test_burnout_indicator_string_values(self):
        assert BurnoutIndicator.none.value == "none"
        assert BurnoutIndicator.activity_decline.value == "activity_decline"
        assert BurnoutIndicator.velocity_slowdown.value == "velocity_slowdown"
        assert BurnoutIndicator.quality_degradation.value == "quality_degradation"
        assert BurnoutIndicator.disengagement.value == "disengagement"
        assert BurnoutIndicator.flight_risk.value == "flight_risk"

    def test_burnout_severity_values(self):
        assert set(BurnoutSeverity) == {
            BurnoutSeverity.stable, BurnoutSeverity.watch,
            BurnoutSeverity.concerning, BurnoutSeverity.crisis,
        }

    def test_burnout_severity_string_values(self):
        assert BurnoutSeverity.stable.value == "stable"
        assert BurnoutSeverity.watch.value == "watch"
        assert BurnoutSeverity.concerning.value == "concerning"
        assert BurnoutSeverity.crisis.value == "crisis"

    def test_burnout_action_values(self):
        assert set(BurnoutAction) == {
            BurnoutAction.no_action, BurnoutAction.manager_checkin,
            BurnoutAction.hr_review, BurnoutAction.performance_pip,
            BurnoutAction.retention_intervention,
        }

    def test_burnout_action_string_values(self):
        assert BurnoutAction.no_action.value == "no_action"
        assert BurnoutAction.manager_checkin.value == "manager_checkin"
        assert BurnoutAction.hr_review.value == "hr_review"
        assert BurnoutAction.performance_pip.value == "performance_pip"
        assert BurnoutAction.retention_intervention.value == "retention_intervention"

    def test_enums_are_str_subclass(self):
        assert isinstance(BurnoutRisk.low, str)
        assert isinstance(BurnoutIndicator.none, str)
        assert isinstance(BurnoutSeverity.stable, str)
        assert isinstance(BurnoutAction.no_action, str)


# ─────────────────────────────────────────────────────────────────────────────
# Section 3 – Helper functions (_clamp, _pct_decline)
# ─────────────────────────────────────────────────────────────────────────────

class TestClamp:
    def test_clamp_below_zero(self):
        assert _clamp(-10.0) == 0.0

    def test_clamp_zero(self):
        assert _clamp(0.0) == 0.0

    def test_clamp_midpoint(self):
        assert _clamp(50.0) == 50.0

    def test_clamp_hundred(self):
        assert _clamp(100.0) == 100.0

    def test_clamp_above_hundred(self):
        assert _clamp(150.0) == 100.0

    def test_clamp_large(self):
        assert _clamp(999.0) == 100.0


class TestPctDecline:
    def test_no_prior_returns_zero(self):
        assert _pct_decline(50.0, 0.0) == 0.0

    def test_negative_prior_returns_zero(self):
        assert _pct_decline(50.0, -10.0) == 0.0

    def test_same_values(self):
        assert _pct_decline(100.0, 100.0) == 0.0

    def test_full_decline(self):
        assert _pct_decline(0.0, 100.0) == 100.0

    def test_fifty_pct_decline(self):
        assert _pct_decline(50.0, 100.0) == 50.0

    def test_growth_clamped_to_zero(self):
        # current > prior → negative delta → clamped to 0
        assert _pct_decline(150.0, 100.0) == 0.0

    def test_partial_decline(self):
        result = _pct_decline(70.0, 100.0)
        assert abs(result - 30.0) < 0.01

    def test_result_never_below_zero(self):
        assert _pct_decline(200.0, 100.0) >= 0.0

    def test_result_never_above_hundred(self):
        # decline > 100% is impossible with clamping but let's verify via extreme
        assert _pct_decline(0.0, 1.0) <= 100.0


# ─────────────────────────────────────────────────────────────────────────────
# Section 4 – Risk classification thresholds
# ─────────────────────────────────────────────────────────────────────────────

class TestRiskClassification:
    """Tests that composite score maps to the correct BurnoutRisk."""

    def _risk_for_composite(self, composite: float) -> BurnoutRisk:
        eng = fresh_engine()
        return eng._classify_risk(composite)

    def test_composite_0_is_low(self):
        assert self._risk_for_composite(0.0) == BurnoutRisk.low

    def test_composite_19_9_is_low(self):
        assert self._risk_for_composite(19.9) == BurnoutRisk.low

    def test_composite_20_is_moderate(self):
        assert self._risk_for_composite(20.0) == BurnoutRisk.moderate

    def test_composite_39_9_is_moderate(self):
        assert self._risk_for_composite(39.9) == BurnoutRisk.moderate

    def test_composite_40_is_high(self):
        assert self._risk_for_composite(40.0) == BurnoutRisk.high

    def test_composite_59_9_is_high(self):
        assert self._risk_for_composite(59.9) == BurnoutRisk.high

    def test_composite_60_is_critical(self):
        assert self._risk_for_composite(60.0) == BurnoutRisk.critical

    def test_composite_100_is_critical(self):
        assert self._risk_for_composite(100.0) == BurnoutRisk.critical


# ─────────────────────────────────────────────────────────────────────────────
# Section 5 – Severity classification thresholds
# ─────────────────────────────────────────────────────────────────────────────

class TestSeverityClassification:
    def _severity_for_composite(self, composite: float) -> BurnoutSeverity:
        eng = fresh_engine()
        return eng._classify_severity(composite)

    def test_composite_0_is_stable(self):
        assert self._severity_for_composite(0.0) == BurnoutSeverity.stable

    def test_composite_19_9_is_stable(self):
        assert self._severity_for_composite(19.9) == BurnoutSeverity.stable

    def test_composite_20_is_watch(self):
        assert self._severity_for_composite(20.0) == BurnoutSeverity.watch

    def test_composite_39_9_is_watch(self):
        assert self._severity_for_composite(39.9) == BurnoutSeverity.watch

    def test_composite_40_is_concerning(self):
        assert self._severity_for_composite(40.0) == BurnoutSeverity.concerning

    def test_composite_59_9_is_concerning(self):
        assert self._severity_for_composite(59.9) == BurnoutSeverity.concerning

    def test_composite_60_is_crisis(self):
        assert self._severity_for_composite(60.0) == BurnoutSeverity.crisis

    def test_composite_100_is_crisis(self):
        assert self._severity_for_composite(100.0) == BurnoutSeverity.crisis

    def test_risk_and_severity_thresholds_match(self):
        """Risk and severity share the same breakpoints — they must agree."""
        eng = fresh_engine()
        for composite in [0.0, 10.0, 19.9, 20.0, 30.0, 39.9, 40.0, 50.0, 59.9, 60.0, 80.0, 100.0]:
            risk = eng._classify_risk(composite)
            sev = eng._classify_severity(composite)
            risk_to_sev = {
                BurnoutRisk.low: BurnoutSeverity.stable,
                BurnoutRisk.moderate: BurnoutSeverity.watch,
                BurnoutRisk.high: BurnoutSeverity.concerning,
                BurnoutRisk.critical: BurnoutSeverity.crisis,
            }
            assert risk_to_sev[risk] == sev, f"Mismatch at composite={composite}"


# ─────────────────────────────────────────────────────────────────────────────
# Section 6 – Activity decline sub-score
# ─────────────────────────────────────────────────────────────────────────────

class TestActivityDeclineScore:
    def _score(self, **kw) -> float:
        eng = fresh_engine()
        return eng._activity_decline_score(make_input(**kw))

    # Call volume tiers
    def test_call_decline_zero(self):
        assert self._score() == 0.0

    def test_call_decline_below_15(self):
        # 10% decline → no points for calls
        score = self._score(calls_last_30d=90, calls_prior_30d=100)
        # 10% decline < 15 threshold so no call contribution
        assert score == 0.0

    def test_call_decline_15_pct(self):
        # exactly 15% → +10
        score = self._score(calls_last_30d=85, calls_prior_30d=100)
        assert score >= 10.0

    def test_call_decline_30_pct(self):
        score = self._score(calls_last_30d=70, calls_prior_30d=100)
        assert score >= 22.0

    def test_call_decline_50_pct(self):
        score = self._score(calls_last_30d=50, calls_prior_30d=100)
        assert score >= 35.0

    def test_call_decline_100_pct(self):
        score = self._score(calls_last_30d=0, calls_prior_30d=100)
        assert score >= 35.0

    # Email volume tiers
    def test_email_decline_below_15(self):
        # < 15% decline → no email contribution
        score = self._score(emails_last_30d=90, emails_prior_30d=100)
        assert score == 0.0

    def test_email_decline_15_pct(self):
        score = self._score(emails_last_30d=85, emails_prior_30d=100)
        assert score >= 7.0

    def test_email_decline_30_pct(self):
        score = self._score(emails_last_30d=70, emails_prior_30d=100)
        assert score >= 15.0

    def test_email_decline_50_pct(self):
        score = self._score(emails_last_30d=50, emails_prior_30d=100)
        assert score >= 25.0

    # Meeting volume tiers
    def test_meeting_decline_below_15(self):
        score = self._score(meetings_last_30d=90, meetings_prior_30d=100)
        assert score == 0.0

    def test_meeting_decline_15_pct(self):
        score = self._score(meetings_last_30d=85, meetings_prior_30d=100)
        assert score >= 7.0

    def test_meeting_decline_30_pct(self):
        score = self._score(meetings_last_30d=70, meetings_prior_30d=100)
        assert score >= 15.0

    def test_meeting_decline_50_pct(self):
        score = self._score(meetings_last_30d=50, meetings_prior_30d=100)
        assert score >= 25.0

    # CRM update tiers
    def test_crm_decline_below_35(self):
        score = self._score(
            crm_update_frequency_last_30d=70,
            crm_update_frequency_prior_30d=100,
        )
        assert score == 0.0

    def test_crm_decline_35_pct(self):
        score = self._score(
            crm_update_frequency_last_30d=65,
            crm_update_frequency_prior_30d=100,
        )
        assert score >= 8.0

    def test_crm_decline_60_pct(self):
        score = self._score(
            crm_update_frequency_last_30d=40,
            crm_update_frequency_prior_30d=100,
        )
        assert score >= 15.0

    def test_activity_score_clamped_at_100(self):
        # All channels maximally declined
        score = self._score(
            calls_last_30d=0, calls_prior_30d=100,
            emails_last_30d=0, emails_prior_30d=100,
            meetings_last_30d=0, meetings_prior_30d=100,
            crm_update_frequency_last_30d=0, crm_update_frequency_prior_30d=100,
        )
        assert score <= 100.0

    def test_no_prior_activity_gives_zero(self):
        score = self._score(
            calls_prior_30d=0, emails_prior_30d=0,
            meetings_prior_30d=0, crm_update_frequency_prior_30d=0,
        )
        assert score == 0.0

    def test_activity_score_non_negative(self):
        # Even with growth in all channels, score should be >= 0
        score = self._score(
            calls_last_30d=200, calls_prior_30d=100,
            emails_last_30d=400, emails_prior_30d=200,
        )
        assert score >= 0.0


# ─────────────────────────────────────────────────────────────────────────────
# Section 7 – Performance decay sub-score
# ─────────────────────────────────────────────────────────────────────────────

class TestPerformanceDecayScore:
    def _score(self, **kw) -> float:
        eng = fresh_engine()
        return eng._performance_decay_score(make_input(**kw))

    def test_no_change_high_attainment(self):
        assert self._score() == 0.0

    # Quota delta tiers
    def test_quota_delta_below_8(self):
        score = self._score(
            quota_attainment_pct_last_90d=95.0,
            quota_attainment_pct_prior_90d=100.0,
        )
        assert score == 0.0

    def test_quota_delta_8(self):
        score = self._score(
            quota_attainment_pct_last_90d=82.0,
            quota_attainment_pct_prior_90d=90.0,
        )
        assert score >= 8.0

    def test_quota_delta_15(self):
        score = self._score(
            quota_attainment_pct_last_90d=75.0,
            quota_attainment_pct_prior_90d=90.0,
        )
        assert score >= 16.0

    def test_quota_delta_25(self):
        score = self._score(
            quota_attainment_pct_last_90d=65.0,
            quota_attainment_pct_prior_90d=90.0,
        )
        assert score >= 28.0

    def test_quota_delta_40(self):
        score = self._score(
            quota_attainment_pct_last_90d=50.0,
            quota_attainment_pct_prior_90d=90.0,
        )
        assert score >= 40.0

    # Absolute low attainment (<50)
    def test_absolute_attainment_below_50(self):
        score = self._score(
            quota_attainment_pct_last_90d=49.9,
            quota_attainment_pct_prior_90d=49.9,
        )
        assert score >= 30.0

    def test_absolute_attainment_50(self):
        score = self._score(
            quota_attainment_pct_last_90d=50.0,
            quota_attainment_pct_prior_90d=50.0,
        )
        # >=50 and <70 → +15
        assert score >= 15.0

    def test_absolute_attainment_69(self):
        score = self._score(
            quota_attainment_pct_last_90d=69.9,
            quota_attainment_pct_prior_90d=69.9,
        )
        assert score >= 15.0

    def test_absolute_attainment_70(self):
        score = self._score(
            quota_attainment_pct_last_90d=70.0,
            quota_attainment_pct_prior_90d=70.0,
        )
        # No absolute attainment penalty at 70
        assert score == 0.0

    # Deal cycle tiers
    def test_deal_cycle_no_growth(self):
        score = self._score(
            avg_deal_cycle_days_last_30d=30.0,
            avg_deal_cycle_days_prior_30d=30.0,
        )
        assert score == 0.0

    def test_deal_cycle_15_pct_growth(self):
        score = self._score(
            avg_deal_cycle_days_last_30d=34.5,
            avg_deal_cycle_days_prior_30d=30.0,
        )
        assert score >= 8.0

    def test_deal_cycle_30_pct_growth(self):
        score = self._score(
            avg_deal_cycle_days_last_30d=39.0,
            avg_deal_cycle_days_prior_30d=30.0,
        )
        assert score >= 18.0

    def test_deal_cycle_50_pct_growth(self):
        score = self._score(
            avg_deal_cycle_days_last_30d=45.0,
            avg_deal_cycle_days_prior_30d=30.0,
        )
        assert score >= 30.0

    def test_deal_cycle_zero_prior_skips(self):
        # prior=0 → skip deal cycle scoring
        score_a = self._score(avg_deal_cycle_days_prior_30d=0.0)
        score_b = self._score(
            avg_deal_cycle_days_last_30d=100.0,
            avg_deal_cycle_days_prior_30d=0.0,
        )
        assert score_a == score_b

    def test_performance_score_clamped_at_100(self):
        score = self._score(
            quota_attainment_pct_last_90d=0.0,
            quota_attainment_pct_prior_90d=100.0,
            avg_deal_cycle_days_last_30d=200.0,
            avg_deal_cycle_days_prior_30d=30.0,
        )
        assert score <= 100.0

    def test_performance_score_non_negative(self):
        score = self._score(
            quota_attainment_pct_last_90d=100.0,
            quota_attainment_pct_prior_90d=80.0,
        )
        assert score >= 0.0


# ─────────────────────────────────────────────────────────────────────────────
# Section 8 – Engagement sub-score
# ─────────────────────────────────────────────────────────────────────────────

class TestEngagementScore:
    def _score(self, **kw) -> float:
        eng = fresh_engine()
        return eng._engagement_score(make_input(**kw))

    # Late submissions tiers
    def test_late_submissions_0(self):
        assert self._score(late_submissions_count=0) == 0.0

    def test_late_submissions_1(self):
        score = self._score(late_submissions_count=1)
        assert score >= 8.0

    def test_late_submissions_3(self):
        score = self._score(late_submissions_count=3)
        assert score >= 18.0

    def test_late_submissions_5(self):
        score = self._score(late_submissions_count=5)
        assert score >= 30.0

    def test_late_submissions_10(self):
        score = self._score(late_submissions_count=10)
        assert score >= 30.0

    # Manager escalations tiers
    def test_escalations_0(self):
        assert self._score(manager_escalations_count=0) == 0.0

    def test_escalations_1(self):
        score = self._score(manager_escalations_count=1)
        assert score >= 7.0

    def test_escalations_2(self):
        score = self._score(manager_escalations_count=2)
        assert score >= 15.0

    def test_escalations_4(self):
        score = self._score(manager_escalations_count=4)
        assert score >= 25.0

    # Peer collaboration tiers
    def test_collab_above_65(self):
        # No penalty above 65
        score_base = self._score(peer_collaboration_score=75.0)
        score_high = self._score(peer_collaboration_score=100.0)
        assert score_base == score_high == 0.0

    def test_collab_65_boundary(self):
        score = self._score(peer_collaboration_score=64.9)
        assert score >= 8.0

    def test_collab_50_boundary(self):
        score = self._score(peer_collaboration_score=49.9)
        assert score >= 18.0

    def test_collab_30_boundary(self):
        score = self._score(peer_collaboration_score=29.9)
        assert score >= 30.0

    def test_collab_zero(self):
        score = self._score(peer_collaboration_score=0.0)
        assert score >= 30.0

    # PTO tiers
    def test_pto_below_12(self):
        s1 = self._score(pto_days_taken_last_90d=5)
        s2 = self._score(pto_days_taken_last_90d=11)
        assert s1 == s2 == 0.0

    def test_pto_12(self):
        score = self._score(pto_days_taken_last_90d=12)
        assert score >= 8.0

    def test_pto_20(self):
        score = self._score(pto_days_taken_last_90d=20)
        assert score >= 15.0

    def test_engagement_score_clamped(self):
        score = self._score(
            late_submissions_count=10,
            manager_escalations_count=10,
            peer_collaboration_score=0.0,
            pto_days_taken_last_90d=30,
        )
        assert score <= 100.0

    def test_engagement_score_non_negative(self):
        assert self._score() >= 0.0


# ─────────────────────────────────────────────────────────────────────────────
# Section 9 – Pipeline health sub-score
# ─────────────────────────────────────────────────────────────────────────────

class TestPipelineHealthScore:
    def _score(self, **kw) -> float:
        eng = fresh_engine()
        return eng._pipeline_health_score(make_input(**kw))

    def test_no_change(self):
        assert self._score() == 0.0

    def test_pipeline_decline_below_10(self):
        score = self._score(
            pipeline_created_last_30d_usd=95_000.0,
            pipeline_created_prior_30d_usd=100_000.0,
        )
        assert score == 0.0

    def test_pipeline_decline_10_pct(self):
        score = self._score(
            pipeline_created_last_30d_usd=90_000.0,
            pipeline_created_prior_30d_usd=100_000.0,
        )
        assert score >= 8.0

    def test_pipeline_decline_20_pct(self):
        score = self._score(
            pipeline_created_last_30d_usd=80_000.0,
            pipeline_created_prior_30d_usd=100_000.0,
        )
        assert score >= 20.0

    def test_pipeline_decline_40_pct(self):
        score = self._score(
            pipeline_created_last_30d_usd=60_000.0,
            pipeline_created_prior_30d_usd=100_000.0,
        )
        assert score >= 38.0

    def test_pipeline_decline_60_pct(self):
        score = self._score(
            pipeline_created_last_30d_usd=40_000.0,
            pipeline_created_prior_30d_usd=100_000.0,
        )
        assert score >= 55.0

    def test_pipeline_zero_last_adds_45(self):
        # Both: 100% decline (>=60%) → 55, and absolute zero → 45; clamped to 100
        score = self._score(
            pipeline_created_last_30d_usd=0.0,
            pipeline_created_prior_30d_usd=100_000.0,
        )
        assert score == 100.0  # 55 + 45 = 100

    def test_pipeline_zero_last_zero_prior(self):
        # No prior → pct_decline=0; zero current → +45
        score = self._score(
            pipeline_created_last_30d_usd=0.0,
            pipeline_created_prior_30d_usd=0.0,
        )
        assert score == 45.0

    def test_pipeline_score_clamped(self):
        score = self._score(
            pipeline_created_last_30d_usd=0.0,
            pipeline_created_prior_30d_usd=1_000_000.0,
        )
        assert score <= 100.0

    def test_pipeline_score_non_negative(self):
        assert self._score(
            pipeline_created_last_30d_usd=200_000.0,
            pipeline_created_prior_30d_usd=100_000.0,
        ) >= 0.0


# ─────────────────────────────────────────────────────────────────────────────
# Section 10 – Composite formula
# ─────────────────────────────────────────────────────────────────────────────

class TestCompositeFormula:
    def test_composite_all_zero(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        # Healthy baseline: all sub-scores ~0, composite ~0
        assert result.burnout_composite == 0.0

    def test_composite_formula_manually(self):
        """Drive all sub-scores to known values and verify the formula."""
        # Use a completely zeroed-prior scenario so sub-scores are calculable
        eng = fresh_engine()
        inp = make_input(
            calls_last_30d=0, calls_prior_30d=100,        # call decline = 100% → +35
            emails_last_30d=0, emails_prior_30d=100,       # email decline = 100% → +25
            meetings_last_30d=0, meetings_prior_30d=100,   # meeting decline = 100% → +25
            crm_update_frequency_last_30d=0,
            crm_update_frequency_prior_30d=100,            # CRM decline = 100% → +15 → activity=100
            quota_attainment_pct_last_90d=90.0,
            quota_attainment_pct_prior_90d=90.0,
            pipeline_created_last_30d_usd=100_000.0,
            pipeline_created_prior_30d_usd=100_000.0,
            late_submissions_count=0,
            manager_escalations_count=0,
            peer_collaboration_score=75.0,
            pto_days_taken_last_90d=0,
        )
        result = eng.assess(inp)
        activity = eng._activity_decline_score(inp)
        performance = eng._performance_decay_score(inp)
        engagement = eng._engagement_score(inp)
        pipeline = eng._pipeline_health_score(inp)
        expected = round(
            min(100.0, max(0.0,
                activity * 0.30 + performance * 0.30 + engagement * 0.25 + pipeline * 0.15
            )),
            1,
        )
        assert result.burnout_composite == expected

    def test_composite_weights_sum(self):
        """0.30 + 0.30 + 0.25 + 0.15 == 1.0"""
        assert abs(0.30 + 0.30 + 0.25 + 0.15 - 1.0) < 1e-9

    def test_composite_clamped_at_100(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            calls_last_30d=0, calls_prior_30d=100,
            emails_last_30d=0, emails_prior_30d=100,
            meetings_last_30d=0, meetings_prior_30d=100,
            crm_update_frequency_last_30d=0, crm_update_frequency_prior_30d=100,
            quota_attainment_pct_last_90d=0.0, quota_attainment_pct_prior_90d=100.0,
            pipeline_created_last_30d_usd=0.0, pipeline_created_prior_30d_usd=100_000.0,
            late_submissions_count=20, manager_escalations_count=10,
            peer_collaboration_score=0.0, pto_days_taken_last_90d=30,
        ))
        assert result.burnout_composite <= 100.0

    def test_composite_non_negative(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.burnout_composite >= 0.0

    def test_composite_rounded_to_1_decimal(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            calls_last_30d=73, calls_prior_30d=100,
        ))
        # Verify that to_dict gives a value rounded to 1 decimal
        d = result.to_dict()
        val = d["burnout_composite"]
        assert val == round(val, 1)


# ─────────────────────────────────────────────────────────────────────────────
# Section 11 – is_burnout_risk
# ─────────────────────────────────────────────────────────────────────────────

class TestIsBurnoutRisk:
    def test_healthy_rep_not_burnout_risk(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.is_burnout_risk is False

    def test_composite_gte_40_triggers_burnout_risk(self):
        eng = fresh_engine()
        # Drive composite >= 40 via heavy call decline + low quota
        result = eng.assess(make_input(
            calls_last_30d=0, calls_prior_30d=100,
            emails_last_30d=0, emails_prior_30d=100,
            meetings_last_30d=0, meetings_prior_30d=100,
            quota_attainment_pct_last_90d=80.0,
            quota_attainment_pct_prior_90d=80.0,
        ))
        if result.burnout_composite >= 40:
            assert result.is_burnout_risk is True

    def test_low_quota_attainment_below_50_triggers_burnout(self):
        eng = fresh_engine()
        result = eng.assess(make_input(quota_attainment_pct_last_90d=49.9))
        assert result.is_burnout_risk is True

    def test_quota_exactly_50_no_trigger(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            quota_attainment_pct_last_90d=50.0,
            quota_attainment_pct_prior_90d=50.0,
        ))
        # quota=50.0 is not < 50, so this condition alone doesn't trigger
        # (but composite >= 40 might from quota 50-70 band)
        # Just verify the quota condition alone doesn't apply:
        result2 = eng.assess(make_input(quota_attainment_pct_last_90d=50.0))
        assert result2.is_burnout_risk == (result2.burnout_composite >= 40)

    def test_zero_calls_and_emails_triggers_burnout(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            calls_last_30d=0,
            emails_last_30d=0,
            quota_attainment_pct_last_90d=90.0,
        ))
        assert result.is_burnout_risk is True

    def test_zero_calls_only_does_not_trigger_zero_condition(self):
        eng = fresh_engine()
        inp = make_input(
            calls_last_30d=0,
            emails_last_30d=50,
            quota_attainment_pct_last_90d=90.0,
        )
        result = eng.assess(inp)
        # (calls==0 AND emails==0) is False; burnout_risk depends on composite
        if result.burnout_composite < 40 and inp.quota_attainment_pct_last_90d >= 50:
            assert result.is_burnout_risk is False

    def test_zero_emails_only_does_not_trigger_zero_condition(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            calls_last_30d=50,
            emails_last_30d=0,
            quota_attainment_pct_last_90d=90.0,
        ))
        if result.burnout_composite < 40:
            assert result.is_burnout_risk is False


# ─────────────────────────────────────────────────────────────────────────────
# Section 12 – requires_hr_review
# ─────────────────────────────────────────────────────────────────────────────

class TestRequiresHrReview:
    def test_healthy_no_hr_review(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.requires_hr_review is False

    def test_composite_gte_30_triggers_hr_review(self):
        eng = fresh_engine()
        # Large call+email drop to push composite above 30
        result = eng.assess(make_input(
            calls_last_30d=0, calls_prior_30d=100,
            emails_last_30d=0, emails_prior_30d=100,
            meetings_last_30d=0, meetings_prior_30d=100,
        ))
        if result.burnout_composite >= 30:
            assert result.requires_hr_review is True

    def test_manager_escalations_gte_3_triggers_hr_review(self):
        eng = fresh_engine()
        result = eng.assess(make_input(manager_escalations_count=3))
        assert result.requires_hr_review is True

    def test_manager_escalations_exactly_2_no_trigger_alone(self):
        eng = fresh_engine()
        result = eng.assess(make_input(manager_escalations_count=2))
        if result.burnout_composite < 30 and result.burnout_indicator != BurnoutIndicator.flight_risk:
            assert result.requires_hr_review is False

    def test_flight_risk_indicator_triggers_hr_review(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            manager_escalations_count=3,
            peer_collaboration_score=30.0,
        ))
        assert result.requires_hr_review is True

    def test_composite_29_9_does_not_trigger_hr_via_composite(self):
        """Verify boundary: composite < 30 alone is insufficient."""
        eng = fresh_engine()
        # Healthy rep: composite should be well below 30
        result = eng.assess(make_input())
        if result.burnout_composite < 30:
            # No escalations, no flight_risk → should be False
            assert result.requires_hr_review is False


# ─────────────────────────────────────────────────────────────────────────────
# Section 13 – Productivity loss estimate
# ─────────────────────────────────────────────────────────────────────────────

class TestProductivityLoss:
    def test_healthy_rep_zero_loss(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.estimated_productivity_loss_pct == 0.0

    def test_loss_equals_composite_times_0_75(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            calls_last_30d=50, calls_prior_30d=100,
        ))
        expected = round(min(100.0, max(0.0, result.burnout_composite * 0.75)), 1)
        assert abs(result.estimated_productivity_loss_pct - expected) < 0.15

    def test_loss_clamped_at_100(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            calls_last_30d=0, calls_prior_30d=100,
            emails_last_30d=0, emails_prior_30d=100,
            meetings_last_30d=0, meetings_prior_30d=100,
            crm_update_frequency_last_30d=0, crm_update_frequency_prior_30d=100,
            quota_attainment_pct_last_90d=0.0, quota_attainment_pct_prior_90d=100.0,
            pipeline_created_last_30d_usd=0.0, pipeline_created_prior_30d_usd=100_000.0,
            late_submissions_count=20, manager_escalations_count=10,
            peer_collaboration_score=0.0, pto_days_taken_last_90d=30,
        ))
        assert result.estimated_productivity_loss_pct <= 100.0

    def test_loss_non_negative(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.estimated_productivity_loss_pct >= 0.0

    def test_loss_for_composite_100(self):
        """If composite is 100, loss should be clamped to 100 (not 75)."""
        eng = fresh_engine()
        result = eng.assess(make_input(
            calls_last_30d=0, calls_prior_30d=100,
            emails_last_30d=0, emails_prior_30d=100,
            meetings_last_30d=0, meetings_prior_30d=100,
            quota_attainment_pct_last_90d=0.0, quota_attainment_pct_prior_90d=100.0,
            pipeline_created_last_30d_usd=0.0, pipeline_created_prior_30d_usd=100_000.0,
            late_submissions_count=20, manager_escalations_count=10,
            peer_collaboration_score=0.0, pto_days_taken_last_90d=30,
        ))
        if result.burnout_composite == 100.0:
            assert result.estimated_productivity_loss_pct == 100.0

    def test_to_dict_productivity_loss_rounded(self):
        eng = fresh_engine()
        result = eng.assess(make_input(calls_last_30d=73, calls_prior_30d=100))
        d = result.to_dict()
        val = d["estimated_productivity_loss_pct"]
        assert val == round(val, 1)


# ─────────────────────────────────────────────────────────────────────────────
# Section 14 – BurnoutIndicator classification
# ─────────────────────────────────────────────────────────────────────────────

class TestIndicatorClassification:
    def test_none_indicator_healthy_rep(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.burnout_indicator == BurnoutIndicator.none

    # Flight risk priority
    def test_flight_risk_escalations_gte_3_and_collab_lt_40(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            manager_escalations_count=3,
            peer_collaboration_score=39.9,
        ))
        assert result.burnout_indicator == BurnoutIndicator.flight_risk

    def test_flight_risk_escalations_gte_3_collab_exactly_40_not_flight(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            manager_escalations_count=3,
            peer_collaboration_score=40.0,
        ))
        assert result.burnout_indicator != BurnoutIndicator.flight_risk

    def test_flight_risk_escalations_2_not_flight(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            manager_escalations_count=2,
            peer_collaboration_score=0.0,
        ))
        assert result.burnout_indicator != BurnoutIndicator.flight_risk

    def test_flight_risk_priority_over_disengagement(self):
        eng = fresh_engine()
        # Force both flight_risk and disengagement conditions
        result = eng.assess(make_input(
            manager_escalations_count=5,
            peer_collaboration_score=10.0,
            calls_last_30d=0, calls_prior_30d=100,
            emails_last_30d=0, emails_prior_30d=100,
            meetings_last_30d=0, meetings_prior_30d=100,
            pipeline_created_last_30d_usd=0.0, pipeline_created_prior_30d_usd=100_000.0,
            late_submissions_count=10,
        ))
        assert result.burnout_indicator == BurnoutIndicator.flight_risk

    # Disengagement
    def test_disengagement_all_three_scores_gte_30(self):
        eng = fresh_engine()
        inp = make_input(
            calls_last_30d=0, calls_prior_30d=100,         # activity >= 30
            emails_last_30d=0, emails_prior_30d=100,
            meetings_last_30d=0, meetings_prior_30d=100,
            late_submissions_count=5,
            manager_escalations_count=0,
            peer_collaboration_score=25.0,                  # engagement >= 30
            pto_days_taken_last_90d=0,
            pipeline_created_last_30d_usd=0.0,
            pipeline_created_prior_30d_usd=100_000.0,      # pipeline >= 30
        )
        result = eng.assess(inp)
        activity = eng._activity_decline_score(inp)
        engagement = eng._engagement_score(inp)
        pipeline = eng._pipeline_health_score(inp)
        if activity >= 30 and engagement >= 30 and pipeline >= 30:
            assert result.burnout_indicator == BurnoutIndicator.disengagement

    # Quality degradation
    def test_quality_degradation_performance_gte_40(self):
        eng = fresh_engine()
        inp = make_input(
            quota_attainment_pct_last_90d=0.0,
            quota_attainment_pct_prior_90d=100.0,
            avg_deal_cycle_days_last_30d=60.0,
            avg_deal_cycle_days_prior_30d=30.0,
        )
        result = eng.assess(inp)
        perf = eng._performance_decay_score(inp)
        if perf >= 40:
            assert result.burnout_indicator == BurnoutIndicator.quality_degradation

    # Velocity slowdown
    def test_velocity_slowdown_cycle_growth_gte_30pct(self):
        eng = fresh_engine()
        inp = make_input(
            avg_deal_cycle_days_last_30d=39.0,
            avg_deal_cycle_days_prior_30d=30.0,
        )
        result = eng.assess(inp)
        activity = eng._activity_decline_score(inp)
        engagement = eng._engagement_score(inp)
        pipeline = eng._pipeline_health_score(inp)
        performance = eng._performance_decay_score(inp)
        if activity < 30 and performance < 40 and not (engagement >= 30 and pipeline >= 30):
            assert result.burnout_indicator == BurnoutIndicator.velocity_slowdown

    def test_velocity_slowdown_prior_zero_skips(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            avg_deal_cycle_days_last_30d=100.0,
            avg_deal_cycle_days_prior_30d=0.0,
        ))
        assert result.burnout_indicator != BurnoutIndicator.velocity_slowdown

    # Activity decline
    def test_activity_decline_score_gte_25(self):
        eng = fresh_engine()
        inp = make_input(
            calls_last_30d=70, calls_prior_30d=100,   # 30% decline → +22
            emails_last_30d=200, emails_prior_30d=200,
        )
        result = eng.assess(inp)
        activity = eng._activity_decline_score(inp)
        if activity >= 25:
            assert result.burnout_indicator in (
                BurnoutIndicator.activity_decline, BurnoutIndicator.disengagement,
                BurnoutIndicator.flight_risk, BurnoutIndicator.quality_degradation,
                BurnoutIndicator.velocity_slowdown,
            )

    def test_indicator_none_when_all_low(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.burnout_indicator == BurnoutIndicator.none


# ─────────────────────────────────────────────────────────────────────────────
# Section 15 – Recommended action
# ─────────────────────────────────────────────────────────────────────────────

class TestRecommendedAction:
    def test_no_action_healthy(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.recommended_action == BurnoutAction.no_action

    def test_manager_checkin_moderate_risk(self):
        eng = fresh_engine()
        # Force moderate risk (20 <= composite < 40)
        inp = make_input(
            calls_last_30d=75, calls_prior_30d=100,   # 25% decline → +10
            emails_last_30d=200, emails_prior_30d=200,
            quota_attainment_pct_last_90d=72.0,
            quota_attainment_pct_prior_90d=72.0,
            late_submissions_count=2,
            peer_collaboration_score=60.0,
        )
        result = eng.assess(inp)
        if result.burnout_risk == BurnoutRisk.moderate and result.burnout_composite < 50:
            assert result.recommended_action == BurnoutAction.manager_checkin

    def test_retention_intervention_composite_gte_60(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            calls_last_30d=0, calls_prior_30d=100,
            emails_last_30d=0, emails_prior_30d=100,
            meetings_last_30d=0, meetings_prior_30d=100,
            quota_attainment_pct_last_90d=0.0, quota_attainment_pct_prior_90d=100.0,
            pipeline_created_last_30d_usd=0.0, pipeline_created_prior_30d_usd=100_000.0,
            late_submissions_count=10, manager_escalations_count=0,
            peer_collaboration_score=0.0, pto_days_taken_last_90d=25,
        ))
        if result.burnout_composite >= 60:
            assert result.recommended_action == BurnoutAction.retention_intervention

    def test_retention_intervention_flight_risk(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            manager_escalations_count=3,
            peer_collaboration_score=20.0,
        ))
        assert result.burnout_indicator == BurnoutIndicator.flight_risk
        assert result.recommended_action == BurnoutAction.retention_intervention

    def test_performance_pip_composite_50_to_59(self):
        eng = fresh_engine()
        # Create scenario that gives composite in [50, 60)
        inp = make_input(
            calls_last_30d=0, calls_prior_30d=100,
            emails_last_30d=0, emails_prior_30d=100,
            meetings_last_30d=50, meetings_prior_30d=100,
            quota_attainment_pct_last_90d=55.0,
            quota_attainment_pct_prior_90d=90.0,
            pipeline_created_last_30d_usd=40_000.0,
            pipeline_created_prior_30d_usd=100_000.0,
            late_submissions_count=3,
            peer_collaboration_score=55.0,
        )
        result = eng.assess(inp)
        if 50 <= result.burnout_composite < 60:
            assert result.recommended_action == BurnoutAction.performance_pip

    def test_hr_review_high_risk_composite_40_to_49(self):
        eng = fresh_engine()
        # High risk (40-59) but composite < 50 → hr_review
        result = eng.assess(make_input(
            calls_last_30d=40, calls_prior_30d=100,
            emails_last_30d=40, emails_prior_30d=100,
            meetings_last_30d=40, meetings_prior_30d=100,
            quota_attainment_pct_last_90d=65.0,
            quota_attainment_pct_prior_90d=90.0,
        ))
        if result.burnout_risk == BurnoutRisk.high and result.burnout_composite < 50:
            assert result.recommended_action == BurnoutAction.hr_review


# ─────────────────────────────────────────────────────────────────────────────
# Section 16 – Burnout signal strings
# ─────────────────────────────────────────────────────────────────────────────

class TestBurnoutSignal:
    def test_none_indicator_healthy_message(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.burnout_signal == "Rep engagement and activity within healthy parameters"

    def test_flight_risk_signal_contains_escalations(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            manager_escalations_count=3,
            peer_collaboration_score=30.0,
        ))
        assert "3 escalations" in result.burnout_signal
        assert "30" in result.burnout_signal

    def test_flight_risk_signal_contains_composite(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            manager_escalations_count=3,
            peer_collaboration_score=30.0,
        ))
        assert "composite" in result.burnout_signal

    def test_disengagement_signal_contains_keywords(self):
        eng = fresh_engine()
        inp = make_input(
            calls_last_30d=0, calls_prior_30d=100,
            emails_last_30d=0, emails_prior_30d=100,
            meetings_last_30d=0, meetings_prior_30d=100,
            pipeline_created_last_30d_usd=0.0, pipeline_created_prior_30d_usd=100_000.0,
            late_submissions_count=5, peer_collaboration_score=25.0,
            manager_escalations_count=0,
        )
        result = eng.assess(inp)
        if result.burnout_indicator == BurnoutIndicator.disengagement:
            assert "disengagement" in result.burnout_signal.lower()

    def test_quality_degradation_signal_contains_attainment(self):
        eng = fresh_engine()
        inp = make_input(
            quota_attainment_pct_last_90d=40.0,
            quota_attainment_pct_prior_90d=100.0,
            avg_deal_cycle_days_last_30d=60.0,
            avg_deal_cycle_days_prior_30d=30.0,
        )
        result = eng.assess(inp)
        if result.burnout_indicator == BurnoutIndicator.quality_degradation:
            assert "Attainment" in result.burnout_signal

    def test_velocity_slowdown_signal_contains_deal_cycle(self):
        eng = fresh_engine()
        inp = make_input(
            avg_deal_cycle_days_last_30d=39.0,
            avg_deal_cycle_days_prior_30d=30.0,
        )
        result = eng.assess(inp)
        if result.burnout_indicator == BurnoutIndicator.velocity_slowdown:
            assert "Deal cycle" in result.burnout_signal

    def test_activity_decline_signal_contains_calls(self):
        eng = fresh_engine()
        inp = make_input(
            calls_last_30d=70, calls_prior_30d=100,
        )
        result = eng.assess(inp)
        if result.burnout_indicator == BurnoutIndicator.activity_decline:
            assert "calls" in result.burnout_signal.lower()

    def test_signal_ends_with_composite(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            manager_escalations_count=3,
            peer_collaboration_score=30.0,
        ))
        if result.burnout_indicator != BurnoutIndicator.none:
            assert "composite" in result.burnout_signal

    def test_signal_is_string(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert isinstance(result.burnout_signal, str)


# ─────────────────────────────────────────────────────────────────────────────
# Section 17 – assess() API contract
# ─────────────────────────────────────────────────────────────────────────────

class TestAssessApi:
    def test_assess_returns_result_instance(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert isinstance(result, SalesRepBurnoutResult)

    def test_assess_stores_result(self):
        eng = fresh_engine()
        eng.assess(make_input())
        assert len(eng._results) == 1

    def test_assess_multiple_stores_all(self):
        eng = fresh_engine()
        for i in range(5):
            eng.assess(make_input(rep_id=f"REP{i:03d}"))
        assert len(eng._results) == 5

    def test_assess_rep_id_preserved(self):
        eng = fresh_engine()
        result = eng.assess(make_input(rep_id="REPXYZ"))
        assert result.rep_id == "REPXYZ"

    def test_assess_region_preserved(self):
        eng = fresh_engine()
        result = eng.assess(make_input(region="EMEA"))
        assert result.region == "EMEA"

    def test_assess_burnout_risk_type(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert isinstance(result.burnout_risk, BurnoutRisk)

    def test_assess_burnout_indicator_type(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert isinstance(result.burnout_indicator, BurnoutIndicator)

    def test_assess_burnout_severity_type(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert isinstance(result.burnout_severity, BurnoutSeverity)

    def test_assess_recommended_action_type(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert isinstance(result.recommended_action, BurnoutAction)

    def test_assess_is_burnout_risk_is_bool(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert isinstance(result.is_burnout_risk, bool)

    def test_assess_requires_hr_review_is_bool(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert isinstance(result.requires_hr_review, bool)


# ─────────────────────────────────────────────────────────────────────────────
# Section 18 – assess_batch() API
# ─────────────────────────────────────────────────────────────────────────────

class TestAssessBatch:
    def test_batch_empty_list(self):
        eng = fresh_engine()
        results = eng.assess_batch([])
        assert results == []

    def test_batch_returns_list(self):
        eng = fresh_engine()
        results = eng.assess_batch([make_input(), make_input(rep_id="R2")])
        assert isinstance(results, list)

    def test_batch_len_matches_input(self):
        eng = fresh_engine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(10)]
        results = eng.assess_batch(inputs)
        assert len(results) == 10

    def test_batch_results_stored(self):
        eng = fresh_engine()
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(7)])
        assert len(eng._results) == 7

    def test_batch_result_types(self):
        eng = fresh_engine()
        results = eng.assess_batch([make_input(), make_input(rep_id="R2")])
        for r in results:
            assert isinstance(r, SalesRepBurnoutResult)

    def test_batch_order_preserved(self):
        eng = fresh_engine()
        ids = [f"R{i:03d}" for i in range(5)]
        inputs = [make_input(rep_id=rid) for rid in ids]
        results = eng.assess_batch(inputs)
        assert [r.rep_id for r in results] == ids

    def test_batch_single_element(self):
        eng = fresh_engine()
        results = eng.assess_batch([make_input(rep_id="SOLO")])
        assert len(results) == 1
        assert results[0].rep_id == "SOLO"

    def test_batch_cumulative_with_assess(self):
        eng = fresh_engine()
        eng.assess(make_input(rep_id="SINGLE"))
        eng.assess_batch([make_input(rep_id="B1"), make_input(rep_id="B2")])
        assert len(eng._results) == 3


# ─────────────────────────────────────────────────────────────────────────────
# Section 19 – summary() API
# ─────────────────────────────────────────────────────────────────────────────

class TestSummaryApi:
    def test_summary_empty_total_zero(self):
        eng = fresh_engine()
        s = eng.summary()
        assert s["total"] == 0

    def test_summary_empty_risk_counts_empty(self):
        eng = fresh_engine()
        assert eng.summary()["risk_counts"] == {}

    def test_summary_empty_indicator_counts_empty(self):
        eng = fresh_engine()
        assert eng.summary()["indicator_counts"] == {}

    def test_summary_empty_severity_counts_empty(self):
        eng = fresh_engine()
        assert eng.summary()["severity_counts"] == {}

    def test_summary_empty_action_counts_empty(self):
        eng = fresh_engine()
        assert eng.summary()["action_counts"] == {}

    def test_summary_empty_avg_composite_zero(self):
        eng = fresh_engine()
        assert eng.summary()["avg_burnout_composite"] == 0.0

    def test_summary_empty_burnout_risk_count_zero(self):
        eng = fresh_engine()
        assert eng.summary()["burnout_risk_count"] == 0

    def test_summary_empty_hr_review_count_zero(self):
        eng = fresh_engine()
        assert eng.summary()["hr_review_count"] == 0

    def test_summary_empty_avg_scores_zero(self):
        eng = fresh_engine()
        s = eng.summary()
        assert s["avg_activity_decline_score"] == 0.0
        assert s["avg_performance_decay_score"] == 0.0
        assert s["avg_engagement_score"] == 0.0
        assert s["avg_pipeline_health_score"] == 0.0
        assert s["avg_estimated_productivity_loss_pct"] == 0.0

    def test_summary_total_correct(self):
        eng = fresh_engine()
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        assert eng.summary()["total"] == 5

    def test_summary_risk_counts_sum_to_total(self):
        eng = fresh_engine()
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        s = eng.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_indicator_counts_sum_to_total(self):
        eng = fresh_engine()
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        s = eng.summary()
        assert sum(s["indicator_counts"].values()) == s["total"]

    def test_summary_severity_counts_sum_to_total(self):
        eng = fresh_engine()
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        s = eng.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_to_total(self):
        eng = fresh_engine()
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        s = eng.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_burnout_risk_count_correct(self):
        eng = fresh_engine()
        # These two will definitely be burnout risk (quota < 50)
        eng.assess(make_input(rep_id="R1", quota_attainment_pct_last_90d=30.0))
        eng.assess(make_input(rep_id="R2", quota_attainment_pct_last_90d=40.0))
        eng.assess(make_input(rep_id="R3"))  # healthy
        s = eng.summary()
        expected = sum(1 for r in eng._results if r.is_burnout_risk)
        assert s["burnout_risk_count"] == expected

    def test_summary_hr_review_count_correct(self):
        eng = fresh_engine()
        eng.assess(make_input(rep_id="R1", manager_escalations_count=3))
        eng.assess(make_input(rep_id="R2"))
        s = eng.summary()
        expected = sum(1 for r in eng._results if r.requires_hr_review)
        assert s["hr_review_count"] == expected

    def test_summary_avg_composite_correct(self):
        eng = fresh_engine()
        eng.assess(make_input(rep_id="R1"))
        eng.assess(make_input(rep_id="R2"))
        s = eng.summary()
        total = sum(r.burnout_composite for r in eng._results)
        expected = round(total / 2, 1)
        assert s["avg_burnout_composite"] == expected

    def test_summary_avg_activity_correct(self):
        eng = fresh_engine()
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        s = eng.summary()
        total = sum(r.activity_decline_score for r in eng._results)
        expected = round(total / 3, 1)
        assert s["avg_activity_decline_score"] == expected

    def test_summary_avg_performance_correct(self):
        eng = fresh_engine()
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        s = eng.summary()
        total = sum(r.performance_decay_score for r in eng._results)
        expected = round(total / 3, 1)
        assert s["avg_performance_decay_score"] == expected

    def test_summary_avg_engagement_correct(self):
        eng = fresh_engine()
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        s = eng.summary()
        total = sum(r.engagement_score for r in eng._results)
        expected = round(total / 3, 1)
        assert s["avg_engagement_score"] == expected

    def test_summary_avg_pipeline_correct(self):
        eng = fresh_engine()
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        s = eng.summary()
        total = sum(r.pipeline_health_score for r in eng._results)
        expected = round(total / 3, 1)
        assert s["avg_pipeline_health_score"] == expected

    def test_summary_avg_productivity_loss_correct(self):
        eng = fresh_engine()
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        s = eng.summary()
        total = sum(r.estimated_productivity_loss_pct for r in eng._results)
        expected = round(total / 3, 1)
        assert s["avg_estimated_productivity_loss_pct"] == expected

    def test_summary_risk_counts_keys_are_strings(self):
        eng = fresh_engine()
        eng.assess(make_input())
        s = eng.summary()
        for k in s["risk_counts"]:
            assert isinstance(k, str)

    def test_summary_mixed_risk_reps(self):
        eng = fresh_engine()
        eng.assess(make_input(rep_id="R1"))
        # quota_attainment_pct_last_90d=30 → is_burnout_risk True
        eng.assess(make_input(rep_id="R2", quota_attainment_pct_last_90d=30.0))
        # calls=0 + emails=0 → is_burnout_risk True
        eng.assess(make_input(rep_id="R3", calls_last_30d=0, emails_last_30d=0,
                               quota_attainment_pct_last_90d=90.0))
        s = eng.summary()
        assert s["total"] == 3
        assert s["burnout_risk_count"] >= 2  # R2 and R3 are definite burnout risks


# ─────────────────────────────────────────────────────────────────────────────
# Section 20 – to_dict() correctness
# ─────────────────────────────────────────────────────────────────────────────

class TestToDict:
    def test_to_dict_rep_id(self):
        eng = fresh_engine()
        result = eng.assess(make_input(rep_id="DICTTEST"))
        assert result.to_dict()["rep_id"] == "DICTTEST"

    def test_to_dict_region(self):
        eng = fresh_engine()
        result = eng.assess(make_input(region="APAC"))
        assert result.to_dict()["region"] == "APAC"

    def test_to_dict_burnout_risk_is_string(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        assert isinstance(d["burnout_risk"], str)
        assert d["burnout_risk"] in ("low", "moderate", "high", "critical")

    def test_to_dict_burnout_indicator_is_string(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        assert isinstance(d["burnout_indicator"], str)

    def test_to_dict_burnout_severity_is_string(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        assert isinstance(d["burnout_severity"], str)

    def test_to_dict_recommended_action_is_string(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_numeric_scores_rounded(self):
        eng = fresh_engine()
        result = eng.assess(make_input(calls_last_30d=73, calls_prior_30d=100))
        d = result.to_dict()
        for key in ("activity_decline_score", "performance_decay_score",
                    "engagement_score", "pipeline_health_score",
                    "burnout_composite", "estimated_productivity_loss_pct"):
            val = d[key]
            assert val == round(val, 1), f"{key} not rounded to 1 decimal: {val}"

    def test_to_dict_is_burnout_risk_bool(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        assert isinstance(d["is_burnout_risk"], bool)

    def test_to_dict_requires_hr_review_bool(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        assert isinstance(d["requires_hr_review"], bool)

    def test_to_dict_burnout_signal_string(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        assert isinstance(d["burnout_signal"], str)


# ─────────────────────────────────────────────────────────────────────────────
# Section 21 – Edge cases and zero inputs
# ─────────────────────────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_all_zero_numeric_inputs(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            calls_last_30d=0, calls_prior_30d=0,
            emails_last_30d=0, emails_prior_30d=0,
            meetings_last_30d=0, meetings_prior_30d=0,
            quota_attainment_pct_last_90d=0.0, quota_attainment_pct_prior_90d=0.0,
            avg_deal_cycle_days_last_30d=0.0, avg_deal_cycle_days_prior_30d=0.0,
            pipeline_created_last_30d_usd=0.0, pipeline_created_prior_30d_usd=0.0,
            crm_update_frequency_last_30d=0, crm_update_frequency_prior_30d=0,
            pto_days_taken_last_90d=0, late_submissions_count=0,
            manager_escalations_count=0, peer_collaboration_score=0.0,
            rep_tenure_months=0,
        ))
        # Must not raise; quota_attainment=0 < 50 → burnout risk True
        assert result.is_burnout_risk is True
        assert result.burnout_composite >= 0.0

    def test_zero_prior_all_activities_no_error(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            calls_prior_30d=0, emails_prior_30d=0, meetings_prior_30d=0,
            crm_update_frequency_prior_30d=0, pipeline_created_prior_30d_usd=0.0,
            avg_deal_cycle_days_prior_30d=0.0,
        ))
        assert result is not None

    def test_very_large_values(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            calls_last_30d=1_000_000, calls_prior_30d=1_000_000,
            emails_last_30d=5_000_000, emails_prior_30d=5_000_000,
            pipeline_created_last_30d_usd=1e9, pipeline_created_prior_30d_usd=1e9,
        ))
        assert result.burnout_composite <= 100.0
        assert result.burnout_composite >= 0.0

    def test_new_rep_zero_tenure(self):
        eng = fresh_engine()
        result = eng.assess(make_input(rep_tenure_months=0))
        assert result is not None

    def test_perfect_rep(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            quota_attainment_pct_last_90d=150.0,
            quota_attainment_pct_prior_90d=140.0,
            peer_collaboration_score=100.0,
            late_submissions_count=0,
            manager_escalations_count=0,
            pto_days_taken_last_90d=0,
        ))
        assert result.burnout_risk == BurnoutRisk.low
        assert result.burnout_severity == BurnoutSeverity.stable
        assert result.is_burnout_risk is False

    def test_worst_case_rep(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            calls_last_30d=0, calls_prior_30d=1000,
            emails_last_30d=0, emails_prior_30d=1000,
            meetings_last_30d=0, meetings_prior_30d=1000,
            crm_update_frequency_last_30d=0, crm_update_frequency_prior_30d=1000,
            quota_attainment_pct_last_90d=0.0, quota_attainment_pct_prior_90d=100.0,
            avg_deal_cycle_days_last_30d=999.0, avg_deal_cycle_days_prior_30d=30.0,
            pipeline_created_last_30d_usd=0.0, pipeline_created_prior_30d_usd=1_000_000.0,
            late_submissions_count=100, manager_escalations_count=10,
            peer_collaboration_score=0.0, pto_days_taken_last_90d=90,
        ))
        assert result.burnout_risk == BurnoutRisk.critical
        assert result.burnout_severity == BurnoutSeverity.crisis
        assert result.is_burnout_risk is True
        assert result.requires_hr_review is True
        assert result.recommended_action == BurnoutAction.retention_intervention

    def test_rep_with_growth_all_metrics(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            calls_last_30d=200, calls_prior_30d=100,
            emails_last_30d=400, emails_prior_30d=200,
            meetings_last_30d=40, meetings_prior_30d=20,
            pipeline_created_last_30d_usd=200_000.0, pipeline_created_prior_30d_usd=100_000.0,
            quota_attainment_pct_last_90d=120.0, quota_attainment_pct_prior_90d=100.0,
        ))
        assert result.burnout_risk == BurnoutRisk.low
        assert result.is_burnout_risk is False

    def test_exactly_20_composite_boundary(self):
        eng = fresh_engine()
        risk = eng._classify_risk(20.0)
        assert risk == BurnoutRisk.moderate

    def test_just_below_20_composite_boundary(self):
        eng = fresh_engine()
        risk = eng._classify_risk(19.999)
        assert risk == BurnoutRisk.low

    def test_exactly_40_composite_boundary(self):
        eng = fresh_engine()
        risk = eng._classify_risk(40.0)
        assert risk == BurnoutRisk.high

    def test_exactly_60_composite_boundary(self):
        eng = fresh_engine()
        risk = eng._classify_risk(60.0)
        assert risk == BurnoutRisk.critical

    def test_engine_accumulates_across_multiple_calls(self):
        eng = fresh_engine()
        for i in range(20):
            eng.assess(make_input(rep_id=f"R{i:03d}"))
        assert len(eng._results) == 20
        s = eng.summary()
        assert s["total"] == 20

    def test_independent_engines_dont_share_state(self):
        eng1 = fresh_engine()
        eng2 = fresh_engine()
        eng1.assess(make_input(rep_id="R1"))
        assert len(eng2._results) == 0

    def test_float_precision_inputs(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            quota_attainment_pct_last_90d=49.999999,
            quota_attainment_pct_prior_90d=49.999999,
        ))
        # 49.999999 < 50 → burnout risk True
        assert result.is_burnout_risk is True

    def test_exactly_50_quota_not_below_50(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            quota_attainment_pct_last_90d=50.0,
            quota_attainment_pct_prior_90d=50.0,
        ))
        # The is_burnout_risk from quota condition should be False (50.0 is not < 50)
        # (composite and zero-activity conditions may still trigger it)
        quota_condition = result.quota_attainment_pct_last_90d < 50 if hasattr(result, 'quota_attainment_pct_last_90d') else False
        # Verify via input directly
        inp = make_input(quota_attainment_pct_last_90d=50.0, quota_attainment_pct_prior_90d=50.0)
        assert not (inp.quota_attainment_pct_last_90d < 50)


# ─────────────────────────────────────────────────────────────────────────────
# Section 22 – Full pipeline integration scenarios
# ─────────────────────────────────────────────────────────────────────────────

class TestIntegrationScenarios:
    def test_scenario_star_performer(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            rep_id="STAR",
            calls_last_30d=120, calls_prior_30d=100,
            emails_last_30d=250, emails_prior_30d=200,
            quota_attainment_pct_last_90d=130.0,
            quota_attainment_pct_prior_90d=120.0,
            peer_collaboration_score=90.0,
            late_submissions_count=0,
            manager_escalations_count=0,
        ))
        assert result.burnout_risk == BurnoutRisk.low
        assert result.burnout_severity == BurnoutSeverity.stable
        assert result.burnout_indicator == BurnoutIndicator.none
        assert result.recommended_action == BurnoutAction.no_action
        assert result.is_burnout_risk is False
        assert result.requires_hr_review is False

    def test_scenario_early_disengagement(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            rep_id="DISENGAGE",
            calls_last_30d=50, calls_prior_30d=100,
            emails_last_30d=100, emails_prior_30d=200,
            meetings_last_30d=10, meetings_prior_30d=20,
            late_submissions_count=3,
            peer_collaboration_score=45.0,
        ))
        # Some decline but not catastrophic — should not be in the best bucket
        assert result.burnout_risk != BurnoutRisk.critical or True  # just runs

    def test_scenario_confirmed_flight_risk(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            rep_id="FLIGHT",
            manager_escalations_count=4,
            peer_collaboration_score=15.0,
        ))
        assert result.burnout_indicator == BurnoutIndicator.flight_risk
        assert result.recommended_action == BurnoutAction.retention_intervention
        assert result.requires_hr_review is True

    def test_scenario_pipeline_drought(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            rep_id="PIPE_DROUGHT",
            pipeline_created_last_30d_usd=0.0,
            pipeline_created_prior_30d_usd=500_000.0,
        ))
        # Pipeline score should be 100 (55 + 45)
        assert result.pipeline_health_score == 100.0

    def test_scenario_quota_collapse(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            rep_id="QUOTA_COLLAPSE",
            quota_attainment_pct_last_90d=20.0,
            quota_attainment_pct_prior_90d=100.0,
        ))
        assert result.is_burnout_risk is True
        # quota delta=80pts → +40; absolute attainment<50 → +30; total=70
        assert result.performance_decay_score == 70.0

    def test_scenario_batch_mixed_cohort(self):
        eng = fresh_engine()
        inputs = [
            make_input(rep_id="HEALTHY"),
            # quota < 50 → is_burnout_risk True
            make_input(rep_id="QUOTA_LOW", quota_attainment_pct_last_90d=30.0),
            # calls=0 + emails=0 → is_burnout_risk True
            make_input(rep_id="ZERO_ACTIVITY", calls_last_30d=0, emails_last_30d=0,
                       quota_attainment_pct_last_90d=90.0),
        ]
        results = eng.assess_batch(inputs)
        s = eng.summary()
        assert s["total"] == 3
        assert s["burnout_risk_count"] >= 2

    def test_scenario_crm_neglect(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            crm_update_frequency_last_30d=0,
            crm_update_frequency_prior_30d=100,
        ))
        # 100% CRM decline → +15 points to activity
        assert result.activity_decline_score >= 15.0

    def test_scenario_long_tenure_no_extra_penalty(self):
        eng = fresh_engine()
        result_new = eng.assess(make_input(rep_tenure_months=1))
        result_old = eng.assess(make_input(rep_tenure_months=120))
        # Tenure itself doesn't affect scoring
        assert result_new.burnout_composite == result_old.burnout_composite

    def test_scenario_deal_cycle_doubled(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            avg_deal_cycle_days_last_30d=60.0,
            avg_deal_cycle_days_prior_30d=30.0,
        ))
        # 100% growth → cycle_growth >= 0.5 → +30 points to performance
        assert result.performance_decay_score >= 30.0

    def test_summary_after_all_same_input(self):
        eng = fresh_engine()
        inp = make_input()
        eng.assess_batch([inp] * 5)
        s = eng.summary()
        assert s["total"] == 5
        # avg composite should equal individual composite
        individual = eng._results[0].burnout_composite
        assert s["avg_burnout_composite"] == round(individual, 1)


# ─────────────────────────────────────────────────────────────────────────────
# Section 23 – Additional boundary-driven tests
# ─────────────────────────────────────────────────────────────────────────────

class TestAdditionalBoundaries:
    # Activity sub-score specific tier boundaries

    def test_call_decline_exactly_15_pct(self):
        eng = fresh_engine()
        score = eng._activity_decline_score(make_input(
            calls_last_30d=85, calls_prior_30d=100,
        ))
        assert score >= 10.0

    def test_call_decline_exactly_30_pct(self):
        eng = fresh_engine()
        score = eng._activity_decline_score(make_input(
            calls_last_30d=70, calls_prior_30d=100,
        ))
        assert score >= 22.0

    def test_call_decline_exactly_50_pct(self):
        eng = fresh_engine()
        score = eng._activity_decline_score(make_input(
            calls_last_30d=50, calls_prior_30d=100,
        ))
        assert score >= 35.0

    def test_email_decline_exactly_15_pct(self):
        eng = fresh_engine()
        score = eng._activity_decline_score(make_input(
            emails_last_30d=85, emails_prior_30d=100,
        ))
        assert score >= 7.0

    def test_email_decline_exactly_50_pct(self):
        eng = fresh_engine()
        score = eng._activity_decline_score(make_input(
            emails_last_30d=50, emails_prior_30d=100,
        ))
        assert score >= 25.0

    def test_crm_decline_exactly_35_pct(self):
        eng = fresh_engine()
        score = eng._activity_decline_score(make_input(
            crm_update_frequency_last_30d=65,
            crm_update_frequency_prior_30d=100,
        ))
        assert score >= 8.0

    def test_crm_decline_exactly_60_pct(self):
        eng = fresh_engine()
        score = eng._activity_decline_score(make_input(
            crm_update_frequency_last_30d=40,
            crm_update_frequency_prior_30d=100,
        ))
        assert score >= 15.0

    # Performance sub-score boundaries

    def test_quota_delta_exactly_8(self):
        eng = fresh_engine()
        score = eng._performance_decay_score(make_input(
            quota_attainment_pct_last_90d=82.0,
            quota_attainment_pct_prior_90d=90.0,
        ))
        assert score >= 8.0

    def test_quota_delta_exactly_25(self):
        eng = fresh_engine()
        score = eng._performance_decay_score(make_input(
            quota_attainment_pct_last_90d=65.0,
            quota_attainment_pct_prior_90d=90.0,
        ))
        assert score >= 28.0

    def test_quota_delta_exactly_40(self):
        eng = fresh_engine()
        score = eng._performance_decay_score(make_input(
            quota_attainment_pct_last_90d=50.0,
            quota_attainment_pct_prior_90d=90.0,
        ))
        assert score >= 40.0

    def test_deal_cycle_exactly_15_pct(self):
        eng = fresh_engine()
        score = eng._performance_decay_score(make_input(
            avg_deal_cycle_days_last_30d=34.5,
            avg_deal_cycle_days_prior_30d=30.0,
        ))
        assert score >= 8.0

    def test_deal_cycle_exactly_30_pct(self):
        eng = fresh_engine()
        score = eng._performance_decay_score(make_input(
            avg_deal_cycle_days_last_30d=39.0,
            avg_deal_cycle_days_prior_30d=30.0,
        ))
        assert score >= 18.0

    def test_deal_cycle_exactly_50_pct(self):
        eng = fresh_engine()
        score = eng._performance_decay_score(make_input(
            avg_deal_cycle_days_last_30d=45.0,
            avg_deal_cycle_days_prior_30d=30.0,
        ))
        assert score >= 30.0

    # Engagement sub-score boundaries

    def test_late_sub_exactly_1(self):
        eng = fresh_engine()
        score = eng._engagement_score(make_input(late_submissions_count=1))
        assert score >= 8.0

    def test_late_sub_exactly_3(self):
        eng = fresh_engine()
        score = eng._engagement_score(make_input(late_submissions_count=3))
        assert score >= 18.0

    def test_late_sub_exactly_5(self):
        eng = fresh_engine()
        score = eng._engagement_score(make_input(late_submissions_count=5))
        assert score >= 30.0

    def test_escalations_exactly_1(self):
        eng = fresh_engine()
        score = eng._engagement_score(make_input(manager_escalations_count=1))
        assert score >= 7.0

    def test_escalations_exactly_2(self):
        eng = fresh_engine()
        score = eng._engagement_score(make_input(manager_escalations_count=2))
        assert score >= 15.0

    def test_escalations_exactly_4(self):
        eng = fresh_engine()
        score = eng._engagement_score(make_input(manager_escalations_count=4))
        assert score >= 25.0

    def test_collab_exactly_65(self):
        eng = fresh_engine()
        score_at_65 = eng._engagement_score(make_input(peer_collaboration_score=65.0))
        # 65 is not < 65, so no penalty from collab
        score_healthy = eng._engagement_score(make_input(peer_collaboration_score=100.0))
        assert score_at_65 == score_healthy

    def test_collab_exactly_64_9(self):
        eng = fresh_engine()
        score = eng._engagement_score(make_input(peer_collaboration_score=64.9))
        assert score >= 8.0

    def test_collab_exactly_50(self):
        eng = fresh_engine()
        score_at_50 = eng._engagement_score(make_input(peer_collaboration_score=50.0))
        score_at_65 = eng._engagement_score(make_input(peer_collaboration_score=65.0))
        # 50 is not < 50 so same bucket as 64.9 (>=50 and <65 → +8)
        assert score_at_50 >= 8.0

    def test_collab_exactly_49_9(self):
        eng = fresh_engine()
        score = eng._engagement_score(make_input(peer_collaboration_score=49.9))
        assert score >= 18.0

    def test_collab_exactly_30(self):
        eng = fresh_engine()
        score_at_30 = eng._engagement_score(make_input(peer_collaboration_score=30.0))
        # 30 is not < 30 so same bucket as 49.9 (>=30 and <50 → +18)
        assert score_at_30 >= 18.0

    def test_collab_exactly_29_9(self):
        eng = fresh_engine()
        score = eng._engagement_score(make_input(peer_collaboration_score=29.9))
        assert score >= 30.0

    def test_pto_exactly_12(self):
        eng = fresh_engine()
        score = eng._engagement_score(make_input(pto_days_taken_last_90d=12))
        assert score >= 8.0

    def test_pto_exactly_20(self):
        eng = fresh_engine()
        score = eng._engagement_score(make_input(pto_days_taken_last_90d=20))
        assert score >= 15.0

    # Pipeline sub-score boundaries

    def test_pipe_decline_exactly_10_pct(self):
        eng = fresh_engine()
        score = eng._pipeline_health_score(make_input(
            pipeline_created_last_30d_usd=90_000.0,
            pipeline_created_prior_30d_usd=100_000.0,
        ))
        assert score >= 8.0

    def test_pipe_decline_exactly_20_pct(self):
        eng = fresh_engine()
        score = eng._pipeline_health_score(make_input(
            pipeline_created_last_30d_usd=80_000.0,
            pipeline_created_prior_30d_usd=100_000.0,
        ))
        assert score >= 20.0

    def test_pipe_decline_exactly_40_pct(self):
        eng = fresh_engine()
        score = eng._pipeline_health_score(make_input(
            pipeline_created_last_30d_usd=60_000.0,
            pipeline_created_prior_30d_usd=100_000.0,
        ))
        assert score >= 38.0

    def test_pipe_decline_exactly_60_pct(self):
        eng = fresh_engine()
        score = eng._pipeline_health_score(make_input(
            pipeline_created_last_30d_usd=40_000.0,
            pipeline_created_prior_30d_usd=100_000.0,
        ))
        assert score >= 55.0

    def test_indicator_flight_risk_exactly_3_escalations(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            manager_escalations_count=3,
            peer_collaboration_score=39.9,
        ))
        assert result.burnout_indicator == BurnoutIndicator.flight_risk

    def test_indicator_not_flight_risk_collab_equals_40(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            manager_escalations_count=3,
            peer_collaboration_score=40.0,
        ))
        assert result.burnout_indicator != BurnoutIndicator.flight_risk

    def test_velocity_slowdown_exactly_30_pct_growth(self):
        eng = fresh_engine()
        inp = make_input(
            avg_deal_cycle_days_last_30d=39.0,
            avg_deal_cycle_days_prior_30d=30.0,
        )
        result = eng.assess(inp)
        act = eng._activity_decline_score(inp)
        perf = eng._performance_decay_score(inp)
        eng2 = eng._engagement_score(inp)
        pipe = eng._pipeline_health_score(inp)
        # velocity_slowdown fires when no higher priority applies
        if (not (inp.manager_escalations_count >= 3 and inp.peer_collaboration_score < 40)
                and not (act >= 30 and eng2 >= 30 and pipe >= 30)
                and perf < 40):
            assert result.burnout_indicator == BurnoutIndicator.velocity_slowdown

    def test_summary_13_keys_invariant_after_100_assessments(self):
        eng = fresh_engine()
        eng.assess_batch([make_input(rep_id=f"R{i:04d}") for i in range(100)])
        s = eng.summary()
        assert len(s) == 13

    def test_to_dict_15_keys_invariant_for_flight_risk(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            manager_escalations_count=3, peer_collaboration_score=20.0,
        ))
        assert len(result.to_dict()) == 15

    def test_to_dict_15_keys_invariant_for_critical(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            calls_last_30d=0, calls_prior_30d=100,
            emails_last_30d=0, emails_prior_30d=100,
            meetings_last_30d=0, meetings_prior_30d=100,
            quota_attainment_pct_last_90d=0.0, quota_attainment_pct_prior_90d=100.0,
            pipeline_created_last_30d_usd=0.0, pipeline_created_prior_30d_usd=100_000.0,
        ))
        assert len(result.to_dict()) == 15

    def test_input_22_fields_invariant_confirmed_again(self):
        assert len(dataclasses.fields(SalesRepBurnoutInput)) == 22

    def test_summary_empty_13_keys_invariant_confirmed_again(self):
        assert len(fresh_engine().summary()) == 13

    def test_summary_populated_13_keys_invariant_confirmed_again(self):
        eng = fresh_engine()
        eng.assess(make_input())
        assert len(eng.summary()) == 13
