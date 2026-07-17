"""
Module 234 — Data Protection Engine
Expert agent specialised in RGPD/CCPA compliance, data-subject rights,
breach detection, encryption auditing and cross-border transfer controls —
operating silently alongside all Caelum swarm agents.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class ProtectionRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ViolationPattern(str, Enum):
    none                  = "none"
    consent_violation     = "consent_violation"
    data_breach           = "data_breach"
    rights_denial         = "rights_denial"
    cross_border_exposure = "cross_border_exposure"
    retention_breach      = "retention_breach"


class ProtectionSeverity(str, Enum):
    compliant   = "compliant"
    monitoring  = "monitoring"
    at_risk     = "at_risk"
    breached    = "breached"


class ProtectionAction(str, Enum):
    no_action               = "no_action"
    compliance_monitoring   = "compliance_monitoring"
    consent_remediation     = "consent_remediation"
    rights_processing       = "rights_processing"
    dpia_required           = "dpia_required"
    breach_notification     = "breach_notification"
    transfer_suspension     = "transfer_suspension"
    regulatory_filing       = "regulatory_filing"
    emergency_data_lockdown = "emergency_data_lockdown"


@dataclass
class ProtectionInput:
    dossier_id: str
    entity_type: str                         # customer / employee / partner / prospect
    region: str
    # Consent & lawfulness
    consent_validity_score: float            # 0-1 (1 = fully valid, documented)
    consent_recency_days: int                # days since last consent refresh
    data_minimization_score: float           # 0-1 (1 = minimal data only)
    purpose_limitation_score: float          # 0-1 (1 = data used only for stated purpose)
    # Data-subject rights
    access_request_pending_days: int         # days overdue for access request
    erasure_request_pending_days: int        # days overdue for erasure request
    portability_request_pending_days: int    # days overdue for portability request
    # Breach & security
    breach_detection_days_since: int         # days since potential breach detected
    breach_notification_delay_hours: int     # hours delay for supervisory notification
    encryption_at_rest_pct: float            # 0-1
    encryption_in_transit_pct: float         # 0-1
    vulnerability_exposure_score: float      # 0-1 (1 = highly exposed)
    # Cross-border transfers
    cross_border_transfer_unprotected: int   # transfers without adequate safeguards
    standard_contractual_clauses_pct: float  # 0-1 (% of transfers covered by SCCs)
    # Retention
    retention_excess_days: int               # days past retention limit
    retention_violation_count: int
    # Accountability
    dpia_completion_pct: float               # 0-1 (% of required DPIAs completed)
    third_party_processor_compliance: float  # 0-1 (processor audit score)


@dataclass
class ProtectionResult:
    dossier_id: str
    entity_type: str
    region: str
    protection_risk: str
    violation_pattern: str
    protection_severity: str
    recommended_action: str
    rgpd_score: float
    rights_score: float
    breach_score: float
    transfer_score: float
    protection_composite: float
    has_active_violation: bool
    requires_dpa_notification: bool
    estimated_fine_risk_index: float
    protection_signal: str

    def to_dict(self) -> Dict:
        return {
            "dossier_id":             self.dossier_id,
            "entity_type":            self.entity_type,
            "region":                 self.region,
            "protection_risk":        self.protection_risk,
            "violation_pattern":      self.violation_pattern,
            "protection_severity":    self.protection_severity,
            "recommended_action":     self.recommended_action,
            "rgpd_score":             self.rgpd_score,
            "rights_score":           self.rights_score,
            "breach_score":           self.breach_score,
            "transfer_score":         self.transfer_score,
            "protection_composite":   self.protection_composite,
            "has_active_violation":   self.has_active_violation,
            "requires_dpa_notification": self.requires_dpa_notification,
            "estimated_fine_risk_index": self.estimated_fine_risk_index,
            "protection_signal":      self.protection_signal,
        }


class DataProtectionEngine:
    def __init__(self) -> None:
        self._results: List[ProtectionResult] = []

    def _rgpd_score(self, i: ProtectionInput) -> float:
        s = 0
        if   i.consent_validity_score  <= 0.40: s += 40
        elif i.consent_validity_score  <= 0.70: s += 22
        elif i.consent_validity_score  <= 0.90: s += 8

        if   i.consent_recency_days    >= 365:  s += 25
        elif i.consent_recency_days    >= 180:  s += 12
        elif i.consent_recency_days    >= 90:   s += 5

        if   i.data_minimization_score <= 0.40: s += 20
        elif i.data_minimization_score <= 0.70: s += 10
        elif i.data_minimization_score <= 0.85: s += 4

        if   i.purpose_limitation_score <= 0.40: s += 15
        elif i.purpose_limitation_score <= 0.70: s += 8
        return min(s, 100)

    def _rights_score(self, i: ProtectionInput) -> float:
        s = 0
        if   i.access_request_pending_days      >= 30: s += 40
        elif i.access_request_pending_days      >= 10: s += 22
        elif i.access_request_pending_days      >= 1:  s += 8

        if   i.erasure_request_pending_days     >= 30: s += 35
        elif i.erasure_request_pending_days     >= 10: s += 18
        elif i.erasure_request_pending_days     >= 1:  s += 6

        if   i.portability_request_pending_days >= 30: s += 25
        elif i.portability_request_pending_days >= 10: s += 12
        elif i.portability_request_pending_days >= 1:  s += 4
        return min(s, 100)

    def _breach_score(self, i: ProtectionInput) -> float:
        s = 0
        if   i.breach_notification_delay_hours  >= 72: s += 40
        elif i.breach_notification_delay_hours  >= 24: s += 22
        elif i.breach_notification_delay_hours  >= 1:  s += 8

        if   i.vulnerability_exposure_score     >= 0.70: s += 30
        elif i.vulnerability_exposure_score     >= 0.40: s += 16
        elif i.vulnerability_exposure_score     >= 0.15: s += 6

        if   i.encryption_at_rest_pct           <= 0.50: s += 20
        elif i.encryption_at_rest_pct           <= 0.80: s += 10

        if   i.encryption_in_transit_pct        <= 0.50: s += 10
        elif i.encryption_in_transit_pct        <= 0.80: s += 5
        return min(s, 100)

    def _transfer_score(self, i: ProtectionInput) -> float:
        s = 0
        if   i.cross_border_transfer_unprotected >= 5:  s += 45
        elif i.cross_border_transfer_unprotected >= 2:  s += 25
        elif i.cross_border_transfer_unprotected >= 1:  s += 10

        if   i.standard_contractual_clauses_pct  <= 0.40: s += 35
        elif i.standard_contractual_clauses_pct  <= 0.70: s += 18
        elif i.standard_contractual_clauses_pct  <= 0.90: s += 6

        if   i.retention_excess_days             >= 90: s += 20
        elif i.retention_excess_days             >= 30: s += 10
        return min(s, 100)

    def _composite(self, rg: float, ri: float, br: float, tr: float) -> float:
        return min(round(rg * 0.30 + ri * 0.25 + br * 0.25 + tr * 0.20, 2), 100.0)

    def _risk(self, c: float) -> ProtectionRisk:
        if c >= 60: return ProtectionRisk.critical
        if c >= 40: return ProtectionRisk.high
        if c >= 20: return ProtectionRisk.moderate
        return ProtectionRisk.low

    def _severity(self, c: float) -> ProtectionSeverity:
        if c >= 60: return ProtectionSeverity.breached
        if c >= 40: return ProtectionSeverity.at_risk
        if c >= 20: return ProtectionSeverity.monitoring
        return ProtectionSeverity.compliant

    def _pattern(self, i: ProtectionInput) -> ViolationPattern:
        if i.breach_notification_delay_hours >= 24 or i.vulnerability_exposure_score >= 0.60:
            return ViolationPattern.data_breach
        if i.consent_validity_score <= 0.40 or i.purpose_limitation_score <= 0.40:
            return ViolationPattern.consent_violation
        if (i.access_request_pending_days >= 15
                or i.erasure_request_pending_days >= 15
                or i.portability_request_pending_days >= 15):
            return ViolationPattern.rights_denial
        if i.cross_border_transfer_unprotected >= 2 or i.standard_contractual_clauses_pct <= 0.50:
            return ViolationPattern.cross_border_exposure
        if i.retention_excess_days >= 30 or i.retention_violation_count >= 2:
            return ViolationPattern.retention_breach
        return ViolationPattern.none

    def _action(self, risk: ProtectionRisk, pat: ViolationPattern) -> ProtectionAction:
        if risk == ProtectionRisk.critical:
            if pat == ViolationPattern.data_breach:
                return ProtectionAction.emergency_data_lockdown
            if pat in (ViolationPattern.cross_border_exposure,):
                return ProtectionAction.transfer_suspension
            return ProtectionAction.regulatory_filing
        if risk == ProtectionRisk.high:
            if pat == ViolationPattern.data_breach:        return ProtectionAction.breach_notification
            if pat == ViolationPattern.consent_violation:  return ProtectionAction.consent_remediation
            if pat == ViolationPattern.rights_denial:      return ProtectionAction.rights_processing
            if pat == ViolationPattern.cross_border_exposure: return ProtectionAction.dpia_required
            if pat == ViolationPattern.retention_breach:   return ProtectionAction.regulatory_filing
            return ProtectionAction.compliance_monitoring
        if risk == ProtectionRisk.moderate:
            return ProtectionAction.compliance_monitoring
        return ProtectionAction.no_action

    def _fine_risk(self, i: ProtectionInput, comp: float) -> float:
        gdpr_aggravator = 1 + (1 - i.dpia_completion_pct) * 0.5 + (1 - i.third_party_processor_compliance) * 0.3
        return round(min(comp / 100 * gdpr_aggravator * 10, 10.0), 2)

    def _active_violation(self, i: ProtectionInput, comp: float) -> bool:
        return (comp >= 40
                or i.breach_notification_delay_hours >= 24
                or i.access_request_pending_days >= 15
                or i.erasure_request_pending_days >= 15
                or i.cross_border_transfer_unprotected >= 2)

    def _dpa_notification(self, i: ProtectionInput, comp: float) -> bool:
        return (comp >= 25
                or i.breach_notification_delay_hours >= 1
                or i.vulnerability_exposure_score >= 0.60
                or i.cross_border_transfer_unprotected >= 3)

    def _signal(self, i: ProtectionInput, pat: ViolationPattern, comp: float) -> str:
        if comp < 20:
            return "Protection des données conforme — consentement valide, droits respectés, aucune violation détectée"
        labels: Dict[ViolationPattern, str] = {
            ViolationPattern.consent_violation:     "Violation de consentement",
            ViolationPattern.data_breach:           "Violation de données",
            ViolationPattern.rights_denial:         "Déni des droits RGPD",
            ViolationPattern.cross_border_exposure: "Transfert transfrontalier non sécurisé",
            ViolationPattern.retention_breach:      "Violation de rétention",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — consentement {round(i.consent_validity_score*100)}% — "
            f"accès en retard {i.access_request_pending_days}j — "
            f"effacement en retard {i.erasure_request_pending_days}j — "
            f"transferts non protégés {i.cross_border_transfer_unprotected} — "
            f"composite {round(comp)}"
        )

    def assess(self, i: ProtectionInput) -> ProtectionResult:
        rg   = self._rgpd_score(i)
        ri   = self._rights_score(i)
        br   = self._breach_score(i)
        tr   = self._transfer_score(i)
        comp = self._composite(rg, ri, br, tr)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = ProtectionResult(
            dossier_id=i.dossier_id,
            entity_type=i.entity_type,
            region=i.region,
            protection_risk=risk.value,
            violation_pattern=pat.value,
            protection_severity=sev.value,
            recommended_action=act.value,
            rgpd_score=rg,
            rights_score=ri,
            breach_score=br,
            transfer_score=tr,
            protection_composite=comp,
            has_active_violation=self._active_violation(i, comp),
            requires_dpa_notification=self._dpa_notification(i, comp),
            estimated_fine_risk_index=self._fine_risk(i, comp),
            protection_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[ProtectionInput]) -> List[ProtectionResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_protection_composite": 0.0,
                "active_violation_count": 0,
                "dpa_notification_count": 0,
                "avg_rgpd_score": 0.0,
                "avg_rights_score": 0.0,
                "avg_breach_score": 0.0,
                "avg_transfer_score": 0.0,
                "avg_estimated_fine_risk_index": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        trg = tri = tbr = ttr = tcomp = tfine = 0.0
        av = dpa = 0
        for r in self._results:
            rc[r.protection_risk]      = rc.get(r.protection_risk, 0)      + 1
            pc[r.violation_pattern]    = pc.get(r.violation_pattern, 0)    + 1
            sc[r.protection_severity]  = sc.get(r.protection_severity, 0)  + 1
            ac[r.recommended_action]   = ac.get(r.recommended_action, 0)   + 1
            trg   += r.rgpd_score
            tri   += r.rights_score
            tbr   += r.breach_score
            ttr   += r.transfer_score
            tcomp += r.protection_composite
            tfine += r.estimated_fine_risk_index
            if r.has_active_violation:     av  += 1
            if r.requires_dpa_notification: dpa += 1
        return {
            "total":                          n,
            "risk_counts":                    rc,
            "pattern_counts":                 pc,
            "severity_counts":                sc,
            "action_counts":                  ac,
            "avg_protection_composite":       round(tcomp / n, 1),
            "active_violation_count":         av,
            "dpa_notification_count":         dpa,
            "avg_rgpd_score":                 round(trg / n, 1),
            "avg_rights_score":               round(tri / n, 1),
            "avg_breach_score":               round(tbr / n, 1),
            "avg_transfer_score":             round(ttr / n, 1),
            "avg_estimated_fine_risk_index":  round(tfine / n, 2),
        }
