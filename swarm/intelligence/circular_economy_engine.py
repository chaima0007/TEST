"""
Module 329 — Circular Economy & Regenerative Business Intelligence Engine
Caelum Partners Swarm Intelligence — Propriété exclusive de Chaima Mhadbi
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class CircularEconomyInput:
    entity_id: str
    economy_sector: str
    region: str
    # 17 float fields 0-1
    material_circularity_rate: float
    waste_generation_index: float
    resource_efficiency_score: float
    product_lifecycle_extension: float
    regenerative_business_model_adoption: float
    supply_loop_closure_rate: float
    industrial_symbiosis_level: float
    consumer_circular_behavior: float
    repair_reuse_accessibility: float
    circular_financing_availability: float
    regulatory_circular_support: float
    linear_economy_lock_in: float
    circular_innovation_pipeline: float
    carbon_circularity_coupling: float
    biodiversity_regeneration_index: float
    social_circular_equity: float
    systemic_circular_transition_readiness: float


def _material_score(e: CircularEconomyInput) -> float:
    raw = (
        e.material_circularity_rate * 0.4
        + e.resource_efficiency_score * 0.35
        + e.supply_loop_closure_rate * 0.25
    ) * 100
    return round(raw * 100) / 100


def _regeneration_score(e: CircularEconomyInput) -> float:
    raw = (
        e.regenerative_business_model_adoption * 0.4
        + e.industrial_symbiosis_level * 0.35
        + e.circular_innovation_pipeline * 0.25
    ) * 100
    return round(raw * 100) / 100


def _behavior_score(e: CircularEconomyInput) -> float:
    raw = (
        e.consumer_circular_behavior * 0.4
        + e.repair_reuse_accessibility * 0.35
        + e.circular_financing_availability * 0.25
    ) * 100
    return round(raw * 100) / 100


def _system_score(e: CircularEconomyInput) -> float:
    raw = (
        e.systemic_circular_transition_readiness * 0.4
        + e.regulatory_circular_support * 0.35
        + e.biodiversity_regeneration_index * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(material: float, regeneration: float, behavior: float, system: float) -> float:
    return round((material * 0.30 + regeneration * 0.25 + behavior * 0.25 + system * 0.20) * 100) / 100


def _risk_level(composite: float) -> str:
    # Inverted: LOW circularity = HIGH risk
    if composite < 40:
        return "critical"
    if composite < 60:
        return "high"
    if composite < 80:
        return "moderate"
    return "low"


def _circular_pattern(e: CircularEconomyInput) -> str:
    if e.material_circularity_rate < 0.35 and e.linear_economy_lock_in > 0.65:
        return "linear_lock_in"
    if e.waste_generation_index > 0.70 and e.supply_loop_closure_rate < 0.35:
        return "waste_crisis"
    if e.regenerative_business_model_adoption < 0.35 and e.biodiversity_regeneration_index < 0.35:
        return "regeneration_collapse"
    if e.social_circular_equity < 0.35 and e.repair_reuse_accessibility < 0.40:
        return "circular_inequality"
    if e.systemic_circular_transition_readiness < 0.35 and e.regulatory_circular_support < 0.40:
        return "systemic_inertia"
    return "none"


def _severity(risk: str) -> str:
    return {
        "critical": "effondrement_circulaire",
        "high":     "transition_bloquée",
        "moderate": "inertie_structurelle",
        "low":      "transition_engagée",
    }[risk]


def _recommended_action(risk: str) -> str:
    return {
        "critical": "activation_protocole_transition_d_urgence",
        "high":     "restructuration_modèle_économique",
        "moderate": "accélération_leviers_circulaires",
        "low":      "optimisation_continue",
    }[risk]


def _signal(risk: str) -> str:
    return {
        "critical": "🔴 Économie linéaire dominante — risque systémique circulaire",
        "high":     "🟠 Blocages structurels — transition incomplète",
        "moderate": "🟡 Transition en cours — inertie résiduelle",
        "low":      "🟢 Circularité avancée — modèle régénératif",
    }[risk]


def analyze_entity(e: CircularEconomyInput) -> Dict[str, Any]:
    material = _material_score(e)
    regeneration = _regeneration_score(e)
    behavior = _behavior_score(e)
    system = _system_score(e)
    comp = _composite(material, regeneration, behavior, system)
    risk = _risk_level(comp)
    pattern = _circular_pattern(e)
    severity = _severity(risk)
    action = _recommended_action(risk)
    sig = _signal(risk)

    # to_dict() returns exactly 15 keys
    return {
        "entity_id": e.entity_id,
        "economy_sector": e.economy_sector,
        "region": e.region,
        "material_score": material,
        "regeneration_score": regeneration,
        "behavior_score": behavior,
        "system_score": system,
        "composite_score": comp,
        "risk_level": risk,
        "circular_pattern": pattern,
        "severity": severity,
        "recommended_action": action,
        "signal": sig,
        "product_lifecycle_extension": e.product_lifecycle_extension,
        "carbon_circularity_coupling": e.carbon_circularity_coupling,
    }


class CircularEconomyEngine:
    def run(self, inputs: List[CircularEconomyInput]) -> Dict[str, Any]:
        entities = [analyze_entity(e) for e in inputs]

        risk_distribution: Dict[str, int] = {}
        pattern_distribution: Dict[str, int] = {}
        severity_distribution: Dict[str, int] = {}
        action_distribution: Dict[str, int] = {}

        total_composite = 0.0
        critical_count = 0
        high_count = 0
        moderate_count = 0
        low_count = 0

        for ent in entities:
            r = ent["risk_level"]
            risk_distribution[r] = risk_distribution.get(r, 0) + 1
            pattern_distribution[ent["circular_pattern"]] = pattern_distribution.get(ent["circular_pattern"], 0) + 1
            severity_distribution[ent["severity"]] = severity_distribution.get(ent["severity"], 0) + 1
            action_distribution[ent["recommended_action"]] = action_distribution.get(ent["recommended_action"], 0) + 1
            total_composite += ent["composite_score"]
            if r == "critical":
                critical_count += 1
            elif r == "high":
                high_count += 1
            elif r == "moderate":
                moderate_count += 1
            else:
                low_count += 1

        n = len(entities)
        avg_composite = round(total_composite / n * 100) / 100 if n else 0.0
        # summary() returns exactly 13 keys
        summary = {
            "module_id": 329,
            "module_name": "Circular Economy & Regenerative Business Intelligence Engine",
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
            "avg_estimated_circularity_index": round(avg_composite / 100 * 10, 2),
        }

        return {"entities": entities, "summary": summary}
