"""
Comprehensive pytest test suite for Module 27 — Account Health Scorer.

Coverage targets:
- All 4 enums
- AccountHealthInput / AccountHealthResult dataclasses
- All private scoring functions
- All churn-risk, expansion-potential, health-action, renewal-probability helpers
- AccountHealthScorerEngine methods (22 test classes, 270+ tests)
"""
from __future__ import annotations

import pytest

from swarm.intelligence.account_health_scorer import (
    AccountHealthInput,
    AccountHealthResult,
    AccountHealthScorerEngine,
    ChurnRisk,
    ExpansionPotential,
    HealthAction,
    HealthTier,
    _churn_risk,
    _commercial_score,
    _expansion_potential,
    _health_action,
    _health_drivers,
    _health_score,
    _health_tier,
    _recommended_plays,
    _renewal_probability,
    _risk_signals,
    _satisfaction_score,
    _relationship_score,
    _usage_score,
)


# ---------------------------------------------------------------------------
# Factory helper
# ---------------------------------------------------------------------------

def make_account(
    account_id: str = "acc-001",
    account_name: str = "Acme Corp",
    arr_eur: float = 100_000.0,
    segment: str = "enterprise",
    dau_mau_ratio: float = 0.4,
    feature_adoption_pct: float = 70.0,
    integrations_active: int = 4,
    nps_score: int = 40,
    support_tickets_last_90d: int = 1,
    critical_tickets_open: int = 0,
    contract_months_remaining: int = 12,
    expansion_discussions: bool = True,
    last_qbr_days_ago: int = 20,
    executive_sponsor_engaged: bool = True,
    champion_score: int = 8,
    stakeholders_active: int = 3,
    payment_on_time: bool = True,
    invoices_overdue: int = 0,
) -> AccountHealthInput:
    """Return a healthy, champion-tier account with sensible defaults."""
    return AccountHealthInput(
        account_id=account_id,
        account_name=account_name,
        arr_eur=arr_eur,
        segment=segment,
        dau_mau_ratio=dau_mau_ratio,
        feature_adoption_pct=feature_adoption_pct,
        integrations_active=integrations_active,
        nps_score=nps_score,
        support_tickets_last_90d=support_tickets_last_90d,
        critical_tickets_open=critical_tickets_open,
        contract_months_remaining=contract_months_remaining,
        expansion_discussions=expansion_discussions,
        last_qbr_days_ago=last_qbr_days_ago,
        executive_sponsor_engaged=executive_sponsor_engaged,
        champion_score=champion_score,
        stakeholders_active=stakeholders_active,
        payment_on_time=payment_on_time,
        invoices_overdue=invoices_overdue,
    )


# ===========================================================================
# 1. Enum Tests
# ===========================================================================

class TestHealthTierEnum:
    def test_champion_value(self):
        assert HealthTier.CHAMPION.value == "champion"

    def test_healthy_value(self):
        assert HealthTier.HEALTHY.value == "healthy"

    def test_at_risk_value(self):
        assert HealthTier.AT_RISK.value == "at_risk"

    def test_critical_value(self):
        assert HealthTier.CRITICAL.value == "critical"

    def test_all_members(self):
        assert set(HealthTier) == {
            HealthTier.CHAMPION,
            HealthTier.HEALTHY,
            HealthTier.AT_RISK,
            HealthTier.CRITICAL,
        }

    def test_is_str_subclass(self):
        assert isinstance(HealthTier.CHAMPION, str)


class TestHealthActionEnum:
    def test_celebrate_value(self):
        assert HealthAction.CELEBRATE.value == "celebrate"

    def test_maintain_value(self):
        assert HealthAction.MAINTAIN.value == "maintain"

    def test_intervene_value(self):
        assert HealthAction.INTERVENE.value == "intervene"

    def test_escalate_value(self):
        assert HealthAction.ESCALATE.value == "escalate"

    def test_all_members(self):
        assert set(HealthAction) == {
            HealthAction.CELEBRATE,
            HealthAction.MAINTAIN,
            HealthAction.INTERVENE,
            HealthAction.ESCALATE,
        }

    def test_is_str_subclass(self):
        assert isinstance(HealthAction.ESCALATE, str)


class TestChurnRiskEnum:
    def test_low_value(self):
        assert ChurnRisk.LOW.value == "low"

    def test_medium_value(self):
        assert ChurnRisk.MEDIUM.value == "medium"

    def test_high_value(self):
        assert ChurnRisk.HIGH.value == "high"

    def test_imminent_value(self):
        assert ChurnRisk.IMMINENT.value == "imminent"

    def test_all_members(self):
        assert set(ChurnRisk) == {
            ChurnRisk.LOW,
            ChurnRisk.MEDIUM,
            ChurnRisk.HIGH,
            ChurnRisk.IMMINENT,
        }

    def test_is_str_subclass(self):
        assert isinstance(ChurnRisk.HIGH, str)


class TestExpansionPotentialEnum:
    def test_strong_value(self):
        assert ExpansionPotential.STRONG.value == "strong"

    def test_moderate_value(self):
        assert ExpansionPotential.MODERATE.value == "moderate"

    def test_limited_value(self):
        assert ExpansionPotential.LIMITED.value == "limited"

    def test_none_value(self):
        assert ExpansionPotential.NONE.value == "none"

    def test_all_members(self):
        assert set(ExpansionPotential) == {
            ExpansionPotential.STRONG,
            ExpansionPotential.MODERATE,
            ExpansionPotential.LIMITED,
            ExpansionPotential.NONE,
        }

    def test_is_str_subclass(self):
        assert isinstance(ExpansionPotential.NONE, str)


# ===========================================================================
# 2. AccountHealthInput dataclass
# ===========================================================================

class TestAccountHealthInput:
    def test_can_construct(self):
        inp = make_account()
        assert inp.account_id == "acc-001"

    def test_fields_stored_correctly(self):
        inp = make_account(arr_eur=999.0, segment="smb", dau_mau_ratio=0.1)
        assert inp.arr_eur == 999.0
        assert inp.segment == "smb"
        assert inp.dau_mau_ratio == 0.1

    def test_bool_fields(self):
        inp = make_account(expansion_discussions=False, executive_sponsor_engaged=False, payment_on_time=False)
        assert inp.expansion_discussions is False
        assert inp.executive_sponsor_engaged is False
        assert inp.payment_on_time is False

    def test_int_fields(self):
        inp = make_account(nps_score=-50, support_tickets_last_90d=8, critical_tickets_open=2)
        assert inp.nps_score == -50
        assert inp.support_tickets_last_90d == 8
        assert inp.critical_tickets_open == 2

    def test_nps_extreme_negative(self):
        inp = make_account(nps_score=-100)
        assert inp.nps_score == -100

    def test_nps_extreme_positive(self):
        inp = make_account(nps_score=100)
        assert inp.nps_score == 100


# ===========================================================================
# 3. _usage_score
# ===========================================================================

