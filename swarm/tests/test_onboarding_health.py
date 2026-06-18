"""
Comprehensive pytest tests for swarm/intelligence/onboarding_health.py

Covers all helper functions, enums, dataclasses, signal detection,
OnboardingHealthMonitor methods, and edge cases.
"""

from __future__ import annotations

import math
import pytest

from swarm.intelligence.onboarding_health import (
    OnboardingStatus,
    OnboardingAction,
    OnboardingInput,
    OnboardingResult,
    OnboardingHealthMonitor,
    _MILESTONE_WEIGHTS,
    _milestone_score,
    _engagement_score,
    _health_score,
    _overall_score,
    _schedule_delta,
    _onboarding_status,
    _onboarding_action,
    _build_signals,
)


# ─── Factory helper ───────────────────────────────────────────────────────────


def make_inp(
    account_id: str = "acc-001",
    account_name: str = "Test Corp",
    arr_eur: float = 50_000.0,
    contract_start_days: int = 30,
    target_go_live_days: int = 90,
    kickoff_done: bool = True,
    technical_setup_pct: float = 80.0,
    data_migration_pct: float = 70.0,
    integrations_pct: float = 60.0,
    user_training_pct: float = 50.0,
    uat_pct: float = 40.0,
    go_live_done: bool = False,
    customer_pm_engaged: bool = True,
    executive_sponsor_active: bool = True,
    dedicated_csm_assigned: bool = True,
    integration_blockers: int = 0,
    support_tickets_open: int = 0,
    days_since_last_contact: int = 2,
    nps_at_onboarding: int = -999,
) -> OnboardingInput:
    return OnboardingInput(
        account_id=account_id,
        account_name=account_name,
        arr_eur=arr_eur,
        contract_start_days=contract_start_days,
        target_go_live_days=target_go_live_days,
        kickoff_done=kickoff_done,
        technical_setup_pct=technical_setup_pct,
        data_migration_pct=data_migration_pct,
        integrations_pct=integrations_pct,
        user_training_pct=user_training_pct,
        uat_pct=uat_pct,
        go_live_done=go_live_done,
        customer_pm_engaged=customer_pm_engaged,
        executive_sponsor_active=executive_sponsor_active,
        dedicated_csm_assigned=dedicated_csm_assigned,
        integration_blockers=integration_blockers,
        support_tickets_open=support_tickets_open,
        days_since_last_contact=days_since_last_contact,
        nps_at_onboarding=nps_at_onboarding,
    )


def make_monitor(*inputs: OnboardingInput) -> OnboardingHealthMonitor:
    m = OnboardingHealthMonitor()
    for inp in inputs:
        m.assess(inp)
    return m


# ─── Class 1: OnboardingStatus enum ──────────────────────────────────────────


class TestOnboardingStatus:
    def test_on_track_value(self):
        assert OnboardingStatus.ON_TRACK.value == "on_track"

    def test_at_risk_value(self):
        assert OnboardingStatus.AT_RISK.value == "at_risk"

    def test_delayed_value(self):
        assert OnboardingStatus.DELAYED.value == "delayed"

    def test_critical_value(self):
        assert OnboardingStatus.CRITICAL.value == "critical"

    def test_is_str_enum(self):
        assert isinstance(OnboardingStatus.ON_TRACK, str)

    def test_four_members(self):
        assert len(OnboardingStatus) == 4

    def test_str_comparison(self):
        assert OnboardingStatus.ON_TRACK == "on_track"


# ─── Class 2: OnboardingAction enum ──────────────────────────────────────────


class TestOnboardingAction:
    def test_celebrate_value(self):
        assert OnboardingAction.CELEBRATE.value == "celebrate"

    def test_accelerate_value(self):
        assert OnboardingAction.ACCELERATE.value == "accelerate"

    def test_rescue_value(self):
        assert OnboardingAction.RESCUE.value == "rescue"

    def test_monitor_value(self):
        assert OnboardingAction.MONITOR.value == "monitor"

    def test_is_str_enum(self):
        assert isinstance(OnboardingAction.CELEBRATE, str)

    def test_four_members(self):
        assert len(OnboardingAction) == 4

    def test_str_comparison(self):
        assert OnboardingAction.RESCUE == "rescue"


# ─── Class 3: _MILESTONE_WEIGHTS ─────────────────────────────────────────────


class TestMilestoneWeights:
    def test_sum_to_100(self):
        assert sum(_MILESTONE_WEIGHTS.values()) == 100

    def test_kickoff_weight(self):
        assert _MILESTONE_WEIGHTS["kickoff"] == 5

    def test_technical_weight(self):
        assert _MILESTONE_WEIGHTS["technical"] == 25

    def test_migration_weight(self):
        assert _MILESTONE_WEIGHTS["migration"] == 20

    def test_integrations_weight(self):
        assert _MILESTONE_WEIGHTS["integrations"] == 20

    def test_training_weight(self):
        assert _MILESTONE_WEIGHTS["training"] == 15

    def test_uat_weight(self):
        assert _MILESTONE_WEIGHTS["uat"] == 10

    def test_go_live_weight(self):
        assert _MILESTONE_WEIGHTS["go_live"] == 5

    def test_has_seven_keys(self):
        assert len(_MILESTONE_WEIGHTS) == 7


# ─── Class 4: _milestone_score ────────────────────────────────────────────────


class TestMilestoneScore:
    def test_returns_tuple_of_two(self):
        result = _milestone_score(make_inp())
        assert isinstance(result, tuple) and len(result) == 2

    def test_both_values_equal(self):
        ms, cp = _milestone_score(make_inp())
        assert ms == cp

    def test_all_done_gives_100(self):
        inp = make_inp(
            kickoff_done=True,
            technical_setup_pct=100,
            data_migration_pct=100,
            integrations_pct=100,
            user_training_pct=100,
            uat_pct=100,
            go_live_done=True,
        )
        ms, _ = _milestone_score(inp)
        assert ms == 100.0

    def test_nothing_done_gives_0(self):
        inp = make_inp(
            kickoff_done=False,
            technical_setup_pct=0,
            data_migration_pct=0,
            integrations_pct=0,
            user_training_pct=0,
            uat_pct=0,
            go_live_done=False,
        )
        ms, _ = _milestone_score(inp)
        assert ms == 0.0

    def test_only_kickoff_done(self):
        inp = make_inp(
            kickoff_done=True,
            technical_setup_pct=0,
            data_migration_pct=0,
            integrations_pct=0,
            user_training_pct=0,
            uat_pct=0,
            go_live_done=False,
        )
        ms, _ = _milestone_score(inp)
        # 100 * 5 / 100 = 5.0
        assert ms == 5.0

    def test_only_go_live_done(self):
        inp = make_inp(
            kickoff_done=False,
            technical_setup_pct=0,
            data_migration_pct=0,
            integrations_pct=0,
            user_training_pct=0,
            uat_pct=0,
            go_live_done=True,
        )
        ms, _ = _milestone_score(inp)
        # 100 * 5 / 100 = 5.0
        assert ms == 5.0

    def test_technical_only_at_100(self):
        inp = make_inp(
            kickoff_done=False,
            technical_setup_pct=100,
            data_migration_pct=0,
            integrations_pct=0,
            user_training_pct=0,
            uat_pct=0,
            go_live_done=False,
        )
        ms, _ = _milestone_score(inp)
        # 100 * 25 / 100 = 25.0
        assert ms == 25.0

    def test_clamps_technical_above_100(self):
        inp = make_inp(technical_setup_pct=150)
        inp2 = make_inp(technical_setup_pct=100)
        assert _milestone_score(inp) == _milestone_score(inp2)

    def test_clamps_migration_below_0(self):
        inp = make_inp(data_migration_pct=-10)
        inp2 = make_inp(data_migration_pct=0)
        assert _milestone_score(inp) == _milestone_score(inp2)

    def test_partial_scenario(self):
        inp = make_inp(
            kickoff_done=True,
            technical_setup_pct=50,
            data_migration_pct=0,
            integrations_pct=0,
            user_training_pct=0,
            uat_pct=0,
            go_live_done=False,
        )
        # (100*5 + 50*25) / 100 = (500 + 1250) / 100 = 17.5
        ms, _ = _milestone_score(inp)
        assert ms == pytest.approx(17.5, abs=0.01)

    def test_score_in_range_0_100(self):
        inp = make_inp(technical_setup_pct=75, data_migration_pct=80, integrations_pct=60)
        ms, _ = _milestone_score(inp)
        assert 0 <= ms <= 100

    def test_returns_floats(self):
        ms, cp = _milestone_score(make_inp())
        assert isinstance(ms, float) and isinstance(cp, float)

    def test_weighted_calculation(self):
        inp = make_inp(
            kickoff_done=True,      # 100 * 5 = 500
            technical_setup_pct=80, # 80 * 25 = 2000
            data_migration_pct=60,  # 60 * 20 = 1200
            integrations_pct=40,    # 40 * 20 = 800
            user_training_pct=20,   # 20 * 15 = 300
            uat_pct=10,             # 10 * 10 = 100
            go_live_done=False,     # 0 * 5 = 0
        )
        # total = (500+2000+1200+800+300+100+0)/100 = 4900/100 = 49.0
        ms, _ = _milestone_score(inp)
        assert ms == pytest.approx(49.0, abs=0.01)


