"""
Comprehensive tests for swarm/intelligence/churn_predictor.py
Run from /home/user/TEST:
    python -m pytest swarm/tests/test_churn_predictor.py -v
"""

from __future__ import annotations

import pytest

from swarm.intelligence.churn_predictor import (
    ChurnRisk,
    RetentionAction,
    ChurnInput,
    ChurnResult,
    ChurnPredictor,
    _usage_risk,
    _support_risk,
    _financial_risk,
    _relationship_risk,
    _competitive_risk,
    _churn_probability,
    _churn_risk,
    _retention_action,
    _build_signals,
    _DAYS_TO_ACT,
)


# ─── Fixtures / helpers ───────────────────────────────────────────────────────

def make_input(
    account_id: str = "acct_001",
    account_name: str = "Acme Corp",
    arr_eur: float = 100_000.0,
    contract_end_days: int = 180,
    monthly_active_users: int = 50,
    mau_trend_pct: float = 0.0,
    feature_adoption_pct: float = 60.0,
    login_frequency_days: float = 2.0,
    open_tickets: int = 0,
    overdue_tickets: int = 0,
    critical_bugs_open: int = 0,
    avg_ticket_resolution_days: float = 3.0,
    payment_delays: int = 0,
    invoice_disputes: int = 0,
    champion_lost: bool = False,
    executive_sponsor_engaged: bool = True,
    nps_score: int = 40,
    nps_trend: str = "stable",
    last_qbr_days: int = 30,
    competitor_mentioned: bool = False,
    rfp_received: bool = False,
) -> ChurnInput:
    return ChurnInput(
        account_id=account_id,
        account_name=account_name,
        arr_eur=arr_eur,
        contract_end_days=contract_end_days,
        monthly_active_users=monthly_active_users,
        mau_trend_pct=mau_trend_pct,
        feature_adoption_pct=feature_adoption_pct,
        login_frequency_days=login_frequency_days,
        open_tickets=open_tickets,
        overdue_tickets=overdue_tickets,
        critical_bugs_open=critical_bugs_open,
        avg_ticket_resolution_days=avg_ticket_resolution_days,
        payment_delays=payment_delays,
        invoice_disputes=invoice_disputes,
        champion_lost=champion_lost,
        executive_sponsor_engaged=executive_sponsor_engaged,
        nps_score=nps_score,
        nps_trend=nps_trend,
        last_qbr_days=last_qbr_days,
        competitor_mentioned=competitor_mentioned,
        rfp_received=rfp_received,
    )


def safe_input() -> ChurnInput:
    """A healthy account: good usage, no issues, happy customer."""
    return make_input(
        mau_trend_pct=15.0,
        feature_adoption_pct=80.0,
        login_frequency_days=1.0,
        nps_score=60,
        nps_trend="improving",
        executive_sponsor_engaged=True,
        last_qbr_days=20,
    )


def critical_input() -> ChurnInput:
    """An account in serious danger of churning."""
    return make_input(
        mau_trend_pct=-50.0,
        feature_adoption_pct=10.0,
        login_frequency_days=12.0,
        open_tickets=8,
        overdue_tickets=5,
        critical_bugs_open=3,
        avg_ticket_resolution_days=15.0,
        payment_delays=4,
        invoice_disputes=2,
        champion_lost=True,
        executive_sponsor_engaged=False,
        nps_score=-60,
        nps_trend="declining",
        last_qbr_days=120,
        competitor_mentioned=True,
        rfp_received=True,
    )


def predictor() -> ChurnPredictor:
    return ChurnPredictor()


# ─── 1. ChurnRisk enum ────────────────────────────────────────────────────────

class TestChurnRiskEnum:
    def test_critical_value(self):
        assert ChurnRisk.CRITICAL.value == "critical"

    def test_high_value(self):
        assert ChurnRisk.HIGH.value == "high"

    def test_medium_value(self):
        assert ChurnRisk.MEDIUM.value == "medium"

    def test_low_value(self):
        assert ChurnRisk.LOW.value == "low"

    def test_safe_value(self):
        assert ChurnRisk.SAFE.value == "safe"

    def test_all_members_count(self):
        assert len(ChurnRisk) == 5

    def test_is_str_enum(self):
        assert isinstance(ChurnRisk.HIGH, str)


# ─── 2. RetentionAction enum ──────────────────────────────────────────────────

class TestRetentionActionEnum:
    def test_emergency_value(self):
        assert RetentionAction.EMERGENCY.value == "emergency"

    def test_rescue_value(self):
        assert RetentionAction.RESCUE.value == "rescue"

    def test_proactive_value(self):
        assert RetentionAction.PROACTIVE.value == "proactive"

    def test_nurture_value(self):
        assert RetentionAction.NURTURE.value == "nurture"

    def test_expand_value(self):
        assert RetentionAction.EXPAND.value == "expand"

    def test_all_members_count(self):
        assert len(RetentionAction) == 5

    def test_is_str_enum(self):
        assert isinstance(RetentionAction.EXPAND, str)


# ─── 3. _usage_risk ───────────────────────────────────────────────────────────

