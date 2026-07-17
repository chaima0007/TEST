from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List


class AttritionRisk(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class AttritionSignal(str, Enum):
    NO_SIGNAL = "no_signal"
    EARLY_WARNING = "early_warning"
    ACTIVE_SEARCH = "active_search"
    LIKELY_DEPARTING = "likely_departing"


class CompensationHealth(str, Enum):
    COMPETITIVE = "competitive"
    ADEQUATE = "adequate"
    AT_RISK = "at_risk"
    UNDERPAID = "underpaid"


class RetentionAction(str, Enum):
    MAINTAIN = "maintain"
    RECOGNITION_AND_DEVELOPMENT = "recognition_and_development"
    COMPENSATION_REVIEW = "compensation_review"
    URGENT_RETENTION_MEETING = "urgent_retention_meeting"


@dataclass
class RepAttritionInput:
    rep_id: str
    rep_name: str
    region: str
    tenure_months: int
    quota_attainment_pct: float
    quota_attainment_pct_prev_year: float
    compensation_vs_market_pct: float
    uncapped_commission: int
    manager_satisfaction_score: float
    peer_relationships_score: float
    activity_trend_30d: float
    deal_win_rate_last_90d: float
    deal_win_rate_prev_quarter: float
    days_since_last_promotion: int
    linkedin_activity_score: float
    skipped_training_sessions_count: int
    pipeline_outside_territory_pct: float
    manager_1on1_completion_rate: float
    team_attrition_rate_90d: float
    pto_days_unused: int
    sales_target_increase_pct: float
    active_pipeline_usd: float


@dataclass
class RepAttritionResult:
    rep_id: str
    rep_name: str
    attrition_risk: AttritionRisk
    attrition_signal: AttritionSignal
    compensation_health: CompensationHealth
    retention_action: RetentionAction
    disengagement_score: float
    compensation_risk_score: float
    performance_satisfaction_score: float
    social_risk_score: float
    attrition_composite: float
    is_flight_risk: bool
    needs_urgent_retention: bool
    estimated_pipeline_at_risk_usd: float
    primary_attrition_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id": self.rep_id,
            "rep_name": self.rep_name,
            "attrition_risk": self.attrition_risk.value,
            "attrition_signal": self.attrition_signal.value,
            "compensation_health": self.compensation_health.value,
            "retention_action": self.retention_action.value,
            "disengagement_score": self.disengagement_score,
            "compensation_risk_score": self.compensation_risk_score,
            "performance_satisfaction_score": self.performance_satisfaction_score,
            "social_risk_score": self.social_risk_score,
            "attrition_composite": self.attrition_composite,
            "is_flight_risk": self.is_flight_risk,
            "needs_urgent_retention": self.needs_urgent_retention,
            "estimated_pipeline_at_risk_usd": self.estimated_pipeline_at_risk_usd,
            "primary_attrition_signal": self.primary_attrition_signal,
        }


def _disengagement_score(inp: RepAttritionInput) -> float:
    score = 0.0
    # Activity decline (0-30)
    if inp.activity_trend_30d <= -30:
        score += 30.0
    elif inp.activity_trend_30d <= -15:
        score += 20.0
    elif inp.activity_trend_30d < 0:
        score += 10.0
    # Training avoidance (0-20)
    if inp.skipped_training_sessions_count >= 3:
        score += 20.0
    elif inp.skipped_training_sessions_count >= 1:
        score += 10.0
    # Manager 1:1 avoidance (0-15)
    if inp.manager_1on1_completion_rate < 50:
        score += 15.0
    elif inp.manager_1on1_completion_rate < 75:
        score += 8.0
    # LinkedIn activity (passive job search signal) (0-20)
    if inp.linkedin_activity_score >= 70:
        score += 20.0
    elif inp.linkedin_activity_score >= 40:
        score += 12.0
    elif inp.linkedin_activity_score >= 20:
        score += 5.0
    # Win rate decline (0-15)
    rate_delta = inp.deal_win_rate_prev_quarter - inp.deal_win_rate_last_90d
    if rate_delta >= 15:
        score += 15.0
    elif rate_delta >= 8:
        score += 8.0
    return max(0.0, min(100.0, round(score, 1)))