# ─── Class 5: _engagement_score ──────────────────────────────────────────────


class TestEngagementScore:
    def test_all_positive_max_contact(self):
        inp = make_inp(
            customer_pm_engaged=True,
            executive_sponsor_active=True,
            dedicated_csm_assigned=True,
            days_since_last_contact=1,
        )
        # 35+30+25+10 = 100
        assert _engagement_score(inp) == 100.0

    def test_nothing_engaged_no_contact(self):
        inp = make_inp(
            customer_pm_engaged=False,
            executive_sponsor_active=False,
            dedicated_csm_assigned=False,
            days_since_last_contact=20,
        )
        # 0 - 15 = -15 → clamped to 0
        assert _engagement_score(inp) == 0.0

    def test_customer_pm_adds_35(self):
        base = make_inp(
            customer_pm_engaged=False,
            executive_sponsor_active=False,
            dedicated_csm_assigned=False,
            days_since_last_contact=8,  # no contact bonus/penalty
        )
        with_pm = make_inp(
            customer_pm_engaged=True,
            executive_sponsor_active=False,
            dedicated_csm_assigned=False,
            days_since_last_contact=8,
        )
        assert _engagement_score(with_pm) - _engagement_score(base) == pytest.approx(35.0)

    def test_exec_sponsor_adds_30(self):
        base = make_inp(
            customer_pm_engaged=False,
            executive_sponsor_active=False,
            dedicated_csm_assigned=False,
            days_since_last_contact=8,
        )
        with_exec = make_inp(
            customer_pm_engaged=False,
            executive_sponsor_active=True,
            dedicated_csm_assigned=False,
            days_since_last_contact=8,
        )
        assert _engagement_score(with_exec) - _engagement_score(base) == pytest.approx(30.0)

    def test_csm_adds_25(self):
        base = make_inp(
            customer_pm_engaged=False,
            executive_sponsor_active=False,
            dedicated_csm_assigned=False,
            days_since_last_contact=8,
        )
        with_csm = make_inp(
            customer_pm_engaged=False,
            executive_sponsor_active=False,
            dedicated_csm_assigned=True,
            days_since_last_contact=8,
        )
        assert _engagement_score(with_csm) - _engagement_score(base) == pytest.approx(25.0)

    def test_contact_within_3_days_adds_10(self):
        base = make_inp(
            customer_pm_engaged=False,
            executive_sponsor_active=False,
            dedicated_csm_assigned=False,
            days_since_last_contact=8,
        )
        recent = make_inp(
            customer_pm_engaged=False,
            executive_sponsor_active=False,
            dedicated_csm_assigned=False,
            days_since_last_contact=3,
        )
        assert _engagement_score(recent) - _engagement_score(base) == pytest.approx(10.0)

    def test_contact_exactly_3_days_adds_10(self):
        inp = make_inp(
            customer_pm_engaged=False,
            executive_sponsor_active=False,
            dedicated_csm_assigned=False,
            days_since_last_contact=3,
        )
        assert _engagement_score(inp) == 10.0

    def test_contact_4_to_7_days_adds_5(self):
        base = make_inp(
            customer_pm_engaged=False,
            executive_sponsor_active=False,
            dedicated_csm_assigned=False,
            days_since_last_contact=8,
        )
        mid = make_inp(
            customer_pm_engaged=False,
            executive_sponsor_active=False,
            dedicated_csm_assigned=False,
            days_since_last_contact=7,
        )
        assert _engagement_score(mid) - _engagement_score(base) == pytest.approx(5.0)

    def test_contact_exactly_7_days_adds_5(self):
        inp = make_inp(
            customer_pm_engaged=False,
            executive_sponsor_active=False,
            dedicated_csm_assigned=False,
            days_since_last_contact=7,
        )
        assert _engagement_score(inp) == 5.0

    def test_contact_above_14_days_subtracts_15(self):
        inp = make_inp(
            customer_pm_engaged=False,
            executive_sponsor_active=False,
            dedicated_csm_assigned=False,
            days_since_last_contact=15,
        )
        # 0 - 15 = -15 → clamped to 0
        assert _engagement_score(inp) == 0.0

    def test_score_clamped_above_100(self):
        # All positives + extra still max 100
        inp = make_inp(
            customer_pm_engaged=True,
            executive_sponsor_active=True,
            dedicated_csm_assigned=True,
            days_since_last_contact=1,
        )
        assert _engagement_score(inp) <= 100.0

    def test_score_clamped_at_0(self):
        inp = make_inp(
            customer_pm_engaged=False,
            executive_sponsor_active=False,
            dedicated_csm_assigned=False,
            days_since_last_contact=30,
        )
        assert _engagement_score(inp) == 0.0

    def test_returns_float(self):
        assert isinstance(_engagement_score(make_inp()), (int, float))

    def test_no_penalty_8_to_14_days(self):
        # days_since_last_contact=10 is between 7 and 14 — no bonus, no penalty
        inp = make_inp(
            customer_pm_engaged=False,
            executive_sponsor_active=False,
            dedicated_csm_assigned=False,
            days_since_last_contact=10,
        )
        assert _engagement_score(inp) == 0.0

    def test_contact_exactly_14_days_no_penalty(self):
        inp = make_inp(
            customer_pm_engaged=False,
            executive_sponsor_active=False,
            dedicated_csm_assigned=False,
            days_since_last_contact=14,
        )
        assert _engagement_score(inp) == 0.0

    def test_all_engaged_contact_4_to_7(self):
        inp = make_inp(
            customer_pm_engaged=True,
            executive_sponsor_active=True,
            dedicated_csm_assigned=True,
            days_since_last_contact=5,
        )
        # 35+30+25+5 = 95
        assert _engagement_score(inp) == 95.0


# ─── Class 6: _health_score ──────────────────────────────────────────────────


