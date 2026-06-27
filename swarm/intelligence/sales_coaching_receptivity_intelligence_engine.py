from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class CoachRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class CoachPattern(str, Enum):
    none               = "none"
    passive_resistor   = "passive_resistor"
    active_deflector   = "active_deflector"
    habit_reverter     = "habit_reverter"
    selective_listener = "selective_listener"
    ghost_committor    = "ghost_committor"


class CoachSeverity(str, Enum):
    receptive    = "receptive"
    developing   = "developing"
    resistant    = "resistant"
    unreachable  = "unreachable"


class CoachAction(str, Enum):
    no_action                        = "no_action"
    coaching_check_in                = "coaching_check_in"
    structured_feedback_plan         = "structured_feedback_plan"
    behavioral_change_coaching       = "behavioral_change_coaching"
    manager_escalation               = "manager_escalation"
    performance_improvement_plan     = "performance_improvement_plan"
    leadership_intervention          = "leadership_intervention"


@dataclass
class CoachInput:
    rep_id:                          str
    region:                          str
    evaluation_period_id:            str
    feedback_implementation_rate_pct: float  # 0-1
    skill_improvement_after_coaching: float  # 0-1
    action_item_completion_rate_pct:  float  # 0-1
    sessions_attended_rate_pct:       float  # 0-1
    voluntary_coaching_requests:      int    # count per period
    reversion_rate_pct:               float  # 0-1 (habits reverting after coaching)
    follow_through_score:             float  # 0-1
    peer_learning_engagement_pct:     float  # 0-1
    call_recording_review_rate_pct:   float  # 0-1
    manager_satisfaction_score:       float  # 0-1
    self_assessment_accuracy_pct:     float  # 0-1 (rep vs mgr scoring diff)
    improvement_velocity:             float  # 0-1 (rate of skill gain)
    prior_pip_count:                  int    # count
    coaching_hours_utilized_pct:      float  # 0-1
    multi_modal_engagement_pct:       float  # 0-1 (video/written/role-play)
    challenge_question_rate_pct:      float  # 0-1 (how often pushes back on coach)
    engagement_consistency_pct:       float  # 0-1
    total_coaching_sessions:          int
    avg_session_duration_minutes:     float


@dataclass
class CoachResult:
    rep_id:                          str
    region:                          str
    coach_risk:                      CoachRisk
    coach_pattern:                   CoachPattern
    coach_severity:                  CoachSeverity
    recommended_action:              CoachAction
    receptivity_score:               float
    implementation_score:            float
    engagement_score:                float
    improvement_score:               float
    coach_composite:                 float
    has_coach_gap:                   bool
    requires_coach_intervention:     bool
    estimated_coaching_waste_usd:    float
    coach_signal:                    str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "coach_risk":                       self.coach_risk.value,
            "coach_pattern":                    self.coach_pattern.value,
            "coach_severity":                   self.coach_severity.value,
            "recommended_action":               self.recommended_action.value,
            "receptivity_score":                self.receptivity_score,
            "implementation_score":             self.implementation_score,
            "engagement_score":                 self.engagement_score,
            "improvement_score":                self.improvement_score,
            "coach_composite":                  self.coach_composite,
            "has_coach_gap":                    self.has_coach_gap,
            "requires_coach_intervention":      self.requires_coach_intervention,
            "estimated_coaching_waste_usd":     self.estimated_coaching_waste_usd,
            "coach_signal":                     self.coach_signal,
        }


