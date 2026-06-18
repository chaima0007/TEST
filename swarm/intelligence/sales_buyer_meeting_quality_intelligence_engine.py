from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class MeetingRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class MeetingPattern(str, Enum):
    none                      = "none"
    no_agenda_discipline      = "no_agenda_discipline"
    poor_followup             = "poor_followup"
    single_stakeholder_trap   = "single_stakeholder_trap"
    no_next_step_close        = "no_next_step_close"
    meeting_fatigue           = "meeting_fatigue"


class MeetingSeverity(str, Enum):
    structured  = "structured"
    developing  = "developing"
    ad_hoc      = "ad_hoc"
    chaotic     = "chaotic"


class MeetingAction(str, Enum):
    no_action                          = "no_action"
    meeting_prep_coaching              = "meeting_prep_coaching"
    followup_discipline_training       = "followup_discipline_training"
    stakeholder_expansion_in_meetings  = "stakeholder_expansion_in_meetings"
    next_step_close_training           = "next_step_close_training"
    meeting_cadence_optimization       = "meeting_cadence_optimization"


@dataclass
class MeetingInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    total_meetings_conducted: int
    meetings_with_agenda_sent_pct: float
    avg_agenda_sent_hours_before_meeting: float
    followup_within_24h_rate_pct: float
    avg_followup_delay_hours: float
    meeting_to_next_meeting_conversion_pct: float
    avg_stakeholders_per_meeting: float
    decision_maker_in_meeting_pct: float
    meetings_with_no_outcome_pct: float
    next_step_committed_at_meeting_pct: float
    meetings_rescheduled_by_buyer_pct: float
    avg_meeting_duration_minutes: float
    meeting_recording_review_rate_pct: float
    demo_conversion_from_meeting_pct: float
    proposal_conversion_from_demo_pct: float
    repeat_meeting_same_stage_pct: float
    meeting_cancellation_rate_pct: float
    avg_time_between_meetings_days: float
    avg_opportunity_value_usd: float


@dataclass
class MeetingResult:
    rep_id: str
    region: str
    meeting_risk: MeetingRisk
    meeting_pattern: MeetingPattern
    meeting_severity: MeetingSeverity
    recommended_action: MeetingAction
    meeting_prep_score: float
    meeting_engagement_score: float
    meeting_outcome_score: float
    meeting_conversion_score: float
    meeting_composite: float
    has_meeting_gap: bool
    requires_meeting_coaching: bool
    estimated_pipeline_drag_usd: float
    meeting_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "meeting_risk":                     self.meeting_risk.value,
            "meeting_pattern":                  self.meeting_pattern.value,
            "meeting_severity":                 self.meeting_severity.value,
            "recommended_action":               self.recommended_action.value,
            "meeting_prep_score":               self.meeting_prep_score,
            "meeting_engagement_score":         self.meeting_engagement_score,
            "meeting_outcome_score":            self.meeting_outcome_score,
            "meeting_conversion_score":         self.meeting_conversion_score,
            "meeting_composite":                self.meeting_composite,
            "has_meeting_gap":                  self.has_meeting_gap,
            "requires_meeting_coaching":        self.requires_meeting_coaching,
            "estimated_pipeline_drag_usd":      self.estimated_pipeline_drag_usd,
            "meeting_signal":                   self.meeting_signal,
        }


class SalesBuyerMeetingQualityIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[MeetingResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _meeting_prep_score(self, inp: MeetingInput) -> float:
        score = 0.0

        if inp.meetings_with_agenda_sent_pct <= 0.20:
            score += 40.0
        elif inp.meetings_with_agenda_sent_pct <= 0.50:
            score += 22.0
        elif inp.meetings_with_agenda_sent_pct <= 0.75:
            score += 8.0

        if inp.avg_agenda_sent_hours_before_meeting <= 2.0:
            score += 35.0
        elif inp.avg_agenda_sent_hours_before_meeting <= 12.0:
            score += 18.0

        if inp.meeting_recording_review_rate_pct <= 0.10:
            score += 25.0
        elif inp.meeting_recording_review_rate_pct <= 0.30:
            score += 12.0

        return min(score, 100.0)

    def _meeting_engagement_score(self, inp: MeetingInput) -> float:
        score = 0.0

        if inp.avg_stakeholders_per_meeting <= 1.0:
            score += 40.0
        elif inp.avg_stakeholders_per_meeting <= 1.5:
            score += 22.0
        elif inp.avg_stakeholders_per_meeting <= 2.0:
            score += 8.0

        if inp.decision_maker_in_meeting_pct <= 0.20:
            score += 35.0
        elif inp.decision_maker_in_meeting_pct <= 0.50:
            score += 18.0

        if inp.meeting_cancellation_rate_pct >= 0.35:
            score += 25.0
        elif inp.meeting_cancellation_rate_pct >= 0.20:
            score += 12.0

        return min(score, 100.0)

    def _meeting_outcome_score(self, inp: MeetingInput) -> float:
        score = 0.0

        if inp.next_step_committed_at_meeting_pct <= 0.25:
            score += 40.0
        elif inp.next_step_committed_at_meeting_pct <= 0.55:
            score += 22.0
        elif inp.next_step_committed_at_meeting_pct <= 0.75:
            score += 8.0

        if inp.meetings_with_no_outcome_pct >= 0.50:
            score += 35.0
        elif inp.meetings_with_no_outcome_pct >= 0.25:
            score += 18.0

        if inp.repeat_meeting_same_stage_pct >= 0.50:
            score += 25.0
        elif inp.repeat_meeting_same_stage_pct >= 0.25:
            score += 12.0

        return min(score, 100.0)

    def _meeting_conversion_score(self, inp: MeetingInput) -> float:
        score = 0.0

        if inp.followup_within_24h_rate_pct <= 0.20:
            score += 45.0
        elif inp.followup_within_24h_rate_pct <= 0.50:
            score += 25.0
        elif inp.followup_within_24h_rate_pct <= 0.75:
            score += 10.0

        if inp.demo_conversion_from_meeting_pct <= 0.15:
            score += 30.0
        elif inp.demo_conversion_from_meeting_pct <= 0.35:
            score += 15.0

        if inp.proposal_conversion_from_demo_pct <= 0.25:
            score += 25.0
        elif inp.proposal_conversion_from_demo_pct <= 0.50:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: MeetingInput,
                          prep: float, engagement: float,
                          outcome: float, conversion: float) -> MeetingPattern:
        if prep >= 40 and inp.meetings_with_agenda_sent_pct <= 0.30:
            return MeetingPattern.no_agenda_discipline

        if conversion >= 30 and inp.followup_within_24h_rate_pct <= 0.30:
            return MeetingPattern.poor_followup

        if engagement >= 30 and inp.avg_stakeholders_per_meeting <= 1.2:
            return MeetingPattern.single_stakeholder_trap

        if outcome >= 40 and inp.next_step_committed_at_meeting_pct <= 0.30:
            return MeetingPattern.no_next_step_close

        if engagement >= 30 and inp.meeting_cancellation_rate_pct >= 0.30:
            return MeetingPattern.meeting_fatigue

        return MeetingPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> MeetingRisk:
        if composite >= 60:
            return MeetingRisk.critical
        if composite >= 40:
            return MeetingRisk.high
        if composite >= 20:
            return MeetingRisk.moderate
        return MeetingRisk.low

    def _severity(self, composite: float) -> MeetingSeverity:
        if composite >= 60:
            return MeetingSeverity.chaotic
        if composite >= 40:
            return MeetingSeverity.ad_hoc
        if composite >= 20:
            return MeetingSeverity.developing
        return MeetingSeverity.structured

    def _action(self, risk: MeetingRisk, pattern: MeetingPattern) -> MeetingAction:
        if risk == MeetingRisk.critical:
            if pattern == MeetingPattern.no_next_step_close:
                return MeetingAction.next_step_close_training
            if pattern == MeetingPattern.single_stakeholder_trap:
                return MeetingAction.stakeholder_expansion_in_meetings
            return MeetingAction.meeting_prep_coaching
        if risk == MeetingRisk.high:
            if pattern == MeetingPattern.poor_followup:
                return MeetingAction.followup_discipline_training
            if pattern == MeetingPattern.meeting_fatigue:
                return MeetingAction.meeting_cadence_optimization
            return MeetingAction.meeting_prep_coaching
        if risk == MeetingRisk.moderate:
            return MeetingAction.meeting_prep_coaching
        return MeetingAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_meeting_gap(self, composite: float, inp: MeetingInput) -> bool:
        return (
            composite >= 40
            or inp.meetings_with_no_outcome_pct >= 0.40
            or inp.next_step_committed_at_meeting_pct <= 0.25
        )

    def _requires_meeting_coaching(self, composite: float, inp: MeetingInput) -> bool:
        return (
            composite >= 30
            or inp.meetings_with_agenda_sent_pct <= 0.40
            or inp.followup_within_24h_rate_pct <= 0.40
        )

    # ------------------------------------------------------------------
    # Pipeline drag estimate
    # ------------------------------------------------------------------

    def _estimated_pipeline_drag(self, inp: MeetingInput, composite: float) -> float:
        no_outcome_meetings = round(inp.total_meetings_conducted * inp.meetings_with_no_outcome_pct)
        return round(no_outcome_meetings * inp.avg_opportunity_value_usd * (composite / 100.0) * 0.20, 2)

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: MeetingInput, pattern: MeetingPattern, composite: float) -> str:
        if pattern == MeetingPattern.none and composite < 20:
            return "Meeting quality healthy — preparation, stakeholder engagement, and next-step discipline within benchmarks"
        parts: list[str] = []
        if inp.meetings_with_agenda_sent_pct < 1.0:
            parts.append(f"{inp.meetings_with_agenda_sent_pct*100:.0f}% meetings with agenda")
        if inp.next_step_committed_at_meeting_pct < 1.0:
            parts.append(f"{inp.next_step_committed_at_meeting_pct*100:.0f}% next-step committed")
        parts.append(f"{inp.avg_stakeholders_per_meeting:.1f} avg stakeholders")
        label = pattern.value.replace("_", " ") if pattern != MeetingPattern.none else "Meeting quality risk"
        summary = " — ".join(parts) if parts else "meeting quality gap"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: MeetingInput) -> MeetingResult:
        prep        = round(self._meeting_prep_score(inp), 1)
        engagement  = round(self._meeting_engagement_score(inp), 1)
        outcome     = round(self._meeting_outcome_score(inp), 1)
        conversion  = round(self._meeting_conversion_score(inp), 1)

        composite = round(
            prep * 0.25 + engagement * 0.30 + outcome * 0.30 + conversion * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, prep, engagement, outcome, conversion)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap    = self._has_meeting_gap(composite, inp)
        coach  = self._requires_meeting_coaching(composite, inp)
        drag   = self._estimated_pipeline_drag(inp, composite)
        signal = self._signal(inp, pattern, composite)

        result = MeetingResult(
            rep_id=inp.rep_id,
            region=inp.region,
            meeting_risk=risk,
            meeting_pattern=pattern,
            meeting_severity=severity,
            recommended_action=action,
            meeting_prep_score=prep,
            meeting_engagement_score=engagement,
            meeting_outcome_score=outcome,
            meeting_conversion_score=conversion,
            meeting_composite=composite,
            has_meeting_gap=gap,
            requires_meeting_coaching=coach,
            estimated_pipeline_drag_usd=drag,
            meeting_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[MeetingInput]) -> list[MeetingResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_meeting_composite": 0.0,
                "meeting_gap_count": 0,
                "coaching_count": 0,
                "avg_meeting_prep_score": 0.0,
                "avg_meeting_engagement_score": 0.0,
                "avg_meeting_outcome_score": 0.0,
                "avg_meeting_conversion_score": 0.0,
                "total_estimated_pipeline_drag_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_pre = total_eng = total_out = total_cvt = total_drag = 0.0

        for r in self._results:
            risk_counts[r.meeting_risk.value]       = risk_counts.get(r.meeting_risk.value, 0) + 1
            pattern_counts[r.meeting_pattern.value] = pattern_counts.get(r.meeting_pattern.value, 0) + 1
            severity_counts[r.meeting_severity.value] = severity_counts.get(r.meeting_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.meeting_composite
            total_pre  += r.meeting_prep_score
            total_eng  += r.meeting_engagement_score
            total_out  += r.meeting_outcome_score
            total_cvt  += r.meeting_conversion_score
            total_drag += r.estimated_pipeline_drag_usd

        n = len(self._results)

        return {
            "total":                                    n,
            "risk_counts":                              risk_counts,
            "pattern_counts":                           pattern_counts,
            "severity_counts":                          severity_counts,
            "action_counts":                            action_counts,
            "avg_meeting_composite":                    round(total_comp / n, 1),
            "meeting_gap_count":                        sum(1 for r in self._results if r.has_meeting_gap),
            "coaching_count":                           sum(1 for r in self._results if r.requires_meeting_coaching),
            "avg_meeting_prep_score":                   round(total_pre / n, 1),
            "avg_meeting_engagement_score":             round(total_eng / n, 1),
            "avg_meeting_outcome_score":                round(total_out / n, 1),
            "avg_meeting_conversion_score":             round(total_cvt / n, 1),
            "total_estimated_pipeline_drag_usd":        round(total_drag, 2),
        }
