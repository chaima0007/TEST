from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class ForecastRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ForecastPattern(str, Enum):
    none               = "none"
    chronic_overcommit = "chronic_overcommit"
    sandbagger         = "sandbagger"
    volatile_caller    = "volatile_caller"
    stage_inflate      = "stage_inflate"
    late_quarter_crash = "late_quarter_crash"


class ForecastSeverity(str, Enum):
    precise    = "precise"
    acceptable = "acceptable"
    unreliable = "unreliable"
    deceptive  = "deceptive"


class ForecastAction(str, Enum):
    no_action                       = "no_action"
    forecast_calibration_coaching   = "forecast_calibration_coaching"
    pipeline_qualification_coaching = "pipeline_qualification_coaching"
    forecast_discipline_coaching    = "forecast_discipline_coaching"
    forecast_review_escalation      = "forecast_review_escalation"
    manager_override_required       = "manager_override_required"
    forecast_audit                  = "forecast_audit"


@dataclass
class ForecastInput:
    rep_id:                         str
    region:                         str
    evaluation_period_id:           str
    forecast_accuracy_pct:          float   # 0-1 (actuals/forecast)
    avg_commit_variance_pct:        float   # 0-1 (avg abs deviation)
    overcommit_rate_pct:            float   # 0-1 (how often over-called)
    undercommit_rate_pct:           float   # 0-1 (how often under-called)
    late_quarter_slip_rate_pct:     float   # 0-1 (deals slipping Q-end)
    stage_accuracy_pct:             float   # 0-1 (stages match close prob)
    close_date_change_rate_pct:     float   # 0-1 (how often dates pushed)
    pipeline_coverage_ratio:        float   # X.Xx (3.0+ is healthy)
    deal_aging_accuracy_pct:        float   # 0-1 (cycle vs benchmark)
    weighted_pipeline_accuracy_pct: float   # 0-1 (weighted vs actual close)
    commit_vs_actual_delta_pct:     float   # 0-1 (avg per-quarter delta)
    historical_hit_rate_pct:        float   # 0-1 (quarters hitting forecast)
    upside_conversion_rate_pct:     float   # 0-1
    best_case_accuracy_pct:         float   # 0-1
    cfo_adjustment_rate_pct:        float   # 0-1 (how often mgmt adjusts)
    total_committed_pipeline_usd:   float
    total_actual_closed_usd:        float
    quota_usd:                      float
    periods_evaluated:              int


@dataclass
class ForecastResult:
    rep_id:                         str
    region:                         str
    forecast_risk:                  ForecastRisk
    forecast_pattern:               ForecastPattern
    forecast_severity:              ForecastSeverity
    recommended_action:             ForecastAction
    accuracy_score:                 float
    consistency_score:              float
    pipeline_quality_score:         float
    calibration_score:              float
    forecast_composite:             float
    has_forecast_gap:               bool
    requires_forecast_coaching:     bool
    estimated_forecast_error_usd:   float
    forecast_signal:                str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "forecast_risk":                    self.forecast_risk.value,
            "forecast_pattern":                 self.forecast_pattern.value,
            "forecast_severity":                self.forecast_severity.value,
            "recommended_action":               self.recommended_action.value,
            "accuracy_score":                   self.accuracy_score,
            "consistency_score":                self.consistency_score,
            "pipeline_quality_score":           self.pipeline_quality_score,
            "calibration_score":                self.calibration_score,
            "forecast_composite":               self.forecast_composite,
            "has_forecast_gap":                 self.has_forecast_gap,
            "requires_forecast_coaching":       self.requires_forecast_coaching,
            "estimated_forecast_error_usd":     self.estimated_forecast_error_usd,
            "forecast_signal":                  self.forecast_signal,
        }


