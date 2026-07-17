"""
Aging Infrastructure & Physical System Collapse Intelligence Engine
Module 392 — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
"""
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class AgingInfrastructureInput:
    entity_id: str
    infrastructure_type: str
    region: str
    # 17 float fields (0.0-1.0)
    structural_deterioration_rate: float = 0.0
    maintenance_deficit_severity: float = 0.0
    bridge_dam_collapse_risk: float = 0.0
    water_pipe_failure_rate: float = 0.0
    power_grid_aging_vulnerability: float = 0.0
    transport_network_degradation: float = 0.0
    investment_deficit_chronic: float = 0.0
    population_exposure_risk: float = 0.0
    failure_cascade_potential: float = 0.0
    regulatory_inspection_gap: float = 0.0
    climate_accelerated_aging: float = 0.0
    critical_failure_imminent: float = 0.0
    emergency_repair_capacity: float = 0.0
    insurance_withdrawal_risk: float = 0.0
    public_safety_exposure: float = 0.0
    economic_productivity_loss: float = 0.0
    political_will_deficit: float = 0.0


@dataclass
class AgingInfrastructureResult:
    entity_id: str
    infrastructure_type: str
    region: str
    deterioration_score: float
    safety_score: float
    investment_score: float
    cascade_score: float
    composite_score: float
    risk_level: str
    aging_pattern: str
    severity: str
    recommended_action: str
    signal: str
    structural_deterioration_rate: float
    critical_failure_imminent: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "infrastructure_type": self.infrastructure_type,
            "region": self.region,
            "deterioration_score": self.deterioration_score,
            "safety_score": self.safety_score,
            "investment_score": self.investment_score,
            "cascade_score": self.cascade_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "aging_pattern": self.aging_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "structural_deterioration_rate": self.structural_deterioration_rate,
            "critical_failure_imminent": self.critical_failure_imminent,
        }


def _deterioration_score(inp: AgingInfrastructureInput) -> float:
    raw = (
        inp.structural_deterioration_rate * 0.4
        + inp.transport_network_degradation * 0.35
        + inp.climate_accelerated_aging * 0.25
    ) * 100
    return round(raw * 100) / 100


def _safety_score(inp: AgingInfrastructureInput) -> float:
    raw = (
        inp.bridge_dam_collapse_risk * 0.4
        + inp.public_safety_exposure * 0.35
        + inp.critical_failure_imminent * 0.25
    ) * 100
    return round(raw * 100) / 100


def _investment_score(inp: AgingInfrastructureInput) -> float:
    raw = (
        inp.investment_deficit_chronic * 0.4
        + inp.maintenance_deficit_severity * 0.35
        + inp.political_will_deficit * 0.25
    ) * 100
    return round(raw * 100) / 100


def _cascade_score(inp: AgingInfrastructureInput) -> float:
    raw = (
        inp.failure_cascade_potential * 0.4
        + inp.population_exposure_risk * 0.35
        + inp.economic_productivity_loss * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(
    deterioration: float,
    safety: float,
    investment: float,
    cascade: float,
) -> float:
    return round(
        deterioration * 0.30
        + safety * 0.25
        + investment * 0.25
        + cascade * 0.20,
        2,
    )


def _aging_pattern(inp: AgingInfrastructureInput) -> str:
    if inp.critical_failure_imminent > 0.85 and inp.structural_deterioration_rate > 0.80:
        return "critical_infrastructure_imminent_failure"
    if inp.investment_deficit_chronic > 0.85 and inp.maintenance_deficit_severity > 0.80:
        return "investment_deficit_crisis"
    if inp.water_pipe_failure_rate > 0.85 and inp.power_grid_aging_vulnerability > 0.80:
        return "water_power_grid_collapse"
    if inp.bridge_dam_collapse_risk > 0.80 and inp.population_exposure_risk > 0.75:
        return "bridge_dam_catastrophe_risk"
    if inp.failure_cascade_potential > 0.80 and inp.climate_accelerated_aging > 0.75:
        return "failure_cascade_systemic"
    return "none"


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _severity(risk: str) -> str:
    if risk == "critical":
        return "urgence_effondrement_infrastructure_physique"
    if risk == "high":
        return "crise_vieillissement_infrastructure_majeure"
    if risk == "moderate":
        return "dégradation_structurelle_chronique"
    return "vieillissement_infrastructure_géré"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "plan_urgence_réhabilitation_infrastructure"
    if risk == "high":
        return "réparation_urgente_infrastructure_critique"
    if risk == "moderate":
        return "programme_maintenance_préventive_accéléré"
    return "veille_vieillissement_infrastructure_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Urgence effondrement infrastructure — défaillance physique imminente"
    if risk == "high":
        return "🟠 Crise vieillissement infrastructure majeure détectée"
    if risk == "moderate":
        return "🟡 Dégradation structurelle chronique active"
    return "🟢 Vieillissement infrastructure sous surveillance"


def analyze_aging_infrastructure(inp: AgingInfrastructureInput) -> AgingInfrastructureResult:
    deterioration = _deterioration_score(inp)
    safety = _safety_score(inp)
    investment = _investment_score(inp)
    cascade = _cascade_score(inp)
    comp = _composite(deterioration, safety, investment, cascade)
    risk = _risk_level(comp)
    pattern = _aging_pattern(inp)
    sev = _severity(risk)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return AgingInfrastructureResult(
        entity_id=inp.entity_id,
        infrastructure_type=inp.infrastructure_type,
        region=inp.region,
        deterioration_score=deterioration,
        safety_score=safety,
        investment_score=investment,
        cascade_score=cascade,
        composite_score=comp,
        risk_level=risk,
        aging_pattern=pattern,
        severity=sev,
        recommended_action=action,
        signal=sig,
        structural_deterioration_rate=inp.structural_deterioration_rate,
        critical_failure_imminent=inp.critical_failure_imminent,
    )


class AgingInfrastructureEngine:
    def analyze(self, entities: List[AgingInfrastructureInput]) -> Dict[str, Any]:
        results = [analyze_aging_infrastructure(e) for e in entities]
        n = len(results) or 1

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
            pattern_distribution[r.aging_pattern] = pattern_distribution.get(r.aging_pattern, 0) + 1
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

        avg_composite = round(total_composite / n, 2)
        summ = self.summary(
            results,
            avg_composite,
            critical_count,
            high_count,
            moderate_count,
            low_count,
            pattern_distribution,
            risk_distribution,
            severity_distribution,
            action_distribution,
        )

        return {
            "entities": [r.to_dict() for r in results],
            "summary": summ,
        }

    def summary(
        self,
        results: List[AgingInfrastructureResult],
        avg_composite: float,
        critical_count: int,
        high_count: int,
        moderate_count: int,
        low_count: int,
        pattern_distribution: Dict[str, int],
        risk_distribution: Dict[str, int],
        severity_distribution: Dict[str, int],
        action_distribution: Dict[str, int],
    ) -> Dict[str, Any]:
        return {
            "module_id": 392,
            "module_name": "Aging Infrastructure & Physical System Collapse Intelligence Engine",
            "total": len(results),
            "critical": critical_count,
            "high": high_count,
            "moderate": moderate_count,
            "low": low_count,
            "avg_composite": avg_composite,
            "distributions": {
                "risk": risk_distribution,
                "pattern": pattern_distribution,
                "severity": severity_distribution,
                "action": action_distribution,
            },
            "avg_estimated_infrastructure_aging_index": round(avg_composite / 100 * 10, 2),
        }
