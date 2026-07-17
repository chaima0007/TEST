from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class AutonomousVehicleInput:
    entity_id: str
    vehicle_type: str
    region: str
    safety_score_raw: float
    accident_rate: float
    regulatory_compliance: float
    liability_clarity: float
    insurance_coverage: float
    ethical_alignment: float
    data_privacy: float
    cybersecurity_resilience: float
    public_trust: float
    legislative_readiness: float
    bias_detection: float
    emergency_response: float
    manufacturer_accountability: float
    algorithmic_transparency: float
    mixed_traffic_safety: float
    pedestrian_protection: float
    weather_performance: float


@dataclass
class AutonomousVehicleResult:
    entity_id: str
    vehicle_type: str
    region: str
    safety_score: float
    liability_score: float
    regulatory_score: float
    ethics_score: float
    composite_score: float
    risk_level: str
    av_pattern: str
    severity: str
    recommended_action: str
    signal: str
    accident_rate: float
    liability_clarity: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "vehicle_type": self.vehicle_type,
            "region": self.region,
            "safety_score": self.safety_score,
            "liability_score": self.liability_score,
            "regulatory_score": self.regulatory_score,
            "ethics_score": self.ethics_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "av_pattern": self.av_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "accident_rate": self.accident_rate,
            "liability_clarity": self.liability_clarity,
        }


def _safety_score(e: AutonomousVehicleInput) -> float:
    raw = (
        e.accident_rate * 0.40
        + e.mixed_traffic_safety * 0.35
        + e.pedestrian_protection * 0.25
    ) * 100
    return round(raw * 100) / 100


def _liability_score(e: AutonomousVehicleInput) -> float:
    raw = (
        e.liability_clarity * 0.40
        + e.manufacturer_accountability * 0.35
        + e.insurance_coverage * 0.25
    ) * 100
    return round(raw * 100) / 100


def _regulatory_score(e: AutonomousVehicleInput) -> float:
    raw = (
        e.regulatory_compliance * 0.40
        + e.legislative_readiness * 0.35
        + e.safety_score_raw * 0.25
    ) * 100
    return round(raw * 100) / 100


def _ethics_score(e: AutonomousVehicleInput) -> float:
    raw = (
        e.ethical_alignment * 0.40
        + e.algorithmic_transparency * 0.35
        + e.bias_detection * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    safety: float,
    liability: float,
    regulatory: float,
    ethics: float,
) -> float:
    return round(
        (safety * 0.30 + liability * 0.25 + regulatory * 0.25 + ethics * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _av_pattern(e: AutonomousVehicleInput) -> str:
    if e.accident_rate > 0.85 and e.liability_clarity > 0.80:
        return "fatal_accident_liability_gap"
    if e.regulatory_compliance > 0.85 and e.legislative_readiness > 0.80:
        return "regulatory_arbitrage_race"
    if e.bias_detection > 0.85 and e.ethical_alignment > 0.80:
        return "algorithmic_bias_discrimination"
    if e.insurance_coverage > 0.80 and e.manufacturer_accountability > 0.75:
        return "insurance_market_collapse"
    if e.data_privacy > 0.80 and e.cybersecurity_resilience > 0.75:
        return "data_sovereignty_failure"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_responsabilité_véhicules_autonomes_systémique"
    if composite >= 40:
        return "risque_juridique_majeur_véhicule_autonome"
    if composite >= 20:
        return "vulnérabilité_réglementaire_structurelle"
    return "surveillance_sécurité_véhicules_autonomes"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_responsabilité_juridique_critique"
    if risk == "high":
        return "révision_cadre_légal_véhicules_autonomes_accélérée"
    if risk == "moderate":
        return "renforcement_protocoles_sécurité_réglementaires"
    return "veille_conformité_véhicules_autonomes_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise responsabilité juridique véhicules autonomes — intervention systémique requise"
    if risk == "high":
        return "🟠 Risque juridique majeur détecté — révision légale urgente"
    if risk == "moderate":
        return "🟡 Vulnérabilité réglementaire structurelle active"
    return "🟢 Sécurité véhicules autonomes sous surveillance"


def analyze_autonomous_vehicle(e: AutonomousVehicleInput) -> AutonomousVehicleResult:
    safety = _safety_score(e)
    liability = _liability_score(e)
    regulatory = _regulatory_score(e)
    ethics = _ethics_score(e)
    composite = _composite_score(safety, liability, regulatory, ethics)
    risk = _risk_level(composite)
    pattern = _av_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return AutonomousVehicleResult(
        entity_id=e.entity_id,
        vehicle_type=e.vehicle_type,
        region=e.region,
        safety_score=safety,
        liability_score=liability,
        regulatory_score=regulatory,
        ethics_score=ethics,
        composite_score=composite,
        risk_level=risk,
        av_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        accident_rate=e.accident_rate,
        liability_clarity=e.liability_clarity,
    )


class AutonomousVehicleEngine:
    def analyze(self, entities: List[AutonomousVehicleInput]) -> Dict[str, Any]:
        results = [analyze_autonomous_vehicle(e) for e in entities]

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
            pattern_distribution[r.av_pattern] = pattern_distribution.get(r.av_pattern, 0) + 1
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
        results: List[AutonomousVehicleResult] = None,
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
            "module_id": 394,
            "module_name": "Véhicules Autonomes & Responsabilité Juridique Intelligence Engine",
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
            "avg_estimated_av_safety_index": round(avg_composite / 100 * 10, 2),
        }
