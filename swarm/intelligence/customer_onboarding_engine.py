from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class OnboardingPhase(str, Enum):
    KICKOFF           = "kickoff"
    CONFIGURATION     = "configuration"
    TRAINING          = "training"
    ADOPTION          = "adoption"
    VALUE_REALIZATION = "value_realization"
    COMPLETE          = "complete"


class OnboardingRisk(str, Enum):
    LOW      = "low"
    MEDIUM   = "medium"
    HIGH     = "high"
    CRITICAL = "critical"


class SuccessProbability(str, Enum):
    HIGH    = "high"
    MEDIUM  = "medium"
    LOW     = "low"
    AT_RISK = "at_risk"


class OnboardingAction(str, Enum):
    ACCELERATE = "accelerate"
    STANDARD   = "standard"
    ESCALATE   = "escalate"
    REASSIGN   = "reassign"
    INTERVENE  = "intervene"
    CELEBRATE  = "celebrate"


@dataclass
class CustomerOnboardingInput:
    account_id:                  str
    account_name:                str
    csm_id:                      str
    segment:                     str              # smb / mid_market / enterprise
    contract_start_days:         int              # days since contract start
    expected_onboarding_days:    int              # target onboarding duration
    current_phase:               OnboardingPhase
    setup_completion_pct:        float            # 0–100
    training_sessions_completed: int
    training_sessions_planned:   int
    users_activated:             int
    users_licensed:              int
    days_to_first_login:         int
    support_tickets_open:        int
    support_tickets_resolved:    int
    executive_sponsor_engaged:   bool
    implementation_partner:      bool
    integration_count:           int
    integrations_complete:       int
    nps_onboarding:              float            # -100 to 100
    previous_platform_migration: bool
    data_migration_complexity:   str              # "simple" / "moderate" / "complex"
    kickoff_held:                bool


@dataclass
class CustomerOnboardingResult:
    account_id:               str
    account_name:             str
    csm_id:                   str
    current_phase:            OnboardingPhase
    onboarding_risk:          OnboardingRisk
    success_probability:      SuccessProbability
    onboarding_action:        OnboardingAction
    completion_score:         float    # 0–100 composite
    time_to_value_score:      float    # 0–100 (higher = better trajectory)
    adoption_velocity:        float    # activated users per 30 days
    training_completion_rate: float    # 0–100
    integration_health:       float    # 0–100
    risk_flags_count:         int
    is_on_track:              bool
    is_at_risk:               bool

    def to_dict(self) -> dict:
        return {
            "account_id":               self.account_id,
            "account_name":             self.account_name,
            "csm_id":                   self.csm_id,
            "current_phase":            self.current_phase.value,
            "onboarding_risk":          self.onboarding_risk.value,
            "success_probability":      self.success_probability.value,
            "onboarding_action":        self.onboarding_action.value,
            "completion_score":         self.completion_score,
            "time_to_value_score":      self.time_to_value_score,
            "adoption_velocity":        self.adoption_velocity,
            "training_completion_rate": self.training_completion_rate,
            "integration_health":       self.integration_health,
            "risk_flags_count":         self.risk_flags_count,
            "is_on_track":              self.is_on_track,
            "is_at_risk":               self.is_at_risk,
        }


