"""Certification & Industry Standards Tracker Engine — monitors cert expiry, compliance gaps, and audit readiness."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CertRisk(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class CertPattern(str, Enum):
    NONE = "none"
    CERTIFICATION_EXPIRY = "certification_expiry"
    STANDARD_OBSOLESCENCE = "standard_obsolescence"
    COMPLIANCE_GAP = "compliance_gap"
    AUDIT_FAILURE = "audit_failure"
    NEW_REQUIREMENT = "new_requirement"


class CertSeverity(str, Enum):
    CURRENT = "current"
    DUE_SOON = "due_soon"
    OVERDUE = "overdue"
    EXPIRED = "expired"


class CertAction(str, Enum):
    NO_ACTION = "no_action"
    CERT_MONITORING = "cert_monitoring"
    RENEWAL_SCHEDULING = "renewal_scheduling"
    STANDARD_UPDATE = "standard_update"
    GAP_REMEDIATION = "gap_remediation"
    AUDIT_PREPARATION = "audit_preparation"
    EMERGENCY_RECERTIFICATION = "emergency_recertification"
    REGULATORY_SUBMISSION = "regulatory_submission"
    BOARD_COMPLIANCE_REVIEW = "board_compliance_review"


@dataclass
class CertInput:
    cert_id: str
    standard_body: str
    region: str
    days_to_expiry: int
    certification_coverage_pct: float          # 0-1
    standard_version_lag_months: float
    new_requirements_count: int
    gap_assessment_score: float                 # 0-1, 1=large gap
    audit_readiness_score: float                # 0-1, 1=ready
    last_audit_finding_count: int
    regulatory_change_frequency_pct: float      # 0-1
    industry_peer_compliance_pct: float         # 0-1
    internal_process_maturity: float            # 0-1, 1=mature
    documentation_completeness_pct: float       # 0-1
    training_alignment_score: float             # 0-1
    mandatory_cert_count: int
    voluntary_cert_count: int
    cert_renewal_cost_index: float              # 0-10
    compliance_officer_tenure_months: int
    prior_non_compliance_count: int


@dataclass
class CertResult:
    cert_id: str
    region: str
    cert_risk: CertRisk
    cert_pattern: CertPattern
    cert_severity: CertSeverity
    recommended_action: CertAction
    expiry_score: float
    gap_score: float
    audit_score: float
    compliance_score: float
    cert_composite: float
    has_cert_risk: bool
    requires_immediate_action: bool
    estimated_compliance_gap_index: float       # 0-10
    cert_signal: str

    def to_dict(self) -> dict:
        return {
            "cert_id": self.cert_id,
            "region": self.region,
            "cert_risk": self.cert_risk.value,
            "cert_pattern": self.cert_pattern.value,
            "cert_severity": self.cert_severity.value,
            "recommended_action": self.recommended_action.value,
            "expiry_score": self.expiry_score,
            "gap_score": self.gap_score,
            "audit_score": self.audit_score,
            "compliance_score": self.compliance_score,
            "cert_composite": self.cert_composite,
            "has_cert_risk": self.has_cert_risk,
            "requires_immediate_action": self.requires_immediate_action,
            "estimated_compliance_gap_index": self.estimated_compliance_gap_index,
            "cert_signal": self.cert_signal,
        }


# ── sub-score calculators ─────────────────────────────────────────────────────

def _expiry_score(inp: CertInput) -> float:
    score = 0.0
    # days_to_expiry
    if inp.days_to_expiry <= 30:
        score += 40
    elif inp.days_to_expiry <= 90:
        score += 22
    elif inp.days_to_expiry <= 180:
        score += 8
    # certification_coverage_pct
    if inp.certification_coverage_pct <= 0.60:
        score += 35
    elif inp.certification_coverage_pct <= 0.75:
        score += 18
    elif inp.certification_coverage_pct <= 0.88:
        score += 6
    # new_requirements_count
    if inp.new_requirements_count >= 5:
        score += 25
    elif inp.new_requirements_count >= 2:
        score += 12
    return round(min(score, 100.0), 2)


def _gap_score(inp: CertInput) -> float:
    score = 0.0
    # gap_assessment_score
    if inp.gap_assessment_score >= 0.65:
        score += 40
    elif inp.gap_assessment_score >= 0.45:
        score += 22
    elif inp.gap_assessment_score >= 0.25:
        score += 8
    # standard_version_lag_months
    if inp.standard_version_lag_months >= 18:
        score += 35
    elif inp.standard_version_lag_months >= 9:
        score += 18
    elif inp.standard_version_lag_months >= 3:
        score += 6
    # documentation_completeness_pct
    if inp.documentation_completeness_pct <= 0.60:
        score += 25
    elif inp.documentation_completeness_pct <= 0.78:
        score += 12
    return round(min(score, 100.0), 2)


def _audit_score(inp: CertInput) -> float:
    score = 0.0
    # audit_readiness_score
    if inp.audit_readiness_score <= 0.40:
        score += 45
    elif inp.audit_readiness_score <= 0.60:
        score += 25
    elif inp.audit_readiness_score <= 0.75:
        score += 10
    # last_audit_finding_count
    if inp.last_audit_finding_count >= 5:
        score += 30
    elif inp.last_audit_finding_count >= 2:
        score += 15
    # prior_non_compliance_count
    if inp.prior_non_compliance_count >= 3:
        score += 25
    elif inp.prior_non_compliance_count >= 1:
        score += 12
    return round(min(score, 100.0), 2)


def _compliance_score(inp: CertInput) -> float:
    score = 0.0
    # regulatory_change_frequency_pct
    if inp.regulatory_change_frequency_pct >= 0.40:
        score += 40
    elif inp.regulatory_change_frequency_pct >= 0.25:
        score += 22
    elif inp.regulatory_change_frequency_pct >= 0.10:
        score += 8
    # industry_peer_compliance_pct
    if inp.industry_peer_compliance_pct <= 0.70:
        score += 35
    elif inp.industry_peer_compliance_pct <= 0.85:
        score += 18
    # internal_process_maturity
    if inp.internal_process_maturity <= 0.45:
        score += 25
    elif inp.internal_process_maturity <= 0.65:
        score += 12
    return round(min(score, 100.0), 2)


def _composite(exp: float, gap: float, audit: float, comp: float) -> float:
    return round(exp * 0.30 + gap * 0.25 + audit * 0.25 + comp * 0.20, 2)


def _risk(composite: float) -> CertRisk:
    if composite >= 60:
        return CertRisk.CRITICAL
    if composite >= 40:
        return CertRisk.HIGH
    if composite >= 20:
        return CertRisk.MODERATE
    return CertRisk.LOW


def _severity(composite: float) -> CertSeverity:
    if composite >= 60:
        return CertSeverity.EXPIRED
    if composite >= 40:
        return CertSeverity.OVERDUE
    if composite >= 20:
        return CertSeverity.DUE_SOON
    return CertSeverity.CURRENT


def _pattern(inp: CertInput) -> CertPattern:
    if inp.days_to_expiry <= 60 and inp.certification_coverage_pct <= 0.75:
        return CertPattern.CERTIFICATION_EXPIRY
    if inp.standard_version_lag_months >= 15 and inp.new_requirements_count >= 3:
        return CertPattern.STANDARD_OBSOLESCENCE
    if inp.gap_assessment_score >= 0.55 and inp.documentation_completeness_pct <= 0.65:
        return CertPattern.COMPLIANCE_GAP
    if inp.audit_readiness_score <= 0.45 and inp.last_audit_finding_count >= 3:
        return CertPattern.AUDIT_FAILURE
    if inp.new_requirements_count >= 4 and inp.regulatory_change_frequency_pct >= 0.30:
        return CertPattern.NEW_REQUIREMENT
    return CertPattern.NONE


def _action(risk: CertRisk, pattern: CertPattern) -> CertAction:
    if risk == CertRisk.CRITICAL:
        if pattern in (CertPattern.CERTIFICATION_EXPIRY, CertPattern.AUDIT_FAILURE):
            return CertAction.EMERGENCY_RECERTIFICATION
        return CertAction.BOARD_COMPLIANCE_REVIEW
    if risk == CertRisk.HIGH:
        if pattern == CertPattern.CERTIFICATION_EXPIRY:
            return CertAction.RENEWAL_SCHEDULING
        if pattern == CertPattern.STANDARD_OBSOLESCENCE:
            return CertAction.STANDARD_UPDATE
        if pattern == CertPattern.COMPLIANCE_GAP:
            return CertAction.GAP_REMEDIATION
        if pattern == CertPattern.AUDIT_FAILURE:
            return CertAction.AUDIT_PREPARATION
        if pattern == CertPattern.NEW_REQUIREMENT:
            return CertAction.REGULATORY_SUBMISSION
        return CertAction.CERT_MONITORING
    if risk == CertRisk.MODERATE:
        return CertAction.RENEWAL_SCHEDULING
    return CertAction.NO_ACTION


def _signal(inp: CertInput, comp: float, risk: CertRisk) -> str:
    if comp < 20:
        return "Certification posture current — all standards up-to-date and audit-ready"
    label = risk.value.replace("_", " ").title()
    return (
        f"{label} — {inp.days_to_expiry}d to expiry"
        f" — gap {round(inp.gap_assessment_score * 100)}%"
        f" — {inp.last_audit_finding_count} audit findings"
        f" — composite {round(comp)}"
    )


class CertificationStandardsTrackerEngine:
    """Monitors certification expiry, compliance gaps, and audit readiness across the organisation."""

    def __init__(self) -> None:
        self._results: list[CertResult] = []

    def analyze(self, inp: CertInput) -> CertResult:
        exp_s = _expiry_score(inp)
        gap_s = _gap_score(inp)
        aud_s = _audit_score(inp)
        cmp_s = _compliance_score(inp)
        cert_comp = _composite(exp_s, gap_s, aud_s, cmp_s)

        risk = _risk(cert_comp)
        severity = _severity(cert_comp)
        pattern = _pattern(inp)
        action = _action(risk, pattern)

        has_risk = cert_comp >= 40 or inp.days_to_expiry <= 90 or inp.gap_assessment_score >= 0.40
        requires_immediate = cert_comp >= 25 or inp.days_to_expiry <= 30 or inp.last_audit_finding_count >= 3
        gap_index = round(min(cert_comp / 100 * inp.gap_assessment_score * 10, 10.0), 2)
        sig = _signal(inp, cert_comp, risk)

        result = CertResult(
            cert_id=inp.cert_id,
            region=inp.region,
            cert_risk=risk,
            cert_pattern=pattern,
            cert_severity=severity,
            recommended_action=action,
            expiry_score=exp_s,
            gap_score=gap_s,
            audit_score=aud_s,
            compliance_score=cmp_s,
            cert_composite=cert_comp,
            has_cert_risk=has_risk,
            requires_immediate_action=requires_immediate,
            estimated_compliance_gap_index=gap_index,
            cert_signal=sig,
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[CertInput]) -> list[CertResult]:
        for inp in inputs:
            self.analyze(inp)
        self._results.sort(key=lambda r: r.cert_composite, reverse=True)
        return self._results

    def reset(self) -> None:
        self._results.clear()

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_cert_composite": 0.0,
                "cert_risk_count": 0,
                "immediate_action_count": 0,
                "avg_expiry_score": 0.0,
                "avg_gap_score": 0.0,
                "avg_audit_score": 0.0,
                "avg_compliance_score": 0.0,
                "avg_estimated_compliance_gap_index": 0.0,
            }
        risk_counts: dict[str, int] = {}
        pattern_counts: dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        total_comp = total_exp = total_gap = total_aud = total_cmp = total_idx = 0.0
        for r in self._results:
            risk_counts[r.cert_risk.value] = risk_counts.get(r.cert_risk.value, 0) + 1
            pattern_counts[r.cert_pattern.value] = pattern_counts.get(r.cert_pattern.value, 0) + 1
            severity_counts[r.cert_severity.value] = severity_counts.get(r.cert_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.cert_composite
            total_exp += r.expiry_score
            total_gap += r.gap_score
            total_aud += r.audit_score
            total_cmp += r.compliance_score
            total_idx += r.estimated_compliance_gap_index
        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_cert_composite": round(total_comp / n, 2),
            "cert_risk_count": sum(1 for r in self._results if r.has_cert_risk),
            "immediate_action_count": sum(1 for r in self._results if r.requires_immediate_action),
            "avg_expiry_score": round(total_exp / n, 2),
            "avg_gap_score": round(total_gap / n, 2),
            "avg_audit_score": round(total_aud / n, 2),
            "avg_compliance_score": round(total_cmp / n, 2),
            "avg_estimated_compliance_gap_index": round(total_idx / n, 2),
        }
