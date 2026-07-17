from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List


class AnomalyLevel(str, Enum):
    NONE = "none"
    LOW = "low"
    ELEVATED = "elevated"
    HIGH = "high"
    CRITICAL = "critical"


class AnomalyRisk(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class AnomalyType(str, Enum):
    NONE = "none"
    BULK_EXPORT = "bulk_export"
    OFF_HOURS = "off_hours"
    CREDENTIAL_SHARING = "credential_sharing"
    DATA_EXFILTRATION = "data_exfiltration"
    PRIVILEGE_ABUSE = "privilege_abuse"


class AnomalyAction(str, Enum):
    NO_ACTION = "no_action"
    LOG_ALERT = "log_alert"
    SECURITY_REVIEW = "security_review"
    ACCOUNT_SUSPEND = "account_suspend"
    IMMEDIATE_LOCKDOWN = "immediate_lockdown"


@dataclass
class SalesDataAccessInput:
    user_id: str
    user_name: str
    role: str
    region: str
    records_accessed_count: int
    records_accessed_prior_avg: float
    download_volume_mb: float
    download_prior_avg_mb: float
    off_hours_access_pct: float
    bulk_export_count: int
    sensitive_field_access_count: int
    failed_auth_attempts: int
    vpn_connected: int
    shared_account_flag: int
    unusual_ip_count: int
    data_sensitivity_avg_score: float
    export_to_personal_email_count: int
    concurrent_session_count: int
    access_outside_territory_pct: float
    privileged_data_access_count: int
    anomaly_score_external: float
    account_type: str


@dataclass
class SalesDataAccessResult:
    user_id: str
    user_name: str
    anomaly_level: AnomalyLevel
    anomaly_risk: AnomalyRisk
    primary_anomaly_type: AnomalyType
    recommended_action: AnomalyAction
    access_volume_score: float
    behavioral_deviation_score: float
    data_sensitivity_score: float
    authentication_risk_score: float
    anomaly_composite: float
    is_active_threat: bool
    requires_immediate_action: bool
    estimated_data_exposure_mb: float
    anomaly_signal: str

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "anomaly_level": self.anomaly_level.value,
            "anomaly_risk": self.anomaly_risk.value,
            "primary_anomaly_type": self.primary_anomaly_type.value,
            "recommended_action": self.recommended_action.value,
            "access_volume_score": self.access_volume_score,
            "behavioral_deviation_score": self.behavioral_deviation_score,
            "data_sensitivity_score": self.data_sensitivity_score,
            "authentication_risk_score": self.authentication_risk_score,
            "anomaly_composite": self.anomaly_composite,
            "is_active_threat": self.is_active_threat,
            "requires_immediate_action": self.requires_immediate_action,
            "estimated_data_exposure_mb": self.estimated_data_exposure_mb,
            "anomaly_signal": self.anomaly_signal,
        }


def _access_volume_score(inp: SalesDataAccessInput) -> float:
    # HIGHER = more anomalous
    score = 0.0
    # Records accessed vs baseline (0-40)
    if inp.records_accessed_prior_avg > 0:
        ratio = inp.records_accessed_count / inp.records_accessed_prior_avg
    else:
        ratio = 1.0 if inp.records_accessed_count == 0 else 5.0
    if ratio >= 5.0:
        score += 40.0
    elif ratio >= 3.0:
        score += 28.0
    elif ratio >= 2.0:
        score += 16.0
    elif ratio >= 1.5:
        score += 8.0
    # Download volume vs baseline (0-35)
    if inp.download_prior_avg_mb > 0:
        dl_ratio = inp.download_volume_mb / inp.download_prior_avg_mb
    else:
        dl_ratio = 1.0 if inp.download_volume_mb == 0 else 5.0
    if dl_ratio >= 5.0:
        score += 35.0
    elif dl_ratio >= 3.0:
        score += 24.0
    elif dl_ratio >= 2.0:
        score += 12.0
    elif dl_ratio >= 1.5:
        score += 6.0
    # Bulk exports (0-25)
    if inp.bulk_export_count >= 5:
        score += 25.0
    elif inp.bulk_export_count >= 3:
        score += 17.0
    elif inp.bulk_export_count >= 1:
        score += 8.0
    return max(0.0, min(100.0, round(score, 1)))