class CustomerOnboardingEngine:
    def __init__(self) -> None:
        self._results: list[CustomerOnboardingResult] = []

    # ── public API ─────────────────────────────────────────────────────────────

    def analyze(self, inp: CustomerOnboardingInput) -> CustomerOnboardingResult:
        completion   = self._completion_score(inp)
        ttv_score    = self._time_to_value_score(inp, completion)
        adoption_vel = self._adoption_velocity(inp)
        train_rate   = self._training_completion_rate(inp)
        int_health   = self._integration_health(inp)
        risk_score, flags = self._risk_details(inp, completion)
        risk         = self._onboarding_risk(risk_score)
        success_prob = self._success_probability(completion, risk)
        action       = self._onboarding_action(inp, risk, completion, ttv_score)
        on_track     = risk in (OnboardingRisk.LOW, OnboardingRisk.MEDIUM) and completion >= 65
        at_risk      = risk in (OnboardingRisk.HIGH, OnboardingRisk.CRITICAL)

        result = CustomerOnboardingResult(
            account_id=inp.account_id,
            account_name=inp.account_name,
            csm_id=inp.csm_id,
            current_phase=inp.current_phase,
            onboarding_risk=risk,
            success_probability=success_prob,
            onboarding_action=action,
            completion_score=completion,
            time_to_value_score=ttv_score,
            adoption_velocity=adoption_vel,
            training_completion_rate=train_rate,
            integration_health=int_health,
            risk_flags_count=flags,
            is_on_track=on_track,
            is_at_risk=at_risk,
        )
        self._results.append(result)
        return result

    def analyze_batch(
        self, inputs: list[CustomerOnboardingInput]
    ) -> list[CustomerOnboardingResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ─────────────────────────────────────────────────────────────

    @property
    def at_risk_accounts(self) -> list[CustomerOnboardingResult]:
        return [r for r in self._results if r.is_at_risk]

    @property
    def on_track_accounts(self) -> list[CustomerOnboardingResult]:
        return [r for r in self._results if r.is_on_track]

    @property
    def critical_accounts(self) -> list[CustomerOnboardingResult]:
        return [r for r in self._results if r.onboarding_risk == OnboardingRisk.CRITICAL]

    @property
    def high_success_accounts(self) -> list[CustomerOnboardingResult]:
        return [r for r in self._results if r.success_probability == SuccessProbability.HIGH]

    # ── scoring helpers ────────────────────────────────────────────────────────

    def _completion_score(self, inp: CustomerOnboardingInput) -> float:
        score = 0.0
        # Setup progress (30%)
        score += inp.setup_completion_pct * 0.30
        # Training progress (20%)
        if inp.training_sessions_planned > 0:
            train_rate = min(1.0, inp.training_sessions_completed / inp.training_sessions_planned)
            score += train_rate * 100 * 0.20
        # User activation (25%)
        if inp.users_licensed > 0:
            act_rate = min(1.0, inp.users_activated / inp.users_licensed)
            score += act_rate * 100 * 0.25
        # Integration progress (15%)
        if inp.integration_count > 0:
            int_rate = min(1.0, inp.integrations_complete / inp.integration_count)
            score += int_rate * 100 * 0.15
        else:
            score += 15.0  # full credit when no integrations required
        # Kickoff held (+5)
        if inp.kickoff_held:
            score += 5.0
        # Executive engaged (+5)
        if inp.executive_sponsor_engaged:
            score += 5.0
        return round(max(0.0, min(100.0, score)), 1)

    def _time_to_value_score(
        self, inp: CustomerOnboardingInput, completion: float
    ) -> float:
        score = 50.0
        # First login speed
        if inp.days_to_first_login <= 1:    score += 20.0
        elif inp.days_to_first_login <= 3:  score += 15.0
        elif inp.days_to_first_login <= 7:  score += 5.0
        elif inp.days_to_first_login > 14:  score -= 20.0
        else:                               score -= 10.0
        # Schedule adherence
        if inp.expected_onboarding_days > 0:
            pct_time = inp.contract_start_days / inp.expected_onboarding_days
            if pct_time < 0.5 and completion >= 50:  score += 15.0
            elif pct_time > 1.5:                     score -= 20.0
            elif pct_time > 1.0:                     score -= 10.0
        # Complexity penalties
        if inp.previous_platform_migration:               score -= 10.0
        if inp.data_migration_complexity == "complex":    score -= 15.0
        elif inp.data_migration_complexity == "moderate": score -= 5.0
        # NPS sentiment during onboarding
        nps_norm = (inp.nps_onboarding + 100) / 200  # 0–1
        score += nps_norm * 20.0
        return round(max(0.0, min(100.0, score)), 1)

    def _adoption_velocity(self, inp: CustomerOnboardingInput) -> float:
        days = max(1, inp.contract_start_days)
        velocity = (inp.users_activated / days) * 30.0
        cap = float(inp.users_licensed) if inp.users_licensed > 0 else velocity
        return round(min(cap, velocity), 2)

    def _training_completion_rate(self, inp: CustomerOnboardingInput) -> float:
        if inp.training_sessions_planned <= 0:
            return 100.0
        return round(min(100.0, (inp.training_sessions_completed / inp.training_sessions_planned) * 100), 1)

    def _integration_health(self, inp: CustomerOnboardingInput) -> float:
        if inp.integration_count <= 0:
            return 100.0
        return round(min(100.0, (inp.integrations_complete / inp.integration_count) * 100), 1)

    def _risk_details(
        self, inp: CustomerOnboardingInput, completion: float
    ) -> tuple[int, int]:
        risk_score = 0
        flags = 0

        # Completion risk
        if completion < 30:
            risk_score += 3; flags += 1
        elif completion < 50:
            risk_score += 2; flags += 1
        elif completion < 70:
            risk_score += 1

        # Support overload
        if inp.support_tickets_open >= 5:
            risk_score += 3; flags += 1
        elif inp.support_tickets_open >= 3:
            risk_score += 2; flags += 1
        elif inp.support_tickets_open >= 1:
            risk_score += 1

        # Timeline overrun
        if inp.expected_onboarding_days > 0:
            time_ratio = inp.contract_start_days / inp.expected_onboarding_days
            if time_ratio > 1.5:
                risk_score += 3; flags += 1
            elif time_ratio > 1.0:
                risk_score += 2; flags += 1

        # No executive sponsor
        if not inp.executive_sponsor_engaged:
            risk_score += 1; flags += 1

        # Data migration complexity
        if inp.data_migration_complexity == "complex":
            risk_score += 2; flags += 1
        elif inp.data_migration_complexity == "moderate":
            risk_score += 1

        # Negative onboarding sentiment
        if inp.nps_onboarding < -20:
            risk_score += 2; flags += 1
        elif inp.nps_onboarding < 0:
            risk_score += 1

        return risk_score, flags

    def _onboarding_risk(self, risk_score: int) -> OnboardingRisk:
        if risk_score >= 7: return OnboardingRisk.CRITICAL
        if risk_score >= 4: return OnboardingRisk.HIGH
        if risk_score >= 2: return OnboardingRisk.MEDIUM
        return OnboardingRisk.LOW

    def _success_probability(
        self, completion: float, risk: OnboardingRisk
    ) -> SuccessProbability:
        if risk == OnboardingRisk.CRITICAL:
            return SuccessProbability.AT_RISK
        if risk == OnboardingRisk.HIGH:
            return SuccessProbability.LOW
        if completion >= 80 and risk == OnboardingRisk.LOW:
            return SuccessProbability.HIGH
        return SuccessProbability.MEDIUM

    def _onboarding_action(
        self,
        inp: CustomerOnboardingInput,
        risk: OnboardingRisk,
        completion: float,
        ttv_score: float,
    ) -> OnboardingAction:
        if risk == OnboardingRisk.CRITICAL:
            return OnboardingAction.INTERVENE
        if risk == OnboardingRisk.HIGH:
            if completion < 40:
                return OnboardingAction.REASSIGN
            return OnboardingAction.ESCALATE
        if inp.current_phase == OnboardingPhase.COMPLETE and completion >= 90:
            return OnboardingAction.CELEBRATE
        if ttv_score >= 75 and completion >= 70:
            return OnboardingAction.ACCELERATE
        return OnboardingAction.STANDARD

    # ── summary ────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                   0,
                "phase_counts":            {},
                "risk_counts":             {},
                "probability_counts":      {},
                "action_counts":           {},
                "avg_completion_score":    0.0,
                "avg_time_to_value_score": 0.0,
                "avg_adoption_velocity":   0.0,
                "at_risk_count":           0,
                "on_track_count":          0,
                "critical_count":          0,
                "high_success_count":      0,
                "escalation_needed_count": 0,
            }

        phase_counts: dict[str, int] = {}
        risk_counts:  dict[str, int] = {}
        prob_counts:  dict[str, int] = {}
        action_counts: dict[str, int] = {}
        total_completion = 0.0
        total_ttv        = 0.0
        total_velocity   = 0.0

        for r in self._results:
            phase_counts[r.current_phase.value]       = phase_counts.get(r.current_phase.value, 0) + 1
            risk_counts[r.onboarding_risk.value]      = risk_counts.get(r.onboarding_risk.value, 0) + 1
            prob_counts[r.success_probability.value]  = prob_counts.get(r.success_probability.value, 0) + 1
            action_counts[r.onboarding_action.value]  = action_counts.get(r.onboarding_action.value, 0) + 1
            total_completion += r.completion_score
            total_ttv        += r.time_to_value_score
            total_velocity   += r.adoption_velocity

        escalation_needed = sum(
            1 for r in self._results
            if r.onboarding_action in (OnboardingAction.ESCALATE, OnboardingAction.INTERVENE)
        )

        return {
            "total":                   n,
            "phase_counts":            phase_counts,
            "risk_counts":             risk_counts,
            "probability_counts":      prob_counts,
            "action_counts":           action_counts,
            "avg_completion_score":    round(total_completion / n, 1),
            "avg_time_to_value_score": round(total_ttv / n, 1),
            "avg_adoption_velocity":   round(total_velocity / n, 2),
            "at_risk_count":           len(self.at_risk_accounts),
            "on_track_count":          len(self.on_track_accounts),
            "critical_count":          len(self.critical_accounts),
            "high_success_count":      len(self.high_success_accounts),
            "escalation_needed_count": escalation_needed,
        }
