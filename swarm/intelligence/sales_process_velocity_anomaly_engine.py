"""Sales Process Velocity Anomaly Engine — detects abnormally fast or slow
deal progression through sales stages that signals gaming, misclassification,
or forecast manipulation."""

from __future__ import annotations

import dataclasses
from enum import Enum


class VelocityAnomaly(str, Enum):
    normal = "normal"
    suspicious_fast = "suspicious_fast"
    stage_skipping = "stage_skipping"
    stalled = "stalled"
    recycled = "recycled"
    forced_close = "forced_close"


class VelocityRisk(str, Enum):
    low = "low"
    moderate = "moderate"
    high = "high"
    critical = "critical"


class VelocityAlert(str, Enum):
    none = "none"
    flag = "flag"
    review = "review"
    escalate = "escalate"
    audit = "audit"


class VelocitySeverity(str, Enum):
    clean = "clean"
    watch = "watch"
    anomalous = "anomalous"
    fraud_risk = "fraud_risk"


@dataclasses.dataclass
class SalesProcessVelocityInput:
    deal_id: str
    rep_id: str
    deal_value_usd: float
    company_avg_deal_value_usd: float
    days_in_pipeline: int
    company_avg_days_in_pipeline: float
    stages_completed: int
    expected_stages: int
    discovery_days: int
    expected_discovery_days: float
    demo_days: int
    expected_demo_days: float
    proposal_days: int
    expected_proposal_days: float
    negotiation_days: int
    expected_negotiation_days: float
    stage_regression_count: int
    stage_skip_count: int
    close_date_changes: int
    forecast_category_changes: int
    end_of_period_push: int
    rep_avg_deal_cycle_days: float


@dataclasses.dataclass
class SalesProcessVelocityResult:
    deal_id: str
    rep_id: str
    velocity_anomaly: VelocityAnomaly
    velocity_risk: VelocityRisk
    velocity_alert: VelocityAlert
    velocity_severity: VelocitySeverity
    stage_completion_score: float
    timeline_deviation_score: float
    forecast_integrity_score: float
    pattern_risk_score: float
    velocity_composite: float
    is_anomalous: bool
    requires_review: bool
    pipeline_days_deviation: float
    velocity_signal: str

    def to_dict(self) -> dict:
        return {
            "deal_id":                  self.deal_id,
            "rep_id":                   self.rep_id,
            "velocity_anomaly":         self.velocity_anomaly.value,
            "velocity_risk":            self.velocity_risk.value,
            "velocity_alert":           self.velocity_alert.value,
            "velocity_severity":        self.velocity_severity.value,
            "stage_completion_score":   round(self.stage_completion_score, 1),
            "timeline_deviation_score": round(self.timeline_deviation_score, 1),
            "forecast_integrity_score": round(self.forecast_integrity_score, 1),
            "pattern_risk_score":       round(self.pattern_risk_score, 1),
            "velocity_composite":       round(self.velocity_composite, 1),
            "is_anomalous":             self.is_anomalous,
            "requires_review":          self.requires_review,
            "pipeline_days_deviation":  round(self.pipeline_days_deviation, 1),
            "velocity_signal":          self.velocity_signal,
        }


def _clamp(v: float) -> float:
    return max(0.0, min(100.0, v))


