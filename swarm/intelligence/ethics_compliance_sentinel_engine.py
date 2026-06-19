"""Ethics & Compliance Sentinel Engine — Module 228
Monitors AI agents for bias, privacy, ethical, and regulatory compliance risks
across the Caelum Swarm and escalates findings to appropriate oversight bodies."""

from __future__ import annotations

import dataclasses
from enum import Enum


class ComplianceRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class CompliancePattern(str, Enum):
    none                = "none"
    bias_detection      = "bias_detection"
    gdpr_violation      = "gdpr_violation"
    ethical_breach      = "ethical_breach"
    regulatory_gap      = "regulatory_gap"
    transparency_failure = "transparency_failure"


class ComplianceSeverity(str, Enum):
    compliant     = "compliant"
    watchlist     = "watchlist"
    non_compliant = "non_compliant"
    breach        = "breach"


class ComplianceAction(str, Enum):
    no_action                  = "no_action"
    compliance_monitoring      = "compliance_monitoring"
    bias_review                = "bias_review"
    gdpr_remediation           = "gdpr_remediation"
    ethical_committee_review   = "ethical_committee_review"
    regulatory_audit           = "regulatory_audit"
    transparency_report        = "transparency_report"
    immediate_suspension       = "immediate_suspension"
    legal_escalation           = "legal_escalation"


@dataclasses.dataclass
class ComplianceInput:
    agent_id:                         str
    agent_type:                       str
    region:                           str
    # Bias detection fields
    decision_bias_score:              float   # 0-1
    demographic_disparity_pct:        float   # 0-1
    model_fairness_score:             float   # 0-1, 1=fair
    # Privacy / GDPR fields
    data_consent_compliance_pct:      float   # 0-1
    right_to_erasure_violations:      int
    data_minimization_score:          float   # 0-1, 1=minimal
    cross_border_transfer_violations: int
    # Ethics fields
    ethical_override_frequency:       float   # 0-1
    value_alignment_score:            float   # 0-1, 1=aligned
    human_oversight_pct:              float   # 0-1, % decisions with human review
    # Regulatory fields
    regulatory_update_lag_days:       int
    compliance_training_completion_pct: float # 0-1
    audit_finding_count:              int
    policy_exception_rate_pct:        float   # 0-1
    # Transparency fields
    transparency_score:               float   # 0-1, 1=fully transparent
    explainability_score:             float   # 0-1
    # Incident fields
    stakeholder_concern_count:        int
    incident_report_count_90d:        int


@dataclasses.dataclass
class ComplianceResult:
    agent_id:                  str
    region:                    str
    compliance_risk:           ComplianceRisk
    compliance_pattern:        CompliancePattern
    compliance_severity:       ComplianceSeverity
    recommended_action:        ComplianceAction
    bias_score:                float
    privacy_score:             float
    ethics_score:              float
    regulatory_score:          float
    compliance_composite:      float
    has_compliance_flag:       bool
    requires_immediate_review: bool
    estimated_liability_index: float  # 0-10
    compliance_signal:         str

    def to_dict(self) -> dict:
        return {
            "agent_id":                  self.agent_id,
            "region":                    self.region,
            "compliance_risk":           self.compliance_risk.value,
            "compliance_pattern":        self.compliance_pattern.value,
            "compliance_severity":       self.compliance_severity.value,
            "recommended_action":        self.recommended_action.value,
            "bias_score":                round(self.bias_score, 1),
            "privacy_score":             round(self.privacy_score, 1),
            "ethics_score":              round(self.ethics_score, 1),
            "regulatory_score":          round(self.regulatory_score, 1),
            "compliance_composite":      round(self.compliance_composite, 1),
            "has_compliance_flag":       self.has_compliance_flag,
            "requires_immediate_review": self.requires_immediate_review,
            "estimated_liability_index": self.estimated_liability_index,
            "compliance_signal":         self.compliance_signal,
        }


def _clamp(v: float) -> float:
    return max(0.0, min(100.0, v))


