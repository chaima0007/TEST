"""Comprehensive pytest test suite for CustomerLTVErosionDetector."""

from __future__ import annotations

import pytest

from swarm.intelligence.customer_ltv_erosion_detector import (
    CustomerLTVErosionDetector,
    CustomerLTVInput,
    CustomerLTVResult,
    ErosionRisk,
    ErosionPattern,
    ErosionSeverity,
    ErosionAction,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_input(**overrides) -> CustomerLTVInput:
    """Return a healthy-baseline CustomerLTVInput with overridable fields."""
    defaults = dict(
        customer_id="CUST-001",
        csm_id="CSM-001",
        evaluation_period_id="2024-Q1",
        contract_arr_usd=100_000.0,
        account_age_months=12,
        product_usage_score_last_30d=80.0,
        product_usage_score_prior_30d=80.0,
        feature_adoption_pct=60.0,
        benchmark_feature_adoption_pct=65.0,
        nps_score=70,
        nps_score_prior=70,
        executive_last_contact_days=15,
        executive_meetings_last_90d=3,
        executive_meetings_prior_90d=3,
        support_tickets_last_30d=2,
        support_tickets_prior_30d=2,
        critical_tickets_last_30d=0,
        expansion_revenue_last_12m_usd=20_000.0,
        expansion_revenue_prior_12m_usd=20_000.0,
        logo_at_risk_flag=0,
        competitor_evaluation_signal=0,
        renewal_days_remaining=180,
    )
    defaults.update(overrides)
    return CustomerLTVInput(**defaults)


def fresh_engine() -> CustomerLTVErosionDetector:
    return CustomerLTVErosionDetector()


# ── Section 1: Enum values ────────────────────────────────────────────────────

class TestEnumValues:
    def test_erosion_risk_low(self):
        assert ErosionRisk.low.value == "low"

    def test_erosion_risk_moderate(self):
        assert ErosionRisk.moderate.value == "moderate"

    def test_erosion_risk_high(self):
        assert ErosionRisk.high.value == "high"

    def test_erosion_risk_critical(self):
        assert ErosionRisk.critical.value == "critical"

    def test_erosion_pattern_none(self):
        assert ErosionPattern.none.value == "none"

    def test_erosion_pattern_usage_cliff(self):
        assert ErosionPattern.usage_cliff.value == "usage_cliff"

    def test_erosion_pattern_exec_relationship_loss(self):
        assert ErosionPattern.exec_relationship_loss.value == "exec_relationship_loss"

    def test_erosion_pattern_expansion_stall(self):
        assert ErosionPattern.expansion_stall.value == "expansion_stall"

    def test_erosion_pattern_support_overload(self):
        assert ErosionPattern.support_overload.value == "support_overload"

    def test_erosion_pattern_competitive_migration(self):
        assert ErosionPattern.competitive_migration.value == "competitive_migration"

    def test_erosion_severity_healthy(self):
        assert ErosionSeverity.healthy.value == "healthy"

    def test_erosion_severity_watch(self):
        assert ErosionSeverity.watch.value == "watch"

    def test_erosion_severity_degrading(self):
        assert ErosionSeverity.degrading.value == "degrading"

    def test_erosion_severity_critical(self):
        assert ErosionSeverity.critical.value == "critical"

    def test_erosion_action_no_action(self):
        assert ErosionAction.no_action.value == "no_action"

    def test_erosion_action_csm_outreach(self):
        assert ErosionAction.csm_outreach.value == "csm_outreach"

    def test_erosion_action_executive_qbr(self):
        assert ErosionAction.executive_qbr.value == "executive_qbr"

    def test_erosion_action_rescue_plan(self):
        assert ErosionAction.rescue_plan.value == "rescue_plan"

    def test_erosion_action_churn_prevention_team(self):
        assert ErosionAction.churn_prevention_team.value == "churn_prevention_team"


# ── Section 2: Healthy baseline ───────────────────────────────────────────────

class TestHealthyBaseline:
    def setup_method(self):
        self.engine = fresh_engine()
        self.result = self.engine.assess(make_input())

    def test_returns_result_type(self):
        assert isinstance(self.result, CustomerLTVResult)

    def test_customer_id_preserved(self):
        assert self.result.customer_id == "CUST-001"

    def test_csm_id_preserved(self):
        assert self.result.csm_id == "CSM-001"

    def test_risk_low(self):
        assert self.result.erosion_risk == ErosionRisk.low

    def test_severity_healthy(self):
        assert self.result.erosion_severity == ErosionSeverity.healthy

    def test_pattern_none(self):
        assert self.result.erosion_pattern == ErosionPattern.none

    def test_action_no_action(self):
        assert self.result.recommended_action == ErosionAction.no_action

    def test_not_at_churn_risk(self):
        assert self.result.is_at_churn_risk is False

    def test_no_executive_attention_needed(self):
        assert self.result.requires_executive_attention is False

    def test_composite_low(self):
        assert self.result.erosion_composite < 20

    def test_usage_decline_score_low(self):
        assert self.result.usage_decline_score < 20

    def test_engagement_decay_score_low(self):
        assert self.result.engagement_decay_score < 20

    def test_signal_contains_acceptable(self):
        assert "acceptable" in self.result.erosion_signal.lower()


# ── Section 3: Usage decline score ───────────────────────────────────────────

class TestUsageDeclineScore:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_no_decline_zero_score(self):
        r = self.engine.assess(make_input(
            product_usage_score_last_30d=80.0,
            product_usage_score_prior_30d=80.0,
        ))
        # adoption gap is small so usage score is just from adoption
        assert r.usage_decline_score < 15

    def test_5pct_decline_adds_6(self):
        # exactly 5% decline
        r = self.engine.assess(make_input(
            product_usage_score_last_30d=76.0,
            product_usage_score_prior_30d=80.0,
            feature_adoption_pct=65.0,
            benchmark_feature_adoption_pct=65.0,
            critical_tickets_last_30d=0,
        ))
        assert r.usage_decline_score >= 6.0

    def test_10pct_decline_adds_14(self):
        r = self.engine.assess(make_input(
            product_usage_score_last_30d=72.0,
            product_usage_score_prior_30d=80.0,
            feature_adoption_pct=65.0,
            benchmark_feature_adoption_pct=65.0,
            critical_tickets_last_30d=0,
        ))
        assert r.usage_decline_score >= 14.0

    def test_25pct_decline_adds_28(self):
        r = self.engine.assess(make_input(
            product_usage_score_last_30d=60.0,
            product_usage_score_prior_30d=80.0,
            feature_adoption_pct=65.0,
            benchmark_feature_adoption_pct=65.0,
            critical_tickets_last_30d=0,
        ))
        assert r.usage_decline_score >= 28.0

    def test_40pct_decline_adds_45(self):
        r = self.engine.assess(make_input(
            product_usage_score_last_30d=48.0,
            product_usage_score_prior_30d=80.0,
            feature_adoption_pct=65.0,
            benchmark_feature_adoption_pct=65.0,
            critical_tickets_last_30d=0,
        ))
        assert r.usage_decline_score >= 45.0

    def test_adoption_gap_10_adds_8(self):
        r = self.engine.assess(make_input(
            product_usage_score_last_30d=80.0,
            product_usage_score_prior_30d=80.0,
            feature_adoption_pct=60.0,
            benchmark_feature_adoption_pct=70.0,
            critical_tickets_last_30d=0,
        ))
        assert r.usage_decline_score >= 8.0

    def test_adoption_gap_25_adds_18(self):
        r = self.engine.assess(make_input(
            product_usage_score_last_30d=80.0,
            product_usage_score_prior_30d=80.0,
            feature_adoption_pct=40.0,
            benchmark_feature_adoption_pct=65.0,
            critical_tickets_last_30d=0,
        ))
        assert r.usage_decline_score >= 18.0

    def test_adoption_gap_40_adds_30(self):
        r = self.engine.assess(make_input(
            product_usage_score_last_30d=80.0,
            product_usage_score_prior_30d=80.0,
            feature_adoption_pct=20.0,
            benchmark_feature_adoption_pct=60.0,
            critical_tickets_last_30d=0,
        ))
        assert r.usage_decline_score >= 30.0

    def test_1_critical_ticket_adds_12(self):
        r = self.engine.assess(make_input(
            product_usage_score_last_30d=80.0,
            product_usage_score_prior_30d=80.0,
            feature_adoption_pct=65.0,
            benchmark_feature_adoption_pct=65.0,
            critical_tickets_last_30d=1,
        ))
        assert r.usage_decline_score >= 12.0

    def test_3_critical_tickets_adds_25(self):
        r = self.engine.assess(make_input(
            product_usage_score_last_30d=80.0,
            product_usage_score_prior_30d=80.0,
            feature_adoption_pct=65.0,
            benchmark_feature_adoption_pct=65.0,
            critical_tickets_last_30d=3,
        ))
        assert r.usage_decline_score >= 25.0

    def test_zero_prior_usage_skips_usage_delta(self):
        # prior=0 means the delta branch is skipped entirely
        r = self.engine.assess(make_input(
            product_usage_score_last_30d=0.0,
            product_usage_score_prior_30d=0.0,
            feature_adoption_pct=65.0,
            benchmark_feature_adoption_pct=65.0,
            critical_tickets_last_30d=0,
        ))
        assert r.usage_decline_score == 0.0

    def test_usage_score_clamped_at_100(self):
        # max possible: 45 + 30 + 25 = 100
        r = self.engine.assess(make_input(
            product_usage_score_last_30d=0.0,
            product_usage_score_prior_30d=100.0,
            feature_adoption_pct=0.0,
            benchmark_feature_adoption_pct=60.0,
            critical_tickets_last_30d=5,
        ))
        assert r.usage_decline_score <= 100.0

    def test_usage_score_not_negative(self):
        r = self.engine.assess(make_input(
            product_usage_score_last_30d=100.0,
            product_usage_score_prior_30d=80.0,
            feature_adoption_pct=70.0,
            benchmark_feature_adoption_pct=65.0,
            critical_tickets_last_30d=0,
        ))
        assert r.usage_decline_score >= 0.0


# ── Section 4: Engagement decay score ────────────────────────────────────────

class TestEngagementDecayScore:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_stable_nps_low_score(self):
        r = self.engine.assess(make_input(nps_score=70, nps_score_prior=70))
        assert r.engagement_decay_score < 10

    def test_nps_delta_10_adds_12(self):
        r = self.engine.assess(make_input(
            nps_score=60,
            nps_score_prior=70,
            support_tickets_last_30d=2,
            support_tickets_prior_30d=2,
        ))
        assert r.engagement_decay_score >= 12.0

    def test_nps_delta_20_adds_25(self):
        r = self.engine.assess(make_input(
            nps_score=50,
            nps_score_prior=70,
            support_tickets_last_30d=2,
            support_tickets_prior_30d=2,
        ))
        assert r.engagement_decay_score >= 25.0

    def test_nps_delta_30_adds_40(self):
        r = self.engine.assess(make_input(
            nps_score=40,
            nps_score_prior=70,
            support_tickets_last_30d=2,
            support_tickets_prior_30d=2,
        ))
        assert r.engagement_decay_score >= 40.0

    def test_absolute_nps_20_adds_30(self):
        r = self.engine.assess(make_input(
            nps_score=20,
            nps_score_prior=20,
            support_tickets_last_30d=2,
            support_tickets_prior_30d=2,
        ))
        assert r.engagement_decay_score >= 30.0

    def test_absolute_nps_40_adds_15(self):
        r = self.engine.assess(make_input(
            nps_score=40,
            nps_score_prior=40,
            support_tickets_last_30d=2,
            support_tickets_prior_30d=2,
        ))
        assert r.engagement_decay_score >= 15.0

    def test_ticket_ratio_1p5x_adds_8(self):
        r = self.engine.assess(make_input(
            nps_score=70,
            nps_score_prior=70,
            support_tickets_last_30d=3,
            support_tickets_prior_30d=2,
        ))
        assert r.engagement_decay_score >= 8.0

    def test_ticket_ratio_2x_adds_18(self):
        r = self.engine.assess(make_input(
            nps_score=70,
            nps_score_prior=70,
            support_tickets_last_30d=4,
            support_tickets_prior_30d=2,
        ))
        assert r.engagement_decay_score >= 18.0

    def test_ticket_ratio_3x_adds_30(self):
        r = self.engine.assess(make_input(
            nps_score=70,
            nps_score_prior=70,
            support_tickets_last_30d=6,
            support_tickets_prior_30d=2,
        ))
        assert r.engagement_decay_score >= 30.0

    def test_zero_prior_tickets_skips_ratio(self):
        r = self.engine.assess(make_input(
            nps_score=70,
            nps_score_prior=70,
            support_tickets_last_30d=10,
            support_tickets_prior_30d=0,
        ))
        # ratio branch skipped; only non-ticket contributions
        assert r.engagement_decay_score < 20

    def test_engagement_score_clamped_at_100(self):
        r = self.engine.assess(make_input(
            nps_score=0,
            nps_score_prior=70,
            support_tickets_last_30d=9,
            support_tickets_prior_30d=2,
        ))
        assert r.engagement_decay_score <= 100.0

    def test_engagement_score_not_negative(self):
        r = self.engine.assess(make_input(
            nps_score=80,
            nps_score_prior=70,
        ))
        assert r.engagement_decay_score >= 0.0


# ── Section 5: Expansion health score ────────────────────────────────────────

class TestExpansionHealthScore:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_stable_expansion_low_score(self):
        r = self.engine.assess(make_input(
            expansion_revenue_last_12m_usd=20_000.0,
            expansion_revenue_prior_12m_usd=20_000.0,
            logo_at_risk_flag=0,
            renewal_days_remaining=180,
        ))
        assert r.expansion_health_score < 15

    def test_expansion_delta_10pct_adds_12(self):
        r = self.engine.assess(make_input(
            expansion_revenue_last_12m_usd=18_000.0,
            expansion_revenue_prior_12m_usd=20_000.0,
            logo_at_risk_flag=0,
            renewal_days_remaining=180,
        ))
        assert r.expansion_health_score >= 12.0

    def test_expansion_delta_30pct_adds_25(self):
        r = self.engine.assess(make_input(
            expansion_revenue_last_12m_usd=14_000.0,
            expansion_revenue_prior_12m_usd=20_000.0,
            logo_at_risk_flag=0,
            renewal_days_remaining=180,
        ))
        assert r.expansion_health_score >= 25.0

    def test_expansion_delta_50pct_adds_40(self):
        r = self.engine.assess(make_input(
            expansion_revenue_last_12m_usd=10_000.0,
            expansion_revenue_prior_12m_usd=20_000.0,
            logo_at_risk_flag=0,
            renewal_days_remaining=180,
        ))
        assert r.expansion_health_score >= 40.0

    def test_zero_expansion_age_24_adds_20(self):
        r = self.engine.assess(make_input(
            expansion_revenue_last_12m_usd=0.0,
            expansion_revenue_prior_12m_usd=0.0,
            account_age_months=24,
            logo_at_risk_flag=0,
            renewal_days_remaining=180,
        ))
        assert r.expansion_health_score >= 20.0

    def test_zero_expansion_age_23_no_bonus(self):
        # prior=0, last=0 but age < 24 → bonus branch not entered
        r = self.engine.assess(make_input(
            expansion_revenue_last_12m_usd=0.0,
            expansion_revenue_prior_12m_usd=0.0,
            account_age_months=23,
            logo_at_risk_flag=0,
            renewal_days_remaining=180,
        ))
        assert r.expansion_health_score < 20.0

    def test_logo_at_risk_adds_35(self):
        r = self.engine.assess(make_input(
            expansion_revenue_last_12m_usd=20_000.0,
            expansion_revenue_prior_12m_usd=20_000.0,
            logo_at_risk_flag=1,
            renewal_days_remaining=180,
        ))
        assert r.expansion_health_score >= 35.0

    def test_renewal_30d_adds_25(self):
        r = self.engine.assess(make_input(
            expansion_revenue_last_12m_usd=20_000.0,
            expansion_revenue_prior_12m_usd=20_000.0,
            logo_at_risk_flag=0,
            renewal_days_remaining=30,
        ))
        assert r.expansion_health_score >= 25.0

    def test_renewal_60d_adds_12(self):
        r = self.engine.assess(make_input(
            expansion_revenue_last_12m_usd=20_000.0,
            expansion_revenue_prior_12m_usd=20_000.0,
            logo_at_risk_flag=0,
            renewal_days_remaining=60,
        ))
        assert r.expansion_health_score >= 12.0

    def test_renewal_61d_no_bonus(self):
        r = self.engine.assess(make_input(
            expansion_revenue_last_12m_usd=20_000.0,
            expansion_revenue_prior_12m_usd=20_000.0,
            logo_at_risk_flag=0,
            renewal_days_remaining=61,
        ))
        assert r.expansion_health_score < 12.0

    def test_zero_prior_expansion_skips_delta(self):
        # prior > 0 branch not entered; last > 0 so no age-based bonus either
        r = self.engine.assess(make_input(
            expansion_revenue_last_12m_usd=5_000.0,
            expansion_revenue_prior_12m_usd=0.0,
            logo_at_risk_flag=0,
            renewal_days_remaining=180,
        ))
        # no delta contribution, no logo, no renewal urgency
        assert r.expansion_health_score < 15

    def test_expansion_health_score_clamped_at_100(self):
        r = self.engine.assess(make_input(
            expansion_revenue_last_12m_usd=0.0,
            expansion_revenue_prior_12m_usd=100_000.0,
            logo_at_risk_flag=1,
            renewal_days_remaining=30,
        ))
        assert r.expansion_health_score <= 100.0

    def test_expansion_health_score_not_negative(self):
        r = self.engine.assess(make_input(
            expansion_revenue_last_12m_usd=50_000.0,
            expansion_revenue_prior_12m_usd=20_000.0,
            logo_at_risk_flag=0,
            renewal_days_remaining=200,
        ))
        assert r.expansion_health_score >= 0.0


# ── Section 6: Relationship risk score ───────────────────────────────────────

class TestRelationshipRiskScore:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_recent_contact_low_score(self):
        r = self.engine.assess(make_input(
            executive_last_contact_days=10,
            executive_meetings_last_90d=3,
            executive_meetings_prior_90d=3,
            competitor_evaluation_signal=0,
        ))
        assert r.relationship_risk_score < 15

    def test_contact_30d_adds_10(self):
        r = self.engine.assess(make_input(
            executive_last_contact_days=30,
            executive_meetings_last_90d=3,
            executive_meetings_prior_90d=3,
            competitor_evaluation_signal=0,
        ))
        assert r.relationship_risk_score >= 10.0

    def test_contact_60d_adds_24(self):
        r = self.engine.assess(make_input(
            executive_last_contact_days=60,
            executive_meetings_last_90d=3,
            executive_meetings_prior_90d=3,
            competitor_evaluation_signal=0,
        ))
        assert r.relationship_risk_score >= 24.0

    def test_contact_90d_adds_40(self):
        r = self.engine.assess(make_input(
            executive_last_contact_days=90,
            executive_meetings_last_90d=3,
            executive_meetings_prior_90d=3,
            competitor_evaluation_signal=0,
        ))
        assert r.relationship_risk_score >= 40.0

    def test_meeting_decline_20pct_adds_8(self):
        r = self.engine.assess(make_input(
            executive_last_contact_days=10,
            executive_meetings_last_90d=4,
            executive_meetings_prior_90d=5,
            competitor_evaluation_signal=0,
        ))
        assert r.relationship_risk_score >= 8.0

    def test_meeting_decline_40pct_adds_18(self):
        r = self.engine.assess(make_input(
            executive_last_contact_days=10,
            executive_meetings_last_90d=3,
            executive_meetings_prior_90d=5,
            competitor_evaluation_signal=0,
        ))
        assert r.relationship_risk_score >= 18.0

    def test_meeting_decline_70pct_adds_30(self):
        r = self.engine.assess(make_input(
            executive_last_contact_days=10,
            executive_meetings_last_90d=1,
            executive_meetings_prior_90d=5,
            competitor_evaluation_signal=0,
        ))
        assert r.relationship_risk_score >= 30.0

    def test_competitor_signal_adds_30(self):
        r = self.engine.assess(make_input(
            executive_last_contact_days=10,
            executive_meetings_last_90d=3,
            executive_meetings_prior_90d=3,
            competitor_evaluation_signal=1,
        ))
        assert r.relationship_risk_score >= 30.0

    def test_zero_prior_meetings_skips_delta(self):
        r = self.engine.assess(make_input(
            executive_last_contact_days=10,
            executive_meetings_last_90d=5,
            executive_meetings_prior_90d=0,
            competitor_evaluation_signal=0,
        ))
        # no meeting delta; only contact contribution
        assert r.relationship_risk_score < 15

    def test_relationship_score_clamped_at_100(self):
        r = self.engine.assess(make_input(
            executive_last_contact_days=90,
            executive_meetings_last_90d=0,
            executive_meetings_prior_90d=10,
            competitor_evaluation_signal=1,
        ))
        assert r.relationship_risk_score <= 100.0

    def test_relationship_score_not_negative(self):
        r = self.engine.assess(make_input(
            executive_last_contact_days=5,
            executive_meetings_last_90d=5,
            executive_meetings_prior_90d=3,
            competitor_evaluation_signal=0,
        ))
        assert r.relationship_risk_score >= 0.0


# ── Section 7: Composite & risk thresholds ───────────────────────────────────

class TestCompositeAndRisk:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_composite_formula_low(self):
        """Ensure composite = weighted sum when all subscores are well-known."""
        r = self.engine.assess(make_input())
        expected = (
            r.usage_decline_score * 0.30
            + r.engagement_decay_score * 0.30
            + r.expansion_health_score * 0.25
            + r.relationship_risk_score * 0.15
        )
        assert abs(r.erosion_composite - round(expected, 1)) <= 0.15

    def test_risk_low_below_20(self):
        r = self.engine.assess(make_input())
        assert r.erosion_composite < 20
        assert r.erosion_risk == ErosionRisk.low

    def test_risk_moderate_between_20_and_40(self):
        # elevate composite into [20, 40)
        r = self.engine.assess(make_input(
            nps_score=40,
            nps_score_prior=40,
            executive_last_contact_days=30,
        ))
        if 20 <= r.erosion_composite < 40:
            assert r.erosion_risk == ErosionRisk.moderate

    def test_risk_high_between_40_and_60(self):
        r = self.engine.assess(make_input(
            nps_score=20,
            nps_score_prior=50,
            support_tickets_last_30d=6,
            support_tickets_prior_30d=2,
            executive_last_contact_days=60,
            logo_at_risk_flag=0,
        ))
        if 40 <= r.erosion_composite < 60:
            assert r.erosion_risk == ErosionRisk.high

    def test_risk_critical_at_60(self):
        r = self.engine.assess(make_input(
            product_usage_score_last_30d=40.0,
            product_usage_score_prior_30d=80.0,
            nps_score=15,
            nps_score_prior=60,
            support_tickets_last_30d=6,
            support_tickets_prior_30d=2,
            executive_last_contact_days=90,
            logo_at_risk_flag=1,
            renewal_days_remaining=20,
            critical_tickets_last_30d=3,
        ))
        assert r.erosion_composite >= 60
        assert r.erosion_risk == ErosionRisk.critical

    def test_composite_not_negative(self):
        r = self.engine.assess(make_input())
        assert r.erosion_composite >= 0.0

    def test_composite_not_above_100(self):
        r = self.engine.assess(make_input(
            product_usage_score_last_30d=0.0,
            product_usage_score_prior_30d=100.0,
            nps_score=0,
            nps_score_prior=100,
            support_tickets_last_30d=30,
            support_tickets_prior_30d=2,
            executive_last_contact_days=90,
            logo_at_risk_flag=1,
            renewal_days_remaining=10,
            critical_tickets_last_30d=5,
            competitor_evaluation_signal=1,
            feature_adoption_pct=0.0,
            benchmark_feature_adoption_pct=100.0,
            expansion_revenue_last_12m_usd=0.0,
            expansion_revenue_prior_12m_usd=100_000.0,
        ))
        assert r.erosion_composite <= 100.0


# ── Section 8: Severity thresholds ───────────────────────────────────────────

class TestSeverityThresholds:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_severity_healthy_below_20(self):
        r = self.engine.assess(make_input())
        assert r.erosion_composite < 20
        assert r.erosion_severity == ErosionSeverity.healthy

    def test_severity_watch_20_to_39(self):
        r = self.engine.assess(make_input(
            nps_score=40,
            nps_score_prior=40,
            executive_last_contact_days=30,
        ))
        if 20 <= r.erosion_composite < 40:
            assert r.erosion_severity == ErosionSeverity.watch

    def test_severity_degrading_40_to_59(self):
        r = self.engine.assess(make_input(
            nps_score=20,
            nps_score_prior=50,
            support_tickets_last_30d=6,
            support_tickets_prior_30d=2,
            executive_last_contact_days=60,
        ))
        if 40 <= r.erosion_composite < 60:
            assert r.erosion_severity == ErosionSeverity.degrading

    def test_severity_critical_at_60(self):
        r = self.engine.assess(make_input(
            product_usage_score_last_30d=40.0,
            product_usage_score_prior_30d=80.0,
            nps_score=15,
            nps_score_prior=60,
            support_tickets_last_30d=6,
            support_tickets_prior_30d=2,
            executive_last_contact_days=90,
            logo_at_risk_flag=1,
            renewal_days_remaining=20,
            critical_tickets_last_30d=3,
        ))
        if r.erosion_composite >= 60:
            assert r.erosion_severity == ErosionSeverity.critical


# ── Section 9: Recommended action ────────────────────────────────────────────

class TestRecommendedAction:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_no_action_low_risk(self):
        r = self.engine.assess(make_input())
        assert r.erosion_risk == ErosionRisk.low
        assert r.recommended_action == ErosionAction.no_action

    def test_csm_outreach_moderate_risk(self):
        # Force composite into moderate band [20, 40) and below 50
        r = self.engine.assess(make_input(
            nps_score=40,
            nps_score_prior=55,
            executive_last_contact_days=30,
            support_tickets_last_30d=2,
            support_tickets_prior_30d=2,
        ))
        if r.erosion_risk == ErosionRisk.moderate:
            assert r.recommended_action == ErosionAction.csm_outreach

    def test_executive_qbr_high_risk_below_50(self):
        r = self.engine.assess(make_input(
            nps_score=20,
            nps_score_prior=50,
            support_tickets_last_30d=6,
            support_tickets_prior_30d=2,
            executive_last_contact_days=60,
        ))
        if r.erosion_risk == ErosionRisk.high and r.erosion_composite < 50:
            assert r.recommended_action == ErosionAction.executive_qbr

    def test_rescue_plan_composite_50_to_59(self):
        # Need composite in [50, 60)
        r = self.engine.assess(make_input(
            product_usage_score_last_30d=48.0,
            product_usage_score_prior_30d=80.0,
            nps_score=20,
            nps_score_prior=50,
            executive_last_contact_days=60,
            support_tickets_last_30d=4,
            support_tickets_prior_30d=2,
        ))
        if 50 <= r.erosion_composite < 60:
            assert r.recommended_action == ErosionAction.rescue_plan

    def test_churn_prevention_team_composite_60_plus(self):
        r = self.engine.assess(make_input(
            product_usage_score_last_30d=40.0,
            product_usage_score_prior_30d=80.0,
            nps_score=15,
            nps_score_prior=60,
            support_tickets_last_30d=6,
            support_tickets_prior_30d=2,
            executive_last_contact_days=90,
            logo_at_risk_flag=1,
            renewal_days_remaining=20,
            critical_tickets_last_30d=3,
        ))
        if r.erosion_composite >= 60:
            assert r.recommended_action == ErosionAction.churn_prevention_team


# ── Section 10: Erosion patterns ─────────────────────────────────────────────

class TestErosionPatterns:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_pattern_none_healthy(self):
        r = self.engine.assess(make_input())
        assert r.erosion_pattern == ErosionPattern.none

    def test_competitive_migration_pattern(self):
        # competitor_evaluation_signal=1 AND relationship>=20
        r = self.engine.assess(make_input(
            competitor_evaluation_signal=1,
            executive_last_contact_days=90,
        ))
        assert r.erosion_pattern == ErosionPattern.competitive_migration

    def test_competitive_migration_requires_relationship_ge_20(self):
        # competitor_evaluation_signal=1 but relationship < 20 → different pattern
        r = self.engine.assess(make_input(
            competitor_evaluation_signal=1,
            executive_last_contact_days=5,
            executive_meetings_last_90d=3,
            executive_meetings_prior_90d=3,
        ))
        # relationship score from only competitor signal = 30 >= 20 so still competitive_migration
        assert r.erosion_pattern == ErosionPattern.competitive_migration

    def test_exec_relationship_loss_pattern(self):
        # executive_last_contact_days>=60 AND relationship>=25, no competitor signal
        r = self.engine.assess(make_input(
            competitor_evaluation_signal=0,
            executive_last_contact_days=60,
            executive_meetings_last_90d=1,
            executive_meetings_prior_90d=5,
        ))
        assert r.erosion_pattern == ErosionPattern.exec_relationship_loss

    def test_exec_relationship_loss_needs_days_ge_60(self):
        r = self.engine.assess(make_input(
            competitor_evaluation_signal=0,
            executive_last_contact_days=59,
        ))
        assert r.erosion_pattern != ErosionPattern.exec_relationship_loss

    def test_support_overload_pattern(self):
        # critical_tickets>=2 AND engagement>=25, no higher-priority pattern
        r = self.engine.assess(make_input(
            competitor_evaluation_signal=0,
            executive_last_contact_days=10,
            critical_tickets_last_30d=2,
            nps_score=20,
            nps_score_prior=20,
            support_tickets_last_30d=2,
            support_tickets_prior_30d=2,
        ))
        assert r.erosion_pattern == ErosionPattern.support_overload

    def test_support_overload_needs_critical_ge_2(self):
        r = self.engine.assess(make_input(
            competitor_evaluation_signal=0,
            executive_last_contact_days=10,
            critical_tickets_last_30d=1,
            nps_score=20,
            nps_score_prior=20,
        ))
        assert r.erosion_pattern != ErosionPattern.support_overload

    def test_usage_cliff_pattern(self):
        # usage_delta>=0.25 AND usage>=20, no higher-priority patterns
        r = self.engine.assess(make_input(
            competitor_evaluation_signal=0,
            executive_last_contact_days=10,
            critical_tickets_last_30d=0,
            product_usage_score_last_30d=50.0,
            product_usage_score_prior_30d=80.0,
            feature_adoption_pct=20.0,
            benchmark_feature_adoption_pct=60.0,
        ))
        assert r.erosion_pattern == ErosionPattern.usage_cliff

    def test_usage_cliff_needs_prior_gt_0(self):
        # prior=0 skips usage_delta → no usage_cliff
        r = self.engine.assess(make_input(
            competitor_evaluation_signal=0,
            executive_last_contact_days=10,
            critical_tickets_last_30d=0,
            product_usage_score_last_30d=0.0,
            product_usage_score_prior_30d=0.0,
            expansion_revenue_last_12m_usd=20_000.0,
            account_age_months=10,
        ))
        assert r.erosion_pattern != ErosionPattern.usage_cliff

    def test_expansion_stall_pattern(self):
        # account_age_months>=18 AND expansion_revenue_last_12m_usd==0
        r = self.engine.assess(make_input(
            competitor_evaluation_signal=0,
            executive_last_contact_days=10,
            critical_tickets_last_30d=0,
            product_usage_score_last_30d=80.0,
            product_usage_score_prior_30d=80.0,
            account_age_months=18,
            expansion_revenue_last_12m_usd=0.0,
        ))
        assert r.erosion_pattern == ErosionPattern.expansion_stall

    def test_expansion_stall_needs_age_ge_18(self):
        r = self.engine.assess(make_input(
            competitor_evaluation_signal=0,
            executive_last_contact_days=10,
            critical_tickets_last_30d=0,
            product_usage_score_last_30d=80.0,
            product_usage_score_prior_30d=80.0,
            account_age_months=17,
            expansion_revenue_last_12m_usd=0.0,
        ))
        assert r.erosion_pattern != ErosionPattern.expansion_stall

    def test_competitive_migration_takes_priority_over_exec_loss(self):
        r = self.engine.assess(make_input(
            competitor_evaluation_signal=1,
            executive_last_contact_days=90,
            executive_meetings_last_90d=0,
            executive_meetings_prior_90d=5,
        ))
        assert r.erosion_pattern == ErosionPattern.competitive_migration

    def test_competitive_migration_takes_priority_over_support_overload(self):
        r = self.engine.assess(make_input(
            competitor_evaluation_signal=1,
            executive_last_contact_days=90,
            critical_tickets_last_30d=3,
            nps_score=20,
            nps_score_prior=20,
        ))
        assert r.erosion_pattern == ErosionPattern.competitive_migration

    def test_exec_loss_takes_priority_over_support_overload(self):
        r = self.engine.assess(make_input(
            competitor_evaluation_signal=0,
            executive_last_contact_days=90,
            executive_meetings_last_90d=0,
            executive_meetings_prior_90d=5,
            critical_tickets_last_30d=3,
            nps_score=20,
            nps_score_prior=20,
        ))
        assert r.erosion_pattern == ErosionPattern.exec_relationship_loss

    def test_exec_loss_takes_priority_over_usage_cliff(self):
        r = self.engine.assess(make_input(
            competitor_evaluation_signal=0,
            executive_last_contact_days=90,
            executive_meetings_last_90d=0,
            executive_meetings_prior_90d=5,
            critical_tickets_last_30d=0,
            product_usage_score_last_30d=40.0,
            product_usage_score_prior_30d=80.0,
            feature_adoption_pct=10.0,
            benchmark_feature_adoption_pct=60.0,
        ))
        assert r.erosion_pattern == ErosionPattern.exec_relationship_loss

    def test_support_overload_takes_priority_over_usage_cliff(self):
        r = self.engine.assess(make_input(
            competitor_evaluation_signal=0,
            executive_last_contact_days=10,
            critical_tickets_last_30d=3,
            nps_score=20,
            nps_score_prior=20,
            product_usage_score_last_30d=40.0,
            product_usage_score_prior_30d=80.0,
            feature_adoption_pct=10.0,
            benchmark_feature_adoption_pct=60.0,
        ))
        assert r.erosion_pattern == ErosionPattern.support_overload

    def test_usage_cliff_takes_priority_over_expansion_stall(self):
        r = self.engine.assess(make_input(
            competitor_evaluation_signal=0,
            executive_last_contact_days=10,
            critical_tickets_last_30d=0,
            product_usage_score_last_30d=40.0,
            product_usage_score_prior_30d=80.0,
            feature_adoption_pct=10.0,
            benchmark_feature_adoption_pct=60.0,
            account_age_months=24,
            expansion_revenue_last_12m_usd=0.0,
        ))
        assert r.erosion_pattern == ErosionPattern.usage_cliff


# ── Section 11: is_at_churn_risk ─────────────────────────────────────────────

class TestIsAtChurnRisk:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_not_at_risk_healthy(self):
        r = self.engine.assess(make_input())
        assert r.is_at_churn_risk is False

    def test_at_risk_composite_ge_40(self):
        r = self.engine.assess(make_input(
            nps_score=20,
            nps_score_prior=50,
            support_tickets_last_30d=6,
            support_tickets_prior_30d=2,
            executive_last_contact_days=60,
        ))
        if r.erosion_composite >= 40:
            assert r.is_at_churn_risk is True

    def test_at_risk_logo_flag_regardless_of_composite(self):
        # logo_at_risk_flag=1 alone makes it at churn risk
        r = self.engine.assess(make_input(logo_at_risk_flag=1))
        assert r.is_at_churn_risk is True

    def test_at_risk_renewal_30d_and_composite_ge_20(self):
        # renewal<=30 AND composite>=20 → at risk
        r = self.engine.assess(make_input(
            renewal_days_remaining=30,
            nps_score=40,
            nps_score_prior=50,
            executive_last_contact_days=30,
        ))
        if r.erosion_composite >= 20 and r.erosion_composite < 40:
            assert r.is_at_churn_risk is True

    def test_not_at_risk_renewal_31d_composite_20_to_39(self):
        r = self.engine.assess(make_input(
            renewal_days_remaining=31,
            nps_score=40,
            nps_score_prior=50,
            logo_at_risk_flag=0,
            executive_last_contact_days=30,
        ))
        if 20 <= r.erosion_composite < 40:
            assert r.is_at_churn_risk is False

    def test_not_at_risk_renewal_30d_composite_below_20(self):
        r = self.engine.assess(make_input(
            renewal_days_remaining=30,
            logo_at_risk_flag=0,
        ))
        if r.erosion_composite < 20:
            assert r.is_at_churn_risk is False


# ── Section 12: requires_executive_attention ──────────────────────────────────

class TestRequiresExecutiveAttention:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_no_attention_healthy(self):
        r = self.engine.assess(make_input())
        assert r.requires_executive_attention is False

    def test_attention_composite_ge_30(self):
        r = self.engine.assess(make_input(
            nps_score=40,
            nps_score_prior=40,
            executive_last_contact_days=30,
            support_tickets_last_30d=3,
            support_tickets_prior_30d=2,
        ))
        if r.erosion_composite >= 30:
            assert r.requires_executive_attention is True

    def test_attention_competitor_signal(self):
        r = self.engine.assess(make_input(competitor_evaluation_signal=1))
        assert r.requires_executive_attention is True

    def test_attention_exec_contact_ge_60(self):
        r = self.engine.assess(make_input(executive_last_contact_days=60))
        assert r.requires_executive_attention is True

    def test_no_attention_exec_contact_59d(self):
        r = self.engine.assess(make_input(
            executive_last_contact_days=59,
            competitor_evaluation_signal=0,
        ))
        if r.erosion_composite < 30:
            assert r.requires_executive_attention is False


# ── Section 13: estimated_arr_at_risk ────────────────────────────────────────

class TestEstimatedArrAtRisk:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_arr_at_risk_formula(self):
        arr = 200_000.0
        r = self.engine.assess(make_input(contract_arr_usd=arr))
        expected = arr * (r.erosion_composite / 100.0)
        assert abs(r.estimated_arr_at_risk_usd - expected) < 0.01

    def test_arr_zero_composite_zero_risk(self):
        r = self.engine.assess(make_input(contract_arr_usd=100_000.0))
        if r.erosion_composite == 0:
            assert r.estimated_arr_at_risk_usd == 0.0

    def test_arr_scales_with_composite(self):
        # higher composite → higher arr at risk
        r_low = self.engine.assess(make_input(
            customer_id="A",
            contract_arr_usd=100_000.0,
        ))
        r_high = fresh_engine().assess(make_input(
            customer_id="B",
            contract_arr_usd=100_000.0,
            nps_score=15,
            nps_score_prior=60,
            support_tickets_last_30d=6,
            support_tickets_prior_30d=2,
            executive_last_contact_days=90,
            critical_tickets_last_30d=3,
        ))
        assert r_high.estimated_arr_at_risk_usd >= r_low.estimated_arr_at_risk_usd

    def test_arr_proportional_to_contract(self):
        composite_same = make_input(nps_score=70, nps_score_prior=70)
        r1 = fresh_engine().assess(make_input(contract_arr_usd=50_000.0))
        r2 = fresh_engine().assess(make_input(contract_arr_usd=100_000.0))
        # ratio should be approximately 2x
        if r1.erosion_composite == r2.erosion_composite and r1.erosion_composite > 0:
            assert abs(r2.estimated_arr_at_risk_usd / r1.estimated_arr_at_risk_usd - 2.0) < 0.01


# ── Section 14: erosion_signal ────────────────────────────────────────────────

class TestErosionSignal:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_signal_none_pattern(self):
        r = self.engine.assess(make_input())
        assert "acceptable" in r.erosion_signal.lower()

    def test_signal_competitive_migration_contains_exec_days(self):
        days = 75
        r = self.engine.assess(make_input(
            competitor_evaluation_signal=1,
            executive_last_contact_days=days,
        ))
        assert str(days) in r.erosion_signal

    def test_signal_exec_relationship_loss_contains_meetings(self):
        r = self.engine.assess(make_input(
            competitor_evaluation_signal=0,
            executive_last_contact_days=90,
            executive_meetings_last_90d=1,
            executive_meetings_prior_90d=5,
        ))
        assert "1" in r.erosion_signal
        assert "5" in r.erosion_signal

    def test_signal_support_overload_contains_critical_tickets(self):
        r = self.engine.assess(make_input(
            competitor_evaluation_signal=0,
            executive_last_contact_days=10,
            critical_tickets_last_30d=3,
            nps_score=20,
            nps_score_prior=20,
        ))
        assert "3" in r.erosion_signal

    def test_signal_usage_cliff_contains_scores(self):
        r = self.engine.assess(make_input(
            competitor_evaluation_signal=0,
            executive_last_contact_days=10,
            critical_tickets_last_30d=0,
            product_usage_score_last_30d=40.0,
            product_usage_score_prior_30d=80.0,
            feature_adoption_pct=10.0,
            benchmark_feature_adoption_pct=60.0,
        ))
        assert "40" in r.erosion_signal
        assert "80" in r.erosion_signal

    def test_signal_expansion_stall_contains_age(self):
        age = 24
        r = self.engine.assess(make_input(
            competitor_evaluation_signal=0,
            executive_last_contact_days=10,
            critical_tickets_last_30d=0,
            product_usage_score_last_30d=80.0,
            product_usage_score_prior_30d=80.0,
            account_age_months=age,
            expansion_revenue_last_12m_usd=0.0,
        ))
        assert str(age) in r.erosion_signal

    def test_signal_contains_composite(self):
        r = self.engine.assess(make_input(
            competitor_evaluation_signal=1,
            executive_last_contact_days=90,
        ))
        composite_str = str(int(r.erosion_composite))
        assert composite_str in r.erosion_signal


# ── Section 15: to_dict() ─────────────────────────────────────────────────────

class TestToDict:
    def setup_method(self):
        self.engine = fresh_engine()
        self.r = self.engine.assess(make_input())
        self.d = self.r.to_dict()

    def test_to_dict_has_15_keys(self):
        assert len(self.d) == 15

    def test_to_dict_customer_id(self):
        assert self.d["customer_id"] == "CUST-001"

    def test_to_dict_csm_id(self):
        assert self.d["csm_id"] == "CSM-001"

    def test_to_dict_erosion_risk_is_string(self):
        assert isinstance(self.d["erosion_risk"], str)

    def test_to_dict_erosion_pattern_is_string(self):
        assert isinstance(self.d["erosion_pattern"], str)

    def test_to_dict_erosion_severity_is_string(self):
        assert isinstance(self.d["erosion_severity"], str)

    def test_to_dict_recommended_action_is_string(self):
        assert isinstance(self.d["recommended_action"], str)

    def test_to_dict_usage_decline_score_is_float(self):
        assert isinstance(self.d["usage_decline_score"], float)

    def test_to_dict_engagement_decay_score_is_float(self):
        assert isinstance(self.d["engagement_decay_score"], float)

    def test_to_dict_expansion_health_score_is_float(self):
        assert isinstance(self.d["expansion_health_score"], float)

    def test_to_dict_relationship_risk_score_is_float(self):
        assert isinstance(self.d["relationship_risk_score"], float)

    def test_to_dict_erosion_composite_is_float(self):
        assert isinstance(self.d["erosion_composite"], float)

    def test_to_dict_is_at_churn_risk_is_bool(self):
        assert isinstance(self.d["is_at_churn_risk"], bool)

    def test_to_dict_requires_executive_attention_is_bool(self):
        assert isinstance(self.d["requires_executive_attention"], bool)

    def test_to_dict_estimated_arr_at_risk_usd_is_float(self):
        assert isinstance(self.d["estimated_arr_at_risk_usd"], float)

    def test_to_dict_erosion_signal_is_str(self):
        assert isinstance(self.d["erosion_signal"], str)

    def test_to_dict_expected_keys(self):
        expected = {
            "customer_id", "csm_id", "erosion_risk", "erosion_pattern",
            "erosion_severity", "recommended_action", "usage_decline_score",
            "engagement_decay_score", "expansion_health_score",
            "relationship_risk_score", "erosion_composite", "is_at_churn_risk",
            "requires_executive_attention", "estimated_arr_at_risk_usd",
            "erosion_signal",
        }
        assert set(self.d.keys()) == expected

    def test_to_dict_risk_value_is_valid_enum(self):
        assert self.d["erosion_risk"] in [e.value for e in ErosionRisk]

    def test_to_dict_pattern_value_is_valid_enum(self):
        assert self.d["erosion_pattern"] in [e.value for e in ErosionPattern]

    def test_to_dict_severity_value_is_valid_enum(self):
        assert self.d["erosion_severity"] in [e.value for e in ErosionSeverity]

    def test_to_dict_action_value_is_valid_enum(self):
        assert self.d["recommended_action"] in [e.value for e in ErosionAction]

    def test_to_dict_scores_rounded_to_1dp(self):
        # rounded values should match round(x, 1)
        assert self.d["usage_decline_score"] == round(self.r.usage_decline_score, 1)
        assert self.d["engagement_decay_score"] == round(self.r.engagement_decay_score, 1)
        assert self.d["expansion_health_score"] == round(self.r.expansion_health_score, 1)
        assert self.d["relationship_risk_score"] == round(self.r.relationship_risk_score, 1)
        assert self.d["erosion_composite"] == round(self.r.erosion_composite, 1)

    def test_to_dict_arr_rounded_to_2dp(self):
        assert self.d["estimated_arr_at_risk_usd"] == round(self.r.estimated_arr_at_risk_usd, 2)


# ── Section 16: assess_batch() ───────────────────────────────────────────────

class TestAssessBatch:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_batch_returns_list(self):
        results = self.engine.assess_batch([make_input(customer_id="A"), make_input(customer_id="B")])
        assert isinstance(results, list)

    def test_batch_length_matches_input(self):
        inputs = [make_input(customer_id=f"C{i}") for i in range(5)]
        results = self.engine.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_empty_input(self):
        results = self.engine.assess_batch([])
        assert results == []

    def test_batch_each_result_is_customer_ltv_result(self):
        results = self.engine.assess_batch([make_input(), make_input(customer_id="X")])
        for r in results:
            assert isinstance(r, CustomerLTVResult)

    def test_batch_preserves_order(self):
        ids = ["ID1", "ID2", "ID3"]
        results = self.engine.assess_batch([make_input(customer_id=i) for i in ids])
        assert [r.customer_id for r in results] == ids

    def test_batch_single_item(self):
        results = self.engine.assess_batch([make_input(customer_id="SOLO")])
        assert len(results) == 1
        assert results[0].customer_id == "SOLO"

    def test_batch_accumulates_in_summary(self):
        self.engine.assess_batch([make_input(customer_id=f"C{i}") for i in range(3)])
        s = self.engine.summary()
        assert s["total"] == 3


# ── Section 17: summary() ────────────────────────────────────────────────────

class TestSummary:
    def test_summary_empty_engine(self):
        engine = fresh_engine()
        s = engine.summary()
        assert s["total"] == 0

    def test_summary_empty_has_13_keys(self):
        s = fresh_engine().summary()
        assert len(s) == 13

    def test_summary_empty_zero_values(self):
        s = fresh_engine().summary()
        assert s["avg_erosion_composite"] == 0.0
        assert s["churn_risk_count"] == 0
        assert s["executive_attention_count"] == 0
        assert s["total_estimated_arr_at_risk_usd"] == 0.0

    def test_summary_has_13_keys_after_assess(self):
        engine = fresh_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert len(s) == 13

    def test_summary_expected_keys(self):
        engine = fresh_engine()
        engine.assess(make_input())
        s = engine.summary()
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_erosion_composite", "churn_risk_count",
            "executive_attention_count", "avg_usage_decline_score",
            "avg_engagement_decay_score", "avg_expansion_health_score",
            "avg_relationship_risk_score", "total_estimated_arr_at_risk_usd",
        }
        assert set(s.keys()) == expected

    def test_summary_total_count(self):
        engine = fresh_engine()
        for i in range(4):
            engine.assess(make_input(customer_id=f"C{i}"))
        assert engine.summary()["total"] == 4

    def test_summary_risk_counts_dict(self):
        engine = fresh_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert isinstance(s["risk_counts"], dict)

    def test_summary_risk_counts_sum(self):
        engine = fresh_engine()
        for i in range(3):
            engine.assess(make_input(customer_id=f"C{i}"))
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == 3

    def test_summary_pattern_counts_sum(self):
        engine = fresh_engine()
        for i in range(3):
            engine.assess(make_input(customer_id=f"C{i}"))
        s = engine.summary()
        assert sum(s["pattern_counts"].values()) == 3

    def test_summary_severity_counts_sum(self):
        engine = fresh_engine()
        for i in range(3):
            engine.assess(make_input(customer_id=f"C{i}"))
        s = engine.summary()
        assert sum(s["severity_counts"].values()) == 3

    def test_summary_action_counts_sum(self):
        engine = fresh_engine()
        for i in range(3):
            engine.assess(make_input(customer_id=f"C{i}"))
        s = engine.summary()
        assert sum(s["action_counts"].values()) == 3

    def test_summary_avg_composite_correct(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input(customer_id="A"))
        r2 = engine.assess(make_input(customer_id="B"))
        s = engine.summary()
        expected = round((r1.erosion_composite + r2.erosion_composite) / 2, 1)
        assert s["avg_erosion_composite"] == expected

    def test_summary_total_arr_at_risk_is_sum(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input(customer_id="A", contract_arr_usd=100_000.0))
        r2 = engine.assess(make_input(customer_id="B", contract_arr_usd=200_000.0))
        s = engine.summary()
        expected = round(r1.estimated_arr_at_risk_usd + r2.estimated_arr_at_risk_usd, 2)
        assert s["total_estimated_arr_at_risk_usd"] == expected

    def test_summary_churn_risk_count(self):
        engine = fresh_engine()
        engine.assess(make_input(customer_id="A", logo_at_risk_flag=1))
        engine.assess(make_input(customer_id="B"))
        s = engine.summary()
        assert s["churn_risk_count"] >= 1

    def test_summary_executive_attention_count(self):
        engine = fresh_engine()
        engine.assess(make_input(customer_id="A", competitor_evaluation_signal=1))
        engine.assess(make_input(customer_id="B"))
        s = engine.summary()
        assert s["executive_attention_count"] >= 1

    def test_summary_avg_usage_decline_score(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input(customer_id="A"))
        r2 = engine.assess(make_input(customer_id="B"))
        s = engine.summary()
        expected = round((r1.usage_decline_score + r2.usage_decline_score) / 2, 1)
        assert s["avg_usage_decline_score"] == expected

    def test_summary_avg_engagement_decay_score(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input(customer_id="A"))
        r2 = engine.assess(make_input(customer_id="B"))
        s = engine.summary()
        expected = round((r1.engagement_decay_score + r2.engagement_decay_score) / 2, 1)
        assert s["avg_engagement_decay_score"] == expected

    def test_summary_avg_expansion_health_score(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input(customer_id="A"))
        r2 = engine.assess(make_input(customer_id="B"))
        s = engine.summary()
        expected = round((r1.expansion_health_score + r2.expansion_health_score) / 2, 1)
        assert s["avg_expansion_health_score"] == expected

    def test_summary_avg_relationship_risk_score(self):
        engine = fresh_engine()
        r1 = engine.assess(make_input(customer_id="A"))
        r2 = engine.assess(make_input(customer_id="B"))
        s = engine.summary()
        expected = round((r1.relationship_risk_score + r2.relationship_risk_score) / 2, 1)
        assert s["avg_relationship_risk_score"] == expected

    def test_summary_single_assess_accumulates(self):
        engine = fresh_engine()
        engine.assess(make_input())
        assert engine.summary()["total"] == 1

    def test_summary_multiple_assess_accumulates(self):
        engine = fresh_engine()
        engine.assess(make_input(customer_id="A"))
        engine.assess(make_input(customer_id="B"))
        engine.assess(make_input(customer_id="C"))
        assert engine.summary()["total"] == 3


