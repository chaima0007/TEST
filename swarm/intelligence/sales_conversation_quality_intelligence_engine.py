from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class ConversationRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ConversationPattern(str, Enum):
    none                     = "none"
    monologue_tendency        = "monologue_tendency"
    shallow_discovery         = "shallow_discovery"
    poor_objection_handling   = "poor_objection_handling"
    no_next_step_discipline   = "no_next_step_discipline"
    low_engagement_calls      = "low_engagement_calls"


class ConversationSeverity(str, Enum):
    sharp       = "sharp"
    developing  = "developing"
    weak        = "weak"
    failing     = "failing"


class ConversationAction(str, Enum):
    no_action                   = "no_action"
    call_coaching_session       = "call_coaching_session"
    discovery_skills_training   = "discovery_skills_training"
    objection_handling_workshop = "objection_handling_workshop"
    next_step_discipline_review = "next_step_discipline_review"
    call_recording_audit        = "call_recording_audit"


@dataclass
class ConversationQualityInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    total_calls_analyzed: int
    avg_talk_listen_ratio: float
    avg_questions_per_call: float
    discovery_questions_pct: float
    avg_call_duration_minutes: float
    calls_with_next_step_pct: float
    avg_days_to_next_step: float
    objection_raised_count: int
    objection_handled_successfully_count: int
    filler_words_per_minute: float
    interruptions_per_call: float
    avg_prospect_talk_time_pct: float
    closing_attempt_rate_pct: float
    calls_with_decision_maker_pct: float
    pain_identified_calls_pct: float
    budget_discussed_calls_pct: float
    multi_thread_calls_pct: float
    call_recording_compliance_pct: float
    avg_opportunity_value_usd: float


@dataclass
class ConversationQualityResult:
    rep_id: str
    region: str
    conversation_risk: ConversationRisk
    conversation_pattern: ConversationPattern
    conversation_severity: ConversationSeverity
    recommended_action: ConversationAction
    engagement_quality_score: float
    discovery_depth_score: float
    objection_handling_score: float
    next_step_discipline_score: float
    conversation_composite: float
    has_conversation_gap: bool
    requires_call_coaching: bool
    estimated_revenue_impact_usd: float
    conversation_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                       self.rep_id,
            "region":                       self.region,
            "conversation_risk":            self.conversation_risk.value,
            "conversation_pattern":         self.conversation_pattern.value,
            "conversation_severity":        self.conversation_severity.value,
            "recommended_action":           self.recommended_action.value,
            "engagement_quality_score":     self.engagement_quality_score,
            "discovery_depth_score":        self.discovery_depth_score,
            "objection_handling_score":     self.objection_handling_score,
            "next_step_discipline_score":   self.next_step_discipline_score,
            "conversation_composite":       self.conversation_composite,
            "has_conversation_gap":         self.has_conversation_gap,
            "requires_call_coaching":       self.requires_call_coaching,
            "estimated_revenue_impact_usd": self.estimated_revenue_impact_usd,
            "conversation_signal":          self.conversation_signal,
        }


class SalesConversationQualityIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[ConversationQualityResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _engagement_quality_score(self, inp: ConversationQualityInput) -> float:
        score = 0.0

        if inp.avg_talk_listen_ratio >= 2.5:
            score += 40.0
        elif inp.avg_talk_listen_ratio >= 2.0:
            score += 22.0
        elif inp.avg_talk_listen_ratio >= 1.5:
            score += 8.0

        if inp.avg_prospect_talk_time_pct < 0.30:
            score += 30.0
        elif inp.avg_prospect_talk_time_pct < 0.40:
            score += 15.0

        if inp.filler_words_per_minute >= 5.0:
            score += 20.0
        elif inp.filler_words_per_minute >= 3.0:
            score += 10.0

        return min(score, 100.0)

    def _discovery_depth_score(self, inp: ConversationQualityInput) -> float:
        score = 0.0

        if inp.avg_questions_per_call < 3.0:
            score += 35.0
        elif inp.avg_questions_per_call < 5.0:
            score += 18.0
        elif inp.avg_questions_per_call < 7.0:
            score += 7.0

        if inp.pain_identified_calls_pct < 0.30:
            score += 30.0
        elif inp.pain_identified_calls_pct < 0.50:
            score += 15.0

        if inp.budget_discussed_calls_pct < 0.20:
            score += 25.0
        elif inp.budget_discussed_calls_pct < 0.40:
            score += 12.0

        return min(score, 100.0)

    def _objection_handling_score(self, inp: ConversationQualityInput) -> float:
        score = 0.0

        total_objections = max(inp.objection_raised_count, 1)
        handle_rate = inp.objection_handled_successfully_count / total_objections
        if handle_rate < 0.30:
            score += 45.0
        elif handle_rate < 0.50:
            score += 25.0
        elif handle_rate < 0.70:
            score += 10.0

        if inp.interruptions_per_call >= 5.0:
            score += 30.0
        elif inp.interruptions_per_call >= 3.0:
            score += 15.0

        if inp.calls_with_decision_maker_pct < 0.20:
            score += 20.0
        elif inp.calls_with_decision_maker_pct < 0.40:
            score += 10.0

        return min(score, 100.0)

    def _next_step_discipline_score(self, inp: ConversationQualityInput) -> float:
        score = 0.0

        if inp.calls_with_next_step_pct < 0.40:
            score += 40.0
        elif inp.calls_with_next_step_pct < 0.60:
            score += 22.0
        elif inp.calls_with_next_step_pct < 0.80:
            score += 8.0

        if inp.avg_days_to_next_step >= 10.0:
            score += 35.0
        elif inp.avg_days_to_next_step >= 7.0:
            score += 18.0
        elif inp.avg_days_to_next_step >= 4.0:
            score += 7.0

        if inp.call_recording_compliance_pct < 0.50:
            score += 20.0
        elif inp.call_recording_compliance_pct < 0.70:
            score += 10.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: ConversationQualityInput,
                          engagement: float, discovery: float,
                          objection: float, next_step: float) -> ConversationPattern:
        if engagement >= 35 and inp.avg_talk_listen_ratio >= 2.0:
            return ConversationPattern.monologue_tendency

        if next_step >= 35 and inp.calls_with_next_step_pct < 0.50:
            return ConversationPattern.no_next_step_discipline

        total_objections = max(inp.objection_raised_count, 1)
        handle_rate = inp.objection_handled_successfully_count / total_objections
        if objection >= 30 and handle_rate < 0.50:
            return ConversationPattern.poor_objection_handling

        if discovery >= 30 and inp.pain_identified_calls_pct < 0.40:
            return ConversationPattern.shallow_discovery

        if engagement >= 20 and inp.avg_prospect_talk_time_pct < 0.35:
            return ConversationPattern.low_engagement_calls

        return ConversationPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> ConversationRisk:
        if composite >= 60:
            return ConversationRisk.critical
        if composite >= 40:
            return ConversationRisk.high
        if composite >= 20:
            return ConversationRisk.moderate
        return ConversationRisk.low

    def _severity(self, composite: float) -> ConversationSeverity:
        if composite >= 60:
            return ConversationSeverity.failing
        if composite >= 40:
            return ConversationSeverity.weak
        if composite >= 20:
            return ConversationSeverity.developing
        return ConversationSeverity.sharp

    def _action(self, risk: ConversationRisk, pattern: ConversationPattern) -> ConversationAction:
        if risk == ConversationRisk.critical:
            if pattern == ConversationPattern.poor_objection_handling:
                return ConversationAction.objection_handling_workshop
            if pattern == ConversationPattern.shallow_discovery:
                return ConversationAction.discovery_skills_training
            return ConversationAction.call_recording_audit
        if risk == ConversationRisk.high:
            if pattern == ConversationPattern.monologue_tendency:
                return ConversationAction.call_coaching_session
            if pattern == ConversationPattern.no_next_step_discipline:
                return ConversationAction.next_step_discipline_review
            return ConversationAction.call_coaching_session
        if risk == ConversationRisk.moderate:
            return ConversationAction.call_coaching_session
        return ConversationAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_conversation_gap(self, composite: float,
                               inp: ConversationQualityInput) -> bool:
        return (
            composite >= 40
            or inp.calls_with_next_step_pct < 0.40
            or inp.avg_talk_listen_ratio >= 2.5
        )

    def _requires_call_coaching(self, composite: float,
                                  inp: ConversationQualityInput) -> bool:
        total_objections = max(inp.objection_raised_count, 1)
        handle_rate = inp.objection_handled_successfully_count / total_objections
        return (
            composite >= 30
            or handle_rate < 0.50
            or inp.pain_identified_calls_pct < 0.30
        )

    # ------------------------------------------------------------------
    # Revenue impact
    # ------------------------------------------------------------------

    def _estimated_revenue_impact(self, inp: ConversationQualityInput,
                                   composite: float) -> float:
        low_engagement_calls = round(inp.total_calls_analyzed * (composite / 100.0))
        conversion_loss_factor = composite / 100.0
        return round(low_engagement_calls * inp.avg_opportunity_value_usd * conversion_loss_factor * 0.15, 2)

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: ConversationQualityInput,
                 pattern: ConversationPattern, composite: float) -> str:
        if pattern == ConversationPattern.none and composite < 20:
            return "Conversation quality healthy — discovery, objection handling, and next steps within benchmarks"
        parts: list[str] = []
        if inp.avg_talk_listen_ratio >= 1.5:
            parts.append(f"{inp.avg_talk_listen_ratio:.1f}x talk/listen ratio")
        if inp.calls_with_next_step_pct < 1.0:
            parts.append(f"{inp.calls_with_next_step_pct*100:.0f}% calls with next step")
        if inp.pain_identified_calls_pct < 1.0:
            parts.append(f"{inp.pain_identified_calls_pct*100:.0f}% pain identified")
        label = pattern.value.replace("_", " ") if pattern != ConversationPattern.none else "Conversation risk"
        summary = " — ".join(parts) if parts else "call quality declining"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: ConversationQualityInput) -> ConversationQualityResult:
        engagement  = round(self._engagement_quality_score(inp), 1)
        discovery   = round(self._discovery_depth_score(inp), 1)
        objection   = round(self._objection_handling_score(inp), 1)
        next_step   = round(self._next_step_discipline_score(inp), 1)

        composite = round(
            engagement * 0.30 + discovery * 0.30 + objection * 0.25 + next_step * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, engagement, discovery, objection, next_step)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap     = self._has_conversation_gap(composite, inp)
        coach   = self._requires_call_coaching(composite, inp)
        impact  = self._estimated_revenue_impact(inp, composite)
        signal  = self._signal(inp, pattern, composite)

        result = ConversationQualityResult(
            rep_id=inp.rep_id,
            region=inp.region,
            conversation_risk=risk,
            conversation_pattern=pattern,
            conversation_severity=severity,
            recommended_action=action,
            engagement_quality_score=engagement,
            discovery_depth_score=discovery,
            objection_handling_score=objection,
            next_step_discipline_score=next_step,
            conversation_composite=composite,
            has_conversation_gap=gap,
            requires_call_coaching=coach,
            estimated_revenue_impact_usd=impact,
            conversation_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[ConversationQualityInput]) -> list[ConversationQualityResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_conversation_composite": 0.0,
                "conversation_gap_count": 0,
                "coaching_count": 0,
                "avg_engagement_quality_score": 0.0,
                "avg_discovery_depth_score": 0.0,
                "avg_objection_handling_score": 0.0,
                "avg_next_step_discipline_score": 0.0,
                "total_estimated_revenue_impact_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_eng = total_disc = total_obj = total_nxt = total_impact = 0.0

        for r in self._results:
            risk_counts[r.conversation_risk.value]       = risk_counts.get(r.conversation_risk.value, 0) + 1
            pattern_counts[r.conversation_pattern.value] = pattern_counts.get(r.conversation_pattern.value, 0) + 1
            severity_counts[r.conversation_severity.value] = severity_counts.get(r.conversation_severity.value, 0) + 1
            action_counts[r.recommended_action.value]    = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp   += r.conversation_composite
            total_eng    += r.engagement_quality_score
            total_disc   += r.discovery_depth_score
            total_obj    += r.objection_handling_score
            total_nxt    += r.next_step_discipline_score
            total_impact += r.estimated_revenue_impact_usd

        n = len(self._results)

        return {
            "total":                                    n,
            "risk_counts":                              risk_counts,
            "pattern_counts":                           pattern_counts,
            "severity_counts":                          severity_counts,
            "action_counts":                            action_counts,
            "avg_conversation_composite":               round(total_comp / n, 1),
            "conversation_gap_count":                   sum(1 for r in self._results if r.has_conversation_gap),
            "coaching_count":                           sum(1 for r in self._results if r.requires_call_coaching),
            "avg_engagement_quality_score":             round(total_eng / n, 1),
            "avg_discovery_depth_score":                round(total_disc / n, 1),
            "avg_objection_handling_score":             round(total_obj / n, 1),
            "avg_next_step_discipline_score":           round(total_nxt / n, 1),
            "total_estimated_revenue_impact_usd":       round(total_impact, 2),
        }
