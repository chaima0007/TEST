from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class InsuranceClimateInput:
    entity_id: str
    risk_category: str
    region: str
    uninsurability_rate: float
    premium_increase_trajectory: float
    insurer_market_exit_rate: float
    government_backstop_dependence: float
    stranded_property_value: float
    flood_zone_exposure: float
    wildfire_risk_penetration: float
    storm_surge_vulnerability: float
    regulatory_solvency_risk: float
    reinsurance_withdrawal: float
    parametric_solution_gap: float
    low_income_exposure: float
    mortgage_market_contagion: float
    infrastructure_coverage_gap: float
    climate_model_uncertainty: float
    political_risk_influence: float
    innovation_solution_adoption: float


@dataclass
class InsuranceClimateResult:
    entity_id: str
    risk_category: str
    region: str
    uninsurability_score: float
    affordability_score: float
    market_failure_score: float
    systemic_score: float
    composite_score: float
    risk_level: str
    insurance_pattern: str
    severity: str
    recommended_action: str
    signal: str
    uninsurability_rate: float
    reinsurance_withdrawal: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "risk_category": self.risk_category,
            "region": self.region,
            "uninsurability_score": self.uninsurability_score,
            "affordability_score": self.affordability_score,
            "market_failure_score": self.market_failure_score,
            "systemic_score": self.systemic_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "insurance_pattern": self.insurance_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "uninsurability_rate": self.uninsurability_rate,
            "reinsurance_withdrawal": self.reinsurance_withdrawal,
        }


def _uninsurability_score(e: InsuranceClimateInput) -> float:
    raw = (
        e.uninsurability_rate * 0.4
        + e.insurer_market_exit_rate * 0.35
        + e.flood_zone_exposure * 0.25
    ) * 100
    return round(raw * 100) / 100


def _affordability_score(e: InsuranceClimateInput) -> float:
    raw = (
        e.premium_increase_trajectory * 0.4
        + e.low_income_exposure * 0.35
        + e.parametric_solution_gap * 0.25
    ) * 100
    return round(raw * 100) / 100


def _market_failure_score(e: InsuranceClimateInput) -> float:
    raw = (
        e.reinsurance_withdrawal * 0.4
        + e.government_backstop_dependence * 0.35
        + e.regulatory_solvency_risk * 0.25
    ) * 100
    return round(raw * 100) / 100


def _systemic_score(e: InsuranceClimateInput) -> float:
    raw = (
        e.mortgage_market_contagion * 0.4
        + e.stranded_property_value * 0.35
        + e.infrastructure_coverage_gap * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    uninsurability: float,
    affordability: float,
    market_failure: float,
    systemic: float,
) -> float:
    return round(
        (
            uninsurability * 0.30
            + affordability * 0.25
            + market_failure * 0.25
            + systemic * 0.20
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


def _insurance_pattern(e: InsuranceClimateInput) -> str:
    if e.uninsurability_rate > 0.85 and e.insurer_market_exit_rate > 0.80:
        return "market_exit_uninsurability"
    if e.premium_increase_trajectory > 0.85 and e.low_income_exposure > 0.80:
        return "premium_unaffordability_crisis"
    if e.government_backstop_dependence > 0.85 and e.regulatory_solvency_risk > 0.80:
        return "government_insurer_last_resort"
    if e.stranded_property_value > 0.80 and e.mortgage_market_contagion > 0.75:
        return "stranded_asset_collapse"
    if e.reinsurance_withdrawal > 0.80 and e.infrastructure_coverage_gap > 0.75:
        return "systemic_financial_contagion"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_assurance_climatique_systémique"
    if composite >= 40:
        return "retrait_couverture_majeur_détecté"
    if composite >= 20:
        return "stress_marché_assurance_structurel"
    return "surveillance_risque_assurance_active"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_retrait_couverture_critique"
    if risk == "high":
        return "restructuration_marché_assurance_accélérée"
    if risk == "moderate":
        return "renforcement_mécanismes_assurance_publique"
    return "veille_risque_assurance_climatique_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise assurance climatique systémique — retrait couverture en péril"
    if risk == "high":
        return "🟠 Retrait couverture majeur détecté — marché en stress"
    if risk == "moderate":
        return "🟡 Stress marché assurance structurel actif"
    return "🟢 Risque assurance climatique sous surveillance"


def analyze_insurance_climate(e: InsuranceClimateInput) -> InsuranceClimateResult:
    uninsurability = _uninsurability_score(e)
    affordability = _affordability_score(e)
    market_failure = _market_failure_score(e)
    systemic = _systemic_score(e)
    composite = _composite_score(uninsurability, affordability, market_failure, systemic)
    risk = _risk_level(composite)
    pattern = _insurance_pattern(e)
    sev = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return InsuranceClimateResult(
        entity_id=e.entity_id,
        risk_category=e.risk_category,
        region=e.region,
        uninsurability_score=uninsurability,
        affordability_score=affordability,
        market_failure_score=market_failure,
        systemic_score=systemic,
        composite_score=composite,
        risk_level=risk,
        insurance_pattern=pattern,
        severity=sev,
        recommended_action=action,
        signal=sig,
        uninsurability_rate=e.uninsurability_rate,
        reinsurance_withdrawal=e.reinsurance_withdrawal,
    )


class InsuranceClimateEngine:
    def analyze(self, entities: List[InsuranceClimateInput]) -> Dict[str, Any]:
        results = [analyze_insurance_climate(e) for e in entities]

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
            pattern_distribution[r.insurance_pattern] = pattern_distribution.get(r.insurance_pattern, 0) + 1
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
        results: List[InsuranceClimateResult] = None,
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
            "module_id": 427,
            "module_name": "Assurance Risque Climatique & Retrait Couverture Intelligence Engine",
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
            "avg_estimated_insurance_retreat_index": round(avg_composite / 100 * 10, 2),
        }
