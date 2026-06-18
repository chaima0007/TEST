from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class ForecastRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ForecastPattern(str, Enum):
    none                       = "none"
    chronic_over_forecasting   = "chronic_over_forecasting"
    chronic_under_forecasting  = "chronic_under_forecasting"
    end_of_quarter_cliff       = "end_of_quarter_cliff"
    recency_bias_sandbagging   = "recency_bias_sandbagging"
    stage_inflation_blindspot  = "stage_inflation_blindspot"


class ForecastSeverity(str, Enum):
    precise     = "precise"
    calibrating = "calibrating"
    drifting    = "drifting"
    unreliable  = "unreliable"


class ForecastAction(str, Enum):
    no_action                     = "no_action"
    forecast_calibration_coaching = "forecast_calibration_coaching"
    pipeline_inspection_coaching  = "pipeline_inspection_coaching"
    stage_criteria_coaching       = "stage_criteria_coaching"
    commit_discipline_coaching    = "commit_discipline_coaching"
    forecast_reset_intervention   = "forecast_reset_intervention"


@dataclass
class ForecastInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    forecast_vs_actual_variance_pct: float
    over_forecast_frequency_pct: float
    under_forecast_frequency_pct: float
    commit_to_close_rate_pct: float
    best_case_to_close_rate_pct: float
    pipeline_to_quota_ratio: float
    late_add_to_forecast_pct: float
    deals_pulled_from_forecast_pct: float
    avg_deal_slip_days: float
    stage_advancement_accuracy_pct: float
    close_date_accuracy_within_week_pct: float
    forecast_change_frequency_per_qtr: float
    upside_deals_closed_pct: float
    commit_deals_lost_pct: float
    sandbag_conversion_rate_pct: float
    multi_quarter_slip_rate_pct: float
    forecast_submitted_on_time_pct: float
    total_deals_forecasted: int
    avg_opportunity_value_usd: float


@dataclass
class ForecastResult:
    rep_id: str
    region: str
    forecast_risk: ForecastRisk
    forecast_pattern: ForecastPattern
    forecast_severity: ForecastSeverity
    recommended_action: ForecastAction
    accuracy_score: float
    discipline_score: float
    stage_score: float
    commit_score: float
    forecast_composite: float
    has_forecast_gap: bool
    requires_forecast_coaching: bool
    estimated_revenue_at_risk_usd: float
    forecast_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                        self.rep_id,
            "region":                        self.region,
            "forecast_risk":                 self.forecast_risk.value,
            "forecast_pattern":              self.forecast_pattern.value,
            "forecast_severity":             self.forecast_severity.value,
            "recommended_action":            self.recommended_action.value,
            "accuracy_score":                self.accuracy_score,
            "discipline_score":              self.discipline_score,
            "stage_score":                   self.stage_score,
            "commit_score":                  self.commit_score,
            "forecast_composite":            self.forecast_composite,
            "has_forecast_gap":              self.has_forecast_gap,
            "requires_forecast_coaching":    self.requires_forecast_coaching,
            "estimated_revenue_at_risk_usd": self.estimated_revenue_at_risk_usd,
            "forecast_signal":               self.forecast_signal,
        }


class SalesForecastAccuracyIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[ForecastResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _accuracy_score(self, inp: ForecastInput) -> float:
        score = 0.0

        if inp.forecast_vs_actual_variance_pct >= 0.40:
            score += 40.0
        elif inp.forecast_vs_actual_variance_pct >= 0.20:
            score += 22.0
        elif inp.forecast_vs_actual_variance_pct >= 0.10:
            score += 8.0

        if inp.commit_deals_lost_pct >= 0.40:
            score += 35.0
        elif inp.commit_deals_lost_pct >= 0.20:
            score += 18.0

        if inp.close_date_accuracy_within_week_pct <= 0.30:
            score += 25.0
        elif inp.close_date_accuracy_within_week_pct <= 0.55:
            score += 12.0

        return min(score, 100.0)

    def _discipline_score(self, inp: ForecastInput) -> float:
        score = 0.0

        if inp.forecast_change_frequency_per_qtr >= 5.0:
            score += 40.0
        elif inp.forecast_change_frequency_per_qtr >= 3.0:
            score += 22.0
        elif inp.forecast_change_frequency_per_qtr >= 1.5:
            score += 8.0

        if inp.late_add_to_forecast_pct >= 0.40:
            score += 35.0
        elif inp.late_add_to_forecast_pct >= 0.20:
            score += 18.0

        if inp.multi_quarter_slip_rate_pct >= 0.35:
            score += 25.0
        elif inp.multi_quarter_slip_rate_pct >= 0.15:
            score += 12.0

        return min(score, 100.0)

    def _stage_score(self, inp: ForecastInput) -> float:
        score = 0.0

        if inp.stage_advancement_accuracy_pct <= 0.40:
            score += 40.0
        elif inp.stage_advancement_accuracy_pct <= 0.60:
            score += 22.0
        elif inp.stage_advancement_accuracy_pct <= 0.75:
            score += 8.0

        if inp.deals_pulled_from_forecast_pct >= 0.35:
            score += 35.0
        elif inp.deals_pulled_from_forecast_pct >= 0.20:
            score += 18.0

        if inp.avg_deal_slip_days >= 30.0:
            score += 25.0
        elif inp.avg_deal_slip_days >= 14.0:
            score += 12.0

        return min(score, 100.0)

    def _commit_score(self, inp: ForecastInput) -> float:
        score = 0.0

        if inp.commit_to_close_rate_pct <= 0.40:
            score += 45.0
        elif inp.commit_to_close_rate_pct <= 0.60:
            score += 25.0
        elif inp.commit_to_close_rate_pct <= 0.75:
            score += 10.0

        if inp.over_forecast_frequency_pct >= 0.60:
            score += 30.0
        elif inp.over_forecast_frequency_pct >= 0.40:
            score += 15.0

        if inp.under_forecast_frequency_pct >= 0.50:
            score += 25.0
        elif inp.under_forecast_frequency_pct >= 0.30:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: ForecastInput,
                         accuracy: float, discipline: float,
                         stage: float, commit: float) -> ForecastPattern:
        # Stage inflation blindspot: stage data is wrong, misrepresenting pipeline
        if inp.stage_advancement_accuracy_pct <= 0.35 and inp.deals_pulled_from_forecast_pct >= 0.30:
            return ForecastPattern.stage_inflation_blindspot

        # Chronic over-forecasting: consistently forecasts more than closes
        if inp.over_forecast_frequency_pct >= 0.55 and inp.commit_deals_lost_pct >= 0.30:
            return ForecastPattern.chronic_over_forecasting

        # End of quarter cliff: deals slip heavily at quarter end
        if discipline >= 35 and inp.multi_quarter_slip_rate_pct >= 0.25:
            return ForecastPattern.end_of_quarter_cliff

        # Recency bias sandbagging: underforecast early, last-minute upside adds
        if inp.sandbag_conversion_rate_pct >= 0.50 and inp.late_add_to_forecast_pct >= 0.30:
            return ForecastPattern.recency_bias_sandbagging

        # Chronic under-forecasting: consistently sandbagging
        if inp.under_forecast_frequency_pct >= 0.45 and commit >= 30:
            return ForecastPattern.chronic_under_forecasting

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
            return ForecastSeverity.unreliable
        if composite >= 40:
            return ForecastSeverity.drifting
        if composite >= 20:
            return ForecastSeverity.calibrating
        return ForecastSeverity.precise

    def _action(self, risk: ForecastRisk, pattern: ForecastPattern) -> ForecastAction:
        if risk == ForecastRisk.critical:
            if pattern == ForecastPattern.stage_inflation_blindspot:
                return ForecastAction.stage_criteria_coaching
            if pattern == ForecastPattern.chronic_over_forecasting:
                return ForecastAction.commit_discipline_coaching
            return ForecastAction.forecast_reset_intervention
        if risk == ForecastRisk.high:
            if pattern == ForecastPattern.end_of_quarter_cliff:
                return ForecastAction.pipeline_inspection_coaching
            if pattern == ForecastPattern.recency_bias_sandbagging:
                return ForecastAction.forecast_calibration_coaching
            return ForecastAction.commit_discipline_coaching
        if risk == ForecastRisk.moderate:
            return ForecastAction.forecast_calibration_coaching
        return ForecastAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_forecast_gap(self, composite: float, inp: ForecastInput) -> bool:
        return (
            composite >= 40
            or inp.commit_deals_lost_pct >= 0.30
            or inp.commit_to_close_rate_pct <= 0.50
        )

    def _requires_forecast_coaching(self, composite: float, inp: ForecastInput) -> bool:
        return (
            composite >= 30
            or inp.forecast_vs_actual_variance_pct >= 0.15
            or inp.stage_advancement_accuracy_pct <= 0.60
        )

    # ------------------------------------------------------------------
    # Revenue at risk estimate
    # ------------------------------------------------------------------

    def _estimated_revenue_at_risk(self, inp: ForecastInput, composite: float) -> float:
        return round(
            inp.total_deals_forecasted
            * inp.avg_opportunity_value_usd
            * inp.commit_deals_lost_pct
            * (composite / 100.0),
            2,
        )

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: ForecastInput,
                 pattern: ForecastPattern, composite: float) -> str:
        if pattern == ForecastPattern.none and composite < 20:
            return "Forecast accuracy healthy — variance, commit discipline, and stage accuracy within benchmarks"
        parts: list[str] = []
        parts.append(f"{inp.forecast_vs_actual_variance_pct * 100:.0f}% forecast variance")
        parts.append(f"{inp.commit_to_close_rate_pct * 100:.0f}% commit-to-close rate")
        parts.append(f"{inp.commit_deals_lost_pct * 100:.0f}% committed deals lost")
        label = pattern.value.replace("_", " ") if pattern != ForecastPattern.none else "Forecast risk"
        return f"{label.capitalize()} — {' — '.join(parts)} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: ForecastInput) -> ForecastResult:
        accuracy   = round(self._accuracy_score(inp), 1)
        discipline = round(self._discipline_score(inp), 1)
        stage      = round(self._stage_score(inp), 1)
        commit     = round(self._commit_score(inp), 1)

        composite = round(
            accuracy * 0.35 + discipline * 0.25 + stage * 0.25 + commit * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, accuracy, discipline, stage, commit)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap    = self._has_forecast_gap(composite, inp)
        coach  = self._requires_forecast_coaching(composite, inp)
        loss   = self._estimated_revenue_at_risk(inp, composite)
        signal = self._signal(inp, pattern, composite)

        result = ForecastResult(
            rep_id=inp.rep_id,
            region=inp.region,
            forecast_risk=risk,
            forecast_pattern=pattern,
            forecast_severity=severity,
            recommended_action=action,
            accuracy_score=accuracy,
            discipline_score=discipline,
            stage_score=stage,
            commit_score=commit,
            forecast_composite=composite,
            has_forecast_gap=gap,
            requires_forecast_coaching=coach,
            estimated_revenue_at_risk_usd=loss,
            forecast_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[ForecastInput]) -> list[ForecastResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_forecast_composite": 0.0,
                "forecast_gap_count": 0,
                "coaching_count": 0,
                "avg_accuracy_score": 0.0,
                "avg_discipline_score": 0.0,
                "avg_stage_score": 0.0,
                "avg_commit_score": 0.0,
                "total_estimated_revenue_at_risk_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_acc = total_dis = total_sta = total_com = total_loss = 0.0

        for r in self._results:
            risk_counts[r.forecast_risk.value]         = risk_counts.get(r.forecast_risk.value, 0) + 1
            pattern_counts[r.forecast_pattern.value]   = pattern_counts.get(r.forecast_pattern.value, 0) + 1
            severity_counts[r.forecast_severity.value] = severity_counts.get(r.forecast_severity.value, 0) + 1
            action_counts[r.recommended_action.value]  = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.forecast_composite
            total_acc  += r.accuracy_score
            total_dis  += r.discipline_score
            total_sta  += r.stage_score
            total_com  += r.commit_score
            total_loss += r.estimated_revenue_at_risk_usd

        n = len(self._results)

        return {
            "total":                                    n,
            "risk_counts":                              risk_counts,
            "pattern_counts":                           pattern_counts,
            "severity_counts":                          severity_counts,
            "action_counts":                            action_counts,
            "avg_forecast_composite":                   round(total_comp / n, 1),
            "forecast_gap_count":                       sum(1 for r in self._results if r.has_forecast_gap),
            "coaching_count":                           sum(1 for r in self._results if r.requires_forecast_coaching),
            "avg_accuracy_score":                       round(total_acc / n, 1),
            "avg_discipline_score":                     round(total_dis / n, 1),
            "avg_stage_score":                          round(total_sta / n, 1),
            "avg_commit_score":                         round(total_com / n, 1),
            "total_estimated_revenue_at_risk_usd":      round(total_loss, 2),
        }