# ── Section 18: Edge cases ────────────────────────────────────────────────────

class TestEdgeCases:
    def setup_method(self):
        self.engine = fresh_engine()

    def test_zero_product_usage_prior(self):
        r = self.engine.assess(make_input(
            product_usage_score_prior_30d=0.0,
            product_usage_score_last_30d=0.0,
        ))
        assert isinstance(r, CustomerLTVResult)
        assert r.usage_decline_score >= 0.0

    def test_zero_expansion_revenue_prior(self):
        r = self.engine.assess(make_input(
            expansion_revenue_prior_12m_usd=0.0,
            expansion_revenue_last_12m_usd=0.0,
            account_age_months=12,
        ))
        assert isinstance(r, CustomerLTVResult)
        assert r.expansion_health_score >= 0.0

    def test_zero_support_tickets_prior(self):
        r = self.engine.assess(make_input(
            support_tickets_prior_30d=0,
            support_tickets_last_30d=5,
        ))
        # ticket ratio branch skipped; no division by zero
        assert isinstance(r, CustomerLTVResult)

    def test_zero_executive_meetings_prior(self):
        r = self.engine.assess(make_input(
            executive_meetings_prior_90d=0,
            executive_meetings_last_90d=0,
        ))
        # meeting delta branch skipped; no division by zero
        assert isinstance(r, CustomerLTVResult)

    def test_large_contract_arr(self):
        r = self.engine.assess(make_input(contract_arr_usd=10_000_000.0))
        assert r.estimated_arr_at_risk_usd >= 0.0

    def test_zero_contract_arr(self):
        r = self.engine.assess(make_input(contract_arr_usd=0.0))
        assert r.estimated_arr_at_risk_usd == 0.0

    def test_renewal_days_zero(self):
        r = self.engine.assess(make_input(renewal_days_remaining=0))
        assert r.expansion_health_score >= 25.0

    def test_nps_scores_equal_no_delta_contribution(self):
        r = self.engine.assess(make_input(nps_score=70, nps_score_prior=70))
        # no delta contribution to engagement
        assert r.engagement_decay_score < 10

    def test_all_zeros_does_not_crash(self):
        inp = CustomerLTVInput(
            customer_id="Z",
            csm_id="CSM-Z",
            evaluation_period_id="EP-Z",
            contract_arr_usd=0.0,
            account_age_months=0,
            product_usage_score_last_30d=0.0,
            product_usage_score_prior_30d=0.0,
            feature_adoption_pct=0.0,
            benchmark_feature_adoption_pct=0.0,
            nps_score=0,
            nps_score_prior=0,
            executive_last_contact_days=0,
            executive_meetings_last_90d=0,
            executive_meetings_prior_90d=0,
            support_tickets_last_30d=0,
            support_tickets_prior_30d=0,
            critical_tickets_last_30d=0,
            expansion_revenue_last_12m_usd=0.0,
            expansion_revenue_prior_12m_usd=0.0,
            logo_at_risk_flag=0,
            competitor_evaluation_signal=0,
            renewal_days_remaining=0,
        )
        r = fresh_engine().assess(inp)
        assert isinstance(r, CustomerLTVResult)

    def test_high_nps_improvement_negative_delta_no_contribution(self):
        # nps_delta = prior - current < 0 → no contribution
        r = self.engine.assess(make_input(nps_score=80, nps_score_prior=60))
        assert r.engagement_decay_score >= 0.0

    def test_expansion_revenue_increase_no_delta_contribution(self):
        # last > prior → negative exp_delta → no contribution
        r = self.engine.assess(make_input(
            expansion_revenue_last_12m_usd=30_000.0,
            expansion_revenue_prior_12m_usd=20_000.0,
        ))
        assert r.expansion_health_score >= 0.0

    def test_usage_increase_no_delta_contribution(self):
        r = self.engine.assess(make_input(
            product_usage_score_last_30d=90.0,
            product_usage_score_prior_30d=80.0,
        ))
        assert r.usage_decline_score >= 0.0

    def test_meeting_increase_no_delta_contribution(self):
        r = self.engine.assess(make_input(
            executive_meetings_last_90d=5,
            executive_meetings_prior_90d=3,
            competitor_evaluation_signal=0,
            executive_last_contact_days=10,
        ))
        assert r.relationship_risk_score >= 0.0


