from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class EfficiencyRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class EfficiencyPattern(str, Enum):
    none                        = "none"
    low_activity_volume         = "low_activity_volume"
    poor_conversion             = "poor_conversion"
    activity_channel_overreliance = "activity_channel_overreliance"
    pipeline_coverage_gap       = "pipeline_coverage_gap"
    activity_decay              = "activity_decay"


class EfficiencySeverity(str, Enum):
    healthy        = "healthy"
    underperforming = "underperforming"
    degraded       = "degraded"
    critical       = "critical"


class EfficiencyAction(str, Enum):
    no_action                   = "no_action"
    activity_increase           = "activity_increase"
    conversion_coaching         = "conversion_coaching"
    channel_diversification     = "channel_diversification"
    pipeline_blitz              = "pipeline_blitz"
    performance_improvement_plan = "performance_improvement_plan"


@dataclass
class PipelineEfficiencyInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    cold_calls_made: int
    cold_call_connect_rate_pct: float
    emails_sent: int
    email_reply_rate_pct: float
    demos_conducted: int
    demo_to_opp_conversion_rate_pct: float
    events_attended: int
    event_leads_generated: int
    referrals_requested: int
    referrals_received: int
    social_touches_count: int
    meetings_booked: int
    qualified_opps_created: int
    pipeline_generated_usd: float
    pipeline_target_usd: float
    activity_mix_variance_score: float
    prior_period_pipeline_generated_usd: float
    activities_total_count: int
    crm_activity_logging_rate_pct: float


@dataclass
class PipelineEfficiencyResult:
    rep_id: str
    region: str
    efficiency_risk: EfficiencyRisk
    efficiency_pattern: EfficiencyPattern
    efficiency_severity: EfficiencySeverity
    recommended_action: EfficiencyAction
    activity_volume_score: float
    conversion_efficiency_score: float
    pipeline_coverage_score: float
    activity_mix_score: float
    pipeline_efficiency_composite: float
    is_pipeline_at_risk: bool
    requires_activity_intervention: bool
    estimated_pipeline_gap_usd: float
    efficiency_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                       self.rep_id,
            "region":                       self.region,
            "efficiency_risk":              self.efficiency_risk.value,
            "efficiency_pattern":           self.efficiency_pattern.value,
            "efficiency_severity":          self.efficiency_severity.value,
            "recommended_action":           self.recommended_action.value,
            "activity_volume_score":        self.activity_volume_score,
            "conversion_efficiency_score":  self.conversion_efficiency_score,
            "pipeline_coverage_score":      self.pipeline_coverage_score,
            "activity_mix_score":           self.activity_mix_score,
            "pipeline_efficiency_composite": self.pipeline_efficiency_composite,
            "is_pipeline_at_risk":          self.is_pipeline_at_risk,
            "requires_activity_intervention": self.requires_activity_intervention,
            "estimated_pipeline_gap_usd":   self.estimated_pipeline_gap_usd,
            "efficiency_signal":            self.efficiency_signal,
        }


