"""
Module 302 — Synthetic Biology Risk & Biosecurity Intelligence Engine
Caelum Partners Swarm Intelligence — © Chaima Mhadbi, Fondatrice Caelum Partners, Bruxelles
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class SyntheticBiologyRiskInput:
    entity_id: str
    bio_domain: str
    region: str
    pathogen_engineering_capability: float
    dual_use_research_exposure: float
    containment_protocol_quality: float
    biosurveillance_coverage: float
    bioweapon_proliferation_risk: float
    lab_safety_compliance: float
    international_treaty_adherence: float
    pandemic_preparedness_index: float
    gene_drive_deployment_risk: float
    biosecurity_governance_maturity: float
    academic_biosecurity_culture: float
    emerging_pathogen_monitoring: float
    biodefense_investment_rate: float
    supply_chain_bio_vulnerability: float
    synthetic_pathogen_detectability: float
    public_health_response_speed: float
    biosecurity_intelligence_coverage: float


@dataclass
class SyntheticBiologyRiskResult:
    entity_id: str
    region: str
    bio_domain: str
    bio_risk: str
    bio_pattern: str
    bio_severity: str
    recommended_action: str
    containment_score: float
    proliferation_score: float
    governance_score: float
    preparedness_score: float
    bio_composite: float
    is_in_bio_crisis: bool
    requires_bio_intervention: bool
    bio_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "bio_domain": self.bio_domain,
            "bio_risk": self.bio_risk,
            "bio_pattern": self.bio_pattern,
            "bio_severity": self.bio_severity,
            "recommended_action": self.recommended_action,
            "containment_score": self.containment_score,
            "proliferation_score": self.proliferation_score,
            "governance_score": self.governance_score,
            "preparedness_score": self.preparedness_score,
            "bio_composite": self.bio_composite,
            "is_in_bio_crisis": self.is_in_bio_crisis,
            "requires_bio_intervention": self.requires_bio_intervention,
            "bio_signal": self.bio_signal,
        }


def _containment_score(inp: SyntheticBiologyRiskInput) -> float:
    raw = (
        (1 - inp.containment_protocol_quality) * 0.4
        + (1 - inp.lab_safety_compliance) * 0.35
        + (1 - inp.biosurveillance_coverage) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _proliferation_score(inp: SyntheticBiologyRiskInput) -> float:
    raw = (
        inp.bioweapon_proliferation_risk * 0.4
        + inp.dual_use_research_exposure * 0.35
        + inp.pathogen_engineering_capability * 0.25
    ) * 100
    return round(raw * 100) / 100


def _governance_score(inp: SyntheticBiologyRiskInput) -> float:
    raw = (
        (1 - inp.biosecurity_governance_maturity) * 0.4
        + (1 - inp.international_treaty_adherence) * 0.35
        + (1 - inp.academic_biosecurity_culture) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _preparedness_score(inp: SyntheticBiologyRiskInput) -> float:
    raw = (
        (1 - inp.pandemic_preparedness_index) * 0.4
        + (1 - inp.public_health_response_speed) * 0.35
        + (1 - inp.biodefense_investment_rate) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(containment: float, proliferation: float, governance: float, preparedness: float) -> float:
    raw = (
        containment * 0.30
        + proliferation * 0.25
        + governance * 0.25
        + preparedness * 0.20
    )
    return round(raw * 100) / 100


def _bio_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _bio_pattern(inp: SyntheticBiologyRiskInput) -> str:
    if inp.bioweapon_proliferation_risk >= 0.65 and (1 - inp.international_treaty_adherence) >= 0.55:
        return "bioweapon_proliferation"
    if (1 - inp.lab_safety_compliance) >= 0.65 and inp.pathogen_engineering_capability >= 0.60:
        return "lab_leak_risk"
    if (1 - inp.biosurveillance_coverage) >= 0.65 and (1 - inp.emerging_pathogen_monitoring) >= 0.60:
        return "surveillance_blindspot"
    if (1 - inp.pandemic_preparedness_index) >= 0.70 and (1 - inp.public_health_response_speed) >= 0.60:
        return "pandemic_unpreparedness"
    if inp.gene_drive_deployment_risk >= 0.70 and (1 - inp.biosecurity_governance_maturity) >= 0.60:
        return "gene_drive_risk"
    return "none"


def _bio_severity(composite: float) -> str:
    if composite >= 75:
        return "biosecurity_emergency"
    if composite >= 50:
        return "high_bio_risk"
    if composite >= 25:
        return "bio_stress"
    return "biosecure"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "biosecurity_emergency_response"
    if risk == "high" and pattern == "bioweapon_proliferation":
        return "bioweapon_interdiction"
    if risk == "high":
        return "biosecurity_reinforcement"
    if risk == "moderate":
        return "bio_monitoring"
    return "no_action"


def _bio_signal(inp: SyntheticBiologyRiskInput, risk: str, composite: float) -> str:
    if risk == "critical":
        return (
            f"Critique — risque prolifération bioarmes {int(inp.bioweapon_proliferation_risk * 100)}% "
            f"— qualité confinement {int(inp.containment_protocol_quality * 100)}% "
            f"— composite {int(composite)}"
        )
    if risk == "high":
        return (
            f"Élevé — couverture biosurveillance {int(inp.biosurveillance_coverage * 100)}% "
            f"— préparation pandémique {int(inp.pandemic_preparedness_index * 100)}% "
            f"— composite {int(composite)}"
        )
    if risk == "moderate":
        return (
            f"Modéré — exposition recherche double usage {int(inp.dual_use_research_exposure * 100)}% "
            f"— composite {int(composite)}"
        )
    return "Biosécurité optimale — confinement rigoureux, gouvernance mature, préparation pandémique solide"


def analyse(inp: SyntheticBiologyRiskInput) -> SyntheticBiologyRiskResult:
    containment = _containment_score(inp)
    proliferation = _proliferation_score(inp)
    governance = _governance_score(inp)
    preparedness = _preparedness_score(inp)
    composite = _composite(containment, proliferation, governance, preparedness)
    risk = _bio_risk(composite)
    pattern = _bio_pattern(inp)
    severity = _bio_severity(composite)
    action = _recommended_action(risk, pattern)
    signal = _bio_signal(inp, risk, composite)
    return SyntheticBiologyRiskResult(
        entity_id=inp.entity_id,
        region=inp.region,
        bio_domain=inp.bio_domain,
        bio_risk=risk,
        bio_pattern=pattern,
        bio_severity=severity,
        recommended_action=action,
        containment_score=containment,
        proliferation_score=proliferation,
        governance_score=governance,
        preparedness_score=preparedness,
        bio_composite=composite,
        is_in_bio_crisis=composite >= 60,
        requires_bio_intervention=composite >= 40,
        bio_signal=signal,
    )


class SyntheticBiologyRiskEngine:
    def run(self, inputs: List[SyntheticBiologyRiskInput]) -> Dict[str, Any]:
        results = [analyse(inp) for inp in inputs]
        dicts = [r.to_dict() for r in results]

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}
        total_composite = 0.0
        total_containment = 0.0
        total_proliferation = 0.0
        total_governance = 0.0
        total_preparedness = 0.0
        bio_crisis_count = 0
        bio_intervention_count = 0

        for r in results:
            risk_counts[r.bio_risk] = risk_counts.get(r.bio_risk, 0) + 1
            pattern_counts[r.bio_pattern] = pattern_counts.get(r.bio_pattern, 0) + 1
            severity_counts[r.bio_severity] = severity_counts.get(r.bio_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1
            total_composite += r.bio_composite
            total_containment += r.containment_score
            total_proliferation += r.proliferation_score
            total_governance += r.governance_score
            total_preparedness += r.preparedness_score
            if r.is_in_bio_crisis:
                bio_crisis_count += 1
            if r.requires_bio_intervention:
                bio_intervention_count += 1

        n = len(results) or 1
        avg_composite = total_composite / n

        summary = {
            "total": len(results),
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_bio_composite": round(avg_composite * 10) / 10,
            "bio_crisis_count": bio_crisis_count,
            "bio_intervention_count": bio_intervention_count,
            "avg_containment_score": round(total_containment / n * 10) / 10,
            "avg_proliferation_score": round(total_proliferation / n * 10) / 10,
            "avg_governance_score": round(total_governance / n * 10) / 10,
            "avg_preparedness_score": round(total_preparedness / n * 10) / 10,
            "avg_estimated_bio_risk_index": round(avg_composite / 100 * 10, 2),
        }

        return {"entities": dicts, "summary": summary}
