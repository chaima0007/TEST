from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class BurnoutRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class AttritionPattern(str, Enum):
    none                 = "none"
    workload_exhaustion  = "workload_exhaustion"
    quota_pressure       = "quota_pressure"
    disengagement        = "disengagement"
    compensation_dissatisfaction = "compensation_dissatisfaction"
    manager_conflict     = "manager_conflict"


class BurnoutSeverity(str, Enum):
    healthy     = "healthy"
    watch       = "watch"
    at_risk     = "at_risk"
    flight_risk = "flight_risk"


class BurnoutAction(str, Enum):
    no_action           = "no_action"
    wellness_checkin    = "wellness_checkin"
    workload_rebalance  = "workload_rebalance"
    retention_interview = "retention_interview"
    executive_retention = "executive_retention"


@dataclass
class BurnoutAttritionInput:
    rep_id: str
    region: str
    tenure_months: int
    quota_attainment_pct: float
    quota_attainment_prior_pct: float
    quota_pressure_score: float
    pto_days_taken_ytd: float
    pto_days_allocated_ytd: float
    avg_weekly_activity_count: float
    activity_count_prior_period: float
    after_hours_activity_pct: float
    crm_update_compliance_pct: float
    crm_compliance_prior_pct: float
    voluntary_meeting_attendance_pct: float
    manager_interaction_days_since: int
    peer_collaboration_score: float
    compensation_satisfaction_score: float
    consecutive_missed_quota_periods: int
    sick_days_last_90d: int
    escalations_raised_last_90d: int
    linkedin_activity_spike: int
    deal_disengagement_count: int


@dataclass
class BurnoutAttritionResult:
    rep_id: str
    region: str
    burnout_risk: BurnoutRisk
    attrition_pattern: AttritionPattern
    burnout_severity: BurnoutSeverity
    recommended_action: BurnoutAction
    workload_strain_score: float
    engagement_decay_score: float
    quota_pressure_score: float
    flight_signal_score: float
    burnout_composite: float
    is_burnout_risk: bool
    is_flight_risk: bool
    estimated_replacement_cost_usd: float
    burnout_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                       self.rep_id,
            "region":                       self.region,
            "burnout_risk":                 self.burnout_risk.value,
            "attrition_pattern":            self.attrition_pattern.value,
            "burnout_severity":             self.burnout_severity.value,
            "recommended_action":           self.recommended_action.value,
            "workload_strain_score":        self.workload_strain_score,
            "engagement_decay_score":       self.engagement_decay_score,
            "quota_pressure_score":         self.quota_pressure_score,
            "flight_signal_score":          self.flight_signal_score,
            "burnout_composite":            self.burnout_composite,
            "is_burnout_risk":              self.is_burnout_risk,
            "is_flight_risk":               self.is_flight_risk,
            "estimated_replacement_cost_usd": self.estimated_replacement_cost_usd,
            "burnout_signal":               self.burnout_signal,
        }


