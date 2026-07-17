"""
Module 347 — Rare Earth & Critical Materials Geopolitics Intelligence Engine
Caelum Partners Swarm Intelligence — Propriété exclusive de Chaima Mhadbi
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class RareEarthInput:
    entity_id: str
    material_category: str
    region: str
    supply_concentration_monopoly_risk: float
    critical_material_import_dependency: float
    mining_geopolitical_leverage: float
    processing_chokepoint_control: float
    strategic_reserve_depletion_rate: float
    conflict_mineral_sourcing_risk: float
    green_tech_material_demand_surge: float
    recycling_capacity_inadequacy: float
    substitute_material_unavailability: float
    export_restriction_weaponization_risk: float
    environmental_mining_collapse_risk: float
    labor_rights_mining_violation: float
    material_scarcity_technology_lock: float
    critical_material_price_volatility: float
    supply_chain_single_point_failure: float
    allied_mining_diversification_gap: float
    deep_sea_mining_regulatory_vacuum: float


def _supply_score(e: RareEarthInput) -> float:
    raw = (
        e.supply_concentration_monopoly_risk * 0.4
        + e.critical_material_import_dependency * 0.35
        + e.processing_chokepoint_control * 0.25
    ) * 100
    return round(raw * 100) / 100


def _geopolitical_score(e: RareEarthInput) -> float:
    raw = (
        e.mining_geopolitical_leverage * 0.4
        + e.export_restriction_weaponization_risk * 0.35
        + e.conflict_mineral_sourcing_risk * 0.25
    ) * 100
    return round(raw * 100) / 100


def _demand_score(e: RareEarthInput) -> float:
    raw = (
        e.green_tech_material_demand_surge * 0.4
        + e.material_scarcity_technology_lock * 0.35
        + e.substitute_material_unavailability * 0.25
    ) * 100
    return round(raw * 100) / 100


def _resilience_score(e: RareEarthInput) -> float:
    raw = (
        e.recycling_capacity_inadequacy * 0.4
        + e.supply_chain_single_point_failure * 0.35
        + e.allied_mining_diversification_gap * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(supply: float, geopolitical: float, demand: float, resilience: float) -> float:
    return round((supply * 0.30 + geopolitical * 0.25 + demand * 0.25 + resilience * 0.20) * 100) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _material_pattern(e: RareEarthInput) -> str:
    if e.supply_concentration_monopoly_risk >= 0.70 and e.processing_chokepoint_control >= 0.65:
        return "rare_earth_monopoly_crisis"
    if e.export_restriction_weaponization_risk >= 0.70 and e.mining_geopolitical_leverage >= 0.65:
        return "export_weapon_deployment"
    if e.green_tech_material_demand_surge >= 0.70 and e.substitute_material_unavailability >= 0.65:
        return "green_tech_material_crunch"
    if e.conflict_mineral_sourcing_risk >= 0.70 and e.labor_rights_mining_violation >= 0.65:
        return "conflict_mineral_cascade"
    if e.supply_chain_single_point_failure >= 0.70 and e.critical_material_import_dependency >= 0.65:
        return "supply_chain_collapse"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_matières_critiques_systémique"
    if composite >= 40:
        return "pénurie_stratégique_majeure"
    if composite >= 20:
        return "tension_approvisionnement_critique"
    return "approvisionnement_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "sécurisation_urgente_approvisionnements_critiques"
    if risk == "high":
        return "diversification_stratégique_accélérée"
    if risk == "moderate":
        return "renforcement_résilience_chaînes_approvisionnement"
    return "veille_matières_critiques_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise matières critiques systémique — dépendance stratégique extrême"
    if risk == "high":
        return "🟠 Pénurie stratégique majeure détectée"
    if risk == "moderate":
        return "🟡 Tension approvisionnement critique active"
    return "🟢 Approvisionnement matières critiques sous surveillance"


def _analyze(e: RareEarthInput) -> Dict[str, Any]:
    supply = _supply_score(e)
    geopolitical = _geopolitical_score(e)
    demand = _demand_score(e)
    resilience = _resilience_score(e)
    composite = _composite(supply, geopolitical, demand, resilience)
    risk = _risk_level(composite)
    pattern = _material_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    signal = _signal(risk)

    return {
        "entity_id": e.entity_id,
        "material_category": e.material_category,
        "region": e.region,
        "supply_score": supply,
        "geopolitical_score": geopolitical,
        "demand_score": demand,
        "resilience_score": resilience,
        "composite_score": composite,
        "risk_level": risk,
        "material_pattern": pattern,
        "severity": severity,
        "recommended_action": action,
        "signal": signal,
        "supply_concentration_monopoly_risk": e.supply_concentration_monopoly_risk,
        "export_restriction_weaponization_risk": e.export_restriction_weaponization_risk,
    }


class RareEarthIntelligenceEngine:
    def run(self, inputs: List[RareEarthInput]) -> Dict[str, Any]:
        entities = [_analyze(e) for e in inputs]

        risk_distribution: Dict[str, int] = {}
        pattern_distribution: Dict[str, int] = {}
        severity_distribution: Dict[str, int] = {}
        action_distribution: Dict[str, int] = {}

        critical_count = 0
        high_count = 0
        moderate_count = 0
        low_count = 0
        total_composite = 0.0

        for ent in entities:
            risk = ent["risk_level"]
            risk_distribution[risk] = risk_distribution.get(risk, 0) + 1
            pattern_distribution[ent["material_pattern"]] = pattern_distribution.get(ent["material_pattern"], 0) + 1
            severity_distribution[ent["severity"]] = severity_distribution.get(ent["severity"], 0) + 1
            action_distribution[ent["recommended_action"]] = action_distribution.get(ent["recommended_action"], 0) + 1
            total_composite += ent["composite_score"]

            if risk == "critical":
                critical_count += 1
            elif risk == "high":
                high_count += 1
            elif risk == "moderate":
                moderate_count += 1
            else:
                low_count += 1

        n = len(entities)
        avg_composite = round(total_composite / n * 10) / 10 if n else 0.0

        summary = {
            "module_id": 347,
            "module_name": "Rare Earth & Critical Materials Geopolitics Intelligence Engine",
            "total_entities": n,
            "critical_count": critical_count,
            "high_count": high_count,
            "moderate_count": moderate_count,
            "low_count": low_count,
            "avg_composite": avg_composite,
            "pattern_distribution": pattern_distribution,
            "risk_distribution": risk_distribution,
            "severity_distribution": severity_distribution,
            "action_distribution": action_distribution,
            "avg_estimated_material_risk_index": round(avg_composite / 100 * 10, 2),
        }

        return {"entities": entities, "summary": summary}
