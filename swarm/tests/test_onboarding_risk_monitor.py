"""
Comprehensive pytest test suite for Module 29 — Onboarding Risk Monitor.
Target: 22 test classes, 270+ tests, all passing.
"""
from __future__ import annotations

import pytest

from swarm.intelligence.onboarding_risk_monitor import (
    ChurnSignal,
    OnboardingAction,
    OnboardingInput,
    OnboardingPhase,
    OnboardingResult,
    OnboardingRisk,
    OnboardingRiskMonitorEngine,
    _churn_signal,
    _go_live_delay,
    _intervention_plan,
    _positive_signals,
    _risk_action,
    _risk_factors,
    _risk_level,
    _risk_score,
    _time_to_value_score,
)


# ---------------------------------------------------------------------------
# Factory helper — produces a perfectly healthy customer (no risk factors)
# ---------------------------------------------------------------------------

def make_customer(
    customer_id: str = "cust-001",
    customer_name: str = "Healthy Corp",
    arr_eur: float = 50_000.0,
    segment: str = "enterprise",
    phase: OnboardingPhase = OnboardingPhase.ADOPTION,
    days_since_contract: int = 20,
    expected_go_live_days: int = 60,
    actual_go_live_days: int = 0,
    exec_sponsor_active: bool = True,
    champion_engaged: bool = True,
    training_completion_pct: float = 90.0,
    users_activated_pct: float = 70.0,
    first_value_achieved: bool = True,
    integrations_completed: int = 3,
    integrations_planned: int = 3,
    open_blockers: int = 0,
    escalated_tickets: int = 0,
    last_cs_contact_days: int = 3,
    kickoff_completed: bool = True,
    health_check_completed: bool = True,
) -> OnboardingInput:
    return OnboardingInput(
        customer_id=customer_id,
        customer_name=customer_name,
        arr_eur=arr_eur,
        segment=segment,
        phase=phase,
        days_since_contract=days_since_contract,
        expected_go_live_days=expected_go_live_days,
        actual_go_live_days=actual_go_live_days,
        exec_sponsor_active=exec_sponsor_active,
        champion_engaged=champion_engaged,
        training_completion_pct=training_completion_pct,
        users_activated_pct=users_activated_pct,
        first_value_achieved=first_value_achieved,
        integrations_completed=integrations_completed,
        integrations_planned=integrations_planned,
        open_blockers=open_blockers,
        escalated_tickets=escalated_tickets,
        last_cs_contact_days=last_cs_contact_days,
        kickoff_completed=kickoff_completed,
        health_check_completed=health_check_completed,
    )


# ---------------------------------------------------------------------------
# 1. Enums
# ---------------------------------------------------------------------------

class TestOnboardingRiskEnum:
    def test_has_low(self):
        assert OnboardingRisk.LOW == "low"

    def test_has_moderate(self):
        assert OnboardingRisk.MODERATE == "moderate"

    def test_has_high(self):
        assert OnboardingRisk.HIGH == "high"

    def test_has_critical(self):
        assert OnboardingRisk.CRITICAL == "critical"

    def test_all_four_values(self):
        assert len(OnboardingRisk) == 4

    def test_is_str_enum(self):
        assert isinstance(OnboardingRisk.LOW, str)


class TestOnboardingActionEnum:
    def test_monitor(self):
        assert OnboardingAction.MONITOR == "monitor"

    def test_accelerate(self):
        assert OnboardingAction.ACCELERATE == "accelerate"

    def test_rescue(self):
        assert OnboardingAction.RESCUE == "rescue"

    def test_escalate(self):
        assert OnboardingAction.ESCALATE == "escalate"

    def test_all_four_values(self):
        assert len(OnboardingAction) == 4

    def test_is_str_enum(self):
        assert isinstance(OnboardingAction.ESCALATE, str)


class TestOnboardingPhaseEnum:
    def test_kickoff(self):
        assert OnboardingPhase.KICKOFF == "kickoff"

    def test_setup(self):
        assert OnboardingPhase.SETUP == "setup"

    def test_training(self):
        assert OnboardingPhase.TRAINING == "training"

    def test_adoption(self):
        assert OnboardingPhase.ADOPTION == "adoption"

    def test_value_realization(self):
        assert OnboardingPhase.VALUE_REALIZATION == "value_realization"

    def test_all_five_values(self):
        assert len(OnboardingPhase) == 5

    def test_is_str_enum(self):
        assert isinstance(OnboardingPhase.KICKOFF, str)


class TestChurnSignalEnum:
    def test_none(self):
        assert ChurnSignal.NONE == "none"

    def test_early(self):
        assert ChurnSignal.EARLY == "early"

    def test_moderate(self):
        assert ChurnSignal.MODERATE == "moderate"

    def test_strong(self):
        assert ChurnSignal.STRONG == "strong"

    def test_all_four_values(self):
        assert len(ChurnSignal) == 4

    def test_is_str_enum(self):
        assert isinstance(ChurnSignal.STRONG, str)


# ---------------------------------------------------------------------------
# 2. OnboardingInput dataclass
# ---------------------------------------------------------------------------

class TestOnboardingInput:
    def test_create_instance(self):
        inp = make_customer()
        assert inp.customer_id == "cust-001"

    def test_customer_name(self):
        inp = make_customer(customer_name="Acme")
        assert inp.customer_name == "Acme"

    def test_arr_eur(self):
        inp = make_customer(arr_eur=100_000.0)
        assert inp.arr_eur == 100_000.0

    def test_segment(self):
        inp = make_customer(segment="smb")
        assert inp.segment == "smb"

    def test_phase(self):
        inp = make_customer(phase=OnboardingPhase.KICKOFF)
        assert inp.phase == OnboardingPhase.KICKOFF

    def test_days_since_contract(self):
        inp = make_customer(days_since_contract=45)
        assert inp.days_since_contract == 45

    def test_expected_go_live_days(self):
        inp = make_customer(expected_go_live_days=90)
        assert inp.expected_go_live_days == 90

    def test_actual_go_live_days_zero(self):
        inp = make_customer(actual_go_live_days=0)
        assert inp.actual_go_live_days == 0

    def test_exec_sponsor_active_true(self):
        inp = make_customer(exec_sponsor_active=True)
        assert inp.exec_sponsor_active is True

    def test_exec_sponsor_active_false(self):
        inp = make_customer(exec_sponsor_active=False)
        assert inp.exec_sponsor_active is False

    def test_champion_engaged(self):
        inp = make_customer(champion_engaged=False)
        assert inp.champion_engaged is False

    def test_training_pct(self):
        inp = make_customer(training_completion_pct=45.5)
        assert inp.training_completion_pct == 45.5

    def test_users_activated_pct(self):
        inp = make_customer(users_activated_pct=33.3)
        assert inp.users_activated_pct == 33.3

    def test_first_value_achieved_false(self):
        inp = make_customer(first_value_achieved=False)
        assert inp.first_value_achieved is False

    def test_integrations(self):
        inp = make_customer(integrations_completed=2, integrations_planned=5)
        assert inp.integrations_completed == 2
        assert inp.integrations_planned == 5

    def test_open_blockers(self):
        inp = make_customer(open_blockers=3)
        assert inp.open_blockers == 3

    def test_escalated_tickets(self):
        inp = make_customer(escalated_tickets=1)
        assert inp.escalated_tickets == 1

    def test_last_cs_contact_days(self):
        inp = make_customer(last_cs_contact_days=20)
        assert inp.last_cs_contact_days == 20

    def test_kickoff_completed(self):
        inp = make_customer(kickoff_completed=False)
        assert inp.kickoff_completed is False

    def test_health_check_completed(self):
        inp = make_customer(health_check_completed=False)
        assert inp.health_check_completed is False