def _compensation_risk_score(inp: RepAttritionInput) -> float:
    score = 0.0
    # Market compensation gap (0-40)
    if inp.compensation_vs_market_pct < 70:
        score += 40.0
    elif inp.compensation_vs_market_pct < 80:
        score += 30.0
    elif inp.compensation_vs_market_pct < 90:
        score += 20.0
    elif inp.compensation_vs_market_pct < 100:
        score += 10.0
    # Capped commission risk (0-15)
    if not inp.uncapped_commission:
        score += 15.0
    # Target increase pressure (0-20)
    if inp.sales_target_increase_pct >= 30:
        score += 20.0
    elif inp.sales_target_increase_pct >= 15:
        score += 12.0
    elif inp.sales_target_increase_pct >= 5:
        score += 5.0
    # Promotion stagnation (0-15)
    if inp.days_since_last_promotion >= 730:
        score += 15.0
    elif inp.days_since_last_promotion >= 365:
        score += 8.0
    # Attainment decline (0-10)
    att_delta = inp.quota_attainment_pct_prev_year - inp.quota_attainment_pct
    if att_delta >= 20:
        score += 10.0
    elif att_delta >= 10:
        score += 5.0
    return max(0.0, min(100.0, round(score, 1)))


def _performance_satisfaction_score(inp: RepAttritionInput) -> float:
    score = 0.0
    # Quota attainment (0-30)
    if inp.quota_attainment_pct >= 100:
        score += 30.0
    elif inp.quota_attainment_pct >= 80:
        score += 22.0
    elif inp.quota_attainment_pct >= 60:
        score += 14.0
    elif inp.quota_attainment_pct >= 40:
        score += 7.0
    # Deal win rate (0-20)
    if inp.deal_win_rate_last_90d >= 30:
        score += 20.0
    elif inp.deal_win_rate_last_90d >= 20:
        score += 14.0
    elif inp.deal_win_rate_last_90d >= 10:
        score += 8.0
    # Manager satisfaction (0-25)
    if inp.manager_satisfaction_score >= 8:
        score += 25.0
    elif inp.manager_satisfaction_score >= 6:
        score += 18.0
    elif inp.manager_satisfaction_score >= 4:
        score += 10.0
    # Peer relationships (0-15)
    if inp.peer_relationships_score >= 8:
        score += 15.0
    elif inp.peer_relationships_score >= 6:
        score += 10.0
    elif inp.peer_relationships_score >= 4:
        score += 5.0
    # Tenure stability bonus (0-10)
    if inp.tenure_months >= 24:
        score += 10.0
    elif inp.tenure_months >= 12:
        score += 5.0
    return max(0.0, min(100.0, round(score, 1)))


def _social_risk_score(inp: RepAttritionInput) -> float:
    score = 0.0
    # Team attrition contagion (0-40)
    if inp.team_attrition_rate_90d >= 30:
        score += 40.0
    elif inp.team_attrition_rate_90d >= 20:
        score += 28.0
    elif inp.team_attrition_rate_90d >= 10:
        score += 15.0
    # Pipeline outside territory (planning exit) (0-20)
    if inp.pipeline_outside_territory_pct >= 30:
        score += 20.0
    elif inp.pipeline_outside_territory_pct >= 15:
        score += 12.0
    # Unused PTO (cashing out) (0-15)
    if inp.pto_days_unused >= 20:
        score += 15.0
    elif inp.pto_days_unused >= 10:
        score += 8.0
    # LinkedIn job-search signal (0-25)
    if inp.linkedin_activity_score >= 70:
        score += 25.0
    elif inp.linkedin_activity_score >= 50:
        score += 15.0
    elif inp.linkedin_activity_score >= 30:
        score += 7.0
    return max(0.0, min(100.0, round(score, 1)))