def _behavioral_deviation_score(inp: SalesDataAccessInput) -> float:
    # HIGHER = more anomalous
    score = 0.0
    # Off-hours access (0-30)
    if inp.off_hours_access_pct >= 60:
        score += 30.0
    elif inp.off_hours_access_pct >= 40:
        score += 20.0
    elif inp.off_hours_access_pct >= 20:
        score += 10.0
    elif inp.off_hours_access_pct >= 10:
        score += 4.0
    # Access outside territory (0-25)
    if inp.access_outside_territory_pct >= 50:
        score += 25.0
    elif inp.access_outside_territory_pct >= 30:
        score += 16.0
    elif inp.access_outside_territory_pct >= 15:
        score += 8.0
    # Concurrent sessions (0-25)
    if inp.concurrent_session_count >= 4:
        score += 25.0
    elif inp.concurrent_session_count >= 3:
        score += 16.0
    elif inp.concurrent_session_count == 2:
        score += 8.0
    # Export to personal email (0-20)
    if inp.export_to_personal_email_count >= 3:
        score += 20.0
    elif inp.export_to_personal_email_count >= 1:
        score += 12.0
    return max(0.0, min(100.0, round(score, 1)))


def _data_sensitivity_score(inp: SalesDataAccessInput) -> float:
    # HIGHER = greater sensitivity risk
    score = 0.0
    # Sensitive field access (0-35)
    if inp.sensitive_field_access_count >= 50:
        score += 35.0
    elif inp.sensitive_field_access_count >= 25:
        score += 24.0
    elif inp.sensitive_field_access_count >= 10:
        score += 12.0
    elif inp.sensitive_field_access_count >= 5:
        score += 5.0
    # Data sensitivity level (0-35)
    score += inp.data_sensitivity_avg_score * 0.35
    # Privileged data access (0-20)
    if inp.privileged_data_access_count >= 10:
        score += 20.0
    elif inp.privileged_data_access_count >= 5:
        score += 13.0
    elif inp.privileged_data_access_count >= 1:
        score += 6.0
    # Unusual IP origins (0-10)
    if inp.unusual_ip_count >= 3:
        score += 10.0
    elif inp.unusual_ip_count >= 1:
        score += 5.0
    return max(0.0, min(100.0, round(score, 1)))


def _authentication_risk_score(inp: SalesDataAccessInput) -> float:
    # HIGHER = more authentication risk
    score = 0.0
    # Shared account flag (0-40): immediate red flag
    if inp.shared_account_flag:
        score += 40.0
    # Failed auth attempts (0-30)
    if inp.failed_auth_attempts >= 10:
        score += 30.0
    elif inp.failed_auth_attempts >= 5:
        score += 20.0
    elif inp.failed_auth_attempts >= 3:
        score += 10.0
    elif inp.failed_auth_attempts >= 1:
        score += 4.0
    # Unusual IPs (0-20)
    if inp.unusual_ip_count >= 5:
        score += 20.0
    elif inp.unusual_ip_count >= 3:
        score += 13.0
    elif inp.unusual_ip_count >= 1:
        score += 6.0
    # No VPN when accessing sensitive data (0-10)
    if not inp.vpn_connected and inp.data_sensitivity_avg_score >= 60:
        score += 10.0
    # External anomaly score contribution (0-0 extra) — already integrated
    score += inp.anomaly_score_external * 0.10
    return max(0.0, min(100.0, round(score, 1)))


def _anomaly_composite(access: float, behavioral: float, sensitivity: float, auth: float) -> float:
    raw = access * 0.30 + behavioral * 0.25 + sensitivity * 0.25 + auth * 0.20
    return round(raw, 1)


def _anomaly_level(composite: float) -> AnomalyLevel:
    if composite < 10:
        return AnomalyLevel.NONE
    if composite < 25:
        return AnomalyLevel.LOW
    if composite < 45:
        return AnomalyLevel.ELEVATED
    if composite < 65:
        return AnomalyLevel.HIGH
    return AnomalyLevel.CRITICAL


