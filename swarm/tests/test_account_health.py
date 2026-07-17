"""
Comprehensive pytest tests for swarm/intelligence/account_health.py

Covers all dimension scorers, tier logic, churn/expansion/action/forecast helpers,
signal detection, AccountHealthMonitor methods, and edge cases.
"""

from __future__ import annotations

import math
import pytest

from swarm.intelligence.account_health import (
    AccountHealthMonitor,
    AccountMetrics,
    AccountHealth,
    HealthTier,
    AccountAction,
    ContractType,
    _engagement,
    _adoption,
    _financial,
    _relationship,
    _health_tier,
    _churn_risk,
    _expansion_potential,
    _primary_action,
    _renewal_forecast,
)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def make_account(
    account_id: str = "acc-001",
    account_name: str = "Test Corp",
    industry: str = "SaaS",
    contract_type: ContractType = ContractType.ANNUAL,
    arr_eur: float = 60_000.0,
    contract_start_date: str = "2024-01-01",
    days_until_renewal: int = 180,
    dau_wau_ratio: float = 0.4,
    feature_adoption_pct: float = 70.0,
    logins_last_30d: int = 25,
    api_calls_last_30d: int = 1_000,
    features_used: int = 7,
    total_features: int = 10,
    integrations_active: int = 2,
    users_active: int = 10,
    users_licensed: int = 15,
    payments_on_time_pct: float = 98.0,
    overdue_invoices: int = 0,
    expansion_revenue_eur: float = 0.0,
    nps_score: int = 40,
    support_tickets_open: int = 1,
    support_tickets_30d: int = 3,
    executive_contacts: int = 2,
    last_qbr_days: int = 45,
    csm_sentiment: float = 75.0,
    usage_pct_of_limit: float = 50.0,
) -> AccountMetrics:
    return AccountMetrics(
        account_id=account_id,
        account_name=account_name,
        industry=industry,
        contract_type=contract_type,
        arr_eur=arr_eur,
        contract_start_date=contract_start_date,
        days_until_renewal=days_until_renewal,
        dau_wau_ratio=dau_wau_ratio,
        feature_adoption_pct=feature_adoption_pct,
        logins_last_30d=logins_last_30d,
        api_calls_last_30d=api_calls_last_30d,
        features_used=features_used,
        total_features=total_features,
        integrations_active=integrations_active,
        users_active=users_active,
        users_licensed=users_licensed,
        payments_on_time_pct=payments_on_time_pct,
        overdue_invoices=overdue_invoices,
        expansion_revenue_eur=expansion_revenue_eur,
        nps_score=nps_score,
        support_tickets_open=support_tickets_open,
        support_tickets_30d=support_tickets_30d,
        executive_contacts=executive_contacts,
        last_qbr_days=last_qbr_days,
        csm_sentiment=csm_sentiment,
        usage_pct_of_limit=usage_pct_of_limit,
    )


# ─── _engagement tests ────────────────────────────────────────────────────────

class TestEngagement:
    def test_returns_tuple_of_three(self):
        a = make_account()
        result = _engagement(a)
        assert isinstance(result, tuple) and len(result) == 3

    def test_score_is_float(self):
        score, _, _ = _engagement(make_account())
        assert isinstance(score, float)

    def test_dau_score_capped_at_100(self):
        # ratio=1.0 → dau_score=200, capped to 100
        score, _, _ = _engagement(make_account(dau_wau_ratio=1.0, logins_last_30d=0, api_calls_last_30d=1))
        # dau=100*0.45 + 0 + 0 = 45
        assert score == pytest.approx(45.0, abs=0.1)

    def test_dau_score_at_0_5_ratio(self):
        # 0.5 * 200 = 100 → capped at 100
        score, _, _ = _engagement(make_account(dau_wau_ratio=0.5, logins_last_30d=0, api_calls_last_30d=1))
        assert score == pytest.approx(45.0, abs=0.1)

    def test_dau_score_below_cap(self):
        # 0.25 * 200 = 50
        score, _, _ = _engagement(make_account(dau_wau_ratio=0.25, logins_last_30d=0, api_calls_last_30d=1))
        assert score == pytest.approx(50 * 0.45, abs=0.1)

    def test_login_score_at_20_logins(self):
        # 20 logins = 100
        score, _, _ = _engagement(make_account(dau_wau_ratio=0.0, logins_last_30d=20, api_calls_last_30d=1))
        assert score == pytest.approx(100 * 0.30, abs=0.1)

    def test_login_score_capped_at_20_plus(self):
        score, _, _ = _engagement(make_account(dau_wau_ratio=0.0, logins_last_30d=40, api_calls_last_30d=1))
        assert score == pytest.approx(100 * 0.30, abs=0.1)

    def test_login_score_zero_logins(self):
        score, _, _ = _engagement(make_account(dau_wau_ratio=0.0, logins_last_30d=0, api_calls_last_30d=1))
        assert score == pytest.approx(0.0, abs=0.1)

    def test_api_score_at_10000_calls(self):
        # log10(10000)/4 * 100 = 1.0 * 100 = 100
        score, _, _ = _engagement(make_account(dau_wau_ratio=0.0, logins_last_30d=0, api_calls_last_30d=10_000))
        assert score == pytest.approx(100 * 0.25, abs=0.1)

    def test_api_score_at_1_call(self):
        # log10(1)/4 * 100 = 0
        score, _, _ = _engagement(make_account(dau_wau_ratio=0.0, logins_last_30d=0, api_calls_last_30d=1))
        assert score == pytest.approx(0.0, abs=0.1)

    def test_api_score_at_0_calls_treated_as_1(self):
        # max(1, 0) = 1 → same as 1 call
        score, _, _ = _engagement(make_account(dau_wau_ratio=0.0, logins_last_30d=0, api_calls_last_30d=0))
        assert score == pytest.approx(0.0, abs=0.1)

    def test_api_score_above_10000_capped(self):
        score, _, _ = _engagement(make_account(dau_wau_ratio=0.0, logins_last_30d=0, api_calls_last_30d=100_000))
        assert score == pytest.approx(100 * 0.25, abs=0.1)

    def test_high_engagement_signal_at_0_35(self):
        _, good, bad = _engagement(make_account(dau_wau_ratio=0.35))
        assert "high_engagement" in good
        assert "low_engagement" not in bad

    def test_high_engagement_signal_above_0_35(self):
        _, good, _ = _engagement(make_account(dau_wau_ratio=0.8))
        assert "high_engagement" in good

    def test_no_high_engagement_below_0_35(self):
        _, good, _ = _engagement(make_account(dau_wau_ratio=0.34))
        assert "high_engagement" not in good

    def test_low_engagement_signal_below_0_10(self):
        _, _, bad = _engagement(make_account(dau_wau_ratio=0.09))
        assert "low_engagement" in bad

    def test_low_engagement_signal_at_exactly_0_10_not_flagged(self):
        _, _, bad = _engagement(make_account(dau_wau_ratio=0.10))
        assert "low_engagement" not in bad

    def test_no_signal_in_middle_range(self):
        _, good, bad = _engagement(make_account(dau_wau_ratio=0.20))
        assert "high_engagement" not in good
        assert "low_engagement" not in bad

    def test_composite_score_formula(self):
        a = make_account(dau_wau_ratio=0.4, logins_last_30d=20, api_calls_last_30d=10_000)
        dau = min(100, 0.4 * 200)   # 80
        login = min(100, 20 / 20 * 100)  # 100
        api = min(100, math.log10(10_000) / 4 * 100)  # 100
        expected = round(dau * 0.45 + login * 0.30 + api * 0.25, 2)
        score, _, _ = _engagement(a)
        assert score == pytest.approx(expected, abs=0.01)

    def test_all_zeros_score(self):
        score, _, _ = _engagement(make_account(dau_wau_ratio=0.0, logins_last_30d=0, api_calls_last_30d=0))
        assert score == pytest.approx(0.0, abs=0.01)

    def test_score_rounded_to_two_decimals(self):
        score, _, _ = _engagement(make_account(dau_wau_ratio=0.33, logins_last_30d=7, api_calls_last_30d=123))
        assert score == round(score, 2)