class TestHealthScore:
    def test_perfect_health_no_nps(self):
        inp = make_inp(
            integration_blockers=0,
            support_tickets_open=0,
            days_since_last_contact=5,
            nps_at_onboarding=-999,
        )
        assert _health_score(inp) == 100.0

    def test_one_integration_blocker(self):
        inp = make_inp(
            integration_blockers=1,
            support_tickets_open=0,
            days_since_last_contact=5,
            nps_at_onboarding=-999,
        )
        assert _health_score(inp) == pytest.approx(85.0)

    def test_two_integration_blockers(self):
        inp = make_inp(
            integration_blockers=2,
            support_tickets_open=0,
            days_since_last_contact=5,
            nps_at_onboarding=-999,
        )
        assert _health_score(inp) == pytest.approx(70.0)

    def test_three_integration_blockers_capped_at_45(self):
        inp = make_inp(
            integration_blockers=3,
            support_tickets_open=0,
            days_since_last_contact=5,
            nps_at_onboarding=-999,
        )
        # 3*15=45, capped at 45
        assert _health_score(inp) == pytest.approx(55.0)

    def test_four_integration_blockers_still_45_penalty(self):
        inp3 = make_inp(
            integration_blockers=3,
            support_tickets_open=0,
            days_since_last_contact=5,
            nps_at_onboarding=-999,
        )
        inp4 = make_inp(
            integration_blockers=4,
            support_tickets_open=0,
            days_since_last_contact=5,
            nps_at_onboarding=-999,
        )
        assert _health_score(inp3) == _health_score(inp4)

    def test_one_support_ticket(self):
        inp = make_inp(
            integration_blockers=0,
            support_tickets_open=1,
            days_since_last_contact=5,
            nps_at_onboarding=-999,
        )
        assert _health_score(inp) == pytest.approx(95.0)

    def test_five_support_tickets_capped_at_25(self):
        inp = make_inp(
            integration_blockers=0,
            support_tickets_open=5,
            days_since_last_contact=5,
            nps_at_onboarding=-999,
        )
        # 5*5=25, capped at 25
        assert _health_score(inp) == pytest.approx(75.0)

    def test_six_support_tickets_still_25_penalty(self):
        inp5 = make_inp(
            integration_blockers=0,
            support_tickets_open=5,
            days_since_last_contact=5,
            nps_at_onboarding=-999,
        )
        inp6 = make_inp(
            integration_blockers=0,
            support_tickets_open=6,
            days_since_last_contact=5,
            nps_at_onboarding=-999,
        )
        assert _health_score(inp5) == _health_score(inp6)

    def test_contact_above_14_days_penalty_15(self):
        inp = make_inp(
            integration_blockers=0,
            support_tickets_open=0,
            days_since_last_contact=15,
            nps_at_onboarding=-999,
        )
        assert _health_score(inp) == pytest.approx(85.0)

    def test_contact_exactly_14_days_no_penalty(self):
        inp = make_inp(
            integration_blockers=0,
            support_tickets_open=0,
            days_since_last_contact=14,
            nps_at_onboarding=-999,
        )
        # <=14 and >7 → -5
        assert _health_score(inp) == pytest.approx(95.0)

    def test_contact_8_to_14_days_penalty_5(self):
        inp = make_inp(
            integration_blockers=0,
            support_tickets_open=0,
            days_since_last_contact=8,
            nps_at_onboarding=-999,
        )
        assert _health_score(inp) == pytest.approx(95.0)

    def test_nps_below_minus10_penalty_20(self):
        inp = make_inp(
            integration_blockers=0,
            support_tickets_open=0,
            days_since_last_contact=5,
            nps_at_onboarding=-50,
        )
        assert _health_score(inp) == pytest.approx(80.0)

    def test_nps_exactly_minus10_penalty_20(self):
        inp = make_inp(
            integration_blockers=0,
            support_tickets_open=0,
            days_since_last_contact=5,
            nps_at_onboarding=-10,
        )
        # -10 < 0 but >= -10 → penalty 10
        assert _health_score(inp) == pytest.approx(90.0)

    def test_nps_between_minus10_and_0_penalty_10(self):
        inp = make_inp(
            integration_blockers=0,
            support_tickets_open=0,
            days_since_last_contact=5,
            nps_at_onboarding=-5,
        )
        assert _health_score(inp) == pytest.approx(90.0)

    def test_nps_0_no_effect(self):
        inp = make_inp(
            integration_blockers=0,
            support_tickets_open=0,
            days_since_last_contact=5,
            nps_at_onboarding=0,
        )
        # nps == 0 → not < -10, not < 0, not > 30 → no effect
        assert _health_score(inp) == pytest.approx(100.0)

    def test_nps_above_30_bonus_10(self):
        inp = make_inp(
            integration_blockers=0,
            support_tickets_open=0,
            days_since_last_contact=5,
            nps_at_onboarding=50,
        )
        # 100 + 10 = 110 → clamped to 100
        assert _health_score(inp) == 100.0

    def test_nps_exactly_30_no_bonus(self):
        inp = make_inp(
            integration_blockers=0,
            support_tickets_open=0,
            days_since_last_contact=5,
            nps_at_onboarding=30,
        )
        # 30 is not > 30 → no bonus
        assert _health_score(inp) == pytest.approx(100.0)

    def test_nps_sentinel_not_applied(self):
        with_sentinel = make_inp(nps_at_onboarding=-999)
        without_nps = make_inp(nps_at_onboarding=-999)
        assert _health_score(with_sentinel) == _health_score(without_nps)

    def test_score_clamped_at_0(self):
        # Max penalties: 45 + 25 + 15 + 20 = 105 → clamped to 0
        inp = make_inp(
            integration_blockers=10,
            support_tickets_open=10,
            days_since_last_contact=30,
            nps_at_onboarding=-100,
        )
        assert _health_score(inp) == 0.0

    def test_returns_float(self):
        assert isinstance(_health_score(make_inp()), (int, float))

    def test_combined_penalties_and_bonus(self):
        inp = make_inp(
            integration_blockers=1,   # -15
            support_tickets_open=0,
            days_since_last_contact=5,
            nps_at_onboarding=50,     # +10
        )
        # 100 - 15 + 10 = 95
        assert _health_score(inp) == pytest.approx(95.0)


# ─── Class 7: _overall_score ─────────────────────────────────────────────────


class TestOverallScore:
    def test_all_100(self):
        assert _overall_score(100.0, 100.0, 100.0) == 100.0

    def test_all_0(self):
        assert _overall_score(0.0, 0.0, 0.0) == 0.0

    def test_weighting_milestone_55(self):
        assert _overall_score(100.0, 0.0, 0.0) == pytest.approx(55.0)

    def test_weighting_engagement_25(self):
        assert _overall_score(0.0, 100.0, 0.0) == pytest.approx(25.0)

    def test_weighting_health_20(self):
        assert _overall_score(0.0, 0.0, 100.0) == pytest.approx(20.0)

    def test_weights_sum_to_100(self):
        assert _overall_score(100.0, 100.0, 100.0) == pytest.approx(100.0)

    def test_typical_scenario(self):
        # 60*0.55 + 70*0.25 + 80*0.20 = 33+17.5+16 = 66.5
        result = _overall_score(60.0, 70.0, 80.0)
        assert result == pytest.approx(66.5)

    def test_returns_float(self):
        assert isinstance(_overall_score(50.0, 50.0, 50.0), float)

    def test_rounded_to_2_decimals(self):
        result = _overall_score(33.33, 33.33, 33.33)
        assert result == round(result, 2)


# ─── Class 8: _schedule_delta ─────────────────────────────────────────────────


class TestScheduleDelta:
    def test_zero_target_returns_0(self):
        inp = make_inp(target_go_live_days=0, contract_start_days=10)
        assert _schedule_delta(inp, 50.0) == 0.0

    def test_negative_target_returns_0(self):
        inp = make_inp(target_go_live_days=-5, contract_start_days=10)
        assert _schedule_delta(inp, 50.0) == 0.0

    def test_on_schedule(self):
        # 30/90 = 33.3%, completion=33.3 → delta ≈ 0
        inp = make_inp(contract_start_days=30, target_go_live_days=90)
        delta = _schedule_delta(inp, 33.3)
        assert delta == pytest.approx(0.0, abs=0.5)

    def test_ahead_of_schedule(self):
        # expected = 30/90*100 = 33.3%, completion=60 → delta=26.7
        inp = make_inp(contract_start_days=30, target_go_live_days=90)
        delta = _schedule_delta(inp, 60.0)
        assert delta > 0

    def test_behind_schedule(self):
        # expected = 60/90*100 = 66.7%, completion=30 → delta=-36.7
        inp = make_inp(contract_start_days=60, target_go_live_days=90)
        delta = _schedule_delta(inp, 30.0)
        assert delta < 0

    def test_expected_capped_at_100(self):
        # start_days > target: expected_pct would be >100 → clamped to 100
        inp = make_inp(contract_start_days=120, target_go_live_days=90)
        delta = _schedule_delta(inp, 80.0)
        # expected=100, delta=80-100=-20
        assert delta == pytest.approx(-20.0, abs=0.1)

    def test_returns_float(self):
        inp = make_inp(contract_start_days=10, target_go_live_days=90)
        assert isinstance(_schedule_delta(inp, 50.0), float)

    def test_rounding(self):
        inp = make_inp(contract_start_days=1, target_go_live_days=3)
        # expected = 33.333...%, completion=0 → delta=-33.3 rounded to 1 decimal
        delta = _schedule_delta(inp, 0.0)
        assert delta == round(delta, 1)