def _anomaly_risk(composite: float) -> AnomalyRisk:
    if composite < 15:
        return AnomalyRisk.LOW
    if composite < 35:
        return AnomalyRisk.MODERATE
    if composite < 55:
        return AnomalyRisk.HIGH
    return AnomalyRisk.CRITICAL


def _primary_type(inp: SalesDataAccessInput, access: float, behavioral: float,
                  sensitivity: float, auth: float) -> AnomalyType:
    worst = max(access, behavioral, sensitivity, auth)
    if worst < 25:
        return AnomalyType.NONE
    # Hard rules first
    if inp.export_to_personal_email_count >= 1 or (inp.bulk_export_count >= 3 and inp.download_volume_mb > inp.download_prior_avg_mb * 3):
        return AnomalyType.DATA_EXFILTRATION
    if inp.shared_account_flag or inp.concurrent_session_count >= 3:
        return AnomalyType.CREDENTIAL_SHARING
    if inp.privileged_data_access_count >= 10 and sensitivity >= 50:
        return AnomalyType.PRIVILEGE_ABUSE
    if access >= behavioral and access >= sensitivity and access >= auth and inp.bulk_export_count >= 1:
        return AnomalyType.BULK_EXPORT
    if behavioral >= sensitivity and behavioral >= auth and inp.off_hours_access_pct >= 40:
        return AnomalyType.OFF_HOURS
    # Fallback: highest dimension
    dim_map = {
        AnomalyType.BULK_EXPORT: access,
        AnomalyType.OFF_HOURS: behavioral,
        AnomalyType.DATA_EXFILTRATION: sensitivity,
        AnomalyType.CREDENTIAL_SHARING: auth,
    }
    return max(dim_map, key=lambda k: dim_map[k])


def _recommended_action(level: AnomalyLevel, inp: SalesDataAccessInput) -> AnomalyAction:
    if level == AnomalyLevel.CRITICAL:
        return AnomalyAction.IMMEDIATE_LOCKDOWN
    if level == AnomalyLevel.HIGH:
        return AnomalyAction.ACCOUNT_SUSPEND if inp.export_to_personal_email_count >= 1 else AnomalyAction.SECURITY_REVIEW
    if level == AnomalyLevel.ELEVATED:
        return AnomalyAction.SECURITY_REVIEW
    if level == AnomalyLevel.LOW:
        return AnomalyAction.LOG_ALERT
    return AnomalyAction.NO_ACTION


def _data_exposure_mb(inp: SalesDataAccessInput, composite: float) -> float:
    exposure = inp.download_volume_mb * (composite / 100.0)
    return round(exposure, 2)


def _anomaly_signal(inp: SalesDataAccessInput, atype: AnomalyType, composite: float) -> str:
    if atype == AnomalyType.DATA_EXFILTRATION:
        return f"data exfiltration alert — {inp.export_to_personal_email_count} exports to personal email, {inp.download_volume_mb:.0f}MB downloaded"
    if atype == AnomalyType.CREDENTIAL_SHARING:
        return f"credential sharing detected — {inp.concurrent_session_count} concurrent sessions, shared account flag: {bool(inp.shared_account_flag)}"
    if atype == AnomalyType.PRIVILEGE_ABUSE:
        return f"privilege abuse — {inp.privileged_data_access_count} privileged record accesses, sensitivity score {inp.data_sensitivity_avg_score:.0f}"
    if atype == AnomalyType.BULK_EXPORT:
        return f"bulk export anomaly — {inp.bulk_export_count} bulk exports, {inp.download_volume_mb:.0f}MB vs {inp.download_prior_avg_mb:.0f}MB baseline"
    if atype == AnomalyType.OFF_HOURS:
        return f"off-hours access pattern — {inp.off_hours_access_pct:.0f}% of accesses outside business hours"
    if composite < 10:
        return "normal access patterns — no anomalies detected"
    return f"low-level anomaly indicators — composite score {composite:.0f}, monitoring recommended"