class TestUsageRisk:
    def test_zero_when_no_risk(self):
        inp = make_input(mau_trend_pct=0.0, feature_adoption_pct=60.0, login_frequency_days=2.0)
        assert _usage_risk(inp) == 0.0

    def test_mau_negative_contributes(self):
        inp = make_input(mau_trend_pct=-10.0, feature_adoption_pct=60.0, login_frequency_days=2.0)
        # mau_score = min(80, 10 * 1.2) = 12.0
        # adoption_risk = 0.0 (pct >= 50)
        # login_risk = 0.0 (days <= 3)
        # result = 12.0 * 0.50 = 6.0
        assert _usage_risk(inp) == pytest.approx(6.0, abs=0.01)

    def test_mau_positive_no_risk(self):
        inp = make_input(mau_trend_pct=20.0, feature_adoption_pct=60.0, login_frequency_days=2.0)
        assert _usage_risk(inp) == 0.0

    def test_mau_capped_at_80(self):
        # -100 * 1.2 = 120, capped at 80
        inp = make_input(mau_trend_pct=-100.0, feature_adoption_pct=60.0, login_frequency_days=2.0)
        expected = round(min(100, 80 * 0.50), 2)
        assert _usage_risk(inp) == pytest.approx(expected, abs=0.01)

    def test_low_adoption_contributes(self):
        inp = make_input(mau_trend_pct=0.0, feature_adoption_pct=30.0, login_frequency_days=2.0)
        # adoption_risk = min(40, (50 - 30) * 0.8) = min(40, 16) = 16.0
        # result = 16.0 * 0.30 = 4.8
        assert _usage_risk(inp) == pytest.approx(4.8, abs=0.01)

    def test_adoption_50_no_risk(self):
        inp = make_input(mau_trend_pct=0.0, feature_adoption_pct=50.0, login_frequency_days=2.0)
        assert _usage_risk(inp) == 0.0

    def test_adoption_capped_at_40(self):
        inp = make_input(mau_trend_pct=0.0, feature_adoption_pct=0.0, login_frequency_days=2.0)
        # adoption_risk = min(40, 50 * 0.8) = min(40, 40) = 40.0
        assert _usage_risk(inp) == pytest.approx(40 * 0.30, abs=0.01)

    def test_login_frequency_above_3_contributes(self):
        inp = make_input(mau_trend_pct=0.0, feature_adoption_pct=60.0, login_frequency_days=5.0)
        # login_risk = min(40, (5 - 3) * 5) = min(40, 10) = 10.0
        # result = 10.0 * 0.20 = 2.0
        assert _usage_risk(inp) == pytest.approx(2.0, abs=0.01)

    def test_login_frequency_3_no_risk(self):
        inp = make_input(mau_trend_pct=0.0, feature_adoption_pct=60.0, login_frequency_days=3.0)
        assert _usage_risk(inp) == 0.0

    def test_login_risk_capped_at_40(self):
        inp = make_input(mau_trend_pct=0.0, feature_adoption_pct=60.0, login_frequency_days=100.0)
        # login_risk = min(40, ...) = 40 → * 0.20 = 8.0
        assert _usage_risk(inp) == pytest.approx(8.0, abs=0.01)

    def test_combined_risk_capped_at_100(self):
        inp = make_input(mau_trend_pct=-100.0, feature_adoption_pct=0.0, login_frequency_days=100.0)
        assert _usage_risk(inp) <= 100.0

    def test_combined_all_risks(self):
        inp = make_input(mau_trend_pct=-20.0, feature_adoption_pct=20.0, login_frequency_days=7.0)
        # mau_score = min(80, 20 * 1.2) = 24.0
        # adoption_risk = min(40, (50-20)*0.8) = min(40, 24) = 24.0
        # login_risk = min(40, (7-3)*5) = min(40, 20) = 20.0
        # result = 24*0.50 + 24*0.30 + 20*0.20 = 12 + 7.2 + 4 = 23.2
        assert _usage_risk(inp) == pytest.approx(23.2, abs=0.01)

    def test_result_is_float(self):
        inp = make_input()
        assert isinstance(_usage_risk(inp), float)

    def test_never_negative(self):
        inp = make_input(mau_trend_pct=50.0, feature_adoption_pct=100.0, login_frequency_days=0.0)
        assert _usage_risk(inp) >= 0.0


# ─── 4. _support_risk ────────────────────────────────────────────────────────

class TestSupportRisk:
    def test_zero_when_clean(self):
        inp = make_input(open_tickets=0, overdue_tickets=0, critical_bugs_open=0, avg_ticket_resolution_days=3.0)
        assert _support_risk(inp) == 0.0

    def test_open_tickets_score(self):
        inp = make_input(open_tickets=3, overdue_tickets=0, critical_bugs_open=0, avg_ticket_resolution_days=3.0)
        # ticket_score = min(25, 3 * 5) = 15
        assert _support_risk(inp) == pytest.approx(15.0, abs=0.01)

    def test_open_tickets_capped_at_25(self):
        inp = make_input(open_tickets=10, overdue_tickets=0, critical_bugs_open=0, avg_ticket_resolution_days=3.0)
        # ticket_score = min(25, 10 * 5) = 25
        assert _support_risk(inp) == pytest.approx(25.0, abs=0.01)

    def test_overdue_tickets_score(self):
        inp = make_input(open_tickets=0, overdue_tickets=2, critical_bugs_open=0, avg_ticket_resolution_days=3.0)
        # overdue_score = min(30, 2 * 10) = 20
        assert _support_risk(inp) == pytest.approx(20.0, abs=0.01)

    def test_overdue_tickets_capped_at_30(self):
        inp = make_input(open_tickets=0, overdue_tickets=5, critical_bugs_open=0, avg_ticket_resolution_days=3.0)
        assert _support_risk(inp) == pytest.approx(30.0, abs=0.01)

    def test_critical_bugs_score(self):
        inp = make_input(open_tickets=0, overdue_tickets=0, critical_bugs_open=2, avg_ticket_resolution_days=3.0)
        # bug_score = min(40, 2 * 15) = 30
        assert _support_risk(inp) == pytest.approx(30.0, abs=0.01)

    def test_critical_bugs_capped_at_40(self):
        inp = make_input(open_tickets=0, overdue_tickets=0, critical_bugs_open=5, avg_ticket_resolution_days=3.0)
        assert _support_risk(inp) == pytest.approx(40.0, abs=0.01)

    def test_resolution_penalty_above_5_days(self):
        inp = make_input(open_tickets=0, overdue_tickets=0, critical_bugs_open=0, avg_ticket_resolution_days=8.0)
        # penalty = min(20, (8 - 5) * 3) = min(20, 9) = 9
        assert _support_risk(inp) == pytest.approx(9.0, abs=0.01)

    def test_resolution_exactly_5_no_penalty(self):
        inp = make_input(open_tickets=0, overdue_tickets=0, critical_bugs_open=0, avg_ticket_resolution_days=5.0)
        assert _support_risk(inp) == 0.0

    def test_resolution_penalty_capped_at_20(self):
        inp = make_input(open_tickets=0, overdue_tickets=0, critical_bugs_open=0, avg_ticket_resolution_days=100.0)
        assert _support_risk(inp) == pytest.approx(20.0, abs=0.01)

    def test_combined_capped_at_100(self):
        inp = make_input(open_tickets=20, overdue_tickets=10, critical_bugs_open=10, avg_ticket_resolution_days=100.0)
        assert _support_risk(inp) <= 100.0

    def test_combined_sum(self):
        inp = make_input(open_tickets=2, overdue_tickets=1, critical_bugs_open=1, avg_ticket_resolution_days=7.0)
        # ticket = 10, overdue = 10, bug = 15, penalty = min(20, 6) = 6
        assert _support_risk(inp) == pytest.approx(41.0, abs=0.01)

    def test_result_is_float(self):
        assert isinstance(_support_risk(make_input()), (int, float))


# ─── 5. _financial_risk ──────────────────────────────────────────────────────

class TestFinancialRisk:
    def test_zero_when_clean(self):
        inp = make_input(payment_delays=0, invoice_disputes=0)
        assert _financial_risk(inp) == 0.0

    def test_payment_delays_score(self):
        inp = make_input(payment_delays=2, invoice_disputes=0)
        # delay_score = min(60, 2 * 15) = 30
        assert _financial_risk(inp) == pytest.approx(30.0, abs=0.01)

    def test_payment_delays_capped_at_60(self):
        inp = make_input(payment_delays=10, invoice_disputes=0)
        assert _financial_risk(inp) == pytest.approx(60.0, abs=0.01)

    def test_invoice_disputes_score(self):
        inp = make_input(payment_delays=0, invoice_disputes=1)
        # dispute_score = min(40, 1 * 20) = 20
        assert _financial_risk(inp) == pytest.approx(20.0, abs=0.01)

    def test_invoice_disputes_capped_at_40(self):
        inp = make_input(payment_delays=0, invoice_disputes=5)
        assert _financial_risk(inp) == pytest.approx(40.0, abs=0.01)

    def test_combined_capped_at_100(self):
        inp = make_input(payment_delays=10, invoice_disputes=10)
        assert _financial_risk(inp) == 100.0

    def test_combined_sum(self):
        inp = make_input(payment_delays=1, invoice_disputes=1)
        # 15 + 20 = 35
        assert _financial_risk(inp) == pytest.approx(35.0, abs=0.01)

    def test_result_is_float(self):
        assert isinstance(_financial_risk(make_input()), (int, float))


