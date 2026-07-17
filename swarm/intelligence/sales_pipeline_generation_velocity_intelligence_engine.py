from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional


class PipelineRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class PipelinePattern(str, Enum):
    none                  = "none"
    burst_and_fade        = "burst_and_fade"
    reactive_only         = "reactive_only"
    slow_starter          = "slow_starter"
    territory_exhaustion  = "territory_exhaustion"
    channel_dependency    = "channel_dependency"


class PipelineSeverity(str, Enum):
    generating = "generating"
    adequate   = "adequate"
    sluggish   = "sluggish"
    stalled    = "stalled"


class PipelineAction(str, Enum):
    no_action                      = "no_action"
    prospecting_cadence_coaching   = "prospecting_cadence_coaching"
    icp_targeting_coaching         = "icp_targeting_coaching"
    channel_diversification_coaching = "channel_diversification_coaching"
    pipeline_generation_coaching   = "pipeline_generation_coaching"
    pipeline_generation_intervention = "pipeline_generation_intervention"
    pipeline_reset_intervention    = "pipeline_reset_intervention"


@dataclass
class PipelineInput:
    rep_id:                             str
    region:                             str
    evaluation_period_id:               str
    outreach_attempts_per_week_avg:     float   # e.g. 30.0
    outreach_to_connect_rate_pct:       float   # 0-1
    connect_to_meeting_rate_pct:        float   # 0-1
    meeting_to_opportunity_rate_pct:    float   # 0-1
    new_opportunities_per_week_avg:     float   # e.g. 2.0
    pipeline_coverage_ratio:            float   # e.g. 3.5x
    days_to_first_opportunity_avg:      float   # days
    icp_targeted_outreach_pct:          float   # 0-1
    multi_channel_outreach_pct:         float   # 0-1
    referral_sourced_pipeline_pct:      float   # 0-1
    stale_opportunity_rate_pct:         float   # 0-1
    opportunity_no_activity_14d_pct:    float   # 0-1
    consecutive_low_pipeline_weeks:     int     # count
    territory_coverage_depth_pct:       float   # 0-1
    avg_opportunity_age_at_stage1_days: float   # days
    inbound_conversion_rate_pct:        float   # 0-1
    pipeline_created_per_week_usd:      float   # dollars
    total_outreach_attempts:            int     # count
    avg_opportunity_value_usd:          float   # dollars


@dataclass
class PipelineResult:
    rep_id:                              str
    region:                              str
    pipeline_risk:                       PipelineRisk
    pipeline_pattern:                    PipelinePattern
    pipeline_severity:                   PipelineSeverity
    recommended_action:                  PipelineAction
    generation_rate_score:               float
    pipeline_volume_score:               float
    prospecting_quality_score:           float
    consistency_score:                   float
    pipeline_composite:                  float
    has_pipeline_gap:                    bool
    requires_pipeline_coaching:          bool
    estimated_pipeline_shortfall_usd:    float
    pipeline_signal:                     str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "pipeline_risk":                    self.pipeline_risk.value,
            "pipeline_pattern":                 self.pipeline_pattern.value,
            "pipeline_severity":                self.pipeline_severity.value,
            "recommended_action":               self.recommended_action.value,
            "generation_rate_score":            self.generation_rate_score,
            "pipeline_volume_score":            self.pipeline_volume_score,
            "prospecting_quality_score":        self.prospecting_quality_score,
            "consistency_score":                self.consistency_score,
            "pipeline_composite":               self.pipeline_composite,
            "has_pipeline_gap":                 self.has_pipeline_gap,
            "requires_pipeline_coaching":       self.requires_pipeline_coaching,
            "estimated_pipeline_shortfall_usd": self.estimated_pipeline_shortfall_usd,
            "pipeline_signal":                  self.pipeline_signal,
        }


