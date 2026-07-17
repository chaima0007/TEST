from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class UrbanFloodingInput:
    entity_id: str
    city_type: str
    region: str
    flood_frequency_increase: float
    impervious_surface_expansion: float
    stormwater_system_age: float
    drainage_capacity_deficit: float
    combined_sewer_overflow: float
    green_infrastructure_adoption: float
    early_warning_effectiveness: float
    emergency_response_capacity: float
    low_income_flood_exposure: float
    climate_vulnerability_index: float
    insurance_coverage_gap: float
    urban_heat_compounding: float
    sea_level_rise_interaction: float
    maintenance_budget_gap: float
    nature_based_solution_adoption: float
    informal_settlement_exposure: float
    urban_planning_integration: float


@dataclass
class UrbanFloodingResult:
    entity_id: str
    city_type: str
    region: str
    exposure_score: float
    infrastructure_score: float
    governance_score: float
    equity_score: float
    composite_score: float
    risk_level: str
    flood_pattern: str
    severity: str
    recommended_action: str
    signal: str
    drainage_capacity_deficit: float
    low_income_flood_exposure: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "city_type": self.city_type,
            "region": self.region,
            "exposure_score": self.exposure_score,
            "infrastructure_score": self.infrastructure_score,
            "governance_score": self.governance_score,
            "equity_score": self.equity_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "flood_pattern": self.flood_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "drainage_capacity_deficit": self.drainage_capacity_deficit,
            "low_income_flood_exposure": self.low_income_flood_exposure,
        }


def _exposure_score(e: UrbanFloodingInput) -> float:
    raw = (
        e.flood_frequency_increase * 0.40
        + e.impervious_surface_expansion * 0.35
        + e.sea_level_rise_interaction * 0.25
    ) * 100
    return round(raw * 100) / 100


def _infrastructure_score(e: UrbanFloodingInput) -> float:
    raw = (
        e.drainage_capacity_deficit * 0.40
        + e.stormwater_system_age * 0.35
        + e.maintenance_budget_gap * 0.25
    ) * 100
    return round(raw * 100) / 100


def _governance_score(e: UrbanFloodingInput) -> float:
    raw = (
        e.combined_sewer_overflow * 0.40
        + e.urban_planning_integration * 0.35
        + e.early_warning_effectiveness * 0.25
    ) * 100
    return round(raw * 100) / 100


def _equity_score(e: UrbanFloodingInput) -> float:
    raw = (
        e.low_income_flood_exposure * 0.40
        + e.informal_settlement_exposure * 0.35
        + e.insurance_coverage_gap * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    exposure: float,
    infrastructure: float,
    governance: float,
    equity: float,
) -> float:
    return round(
        (exposure * 0.30 + infrastructure * 0.25 + governance * 0.25 + equity * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _flood_pattern(e: UrbanFloodingInput) -> str:
    if e.stormwater_system_age > 0.85 and e.drainage_capacity_deficit > 0.80:
        return "stormwater_infrastructure_collapse"
    if e.informal_settlement_exposure > 0.85 and e.low_income_flood_exposure > 0.80:
        return "informal_settlement_flood_trap"
    if e.urban_heat_compounding > 0.85 and e.impervious_surface_expansion > 0.80:
        return "urban_heat_flood_compound"
    if e.combined_sewer_overflow > 0.80 and e.drainage_capacity_deficit > 0.75:
        return "drainage_capacity_failure"
    if e.maintenance_budget_gap > 0.80 and e.insurance_coverage_gap > 0.75:
        return "climate_adaptation_funding_gap"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_inondation_urbaine_systémique"
    if composite >= 40:
        return "crise_résilience_hydraulique_majeure"
    if composite >= 20:
        return "vulnérabilité_eaux_pluviales_structurelle"
    return "gestion_inondations_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_infrastructure_hydraulique_critique"
    if risk == "high":
        return "réhabilitation_accélérée_réseaux_eaux_pluviales"
    if risk == "moderate":
        return "renforcement_gouvernance_eaux_pluviales_urbaines"
    return "veille_résilience_inondations_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise inondation urbaine systémique — infrastructure hydraulique en péril"
    if risk == "high":
        return "🟠 Crise résilience hydraulique majeure détectée"
    if risk == "moderate":
        return "🟡 Vulnérabilité eaux pluviales structurelle active"
    return "🟢 Gestion inondations sous surveillance"


def analyze_urban_flooding(e: UrbanFloodingInput) -> UrbanFloodingResult:
    exposure = _exposure_score(e)
    infrastructure = _infrastructure_score(e)
    governance = _governance_score(e)
    equity = _equity_score(e)
    composite = _composite_score(exposure, infrastructure, governance, equity)
    risk = _risk_level(composite)
    pattern = _flood_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return UrbanFloodingResult(
        entity_id=e.entity_id,
        city_type=e.city_type,
        region=e.region,
        exposure_score=exposure,
        infrastructure_score=infrastructure,
        governance_score=governance,
        equity_score=equity,
        composite_score=composite,
        risk_level=risk,
        flood_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        drainage_capacity_deficit=e.drainage_capacity_deficit,
        low_income_flood_exposure=e.low_income_flood_exposure,
    )


class UrbanFloodingEngine:
    def analyze(self, entities: List[UrbanFloodingInput]) -> Dict[str, Any]:
        results = [analyze_urban_flooding(e) for e in entities]

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
            pattern_distribution[r.flood_pattern] = pattern_distribution.get(r.flood_pattern, 0) + 1
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
        results: List[UrbanFloodingResult] = None,
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
            "module_id": 429,
            "module_name": "Inondations Urbaines & Gestion Eaux Pluviales Intelligence Engine",
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
            "avg_estimated_flood_resilience_index": round(avg_composite / 100 * 10, 2),
        }
