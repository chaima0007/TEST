from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AttainmentLikelihood(str, Enum):
    VERY_LIKELY    = "very_likely"
    LIKELY         = "likely"
    POSSIBLE       = "possible"
    UNLIKELY       = "unlikely"
    VERY_UNLIKELY  = "very_unlikely"


class AttainmentRisk(str, Enum):
    LOW      = "low"
    MEDIUM   = "medium"
    HIGH     = "high"
    CRITICAL = "critical"


class PerformanceTrend(str, Enum):
    ACCELERATING = "accelerating"
    ON_TRACK     = "on_track"
    SLOWING      = "slowing"
    DECLINING    = "declining"


class AttainmentAction(str, Enum):
    MAINTAIN          = "maintain"
    ACCELERATE        = "accelerate"
    PIPELINE_BUILD    = "pipeline_build"
    COACHING_REQUIRED = "coaching_required"
    URGENT_REVIEW     = "urgent_review"


@dataclass
class QuotaAttainmentInput:
    rep_id:                  str
    rep_name:                str
    manager_id:              str
    annual_quota:            float    # full-year quota
    quota_ytd:               float    # quota to date (pro-rated)
    closed_won_ytd:          float    # revenue closed so far
    commit_pipeline:         float    # rep-committed pipeline
    best_case_pipeline:      float    # best-case pipeline
    weighted_pipeline:       float    # probability-weighted open pipeline
    days_remaining:          int      # days left in period
    total_period_days:       int      # total days in period
    historical_attainment:   float    # avg attainment % over last 4 quarters (0–150+)
    last_quarter_attainment: float    # most recent quarter attainment %
    win_rate:                float    # 0–100
    avg_deal_size:           float
    avg_sales_cycle_days:    int
    active_deal_count:       int
    stalled_deal_count:      int
    new_deals_added_mtd:     int
    activities_per_day:      float    # call/email/meeting activity rate
    coaching_sessions_qtd:   int


@dataclass
class QuotaAttainmentResult:
    rep_id:                  str
    rep_name:                str
    attainment_likelihood:   AttainmentLikelihood
    attainment_risk:         AttainmentRisk
    performance_trend:       PerformanceTrend
    attainment_action:       AttainmentAction
    attainment_pct:          float    # closed_won_ytd / quota_ytd × 100
    projected_attainment:    float    # projected end-of-period %
    gap_to_quota:            float    # quota_ytd - closed_won_ytd (0 if ahead)
    coverage_ratio:          float    # (closed_won + weighted_pipeline) / quota_ytd
    confidence_score:        float    # 0–100 composite
    momentum_score:          float    # 0–100 activity + pipeline momentum
    pace_score:              float    # 0–100 based on time vs attainment
    is_at_risk:              bool
    needs_coaching:          bool

    def to_dict(self) -> dict:
        return {
            "rep_id":               self.rep_id,
            "rep_name":             self.rep_name,
            "attainment_likelihood": self.attainment_likelihood.value,
            "attainment_risk":      self.attainment_risk.value,
            "performance_trend":    self.performance_trend.value,
            "attainment_action":    self.attainment_action.value,
            "attainment_pct":       self.attainment_pct,
            "projected_attainment": self.projected_attainment,
            "gap_to_quota":         self.gap_to_quota,
            "coverage_ratio":       self.coverage_ratio,
            "confidence_score":     self.confidence_score,
            "momentum_score":       self.momentum_score,
            "pace_score":           self.pace_score,
            "is_at_risk":           self.is_at_risk,
            "needs_coaching":       self.needs_coaching,
        }


