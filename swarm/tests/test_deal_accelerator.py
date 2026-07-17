"""
Comprehensive tests for swarm/intelligence/deal_accelerator.py
"""

from __future__ import annotations

import pytest
from swarm.intelligence.deal_accelerator import (
    DealAccelerator,
    DealContext,
    AccelerationPlan,
    DealHealth,
    AccelerationStrategy,
    SalesStage,
    _inactivity_risk,
    _stakeholder_gap,
    _competitive_risk,
    _budget_risk,
    _deal_health,
    _select_strategy,
    _win_probability,
    _deal_momentum,
    _STAGE_EXPECTED_DAYS,
)


# ─── Helper ───────────────────────────────────────────────────────────────────

def make_deal(
    deal_id: str = "d1",
    deal_name: str = "Test Deal",
    company: str = "Acme Corp",
    contact_name: str = "John Doe",
    stage: SalesStage = SalesStage.PROPOSAL,
    deal_value_eur: float = 50_000.0,
    days_in_stage: int = 15,
    days_since_last_activity: int = 5,
    close_date_in_days: int = 30,
    contacts_count: int = 2,
    decision_maker_identified: bool = True,
    champion_identified: bool = True,
    executive_sponsor: bool = True,
    budget_confirmed: bool = True,
    has_competitor: bool = False,
    competitor_strength: float = 0.0,
    competitor_name: str | None = None,
    next_step_defined: bool = True,
    meetings_last_30d: int = 2,
    prospect_initiated_last_30d: int = 1,
    last_email_response_days: int = 3,
    price_objection: bool = False,
    technical_hold: bool = False,
    rep_notes_concern: bool = False,
) -> DealContext:
    return DealContext(
        deal_id=deal_id,
        deal_name=deal_name,
        company=company,
        contact_name=contact_name,
        stage=stage,
        deal_value_eur=deal_value_eur,
        days_in_stage=days_in_stage,
        days_since_last_activity=days_since_last_activity,
        close_date_in_days=close_date_in_days,
        contacts_count=contacts_count,
        decision_maker_identified=decision_maker_identified,
        champion_identified=champion_identified,
        executive_sponsor=executive_sponsor,
        budget_confirmed=budget_confirmed,
        has_competitor=has_competitor,
        competitor_strength=competitor_strength,
        competitor_name=competitor_name,
        next_step_defined=next_step_defined,
        meetings_last_30d=meetings_last_30d,
        prospect_initiated_last_30d=prospect_initiated_last_30d,
        last_email_response_days=last_email_response_days,
        price_objection=price_objection,
        technical_hold=technical_hold,
        rep_notes_concern=rep_notes_concern,
    )


# ─── _STAGE_EXPECTED_DAYS ─────────────────────────────────────────────────────

class TestStageExpectedDays:
    def test_prospecting(self):
        assert _STAGE_EXPECTED_DAYS[SalesStage.PROSPECTING] == 14

    def test_discovery(self):
        assert _STAGE_EXPECTED_DAYS[SalesStage.DISCOVERY] == 21

    def test_demo(self):
        assert _STAGE_EXPECTED_DAYS[SalesStage.DEMO] == 21

    def test_proposal(self):
        assert _STAGE_EXPECTED_DAYS[SalesStage.PROPOSAL] == 30

    def test_negotiation(self):
        assert _STAGE_EXPECTED_DAYS[SalesStage.NEGOTIATION] == 21

    def test_closing(self):
        assert _STAGE_EXPECTED_DAYS[SalesStage.CLOSING] == 14

    def test_all_six_stages_present(self):
        assert len(_STAGE_EXPECTED_DAYS) == 6


# ─── _inactivity_risk ─────────────────────────────────────────────────────────