# ─── _adoption tests ──────────────────────────────────────────────────────────

class TestAdoption:
    def test_returns_tuple_of_three(self):
        result = _adoption(make_account())
        assert isinstance(result, tuple) and len(result) == 3

    def test_feature_score_capped_at_100(self):
        score, _, _ = _adoption(make_account(feature_adoption_pct=120.0, users_active=0, users_licensed=0, integrations_active=0, usage_pct_of_limit=0))
        assert score == pytest.approx(100 * 0.45, abs=0.1)

    def test_feature_score_at_exactly_100(self):
        score, _, _ = _adoption(make_account(feature_adoption_pct=100.0, users_active=0, users_licensed=0, integrations_active=0, usage_pct_of_limit=0))
        assert score == pytest.approx(100 * 0.45, abs=0.1)

    def test_user_ratio_with_licensed_users(self):
        # 10 active / 20 licensed = 50%
        a = make_account(users_active=10, users_licensed=20, feature_adoption_pct=0, integrations_active=0, usage_pct_of_limit=0)
        score, _, _ = _adoption(a)
        assert score == pytest.approx(50 * 0.35, abs=0.1)

    def test_user_ratio_capped_at_100(self):
        # 20 active / 10 licensed = 200%, capped at 100
        a = make_account(users_active=20, users_licensed=10, feature_adoption_pct=0, integrations_active=0, usage_pct_of_limit=0)
        score, _, _ = _adoption(a)
        assert score == pytest.approx(100 * 0.35, abs=0.1)

    def test_user_ratio_zero_licensed(self):
        a = make_account(users_active=5, users_licensed=0, feature_adoption_pct=0, integrations_active=0, usage_pct_of_limit=0)
        score, _, _ = _adoption(a)
        assert score == pytest.approx(0.0, abs=0.1)

    def test_integration_score_at_4(self):
        # 4 * 25 = 100
        a = make_account(feature_adoption_pct=0, users_active=0, users_licensed=0, integrations_active=4, usage_pct_of_limit=0)
        score, _, _ = _adoption(a)
        assert score == pytest.approx(100 * 0.20, abs=0.1)

    def test_integration_score_capped_above_4(self):
        a = make_account(feature_adoption_pct=0, users_active=0, users_licensed=0, integrations_active=10, usage_pct_of_limit=0)
        score, _, _ = _adoption(a)
        assert score == pytest.approx(100 * 0.20, abs=0.1)

    def test_integration_score_at_2(self):
        a = make_account(feature_adoption_pct=0, users_active=0, users_licensed=0, integrations_active=2, usage_pct_of_limit=0)
        score, _, _ = _adoption(a)
        assert score == pytest.approx(50 * 0.20, abs=0.1)

    def test_strong_adoption_at_70(self):
        _, good, bad = _adoption(make_account(feature_adoption_pct=70.0, users_active=5))
        assert "strong_adoption" in good
        assert "low_adoption" not in bad

    def test_strong_adoption_above_70(self):
        _, good, _ = _adoption(make_account(feature_adoption_pct=85.0, users_active=5))
        assert "strong_adoption" in good

    def test_no_strong_adoption_below_70(self):
        _, good, _ = _adoption(make_account(feature_adoption_pct=69.9, users_active=5))
        assert "strong_adoption" not in good

    def test_power_user_when_strong_adoption_and_5_plus_active(self):
        _, good, _ = _adoption(make_account(feature_adoption_pct=70.0, users_active=5))
        assert "power_user" in good

    def test_no_power_user_when_less_than_5_active(self):
        _, good, _ = _adoption(make_account(feature_adoption_pct=70.0, users_active=4))
        assert "power_user" not in good

    def test_no_power_user_when_adoption_below_70(self):
        _, good, _ = _adoption(make_account(feature_adoption_pct=69.0, users_active=10))
        assert "power_user" not in good

    def test_low_adoption_below_35(self):
        _, _, bad = _adoption(make_account(feature_adoption_pct=34.9))
        assert "low_adoption" in bad

    def test_no_low_adoption_at_35(self):
        _, _, bad = _adoption(make_account(feature_adoption_pct=35.0))
        assert "low_adoption" not in bad

    def test_upsell_opportunity_at_80_pct(self):
        _, good, _ = _adoption(make_account(usage_pct_of_limit=80.0))
        assert "upsell_opportunity" in good

    def test_upsell_opportunity_above_80(self):
        _, good, _ = _adoption(make_account(usage_pct_of_limit=95.0))
        assert "upsell_opportunity" in good

    def test_no_upsell_below_80(self):
        _, good, _ = _adoption(make_account(usage_pct_of_limit=79.9))
        assert "upsell_opportunity" not in good

    def test_composite_formula(self):
        a = make_account(feature_adoption_pct=70.0, users_active=10, users_licensed=15, integrations_active=2, usage_pct_of_limit=50.0)
        feature = min(100.0, 70.0)
        user = min(100.0, 10 / 15 * 100)
        integration = min(100.0, 2 * 25.0)
        expected = round(feature * 0.45 + user * 0.35 + integration * 0.20, 2)
        score, _, _ = _adoption(a)
        assert score == pytest.approx(expected, abs=0.01)

    def test_all_zeros(self):
        score, _, _ = _adoption(make_account(feature_adoption_pct=0, users_active=0, users_licensed=0, integrations_active=0, usage_pct_of_limit=0))
        assert score == pytest.approx(0.0, abs=0.01)

    def test_score_rounded_to_two_decimals(self):
        score, _, _ = _adoption(make_account(feature_adoption_pct=33.3, users_active=7, users_licensed=13, integrations_active=1))
        assert score == round(score, 2)


# ─── _financial tests ─────────────────────────────────────────────────────────

