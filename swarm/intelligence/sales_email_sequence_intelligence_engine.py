from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class EmailSequenceRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class EmailSequencePattern(str, Enum):
    none                = "none"
    low_open_rate       = "low_open_rate"
    poor_personalization = "poor_personalization"
    email_fatigue       = "email_fatigue"
    timing_failure      = "timing_failure"
    template_overuse    = "template_overuse"


class EmailSequenceSeverity(str, Enum):
    strong      = "strong"
    developing  = "developing"
    weak        = "weak"
    failing     = "failing"


class EmailSequenceAction(str, Enum):
    no_action                    = "no_action"
    sequence_optimization        = "sequence_optimization"
    personalization_coaching     = "personalization_coaching"
    timing_recalibration         = "timing_recalibration"
    template_refresh             = "template_refresh"
    email_fatigue_intervention   = "email_fatigue_intervention"


@dataclass
class EmailSequenceInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    total_sequences_active: int
    avg_email_open_rate_pct: float
    avg_email_reply_rate_pct: float
    avg_click_through_rate_pct: float
    avg_bounce_rate_pct: float
    avg_unsubscribe_rate_pct: float
    avg_follow_up_attempts_per_prospect: float
    avg_days_between_touchpoints: float
    sequences_with_no_reply_pct: float
    avg_subject_line_length_chars: float
    avg_email_word_count: float
    personalization_rate_pct: float
    calls_to_action_per_email_avg: float
    avg_send_time_score: float
    template_vs_custom_ratio: float
    multi_touch_response_rate_pct: float
    prospect_meeting_booked_from_sequence_pct: float
    email_to_meeting_conversion_pct: float
    avg_opportunity_value_usd: float


@dataclass
class EmailSequenceResult:
    rep_id: str
    region: str
    email_sequence_risk: EmailSequenceRisk
    email_sequence_pattern: EmailSequencePattern
    email_sequence_severity: EmailSequenceSeverity
    recommended_action: EmailSequenceAction
    engagement_decay_score: float
    sequence_quality_score: float
    timing_optimization_score: float
    conversion_effectiveness_score: float
    email_sequence_composite: float
    has_sequence_gap: bool
    requires_sequence_coaching: bool
    estimated_pipeline_impact_usd: float
    email_sequence_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "email_sequence_risk":              self.email_sequence_risk.value,
            "email_sequence_pattern":           self.email_sequence_pattern.value,
            "email_sequence_severity":          self.email_sequence_severity.value,
            "recommended_action":               self.recommended_action.value,
            "engagement_decay_score":           self.engagement_decay_score,
            "sequence_quality_score":           self.sequence_quality_score,
            "timing_optimization_score":        self.timing_optimization_score,
            "conversion_effectiveness_score":   self.conversion_effectiveness_score,
            "email_sequence_composite":         self.email_sequence_composite,
            "has_sequence_gap":                 self.has_sequence_gap,
            "requires_sequence_coaching":       self.requires_sequence_coaching,
            "estimated_pipeline_impact_usd":    self.estimated_pipeline_impact_usd,
            "email_sequence_signal":            self.email_sequence_signal,
        }


class SalesEmailSequenceIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[EmailSequenceResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _engagement_decay_score(self, inp: EmailSequenceInput) -> float:
        score = 0.0

        if inp.avg_email_open_rate_pct < 0.15:
            score += 40.0
        elif inp.avg_email_open_rate_pct < 0.25:
            score += 20.0
        elif inp.avg_email_open_rate_pct < 0.35:
            score += 8.0

        if inp.avg_email_reply_rate_pct < 0.05:
            score += 35.0
        elif inp.avg_email_reply_rate_pct < 0.10:
            score += 18.0
        elif inp.avg_email_reply_rate_pct < 0.15:
            score += 7.0

        if inp.avg_unsubscribe_rate_pct >= 0.05:
            score += 25.0
        elif inp.avg_unsubscribe_rate_pct >= 0.02:
            score += 12.0

        return min(score, 100.0)

    def _sequence_quality_score(self, inp: EmailSequenceInput) -> float:
        score = 0.0

        if inp.personalization_rate_pct < 0.20:
            score += 35.0
        elif inp.personalization_rate_pct < 0.40:
            score += 18.0
        elif inp.personalization_rate_pct < 0.60:
            score += 7.0

        if inp.template_vs_custom_ratio >= 0.85:
            score += 30.0
        elif inp.template_vs_custom_ratio >= 0.70:
            score += 15.0

        if inp.avg_email_word_count > 300:
            score += 20.0
        elif inp.avg_email_word_count > 200:
            score += 10.0

        if inp.calls_to_action_per_email_avg > 3.0:
            score += 15.0
        elif inp.calls_to_action_per_email_avg > 2.0:
            score += 7.0

        return min(score, 100.0)

    def _timing_optimization_score(self, inp: EmailSequenceInput) -> float:
        score = 0.0

        if inp.avg_send_time_score < 0.30:
            score += 40.0
        elif inp.avg_send_time_score < 0.55:
            score += 20.0
        elif inp.avg_send_time_score < 0.70:
            score += 8.0

        if inp.avg_days_between_touchpoints >= 14.0:
            score += 35.0
        elif inp.avg_days_between_touchpoints >= 7.0:
            score += 18.0
        elif inp.avg_days_between_touchpoints >= 4.0:
            score += 7.0

        if inp.avg_follow_up_attempts_per_prospect < 2.0:
            score += 25.0
        elif inp.avg_follow_up_attempts_per_prospect < 4.0:
            score += 10.0

        return min(score, 100.0)

    def _conversion_effectiveness_score(self, inp: EmailSequenceInput) -> float:
        score = 0.0

        if inp.email_to_meeting_conversion_pct < 0.03:
            score += 45.0
        elif inp.email_to_meeting_conversion_pct < 0.06:
            score += 25.0
        elif inp.email_to_meeting_conversion_pct < 0.10:
            score += 10.0

        if inp.sequences_with_no_reply_pct >= 0.70:
            score += 30.0
        elif inp.sequences_with_no_reply_pct >= 0.50:
            score += 15.0

        if inp.avg_bounce_rate_pct >= 0.10:
            score += 25.0
        elif inp.avg_bounce_rate_pct >= 0.05:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: EmailSequenceInput,
                         engagement: float, quality: float,
                         timing: float, conversion: float) -> EmailSequencePattern:
        if engagement >= 35 and inp.avg_email_open_rate_pct < 0.20:
            return EmailSequencePattern.low_open_rate

        if quality >= 30 and inp.personalization_rate_pct < 0.30:
            return EmailSequencePattern.poor_personalization

        if engagement >= 25 and inp.avg_unsubscribe_rate_pct >= 0.03:
            return EmailSequencePattern.email_fatigue

        if timing >= 30 and inp.avg_days_between_touchpoints >= 7.0:
            return EmailSequencePattern.timing_failure

        if quality >= 20 and inp.template_vs_custom_ratio >= 0.75:
            return EmailSequencePattern.template_overuse

        return EmailSequencePattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> EmailSequenceRisk:
        if composite >= 60:
            return EmailSequenceRisk.critical
        if composite >= 40:
            return EmailSequenceRisk.high
        if composite >= 20:
            return EmailSequenceRisk.moderate
        return EmailSequenceRisk.low

    def _severity(self, composite: float) -> EmailSequenceSeverity:
        if composite >= 60:
            return EmailSequenceSeverity.failing
        if composite >= 40:
            return EmailSequenceSeverity.weak
        if composite >= 20:
            return EmailSequenceSeverity.developing
        return EmailSequenceSeverity.strong

    def _action(self, risk: EmailSequenceRisk,
                 pattern: EmailSequencePattern) -> EmailSequenceAction:
        if risk == EmailSequenceRisk.critical:
            if pattern == EmailSequencePattern.email_fatigue:
                return EmailSequenceAction.email_fatigue_intervention
            if pattern == EmailSequencePattern.poor_personalization:
                return EmailSequenceAction.personalization_coaching
            return EmailSequenceAction.sequence_optimization
        if risk == EmailSequenceRisk.high:
            if pattern == EmailSequencePattern.timing_failure:
                return EmailSequenceAction.timing_recalibration
            if pattern == EmailSequencePattern.template_overuse:
                return EmailSequenceAction.template_refresh
            return EmailSequenceAction.sequence_optimization
        if risk == EmailSequenceRisk.moderate:
            return EmailSequenceAction.sequence_optimization
        return EmailSequenceAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_sequence_gap(self, composite: float,
                           inp: EmailSequenceInput) -> bool:
        return (
            composite >= 40
            or inp.email_to_meeting_conversion_pct < 0.03
            or inp.avg_unsubscribe_rate_pct >= 0.05
        )

    def _requires_sequence_coaching(self, composite: float,
                                     inp: EmailSequenceInput) -> bool:
        return (
            composite >= 30
            or inp.personalization_rate_pct < 0.20
            or inp.avg_email_reply_rate_pct < 0.05
        )

    # ------------------------------------------------------------------
    # Pipeline impact
    # ------------------------------------------------------------------

    def _estimated_pipeline_impact(self, inp: EmailSequenceInput,
                                    composite: float) -> float:
        silent_sequences = round(inp.total_sequences_active * inp.sequences_with_no_reply_pct)
        return round(silent_sequences * inp.avg_opportunity_value_usd * (composite / 100.0) * 0.12, 2)

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: EmailSequenceInput,
                 pattern: EmailSequencePattern, composite: float) -> str:
        if pattern == EmailSequencePattern.none and composite < 20:
            return "Email sequence performance healthy — engagement, personalization, and conversion within benchmarks"
        parts: list[str] = []
        if inp.avg_email_open_rate_pct < 1.0:
            parts.append(f"{inp.avg_email_open_rate_pct*100:.0f}% open rate")
        if inp.avg_email_reply_rate_pct < 1.0:
            parts.append(f"{inp.avg_email_reply_rate_pct*100:.0f}% reply rate")
        if inp.email_to_meeting_conversion_pct < 1.0:
            parts.append(f"{inp.email_to_meeting_conversion_pct*100:.1f}% email-to-meeting")
        label = pattern.value.replace("_", " ") if pattern != EmailSequencePattern.none else "Email sequence risk"
        summary = " — ".join(parts) if parts else "sequence performance declining"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: EmailSequenceInput) -> EmailSequenceResult:
        engagement  = round(self._engagement_decay_score(inp), 1)
        quality     = round(self._sequence_quality_score(inp), 1)
        timing      = round(self._timing_optimization_score(inp), 1)
        conversion  = round(self._conversion_effectiveness_score(inp), 1)

        composite = round(
            engagement * 0.30 + quality * 0.30 + timing * 0.25 + conversion * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, engagement, quality, timing, conversion)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap    = self._has_sequence_gap(composite, inp)
        coach  = self._requires_sequence_coaching(composite, inp)
        impact = self._estimated_pipeline_impact(inp, composite)
        signal = self._signal(inp, pattern, composite)

        result = EmailSequenceResult(
            rep_id=inp.rep_id,
            region=inp.region,
            email_sequence_risk=risk,
            email_sequence_pattern=pattern,
            email_sequence_severity=severity,
            recommended_action=action,
            engagement_decay_score=engagement,
            sequence_quality_score=quality,
            timing_optimization_score=timing,
            conversion_effectiveness_score=conversion,
            email_sequence_composite=composite,
            has_sequence_gap=gap,
            requires_sequence_coaching=coach,
            estimated_pipeline_impact_usd=impact,
            email_sequence_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[EmailSequenceInput]) -> list[EmailSequenceResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_email_sequence_composite": 0.0,
                "sequence_gap_count": 0,
                "coaching_count": 0,
                "avg_engagement_decay_score": 0.0,
                "avg_sequence_quality_score": 0.0,
                "avg_timing_optimization_score": 0.0,
                "avg_conversion_effectiveness_score": 0.0,
                "total_estimated_pipeline_impact_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_eng = total_qual = total_tim = total_conv = total_impact = 0.0

        for r in self._results:
            risk_counts[r.email_sequence_risk.value]       = risk_counts.get(r.email_sequence_risk.value, 0) + 1
            pattern_counts[r.email_sequence_pattern.value] = pattern_counts.get(r.email_sequence_pattern.value, 0) + 1
            severity_counts[r.email_sequence_severity.value] = severity_counts.get(r.email_sequence_severity.value, 0) + 1
            action_counts[r.recommended_action.value]      = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp   += r.email_sequence_composite
            total_eng    += r.engagement_decay_score
            total_qual   += r.sequence_quality_score
            total_tim    += r.timing_optimization_score
            total_conv   += r.conversion_effectiveness_score
            total_impact += r.estimated_pipeline_impact_usd

        n = len(self._results)

        return {
            "total":                                    n,
            "risk_counts":                              risk_counts,
            "pattern_counts":                           pattern_counts,
            "severity_counts":                          severity_counts,
            "action_counts":                            action_counts,
            "avg_email_sequence_composite":             round(total_comp / n, 1),
            "sequence_gap_count":                       sum(1 for r in self._results if r.has_sequence_gap),
            "coaching_count":                           sum(1 for r in self._results if r.requires_sequence_coaching),
            "avg_engagement_decay_score":               round(total_eng / n, 1),
            "avg_sequence_quality_score":               round(total_qual / n, 1),
            "avg_timing_optimization_score":            round(total_tim / n, 1),
            "avg_conversion_effectiveness_score":       round(total_conv / n, 1),
            "total_estimated_pipeline_impact_usd":      round(total_impact, 2),
        }
