from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class EpigeneticHealthInput:
    entity_id: str
    health_domain: str
    region: str
    epigenetic_toxin_exposure_rate: float
    endocrine_disruption_prevalence: float
    microplastic_bioaccumulation_index: float
    air_quality_chronic_disease_coupling: float
    heavy_metal_cognitive_impairment_rate: float
    pesticide_epigenetic_impact: float
    forever_chemical_contamination_level: float
    gut_microbiome_disruption_index: float
    intergenerational_epigenetic_damage: float
    environmental_health_inequality: float
    chemical_industry_capture_of_regulation: float
    biodiversity_loss_health_cascade: float
    noise_pollution_cardiovascular_risk: float
    light_pollution_circadian_disruption: float
    urban_heat_mortality_index: float
    soil_contamination_food_chain_risk: float
    industrial_waste_community_exposure: float


@dataclass
class EpigeneticHealthResult:
    entity_id: str
    health_domain: str
    region: str
    chemical_score: float
    biological_score: float
    environmental_score: float
    social_score: float
    composite_score: float
    risk_level: str
    health_pattern: str
    severity: str
    recommended_action: str
    signal: str
    epigenetic_toxin_exposure_rate: float
    intergenerational_epigenetic_damage: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "health_domain": self.health_domain,
            "region": self.region,
            "chemical_score": self.chemical_score,
            "biological_score": self.biological_score,
            "environmental_score": self.environmental_score,
            "social_score": self.social_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "health_pattern": self.health_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "epigenetic_toxin_exposure_rate": self.epigenetic_toxin_exposure_rate,
            "intergenerational_epigenetic_damage": self.intergenerational_epigenetic_damage,
        }


def _chemical_score(e: EpigeneticHealthInput) -> float:
    raw = (
        e.epigenetic_toxin_exposure_rate * 0.4
        + e.forever_chemical_contamination_level * 0.35
        + e.endocrine_disruption_prevalence * 0.25
    ) * 100
    return round(raw * 100) / 100


def _biological_score(e: EpigeneticHealthInput) -> float:
    raw = (
        e.microplastic_bioaccumulation_index * 0.4
        + e.gut_microbiome_disruption_index * 0.35
        + e.intergenerational_epigenetic_damage * 0.25
    ) * 100
    return round(raw * 100) / 100


def _environmental_score(e: EpigeneticHealthInput) -> float:
    raw = (
        e.air_quality_chronic_disease_coupling * 0.4
        + e.urban_heat_mortality_index * 0.35
        + e.biodiversity_loss_health_cascade * 0.25
    ) * 100
    return round(raw * 100) / 100


def _social_score(e: EpigeneticHealthInput) -> float:
    raw = (
        e.environmental_health_inequality * 0.4
        + e.chemical_industry_capture_of_regulation * 0.35
        + e.industrial_waste_community_exposure * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    chemical: float,
    biological: float,
    environmental: float,
    social: float,
) -> float:
    return round(
        (chemical * 0.30 + biological * 0.25 + environmental * 0.25 + social * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _health_pattern(e: EpigeneticHealthInput) -> str:
    if e.epigenetic_toxin_exposure_rate >= 0.70 and e.intergenerational_epigenetic_damage >= 0.65:
        return "epigenetic_catastrophe"
    if e.forever_chemical_contamination_level >= 0.70 and e.endocrine_disruption_prevalence >= 0.65:
        return "chemical_body_burden"
    if e.microplastic_bioaccumulation_index >= 0.70 and e.gut_microbiome_disruption_index >= 0.65:
        return "microbiome_collapse"
    if e.environmental_health_inequality >= 0.70 and e.industrial_waste_community_exposure >= 0.65:
        return "environmental_injustice"
    if e.chemical_industry_capture_of_regulation >= 0.70 and e.air_quality_chronic_disease_coupling >= 0.65:
        return "regulatory_chemical_capture"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "catastrophe_sanitaire_environnementale"
    if composite >= 40:
        return "crise_santé_épigénétique_majeure"
    if composite >= 20:
        return "dégradation_santé_environnementale"
    return "santé_environnementale_contenue"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_sanitaire_urgente"
    if risk == "high":
        return "réglementation_chimique_stricte"
    if risk == "moderate":
        return "renforcement_prévention_environnementale"
    return "surveillance_épigénétique_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Catastrophe sanitaire environnementale — dommages épigénétiques systémiques"
    if risk == "high":
        return "🟠 Crise santé épigénétique majeure détectée"
    if risk == "moderate":
        return "🟡 Dégradation santé environnementale active"
    return "🟢 Santé environnementale relativement contenue"


def analyze_epigenetic_health(e: EpigeneticHealthInput) -> EpigeneticHealthResult:
    chemical = _chemical_score(e)
    biological = _biological_score(e)
    environmental = _environmental_score(e)
    social = _social_score(e)
    composite = _composite_score(chemical, biological, environmental, social)
    risk = _risk_level(composite)
    pattern = _health_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return EpigeneticHealthResult(
        entity_id=e.entity_id,
        health_domain=e.health_domain,
        region=e.region,
        chemical_score=chemical,
        biological_score=biological,
        environmental_score=environmental,
        social_score=social,
        composite_score=composite,
        risk_level=risk,
        health_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        epigenetic_toxin_exposure_rate=e.epigenetic_toxin_exposure_rate,
        intergenerational_epigenetic_damage=e.intergenerational_epigenetic_damage,
    )


class EpigeneticHealthEngine:
    def analyze(self, entities: List[EpigeneticHealthInput]) -> Dict[str, Any]:
        results = [analyze_epigenetic_health(e) for e in entities]

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
            pattern_distribution[r.health_pattern] = pattern_distribution.get(r.health_pattern, 0) + 1
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

        return self._summary(
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

    def _summary(
        self,
        results: List[EpigeneticHealthResult],
        risk_distribution: Dict[str, int],
        pattern_distribution: Dict[str, int],
        severity_distribution: Dict[str, int],
        action_distribution: Dict[str, int],
        avg_composite: float,
        critical_count: int,
        high_count: int,
        moderate_count: int,
        low_count: int,
    ) -> Dict[str, Any]:
        return {
            "module_id": 340,
            "module_name": "Epigenetic & Environmental Health Intelligence Engine",
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
            "avg_estimated_health_risk_index": round(avg_composite / 100 * 10, 2),
        }

    def summary(self, entities: List[EpigeneticHealthInput]) -> Dict[str, Any]:
        return self.analyze(entities)
