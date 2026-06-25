from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ConfidenceLevel(str, Enum):
    LOW         = "low"
    MODERATE    = "moderate"
    HIGH        = "high"
    COMMITTED   = "committed"


class ForecastPattern(str, Enum):
    RELIABLE        = "reliable"
    OPTIMISTIC_BIAS = "optimistic_bias"
    SANDBAGGING     = "sandbagging"
    VOLATILE        = "volatile"
    INSUFFICIENT    = "insufficient"


class PipelineHealth(str, Enum):
    UNDERPIPELINED  = "underpipelined"
    ADEQUATE        = "adequate"
    HEALTHY         = "healthy"
    OVERPIPELINED   = "overpipelined"


class ForecastAction(str, Enum):
    ACCEPT              = "accept"
    REVIEW_WITH_REP     = "review_with_rep"
    SCRUB_REQUIRED      = "scrub_required"
    ESCALATE_TO_MANAGER = "escalate_to_manager"


@dataclass
class ForecastConfidenceInput:
    rep_id:                         str
    rep_name:                       str
    manager_id:                     str
    forecast_amount:                float   # rep's committed forecast ($)
    quota_amount:                   float   # current period quota ($)
    pipeline_total:                 float   # total open pipeline ($)
    pipeline_in_commit_stage:       float   # pipeline in commit/close stage ($)
    pipeline_in_best_case:          float   # pipeline in best-case stage ($)
    deals_in_commit:                int     # # deals in commit stage
    deals_closed_this_period:       int     # deals already closed
    revenue_closed_this_period:     float   # revenue already closed ($)
    avg_deal_size_historical:       float   # rep's historical avg deal size ($)
    win_rate_historical_pct:        float   # rep's historical win rate (0-100)
    forecast_accuracy_last_3q:      float   # avg forecast accuracy last 3 quarters (0-100)
    close_date_slip_rate_pct:       float   # % of deals that slip close date (0-100)
    days_remaining_in_period:       int     # days left in quarter/month
    activities_last_14d:            int     # total activities (calls, emails, meetings) last 14 days
    avg_activities_per_commit_deal: float   # avg activities per commit deal (0-100 scale)
    exec_sponsored_deal_count:      int     # # of commit deals with exec sponsor
    multi_stakeholder_deal_count:   int     # # of commit deals with 3+ stakeholders
    new_deals_added_last_30d:       int     # new deals added in last 30 days
    cfo_approval_required_count:    int     # # of deals needing CFO sign-off


@dataclass
class ForecastConfidenceResult:
    rep_id:                 str
    rep_name:               str
    confidence_level:       ConfidenceLevel
    forecast_pattern:       ForecastPattern
    pipeline_health:        PipelineHealth
    forecast_action:        ForecastAction
    historical_accuracy_score:  float   # 0-100
    pipeline_coverage_score:    float   # 0-100
    deal_quality_score:         float   # 0-100
    activity_signal_score:      float   # 0-100
    forecast_composite:         float   # 0-100
    attainment_probability:     float   # 0-100, probability of hitting quota
    pipeline_coverage_ratio:    float   # pipeline / forecast ratio
    is_forecast_reliable:       bool
    needs_forecast_scrub:       bool

    def to_dict(self) -> dict:
        return {
            "rep_id":                       self.rep_id,
            "rep_name":                     self.rep_name,
            "confidence_level":             self.confidence_level.value,
            "forecast_pattern":             self.forecast_pattern.value,
            "pipeline_health":              self.pipeline_health.value,
            "forecast_action":              self.forecast_action.value,
            "historical_accuracy_score":    self.historical_accuracy_score,
            "pipeline_coverage_score":      self.pipeline_coverage_score,
            "deal_quality_score":           self.deal_quality_score,
            "activity_signal_score":        self.activity_signal_score,
            "forecast_composite":           self.forecast_composite,
            "attainment_probability":       self.attainment_probability,
            "pipeline_coverage_ratio":      self.pipeline_coverage_ratio,
            "is_forecast_reliable":         self.is_forecast_reliable,
            "needs_forecast_scrub":         self.needs_forecast_scrub,
        }


