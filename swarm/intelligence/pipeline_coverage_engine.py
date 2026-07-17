from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CoverageStatus(str, Enum):
    OVER_COVERED    = "over_covered"
    ADEQUATE        = "adequate"
    UNDER_COVERED   = "under_covered"
    CRITICAL_GAP    = "critical_gap"


class GapSeverity(str, Enum):
    NONE     = "none"
    LOW      = "low"
    MEDIUM   = "medium"
    HIGH     = "high"
    CRITICAL = "critical"


class PipelineQuality(str, Enum):
    EXCELLENT = "excellent"
    GOOD      = "good"
    FAIR      = "fair"
    POOR      = "poor"


class CoverageAction(str, Enum):
    MAINTAIN          = "maintain"
    ACCELERATE_EXISTING = "accelerate_existing"
    GENERATE_PIPELINE = "generate_pipeline"
    REALLOCATE        = "reallocate"
    EXPAND_UPMARKET   = "expand_upmarket"
    STRATEGIC_REVIEW  = "strategic_review"


@dataclass
class PipelineCoverageInput:
    team_id:               str
    region:                str
    segment:               str
    manager_id:            str
    quota_remaining:       float    # remaining quota for the period
    current_pipeline:      float    # total open pipeline value
    weighted_pipeline:     float    # probability-weighted pipeline
    stage1_value:          float    # early prospecting
    stage2_value:          float    # qualified
    stage3_value:          float    # solution/demo
    stage4_value:          float    # proposal/negotiation
    stage5_value:          float    # verbal close / contract
    historical_win_rate:   float    # team win rate 0–100
    avg_deal_size:         float
    avg_sales_cycle_days:  int
    days_remaining:        int      # days left in period
    pipeline_added_qtd:    float    # new pipe created this period
    churned_pipeline_qtd:  float    # deals lost/removed this period
    stalled_deal_count:    int      # deals with no activity >14 days
    avg_deal_health:       float    # avg health index 0–100
    competitive_deal_pct:  float    # % of deals with competitor 0–100


@dataclass
class PipelineCoverageResult:
    team_id:                str
    region:                 str
    coverage_status:        CoverageStatus
    gap_severity:           GapSeverity
    pipeline_quality:       PipelineQuality
    coverage_action:        CoverageAction
    coverage_ratio:         float    # current_pipeline / quota_remaining
    weighted_coverage_ratio: float   # weighted_pipeline / quota_remaining
    gap_to_quota:           float    # quota_remaining - weighted_pipeline (0 if covered)
    pipeline_velocity:      float    # pipeline added/day
    quality_score:          float    # 0–100
    stage_mix_score:        float    # 0–100 (late-stage weight)
    coverage_trend:         float    # (added - churned) / max(1, quota_remaining) × 100
    is_at_risk:             bool
    needs_intervention:     bool

    def to_dict(self) -> dict:
        return {
            "team_id":                 self.team_id,
            "region":                  self.region,
            "coverage_status":         self.coverage_status.value,
            "gap_severity":            self.gap_severity.value,
            "pipeline_quality":        self.pipeline_quality.value,
            "coverage_action":         self.coverage_action.value,
            "coverage_ratio":          self.coverage_ratio,
            "weighted_coverage_ratio": self.weighted_coverage_ratio,
            "gap_to_quota":            self.gap_to_quota,
            "pipeline_velocity":       self.pipeline_velocity,
            "quality_score":           self.quality_score,
            "stage_mix_score":         self.stage_mix_score,
            "coverage_trend":          self.coverage_trend,
            "is_at_risk":              self.is_at_risk,
            "needs_intervention":      self.needs_intervention,
        }


