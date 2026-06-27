from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ForecastBand(str, Enum):
    BEST_CASE = "best_case"
    UPSIDE    = "upside"
    COMMIT    = "commit"
    LIKELY    = "likely"      # below commit


class ForecastAccuracy(str, Enum):
    EXCELLENT = "excellent"
    GOOD      = "good"
    FAIR      = "fair"
    POOR      = "poor"


class CallReliability(str, Enum):
    HIGH       = "high"
    MEDIUM     = "medium"
    LOW        = "low"
    UNRELIABLE = "unreliable"


class ForecastAction(str, Enum):
    COMMIT_AS_IS = "commit_as_is"
    ADJUST_UP    = "adjust_up"
    ADJUST_DOWN  = "adjust_down"
    INVESTIGATE  = "investigate"
    ESCALATE     = "escalate"


@dataclass
class SalesForecastInput:
    rep_id:                  str
    rep_name:                str
    manager_id:              str
    region:                  str
    quota:                   float
    submitted_commit:        float            # rep's committed forecast
    submitted_best_case:     float            # rep's best-case forecast
    pipeline_value:          float            # total pipeline
    closed_won_qtd:          float            # booked revenue this period
    late_stage_pipeline:     float            # stage 3+ deals
    early_stage_pipeline:    float            # stage 1-2 deals
    days_remaining:          int              # days left in period
    period_days:             int              # total period length
    historical_accuracy_pct: float            # % of time commit was met, last 4Q avg
    historical_beat_pct:     float            # avg % they beat commit by (sandbagging signal)
    last_period_attainment:  float            # previous period attainment %
    slipped_deals_count:     int              # deals that moved out this period
    new_pipeline_added_qtd:  float            # new pipeline created this period
    calls_made:              int              # forecast calls to manager this period
    calls_hit:               int              # past calls that proved accurate
    nrr_contribution:        float            # renewal + expansion revenue in period


@dataclass
class SalesForecastResult:
    rep_id:               str
    rep_name:             str
    manager_id:           str
    forecast_band:        ForecastBand
    forecast_accuracy:    ForecastAccuracy
    call_reliability:     CallReliability
    forecast_action:      ForecastAction
    adjusted_forecast:    float    # engine-adjusted revenue estimate
    coverage_ratio:       float    # pipeline / quota
    sandbagging_score:    float    # 0–100 (high = likely sandbagging)
    pipeline_health:      float    # 0–100
    commit_vs_quota_pct:  float    # submitted_commit / quota × 100
    upside_potential:     float    # best_case − commit
    is_at_risk:           bool
    is_sandbagging:       bool

    def to_dict(self) -> dict:
        return {
            "rep_id":              self.rep_id,
            "rep_name":            self.rep_name,
            "manager_id":          self.manager_id,
            "forecast_band":       self.forecast_band.value,
            "forecast_accuracy":   self.forecast_accuracy.value,
            "call_reliability":    self.call_reliability.value,
            "forecast_action":     self.forecast_action.value,
            "adjusted_forecast":   self.adjusted_forecast,
            "coverage_ratio":      self.coverage_ratio,
            "sandbagging_score":   self.sandbagging_score,
            "pipeline_health":     self.pipeline_health,
            "commit_vs_quota_pct": self.commit_vs_quota_pct,
            "upside_potential":    self.upside_potential,
            "is_at_risk":          self.is_at_risk,
            "is_sandbagging":      self.is_sandbagging,
        }


