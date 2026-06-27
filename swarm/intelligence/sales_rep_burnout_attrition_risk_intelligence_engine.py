from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class BurnoutRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class BurnoutPattern(str, Enum):
    none                 = "none"
    gradual_disengagement = "gradual_disengagement"
    quota_fatigue        = "quota_fatigue"
    manager_friction     = "manager_friction"
    peer_isolation       = "peer_isolation"
    recognition_drought  = "recognition_drought"


class BurnoutSeverity(str, Enum):
    thriving    = "thriving"
    straining   = "straining"
    burning_out = "burning_out"
    flight_risk = "flight_risk"


class BurnoutAction(str, Enum):
    no_action                    = "no_action"
    wellness_check_in            = "wellness_check_in"
    workload_rebalancing         = "workload_rebalancing"
    recognition_intervention     = "recognition_intervention"
    manager_mediation            = "manager_mediation"
    territory_reassignment       = "territory_reassignment"
    retention_package_discussion = "retention_package_discussion"


@dataclass
class BurnoutInput:
    rep_id:                         str
    region:                         str
    evaluation_period_id:           str
    activity_volume_trend_pct:      float  # -1 to 1 (negative = declining)
    win_rate_trend_pct:             float  # -1 to 1 (negative = declining)
    pipeline_creation_trend_pct:    float  # -1 to 1 (negative = declining)
    avg_deal_size_trend_pct:        float  # -1 to 1 (negative = declining)
    pto_utilization_rate_pct:       float  # 0-1 (how much PTO taken)
    unplanned_absence_days:         int    # days absent unplanned
    overtime_hours_per_week:        float  # avg hours/week over standard
    after_hours_activity_rate_pct:  float  # 0-1 (% activity outside hours)
    manager_satisfaction_score:     float  # 0-1
    peer_collaboration_score:       float  # 0-1
    recognition_received_count:     int    # # of recognitions in period
    voluntary_task_completion_pct:  float  # 0-1
    training_participation_pct:     float  # 0-1
    internal_mobility_applications: int    # # of internal job apps
    tenure_months:                  int
    consecutive_quota_miss_streak:  int
    comp_plan_satisfaction_score:   float  # 0-1 (survey)
    career_path_clarity_score:      float  # 0-1 (survey)
    exit_interview_signals:         int    # 0 or 1 (prior early warning signals logged)
    team_attrition_exposure_pct:    float  # 0-1 (peers who left recently)


@dataclass
class BurnoutResult:
    rep_id:                         str
    region:                         str
    burnout_risk:                   BurnoutRisk
    burnout_pattern:                BurnoutPattern
    burnout_severity:               BurnoutSeverity
    recommended_action:             BurnoutAction
    disengagement_score:            float
    fatigue_score:                  float
    sentiment_score:                float
    performance_erosion_score:      float
    burnout_composite:              float
    has_burnout_gap:                bool
    is_flight_risk:                 bool
    estimated_replacement_cost_usd: float
    burnout_signal:                 str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "burnout_risk":                     self.burnout_risk.value,
            "burnout_pattern":                  self.burnout_pattern.value,
            "burnout_severity":                 self.burnout_severity.value,
            "recommended_action":               self.recommended_action.value,
            "disengagement_score":              self.disengagement_score,
            "fatigue_score":                    self.fatigue_score,
            "sentiment_score":                  self.sentiment_score,
            "performance_erosion_score":        self.performance_erosion_score,
            "burnout_composite":                self.burnout_composite,
            "has_burnout_gap":                  self.has_burnout_gap,
            "is_flight_risk":                   self.is_flight_risk,
            "estimated_replacement_cost_usd":   self.estimated_replacement_cost_usd,
            "burnout_signal":                   self.burnout_signal,
        }


