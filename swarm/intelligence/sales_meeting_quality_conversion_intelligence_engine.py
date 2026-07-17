from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class MeetingRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class MeetingPattern(str, Enum):
    none                  = "none"
    calendar_stuffing     = "calendar_stuffing"
    discovery_skipper     = "discovery_skipper"
    next_step_avoider     = "next_step_avoider"
    phantom_meeting_maker = "phantom_meeting_maker"
    demo_looper           = "demo_looper"


class MeetingSeverity(str, Enum):
    converting   = "converting"
    slipping     = "slipping"
    stalling     = "stalling"
    collapsing   = "collapsing"


class MeetingAction(str, Enum):
    no_action                       = "no_action"
    meeting_quality_monitoring      = "meeting_quality_monitoring"
    discovery_coaching              = "discovery_coaching"
    next_step_discipline_coaching   = "next_step_discipline_coaching"
    pipeline_qualification_coaching = "pipeline_qualification_coaching"
    meeting_audit                   = "meeting_audit"
    full_pipeline_reset             = "full_pipeline_reset"


@dataclass
class MeetingInput:
    rep_id:                              str
    region:                              str
    evaluation_period_id:                str
    meetings_to_opportunity_rate_pct:    float  # 0-1 (% meetings creating opps)
    discovery_completion_rate_pct:       float  # 0-1 (% meetings with full discovery)
    next_step_confirmed_rate_pct:        float  # 0-1 (% meetings closing with NS)
    demo_to_proposal_rate_pct:           float  # 0-1
    proposal_to_close_rate_pct:          float  # 0-1
    avg_meeting_duration_minutes:        float
    no_show_rate_pct:                    float  # 0-1
    reschedule_rate_pct:                 float  # 0-1
    multi_stakeholder_meeting_rate_pct:  float  # 0-1
    pain_identified_rate_pct:            float  # 0-1 (% meetings with pain documented)
    budget_confirmed_in_meeting_rate_pct: float  # 0-1
    decision_process_mapped_rate_pct:    float  # 0-1
    meeting_notes_completion_rate_pct:   float  # 0-1
    repeat_meeting_same_stage_rate_pct:  float  # 0-1 (% meetings that repeat without advancing)
    meeting_to_pipeline_velocity_days:   float  # avg days meeting→pipeline stage advance
    champion_identified_meeting_rate_pct: float  # 0-1
    competitive_mentioned_rate_pct:      float  # 0-1 (% meetings where comp discussed)
    executive_access_secured_rate_pct:   float  # 0-1
    total_meetings_held:                 int
    avg_deal_value_usd:                  float


@dataclass
class MeetingResult:
    rep_id:                          str
    region:                          str
    meeting_risk:                    MeetingRisk
    meeting_pattern:                 MeetingPattern
    meeting_severity:                MeetingSeverity
    recommended_action:              MeetingAction
    conversion_score:                float
    quality_score:                   float
    execution_score:                 float
    advancement_score:               float
    meeting_composite:               float
    has_meeting_gap:                 bool
    requires_meeting_coaching:       bool
    estimated_wasted_meeting_usd:    float
    meeting_signal:                  str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "meeting_risk":                     self.meeting_risk.value,
            "meeting_pattern":                  self.meeting_pattern.value,
            "meeting_severity":                 self.meeting_severity.value,
            "recommended_action":               self.recommended_action.value,
            "conversion_score":                 self.conversion_score,
            "quality_score":                    self.quality_score,
            "execution_score":                  self.execution_score,
            "advancement_score":                self.advancement_score,
            "meeting_composite":                self.meeting_composite,
            "has_meeting_gap":                  self.has_meeting_gap,
            "requires_meeting_coaching":        self.requires_meeting_coaching,
            "estimated_wasted_meeting_usd":     self.estimated_wasted_meeting_usd,
            "meeting_signal":                   self.meeting_signal,
        }