class SalesPipelineGenerationVelocityIntelligenceEngine:
    """Detects per-rep pipeline generation velocity gaps and patterns."""

    def __init__(self) -> None:
        self._results: List[PipelineResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────

    def _generation_rate_score(self, inp: PipelineInput) -> float:
        s = 0.0
        # outreach_to_connect_rate_pct: low rate = high risk
        if   inp.outreach_to_connect_rate_pct <= 0.05: s += 40
        elif inp.outreach_to_connect_rate_pct <= 0.10: s += 22
        elif inp.outreach_to_connect_rate_pct <= 0.18: s += 8
        # connect_to_meeting_rate_pct
        if   inp.connect_to_meeting_rate_pct  <= 0.15: s += 35
        elif inp.connect_to_meeting_rate_pct  <= 0.28: s += 18
        # meeting_to_opportunity_rate_pct
        if   inp.meeting_to_opportunity_rate_pct <= 0.20: s += 25
        elif inp.meeting_to_opportunity_rate_pct <= 0.38: s += 12
        return min(s, 100.0)

    def _pipeline_volume_score(self, inp: PipelineInput) -> float:
        s = 0.0
        # new_opportunities_per_week_avg
        if   inp.new_opportunities_per_week_avg <= 0.5:  s += 40
        elif inp.new_opportunities_per_week_avg <= 1.0:  s += 22
        elif inp.new_opportunities_per_week_avg <= 1.8:  s += 8
        # pipeline_coverage_ratio
        if   inp.pipeline_coverage_ratio <= 1.5: s += 35
        elif inp.pipeline_coverage_ratio <= 2.5: s += 18
        # pipeline_created_per_week_usd
        if   inp.pipeline_created_per_week_usd <= 5_000:   s += 25
        elif inp.pipeline_created_per_week_usd <= 15_000:  s += 12
        return min(s, 100.0)

    def _prospecting_quality_score(self, inp: PipelineInput) -> float:
        s = 0.0
        # icp_targeted_outreach_pct
        if   inp.icp_targeted_outreach_pct <= 0.30: s += 45
        elif inp.icp_targeted_outreach_pct <= 0.50: s += 25
        elif inp.icp_targeted_outreach_pct <= 0.65: s += 10
        # multi_channel_outreach_pct
        if   inp.multi_channel_outreach_pct <= 0.20: s += 30
        elif inp.multi_channel_outreach_pct <= 0.40: s += 15
        # territory_coverage_depth_pct
        if   inp.territory_coverage_depth_pct <= 0.15: s += 25
        elif inp.territory_coverage_depth_pct <= 0.35: s += 12
        return min(s, 100.0)

    def _consistency_score(self, inp: PipelineInput) -> float:
        s = 0.0
        # consecutive_low_pipeline_weeks
        if   inp.consecutive_low_pipeline_weeks >= 6:  s += 40
        elif inp.consecutive_low_pipeline_weeks >= 3:  s += 22
        elif inp.consecutive_low_pipeline_weeks >= 1:  s += 8
        # opportunity_no_activity_14d_pct
        if   inp.opportunity_no_activity_14d_pct >= 0.50: s += 35
        elif inp.opportunity_no_activity_14d_pct >= 0.30: s += 18
        # stale_opportunity_rate_pct
        if   inp.stale_opportunity_rate_pct >= 0.40: s += 25
        elif inp.stale_opportunity_rate_pct >= 0.20: s += 12
        return min(s, 100.0)

    # ── composite ─────────────────────────────────────────────────────────

    def _composite(self, gr: float, pv: float, pq: float, cs: float) -> float:
        return min(round(gr * 0.35 + pv * 0.30 + pq * 0.20 + cs * 0.15, 2), 100.0)

    # ── pattern ───────────────────────────────────────────────────────────

    def _pattern(self, inp: PipelineInput) -> PipelinePattern:
        if inp.consecutive_low_pipeline_weeks >= 4 and inp.new_opportunities_per_week_avg <= 0.5:
            return PipelinePattern.burst_and_fade
        if inp.inbound_conversion_rate_pct >= 0.70 and inp.outreach_attempts_per_week_avg <= 10:
            return PipelinePattern.reactive_only
        if inp.days_to_first_opportunity_avg >= 45 and inp.new_opportunities_per_week_avg <= 1.0:
            return PipelinePattern.slow_starter
        if inp.territory_coverage_depth_pct <= 0.20 and inp.icp_targeted_outreach_pct <= 0.40:
            return PipelinePattern.territory_exhaustion
        if inp.multi_channel_outreach_pct <= 0.20 and inp.referral_sourced_pipeline_pct <= 0.10:
            return PipelinePattern.channel_dependency
        return PipelinePattern.none

    # ── thresholds ────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> PipelineRisk:
        if   composite >= 60: return PipelineRisk.critical
        elif composite >= 40: return PipelineRisk.high
        elif composite >= 20: return PipelineRisk.moderate
        return PipelineRisk.low

    def _severity(self, composite: float) -> PipelineSeverity:
        if   composite >= 60: return PipelineSeverity.stalled
        elif composite >= 40: return PipelineSeverity.sluggish
        elif composite >= 20: return PipelineSeverity.adequate
        return PipelineSeverity.generating

    def _action(self, risk: PipelineRisk, pattern: PipelinePattern) -> PipelineAction:
        if risk == PipelineRisk.critical:
            if pattern == PipelinePattern.burst_and_fade:
                return PipelineAction.pipeline_reset_intervention
            if pattern == PipelinePattern.reactive_only:
                return PipelineAction.pipeline_generation_intervention
            return PipelineAction.pipeline_reset_intervention
        if risk == PipelineRisk.high:
            if pattern == PipelinePattern.slow_starter:
                return PipelineAction.prospecting_cadence_coaching
            if pattern == PipelinePattern.channel_dependency:
                return PipelineAction.channel_diversification_coaching
            if pattern == PipelinePattern.territory_exhaustion:
                return PipelineAction.icp_targeting_coaching
            return PipelineAction.pipeline_generation_coaching
        if risk == PipelineRisk.moderate:
            return PipelineAction.pipeline_generation_coaching
        return PipelineAction.no_action

    # ── flags ─────────────────────────────────────────────────────────────

    def _has_gap(self, inp: PipelineInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.pipeline_coverage_ratio <= 2.0
            or inp.new_opportunities_per_week_avg <= 0.8
        )

    def _requires_coaching(self, inp: PipelineInput, composite: float) -> bool:
        return (
            composite >= 30
            or inp.outreach_to_connect_rate_pct <= 0.12
            or inp.consecutive_low_pipeline_weeks >= 2
        )

    # ── dollar impact ─────────────────────────────────────────────────────

    def _shortfall(self, inp: PipelineInput, composite: float) -> float:
        target_coverage = 3.0
        shortfall_ratio = max(0.0, target_coverage - inp.pipeline_coverage_ratio) / target_coverage
        return round(
            inp.total_outreach_attempts * inp.avg_opportunity_value_usd
            * shortfall_ratio * (composite / 100),
            2,
        )

    # ── signal ────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        PipelinePattern.burst_and_fade:       "Burst and fade",
        PipelinePattern.reactive_only:        "Reactive only",
        PipelinePattern.slow_starter:         "Slow starter",
        PipelinePattern.territory_exhaustion: "Territory exhaustion",
        PipelinePattern.channel_dependency:   "Channel dependency",
    }

    def _signal(self, inp: PipelineInput, pattern: PipelinePattern, composite: float) -> str:
        if composite < 20:
            return (
                "Pipeline generation healthy — outreach conversion, volume, "
                "and prospecting quality within benchmarks"
            )
        label = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        conn_pct   = round(inp.outreach_to_connect_rate_pct * 100)
        opp_pw     = f"{inp.new_opportunities_per_week_avg:.1f}"
        low_wks    = inp.consecutive_low_pipeline_weeks
        comp_int   = round(composite)
        return (
            f"{label} — {conn_pct}% outreach-to-connect — "
            f"{opp_pw} new opps/week — {low_wks} consecutive low-pipeline weeks — "
            f"composite {comp_int}"
        )

    # ── public API ────────────────────────────────────────────────────────

    def assess(self, inp: PipelineInput) -> PipelineResult:
        gr  = self._generation_rate_score(inp)
        pv  = self._pipeline_volume_score(inp)
        pq  = self._prospecting_quality_score(inp)
        cs  = self._consistency_score(inp)
        comp = self._composite(gr, pv, pq, cs)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = PipelineResult(
            rep_id                           = inp.rep_id,
            region                           = inp.region,
            pipeline_risk                    = risk,
            pipeline_pattern                 = pattern,
            pipeline_severity                = severity,
            recommended_action               = action,
            generation_rate_score            = gr,
            pipeline_volume_score            = pv,
            prospecting_quality_score        = pq,
            consistency_score                = cs,
            pipeline_composite               = comp,
            has_pipeline_gap                 = self._has_gap(inp, comp),
            requires_pipeline_coaching       = self._requires_coaching(inp, comp),
            estimated_pipeline_shortfall_usd = self._shortfall(inp, comp),
            pipeline_signal                  = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[PipelineInput]) -> List[PipelineResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_pipeline_composite": 0.0,
                "pipeline_gap_count": 0,
                "coaching_count": 0,
                "avg_generation_rate_score": 0.0,
                "avg_pipeline_volume_score": 0.0,
                "avg_prospecting_quality_score": 0.0,
                "avg_consistency_score": 0.0,
                "total_estimated_pipeline_shortfall_usd": 0.0,
            }

        risk_counts: Dict[str, int]     = {}
        pattern_counts: Dict[str, int]  = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int]   = {}
        total_comp = total_gr = total_pv = total_pq = total_cs = total_short = 0.0
        gap_count = coaching_count = 0

        for r in self._results:
            risk_counts[r.pipeline_risk.value]         = risk_counts.get(r.pipeline_risk.value, 0) + 1
            pattern_counts[r.pipeline_pattern.value]   = pattern_counts.get(r.pipeline_pattern.value, 0) + 1
            severity_counts[r.pipeline_severity.value] = severity_counts.get(r.pipeline_severity.value, 0) + 1
            action_counts[r.recommended_action.value]  = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp  += r.pipeline_composite
            total_gr    += r.generation_rate_score
            total_pv    += r.pipeline_volume_score
            total_pq    += r.prospecting_quality_score
            total_cs    += r.consistency_score
            total_short += r.estimated_pipeline_shortfall_usd
            if r.has_pipeline_gap:       gap_count      += 1
            if r.requires_pipeline_coaching: coaching_count += 1

        n = len(self._results)
        return {
            "total":                                   n,
            "risk_counts":                             risk_counts,
            "pattern_counts":                          pattern_counts,
            "severity_counts":                         severity_counts,
            "action_counts":                           action_counts,
            "avg_pipeline_composite":                  round(total_comp / n, 1),
            "pipeline_gap_count":                      gap_count,
            "coaching_count":                          coaching_count,
            "avg_generation_rate_score":               round(total_gr / n, 1),
            "avg_pipeline_volume_score":               round(total_pv / n, 1),
            "avg_prospecting_quality_score":           round(total_pq / n, 1),
            "avg_consistency_score":                   round(total_cs / n, 1),
            "total_estimated_pipeline_shortfall_usd":  round(total_short, 2),
        }
