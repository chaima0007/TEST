from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List


class RampStatus(str, Enum):
    AHEAD = "ahead"
    ON_TRACK = "on_track"
    AT_RISK = "at_risk"
    BEHIND = "behind"


class RampPhase(str, Enum):
    LEARNING = "learning"
    RAMPING = "ramping"
    APPROACHING_QUOTA = "approaching_quota"
    AT_QUOTA = "at_quota"


class RampRisk(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class RampAction(str, Enum):
    MAINTAIN = "maintain"
    ACCELERATE_COACHING = "accelerate_coaching"
    TERRITORY_ADJUSTMENT = "territory_adjustment"
    PIP = "performance_improvement_plan"


@dataclass
class RepRampInput:
    rep_id: str
    rep_name: str
    hire_date_days_ago: int
    quota_assigned_usd: float
    calls_last_7d: int
    emails_last_7d: int
    meetings_completed_last_30d: int
    demos_completed_last_30d: int
    deals_created_last_30d: int
    pipeline_value_usd: float
    first_deal_closed_days_after_hire: int
    revenue_attainment_pct: float
    manager_coaching_sessions_per_month: int
    peer_shadowing_sessions_completed: int
    product_certification_complete: int
    crm_adoption_score: float
    onboarding_assessment_score: float
    territory_quality_score: float
    previous_sales_experience_years: float
    industry_match_score: float
    support_ticket_count: int
    expected_ramp_days: int


@dataclass
class RepRampResult:
    rep_id: str
    rep_name: str
    ramp_status: RampStatus
    ramp_phase: RampPhase
    ramp_risk: RampRisk
    ramp_action: RampAction
    activity_score: float
    readiness_score: float
    pipeline_health_score: float
    attainment_score: float
    ramp_composite: float
    projected_full_ramp_days: int
    is_on_track: bool
    needs_intervention: bool
    key_risk_factor: str

    def to_dict(self) -> dict:
        return {
            "rep_id": self.rep_id,
            "rep_name": self.rep_name,
            "ramp_status": self.ramp_status.value,
            "ramp_phase": self.ramp_phase.value,
            "ramp_risk": self.ramp_risk.value,
            "ramp_action": self.ramp_action.value,
            "activity_score": self.activity_score,
            "readiness_score": self.readiness_score,
            "pipeline_health_score": self.pipeline_health_score,
            "attainment_score": self.attainment_score,
            "ramp_composite": self.ramp_composite,
            "projected_full_ramp_days": self.projected_full_ramp_days,
            "is_on_track": self.is_on_track,
            "needs_intervention": self.needs_intervention,
            "key_risk_factor": self.key_risk_factor,
        }


def _activity_score(inp: RepRampInput) -> float:
    score = 0.0
    # Call cadence (0-30)
    if inp.calls_last_7d >= 30:
        score += 30.0
    elif inp.calls_last_7d >= 20:
        score += 22.0
    elif inp.calls_last_7d >= 10:
        score += 14.0
    elif inp.calls_last_7d >= 5:
        score += 7.0
    # Email cadence (0-20)
    if inp.emails_last_7d >= 50:
        score += 20.0
    elif inp.emails_last_7d >= 30:
        score += 14.0
    elif inp.emails_last_7d >= 15:
        score += 8.0
    elif inp.emails_last_7d >= 5:
        score += 4.0
    # Meetings (0-25)
    if inp.meetings_completed_last_30d >= 10:
        score += 25.0
    elif inp.meetings_completed_last_30d >= 6:
        score += 18.0
    elif inp.meetings_completed_last_30d >= 3:
        score += 10.0
    elif inp.meetings_completed_last_30d >= 1:
        score += 5.0
    # Demos (0-15)
    if inp.demos_completed_last_30d >= 4:
        score += 15.0
    elif inp.demos_completed_last_30d >= 2:
        score += 10.0
    elif inp.demos_completed_last_30d >= 1:
        score += 5.0
    # Deals created (0-10)
    if inp.deals_created_last_30d >= 5:
        score += 10.0
    elif inp.deals_created_last_30d >= 3:
        score += 7.0
    elif inp.deals_created_last_30d >= 1:
        score += 3.0
    # Support ticket penalty
    if inp.support_ticket_count >= 5:
        score -= 8.0
    elif inp.support_ticket_count >= 3:
        score -= 4.0
    return max(0.0, min(100.0, round(score, 1)))


def _readiness_score(inp: RepRampInput) -> float:
    score = 0.0
    # Product certification (0-25)
    if inp.product_certification_complete:
        score += 25.0
    # CRM adoption (0-20)
    score += inp.crm_adoption_score * 0.20
    # Onboarding assessment (0-20)
    score += inp.onboarding_assessment_score * 0.20
    # Peer shadowing (0-15)
    if inp.peer_shadowing_sessions_completed >= 5:
        score += 15.0
    elif inp.peer_shadowing_sessions_completed >= 3:
        score += 10.0
    elif inp.peer_shadowing_sessions_completed >= 1:
        score += 5.0
    # Industry match (0-10)
    score += inp.industry_match_score * 0.10
    # Prior experience bonus (0-10)
    if inp.previous_sales_experience_years >= 5:
        score += 10.0
    elif inp.previous_sales_experience_years >= 3:
        score += 7.0
    elif inp.previous_sales_experience_years >= 1:
        score += 4.0
    return max(0.0, min(100.0, round(score, 1)))


def _pipeline_health_score(inp: RepRampInput) -> float:
    score = 0.0
    # Pipeline value relative to quota (0-40)
    if inp.quota_assigned_usd > 0:
        coverage = inp.pipeline_value_usd / inp.quota_assigned_usd
    else:
        coverage = 0.0
    if coverage >= 3.0:
        score += 40.0
    elif coverage >= 2.0:
        score += 30.0
    elif coverage >= 1.0:
        score += 20.0
    elif coverage >= 0.5:
        score += 10.0
    # Deals in pipeline (0-25)
    if inp.deals_created_last_30d >= 5:
        score += 25.0
    elif inp.deals_created_last_30d >= 3:
        score += 17.0
    elif inp.deals_created_last_30d >= 1:
        score += 8.0
    # Territory quality (0-20)
    score += inp.territory_quality_score * 0.20
    # First deal closed bonus (0-15)
    if inp.first_deal_closed_days_after_hire > 0:
        if inp.first_deal_closed_days_after_hire <= 60:
            score += 15.0
        elif inp.first_deal_closed_days_after_hire <= 90:
            score += 10.0
        else:
            score += 5.0
    return max(0.0, min(100.0, round(score, 1)))


def _attainment_score(inp: RepRampInput) -> float:
    # Score based on actual attainment vs expected pace
    expected_ramp = max(1, inp.expected_ramp_days)
    progress_pct = min(1.0, inp.hire_date_days_ago / expected_ramp)
    expected_attainment = progress_pct * 100.0

    if expected_attainment <= 0:
        return 50.0  # too early to judge

    ratio = inp.revenue_attainment_pct / expected_attainment
    if ratio >= 1.2:
        score = 100.0
    elif ratio >= 1.0:
        score = 80.0
    elif ratio >= 0.8:
        score = 60.0
    elif ratio >= 0.6:
        score = 40.0
    elif ratio >= 0.4:
        score = 20.0
    else:
        score = 5.0

    # Manager coaching boost
    if inp.manager_coaching_sessions_per_month >= 4:
        score = min(100.0, score + 10.0)
    elif inp.manager_coaching_sessions_per_month >= 2:
        score = min(100.0, score + 5.0)

    return max(0.0, min(100.0, round(score, 1)))


def _composite(activity: float, readiness: float, pipeline: float, attainment: float) -> float:
    raw = activity * 0.25 + readiness * 0.25 + pipeline * 0.30 + attainment * 0.20
    return round(raw, 1)


def _ramp_phase(inp: RepRampInput) -> RampPhase:
    if inp.revenue_attainment_pct >= 90:
        return RampPhase.AT_QUOTA
    if inp.revenue_attainment_pct >= 50:
        return RampPhase.APPROACHING_QUOTA
    if inp.hire_date_days_ago >= 30:
        return RampPhase.RAMPING
    return RampPhase.LEARNING


def _ramp_status(composite: float, inp: RepRampInput) -> RampStatus:
    expected_ramp = max(1, inp.expected_ramp_days)
    progress_pct = min(1.0, inp.hire_date_days_ago / expected_ramp)
    expected_attainment = progress_pct * 100.0
    if composite >= 70 and inp.revenue_attainment_pct >= expected_attainment * 1.1:
        return RampStatus.AHEAD
    if composite >= 55:
        return RampStatus.ON_TRACK
    if composite >= 40:
        return RampStatus.AT_RISK
    return RampStatus.BEHIND


def _ramp_risk(composite: float, inp: RepRampInput) -> RampRisk:
    if composite < 30 or (inp.hire_date_days_ago >= 60 and inp.revenue_attainment_pct < 10):
        return RampRisk.CRITICAL
    if composite < 45:
        return RampRisk.HIGH
    if composite < 60:
        return RampRisk.MODERATE
    return RampRisk.LOW


def _ramp_action(risk: RampRisk, composite: float) -> RampAction:
    if risk == RampRisk.CRITICAL:
        return RampAction.PIP
    if risk == RampRisk.HIGH:
        return RampAction.ACCELERATE_COACHING
    if risk == RampRisk.MODERATE:
        return RampAction.TERRITORY_ADJUSTMENT
    return RampAction.MAINTAIN


def _projected_full_ramp_days(inp: RepRampInput, composite: float) -> int:
    base = inp.expected_ramp_days
    if composite >= 75:
        return max(30, int(base * 0.85))
    if composite >= 55:
        return base
    if composite >= 40:
        return int(base * 1.25)
    return int(base * 1.6)


def _key_risk_factor(inp: RepRampInput, activity: float, readiness: float,
                     pipeline: float, attainment: float) -> str:
    scores = {
        "low activity volume": activity,
        "poor product readiness": readiness,
        "weak pipeline": pipeline,
        "low revenue attainment": attainment,
    }
    weakest = min(scores, key=lambda k: scores[k])
    if not inp.product_certification_complete and readiness < 50:
        return "product certification incomplete"
    if inp.support_ticket_count >= 5:
        return "blocked by tooling/admin issues"
    if inp.manager_coaching_sessions_per_month < 1:
        return "insufficient manager coaching"
    return weakest


class RepRampIntelligence:
    def __init__(self) -> None:
        self._results: dict[str, RepRampResult] = {}

    def assess(self, inp: RepRampInput) -> RepRampResult:
        activity = _activity_score(inp)
        readiness = _readiness_score(inp)
        pipeline = _pipeline_health_score(inp)
        attainment = _attainment_score(inp)
        composite = _composite(activity, readiness, pipeline, attainment)

        phase = _ramp_phase(inp)
        risk = _ramp_risk(composite, inp)
        status = _ramp_status(composite, inp)
        action = _ramp_action(risk, composite)
        projected = _projected_full_ramp_days(inp, composite)
        key_risk = _key_risk_factor(inp, activity, readiness, pipeline, attainment)

        expected_ramp = max(1, inp.expected_ramp_days)
        progress_pct = min(1.0, inp.hire_date_days_ago / expected_ramp)
        is_on_track = composite >= 55 and inp.revenue_attainment_pct >= progress_pct * 60.0
        needs_intervention = composite < 40 or risk == RampRisk.CRITICAL

        result = RepRampResult(
            rep_id=inp.rep_id,
            rep_name=inp.rep_name,
            ramp_status=status,
            ramp_phase=phase,
            ramp_risk=risk,
            ramp_action=action,
            activity_score=activity,
            readiness_score=readiness,
            pipeline_health_score=pipeline,
            attainment_score=attainment,
            ramp_composite=composite,
            projected_full_ramp_days=projected,
            is_on_track=is_on_track,
            needs_intervention=needs_intervention,
            key_risk_factor=key_risk,
        )
        self._results[inp.rep_id] = result
        return result

    def assess_batch(self, inputs: List[RepRampInput]) -> List[RepRampResult]:
        results = [self.assess(inp) for inp in inputs]
        results.sort(key=lambda r: r.ramp_composite, reverse=True)
        return results

    def get(self, rep_id: str) -> RepRampResult | None:
        return self._results.get(rep_id)

    def all_reps(self) -> List[RepRampResult]:
        return sorted(self._results.values(), key=lambda r: r.ramp_composite, reverse=True)

    def on_track_reps(self) -> List[RepRampResult]:
        return [r for r in self._results.values() if r.is_on_track]

    def intervention_queue(self) -> List[RepRampResult]:
        return [r for r in self._results.values() if r.needs_intervention]

    def by_status(self, status: RampStatus) -> List[RepRampResult]:
        return [r for r in self._results.values() if r.ramp_status == status]

    def by_phase(self, phase: RampPhase) -> List[RepRampResult]:
        return [r for r in self._results.values() if r.ramp_phase == phase]

    def avg_ramp_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.ramp_composite for r in self._results.values()) / len(self._results), 1)

    def reset(self) -> None:
        self._results.clear()

    def summary(self) -> dict:
        results = list(self._results.values())
        n = len(results)
        status_counts: dict[str, int] = {}
        phase_counts: dict[str, int] = {}
        risk_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        for r in results:
            status_counts[r.ramp_status.value] = status_counts.get(r.ramp_status.value, 0) + 1
            phase_counts[r.ramp_phase.value] = phase_counts.get(r.ramp_phase.value, 0) + 1
            risk_counts[r.ramp_risk.value] = risk_counts.get(r.ramp_risk.value, 0) + 1
            action_counts[r.ramp_action.value] = action_counts.get(r.ramp_action.value, 0) + 1
        return {
            "total": n,
            "ramp_status_counts": status_counts,
            "ramp_phase_counts": phase_counts,
            "ramp_risk_counts": risk_counts,
            "action_counts": action_counts,
            "avg_ramp_composite": self.avg_ramp_composite(),
            "on_track_count": len(self.on_track_reps()),
            "intervention_count": len(self.intervention_queue()),
            "avg_activity_score": round(sum(r.activity_score for r in results) / n, 1) if n else 0.0,
            "avg_readiness_score": round(sum(r.readiness_score for r in results) / n, 1) if n else 0.0,
            "avg_pipeline_health_score": round(sum(r.pipeline_health_score for r in results) / n, 1) if n else 0.0,
            "avg_attainment_score": round(sum(r.attainment_score for r in results) / n, 1) if n else 0.0,
            "avg_projected_full_ramp_days": round(sum(r.projected_full_ramp_days for r in results) / n) if n else 0,
        }