class SalesProcessVelocityAnomalyEngine:
    """Detects velocity anomalies in deal pipeline progression."""

    def __init__(self) -> None:
        self._results: list[SalesProcessVelocityResult] = []

    # ── sub-scores (HIGHER = more anomalous) ────────────────────────────────

    def _stage_completion_score(self, inp: SalesProcessVelocityInput) -> float:
        score = 0.0
        # Stages skipped
        if inp.stage_skip_count >= 3:
            score += 45.0
        elif inp.stage_skip_count >= 2:
            score += 30.0
        elif inp.stage_skip_count >= 1:
            score += 15.0
        # Stage regressions (deal went backwards)
        if inp.stage_regression_count >= 3:
            score += 35.0
        elif inp.stage_regression_count >= 2:
            score += 22.0
        elif inp.stage_regression_count >= 1:
            score += 10.0
        # Stages completed vs expected
        if inp.expected_stages > 0:
            completion_ratio = inp.stages_completed / inp.expected_stages
            if completion_ratio < 0.5 and inp.days_in_pipeline > inp.company_avg_days_in_pipeline * 0.8:
                score += 20.0
        return _clamp(score)

    def _timeline_deviation_score(self, inp: SalesProcessVelocityInput) -> float:
        score = 0.0
        # Overall pipeline speed vs company avg
        if inp.company_avg_days_in_pipeline > 0:
            speed_ratio = inp.days_in_pipeline / inp.company_avg_days_in_pipeline
        else:
            speed_ratio = 1.0
        if speed_ratio < 0.1:
            score += 45.0  # < 10% of normal time = very suspicious
        elif speed_ratio < 0.25:
            score += 30.0
        elif speed_ratio < 0.4:
            score += 18.0
        elif speed_ratio > 3.0:
            score += 25.0  # stalled deals
        elif speed_ratio > 2.0:
            score += 12.0
        # Individual stage deviations
        for actual, expected in [
            (inp.discovery_days, inp.expected_discovery_days),
            (inp.demo_days, inp.expected_demo_days),
            (inp.proposal_days, inp.expected_proposal_days),
            (inp.negotiation_days, inp.expected_negotiation_days),
        ]:
            if expected > 0 and actual > 0:
                stage_ratio = actual / expected
                if stage_ratio < 0.15:
                    score += 8.0
                elif stage_ratio < 0.3:
                    score += 4.0
        return _clamp(score)

    def _forecast_integrity_score(self, inp: SalesProcessVelocityInput) -> float:
        score = 0.0
        # Repeated close date changes
        if inp.close_date_changes >= 5:
            score += 40.0
        elif inp.close_date_changes >= 3:
            score += 28.0
        elif inp.close_date_changes >= 2:
            score += 15.0
        # Forecast category changes
        if inp.forecast_category_changes >= 4:
            score += 35.0
        elif inp.forecast_category_changes >= 2:
            score += 20.0
        elif inp.forecast_category_changes >= 1:
            score += 8.0
        # End of period push
        if inp.end_of_period_push:
            score += 25.0
        return _clamp(score)

    def _pattern_risk_score(self, inp: SalesProcessVelocityInput) -> float:
        score = 0.0
        # Deal much larger than avg
        if inp.company_avg_deal_value_usd > 0:
            size_ratio = inp.deal_value_usd / inp.company_avg_deal_value_usd
            if size_ratio > 10.0 and inp.days_in_pipeline < inp.company_avg_days_in_pipeline * 0.5:
                score += 35.0
            elif size_ratio > 5.0 and inp.days_in_pipeline < inp.company_avg_days_in_pipeline * 0.4:
                score += 20.0
        # Rep closing much faster than their own avg
        if inp.rep_avg_deal_cycle_days > 0:
            rep_ratio = inp.days_in_pipeline / inp.rep_avg_deal_cycle_days
            if rep_ratio < 0.2:
                score += 30.0
            elif rep_ratio < 0.35:
                score += 18.0
        return _clamp(score)

    # ── classification ───────────────────────────────────────────────────────

    def _classify_anomaly(
        self,
        inp: SalesProcessVelocityInput,
        timeline: float,
        stage: float,
        forecast: float,
    ) -> VelocityAnomaly:
        speed_ratio = (inp.days_in_pipeline / inp.company_avg_days_in_pipeline) if inp.company_avg_days_in_pipeline > 0 else 1.0
        if inp.stage_skip_count >= 2:
            return VelocityAnomaly.stage_skipping
        if inp.stage_regression_count >= 2:
            return VelocityAnomaly.recycled
        if inp.end_of_period_push and inp.close_date_changes >= 2:
            return VelocityAnomaly.forced_close
        if speed_ratio < 0.3 and timeline > 25:
            return VelocityAnomaly.suspicious_fast
        if speed_ratio > 2.5:
            return VelocityAnomaly.stalled
        return VelocityAnomaly.normal

    def _classify_risk(self, composite: float) -> VelocityRisk:
        if composite < 20:
            return VelocityRisk.low
        if composite < 40:
            return VelocityRisk.moderate
        if composite < 60:
            return VelocityRisk.high
        return VelocityRisk.critical

    def _classify_severity(self, composite: float) -> VelocitySeverity:
        if composite < 20:
            return VelocitySeverity.clean
        if composite < 40:
            return VelocitySeverity.watch
        if composite < 65:
            return VelocitySeverity.anomalous
        return VelocitySeverity.fraud_risk

    def _recommended_alert(self, risk: VelocityRisk, composite: float) -> VelocityAlert:
        if composite >= 65:
            return VelocityAlert.audit
        if risk == VelocityRisk.critical:
            return VelocityAlert.escalate
        if risk == VelocityRisk.high:
            return VelocityAlert.review
        if risk == VelocityRisk.moderate:
            return VelocityAlert.flag
        return VelocityAlert.none

    def _signal(
        self,
        anomaly: VelocityAnomaly,
        composite: float,
        inp: SalesProcessVelocityInput,
    ) -> str:
        if anomaly == VelocityAnomaly.normal:
            return "deal velocity within normal parameters"
        speed_ratio = (inp.days_in_pipeline / inp.company_avg_days_in_pipeline) if inp.company_avg_days_in_pipeline > 0 else 1.0
        msgs = {
            VelocityAnomaly.suspicious_fast: (
                f"deal closed {(1-speed_ratio)*100:.0f}% faster than avg "
                f"({inp.days_in_pipeline} vs {inp.company_avg_days_in_pipeline:.0f} days)"
            ),
            VelocityAnomaly.stage_skipping: (
                f"{inp.stage_skip_count} stage skip(s) detected — "
                f"{inp.stages_completed}/{inp.expected_stages} stages completed"
            ),
            VelocityAnomaly.stalled: (
                f"deal stalled — {inp.days_in_pipeline} days vs avg {inp.company_avg_days_in_pipeline:.0f}"
            ),
            VelocityAnomaly.recycled: (
                f"deal recycled {inp.stage_regression_count}x — instability in qualification"
            ),
            VelocityAnomaly.forced_close: (
                f"end-of-period forced close — {inp.close_date_changes} date changes, "
                f"{inp.forecast_category_changes} category shifts"
            ),
        }
        base = msgs.get(anomaly, f"velocity anomaly composite {composite:.0f}")
        return f"{base} — composite {composite:.0f}"

    # ── public API ───────────────────────────────────────────────────────────

    def assess(self, inp: SalesProcessVelocityInput) -> SalesProcessVelocityResult:
        stage    = self._stage_completion_score(inp)
        timeline = self._timeline_deviation_score(inp)
        forecast = self._forecast_integrity_score(inp)
        pattern  = self._pattern_risk_score(inp)

        composite = _clamp(
            stage    * 0.25
            + timeline * 0.35
            + forecast * 0.25
            + pattern  * 0.15
        )
        composite = round(composite, 1)

        anomaly  = self._classify_anomaly(inp, timeline, stage, forecast)
        risk     = self._classify_risk(composite)
        severity = self._classify_severity(composite)
        alert    = self._recommended_alert(risk, composite)

        is_anomalous = (
            composite >= 35
            or inp.stage_skip_count >= 2
            or (inp.end_of_period_push == 1 and inp.close_date_changes >= 3)
        )
        requires_review = (
            composite >= 30
            or inp.close_date_changes >= 4
            or inp.stage_skip_count >= 2
        )

        avg_days = inp.company_avg_days_in_pipeline
        pipeline_days_deviation = inp.days_in_pipeline - avg_days

        result = SalesProcessVelocityResult(
            deal_id=inp.deal_id,
            rep_id=inp.rep_id,
            velocity_anomaly=anomaly,
            velocity_risk=risk,
            velocity_alert=alert,
            velocity_severity=severity,
            stage_completion_score=stage,
            timeline_deviation_score=timeline,
            forecast_integrity_score=forecast,
            pattern_risk_score=pattern,
            velocity_composite=composite,
            is_anomalous=is_anomalous,
            requires_review=requires_review,
            pipeline_days_deviation=pipeline_days_deviation,
            velocity_signal=self._signal(anomaly, composite, inp),
        )
        self._results.append(result)
        return result

    def assess_batch(
        self, inputs: list[SalesProcessVelocityInput]
    ) -> list[SalesProcessVelocityResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "anomaly_counts": {},
                "risk_counts": {},
                "alert_counts": {},
                "severity_counts": {},
                "avg_velocity_composite": 0.0,
                "anomalous_count": 0,
                "review_required_count": 0,
                "avg_stage_completion_score": 0.0,
                "avg_timeline_deviation_score": 0.0,
                "avg_forecast_integrity_score": 0.0,
                "avg_pattern_risk_score": 0.0,
                "avg_pipeline_days_deviation": 0.0,
            }

        anomaly_counts:  dict[str, int] = {}
        risk_counts:     dict[str, int] = {}
        alert_counts:    dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        total_comp = total_stage = total_time = total_fore = total_pat = total_dev = 0.0
        anomalous = review = 0

        for r in self._results:
            anomaly_counts[r.velocity_anomaly.value]  = anomaly_counts.get(r.velocity_anomaly.value, 0) + 1
            risk_counts[r.velocity_risk.value]        = risk_counts.get(r.velocity_risk.value, 0) + 1
            alert_counts[r.velocity_alert.value]      = alert_counts.get(r.velocity_alert.value, 0) + 1
            severity_counts[r.velocity_severity.value] = severity_counts.get(r.velocity_severity.value, 0) + 1
            total_comp  += r.velocity_composite
            total_stage += r.stage_completion_score
            total_time  += r.timeline_deviation_score
            total_fore  += r.forecast_integrity_score
            total_pat   += r.pattern_risk_score
            total_dev   += r.pipeline_days_deviation
            if r.is_anomalous:
                anomalous += 1
            if r.requires_review:
                review += 1

        n = len(self._results)
        return {
            "total":                        n,
            "anomaly_counts":               anomaly_counts,
            "risk_counts":                  risk_counts,
            "alert_counts":                 alert_counts,
            "severity_counts":              severity_counts,
            "avg_velocity_composite":       round(total_comp  / n, 1),
            "anomalous_count":              anomalous,
            "review_required_count":        review,
            "avg_stage_completion_score":   round(total_stage / n, 1),
            "avg_timeline_deviation_score": round(total_time  / n, 1),
            "avg_forecast_integrity_score": round(total_fore  / n, 1),
            "avg_pattern_risk_score":       round(total_pat   / n, 1),
            "avg_pipeline_days_deviation":  round(total_dev   / n, 1),
        }