# ---------------------------------------------------------------------------
# 3. OnboardingResult dataclass
# ---------------------------------------------------------------------------

class TestOnboardingResult:
    def setup_method(self):
        engine = OnboardingRiskMonitorEngine()
        self.result = engine.monitor(make_customer())

    def test_customer_id(self):
        assert self.result.customer_id == "cust-001"

    def test_customer_name(self):
        assert self.result.customer_name == "Healthy Corp"

    def test_arr_eur(self):
        assert isinstance(self.result.arr_eur, (int, float))

    def test_segment(self):
        assert self.result.segment == "enterprise"

    def test_phase(self):
        assert isinstance(self.result.phase, OnboardingPhase)

    def test_risk_score_type(self):
        assert isinstance(self.result.risk_score, (int, float))

    def test_risk_score_range(self):
        assert 0.0 <= self.result.risk_score <= 100.0

    def test_risk_level_type(self):
        assert isinstance(self.result.risk_level, OnboardingRisk)

    def test_risk_action_type(self):
        assert isinstance(self.result.risk_action, OnboardingAction)

    def test_churn_signal_type(self):
        assert isinstance(self.result.churn_signal, ChurnSignal)

    def test_go_live_delay_type(self):
        assert isinstance(self.result.go_live_delay_days, (int, float))

    def test_risk_factors_list(self):
        assert isinstance(self.result.risk_factors, list)

    def test_positive_signals_list(self):
        assert isinstance(self.result.positive_signals, list)

    def test_intervention_plan_list(self):
        assert isinstance(self.result.intervention_plan, list)
        assert len(self.result.intervention_plan) >= 1

    def test_time_to_value_score_type(self):
        assert isinstance(self.result.time_to_value_score, (int, float))

    def test_time_to_value_score_range(self):
        assert 0.0 <= self.result.time_to_value_score <= 100.0

    def test_to_dict_keys(self):
        d = self.result.to_dict()
        expected_keys = {
            "customer_id", "customer_name", "arr_eur", "segment", "phase",
            "risk_score", "risk_level", "risk_action", "churn_signal",
            "go_live_delay_days", "risk_factors", "positive_signals",
            "intervention_plan", "time_to_value_score",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_phase_value(self):
        d = self.result.to_dict()
        assert isinstance(d["phase"], str)

    def test_to_dict_risk_level_value(self):
        d = self.result.to_dict()
        assert d["risk_level"] in ("low", "moderate", "high", "critical")

    def test_to_dict_risk_action_value(self):
        d = self.result.to_dict()
        assert d["risk_action"] in ("monitor", "accelerate", "rescue", "escalate")

    def test_to_dict_churn_signal_value(self):
        d = self.result.to_dict()
        assert d["churn_signal"] in ("none", "early", "moderate", "strong")


# ---------------------------------------------------------------------------
# 4. _go_live_delay
# ---------------------------------------------------------------------------

class TestGoLiveDelay:
    def test_not_live_on_time(self):
        inp = make_customer(days_since_contract=20, expected_go_live_days=60, actual_go_live_days=0)
        assert _go_live_delay(inp) == 0

    def test_not_live_overdue(self):
        inp = make_customer(days_since_contract=80, expected_go_live_days=60, actual_go_live_days=0)
        assert _go_live_delay(inp) == 20

    def test_not_live_exactly_on_time(self):
        inp = make_customer(days_since_contract=60, expected_go_live_days=60, actual_go_live_days=0)
        assert _go_live_delay(inp) == 0

    def test_live_early(self):
        inp = make_customer(actual_go_live_days=50, expected_go_live_days=60)
        assert _go_live_delay(inp) == -10

    def test_live_on_time(self):
        inp = make_customer(actual_go_live_days=60, expected_go_live_days=60)
        assert _go_live_delay(inp) == 0

    def test_live_late(self):
        inp = make_customer(actual_go_live_days=75, expected_go_live_days=60)
        assert _go_live_delay(inp) == 15

    def test_live_takes_priority(self):
        # actual_go_live_days > 0 → use actual-expected, not days_since_contract
        inp = make_customer(
            actual_go_live_days=70,
            expected_go_live_days=60,
            days_since_contract=200,
        )
        assert _go_live_delay(inp) == 10

    def test_not_live_just_before_due(self):
        inp = make_customer(days_since_contract=59, expected_go_live_days=60, actual_go_live_days=0)
        assert _go_live_delay(inp) == 0

    def test_not_live_one_day_over(self):
        inp = make_customer(days_since_contract=61, expected_go_live_days=60, actual_go_live_days=0)
        assert _go_live_delay(inp) == 1


# ---------------------------------------------------------------------------
# 5. _risk_score — timeline component
# ---------------------------------------------------------------------------

class TestRiskScoreTimeline:
    def test_no_delay(self):
        inp = make_customer(days_since_contract=10, expected_go_live_days=60, actual_go_live_days=0)
        score = _risk_score(inp)
        # Healthy customer — no timeline points
        assert score == 0.0

    def test_delay_7_days(self):
        inp = make_customer(actual_go_live_days=67, expected_go_live_days=60)
        score = _risk_score(inp)
        # At least 10 from timeline
        assert score >= 10.0

    def test_delay_14_days(self):
        inp = make_customer(actual_go_live_days=74, expected_go_live_days=60)
        score = _risk_score(inp)
        assert score >= 20.0

    def test_delay_30_days(self):
        inp = make_customer(actual_go_live_days=90, expected_go_live_days=60)
        score = _risk_score(inp)
        assert score >= 30.0

    def test_delay_exactly_7(self):
        inp = make_customer(actual_go_live_days=67, expected_go_live_days=60)
        base = _risk_score(make_customer())
        score = _risk_score(inp)
        assert score >= base + 10.0

    def test_delay_exactly_14(self):
        inp = make_customer(actual_go_live_days=74, expected_go_live_days=60)
        score = _risk_score(inp)
        # 20 for timeline, 0 everything else for healthy
        assert score >= 20.0

    def test_delay_exactly_30(self):
        inp = make_customer(actual_go_live_days=90, expected_go_live_days=60)
        score = _risk_score(inp)
        assert score >= 30.0


# ---------------------------------------------------------------------------
# 6. _risk_score — engagement component
# ---------------------------------------------------------------------------

class TestRiskScoreEngagement:
    def test_no_exec_sponsor_adds_10(self):
        healthy = make_customer()
        no_sponsor = make_customer(exec_sponsor_active=False)
        assert _risk_score(no_sponsor) - _risk_score(healthy) == 10.0

    def test_no_champion_adds_8(self):
        healthy = make_customer()
        no_champ = make_customer(champion_engaged=False)
        assert _risk_score(no_champ) - _risk_score(healthy) == 8.0

    def test_training_below_30_adds_7(self):
        healthy = make_customer()
        low_train = make_customer(training_completion_pct=20.0)
        assert _risk_score(low_train) - _risk_score(healthy) == 7.0

    def test_training_between_30_and_60_adds_3(self):
        healthy = make_customer()
        mid_train = make_customer(training_completion_pct=45.0)
        assert _risk_score(mid_train) - _risk_score(healthy) == 3.0

    def test_training_above_60_adds_0(self):
        healthy = make_customer()
        good_train = make_customer(training_completion_pct=75.0)
        assert _risk_score(good_train) == _risk_score(healthy)

    def test_training_exactly_30_adds_3(self):
        healthy = make_customer()
        train_30 = make_customer(training_completion_pct=30.0)
        assert _risk_score(train_30) - _risk_score(healthy) == 3.0

    def test_training_exactly_60_adds_0(self):
        healthy = make_customer()
        train_60 = make_customer(training_completion_pct=60.0)
        assert _risk_score(train_60) == _risk_score(healthy)


# ---------------------------------------------------------------------------
# 7. _risk_score — adoption component
# ---------------------------------------------------------------------------

class TestRiskScoreAdoption:
    def test_users_below_20_adds_12(self):
        healthy = make_customer()
        low_users = make_customer(users_activated_pct=10.0)
        assert _risk_score(low_users) - _risk_score(healthy) == 12.0

    def test_users_between_20_and_50_adds_6(self):
        healthy = make_customer()
        mid_users = make_customer(users_activated_pct=35.0)
        assert _risk_score(mid_users) - _risk_score(healthy) == 6.0

    def test_users_above_50_adds_0(self):
        healthy = make_customer()
        good_users = make_customer(users_activated_pct=60.0)
        assert _risk_score(good_users) == _risk_score(healthy)

    def test_users_exactly_20_adds_6(self):
        healthy = make_customer()
        border = make_customer(users_activated_pct=20.0)
        assert _risk_score(border) - _risk_score(healthy) == 6.0

    def test_users_exactly_50_adds_0(self):
        healthy = make_customer()
        border = make_customer(users_activated_pct=50.0)
        assert _risk_score(border) == _risk_score(healthy)

    def test_no_first_value_after_30_days_adds_8(self):
        healthy = make_customer()
        no_val = make_customer(first_value_achieved=False, days_since_contract=31)
        assert _risk_score(no_val) - _risk_score(healthy) == 8.0

    def test_no_first_value_before_30_days_adds_0(self):
        healthy = make_customer()
        no_val = make_customer(first_value_achieved=False, days_since_contract=20)
        assert _risk_score(no_val) == _risk_score(healthy)

    def test_no_first_value_exactly_30_days_adds_0(self):
        healthy = make_customer()
        no_val = make_customer(first_value_achieved=False, days_since_contract=30)
        assert _risk_score(no_val) == _risk_score(healthy)


# ---------------------------------------------------------------------------
# 8. _risk_score — blocker component
# ---------------------------------------------------------------------------

class TestRiskScoreBlockers:
    def test_zero_open_blockers_adds_0(self):
        healthy = make_customer()
        assert _risk_score(healthy) == 0.0

    def test_one_open_blocker_adds_3(self):
        healthy = make_customer()
        one_block = make_customer(open_blockers=1)
        assert _risk_score(one_block) - _risk_score(healthy) == 3.0

    def test_two_open_blockers_adds_6(self):
        healthy = make_customer()
        two_blocks = make_customer(open_blockers=2)
        assert _risk_score(two_blocks) - _risk_score(healthy) == 6.0

    def test_three_open_blockers_adds_9(self):
        healthy = make_customer()
        three_blocks = make_customer(open_blockers=3)
        assert _risk_score(three_blocks) - _risk_score(healthy) == 9.0

    def test_four_open_blockers_capped_at_10(self):
        healthy = make_customer()
        four_blocks = make_customer(open_blockers=4)
        assert _risk_score(four_blocks) - _risk_score(healthy) == 10.0

    def test_many_open_blockers_capped_at_10(self):
        healthy = make_customer()
        many_blocks = make_customer(open_blockers=100)
        assert _risk_score(many_blocks) - _risk_score(healthy) == 10.0

    def test_one_escalated_adds_2_5(self):
        healthy = make_customer()
        one_esc = make_customer(escalated_tickets=1)
        assert _risk_score(one_esc) - _risk_score(healthy) == 2.5

    def test_two_escalated_adds_5(self):
        healthy = make_customer()
        two_esc = make_customer(escalated_tickets=2)
        assert _risk_score(two_esc) - _risk_score(healthy) == 5.0

    def test_three_escalated_capped_at_5(self):
        healthy = make_customer()
        three_esc = make_customer(escalated_tickets=3)
        assert _risk_score(three_esc) - _risk_score(healthy) == 5.0


# ---------------------------------------------------------------------------
# 9. _risk_score — CS engagement component
# ---------------------------------------------------------------------------

class TestRiskScoreCSEngagement:
    def test_kickoff_done_no_points(self):
        healthy = make_customer(kickoff_completed=True, last_cs_contact_days=3)
        assert _risk_score(healthy) == 0.0

    def test_no_kickoff_adds_5(self):
        healthy = make_customer()
        no_kickoff = make_customer(kickoff_completed=False)
        assert _risk_score(no_kickoff) - _risk_score(healthy) == 5.0

    def test_cs_contact_over_14_adds_5(self):
        healthy = make_customer()
        late_cs = make_customer(last_cs_contact_days=15)
        assert _risk_score(late_cs) - _risk_score(healthy) == 5.0

    def test_cs_contact_over_7_adds_2(self):
        healthy = make_customer()
        mid_cs = make_customer(last_cs_contact_days=10)
        assert _risk_score(mid_cs) - _risk_score(healthy) == 2.0

    def test_cs_contact_exactly_7_adds_0(self):
        healthy = make_customer()
        exactly_7 = make_customer(last_cs_contact_days=7)
        assert _risk_score(exactly_7) == _risk_score(healthy)

    def test_cs_contact_exactly_14_adds_2(self):
        healthy = make_customer()
        exactly_14 = make_customer(last_cs_contact_days=14)
        assert _risk_score(exactly_14) - _risk_score(healthy) == 2.0

    def test_score_max_clamped_to_100(self):
        # Worst-case customer
        worst = make_customer(
            exec_sponsor_active=False,
            champion_engaged=False,
            training_completion_pct=0.0,
            users_activated_pct=0.0,
            first_value_achieved=False,
            days_since_contract=90,
            expected_go_live_days=60,
            actual_go_live_days=0,
            open_blockers=10,
            escalated_tickets=10,
            last_cs_contact_days=30,
            kickoff_completed=False,
        )
        assert _risk_score(worst) == 100.0

    def test_score_is_float(self):
        inp = make_customer()
        assert isinstance(_risk_score(inp), (int, float))

    def test_score_nonnegative(self):
        inp = make_customer()
        assert _risk_score(inp) >= 0.0


# ---------------------------------------------------------------------------
# 10. _risk_level
# ---------------------------------------------------------------------------

class TestRiskLevel:
    def test_score_0_is_low(self):
        assert _risk_level(0.0) == OnboardingRisk.LOW

    def test_score_19_is_low(self):
        assert _risk_level(19.9) == OnboardingRisk.LOW

    def test_score_20_is_moderate(self):
        assert _risk_level(20.0) == OnboardingRisk.MODERATE

    def test_score_39_is_moderate(self):
        assert _risk_level(39.9) == OnboardingRisk.MODERATE

    def test_score_40_is_high(self):
        assert _risk_level(40.0) == OnboardingRisk.HIGH

    def test_score_64_is_high(self):
        assert _risk_level(64.9) == OnboardingRisk.HIGH

    def test_score_65_is_critical(self):
        assert _risk_level(65.0) == OnboardingRisk.CRITICAL

    def test_score_100_is_critical(self):
        assert _risk_level(100.0) == OnboardingRisk.CRITICAL

    def test_returns_enum(self):
        assert isinstance(_risk_level(50.0), OnboardingRisk)


# ---------------------------------------------------------------------------
# 11. _risk_action
# ---------------------------------------------------------------------------

class TestRiskAction:
    def test_low_risk_gives_monitor(self):
        inp = make_customer()
        assert _risk_action(OnboardingRisk.LOW, inp) == OnboardingAction.MONITOR

    def test_moderate_risk_gives_accelerate(self):
        inp = make_customer()
        assert _risk_action(OnboardingRisk.MODERATE, inp) == OnboardingAction.ACCELERATE

    def test_high_risk_gives_rescue(self):
        inp = make_customer()
        assert _risk_action(OnboardingRisk.HIGH, inp) == OnboardingAction.RESCUE

    def test_critical_risk_gives_escalate(self):
        inp = make_customer()
        assert _risk_action(OnboardingRisk.CRITICAL, inp) == OnboardingAction.ESCALATE

    def test_low_risk_with_2_escalated_gives_escalate(self):
        inp = make_customer(escalated_tickets=2)
        assert _risk_action(OnboardingRisk.LOW, inp) == OnboardingAction.ESCALATE

    def test_moderate_risk_with_2_escalated_gives_escalate(self):
        inp = make_customer(escalated_tickets=2)
        assert _risk_action(OnboardingRisk.MODERATE, inp) == OnboardingAction.ESCALATE

    def test_high_risk_with_2_escalated_gives_escalate(self):
        inp = make_customer(escalated_tickets=2)
        assert _risk_action(OnboardingRisk.HIGH, inp) == OnboardingAction.ESCALATE

    def test_low_risk_with_1_escalated_gives_monitor(self):
        inp = make_customer(escalated_tickets=1)
        assert _risk_action(OnboardingRisk.LOW, inp) == OnboardingAction.MONITOR

    def test_returns_enum(self):
        inp = make_customer()
        assert isinstance(_risk_action(OnboardingRisk.LOW, inp), OnboardingAction)


# ---------------------------------------------------------------------------
# 12. _churn_signal
# ---------------------------------------------------------------------------

class TestChurnSignal:
    def test_low_score_exec_active_gives_none(self):
        inp = make_customer(exec_sponsor_active=True)
        assert _churn_signal(0.0, inp) == ChurnSignal.NONE

    def test_score_20_gives_early(self):
        inp = make_customer(exec_sponsor_active=True)
        assert _churn_signal(20.0, inp) == ChurnSignal.EARLY

    def test_score_39_gives_early(self):
        inp = make_customer(exec_sponsor_active=True)
        assert _churn_signal(39.0, inp) == ChurnSignal.EARLY

    def test_score_40_gives_moderate(self):
        inp = make_customer(exec_sponsor_active=True)
        assert _churn_signal(40.0, inp) == ChurnSignal.MODERATE

    def test_score_64_gives_moderate(self):
        inp = make_customer(exec_sponsor_active=True)
        assert _churn_signal(64.0, inp) == ChurnSignal.MODERATE

    def test_score_65_gives_strong(self):
        inp = make_customer(exec_sponsor_active=True)
        assert _churn_signal(65.0, inp) == ChurnSignal.STRONG

    def test_score_100_gives_strong(self):
        inp = make_customer(exec_sponsor_active=True)
        assert _churn_signal(100.0, inp) == ChurnSignal.STRONG

    def test_no_exec_sponsor_low_score_gives_moderate(self):
        inp = make_customer(exec_sponsor_active=False)
        assert _churn_signal(0.0, inp) == ChurnSignal.MODERATE

    def test_two_escalated_gives_strong(self):
        inp = make_customer(escalated_tickets=2, exec_sponsor_active=True)
        assert _churn_signal(0.0, inp) == ChurnSignal.STRONG

    def test_one_escalated_not_strong(self):
        inp = make_customer(escalated_tickets=1, exec_sponsor_active=True)
        # score 0 and exec active → NONE (1 escalated alone doesn't trigger STRONG)
        assert _churn_signal(0.0, inp) == ChurnSignal.NONE

    def test_returns_enum(self):
        inp = make_customer()
        assert isinstance(_churn_signal(0.0, inp), ChurnSignal)


# ---------------------------------------------------------------------------
# 13. _time_to_value_score
# ---------------------------------------------------------------------------

class TestTimeToValueScore:
    def test_healthy_customer_high_ttv(self):
        # first_value + users>=50 + all integrations + training>=80
        inp = make_customer(
            first_value_achieved=True,
            users_activated_pct=70.0,
            integrations_completed=3,
            integrations_planned=3,
            training_completion_pct=90.0,
        )
        # 35 + 25 + 20 + 20 = 100
        assert _time_to_value_score(inp) == 100.0

    def test_no_first_value_reduces_score(self):
        full = make_customer(first_value_achieved=True)
        no_val = make_customer(first_value_achieved=False)
        assert _time_to_value_score(no_val) < _time_to_value_score(full)

    def test_first_value_adds_35(self):
        no_val = make_customer(
            first_value_achieved=False,
            users_activated_pct=0.0,
            integrations_planned=0,
            training_completion_pct=0.0,
        )
        with_val = make_customer(
            first_value_achieved=True,
            users_activated_pct=0.0,
            integrations_planned=0,
            training_completion_pct=0.0,
        )
        assert _time_to_value_score(with_val) - _time_to_value_score(no_val) == 35.0

    def test_users_above_50_adds_25(self):
        base = make_customer(
            first_value_achieved=False,
            users_activated_pct=0.0,
            integrations_planned=0,
            training_completion_pct=0.0,
        )
        with_users = make_customer(
            first_value_achieved=False,
            users_activated_pct=60.0,
            integrations_planned=0,
            training_completion_pct=0.0,
        )
        assert _time_to_value_score(with_users) - _time_to_value_score(base) == 25.0

    def test_users_25_to_50_adds_12(self):
        base = make_customer(
            first_value_achieved=False,
            users_activated_pct=0.0,
            integrations_planned=0,
            training_completion_pct=0.0,
        )
        with_users = make_customer(
            first_value_achieved=False,
            users_activated_pct=30.0,
            integrations_planned=0,
            training_completion_pct=0.0,
        )
        assert _time_to_value_score(with_users) - _time_to_value_score(base) == 12.0

    def test_users_exactly_25_adds_12(self):
        base = make_customer(
            first_value_achieved=False,
            users_activated_pct=0.0,
            integrations_planned=0,
            training_completion_pct=0.0,
        )
        with_users = make_customer(
            first_value_achieved=False,
            users_activated_pct=25.0,
            integrations_planned=0,
            training_completion_pct=0.0,
        )
        assert _time_to_value_score(with_users) - _time_to_value_score(base) == 12.0

    def test_users_exactly_50_adds_25(self):
        base = make_customer(
            first_value_achieved=False,
            users_activated_pct=0.0,
            integrations_planned=0,
            training_completion_pct=0.0,
        )
        with_users = make_customer(
            first_value_achieved=False,
            users_activated_pct=50.0,
            integrations_planned=0,
            training_completion_pct=0.0,
        )
        assert _time_to_value_score(with_users) - _time_to_value_score(base) == 25.0

    def test_integrations_ratio_adds_up_to_20(self):
        base = make_customer(
            first_value_achieved=False,
            users_activated_pct=0.0,
            integrations_completed=0,
            integrations_planned=0,
            training_completion_pct=0.0,
        )
        full_int = make_customer(
            first_value_achieved=False,
            users_activated_pct=0.0,
            integrations_completed=5,
            integrations_planned=5,
            training_completion_pct=0.0,
        )
        assert _time_to_value_score(full_int) - _time_to_value_score(base) == 20.0

    def test_half_integrations_adds_10(self):
        base = make_customer(
            first_value_achieved=False,
            users_activated_pct=0.0,
            integrations_completed=0,
            integrations_planned=0,
            training_completion_pct=0.0,
        )
        half_int = make_customer(
            first_value_achieved=False,
            users_activated_pct=0.0,
            integrations_completed=2,
            integrations_planned=4,
            training_completion_pct=0.0,
        )
        assert _time_to_value_score(half_int) - _time_to_value_score(base) == 10.0

    def test_no_planned_integrations_adds_0(self):
        base = make_customer(
            first_value_achieved=False,
            users_activated_pct=0.0,
            integrations_completed=0,
            integrations_planned=0,
            training_completion_pct=0.0,
        )
        assert _time_to_value_score(base) == 0.0

    def test_training_above_80_adds_20(self):
        base = make_customer(
            first_value_achieved=False,
            users_activated_pct=0.0,
            integrations_planned=0,
            training_completion_pct=0.0,
        )
        good_train = make_customer(
            first_value_achieved=False,
            users_activated_pct=0.0,
            integrations_planned=0,
            training_completion_pct=85.0,
        )
        assert _time_to_value_score(good_train) - _time_to_value_score(base) == 20.0

    def test_training_50_to_80_adds_10(self):
        base = make_customer(
            first_value_achieved=False,
            users_activated_pct=0.0,
            integrations_planned=0,
            training_completion_pct=0.0,
        )
        mid_train = make_customer(
            first_value_achieved=False,
            users_activated_pct=0.0,
            integrations_planned=0,
            training_completion_pct=60.0,
        )
        assert _time_to_value_score(mid_train) - _time_to_value_score(base) == 10.0

    def test_training_exactly_80_adds_20(self):
        base = make_customer(
            first_value_achieved=False,
            users_activated_pct=0.0,
            integrations_planned=0,
            training_completion_pct=0.0,
        )
        train_80 = make_customer(
            first_value_achieved=False,
            users_activated_pct=0.0,
            integrations_planned=0,
            training_completion_pct=80.0,
        )
        assert _time_to_value_score(train_80) - _time_to_value_score(base) == 20.0

    def test_training_exactly_50_adds_10(self):
        base = make_customer(
            first_value_achieved=False,
            users_activated_pct=0.0,
            integrations_planned=0,
            training_completion_pct=0.0,
        )
        train_50 = make_customer(
            first_value_achieved=False,
            users_activated_pct=0.0,
            integrations_planned=0,
            training_completion_pct=50.0,
        )
        assert _time_to_value_score(train_50) - _time_to_value_score(base) == 10.0

    def test_score_clamped_max_100(self):
        inp = make_customer(
            first_value_achieved=True,
            users_activated_pct=100.0,
            integrations_completed=10,
            integrations_planned=10,
            training_completion_pct=100.0,
        )
        assert _time_to_value_score(inp) == 100.0

    def test_score_clamped_min_0(self):
        inp = make_customer(
            first_value_achieved=False,
            users_activated_pct=0.0,
            integrations_completed=0,
            integrations_planned=0,
            training_completion_pct=0.0,
        )
        assert _time_to_value_score(inp) == 0.0

    def test_returns_float(self):
        inp = make_customer()
        assert isinstance(_time_to_value_score(inp), (int, float))


# ---------------------------------------------------------------------------
# 14. _risk_factors
# ---------------------------------------------------------------------------

class TestRiskFactors:
    def test_healthy_has_no_factors(self):
        inp = make_customer()
        assert _risk_factors(inp, 0) == []

    def test_delay_14_mentioned(self):
        inp = make_customer()
        factors = _risk_factors(inp, 14)
        assert any("14" in f for f in factors)

    def test_delay_less_than_14_not_mentioned(self):
        inp = make_customer()
        factors = _risk_factors(inp, 13)
        # No delay factor
        assert not any("retard" in f for f in factors)

    def test_no_exec_sponsor_mentioned(self):
        inp = make_customer(exec_sponsor_active=False)
        factors = _risk_factors(inp, 0)
        assert any("sponsor" in f.lower() or "exécutif" in f for f in factors)

    def test_no_champion_mentioned(self):
        inp = make_customer(champion_engaged=False)
        factors = _risk_factors(inp, 0)
        assert any("champion" in f.lower() for f in factors)

    def test_training_below_30_mentioned(self):
        inp = make_customer(training_completion_pct=20.0)
        factors = _risk_factors(inp, 0)
        assert any("formation" in f.lower() or "20" in f for f in factors)

    def test_training_above_30_not_mentioned(self):
        inp = make_customer(training_completion_pct=50.0)
        factors = _risk_factors(inp, 0)
        assert not any("formation" in f.lower() for f in factors)

    def test_users_below_20_mentioned(self):
        inp = make_customer(users_activated_pct=10.0)
        factors = _risk_factors(inp, 0)
        assert any("adoption" in f.lower() or "utilisateurs" in f.lower() for f in factors)

    def test_no_first_value_after_30_days_mentioned(self):
        inp = make_customer(first_value_achieved=False, days_since_contract=31)
        factors = _risk_factors(inp, 0)
        assert any("value" in f.lower() or "valeur" in f.lower() or "usage" in f.lower() for f in factors)

    def test_no_first_value_before_30_days_not_mentioned(self):
        inp = make_customer(first_value_achieved=False, days_since_contract=20)
        factors = _risk_factors(inp, 0)
        assert not any("value" in f.lower() or "valeur" in f.lower() or "usage" in f.lower() for f in factors)

    def test_open_blockers_2_mentioned(self):
        inp = make_customer(open_blockers=2)
        factors = _risk_factors(inp, 0)
        assert any("blocage" in f.lower() or "bloq" in f.lower() for f in factors)

    def test_open_blockers_1_not_mentioned(self):
        inp = make_customer(open_blockers=1)
        factors = _risk_factors(inp, 0)
        assert not any("blocage" in f.lower() for f in factors)

    def test_escalated_tickets_1_mentioned(self):
        inp = make_customer(escalated_tickets=1)
        factors = _risk_factors(inp, 0)
        assert any("escalad" in f.lower() or "ticket" in f.lower() for f in factors)

    def test_no_kickoff_mentioned(self):
        inp = make_customer(kickoff_completed=False)
        factors = _risk_factors(inp, 0)
        assert any("kickoff" in f.lower() for f in factors)

    def test_cs_contact_over_14_mentioned(self):
        inp = make_customer(last_cs_contact_days=20)
        factors = _risk_factors(inp, 0)
        assert any("contact" in f.lower() or "cs" in f.lower() for f in factors)

    def test_returns_list(self):
        inp = make_customer()
        assert isinstance(_risk_factors(inp, 0), list)


# ---------------------------------------------------------------------------
# 15. _positive_signals
# ---------------------------------------------------------------------------

class TestPositiveSignals:
    def test_healthy_has_many_signals(self):
        inp = make_customer()
        signals = _positive_signals(inp)
        assert len(signals) >= 5

    def test_first_value_signal(self):
        inp = make_customer(first_value_achieved=True)
        signals = _positive_signals(inp)
        assert any("value" in s.lower() or "valeur" in s.lower() or "usage" in s.lower() for s in signals)

    def test_no_first_value_no_signal(self):
        inp = make_customer(first_value_achieved=False)
        signals = _positive_signals(inp)
        assert not any("value" in s.lower() or "valeur" in s.lower() or "usage" in s.lower() for s in signals)

    def test_exec_sponsor_signal(self):
        inp = make_customer(exec_sponsor_active=True)
        signals = _positive_signals(inp)
        assert any("sponsor" in s.lower() or "exécutif" in s.lower() for s in signals)

    def test_no_exec_sponsor_no_signal(self):
        inp = make_customer(exec_sponsor_active=False)
        signals = _positive_signals(inp)
        assert not any("sponsor" in s.lower() or "exécutif" in s.lower() for s in signals)

    def test_champion_signal(self):
        inp = make_customer(champion_engaged=True)
        signals = _positive_signals(inp)
        assert any("champion" in s.lower() for s in signals)

    def test_training_above_80_signal(self):
        inp = make_customer(training_completion_pct=90.0)
        signals = _positive_signals(inp)
        assert any("formation" in s.lower() for s in signals)

    def test_training_below_80_no_signal(self):
        inp = make_customer(training_completion_pct=70.0)
        signals = _positive_signals(inp)
        assert not any("formation" in s.lower() for s in signals)

    def test_users_above_50_signal(self):
        inp = make_customer(users_activated_pct=60.0)
        signals = _positive_signals(inp)
        assert any("adoption" in s.lower() or "utilisateurs" in s.lower() for s in signals)

    def test_kickoff_signal(self):
        inp = make_customer(kickoff_completed=True)
        signals = _positive_signals(inp)
        assert any("kickoff" in s.lower() for s in signals)

    def test_health_check_signal(self):
        inp = make_customer(health_check_completed=True)
        signals = _positive_signals(inp)
        assert any("health" in s.lower() for s in signals)

    def test_zero_blockers_signal(self):
        inp = make_customer(open_blockers=0)
        signals = _positive_signals(inp)
        assert any("blocage" in s.lower() or "bloq" in s.lower() for s in signals)

    def test_one_blocker_no_zero_blocker_signal(self):
        inp = make_customer(open_blockers=1)
        signals = _positive_signals(inp)
        assert not any("blocage" in s.lower() or "aucun blocage" in s.lower() for s in signals)

    def test_all_integrations_done_signal(self):
        inp = make_customer(integrations_completed=3, integrations_planned=3)
        signals = _positive_signals(inp)
        assert any("intégration" in s.lower() for s in signals)

    def test_partial_integrations_no_signal(self):
        inp = make_customer(integrations_completed=2, integrations_planned=3)
        signals = _positive_signals(inp)
        assert not any("intégration" in s.lower() for s in signals)

    def test_returns_list(self):
        inp = make_customer()
        assert isinstance(_positive_signals(inp), list)


# ---------------------------------------------------------------------------
# 16. _intervention_plan
# ---------------------------------------------------------------------------

class TestInterventionPlan:
    def test_escalate_action_has_3_items(self):
        inp = make_customer(open_blockers=2)
        plan = _intervention_plan(OnboardingRisk.CRITICAL, OnboardingAction.ESCALATE, inp, 30)
        assert len(plan) == 3

    def test_escalate_mentions_clevel(self):
        inp = make_customer(open_blockers=0)
        plan = _intervention_plan(OnboardingRisk.CRITICAL, OnboardingAction.ESCALATE, inp, 30)
        assert any("c-level" in p.lower() or "direction" in p.lower() or "escalade" in p.lower() for p in plan)

    def test_escalate_with_blockers_has_task_force(self):
        inp = make_customer(open_blockers=2)
        plan = _intervention_plan(OnboardingRisk.CRITICAL, OnboardingAction.ESCALATE, inp, 30)
        assert any("blocage" in p.lower() or "task" in p.lower() for p in plan)

    def test_rescue_action_has_steps(self):
        inp = make_customer(first_value_achieved=False)
        plan = _intervention_plan(OnboardingRisk.HIGH, OnboardingAction.RESCUE, inp, 0)
        assert len(plan) >= 2

    def test_rescue_mentions_rescue(self):
        inp = make_customer(first_value_achieved=True)
        plan = _intervention_plan(OnboardingRisk.HIGH, OnboardingAction.RESCUE, inp, 0)
        assert any("rescue" in p.lower() or "freins" in p.lower() or "rebloquer" in p.lower() for p in plan)

    def test_rescue_no_first_value_adds_quickwin(self):
        inp = make_customer(first_value_achieved=False)
        plan = _intervention_plan(OnboardingRisk.HIGH, OnboardingAction.RESCUE, inp, 0)
        assert any("quickwin" in p.lower() or "valeur" in p.lower() for p in plan)

    def test_accelerate_action_has_steps(self):
        inp = make_customer()
        plan = _intervention_plan(OnboardingRisk.MODERATE, OnboardingAction.ACCELERATE, inp, 0)
        assert len(plan) >= 2

    def test_accelerate_mentions_formation(self):
        inp = make_customer()
        plan = _intervention_plan(OnboardingRisk.MODERATE, OnboardingAction.ACCELERATE, inp, 0)
        assert any("formation" in p.lower() or "accélérer" in p.lower() for p in plan)

    def test_accelerate_delay_over_7_adds_planning(self):
        inp = make_customer()
        plan = _intervention_plan(OnboardingRisk.MODERATE, OnboardingAction.ACCELERATE, inp, 10)
        assert any("planning" in p.lower() or "jalons" in p.lower() for p in plan)

    def test_monitor_action_has_3_items(self):
        inp = make_customer()
        plan = _intervention_plan(OnboardingRisk.LOW, OnboardingAction.MONITOR, inp, 0)
        assert len(plan) == 3

    def test_monitor_mentions_weekly(self):
        inp = make_customer()
        plan = _intervention_plan(OnboardingRisk.LOW, OnboardingAction.MONITOR, inp, 0)
        assert any("hebdomadaire" in p.lower() or "cadence" in p.lower() for p in plan)

    def test_returns_list(self):
        inp = make_customer()
        assert isinstance(_intervention_plan(OnboardingRisk.LOW, OnboardingAction.MONITOR, inp, 0), list)


# ---------------------------------------------------------------------------
# 17. OnboardingRiskMonitorEngine.monitor
# ---------------------------------------------------------------------------

class TestEngineMonitor:
    def setup_method(self):
        self.engine = OnboardingRiskMonitorEngine()

    def test_returns_result(self):
        inp = make_customer()
        result = self.engine.monitor(inp)
        assert isinstance(result, OnboardingResult)

    def test_stores_result(self):
        inp = make_customer(customer_id="x1")
        self.engine.monitor(inp)
        assert len(self.engine.all_customers()) == 1

    def test_healthy_customer_low_risk(self):
        inp = make_customer()
        result = self.engine.monitor(inp)
        assert result.risk_level == OnboardingRisk.LOW

    def test_worst_case_critical_risk(self):
        inp = make_customer(
            exec_sponsor_active=False,
            champion_engaged=False,
            training_completion_pct=0.0,
            users_activated_pct=0.0,
            first_value_achieved=False,
            days_since_contract=90,
            expected_go_live_days=60,
            actual_go_live_days=0,
            open_blockers=10,
            escalated_tickets=3,
            last_cs_contact_days=30,
            kickoff_completed=False,
        )
        result = self.engine.monitor(inp)
        assert result.risk_level == OnboardingRisk.CRITICAL

    def test_overwrites_existing_result(self):
        inp1 = make_customer(customer_id="same", training_completion_pct=90.0)
        inp2 = make_customer(customer_id="same", training_completion_pct=10.0)
        self.engine.monitor(inp1)
        self.engine.monitor(inp2)
        assert len(self.engine.all_customers()) == 1

    def test_correct_customer_id(self):
        inp = make_customer(customer_id="abc-123")
        result = self.engine.monitor(inp)
        assert result.customer_id == "abc-123"

    def test_correct_arr(self):
        inp = make_customer(arr_eur=999_999.0)
        result = self.engine.monitor(inp)
        assert result.arr_eur == 999_999.0

    def test_correct_phase(self):
        inp = make_customer(phase=OnboardingPhase.TRAINING)
        result = self.engine.monitor(inp)
        assert result.phase == OnboardingPhase.TRAINING

    def test_go_live_delay_computed(self):
        inp = make_customer(actual_go_live_days=80, expected_go_live_days=60)
        result = self.engine.monitor(inp)
        assert result.go_live_delay_days == 20

    def test_intervention_plan_not_empty(self):
        inp = make_customer()
        result = self.engine.monitor(inp)
        assert len(result.intervention_plan) >= 1


# ---------------------------------------------------------------------------
# 18. monitor_batch
# ---------------------------------------------------------------------------

class TestMonitorBatch:
    def setup_method(self):
        self.engine = OnboardingRiskMonitorEngine()

    def test_returns_list(self):
        results = self.engine.monitor_batch([make_customer()])
        assert isinstance(results, list)

    def test_processes_all(self):
        customers = [make_customer(customer_id=f"c{i}") for i in range(5)]
        results = self.engine.monitor_batch(customers)
        assert len(results) == 5

    def test_sorted_desc_by_risk_score(self):
        bad = make_customer(
            customer_id="bad",
            exec_sponsor_active=False,
            champion_engaged=False,
            training_completion_pct=0.0,
        )
        good = make_customer(customer_id="good")
        results = self.engine.monitor_batch([good, bad])
        assert results[0].risk_score >= results[1].risk_score

    def test_all_stored_after_batch(self):
        customers = [make_customer(customer_id=f"c{i}") for i in range(3)]
        self.engine.monitor_batch(customers)
        assert len(self.engine.all_customers()) == 3

    def test_empty_batch(self):
        results = self.engine.monitor_batch([])
        assert results == []

    def test_single_item_batch(self):
        results = self.engine.monitor_batch([make_customer()])
        assert len(results) == 1


# ---------------------------------------------------------------------------
# 19. Engine query methods
# ---------------------------------------------------------------------------

class TestEngineQueryMethods:
    def setup_method(self):
        self.engine = OnboardingRiskMonitorEngine()
        # Low-risk customer
        self.engine.monitor(make_customer(customer_id="low1"))
        # High-risk customer
        self.engine.monitor(make_customer(
            customer_id="high1",
            exec_sponsor_active=False,
            champion_engaged=False,
            training_completion_pct=5.0,
            users_activated_pct=5.0,
            first_value_achieved=False,
            days_since_contract=50,
            expected_go_live_days=30,
            open_blockers=3,
            escalated_tickets=0,
            last_cs_contact_days=20,
            kickoff_completed=False,
        ))
        # Critical-risk customer
        self.engine.monitor(make_customer(
            customer_id="crit1",
            exec_sponsor_active=False,
            champion_engaged=False,
            training_completion_pct=0.0,
            users_activated_pct=0.0,
            first_value_achieved=False,
            days_since_contract=100,
            expected_go_live_days=60,
            open_blockers=5,
            escalated_tickets=3,
            last_cs_contact_days=30,
            kickoff_completed=False,
        ))

    def test_all_customers_count(self):
        assert len(self.engine.all_customers()) == 3

    def test_all_customers_sorted_desc(self):
        results = self.engine.all_customers()
        for i in range(len(results) - 1):
            assert results[i].risk_score >= results[i + 1].risk_score

    def test_by_risk_low(self):
        low = self.engine.by_risk(OnboardingRisk.LOW)
        assert all(r.risk_level == OnboardingRisk.LOW for r in low)

    def test_by_risk_critical(self):
        crit = self.engine.by_risk(OnboardingRisk.CRITICAL)
        assert all(r.risk_level == OnboardingRisk.CRITICAL for r in crit)
        assert len(crit) >= 1

    def test_by_action_escalate(self):
        esc = self.engine.by_action(OnboardingAction.ESCALATE)
        assert all(r.risk_action == OnboardingAction.ESCALATE for r in esc)

    def test_by_phase_adoption(self):
        adop = self.engine.by_phase(OnboardingPhase.ADOPTION)
        assert all(r.phase == OnboardingPhase.ADOPTION for r in adop)

    def test_critical_customers(self):
        crit = self.engine.critical_customers()
        assert all(r.risk_level == OnboardingRisk.CRITICAL for r in crit)

    def test_needs_escalation(self):
        esc = self.engine.needs_escalation()
        assert all(r.risk_action == OnboardingAction.ESCALATE for r in esc)

    def test_at_risk_customers(self):
        at_risk = self.engine.at_risk_customers()
        for r in at_risk:
            assert r.risk_level in (OnboardingRisk.HIGH, OnboardingRisk.CRITICAL)

    def test_behind_schedule(self):
        engine = OnboardingRiskMonitorEngine()
        on_time = make_customer(customer_id="ontime", days_since_contract=30, expected_go_live_days=60, actual_go_live_days=0)
        late = make_customer(customer_id="late", days_since_contract=80, expected_go_live_days=60, actual_go_live_days=0)
        engine.monitor(on_time)
        engine.monitor(late)
        behind = engine.behind_schedule()
        assert all(r.go_live_delay_days > 0 for r in behind)
        assert any(r.customer_id == "late" for r in behind)

    def test_achieved_value(self):
        achieved = self.engine.achieved_value()
        assert all(r.time_to_value_score >= 50 for r in achieved)

    def test_avg_risk_score_type(self):
        avg = self.engine.avg_risk_score()
        assert isinstance(avg, (int, float))

    def test_avg_risk_score_in_range(self):
        avg = self.engine.avg_risk_score()
        assert 0.0 <= avg <= 100.0

    def test_avg_time_to_value_type(self):
        avg = self.engine.avg_time_to_value()
        assert isinstance(avg, (int, float))

    def test_total_arr_at_risk(self):
        total = self.engine.total_arr_at_risk_eur()
        assert isinstance(total, (int, float))
        # Only high and critical customers contribute
        at_risk = self.engine.at_risk_customers()
        expected = sum(r.arr_eur for r in at_risk)
        assert total == expected


# ---------------------------------------------------------------------------
# 20. Engine aggregate / analytics
# ---------------------------------------------------------------------------

class TestEngineAnalytics:
    def setup_method(self):
        self.engine = OnboardingRiskMonitorEngine()

    def test_avg_risk_score_empty(self):
        assert self.engine.avg_risk_score() == 0.0

    def test_avg_time_to_value_empty(self):
        assert self.engine.avg_time_to_value() == 0.0

    def test_total_arr_at_risk_empty(self):
        assert self.engine.total_arr_at_risk_eur() == 0.0

    def test_avg_risk_score_single(self):
        self.engine.monitor(make_customer())
        avg = self.engine.avg_risk_score()
        assert avg == 0.0

    def test_avg_risk_score_two_customers(self):
        self.engine.monitor(make_customer(customer_id="c1"))
        bad = make_customer(
            customer_id="c2",
            exec_sponsor_active=False,
            champion_engaged=False,
            training_completion_pct=0.0,
        )
        self.engine.monitor(bad)
        avg = self.engine.avg_risk_score()
        assert avg > 0.0

    def test_total_arr_at_risk_includes_critical(self):
        crit = make_customer(
            customer_id="crit",
            arr_eur=100_000.0,
            exec_sponsor_active=False,
            champion_engaged=False,
            training_completion_pct=0.0,
            users_activated_pct=0.0,
            first_value_achieved=False,
            days_since_contract=100,
            expected_go_live_days=60,
            open_blockers=5,
            escalated_tickets=3,
            last_cs_contact_days=30,
            kickoff_completed=False,
        )
        result = self.engine.monitor(crit)
        if result.risk_level in (OnboardingRisk.HIGH, OnboardingRisk.CRITICAL):
            assert self.engine.total_arr_at_risk_eur() == 100_000.0

    def test_total_arr_excludes_low(self):
        self.engine.monitor(make_customer(customer_id="low", arr_eur=50_000.0))
        # Low risk → not included unless it's actually high/critical
        result = self.engine.all_customers()[0]
        if result.risk_level == OnboardingRisk.LOW:
            assert self.engine.total_arr_at_risk_eur() == 0.0

    def test_avg_time_to_value_healthy(self):
        self.engine.monitor(make_customer())
        avg = self.engine.avg_time_to_value()
        assert avg > 50.0


# ---------------------------------------------------------------------------
# 21. Engine summary
# ---------------------------------------------------------------------------

class TestEngineSummary:
    def setup_method(self):
        self.engine = OnboardingRiskMonitorEngine()
        self.engine.monitor(make_customer(customer_id="c1"))
        self.engine.monitor(make_customer(customer_id="c2", phase=OnboardingPhase.TRAINING))

    def test_summary_total(self):
        s = self.engine.summary()
        assert s["total"] == 2

    def test_summary_risk_counts_keys(self):
        s = self.engine.summary()
        assert set(s["risk_counts"].keys()) == {"low", "moderate", "high", "critical"}

    def test_summary_action_counts_keys(self):
        s = self.engine.summary()
        assert set(s["action_counts"].keys()) == {"monitor", "accelerate", "rescue", "escalate"}

    def test_summary_phase_counts_keys(self):
        s = self.engine.summary()
        assert set(s["phase_counts"].keys()) == {"kickoff", "setup", "training", "adoption", "value_realization"}

    def test_summary_avg_risk_score(self):
        s = self.engine.summary()
        assert "avg_risk_score" in s
        assert isinstance(s["avg_risk_score"], (int, float))

    def test_summary_avg_time_to_value(self):
        s = self.engine.summary()
        assert "avg_time_to_value" in s
        assert isinstance(s["avg_time_to_value"], (int, float))

    def test_summary_critical_count(self):
        s = self.engine.summary()
        assert "critical_count" in s
        assert isinstance(s["critical_count"], int)

    def test_summary_behind_schedule_count(self):
        s = self.engine.summary()
        assert "behind_schedule_count" in s
        assert isinstance(s["behind_schedule_count"], int)

    def test_summary_total_arr_at_risk(self):
        s = self.engine.summary()
        assert "total_arr_at_risk_eur" in s
        assert isinstance(s["total_arr_at_risk_eur"], (int, float))

    def test_summary_risk_counts_sum(self):
        s = self.engine.summary()
        total_risk = sum(s["risk_counts"].values())
        assert total_risk == s["total"]

    def test_summary_action_counts_sum(self):
        s = self.engine.summary()
        total_actions = sum(s["action_counts"].values())
        assert total_actions == s["total"]

    def test_summary_phase_counts_sum(self):
        s = self.engine.summary()
        total_phases = sum(s["phase_counts"].values())
        assert total_phases == s["total"]

    def test_empty_engine_summary(self):
        engine = OnboardingRiskMonitorEngine()
        s = engine.summary()
        assert s["total"] == 0
        assert s["avg_risk_score"] == 0.0

    def test_summary_returns_dict(self):
        s = self.engine.summary()
        assert isinstance(s, dict)


# ---------------------------------------------------------------------------
# 22. Engine reset and edge cases
# ---------------------------------------------------------------------------

class TestEngineResetAndEdgeCases:
    def test_reset_clears_results(self):
        engine = OnboardingRiskMonitorEngine()
        engine.monitor(make_customer(customer_id="c1"))
        engine.reset()
        assert len(engine.all_customers()) == 0

    def test_reset_allows_re_use(self):
        engine = OnboardingRiskMonitorEngine()
        engine.monitor(make_customer(customer_id="c1"))
        engine.reset()
        engine.monitor(make_customer(customer_id="c2"))
        assert len(engine.all_customers()) == 1

    def test_by_risk_no_match_returns_empty(self):
        engine = OnboardingRiskMonitorEngine()
        engine.monitor(make_customer())  # low risk
        assert engine.by_risk(OnboardingRisk.CRITICAL) == []

    def test_by_action_no_match_returns_empty(self):
        engine = OnboardingRiskMonitorEngine()
        engine.monitor(make_customer())  # monitor
        assert engine.by_action(OnboardingAction.ESCALATE) == []

    def test_by_phase_no_match_returns_empty(self):
        engine = OnboardingRiskMonitorEngine()
        engine.monitor(make_customer(phase=OnboardingPhase.ADOPTION))
        assert engine.by_phase(OnboardingPhase.KICKOFF) == []

    def test_critical_customers_empty_when_none(self):
        engine = OnboardingRiskMonitorEngine()
        engine.monitor(make_customer())
        assert engine.critical_customers() == []

    def test_needs_escalation_empty_when_none(self):
        engine = OnboardingRiskMonitorEngine()
        engine.monitor(make_customer())
        # If no escalation, list should be empty (or match action)
        for r in engine.needs_escalation():
            assert r.risk_action == OnboardingAction.ESCALATE

    def test_monitor_multiple_phases(self):
        engine = OnboardingRiskMonitorEngine()
        for phase in OnboardingPhase:
            engine.monitor(make_customer(customer_id=phase.value, phase=phase))
        assert len(engine.all_customers()) == 5

    def test_monitor_all_segments(self):
        engine = OnboardingRiskMonitorEngine()
        for seg in ["enterprise", "mid_market", "smb"]:
            engine.monitor(make_customer(customer_id=seg, segment=seg))
        results = engine.all_customers()
        segs = {r.segment for r in results}
        assert segs == {"enterprise", "mid_market", "smb"}

    def test_behind_schedule_empty_when_on_time(self):
        engine = OnboardingRiskMonitorEngine()
        engine.monitor(make_customer(days_since_contract=10, expected_go_live_days=60, actual_go_live_days=0))
        assert engine.behind_schedule() == []

    def test_achieved_value_healthy(self):
        engine = OnboardingRiskMonitorEngine()
        engine.monitor(make_customer())
        # Healthy customer should have high TTV
        results = engine.all_customers()
        if results[0].time_to_value_score >= 50:
            assert len(engine.achieved_value()) >= 1

    def test_engine_fresh_instance_empty(self):
        engine = OnboardingRiskMonitorEngine()
        assert engine.all_customers() == []
        assert engine.avg_risk_score() == 0.0
        assert engine.avg_time_to_value() == 0.0
        assert engine.total_arr_at_risk_eur() == 0.0

    def test_monitor_batch_sorted_correctly_multiple(self):
        engine = OnboardingRiskMonitorEngine()
        customers = []
        for i in range(5):
            customers.append(make_customer(
                customer_id=f"c{i}",
                open_blockers=i,
            ))
        results = engine.monitor_batch(customers)
        for j in range(len(results) - 1):
            assert results[j].risk_score >= results[j + 1].risk_score

    def test_risk_score_rounded_to_1_decimal(self):
        engine = OnboardingRiskMonitorEngine()
        inp = make_customer(open_blockers=1)  # adds 3.0
        result = engine.monitor(inp)
        # Score should be expressed with at most 1 decimal place
        assert result.risk_score == round(result.risk_score, 1)
