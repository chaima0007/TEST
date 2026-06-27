from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class SoilCarbonInput:
    entity_id: str
    soil_type: str
    region: str
    carbon_loss_rate: float
    organic_matter_depletion: float
    tillage_intensity: float
    erosion_rate: float
    sequestration_potential: float
    regenerative_adoption: float
    cover_crop_use: float
    market_offset_credibility: float
    policy_incentive_effectiveness: float
    biodiversity_indicator: float
    fungal_network_health: float
    heavy_metal_contamination: float
    monoculture_pressure: float
    irrigation_salinization: float
    drought_vulnerability: float
    carbon_credit_fraud_risk: float
    farmer_income_impact: float


@dataclass
class SoilCarbonResult:
    entity_id: str
    soil_type: str
    region: str
    degradation_score: float
    sequestration_score: float
    policy_score: float
    biodiversity_score: float
    composite_score: float
    risk_level: str
    carbon_pattern: str
    severity: str
    recommended_action: str
    signal: str
    carbon_loss_rate: float
    sequestration_potential: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "soil_type": self.soil_type,
            "region": self.region,
            "degradation_score": self.degradation_score,
            "sequestration_score": self.sequestration_score,
            "policy_score": self.policy_score,
            "biodiversity_score": self.biodiversity_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "carbon_pattern": self.carbon_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "carbon_loss_rate": self.carbon_loss_rate,
            "sequestration_potential": self.sequestration_potential,
        }


def _degradation_score(e: SoilCarbonInput) -> float:
    raw = (
        e.carbon_loss_rate * 0.4
        + e.organic_matter_depletion * 0.35
        + e.erosion_rate * 0.25
    ) * 100
    return round(raw * 100) / 100


def _sequestration_score(e: SoilCarbonInput) -> float:
    raw = (
        (1.0 - e.sequestration_potential) * 0.4
        + (1.0 - e.regenerative_adoption) * 0.35
        + (1.0 - e.cover_crop_use) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _policy_score(e: SoilCarbonInput) -> float:
    raw = (
        (1.0 - e.policy_incentive_effectiveness) * 0.4
        + (1.0 - e.market_offset_credibility) * 0.35
        + e.carbon_credit_fraud_risk * 0.25
    ) * 100
    return round(raw * 100) / 100


def _biodiversity_score(e: SoilCarbonInput) -> float:
    raw = (
        (1.0 - e.biodiversity_indicator) * 0.4
        + (1.0 - e.fungal_network_health) * 0.35
        + e.monoculture_pressure * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    degradation: float,
    sequestration: float,
    policy: float,
    biodiversity: float,
) -> float:
    return round(
        (
            degradation * 0.30
            + sequestration * 0.25
            + policy * 0.25
            + biodiversity * 0.20
        )
        * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _carbon_pattern(e: SoilCarbonInput) -> str:
    if e.carbon_loss_rate > 0.85 and e.organic_matter_depletion > 0.80:
        return "carbon_debt_acceleration"
    if e.tillage_intensity > 0.85 and e.erosion_rate > 0.80:
        return "tillage_erosion_crisis"
    if e.sequestration_potential > 0.80 and e.regenerative_adoption < 0.20:
        return "rewilding_sequestration_collapse"
    if e.carbon_credit_fraud_risk > 0.80 and e.market_offset_credibility < 0.25:
        return "market_greenwashing_fraud"
    if e.fungal_network_health < 0.20 and e.monoculture_pressure > 0.80:
        return "soil_microbiome_collapse"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_carbone_sol_systémique"
    if composite >= 40:
        return "dégradation_sol_majeure"
    if composite >= 20:
        return "appauvrissement_sol_structurel"
    return "sol_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_restauration_sol_critique"
    if risk == "high":
        return "programme_séquestration_carbone_accéléré"
    if risk == "moderate":
        return "renforcement_pratiques_régénératives"
    return "veille_carbone_sol_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise carbone sol systémique — séquestration en péril immédiat"
    if risk == "high":
        return "🟠 Dégradation sol majeure — action urgente requise"
    if risk == "moderate":
        return "🟡 Appauvrissement sol structurel détecté"
    return "🟢 Sol sous surveillance carbone"


def analyze_soil_carbon(e: SoilCarbonInput) -> SoilCarbonResult:
    degradation = _degradation_score(e)
    sequestration = _sequestration_score(e)
    policy = _policy_score(e)
    biodiversity = _biodiversity_score(e)
    composite = _composite_score(degradation, sequestration, policy, biodiversity)
    risk = _risk_level(composite)
    pattern = _carbon_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return SoilCarbonResult(
        entity_id=e.entity_id,
        soil_type=e.soil_type,
        region=e.region,
        degradation_score=degradation,
        sequestration_score=sequestration,
        policy_score=policy,
        biodiversity_score=biodiversity,
        composite_score=composite,
        risk_level=risk,
        carbon_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        carbon_loss_rate=e.carbon_loss_rate,
        sequestration_potential=e.sequestration_potential,
    )


class SoilCarbonEngine:
    def analyze(self, entities: List[SoilCarbonInput]) -> Dict[str, Any]:
        results = [analyze_soil_carbon(e) for e in entities]

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
            pattern_distribution[r.carbon_pattern] = pattern_distribution.get(r.carbon_pattern, 0) + 1
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
        results: List[SoilCarbonResult] = None,
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
            "module_id": 409,
            "module_name": "Carbone Sol Agricole & Séquestration Intelligence Engine",
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
            "avg_estimated_soil_carbon_index": round(avg_composite / 100 * 10, 2),
        }
