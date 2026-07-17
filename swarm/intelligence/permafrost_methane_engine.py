from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class PermafrostMethaneInput:
    entity_id: str
    ecosystem_type: str
    region: str
    permafrost_degradation_rate: float
    active_layer_deepening: float
    methane_flux_intensity: float
    thermokarst_expansion: float
    subsea_methane_seepage: float
    carbon_stock_released: float
    tipping_point_proximity: float
    feedback_loop_acceleration: float
    albedo_reduction: float
    sea_level_contribution: float
    infrastructure_damage_rate: float
    indigenous_displacement: float
    monitoring_gap: float
    international_coordination_failure: float
    adaptation_capacity: float
    economic_loss_rate: float
    ecosystem_biodiversity_loss: float


@dataclass
class PermafrostMethaneResult:
    entity_id: str
    ecosystem_type: str
    region: str
    thaw_score: float
    methane_score: float
    feedback_score: float
    governance_score: float
    composite_score: float
    risk_level: str
    permafrost_pattern: str
    severity: str
    recommended_action: str
    signal: str
    permafrost_degradation_rate: float
    methane_flux_intensity: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "ecosystem_type": self.ecosystem_type,
            "region": self.region,
            "thaw_score": self.thaw_score,
            "methane_score": self.methane_score,
            "feedback_score": self.feedback_score,
            "governance_score": self.governance_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "permafrost_pattern": self.permafrost_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "permafrost_degradation_rate": self.permafrost_degradation_rate,
            "methane_flux_intensity": self.methane_flux_intensity,
        }


def _thaw_score(e: PermafrostMethaneInput) -> float:
    raw = (
        e.permafrost_degradation_rate * 0.4
        + e.active_layer_deepening * 0.35
        + e.thermokarst_expansion * 0.25
    ) * 100
    return round(raw * 100) / 100


def _methane_score(e: PermafrostMethaneInput) -> float:
    raw = (
        e.methane_flux_intensity * 0.4
        + e.subsea_methane_seepage * 0.35
        + e.carbon_stock_released * 0.25
    ) * 100
    return round(raw * 100) / 100


def _feedback_score(e: PermafrostMethaneInput) -> float:
    raw = (
        e.tipping_point_proximity * 0.4
        + e.feedback_loop_acceleration * 0.35
        + e.albedo_reduction * 0.25
    ) * 100
    return round(raw * 100) / 100


def _governance_score(e: PermafrostMethaneInput) -> float:
    raw = (
        e.international_coordination_failure * 0.4
        + e.monitoring_gap * 0.35
        + e.indigenous_displacement * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    thaw: float,
    methane: float,
    feedback: float,
    governance: float,
) -> float:
    return round(
        (thaw * 0.30 + methane * 0.25 + feedback * 0.25 + governance * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _permafrost_pattern(e: PermafrostMethaneInput) -> str:
    if e.permafrost_degradation_rate > 0.85 and e.thermokarst_expansion > 0.80:
        return "abrupt_thaw_collapse"
    if e.subsea_methane_seepage > 0.85 and e.methane_flux_intensity > 0.80:
        return "subsea_methane_eruption"
    if e.tipping_point_proximity > 0.85 and e.feedback_loop_acceleration > 0.80:
        return "tipping_point_cascade"
    if e.infrastructure_damage_rate > 0.80 and e.economic_loss_rate > 0.75:
        return "infrastructure_sinkhole_crisis"
    if e.indigenous_displacement > 0.80 and e.ecosystem_biodiversity_loss > 0.75:
        return "indigenous_territory_loss"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_pergélisol_méthane_systémique"
    if composite >= 40:
        return "crise_climatique_arctique_majeure"
    if composite >= 20:
        return "dégradation_pergélisol_structurelle"
    return "pergélisol_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_pergélisol_méthane_critique"
    if risk == "high":
        return "surveillance_renforcée_émissions_arctiques"
    if risk == "moderate":
        return "renforcement_monitoring_pergélisol_régional"
    return "veille_pergélisol_méthane_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise pergélisol & méthane systémique — basculement climatique imminent"
    if risk == "high":
        return "🟠 Crise climatique arctique majeure détectée"
    if risk == "moderate":
        return "🟡 Dégradation pergélisol structurelle active"
    return "🟢 Pergélisol sous surveillance"


def analyze_permafrost_methane(e: PermafrostMethaneInput) -> PermafrostMethaneResult:
    thaw = _thaw_score(e)
    methane = _methane_score(e)
    feedback = _feedback_score(e)
    governance = _governance_score(e)
    composite = _composite_score(thaw, methane, feedback, governance)
    risk = _risk_level(composite)
    pattern = _permafrost_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return PermafrostMethaneResult(
        entity_id=e.entity_id,
        ecosystem_type=e.ecosystem_type,
        region=e.region,
        thaw_score=thaw,
        methane_score=methane,
        feedback_score=feedback,
        governance_score=governance,
        composite_score=composite,
        risk_level=risk,
        permafrost_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        permafrost_degradation_rate=e.permafrost_degradation_rate,
        methane_flux_intensity=e.methane_flux_intensity,
    )


class PermafrostMethaneEngine:
    def analyze(self, entities: List[PermafrostMethaneInput]) -> Dict[str, Any]:
        results = [analyze_permafrost_methane(e) for e in entities]

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
            pattern_distribution[r.permafrost_pattern] = pattern_distribution.get(r.permafrost_pattern, 0) + 1
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
        results: List[PermafrostMethaneResult] = None,
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
            "module_id": 433,
            "module_name": "Pergélisol & Méthane Arctique Intelligence Engine",
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
            "avg_estimated_permafrost_risk_index": round(avg_composite / 100 * 10, 2),
        }