def _composite(disengagement: float, comp_risk: float, perf_sat: float, social: float) -> float:
    raw = disengagement * 0.30 + comp_risk * 0.25 + (100.0 - perf_sat) * 0.25 + social * 0.20
    return round(raw, 1)


def _attrition_risk(composite: float) -> AttritionRisk:
    if composite >= 75:
        return AttritionRisk.CRITICAL
    if composite >= 55:
        return AttritionRisk.HIGH
    if composite >= 35:
        return AttritionRisk.MODERATE
    return AttritionRisk.LOW


def _attrition_signal(inp: RepAttritionInput, composite: float) -> AttritionSignal:
    if inp.linkedin_activity_score >= 70 and composite >= 65:
        return AttritionSignal.LIKELY_DEPARTING
    if inp.linkedin_activity_score >= 50 or composite >= 55:
        return AttritionSignal.ACTIVE_SEARCH
    if composite >= 35 or inp.activity_trend_30d <= -20:
        return AttritionSignal.EARLY_WARNING
    return AttritionSignal.NO_SIGNAL


def _compensation_health(inp: RepAttritionInput) -> CompensationHealth:
    if inp.compensation_vs_market_pct >= 100:
        return CompensationHealth.COMPETITIVE
    if inp.compensation_vs_market_pct >= 90:
        return CompensationHealth.ADEQUATE
    if inp.compensation_vs_market_pct >= 80:
        return CompensationHealth.AT_RISK
    return CompensationHealth.UNDERPAID


def _retention_action(risk: AttritionRisk, inp: RepAttritionInput) -> RetentionAction:
    if risk == AttritionRisk.CRITICAL:
        return RetentionAction.URGENT_RETENTION_MEETING
    if risk == AttritionRisk.HIGH:
        if inp.compensation_vs_market_pct < 85:
            return RetentionAction.COMPENSATION_REVIEW
        return RetentionAction.RECOGNITION_AND_DEVELOPMENT
    if risk == AttritionRisk.MODERATE:
        return RetentionAction.RECOGNITION_AND_DEVELOPMENT
    return RetentionAction.MAINTAIN


def _primary_attrition_signal(inp: RepAttritionInput, disengagement: float,
                               comp_risk: float, perf_sat: float, social: float) -> str:
    if inp.linkedin_activity_score >= 70:
        return "high LinkedIn activity — active job search detected"
    if inp.team_attrition_rate_90d >= 25:
        return "team attrition contagion — peer departures driving exit risk"
    if inp.compensation_vs_market_pct < 80:
        return f"underpaid vs market ({inp.compensation_vs_market_pct:.0f}%) — compensation is primary flight risk"
    if inp.activity_trend_30d <= -25:
        return f"activity collapsed {inp.activity_trend_30d:.0f}% — disengagement in progress"
    if inp.manager_satisfaction_score < 4:
        return "low manager satisfaction — relationship breakdown flagged"
    scores = {
        "disengagement": disengagement,
        "compensation risk": comp_risk,
        "performance dissatisfaction": 100.0 - perf_sat,
        "social risk": social,
    }
    weakest = max(scores, key=lambda k: scores[k])
    return f"primary driver: {weakest}"


