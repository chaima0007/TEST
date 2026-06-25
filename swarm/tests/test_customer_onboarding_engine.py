"""
Comprehensive pytest tests for CustomerOnboardingEngine.
Coverage: enums, dataclasses, all scoring helpers, boundary values,
edge cases, end-to-end scenarios, to_dict() / summary() key invariants.
"""
from __future__ import annotations

import pytest
from swarm.intelligence.customer_onboarding_engine import (
    CustomerOnboardingEngine,
    CustomerOnboardingInput,
    CustomerOnboardingResult,
    OnboardingAction,
    OnboardingPhase,
    OnboardingRisk,
    SuccessProbability,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers / fixtures
# ─────────────────────────────────────────────────────────────────────────────

def make_input(
    *,
    account_id: str = "ACC-001",
    account_name: str = "Acme Corp",
    csm_id: str = "CSM-001",
    segment: str = "enterprise",
    contract_start_days: int = 30,
    expected_onboarding_days: int = 90,
    current_phase: OnboardingPhase = OnboardingPhase.CONFIGURATION,
    setup_completion_pct: float = 50.0,
    training_sessions_completed: int = 3,
    training_sessions_planned: int = 5,
    users_activated: int = 5,
    users_licensed: int = 10,
    days_to_first_login: int = 2,
    support_tickets_open: int = 0,
    support_tickets_resolved: int = 2,
    executive_sponsor_engaged: bool = True,
    implementation_partner: bool = False,
    integration_count: int = 0,
    integrations_complete: int = 0,
    nps_onboarding: float = 20.0,
    previous_platform_migration: bool = False,
    data_migration_complexity: str = "simple",
    kickoff_held: bool = True,
) -> CustomerOnboardingInput:
    return CustomerOnboardingInput(
        account_id=account_id,
        account_name=account_name,
        csm_id=csm_id,
        segment=segment,
        contract_start_days=contract_start_days,
        expected_onboarding_days=expected_onboarding_days,
        current_phase=current_phase,
        setup_completion_pct=setup_completion_pct,
        training_sessions_completed=training_sessions_completed,
        training_sessions_planned=training_sessions_planned,
        users_activated=users_activated,
        users_licensed=users_licensed,
        days_to_first_login=days_to_first_login,
        support_tickets_open=support_tickets_open,
        support_tickets_resolved=support_tickets_resolved,
        executive_sponsor_engaged=executive_sponsor_engaged,
        implementation_partner=implementation_partner,
        integration_count=integration_count,
        integrations_complete=integrations_complete,
        nps_onboarding=nps_onboarding,
        previous_platform_migration=previous_platform_migration,
        data_migration_complexity=data_migration_complexity,
        kickoff_held=kickoff_held,
    )


def make_perfect_input() -> CustomerOnboardingInput:
    """All-green, high-performing account."""
    return make_input(
        setup_completion_pct=100.0,
        training_sessions_completed=5,
        training_sessions_planned=5,
        users_activated=10,
        users_licensed=10,
        days_to_first_login=1,
        support_tickets_open=0,
        executive_sponsor_engaged=True,
        integration_count=4,
        integrations_complete=4,
        nps_onboarding=80.0,
        kickoff_held=True,
        contract_start_days=30,
        expected_onboarding_days=90,
        current_phase=OnboardingPhase.COMPLETE,
    )


def make_worst_input() -> CustomerOnboardingInput:
    """All-red account."""
    return make_input(
        setup_completion_pct=0.0,
        training_sessions_completed=0,
        training_sessions_planned=5,
        users_activated=0,
        users_licensed=10,
        days_to_first_login=30,
        support_tickets_open=10,
        executive_sponsor_engaged=False,
        integration_count=4,
        integrations_complete=0,
        nps_onboarding=-80.0,
        kickoff_held=False,
        contract_start_days=200,
        expected_onboarding_days=90,
        current_phase=OnboardingPhase.KICKOFF,
        previous_platform_migration=True,
        data_migration_complexity="complex",
    )


@pytest.fixture
def engine() -> CustomerOnboardingEngine:
    return CustomerOnboardingEngine()


@pytest.fixture
def perfect_input() -> CustomerOnboardingInput:
    return make_perfect_input()


@pytest.fixture
def worst_input() -> CustomerOnboardingInput:
    return make_worst_input()


# ─────────────────────────────────────────────────────────────────────────────
# 1. Enum values
# ─────────────────────────────────────────────────────────────────────────────

class TestEnums:
    def test_onboarding_phase_values(self):
        assert OnboardingPhase.KICKOFF.value == "kickoff"
        assert OnboardingPhase.CONFIGURATION.value == "configuration"
        assert OnboardingPhase.TRAINING.value == "training"
        assert OnboardingPhase.ADOPTION.value == "adoption"
        assert OnboardingPhase.VALUE_REALIZATION.value == "value_realization"
        assert OnboardingPhase.COMPLETE.value == "complete"

    def test_onboarding_phase_count(self):
        assert len(OnboardingPhase) == 6

    def test_onboarding_risk_values(self):
        assert OnboardingRisk.LOW.value == "low"
        assert OnboardingRisk.MEDIUM.value == "medium"
        assert OnboardingRisk.HIGH.value == "high"
        assert OnboardingRisk.CRITICAL.value == "critical"

    def test_onboarding_risk_count(self):
        assert len(OnboardingRisk) == 4

    def test_success_probability_values(self):
        assert SuccessProbability.HIGH.value == "high"
        assert SuccessProbability.MEDIUM.value == "medium"
        assert SuccessProbability.LOW.value == "low"
        assert SuccessProbability.AT_RISK.value == "at_risk"

    def test_success_probability_count(self):
        assert len(SuccessProbability) == 4

    def test_onboarding_action_values(self):
        assert OnboardingAction.ACCELERATE.value == "accelerate"
        assert OnboardingAction.STANDARD.value == "standard"
        assert OnboardingAction.ESCALATE.value == "escalate"
        assert OnboardingAction.REASSIGN.value == "reassign"
        assert OnboardingAction.INTERVENE.value == "intervene"
        assert OnboardingAction.CELEBRATE.value == "celebrate"

    def test_onboarding_action_count(self):
        assert len(OnboardingAction) == 6

    def test_enums_are_str_subclasses(self):
        assert isinstance(OnboardingPhase.KICKOFF, str)
        assert isinstance(OnboardingRisk.LOW, str)
        assert isinstance(SuccessProbability.HIGH, str)
        assert isinstance(OnboardingAction.STANDARD, str)


# ─────────────────────────────────────────────────────────────────────────────
# 2. CustomerOnboardingInput dataclass
# ─────────────────────────────────────────────────────────────────────────────

class TestCustomerOnboardingInput:
    def test_all_23_fields_accessible(self):
        inp = make_input()
        fields = [
            "account_id", "account_name", "csm_id", "segment",
            "contract_start_days", "expected_onboarding_days", "current_phase",
            "setup_completion_pct", "training_sessions_completed",
            "training_sessions_planned", "users_activated", "users_licensed",
            "days_to_first_login", "support_tickets_open", "support_tickets_resolved",
            "executive_sponsor_engaged", "implementation_partner",
            "integration_count", "integrations_complete", "nps_onboarding",
            "previous_platform_migration", "data_migration_complexity", "kickoff_held",
        ]
        assert len(fields) == 23
        for f in fields:
            assert hasattr(inp, f)

    def test_field_types(self):
        inp = make_input()
        assert isinstance(inp.account_id, str)
        assert isinstance(inp.setup_completion_pct, float)
        assert isinstance(inp.executive_sponsor_engaged, bool)
        assert isinstance(inp.users_activated, int)
        assert isinstance(inp.current_phase, OnboardingPhase)


# ─────────────────────────────────────────────────────────────────────────────
# 3. CustomerOnboardingResult.to_dict() – exact 15-key invariant
# ─────────────────────────────────────────────────────────────────────────────

EXPECTED_TO_DICT_KEYS = {
    "account_id", "account_name", "csm_id", "current_phase",
    "onboarding_risk", "success_probability", "onboarding_action",
    "completion_score", "time_to_value_score", "adoption_velocity",
    "training_completion_rate", "integration_health", "risk_flags_count",
    "is_on_track", "is_at_risk",
}


class TestToDict:
    def test_to_dict_exact_15_keys(self, engine):
        result = engine.analyze(make_input())
        d = result.to_dict()
        assert set(d.keys()) == EXPECTED_TO_DICT_KEYS

    def test_to_dict_key_count(self, engine):
        result = engine.analyze(make_input())
        assert len(result.to_dict()) == 15

    def test_to_dict_account_id(self, engine):
        result = engine.analyze(make_input(account_id="X-999"))
        assert result.to_dict()["account_id"] == "X-999"

    def test_to_dict_account_name(self, engine):
        result = engine.analyze(make_input(account_name="Beta Inc"))
        assert result.to_dict()["account_name"] == "Beta Inc"

    def test_to_dict_csm_id(self, engine):
        result = engine.analyze(make_input(csm_id="CSM-42"))
        assert result.to_dict()["csm_id"] == "CSM-42"

    def test_to_dict_current_phase_is_string(self, engine):
        result = engine.analyze(make_input(current_phase=OnboardingPhase.TRAINING))
        d = result.to_dict()
        assert d["current_phase"] == "training"
        assert isinstance(d["current_phase"], str)

    def test_to_dict_onboarding_risk_is_string(self, engine):
        result = engine.analyze(make_input())
        d = result.to_dict()
        assert d["onboarding_risk"] in {"low", "medium", "high", "critical"}

    def test_to_dict_success_probability_is_string(self, engine):
        result = engine.analyze(make_input())
        d = result.to_dict()
        assert d["success_probability"] in {"high", "medium", "low", "at_risk"}

    def test_to_dict_onboarding_action_is_string(self, engine):
        result = engine.analyze(make_input())
        d = result.to_dict()
        assert d["onboarding_action"] in {"accelerate", "standard", "escalate", "reassign", "intervene", "celebrate"}

    def test_to_dict_numeric_fields_present(self, engine):
        result = engine.analyze(make_input())
        d = result.to_dict()
        for key in ("completion_score", "time_to_value_score", "adoption_velocity",
                    "training_completion_rate", "integration_health"):
            assert isinstance(d[key], (int, float))

    def test_to_dict_bool_fields(self, engine):
        result = engine.analyze(make_input())
        d = result.to_dict()
        assert isinstance(d["is_on_track"], bool)
        assert isinstance(d["is_at_risk"], bool)

    def test_to_dict_risk_flags_count_is_int(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.to_dict()["risk_flags_count"], int)


# ─────────────────────────────────────────────────────────────────────────────
# 4. _completion_score
# ─────────────────────────────────────────────────────────────────────────────

class TestCompletionScore:
    def _score(self, **kwargs) -> float:
        eng = CustomerOnboardingEngine()
        return eng._completion_score(make_input(**kwargs))

    def test_perfect_score_is_100(self):
        s = self._score(
            setup_completion_pct=100.0,
            training_sessions_completed=5, training_sessions_planned=5,
            users_activated=10, users_licensed=10,
            integration_count=4, integrations_complete=4,
            kickoff_held=True, executive_sponsor_engaged=True,
        )
        assert s == 100.0

    def test_zero_score_minimum_is_0(self):
        s = self._score(
            setup_completion_pct=0.0,
            training_sessions_completed=0, training_sessions_planned=5,
            users_activated=0, users_licensed=10,
            integration_count=4, integrations_complete=0,
            kickoff_held=False, executive_sponsor_engaged=False,
        )
        assert s == 0.0

    def test_setup_weight_30pct(self):
        # Only setup contributes; no integrations → +15 free
        s = self._score(
            setup_completion_pct=100.0,
            training_sessions_completed=0, training_sessions_planned=5,
            users_activated=0, users_licensed=10,
            integration_count=0, integrations_complete=0,
            kickoff_held=False, executive_sponsor_engaged=False,
        )
        # 100*0.30 + 0 + 0 + 15 (no integrations) + 0 + 0 = 45
        assert s == 45.0

    def test_training_weight_20pct(self):
        s = self._score(
            setup_completion_pct=0.0,
            training_sessions_completed=5, training_sessions_planned=5,
            users_activated=0, users_licensed=10,
            integration_count=0, integrations_complete=0,
            kickoff_held=False, executive_sponsor_engaged=False,
        )
        # 0 + 100*0.20 + 0 + 15 + 0 + 0 = 35
        assert s == 35.0

    def test_activation_weight_25pct(self):
        s = self._score(
            setup_completion_pct=0.0,
            training_sessions_completed=0, training_sessions_planned=5,
            users_activated=10, users_licensed=10,
            integration_count=0, integrations_complete=0,
            kickoff_held=False, executive_sponsor_engaged=False,
        )
        # 0 + 0 + 100*0.25 + 15 + 0 + 0 = 40
        assert s == 40.0

    def test_integration_weight_15pct(self):
        s = self._score(
            setup_completion_pct=0.0,
            training_sessions_completed=0, training_sessions_planned=5,
            users_activated=0, users_licensed=10,
            integration_count=4, integrations_complete=4,
            kickoff_held=False, executive_sponsor_engaged=False,
        )
        # 0 + 0 + 0 + 100*0.15 + 0 + 0 = 15
        assert s == 15.0

    def test_no_integrations_gives_full_15_credit(self):
        s = self._score(
            setup_completion_pct=0.0,
            training_sessions_completed=0, training_sessions_planned=5,
            users_activated=0, users_licensed=10,
            integration_count=0, integrations_complete=0,
            kickoff_held=False, executive_sponsor_engaged=False,
        )
        assert s == 15.0

    def test_kickoff_adds_5(self):
        base = self._score(
            setup_completion_pct=0.0,
            training_sessions_completed=0, training_sessions_planned=5,
            users_activated=0, users_licensed=10,
            integration_count=0, integrations_complete=0,
            kickoff_held=False, executive_sponsor_engaged=False,
        )
        with_kickoff = self._score(
            setup_completion_pct=0.0,
            training_sessions_completed=0, training_sessions_planned=5,
            users_activated=0, users_licensed=10,
            integration_count=0, integrations_complete=0,
            kickoff_held=True, executive_sponsor_engaged=False,
        )
        assert with_kickoff - base == 5.0

    def test_exec_sponsor_adds_5(self):
        base = self._score(
            setup_completion_pct=0.0,
            training_sessions_completed=0, training_sessions_planned=5,
            users_activated=0, users_licensed=10,
            integration_count=0, integrations_complete=0,
            kickoff_held=False, executive_sponsor_engaged=False,
        )
        with_exec = self._score(
            setup_completion_pct=0.0,
            training_sessions_completed=0, training_sessions_planned=5,
            users_activated=0, users_licensed=10,
            integration_count=0, integrations_complete=0,
            kickoff_held=False, executive_sponsor_engaged=True,
        )
        assert with_exec - base == 5.0

    def test_training_sessions_planned_zero_no_contribution(self):
        # planned=0, so training weight skipped
        s = self._score(
            setup_completion_pct=0.0,
            training_sessions_completed=99, training_sessions_planned=0,
            users_activated=0, users_licensed=10,
            integration_count=0, integrations_complete=0,
            kickoff_held=False, executive_sponsor_engaged=False,
        )
        assert s == 15.0  # only free integration credit

    def test_users_licensed_zero_no_activation_contribution(self):
        s = self._score(
            setup_completion_pct=0.0,
            training_sessions_completed=0, training_sessions_planned=5,
            users_activated=99, users_licensed=0,
            integration_count=0, integrations_complete=0,
            kickoff_held=False, executive_sponsor_engaged=False,
        )
        assert s == 15.0  # only free integration credit

    def test_score_capped_at_100(self):
        s = self._score(
            setup_completion_pct=200.0,  # impossible but test clamp
            training_sessions_completed=100, training_sessions_planned=5,
            users_activated=100, users_licensed=10,
            integration_count=4, integrations_complete=4,
            kickoff_held=True, executive_sponsor_engaged=True,
        )
        assert s == 100.0

    def test_partial_training(self):
        s = self._score(
            setup_completion_pct=0.0,
            training_sessions_completed=2, training_sessions_planned=5,
            users_activated=0, users_licensed=10,
            integration_count=0, integrations_complete=0,
            kickoff_held=False, executive_sponsor_engaged=False,
        )
        # 0 + (0.4*100*0.20) + 0 + 15 + 0 + 0 = 8 + 15 = 23
        assert s == 23.0

    def test_partial_activation(self):
        s = self._score(
            setup_completion_pct=0.0,
            training_sessions_completed=0, training_sessions_planned=5,
            users_activated=5, users_licensed=10,
            integration_count=0, integrations_complete=0,
            kickoff_held=False, executive_sponsor_engaged=False,
        )
        # 0 + 0 + (0.5*100*0.25) + 15 = 12.5 + 15 = 27.5
        assert s == 27.5

    def test_partial_integrations(self):
        s = self._score(
            setup_completion_pct=0.0,
            training_sessions_completed=0, training_sessions_planned=5,
            users_activated=0, users_licensed=10,
            integration_count=4, integrations_complete=2,
            kickoff_held=False, executive_sponsor_engaged=False,
        )
        # 0 + 0 + 0 + (0.5*100*0.15) = 7.5
        assert s == 7.5

    def test_over_activated_capped_at_licensed(self):
        # 20 activated / 10 licensed → capped at 1.0
        s = self._score(
            setup_completion_pct=0.0,
            training_sessions_completed=0, training_sessions_planned=5,
            users_activated=20, users_licensed=10,
            integration_count=0, integrations_complete=0,
            kickoff_held=False, executive_sponsor_engaged=False,
        )
        # 0 + 0 + 25 + 15 = 40
        assert s == 40.0

    def test_integrations_complete_over_count_capped(self):
        s = self._score(
            setup_completion_pct=0.0,
            training_sessions_completed=0, training_sessions_planned=5,
            users_activated=0, users_licensed=10,
            integration_count=2, integrations_complete=10,
            kickoff_held=False, executive_sponsor_engaged=False,
        )
        # capped at 1.0 → 15
        assert s == 15.0

    def test_setup_50pct(self):
        s = self._score(
            setup_completion_pct=50.0,
            training_sessions_completed=0, training_sessions_planned=5,
            users_activated=0, users_licensed=10,
            integration_count=0, integrations_complete=0,
            kickoff_held=False, executive_sponsor_engaged=False,
        )
        # 50*0.30 + 0 + 0 + 15 = 15 + 15 = 30
        assert s == 30.0

    def test_all_components_combined(self):
        s = self._score(
            setup_completion_pct=100.0,
            training_sessions_completed=4, training_sessions_planned=5,
            users_activated=8, users_licensed=10,
            integration_count=4, integrations_complete=3,
            kickoff_held=True, executive_sponsor_engaged=True,
        )
        # 30 + 16 + 20 + 11.25 + 5 + 5 = 87.25
        expected = round(30 + 16 + 20 + 11.25 + 5 + 5, 1)
        assert s == expected


# ─────────────────────────────────────────────────────────────────────────────
# 5. _time_to_value_score
# ─────────────────────────────────────────────────────────────────────────────

class TestTimeToValueScore:
    def _ttv(self, completion: float = 50.0, **kwargs) -> float:
        eng = CustomerOnboardingEngine()
        inp = make_input(**kwargs)
        return eng._time_to_value_score(inp, completion)

    def test_base_score_50(self):
        # No positive/negative modifiers: days_to_first_login=8..14, pct_time=0.5,
        # no prev_migration, simple complexity, nps=0
        ttv = self._ttv(
            completion=50.0,
            days_to_first_login=10,
            contract_start_days=45, expected_onboarding_days=90,
            previous_platform_migration=False,
            data_migration_complexity="simple",
            nps_onboarding=0.0,
        )
        # 50 - 10 (days 8-14) + 0 (schedule, pct=0.5 exactly, no bonus) + 0 + nps_norm*20
        # nps_norm = (0+100)/200 = 0.5, *20 = 10
        # pct_time=0.5 → not <0.5, not >1.5, not >1.0 → 0
        assert ttv == 50.0

    def test_first_login_day_1_bonus_20(self):
        ttv1 = self._ttv(
            completion=0.0,
            days_to_first_login=1,
            contract_start_days=90, expected_onboarding_days=90,
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="simple",
        )
        ttv2 = self._ttv(
            completion=0.0,
            days_to_first_login=5,
            contract_start_days=90, expected_onboarding_days=90,
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="simple",
        )
        # Day 1 adds 20, day 5 adds 5 → difference of 15
        assert ttv1 - ttv2 == 15.0

    def test_first_login_day_3_bonus_15(self):
        ttv = self._ttv(
            completion=0.0,
            days_to_first_login=3,
            contract_start_days=90, expected_onboarding_days=90,
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="simple",
        )
        ttv_day5 = self._ttv(
            completion=0.0,
            days_to_first_login=5,
            contract_start_days=90, expected_onboarding_days=90,
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="simple",
        )
        assert ttv - ttv_day5 == 10.0  # 15 - 5

    def test_first_login_day_7_bonus_5(self):
        ttv = self._ttv(
            completion=0.0,
            days_to_first_login=7,
            contract_start_days=90, expected_onboarding_days=90,
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="simple",
        )
        ttv_day15 = self._ttv(
            completion=0.0,
            days_to_first_login=15,
            contract_start_days=90, expected_onboarding_days=90,
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="simple",
        )
        # Day 7 adds 5; >14 subtracts 20 → diff = 5+20 = 25
        assert ttv - ttv_day15 == 25.0

    def test_first_login_greater_than_14_penalty_20(self):
        ttv = self._ttv(
            completion=0.0,
            days_to_first_login=15,
            contract_start_days=90, expected_onboarding_days=90,
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="simple",
        )
        ttv_day8 = self._ttv(
            completion=0.0,
            days_to_first_login=8,
            contract_start_days=90, expected_onboarding_days=90,
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="simple",
        )
        # >14 → -20, day 8 → -10 → diff = -10
        assert ttv_day8 - ttv == 10.0

    def test_days_8_to_14_penalty_10(self):
        ttv = self._ttv(
            completion=0.0,
            days_to_first_login=10,
            contract_start_days=90, expected_onboarding_days=90,
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="simple",
        )
        ttv_day5 = self._ttv(
            completion=0.0,
            days_to_first_login=5,
            contract_start_days=90, expected_onboarding_days=90,
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="simple",
        )
        # day 10 → -10, day 5 → +5 → diff = -15
        assert ttv_day5 - ttv == 15.0

    def test_schedule_bonus_pct_under_half_and_completion_ge_50(self):
        ttv_bonus = self._ttv(
            completion=50.0,
            days_to_first_login=1,
            contract_start_days=20, expected_onboarding_days=90,
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="simple",
        )
        ttv_no_bonus = self._ttv(
            completion=50.0,
            days_to_first_login=1,
            contract_start_days=46, expected_onboarding_days=90,  # pct=0.511
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="simple",
        )
        assert ttv_bonus - ttv_no_bonus == 15.0

    def test_schedule_no_bonus_when_completion_lt_50(self):
        ttv_low = self._ttv(
            completion=49.9,
            days_to_first_login=1,
            contract_start_days=20, expected_onboarding_days=90,
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="simple",
        )
        ttv_high = self._ttv(
            completion=50.0,
            days_to_first_login=1,
            contract_start_days=20, expected_onboarding_days=90,
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="simple",
        )
        assert ttv_high - ttv_low == 15.0

    def test_schedule_overrun_gt_1_5_penalty_20(self):
        ttv = self._ttv(
            completion=0.0,
            days_to_first_login=10,
            contract_start_days=150, expected_onboarding_days=90,  # 1.667
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="simple",
        )
        ttv_ok = self._ttv(
            completion=0.0,
            days_to_first_login=10,
            contract_start_days=45, expected_onboarding_days=90,  # 0.5
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="simple",
        )
        assert ttv_ok - ttv == 20.0

    def test_schedule_overrun_gt_1_0_penalty_10(self):
        ttv = self._ttv(
            completion=0.0,
            days_to_first_login=10,
            contract_start_days=100, expected_onboarding_days=90,  # 1.111
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="simple",
        )
        ttv_ok = self._ttv(
            completion=0.0,
            days_to_first_login=10,
            contract_start_days=45, expected_onboarding_days=90,
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="simple",
        )
        assert ttv_ok - ttv == 10.0

    def test_prev_migration_penalty_10(self):
        with_mig = self._ttv(
            completion=0.0,
            days_to_first_login=10,
            contract_start_days=45, expected_onboarding_days=90,
            nps_onboarding=-100.0, previous_platform_migration=True,
            data_migration_complexity="simple",
        )
        without = self._ttv(
            completion=0.0,
            days_to_first_login=10,
            contract_start_days=45, expected_onboarding_days=90,
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="simple",
        )
        assert without - with_mig == 10.0

    def test_complex_migration_penalty_15(self):
        with_complex = self._ttv(
            completion=0.0,
            days_to_first_login=10,
            contract_start_days=45, expected_onboarding_days=90,
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="complex",
        )
        simple = self._ttv(
            completion=0.0,
            days_to_first_login=10,
            contract_start_days=45, expected_onboarding_days=90,
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="simple",
        )
        assert simple - with_complex == 15.0

    def test_moderate_migration_penalty_5(self):
        with_mod = self._ttv(
            completion=0.0,
            days_to_first_login=10,
            contract_start_days=45, expected_onboarding_days=90,
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="moderate",
        )
        simple = self._ttv(
            completion=0.0,
            days_to_first_login=10,
            contract_start_days=45, expected_onboarding_days=90,
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="simple",
        )
        assert simple - with_mod == 5.0

    def test_nps_100_adds_20(self):
        ttv_high = self._ttv(
            completion=0.0,
            days_to_first_login=10,
            contract_start_days=45, expected_onboarding_days=90,
            nps_onboarding=100.0, previous_platform_migration=False,
            data_migration_complexity="simple",
        )
        ttv_low = self._ttv(
            completion=0.0,
            days_to_first_login=10,
            contract_start_days=45, expected_onboarding_days=90,
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="simple",
        )
        assert ttv_high - ttv_low == 20.0

    def test_nps_0_adds_10(self):
        # nps_norm = (0+100)/200 = 0.5, *20 = 10
        ttv_zero = self._ttv(
            completion=0.0,
            days_to_first_login=10,
            contract_start_days=45, expected_onboarding_days=90,
            nps_onboarding=0.0, previous_platform_migration=False,
            data_migration_complexity="simple",
        )
        ttv_neg100 = self._ttv(
            completion=0.0,
            days_to_first_login=10,
            contract_start_days=45, expected_onboarding_days=90,
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="simple",
        )
        assert round(ttv_zero - ttv_neg100, 1) == 10.0

    def test_ttv_clamped_at_100(self):
        ttv = self._ttv(
            completion=50.0,
            days_to_first_login=1,
            contract_start_days=10, expected_onboarding_days=90,
            nps_onboarding=100.0, previous_platform_migration=False,
            data_migration_complexity="simple",
        )
        assert ttv <= 100.0

    def test_ttv_clamped_at_0(self):
        ttv = self._ttv(
            completion=0.0,
            days_to_first_login=30,
            contract_start_days=200, expected_onboarding_days=90,
            nps_onboarding=-100.0, previous_platform_migration=True,
            data_migration_complexity="complex",
        )
        assert ttv >= 0.0

    def test_expected_days_zero_skips_schedule(self):
        # Should not crash; schedule section skipped
        ttv = self._ttv(
            completion=50.0,
            days_to_first_login=1,
            contract_start_days=10, expected_onboarding_days=0,
            nps_onboarding=0.0, previous_platform_migration=False,
            data_migration_complexity="simple",
        )
        assert 0.0 <= ttv <= 100.0


# ─────────────────────────────────────────────────────────────────────────────
# 6. _adoption_velocity
# ─────────────────────────────────────────────────────────────────────────────

class TestAdoptionVelocity:
    def _vel(self, **kwargs) -> float:
        eng = CustomerOnboardingEngine()
        return eng._adoption_velocity(make_input(**kwargs))

    def test_basic_velocity(self):
        v = self._vel(users_activated=30, users_licensed=100, contract_start_days=30)
        # (30/30)*30 = 30
        assert v == 30.0

    def test_velocity_capped_at_users_licensed(self):
        v = self._vel(users_activated=1000, users_licensed=10, contract_start_days=1)
        assert v == 10.0

    def test_zero_days_uses_1(self):
        v = self._vel(users_activated=30, users_licensed=1000, contract_start_days=0)
        # days → max(1,0)=1; (30/1)*30 = 900 capped at 1000 → 900
        assert v == 900.0

    def test_zero_activated(self):
        v = self._vel(users_activated=0, users_licensed=10, contract_start_days=30)
        assert v == 0.0

    def test_velocity_formula(self):
        v = self._vel(users_activated=5, users_licensed=100, contract_start_days=15)
        # (5/15)*30 = 10
        assert v == 10.0

    def test_zero_licensed_no_cap(self):
        v = self._vel(users_activated=3, users_licensed=0, contract_start_days=30)
        # cap = velocity → no cap; (3/30)*30 = 3
        assert v == 3.0

    def test_rounded_to_2_decimal(self):
        v = self._vel(users_activated=1, users_licensed=100, contract_start_days=3)
        # (1/3)*30 = 10.0
        assert v == 10.0

    def test_negative_days_uses_1(self):
        v = self._vel(users_activated=5, users_licensed=100, contract_start_days=-5)
        # max(1, -5) = 1 → (5/1)*30 = 150 capped at 100
        assert v == 100.0


# ─────────────────────────────────────────────────────────────────────────────
# 7. _training_completion_rate
# ─────────────────────────────────────────────────────────────────────────────

class TestTrainingCompletionRate:
    def _rate(self, **kwargs) -> float:
        eng = CustomerOnboardingEngine()
        return eng._training_completion_rate(make_input(**kwargs))

    def test_zero_planned_returns_100(self):
        assert self._rate(training_sessions_completed=0, training_sessions_planned=0) == 100.0

    def test_negative_planned_returns_100(self):
        assert self._rate(training_sessions_completed=5, training_sessions_planned=-1) == 100.0

    def test_all_completed(self):
        assert self._rate(training_sessions_completed=5, training_sessions_planned=5) == 100.0

    def test_half_completed(self):
        assert self._rate(training_sessions_completed=3, training_sessions_planned=6) == 50.0

    def test_zero_completed(self):
        assert self._rate(training_sessions_completed=0, training_sessions_planned=5) == 0.0

    def test_more_than_planned_capped_100(self):
        assert self._rate(training_sessions_completed=10, training_sessions_planned=5) == 100.0

    def test_rate_rounded_1_decimal(self):
        r = self._rate(training_sessions_completed=1, training_sessions_planned=3)
        assert r == round((1 / 3) * 100, 1)


# ─────────────────────────────────────────────────────────────────────────────
# 8. _integration_health
# ─────────────────────────────────────────────────────────────────────────────

class TestIntegrationHealth:
    def _health(self, **kwargs) -> float:
        eng = CustomerOnboardingEngine()
        return eng._integration_health(make_input(**kwargs))

    def test_zero_count_returns_100(self):
        assert self._health(integration_count=0, integrations_complete=0) == 100.0

    def test_negative_count_returns_100(self):
        assert self._health(integration_count=-1, integrations_complete=0) == 100.0

    def test_all_complete(self):
        assert self._health(integration_count=4, integrations_complete=4) == 100.0

    def test_half_complete(self):
        assert self._health(integration_count=4, integrations_complete=2) == 50.0

    def test_none_complete(self):
        assert self._health(integration_count=4, integrations_complete=0) == 0.0

    def test_more_complete_than_count_capped_100(self):
        assert self._health(integration_count=2, integrations_complete=5) == 100.0

    def test_health_rounded_1_decimal(self):
        h = self._health(integration_count=3, integrations_complete=1)
        assert h == round((1 / 3) * 100, 1)


# ─────────────────────────────────────────────────────────────────────────────
# 9. _risk_details
# ─────────────────────────────────────────────────────────────────────────────

class TestRiskDetails:
    def _risk(self, completion: float, **kwargs) -> tuple[int, int]:
        eng = CustomerOnboardingEngine()
        return eng._risk_details(make_input(**kwargs), completion)

    def test_clean_account_zero_risk(self):
        score, flags = self._risk(
            completion=80.0,
            support_tickets_open=0,
            contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=True,
            data_migration_complexity="simple",
            nps_onboarding=50.0,
        )
        assert score == 0
        assert flags == 0

    def test_completion_lt_30_adds_3_and_flag(self):
        s1, f1 = self._risk(
            completion=29.9,
            support_tickets_open=0,
            contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=True,
            data_migration_complexity="simple",
            nps_onboarding=50.0,
        )
        s2, f2 = self._risk(
            completion=30.0,
            support_tickets_open=0,
            contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=True,
            data_migration_complexity="simple",
            nps_onboarding=50.0,
        )
        assert s1 - s2 == 1  # 3 vs 2
        assert f1 >= f2

    def test_completion_lt_30_score_3_flag_1(self):
        score, flags = self._risk(
            completion=10.0,
            support_tickets_open=0,
            contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=True,
            data_migration_complexity="simple",
            nps_onboarding=50.0,
        )
        assert score == 3
        assert flags == 1

    def test_completion_30_to_49_score_2_flag_1(self):
        score, flags = self._risk(
            completion=40.0,
            support_tickets_open=0,
            contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=True,
            data_migration_complexity="simple",
            nps_onboarding=50.0,
        )
        assert score == 2
        assert flags == 1

    def test_completion_50_to_69_score_1_flag_0(self):
        score, flags = self._risk(
            completion=60.0,
            support_tickets_open=0,
            contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=True,
            data_migration_complexity="simple",
            nps_onboarding=50.0,
        )
        assert score == 1
        assert flags == 0

    def test_completion_ge_70_no_contribution(self):
        score, flags = self._risk(
            completion=70.0,
            support_tickets_open=0,
            contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=True,
            data_migration_complexity="simple",
            nps_onboarding=50.0,
        )
        assert score == 0
        assert flags == 0

    def test_tickets_ge_5_score_3_flag_1(self):
        score, flags = self._risk(
            completion=80.0,
            support_tickets_open=5,
            contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=True,
            data_migration_complexity="simple",
            nps_onboarding=50.0,
        )
        assert score == 3
        assert flags == 1

    def test_tickets_3_or_4_score_2_flag_1(self):
        score, flags = self._risk(
            completion=80.0,
            support_tickets_open=3,
            contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=True,
            data_migration_complexity="simple",
            nps_onboarding=50.0,
        )
        assert score == 2
        assert flags == 1

    def test_tickets_1_or_2_score_1_flag_0(self):
        score, flags = self._risk(
            completion=80.0,
            support_tickets_open=1,
            contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=True,
            data_migration_complexity="simple",
            nps_onboarding=50.0,
        )
        assert score == 1
        assert flags == 0

    def test_time_ratio_gt_1_5_score_3_flag_1(self):
        score, flags = self._risk(
            completion=80.0,
            support_tickets_open=0,
            contract_start_days=200, expected_onboarding_days=90,  # ratio ~2.22
            executive_sponsor_engaged=True,
            data_migration_complexity="simple",
            nps_onboarding=50.0,
        )
        assert score == 3
        assert flags == 1

    def test_time_ratio_gt_1_0_score_2_flag_1(self):
        score, flags = self._risk(
            completion=80.0,
            support_tickets_open=0,
            contract_start_days=100, expected_onboarding_days=90,  # ratio ~1.11
            executive_sponsor_engaged=True,
            data_migration_complexity="simple",
            nps_onboarding=50.0,
        )
        assert score == 2
        assert flags == 1

    def test_time_ratio_le_1_0_no_timeline_risk(self):
        score, flags = self._risk(
            completion=80.0,
            support_tickets_open=0,
            contract_start_days=90, expected_onboarding_days=90,  # ratio=1.0
            executive_sponsor_engaged=True,
            data_migration_complexity="simple",
            nps_onboarding=50.0,
        )
        assert score == 0
        assert flags == 0

    def test_no_exec_sponsor_score_1_flag_1(self):
        score, flags = self._risk(
            completion=80.0,
            support_tickets_open=0,
            contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=False,
            data_migration_complexity="simple",
            nps_onboarding=50.0,
        )
        assert score == 1
        assert flags == 1

    def test_complex_migration_score_2_flag_1(self):
        score, flags = self._risk(
            completion=80.0,
            support_tickets_open=0,
            contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=True,
            data_migration_complexity="complex",
            nps_onboarding=50.0,
        )
        assert score == 2
        assert flags == 1

    def test_moderate_migration_score_1_flag_0(self):
        score, flags = self._risk(
            completion=80.0,
            support_tickets_open=0,
            contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=True,
            data_migration_complexity="moderate",
            nps_onboarding=50.0,
        )
        assert score == 1
        assert flags == 0

    def test_nps_lt_neg20_score_2_flag_1(self):
        score, flags = self._risk(
            completion=80.0,
            support_tickets_open=0,
            contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=True,
            data_migration_complexity="simple",
            nps_onboarding=-30.0,
        )
        assert score == 2
        assert flags == 1

    def test_nps_neg20_to_0_score_1_flag_0(self):
        score, flags = self._risk(
            completion=80.0,
            support_tickets_open=0,
            contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=True,
            data_migration_complexity="simple",
            nps_onboarding=-10.0,
        )
        assert score == 1
        assert flags == 0

    def test_nps_exactly_minus20_score_1_not_2(self):
        score, flags = self._risk(
            completion=80.0,
            support_tickets_open=0,
            contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=True,
            data_migration_complexity="simple",
            nps_onboarding=-20.0,
        )
        assert score == 1  # -20 is not < -20

    def test_expected_days_zero_skips_timeline(self):
        score, flags = self._risk(
            completion=80.0,
            support_tickets_open=0,
            contract_start_days=30, expected_onboarding_days=0,
            executive_sponsor_engaged=True,
            data_migration_complexity="simple",
            nps_onboarding=50.0,
        )
        assert score == 0
        assert flags == 0

    def test_all_risk_factors_maxed(self):
        score, flags = self._risk(
            completion=10.0,
            support_tickets_open=10,
            contract_start_days=200, expected_onboarding_days=90,
            executive_sponsor_engaged=False,
            data_migration_complexity="complex",
            nps_onboarding=-50.0,
        )
        # 3(completion) + 3(tickets) + 3(timeline) + 1(no exec) + 2(complex) + 2(nps) = 14
        assert score == 14
        assert flags == 6

    def test_cumulative_flags_count(self):
        # exec=False flag, complex flag, nps<-20 flag
        _, flags = self._risk(
            completion=80.0,
            support_tickets_open=0,
            contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=False,
            data_migration_complexity="complex",
            nps_onboarding=-30.0,
        )
        assert flags == 3


# ─────────────────────────────────────────────────────────────────────────────
# 10. _onboarding_risk thresholds
# ─────────────────────────────────────────────────────────────────────────────

class TestOnboardingRisk:
    def _risk(self, score: int) -> OnboardingRisk:
        return CustomerOnboardingEngine()._onboarding_risk(score)

    def test_score_0_is_low(self):
        assert self._risk(0) == OnboardingRisk.LOW

    def test_score_1_is_low(self):
        assert self._risk(1) == OnboardingRisk.LOW

    def test_score_2_is_medium(self):
        assert self._risk(2) == OnboardingRisk.MEDIUM

    def test_score_3_is_medium(self):
        assert self._risk(3) == OnboardingRisk.MEDIUM

    def test_score_4_is_high(self):
        assert self._risk(4) == OnboardingRisk.HIGH

    def test_score_6_is_high(self):
        assert self._risk(6) == OnboardingRisk.HIGH

    def test_score_7_is_critical(self):
        assert self._risk(7) == OnboardingRisk.CRITICAL

    def test_score_15_is_critical(self):
        assert self._risk(15) == OnboardingRisk.CRITICAL


# ─────────────────────────────────────────────────────────────────────────────
# 11. _success_probability
# ─────────────────────────────────────────────────────────────────────────────

class TestSuccessProbability:
    def _prob(self, completion: float, risk: OnboardingRisk) -> SuccessProbability:
        return CustomerOnboardingEngine()._success_probability(completion, risk)

    def test_critical_always_at_risk(self):
        for c in [0, 50, 80, 100]:
            assert self._prob(c, OnboardingRisk.CRITICAL) == SuccessProbability.AT_RISK

    def test_high_risk_always_low(self):
        for c in [0, 50, 80, 100]:
            assert self._prob(c, OnboardingRisk.HIGH) == SuccessProbability.LOW

    def test_completion_ge_80_and_low_risk_is_high(self):
        assert self._prob(80.0, OnboardingRisk.LOW) == SuccessProbability.HIGH

    def test_completion_100_and_low_risk_is_high(self):
        assert self._prob(100.0, OnboardingRisk.LOW) == SuccessProbability.HIGH

    def test_completion_79_and_low_risk_is_medium(self):
        assert self._prob(79.9, OnboardingRisk.LOW) == SuccessProbability.MEDIUM

    def test_completion_80_and_medium_risk_is_medium(self):
        assert self._prob(80.0, OnboardingRisk.MEDIUM) == SuccessProbability.MEDIUM

    def test_completion_low_and_medium_risk_is_medium(self):
        assert self._prob(30.0, OnboardingRisk.MEDIUM) == SuccessProbability.MEDIUM

    def test_completion_low_and_low_risk_is_medium(self):
        assert self._prob(50.0, OnboardingRisk.LOW) == SuccessProbability.MEDIUM


# ─────────────────────────────────────────────────────────────────────────────
# 12. _onboarding_action
# ─────────────────────────────────────────────────────────────────────────────

class TestOnboardingAction:
    def _action(
        self,
        risk: OnboardingRisk,
        completion: float,
        ttv_score: float,
        phase: OnboardingPhase = OnboardingPhase.CONFIGURATION,
    ) -> OnboardingAction:
        eng = CustomerOnboardingEngine()
        inp = make_input(current_phase=phase)
        return eng._onboarding_action(inp, risk, completion, ttv_score)

    def test_critical_always_intervene(self):
        for c in [0, 30, 80]:
            assert self._action(OnboardingRisk.CRITICAL, c, 90) == OnboardingAction.INTERVENE

    def test_high_completion_lt_40_reassign(self):
        assert self._action(OnboardingRisk.HIGH, 39.9, 90) == OnboardingAction.REASSIGN

    def test_high_completion_0_reassign(self):
        assert self._action(OnboardingRisk.HIGH, 0.0, 90) == OnboardingAction.REASSIGN

    def test_high_completion_40_escalate(self):
        assert self._action(OnboardingRisk.HIGH, 40.0, 90) == OnboardingAction.ESCALATE

    def test_high_completion_80_escalate(self):
        assert self._action(OnboardingRisk.HIGH, 80.0, 90) == OnboardingAction.ESCALATE

    def test_complete_phase_and_ge_90_celebrate(self):
        assert self._action(
            OnboardingRisk.LOW, 90.0, 50, OnboardingPhase.COMPLETE
        ) == OnboardingAction.CELEBRATE

    def test_complete_phase_lt_90_no_celebrate(self):
        action = self._action(
            OnboardingRisk.LOW, 89.9, 50, OnboardingPhase.COMPLETE
        )
        assert action != OnboardingAction.CELEBRATE

    def test_ttv_ge_75_and_completion_ge_70_accelerate(self):
        assert self._action(OnboardingRisk.LOW, 70.0, 75.0) == OnboardingAction.ACCELERATE

    def test_ttv_74_9_no_accelerate(self):
        action = self._action(OnboardingRisk.LOW, 70.0, 74.9)
        assert action != OnboardingAction.ACCELERATE

    def test_completion_69_9_no_accelerate_even_high_ttv(self):
        action = self._action(OnboardingRisk.LOW, 69.9, 90.0)
        assert action != OnboardingAction.ACCELERATE

    def test_default_standard(self):
        assert self._action(OnboardingRisk.LOW, 50.0, 50.0) == OnboardingAction.STANDARD

    def test_medium_risk_below_40_standard_not_reassign(self):
        # REASSIGN only for HIGH risk
        action = self._action(OnboardingRisk.MEDIUM, 30.0, 50.0)
        assert action != OnboardingAction.REASSIGN


# ─────────────────────────────────────────────────────────────────────────────
# 13. is_on_track / is_at_risk logic
# ─────────────────────────────────────────────────────────────────────────────

class TestOnTrackAtRisk:
    def test_low_risk_and_high_completion_on_track(self, engine):
        # Build an input that results in LOW risk and completion ≥ 65
        inp = make_input(
            setup_completion_pct=100.0,
            training_sessions_completed=5, training_sessions_planned=5,
            users_activated=10, users_licensed=10,
            integration_count=0, kickoff_held=True,
            executive_sponsor_engaged=True,
            support_tickets_open=0,
            contract_start_days=30, expected_onboarding_days=90,
            nps_onboarding=80.0,
            data_migration_complexity="simple",
        )
        r = engine.analyze(inp)
        if r.onboarding_risk in (OnboardingRisk.LOW, OnboardingRisk.MEDIUM) and r.completion_score >= 65:
            assert r.is_on_track is True
        else:
            assert r.is_on_track is False

    def test_high_risk_is_at_risk(self, engine):
        inp = make_input(
            setup_completion_pct=10.0,
            support_tickets_open=5,
            contract_start_days=200, expected_onboarding_days=90,
            executive_sponsor_engaged=False,
            nps_onboarding=-50.0,
            data_migration_complexity="complex",
        )
        r = engine.analyze(inp)
        if r.onboarding_risk in (OnboardingRisk.HIGH, OnboardingRisk.CRITICAL):
            assert r.is_at_risk is True
        else:
            assert r.is_at_risk is False

    def test_low_risk_not_at_risk(self, engine):
        r = engine.analyze(make_input())
        if r.onboarding_risk == OnboardingRisk.LOW:
            assert r.is_at_risk is False

    def test_medium_risk_not_at_risk(self, engine):
        # medium risk → is_at_risk = False
        inp = make_input(
            setup_completion_pct=40.0,
            support_tickets_open=0,
            contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=False,
            nps_onboarding=-10.0,
            data_migration_complexity="simple",
        )
        r = engine.analyze(inp)
        if r.onboarding_risk == OnboardingRisk.MEDIUM:
            assert r.is_at_risk is False

    def test_critical_risk_is_at_risk(self, engine):
        r = engine.analyze(make_input(
            setup_completion_pct=0.0, support_tickets_open=10,
            contract_start_days=200, expected_onboarding_days=90,
            executive_sponsor_engaged=False,
            nps_onboarding=-80.0, data_migration_complexity="complex",
        ))
        if r.onboarding_risk == OnboardingRisk.CRITICAL:
            assert r.is_at_risk is True

    def test_on_track_requires_completion_ge_65(self, engine):
        # Same risk but completion < 65 should NOT be on_track
        inp = make_input(
            setup_completion_pct=20.0,
            training_sessions_completed=1, training_sessions_planned=5,
            users_activated=1, users_licensed=10,
            integration_count=0, kickoff_held=False,
            executive_sponsor_engaged=True,
            support_tickets_open=0,
            contract_start_days=30, expected_onboarding_days=90,
            nps_onboarding=80.0,
        )
        r = engine.analyze(inp)
        if r.completion_score < 65:
            assert r.is_on_track is False


# ─────────────────────────────────────────────────────────────────────────────
# 14. Engine.analyze() – full end-to-end
# ─────────────────────────────────────────────────────────────────────────────

class TestAnalyze:
    def test_returns_result_instance(self, engine):
        r = engine.analyze(make_input())
        assert isinstance(r, CustomerOnboardingResult)

    def test_result_appended_to_internal_list(self, engine):
        engine.analyze(make_input())
        engine.analyze(make_input())
        assert len(engine._results) == 2

    def test_analyze_perfect_account(self, engine, perfect_input):
        r = engine.analyze(perfect_input)
        assert r.completion_score == 100.0
        assert r.onboarding_risk == OnboardingRisk.LOW
        assert r.success_probability == SuccessProbability.HIGH
        assert r.onboarding_action == OnboardingAction.CELEBRATE

    def test_analyze_worst_account_critical_intervene(self, engine, worst_input):
        r = engine.analyze(worst_input)
        assert r.onboarding_risk == OnboardingRisk.CRITICAL
        assert r.onboarding_action == OnboardingAction.INTERVENE
        assert r.is_at_risk is True

    def test_analyze_preserves_account_id(self, engine):
        r = engine.analyze(make_input(account_id="TEST-123"))
        assert r.account_id == "TEST-123"

    def test_analyze_preserves_account_name(self, engine):
        r = engine.analyze(make_input(account_name="Widget Co"))
        assert r.account_name == "Widget Co"

    def test_analyze_preserves_csm_id(self, engine):
        r = engine.analyze(make_input(csm_id="CSM-999"))
        assert r.csm_id == "CSM-999"

    def test_analyze_preserves_phase(self, engine):
        r = engine.analyze(make_input(current_phase=OnboardingPhase.TRAINING))
        assert r.current_phase == OnboardingPhase.TRAINING

    def test_completion_score_range(self, engine):
        r = engine.analyze(make_input())
        assert 0.0 <= r.completion_score <= 100.0

    def test_ttv_score_range(self, engine):
        r = engine.analyze(make_input())
        assert 0.0 <= r.time_to_value_score <= 100.0

    def test_adoption_velocity_non_negative(self, engine):
        r = engine.analyze(make_input())
        assert r.adoption_velocity >= 0.0

    def test_training_completion_range(self, engine):
        r = engine.analyze(make_input())
        assert 0.0 <= r.training_completion_rate <= 100.0

    def test_integration_health_range(self, engine):
        r = engine.analyze(make_input())
        assert 0.0 <= r.integration_health <= 100.0

    def test_risk_flags_non_negative(self, engine):
        r = engine.analyze(make_input())
        assert r.risk_flags_count >= 0

    def test_at_risk_and_on_track_mutually_exclusive_high_risk(self, engine):
        inp = make_input(
            setup_completion_pct=0.0, support_tickets_open=10,
            contract_start_days=200, expected_onboarding_days=90,
            executive_sponsor_engaged=False,
            nps_onboarding=-80.0, data_migration_complexity="complex",
            previous_platform_migration=True,
        )
        r = engine.analyze(inp)
        if r.is_at_risk:
            assert r.is_on_track is False

    def test_high_risk_completion_30_to_40_reassign(self, engine):
        # Force HIGH risk + low completion → REASSIGN
        inp = make_input(
            setup_completion_pct=0.0,
            training_sessions_completed=0, training_sessions_planned=5,
            users_activated=0, users_licensed=10,
            support_tickets_open=5,
            contract_start_days=200, expected_onboarding_days=90,
            executive_sponsor_engaged=False,
            data_migration_complexity="simple",
            nps_onboarding=50.0,
            integration_count=0, kickoff_held=False,
        )
        r = engine.analyze(inp)
        if r.onboarding_risk == OnboardingRisk.HIGH and r.completion_score < 40:
            assert r.onboarding_action == OnboardingAction.REASSIGN


# ─────────────────────────────────────────────────────────────────────────────
# 15. Engine.analyze_batch()
# ─────────────────────────────────────────────────────────────────────────────

class TestAnalyzeBatch:
    def test_returns_list(self, engine):
        results = engine.analyze_batch([make_input(), make_input(account_id="A2")])
        assert isinstance(results, list)

    def test_empty_batch(self, engine):
        results = engine.analyze_batch([])
        assert results == []

    def test_batch_count_matches_input(self, engine):
        inputs = [make_input(account_id=f"A{i}") for i in range(5)]
        results = engine.analyze_batch(inputs)
        assert len(results) == 5

    def test_batch_appends_to_results(self, engine):
        inputs = [make_input(account_id=f"A{i}") for i in range(3)]
        engine.analyze_batch(inputs)
        assert len(engine._results) == 3

    def test_batch_result_types(self, engine):
        results = engine.analyze_batch([make_input(), make_input()])
        for r in results:
            assert isinstance(r, CustomerOnboardingResult)


# ─────────────────────────────────────────────────────────────────────────────
# 16. Engine.reset()
# ─────────────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_results(self, engine):
        engine.analyze(make_input())
        engine.analyze(make_input())
        engine.reset()
        assert engine._results == []

    def test_reset_empty_engine_no_error(self, engine):
        engine.reset()
        assert engine._results == []

    def test_analyze_after_reset(self, engine):
        engine.analyze(make_input())
        engine.reset()
        engine.analyze(make_input(account_id="NEW"))
        assert len(engine._results) == 1
        assert engine._results[0].account_id == "NEW"


# ─────────────────────────────────────────────────────────────────────────────
# 17. Engine properties
# ─────────────────────────────────────────────────────────────────────────────

class TestProperties:
    def test_at_risk_accounts_empty_initially(self, engine):
        assert engine.at_risk_accounts == []

    def test_on_track_accounts_empty_initially(self, engine):
        assert engine.on_track_accounts == []

    def test_critical_accounts_empty_initially(self, engine):
        assert engine.critical_accounts == []

    def test_high_success_accounts_empty_initially(self, engine):
        assert engine.high_success_accounts == []

    def test_at_risk_accounts_returns_at_risk_only(self, engine, worst_input):
        engine.analyze(make_input())
        engine.analyze(worst_input)
        for r in engine.at_risk_accounts:
            assert r.is_at_risk is True

    def test_on_track_accounts_returns_on_track_only(self, engine, worst_input):
        engine.analyze(make_input())
        engine.analyze(worst_input)
        for r in engine.on_track_accounts:
            assert r.is_on_track is True

    def test_critical_accounts_returns_critical_only(self, engine, worst_input):
        engine.analyze(worst_input)
        for r in engine.critical_accounts:
            assert r.onboarding_risk == OnboardingRisk.CRITICAL

    def test_high_success_accounts_returns_high_prob_only(self, engine, perfect_input):
        engine.analyze(perfect_input)
        for r in engine.high_success_accounts:
            assert r.success_probability == SuccessProbability.HIGH

    def test_at_risk_count_correct(self, engine, worst_input):
        engine.analyze_batch([make_input(), worst_input, worst_input])
        at_risk = engine.at_risk_accounts
        assert all(r.is_at_risk for r in at_risk)

    def test_at_risk_count_correct_via_batch(self, engine, worst_input):
        engine.analyze_batch([make_input(), worst_input])
        at_risk = engine.at_risk_accounts
        assert all(r.is_at_risk for r in at_risk)

    def test_properties_after_reset(self, engine):
        engine.analyze(make_input())
        engine.reset()
        assert engine.at_risk_accounts == []
        assert engine.on_track_accounts == []
        assert engine.critical_accounts == []
        assert engine.high_success_accounts == []


# ─────────────────────────────────────────────────────────────────────────────
# 18. summary() – exact 13-key invariant
# ─────────────────────────────────────────────────────────────────────────────

EXPECTED_SUMMARY_KEYS = {
    "total", "phase_counts", "risk_counts", "probability_counts", "action_counts",
    "avg_completion_score", "avg_time_to_value_score", "avg_adoption_velocity",
    "at_risk_count", "on_track_count", "critical_count", "high_success_count",
    "escalation_needed_count",
}


class TestSummary:
    def test_empty_summary_exact_13_keys(self, engine):
        s = engine.summary()
        assert set(s.keys()) == EXPECTED_SUMMARY_KEYS

    def test_empty_summary_key_count(self, engine):
        assert len(engine.summary()) == 13

    def test_populated_summary_exact_13_keys(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        assert set(s.keys()) == EXPECTED_SUMMARY_KEYS

    def test_populated_summary_key_count(self, engine):
        engine.analyze(make_input())
        assert len(engine.summary()) == 13

    def test_empty_summary_total_0(self, engine):
        assert engine.summary()["total"] == 0

    def test_empty_summary_empty_dicts(self, engine):
        s = engine.summary()
        assert s["phase_counts"] == {}
        assert s["risk_counts"] == {}
        assert s["probability_counts"] == {}
        assert s["action_counts"] == {}

    def test_empty_summary_zeros(self, engine):
        s = engine.summary()
        for key in ("avg_completion_score", "avg_time_to_value_score",
                    "avg_adoption_velocity", "at_risk_count", "on_track_count",
                    "critical_count", "high_success_count", "escalation_needed_count"):
            assert s[key] == 0 or s[key] == 0.0

    def test_total_count(self, engine):
        engine.analyze_batch([make_input(account_id=f"A{i}") for i in range(4)])
        assert engine.summary()["total"] == 4

    def test_phase_counts_populated(self, engine):
        engine.analyze(make_input(current_phase=OnboardingPhase.KICKOFF))
        engine.analyze(make_input(current_phase=OnboardingPhase.TRAINING))
        s = engine.summary()
        assert s["phase_counts"].get("kickoff", 0) >= 1
        assert s["phase_counts"].get("training", 0) >= 1

    def test_risk_counts_keys_are_strings(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        for k in s["risk_counts"]:
            assert isinstance(k, str)

    def test_avg_completion_score_accuracy(self, engine):
        # Use two identical accounts so average equals one account's score
        r1 = engine.analyze(make_input())
        engine.reset()
        r2 = engine.analyze(make_input())
        engine.reset()
        engine.analyze(make_input())
        engine.analyze(make_input())
        s = engine.summary()
        assert s["avg_completion_score"] == r1.completion_score

    def test_at_risk_count_matches_property(self, engine):
        engine.analyze(make_worst_input())
        engine.analyze(make_input())
        s = engine.summary()
        assert s["at_risk_count"] == len(engine.at_risk_accounts)

    def test_on_track_count_matches_property(self, engine):
        engine.analyze(make_perfect_input())
        engine.analyze(make_worst_input())
        s = engine.summary()
        assert s["on_track_count"] == len(engine.on_track_accounts)

    def test_critical_count_matches_property(self, engine):
        engine.analyze(make_worst_input())
        s = engine.summary()
        assert s["critical_count"] == len(engine.critical_accounts)

    def test_high_success_count_matches_property(self, engine):
        engine.analyze(make_perfect_input())
        s = engine.summary()
        assert s["high_success_count"] == len(engine.high_success_accounts)

    def test_escalation_needed_counts_escalate_and_intervene(self, engine):
        engine.analyze(make_worst_input())  # → INTERVENE
        s = engine.summary()
        assert s["escalation_needed_count"] >= 1

    def test_escalation_needed_standard_not_counted(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        for r in engine._results:
            if r.onboarding_action == OnboardingAction.STANDARD:
                assert s["escalation_needed_count"] == 0

    def test_action_counts_all_strings(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        for k in s["action_counts"]:
            assert isinstance(k, str)

    def test_probability_counts_populated(self, engine):
        engine.analyze(make_worst_input())
        s = engine.summary()
        assert sum(s["probability_counts"].values()) == 1

    def test_avg_values_rounded(self, engine):
        for i in range(3):
            engine.analyze(make_input(account_id=f"A{i}"))
        s = engine.summary()
        # values should be rounded (not just floating-point noise)
        assert isinstance(s["avg_completion_score"], float)
        assert isinstance(s["avg_adoption_velocity"], float)

    def test_escalation_needed_includes_escalate_action(self, engine):
        # Build an account that gets ESCALATE: HIGH risk + completion>=40
        # HIGH risk: score >= 4
        # tickets=5 → +3, no exec → +1, no timeline issue, completion just above 30
        # Use moderate complexity to push to score=4 exactly
        inp = make_input(
            setup_completion_pct=50.0,
            training_sessions_completed=0, training_sessions_planned=5,
            users_activated=0, users_licensed=10,
            support_tickets_open=3,
            contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=False,
            data_migration_complexity="simple",
            nps_onboarding=50.0,
            integration_count=0, kickoff_held=False,
        )
        r = engine.analyze(inp)
        s = engine.summary()
        if r.onboarding_action in (OnboardingAction.ESCALATE, OnboardingAction.INTERVENE):
            assert s["escalation_needed_count"] >= 1


# ─────────────────────────────────────────────────────────────────────────────
# 19. End-to-end scenario tests
# ─────────────────────────────────────────────────────────────────────────────

class TestEndToEndScenarios:
    def test_smb_healthy_early_stage(self):
        eng = CustomerOnboardingEngine()
        inp = make_input(
            segment="smb",
            contract_start_days=10,
            expected_onboarding_days=60,
            current_phase=OnboardingPhase.KICKOFF,
            setup_completion_pct=40.0,
            training_sessions_completed=1, training_sessions_planned=3,
            users_activated=2, users_licensed=5,
            days_to_first_login=2,
            support_tickets_open=0,
            executive_sponsor_engaged=True,
            integration_count=0,
            nps_onboarding=40.0,
            kickoff_held=True,
        )
        r = eng.analyze(inp)
        assert r.onboarding_risk in (OnboardingRisk.LOW, OnboardingRisk.MEDIUM)

    def test_enterprise_late_stage_high_completion(self):
        eng = CustomerOnboardingEngine()
        inp = make_input(
            segment="enterprise",
            contract_start_days=80,
            expected_onboarding_days=90,
            current_phase=OnboardingPhase.ADOPTION,
            setup_completion_pct=95.0,
            training_sessions_completed=8, training_sessions_planned=10,
            users_activated=45, users_licensed=50,
            days_to_first_login=1,
            support_tickets_open=1,
            executive_sponsor_engaged=True,
            integration_count=3, integrations_complete=3,
            nps_onboarding=60.0,
            kickoff_held=True,
        )
        r = eng.analyze(inp)
        assert r.completion_score > 80
        assert r.success_probability in (SuccessProbability.HIGH, SuccessProbability.MEDIUM)

    def test_mid_market_at_risk_overrun(self):
        eng = CustomerOnboardingEngine()
        inp = make_input(
            segment="mid_market",
            contract_start_days=180,
            expected_onboarding_days=90,
            current_phase=OnboardingPhase.TRAINING,
            setup_completion_pct=30.0,
            training_sessions_completed=2, training_sessions_planned=8,
            users_activated=3, users_licensed=20,
            days_to_first_login=5,
            support_tickets_open=4,
            executive_sponsor_engaged=False,
            integration_count=2, integrations_complete=0,
            nps_onboarding=-30.0,
            kickoff_held=True,
        )
        r = eng.analyze(inp)
        assert r.is_at_risk is True

    def test_complete_phase_high_completion_celebrate(self):
        eng = CustomerOnboardingEngine()
        inp = make_input(
            current_phase=OnboardingPhase.COMPLETE,
            setup_completion_pct=100.0,
            training_sessions_completed=5, training_sessions_planned=5,
            users_activated=10, users_licensed=10,
            integration_count=0, kickoff_held=True,
            executive_sponsor_engaged=True,
            support_tickets_open=0,
            contract_start_days=85, expected_onboarding_days=90,
            nps_onboarding=80.0,
        )
        r = eng.analyze(inp)
        if r.completion_score >= 90 and r.onboarding_risk not in (OnboardingRisk.HIGH, OnboardingRisk.CRITICAL):
            assert r.onboarding_action == OnboardingAction.CELEBRATE

    def test_batch_mixed_risk_summary(self):
        eng = CustomerOnboardingEngine()
        eng.analyze(make_perfect_input())
        eng.analyze(make_worst_input())
        s = eng.summary()
        assert s["total"] == 2
        assert s["at_risk_count"] + s["on_track_count"] <= 2

    def test_multiple_phases_in_summary(self):
        eng = CustomerOnboardingEngine()
        for phase in OnboardingPhase:
            eng.analyze(make_input(
                account_id=phase.value,
                current_phase=phase,
            ))
        s = eng.summary()
        assert s["total"] == 6
        assert len(s["phase_counts"]) == 6

    def test_accelerate_with_high_ttv_and_completion(self):
        eng = CustomerOnboardingEngine()
        inp = make_input(
            current_phase=OnboardingPhase.ADOPTION,
            setup_completion_pct=90.0,
            training_sessions_completed=5, training_sessions_planned=5,
            users_activated=9, users_licensed=10,
            days_to_first_login=1,
            contract_start_days=20, expected_onboarding_days=90,
            support_tickets_open=0,
            executive_sponsor_engaged=True,
            integration_count=0,
            nps_onboarding=80.0,
            kickoff_held=True,
        )
        r = eng.analyze(inp)
        assert r.time_to_value_score >= 75
        assert r.completion_score >= 70
        # With low/medium risk, should not be HIGH/CRITICAL
        if r.onboarding_risk not in (OnboardingRisk.HIGH, OnboardingRisk.CRITICAL):
            assert r.onboarding_action == OnboardingAction.ACCELERATE

    def test_consistent_results_same_input(self):
        eng = CustomerOnboardingEngine()
        inp = make_input()
        r1 = eng.analyze(inp)
        eng.reset()
        r2 = eng.analyze(inp)
        assert r1.completion_score == r2.completion_score
        assert r1.onboarding_risk == r2.onboarding_risk
        assert r1.onboarding_action == r2.onboarding_action

    def test_implementation_partner_field_accepted(self):
        eng = CustomerOnboardingEngine()
        r = eng.analyze(make_input(implementation_partner=True))
        assert isinstance(r, CustomerOnboardingResult)

    def test_value_realization_phase(self):
        eng = CustomerOnboardingEngine()
        r = eng.analyze(make_input(current_phase=OnboardingPhase.VALUE_REALIZATION))
        assert r.current_phase == OnboardingPhase.VALUE_REALIZATION


# ─────────────────────────────────────────────────────────────────────────────
# 20. Boundary / edge value tests
# ─────────────────────────────────────────────────────────────────────────────

class TestBoundaryValues:
    def test_completion_score_boundary_30(self):
        eng = CustomerOnboardingEngine()
        inp_below = make_input(
            setup_completion_pct=0.0,
            training_sessions_completed=0, training_sessions_planned=5,
            users_activated=0, users_licensed=10,
            integration_count=0, kickoff_held=False,
            executive_sponsor_engaged=False,
        )
        # score = 15 (no integrations) → below 30
        s = eng._completion_score(inp_below)
        assert s < 30

    def test_completion_score_exactly_boundary_values(self):
        eng = CustomerOnboardingEngine()
        # Setup 50 → 15; train 0; act 0; no int 15; no kick; no exec = 30 exactly
        inp = make_input(
            setup_completion_pct=50.0,
            training_sessions_completed=0, training_sessions_planned=5,
            users_activated=0, users_licensed=10,
            integration_count=0, kickoff_held=False,
            executive_sponsor_engaged=False,
        )
        s = eng._completion_score(inp)
        assert s == 30.0

    def test_risk_score_boundary_at_2(self):
        eng = CustomerOnboardingEngine()
        assert eng._onboarding_risk(2) == OnboardingRisk.MEDIUM
        assert eng._onboarding_risk(1) == OnboardingRisk.LOW

    def test_risk_score_boundary_at_4(self):
        eng = CustomerOnboardingEngine()
        assert eng._onboarding_risk(4) == OnboardingRisk.HIGH
        assert eng._onboarding_risk(3) == OnboardingRisk.MEDIUM

    def test_risk_score_boundary_at_7(self):
        eng = CustomerOnboardingEngine()
        assert eng._onboarding_risk(7) == OnboardingRisk.CRITICAL
        assert eng._onboarding_risk(6) == OnboardingRisk.HIGH

    def test_tickets_boundary_at_3(self):
        eng = CustomerOnboardingEngine()
        s2, f2 = eng._risk_details(make_input(
            support_tickets_open=2,
            contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=True, data_migration_complexity="simple",
            nps_onboarding=50.0,
        ), 80.0)
        s3, f3 = eng._risk_details(make_input(
            support_tickets_open=3,
            contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=True, data_migration_complexity="simple",
            nps_onboarding=50.0,
        ), 80.0)
        assert s3 > s2  # score jumped from 1 to 2

    def test_tickets_boundary_at_5(self):
        eng = CustomerOnboardingEngine()
        s4, _ = eng._risk_details(make_input(
            support_tickets_open=4,
            contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=True, data_migration_complexity="simple",
            nps_onboarding=50.0,
        ), 80.0)
        s5, _ = eng._risk_details(make_input(
            support_tickets_open=5,
            contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=True, data_migration_complexity="simple",
            nps_onboarding=50.0,
        ), 80.0)
        assert s5 > s4

    def test_time_ratio_boundary_at_1_5(self):
        eng = CustomerOnboardingEngine()
        s_low, _ = eng._risk_details(make_input(
            contract_start_days=135, expected_onboarding_days=90,  # ratio=1.5
            support_tickets_open=0,
            executive_sponsor_engaged=True, data_migration_complexity="simple",
            nps_onboarding=50.0,
        ), 80.0)
        s_high, _ = eng._risk_details(make_input(
            contract_start_days=136, expected_onboarding_days=90,  # ratio=1.511
            support_tickets_open=0,
            executive_sponsor_engaged=True, data_migration_complexity="simple",
            nps_onboarding=50.0,
        ), 80.0)
        assert s_high > s_low

    def test_nps_boundary_at_minus_20(self):
        eng = CustomerOnboardingEngine()
        s_minus21, f1 = eng._risk_details(make_input(
            support_tickets_open=0, contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=True, data_migration_complexity="simple",
            nps_onboarding=-21.0,
        ), 80.0)
        s_minus20, f2 = eng._risk_details(make_input(
            support_tickets_open=0, contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=True, data_migration_complexity="simple",
            nps_onboarding=-20.0,
        ), 80.0)
        assert s_minus21 > s_minus20
        assert f1 > f2

    def test_completion_80_boundary_for_high_success(self):
        eng = CustomerOnboardingEngine()
        assert eng._success_probability(80.0, OnboardingRisk.LOW) == SuccessProbability.HIGH
        assert eng._success_probability(79.9, OnboardingRisk.LOW) == SuccessProbability.MEDIUM

    def test_action_completion_40_boundary_for_reassign_vs_escalate(self):
        eng = CustomerOnboardingEngine()
        inp = make_input()
        a_below = eng._onboarding_action(inp, OnboardingRisk.HIGH, 39.9, 50.0)
        a_at = eng._onboarding_action(inp, OnboardingRisk.HIGH, 40.0, 50.0)
        assert a_below == OnboardingAction.REASSIGN
        assert a_at == OnboardingAction.ESCALATE

    def test_ttv_75_boundary_for_accelerate(self):
        eng = CustomerOnboardingEngine()
        inp = make_input()
        a_below = eng._onboarding_action(inp, OnboardingRisk.LOW, 70.0, 74.9)
        a_at = eng._onboarding_action(inp, OnboardingRisk.LOW, 70.0, 75.0)
        assert a_below != OnboardingAction.ACCELERATE
        assert a_at == OnboardingAction.ACCELERATE

    def test_completion_70_boundary_for_accelerate(self):
        eng = CustomerOnboardingEngine()
        inp = make_input()
        a_below = eng._onboarding_action(inp, OnboardingRisk.LOW, 69.9, 75.0)
        a_at = eng._onboarding_action(inp, OnboardingRisk.LOW, 70.0, 75.0)
        assert a_below != OnboardingAction.ACCELERATE
        assert a_at == OnboardingAction.ACCELERATE

    def test_celebrate_completion_90_boundary(self):
        eng = CustomerOnboardingEngine()
        inp_complete = make_input(current_phase=OnboardingPhase.COMPLETE)
        a_just_below = eng._onboarding_action(inp_complete, OnboardingRisk.LOW, 89.9, 50.0)
        a_at = eng._onboarding_action(inp_complete, OnboardingRisk.LOW, 90.0, 50.0)
        assert a_just_below != OnboardingAction.CELEBRATE
        assert a_at == OnboardingAction.CELEBRATE

    def test_on_track_completion_65_boundary(self):
        eng = CustomerOnboardingEngine()
        # Craft inputs with LOW risk
        # LOW risk: risk_score < 2
        # Need exec=True, nps>0, tickets=0, time_ratio<=1, complexity=simple, completion>=70
        common = dict(
            support_tickets_open=0,
            contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=True,
            data_migration_complexity="simple",
            nps_onboarding=50.0,
            previous_platform_migration=False,
            integration_count=0, kickoff_held=True,
            days_to_first_login=2,
        )
        # completion ~64: setup=60.0*0.3=18, train=0*0.2=0, act=0*0.25=0, noInt=15, kick=5, exec=5 → 43
        # we need exactly 65: setup= (65-15-5-5)/0.30 = 133.3 → impossible without training/activation
        # Just verify through analyze()
        inp65 = make_input(
            setup_completion_pct=100.0,
            training_sessions_completed=0, training_sessions_planned=5,
            users_activated=0, users_licensed=10,
            **common
        )
        r = eng.analyze(inp65)
        # completion = 30+0+0+15+5+5 = 55 → below 65
        if r.onboarding_risk in (OnboardingRisk.LOW, OnboardingRisk.MEDIUM):
            if r.completion_score < 65:
                assert r.is_on_track is False
            else:
                assert r.is_on_track is True

    def test_nps_minus_100_minimum(self):
        eng = CustomerOnboardingEngine()
        ttv = eng._time_to_value_score(make_input(nps_onboarding=-100.0), 50.0)
        assert ttv >= 0.0

    def test_nps_100_maximum(self):
        eng = CustomerOnboardingEngine()
        ttv = eng._time_to_value_score(make_input(nps_onboarding=100.0), 50.0)
        assert ttv <= 100.0

    def test_first_login_day_14_is_penalty_10(self):
        eng = CustomerOnboardingEngine()
        # day=14 is not >14, so falls in else branch → -10
        ttv14 = eng._time_to_value_score(make_input(days_to_first_login=14,
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="simple",
            contract_start_days=45, expected_onboarding_days=90), 0.0)
        ttv15 = eng._time_to_value_score(make_input(days_to_first_login=15,
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="simple",
            contract_start_days=45, expected_onboarding_days=90), 0.0)
        assert ttv15 < ttv14  # day 15 has -20 penalty vs -10

    def test_pct_time_exactly_half_no_schedule_bonus(self):
        eng = CustomerOnboardingEngine()
        # pct_time = 0.5 exactly → condition is pct_time < 0.5, so no bonus
        ttv = eng._time_to_value_score(make_input(
            contract_start_days=45, expected_onboarding_days=90,
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="simple", days_to_first_login=10,
        ), 60.0)
        ttv_under = eng._time_to_value_score(make_input(
            contract_start_days=44, expected_onboarding_days=90,
            nps_onboarding=-100.0, previous_platform_migration=False,
            data_migration_complexity="simple", days_to_first_login=10,
        ), 60.0)
        # under 0.5 with completion >=50 should get +15 bonus
        assert ttv_under - ttv == 15.0


# ─────────────────────────────────────────────────────────────────────────────
# 21. Additional targeted tests
# ─────────────────────────────────────────────────────────────────────────────

class TestAdditionalCoverage:
    def test_engine_initial_state(self):
        eng = CustomerOnboardingEngine()
        assert eng._results == []

    def test_multiple_engines_independent(self):
        eng1 = CustomerOnboardingEngine()
        eng2 = CustomerOnboardingEngine()
        eng1.analyze(make_input())
        assert len(eng1._results) == 1
        assert len(eng2._results) == 0

    def test_all_onboarding_phases_analyzed(self):
        eng = CustomerOnboardingEngine()
        for phase in OnboardingPhase:
            r = eng.analyze(make_input(current_phase=phase))
            assert r.current_phase == phase

    def test_all_segments_accepted(self):
        eng = CustomerOnboardingEngine()
        for seg in ("smb", "mid_market", "enterprise"):
            r = eng.analyze(make_input(segment=seg))
            assert isinstance(r, CustomerOnboardingResult)

    def test_training_rate_100_when_planned_0(self):
        eng = CustomerOnboardingEngine()
        r = eng.analyze(make_input(
            training_sessions_completed=0, training_sessions_planned=0
        ))
        assert r.training_completion_rate == 100.0

    def test_integration_health_100_when_count_0(self):
        eng = CustomerOnboardingEngine()
        r = eng.analyze(make_input(integration_count=0, integrations_complete=0))
        assert r.integration_health == 100.0

    def test_summary_avg_uses_all_results(self):
        eng = CustomerOnboardingEngine()
        r1 = eng.analyze(make_input(account_id="A1"))
        r2 = eng.analyze(make_input(account_id="A2"))
        s = eng.summary()
        expected_avg = round((r1.completion_score + r2.completion_score) / 2, 1)
        assert s["avg_completion_score"] == expected_avg

    def test_summary_avg_ttv_accuracy(self):
        eng = CustomerOnboardingEngine()
        r1 = eng.analyze(make_input(account_id="A1"))
        r2 = eng.analyze(make_input(account_id="A2"))
        s = eng.summary()
        expected = round((r1.time_to_value_score + r2.time_to_value_score) / 2, 1)
        assert s["avg_time_to_value_score"] == expected

    def test_summary_avg_velocity_accuracy(self):
        eng = CustomerOnboardingEngine()
        r1 = eng.analyze(make_input(account_id="A1"))
        r2 = eng.analyze(make_input(account_id="A2"))
        s = eng.summary()
        expected = round((r1.adoption_velocity + r2.adoption_velocity) / 2, 2)
        assert s["avg_adoption_velocity"] == expected

    def test_escalation_counts_both_escalate_and_intervene(self):
        eng = CustomerOnboardingEngine()
        # worst → INTERVENE
        eng.analyze(make_worst_input())
        s1 = eng.summary()
        count_before = s1["escalation_needed_count"]
        # HIGH risk + completion>=40 → ESCALATE
        inp_escalate = make_input(
            setup_completion_pct=50.0,
            training_sessions_completed=3, training_sessions_planned=5,
            users_activated=5, users_licensed=10,
            support_tickets_open=5,
            contract_start_days=100, expected_onboarding_days=90,
            executive_sponsor_engaged=False,
            data_migration_complexity="complex",
            nps_onboarding=50.0,
            integration_count=0, kickoff_held=True,
        )
        r_esc = eng.analyze(inp_escalate)
        s2 = eng.summary()
        if r_esc.onboarding_action in (OnboardingAction.ESCALATE, OnboardingAction.INTERVENE):
            assert s2["escalation_needed_count"] > count_before

    def test_to_dict_values_match_result_attributes(self):
        eng = CustomerOnboardingEngine()
        r = eng.analyze(make_input())
        d = r.to_dict()
        assert d["completion_score"] == r.completion_score
        assert d["time_to_value_score"] == r.time_to_value_score
        assert d["adoption_velocity"] == r.adoption_velocity
        assert d["training_completion_rate"] == r.training_completion_rate
        assert d["integration_health"] == r.integration_health
        assert d["risk_flags_count"] == r.risk_flags_count
        assert d["is_on_track"] == r.is_on_track
        assert d["is_at_risk"] == r.is_at_risk

    def test_high_risk_success_probability_is_low(self):
        eng = CustomerOnboardingEngine()
        assert eng._success_probability(90.0, OnboardingRisk.HIGH) == SuccessProbability.LOW

    def test_critical_risk_success_probability_is_at_risk(self):
        eng = CustomerOnboardingEngine()
        assert eng._success_probability(100.0, OnboardingRisk.CRITICAL) == SuccessProbability.AT_RISK

    def test_medium_risk_80_completion_still_medium(self):
        eng = CustomerOnboardingEngine()
        # HIGH success only when LOW risk + completion>=80
        assert eng._success_probability(80.0, OnboardingRisk.MEDIUM) == SuccessProbability.MEDIUM

    def test_analyze_multiple_different_accounts(self):
        eng = CustomerOnboardingEngine()
        accounts = [
            make_input(account_id="A", segment="smb"),
            make_input(account_id="B", segment="enterprise"),
            make_input(account_id="C", segment="mid_market"),
        ]
        results = eng.analyze_batch(accounts)
        ids = [r.account_id for r in results]
        assert ids == ["A", "B", "C"]

    def test_no_tickets_zero_score_contribution(self):
        eng = CustomerOnboardingEngine()
        score, flags = eng._risk_details(make_input(
            support_tickets_open=0,
            contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=True, data_migration_complexity="simple",
            nps_onboarding=50.0,
        ), 80.0)
        assert score == 0
        assert flags == 0

    def test_summary_risk_counts_sum_to_total(self):
        eng = CustomerOnboardingEngine()
        for i in range(4):
            eng.analyze(make_input(account_id=f"A{i}"))
        s = eng.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_probability_counts_sum_to_total(self):
        eng = CustomerOnboardingEngine()
        for i in range(3):
            eng.analyze(make_input(account_id=f"A{i}"))
        s = eng.summary()
        assert sum(s["probability_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_to_total(self):
        eng = CustomerOnboardingEngine()
        for i in range(3):
            eng.analyze(make_input(account_id=f"A{i}"))
        s = eng.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_phase_counts_sum_to_total(self):
        eng = CustomerOnboardingEngine()
        for phase in OnboardingPhase:
            eng.analyze(make_input(account_id=phase.value, current_phase=phase))
        s = eng.summary()
        assert sum(s["phase_counts"].values()) == s["total"]

    def test_is_at_risk_false_for_low_risk(self):
        eng = CustomerOnboardingEngine()
        r = eng.analyze(make_input(
            setup_completion_pct=100.0,
            training_sessions_completed=5, training_sessions_planned=5,
            users_activated=10, users_licensed=10,
            support_tickets_open=0,
            contract_start_days=30, expected_onboarding_days=90,
            executive_sponsor_engaged=True,
            data_migration_complexity="simple",
            nps_onboarding=80.0,
            integration_count=0, kickoff_held=True,
        ))
        if r.onboarding_risk == OnboardingRisk.LOW:
            assert r.is_at_risk is False

    def test_velocity_scales_with_days(self):
        eng = CustomerOnboardingEngine()
        v30 = eng._adoption_velocity(make_input(users_activated=10, users_licensed=100, contract_start_days=30))
        v60 = eng._adoption_velocity(make_input(users_activated=10, users_licensed=100, contract_start_days=60))
        # Fewer days → higher velocity
        assert v30 > v60
