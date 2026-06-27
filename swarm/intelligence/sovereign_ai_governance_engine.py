"""
Sovereign AI Governance & Alignment Audit Engine
Caelum Partners — Audit des frameworks de gouvernance IA, alignement des modèles,
et conformité souveraine à travers les systèmes déployés.
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class AIGovernanceInput:
    system_id: str
    ai_domain: str  # generative_llm | autonomous_agent | decision_engine | computer_vision
                    # predictive_model | reinforcement_agent | biometric_system | swarm_intelligence
    region: str

    # Alignment & safety
    alignment_score: float                    # 0.0–1.0
    autonomous_decision_risk: float           # 0.0–1.0  higher = worse
    model_drift_detection_capability: float   # 0.0–1.0

    # Transparency
    explainability_score: float               # 0.0–1.0
    model_transparency_index: float           # 0.0–1.0
    algorithmic_accountability_score: float   # 0.0–1.0

    # Compliance
    regulatory_ai_compliance: float           # 0.0–1.0
    ethical_review_frequency: float           # 0.0–1.0
    bias_audit_completeness: float            # 0.0–1.0

    # Sovereignty
    sovereignty_preservation_score: float     # 0.0–1.0
    human_oversight_level: float              # 0.0–1.0
    ai_incident_response_maturity: float      # 0.0–1.0

    # Additional governance fields
    data_provenance_clarity: float            # 0.0–1.0
    adversarial_robustness_score: float       # 0.0–1.0
    ai_rights_framework_clarity: float        # 0.0–1.0
    unintended_consequence_monitoring: float  # 0.0–1.0
    stakeholder_consent_coverage: float       # 0.0–1.0


def _inv(v: float) -> float:
    """Invert a 0–1 score so that higher original value → lower risk contribution."""
    return 1.0 - v


def _alignment_risk_score(inp: AIGovernanceInput) -> float:
    """0.30 weight — higher = more misaligned/risky."""
    return (
        _inv(inp.alignment_score) * 0.40
        + inp.autonomous_decision_risk * 0.35
        + _inv(inp.model_drift_detection_capability) * 0.25
    )


def _transparency_score(inp: AIGovernanceInput) -> float:
    """0.25 weight — higher = more opaque."""
    return (
        _inv(inp.explainability_score) * 0.40
        + _inv(inp.model_transparency_index) * 0.35
        + _inv(inp.algorithmic_accountability_score) * 0.25
    )


def _compliance_score(inp: AIGovernanceInput) -> float:
    """0.25 weight — higher = less compliant."""
    return (
        _inv(inp.regulatory_ai_compliance) * 0.40
        + _inv(inp.ethical_review_frequency) * 0.35
        + _inv(inp.bias_audit_completeness) * 0.25
    )


def _sovereignty_score(inp: AIGovernanceInput) -> float:
    """0.20 weight — higher = weaker sovereignty."""
    return (
        _inv(inp.sovereignty_preservation_score) * 0.40
        + _inv(inp.human_oversight_level) * 0.35
        + _inv(inp.ai_incident_response_maturity) * 0.25
    )


def _composite(
    alignment: float,
    transparency: float,
    compliance: float,
    sovereignty: float,
) -> float:
    raw = (
        alignment   * 0.30
        + transparency * 0.25
        + compliance   * 0.25
        + sovereignty  * 0.20
    )
    return round(min(raw * 100, 100.0), 2)


def _governance_pattern(inp: AIGovernanceInput) -> str:
    if inp.alignment_score < 0.35 or inp.autonomous_decision_risk > 0.70:
        return "alignment_failure"
    if inp.explainability_score < 0.30 and inp.model_transparency_index < 0.30:
        return "opacity_crisis"
    if inp.regulatory_ai_compliance < 0.35 or inp.bias_audit_completeness < 0.30:
        return "regulatory_breach"
    if inp.sovereignty_preservation_score < 0.35 or inp.human_oversight_level < 0.30:
        return "sovereignty_erosion"
    if inp.bias_audit_completeness < 0.40 and inp.algorithmic_accountability_score < 0.40:
        return "bias_amplification"
    return "none"


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "misaligned"
    if composite >= 40:
        return "at_risk"
    if composite >= 20:
        return "monitored"
    return "aligned"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        if pattern == "alignment_failure":
            return "emergency_shutdown"
        return "alignment_reset"
    if risk == "high":
        if pattern == "bias_amplification":
            return "bias_remediation"
        return "governance_audit"
    if risk == "moderate":
        return "ai_monitoring"
    return "no_action"


def _governance_signal(inp: AIGovernanceInput, pattern: str, composite: float) -> str:
    if composite < 20:
        return (
            "Gouvernance IA exemplaire — alignement robuste, conformité souveraine assurée, "
            "contrôle humain effectif et transparence algorithmique validée"
        )
    labels: Dict[str, str] = {
        "alignment_failure":   "Échec d'alignement IA",
        "opacity_crisis":      "Crise d'opacité algorithmique",
        "regulatory_breach":   "Violation réglementaire IA",
        "sovereignty_erosion": "Érosion de la souveraineté IA",
        "bias_amplification":  "Amplification des biais",
    }
    label = labels.get(pattern, pattern.replace("_", " "))
    return (
        f"{label} — alignement {inp.alignment_score:.2f} — conformité {inp.regulatory_ai_compliance:.2f} "
        f"— explicabilité {inp.explainability_score:.2f} — souveraineté {inp.sovereignty_preservation_score:.2f} "
        f"— risque autonome {inp.autonomous_decision_risk:.2f} — composite {composite:.1f}"
    )


def _assess_single(inp: AIGovernanceInput) -> Dict[str, Any]:
    alignment   = _alignment_risk_score(inp)
    transparency = _transparency_score(inp)
    compliance  = _compliance_score(inp)
    sovereignty = _sovereignty_score(inp)
    composite   = _composite(alignment, transparency, compliance, sovereignty)
    pattern     = _governance_pattern(inp)
    risk        = _risk_level(composite)
    sev         = _severity(composite)
    action      = _recommended_action(risk, pattern)
    signal      = _governance_signal(inp, pattern, composite)

    return {
        "system_id":                         inp.system_id,
        "ai_domain":                         inp.ai_domain,
        "region":                            inp.region,
        "governance_risk":                   risk,
        "governance_pattern":                pattern,
        "governance_severity":               sev,
        "recommended_action":                action,
        "alignment_risk_score":              round(alignment * 100, 2),
        "transparency_score":                round(transparency * 100, 2),
        "compliance_score":                  round(compliance * 100, 2),
        "sovereignty_score":                 round(sovereignty * 100, 2),
        "governance_composite":              composite,
        "has_misalignment_signal":           composite >= 40 or inp.alignment_score < 0.45 or inp.autonomous_decision_risk > 0.60,
        "requires_immediate_intervention":   composite >= 25 or inp.regulatory_ai_compliance < 0.35 or inp.human_oversight_level < 0.30,
        "estimated_misalignment_severity_index": round(min(composite / 100 * (1 - inp.alignment_score + 0.01) * 10, 10.0), 2),
        "governance_signal":                 signal,
    }


class SovereignAIGovernanceEngine:

    def assess_batch(self, inputs: List[AIGovernanceInput]) -> List[Dict[str, Any]]:
        return [_assess_single(inp) for inp in inputs]

    def summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        n = len(results) or 1

        risk_counts:    Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:  Dict[str, int] = {}

        t_alignment = t_transparency = t_compliance = t_sovereignty = 0.0
        t_composite = t_gap = 0.0
        misalignment_count = intervention_count = 0

        for r in results:
            risk_counts[r["governance_risk"]]        = risk_counts.get(r["governance_risk"], 0) + 1
            pattern_counts[r["governance_pattern"]]  = pattern_counts.get(r["governance_pattern"], 0) + 1
            severity_counts[r["governance_severity"]] = severity_counts.get(r["governance_severity"], 0) + 1
            action_counts[r["recommended_action"]]   = action_counts.get(r["recommended_action"], 0) + 1

            t_alignment   += r["alignment_risk_score"]
            t_transparency += r["transparency_score"]
            t_compliance  += r["compliance_score"]
            t_sovereignty += r["sovereignty_score"]
            t_composite   += r["governance_composite"]
            t_gap         += r["estimated_misalignment_severity_index"]
            if r["has_misalignment_signal"]:
                misalignment_count += 1
            if r["requires_immediate_intervention"]:
                intervention_count += 1

        return {
            "total":                                    len(results),
            "risk_counts":                              risk_counts,
            "pattern_counts":                           pattern_counts,
            "severity_counts":                          severity_counts,
            "action_counts":                            action_counts,
            "avg_governance_composite":                 round(t_composite / n, 1),
            "misalignment_signal_count":                misalignment_count,
            "immediate_intervention_count":             intervention_count,
            "avg_alignment_risk_score":                 round(t_alignment / n, 1),
            "avg_transparency_score":                   round(t_transparency / n, 1),
            "avg_compliance_score":                     round(t_compliance / n, 1),
            "avg_sovereignty_score":                    round(t_sovereignty / n, 1),
            "avg_estimated_misalignment_severity_index": round(t_gap / n, 2),
        }


def to_dict(inp: AIGovernanceInput) -> Dict[str, Any]:
    """Serialise an AIGovernanceInput to exactly 15 keys."""
    return {
        "system_id":                          inp.system_id,
        "ai_domain":                          inp.ai_domain,
        "region":                             inp.region,
        "alignment_score":                    inp.alignment_score,
        "explainability_score":               inp.explainability_score,
        "bias_audit_completeness":            inp.bias_audit_completeness,
        "human_oversight_level":              inp.human_oversight_level,
        "autonomous_decision_risk":           inp.autonomous_decision_risk,
        "data_provenance_clarity":            inp.data_provenance_clarity,
        "model_drift_detection_capability":   inp.model_drift_detection_capability,
        "adversarial_robustness_score":       inp.adversarial_robustness_score,
        "regulatory_ai_compliance":           inp.regulatory_ai_compliance,
        "sovereignty_preservation_score":     inp.sovereignty_preservation_score,
        "stakeholder_consent_coverage":       inp.stakeholder_consent_coverage,
        "ai_incident_response_maturity":      inp.ai_incident_response_maturity,
    }