class RepAttritionRiskEngine:
    def __init__(self) -> None:
        self._results: dict[str, RepAttritionResult] = {}

    def assess(self, inp: RepAttritionInput) -> RepAttritionResult:
        disengagement = _disengagement_score(inp)
        comp_risk = _compensation_risk_score(inp)
        perf_sat = _performance_satisfaction_score(inp)
        social = _social_risk_score(inp)
        composite = _composite(disengagement, comp_risk, perf_sat, social)

        risk = _attrition_risk(composite)
        signal = _attrition_signal(inp, composite)
        comp_health = _compensation_health(inp)
        action = _retention_action(risk, inp)
        is_flight_risk = composite >= 60 or risk == AttritionRisk.CRITICAL
        needs_urgent = composite >= 75 or (risk == AttritionRisk.CRITICAL and inp.tenure_months >= 12)
        exposure = round(inp.active_pipeline_usd * (composite / 100.0), 2)
        gap = _primary_attrition_signal(inp, disengagement, comp_risk, perf_sat, social)

        result = RepAttritionResult(
            rep_id=inp.rep_id,
            rep_name=inp.rep_name,
            attrition_risk=risk,
            attrition_signal=signal,
            compensation_health=comp_health,
            retention_action=action,
            disengagement_score=disengagement,
            compensation_risk_score=comp_risk,
            performance_satisfaction_score=perf_sat,
            social_risk_score=social,
            attrition_composite=composite,
            is_flight_risk=is_flight_risk,
            needs_urgent_retention=needs_urgent,
            estimated_pipeline_at_risk_usd=exposure,
            primary_attrition_signal=gap,
        )
        self._results[inp.rep_id] = result
        return result

    def assess_batch(self, inputs: List[RepAttritionInput]) -> List[RepAttritionResult]:
        results = [self.assess(inp) for inp in inputs]
        results.sort(key=lambda r: r.attrition_composite, reverse=True)
        return results

    def get(self, rep_id: str) -> RepAttritionResult | None:
        return self._results.get(rep_id)

    def all_reps(self) -> List[RepAttritionResult]:
        return sorted(self._results.values(), key=lambda r: r.attrition_composite, reverse=True)

    def flight_risks(self) -> List[RepAttritionResult]:
        return [r for r in self._results.values() if r.is_flight_risk]

    def urgent_retention(self) -> List[RepAttritionResult]:
        return [r for r in self._results.values() if r.needs_urgent_retention]

    def by_risk(self, risk: AttritionRisk) -> List[RepAttritionResult]:
        return [r for r in self._results.values() if r.attrition_risk == risk]

    def by_signal(self, signal: AttritionSignal) -> List[RepAttritionResult]:
        return [r for r in self._results.values() if r.attrition_signal == signal]

    def avg_attrition_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.attrition_composite for r in self._results.values()) / len(self._results), 1)

    def total_pipeline_at_risk(self) -> float:
        return round(sum(r.estimated_pipeline_at_risk_usd for r in self._results.values()), 2)

    def reset(self) -> None:
        self._results.clear()

    def summary(self) -> dict:
        results = list(self._results.values())
        n = len(results)
        risk_counts: dict[str, int] = {}
        signal_counts: dict[str, int] = {}
        comp_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        for r in results:
            risk_counts[r.attrition_risk.value] = risk_counts.get(r.attrition_risk.value, 0) + 1
            signal_counts[r.attrition_signal.value] = signal_counts.get(r.attrition_signal.value, 0) + 1
            comp_counts[r.compensation_health.value] = comp_counts.get(r.compensation_health.value, 0) + 1
            action_counts[r.retention_action.value] = action_counts.get(r.retention_action.value, 0) + 1
        return {
            "total": n,
            "risk_counts": risk_counts,
            "signal_counts": signal_counts,
            "compensation_counts": comp_counts,
            "action_counts": action_counts,
            "avg_attrition_composite": self.avg_attrition_composite(),
            "flight_risk_count": len(self.flight_risks()),
            "urgent_retention_count": len(self.urgent_retention()),
            "avg_disengagement_score": round(sum(r.disengagement_score for r in results) / n, 1) if n else 0.0,
            "avg_compensation_risk_score": round(sum(r.compensation_risk_score for r in results) / n, 1) if n else 0.0,
            "avg_performance_satisfaction_score": round(sum(r.performance_satisfaction_score for r in results) / n, 1) if n else 0.0,
            "avg_social_risk_score": round(sum(r.social_risk_score for r in results) / n, 1) if n else 0.0,
            "total_pipeline_at_risk_usd": self.total_pipeline_at_risk(),
        }
