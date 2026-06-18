from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List


class DecayStatus(str, Enum):
    FRESH = "fresh"
    AGING = "aging"
    STALE = "stale"
    DEAD = "dead"


class DecayRisk(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class StageVelocity(str, Enum):
    FAST = "fast"
    ON_TRACK = "on_track"
    SLOW = "slow"
    STALLED = "stalled"


class RecoveryAction(str, Enum):
    MAINTAIN = "maintain"
    RE_ENGAGE_CHAMPION = "re_engage_champion"
    EXECUTIVE_ESCALATION = "executive_escalation"
    KILL_OR_RECYCLE = "kill_or_recycle"


@dataclass
class PipelineAgingInput:
    deal_id: str
    rep_id: str
    deal_name: str
    deal_value_usd: float
    deal_stage: int
    days_in_current_stage: int
    days_since_last_activity: int
    days_since_last_buyer_response: int
    total_deal_age_days: int
    velocity_vs_benchmark_pct: float
    activity_count_last_14d: int
    activity_count_prev_14d: int
    emails_opened_last_30d: int
    meetings_completed_last_30d: int
    champion_last_engaged_days_ago: int
    exec_last_engaged_days_ago: int
    next_step_defined: int
    close_date_changes_count: int
    stage_regression_count: int
    deal_source: int
    historical_avg_days_at_stage: int
    expected_close_days_remaining: int


@dataclass
class PipelineAgingResult:
    deal_id: str
    rep_id: str
    decay_status: DecayStatus
    decay_risk: DecayRisk
    stage_velocity: StageVelocity
    recovery_action: RecoveryAction
    activity_decay_score: float
    engagement_decay_score: float
    velocity_decay_score: float
    stage_health_score: float
    decay_composite: float
    is_stale: bool
    needs_immediate_action: bool
    recovery_probability_pct: float
    primary_decay_signal: str

    def to_dict(self) -> dict:
        return {
            "deal_id": self.deal_id,
            "rep_id": self.rep_id,
            "decay_status": self.decay_status.value,
            "decay_risk": self.decay_risk.value,
            "stage_velocity": self.stage_velocity.value,
            "recovery_action": self.recovery_action.value,
            "activity_decay_score": self.activity_decay_score,
            "engagement_decay_score": self.engagement_decay_score,
            "velocity_decay_score": self.velocity_decay_score,
            "stage_health_score": self.stage_health_score,
            "decay_composite": self.decay_composite,
            "is_stale": self.is_stale,
            "needs_immediate_action": self.needs_immediate_action,
            "recovery_probability_pct": self.recovery_probability_pct,
            "primary_decay_signal": self.primary_decay_signal,
        }


def _activity_decay_score(inp: PipelineAgingInput) -> float:
    score = 0.0
    # Days since last activity (0-35)
    if inp.days_since_last_activity >= 30:
        score += 35.0
    elif inp.days_since_last_activity >= 14:
        score += 25.0
    elif inp.days_since_last_activity >= 7:
        score += 12.0
    elif inp.days_since_last_activity >= 3:
        score += 5.0
    # Activity trend decline (0-30)
    if inp.activity_count_prev_14d > 0:
        trend = (inp.activity_count_last_14d - inp.activity_count_prev_14d) / inp.activity_count_prev_14d
    else:
        trend = 0.0 if inp.activity_count_last_14d > 0 else -1.0
    if trend <= -0.75:
        score += 30.0
    elif trend <= -0.50:
        score += 20.0
    elif trend <= -0.25:
        score += 12.0
    elif trend < 0:
        score += 5.0
    # No next step (0-20)
    if not inp.next_step_defined:
        score += 20.0
    # Stage regression penalty (0-15)
    if inp.stage_regression_count >= 2:
        score += 15.0
    elif inp.stage_regression_count >= 1:
        score += 8.0
    return max(0.0, min(100.0, round(score, 1)))


def _engagement_decay_score(inp: PipelineAgingInput) -> float:
    score = 0.0
    # Days since buyer response (0-35)
    if inp.days_since_last_buyer_response >= 30:
        score += 35.0
    elif inp.days_since_last_buyer_response >= 14:
        score += 25.0
    elif inp.days_since_last_buyer_response >= 7:
        score += 12.0
    elif inp.days_since_last_buyer_response >= 3:
        score += 5.0
    # Email engagement (0-20)
    if inp.emails_opened_last_30d == 0:
        score += 20.0
    elif inp.emails_opened_last_30d <= 2:
        score += 10.0
    # Meeting cadence (0-20)
    if inp.meetings_completed_last_30d == 0:
        score += 20.0
    elif inp.meetings_completed_last_30d == 1:
        score += 8.0
    # Champion recency (0-15)
    if inp.champion_last_engaged_days_ago >= 21:
        score += 15.0
    elif inp.champion_last_engaged_days_ago >= 14:
        score += 8.0
    # Close date manipulation (0-10)
    if inp.close_date_changes_count >= 3:
        score += 10.0
    elif inp.close_date_changes_count >= 2:
        score += 5.0
    return max(0.0, min(100.0, round(score, 1)))


def _velocity_decay_score(inp: PipelineAgingInput) -> float:
    score = 0.0
    # Velocity vs benchmark (0-40)
    if inp.velocity_vs_benchmark_pct >= 200:
        score += 40.0
    elif inp.velocity_vs_benchmark_pct >= 150:
        score += 30.0
    elif inp.velocity_vs_benchmark_pct >= 120:
        score += 18.0
    elif inp.velocity_vs_benchmark_pct >= 100:
        score += 8.0
    # Days in current stage vs historical (0-30)
    if inp.historical_avg_days_at_stage > 0:
        overage = inp.days_in_current_stage / inp.historical_avg_days_at_stage
    else:
        overage = 1.0
    if overage >= 2.0:
        score += 30.0
    elif overage >= 1.5:
        score += 20.0
    elif overage >= 1.2:
        score += 10.0
    # Overdue close date (0-20)
    if inp.expected_close_days_remaining < 0:
        score += 20.0
    elif inp.expected_close_days_remaining <= 7 and inp.deal_stage < 4:
        score += 12.0
    # Exec engagement gap (0-10)
    if inp.exec_last_engaged_days_ago >= 30 and inp.deal_stage >= 3:
        score += 10.0
    elif inp.exec_last_engaged_days_ago >= 14 and inp.deal_stage >= 4:
        score += 5.0
    return max(0.0, min(100.0, round(score, 1)))


def _stage_health_score(inp: PipelineAgingInput) -> float:
    score = 0.0
    # Recent meetings (0-30)
    if inp.meetings_completed_last_30d >= 3:
        score += 30.0
    elif inp.meetings_completed_last_30d >= 2:
        score += 20.0
    elif inp.meetings_completed_last_30d >= 1:
        score += 10.0
    # Next step defined (0-25)
    if inp.next_step_defined:
        score += 25.0
    # Recent activity (0-20)
    if inp.activity_count_last_14d >= 5:
        score += 20.0
    elif inp.activity_count_last_14d >= 3:
        score += 14.0
    elif inp.activity_count_last_14d >= 1:
        score += 7.0
    # Champion engaged recently (0-15)
    if inp.champion_last_engaged_days_ago <= 7:
        score += 15.0
    elif inp.champion_last_engaged_days_ago <= 14:
        score += 10.0
    # Email opens (0-10)
    if inp.emails_opened_last_30d >= 3:
        score += 10.0
    elif inp.emails_opened_last_30d >= 1:
        score += 5.0
    return max(0.0, min(100.0, round(score, 1)))


def _composite(activity: float, engagement: float, velocity: float, stage_health: float) -> float:
    raw = activity * 0.30 + engagement * 0.25 + velocity * 0.25 + (100.0 - stage_health) * 0.20
    return round(raw, 1)


def _is_stale(inp: PipelineAgingInput) -> bool:
    return inp.days_since_last_activity >= 14 or inp.days_since_last_buyer_response >= 21


def _decay_status(composite: float, inp: PipelineAgingInput) -> DecayStatus:
    if composite >= 75 or (inp.days_since_last_activity >= 30 and inp.days_since_last_buyer_response >= 30):
        return DecayStatus.DEAD
    if composite >= 55:
        return DecayStatus.STALE
    if composite >= 30:
        return DecayStatus.AGING
    return DecayStatus.FRESH


def _decay_risk(composite: float) -> DecayRisk:
    if composite >= 70:
        return DecayRisk.CRITICAL
    if composite >= 50:
        return DecayRisk.HIGH
    if composite >= 30:
        return DecayRisk.MODERATE
    return DecayRisk.LOW


def _stage_velocity(inp: PipelineAgingInput) -> StageVelocity:
    if inp.velocity_vs_benchmark_pct >= 150:
        return StageVelocity.STALLED
    if inp.velocity_vs_benchmark_pct >= 110:
        return StageVelocity.SLOW
    if inp.velocity_vs_benchmark_pct <= 85:
        return StageVelocity.FAST
    return StageVelocity.ON_TRACK


def _recovery_action(risk: DecayRisk, inp: PipelineAgingInput) -> RecoveryAction:
    if risk == DecayRisk.CRITICAL:
        return RecoveryAction.KILL_OR_RECYCLE
    if risk == DecayRisk.HIGH:
        return RecoveryAction.EXECUTIVE_ESCALATION
    if risk == DecayRisk.MODERATE:
        return RecoveryAction.RE_ENGAGE_CHAMPION
    return RecoveryAction.MAINTAIN


def _primary_decay_signal(inp: PipelineAgingInput, activity: float,
                           engagement: float, velocity: float, stage_health: float) -> str:
    if inp.days_since_last_buyer_response >= 30:
        return f"buyer dark for {inp.days_since_last_buyer_response} days — deal may be lost"
    if inp.days_since_last_activity >= 21:
        return f"no rep activity for {inp.days_since_last_activity} days — deal abandoned"
    if inp.velocity_vs_benchmark_pct >= 200:
        return f"deal {inp.velocity_vs_benchmark_pct:.0f}% slower than benchmark — stage stalled"
    if inp.stage_regression_count >= 2:
        return "multiple stage regressions — deal health deteriorating"
    if inp.close_date_changes_count >= 3:
        return f"close date pushed {inp.close_date_changes_count} times — buyer commitment weak"
    if inp.champion_last_engaged_days_ago >= 21:
        return f"champion not engaged in {inp.champion_last_engaged_days_ago} days — internal advocate at risk"
    scores = {
        "activity decay": activity,
        "engagement decay": engagement,
        "velocity decay": velocity,
        "stage health gap": 100.0 - stage_health,
    }
    worst = max(scores, key=lambda k: scores[k])
    return f"primary decay driver: {worst}"


class PipelineAgingIntelligence:
    def __init__(self) -> None:
        self._results: dict[str, PipelineAgingResult] = {}
        self._deal_values: dict[str, float] = {}

    def assess(self, inp: PipelineAgingInput) -> PipelineAgingResult:
        activity = _activity_decay_score(inp)
        engagement = _engagement_decay_score(inp)
        velocity = _velocity_decay_score(inp)
        stage_health = _stage_health_score(inp)
        composite = _composite(activity, engagement, velocity, stage_health)

        is_stale = _is_stale(inp)
        status = _decay_status(composite, inp)
        risk = _decay_risk(composite)
        vel = _stage_velocity(inp)
        action = _recovery_action(risk, inp)
        needs_action = composite >= 70 or risk == DecayRisk.CRITICAL
        recovery_prob = round(max(0.0, min(100.0, 100.0 - composite)), 1)
        signal = _primary_decay_signal(inp, activity, engagement, velocity, stage_health)

        result = PipelineAgingResult(
            deal_id=inp.deal_id,
            rep_id=inp.rep_id,
            decay_status=status,
            decay_risk=risk,
            stage_velocity=vel,
            recovery_action=action,
            activity_decay_score=activity,
            engagement_decay_score=engagement,
            velocity_decay_score=velocity,
            stage_health_score=stage_health,
            decay_composite=composite,
            is_stale=is_stale,
            needs_immediate_action=needs_action,
            recovery_probability_pct=recovery_prob,
            primary_decay_signal=signal,
        )
        self._results[inp.deal_id] = result
        self._deal_values[inp.deal_id] = inp.deal_value_usd
        return result

    def assess_batch(self, inputs: List[PipelineAgingInput]) -> List[PipelineAgingResult]:
        results = [self.assess(inp) for inp in inputs]
        results.sort(key=lambda r: r.decay_composite, reverse=True)
        return results

    def get(self, deal_id: str) -> PipelineAgingResult | None:
        return self._results.get(deal_id)

    def all_deals(self) -> List[PipelineAgingResult]:
        return sorted(self._results.values(), key=lambda r: r.decay_composite, reverse=True)

    def stale_deals(self) -> List[PipelineAgingResult]:
        return [r for r in self._results.values() if r.is_stale]

    def immediate_action_queue(self) -> List[PipelineAgingResult]:
        return [r for r in self._results.values() if r.needs_immediate_action]

    def by_status(self, status: DecayStatus) -> List[PipelineAgingResult]:
        return [r for r in self._results.values() if r.decay_status == status]

    def by_risk(self, risk: DecayRisk) -> List[PipelineAgingResult]:
        return [r for r in self._results.values() if r.decay_risk == risk]

    def avg_decay_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.decay_composite for r in self._results.values()) / len(self._results), 1)

    def total_stale_pipeline_usd(self) -> float:
        return round(sum(
            self._deal_values.get(r.deal_id, 0.0)
            for r in self._results.values() if r.is_stale
        ), 2)

    def reset(self) -> None:
        self._results.clear()
        self._deal_values.clear()

    def summary(self) -> dict:
        results = list(self._results.values())
        n = len(results)
        status_counts: dict[str, int] = {}
        risk_counts: dict[str, int] = {}
        vel_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        for r in results:
            status_counts[r.decay_status.value] = status_counts.get(r.decay_status.value, 0) + 1
            risk_counts[r.decay_risk.value] = risk_counts.get(r.decay_risk.value, 0) + 1
            vel_counts[r.stage_velocity.value] = vel_counts.get(r.stage_velocity.value, 0) + 1
            action_counts[r.recovery_action.value] = action_counts.get(r.recovery_action.value, 0) + 1
        return {
            "total": n,
            "decay_status_counts": status_counts,
            "risk_counts": risk_counts,
            "velocity_counts": vel_counts,
            "action_counts": action_counts,
            "avg_decay_composite": self.avg_decay_composite(),
            "stale_deal_count": len(self.stale_deals()),
            "immediate_action_count": len(self.immediate_action_queue()),
            "avg_activity_decay_score": round(sum(r.activity_decay_score for r in results) / n, 1) if n else 0.0,
            "avg_engagement_decay_score": round(sum(r.engagement_decay_score for r in results) / n, 1) if n else 0.0,
            "avg_velocity_decay_score": round(sum(r.velocity_decay_score for r in results) / n, 1) if n else 0.0,
            "avg_stage_health_score": round(sum(r.stage_health_score for r in results) / n, 1) if n else 0.0,
            "total_stale_pipeline_usd": self.total_stale_pipeline_usd(),
        }
