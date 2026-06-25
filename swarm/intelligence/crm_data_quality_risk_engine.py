"""CRM Data Quality Risk Engine — detects incomplete, stale, and inconsistent
CRM records maintained by sales reps that distort pipeline visibility,
forecast accuracy, and revenue reporting."""

from __future__ import annotations

import dataclasses
from enum import Enum


class DataQualityRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class QualityFailureMode(str, Enum):
    none               = "none"
    missing_data       = "missing_data"
    stale_records      = "stale_records"
    stage_drift        = "stage_drift"
    activity_gap       = "activity_gap"
    duplicate_accounts = "duplicate_accounts"


class QualitySeverity(str, Enum):
    clean       = "clean"
    degraded    = "degraded"
    unreliable  = "unreliable"
    corrupt     = "corrupt"


class QualityAction(str, Enum):
    no_action       = "no_action"
    self_remediate  = "self_remediate"
    crm_coaching    = "crm_coaching"
    data_audit      = "data_audit"
    pipeline_freeze = "pipeline_freeze"


@dataclasses.dataclass
class CRMDataQualityInput:
    rep_id:                              str
    region:                              str
    evaluation_period_id:                str
    total_records_evaluated:             int
    missing_close_date_count:            int
    missing_opportunity_value_count:     int
    missing_contact_count:               int
    stale_record_count:                  int
    stage_mismatch_count:                int
    duplicate_account_count:             int
    missing_decision_maker_count:        int
    data_entry_completeness_pct:         float
    records_with_activity_notes_pct:     float
    forecast_without_recent_activity_count: int
    overdue_follow_up_count:             int
    avg_record_staleness_days:           float
    deal_source_missing_count:           int
    crm_login_frequency_last_30d:        int
    auto_filled_fields_pct:              float
    records_audited_by_admin_count:      int
    pipeline_audit_score:                float
    last_crm_training_days_ago:          int


@dataclasses.dataclass
class CRMDataQualityResult:
    rep_id:                            str
    region:                            str
    data_quality_risk:                 DataQualityRisk
    quality_failure_mode:              QualityFailureMode
    quality_severity:                  QualitySeverity
    recommended_action:                QualityAction
    completeness_score:                float
    accuracy_score:                    float
    timeliness_score:                  float
    activity_coverage_score:           float
    quality_composite:                 float
    is_data_quality_risk:              bool
    requires_data_audit:               bool
    estimated_pipeline_distortion_pct: float
    quality_signal:                    str

    def to_dict(self) -> dict:
        return {
            "rep_id":                            self.rep_id,
            "region":                            self.region,
            "data_quality_risk":                 self.data_quality_risk.value,
            "quality_failure_mode":              self.quality_failure_mode.value,
            "quality_severity":                  self.quality_severity.value,
            "recommended_action":                self.recommended_action.value,
            "completeness_score":                round(self.completeness_score, 1),
            "accuracy_score":                    round(self.accuracy_score, 1),
            "timeliness_score":                  round(self.timeliness_score, 1),
            "activity_coverage_score":           round(self.activity_coverage_score, 1),
            "quality_composite":                 round(self.quality_composite, 1),
            "is_data_quality_risk":              self.is_data_quality_risk,
            "requires_data_audit":               self.requires_data_audit,
            "estimated_pipeline_distortion_pct": round(self.estimated_pipeline_distortion_pct, 1),
            "quality_signal":                    self.quality_signal,
        }


def _clamp(v: float) -> float:
    return max(0.0, min(100.0, v))