class EthicsComplianceSentinelEngine:
    """Monitors AI agents for ethics and compliance violations across the Caelum Swarm."""

    def __init__(self) -> None:
        self._results: list[ComplianceResult] = []

    # ── sub-scores (HIGHER = worse compliance) ───────────────────────────────

    def _bias_score(self, inp: ComplianceInput) -> float:
        score = 0.0
        # decision_bias_score
        if inp.decision_bias_score >= 0.60:
            score += 40.0
        elif inp.decision_bias_score >= 0.35:
            score += 22.0
        elif inp.decision_bias_score >= 0.15:
            score += 8.0
        # demographic_disparity_pct
        if inp.demographic_disparity_pct >= 0.30:
            score += 35.0
        elif inp.demographic_disparity_pct >= 0.15:
            score += 18.0
        elif inp.demographic_disparity_pct >= 0.05:
            score += 6.0
        # model_fairness_score (lower = worse)
        if inp.model_fairness_score <= 0.50:
            score += 25.0
        elif inp.model_fairness_score <= 0.70:
            score += 12.0
        return _clamp(score)

    def _privacy_score(self, inp: ComplianceInput) -> float:
        score = 0.0
        # data_consent_compliance_pct (lower = worse)
        if inp.data_consent_compliance_pct <= 0.70:
            score += 40.0
        elif inp.data_consent_compliance_pct <= 0.85:
            score += 22.0
        elif inp.data_consent_compliance_pct <= 0.95:
            score += 8.0
        # right_to_erasure_violations
        if inp.right_to_erasure_violations >= 3:
            score += 35.0
        elif inp.right_to_erasure_violations >= 1:
            score += 18.0
        # cross_border_transfer_violations
        if inp.cross_border_transfer_violations >= 2:
            score += 25.0
        elif inp.cross_border_transfer_violations >= 1:
            score += 12.0
        return _clamp(score)

    def _ethics_score(self, inp: ComplianceInput) -> float:
        score = 0.0
        # ethical_override_frequency
        if inp.ethical_override_frequency >= 0.30:
            score += 45.0
        elif inp.ethical_override_frequency >= 0.15:
            score += 25.0
        elif inp.ethical_override_frequency >= 0.05:
            score += 10.0
        # value_alignment_score (lower = worse)
        if inp.value_alignment_score <= 0.50:
            score += 30.0
        elif inp.value_alignment_score <= 0.70:
            score += 15.0
        # human_oversight_pct (lower = worse)
        if inp.human_oversight_pct <= 0.30:
            score += 25.0
        elif inp.human_oversight_pct <= 0.55:
            score += 12.0
        return _clamp(score)

    def _regulatory_score(self, inp: ComplianceInput) -> float:
        score = 0.0
        # regulatory_update_lag_days
        if inp.regulatory_update_lag_days >= 60:
            score += 40.0
        elif inp.regulatory_update_lag_days >= 30:
            score += 22.0
        elif inp.regulatory_update_lag_days >= 15:
            score += 8.0
        # audit_finding_count
        if inp.audit_finding_count >= 5:
            score += 35.0
        elif inp.audit_finding_count >= 2:
            score += 18.0
        elif inp.audit_finding_count >= 1:
            score += 6.0
        # policy_exception_rate_pct
        if inp.policy_exception_rate_pct >= 0.20:
            score += 25.0
        elif inp.policy_exception_rate_pct >= 0.10:
            score += 12.0
        return _clamp(score)

    # ── classification ───────────────────────────────────────────────────────

    def _classify_risk(self, composite: float) -> ComplianceRisk:
        if composite >= 60:
            return ComplianceRisk.critical
        if composite >= 40:
            return ComplianceRisk.high
        if composite >= 20:
            return ComplianceRisk.moderate
        return ComplianceRisk.low

    def _classify_severity(self, composite: float) -> ComplianceSeverity:
        if composite >= 60:
            return ComplianceSeverity.breach
        if composite >= 40:
            return ComplianceSeverity.non_compliant
        if composite >= 20:
            return ComplianceSeverity.watchlist
        return ComplianceSeverity.compliant

    def _classify_pattern(self, inp: ComplianceInput) -> CompliancePattern:
        # Priority order: check most severe first
        if inp.decision_bias_score >= 0.50 and inp.demographic_disparity_pct >= 0.20:
            return CompliancePattern.bias_detection
        if inp.data_consent_compliance_pct <= 0.75 and inp.right_to_erasure_violations >= 1:
            return CompliancePattern.gdpr_violation
        if inp.ethical_override_frequency >= 0.25 and inp.value_alignment_score <= 0.55:
            return CompliancePattern.ethical_breach
        if inp.regulatory_update_lag_days >= 45 and inp.audit_finding_count >= 3:
            return CompliancePattern.regulatory_gap
        if inp.transparency_score <= 0.40 and inp.explainability_score <= 0.40:
            return CompliancePattern.transparency_failure
        return CompliancePattern.none

    def _recommended_action(
        self,
        risk: ComplianceRisk,
        pattern: CompliancePattern,
    ) -> ComplianceAction:
        if risk == ComplianceRisk.critical:
            if pattern in (CompliancePattern.bias_detection, CompliancePattern.gdpr_violation):
                return ComplianceAction.legal_escalation
            return ComplianceAction.immediate_suspension
        if risk == ComplianceRisk.high:
            if pattern == CompliancePattern.bias_detection:
                return ComplianceAction.bias_review
            if pattern == CompliancePattern.gdpr_violation:
                return ComplianceAction.gdpr_remediation
            if pattern == CompliancePattern.ethical_breach:
                return ComplianceAction.ethical_committee_review
            if pattern == CompliancePattern.regulatory_gap:
                return ComplianceAction.regulatory_audit
            if pattern == CompliancePattern.transparency_failure:
                return ComplianceAction.transparency_report
            return ComplianceAction.compliance_monitoring
        if risk == ComplianceRisk.moderate:
            return ComplianceAction.compliance_monitoring
        return ComplianceAction.no_action

    def _signal(
        self,
        comp: float,
        inp: ComplianceInput,
    ) -> str:
        if comp < 20:
            return (
                "Compliance posture strong — bias, privacy, ethics and regulatory "
                "indicators within acceptable thresholds"
            )
        risk = self._classify_risk(comp)
        label = risk.value
        return (
            f"{label} — bias {round(inp.decision_bias_score * 100)}% "
            f"— consent {round(inp.data_consent_compliance_pct * 100)}% "
            f"— lag {inp.regulatory_update_lag_days}d "
            f"— composite {round(comp)}"
        )

    # ── public API ───────────────────────────────────────────────────────────

    def assess(self, inp: ComplianceInput) -> ComplianceResult:
        bias       = self._bias_score(inp)
        privacy    = self._privacy_score(inp)
        ethics     = self._ethics_score(inp)
        regulatory = self._regulatory_score(inp)

        composite = _clamp(
            bias       * 0.30
            + privacy  * 0.25
            + ethics   * 0.25
            + regulatory * 0.20
        )
        composite = round(composite, 1)

        risk     = self._classify_risk(composite)
        severity = self._classify_severity(composite)
        pattern  = self._classify_pattern(inp)
        action   = self._recommended_action(risk, pattern)

        has_compliance_flag = (
            composite >= 40
            or inp.right_to_erasure_violations >= 1
            or inp.decision_bias_score >= 0.35
        )
        requires_immediate_review = (
            composite >= 25
            or inp.audit_finding_count >= 2
            or inp.cross_border_transfer_violations >= 1
        )

        estimated_liability_index = round(
            min(composite / 100 * (1 - inp.model_fairness_score + 0.01) * 10, 10.0), 2
        )

        result = ComplianceResult(
            agent_id=inp.agent_id,
            region=inp.region,
            compliance_risk=risk,
            compliance_pattern=pattern,
            compliance_severity=severity,
            recommended_action=action,
            bias_score=bias,
            privacy_score=privacy,
            ethics_score=ethics,
            regulatory_score=regulatory,
            compliance_composite=composite,
            has_compliance_flag=has_compliance_flag,
            requires_immediate_review=requires_immediate_review,
            estimated_liability_index=estimated_liability_index,
            compliance_signal=self._signal(composite, inp),
        )
        self._results.append(result)
        return result

    def assess_batch(
        self, inputs: list[ComplianceInput]
    ) -> list[ComplianceResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total":                        0,
                "risk_counts":                  {},
                "pattern_counts":               {},
                "severity_counts":              {},
                "action_counts":                {},
                "avg_compliance_composite":     0.0,
                "compliance_flag_count":        0,
                "immediate_review_count":       0,
                "avg_bias_score":               0.0,
                "avg_privacy_score":            0.0,
                "avg_ethics_score":             0.0,
                "avg_regulatory_score":         0.0,
                "avg_estimated_liability_index": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_bias = total_priv = total_eth = total_reg = total_liab = 0.0
        flag_count = review_count = 0

        for r in self._results:
            risk_counts[r.compliance_risk.value]       = risk_counts.get(r.compliance_risk.value, 0) + 1
            pattern_counts[r.compliance_pattern.value] = pattern_counts.get(r.compliance_pattern.value, 0) + 1
            severity_counts[r.compliance_severity.value] = severity_counts.get(r.compliance_severity.value, 0) + 1
            action_counts[r.recommended_action.value]  = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp  += r.compliance_composite
            total_bias  += r.bias_score
            total_priv  += r.privacy_score
            total_eth   += r.ethics_score
            total_reg   += r.regulatory_score
            total_liab  += r.estimated_liability_index
            if r.has_compliance_flag:
                flag_count += 1
            if r.requires_immediate_review:
                review_count += 1

        n = len(self._results)
        return {
            "total":                         n,
            "risk_counts":                   risk_counts,
            "pattern_counts":                pattern_counts,
            "severity_counts":               severity_counts,
            "action_counts":                 action_counts,
            "avg_compliance_composite":      round(total_comp / n, 1),
            "compliance_flag_count":         flag_count,
            "immediate_review_count":        review_count,
            "avg_bias_score":                round(total_bias / n, 1),
            "avg_privacy_score":             round(total_priv / n, 1),
            "avg_ethics_score":              round(total_eth  / n, 1),
            "avg_regulatory_score":          round(total_reg  / n, 1),
            "avg_estimated_liability_index": round(total_liab / n, 2),
        }
