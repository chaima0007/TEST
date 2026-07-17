"""
Urban Heat Island & City Climate Emergency Intelligence Engine
Module 354 — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
"""
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class UrbanHeatInput:
    entity_id: str
    city_type: str
    region: str
    # 17 float fields (0.0-1.0)
    heat_island_intensity_index: float = 0.0
    extreme_heat_mortality_rate: float = 0.0
    urban_cooling_infrastructure_deficit: float = 0.0
    green_space_accessibility_inequality: float = 0.0
    air_conditioning_energy_spiral: float = 0.0
    cooling_poverty_exposure: float = 0.0
    urban_albedo_reduction_factor: float = 0.0
    heat_vulnerable_population_density: float = 0.0
    flood_heat_compound_risk: float = 0.0
    urban_biodiversity_collapse: float = 0.0
    pavement_heat_retention_index: float = 0.0
    night_cooling_failure_rate: float = 0.0
    emergency_cooling_center_gap: float = 0.0
    housing_heat_trap_density: float = 0.0
    urban_tree_canopy_deficit: float = 0.0
    heat_adaptation_funding_gap: float = 0.0
    urban_heat_mortality_inequality: float = 0.0


@dataclass
class UrbanHeatResult:
    entity_id: str
    city_type: str
    region: str
    thermal_score: float
    mortality_score: float
    adaptation_score: float
    equity_score: float
    composite_score: float
    risk_level: str
    heat_pattern: str
    severity: str
    recommended_action: str
    signal: str
    heat_island_intensity_index: float
    extreme_heat_mortality_rate: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "city_type": self.city_type,
            "region": self.region,
            "thermal_score": self.thermal_score,
            "mortality_score": self.mortality_score,
            "adaptation_score": self.adaptation_score,
            "equity_score": self.equity_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "heat_pattern": self.heat_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "heat_island_intensity_index": self.heat_island_intensity_index,
            "extreme_heat_mortality_rate": self.extreme_heat_mortality_rate,
        }


def _thermal_score(inp: UrbanHeatInput) -> float:
    raw = (
        inp.heat_island_intensity_index * 0.4
        + inp.pavement_heat_retention_index * 0.35
        + inp.urban_albedo_reduction_factor * 0.25
    ) * 100
    return round(raw * 100) / 100


def _mortality_score(inp: UrbanHeatInput) -> float:
    raw = (
        inp.extreme_heat_mortality_rate * 0.4
        + inp.heat_vulnerable_population_density * 0.35
        + inp.urban_heat_mortality_inequality * 0.25
    ) * 100
    return round(raw * 100) / 100


def _adaptation_score(inp: UrbanHeatInput) -> float:
    raw = (
        inp.urban_cooling_infrastructure_deficit * 0.4
        + inp.emergency_cooling_center_gap * 0.35
        + inp.heat_adaptation_funding_gap * 0.25
    ) * 100
    return round(raw * 100) / 100


