"""
Food System Collapse & Agricultural Intelligence Engine
Module 319 — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any


@dataclass
class FoodSystemInput:
    entity_id: str
    food_system_type: str
    region: str
    # 17 float fields (0.0-1.0)
    crop_yield_collapse_risk: float
    monoculture_vulnerability: float
    seed_sovereignty_erosion: float
    agrochemical_dependency: float
    soil_degradation_rate: float
    pollinator_collapse_index: float
    extreme_weather_frequency: float
    supply_chain_food_fragility: float
    food_import_dependency: float
    price_spike_transmission: float
    urban_food_desert_expansion: float
    protein_transition_disruption: float
    vertical_farming_disruption_gap: float
    water_food_nexus_stress: float
    nitrogen_cycle_disruption: float
    smallholder_displacement_rate: float
    food_system_digitalization_risk: float


@dataclass
class FoodSystemResult:
    entity_id: str
    region: str
    food_system_type: str
    food_risk: str
    food_pattern: str
    food_severity: str
    recommended_action: str
    production_score: float
    supply_score: float
    access_score: float
    resilience_score: float
    food_composite: float
    is_food_crisis: bool
    requires_food_intervention: bool
    food_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "food_system_type": self.food_system_type,
            "food_risk": self.food_risk,
            "food_pattern": self.food_pattern,
            "food_severity": self.food_severity,
            "recommended_action": self.recommended_action,
            "production_score": self.production_score,
            "supply_score": self.supply_score,
            "access_score": self.access_score,
            "resilience_score": self.resilience_score,
            "food_composite": self.food_composite,
            "is_food_crisis": self.is_food_crisis,
            "requires_food_intervention": self.requires_food_intervention,
            "food_signal": self.food_signal,
        }


def _production_score(inp: FoodSystemInput) -> float:
    raw = (
        inp.crop_yield_collapse_risk * 0.4
        + inp.soil_degradation_rate * 0.35
        + inp.pollinator_collapse_index * 0.25
    ) * 100
    return round(raw * 100) / 100


def _supply_score(inp: FoodSystemInput) -> float:
    raw = (
        inp.food_import_dependency * 0.4
        + inp.supply_chain_food_fragility * 0.35
        + inp.monoculture_vulnerability * 0.25
    ) * 100
    return round(raw * 100) / 100


def _access_score(inp: FoodSystemInput) -> float:
    raw = (
        inp.price_spike_transmission * 0.4
        + inp.urban_food_desert_expansion * 0.35
        + inp.smallholder_displacement_rate * 0.25
    ) * 100
    return round(raw * 100) / 100


def _resilience_score(inp: FoodSystemInput) -> float:
    raw = (
        inp.extreme_weather_frequency * 0.4
        + inp.nitrogen_cycle_disruption * 0.35
        + inp.agrochemical_dependency * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(
    production: float,
    supply: float,
    access: float,
    resilience: float,
) -> float:
    return round(
        production * 0.30
        + supply * 0.25
        + access * 0.25
        + resilience * 0.20,
        2,
    )


def _food_pattern(inp: FoodSystemInput) -> str:
    if inp.crop_yield_collapse_risk >= 0.70 and inp.food_import_dependency >= 0.65:
        return "famine_cascade"
    if inp.monoculture_vulnerability >= 0.70 and inp.pollinator_collapse_index >= 0.65:
        return "monoculture_collapse"
    if inp.price_spike_transmission >= 0.70 and inp.supply_chain_food_fragility >= 0.65:
        return "price_shock_explosion"
    if inp.soil_degradation_rate >= 0.70 and inp.nitrogen_cycle_disruption >= 0.65:
        return "soil_death_spiral"
    if inp.protein_transition_disruption >= 0.70 and inp.smallholder_displacement_rate >= 0.60:
        return "protein_transition_shock"
    return "none"


def _food_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _food_severity(composite: float) -> str:
    if composite >= 75:
        return "food_emergency"
    if composite >= 50:
        return "food_crisis"
    if composite >= 25:
        return "food_stress"
    return "food_secure"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "food_emergency_protocol"
    if risk == "high" and pattern == "famine_cascade":
        return "emergency_food_reserves"
    if risk == "high":
        return "food_resilience_program"
    if risk == "moderate":
        return "food_monitoring"
    return "no_action"


def _food_signal(inp: FoodSystemInput, risk: str, composite: float) -> str:
    if risk == "critical":
        return (
            f"Critique — risque effondrement rendements {int(inp.crop_yield_collapse_risk * 100)}% "
            f"— dépendance importations alimentaires {int(inp.food_import_dependency * 100)}% "
            f"— composite {int(composite)}"
        )
    if risk == "high":
        return (
            f"Élevé — vulnérabilité monoculture {int(inp.monoculture_vulnerability * 100)}% "
            f"— dégradation sols {int(inp.soil_degradation_rate * 100)}% "
            f"— composite {int(composite)}"
        )
    if risk == "moderate":
        return (
            f"Modéré — transmission choc prix {int(inp.price_spike_transmission * 100)}% "
            f"— composite {int(composite)}"
        )
    return "Système alimentaire stable — résilience agricole solide, souveraineté alimentaire préservée, aucun risque imminent d'effondrement"


def analyze(inp: FoodSystemInput) -> FoodSystemResult:
    production = _production_score(inp)
    supply = _supply_score(inp)
    access = _access_score(inp)
    resilience = _resilience_score(inp)
    comp = _composite(production, supply, access, resilience)
    pat = _food_pattern(inp)
    risk = _food_risk(comp)
    sev = _food_severity(comp)
    action = _recommended_action(risk, pat)
    sig = _food_signal(inp, risk, comp)

    return FoodSystemResult(
        entity_id=inp.entity_id,
        region=inp.region,
        food_system_type=inp.food_system_type,
        food_risk=risk,
        food_pattern=pat,
        food_severity=sev,
        recommended_action=action,
        production_score=production,
        supply_score=supply,
        access_score=access,
        resilience_score=resilience,
        food_composite=comp,
        is_food_crisis=comp >= 60,
        requires_food_intervention=comp >= 40,
        food_signal=sig,
    )


class FoodSystemCollapseEngine:
    def analyze(self, entities: List[FoodSystemInput]) -> Dict[str, Any]:
        results = [analyze(e) for e in entities]
        n = len(results)
        if n == 0:
            return {}

        critical_count = sum(1 for r in results if r.food_risk == "critical")
        high_count = sum(1 for r in results if r.food_risk == "high")
        moderate_count = sum(1 for r in results if r.food_risk == "moderate")
        low_count = sum(1 for r in results if r.food_risk == "low")
        food_crisis_count = sum(1 for r in results if r.is_food_crisis)
        requires_intervention_count = sum(1 for r in results if r.requires_food_intervention)

        total_composite = sum(r.food_composite for r in results)
        avg_composite = round(total_composite / n, 2)

        pattern_counts: Dict[str, int] = {}
        for r in results:
            pattern_counts[r.food_pattern] = pattern_counts.get(r.food_pattern, 0) + 1
        dominant_food_pattern = max(pattern_counts, key=lambda k: pattern_counts[k])

        region_composite: Dict[str, float] = {}
        region_count: Dict[str, int] = {}
        for r in results:
            region_composite[r.region] = region_composite.get(r.region, 0.0) + r.food_composite
            region_count[r.region] = region_count.get(r.region, 0) + 1
        region_avg = {reg: region_composite[reg] / region_count[reg] for reg in region_composite}
        most_vulnerable_region = max(region_avg, key=lambda k: region_avg[k])

        return {
            "total_entities": n,
            "critical_count": critical_count,
            "high_count": high_count,
            "moderate_count": moderate_count,
            "low_count": low_count,
            "food_crisis_count": food_crisis_count,
            "requires_intervention_count": requires_intervention_count,
            "avg_food_composite": avg_composite,
            "avg_estimated_food_crisis_index": round(avg_composite / 100 * 10, 2),
            "dominant_food_pattern": dominant_food_pattern,
            "most_vulnerable_region": most_vulnerable_region,
            "results": [r.to_dict() for r in results],
            "analysis_timestamp": datetime.utcnow().isoformat() + "Z",
        }
