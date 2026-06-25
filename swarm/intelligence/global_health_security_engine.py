from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class GlobalHealthSecurityInput:
    entity_id: str
    health_system_type: str
    region: str
    pandemic_preparedness_gap: float
    surveillance_system_weakness: float
    healthcare_system_resilience: float
    international_coordination_failure: float
    WHO_funding_adequacy: float
    vaccine_manufacturing_capacity: float
    supply_chain_health_vulnerability: float
    health_worker_shortage: float
    IHR_compliance_failure: float
    diagnostic_capacity_gap: float
    PHEIC_response_speed: float
    cross_border_health_cooperation: float
    health_financing_gap: float
    antimicrobial_resistance_burden: float
    zoonotic_spillover_risk: float
    climate_health_nexus: float
    health_inequality_structural: float


@dataclass
class GlobalHealthSecurityResult:
    entity_id: str
    health_system_type: str
    region: str
    preparedness_score: float
    response_score: float
    governance_score: float
    equity_score: float
    composite_score: float
    risk_level: str
    ghs_pattern: str
    severity: str
    recommended_action: str
    signal: str
    pandemic_preparedness_gap: float
    IHR_compliance_failure: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "health_system_type": self.health_system_type,
            "region": self.region,
            "preparedness_score": self.preparedness_score,
            "response_score": self.response_score,
            "governance_score": self.governance_score,
            "equity_score": self.equity_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "ghs_pattern": self.ghs_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "pandemic_preparedness_gap": self.pandemic_preparedness_gap,
            "IHR_compliance_failure": self.IHR_compliance_failure,
        }


def _preparedness_score(e: GlobalHealthSecurityInput) -> float:
    raw = (
        e.pandemic_preparedness_gap * 0.4
        + e.surveillance_system_weakness * 0.35
        + e.diagnostic_capacity_gap * 0.25
    ) * 100
    return round(raw * 100) / 100


def _response_score(e: GlobalHealthSecurityInput) -> float:
    raw = (
        e.PHEIC_response_speed * 0.4
        + e.supply_chain_health_vulnerability * 0.35
        + e.vaccine_manufacturing_capacity * 0.25
    ) * 100
    return round(raw * 100) / 100


def _governance_score(e: GlobalHealthSecurityInput) -> float:
    raw = (
        e.IHR_compliance_failure * 0.4
        + e.international_coordination_failure * 0.35
        + e.WHO_funding_adequacy * 0.25
    ) * 100
    return round(raw * 100) / 100


def _equity_score(e: GlobalHealthSecurityInput) -> float:
    raw = (
        e.health_inequality_structural * 0.4
        + e.health_financing_gap * 0.35
        + e.health_worker_shortage * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    preparedness: float,
    response: float,
    governance: float,
    equity: float,
) -> float:
    return round(
        (preparedness * 0.30 + response * 0.25 + governance * 0.25 + equity * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _ghs_pattern(e: GlobalHealthSecurityInput) -> str:
    if e.pandemic_preparedness_gap > 0.85 and e.surveillance_system_weakness > 0.80:
        return "pandemic_preparedness_collapse"
    if e.WHO_funding_adequacy > 0.85 and e.international_coordination_failure > 0.80:
        return "international_health_governance_failure"
    if e.supply_chain_health_vulnerability > 0.85 and e.vaccine_manufacturing_capacity > 0.80:
        return "health_supply_chain_crisis"
    if e.healthcare_system_resilience > 0.80 and e.health_worker_shortage > 0.75:
        return "health_system_resilience_collapse"
    if e.climate_health_nexus > 0.80 and e.zoonotic_spillover_risk > 0.75:
        return "climate_zoonotic_health_nexus"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "effondrement_sécurité_sanitaire_mondiale"
    if composite >= 40:
        return "crise_sécurité_sanitaire_majeure"
    if composite >= 20:
        return "vulnérabilité_sanitaire_structurelle"
    return "sécurité_sanitaire_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgence_sanitaire_mondiale"
    if risk == "high":
        return "renforcement_architecture_sanitaire_urgence"
    if risk == "moderate":
        return "consolidation_systèmes_santé_structurelle"
    return "veille_sécurité_sanitaire_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Effondrement sécurité sanitaire — architecture mondiale critique"
    if risk == "high":
        return "🟠 Crise sécurité sanitaire mondiale majeure détectée"
    if risk == "moderate":
        return "🟡 Vulnérabilité sanitaire structurelle active"
    return "🟢 Sécurité sanitaire sous surveillance et contenue"


def analyze_global_health_security(e: GlobalHealthSecurityInput) -> GlobalHealthSecurityResult:
    preparedness = _preparedness_score(e)
    response = _response_score(e)
    governance = _governance_score(e)
    equity = _equity_score(e)
    composite = _composite_score(preparedness, response, governance, equity)
    risk = _risk_level(composite)
    pattern = _ghs_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return GlobalHealthSecurityResult(
        entity_id=e.entity_id,
        health_system_type=e.health_system_type,
        region=e.region,
        preparedness_score=preparedness,
        response_score=response,
        governance_score=governance,
        equity_score=equity,
        composite_score=composite,
        risk_level=risk,
        ghs_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        pandemic_preparedness_gap=e.pandemic_preparedness_gap,
        IHR_compliance_failure=e.IHR_compliance_failure,
    )


class GlobalHealthSecurityEngine:
    def analyze(self, entities: List[GlobalHealthSecurityInput]) -> Dict[str, Any]:
        results = [analyze_global_health_security(e) for e in entities]

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
            pattern_distribution[r.ghs_pattern] = pattern_distribution.get(r.ghs_pattern, 0) + 1
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
        results: List[GlobalHealthSecurityResult],
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
            "module_id": 382,
            "module_name": "Global Health Security Architecture Intelligence Engine",
            "total": len(results),
            "critical": critical_count,
            "high": high_count,
            "moderate": moderate_count,
            "low": low_count,
            "avg_composite": avg_composite,
            "risk_distribution": risk_distribution,
            "pattern_distribution": pattern_distribution,
            "severity_distribution": severity_distribution,
            "action_distribution": action_distribution,
            "avg_estimated_health_security_index": round(avg_composite / 100 * 10, 2),
        }

    def summary(self, entities: List[GlobalHealthSecurityInput]) -> Dict[str, Any]:
        return self.analyze(entities)
