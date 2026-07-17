"""
Infrastructure Resilience & Critical System Failure Intelligence Engine — Module 351
Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
"""
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class InfrastructureResilienceInput:
    entity_id: str
    infrastructure_type: str
    region: str
    # 17 float fields (0.0–1.0)
    aging_infrastructure_deterioration_rate: float
    cascading_failure_interconnection_risk: float
    cyber_physical_attack_vulnerability: float
    climate_infrastructure_stress_index: float
    single_point_failure_density: float
    maintenance_investment_deficit: float
    emergency_response_capacity_gap: float
    backup_redundancy_inadequacy: float
    private_infrastructure_owner_underinvestment: float
    cross_sector_dependency_fragility: float
    extreme_weather_infrastructure_exposure: float
    infrastructure_workforce_shortage: float
    regulatory_enforcement_gap: float
    geopolitical_infrastructure_targeting_risk: float
    smart_infrastructure_vulnerability: float
    underground_infrastructure_neglect: float
    critical_node_attack_surface: float


@dataclass
class InfrastructureResilienceResult:
    entity_id: str
    infrastructure_type: str
    region: str
    physical_score: float
    cascade_score: float
    threat_score: float
    resilience_score: float
    composite_score: float
    risk_level: str
    infra_pattern: str
    severity: str
    recommended_action: str
    signal: str
    aging_infrastructure_deterioration_rate: float
    cascading_failure_interconnection_risk: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "infrastructure_type": self.infrastructure_type,
            "region": self.region,
            "physical_score": self.physical_score,
            "cascade_score": self.cascade_score,
            "threat_score": self.threat_score,
            "resilience_score": self.resilience_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "infra_pattern": self.infra_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "aging_infrastructure_deterioration_rate": self.aging_infrastructure_deterioration_rate,
            "cascading_failure_interconnection_risk": self.cascading_failure_interconnection_risk,
        }


def _physical_score(inp: InfrastructureResilienceInput) -> float:
    raw = (
        inp.aging_infrastructure_deterioration_rate * 0.4
        + inp.maintenance_investment_deficit * 0.35
        + inp.underground_infrastructure_neglect * 0.25
    ) * 100
    return round(raw * 100) / 100


def _cascade_score(inp: InfrastructureResilienceInput) -> float:
    raw = (
        inp.cascading_failure_interconnection_risk * 0.4
        + inp.cross_sector_dependency_fragility * 0.35
        + inp.single_point_failure_density * 0.25
    ) * 100
    return round(raw * 100) / 100


def _threat_score(inp: InfrastructureResilienceInput) -> float:
    raw = (
        inp.cyber_physical_attack_vulnerability * 0.4
        + inp.geopolitical_infrastructure_targeting_risk * 0.35
        + inp.smart_infrastructure_vulnerability * 0.25
    ) * 100
    return round(raw * 100) / 100


