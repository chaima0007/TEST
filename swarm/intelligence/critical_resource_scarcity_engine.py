from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class CriticalResourceInput:
    entity_id: str
    resource_category: str
    region: str
    supply_concentration_risk: float
    demand_growth_rate: float
    substitution_difficulty: float
    geopolitical_supply_risk: float
    stockpile_adequacy: float
    recycling_circularity_rate: float
    processing_choke_point: float
    reserve_depletion_rate: float
    alternative_source_development: float
    price_volatility_index: float
    import_dependency: float
    environmental_extraction_cost: float
    water_stress_index: float
    food_system_fragility: float
    semiconductor_supply_risk: float
    rare_earth_concentration: float
    critical_mineral_pipeline_gap: float


@dataclass
class CriticalResourceResult:
    entity_id: str
    region: str
    resource_category: str
    scarcity_risk: str
    scarcity_pattern: str
    scarcity_severity: str
    recommended_action: str
    supply_score: float
    demand_score: float
    geopolitical_score: float
    sustainability_score: float
    scarcity_composite: float
    is_in_scarcity_crisis: bool
    requires_scarcity_intervention: bool
    scarcity_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "resource_category": self.resource_category,
            "scarcity_risk": self.scarcity_risk,
            "scarcity_pattern": self.scarcity_pattern,
            "scarcity_severity": self.scarcity_severity,
            "recommended_action": self.recommended_action,
            "supply_score": self.supply_score,
            "demand_score": self.demand_score,
            "geopolitical_score": self.geopolitical_score,
            "sustainability_score": self.sustainability_score,
            "scarcity_composite": self.scarcity_composite,
            "is_in_scarcity_crisis": self.is_in_scarcity_crisis,
            "requires_scarcity_intervention": self.requires_scarcity_intervention,
            "scarcity_signal": self.scarcity_signal,
        }