class SalesRepBurnoutAttritionRiskEngine:

    def __init__(self) -> None:
        self._results: list[BurnoutAttritionResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100)
    # ------------------------------------------------------------------

    def _workload_strain_score(self, inp: BurnoutAttritionInput) -> float:
        score = 0.0

        # After-hours overwork
        if inp.after_hours_activity_pct >= 0.5:
            score += 40.0
        elif inp.after_hours_activity_pct >= 0.35:
            score += 25.0
        elif inp.after_hours_activity_pct >= 0.20:
            score += 12.0

        # Activity surge vs prior period
        if inp.activity_count_prior_period > 0:
            surge = (inp.avg_weekly_activity_count - inp.activity_count_prior_period) / inp.activity_count_prior_period
            if surge >= 0.5:
                score += 30.0
            elif surge >= 0.25:
                score += 18.0
            elif surge >= 0.10:
                score += 8.0

        # PTO deprivation
        if inp.pto_days_allocated_ytd > 0:
            pto_used_pct = inp.pto_days_taken_ytd / inp.pto_days_allocated_ytd
            if pto_used_pct < 0.20:
                score += 20.0
            elif pto_used_pct < 0.40:
                score += 10.0

        # Sick days spike
        if inp.sick_days_last_90d >= 5:
            score += 15.0
        elif inp.sick_days_last_90d >= 3:
            score += 8.0

        return min(score, 100.0)

    def _engagement_decay_score(self, inp: BurnoutAttritionInput) -> float:
        score = 0.0

        # CRM compliance drop
        decay = inp.crm_compliance_prior_pct - inp.crm_update_compliance_pct
        if decay >= 30.0:
            score += 35.0
        elif decay >= 20.0:
            score += 22.0
        elif decay >= 10.0:
            score += 10.0

        # Low voluntary meeting attendance
        if inp.voluntary_meeting_attendance_pct < 0.40:
            score += 30.0
        elif inp.voluntary_meeting_attendance_pct < 0.60:
            score += 15.0

        # Manager distance
        if inp.manager_interaction_days_since >= 21:
            score += 20.0
        elif inp.manager_interaction_days_since >= 14:
            score += 10.0

        # Peer collaboration drop
        if inp.peer_collaboration_score < 30.0:
            score += 15.0
        elif inp.peer_collaboration_score < 50.0:
            score += 7.0

        return min(score, 100.0)

    def _quota_pressure_composite_score(self, inp: BurnoutAttritionInput) -> float:
        score = 0.0

        # Raw pressure score
        if inp.quota_pressure_score >= 80.0:
            score += 40.0
        elif inp.quota_pressure_score >= 60.0:
            score += 25.0
        elif inp.quota_pressure_score >= 40.0:
            score += 12.0

        # Consecutive misses
        if inp.consecutive_missed_quota_periods >= 3:
            score += 30.0
        elif inp.consecutive_missed_quota_periods >= 2:
            score += 18.0
        elif inp.consecutive_missed_quota_periods >= 1:
            score += 8.0

        # Attainment decline
        decline = inp.quota_attainment_prior_pct - inp.quota_attainment_pct
        if decline >= 25.0:
            score += 20.0
        elif decline >= 15.0:
            score += 12.0
        elif decline >= 8.0:
            score += 5.0

        # Escalations raised (frustration signal)
        if inp.escalations_raised_last_90d >= 4:
            score += 10.0
        elif inp.escalations_raised_last_90d >= 2:
            score += 5.0

        return min(score, 100.0)

    def _flight_signal_score(self, inp: BurnoutAttritionInput) -> float:
        score = 0.0

        # LinkedIn activity spike (job searching)
        if inp.linkedin_activity_spike == 1:
            score += 40.0

        # Deal disengagement (stopped caring)
        if inp.deal_disengagement_count >= 5:
            score += 30.0
        elif inp.deal_disengagement_count >= 3:
            score += 18.0
        elif inp.deal_disengagement_count >= 1:
            score += 8.0

        # Compensation dissatisfaction
        if inp.compensation_satisfaction_score < 30.0:
            score += 20.0
        elif inp.compensation_satisfaction_score < 50.0:
            score += 10.0

        # Short tenure with high stress = higher flight risk
        if inp.tenure_months <= 12 and inp.quota_pressure_score >= 60.0:
            score += 10.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: BurnoutAttritionInput,
                         workload: float, engagement: float,
                         quota: float, flight: float) -> AttritionPattern:
        # Priority: manager_conflict > compensation_dissatisfaction > disengagement
        #           > quota_pressure > workload_exhaustion > none
        if inp.escalations_raised_last_90d >= 3 and inp.manager_interaction_days_since >= 14:
            return AttritionPattern.manager_conflict
        if inp.compensation_satisfaction_score < 35.0 and flight >= 20.0:
            return AttritionPattern.compensation_dissatisfaction
        if engagement >= 30.0 and inp.voluntary_meeting_attendance_pct < 0.50:
            return AttritionPattern.disengagement
        if quota >= 25.0 and inp.consecutive_missed_quota_periods >= 2:
            return AttritionPattern.quota_pressure
        if workload >= 25.0 and inp.after_hours_activity_pct >= 0.25:
            return AttritionPattern.workload_exhaustion
        return AttritionPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> BurnoutRisk:
        if composite >= 60:
            return BurnoutRisk.critical
        if composite >= 40:
            return BurnoutRisk.high
        if composite >= 20:
            return BurnoutRisk.moderate
        return BurnoutRisk.low

    def _severity(self, composite: float) -> BurnoutSeverity:
        if composite >= 60:
            return BurnoutSeverity.flight_risk
        if composite >= 40:
            return BurnoutSeverity.at_risk
        if composite >= 20:
            return BurnoutSeverity.watch
        return BurnoutSeverity.healthy

    def _action(self, risk: BurnoutRisk, pattern: AttritionPattern,
                 is_flight_risk: bool) -> BurnoutAction:
        if is_flight_risk or risk == BurnoutRisk.critical:
            if pattern == AttritionPattern.manager_conflict:
                return BurnoutAction.executive_retention
            return BurnoutAction.retention_interview
        if risk == BurnoutRisk.high:
            return BurnoutAction.workload_rebalance
        if risk == BurnoutRisk.moderate:
            return BurnoutAction.wellness_checkin
        return BurnoutAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _is_burnout_risk(self, composite: float, inp: BurnoutAttritionInput) -> bool:
        return (
            composite >= 40
            or inp.sick_days_last_90d >= 5
            or (inp.after_hours_activity_pct >= 0.40 and inp.pto_days_taken_ytd == 0)
        )

    def _is_flight_risk(self, composite: float, inp: BurnoutAttritionInput) -> bool:
        return (
            composite >= 30
            or inp.linkedin_activity_spike == 1
            or inp.consecutive_missed_quota_periods >= 3
        )

    # ------------------------------------------------------------------
    # Cost estimate
    # ------------------------------------------------------------------

    def _replacement_cost(self, inp: BurnoutAttritionInput, composite: float) -> float:
        # Base industry replacement = 150% of annual OTE; proxy OTE from deal activity
        base_replacement_usd = 120_000.0
        return round(base_replacement_usd * (composite / 100.0), 2)

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: BurnoutAttritionInput, pattern: AttritionPattern,
                composite: float) -> str:
        parts: list[str] = []
        if inp.after_hours_activity_pct >= 0.35:
            parts.append(f"{inp.after_hours_activity_pct*100:.0f}% after-hours activity")
        if inp.consecutive_missed_quota_periods >= 2:
            parts.append(f"{inp.consecutive_missed_quota_periods} missed quota periods")
        if inp.linkedin_activity_spike == 1:
            parts.append("LinkedIn activity spike detected")
        if inp.pto_days_allocated_ytd > 0 and inp.pto_days_taken_ytd / inp.pto_days_allocated_ytd < 0.25:
            parts.append(f"only {inp.pto_days_taken_ytd:.0f}d PTO taken")
        if inp.deal_disengagement_count >= 2:
            parts.append(f"{inp.deal_disengagement_count} disengaged deals")
        if not parts:
            return "Rep burnout indicators within healthy range"
        label = pattern.value.replace("_", " ")
        return f"{label.capitalize()} pattern — {' — '.join(parts)} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: BurnoutAttritionInput) -> BurnoutAttritionResult:
        w = round(self._workload_strain_score(inp), 1)
        e = round(self._engagement_decay_score(inp), 1)
        q = round(self._quota_pressure_composite_score(inp), 1)
        f = round(self._flight_signal_score(inp), 1)

        composite = round(w * 0.30 + e * 0.25 + q * 0.30 + f * 0.15, 1)
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, w, e, q, f)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)

        is_br = self._is_burnout_risk(composite, inp)
        is_fr = self._is_flight_risk(composite, inp)

        action = self._action(risk, pattern, is_fr)
        cost   = self._replacement_cost(inp, composite)
        signal = self._signal(inp, pattern, composite)

        result = BurnoutAttritionResult(
            rep_id=inp.rep_id,
            region=inp.region,
            burnout_risk=risk,
            attrition_pattern=pattern,
            burnout_severity=severity,
            recommended_action=action,
            workload_strain_score=w,
            engagement_decay_score=e,
            quota_pressure_score=q,
            flight_signal_score=f,
            burnout_composite=composite,
            is_burnout_risk=is_br,
            is_flight_risk=is_fr,
            estimated_replacement_cost_usd=cost,
            burnout_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[BurnoutAttritionInput]) -> list[BurnoutAttritionResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_burnout_composite": 0.0,
                "burnout_risk_count": 0,
                "flight_risk_count": 0,
                "avg_workload_strain_score": 0.0,
                "avg_engagement_decay_score": 0.0,
                "avg_quota_pressure_score": 0.0,
                "avg_flight_signal_score": 0.0,
                "total_estimated_replacement_cost_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_work = total_eng = total_quot = total_flt = total_cost = 0.0

        for r in self._results:
            risk_counts[r.burnout_risk.value]         = risk_counts.get(r.burnout_risk.value, 0) + 1
            pattern_counts[r.attrition_pattern.value] = pattern_counts.get(r.attrition_pattern.value, 0) + 1
            severity_counts[r.burnout_severity.value] = severity_counts.get(r.burnout_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.burnout_composite
            total_work += r.workload_strain_score
            total_eng  += r.engagement_decay_score
            total_quot += r.quota_pressure_score
            total_flt  += r.flight_signal_score
            total_cost += r.estimated_replacement_cost_usd

        n = len(self._results)

        return {
            "total":                                  n,
            "risk_counts":                            risk_counts,
            "pattern_counts":                         pattern_counts,
            "severity_counts":                        severity_counts,
            "action_counts":                          action_counts,
            "avg_burnout_composite":                  round(total_comp / n, 1),
            "burnout_risk_count":                     sum(1 for r in self._results if r.is_burnout_risk),
            "flight_risk_count":                      sum(1 for r in self._results if r.is_flight_risk),
            "avg_workload_strain_score":               round(total_work / n, 1),
            "avg_engagement_decay_score":              round(total_eng  / n, 1),
            "avg_quota_pressure_score":                round(total_quot / n, 1),
            "avg_flight_signal_score":                 round(total_flt  / n, 1),
            "total_estimated_replacement_cost_usd":    round(total_cost, 2),
        }
