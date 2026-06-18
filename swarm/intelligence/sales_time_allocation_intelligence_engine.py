from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class AllocationRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class AllocationPattern(str, Enum):
    none               = "none"
    admin_overload     = "admin_overload"
    meeting_fatigue    = "meeting_fatigue"
    low_selling_time   = "low_selling_time"
    reactive_mode      = "reactive_mode"
    time_fragmentation = "time_fragmentation"


class AllocationSeverity(str, Enum):
    optimized  = "optimized"
    developing = "developing"
    burdened   = "burdened"
    fragmented = "fragmented"


class AllocationAction(str, Enum):
    no_action               = "no_action"
    time_audit_coaching     = "time_audit_coaching"
    admin_reduction_plan    = "admin_reduction_plan"
    meeting_hygiene_review  = "meeting_hygiene_review"
    selling_time_recovery   = "selling_time_recovery"
    workflow_optimization   = "workflow_optimization"


@dataclass
class TimeAllocationInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    total_hours_tracked: float
    customer_facing_hours: float
    prospecting_hours: float
    admin_hours: float
    internal_meeting_hours: float
    proposal_prep_hours: float
    travel_hours: float
    training_hours: float
    emails_sent_count: int
    avg_email_response_time_minutes: float
    calls_made_count: int
    avg_call_duration_minutes: float
    meetings_attended_count: int
    internal_meetings_count: int
    demo_hours: float
    pipeline_review_hours: float
    coaching_sessions_hours: float
    focus_blocks_per_week: float
    after_hours_work_hours: float


@dataclass
class TimeAllocationResult:
    rep_id: str
    region: str
    allocation_risk: AllocationRisk
    allocation_pattern: AllocationPattern
    allocation_severity: AllocationSeverity
    recommended_action: AllocationAction
    selling_time_score: float
    admin_burden_score: float
    activity_quality_score: float
    time_discipline_score: float
    time_allocation_composite: float
    has_time_gap: bool
    requires_allocation_coaching: bool
    estimated_selling_hours_lost_per_week: float
    allocation_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                               self.rep_id,
            "region":                               self.region,
            "allocation_risk":                      self.allocation_risk.value,
            "allocation_pattern":                   self.allocation_pattern.value,
            "allocation_severity":                  self.allocation_severity.value,
            "recommended_action":                   self.recommended_action.value,
            "selling_time_score":                   self.selling_time_score,
            "admin_burden_score":                   self.admin_burden_score,
            "activity_quality_score":               self.activity_quality_score,
            "time_discipline_score":                self.time_discipline_score,
            "time_allocation_composite":            self.time_allocation_composite,
            "has_time_gap":                         self.has_time_gap,
            "requires_allocation_coaching":         self.requires_allocation_coaching,
            "estimated_selling_hours_lost_per_week": self.estimated_selling_hours_lost_per_week,
            "allocation_signal":                    self.allocation_signal,
        }


class SalesTimeAllocationIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[TimeAllocationResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _selling_time_score(self, inp: TimeAllocationInput) -> float:
        score = 0.0
        total = max(inp.total_hours_tracked, 1.0)

        selling_pct = (inp.customer_facing_hours + inp.proposal_prep_hours) / total
        if selling_pct < 0.20:
            score += 45.0
        elif selling_pct < 0.30:
            score += 25.0
        elif selling_pct < 0.40:
            score += 10.0

        demo_pct = inp.demo_hours / total
        if demo_pct < 0.05:
            score += 25.0
        elif demo_pct < 0.10:
            score += 12.0

        prospecting_pct = inp.prospecting_hours / total
        if prospecting_pct < 0.10:
            score += 20.0
        elif prospecting_pct < 0.15:
            score += 10.0

        return min(score, 100.0)

    def _admin_burden_score(self, inp: TimeAllocationInput) -> float:
        score = 0.0
        total = max(inp.total_hours_tracked, 1.0)

        admin_pct = (inp.admin_hours + inp.travel_hours) / total
        if admin_pct >= 0.30:
            score += 40.0
        elif admin_pct >= 0.20:
            score += 20.0
        elif admin_pct >= 0.15:
            score += 8.0

        internal_pct = inp.internal_meeting_hours / total
        if internal_pct >= 0.25:
            score += 35.0
        elif internal_pct >= 0.15:
            score += 18.0
        elif internal_pct >= 0.10:
            score += 7.0

        if inp.internal_meetings_count >= 15:
            score += 20.0
        elif inp.internal_meetings_count >= 10:
            score += 10.0

        return min(score, 100.0)

    def _activity_quality_score(self, inp: TimeAllocationInput) -> float:
        score = 0.0
        total = max(inp.total_hours_tracked, 1.0)

        if inp.avg_call_duration_minutes < 5.0:
            score += 35.0
        elif inp.avg_call_duration_minutes < 10.0:
            score += 18.0
        elif inp.avg_call_duration_minutes < 15.0:
            score += 7.0

        email_rate = inp.emails_sent_count / total
        if email_rate < 2.0:
            score += 30.0
        elif email_rate < 5.0:
            score += 15.0

        if inp.avg_email_response_time_minutes >= 1440.0:
            score += 25.0
        elif inp.avg_email_response_time_minutes >= 480.0:
            score += 12.0

        return min(score, 100.0)

    def _time_discipline_score(self, inp: TimeAllocationInput) -> float:
        score = 0.0

        if inp.focus_blocks_per_week < 2.0:
            score += 35.0
        elif inp.focus_blocks_per_week < 5.0:
            score += 18.0
        elif inp.focus_blocks_per_week < 8.0:
            score += 7.0

        if inp.after_hours_work_hours >= 10.0:
            score += 30.0
        elif inp.after_hours_work_hours >= 5.0:
            score += 15.0

        if inp.pipeline_review_hours < 1.0:
            score += 20.0
        elif inp.pipeline_review_hours < 2.0:
            score += 10.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: TimeAllocationInput,
                         selling: float, admin: float,
                         quality: float, discipline: float) -> AllocationPattern:
        total = max(inp.total_hours_tracked, 1.0)
        admin_pct = (inp.admin_hours + inp.travel_hours) / total
        if admin >= 35 and admin_pct >= 0.25:
            return AllocationPattern.admin_overload

        internal_pct = inp.internal_meeting_hours / total
        if admin >= 30 and internal_pct >= 0.20:
            return AllocationPattern.meeting_fatigue

        selling_pct = (inp.customer_facing_hours + inp.proposal_prep_hours) / total
        if selling >= 35 and selling_pct < 0.25:
            return AllocationPattern.low_selling_time

        if quality >= 30 and inp.avg_email_response_time_minutes >= 480.0:
            return AllocationPattern.reactive_mode

        if discipline >= 30 and inp.focus_blocks_per_week < 3.0:
            return AllocationPattern.time_fragmentation

        return AllocationPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> AllocationRisk:
        if composite >= 60:
            return AllocationRisk.critical
        if composite >= 40:
            return AllocationRisk.high
        if composite >= 20:
            return AllocationRisk.moderate
        return AllocationRisk.low

    def _severity(self, composite: float) -> AllocationSeverity:
        if composite >= 60:
            return AllocationSeverity.fragmented
        if composite >= 40:
            return AllocationSeverity.burdened
        if composite >= 20:
            return AllocationSeverity.developing
        return AllocationSeverity.optimized

    def _action(self, risk: AllocationRisk,
                 pattern: AllocationPattern) -> AllocationAction:
        if risk == AllocationRisk.critical:
            if pattern == AllocationPattern.admin_overload:
                return AllocationAction.admin_reduction_plan
            if pattern == AllocationPattern.low_selling_time:
                return AllocationAction.selling_time_recovery
            return AllocationAction.workflow_optimization
        if risk == AllocationRisk.high:
            if pattern == AllocationPattern.meeting_fatigue:
                return AllocationAction.meeting_hygiene_review
            if pattern == AllocationPattern.time_fragmentation:
                return AllocationAction.time_audit_coaching
            return AllocationAction.selling_time_recovery
        if risk == AllocationRisk.moderate:
            return AllocationAction.time_audit_coaching
        return AllocationAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_time_gap(self, composite: float,
                       inp: TimeAllocationInput) -> bool:
        total = max(inp.total_hours_tracked, 1.0)
        selling_pct = (inp.customer_facing_hours + inp.proposal_prep_hours) / total
        admin_pct = (inp.admin_hours + inp.travel_hours) / total
        return (
            composite >= 40
            or selling_pct < 0.15
            or admin_pct >= 0.35
        )

    def _requires_allocation_coaching(self, composite: float,
                                       inp: TimeAllocationInput) -> bool:
        total = max(inp.total_hours_tracked, 1.0)
        selling_pct = (inp.customer_facing_hours + inp.proposal_prep_hours) / total
        internal_pct = inp.internal_meeting_hours / total
        return (
            composite >= 30
            or selling_pct < 0.20
            or internal_pct >= 0.25
        )

    # ------------------------------------------------------------------
    # Hours lost
    # ------------------------------------------------------------------

    def _estimated_selling_hours_lost(self, inp: TimeAllocationInput,
                                       composite: float) -> float:
        total = max(inp.total_hours_tracked, 1.0)
        selling_pct = (inp.customer_facing_hours + inp.proposal_prep_hours) / total
        gap = max(0.0, 0.40 - selling_pct)
        return round(gap * total / 4.0 * composite / 100.0, 2)

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: TimeAllocationInput,
                 pattern: AllocationPattern, composite: float) -> str:
        if pattern == AllocationPattern.none and composite < 20:
            return "Time allocation and selling productivity within healthy benchmarks"
        total = max(inp.total_hours_tracked, 1.0)
        selling_pct = (inp.customer_facing_hours + inp.proposal_prep_hours) / total
        admin_pct = (inp.admin_hours + inp.travel_hours) / total
        parts: list[str] = []
        if selling_pct < 0.30:
            parts.append(f"{inp.customer_facing_hours:.0f}h customer-facing")
        if admin_pct >= 0.15:
            parts.append(f"{inp.admin_hours:.0f}h admin")
        if inp.internal_meeting_hours >= 5.0:
            parts.append(f"{inp.internal_meeting_hours:.0f}h internal meetings")
        label = pattern.value.replace("_", " ") if pattern != AllocationPattern.none else "Allocation risk"
        summary = " — ".join(parts) if parts else "selling time below target"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: TimeAllocationInput) -> TimeAllocationResult:
        selling    = round(self._selling_time_score(inp), 1)
        admin      = round(self._admin_burden_score(inp), 1)
        quality    = round(self._activity_quality_score(inp), 1)
        discipline = round(self._time_discipline_score(inp), 1)

        composite = round(
            selling * 0.35 + admin * 0.30 + quality * 0.20 + discipline * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, selling, admin, quality, discipline)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap      = self._has_time_gap(composite, inp)
        coaching = self._requires_allocation_coaching(composite, inp)
        lost     = self._estimated_selling_hours_lost(inp, composite)
        signal   = self._signal(inp, pattern, composite)

        result = TimeAllocationResult(
            rep_id=inp.rep_id,
            region=inp.region,
            allocation_risk=risk,
            allocation_pattern=pattern,
            allocation_severity=severity,
            recommended_action=action,
            selling_time_score=selling,
            admin_burden_score=admin,
            activity_quality_score=quality,
            time_discipline_score=discipline,
            time_allocation_composite=composite,
            has_time_gap=gap,
            requires_allocation_coaching=coaching,
            estimated_selling_hours_lost_per_week=lost,
            allocation_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[TimeAllocationInput]) -> list[TimeAllocationResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_time_allocation_composite": 0.0,
                "time_gap_count": 0,
                "allocation_coaching_count": 0,
                "avg_selling_time_score": 0.0,
                "avg_admin_burden_score": 0.0,
                "avg_activity_quality_score": 0.0,
                "avg_time_discipline_score": 0.0,
                "total_estimated_selling_hours_lost_per_week": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_sel = total_adm = total_qua = total_dis = total_lost = 0.0

        for r in self._results:
            risk_counts[r.allocation_risk.value]       = risk_counts.get(r.allocation_risk.value, 0) + 1
            pattern_counts[r.allocation_pattern.value] = pattern_counts.get(r.allocation_pattern.value, 0) + 1
            severity_counts[r.allocation_severity.value] = severity_counts.get(r.allocation_severity.value, 0) + 1
            action_counts[r.recommended_action.value]    = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.time_allocation_composite
            total_sel  += r.selling_time_score
            total_adm  += r.admin_burden_score
            total_qua  += r.activity_quality_score
            total_dis  += r.time_discipline_score
            total_lost += r.estimated_selling_hours_lost_per_week

        n = len(self._results)

        return {
            "total":                                        n,
            "risk_counts":                                  risk_counts,
            "pattern_counts":                               pattern_counts,
            "severity_counts":                              severity_counts,
            "action_counts":                                action_counts,
            "avg_time_allocation_composite":                round(total_comp / n, 1),
            "time_gap_count":                               sum(1 for r in self._results if r.has_time_gap),
            "allocation_coaching_count":                    sum(1 for r in self._results if r.requires_allocation_coaching),
            "avg_selling_time_score":                       round(total_sel / n, 1),
            "avg_admin_burden_score":                       round(total_adm / n, 1),
            "avg_activity_quality_score":                   round(total_qua / n, 1),
            "avg_time_discipline_score":                    round(total_dis / n, 1),
            "total_estimated_selling_hours_lost_per_week":  round(total_lost, 2),
        }