class SalesMeetingQualityConversionIntelligenceEngine:
    """Detects meeting-to-pipeline conversion collapse — reps who fill calendars but generate zero opportunities."""

    def __init__(self) -> None:
        self._results: List[MeetingResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────────

    def _conversion_score(self, inp: MeetingInput) -> float:
        s = 0.0
        if   inp.meetings_to_opportunity_rate_pct  <= 0.20: s += 40
        elif inp.meetings_to_opportunity_rate_pct  <= 0.40: s += 22
        elif inp.meetings_to_opportunity_rate_pct  <= 0.60: s += 8
        if   inp.demo_to_proposal_rate_pct         <= 0.25: s += 35
        elif inp.demo_to_proposal_rate_pct         <= 0.50: s += 18
        if   inp.proposal_to_close_rate_pct        <= 0.15: s += 25
        elif inp.proposal_to_close_rate_pct        <= 0.30: s += 12
        return min(s, 100.0)

    def _quality_score(self, inp: MeetingInput) -> float:
        s = 0.0
        if   inp.discovery_completion_rate_pct     <= 0.30: s += 40
        elif inp.discovery_completion_rate_pct     <= 0.55: s += 22
        elif inp.discovery_completion_rate_pct     <= 0.75: s += 8
        if   inp.pain_identified_rate_pct          <= 0.30: s += 35
        elif inp.pain_identified_rate_pct          <= 0.55: s += 18
        if   inp.multi_stakeholder_meeting_rate_pct <= 0.20: s += 25
        elif inp.multi_stakeholder_meeting_rate_pct <= 0.40: s += 12
        return min(s, 100.0)

    def _execution_score(self, inp: MeetingInput) -> float:
        s = 0.0
        if   inp.no_show_rate_pct                  >= 0.30: s += 40
        elif inp.no_show_rate_pct                  >= 0.18: s += 22
        elif inp.no_show_rate_pct                  >= 0.08: s += 8
        if   inp.reschedule_rate_pct               >= 0.40: s += 35
        elif inp.reschedule_rate_pct               >= 0.22: s += 18
        if   inp.meeting_notes_completion_rate_pct <= 0.30: s += 25
        elif inp.meeting_notes_completion_rate_pct <= 0.55: s += 12
        return min(s, 100.0)

    def _advancement_score(self, inp: MeetingInput) -> float:
        s = 0.0
        if   inp.next_step_confirmed_rate_pct      <= 0.30: s += 45
        elif inp.next_step_confirmed_rate_pct      <= 0.55: s += 25
        elif inp.next_step_confirmed_rate_pct      <= 0.75: s += 10
        if   inp.repeat_meeting_same_stage_rate_pct >= 0.45: s += 30
        elif inp.repeat_meeting_same_stage_rate_pct >= 0.25: s += 15
        if   inp.meeting_to_pipeline_velocity_days >= 21: s += 25
        elif inp.meeting_to_pipeline_velocity_days >= 12: s += 12
        return min(s, 100.0)

    # ── composite ─────────────────────────────────────────────────────────────

    def _composite(self, co: float, qu: float, ex: float, ad: float) -> float:
        return min(round(co * 0.30 + qu * 0.25 + ex * 0.20 + ad * 0.25, 2), 100.0)

    # ── pattern ───────────────────────────────────────────────────────────────

    def _pattern(self, inp: MeetingInput) -> MeetingPattern:
        if inp.meetings_to_opportunity_rate_pct <= 0.20 and inp.total_meetings_held >= 15:
            return MeetingPattern.calendar_stuffing
        if inp.discovery_completion_rate_pct <= 0.30 and inp.pain_identified_rate_pct <= 0.35:
            return MeetingPattern.discovery_skipper
        if inp.next_step_confirmed_rate_pct <= 0.25 and inp.repeat_meeting_same_stage_rate_pct >= 0.40:
            return MeetingPattern.next_step_avoider
        if inp.no_show_rate_pct >= 0.25 and inp.reschedule_rate_pct >= 0.30:
            return MeetingPattern.phantom_meeting_maker
        if inp.demo_to_proposal_rate_pct <= 0.20 and inp.repeat_meeting_same_stage_rate_pct >= 0.35:
            return MeetingPattern.demo_looper
        return MeetingPattern.none

    # ── thresholds ────────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> MeetingRisk:
        if   composite >= 60: return MeetingRisk.critical
        elif composite >= 40: return MeetingRisk.high
        elif composite >= 20: return MeetingRisk.moderate
        return MeetingRisk.low

    def _severity(self, composite: float) -> MeetingSeverity:
        if   composite >= 60: return MeetingSeverity.collapsing
        elif composite >= 40: return MeetingSeverity.stalling
        elif composite >= 20: return MeetingSeverity.slipping
        return MeetingSeverity.converting

    def _action(self, risk: MeetingRisk, pattern: MeetingPattern) -> MeetingAction:
        if risk == MeetingRisk.critical:
            if pattern in (MeetingPattern.calendar_stuffing, MeetingPattern.phantom_meeting_maker):
                return MeetingAction.full_pipeline_reset
            return MeetingAction.meeting_audit
        if risk == MeetingRisk.high:
            if pattern == MeetingPattern.calendar_stuffing:
                return MeetingAction.pipeline_qualification_coaching
            if pattern == MeetingPattern.discovery_skipper:
                return MeetingAction.discovery_coaching
            if pattern == MeetingPattern.next_step_avoider:
                return MeetingAction.next_step_discipline_coaching
            if pattern == MeetingPattern.phantom_meeting_maker:
                return MeetingAction.pipeline_qualification_coaching
            if pattern == MeetingPattern.demo_looper:
                return MeetingAction.next_step_discipline_coaching
            return MeetingAction.discovery_coaching
        if risk == MeetingRisk.moderate:
            return MeetingAction.meeting_quality_monitoring
        return MeetingAction.no_action

    # ── flags ─────────────────────────────────────────────────────────────────

    def _has_gap(self, inp: MeetingInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.meetings_to_opportunity_rate_pct <= 0.40
            or inp.next_step_confirmed_rate_pct     <= 0.55
        )

    def _requires_coaching(self, inp: MeetingInput, composite: float) -> bool:
        return (
            composite >= 25
            or inp.discovery_completion_rate_pct    <= 0.55
            or inp.no_show_rate_pct                 >= 0.15
        )

    # ── wasted meeting cost ───────────────────────────────────────────────────

    def _wasted_meeting_cost(self, inp: MeetingInput, composite: float) -> float:
        cost_per_meeting_usd  = 350.0
        waste_rate            = (1.0 - inp.meetings_to_opportunity_rate_pct) * (composite / 100)
        return round(inp.total_meetings_held * cost_per_meeting_usd * waste_rate, 2)

    # ── signal ────────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        MeetingPattern.calendar_stuffing:     "Calendar stuffing",
        MeetingPattern.discovery_skipper:     "Discovery skipper",
        MeetingPattern.next_step_avoider:     "Next-step avoider",
        MeetingPattern.phantom_meeting_maker: "Phantom meeting maker",
        MeetingPattern.demo_looper:           "Demo looper",
    }

    def _signal(self, inp: MeetingInput, pattern: MeetingPattern, composite: float) -> str:
        if composite < 20:
            return (
                "Meeting quality and conversion healthy — discovery completion, "
                "next steps, and opportunity creation within benchmarks"
            )
        label    = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        conv_pct = round(inp.meetings_to_opportunity_rate_pct * 100)
        disc_pct = round(inp.discovery_completion_rate_pct * 100)
        ns_pct   = round(inp.next_step_confirmed_rate_pct * 100)
        comp_int = round(composite)
        return (
            f"{label} — {conv_pct}% meetings→opp — {disc_pct}% discovery complete — "
            f"{ns_pct}% next steps confirmed — composite {comp_int}"
        )

    # ── public API ────────────────────────────────────────────────────────────

    def assess(self, inp: MeetingInput) -> MeetingResult:
        co   = self._conversion_score(inp)
        qu   = self._quality_score(inp)
        ex   = self._execution_score(inp)
        ad   = self._advancement_score(inp)
        comp = self._composite(co, qu, ex, ad)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = MeetingResult(
            rep_id                          = inp.rep_id,
            region                          = inp.region,
            meeting_risk                    = risk,
            meeting_pattern                 = pattern,
            meeting_severity                = severity,
            recommended_action              = action,
            conversion_score                = co,
            quality_score                   = qu,
            execution_score                 = ex,
            advancement_score               = ad,
            meeting_composite               = comp,
            has_meeting_gap                 = self._has_gap(inp, comp),
            requires_meeting_coaching       = self._requires_coaching(inp, comp),
            estimated_wasted_meeting_usd    = self._wasted_meeting_cost(inp, comp),
            meeting_signal                  = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[MeetingInput]) -> List[MeetingResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
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
                "avg_conversion_score": 0.0,
                "avg_quality_score": 0.0,
                "avg_execution_score": 0.0,
                "avg_advancement_score": 0.0,
                "total_estimated_wasted_meeting_usd": 0.0,
            }

        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        total_comp = total_co = total_qu = total_ex = total_ad = total_wm = 0.0
        gap_count = coaching_count = 0

        for res in self._results:
            risk_counts[res.meeting_risk.value]         = risk_counts.get(res.meeting_risk.value, 0) + 1
            pattern_counts[res.meeting_pattern.value]   = pattern_counts.get(res.meeting_pattern.value, 0) + 1
            severity_counts[res.meeting_severity.value] = severity_counts.get(res.meeting_severity.value, 0) + 1
            action_counts[res.recommended_action.value] = action_counts.get(res.recommended_action.value, 0) + 1
            total_comp += res.meeting_composite
            total_co   += res.conversion_score
            total_qu   += res.quality_score
            total_ex   += res.execution_score
            total_ad   += res.advancement_score
            total_wm   += res.estimated_wasted_meeting_usd
            if res.has_meeting_gap:          gap_count      += 1
            if res.requires_meeting_coaching: coaching_count += 1

        n = len(self._results)
        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_meeting_composite":                round(total_comp / n, 1),
            "meeting_gap_count":                    gap_count,
            "coaching_count":                       coaching_count,
            "avg_conversion_score":                 round(total_co / n, 1),
            "avg_quality_score":                    round(total_qu / n, 1),
            "avg_execution_score":                  round(total_ex / n, 1),
            "avg_advancement_score":                round(total_ad / n, 1),
            "total_estimated_wasted_meeting_usd":   round(total_wm, 2),
        }
