from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class MicroplasticsHealthInput:
    entity_id: str
    exposure_route: str
    region: str
    blood_microplastic_concentration: float
    lung_particle_accumulation: float
    digestive_system_exposure: float
    endocrine_disruption_risk: float
    cardiovascular_inflammation: float
    placental_crossing_rate: float
    neurotoxicity_indicator: float
    carcinogenicity_evidence: float
    daily_ingestion_estimate: float
    air_inhalation_intensity: float
    food_packaging_leaching: float
    seafood_contamination: float
    drinking_water_particles: float
    skin_absorption_rate: float
    chemical_additive_toxicity: float
    bioaccumulation_factor: float
    regulatory_detection_gap: float


@dataclass
class MicroplasticsHealthResult:
    entity_id: str
    exposure_route: str
    region: str
    exposure_score: float
    health_score: float
    source_score: float
    governance_score: float
    composite_score: float
    risk_level: str
    health_pattern: str
    severity: str
    recommended_action: str
    signal: str
    blood_microplastic_concentration: float
    lung_particle_accumulation: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "exposure_route": self.exposure_route,
            "region": self.region,
            "exposure_score": self.exposure_score,
            "health_score": self.health_score,
            "source_score": self.source_score,
            "governance_score": self.governance_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "health_pattern": self.health_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "blood_microplastic_concentration": self.blood_microplastic_concentration,
            "lung_particle_accumulation": self.lung_particle_accumulation,
        }


def _exposure_score(e: MicroplasticsHealthInput) -> float:
    raw = (
        e.blood_microplastic_concentration * 0.4
        + e.lung_particle_accumulation * 0.35
        + e.digestive_system_exposure * 0.25
    ) * 100
    return round(raw * 100) / 100


def _health_score(e: MicroplasticsHealthInput) -> float:
    raw = (
        e.endocrine_disruption_risk * 0.4
        + e.cardiovascular_inflammation * 0.35
        + e.neurotoxicity_indicator * 0.25
    ) * 100
    return round(raw * 100) / 100


def _source_score(e: MicroplasticsHealthInput) -> float:
    raw = (
        e.food_packaging_leaching * 0.4
        + e.seafood_contamination * 0.35
        + e.drinking_water_particles * 0.25
    ) * 100
    return round(raw * 100) / 100


def _governance_score(e: MicroplasticsHealthInput) -> float:
    raw = (
        e.regulatory_detection_gap * 0.4
        + e.chemical_additive_toxicity * 0.35
        + e.bioaccumulation_factor * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    exposure: float,
    health: float,
    source: float,
    governance: float,
) -> float:
    return round(
        (exposure * 0.30 + health * 0.25 + source * 0.25 + governance * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _health_pattern(e: MicroplasticsHealthInput) -> str:
    if e.endocrine_disruption_risk > 0.85 and e.chemical_additive_toxicity > 0.80:
        return "endocrine_disruption_epidemic"
    if e.cardiovascular_inflammation > 0.85 and e.blood_microplastic_concentration > 0.80:
        return "cardiovascular_microplastic_crisis"
    if e.placental_crossing_rate > 0.85 and e.neurotoxicity_indicator > 0.80:
        return "maternal_fetal_exposure_trap"
    if e.seafood_contamination > 0.85 and e.food_packaging_leaching > 0.80:
        return "food_chain_saturation_collapse"
    if e.regulatory_detection_gap > 0.85 and e.bioaccumulation_factor > 0.80:
        return "regulatory_threshold_vacuum"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_microplastiques_santé_systémique"
    if composite >= 40:
        return "crise_contamination_microplastique_majeure"
    if composite >= 20:
        return "exposition_microplastique_structurelle"
    return "surveillance_microplastiques_continue"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_décontamination_microplastique_critique"
    if risk == "high":
        return "réduction_exposition_sources_microplastiques_prioritaires"
    if risk == "moderate":
        return "renforcement_détection_régulation_microplastiques"
    return "veille_exposition_microplastique_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise microplastiques santé systémique — impact sanitaire en péril"
    if risk == "high":
        return "🟠 Crise contamination microplastique majeure détectée"
    if risk == "moderate":
        return "🟡 Exposition microplastique structurelle active"
    return "🟢 Surveillance microplastiques en cours"


def analyze_microplastics_health(e: MicroplasticsHealthInput) -> MicroplasticsHealthResult:
    exposure = _exposure_score(e)
    health = _health_score(e)
    source = _source_score(e)
    governance = _governance_score(e)
    composite = _composite_score(exposure, health, source, governance)
    risk = _risk_level(composite)
    pattern = _health_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return MicroplasticsHealthResult(
        entity_id=e.entity_id,
        exposure_route=e.exposure_route,
        region=e.region,
        exposure_score=exposure,
        health_score=health,
        source_score=source,
        governance_score=governance,
        composite_score=composite,
        risk_level=risk,
        health_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        blood_microplastic_concentration=e.blood_microplastic_concentration,
        lung_particle_accumulation=e.lung_particle_accumulation,
    )


class MicroplasticsHealthEngine:
    def analyze(self, entities: List[MicroplasticsHealthInput]) -> Dict[str, Any]:
        results = [analyze_microplastics_health(e) for e in entities]

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
        results: List[MicroplasticsHealthResult] = None,
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
            "module_id": 426,
            "module_name": "Microplastiques & Impact Santé Humaine Intelligence Engine",
            "total": len(results),
            "critical": critical_count,
            "high": high_count,
            "moderate": moderate_count,
            "low": low_count,
            "avg_composite": avg_composite,
            "pattern_distribution": pattern_distribution or {},
            "risk_distribution": risk_distribution or {},
            "severity_distribution": severity_distribution or {},
            "action_distribution": action_distribution or {},
            "avg_estimated_microplastic_health_index": round(avg_composite / 100 * 10, 2),
        }