# ─── Class 9: _onboarding_status ─────────────────────────────────────────────


class TestOnboardingStatus_Function:
    def test_75_is_on_track(self):
        assert _onboarding_status(75.0) == OnboardingStatus.ON_TRACK

    def test_100_is_on_track(self):
        assert _onboarding_status(100.0) == OnboardingStatus.ON_TRACK

    def test_74_9_is_at_risk(self):
        assert _onboarding_status(74.9) == OnboardingStatus.AT_RISK

    def test_50_is_at_risk(self):
        assert _onboarding_status(50.0) == OnboardingStatus.AT_RISK

    def test_49_9_is_delayed(self):
        assert _onboarding_status(49.9) == OnboardingStatus.DELAYED

    def test_25_is_delayed(self):
        assert _onboarding_status(25.0) == OnboardingStatus.DELAYED

    def test_24_9_is_critical(self):
        assert _onboarding_status(24.9) == OnboardingStatus.CRITICAL

    def test_0_is_critical(self):
        assert _onboarding_status(0.0) == OnboardingStatus.CRITICAL

    def test_exactly_50_at_risk(self):
        assert _onboarding_status(50.0) == OnboardingStatus.AT_RISK

    def test_exactly_25_delayed(self):
        assert _onboarding_status(25.0) == OnboardingStatus.DELAYED


# ─── Class 10: _onboarding_action ────────────────────────────────────────────


class TestOnboardingAction_Function:
    def test_go_live_done_celebrates_regardless_critical(self):
        inp = make_inp(go_live_done=True)
        assert _onboarding_action(inp, OnboardingStatus.CRITICAL, -50.0) == OnboardingAction.CELEBRATE

    def test_go_live_done_celebrates_regardless_at_risk(self):
        inp = make_inp(go_live_done=True)
        assert _onboarding_action(inp, OnboardingStatus.AT_RISK, 0.0) == OnboardingAction.CELEBRATE

    def test_go_live_done_celebrates_regardless_on_track(self):
        inp = make_inp(go_live_done=True)
        assert _onboarding_action(inp, OnboardingStatus.ON_TRACK, 10.0) == OnboardingAction.CELEBRATE

    def test_critical_status_rescues(self):
        inp = make_inp(go_live_done=False)
        assert _onboarding_action(inp, OnboardingStatus.CRITICAL, 0.0) == OnboardingAction.RESCUE

    def test_at_risk_accelerates(self):
        inp = make_inp(go_live_done=False)
        assert _onboarding_action(inp, OnboardingStatus.AT_RISK, 0.0) == OnboardingAction.ACCELERATE

    def test_delayed_accelerates(self):
        inp = make_inp(go_live_done=False)
        assert _onboarding_action(inp, OnboardingStatus.DELAYED, 0.0) == OnboardingAction.ACCELERATE

    def test_on_track_delta_minus_11_accelerates(self):
        inp = make_inp(go_live_done=False)
        assert _onboarding_action(inp, OnboardingStatus.ON_TRACK, -11.0) == OnboardingAction.ACCELERATE

    def test_on_track_delta_exactly_minus_10_monitors(self):
        inp = make_inp(go_live_done=False)
        assert _onboarding_action(inp, OnboardingStatus.ON_TRACK, -10.0) == OnboardingAction.MONITOR

    def test_on_track_delta_positive_monitors(self):
        inp = make_inp(go_live_done=False)
        assert _onboarding_action(inp, OnboardingStatus.ON_TRACK, 5.0) == OnboardingAction.MONITOR

    def test_on_track_delta_0_monitors(self):
        inp = make_inp(go_live_done=False)
        assert _onboarding_action(inp, OnboardingStatus.ON_TRACK, 0.0) == OnboardingAction.MONITOR


# ─── Class 11: _build_signals ────────────────────────────────────────────────