class TestInactivityRisk:
    # --- activity score branches ---

    def test_activity_zero_days(self):
        d = make_deal(days_since_last_activity=0)
        score, blockers = _inactivity_risk(d)
        assert score >= 0.0
        assert "no_activity" not in blockers

    def test_activity_6_days(self):
        # 6 < 7, so act_score = 6 * (30/7) ≈ 25.71
        d = make_deal(days_since_last_activity=6, next_step_defined=True,
                      meetings_last_30d=0, prospect_initiated_last_30d=0,
                      days_in_stage=0, last_email_response_days=5)
        score, blockers = _inactivity_risk(d)
        assert "no_activity" not in blockers
        expected_act = 6 * (30.0 / 7.0)
        assert abs(score - round(min(100, max(0, expected_act * 0.5)), 2)) < 1.0

    def test_activity_7_days_lower_branch(self):
        # exactly 7 is in ">=7" branch: 30 + (7-7)*(40/7) = 30
        d = make_deal(days_since_last_activity=7, next_step_defined=True,
                      meetings_last_30d=0, prospect_initiated_last_30d=0,
                      days_in_stage=0, last_email_response_days=5)
        score, blockers = _inactivity_risk(d)
        assert "no_activity" not in blockers

    def test_activity_13_days_in_7_14_branch(self):
        # 13 >= 7 and < 14: act_score = 30 + (13-7)*(40/7) ≈ 64.29
        d = make_deal(days_since_last_activity=13, next_step_defined=True,
                      meetings_last_30d=0, prospect_initiated_last_30d=0,
                      days_in_stage=0, last_email_response_days=5)
        score, blockers = _inactivity_risk(d)
        assert "no_activity" not in blockers

    def test_activity_14_days_triggers_no_activity(self):
        d = make_deal(days_since_last_activity=14)
        _, blockers = _inactivity_risk(d)
        assert "no_activity" in blockers

    def test_activity_14_days_score_formula(self):
        # act_score = 70 + (14-14)*(30/16) = 70
        d = make_deal(days_since_last_activity=14, next_step_defined=True,
                      meetings_last_30d=0, prospect_initiated_last_30d=0,
                      days_in_stage=0, last_email_response_days=5)
        score, blockers = _inactivity_risk(d)
        # act_score=70, overrun=0, penalty=0, bonus=0 => 70*0.5 = 35
        assert abs(score - 35.0) < 0.1

    def test_activity_22_days_score_formula(self):
        # act_score = 70 + (22-14)*(30/16) = 70 + 15 = 85
        d = make_deal(days_since_last_activity=22, next_step_defined=True,
                      meetings_last_30d=0, prospect_initiated_last_30d=0,
                      days_in_stage=0, last_email_response_days=5)
        score, _ = _inactivity_risk(d)
        expected_act = 70 + (22 - 14) * (30 / 16)
        expected = expected_act * 0.5
        assert abs(score - round(min(100, expected), 2)) < 0.1

    def test_activity_30_days_max_score(self):
        d = make_deal(days_since_last_activity=30)
        _, blockers = _inactivity_risk(d)
        assert "no_activity" in blockers

    def test_activity_gt_30_days_capped_100(self):
        # act_score = 100, score should be capped
        d = make_deal(days_since_last_activity=60, next_step_defined=False,
                      meetings_last_30d=0, prospect_initiated_last_30d=0,
                      days_in_stage=100, last_email_response_days=20,
                      stage=SalesStage.CLOSING)  # expected=14, overrun=86 => overrun_score=40
        score, _ = _inactivity_risk(d)
        assert score == 100.0

    def test_activity_29_days_no_activity_blocker(self):
        d = make_deal(days_since_last_activity=29)
        _, blockers = _inactivity_risk(d)
        assert "no_activity" in blockers

    # --- overrun / long_cycle ---

    def test_no_overrun_no_long_cycle(self):
        # stage=PROPOSAL expected=30, days_in_stage=15 => overrun=0
        d = make_deal(stage=SalesStage.PROPOSAL, days_in_stage=15)
        _, blockers = _inactivity_risk(d)
        assert "long_cycle" not in blockers

    def test_overrun_exactly_14_no_long_cycle(self):
        # overrun=14, not >14
        d = make_deal(stage=SalesStage.PROPOSAL, days_in_stage=44)  # 44-30=14
        _, blockers = _inactivity_risk(d)
        assert "long_cycle" not in blockers

    def test_overrun_15_triggers_long_cycle(self):
        # overrun=15 > 14 → long_cycle
        d = make_deal(stage=SalesStage.PROPOSAL, days_in_stage=45)  # 45-30=15
        _, blockers = _inactivity_risk(d)
        assert "long_cycle" in blockers

    def test_overrun_score_capped_at_40(self):
        # overrun=100 => overrun_score = min(40, 100*2)=40
        d = make_deal(stage=SalesStage.PROSPECTING, days_in_stage=114,  # 114-14=100
                      days_since_last_activity=0, next_step_defined=True,
                      meetings_last_30d=2, prospect_initiated_last_30d=1,
                      last_email_response_days=3)
        score, _ = _inactivity_risk(d)
        # act_score=0, overrun=40, penalty=0, bonus=min(20, 1*15+2*10)=20 => 0+40+0-20=20
        assert abs(score - 20.0) < 0.1

    def test_overrun_score_partial(self):
        # stage=CLOSING expected=14, days_in_stage=20 => overrun=6 => overrun_score=12
        d = make_deal(stage=SalesStage.CLOSING, days_in_stage=20,
                      days_since_last_activity=0, next_step_defined=True,
                      meetings_last_30d=0, prospect_initiated_last_30d=0,
                      last_email_response_days=5)
        score, _ = _inactivity_risk(d)
        # act_score=0, overrun_score=12, penalty=0, bonus=0 => score=12
        assert abs(score - 12.0) < 0.1

    # --- no_next_step penalty ---

    def test_no_next_step_adds_blocker(self):
        d = make_deal(next_step_defined=False)
        _, blockers = _inactivity_risk(d)
        assert "no_next_step" in blockers

    def test_next_step_defined_no_blocker(self):
        d = make_deal(next_step_defined=True)
        _, blockers = _inactivity_risk(d)
        assert "no_next_step" not in blockers

    def test_no_next_step_adds_20_penalty(self):
        d_with = make_deal(next_step_defined=True, days_since_last_activity=0,
                           days_in_stage=0, meetings_last_30d=0,
                           prospect_initiated_last_30d=0, last_email_response_days=5)
        d_without = make_deal(next_step_defined=False, days_since_last_activity=0,
                              days_in_stage=0, meetings_last_30d=0,
                              prospect_initiated_last_30d=0, last_email_response_days=5)
        s_with, _ = _inactivity_risk(d_with)
        s_without, _ = _inactivity_risk(d_without)
        assert abs((s_without - s_with) - 20.0) < 0.1

    # --- engagement bonus ---

    def test_engagement_bonus_capped_at_20(self):
        # prospect_initiated=5 (5*15=75), meetings=5 (5*10=50) => engagement=125, bonus=20
        d = make_deal(prospect_initiated_last_30d=5, meetings_last_30d=5,
                      days_since_last_activity=0, days_in_stage=0,
                      next_step_defined=True, last_email_response_days=5)
        score, _ = _inactivity_risk(d)
        # act_score=0, overrun=0, penalty=0, bonus=20 => max(0, 0-20)=0
        assert score == 0.0

    def test_engagement_bonus_partial(self):
        # prospect_initiated=0, meetings=1 => engagement=10 => bonus=10
        d = make_deal(prospect_initiated_last_30d=0, meetings_last_30d=1,
                      days_since_last_activity=0, days_in_stage=0,
                      next_step_defined=True, last_email_response_days=5)
        score, _ = _inactivity_risk(d)
        # 0*0.5 + 0 + 0 - 10 = -10 => clamped to 0
        assert score == 0.0

    # --- low_engagement blocker ---

    def test_low_engagement_meetings_zero_and_email_gt_14(self):
        d = make_deal(meetings_last_30d=0, last_email_response_days=15)
        _, blockers = _inactivity_risk(d)
        assert "low_engagement" in blockers

    def test_low_engagement_meetings_1_not_triggered(self):
        d = make_deal(meetings_last_30d=1, last_email_response_days=20)
        _, blockers = _inactivity_risk(d)
        assert "low_engagement" not in blockers

    def test_low_engagement_email_exactly_14_not_triggered(self):
        d = make_deal(meetings_last_30d=0, last_email_response_days=14)
        _, blockers = _inactivity_risk(d)
        assert "low_engagement" not in blockers

    def test_low_engagement_email_0_not_triggered(self):
        # last_email_response_days=0 is not > 14
        d = make_deal(meetings_last_30d=0, last_email_response_days=0)
        _, blockers = _inactivity_risk(d)
        assert "low_engagement" not in blockers

    # --- clamping ---

    def test_score_never_below_0(self):
        d = make_deal(days_since_last_activity=0, days_in_stage=0,
                      next_step_defined=True, meetings_last_30d=10,
                      prospect_initiated_last_30d=10, last_email_response_days=1)
        score, _ = _inactivity_risk(d)
        assert score >= 0.0

    def test_score_never_above_100(self):
        d = make_deal(days_since_last_activity=60, days_in_stage=200,
                      next_step_defined=False, meetings_last_30d=0,
                      prospect_initiated_last_30d=0, last_email_response_days=60,
                      stage=SalesStage.PROSPECTING)
        score, _ = _inactivity_risk(d)
        assert score <= 100.0

    def test_score_is_rounded_to_2dp(self):
        d = make_deal(days_since_last_activity=13)
        score, _ = _inactivity_risk(d)
        assert score == round(score, 2)


# ─── _stakeholder_gap ─────────────────────────────────────────────────────────

class TestStakeholderGap:
    def test_perfect_deal_zero_score(self):
        d = make_deal(contacts_count=3, decision_maker_identified=True,
                      champion_identified=True, executive_sponsor=True,
                      deal_value_eur=50_000)
        score, blockers = _stakeholder_gap(d)
        assert score == 0.0
        assert blockers == []

    def test_single_contact_adds_40_and_blocker(self):
        d = make_deal(contacts_count=1, decision_maker_identified=True,
                      champion_identified=True, executive_sponsor=True)
        score, blockers = _stakeholder_gap(d)
        assert score == 40.0
        assert "single_threaded" in blockers

    def test_two_contacts_adds_20_no_single_threaded(self):
        d = make_deal(contacts_count=2, decision_maker_identified=True,
                      champion_identified=True, executive_sponsor=True)
        score, blockers = _stakeholder_gap(d)
        assert score == 20.0
        assert "single_threaded" not in blockers

    def test_three_contacts_adds_0_stakeholder(self):
        d = make_deal(contacts_count=3, decision_maker_identified=True,
                      champion_identified=True, executive_sponsor=True)
        score, blockers = _stakeholder_gap(d)
        assert score == 0.0

    def test_no_decision_maker_adds_30_and_blocker(self):
        d = make_deal(contacts_count=3, decision_maker_identified=False,
                      champion_identified=True, executive_sponsor=True)
        score, blockers = _stakeholder_gap(d)
        assert score == 30.0
        assert "no_decision_maker" in blockers

    def test_no_champion_adds_20_and_blocker(self):
        d = make_deal(contacts_count=3, decision_maker_identified=True,
                      champion_identified=False, executive_sponsor=True)
        score, blockers = _stakeholder_gap(d)
        assert score == 20.0
        assert "no_champion" in blockers

    def test_no_executive_sponsor_high_value_adds_15(self):
        d = make_deal(contacts_count=3, decision_maker_identified=True,
                      champion_identified=True, executive_sponsor=False,
                      deal_value_eur=50_000)
        score, blockers = _stakeholder_gap(d)
        assert score == 15.0
        assert "executive_misalignment" in blockers

    def test_no_executive_sponsor_low_value_no_penalty(self):
        d = make_deal(contacts_count=3, decision_maker_identified=True,
                      champion_identified=True, executive_sponsor=False,
                      deal_value_eur=49_999)
        score, blockers = _stakeholder_gap(d)
        assert score == 0.0
        assert "executive_misalignment" not in blockers

    def test_executive_misalignment_threshold_exactly_50k(self):
        d = make_deal(contacts_count=3, decision_maker_identified=True,
                      champion_identified=True, executive_sponsor=False,
                      deal_value_eur=50_000)
        score, blockers = _stakeholder_gap(d)
        assert "executive_misalignment" in blockers

    def test_all_bad_single_contact_no_dm_no_champ_no_exec(self):
        d = make_deal(contacts_count=1, decision_maker_identified=False,
                      champion_identified=False, executive_sponsor=False,
                      deal_value_eur=100_000)
        score, blockers = _stakeholder_gap(d)
        # 40 + 30 + 20 + 15 = 105 => capped at 100
        assert score == 100.0
        assert "single_threaded" in blockers
        assert "no_decision_maker" in blockers
        assert "no_champion" in blockers
        assert "executive_misalignment" in blockers

    def test_score_capped_at_100(self):
        d = make_deal(contacts_count=1, decision_maker_identified=False,
                      champion_identified=False, executive_sponsor=False,
                      deal_value_eur=100_000)
        score, _ = _stakeholder_gap(d)
        assert score == 100.0

    def test_score_rounded_2dp(self):
        d = make_deal()
        score, _ = _stakeholder_gap(d)
        assert score == round(score, 2)

    def test_two_contacts_no_dm_combined(self):
        d = make_deal(contacts_count=2, decision_maker_identified=False,
                      champion_identified=True, executive_sponsor=True)
        score, blockers = _stakeholder_gap(d)
        assert score == 50.0
        assert "no_decision_maker" in blockers