class TestUsageScore:
    def test_returns_numeric(self):
        inp = make_account()
        assert isinstance(_usage_score(inp), (int, float))

    def test_max_35(self):
        inp = make_account(dau_mau_ratio=1.0, feature_adoption_pct=100.0, integrations_active=100)
        assert _usage_score(inp) <= 35.0

    def test_min_0(self):
        inp = make_account(dau_mau_ratio=0.0, feature_adoption_pct=0.0, integrations_active=0)
        assert _usage_score(inp) >= 0.0

    def test_dau_mau_zero(self):
        inp = make_account(dau_mau_ratio=0.0, feature_adoption_pct=0.0, integrations_active=0)
        assert _usage_score(inp) == 0.0

    def test_dau_mau_at_threshold_gives_15(self):
        inp = make_account(dau_mau_ratio=0.4, feature_adoption_pct=0.0, integrations_active=0)
        assert _usage_score(inp) == pytest.approx(15.0, abs=0.01)

    def test_dau_mau_above_threshold_capped(self):
        inp = make_account(dau_mau_ratio=1.0, feature_adoption_pct=0.0, integrations_active=0)
        assert _usage_score(inp) == pytest.approx(15.0, abs=0.01)

    def test_dau_mau_half(self):
        inp = make_account(dau_mau_ratio=0.2, feature_adoption_pct=0.0, integrations_active=0)
        assert _usage_score(inp) == pytest.approx(7.5, abs=0.01)

    def test_feature_adoption_60_gives_12(self):
        inp = make_account(dau_mau_ratio=0.0, feature_adoption_pct=60.0, integrations_active=0)
        assert _usage_score(inp) == pytest.approx(12.0, abs=0.01)

    def test_feature_adoption_above_60_capped(self):
        inp = make_account(dau_mau_ratio=0.0, feature_adoption_pct=100.0, integrations_active=0)
        assert _usage_score(inp) == pytest.approx(12.0, abs=0.01)

    def test_feature_adoption_30_gives_6(self):
        inp = make_account(dau_mau_ratio=0.0, feature_adoption_pct=30.0, integrations_active=0)
        assert _usage_score(inp) == pytest.approx(6.0, abs=0.01)

    def test_integrations_2_gives_4(self):
        inp = make_account(dau_mau_ratio=0.0, feature_adoption_pct=0.0, integrations_active=2)
        assert _usage_score(inp) == pytest.approx(4.0, abs=0.01)

    def test_integrations_4_gives_8(self):
        inp = make_account(dau_mau_ratio=0.0, feature_adoption_pct=0.0, integrations_active=4)
        assert _usage_score(inp) == pytest.approx(8.0, abs=0.01)

    def test_integrations_above_4_capped(self):
        inp = make_account(dau_mau_ratio=0.0, feature_adoption_pct=0.0, integrations_active=10)
        assert _usage_score(inp) == pytest.approx(8.0, abs=0.01)

    def test_all_max_gives_35(self):
        inp = make_account(dau_mau_ratio=1.0, feature_adoption_pct=100.0, integrations_active=10)
        assert _usage_score(inp) == pytest.approx(35.0, abs=0.01)

    def test_partial_score_additive(self):
        inp = make_account(dau_mau_ratio=0.2, feature_adoption_pct=30.0, integrations_active=2)
        # 7.5 + 6.0 + 4.0 = 17.5
        assert _usage_score(inp) == pytest.approx(17.5, abs=0.01)


# ===========================================================================
# 4. _satisfaction_score
# ===========================================================================

class TestSatisfactionScore:
    def test_returns_numeric(self):
        inp = make_account()
        assert isinstance(_satisfaction_score(inp), (int, float))

    def test_max_25(self):
        inp = make_account(nps_score=100, support_tickets_last_90d=0, critical_tickets_open=0)
        assert _satisfaction_score(inp) <= 25.0

    def test_min_0(self):
        inp = make_account(nps_score=-100, support_tickets_last_90d=20, critical_tickets_open=5)
        assert _satisfaction_score(inp) >= 0.0

    def test_nps_100_gives_15(self):
        inp = make_account(nps_score=100, support_tickets_last_90d=20, critical_tickets_open=5)
        assert _satisfaction_score(inp) == pytest.approx(15.0, abs=0.01)

    def test_nps_negative_100_gives_0_nps_component(self):
        inp = make_account(nps_score=-100, support_tickets_last_90d=20, critical_tickets_open=5)
        assert _satisfaction_score(inp) == pytest.approx(0.0, abs=0.01)

    def test_nps_zero_gives_7_5_nps_component(self):
        # (0+100)/200 * 15 = 7.5
        inp = make_account(nps_score=0, support_tickets_last_90d=20, critical_tickets_open=5)
        assert _satisfaction_score(inp) == pytest.approx(7.5, abs=0.01)

    def test_tickets_le2_gives_6(self):
        inp = make_account(nps_score=-100, support_tickets_last_90d=2, critical_tickets_open=5)
        assert _satisfaction_score(inp) == pytest.approx(6.0, abs=0.01)

    def test_tickets_0_gives_6(self):
        inp = make_account(nps_score=-100, support_tickets_last_90d=0, critical_tickets_open=5)
        assert _satisfaction_score(inp) == pytest.approx(6.0, abs=0.01)

    def test_tickets_le5_gives_4(self):
        inp = make_account(nps_score=-100, support_tickets_last_90d=4, critical_tickets_open=5)
        assert _satisfaction_score(inp) == pytest.approx(4.0, abs=0.01)

    def test_tickets_le10_gives_2(self):
        inp = make_account(nps_score=-100, support_tickets_last_90d=8, critical_tickets_open=5)
        assert _satisfaction_score(inp) == pytest.approx(2.0, abs=0.01)

    def test_tickets_gt10_gives_0(self):
        inp = make_account(nps_score=-100, support_tickets_last_90d=11, critical_tickets_open=5)
        assert _satisfaction_score(inp) == pytest.approx(0.0, abs=0.01)

    def test_critical_0_gives_4(self):
        inp = make_account(nps_score=-100, support_tickets_last_90d=20, critical_tickets_open=0)
        assert _satisfaction_score(inp) == pytest.approx(4.0, abs=0.01)

    def test_critical_1_gives_2(self):
        inp = make_account(nps_score=-100, support_tickets_last_90d=20, critical_tickets_open=1)
        assert _satisfaction_score(inp) == pytest.approx(2.0, abs=0.01)

    def test_critical_2_gives_0(self):
        inp = make_account(nps_score=-100, support_tickets_last_90d=20, critical_tickets_open=2)
        assert _satisfaction_score(inp) == pytest.approx(0.0, abs=0.01)

    def test_perfect_score(self):
        inp = make_account(nps_score=100, support_tickets_last_90d=0, critical_tickets_open=0)
        # 15 + 6 + 4 = 25
        assert _satisfaction_score(inp) == pytest.approx(25.0, abs=0.01)


# ===========================================================================
# 5. _relationship_score
# ===========================================================================

class TestRelationshipScore:
    def test_returns_numeric(self):
        inp = make_account()
        assert isinstance(_relationship_score(inp), (int, float))

    def test_max_25(self):
        inp = make_account(executive_sponsor_engaged=True, champion_score=10, stakeholders_active=10, last_qbr_days_ago=1)
        assert _relationship_score(inp) <= 25.0

    def test_min_0(self):
        inp = make_account(executive_sponsor_engaged=False, champion_score=0, stakeholders_active=0, last_qbr_days_ago=999)
        assert _relationship_score(inp) >= 0.0

    def test_exec_sponsor_adds_8(self):
        without = make_account(executive_sponsor_engaged=False, champion_score=0, stakeholders_active=0, last_qbr_days_ago=999)
        with_ = make_account(executive_sponsor_engaged=True, champion_score=0, stakeholders_active=0, last_qbr_days_ago=999)
        assert _relationship_score(with_) - _relationship_score(without) == pytest.approx(8.0, abs=0.01)

    def test_no_exec_sponsor(self):
        inp = make_account(executive_sponsor_engaged=False, champion_score=0, stakeholders_active=0, last_qbr_days_ago=999)
        assert _relationship_score(inp) == pytest.approx(0.0, abs=0.01)

    def test_champion_score_10_gives_9(self):
        inp = make_account(executive_sponsor_engaged=False, champion_score=10, stakeholders_active=0, last_qbr_days_ago=999)
        assert _relationship_score(inp) == pytest.approx(9.0, abs=0.01)

    def test_champion_score_5_gives_4_5(self):
        inp = make_account(executive_sponsor_engaged=False, champion_score=5, stakeholders_active=0, last_qbr_days_ago=999)
        assert _relationship_score(inp) == pytest.approx(4.5, abs=0.01)

    def test_stakeholders_3_gives_4_5(self):
        inp = make_account(executive_sponsor_engaged=False, champion_score=0, stakeholders_active=3, last_qbr_days_ago=999)
        assert _relationship_score(inp) == pytest.approx(4.5, abs=0.01)

    def test_stakeholders_capped_at_5(self):
        inp = make_account(executive_sponsor_engaged=False, champion_score=0, stakeholders_active=10, last_qbr_days_ago=999)
        assert _relationship_score(inp) == pytest.approx(5.0, abs=0.01)

    def test_qbr_le30_gives_3(self):
        inp = make_account(executive_sponsor_engaged=False, champion_score=0, stakeholders_active=0, last_qbr_days_ago=30)
        assert _relationship_score(inp) == pytest.approx(3.0, abs=0.01)

    def test_qbr_le60_gives_1_5(self):
        inp = make_account(executive_sponsor_engaged=False, champion_score=0, stakeholders_active=0, last_qbr_days_ago=60)
        assert _relationship_score(inp) == pytest.approx(1.5, abs=0.01)

    def test_qbr_gt60_gives_0(self):
        inp = make_account(executive_sponsor_engaged=False, champion_score=0, stakeholders_active=0, last_qbr_days_ago=61)
        assert _relationship_score(inp) == pytest.approx(0.0, abs=0.01)

    def test_all_max_capped_25(self):
        inp = make_account(executive_sponsor_engaged=True, champion_score=10, stakeholders_active=10, last_qbr_days_ago=1)
        # 8 + 9 + 5 + 3 = 25
        assert _relationship_score(inp) == pytest.approx(25.0, abs=0.01)