class SalesForecastAccuracyIntelligenceEngine:
    """Detects per-rep forecast reliability issues — overcommit, sandbagging, late-quarter crashes."""

    def __init__(self) -> None:
        self._results: List[ForecastResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────

    def _accuracy_score(self, inp: ForecastInput) -> float:
        s = 0.0
        if   inp.forecast_accuracy_pct          <= 0.70: s += 40
        elif inp.forecast_accuracy_pct          <= 0.85: s += 22
        elif inp.forecast_accuracy_pct          <= 0.93: s += 8
        if   inp.historical_hit_rate_pct        <= 0.40: s += 35
        elif inp.historical_hit_rate_pct        <= 0.60: s += 18
        if   inp.commit_vs_actual_delta_pct     >= 0.25: s += 25
        elif inp.commit_vs_actual_delta_pct     >= 0.12: s += 12
        return min(s, 100.0)

    def _consistency_score(self, inp: ForecastInput) -> float:
        s = 0.0
        if   inp.avg_commit_variance_pct        >= 0.30: s += 40
        elif inp.avg_commit_variance_pct        >= 0.20: s += 22
        elif inp.avg_commit_variance_pct        >= 0.12: s += 8
        if   inp.close_date_change_rate_pct     >= 0.50: s += 35
        elif inp.close_date_change_rate_pct     >= 0.30: s += 18
        if   inp.late_quarter_slip_rate_pct     >= 0.35: s += 25
        elif inp.late_quarter_slip_rate_pct     >= 0.20: s += 12
        return min(s, 100.0)

    def _pipeline_quality_score(self, inp: ForecastInput) -> float:
        s = 0.0
        if   inp.pipeline_coverage_ratio        <= 1.5: s += 40
        elif inp.pipeline_coverage_ratio        <= 2.0: s += 22
        elif inp.pipeline_coverage_ratio        <= 2.5: s += 8
        if   inp.stage_accuracy_pct             <= 0.50: s += 35
        elif inp.stage_accuracy_pct             <= 0.70: s += 18
        if   inp.weighted_pipeline_accuracy_pct <= 0.55: s += 25
        elif inp.weighted_pipeline_accuracy_pct <= 0.75: s += 12
        return min(s, 100.0)

    def _calibration_score(self, inp: ForecastInput) -> float:
        s = 0.0
        if   inp.cfo_adjustment_rate_pct        >= 0.50: s += 45
        elif inp.cfo_adjustment_rate_pct        >= 0.30: s += 25
        elif inp.cfo_adjustment_rate_pct        >= 0.15: s += 10
        if   inp.upside_conversion_rate_pct     <= 0.20: s += 30
        elif inp.upside_conversion_rate_pct     <= 0.40: s += 15
        if   inp.best_case_accuracy_pct         <= 0.40: s += 25
        elif inp.best_case_accuracy_pct         <= 0.60: s += 12
        return min(s, 100.0)

    # ── composite ─────────────────────────────────────────────────────────

    def _composite(self, ac: float, co: float, pq: float, ca: float) -> float:
        return min(round(ac * 0.35 + co * 0.25 + pq * 0.25 + ca * 0.15, 2), 100.0)

    # ── pattern ───────────────────────────────────────────────────────────

    def _pattern(self, inp: ForecastInput) -> ForecastPattern:
        if inp.overcommit_rate_pct >= 0.60 and inp.forecast_accuracy_pct <= 0.75:
            return ForecastPattern.chronic_overcommit
        if inp.undercommit_rate_pct >= 0.60 and inp.historical_hit_rate_pct >= 0.85:
            return ForecastPattern.sandbagger
        if inp.avg_commit_variance_pct >= 0.25 and inp.close_date_change_rate_pct >= 0.45:
            return ForecastPattern.volatile_caller
        if inp.stage_accuracy_pct <= 0.45 and inp.weighted_pipeline_accuracy_pct <= 0.55:
            return ForecastPattern.stage_inflate
        if inp.late_quarter_slip_rate_pct >= 0.35 and inp.commit_vs_actual_delta_pct >= 0.20:
            return ForecastPattern.late_quarter_crash
        return ForecastPattern.none

    # ── thresholds ────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> ForecastRisk:
        if   composite >= 60: return ForecastRisk.critical
        elif composite >= 40: return ForecastRisk.high
        elif composite >= 20: return ForecastRisk.moderate
        return ForecastRisk.low

    def _severity(self, composite: float) -> ForecastSeverity:
        if   composite >= 60: return ForecastSeverity.deceptive
        elif composite >= 40: return ForecastSeverity.unreliable
        elif composite >= 20: return ForecastSeverity.acceptable
        return ForecastSeverity.precise

    def _action(self, risk: ForecastRisk, pattern: ForecastPattern) -> ForecastAction:
        if risk == ForecastRisk.critical:
            if pattern in (ForecastPattern.chronic_overcommit, ForecastPattern.stage_inflate):
                return ForecastAction.forecast_audit
            return ForecastAction.manager_override_required
        if risk == ForecastRisk.high:
            if pattern == ForecastPattern.chronic_overcommit:
                return ForecastAction.forecast_discipline_coaching
            if pattern == ForecastPattern.sandbagger:
                return ForecastAction.forecast_calibration_coaching
            if pattern == ForecastPattern.volatile_caller:
                return ForecastAction.forecast_review_escalation
            if pattern == ForecastPattern.stage_inflate:
                return ForecastAction.pipeline_qualification_coaching
            if pattern == ForecastPattern.late_quarter_crash:
                return ForecastAction.forecast_review_escalation
            return ForecastAction.forecast_discipline_coaching
        if risk == ForecastRisk.moderate:
            return ForecastAction.forecast_calibration_coaching
        return ForecastAction.no_action

    # ── flags ─────────────────────────────────────────────────────────────

    def _has_gap(self, inp: ForecastInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.forecast_accuracy_pct     <= 0.85
            or inp.late_quarter_slip_rate_pct >= 0.25
        )

    def _requires_coaching(self, inp: ForecastInput, composite: float) -> bool:
        return (
            composite >= 25
            or inp.avg_commit_variance_pct   >= 0.15
            or inp.cfo_adjustment_rate_pct   >= 0.20
        )

    # ── dollar impact ─────────────────────────────────────────────────────

    def _forecast_error(self, inp: ForecastInput) -> float:
        error = abs(inp.total_committed_pipeline_usd - inp.total_actual_closed_usd)
        return round(error, 2)

    # ── signal ────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        ForecastPattern.chronic_overcommit: "Chronic overcommit",
        ForecastPattern.sandbagger:         "Sandbagger",
        ForecastPattern.volatile_caller:    "Volatile caller",
        ForecastPattern.stage_inflate:      "Stage inflate",
        ForecastPattern.late_quarter_crash: "Late-quarter crash",
    }

    def _signal(self, inp: ForecastInput, pattern: ForecastPattern, composite: float) -> str:
        if composite < 20:
            return (
                "Forecast accuracy strong — commit variance, pipeline quality, "
                "stage accuracy, and calibration within benchmarks"
            )
        label     = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        acc_pct   = round(inp.forecast_accuracy_pct * 100)
        var_pct   = round(inp.avg_commit_variance_pct * 100)
        slip_pct  = round(inp.late_quarter_slip_rate_pct * 100)
        comp_int  = round(composite)
        return (
            f"{label} — {acc_pct}% forecast accuracy — "
            f"{var_pct}% avg commit variance — "
            f"{slip_pct}% late-quarter slip rate — composite {comp_int}"
        )

    # ── public API ────────────────────────────────────────────────────────

    def assess(self, inp: ForecastInput) -> ForecastResult:
        ac  = self._accuracy_score(inp)
        co  = self._consistency_score(inp)
        pq  = self._pipeline_quality_score(inp)
        ca  = self._calibration_score(inp)
        comp = self._composite(ac, co, pq, ca)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = ForecastResult(
            rep_id                      = inp.rep_id,
            region                      = inp.region,
            forecast_risk               = risk,
            forecast_pattern            = pattern,
            forecast_severity           = severity,
            recommended_action          = action,
            accuracy_score              = ac,
            consistency_score           = co,
            pipeline_quality_score      = pq,
            calibration_score           = ca,
            forecast_composite          = comp,
            has_forecast_gap            = self._has_gap(inp, comp),
            requires_forecast_coaching  = self._requires_coaching(inp, comp),
            estimated_forecast_error_usd= self._forecast_error(inp),
            forecast_signal             = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[ForecastInput]) -> List[ForecastResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
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
                "avg_consistency_score": 0.0,
                "avg_pipeline_quality_score": 0.0,
                "avg_calibration_score": 0.0,
                "total_estimated_forecast_error_usd": 0.0,
            }

        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        total_comp = total_ac = total_co = total_pq = total_ca = total_fe = 0.0
        gap_count = coaching_count = 0

        for res in self._results:
            risk_counts[res.forecast_risk.value]       = risk_counts.get(res.forecast_risk.value, 0) + 1
            pattern_counts[res.forecast_pattern.value] = pattern_counts.get(res.forecast_pattern.value, 0) + 1
            severity_counts[res.forecast_severity.value] = severity_counts.get(res.forecast_severity.value, 0) + 1
            action_counts[res.recommended_action.value] = action_counts.get(res.recommended_action.value, 0) + 1
            total_comp += res.forecast_composite
            total_ac   += res.accuracy_score
            total_co   += res.consistency_score
            total_pq   += res.pipeline_quality_score
            total_ca   += res.calibration_score
            total_fe   += res.estimated_forecast_error_usd
            if res.has_forecast_gap:          gap_count      += 1
            if res.requires_forecast_coaching: coaching_count += 1

        n = len(self._results)
        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_forecast_composite":               round(total_comp / n, 1),
            "forecast_gap_count":                   gap_count,
            "coaching_count":                       coaching_count,
            "avg_accuracy_score":                   round(total_ac / n, 1),
            "avg_consistency_score":                round(total_co / n, 1),
            "avg_pipeline_quality_score":           round(total_pq / n, 1),
            "avg_calibration_score":                round(total_ca / n, 1),
            "total_estimated_forecast_error_usd":   round(total_fe, 2),
        }
