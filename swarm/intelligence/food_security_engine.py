from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class FoodSecurityInput:
    entity_id: str
    food_system_type: str
    region: str
    acute_hunger_prevalence: float
    famine_risk_level: float
    agricultural_production_collapse: float
    climate_crop_failure: float
    supply_chain_disruption_food: float
    price_volatility_extreme: float
    seed_monopoly_risk: float
    water_food_nexus_stress: float
    conflict_food_weaponization: float
    food_import_dependency: float
    nutrition_transition_risk: float
    smallholder_collapse: float
    fertilizer_supply_crisis: float
    food_waste_system_failure: float
    urban_food_desert_expansion: float
    WFP_funding_gap: float
    geopolitical_food_coercion: float


@dataclass
class FoodSecurityResult:
    entity_id: str
    food_system_type: str
    region: str
    hunger_score: float
    production_score: float
    access_score: float
    systemic_score: float
    composite_score: float
    risk_level: str
    food_pattern: str
    severity: str
    recommended_action: str
    signal: str
    acute_hunger_prevalence: float
    famine_risk_level: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "food_system_type": self.food_system_type,
            "region": self.region,
            "hunger_score": self.hunger_score,
            "production_score": self.production_score,
            "access_score": self.access_score,
            "systemic_score": self.systemic_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "food_pattern": self.food_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "acute_hunger_prevalence": self.acute_hunger_prevalence,
            "famine_risk_level": self.famine_risk_level,
        }


def _hunger_score(e: FoodSecurityInput) -> float:
    raw = (
        e.acute_hunger_prevalence * 0.4
        + e.famine_risk_level * 0.35
        + e.conflict_food_weaponization * 0.25
    ) * 100
    return round(raw * 100) / 100


def _production_score(e: FoodSecurityInput) -> float:
    raw = (
        e.agricultural_production_collapse * 0.4
        + e.climate_crop_failure * 0.35
        + e.smallholder_collapse * 0.25
    ) * 100
    return round(raw * 100) / 100


def _access_score(e: FoodSecurityInput) -> float:
    raw = (
        e.supply_chain_disruption_food * 0.4
        + e.price_volatility_extreme * 0.35
        + e.food_import_dependency * 0.25
    ) * 100
    return round(raw * 100) / 100


def _systemic_score(e: FoodSecurityInput) -> float:
    raw = (
        e.geopolitical_food_coercion * 0.4
        + e.seed_monopoly_risk * 0.35
        + e.fertilizer_supply_crisis * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    hunger: float,
    production: float,
    access: float,
    systemic: float,
) -> float:
    return round(
        (hunger * 0.30 + production * 0.25 + access * 0.25 + systemic * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _food_pattern(e: FoodSecurityInput) -> str:
    if e.famine_risk_level > 0.85 and e.acute_hunger_prevalence > 0.80:
        return "famine_emergency"
    if e.agricultural_production_collapse > 0.85 and e.climate_crop_failure > 0.80:
        return "agricultural_collapse"
    if e.supply_chain_disruption_food > 0.85 and e.price_volatility_extreme > 0.80:
        return "food_supply_chain_crisis"
    if e.geopolitical_food_coercion > 0.80 and e.food_import_dependency > 0.75:
        return "food_geopolitical_weapon"
    if e.seed_monopoly_risk > 0.80 and e.fertilizer_supply_crisis > 0.75:
        return "seed_fertilizer_monopoly_crisis"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "famine_systémique_catastrophique"
    if composite >= 40:
        return "crise_alimentaire_majeure"
    if composite >= 20:
        return "insécurité_alimentaire_structurelle"
    return "système_alimentaire_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_humanitaire_urgente_famine"
    if risk == "high":
        return "mobilisation_aide_alimentaire_accélérée"
    if risk == "moderate":
        return "renforcement_résilience_alimentaire"
    return "veille_sécurité_alimentaire_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Famine systémique — effondrement alimentaire catastrophique imminent"
    if risk == "high":
        return "🟠 Crise alimentaire majeure détectée"
    if risk == "moderate":
        return "🟡 Insécurité alimentaire structurelle active"
    return "🟢 Système alimentaire sous surveillance"


def analyze_food_security(e: FoodSecurityInput) -> FoodSecurityResult:
    hunger = _hunger_score(e)
    production = _production_score(e)
    access = _access_score(e)
    systemic = _systemic_score(e)
    composite = _composite_score(hunger, production, access, systemic)
    risk = _risk_level(composite)
    pattern = _food_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return FoodSecurityResult(
        entity_id=e.entity_id,
        food_system_type=e.food_system_type,
        region=e.region,
        hunger_score=hunger,
        production_score=production,
        access_score=access,
        systemic_score=systemic,
        composite_score=composite,
        risk_level=risk,
        food_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        acute_hunger_prevalence=e.acute_hunger_prevalence,
        famine_risk_level=e.famine_risk_level,
    )


class FoodSecurityEngine:
    def analyze(self, entities: List[FoodSecurityInput]) -> Dict[str, Any]:
        results = [analyze_food_security(e) for e in entities]

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
            pattern_distribution[r.food_pattern] = pattern_distribution.get(r.food_pattern, 0) + 1
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
        results: List[FoodSecurityResult] = None,
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
        # summary() returns exactly 13 keys
        return {
            "module_id": 387,
            "module_name": "Global Food Security & Famine Intelligence Engine",
            "total": len(results),
            "critical": critical_count,
            "high": high_count,
            "moderate": moderate_count,
            "low": low_count,
            "avg_composite": avg_composite,
            "risk_distribution": risk_distribution or {},
            "pattern_distribution": pattern_distribution or {},
            "severity_distribution": severity_distribution or {},
            "action_distribution": action_distribution or {},
            "avg_estimated_food_security_index": round(avg_composite / 100 * 10, 2),
        }
