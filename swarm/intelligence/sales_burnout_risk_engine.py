from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List


class BurnoutRisk(str, Enum):
    NONE = "none"
    EARLY_WARNING = "early_warning"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class BurnoutStage(str, Enum):
    ENGAGED = "engaged"
    COASTING = "coasting"
    DISENGAGING = "disengaging"
    BURNED_OUT = "burned_out"
    DEPLETED = "depleted"


class BurnoutSignal(str, Enum):
    NONE = "none"
    ACTIVITY_DECLINE = "activity_decline"
    ISOLATION = "isolation"
    PERFORMANCE_DECAY = "performance_decay"
    EXHAUSTION = "exhaustion"
    OVERWHELM = "overwhelm"


class BurnoutAction(str, Enum):
    MONITOR = "monitor"
    CHECK_IN = "check_in"
    COACHING_SESSION = "coaching_session"
    WORKLOAD_REDUCTION = "workload_reduction"
    URGENT_INTERVENTION = "urgent_intervention"


@dataclass
class SalesBurnoutInput:
    rep_id: str
    rep_name: str
    region: str
    activity_decline_pct: float
    avg_daily_calls_last_30d: float
    avg_daily_calls_prior_30d: float
    email_response_time_hrs: float
    meeting_acceptance_rate_pct: float
    pipeline_creation_last_30d_usd: float
    pipeline_creation_prior_30d_usd: float
    consecutive_no_close_weeks: int
    deal_win_rate_last_90d: float
    deal_win_rate_prior_quarter: float
    pto_days_taken_ytd: float
    pto_days_available_ytd: float
    weekend_work_hours_avg: float
    overtime_hours_per_week: float
    sick_days_last_90d: int
    manager_checkin_frequency: float
    peer_interaction_score: float
    quota_pressure_score: float
    customer_escalations_last_30d: int


@dataclass
class SalesBurnoutResult:
    rep_id: str
    rep_name: str
    burnout_risk: BurnoutRisk
    burnout_stage: BurnoutStage
    primary_burnout_signal: BurnoutSignal
    burnout_action: BurnoutAction
    activity_health_score: float
    wellbeing_score: float
    performance_sustainability_score: float
    social_engagement_score: float
    burnout_composite: float
    is_at_burnout_risk: bool
    needs_immediate_support: bool
    estimated_productivity_impact_pct: float
    burnout_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id": self.rep_id,
            "rep_name": self.rep_name,
            "burnout_risk": self.burnout_risk.value,
            "burnout_stage": self.burnout_stage.value,
            "primary_burnout_signal": self.primary_burnout_signal.value,
            "burnout_action": self.burnout_action.value,
            "activity_health_score": self.activity_health_score,
            "wellbeing_score": self.wellbeing_score,
            "performance_sustainability_score": self.performance_sustainability_score,
            "social_engagement_score": self.social_engagement_score,
            "burnout_composite": self.burnout_composite,
            "is_at_burnout_risk": self.is_at_burnout_risk,
            "needs_immediate_support": self.needs_immediate_support,
            "estimated_productivity_impact_pct": self.estimated_productivity_impact_pct,
            "burnout_signal": self.burnout_signal,
        }


def _activity_health_score(inp: SalesBurnoutInput) -> float:
    # HIGHER = healthier (less burnout risk)
    score = 0.0
    # Activity trend vs prior period (0-35)
    if inp.activity_decline_pct <= 5:
        score += 35.0
    elif inp.activity_decline_pct <= 15:
        score += 24.0
    elif inp.activity_decline_pct <= 30:
        score += 12.0
    elif inp.activity_decline_pct <= 50:
        score += 4.0
    # Pipeline creation trend (0-35)
    if inp.pipeline_creation_prior_30d_usd > 0:
        pipe_ratio = inp.pipeline_creation_last_30d_usd / inp.pipeline_creation_prior_30d_usd
    else:
        pipe_ratio = 1.0
    if pipe_ratio >= 0.90:
        score += 35.0
    elif pipe_ratio >= 0.75:
        score += 24.0
    elif pipe_ratio >= 0.55:
        score += 12.0
    elif pipe_ratio >= 0.35:
        score += 4.0
    # Meeting acceptance rate (0-30)
    if inp.meeting_acceptance_rate_pct >= 85:
        score += 30.0
    elif inp.meeting_acceptance_rate_pct >= 70:
        score += 20.0
    elif inp.meeting_acceptance_rate_pct >= 55:
        score += 10.0
    elif inp.meeting_acceptance_rate_pct >= 40:
        score += 3.0
    return max(0.0, min(100.0, round(score, 1)))