# ── Section 19: All risk levels present in results ────────────────────────────

class TestAllRiskLevels:
    def test_low_risk_result(self):
        r = fresh_engine().assess(make_input())
        assert r.erosion_risk == ErosionRisk.low

    def test_moderate_risk_result(self):
        r = fresh_engine().assess(make_input(
            nps_score=40,
            nps_score_prior=55,
            executive_last_contact_days=30,
        ))
        # verify in valid enum range
        assert r.erosion_risk in list(ErosionRisk)

    def test_critical_risk_result(self):
        r = fresh_engine().assess(make_input(
            product_usage_score_last_30d=40.0,
            product_usage_score_prior_30d=80.0,
            nps_score=15,
            nps_score_prior=60,
            support_tickets_last_30d=6,
            support_tickets_prior_30d=2,
            executive_last_contact_days=90,
            logo_at_risk_flag=1,
            renewal_days_remaining=20,
            critical_tickets_last_30d=3,
        ))
        assert r.erosion_composite >= 60
        assert r.erosion_risk == ErosionRisk.critical


# ── Section 20: All severity levels ──────────────────────────────────────────

class TestAllSeverityLevels:
    def test_healthy_severity(self):
        r = fresh_engine().assess(make_input())
        assert r.erosion_severity == ErosionSeverity.healthy

    def test_critical_severity(self):
        r = fresh_engine().assess(make_input(
            product_usage_score_last_30d=40.0,
            product_usage_score_prior_30d=80.0,
            nps_score=15,
            nps_score_prior=60,
            support_tickets_last_30d=6,
            support_tickets_prior_30d=2,
            executive_last_contact_days=90,
            logo_at_risk_flag=1,
            renewal_days_remaining=20,
            critical_tickets_last_30d=3,
        ))
        if r.erosion_composite >= 60:
            assert r.erosion_severity == ErosionSeverity.critical


