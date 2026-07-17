"""
Module 373 — Nuclear Fusion Energy Race & Geopolitics Intelligence Engine
Caelum Partners Swarm Intelligence — Propriété exclusive de Chaima Mhadbi
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class NuclearFusionInput:
    entity_id: str
    fusion_program: str
    region: str
    technological_lead: float
    tritium_supply_control: float
    plasma_confinement_advantage: float
    fusion_patent_monopoly: float
    rare_material_access: float
    commercial_deployment_speed: float
    military_fusion_application: float
    geopolitical_leverage_gain: float
    ITER_dependency: float
    private_fusion_dominance: float
    IP_theft_vulnerability: float
    fusion_standards_capture: float
    energy_independence_threat: float
    proliferation_risk: float
    workforce_concentration: float
    supply_chain_dominance: float
    first_mover_advantage: float


def _dominance_score(e: NuclearFusionInput) -> float:
    raw = (
        e.technological_lead * 0.40
        + e.plasma_confinement_advantage * 0.35
        + e.first_mover_advantage * 0.25
    ) * 100
    return round(raw * 100) / 100


def _supply_score(e: NuclearFusionInput) -> float:
    raw = (
        e.tritium_supply_control * 0.40
        + e.rare_material_access * 0.35
        + e.supply_chain_dominance * 0.25
    ) * 100
    return round(raw * 100) / 100


def _geopolitical_score(e: NuclearFusionInput) -> float:
    raw = (
        e.geopolitical_leverage_gain * 0.40
        + e.fusion_standards_capture * 0.35
        + e.energy_independence_threat * 0.25
    ) * 100
    return round(raw * 100) / 100


def _risk_score(e: NuclearFusionInput) -> float:
    raw = (
        e.proliferation_risk * 0.40
        + e.IP_theft_vulnerability * 0.35
        + e.workforce_concentration * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(dominance: float, supply: float, geopolitical: float, risk: float) -> float:
    return round((dominance * 0.30 + supply * 0.25 + geopolitical * 0.25 + risk * 0.20) * 100) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _fusion_pattern(e: NuclearFusionInput) -> str:
    if e.technological_lead > 0.85 and e.first_mover_advantage > 0.80:
        return "fusion_supremacy_race"
    if e.tritium_supply_control > 0.85 and e.rare_material_access > 0.80:
        return "tritium_geopolitical_weapon"
    if e.fusion_patent_monopoly > 0.85 and e.IP_theft_vulnerability > 0.70:
        return "fusion_IP_monopoly_capture"
    if e.private_fusion_dominance > 0.80 and e.commercial_deployment_speed > 0.75:
        return "private_fusion_disruption"
    if e.proliferation_risk > 0.80 and e.military_fusion_application > 0.75:
        return "fusion_proliferation_crisis"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_fusion_géopolitique_systémique"
    if composite >= 40:
        return "domination_fusion_stratégique_majeure"
    if composite >= 20:
        return "tension_course_fusion_nucléaire"
    return "programme_fusion_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_course_fusion_nucléaire"
    if risk == "high":
        return "containment_stratégique_programme_fusion"
    if risk == "moderate":
        return "surveillance_renforcée_géopolitique_fusion"
    return "veille_fusion_nucléaire_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise fusion géopolitique systémique — domination technologique extrême"
    if risk == "high":
        return "🟠 Domination fusion stratégique majeure détectée"
    if risk == "moderate":
        return "🟡 Tension course fusion nucléaire active"
    return "🟢 Programme fusion nucléaire sous surveillance"


def _analyze(e: NuclearFusionInput) -> Dict[str, Any]:
    dominance = _dominance_score(e)
    supply = _supply_score(e)
    geopolitical = _geopolitical_score(e)
    risk = _risk_score(e)
    composite = _composite(dominance, supply, geopolitical, risk)
    risk_lvl = _risk_level(composite)
    pattern = _fusion_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk_lvl)
    signal = _signal(risk_lvl)

    return {
        "entity_id": e.entity_id,
        "fusion_program": e.fusion_program,
        "region": e.region,
        "dominance_score": dominance,
        "supply_score": supply,
        "geopolitical_score": geopolitical,
        "risk_score": risk,
        "composite_score": composite,
        "risk_level": risk_lvl,
        "fusion_pattern": pattern,
        "severity": severity,
        "recommended_action": action,
        "signal": signal,
        "technological_lead": e.technological_lead,
        "proliferation_risk": e.proliferation_risk,
    }


class NuclearFusionResult:
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    def to_dict(self) -> Dict[str, Any]:
        # Returns exactly 15 keys
        return self._data


class NuclearFusionEngine:
    def run(self, inputs: List[NuclearFusionInput]) -> Dict[str, Any]:
        results = [NuclearFusionResult(_analyze(e)) for e in inputs]
        entities = [r.to_dict() for r in results]

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
            pattern_distribution[ent["fusion_pattern"]] = pattern_distribution.get(ent["fusion_pattern"], 0) + 1
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

        return {
            "entities": entities,
            "summary": self.summary(
                n, critical_count, high_count, moderate_count, low_count,
                avg_composite, pattern_distribution, risk_distribution,
                severity_distribution, action_distribution,
            ),
        }

    def summary(
        self,
        n: int,
        critical_count: int,
        high_count: int,
        moderate_count: int,
        low_count: int,
        avg_composite: float,
        pattern_distribution: Dict[str, int],
        risk_distribution: Dict[str, int],
        severity_distribution: Dict[str, int],
        action_distribution: Dict[str, int],
    ) -> Dict[str, Any]:
        # Returns exactly 13 keys
        return {
            "module_id": 373,
            "module_name": "Nuclear Fusion Energy Race & Geopolitics Intelligence Engine",
            "total": n,
            "critical": critical_count,
            "high": high_count,
            "moderate": moderate_count,
            "low": low_count,
            "avg_composite": avg_composite,
            "pattern_distribution": pattern_distribution,
            "risk_distribution": risk_distribution,
            "severity_distribution": severity_distribution,
            "action_distribution": action_distribution,
            "avg_estimated_fusion_dominance_index": round(avg_composite / 100 * 10, 2),
        }