# ─── 6. _relationship_risk ───────────────────────────────────────────────────

class TestRelationshipRisk:
    def test_zero_when_healthy(self):
        inp = make_input(
            champion_lost=False,
            executive_sponsor_engaged=False,
            nps_score=40,
            nps_trend="stable",
            last_qbr_days=30,
        )
        assert _relationship_risk(inp) == 0.0

    def test_champion_lost_adds_40(self):
        inp = make_input(
            champion_lost=True,
            executive_sponsor_engaged=False,
            nps_score=40,
            nps_trend="stable",
            last_qbr_days=30,
        )
        assert _relationship_risk(inp) == pytest.approx(40.0, abs=0.01)

    def test_executive_sponsor_subtracts_15(self):
        inp = make_input(
            champion_lost=False,
            executive_sponsor_engaged=True,
            nps_score=40,
            nps_trend="stable",
            last_qbr_days=30,
        )
        # max(0, -15) = 0
        assert _relationship_risk(inp) == 0.0

    def test_executive_sponsor_reduces_champion_lost(self):
        inp = make_input(
            champion_lost=True,
            executive_sponsor_engaged=True,
            nps_score=40,
            nps_trend="stable",
            last_qbr_days=30,
        )
        # 40 - 15 = 25
        assert _relationship_risk(inp) == pytest.approx(25.0, abs=0.01)

    def test_nps_very_negative_adds_30(self):
        inp = make_input(
            champion_lost=False,
            executive_sponsor_engaged=False,
            nps_score=-50,
            nps_trend="stable",
            last_qbr_days=30,
        )
        assert _relationship_risk(inp) == pytest.approx(30.0, abs=0.01)

    def test_nps_negative_adds_15(self):
        inp = make_input(
            champion_lost=False,
            executive_sponsor_engaged=False,
            nps_score=-10,
            nps_trend="stable",
            last_qbr_days=30,
        )
        assert _relationship_risk(inp) == pytest.approx(15.0, abs=0.01)

    def test_nps_boundary_minus_30(self):
        # -30 is not < -30, so it should add +15 (< 0 branch)
        inp = make_input(
            champion_lost=False,
            executive_sponsor_engaged=False,
            nps_score=-30,
            nps_trend="stable",
            last_qbr_days=30,
        )
        assert _relationship_risk(inp) == pytest.approx(15.0, abs=0.01)

    def test_nps_minus_31_adds_30(self):
        inp = make_input(
            champion_lost=False,
            executive_sponsor_engaged=False,
            nps_score=-31,
            nps_trend="stable",
            last_qbr_days=30,
        )
        assert _relationship_risk(inp) == pytest.approx(30.0, abs=0.01)

    def test_nps_above_50_subtracts_10(self):
        inp = make_input(
            champion_lost=False,
            executive_sponsor_engaged=False,
            nps_score=60,
            nps_trend="stable",
            last_qbr_days=30,
        )
        # max(0, -10) = 0
        assert _relationship_risk(inp) == 0.0

    def test_nps_trend_declining_adds_15(self):
        inp = make_input(
            champion_lost=False,
            executive_sponsor_engaged=False,
            nps_score=40,
            nps_trend="declining",
            last_qbr_days=30,
        )
        assert _relationship_risk(inp) == pytest.approx(15.0, abs=0.01)

    def test_nps_trend_improving_subtracts_10(self):
        inp = make_input(
            champion_lost=True,
            executive_sponsor_engaged=False,
            nps_score=40,
            nps_trend="improving",
            last_qbr_days=30,
        )
        # 40 - 10 = 30
        assert _relationship_risk(inp) == pytest.approx(30.0, abs=0.01)

    def test_last_qbr_above_90_adds_20(self):
        inp = make_input(
            champion_lost=False,
            executive_sponsor_engaged=False,
            nps_score=40,
            nps_trend="stable",
            last_qbr_days=100,
        )
        assert _relationship_risk(inp) == pytest.approx(20.0, abs=0.01)

    def test_last_qbr_above_60_adds_10(self):
        inp = make_input(
            champion_lost=False,
            executive_sponsor_engaged=False,
            nps_score=40,
            nps_trend="stable",
            last_qbr_days=70,
        )
        assert _relationship_risk(inp) == pytest.approx(10.0, abs=0.01)

    def test_last_qbr_exactly_90_adds_10_not_20(self):
        # 90 is not > 90, so it hits the elif > 60 branch
        inp = make_input(
            champion_lost=False,
            executive_sponsor_engaged=False,
            nps_score=40,
            nps_trend="stable",
            last_qbr_days=90,
        )
        assert _relationship_risk(inp) == pytest.approx(10.0, abs=0.01)

    def test_result_capped_at_100(self):
        inp = make_input(
            champion_lost=True,
            executive_sponsor_engaged=False,
            nps_score=-100,
            nps_trend="declining",
            last_qbr_days=200,
        )
        assert _relationship_risk(inp) <= 100.0

    def test_result_floor_at_0(self):
        inp = make_input(
            champion_lost=False,
            executive_sponsor_engaged=True,
            nps_score=100,
            nps_trend="improving",
            last_qbr_days=10,
        )
        assert _relationship_risk(inp) >= 0.0

    def test_nps_trend_case_insensitive(self):
        inp_lower = make_input(nps_trend="declining", champion_lost=False, executive_sponsor_engaged=False, nps_score=40, last_qbr_days=30)
        inp_upper = make_input(nps_trend="DECLINING", champion_lost=False, executive_sponsor_engaged=False, nps_score=40, last_qbr_days=30)
        assert _relationship_risk(inp_lower) == _relationship_risk(inp_upper)


# ─── 7. _competitive_risk ────────────────────────────────────────────────────