class SalesCoachingReceptivityIntelligenceEngine:
    """Detects per-rep coaching resistance — passive resistors, active deflectors, habit reverters."""

    def __init__(self) -> None:
        self._results: List[CoachResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────

    def _receptivity_score(self, inp: CoachInput) -> float:
        s = 0.0
        if   inp.sessions_attended_rate_pct      <= 0.50: s += 40
        elif inp.sessions_attended_rate_pct      <= 0.70: s += 22
        elif inp.sessions_attended_rate_pct      <= 0.85: s += 8
        if   inp.challenge_question_rate_pct     >= 0.60: s += 35
        elif inp.challenge_question_rate_pct     >= 0.40: s += 18
        if   inp.manager_satisfaction_score      <= 0.35: s += 25
        elif inp.manager_satisfaction_score      <= 0.55: s += 12
        return min(s, 100.0)

    def _implementation_score(self, inp: CoachInput) -> float:
        s = 0.0
        if   inp.feedback_implementation_rate_pct <= 0.30: s += 40
        elif inp.feedback_implementation_rate_pct <= 0.55: s += 22
        elif inp.feedback_implementation_rate_pct <= 0.75: s += 8
        if   inp.action_item_completion_rate_pct  <= 0.40: s += 35
        elif inp.action_item_completion_rate_pct  <= 0.65: s += 18
        if   inp.reversion_rate_pct               >= 0.50: s += 25
        elif inp.reversion_rate_pct               >= 0.30: s += 12
        return min(s, 100.0)

    def _engagement_score(self, inp: CoachInput) -> float:
        s = 0.0
        if   inp.coaching_hours_utilized_pct     <= 0.40: s += 40
        elif inp.coaching_hours_utilized_pct     <= 0.60: s += 22
        elif inp.coaching_hours_utilized_pct     <= 0.80: s += 8
        if   inp.call_recording_review_rate_pct  <= 0.25: s += 35
        elif inp.call_recording_review_rate_pct  <= 0.50: s += 18
        if   inp.peer_learning_engagement_pct    <= 0.20: s += 25
        elif inp.peer_learning_engagement_pct    <= 0.45: s += 12
        return min(s, 100.0)

    def _improvement_score(self, inp: CoachInput) -> float:
        s = 0.0
        if   inp.skill_improvement_after_coaching <= 0.10: s += 45
        elif inp.skill_improvement_after_coaching <= 0.25: s += 25
        elif inp.skill_improvement_after_coaching <= 0.45: s += 10
        if   inp.improvement_velocity             <= 0.10: s += 30
        elif inp.improvement_velocity             <= 0.25: s += 15
        if   inp.follow_through_score             <= 0.25: s += 25
        elif inp.follow_through_score             <= 0.50: s += 12
        return min(s, 100.0)

    # ── composite ─────────────────────────────────────────────────────────

    def _composite(self, re: float, im: float, en: float, ip: float) -> float:
        return min(round(re * 0.30 + im * 0.30 + en * 0.20 + ip * 0.20, 2), 100.0)

    # ── pattern ───────────────────────────────────────────────────────────

    def _pattern(self, inp: CoachInput) -> CoachPattern:
        if inp.sessions_attended_rate_pct <= 0.55 and inp.manager_satisfaction_score <= 0.40:
            return CoachPattern.passive_resistor
        if inp.challenge_question_rate_pct >= 0.55 and inp.action_item_completion_rate_pct <= 0.45:
            return CoachPattern.active_deflector
        if inp.feedback_implementation_rate_pct >= 0.55 and inp.reversion_rate_pct >= 0.45:
            return CoachPattern.habit_reverter
        if inp.sessions_attended_rate_pct >= 0.80 and inp.skill_improvement_after_coaching <= 0.15:
            return CoachPattern.selective_listener
        if inp.action_item_completion_rate_pct <= 0.30 and inp.follow_through_score <= 0.25:
            return CoachPattern.ghost_committor
        return CoachPattern.none

    # ── thresholds ────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> CoachRisk:
        if   composite >= 60: return CoachRisk.critical
        elif composite >= 40: return CoachRisk.high
        elif composite >= 20: return CoachRisk.moderate
        return CoachRisk.low

    def _severity(self, composite: float) -> CoachSeverity:
        if   composite >= 60: return CoachSeverity.unreachable
        elif composite >= 40: return CoachSeverity.resistant
        elif composite >= 20: return CoachSeverity.developing
        return CoachSeverity.receptive

    def _action(self, risk: CoachRisk, pattern: CoachPattern) -> CoachAction:
        if risk == CoachRisk.critical:
            if pattern in (CoachPattern.passive_resistor, CoachPattern.active_deflector):
                return CoachAction.leadership_intervention
            return CoachAction.performance_improvement_plan
        if risk == CoachRisk.high:
            if pattern == CoachPattern.passive_resistor:
                return CoachAction.manager_escalation
            if pattern == CoachPattern.active_deflector:
                return CoachAction.behavioral_change_coaching
            if pattern == CoachPattern.habit_reverter:
                return CoachAction.structured_feedback_plan
            if pattern == CoachPattern.selective_listener:
                return CoachAction.structured_feedback_plan
            if pattern == CoachPattern.ghost_committor:
                return CoachAction.manager_escalation
            return CoachAction.behavioral_change_coaching
        if risk == CoachRisk.moderate:
            return CoachAction.coaching_check_in
        return CoachAction.no_action

    # ── flags ─────────────────────────────────────────────────────────────

    def _has_gap(self, inp: CoachInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.feedback_implementation_rate_pct <= 0.60
            or inp.action_item_completion_rate_pct  <= 0.55
        )

    def _requires_intervention(self, inp: CoachInput, composite: float) -> bool:
        return (
            composite >= 25
            or inp.reversion_rate_pct                >= 0.30
            or inp.manager_satisfaction_score        <= 0.55
        )

    # ── dollar impact ─────────────────────────────────────────────────────

    def _coaching_waste(self, inp: CoachInput, composite: float) -> float:
        avg_cost_per_session_usd = 500.0
        waste_rate = (composite / 100) * (1 - inp.feedback_implementation_rate_pct)
        return round(inp.total_coaching_sessions * avg_cost_per_session_usd * waste_rate, 2)

    # ── signal ────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        CoachPattern.passive_resistor:   "Passive resistor",
        CoachPattern.active_deflector:   "Active deflector",
        CoachPattern.habit_reverter:     "Habit reverter",
        CoachPattern.selective_listener: "Selective listener",
        CoachPattern.ghost_committor:    "Ghost committor",
    }

    def _signal(self, inp: CoachInput, pattern: CoachPattern, composite: float) -> str:
        if composite < 20:
            return (
                "Coaching receptivity strong — implementation rate, engagement, "
                "action items, and skill improvement within benchmarks"
            )
        label    = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        impl_pct = round(inp.feedback_implementation_rate_pct * 100)
        att_pct  = round(inp.sessions_attended_rate_pct * 100)
        rev_pct  = round(inp.reversion_rate_pct * 100)
        comp_int = round(composite)
        return (
            f"{label} — {impl_pct}% feedback implemented — "
            f"{att_pct}% sessions attended — "
            f"{rev_pct}% habit reversion rate — composite {comp_int}"
        )

    # ── public API ────────────────────────────────────────────────────────

    def assess(self, inp: CoachInput) -> CoachResult:
        re  = self._receptivity_score(inp)
        im  = self._implementation_score(inp)
        en  = self._engagement_score(inp)
        ip  = self._improvement_score(inp)
        comp = self._composite(re, im, en, ip)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = CoachResult(
            rep_id                      = inp.rep_id,
            region                      = inp.region,
            coach_risk                  = risk,
            coach_pattern               = pattern,
            coach_severity              = severity,
            recommended_action          = action,
            receptivity_score           = re,
            implementation_score        = im,
            engagement_score            = en,
            improvement_score           = ip,
            coach_composite             = comp,
            has_coach_gap               = self._has_gap(inp, comp),
            requires_coach_intervention = self._requires_intervention(inp, comp),
            estimated_coaching_waste_usd= self._coaching_waste(inp, comp),
            coach_signal                = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[CoachInput]) -> List[CoachResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_coach_composite": 0.0,
                "coach_gap_count": 0,
                "intervention_count": 0,
                "avg_receptivity_score": 0.0,
                "avg_implementation_score": 0.0,
                "avg_engagement_score": 0.0,
                "avg_improvement_score": 0.0,
                "total_estimated_coaching_waste_usd": 0.0,
            }

        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        total_comp = total_re = total_im = total_en = total_ip = total_cw = 0.0
        gap_count = intervention_count = 0

        for res in self._results:
            risk_counts[res.coach_risk.value]       = risk_counts.get(res.coach_risk.value, 0) + 1
            pattern_counts[res.coach_pattern.value] = pattern_counts.get(res.coach_pattern.value, 0) + 1
            severity_counts[res.coach_severity.value] = severity_counts.get(res.coach_severity.value, 0) + 1
            action_counts[res.recommended_action.value] = action_counts.get(res.recommended_action.value, 0) + 1
            total_comp += res.coach_composite
            total_re   += res.receptivity_score
            total_im   += res.implementation_score
            total_en   += res.engagement_score
            total_ip   += res.improvement_score
            total_cw   += res.estimated_coaching_waste_usd
            if res.has_coach_gap:              gap_count          += 1
            if res.requires_coach_intervention: intervention_count += 1

        n = len(self._results)
        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_coach_composite":                  round(total_comp / n, 1),
            "coach_gap_count":                      gap_count,
            "intervention_count":                   intervention_count,
            "avg_receptivity_score":                round(total_re / n, 1),
            "avg_implementation_score":             round(total_im / n, 1),
            "avg_engagement_score":                 round(total_en / n, 1),
            "avg_improvement_score":                round(total_ip / n, 1),
            "total_estimated_coaching_waste_usd":   round(total_cw, 2),
        }
