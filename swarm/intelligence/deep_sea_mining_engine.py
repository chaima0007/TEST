"""
Module 390 — Deep Sea Mining & Seabed Resource Geopolitics Intelligence Engine
Caelum Partners Swarm Intelligence — Propriété exclusive de Chaima Mhadbi
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class DeepSeaMiningInput:
    entity_id: str
    mining_zone: str
    region: str
    ecological_destruction_scale: float
    polymetallic_nodule_competition: float
    ISA_governance_failure: float
    deep_sea_biodiversity_collapse: float
    sediment_plume_impact: float
    carbon_sequestration_disruption: float
    geopolitical_seabed_claim: float
    technological_mining_dominance: float
    small_island_state_exclusion: float
    treaty_violation_risk: float
    rare_mineral_seabed_value: float
    ocean_floor_sovereignty_dispute: float
    deep_sea_cable_risk: float
    military_seabed_use: float
    private_company_capture: float
    monitoring_enforcement_gap: float
    UNCLOS_framework_stress: float


@dataclass
class DeepSeaMiningResult:
    entity_id: str
    mining_zone: str
    region: str
    ecological_score: float
    geopolitical_score: float
    governance_score: float
    exploitation_score: float
    composite_score: float
    risk_level: str
    mining_pattern: str
    severity: str
    recommended_action: str
    signal: str
    ecological_destruction_scale: float
    geopolitical_seabed_claim: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "mining_zone": self.mining_zone,
            "region": self.region,
            "ecological_score": self.ecological_score,
            "geopolitical_score": self.geopolitical_score,
            "governance_score": self.governance_score,
            "exploitation_score": self.exploitation_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "mining_pattern": self.mining_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "ecological_destruction_scale": self.ecological_destruction_scale,
            "geopolitical_seabed_claim": self.geopolitical_seabed_claim,
        }


def _ecological_score(e: DeepSeaMiningInput) -> float:
    raw = (
        e.ecological_destruction_scale * 0.4
        + e.deep_sea_biodiversity_collapse * 0.35
        + e.sediment_plume_impact * 0.25
    ) * 100
    return round(raw * 100) / 100


def _geopolitical_score(e: DeepSeaMiningInput) -> float:
    raw = (
        e.geopolitical_seabed_claim * 0.4
        + e.ocean_floor_sovereignty_dispute * 0.35
        + e.military_seabed_use * 0.25
    ) * 100
    return round(raw * 100) / 100


def _governance_score(e: DeepSeaMiningInput) -> float:
    raw = (
        e.ISA_governance_failure * 0.4
        + e.treaty_violation_risk * 0.35
        + e.UNCLOS_framework_stress * 0.25
    ) * 100
    return round(raw * 100) / 100


def _exploitation_score(e: DeepSeaMiningInput) -> float:
    raw = (
        e.rare_mineral_seabed_value * 0.4
        + e.polymetallic_nodule_competition * 0.35
        + e.technological_mining_dominance * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(ecological: float, geopolitical: float, governance: float, exploitation: float) -> float:
    return round((ecological * 0.30 + geopolitical * 0.25 + governance * 0.25 + exploitation * 0.20) * 100) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _mining_pattern(e: DeepSeaMiningInput) -> str:
    if e.ecological_destruction_scale > 0.85 and e.deep_sea_biodiversity_collapse > 0.80:
        return "deep_sea_ecosystem_destruction"
    if e.geopolitical_seabed_claim > 0.85 and e.ocean_floor_sovereignty_dispute > 0.80:
        return "seabed_geopolitical_conflict"
    if e.ISA_governance_failure > 0.85 and e.private_company_capture > 0.80:
        return "ISA_governance_capture"
    if e.small_island_state_exclusion > 0.80 and e.UNCLOS_framework_stress > 0.75:
        return "small_island_exclusion_crisis"
    if e.rare_mineral_seabed_value > 0.80 and e.monitoring_enforcement_gap > 0.75:
        return "mineral_rush_ecological_catastrophe"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "catastrophe_écologique_fond_marin_systémique"
    if composite >= 40:
        return "crise_géopolitique_ressources_seabed_majeure"
    if composite >= 20:
        return "tension_exploitation_fond_marin_active"
    return "surveillance_exploitation_minière_fond_marin"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_protection_écosystème_fond_marin"
    if risk == "high":
        return "renforcement_gouvernance_ISA_multilatérale"
    if risk == "moderate":
        return "surveillance_renforcée_zones_extraction_seabed"
    return "veille_exploitation_minière_fond_marin_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Catastrophe écologique fond marin systémique — destruction irréversible imminente"
    if risk == "high":
        return "🟠 Crise géopolitique ressources seabed majeure détectée"
    if risk == "moderate":
        return "🟡 Tension exploitation fond marin active"
    return "🟢 Exploitation minière fond marin sous surveillance"


def _analyze(e: DeepSeaMiningInput) -> Dict[str, Any]:
    ecological = _ecological_score(e)
    geopolitical = _geopolitical_score(e)
    governance = _governance_score(e)
    exploitation = _exploitation_score(e)
    composite = _composite(ecological, geopolitical, governance, exploitation)
    risk = _risk_level(composite)
    pattern = _mining_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    signal = _signal(risk)

    result = DeepSeaMiningResult(
        entity_id=e.entity_id,
        mining_zone=e.mining_zone,
        region=e.region,
        ecological_score=ecological,
        geopolitical_score=geopolitical,
        governance_score=governance,
        exploitation_score=exploitation,
        composite_score=composite,
        risk_level=risk,
        mining_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=signal,
        ecological_destruction_scale=e.ecological_destruction_scale,
        geopolitical_seabed_claim=e.geopolitical_seabed_claim,
    )
    return result.to_dict()


class DeepSeaMiningEngine:
    def run(self, inputs: List[DeepSeaMiningInput]) -> Dict[str, Any]:
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
            pattern_distribution[ent["mining_pattern"]] = pattern_distribution.get(ent["mining_pattern"], 0) + 1
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

        # summary has EXACTLY 13 keys
        summary = {
            "module_id": 390,
            "module_name": "Deep Sea Mining & Seabed Resource Geopolitics Intelligence Engine",
            "total": n,
            "critical": critical_count,
            "high": high_count,
            "moderate": moderate_count,
            "low": low_count,
            "avg_composite": avg_composite,
            "distributions": {
                "risk": risk_distribution,
                "pattern": pattern_distribution,
                "severity": severity_distribution,
                "action": action_distribution,
            },
            "pattern_distribution": pattern_distribution,
            "risk_distribution": risk_distribution,
            "severity_distribution": severity_distribution,
            "avg_estimated_seabed_risk_index": round(avg_composite / 100 * 10, 2),
        }

        return {"entities": entities, "summary": summary}
