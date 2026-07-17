"""
Module 341 — Cultural Capital & Heritage Destruction Intelligence Engine
Caelum Partners Swarm Intelligence — Propriété exclusive de Chaima Mhadbi
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class CulturalHeritageInput:
    entity_id: str
    cultural_domain: str
    region: str
    # 17 float fields 0-1
    heritage_physical_destruction_rate: float
    cultural_gentrification_displacement: float
    digital_colonialism_cultural_impact: float
    intangible_heritage_extinction_speed: float
    cultural_commodification_distortion: float
    AI_cultural_appropriation_risk: float
    conflict_cultural_targeting_index: float
    climate_cultural_heritage_threat: float
    tourism_overcrowding_degradation: float
    cultural_funding_collapse: float
    indigenous_cultural_sovereignty_erosion: float
    language_heritage_extinction_rate: float
    institutional_cultural_memory_loss: float
    global_brand_monoculture_dominance: float
    cultural_resistance_suppression: float
    diaspora_cultural_connection_severing: float
    generational_cultural_transmission_failure: float


def _destruction_score(e: CulturalHeritageInput) -> float:
    raw = (
        e.heritage_physical_destruction_rate * 0.4
        + e.conflict_cultural_targeting_index * 0.35
        + e.climate_cultural_heritage_threat * 0.25
    ) * 100
    return round(raw * 100) / 100


def _erosion_score(e: CulturalHeritageInput) -> float:
    raw = (
        e.intangible_heritage_extinction_speed * 0.4
        + e.language_heritage_extinction_rate * 0.35
        + e.generational_cultural_transmission_failure * 0.25
    ) * 100
    return round(raw * 100) / 100


def _commodification_score(e: CulturalHeritageInput) -> float:
    raw = (
        e.cultural_commodification_distortion * 0.4
        + e.global_brand_monoculture_dominance * 0.35
        + e.tourism_overcrowding_degradation * 0.25
    ) * 100
    return round(raw * 100) / 100


def _sovereignty_score(e: CulturalHeritageInput) -> float:
    raw = (
        e.indigenous_cultural_sovereignty_erosion * 0.4
        + e.cultural_resistance_suppression * 0.35
        + e.cultural_funding_collapse * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(destruction: float, erosion: float, commodification: float, sovereignty: float) -> float:
    return round(
        (destruction * 0.30 + erosion * 0.25 + commodification * 0.25 + sovereignty * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _cultural_pattern(e: CulturalHeritageInput) -> str:
    if e.heritage_physical_destruction_rate >= 0.70 and e.conflict_cultural_targeting_index >= 0.65:
        return "active_cultural_destruction"
    if e.intangible_heritage_extinction_speed >= 0.70 and e.generational_cultural_transmission_failure >= 0.65:
        return "intangible_heritage_collapse"
    if e.cultural_commodification_distortion >= 0.70 and e.global_brand_monoculture_dominance >= 0.65:
        return "cultural_commodification_crisis"
    if e.indigenous_cultural_sovereignty_erosion >= 0.70 and e.language_heritage_extinction_rate >= 0.65:
        return "indigenous_erasure"
    if e.institutional_cultural_memory_loss >= 0.70 and e.diaspora_cultural_connection_severing >= 0.65:
        return "cultural_memory_implosion"
    return "none"


def _severity(risk: str) -> str:
    return {
        "critical": "destruction_patrimoine_systémique",
        "high":     "crise_capital_culturel_majeure",
        "moderate": "érosion_culturelle_structurelle",
        "low":      "patrimoine_relativement_préservé",
    }[risk]


def _recommended_action(risk: str) -> str:
    return {
        "critical": "protection_patrimoine_urgente",
        "high":     "stratégie_préservation_culturelle_activée",
        "moderate": "renforcement_transmission_culturelle",
        "low":      "veille_patrimoine_continue",
    }[risk]


def _signal(risk: str) -> str:
    return {
        "critical": "🔴 Destruction patrimoine systémique — capital culturel en péril",
        "high":     "🟠 Crise capital culturel majeure détectée",
        "moderate": "🟡 Érosion culturelle structurelle active",
        "low":      "🟢 Patrimoine culturel relativement préservé",
    }[risk]


def analyze_entity(e: CulturalHeritageInput) -> Dict[str, Any]:
    destruction = _destruction_score(e)
    erosion = _erosion_score(e)
    commodification = _commodification_score(e)
    sovereignty = _sovereignty_score(e)
    comp = _composite(destruction, erosion, commodification, sovereignty)
    risk = _risk_level(comp)
    pattern = _cultural_pattern(e)
    severity = _severity(risk)
    action = _recommended_action(risk)
    sig = _signal(risk)

    # to_dict() returns exactly 15 keys
    return {
        "entity_id": e.entity_id,
        "cultural_domain": e.cultural_domain,
        "region": e.region,
        "destruction_score": destruction,
        "erosion_score": erosion,
        "commodification_score": commodification,
        "sovereignty_score": sovereignty,
        "composite_score": comp,
        "risk_level": risk,
        "cultural_pattern": pattern,
        "severity": severity,
        "recommended_action": action,
        "signal": sig,
        "heritage_physical_destruction_rate": e.heritage_physical_destruction_rate,
        "indigenous_cultural_sovereignty_erosion": e.indigenous_cultural_sovereignty_erosion,
    }


class CulturalHeritageEngine:
    def run(self, inputs: List[CulturalHeritageInput]) -> Dict[str, Any]:
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
            pattern_distribution[ent["cultural_pattern"]] = pattern_distribution.get(ent["cultural_pattern"], 0) + 1
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
            "module_id": 341,
            "module_name": "Cultural Capital & Heritage Destruction Intelligence Engine",
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
            "avg_estimated_heritage_risk_index": round(avg_composite / 100 * 10, 2),
        }

        return {"entities": entities, "summary": summary}