class QuotaAttainmentEngine:
    def __init__(self) -> None:
        self._results: list[QuotaAttainmentResult] = []

    # ── public API ─────────────────────────────────────────────────────────────

    def analyze(self, inp: QuotaAttainmentInput) -> QuotaAttainmentResult:
        attainment_pct    = self._attainment_pct(inp)
        projected         = self._projected_attainment(inp, attainment_pct)
        gap               = self._gap_to_quota(inp)
        coverage          = self._coverage_ratio(inp)
        confidence        = self._confidence_score(inp, projected, coverage)
        momentum          = self._momentum_score(inp)
        pace              = self._pace_score(inp, attainment_pct)
        trend             = self._performance_trend(inp, attainment_pct, pace)
        likelihood        = self._attainment_likelihood(projected, confidence)
        risk              = self._attainment_risk(inp, projected, gap)
        is_at_risk        = projected < 80.0 or risk in (AttainmentRisk.HIGH, AttainmentRisk.CRITICAL)
        needs_coaching    = (
            inp.last_quarter_attainment < 70.0
            or trend in (PerformanceTrend.DECLINING,)
            or (inp.stalled_deal_count > inp.active_deal_count * 0.5 and inp.active_deal_count > 0)
        )
        action = self._attainment_action(inp, likelihood, risk, trend, momentum)

        result = QuotaAttainmentResult(
            rep_id=inp.rep_id,
            rep_name=inp.rep_name,
            attainment_likelihood=likelihood,
            attainment_risk=risk,
            performance_trend=trend,
            attainment_action=action,
            attainment_pct=attainment_pct,
            projected_attainment=projected,
            gap_to_quota=gap,
            coverage_ratio=coverage,
            confidence_score=confidence,
            momentum_score=momentum,
            pace_score=pace,
            is_at_risk=is_at_risk,
            needs_coaching=needs_coaching,
        )
        self._results.append(result)
        return result

    def analyze_batch(
        self, inputs: list[QuotaAttainmentInput]
    ) -> list[QuotaAttainmentResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ─────────────────────────────────────────────────────────────

    @property
    def at_risk_reps(self) -> list[QuotaAttainmentResult]:
        return [r for r in self._results if r.is_at_risk]

    @property
    def coaching_reps(self) -> list[QuotaAttainmentResult]:
        return [r for r in self._results if r.needs_coaching]

    @property
    def likely_attainers(self) -> list[QuotaAttainmentResult]:
        return [r for r in self._results if r.attainment_likelihood in (
            AttainmentLikelihood.VERY_LIKELY, AttainmentLikelihood.LIKELY
        )]

    @property
    def total_gap_to_quota(self) -> float:
        return round(sum(r.gap_to_quota for r in self._results), 2)

    @property
    def avg_projected_attainment(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.projected_attainment for r in self._results) / len(self._results), 1)

    # ── scoring helpers ────────────────────────────────────────────────────────

    def _attainment_pct(self, inp: QuotaAttainmentInput) -> float:
        if inp.quota_ytd <= 0:
            return 0.0
        return round((inp.closed_won_ytd / inp.quota_ytd) * 100, 1)

    def _projected_attainment(
        self, inp: QuotaAttainmentInput, attainment_pct: float
    ) -> float:
        if inp.total_period_days <= 0:
            return attainment_pct
        days_elapsed = max(1, inp.total_period_days - inp.days_remaining)
        run_rate = inp.closed_won_ytd / days_elapsed
        projected_closed = inp.closed_won_ytd + run_rate * inp.days_remaining

        # Blend with pipeline contribution
        pipeline_contribution = inp.weighted_pipeline * (inp.win_rate / 100.0)
        blended_closed = projected_closed * 0.6 + (inp.closed_won_ytd + pipeline_contribution) * 0.4

        if inp.quota_ytd <= 0:
            return 0.0
        return round((blended_closed / inp.quota_ytd) * 100, 1)

    def _gap_to_quota(self, inp: QuotaAttainmentInput) -> float:
        gap = inp.quota_ytd - inp.closed_won_ytd
        return round(max(0.0, gap), 2)

    def _coverage_ratio(self, inp: QuotaAttainmentInput) -> float:
        if inp.quota_ytd <= 0:
            return 0.0
        total = inp.closed_won_ytd + inp.weighted_pipeline
        return round(total / inp.quota_ytd, 2)

    def _confidence_score(
        self, inp: QuotaAttainmentInput, projected: float, coverage: float
    ) -> float:
        score = 0.0
        # Historical attainment (up to 35)
        score += min(35.0, inp.historical_attainment * 0.25)
        # Projected attainment (up to 30)
        score += min(30.0, projected * 0.20)
        # Coverage ratio (up to 20)
        score += min(20.0, coverage * 10.0)
        # Win rate (up to 15)
        score += inp.win_rate * 0.15
        # Stalled deal penalty
        if inp.active_deal_count > 0:
            stall_rate = inp.stalled_deal_count / inp.active_deal_count
            score -= stall_rate * 15.0
        return round(max(0.0, min(100.0, score)), 1)

    def _momentum_score(self, inp: QuotaAttainmentInput) -> float:
        score = 0.0
        # Activity rate (up to 40)
        score += min(40.0, inp.activities_per_day * 8.0)
        # New deals added (up to 30)
        score += min(30.0, inp.new_deals_added_mtd * 5.0)
        # Active deal health (up to 30)
        if inp.active_deal_count > 0:
            healthy_rate = max(0, inp.active_deal_count - inp.stalled_deal_count) / inp.active_deal_count
            score += healthy_rate * 30.0
        return round(max(0.0, min(100.0, score)), 1)

    def _pace_score(self, inp: QuotaAttainmentInput, attainment_pct: float) -> float:
        if inp.total_period_days <= 0:
            return 50.0
        period_progress_pct = (
            (inp.total_period_days - inp.days_remaining) / inp.total_period_days
        ) * 100
        # Pace = how far ahead/behind expected attainment given time elapsed
        if period_progress_pct <= 0:
            return 50.0
        expected_attainment = period_progress_pct  # linear expectation
        delta = attainment_pct - expected_attainment
        # delta +20 → 100, delta -20 → 0
        score = 50.0 + delta * 2.5
        return round(max(0.0, min(100.0, score)), 1)

    def _performance_trend(
        self, inp: QuotaAttainmentInput, attainment_pct: float, pace: float
    ) -> PerformanceTrend:
        prev = inp.historical_attainment
        curr = inp.last_quarter_attainment
        if curr >= prev * 1.1 and pace >= 55:
            return PerformanceTrend.ACCELERATING
        if curr < prev * 0.85 or pace < 35:
            return PerformanceTrend.DECLINING
        if curr < prev * 0.95 or pace < 45:
            return PerformanceTrend.SLOWING
        return PerformanceTrend.ON_TRACK

    def _attainment_likelihood(
        self, projected: float, confidence: float
    ) -> AttainmentLikelihood:
        score = projected * 0.6 + confidence * 0.4
        if score >= 90:
            return AttainmentLikelihood.VERY_LIKELY
        if score >= 75:
            return AttainmentLikelihood.LIKELY
        if score >= 55:
            return AttainmentLikelihood.POSSIBLE
        if score >= 35:
            return AttainmentLikelihood.UNLIKELY
        return AttainmentLikelihood.VERY_UNLIKELY

    def _attainment_risk(
        self, inp: QuotaAttainmentInput, projected: float, gap: float
    ) -> AttainmentRisk:
        if inp.quota_ytd <= 0:
            return AttainmentRisk.LOW
        gap_pct = (gap / inp.quota_ytd) * 100 if inp.quota_ytd > 0 else 0
        if projected >= 90 and gap_pct < 20:
            return AttainmentRisk.LOW
        if projected >= 70 and gap_pct < 40:
            return AttainmentRisk.MEDIUM
        if projected >= 50:
            return AttainmentRisk.HIGH
        return AttainmentRisk.CRITICAL

    def _attainment_action(
        self,
        inp: QuotaAttainmentInput,
        likelihood: AttainmentLikelihood,
        risk: AttainmentRisk,
        trend: PerformanceTrend,
        momentum: float,
    ) -> AttainmentAction:
        if risk == AttainmentRisk.CRITICAL:
            return AttainmentAction.URGENT_REVIEW
        if trend == PerformanceTrend.DECLINING and risk == AttainmentRisk.HIGH:
            return AttainmentAction.COACHING_REQUIRED
        if likelihood in (AttainmentLikelihood.UNLIKELY, AttainmentLikelihood.VERY_UNLIKELY):
            return AttainmentAction.PIPELINE_BUILD
        if momentum < 40 or trend == PerformanceTrend.SLOWING:
            return AttainmentAction.ACCELERATE
        return AttainmentAction.MAINTAIN

    # ── summary ────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                     0,
                "likelihood_counts":         {},
                "risk_counts":               {},
                "trend_counts":              {},
                "action_counts":             {},
                "avg_attainment_pct":        0.0,
                "avg_projected_attainment":  0.0,
                "total_gap_to_quota":        0.0,
                "at_risk_count":             0,
                "coaching_count":            0,
                "avg_confidence_score":      0.0,
                "avg_momentum_score":        0.0,
                "likely_attainer_count":     0,
            }

        likelihood_counts: dict[str, int] = {}
        risk_counts:       dict[str, int] = {}
        trend_counts:      dict[str, int] = {}
        action_counts:     dict[str, int] = {}
        total_attainment   = 0.0
        total_projected    = 0.0
        total_confidence   = 0.0
        total_momentum     = 0.0

        for r in self._results:
            likelihood_counts[r.attainment_likelihood.value] = likelihood_counts.get(r.attainment_likelihood.value, 0) + 1
            risk_counts[r.attainment_risk.value]             = risk_counts.get(r.attainment_risk.value, 0) + 1
            trend_counts[r.performance_trend.value]          = trend_counts.get(r.performance_trend.value, 0) + 1
            action_counts[r.attainment_action.value]         = action_counts.get(r.attainment_action.value, 0) + 1
            total_attainment  += r.attainment_pct
            total_projected   += r.projected_attainment
            total_confidence  += r.confidence_score
            total_momentum    += r.momentum_score

        return {
            "total":                     n,
            "likelihood_counts":         likelihood_counts,
            "risk_counts":               risk_counts,
            "trend_counts":              trend_counts,
            "action_counts":             action_counts,
            "avg_attainment_pct":        round(total_attainment / n, 1),
            "avg_projected_attainment":  round(total_projected / n, 1),
            "total_gap_to_quota":        self.total_gap_to_quota,
            "at_risk_count":             len(self.at_risk_reps),
            "coaching_count":            len(self.coaching_reps),
            "avg_confidence_score":      round(total_confidence / n, 1),
            "avg_momentum_score":        round(total_momentum / n, 1),
            "likely_attainer_count":     len(self.likely_attainers),
        }