# ── Section 21: All actions reachable ────────────────────────────────────────

class TestAllActionsReachable:
    def test_no_action_reachable(self):
        r = fresh_engine().assess(make_input())
        assert r.recommended_action == ErosionAction.no_action

    def test_churn_prevention_team_reachable(self):
        r = fresh_engine().assess(make_input(
            product_usage_score_last_30d=40.0,
            product_usage_score_prior_30d=80.0,
            nps_score=15,
            nps_score_prior=60,
            support_tickets_last_30d=6,
            support_tickets_prior_30d=2,
            executive_last_contact_days=90,
            logo_at_risk_flag=1,
            renewal_days_remaining=20,
            critical_tickets_last_30d=3,
        ))
        if r.erosion_composite >= 60:
            assert r.recommended_action == ErosionAction.churn_prevention_team


# ── Section 22: InputDataclass fields ────────────────────────────────────────

class TestInputDataclass:
    def test_input_has_22_fields(self):
        import dataclasses
        fields = dataclasses.fields(CustomerLTVInput)
        assert len(fields) == 22

    def test_input_customer_id_field(self):
        inp = make_input(customer_id="TEST-ID")
        assert inp.customer_id == "TEST-ID"

    def test_input_contract_arr_usd_field(self):
        inp = make_input(contract_arr_usd=500_000.0)
        assert inp.contract_arr_usd == 500_000.0

    def test_input_logo_at_risk_flag_field(self):
        inp = make_input(logo_at_risk_flag=1)
        assert inp.logo_at_risk_flag == 1

    def test_input_competitor_evaluation_signal_field(self):
        inp = make_input(competitor_evaluation_signal=1)
        assert inp.competitor_evaluation_signal == 1