class TestBuildSignals:
    def _call(self, inp, completion=50.0, delta=0.0, days_remaining=30):
        return _build_signals(inp, completion, delta, days_remaining)

    # Blockers
    def test_integration_blockers_in_blockers(self):
        inp = make_inp(integration_blockers=2)
        blockers, _, _ = self._call(inp)
        assert any("2" in b and "intégration" in b for b in blockers)

    def test_support_tickets_in_blockers(self):
        inp = make_inp(support_tickets_open=3)
        blockers, _, _ = self._call(inp)
        assert any("3" in b and "ticket" in b for b in blockers)

    def test_kickoff_not_done_in_blockers(self):
        inp = make_inp(kickoff_done=False)
        blockers, _, _ = self._call(inp)
        assert any("Kickoff non effectué" in b for b in blockers)

    def test_kickoff_done_not_in_blockers(self):
        inp = make_inp(kickoff_done=True)
        blockers, _, _ = self._call(inp)
        assert not any("Kickoff non effectué" in b for b in blockers)

    def test_technical_setup_low_after_14_days(self):
        inp = make_inp(technical_setup_pct=30, contract_start_days=20)
        blockers, _, _ = self._call(inp)
        assert any("Configuration technique" in b for b in blockers)

    def test_technical_setup_not_in_blockers_before_14_days(self):
        inp = make_inp(technical_setup_pct=30, contract_start_days=10)
        blockers, _, _ = self._call(inp)
        assert not any("Configuration technique" in b for b in blockers)

    def test_technical_setup_50_not_in_blockers(self):
        inp = make_inp(technical_setup_pct=50, contract_start_days=20)
        blockers, _, _ = self._call(inp)
        assert not any("Configuration technique" in b for b in blockers)

    def test_migration_low_after_21_days(self):
        inp = make_inp(data_migration_pct=20, contract_start_days=25)
        blockers, _, _ = self._call(inp)
        assert any("Migration données" in b for b in blockers)

    def test_migration_not_in_blockers_before_21_days(self):
        inp = make_inp(data_migration_pct=20, contract_start_days=15)
        blockers, _, _ = self._call(inp)
        assert not any("Migration données" in b for b in blockers)

    def test_delta_minus_25_in_blockers(self):
        inp = make_inp()
        blockers, _, _ = self._call(inp, delta=-25.0)
        assert any("Retard" in b for b in blockers)

    def test_delta_minus_20_not_in_blockers(self):
        inp = make_inp()
        blockers, _, _ = self._call(inp, delta=-20.0)
        assert not any("Retard" in b for b in blockers)

    def test_negative_days_remaining_in_blockers(self):
        inp = make_inp()
        blockers, _, _ = self._call(inp, days_remaining=-5)
        assert any("Go-live en retard" in b for b in blockers)

    def test_positive_days_remaining_not_in_blockers(self):
        inp = make_inp()
        blockers, _, _ = self._call(inp, days_remaining=10)
        assert not any("Go-live en retard" in b for b in blockers)

    def test_no_customer_pm_in_blockers(self):
        inp = make_inp(customer_pm_engaged=False)
        blockers, _, _ = self._call(inp)
        assert any("chef de projet" in b for b in blockers)

    def test_with_customer_pm_not_in_blockers(self):
        inp = make_inp(customer_pm_engaged=True)
        blockers, _, _ = self._call(inp)
        assert not any("chef de projet" in b for b in blockers)

    def test_no_contact_15_days_in_blockers(self):
        inp = make_inp(days_since_last_contact=15)
        blockers, _, _ = self._call(inp)
        assert any("Aucun contact" in b for b in blockers)

    def test_contact_14_days_not_in_blockers(self):
        inp = make_inp(days_since_last_contact=14)
        blockers, _, _ = self._call(inp)
        assert not any("Aucun contact" in b for b in blockers)

    # Achievements
    def test_go_live_done_in_achievements(self):
        inp = make_inp(go_live_done=True)
        _, achievements, _ = self._call(inp)
        assert any("Go-live complété" in a for a in achievements)

    def test_kickoff_done_in_achievements(self):
        inp = make_inp(kickoff_done=True)
        _, achievements, _ = self._call(inp)
        assert any("Kickoff effectué" in a for a in achievements)

    def test_technical_90_in_achievements(self):
        inp = make_inp(technical_setup_pct=90)
        _, achievements, _ = self._call(inp)
        assert any("Configuration technique quasi-complète" in a for a in achievements)

    def test_technical_89_not_in_achievements(self):
        inp = make_inp(technical_setup_pct=89)
        _, achievements, _ = self._call(inp)
        assert not any("Configuration technique quasi-complète" in a for a in achievements)

    def test_migration_90_in_achievements(self):
        inp = make_inp(data_migration_pct=90)
        _, achievements, _ = self._call(inp)
        assert any("Migration données quasi-complète" in a for a in achievements)

    def test_training_80_in_achievements(self):
        inp = make_inp(user_training_pct=80)
        _, achievements, _ = self._call(inp)
        assert any("Formation utilisateurs" in a for a in achievements)

    def test_exec_sponsor_in_achievements(self):
        inp = make_inp(executive_sponsor_active=True)
        _, achievements, _ = self._call(inp)
        assert any("Sponsor exécutif" in a for a in achievements)

    def test_csm_in_achievements(self):
        inp = make_inp(dedicated_csm_assigned=True)
        _, achievements, _ = self._call(inp)
        assert any("CSM dédié" in a for a in achievements)

    def test_ahead_of_schedule_in_achievements(self):
        inp = make_inp()
        _, achievements, _ = self._call(inp, delta=15.0)
        assert any("En avance" in a for a in achievements)

    def test_delta_exactly_10_not_in_achievements(self):
        inp = make_inp()
        _, achievements, _ = self._call(inp, delta=10.0)
        assert not any("En avance" in a for a in achievements)

    def test_nps_above_30_in_achievements(self):
        inp = make_inp(nps_at_onboarding=50)
        _, achievements, _ = self._call(inp)
        assert any("NPS onboarding positif" in a for a in achievements)

    def test_nps_exactly_30_not_in_achievements(self):
        inp = make_inp(nps_at_onboarding=30)
        _, achievements, _ = self._call(inp)
        assert not any("NPS onboarding positif" in a for a in achievements)

    def test_nps_sentinel_not_in_achievements(self):
        inp = make_inp(nps_at_onboarding=-999)
        _, achievements, _ = self._call(inp)
        assert not any("NPS onboarding positif" in a for a in achievements)

    # Recommended actions
    def test_integration_blockers_in_actions(self):
        inp = make_inp(integration_blockers=1)
        _, _, actions = self._call(inp)
        assert any("Résoudre en urgence" in a for a in actions)

    def test_kickoff_not_done_in_actions(self):
        inp = make_inp(kickoff_done=False)
        _, _, actions = self._call(inp)
        assert any("Planifier le kickoff" in a for a in actions)

    def test_technical_below_30_in_actions(self):
        inp = make_inp(technical_setup_pct=20)
        _, _, actions = self._call(inp)
        assert any("Escalader la configuration technique" in a for a in actions)

    def test_technical_exactly_30_not_in_actions(self):
        inp = make_inp(technical_setup_pct=30)
        _, _, actions = self._call(inp)
        assert not any("Escalader la configuration technique" in a for a in actions)

    def test_migration_below_30_after_14_days_in_actions(self):
        inp = make_inp(data_migration_pct=20, contract_start_days=20)
        _, _, actions = self._call(inp)
        assert any("Lancer la migration" in a for a in actions)

    def test_migration_below_30_before_14_days_not_in_actions(self):
        inp = make_inp(data_migration_pct=20, contract_start_days=10)
        _, _, actions = self._call(inp)
        assert not any("Lancer la migration" in a for a in actions)

    def test_no_customer_pm_in_actions(self):
        inp = make_inp(customer_pm_engaged=False)
        _, _, actions = self._call(inp)
        assert any("Demander la désignation" in a for a in actions)

    def test_no_exec_sponsor_in_actions(self):
        inp = make_inp(executive_sponsor_active=False)
        _, _, actions = self._call(inp)
        assert any("Activer le sponsor exécutif" in a for a in actions)

    def test_no_contact_8_days_in_actions(self):
        inp = make_inp(days_since_last_contact=8)
        _, _, actions = self._call(inp)
        assert any("Reprendre contact" in a for a in actions)

    def test_contact_7_days_not_in_actions(self):
        inp = make_inp(days_since_last_contact=7)
        _, _, actions = self._call(inp)
        assert not any("Reprendre contact" in a for a in actions)

    def test_training_low_uat_high_in_actions(self):
        inp = make_inp(user_training_pct=40, uat_pct=60)
        _, _, actions = self._call(inp)
        assert any("formation avant UAT" in a for a in actions)

    def test_training_50_uat_high_not_in_actions(self):
        inp = make_inp(user_training_pct=50, uat_pct=60)
        _, _, actions = self._call(inp)
        assert not any("formation avant UAT" in a for a in actions)

    def test_days_remaining_10_in_actions(self):
        inp = make_inp()
        _, _, actions = self._call(inp, days_remaining=10)
        assert any("Intensifier le rythme" in a for a in actions)

    def test_days_remaining_0_not_in_actions(self):
        inp = make_inp()
        _, _, actions = self._call(inp, days_remaining=0)
        assert not any("Intensifier le rythme" in a for a in actions)

    def test_days_remaining_15_not_in_actions(self):
        inp = make_inp()
        _, _, actions = self._call(inp, days_remaining=15)
        assert not any("Intensifier le rythme" in a for a in actions)

    def test_go_live_done_in_actions(self):
        inp = make_inp(go_live_done=True)
        _, _, actions = self._call(inp)
        assert any("revue post-onboarding" in a for a in actions)

    def test_returns_three_lists(self):
        result = self._call(make_inp())
        assert len(result) == 3
        assert all(isinstance(x, list) for x in result)


# ─── Class 12: OnboardingResult.to_dict ──────────────────────────────────────


class TestOnboardingResultToDict:
    def _get_result(self):
        m = OnboardingHealthMonitor()
        return m.assess(make_inp())

    def test_to_dict_returns_dict(self):
        assert isinstance(self._get_result().to_dict(), dict)

    def test_onboarding_status_is_string(self):
        d = self._get_result().to_dict()
        assert isinstance(d["onboarding_status"], str)

    def test_onboarding_action_is_string(self):
        d = self._get_result().to_dict()
        assert isinstance(d["onboarding_action"], str)

    def test_onboarding_status_value(self):
        result = self._get_result()
        d = result.to_dict()
        assert d["onboarding_status"] == result.onboarding_status.value

    def test_onboarding_action_value(self):
        result = self._get_result()
        d = result.to_dict()
        assert d["onboarding_action"] == result.onboarding_action.value

    def test_contains_expected_keys(self):
        d = self._get_result().to_dict()
        for key in [
            "account_id", "account_name", "arr_eur", "onboarding_status",
            "onboarding_action", "overall_score", "milestone_score",
            "engagement_score", "health_score", "completion_pct",
            "days_remaining", "schedule_delta_pct", "blockers",
            "achievements", "recommended_actions", "go_live_done"
        ]:
            assert key in d

    def test_blockers_is_list(self):
        d = self._get_result().to_dict()
        assert isinstance(d["blockers"], list)

    def test_achievements_is_list(self):
        d = self._get_result().to_dict()
        assert isinstance(d["achievements"], list)

    def test_recommended_actions_is_list(self):
        d = self._get_result().to_dict()
        assert isinstance(d["recommended_actions"], list)

    def test_critical_status_string(self):
        m = OnboardingHealthMonitor()
        inp = make_inp(
            kickoff_done=False,
            technical_setup_pct=0,
            data_migration_pct=0,
            integrations_pct=0,
            user_training_pct=0,
            uat_pct=0,
            customer_pm_engaged=False,
            executive_sponsor_active=False,
            dedicated_csm_assigned=False,
            days_since_last_contact=30,
            nps_at_onboarding=-50,
            integration_blockers=5,
        )
        result = m.assess(inp)
        d = result.to_dict()
        assert d["onboarding_status"] == "critical"