# ===========================================================================
# 6. _commercial_score
# ===========================================================================

class TestCommercialScore:
    def test_returns_numeric(self):
        inp = make_account()
        assert isinstance(_commercial_score(inp), (int, float))

    def test_max_15(self):
        inp = make_account(payment_on_time=True, invoices_overdue=0, contract_months_remaining=12, expansion_discussions=True)
        assert _commercial_score(inp) <= 15.0

    def test_min_0(self):
        inp = make_account(payment_on_time=False, invoices_overdue=5, contract_months_remaining=0, expansion_discussions=False)
        assert _commercial_score(inp) >= 0.0

    def test_payment_on_time_adds_5(self):
        without = make_account(payment_on_time=False, invoices_overdue=5, contract_months_remaining=0, expansion_discussions=False)
        with_ = make_account(payment_on_time=True, invoices_overdue=5, contract_months_remaining=0, expansion_discussions=False)
        assert _commercial_score(with_) - _commercial_score(without) == pytest.approx(5.0, abs=0.01)

    def test_invoices_overdue_0_gives_3(self):
        inp = make_account(payment_on_time=False, invoices_overdue=0, contract_months_remaining=0, expansion_discussions=False)
        assert _commercial_score(inp) == pytest.approx(3.0, abs=0.01)

    def test_invoices_overdue_1_gives_1(self):
        inp = make_account(payment_on_time=False, invoices_overdue=1, contract_months_remaining=0, expansion_discussions=False)
        assert _commercial_score(inp) == pytest.approx(1.0, abs=0.01)

    def test_invoices_overdue_2_gives_0(self):
        inp = make_account(payment_on_time=False, invoices_overdue=2, contract_months_remaining=0, expansion_discussions=False)
        assert _commercial_score(inp) == pytest.approx(0.0, abs=0.01)

    def test_contract_ge6_gives_4(self):
        inp = make_account(payment_on_time=False, invoices_overdue=5, contract_months_remaining=6, expansion_discussions=False)
        assert _commercial_score(inp) == pytest.approx(4.0, abs=0.01)

    def test_contract_ge3_gives_2(self):
        inp = make_account(payment_on_time=False, invoices_overdue=5, contract_months_remaining=3, expansion_discussions=False)
        assert _commercial_score(inp) == pytest.approx(2.0, abs=0.01)

    def test_contract_lt3_gives_0(self):
        inp = make_account(payment_on_time=False, invoices_overdue=5, contract_months_remaining=2, expansion_discussions=False)
        assert _commercial_score(inp) == pytest.approx(0.0, abs=0.01)

    def test_expansion_discussions_adds_3(self):
        without = make_account(payment_on_time=False, invoices_overdue=5, contract_months_remaining=0, expansion_discussions=False)
        with_ = make_account(payment_on_time=False, invoices_overdue=5, contract_months_remaining=0, expansion_discussions=True)
        assert _commercial_score(with_) - _commercial_score(without) == pytest.approx(3.0, abs=0.01)

    def test_perfect_commercial(self):
        inp = make_account(payment_on_time=True, invoices_overdue=0, contract_months_remaining=12, expansion_discussions=True)
        # 5 + 3 + 4 + 3 = 15
        assert _commercial_score(inp) == pytest.approx(15.0, abs=0.01)

    def test_no_commercial(self):
        inp = make_account(payment_on_time=False, invoices_overdue=5, contract_months_remaining=0, expansion_discussions=False)
        assert _commercial_score(inp) == pytest.approx(0.0, abs=0.01)


# ===========================================================================
# 7. _health_score (aggregate)
# ===========================================================================

class TestHealthScore:
    def test_returns_numeric(self):
        inp = make_account()
        assert isinstance(_health_score(inp), (int, float))

    def test_max_100(self):
        inp = make_account(
            dau_mau_ratio=1.0, feature_adoption_pct=100.0, integrations_active=10,
            nps_score=100, support_tickets_last_90d=0, critical_tickets_open=0,
            executive_sponsor_engaged=True, champion_score=10, stakeholders_active=10, last_qbr_days_ago=1,
            payment_on_time=True, invoices_overdue=0, contract_months_remaining=12, expansion_discussions=True,
        )
        assert _health_score(inp) <= 100.0

    def test_min_0(self):
        inp = make_account(
            dau_mau_ratio=0.0, feature_adoption_pct=0.0, integrations_active=0,
            nps_score=-100, support_tickets_last_90d=20, critical_tickets_open=10,
            executive_sponsor_engaged=False, champion_score=0, stakeholders_active=0, last_qbr_days_ago=999,
            payment_on_time=False, invoices_overdue=10, contract_months_remaining=0, expansion_discussions=False,
        )
        assert _health_score(inp) >= 0.0

    def test_perfect_account_scores_100(self):
        inp = make_account(
            dau_mau_ratio=1.0, feature_adoption_pct=100.0, integrations_active=10,
            nps_score=100, support_tickets_last_90d=0, critical_tickets_open=0,
            executive_sponsor_engaged=True, champion_score=10, stakeholders_active=10, last_qbr_days_ago=1,
            payment_on_time=True, invoices_overdue=0, contract_months_remaining=12, expansion_discussions=True,
        )
        assert _health_score(inp) == 100.0

    def test_result_is_rounded_to_1_decimal(self):
        inp = make_account(dau_mau_ratio=0.1)
        score = _health_score(inp)
        assert score == round(score, 1)

    def test_default_healthy_account_high_score(self):
        inp = make_account()
        assert _health_score(inp) >= 60.0

    def test_all_zeroes_returns_something(self):
        inp = make_account(
            dau_mau_ratio=0.0, feature_adoption_pct=0.0, integrations_active=0,
            nps_score=-100, support_tickets_last_90d=20, critical_tickets_open=10,
            executive_sponsor_engaged=False, champion_score=0, stakeholders_active=0, last_qbr_days_ago=999,
            payment_on_time=False, invoices_overdue=10, contract_months_remaining=0, expansion_discussions=False,
        )
        # NPS = -100 → (0)/200*15 = 0. Everything else 0. Score = 0.
        assert _health_score(inp) == 0.0

    def test_sum_of_components(self):
        inp = make_account(
            dau_mau_ratio=0.2, feature_adoption_pct=30.0, integrations_active=2,
            nps_score=0, support_tickets_last_90d=4, critical_tickets_open=1,
            executive_sponsor_engaged=False, champion_score=5, stakeholders_active=2, last_qbr_days_ago=45,
            payment_on_time=True, invoices_overdue=1, contract_months_remaining=4, expansion_discussions=False,
        )
        expected = (
            _usage_score(inp)
            + _satisfaction_score(inp)
            + _relationship_score(inp)
            + _commercial_score(inp)
        )
        assert _health_score(inp) == pytest.approx(round(min(100.0, max(0.0, expected)), 1), abs=0.01)


# ===========================================================================
# 8. _health_tier
# ===========================================================================

class TestHealthTier:
    def test_80_is_champion(self):
        assert _health_tier(80.0) == HealthTier.CHAMPION

    def test_100_is_champion(self):
        assert _health_tier(100.0) == HealthTier.CHAMPION

    def test_79_9_is_healthy(self):
        assert _health_tier(79.9) == HealthTier.HEALTHY

    def test_60_is_healthy(self):
        assert _health_tier(60.0) == HealthTier.HEALTHY

    def test_59_9_is_at_risk(self):
        assert _health_tier(59.9) == HealthTier.AT_RISK

    def test_35_is_at_risk(self):
        assert _health_tier(35.0) == HealthTier.AT_RISK

    def test_34_9_is_critical(self):
        assert _health_tier(34.9) == HealthTier.CRITICAL

    def test_0_is_critical(self):
        assert _health_tier(0.0) == HealthTier.CRITICAL

    def test_returns_health_tier_instance(self):
        assert isinstance(_health_tier(50.0), HealthTier)


# ===========================================================================
# 9. _churn_risk
# ===========================================================================