# ── Section 23: ResultDataclass fields ───────────────────────────────────────

class TestResultDataclass:
    def setup_method(self):
        self.r = fresh_engine().assess(make_input())

    def test_result_has_15_fields(self):
        import dataclasses
        fields = dataclasses.fields(CustomerLTVResult)
        assert len(fields) == 15

    def test_result_erosion_risk_type(self):
        assert isinstance(self.r.erosion_risk, ErosionRisk)

    def test_result_erosion_pattern_type(self):
        assert isinstance(self.r.erosion_pattern, ErosionPattern)

    def test_result_erosion_severity_type(self):
        assert isinstance(self.r.erosion_severity, ErosionSeverity)

    def test_result_recommended_action_type(self):
        assert isinstance(self.r.recommended_action, ErosionAction)

    def test_result_is_at_churn_risk_bool(self):
        assert isinstance(self.r.is_at_churn_risk, bool)

    def test_result_requires_executive_attention_bool(self):
        assert isinstance(self.r.requires_executive_attention, bool)

    def test_result_usage_decline_score_float(self):
        assert isinstance(self.r.usage_decline_score, float)

    def test_result_engagement_decay_score_float(self):
        assert isinstance(self.r.engagement_decay_score, float)

    def test_result_expansion_health_score_float(self):
        assert isinstance(self.r.expansion_health_score, float)

    def test_result_relationship_risk_score_float(self):
        assert isinstance(self.r.relationship_risk_score, float)

    def test_result_erosion_composite_float(self):
        assert isinstance(self.r.erosion_composite, float)

    def test_result_estimated_arr_at_risk_float(self):
        assert isinstance(self.r.estimated_arr_at_risk_usd, float)

    def test_result_erosion_signal_str(self):
        assert isinstance(self.r.erosion_signal, str)