class TestCompetitiveRisk:
    def test_zero_when_no_signals(self):
        inp = make_input(competitor_mentioned=False, rfp_received=False)
        assert _competitive_risk(inp) == 0.0

    def test_competitor_mentioned_adds_35(self):
        inp = make_input(competitor_mentioned=True, rfp_received=False)
        assert _competitive_risk(inp) == pytest.approx(35.0, abs=0.01)

    def test_rfp_received_adds_50(self):
        inp = make_input(competitor_mentioned=False, rfp_received=True)
        assert _competitive_risk(inp) == pytest.approx(50.0, abs=0.01)

    def test_both_signals_combined(self):
        inp = make_input(competitor_mentioned=True, rfp_received=True)
        # 35 + 50 = 85, capped at 100
        assert _competitive_risk(inp) == pytest.approx(85.0, abs=0.01)

    def test_result_capped_at_100(self):
        # Even extreme cases stay at 100
        inp = make_input(competitor_mentioned=True, rfp_received=True)
        assert _competitive_risk(inp) <= 100.0

    def test_result_is_float(self):
        assert isinstance(_competitive_risk(make_input()), float)


# ─── 8. _churn_probability ───────────────────────────────────────────────────

class TestChurnProbability:
    def test_zero_components_gives_zero(self):
        result = _churn_probability(0, 0, 0, 0, 0, make_input(contract_end_days=180))
        assert result == 0.0

    def test_weighted_sum(self):
        # usage=20, support=10, financial=10, relationship=40, competitive=20
        # base = 20*0.25 + 10*0.15 + 10*0.15 + 40*0.30 + 20*0.15 = 5 + 1.5 + 1.5 + 12 + 3 = 23
        inp = make_input(contract_end_days=180)
        result = _churn_probability(20, 10, 10, 40, 20, inp)
        assert result == pytest.approx(23.0, abs=0.01)

    def test_contract_urgency_bonus_both_conditions(self):
        # base >= 35 AND contract_end_days <= 60 → +8 bonus
        # contract_end_days <= 30 → +5 bonus
        inp = make_input(contract_end_days=25)
        # base = 40, bonus = 8 + 5 = 13
        result = _churn_probability(40, 40, 40, 40, 40, inp)
        # base = 40*0.25 + 40*0.15 + 40*0.15 + 40*0.30 + 40*0.15 = 40
        assert result == pytest.approx(min(95, 40 + 13), abs=0.01)

    def test_contract_urgency_bonus_60_day_only(self):
        # contract_end_days = 50 (<=60), base = 40 (>=35) → +8
        # but NOT <=30, so no extra +5
        inp = make_input(contract_end_days=50)
        result = _churn_probability(40, 40, 40, 40, 40, inp)
        assert result == pytest.approx(min(95, 40 + 8), abs=0.01)

    def test_no_bonus_when_base_below_35_but_contract_above_60(self):
        # contract_end_days > 60 → no bonus from either condition
        inp = make_input(contract_end_days=90)
        result = _churn_probability(10, 10, 10, 10, 10, inp)
        base = 10 * 0.25 + 10 * 0.15 + 10 * 0.15 + 10 * 0.30 + 10 * 0.15
        assert result == pytest.approx(base, abs=0.01)

    def test_contract_le_30_adds_5_regardless_of_base(self):
        # contract_end_days <= 30 always adds +5, even if base < 35
        inp = make_input(contract_end_days=20)
        result = _churn_probability(10, 10, 10, 10, 10, inp)
        base = 10 * 0.25 + 10 * 0.15 + 10 * 0.15 + 10 * 0.30 + 10 * 0.15
        # Only the <= 30 bonus of +5 applies (base < 35 so no +8)
        assert result == pytest.approx(base + 5, abs=0.01)

    def test_capped_at_95(self):
        inp = make_input(contract_end_days=10)
        result = _churn_probability(100, 100, 100, 100, 100, inp)
        assert result == 95.0

    def test_minimum_is_0(self):
        inp = make_input(contract_end_days=180)
        result = _churn_probability(0, 0, 0, 0, 0, inp)
        assert result >= 0.0

    def test_result_is_float(self):
        inp = make_input()
        result = _churn_probability(10, 10, 10, 10, 10, inp)
        assert isinstance(result, float)

    def test_contract_end_61_no_bonus(self):
        # exactly 61 days — not <= 60, so no bonus
        inp = make_input(contract_end_days=61)
        base_result = _churn_probability(40, 40, 40, 40, 40, inp)
        assert base_result == pytest.approx(40.0, abs=0.01)

    def test_contract_end_60_with_bonus(self):
        inp = make_input(contract_end_days=60)
        result = _churn_probability(40, 40, 40, 40, 40, inp)
        assert result == pytest.approx(48.0, abs=0.01)  # 40 + 8


# ─── 9. _churn_risk ──────────────────────────────────────────────────────────

class TestChurnRiskThresholds:
    def test_critical_at_80(self):
        assert _churn_risk(80.0) == ChurnRisk.CRITICAL

    def test_critical_above_80(self):
        assert _churn_risk(90.0) == ChurnRisk.CRITICAL

    def test_high_at_60(self):
        assert _churn_risk(60.0) == ChurnRisk.HIGH

    def test_high_below_80(self):
        assert _churn_risk(79.9) == ChurnRisk.HIGH

    def test_medium_at_40(self):
        assert _churn_risk(40.0) == ChurnRisk.MEDIUM

    def test_medium_below_60(self):
        assert _churn_risk(59.9) == ChurnRisk.MEDIUM

    def test_low_at_20(self):
        assert _churn_risk(20.0) == ChurnRisk.LOW

    def test_low_below_40(self):
        assert _churn_risk(39.9) == ChurnRisk.LOW

    def test_safe_below_20(self):
        assert _churn_risk(19.9) == ChurnRisk.SAFE

    def test_safe_at_0(self):
        assert _churn_risk(0.0) == ChurnRisk.SAFE


# ─── 10. _DAYS_TO_ACT ────────────────────────────────────────────────────────

class TestDaysToAct:
    def test_critical_is_3(self):
        assert _DAYS_TO_ACT[ChurnRisk.CRITICAL] == 3

    def test_high_is_7(self):
        assert _DAYS_TO_ACT[ChurnRisk.HIGH] == 7

    def test_medium_is_14(self):
        assert _DAYS_TO_ACT[ChurnRisk.MEDIUM] == 14

    def test_low_is_30(self):
        assert _DAYS_TO_ACT[ChurnRisk.LOW] == 30

    def test_safe_is_90(self):
        assert _DAYS_TO_ACT[ChurnRisk.SAFE] == 90

    def test_all_five_risks_present(self):
        assert len(_DAYS_TO_ACT) == 5


# ─── 11. _retention_action ───────────────────────────────────────────────────