def _supply_score(e: CriticalResourceInput) -> float:
    raw = (
        e.supply_concentration_risk * 0.4
        + e.processing_choke_point * 0.35
        + (1 - e.stockpile_adequacy) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _demand_score(e: CriticalResourceInput) -> float:
    raw = (
        e.demand_growth_rate * 0.4
        + e.substitution_difficulty * 0.35
        + e.reserve_depletion_rate * 0.25
    ) * 100
    return round(raw * 100) / 100


def _geopolitical_score(e: CriticalResourceInput) -> float:
    raw = (
        e.geopolitical_supply_risk * 0.4
        + e.import_dependency * 0.35
        + e.rare_earth_concentration * 0.25
    ) * 100
    return round(raw * 100) / 100


def _sustainability_score(e: CriticalResourceInput) -> float:
    raw = (
        e.environmental_extraction_cost * 0.4
        + (1 - e.recycling_circularity_rate) * 0.35
        + (1 - e.alternative_source_development) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(supply: float, demand: float, geopolitical: float, sustainability: float) -> float:
    return round(
        (supply * 0.30 + demand * 0.25 + geopolitical * 0.25 + sustainability * 0.20) * 100
    ) / 100


def _scarcity_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _scarcity_pattern(e: CriticalResourceInput) -> str:
    if e.supply_concentration_risk >= 0.70 and (1 - e.stockpile_adequacy) >= 0.60:
        return "supply_shock"
    if e.geopolitical_supply_risk >= 0.70 and e.import_dependency >= 0.65:
        return "geopolitical_embargo"
    if e.demand_growth_rate >= 0.70 and e.substitution_difficulty >= 0.65:
        return "demand_explosion"
    if e.reserve_depletion_rate >= 0.70 and (1 - e.alternative_source_development) >= 0.60:
        return "depletion_crisis"
    if e.processing_choke_point >= 0.70 and e.rare_earth_concentration >= 0.65:
        return "processing_monopoly"
    return "none"


def _scarcity_severity(composite: float) -> str:
    if composite >= 75:
        return "resource_emergency"
    if composite >= 50:
        return "high_scarcity"
    if composite >= 25:
        return "supply_tension"
    return "resource_abundant"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "resource_emergency_program"
    if risk == "high" and pattern == "geopolitical_embargo":
        return "supply_diversification"
    if risk == "high":
        return "strategic_reserve_buildup"
    if risk == "moderate":
        return "resource_monitoring"
    return "no_action"


def _scarcity_signal(e: CriticalResourceInput, risk: str, composite: float) -> str:
    if risk == "critical":
        return (
            f"Critique — concentration approvisionnement {int(e.supply_concentration_risk * 100)}%"
            f" — risque géopolitique {int(e.geopolitical_supply_risk * 100)}%"
            f" — composite {int(composite)}"
        )
    if risk == "high":
        return (
            f"Élevé — croissance demande {int(e.demand_growth_rate * 100)}%"
            f" — dépendance importations {int(e.import_dependency * 100)}%"
            f" — composite {int(composite)}"
        )
    if risk == "moderate":
        return (
            f"Modéré — taux recyclage {int(e.recycling_circularity_rate * 100)}%"
            f" — composite {int(composite)}"
        )
    return "Ressources critiques abondantes — diversification approvisionnement, circularité élevée"


def analyze_resource(e: CriticalResourceInput) -> CriticalResourceResult:
    supply = _supply_score(e)
    demand = _demand_score(e)
    geopolitical = _geopolitical_score(e)
    sustainability = _sustainability_score(e)
    composite = _composite(supply, demand, geopolitical, sustainability)
    risk = _scarcity_risk(composite)
    pattern = _scarcity_pattern(e)
    severity = _scarcity_severity(composite)
    action = _recommended_action(risk, pattern)
    signal = _scarcity_signal(e, risk, composite)

    return CriticalResourceResult(
        entity_id=e.entity_id,
        region=e.region,
        resource_category=e.resource_category,
        scarcity_risk=risk,
        scarcity_pattern=pattern,
        scarcity_severity=severity,
        recommended_action=action,
        supply_score=supply,
        demand_score=demand,
        geopolitical_score=geopolitical,
        sustainability_score=sustainability,
        scarcity_composite=composite,
        is_in_scarcity_crisis=composite >= 60,
        requires_scarcity_intervention=composite >= 40,
        scarcity_signal=signal,
    )


class CriticalResourceScarcityEngine:
    def analyze(self, entities: List[CriticalResourceInput]) -> Dict[str, Any]:
        results = [analyze_resource(e) for e in entities]

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}

        total_supply = 0.0
        total_demand = 0.0
        total_geopolitical = 0.0
        total_sustainability = 0.0
        total_composite = 0.0
        scarcity_crisis_count = 0
        scarcity_intervention_count = 0

        for r in results:
            risk_counts[r.scarcity_risk] = risk_counts.get(r.scarcity_risk, 0) + 1
            pattern_counts[r.scarcity_pattern] = pattern_counts.get(r.scarcity_pattern, 0) + 1
            severity_counts[r.scarcity_severity] = severity_counts.get(r.scarcity_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1
            total_supply += r.supply_score
            total_demand += r.demand_score
            total_geopolitical += r.geopolitical_score
            total_sustainability += r.sustainability_score
            total_composite += r.scarcity_composite
            if r.is_in_scarcity_crisis:
                scarcity_crisis_count += 1
            if r.requires_scarcity_intervention:
                scarcity_intervention_count += 1

        n = len(results) or 1
        avg_composite = round(total_composite / n * 10) / 10

        return {
            "total": len(results),
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_scarcity_composite": avg_composite,
            "scarcity_crisis_count": scarcity_crisis_count,
            "scarcity_intervention_count": scarcity_intervention_count,
            "avg_supply_score": round(total_supply / n * 10) / 10,
            "avg_demand_score": round(total_demand / n * 10) / 10,
            "avg_geopolitical_score": round(total_geopolitical / n * 10) / 10,
            "avg_sustainability_score": round(total_sustainability / n * 10) / 10,
            "avg_estimated_scarcity_index": round(avg_composite / 100 * 10, 2),
        }