class CRMDataQualityRiskEngine:
    """Identifies CRM data quality issues that distort pipeline and forecast integrity."""

    def __init__(self) -> None:
        self._results: list[CRMDataQualityResult] = []

    # ── sub-scores (HIGHER = worse quality) ─────────────────────────────────

    def _completeness_score(self, inp: CRMDataQualityInput) -> float:
        score = 0.0
        # Low overall data entry completeness
        if inp.data_entry_completeness_pct < 50:
            score += 50.0
        elif inp.data_entry_completeness_pct < 65:
            score += 35.0
        elif inp.data_entry_completeness_pct < 80:
            score += 18.0
        # Missing close dates
        if inp.missing_close_date_count >= 8:
            score += 30.0
        elif inp.missing_close_date_count >= 5:
            score += 20.0
        elif inp.missing_close_date_count >= 2:
            score += 8.0
        # Missing opportunity values
        if inp.missing_opportunity_value_count >= 5:
            score += 20.0
        elif inp.missing_opportunity_value_count >= 3:
            score += 12.0
        elif inp.missing_opportunity_value_count >= 1:
            score += 5.0
        return _clamp(score)

    def _accuracy_score(self, inp: CRMDataQualityInput) -> float:
        score = 0.0
        # Stage mismatches vs deal age
        if inp.stage_mismatch_count >= 6:
            score += 40.0
        elif inp.stage_mismatch_count >= 4:
            score += 28.0
        elif inp.stage_mismatch_count >= 2:
            score += 15.0
        # Duplicate accounts (data integrity failure)
        if inp.duplicate_account_count >= 5:
            score += 35.0
        elif inp.duplicate_account_count >= 2:
            score += 20.0
        elif inp.duplicate_account_count >= 1:
            score += 8.0
        # High auto-fill ratio (lazy entry)
        if inp.auto_filled_fields_pct >= 70:
            score += 15.0
        elif inp.auto_filled_fields_pct >= 50:
            score += 8.0
        # Missing deal source
        if inp.total_records_evaluated > 0:
            source_gap_ratio = inp.deal_source_missing_count / inp.total_records_evaluated
            if source_gap_ratio >= 0.5:
                score += 10.0
            elif source_gap_ratio >= 0.25:
                score += 5.0
        return _clamp(score)

    def _timeliness_score(self, inp: CRMDataQualityInput) -> float:
        score = 0.0
        # Stale records (not updated in 30+ days)
        if inp.total_records_evaluated > 0:
            stale_ratio = inp.stale_record_count / inp.total_records_evaluated
            if stale_ratio >= 0.5:
                score += 40.0
            elif stale_ratio >= 0.3:
                score += 25.0
            elif stale_ratio >= 0.15:
                score += 12.0
        # Average record staleness
        if inp.avg_record_staleness_days >= 60:
            score += 30.0
        elif inp.avg_record_staleness_days >= 30:
            score += 18.0
        elif inp.avg_record_staleness_days >= 14:
            score += 8.0
        # Low CRM login frequency
        if inp.crm_login_frequency_last_30d <= 3:
            score += 20.0
        elif inp.crm_login_frequency_last_30d <= 8:
            score += 10.0
        return _clamp(score)

    def _activity_coverage_score(self, inp: CRMDataQualityInput) -> float:
        score = 0.0
        # Low activity notes coverage
        if inp.records_with_activity_notes_pct < 40:
            score += 40.0
        elif inp.records_with_activity_notes_pct < 60:
            score += 25.0
        elif inp.records_with_activity_notes_pct < 75:
            score += 12.0
        # Deals in forecast with no recent activity
        if inp.forecast_without_recent_activity_count >= 5:
            score += 30.0
        elif inp.forecast_without_recent_activity_count >= 3:
            score += 18.0
        elif inp.forecast_without_recent_activity_count >= 1:
            score += 8.0
        # Overdue follow-ups
        if inp.overdue_follow_up_count >= 8:
            score += 20.0
        elif inp.overdue_follow_up_count >= 4:
            score += 10.0
        elif inp.overdue_follow_up_count >= 2:
            score += 5.0
        return _clamp(score)

    # ── classification ───────────────────────────────────────────────────────

    def _classify_risk(self, composite: float) -> DataQualityRisk:
        if composite < 20:
            return DataQualityRisk.low
        if composite < 40:
            return DataQualityRisk.moderate
        if composite < 60:
            return DataQualityRisk.high
        return DataQualityRisk.critical

    def _classify_severity(self, composite: float) -> QualitySeverity:
        if composite < 20:
            return QualitySeverity.clean
        if composite < 40:
            return QualitySeverity.degraded
        if composite < 60:
            return QualitySeverity.unreliable
        return QualitySeverity.corrupt

    def _classify_failure_mode(
        self,
        inp: CRMDataQualityInput,
        completeness: float,
        accuracy: float,
        timeliness: float,
        activity: float,
    ) -> QualityFailureMode:
        if inp.duplicate_account_count >= 2:
            return QualityFailureMode.duplicate_accounts
        if inp.data_entry_completeness_pct < 60 or inp.missing_close_date_count >= 5:
            return QualityFailureMode.missing_data
        if inp.avg_record_staleness_days >= 30 or inp.stale_record_count >= 5:
            return QualityFailureMode.stale_records
        if inp.stage_mismatch_count >= 4:
            return QualityFailureMode.stage_drift
        if inp.records_with_activity_notes_pct < 50 or inp.forecast_without_recent_activity_count >= 3:
            return QualityFailureMode.activity_gap
        return QualityFailureMode.none

    def _recommended_action(
        self, risk: DataQualityRisk, composite: float
    ) -> QualityAction:
        if composite >= 60:
            return QualityAction.pipeline_freeze
        if risk == DataQualityRisk.high:
            return QualityAction.data_audit
        if risk == DataQualityRisk.moderate:
            return QualityAction.crm_coaching
        if composite >= 10:
            return QualityAction.self_remediate
        return QualityAction.no_action

    def _signal(
        self,
        mode: QualityFailureMode,
        composite: float,
        inp: CRMDataQualityInput,
    ) -> str:
        if mode == QualityFailureMode.none:
            return "CRM data quality within acceptable parameters"
        msgs = {
            QualityFailureMode.missing_data: (
                f"{inp.missing_close_date_count} records missing close date — "
                f"completeness {inp.data_entry_completeness_pct:.0f}%"
            ),
            QualityFailureMode.stale_records: (
                f"{inp.stale_record_count} stale records — "
                f"avg staleness {inp.avg_record_staleness_days:.0f} days"
            ),
            QualityFailureMode.stage_drift: (
                f"{inp.stage_mismatch_count} stage mismatch(es) — pipeline age vs stage inconsistency"
            ),
            QualityFailureMode.activity_gap: (
                f"{inp.records_with_activity_notes_pct:.0f}% records with notes — "
                f"{inp.forecast_without_recent_activity_count} forecast deals without activity"
            ),
            QualityFailureMode.duplicate_accounts: (
                f"{inp.duplicate_account_count} duplicate account(s) detected"
            ),
        }
        base = msgs.get(mode, f"data quality composite {composite:.0f}")
        return f"{base} — composite {composite:.0f}"

    # ── public API ───────────────────────────────────────────────────────────

    def assess(self, inp: CRMDataQualityInput) -> CRMDataQualityResult:
        completeness = self._completeness_score(inp)
        accuracy     = self._accuracy_score(inp)
        timeliness   = self._timeliness_score(inp)
        activity     = self._activity_coverage_score(inp)

        composite = _clamp(
            completeness * 0.30
            + accuracy   * 0.25
            + timeliness * 0.25
            + activity   * 0.20
        )
        composite = round(composite, 1)

        risk     = self._classify_risk(composite)
        severity = self._classify_severity(composite)
        mode     = self._classify_failure_mode(inp, completeness, accuracy, timeliness, activity)
        action   = self._recommended_action(risk, composite)

        is_data_quality_risk = (
            composite >= 40
            or inp.missing_close_date_count >= 5
            or inp.data_entry_completeness_pct < 50
        )
        requires_data_audit = (
            composite >= 30
            or inp.missing_opportunity_value_count >= 3
            or inp.duplicate_account_count >= 2
        )

        estimated_pipeline_distortion_pct = _clamp(composite * 0.8)

        result = CRMDataQualityResult(
            rep_id=inp.rep_id,
            region=inp.region,
            data_quality_risk=risk,
            quality_failure_mode=mode,
            quality_severity=severity,
            recommended_action=action,
            completeness_score=completeness,
            accuracy_score=accuracy,
            timeliness_score=timeliness,
            activity_coverage_score=activity,
            quality_composite=composite,
            is_data_quality_risk=is_data_quality_risk,
            requires_data_audit=requires_data_audit,
            estimated_pipeline_distortion_pct=estimated_pipeline_distortion_pct,
            quality_signal=self._signal(mode, composite, inp),
        )
        self._results.append(result)
        return result

    def assess_batch(
        self, inputs: list[CRMDataQualityInput]
    ) -> list[CRMDataQualityResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total":                                0,
                "risk_counts":                          {},
                "failure_mode_counts":                  {},
                "severity_counts":                      {},
                "action_counts":                        {},
                "avg_quality_composite":                0.0,
                "data_quality_risk_count":              0,
                "audit_required_count":                 0,
                "avg_completeness_score":               0.0,
                "avg_accuracy_score":                   0.0,
                "avg_timeliness_score":                 0.0,
                "avg_activity_coverage_score":          0.0,
                "avg_estimated_pipeline_distortion_pct": 0.0,
            }

        risk_counts:         dict[str, int] = {}
        failure_mode_counts: dict[str, int] = {}
        severity_counts:     dict[str, int] = {}
        action_counts:       dict[str, int] = {}
        total_comp = total_comp2 = total_acc = total_time = total_act = total_dist = 0.0
        dq_risk = audit = 0

        for r in self._results:
            risk_counts[r.data_quality_risk.value]       = risk_counts.get(r.data_quality_risk.value, 0) + 1
            failure_mode_counts[r.quality_failure_mode.value] = failure_mode_counts.get(r.quality_failure_mode.value, 0) + 1
            severity_counts[r.quality_severity.value]    = severity_counts.get(r.quality_severity.value, 0) + 1
            action_counts[r.recommended_action.value]    = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp  += r.quality_composite
            total_comp2 += r.completeness_score
            total_acc   += r.accuracy_score
            total_time  += r.timeliness_score
            total_act   += r.activity_coverage_score
            total_dist  += r.estimated_pipeline_distortion_pct
            if r.is_data_quality_risk:
                dq_risk += 1
            if r.requires_data_audit:
                audit += 1

        n = len(self._results)
        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "failure_mode_counts":                  failure_mode_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_quality_composite":                round(total_comp  / n, 1),
            "data_quality_risk_count":              dq_risk,
            "audit_required_count":                 audit,
            "avg_completeness_score":               round(total_comp2 / n, 1),
            "avg_accuracy_score":                   round(total_acc   / n, 1),
            "avg_timeliness_score":                 round(total_time  / n, 1),
            "avg_activity_coverage_score":          round(total_act   / n, 1),
            "avg_estimated_pipeline_distortion_pct": round(total_dist / n, 1),
        }
