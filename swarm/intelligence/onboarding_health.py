"""Onboarding Health Monitor — tracks new customer onboarding milestones and flags at-risk accounts."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional


class OnboardingStatus(str, Enum):
    ON_TRACK = "on_track"       # score >= 75
    AT_RISK = "at_risk"         # score >= 50
    DELAYED = "delayed"         # score >= 25
    CRITICAL = "critical"       # score < 25


class OnboardingAction(str, Enum):
    CELEBRATE = "celebrate"     # go-live done, prepare handoff to CS
    ACCELERATE = "accelerate"   # active push needed to complete on time
    RESCUE = "rescue"           # significant intervention required
    MONITOR = "monitor"         # regular check-ins sufficient


@dataclass
class OnboardingInput:
    account_id: str
    account_name: str
    arr_eur: float

    # Timeline
    contract_start_days: int        # days elapsed since contract start
    target_go_live_days: int        # planned days from start to go-live

    # Milestone completion
    kickoff_done: bool
    technical_setup_pct: float      # 0-100
    data_migration_pct: float       # 0-100
    integrations_pct: float         # 0-100
    user_training_pct: float        # 0-100
    uat_pct: float                  # User Acceptance Testing 0-100
    go_live_done: bool

    # Team engagement
    customer_pm_engaged: bool       # customer has assigned a project manager
    executive_sponsor_active: bool
    dedicated_csm_assigned: bool    # our CSM assigned

    # Health signals
    integration_blockers: int       # number of active blockers
    support_tickets_open: int
    days_since_last_contact: int
    nps_at_onboarding: int          # -100 to 100 (-999 if not yet recorded)


@dataclass
class OnboardingResult:
    account_id: str
    account_name: str
    arr_eur: float
    onboarding_status: OnboardingStatus
    onboarding_action: OnboardingAction
    overall_score: float
    milestone_score: float
    engagement_score: float
    health_score: float
    completion_pct: float           # overall milestone weighted completion
    days_remaining: int             # positive = days left; negative = overdue
    schedule_delta_pct: float       # actual vs expected completion (+ = ahead)
    blockers: list[str]             # active issues blocking progress
    achievements: list[str]         # completed/positive signals
    recommended_actions: list[str]
    go_live_done: bool

    def to_dict(self) -> dict:
        d = asdict(self)
        d["onboarding_status"] = self.onboarding_status.value
        d["onboarding_action"] = self.onboarding_action.value
        return d


# ─── Milestone weights (must sum to 100) ─────────────────────────────────────

_MILESTONE_WEIGHTS = {
    "kickoff":    5,
    "technical":  25,
    "migration":  20,
    "integrations": 20,
    "training":   15,
    "uat":        10,
    "go_live":    5,
}


def _milestone_score(inp: OnboardingInput) -> tuple[float, float]:
    """Returns (milestone_score 0-100, completion_pct 0-100)."""
    vals = {
        "kickoff":      100.0 if inp.kickoff_done else 0.0,
        "technical":    max(0, min(100, inp.technical_setup_pct)),
        "migration":    max(0, min(100, inp.data_migration_pct)),
        "integrations": max(0, min(100, inp.integrations_pct)),
        "training":     max(0, min(100, inp.user_training_pct)),
        "uat":          max(0, min(100, inp.uat_pct)),
        "go_live":      100.0 if inp.go_live_done else 0.0,
    }
    weighted = sum(vals[k] * _MILESTONE_WEIGHTS[k] for k in vals) / 100
    return round(weighted, 2), round(weighted, 2)


def _engagement_score(inp: OnboardingInput) -> float:
    score = 0.0
    if inp.customer_pm_engaged:
        score += 35
    if inp.executive_sponsor_active:
        score += 30
    if inp.dedicated_csm_assigned:
        score += 25
    if inp.days_since_last_contact <= 3:
        score += 10
    elif inp.days_since_last_contact <= 7:
        score += 5
    elif inp.days_since_last_contact > 14:
        score -= 15
    return round(max(0, min(100, score)), 2)


def _health_score(inp: OnboardingInput) -> float:
    score = 100.0
    blocker_penalty = min(45, inp.integration_blockers * 15)
    ticket_penalty = min(25, inp.support_tickets_open * 5)
    score -= blocker_penalty + ticket_penalty
    if inp.days_since_last_contact > 14:
        score -= 15
    elif inp.days_since_last_contact > 7:
        score -= 5
    if inp.nps_at_onboarding != -999:
        if inp.nps_at_onboarding < -10:
            score -= 20
        elif inp.nps_at_onboarding < 0:
            score -= 10
        elif inp.nps_at_onboarding > 30:
            score += 10
    return round(max(0, min(100, score)), 2)


def _overall_score(milestone: float, engagement: float, health: float) -> float:
    return round(milestone * 0.55 + engagement * 0.25 + health * 0.20, 2)


def _schedule_delta(inp: OnboardingInput, completion: float) -> float:
    if inp.target_go_live_days <= 0:
        return 0.0
    expected_pct = min(100, inp.contract_start_days / inp.target_go_live_days * 100)
    return round(completion - expected_pct, 1)


def _onboarding_status(score: float) -> OnboardingStatus:
    if score >= 75:
        return OnboardingStatus.ON_TRACK
    if score >= 50:
        return OnboardingStatus.AT_RISK
    if score >= 25:
        return OnboardingStatus.DELAYED
    return OnboardingStatus.CRITICAL


def _onboarding_action(
    inp: OnboardingInput,
    status: OnboardingStatus,
    delta: float,
) -> OnboardingAction:
    if inp.go_live_done:
        return OnboardingAction.CELEBRATE
    if status == OnboardingStatus.CRITICAL:
        return OnboardingAction.RESCUE
    if status in (OnboardingStatus.AT_RISK, OnboardingStatus.DELAYED):
        return OnboardingAction.ACCELERATE
    # ON_TRACK
    if delta < -10:
        return OnboardingAction.ACCELERATE
    return OnboardingAction.MONITOR


def _build_signals(
    inp: OnboardingInput,
    completion: float,
    delta: float,
    days_remaining: int,
) -> tuple[list[str], list[str], list[str]]:
    blockers: list[str] = []
    achievements: list[str] = []
    actions: list[str] = []

    # Blockers
    if inp.integration_blockers > 0:
        blockers.append(f"{inp.integration_blockers} bloqueur(s) d'intégration actif(s)")
    if inp.support_tickets_open > 0:
        blockers.append(f"{inp.support_tickets_open} ticket(s) support ouvert(s)")
    if not inp.kickoff_done:
        blockers.append("Kickoff non effectué — onboarding non démarré")
    if inp.technical_setup_pct < 50 and inp.contract_start_days > 14:
        blockers.append(f"Configuration technique à {inp.technical_setup_pct:.0f}% après {inp.contract_start_days}j")
    if inp.data_migration_pct < 50 and inp.contract_start_days > 21:
        blockers.append(f"Migration données à {inp.data_migration_pct:.0f}% après {inp.contract_start_days}j")
    if delta < -20:
        blockers.append(f"Retard de {abs(delta):.0f}% sur le planning prévu")
    if days_remaining < 0:
        blockers.append(f"Go-live en retard de {-days_remaining}j sur la date cible")
    if not inp.customer_pm_engaged:
        blockers.append("Aucun chef de projet côté client désigné")
    if inp.days_since_last_contact > 14:
        blockers.append(f"Aucun contact depuis {inp.days_since_last_contact}j")

    # Achievements
    if inp.go_live_done:
        achievements.append("Go-live complété — onboarding réussi!")
    if inp.kickoff_done:
        achievements.append("Kickoff effectué — onboarding lancé")
    if inp.technical_setup_pct >= 90:
        achievements.append(f"Configuration technique quasi-complète ({inp.technical_setup_pct:.0f}%)")
    if inp.data_migration_pct >= 90:
        achievements.append(f"Migration données quasi-complète ({inp.data_migration_pct:.0f}%)")
    if inp.user_training_pct >= 80:
        achievements.append(f"Formation utilisateurs avancée ({inp.user_training_pct:.0f}%)")
    if inp.executive_sponsor_active:
        achievements.append("Sponsor exécutif client actif — bon alignement stratégique")
    if inp.dedicated_csm_assigned:
        achievements.append("CSM dédié assigné — accompagnement personnalisé")
    if delta > 10:
        achievements.append(f"En avance de {delta:.0f}% sur le planning — bon rythme!")
    if inp.nps_at_onboarding != -999 and inp.nps_at_onboarding > 30:
        achievements.append(f"NPS onboarding positif ({inp.nps_at_onboarding})")

    # Recommended actions
    if inp.integration_blockers > 0:
        actions.append(f"Résoudre en urgence les {inp.integration_blockers} bloqueur(s) d'intégration")
    if not inp.kickoff_done:
        actions.append("Planifier le kickoff immédiatement")
    if inp.technical_setup_pct < 30:
        actions.append("Escalader la configuration technique — appel avec l'équipe d'implémentation")
    if inp.data_migration_pct < 30 and inp.contract_start_days > 14:
        actions.append("Lancer la migration des données — ressources à débloquer")
    if not inp.customer_pm_engaged:
        actions.append("Demander la désignation d'un PM côté client")
    if not inp.executive_sponsor_active:
        actions.append("Activer le sponsor exécutif pour débloquer les ressources")
    if inp.days_since_last_contact > 7:
        actions.append(f"Reprendre contact — {inp.days_since_last_contact}j sans interaction")
    if inp.user_training_pct < 50 and inp.uat_pct > 50:
        actions.append("Planifier les sessions de formation avant UAT complet")
    if days_remaining > 0 and days_remaining <= 14:
        actions.append(f"Intensifier le rythme — go-live dans {days_remaining}j")
    if inp.go_live_done:
        actions.append("Planifier la revue post-onboarding et passation au CSM")

    return blockers, achievements, actions


class OnboardingHealthMonitor:
    """Tracks new customer onboarding milestones and flags at-risk accounts."""

    def __init__(self) -> None:
        self._results: dict[str, OnboardingResult] = {}

    def assess(self, inp: OnboardingInput) -> OnboardingResult:
        milestone, completion = _milestone_score(inp)
        engagement = _engagement_score(inp)
        health = _health_score(inp)
        overall = _overall_score(milestone, engagement, health)

        delta = _schedule_delta(inp, completion)
        days_remaining = inp.target_go_live_days - inp.contract_start_days

        status = _onboarding_status(overall)
        action = _onboarding_action(inp, status, delta)

        blockers_list, achievements_list, actions_list = _build_signals(
            inp, completion, delta, days_remaining
        )

        result = OnboardingResult(
            account_id=inp.account_id,
            account_name=inp.account_name,
            arr_eur=inp.arr_eur,
            onboarding_status=status,
            onboarding_action=action,
            overall_score=overall,
            milestone_score=milestone,
            engagement_score=engagement,
            health_score=health,
            completion_pct=completion,
            days_remaining=days_remaining,
            schedule_delta_pct=delta,
            blockers=blockers_list,
            achievements=achievements_list,
            recommended_actions=actions_list,
            go_live_done=inp.go_live_done,
        )
        self._results[inp.account_id] = result
        return result

    def assess_batch(self, inputs: list[OnboardingInput]) -> list[OnboardingResult]:
        return sorted(
            [self.assess(inp) for inp in inputs],
            key=lambda r: r.overall_score,
        )

    def get(self, account_id: str) -> Optional[OnboardingResult]:
        return self._results.get(account_id)

    def all_accounts(self) -> list[OnboardingResult]:
        return sorted(self._results.values(), key=lambda r: r.overall_score)

    def by_status(self, status: OnboardingStatus) -> list[OnboardingResult]:
        return [r for r in self.all_accounts() if r.onboarding_status == status]

    def critical(self) -> list[OnboardingResult]:
        return self.by_status(OnboardingStatus.CRITICAL)

    def at_risk(self) -> list[OnboardingResult]:
        return [r for r in self.all_accounts() if r.onboarding_status in (
            OnboardingStatus.CRITICAL, OnboardingStatus.AT_RISK
        )]

    def on_track(self) -> list[OnboardingResult]:
        return self.by_status(OnboardingStatus.ON_TRACK)

    def needs_rescue(self) -> list[OnboardingResult]:
        return [r for r in self.all_accounts() if r.onboarding_action == OnboardingAction.RESCUE]

    def completed(self) -> list[OnboardingResult]:
        return [r for r in self.all_accounts() if r.go_live_done]

    def overdue(self) -> list[OnboardingResult]:
        return [r for r in self.all_accounts() if r.days_remaining < 0 and not r.go_live_done]

    def total_arr_at_risk_eur(self) -> float:
        return round(sum(r.arr_eur for r in self.at_risk()), 2)

    def avg_completion_pct(self) -> float:
        accounts = self.all_accounts()
        if not accounts:
            return 0.0
        return round(sum(r.completion_pct for r in accounts) / len(accounts), 1)

    def summary(self) -> dict:
        all_r = self.all_accounts()
        if not all_r:
            return {
                "total": 0,
                "status_counts": {},
                "action_counts": {},
                "avg_completion_pct": 0.0,
                "avg_overall_score": 0.0,
                "critical_count": 0,
                "overdue_count": 0,
                "completed_count": 0,
                "total_arr_at_risk_eur": 0.0,
            }
        status_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        total_score = 0.0
        for r in all_r:
            status_counts[r.onboarding_status.value] = status_counts.get(r.onboarding_status.value, 0) + 1
            action_counts[r.onboarding_action.value] = action_counts.get(r.onboarding_action.value, 0) + 1
            total_score += r.overall_score
        return {
            "total": len(all_r),
            "status_counts": status_counts,
            "action_counts": action_counts,
            "avg_completion_pct": self.avg_completion_pct(),
            "avg_overall_score": round(total_score / len(all_r), 1),
            "critical_count": len(self.critical()),
            "overdue_count": len(self.overdue()),
            "completed_count": len(self.completed()),
            "total_arr_at_risk_eur": self.total_arr_at_risk_eur(),
        }

    def reset(self) -> None:
        self._results.clear()