class ForecastConfidenceScorer:
    def __init__(self) -> None:
        self._results: list[ForecastConfidenceResult] = []

    # ── public API ──────────────────────────────────────────────────────────────

    def score(self, inp: ForecastConfidenceInput) -> ForecastConfidenceResult:
        hist    = self._historical_accuracy_score(inp)
        pipe    = self._pipeline_coverage_score(inp)
        quality = self._deal_quality_score(inp)
        activity = self._activity_signal_score(inp)
        composite = self._composite(hist, pipe, quality, activity)
        coverage_ratio = (inp.pipeline_total / inp.forecast_amount) if inp.forecast_amount > 0 else 0.0
        confidence  = self._confidence_level(composite, inp)
        pattern     = self._forecast_pattern(inp)
        ph          = self._pipeline_health(coverage_ratio, inp)
        attain_prob = self._attainment_probability(inp, composite)
        is_reliable = composite >= 60 and inp.forecast_accuracy_last_3q >= 70
        needs_scrub = composite < 45 or inp.close_date_slip_rate_pct >= 40
        action      = self._forecast_action(confidence, needs_scrub, inp)

        result = ForecastConfidenceResult(
            rep_id=inp.rep_id,
            rep_name=inp.rep_name,
            confidence_level=confidence,
            forecast_pattern=pattern,
            pipeline_health=ph,
            forecast_action=action,
            historical_accuracy_score=hist,
            pipeline_coverage_score=pipe,
            deal_quality_score=quality,
            activity_signal_score=activity,
            forecast_composite=composite,
            attainment_probability=attain_prob,
            pipeline_coverage_ratio=round(coverage_ratio, 2),
            is_forecast_reliable=is_reliable,
            needs_forecast_scrub=needs_scrub,
        )
        self._results.append(result)
        return result

    def score_batch(self, inputs: list[ForecastConfidenceInput]) -> list[ForecastConfidenceResult]:
        return [self.score(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ──────────────────────────────────────────────────────────────

    @property
    def reliable_forecasts(self) -> list[ForecastConfidenceResult]:
        return [r for r in self._results if r.is_forecast_reliable]

    @property
    def scrub_queue(self) -> list[ForecastConfidenceResult]:
        return [r for r in self._results if r.needs_forecast_scrub]

    @property
    def avg_forecast_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.forecast_composite for r in self._results) / len(self._results), 1)

    @property
    def avg_attainment_probability(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.attainment_probability for r in self._results) / len(self._results), 1)

    # ── scoring helpers ─────────────────────────────────────────────────────────

    def _historical_accuracy_score(self, inp: ForecastConfidenceInput) -> float:
        score = 0.0
        # Historical accuracy (0-100 → weight 50 pts)
        acc = inp.forecast_accuracy_last_3q
        if acc >= 90:
            score += 50.0
        elif acc >= 80:
            score += 40.0
        elif acc >= 70:
            score += 28.0
        elif acc >= 55:
            score += 15.0
        # Win rate (weight 30 pts)
        wr = inp.win_rate_historical_pct
        if wr >= 35:
            score += 30.0
        elif wr >= 25:
            score += 20.0
        elif wr >= 15:
            score += 10.0
        # Slip rate penalty (weight -20 pts)
        slip = inp.close_date_slip_rate_pct
        if slip >= 50:
            score -= 20.0
        elif slip >= 35:
            score -= 12.0
        elif slip >= 20:
            score -= 6.0
        return round(max(0.0, min(100.0, score)), 1)

    def _pipeline_coverage_score(self, inp: ForecastConfidenceInput) -> float:
        score = 0.0
        if inp.forecast_amount <= 0:
            return 0.0
        # Coverage ratio (pipeline / forecast)
        ratio = inp.pipeline_total / inp.forecast_amount
        if ratio >= 4.0:
            score += 40.0
        elif ratio >= 3.0:
            score += 32.0
        elif ratio >= 2.0:
            score += 22.0
        elif ratio >= 1.5:
            score += 12.0
        # Commit stage coverage (commit pipeline vs forecast)
        commit_ratio = inp.pipeline_in_commit_stage / inp.forecast_amount
        if commit_ratio >= 1.2:
            score += 35.0
        elif commit_ratio >= 1.0:
            score += 28.0
        elif commit_ratio >= 0.8:
            score += 18.0
        elif commit_ratio >= 0.5:
            score += 8.0
        # Already closed contribution
        closed_ratio = inp.revenue_closed_this_period / inp.forecast_amount
        if closed_ratio >= 0.5:
            score += 25.0
        elif closed_ratio >= 0.3:
            score += 15.0
        elif closed_ratio >= 0.1:
            score += 8.0
        return round(max(0.0, min(100.0, score)), 1)

    def _deal_quality_score(self, inp: ForecastConfidenceInput) -> float:
        score = 0.0
        # Exec sponsor = higher quality (weight 30 pts)
        if inp.deals_in_commit > 0:
            exec_ratio = inp.exec_sponsored_deal_count / inp.deals_in_commit
            if exec_ratio >= 0.5:
                score += 30.0
            elif exec_ratio >= 0.25:
                score += 18.0
        # Multi-stakeholder (weight 25 pts)
        if inp.deals_in_commit > 0:
            ms_ratio = inp.multi_stakeholder_deal_count / inp.deals_in_commit
            if ms_ratio >= 0.5:
                score += 25.0
            elif ms_ratio >= 0.25:
                score += 15.0
        # Deal size vs historical avg (abnormally large = risk)
        if inp.deals_in_commit > 0 and inp.avg_deal_size_historical > 0:
            commit_avg = inp.pipeline_in_commit_stage / inp.deals_in_commit
            size_ratio = commit_avg / inp.avg_deal_size_historical
            if 0.7 <= size_ratio <= 2.0:
                score += 20.0
            elif size_ratio > 2.0:
                score += 8.0  # big deals = high risk
        # Days remaining risk
        if inp.days_remaining_in_period >= 20:
            score += 15.0
        elif inp.days_remaining_in_period >= 10:
            score += 8.0
        # CFO sign-off risk penalty
        if inp.cfo_approval_required_count >= 3:
            score -= 15.0
        elif inp.cfo_approval_required_count >= 1:
            score -= 8.0
        return round(max(0.0, min(100.0, score)), 1)

    def _activity_signal_score(self, inp: ForecastConfidenceInput) -> float:
        score = 0.0
        # Raw activities last 14d
        if inp.activities_last_14d >= 20:
            score += 35.0
        elif inp.activities_last_14d >= 12:
            score += 25.0
        elif inp.activities_last_14d >= 6:
            score += 14.0
        elif inp.activities_last_14d >= 2:
            score += 6.0
        # Avg activities per commit deal (quality of coverage)
        avg_act = inp.avg_activities_per_commit_deal
        if avg_act >= 80:
            score += 40.0
        elif avg_act >= 60:
            score += 28.0
        elif avg_act >= 40:
            score += 16.0
        elif avg_act >= 20:
            score += 8.0
        # New deals added = pipeline build
        if inp.new_deals_added_last_30d >= 4:
            score += 15.0
        elif inp.new_deals_added_last_30d >= 2:
            score += 8.0
        elif inp.new_deals_added_last_30d >= 1:
            score += 4.0
        # Deals closed this period already
        if inp.deals_closed_this_period >= 3:
            score += 10.0
        elif inp.deals_closed_this_period >= 1:
            score += 5.0
        return round(max(0.0, min(100.0, score)), 1)

    def _composite(
        self,
        hist: float,
        pipe: float,
        quality: float,
        activity: float,
    ) -> float:
        composite = hist * 0.30 + pipe * 0.35 + quality * 0.20 + activity * 0.15
        return round(max(0.0, min(100.0, composite)), 1)

    def _confidence_level(self, composite: float, inp: ForecastConfidenceInput) -> ConfidenceLevel:
        if composite >= 75 and inp.forecast_accuracy_last_3q >= 80:
            return ConfidenceLevel.COMMITTED
        if composite >= 60:
            return ConfidenceLevel.HIGH
        if composite >= 40:
            return ConfidenceLevel.MODERATE
        return ConfidenceLevel.LOW

    def _forecast_pattern(self, inp: ForecastConfidenceInput) -> ForecastPattern:
        if inp.forecast_accuracy_last_3q < 40:
            return ForecastPattern.INSUFFICIENT
        acc = inp.forecast_accuracy_last_3q
        # Optimistic if commits too much vs actual close rate
        commit_ratio = (
            inp.pipeline_in_commit_stage / inp.forecast_amount
            if inp.forecast_amount > 0 else 0
        )
        if acc < 70 and commit_ratio < 0.8:
            return ForecastPattern.OPTIMISTIC_BIAS
        # Sandbagging: high accuracy + very conservative forecast vs pipeline
        if acc >= 80 and (inp.pipeline_total / inp.forecast_amount if inp.forecast_amount > 0 else 0) > 5.0:
            return ForecastPattern.SANDBAGGING
        # Volatile: slip rate high + accuracy varies
        if inp.close_date_slip_rate_pct >= 40:
            return ForecastPattern.VOLATILE
        return ForecastPattern.RELIABLE

    def _pipeline_health(self, coverage_ratio: float, inp: ForecastConfidenceInput) -> PipelineHealth:
        if coverage_ratio >= 5.0:
            return PipelineHealth.OVERPIPELINED
        if coverage_ratio >= 3.0:
            return PipelineHealth.HEALTHY
        if coverage_ratio >= 2.0:
            return PipelineHealth.ADEQUATE
        return PipelineHealth.UNDERPIPELINED

    def _attainment_probability(self, inp: ForecastConfidenceInput, composite: float) -> float:
        base = composite * 0.5
        # Closed revenue already contributes directly
        if inp.quota_amount > 0:
            closed_pct = (inp.revenue_closed_this_period / inp.quota_amount) * 100
            base = min(100.0, base + closed_pct * 0.4)
        # Historical accuracy bonus
        if inp.forecast_accuracy_last_3q >= 85:
            base = min(100.0, base + 15.0)
        elif inp.forecast_accuracy_last_3q >= 70:
            base = min(100.0, base + 8.0)
        # Days remaining penalty
        if inp.days_remaining_in_period <= 5:
            base -= 10.0
        return round(max(0.0, min(100.0, base)), 1)

    def _forecast_action(
        self,
        confidence: ConfidenceLevel,
        needs_scrub: bool,
        inp: ForecastConfidenceInput,
    ) -> ForecastAction:
        if confidence == ConfidenceLevel.LOW or inp.forecast_accuracy_last_3q < 50:
            return ForecastAction.ESCALATE_TO_MANAGER
        if needs_scrub:
            return ForecastAction.SCRUB_REQUIRED
        if confidence == ConfidenceLevel.MODERATE:
            return ForecastAction.REVIEW_WITH_REP
        return ForecastAction.ACCEPT

    # ── summary ─────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                        0,
                "confidence_counts":            {},
                "pattern_counts":               {},
                "pipeline_health_counts":       {},
                "action_counts":                {},
                "avg_forecast_composite":       0.0,
                "avg_attainment_probability":   0.0,
                "reliable_count":               0,
                "scrub_count":                  0,
                "avg_historical_accuracy_score":    0.0,
                "avg_pipeline_coverage_score":      0.0,
                "avg_deal_quality_score":           0.0,
                "avg_activity_signal_score":        0.0,
            }

        confidence_counts:      dict[str, int] = {}
        pattern_counts:         dict[str, int] = {}
        pipeline_health_counts: dict[str, int] = {}
        action_counts:          dict[str, int] = {}
        total_comp  = 0.0; total_attain = 0.0; total_hist = 0.0
        total_pipe  = 0.0; total_qual   = 0.0; total_act  = 0.0

        for r in self._results:
            confidence_counts[r.confidence_level.value]       = confidence_counts.get(r.confidence_level.value, 0) + 1
            pattern_counts[r.forecast_pattern.value]          = pattern_counts.get(r.forecast_pattern.value, 0) + 1
            pipeline_health_counts[r.pipeline_health.value]   = pipeline_health_counts.get(r.pipeline_health.value, 0) + 1
            action_counts[r.forecast_action.value]            = action_counts.get(r.forecast_action.value, 0) + 1
            total_comp   += r.forecast_composite
            total_attain += r.attainment_probability
            total_hist   += r.historical_accuracy_score
            total_pipe   += r.pipeline_coverage_score
            total_qual   += r.deal_quality_score
            total_act    += r.activity_signal_score

        return {
            "total":                            n,
            "confidence_counts":                confidence_counts,
            "pattern_counts":                   pattern_counts,
            "pipeline_health_counts":           pipeline_health_counts,
            "action_counts":                    action_counts,
            "avg_forecast_composite":           round(total_comp / n, 1),
            "avg_attainment_probability":       round(total_attain / n, 1),
            "reliable_count":                   len(self.reliable_forecasts),
            "scrub_count":                      len(self.scrub_queue),
            "avg_historical_accuracy_score":    round(total_hist / n, 1),
            "avg_pipeline_coverage_score":      round(total_pipe / n, 1),
            "avg_deal_quality_score":           round(total_qual / n, 1),
            "avg_activity_signal_score":        round(total_act / n, 1),
        }
