from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class RetentionRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class RetentionPattern(str, Enum):
    none                    = "none"
    compensation_risk       = "compensation_risk"
    disengagement           = "disengagement"
    career_stagnation       = "career_stagnation"
    manager_instability     = "manager_instability"
    performance_frustration = "performance_frustration"


class RetentionSeverity(str, Enum):
    committed  = "committed"
    developing = "developing"
    wavering   = "wavering"
    flight_risk = "flight_risk"


class RetentionAction(str, Enum):
    no_action                    = "no_action"
    retention_check_in           = "retention_check_in"
    compensation_review          = "compensation_review"
    career_development_plan      = "career_development_plan"
    manager_intervention         = "manager_intervention"
    immediate_retention_package  = "immediate_retention_package"


@dataclass
class RepRetentionInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    tenure_months: int
    quota_attainment_pct: float
    quota_attainment_prior_pct: float
    compensation_vs_market_pct: float
    promotion_wait_months: int
    manager_1on1_completion_pct: float
    direct_manager_change_count: int
    internal_job_app_count: int
    activity_trend_pct: float
    avg_daily_activity_count: float
    late_crm_update_rate_pct: float
    pto_days_taken: int
    peer_comparison_rank_pct: float
    positive_feedback_received_count: int
    skill_development_hours: float
    deal_win_rate_pct: float
    avg_response_time_to_manager_hours: float
    team_meetings_attendance_pct: float
    voluntary_overtime_hours: float


@dataclass
class RepRetentionResult:
    rep_id: str
    region: str
    retention_risk: RetentionRisk
    retention_pattern: RetentionPattern
    retention_severity: RetentionSeverity
    recommended_action: RetentionAction
    compensation_satisfaction_score: float
    engagement_vitality_score: float
    career_progression_score: float
    performance_satisfaction_score: float
    retention_risk_composite: float
    is_flight_risk: bool
    requires_retention_action: bool
    estimated_replacement_cost_usd: float
    retention_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "retention_risk":                   self.retention_risk.value,
            "retention_pattern":                self.retention_pattern.value,
            "retention_severity":               self.retention_severity.value,
            "recommended_action":               self.recommended_action.value,
            "compensation_satisfaction_score":  self.compensation_satisfaction_score,
            "engagement_vitality_score":        self.engagement_vitality_score,
            "career_progression_score":         self.career_progression_score,
            "performance_satisfaction_score":   self.performance_satisfaction_score,
            "retention_risk_composite":         self.retention_risk_composite,
            "is_flight_risk":                   self.is_flight_risk,
            "requires_retention_action":        self.requires_retention_action,
            "estimated_replacement_cost_usd":   self.estimated_replacement_cost_usd,
            "retention_signal":                 self.retention_signal,
        }


class SalesRepRetentionRiskIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[RepRetentionResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more retention risk)
    # ------------------------------------------------------------------

    def _compensation_satisfaction_score(self, inp: RepRetentionInput) -> float:
        score = 0.0

        if inp.compensation_vs_market_pct < -0.15:
            score += 40.0
        elif inp.compensation_vs_market_pct < -0.05:
            score += 20.0
        elif inp.compensation_vs_market_pct < 0.05:
            score += 8.0

        if inp.promotion_wait_months >= 24:
            score += 35.0
        elif inp.promotion_wait_months >= 18:
            score += 18.0
        elif inp.promotion_wait_months >= 12:
            score += 8.0

        if inp.positive_feedback_received_count == 0:
            score += 15.0
        elif inp.positive_feedback_received_count < 2:
            score += 7.0

        return min(score, 100.0)

    def _engagement_vitality_score(self, inp: RepRetentionInput) -> float:
        score = 0.0

        if inp.activity_trend_pct <= -0.30:
            score += 40.0
        elif inp.activity_trend_pct <= -0.15:
            score += 20.0
        elif inp.activity_trend_pct <= -0.05:
            score += 8.0

        if inp.late_crm_update_rate_pct >= 0.40:
            score += 30.0
        elif inp.late_crm_update_rate_pct >= 0.25:
            score += 15.0
        elif inp.late_crm_update_rate_pct >= 0.10:
            score += 7.0

        if inp.team_meetings_attendance_pct < 0.60:
            score += 20.0
        elif inp.team_meetings_attendance_pct < 0.75:
            score += 10.0

        if inp.manager_1on1_completion_pct < 0.50:
            score += 10.0

        return min(score, 100.0)

    def _career_progression_score(self, inp: RepRetentionInput) -> float:
        score = 0.0

        if inp.skill_development_hours < 2.0:
            score += 35.0
        elif inp.skill_development_hours < 5.0:
            score += 18.0
        elif inp.skill_development_hours < 10.0:
            score += 7.0

        if inp.direct_manager_change_count >= 3:
            score += 30.0
        elif inp.direct_manager_change_count >= 2:
            score += 15.0
        elif inp.direct_manager_change_count >= 1:
            score += 8.0

        if inp.internal_job_app_count >= 2:
            score += 25.0
        elif inp.internal_job_app_count >= 1:
            score += 12.0

        return min(score, 100.0)

    def _performance_satisfaction_score(self, inp: RepRetentionInput) -> float:
        score = 0.0

        trend = inp.quota_attainment_pct - inp.quota_attainment_prior_pct
        if trend <= -0.20:
            score += 30.0
        elif trend <= -0.10:
            score += 15.0

        if inp.deal_win_rate_pct < 0.20:
            score += 30.0
        elif inp.deal_win_rate_pct < 0.35:
            score += 15.0

        if inp.avg_response_time_to_manager_hours >= 24.0:
            score += 25.0
        elif inp.avg_response_time_to_manager_hours >= 8.0:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: RepRetentionInput,
                          comp: float, engagement: float,
                          career: float, performance: float) -> RetentionPattern:
        if comp >= 35 and inp.compensation_vs_market_pct < -0.10:
            return RetentionPattern.compensation_risk

        if engagement >= 35 and inp.activity_trend_pct <= -0.15:
            return RetentionPattern.disengagement

        if career >= 35 and inp.promotion_wait_months >= 24:
            return RetentionPattern.career_stagnation

        if career >= 25 and inp.direct_manager_change_count >= 2:
            return RetentionPattern.manager_instability

        if performance >= 30 and inp.quota_attainment_pct < 0.75:
            return RetentionPattern.performance_frustration

        return RetentionPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> RetentionRisk:
        if composite >= 60:
            return RetentionRisk.critical
        if composite >= 40:
            return RetentionRisk.high
        if composite >= 20:
            return RetentionRisk.moderate
        return RetentionRisk.low

    def _severity(self, composite: float) -> RetentionSeverity:
        if composite >= 60:
            return RetentionSeverity.flight_risk
        if composite >= 40:
            return RetentionSeverity.wavering
        if composite >= 20:
            return RetentionSeverity.developing
        return RetentionSeverity.committed

    def _action(self, risk: RetentionRisk,
                 pattern: RetentionPattern) -> RetentionAction:
        if risk == RetentionRisk.critical:
            if pattern == RetentionPattern.compensation_risk:
                return RetentionAction.immediate_retention_package
            if pattern == RetentionPattern.manager_instability:
                return RetentionAction.manager_intervention
            return RetentionAction.immediate_retention_package
        if risk == RetentionRisk.high:
            if pattern == RetentionPattern.career_stagnation:
                return RetentionAction.career_development_plan
            if pattern == RetentionPattern.compensation_risk:
                return RetentionAction.compensation_review
            return RetentionAction.retention_check_in
        if risk == RetentionRisk.moderate:
            return RetentionAction.retention_check_in
        return RetentionAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _is_flight_risk(self, composite: float,
                         inp: RepRetentionInput) -> bool:
        return (
            composite >= 40
            or inp.internal_job_app_count >= 1
            or (inp.compensation_vs_market_pct < -0.15 and inp.promotion_wait_months >= 18)
        )

    def _requires_retention_action(self, composite: float,
                                    inp: RepRetentionInput) -> bool:
        return (
            composite >= 30
            or inp.activity_trend_pct <= -0.20
            or inp.late_crm_update_rate_pct >= 0.30
        )

    # ------------------------------------------------------------------
    # Replacement cost
    # ------------------------------------------------------------------

    def _estimated_replacement_cost(self, inp: RepRetentionInput,
                                     composite: float) -> float:
        tenure_multiplier = 1.0 + min(inp.tenure_months / 36.0, 1.0)
        return round(80000.0 * tenure_multiplier * (composite / 100.0), 2)

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: RepRetentionInput,
                 pattern: RetentionPattern, composite: float) -> str:
        if pattern == RetentionPattern.none and composite < 20:
            return "Retention indicators healthy — rep showing strong engagement and satisfaction"
        parts: list[str] = []
        if inp.compensation_vs_market_pct < -0.05:
            pct = abs(inp.compensation_vs_market_pct) * 100
            parts.append(f"{pct:.0f}% below market comp")
        if inp.activity_trend_pct <= -0.10:
            pct = abs(inp.activity_trend_pct) * 100
            parts.append(f"activity down {pct:.0f}%")
        if inp.tenure_months >= 12:
            parts.append(f"{inp.tenure_months}mo tenure at risk")
        label = pattern.value.replace("_", " ") if pattern != RetentionPattern.none else "Retention risk"
        summary = " — ".join(parts) if parts else "disengagement signals detected"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: RepRetentionInput) -> RepRetentionResult:
        comp        = round(self._compensation_satisfaction_score(inp), 1)
        engagement  = round(self._engagement_vitality_score(inp), 1)
        career      = round(self._career_progression_score(inp), 1)
        performance = round(self._performance_satisfaction_score(inp), 1)

        composite = round(
            comp * 0.30 + engagement * 0.30 + career * 0.25 + performance * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, comp, engagement, career, performance)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        flight   = self._is_flight_risk(composite, inp)
        retention_action = self._requires_retention_action(composite, inp)
        cost     = self._estimated_replacement_cost(inp, composite)
        signal   = self._signal(inp, pattern, composite)

        result = RepRetentionResult(
            rep_id=inp.rep_id,
            region=inp.region,
            retention_risk=risk,
            retention_pattern=pattern,
            retention_severity=severity,
            recommended_action=action,
            compensation_satisfaction_score=comp,
            engagement_vitality_score=engagement,
            career_progression_score=career,
            performance_satisfaction_score=performance,
            retention_risk_composite=composite,
            is_flight_risk=flight,
            requires_retention_action=retention_action,
            estimated_replacement_cost_usd=cost,
            retention_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[RepRetentionInput]) -> list[RepRetentionResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_retention_risk_composite": 0.0,
                "flight_risk_count": 0,
                "retention_action_count": 0,
                "avg_compensation_satisfaction_score": 0.0,
                "avg_engagement_vitality_score": 0.0,
                "avg_career_progression_score": 0.0,
                "avg_performance_satisfaction_score": 0.0,
                "total_estimated_replacement_cost_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_eng = total_car = total_per = total_cost = total_composite = 0.0

        for r in self._results:
            risk_counts[r.retention_risk.value]         = risk_counts.get(r.retention_risk.value, 0) + 1
            pattern_counts[r.retention_pattern.value]   = pattern_counts.get(r.retention_pattern.value, 0) + 1
            severity_counts[r.retention_severity.value] = severity_counts.get(r.retention_severity.value, 0) + 1
            action_counts[r.recommended_action.value]   = action_counts.get(r.recommended_action.value, 0) + 1
            total_composite += r.retention_risk_composite
            total_comp      += r.compensation_satisfaction_score
            total_eng       += r.engagement_vitality_score
            total_car       += r.career_progression_score
            total_per       += r.performance_satisfaction_score
            total_cost      += r.estimated_replacement_cost_usd

        n = len(self._results)

        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_retention_risk_composite":         round(total_composite / n, 1),
            "flight_risk_count":                    sum(1 for r in self._results if r.is_flight_risk),
            "retention_action_count":               sum(1 for r in self._results if r.requires_retention_action),
            "avg_compensation_satisfaction_score":  round(total_comp / n, 1),
            "avg_engagement_vitality_score":        round(total_eng / n, 1),
            "avg_career_progression_score":         round(total_car / n, 1),
            "avg_performance_satisfaction_score":   round(total_per / n, 1),
            "total_estimated_replacement_cost_usd": round(total_cost, 2),
        }
