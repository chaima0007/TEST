from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class AlternativeProteinInput:
    entity_id: str
    protein_sector: str
    region: str
    cultivated_meat_cost_parity_proximity: float
    plant_based_market_saturation_risk: float
    precision_fermentation_disruption: float
    traditional_livestock_industry_disruption_speed: float
    regulatory_approval_barrier_level: float
    consumer_acceptance_gap: float
    intellectual_property_concentration_risk: float
    biotech_monopoly_in_food_production: float
    nutritional_transition_risk: float
    supply_chain_protein_transition_fragility: float
    small_farmer_displacement_rate: float
    food_sovereignty_tech_capture: float
    allergen_safety_gap_in_novel_proteins: float
    carbon_emission_protein_transition_benefit: float
    protein_transition_inequality: float
    food_culture_disruption_index: float
    cellular_agriculture_biosafety_risk: float


@dataclass
class AlternativeProteinResult:
    entity_id: str
    protein_sector: str
    region: str
    disruption_score: float
    monopoly_score: float
    transition_score: float
    safety_score: float
    composite_score: float
    risk_level: str
    protein_pattern: str
    severity: str
    recommended_action: str
    signal: str
    traditional_livestock_industry_disruption_speed: float
    biotech_monopoly_in_food_production: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "protein_sector": self.protein_sector,
            "region": self.region,
            "disruption_score": self.disruption_score,
            "monopoly_score": self.monopoly_score,
            "transition_score": self.transition_score,
            "safety_score": self.safety_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "protein_pattern": self.protein_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "traditional_livestock_industry_disruption_speed": self.traditional_livestock_industry_disruption_speed,
            "biotech_monopoly_in_food_production": self.biotech_monopoly_in_food_production,
        }


def _disruption_score(e: AlternativeProteinInput) -> float:
    raw = (
        e.cultivated_meat_cost_parity_proximity * 0.4
        + e.traditional_livestock_industry_disruption_speed * 0.35
        + e.precision_fermentation_disruption * 0.25
    ) * 100
    return round(raw * 100) / 100


def _monopoly_score(e: AlternativeProteinInput) -> float:
    raw = (
        e.biotech_monopoly_in_food_production * 0.4
        + e.intellectual_property_concentration_risk * 0.35
        + e.food_sovereignty_tech_capture * 0.25
    ) * 100
    return round(raw * 100) / 100


def _transition_score(e: AlternativeProteinInput) -> float:
    raw = (
        e.supply_chain_protein_transition_fragility * 0.4
        + e.small_farmer_displacement_rate * 0.35
        + e.protein_transition_inequality * 0.25
    ) * 100
    return round(raw * 100) / 100


