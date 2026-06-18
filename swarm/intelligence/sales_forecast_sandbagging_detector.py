"""Sales Forecast Sandbagging Detector — identifies reps who systematically
under-forecast to guarantee over-attainment, gaming compensation and quota
recalibration mechanisms."""

from __future__ import annotations

import dataclasses
from enum import Enum


class SandbaggingRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class SandbaggingPattern(str, Enum):
    none               = "none"
    consistent_low     = "consistent_low"
    deal_hoarding      = "deal_hoarding"
    late_pushes        = "late_pushes"
    forecast_delay     = "forecast_delay"
    pull_forward_abuse = "pull_forward_abuse"


class SandbaggingSeverity(str, Enum):
    clean      = "clean"
    watch      = "watch"
    suspicious = "suspicious"
    confirmed  = "confirmed"


class SandbaggingAction(str, Enum):
    no_action          = "no_action"
    monitor            = "monitor"
    manager_review     = "manager_review"
    quota_recalibrate  = "quota_recalibrate"
    compensation_audit = "compensation_audit"


@dataclasses.dataclass
class SalesForecastSandbaggingInput:
    rep_id:                              str
    region:                              str
    forecast_period_id:                  str
    committed_forecast_usd:              float
    actual_attained_usd:                 float
    prior_period_over_attainment_pct:    float
    avg_quarter_over_attainment_pct:     float
    deals_held_from_forecast_count:      int
    late_stage_deals_not_committed_count: int
    close_date_pushed_past_period_count: int
    pipeline_coverage_ratio:             float
    forecast_submission_days_late:       int
    forecast_change_count:               int
    sandbagged_deal_value_usd:           float
    avg_deal_size_usd:                   float
    peer_avg_over_attainment_pct:        float
    rep_tenure_years:                    float
    quota_usd:                           float
    manager_override_count:              int
    deal_pull_forward_count:             int
    historical_accuracy_pct:             float
    deals_pulled_from_next_period_count: int


@dataclasses.dataclass
class SalesForecastSandbaggingResult:
    rep_id:                       str
    region:                       str
    sandbagging_risk:             SandbaggingRisk
    sandbagging_pattern:          SandbaggingPattern
    sandbagging_severity:         SandbaggingSeverity
    recommended_action:           SandbaggingAction
    forecast_accuracy_score:      float
    pattern_consistency_score:    float
    deal_manipulation_score:      float
    over_attainment_score:        float
    sandbagging_composite:        float
    is_sandbagging:               bool
    requires_quota_review:        bool
    estimated_hidden_pipeline_usd: float
    sandbagging_signal:           str

    def to_dict(self) -> dict:
        return {
            "rep_id":                        self.rep_id,
            "region":                        self.region,
            "sandbagging_risk":              self.sandbagging_risk.value,
            "sandbagging_pattern":           self.sandbagging_pattern.value,
            "sandbagging_severity":          self.sandbagging_severity.value,
            "recommended_action":            self.recommended_action.value,
            "forecast_accuracy_score":       round(self.forecast_accuracy_score, 1),
            "pattern_consistency_score":     round(self.pattern_consistency_score, 1),
            "deal_manipulation_score":       round(self.deal_manipulation_score, 1),
            "over_attainment_score":         round(self.over_attainment_score, 1),
            "sandbagging_composite":         round(self.sandbagging_composite, 1),
            "is_sandbagging":                self.is_sandbagging,
            "requires_quota_review":         self.requires_quota_review,
            "estimated_hidden_pipeline_usd": round(self.estimated_hidden_pipeline_usd, 2),
            "sandbagging_signal":            self.sandbagging_signal,
        }


def _clamp(v: float) -> float:
    return max(0.0, min(100.0, v))