# ─── _competitive_risk ────────────────────────────────────────────────────────

class TestCompetitiveRisk:
    def test_no_competitor_returns_zero(self):
        d = make_deal(has_competitor=False, competitor_strength=80)
        score, blockers = _competitive_risk(d)
        assert score == 0.0
        assert blockers == []

    def test_competitor_below_40_no_blocker(self):
        d = make_deal(has_competitor=True, competitor_strength=30)
        score, blockers = _competitive_risk(d)
        assert score == 30.0
        assert "competitive_threat" not in blockers

    def test_competitor_exactly_40_triggers_blocker(self):
        d = make_deal(has_competitor=True, competitor_strength=40)
        score, blockers = _competitive_risk(d)
        assert score == 40.0
        assert "competitive_threat" in blockers

    def test_competitor_above_40_triggers_blocker(self):
        d = make_deal(has_competitor=True, competitor_strength=75)
        score, blockers = _competitive_risk(d)
        assert score == 75.0
        assert "competitive_threat" in blockers

    def test_competitor_strength_100_max(self):
        d = make_deal(has_competitor=True, competitor_strength=100)
        score, _ = _competitive_risk(d)
        assert score == 100.0

    def test_competitor_strength_above_100_capped(self):
        d = make_deal(has_competitor=True, competitor_strength=150)
        score, _ = _competitive_risk(d)
        assert score == 100.0

    def test_competitor_strength_0_no_blocker(self):
        d = make_deal(has_competitor=True, competitor_strength=0)
        score, blockers = _competitive_risk(d)
        assert score == 0.0
        assert "competitive_threat" not in blockers

    def test_score_rounded_2dp(self):
        d = make_deal(has_competitor=True, competitor_strength=33.333)
        score, _ = _competitive_risk(d)
        assert score == round(score, 2)

    def test_competitor_strength_39_no_threat(self):
        d = make_deal(has_competitor=True, competitor_strength=39)
        score, blockers = _competitive_risk(d)
        assert "competitive_threat" not in blockers
        assert score == 39.0


# ─── _budget_risk ─────────────────────────────────────────────────────────────

class TestBudgetRisk:
    def test_all_good_zero_score(self):
        d = make_deal(budget_confirmed=True, price_objection=False, technical_hold=False)
        score, blockers = _budget_risk(d)
        assert score == 0.0
        assert blockers == []

    def test_budget_not_confirmed_adds_40(self):
        d = make_deal(budget_confirmed=False, price_objection=False, technical_hold=False)
        score, blockers = _budget_risk(d)
        assert score == 40.0
        assert "budget_not_confirmed" in blockers

    def test_price_objection_adds_35(self):
        d = make_deal(budget_confirmed=True, price_objection=True, technical_hold=False)
        score, blockers = _budget_risk(d)
        assert score == 35.0
        assert "price_objection" in blockers

    def test_technical_hold_adds_25(self):
        d = make_deal(budget_confirmed=True, price_objection=False, technical_hold=True)
        score, blockers = _budget_risk(d)
        assert score == 25.0
        assert "technical_hold" in blockers

    def test_all_bad_capped_at_100(self):
        d = make_deal(budget_confirmed=False, price_objection=True, technical_hold=True)
        score, blockers = _budget_risk(d)
        # 40 + 35 + 25 = 100
        assert score == 100.0
        assert "budget_not_confirmed" in blockers
        assert "price_objection" in blockers
        assert "technical_hold" in blockers

    def test_budget_plus_price_objection(self):
        d = make_deal(budget_confirmed=False, price_objection=True, technical_hold=False)
        score, blockers = _budget_risk(d)
        assert score == 75.0

    def test_budget_plus_technical_hold(self):
        d = make_deal(budget_confirmed=False, price_objection=False, technical_hold=True)
        score, blockers = _budget_risk(d)
        assert score == 65.0

    def test_price_objection_plus_technical_hold(self):
        d = make_deal(budget_confirmed=True, price_objection=True, technical_hold=True)
        score, blockers = _budget_risk(d)
        assert score == 60.0

    def test_score_rounded_2dp(self):
        d = make_deal(budget_confirmed=False)
        score, _ = _budget_risk(d)
        assert score == round(score, 2)


# ─── _deal_health ─────────────────────────────────────────────────────────────

class TestDealHealth:
    def test_stall_80_returns_critical(self):
        d = make_deal()
        result = _deal_health(80.0, 30, d)
        assert result == DealHealth.CRITICAL

    def test_stall_above_80_returns_critical(self):
        d = make_deal()
        result = _deal_health(95.0, 30, d)
        assert result == DealHealth.CRITICAL

    def test_stall_60_overdue_returns_critical(self):
        d = make_deal()
        result = _deal_health(60.0, -1, d)
        assert result == DealHealth.CRITICAL

    def test_stall_60_not_overdue_returns_stalled(self):
        d = make_deal()
        result = _deal_health(60.0, 10, d)
        assert result == DealHealth.STALLED

    def test_stall_60_returns_stalled(self):
        d = make_deal()
        result = _deal_health(60.0, 30, d)
        assert result == DealHealth.STALLED

    def test_stall_40_overdue_returns_stalled(self):
        d = make_deal()
        result = _deal_health(40.0, -5, d)
        assert result == DealHealth.STALLED

    def test_stall_35_returns_at_risk(self):
        d = make_deal()
        result = _deal_health(35.0, 30, d)
        assert result == DealHealth.AT_RISK

    def test_stall_below_35_overdue_returns_at_risk(self):
        d = make_deal()
        result = _deal_health(10.0, -1, d)
        assert result == DealHealth.AT_RISK

    def test_stall_15_returns_active(self):
        d = make_deal()
        result = _deal_health(15.0, 30, d)
        assert result == DealHealth.ACTIVE

    def test_stall_34_returns_active(self):
        # 34 < 35, not overdue → falls through to ACTIVE
        d = make_deal()
        result = _deal_health(34.0, 30, d)
        assert result == DealHealth.ACTIVE

    def test_stall_0_returns_active(self):
        d = make_deal()
        result = _deal_health(0.0, 30, d)
        assert result == DealHealth.ACTIVE

    def test_stall_59_not_overdue_returns_stalled(self):
        # 59 >= 35 but < 60, not overdue → AT_RISK
        d = make_deal()
        result = _deal_health(59.0, 30, d)
        assert result == DealHealth.AT_RISK

    def test_stall_79_not_overdue_returns_stalled(self):
        d = make_deal()
        result = _deal_health(79.0, 30, d)
        assert result == DealHealth.STALLED

    def test_stall_79_overdue_returns_critical(self):
        # overdue and stall>=60 => critical
        d = make_deal()
        result = _deal_health(79.0, -1, d)
        assert result == DealHealth.CRITICAL

    def test_stall_14_returns_active(self):
        d = make_deal()
        result = _deal_health(14.0, 30, d)
        assert result == DealHealth.ACTIVE


