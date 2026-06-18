from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class ForecastRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ForecastPattern(str, Enum):
    none                   = "none"
    systematic_overforecast = "systematic_overforecast"
    sandbag_behavior       = "sandbag_behavior"
    pipeline_gap           = "pipeline_gap"
    crm_neglect            = "crm_neglect"
    stage_manipulation     = "stage_manipulation"


class ForecastSeverity(str, Enum):
    reliable   = "reliable"
    variable   = "variable"
    unreliable = "unreliable"
    chaotic    = "chaotic"


class ForecastAction(str, Enum):
    no_action                  = "no_action"
    forecast_recalibration     = "forecast_recalibration"
    pipeline_inspection        = "pipeline_inspection"
    crm_training               = "crm_training"
    forecast_review_cadence    = "forecast_review_cadence"
    forecast_override          = "forecast_override"


@dataclass
class ForecastAccuracyInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    total_forecasted_deals: int
    forecast_commit_count: int
    forecast_commit_closed_count: int
    forecast_upside_count: int
    forecast_upside_closed_count: int
    late_stage_slippage_count: int
    sandbagged_deals_identified: int
    avg_forecast_accuracy_pct: float
    forecast_overestimate_count: int
    forecast_underestimate_count: int
    pipeline_coverage_ratio: float
    avg_deal_age_days: float
    avg_close_date_slip_days: float
    stage_advancement_rate_pct: float
    crm_update_frequency_score: float
    manager_review_sessions_count: int
    multi_stakeholder_deals_pct: float
    avg_deal_size_usd: float
    deals_closed_not_forecasted_count: int


@dataclass
class ForecastAccuracyResult:
    rep_id: str
    region: str
    forecast_risk: ForecastRisk
    forecast_pattern: ForecastPattern
    forecast_severity: ForecastSeverity
    recommended_action: ForecastAction
    forecast_accuracy_score: float
    forecast_discipline_score: float
    pipeline_health_score: float
    crm_hygiene_score: float
    forecast_effectiveness_composite: float
    is_forecast_unreliable: bool
    requires_pipeline_inspection: bool
    estimated_revenue_variance_usd: float
    forecast_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "forecast_risk":                    self.forecast_risk.value,
            "forecast_pattern":                 self.forecast_pattern.value,
            "forecast_severity":                self.forecast_severity.value,
            "recommended_action":               self.recommended_action.value,
            "forecast_accuracy_score":          self.forecast_accuracy_score,
            "forecast_discipline_score":        self.forecast_discipline_score,
            "pipeline_health_score":            self.pipeline_health_score,
            "crm_hygiene_score":                self.crm_hygiene_score,
            "forecast_effectiveness_composite": self.forecast_effectiveness_composite,
            "is_forecast_unreliable":           self.is_forecast_unreliable,
            "requires_pipeline_inspection":     self.requires_pipeline_inspection,
            "estimated_revenue_variance_usd":   self.estimated_revenue_variance_usd,
            "forecast_signal":                  self.forecast_signal,
        }


class SalesForecastAccuracyIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[ForecastAccuracyResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _forecast_accuracy_score(self, inp: ForecastAccuracyInput) -> float:
        score = 0.0

        # Accuracy deviation from 100%
        dev = abs(inp.avg_forecast_accuracy_pct - 1.0)
        if dev >= 0.40:
            score += 40.0
        elif dev >= 0.25:
            score += 25.0
        elif dev >= 0.15:
            score += 12.0

        # Commit accuracy (commit deals that actually closed)
        commit_denom = max(inp.forecast_commit_count, 1)
        commit_rate = inp.forecast_commit_closed_count / commit_denom
        if commit_rate < 0.50:
            score += 30.0
        elif commit_rate < 0.70:
            score += 15.0
        elif commit_rate < 0.85:
            score += 5.0

        # Overestimate ratio
        total = max(inp.total_forecasted_deals, 1)
        over_ratio = inp.forecast_overestimate_count / total
        if over_ratio >= 0.40:
            score += 20.0
        elif over_ratio >= 0.25:
            score += 10.0
        elif over_ratio >= 0.15:
            score += 5.0

        return min(score, 100.0)

    def _forecast_discipline_score(self, inp: ForecastAccuracyInput) -> float:
        score = 0.0

        # Late stage slippage
        if inp.late_stage_slippage_count >= 4:
            score += 35.0
        elif inp.late_stage_slippage_count >= 2:
            score += 20.0
        elif inp.late_stage_slippage_count >= 1:
            score += 8.0

        # Close date slippage
        if inp.avg_close_date_slip_days >= 45:
            score += 30.0
        elif inp.avg_close_date_slip_days >= 25:
            score += 18.0
        elif inp.avg_close_date_slip_days >= 10:
            score += 8.0

        # Unknown closes (closed but not in forecast)
        if inp.deals_closed_not_forecasted_count >= 3:
            score += 25.0
        elif inp.deals_closed_not_forecasted_count >= 2:
            score += 12.0
        elif inp.deals_closed_not_forecasted_count >= 1:
            score += 5.0

        # Missed manager review sessions
        if inp.manager_review_sessions_count == 0:
            score += 10.0
        elif inp.manager_review_sessions_count <= 1:
            score += 5.0

        return min(score, 100.0)

    def _pipeline_health_score(self, inp: ForecastAccuracyInput) -> float:
        score = 0.0

        # Pipeline coverage ratio
        if inp.pipeline_coverage_ratio < 2.0:
            score += 35.0
        elif inp.pipeline_coverage_ratio < 3.0:
            score += 18.0
        elif inp.pipeline_coverage_ratio < 4.0:
            score += 8.0

        # Deal age (stale pipeline)
        if inp.avg_deal_age_days >= 120:
            score += 25.0
        elif inp.avg_deal_age_days >= 75:
            score += 15.0
        elif inp.avg_deal_age_days >= 45:
            score += 5.0

        # Stage advancement rate
        if inp.stage_advancement_rate_pct < 0.30:
            score += 25.0
        elif inp.stage_advancement_rate_pct < 0.50:
            score += 12.0

        # Multi-stakeholder coverage
        if inp.multi_stakeholder_deals_pct < 0.30:
            score += 15.0
        elif inp.multi_stakeholder_deals_pct < 0.50:
            score += 8.0

        return min(score, 100.0)

    def _crm_hygiene_score(self, inp: ForecastAccuracyInput) -> float:
        score = 0.0

        # CRM update frequency (0–10 scale, low = risky)
        if inp.crm_update_frequency_score < 3.0:
            score += 45.0
        elif inp.crm_update_frequency_score < 5.0:
            score += 25.0
        elif inp.crm_update_frequency_score < 7.0:
            score += 10.0

        # Sandbag signals (hide deals from CRM until close)
        if inp.sandbagged_deals_identified >= 3:
            score += 35.0
        elif inp.sandbagged_deals_identified >= 2:
            score += 18.0
        elif inp.sandbagged_deals_identified >= 1:
            score += 8.0

        # Underestimate (closed not in forecast — CRM miss)
        if inp.forecast_underestimate_count >= 3:
            score += 20.0
        elif inp.forecast_underestimate_count >= 2:
            score += 10.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: ForecastAccuracyInput,
                         accuracy: float, discipline: float,
                         pipeline: float, crm: float) -> ForecastPattern:
        # Priority: systematic_overforecast > sandbag_behavior > pipeline_gap
        #           > crm_neglect > stage_manipulation > none

        total = max(inp.total_forecasted_deals, 1)
        over_ratio = inp.forecast_overestimate_count / total
        if accuracy >= 35 and over_ratio >= 0.30:
            return ForecastPattern.systematic_overforecast

        if inp.sandbagged_deals_identified >= 2 and crm >= 25:
            return ForecastPattern.sandbag_behavior

        if pipeline >= 35 and inp.pipeline_coverage_ratio < 2.5:
            return ForecastPattern.pipeline_gap

        if crm >= 30 and inp.crm_update_frequency_score < 5.0:
            return ForecastPattern.crm_neglect

        if discipline >= 30 and inp.late_stage_slippage_count >= 2:
            return ForecastPattern.stage_manipulation

        return ForecastPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> ForecastRisk:
        if composite >= 60:
            return ForecastRisk.critical
        if composite >= 40:
            return ForecastRisk.high
        if composite >= 20:
            return ForecastRisk.moderate
        return ForecastRisk.low

    def _severity(self, composite: float) -> ForecastSeverity:
        if composite >= 60:
            return ForecastSeverity.chaotic
        if composite >= 40:
            return ForecastSeverity.unreliable
        if composite >= 20:
            return ForecastSeverity.variable
        return ForecastSeverity.reliable

    def _action(self, risk: ForecastRisk, pattern: ForecastPattern) -> ForecastAction:
        if risk == ForecastRisk.critical:
            if pattern == ForecastPattern.systematic_overforecast:
                return ForecastAction.forecast_override
            if pattern == ForecastPattern.pipeline_gap:
                return ForecastAction.pipeline_inspection
            return ForecastAction.forecast_review_cadence
        if risk == ForecastRisk.high:
            if pattern == ForecastPattern.crm_neglect:
                return ForecastAction.crm_training
            if pattern == ForecastPattern.sandbag_behavior:
                return ForecastAction.forecast_review_cadence
            return ForecastAction.pipeline_inspection
        if risk == ForecastRisk.moderate:
            return ForecastAction.forecast_recalibration
        return ForecastAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _is_forecast_unreliable(self, composite: float,
                                 inp: ForecastAccuracyInput) -> bool:
        commit_denom = max(inp.forecast_commit_count, 1)
        commit_rate = inp.forecast_commit_closed_count / commit_denom
        return (
            composite >= 40
            or commit_rate < 0.50
            or inp.late_stage_slippage_count >= 3
        )

    def _requires_pipeline_inspection(self, composite: float,
                                       inp: ForecastAccuracyInput) -> bool:
        return (
            composite >= 30
            or inp.pipeline_coverage_ratio < 2.5
            or inp.avg_close_date_slip_days >= 30
        )

    # ------------------------------------------------------------------
    # Revenue variance
    # ------------------------------------------------------------------

    def _estimated_revenue_variance(self, inp: ForecastAccuracyInput,
                                     composite: float) -> float:
        return round(
            inp.forecast_overestimate_count * inp.avg_deal_size_usd * (composite / 100.0), 2
        )

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: ForecastAccuracyInput,
                 pattern: ForecastPattern, composite: float) -> str:
        if pattern == ForecastPattern.none and composite < 20:
            return "Forecast accuracy within acceptable benchmarks"
        parts: list[str] = []
        if inp.forecast_overestimate_count >= 1:
            parts.append(f"{inp.forecast_overestimate_count} over-forecasted deals")
        if inp.late_stage_slippage_count >= 1:
            parts.append(f"{inp.late_stage_slippage_count} late-stage slippages")
        if inp.sandbagged_deals_identified >= 1:
            parts.append(f"{inp.sandbagged_deals_identified} sandbagged deals")
        if inp.deals_closed_not_forecasted_count >= 1:
            parts.append(f"{inp.deals_closed_not_forecasted_count} unforecast closes")
        label = pattern.value.replace("_", " ") if pattern != ForecastPattern.none else "Forecast risk"
        summary = " — ".join(parts) if parts else "forecast quality degrading"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: ForecastAccuracyInput) -> ForecastAccuracyResult:
        accuracy   = round(self._forecast_accuracy_score(inp), 1)
        discipline = round(self._forecast_discipline_score(inp), 1)
        pipeline   = round(self._pipeline_health_score(inp), 1)
        crm        = round(self._crm_hygiene_score(inp), 1)

        composite = round(accuracy * 0.35 + discipline * 0.25 + pipeline * 0.25 + crm * 0.15, 1)
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, accuracy, discipline, pipeline, crm)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        unreliable = self._is_forecast_unreliable(composite, inp)
        inspection = self._requires_pipeline_inspection(composite, inp)
        variance   = self._estimated_revenue_variance(inp, composite)
        signal     = self._signal(inp, pattern, composite)

        result = ForecastAccuracyResult(
            rep_id=inp.rep_id,
            region=inp.region,
            forecast_risk=risk,
            forecast_pattern=pattern,
            forecast_severity=severity,
            recommended_action=action,
            forecast_accuracy_score=accuracy,
            forecast_discipline_score=discipline,
            pipeline_health_score=pipeline,
            crm_hygiene_score=crm,
            forecast_effectiveness_composite=composite,
            is_forecast_unreliable=unreliable,
            requires_pipeline_inspection=inspection,
            estimated_revenue_variance_usd=variance,
            forecast_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[ForecastAccuracyInput]) -> list[ForecastAccuracyResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_forecast_effectiveness_composite": 0.0,
                "unreliable_forecast_count": 0,
                "pipeline_inspection_count": 0,
                "avg_forecast_accuracy_score": 0.0,
                "avg_forecast_discipline_score": 0.0,
                "avg_pipeline_health_score": 0.0,
                "avg_crm_hygiene_score": 0.0,
                "total_estimated_revenue_variance_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_acc = total_disc = total_pipe = total_crm = total_var = 0.0

        for r in self._results:
            risk_counts[r.forecast_risk.value]       = risk_counts.get(r.forecast_risk.value, 0) + 1
            pattern_counts[r.forecast_pattern.value] = pattern_counts.get(r.forecast_pattern.value, 0) + 1
            severity_counts[r.forecast_severity.value] = severity_counts.get(r.forecast_severity.value, 0) + 1
            action_counts[r.recommended_action.value]  = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.forecast_effectiveness_composite
            total_acc  += r.forecast_accuracy_score
            total_disc += r.forecast_discipline_score
            total_pipe += r.pipeline_health_score
            total_crm  += r.crm_hygiene_score
            total_var  += r.estimated_revenue_variance_usd

        n = len(self._results)

        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_forecast_effectiveness_composite": round(total_comp / n, 1),
            "unreliable_forecast_count":            sum(1 for r in self._results if r.is_forecast_unreliable),
            "pipeline_inspection_count":            sum(1 for r in self._results if r.requires_pipeline_inspection),
            "avg_forecast_accuracy_score":          round(total_acc / n, 1),
            "avg_forecast_discipline_score":        round(total_disc / n, 1),
            "avg_pipeline_health_score":            round(total_pipe / n, 1),
            "avg_crm_hygiene_score":                round(total_crm / n, 1),
            "total_estimated_revenue_variance_usd": round(total_var, 2),
        }