class TestFinancial:
    def test_returns_tuple_of_three(self):
        result = _financial(make_account())
        assert isinstance(result, tuple) and len(result) == 3

    def test_on_time_payments_signal_pct_95_no_overdue(self):
        _, good, bad = _financial(make_account(payments_on_time_pct=95.0, overdue_invoices=0))
        assert "on_time_payments" in good
        assert "payment_issues" not in bad

    def test_on_time_payments_signal_above_95(self):
        _, good, _ = _financial(make_account(payments_on_time_pct=100.0, overdue_invoices=0))
        assert "on_time_payments" in good

    def test_no_on_time_payments_below_95(self):
        _, good, _ = _financial(make_account(payments_on_time_pct=94.9, overdue_invoices=0))
        assert "on_time_payments" not in good

    def test_no_on_time_payments_when_overdue(self):
        _, good, _ = _financial(make_account(payments_on_time_pct=100.0, overdue_invoices=1))
        assert "on_time_payments" not in good

    def test_payment_issues_at_2_overdue(self):
        _, _, bad = _financial(make_account(overdue_invoices=2))
        assert "payment_issues" in bad

    def test_payment_issues_above_2(self):
        _, _, bad = _financial(make_account(overdue_invoices=5))
        assert "payment_issues" in bad

    def test_no_payment_issues_at_1(self):
        _, _, bad = _financial(make_account(overdue_invoices=1))
        assert "payment_issues" not in bad

    def test_overdue_penalty_capped_at_40(self):
        # 3 overdue * 15 = 45 → capped at 40
        # (30 - 40) * 0.40 = -4
        a = make_account(payments_on_time_pct=100.0, overdue_invoices=3, arr_eur=0, expansion_revenue_eur=0)
        score, _, _ = _financial(a)
        expected = min(100.0, max(0.0, 100.0 * 0.60 + 0 + (30.0 - 40.0) * 0.40))
        assert score == pytest.approx(expected, abs=0.01)

    def test_expansion_score_zero_when_arr_zero(self):
        a = make_account(arr_eur=0, expansion_revenue_eur=10_000, payments_on_time_pct=100, overdue_invoices=0)
        score, _, _ = _financial(a)
        # no expansion contribution; score = 100*0.60 + 0 + 30*0.40 = 72
        assert score == pytest.approx(72.0, abs=0.01)

    def test_expansion_score_calculation(self):
        # expansion = min(30, (10000/60000 * 100) * 0.60) = min(30, 16.67*0.60) = min(30, 10.0) = 10.0
        a = make_account(arr_eur=60_000, expansion_revenue_eur=10_000, payments_on_time_pct=100, overdue_invoices=0)
        score, _, _ = _financial(a)
        expansion = min(30.0, (10_000 / 60_000 * 100) * 0.60)
        expected = round(min(100.0, max(0.0, 100.0 * 0.60 + expansion + 30.0 * 0.40)), 2)
        assert score == pytest.approx(expected, abs=0.01)

    def test_expansion_score_capped_at_30(self):
        # very large expansion → capped at 30
        a = make_account(arr_eur=10_000, expansion_revenue_eur=1_000_000, payments_on_time_pct=100, overdue_invoices=0)
        score, _, _ = _financial(a)
        assert score == pytest.approx(min(100.0, 100.0 * 0.60 + 30.0 + 30.0 * 0.40), abs=0.01)

    def test_score_clamped_to_100(self):
        a = make_account(payments_on_time_pct=100.0, overdue_invoices=0, arr_eur=10_000, expansion_revenue_eur=1_000_000)
        score, _, _ = _financial(a)
        assert score <= 100.0

    def test_score_clamped_to_0(self):
        a = make_account(payments_on_time_pct=0.0, overdue_invoices=10, arr_eur=0, expansion_revenue_eur=0)
        score, _, _ = _financial(a)
        assert score >= 0.0

    def test_perfect_financial_score(self):
        a = make_account(payments_on_time_pct=100.0, overdue_invoices=0, arr_eur=0, expansion_revenue_eur=0)
        score, _, _ = _financial(a)
        # 100*0.60 + 0 + 30*0.40 = 72
        assert score == pytest.approx(72.0, abs=0.01)

    def test_score_rounded_to_two_decimals(self):
        score, _, _ = _financial(make_account(payments_on_time_pct=87.3, overdue_invoices=1))
        assert score == round(score, 2)


# ─── _relationship tests ──────────────────────────────────────────────────────

class TestRelationship:
    def test_returns_tuple_of_three(self):
        result = _relationship(make_account())
        assert isinstance(result, tuple) and len(result) == 3

    def test_nps_unknown_gives_neutral_50(self):
        a = make_account(nps_score=-999, support_tickets_open=0, support_tickets_30d=0, executive_contacts=0, last_qbr_days=45, csm_sentiment=50.0)
        # nps_score=50 (neutral), sentiment=50, no penalty, no exec bonus, qbr=100
        # (50+50)/2 * 0.45 + (100-0)*0.25 + 0*(100/20)*0.15 + 100*0.15
        # = 22.5 + 25.0 + 0.0 + 15.0 = 62.5
        score, _, _ = _relationship(a)
        assert score == pytest.approx(62.5, abs=0.1)

    def test_nps_positive_100(self):
        a = make_account(nps_score=100, support_tickets_open=0, support_tickets_30d=0, executive_contacts=0, last_qbr_days=45, csm_sentiment=100.0)
        # nps_score = (100+100)/2 = 100
        score, _, _ = _relationship(a)
        expected_nps = min(100.0, (100 + 100) / 2)
        assert score == pytest.approx(min(100.0, max(0.0, (expected_nps + 100.0) / 2 * 0.45 + 100 * 0.25 + 0 + 100 * 0.15)), abs=0.1)

    def test_nps_negative_100(self):
        a = make_account(nps_score=-100, support_tickets_open=0, support_tickets_30d=0, executive_contacts=0, last_qbr_days=45, csm_sentiment=0.0)
        # nps_score = (-100+100)/2 = 0
        score, _, _ = _relationship(a)
        assert score == pytest.approx(min(100.0, max(0.0, (0.0 + 0.0) / 2 * 0.45 + 100 * 0.25 + 0 + 100 * 0.15)), abs=0.1)

    def test_nps_score_clamped_at_100(self):
        # nps=100 → (100+100)/2 = 100, already 100
        a = make_account(nps_score=100)
        _, good, _ = _relationship(a)
        assert "nps_promoter" in good

    def test_nps_detractor_at_minus_20(self):
        _, _, bad = _relationship(make_account(nps_score=-20))
        assert "nps_detractor" in bad

    def test_nps_detractor_below_minus_20(self):
        _, _, bad = _relationship(make_account(nps_score=-50))
        assert "nps_detractor" in bad

    def test_no_nps_detractor_at_minus_19(self):
        _, _, bad = _relationship(make_account(nps_score=-19))
        assert "nps_detractor" not in bad

    def test_nps_promoter_at_50(self):
        _, good, _ = _relationship(make_account(nps_score=50))
        assert "nps_promoter" in good

    def test_nps_promoter_above_50(self):
        _, good, _ = _relationship(make_account(nps_score=80))
        assert "nps_promoter" in good

    def test_no_nps_promoter_at_49(self):
        _, good, _ = _relationship(make_account(nps_score=49))
        assert "nps_promoter" not in good

    def test_no_nps_signals_when_unknown(self):
        _, good, bad = _relationship(make_account(nps_score=-999))
        assert "nps_detractor" not in bad
        assert "nps_promoter" not in good

    def test_support_penalty_calculation(self):
        # 3 open * 10 + 5 * 30d * 2 = 30 + 10 = 40, capped at 30
        a = make_account(support_tickets_open=3, support_tickets_30d=5, executive_contacts=0, last_qbr_days=45, nps_score=-999, csm_sentiment=50.0)
        score, _, _ = _relationship(a)
        penalty = min(30.0, 3 * 10.0 + 5 * 2.0)  # 40 → 30
        expected = min(100.0, max(0.0, (50.0 + 50.0) / 2 * 0.45 + (100.0 - penalty) * 0.25 + 0 + 100 * 0.15))
        assert score == pytest.approx(expected, abs=0.01)

    def test_support_penalty_capped_at_30(self):
        a = make_account(support_tickets_open=10, support_tickets_30d=20, executive_contacts=0, last_qbr_days=45, nps_score=-999, csm_sentiment=50.0)
        score, _, _ = _relationship(a)
        penalty = 30.0  # capped
        expected = min(100.0, max(0.0, (50 + 50) / 2 * 0.45 + (100 - penalty) * 0.25 + 0 + 100 * 0.15))
        assert score == pytest.approx(expected, abs=0.01)

    def test_support_overload_at_3_open(self):
        _, _, bad = _relationship(make_account(support_tickets_open=3))
        assert "support_overload" in bad

    def test_support_overload_above_3(self):
        _, _, bad = _relationship(make_account(support_tickets_open=5))
        assert "support_overload" in bad

    def test_no_support_overload_at_2(self):
        _, _, bad = _relationship(make_account(support_tickets_open=2))
        assert "support_overload" not in bad

    def test_exec_bonus_at_2_contacts(self):
        # 2 * 7 = 14
        a = make_account(executive_contacts=2, nps_score=-999, support_tickets_open=0, support_tickets_30d=0, last_qbr_days=45, csm_sentiment=50.0)
        score, _, _ = _relationship(a)
        exec_bonus = min(20.0, 2 * 7.0)  # 14
        expected = min(100.0, max(0.0, (50 + 50) / 2 * 0.45 + 100 * 0.25 + exec_bonus * (100.0 / 20.0) * 0.15 + 100 * 0.15))
        assert score == pytest.approx(expected, abs=0.01)

    def test_exec_bonus_capped_at_20(self):
        a = make_account(executive_contacts=10, nps_score=-999, support_tickets_open=0, support_tickets_30d=0, last_qbr_days=45, csm_sentiment=50.0)
        score, _, _ = _relationship(a)
        exec_bonus = 20.0  # capped
        expected = min(100.0, max(0.0, (50 + 50) / 2 * 0.45 + 100 * 0.25 + 20 * (100.0 / 20.0) * 0.15 + 100 * 0.15))
        assert score == pytest.approx(expected, abs=0.01)

    def test_qbr_score_100_at_exactly_90_days(self):
        a = make_account(last_qbr_days=90, nps_score=-999, support_tickets_open=0, support_tickets_30d=0, executive_contacts=0, csm_sentiment=50.0)
        score, _, _ = _relationship(a)
        expected = min(100.0, max(0.0, (50 + 50) / 2 * 0.45 + 100 * 0.25 + 0 + 100.0 * 0.15))
        assert score == pytest.approx(expected, abs=0.01)

    def test_qbr_score_100_below_90_days(self):
        a = make_account(last_qbr_days=30, nps_score=-999, support_tickets_open=0, support_tickets_30d=0, executive_contacts=0, csm_sentiment=50.0)
        score, _, _ = _relationship(a)
        expected = min(100.0, max(0.0, (50 + 50) / 2 * 0.45 + 100 * 0.25 + 0 + 100.0 * 0.15))
        assert score == pytest.approx(expected, abs=0.01)

    def test_qbr_score_decreases_after_90_days(self):
        # 180 days → 100 - (180-90) = 10
        a = make_account(last_qbr_days=180, nps_score=-999, support_tickets_open=0, support_tickets_30d=0, executive_contacts=0, csm_sentiment=50.0)
        score, _, _ = _relationship(a)
        qbr = max(0.0, 100.0 - (180 - 90))
        expected = min(100.0, max(0.0, (50 + 50) / 2 * 0.45 + 100 * 0.25 + 0 + qbr * 0.15))
        assert score == pytest.approx(expected, abs=0.01)

    def test_qbr_score_zero_at_190_days(self):
        # 190 days → 100 - 100 = 0
        a = make_account(last_qbr_days=190, nps_score=-999, support_tickets_open=0, support_tickets_30d=0, executive_contacts=0, csm_sentiment=50.0)
        score, _, _ = _relationship(a)
        qbr = max(0.0, 100.0 - (190 - 90))  # 0
        expected = min(100.0, max(0.0, (50 + 50) / 2 * 0.45 + 100 * 0.25 + 0 + qbr * 0.15))
        assert score == pytest.approx(expected, abs=0.01)

    def test_strong_relationship_when_exec_bonus_ge_14_and_nps_ge_60(self):
        # exec_contacts=2 → bonus=14; nps=20 → nps_score=(20+100)/2=60
        _, good, _ = _relationship(make_account(executive_contacts=2, nps_score=20))
        assert "strong_relationship" in good

    def test_strong_relationship_not_when_exec_bonus_lt_14(self):
        _, good, _ = _relationship(make_account(executive_contacts=1, nps_score=20))
        assert "strong_relationship" not in good

    def test_strong_relationship_not_when_nps_lt_60(self):
        # nps=-999 → nps_score=50 < 60
        _, good, _ = _relationship(make_account(executive_contacts=2, nps_score=-999))
        assert "strong_relationship" not in good

    def test_weak_relationship_when_exec_0_and_nps_lt_50(self):
        # exec=0, nps=0 → nps_score=50 which is NOT < 50 so no weak_rel; use nps=-10
        # nps=-10 → (-10+100)/2=45 < 50
        _, _, bad = _relationship(make_account(executive_contacts=0, nps_score=-10))
        assert "weak_relationship" in bad

    def test_no_weak_relationship_when_exec_gt_0(self):
        _, _, bad = _relationship(make_account(executive_contacts=1, nps_score=-50))
        assert "weak_relationship" not in bad

    def test_no_weak_relationship_when_nps_score_ge_50(self):
        # nps=0 → nps_score=50, not < 50
        _, _, bad = _relationship(make_account(executive_contacts=0, nps_score=0))
        assert "weak_relationship" not in bad

    def test_score_clamped_to_100(self):
        a = make_account(nps_score=100, support_tickets_open=0, support_tickets_30d=0, executive_contacts=10, last_qbr_days=1, csm_sentiment=100.0)
        score, _, _ = _relationship(a)
        assert score <= 100.0

    def test_score_clamped_to_0(self):
        a = make_account(nps_score=-100, support_tickets_open=10, support_tickets_30d=50, executive_contacts=0, last_qbr_days=500, csm_sentiment=0.0)
        score, _, _ = _relationship(a)
        assert score >= 0.0

    def test_score_rounded_to_two_decimals(self):
        score, _, _ = _relationship(make_account(nps_score=33, csm_sentiment=66.7))
        assert score == round(score, 2)