class SalesForecastSandbaggingDetector:
    """Detects systematic forecast sandbagging in sales rep behavior."""

    def __init__(self) -> None:
        self._results: list[SalesForecastSandbaggingResult] = []

    # ── sub-scores (HIGHER = more sandbagging) ──────────────────────────────

    def _forecast_accuracy_score(self, inp: SalesForecastSandbaggingInput) -> float:
        score = 0.0
        # Current period over-attainment vs committed
        if inp.committed_forecast_usd > 0:
            attainment_ratio = inp.actual_attained_usd / inp.committed_forecast_usd
            if attainment_ratio >= 2.0:
                score += 50.0
            elif attainment_ratio >= 1.75:
                score += 38.0
            elif attainment_ratio >= 1.5:
                score += 25.0
            elif attainment_ratio >= 1.25:
                score += 12.0
        # Low historical accuracy (high variance = gaming)
        if inp.historical_accuracy_pct < 70:
            score += 10.0
        elif inp.historical_accuracy_pct < 80:
            score += 5.0
        # Submitted late — avoids early commitment
        if inp.forecast_submission_days_late >= 5:
            score += 20.0
        elif inp.forecast_submission_days_late >= 2:
            score += 10.0
        return _clamp(score)

    def _pattern_consistency_score(self, inp: SalesForecastSandbaggingInput) -> float:
        score = 0.0
        # Consistent multi-period over-attainment vs peers
        if inp.avg_quarter_over_attainment_pct >= 160:
            score += 45.0
        elif inp.avg_quarter_over_attainment_pct >= 140:
            score += 32.0
        elif inp.avg_quarter_over_attainment_pct >= 120:
            score += 18.0
        # Rep over-attainment vs peer benchmark
        if inp.peer_avg_over_attainment_pct > 0:
            outperform_delta = inp.avg_quarter_over_attainment_pct - inp.peer_avg_over_attainment_pct
            if outperform_delta >= 50:
                score += 30.0
            elif outperform_delta >= 30:
                score += 18.0
            elif outperform_delta >= 15:
                score += 8.0
        # Manager overrides indicate gaming detected by management
        if inp.manager_override_count >= 3:
            score += 25.0
        elif inp.manager_override_count >= 1:
            score += 12.0
        return _clamp(score)

    def _deal_manipulation_score(self, inp: SalesForecastSandbaggingInput) -> float:
        score = 0.0
        # Deals held from forecast
        if inp.deals_held_from_forecast_count >= 5:
            score += 45.0
        elif inp.deals_held_from_forecast_count >= 3:
            score += 30.0
        elif inp.deals_held_from_forecast_count >= 1:
            score += 15.0
        # Late-stage deals not committed
        if inp.late_stage_deals_not_committed_count >= 4:
            score += 30.0
        elif inp.late_stage_deals_not_committed_count >= 2:
            score += 18.0
        elif inp.late_stage_deals_not_committed_count >= 1:
            score += 8.0
        # Close date pushed past period end
        if inp.close_date_pushed_past_period_count >= 3:
            score += 20.0
        elif inp.close_date_pushed_past_period_count >= 1:
            score += 10.0
        # Pull-forward abuse (robbing next period)
        if inp.deal_pull_forward_count >= 3:
            score += 10.0
        return _clamp(score)

    def _over_attainment_score(self, inp: SalesForecastSandbaggingInput) -> float:
        score = 0.0
        # Prior period over-attainment
        if inp.prior_period_over_attainment_pct >= 200:
            score += 50.0
        elif inp.prior_period_over_attainment_pct >= 175:
            score += 38.0
        elif inp.prior_period_over_attainment_pct >= 150:
            score += 25.0
        elif inp.prior_period_over_attainment_pct >= 125:
            score += 12.0
        # Pipeline far above quota with low commitment
        if inp.quota_usd > 0:
            coverage_vs_commitment = (inp.committed_forecast_usd / inp.quota_usd) if inp.quota_usd > 0 else 1.0
            if inp.pipeline_coverage_ratio >= 4.0 and coverage_vs_commitment < 0.8:
                score += 30.0
            elif inp.pipeline_coverage_ratio >= 3.0 and coverage_vs_commitment < 0.9:
                score += 18.0
        # Deals pulled from next period
        if inp.deals_pulled_from_next_period_count >= 3:
            score += 20.0
        elif inp.deals_pulled_from_next_period_count >= 1:
            score += 10.0
        return _clamp(score)

    # ── classification ───────────────────────────────────────────────────────

    def _classify_risk(self, composite: float) -> SandbaggingRisk:
        if composite < 20:
            return SandbaggingRisk.low
        if composite < 40:
            return SandbaggingRisk.moderate
        if composite < 60:
            return SandbaggingRisk.high
        return SandbaggingRisk.critical

    def _classify_severity(self, composite: float) -> SandbaggingSeverity:
        if composite < 20:
            return SandbaggingSeverity.clean
        if composite < 40:
            return SandbaggingSeverity.watch
        if composite < 60:
            return SandbaggingSeverity.suspicious
        return SandbaggingSeverity.confirmed

    def _classify_pattern(
        self,
        inp: SalesForecastSandbaggingInput,
        accuracy: float,
        pattern: float,
        deal: float,
    ) -> SandbaggingPattern:
        if inp.deals_held_from_forecast_count >= 3:
            return SandbaggingPattern.deal_hoarding
        if inp.close_date_pushed_past_period_count >= 3:
            return SandbaggingPattern.late_pushes
        if inp.forecast_submission_days_late >= 3:
            return SandbaggingPattern.forecast_delay
        if inp.deal_pull_forward_count >= 3:
            return SandbaggingPattern.pull_forward_abuse
        if inp.avg_quarter_over_attainment_pct >= 140:
            return SandbaggingPattern.consistent_low
        return SandbaggingPattern.none

    def _recommended_action(
        self, risk: SandbaggingRisk, composite: float
    ) -> SandbaggingAction:
        if composite >= 60:
            return SandbaggingAction.compensation_audit
        if risk == SandbaggingRisk.high:
            return SandbaggingAction.quota_recalibrate
        if risk == SandbaggingRisk.moderate:
            return SandbaggingAction.manager_review
        if composite >= 10:
            return SandbaggingAction.monitor
        return SandbaggingAction.no_action

    def _signal(
        self,
        pattern: SandbaggingPattern,
        composite: float,
        inp: SalesForecastSandbaggingInput,
    ) -> str:
        if pattern == SandbaggingPattern.none:
            return "forecast behavior within normal parameters"
        msgs = {
            SandbaggingPattern.consistent_low: (
                f"avg over-attainment {inp.avg_quarter_over_attainment_pct:.0f}% "
                f"vs peer avg {inp.peer_avg_over_attainment_pct:.0f}%"
            ),
            SandbaggingPattern.deal_hoarding: (
                f"{inp.deals_held_from_forecast_count} deals held from forecast "
                f"({inp.late_stage_deals_not_committed_count} late-stage uncommitted)"
            ),
            SandbaggingPattern.late_pushes: (
                f"{inp.close_date_pushed_past_period_count} deal(s) pushed past period end"
            ),
            SandbaggingPattern.forecast_delay: (
                f"forecast submitted {inp.forecast_submission_days_late} days late — "
                f"avoids early commitment"
            ),
            SandbaggingPattern.pull_forward_abuse: (
                f"{inp.deal_pull_forward_count} deal(s) pulled from future period"
            ),
        }
        base = msgs.get(pattern, f"sandbagging composite {composite:.0f}")
        return f"{base} — composite {composite:.0f}"

    # ── public API ───────────────────────────────────────────────────────────

    def assess(self, inp: SalesForecastSandbaggingInput) -> SalesForecastSandbaggingResult:
        accuracy = self._forecast_accuracy_score(inp)
        pattern  = self._pattern_consistency_score(inp)
        deal     = self._deal_manipulation_score(inp)
        overatt  = self._over_attainment_score(inp)

        composite = _clamp(
            accuracy * 0.30
            + pattern * 0.25
            + deal    * 0.25
            + overatt * 0.20
        )
        composite = round(composite, 1)

        risk     = self._classify_risk(composite)
        severity = self._classify_severity(composite)
        patt     = self._classify_pattern(inp, accuracy, pattern, deal)
        action   = self._recommended_action(risk, composite)

        is_sandbagging = (
            composite >= 40
            or inp.prior_period_over_attainment_pct >= 150
            or inp.deals_held_from_forecast_count >= 3
        )
        requires_quota_review = (
            composite >= 30
            or inp.avg_quarter_over_attainment_pct >= 130
            or (inp.deals_held_from_forecast_count >= 2 and inp.forecast_change_count >= 3)
        )

        estimated_hidden_pipeline_usd = inp.sandbagged_deal_value_usd * (composite / 100.0)

        result = SalesForecastSandbaggingResult(
            rep_id=inp.rep_id,
            region=inp.region,
            sandbagging_risk=risk,
            sandbagging_pattern=patt,
            sandbagging_severity=severity,
            recommended_action=action,
            forecast_accuracy_score=accuracy,
            pattern_consistency_score=pattern,
            deal_manipulation_score=deal,
            over_attainment_score=overatt,
            sandbagging_composite=composite,
            is_sandbagging=is_sandbagging,
            requires_quota_review=requires_quota_review,
            estimated_hidden_pipeline_usd=estimated_hidden_pipeline_usd,
            sandbagging_signal=self._signal(patt, composite, inp),
        )
        self._results.append(result)
        return result

    def assess_batch(
        self, inputs: list[SalesForecastSandbaggingInput]
    ) -> list[SalesForecastSandbaggingResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total":                           0,
                "risk_counts":                     {},
                "pattern_counts":                  {},
                "severity_counts":                 {},
                "action_counts":                   {},
                "avg_sandbagging_composite":        0.0,
                "sandbagging_count":                0,
                "quota_review_count":               0,
                "avg_forecast_accuracy_score":      0.0,
                "avg_pattern_consistency_score":    0.0,
                "avg_deal_manipulation_score":      0.0,
                "avg_over_attainment_score":        0.0,
                "total_estimated_hidden_pipeline_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_acc = total_pat = total_deal = total_over = total_hidden = 0.0
        sandbagging = quota_review = 0

        for r in self._results:
            risk_counts[r.sandbagging_risk.value]       = risk_counts.get(r.sandbagging_risk.value, 0) + 1
            pattern_counts[r.sandbagging_pattern.value] = pattern_counts.get(r.sandbagging_pattern.value, 0) + 1
            severity_counts[r.sandbagging_severity.value] = severity_counts.get(r.sandbagging_severity.value, 0) + 1
            action_counts[r.recommended_action.value]   = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp   += r.sandbagging_composite
            total_acc    += r.forecast_accuracy_score
            total_pat    += r.pattern_consistency_score
            total_deal   += r.deal_manipulation_score
            total_over   += r.over_attainment_score
            total_hidden += r.estimated_hidden_pipeline_usd
            if r.is_sandbagging:
                sandbagging += 1
            if r.requires_quota_review:
                quota_review += 1

        n = len(self._results)
        return {
            "total":                              n,
            "risk_counts":                        risk_counts,
            "pattern_counts":                     pattern_counts,
            "severity_counts":                    severity_counts,
            "action_counts":                      action_counts,
            "avg_sandbagging_composite":          round(total_comp / n, 1),
            "sandbagging_count":                  sandbagging,
            "quota_review_count":                 quota_review,
            "avg_forecast_accuracy_score":        round(total_acc  / n, 1),
            "avg_pattern_consistency_score":      round(total_pat  / n, 1),
            "avg_deal_manipulation_score":        round(total_deal / n, 1),
            "avg_over_attainment_score":          round(total_over / n, 1),
            "total_estimated_hidden_pipeline_usd": round(total_hidden, 2),
        }