class TestRetentionAction:
    def test_critical_risk_returns_emergency(self):
        inp = make_input(champion_lost=False, rfp_received=False)
        assert _retention_action(inp, ChurnRisk.CRITICAL) == RetentionAction.EMERGENCY

    def test_high_with_champion_lost_returns_emergency(self):
        inp = make_input(champion_lost=True, rfp_received=False)
        assert _retention_action(inp, ChurnRisk.HIGH) == RetentionAction.EMERGENCY

    def test_high_with_rfp_returns_emergency(self):
        inp = make_input(champion_lost=False, rfp_received=True)
        assert _retention_action(inp, ChurnRisk.HIGH) == RetentionAction.EMERGENCY

    def test_high_with_both_returns_emergency(self):
        inp = make_input(champion_lost=True, rfp_received=True)
        assert _retention_action(inp, ChurnRisk.HIGH) == RetentionAction.EMERGENCY

    def test_high_no_triggers_returns_rescue(self):
        inp = make_input(champion_lost=False, rfp_received=False)
        assert _retention_action(inp, ChurnRisk.HIGH) == RetentionAction.RESCUE

    def test_medium_returns_proactive(self):
        inp = make_input(champion_lost=False, rfp_received=False)
        assert _retention_action(inp, ChurnRisk.MEDIUM) == RetentionAction.PROACTIVE

    def test_low_returns_nurture(self):
        inp = make_input(champion_lost=False, rfp_received=False)
        assert _retention_action(inp, ChurnRisk.LOW) == RetentionAction.NURTURE

    def test_safe_positive_mau_and_good_nps_returns_expand(self):
        inp = make_input(mau_trend_pct=5.0, nps_score=50)
        assert _retention_action(inp, ChurnRisk.SAFE) == RetentionAction.EXPAND

    def test_safe_zero_mau_and_good_nps_returns_expand(self):
        inp = make_input(mau_trend_pct=0.0, nps_score=50)
        assert _retention_action(inp, ChurnRisk.SAFE) == RetentionAction.EXPAND

    def test_safe_negative_mau_returns_nurture(self):
        inp = make_input(mau_trend_pct=-5.0, nps_score=50)
        assert _retention_action(inp, ChurnRisk.SAFE) == RetentionAction.NURTURE

    def test_safe_low_nps_returns_nurture(self):
        inp = make_input(mau_trend_pct=10.0, nps_score=25)
        assert _retention_action(inp, ChurnRisk.SAFE) == RetentionAction.NURTURE

    def test_safe_nps_exactly_30_returns_nurture(self):
        # nps_score > 30 required for EXPAND; exactly 30 → NURTURE
        inp = make_input(mau_trend_pct=10.0, nps_score=30)
        assert _retention_action(inp, ChurnRisk.SAFE) == RetentionAction.NURTURE

    def test_safe_nps_31_returns_expand(self):
        inp = make_input(mau_trend_pct=10.0, nps_score=31)
        assert _retention_action(inp, ChurnRisk.SAFE) == RetentionAction.EXPAND


# ─── 12. _build_signals ──────────────────────────────────────────────────────

