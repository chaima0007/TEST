from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class ProspectingRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ProspectingPattern(str, Enum):
    none             = "none"
    low_activity     = "low_activity"
    poor_targeting   = "poor_targeting"
    low_connect_rate = "low_connect_rate"
    pipeline_stall   = "pipeline_stall"
    burnout_signal   = "burnout_signal"


class ProspectingSeverity(str, Enum):
    active     = "active"
    developing = "developing"
    lagging    = "lagging"
    stalled    = "stalled"


class ProspectingAction(str, Enum):
    no_action              = "no_action"
    activity_coaching      = "activity_coaching"
    targeting_calibration  = "targeting_calibration"
    messaging_optimization = "messaging_optimization"
    cadence_redesign       = "cadence_redesign"
    pipeline_acceleration  = "pipeline_acceleration"


@dataclass
class OutboundProspectingInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    outbound_attempts_total: int
    outbound_calls_made: int
    outbound_emails_sent: int
    social_touches_made: int
    connected_conversations: int
    connect_rate_pct: float
    discovery_calls_booked: int
    discovery_to_demo_conversion_rate_pct: float
    demos_booked_from_outbound: int
    outbound_pipeline_created_usd: float
    avg_touches_per_prospect: float
    prospects_contacted: int
    new_prospects_added: int
    icp_prospects_targeted_pct: float
    avg_response_rate_pct: float
    sequence_completion_rate_pct: float
    meetings_no_show_rate_pct: float
    avg_outreach_quality_score: float
    days_with_zero_outbound_activity: int


@dataclass
class OutboundProspectingResult:
    rep_id: str
    region: str
    prospecting_risk: ProspectingRisk
    prospecting_pattern: ProspectingPattern
    prospecting_severity: ProspectingSeverity
    recommended_action: ProspectingAction
    activity_volume_score: float
    targeting_quality_score: float
    conversion_effectiveness_score: float
    pipeline_contribution_score: float
    prospecting_effectiveness_composite: float
    has_prospecting_gap: bool
    requires_prospecting_coaching: bool
    estimated_pipeline_shortfall_usd: float
    prospecting_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                               self.rep_id,
            "region":                               self.region,
            "prospecting_risk":                     self.prospecting_risk.value,
            "prospecting_pattern":                  self.prospecting_pattern.value,
            "prospecting_severity":                 self.prospecting_severity.value,
            "recommended_action":                   self.recommended_action.value,
            "activity_volume_score":                self.activity_volume_score,
            "targeting_quality_score":              self.targeting_quality_score,
            "conversion_effectiveness_score":       self.conversion_effectiveness_score,
            "pipeline_contribution_score":          self.pipeline_contribution_score,
            "prospecting_effectiveness_composite":  self.prospecting_effectiveness_composite,
            "has_prospecting_gap":                  self.has_prospecting_gap,
            "requires_prospecting_coaching":        self.requires_prospecting_coaching,
            "estimated_pipeline_shortfall_usd":     self.estimated_pipeline_shortfall_usd,
            "prospecting_signal":                   self.prospecting_signal,
        }


class SalesOutboundProspectingIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[OutboundProspectingResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _activity_volume_score(self, inp: OutboundProspectingInput) -> float:
        score = 0.0

        if inp.outbound_attempts_total < 50:
            score += 40.0
        elif inp.outbound_attempts_total < 100:
            score += 20.0
        elif inp.outbound_attempts_total < 150:
            score += 8.0

        if inp.days_with_zero_outbound_activity >= 10:
            score += 30.0
        elif inp.days_with_zero_outbound_activity >= 5:
            score += 15.0
        elif inp.days_with_zero_outbound_activity >= 2:
            score += 5.0

        if inp.new_prospects_added < 10:
            score += 20.0
        elif inp.new_prospects_added < 20:
            score += 10.0

        return min(score, 100.0)

    def _targeting_quality_score(self, inp: OutboundProspectingInput) -> float:
        score = 0.0

        if inp.icp_prospects_targeted_pct < 0.30:
            score += 40.0
        elif inp.icp_prospects_targeted_pct < 0.50:
            score += 20.0
        elif inp.icp_prospects_targeted_pct < 0.70:
            score += 8.0

        if inp.avg_outreach_quality_score < 4.0:
            score += 30.0
        elif inp.avg_outreach_quality_score < 6.0:
            score += 15.0

        if inp.avg_touches_per_prospect < 3.0:
            score += 20.0
        elif inp.avg_touches_per_prospect < 5.0:
            score += 10.0

        return min(score, 100.0)

    def _conversion_effectiveness_score(self, inp: OutboundProspectingInput) -> float:
        score = 0.0

        if inp.connect_rate_pct < 0.05:
            score += 45.0
        elif inp.connect_rate_pct < 0.10:
            score += 25.0
        elif inp.connect_rate_pct < 0.15:
            score += 10.0

        if inp.avg_response_rate_pct < 0.03:
            score += 30.0
        elif inp.avg_response_rate_pct < 0.05:
            score += 15.0

        if inp.meetings_no_show_rate_pct >= 0.30:
            score += 20.0
        elif inp.meetings_no_show_rate_pct >= 0.15:
            score += 10.0

        return min(score, 100.0)

    def _pipeline_contribution_score(self, inp: OutboundProspectingInput) -> float:
        score = 0.0

        if inp.outbound_pipeline_created_usd < 10_000:
            score += 40.0
        elif inp.outbound_pipeline_created_usd < 50_000:
            score += 20.0
        elif inp.outbound_pipeline_created_usd < 100_000:
            score += 8.0

        if inp.discovery_calls_booked < 3:
            score += 30.0
        elif inp.discovery_calls_booked < 7:
            score += 15.0

        if inp.discovery_to_demo_conversion_rate_pct < 0.30:
            score += 20.0
        elif inp.discovery_to_demo_conversion_rate_pct < 0.50:
            score += 10.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: OutboundProspectingInput,
                         volume: float, targeting: float,
                         conversion: float, pipeline: float) -> ProspectingPattern:
        if volume >= 35 and inp.outbound_attempts_total < 100 and inp.days_with_zero_outbound_activity >= 5:
            return ProspectingPattern.low_activity

        if targeting >= 30 and inp.icp_prospects_targeted_pct < 0.40:
            return ProspectingPattern.poor_targeting

        if conversion >= 30 and inp.connect_rate_pct < 0.08:
            return ProspectingPattern.low_connect_rate

        if pipeline >= 30 and inp.outbound_pipeline_created_usd < 50_000:
            return ProspectingPattern.pipeline_stall

        if volume >= 25 and inp.days_with_zero_outbound_activity >= 8:
            return ProspectingPattern.burnout_signal

        return ProspectingPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> ProspectingRisk:
        if composite >= 60:
            return ProspectingRisk.critical
        if composite >= 40:
            return ProspectingRisk.high
        if composite >= 20:
            return ProspectingRisk.moderate
        return ProspectingRisk.low

    def _severity(self, composite: float) -> ProspectingSeverity:
        if composite >= 60:
            return ProspectingSeverity.stalled
        if composite >= 40:
            return ProspectingSeverity.lagging
        if composite >= 20:
            return ProspectingSeverity.developing
        return ProspectingSeverity.active

    def _action(self, risk: ProspectingRisk,
                 pattern: ProspectingPattern) -> ProspectingAction:
        if risk == ProspectingRisk.critical:
            if pattern == ProspectingPattern.low_activity:
                return ProspectingAction.cadence_redesign
            if pattern == ProspectingPattern.poor_targeting:
                return ProspectingAction.targeting_calibration
            return ProspectingAction.pipeline_acceleration
        if risk == ProspectingRisk.high:
            if pattern == ProspectingPattern.low_connect_rate:
                return ProspectingAction.messaging_optimization
            if pattern == ProspectingPattern.burnout_signal:
                return ProspectingAction.cadence_redesign
            return ProspectingAction.activity_coaching
        if risk == ProspectingRisk.moderate:
            return ProspectingAction.activity_coaching
        return ProspectingAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_prospecting_gap(self, composite: float,
                              inp: OutboundProspectingInput) -> bool:
        return (
            composite >= 40
            or inp.outbound_attempts_total < 50
            or inp.discovery_calls_booked < 3
        )

    def _requires_prospecting_coaching(self, composite: float,
                                        inp: OutboundProspectingInput) -> bool:
        return (
            composite >= 30
            or inp.connect_rate_pct < 0.05
            or inp.icp_prospects_targeted_pct < 0.40
        )

    # ------------------------------------------------------------------
    # Pipeline shortfall
    # ------------------------------------------------------------------

    def _estimated_pipeline_shortfall(self, inp: OutboundProspectingInput,
                                       composite: float) -> float:
        shortfall = (100_000.0 - inp.outbound_pipeline_created_usd) * (composite / 100.0)
        return round(max(shortfall, 0.0), 2)

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: OutboundProspectingInput,
                 pattern: ProspectingPattern, composite: float) -> str:
        if pattern == ProspectingPattern.none and composite < 20:
            return "Outbound prospecting activity and pipeline contribution on track"
        parts: list[str] = []
        if inp.outbound_attempts_total < 150:
            parts.append(f"{inp.outbound_attempts_total} total attempts")
        if inp.connect_rate_pct < 0.15:
            parts.append(f"{inp.connect_rate_pct*100:.0f}% connect rate")
        if inp.discovery_calls_booked < 10:
            parts.append(f"{inp.discovery_calls_booked} discovery calls booked")
        label = pattern.value.replace("_", " ") if pattern != ProspectingPattern.none else "Prospecting risk"
        summary = " — ".join(parts) if parts else "prospecting effectiveness declining"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: OutboundProspectingInput) -> OutboundProspectingResult:
        volume     = round(self._activity_volume_score(inp), 1)
        targeting  = round(self._targeting_quality_score(inp), 1)
        conversion = round(self._conversion_effectiveness_score(inp), 1)
        pipeline   = round(self._pipeline_contribution_score(inp), 1)

        composite = round(
            volume * 0.25 + targeting * 0.25 + conversion * 0.30 + pipeline * 0.20, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, volume, targeting, conversion, pipeline)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap       = self._has_prospecting_gap(composite, inp)
        coaching  = self._requires_prospecting_coaching(composite, inp)
        shortfall = self._estimated_pipeline_shortfall(inp, composite)
        signal    = self._signal(inp, pattern, composite)

        result = OutboundProspectingResult(
            rep_id=inp.rep_id,
            region=inp.region,
            prospecting_risk=risk,
            prospecting_pattern=pattern,
            prospecting_severity=severity,
            recommended_action=action,
            activity_volume_score=volume,
            targeting_quality_score=targeting,
            conversion_effectiveness_score=conversion,
            pipeline_contribution_score=pipeline,
            prospecting_effectiveness_composite=composite,
            has_prospecting_gap=gap,
            requires_prospecting_coaching=coaching,
            estimated_pipeline_shortfall_usd=shortfall,
            prospecting_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[OutboundProspectingInput]) -> list[OutboundProspectingResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_prospecting_effectiveness_composite": 0.0,
                "prospecting_gap_count": 0,
                "prospecting_coaching_count": 0,
                "avg_activity_volume_score": 0.0,
                "avg_targeting_quality_score": 0.0,
                "avg_conversion_effectiveness_score": 0.0,
                "avg_pipeline_contribution_score": 0.0,
                "total_estimated_pipeline_shortfall_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_vol = total_tgt = total_conv = total_pipe = total_short = 0.0

        for r in self._results:
            risk_counts[r.prospecting_risk.value]       = risk_counts.get(r.prospecting_risk.value, 0) + 1
            pattern_counts[r.prospecting_pattern.value] = pattern_counts.get(r.prospecting_pattern.value, 0) + 1
            severity_counts[r.prospecting_severity.value] = severity_counts.get(r.prospecting_severity.value, 0) + 1
            action_counts[r.recommended_action.value]     = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp  += r.prospecting_effectiveness_composite
            total_vol   += r.activity_volume_score
            total_tgt   += r.targeting_quality_score
            total_conv  += r.conversion_effectiveness_score
            total_pipe  += r.pipeline_contribution_score
            total_short += r.estimated_pipeline_shortfall_usd

        n = len(self._results)

        return {
            "total":                                    n,
            "risk_counts":                              risk_counts,
            "pattern_counts":                           pattern_counts,
            "severity_counts":                          severity_counts,
            "action_counts":                            action_counts,
            "avg_prospecting_effectiveness_composite":  round(total_comp / n, 1),
            "prospecting_gap_count":                    sum(1 for r in self._results if r.has_prospecting_gap),
            "prospecting_coaching_count":               sum(1 for r in self._results if r.requires_prospecting_coaching),
            "avg_activity_volume_score":                round(total_vol / n, 1),
            "avg_targeting_quality_score":              round(total_tgt / n, 1),
            "avg_conversion_effectiveness_score":       round(total_conv / n, 1),
            "avg_pipeline_contribution_score":          round(total_pipe / n, 1),
            "total_estimated_pipeline_shortfall_usd":   round(total_short, 2),
        }