# ─── _health_tier tests ───────────────────────────────────────────────────────

class TestHealthTier:
    def test_champion_at_80(self):
        assert _health_tier(80.0) == HealthTier.CHAMPION

    def test_champion_above_80(self):
        assert _health_tier(95.0) == HealthTier.CHAMPION

    def test_champion_at_100(self):
        assert _health_tier(100.0) == HealthTier.CHAMPION

    def test_healthy_at_65(self):
        assert _health_tier(65.0) == HealthTier.HEALTHY

    def test_healthy_at_79_9(self):
        assert _health_tier(79.9) == HealthTier.HEALTHY

    def test_neutral_at_45(self):
        assert _health_tier(45.0) == HealthTier.NEUTRAL

    def test_neutral_at_64_9(self):
        assert _health_tier(64.9) == HealthTier.NEUTRAL

    def test_at_risk_at_25(self):
        assert _health_tier(25.0) == HealthTier.AT_RISK

    def test_at_risk_at_44_9(self):
        assert _health_tier(44.9) == HealthTier.AT_RISK

    def test_churning_at_24_9(self):
        assert _health_tier(24.9) == HealthTier.CHURNING

    def test_churning_at_0(self):
        assert _health_tier(0.0) == HealthTier.CHURNING

    def test_returns_health_tier_enum(self):
        assert isinstance(_health_tier(50.0), HealthTier)


# ─── _churn_risk tests ────────────────────────────────────────────────────────

class TestChurnRisk:
    def test_base_risk_equals_100_minus_health(self):
        risk = _churn_risk(70.0, 180, 0, 40)
        assert risk == pytest.approx(30.0, abs=0.01)

    def test_renewal_bonus_when_days_le_30_and_health_lt_50(self):
        # +20 bonus
        risk = _churn_risk(40.0, 30, 0, 0)
        assert risk == pytest.approx(min(100.0, 60.0 + 20.0), abs=0.01)

    def test_renewal_bonus_not_applied_when_health_ge_50(self):
        risk = _churn_risk(60.0, 10, 0, 0)
        assert risk == pytest.approx(40.0, abs=0.01)

    def test_renewal_bonus_not_applied_when_days_gt_30(self):
        risk = _churn_risk(40.0, 31, 0, 0)
        assert risk == pytest.approx(60.0, abs=0.01)

    def test_overdue_bonus_at_2(self):
        risk = _churn_risk(70.0, 180, 2, 0)
        assert risk == pytest.approx(min(100.0, 30.0 + 15.0), abs=0.01)

    def test_overdue_bonus_not_applied_at_1(self):
        risk = _churn_risk(70.0, 180, 1, 0)
        assert risk == pytest.approx(30.0, abs=0.01)

    def test_nps_bonus_at_minus_30(self):
        risk = _churn_risk(70.0, 180, 0, -30)
        assert risk == pytest.approx(min(100.0, 30.0 + 10.0), abs=0.01)

    def test_nps_bonus_not_applied_at_minus_29(self):
        risk = _churn_risk(70.0, 180, 0, -29)
        assert risk == pytest.approx(30.0, abs=0.01)

    def test_nps_bonus_not_applied_when_unknown(self):
        risk = _churn_risk(70.0, 180, 0, -999)
        assert risk == pytest.approx(30.0, abs=0.01)

    def test_all_bonuses_stacked(self):
        # base=60+20+15+10=105 → clamped to 100
        risk = _churn_risk(40.0, 15, 2, -30)
        assert risk == pytest.approx(100.0, abs=0.01)

    def test_risk_clamped_at_100(self):
        risk = _churn_risk(0.0, 0, 10, -100)
        assert risk <= 100.0

    def test_risk_at_perfect_health(self):
        risk = _churn_risk(100.0, 180, 0, 100)
        assert risk == pytest.approx(0.0, abs=0.01)

    def test_returns_float(self):
        risk = _churn_risk(50.0, 60, 0, 0)
        assert isinstance(risk, float)

    def test_rounded_to_two_decimals(self):
        risk = _churn_risk(33.33, 180, 0, 0)
        assert risk == round(risk, 2)


