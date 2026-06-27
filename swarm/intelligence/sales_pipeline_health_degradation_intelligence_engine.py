from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class PipelineRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class PipelinePattern(str, Enum):
    none                    = "none"
    zombie_deal_accumulation = "zombie_deal_accumulation"
    stage_stagnation         = "stage_stagnation"
    pipeline_inflation       = "pipeline_inflation"
    curation_avoidance       = "curation_avoidance"
    late_stage_concentration = "late_stage_concentration"


class PipelineSeverity(str, Enum):
    healthy     = "healthy"
    declining   = "declining"
    degraded    = "degraded"
    critical    = "critical"


class PipelineAction(str, Enum):
    no_action                    = "no_action"
    pipeline_hygiene_coaching    = "pipeline_hygiene_coaching"
    deal_progression_review      = "deal_progression_review"
    pipeline_curation_workshop   = "pipeline_curation_workshop"
    stage_exit_criteria_coaching = "stage_exit_criteria_coaching"
    pipeline_reset_intervention  = "pipeline_reset_intervention"


@dataclass
class PipelineInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    avg_deal_age_days: float
    deals_exceeding_avg_stage_duration_pct: float
    deals_with_no_activity_30d_pct: float
    deals_with_no_activity_60d_pct: float
    stage_to_stage_progression_rate_pct: float
    pipeline_value_change_pct: float
    deals_added_not_touched_after_create_pct: float
    deals_closed_lost_rate_pct: float
    deals_deleted_or_merged_per_qtr: float
    avg_days_in_current_stage: float
    expected_days_in_stage: float
    late_stage_deals_pct: float
    early_stage_deals_pct: float
    single_stage_pipeline_concentration: float
    pipeline_refresh_rate_pct: float
    closed_won_from_current_pipeline_pct: float
    deals_slipped_more_than_once_pct: float
    total_open_deals: int
    avg_opportunity_value_usd: float


@dataclass
class PipelineResult:
    rep_id: str
    region: str
    pipeline_risk: PipelineRisk
    pipeline_pattern: PipelinePattern
    pipeline_severity: PipelineSeverity
    recommended_action: PipelineAction
    staleness_score: float
    progression_score: float
    curation_score: float
    concentration_score: float
    pipeline_composite: float
    has_pipeline_gap: bool
    requires_pipeline_coaching: bool
    estimated_phantom_pipeline_usd: float
    pipeline_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                        self.rep_id,
            "region":                        self.region,
            "pipeline_risk":                 self.pipeline_risk.value,
            "pipeline_pattern":              self.pipeline_pattern.value,
            "pipeline_severity":             self.pipeline_severity.value,
            "recommended_action":            self.recommended_action.value,
            "staleness_score":               self.staleness_score,
            "progression_score":             self.progression_score,
            "curation_score":                self.curation_score,
            "concentration_score":           self.concentration_score,
            "pipeline_composite":            self.pipeline_composite,
            "has_pipeline_gap":              self.has_pipeline_gap,
            "requires_pipeline_coaching":    self.requires_pipeline_coaching,
            "estimated_phantom_pipeline_usd":self.estimated_phantom_pipeline_usd,
            "pipeline_signal":               self.pipeline_signal,
        }


class SalesPipelineHealthDegradationIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[PipelineResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _staleness_score(self, inp: PipelineInput) -> float:
        score = 0.0

        if inp.deals_with_no_activity_30d_pct >= 0.50:
            score += 40.0
        elif inp.deals_with_no_activity_30d_pct >= 0.30:
            score += 22.0
        elif inp.deals_with_no_activity_30d_pct >= 0.15:
            score += 8.0

        if inp.avg_deal_age_days >= 120.0:
            score += 35.0
        elif inp.avg_deal_age_days >= 75.0:
            score += 18.0

        if inp.deals_with_no_activity_60d_pct >= 0.35:
            score += 25.0
        elif inp.deals_with_no_activity_60d_pct >= 0.15:
            score += 12.0

        return min(score, 100.0)

    def _progression_score(self, inp: PipelineInput) -> float:
        score = 0.0

        if inp.stage_to_stage_progression_rate_pct <= 0.20:
            score += 40.0
        elif inp.stage_to_stage_progression_rate_pct <= 0.40:
            score += 22.0
        elif inp.stage_to_stage_progression_rate_pct <= 0.60:
            score += 8.0

        if inp.deals_slipped_more_than_once_pct >= 0.45:
            score += 35.0
        elif inp.deals_slipped_more_than_once_pct >= 0.25:
            score += 18.0

        stage_overage = inp.avg_days_in_current_stage - inp.expected_days_in_stage
        if stage_overage >= 30.0:
            score += 25.0
        elif stage_overage >= 14.0:
            score += 12.0

        return min(score, 100.0)

    def _curation_score(self, inp: PipelineInput) -> float:
        score = 0.0

        if inp.deals_added_not_touched_after_create_pct >= 0.40:
            score += 40.0
        elif inp.deals_added_not_touched_after_create_pct >= 0.25:
            score += 22.0
        elif inp.deals_added_not_touched_after_create_pct >= 0.10:
            score += 8.0

        if inp.deals_exceeding_avg_stage_duration_pct >= 0.55:
            score += 35.0
        elif inp.deals_exceeding_avg_stage_duration_pct >= 0.35:
            score += 18.0

        if inp.closed_won_from_current_pipeline_pct <= 0.15:
            score += 25.0
        elif inp.closed_won_from_current_pipeline_pct <= 0.30:
            score += 12.0

        return min(score, 100.0)

    def _concentration_score(self, inp: PipelineInput) -> float:
        score = 0.0

        if inp.single_stage_pipeline_concentration >= 0.65:
            score += 45.0
        elif inp.single_stage_pipeline_concentration >= 0.45:
            score += 25.0
        elif inp.single_stage_pipeline_concentration >= 0.30:
            score += 10.0

        if inp.late_stage_deals_pct <= 0.10:
            score += 30.0
        elif inp.late_stage_deals_pct <= 0.25:
            score += 15.0

        if inp.pipeline_refresh_rate_pct <= 0.15:
            score += 25.0
        elif inp.pipeline_refresh_rate_pct <= 0.30:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: PipelineInput,
                          staleness: float, progression: float,
                          curation: float, concentration: float) -> PipelinePattern:
        # Zombie deal accumulation: lots of stale, unworked deals clogging pipeline
        if inp.deals_with_no_activity_60d_pct >= 0.30 and inp.deals_added_not_touched_after_create_pct >= 0.30:
            return PipelinePattern.zombie_deal_accumulation

        # Pipeline inflation: adds deals but doesn't win from them
        if curation >= 40 and inp.closed_won_from_current_pipeline_pct <= 0.20:
            return PipelinePattern.pipeline_inflation

        # Stage stagnation: deals stuck in same stage too long
        if progression >= 35 and inp.deals_slipped_more_than_once_pct >= 0.35:
            return PipelinePattern.stage_stagnation

        # Curation avoidance: never removes dead deals
        if inp.deals_closed_lost_rate_pct <= 0.10 and staleness >= 30:
            return PipelinePattern.curation_avoidance

        # Late stage concentration: all bets on a few late-stage deals
        if inp.late_stage_deals_pct >= 0.65 and concentration >= 25:
            return PipelinePattern.late_stage_concentration

        return PipelinePattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> PipelineRisk:
        if composite >= 60:
            return PipelineRisk.critical
        if composite >= 40:
            return PipelineRisk.high
        if composite >= 20:
            return PipelineRisk.moderate
        return PipelineRisk.low

    def _severity(self, composite: float) -> PipelineSeverity:
        if composite >= 60:
            return PipelineSeverity.critical
        if composite >= 40:
            return PipelineSeverity.degraded
        if composite >= 20:
            return PipelineSeverity.declining
        return PipelineSeverity.healthy

    def _action(self, risk: PipelineRisk, pattern: PipelinePattern) -> PipelineAction:
        if risk == PipelineRisk.critical:
            if pattern == PipelinePattern.zombie_deal_accumulation:
                return PipelineAction.pipeline_hygiene_coaching
            if pattern == PipelinePattern.pipeline_inflation:
                return PipelineAction.pipeline_curation_workshop
            return PipelineAction.pipeline_reset_intervention
        if risk == PipelineRisk.high:
            if pattern == PipelinePattern.stage_stagnation:
                return PipelineAction.stage_exit_criteria_coaching
            if pattern == PipelinePattern.curation_avoidance:
                return PipelineAction.pipeline_hygiene_coaching
            return PipelineAction.deal_progression_review
        if risk == PipelineRisk.moderate:
            return PipelineAction.pipeline_hygiene_coaching
        return PipelineAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_pipeline_gap(self, composite: float, inp: PipelineInput) -> bool:
        return (
            composite >= 40
            or inp.deals_with_no_activity_60d_pct >= 0.25
            or inp.closed_won_from_current_pipeline_pct <= 0.20
        )

    def _requires_pipeline_coaching(self, composite: float, inp: PipelineInput) -> bool:
        return (
            composite >= 30
            or inp.deals_exceeding_avg_stage_duration_pct >= 0.35
            or inp.deals_with_no_activity_30d_pct >= 0.25
        )

    # ------------------------------------------------------------------
    # Phantom pipeline estimate
    # ------------------------------------------------------------------

    def _estimated_phantom_pipeline(self, inp: PipelineInput, composite: float) -> float:
        return round(
            inp.total_open_deals
            * inp.avg_opportunity_value_usd
            * inp.deals_with_no_activity_60d_pct
            * (composite / 100.0),
            2,
        )

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: PipelineInput,
                 pattern: PipelinePattern, composite: float) -> str:
        if pattern == PipelinePattern.none and composite < 20:
            return "Pipeline health strong — deal activity, stage progression, and curation within benchmarks"
        parts: list[str] = []
        parts.append(f"{inp.deals_with_no_activity_30d_pct * 100:.0f}% deals with no activity 30d")
        parts.append(f"{inp.stage_to_stage_progression_rate_pct * 100:.0f}% stage progression rate")
        parts.append(f"{inp.closed_won_from_current_pipeline_pct * 100:.0f}% pipeline converting to wins")
        label = pattern.value.replace("_", " ") if pattern != PipelinePattern.none else "Pipeline risk"
        return f"{label.capitalize()} — {' — '.join(parts)} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: PipelineInput) -> PipelineResult:
        staleness    = round(self._staleness_score(inp), 1)
        progression  = round(self._progression_score(inp), 1)
        curation     = round(self._curation_score(inp), 1)
        concentration = round(self._concentration_score(inp), 1)

        composite = round(
            staleness * 0.30 + progression * 0.30 + curation * 0.25 + concentration * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, staleness, progression, curation, concentration)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap    = self._has_pipeline_gap(composite, inp)
        coach  = self._requires_pipeline_coaching(composite, inp)
        loss   = self._estimated_phantom_pipeline(inp, composite)
        signal = self._signal(inp, pattern, composite)

        result = PipelineResult(
            rep_id=inp.rep_id,
            region=inp.region,
            pipeline_risk=risk,
            pipeline_pattern=pattern,
            pipeline_severity=severity,
            recommended_action=action,
            staleness_score=staleness,
            progression_score=progression,
            curation_score=curation,
            concentration_score=concentration,
            pipeline_composite=composite,
            has_pipeline_gap=gap,
            requires_pipeline_coaching=coach,
            estimated_phantom_pipeline_usd=loss,
            pipeline_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[PipelineInput]) -> list[PipelineResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
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
                "avg_staleness_score": 0.0,
                "avg_progression_score": 0.0,
                "avg_curation_score": 0.0,
                "avg_concentration_score": 0.0,
                "total_estimated_phantom_pipeline_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_sta = total_pro = total_cur = total_con = total_loss = 0.0

        for r in self._results:
            risk_counts[r.pipeline_risk.value]         = risk_counts.get(r.pipeline_risk.value, 0) + 1
            pattern_counts[r.pipeline_pattern.value]   = pattern_counts.get(r.pipeline_pattern.value, 0) + 1
            severity_counts[r.pipeline_severity.value] = severity_counts.get(r.pipeline_severity.value, 0) + 1
            action_counts[r.recommended_action.value]  = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.pipeline_composite
            total_sta  += r.staleness_score
            total_pro  += r.progression_score
            total_cur  += r.curation_score
            total_con  += r.concentration_score
            total_loss += r.estimated_phantom_pipeline_usd

        n = len(self._results)

        return {
            "total":                                    n,
            "risk_counts":                              risk_counts,
            "pattern_counts":                           pattern_counts,
            "severity_counts":                          severity_counts,
            "action_counts":                            action_counts,
            "avg_pipeline_composite":                   round(total_comp / n, 1),
            "pipeline_gap_count":                       sum(1 for r in self._results if r.has_pipeline_gap),
            "coaching_count":                           sum(1 for r in self._results if r.requires_pipeline_coaching),
            "avg_staleness_score":                      round(total_sta / n, 1),
            "avg_progression_score":                    round(total_pro / n, 1),
            "avg_curation_score":                       round(total_cur / n, 1),
            "avg_concentration_score":                  round(total_con / n, 1),
            "total_estimated_phantom_pipeline_usd":     round(total_loss, 2),
        }
