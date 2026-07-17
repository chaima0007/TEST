"""
Module 377 — Gene Drive & Extinction Technology Intelligence Engine
Caelum Partners Swarm Intelligence — © Chaima Mhadbi, Fondatrice Caelum Partners, Bruxelles
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class GeneDriveInput:
    entity_id: str
    organism_type: str
    region: str
    extinction_drive_capability: float
    ecological_cascade_risk: float
    containment_failure_probability: float
    weaponization_risk: float
    regulatory_governance_gap: float
    accidental_release_risk: float
    gene_drive_proliferation: float
    species_targeting_precision: float
    cross_species_transfer: float
    irreversibility_level: float
    agricultural_disruption: float
    biodiversity_collapse_risk: float
    biosecurity_gap: float
    dual_use_intensity: float
    international_monitoring_failure: float
    natural_ecosystem_invasion: float
    democratic_consent_failure: float


@dataclass
class GeneDriveResult:
    entity_id: str
    organism_type: str
    region: str
    extinction_score: float
    containment_score: float
    governance_score: float
    weaponization_score: float
    composite_score: float
    risk_level: str
    gene_drive_pattern: str
    severity: str
    recommended_action: str
    signal: str
    extinction_drive_capability: float
    ecological_cascade_risk: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "organism_type": self.organism_type,
            "region": self.region,
            "extinction_score": self.extinction_score,
            "containment_score": self.containment_score,
            "governance_score": self.governance_score,
            "weaponization_score": self.weaponization_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "gene_drive_pattern": self.gene_drive_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "extinction_drive_capability": self.extinction_drive_capability,
            "ecological_cascade_risk": self.ecological_cascade_risk,
        }


def _extinction_score(e: GeneDriveInput) -> float:
    raw = (
        e.extinction_drive_capability * 0.40
        + e.ecological_cascade_risk * 0.35
        + e.biodiversity_collapse_risk * 0.25
    ) * 100
    return round(raw * 100) / 100


def _containment_score(e: GeneDriveInput) -> float:
    raw = (
        e.containment_failure_probability * 0.40
        + e.accidental_release_risk * 0.35
        + e.cross_species_transfer * 0.25
    ) * 100
    return round(raw * 100) / 100


def _governance_score(e: GeneDriveInput) -> float:
    raw = (
        e.regulatory_governance_gap * 0.40
        + e.international_monitoring_failure * 0.35
        + e.democratic_consent_failure * 0.25
    ) * 100
    return round(raw * 100) / 100


def _weaponization_score(e: GeneDriveInput) -> float:
    raw = (
        e.weaponization_risk * 0.40
        + e.dual_use_intensity * 0.35
        + e.biosecurity_gap * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    extinction: float,
    containment: float,
    governance: float,
    weaponization: float,
) -> float:
    return round(
        (extinction * 0.30 + containment * 0.25 + governance * 0.25 + weaponization * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _gene_drive_pattern(e: GeneDriveInput) -> str:
    if e.extinction_drive_capability > 0.85 and e.ecological_cascade_risk > 0.80:
        return "mass_extinction_cascade"
    if e.containment_failure_probability > 0.85 and e.accidental_release_risk > 0.80:
        return "containment_breach_catastrophe"
    if e.weaponization_risk > 0.85 and e.dual_use_intensity > 0.80:
        return "gene_drive_bioweapon"
    if e.regulatory_governance_gap > 0.80 and e.international_monitoring_failure > 0.75:
        return "governance_monitoring_void"
    if e.irreversibility_level > 0.80 and e.natural_ecosystem_invasion > 0.75:
        return "irreversible_ecosystem_invasion"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "extinction_écosystémique_catastrophique"
    if composite >= 40:
        return "crise_gene_drive_majeure"
    if composite >= 20:
        return "risque_gene_drive_structurel"
    return "gene_drive_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_extinction_urgence_mondiale"
    if risk == "high":
        return "confinement_gene_drive_urgence"
    if risk == "moderate":
        return "renforcement_gouvernance_gene_drive"
    return "veille_gene_drive_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Extinction systémique — technologie gene drive hors contrôle"
    if risk == "high":
        return "🟠 Crise gene drive majeure — risque écosystémique élevé"
    if risk == "moderate":
        return "🟡 Risque gene drive structurel — surveillance renforcée requise"
    return "🟢 Gene drive sous surveillance — confinement et gouvernance opérationnels"


def analyze_gene_drive(e: GeneDriveInput) -> GeneDriveResult:
    extinction = _extinction_score(e)
    containment = _containment_score(e)
    governance = _governance_score(e)
    weaponization = _weaponization_score(e)
    composite = _composite_score(extinction, containment, governance, weaponization)
    risk = _risk_level(composite)
    pattern = _gene_drive_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return GeneDriveResult(
        entity_id=e.entity_id,
        organism_type=e.organism_type,
        region=e.region,
        extinction_score=extinction,
        containment_score=containment,
        governance_score=governance,
        weaponization_score=weaponization,
        composite_score=composite,
        risk_level=risk,
        gene_drive_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        extinction_drive_capability=e.extinction_drive_capability,
        ecological_cascade_risk=e.ecological_cascade_risk,
    )


class GeneDriveEngine:
    def analyze(self, entities: List[GeneDriveInput]) -> Dict[str, Any]:
        results = [analyze_gene_drive(e) for e in entities]

        risk_distribution: Dict[str, int] = {}
        pattern_distribution: Dict[str, int] = {}
        severity_distribution: Dict[str, int] = {}
        action_distribution: Dict[str, int] = {}

        total_composite = 0.0
        critical_count = 0
        high_count = 0
        moderate_count = 0
        low_count = 0

        for r in results:
            risk_distribution[r.risk_level] = risk_distribution.get(r.risk_level, 0) + 1
            pattern_distribution[r.gene_drive_pattern] = pattern_distribution.get(r.gene_drive_pattern, 0) + 1
            severity_distribution[r.severity] = severity_distribution.get(r.severity, 0) + 1
            action_distribution[r.recommended_action] = action_distribution.get(r.recommended_action, 0) + 1
            total_composite += r.composite_score
            if r.risk_level == "critical":
                critical_count += 1
            elif r.risk_level == "high":
                high_count += 1
            elif r.risk_level == "moderate":
                moderate_count += 1
            else:
                low_count += 1

        n = len(results) or 1
        avg_composite = round(total_composite / n * 10) / 10

        return self._summary(
            results=results,
            risk_distribution=risk_distribution,
            pattern_distribution=pattern_distribution,
            severity_distribution=severity_distribution,
            action_distribution=action_distribution,
            avg_composite=avg_composite,
            critical_count=critical_count,
            high_count=high_count,
            moderate_count=moderate_count,
            low_count=low_count,
        )

    def _summary(
        self,
        results: List[GeneDriveResult],
        risk_distribution: Dict[str, int],
        pattern_distribution: Dict[str, int],
        severity_distribution: Dict[str, int],
        action_distribution: Dict[str, int],
        avg_composite: float,
        critical_count: int,
        high_count: int,
        moderate_count: int,
        low_count: int,
    ) -> Dict[str, Any]:
        return {
            "module_id": 377,
            "module_name": "Gene Drive & Extinction Technology Intelligence Engine",
            "total": len(results),
            "critical": critical_count,
            "high": high_count,
            "moderate": moderate_count,
            "low": low_count,
            "avg_composite": avg_composite,
            "pattern_distribution": pattern_distribution,
            "risk_distribution": risk_distribution,
            "severity_distribution": severity_distribution,
            "action_distribution": action_distribution,
            "avg_estimated_gene_drive_risk_index": round(avg_composite / 100 * 10, 2),
        }

    def summary(self, entities: List[GeneDriveInput]) -> Dict[str, Any]:
        return self.analyze(entities)