# ─── _expansion_potential tests ───────────────────────────────────────────────

class TestExpansionPotential:
    def test_zero_when_health_below_50(self):
        a = make_account(arr_eur=100_000, usage_pct_of_limit=90)
        assert _expansion_potential(a, 49.9) == 0.0

    def test_zero_when_health_exactly_49(self):
        a = make_account(arr_eur=100_000, usage_pct_of_limit=50)
        assert _expansion_potential(a, 49.0) == 0.0

    def test_nonzero_at_health_50(self):
        a = make_account(arr_eur=100_000, usage_pct_of_limit=50)
        result = _expansion_potential(a, 50.0)
        assert result > 0.0

    def test_base_formula_no_usage_boost(self):
        a = make_account(arr_eur=60_000, usage_pct_of_limit=50)
        # base = 60000 * (70/100) * 0.30 = 12600
        result = _expansion_potential(a, 70.0)
        expected = round(60_000 * (70 / 100) * 0.30 * 1.0, 2)
        assert result == pytest.approx(expected, abs=0.01)

    def test_usage_boost_at_80_pct(self):
        a = make_account(arr_eur=60_000, usage_pct_of_limit=80)
        result = _expansion_potential(a, 70.0)
        expected = round(60_000 * (70 / 100) * 0.30 * 1.5, 2)
        assert result == pytest.approx(expected, abs=0.01)

    def test_usage_boost_above_80(self):
        a = make_account(arr_eur=60_000, usage_pct_of_limit=95)
        result = _expansion_potential(a, 70.0)
        expected = round(60_000 * (70 / 100) * 0.30 * 1.5, 2)
        assert result == pytest.approx(expected, abs=0.01)

    def test_no_usage_boost_below_80(self):
        a = make_account(arr_eur=60_000, usage_pct_of_limit=79.9)
        result = _expansion_potential(a, 70.0)
        expected = round(60_000 * (70 / 100) * 0.30 * 1.0, 2)
        assert result == pytest.approx(expected, abs=0.01)

    def test_zero_arr_gives_zero(self):
        a = make_account(arr_eur=0, usage_pct_of_limit=90)
        assert _expansion_potential(a, 80.0) == 0.0

    def test_returns_float(self):
        a = make_account()
        result = _expansion_potential(a, 70.0)
        assert isinstance(result, float)

    def test_rounded_to_two_decimals(self):
        a = make_account(arr_eur=33_333, usage_pct_of_limit=50)
        result = _expansion_potential(a, 66.7)
        assert result == round(result, 2)


# ─── _primary_action tests ────────────────────────────────────────────────────

class TestPrimaryAction:
    def test_churning_save_when_days_gt_0(self):
        assert _primary_action(HealthTier.CHURNING, 1, 0) == AccountAction.SAVE

    def test_churning_offboard_when_days_0(self):
        assert _primary_action(HealthTier.CHURNING, 0, 0) == AccountAction.OFFBOARD

    def test_churning_offboard_when_days_negative(self):
        assert _primary_action(HealthTier.CHURNING, -10, 0) == AccountAction.OFFBOARD

    def test_at_risk_always_save(self):
        assert _primary_action(HealthTier.AT_RISK, 0, 0) == AccountAction.SAVE
        assert _primary_action(HealthTier.AT_RISK, 100, 5000) == AccountAction.SAVE

    def test_neutral_always_stabilize(self):
        assert _primary_action(HealthTier.NEUTRAL, 0, 0) == AccountAction.STABILIZE
        assert _primary_action(HealthTier.NEUTRAL, 200, 50000) == AccountAction.STABILIZE

    def test_healthy_expand_when_expansion_gt_0(self):
        assert _primary_action(HealthTier.HEALTHY, 180, 5000) == AccountAction.EXPAND

    def test_healthy_nurture_when_expansion_0(self):
        assert _primary_action(HealthTier.HEALTHY, 180, 0) == AccountAction.NURTURE

    def test_champion_always_expand(self):
        assert _primary_action(HealthTier.CHAMPION, 0, 0) == AccountAction.EXPAND
        assert _primary_action(HealthTier.CHAMPION, 200, 0) == AccountAction.EXPAND

    def test_returns_account_action_enum(self):
        result = _primary_action(HealthTier.NEUTRAL, 30, 0)
        assert isinstance(result, AccountAction)


# ─── _renewal_forecast tests ──────────────────────────────────────────────────

class TestRenewalForecast:
    def test_confident_at_70(self):
        assert _renewal_forecast(70.0, 30) == "confident"

    def test_confident_above_70(self):
        assert _renewal_forecast(90.0, 0) == "confident"

    def test_uncertain_at_45_with_low_days(self):
        assert _renewal_forecast(45.0, 30) == "uncertain"

    def test_uncertain_when_days_gt_90_regardless_of_score(self):
        assert _renewal_forecast(30.0, 91) == "uncertain"

    def test_uncertain_days_exactly_91(self):
        assert _renewal_forecast(0.0, 91) == "uncertain"

    def test_at_risk_when_score_lt_45_and_days_le_90(self):
        assert _renewal_forecast(44.9, 90) == "at_risk"

    def test_at_risk_at_zero_score_zero_days(self):
        assert _renewal_forecast(0.0, 0) == "at_risk"

    def test_uncertain_score_45_days_0(self):
        # score >= 45 → uncertain
        assert _renewal_forecast(45.0, 0) == "uncertain"

    def test_returns_string(self):
        assert isinstance(_renewal_forecast(60.0, 60), str)


# ─── Composite health score tests ─────────────────────────────────────────────

class TestCompositeScore:
    def test_composite_formula_weights(self):
        a = make_account()
        eng, _, _ = _engagement(a)
        adp, _, _ = _adoption(a)
        fin, _, _ = _financial(a)
        rel, _, _ = _relationship(a)
        expected = round(eng * 0.30 + adp * 0.25 + fin * 0.25 + rel * 0.20, 2)
        monitor = AccountHealthMonitor()
        result = monitor.assess(a)
        assert result.health_score == pytest.approx(expected, abs=0.01)

    def test_all_zero_inputs_give_low_score(self):
        a = make_account(
            dau_wau_ratio=0.0, logins_last_30d=0, api_calls_last_30d=0,
            feature_adoption_pct=0.0, users_active=0, users_licensed=0, integrations_active=0,
            payments_on_time_pct=0.0, overdue_invoices=10, arr_eur=0, expansion_revenue_eur=0,
            nps_score=-100, support_tickets_open=10, support_tickets_30d=50,
            executive_contacts=0, last_qbr_days=500, csm_sentiment=0.0,
            usage_pct_of_limit=0.0,
        )
        monitor = AccountHealthMonitor()
        result = monitor.assess(a)
        assert result.health_score < 25.0

    def test_perfect_inputs_give_champion(self):
        a = make_account(
            dau_wau_ratio=1.0, logins_last_30d=40, api_calls_last_30d=100_000,
            feature_adoption_pct=100.0, users_active=20, users_licensed=10, integrations_active=10,
            payments_on_time_pct=100.0, overdue_invoices=0, arr_eur=100_000, expansion_revenue_eur=50_000,
            nps_score=100, support_tickets_open=0, support_tickets_30d=0,
            executive_contacts=10, last_qbr_days=30, csm_sentiment=100.0,
            usage_pct_of_limit=90.0,
        )
        monitor = AccountHealthMonitor()
        result = monitor.assess(a)
        assert result.health_tier == HealthTier.CHAMPION


