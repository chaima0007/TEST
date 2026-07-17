from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class SoilDegradationInput:
    entity_id: str
    land_type: str
    region: str
    topsoil_loss_acceleration_rate: float
    soil_carbon_depletion_index: float
    microbiome_diversity_collapse: float
    desertification_expansion_rate: float
    agricultural_chemical_soil_toxicity: float
    compaction_crisis_density: float
    irrigation_salt_accumulation: float
    soil_erosion_from_extreme_weather: float
    land_conversion_pressure: float
    regenerative_agriculture_adoption_gap: float
    soil_acidification_rate: float
    phosphorus_depletion_trajectory: float
    groundwater_contamination_from_soil: float
    soil_food_web_collapse: float
    land_tenure_insecurity: float
    monoculture_soil_exhaustion_rate: float
    urban_soil_sealing_expansion: float


@dataclass
class SoilDegradationResult:
    entity_id: str
    land_type: str
    region: str
    physical_score: float
    chemical_score: float
    biological_score: float
    systemic_score: float
    composite_score: float
    risk_level: str
    soil_pattern: str
    severity: str
    recommended_action: str
    signal: str
    topsoil_loss_acceleration_rate: float
    desertification_expansion_rate: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "land_type": self.land_type,
            "region": self.region,
            "physical_score": self.physical_score,
            "chemical_score": self.chemical_score,
            "biological_score": self.biological_score,
            "systemic_score": self.systemic_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "soil_pattern": self.soil_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "topsoil_loss_acceleration_rate": self.topsoil_loss_acceleration_rate,
            "desertification_expansion_rate": self.desertification_expansion_rate,
        }


def _physical_score(e: SoilDegradationInput) -> float:
    raw = (
        e.topsoil_loss_acceleration_rate * 0.4
        + e.soil_erosion_from_extreme_weather * 0.35
        + e.compaction_crisis_density * 0.25
    ) * 100
    return round(raw * 100) / 100


def _chemical_score(e: SoilDegradationInput) -> float:
    raw = (
        e.agricultural_chemical_soil_toxicity * 0.4
        + e.soil_acidification_rate * 0.35
        + e.irrigation_salt_accumulation * 0.25
    ) * 100
    return round(raw * 100) / 100


def _biological_score(e: SoilDegradationInput) -> float:
    raw = (
        e.microbiome_diversity_collapse * 0.4
        + e.soil_food_web_collapse * 0.35
        + e.soil_carbon_depletion_index * 0.25
    ) * 100
    return round(raw * 100) / 100


def _systemic_score(e: SoilDegradationInput) -> float:
    raw = (
        e.desertification_expansion_rate * 0.4
        + e.monoculture_soil_exhaustion_rate * 0.35
        + e.regenerative_agriculture_adoption_gap * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    physical: float,
    chemical: float,
    biological: float,
    systemic: float,
) -> float:
    return round(
        (physical * 0.30 + chemical * 0.25 + biological * 0.25 + systemic * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _soil_pattern(e: SoilDegradationInput) -> str:
    if e.topsoil_loss_acceleration_rate >= 0.70 and e.monoculture_soil_exhaustion_rate >= 0.65:
        return "topsoil_extinction"
    if e.microbiome_diversity_collapse >= 0.70 and e.soil_food_web_collapse >= 0.65:
        return "soil_biome_collapse"
    if e.desertification_expansion_rate >= 0.70 and e.soil_erosion_from_extreme_weather >= 0.65:
        return "desertification_cascade"
    if e.agricultural_chemical_soil_toxicity >= 0.70 and e.soil_acidification_rate >= 0.65:
        return "chemical_soil_death"
    if e.phosphorus_depletion_trajectory >= 0.70 and e.soil_carbon_depletion_index >= 0.65:
        return "phosphorus_crisis"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "extinction_sol_systémique"
    if composite >= 40:
        return "crise_dégradation_sols_majeure"
    if composite >= 20:
        return "dégradation_sols_structurelle"
    return "sols_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "régénération_urgente_sols_critiques"
    if risk == "high":
        return "transition_agriculture_régénératrice_accélérée"
    if risk == "moderate":
        return "renforcement_protection_sols"
    return "veille_santé_sols_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Extinction sol systémique — fondement alimentaire en péril"
    if risk == "high":
        return "🟠 Crise dégradation sols majeure détectée"
    if risk == "moderate":
        return "🟡 Dégradation sols structurelle active"
    return "🟢 Santé sols sous surveillance"


def analyze_soil_degradation(e: SoilDegradationInput) -> SoilDegradationResult:
    physical = _physical_score(e)
    chemical = _chemical_score(e)
    biological = _biological_score(e)
    systemic = _systemic_score(e)
    composite = _composite_score(physical, chemical, biological, systemic)
    risk = _risk_level(composite)
    pattern = _soil_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return SoilDegradationResult(
        entity_id=e.entity_id,
        land_type=e.land_type,
        region=e.region,
        physical_score=physical,
        chemical_score=chemical,
        biological_score=biological,
        systemic_score=systemic,
        composite_score=composite,
        risk_level=risk,
        soil_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        topsoil_loss_acceleration_rate=e.topsoil_loss_acceleration_rate,
        desertification_expansion_rate=e.desertification_expansion_rate,
    )


class SoilDegradationEngine:
    def analyze(self, entities: List[SoilDegradationInput]) -> Dict[str, Any]:
        results = [analyze_soil_degradation(e) for e in entities]

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
            pattern_distribution[r.soil_pattern] = pattern_distribution.get(r.soil_pattern, 0) + 1
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

        n = len(results) or 1
        avg_composite = round(total_composite / n * 10) / 10

        return self.summary(
            results=results,
            risk_distribution=risk_distribution,
            pattern_distribution=pattern_distribution,
            severity_distribution=severity_distribution,
            action_distribution=action_distribution,
            avg_composite=avg_composite,
            critical_count=critical_count,
            high_count=high_count,
            moderate_count=moderate_count,
            low_count=low_count,
        )

    def summary(
        self,
        results: List[SoilDegradationResult] = None,
        risk_distribution: Dict[str, int] = None,
        pattern_distribution: Dict[str, int] = None,
        severity_distribution: Dict[str, int] = None,
        action_distribution: Dict[str, int] = None,
        avg_composite: float = 0.0,
        critical_count: int = 0,
        high_count: int = 0,
        moderate_count: int = 0,
        low_count: int = 0,
    ) -> Dict[str, Any]:
        results = results or []
        return {
            "module_id": 356,
            "module_name": "Soil Degradation & Land Collapse Intelligence Engine",
            "total_entities": len(results),
            "critical_count": critical_count,
            "high_count": high_count,
            "moderate_count": moderate_count,
            "low_count": low_count,
            "avg_composite": avg_composite,
            "pattern_distribution": pattern_distribution or {},
            "risk_distribution": risk_distribution or {},
            "severity_distribution": severity_distribution or {},
            "action_distribution": action_distribution or {},
            "avg_estimated_soil_degradation_index": round(avg_composite / 100 * 10, 2),
        }