class SalesRepBurnoutAttritionRiskIntelligenceEngine:
    """Detects early-warning burnout and flight-risk signals before reps actually quit."""

    def __init__(self) -> None:
        self._results: List[BurnoutResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────────

    def _disengagement_score(self, inp: BurnoutInput) -> float:
        s = 0.0
        if   inp.activity_volume_trend_pct       <= -0.30: s += 40
        elif inp.activity_volume_trend_pct       <= -0.15: s += 22
        elif inp.activity_volume_trend_pct       <= -0.05: s += 8
        if   inp.training_participation_pct      <= 0.25:  s += 35
        elif inp.training_participation_pct      <= 0.50:  s += 18
        if   inp.voluntary_task_completion_pct   <= 0.40:  s += 25
        elif inp.voluntary_task_completion_pct   <= 0.65:  s += 12
        return min(s, 100.0)

    def _fatigue_score(self, inp: BurnoutInput) -> float:
        s = 0.0
        if   inp.overtime_hours_per_week         >= 20:    s += 40
        elif inp.overtime_hours_per_week         >= 12:    s += 22
        elif inp.overtime_hours_per_week         >= 6:     s += 8
        if   inp.after_hours_activity_rate_pct   >= 0.50:  s += 35
        elif inp.after_hours_activity_rate_pct   >= 0.30:  s += 18
        if   inp.unplanned_absence_days          >= 5:     s += 25
        elif inp.unplanned_absence_days          >= 2:     s += 12
        return min(s, 100.0)

    def _sentiment_score(self, inp: BurnoutInput) -> float:
        s = 0.0
        if   inp.comp_plan_satisfaction_score    <= 0.30:  s += 40
        elif inp.comp_plan_satisfaction_score    <= 0.50:  s += 22
        elif inp.comp_plan_satisfaction_score    <= 0.70:  s += 8
        if   inp.career_path_clarity_score       <= 0.25:  s += 35
        elif inp.career_path_clarity_score       <= 0.50:  s += 18
        if   inp.manager_satisfaction_score      <= 0.30:  s += 25
        elif inp.manager_satisfaction_score      <= 0.50:  s += 12
        return min(s, 100.0)

    def _performance_erosion_score(self, inp: BurnoutInput) -> float:
        s = 0.0
        if   inp.win_rate_trend_pct              <= -0.25: s += 45
        elif inp.win_rate_trend_pct              <= -0.10: s += 25
        elif inp.win_rate_trend_pct              <= -0.03: s += 10
        if   inp.pipeline_creation_trend_pct     <= -0.25: s += 30
        elif inp.pipeline_creation_trend_pct     <= -0.10: s += 15
        if   inp.consecutive_quota_miss_streak   >= 3:     s += 25
        elif inp.consecutive_quota_miss_streak   >= 2:     s += 12
        return min(s, 100.0)

    # ── composite ─────────────────────────────────────────────────────────────

    def _composite(self, dis: float, fat: float, sent: float, perf: float) -> float:
        return min(round(dis * 0.30 + fat * 0.25 + sent * 0.30 + perf * 0.15, 2), 100.0)

    # ── pattern ───────────────────────────────────────────────────────────────

    def _pattern(self, inp: BurnoutInput) -> BurnoutPattern:
        if inp.activity_volume_trend_pct <= -0.20 and inp.training_participation_pct <= 0.40:
            return BurnoutPattern.gradual_disengagement
        if inp.consecutive_quota_miss_streak >= 2 and inp.comp_plan_satisfaction_score <= 0.45:
            return BurnoutPattern.quota_fatigue
        if inp.manager_satisfaction_score <= 0.35 and inp.peer_collaboration_score <= 0.40:
            return BurnoutPattern.manager_friction
        if inp.peer_collaboration_score <= 0.30 and inp.recognition_received_count <= 1:
            return BurnoutPattern.peer_isolation
        if inp.recognition_received_count <= 1 and inp.career_path_clarity_score <= 0.35:
            return BurnoutPattern.recognition_drought
        return BurnoutPattern.none

    # ── thresholds ────────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> BurnoutRisk:
        if   composite >= 60: return BurnoutRisk.critical
        elif composite >= 40: return BurnoutRisk.high
        elif composite >= 20: return BurnoutRisk.moderate
        return BurnoutRisk.low

    def _severity(self, composite: float) -> BurnoutSeverity:
        if   composite >= 60: return BurnoutSeverity.flight_risk
        elif composite >= 40: return BurnoutSeverity.burning_out
        elif composite >= 20: return BurnoutSeverity.straining
        return BurnoutSeverity.thriving

    def _action(self, risk: BurnoutRisk, pattern: BurnoutPattern) -> BurnoutAction:
        if risk == BurnoutRisk.critical:
            if pattern in (BurnoutPattern.manager_friction, BurnoutPattern.peer_isolation):
                return BurnoutAction.retention_package_discussion
            return BurnoutAction.retention_package_discussion
        if risk == BurnoutRisk.high:
            if pattern == BurnoutPattern.gradual_disengagement:
                return BurnoutAction.workload_rebalancing
            if pattern == BurnoutPattern.quota_fatigue:
                return BurnoutAction.territory_reassignment
            if pattern == BurnoutPattern.manager_friction:
                return BurnoutAction.manager_mediation
            if pattern == BurnoutPattern.peer_isolation:
                return BurnoutAction.recognition_intervention
            if pattern == BurnoutPattern.recognition_drought:
                return BurnoutAction.recognition_intervention
            return BurnoutAction.workload_rebalancing
        if risk == BurnoutRisk.moderate:
            return BurnoutAction.wellness_check_in
        return BurnoutAction.no_action

    # ── flags ─────────────────────────────────────────────────────────────────

    def _has_gap(self, inp: BurnoutInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.activity_volume_trend_pct <= -0.20
            or inp.consecutive_quota_miss_streak >= 2
        )

    def _is_flight_risk(self, inp: BurnoutInput, composite: float) -> bool:
        return (
            composite >= 25
            or inp.internal_mobility_applications >= 1
            or inp.comp_plan_satisfaction_score <= 0.40
            or inp.exit_interview_signals >= 1
        )

    # ── replacement cost ──────────────────────────────────────────────────────

    def _replacement_cost(self, inp: BurnoutInput, composite: float) -> float:
        base_salary_estimate_usd = 85_000.0
        replacement_multiplier   = 1.5 + (inp.tenure_months / 24) * 0.5
        risk_weight              = composite / 100
        return round(base_salary_estimate_usd * replacement_multiplier * risk_weight, 2)

    # ── signal ────────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        BurnoutPattern.gradual_disengagement: "Gradual disengagement",
        BurnoutPattern.quota_fatigue:         "Quota fatigue",
        BurnoutPattern.manager_friction:      "Manager friction",
        BurnoutPattern.peer_isolation:        "Peer isolation",
        BurnoutPattern.recognition_drought:   "Recognition drought",
    }

    def _signal(self, inp: BurnoutInput, pattern: BurnoutPattern, composite: float) -> str:
        if composite < 20:
            return (
                "Rep engagement and wellbeing healthy — activity trends, sentiment, "
                "and performance indicators within normal benchmarks"
            )
        label     = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        act_trend = round(inp.activity_volume_trend_pct * 100)
        wr_trend  = round(inp.win_rate_trend_pct * 100)
        mgr_score = round(inp.manager_satisfaction_score * 100)
        comp_int  = round(composite)
        return (
            f"{label} — activity trend {act_trend:+d}% — win rate trend {wr_trend:+d}% — "
            f"manager satisfaction {mgr_score}% — composite {comp_int}"
        )

    # ── public API ────────────────────────────────────────────────────────────

    def assess(self, inp: BurnoutInput) -> BurnoutResult:
        dis  = self._disengagement_score(inp)
        fat  = self._fatigue_score(inp)
        sent = self._sentiment_score(inp)
        perf = self._performance_erosion_score(inp)
        comp = self._composite(dis, fat, sent, perf)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = BurnoutResult(
            rep_id                          = inp.rep_id,
            region                          = inp.region,
            burnout_risk                    = risk,
            burnout_pattern                 = pattern,
            burnout_severity                = severity,
            recommended_action              = action,
            disengagement_score             = dis,
            fatigue_score                   = fat,
            sentiment_score                 = sent,
            performance_erosion_score       = perf,
            burnout_composite               = comp,
            has_burnout_gap                 = self._has_gap(inp, comp),
            is_flight_risk                  = self._is_flight_risk(inp, comp),
            estimated_replacement_cost_usd  = self._replacement_cost(inp, comp),
            burnout_signal                  = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[BurnoutInput]) -> List[BurnoutResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_burnout_composite": 0.0,
                "burnout_gap_count": 0,
                "flight_risk_count": 0,
                "avg_disengagement_score": 0.0,
                "avg_fatigue_score": 0.0,
                "avg_sentiment_score": 0.0,
                "avg_performance_erosion_score": 0.0,
                "total_estimated_replacement_cost_usd": 0.0,
            }

        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        total_comp = total_dis = total_fat = total_sent = total_perf = total_rc = 0.0
        gap_count = flight_count = 0

        for res in self._results:
            risk_counts[res.burnout_risk.value]         = risk_counts.get(res.burnout_risk.value, 0) + 1
            pattern_counts[res.burnout_pattern.value]   = pattern_counts.get(res.burnout_pattern.value, 0) + 1
            severity_counts[res.burnout_severity.value] = severity_counts.get(res.burnout_severity.value, 0) + 1
            action_counts[res.recommended_action.value] = action_counts.get(res.recommended_action.value, 0) + 1
            total_comp  += res.burnout_composite
            total_dis   += res.disengagement_score
            total_fat   += res.fatigue_score
            total_sent  += res.sentiment_score
            total_perf  += res.performance_erosion_score
            total_rc    += res.estimated_replacement_cost_usd
            if res.has_burnout_gap:   gap_count    += 1
            if res.is_flight_risk:    flight_count += 1

        n = len(self._results)
        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_burnout_composite":                round(total_comp / n, 1),
            "burnout_gap_count":                    gap_count,
            "flight_risk_count":                    flight_count,
            "avg_disengagement_score":              round(total_dis / n, 1),
            "avg_fatigue_score":                    round(total_fat / n, 1),
            "avg_sentiment_score":                  round(total_sent / n, 1),
            "avg_performance_erosion_score":        round(total_perf / n, 1),
            "total_estimated_replacement_cost_usd": round(total_rc, 2),
        }
