from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class ChildOnlineSafetyInput:
    entity_id: str
    platform_type: str
    region: str
    predator_network_density: float
    grooming_incident_rate: float
    csam_detection_gap: float
    algorithmic_harm_amplification: float
    screen_addiction_severity: float
    cyberbullying_prevalence: float
    sextortion_risk_index: float
    age_verification_failure: float
    parental_control_gap: float
    dark_web_exposure: float
    mental_health_impact: float
    reporting_mechanism_gap: float
    law_enforcement_capacity: float
    cross_border_jurisdiction_gap: float
    digital_literacy_children: float
    platform_transparency_failure: float
    regulatory_enforcement_gap: float


@dataclass
class ChildOnlineSafetyResult:
    entity_id: str
    platform_type: str
    region: str
    predation_score: float
    content_score: float
    platform_score: float
    governance_score: float
    composite_score: float
    risk_level: str
    safety_pattern: str
    severity: str
    recommended_action: str
    signal: str
    predator_network_density: float
    csam_detection_gap: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "platform_type": self.platform_type,
            "region": self.region,
            "predation_score": self.predation_score,
            "content_score": self.content_score,
            "platform_score": self.platform_score,
            "governance_score": self.governance_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "safety_pattern": self.safety_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "predator_network_density": self.predator_network_density,
            "csam_detection_gap": self.csam_detection_gap,
        }


def _predation_score(e: ChildOnlineSafetyInput) -> float:
    raw = (
        e.predator_network_density * 0.4
        + e.grooming_incident_rate * 0.35
        + e.sextortion_risk_index * 0.25
    ) * 100
    return round(raw * 100) / 100


def _content_score(e: ChildOnlineSafetyInput) -> float:
    raw = (
        e.csam_detection_gap * 0.4
        + e.dark_web_exposure * 0.35
        + e.algorithmic_harm_amplification * 0.25
    ) * 100
    return round(raw * 100) / 100


def _platform_score(e: ChildOnlineSafetyInput) -> float:
    raw = (
        e.age_verification_failure * 0.4
        + e.platform_transparency_failure * 0.35
        + e.parental_control_gap * 0.25
    ) * 100
    return round(raw * 100) / 100


def _governance_score(e: ChildOnlineSafetyInput) -> float:
    raw = (
        e.regulatory_enforcement_gap * 0.4
        + e.cross_border_jurisdiction_gap * 0.35
        + e.law_enforcement_capacity * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    predation: float,
    content: float,
    platform: float,
    governance: float,
) -> float:
    return round(
        (predation * 0.30 + content * 0.25 + platform * 0.25 + governance * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _safety_pattern(e: ChildOnlineSafetyInput) -> str:
    if e.predator_network_density > 0.85 and e.grooming_incident_rate > 0.80:
        return "grooming_network_proliferation"
    if e.csam_detection_gap > 0.85 and e.dark_web_exposure > 0.80:
        return "csam_distribution_infrastructure"
    if e.algorithmic_harm_amplification > 0.85 and e.screen_addiction_severity > 0.80:
        return "algorithmic_radicalization_youth"
    if e.sextortion_risk_index > 0.80 and e.cyberbullying_prevalence > 0.75:
        return "sextortion_epidemic"
    if e.platform_transparency_failure > 0.80 and e.reporting_mechanism_gap > 0.75:
        return "platform_moderation_failure"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_protection_enfants_systémique"
    if composite >= 40:
        return "crise_sécurité_numérique_majeure"
    if composite >= 20:
        return "vulnérabilité_numérique_structurelle"
    return "surveillance_sécurité_enfants_active"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_protection_enfants_critique"
    if risk == "high":
        return "renforcement_immédiat_modération_plateforme"
    if risk == "moderate":
        return "amélioration_mécanismes_signalement_enfants"
    return "veille_sécurité_numérique_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise protection enfants systémique — intervention d'urgence requise"
    if risk == "high":
        return "🟠 Crise sécurité numérique majeure détectée"
    if risk == "moderate":
        return "🟡 Vulnérabilité numérique structurelle active"
    return "🟢 Sécurité enfants numérique sous surveillance"


def analyze_child_online_safety(e: ChildOnlineSafetyInput) -> ChildOnlineSafetyResult:
    predation = _predation_score(e)
    content = _content_score(e)
    platform = _platform_score(e)
    governance = _governance_score(e)
    composite = _composite_score(predation, content, platform, governance)
    risk = _risk_level(composite)
    pattern = _safety_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return ChildOnlineSafetyResult(
        entity_id=e.entity_id,
        platform_type=e.platform_type,
        region=e.region,
        predation_score=predation,
        content_score=content,
        platform_score=platform,
        governance_score=governance,
        composite_score=composite,
        risk_level=risk,
        safety_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        predator_network_density=e.predator_network_density,
        csam_detection_gap=e.csam_detection_gap,
    )


class ChildOnlineSafetyEngine:
    def analyze(self, entities: List[ChildOnlineSafetyInput]) -> Dict[str, Any]:
        results = [analyze_child_online_safety(e) for e in entities]

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
            pattern_distribution[r.safety_pattern] = pattern_distribution.get(r.safety_pattern, 0) + 1
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
        results: List[ChildOnlineSafetyResult] = None,
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
            "module_id": 436,
            "module_name": "Sécurité Enfants Numérique & Préjudices en Ligne Intelligence Engine",
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
            "avg_estimated_child_digital_safety_index": round(avg_composite / 100 * 10, 2),
        }
