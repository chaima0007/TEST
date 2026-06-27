"""
Module 216 — Sales Rep Burnout & Productivity Decay Engine
Detects early warning signals of rep burnout through activity decay,
engagement drop, error pattern increases, and productivity cliff risks.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class BurnoutRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class BurnoutPattern(str, Enum):
    none                   = "none"
    activity_cliff         = "activity_cliff"
    quality_erosion        = "quality_erosion"
    disengagement_spiral   = "disengagement_spiral"
    weekend_overload       = "weekend_overload"
    pipeline_withdrawal    = "pipeline_withdrawal"


class BurnoutSeverity(str, Enum):
    thriving    = "thriving"
    stressed    = "stressed"
    fatigued    = "fatigued"
    burned_out  = "burned_out"


class BurnoutAction(str, Enum):
    no_action                      = "no_action"
    productivity_monitoring        = "productivity_monitoring"
    workload_review_conversation   = "workload_review_conversation"
    territory_rebalancing          = "territory_rebalancing"
    coaching_cadence_increase      = "coaching_cadence_increase"
    quota_relief_assessment        = "quota_relief_assessment"
    manager_wellbeing_check_in     = "manager_wellbeing_check_in"
    immediate_support_intervention = "immediate_support_intervention"
    retention_risk_escalation      = "retention_risk_escalation"


@dataclass
class BurnoutInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    # Activity volume decay
    outbound_activity_decay_rate_pct: float    # % drop in outbound vs prior period
    meetings_booked_decay_rate_pct: float      # % drop in meetings booked
    pipeline_creation_decay_rate_pct: float    # % drop in new pipeline created
    avg_response_time_increase_pct: float      # % increase in response time to prospects
    # Quality indicators
    proposal_error_rate_pct: float             # % proposals with errors/revisions
    crm_entry_accuracy_drop_pct: float         # % drop in CRM data accuracy
    follow_up_timeliness_score: float          # 0-1 (lower = worse)
    call_quality_score_decay_pct: float        # % drop in call quality scores
    # Engagement signals
    manager_meeting_attendance_rate_pct: float # % 1:1s attended vs scheduled
    team_activity_participation_rate_pct: float # % team activities participated
    enablement_session_attendance_rate_pct: float  # % training sessions attended
    voluntary_overtime_rate_pct: float         # % of work done outside hours
    # Work pattern stress
    weekend_work_frequency_pct: float          # % weekends with significant activity
    avg_daily_work_hours: float                # avg hours worked per day
    vacation_utilization_pct: float            # % vacation days taken (low = stressed)
    # Rep sentiment proxy
    deal_abandonment_rate_pct: float           # % deals dropped prematurely
    prospecting_avoidance_rate_pct: float      # % days with zero prospecting activity
    # Volume context
    quota_attainment_trend: float              # 0-1 (quota attainment vs prior period)
    total_active_deals: int
    avg_deal_value_usd: float


@dataclass
class BurnoutResult:
    rep_id: str
    region: str
    burnout_risk: str
    burnout_pattern: str
    burnout_severity: str
    recommended_action: str
    activity_score: float
    quality_score: float
    engagement_score: float
    stress_score: float
    burnout_composite: float
    has_burnout_signal: bool
    requires_manager_action: bool
    estimated_productivity_loss_usd: float
    burnout_signal: str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                          self.rep_id,
            "region":                          self.region,
            "burnout_risk":                    self.burnout_risk,
            "burnout_pattern":                 self.burnout_pattern,
            "burnout_severity":                self.burnout_severity,
            "recommended_action":              self.recommended_action,
            "activity_score":                  self.activity_score,
            "quality_score":                   self.quality_score,
            "engagement_score":                self.engagement_score,
            "stress_score":                    self.stress_score,
            "burnout_composite":               self.burnout_composite,
            "has_burnout_signal":              self.has_burnout_signal,
            "requires_manager_action":         self.requires_manager_action,
            "estimated_productivity_loss_usd": self.estimated_productivity_loss_usd,
            "burnout_signal":                  self.burnout_signal,
        }


class SalesRepBurnoutProductivityDecayEngine:
    def __init__(self) -> None:
        self._results: List[BurnoutResult] = []

    # ── Sub-scores ────────────────────────────────────────────────────────────

    def _activity_score(self, i: BurnoutInput) -> float:
        s = 0
        if   i.outbound_activity_decay_rate_pct   >= 0.50: s += 40
        elif i.outbound_activity_decay_rate_pct   >= 0.30: s += 22
        elif i.outbound_activity_decay_rate_pct   >= 0.15: s += 8

        if   i.pipeline_creation_decay_rate_pct   >= 0.45: s += 35
        elif i.pipeline_creation_decay_rate_pct   >= 0.25: s += 18

        if   i.prospecting_avoidance_rate_pct     >= 0.50: s += 25
        elif i.prospecting_avoidance_rate_pct     >= 0.30: s += 12
        return min(s, 100)

    def _quality_score(self, i: BurnoutInput) -> float:
        s = 0
        if   i.proposal_error_rate_pct            >= 0.30: s += 40
        elif i.proposal_error_rate_pct            >= 0.15: s += 22
        elif i.proposal_error_rate_pct            >= 0.07: s += 8

        if   i.follow_up_timeliness_score         <= 0.30: s += 35
        elif i.follow_up_timeliness_score         <= 0.55: s += 18

        if   i.deal_abandonment_rate_pct          >= 0.25: s += 25
        elif i.deal_abandonment_rate_pct          >= 0.12: s += 12
        return min(s, 100)

    def _engagement_score(self, i: BurnoutInput) -> float:
        s = 0
        if   i.manager_meeting_attendance_rate_pct   <= 0.55: s += 45
        elif i.manager_meeting_attendance_rate_pct   <= 0.75: s += 25
        elif i.manager_meeting_attendance_rate_pct   <= 0.88: s += 10

        if   i.enablement_session_attendance_rate_pct <= 0.35: s += 30
        elif i.enablement_session_attendance_rate_pct <= 0.60: s += 15

        if   i.vacation_utilization_pct              <= 0.20: s += 25
        elif i.vacation_utilization_pct              <= 0.45: s += 12
        return min(s, 100)

    def _stress_score(self, i: BurnoutInput) -> float:
        s = 0
        if   i.weekend_work_frequency_pct         >= 0.55: s += 45
        elif i.weekend_work_frequency_pct         >= 0.35: s += 25
        elif i.weekend_work_frequency_pct         >= 0.20: s += 10

        if   i.avg_daily_work_hours               >= 12.0: s += 30
        elif i.avg_daily_work_hours               >= 10.0: s += 15

        if   i.voluntary_overtime_rate_pct        >= 0.50: s += 25
        elif i.voluntary_overtime_rate_pct        >= 0.30: s += 12
        return min(s, 100)

    # ── Composite ─────────────────────────────────────────────────────────────

    def _composite(self, ac: float, qu: float, en: float, st: float) -> float:
        return min(round(ac * 0.30 + qu * 0.25 + en * 0.25 + st * 0.20, 2), 100.0)

    # ── Risk / Severity ───────────────────────────────────────────────────────

    def _risk(self, c: float) -> BurnoutRisk:
        if c >= 60: return BurnoutRisk.critical
        if c >= 40: return BurnoutRisk.high
        if c >= 20: return BurnoutRisk.moderate
        return BurnoutRisk.low

    def _severity(self, c: float) -> BurnoutSeverity:
        if c >= 60: return BurnoutSeverity.burned_out
        if c >= 40: return BurnoutSeverity.fatigued
        if c >= 20: return BurnoutSeverity.stressed
        return BurnoutSeverity.thriving

    # ── Pattern ───────────────────────────────────────────────────────────────

    def _pattern(self, i: BurnoutInput) -> BurnoutPattern:
        if (i.outbound_activity_decay_rate_pct >= 0.45
                and i.pipeline_creation_decay_rate_pct >= 0.40):
            return BurnoutPattern.activity_cliff
        if (i.proposal_error_rate_pct >= 0.25
                and i.follow_up_timeliness_score <= 0.40):
            return BurnoutPattern.quality_erosion
        if (i.weekend_work_frequency_pct >= 0.50
                and i.avg_daily_work_hours >= 11.0):
            return BurnoutPattern.weekend_overload
        if (i.manager_meeting_attendance_rate_pct <= 0.60
                and i.enablement_session_attendance_rate_pct <= 0.40):
            return BurnoutPattern.disengagement_spiral
        if (i.deal_abandonment_rate_pct >= 0.22
                and i.prospecting_avoidance_rate_pct >= 0.35):
            return BurnoutPattern.pipeline_withdrawal
        return BurnoutPattern.none

    # ── Action ────────────────────────────────────────────────────────────────

    def _action(self, risk: BurnoutRisk, pat: BurnoutPattern) -> BurnoutAction:
        if risk == BurnoutRisk.critical:
            if pat in (BurnoutPattern.activity_cliff, BurnoutPattern.pipeline_withdrawal):
                return BurnoutAction.retention_risk_escalation
            return BurnoutAction.immediate_support_intervention
        if risk == BurnoutRisk.high:
            if pat == BurnoutPattern.activity_cliff:        return BurnoutAction.quota_relief_assessment
            if pat == BurnoutPattern.quality_erosion:       return BurnoutAction.coaching_cadence_increase
            if pat == BurnoutPattern.weekend_overload:      return BurnoutAction.territory_rebalancing
            if pat == BurnoutPattern.disengagement_spiral:  return BurnoutAction.manager_wellbeing_check_in
            if pat == BurnoutPattern.pipeline_withdrawal:   return BurnoutAction.workload_review_conversation
            return BurnoutAction.productivity_monitoring
        if risk == BurnoutRisk.moderate:
            return BurnoutAction.productivity_monitoring
        return BurnoutAction.no_action

    # ── Signal ────────────────────────────────────────────────────────────────

    def _signal(self, i: BurnoutInput, pat: BurnoutPattern, comp: float) -> str:
        if comp < 20:
            return "Rep productivity healthy — activity levels, quality, engagement and stress indicators within benchmark targets"
        labels = {
            BurnoutPattern.activity_cliff:        "Activity cliff",
            BurnoutPattern.quality_erosion:       "Quality erosion",
            BurnoutPattern.disengagement_spiral:  "Disengagement spiral",
            BurnoutPattern.weekend_overload:      "Weekend overload",
            BurnoutPattern.pipeline_withdrawal:   "Pipeline withdrawal",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — {round(i.outbound_activity_decay_rate_pct*100)}% activity decay — "
            f"{round(i.weekend_work_frequency_pct*100)}% weekend work — "
            f"{round(i.quota_attainment_trend*100)}% quota trend — "
            f"composite {round(comp)}"
        )

    # ── Flags ─────────────────────────────────────────────────────────────────

    def _has_burnout_signal(self, i: BurnoutInput, comp: float) -> bool:
        return (comp >= 40
                or i.outbound_activity_decay_rate_pct >= 0.30
                or i.quota_attainment_trend <= 0.70)

    def _requires_manager_action(self, i: BurnoutInput, comp: float) -> bool:
        return (comp >= 25
                or i.manager_meeting_attendance_rate_pct <= 0.75
                or i.weekend_work_frequency_pct >= 0.30)

    # ── Productivity loss estimate ────────────────────────────────────────────

    def _productivity_loss(self, i: BurnoutInput, comp: float) -> float:
        return round(
            i.total_active_deals
            * i.avg_deal_value_usd
            * (1 - i.quota_attainment_trend)
            * (comp / 100),
            2,
        )

    # ── Public API ────────────────────────────────────────────────────────────

    def assess(self, i: BurnoutInput) -> BurnoutResult:
        ac  = self._activity_score(i)
        qu  = self._quality_score(i)
        en  = self._engagement_score(i)
        st  = self._stress_score(i)
        comp = self._composite(ac, qu, en, st)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = BurnoutResult(
            rep_id=i.rep_id,
            region=i.region,
            burnout_risk=risk.value,
            burnout_pattern=pat.value,
            burnout_severity=sev.value,
            recommended_action=act.value,
            activity_score=ac,
            quality_score=qu,
            engagement_score=en,
            stress_score=st,
            burnout_composite=comp,
            has_burnout_signal=self._has_burnout_signal(i, comp),
            requires_manager_action=self._requires_manager_action(i, comp),
            estimated_productivity_loss_usd=self._productivity_loss(i, comp),
            burnout_signal=self._signal(i, pat, comp),
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
                "burnout_signal_count": 0,
                "manager_action_count": 0,
                "avg_activity_score": 0.0,
                "avg_quality_score": 0.0,
                "avg_engagement_score": 0.0,
                "avg_stress_score": 0.0,
                "total_estimated_productivity_loss_usd": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tac = tqu = ten = tst = tcomp = tpl = 0.0
        gc = mc = 0
        for r in self._results:
            rc[r.burnout_risk]      = rc.get(r.burnout_risk, 0)      + 1
            pc[r.burnout_pattern]   = pc.get(r.burnout_pattern, 0)   + 1
            sc[r.burnout_severity]  = sc.get(r.burnout_severity, 0)  + 1
            ac[r.recommended_action] = ac.get(r.recommended_action, 0) + 1
            tac  += r.activity_score
            tqu  += r.quality_score
            ten  += r.engagement_score
            tst  += r.stress_score
            tcomp += r.burnout_composite
            tpl  += r.estimated_productivity_loss_usd
            if r.has_burnout_signal:       gc += 1
            if r.requires_manager_action:  mc += 1
        return {
            "total":                                   n,
            "risk_counts":                             rc,
            "pattern_counts":                          pc,
            "severity_counts":                         sc,
            "action_counts":                           ac,
            "avg_burnout_composite":                   round(tcomp / n, 1),
            "burnout_signal_count":                    gc,
            "manager_action_count":                    mc,
            "avg_activity_score":                      round(tac / n, 1),
            "avg_quality_score":                       round(tqu / n, 1),
            "avg_engagement_score":                    round(ten / n, 1),
            "avg_stress_score":                        round(tst / n, 1),
            "total_estimated_productivity_loss_usd":   round(tpl, 2),
        }