# ─── AccountHealthMonitor: assess & store ─────────────────────────────────────

class TestAccountHealthMonitorAssess:
    def test_assess_returns_account_health(self):
        monitor = AccountHealthMonitor()
        a = make_account()
        result = monitor.assess(a)
        assert isinstance(result, AccountHealth)

    def test_assess_stores_result(self):
        monitor = AccountHealthMonitor()
        a = make_account(account_id="x1")
        monitor.assess(a)
        assert monitor.get("x1") is not None

    def test_get_returns_none_for_unknown(self):
        monitor = AccountHealthMonitor()
        assert monitor.get("nonexistent") is None

    def test_assess_batch_processes_all(self):
        monitor = AccountHealthMonitor()
        accounts = [make_account(account_id=f"a{i}") for i in range(5)]
        results = monitor.assess_batch(accounts)
        assert len(results) == 5

    def test_assess_batch_returns_list_of_account_health(self):
        monitor = AccountHealthMonitor()
        results = monitor.assess_batch([make_account(account_id="b1"), make_account(account_id="b2")])
        assert all(isinstance(r, AccountHealth) for r in results)

    def test_assess_overwrites_previous(self):
        monitor = AccountHealthMonitor()
        a1 = make_account(account_id="dup", nps_score=80)
        a2 = make_account(account_id="dup", nps_score=-80)
        monitor.assess(a1)
        monitor.assess(a2)
        stored = monitor.get("dup")
        assert stored.account.nps_score == -80

    def test_account_health_has_correct_fields(self):
        monitor = AccountHealthMonitor()
        result = monitor.assess(make_account())
        assert hasattr(result, "health_tier")
        assert hasattr(result, "health_score")
        assert hasattr(result, "engagement_score")
        assert hasattr(result, "adoption_score")
        assert hasattr(result, "financial_score")
        assert hasattr(result, "relationship_score")
        assert hasattr(result, "churn_risk_pct")
        assert hasattr(result, "expansion_potential_eur")
        assert hasattr(result, "primary_action")
        assert hasattr(result, "health_signals")
        assert hasattr(result, "risk_signals")
        assert hasattr(result, "renewal_forecast")

    def test_health_signals_are_strings(self):
        monitor = AccountHealthMonitor()
        result = monitor.assess(make_account())
        assert all(isinstance(s, str) for s in result.health_signals)

    def test_risk_signals_are_strings(self):
        monitor = AccountHealthMonitor()
        result = monitor.assess(make_account())
        assert all(isinstance(s, str) for s in result.risk_signals)

    def test_health_signals_no_duplicates(self):
        monitor = AccountHealthMonitor()
        # Arrange to trigger multiple signals
        a = make_account(dau_wau_ratio=0.5, feature_adoption_pct=80, users_active=10, usage_pct_of_limit=85,
                         payments_on_time_pct=100, overdue_invoices=0, nps_score=60,
                         executive_contacts=2, last_qbr_days=45)
        result = monitor.assess(a)
        assert len(result.health_signals) == len(set(result.health_signals))

    def test_risk_signals_no_duplicates(self):
        monitor = AccountHealthMonitor()
        a = make_account(dau_wau_ratio=0.05, feature_adoption_pct=20, overdue_invoices=3,
                         nps_score=-50, support_tickets_open=5)
        result = monitor.assess(a)
        assert len(result.risk_signals) == len(set(result.risk_signals))


# ─── AccountHealthMonitor: queries ───────────────────────────────────────────

class TestAccountHealthMonitorQueries:
    def _setup(self) -> AccountHealthMonitor:
        monitor = AccountHealthMonitor()
        # Champion
        monitor.assess(make_account(account_id="champ", dau_wau_ratio=1.0, logins_last_30d=40,
                                     api_calls_last_30d=100_000, feature_adoption_pct=100, users_active=20,
                                     users_licensed=10, integrations_active=10, payments_on_time_pct=100,
                                     overdue_invoices=0, arr_eur=120_000, nps_score=90,
                                     support_tickets_open=0, support_tickets_30d=0, executive_contacts=3,
                                     last_qbr_days=30, csm_sentiment=100, usage_pct_of_limit=85))
        # Churning
        monitor.assess(make_account(account_id="churn", dau_wau_ratio=0.0, logins_last_30d=0,
                                     api_calls_last_30d=0, feature_adoption_pct=0, users_active=0,
                                     users_licensed=10, integrations_active=0, payments_on_time_pct=0,
                                     overdue_invoices=5, arr_eur=30_000, nps_score=-80,
                                     support_tickets_open=8, support_tickets_30d=20, executive_contacts=0,
                                     last_qbr_days=400, csm_sentiment=0, usage_pct_of_limit=10,
                                     days_until_renewal=60))
        # Healthy
        monitor.assess(make_account(account_id="healthy", dau_wau_ratio=0.5, logins_last_30d=25,
                                     api_calls_last_30d=5_000, feature_adoption_pct=80, users_active=12,
                                     users_licensed=15, integrations_active=3, payments_on_time_pct=97,
                                     overdue_invoices=0, arr_eur=80_000, nps_score=60,
                                     support_tickets_open=1, support_tickets_30d=3, executive_contacts=2,
                                     last_qbr_days=60, csm_sentiment=80, usage_pct_of_limit=60))
        return monitor

    def test_all_accounts_returns_all(self):
        monitor = self._setup()
        assert len(monitor.all_accounts()) == 3

    def test_all_accounts_sorted_desc_by_score(self):
        monitor = self._setup()
        scores = [h.health_score for h in monitor.all_accounts()]
        assert scores == sorted(scores, reverse=True)

    def test_by_tier_champion(self):
        monitor = self._setup()
        champions = monitor.by_tier(HealthTier.CHAMPION)
        assert all(h.health_tier == HealthTier.CHAMPION for h in champions)

    def test_churning_accounts(self):
        monitor = self._setup()
        churning = monitor.churning_accounts()
        assert all(h.health_tier == HealthTier.CHURNING for h in churning)

    def test_champion_accounts(self):
        monitor = self._setup()
        champs = monitor.champion_accounts()
        assert all(h.health_tier == HealthTier.CHAMPION for h in champs)

    def test_at_risk_accounts_includes_churning(self):
        monitor = self._setup()
        at_risk = monitor.at_risk_accounts()
        tiers = {h.health_tier for h in at_risk}
        assert tiers.issubset({HealthTier.AT_RISK, HealthTier.CHURNING})

    def test_expansion_opportunities_min_threshold(self):
        monitor = self._setup()
        opps = monitor.expansion_opportunities(min_potential=5_000)
        assert all(h.expansion_potential_eur >= 5_000 for h in opps)

    def test_expansion_opportunities_sorted_desc(self):
        monitor = self._setup()
        opps = monitor.expansion_opportunities(min_potential=0)
        potentials = [h.expansion_potential_eur for h in opps]
        assert potentials == sorted(potentials, reverse=True)

    def test_expansion_opportunities_default_threshold(self):
        monitor = self._setup()
        opps = monitor.expansion_opportunities()
        assert all(h.expansion_potential_eur >= 5_000 for h in opps)

    def test_renewal_at_risk_filters_by_days(self):
        monitor = self._setup()
        risky = monitor.renewal_at_risk(days_threshold=90)
        assert all(h.account.days_until_renewal <= 90 for h in risky)

    def test_renewal_at_risk_forecast_filter(self):
        monitor = self._setup()
        risky = monitor.renewal_at_risk(days_threshold=90)
        assert all(h.renewal_forecast in ("uncertain", "at_risk") for h in risky)

    def test_total_arr(self):
        monitor = self._setup()
        expected = 120_000 + 30_000 + 80_000
        assert monitor.total_arr() == pytest.approx(expected, abs=0.01)

    def test_arr_at_risk_only_at_risk_churning(self):
        monitor = self._setup()
        arr = monitor.arr_at_risk()
        at_risk_items = monitor.at_risk_accounts()
        expected = sum(h.account.arr_eur for h in at_risk_items)
        assert arr == pytest.approx(expected, abs=0.01)

    def test_reset_clears_store(self):
        monitor = self._setup()
        monitor.reset()
        assert monitor.all_accounts() == []
        assert monitor.total_arr() == 0.0

    def test_get_after_reset_returns_none(self):
        monitor = self._setup()
        monitor.reset()
        assert monitor.get("champ") is None