def _wellbeing_score(inp: SalesBurnoutInput) -> float:
    # HIGHER = healthier
    score = 0.0
    # Weekend work hours: minimal weekend work is healthy (0-30)
    if inp.weekend_work_hours_avg <= 2:
        score += 30.0
    elif inp.weekend_work_hours_avg <= 5:
        score += 20.0
    elif inp.weekend_work_hours_avg <= 10:
        score += 10.0
    # Overtime hours per week (0-25)
    if inp.overtime_hours_per_week <= 5:
        score += 25.0
    elif inp.overtime_hours_per_week <= 10:
        score += 15.0
    elif inp.overtime_hours_per_week <= 20:
        score += 6.0
    # PTO utilization (0-25): using PTO is healthy
    if inp.pto_days_available_ytd > 0:
        pto_ratio = inp.pto_days_taken_ytd / inp.pto_days_available_ytd
    else:
        pto_ratio = 0.0
    if pto_ratio >= 0.50:
        score += 25.0
    elif pto_ratio >= 0.30:
        score += 18.0
    elif pto_ratio >= 0.15:
        score += 9.0
    # Sick days in 90d: many sick days = exhaustion signal (0-20)
    if inp.sick_days_last_90d <= 1:
        score += 20.0
    elif inp.sick_days_last_90d <= 3:
        score += 12.0
    elif inp.sick_days_last_90d <= 5:
        score += 4.0
    return max(0.0, min(100.0, round(score, 1)))


def _performance_sustainability_score(inp: SalesBurnoutInput) -> float:
    # HIGHER = more sustainable performance
    score = 0.0
    # Win rate stability (0-35)
    win_rate_delta = inp.deal_win_rate_last_90d - inp.deal_win_rate_prior_quarter
    if win_rate_delta >= -5:
        score += 35.0
    elif win_rate_delta >= -10:
        score += 24.0
    elif win_rate_delta >= -20:
        score += 12.0
    # Consecutive no-close weeks (0-30)
    if inp.consecutive_no_close_weeks <= 2:
        score += 30.0
    elif inp.consecutive_no_close_weeks <= 4:
        score += 20.0
    elif inp.consecutive_no_close_weeks <= 7:
        score += 8.0
    # Customer escalations (0-20)
    if inp.customer_escalations_last_30d == 0:
        score += 20.0
    elif inp.customer_escalations_last_30d == 1:
        score += 13.0
    elif inp.customer_escalations_last_30d <= 2:
        score += 6.0
    # Quota pressure vs performance buffer (0-15)
    if inp.quota_pressure_score <= 40:
        score += 15.0
    elif inp.quota_pressure_score <= 60:
        score += 10.0
    elif inp.quota_pressure_score <= 75:
        score += 4.0
    return max(0.0, min(100.0, round(score, 1)))


def _social_engagement_score(inp: SalesBurnoutInput) -> float:
    # HIGHER = more socially engaged (healthier)
    score = 0.0
    # Manager check-in frequency (0-35)
    if inp.manager_checkin_frequency >= 4:
        score += 35.0
    elif inp.manager_checkin_frequency >= 2:
        score += 24.0
    elif inp.manager_checkin_frequency >= 1:
        score += 12.0
    # Peer interaction (0-35)
    score += inp.peer_interaction_score * 0.35
    # Email responsiveness (0-30): very fast OR very slow = indicator
    if inp.email_response_time_hrs <= 4:
        score += 30.0
    elif inp.email_response_time_hrs <= 12:
        score += 20.0
    elif inp.email_response_time_hrs <= 24:
        score += 10.0
    return max(0.0, min(100.0, round(score, 1)))


