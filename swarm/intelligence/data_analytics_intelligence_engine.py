"""Data Analytics Intelligence Engine — monitors data pipeline health, quality,
analytics reliability, and governance posture to detect pipeline failures, data
drift, quality degradation, model staleness, and insight gaps across the
analytics estate."""

from __future__ import annotations

import dataclasses
from enum import Enum


class DataRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class DataPattern(str, Enum):
    none                = "none"
    pipeline_failure    = "pipeline_failure"
    data_drift          = "data_drift"
    quality_degradation = "quality_degradation"
    model_staleness     = "model_staleness"
    insight_gap         = "insight_gap"


class DataSeverity(str, Enum):
    reliable   = "reliable"
    degraded   = "degraded"
    unreliable = "unreliable"
    blind      = "blind"


class DataAction(str, Enum):
    no_action                   = "no_action"
    data_monitoring             = "data_monitoring"
    pipeline_repair             = "pipeline_repair"
    data_quality_remediation    = "data_quality_remediation"
    drift_investigation         = "drift_investigation"
    model_retraining            = "model_retraining"
    schema_validation           = "schema_validation"
    data_governance_review      = "data_governance_review"
    analytics_emergency         = "analytics_emergency"


@dataclasses.dataclass
class DataInput:
    pipeline_id:                        str
    data_domain:                        str
    region:                             str
    pipeline_success_rate_pct:          float
    avg_pipeline_lag_minutes:           float
    data_completeness_pct:              float
    null_rate_pct:                      float
    duplicate_record_rate_pct:          float
    schema_change_count_30d:            int
    data_drift_score:                   float
    feature_distribution_shift:         float
    model_accuracy_decay_pct:           float
    prediction_confidence_score:        float
    report_delivery_failure_rate_pct:   float
    dashboard_error_rate_pct:           float
    analyst_query_failure_rate_pct:     float
    data_volume_anomaly_pct:            float
    source_system_failure_count:        int
    data_retention_compliance_pct:      float
    access_control_violations:          int
    row_count_variance_pct:             float
    cross_system_reconciliation_gap_pct: float


@dataclasses.dataclass
class DataResult:
    pipeline_id:                    str
    region:                         str
    data_risk:                      DataRisk
    data_pattern:                   DataPattern
    data_severity:                  DataSeverity
    recommended_action:             DataAction
    pipeline_score:                 float
    quality_score:                  float
    analytics_score:                float
    governance_score:               float
    data_composite:                 float
    has_data_alert:                 bool
    requires_data_governance:       bool
    estimated_insight_delay_hours:  float
    data_signal:                    str

    def to_dict(self) -> dict:
        return {
            "pipeline_id":                   self.pipeline_id,
            "region":                        self.region,
            "data_risk":                     self.data_risk.value,
            "data_pattern":                  self.data_pattern.value,
            "data_severity":                 self.data_severity.value,
            "recommended_action":            self.recommended_action.value,
            "pipeline_score":                round(self.pipeline_score, 1),
            "quality_score":                 round(self.quality_score, 1),
            "analytics_score":               round(self.analytics_score, 1),
            "governance_score":              round(self.governance_score, 1),
            "data_composite":                round(self.data_composite, 2),
            "has_data_alert":                self.has_data_alert,
            "requires_data_governance":      self.requires_data_governance,
            "estimated_insight_delay_hours": self.estimated_insight_delay_hours,
            "data_signal":                   self.data_signal,
        }


def _clamp(v: float) -> float:
    return max(0.0, min(100.0, v))


