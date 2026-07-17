from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class AntibioticResistanceInput:
    entity_id: str
    health_context: str
    region: str
    AMR_mortality_acceleration_rate: float
    last_resort_antibiotic_failure_rate: float
    agricultural_antibiotic_overuse_index: float
    hospital_acquired_AMR_prevalence: float
    AMR_surveillance_gap_index: float
    new_antibiotic_pipeline_drought: float
    global_AMR_spread_velocity: float
    poor_hygiene_AMR_amplification: float
    AMR_travel_transmission_rate: float
    pharmaceutical_industry_AMR_neglect: float
    wastewater_AMR_contamination: float
    soil_AMR_reservoir_expansion: float
    AMR_impact_on_surgery_safety: float
    AMR_impact_on_cancer_treatment: float
    AMR_poverty_mortality_amplification: float
    one_health_AMR_approach_deficit: float
    AMR_geopolitical_cooperation_failure: float


@dataclass
class AntibioticResistanceResult:
    entity_id: str
    health_context: str
    region: str
    resistance_score: float
    pipeline_score: float
    transmission_score: float
    systemic_score: float
    composite_score: float
    risk_level: str
    amr_pattern: str
    severity: str
    recommended_action: str
    signal: str
    last_resort_antibiotic_failure_rate: float
    AMR_mortality_acceleration_rate: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "health_context": self.health_context,
            "region": self.region,
            "resistance_score": self.resistance_score,
            "pipeline_score": self.pipeline_score,
            "transmission_score": self.transmission_score,
            "systemic_score": self.systemic_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "amr_pattern": self.amr_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "last_resort_antibiotic_failure_rate": self.last_resort_antibiotic_failure_rate,
            "AMR_mortality_acceleration_rate": self.AMR_mortality_acceleration_rate,
        }


def _resistance_score(e: AntibioticResistanceInput) -> float:
    raw = (
        e.last_resort_antibiotic_failure_rate * 0.4
        + e.AMR_mortality_acceleration_rate * 0.35
        + e.global_AMR_spread_velocity * 0.25
    ) * 100
    return round(raw * 100) / 100


def _pipeline_score(e: AntibioticResistanceInput) -> float:
    raw = (
        e.new_antibiotic_pipeline_drought * 0.4
        + e.pharmaceutical_industry_AMR_neglect * 0.35
        + e.AMR_surveillance_gap_index * 0.25
    ) * 100
    return round(raw * 100) / 100


def _transmission_score(e: AntibioticResistanceInput) -> float:
    raw = (
        e.agricultural_antibiotic_overuse_index * 0.4
        + e.wastewater_AMR_contamination * 0.35
        + e.soil_AMR_reservoir_expansion * 0.25
    ) * 100
    return round(raw * 100) / 100


def _systemic_score(e: AntibioticResistanceInput) -> float:
    raw = (
        e.one_health_AMR_approach_deficit * 0.4
        + e.AMR_geopolitical_cooperation_failure * 0.35
        + e.AMR_poverty_mortality_amplification * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    resistance: float,
    pipeline: float,
    transmission: float,
    systemic: float,
) -> float:
    return round(
        (resistance * 0.30 + pipeline * 0.25 + transmission * 0.25 + systemic * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _amr_pattern(e: AntibioticResistanceInput) -> str:
    if e.last_resort_antibiotic_failure_rate >= 0.70 and e.new_antibiotic_pipeline_drought >= 0.65:
        return "post_antibiotic_era"
    if e.agricultural_antibiotic_overuse_index >= 0.70 and e.soil_AMR_reservoir_expansion >= 0.65:
        return "agricultural_AMR_reservoir"
    if e.hospital_acquired_AMR_prevalence >= 0.70 and e.AMR_impact_on_surgery_safety >= 0.65:
        return "hospital_AMR_catastrophe"
    if e.global_AMR_spread_velocity >= 0.70 and e.AMR_travel_transmission_rate >= 0.65:
        return "AMR_global_spread"
    if e.pharmaceutical_industry_AMR_neglect >= 0.70 and e.one_health_AMR_approach_deficit >= 0.65:
        return "pharmaceutical_neglect_crisis"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "ère_post-antibiotique_systémique"
    if composite >= 40:
        return "crise_résistance_antibiotique_majeure"
    if composite >= 20:
        return "résistance_antibiotique_structurelle"
    return "AMR_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_AMR_urgence_mondiale"
    if risk == "high":
        return "pipeline_antibiotique_urgence"
    if risk == "moderate":
        return "renforcement_surveillance_AMR_systémique"
    return "veille_AMR_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Ère post-antibiotique — résistance antimicrobienne critique"
    if risk == "high":
        return "🟠 Crise résistance antibiotique majeure détectée"
    if risk == "moderate":
        return "🟡 Résistance antibiotique structurelle active"
    return "🟢 AMR sous surveillance et contenu"


def analyze_antibiotic_resistance(e: AntibioticResistanceInput) -> AntibioticResistanceResult:
    resistance = _resistance_score(e)
    pipeline = _pipeline_score(e)
    transmission = _transmission_score(e)
    systemic = _systemic_score(e)
    composite = _composite_score(resistance, pipeline, transmission, systemic)
    risk = _risk_level(composite)
    pattern = _amr_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return AntibioticResistanceResult(
        entity_id=e.entity_id,
        health_context=e.health_context,
        region=e.region,
        resistance_score=resistance,
        pipeline_score=pipeline,
        transmission_score=transmission,
        systemic_score=systemic,
        composite_score=composite,
        risk_level=risk,
        amr_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        last_resort_antibiotic_failure_rate=e.last_resort_antibiotic_failure_rate,
        AMR_mortality_acceleration_rate=e.AMR_mortality_acceleration_rate,
    )


class AntibioticResistanceEngine:
    def analyze(self, entities: List[AntibioticResistanceInput]) -> Dict[str, Any]:
        results = [analyze_antibiotic_resistance(e) for e in entities]

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
            pattern_distribution[r.amr_pattern] = pattern_distribution.get(r.amr_pattern, 0) + 1
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
        results: List[AntibioticResistanceResult],
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
            "module_id": 358,
            "module_name": "Antibiotic Resistance & Post-Antibiotic Era Intelligence Engine",
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
            "avg_estimated_AMR_risk_index": round(avg_composite / 100 * 10, 2),
        }

    def summary(self, entities: List[AntibioticResistanceInput]) -> Dict[str, Any]:
        return self.analyze(entities)
