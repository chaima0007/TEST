from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class ForecastRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ForecastPattern(str, Enum):
    none                     = "none"
    overforecast_bias        = "overforecast_bias"
    sandbag_bias             = "sandbag_bias"
    late_quarter_stuffing    = "late_quarter_stuffing"
    stage_inflation          = "stage_inflation"
    history_disconnect       = "history_disconnect"


class ForecastSeverity(str, Enum):
    accurate    = "accurate"
    drifting    = "drifting"
    unreliable  = "unreliable"
    distorted   = "distorted"


class ForecastAction(str, Enum):
    no_action                       = "no_action"
    forecast_review_coaching        = "forecast_review_coaching"
    pipeline_validation_session     = "pipeline_validation_session"
    deal_stage_audit                = "deal_stage_audit"
    historical_recalibration        = "historical_recalibration"
    forecast_override_intervention  = "forecast_override_intervention"


@dataclass
class ForecastSanityCheckInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    current_forecast_usd: float
    historical_avg_attainment_pct: float
    quota_usd: float
    pipeline_coverage_ratio: float
    avg_deal_age_in_forecast_days: float
    deals_added_last_7d_count: int
    deals_pulled_in_from_next_qtr_count: int
    stage_3_plus_deal_count: int
    stage_3_plus_avg_age_days: float
    forecast_vs_prior_week_delta_pct: float
    manual_forecast_override_count: int
    won_deals_ytd_count: int
    lost_deals_ytd_count: int
    avg_days_in_stage_before_advance: float
    late_quarter_close_date_count: int
    total_forecast_deals: int
    close_date_pushed_count: int
    avg_opportunity_value_usd: float
    crm_signal_quality_score: float


@dataclass
class ForecastSanityCheckResult:
    rep_id: str
    region: str
    forecast_risk: ForecastRisk
    forecast_pattern: ForecastPattern
    forecast_severity: ForecastSeverity
    recommended_action: ForecastAction
    overforecast_bias_score: float
    pipeline_quality_score: float
    stage_integrity_score: float
    history_alignment_score: float
    forecast_sanity_composite: float
    has_forecast_gap: bool
    requires_forecast_review: bool
    estimated_forecast_variance_usd: float
    forecast_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "forecast_risk":                    self.forecast_risk.value,
            "forecast_pattern":                 self.forecast_pattern.value,
            "forecast_severity":                self.forecast_severity.value,
            "recommended_action":               self.recommended_action.value,
            "overforecast_bias_score":          self.overforecast_bias_score,
            "pipeline_quality_score":           self.pipeline_quality_score,
            "stage_integrity_score":            self.stage_integrity_score,
            "history_alignment_score":          self.history_alignment_score,
            "forecast_sanity_composite":        self.forecast_sanity_composite,
            "has_forecast_gap":                 self.has_forecast_gap,
            "requires_forecast_review":         self.requires_forecast_review,
            "estimated_forecast_variance_usd":  self.estimated_forecast_variance_usd,
            "forecast_signal":                  self.forecast_signal,
        }


class SalesForecastSanityCheckIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[ForecastSanityCheckResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _overforecast_bias_score(self, inp: ForecastSanityCheckInput) -> float:
        score = 0.0

        expected = inp.quota_usd * inp.historical_avg_attainment_pct
        if expected > 0:
            overforecast_ratio = (inp.current_forecast_usd - expected) / expected
            if overforecast_ratio >= 0.30:
                score += 40.0
            elif overforecast_ratio >= 0.15:
                score += 20.0
            elif overforecast_ratio >= 0.05:
                score += 8.0

        if inp.forecast_vs_prior_week_delta_pct >= 0.20:
            score += 30.0
        elif inp.forecast_vs_prior_week_delta_pct >= 0.10:
            score += 15.0

        total = max(inp.total_forecast_deals, 1)
        pull_in_rate = inp.deals_pulled_in_from_next_qtr_count / total
        if pull_in_rate >= 0.20:
            score += 25.0
        elif pull_in_rate >= 0.10:
            score += 12.0

        return min(score, 100.0)

    def _pipeline_quality_score(self, inp: ForecastSanityCheckInput) -> float:
        score = 0.0

        if inp.pipeline_coverage_ratio < 2.0:
            score += 35.0
        elif inp.pipeline_coverage_ratio < 2.5:
            score += 18.0
        elif inp.pipeline_coverage_ratio < 3.0:
            score += 7.0

        total = max(inp.total_forecast_deals, 1)
        push_rate = inp.close_date_pushed_count / total
        if push_rate >= 0.30:
            score += 35.0
        elif push_rate >= 0.15:
            score += 18.0
        elif push_rate >= 0.05:
            score += 7.0

        if inp.crm_signal_quality_score < 0.40:
            score += 25.0
        elif inp.crm_signal_quality_score < 0.60:
            score += 12.0

        return min(score, 100.0)

    def _stage_integrity_score(self, inp: ForecastSanityCheckInput) -> float:
        score = 0.0

        if inp.stage_3_plus_avg_age_days >= 60.0:
            score += 40.0
        elif inp.stage_3_plus_avg_age_days >= 45.0:
            score += 22.0
        elif inp.stage_3_plus_avg_age_days >= 30.0:
            score += 8.0

        if inp.avg_days_in_stage_before_advance >= 20.0:
            score += 30.0
        elif inp.avg_days_in_stage_before_advance >= 12.0:
            score += 15.0

        total = max(inp.total_forecast_deals, 1)
        late_close_rate = inp.late_quarter_close_date_count / total
        if late_close_rate >= 0.50:
            score += 25.0
        elif late_close_rate >= 0.30:
            score += 12.0

        return min(score, 100.0)

    def _history_alignment_score(self, inp: ForecastSanityCheckInput) -> float:
        score = 0.0

        total_closed = max(inp.won_deals_ytd_count + inp.lost_deals_ytd_count, 1)
        win_rate = inp.won_deals_ytd_count / total_closed
        if inp.historical_avg_attainment_pct > 0.0:
            implied_win_rate = inp.historical_avg_attainment_pct
            win_rate_gap = implied_win_rate - win_rate
            if win_rate_gap >= 0.20:
                score += 40.0
            elif win_rate_gap >= 0.10:
                score += 20.0
            elif win_rate_gap >= 0.05:
                score += 8.0

        if inp.manual_forecast_override_count >= 5:
            score += 35.0
        elif inp.manual_forecast_override_count >= 2:
            score += 18.0
        elif inp.manual_forecast_override_count >= 1:
            score += 7.0

        if inp.avg_deal_age_in_forecast_days >= 90.0:
            score += 20.0
        elif inp.avg_deal_age_in_forecast_days >= 60.0:
            score += 10.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: ForecastSanityCheckInput,
                          over: float, pipeline: float,
                          stage: float, history: float) -> ForecastPattern:
        expected = inp.quota_usd * inp.historical_avg_attainment_pct
        if expected > 0 and over >= 30 and (inp.current_forecast_usd - expected) / expected >= 0.25:
            return ForecastPattern.overforecast_bias

        total = max(inp.total_forecast_deals, 1)
        pull_in_rate = inp.deals_pulled_in_from_next_qtr_count / total
        late_rate = inp.late_quarter_close_date_count / total
        if over >= 20 and (pull_in_rate >= 0.15 or late_rate >= 0.40):
            return ForecastPattern.late_quarter_stuffing

        if stage >= 30 and inp.stage_3_plus_avg_age_days >= 45.0:
            return ForecastPattern.stage_inflation

        if history >= 30 and inp.manual_forecast_override_count >= 2:
            return ForecastPattern.history_disconnect

        expected_low = inp.quota_usd * inp.historical_avg_attainment_pct
        if expected_low > 0 and (inp.current_forecast_usd / expected_low) < 0.70 and inp.pipeline_coverage_ratio >= 3.5:
            return ForecastPattern.sandbag_bias

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
            return ForecastSeverity.distorted
        if composite >= 40:
            return ForecastSeverity.unreliable
        if composite >= 20:
            return ForecastSeverity.drifting
        return ForecastSeverity.accurate

    def _action(self, risk: ForecastRisk, pattern: ForecastPattern) -> ForecastAction:
        if risk == ForecastRisk.critical:
            if pattern == ForecastPattern.overforecast_bias:
                return ForecastAction.forecast_override_intervention
            if pattern == ForecastPattern.stage_inflation:
                return ForecastAction.deal_stage_audit
            return ForecastAction.forecast_override_intervention
        if risk == ForecastRisk.high:
            if pattern == ForecastPattern.history_disconnect:
                return ForecastAction.historical_recalibration
            if pattern == ForecastPattern.late_quarter_stuffing:
                return ForecastAction.pipeline_validation_session
            return ForecastAction.forecast_review_coaching
        if risk == ForecastRisk.moderate:
            return ForecastAction.forecast_review_coaching
        return ForecastAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_forecast_gap(self, composite: float,
                           inp: ForecastSanityCheckInput) -> bool:
        expected = inp.quota_usd * inp.historical_avg_attainment_pct
        return (
            composite >= 40
            or inp.manual_forecast_override_count >= 3
            or (expected > 0 and abs(inp.current_forecast_usd - expected) / expected >= 0.25)
        )

    def _requires_forecast_review(self, composite: float,
                                    inp: ForecastSanityCheckInput) -> bool:
        total = max(inp.total_forecast_deals, 1)
        push_rate = inp.close_date_pushed_count / total
        return (
            composite >= 30
            or push_rate >= 0.20
            or inp.manual_forecast_override_count >= 2
        )

    # ------------------------------------------------------------------
    # Forecast variance
    # ------------------------------------------------------------------

    def _estimated_forecast_variance(self, inp: ForecastSanityCheckInput,
                                      composite: float) -> float:
        expected = inp.quota_usd * inp.historical_avg_attainment_pct
        raw_variance = abs(inp.current_forecast_usd - expected)
        return round(raw_variance * (composite / 100.0), 2)

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: ForecastSanityCheckInput,
                 pattern: ForecastPattern, composite: float) -> str:
        if pattern == ForecastPattern.none and composite < 20:
            return "Forecast accuracy healthy — historical alignment and pipeline quality within benchmarks"
        parts: list[str] = []
        expected = inp.quota_usd * inp.historical_avg_attainment_pct
        if expected > 0:
            ratio = inp.current_forecast_usd / expected
            parts.append(f"{ratio*100:.0f}% of expected attainment")
        if inp.manual_forecast_override_count > 0:
            parts.append(f"{inp.manual_forecast_override_count} manual overrides")
        if inp.close_date_pushed_count > 0:
            total = max(inp.total_forecast_deals, 1)
            parts.append(f"{inp.close_date_pushed_count/total*100:.0f}% close dates pushed")
        label = pattern.value.replace("_", " ") if pattern != ForecastPattern.none else "Forecast risk"
        summary = " — ".join(parts) if parts else "forecast accuracy declining"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: ForecastSanityCheckInput) -> ForecastSanityCheckResult:
        over      = round(self._overforecast_bias_score(inp), 1)
        pipeline  = round(self._pipeline_quality_score(inp), 1)
        stage     = round(self._stage_integrity_score(inp), 1)
        history   = round(self._history_alignment_score(inp), 1)

        composite = round(
            over * 0.30 + pipeline * 0.30 + stage * 0.25 + history * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, over, pipeline, stage, history)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap      = self._has_forecast_gap(composite, inp)
        review   = self._requires_forecast_review(composite, inp)
        variance = self._estimated_forecast_variance(inp, composite)
        signal   = self._signal(inp, pattern, composite)

        result = ForecastSanityCheckResult(
            rep_id=inp.rep_id,
            region=inp.region,
            forecast_risk=risk,
            forecast_pattern=pattern,
            forecast_severity=severity,
            recommended_action=action,
            overforecast_bias_score=over,
            pipeline_quality_score=pipeline,
            stage_integrity_score=stage,
            history_alignment_score=history,
            forecast_sanity_composite=composite,
            has_forecast_gap=gap,
            requires_forecast_review=review,
            estimated_forecast_variance_usd=variance,
            forecast_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[ForecastSanityCheckInput]) -> list[ForecastSanityCheckResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_forecast_sanity_composite": 0.0,
                "forecast_gap_count": 0,
                "review_required_count": 0,
                "avg_overforecast_bias_score": 0.0,
                "avg_pipeline_quality_score": 0.0,
                "avg_stage_integrity_score": 0.0,
                "avg_history_alignment_score": 0.0,
                "total_estimated_forecast_variance_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_over = total_pipe = total_stage = total_hist = total_var = 0.0

        for r in self._results:
            risk_counts[r.forecast_risk.value]       = risk_counts.get(r.forecast_risk.value, 0) + 1
            pattern_counts[r.forecast_pattern.value] = pattern_counts.get(r.forecast_pattern.value, 0) + 1
            severity_counts[r.forecast_severity.value] = severity_counts.get(r.forecast_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp  += r.forecast_sanity_composite
            total_over  += r.overforecast_bias_score
            total_pipe  += r.pipeline_quality_score
            total_stage += r.stage_integrity_score
            total_hist  += r.history_alignment_score
            total_var   += r.estimated_forecast_variance_usd

        n = len(self._results)

        return {
            "total":                                    n,
            "risk_counts":                              risk_counts,
            "pattern_counts":                           pattern_counts,
            "severity_counts":                          severity_counts,
            "action_counts":                            action_counts,
            "avg_forecast_sanity_composite":            round(total_comp / n, 1),
            "forecast_gap_count":                       sum(1 for r in self._results if r.has_forecast_gap),
            "review_required_count":                    sum(1 for r in self._results if r.requires_forecast_review),
            "avg_overforecast_bias_score":              round(total_over / n, 1),
            "avg_pipeline_quality_score":               round(total_pipe / n, 1),
            "avg_stage_integrity_score":                round(total_stage / n, 1),
            "avg_history_alignment_score":              round(total_hist / n, 1),
            "total_estimated_forecast_variance_usd":    round(total_var, 2),
        }