class DataAnalyticsIntelligenceEngine:
    """Monitors data pipeline health, quality, analytics reliability, and
    governance posture to surface actionable intelligence for data operations."""

    def __init__(self) -> None:
        self._results: list[DataResult] = []

    # ── sub-scores (HIGHER = more risk / worse health) ───────────────────────

    def _pipeline_score(self, inp: DataInput) -> float:
        score = 0.0
        # pipeline_success_rate_pct: lower is worse
        if inp.pipeline_success_rate_pct <= 0.80:
            score += 40.0
        elif inp.pipeline_success_rate_pct <= 0.92:
            score += 22.0
        elif inp.pipeline_success_rate_pct <= 0.97:
            score += 8.0
        # avg_pipeline_lag_minutes: higher is worse
        if inp.avg_pipeline_lag_minutes >= 120:
            score += 35.0
        elif inp.avg_pipeline_lag_minutes >= 60:
            score += 18.0
        elif inp.avg_pipeline_lag_minutes >= 30:
            score += 6.0
        # source_system_failure_count: higher is worse
        if inp.source_system_failure_count >= 5:
            score += 25.0
        elif inp.source_system_failure_count >= 2:
            score += 12.0
        return _clamp(score)

    def _quality_score(self, inp: DataInput) -> float:
        score = 0.0
        # data_completeness_pct: lower is worse
        if inp.data_completeness_pct <= 0.85:
            score += 40.0
        elif inp.data_completeness_pct <= 0.92:
            score += 22.0
        elif inp.data_completeness_pct <= 0.97:
            score += 8.0
        # null_rate_pct: higher is worse
        if inp.null_rate_pct >= 0.10:
            score += 35.0
        elif inp.null_rate_pct >= 0.05:
            score += 18.0
        elif inp.null_rate_pct >= 0.02:
            score += 6.0
        # duplicate_record_rate_pct: higher is worse
        if inp.duplicate_record_rate_pct >= 0.05:
            score += 25.0
        elif inp.duplicate_record_rate_pct >= 0.02:
            score += 12.0
        return _clamp(score)

    def _analytics_score(self, inp: DataInput) -> float:
        score = 0.0
        # data_drift_score: higher is worse
        if inp.data_drift_score >= 0.60:
            score += 45.0
        elif inp.data_drift_score >= 0.35:
            score += 25.0
        elif inp.data_drift_score >= 0.15:
            score += 10.0
        # model_accuracy_decay_pct: higher is worse
        if inp.model_accuracy_decay_pct >= 0.20:
            score += 30.0
        elif inp.model_accuracy_decay_pct >= 0.10:
            score += 15.0
        # dashboard_error_rate_pct: higher is worse
        if inp.dashboard_error_rate_pct >= 0.15:
            score += 25.0
        elif inp.dashboard_error_rate_pct >= 0.05:
            score += 12.0
        return _clamp(score)

    def _governance_score(self, inp: DataInput) -> float:
        score = 0.0
        # access_control_violations: higher is worse
        if inp.access_control_violations >= 5:
            score += 40.0
        elif inp.access_control_violations >= 2:
            score += 22.0
        elif inp.access_control_violations >= 1:
            score += 8.0
        # data_retention_compliance_pct: lower is worse
        if inp.data_retention_compliance_pct <= 0.70:
            score += 35.0
        elif inp.data_retention_compliance_pct <= 0.85:
            score += 18.0
        elif inp.data_retention_compliance_pct <= 0.95:
            score += 6.0
        # cross_system_reconciliation_gap_pct: higher is worse
        if inp.cross_system_reconciliation_gap_pct >= 0.15:
            score += 25.0
        elif inp.cross_system_reconciliation_gap_pct >= 0.08:
            score += 12.0
        return _clamp(score)

    # ── classification ───────────────────────────────────────────────────────

    def _classify_risk(self, composite: float) -> DataRisk:
        if composite >= 60:
            return DataRisk.critical
        if composite >= 40:
            return DataRisk.high
        if composite >= 20:
            return DataRisk.moderate
        return DataRisk.low

    def _classify_severity(self, composite: float) -> DataSeverity:
        if composite >= 60:
            return DataSeverity.blind
        if composite >= 40:
            return DataSeverity.unreliable
        if composite >= 20:
            return DataSeverity.degraded
        return DataSeverity.reliable

    def _classify_pattern(self, inp: DataInput) -> DataPattern:
        # Priority order: first match wins
        if inp.pipeline_success_rate_pct <= 0.85 and inp.source_system_failure_count >= 3:
            return DataPattern.pipeline_failure
        if inp.data_drift_score >= 0.50 and inp.feature_distribution_shift >= 0.40:
            return DataPattern.data_drift
        if inp.data_completeness_pct <= 0.88 and inp.null_rate_pct >= 0.08:
            return DataPattern.quality_degradation
        if inp.model_accuracy_decay_pct >= 0.15 and inp.prediction_confidence_score <= 0.55:
            return DataPattern.model_staleness
        if inp.dashboard_error_rate_pct >= 0.12 and inp.analyst_query_failure_rate_pct >= 0.10:
            return DataPattern.insight_gap
        return DataPattern.none

    def _recommended_action(
        self, risk: DataRisk, pattern: DataPattern
    ) -> DataAction:
        if risk == DataRisk.critical and pattern in (DataPattern.pipeline_failure, DataPattern.data_drift):
            return DataAction.analytics_emergency
        if risk == DataRisk.critical:
            return DataAction.data_governance_review
        if risk == DataRisk.high:
            if pattern == DataPattern.pipeline_failure:
                return DataAction.pipeline_repair
            if pattern == DataPattern.data_drift:
                return DataAction.drift_investigation
            if pattern == DataPattern.quality_degradation:
                return DataAction.data_quality_remediation
            if pattern == DataPattern.model_staleness:
                return DataAction.model_retraining
            if pattern == DataPattern.insight_gap:
                return DataAction.schema_validation
            return DataAction.data_monitoring
        if risk == DataRisk.moderate:
            return DataAction.data_monitoring
        return DataAction.no_action

    def _signal(self, composite: float, inp: DataInput, risk: DataRisk) -> str:
        if composite < 20:
            return (
                "Data pipelines reliable — quality, analytics and governance "
                "within operational standards"
            )
        label = risk.value.capitalize()
        return (
            f"{label} — {round(inp.pipeline_success_rate_pct * 100)}% pipeline success"
            f" — {round(inp.data_completeness_pct * 100)}% completeness"
            f" — drift {round(inp.data_drift_score * 100)}"
            f" — composite {round(composite)}"
        )

    # ── public API ───────────────────────────────────────────────────────────

    def assess(self, inp: DataInput) -> DataResult:
        pipeline   = self._pipeline_score(inp)
        quality    = self._quality_score(inp)
        analytics  = self._analytics_score(inp)
        governance = self._governance_score(inp)

        raw = (
            pipeline   * 0.30
            + quality  * 0.25
            + analytics * 0.25
            + governance * 0.20
        )
        composite = min(round(raw, 2), 100.0)

        risk     = self._classify_risk(composite)
        severity = self._classify_severity(composite)
        pattern  = self._classify_pattern(inp)
        action   = self._recommended_action(risk, pattern)

        has_data_alert = (
            composite >= 40
            or inp.pipeline_success_rate_pct <= 0.90
            or inp.data_drift_score >= 0.35
        )
        requires_data_governance = (
            composite >= 25
            or inp.access_control_violations >= 1
            or inp.data_retention_compliance_pct <= 0.90
        )
        estimated_insight_delay_hours = round(
            (inp.avg_pipeline_lag_minutes / 60) * (composite / 100 + 1), 2
        )

        result = DataResult(
            pipeline_id=inp.pipeline_id,
            region=inp.region,
            data_risk=risk,
            data_pattern=pattern,
            data_severity=severity,
            recommended_action=action,
            pipeline_score=pipeline,
            quality_score=quality,
            analytics_score=analytics,
            governance_score=governance,
            data_composite=composite,
            has_data_alert=has_data_alert,
            requires_data_governance=requires_data_governance,
            estimated_insight_delay_hours=estimated_insight_delay_hours,
            data_signal=self._signal(composite, inp, risk),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[DataInput]) -> list[DataResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total":                          0,
                "risk_counts":                    {},
                "pattern_counts":                 {},
                "severity_counts":                {},
                "action_counts":                  {},
                "avg_data_composite":             0.0,
                "data_alert_count":               0,
                "governance_count":               0,
                "avg_pipeline_score":             0.0,
                "avg_quality_score":              0.0,
                "avg_analytics_score":            0.0,
                "avg_governance_score":           0.0,
                "avg_estimated_insight_delay_hours": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_pipe = total_qual = total_anal = total_gov = total_delay = 0.0
        alert_count = gov_count = 0

        for r in self._results:
            risk_counts[r.data_risk.value]         = risk_counts.get(r.data_risk.value, 0) + 1
            pattern_counts[r.data_pattern.value]   = pattern_counts.get(r.data_pattern.value, 0) + 1
            severity_counts[r.data_severity.value] = severity_counts.get(r.data_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp  += r.data_composite
            total_pipe  += r.pipeline_score
            total_qual  += r.quality_score
            total_anal  += r.analytics_score
            total_gov   += r.governance_score
            total_delay += r.estimated_insight_delay_hours
            if r.has_data_alert:
                alert_count += 1
            if r.requires_data_governance:
                gov_count += 1

        n = len(self._results)
        return {
            "total":                            n,
            "risk_counts":                      risk_counts,
            "pattern_counts":                   pattern_counts,
            "severity_counts":                  severity_counts,
            "action_counts":                    action_counts,
            "avg_data_composite":               round(total_comp  / n, 2),
            "data_alert_count":                 alert_count,
            "governance_count":                 gov_count,
            "avg_pipeline_score":               round(total_pipe  / n, 1),
            "avg_quality_score":                round(total_qual  / n, 1),
            "avg_analytics_score":              round(total_anal  / n, 1),
            "avg_governance_score":             round(total_gov   / n, 1),
            "avg_estimated_insight_delay_hours": round(total_delay / n, 2),
        }