def _safety_score(e: AlternativeProteinInput) -> float:
    raw = (
        e.allergen_safety_gap_in_novel_proteins * 0.4
        + e.cellular_agriculture_biosafety_risk * 0.35
        + e.nutritional_transition_risk * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    disruption: float,
    monopoly: float,
    transition: float,
    safety: float,
) -> float:
    return round(
        (disruption * 0.30 + monopoly * 0.25 + transition * 0.25 + safety * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _protein_pattern(e: AlternativeProteinInput) -> str:
    if e.traditional_livestock_industry_disruption_speed >= 0.70 and e.cultivated_meat_cost_parity_proximity >= 0.65:
        return "livestock_disruption_crisis"
    if e.biotech_monopoly_in_food_production >= 0.70 and e.intellectual_property_concentration_risk >= 0.65:
        return "biotech_food_monopoly"
    if e.food_sovereignty_tech_capture >= 0.70 and e.small_farmer_displacement_rate >= 0.65:
        return "food_sovereignty_capture"
    if e.protein_transition_inequality >= 0.70 and e.supply_chain_protein_transition_fragility >= 0.65:
        return "transition_inequality_trap"
    if e.cellular_agriculture_biosafety_risk >= 0.70 and e.allergen_safety_gap_in_novel_proteins >= 0.65:
        return "biosafety_novel_protein"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "disruption_alimentaire_systémique"
    if composite >= 40:
        return "transition_protéique_critique"
    if composite >= 20:
        return "restructuration_alimentaire_active"
    return "transition_protéique_gérée"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "gouvernance_urgente_disruption_alimentaire"
    if risk == "high":
        return "régulation_biotech_alimentaire_stricte"
    if risk == "moderate":
        return "accompagnement_transition_protéique_équitable"
    return "veille_disruption_alimentaire_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Disruption alimentaire systémique — transition protéique critique"
    if risk == "high":
        return "🟠 Transition protéique critique détectée"
    if risk == "moderate":
        return "🟡 Restructuration alimentaire active en cours"
    return "🟢 Transition protéique gérée et suivie"


def analyze_alternative_protein(e: AlternativeProteinInput) -> AlternativeProteinResult:
    disruption = _disruption_score(e)
    monopoly = _monopoly_score(e)
    transition = _transition_score(e)
    safety = _safety_score(e)
    composite = _composite_score(disruption, monopoly, transition, safety)
    risk = _risk_level(composite)
    pattern = _protein_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    signal = _signal(risk)

    return AlternativeProteinResult(
        entity_id=e.entity_id,
        protein_sector=e.protein_sector,
        region=e.region,
        disruption_score=disruption,
        monopoly_score=monopoly,
        transition_score=transition,
        safety_score=safety,
        composite_score=composite,
        risk_level=risk,
        protein_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=signal,
        traditional_livestock_industry_disruption_speed=e.traditional_livestock_industry_disruption_speed,
        biotech_monopoly_in_food_production=e.biotech_monopoly_in_food_production,
    )


class AlternativeProteinEngine:
    def analyze(self, entities: List[AlternativeProteinInput]) -> Dict[str, Any]:
        results = [analyze_alternative_protein(e) for e in entities]
        return self._build_summary([r.to_dict() for r in results])

    def _build_summary(self, entity_dicts: List[Dict[str, Any]]) -> Dict[str, Any]:
        risk_distribution: Dict[str, int] = {}
        pattern_distribution: Dict[str, int] = {}
        severity_distribution: Dict[str, int] = {}
        action_distribution: Dict[str, int] = {}

        total_composite = 0.0
        critical_count = 0
        high_count = 0
        moderate_count = 0
        low_count = 0

        for r in entity_dicts:
            risk = r["risk_level"]
            risk_distribution[risk] = risk_distribution.get(risk, 0) + 1
            pattern_distribution[r["protein_pattern"]] = pattern_distribution.get(r["protein_pattern"], 0) + 1
            severity_distribution[r["severity"]] = severity_distribution.get(r["severity"], 0) + 1
            action_distribution[r["recommended_action"]] = action_distribution.get(r["recommended_action"], 0) + 1
            total_composite += r["composite_score"]
            if risk == "critical":
                critical_count += 1
            elif risk == "high":
                high_count += 1
            elif risk == "moderate":
                moderate_count += 1
            else:
                low_count += 1

        n = len(entity_dicts) or 1
        avg_composite = round(total_composite / n * 10) / 10

        return {
            "module_id": 349,
            "module_name": "Alternative Protein & Food Tech Disruption Intelligence Engine",
            "total_entities": len(entity_dicts),
            "critical_count": critical_count,
            "high_count": high_count,
            "moderate_count": moderate_count,
            "low_count": low_count,
            "avg_composite": avg_composite,
            "pattern_distribution": pattern_distribution,
            "risk_distribution": risk_distribution,
            "severity_distribution": severity_distribution,
            "action_distribution": action_distribution,
            "avg_estimated_protein_disruption_index": round(avg_composite / 100 * 10, 2),
        }

    def summary(self, entities: List[AlternativeProteinInput]) -> Dict[str, Any]:
        results = [analyze_alternative_protein(e) for e in entities]
        entity_dicts = [r.to_dict() for r in results]

        risk_distribution: Dict[str, int] = {}
        pattern_distribution: Dict[str, int] = {}
        severity_distribution: Dict[str, int] = {}
        action_distribution: Dict[str, int] = {}

        total_composite = 0.0
        critical_count = 0
        high_count = 0
        moderate_count = 0
        low_count = 0

        for r in entity_dicts:
            risk = r["risk_level"]
            risk_distribution[risk] = risk_distribution.get(risk, 0) + 1
            pattern_distribution[r["protein_pattern"]] = pattern_distribution.get(r["protein_pattern"], 0) + 1
            severity_distribution[r["severity"]] = severity_distribution.get(r["severity"], 0) + 1
            action_distribution[r["recommended_action"]] = action_distribution.get(r["recommended_action"], 0) + 1
            total_composite += r["composite_score"]
            if risk == "critical":
                critical_count += 1
            elif risk == "high":
                high_count += 1
            elif risk == "moderate":
                moderate_count += 1
            else:
                low_count += 1

        n = len(entity_dicts) or 1
        avg_composite = round(total_composite / n * 10) / 10

        return {
            "module_id": 349,
            "module_name": "Alternative Protein & Food Tech Disruption Intelligence Engine",
            "total_entities": len(entity_dicts),
            "critical_count": critical_count,
            "high_count": high_count,
            "moderate_count": moderate_count,
            "low_count": low_count,
            "avg_composite": avg_composite,
            "pattern_distribution": pattern_distribution,
            "risk_distribution": risk_distribution,
            "severity_distribution": severity_distribution,
            "action_distribution": action_distribution,
            "avg_estimated_protein_disruption_index": round(avg_composite / 100 * 10, 2),
        }
