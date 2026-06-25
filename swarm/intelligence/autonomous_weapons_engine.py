from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class AutonomousWeaponsInput:
    entity_id: str
    system_type: str
    region: str
    human_control_removal: float
    legal_accountability_gap: float
    civilian_discrimination_failure: float
    proportionality_compliance: float
    targeting_algorithm_bias: float
    proliferation_risk: float
    treaty_compliance: float
    export_control_effectiveness: float
    arms_race_intensity: float
    ngo_oversight_access: float
    incident_transparency: float
    review_mechanism_quality: float
    international_law_compliance: float
    dual_use_risk: float
    small_state_deployment: float
    non_state_actor_access: float
    autonomous_escalation_risk: float


@dataclass
class AutonomousWeaponsResult:
    entity_id: str
    system_type: str
    region: str
    accountability_score: float
    legal_score: float
    proliferation_score: float
    bias_score: float
    composite_score: float
    risk_level: str
    weapons_pattern: str
    severity: str
    recommended_action: str
    signal: str
    human_control_removal: float
    proliferation_risk: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "system_type": self.system_type,
            "region": self.region,
            "accountability_score": self.accountability_score,
            "legal_score": self.legal_score,
            "proliferation_score": self.proliferation_score,
            "bias_score": self.bias_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "weapons_pattern": self.weapons_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "human_control_removal": self.human_control_removal,
            "proliferation_risk": self.proliferation_risk,
        }


def _accountability_score(e: AutonomousWeaponsInput) -> float:
    raw = (
        e.human_control_removal * 0.5
        + e.legal_accountability_gap * 0.5
    ) * 100
    return round(raw * 100) / 100


def _legal_score(e: AutonomousWeaponsInput) -> float:
    raw = (
        e.civilian_discrimination_failure * 0.35
        + (1 - e.proportionality_compliance) * 0.25
        + (1 - e.international_law_compliance) * 0.25
        + (1 - e.treaty_compliance) * 0.15
    ) * 100
    return round(raw * 100) / 100


def _proliferation_score(e: AutonomousWeaponsInput) -> float:
    raw = (
        e.proliferation_risk * 0.25
        + e.arms_race_intensity * 0.20
        + e.dual_use_risk * 0.20
        + e.small_state_deployment * 0.15
        + e.non_state_actor_access * 0.15
        + (1 - e.export_control_effectiveness) * 0.05
    ) * 100
    return round(raw * 100) / 100


def _bias_score(e: AutonomousWeaponsInput) -> float:
    raw = (
        e.targeting_algorithm_bias * 0.40
        + e.autonomous_escalation_risk * 0.30
        + (1 - e.ngo_oversight_access) * 0.15
        + (1 - e.incident_transparency) * 0.10
        + (1 - e.review_mechanism_quality) * 0.05
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    accountability: float,
    legal: float,
    proliferation: float,
    bias: float,
) -> float:
    return round(
        (accountability * 0.30 + legal * 0.25 + proliferation * 0.25 + bias * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _weapons_pattern(e: AutonomousWeaponsInput) -> str:
    if e.human_control_removal > 0.85 and e.legal_accountability_gap > 0.80:
        return "accountability_vacuum_crisis"
    if e.civilian_discrimination_failure > 0.85 and (1 - e.proportionality_compliance) > 0.80:
        return "civilian_harm_discrimination_failure"
    if e.proliferation_risk > 0.85 and e.non_state_actor_access > 0.80:
        return "arms_race_proliferation"
    if (1 - e.treaty_compliance) > 0.80 and (1 - e.international_law_compliance) > 0.75:
        return "treaty_governance_collapse"
    if e.targeting_algorithm_bias > 0.80 and e.autonomous_escalation_risk > 0.75:
        return "algorithmic_bias_targeting"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_gouvernance_létale_systémique"
    if composite >= 40:
        return "crise_prolifération_armes_autonomes_majeure"
    if composite >= 20:
        return "risque_biais_algorithmique_structurel"
    return "surveillance_gouvernance_armes_ia"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_contrôle_armes_létales_ia"
    if risk == "high":
        return "renforcement_traités_non_prolifération_systèmes_autonomes"
    if risk == "moderate":
        return "révision_mécanismes_supervision_humaine_ia"
    return "veille_gouvernance_armes_autonomes_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise gouvernance létale systémique — contrôle humain en péril"
    if risk == "high":
        return "🟠 Crise prolifération armes autonomes majeure détectée"
    if risk == "moderate":
        return "🟡 Risque biais algorithmique structurel actif"
    return "🟢 Surveillance gouvernance armes IA continue"


def analyze_autonomous_weapons(e: AutonomousWeaponsInput) -> AutonomousWeaponsResult:
    accountability = _accountability_score(e)
    legal = _legal_score(e)
    proliferation = _proliferation_score(e)
    bias = _bias_score(e)
    composite = _composite_score(accountability, legal, proliferation, bias)
    risk = _risk_level(composite)
    pattern = _weapons_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return AutonomousWeaponsResult(
        entity_id=e.entity_id,
        system_type=e.system_type,
        region=e.region,
        accountability_score=accountability,
        legal_score=legal,
        proliferation_score=proliferation,
        bias_score=bias,
        composite_score=composite,
        risk_level=risk,
        weapons_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        human_control_removal=e.human_control_removal,
        proliferation_risk=e.proliferation_risk,
    )


class AutonomousWeaponsEngine:
    def analyze(self, entities: List[AutonomousWeaponsInput]) -> Dict[str, Any]:
        results = [analyze_autonomous_weapons(e) for e in entities]

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
            pattern_distribution[r.weapons_pattern] = pattern_distribution.get(r.weapons_pattern, 0) + 1
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
        results: List[AutonomousWeaponsResult] = None,
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
            "module_id": 406,
            "module_name": "Autonomous Weapons & Lethal AI Governance Intelligence Engine",
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
            "avg_estimated_lethal_ai_governance_index": round(avg_composite / 100 * 10, 2),
        }