# ─── Class 13: OnboardingHealthMonitor.assess ─────────────────────────────────


class TestMonitorAssess:
    def test_returns_onboarding_result(self):
        m = OnboardingHealthMonitor()
        result = m.assess(make_inp())
        assert isinstance(result, OnboardingResult)

    def test_account_id_preserved(self):
        m = OnboardingHealthMonitor()
        result = m.assess(make_inp(account_id="xyz-123"))
        assert result.account_id == "xyz-123"

    def test_account_name_preserved(self):
        m = OnboardingHealthMonitor()
        result = m.assess(make_inp(account_name="Acme Ltd"))
        assert result.account_name == "Acme Ltd"

    def test_arr_eur_preserved(self):
        m = OnboardingHealthMonitor()
        result = m.assess(make_inp(arr_eur=99_000.0))
        assert result.arr_eur == 99_000.0

    def test_go_live_done_preserved(self):
        m = OnboardingHealthMonitor()
        result = m.assess(make_inp(go_live_done=True))
        assert result.go_live_done is True

    def test_days_remaining_calculation(self):
        m = OnboardingHealthMonitor()
        result = m.assess(make_inp(target_go_live_days=90, contract_start_days=30))
        assert result.days_remaining == 60

    def test_days_remaining_negative_when_overdue(self):
        m = OnboardingHealthMonitor()
        result = m.assess(make_inp(target_go_live_days=60, contract_start_days=80))
        assert result.days_remaining == -20

    def test_overall_score_in_range(self):
        m = OnboardingHealthMonitor()
        result = m.assess(make_inp())
        assert 0 <= result.overall_score <= 100

    def test_on_track_status_for_good_account(self):
        m = OnboardingHealthMonitor()
        inp = make_inp(
            kickoff_done=True,
            technical_setup_pct=90,
            data_migration_pct=85,
            integrations_pct=80,
            user_training_pct=75,
            uat_pct=70,
            go_live_done=False,
            customer_pm_engaged=True,
            executive_sponsor_active=True,
            dedicated_csm_assigned=True,
            days_since_last_contact=2,
            nps_at_onboarding=50,
            integration_blockers=0,
            support_tickets_open=0,
        )
        result = m.assess(inp)
        assert result.onboarding_status == OnboardingStatus.ON_TRACK

    def test_critical_status_for_bad_account(self):
        m = OnboardingHealthMonitor()
        inp = make_inp(
            kickoff_done=False,
            technical_setup_pct=0,
            data_migration_pct=0,
            integrations_pct=0,
            user_training_pct=0,
            uat_pct=0,
            customer_pm_engaged=False,
            executive_sponsor_active=False,
            dedicated_csm_assigned=False,
            days_since_last_contact=30,
            nps_at_onboarding=-50,
            integration_blockers=5,
            support_tickets_open=5,
        )
        result = m.assess(inp)
        assert result.onboarding_status == OnboardingStatus.CRITICAL

    def test_celebrate_action_when_go_live_done(self):
        m = OnboardingHealthMonitor()
        result = m.assess(make_inp(go_live_done=True))
        assert result.onboarding_action == OnboardingAction.CELEBRATE

    def test_stored_in_results(self):
        m = OnboardingHealthMonitor()
        inp = make_inp(account_id="store-test")
        m.assess(inp)
        assert m.get("store-test") is not None

    def test_overwrite_existing_account(self):
        m = OnboardingHealthMonitor()
        m.assess(make_inp(account_id="same-id", arr_eur=10_000))
        m.assess(make_inp(account_id="same-id", arr_eur=99_000))
        assert m.get("same-id").arr_eur == 99_000

    def test_milestone_score_field(self):
        m = OnboardingHealthMonitor()
        result = m.assess(make_inp())
        assert isinstance(result.milestone_score, float)

    def test_engagement_score_field(self):
        m = OnboardingHealthMonitor()
        result = m.assess(make_inp())
        assert isinstance(result.engagement_score, (int, float))

    def test_health_score_field(self):
        m = OnboardingHealthMonitor()
        result = m.assess(make_inp())
        assert isinstance(result.health_score, (int, float))

    def test_completion_pct_equals_milestone_score(self):
        m = OnboardingHealthMonitor()
        result = m.assess(make_inp())
        assert result.completion_pct == result.milestone_score


# ─── Class 14: OnboardingHealthMonitor.assess_batch ──────────────────────────


class TestMonitorAssessBatch:
    def test_returns_list(self):
        m = OnboardingHealthMonitor()
        result = m.assess_batch([make_inp()])
        assert isinstance(result, list)

    def test_sorted_worst_first(self):
        m = OnboardingHealthMonitor()
        good = make_inp(
            account_id="good",
            technical_setup_pct=100,
            data_migration_pct=100,
            customer_pm_engaged=True,
            executive_sponsor_active=True,
            dedicated_csm_assigned=True,
        )
        bad = make_inp(
            account_id="bad",
            kickoff_done=False,
            technical_setup_pct=0,
            data_migration_pct=0,
            integrations_pct=0,
            user_training_pct=0,
            uat_pct=0,
            customer_pm_engaged=False,
            executive_sponsor_active=False,
            dedicated_csm_assigned=False,
        )
        results = m.assess_batch([good, bad])
        assert results[0].account_id == "bad"
        assert results[1].account_id == "good"

    def test_empty_list_returns_empty(self):
        m = OnboardingHealthMonitor()
        assert m.assess_batch([]) == []

    def test_all_stored(self):
        m = OnboardingHealthMonitor()
        inputs = [make_inp(account_id=f"acc-{i}") for i in range(3)]
        m.assess_batch(inputs)
        for i in range(3):
            assert m.get(f"acc-{i}") is not None

    def test_ascending_order(self):
        m = OnboardingHealthMonitor()
        inputs = [make_inp(account_id=f"b{i}") for i in range(5)]
        results = m.assess_batch(inputs)
        scores = [r.overall_score for r in results]
        assert scores == sorted(scores)


# ─── Class 15: OnboardingHealthMonitor query methods ─────────────────────────