class TestBuildSignals:
    def _call(self, inp: ChurnInput, prob: float = 50.0, risk: ChurnRisk = ChurnRisk.MEDIUM, arr_at_risk: float = 50000.0):
        return _build_signals(inp, prob, risk, arr_at_risk)

    # --- churn drivers ---

    def test_mau_decline_heavy_driver(self):
        inp = make_input(mau_trend_pct=-25.0)
        drivers, _, _, _ = self._call(inp)
        assert any("Usage en déclin" in d for d in drivers)

    def test_mau_decline_slight_driver(self):
        inp = make_input(mau_trend_pct=-10.0)
        drivers, _, _, _ = self._call(inp)
        assert any("Légère baisse" in d for d in drivers)

    def test_mau_decline_exactly_minus20_is_heavy(self):
        inp = make_input(mau_trend_pct=-20.0)
        drivers, _, _, _ = self._call(inp)
        assert any("Usage en déclin" in d for d in drivers)
        assert not any("Légère baisse" in d for d in drivers)

    def test_mau_positive_no_driver(self):
        inp = make_input(mau_trend_pct=5.0)
        drivers, _, _, _ = self._call(inp)
        assert not any("Usage" in d and "déclin" in d for d in drivers)

    def test_rare_login_driver(self):
        inp = make_input(login_frequency_days=10.0)
        drivers, _, _, _ = self._call(inp)
        assert any("Connexions rares" in d for d in drivers)

    def test_login_exactly_7_no_driver(self):
        inp = make_input(login_frequency_days=7.0)
        drivers, _, _, _ = self._call(inp)
        assert not any("Connexions rares" in d for d in drivers)

    def test_low_adoption_driver(self):
        inp = make_input(feature_adoption_pct=20.0)
        drivers, _, _, _ = self._call(inp)
        assert any("Adoption très faible" in d for d in drivers)

    def test_adoption_30_triggers_driver(self):
        # < 30 triggers driver
        inp = make_input(feature_adoption_pct=29.0)
        drivers, _, _, _ = self._call(inp)
        assert any("Adoption très faible" in d for d in drivers)

    def test_adoption_exactly_30_no_driver(self):
        inp = make_input(feature_adoption_pct=30.0)
        drivers, _, _, _ = self._call(inp)
        assert not any("Adoption très faible" in d for d in drivers)

    def test_overdue_tickets_driver(self):
        inp = make_input(overdue_tickets=2)
        drivers, _, _, _ = self._call(inp)
        assert any("ticket(s) en retard" in d for d in drivers)

    def test_critical_bugs_driver(self):
        inp = make_input(critical_bugs_open=1)
        drivers, _, _, _ = self._call(inp)
        assert any("bug(s) critique(s)" in d for d in drivers)

    def test_payment_delays_driver(self):
        inp = make_input(payment_delays=2)
        drivers, _, _, _ = self._call(inp)
        assert any("retard(s) de paiement" in d for d in drivers)

    def test_champion_lost_driver(self):
        inp = make_input(champion_lost=True)
        drivers, _, _, _ = self._call(inp)
        assert any("Champion perdu" in d for d in drivers)

    def test_nps_very_negative_driver(self):
        inp = make_input(nps_score=-50)
        drivers, _, _, _ = self._call(inp)
        assert any("NPS très négatif" in d for d in drivers)

    def test_nps_negative_driver(self):
        inp = make_input(nps_score=-10)
        drivers, _, _, _ = self._call(inp)
        assert any("NPS négatif" in d for d in drivers)

    def test_nps_declining_driver(self):
        inp = make_input(nps_trend="declining")
        drivers, _, _, _ = self._call(inp)
        assert any("NPS en déclin" in d for d in drivers)

    def test_competitor_mentioned_driver(self):
        inp = make_input(competitor_mentioned=True)
        drivers, _, _, _ = self._call(inp)
        assert any("Concurrent mentionné" in d for d in drivers)

    def test_rfp_received_driver(self):
        inp = make_input(rfp_received=True)
        drivers, _, _, _ = self._call(inp)
        assert any("RFP reçu" in d for d in drivers)

    def test_contract_end_60_days_driver(self):
        inp = make_input(contract_end_days=45)
        drivers, _, _, _ = self._call(inp)
        assert any("Renouvellement dans" in d for d in drivers)

    def test_contract_end_61_days_no_driver(self):
        inp = make_input(contract_end_days=61)
        drivers, _, _, _ = self._call(inp)
        assert not any("Renouvellement dans" in d for d in drivers)

    # --- retention signals ---

    def test_mau_growing_signal(self):
        inp = make_input(mau_trend_pct=15.0)
        _, signals, _, _ = self._call(inp)
        assert any("Usage en hausse" in s for s in signals)

    def test_mau_exactly_10_signal(self):
        inp = make_input(mau_trend_pct=10.0)
        _, signals, _, _ = self._call(inp)
        assert any("Usage en hausse" in s for s in signals)

    def test_mau_9_no_signal(self):
        inp = make_input(mau_trend_pct=9.0)
        _, signals, _, _ = self._call(inp)
        assert not any("Usage en hausse" in s for s in signals)

    def test_high_adoption_signal(self):
        inp = make_input(feature_adoption_pct=75.0)
        _, signals, _, _ = self._call(inp)
        assert any("Forte adoption" in s for s in signals)

    def test_executive_sponsor_signal(self):
        inp = make_input(executive_sponsor_engaged=True)
        _, signals, _, _ = self._call(inp)
        assert any("Sponsor exécutif" in s for s in signals)

    def test_good_nps_signal(self):
        inp = make_input(nps_score=50)
        _, signals, _, _ = self._call(inp)
        assert any("NPS positif" in s for s in signals)

    def test_nps_improving_signal(self):
        inp = make_input(nps_trend="improving")
        _, signals, _, _ = self._call(inp)
        assert any("NPS en amélioration" in s for s in signals)

    def test_no_open_tickets_signal(self):
        inp = make_input(open_tickets=0)
        _, signals, _, _ = self._call(inp)
        assert any("Aucun ticket ouvert" in s for s in signals)

    def test_perfect_payment_signal(self):
        inp = make_input(payment_delays=0, invoice_disputes=0)
        _, signals, _, _ = self._call(inp)
        assert any("paiement parfait" in s for s in signals)

    def test_payment_delay_suppresses_payment_signal(self):
        inp = make_input(payment_delays=1, invoice_disputes=0)
        _, signals, _, _ = self._call(inp)
        assert not any("paiement parfait" in s for s in signals)

    # --- risk flags ---

    def test_critical_prob_flag(self):
        inp = make_input()
        _, _, flags, _ = self._call(inp, prob=85.0, arr_at_risk=50000.0)
        assert any("CRITIQUE" in f for f in flags)

    def test_below_80_no_critical_flag(self):
        inp = make_input()
        _, _, flags, _ = self._call(inp, prob=79.0)
        assert not any("CRITIQUE — perte imminente" in f for f in flags)

    def test_double_threat_flag(self):
        inp = make_input(champion_lost=True, rfp_received=True)
        _, _, flags, _ = self._call(inp)
        assert any("Double menace" in f for f in flags)

    def test_no_double_threat_without_both(self):
        inp = make_input(champion_lost=True, rfp_received=False)
        _, _, flags, _ = self._call(inp)
        assert not any("Double menace" in f for f in flags)

    def test_payment_delay_repeated_flag(self):
        inp = make_input(payment_delays=3)
        _, _, flags, _ = self._call(inp)
        assert any("Retards de paiement répétés" in f for f in flags)

    def test_payment_delay_2_no_flag(self):
        inp = make_input(payment_delays=2)
        _, _, flags, _ = self._call(inp)
        assert not any("Retards de paiement répétés" in f for f in flags)

    def test_contract_critical_flag(self):
        inp = make_input(contract_end_days=15)
        _, _, flags, _ = self._call(inp)
        assert any("Renouvellement CRITIQUE" in f for f in flags)

    def test_contract_31_days_no_critical_flag(self):
        inp = make_input(contract_end_days=31)
        _, _, flags, _ = self._call(inp)
        assert not any("Renouvellement CRITIQUE" in f for f in flags)

    def test_2_critical_bugs_flag(self):
        inp = make_input(critical_bugs_open=2)
        _, _, flags, _ = self._call(inp)
        assert any("bugs critiques bloquants" in f for f in flags)

    def test_1_critical_bug_no_flag(self):
        inp = make_input(critical_bugs_open=1)
        _, _, flags, _ = self._call(inp)
        assert not any("bugs critiques bloquants" in f for f in flags)

    # --- recommended actions ---

    def test_champion_lost_action(self):
        inp = make_input(champion_lost=True)
        _, _, _, actions = self._call(inp)
        assert any("champion interne" in a for a in actions)

    def test_rfp_received_action(self):
        inp = make_input(rfp_received=True)
        _, _, _, actions = self._call(inp)
        assert any("call exécutif d'urgence" in a for a in actions)

    def test_critical_bugs_action(self):
        inp = make_input(critical_bugs_open=2)
        _, _, _, actions = self._call(inp)
        assert any("Escalader" in a for a in actions)

    def test_mau_decline_severe_action(self):
        inp = make_input(mau_trend_pct=-25.0)
        _, _, _, actions = self._call(inp)
        assert any("Success Call" in a for a in actions)

    def test_mau_slight_decline_no_success_call(self):
        inp = make_input(mau_trend_pct=-10.0)
        _, _, _, actions = self._call(inp)
        assert not any("Success Call" in a for a in actions)

    def test_low_adoption_action(self):
        inp = make_input(feature_adoption_pct=20.0)
        _, _, _, actions = self._call(inp)
        assert any("formation" in a for a in actions)

    def test_contract_end_90_days_action(self):
        inp = make_input(contract_end_days=80)
        _, _, _, actions = self._call(inp)
        assert any("renouvellement anticipé" in a for a in actions)

    def test_contract_end_91_days_no_renewal_action(self):
        inp = make_input(contract_end_days=91)
        _, _, _, actions = self._call(inp)
        assert not any("renouvellement anticipé" in a for a in actions)

    def test_negative_nps_action(self):
        inp = make_input(nps_score=-5)
        _, _, _, actions = self._call(inp)
        assert any("NPS Detractor" in a for a in actions)

    def test_positive_nps_no_detractor_action(self):
        inp = make_input(nps_score=10)
        _, _, _, actions = self._call(inp)
        assert not any("NPS Detractor" in a for a in actions)

    def test_payment_delays_action(self):
        inp = make_input(payment_delays=1)
        _, _, _, actions = self._call(inp)
        assert any("Finance" in a for a in actions)

    def test_old_qbr_action(self):
        inp = make_input(last_qbr_days=95)
        _, _, _, actions = self._call(inp)
        assert any("QBR immédiatement" in a for a in actions)

    def test_recent_qbr_no_action(self):
        inp = make_input(last_qbr_days=30)
        _, _, _, actions = self._call(inp)
        assert not any("QBR immédiatement" in a for a in actions)

    def test_no_exec_sponsor_action(self):
        inp = make_input(executive_sponsor_engaged=False)
        _, _, _, actions = self._call(inp)
        assert any("sponsor exécutif" in a for a in actions)

    def test_exec_sponsor_engaged_no_action(self):
        inp = make_input(executive_sponsor_engaged=True)
        _, _, _, actions = self._call(inp)
        assert not any("sponsor exécutif" in a for a in actions)