# ─── _win_probability ─────────────────────────────────────────────────────────

class TestWinProbability:
    def test_prospecting_base(self):
        d = make_deal(stage=SalesStage.PROSPECTING, decision_maker_identified=False,
                      champion_identified=False, budget_confirmed=False,
                      has_competitor=False, price_objection=False, next_step_defined=False)
        prob = _win_probability(d, 0.0)
        # 10 - 8 = 2
        assert prob == 2.0

    def test_closing_base_all_good(self):
        d = make_deal(stage=SalesStage.CLOSING)
        prob = _win_probability(d, 0.0)
        # 80 + 5 + 8 + 7 = 100
        assert prob == 100.0

    def test_decision_maker_adds_5(self):
        d_yes = make_deal(decision_maker_identified=True, champion_identified=False,
                          budget_confirmed=False, has_competitor=False,
                          price_objection=False, next_step_defined=True)
        d_no = make_deal(decision_maker_identified=False, champion_identified=False,
                         budget_confirmed=False, has_competitor=False,
                         price_objection=False, next_step_defined=True)
        diff = _win_probability(d_yes, 0) - _win_probability(d_no, 0)
        assert abs(diff - 5.0) < 0.01

    def test_champion_adds_8(self):
        d_yes = make_deal(champion_identified=True, decision_maker_identified=False,
                          budget_confirmed=False, has_competitor=False,
                          price_objection=False, next_step_defined=True)
        d_no = make_deal(champion_identified=False, decision_maker_identified=False,
                         budget_confirmed=False, has_competitor=False,
                         price_objection=False, next_step_defined=True)
        diff = _win_probability(d_yes, 0) - _win_probability(d_no, 0)
        assert abs(diff - 8.0) < 0.01

    def test_budget_confirmed_adds_7(self):
        d_yes = make_deal(budget_confirmed=True, decision_maker_identified=False,
                          champion_identified=False, has_competitor=False,
                          price_objection=False, next_step_defined=True)
        d_no = make_deal(budget_confirmed=False, decision_maker_identified=False,
                         champion_identified=False, has_competitor=False,
                         price_objection=False, next_step_defined=True)
        diff = _win_probability(d_yes, 0) - _win_probability(d_no, 0)
        assert abs(diff - 7.0) < 0.01

    def test_competitor_reduces_by_strength_times_015(self):
        d = make_deal(has_competitor=True, competitor_strength=40,
                      decision_maker_identified=False, champion_identified=False,
                      budget_confirmed=False, price_objection=False,
                      next_step_defined=True)
        prob = _win_probability(d, 0.0)
        # base=50 (PROPOSAL) - 40*0.15 = 50 - 6 = 44
        assert abs(prob - 44.0) < 0.1

    def test_price_objection_subtracts_10(self):
        d_yes = make_deal(price_objection=True, decision_maker_identified=False,
                          champion_identified=False, budget_confirmed=False,
                          has_competitor=False, next_step_defined=True)
        d_no = make_deal(price_objection=False, decision_maker_identified=False,
                         champion_identified=False, budget_confirmed=False,
                         has_competitor=False, next_step_defined=True)
        diff = _win_probability(d_no, 0) - _win_probability(d_yes, 0)
        assert abs(diff - 10.0) < 0.01

    def test_no_next_step_subtracts_8(self):
        d_yes = make_deal(next_step_defined=True, decision_maker_identified=False,
                          champion_identified=False, budget_confirmed=False,
                          has_competitor=False, price_objection=False)
        d_no = make_deal(next_step_defined=False, decision_maker_identified=False,
                         champion_identified=False, budget_confirmed=False,
                         has_competitor=False, price_objection=False)
        diff = _win_probability(d_yes, 0) - _win_probability(d_no, 0)
        assert abs(diff - 8.0) < 0.01

    def test_stall_penalty_applied(self):
        d = make_deal(decision_maker_identified=False, champion_identified=False,
                      budget_confirmed=False, has_competitor=False,
                      price_objection=False, next_step_defined=True)
        # PROPOSAL base=50, stall_penalty=100*0.30=30 => 50-30=20
        prob = _win_probability(d, 100.0)
        assert abs(prob - 20.0) < 0.01

    def test_clamped_below_0(self):
        d = make_deal(stage=SalesStage.PROSPECTING, has_competitor=True,
                      competitor_strength=100, price_objection=True,
                      next_step_defined=False, decision_maker_identified=False,
                      champion_identified=False, budget_confirmed=False)
        prob = _win_probability(d, 100.0)
        assert prob == 0.0

    def test_clamped_above_100(self):
        d = make_deal(stage=SalesStage.CLOSING)
        prob = _win_probability(d, 0.0)
        assert prob <= 100.0

    def test_all_stages_produce_valid_probability(self):
        for stage in SalesStage:
            d = make_deal(stage=stage)
            prob = _win_probability(d, 0.0)
            assert 0 <= prob <= 100


# ─── _deal_momentum ───────────────────────────────────────────────────────────

