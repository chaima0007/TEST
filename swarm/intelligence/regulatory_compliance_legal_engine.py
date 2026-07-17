from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class ComplianceRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class CompliancePattern(str, Enum):
    none                = "none"
    regulatory_breach   = "regulatory_breach"
    policy_gap          = "policy_gap"
    audit_failure       = "audit_failure"
    sanction_risk       = "sanction_risk"
    reporting_violation = "reporting_violation"


class ComplianceSeverity(str, Enum):
    compliant = "compliant"
    monitored = "monitored"
    exposed   = "exposed"
    violated  = "violated"


class ComplianceAction(str, Enum):
    no_action             = "no_action"
    compliance_monitoring = "compliance_monitoring"
    policy_update         = "policy_update"
    audit_remediation     = "audit_remediation"
    regulatory_dialogue   = "regulatory_dialogue"
    sanction_response     = "sanction_response"
    emergency_compliance  = "emergency_compliance"
    regulatory_shutdown   = "regulatory_shutdown"


@dataclass
class ComplianceInput:
    entity_id: str
    entity_domain: str
    region: str
    policy_adherence_score: float
    regulatory_deadline_compliance: float
    internal_audit_score: float
    external_audit_score: float
    sanction_history_score: float
    reporting_accuracy: float
    documentation_completeness: float
    training_completion_rate: float
    whistleblower_incident_rate: float
    data_governance_score: float
    third_party_compliance_score: float
    regulatory_change_adaptation_speed: float
    ethics_committee_effectiveness: float
    control_testing_coverage: float
    risk_register_completeness: float
    legal_counsel_access_score: float
    compliance_culture_score: float


@dataclass
class ComplianceResult:
    entity_id: str
    region: str
    compliance_risk: str
    compliance_pattern: str
    compliance_severity: str
    recommended_action: str
    policy_score: float
    audit_score: float
    risk_score: float
    culture_score: float
    compliance_composite: float
    has_compliance_breach: bool
    requires_executive_action: bool
    estimated_sanction_risk_index: float
    compliance_signal: str

    def to_dict(self) -> Dict:
        return {
            "entity_id":                      self.entity_id,
            "region":                         self.region,
            "compliance_risk":                self.compliance_risk,
            "compliance_pattern":             self.compliance_pattern,
            "compliance_severity":            self.compliance_severity,
            "recommended_action":             self.recommended_action,
            "policy_score":                   self.policy_score,
            "audit_score":                    self.audit_score,
            "risk_score":                     self.risk_score,
            "culture_score":                  self.culture_score,
            "compliance_composite":           self.compliance_composite,
            "has_compliance_breach":          self.has_compliance_breach,
            "requires_executive_action":      self.requires_executive_action,
            "estimated_sanction_risk_index":  self.estimated_sanction_risk_index,
            "compliance_signal":              self.compliance_signal,
        }


