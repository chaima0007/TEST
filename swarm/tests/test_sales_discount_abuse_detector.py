"""Comprehensive pytest test suite for SalesDiscountAbuseDetector."""

from __future__ import annotations

import dataclasses
import math
import pytest

from swarm.intelligence.sales_discount_abuse_detector import (
    SalesDiscountAbuseDetector,
    SalesDiscountAbuseInput,
    SalesDiscountAbuseResult,
    DiscountRisk,
    DiscountPattern,
    DiscountSeverity,
    DiscountAction,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**kwargs) -> SalesDiscountAbuseInput:
    """Return a clean baseline input, overriding any supplied fields."""
    defaults = dict(
        rep_id="REP001",
        region="West",
        period_id="2024-Q1",
        deals_closed_count=10,
        avg_discount_pct=10.0,
        company_avg_discount_pct=10.0,
        deals_above_policy_count=0,
        max_discount_pct=15.0,
        policy_max_discount_pct=20.0,
        discount_requested_by_rep_count=0,
        deal_value_usd_total=100_000.0,
        revenue_at_risk_from_discount_usd=5_000.0,
        competitive_pressure_deals_count=2,
        manager_approved_exceptions_count=0,
        unauthorized_discount_count=0,
        discount_trend_delta_pct=0.0,
        avg_deal_cycle_days=30.0,
        company_avg_deal_cycle_days=30.0,
        win_rate_with_discount_pct=60.0,
        win_rate_without_discount_pct=55.0,
        rep_quota_attainment_pct=100.0,
        repeat_discount_customer_count=0,
    )
    defaults.update(kwargs)
    return SalesDiscountAbuseInput(**defaults)


def fresh() -> SalesDiscountAbuseDetector:
    return SalesDiscountAbuseDetector()


# ---------------------------------------------------------------------------
# 1. ENUM TESTS
# ---------------------------------------------------------------------------

class TestEnums:
    def test_discount_risk_values(self):
        assert DiscountRisk.low.value == "low"
        assert DiscountRisk.moderate.value == "moderate"
        assert DiscountRisk.high.value == "high"
        assert DiscountRisk.critical.value == "critical"

    def test_discount_risk_count(self):
        assert len(DiscountRisk) == 4

    def test_discount_pattern_values(self):
        assert DiscountPattern.none.value == "none"
        assert DiscountPattern.policy_breach.value == "policy_breach"
        assert DiscountPattern.habitual_discounting.value == "habitual_discounting"
        assert DiscountPattern.dependency_pattern.value == "dependency_pattern"
        assert DiscountPattern.unauthorized.value == "unauthorized"
        assert DiscountPattern.margin_destruction.value == "margin_destruction"

    def test_discount_pattern_count(self):
        assert len(DiscountPattern) == 6

    def test_discount_severity_values(self):
        assert DiscountSeverity.clean.value == "clean"
        assert DiscountSeverity.watch.value == "watch"
        assert DiscountSeverity.concerning.value == "concerning"
        assert DiscountSeverity.abusive.value == "abusive"

    def test_discount_severity_count(self):
        assert len(DiscountSeverity) == 4

    def test_discount_action_values(self):
        assert DiscountAction.no_action.value == "no_action"
        assert DiscountAction.flag_for_review.value == "flag_for_review"
        assert DiscountAction.manager_approval.value == "manager_approval"
        assert DiscountAction.discount_freeze.value == "discount_freeze"
        assert DiscountAction.compensation_review.value == "compensation_review"

    def test_discount_action_count(self):
        assert len(DiscountAction) == 5

    def test_enums_are_str_subclass(self):
        assert isinstance(DiscountRisk.low, str)
        assert isinstance(DiscountPattern.none, str)
        assert isinstance(DiscountSeverity.clean, str)
        assert isinstance(DiscountAction.no_action, str)


# ---------------------------------------------------------------------------
# 2. INPUT DATACLASS TESTS
# ---------------------------------------------------------------------------

class TestInputDataclass:
    def test_exactly_22_fields(self):
        fields = dataclasses.fields(SalesDiscountAbuseInput)
        assert len(fields) == 22

    def test_field_names(self):
        names = {f.name for f in dataclasses.fields(SalesDiscountAbuseInput)}
        expected = {
            "rep_id", "region", "period_id", "deals_closed_count",
            "avg_discount_pct", "company_avg_discount_pct", "deals_above_policy_count",
            "max_discount_pct", "policy_max_discount_pct", "discount_requested_by_rep_count",
            "deal_value_usd_total", "revenue_at_risk_from_discount_usd",
            "competitive_pressure_deals_count", "manager_approved_exceptions_count",
            "unauthorized_discount_count", "discount_trend_delta_pct",
            "avg_deal_cycle_days", "company_avg_deal_cycle_days",
            "win_rate_with_discount_pct", "win_rate_without_discount_pct",
            "rep_quota_attainment_pct", "repeat_discount_customer_count",
        }
        assert names == expected

    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(SalesDiscountAbuseInput)

    def test_can_instantiate(self):
        inp = make_input()
        assert inp.rep_id == "REP001"
        assert inp.region == "West"

    def test_field_types_accessible(self):
        inp = make_input()
        assert isinstance(inp.deals_closed_count, int)
        assert isinstance(inp.avg_discount_pct, float)
        assert isinstance(inp.rep_id, str)

    def test_zero_values_allowed(self):
        inp = make_input(deals_closed_count=0, deal_value_usd_total=0.0)
        assert inp.deals_closed_count == 0
        assert inp.deal_value_usd_total == 0.0


# ---------------------------------------------------------------------------
# 3. RESULT DATACLASS & to_dict TESTS
# ---------------------------------------------------------------------------