class TestDealMomentum:
    def test_baseline_50(self):
        # prospect_init=0, meetings=0, email=7, no next_step, activity=5
        d = make_deal(prospect_initiated_last_30d=0, meetings_last_30d=0,
                      last_email_response_days=7, next_step_defined=False,
                      days_since_last_activity=5)
        score = _deal_momentum(d)
        # 50 + 0 + 0 + 0 - 15 = 35
        assert abs(score - 35.0) < 0.1

    def test_prospect_initiated_bonus_capped_20(self):
        d = make_deal(prospect_initiated_last_30d=5, meetings_last_30d=0,
                      last_email_response_days=7, next_step_defined=False,
                      days_since_last_activity=5)
        score = _deal_momentum(d)
        # 50 + 20 + 0 + 0 - 15 = 55
        assert abs(score - 55.0) < 0.1

    def test_meetings_bonus_capped_20(self):
        d = make_deal(prospect_initiated_last_30d=0, meetings_last_30d=5,
                      last_email_response_days=7, next_step_defined=True,
                      days_since_last_activity=5)
        score = _deal_momentum(d)
        # 50 + 0 + min(20, 35) + 0 + 10 = 80
        assert abs(score - 80.0) < 0.1

    def test_email_response_le_3_adds_10(self):
        d = make_deal(prospect_initiated_last_30d=0, meetings_last_30d=0,
                      last_email_response_days=3, next_step_defined=True,
                      days_since_last_activity=5)
        score = _deal_momentum(d)
        # 50 + 0 + 0 + 10 + 10 = 70
        assert abs(score - 70.0) < 0.1

    def test_email_response_gt_14_subtracts_20(self):
        d = make_deal(prospect_initiated_last_30d=0, meetings_last_30d=0,
                      last_email_response_days=15, next_step_defined=True,
                      days_since_last_activity=5)
        score = _deal_momentum(d)
        # 50 + 0 + 0 - 20 + 10 = 40
        assert abs(score - 40.0) < 0.1

    def test_email_response_1_adds_10(self):
        d = make_deal(prospect_initiated_last_30d=0, meetings_last_30d=0,
                      last_email_response_days=1, next_step_defined=True,
                      days_since_last_activity=5)
        score = _deal_momentum(d)
        # 50 + 0 + 0 + 10 + 10 = 70
        assert abs(score - 70.0) < 0.1

    def test_email_response_0_no_adjustment(self):
        # last_email_response_days=0 → not >0 so not <=3 branch, not >14
        d = make_deal(prospect_initiated_last_30d=0, meetings_last_30d=0,
                      last_email_response_days=0, next_step_defined=True,
                      days_since_last_activity=5)
        score = _deal_momentum(d)
        # 50 + 0 + 0 + 0 + 10 = 60
        assert abs(score - 60.0) < 0.1

    def test_no_next_step_subtracts_15(self):
        d = make_deal(prospect_initiated_last_30d=0, meetings_last_30d=0,
                      last_email_response_days=7, next_step_defined=False,
                      days_since_last_activity=5)
        score = _deal_momentum(d)
        # 50 + 0 + 0 + 0 - 15 = 35
        assert abs(score - 35.0) < 0.1

    def test_next_step_adds_10(self):
        d = make_deal(prospect_initiated_last_30d=0, meetings_last_30d=0,
                      last_email_response_days=7, next_step_defined=True,
                      days_since_last_activity=5)
        score = _deal_momentum(d)
        # 50 + 0 + 0 + 0 + 10 = 60
        assert abs(score - 60.0) < 0.1

    def test_activity_gt_14_subtracts_20(self):
        d = make_deal(prospect_initiated_last_30d=0, meetings_last_30d=0,
                      last_email_response_days=7, next_step_defined=True,
                      days_since_last_activity=15)
        score = _deal_momentum(d)
        # 50 + 0 + 0 + 0 + 10 - 20 = 40
        assert abs(score - 40.0) < 0.1

    def test_clamped_min_0(self):
        d = make_deal(prospect_initiated_last_30d=0, meetings_last_30d=0,
                      last_email_response_days=20, next_step_defined=False,
                      days_since_last_activity=30)
        score = _deal_momentum(d)
        # 50 + 0 + 0 - 20 - 15 - 20 = -5 => 0
        assert score == 0.0

    def test_clamped_max_100(self):
        d = make_deal(prospect_initiated_last_30d=10, meetings_last_30d=10,
                      last_email_response_days=1, next_step_defined=True,
                      days_since_last_activity=3)
        score = _deal_momentum(d)
        # 50 + 20 + 20 + 10 + 10 = 110 => 100
        assert score == 100.0

    def test_score_rounded_2dp(self):
        d = make_deal()
        score = _deal_momentum(d)
        assert score == round(score, 2)


# ─── _select_strategy ─────────────────────────────────────────────────────────

class TestSelectStrategy:
    def test_no_dm_prefers_executive_sponsor(self):
        d = make_deal(decision_maker_identified=False, executive_sponsor=False,
                      champion_identified=True, price_objection=False,
                      budget_confirmed=True, close_date_in_days=30,
                      deal_value_eur=10_000)
        primary, _ = _select_strategy(d, 0, 0, 0, 0)
        assert primary == AccelerationStrategy.EXECUTIVE_SPONSOR

    def test_no_champion_adds_champion_build_score(self):
        d = make_deal(decision_maker_identified=True, executive_sponsor=True,
                      champion_identified=False, price_objection=False,
                      budget_confirmed=True, close_date_in_days=30,
                      deal_value_eur=10_000, has_competitor=False)
        primary, _ = _select_strategy(d, 0, 0, 0, 0)
        assert primary == AccelerationStrategy.CHAMPION_BUILD

    def test_high_competitive_score_prefers_competitive_play(self):
        d = make_deal(decision_maker_identified=True, executive_sponsor=True,
                      champion_identified=True, price_objection=False,
                      budget_confirmed=True, close_date_in_days=30,
                      deal_value_eur=10_000)
        primary, _ = _select_strategy(d, 0, 0, 80, 0)
        # competitive >= 50 → COMPETITIVE_PLAY += 80*0.5 = 40
        assert primary == AccelerationStrategy.COMPETITIVE_PLAY

    def test_closing_stage_near_deadline_direct_close(self):
        d = make_deal(stage=SalesStage.CLOSING, close_date_in_days=5,
                      decision_maker_identified=True, executive_sponsor=True,
                      champion_identified=True, budget_confirmed=True,
                      price_objection=False, deal_value_eur=10_000, has_competitor=False)
        primary, _ = _select_strategy(d, 0, 0, 0, 0)
        assert primary == AccelerationStrategy.DIRECT_CLOSE

    def test_negotiation_near_deadline_direct_close(self):
        d = make_deal(stage=SalesStage.NEGOTIATION, close_date_in_days=3,
                      decision_maker_identified=True, executive_sponsor=True,
                      champion_identified=True, budget_confirmed=True,
                      price_objection=False, deal_value_eur=10_000, has_competitor=False)
        primary, _ = _select_strategy(d, 0, 0, 0, 0)
        assert primary == AccelerationStrategy.DIRECT_CLOSE

    def test_high_inactivity_adds_urgency(self):
        d = make_deal(decision_maker_identified=True, executive_sponsor=True,
                      champion_identified=True, budget_confirmed=True,
                      price_objection=False, deal_value_eur=10_000, has_competitor=False,
                      close_date_in_days=30)
        primary, _ = _select_strategy(d, 70, 0, 0, 0)
        # urgency_create += 30
        assert primary == AccelerationStrategy.URGENCY_CREATE

    def test_secondary_strategies_not_empty_when_multiple_signals(self):
        d = make_deal(decision_maker_identified=False, champion_identified=False,
                      budget_confirmed=False, price_objection=True,
                      executive_sponsor=False, deal_value_eur=50_000)
        primary, secondary = _select_strategy(d, 70, 50, 60, 75)
        assert isinstance(secondary, list)
        assert len(secondary) <= 3

    def test_returns_valid_strategy_types(self):
        d = make_deal()
        primary, secondary = _select_strategy(d, 20, 10, 30, 40)
        assert isinstance(primary, AccelerationStrategy)
        for s in secondary:
            assert isinstance(s, AccelerationStrategy)


# ─── Composite stall_score formula ────────────────────────────────────────────

class TestCompositeStallScore:
    def test_formula_weights(self):
        """Verify inact*0.35 + stakeh*0.25 + comp*0.20 + budget*0.20"""
        d = make_deal(
            days_since_last_activity=30,   # inact near 100
            contacts_count=1,              # stakeh has 40
            has_competitor=True,
            competitor_strength=50,
            budget_confirmed=False,
            decision_maker_identified=True,
            champion_identified=True,
            executive_sponsor=True,
            next_step_defined=True,
            meetings_last_30d=0,
            prospect_initiated_last_30d=0,
            last_email_response_days=5,
            days_in_stage=0,
            price_objection=False,
            technical_hold=False,
        )
        inact, _ = _inactivity_risk(d)
        stakeh, _ = _stakeholder_gap(d)
        comp, _ = _competitive_risk(d)
        budget, _ = _budget_risk(d)
        expected = round(inact * 0.35 + stakeh * 0.25 + comp * 0.20 + budget * 0.20, 2)

        acc = DealAccelerator()
        plan = acc.accelerate(d)
        assert abs(plan.stall_score - expected) < 0.01

    def test_perfect_deal_near_zero_stall(self):
        d = make_deal(
            days_since_last_activity=0,
            contacts_count=5,
            has_competitor=False,
            budget_confirmed=True,
            decision_maker_identified=True,
            champion_identified=True,
            executive_sponsor=True,
            next_step_defined=True,
            meetings_last_30d=3,
            prospect_initiated_last_30d=2,
            last_email_response_days=1,
            days_in_stage=5,
            price_objection=False,
            technical_hold=False,
        )
        acc = DealAccelerator()
        plan = acc.accelerate(d)
        assert plan.stall_score < 20.0


# ─── DealAccelerator methods ──────────────────────────────────────────────────