def _composite(activity: float, wellbeing: float, performance: float, social: float) -> float:
    # Invert: (100 - score) so higher composite = more at risk
    raw = (100 - activity) * 0.30 + (100 - wellbeing) * 0.25 + (100 - performance) * 0.25 + (100 - social) * 0.20
    return round(raw, 1)


def _burnout_risk(composite: float) -> BurnoutRisk:
    if composite < 20:
        return BurnoutRisk.NONE
    if composite < 35:
        return BurnoutRisk.EARLY_WARNING
    if composite < 50:
        return BurnoutRisk.MODERATE
    if composite < 70:
        return BurnoutRisk.HIGH
    return BurnoutRisk.CRITICAL


def _burnout_stage(composite: float) -> BurnoutStage:
    if composite < 20:
        return BurnoutStage.ENGAGED
    if composite < 35:
        return BurnoutStage.COASTING
    if composite < 50:
        return BurnoutStage.DISENGAGING
    if composite < 70:
        return BurnoutStage.BURNED_OUT
    return BurnoutStage.DEPLETED


def _primary_signal(inp: SalesBurnoutInput, activity: float, wellbeing: float,
                    performance: float, social: float) -> BurnoutSignal:
    scores = {
        BurnoutSignal.ACTIVITY_DECLINE: 100 - activity,
        BurnoutSignal.EXHAUSTION: 100 - wellbeing,
        BurnoutSignal.PERFORMANCE_DECAY: 100 - performance,
        BurnoutSignal.ISOLATION: 100 - social,
    }
    strongest = max(scores, key=lambda k: scores[k])
    if scores[strongest] < 20:
        return BurnoutSignal.NONE
    if inp.overtime_hours_per_week >= 20 or inp.weekend_work_hours_avg >= 10:
        return BurnoutSignal.OVERWHELM
    return strongest


def _burnout_action(risk: BurnoutRisk) -> BurnoutAction:
    if risk == BurnoutRisk.CRITICAL:
        return BurnoutAction.URGENT_INTERVENTION
    if risk == BurnoutRisk.HIGH:
        return BurnoutAction.WORKLOAD_REDUCTION
    if risk == BurnoutRisk.MODERATE:
        return BurnoutAction.COACHING_SESSION
    if risk == BurnoutRisk.EARLY_WARNING:
        return BurnoutAction.CHECK_IN
    return BurnoutAction.MONITOR


def _productivity_impact_pct(composite: float) -> float:
    if composite < 20:
        return 0.0
    if composite < 35:
        return round(composite * 0.3, 1)
    if composite < 50:
        return round(composite * 0.5, 1)
    return round(composite * 0.7, 1)


def _burnout_signal_text(inp: SalesBurnoutInput, signal: BurnoutSignal, composite: float) -> str:
    if signal == BurnoutSignal.OVERWHELM:
        return f"chronic overwork — {inp.overtime_hours_per_week:.0f}h overtime/wk + {inp.weekend_work_hours_avg:.0f}h weekends"
    if signal == BurnoutSignal.ACTIVITY_DECLINE:
        return f"activity down {inp.activity_decline_pct:.0f}% — {inp.consecutive_no_close_weeks} weeks without a close"
    if signal == BurnoutSignal.EXHAUSTION:
        return f"{inp.sick_days_last_90d} sick days in 90d, only {inp.pto_days_taken_ytd:.0f} PTO days used"
    if signal == BurnoutSignal.PERFORMANCE_DECAY:
        delta = inp.deal_win_rate_last_90d - inp.deal_win_rate_prior_quarter
        return f"win rate declined {abs(delta):.0f}pts — customer escalations: {inp.customer_escalations_last_30d}"
    if signal == BurnoutSignal.ISOLATION:
        return f"peer score {inp.peer_interaction_score:.0f}/100, manager check-ins {inp.manager_checkin_frequency:.1f}x/mo"
    if composite < 20:
        return f"rep healthy — no burnout signals detected"
    return f"early burnout indicators present — composite risk score {composite:.0f}"


