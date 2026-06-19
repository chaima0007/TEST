"""
Module 380 — Battery Geopolitics & Critical Minerals for Clean Energy Intelligence Engine
Caelum Partners Swarm Intelligence — Propriété exclusive de Chaima Mhadbi
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class BatteryGeopoliticsInput:
    entity_id: str
    mineral_type: str
    region: str
    lithium_supply_concentration: float
    cobalt_congo_dependency: float
    nickel_supply_risk: float
    manganese_geopolitical_control: float
    battery_manufacturing_monopoly: float
    EV_supply_chain_vulnerability: float
    Chinese_battery_dominance: float
    recycling_infrastructure_gap: float
    artisanal_mining_risk: float
    child_labor_exposure: float
    environmental_mining_destruction: float
    strategic_stockpile_inadequacy: float
    processing_chokepoint: float
    battery_technology_lock_in: float
    energy_storage_sovereignty: float
    mineral_nationalism_risk: float
    green_tech_supply_weaponization: float


@dataclass
class BatteryGeopoliticsResult:
    entity_id: str
    mineral_type: str
    region: str
    supply_score: float
    geopolitical_score: float
    humanitarian_score: float
    sovereignty_score: float
    composite_score: float
    risk_level: str
    battery_pattern: str
    severity: str
    recommended_action: str
    signal: str
    lithium_supply_concentration: float
    green_tech_supply_weaponization: float

    def to_dict(self) -> Dict[str, Any]:
        # INVARIANT: exactly 15 keys
        return {
            "entity_id": self.entity_id,
            "mineral_type": self.mineral_type,
            "region": self.region,
            "supply_score": self.supply_score,
            "geopolitical_score": self.geopolitical_score,
            "humanitarian_score": self.humanitarian_score,
            "sovereignty_score": self.sovereignty_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "battery_pattern": self.battery_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "lithium_supply_concentration": self.lithium_supply_concentration,
            "green_tech_supply_weaponization": self.green_tech_supply_weaponization,
        }


def _supply_score(e: BatteryGeopoliticsInput) -> float:
    raw = (
        e.lithium_supply_concentration * 0.4
        + e.cobalt_congo_dependency * 0.35
        + e.nickel_supply_risk * 0.25
    ) * 100
    return round(raw * 100) / 100


def _geopolitical_score(e: BatteryGeopoliticsInput) -> float:
    raw = (
        e.Chinese_battery_dominance * 0.4
        + e.battery_manufacturing_monopoly * 0.35
        + e.manganese_geopolitical_control * 0.25
    ) * 100
    return round(raw * 100) / 100


def _humanitarian_score(e: BatteryGeopoliticsInput) -> float:
    raw = (
        e.artisanal_mining_risk * 0.4
        + e.child_labor_exposure * 0.35
        + e.environmental_mining_destruction * 0.25
    ) * 100
    return round(raw * 100) / 100


def _sovereignty_score(e: BatteryGeopoliticsInput) -> float:
    raw = (
        e.energy_storage_sovereignty * 0.4
        + e.battery_technology_lock_in * 0.35
        + e.recycling_infrastructure_gap * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(supply: float, geopolitical: float, humanitarian: float, sovereignty: float) -> float:
    return round((supply * 0.30 + geopolitical * 0.25 + humanitarian * 0.25 + sovereignty * 0.20) * 100) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _battery_pattern(e: BatteryGeopoliticsInput) -> str:
    if e.lithium_supply_concentration > 0.85 and e.battery_manufacturing_monopoly > 0.80:
        return "lithium_supply_crisis"
    if e.Chinese_battery_dominance > 0.85 and e.processing_chokepoint > 0.80:
        return "Chinese_battery_capture"
    if e.cobalt_congo_dependency > 0.85 and e.child_labor_exposure > 0.80:
        return "cobalt_humanitarian_crisis"
    if e.green_tech_supply_weaponization > 0.80 and e.mineral_nationalism_risk > 0.75:
        return "green_tech_weaponization"
    if e.EV_supply_chain_vulnerability > 0.80 and e.strategic_stockpile_inadequacy > 0.75:
        return "EV_supply_chain_collapse"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_géopolitique_batteries_systémique"
    if composite >= 40:
        return "tension_approvisionnement_minéraux_majeure"
    if composite >= 20:
        return "risque_chaîne_batteries_modéré"
    return "surveillance_minéraux_transition_verte"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "sécurisation_urgente_minéraux_batteries_critiques"
    if risk == "high":
        return "diversification_approvisionnement_batteries_accélérée"
    if risk == "moderate":
        return "renforcement_résilience_chaîne_valeur_batteries"
    return "veille_géopolitique_minéraux_transition_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise géopolitique batteries systémique — dépendance minéraux extrême"
    if risk == "high":
        return "🟠 Tension approvisionnement minéraux batteries majeure détectée"
    if risk == "moderate":
        return "🟡 Risque chaîne valeur batteries modéré actif"
    return "🟢 Surveillance minéraux transition verte en cours"


def _analyze(e: BatteryGeopoliticsInput) -> Dict[str, Any]:
    supply = _supply_score(e)
    geopolitical = _geopolitical_score(e)
    humanitarian = _humanitarian_score(e)
    sovereignty = _sovereignty_score(e)
    composite = _composite(supply, geopolitical, humanitarian, sovereignty)
    risk = _risk_level(composite)
    pattern = _battery_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    signal = _signal(risk)

    result = BatteryGeopoliticsResult(
        entity_id=e.entity_id,
        mineral_type=e.mineral_type,
        region=e.region,
        supply_score=supply,
        geopolitical_score=geopolitical,
        humanitarian_score=humanitarian,
        sovereignty_score=sovereignty,
        composite_score=composite,
        risk_level=risk,
        battery_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=signal,
        lithium_supply_concentration=e.lithium_supply_concentration,
        green_tech_supply_weaponization=e.green_tech_supply_weaponization,
    )
    return result.to_dict()


class BatteryGeopoliticsEngine:
    def run(self, inputs: List[BatteryGeopoliticsInput]) -> Dict[str, Any]:
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
            pattern_distribution[ent["battery_pattern"]] = pattern_distribution.get(ent["battery_pattern"], 0) + 1
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

        # INVARIANT: summary() returns exactly 13 keys
        summary = {
            "module_id": 380,
            "module_name": "Battery Geopolitics & Critical Minerals for Clean Energy Intelligence Engine",
            "total": n,
            "critical": critical_count,
            "high": high_count,
            "moderate": moderate_count,
            "low": low_count,
            "avg_composite": avg_composite,
            "risk_distribution": risk_distribution,
            "pattern_distribution": pattern_distribution,
            "severity_distribution": severity_distribution,
            "action_distribution": action_distribution,
            "avg_estimated_battery_geopolitics_index": round(avg_composite / 100 * 10, 2),
        }

        return {"entities": entities, "summary": summary}

    def summary(self, inputs: List[BatteryGeopoliticsInput]) -> Dict[str, Any]:
        result = self.run(inputs)
        return result["summary"]