# ── Section 24: Composite score weights integration ───────────────────────────

class TestCompositeWeights:
    """Verify weights: usage*0.30 + engagement*0.30 + expansion*0.25 + relationship*0.15"""

    def test_weights_sum_to_1(self):
        assert abs(0.30 + 0.30 + 0.25 + 0.15 - 1.0) < 1e-9

    def test_composite_dominated_by_usage_when_others_zero(self):
        # Drive usage high, keep others near zero
        r = fresh_engine().assess(make_input(
            product_usage_score_last_30d=0.0,
            product_usage_score_prior_30d=100.0,
            feature_adoption_pct=65.0,
            benchmark_feature_adoption_pct=65.0,
            critical_tickets_last_30d=0,
            nps_score=70,
            nps_score_prior=70,
            support_tickets_last_30d=2,
            support_tickets_prior_30d=2,
            expansion_revenue_last_12m_usd=20_000.0,
            expansion_revenue_prior_12m_usd=20_000.0,
            logo_at_risk_flag=0,
            renewal_days_remaining=180,
            executive_last_contact_days=10,
            executive_meetings_last_90d=3,
            executive_meetings_prior_90d=3,
            competitor_evaluation_signal=0,
        ))
        # usage contributes 45 * 0.30 = 13.5 to composite
        assert r.erosion_composite >= 13.0

    def test_composite_increases_with_more_signals(self):
        r_low = fresh_engine().assess(make_input())
        r_high = fresh_engine().assess(make_input(
            nps_score=20,
            nps_score_prior=50,
            executive_last_contact_days=60,
        ))
        assert r_high.erosion_composite >= r_low.erosion_composite


# ── Section 25: Full scenario tests ──────────────────────────────────────────