def _equity_score(inp: UrbanHeatInput) -> float:
    raw = (
        inp.cooling_poverty_exposure * 0.4
        + inp.green_space_accessibility_inequality * 0.35
        + inp.housing_heat_trap_density * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(
    thermal: float,
    mortality: float,
    adaptation: float,
    equity: float,
) -> float:
    return round(
        thermal * 0.30
        + mortality * 0.25
        + adaptation * 0.25
        + equity * 0.20,
        2,
    )


def _heat_pattern(inp: UrbanHeatInput) -> str:
    if inp.extreme_heat_mortality_rate >= 0.70 and inp.heat_vulnerable_population_density >= 0.65:
        return "lethal_heat_dome"
    if inp.urban_cooling_infrastructure_deficit >= 0.70 and inp.emergency_cooling_center_gap >= 0.65:
        return "cooling_infrastructure_collapse"
    if inp.urban_tree_canopy_deficit >= 0.70 and inp.urban_albedo_reduction_factor >= 0.65:
        return "green_desert_city"
    if inp.cooling_poverty_exposure >= 0.70 and inp.housing_heat_trap_density >= 0.65:
        return "heat_poverty_trap"
    if inp.flood_heat_compound_risk >= 0.70 and inp.heat_island_intensity_index >= 0.65:
        return "compound_climate_crisis"
    return "none"


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _severity(risk: str) -> str:
    if risk == "critical":
        return "urgence_chaleur_urbaine_létale"
    if risk == "high":
        return "crise_chaleur_urbaine_majeure"
    if risk == "moderate":
        return "stress_thermique_structurel"
    return "chaleur_urbaine_gérée"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "plan_urgence_chaleur_urbaine"
    if risk == "high":
        return "infrastructure_refroidissement_urgente"
    if risk == "moderate":
        return "verdissement_urbain_accéléré"
    return "veille_chaleur_urbaine_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Urgence chaleur urbaine létale — vies humaines en danger"
    if risk == "high":
        return "🟠 Crise chaleur urbaine majeure détectée"
    if risk == "moderate":
        return "🟡 Stress thermique structurel actif"
    return "🟢 Chaleur urbaine sous surveillance"


def analyze_urban_heat(inp: UrbanHeatInput) -> UrbanHeatResult:
    thermal = _thermal_score(inp)
    mortality = _mortality_score(inp)
    adaptation = _adaptation_score(inp)
    equity = _equity_score(inp)
    comp = _composite(thermal, mortality, adaptation, equity)
    risk = _risk_level(comp)
    pattern = _heat_pattern(inp)
    sev = _severity(risk)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return UrbanHeatResult(
        entity_id=inp.entity_id,
        city_type=inp.city_type,
        region=inp.region,
        thermal_score=thermal,
        mortality_score=mortality,
        adaptation_score=adaptation,
        equity_score=equity,
        composite_score=comp,
        risk_level=risk,
        heat_pattern=pattern,
        severity=sev,
        recommended_action=action,
        signal=sig,
        heat_island_intensity_index=inp.heat_island_intensity_index,
        extreme_heat_mortality_rate=inp.extreme_heat_mortality_rate,
    )


class UrbanHeatEngine:
    def analyze(self, entities: List[UrbanHeatInput]) -> Dict[str, Any]:
        results = [analyze_urban_heat(e) for e in entities]
        n = len(results) or 1

        risk_distribution: Dict[str, int] = {}
        pattern_distribution: Dict[str, int] = {}
        severity_distribution: Dict[str, int] = {}
        action_distribution: Dict[str, int] = {}

        total_composite = 0.0
        critical_count = 0
        high_count = 0
        moderate_count = 0
        low_count = 0

        for r in results:
            risk_distribution[r.risk_level] = risk_distribution.get(r.risk_level, 0) + 1
            pattern_distribution[r.heat_pattern] = pattern_distribution.get(r.heat_pattern, 0) + 1
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

        avg_composite = round(total_composite / n, 2)
        summ = self.summary(
            results,
            avg_composite,
            critical_count,
            high_count,
            moderate_count,
            low_count,
            pattern_distribution,
            risk_distribution,
            severity_distribution,
            action_distribution,
        )

        return {
            "entities": [r.to_dict() for r in results],
            "summary": summ,
        }

    def summary(
        self,
        results: List[UrbanHeatResult],
        avg_composite: float,
        critical_count: int,
        high_count: int,
        moderate_count: int,
        low_count: int,
        pattern_distribution: Dict[str, int],
        risk_distribution: Dict[str, int],
        severity_distribution: Dict[str, int],
        action_distribution: Dict[str, int],
    ) -> Dict[str, Any]:
        return {
            "module_id": 354,
            "module_name": "Urban Heat Island & City Climate Emergency Intelligence Engine",
            "total_entities": len(results),
            "critical_count": critical_count,
            "high_count": high_count,
            "moderate_count": moderate_count,
            "low_count": low_count,
            "avg_composite": avg_composite,
            "pattern_distribution": pattern_distribution,
            "risk_distribution": risk_distribution,
            "severity_distribution": severity_distribution,
            "action_distribution": action_distribution,
            "avg_estimated_urban_heat_index": round(avg_composite / 100 * 10, 2),
        }
