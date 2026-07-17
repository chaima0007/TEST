"""Pipeline Velocity Calculator — measures deal momentum and flow rate through the sales pipeline."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional


class VelocityStatus(str, Enum):
    FAST = "fast"        # score >= 75
    ON_PACE = "on_pace"  # score >= 50
    SLOW = "slow"        # score >= 25
    STALLED = "stalled"  # score < 25


class VelocityAction(str, Enum):
    CLOSE_NOW = "close_now"    # closing stage, high win prob, ready to close
    RESCUE = "rescue"          # stalled/regressing, urgent intervention
    ACCELERATE = "accelerate"  # slow/inactive, needs push
    MONITOR = "monitor"        # healthy momentum, regular check-ins


# Expected days per stage (benchmark)
_STAGE_BENCHMARKS: dict[str, int] = {
    "prospecting": 7,
    "qualification": 14,
    "demo": 14,
    "proposal": 21,
    "negotiation": 14,
    "closing": 7,
}


@dataclass
class PipelineVelocityInput:
    deal_id: str
    deal_name: str
    account_name: str
    segment: str             # enterprise / mid_market / smb

    arr_eur: float
    stage: str               # prospecting/qualification/demo/proposal/negotiation/closing
    days_in_current_stage: int
    total_days_in_pipeline: int
    expected_total_days: int  # target sales cycle length

    win_probability_pct: float   # 0-100
    last_activity_days: int      # days since last touch
    has_next_step_scheduled: bool
    stage_regression_count: int  # times the deal went backward
    blocker_count: int

    champion_present: bool
    decision_maker_engaged: bool


@dataclass
class PipelineVelocityResult:
    deal_id: str
    deal_name: str
    account_name: str
    segment: str
    arr_eur: float
    stage: str

    velocity_status: VelocityStatus
    velocity_action: VelocityAction
    velocity_score: float        # 0-100 composite momentum score
    stage_pace_score: float      # 0-100 how fast through current stage
    activity_score: float        # 0-100 engagement momentum
    probability_score: float     # 0-100 win probability component

    velocity_eur_per_day: float  # weighted pipeline value flowing per day
    schedule_delta_pct: float    # vs expected cycle (+ = ahead)
    days_in_current_stage: int
    stage_benchmark_days: int
    stage_overdue: bool

    risk_flags: list[str]
    momentum_signals: list[str]
    recommended_actions: list[str]

    def to_dict(self) -> dict:
        d = asdict(self)
        d["velocity_status"] = self.velocity_status.value
        d["velocity_action"] = self.velocity_action.value
        return d


def _stage_pace_score(inp: PipelineVelocityInput) -> tuple[float, bool]:
    """Returns (stage_pace_score 0-100, stage_overdue bool)."""
    benchmark = _STAGE_BENCHMARKS.get(inp.stage, 14)
    overdue = inp.days_in_current_stage > benchmark
    ratio = inp.days_in_current_stage / max(1, benchmark)
    if ratio <= 0.5:
        score = 100.0
    elif ratio <= 1.0:
        score = 100.0 - (ratio - 0.5) * 60.0  # 100 → 70
    elif ratio <= 1.5:
        score = 70.0 - (ratio - 1.0) * 80.0   # 70 → 30
    elif ratio <= 2.0:
        score = 30.0 - (ratio - 1.5) * 60.0   # 30 → 0
    else:
        score = 0.0
    return round(max(0.0, min(100.0, score)), 2), overdue


def _activity_score(inp: PipelineVelocityInput) -> float:
    score = 0.0
    if inp.last_activity_days <= 1:
        score += 50
    elif inp.last_activity_days <= 3:
        score += 40
    elif inp.last_activity_days <= 7:
        score += 25
    elif inp.last_activity_days <= 14:
        score += 10
    if inp.has_next_step_scheduled:
        score += 25
    if inp.champion_present:
        score += 15
    if inp.decision_maker_engaged:
        score += 10
    return round(max(0.0, min(100.0, score)), 2)


def _probability_score(inp: PipelineVelocityInput) -> float:
    return round(max(0.0, min(100.0, inp.win_probability_pct)), 2)


def _velocity_score(pace: float, activity: float, probability: float, inp: PipelineVelocityInput) -> float:
    base = pace * 0.40 + activity * 0.30 + probability * 0.20
    penalty = min(20.0, inp.stage_regression_count * 8.0) + min(15.0, inp.blocker_count * 7.0)
    return round(max(0.0, min(100.0, base - penalty)), 2)


def _schedule_delta(inp: PipelineVelocityInput) -> float:
    if inp.expected_total_days <= 0:
        return 0.0
    elapsed_pct = min(100.0, inp.total_days_in_pipeline / inp.expected_total_days * 100.0)
    return round(inp.win_probability_pct - elapsed_pct, 1)


def _velocity_eur_per_day(inp: PipelineVelocityInput) -> float:
    weighted = inp.arr_eur * inp.win_probability_pct / 100.0
    return round(weighted / max(1, inp.total_days_in_pipeline), 2)


def _velocity_status(score: float) -> VelocityStatus:
    if score >= 75:
        return VelocityStatus.FAST
    if score >= 50:
        return VelocityStatus.ON_PACE
    if score >= 25:
        return VelocityStatus.SLOW
    return VelocityStatus.STALLED


def _velocity_action(inp: PipelineVelocityInput, status: VelocityStatus) -> VelocityAction:
    if inp.stage == "closing" and inp.win_probability_pct >= 70 and inp.last_activity_days <= 3:
        return VelocityAction.CLOSE_NOW
    if status == VelocityStatus.STALLED or inp.stage_regression_count >= 2 or inp.blocker_count >= 2:
        return VelocityAction.RESCUE
    if status == VelocityStatus.SLOW or inp.last_activity_days > 7 or not inp.has_next_step_scheduled:
        return VelocityAction.ACCELERATE
    return VelocityAction.MONITOR


def _build_signals(
    inp: PipelineVelocityInput,
    status: VelocityStatus,
    stage_overdue: bool,
    delta: float,
) -> tuple[list[str], list[str], list[str]]:
    flags: list[str] = []
    signals: list[str] = []
    actions: list[str] = []

    # Risk flags
    if stage_overdue:
        benchmark = _STAGE_BENCHMARKS.get(inp.stage, 14)
        flags.append(f"En stage '{inp.stage}' depuis {inp.days_in_current_stage}j (benchmark: {benchmark}j)")
    if inp.stage_regression_count >= 2:
        flags.append(f"Deal revenu en arrière {inp.stage_regression_count}x — instabilité du cycle")
    elif inp.stage_regression_count == 1:
        flags.append("1 régression de stage détectée")
    if inp.blocker_count > 0:
        flags.append(f"{inp.blocker_count} bloqueur(s) actif(s) dans le deal")
    if inp.last_activity_days > 14:
        flags.append(f"Aucune activité depuis {inp.last_activity_days}j — deal en danger")
    elif inp.last_activity_days > 7:
        flags.append(f"Faible activité — {inp.last_activity_days}j sans contact")
    if not inp.has_next_step_scheduled:
        flags.append("Pas de prochaine étape planifiée")
    if not inp.champion_present:
        flags.append("Pas de champion identifié côté client")
    if inp.win_probability_pct < 20:
        flags.append(f"Probabilité de gain faible ({inp.win_probability_pct:.0f}%)")
    if delta < -20:
        flags.append(f"En retard de {abs(delta):.0f}% sur le cycle prévu")

    # Momentum signals
    if inp.win_probability_pct >= 70:
        signals.append(f"Probabilité de gain élevée ({inp.win_probability_pct:.0f}%)")
    if inp.champion_present:
        signals.append("Champion actif côté client — bonne adhésion interne")
    if inp.decision_maker_engaged:
        signals.append("Décideur engagé — raccourcit le cycle de décision")
    if inp.has_next_step_scheduled:
        signals.append("Prochaine étape planifiée — momentum maintenu")
    if inp.last_activity_days <= 3:
        signals.append("Activité récente — deal vivant et engagé")
    if inp.stage_regression_count == 0 and inp.total_days_in_pipeline > 7:
        signals.append("Progression linéaire — aucune régression")
    if delta > 10:
        signals.append(f"En avance de {delta:.0f}% sur le cycle de vente prévu")
    if inp.stage == "closing":
        signals.append("Deal en phase de closing — proche de la signature")

    # Recommended actions
    if inp.blocker_count > 0:
        actions.append(f"Résoudre les {inp.blocker_count} bloqueur(s) avant d'avancer")
    if not inp.has_next_step_scheduled:
        actions.append("Planifier la prochaine étape immédiatement")
    if inp.last_activity_days > 7:
        actions.append(f"Reprendre contact — {inp.last_activity_days}j sans interaction")
    if inp.stage_regression_count >= 1:
        actions.append("Analyser les causes de régression et requalifier")
    if not inp.champion_present:
        actions.append("Identifier et activer un champion interne")
    if not inp.decision_maker_engaged and inp.stage in ("proposal", "negotiation", "closing"):
        actions.append("Engager le décideur — critique en phase avancée")
    if inp.stage == "closing" and inp.win_probability_pct >= 70:
        actions.append("Finaliser les termes contractuels et accélérer la signature")
    if status == VelocityStatus.STALLED:
        actions.append("Évaluer si le deal doit être mis en pause ou abandonné")
    if stage_overdue:
        benchmark = _STAGE_BENCHMARKS.get(inp.stage, 14)
        overdue_days = inp.days_in_current_stage - benchmark
        actions.append(f"Accélérer la sortie du stage '{inp.stage}' (dépassé de {overdue_days}j)")

    return flags, signals, actions


class PipelineVelocityCalculator:
    """Measures deal momentum and pipeline flow rate to identify stalled deals and close-ready opportunities."""

    def __init__(self) -> None:
        self._results: dict[str, PipelineVelocityResult] = {}

    def calculate(self, inp: PipelineVelocityInput) -> PipelineVelocityResult:
        pace, stage_overdue = _stage_pace_score(inp)
        activity = _activity_score(inp)
        probability = _probability_score(inp)
        score = _velocity_score(pace, activity, probability, inp)
        delta = _schedule_delta(inp)
        vel_eur = _velocity_eur_per_day(inp)

        status = _velocity_status(score)
        action = _velocity_action(inp, status)

        flags, signals, actions = _build_signals(inp, status, stage_overdue, delta)

        result = PipelineVelocityResult(
            deal_id=inp.deal_id,
            deal_name=inp.deal_name,
            account_name=inp.account_name,
            segment=inp.segment,
            arr_eur=inp.arr_eur,
            stage=inp.stage,
            velocity_status=status,
            velocity_action=action,
            velocity_score=score,
            stage_pace_score=pace,
            activity_score=activity,
            probability_score=probability,
            velocity_eur_per_day=vel_eur,
            schedule_delta_pct=delta,
            days_in_current_stage=inp.days_in_current_stage,
            stage_benchmark_days=_STAGE_BENCHMARKS.get(inp.stage, 14),
            stage_overdue=stage_overdue,
            risk_flags=flags,
            momentum_signals=signals,
            recommended_actions=actions,
        )
        self._results[inp.deal_id] = result
        return result

    def calculate_batch(self, inputs: list[PipelineVelocityInput]) -> list[PipelineVelocityResult]:
        return sorted(
            [self.calculate(inp) for inp in inputs],
            key=lambda r: r.velocity_score,
        )

    def get(self, deal_id: str) -> Optional[PipelineVelocityResult]:
        return self._results.get(deal_id)

    def all_deals(self) -> list[PipelineVelocityResult]:
        return sorted(self._results.values(), key=lambda r: r.velocity_score)

    def by_status(self, status: VelocityStatus) -> list[PipelineVelocityResult]:
        return [r for r in self.all_deals() if r.velocity_status == status]

    def stalled(self) -> list[PipelineVelocityResult]:
        return self.by_status(VelocityStatus.STALLED)

    def fast(self) -> list[PipelineVelocityResult]:
        return self.by_status(VelocityStatus.FAST)

    def needs_rescue(self) -> list[PipelineVelocityResult]:
        return [r for r in self.all_deals() if r.velocity_action == VelocityAction.RESCUE]

    def close_now(self) -> list[PipelineVelocityResult]:
        return [r for r in self.all_deals() if r.velocity_action == VelocityAction.CLOSE_NOW]

    def at_risk(self) -> list[PipelineVelocityResult]:
        return [r for r in self.all_deals() if r.velocity_status in (VelocityStatus.STALLED, VelocityStatus.SLOW)]

    def total_pipeline_eur(self) -> float:
        return round(sum(r.arr_eur for r in self._results.values()), 2)

    def total_weighted_pipeline_eur(self) -> float:
        return round(sum(r.arr_eur * r.probability_score / 100.0 for r in self._results.values()), 2)

    def total_velocity_eur_per_day(self) -> float:
        return round(sum(r.velocity_eur_per_day for r in self._results.values()), 2)

    def avg_velocity_score(self) -> float:
        deals = list(self._results.values())
        if not deals:
            return 0.0
        return round(sum(r.velocity_score for r in deals) / len(deals), 1)

    def by_segment(self, segment: str) -> list[PipelineVelocityResult]:
        return [r for r in self.all_deals() if r.segment == segment]

    def by_stage(self, stage: str) -> list[PipelineVelocityResult]:
        return [r for r in self.all_deals() if r.stage == stage]

    def top_n(self, n: int) -> list[PipelineVelocityResult]:
        return sorted(self._results.values(), key=lambda r: r.velocity_eur_per_day, reverse=True)[:n]

    def summary(self) -> dict:
        all_r = list(self._results.values())
        if not all_r:
            return {
                "total": 0,
                "status_counts": {},
                "action_counts": {},
                "avg_velocity_score": 0.0,
                "total_velocity_eur_per_day": 0.0,
                "total_pipeline_eur": 0.0,
                "total_weighted_pipeline_eur": 0.0,
                "stalled_count": 0,
                "rescue_count": 0,
                "close_now_count": 0,
            }
        status_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        for r in all_r:
            status_counts[r.velocity_status.value] = status_counts.get(r.velocity_status.value, 0) + 1
            action_counts[r.velocity_action.value] = action_counts.get(r.velocity_action.value, 0) + 1
        return {
            "total": len(all_r),
            "status_counts": status_counts,
            "action_counts": action_counts,
            "avg_velocity_score": self.avg_velocity_score(),
            "total_velocity_eur_per_day": self.total_velocity_eur_per_day(),
            "total_pipeline_eur": self.total_pipeline_eur(),
            "total_weighted_pipeline_eur": self.total_weighted_pipeline_eur(),
            "stalled_count": len(self.stalled()),
            "rescue_count": len(self.needs_rescue()),
            "close_now_count": len(self.close_now()),
        }

    def reset(self) -> None:
        self._results.clear()