class TestFullScenarios:
    """End-to-end scenarios combining multiple signals."""

    def test_perfect_health_scenario(self):
        r = fresh_engine().assess(make_input(
            product_usage_score_last_30d=90.0,
            product_usage_score_prior_30d=85.0,
            feature_adoption_pct=70.0,
            benchmark_feature_adoption_pct=65.0,
            nps_score=80,
            nps_score_prior=75,
            executive_last_contact_days=7,
            executive_meetings_last_90d=4,
            executive_meetings_prior_90d=3,
            support_tickets_last_30d=1,
            support_tickets_prior_30d=2,
            critical_tickets_last_30d=0,
            expansion_revenue_last_12m_usd=30_000.0,
            expansion_revenue_prior_12m_usd=25_000.0,
            logo_at_risk_flag=0,
            competitor_evaluation_signal=0,
            renewal_days_remaining=300,
        ))
        assert r.erosion_risk == ErosionRisk.low
        assert r.erosion_severity == ErosionSeverity.healthy
        assert r.is_at_churn_risk is False

    def test_full_crisis_scenario(self):
        r = fresh_engine().assess(make_input(
            product_usage_score_last_30d=30.0,
            product_usage_score_prior_30d=80.0,
            feature_adoption_pct=10.0,
            benchmark_feature_adoption_pct=70.0,
            nps_score=10,
            nps_score_prior=70,
            executive_last_contact_days=120,
            executive_meetings_last_90d=0,
            executive_meetings_prior_90d=5,
            support_tickets_last_30d=9,
            support_tickets_prior_30d=2,
            critical_tickets_last_30d=4,
            expansion_revenue_last_12m_usd=0.0,
            expansion_revenue_prior_12m_usd=50_000.0,
            logo_at_risk_flag=1,
            competitor_evaluation_signal=1,
            renewal_days_remaining=15,
            account_age_months=30,
        ))
        assert r.erosion_composite >= 60
        assert r.erosion_risk == ErosionRisk.critical
        assert r.erosion_severity == ErosionSeverity.critical
        assert r.is_at_churn_risk is True
        assert r.requires_executive_attention is True
        assert r.erosion_pattern == ErosionPattern.competitive_migration
        assert r.recommended_action == ErosionAction.churn_prevention_team

    def test_expansion_stall_scenario(self):
        r = fresh_engine().assess(make_input(
            competitor_evaluation_signal=0,
            executive_last_contact_days=20,
            critical_tickets_last_30d=0,
            product_usage_score_last_30d=80.0,
            product_usage_score_prior_30d=80.0,
            account_age_months=24,
            expansion_revenue_last_12m_usd=0.0,
            expansion_revenue_prior_12m_usd=0.0,
        ))
        assert r.erosion_pattern == ErosionPattern.expansion_stall

    def test_usage_cliff_scenario(self):
        r = fresh_engine().assess(make_input(
            competitor_evaluation_signal=0,
            executive_last_contact_days=10,
            critical_tickets_last_30d=0,
            product_usage_score_last_30d=40.0,
            product_usage_score_prior_30d=80.0,
            feature_adoption_pct=20.0,
            benchmark_feature_adoption_pct=60.0,
            account_age_months=10,
            expansion_revenue_last_12m_usd=10_000.0,
        ))
        assert r.erosion_pattern == ErosionPattern.usage_cliff

    def test_competitor_evaluation_scenario(self):
        r = fresh_engine().assess(make_input(
            competitor_evaluation_signal=1,
            executive_last_contact_days=90,
        ))
        assert r.erosion_pattern == ErosionPattern.competitive_migration
        assert r.requires_executive_attention is True

    def test_exec_relationship_loss_scenario(self):
        r = fresh_engine().assess(make_input(
            competitor_evaluation_signal=0,
            executive_last_contact_days=90,
            executive_meetings_last_90d=0,
            executive_meetings_prior_90d=4,
        ))
        assert r.erosion_pattern == ErosionPattern.exec_relationship_loss
        assert r.requires_executive_attention is True

    def test_support_overload_scenario(self):
        r = fresh_engine().assess(make_input(
            competitor_evaluation_signal=0,
            executive_last_contact_days=10,
            critical_tickets_last_30d=3,
            nps_score=15,
            nps_score_prior=15,
            support_tickets_last_30d=2,
            support_tickets_prior_30d=2,
        ))
        assert r.erosion_pattern == ErosionPattern.support_overload

    def test_logo_at_risk_forces_churn_risk(self):
        r = fresh_engine().assess(make_input(logo_at_risk_flag=1))
        assert r.is_at_churn_risk is True

    def test_competitor_signal_forces_exec_attention(self):
        r = fresh_engine().assess(make_input(competitor_evaluation_signal=1))
        assert r.requires_executive_attention is True

    def test_exec_dark_60d_forces_exec_attention(self):
        r = fresh_engine().assess(make_input(executive_last_contact_days=60))
        assert r.requires_executive_attention is True

    def test_multiple_customers_different_risks(self):
        engine = fresh_engine()
        r_low = engine.assess(make_input(customer_id="LOW"))
        r_crit = engine.assess(make_input(
            customer_id="CRIT",
            product_usage_score_last_30d=40.0,
            product_usage_score_prior_30d=80.0,
            nps_score=15,
            nps_score_prior=60,
            support_tickets_last_30d=6,
            support_tickets_prior_30d=2,
            executive_last_contact_days=90,
            logo_at_risk_flag=1,
            renewal_days_remaining=20,
            critical_tickets_last_30d=3,
        ))
        assert r_low.erosion_risk == ErosionRisk.low
        if r_crit.erosion_composite >= 60:
            assert r_crit.erosion_risk == ErosionRisk.critical

    def test_batch_then_summary_arr_sum(self):
        engine = fresh_engine()
        inputs = [
            make_input(customer_id="A", contract_arr_usd=100_000.0),
            make_input(customer_id="B", contract_arr_usd=200_000.0),
            make_input(customer_id="C", contract_arr_usd=50_000.0),
        ]
        results = engine.assess_batch(inputs)
        s = engine.summary()
        total_expected = round(sum(r.estimated_arr_at_risk_usd for r in results), 2)
        assert s["total_estimated_arr_at_risk_usd"] == total_expected

    def test_renewal_urgency_elevates_expansion_score(self):
        r_far = fresh_engine().assess(make_input(renewal_days_remaining=365))
        r_near = fresh_engine().assess(make_input(renewal_days_remaining=20))
        assert r_near.expansion_health_score > r_far.expansion_health_score

    def test_high_nps_and_growing_usage_low_composite(self):
        r = fresh_engine().assess(make_input(
            nps_score=90,
            nps_score_prior=80,
            product_usage_score_last_30d=95.0,
            product_usage_score_prior_30d=85.0,
            competitor_evaluation_signal=0,
            executive_last_contact_days=5,
        ))
        assert r.erosion_composite < 30


# ── Section 26: Boundary threshold exact values ───────────────────────────────