# ─── Summary tests ────────────────────────────────────────────────────────────

class TestSummary:
    def test_empty_summary_structure(self):
        monitor = AccountHealthMonitor()
        s = monitor.summary()
        assert s["total"] == 0
        assert s["avg_health_score"] == 0.0
        assert s["avg_churn_risk_pct"] == 0.0
        assert s["total_arr_eur"] == 0.0
        assert s["arr_at_risk_eur"] == 0.0
        assert s["total_expansion_potential_eur"] == 0.0

    def test_empty_summary_tier_counts_all_zero(self):
        monitor = AccountHealthMonitor()
        s = monitor.summary()
        for tier in HealthTier:
            assert s["tier_counts"][tier.value] == 0

    def test_empty_summary_action_counts_all_zero(self):
        monitor = AccountHealthMonitor()
        s = monitor.summary()
        for action in AccountAction:
            assert s["action_counts"][action.value] == 0

    def test_non_empty_summary_total(self):
        monitor = AccountHealthMonitor()
        monitor.assess(make_account(account_id="a1"))
        monitor.assess(make_account(account_id="a2"))
        s = monitor.summary()
        assert s["total"] == 2

    def test_non_empty_summary_has_all_tier_keys(self):
        monitor = AccountHealthMonitor()
        monitor.assess(make_account())
        s = monitor.summary()
        for tier in HealthTier:
            assert tier.value in s["tier_counts"]

    def test_non_empty_summary_has_all_action_keys(self):
        monitor = AccountHealthMonitor()
        monitor.assess(make_account())
        s = monitor.summary()
        for action in AccountAction:
            assert action.value in s["action_counts"]

    def test_summary_tier_counts_sum_to_total(self):
        monitor = AccountHealthMonitor()
        for i in range(5):
            monitor.assess(make_account(account_id=f"s{i}"))
        s = monitor.summary()
        assert sum(s["tier_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_to_total(self):
        monitor = AccountHealthMonitor()
        for i in range(5):
            monitor.assess(make_account(account_id=f"t{i}"))
        s = monitor.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_avg_health_score(self):
        monitor = AccountHealthMonitor()
        monitor.assess(make_account(account_id="u1"))
        monitor.assess(make_account(account_id="u2"))
        scores = [monitor.get("u1").health_score, monitor.get("u2").health_score]
        s = monitor.summary()
        assert s["avg_health_score"] == pytest.approx(sum(scores) / 2, abs=0.01)

    def test_summary_total_arr(self):
        monitor = AccountHealthMonitor()
        monitor.assess(make_account(account_id="v1", arr_eur=10_000))
        monitor.assess(make_account(account_id="v2", arr_eur=20_000))
        s = monitor.summary()
        assert s["total_arr_eur"] == pytest.approx(30_000, abs=0.01)

    def test_summary_total_expansion_potential(self):
        monitor = AccountHealthMonitor()
        monitor.assess(make_account(account_id="w1"))
        s = monitor.summary()
        exp = monitor.get("w1").expansion_potential_eur
        assert s["total_expansion_potential_eur"] == pytest.approx(exp, abs=0.01)

    def test_summary_avg_churn_risk(self):
        monitor = AccountHealthMonitor()
        monitor.assess(make_account(account_id="z1"))
        monitor.assess(make_account(account_id="z2"))
        risks = [monitor.get("z1").churn_risk_pct, monitor.get("z2").churn_risk_pct]
        s = monitor.summary()
        assert s["avg_churn_risk_pct"] == pytest.approx(sum(risks) / 2, abs=0.01)


# ─── to_dict tests ────────────────────────────────────────────────────────────

class TestToDicts:
    def test_account_metrics_to_dict(self):
        a = make_account()
        d = a.to_dict()
        assert isinstance(d, dict)
        assert d["account_id"] == a.account_id
        assert d["arr_eur"] == a.arr_eur

    def test_account_health_to_dict_keys(self):
        monitor = AccountHealthMonitor()
        result = monitor.assess(make_account())
        d = result.to_dict()
        expected_keys = {
            "account", "health_tier", "health_score", "engagement_score",
            "adoption_score", "financial_score", "relationship_score",
            "churn_risk_pct", "expansion_potential_eur", "primary_action",
            "health_signals", "risk_signals", "renewal_forecast",
        }
        assert expected_keys.issubset(d.keys())

    def test_account_health_to_dict_enum_values(self):
        monitor = AccountHealthMonitor()
        result = monitor.assess(make_account())
        d = result.to_dict()
        assert isinstance(d["health_tier"], str)
        assert isinstance(d["primary_action"], str)


# ─── Enum / ContractType tests ────────────────────────────────────────────────

class TestEnums:
    def test_health_tier_values(self):
        assert HealthTier.CHAMPION.value == "champion"
        assert HealthTier.HEALTHY.value == "healthy"
        assert HealthTier.NEUTRAL.value == "neutral"
        assert HealthTier.AT_RISK.value == "at_risk"
        assert HealthTier.CHURNING.value == "churning"

    def test_account_action_values(self):
        assert AccountAction.EXPAND.value == "expand"
        assert AccountAction.NURTURE.value == "nurture"
        assert AccountAction.STABILIZE.value == "stabilize"
        assert AccountAction.SAVE.value == "save"
        assert AccountAction.OFFBOARD.value == "offboard"

    def test_contract_type_values(self):
        assert ContractType.MONTHLY.value == "monthly"
        assert ContractType.ANNUAL.value == "annual"
        assert ContractType.MULTI_YEAR.value == "multi_year"


# ─── Edge-case / integration tests ───────────────────────────────────────────

class TestEdgeCases:
    def test_days_until_renewal_negative_churning_offboard(self):
        monitor = AccountHealthMonitor()
        a = make_account(dau_wau_ratio=0.0, logins_last_30d=0, api_calls_last_30d=0,
                         feature_adoption_pct=0, users_active=0, users_licensed=10,
                         integrations_active=0, payments_on_time_pct=0, overdue_invoices=5,
                         arr_eur=0, nps_score=-100, support_tickets_open=10, support_tickets_30d=20,
                         executive_contacts=0, last_qbr_days=500, csm_sentiment=0,
                         usage_pct_of_limit=0, days_until_renewal=-5)
        result = monitor.assess(a)
        if result.health_tier == HealthTier.CHURNING:
            assert result.primary_action == AccountAction.OFFBOARD

    def test_days_until_renewal_zero_churning_offboard(self):
        monitor = AccountHealthMonitor()
        a = make_account(dau_wau_ratio=0.0, logins_last_30d=0, api_calls_last_30d=0,
                         feature_adoption_pct=0, users_active=0, users_licensed=10,
                         integrations_active=0, payments_on_time_pct=0, overdue_invoices=5,
                         arr_eur=0, nps_score=-100, support_tickets_open=10, support_tickets_30d=20,
                         executive_contacts=0, last_qbr_days=500, csm_sentiment=0,
                         usage_pct_of_limit=0, days_until_renewal=0)
        result = monitor.assess(a)
        if result.health_tier == HealthTier.CHURNING:
            assert result.primary_action == AccountAction.OFFBOARD

    def test_monitor_empty_returns_empty_lists(self):
        monitor = AccountHealthMonitor()
        assert monitor.all_accounts() == []
        assert monitor.churning_accounts() == []
        assert monitor.champion_accounts() == []
        assert monitor.at_risk_accounts() == []
        assert monitor.expansion_opportunities() == []
        assert monitor.renewal_at_risk() == []

    def test_monitor_total_arr_empty(self):
        monitor = AccountHealthMonitor()
        assert monitor.total_arr() == 0.0

    def test_monitor_arr_at_risk_empty(self):
        monitor = AccountHealthMonitor()
        assert monitor.arr_at_risk() == 0.0

    def test_assess_batch_empty_list(self):
        monitor = AccountHealthMonitor()
        results = monitor.assess_batch([])
        assert results == []

    def test_multi_year_contract(self):
        monitor = AccountHealthMonitor()
        a = make_account(contract_type=ContractType.MULTI_YEAR)
        result = monitor.assess(a)
        assert result.account.contract_type == ContractType.MULTI_YEAR

    def test_monthly_contract(self):
        monitor = AccountHealthMonitor()
        a = make_account(contract_type=ContractType.MONTHLY)
        result = monitor.assess(a)
        assert result.account.contract_type == ContractType.MONTHLY

    def test_nps_score_minus_999_no_nps_bonus_in_churn_risk(self):
        risk = _churn_risk(70.0, 180, 0, -999)
        # should NOT add +10 for nps
        assert risk == pytest.approx(30.0, abs=0.01)

    def test_very_high_api_calls_capped(self):
        score, _, _ = _engagement(make_account(dau_wau_ratio=0.0, logins_last_30d=0, api_calls_last_30d=10**10))
        # only api contribution, capped at 25
        assert score == pytest.approx(25.0, abs=0.1)

    def test_single_executive_contact_bonus(self):
        # 1 * 7 = 7
        a = make_account(executive_contacts=1, nps_score=-999, support_tickets_open=0, support_tickets_30d=0,
                         last_qbr_days=45, csm_sentiment=50.0)
        score, _, _ = _relationship(a)
        exec_bonus = 7.0
        expected = min(100.0, max(0.0, (50 + 50) / 2 * 0.45 + 100 * 0.25 + exec_bonus * (100.0 / 20.0) * 0.15 + 100 * 0.15))
        assert score == pytest.approx(expected, abs=0.01)

    def test_expansion_opportunity_filter_by_min(self):
        monitor = AccountHealthMonitor()
        monitor.assess(make_account(account_id="e1", arr_eur=100_000, usage_pct_of_limit=90,
                                     dau_wau_ratio=0.7, logins_last_30d=30, api_calls_last_30d=10_000,
                                     feature_adoption_pct=90, users_active=15, users_licensed=15,
                                     integrations_active=4, payments_on_time_pct=100, overdue_invoices=0,
                                     nps_score=80, support_tickets_open=0, support_tickets_30d=0,
                                     executive_contacts=3, last_qbr_days=30, csm_sentiment=90))
        monitor.assess(make_account(account_id="e2", arr_eur=1_000))  # tiny arr, low expansion
        big = monitor.expansion_opportunities(min_potential=10_000)
        small = monitor.expansion_opportunities(min_potential=0)
        assert len(small) >= len(big)

    def test_by_tier_returns_empty_when_no_match(self):
        monitor = AccountHealthMonitor()
        monitor.assess(make_account())
        # Whatever tier it is, a non-matching tier should be empty
        present_tier = monitor.all_accounts()[0].health_tier
        for tier in HealthTier:
            if tier != present_tier:
                assert monitor.by_tier(tier) == []
                break

    def test_reset_then_assess_works(self):
        monitor = AccountHealthMonitor()
        monitor.assess(make_account(account_id="r1"))
        monitor.reset()
        monitor.assess(make_account(account_id="r2"))
        assert monitor.get("r1") is None
        assert monitor.get("r2") is not None

    def test_feature_adoption_exactly_35_no_low_adoption(self):
        _, _, bad = _adoption(make_account(feature_adoption_pct=35.0))
        assert "low_adoption" not in bad

    def test_feature_adoption_exactly_70_strong_adoption(self):
        _, good, _ = _adoption(make_account(feature_adoption_pct=70.0, users_active=5))
        assert "strong_adoption" in good

    def test_dau_wau_exactly_035_high_engagement(self):
        _, good, _ = _engagement(make_account(dau_wau_ratio=0.35))
        assert "high_engagement" in good

    def test_dau_wau_below_010_low_engagement(self):
        _, _, bad = _engagement(make_account(dau_wau_ratio=0.0))
        assert "low_engagement" in bad

    def test_overdue_2_penalty_30(self):
        # 2 * 15 = 30
        a = make_account(payments_on_time_pct=100.0, overdue_invoices=2, arr_eur=0, expansion_revenue_eur=0)
        score, _, _ = _financial(a)
        # score = 100*0.60 + 0 + (30-30)*0.40 = 60
        assert score == pytest.approx(60.0, abs=0.01)

    def test_overdue_1_penalty_15(self):
        a = make_account(payments_on_time_pct=100.0, overdue_invoices=1, arr_eur=0, expansion_revenue_eur=0)
        score, _, _ = _financial(a)
        # score = 100*0.60 + 0 + (30-15)*0.40 = 60 + 6 = 66
        assert score == pytest.approx(66.0, abs=0.01)

    def test_health_score_range_0_to_100(self):
        monitor = AccountHealthMonitor()
        accounts = [
            make_account(account_id="range1", dau_wau_ratio=0.0),
            make_account(account_id="range2", dau_wau_ratio=1.0),
        ]
        for a in accounts:
            result = monitor.assess(a)
            assert 0.0 <= result.health_score <= 100.0

    def test_churn_risk_range_0_to_100(self):
        monitor = AccountHealthMonitor()
        result = monitor.assess(make_account())
        assert 0.0 <= result.churn_risk_pct <= 100.0

    def test_account_id_persisted(self):
        monitor = AccountHealthMonitor()
        a = make_account(account_id="persist-me")
        monitor.assess(a)
        assert monitor.get("persist-me").account.account_id == "persist-me"

    def test_expansion_potential_zero_below_50_health(self):
        # Use a very bad account that should have health < 50
        monitor = AccountHealthMonitor()
        a = make_account(
            dau_wau_ratio=0.0, logins_last_30d=0, api_calls_last_30d=0,
            feature_adoption_pct=0, users_active=0, users_licensed=10,
            integrations_active=0, payments_on_time_pct=0, overdue_invoices=5,
            arr_eur=100_000, nps_score=-100, support_tickets_open=10, support_tickets_30d=20,
            executive_contacts=0, last_qbr_days=500, csm_sentiment=0, usage_pct_of_limit=10
        )
        result = monitor.assess(a)
        if result.health_score < 50:
            assert result.expansion_potential_eur == 0.0

    def test_nps_exactly_minus_20_is_detractor(self):
        _, _, bad = _relationship(make_account(nps_score=-20))
        assert "nps_detractor" in bad

    def test_nps_exactly_50_is_promoter(self):
        _, good, _ = _relationship(make_account(nps_score=50))
        assert "nps_promoter" in good