class SalesBurnoutRiskEngine:
    def __init__(self) -> None:
        self._results: dict[str, SalesBurnoutResult] = {}

    def assess(self, inp: SalesBurnoutInput) -> SalesBurnoutResult:
        activity = _activity_health_score(inp)
        wellbeing = _wellbeing_score(inp)
        performance = _performance_sustainability_score(inp)
        social = _social_engagement_score(inp)
        composite = _composite(activity, wellbeing, performance, social)

        risk = _burnout_risk(composite)
        stage = _burnout_stage(composite)
        signal = _primary_signal(inp, activity, wellbeing, performance, social)
        action = _burnout_action(risk)
        is_at_risk = composite >= 35
        needs_support = composite >= 50 or (inp.sick_days_last_90d >= 5 and inp.overtime_hours_per_week >= 15)
        productivity_impact = _productivity_impact_pct(composite)
        signal_text = _burnout_signal_text(inp, signal, composite)

        result = SalesBurnoutResult(
            rep_id=inp.rep_id,
            rep_name=inp.rep_name,
            burnout_risk=risk,
            burnout_stage=stage,
            primary_burnout_signal=signal,
            burnout_action=action,
            activity_health_score=activity,
            wellbeing_score=wellbeing,
            performance_sustainability_score=performance,
            social_engagement_score=social,
            burnout_composite=composite,
            is_at_burnout_risk=is_at_risk,
            needs_immediate_support=needs_support,
            estimated_productivity_impact_pct=productivity_impact,
            burnout_signal=signal_text,
        )
        self._results[inp.rep_id] = result
        return result

    def assess_batch(self, inputs: List[SalesBurnoutInput]) -> List[SalesBurnoutResult]:
        results = [self.assess(inp) for inp in inputs]
        results.sort(key=lambda r: r.burnout_composite, reverse=True)
        return results

    def get(self, rep_id: str) -> SalesBurnoutResult | None:
        return self._results.get(rep_id)

    def all_reps(self) -> List[SalesBurnoutResult]:
        return sorted(self._results.values(), key=lambda r: r.burnout_composite, reverse=True)

    def at_risk_reps(self) -> List[SalesBurnoutResult]:
        return [r for r in self._results.values() if r.is_at_burnout_risk]

    def by_risk(self, risk: BurnoutRisk) -> List[SalesBurnoutResult]:
        return [r for r in self._results.values() if r.burnout_risk == risk]

    def by_stage(self, stage: BurnoutStage) -> List[SalesBurnoutResult]:
        return [r for r in self._results.values() if r.burnout_stage == stage]

    def avg_burnout_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.burnout_composite for r in self._results.values()) / len(self._results), 1)

    def total_productivity_impact_pct(self) -> float:
        return round(sum(r.estimated_productivity_impact_pct for r in self._results.values()), 1)

    def reset(self) -> None:
        self._results.clear()

    def summary(self) -> dict:
        results = list(self._results.values())
        n = len(results)
        risk_counts: dict[str, int] = {}
        stage_counts: dict[str, int] = {}
        signal_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        for r in results:
            risk_counts[r.burnout_risk.value] = risk_counts.get(r.burnout_risk.value, 0) + 1
            stage_counts[r.burnout_stage.value] = stage_counts.get(r.burnout_stage.value, 0) + 1
            signal_counts[r.primary_burnout_signal.value] = signal_counts.get(r.primary_burnout_signal.value, 0) + 1
            action_counts[r.burnout_action.value] = action_counts.get(r.burnout_action.value, 0) + 1
        return {
            "total": n,
            "risk_counts": risk_counts,
            "stage_counts": stage_counts,
            "signal_counts": signal_counts,
            "action_counts": action_counts,
            "avg_burnout_composite": self.avg_burnout_composite(),
            "at_burnout_risk_count": len(self.at_risk_reps()),
            "immediate_support_count": sum(1 for r in results if r.needs_immediate_support),
            "avg_activity_health_score": round(sum(r.activity_health_score for r in results) / n, 1) if n else 0.0,
            "avg_wellbeing_score": round(sum(r.wellbeing_score for r in results) / n, 1) if n else 0.0,
            "avg_performance_sustainability_score": round(sum(r.performance_sustainability_score for r in results) / n, 1) if n else 0.0,
            "avg_social_engagement_score": round(sum(r.social_engagement_score for r in results) / n, 1) if n else 0.0,
            "total_productivity_impact_pct": self.total_productivity_impact_pct(),
        }