class TestMonitorQueryMethods:
    def _make_populated_monitor(self):
        m = OnboardingHealthMonitor()
        # Good (ON_TRACK likely)
        m.assess(make_inp(
            account_id="good-1",
            arr_eur=100_000,
            kickoff_done=True,
            technical_setup_pct=95,
            data_migration_pct=90,
            integrations_pct=85,
            user_training_pct=80,
            uat_pct=75,
            go_live_done=False,
            customer_pm_engaged=True,
            executive_sponsor_active=True,
            dedicated_csm_assigned=True,
            days_since_last_contact=1,
            nps_at_onboarding=50,
            integration_blockers=0,
            support_tickets_open=0,
        ))
        # Critical
        m.assess(make_inp(
            account_id="critical-1",
            arr_eur=20_000,
            kickoff_done=False,
            technical_setup_pct=0,
            data_migration_pct=0,
            integrations_pct=0,
            user_training_pct=0,
            uat_pct=0,
            go_live_done=False,
            customer_pm_engaged=False,
            executive_sponsor_active=False,
            dedicated_csm_assigned=False,
            days_since_last_contact=30,
            nps_at_onboarding=-50,
            integration_blockers=5,
            support_tickets_open=5,
        ))
        # Completed
        m.assess(make_inp(
            account_id="done-1",
            arr_eur=75_000,
            go_live_done=True,
            kickoff_done=True,
            technical_setup_pct=100,
            data_migration_pct=100,
            integrations_pct=100,
            user_training_pct=100,
            uat_pct=100,
            customer_pm_engaged=True,
            executive_sponsor_active=True,
            dedicated_csm_assigned=True,
            days_since_last_contact=1,
        ))
        # Overdue
        m.assess(make_inp(
            account_id="overdue-1",
            arr_eur=30_000,
            contract_start_days=100,
            target_go_live_days=90,
            go_live_done=False,
            kickoff_done=True,
            technical_setup_pct=50,
            data_migration_pct=40,
            integrations_pct=30,
            customer_pm_engaged=True,
            executive_sponsor_active=False,
            dedicated_csm_assigned=True,
            days_since_last_contact=5,
        ))
        return m

    def test_get_existing(self):
        m = self._make_populated_monitor()
        assert m.get("good-1") is not None

    def test_get_missing_returns_none(self):
        m = OnboardingHealthMonitor()
        assert m.get("nonexistent") is None

    def test_all_accounts_returns_list(self):
        m = self._make_populated_monitor()
        assert isinstance(m.all_accounts(), list)

    def test_all_accounts_sorted_asc(self):
        m = self._make_populated_monitor()
        scores = [r.overall_score for r in m.all_accounts()]
        assert scores == sorted(scores)

    def test_critical_contains_critical_only(self):
        m = self._make_populated_monitor()
        for r in m.critical():
            assert r.onboarding_status == OnboardingStatus.CRITICAL

    def test_critical_includes_expected(self):
        m = self._make_populated_monitor()
        ids = [r.account_id for r in m.critical()]
        assert "critical-1" in ids

    def test_at_risk_contains_critical_and_at_risk(self):
        m = self._make_populated_monitor()
        for r in m.at_risk():
            assert r.onboarding_status in (OnboardingStatus.CRITICAL, OnboardingStatus.AT_RISK)

    def test_on_track_contains_on_track_only(self):
        m = self._make_populated_monitor()
        for r in m.on_track():
            assert r.onboarding_status == OnboardingStatus.ON_TRACK

    def test_needs_rescue_contains_rescue_only(self):
        m = self._make_populated_monitor()
        for r in m.needs_rescue():
            assert r.onboarding_action == OnboardingAction.RESCUE

    def test_completed_go_live_done_true(self):
        m = self._make_populated_monitor()
        for r in m.completed():
            assert r.go_live_done is True

    def test_completed_includes_done_account(self):
        m = self._make_populated_monitor()
        ids = [r.account_id for r in m.completed()]
        assert "done-1" in ids

    def test_overdue_has_negative_days_remaining(self):
        m = self._make_populated_monitor()
        for r in m.overdue():
            assert r.days_remaining < 0
            assert r.go_live_done is False

    def test_overdue_includes_overdue_account(self):
        m = self._make_populated_monitor()
        ids = [r.account_id for r in m.overdue()]
        assert "overdue-1" in ids

    def test_by_status_filter(self):
        m = self._make_populated_monitor()
        results = m.by_status(OnboardingStatus.CRITICAL)
        for r in results:
            assert r.onboarding_status == OnboardingStatus.CRITICAL

    def test_empty_monitor_all_accounts(self):
        m = OnboardingHealthMonitor()
        assert m.all_accounts() == []

    def test_empty_monitor_critical(self):
        m = OnboardingHealthMonitor()
        assert m.critical() == []

    def test_empty_monitor_at_risk(self):
        m = OnboardingHealthMonitor()
        assert m.at_risk() == []

    def test_empty_monitor_on_track(self):
        m = OnboardingHealthMonitor()
        assert m.on_track() == []

    def test_empty_monitor_completed(self):
        m = OnboardingHealthMonitor()
        assert m.completed() == []

    def test_empty_monitor_overdue(self):
        m = OnboardingHealthMonitor()
        assert m.overdue() == []

    def test_empty_monitor_needs_rescue(self):
        m = OnboardingHealthMonitor()
        assert m.needs_rescue() == []


# ─── Class 16: OnboardingHealthMonitor aggregate methods ──────────────────────


class TestMonitorAggregates:
    def test_total_arr_at_risk_eur_empty(self):
        m = OnboardingHealthMonitor()
        assert m.total_arr_at_risk_eur() == 0.0

    def test_total_arr_at_risk_eur_sums_at_risk_only(self):
        m = OnboardingHealthMonitor()
        # Critical account → at_risk
        m.assess(make_inp(
            account_id="crit",
            arr_eur=10_000,
            kickoff_done=False,
            technical_setup_pct=0,
            data_migration_pct=0,
            integrations_pct=0,
            user_training_pct=0,
            uat_pct=0,
            customer_pm_engaged=False,
            executive_sponsor_active=False,
            dedicated_csm_assigned=False,
            days_since_last_contact=30,
            nps_at_onboarding=-50,
            integration_blockers=5,
        ))
        # Good account → should not be included
        m.assess(make_inp(
            account_id="good",
            arr_eur=50_000,
            kickoff_done=True,
            technical_setup_pct=95,
            data_migration_pct=90,
            integrations_pct=85,
            user_training_pct=80,
            uat_pct=75,
            customer_pm_engaged=True,
            executive_sponsor_active=True,
            dedicated_csm_assigned=True,
            days_since_last_contact=1,
            nps_at_onboarding=50,
            integration_blockers=0,
        ))
        arr = m.total_arr_at_risk_eur()
        assert arr == pytest.approx(10_000.0)

    def test_avg_completion_pct_empty(self):
        m = OnboardingHealthMonitor()
        assert m.avg_completion_pct() == 0.0

    def test_avg_completion_pct_single(self):
        m = OnboardingHealthMonitor()
        m.assess(make_inp(
            kickoff_done=True,
            technical_setup_pct=100,
            data_migration_pct=100,
            integrations_pct=100,
            user_training_pct=100,
            uat_pct=100,
            go_live_done=True,
        ))
        assert m.avg_completion_pct() == 100.0

    def test_avg_completion_pct_multiple(self):
        m = OnboardingHealthMonitor()
        m.assess(make_inp(
            account_id="a1",
            kickoff_done=True,
            technical_setup_pct=100,
            data_migration_pct=100,
            integrations_pct=100,
            user_training_pct=100,
            uat_pct=100,
            go_live_done=True,
        ))
        m.assess(make_inp(
            account_id="a2",
            kickoff_done=False,
            technical_setup_pct=0,
            data_migration_pct=0,
            integrations_pct=0,
            user_training_pct=0,
            uat_pct=0,
            go_live_done=False,
        ))
        avg = m.avg_completion_pct()
        assert 0 < avg < 100


# ─── Class 17: OnboardingHealthMonitor.summary ───────────────────────────────