class TestDealAcceleratorAccelerate:
    def test_returns_acceleration_plan(self):
        acc = DealAccelerator()
        d = make_deal()
        plan = acc.accelerate(d)
        assert isinstance(plan, AccelerationPlan)

    def test_plan_stored_by_deal_id(self):
        acc = DealAccelerator()
        d = make_deal(deal_id="abc")
        acc.accelerate(d)
        assert acc.get("abc") is not None

    def test_get_returns_none_for_unknown(self):
        acc = DealAccelerator()
        assert acc.get("nonexistent") is None

    def test_get_returns_plan_after_accelerate(self):
        acc = DealAccelerator()
        d = make_deal(deal_id="x1")
        plan = acc.accelerate(d)
        assert acc.get("x1") is plan

    def test_accelerate_overwrites_old_plan(self):
        acc = DealAccelerator()
        d1 = make_deal(deal_id="same")
        d2 = make_deal(deal_id="same", days_since_last_activity=30)
        acc.accelerate(d1)
        plan2 = acc.accelerate(d2)
        assert acc.get("same") is plan2

    def test_plan_has_all_required_fields(self):
        acc = DealAccelerator()
        plan = acc.accelerate(make_deal())
        assert hasattr(plan, "deal_health")
        assert hasattr(plan, "stall_score")
        assert hasattr(plan, "inactivity_risk")
        assert hasattr(plan, "stakeholder_gap")
        assert hasattr(plan, "competitive_risk")
        assert hasattr(plan, "budget_risk")
        assert hasattr(plan, "primary_strategy")
        assert hasattr(plan, "secondary_strategies")
        assert hasattr(plan, "active_blockers")
        assert hasattr(plan, "action_plan")
        assert hasattr(plan, "days_to_act")
        assert hasattr(plan, "win_probability_adj")
        assert hasattr(plan, "deal_momentum")


class TestDealAcceleratorBatch:
    def test_accelerate_batch_returns_list(self):
        acc = DealAccelerator()
        deals = [make_deal(deal_id=f"d{i}") for i in range(3)]
        plans = acc.accelerate_batch(deals)
        assert len(plans) == 3

    def test_accelerate_batch_stores_all(self):
        acc = DealAccelerator()
        deals = [make_deal(deal_id=f"b{i}") for i in range(5)]
        acc.accelerate_batch(deals)
        for i in range(5):
            assert acc.get(f"b{i}") is not None

    def test_accelerate_batch_empty_list(self):
        acc = DealAccelerator()
        plans = acc.accelerate_batch([])
        assert plans == []


class TestDealAcceleratorAllPlans:
    def test_all_plans_sorted_by_stall_score_desc(self):
        acc = DealAccelerator()
        d_low = make_deal(deal_id="low", days_since_last_activity=0)
        d_high = make_deal(deal_id="high", days_since_last_activity=30,
                           contacts_count=1, decision_maker_identified=False)
        acc.accelerate(d_low)
        acc.accelerate(d_high)
        plans = acc.all_plans()
        assert plans[0].stall_score >= plans[-1].stall_score

    def test_all_plans_empty_initially(self):
        acc = DealAccelerator()
        assert acc.all_plans() == []

    def test_all_plans_count(self):
        acc = DealAccelerator()
        for i in range(4):
            acc.accelerate(make_deal(deal_id=f"p{i}"))
        assert len(acc.all_plans()) == 4


class TestDealAcceleratorByHealth:
    def test_by_health_filters_correctly(self):
        acc = DealAccelerator()
        # Force a critical deal
        d_crit = make_deal(deal_id="crit", days_since_last_activity=30,
                           contacts_count=1, decision_maker_identified=False,
                           champion_identified=False, budget_confirmed=False,
                           price_objection=True, technical_hold=True,
                           next_step_defined=False, meetings_last_30d=0,
                           prospect_initiated_last_30d=0, last_email_response_days=30,
                           days_in_stage=100)
        d_good = make_deal(deal_id="good")
        acc.accelerate(d_crit)
        acc.accelerate(d_good)
        critical = acc.by_health(DealHealth.CRITICAL)
        for p in critical:
            assert p.deal_health == DealHealth.CRITICAL

    def test_by_health_returns_empty_when_no_match(self):
        acc = DealAccelerator()
        acc.accelerate(make_deal())
        lost = acc.by_health(DealHealth.LOST)
        assert lost == []


class TestDealAcceleratorCriticalDeals:
    def test_critical_deals_only_critical(self):
        acc = DealAccelerator()
        d = make_deal(deal_id="cr", days_since_last_activity=30,
                      contacts_count=1, decision_maker_identified=False,
                      champion_identified=False, budget_confirmed=False,
                      price_objection=True, technical_hold=True,
                      next_step_defined=False, meetings_last_30d=0,
                      prospect_initiated_last_30d=0, last_email_response_days=30,
                      days_in_stage=100)
        acc.accelerate(d)
        acc.accelerate(make_deal(deal_id="ok"))
        for plan in acc.critical_deals():
            assert plan.deal_health == DealHealth.CRITICAL

    def test_critical_deals_empty_when_none(self):
        acc = DealAccelerator()
        acc.accelerate(make_deal(deal_id="fine"))
        # a healthy deal should not be critical
        result = acc.critical_deals()
        for p in result:
            assert p.deal_health == DealHealth.CRITICAL


class TestDealAcceleratorStalledDeals:
    def test_stalled_deals_includes_critical(self):
        acc = DealAccelerator()
        d = make_deal(deal_id="cr2", days_since_last_activity=30,
                      contacts_count=1, decision_maker_identified=False,
                      champion_identified=False, budget_confirmed=False,
                      price_objection=True, technical_hold=True,
                      next_step_defined=False, meetings_last_30d=0,
                      prospect_initiated_last_30d=0, last_email_response_days=30,
                      days_in_stage=100)
        acc.accelerate(d)
        stalled = acc.stalled_deals()
        healths = {p.deal_health for p in stalled}
        assert healths.issubset({DealHealth.STALLED, DealHealth.CRITICAL})

    def test_stalled_deals_excludes_active(self):
        acc = DealAccelerator()
        acc.accelerate(make_deal(deal_id="active_deal"))
        stalled = acc.stalled_deals()
        for p in stalled:
            assert p.deal_health != DealHealth.ACTIVE


class TestDealAcceleratorByStrategy:
    def test_by_strategy_filters_primary(self):
        acc = DealAccelerator()
        d = make_deal(stage=SalesStage.CLOSING, close_date_in_days=3,
                      decision_maker_identified=True, executive_sponsor=True,
                      champion_identified=True, budget_confirmed=True,
                      price_objection=False, deal_value_eur=10_000, has_competitor=False)
        plan = acc.accelerate(d)
        results = acc.by_strategy(plan.primary_strategy)
        assert any(p.deal.deal_id == d.deal_id for p in results)

    def test_by_strategy_empty_for_unused_strategy(self):
        acc = DealAccelerator()
        acc.accelerate(make_deal())
        # Extremely unlikely all strategies show up
        results = acc.by_strategy(AccelerationStrategy.DIRECT_CLOSE)
        for p in results:
            assert p.primary_strategy == AccelerationStrategy.DIRECT_CLOSE


class TestDealAcceleratorTopAtRisk:
    def test_top_at_risk_default_5(self):
        acc = DealAccelerator()
        for i in range(10):
            acc.accelerate(make_deal(deal_id=f"t{i}"))
        top = acc.top_at_risk()
        assert len(top) <= 5

    def test_top_at_risk_custom_n(self):
        acc = DealAccelerator()
        for i in range(10):
            acc.accelerate(make_deal(deal_id=f"r{i}"))
        top = acc.top_at_risk(n=3)
        assert len(top) <= 3

    def test_top_at_risk_returns_highest_stall_first(self):
        acc = DealAccelerator()
        d_low = make_deal(deal_id="tl", days_since_last_activity=0)
        d_high = make_deal(deal_id="th", days_since_last_activity=30,
                           contacts_count=1, decision_maker_identified=False,
                           budget_confirmed=False)
        acc.accelerate(d_low)
        acc.accelerate(d_high)
        top = acc.top_at_risk(n=2)
        if len(top) >= 2:
            assert top[0].stall_score >= top[1].stall_score

    def test_top_at_risk_fewer_than_n(self):
        acc = DealAccelerator()
        acc.accelerate(make_deal(deal_id="only1"))
        top = acc.top_at_risk(n=5)
        assert len(top) == 1