class RegulatoryComplianceLegalEngine:
    def __init__(self) -> None:
        self._results: List[ComplianceResult] = []

    def _policy_score(self, i: ComplianceInput) -> float:
        s = 0
        if   i.policy_adherence_score <= 0.30: s += 40
        elif i.policy_adherence_score <= 0.55: s += 22
        elif i.policy_adherence_score <= 0.75: s += 8

        if   i.regulatory_deadline_compliance <= 0.30: s += 35
        elif i.regulatory_deadline_compliance <= 0.55: s += 18
        elif i.regulatory_deadline_compliance <= 0.75: s += 6

        if   i.documentation_completeness <= 0.30: s += 25
        elif i.documentation_completeness <= 0.55: s += 12
        return min(s, 100)

    def _audit_score(self, i: ComplianceInput) -> float:
        s = 0
        if   i.internal_audit_score <= 0.30: s += 40
        elif i.internal_audit_score <= 0.55: s += 22
        elif i.internal_audit_score <= 0.75: s += 8

        if   i.external_audit_score <= 0.30: s += 35
        elif i.external_audit_score <= 0.55: s += 18
        elif i.external_audit_score <= 0.75: s += 6

        if   i.control_testing_coverage <= 0.30: s += 25
        elif i.control_testing_coverage <= 0.55: s += 12
        return min(s, 100)

    def _risk_score(self, i: ComplianceInput) -> float:
        s = 0
        if   i.sanction_history_score >= 0.70: s += 40
        elif i.sanction_history_score >= 0.45: s += 22
        elif i.sanction_history_score >= 0.25: s += 8

        if   i.whistleblower_incident_rate >= 0.70: s += 35
        elif i.whistleblower_incident_rate >= 0.45: s += 18
        elif i.whistleblower_incident_rate >= 0.25: s += 6

        if   i.risk_register_completeness <= 0.30: s += 25
        elif i.risk_register_completeness <= 0.55: s += 12
        return min(s, 100)

    def _culture_score(self, i: ComplianceInput) -> float:
        s = 0
        if   i.compliance_culture_score <= 0.30: s += 40
        elif i.compliance_culture_score <= 0.55: s += 22
        elif i.compliance_culture_score <= 0.75: s += 8

        if   i.training_completion_rate <= 0.30: s += 35
        elif i.training_completion_rate <= 0.55: s += 18
        elif i.training_completion_rate <= 0.75: s += 6

        if   i.ethics_committee_effectiveness <= 0.30: s += 25
        elif i.ethics_committee_effectiveness <= 0.55: s += 12
        return min(s, 100)

    def _composite(self, pol: float, aud: float, rsk: float, cul: float) -> float:
        return min(round(pol * 0.30 + aud * 0.25 + rsk * 0.25 + cul * 0.20, 2), 100.0)

    def _risk(self, c: float) -> ComplianceRisk:
        if c >= 60: return ComplianceRisk.critical
        if c >= 40: return ComplianceRisk.high
        if c >= 20: return ComplianceRisk.moderate
        return ComplianceRisk.low

    def _severity(self, c: float) -> ComplianceSeverity:
        if c >= 60: return ComplianceSeverity.violated
        if c >= 40: return ComplianceSeverity.exposed
        if c >= 20: return ComplianceSeverity.monitored
        return ComplianceSeverity.compliant

    def _pattern(self, i: ComplianceInput) -> CompliancePattern:
        if i.policy_adherence_score <= 0.35 or i.regulatory_deadline_compliance <= 0.35:
            return CompliancePattern.regulatory_breach
        if i.internal_audit_score <= 0.4 and i.external_audit_score <= 0.45:
            return CompliancePattern.audit_failure
        if i.sanction_history_score >= 0.5 or i.whistleblower_incident_rate >= 0.5:
            return CompliancePattern.sanction_risk
        if i.documentation_completeness <= 0.45 or i.control_testing_coverage <= 0.4:
            return CompliancePattern.policy_gap
        if i.reporting_accuracy <= 0.45 or i.data_governance_score <= 0.4:
            return CompliancePattern.reporting_violation
        return CompliancePattern.none

    def _action(self, risk: ComplianceRisk, pat: CompliancePattern) -> ComplianceAction:
        if risk == ComplianceRisk.critical:
            if pat == CompliancePattern.regulatory_breach: return ComplianceAction.regulatory_shutdown
            if pat == CompliancePattern.sanction_risk:     return ComplianceAction.emergency_compliance
            return ComplianceAction.sanction_response
        if risk == ComplianceRisk.high:
            if pat == CompliancePattern.audit_failure:       return ComplianceAction.audit_remediation
            if pat == CompliancePattern.regulatory_breach:   return ComplianceAction.emergency_compliance
            if pat == CompliancePattern.policy_gap:          return ComplianceAction.policy_update
            if pat == CompliancePattern.reporting_violation: return ComplianceAction.regulatory_dialogue
            return ComplianceAction.audit_remediation
        if risk == ComplianceRisk.moderate:
            return ComplianceAction.compliance_monitoring
        return ComplianceAction.no_action

    def _has_breach(self, i: ComplianceInput, comp: float) -> bool:
        return (comp >= 40
                or i.sanction_history_score >= 0.4
                or i.policy_adherence_score <= 0.4
                or i.external_audit_score <= 0.4)

    def _requires_exec(self, i: ComplianceInput, comp: float) -> bool:
        return (comp >= 25
                or i.whistleblower_incident_rate >= 0.4
                or i.regulatory_deadline_compliance <= 0.35)

    def _risk_index(self, i: ComplianceInput, comp: float) -> float:
        return round(min(comp / 100 * (1 - i.legal_counsel_access_score + 0.01) * 10, 10.0), 2)

    def _signal(self, i: ComplianceInput, pat: CompliancePattern, comp: float) -> str:
        if comp < 20:
            return "Conformité réglementaire exemplaire — politiques respectées, audits réussis, culture compliance forte"
        labels = {
            CompliancePattern.regulatory_breach:   "Brèche réglementaire",
            CompliancePattern.audit_failure:       "Défaillance audit",
            CompliancePattern.sanction_risk:       "Risque sanction",
            CompliancePattern.policy_gap:          "Lacune politique",
            CompliancePattern.reporting_violation: "Violation reporting",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — adhésion politiques {round(i.policy_adherence_score * 100)}%"
            f" — audits internes {round(i.internal_audit_score * 100)}%"
            f" — risque sanction {round(i.sanction_history_score * 100)}%"
            f" — composite {round(comp)}"
        )

    def assess(self, i: ComplianceInput) -> ComplianceResult:
        pol  = self._policy_score(i)
        aud  = self._audit_score(i)
        rsk  = self._risk_score(i)
        cul  = self._culture_score(i)
        comp = self._composite(pol, aud, rsk, cul)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = ComplianceResult(
            entity_id=i.entity_id,
            region=i.region,
            compliance_risk=risk.value,
            compliance_pattern=pat.value,
            compliance_severity=sev.value,
            recommended_action=act.value,
            policy_score=pol,
            audit_score=aud,
            risk_score=rsk,
            culture_score=cul,
            compliance_composite=comp,
            has_compliance_breach=self._has_breach(i, comp),
            requires_executive_action=self._requires_exec(i, comp),
            estimated_sanction_risk_index=self._risk_index(i, comp),
            compliance_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[ComplianceInput]) -> List[ComplianceResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_compliance_composite": 0.0,
                "compliance_breach_count": 0,
                "executive_action_count": 0,
                "avg_policy_score": 0.0,
                "avg_audit_score": 0.0,
                "avg_risk_score": 0.0,
                "avg_culture_score": 0.0,
                "avg_estimated_sanction_risk_index": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tpol = taud = trsk = tcul = tcomp = tridx = 0.0
        breach_count = exec_count = 0
        for r in self._results:
            rc[r.compliance_risk]     = rc.get(r.compliance_risk, 0)     + 1
            pc[r.compliance_pattern]  = pc.get(r.compliance_pattern, 0)  + 1
            sc[r.compliance_severity] = sc.get(r.compliance_severity, 0) + 1
            ac[r.recommended_action]  = ac.get(r.recommended_action, 0)  + 1
            tpol  += r.policy_score
            taud  += r.audit_score
            trsk  += r.risk_score
            tcul  += r.culture_score
            tcomp += r.compliance_composite
            tridx += r.estimated_sanction_risk_index
            if r.has_compliance_breach:     breach_count += 1
            if r.requires_executive_action: exec_count   += 1
        return {
            "total":                              n,
            "risk_counts":                        rc,
            "pattern_counts":                     pc,
            "severity_counts":                    sc,
            "action_counts":                      ac,
            "avg_compliance_composite":           round(tcomp / n, 1),
            "compliance_breach_count":            breach_count,
            "executive_action_count":             exec_count,
            "avg_policy_score":                   round(tpol / n, 1),
            "avg_audit_score":                    round(taud / n, 1),
            "avg_risk_score":                     round(trsk / n, 1),
            "avg_culture_score":                  round(tcul / n, 1),
            "avg_estimated_sanction_risk_index":  round(tridx / n, 2),
        }