class TestChurnRisk:
    def test_score_below_35_imminent(self):
        inp = make_account(critical_tickets_open=0, invoices_overdue=0)
        assert _churn_risk(34.9, inp) == ChurnRisk.IMMINENT

    def test_score_0_imminent(self):
        inp = make_account(critical_tickets_open=0, invoices_overdue=0)
        assert _churn_risk(0.0, inp) == ChurnRisk.IMMINENT

    def test_critical_tickets_ge2_imminent(self):
        inp = make_account(critical_tickets_open=2, invoices_overdue=0)
        assert _churn_risk(90.0, inp) == ChurnRisk.IMMINENT

    def test_critical_tickets_3_imminent(self):
        inp = make_account(critical_tickets_open=3, invoices_overdue=0)
        assert _churn_risk(90.0, inp) == ChurnRisk.IMMINENT

    def test_invoices_overdue_ge2_imminent(self):
        inp = make_account(critical_tickets_open=0, invoices_overdue=2)
        assert _churn_risk(90.0, inp) == ChurnRisk.IMMINENT

    def test_invoices_overdue_5_imminent(self):
        inp = make_account(critical_tickets_open=0, invoices_overdue=5)
        assert _churn_risk(90.0, inp) == ChurnRisk.IMMINENT

    def test_score_below_60_high(self):
        inp = make_account(critical_tickets_open=0, invoices_overdue=0, contract_months_remaining=12)
        assert _churn_risk(50.0, inp) == ChurnRisk.HIGH

    def test_contract_le3_and_score_below_70_high(self):
        inp = make_account(critical_tickets_open=0, invoices_overdue=0, contract_months_remaining=3)
        assert _churn_risk(65.0, inp) == ChurnRisk.HIGH

    def test_contract_le3_score_ge70_not_high(self):
        inp = make_account(critical_tickets_open=0, invoices_overdue=0, contract_months_remaining=3, nps_score=40)
        risk = _churn_risk(70.0, inp)
        # score=70 >= 60; contract=3 <= 3 but score not < 70, so not HIGH; score=70 < 75 → MEDIUM
        assert risk == ChurnRisk.MEDIUM

    def test_score_below_75_medium(self):
        inp = make_account(critical_tickets_open=0, invoices_overdue=0, contract_months_remaining=12, nps_score=10)
        assert _churn_risk(70.0, inp) == ChurnRisk.MEDIUM

    def test_nps_negative_medium(self):
        inp = make_account(critical_tickets_open=0, invoices_overdue=0, contract_months_remaining=12, nps_score=-1)
        assert _churn_risk(80.0, inp) == ChurnRisk.MEDIUM

    def test_perfect_account_low(self):
        inp = make_account(critical_tickets_open=0, invoices_overdue=0, contract_months_remaining=12, nps_score=50)
        assert _churn_risk(80.0, inp) == ChurnRisk.LOW

    def test_returns_churn_risk_instance(self):
        inp = make_account()
        assert isinstance(_churn_risk(80.0, inp), ChurnRisk)


# ===========================================================================
# 10. _expansion_potential
# ===========================================================================

class TestExpansionPotential:
    def test_strong_all_conditions(self):
        inp = make_account(expansion_discussions=True, champion_score=7)
        assert _expansion_potential(75.0, inp) == ExpansionPotential.STRONG

    def test_strong_requires_ge75(self):
        inp = make_account(expansion_discussions=True, champion_score=7)
        result = _expansion_potential(74.9, inp)
        # At 74.9, score<75 so cannot be STRONG; expansion=True so MODERATE (score>=60)
        assert result == ExpansionPotential.MODERATE

    def test_strong_requires_expansion_discussions(self):
        inp = make_account(expansion_discussions=False, champion_score=7)
        result = _expansion_potential(75.0, inp)
        # champion_score=7>=6 so MODERATE
        assert result == ExpansionPotential.MODERATE

    def test_strong_requires_champion_ge7(self):
        inp = make_account(expansion_discussions=True, champion_score=6)
        result = _expansion_potential(75.0, inp)
        # expansion=True so MODERATE (score>=60)
        assert result == ExpansionPotential.MODERATE

    def test_moderate_expansion_true(self):
        inp = make_account(expansion_discussions=True, champion_score=0)
        assert _expansion_potential(60.0, inp) == ExpansionPotential.MODERATE

    def test_moderate_champion_ge6(self):
        inp = make_account(expansion_discussions=False, champion_score=6)
        assert _expansion_potential(60.0, inp) == ExpansionPotential.MODERATE

    def test_moderate_requires_ge60(self):
        inp = make_account(expansion_discussions=True, champion_score=6)
        result = _expansion_potential(59.9, inp)
        # score=59.9 >= 45 → LIMITED
        assert result == ExpansionPotential.LIMITED

    def test_limited_score_ge45(self):
        inp = make_account(expansion_discussions=False, champion_score=0)
        assert _expansion_potential(45.0, inp) == ExpansionPotential.LIMITED

    def test_limited_score_45_to_59(self):
        inp = make_account(expansion_discussions=False, champion_score=0)
        assert _expansion_potential(50.0, inp) == ExpansionPotential.LIMITED

    def test_none_score_below_45(self):
        inp = make_account(expansion_discussions=False, champion_score=0)
        assert _expansion_potential(44.9, inp) == ExpansionPotential.NONE

    def test_none_score_0(self):
        inp = make_account(expansion_discussions=False, champion_score=0)
        assert _expansion_potential(0.0, inp) == ExpansionPotential.NONE

    def test_returns_expansion_potential_instance(self):
        inp = make_account()
        assert isinstance(_expansion_potential(70.0, inp), ExpansionPotential)


# ===========================================================================
# 11. _health_action
# ===========================================================================

class TestHealthAction:
    def test_champion_tier_celebrate(self):
        assert _health_action(HealthTier.CHAMPION, ChurnRisk.LOW) == HealthAction.CELEBRATE

    def test_champion_tier_celebrate_even_high_churn(self):
        assert _health_action(HealthTier.CHAMPION, ChurnRisk.HIGH) == HealthAction.CELEBRATE

    def test_healthy_tier_maintain(self):
        assert _health_action(HealthTier.HEALTHY, ChurnRisk.MEDIUM) == HealthAction.MAINTAIN

    def test_healthy_tier_maintain_low_churn(self):
        assert _health_action(HealthTier.HEALTHY, ChurnRisk.LOW) == HealthAction.MAINTAIN

    def test_at_risk_tier_intervene(self):
        assert _health_action(HealthTier.AT_RISK, ChurnRisk.MEDIUM) == HealthAction.INTERVENE

    def test_at_risk_tier_with_high_churn_intervene(self):
        assert _health_action(HealthTier.AT_RISK, ChurnRisk.HIGH) == HealthAction.INTERVENE

    def test_healthy_high_churn_still_maintain(self):
        # HEALTHY tier short-circuits to MAINTAIN before the churn-HIGH check
        assert _health_action(HealthTier.HEALTHY, ChurnRisk.HIGH) == HealthAction.MAINTAIN

    def test_critical_tier_escalate(self):
        assert _health_action(HealthTier.CRITICAL, ChurnRisk.IMMINENT) == HealthAction.ESCALATE

    def test_critical_medium_churn_escalate(self):
        assert _health_action(HealthTier.CRITICAL, ChurnRisk.MEDIUM) == HealthAction.ESCALATE

    def test_returns_health_action_instance(self):
        assert isinstance(_health_action(HealthTier.HEALTHY, ChurnRisk.LOW), HealthAction)


# ===========================================================================
# 12. _renewal_probability
# ===========================================================================

