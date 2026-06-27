from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class OceanPlasticInput:
    entity_id: str
    ocean_zone: str
    region: str
    plastic_concentration: float
    microplastic_density: float
    macroplastic_accumulation: float
    marine_biodiversity_loss: float
    coral_reef_damage: float
    fisheries_contamination: float
    human_health_exposure: float
    cleanup_effectiveness: float
    corporate_accountability: float
    policy_enforcement: float
    recycling_rate: float
    single_use_reduction: float
    circular_economy_adoption: float
    coastal_management: float
    treaty_compliance: float
    innovation_investment: float
    community_action: float


@dataclass
class OceanPlasticResult:
    entity_id: str
    ocean_zone: str
    region: str
    pollution_score: float
    ecosystem_score: float
    governance_score: float
    health_score: float
    composite_score: float
    risk_level: str
    ocean_pattern: str
    severity: str
    recommended_action: str
    signal: str
    plastic_concentration: float
    microplastic_density: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "ocean_zone": self.ocean_zone,
            "region": self.region,
            "pollution_score": self.pollution_score,
            "ecosystem_score": self.ecosystem_score,
            "governance_score": self.governance_score,
            "health_score": self.health_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "ocean_pattern": self.ocean_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "plastic_concentration": self.plastic_concentration,
            "microplastic_density": self.microplastic_density,
        }


def _pollution_score(e: OceanPlasticInput) -> float:
    raw = (
        e.plastic_concentration * 0.4
        + e.microplastic_density * 0.35
        + e.macroplastic_accumulation * 0.25
    ) * 100
    return round(raw * 100) / 100


def _ecosystem_score(e: OceanPlasticInput) -> float:
    raw = (
        e.marine_biodiversity_loss * 0.4
        + e.coral_reef_damage * 0.35
        + e.fisheries_contamination * 0.25
    ) * 100
    return round(raw * 100) / 100


def _governance_score(e: OceanPlasticInput) -> float:
    raw = (
        e.corporate_accountability * 0.4
        + e.policy_enforcement * 0.35
        + e.treaty_compliance * 0.25
    ) * 100
    return round(raw * 100) / 100


def _health_score(e: OceanPlasticInput) -> float:
    raw = (
        e.human_health_exposure * 0.4
        + e.cleanup_effectiveness * 0.35
        + e.community_action * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    pollution: float,
    ecosystem: float,
    governance: float,
    health: float,
) -> float:
    return round(
        (pollution * 0.30 + ecosystem * 0.25 + governance * 0.25 + health * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _ocean_pattern(e: OceanPlasticInput) -> str:
    if e.plastic_concentration > 0.85 and e.microplastic_density > 0.80:
        return "great_garbage_patch_expansion"
    if e.microplastic_density > 0.85 and e.fisheries_contamination > 0.80:
        return "microplastic_food_chain_collapse"
    if e.coral_reef_damage > 0.85 and e.marine_biodiversity_loss > 0.80:
        return "coastal_ecosystem_destruction"
    if e.corporate_accountability > 0.80 and e.policy_enforcement > 0.75:
        return "corporate_plastic_impunity"
    if e.treaty_compliance > 0.80 and e.single_use_reduction > 0.75:
        return "treaty_governance_failure"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_plastique_océanique_systémique"
    if composite >= 40:
        return "crise_écosystème_marin_majeure"
    if composite >= 20:
        return "contamination_plastique_structurelle"
    return "surveillance_débris_marins_active"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_dépollution_océanique_critique"
    if risk == "high":
        return "mobilisation_accélérée_nettoyage_zones_vulnérables"
    if risk == "moderate":
        return "renforcement_politiques_réduction_plastique"
    return "veille_contamination_plastique_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise plastique océanique systémique — écosystèmes marins en péril"
    if risk == "high":
        return "🟠 Crise écosystème marin majeure détectée"
    if risk == "moderate":
        return "🟡 Contamination plastique structurelle active"
    return "🟢 Surveillance débris marins active"


def analyze_ocean_plastic(e: OceanPlasticInput) -> OceanPlasticResult:
    pollution = _pollution_score(e)
    ecosystem = _ecosystem_score(e)
    governance = _governance_score(e)
    health = _health_score(e)
    composite = _composite_score(pollution, ecosystem, governance, health)
    risk = _risk_level(composite)
    pattern = _ocean_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return OceanPlasticResult(
        entity_id=e.entity_id,
        ocean_zone=e.ocean_zone,
        region=e.region,
        pollution_score=pollution,
        ecosystem_score=ecosystem,
        governance_score=governance,
        health_score=health,
        composite_score=composite,
        risk_level=risk,
        ocean_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        plastic_concentration=e.plastic_concentration,
        microplastic_density=e.microplastic_density,
    )


class OceanPlasticEngine:
    def analyze(self, entities: List[OceanPlasticInput]) -> Dict[str, Any]:
        results = [analyze_ocean_plastic(e) for e in entities]

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
            pattern_distribution[r.ocean_pattern] = pattern_distribution.get(r.ocean_pattern, 0) + 1
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

        return self.summary(
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

    def summary(
        self,
        results: List[OceanPlasticResult] = None,
        risk_distribution: Dict[str, int] = None,
        pattern_distribution: Dict[str, int] = None,
        severity_distribution: Dict[str, int] = None,
        action_distribution: Dict[str, int] = None,
        avg_composite: float = 0.0,
        critical_count: int = 0,
        high_count: int = 0,
        moderate_count: int = 0,
        low_count: int = 0,
    ) -> Dict[str, Any]:
        results = results or []
        return {
            "module_id": 402,
            "module_name": "Pollution Plastique Océanique & Débris Marins Intelligence Engine",
            "total": len(results),
            "critical": critical_count,
            "high": high_count,
            "moderate": moderate_count,
            "low": low_count,
            "avg_composite": avg_composite,
            "pattern_distribution": pattern_distribution or {},
            "risk_distribution": risk_distribution or {},
            "severity_distribution": severity_distribution or {},
            "action_distribution": action_distribution or {},
            "avg_estimated_ocean_plastic_index": round(avg_composite / 100 * 10, 2),
        }
