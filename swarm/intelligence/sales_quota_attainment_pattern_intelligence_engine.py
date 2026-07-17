from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class QuotaRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class QuotaPattern(str, Enum):
    none                          = "none"
    sandbagging                   = "sandbagging"
    feast_or_famine               = "feast_or_famine"
    late_quarter_cliff            = "late_quarter_cliff"
    early_coasting                = "early_coasting"
    consistent_underperformance   = "consistent_underperformance"


class QuotaSeverity(str, Enum):
    disciplined   = "disciplined"
    developing    = "developing"
    inconsistent  = "inconsistent"
    at_risk       = "at_risk"


class QuotaAction(str, Enum):
    no_action                     = "no_action"
    pipeline_pacing_coaching      = "pipeline_pacing_coaching"
    activity_rhythm_coaching      = "activity_rhythm_coaching"
    forecast_accuracy_training    = "forecast_accuracy_training"
    performance_improvement_plan  = "performance_improvement_plan"
    quota_reset_review            = "quota_reset_review"


@dataclass
class QuotaInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    quota_attainment_pct: float
    prior_quarter_attainment_pct: float
    attainment_variance_pct: float
    pct_quota_achieved_by_month1_end: float
    pct_quota_achieved_by_month2_end: float
    pct_deals_closed_in_final_2_weeks_pct: float
    avg_monthly_bookings_variance_pct: float
    forecast_accuracy_pct: float
    commit_to_close_rate_pct: float
    pipeline_coverage_ratio: float
    avg_deal_size_usd: float
    total_deals_closed: int
    deals_pushed_to_next_quarter_pct: float
    discount_rate_avg_pct: float
    new_logo_pct: float
    expansion_revenue_pct: float
    avg_sales_cycle_days: float
    quarters_above_quota_last_4: int
    avg_opportunity_value_usd: float


@dataclass
class QuotaResult:
    rep_id: str
    region: str
    quota_risk: QuotaRisk
    quota_pattern: QuotaPattern
    quota_severity: QuotaSeverity
    recommended_action: QuotaAction
    pacing_score: float
    consistency_score: float
    forecast_score: float
    pipeline_health_score: float
    quota_composite: float
    has_quota_gap: bool
    requires_quota_coaching: bool
    estimated_revenue_at_risk_usd: float
    quota_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                         self.rep_id,
            "region":                         self.region,
            "quota_risk":                     self.quota_risk.value,
            "quota_pattern":                  self.quota_pattern.value,
            "quota_severity":                 self.quota_severity.value,
            "recommended_action":             self.recommended_action.value,
            "pacing_score":                   self.pacing_score,
            "consistency_score":              self.consistency_score,
            "forecast_score":                 self.forecast_score,
            "pipeline_health_score":          self.pipeline_health_score,
            "quota_composite":                self.quota_composite,
            "has_quota_gap":                  self.has_quota_gap,
            "requires_quota_coaching":        self.requires_quota_coaching,
            "estimated_revenue_at_risk_usd":  self.estimated_revenue_at_risk_usd,
            "quota_signal":                   self.quota_signal,
        }


class SalesQuotaAttainmentPatternIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[QuotaResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _pacing_score(self, inp: QuotaInput) -> float:
        """Risk from back-loaded / cliff-edge closing patterns."""
        score = 0.0

        if inp.pct_deals_closed_in_final_2_weeks_pct >= 0.60:
            score += 40.0
        elif inp.pct_deals_closed_in_final_2_weeks_pct >= 0.40:
            score += 22.0
        elif inp.pct_deals_closed_in_final_2_weeks_pct >= 0.25:
            score += 8.0

        if inp.pct_quota_achieved_by_month1_end <= 0.15:
            score += 35.0
        elif inp.pct_quota_achieved_by_month1_end <= 0.30:
            score += 18.0

        if inp.deals_pushed_to_next_quarter_pct >= 0.35:
            score += 25.0
        elif inp.deals_pushed_to_next_quarter_pct >= 0.20:
            score += 12.0

        return min(score, 100.0)

    def _consistency_score(self, inp: QuotaInput) -> float:
        """Risk from feast-or-famine / high variance attainment."""
        score = 0.0

        if inp.attainment_variance_pct >= 0.50:
            score += 40.0
        elif inp.attainment_variance_pct >= 0.30:
            score += 22.0
        elif inp.attainment_variance_pct >= 0.15:
            score += 8.0

        if inp.avg_monthly_bookings_variance_pct >= 0.60:
            score += 35.0
        elif inp.avg_monthly_bookings_variance_pct >= 0.35:
            score += 18.0

        if inp.quarters_above_quota_last_4 <= 1:
            score += 25.0
        elif inp.quarters_above_quota_last_4 <= 2:
            score += 12.0

        return min(score, 100.0)

    def _forecast_score(self, inp: QuotaInput) -> float:
        """Risk from poor forecast accuracy and commit reliability."""
        score = 0.0

        if inp.forecast_accuracy_pct <= 0.60:
            score += 40.0
        elif inp.forecast_accuracy_pct <= 0.75:
            score += 22.0
        elif inp.forecast_accuracy_pct <= 0.85:
            score += 8.0

        if inp.commit_to_close_rate_pct <= 0.50:
            score += 35.0
        elif inp.commit_to_close_rate_pct <= 0.70:
            score += 18.0

        if inp.prior_quarter_attainment_pct < 0.80:
            score += 25.0
        elif inp.prior_quarter_attainment_pct < 1.00:
            score += 12.0

        return min(score, 100.0)

    def _pipeline_health_score(self, inp: QuotaInput) -> float:
        """Risk from thin / unhealthy pipeline composition."""
        score = 0.0

        if inp.pipeline_coverage_ratio <= 2.0:
            score += 45.0
        elif inp.pipeline_coverage_ratio <= 3.0:
            score += 25.0
        elif inp.pipeline_coverage_ratio <= 4.0:
            score += 10.0

        if inp.discount_rate_avg_pct >= 0.30:
            score += 30.0
        elif inp.discount_rate_avg_pct >= 0.20:
            score += 15.0

        if inp.new_logo_pct <= 0.10:
            score += 25.0
        elif inp.new_logo_pct <= 0.25:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: QuotaInput,
                         pacing: float, consistency: float,
                         forecast: float, pipeline: float) -> QuotaPattern:
        # Consistent underperformance: low quarters above quota + high forecast miss
        if inp.quarters_above_quota_last_4 <= 1 and forecast >= 30:
            return QuotaPattern.consistent_underperformance

        # Sandbagging: high close-rate commit but deals pushed to next quarter
        if inp.commit_to_close_rate_pct >= 0.85 and inp.deals_pushed_to_next_quarter_pct >= 0.30:
            return QuotaPattern.sandbagging

        # Feast-or-famine: very high monthly variance
        if consistency >= 35 and inp.avg_monthly_bookings_variance_pct >= 0.50:
            return QuotaPattern.feast_or_famine

        # Late-quarter cliff: majority of deals in final 2 weeks
        if pacing >= 30 and inp.pct_deals_closed_in_final_2_weeks_pct >= 0.50:
            return QuotaPattern.late_quarter_cliff

        # Early coasting: strong month-1 but poor overall pacing discipline
        if inp.pct_quota_achieved_by_month1_end >= 0.50 and inp.pct_quota_achieved_by_month2_end <= 0.65:
            return QuotaPattern.early_coasting

        return QuotaPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> QuotaRisk:
        if composite >= 60:
            return QuotaRisk.critical
        if composite >= 40:
            return QuotaRisk.high
        if composite >= 20:
            return QuotaRisk.moderate
        return QuotaRisk.low

    def _severity(self, composite: float) -> QuotaSeverity:
        if composite >= 60:
            return QuotaSeverity.at_risk
        if composite >= 40:
            return QuotaSeverity.inconsistent
        if composite >= 20:
            return QuotaSeverity.developing
        return QuotaSeverity.disciplined

    def _action(self, risk: QuotaRisk, pattern: QuotaPattern) -> QuotaAction:
        if risk == QuotaRisk.critical:
            if pattern == QuotaPattern.consistent_underperformance:
                return QuotaAction.performance_improvement_plan
            if pattern == QuotaPattern.sandbagging:
                return QuotaAction.forecast_accuracy_training
            return QuotaAction.quota_reset_review
        if risk == QuotaRisk.high:
            if pattern == QuotaPattern.feast_or_famine:
                return QuotaAction.activity_rhythm_coaching
            if pattern == QuotaPattern.late_quarter_cliff:
                return QuotaAction.pipeline_pacing_coaching
            return QuotaAction.pipeline_pacing_coaching
        if risk == QuotaRisk.moderate:
            return QuotaAction.pipeline_pacing_coaching
        return QuotaAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_quota_gap(self, composite: float, inp: QuotaInput) -> bool:
        return (
            composite >= 40
            or inp.quota_attainment_pct < 0.80
            or inp.quarters_above_quota_last_4 <= 1
        )

    def _requires_quota_coaching(self, composite: float, inp: QuotaInput) -> bool:
        return (
            composite >= 30
            or inp.forecast_accuracy_pct < 0.75
            or inp.deals_pushed_to_next_quarter_pct >= 0.25
        )

    # ------------------------------------------------------------------
    # Revenue at risk
    # ------------------------------------------------------------------

    def _estimated_revenue_at_risk(self, inp: QuotaInput, composite: float) -> float:
        return round(
            inp.total_deals_closed
            * inp.avg_opportunity_value_usd
            * (1.0 - inp.quota_attainment_pct)
            * (composite / 100.0),
            2,
        )

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: QuotaInput,
                 pattern: QuotaPattern, composite: float) -> str:
        if pattern == QuotaPattern.none and composite < 20:
            return "Quota attainment healthy — pacing, consistency, and forecast accuracy within benchmarks"
        parts: list[str] = []
        parts.append(f"{inp.quota_attainment_pct * 100:.0f}% quota attained")
        parts.append(f"{inp.pct_deals_closed_in_final_2_weeks_pct * 100:.0f}% deals in final 2 weeks")
        parts.append(f"{inp.forecast_accuracy_pct * 100:.0f}% forecast accuracy")
        label = pattern.value.replace("_", " ") if pattern != QuotaPattern.none else "Quota risk"
        return f"{label.capitalize()} — {' — '.join(parts)} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: QuotaInput) -> QuotaResult:
        pacing      = round(self._pacing_score(inp), 1)
        consistency = round(self._consistency_score(inp), 1)
        forecast    = round(self._forecast_score(inp), 1)
        pipeline    = round(self._pipeline_health_score(inp), 1)

        composite = round(
            pacing * 0.30 + consistency * 0.30 + forecast * 0.25 + pipeline * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, pacing, consistency, forecast, pipeline)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap    = self._has_quota_gap(composite, inp)
        coach  = self._requires_quota_coaching(composite, inp)
        loss   = self._estimated_revenue_at_risk(inp, composite)
        signal = self._signal(inp, pattern, composite)

        result = QuotaResult(
            rep_id=inp.rep_id,
            region=inp.region,
            quota_risk=risk,
            quota_pattern=pattern,
            quota_severity=severity,
            recommended_action=action,
            pacing_score=pacing,
            consistency_score=consistency,
            forecast_score=forecast,
            pipeline_health_score=pipeline,
            quota_composite=composite,
            has_quota_gap=gap,
            requires_quota_coaching=coach,
            estimated_revenue_at_risk_usd=loss,
            quota_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[QuotaInput]) -> list[QuotaResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_quota_composite": 0.0,
                "quota_gap_count": 0,
                "coaching_count": 0,
                "avg_pacing_score": 0.0,
                "avg_consistency_score": 0.0,
                "avg_forecast_score": 0.0,
                "avg_pipeline_health_score": 0.0,
                "total_estimated_revenue_at_risk_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_pac = total_con = total_for = total_pip = total_loss = 0.0

        for r in self._results:
            risk_counts[r.quota_risk.value]       = risk_counts.get(r.quota_risk.value, 0) + 1
            pattern_counts[r.quota_pattern.value] = pattern_counts.get(r.quota_pattern.value, 0) + 1
            severity_counts[r.quota_severity.value] = severity_counts.get(r.quota_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.quota_composite
            total_pac  += r.pacing_score
            total_con  += r.consistency_score
            total_for  += r.forecast_score
            total_pip  += r.pipeline_health_score
            total_loss += r.estimated_revenue_at_risk_usd

        n = len(self._results)

        return {
            "total":                                   n,
            "risk_counts":                             risk_counts,
            "pattern_counts":                          pattern_counts,
            "severity_counts":                         severity_counts,
            "action_counts":                           action_counts,
            "avg_quota_composite":                     round(total_comp / n, 1),
            "quota_gap_count":                         sum(1 for r in self._results if r.has_quota_gap),
            "coaching_count":                          sum(1 for r in self._results if r.requires_quota_coaching),
            "avg_pacing_score":                        round(total_pac / n, 1),
            "avg_consistency_score":                   round(total_con / n, 1),
            "avg_forecast_score":                      round(total_for / n, 1),
            "avg_pipeline_health_score":               round(total_pip / n, 1),
            "total_estimated_revenue_at_risk_usd":     round(total_loss, 2),
        }