class PipelineCoverageEngine:
    def __init__(self) -> None:
        self._results: list[PipelineCoverageResult] = []

    # ── public API ─────────────────────────────────────────────────────────────

    def analyze(self, inp: PipelineCoverageInput) -> PipelineCoverageResult:
        coverage      = self._coverage_ratio(inp)
        w_coverage    = self._weighted_coverage_ratio(inp)
        gap           = self._gap_to_quota(inp)
        velocity      = self._pipeline_velocity(inp)
        quality       = self._quality_score(inp)
        stage_mix     = self._stage_mix_score(inp)
        trend         = self._coverage_trend(inp)
        status        = self._coverage_status(coverage)
        gap_sev       = self._gap_severity(gap, inp)
        pip_quality   = self._pipeline_quality(quality)
        at_risk       = w_coverage < 1.0 or gap_sev in (GapSeverity.HIGH, GapSeverity.CRITICAL)
        intervention  = status == CoverageStatus.CRITICAL_GAP or gap_sev == GapSeverity.CRITICAL
        action        = self._coverage_action(inp, status, gap_sev, quality, velocity)

        result = PipelineCoverageResult(
            team_id=inp.team_id,
            region=inp.region,
            coverage_status=status,
            gap_severity=gap_sev,
            pipeline_quality=pip_quality,
            coverage_action=action,
            coverage_ratio=coverage,
            weighted_coverage_ratio=w_coverage,
            gap_to_quota=gap,
            pipeline_velocity=velocity,
            quality_score=quality,
            stage_mix_score=stage_mix,
            coverage_trend=trend,
            is_at_risk=at_risk,
            needs_intervention=intervention,
        )
        self._results.append(result)
        return result

    def analyze_batch(
        self, inputs: list[PipelineCoverageInput]
    ) -> list[PipelineCoverageResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ─────────────────────────────────────────────────────────────

    @property
    def at_risk_teams(self) -> list[PipelineCoverageResult]:
        return [r for r in self._results if r.is_at_risk]

    @property
    def intervention_teams(self) -> list[PipelineCoverageResult]:
        return [r for r in self._results if r.needs_intervention]

    @property
    def healthy_teams(self) -> list[PipelineCoverageResult]:
        return [r for r in self._results if r.coverage_status in (
            CoverageStatus.OVER_COVERED, CoverageStatus.ADEQUATE
        )]

    @property
    def total_gap_to_quota(self) -> float:
        return round(sum(r.gap_to_quota for r in self._results), 2)

    @property
    def total_weighted_pipeline(self) -> float:
        return round(sum(
            r.weighted_coverage_ratio * 1  # weighted_coverage_ratio * quota_remaining
            for r in self._results
        ), 2)

    # ── scoring helpers ────────────────────────────────────────────────────────

    def _coverage_ratio(self, inp: PipelineCoverageInput) -> float:
        if inp.quota_remaining <= 0:
            return 0.0
        return round(inp.current_pipeline / inp.quota_remaining, 2)

    def _weighted_coverage_ratio(self, inp: PipelineCoverageInput) -> float:
        if inp.quota_remaining <= 0:
            return 0.0
        return round(inp.weighted_pipeline / inp.quota_remaining, 2)

    def _gap_to_quota(self, inp: PipelineCoverageInput) -> float:
        gap = inp.quota_remaining - inp.weighted_pipeline
        return round(max(0.0, gap), 2)

    def _pipeline_velocity(self, inp: PipelineCoverageInput) -> float:
        if inp.days_remaining <= 0:
            return 0.0
        period_elapsed = max(1, inp.avg_sales_cycle_days - inp.days_remaining)
        return round(inp.pipeline_added_qtd / period_elapsed, 2)

    def _quality_score(self, inp: PipelineCoverageInput) -> float:
        score = 0.0
        # Deal health contribution (up to 40)
        score += inp.avg_deal_health * 0.40
        # Win-rate adjusted confidence (up to 30)
        score += inp.historical_win_rate * 0.30
        # Stalled deal penalty
        total_deals = max(1, inp.current_pipeline / max(1, inp.avg_deal_size))
        stall_rate  = inp.stalled_deal_count / total_deals
        score -= stall_rate * 20.0
        # Competitive pressure penalty (up to -10)
        score -= min(10.0, inp.competitive_deal_pct * 0.10)
        return round(max(0.0, min(100.0, score)), 1)

    def _stage_mix_score(self, inp: PipelineCoverageInput) -> float:
        total = max(1.0, inp.current_pipeline)
        late  = inp.stage4_value + inp.stage5_value
        mid   = inp.stage3_value
        early = inp.stage1_value + inp.stage2_value
        # Weight: late-stage 60%, mid 30%, early 10%
        score = (late / total) * 60.0 + (mid / total) * 30.0 + (early / total) * 10.0
        return round(max(0.0, min(100.0, score)), 1)

    def _coverage_trend(self, inp: PipelineCoverageInput) -> float:
        net = inp.pipeline_added_qtd - inp.churned_pipeline_qtd
        if inp.quota_remaining <= 0:
            return 0.0
        return round((net / inp.quota_remaining) * 100, 1)

    def _coverage_status(self, coverage: float) -> CoverageStatus:
        if coverage >= 3.5:
            return CoverageStatus.OVER_COVERED
        if coverage >= 2.0:
            return CoverageStatus.ADEQUATE
        if coverage >= 1.0:
            return CoverageStatus.UNDER_COVERED
        return CoverageStatus.CRITICAL_GAP

    def _gap_severity(
        self, gap: float, inp: PipelineCoverageInput
    ) -> GapSeverity:
        if gap <= 0:
            return GapSeverity.NONE
        if inp.quota_remaining <= 0:
            return GapSeverity.NONE
        pct = (gap / inp.quota_remaining) * 100
        if pct >= 60:
            return GapSeverity.CRITICAL
        if pct >= 40:
            return GapSeverity.HIGH
        if pct >= 20:
            return GapSeverity.MEDIUM
        return GapSeverity.LOW

    def _pipeline_quality(self, quality: float) -> PipelineQuality:
        if quality >= 75:
            return PipelineQuality.EXCELLENT
        if quality >= 55:
            return PipelineQuality.GOOD
        if quality >= 35:
            return PipelineQuality.FAIR
        return PipelineQuality.POOR

    def _coverage_action(
        self,
        inp: PipelineCoverageInput,
        status: CoverageStatus,
        gap_sev: GapSeverity,
        quality: float,
        velocity: float,
    ) -> CoverageAction:
        if status == CoverageStatus.CRITICAL_GAP:
            return CoverageAction.GENERATE_PIPELINE
        if gap_sev in (GapSeverity.HIGH, GapSeverity.CRITICAL):
            return CoverageAction.REALLOCATE if velocity < 1000 else CoverageAction.GENERATE_PIPELINE
        if status == CoverageStatus.UNDER_COVERED and quality < 50:
            return CoverageAction.ACCELERATE_EXISTING
        if status == CoverageStatus.OVER_COVERED and inp.avg_deal_size < inp.quota_remaining * 0.05:
            return CoverageAction.EXPAND_UPMARKET
        if status == CoverageStatus.ADEQUATE:
            return CoverageAction.MAINTAIN
        if quality < 40:
            return CoverageAction.STRATEGIC_REVIEW
        return CoverageAction.MAINTAIN

    # ── summary ────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                    0,
                "status_counts":            {},
                "gap_severity_counts":      {},
                "quality_counts":           {},
                "action_counts":            {},
                "avg_coverage_ratio":       0.0,
                "avg_weighted_coverage":    0.0,
                "total_gap_to_quota":       0.0,
                "at_risk_count":            0,
                "intervention_count":       0,
                "avg_quality_score":        0.0,
                "avg_stage_mix_score":      0.0,
                "healthy_team_count":       0,
            }

        status_counts:    dict[str, int] = {}
        gap_counts:       dict[str, int] = {}
        quality_counts:   dict[str, int] = {}
        action_counts:    dict[str, int] = {}
        total_coverage    = 0.0
        total_w_coverage  = 0.0
        total_quality     = 0.0
        total_stage_mix   = 0.0

        for r in self._results:
            status_counts[r.coverage_status.value]   = status_counts.get(r.coverage_status.value, 0) + 1
            gap_counts[r.gap_severity.value]         = gap_counts.get(r.gap_severity.value, 0) + 1
            quality_counts[r.pipeline_quality.value] = quality_counts.get(r.pipeline_quality.value, 0) + 1
            action_counts[r.coverage_action.value]   = action_counts.get(r.coverage_action.value, 0) + 1
            total_coverage   += r.coverage_ratio
            total_w_coverage += r.weighted_coverage_ratio
            total_quality    += r.quality_score
            total_stage_mix  += r.stage_mix_score

        return {
            "total":                    n,
            "status_counts":            status_counts,
            "gap_severity_counts":      gap_counts,
            "quality_counts":           quality_counts,
            "action_counts":            action_counts,
            "avg_coverage_ratio":       round(total_coverage / n, 2),
            "avg_weighted_coverage":    round(total_w_coverage / n, 2),
            "total_gap_to_quota":       self.total_gap_to_quota,
            "at_risk_count":            len(self.at_risk_teams),
            "intervention_count":       len(self.intervention_teams),
            "avg_quality_score":        round(total_quality / n, 1),
            "avg_stage_mix_score":      round(total_stage_mix / n, 1),
            "healthy_team_count":       len(self.healthy_teams),
        }
