from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class QuotaRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class QuotaPattern(str, Enum):
    none                      = "none"
    consistent_underperformance = "consistent_underperformance"
    sandbagging               = "sandbagging"
    late_quarter_surge        = "late_quarter_surge"
    early_drop_off            = "early_drop_off"
    quota_avoidance           = "quota_avoidance"


class QuotaSeverity(str, Enum):
    on_track   = "on_track"
    developing = "developing"
    at_risk    = "at_risk"
    critical   = "critical"


class QuotaAction(str, Enum):
    no_action              = "no_action"
    quota_coaching         = "quota_coaching"
    performance_plan       = "performance_plan"
    sandbagging_review     = "sandbagging_review"
    deal_acceleration      = "deal_acceleration"
    quota_adjustment       = "quota_adjustment"


@dataclass
class QuotaAttainmentInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    quota_amount_usd: float
    revenue_closed_usd: float
    attainment_pct: float
    prior_period_attainment_pct: float
    quarters_below_quota_last_4: int
    quarters_above_quota_last_4: int
    deals_closed_last_week_of_period: int
    total_deals_closed: int
    deals_pushed_to_next_period: int
    avg_deal_size_usd: float
    pipeline_coverage_ratio: float
    forecast_commit_accuracy_pct: float
    discount_rate_avg_pct: float
    avg_sales_cycle_days: float
    multi_year_deals_closed: int
    expansion_revenue_usd: float
    new_logo_revenue_usd: float
    days_to_reach_50pct_quota: int
    deals_lost_after_commit_count: int


@dataclass
class QuotaAttainmentResult:
    rep_id: str
    region: str
    quota_risk: QuotaRisk
    quota_pattern: QuotaPattern
    quota_severity: QuotaSeverity
    recommended_action: QuotaAction
    attainment_consistency_score: float
    deal_quality_score: float
    pipeline_health_score: float
    forecast_reliability_score: float
    quota_effectiveness_composite: float
    is_below_quota_threshold: bool
    requires_performance_intervention: bool
    estimated_quota_gap_usd: float
    quota_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "quota_risk":                       self.quota_risk.value,
            "quota_pattern":                    self.quota_pattern.value,
            "quota_severity":                   self.quota_severity.value,
            "recommended_action":               self.recommended_action.value,
            "attainment_consistency_score":     self.attainment_consistency_score,
            "deal_quality_score":               self.deal_quality_score,
            "pipeline_health_score":            self.pipeline_health_score,
            "forecast_reliability_score":       self.forecast_reliability_score,
            "quota_effectiveness_composite":    self.quota_effectiveness_composite,
            "is_below_quota_threshold":         self.is_below_quota_threshold,
            "requires_performance_intervention": self.requires_performance_intervention,
            "estimated_quota_gap_usd":          self.estimated_quota_gap_usd,
            "quota_signal":                     self.quota_signal,
        }


class SalesQuotaAttainmentIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[QuotaAttainmentResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _attainment_consistency_score(self, inp: QuotaAttainmentInput) -> float:
        score = 0.0

        if inp.attainment_pct < 0.50:
            score += 45.0
        elif inp.attainment_pct < 0.75:
            score += 25.0
        elif inp.attainment_pct < 0.90:
            score += 10.0

        if inp.quarters_below_quota_last_4 >= 3:
            score += 30.0
        elif inp.quarters_below_quota_last_4 >= 2:
            score += 15.0
        elif inp.quarters_below_quota_last_4 >= 1:
            score += 5.0

        total = max(inp.total_deals_closed, 1)
        last_week_rate = inp.deals_closed_last_week_of_period / total
        if last_week_rate >= 0.50:
            score += 15.0
        elif last_week_rate >= 0.35:
            score += 7.0

        return min(score, 100.0)

    def _deal_quality_score(self, inp: QuotaAttainmentInput) -> float:
        score = 0.0

        if inp.avg_deal_size_usd < 5_000:
            score += 30.0
        elif inp.avg_deal_size_usd < 15_000:
            score += 15.0

        if inp.discount_rate_avg_pct >= 0.25:
            score += 30.0
        elif inp.discount_rate_avg_pct >= 0.15:
            score += 15.0

        if inp.deals_pushed_to_next_period >= 5:
            score += 30.0
        elif inp.deals_pushed_to_next_period >= 3:
            score += 15.0
        elif inp.deals_pushed_to_next_period >= 1:
            score += 5.0

        return min(score, 100.0)

    def _pipeline_health_score(self, inp: QuotaAttainmentInput) -> float:
        score = 0.0

        if inp.pipeline_coverage_ratio < 2.0:
            score += 45.0
        elif inp.pipeline_coverage_ratio < 3.0:
            score += 25.0
        elif inp.pipeline_coverage_ratio < 4.0:
            score += 10.0

        if inp.days_to_reach_50pct_quota >= 80:
            score += 30.0
        elif inp.days_to_reach_50pct_quota >= 60:
            score += 15.0

        total = max(inp.total_deals_closed, 1)
        lost_rate = inp.deals_lost_after_commit_count / total
        if lost_rate >= 0.20:
            score += 20.0
        elif lost_rate >= 0.10:
            score += 10.0

        return min(score, 100.0)

    def _forecast_reliability_score(self, inp: QuotaAttainmentInput) -> float:
        score = 0.0

        if inp.forecast_commit_accuracy_pct < 0.60:
            score += 45.0
        elif inp.forecast_commit_accuracy_pct < 0.75:
            score += 25.0
        elif inp.forecast_commit_accuracy_pct < 0.85:
            score += 10.0

        total = max(inp.total_deals_closed, 1)
        late_surge_rate = inp.deals_closed_last_week_of_period / total
        if late_surge_rate >= 0.40:
            score += 30.0
        elif late_surge_rate >= 0.25:
            score += 15.0

        if inp.deals_pushed_to_next_period >= 3:
            score += 20.0
        elif inp.deals_pushed_to_next_period >= 1:
            score += 10.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: QuotaAttainmentInput,
                         consistency: float, deal_quality: float,
                         pipeline: float, forecast: float) -> QuotaPattern:
        if consistency >= 35 and inp.quarters_below_quota_last_4 >= 3:
            return QuotaPattern.consistent_underperformance

        total = max(inp.total_deals_closed, 1)
        last_week_rate = inp.deals_closed_last_week_of_period / total
        if last_week_rate >= 0.40 and inp.attainment_pct >= 0.90 and deal_quality >= 20:
            return QuotaPattern.sandbagging

        if consistency >= 25 and last_week_rate >= 0.35:
            return QuotaPattern.late_quarter_surge

        if pipeline >= 25 and inp.days_to_reach_50pct_quota >= 70:
            return QuotaPattern.early_drop_off

        if deal_quality >= 30 and inp.deals_pushed_to_next_period >= 3:
            return QuotaPattern.quota_avoidance

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
            return QuotaSeverity.critical
        if composite >= 40:
            return QuotaSeverity.at_risk
        if composite >= 20:
            return QuotaSeverity.developing
        return QuotaSeverity.on_track

    def _action(self, risk: QuotaRisk, pattern: QuotaPattern) -> QuotaAction:
        if risk == QuotaRisk.critical:
            if pattern == QuotaPattern.consistent_underperformance:
                return QuotaAction.performance_plan
            if pattern == QuotaPattern.sandbagging:
                return QuotaAction.sandbagging_review
            return QuotaAction.deal_acceleration
        if risk == QuotaRisk.high:
            if pattern == QuotaPattern.early_drop_off:
                return QuotaAction.deal_acceleration
            if pattern == QuotaPattern.quota_avoidance:
                return QuotaAction.sandbagging_review
            return QuotaAction.quota_coaching
        if risk == QuotaRisk.moderate:
            return QuotaAction.quota_coaching
        return QuotaAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _is_below_quota_threshold(self, composite: float,
                                   inp: QuotaAttainmentInput) -> bool:
        return inp.attainment_pct < 0.75 or composite >= 40

    def _requires_performance_intervention(self, composite: float,
                                            inp: QuotaAttainmentInput) -> bool:
        return (
            composite >= 30
            or inp.attainment_pct < 0.60
            or inp.quarters_below_quota_last_4 >= 2
        )

    # ------------------------------------------------------------------
    # Quota gap
    # ------------------------------------------------------------------

    def _estimated_quota_gap(self, inp: QuotaAttainmentInput,
                              composite: float) -> float:
        raw_gap = inp.quota_amount_usd - inp.revenue_closed_usd
        return round(max(raw_gap, 0.0) * (composite / 100.0), 2)

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: QuotaAttainmentInput,
                 pattern: QuotaPattern, composite: float) -> str:
        if pattern == QuotaPattern.none and composite < 20:
            return "Quota attainment consistent and on track"
        parts: list[str] = []
        if inp.attainment_pct < 1.0:
            parts.append(f"{inp.attainment_pct*100:.0f}% quota attainment")
        if inp.quarters_below_quota_last_4 >= 1:
            parts.append(f"{inp.quarters_below_quota_last_4}/4 quarters below quota")
        if inp.deals_pushed_to_next_period >= 1:
            parts.append(f"{inp.deals_pushed_to_next_period} deals pushed out")
        label = pattern.value.replace("_", " ") if pattern != QuotaPattern.none else "Quota risk"
        summary = " — ".join(parts) if parts else "quota performance declining"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: QuotaAttainmentInput) -> QuotaAttainmentResult:
        consistency  = round(self._attainment_consistency_score(inp), 1)
        deal_quality = round(self._deal_quality_score(inp), 1)
        pipeline     = round(self._pipeline_health_score(inp), 1)
        forecast     = round(self._forecast_reliability_score(inp), 1)

        composite = round(
            consistency * 0.35 + deal_quality * 0.20 + pipeline * 0.25 + forecast * 0.20, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, consistency, deal_quality, pipeline, forecast)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        below       = self._is_below_quota_threshold(composite, inp)
        intervention = self._requires_performance_intervention(composite, inp)
        gap         = self._estimated_quota_gap(inp, composite)
        signal      = self._signal(inp, pattern, composite)

        result = QuotaAttainmentResult(
            rep_id=inp.rep_id,
            region=inp.region,
            quota_risk=risk,
            quota_pattern=pattern,
            quota_severity=severity,
            recommended_action=action,
            attainment_consistency_score=consistency,
            deal_quality_score=deal_quality,
            pipeline_health_score=pipeline,
            forecast_reliability_score=forecast,
            quota_effectiveness_composite=composite,
            is_below_quota_threshold=below,
            requires_performance_intervention=intervention,
            estimated_quota_gap_usd=gap,
            quota_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[QuotaAttainmentInput]) -> list[QuotaAttainmentResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_quota_effectiveness_composite": 0.0,
                "below_quota_threshold_count": 0,
                "performance_intervention_count": 0,
                "avg_attainment_consistency_score": 0.0,
                "avg_deal_quality_score": 0.0,
                "avg_pipeline_health_score": 0.0,
                "avg_forecast_reliability_score": 0.0,
                "total_estimated_quota_gap_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_con = total_dq = total_pipe = total_fc = total_gap = 0.0

        for r in self._results:
            risk_counts[r.quota_risk.value]       = risk_counts.get(r.quota_risk.value, 0) + 1
            pattern_counts[r.quota_pattern.value] = pattern_counts.get(r.quota_pattern.value, 0) + 1
            severity_counts[r.quota_severity.value] = severity_counts.get(r.quota_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.quota_effectiveness_composite
            total_con  += r.attainment_consistency_score
            total_dq   += r.deal_quality_score
            total_pipe += r.pipeline_health_score
            total_fc   += r.forecast_reliability_score
            total_gap  += r.estimated_quota_gap_usd

        n = len(self._results)

        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_quota_effectiveness_composite":    round(total_comp / n, 1),
            "below_quota_threshold_count":          sum(1 for r in self._results if r.is_below_quota_threshold),
            "performance_intervention_count":       sum(1 for r in self._results if r.requires_performance_intervention),
            "avg_attainment_consistency_score":     round(total_con / n, 1),
            "avg_deal_quality_score":               round(total_dq / n, 1),
            "avg_pipeline_health_score":            round(total_pipe / n, 1),
            "avg_forecast_reliability_score":       round(total_fc / n, 1),
            "total_estimated_quota_gap_usd":        round(total_gap, 2),
        }
