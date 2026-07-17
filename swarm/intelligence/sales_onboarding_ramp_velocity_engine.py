"""
Module 218 — Sales Onboarding Ramp Velocity Engine
Tracks how fast new sales reps ramp to full productivity,
detects stalled ramp patterns, and predicts ramp completion risk.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class RampRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class RampPattern(str, Enum):
    none               = "none"
    stalled_ramp       = "stalled_ramp"
    plateau_trap       = "plateau_trap"
    knowledge_gap      = "knowledge_gap"
    activity_laggard   = "activity_laggard"
    pipeline_void      = "pipeline_void"


class RampSeverity(str, Enum):
    on_track   = "on_track"
    at_risk    = "at_risk"
    stalled    = "stalled"
    failed     = "failed"


class RampAction(str, Enum):
    no_action                    = "no_action"
    ramp_monitoring              = "ramp_monitoring"
    enablement_acceleration      = "enablement_acceleration"
    pipeline_building_support    = "pipeline_building_support"
    skills_gap_coaching          = "skills_gap_coaching"
    manager_ramp_intervention    = "manager_ramp_intervention"
    territory_assignment_review  = "territory_assignment_review"
    ramp_plan_reset              = "ramp_plan_reset"
    early_exit_assessment        = "early_exit_assessment"


@dataclass
class RampInput:
    rep_id: str
    region: str
    cohort_id: str
    # Ramp timeline
    weeks_since_start: int                      # how long in role
    expected_ramp_weeks: int                    # target ramp duration
    quota_attainment_at_ramp_pct: float         # % quota achieved at current point in ramp
    weeks_to_first_deal: int                    # weeks elapsed before first closed deal
    # Activity ramp
    outbound_activity_vs_benchmark_pct: float   # % of benchmark outbound activity achieved
    meetings_booked_vs_benchmark_pct: float     # % of benchmark meetings booked
    pipeline_created_vs_benchmark_pct: float    # % of expected pipeline created
    deals_in_stage_3plus_vs_benchmark_pct: float # % of benchmark late-stage deals
    # Knowledge & readiness
    product_certification_completion_pct: float # % product certs completed
    sales_playbook_completion_pct: float        # % sales playbook milestones completed
    call_shadowing_hours_completed: float       # hrs of call shadowing done
    manager_coaching_sessions_completed: int    # coaching sessions held
    # Engagement & retention signals
    onboarding_portal_activity_score: float     # 0-1 engagement with learning portal
    peer_collaboration_rate_pct: float          # % of team activities joined
    voluntary_extra_training_pct: float         # % extra training taken beyond required
    # Early performance
    win_rate_vs_cohort_avg: float               # win rate vs same-cohort average (1.0=parity)
    avg_deal_size_vs_cohort_avg: float          # deal size vs cohort avg (1.0=parity)
    # Volume context
    total_deals_attempted: int
    avg_deal_value_usd: float


@dataclass
class RampResult:
    rep_id: str
    region: str
    ramp_risk: str
    ramp_pattern: str
    ramp_severity: str
    recommended_action: str
    velocity_score: float
    readiness_score: float
    activity_score: float
    engagement_score: float
    ramp_composite: float
    has_ramp_gap: bool
    requires_intervention: bool
    estimated_ramp_delay_weeks: float
    ramp_signal: str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                     self.rep_id,
            "region":                     self.region,
            "ramp_risk":                  self.ramp_risk,
            "ramp_pattern":               self.ramp_pattern,
            "ramp_severity":              self.ramp_severity,
            "recommended_action":         self.recommended_action,
            "velocity_score":             self.velocity_score,
            "readiness_score":            self.readiness_score,
            "activity_score":             self.activity_score,
            "engagement_score":           self.engagement_score,
            "ramp_composite":             self.ramp_composite,
            "has_ramp_gap":               self.has_ramp_gap,
            "requires_intervention":      self.requires_intervention,
            "estimated_ramp_delay_weeks": self.estimated_ramp_delay_weeks,
            "ramp_signal":                self.ramp_signal,
        }


class SalesOnboardingRampVelocityEngine:
    def __init__(self) -> None:
        self._results: List[RampResult] = []

    # ── Sub-scores ────────────────────────────────────────────────────────────

    def _velocity_score(self, i: RampInput) -> float:
        s = 0
        ramp_progress = i.weeks_since_start / max(i.expected_ramp_weeks, 1)
        quota_gap = max(0.0, ramp_progress - i.quota_attainment_at_ramp_pct)
        if   quota_gap >= 0.50: s += 40
        elif quota_gap >= 0.30: s += 22
        elif quota_gap >= 0.15: s += 8

        if   i.weeks_to_first_deal >= int(i.expected_ramp_weeks * 0.70): s += 35
        elif i.weeks_to_first_deal >= int(i.expected_ramp_weeks * 0.45): s += 18

        if   i.pipeline_created_vs_benchmark_pct <= 0.30: s += 25
        elif i.pipeline_created_vs_benchmark_pct <= 0.55: s += 12
        return min(s, 100)

    def _readiness_score(self, i: RampInput) -> float:
        s = 0
        if   i.product_certification_completion_pct  <= 0.40: s += 40
        elif i.product_certification_completion_pct  <= 0.65: s += 22
        elif i.product_certification_completion_pct  <= 0.80: s += 8

        if   i.sales_playbook_completion_pct         <= 0.35: s += 35
        elif i.sales_playbook_completion_pct         <= 0.60: s += 18

        if   i.manager_coaching_sessions_completed   <= 2:    s += 25
        elif i.manager_coaching_sessions_completed   <= 5:    s += 12
        return min(s, 100)

    def _activity_score(self, i: RampInput) -> float:
        s = 0
        if   i.outbound_activity_vs_benchmark_pct    <= 0.30: s += 45
        elif i.outbound_activity_vs_benchmark_pct    <= 0.55: s += 25
        elif i.outbound_activity_vs_benchmark_pct    <= 0.75: s += 10

        if   i.meetings_booked_vs_benchmark_pct      <= 0.30: s += 30
        elif i.meetings_booked_vs_benchmark_pct      <= 0.55: s += 15

        if   i.deals_in_stage_3plus_vs_benchmark_pct <= 0.20: s += 25
        elif i.deals_in_stage_3plus_vs_benchmark_pct <= 0.45: s += 12
        return min(s, 100)

    def _engagement_score(self, i: RampInput) -> float:
        s = 0
        if   i.onboarding_portal_activity_score      <= 0.25: s += 40
        elif i.onboarding_portal_activity_score      <= 0.50: s += 22
        elif i.onboarding_portal_activity_score      <= 0.70: s += 8

        if   i.peer_collaboration_rate_pct           <= 0.20: s += 35
        elif i.peer_collaboration_rate_pct           <= 0.45: s += 18

        if   i.voluntary_extra_training_pct          <= 0.10: s += 25
        elif i.voluntary_extra_training_pct          <= 0.30: s += 12
        return min(s, 100)

    # ── Composite ─────────────────────────────────────────────────────────────

    def _composite(self, ve: float, re: float, ac: float, en: float) -> float:
        return min(round(ve * 0.30 + re * 0.25 + ac * 0.25 + en * 0.20, 2), 100.0)

    # ── Risk / Severity ───────────────────────────────────────────────────────

    def _risk(self, c: float) -> RampRisk:
        if c >= 60: return RampRisk.critical
        if c >= 40: return RampRisk.high
        if c >= 20: return RampRisk.moderate
        return RampRisk.low

    def _severity(self, c: float) -> RampSeverity:
        if c >= 60: return RampSeverity.failed
        if c >= 40: return RampSeverity.stalled
        if c >= 20: return RampSeverity.at_risk
        return RampSeverity.on_track

    # ── Pattern ───────────────────────────────────────────────────────────────

    def _pattern(self, i: RampInput) -> RampPattern:
        ramp_progress = i.weeks_since_start / max(i.expected_ramp_weeks, 1)
        quota_gap = max(0.0, ramp_progress - i.quota_attainment_at_ramp_pct)
        if (quota_gap >= 0.40
                and i.pipeline_created_vs_benchmark_pct <= 0.40):
            return RampPattern.stalled_ramp
        if (i.quota_attainment_at_ramp_pct >= 0.55
                and i.deals_in_stage_3plus_vs_benchmark_pct <= 0.30):
            return RampPattern.plateau_trap
        if (i.product_certification_completion_pct <= 0.50
                and i.sales_playbook_completion_pct <= 0.50):
            return RampPattern.knowledge_gap
        if (i.outbound_activity_vs_benchmark_pct <= 0.40
                and i.meetings_booked_vs_benchmark_pct <= 0.40):
            return RampPattern.activity_laggard
        if (i.pipeline_created_vs_benchmark_pct <= 0.35
                and i.deals_in_stage_3plus_vs_benchmark_pct <= 0.25):
            return RampPattern.pipeline_void
        return RampPattern.none

    # ── Action ────────────────────────────────────────────────────────────────

    def _action(self, risk: RampRisk, pat: RampPattern) -> RampAction:
        if risk == RampRisk.critical:
            if pat in (RampPattern.stalled_ramp, RampPattern.pipeline_void):
                return RampAction.early_exit_assessment
            return RampAction.ramp_plan_reset
        if risk == RampRisk.high:
            if pat == RampPattern.stalled_ramp:      return RampAction.manager_ramp_intervention
            if pat == RampPattern.plateau_trap:      return RampAction.territory_assignment_review
            if pat == RampPattern.knowledge_gap:     return RampAction.skills_gap_coaching
            if pat == RampPattern.activity_laggard:  return RampAction.enablement_acceleration
            if pat == RampPattern.pipeline_void:     return RampAction.pipeline_building_support
            return RampAction.ramp_monitoring
        if risk == RampRisk.moderate:
            return RampAction.ramp_monitoring
        return RampAction.no_action

    # ── Signal ────────────────────────────────────────────────────────────────

    def _signal(self, i: RampInput, pat: RampPattern, comp: float) -> str:
        if comp < 20:
            return "Rep ramp on track — velocity, readiness, activity, and engagement within expected benchmarks"
        labels = {
            RampPattern.stalled_ramp:     "Stalled ramp",
            RampPattern.plateau_trap:     "Plateau trap",
            RampPattern.knowledge_gap:    "Knowledge gap",
            RampPattern.activity_laggard: "Activity laggard",
            RampPattern.pipeline_void:    "Pipeline void",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        ramp_pct = round(i.weeks_since_start / max(i.expected_ramp_weeks, 1) * 100)
        return (
            f"{label} — {ramp_pct}% ramp elapsed — "
            f"{round(i.quota_attainment_at_ramp_pct*100)}% quota attained — "
            f"{round(i.pipeline_created_vs_benchmark_pct*100)}% pipeline benchmark — "
            f"composite {round(comp)}"
        )

    # ── Flags ─────────────────────────────────────────────────────────────────

    def _has_ramp_gap(self, i: RampInput, comp: float) -> bool:
        ramp_progress = i.weeks_since_start / max(i.expected_ramp_weeks, 1)
        return (comp >= 40
                or i.quota_attainment_at_ramp_pct <= ramp_progress * 0.60
                or i.pipeline_created_vs_benchmark_pct <= 0.40)

    def _requires_intervention(self, i: RampInput, comp: float) -> bool:
        return (comp >= 25
                or i.product_certification_completion_pct <= 0.65
                or i.outbound_activity_vs_benchmark_pct <= 0.55)

    # ── Ramp delay estimate ───────────────────────────────────────────────────

    def _ramp_delay(self, i: RampInput, comp: float) -> float:
        ramp_progress = i.weeks_since_start / max(i.expected_ramp_weeks, 1)
        quota_gap = max(0.0, ramp_progress - i.quota_attainment_at_ramp_pct)
        return round(
            quota_gap * i.expected_ramp_weeks * (comp / 100),
            1,
        )

    # ── Public API ────────────────────────────────────────────────────────────

    def assess(self, i: RampInput) -> RampResult:
        ve  = self._velocity_score(i)
        re  = self._readiness_score(i)
        ac  = self._activity_score(i)
        en  = self._engagement_score(i)
        comp = self._composite(ve, re, ac, en)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = RampResult(
            rep_id=i.rep_id,
            region=i.region,
            ramp_risk=risk.value,
            ramp_pattern=pat.value,
            ramp_severity=sev.value,
            recommended_action=act.value,
            velocity_score=ve,
            readiness_score=re,
            activity_score=ac,
            engagement_score=en,
            ramp_composite=comp,
            has_ramp_gap=self._has_ramp_gap(i, comp),
            requires_intervention=self._requires_intervention(i, comp),
            estimated_ramp_delay_weeks=self._ramp_delay(i, comp),
            ramp_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[RampInput]) -> List[RampResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_ramp_composite": 0.0,
                "ramp_gap_count": 0,
                "intervention_count": 0,
                "avg_velocity_score": 0.0,
                "avg_readiness_score": 0.0,
                "avg_activity_score": 0.0,
                "avg_engagement_score": 0.0,
                "avg_estimated_ramp_delay_weeks": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tve = tre = tac = ten = tcomp = tdel = 0.0
        gc = ic = 0
        for r in self._results:
            rc[r.ramp_risk]      = rc.get(r.ramp_risk, 0)      + 1
            pc[r.ramp_pattern]   = pc.get(r.ramp_pattern, 0)   + 1
            sc[r.ramp_severity]  = sc.get(r.ramp_severity, 0)  + 1
            ac[r.recommended_action] = ac.get(r.recommended_action, 0) + 1
            tve  += r.velocity_score
            tre  += r.readiness_score
            tac  += r.activity_score
            ten  += r.engagement_score
            tcomp += r.ramp_composite
            tdel += r.estimated_ramp_delay_weeks
            if r.has_ramp_gap:        gc += 1
            if r.requires_intervention: ic += 1
        return {
            "total":                          n,
            "risk_counts":                    rc,
            "pattern_counts":                 pc,
            "severity_counts":                sc,
            "action_counts":                  ac,
            "avg_ramp_composite":             round(tcomp / n, 1),
            "ramp_gap_count":                 gc,
            "intervention_count":             ic,
            "avg_velocity_score":             round(tve / n, 1),
            "avg_readiness_score":            round(tre / n, 1),
            "avg_activity_score":             round(tac / n, 1),
            "avg_engagement_score":           round(ten / n, 1),
            "avg_estimated_ramp_delay_weeks": round(tdel / n, 1),
        }
