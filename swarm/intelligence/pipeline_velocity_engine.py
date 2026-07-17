"""
Pipeline Velocity Intelligence Engine

Mesure la vélocité du pipeline commercial : vitesse d'avancement des deals,
points de blocage par stage, durée des cycles et prédiction de clôture.
"""

from __future__ import annotations

from dataclasses import dataclass, fields as dc_fields
from enum import Enum
from typing import Optional


class VelocityRisk(str, Enum):
    low = "low"
    moderate = "moderate"
    high = "high"
    critical = "critical"


class VelocityPattern(str, Enum):
    none = "none"
    top_of_funnel_stall = "top_of_funnel_stall"
    qualification_bottleneck = "qualification_bottleneck"
    proposal_graveyard = "proposal_graveyard"
    late_stage_paralysis = "late_stage_paralysis"
    deal_evaporation = "deal_evaporation"
    velocity_collapse = "velocity_collapse"


class VelocitySeverity(str, Enum):
    flowing = "flowing"
    slowing = "slowing"
    stalling = "stalling"
    blocked = "blocked"


class VelocityAction(str, Enum):
    maintain = "maintain"
    accelerate_qualification = "accelerate_qualification"
    unstick_proposals = "unstick_proposals"
    close_plan_review = "close_plan_review"
    pipeline_purge = "pipeline_purge"
    full_velocity_intervention = "full_velocity_intervention"


@dataclass
class PipelineVelocityInput:
    total_pipeline_value: float = 1000000.0
    deals_in_pipeline: int = 40
    avg_deal_value: float = 25000.0
    avg_sales_cycle_days: float = 60.0
    win_rate_pct: float = 30.0
    stage_1_count: int = 15
    stage_2_count: int = 10
    stage_3_count: int = 8
    stage_4_count: int = 5
    stage_5_count: int = 2
    stage_1_avg_days: float = 12.0
    stage_2_avg_days: float = 18.0
    stage_3_avg_days: float = 20.0
    stage_4_avg_days: float = 25.0
    deals_no_activity_14d: int = 8
    deals_past_expected_close: int = 6
    new_deals_added_30d: int = 12
    deals_closed_30d: int = 5
    deals_lost_30d: int = 4
    pipeline_coverage_ratio: float = 2.5
    quota: float = 400000.0
    historical_cycle_benchmark: float = 55.0


@dataclass
class PipelineVelocityResult:
    composite_score: float
    risk: VelocityRisk
    pattern: VelocityPattern
    severity: VelocitySeverity
    action: VelocityAction
    velocity_index: float
    stage_flow_score: float
    activity_score: float
    coverage_score: float
    pipeline_velocity_value: float
    bottleneck_stage: int
    stale_deal_pct: float
    projected_close_30d: float
    signal: str
    deals_at_risk_count: int

    def to_dict(self) -> dict:
        return {
            "composite_score": self.composite_score,
            "risk": self.risk.value,
            "pattern": self.pattern.value,
            "severity": self.severity.value,
            "action": self.action.value,
            "velocity_index": self.velocity_index,
            "stage_flow_score": self.stage_flow_score,
            "activity_score": self.activity_score,
            "coverage_score": self.coverage_score,
            "pipeline_velocity_value": self.pipeline_velocity_value,
            "bottleneck_stage": self.bottleneck_stage,
            "stale_deal_pct": self.stale_deal_pct,
            "projected_close_30d": self.projected_close_30d,
            "signal": self.signal,
            "deals_at_risk_count": self.deals_at_risk_count,
        }


