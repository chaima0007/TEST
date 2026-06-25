from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class OceanAcidificationInput:
    entity_id: str
    marine_ecosystem: str
    region: str
    pH_decline_rate: float
    coral_bleaching_intensity: float
    calcification_failure_rate: float
    fishery_collapse_risk: float
    food_chain_disruption: float
    aragonite_saturation_collapse: float
    pteropod_dissolution_rate: float
    oyster_shellfish_collapse: float
    carbon_sink_degradation: float
    deep_ocean_acidification: float
    marine_biodiversity_loss: float
    coastal_economy_impact: float
    fishery_dependent_population: float
    tipping_point_proximity: float
    recovery_capacity: float
    co2_absorption_decline: float
    nutrient_cycle_disruption: float


@dataclass
class OceanAcidificationResult:
    entity_id: str
    marine_ecosystem: str
    region: str
    chemical_score: float
    biological_score: float
    food_system_score: float
    systemic_score: float
    composite_score: float
    risk_level: str
    ocean_pattern: str
    severity: str
    recommended_action: str
    signal: str
    pH_decline_rate: float
    coral_bleaching_intensity: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "marine_ecosystem": self.marine_ecosystem,
            "region": self.region,
            "chemical_score": self.chemical_score,
            "biological_score": self.biological_score,
            "food_system_score": self.food_system_score,
            "systemic_score": self.systemic_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "ocean_pattern": self.ocean_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "pH_decline_rate": self.pH_decline_rate,
            "coral_bleaching_intensity": self.coral_bleaching_intensity,
        }


def _chemical_score(e: OceanAcidificationInput) -> float:
    raw = (
        e.pH_decline_rate * 0.40
        + e.aragonite_saturation_collapse * 0.35
        + e.deep_ocean_acidification * 0.25
    ) * 100
    return round(raw * 100) / 100


def _biological_score(e: OceanAcidificationInput) -> float:
    raw = (
        e.coral_bleaching_intensity * 0.40
        + e.marine_biodiversity_loss * 0.35
        + e.pteropod_dissolution_rate * 0.25
    ) * 100
    return round(raw * 100) / 100


def _food_system_score(e: OceanAcidificationInput) -> float:
    raw = (
        e.fishery_collapse_risk * 0.40
        + e.food_chain_disruption * 0.35
        + e.oyster_shellfish_collapse * 0.25
    ) * 100
    return round(raw * 100) / 100


def _systemic_score(e: OceanAcidificationInput) -> float:
    raw = (
        e.carbon_sink_degradation * 0.40
        + e.tipping_point_proximity * 0.35
        + e.co2_absorption_decline * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    chemical: float,
    biological: float,
    food_system: float,
    systemic: float,
) -> float:
    return round(
        (chemical * 0.30 + biological * 0.25 + food_system * 0.25 + systemic * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _ocean_pattern(e: OceanAcidificationInput) -> str:
    if e.coral_bleaching_intensity > 0.85 and e.aragonite_saturation_collapse > 0.80:
        return "coral_reef_mass_extinction"
    if e.fishery_collapse_risk > 0.85 and e.food_chain_disruption > 0.80:
        return "fishery_ecosystem_collapse"
    if e.carbon_sink_degradation > 0.85 and e.co2_absorption_decline > 0.80:
        return "carbon_sink_failure"
    if e.oyster_shellfish_collapse > 0.80 and e.calcification_failure_rate > 0.75:
        return "shellfish_industry_extinction"
    if e.marine_biodiversity_loss > 0.80 and e.tipping_point_proximity > 0.75:
        return "marine_biodiversity_crisis"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "extinction_marine_systémique"
    if composite >= 40:
        return "crise_acidification_océanique_majeure"
    if composite >= 20:
        return "acidification_océanique_structurelle"
    return "écosystèmes_marins_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_écosystèmes_marins_critiques"
    if risk == "high":
        return "restauration_marine_accélérée"
    if risk == "moderate":
        return "renforcement_protection_milieux_marins"
    return "veille_acidification_océanique_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Extinction marine systémique — effondrement des écosystèmes océaniques"
    if risk == "high":
        return "🟠 Crise acidification océanique majeure détectée"
    if risk == "moderate":
        return "🟡 Acidification océanique structurelle active"
    return "🟢 Écosystèmes marins sous surveillance"


def analyze_ocean_acidification(e: OceanAcidificationInput) -> OceanAcidificationResult:
    chemical = _chemical_score(e)
    biological = _biological_score(e)
    food_system = _food_system_score(e)
    systemic = _systemic_score(e)
    composite = _composite_score(chemical, biological, food_system, systemic)
    risk = _risk_level(composite)
    pattern = _ocean_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return OceanAcidificationResult(
        entity_id=e.entity_id,
        marine_ecosystem=e.marine_ecosystem,
        region=e.region,
        chemical_score=chemical,
        biological_score=biological,
        food_system_score=food_system,
        systemic_score=systemic,
        composite_score=composite,
        risk_level=risk,
        ocean_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        pH_decline_rate=e.pH_decline_rate,
        coral_bleaching_intensity=e.coral_bleaching_intensity,
    )


class OceanAcidificationEngine:
    def analyze(self, entities: List[OceanAcidificationInput]) -> Dict[str, Any]:
        results = [analyze_ocean_acidification(e) for e in entities]

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
            pattern_distribution[r.ocean_pattern] = pattern_distribution.get(r.ocean_pattern, 0) + 1
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
        results: List[OceanAcidificationResult] = None,
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
            "module_id": 372,
            "module_name": "Ocean Acidification & Marine Ecosystem Collapse Intelligence Engine",
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
            "avg_estimated_ocean_acidification_index": round(avg_composite / 100 * 10, 2),
        }