class PipelineGenerationEfficiencyEngine:

    def __init__(self) -> None:
        self._results: list[PipelineEfficiencyResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk / less efficient)
    # ------------------------------------------------------------------

    def _activity_volume_score(self, inp: PipelineEfficiencyInput) -> float:
        score = 0.0

        # Insufficient total activity
        if inp.activities_total_count < 50:
            score += 35.0
        elif inp.activities_total_count < 100:
            score += 20.0
        elif inp.activities_total_count < 150:
            score += 8.0

        # Insufficient meetings booked
        if inp.meetings_booked < 5:
            score += 25.0
        elif inp.meetings_booked < 10:
            score += 12.0

        # Suspiciously low outbound calls
        if inp.cold_calls_made < 20:
            score += 15.0
        elif inp.cold_calls_made < 40:
            score += 8.0

        # CRM logging gaps hide true activity levels
        if inp.crm_activity_logging_rate_pct < 0.50:
            score += 25.0
        elif inp.crm_activity_logging_rate_pct < 0.70:
            score += 12.0

        return min(score, 100.0)

    def _conversion_efficiency_score(self, inp: PipelineEfficiencyInput) -> float:
        score = 0.0

        # Cold call connect rate
        if inp.cold_call_connect_rate_pct < 0.10:
            score += 30.0
        elif inp.cold_call_connect_rate_pct < 0.20:
            score += 15.0

        # Email reply rate
        if inp.email_reply_rate_pct < 0.05:
            score += 25.0
        elif inp.email_reply_rate_pct < 0.10:
            score += 12.0

        # Demo to opportunity conversion
        if inp.demo_to_opp_conversion_rate_pct < 0.30:
            score += 30.0
        elif inp.demo_to_opp_conversion_rate_pct < 0.50:
            score += 15.0

        # Zero qualified opps despite meaningful activity
        if inp.qualified_opps_created == 0 and inp.activities_total_count >= 30:
            score += 15.0

        return min(score, 100.0)

    def _pipeline_coverage_score(self, inp: PipelineEfficiencyInput) -> float:
        score = 0.0

        # Coverage vs. target
        if inp.pipeline_target_usd > 0:
            coverage = inp.pipeline_generated_usd / inp.pipeline_target_usd
            if coverage < 0.50:
                score += 40.0
            elif coverage < 0.75:
                score += 25.0
            elif coverage < 1.0:
                score += 10.0

        # Period-over-period pipeline decay
        if inp.prior_period_pipeline_generated_usd > 0:
            delta = (inp.prior_period_pipeline_generated_usd - inp.pipeline_generated_usd) / inp.prior_period_pipeline_generated_usd
            if delta >= 0.30:
                score += 30.0
            elif delta >= 0.15:
                score += 15.0

        # Zero qualified opps when target is non-zero
        if inp.qualified_opps_created == 0 and inp.pipeline_target_usd > 0:
            score += 30.0

        return min(score, 100.0)

    def _activity_mix_score(self, inp: PipelineEfficiencyInput) -> float:
        score = 0.0

        # High variance = over-reliance on single channel
        if inp.activity_mix_variance_score >= 70.0:
            score += 40.0
        elif inp.activity_mix_variance_score >= 50.0:
            score += 22.0
        elif inp.activity_mix_variance_score >= 30.0:
            score += 10.0

        # Cold-call tunnel vision
        if inp.activities_total_count > 0:
            cold_call_share = inp.cold_calls_made / inp.activities_total_count
            if cold_call_share >= 0.80:
                score += 20.0
            elif cold_call_share >= 0.65:
                score += 10.0

        # Referral engine failure (asks but never receives)
        if inp.referrals_requested >= 5 and inp.referrals_received == 0:
            score += 20.0
        elif inp.referrals_requested >= 3 and inp.referrals_received == 0:
            score += 10.0

        # Unlogged activities distort the mix picture
        if inp.crm_activity_logging_rate_pct < 0.40:
            score += 15.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: PipelineEfficiencyInput,
                         volume: float, conversion: float,
                         coverage: float, mix: float) -> EfficiencyPattern:
        # Priority: activity_decay > pipeline_coverage_gap > poor_conversion
        #           > activity_channel_overreliance > low_activity_volume > none
        if inp.prior_period_pipeline_generated_usd > 0:
            decay = (inp.prior_period_pipeline_generated_usd - inp.pipeline_generated_usd) / inp.prior_period_pipeline_generated_usd
            if decay >= 0.30 and conversion >= 30:
                return EfficiencyPattern.activity_decay

        if inp.pipeline_target_usd > 0 and inp.pipeline_generated_usd < inp.pipeline_target_usd * 0.50:
            return EfficiencyPattern.pipeline_coverage_gap

        if conversion >= 35 and inp.demo_to_opp_conversion_rate_pct < 0.30:
            return EfficiencyPattern.poor_conversion

        if mix >= 30 and inp.activity_mix_variance_score >= 50:
            return EfficiencyPattern.activity_channel_overreliance

        if volume >= 30 and inp.activities_total_count < 100:
            return EfficiencyPattern.low_activity_volume

        return EfficiencyPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> EfficiencyRisk:
        if composite >= 60:
            return EfficiencyRisk.critical
        if composite >= 40:
            return EfficiencyRisk.high
        if composite >= 20:
            return EfficiencyRisk.moderate
        return EfficiencyRisk.low

    def _severity(self, composite: float) -> EfficiencySeverity:
        if composite >= 60:
            return EfficiencySeverity.critical
        if composite >= 40:
            return EfficiencySeverity.degraded
        if composite >= 20:
            return EfficiencySeverity.underperforming
        return EfficiencySeverity.healthy

    def _action(self, risk: EfficiencyRisk, pattern: EfficiencyPattern) -> EfficiencyAction:
        if risk == EfficiencyRisk.critical:
            return EfficiencyAction.performance_improvement_plan
        if risk == EfficiencyRisk.high:
            if pattern == EfficiencyPattern.low_activity_volume:
                return EfficiencyAction.pipeline_blitz
            return EfficiencyAction.conversion_coaching
        if risk == EfficiencyRisk.moderate:
            if pattern == EfficiencyPattern.activity_channel_overreliance:
                return EfficiencyAction.channel_diversification
            return EfficiencyAction.activity_increase
        return EfficiencyAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _is_pipeline_at_risk(self, composite: float, inp: PipelineEfficiencyInput) -> bool:
        return (
            composite >= 40
            or (inp.pipeline_target_usd > 0 and inp.pipeline_generated_usd < inp.pipeline_target_usd * 0.75)
            or inp.qualified_opps_created == 0
        )

    def _requires_activity_intervention(self, composite: float, inp: PipelineEfficiencyInput) -> bool:
        return (
            composite >= 30
            or inp.activities_total_count < 50
            or inp.cold_call_connect_rate_pct < 0.05
        )

    # ------------------------------------------------------------------
    # Pipeline gap estimate
    # ------------------------------------------------------------------

    def _estimated_pipeline_gap(self, inp: PipelineEfficiencyInput, composite: float) -> float:
        gap = max(inp.pipeline_target_usd - inp.pipeline_generated_usd, 0.0)
        return round(gap * (composite / 100.0), 2)

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: PipelineEfficiencyInput,
                pattern: EfficiencyPattern, composite: float) -> str:
        if pattern == EfficiencyPattern.none and composite < 20:
            return "Pipeline generation efficiency within targets"
        parts: list[str] = []
        if inp.activities_total_count < 100:
            parts.append(f"{inp.activities_total_count} total activities")
        if inp.demo_to_opp_conversion_rate_pct < 0.30:
            parts.append(f"{inp.demo_to_opp_conversion_rate_pct*100:.0f}% demo-to-opp rate")
        if inp.pipeline_target_usd > 0:
            coverage = inp.pipeline_generated_usd / inp.pipeline_target_usd
            if coverage < 1.0:
                parts.append(f"{coverage*100:.0f}% pipeline coverage")
        if inp.cold_call_connect_rate_pct < 0.15:
            parts.append(f"{inp.cold_call_connect_rate_pct*100:.0f}% call connect rate")
        label = pattern.value.replace("_", " ") if pattern != EfficiencyPattern.none else "Efficiency risk"
        summary = " — ".join(parts) if parts else "pipeline efficiency degraded"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: PipelineEfficiencyInput) -> PipelineEfficiencyResult:
        volume    = round(self._activity_volume_score(inp), 1)
        conversion = round(self._conversion_efficiency_score(inp), 1)
        coverage  = round(self._pipeline_coverage_score(inp), 1)
        mix       = round(self._activity_mix_score(inp), 1)

        composite = round(volume * 0.25 + conversion * 0.35 + coverage * 0.25 + mix * 0.15, 1)
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, volume, conversion, coverage, mix)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        is_par = self._is_pipeline_at_risk(composite, inp)
        is_rai = self._requires_activity_intervention(composite, inp)
        gap    = self._estimated_pipeline_gap(inp, composite)
        signal = self._signal(inp, pattern, composite)

        result = PipelineEfficiencyResult(
            rep_id=inp.rep_id,
            region=inp.region,
            efficiency_risk=risk,
            efficiency_pattern=pattern,
            efficiency_severity=severity,
            recommended_action=action,
            activity_volume_score=volume,
            conversion_efficiency_score=conversion,
            pipeline_coverage_score=coverage,
            activity_mix_score=mix,
            pipeline_efficiency_composite=composite,
            is_pipeline_at_risk=is_par,
            requires_activity_intervention=is_rai,
            estimated_pipeline_gap_usd=gap,
            efficiency_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[PipelineEfficiencyInput]) -> list[PipelineEfficiencyResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_pipeline_efficiency_composite": 0.0,
                "pipeline_at_risk_count": 0,
                "activity_intervention_count": 0,
                "avg_activity_volume_score": 0.0,
                "avg_conversion_efficiency_score": 0.0,
                "avg_pipeline_coverage_score": 0.0,
                "avg_activity_mix_score": 0.0,
                "total_estimated_pipeline_gap_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_vol = total_conv = total_cov = total_mix = total_gap = 0.0

        for r in self._results:
            risk_counts[r.efficiency_risk.value]       = risk_counts.get(r.efficiency_risk.value, 0) + 1
            pattern_counts[r.efficiency_pattern.value] = pattern_counts.get(r.efficiency_pattern.value, 0) + 1
            severity_counts[r.efficiency_severity.value] = severity_counts.get(r.efficiency_severity.value, 0) + 1
            action_counts[r.recommended_action.value]  = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.pipeline_efficiency_composite
            total_vol  += r.activity_volume_score
            total_conv += r.conversion_efficiency_score
            total_cov  += r.pipeline_coverage_score
            total_mix  += r.activity_mix_score
            total_gap  += r.estimated_pipeline_gap_usd

        n = len(self._results)

        return {
            "total":                              n,
            "risk_counts":                        risk_counts,
            "pattern_counts":                     pattern_counts,
            "severity_counts":                    severity_counts,
            "action_counts":                      action_counts,
            "avg_pipeline_efficiency_composite":  round(total_comp / n, 1),
            "pipeline_at_risk_count":             sum(1 for r in self._results if r.is_pipeline_at_risk),
            "activity_intervention_count":        sum(1 for r in self._results if r.requires_activity_intervention),
            "avg_activity_volume_score":          round(total_vol / n, 1),
            "avg_conversion_efficiency_score":    round(total_conv / n, 1),
            "avg_pipeline_coverage_score":        round(total_cov / n, 1),
            "avg_activity_mix_score":             round(total_mix / n, 1),
            "total_estimated_pipeline_gap_usd":   round(total_gap, 2),
        }