class TestMonitorSummary:
    def test_empty_summary(self):
        m = OnboardingHealthMonitor()
        s = m.summary()
        assert s["total"] == 0
        assert s["status_counts"] == {}
        assert s["action_counts"] == {}
        assert s["avg_completion_pct"] == 0.0
        assert s["avg_overall_score"] == 0.0
        assert s["critical_count"] == 0
        assert s["overdue_count"] == 0
        assert s["completed_count"] == 0
        assert s["total_arr_at_risk_eur"] == 0.0

    def test_summary_total_count(self):
        m = OnboardingHealthMonitor()
        for i in range(5):
            m.assess(make_inp(account_id=f"s{i}"))
        assert m.summary()["total"] == 5

    def test_summary_has_all_keys(self):
        m = OnboardingHealthMonitor()
        m.assess(make_inp())
        s = m.summary()
        for key in [
            "total", "status_counts", "action_counts", "avg_completion_pct",
            "avg_overall_score", "critical_count", "overdue_count",
            "completed_count", "total_arr_at_risk_eur"
        ]:
            assert key in s

    def test_summary_status_counts_strings(self):
        m = OnboardingHealthMonitor()
        m.assess(make_inp())
        for k in m.summary()["status_counts"]:
            assert isinstance(k, str)

    def test_summary_action_counts_strings(self):
        m = OnboardingHealthMonitor()
        m.assess(make_inp())
        for k in m.summary()["action_counts"]:
            assert isinstance(k, str)

    def test_summary_critical_count(self):
        m = OnboardingHealthMonitor()
        m.assess(make_inp(
            account_id="crit",
            kickoff_done=False,
            technical_setup_pct=0,
            data_migration_pct=0,
            integrations_pct=0,
            user_training_pct=0,
            uat_pct=0,
            customer_pm_engaged=False,
            executive_sponsor_active=False,
            dedicated_csm_assigned=False,
            days_since_last_contact=30,
            nps_at_onboarding=-50,
            integration_blockers=5,
        ))
        assert m.summary()["critical_count"] >= 1

    def test_summary_completed_count(self):
        m = OnboardingHealthMonitor()
        m.assess(make_inp(account_id="done", go_live_done=True))
        assert m.summary()["completed_count"] == 1

    def test_summary_avg_overall_score_in_range(self):
        m = OnboardingHealthMonitor()
        for i in range(3):
            m.assess(make_inp(account_id=f"t{i}"))
        score = m.summary()["avg_overall_score"]
        assert 0 <= score <= 100


# ─── Class 18: OnboardingHealthMonitor.reset ──────────────────────────────────


class TestMonitorReset:
    def test_reset_clears_results(self):
        m = OnboardingHealthMonitor()
        m.assess(make_inp(account_id="x"))
        m.reset()
        assert m.get("x") is None

    def test_reset_empties_all_accounts(self):
        m = OnboardingHealthMonitor()
        for i in range(5):
            m.assess(make_inp(account_id=f"r{i}"))
        m.reset()
        assert m.all_accounts() == []

    def test_reset_allows_reassess(self):
        m = OnboardingHealthMonitor()
        m.assess(make_inp(account_id="y"))
        m.reset()
        m.assess(make_inp(account_id="y", arr_eur=12345))
        assert m.get("y").arr_eur == 12345

    def test_reset_summary_empty(self):
        m = OnboardingHealthMonitor()
        m.assess(make_inp())
        m.reset()
        assert m.summary()["total"] == 0

    def test_double_reset_safe(self):
        m = OnboardingHealthMonitor()
        m.reset()
        m.reset()
        assert m.all_accounts() == []


# ─── Class 19: Integration / End-to-End scenarios ────────────────────────────


class TestEndToEndScenarios:
    def test_perfect_onboarding_on_track(self):
        m = OnboardingHealthMonitor()
        inp = make_inp(
            kickoff_done=True,
            technical_setup_pct=100,
            data_migration_pct=100,
            integrations_pct=100,
            user_training_pct=100,
            uat_pct=100,
            go_live_done=False,
            customer_pm_engaged=True,
            executive_sponsor_active=True,
            dedicated_csm_assigned=True,
            days_since_last_contact=1,
            nps_at_onboarding=50,
            integration_blockers=0,
            support_tickets_open=0,
        )
        result = m.assess(inp)
        assert result.onboarding_status == OnboardingStatus.ON_TRACK
        assert result.overall_score >= 75

    def test_go_live_completed_celebrates(self):
        m = OnboardingHealthMonitor()
        inp = make_inp(
            go_live_done=True,
            kickoff_done=True,
            technical_setup_pct=100,
            data_migration_pct=100,
            integrations_pct=100,
            user_training_pct=100,
            uat_pct=100,
            customer_pm_engaged=True,
            executive_sponsor_active=True,
            dedicated_csm_assigned=True,
            days_since_last_contact=1,
        )
        result = m.assess(inp)
        assert result.onboarding_action == OnboardingAction.CELEBRATE
        assert result.go_live_done is True

    def test_full_blown_rescue_scenario(self):
        m = OnboardingHealthMonitor()
        inp = make_inp(
            kickoff_done=False,
            technical_setup_pct=0,
            data_migration_pct=0,
            integrations_pct=0,
            user_training_pct=0,
            uat_pct=0,
            go_live_done=False,
            customer_pm_engaged=False,
            executive_sponsor_active=False,
            dedicated_csm_assigned=False,
            days_since_last_contact=30,
            nps_at_onboarding=-50,
            integration_blockers=5,
            support_tickets_open=5,
        )
        result = m.assess(inp)
        assert result.onboarding_status == OnboardingStatus.CRITICAL
        assert result.onboarding_action == OnboardingAction.RESCUE
        assert len(result.blockers) > 0

    def test_overdue_account_detected(self):
        m = OnboardingHealthMonitor()
        inp = make_inp(
            account_id="overdue",
            contract_start_days=100,
            target_go_live_days=90,
            go_live_done=False,
            kickoff_done=True,
            technical_setup_pct=70,
            data_migration_pct=60,
            integrations_pct=50,
            customer_pm_engaged=True,
            executive_sponsor_active=True,
            dedicated_csm_assigned=True,
            days_since_last_contact=3,
        )
        m.assess(inp)
        assert len(m.overdue()) >= 1
        assert any(r.account_id == "overdue" for r in m.overdue())

    def test_schedule_delta_reflected_in_result(self):
        m = OnboardingHealthMonitor()
        inp = make_inp(
            kickoff_done=True,
            technical_setup_pct=100,
            data_migration_pct=100,
            integrations_pct=100,
            user_training_pct=100,
            uat_pct=100,
            go_live_done=False,
            contract_start_days=30,
            target_go_live_days=90,
        )
        result = m.assess(inp)
        # completion_pct should be high, expected=33.3 → delta positive (ahead)
        assert result.schedule_delta_pct > 0

    def test_multiple_accounts_all_accessible(self):
        m = OnboardingHealthMonitor()
        ids = [f"acc-{i}" for i in range(10)]
        for i, acc_id in enumerate(ids):
            m.assess(make_inp(account_id=acc_id))
        assert len(m.all_accounts()) == 10
        for acc_id in ids:
            assert m.get(acc_id) is not None

    def test_arr_at_risk_sums_correctly(self):
        m = OnboardingHealthMonitor()
        # Create 2 critical accounts
        for i in range(2):
            m.assess(make_inp(
                account_id=f"crit-{i}",
                arr_eur=5_000.0,
                kickoff_done=False,
                technical_setup_pct=0,
                data_migration_pct=0,
                integrations_pct=0,
                user_training_pct=0,
                uat_pct=0,
                customer_pm_engaged=False,
                executive_sponsor_active=False,
                dedicated_csm_assigned=False,
                days_since_last_contact=30,
                nps_at_onboarding=-50,
                integration_blockers=5,
            ))
        at_risk_arr = m.total_arr_at_risk_eur()
        assert at_risk_arr == pytest.approx(10_000.0)

    def test_assess_batch_and_query_consistent(self):
        m = OnboardingHealthMonitor()
        inputs = [make_inp(account_id=f"batch-{i}") for i in range(5)]
        m.assess_batch(inputs)
        assert len(m.all_accounts()) == 5

    def test_no_blockers_for_perfect_account(self):
        m = OnboardingHealthMonitor()
        inp = make_inp(
            kickoff_done=True,
            technical_setup_pct=100,
            data_migration_pct=100,
            integrations_pct=100,
            user_training_pct=100,
            uat_pct=100,
            go_live_done=False,
            customer_pm_engaged=True,
            executive_sponsor_active=True,
            dedicated_csm_assigned=True,
            days_since_last_contact=1,
            nps_at_onboarding=50,
            integration_blockers=0,
            support_tickets_open=0,
            contract_start_days=30,
            target_go_live_days=90,
        )
        result = m.assess(inp)
        assert result.blockers == []