class TestRenewalProbability:
    def test_returns_numeric(self):
        inp = make_account()
        assert isinstance(_renewal_probability(80.0, inp), (int, float))

    def test_base_score_times_085(self):
        inp = make_account(
            contract_months_remaining=12, invoices_overdue=0, nps_score=10,
            executive_sponsor_engaged=False, expansion_discussions=False,
        )
        assert _renewal_probability(80.0, inp) == pytest.approx(68.0, abs=0.01)

    def test_contract_le2_deducts_10(self):
        base_inp = make_account(contract_months_remaining=3, invoices_overdue=0, nps_score=10,
                                executive_sponsor_engaged=False, expansion_discussions=False)
        short_inp = make_account(contract_months_remaining=2, invoices_overdue=0, nps_score=10,
                                 executive_sponsor_engaged=False, expansion_discussions=False)
        diff = _renewal_probability(80.0, short_inp) - _renewal_probability(80.0, base_inp)
        assert diff == pytest.approx(-10.0, abs=0.01)

    def test_invoices_ge2_deducts_8(self):
        ok = make_account(contract_months_remaining=12, invoices_overdue=1, nps_score=10,
                          executive_sponsor_engaged=False, expansion_discussions=False)
        bad = make_account(contract_months_remaining=12, invoices_overdue=2, nps_score=10,
                           executive_sponsor_engaged=False, expansion_discussions=False)
        diff = _renewal_probability(80.0, bad) - _renewal_probability(80.0, ok)
        assert diff == pytest.approx(-8.0, abs=0.01)

    def test_nps_below_minus20_deducts_5(self):
        ok = make_account(contract_months_remaining=12, invoices_overdue=0, nps_score=-20,
                          executive_sponsor_engaged=False, expansion_discussions=False)
        bad = make_account(contract_months_remaining=12, invoices_overdue=0, nps_score=-21,
                           executive_sponsor_engaged=False, expansion_discussions=False)
        diff = _renewal_probability(80.0, bad) - _renewal_probability(80.0, ok)
        assert diff == pytest.approx(-5.0, abs=0.01)

    def test_exec_sponsor_adds_5(self):
        without = make_account(contract_months_remaining=12, invoices_overdue=0, nps_score=10,
                               executive_sponsor_engaged=False, expansion_discussions=False)
        with_ = make_account(contract_months_remaining=12, invoices_overdue=0, nps_score=10,
                              executive_sponsor_engaged=True, expansion_discussions=False)
        diff = _renewal_probability(80.0, with_) - _renewal_probability(80.0, without)
        assert diff == pytest.approx(5.0, abs=0.01)

    def test_expansion_discussions_adds_3(self):
        without = make_account(contract_months_remaining=12, invoices_overdue=0, nps_score=10,
                               executive_sponsor_engaged=False, expansion_discussions=False)
        with_ = make_account(contract_months_remaining=12, invoices_overdue=0, nps_score=10,
                              executive_sponsor_engaged=False, expansion_discussions=True)
        diff = _renewal_probability(80.0, with_) - _renewal_probability(80.0, without)
        assert diff == pytest.approx(3.0, abs=0.01)

    def test_clamped_max_100(self):
        inp = make_account(contract_months_remaining=12, invoices_overdue=0, nps_score=50,
                           executive_sponsor_engaged=True, expansion_discussions=True)
        assert _renewal_probability(100.0, inp) <= 100.0

    def test_clamped_min_0(self):
        inp = make_account(contract_months_remaining=1, invoices_overdue=3, nps_score=-50,
                           executive_sponsor_engaged=False, expansion_discussions=False)
        assert _renewal_probability(0.0, inp) >= 0.0

    def test_rounded_to_1_decimal(self):
        inp = make_account()
        prob = _renewal_probability(75.0, inp)
        assert prob == round(prob, 1)


# ===========================================================================
# 13. _health_drivers
# ===========================================================================

class TestHealthDrivers:
    def test_returns_list(self):
        inp = make_account()
        assert isinstance(_health_drivers(inp, 80.0), list)

    def test_high_dau_mau_adds_driver(self):
        inp = make_account(dau_mau_ratio=0.3)
        drivers = _health_drivers(inp, 80.0)
        assert any("DAU/MAU" in d for d in drivers)

    def test_low_dau_mau_no_driver(self):
        inp = make_account(dau_mau_ratio=0.29)
        drivers = _health_drivers(inp, 80.0)
        assert not any("DAU/MAU" in d for d in drivers)

    def test_high_feature_adoption_adds_driver(self):
        inp = make_account(feature_adoption_pct=50.0)
        drivers = _health_drivers(inp, 80.0)
        assert any("Adoption" in d for d in drivers)

    def test_low_feature_adoption_no_driver(self):
        inp = make_account(feature_adoption_pct=49.0)
        drivers = _health_drivers(inp, 80.0)
        assert not any("Adoption" in d for d in drivers)

    def test_high_nps_adds_driver(self):
        inp = make_account(nps_score=30)
        drivers = _health_drivers(inp, 80.0)
        assert any("NPS" in d for d in drivers)

    def test_low_nps_no_driver(self):
        inp = make_account(nps_score=29)
        drivers = _health_drivers(inp, 80.0)
        assert not any("NPS excellent" in d for d in drivers)

    def test_exec_sponsor_adds_driver(self):
        inp = make_account(executive_sponsor_engaged=True)
        drivers = _health_drivers(inp, 80.0)
        assert any("Sponsor" in d for d in drivers)

    def test_no_exec_sponsor_no_driver(self):
        inp = make_account(executive_sponsor_engaged=False)
        drivers = _health_drivers(inp, 80.0)
        assert not any("Sponsor" in d for d in drivers)

    def test_high_champion_adds_driver(self):
        inp = make_account(champion_score=7)
        drivers = _health_drivers(inp, 80.0)
        assert any("Champion" in d for d in drivers)

    def test_low_champion_no_driver(self):
        inp = make_account(champion_score=6)
        drivers = _health_drivers(inp, 80.0)
        assert not any("Champion fort" in d for d in drivers)

    def test_expansion_discussions_adds_driver(self):
        inp = make_account(expansion_discussions=True)
        drivers = _health_drivers(inp, 80.0)
        assert any("expansion" in d for d in drivers)

    def test_no_expansion_no_driver(self):
        inp = make_account(expansion_discussions=False)
        drivers = _health_drivers(inp, 80.0)
        assert not any("expansion" in d for d in drivers)

    def test_many_integrations_adds_driver(self):
        inp = make_account(integrations_active=3)
        drivers = _health_drivers(inp, 80.0)
        assert any("intégration" in d for d in drivers)

    def test_few_integrations_no_driver(self):
        inp = make_account(integrations_active=2)
        drivers = _health_drivers(inp, 80.0)
        assert not any("intégrations actives" in d for d in drivers)

    def test_perfect_payment_adds_driver(self):
        inp = make_account(payment_on_time=True, invoices_overdue=0)
        drivers = _health_drivers(inp, 80.0)
        assert any("paiement" in d for d in drivers)

    def test_late_payment_no_driver(self):
        inp = make_account(payment_on_time=True, invoices_overdue=1)
        drivers = _health_drivers(inp, 80.0)
        assert not any("parfait" in d for d in drivers)


# ===========================================================================
# 14. _risk_signals
# ===========================================================================

class TestRiskSignals:
    def test_returns_list(self):
        inp = make_account()
        assert isinstance(_risk_signals(inp, 80.0), list)

    def test_low_dau_mau_adds_signal(self):
        inp = make_account(dau_mau_ratio=0.19)
        signals = _risk_signals(inp, 80.0)
        assert any("DAU/MAU" in s for s in signals)

    def test_ok_dau_mau_no_signal(self):
        inp = make_account(dau_mau_ratio=0.2)
        signals = _risk_signals(inp, 80.0)
        assert not any("DAU/MAU" in s for s in signals)

    def test_low_feature_adoption_adds_signal(self):
        inp = make_account(feature_adoption_pct=29.0)
        signals = _risk_signals(inp, 80.0)
        assert any("Adoption" in s for s in signals)

    def test_ok_feature_adoption_no_signal(self):
        inp = make_account(feature_adoption_pct=30.0)
        signals = _risk_signals(inp, 80.0)
        assert not any("Adoption" in s for s in signals)

    def test_negative_nps_adds_signal(self):
        inp = make_account(nps_score=-1)
        signals = _risk_signals(inp, 80.0)
        assert any("NPS" in s for s in signals)

    def test_zero_nps_no_signal(self):
        inp = make_account(nps_score=0)
        signals = _risk_signals(inp, 80.0)
        assert not any("NPS négatif" in s for s in signals)

    def test_critical_tickets_adds_signal(self):
        inp = make_account(critical_tickets_open=1)
        signals = _risk_signals(inp, 80.0)
        assert any("critique" in s for s in signals)

    def test_no_critical_tickets_no_signal(self):
        inp = make_account(critical_tickets_open=0)
        signals = _risk_signals(inp, 80.0)
        assert not any("critique" in s for s in signals)

    def test_short_contract_adds_signal(self):
        inp = make_account(contract_months_remaining=3)
        signals = _risk_signals(inp, 80.0)
        assert any("Renouvellement" in s for s in signals)

    def test_long_contract_no_signal(self):
        inp = make_account(contract_months_remaining=4)
        signals = _risk_signals(inp, 80.0)
        assert not any("Renouvellement" in s for s in signals)

    def test_old_qbr_adds_signal(self):
        inp = make_account(last_qbr_days_ago=91)
        signals = _risk_signals(inp, 80.0)
        assert any("QBR" in s for s in signals)

    def test_recent_qbr_no_signal(self):
        inp = make_account(last_qbr_days_ago=90)
        signals = _risk_signals(inp, 80.0)
        assert not any("QBR" in s for s in signals)

    def test_no_exec_sponsor_adds_signal(self):
        inp = make_account(executive_sponsor_engaged=False)
        signals = _risk_signals(inp, 80.0)
        assert any("sponsor" in s for s in signals)

    def test_exec_sponsor_no_signal(self):
        inp = make_account(executive_sponsor_engaged=True)
        signals = _risk_signals(inp, 80.0)
        assert not any("sponsor" in s for s in signals)

    def test_overdue_invoices_adds_signal(self):
        inp = make_account(invoices_overdue=1)
        signals = _risk_signals(inp, 80.0)
        assert any("facture" in s for s in signals)

    def test_no_overdue_invoices_no_signal(self):
        inp = make_account(invoices_overdue=0)
        signals = _risk_signals(inp, 80.0)
        assert not any("facture" in s for s in signals)

    def test_weak_champion_adds_signal(self):
        inp = make_account(champion_score=4)
        signals = _risk_signals(inp, 80.0)
        assert any("Champion faible" in s for s in signals)

    def test_ok_champion_no_signal(self):
        inp = make_account(champion_score=5)
        signals = _risk_signals(inp, 80.0)
        assert not any("Champion faible" in s for s in signals)


