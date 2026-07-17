"""
Module 293 — Energy Transition Intelligence & Decarbonization Engine
Caelum Partners Swarm Intelligence — Propriété exclusive de Chaima Mhadbi
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class EnergyTransitionInput:
    entity_id: str
    energy_sector: str
    region: str
    renewable_penetration_rate: float
    fossil_dependency: float
    grid_stability_index: float
    stranded_asset_exposure: float
    carbon_intensity: float
    energy_storage_capacity: float
    demand_flexibility: float
    grid_modernization_lag: float
    energy_poverty_risk: float
    just_transition_gap: float
    regulatory_carbon_pressure: float
    green_capex_rate: float
    critical_mineral_dependency: float
    hydrogen_readiness: float
    transmission_infrastructure_gap: float
    energy_sovereignty_index: float
    decarbonization_velocity: float


@dataclass
class EnergyTransitionResult:
    entity_id: str
    region: str
    energy_sector: str
    transition_risk: str
    transition_pattern: str
    transition_severity: str
    recommended_action: str
    fossil_score: float
    stability_score: float
    stranded_score: float
    sovereignty_score: float
    transition_composite: float
    is_in_transition_crisis: bool
    requires_transition_intervention: bool
    transition_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "energy_sector": self.energy_sector,
            "transition_risk": self.transition_risk,
            "transition_pattern": self.transition_pattern,
            "transition_severity": self.transition_severity,
            "recommended_action": self.recommended_action,
            "fossil_score": self.fossil_score,
            "stability_score": self.stability_score,
            "stranded_score": self.stranded_score,
            "sovereignty_score": self.sovereignty_score,
            "transition_composite": self.transition_composite,
            "is_in_transition_crisis": self.is_in_transition_crisis,
            "requires_transition_intervention": self.requires_transition_intervention,
            "transition_signal": self.transition_signal,
        }


def _fossil_score(e: EnergyTransitionInput) -> float:
    raw = (
        e.fossil_dependency * 0.4
        + e.carbon_intensity * 0.35
        + (1 - e.renewable_penetration_rate) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _stability_score(e: EnergyTransitionInput) -> float:
    raw = (
        (1 - e.grid_stability_index) * 0.4
        + e.transmission_infrastructure_gap * 0.35
        + (1 - e.energy_storage_capacity) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _stranded_score(e: EnergyTransitionInput) -> float:
    raw = (
        e.stranded_asset_exposure * 0.4
        + (1 - e.green_capex_rate) * 0.35
        + (1 - e.decarbonization_velocity) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _sovereignty_score(e: EnergyTransitionInput) -> float:
    raw = (
        e.critical_mineral_dependency * 0.4
        + (1 - e.energy_sovereignty_index) * 0.35
        + e.energy_poverty_risk * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(fossil: float, stability: float, stranded: float, sovereignty: float) -> float:
    return round((fossil * 0.30 + stability * 0.25 + stranded * 0.25 + sovereignty * 0.20) * 100) / 100


def _transition_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _transition_pattern(e: EnergyTransitionInput) -> str:
    if e.fossil_dependency >= 0.70 and (1 - e.decarbonization_velocity) >= 0.65:
        return "fossil_lock_in"
    if e.stranded_asset_exposure >= 0.70 and (1 - e.green_capex_rate) >= 0.60:
        return "stranded_asset_crisis"
    if (1 - e.grid_stability_index) >= 0.65 and e.transmission_infrastructure_gap >= 0.60:
        return "grid_instability"
    if e.energy_poverty_risk >= 0.70 and e.just_transition_gap >= 0.60:
        return "energy_poverty_trap"
    if e.critical_mineral_dependency >= 0.70 and (1 - e.energy_sovereignty_index) >= 0.60:
        return "mineral_sovereignty_loss"
    return "none"


def _transition_severity(composite: float) -> str:
    if composite >= 75:
        return "transition_emergency"
    if composite >= 50:
        return "high_transition_risk"
    if composite >= 25:
        return "transition_stress"
    return "transition_optimum"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "decarbonization_emergency"
    if risk == "high" and pattern == "stranded_asset_crisis":
        return "stranded_asset_rescue"
    if risk == "high":
        return "transition_acceleration"
    if risk == "moderate":
        return "transition_monitoring"
    return "no_action"


def _transition_signal(e: EnergyTransitionInput, risk: str, composite: float) -> str:
    comp_int = int(composite)
    if risk == "critical":
        return (
            f"Critique — dépendance fossile {int(e.fossil_dependency * 100)}% "
            f"— actifs échoués {int(e.stranded_asset_exposure * 100)}% "
            f"— composite {comp_int}"
        )
    if risk == "high":
        return (
            f"Élevé — stabilité réseau {int(e.grid_stability_index * 100)}% "
            f"— capex vert {int(e.green_capex_rate * 100)}% "
            f"— composite {comp_int}"
        )
    if risk == "moderate":
        return (
            f"Modéré — pénétration renouvelable {int(e.renewable_penetration_rate * 100)}% "
            f"— composite {comp_int}"
        )
    return "Transition énergétique optimale — décarbonisation accélérée, souveraineté énergétique préservée"


def analyze_entity(e: EnergyTransitionInput) -> EnergyTransitionResult:
    fossil = _fossil_score(e)
    stability = _stability_score(e)
    stranded = _stranded_score(e)
    sovereignty = _sovereignty_score(e)
    comp = _composite(fossil, stability, stranded, sovereignty)
    risk = _transition_risk(comp)
    pattern = _transition_pattern(e)
    severity = _transition_severity(comp)
    action = _recommended_action(risk, pattern)
    signal = _transition_signal(e, risk, comp)

    return EnergyTransitionResult(
        entity_id=e.entity_id,
        region=e.region,
        energy_sector=e.energy_sector,
        transition_risk=risk,
        transition_pattern=pattern,
        transition_severity=severity,
        recommended_action=action,
        fossil_score=fossil,
        stability_score=stability,
        stranded_score=stranded,
        sovereignty_score=sovereignty,
        transition_composite=comp,
        is_in_transition_crisis=comp >= 60,
        requires_transition_intervention=comp >= 40,
        transition_signal=signal,
    )


class EnergyTransitionIntelligenceEngine:
    def run(self, inputs: List[EnergyTransitionInput]) -> Dict[str, Any]:
        results = [analyze_entity(e) for e in inputs]
        entities = [r.to_dict() for r in results]

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}

        total_composite = 0.0
        total_fossil = 0.0
        total_stability = 0.0
        total_stranded = 0.0
        total_sovereignty = 0.0
        crisis_count = 0
        intervention_count = 0

        for r in results:
            risk_counts[r.transition_risk] = risk_counts.get(r.transition_risk, 0) + 1
            pattern_counts[r.transition_pattern] = pattern_counts.get(r.transition_pattern, 0) + 1
            severity_counts[r.transition_severity] = severity_counts.get(r.transition_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1
            total_composite += r.transition_composite
            total_fossil += r.fossil_score
            total_stability += r.stability_score
            total_stranded += r.stranded_score
            total_sovereignty += r.sovereignty_score
            if r.is_in_transition_crisis:
                crisis_count += 1
            if r.requires_transition_intervention:
                intervention_count += 1

        n = len(results)
        avg_composite = round(total_composite / n * 10) / 10 if n else 0.0

        summary = {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_transition_composite": avg_composite,
            "transition_crisis_count": crisis_count,
            "transition_intervention_count": intervention_count,
            "avg_fossil_score": round(total_fossil / n * 10) / 10 if n else 0.0,
            "avg_stability_score": round(total_stability / n * 10) / 10 if n else 0.0,
            "avg_stranded_score": round(total_stranded / n * 10) / 10 if n else 0.0,
            "avg_sovereignty_score": round(total_sovereignty / n * 10) / 10 if n else 0.0,
            "avg_estimated_transition_risk_index": round(avg_composite / 100 * 10, 2),
        }

        return {"entities": entities, "summary": summary}