# ─── 13. ChurnPredictor.predict ──────────────────────────────────────────────

class TestChurnPredictorPredict:
    def test_returns_churn_result(self):
        p = predictor()
        result = p.predict(safe_input())
        assert isinstance(result, ChurnResult)

    def test_account_id_preserved(self):
        p = predictor()
        inp = make_input(account_id="test_123")
        result = p.predict(inp)
        assert result.account_id == "test_123"

    def test_account_name_preserved(self):
        p = predictor()
        inp = make_input(account_name="Test Company")
        result = p.predict(inp)
        assert result.account_name == "Test Company"

    def test_arr_eur_preserved(self):
        p = predictor()
        inp = make_input(arr_eur=250_000.0)
        result = p.predict(inp)
        assert result.arr_eur == 250_000.0

    def test_churn_probability_in_range(self):
        p = predictor()
        result = p.predict(critical_input())
        assert 0.0 <= result.churn_probability_pct <= 95.0

    def test_churn_risk_is_enum(self):
        p = predictor()
        result = p.predict(safe_input())
        assert isinstance(result.churn_risk, ChurnRisk)

    def test_retention_action_is_enum(self):
        p = predictor()
        result = p.predict(safe_input())
        assert isinstance(result.retention_action, RetentionAction)

    def test_arr_at_risk_calculated(self):
        p = predictor()
        inp = make_input(arr_eur=100_000.0)
        result = p.predict(inp)
        expected = round(100_000.0 * result.churn_probability_pct / 100, 2)
        assert result.arr_at_risk_eur == pytest.approx(expected, abs=0.01)

    def test_days_to_act_respects_contract_end(self):
        p = predictor()
        # LOW risk (days_to_act base = 30), contract_end_days = 10 → should be 10
        inp = make_input(
            mau_trend_pct=5.0,
            feature_adoption_pct=70.0,
            login_frequency_days=2.0,
            nps_score=40,
            contract_end_days=10,
        )
        result = p.predict(inp)
        assert result.days_to_act <= 10

    def test_days_to_act_zero_contract_uses_base(self):
        p = predictor()
        inp = make_input(contract_end_days=0)
        result = p.predict(inp)
        assert result.days_to_act == _DAYS_TO_ACT[result.churn_risk]

    def test_component_scores_in_range(self):
        p = predictor()
        result = p.predict(critical_input())
        assert 0.0 <= result.usage_risk_score <= 100.0
        assert 0.0 <= result.support_risk_score <= 100.0
        assert 0.0 <= result.financial_risk_score <= 100.0
        assert 0.0 <= result.relationship_risk_score <= 100.0
        assert 0.0 <= result.competitive_risk_score <= 100.0

    def test_result_stored_in_predictor(self):
        p = predictor()
        inp = make_input(account_id="stored_id")
        p.predict(inp)
        assert p.get("stored_id") is not None

    def test_critical_account_has_high_probability(self):
        p = predictor()
        result = p.predict(critical_input())
        assert result.churn_probability_pct >= 60.0

    def test_safe_account_has_low_probability(self):
        p = predictor()
        result = p.predict(safe_input())
        assert result.churn_probability_pct < 40.0

    def test_lists_are_lists(self):
        p = predictor()
        result = p.predict(safe_input())
        assert isinstance(result.churn_drivers, list)
        assert isinstance(result.retention_signals, list)
        assert isinstance(result.risk_flags, list)
        assert isinstance(result.recommended_actions, list)

    def test_negative_contract_end_days_uses_base(self):
        p = predictor()
        inp = make_input(contract_end_days=-1)
        result = p.predict(inp)
        assert result.days_to_act == _DAYS_TO_ACT[result.churn_risk]


# ─── 14. ChurnPredictor query methods ────────────────────────────────────────

class TestChurnPredictorQueryMethods:
    def _setup(self) -> ChurnPredictor:
        p = predictor()
        # Add one of each risk level
        p.predict(make_input(account_id="safe_1", mau_trend_pct=15.0, nps_score=60, feature_adoption_pct=80.0, login_frequency_days=1.0, last_qbr_days=10))
        p.predict(make_input(account_id="crit_1", mau_trend_pct=-80.0, feature_adoption_pct=5.0, login_frequency_days=20.0,
                              open_tickets=10, overdue_tickets=5, critical_bugs_open=3, avg_ticket_resolution_days=20.0,
                              payment_delays=4, invoice_disputes=2, champion_lost=True, executive_sponsor_engaged=False,
                              nps_score=-80, nps_trend="declining", last_qbr_days=200, competitor_mentioned=True, rfp_received=True))
        return p

    def test_get_returns_result(self):
        p = self._setup()
        assert p.get("safe_1") is not None

    def test_get_returns_none_for_unknown(self):
        p = self._setup()
        assert p.get("unknown_id") is None

    def test_all_accounts_sorted_by_probability(self):
        p = self._setup()
        all_r = p.all_accounts()
        probs = [r.churn_probability_pct for r in all_r]
        assert probs == sorted(probs, reverse=True)

    def test_by_risk_returns_correct_risk(self):
        p = self._setup()
        for r in p.by_risk(ChurnRisk.CRITICAL):
            assert r.churn_risk == ChurnRisk.CRITICAL

    def test_critical_method(self):
        p = self._setup()
        for r in p.critical():
            assert r.churn_risk == ChurnRisk.CRITICAL

    def test_high_risk_method(self):
        p = predictor()
        p.predict(make_input(account_id="high_1", mau_trend_pct=-40.0, feature_adoption_pct=20.0,
                              login_frequency_days=8.0, champion_lost=True, executive_sponsor_engaged=False,
                              nps_score=-20, nps_trend="declining", last_qbr_days=100,
                              payment_delays=2, invoice_disputes=1, open_tickets=3))
        for r in p.high_risk():
            assert r.churn_risk == ChurnRisk.HIGH

    def test_at_risk_includes_critical_and_high(self):
        p = self._setup()
        at_r = p.at_risk()
        for r in at_r:
            assert r.churn_risk in (ChurnRisk.CRITICAL, ChurnRisk.HIGH)

    def test_safe_accounts_method(self):
        p = self._setup()
        for r in p.safe_accounts():
            assert r.churn_risk == ChurnRisk.SAFE

    def test_needs_emergency_returns_emergency_only(self):
        p = self._setup()
        for r in p.needs_emergency():
            assert r.retention_action == RetentionAction.EMERGENCY

    def test_expansion_candidates_returns_expand_only(self):
        p = self._setup()
        for r in p.expansion_candidates():
            assert r.retention_action == RetentionAction.EXPAND

    def test_total_arr_at_risk(self):
        p = self._setup()
        expected = round(sum(r.arr_at_risk_eur for r in p.all_accounts()), 2)
        assert p.total_arr_at_risk_eur() == pytest.approx(expected, abs=0.01)

    def test_avg_churn_probability(self):
        p = self._setup()
        all_r = p.all_accounts()
        expected = round(sum(r.churn_probability_pct for r in all_r) / len(all_r), 1)
        assert p.avg_churn_probability() == pytest.approx(expected, abs=0.01)

    def test_avg_churn_probability_empty(self):
        p = predictor()
        assert p.avg_churn_probability() == 0.0

    def test_top_n(self):
        p = predictor()
        for i in range(5):
            p.predict(make_input(account_id=f"acc_{i}"))
        top = p.top_n(3)
        assert len(top) == 3

    def test_top_n_sorted(self):
        p = predictor()
        for i in range(5):
            p.predict(make_input(account_id=f"acc_{i}"))
        top = p.top_n(5)
        probs = [r.churn_probability_pct for r in top]
        assert probs == sorted(probs, reverse=True)

    def test_reset_clears_results(self):
        p = self._setup()
        p.reset()
        assert p.all_accounts() == []
        assert p.get("safe_1") is None

    def test_reset_allows_repredict(self):
        p = self._setup()
        p.reset()
        p.predict(make_input(account_id="new_1"))
        assert p.get("new_1") is not None