# ===========================================================================
# 15. _recommended_plays
# ===========================================================================

class TestRecommendedPlays:
    def test_returns_list(self):
        inp = make_account()
        plays = _recommended_plays(HealthTier.CHAMPION, ChurnRisk.LOW, ExpansionPotential.STRONG, inp)
        assert isinstance(plays, list)

    def test_champion_includes_reference(self):
        inp = make_account()
        plays = _recommended_plays(HealthTier.CHAMPION, ChurnRisk.LOW, ExpansionPotential.MODERATE, inp)
        assert any("référence" in p for p in plays)

    def test_champion_includes_roadmap(self):
        inp = make_account()
        plays = _recommended_plays(HealthTier.CHAMPION, ChurnRisk.LOW, ExpansionPotential.MODERATE, inp)
        assert any("roadmap" in p for p in plays)

    def test_champion_strong_expansion_includes_upsell(self):
        inp = make_account()
        plays = _recommended_plays(HealthTier.CHAMPION, ChurnRisk.LOW, ExpansionPotential.STRONG, inp)
        assert any("upsell" in p for p in plays)

    def test_champion_no_strong_expansion_no_upsell(self):
        inp = make_account()
        plays = _recommended_plays(HealthTier.CHAMPION, ChurnRisk.LOW, ExpansionPotential.MODERATE, inp)
        assert not any("upsell" in p for p in plays)

    def test_healthy_includes_qbr(self):
        inp = make_account()
        plays = _recommended_plays(HealthTier.HEALTHY, ChurnRisk.LOW, ExpansionPotential.NONE, inp)
        assert any("QBR" in p for p in plays)

    def test_healthy_with_expansion_includes_explorer(self):
        inp = make_account()
        plays = _recommended_plays(HealthTier.HEALTHY, ChurnRisk.LOW, ExpansionPotential.MODERATE, inp)
        assert any("expansion" in p for p in plays)

    def test_healthy_no_expansion_no_explorer(self):
        inp = make_account()
        plays = _recommended_plays(HealthTier.HEALTHY, ChurnRisk.LOW, ExpansionPotential.NONE, inp)
        assert not any("expansion" in p for p in plays)

    def test_at_risk_includes_urgent_review(self):
        inp = make_account()
        plays = _recommended_plays(HealthTier.AT_RISK, ChurnRisk.MEDIUM, ExpansionPotential.NONE, inp)
        assert any("urgente" in p for p in plays)

    def test_at_risk_critical_tickets_includes_resolve(self):
        inp = make_account(critical_tickets_open=1)
        plays = _recommended_plays(HealthTier.AT_RISK, ChurnRisk.MEDIUM, ExpansionPotential.NONE, inp)
        assert any("tickets critiques" in p for p in plays)

    def test_at_risk_no_critical_tickets_no_resolve(self):
        inp = make_account(critical_tickets_open=0)
        plays = _recommended_plays(HealthTier.AT_RISK, ChurnRisk.MEDIUM, ExpansionPotential.NONE, inp)
        assert not any("tickets critiques" in p for p in plays)

    def test_at_risk_low_dau_includes_activation(self):
        inp = make_account(dau_mau_ratio=0.19)
        plays = _recommended_plays(HealthTier.AT_RISK, ChurnRisk.MEDIUM, ExpansionPotential.NONE, inp)
        assert any("activation" in p for p in plays)

    def test_critical_includes_c_level_escalation(self):
        inp = make_account()
        plays = _recommended_plays(HealthTier.CRITICAL, ChurnRisk.IMMINENT, ExpansionPotential.NONE, inp)
        assert any("C-level" in p for p in plays)

    def test_critical_overdue_includes_resolve_invoices(self):
        inp = make_account(invoices_overdue=1)
        plays = _recommended_plays(HealthTier.CRITICAL, ChurnRisk.IMMINENT, ExpansionPotential.NONE, inp)
        assert any("impayés" in p for p in plays)

    def test_critical_no_overdue_no_invoice_play(self):
        inp = make_account(invoices_overdue=0)
        plays = _recommended_plays(HealthTier.CRITICAL, ChurnRisk.IMMINENT, ExpansionPotential.NONE, inp)
        assert not any("impayés" in p for p in plays)


# ===========================================================================
# 16. AccountHealthResult dataclass
# ===========================================================================

