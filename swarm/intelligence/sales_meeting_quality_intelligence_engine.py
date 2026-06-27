from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class MeetingRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class MeetingPattern(str, Enum):
    none                  = "none"
    poor_preparation      = "poor_preparation"
    no_deal_advancement   = "no_deal_advancement"
    wrong_stakeholders    = "wrong_stakeholders"
    poor_follow_through   = "poor_follow_through"
    pipeline_stall        = "pipeline_stall"


class MeetingSeverity(str, Enum):
    effective   = "effective"
    developing  = "developing"
    ineffective = "ineffective"
    detrimental = "detrimental"


class MeetingAction(str, Enum):
    no_action                  = "no_action"
    meeting_preparation_coaching = "meeting_preparation_coaching"
    deal_advancement_review    = "deal_advancement_review"
    stakeholder_strategy       = "stakeholder_strategy"
    follow_through_training    = "follow_through_training"
    meeting_cadence_reset      = "meeting_cadence_reset"


@dataclass
class MeetingQualityInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    total_meetings_held: int
    meetings_with_agenda_set: int
    meetings_with_decision_maker: int
    meetings_with_champion_only: int
    meetings_resulting_in_next_step: int
    meetings_with_follow_up_sent_24h: int
    avg_meeting_prep_score: float
    avg_attendees_per_meeting: float
    executive_attendee_rate_pct: float
    demo_meetings_count: int
    demo_to_proposal_conversion_rate_pct: float
    discovery_meetings_count: int
    discovery_to_demo_conversion_rate_pct: float
    meetings_cancelled_by_prospect: int
    meetings_rescheduled_count: int
    avg_deal_stage_advancement_per_meeting: float
    multi_stakeholder_meetings_pct: float
    avg_deal_size_in_meetings_usd: float
    meetings_leading_to_proposal_count: int


@dataclass
class MeetingQualityResult:
    rep_id: str
    region: str
    meeting_risk: MeetingRisk
    meeting_pattern: MeetingPattern
    meeting_severity: MeetingSeverity
    recommended_action: MeetingAction
    meeting_preparation_score: float
    meeting_outcome_score: float
    stakeholder_coverage_score: float
    meeting_discipline_score: float
    meeting_quality_composite: float
    has_meeting_effectiveness_gap: bool
    requires_coaching_intervention: bool
    estimated_revenue_at_risk_usd: float
    meeting_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                         self.rep_id,
            "region":                         self.region,
            "meeting_risk":                   self.meeting_risk.value,
            "meeting_pattern":                self.meeting_pattern.value,
            "meeting_severity":               self.meeting_severity.value,
            "recommended_action":             self.recommended_action.value,
            "meeting_preparation_score":      self.meeting_preparation_score,
            "meeting_outcome_score":          self.meeting_outcome_score,
            "stakeholder_coverage_score":     self.stakeholder_coverage_score,
            "meeting_discipline_score":       self.meeting_discipline_score,
            "meeting_quality_composite":      self.meeting_quality_composite,
            "has_meeting_effectiveness_gap":  self.has_meeting_effectiveness_gap,
            "requires_coaching_intervention": self.requires_coaching_intervention,
            "estimated_revenue_at_risk_usd":  self.estimated_revenue_at_risk_usd,
            "meeting_signal":                 self.meeting_signal,
        }


class SalesMeetingQualityIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[MeetingQualityResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _meeting_preparation_score(self, inp: MeetingQualityInput) -> float:
        score = 0.0
        total = max(inp.total_meetings_held, 1)

        agenda_rate = inp.meetings_with_agenda_set / total
        if agenda_rate < 0.30:
            score += 40.0
        elif agenda_rate < 0.55:
            score += 22.0
        elif agenda_rate < 0.75:
            score += 8.0

        if inp.avg_meeting_prep_score < 3.0:
            score += 35.0
        elif inp.avg_meeting_prep_score < 5.0:
            score += 18.0
        elif inp.avg_meeting_prep_score < 7.0:
            score += 7.0

        if inp.avg_attendees_per_meeting < 1.5:
            score += 15.0
        elif inp.avg_attendees_per_meeting < 2.0:
            score += 7.0

        return min(score, 100.0)

    def _meeting_outcome_score(self, inp: MeetingQualityInput) -> float:
        score = 0.0
        total = max(inp.total_meetings_held, 1)

        next_step_rate = inp.meetings_resulting_in_next_step / total
        if next_step_rate < 0.35:
            score += 40.0
        elif next_step_rate < 0.55:
            score += 22.0
        elif next_step_rate < 0.70:
            score += 8.0

        if inp.avg_deal_stage_advancement_per_meeting < 0.10:
            score += 30.0
        elif inp.avg_deal_stage_advancement_per_meeting < 0.25:
            score += 15.0

        if inp.demo_meetings_count > 0 and inp.demo_to_proposal_conversion_rate_pct < 0.30:
            score += 20.0
        elif inp.demo_meetings_count > 0 and inp.demo_to_proposal_conversion_rate_pct < 0.50:
            score += 10.0

        if inp.discovery_meetings_count > 0 and inp.discovery_to_demo_conversion_rate_pct < 0.40:
            score += 10.0

        return min(score, 100.0)

    def _stakeholder_coverage_score(self, inp: MeetingQualityInput) -> float:
        score = 0.0
        total = max(inp.total_meetings_held, 1)

        dm_rate = inp.meetings_with_decision_maker / total
        if dm_rate < 0.20:
            score += 40.0
        elif dm_rate < 0.40:
            score += 22.0
        elif dm_rate < 0.55:
            score += 8.0

        if inp.executive_attendee_rate_pct < 0.15:
            score += 30.0
        elif inp.executive_attendee_rate_pct < 0.30:
            score += 15.0

        if inp.multi_stakeholder_meetings_pct < 0.25:
            score += 20.0
        elif inp.multi_stakeholder_meetings_pct < 0.45:
            score += 10.0

        champion_only_ratio = inp.meetings_with_champion_only / total
        if champion_only_ratio >= 0.60:
            score += 10.0
        elif champion_only_ratio >= 0.40:
            score += 5.0

        return min(score, 100.0)

    def _meeting_discipline_score(self, inp: MeetingQualityInput) -> float:
        score = 0.0
        total = max(inp.total_meetings_held, 1)

        follow_up_rate = inp.meetings_with_follow_up_sent_24h / total
        if follow_up_rate < 0.30:
            score += 40.0
        elif follow_up_rate < 0.55:
            score += 22.0
        elif follow_up_rate < 0.75:
            score += 8.0

        cancel_rate = inp.meetings_cancelled_by_prospect / total
        if cancel_rate >= 0.30:
            score += 30.0
        elif cancel_rate >= 0.20:
            score += 15.0
        elif cancel_rate >= 0.10:
            score += 8.0

        reschedule_rate = inp.meetings_rescheduled_count / total
        if reschedule_rate >= 0.30:
            score += 20.0
        elif reschedule_rate >= 0.15:
            score += 10.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: MeetingQualityInput,
                          prep: float, outcome: float,
                          stakeholder: float, discipline: float) -> MeetingPattern:
        # Priority: no_deal_advancement > wrong_stakeholders > poor_follow_through
        #           > poor_preparation > pipeline_stall > none
        total = max(inp.total_meetings_held, 1)
        next_step_rate = inp.meetings_resulting_in_next_step / total
        if outcome >= 35 and next_step_rate < 0.40 and inp.avg_deal_stage_advancement_per_meeting < 0.20:
            return MeetingPattern.no_deal_advancement

        dm_rate = inp.meetings_with_decision_maker / total
        if stakeholder >= 35 and dm_rate < 0.30 and inp.executive_attendee_rate_pct < 0.20:
            return MeetingPattern.wrong_stakeholders

        follow_up_rate = inp.meetings_with_follow_up_sent_24h / total
        if discipline >= 35 and follow_up_rate < 0.40:
            return MeetingPattern.poor_follow_through

        agenda_rate = inp.meetings_with_agenda_set / total
        if prep >= 30 and agenda_rate < 0.45:
            return MeetingPattern.poor_preparation

        if inp.demo_meetings_count > 0 and inp.meetings_leading_to_proposal_count == 0:
            return MeetingPattern.pipeline_stall

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
            return MeetingSeverity.detrimental
        if composite >= 40:
            return MeetingSeverity.ineffective
        if composite >= 20:
            return MeetingSeverity.developing
        return MeetingSeverity.effective

    def _action(self, risk: MeetingRisk, pattern: MeetingPattern) -> MeetingAction:
        if risk == MeetingRisk.critical:
            if pattern == MeetingPattern.no_deal_advancement:
                return MeetingAction.deal_advancement_review
            if pattern == MeetingPattern.wrong_stakeholders:
                return MeetingAction.stakeholder_strategy
            return MeetingAction.meeting_cadence_reset
        if risk == MeetingRisk.high:
            if pattern == MeetingPattern.poor_preparation:
                return MeetingAction.meeting_preparation_coaching
            if pattern == MeetingPattern.poor_follow_through:
                return MeetingAction.follow_through_training
            return MeetingAction.deal_advancement_review
        if risk == MeetingRisk.moderate:
            return MeetingAction.meeting_preparation_coaching
        return MeetingAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_meeting_effectiveness_gap(self, composite: float,
                                        inp: MeetingQualityInput) -> bool:
        total = max(inp.total_meetings_held, 1)
        next_step_rate = inp.meetings_resulting_in_next_step / total
        return (
            composite >= 40
            or next_step_rate < 0.40
            or inp.executive_attendee_rate_pct < 0.15
        )

    def _requires_coaching_intervention(self, composite: float,
                                         inp: MeetingQualityInput) -> bool:
        total = max(inp.total_meetings_held, 1)
        agenda_rate = inp.meetings_with_agenda_set / total
        return (
            composite >= 30
            or agenda_rate < 0.40
            or inp.avg_meeting_prep_score < 5.0
        )

    # ------------------------------------------------------------------
    # Revenue at risk
    # ------------------------------------------------------------------

    def _estimated_revenue_at_risk(self, inp: MeetingQualityInput,
                                    composite: float) -> float:
        total = max(inp.total_meetings_held, 1)
        stalled_meetings = total - inp.meetings_resulting_in_next_step
        return round(stalled_meetings * inp.avg_deal_size_in_meetings_usd * (composite / 100.0), 2)

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: MeetingQualityInput,
                 pattern: MeetingPattern, composite: float) -> str:
        if pattern == MeetingPattern.none and composite < 20:
            return "Meeting quality driving strong deal progression"
        parts: list[str] = []
        total = max(inp.total_meetings_held, 1)
        no_next = total - inp.meetings_resulting_in_next_step
        if no_next >= 1:
            parts.append(f"{no_next} meetings without next step")
        no_follow_up = total - inp.meetings_with_follow_up_sent_24h
        if no_follow_up >= 2:
            parts.append(f"{no_follow_up} without 24h follow-up")
        if inp.meetings_cancelled_by_prospect >= 2:
            parts.append(f"{inp.meetings_cancelled_by_prospect} prospect cancellations")
        label = pattern.value.replace("_", " ") if pattern != MeetingPattern.none else "Meeting quality risk"
        summary = " — ".join(parts) if parts else "meeting effectiveness degrading"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: MeetingQualityInput) -> MeetingQualityResult:
        prep        = round(self._meeting_preparation_score(inp), 1)
        outcome     = round(self._meeting_outcome_score(inp), 1)
        stakeholder = round(self._stakeholder_coverage_score(inp), 1)
        discipline  = round(self._meeting_discipline_score(inp), 1)

        composite = round(prep * 0.20 + outcome * 0.35 + stakeholder * 0.25 + discipline * 0.20, 1)
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, prep, outcome, stakeholder, discipline)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap      = self._has_meeting_effectiveness_gap(composite, inp)
        coaching = self._requires_coaching_intervention(composite, inp)
        revenue  = self._estimated_revenue_at_risk(inp, composite)
        signal   = self._signal(inp, pattern, composite)

        result = MeetingQualityResult(
            rep_id=inp.rep_id,
            region=inp.region,
            meeting_risk=risk,
            meeting_pattern=pattern,
            meeting_severity=severity,
            recommended_action=action,
            meeting_preparation_score=prep,
            meeting_outcome_score=outcome,
            stakeholder_coverage_score=stakeholder,
            meeting_discipline_score=discipline,
            meeting_quality_composite=composite,
            has_meeting_effectiveness_gap=gap,
            requires_coaching_intervention=coaching,
            estimated_revenue_at_risk_usd=revenue,
            meeting_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[MeetingQualityInput]) -> list[MeetingQualityResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_meeting_quality_composite": 0.0,
                "effectiveness_gap_count": 0,
                "coaching_intervention_count": 0,
                "avg_meeting_preparation_score": 0.0,
                "avg_meeting_outcome_score": 0.0,
                "avg_stakeholder_coverage_score": 0.0,
                "avg_meeting_discipline_score": 0.0,
                "total_estimated_revenue_at_risk_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_prep = total_out = total_stak = total_disc = total_rev = 0.0

        for r in self._results:
            risk_counts[r.meeting_risk.value]       = risk_counts.get(r.meeting_risk.value, 0) + 1
            pattern_counts[r.meeting_pattern.value] = pattern_counts.get(r.meeting_pattern.value, 0) + 1
            severity_counts[r.meeting_severity.value] = severity_counts.get(r.meeting_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.meeting_quality_composite
            total_prep += r.meeting_preparation_score
            total_out  += r.meeting_outcome_score
            total_stak += r.stakeholder_coverage_score
            total_disc += r.meeting_discipline_score
            total_rev  += r.estimated_revenue_at_risk_usd

        n = len(self._results)

        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_meeting_quality_composite":        round(total_comp / n, 1),
            "effectiveness_gap_count":              sum(1 for r in self._results if r.has_meeting_effectiveness_gap),
            "coaching_intervention_count":          sum(1 for r in self._results if r.requires_coaching_intervention),
            "avg_meeting_preparation_score":        round(total_prep / n, 1),
            "avg_meeting_outcome_score":            round(total_out / n, 1),
            "avg_stakeholder_coverage_score":       round(total_stak / n, 1),
            "avg_meeting_discipline_score":         round(total_disc / n, 1),
            "total_estimated_revenue_at_risk_usd":  round(total_rev, 2),
        }