class PipelineVelocityEngine:

    def _velocity_index(self, inp: PipelineVelocityInput) -> float:
        pv = (inp.deals_in_pipeline * inp.avg_deal_value * inp.win_rate_pct / 100) / max(inp.avg_sales_cycle_days, 1)
        benchmark = (inp.deals_in_pipeline * inp.avg_deal_value * 0.30) / max(inp.historical_cycle_benchmark, 1)
        if benchmark == 0:
            return 50.0
        ratio = pv / benchmark
        raw = min(ratio, 2.0) * 50
        return min(max(round(raw, 1), 0.0), 100.0)

    def _stage_flow_score(self, inp: PipelineVelocityInput) -> float:
        total = inp.deals_in_pipeline or 1
        benchmark_stage_days = [inp.historical_cycle_benchmark / 5] * 5
        stage_days = [inp.stage_1_avg_days, inp.stage_2_avg_days, inp.stage_3_avg_days, inp.stage_4_avg_days, inp.stage_4_avg_days]
        over_penalties = sum(
            max(0, (actual - bench) / max(bench, 1) * 20)
            for actual, bench in zip(stage_days, benchmark_stage_days)
        )
        raw = 100 - min(over_penalties, 60)
        past_close_penalty = min(inp.deals_past_expected_close / total * 50, 40)
        return min(max(round(raw - past_close_penalty, 1), 0.0), 100.0)

    def _activity_score(self, inp: PipelineVelocityInput) -> float:
        total = inp.deals_in_pipeline or 1
        stale_ratio = inp.deals_no_activity_14d / total
        new_deal_flow = min(inp.new_deals_added_30d / max(total * 0.2, 1), 1.0) * 30
        close_flow = min(inp.deals_closed_30d / max(total * 0.1, 1), 1.0) * 20
        raw = 100 - (stale_ratio * 70) + new_deal_flow + close_flow - 50
        return min(max(round(raw, 1), 0.0), 100.0)

    def _coverage_score(self, inp: PipelineVelocityInput) -> float:
        if inp.quota == 0:
            return 50.0
        coverage = inp.pipeline_coverage_ratio
        if coverage >= 3.0:
            raw = 100.0
        elif coverage >= 2.0:
            raw = 75.0 + (coverage - 2.0) * 25
        elif coverage >= 1.0:
            raw = (coverage - 1.0) * 75
        else:
            raw = 0.0
        return min(max(round(raw, 1), 0.0), 100.0)

    def _composite(self, v: float, s: float, a: float, c: float) -> float:
        return min(round(v * 0.30 + s * 0.30 + a * 0.25 + c * 0.15, 1), 100.0)

    def _risk_level(self, score: float) -> VelocityRisk:
        if score >= 70:
            return VelocityRisk.low
        if score >= 50:
            return VelocityRisk.moderate
        if score >= 30:
            return VelocityRisk.high
        return VelocityRisk.critical

    def _severity(self, risk: VelocityRisk) -> VelocitySeverity:
        return {
            VelocityRisk.low: VelocitySeverity.flowing,
            VelocityRisk.moderate: VelocitySeverity.slowing,
            VelocityRisk.high: VelocitySeverity.stalling,
            VelocityRisk.critical: VelocitySeverity.blocked,
        }[risk]

    def _bottleneck_stage(self, inp: PipelineVelocityInput) -> int:
        benchmark = inp.historical_cycle_benchmark / 5
        stage_days = [
            (1, inp.stage_1_avg_days),
            (2, inp.stage_2_avg_days),
            (3, inp.stage_3_avg_days),
            (4, inp.stage_4_avg_days),
        ]
        worst = max(stage_days, key=lambda x: x[1] / max(benchmark, 1))
        return worst[0]

    def _detect_pattern(self, inp: PipelineVelocityInput, bottleneck: int) -> VelocityPattern:
        total = inp.deals_in_pipeline or 1
        stale_ratio = inp.deals_no_activity_14d / total

        if stale_ratio > 0.50:
            return VelocityPattern.velocity_collapse
        if inp.pipeline_coverage_ratio < 1.0:
            return VelocityPattern.deal_evaporation
        if bottleneck == 1 and inp.stage_1_avg_days > inp.historical_cycle_benchmark * 0.30:
            return VelocityPattern.top_of_funnel_stall
        if bottleneck == 2 and inp.stage_2_avg_days > inp.historical_cycle_benchmark * 0.30:
            return VelocityPattern.qualification_bottleneck
        if bottleneck == 3 and inp.stage_3_avg_days > inp.historical_cycle_benchmark * 0.35:
            return VelocityPattern.proposal_graveyard
        if inp.deals_past_expected_close / total > 0.20:
            return VelocityPattern.late_stage_paralysis
        return VelocityPattern.none

    def _action(self, pattern: VelocityPattern) -> VelocityAction:
        mapping = {
            VelocityPattern.velocity_collapse: VelocityAction.full_velocity_intervention,
            VelocityPattern.deal_evaporation: VelocityAction.pipeline_purge,
            VelocityPattern.top_of_funnel_stall: VelocityAction.accelerate_qualification,
            VelocityPattern.qualification_bottleneck: VelocityAction.accelerate_qualification,
            VelocityPattern.proposal_graveyard: VelocityAction.unstick_proposals,
            VelocityPattern.late_stage_paralysis: VelocityAction.close_plan_review,
            VelocityPattern.none: VelocityAction.maintain,
        }
        return mapping[pattern]

    def _pipeline_velocity_value(self, inp: PipelineVelocityInput) -> float:
        return round(
            (inp.deals_in_pipeline * inp.avg_deal_value * inp.win_rate_pct / 100) / max(inp.avg_sales_cycle_days / 30, 1),
            2,
        )

    def _projected_close_30d(self, inp: PipelineVelocityInput) -> float:
        monthly_rate = inp.deals_closed_30d * inp.avg_deal_value
        return round(monthly_rate, 2)

    def _signal(self, risk: VelocityRisk, pattern: VelocityPattern) -> str:
        if risk == VelocityRisk.low and pattern == VelocityPattern.none:
            return "Pipeline velocity healthy — deals flowing through stages at or above benchmark speed"
        signals = {
            VelocityPattern.velocity_collapse: ">50% of deals are stale — full pipeline intervention required immediately",
            VelocityPattern.deal_evaporation: "Pipeline coverage below 1x quota — critical sourcing emergency",
            VelocityPattern.top_of_funnel_stall: "Stage 1 is the bottleneck — outreach and qualification acceleration needed",
            VelocityPattern.qualification_bottleneck: "Deals stalling at qualification — improve BANT rigor and ICP definition",
            VelocityPattern.proposal_graveyard: "Proposals not moving forward — follow-up cadence and value reinforcement needed",
            VelocityPattern.late_stage_paralysis: f"Late-stage deals past close date — mutual close plan activation required",
            VelocityPattern.none: f"Pipeline velocity {risk.value} risk — monitor stage progression",
        }
        return signals.get(pattern, "Pipeline velocity requires attention")

    def assess(self, inp: PipelineVelocityInput) -> PipelineVelocityResult:
        v = self._velocity_index(inp)
        s = self._stage_flow_score(inp)
        a = self._activity_score(inp)
        c = self._coverage_score(inp)
        composite = self._composite(v, s, a, c)
        risk = self._risk_level(composite)
        severity = self._severity(risk)
        bottleneck = self._bottleneck_stage(inp)
        pattern = self._detect_pattern(inp, bottleneck)
        action = self._action(pattern)

        total = inp.deals_in_pipeline or 1
        stale_pct = round(inp.deals_no_activity_14d / total * 100, 1)
        at_risk = inp.deals_no_activity_14d + inp.deals_past_expected_close

        return PipelineVelocityResult(
            composite_score=composite,
            risk=risk,
            pattern=pattern,
            severity=severity,
            action=action,
            velocity_index=v,
            stage_flow_score=s,
            activity_score=a,
            coverage_score=c,
            pipeline_velocity_value=self._pipeline_velocity_value(inp),
            bottleneck_stage=bottleneck,
            stale_deal_pct=stale_pct,
            projected_close_30d=self._projected_close_30d(inp),
            signal=self._signal(risk, pattern),
            deals_at_risk_count=at_risk,
        )

    def batch(self, inputs: list[PipelineVelocityInput]) -> list[PipelineVelocityResult]:
        return [self.assess(inp) for inp in inputs]

    def summary(self, results: list[PipelineVelocityResult]) -> dict:
        if not results:
            return {}
        scores = [r.composite_score for r in results]
        return {
            "total_pipelines": len(results),
            "avg_composite_score": round(sum(scores) / len(scores), 1),
            "critical_count": sum(1 for r in results if r.risk == VelocityRisk.critical),
            "high_risk_count": sum(1 for r in results if r.risk == VelocityRisk.high),
            "top_pattern": max(set(r.pattern.value for r in results), key=lambda p: sum(1 for r in results if r.pattern.value == p)),
            "total_deals_at_risk": sum(r.deals_at_risk_count for r in results),
            "avg_stale_deal_pct": round(sum(r.stale_deal_pct for r in results) / len(results), 1),
            "total_projected_close_30d": round(sum(r.projected_close_30d for r in results), 2),
            "stall_count": sum(1 for r in results if r.severity in (VelocitySeverity.stalling, VelocitySeverity.blocked)),
            "min_score": min(scores),
            "max_score": max(scores),
            "low_risk_pct": round(sum(1 for r in results if r.risk == VelocityRisk.low) / len(results) * 100, 1),
            "avg_velocity_index": round(sum(r.velocity_index for r in results) / len(results), 1),
        }