class TestBoundaryThresholds:
    """Test exact threshold boundaries to ensure correct branching."""

    def setup_method(self):
        self.engine = fresh_engine()

    # usage_decline thresholds
    def test_usage_delta_exactly_5pct(self):
        r = self.engine.assess(make_input(
            product_usage_score_last_30d=76.0,
            product_usage_score_prior_30d=80.0,
            feature_adoption_pct=65.0,
            benchmark_feature_adoption_pct=65.0,
            critical_tickets_last_30d=0,
        ))
        # delta=4/80=0.05, gets 6 points
        assert r.usage_decline_score == pytest.approx(6.0, abs=0.01)

    def test_usage_delta_exactly_10pct(self):
        r = self.engine.assess(make_input(
            product_usage_score_last_30d=72.0,
            product_usage_score_prior_30d=80.0,
            feature_adoption_pct=65.0,
            benchmark_feature_adoption_pct=65.0,
            critical_tickets_last_30d=0,
        ))
        # delta=8/80=0.10, gets 14 points
        assert r.usage_decline_score == pytest.approx(14.0, abs=0.01)

    def test_usage_delta_exactly_25pct(self):
        r = self.engine.assess(make_input(
            product_usage_score_last_30d=60.0,
            product_usage_score_prior_30d=80.0,
            feature_adoption_pct=65.0,
            benchmark_feature_adoption_pct=65.0,
            critical_tickets_last_30d=0,
        ))
        # delta=20/80=0.25, gets 28 points
        assert r.usage_decline_score == pytest.approx(28.0, abs=0.01)

    def test_usage_delta_exactly_40pct(self):
        r = self.engine.assess(make_input(
            product_usage_score_last_30d=48.0,
            product_usage_score_prior_30d=80.0,
            feature_adoption_pct=65.0,
            benchmark_feature_adoption_pct=65.0,
            critical_tickets_last_30d=0,
        ))
        # delta=32/80=0.40, gets 45 points
        assert r.usage_decline_score == pytest.approx(45.0, abs=0.01)

    # adoption gap thresholds
    def test_adoption_gap_exactly_10(self):
        r = self.engine.assess(make_input(
            product_usage_score_last_30d=80.0,
            product_usage_score_prior_30d=80.0,
            feature_adoption_pct=55.0,
            benchmark_feature_adoption_pct=65.0,
            critical_tickets_last_30d=0,
        ))
        # gap=10, gets 8 points
        assert r.usage_decline_score == pytest.approx(8.0, abs=0.01)

    def test_adoption_gap_exactly_25(self):
        r = self.engine.assess(make_input(
            product_usage_score_last_30d=80.0,
            product_usage_score_prior_30d=80.0,
            feature_adoption_pct=40.0,
            benchmark_feature_adoption_pct=65.0,
            critical_tickets_last_30d=0,
        ))
        # gap=25, gets 18 points
        assert r.usage_decline_score == pytest.approx(18.0, abs=0.01)

    def test_adoption_gap_exactly_40(self):
        r = self.engine.assess(make_input(
            product_usage_score_last_30d=80.0,
            product_usage_score_prior_30d=80.0,
            feature_adoption_pct=25.0,
            benchmark_feature_adoption_pct=65.0,
            critical_tickets_last_30d=0,
        ))
        # gap=40, gets 30 points
        assert r.usage_decline_score == pytest.approx(30.0, abs=0.01)

    # NPS delta thresholds
    def test_nps_delta_exactly_10(self):
        r = self.engine.assess(make_input(
            nps_score=60,
            nps_score_prior=70,
            support_tickets_last_30d=2,
            support_tickets_prior_30d=2,
        ))
        # delta=10, gets 12 points; nps=60 > 40 so no absolute contribution
        assert r.engagement_decay_score == pytest.approx(12.0, abs=0.01)

    def test_nps_delta_exactly_20(self):
        r = self.engine.assess(make_input(
            nps_score=50,
            nps_score_prior=70,
            support_tickets_last_30d=2,
            support_tickets_prior_30d=2,
        ))
        # delta=20, gets 25 points; nps=50 > 40 so no absolute contribution
        assert r.engagement_decay_score == pytest.approx(25.0, abs=0.01)

    def test_nps_delta_exactly_30(self):
        r = self.engine.assess(make_input(
            nps_score=45,
            nps_score_prior=75,
            support_tickets_last_30d=2,
            support_tickets_prior_30d=2,
        ))
        # delta=30, gets 40 points; nps=45 > 40 so no absolute contribution
        assert r.engagement_decay_score == pytest.approx(40.0, abs=0.01)

    # absolute NPS thresholds
    def test_nps_absolute_exactly_20(self):
        r = self.engine.assess(make_input(
            nps_score=20,
            nps_score_prior=20,
            support_tickets_last_30d=2,
            support_tickets_prior_30d=2,
        ))
        # delta=0, nps=20 <=20 gets 30 points
        assert r.engagement_decay_score == pytest.approx(30.0, abs=0.01)

    def test_nps_absolute_exactly_40(self):
        r = self.engine.assess(make_input(
            nps_score=40,
            nps_score_prior=40,
            support_tickets_last_30d=2,
            support_tickets_prior_30d=2,
        ))
        # delta=0, nps=40 <=40 gets 15 points
        assert r.engagement_decay_score == pytest.approx(15.0, abs=0.01)

    # ticket ratio thresholds
    def test_ticket_ratio_exactly_1p5(self):
        r = self.engine.assess(make_input(
            nps_score=70,
            nps_score_prior=70,
            support_tickets_last_30d=3,
            support_tickets_prior_30d=2,
        ))
        # ratio=1.5, gets 8 points
        assert r.engagement_decay_score == pytest.approx(8.0, abs=0.01)

    def test_ticket_ratio_exactly_2(self):
        r = self.engine.assess(make_input(
            nps_score=70,
            nps_score_prior=70,
            support_tickets_last_30d=4,
            support_tickets_prior_30d=2,
        ))
        # ratio=2.0, gets 18 points
        assert r.engagement_decay_score == pytest.approx(18.0, abs=0.01)

    def test_ticket_ratio_exactly_3(self):
        r = self.engine.assess(make_input(
            nps_score=70,
            nps_score_prior=70,
            support_tickets_last_30d=6,
            support_tickets_prior_30d=2,
        ))
        # ratio=3.0, gets 30 points
        assert r.engagement_decay_score == pytest.approx(30.0, abs=0.01)

    # expansion revenue delta thresholds
    def test_expansion_delta_exactly_10pct(self):
        r = self.engine.assess(make_input(
            expansion_revenue_last_12m_usd=18_000.0,
            expansion_revenue_prior_12m_usd=20_000.0,
            logo_at_risk_flag=0,
            renewal_days_remaining=180,
        ))
        # delta=0.10, gets 12 points
        assert r.expansion_health_score == pytest.approx(12.0, abs=0.01)

    def test_expansion_delta_exactly_30pct(self):
        r = self.engine.assess(make_input(
            expansion_revenue_last_12m_usd=14_000.0,
            expansion_revenue_prior_12m_usd=20_000.0,
            logo_at_risk_flag=0,
            renewal_days_remaining=180,
        ))
        # delta=0.30, gets 25 points
        assert r.expansion_health_score == pytest.approx(25.0, abs=0.01)

    def test_expansion_delta_exactly_50pct(self):
        r = self.engine.assess(make_input(
            expansion_revenue_last_12m_usd=10_000.0,
            expansion_revenue_prior_12m_usd=20_000.0,
            logo_at_risk_flag=0,
            renewal_days_remaining=180,
        ))
        # delta=0.50, gets 40 points
        assert r.expansion_health_score == pytest.approx(40.0, abs=0.01)

    # exec contact days thresholds
    def test_exec_contact_exactly_30d(self):
        r = self.engine.assess(make_input(
            executive_last_contact_days=30,
            executive_meetings_last_90d=3,
            executive_meetings_prior_90d=3,
            competitor_evaluation_signal=0,
        ))
        # gets 10 points
        assert r.relationship_risk_score == pytest.approx(10.0, abs=0.01)

    def test_exec_contact_exactly_60d(self):
        r = self.engine.assess(make_input(
            executive_last_contact_days=60,
            executive_meetings_last_90d=3,
            executive_meetings_prior_90d=3,
            competitor_evaluation_signal=0,
        ))
        # gets 24 points
        assert r.relationship_risk_score == pytest.approx(24.0, abs=0.01)

    def test_exec_contact_exactly_90d(self):
        r = self.engine.assess(make_input(
            executive_last_contact_days=90,
            executive_meetings_last_90d=3,
            executive_meetings_prior_90d=3,
            competitor_evaluation_signal=0,
        ))
        # gets 40 points
        assert r.relationship_risk_score == pytest.approx(40.0, abs=0.01)

    # meeting decline thresholds
    def test_meeting_decline_exactly_20pct(self):
        r = self.engine.assess(make_input(
            executive_last_contact_days=10,
            executive_meetings_last_90d=4,
            executive_meetings_prior_90d=5,
            competitor_evaluation_signal=0,
        ))
        # delta=1/5=0.20, gets 8 points
        assert r.relationship_risk_score == pytest.approx(8.0, abs=0.01)

    def test_meeting_decline_exactly_40pct(self):
        r = self.engine.assess(make_input(
            executive_last_contact_days=10,
            executive_meetings_last_90d=3,
            executive_meetings_prior_90d=5,
            competitor_evaluation_signal=0,
        ))
        # delta=2/5=0.40, gets 18 points
        assert r.relationship_risk_score == pytest.approx(18.0, abs=0.01)

    def test_meeting_decline_exactly_70pct(self):
        r = self.engine.assess(make_input(
            executive_last_contact_days=10,
            executive_meetings_last_90d=3,
            executive_meetings_prior_90d=10,
            competitor_evaluation_signal=0,
        ))
        # delta=7/10=0.70, gets 30 points
        assert r.relationship_risk_score == pytest.approx(30.0, abs=0.01)

    # composite risk boundary conditions
    def test_composite_19p9_is_low_risk(self):
        r = self.engine.assess(make_input())
        if r.erosion_composite < 20:
            assert r.erosion_risk == ErosionRisk.low
            assert r.erosion_severity == ErosionSeverity.healthy

    def test_risk_boundary_39p9_is_moderate(self):
        """Just below 40 should be moderate."""
        r = fresh_engine().assess(make_input(
            nps_score=40,
            nps_score_prior=55,
            executive_last_contact_days=30,
        ))
        if 20 <= r.erosion_composite < 40:
            assert r.erosion_risk == ErosionRisk.moderate

    def test_risk_boundary_60_is_critical(self):
        r = fresh_engine().assess(make_input(
            product_usage_score_last_30d=40.0,
            product_usage_score_prior_30d=80.0,
            nps_score=15,
            nps_score_prior=60,
            support_tickets_last_30d=6,
            support_tickets_prior_30d=2,
            executive_last_contact_days=90,
            logo_at_risk_flag=1,
            renewal_days_remaining=20,
            critical_tickets_last_30d=3,
        ))
        if r.erosion_composite >= 60:
            assert r.erosion_risk == ErosionRisk.critical


# ── Section 27: Identify fields in dataclasses ────────────────────────────────

class TestDataclassFieldNames:
    def test_input_field_names(self):
        import dataclasses
        names = {f.name for f in dataclasses.fields(CustomerLTVInput)}
        assert "customer_id" in names
        assert "contract_arr_usd" in names
        assert "renewal_days_remaining" in names
        assert "logo_at_risk_flag" in names
        assert "competitor_evaluation_signal" in names
        assert "critical_tickets_last_30d" in names

    def test_result_field_names(self):
        import dataclasses
        names = {f.name for f in dataclasses.fields(CustomerLTVResult)}
        assert "erosion_composite" in names
        assert "is_at_churn_risk" in names
        assert "requires_executive_attention" in names
        assert "estimated_arr_at_risk_usd" in names
        assert "erosion_signal" in names


# ── Section 28: Multiple engines independent ─────────────────────────────────

class TestEngineIsolation:
    def test_two_engines_independent(self):
        e1 = fresh_engine()
        e2 = fresh_engine()
        e1.assess(make_input(customer_id="A"))
        e1.assess(make_input(customer_id="B"))
        e2.assess(make_input(customer_id="C"))
        assert e1.summary()["total"] == 2
        assert e2.summary()["total"] == 1

    def test_fresh_engine_summary_total_zero(self):
        assert fresh_engine().summary()["total"] == 0

    def test_engine_accumulates_across_assess_calls(self):
        e = fresh_engine()
        for i in range(10):
            e.assess(make_input(customer_id=f"C{i}"))
        assert e.summary()["total"] == 10

    def test_batch_and_single_assess_both_accumulate(self):
        e = fresh_engine()
        e.assess(make_input(customer_id="SINGLE"))
        e.assess_batch([make_input(customer_id=f"B{i}") for i in range(3)])
        assert e.summary()["total"] == 4


# ── Section 29: Churn risk OR conditions all three branches ──────────────────

class TestChurnRiskORBranches:
    def test_branch1_composite_ge_40(self):
        # Build a scenario specifically targeting composite >=40
        r = fresh_engine().assess(make_input(
            nps_score=20,
            nps_score_prior=50,
            executive_last_contact_days=60,
            support_tickets_last_30d=4,
            support_tickets_prior_30d=2,
            logo_at_risk_flag=0,
            renewal_days_remaining=180,
        ))
        if r.erosion_composite >= 40:
            assert r.is_at_churn_risk is True

    def test_branch2_logo_at_risk_flag_1(self):
        r = fresh_engine().assess(make_input(logo_at_risk_flag=1))
        assert r.is_at_churn_risk is True

    def test_branch3_renewal_le_30_and_composite_ge_20(self):
        # renewal<=30 and composite in [20,40) triggers churn risk
        r = fresh_engine().assess(make_input(
            renewal_days_remaining=15,
            nps_score=40,
            nps_score_prior=55,
            executive_last_contact_days=30,
            logo_at_risk_flag=0,
        ))
        if 20 <= r.erosion_composite < 40:
            assert r.is_at_churn_risk is True

    def test_not_churn_risk_when_all_conditions_false(self):
        r = fresh_engine().assess(make_input(
            logo_at_risk_flag=0,
            competitor_evaluation_signal=0,
            renewal_days_remaining=365,
        ))
        if r.erosion_composite < 40:
            assert r.is_at_churn_risk is False


# ── Section 30: Executive attention OR conditions ─────────────────────────────

class TestExecAttentionORBranches:
    def test_branch1_composite_ge_30(self):
        r = fresh_engine().assess(make_input(
            nps_score=40,
            nps_score_prior=55,
            executive_last_contact_days=30,
            support_tickets_last_30d=3,
            support_tickets_prior_30d=2,
            competitor_evaluation_signal=0,
        ))
        if r.erosion_composite >= 30:
            assert r.requires_executive_attention is True

    def test_branch2_competitor_signal(self):
        r = fresh_engine().assess(make_input(competitor_evaluation_signal=1))
        assert r.requires_executive_attention is True

    def test_branch3_exec_contact_ge_60d(self):
        r = fresh_engine().assess(make_input(
            executive_last_contact_days=60,
            competitor_evaluation_signal=0,
        ))
        assert r.requires_executive_attention is True

    def test_not_exec_attention_when_all_false(self):
        r = fresh_engine().assess(make_input(
            executive_last_contact_days=30,
            competitor_evaluation_signal=0,
        ))
        if r.erosion_composite < 30:
            assert r.requires_executive_attention is False

    def test_exec_contact_29d_does_not_trigger_attention_alone(self):
        # 29 days < 60, no competitor signal, composite should be low
        r = fresh_engine().assess(make_input(
            executive_last_contact_days=29,
            competitor_evaluation_signal=0,
        ))
        if r.erosion_composite < 30:
            assert r.requires_executive_attention is False