# ─── 15. predict_batch ───────────────────────────────────────────────────────

class TestPredictBatch:
    def test_returns_list(self):
        p = predictor()
        results = p.predict_batch([safe_input(), critical_input()])
        assert isinstance(results, list)

    def test_sorted_by_probability_desc(self):
        p = predictor()
        inputs = [
            make_input(account_id="a1"),
            make_input(account_id="a2", mau_trend_pct=-50.0, feature_adoption_pct=5.0, champion_lost=True),
            make_input(account_id="a3", mau_trend_pct=-20.0),
        ]
        results = p.predict_batch(inputs)
        probs = [r.churn_probability_pct for r in results]
        assert probs == sorted(probs, reverse=True)

    def test_stores_all_results(self):
        p = predictor()
        inputs = [make_input(account_id=f"b{i}") for i in range(4)]
        p.predict_batch(inputs)
        for i in range(4):
            assert p.get(f"b{i}") is not None

    def test_empty_list_returns_empty(self):
        p = predictor()
        results = p.predict_batch([])
        assert results == []

    def test_length_matches_input(self):
        p = predictor()
        inputs = [make_input(account_id=f"c{i}") for i in range(6)]
        results = p.predict_batch(inputs)
        assert len(results) == 6


# ─── 16. summary ─────────────────────────────────────────────────────────────

class TestSummary:
    def test_empty_summary(self):
        p = predictor()
        s = p.summary()
        assert s["total"] == 0
        assert s["risk_counts"] == {}
        assert s["action_counts"] == {}
        assert s["avg_churn_probability"] == 0.0
        assert s["total_arr_at_risk_eur"] == 0.0
        assert s["critical_count"] == 0
        assert s["emergency_count"] == 0

    def test_summary_total(self):
        p = predictor()
        for i in range(3):
            p.predict(make_input(account_id=f"s{i}"))
        assert p.summary()["total"] == 3

    def test_summary_risk_counts(self):
        p = predictor()
        p.predict(safe_input())
        s = p.summary()
        assert isinstance(s["risk_counts"], dict)
        # All keys should be valid risk values
        for key in s["risk_counts"]:
            assert key in {r.value for r in ChurnRisk}

    def test_summary_action_counts(self):
        p = predictor()
        p.predict(safe_input())
        s = p.summary()
        assert isinstance(s["action_counts"], dict)
        for key in s["action_counts"]:
            assert key in {a.value for a in RetentionAction}

    def test_summary_critical_count(self):
        p = predictor()
        p.predict(critical_input())
        s = p.summary()
        assert s["critical_count"] == len(p.critical())

    def test_summary_emergency_count(self):
        p = predictor()
        p.predict(critical_input())
        s = p.summary()
        assert s["emergency_count"] == len(p.needs_emergency())

    def test_summary_avg_probability(self):
        p = predictor()
        p.predict(safe_input())
        p.predict(critical_input())
        s = p.summary()
        assert s["avg_churn_probability"] == p.avg_churn_probability()

    def test_summary_total_arr_at_risk(self):
        p = predictor()
        p.predict(safe_input())
        p.predict(critical_input())
        s = p.summary()
        assert s["total_arr_at_risk_eur"] == pytest.approx(p.total_arr_at_risk_eur(), abs=0.01)

    def test_summary_keys_present(self):
        p = predictor()
        p.predict(safe_input())
        s = p.summary()
        expected_keys = {"total", "risk_counts", "action_counts", "avg_churn_probability",
                         "total_arr_at_risk_eur", "critical_count", "emergency_count"}
        assert set(s.keys()) == expected_keys


# ─── 17. ChurnResult.to_dict ─────────────────────────────────────────────────

class TestChurnResultToDict:
    def test_returns_dict(self):
        p = predictor()
        result = p.predict(safe_input())
        assert isinstance(result.to_dict(), dict)

    def test_churn_risk_is_string(self):
        p = predictor()
        result = p.predict(safe_input())
        d = result.to_dict()
        assert isinstance(d["churn_risk"], str)
        assert d["churn_risk"] in {r.value for r in ChurnRisk}

    def test_retention_action_is_string(self):
        p = predictor()
        result = p.predict(safe_input())
        d = result.to_dict()
        assert isinstance(d["retention_action"], str)
        assert d["retention_action"] in {a.value for a in RetentionAction}

    def test_churn_risk_value_matches(self):
        p = predictor()
        result = p.predict(critical_input())
        d = result.to_dict()
        assert d["churn_risk"] == result.churn_risk.value

    def test_retention_action_value_matches(self):
        p = predictor()
        result = p.predict(critical_input())
        d = result.to_dict()
        assert d["retention_action"] == result.retention_action.value

    def test_all_fields_present(self):
        p = predictor()
        result = p.predict(safe_input())
        d = result.to_dict()
        required_keys = {
            "account_id", "account_name", "arr_eur",
            "churn_probability_pct", "churn_risk", "retention_action",
            "churn_drivers", "retention_signals", "risk_flags", "recommended_actions",
            "arr_at_risk_eur", "days_to_act",
            "usage_risk_score", "support_risk_score", "financial_risk_score",
            "relationship_risk_score", "competitive_risk_score",
        }
        assert required_keys.issubset(set(d.keys()))

    def test_account_id_in_dict(self):
        p = predictor()
        inp = make_input(account_id="dict_test")
        result = p.predict(inp)
        assert result.to_dict()["account_id"] == "dict_test"

    def test_numeric_fields_are_numbers(self):
        p = predictor()
        result = p.predict(safe_input())
        d = result.to_dict()
        assert isinstance(d["arr_eur"], (int, float))
        assert isinstance(d["churn_probability_pct"], (int, float))
        assert isinstance(d["arr_at_risk_eur"], (int, float))

    def test_drivers_is_list_in_dict(self):
        p = predictor()
        result = p.predict(safe_input())
        d = result.to_dict()
        assert isinstance(d["churn_drivers"], list)