class SalesForecastEngine:
    def __init__(self) -> None:
        self._results: list[SalesForecastResult] = []

    # ── public API ─────────────────────────────────────────────────────────────

    def analyze(self, inp: SalesForecastInput) -> SalesForecastResult:
        coverage    = self._coverage_ratio(inp)
        sand_score  = self._sandbagging_score(inp)
        pip_health  = self._pipeline_health(inp, coverage)
        adj_fcst    = self._adjusted_forecast(inp)
        commit_pct  = self._commit_vs_quota_pct(inp)
        upside      = self._upside_potential(inp)
        accuracy    = self._forecast_accuracy(inp)
        reliability = self._call_reliability(inp)
        band        = self._forecast_band(inp, adj_fcst)
        at_risk     = coverage < 1.5 or inp.last_period_attainment < 70
        sandbagging = sand_score >= 50 and inp.historical_beat_pct >= 20
        action      = self._forecast_action(inp, band, accuracy, at_risk, sandbagging, coverage)

        result = SalesForecastResult(
            rep_id=inp.rep_id,
            rep_name=inp.rep_name,
            manager_id=inp.manager_id,
            forecast_band=band,
            forecast_accuracy=accuracy,
            call_reliability=reliability,
            forecast_action=action,
            adjusted_forecast=adj_fcst,
            coverage_ratio=coverage,
            sandbagging_score=sand_score,
            pipeline_health=pip_health,
            commit_vs_quota_pct=commit_pct,
            upside_potential=upside,
            is_at_risk=at_risk,
            is_sandbagging=sandbagging,
        )
        self._results.append(result)
        return result

    def analyze_batch(
        self, inputs: list[SalesForecastInput]
    ) -> list[SalesForecastResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ─────────────────────────────────────────────────────────────

    @property
    def at_risk_reps(self) -> list[SalesForecastResult]:
        return [r for r in self._results if r.is_at_risk]

    @property
    def sandbagging_reps(self) -> list[SalesForecastResult]:
        return [r for r in self._results if r.is_sandbagging]

    @property
    def high_reliability_reps(self) -> list[SalesForecastResult]:
        return [r for r in self._results if r.call_reliability == CallReliability.HIGH]

    @property
    def total_adjusted_forecast(self) -> float:
        return round(sum(r.adjusted_forecast for r in self._results), 2)

    @property
    def total_upside_potential(self) -> float:
        return round(sum(r.upside_potential for r in self._results), 2)

    # ── scoring helpers ────────────────────────────────────────────────────────

    def _coverage_ratio(self, inp: SalesForecastInput) -> float:
        if inp.quota <= 0:
            return 0.0
        return round(inp.pipeline_value / inp.quota, 2)

    def _sandbagging_score(self, inp: SalesForecastInput) -> float:
        # Estimated likely outcome from pipeline weighting
        weighted = (
            inp.closed_won_qtd
            + inp.late_stage_pipeline * 0.65
            + inp.early_stage_pipeline * 0.25
        )
        gap = max(0.0, weighted - inp.submitted_commit)
        gap_ratio = (gap / max(1.0, inp.submitted_commit)) * 100
        score = gap_ratio * 0.6 + inp.historical_beat_pct * 0.4
        return round(max(0.0, min(100.0, score)), 1)

    def _pipeline_health(self, inp: SalesForecastInput, coverage: float) -> float:
        score = 0.0
        # Coverage contribution (up to 40)
        score += min(40.0, coverage * 10.0)
        # Late-stage proportion (up to 30)
        if inp.submitted_commit > 0:
            late_cov = inp.late_stage_pipeline / inp.submitted_commit
            score += min(30.0, late_cov * 20.0)
        # Call accuracy (up to 25)
        if inp.calls_made > 0:
            call_acc = min(1.0, inp.calls_hit / inp.calls_made)
            score += call_acc * 25.0
        else:
            score += 12.5  # neutral when no calls made
        # Slippage penalty
        score -= inp.slipped_deals_count * 8.0
        return round(max(0.0, min(100.0, score)), 1)

    def _adjusted_forecast(self, inp: SalesForecastInput) -> float:
        # Base: probability-weighted pipeline + already closed
        base = (
            inp.closed_won_qtd
            + inp.late_stage_pipeline * 0.70
            + inp.early_stage_pipeline * 0.25
            + inp.nrr_contribution
        )
        # Scale by historical accuracy
        accuracy_factor = max(0.5, inp.historical_accuracy_pct / 100.0)
        estimate = base * accuracy_factor
        # Bound between 80% of commit and best case
        floor = inp.submitted_commit * 0.80
        ceiling = inp.submitted_best_case
        return round(max(floor, min(ceiling, estimate)), 2)

    def _commit_vs_quota_pct(self, inp: SalesForecastInput) -> float:
        if inp.quota <= 0:
            return 0.0
        return round((inp.submitted_commit / inp.quota) * 100, 1)

    def _upside_potential(self, inp: SalesForecastInput) -> float:
        return round(max(0.0, inp.submitted_best_case - inp.submitted_commit), 2)

    def _forecast_accuracy(self, inp: SalesForecastInput) -> ForecastAccuracy:
        pct = inp.historical_accuracy_pct
        if pct >= 85: return ForecastAccuracy.EXCELLENT
        if pct >= 70: return ForecastAccuracy.GOOD
        if pct >= 50: return ForecastAccuracy.FAIR
        return ForecastAccuracy.POOR

    def _call_reliability(self, inp: SalesForecastInput) -> CallReliability:
        if inp.calls_made <= 0:
            return CallReliability.UNRELIABLE
        call_acc = (inp.calls_hit / inp.calls_made) * 100
        # Blend with historical accuracy
        blended = call_acc * 0.60 + inp.historical_accuracy_pct * 0.40
        if blended >= 80: return CallReliability.HIGH
        if blended >= 60: return CallReliability.MEDIUM
        if blended >= 40: return CallReliability.LOW
        return CallReliability.UNRELIABLE

    def _forecast_band(
        self, inp: SalesForecastInput, adjusted: float
    ) -> ForecastBand:
        if adjusted >= inp.submitted_best_case * 0.95:
            return ForecastBand.BEST_CASE
        if adjusted >= inp.submitted_commit * 1.10:
            return ForecastBand.UPSIDE
        if adjusted >= inp.submitted_commit * 0.90:
            return ForecastBand.COMMIT
        return ForecastBand.LIKELY

    def _forecast_action(
        self,
        inp: SalesForecastInput,
        band: ForecastBand,
        accuracy: ForecastAccuracy,
        at_risk: bool,
        sandbagging: bool,
        coverage: float,
    ) -> ForecastAction:
        if at_risk and coverage < 1.5:
            return ForecastAction.ESCALATE
        if at_risk:
            return ForecastAction.INVESTIGATE
        if sandbagging and band == ForecastBand.UPSIDE:
            return ForecastAction.ADJUST_UP
        if accuracy == ForecastAccuracy.POOR and band == ForecastBand.LIKELY:
            return ForecastAction.ADJUST_DOWN
        return ForecastAction.COMMIT_AS_IS

    # ── summary ────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                   0,
                "band_counts":             {},
                "accuracy_counts":         {},
                "reliability_counts":      {},
                "action_counts":           {},
                "avg_coverage_ratio":      0.0,
                "avg_pipeline_health":     0.0,
                "total_adjusted_forecast": 0.0,
                "at_risk_count":           0,
                "sandbagging_count":       0,
                "high_reliability_count":  0,
                "total_upside_potential":  0.0,
                "avg_sandbagging_score":   0.0,
            }

        band_counts:        dict[str, int] = {}
        accuracy_counts:    dict[str, int] = {}
        reliability_counts: dict[str, int] = {}
        action_counts:      dict[str, int] = {}
        total_coverage  = 0.0
        total_health    = 0.0
        total_sandbagging = 0.0

        for r in self._results:
            band_counts[r.forecast_band.value]         = band_counts.get(r.forecast_band.value, 0) + 1
            accuracy_counts[r.forecast_accuracy.value] = accuracy_counts.get(r.forecast_accuracy.value, 0) + 1
            reliability_counts[r.call_reliability.value] = reliability_counts.get(r.call_reliability.value, 0) + 1
            action_counts[r.forecast_action.value]     = action_counts.get(r.forecast_action.value, 0) + 1
            total_coverage    += r.coverage_ratio
            total_health      += r.pipeline_health
            total_sandbagging += r.sandbagging_score

        return {
            "total":                   n,
            "band_counts":             band_counts,
            "accuracy_counts":         accuracy_counts,
            "reliability_counts":      reliability_counts,
            "action_counts":           action_counts,
            "avg_coverage_ratio":      round(total_coverage / n, 2),
            "avg_pipeline_health":     round(total_health / n, 1),
            "total_adjusted_forecast": self.total_adjusted_forecast,
            "at_risk_count":           len(self.at_risk_reps),
            "sandbagging_count":       len(self.sandbagging_reps),
            "high_reliability_count":  len(self.high_reliability_reps),
            "total_upside_potential":  self.total_upside_potential,
            "avg_sandbagging_score":   round(total_sandbagging / n, 1),
        }