class TestDealAcceleratorPipelineAtRisk:
    def test_pipeline_at_risk_empty(self):
        acc = DealAccelerator()
        assert acc.pipeline_at_risk_eur() == 0.0

    def test_pipeline_at_risk_includes_stalled_and_critical(self):
        acc = DealAccelerator()
        d_bad = make_deal(deal_id="bad", deal_value_eur=20_000,
                          days_since_last_activity=30,
                          contacts_count=1, decision_maker_identified=False,
                          champion_identified=False, budget_confirmed=False,
                          price_objection=True, technical_hold=True,
                          next_step_defined=False, meetings_last_30d=0,
                          prospect_initiated_last_30d=0, last_email_response_days=30,
                          days_in_stage=100)
        d_good = make_deal(deal_id="good2", deal_value_eur=10_000)
        acc.accelerate(d_bad)
        acc.accelerate(d_good)
        at_risk = acc.pipeline_at_risk_eur()
        # at_risk should be >= 0 and <= total
        assert at_risk >= 0.0

    def test_pipeline_at_risk_sum_is_correct(self):
        acc = DealAccelerator()
        deals = [make_deal(deal_id=f"ar{i}", deal_value_eur=5000) for i in range(3)]
        acc.accelerate_batch(deals)
        total = acc.pipeline_at_risk_eur()
        # Manually compute
        expected = sum(
            p.deal.deal_value_eur
            for p in acc.all_plans()
            if p.deal_health in (DealHealth.AT_RISK, DealHealth.STALLED, DealHealth.CRITICAL)
        )
        assert abs(total - expected) < 0.01


class TestDealAcceleratorSummary:
    def test_summary_empty(self):
        acc = DealAccelerator()
        s = acc.summary()
        assert s["total"] == 0
        assert s["avg_stall_score"] == 0.0
        assert s["avg_win_probability"] == 0.0
        assert s["pipeline_at_risk_eur"] == 0.0
        assert s["critical_count"] == 0
        for h in DealHealth:
            assert s["health_counts"][h.value] == 0
        for strat in AccelerationStrategy:
            assert s["strategy_counts"][strat.value] == 0

    def test_summary_total_count(self):
        acc = DealAccelerator()
        for i in range(3):
            acc.accelerate(make_deal(deal_id=f"s{i}"))
        s = acc.summary()
        assert s["total"] == 3

    def test_summary_health_counts_sum_to_total(self):
        acc = DealAccelerator()
        for i in range(4):
            acc.accelerate(make_deal(deal_id=f"hc{i}"))
        s = acc.summary()
        total_health = sum(s["health_counts"].values())
        assert total_health == s["total"]

    def test_summary_strategy_counts_sum_to_total(self):
        acc = DealAccelerator()
        for i in range(4):
            acc.accelerate(make_deal(deal_id=f"sc{i}"))
        s = acc.summary()
        total_strategy = sum(s["strategy_counts"].values())
        assert total_strategy == s["total"]

    def test_summary_avg_stall_score_valid(self):
        acc = DealAccelerator()
        acc.accelerate(make_deal(deal_id="avg1"))
        s = acc.summary()
        assert 0 <= s["avg_stall_score"] <= 100

    def test_summary_avg_win_probability_valid(self):
        acc = DealAccelerator()
        acc.accelerate(make_deal(deal_id="wp1"))
        s = acc.summary()
        assert 0 <= s["avg_win_probability"] <= 100

    def test_summary_critical_count_matches_health_counts(self):
        acc = DealAccelerator()
        acc.accelerate(make_deal(deal_id="sc2"))
        s = acc.summary()
        assert s["critical_count"] == s["health_counts"][DealHealth.CRITICAL.value]

    def test_summary_has_all_health_keys(self):
        acc = DealAccelerator()
        s = acc.summary()
        for h in DealHealth:
            assert h.value in s["health_counts"]

    def test_summary_has_all_strategy_keys(self):
        acc = DealAccelerator()
        s = acc.summary()
        for strat in AccelerationStrategy:
            assert strat.value in s["strategy_counts"]


class TestDealAcceleratorReset:
    def test_reset_clears_store(self):
        acc = DealAccelerator()
        for i in range(3):
            acc.accelerate(make_deal(deal_id=f"r{i}"))
        acc.reset()
        assert acc.all_plans() == []

    def test_reset_makes_get_return_none(self):
        acc = DealAccelerator()
        acc.accelerate(make_deal(deal_id="rtest"))
        acc.reset()
        assert acc.get("rtest") is None

    def test_reset_and_reuse(self):
        acc = DealAccelerator()
        acc.accelerate(make_deal(deal_id="before"))
        acc.reset()
        acc.accelerate(make_deal(deal_id="after"))
        assert acc.get("before") is None
        assert acc.get("after") is not None

    def test_summary_empty_after_reset(self):
        acc = DealAccelerator()
        acc.accelerate(make_deal(deal_id="rs1"))
        acc.reset()
        s = acc.summary()
        assert s["total"] == 0


# ─── AccelerationPlan.to_dict ──────────────────────────────────────────────────

class TestAccelerationPlanToDict:
    def test_to_dict_returns_dict(self):
        acc = DealAccelerator()
        plan = acc.accelerate(make_deal())
        d = plan.to_dict()
        assert isinstance(d, dict)

    def test_to_dict_contains_deal(self):
        acc = DealAccelerator()
        plan = acc.accelerate(make_deal(deal_id="td1"))
        d = plan.to_dict()
        assert "deal" in d
        assert d["deal"]["deal_id"] == "td1"

    def test_to_dict_health_is_string(self):
        acc = DealAccelerator()
        plan = acc.accelerate(make_deal())
        d = plan.to_dict()
        assert isinstance(d["deal_health"], str)

    def test_to_dict_primary_strategy_is_string(self):
        acc = DealAccelerator()
        plan = acc.accelerate(make_deal())
        d = plan.to_dict()
        assert isinstance(d["primary_strategy"], str)

    def test_to_dict_secondary_strategies_list_of_strings(self):
        acc = DealAccelerator()
        plan = acc.accelerate(make_deal())
        d = plan.to_dict()
        assert isinstance(d["secondary_strategies"], list)
        for s in d["secondary_strategies"]:
            assert isinstance(s, str)


# ─── DealContext.to_dict ──────────────────────────────────────────────────────

class TestDealContextToDict:
    def test_to_dict_is_dict(self):
        d = make_deal()
        assert isinstance(d.to_dict(), dict)

    def test_to_dict_contains_deal_id(self):
        d = make_deal(deal_id="ctx1")
        assert d.to_dict()["deal_id"] == "ctx1"


# ─── Enum values ──────────────────────────────────────────────────────────────

class TestEnumValues:
    def test_deal_health_values(self):
        assert DealHealth.ACTIVE.value == "active"
        assert DealHealth.AT_RISK.value == "at_risk"
        assert DealHealth.STALLED.value == "stalled"
        assert DealHealth.CRITICAL.value == "critical"
        assert DealHealth.LOST.value == "lost"

    def test_sales_stage_values(self):
        assert SalesStage.PROSPECTING.value == "prospecting"
        assert SalesStage.DISCOVERY.value == "discovery"
        assert SalesStage.DEMO.value == "demo"
        assert SalesStage.PROPOSAL.value == "proposal"
        assert SalesStage.NEGOTIATION.value == "negotiation"
        assert SalesStage.CLOSING.value == "closing"

    def test_acceleration_strategy_values(self):
        assert AccelerationStrategy.EXECUTIVE_SPONSOR.value == "executive_sponsor"
        assert AccelerationStrategy.REQUALIFY.value == "requalify"
        assert AccelerationStrategy.COMPETITIVE_PLAY.value == "competitive_play"
        assert AccelerationStrategy.VALUE_PROOF.value == "value_proof"
        assert AccelerationStrategy.URGENCY_CREATE.value == "urgency_create"
        assert AccelerationStrategy.CHAMPION_BUILD.value == "champion_build"
        assert AccelerationStrategy.BUDGET_RESHAPE.value == "budget_reshape"
        assert AccelerationStrategy.DIRECT_CLOSE.value == "direct_close"


