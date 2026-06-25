"""
Sales Forecast Accuracy Intelligence Engine

Mesure la fiabilité des prévisions commerciales : variance, discipline de commit,
précision par stage, biais de sandbag/over-commit.
"""

from __future__ import annotations

from dataclasses import dataclass, fields as dc_fields
from enum import Enum
from typing import Optional


class ForecastRisk(str, Enum):
    low = "low"
    moderate = "moderate"
    high = "high"
    critical = "critical"


class ForecastPattern(str, Enum):
    none = "none"
    chronic_over_forecasting = "chronic_over_forecasting"
    chronic_under_forecasting = "chronic_under_forecasting"
    end_of_quarter_cliff = "end_of_quarter_cliff"
    recency_bias_sandbagging = "recency_bias_sandbagging"
    stage_inflation_blindspot = "stage_inflation_blindspot"


class ForecastSeverity(str, Enum):
    precise = "precise"
    calibrating = "calibrating"
    drifting = "drifting"
    unreliable = "unreliable"


class ForecastAction(str, Enum):
    maintain = "maintain"
    commit_discipline_coaching = "commit_discipline_coaching"
    stage_criteria_coaching = "stage_criteria_coaching"
    forecast_reset_intervention = "forecast_reset_intervention"
    pipeline_hygiene_audit = "pipeline_hygiene_audit"
    bias_calibration_session = "bias_calibration_session"


@dataclass
class ForecastInput:
    total_deals: int = 20
    avg_deal_value: float = 25000.0
    forecast_variance_pct: float = 12.0
    commit_to_close_ratio: float = 0.75
    over_forecast_frequency: float = 0.25
    under_forecast_frequency: float = 0.15
    stage_accuracy_pct: float = 72.0
    deals_pulled_forward: int = 2
    deals_slipped_last_quarter: int = 3
    avg_slip_days: float = 18.0
    commit_change_frequency: float = 0.20
    late_stage_add_rate: float = 0.15
    close_date_change_avg: float = 14.0
    commit_lost_pct: float = 0.10
    weighted_pipeline: float = 400000.0
    quota: float = 500000.0
    actual_closed: float = 380000.0
    forecast_submitted: float = 420000.0
    deals_in_commit: int = 8
    deals_in_best_case: int = 5
    crm_last_update_days_avg: float = 5.0
    historical_accuracy_pct: float = 78.0


@dataclass
class ForecastResult:
    composite_score: float
    risk: ForecastRisk
    pattern: ForecastPattern
    severity: ForecastSeverity
    action: ForecastAction
    accuracy_score: float
    discipline_score: float
    stage_score: float
    commit_score: float
    has_forecast_gap: bool
    requires_forecast_coaching: bool
    estimated_revenue_at_risk: float
    signal: str
    forecast_gap_pct: float
    commit_accuracy_pct: float

    def to_dict(self) -> dict:
        return {
            "composite_score": self.composite_score,
            "risk": self.risk.value,
            "pattern": self.pattern.value,
            "severity": self.severity.value,
            "action": self.action.value,
            "accuracy_score": self.accuracy_score,
            "discipline_score": self.discipline_score,
            "stage_score": self.stage_score,
            "commit_score": self.commit_score,
            "has_forecast_gap": self.has_forecast_gap,
            "requires_forecast_coaching": self.requires_forecast_coaching,
            "estimated_revenue_at_risk": self.estimated_revenue_at_risk,
            "signal": self.signal,
            "forecast_gap_pct": self.forecast_gap_pct,
            "commit_accuracy_pct": self.commit_accuracy_pct,
        }


