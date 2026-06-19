"""
Module 227 — Swarm Security Shield Engine
Silent guardian that audits all swarm agents for data exposure risks,
access anomalies, credential leaks, injection patterns and compliance
gaps — without disrupting normal agent operations.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class SecurityRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ThreatPattern(str, Enum):
    none                  = "none"
    credential_exposure   = "credential_exposure"
    injection_attempt     = "injection_attempt"
    data_exfiltration     = "data_exfiltration"
    access_anomaly        = "access_anomaly"
    compliance_violation  = "compliance_violation"


class SecuritySeverity(str, Enum):
    secure     = "secure"
    monitoring = "monitoring"
    threatened = "threatened"
    breached   = "breached"


class SecurityAction(str, Enum):
    no_action                = "no_action"
    security_monitoring      = "security_monitoring"
    access_review            = "access_review"
    credential_rotation      = "credential_rotation"
    injection_block          = "injection_block"
    data_quarantine          = "data_quarantine"
    compliance_audit         = "compliance_audit"
    incident_containment     = "incident_containment"
    emergency_lockdown       = "emergency_lockdown"


@dataclass
class SecurityInput:
    agent_id: str
    agent_type: str
    region: str
    # Credential & secrets signals
    hardcoded_secret_detected: float      # 0-1 (1 = secrets found in code/logs)
    env_var_exposure_risk: float          # 0-1 (env vars accessible in logs)
    api_key_rotation_days_overdue: int    # days since last key rotation
    credential_in_plaintext_count: int   # credentials found in plaintext
    # Access & auth signals
    unauthorized_access_attempts: int    # failed auth attempts in 24h
    privilege_escalation_attempts: int   # attempts to elevate permissions
    anomalous_access_pattern_score: float # 0-1 (unusual access timing/volume)
    inactive_user_access_count: int      # inactive users still accessing
    # Injection & input signals
    prompt_injection_attempts: int       # detected prompt injection attempts
    sql_injection_attempts: int          # SQL injection patterns detected
    xss_attempt_count: int               # cross-site scripting attempts
    input_validation_failure_rate: float  # 0-1, % inputs failing validation
    # Data protection signals
    pii_exposure_risk_score: float       # 0-1 (PII in logs/outputs)
    data_encryption_compliance_pct: float # 0-1, % data properly encrypted
    gdpr_compliance_score: float         # 0-1 (1 = fully compliant)
    data_retention_violation_count: int  # retention policy violations
    # Audit & monitoring
    audit_log_completeness_pct: float    # 0-1, % actions logged
    security_scan_days_overdue: int      # days since last security scan
    open_vulnerability_count: int        # known unpatched vulnerabilities
    mfa_enforcement_pct: float           # 0-1, % users with MFA


@dataclass
class SecurityResult:
    agent_id: str
    agent_type: str
    region: str
    security_risk: str
    threat_pattern: str
    security_severity: str
    recommended_action: str
    credential_score: float
    access_score: float
    injection_score: float
    compliance_score: float
    security_composite: float
    has_active_threat: bool
    requires_immediate_response: bool
    estimated_exposure_severity: float
    security_signal: str

    def to_dict(self) -> Dict:
        return {
            "agent_id":                   self.agent_id,
            "agent_type":                 self.agent_type,
            "region":                     self.region,
            "security_risk":              self.security_risk,
            "threat_pattern":             self.threat_pattern,
            "security_severity":          self.security_severity,
            "recommended_action":         self.recommended_action,
            "credential_score":           self.credential_score,
            "access_score":               self.access_score,
            "injection_score":            self.injection_score,
            "compliance_score":           self.compliance_score,
            "security_composite":         self.security_composite,
            "has_active_threat":          self.has_active_threat,
            "requires_immediate_response": self.requires_immediate_response,
            "estimated_exposure_severity": self.estimated_exposure_severity,
            "security_signal":            self.security_signal,
        }


class SwarmSecurityShieldEngine:
    def __init__(self) -> None:
        self._results: List[SecurityResult] = []

    def _credential_score(self, i: SecurityInput) -> float:
        s = 0
        if   i.hardcoded_secret_detected     >= 0.80: s += 40
        elif i.hardcoded_secret_detected     >= 0.40: s += 22
        elif i.hardcoded_secret_detected     >= 0.10: s += 8

        if   i.credential_in_plaintext_count >= 3:    s += 35
        elif i.credential_in_plaintext_count >= 1:    s += 18

        if   i.api_key_rotation_days_overdue >= 90:   s += 25
        elif i.api_key_rotation_days_overdue >= 30:   s += 12
        return min(s, 100)

    def _access_score(self, i: SecurityInput) -> float:
        s = 0
        if   i.unauthorized_access_attempts    >= 10: s += 40
        elif i.unauthorized_access_attempts    >= 5:  s += 22
        elif i.unauthorized_access_attempts    >= 1:  s += 8

        if   i.anomalous_access_pattern_score  >= 0.70: s += 35
        elif i.anomalous_access_pattern_score  >= 0.40: s += 18
        elif i.anomalous_access_pattern_score  >= 0.15: s += 6

        if   i.privilege_escalation_attempts   >= 2:  s += 25
        elif i.privilege_escalation_attempts   >= 1:  s += 12
        return min(s, 100)

    def _injection_score(self, i: SecurityInput) -> float:
        s = 0
        if   i.prompt_injection_attempts       >= 5:    s += 45
        elif i.prompt_injection_attempts       >= 2:    s += 25
        elif i.prompt_injection_attempts       >= 1:    s += 10

        if   i.sql_injection_attempts          >= 3:    s += 30
        elif i.sql_injection_attempts          >= 1:    s += 15

        if   i.input_validation_failure_rate   >= 0.20: s += 25
        elif i.input_validation_failure_rate   >= 0.08: s += 12
        return min(s, 100)

    def _compliance_score(self, i: SecurityInput) -> float:
        s = 0
        if   i.gdpr_compliance_score           <= 0.60: s += 40
        elif i.gdpr_compliance_score           <= 0.75: s += 22
        elif i.gdpr_compliance_score           <= 0.90: s += 8

        if   i.pii_exposure_risk_score         >= 0.50: s += 35
        elif i.pii_exposure_risk_score         >= 0.25: s += 18
        elif i.pii_exposure_risk_score         >= 0.10: s += 6

        if   i.open_vulnerability_count        >= 8:    s += 25
        elif i.open_vulnerability_count        >= 3:    s += 12
        return min(s, 100)

    def _composite(self, cr: float, ac: float, inj: float, co: float) -> float:
        return min(round(cr * 0.30 + ac * 0.25 + inj * 0.25 + co * 0.20, 2), 100.0)

    def _risk(self, c: float) -> SecurityRisk:
        if c >= 60: return SecurityRisk.critical
        if c >= 40: return SecurityRisk.high
        if c >= 20: return SecurityRisk.moderate
        return SecurityRisk.low

    def _severity(self, c: float) -> SecuritySeverity:
        if c >= 60: return SecuritySeverity.breached
        if c >= 40: return SecuritySeverity.threatened
        if c >= 20: return SecuritySeverity.monitoring
        return SecuritySeverity.secure

    def _pattern(self, i: SecurityInput) -> ThreatPattern:
        if (i.hardcoded_secret_detected >= 0.60
                or i.credential_in_plaintext_count >= 2):
            return ThreatPattern.credential_exposure
        if (i.prompt_injection_attempts >= 3
                or i.sql_injection_attempts >= 2):
            return ThreatPattern.injection_attempt
        if (i.pii_exposure_risk_score >= 0.40
                and i.data_encryption_compliance_pct <= 0.70):
            return ThreatPattern.data_exfiltration
        if (i.unauthorized_access_attempts >= 8
                or i.privilege_escalation_attempts >= 1):
            return ThreatPattern.access_anomaly
        if (i.gdpr_compliance_score <= 0.70
                and i.data_retention_violation_count >= 2):
            return ThreatPattern.compliance_violation
        return ThreatPattern.none

    def _action(self, risk: SecurityRisk, pat: ThreatPattern) -> SecurityAction:
        if risk == SecurityRisk.critical:
            if pat in (ThreatPattern.injection_attempt, ThreatPattern.data_exfiltration):
                return SecurityAction.emergency_lockdown
            if pat == ThreatPattern.credential_exposure:
                return SecurityAction.incident_containment
            return SecurityAction.incident_containment
        if risk == SecurityRisk.high:
            if pat == ThreatPattern.credential_exposure:  return SecurityAction.credential_rotation
            if pat == ThreatPattern.injection_attempt:    return SecurityAction.injection_block
            if pat == ThreatPattern.data_exfiltration:    return SecurityAction.data_quarantine
            if pat == ThreatPattern.access_anomaly:       return SecurityAction.access_review
            if pat == ThreatPattern.compliance_violation: return SecurityAction.compliance_audit
            return SecurityAction.security_monitoring
        if risk == SecurityRisk.moderate:
            return SecurityAction.security_monitoring
        return SecurityAction.no_action

    def _signal(self, i: SecurityInput, pat: ThreatPattern, comp: float) -> str:
        if comp < 20:
            return "Security posture strong — no credential exposure, injection attempts, access anomalies or compliance gaps detected"
        labels = {
            ThreatPattern.credential_exposure:  "Credential exposure",
            ThreatPattern.injection_attempt:    "Injection attempt",
            ThreatPattern.data_exfiltration:    "Data exfiltration risk",
            ThreatPattern.access_anomaly:       "Access anomaly",
            ThreatPattern.compliance_violation: "Compliance violation",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — {i.unauthorized_access_attempts} unauth access — "
            f"{i.prompt_injection_attempts} injection attempts — "
            f"GDPR {round(i.gdpr_compliance_score*100)}% — "
            f"{i.open_vulnerability_count} open vulns — "
            f"composite {round(comp)}"
        )

    def _has_active_threat(self, i: SecurityInput, comp: float) -> bool:
        return (comp >= 40
                or i.prompt_injection_attempts >= 1
                or i.unauthorized_access_attempts >= 5
                or i.credential_in_plaintext_count >= 1)

    def _requires_immediate_response(self, i: SecurityInput, comp: float) -> bool:
        return (comp >= 25
                or i.privilege_escalation_attempts >= 1
                or i.hardcoded_secret_detected >= 0.40
                or i.sql_injection_attempts >= 1)

    def _exposure_severity(self, i: SecurityInput, comp: float) -> float:
        return round(min(comp / 100 * (1 - i.gdpr_compliance_score + 0.01) * 10, 10.0), 2)

    def assess(self, i: SecurityInput) -> SecurityResult:
        cr   = self._credential_score(i)
        ac   = self._access_score(i)
        inj  = self._injection_score(i)
        co   = self._compliance_score(i)
        comp = self._composite(cr, ac, inj, co)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = SecurityResult(
            agent_id=i.agent_id,
            agent_type=i.agent_type,
            region=i.region,
            security_risk=risk.value,
            threat_pattern=pat.value,
            security_severity=sev.value,
            recommended_action=act.value,
            credential_score=cr,
            access_score=ac,
            injection_score=inj,
            compliance_score=co,
            security_composite=comp,
            has_active_threat=self._has_active_threat(i, comp),
            requires_immediate_response=self._requires_immediate_response(i, comp),
            estimated_exposure_severity=self._exposure_severity(i, comp),
            security_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[SecurityInput]) -> List[SecurityResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_security_composite": 0.0,
                "active_threat_count": 0,
                "immediate_response_count": 0,
                "avg_credential_score": 0.0,
                "avg_access_score": 0.0,
                "avg_injection_score": 0.0,
                "avg_compliance_score": 0.0,
                "avg_estimated_exposure_severity": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tcr = tac = tinj = tco = tcomp = texpos = 0.0
        gc = ec = 0
        for r in self._results:
            rc[r.security_risk]      = rc.get(r.security_risk, 0)      + 1
            pc[r.threat_pattern]     = pc.get(r.threat_pattern, 0)     + 1
            sc[r.security_severity]  = sc.get(r.security_severity, 0)  + 1
            ac[r.recommended_action] = ac.get(r.recommended_action, 0) + 1
            tcr    += r.credential_score
            tac    += r.access_score
            tinj   += r.injection_score
            tco    += r.compliance_score
            tcomp  += r.security_composite
            texpos += r.estimated_exposure_severity
            if r.has_active_threat:            gc += 1
            if r.requires_immediate_response:  ec += 1
        return {
            "total":                              n,
            "risk_counts":                        rc,
            "pattern_counts":                     pc,
            "severity_counts":                    sc,
            "action_counts":                      ac,
            "avg_security_composite":             round(tcomp / n, 1),
            "active_threat_count":                gc,
            "immediate_response_count":           ec,
            "avg_credential_score":               round(tcr / n, 1),
            "avg_access_score":                   round(tac / n, 1),
            "avg_injection_score":                round(tinj / n, 1),
            "avg_compliance_score":               round(tco / n, 1),
            "avg_estimated_exposure_severity":    round(texpos / n, 2),
        }
