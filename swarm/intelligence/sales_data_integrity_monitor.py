from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List


class IntegrityRisk(str, Enum):
    CLEAN = "clean"
    MINOR_ISSUES = "minor_issues"
    MODERATE_ISSUES = "moderate_issues"
    CRITICAL_BREACH = "critical_breach"


class AnomalyType(str, Enum):
    INFLATED_DEAL_VALUE = "inflated_deal_value"
    CLOSE_DATE_MANIPULATION = "close_date_manipulation"
    PIPELINE_STUFFING = "pipeline_stuffing"
    GHOST_DEAL = "ghost_deal"
    DUPLICATE_ENTRY = "duplicate_entry"
    MISSING_REQUIRED_FIELDS = "missing_required_fields"


class DataQuality(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


class IntegrityAction(str, Enum):
    NO_ACTION = "no_action"
    FLAG_FOR_REVIEW = "flag_for_review"
    MANAGER_ALERT = "manager_alert"
    COMPLIANCE_ESCALATION = "compliance_escalation"


@dataclass
class SalesDataIntegrityInput:
    record_id: str
    rep_id: str
    deal_count_last_30d: int
    avg_deal_size_usd: float
    historical_avg_deal_size_usd: float
    deals_closed_end_of_quarter_pct: float
    close_date_changes_count: int
    days_close_date_pushed: int
    pipeline_created_last_7d_usd: float
    avg_pipeline_created_per_month_usd: float
    duplicate_contact_count: int
    missing_required_fields_count: int
    deals_no_activity_30d: int
    stage_skips_count: int
    backdated_activities_count: int
    deals_closed_same_day_created_count: int
    crm_login_anomaly_count: int
    data_edit_frequency_score: float
    approval_bypass_count: int
    unverified_opportunity_sources_count: int
    team_benchmark_deviation_pct: float
    manager_review_score: float


@dataclass
class SalesDataIntegrityResult:
    record_id: str
    rep_id: str
    integrity_risk: IntegrityRisk
    anomaly_type: AnomalyType
    data_quality: DataQuality
    integrity_action: IntegrityAction
    pipeline_accuracy_score: float
    data_completeness_score: float
    behavioral_consistency_score: float
    compliance_score: float
    integrity_composite: float
    risk_signal_count: int
    is_clean: bool
    needs_escalation: bool
    primary_integrity_signal: str

    def to_dict(self) -> dict:
        return {
            "record_id": self.record_id,
            "rep_id": self.rep_id,
            "integrity_risk": self.integrity_risk.value,
            "anomaly_type": self.anomaly_type.value,
            "data_quality": self.data_quality.value,
            "integrity_action": self.integrity_action.value,
            "pipeline_accuracy_score": self.pipeline_accuracy_score,
            "data_completeness_score": self.data_completeness_score,
            "behavioral_consistency_score": self.behavioral_consistency_score,
            "compliance_score": self.compliance_score,
            "integrity_composite": self.integrity_composite,
            "risk_signal_count": self.risk_signal_count,
            "is_clean": self.is_clean,
            "needs_escalation": self.needs_escalation,
            "primary_integrity_signal": self.primary_integrity_signal,
        }


def _pipeline_accuracy_score(inp: SalesDataIntegrityInput) -> float:
    score = 100.0
    # Deal size inflation check
    if inp.historical_avg_deal_size_usd > 0:
        size_ratio = inp.avg_deal_size_usd / inp.historical_avg_deal_size_usd
    else:
        size_ratio = 1.0
    if size_ratio > 2.5:
        score -= 40.0
    elif size_ratio > 1.8:
        score -= 25.0
    elif size_ratio > 1.4:
        score -= 12.0
    # Pipeline stuffing (last 7d vs monthly average)
    if inp.avg_pipeline_created_per_month_usd > 0:
        pipeline_ratio = inp.pipeline_created_last_7d_usd / (inp.avg_pipeline_created_per_month_usd / 4)
    else:
        pipeline_ratio = 0.0
    if pipeline_ratio > 5.0:
        score -= 30.0
    elif pipeline_ratio > 3.0:
        score -= 18.0
    elif pipeline_ratio > 2.0:
        score -= 8.0
    # End-of-quarter concentration
    if inp.deals_closed_end_of_quarter_pct > 60:
        score -= 15.0
    elif inp.deals_closed_end_of_quarter_pct > 40:
        score -= 8.0
    # Team benchmark deviation
    if inp.team_benchmark_deviation_pct > 50:
        score -= 15.0
    elif inp.team_benchmark_deviation_pct > 30:
        score -= 8.0
    return max(0.0, min(100.0, round(score, 1)))


def _data_completeness_score(inp: SalesDataIntegrityInput) -> float:
    score = 100.0
    # Missing required fields
    if inp.missing_required_fields_count >= 10:
        score -= 40.0
    elif inp.missing_required_fields_count >= 5:
        score -= 25.0
    elif inp.missing_required_fields_count >= 2:
        score -= 12.0
    # Duplicate contacts
    if inp.duplicate_contact_count >= 10:
        score -= 25.0
    elif inp.duplicate_contact_count >= 5:
        score -= 15.0
    elif inp.duplicate_contact_count >= 2:
        score -= 7.0
    # Unverified sources
    if inp.unverified_opportunity_sources_count >= 5:
        score -= 20.0
    elif inp.unverified_opportunity_sources_count >= 2:
        score -= 10.0
    elif inp.unverified_opportunity_sources_count >= 1:
        score -= 5.0
    # Manager review contribution
    score = score * 0.8 + (inp.manager_review_score / 100.0) * 20.0
    return max(0.0, min(100.0, round(score, 1)))


def _behavioral_consistency_score(inp: SalesDataIntegrityInput) -> float:
    score = 100.0
    # Close date manipulation
    if inp.close_date_changes_count >= 5:
        score -= 30.0
    elif inp.close_date_changes_count >= 3:
        score -= 18.0
    elif inp.close_date_changes_count >= 1:
        score -= 8.0
    # Backdated activities
    if inp.backdated_activities_count >= 5:
        score -= 30.0
    elif inp.backdated_activities_count >= 3:
        score -= 18.0
    elif inp.backdated_activities_count >= 1:
        score -= 8.0
    # Ghost deals (no activity)
    if inp.deals_no_activity_30d >= 5:
        score -= 20.0
    elif inp.deals_no_activity_30d >= 3:
        score -= 12.0
    elif inp.deals_no_activity_30d >= 1:
        score -= 5.0
    # Stage skips
    if inp.stage_skips_count >= 5:
        score -= 20.0
    elif inp.stage_skips_count >= 2:
        score -= 10.0
    # Same-day closed deals
    if inp.deals_closed_same_day_created_count >= 3:
        score -= 15.0
    elif inp.deals_closed_same_day_created_count >= 1:
        score -= 8.0
    return max(0.0, min(100.0, round(score, 1)))


def _compliance_score(inp: SalesDataIntegrityInput) -> float:
    score = 100.0
    # CRM login anomalies (security indicator)
    if inp.crm_login_anomaly_count >= 5:
        score -= 35.0
    elif inp.crm_login_anomaly_count >= 3:
        score -= 22.0
    elif inp.crm_login_anomaly_count >= 1:
        score -= 10.0
    # Approval bypasses
    if inp.approval_bypass_count >= 5:
        score -= 30.0
    elif inp.approval_bypass_count >= 3:
        score -= 18.0
    elif inp.approval_bypass_count >= 1:
        score -= 8.0
    # Data edit frequency (high = potential manipulation)
    if inp.data_edit_frequency_score >= 80:
        score -= 25.0
    elif inp.data_edit_frequency_score >= 60:
        score -= 15.0
    elif inp.data_edit_frequency_score >= 40:
        score -= 8.0
    # Days close date pushed
    if inp.days_close_date_pushed >= 90:
        score -= 15.0
    elif inp.days_close_date_pushed >= 45:
        score -= 8.0
    return max(0.0, min(100.0, round(score, 1)))


def _composite(pipeline: float, completeness: float, behavioral: float,
               compliance: float) -> float:
    raw = pipeline * 0.25 + completeness * 0.25 + behavioral * 0.30 + compliance * 0.20
    return round(raw, 1)


def _count_risk_signals(inp: SalesDataIntegrityInput) -> int:
    signals = 0
    if inp.historical_avg_deal_size_usd > 0 and inp.avg_deal_size_usd / inp.historical_avg_deal_size_usd > 1.8:
        signals += 1
    if inp.backdated_activities_count >= 3:
        signals += 1
    if inp.close_date_changes_count >= 3:
        signals += 1
    if inp.deals_closed_same_day_created_count >= 1:
        signals += 1
    if inp.approval_bypass_count >= 1:
        signals += 1
    if inp.crm_login_anomaly_count >= 3:
        signals += 1
    if inp.deals_no_activity_30d >= 3:
        signals += 1
    if inp.stage_skips_count >= 3:
        signals += 1
    return signals


def _integrity_risk(composite: float, risk_signals: int) -> IntegrityRisk:
    if composite < 40 or risk_signals >= 5:
        return IntegrityRisk.CRITICAL_BREACH
    if composite < 60 or risk_signals >= 3:
        return IntegrityRisk.MODERATE_ISSUES
    if composite < 80 or risk_signals >= 1:
        return IntegrityRisk.MINOR_ISSUES
    return IntegrityRisk.CLEAN


def _anomaly_type(inp: SalesDataIntegrityInput, pipeline: float, behavioral: float) -> AnomalyType:
    if inp.crm_login_anomaly_count >= 3:
        return AnomalyType.DUPLICATE_ENTRY
    if inp.historical_avg_deal_size_usd > 0 and inp.avg_deal_size_usd / inp.historical_avg_deal_size_usd > 2.0:
        return AnomalyType.INFLATED_DEAL_VALUE
    if inp.close_date_changes_count >= 3 or inp.days_close_date_pushed >= 60:
        return AnomalyType.CLOSE_DATE_MANIPULATION
    if pipeline < 50:
        return AnomalyType.PIPELINE_STUFFING
    if inp.deals_no_activity_30d >= 3:
        return AnomalyType.GHOST_DEAL
    if inp.missing_required_fields_count >= 5:
        return AnomalyType.MISSING_REQUIRED_FIELDS
    return AnomalyType.MISSING_REQUIRED_FIELDS


def _data_quality(composite: float) -> DataQuality:
    if composite >= 85:
        return DataQuality.EXCELLENT
    if composite >= 70:
        return DataQuality.GOOD
    if composite >= 50:
        return DataQuality.FAIR
    return DataQuality.POOR


def _integrity_action(risk: IntegrityRisk, risk_signals: int) -> IntegrityAction:
    if risk == IntegrityRisk.CRITICAL_BREACH or risk_signals >= 5:
        return IntegrityAction.COMPLIANCE_ESCALATION
    if risk == IntegrityRisk.MODERATE_ISSUES or risk_signals >= 3:
        return IntegrityAction.MANAGER_ALERT
    if risk == IntegrityRisk.MINOR_ISSUES or risk_signals >= 1:
        return IntegrityAction.FLAG_FOR_REVIEW
    return IntegrityAction.NO_ACTION


def _primary_integrity_signal(inp: SalesDataIntegrityInput, pipeline: float,
                               behavioral: float, compliance: float) -> str:
    if inp.crm_login_anomaly_count >= 3:
        return f"{inp.crm_login_anomaly_count} CRM login anomalies — potential unauthorized access"
    if inp.approval_bypass_count >= 3:
        return f"{inp.approval_bypass_count} approval bypasses — compliance risk"
    if inp.backdated_activities_count >= 3:
        return f"{inp.backdated_activities_count} backdated activities — data integrity concern"
    if inp.deals_closed_same_day_created_count >= 2:
        return f"{inp.deals_closed_same_day_created_count} deals closed same day as created — ghost deal risk"
    if inp.historical_avg_deal_size_usd > 0 and inp.avg_deal_size_usd / inp.historical_avg_deal_size_usd > 1.8:
        return "deal size 80%+ above historical average — potential inflation"
    if inp.close_date_changes_count >= 3:
        return f"close date changed {inp.close_date_changes_count}x — forecast manipulation risk"
    if inp.deals_no_activity_30d >= 3:
        return f"{inp.deals_no_activity_30d} ghost deals with no activity in 30 days"
    return "data integrity within acceptable parameters"


class SalesDataIntegrityMonitor:
    def __init__(self) -> None:
        self._results: dict[str, SalesDataIntegrityResult] = {}

    def assess(self, inp: SalesDataIntegrityInput) -> SalesDataIntegrityResult:
        pipeline = _pipeline_accuracy_score(inp)
        completeness = _data_completeness_score(inp)
        behavioral = _behavioral_consistency_score(inp)
        compliance = _compliance_score(inp)
        composite = _composite(pipeline, completeness, behavioral, compliance)
        risk_signals = _count_risk_signals(inp)

        risk = _integrity_risk(composite, risk_signals)
        anomaly = _anomaly_type(inp, pipeline, behavioral)
        quality = _data_quality(composite)
        action = _integrity_action(risk, risk_signals)
        signal = _primary_integrity_signal(inp, pipeline, behavioral, compliance)

        is_clean = composite >= 80 and risk_signals == 0
        needs_escalation = risk == IntegrityRisk.CRITICAL_BREACH or risk_signals >= 5

        result = SalesDataIntegrityResult(
            record_id=inp.record_id,
            rep_id=inp.rep_id,
            integrity_risk=risk,
            anomaly_type=anomaly,
            data_quality=quality,
            integrity_action=action,
            pipeline_accuracy_score=pipeline,
            data_completeness_score=completeness,
            behavioral_consistency_score=behavioral,
            compliance_score=compliance,
            integrity_composite=composite,
            risk_signal_count=risk_signals,
            is_clean=is_clean,
            needs_escalation=needs_escalation,
            primary_integrity_signal=signal,
        )
        self._results[inp.record_id] = result
        return result

    def assess_batch(self, inputs: List[SalesDataIntegrityInput]) -> List[SalesDataIntegrityResult]:
        results = [self.assess(inp) for inp in inputs]
        results.sort(key=lambda r: r.integrity_composite)
        return results

    def get(self, record_id: str) -> SalesDataIntegrityResult | None:
        return self._results.get(record_id)

    def all_records(self) -> List[SalesDataIntegrityResult]:
        return sorted(self._results.values(), key=lambda r: r.integrity_composite)

    def clean_records(self) -> List[SalesDataIntegrityResult]:
        return [r for r in self._results.values() if r.is_clean]

    def escalation_queue(self) -> List[SalesDataIntegrityResult]:
        return [r for r in self._results.values() if r.needs_escalation]

    def by_risk(self, risk: IntegrityRisk) -> List[SalesDataIntegrityResult]:
        return [r for r in self._results.values() if r.integrity_risk == risk]

    def by_anomaly(self, anomaly: AnomalyType) -> List[SalesDataIntegrityResult]:
        return [r for r in self._results.values() if r.anomaly_type == anomaly]

    def avg_integrity_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.integrity_composite for r in self._results.values()) / len(self._results), 1)

    def reset(self) -> None:
        self._results.clear()

    def summary(self) -> dict:
        results = list(self._results.values())
        n = len(results)
        risk_counts: dict[str, int] = {}
        anomaly_counts: dict[str, int] = {}
        quality_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        for r in results:
            risk_counts[r.integrity_risk.value] = risk_counts.get(r.integrity_risk.value, 0) + 1
            anomaly_counts[r.anomaly_type.value] = anomaly_counts.get(r.anomaly_type.value, 0) + 1
            quality_counts[r.data_quality.value] = quality_counts.get(r.data_quality.value, 0) + 1
            action_counts[r.integrity_action.value] = action_counts.get(r.integrity_action.value, 0) + 1
        return {
            "total": n,
            "risk_counts": risk_counts,
            "anomaly_counts": anomaly_counts,
            "quality_counts": quality_counts,
            "action_counts": action_counts,
            "avg_integrity_composite": self.avg_integrity_composite(),
            "clean_count": len(self.clean_records()),
            "escalation_count": len(self.escalation_queue()),
            "avg_pipeline_accuracy_score": round(sum(r.pipeline_accuracy_score for r in results) / n, 1) if n else 0.0,
            "avg_data_completeness_score": round(sum(r.data_completeness_score for r in results) / n, 1) if n else 0.0,
            "avg_behavioral_consistency_score": round(sum(r.behavioral_consistency_score for r in results) / n, 1) if n else 0.0,
            "avg_compliance_score": round(sum(r.compliance_score for r in results) / n, 1) if n else 0.0,
            "high_risk_rep_count": sum(1 for r in results if r.integrity_risk == IntegrityRisk.CRITICAL_BREACH),
        }