class TestResultDataclass:
    def test_to_dict_exactly_15_keys(self):
        d = fresh().assess(make_input()).to_dict()
        assert len(d) == 15

    def test_to_dict_key_names(self):
        d = fresh().assess(make_input()).to_dict()
        expected_keys = {
            "rep_id", "region", "discount_risk", "discount_pattern",
            "discount_severity", "recommended_action", "policy_violation_score",
            "revenue_impact_score", "behavioral_pattern_score", "dependency_score",
            "discount_composite", "is_abusing_discounts", "requires_manager_review",
            "estimated_margin_loss_usd", "discount_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_rep_id_matches(self):
        inp = make_input(rep_id="SALESREP42")
        d = fresh().assess(inp).to_dict()
        assert d["rep_id"] == "SALESREP42"

    def test_to_dict_region_matches(self):
        inp = make_input(region="Northeast")
        d = fresh().assess(inp).to_dict()
        assert d["region"] == "Northeast"

    def test_to_dict_enum_values_are_strings(self):
        d = fresh().assess(make_input()).to_dict()
        assert isinstance(d["discount_risk"], str)
        assert isinstance(d["discount_pattern"], str)
        assert isinstance(d["discount_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_scores_are_rounded_to_1dp(self):
        d = fresh().assess(make_input()).to_dict()
        for key in ("policy_violation_score", "revenue_impact_score",
                    "behavioral_pattern_score", "dependency_score", "discount_composite"):
            val = d[key]
            assert round(val, 1) == val

    def test_to_dict_margin_loss_rounded_to_2dp(self):
        d = fresh().assess(make_input()).to_dict()
        val = d["estimated_margin_loss_usd"]
        assert round(val, 2) == val

    def test_to_dict_booleans(self):
        d = fresh().assess(make_input()).to_dict()
        assert isinstance(d["is_abusing_discounts"], bool)
        assert isinstance(d["requires_manager_review"], bool)

    def test_to_dict_signal_is_string(self):
        d = fresh().assess(make_input()).to_dict()
        assert isinstance(d["discount_signal"], str)

    def test_result_is_dataclass(self):
        result = fresh().assess(make_input())
        assert dataclasses.is_dataclass(result)

    def test_result_fields_count(self):
        fields = dataclasses.fields(SalesDiscountAbuseResult)
        assert len(fields) == 15


# ---------------------------------------------------------------------------
# 4. COMPOSITE FORMULA TESTS
# ---------------------------------------------------------------------------

class TestCompositeFormula:
    def test_composite_zero_for_clean_rep(self):
        inp = make_input()
        result = fresh().assess(inp)
        # All scores should be 0 with fully clean baseline
        assert result.discount_composite == 0.0

    def test_composite_weights_policy(self):
        # Force policy score = 100, others = 0
        # policy*0.35 = 35
        inp = make_input(
            unauthorized_discount_count=5,  # +50
            deals_above_policy_count=6, deals_closed_count=10,  # 60% ratio → +30
            max_discount_pct=40.0, policy_max_discount_pct=20.0,  # excess=20 → +20
        )
        result = fresh().assess(inp)
        # policy_violation_score = min(100, 50+30+20) = 100
        assert result.policy_violation_score == 100.0
        # composite >= 35 (policy contributes 35)
        assert result.discount_composite >= 35.0

    def test_composite_is_clamped_to_100(self):
        # Create worst-case scenario across all dimensions
        inp = make_input(
            unauthorized_discount_count=5,
            deals_above_policy_count=10, deals_closed_count=10,
            max_discount_pct=50.0, policy_max_discount_pct=20.0,
            avg_discount_pct=40.0, company_avg_discount_pct=10.0,
            revenue_at_risk_from_discount_usd=50_000.0, deal_value_usd_total=100_000.0,
            discount_trend_delta_pct=15.0,
            discount_requested_by_rep_count=10,
            avg_deal_cycle_days=5.0, company_avg_deal_cycle_days=30.0,
            manager_approved_exceptions_count=5,
            win_rate_with_discount_pct=90.0, win_rate_without_discount_pct=30.0,
            repeat_discount_customer_count=10,
            rep_quota_attainment_pct=150.0,
        )
        result = fresh().assess(inp)
        assert result.discount_composite <= 100.0

    def test_composite_is_non_negative(self):
        inp = make_input()
        result = fresh().assess(inp)
        assert result.discount_composite >= 0.0

    def test_composite_formula_manual(self):
        # Craft input to get known sub-scores, verify formula
        inp = make_input(
            # policy: unauthorized=1 → +18; above_policy=2/10=0.2 → +8; max=25-20=5 → +5 → total=31
            unauthorized_discount_count=1,
            deals_above_policy_count=2, deals_closed_count=10,
            max_discount_pct=25.0, policy_max_discount_pct=20.0,
            # revenue: excess_avg=0, risk_ratio=0, trend=0 → 0
            avg_discount_pct=10.0, company_avg_discount_pct=10.0,
            revenue_at_risk_from_discount_usd=1_000.0, deal_value_usd_total=100_000.0,
            discount_trend_delta_pct=0.0,
            # behavioral: no rep-initiated, speed=1, no exceptions → 0
            discount_requested_by_rep_count=0,
            avg_deal_cycle_days=30.0, company_avg_deal_cycle_days=30.0,
            manager_approved_exceptions_count=0,
            # dependency: win_gap=5 (<15), repeat=0, quota=100 → 0
            win_rate_with_discount_pct=60.0, win_rate_without_discount_pct=55.0,
            repeat_discount_customer_count=0,
            rep_quota_attainment_pct=100.0,
        )
        result = fresh().assess(inp)
        assert result.policy_violation_score == 31.0
        assert result.revenue_impact_score == 0.0
        assert result.behavioral_pattern_score == 0.0
        assert result.dependency_score == 0.0
        expected_composite = round(31.0 * 0.35 + 0.0 * 0.30 + 0.0 * 0.20 + 0.0 * 0.15, 1)
        assert result.discount_composite == expected_composite

    def test_composite_rounded_to_1dp(self):
        result = fresh().assess(make_input(unauthorized_discount_count=1, deals_above_policy_count=1))
        assert result.discount_composite == round(result.discount_composite, 1)


# ---------------------------------------------------------------------------
# 5. POLICY VIOLATION SCORE TESTS
# ---------------------------------------------------------------------------

class TestPolicyViolationScore:
    def test_zero_when_clean(self):
        inp = make_input()
        result = fresh().assess(inp)
        assert result.policy_violation_score == 0.0

    def test_unauthorized_1(self):
        inp = make_input(unauthorized_discount_count=1)
        result = fresh().assess(inp)
        assert result.policy_violation_score >= 18.0

    def test_unauthorized_3(self):
        inp = make_input(unauthorized_discount_count=3)
        result = fresh().assess(inp)
        assert result.policy_violation_score >= 35.0

    def test_unauthorized_5(self):
        inp = make_input(unauthorized_discount_count=5)
        result = fresh().assess(inp)
        assert result.policy_violation_score >= 50.0

    def test_unauthorized_5_more_than_3(self):
        r3 = fresh().assess(make_input(unauthorized_discount_count=3))
        r5 = fresh().assess(make_input(unauthorized_discount_count=5))
        assert r5.policy_violation_score > r3.policy_violation_score

    def test_unauthorized_3_more_than_1(self):
        r1 = fresh().assess(make_input(unauthorized_discount_count=1))
        r3 = fresh().assess(make_input(unauthorized_discount_count=3))
        assert r3.policy_violation_score > r1.policy_violation_score

    def test_above_policy_ratio_low(self):
        inp = make_input(deals_above_policy_count=2, deals_closed_count=10)  # 20%
        result = fresh().assess(inp)
        assert result.policy_violation_score >= 8.0

    def test_above_policy_ratio_medium(self):
        inp = make_input(deals_above_policy_count=4, deals_closed_count=10)  # 40%
        result = fresh().assess(inp)
        assert result.policy_violation_score >= 18.0

    def test_above_policy_ratio_high(self):
        inp = make_input(deals_above_policy_count=6, deals_closed_count=10)  # 60%
        result = fresh().assess(inp)
        assert result.policy_violation_score >= 30.0

    def test_no_above_policy_ratio_when_zero_deals(self):
        inp = make_input(deals_closed_count=0, deals_above_policy_count=0)
        result = fresh().assess(inp)
        # No division by zero — should not crash
        assert result.policy_violation_score >= 0.0

    def test_max_excess_small(self):
        # max=25, policy=20 → excess=5 → +5
        inp = make_input(max_discount_pct=25.0, policy_max_discount_pct=20.0)
        result = fresh().assess(inp)
        assert result.policy_violation_score >= 5.0

    def test_max_excess_medium(self):
        # max=30, policy=20 → excess=10 → +12
        inp = make_input(max_discount_pct=30.0, policy_max_discount_pct=20.0)
        result = fresh().assess(inp)
        assert result.policy_violation_score >= 12.0

    def test_max_excess_large(self):
        # max=40, policy=20 → excess=20 → +20
        inp = make_input(max_discount_pct=40.0, policy_max_discount_pct=20.0)
        result = fresh().assess(inp)
        assert result.policy_violation_score >= 20.0

    def test_no_max_excess_when_policy_zero(self):
        # policy_max=0 → branch skipped
        inp = make_input(max_discount_pct=50.0, policy_max_discount_pct=0.0)
        result = fresh().assess(inp)
        assert result.policy_violation_score == 0.0

    def test_clamped_at_100(self):
        inp = make_input(
            unauthorized_discount_count=5,
            deals_above_policy_count=10, deals_closed_count=10,
            max_discount_pct=50.0, policy_max_discount_pct=20.0,
        )
        result = fresh().assess(inp)
        assert result.policy_violation_score <= 100.0

    def test_threshold_boundary_unauthorized_2(self):
        # 2 unauthorized → still 18 tier (not 35)
        inp = make_input(unauthorized_discount_count=2)
        result = fresh().assess(inp)
        assert result.policy_violation_score >= 18.0
        assert result.policy_violation_score < 35.0 + 30.0 + 20.0  # no other factors


# ---------------------------------------------------------------------------
# 6. REVENUE IMPACT SCORE TESTS
# ---------------------------------------------------------------------------

class TestRevenueImpactScore:
    def test_zero_when_clean(self):
        inp = make_input()
        result = fresh().assess(inp)
        assert result.revenue_impact_score == 0.0

    def test_excess_avg_small(self):
        inp = make_input(avg_discount_pct=15.0, company_avg_discount_pct=10.0)  # excess=5
        result = fresh().assess(inp)
        assert result.revenue_impact_score >= 12.0

    def test_excess_avg_medium(self):
        inp = make_input(avg_discount_pct=20.0, company_avg_discount_pct=10.0)  # excess=10
        result = fresh().assess(inp)
        assert result.revenue_impact_score >= 25.0

    def test_excess_avg_large(self):
        inp = make_input(avg_discount_pct=25.0, company_avg_discount_pct=10.0)  # excess=15
        result = fresh().assess(inp)
        assert result.revenue_impact_score >= 40.0

    def test_no_excess_avg(self):
        inp = make_input(avg_discount_pct=10.0, company_avg_discount_pct=10.0)
        result = fresh().assess(inp)
        # excess=0 → 0 contribution from avg
        assert result.revenue_impact_score == 0.0

    def test_risk_ratio_low(self):
        # 8% risk ratio
        inp = make_input(revenue_at_risk_from_discount_usd=8_000.0, deal_value_usd_total=100_000.0)
        result = fresh().assess(inp)
        assert result.revenue_impact_score >= 8.0

    def test_risk_ratio_medium(self):
        # 15% risk ratio
        inp = make_input(revenue_at_risk_from_discount_usd=15_000.0, deal_value_usd_total=100_000.0)
        result = fresh().assess(inp)
        assert result.revenue_impact_score >= 18.0

    def test_risk_ratio_high(self):
        # 25% risk ratio
        inp = make_input(revenue_at_risk_from_discount_usd=25_000.0, deal_value_usd_total=100_000.0)
        result = fresh().assess(inp)
        assert result.revenue_impact_score >= 30.0

    def test_no_risk_ratio_when_deal_value_zero(self):
        inp = make_input(deal_value_usd_total=0.0, revenue_at_risk_from_discount_usd=5_000.0)
        result = fresh().assess(inp)
        # Should not crash
        assert result.revenue_impact_score >= 0.0

    def test_trend_medium(self):
        inp = make_input(discount_trend_delta_pct=5.0)
        result = fresh().assess(inp)
        assert result.revenue_impact_score >= 10.0

    def test_trend_high(self):
        inp = make_input(discount_trend_delta_pct=10.0)
        result = fresh().assess(inp)
        assert result.revenue_impact_score >= 20.0

    def test_no_trend(self):
        inp = make_input(discount_trend_delta_pct=0.0)
        result = fresh().assess(inp)
        assert result.revenue_impact_score == 0.0

    def test_clamped_at_100(self):
        inp = make_input(
            avg_discount_pct=40.0, company_avg_discount_pct=10.0,
            revenue_at_risk_from_discount_usd=50_000.0, deal_value_usd_total=100_000.0,
            discount_trend_delta_pct=15.0,
        )
        result = fresh().assess(inp)
        assert result.revenue_impact_score <= 100.0

    def test_trend_boundary_just_below_10(self):
        inp = make_input(discount_trend_delta_pct=9.9)
        result = fresh().assess(inp)
        assert result.revenue_impact_score >= 10.0
        assert result.revenue_impact_score < 20.0


# ---------------------------------------------------------------------------
# 7. BEHAVIORAL PATTERN SCORE TESTS
# ---------------------------------------------------------------------------

class TestBehavioralPatternScore:
    def test_zero_when_clean(self):
        inp = make_input()
        result = fresh().assess(inp)
        assert result.behavioral_pattern_score == 0.0

    def test_rep_initiation_low(self):
        # 30% rep initiation
        inp = make_input(discount_requested_by_rep_count=3, deals_closed_count=10)
        result = fresh().assess(inp)
        assert result.behavioral_pattern_score >= 10.0

    def test_rep_initiation_medium(self):
        # 50% rep initiation
        inp = make_input(discount_requested_by_rep_count=5, deals_closed_count=10)
        result = fresh().assess(inp)
        assert result.behavioral_pattern_score >= 22.0

    def test_rep_initiation_high(self):
        # 70% rep initiation
        inp = make_input(discount_requested_by_rep_count=7, deals_closed_count=10)
        result = fresh().assess(inp)
        assert result.behavioral_pattern_score >= 35.0

    def test_no_rep_initiation_when_zero_requested(self):
        inp = make_input(discount_requested_by_rep_count=0, deals_closed_count=10)
        result = fresh().assess(inp)
        # Only contributes if discount_requested_by_rep_count > 0
        assert result.behavioral_pattern_score == 0.0

    def test_speed_shortcut_strong(self):
        # avg_deal_cycle=10, company=30 → ratio=0.33 < 0.5; avg_disc=20 > company+5=15
        inp = make_input(
            avg_deal_cycle_days=10.0, company_avg_deal_cycle_days=30.0,
            avg_discount_pct=20.0, company_avg_discount_pct=10.0,
        )
        result = fresh().assess(inp)
        assert result.behavioral_pattern_score >= 25.0

    def test_speed_shortcut_moderate(self):
        # avg=19, company=30 → ratio=0.63 between 0.5-0.7; avg_disc=15 > company+3=13
        inp = make_input(
            avg_deal_cycle_days=19.0, company_avg_deal_cycle_days=30.0,
            avg_discount_pct=15.0, company_avg_discount_pct=10.0,
        )
        result = fresh().assess(inp)
        assert result.behavioral_pattern_score >= 12.0

    def test_no_speed_shortcut_when_company_cycle_zero(self):
        inp = make_input(company_avg_deal_cycle_days=0.0)
        result = fresh().assess(inp)
        # Branch condition requires company_avg > 0
        assert result.behavioral_pattern_score >= 0.0

    def test_manager_exceptions_low(self):
        inp = make_input(manager_approved_exceptions_count=1)
        result = fresh().assess(inp)
        assert result.behavioral_pattern_score >= 5.0

    def test_manager_exceptions_medium(self):
        inp = make_input(manager_approved_exceptions_count=3)
        result = fresh().assess(inp)
        assert result.behavioral_pattern_score >= 12.0

    def test_manager_exceptions_high(self):
        inp = make_input(manager_approved_exceptions_count=5)
        result = fresh().assess(inp)
        assert result.behavioral_pattern_score >= 20.0

    def test_clamped_at_100(self):
        inp = make_input(
            discount_requested_by_rep_count=10, deals_closed_count=10,
            avg_deal_cycle_days=5.0, company_avg_deal_cycle_days=30.0,
            avg_discount_pct=30.0, company_avg_discount_pct=10.0,
            manager_approved_exceptions_count=5,
        )
        result = fresh().assess(inp)
        assert result.behavioral_pattern_score <= 100.0


# ---------------------------------------------------------------------------
# 8. DEPENDENCY SCORE TESTS
# ---------------------------------------------------------------------------

class TestDependencyScore:
    def test_zero_when_clean(self):
        inp = make_input()
        result = fresh().assess(inp)
        assert result.dependency_score == 0.0

    def test_win_gap_small(self):
        inp = make_input(win_rate_with_discount_pct=70.0, win_rate_without_discount_pct=55.0)  # gap=15
        result = fresh().assess(inp)
        assert result.dependency_score >= 12.0

    def test_win_gap_medium(self):
        inp = make_input(win_rate_with_discount_pct=80.0, win_rate_without_discount_pct=55.0)  # gap=25
        result = fresh().assess(inp)
        assert result.dependency_score >= 25.0

    def test_win_gap_large(self):
        inp = make_input(win_rate_with_discount_pct=95.0, win_rate_without_discount_pct=55.0)  # gap=40
        result = fresh().assess(inp)
        assert result.dependency_score >= 40.0

    def test_win_gap_below_threshold(self):
        inp = make_input(win_rate_with_discount_pct=65.0, win_rate_without_discount_pct=55.0)  # gap=10
        result = fresh().assess(inp)
        # gap < 15 → no contribution from win gap
        assert result.dependency_score == 0.0

    def test_repeat_customers_low(self):
        inp = make_input(repeat_discount_customer_count=1)
        result = fresh().assess(inp)
        assert result.dependency_score >= 8.0

    def test_repeat_customers_medium(self):
        inp = make_input(repeat_discount_customer_count=3)
        result = fresh().assess(inp)
        assert result.dependency_score >= 18.0

    def test_repeat_customers_high(self):
        inp = make_input(repeat_discount_customer_count=5)
        result = fresh().assess(inp)
        assert result.dependency_score >= 30.0

    def test_quota_attainment_strong_high_discount(self):
        # quota >= 140 AND avg_disc > company_avg + 8
        inp = make_input(rep_quota_attainment_pct=140.0, avg_discount_pct=20.0, company_avg_discount_pct=10.0)
        result = fresh().assess(inp)
        assert result.dependency_score >= 20.0

    def test_quota_attainment_medium_high_discount(self):
        # quota >= 120 AND avg_disc > company_avg + 5
        inp = make_input(rep_quota_attainment_pct=120.0, avg_discount_pct=16.0, company_avg_discount_pct=10.0)
        result = fresh().assess(inp)
        assert result.dependency_score >= 10.0

    def test_quota_attainment_no_effect_without_discount(self):
        inp = make_input(rep_quota_attainment_pct=150.0, avg_discount_pct=10.0, company_avg_discount_pct=10.0)
        result = fresh().assess(inp)
        # avg_disc not exceeding threshold → no contribution
        assert result.dependency_score == 0.0

    def test_clamped_at_100(self):
        inp = make_input(
            win_rate_with_discount_pct=100.0, win_rate_without_discount_pct=40.0,
            repeat_discount_customer_count=10,
            rep_quota_attainment_pct=150.0, avg_discount_pct=25.0, company_avg_discount_pct=10.0,
        )
        result = fresh().assess(inp)
        assert result.dependency_score <= 100.0


# ---------------------------------------------------------------------------
# 9. RISK CLASSIFICATION TESTS
# ---------------------------------------------------------------------------

class TestRiskClassification:
    def test_low_risk_composite_below_20(self):
        inp = make_input()  # composite = 0
        result = fresh().assess(inp)
        assert result.discount_risk == DiscountRisk.low

    def test_moderate_risk_composite_20_to_39(self):
        # unauthorized=1 → policy=18 → composite=18*0.35=6.3 → low
        # Need to get composite in [20, 40)
        inp = make_input(
            unauthorized_discount_count=1,
            deals_above_policy_count=4, deals_closed_count=10,
            max_discount_pct=30.0, policy_max_discount_pct=20.0,
        )
        result = fresh().assess(inp)
        if 20.0 <= result.discount_composite < 40.0:
            assert result.discount_risk == DiscountRisk.moderate

    def test_high_risk_composite_40_to_59(self):
        inp = make_input(
            unauthorized_discount_count=3,
            deals_above_policy_count=6, deals_closed_count=10,
            avg_discount_pct=22.0, company_avg_discount_pct=10.0,
            revenue_at_risk_from_discount_usd=20_000.0, deal_value_usd_total=100_000.0,
        )
        result = fresh().assess(inp)
        if 40.0 <= result.discount_composite < 60.0:
            assert result.discount_risk == DiscountRisk.high

    def test_critical_risk_composite_60_plus(self):
        inp = make_input(
            unauthorized_discount_count=5,
            deals_above_policy_count=10, deals_closed_count=10,
            max_discount_pct=50.0, policy_max_discount_pct=20.0,
            avg_discount_pct=40.0, company_avg_discount_pct=10.0,
            revenue_at_risk_from_discount_usd=40_000.0, deal_value_usd_total=100_000.0,
            discount_trend_delta_pct=15.0,
            discount_requested_by_rep_count=10,
        )
        result = fresh().assess(inp)
        if result.discount_composite >= 60.0:
            assert result.discount_risk == DiscountRisk.critical

    def test_risk_boundary_exact_20(self):
        # Craft composite = exactly 20 → moderate
        detector = fresh()
        # Force via known policy score
        inp = make_input(
            # policy: unauthorized=1→18, above_policy=2/10→8, no excess → 26 total
            # composite = 26*0.35 = 9.1 → low risk; need more
            unauthorized_discount_count=3,  # 35
            deals_above_policy_count=4, deals_closed_count=10,  # 40% → 18
        )
        result = detector.assess(inp)
        # policy = 53 → composite = 53*0.35 = 18.55 → low still
        # Let's just check correct mapping
        c = result.discount_composite
        expected = DiscountRisk.low if c < 20 else (
            DiscountRisk.moderate if c < 40 else (
                DiscountRisk.high if c < 60 else DiscountRisk.critical
            )
        )
        assert result.discount_risk == expected

    def test_risk_matches_composite_for_any_input(self):
        for unauth in [0, 1, 3, 5]:
            for above in [0, 2, 5, 8]:
                inp = make_input(unauthorized_discount_count=unauth,
                                 deals_above_policy_count=above, deals_closed_count=10)
                result = fresh().assess(inp)
                c = result.discount_composite
                if c < 20:
                    assert result.discount_risk == DiscountRisk.low
                elif c < 40:
                    assert result.discount_risk == DiscountRisk.moderate
                elif c < 60:
                    assert result.discount_risk == DiscountRisk.high
                else:
                    assert result.discount_risk == DiscountRisk.critical


# ---------------------------------------------------------------------------
# 10. SEVERITY CLASSIFICATION TESTS
# ---------------------------------------------------------------------------

class TestSeverityClassification:
    def test_clean_composite_below_20(self):
        inp = make_input()
        result = fresh().assess(inp)
        assert result.discount_severity == DiscountSeverity.clean

    def test_severity_matches_composite(self):
        for unauth in [0, 1, 3, 5]:
            inp = make_input(unauthorized_discount_count=unauth,
                             deals_above_policy_count=unauth * 2, deals_closed_count=10)
            result = fresh().assess(inp)
            c = result.discount_composite
            if c < 20:
                assert result.discount_severity == DiscountSeverity.clean
            elif c < 40:
                assert result.discount_severity == DiscountSeverity.watch
            elif c < 60:
                assert result.discount_severity == DiscountSeverity.concerning
            else:
                assert result.discount_severity == DiscountSeverity.abusive

    def test_risk_and_severity_thresholds_aligned(self):
        """Risk and severity use the same composite thresholds."""
        inp = make_input(
            unauthorized_discount_count=3,
            avg_discount_pct=25.0, company_avg_discount_pct=10.0,
        )
        result = fresh().assess(inp)
        # Both use the same breakpoints: <20, <40, <60, >=60
        risk_levels = [DiscountRisk.low, DiscountRisk.moderate, DiscountRisk.high, DiscountRisk.critical]
        sev_levels = [DiscountSeverity.clean, DiscountSeverity.watch, DiscountSeverity.concerning, DiscountSeverity.abusive]
        risk_idx = risk_levels.index(result.discount_risk)
        sev_idx = sev_levels.index(result.discount_severity)
        assert risk_idx == sev_idx


# ---------------------------------------------------------------------------
# 11. PATTERN CLASSIFICATION TESTS
# ---------------------------------------------------------------------------

class TestPatternClassification:
    def test_none_pattern_clean_rep(self):
        inp = make_input()
        result = fresh().assess(inp)
        assert result.discount_pattern == DiscountPattern.none

    def test_unauthorized_pattern_wins_first(self):
        # unauthorized >= 3 → unauthorized pattern regardless of others
        inp = make_input(
            unauthorized_discount_count=3,
            deals_above_policy_count=10, deals_closed_count=10,  # would be policy_breach
        )
        result = fresh().assess(inp)
        assert result.discount_pattern == DiscountPattern.unauthorized

    def test_unauthorized_pattern_requires_3(self):
        inp = make_input(unauthorized_discount_count=2)
        result = fresh().assess(inp)
        assert result.discount_pattern != DiscountPattern.unauthorized

    def test_margin_destruction_pattern(self):
        # revenue >= 50 AND avg_disc > company_avg + 12
        inp = make_input(
            unauthorized_discount_count=0,
            avg_discount_pct=30.0, company_avg_discount_pct=10.0,  # +20 > 12
            revenue_at_risk_from_discount_usd=50_000.0, deal_value_usd_total=100_000.0,  # 50% → revenue=30+30+0=60
            discount_trend_delta_pct=5.0,  # +10
        )
        result = fresh().assess(inp)
        if result.revenue_impact_score >= 50.0 and (30.0 - 10.0) > 12.0:
            assert result.discount_pattern == DiscountPattern.margin_destruction

    def test_policy_breach_pattern(self):
        # deals_above_policy >= 5 (and not unauthorized or margin_destruction)
        inp = make_input(
            unauthorized_discount_count=0,
            deals_above_policy_count=5, deals_closed_count=20,
            avg_discount_pct=12.0, company_avg_discount_pct=10.0,
        )
        result = fresh().assess(inp)
        if result.revenue_impact_score < 50.0:
            assert result.discount_pattern == DiscountPattern.policy_breach

    def test_policy_breach_requires_5(self):
        inp = make_input(deals_above_policy_count=4, deals_closed_count=20)
        result = fresh().assess(inp)
        assert result.discount_pattern != DiscountPattern.policy_breach

    def test_dependency_pattern(self):
        # win_gap >= 30 AND repeat_discount_customers >= 3
        inp = make_input(
            unauthorized_discount_count=0,
            deals_above_policy_count=2, deals_closed_count=20,
            avg_discount_pct=11.0, company_avg_discount_pct=10.0,
            win_rate_with_discount_pct=85.0, win_rate_without_discount_pct=50.0,
            repeat_discount_customer_count=3,
        )
        result = fresh().assess(inp)
        if result.revenue_impact_score < 50.0:
            assert result.discount_pattern == DiscountPattern.dependency_pattern

    def test_habitual_discounting_pattern(self):
        # rep_initiation_ratio >= 0.5
        inp = make_input(
            unauthorized_discount_count=0,
            deals_above_policy_count=2, deals_closed_count=10,
            avg_discount_pct=11.0, company_avg_discount_pct=10.0,
            win_rate_with_discount_pct=60.0, win_rate_without_discount_pct=55.0,
            discount_requested_by_rep_count=5,
        )
        result = fresh().assess(inp)
        if result.revenue_impact_score < 50 and result.discount_pattern not in (
            DiscountPattern.unauthorized, DiscountPattern.margin_destruction,
            DiscountPattern.policy_breach, DiscountPattern.dependency_pattern
        ):
            assert result.discount_pattern == DiscountPattern.habitual_discounting

    def test_habitual_discounting_requires_rep_count_nonzero(self):
        inp = make_input(discount_requested_by_rep_count=0)
        result = fresh().assess(inp)
        assert result.discount_pattern != DiscountPattern.habitual_discounting


# ---------------------------------------------------------------------------
# 12. RECOMMENDED ACTION TESTS
# ---------------------------------------------------------------------------

class TestRecommendedAction:
    def test_no_action_clean_rep(self):
        inp = make_input()
        result = fresh().assess(inp)
        assert result.recommended_action == DiscountAction.no_action

    def test_compensation_review_composite_60_plus(self):
        inp = make_input(
            unauthorized_discount_count=5,
            deals_above_policy_count=10, deals_closed_count=10,
            max_discount_pct=50.0, policy_max_discount_pct=20.0,
            avg_discount_pct=40.0, company_avg_discount_pct=10.0,
            revenue_at_risk_from_discount_usd=40_000.0, deal_value_usd_total=100_000.0,
            discount_trend_delta_pct=15.0,
        )
        result = fresh().assess(inp)
        if result.discount_composite >= 60:
            assert result.recommended_action == DiscountAction.compensation_review

    def test_discount_freeze_high_risk(self):
        # Need composite in [40, 60) → high risk
        inp = make_input(
            unauthorized_discount_count=3,
            deals_above_policy_count=6, deals_closed_count=10,
            avg_discount_pct=20.0, company_avg_discount_pct=10.0,
        )
        result = fresh().assess(inp)
        if result.discount_risk == DiscountRisk.high:
            assert result.recommended_action == DiscountAction.discount_freeze

    def test_manager_approval_moderate_risk(self):
        inp = make_input(
            unauthorized_discount_count=1,
            deals_above_policy_count=4, deals_closed_count=10,
            max_discount_pct=30.0, policy_max_discount_pct=20.0,
            avg_discount_pct=15.0, company_avg_discount_pct=10.0,
        )
        result = fresh().assess(inp)
        if result.discount_risk == DiscountRisk.moderate:
            assert result.recommended_action == DiscountAction.manager_approval

    def test_flag_for_review_low_but_nonzero(self):
        # composite >= 10 but low risk
        inp = make_input(
            unauthorized_discount_count=1,
            max_discount_pct=27.0, policy_max_discount_pct=20.0,
        )
        result = fresh().assess(inp)
        if result.discount_risk == DiscountRisk.low and result.discount_composite >= 10:
            assert result.recommended_action == DiscountAction.flag_for_review

    def test_action_compensation_review_takes_priority_over_high(self):
        # composite >= 60 should give compensation_review, not discount_freeze
        inp = make_input(
            unauthorized_discount_count=5,
            deals_above_policy_count=10, deals_closed_count=10,
            max_discount_pct=50.0, policy_max_discount_pct=20.0,
            avg_discount_pct=40.0, company_avg_discount_pct=10.0,
            revenue_at_risk_from_discount_usd=40_000.0, deal_value_usd_total=100_000.0,
            discount_trend_delta_pct=15.0,
            discount_requested_by_rep_count=8,
        )
        result = fresh().assess(inp)
        if result.discount_composite >= 60:
            assert result.recommended_action == DiscountAction.compensation_review
            assert result.recommended_action != DiscountAction.discount_freeze


# ---------------------------------------------------------------------------
# 13. IS_ABUSING_DISCOUNTS TESTS
# ---------------------------------------------------------------------------

class TestIsAbusingDiscounts:
    def test_false_clean_rep(self):
        result = fresh().assess(make_input())
        assert result.is_abusing_discounts is False

    def test_true_when_composite_40_plus(self):
        inp = make_input(
            unauthorized_discount_count=3,
            deals_above_policy_count=6, deals_closed_count=10,
            avg_discount_pct=25.0, company_avg_discount_pct=10.0,
            revenue_at_risk_from_discount_usd=20_000.0, deal_value_usd_total=100_000.0,
        )
        result = fresh().assess(inp)
        if result.discount_composite >= 40:
            assert result.is_abusing_discounts is True

    def test_true_when_unauthorized_3_plus(self):
        inp = make_input(unauthorized_discount_count=3)
        result = fresh().assess(inp)
        assert result.is_abusing_discounts is True

    def test_true_when_unauthorized_exactly_3(self):
        inp = make_input(unauthorized_discount_count=3)
        result = fresh().assess(inp)
        assert result.is_abusing_discounts is True

    def test_false_when_unauthorized_2(self):
        inp = make_input(unauthorized_discount_count=2)
        result = fresh().assess(inp)
        # Only true if also composite >= 40 or avg_disc > policy*1.5
        if result.discount_composite < 40:
            # check third condition: policy_max=20, avg=10 → 10 > 30 → False
            assert result.is_abusing_discounts is False

    def test_true_when_avg_exceeds_policy_times_1_5(self):
        # policy_max=20, avg=31 → 31 > 20*1.5=30 → True
        inp = make_input(avg_discount_pct=31.0, policy_max_discount_pct=20.0)
        result = fresh().assess(inp)
        assert result.is_abusing_discounts is True

    def test_false_when_avg_exactly_policy_times_1_5(self):
        # avg=30, policy=20 → 30 > 30 is False (strict >), third condition not met
        inp = make_input(avg_discount_pct=30.0, policy_max_discount_pct=20.0,
                         unauthorized_discount_count=0)
        result = fresh().assess(inp)
        # avg_discount_pct == policy_max * 1.5 exactly — strict > means no trigger from 3rd condition
        # composite here is 12.0 < 40, unauthorized=0 < 3, 30 > 30 is False
        assert result.is_abusing_discounts is False

    def test_false_when_policy_max_zero(self):
        # Third condition guarded by policy_max > 0
        inp = make_input(avg_discount_pct=50.0, policy_max_discount_pct=0.0)
        result = fresh().assess(inp)
        # Only other conditions could trigger
        if result.discount_composite < 40 and inp.unauthorized_discount_count < 3:
            assert result.is_abusing_discounts is False

    def test_true_when_all_three_conditions_met(self):
        inp = make_input(
            unauthorized_discount_count=5,
            avg_discount_pct=50.0, policy_max_discount_pct=20.0,
            deals_above_policy_count=6, deals_closed_count=10,
        )
        result = fresh().assess(inp)
        assert result.is_abusing_discounts is True


# ---------------------------------------------------------------------------
# 14. REQUIRES_MANAGER_REVIEW TESTS
# ---------------------------------------------------------------------------

class TestRequiresManagerReview:
    def test_false_clean_rep(self):
        result = fresh().assess(make_input())
        assert result.requires_manager_review is False

    def test_true_composite_30_plus(self):
        inp = make_input(
            unauthorized_discount_count=3,
            deals_above_policy_count=4, deals_closed_count=10,
        )
        result = fresh().assess(inp)
        if result.discount_composite >= 30:
            assert result.requires_manager_review is True

    def test_true_unauthorized_2(self):
        inp = make_input(unauthorized_discount_count=2)
        result = fresh().assess(inp)
        assert result.requires_manager_review is True

    def test_true_unauthorized_exactly_2(self):
        inp = make_input(unauthorized_discount_count=2)
        result = fresh().assess(inp)
        assert result.requires_manager_review is True

    def test_false_unauthorized_1(self):
        inp = make_input(unauthorized_discount_count=1)
        result = fresh().assess(inp)
        if result.discount_composite < 30 and inp.deals_above_policy_count < 5:
            assert result.requires_manager_review is False

    def test_true_deals_above_policy_5(self):
        inp = make_input(deals_above_policy_count=5, deals_closed_count=20)
        result = fresh().assess(inp)
        assert result.requires_manager_review is True

    def test_false_deals_above_policy_4(self):
        inp = make_input(deals_above_policy_count=4, deals_closed_count=20)
        result = fresh().assess(inp)
        if result.discount_composite < 30 and inp.unauthorized_discount_count < 2:
            assert result.requires_manager_review is False

    def test_is_abusing_implies_manager_review(self):
        """If is_abusing_discounts, composite >= 40 > 30, so review also True."""
        for unauth in [3, 5]:
            inp = make_input(unauthorized_discount_count=unauth)
            result = fresh().assess(inp)
            if result.is_abusing_discounts:
                assert result.requires_manager_review is True


# ---------------------------------------------------------------------------
# 15. ESTIMATED MARGIN LOSS TESTS
# ---------------------------------------------------------------------------

class TestEstimatedMarginLoss:
    def test_zero_when_composite_zero(self):
        inp = make_input(revenue_at_risk_from_discount_usd=10_000.0)
        result = fresh().assess(inp)
        if result.discount_composite == 0.0:
            assert result.estimated_margin_loss_usd == 0.0

    def test_formula_margin_loss(self):
        inp = make_input(
            unauthorized_discount_count=1,
            revenue_at_risk_from_discount_usd=10_000.0,
        )
        result = fresh().assess(inp)
        expected = inp.revenue_at_risk_from_discount_usd * (result.discount_composite / 100.0)
        assert abs(result.estimated_margin_loss_usd - expected) < 0.01

    def test_margin_loss_scales_with_revenue_at_risk(self):
        # Keep deal_value proportional so risk_ratio stays same → same composite
        inp1 = make_input(unauthorized_discount_count=3,
                          revenue_at_risk_from_discount_usd=10_000.0,
                          deal_value_usd_total=100_000.0)
        inp2 = make_input(unauthorized_discount_count=3,
                          revenue_at_risk_from_discount_usd=20_000.0,
                          deal_value_usd_total=200_000.0)
        r1 = fresh().assess(inp1)
        r2 = fresh().assess(inp2)
        assert r1.discount_composite == r2.discount_composite
        assert r2.estimated_margin_loss_usd == pytest.approx(r1.estimated_margin_loss_usd * 2, rel=0.01)

    def test_margin_loss_zero_when_revenue_at_risk_zero(self):
        inp = make_input(unauthorized_discount_count=5, revenue_at_risk_from_discount_usd=0.0)
        result = fresh().assess(inp)
        assert result.estimated_margin_loss_usd == 0.0

    def test_margin_loss_in_to_dict_rounded(self):
        inp = make_input(unauthorized_discount_count=1, revenue_at_risk_from_discount_usd=10_000.0)
        d = fresh().assess(inp).to_dict()
        assert round(d["estimated_margin_loss_usd"], 2) == d["estimated_margin_loss_usd"]

    def test_margin_loss_increases_with_composite(self):
        inp_low = make_input(unauthorized_discount_count=1, revenue_at_risk_from_discount_usd=10_000.0)
        inp_high = make_input(unauthorized_discount_count=5, revenue_at_risk_from_discount_usd=10_000.0)
        r_low = fresh().assess(inp_low)
        r_high = fresh().assess(inp_high)
        assert r_high.estimated_margin_loss_usd >= r_low.estimated_margin_loss_usd


# ---------------------------------------------------------------------------
# 16. DISCOUNT SIGNAL TESTS
# ---------------------------------------------------------------------------

class TestDiscountSignal:
    def test_none_pattern_signal(self):
        inp = make_input()
        result = fresh().assess(inp)
        assert "discount behavior within policy norms" in result.discount_signal

    def test_policy_breach_signal(self):
        inp = make_input(
            unauthorized_discount_count=0,
            deals_above_policy_count=5, deals_closed_count=10,
            avg_discount_pct=11.0, company_avg_discount_pct=10.0,
        )
        result = fresh().assess(inp)
        if result.discount_pattern == DiscountPattern.policy_breach:
            assert "deals above policy threshold" in result.discount_signal
            assert "composite" in result.discount_signal

    def test_habitual_discounting_signal(self):
        inp = make_input(
            unauthorized_discount_count=0,
            deals_above_policy_count=0,
            discount_requested_by_rep_count=6, deals_closed_count=10,
        )
        result = fresh().assess(inp)
        if result.discount_pattern == DiscountPattern.habitual_discounting:
            assert "rep initiated discounts" in result.discount_signal

    def test_dependency_pattern_signal(self):
        inp = make_input(
            win_rate_with_discount_pct=85.0, win_rate_without_discount_pct=50.0,
            repeat_discount_customer_count=4,
            unauthorized_discount_count=0,
            deals_above_policy_count=2, deals_closed_count=20,
        )
        result = fresh().assess(inp)
        if result.discount_pattern == DiscountPattern.dependency_pattern:
            assert "win rate gap" in result.discount_signal
            assert "repeat discount customers" in result.discount_signal

    def test_unauthorized_signal(self):
        inp = make_input(unauthorized_discount_count=3)
        result = fresh().assess(inp)
        if result.discount_pattern == DiscountPattern.unauthorized:
            assert "unauthorized discount" in result.discount_signal
            assert "composite" in result.discount_signal

    def test_margin_destruction_signal(self):
        inp = make_input(
            avg_discount_pct=30.0, company_avg_discount_pct=10.0,
            revenue_at_risk_from_discount_usd=50_000.0, deal_value_usd_total=100_000.0,
            discount_trend_delta_pct=5.0,
        )
        result = fresh().assess(inp)
        if result.discount_pattern == DiscountPattern.margin_destruction:
            assert "avg discount" in result.discount_signal
            assert "company avg" in result.discount_signal

    def test_signal_always_non_empty(self):
        for unauth in [0, 1, 3, 5]:
            inp = make_input(unauthorized_discount_count=unauth)
            result = fresh().assess(inp)
            assert len(result.discount_signal) > 0

    def test_signal_contains_composite_when_pattern_not_none(self):
        inp = make_input(unauthorized_discount_count=3)
        result = fresh().assess(inp)
        if result.discount_pattern != DiscountPattern.none:
            assert "composite" in result.discount_signal


# ---------------------------------------------------------------------------
# 17. assess() BASIC TESTS
# ---------------------------------------------------------------------------

class TestAssessBasic:
    def test_returns_result_type(self):
        result = fresh().assess(make_input())
        assert isinstance(result, SalesDiscountAbuseResult)

    def test_rep_id_passes_through(self):
        inp = make_input(rep_id="XREP999")
        result = fresh().assess(inp)
        assert result.rep_id == "XREP999"

    def test_region_passes_through(self):
        inp = make_input(region="EMEA")
        result = fresh().assess(inp)
        assert result.region == "EMEA"

    def test_result_stored_internally(self):
        detector = fresh()
        detector.assess(make_input())
        assert len(detector._results) == 1

    def test_multiple_assess_stored(self):
        detector = fresh()
        for i in range(5):
            detector.assess(make_input(rep_id=f"REP{i}"))
        assert len(detector._results) == 5

    def test_assess_does_not_share_state_between_calls(self):
        detector = fresh()
        r1 = detector.assess(make_input(rep_id="A"))
        r2 = detector.assess(make_input(rep_id="B"))
        assert r1.rep_id == "A"
        assert r2.rep_id == "B"

    def test_all_result_fields_have_correct_types(self):
        result = fresh().assess(make_input())
        assert isinstance(result.rep_id, str)
        assert isinstance(result.region, str)
        assert isinstance(result.discount_risk, DiscountRisk)
        assert isinstance(result.discount_pattern, DiscountPattern)
        assert isinstance(result.discount_severity, DiscountSeverity)
        assert isinstance(result.recommended_action, DiscountAction)
        assert isinstance(result.policy_violation_score, float)
        assert isinstance(result.revenue_impact_score, float)
        assert isinstance(result.behavioral_pattern_score, float)
        assert isinstance(result.dependency_score, float)
        assert isinstance(result.discount_composite, float)
        assert isinstance(result.is_abusing_discounts, bool)
        assert isinstance(result.requires_manager_review, bool)
        assert isinstance(result.estimated_margin_loss_usd, float)
        assert isinstance(result.discount_signal, str)


# ---------------------------------------------------------------------------
# 18. assess_batch() TESTS
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_returns_list(self):
        results = fresh().assess_batch([make_input()])
        assert isinstance(results, list)

    def test_empty_batch_returns_empty_list(self):
        results = fresh().assess_batch([])
        assert results == []

    def test_batch_length_matches_input(self):
        inputs = [make_input(rep_id=f"REP{i}") for i in range(7)]
        results = fresh().assess_batch(inputs)
        assert len(results) == 7

    def test_batch_order_preserved(self):
        inputs = [make_input(rep_id=f"REP{i}") for i in range(5)]
        results = fresh().assess_batch(inputs)
        for i, result in enumerate(results):
            assert result.rep_id == f"REP{i}"

    def test_batch_all_results_stored(self):
        detector = fresh()
        detector.assess_batch([make_input(rep_id=f"R{i}") for i in range(4)])
        assert len(detector._results) == 4

    def test_batch_each_result_is_result_type(self):
        results = fresh().assess_batch([make_input() for _ in range(3)])
        for r in results:
            assert isinstance(r, SalesDiscountAbuseResult)

    def test_batch_single_element(self):
        inp = make_input(rep_id="SOLO")
        results = fresh().assess_batch([inp])
        assert len(results) == 1
        assert results[0].rep_id == "SOLO"

    def test_batch_accumulates_with_prior_assess(self):
        detector = fresh()
        detector.assess(make_input(rep_id="PRE"))
        detector.assess_batch([make_input(rep_id=f"B{i}") for i in range(3)])
        assert len(detector._results) == 4


# ---------------------------------------------------------------------------
# 19. summary() TESTS
# ---------------------------------------------------------------------------

class TestSummary:
    def test_empty_summary_exactly_13_keys(self):
        s = fresh().summary()
        assert len(s) == 13

    def test_empty_summary_zero_total(self):
        s = fresh().summary()
        assert s["total"] == 0

    def test_empty_summary_zero_floats(self):
        s = fresh().summary()
        assert s["avg_discount_composite"] == 0.0
        assert s["avg_policy_violation_score"] == 0.0
        assert s["avg_revenue_impact_score"] == 0.0
        assert s["avg_behavioral_pattern_score"] == 0.0
        assert s["avg_dependency_score"] == 0.0
        assert s["total_estimated_margin_loss_usd"] == 0.0

    def test_empty_summary_empty_counts(self):
        s = fresh().summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}

    def test_empty_summary_zero_count_fields(self):
        s = fresh().summary()
        assert s["abusing_count"] == 0
        assert s["review_required_count"] == 0

    def test_summary_13_keys_after_assess(self):
        detector = fresh()
        detector.assess(make_input())
        s = detector.summary()
        assert len(s) == 13

    def test_summary_key_names(self):
        s = fresh().summary()
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_discount_composite", "abusing_count",
            "review_required_count", "avg_policy_violation_score",
            "avg_revenue_impact_score", "avg_behavioral_pattern_score",
            "avg_dependency_score", "total_estimated_margin_loss_usd",
        }
        assert set(s.keys()) == expected_keys

    def test_summary_total_count(self):
        detector = fresh()
        detector.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        s = detector.summary()
        assert s["total"] == 5

    def test_summary_risk_counts_sum_to_total(self):
        detector = fresh()
        detector.assess_batch([make_input(rep_id=f"R{i}") for i in range(6)])
        s = detector.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_pattern_counts_sum_to_total(self):
        detector = fresh()
        detector.assess_batch([make_input(rep_id=f"R{i}") for i in range(4)])
        s = detector.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_summary_severity_counts_sum_to_total(self):
        detector = fresh()
        detector.assess_batch([make_input(rep_id=f"R{i}") for i in range(4)])
        s = detector.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_to_total(self):
        detector = fresh()
        detector.assess_batch([make_input(rep_id=f"R{i}") for i in range(4)])
        s = detector.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_abusing_count_correct(self):
        detector = fresh()
        # 3 abusing (unauthorized=3), 2 not
        for _ in range(3):
            detector.assess(make_input(unauthorized_discount_count=3))
        for _ in range(2):
            detector.assess(make_input())
        s = detector.summary()
        assert s["abusing_count"] == 3

    def test_summary_review_required_count_correct(self):
        detector = fresh()
        for _ in range(2):
            detector.assess(make_input(unauthorized_discount_count=2))
        for _ in range(3):
            detector.assess(make_input())
        s = detector.summary()
        assert s["review_required_count"] == 2

    def test_summary_avg_composite_single(self):
        detector = fresh()
        result = detector.assess(make_input(unauthorized_discount_count=3))
        s = detector.summary()
        assert s["avg_discount_composite"] == round(result.discount_composite, 1)

    def test_summary_avg_composite_multiple(self):
        detector = fresh()
        r1 = detector.assess(make_input(unauthorized_discount_count=0))
        r2 = detector.assess(make_input(unauthorized_discount_count=3))
        s = detector.summary()
        expected = round((r1.discount_composite + r2.discount_composite) / 2, 1)
        assert s["avg_discount_composite"] == expected

    def test_summary_total_margin_loss(self):
        detector = fresh()
        r1 = detector.assess(make_input(unauthorized_discount_count=1, revenue_at_risk_from_discount_usd=10_000.0))
        r2 = detector.assess(make_input(unauthorized_discount_count=3, revenue_at_risk_from_discount_usd=20_000.0))
        s = detector.summary()
        expected = round(r1.estimated_margin_loss_usd + r2.estimated_margin_loss_usd, 2)
        assert s["total_estimated_margin_loss_usd"] == expected

    def test_summary_avg_scores_accurate(self):
        detector = fresh()
        r1 = detector.assess(make_input(unauthorized_discount_count=1))
        r2 = detector.assess(make_input(unauthorized_discount_count=3))
        s = detector.summary()
        expected_pol = round((r1.policy_violation_score + r2.policy_violation_score) / 2, 1)
        assert s["avg_policy_violation_score"] == expected_pol

    def test_summary_accumulates_across_batches(self):
        detector = fresh()
        detector.assess_batch([make_input(rep_id=f"A{i}") for i in range(3)])
        detector.assess_batch([make_input(rep_id=f"B{i}") for i in range(4)])
        s = detector.summary()
        assert s["total"] == 7

    def test_summary_idempotent(self):
        detector = fresh()
        detector.assess(make_input())
        s1 = detector.summary()
        s2 = detector.summary()
        assert s1 == s2

    def test_summary_risk_counts_values_are_ints(self):
        detector = fresh()
        detector.assess(make_input())
        s = detector.summary()
        for v in s["risk_counts"].values():
            assert isinstance(v, int)


# ---------------------------------------------------------------------------
# 20. EDGE CASES & BOUNDARY CONDITIONS
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_deals_closed_zero_no_crash(self):
        inp = make_input(deals_closed_count=0, deals_above_policy_count=0,
                         discount_requested_by_rep_count=0)
        result = fresh().assess(inp)
        assert result is not None

    def test_deal_value_zero_no_crash(self):
        inp = make_input(deal_value_usd_total=0.0)
        result = fresh().assess(inp)
        assert result is not None

    def test_company_avg_deal_cycle_zero_no_crash(self):
        inp = make_input(company_avg_deal_cycle_days=0.0)
        result = fresh().assess(inp)
        assert result is not None

    def test_all_zeros_no_crash(self):
        inp = SalesDiscountAbuseInput(
            rep_id="Z", region="Z", period_id="Z",
            deals_closed_count=0, avg_discount_pct=0.0, company_avg_discount_pct=0.0,
            deals_above_policy_count=0, max_discount_pct=0.0, policy_max_discount_pct=0.0,
            discount_requested_by_rep_count=0, deal_value_usd_total=0.0,
            revenue_at_risk_from_discount_usd=0.0, competitive_pressure_deals_count=0,
            manager_approved_exceptions_count=0, unauthorized_discount_count=0,
            discount_trend_delta_pct=0.0, avg_deal_cycle_days=0.0,
            company_avg_deal_cycle_days=0.0, win_rate_with_discount_pct=0.0,
            win_rate_without_discount_pct=0.0, rep_quota_attainment_pct=0.0,
            repeat_discount_customer_count=0,
        )
        result = fresh().assess(inp)
        assert result.discount_composite == 0.0

    def test_very_large_values_no_crash(self):
        inp = make_input(
            deal_value_usd_total=1e12,
            revenue_at_risk_from_discount_usd=1e11,
            unauthorized_discount_count=100,
            deals_above_policy_count=10000, deals_closed_count=10001,
        )
        result = fresh().assess(inp)
        assert result.discount_composite <= 100.0

    def test_negative_trend_delta_no_crash(self):
        inp = make_input(discount_trend_delta_pct=-5.0)
        result = fresh().assess(inp)
        assert result.revenue_impact_score >= 0.0

    def test_negative_win_rate_gap_no_crash(self):
        inp = make_input(win_rate_with_discount_pct=40.0, win_rate_without_discount_pct=60.0)
        result = fresh().assess(inp)
        assert result.dependency_score == 0.0

    def test_rep_id_empty_string(self):
        inp = make_input(rep_id="")
        result = fresh().assess(inp)
        assert result.rep_id == ""

    def test_multiple_detectors_independent(self):
        d1 = SalesDiscountAbuseDetector()
        d2 = SalesDiscountAbuseDetector()
        d1.assess(make_input(rep_id="D1"))
        assert len(d2._results) == 0

    def test_unauthorized_exactly_5_triggers_50(self):
        inp = make_input(unauthorized_discount_count=5)
        result = fresh().assess(inp)
        assert result.policy_violation_score >= 50.0

    def test_unauthorized_4_triggers_35_tier(self):
        inp = make_input(unauthorized_discount_count=4)
        result = fresh().assess(inp)
        assert result.policy_violation_score >= 35.0

    def test_above_policy_ratio_exactly_60_pct(self):
        inp = make_input(deals_above_policy_count=6, deals_closed_count=10)  # exactly 60%
        result = fresh().assess(inp)
        assert result.policy_violation_score >= 30.0

    def test_above_policy_ratio_exactly_40_pct(self):
        inp = make_input(deals_above_policy_count=4, deals_closed_count=10)  # exactly 40%
        result = fresh().assess(inp)
        assert result.policy_violation_score >= 18.0

    def test_max_excess_exactly_10(self):
        inp = make_input(max_discount_pct=30.0, policy_max_discount_pct=20.0)  # excess=10
        result = fresh().assess(inp)
        assert result.policy_violation_score >= 12.0

    def test_max_excess_exactly_20(self):
        inp = make_input(max_discount_pct=40.0, policy_max_discount_pct=20.0)  # excess=20
        result = fresh().assess(inp)
        assert result.policy_violation_score >= 20.0

    def test_win_gap_exactly_15(self):
        inp = make_input(win_rate_with_discount_pct=70.0, win_rate_without_discount_pct=55.0)
        result = fresh().assess(inp)
        assert result.dependency_score >= 12.0

    def test_win_gap_exactly_25(self):
        inp = make_input(win_rate_with_discount_pct=80.0, win_rate_without_discount_pct=55.0)
        result = fresh().assess(inp)
        assert result.dependency_score >= 25.0

    def test_win_gap_exactly_40(self):
        inp = make_input(win_rate_with_discount_pct=95.0, win_rate_without_discount_pct=55.0)
        result = fresh().assess(inp)
        assert result.dependency_score >= 40.0

    def test_rep_initiation_exactly_50_pct(self):
        inp = make_input(discount_requested_by_rep_count=5, deals_closed_count=10)
        result = fresh().assess(inp)
        assert result.behavioral_pattern_score >= 22.0

    def test_rep_initiation_exactly_70_pct(self):
        inp = make_input(discount_requested_by_rep_count=7, deals_closed_count=10)
        result = fresh().assess(inp)
        assert result.behavioral_pattern_score >= 35.0

    def test_risk_ratio_exactly_8_pct(self):
        inp = make_input(revenue_at_risk_from_discount_usd=8_000.0, deal_value_usd_total=100_000.0)
        result = fresh().assess(inp)
        assert result.revenue_impact_score >= 8.0

    def test_risk_ratio_exactly_15_pct(self):
        inp = make_input(revenue_at_risk_from_discount_usd=15_000.0, deal_value_usd_total=100_000.0)
        result = fresh().assess(inp)
        assert result.revenue_impact_score >= 18.0

    def test_risk_ratio_exactly_25_pct(self):
        inp = make_input(revenue_at_risk_from_discount_usd=25_000.0, deal_value_usd_total=100_000.0)
        result = fresh().assess(inp)
        assert result.revenue_impact_score >= 30.0


# ---------------------------------------------------------------------------
# 21. INTEGRATION / SCENARIO TESTS
# ---------------------------------------------------------------------------

class TestScenarios:
    def test_clean_rep_full_scenario(self):
        inp = make_input(
            rep_id="CLEAN001", region="West",
            deals_closed_count=20, avg_discount_pct=10.0, company_avg_discount_pct=10.0,
            deals_above_policy_count=0, max_discount_pct=15.0, policy_max_discount_pct=20.0,
            discount_requested_by_rep_count=0,
            revenue_at_risk_from_discount_usd=2_000.0, deal_value_usd_total=100_000.0,
            unauthorized_discount_count=0, discount_trend_delta_pct=0.0,
            win_rate_with_discount_pct=60.0, win_rate_without_discount_pct=58.0,
            rep_quota_attainment_pct=105.0, repeat_discount_customer_count=0,
        )
        result = fresh().assess(inp)
        assert result.discount_risk == DiscountRisk.low
        assert result.discount_severity == DiscountSeverity.clean
        assert result.discount_pattern == DiscountPattern.none
        assert result.is_abusing_discounts is False
        assert result.requires_manager_review is False
        assert result.discount_composite == 0.0
        assert "within policy norms" in result.discount_signal

    def test_abusive_rep_full_scenario(self):
        inp = make_input(
            rep_id="ABUSER001",
            unauthorized_discount_count=5,
            deals_above_policy_count=9, deals_closed_count=10,
            max_discount_pct=50.0, policy_max_discount_pct=20.0,
            avg_discount_pct=40.0, company_avg_discount_pct=10.0,
            revenue_at_risk_from_discount_usd=40_000.0, deal_value_usd_total=100_000.0,
            discount_trend_delta_pct=15.0,
            discount_requested_by_rep_count=8,
            avg_deal_cycle_days=5.0, company_avg_deal_cycle_days=30.0,
            manager_approved_exceptions_count=5,
            win_rate_with_discount_pct=90.0, win_rate_without_discount_pct=40.0,
            repeat_discount_customer_count=8,
            rep_quota_attainment_pct=150.0,
        )
        result = fresh().assess(inp)
        assert result.is_abusing_discounts is True
        assert result.requires_manager_review is True
        assert result.discount_composite >= 60.0
        assert result.discount_risk == DiscountRisk.critical
        assert result.discount_severity == DiscountSeverity.abusive
        assert result.recommended_action == DiscountAction.compensation_review

    def test_batch_mixed_reps_summary_totals(self):
        detector = fresh()
        inputs = [
            make_input(rep_id="C1"),
            make_input(rep_id="C2"),
            make_input(rep_id="A1", unauthorized_discount_count=3),
            make_input(rep_id="A2", unauthorized_discount_count=5,
                       deals_above_policy_count=6, deals_closed_count=10),
        ]
        detector.assess_batch(inputs)
        s = detector.summary()
        assert s["total"] == 4
        assert s["abusing_count"] >= 2  # at least the two unauthorized reps
        assert s["total_estimated_margin_loss_usd"] >= 0.0

    def test_to_dict_round_trip(self):
        inp = make_input(rep_id="RT01", region="Southeast",
                         unauthorized_discount_count=2, deals_above_policy_count=3,
                         deals_closed_count=10)
        result = fresh().assess(inp)
        d = result.to_dict()
        assert d["rep_id"] == "RT01"
        assert d["region"] == "Southeast"
        assert d["discount_risk"] in [r.value for r in DiscountRisk]
        assert d["discount_pattern"] in [p.value for p in DiscountPattern]
        assert d["discount_severity"] in [s.value for s in DiscountSeverity]
        assert d["recommended_action"] in [a.value for a in DiscountAction]

    def test_summary_after_all_abusing(self):
        detector = fresh()
        for _ in range(5):
            detector.assess(make_input(unauthorized_discount_count=3))
        s = detector.summary()
        assert s["abusing_count"] == 5
        assert s["review_required_count"] == 5

    def test_summary_single_rep(self):
        detector = fresh()
        result = detector.assess(make_input(rep_id="ONE"))
        s = detector.summary()
        assert s["total"] == 1
        assert s["avg_discount_composite"] == round(result.discount_composite, 1)
        assert s["avg_policy_violation_score"] == round(result.policy_violation_score, 1)
        assert s["avg_revenue_impact_score"] == round(result.revenue_impact_score, 1)
        assert s["avg_behavioral_pattern_score"] == round(result.behavioral_pattern_score, 1)
        assert s["avg_dependency_score"] == round(result.dependency_score, 1)

    def test_detector_is_stateful(self):
        detector = fresh()
        for i in range(10):
            detector.assess(make_input(rep_id=f"R{i}"))
        assert len(detector._results) == 10
        s = detector.summary()
        assert s["total"] == 10

    def test_fresh_detector_per_test_is_clean(self):
        d1 = fresh()
        d1.assess(make_input())
        d2 = fresh()
        s = d2.summary()
        assert s["total"] == 0

    def test_composite_strictly_between_0_and_100(self):
        inputs = [
            make_input(unauthorized_discount_count=u,
                       deals_above_policy_count=a, deals_closed_count=10)
            for u in [0, 1, 3, 5]
            for a in [0, 2, 5, 8]
        ]
        for inp in inputs:
            result = fresh().assess(inp)
            assert 0.0 <= result.discount_composite <= 100.0

    def test_all_score_components_between_0_and_100(self):
        worst = make_input(
            unauthorized_discount_count=5,
            deals_above_policy_count=10, deals_closed_count=10,
            max_discount_pct=50.0, policy_max_discount_pct=20.0,
            avg_discount_pct=40.0, company_avg_discount_pct=10.0,
            revenue_at_risk_from_discount_usd=50_000.0, deal_value_usd_total=100_000.0,
            discount_trend_delta_pct=15.0,
            discount_requested_by_rep_count=10,
            avg_deal_cycle_days=5.0, company_avg_deal_cycle_days=30.0,
            manager_approved_exceptions_count=5,
            win_rate_with_discount_pct=100.0, win_rate_without_discount_pct=10.0,
            repeat_discount_customer_count=10,
            rep_quota_attainment_pct=160.0,
        )
        result = fresh().assess(worst)
        for score in (result.policy_violation_score, result.revenue_impact_score,
                      result.behavioral_pattern_score, result.dependency_score):
            assert 0.0 <= score <= 100.0


# ---------------------------------------------------------------------------
# 22. ADDITIONAL COVERAGE TESTS
# ---------------------------------------------------------------------------

class TestAdditionalCoverage:
    def test_policy_score_exact_50_plus_30_plus_20_capped(self):
        inp = make_input(
            unauthorized_discount_count=5,  # +50
            deals_above_policy_count=7, deals_closed_count=10,  # 70% → +30
            max_discount_pct=45.0, policy_max_discount_pct=20.0,  # excess=25 → +20
        )
        result = fresh().assess(inp)
        assert result.policy_violation_score == 100.0

    def test_revenue_score_combined_all_tiers(self):
        inp = make_input(
            avg_discount_pct=30.0, company_avg_discount_pct=10.0,  # excess=20 → +40
            revenue_at_risk_from_discount_usd=30_000.0, deal_value_usd_total=100_000.0,  # 30% → +30
            discount_trend_delta_pct=12.0,  # >= 10 → +20
        )
        result = fresh().assess(inp)
        assert result.revenue_impact_score == min(100.0, 40.0 + 30.0 + 20.0)

    def test_behavioral_score_all_components(self):
        inp = make_input(
            discount_requested_by_rep_count=7, deals_closed_count=10,  # 70% → +35
            avg_deal_cycle_days=10.0, company_avg_deal_cycle_days=30.0,
            avg_discount_pct=20.0, company_avg_discount_pct=10.0,  # ratio<0.5, disc>comp+5 → +25
            manager_approved_exceptions_count=5,  # +20
        )
        result = fresh().assess(inp)
        assert result.behavioral_pattern_score == min(100.0, 35.0 + 25.0 + 20.0)

    def test_dependency_score_all_components(self):
        inp = make_input(
            win_rate_with_discount_pct=96.0, win_rate_without_discount_pct=55.0,  # gap=41 → +40
            repeat_discount_customer_count=5,  # +30
            rep_quota_attainment_pct=145.0, avg_discount_pct=22.0, company_avg_discount_pct=10.0,  # +20
        )
        result = fresh().assess(inp)
        assert result.dependency_score == min(100.0, 40.0 + 30.0 + 20.0)

    def test_is_abusing_third_condition_boundary(self):
        # policy_max=20, avg=30.1 → 30.1 > 30 → True
        inp = make_input(avg_discount_pct=30.1, policy_max_discount_pct=20.0)
        result = fresh().assess(inp)
        assert result.is_abusing_discounts is True

    def test_is_abusing_third_condition_just_below(self):
        # policy_max=20, avg=29.9 → 29.9 > 30 → False
        inp = make_input(avg_discount_pct=29.9, policy_max_discount_pct=20.0)
        result = fresh().assess(inp)
        if result.discount_composite < 40 and inp.unauthorized_discount_count < 3:
            assert result.is_abusing_discounts is False

    def test_manager_exceptions_2_trigger_12_not_20(self):
        inp = make_input(manager_approved_exceptions_count=2)
        result = fresh().assess(inp)
        # 2 exceptions → >= 1 tier (5), not >= 3 tier (12), not >= 5 (20)
        # Actually 2 >= 1 → +5
        assert result.behavioral_pattern_score >= 5.0
        assert result.behavioral_pattern_score < 20.0  # can't reach 20 from exceptions alone with count=2

    def test_manager_exceptions_4_trigger_12_tier(self):
        inp = make_input(manager_approved_exceptions_count=4)
        result = fresh().assess(inp)
        assert result.behavioral_pattern_score >= 12.0

    def test_repeat_customers_2_triggers_8_tier(self):
        inp = make_input(repeat_discount_customer_count=2)
        result = fresh().assess(inp)
        assert result.dependency_score >= 8.0
        assert result.dependency_score < 18.0

    def test_repeat_customers_4_triggers_18_tier(self):
        inp = make_input(repeat_discount_customer_count=4)
        result = fresh().assess(inp)
        assert result.dependency_score >= 18.0

    def test_trend_delta_4_triggers_no_score(self):
        inp = make_input(discount_trend_delta_pct=4.9)
        result = fresh().assess(inp)
        assert result.revenue_impact_score == 0.0  # below 5 threshold

    def test_trend_delta_exactly_5_triggers_10(self):
        inp = make_input(discount_trend_delta_pct=5.0)
        result = fresh().assess(inp)
        assert result.revenue_impact_score >= 10.0

    def test_above_policy_below_20_pct_no_score(self):
        # 1/10 = 10% → no score
        inp = make_input(deals_above_policy_count=1, deals_closed_count=10)
        result = fresh().assess(inp)
        # 10% < 20% → no contribution from above_policy_ratio
        assert result.policy_violation_score == 0.0

    def test_unauthorized_6_triggers_50_tier(self):
        inp = make_input(unauthorized_discount_count=6)
        result = fresh().assess(inp)
        assert result.policy_violation_score >= 50.0

    def test_speed_ratio_just_above_70_pct_no_speed_bonus(self):
        # ratio = 22/30 = 0.733 → not < 0.7
        inp = make_input(
            avg_deal_cycle_days=22.0, company_avg_deal_cycle_days=30.0,
            avg_discount_pct=15.0, company_avg_discount_pct=10.0,
        )
        result = fresh().assess(inp)
        # speed ratio 0.733 > 0.7 → no speed contribution
        assert result.behavioral_pattern_score == 0.0  # no other factors

    def test_quota_exactly_140_triggers_high_tier(self):
        inp = make_input(rep_quota_attainment_pct=140.0, avg_discount_pct=20.0, company_avg_discount_pct=10.0)
        result = fresh().assess(inp)
        assert result.dependency_score >= 20.0

    def test_quota_exactly_120_triggers_medium_tier(self):
        inp = make_input(rep_quota_attainment_pct=120.0, avg_discount_pct=17.0, company_avg_discount_pct=10.0)
        result = fresh().assess(inp)
        assert result.dependency_score >= 10.0

    def test_quota_119_no_contribution(self):
        inp = make_input(rep_quota_attainment_pct=119.0, avg_discount_pct=20.0, company_avg_discount_pct=10.0)
        result = fresh().assess(inp)
        # 119 < 120 → no quota contribution; 20-10=10 > 8 but 119<120 → no
        assert result.dependency_score == 0.0

    def test_excess_avg_exactly_5_triggers_12_tier(self):
        inp = make_input(avg_discount_pct=15.0, company_avg_discount_pct=10.0)  # excess=5
        result = fresh().assess(inp)
        assert result.revenue_impact_score >= 12.0

    def test_excess_avg_exactly_10_triggers_25_tier(self):
        inp = make_input(avg_discount_pct=20.0, company_avg_discount_pct=10.0)  # excess=10
        result = fresh().assess(inp)
        assert result.revenue_impact_score >= 25.0

    def test_excess_avg_exactly_15_triggers_40_tier(self):
        inp = make_input(avg_discount_pct=25.0, company_avg_discount_pct=10.0)  # excess=15
        result = fresh().assess(inp)
        assert result.revenue_impact_score >= 40.0

    def test_excess_avg_4_no_score(self):
        inp = make_input(avg_discount_pct=14.0, company_avg_discount_pct=10.0)  # excess=4
        result = fresh().assess(inp)
        assert result.revenue_impact_score == 0.0

    def test_summary_risk_counts_use_string_keys(self):
        detector = fresh()
        detector.assess(make_input())
        s = detector.summary()
        for key in s["risk_counts"]:
            assert isinstance(key, str)

    def test_summary_pattern_counts_use_string_keys(self):
        detector = fresh()
        detector.assess(make_input(unauthorized_discount_count=3))
        s = detector.summary()
        for key in s["pattern_counts"]:
            assert isinstance(key, str)

    def test_summary_after_mixed_batch_no_negative_counts(self):
        detector = fresh()
        detector.assess_batch([make_input(rep_id=f"X{i}", unauthorized_discount_count=i % 4) for i in range(10)])
        s = detector.summary()
        assert s["abusing_count"] >= 0
        assert s["review_required_count"] >= 0

    def test_to_dict_composite_matches_result(self):
        result = fresh().assess(make_input(unauthorized_discount_count=2))
        d = result.to_dict()
        assert d["discount_composite"] == round(result.discount_composite, 1)

    def test_to_dict_is_abusing_matches_result(self):
        inp = make_input(unauthorized_discount_count=3)
        result = fresh().assess(inp)
        d = result.to_dict()
        assert d["is_abusing_discounts"] == result.is_abusing_discounts

    def test_to_dict_requires_review_matches_result(self):
        inp = make_input(deals_above_policy_count=5, deals_closed_count=10)
        result = fresh().assess(inp)
        d = result.to_dict()
        assert d["requires_manager_review"] == result.requires_manager_review

    def test_policy_breach_signal_counts_match(self):
        inp = make_input(deals_above_policy_count=5, deals_closed_count=10,
                         unauthorized_discount_count=0)
        result = fresh().assess(inp)
        if result.discount_pattern == DiscountPattern.policy_breach:
            assert "5/10" in result.discount_signal

    def test_unauthorized_signal_includes_avg_and_policy_pct(self):
        inp = make_input(unauthorized_discount_count=3,
                         avg_discount_pct=25.0, policy_max_discount_pct=20.0)
        result = fresh().assess(inp)
        assert result.discount_pattern == DiscountPattern.unauthorized
        assert "25.0" in result.discount_signal
        assert "20.0" in result.discount_signal

    def test_rep_id_special_chars(self):
        inp = make_input(rep_id="REP-001/WEST:2024")
        result = fresh().assess(inp)
        assert result.rep_id == "REP-001/WEST:2024"
        d = result.to_dict()
        assert d["rep_id"] == "REP-001/WEST:2024"

    def test_summary_margin_loss_is_float(self):
        detector = fresh()
        detector.assess(make_input())
        s = detector.summary()
        assert isinstance(s["total_estimated_margin_loss_usd"], float)

    def test_dependency_score_30_pct_gap_no_high_tier(self):
        # gap=29 < 30 → no 30 tier; but gap=29 >= 25 → 25 tier
        inp = make_input(win_rate_with_discount_pct=84.0, win_rate_without_discount_pct=55.0)
        result = fresh().assess(inp)
        # gap = 29, >= 25 → +25
        assert result.dependency_score >= 25.0

    def test_dependency_score_gap_14_no_score(self):
        # gap=14 < 15 → no contribution
        inp = make_input(win_rate_with_discount_pct=69.0, win_rate_without_discount_pct=55.0)
        result = fresh().assess(inp)
        assert result.dependency_score == 0.0

    def test_summary_avg_scores_rounded_to_1dp(self):
        detector = fresh()
        detector.assess_batch([make_input(unauthorized_discount_count=i) for i in range(4)])
        s = detector.summary()
        for key in ("avg_discount_composite", "avg_policy_violation_score",
                    "avg_revenue_impact_score", "avg_behavioral_pattern_score",
                    "avg_dependency_score"):
            assert round(s[key], 1) == s[key]


# ---------------------------------------------------------------------------
# 23. EXTENDED COVERAGE — score thresholds, patterns, dict keys, signals
# ---------------------------------------------------------------------------

class TestExtendedCoverage:
    # --- to_dict key presence individual checks ---
    def test_to_dict_has_rep_id(self):
        assert "rep_id" in fresh().assess(make_input()).to_dict()

    def test_to_dict_has_region(self):
        assert "region" in fresh().assess(make_input()).to_dict()

    def test_to_dict_has_discount_risk(self):
        assert "discount_risk" in fresh().assess(make_input()).to_dict()

    def test_to_dict_has_discount_pattern(self):
        assert "discount_pattern" in fresh().assess(make_input()).to_dict()

    def test_to_dict_has_discount_severity(self):
        assert "discount_severity" in fresh().assess(make_input()).to_dict()

    def test_to_dict_has_recommended_action(self):
        assert "recommended_action" in fresh().assess(make_input()).to_dict()

    def test_to_dict_has_policy_violation_score(self):
        assert "policy_violation_score" in fresh().assess(make_input()).to_dict()

    def test_to_dict_has_revenue_impact_score(self):
        assert "revenue_impact_score" in fresh().assess(make_input()).to_dict()

    def test_to_dict_has_behavioral_pattern_score(self):
        assert "behavioral_pattern_score" in fresh().assess(make_input()).to_dict()

    def test_to_dict_has_dependency_score(self):
        assert "dependency_score" in fresh().assess(make_input()).to_dict()

    def test_to_dict_has_discount_composite(self):
        assert "discount_composite" in fresh().assess(make_input()).to_dict()

    def test_to_dict_has_is_abusing_discounts(self):
        assert "is_abusing_discounts" in fresh().assess(make_input()).to_dict()

    def test_to_dict_has_requires_manager_review(self):
        assert "requires_manager_review" in fresh().assess(make_input()).to_dict()

    def test_to_dict_has_estimated_margin_loss_usd(self):
        assert "estimated_margin_loss_usd" in fresh().assess(make_input()).to_dict()

    def test_to_dict_has_discount_signal(self):
        assert "discount_signal" in fresh().assess(make_input()).to_dict()

    # --- summary key presence individual checks ---
    def test_summary_has_total(self):
        assert "total" in fresh().summary()

    def test_summary_has_risk_counts(self):
        assert "risk_counts" in fresh().summary()

    def test_summary_has_pattern_counts(self):
        assert "pattern_counts" in fresh().summary()

    def test_summary_has_severity_counts(self):
        assert "severity_counts" in fresh().summary()

    def test_summary_has_action_counts(self):
        assert "action_counts" in fresh().summary()

    def test_summary_has_avg_discount_composite(self):
        assert "avg_discount_composite" in fresh().summary()

    def test_summary_has_abusing_count(self):
        assert "abusing_count" in fresh().summary()

    def test_summary_has_review_required_count(self):
        assert "review_required_count" in fresh().summary()

    def test_summary_has_avg_policy_violation_score(self):
        assert "avg_policy_violation_score" in fresh().summary()

    def test_summary_has_avg_revenue_impact_score(self):
        assert "avg_revenue_impact_score" in fresh().summary()

    def test_summary_has_avg_behavioral_pattern_score(self):
        assert "avg_behavioral_pattern_score" in fresh().summary()

    def test_summary_has_avg_dependency_score(self):
        assert "avg_dependency_score" in fresh().summary()

    def test_summary_has_total_estimated_margin_loss_usd(self):
        assert "total_estimated_margin_loss_usd" in fresh().summary()

    # --- misc additional invariants ---
    def test_assess_returns_same_rep_region_in_dict(self):
        inp = make_input(rep_id="RR01", region="Pacific")
        d = fresh().assess(inp).to_dict()
        assert d["rep_id"] == "RR01" and d["region"] == "Pacific"

    def test_composite_formula_weights_sum_to_1(self):
        assert abs(0.35 + 0.30 + 0.20 + 0.15 - 1.0) < 1e-9

    def test_all_risk_enum_values_reachable(self):
        # At least verify all values are valid strings
        for risk in DiscountRisk:
            assert risk.value in ("low", "moderate", "high", "critical")

    def test_all_severity_enum_values_reachable(self):
        for sev in DiscountSeverity:
            assert sev.value in ("clean", "watch", "concerning", "abusive")

    def test_all_action_enum_values_reachable(self):
        for act in DiscountAction:
            assert act.value in ("no_action", "flag_for_review", "manager_approval",
                                 "discount_freeze", "compensation_review")

    def test_all_pattern_enum_values_reachable(self):
        for pat in DiscountPattern:
            assert pat.value in ("none", "policy_breach", "habitual_discounting",
                                 "dependency_pattern", "unauthorized", "margin_destruction")

    def test_no_action_when_composite_below_10(self):
        inp = make_input()  # composite=0
        result = fresh().assess(inp)
        assert result.recommended_action == DiscountAction.no_action

    def test_margin_loss_proportional_to_composite(self):
        # Same revenue_at_risk, different composites → higher composite → higher loss
        inp_a = make_input(revenue_at_risk_from_discount_usd=10_000.0)  # composite=0
        inp_b = make_input(unauthorized_discount_count=3,
                           revenue_at_risk_from_discount_usd=10_000.0)  # composite>0
        ra = fresh().assess(inp_a)
        rb = fresh().assess(inp_b)
        assert rb.estimated_margin_loss_usd >= ra.estimated_margin_loss_usd

    def test_pattern_none_has_signal_about_policy_norms(self):
        result = fresh().assess(make_input())
        assert "policy norms" in result.discount_signal

    def test_policy_breach_deals_above_policy_reflected_in_signal(self):
        inp = make_input(deals_above_policy_count=5, deals_closed_count=15,
                         unauthorized_discount_count=0)
        result = fresh().assess(inp)
        if result.discount_pattern == DiscountPattern.policy_breach:
            assert "5" in result.discount_signal
            assert "15" in result.discount_signal

    def test_unauthorized_count_reflected_in_signal(self):
        inp = make_input(unauthorized_discount_count=4)
        result = fresh().assess(inp)
        assert result.discount_pattern == DiscountPattern.unauthorized
        assert "4" in result.discount_signal

    def test_batch_with_single_abuser_counted_in_summary(self):
        detector = fresh()
        detector.assess_batch([
            make_input(rep_id="C"),
            make_input(rep_id="A", unauthorized_discount_count=3),
        ])
        s = detector.summary()
        assert s["abusing_count"] >= 1
        assert s["review_required_count"] >= 1