class SalesForecastAccuracyIntelligenceEngine:

    def _accuracy_score(self, inp: ForecastInput) -> float:
        variance_penalty = min(inp.forecast_variance_pct / 30 * 50, 50)
        commit_lost_penalty = min(inp.commit_lost_pct * 100, 30)
        close_date_penalty = min(inp.close_date_change_avg / 30 * 20, 20)
        raw = 100 - variance_penalty - commit_lost_penalty - close_date_penalty
        return min(max(round(raw, 1), 0.0), 100.0)

    def _discipline_score(self, inp: ForecastInput) -> float:
        change_penalty = min(inp.commit_change_frequency * 100, 40)
        late_add_penalty = min(inp.late_stage_add_rate * 100, 30)
        slip_penalty = min(inp.deals_slipped_last_quarter / max(inp.total_deals, 1) * 100, 20)
        slip_days_penalty = min(inp.avg_slip_days / 30 * 10, 10)
        raw = 100 - change_penalty - late_add_penalty - slip_penalty - slip_days_penalty
        return min(max(round(raw, 1), 0.0), 100.0)

    def _stage_score(self, inp: ForecastInput) -> float:
        pulled_penalty = min(inp.deals_pulled_forward / max(inp.total_deals, 1) * 100, 25)
        raw = inp.stage_accuracy_pct - pulled_penalty
        return min(max(round(raw, 1), 0.0), 100.0)

    def _commit_score(self, inp: ForecastInput) -> float:
        commit_ratio_score = min(inp.commit_to_close_ratio, 1.0) * 80
        hist_bonus = inp.historical_accuracy_pct * 0.20
        over_penalty = min(inp.over_forecast_frequency * 50, 20)
        under_penalty = min(inp.under_forecast_frequency * 50, 20)
        raw = commit_ratio_score + hist_bonus - over_penalty - under_penalty
        return min(max(round(raw, 1), 0.0), 100.0)

    def _composite(self, a: float, d: float, s: float, c: float) -> float:
        return min(round(a * 0.35 + d * 0.25 + s * 0.25 + c * 0.15, 1), 100.0)

    def _risk_level(self, score: float) -> ForecastRisk:
        if score >= 75:
            return ForecastRisk.low
        if score >= 55:
            return ForecastRisk.moderate
        if score >= 35:
            return ForecastRisk.high
        return ForecastRisk.critical

    def _severity(self, risk: ForecastRisk) -> ForecastSeverity:
        return {
            ForecastRisk.low: ForecastSeverity.precise,
            ForecastRisk.moderate: ForecastSeverity.calibrating,
            ForecastRisk.high: ForecastSeverity.drifting,
            ForecastRisk.critical: ForecastSeverity.unreliable,
        }[risk]

    def _detect_pattern(self, inp: ForecastInput, a: float, d: float, s: float, c: float) -> ForecastPattern:
        if s < 50:
            return ForecastPattern.stage_inflation_blindspot
        if inp.over_forecast_frequency > 0.35:
            return ForecastPattern.chronic_over_forecasting
        if inp.deals_slipped_last_quarter > inp.total_deals * 0.20 and inp.avg_slip_days > 20:
            return ForecastPattern.end_of_quarter_cliff
        if inp.under_forecast_frequency > 0.30 and inp.commit_to_close_ratio > 0.9:
            return ForecastPattern.recency_bias_sandbagging
        if inp.under_forecast_frequency > 0.30:
            return ForecastPattern.chronic_under_forecasting
        return ForecastPattern.none

    def _action(self, pattern: ForecastPattern) -> ForecastAction:
        mapping = {
            ForecastPattern.stage_inflation_blindspot: ForecastAction.stage_criteria_coaching,
            ForecastPattern.chronic_over_forecasting: ForecastAction.commit_discipline_coaching,
            ForecastPattern.end_of_quarter_cliff: ForecastAction.forecast_reset_intervention,
            ForecastPattern.recency_bias_sandbagging: ForecastAction.bias_calibration_session,
            ForecastPattern.chronic_under_forecasting: ForecastAction.forecast_reset_intervention,
            ForecastPattern.none: ForecastAction.maintain,
        }
        return mapping[pattern]

    def _has_forecast_gap(self, inp: ForecastInput) -> bool:
        submitted_vs_actual = abs(inp.forecast_submitted - inp.actual_closed) / max(inp.actual_closed, 1)
        return submitted_vs_actual > 0.15 or inp.forecast_variance_pct > 20

    def _requires_forecast_coaching(self, inp: ForecastInput) -> bool:
        return (inp.stage_accuracy_pct < 65
                or inp.over_forecast_frequency > 0.30
                or inp.commit_change_frequency > 0.25)

    def _estimated_revenue_at_risk(self, inp: ForecastInput, score: float) -> float:
        return round(inp.total_deals * inp.avg_deal_value * inp.commit_lost_pct * score / 100, 2)

    def _signal(self, risk: ForecastRisk, pattern: ForecastPattern) -> str:
        if risk == ForecastRisk.low and pattern == ForecastPattern.none:
            return "Forecast accuracy healthy — variance, commit discipline, and stage accuracy within benchmarks"
        signals = {
            ForecastPattern.stage_inflation_blindspot: "Stage accuracy below threshold — deals advanced prematurely, distorting forecast",
            ForecastPattern.chronic_over_forecasting: "Chronic over-forecasting pattern detected — commit discipline coaching required",
            ForecastPattern.end_of_quarter_cliff: "End-of-quarter cliff pattern — high slip rate indicates last-minute deal management",
            ForecastPattern.recency_bias_sandbagging: "Sandbagging pattern — consistent under-forecasting with high close rates",
            ForecastPattern.chronic_under_forecasting: "Chronic under-forecasting — conservative bias limiting pipeline visibility",
            ForecastPattern.none: f"Forecast {risk.value} risk — monitor accuracy and commit discipline",
        }
        return signals.get(pattern, "Forecast accuracy requires attention")

    def _forecast_gap_pct(self, inp: ForecastInput) -> float:
        if inp.actual_closed == 0:
            return 0.0
        return round(abs(inp.forecast_submitted - inp.actual_closed) / inp.actual_closed * 100, 1)

    def _commit_accuracy_pct(self, inp: ForecastInput) -> float:
        total_commit_value = inp.deals_in_commit * inp.avg_deal_value
        return round(min(inp.commit_to_close_ratio * 100, 100.0), 1)

    def assess(self, inp: ForecastInput) -> ForecastResult:
        a = self._accuracy_score(inp)
        d = self._discipline_score(inp)
        s = self._stage_score(inp)
        c = self._commit_score(inp)
        composite = self._composite(a, d, s, c)
        risk = self._risk_level(composite)
        severity = self._severity(risk)
        pattern = self._detect_pattern(inp, a, d, s, c)
        action = self._action(pattern)

        return ForecastResult(
            composite_score=composite,
            risk=risk,
            pattern=pattern,
            severity=severity,
            action=action,
            accuracy_score=a,
            discipline_score=d,
            stage_score=s,
            commit_score=c,
            has_forecast_gap=self._has_forecast_gap(inp),
            requires_forecast_coaching=self._requires_forecast_coaching(inp),
            estimated_revenue_at_risk=self._estimated_revenue_at_risk(inp, composite),
            signal=self._signal(risk, pattern),
            forecast_gap_pct=self._forecast_gap_pct(inp),
            commit_accuracy_pct=self._commit_accuracy_pct(inp),
        )

    def batch(self, inputs: list[ForecastInput]) -> list[ForecastResult]:
        return [self.assess(inp) for inp in inputs]

    def summary(self, results: list[ForecastResult]) -> dict:
        if not results:
            return {}
        scores = [r.composite_score for r in results]
        return {
            "total_reps": len(results),
            "avg_forecast_composite": round(sum(scores) / len(scores), 1),
            "critical_count": sum(1 for r in results if r.risk == ForecastRisk.critical),
            "high_risk_count": sum(1 for r in results if r.risk == ForecastRisk.high),
            "coaching_count": sum(1 for r in results if r.requires_forecast_coaching),
            "forecast_gap_count": sum(1 for r in results if r.has_forecast_gap),
            "top_pattern": max(set(r.pattern.value for r in results), key=lambda p: sum(1 for r in results if r.pattern.value == p)),
            "total_revenue_at_risk": round(sum(r.estimated_revenue_at_risk for r in results), 2),
            "avg_forecast_gap_pct": round(sum(r.forecast_gap_pct for r in results) / len(results), 1),
            "min_score": min(scores),
            "max_score": max(scores),
            "low_risk_pct": round(sum(1 for r in results if r.risk == ForecastRisk.low) / len(results) * 100, 1),
            "stage_coaching_count": sum(1 for r in results if r.action == ForecastAction.stage_criteria_coaching),
        }
