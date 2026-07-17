from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class SpaceEconomyInput:
    entity_id: str
    space_sector: str
    region: str
    # 17 float fields (0-1)
    orbital_congestion_index: float
    space_debris_collision_risk: float
    launch_frequency_dominance: float
    satellite_dependency_vulnerability: float
    space_weaponization_level: float
    commercial_space_monopoly_risk: float
    space_resource_extraction_conflict: float
    regulatory_vacuum_exploitation: float
    space_sovereignty_erosion: float
    dual_use_technology_proliferation: float
    space_internet_dominance: float
    anti_satellite_capability: float
    space_supply_chain_fragility: float
    orbital_slot_competition: float
    space_insurance_systemic_risk: float
    low_earth_orbit_saturation: float
    cislunar_territorial_dispute: float


@dataclass
class SpaceEconomySovereigntyResult:
    entity_id: str
    space_sector: str
    region: str
    congestion_score: float
    militarization_score: float
    monopoly_score: float
    sovereignty_score: float
    composite_score: float
    risk_level: str
    space_pattern: str
    severity: str
    recommended_action: str
    signal: str
    orbital_congestion_index: float
    space_weaponization_level: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "space_sector": self.space_sector,
            "region": self.region,
            "congestion_score": self.congestion_score,
            "militarization_score": self.militarization_score,
            "monopoly_score": self.monopoly_score,
            "sovereignty_score": self.sovereignty_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "space_pattern": self.space_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "orbital_congestion_index": self.orbital_congestion_index,
            "space_weaponization_level": self.space_weaponization_level,
        }


def _compute_congestion_score(inp: SpaceEconomyInput) -> float:
    raw = (
        inp.orbital_congestion_index * 0.4
        + inp.space_debris_collision_risk * 0.35
        + inp.low_earth_orbit_saturation * 0.25
    ) * 100
    return round(raw, 2)


def _compute_militarization_score(inp: SpaceEconomyInput) -> float:
    raw = (
        inp.space_weaponization_level * 0.4
        + inp.anti_satellite_capability * 0.35
        + inp.dual_use_technology_proliferation * 0.25
    ) * 100
    return round(raw, 2)


def _compute_monopoly_score(inp: SpaceEconomyInput) -> float:
    raw = (
        inp.commercial_space_monopoly_risk * 0.4
        + inp.space_internet_dominance * 0.35
        + inp.launch_frequency_dominance * 0.25
    ) * 100
    return round(raw, 2)


def _compute_sovereignty_score(inp: SpaceEconomyInput) -> float:
    raw = (
        inp.space_sovereignty_erosion * 0.4
        + inp.regulatory_vacuum_exploitation * 0.35
        + inp.cislunar_territorial_dispute * 0.25
    ) * 100
    return round(raw, 2)


def _compute_composite(
    congestion: float,
    militarization: float,
    monopoly: float,
    sovereignty: float,
) -> float:
    return round(
        congestion * 0.30
        + militarization * 0.25
        + monopoly * 0.25
        + sovereignty * 0.20,
        2,
    )


def _get_risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _get_space_pattern(inp: SpaceEconomyInput) -> str:
    if inp.space_weaponization_level >= 0.70 and inp.anti_satellite_capability >= 0.65:
        return "orbital_warfare"
    if inp.orbital_congestion_index >= 0.70 and inp.space_debris_collision_risk >= 0.65:
        return "kessler_syndrome"
    if inp.commercial_space_monopoly_risk >= 0.70 and inp.space_internet_dominance >= 0.65:
        return "commercial_colonization"
    if inp.space_resource_extraction_conflict >= 0.70 and inp.cislunar_territorial_dispute >= 0.65:
        return "space_resource_war"
    if inp.regulatory_vacuum_exploitation >= 0.70 and inp.space_sovereignty_erosion >= 0.65:
        return "regulatory_vacuum_crisis"
    return "none"


def _get_severity(composite: float) -> str:
    if composite >= 60:
        return "crise_orbitale_systémique"
    if composite >= 40:
        return "escalade_spatiale_majeure"
    if composite >= 20:
        return "tension_orbitale"
    return "espace_stable"


def _get_recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_souveraineté_spatiale_urgente"
    if risk == "high":
        return "diplomatie_spatiale_activée"
    if risk == "moderate":
        return "surveillance_orbital_renforcée"
    return "monitoring_continu"


def _get_signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise orbitale systémique — espace sous tension extrême"
    if risk == "high":
        return "🟠 Escalade spatiale majeure détectée"
    if risk == "moderate":
        return "🟡 Tensions orbitales en développement"
    return "🟢 Environnement spatial stable"


def _analyze_entity(inp: SpaceEconomyInput) -> SpaceEconomySovereigntyResult:
    congestion = _compute_congestion_score(inp)
    militarization = _compute_militarization_score(inp)
    monopoly = _compute_monopoly_score(inp)
    sovereignty = _compute_sovereignty_score(inp)
    composite = _compute_composite(congestion, militarization, monopoly, sovereignty)
    risk = _get_risk_level(composite)
    pattern = _get_space_pattern(inp)
    severity = _get_severity(composite)
    action = _get_recommended_action(risk)
    signal = _get_signal(risk)

    return SpaceEconomySovereigntyResult(
        entity_id=inp.entity_id,
        space_sector=inp.space_sector,
        region=inp.region,
        congestion_score=congestion,
        militarization_score=militarization,
        monopoly_score=monopoly,
        sovereignty_score=sovereignty,
        composite_score=composite,
        risk_level=risk,
        space_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=signal,
        orbital_congestion_index=inp.orbital_congestion_index,
        space_weaponization_level=inp.space_weaponization_level,
    )


class SpaceEconomySovereigntyEngine:
    def __init__(self, inputs: List[SpaceEconomyInput]):
        self.inputs = inputs
        self.results: List[SpaceEconomySovereigntyResult] = [
            _analyze_entity(inp) for inp in inputs
        ]

    def summary(self) -> Dict[str, Any]:
        n = len(self.results)
        if n == 0:
            return {}

        pattern_distribution: Dict[str, int] = {}
        risk_distribution: Dict[str, int] = {}
        severity_distribution: Dict[str, int] = {}
        action_distribution: Dict[str, int] = {}

        critical_count = 0
        high_count = 0
        moderate_count = 0
        low_count = 0
        total_composite = 0.0

        for r in self.results:
            risk_distribution[r.risk_level] = risk_distribution.get(r.risk_level, 0) + 1
            pattern_distribution[r.space_pattern] = pattern_distribution.get(r.space_pattern, 0) + 1
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

        avg_composite = total_composite / n

        return {
            "module_id": 331,
            "module_name": "Space Economy & Orbital Sovereignty Intelligence Engine",
            "total_entities": n,
            "critical_count": critical_count,
            "high_count": high_count,
            "moderate_count": moderate_count,
            "low_count": low_count,
            "avg_composite": round(avg_composite, 2),
            "pattern_distribution": pattern_distribution,
            "risk_distribution": risk_distribution,
            "severity_distribution": severity_distribution,
            "action_distribution": action_distribution,
            "avg_estimated_orbital_risk_index": round(avg_composite / 100 * 10, 2),
        }