def _resilience_score(inp: InfrastructureResilienceInput) -> float:
    raw = (
        inp.backup_redundancy_inadequacy * 0.4
        + inp.emergency_response_capacity_gap * 0.35
        + inp.infrastructure_workforce_shortage * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(
    physical: float,
    cascade: float,
    threat: float,
    resilience: float,
) -> float:
    return round(
        physical * 0.30
        + cascade * 0.25
        + threat * 0.25
        + resilience * 0.20,
        2,
    )


def _infra_pattern(inp: InfrastructureResilienceInput) -> str:
    if inp.cascading_failure_interconnection_risk >= 0.70 and inp.cross_sector_dependency_fragility >= 0.65:
        return "cascading_infrastructure_collapse"
    if inp.aging_infrastructure_deterioration_rate >= 0.70 and inp.maintenance_investment_deficit >= 0.65:
        return "aging_critical_failure"
    if inp.cyber_physical_attack_vulnerability >= 0.70 and inp.smart_infrastructure_vulnerability >= 0.65:
        return "cyber_physical_attack"
    if inp.climate_infrastructure_stress_index >= 0.70 and inp.extreme_weather_infrastructure_exposure >= 0.65:
        return "climate_infrastructure_shock"
    if inp.backup_redundancy_inadequacy >= 0.70 and inp.emergency_response_capacity_gap >= 0.65:
        return "resilience_vacuum"
    return "none"


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "effondrement_infrastructure_critique"
    if composite >= 40:
        return "crise_résilience_systémique"
    if composite >= 20:
        return "fragilité_infrastructure_structurelle"
    return "infrastructure_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "réparation_urgente_infrastructure_critique"
    if risk == "high":
        return "plan_résilience_infrastructure_accéléré"
    if risk == "moderate":
        return "renforcement_redondance_systémique"
    return "veille_infrastructure_critique_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Effondrement infrastructure critique — défaillance systémique imminente"
    if risk == "high":
        return "🟠 Crise résilience systémique détectée"
    if risk == "moderate":
        return "🟡 Fragilité infrastructure structurelle active"
    return "🟢 Infrastructure critique sous surveillance"


def analyze(inp: InfrastructureResilienceInput) -> InfrastructureResilienceResult:
    phys = _physical_score(inp)
    casc = _cascade_score(inp)
    thrt = _threat_score(inp)
    resil = _resilience_score(inp)
    comp = _composite(phys, casc, thrt, resil)
    pat = _infra_pattern(inp)
    risk = _risk_level(comp)
    sev = _severity(comp)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return InfrastructureResilienceResult(
        entity_id=inp.entity_id,
        infrastructure_type=inp.infrastructure_type,
        region=inp.region,
        physical_score=phys,
        cascade_score=casc,
        threat_score=thrt,
        resilience_score=resil,
        composite_score=comp,
        risk_level=risk,
        infra_pattern=pat,
        severity=sev,
        recommended_action=action,
        signal=sig,
        aging_infrastructure_deterioration_rate=inp.aging_infrastructure_deterioration_rate,
        cascading_failure_interconnection_risk=inp.cascading_failure_interconnection_risk,
    )


class InfrastructureResilienceEngine:
    def __init__(self, inputs: List[InfrastructureResilienceInput]):
        self.inputs = inputs
        self.results: List[InfrastructureResilienceResult] = [analyze(i) for i in inputs]

    def analyze(self, entities: List[InfrastructureResilienceInput]) -> Dict[str, Any]:
        results = [analyze(e) for e in entities]
        return InfrastructureResilienceEngine.summary(results)

    @staticmethod
    def summary(results: List[InfrastructureResilienceResult]) -> Dict[str, Any]:
        n = len(results)
        if n == 0:
            return {}

        risk_distribution: Dict[str, int] = {}
        pattern_distribution: Dict[str, int] = {}
        severity_distribution: Dict[str, int] = {}
        action_distribution: Dict[str, int] = {}

        critical_count = 0
        high_count = 0
        moderate_count = 0
        low_count = 0
        total_composite = 0.0

        for r in results:
            risk_distribution[r.risk_level] = risk_distribution.get(r.risk_level, 0) + 1
            pattern_distribution[r.infra_pattern] = pattern_distribution.get(r.infra_pattern, 0) + 1
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

        avg_composite = round(total_composite / n, 1)

        return {
            "module_id": 351,
            "module_name": "Infrastructure Resilience & Critical System Failure Intelligence Engine",
            "total_entities": n,
            "critical_count": critical_count,
            "high_count": high_count,
            "moderate_count": moderate_count,
            "low_count": low_count,
            "avg_composite": avg_composite,
            "pattern_distribution": pattern_distribution,
            "risk_distribution": risk_distribution,
            "severity_distribution": severity_distribution,
            "action_distribution": action_distribution,
            "avg_estimated_infra_risk_index": round(avg_composite / 100 * 10, 2),
        }