class TestAccountHealthResult:
    def _make_result(self):
        engine = AccountHealthScorerEngine()
        return engine.score(make_account())

    def test_result_has_account_id(self):
        r = self._make_result()
        assert r.account_id == "acc-001"

    def test_result_has_account_name(self):
        r = self._make_result()
        assert r.account_name == "Acme Corp"

    def test_result_has_arr_eur(self):
        r = self._make_result()
        assert r.arr_eur == 100_000.0

    def test_result_has_segment(self):
        r = self._make_result()
        assert r.segment == "enterprise"

    def test_result_health_score_numeric(self):
        r = self._make_result()
        assert isinstance(r.health_score, (int, float))

    def test_result_health_tier_is_enum(self):
        r = self._make_result()
        assert isinstance(r.health_tier, HealthTier)

    def test_result_health_action_is_enum(self):
        r = self._make_result()
        assert isinstance(r.health_action, HealthAction)

    def test_result_churn_risk_is_enum(self):
        r = self._make_result()
        assert isinstance(r.churn_risk, ChurnRisk)

    def test_result_expansion_potential_is_enum(self):
        r = self._make_result()
        assert isinstance(r.expansion_potential, ExpansionPotential)

    def test_result_health_drivers_is_list(self):
        r = self._make_result()
        assert isinstance(r.health_drivers, list)

    def test_result_risk_signals_is_list(self):
        r = self._make_result()
        assert isinstance(r.risk_signals, list)

    def test_result_recommended_plays_is_list(self):
        r = self._make_result()
        assert isinstance(r.recommended_plays, list)

    def test_result_renewal_probability_numeric(self):
        r = self._make_result()
        assert isinstance(r.renewal_probability_pct, (int, float))

    def test_to_dict_returns_dict(self):
        r = self._make_result()
        d = r.to_dict()
        assert isinstance(d, dict)

    def test_to_dict_has_all_keys(self):
        r = self._make_result()
        d = r.to_dict()
        expected_keys = {
            "account_id", "account_name", "arr_eur", "segment",
            "health_score", "health_tier", "health_action",
            "churn_risk", "expansion_potential",
            "health_drivers", "risk_signals", "recommended_plays",
            "renewal_probability_pct",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_tier_is_string(self):
        r = self._make_result()
        assert isinstance(r.to_dict()["health_tier"], str)

    def test_to_dict_action_is_string(self):
        r = self._make_result()
        assert isinstance(r.to_dict()["health_action"], str)

    def test_to_dict_churn_risk_is_string(self):
        r = self._make_result()
        assert isinstance(r.to_dict()["churn_risk"], str)

    def test_to_dict_expansion_is_string(self):
        r = self._make_result()
        assert isinstance(r.to_dict()["expansion_potential"], str)


# ===========================================================================
# 17. AccountHealthScorerEngine.score
# ===========================================================================

class TestEngineScore:
    def test_returns_result(self):
        engine = AccountHealthScorerEngine()
        result = engine.score(make_account())
        assert isinstance(result, AccountHealthResult)

    def test_score_stored_in_results(self):
        engine = AccountHealthScorerEngine()
        engine.score(make_account())
        assert len(engine.all_accounts()) == 1

    def test_score_replaces_existing(self):
        engine = AccountHealthScorerEngine()
        engine.score(make_account())
        engine.score(make_account())
        assert len(engine.all_accounts()) == 1

    def test_different_accounts_stored_separately(self):
        engine = AccountHealthScorerEngine()
        engine.score(make_account(account_id="a1"))
        engine.score(make_account(account_id="a2"))
        assert len(engine.all_accounts()) == 2

    def test_champion_account(self):
        engine = AccountHealthScorerEngine()
        result = engine.score(make_account(
            dau_mau_ratio=1.0, feature_adoption_pct=100.0, integrations_active=10,
            nps_score=100, support_tickets_last_90d=0, critical_tickets_open=0,
            executive_sponsor_engaged=True, champion_score=10, stakeholders_active=10,
            last_qbr_days_ago=1, payment_on_time=True, invoices_overdue=0,
            contract_months_remaining=12, expansion_discussions=True,
        ))
        assert result.health_tier == HealthTier.CHAMPION

    def test_critical_account(self):
        engine = AccountHealthScorerEngine()
        result = engine.score(make_account(
            dau_mau_ratio=0.0, feature_adoption_pct=0.0, integrations_active=0,
            nps_score=-100, support_tickets_last_90d=20, critical_tickets_open=5,
            executive_sponsor_engaged=False, champion_score=0, stakeholders_active=0,
            last_qbr_days_ago=365, payment_on_time=False, invoices_overdue=5,
            contract_months_remaining=0, expansion_discussions=False,
        ))
        assert result.health_tier == HealthTier.CRITICAL

    def test_renewal_probability_in_range(self):
        engine = AccountHealthScorerEngine()
        result = engine.score(make_account())
        assert 0.0 <= result.renewal_probability_pct <= 100.0

    def test_result_account_id_matches(self):
        engine = AccountHealthScorerEngine()
        result = engine.score(make_account(account_id="xyz"))
        assert result.account_id == "xyz"


# ===========================================================================
# 18. AccountHealthScorerEngine.score_batch
# ===========================================================================

class TestEngineBatch:
    def test_returns_list(self):
        engine = AccountHealthScorerEngine()
        results = engine.score_batch([make_account(account_id="a1"), make_account(account_id="a2")])
        assert isinstance(results, list)

    def test_all_accounts_scored(self):
        engine = AccountHealthScorerEngine()
        accounts = [make_account(account_id=f"a{i}") for i in range(5)]
        results = engine.score_batch(accounts)
        assert len(results) == 5

    def test_sorted_descending(self):
        engine = AccountHealthScorerEngine()
        good = make_account(account_id="good", dau_mau_ratio=1.0, feature_adoption_pct=100.0)
        bad = make_account(account_id="bad", dau_mau_ratio=0.0, feature_adoption_pct=0.0,
                           executive_sponsor_engaged=False, nps_score=-100,
                           payment_on_time=False, invoices_overdue=5)
        results = engine.score_batch([bad, good])
        assert results[0].health_score >= results[1].health_score

    def test_empty_batch(self):
        engine = AccountHealthScorerEngine()
        results = engine.score_batch([])
        assert results == []

    def test_single_account_batch(self):
        engine = AccountHealthScorerEngine()
        results = engine.score_batch([make_account()])
        assert len(results) == 1

    def test_batch_accumulates_in_engine(self):
        engine = AccountHealthScorerEngine()
        engine.score_batch([make_account(account_id="a1"), make_account(account_id="a2")])
        assert len(engine.all_accounts()) == 2


# ===========================================================================
# 19. Engine filter methods: by_tier, by_action, by_churn_risk
# ===========================================================================

class TestEngineFilterMethods:
    def _engine_with_diverse_accounts(self):
        engine = AccountHealthScorerEngine()
        # Champion
        engine.score(make_account(account_id="champion",
            dau_mau_ratio=1.0, feature_adoption_pct=100.0, integrations_active=10,
            nps_score=100, support_tickets_last_90d=0, critical_tickets_open=0,
            executive_sponsor_engaged=True, champion_score=10, stakeholders_active=10,
            last_qbr_days_ago=1, payment_on_time=True, invoices_overdue=0,
            contract_months_remaining=12, expansion_discussions=True,
        ))
        # Critical
        engine.score(make_account(account_id="critical",
            dau_mau_ratio=0.0, feature_adoption_pct=0.0, integrations_active=0,
            nps_score=-100, support_tickets_last_90d=20, critical_tickets_open=5,
            executive_sponsor_engaged=False, champion_score=0, stakeholders_active=0,
            last_qbr_days_ago=365, payment_on_time=False, invoices_overdue=5,
            contract_months_remaining=0, expansion_discussions=False,
        ))
        return engine

    def test_by_tier_champion(self):
        engine = self._engine_with_diverse_accounts()
        champions = engine.by_tier(HealthTier.CHAMPION)
        assert all(r.health_tier == HealthTier.CHAMPION for r in champions)

    def test_by_tier_critical(self):
        engine = self._engine_with_diverse_accounts()
        crits = engine.by_tier(HealthTier.CRITICAL)
        assert all(r.health_tier == HealthTier.CRITICAL for r in crits)

    def test_by_tier_returns_list(self):
        engine = self._engine_with_diverse_accounts()
        assert isinstance(engine.by_tier(HealthTier.HEALTHY), list)

    def test_by_tier_empty_when_none(self):
        engine = self._engine_with_diverse_accounts()
        assert engine.by_tier(HealthTier.HEALTHY) == []

    def test_by_action_returns_list(self):
        engine = self._engine_with_diverse_accounts()
        assert isinstance(engine.by_action(HealthAction.CELEBRATE), list)

    def test_by_action_celebrate_has_champion(self):
        engine = self._engine_with_diverse_accounts()
        results = engine.by_action(HealthAction.CELEBRATE)
        assert all(r.health_action == HealthAction.CELEBRATE for r in results)

    def test_by_churn_risk_returns_list(self):
        engine = self._engine_with_diverse_accounts()
        assert isinstance(engine.by_churn_risk(ChurnRisk.LOW), list)

    def test_by_churn_risk_imminent_has_critical(self):
        engine = self._engine_with_diverse_accounts()
        results = engine.by_churn_risk(ChurnRisk.IMMINENT)
        assert all(r.churn_risk == ChurnRisk.IMMINENT for r in results)


# ===========================================================================
# 20. Engine convenience methods
# ===========================================================================

class TestEngineConvenience:
    def _populated_engine(self):
        engine = AccountHealthScorerEngine()
        # Champion
        engine.score(make_account(account_id="c1",
            dau_mau_ratio=1.0, feature_adoption_pct=100.0, integrations_active=10,
            nps_score=100, support_tickets_last_90d=0, critical_tickets_open=0,
            executive_sponsor_engaged=True, champion_score=10, stakeholders_active=10,
            last_qbr_days_ago=1, payment_on_time=True, invoices_overdue=0,
            contract_months_remaining=12, expansion_discussions=True,
        ))
        # Critical with large ARR
        engine.score(make_account(account_id="crit1", arr_eur=500_000.0,
            dau_mau_ratio=0.0, feature_adoption_pct=0.0, integrations_active=0,
            nps_score=-100, support_tickets_last_90d=20, critical_tickets_open=5,
            executive_sponsor_engaged=False, champion_score=0, stakeholders_active=0,
            last_qbr_days_ago=365, payment_on_time=False, invoices_overdue=5,
            contract_months_remaining=0, expansion_discussions=False,
        ))
        return engine

    def test_champions_returns_list(self):
        engine = self._populated_engine()
        assert isinstance(engine.champions(), list)

    def test_champions_only_champions(self):
        engine = self._populated_engine()
        assert all(r.health_tier == HealthTier.CHAMPION for r in engine.champions())

    def test_critical_accounts_returns_list(self):
        engine = self._populated_engine()
        assert isinstance(engine.critical_accounts(), list)

    def test_critical_accounts_only_critical(self):
        engine = self._populated_engine()
        assert all(r.health_tier == HealthTier.CRITICAL for r in engine.critical_accounts())

    def test_needs_escalation_returns_list(self):
        engine = self._populated_engine()
        assert isinstance(engine.needs_escalation(), list)

    def test_needs_escalation_only_escalate(self):
        engine = self._populated_engine()
        assert all(r.health_action == HealthAction.ESCALATE for r in engine.needs_escalation())

    def test_at_risk_accounts_includes_at_risk_and_critical(self):
        engine = self._populated_engine()
        results = engine.at_risk_accounts()
        for r in results:
            assert r.health_tier in (HealthTier.AT_RISK, HealthTier.CRITICAL)

    def test_expansion_ready_includes_strong_and_moderate(self):
        engine = self._populated_engine()
        results = engine.expansion_ready()
        for r in results:
            assert r.expansion_potential in (ExpansionPotential.STRONG, ExpansionPotential.MODERATE)

    def test_avg_health_score_numeric(self):
        engine = self._populated_engine()
        assert isinstance(engine.avg_health_score(), (int, float))

    def test_avg_health_score_empty_engine(self):
        engine = AccountHealthScorerEngine()
        assert engine.avg_health_score() == 0.0

    def test_avg_health_score_single(self):
        engine = AccountHealthScorerEngine()
        result = engine.score(make_account())
        assert engine.avg_health_score() == result.health_score

    def test_avg_health_score_correct(self):
        engine = AccountHealthScorerEngine()
        r1 = engine.score(make_account(account_id="a1"))
        r2 = engine.score(make_account(account_id="a2"))
        expected = round((r1.health_score + r2.health_score) / 2, 1)
        assert engine.avg_health_score() == pytest.approx(expected, abs=0.01)

    def test_total_arr_at_risk_eur_numeric(self):
        engine = self._populated_engine()
        assert isinstance(engine.total_arr_at_risk_eur(), (int, float))

    def test_total_arr_at_risk_eur_includes_critical(self):
        engine = self._populated_engine()
        total = engine.total_arr_at_risk_eur()
        assert total >= 500_000.0  # the critical account

    def test_total_arr_at_risk_empty(self):
        engine = AccountHealthScorerEngine()
        assert engine.total_arr_at_risk_eur() == 0.0

    def test_all_accounts_sorted_desc(self):
        engine = self._populated_engine()
        accounts = engine.all_accounts()
        scores = [r.health_score for r in accounts]
        assert scores == sorted(scores, reverse=True)

    def test_all_accounts_returns_list(self):
        engine = self._populated_engine()
        assert isinstance(engine.all_accounts(), list)


# ===========================================================================
# 21. Engine.summary
# ===========================================================================

class TestEngineSummary:
    def _engine(self):
        engine = AccountHealthScorerEngine()
        engine.score(make_account(account_id="c1",
            dau_mau_ratio=1.0, feature_adoption_pct=100.0, integrations_active=10,
            nps_score=100, support_tickets_last_90d=0, critical_tickets_open=0,
            executive_sponsor_engaged=True, champion_score=10, stakeholders_active=10,
            last_qbr_days_ago=1, payment_on_time=True, invoices_overdue=0,
            contract_months_remaining=12, expansion_discussions=True,
        ))
        engine.score(make_account(account_id="crit1",
            dau_mau_ratio=0.0, feature_adoption_pct=0.0, integrations_active=0,
            nps_score=-100, support_tickets_last_90d=20, critical_tickets_open=5,
            executive_sponsor_engaged=False, champion_score=0, stakeholders_active=0,
            last_qbr_days_ago=365, payment_on_time=False, invoices_overdue=5,
            contract_months_remaining=0, expansion_discussions=False,
        ))
        return engine

    def test_summary_returns_dict(self):
        engine = self._engine()
        assert isinstance(engine.summary(), dict)

    def test_summary_total_key(self):
        engine = self._engine()
        s = engine.summary()
        assert "total" in s

    def test_summary_total_correct(self):
        engine = self._engine()
        s = engine.summary()
        assert s["total"] == 2

    def test_summary_tier_counts_key(self):
        engine = self._engine()
        assert "tier_counts" in engine.summary()

    def test_summary_tier_counts_has_all_tiers(self):
        engine = self._engine()
        tc = engine.summary()["tier_counts"]
        for t in HealthTier:
            assert t.value in tc

    def test_summary_action_counts_key(self):
        engine = self._engine()
        assert "action_counts" in engine.summary()

    def test_summary_action_counts_has_all_actions(self):
        engine = self._engine()
        ac = engine.summary()["action_counts"]
        for a in HealthAction:
            assert a.value in ac

    def test_summary_churn_counts_key(self):
        engine = self._engine()
        assert "churn_counts" in engine.summary()

    def test_summary_churn_counts_has_all_churn_risks(self):
        engine = self._engine()
        cc = engine.summary()["churn_counts"]
        for c in ChurnRisk:
            assert c.value in cc

    def test_summary_avg_health_score_key(self):
        engine = self._engine()
        assert "avg_health_score" in engine.summary()

    def test_summary_avg_health_score_numeric(self):
        engine = self._engine()
        assert isinstance(engine.summary()["avg_health_score"], (int, float))

    def test_summary_champion_count_key(self):
        engine = self._engine()
        assert "champion_count" in engine.summary()

    def test_summary_champion_count_correct(self):
        engine = self._engine()
        s = engine.summary()
        assert s["champion_count"] == len(engine.champions())

    def test_summary_critical_count_key(self):
        engine = self._engine()
        assert "critical_count" in engine.summary()

    def test_summary_critical_count_correct(self):
        engine = self._engine()
        s = engine.summary()
        assert s["critical_count"] == len(engine.critical_accounts())

    def test_summary_total_arr_at_risk_key(self):
        engine = self._engine()
        assert "total_arr_at_risk_eur" in engine.summary()

    def test_summary_total_arr_at_risk_numeric(self):
        engine = self._engine()
        assert isinstance(engine.summary()["total_arr_at_risk_eur"], (int, float))

    def test_summary_empty_engine(self):
        engine = AccountHealthScorerEngine()
        s = engine.summary()
        assert s["total"] == 0
        assert s["avg_health_score"] == 0.0


# ===========================================================================
# 22. Engine.reset
# ===========================================================================

class TestEngineReset:
    def test_reset_clears_accounts(self):
        engine = AccountHealthScorerEngine()
        engine.score(make_account(account_id="a1"))
        engine.score(make_account(account_id="a2"))
        engine.reset()
        assert engine.all_accounts() == []

    def test_reset_clears_champions(self):
        engine = AccountHealthScorerEngine()
        engine.score(make_account(account_id="c1",
            dau_mau_ratio=1.0, feature_adoption_pct=100.0, integrations_active=10,
            nps_score=100, support_tickets_last_90d=0, critical_tickets_open=0,
            executive_sponsor_engaged=True, champion_score=10, stakeholders_active=10,
            last_qbr_days_ago=1, payment_on_time=True, invoices_overdue=0,
            contract_months_remaining=12, expansion_discussions=True,
        ))
        engine.reset()
        assert engine.champions() == []

    def test_reset_avg_score_returns_0(self):
        engine = AccountHealthScorerEngine()
        engine.score(make_account())
        engine.reset()
        assert engine.avg_health_score() == 0.0

    def test_reset_arr_at_risk_returns_0(self):
        engine = AccountHealthScorerEngine()
        engine.score(make_account())
        engine.reset()
        assert engine.total_arr_at_risk_eur() == 0.0

    def test_reset_allows_rescoring(self):
        engine = AccountHealthScorerEngine()
        engine.score(make_account())
        engine.reset()
        engine.score(make_account(account_id="b1"))
        assert len(engine.all_accounts()) == 1

    def test_reset_summary_total_0(self):
        engine = AccountHealthScorerEngine()
        engine.score(make_account())
        engine.reset()
        assert engine.summary()["total"] == 0

    def test_reset_idempotent(self):
        engine = AccountHealthScorerEngine()
        engine.reset()
        engine.reset()
        assert engine.all_accounts() == []

    def test_reset_needs_escalation_empty(self):
        engine = AccountHealthScorerEngine()
        engine.score(make_account())
        engine.reset()
        assert engine.needs_escalation() == []

    def test_reset_expansion_ready_empty(self):
        engine = AccountHealthScorerEngine()
        engine.score(make_account())
        engine.reset()
        assert engine.expansion_ready() == []

    def test_reset_at_risk_accounts_empty(self):
        engine = AccountHealthScorerEngine()
        engine.score(make_account())
        engine.reset()
        assert engine.at_risk_accounts() == []