class SalesDataAccessAnomalyEngine:
    def __init__(self) -> None:
        self._results: dict[str, SalesDataAccessResult] = {}

    def assess(self, inp: SalesDataAccessInput) -> SalesDataAccessResult:
        access = _access_volume_score(inp)
        behavioral = _behavioral_deviation_score(inp)
        sensitivity = _data_sensitivity_score(inp)
        auth = _authentication_risk_score(inp)
        composite = _anomaly_composite(access, behavioral, sensitivity, auth)

        level = _anomaly_level(composite)
        risk = _anomaly_risk(composite)
        atype = _primary_type(inp, access, behavioral, sensitivity, auth)
        action = _recommended_action(level, inp)
        is_threat = composite >= 45 or inp.export_to_personal_email_count >= 2 or inp.shared_account_flag == 1
        requires_immediate = composite >= 65 or inp.export_to_personal_email_count >= 3 or (inp.shared_account_flag == 1 and composite >= 40)
        exposure = _data_exposure_mb(inp, composite)
        signal = _anomaly_signal(inp, atype, composite)

        result = SalesDataAccessResult(
            user_id=inp.user_id,
            user_name=inp.user_name,
            anomaly_level=level,
            anomaly_risk=risk,
            primary_anomaly_type=atype,
            recommended_action=action,
            access_volume_score=access,
            behavioral_deviation_score=behavioral,
            data_sensitivity_score=sensitivity,
            authentication_risk_score=auth,
            anomaly_composite=composite,
            is_active_threat=is_threat,
            requires_immediate_action=requires_immediate,
            estimated_data_exposure_mb=exposure,
            anomaly_signal=signal,
        )
        self._results[inp.user_id] = result
        return result

    def assess_batch(self, inputs: List[SalesDataAccessInput]) -> List[SalesDataAccessResult]:
        results = [self.assess(inp) for inp in inputs]
        results.sort(key=lambda r: r.anomaly_composite, reverse=True)
        return results

    def get(self, user_id: str) -> SalesDataAccessResult | None:
        return self._results.get(user_id)

    def all_users(self) -> List[SalesDataAccessResult]:
        return sorted(self._results.values(), key=lambda r: r.anomaly_composite, reverse=True)

    def active_threats(self) -> List[SalesDataAccessResult]:
        return [r for r in self._results.values() if r.is_active_threat]

    def by_level(self, level: AnomalyLevel) -> List[SalesDataAccessResult]:
        return [r for r in self._results.values() if r.anomaly_level == level]

    def by_risk(self, risk: AnomalyRisk) -> List[SalesDataAccessResult]:
        return [r for r in self._results.values() if r.anomaly_risk == risk]

    def total_data_exposure_mb(self) -> float:
        return round(sum(r.estimated_data_exposure_mb for r in self._results.values()), 2)

    def avg_anomaly_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.anomaly_composite for r in self._results.values()) / len(self._results), 1)

    def reset(self) -> None:
        self._results.clear()

    def summary(self) -> dict:
        results = list(self._results.values())
        n = len(results)
        level_counts: dict[str, int] = {}
        risk_counts: dict[str, int] = {}
        type_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        for r in results:
            level_counts[r.anomaly_level.value] = level_counts.get(r.anomaly_level.value, 0) + 1
            risk_counts[r.anomaly_risk.value] = risk_counts.get(r.anomaly_risk.value, 0) + 1
            type_counts[r.primary_anomaly_type.value] = type_counts.get(r.primary_anomaly_type.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
        return {
            "total": n,
            "level_counts": level_counts,
            "risk_counts": risk_counts,
            "type_counts": type_counts,
            "action_counts": action_counts,
            "avg_anomaly_composite": self.avg_anomaly_composite(),
            "active_threat_count": len(self.active_threats()),
            "immediate_action_count": sum(1 for r in results if r.requires_immediate_action),
            "avg_access_volume_score": round(sum(r.access_volume_score for r in results) / n, 1) if n else 0.0,
            "avg_behavioral_deviation_score": round(sum(r.behavioral_deviation_score for r in results) / n, 1) if n else 0.0,
            "avg_data_sensitivity_score": round(sum(r.data_sensitivity_score for r in results) / n, 1) if n else 0.0,
            "avg_authentication_risk_score": round(sum(r.authentication_risk_score for r in results) / n, 1) if n else 0.0,
            "total_data_exposure_mb": self.total_data_exposure_mb(),
        }
