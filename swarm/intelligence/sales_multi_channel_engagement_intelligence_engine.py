from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class ChannelRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ChannelPattern(str, Enum):
    none                       = "none"
    single_channel_dependency  = "single_channel_dependency"
    low_touch_frequency        = "low_touch_frequency"
    poor_email_quality         = "poor_email_quality"
    channel_sequence_violation = "channel_sequence_violation"
    digital_only_approach      = "digital_only_approach"


class ChannelSeverity(str, Enum):
    optimized  = "optimized"
    developing = "developing"
    limited    = "limited"
    siloed     = "siloed"


class ChannelAction(str, Enum):
    no_action                   = "no_action"
    channel_coaching            = "channel_coaching"
    cadence_optimization        = "cadence_optimization"
    email_quality_review        = "email_quality_review"
    multi_channel_training      = "multi_channel_training"
    outreach_sequence_redesign  = "outreach_sequence_redesign"


@dataclass
class MultiChannelEngagementInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    total_prospect_touches: int
    email_touches_count: int
    phone_touches_count: int
    linkedin_touches_count: int
    video_message_touches_count: int
    in_person_touches_count: int
    direct_mail_touches_count: int
    avg_opportunity_value_usd: float
    unique_channels_used_count: int
    avg_touches_per_prospect: float
    single_channel_prospects_count: int
    multi_channel_prospects_count: int
    email_open_rate_pct: float
    email_reply_rate_pct: float
    phone_connect_rate_pct: float
    linkedin_response_rate_pct: float
    follow_up_cadence_compliance_pct: float
    channel_sequence_compliance_pct: float
    avg_days_between_touches: float


@dataclass
class MultiChannelEngagementResult:
    rep_id: str
    region: str
    channel_risk: ChannelRisk
    channel_pattern: ChannelPattern
    channel_severity: ChannelSeverity
    recommended_action: ChannelAction
    channel_diversity_score: float
    channel_effectiveness_score: float
    touch_frequency_score: float
    sequence_compliance_score: float
    channel_engagement_composite: float
    has_channel_gap: bool
    requires_channel_coaching: bool
    estimated_pipeline_impact_usd: float
    channel_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "channel_risk":                     self.channel_risk.value,
            "channel_pattern":                  self.channel_pattern.value,
            "channel_severity":                 self.channel_severity.value,
            "recommended_action":               self.recommended_action.value,
            "channel_diversity_score":          self.channel_diversity_score,
            "channel_effectiveness_score":      self.channel_effectiveness_score,
            "touch_frequency_score":            self.touch_frequency_score,
            "sequence_compliance_score":        self.sequence_compliance_score,
            "channel_engagement_composite":     self.channel_engagement_composite,
            "has_channel_gap":                  self.has_channel_gap,
            "requires_channel_coaching":        self.requires_channel_coaching,
            "estimated_pipeline_impact_usd":    self.estimated_pipeline_impact_usd,
            "channel_signal":                   self.channel_signal,
        }


class SalesMultiChannelEngagementIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[MultiChannelEngagementResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _channel_diversity_score(self, inp: MultiChannelEngagementInput) -> float:
        score = 0.0

        if inp.unique_channels_used_count == 1:
            score += 50.0
        elif inp.unique_channels_used_count == 2:
            score += 30.0
        elif inp.unique_channels_used_count == 3:
            score += 15.0

        total_prospects = max(inp.single_channel_prospects_count + inp.multi_channel_prospects_count, 1)
        single_rate = inp.single_channel_prospects_count / total_prospects
        if single_rate >= 0.60:
            score += 35.0
        elif single_rate >= 0.40:
            score += 18.0
        elif single_rate >= 0.20:
            score += 7.0

        if inp.phone_touches_count == 0 and inp.in_person_touches_count == 0:
            score += 15.0

        return min(score, 100.0)

    def _channel_effectiveness_score(self, inp: MultiChannelEngagementInput) -> float:
        score = 0.0

        if inp.email_open_rate_pct < 0.20:
            score += 30.0
        elif inp.email_open_rate_pct < 0.30:
            score += 15.0
        elif inp.email_open_rate_pct < 0.40:
            score += 7.0

        if inp.email_reply_rate_pct < 0.03:
            score += 35.0
        elif inp.email_reply_rate_pct < 0.05:
            score += 18.0
        elif inp.email_reply_rate_pct < 0.08:
            score += 7.0

        if inp.phone_connect_rate_pct < 0.05:
            score += 25.0
        elif inp.phone_connect_rate_pct < 0.10:
            score += 12.0

        return min(score, 100.0)

    def _touch_frequency_score(self, inp: MultiChannelEngagementInput) -> float:
        score = 0.0

        if inp.avg_touches_per_prospect < 3.0:
            score += 40.0
        elif inp.avg_touches_per_prospect < 5.0:
            score += 20.0
        elif inp.avg_touches_per_prospect < 7.0:
            score += 8.0

        if inp.avg_days_between_touches >= 10.0:
            score += 35.0
        elif inp.avg_days_between_touches >= 7.0:
            score += 18.0
        elif inp.avg_days_between_touches >= 5.0:
            score += 7.0

        if inp.follow_up_cadence_compliance_pct < 0.40:
            score += 20.0
        elif inp.follow_up_cadence_compliance_pct < 0.60:
            score += 10.0

        return min(score, 100.0)

    def _sequence_compliance_score(self, inp: MultiChannelEngagementInput) -> float:
        score = 0.0

        if inp.channel_sequence_compliance_pct < 0.30:
            score += 45.0
        elif inp.channel_sequence_compliance_pct < 0.50:
            score += 25.0
        elif inp.channel_sequence_compliance_pct < 0.70:
            score += 10.0

        total = max(inp.total_prospect_touches, 1)
        email_heavy_rate = inp.email_touches_count / total
        if email_heavy_rate >= 0.80:
            score += 30.0
        elif email_heavy_rate >= 0.60:
            score += 15.0

        if inp.linkedin_response_rate_pct < 0.05 and inp.linkedin_touches_count > 0:
            score += 15.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: MultiChannelEngagementInput,
                          diversity: float, effectiveness: float,
                          frequency: float, compliance: float) -> ChannelPattern:
        if diversity >= 35 and inp.unique_channels_used_count <= 2:
            return ChannelPattern.single_channel_dependency

        if frequency >= 35 and inp.avg_touches_per_prospect < 4.0:
            return ChannelPattern.low_touch_frequency

        if effectiveness >= 30 and inp.email_reply_rate_pct < 0.05:
            return ChannelPattern.poor_email_quality

        if compliance >= 35 and inp.channel_sequence_compliance_pct < 0.50:
            return ChannelPattern.channel_sequence_violation

        if diversity >= 25 and inp.phone_touches_count == 0:
            return ChannelPattern.digital_only_approach

        return ChannelPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> ChannelRisk:
        if composite >= 60:
            return ChannelRisk.critical
        if composite >= 40:
            return ChannelRisk.high
        if composite >= 20:
            return ChannelRisk.moderate
        return ChannelRisk.low

    def _severity(self, composite: float) -> ChannelSeverity:
        if composite >= 60:
            return ChannelSeverity.siloed
        if composite >= 40:
            return ChannelSeverity.limited
        if composite >= 20:
            return ChannelSeverity.developing
        return ChannelSeverity.optimized

    def _action(self, risk: ChannelRisk,
                 pattern: ChannelPattern) -> ChannelAction:
        if risk == ChannelRisk.critical:
            if pattern == ChannelPattern.single_channel_dependency:
                return ChannelAction.multi_channel_training
            if pattern == ChannelPattern.channel_sequence_violation:
                return ChannelAction.outreach_sequence_redesign
            return ChannelAction.multi_channel_training
        if risk == ChannelRisk.high:
            if pattern == ChannelPattern.poor_email_quality:
                return ChannelAction.email_quality_review
            if pattern == ChannelPattern.low_touch_frequency:
                return ChannelAction.cadence_optimization
            return ChannelAction.channel_coaching
        if risk == ChannelRisk.moderate:
            return ChannelAction.channel_coaching
        return ChannelAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_channel_gap(self, composite: float,
                          inp: MultiChannelEngagementInput) -> bool:
        return (
            composite >= 40
            or inp.unique_channels_used_count <= 1
            or inp.avg_touches_per_prospect < 3.0
        )

    def _requires_channel_coaching(self, composite: float,
                                    inp: MultiChannelEngagementInput) -> bool:
        total_prospects = max(inp.single_channel_prospects_count + inp.multi_channel_prospects_count, 1)
        single_rate = inp.single_channel_prospects_count / total_prospects
        return (
            composite >= 30
            or single_rate >= 0.50
            or inp.email_reply_rate_pct < 0.03
        )

    # ------------------------------------------------------------------
    # Pipeline impact
    # ------------------------------------------------------------------

    def _estimated_pipeline_impact(self, inp: MultiChannelEngagementInput,
                                    composite: float) -> float:
        return round(
            inp.single_channel_prospects_count * inp.avg_opportunity_value_usd * (composite / 100.0), 2
        )

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: MultiChannelEngagementInput,
                 pattern: ChannelPattern, composite: float) -> str:
        if pattern == ChannelPattern.none and composite < 20:
            return "Multi-channel outreach balanced and performing within benchmarks"
        parts: list[str] = []
        if inp.unique_channels_used_count <= 2:
            parts.append(f"{inp.unique_channels_used_count} channel(s) only")
        if inp.avg_touches_per_prospect < 6.0:
            parts.append(f"{inp.avg_touches_per_prospect:.1f} avg touches/prospect")
        if inp.email_reply_rate_pct < 0.08:
            parts.append(f"{inp.email_reply_rate_pct*100:.1f}% email reply rate")
        label = pattern.value.replace("_", " ") if pattern != ChannelPattern.none else "Channel risk"
        summary = " — ".join(parts) if parts else "outreach coverage limited"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: MultiChannelEngagementInput) -> MultiChannelEngagementResult:
        diversity     = round(self._channel_diversity_score(inp), 1)
        effectiveness = round(self._channel_effectiveness_score(inp), 1)
        frequency     = round(self._touch_frequency_score(inp), 1)
        compliance    = round(self._sequence_compliance_score(inp), 1)

        composite = round(
            diversity * 0.30 + effectiveness * 0.30 + frequency * 0.25 + compliance * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, diversity, effectiveness, frequency, compliance)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap      = self._has_channel_gap(composite, inp)
        coaching = self._requires_channel_coaching(composite, inp)
        impact   = self._estimated_pipeline_impact(inp, composite)
        signal   = self._signal(inp, pattern, composite)

        result = MultiChannelEngagementResult(
            rep_id=inp.rep_id,
            region=inp.region,
            channel_risk=risk,
            channel_pattern=pattern,
            channel_severity=severity,
            recommended_action=action,
            channel_diversity_score=diversity,
            channel_effectiveness_score=effectiveness,
            touch_frequency_score=frequency,
            sequence_compliance_score=compliance,
            channel_engagement_composite=composite,
            has_channel_gap=gap,
            requires_channel_coaching=coaching,
            estimated_pipeline_impact_usd=impact,
            channel_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[MultiChannelEngagementInput]) -> list[MultiChannelEngagementResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_channel_engagement_composite": 0.0,
                "channel_gap_count": 0,
                "channel_coaching_count": 0,
                "avg_channel_diversity_score": 0.0,
                "avg_channel_effectiveness_score": 0.0,
                "avg_touch_frequency_score": 0.0,
                "avg_sequence_compliance_score": 0.0,
                "total_estimated_pipeline_impact_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_div = total_eff = total_frq = total_seq = total_imp = 0.0

        for r in self._results:
            risk_counts[r.channel_risk.value]       = risk_counts.get(r.channel_risk.value, 0) + 1
            pattern_counts[r.channel_pattern.value] = pattern_counts.get(r.channel_pattern.value, 0) + 1
            severity_counts[r.channel_severity.value] = severity_counts.get(r.channel_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.channel_engagement_composite
            total_div  += r.channel_diversity_score
            total_eff  += r.channel_effectiveness_score
            total_frq  += r.touch_frequency_score
            total_seq  += r.sequence_compliance_score
            total_imp  += r.estimated_pipeline_impact_usd

        n = len(self._results)

        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_channel_engagement_composite":     round(total_comp / n, 1),
            "channel_gap_count":                    sum(1 for r in self._results if r.has_channel_gap),
            "channel_coaching_count":               sum(1 for r in self._results if r.requires_channel_coaching),
            "avg_channel_diversity_score":          round(total_div / n, 1),
            "avg_channel_effectiveness_score":      round(total_eff / n, 1),
            "avg_touch_frequency_score":            round(total_frq / n, 1),
            "avg_sequence_compliance_score":        round(total_seq / n, 1),
            "total_estimated_pipeline_impact_usd":  round(total_imp, 2),
        }