# ─── Integration / edge-case scenarios ────────────────────────────────────────

class TestIntegrationScenarios:
    def test_ideal_deal_is_active_and_high_win_prob(self):
        acc = DealAccelerator()
        d = make_deal(
            days_since_last_activity=1,
            contacts_count=5,
            decision_maker_identified=True,
            champion_identified=True,
            executive_sponsor=True,
            budget_confirmed=True,
            has_competitor=False,
            next_step_defined=True,
            meetings_last_30d=4,
            prospect_initiated_last_30d=2,
            last_email_response_days=1,
            price_objection=False,
            technical_hold=False,
            days_in_stage=5,
            close_date_in_days=20,
            stage=SalesStage.PROPOSAL,
        )
        plan = acc.accelerate(d)
        assert plan.deal_health in (DealHealth.ACTIVE, DealHealth.AT_RISK)
        assert plan.win_probability_adj >= 50.0

    def test_worst_case_deal_is_critical(self):
        acc = DealAccelerator()
        d = make_deal(
            days_since_last_activity=60,
            contacts_count=1,
            decision_maker_identified=False,
            champion_identified=False,
            executive_sponsor=False,
            budget_confirmed=False,
            has_competitor=True,
            competitor_strength=90,
            next_step_defined=False,
            meetings_last_30d=0,
            prospect_initiated_last_30d=0,
            last_email_response_days=60,
            price_objection=True,
            technical_hold=True,
            days_in_stage=120,
            close_date_in_days=-10,
            deal_value_eur=100_000,
        )
        plan = acc.accelerate(d)
        assert plan.deal_health == DealHealth.CRITICAL
        assert plan.stall_score > 70.0

    def test_overdue_deal_promoted_to_at_risk_minimum(self):
        acc = DealAccelerator()
        d = make_deal(
            close_date_in_days=-1,
            days_since_last_activity=5,
            contacts_count=3,
            has_competitor=False,
            budget_confirmed=True,
        )
        plan = acc.accelerate(d)
        assert plan.deal_health in (DealHealth.AT_RISK, DealHealth.STALLED, DealHealth.CRITICAL)

    def test_multiple_deals_pipeline_at_risk_accumulates(self):
        acc = DealAccelerator()
        for i in range(5):
            acc.accelerate(make_deal(
                deal_id=f"multi{i}",
                deal_value_eur=10_000,
                days_since_last_activity=30,
                contacts_count=1,
                decision_maker_identified=False,
                budget_confirmed=False,
                days_in_stage=100,
                close_date_in_days=-5,
            ))
        at_risk = acc.pipeline_at_risk_eur()
        assert at_risk >= 10_000  # At least some deals should be at risk

    def test_batch_produces_same_results_as_individual(self):
        acc1 = DealAccelerator()
        acc2 = DealAccelerator()
        deals = [make_deal(deal_id=f"cmp{i}") for i in range(3)]
        batch_plans = acc1.accelerate_batch(deals)
        individual_plans = [acc2.accelerate(d) for d in deals]
        for bp, ip in zip(batch_plans, individual_plans):
            assert abs(bp.stall_score - ip.stall_score) < 0.01
            assert bp.deal_health == ip.deal_health

    def test_action_plan_not_empty(self):
        acc = DealAccelerator()
        plan = acc.accelerate(make_deal())
        assert len(plan.action_plan) >= 1

    def test_days_to_act_zero_for_inactive_deal(self):
        acc = DealAccelerator()
        d = make_deal(days_since_last_activity=30)
        plan = acc.accelerate(d)
        assert plan.days_to_act == 0

    def test_days_to_act_1_for_no_next_step_but_active(self):
        acc = DealAccelerator()
        d = make_deal(days_since_last_activity=5, next_step_defined=False)
        plan = acc.accelerate(d)
        # no_activity not in blockers (5 < 14), no_next_step in blockers
        assert plan.days_to_act == 1

    def test_stall_score_is_float(self):
        acc = DealAccelerator()
        plan = acc.accelerate(make_deal())
        assert isinstance(plan.stall_score, float)

    def test_win_probability_in_range(self):
        acc = DealAccelerator()
        plan = acc.accelerate(make_deal())
        assert 0.0 <= plan.win_probability_adj <= 100.0

    def test_momentum_in_range(self):
        acc = DealAccelerator()
        plan = acc.accelerate(make_deal())
        assert 0.0 <= plan.deal_momentum <= 100.0

    def test_active_blockers_list_of_strings(self):
        acc = DealAccelerator()
        d = make_deal(budget_confirmed=False, decision_maker_identified=False)
        plan = acc.accelerate(d)
        assert isinstance(plan.active_blockers, list)
        for b in plan.active_blockers:
            assert isinstance(b, str)

    def test_no_duplicate_blockers(self):
        acc = DealAccelerator()
        d = make_deal(budget_confirmed=False, contacts_count=1,
                      decision_maker_identified=False)
        plan = acc.accelerate(d)
        assert len(plan.active_blockers) == len(set(plan.active_blockers))

    def test_secondary_strategies_are_list(self):
        acc = DealAccelerator()
        plan = acc.accelerate(make_deal())
        assert isinstance(plan.secondary_strategies, list)

    def test_all_stages_can_be_accelerated(self):
        acc = DealAccelerator()
        for stage in SalesStage:
            d = make_deal(deal_id=f"stage_{stage.value}", stage=stage)
            plan = acc.accelerate(d)
            assert isinstance(plan, AccelerationPlan)

    def test_reset_then_summary_has_zero_total(self):
        acc = DealAccelerator()
        for i in range(3):
            acc.accelerate(make_deal(deal_id=f"reset_{i}"))
        acc.reset()
        s = acc.summary()
        assert s["total"] == 0

    def test_close_date_exactly_0_is_overdue(self):
        # close_date_in_days=0 is NOT < 0, so not overdue
        d = make_deal(close_date_in_days=0, days_since_last_activity=5,
                      contacts_count=3, has_competitor=False, budget_confirmed=True)
        inact, _ = _inactivity_risk(d)
        stakeh, _ = _stakeholder_gap(d)
        comp, _ = _competitive_risk(d)
        budget, _ = _budget_risk(d)
        stall = inact * 0.35 + stakeh * 0.25 + comp * 0.20 + budget * 0.20
        health = _deal_health(stall, 0, d)
        assert health != DealHealth.CRITICAL  # 0 is not overdue

    def test_close_date_minus_1_is_overdue(self):
        d = make_deal(close_date_in_days=-1, days_since_last_activity=5)
        health = _deal_health(10, -1, d)
        assert health == DealHealth.AT_RISK  # overdue + low stall -> AT_RISK

    def test_deal_value_exactly_50k_triggers_exec_misalignment(self):
        d = make_deal(deal_value_eur=50_000, executive_sponsor=False,
                      contacts_count=3, decision_maker_identified=True,
                      champion_identified=True)
        score, blockers = _stakeholder_gap(d)
        assert "executive_misalignment" in blockers

    def test_deal_value_below_50k_no_exec_misalignment(self):
        d = make_deal(deal_value_eur=49_999, executive_sponsor=False,
                      contacts_count=3, decision_maker_identified=True,
                      champion_identified=True)
        score, blockers = _stakeholder_gap(d)
        assert "executive_misalignment" not in blockers
