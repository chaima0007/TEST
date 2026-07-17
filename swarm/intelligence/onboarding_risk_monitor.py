from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class OnboardingRisk(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class OnboardingAction(str, Enum):
    MONITOR = "monitor"
    ACCELERATE = "accelerate"
    RESCUE = "rescue"
    ESCALATE = "escalate"


class OnboardingPhase(str, Enum):
    KICKOFF = "kickoff"
    SETUP = "setup"
    TRAINING = "training"
    ADOPTION = "adoption"
    VALUE_REALIZATION = "value_realization"


class ChurnSignal(str, Enum):
    NONE = "none"
    EARLY = "early"
    MODERATE = "moderate"
    STRONG = "strong"


@dataclass
class OnboardingInput:
    customer_id: str
    customer_name: str
    arr_eur: float
    segment: str              # enterprise / mid_market / smb
    phase: OnboardingPhase
    # Timeline
    days_since_contract: int
    expected_go_live_days: int  # contractual go-live target
    actual_go_live_days: int    # 0 if not yet live
    # Engagement
    exec_sponsor_active: bool
    champion_engaged: bool
    training_completion_pct: float   # 0-100
    users_activated_pct: float       # 0-100
    # Product usage
    first_value_achieved: bool  # completed first key use case
    integrations_completed: int
    integrations_planned: int
    # Support & blockers
    open_blockers: int
    escalated_tickets: int
    # CS touchpoints
    last_cs_contact_days: int
    kickoff_completed: bool
    health_check_completed: bool


@dataclass
class OnboardingResult:
    customer_id: str
    customer_name: str
    arr_eur: float
    segment: str
    phase: OnboardingPhase
    risk_score: float
    risk_level: OnboardingRisk
    risk_action: OnboardingAction
    churn_signal: ChurnSignal
    go_live_delay_days: int       # positive = behind schedule
    risk_factors: list[str]
    positive_signals: list[str]
    intervention_plan: list[str]
    time_to_value_score: float    # 0-100

    def to_dict(self) -> dict:
        return {
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "arr_eur": self.arr_eur,
            "segment": self.segment,
            "phase": self.phase.value,
            "risk_score": self.risk_score,
            "risk_level": self.risk_level.value,
            "risk_action": self.risk_action.value,
            "churn_signal": self.churn_signal.value,
            "go_live_delay_days": self.go_live_delay_days,
            "risk_factors": self.risk_factors,
            "positive_signals": self.positive_signals,
            "intervention_plan": self.intervention_plan,
            "time_to_value_score": self.time_to_value_score,
        }


def _go_live_delay(inp: OnboardingInput) -> int:
    if inp.actual_go_live_days > 0:
        return inp.actual_go_live_days - inp.expected_go_live_days
    # Still in onboarding — estimate delay from today
    if inp.days_since_contract > inp.expected_go_live_days:
        return inp.days_since_contract - inp.expected_go_live_days
    return 0


def _risk_score(inp: OnboardingInput) -> float:
    score = 0.0

    # Timeline risk (max 30)
    delay = _go_live_delay(inp)
    if delay >= 30:
        score += 30.0
    elif delay >= 14:
        score += 20.0
    elif delay >= 7:
        score += 10.0

    # Engagement risk (max 25)
    if not inp.exec_sponsor_active:
        score += 10.0
    if not inp.champion_engaged:
        score += 8.0
    if inp.training_completion_pct < 30:
        score += 7.0
    elif inp.training_completion_pct < 60:
        score += 3.0

    # Adoption risk (max 20)
    if inp.users_activated_pct < 20:
        score += 12.0
    elif inp.users_activated_pct < 50:
        score += 6.0
    if not inp.first_value_achieved and inp.days_since_contract > 30:
        score += 8.0

    # Blocker risk (max 15)
    score += min(10.0, inp.open_blockers * 3.0)
    score += min(5.0, inp.escalated_tickets * 2.5)

    # CS engagement risk (max 10)
    if not inp.kickoff_completed:
        score += 5.0
    if inp.last_cs_contact_days > 14:
        score += 5.0
    elif inp.last_cs_contact_days > 7:
        score += 2.0

    return round(min(100.0, max(0.0, score)), 1)


def _risk_level(score: float) -> OnboardingRisk:
    if score >= 65:
        return OnboardingRisk.CRITICAL
    if score >= 40:
        return OnboardingRisk.HIGH
    if score >= 20:
        return OnboardingRisk.MODERATE
    return OnboardingRisk.LOW


def _risk_action(level: OnboardingRisk, inp: OnboardingInput) -> OnboardingAction:
    if level == OnboardingRisk.CRITICAL or inp.escalated_tickets >= 2:
        return OnboardingAction.ESCALATE
    if level == OnboardingRisk.HIGH:
        return OnboardingAction.RESCUE
    if level == OnboardingRisk.MODERATE:
        return OnboardingAction.ACCELERATE
    return OnboardingAction.MONITOR


def _churn_signal(score: float, inp: OnboardingInput) -> ChurnSignal:
    if score >= 65 or inp.escalated_tickets >= 2:
        return ChurnSignal.STRONG
    if score >= 40 or not inp.exec_sponsor_active:
        return ChurnSignal.MODERATE
    if score >= 20:
        return ChurnSignal.EARLY
    return ChurnSignal.NONE


def _time_to_value_score(inp: OnboardingInput) -> float:
    score = 0.0
    if inp.first_value_achieved:
        score += 35.0
    if inp.users_activated_pct >= 50:
        score += 25.0
    elif inp.users_activated_pct >= 25:
        score += 12.0
    integrations_ratio = (
        inp.integrations_completed / inp.integrations_planned
        if inp.integrations_planned > 0 else 0.0
    )
    score += integrations_ratio * 20.0
    if inp.training_completion_pct >= 80:
        score += 20.0
    elif inp.training_completion_pct >= 50:
        score += 10.0
    return round(min(100.0, max(0.0, score)), 1)


def _risk_factors(inp: OnboardingInput, delay: int) -> list[str]:
    factors: list[str] = []
    if delay >= 14:
        factors.append(f"Go-live en retard de {delay}j sur la date contractuelle")
    if not inp.exec_sponsor_active:
        factors.append("Sponsor exécutif inactif — manque d'alignement stratégique")
    if not inp.champion_engaged:
        factors.append("Champion non engagé — risque de dérive du projet")
    if inp.training_completion_pct < 30:
        factors.append(f"Formation insuffisante — {inp.training_completion_pct:.0f}% seulement complétée")
    if inp.users_activated_pct < 20:
        factors.append(f"Adoption utilisateurs faible — {inp.users_activated_pct:.0f}% activés")
    if not inp.first_value_achieved and inp.days_since_contract > 30:
        factors.append("Aucun cas d'usage validé après 30j — Time-to-Value compromis")
    if inp.open_blockers >= 2:
        factors.append(f"{inp.open_blockers} blocages ouverts — progression bloquée")
    if inp.escalated_tickets >= 1:
        factors.append(f"{inp.escalated_tickets} ticket(s) escaladé(s) — problème produit critique")
    if not inp.kickoff_completed:
        factors.append("Kickoff non réalisé — base de l'onboarding manquante")
    if inp.last_cs_contact_days > 14:
        factors.append(f"Dernier contact CS il y a {inp.last_cs_contact_days}j — relation négligée")
    return factors


def _positive_signals(inp: OnboardingInput) -> list[str]:
    signals: list[str] = []
    if inp.first_value_achieved:
        signals.append("Premier cas d'usage validé — Time-to-Value atteint")
    if inp.exec_sponsor_active:
        signals.append("Sponsor exécutif actif — engagement fort du côté client")
    if inp.champion_engaged:
        signals.append("Champion engagé — relai interne efficace")
    if inp.training_completion_pct >= 80:
        signals.append(f"Formation avancée — {inp.training_completion_pct:.0f}% complétée")
    if inp.users_activated_pct >= 50:
        signals.append(f"Adoption solide — {inp.users_activated_pct:.0f}% des utilisateurs actifs")
    if inp.kickoff_completed:
        signals.append("Kickoff réalisé — projet sur les rails")
    if inp.health_check_completed:
        signals.append("Health check effectué — risques identifiés et adressés")
    if inp.open_blockers == 0:
        signals.append("Aucun blocage ouvert — progression fluide")
    if inp.integrations_completed >= inp.integrations_planned and inp.integrations_planned > 0:
        signals.append(f"Toutes les intégrations complétées ({inp.integrations_completed}/{inp.integrations_planned})")
    return signals


def _intervention_plan(
    level: OnboardingRisk, action: OnboardingAction, inp: OnboardingInput, delay: int
) -> list[str]:
    plan: list[str] = []
    if action == OnboardingAction.ESCALATE:
        plan.append("Escalade C-level immédiate — mobiliser direction et executive sponsor")
        plan.append("War room onboarding — réunion quotidienne jusqu'à résolution")
        if inp.open_blockers >= 1:
            plan.append("Résoudre les blocages en priorité absolue — task force technique")
    elif action == OnboardingAction.RESCUE:
        plan.append("Appel de rescue urgente — identifier les freins et rebloquer le projet")
        plan.append("Renforcer le champion interne — contacter nouvelles personas")
        if not inp.first_value_achieved:
            plan.append("Définir un quickwin à 14j — démontrer la valeur rapidement")
    elif action == OnboardingAction.ACCELERATE:
        plan.append("Accélérer le plan de formation — sessions intensives à planifier")
        plan.append("Identifier les utilisateurs bloqués et les accompagner")
        if delay > 7:
            plan.append("Réviser le planning avec le client — redéfinir les jalons")
    else:
        plan.append("Maintenir la cadence de contact hebdomadaire")
        plan.append("Suivre les jalons du plan d'implémentation")
        plan.append("Préparer l'évaluation de satisfaction à J+90")
    return plan


class OnboardingRiskMonitorEngine:
    def __init__(self) -> None:
        self._results: dict[str, OnboardingResult] = {}

    def monitor(self, inp: OnboardingInput) -> OnboardingResult:
        delay = _go_live_delay(inp)
        score = _risk_score(inp)
        level = _risk_level(score)
        action = _risk_action(level, inp)
        churn = _churn_signal(score, inp)
        result = OnboardingResult(
            customer_id=inp.customer_id,
            customer_name=inp.customer_name,
            arr_eur=inp.arr_eur,
            segment=inp.segment,
            phase=inp.phase,
            risk_score=score,
            risk_level=level,
            risk_action=action,
            churn_signal=churn,
            go_live_delay_days=delay,
            risk_factors=_risk_factors(inp, delay),
            positive_signals=_positive_signals(inp),
            intervention_plan=_intervention_plan(level, action, inp, delay),
            time_to_value_score=_time_to_value_score(inp),
        )
        self._results[inp.customer_id] = result
        return result

    def monitor_batch(self, customers: list[OnboardingInput]) -> list[OnboardingResult]:
        results = [self.monitor(c) for c in customers]
        return sorted(results, key=lambda r: r.risk_score, reverse=True)

    def all_customers(self) -> list[OnboardingResult]:
        return sorted(self._results.values(), key=lambda r: r.risk_score, reverse=True)

    def by_risk(self, level: OnboardingRisk) -> list[OnboardingResult]:
        return [r for r in self._results.values() if r.risk_level == level]

    def by_action(self, action: OnboardingAction) -> list[OnboardingResult]:
        return [r for r in self._results.values() if r.risk_action == action]

    def by_phase(self, phase: OnboardingPhase) -> list[OnboardingResult]:
        return [r for r in self._results.values() if r.phase == phase]

    def critical_customers(self) -> list[OnboardingResult]:
        return self.by_risk(OnboardingRisk.CRITICAL)

    def needs_escalation(self) -> list[OnboardingResult]:
        return self.by_action(OnboardingAction.ESCALATE)

    def at_risk_customers(self) -> list[OnboardingResult]:
        return [
            r for r in self._results.values()
            if r.risk_level in (OnboardingRisk.HIGH, OnboardingRisk.CRITICAL)
        ]

    def behind_schedule(self) -> list[OnboardingResult]:
        return [r for r in self._results.values() if r.go_live_delay_days > 0]

    def achieved_value(self) -> list[OnboardingResult]:
        return [r for r in self._results.values() if r.time_to_value_score >= 50]

    def avg_risk_score(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.risk_score for r in self._results.values()) / len(self._results), 1)

    def avg_time_to_value(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.time_to_value_score for r in self._results.values()) / len(self._results), 1)

    def total_arr_at_risk_eur(self) -> float:
        return sum(
            r.arr_eur for r in self._results.values()
            if r.risk_level in (OnboardingRisk.HIGH, OnboardingRisk.CRITICAL)
        )

    def summary(self) -> dict:
        all_r = list(self._results.values())
        n = len(all_r)
        return {
            "total": n,
            "risk_counts": {r.value: sum(1 for x in all_r if x.risk_level == r) for r in OnboardingRisk},
            "action_counts": {a.value: sum(1 for x in all_r if x.risk_action == a) for a in OnboardingAction},
            "phase_counts": {p.value: sum(1 for x in all_r if x.phase == p) for p in OnboardingPhase},
            "avg_risk_score": self.avg_risk_score(),
            "avg_time_to_value": self.avg_time_to_value(),
            "critical_count": len(self.critical_customers()),
            "behind_schedule_count": len(self.behind_schedule()),
            "total_arr_at_risk_eur": self.total_arr_at_risk_eur(),
        }

    def reset(self) -> None:
        self._results.clear()
