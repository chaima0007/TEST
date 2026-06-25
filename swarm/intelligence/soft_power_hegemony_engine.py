"""
Module 328 — Soft Power & Cultural Hegemony Intelligence Engine
Caelum Partners Swarm Intelligence — Propriété exclusive de Chaima Mhadbi
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class SoftPowerHegemonyInput:
    entity_id: str
    power_domain: str
    region: str
    cultural_export_dominance: float
    language_hegemony_index: float
    media_narrative_control: float
    educational_model_projection: float
    diaspora_influence_leverage: float
    brand_ideology_penetration: float
    entertainment_culture_capture: float
    algorithmic_culture_shaping: float
    religious_soft_power: float
    normative_framework_dominance: float
    sports_diplomacy_reach: float
    tech_standard_setting_power: float
    cultural_autonomy_erosion: float
    linguistic_diversity_threat: float
    value_system_colonization: float
    counter_hegemony_capacity: float
    soft_power_weaponization_index: float


@dataclass
class SoftPowerHegemonyResult:
    entity_id: str
    region: str
    power_domain: str
    hegemony_risk: str
    hegemony_pattern: str
    hegemony_severity: str
    recommended_action: str
    cultural_score: float
    information_score: float
    normative_score: float
    power_score: float
    hegemony_composite: float
    is_hegemony_crisis: bool
    requires_hegemony_intervention: bool
    hegemony_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "power_domain": self.power_domain,
            "hegemony_risk": self.hegemony_risk,
            "hegemony_pattern": self.hegemony_pattern,
            "hegemony_severity": self.hegemony_severity,
            "recommended_action": self.recommended_action,
            "cultural_score": self.cultural_score,
            "information_score": self.information_score,
            "normative_score": self.normative_score,
            "power_score": self.power_score,
            "hegemony_composite": self.hegemony_composite,
            "is_hegemony_crisis": self.is_hegemony_crisis,
            "requires_hegemony_intervention": self.requires_hegemony_intervention,
            "hegemony_signal": self.hegemony_signal,
        }


def _cultural_score(e: SoftPowerHegemonyInput) -> float:
    raw = (
        e.cultural_export_dominance * 0.4
        + e.entertainment_culture_capture * 0.35
        + e.brand_ideology_penetration * 0.25
    ) * 100
    return round(raw * 100) / 100


def _information_score(e: SoftPowerHegemonyInput) -> float:
    raw = (
        e.media_narrative_control * 0.4
        + e.algorithmic_culture_shaping * 0.35
        + e.language_hegemony_index * 0.25
    ) * 100
    return round(raw * 100) / 100


def _normative_score(e: SoftPowerHegemonyInput) -> float:
    raw = (
        e.normative_framework_dominance * 0.4
        + e.educational_model_projection * 0.35
        + e.value_system_colonization * 0.25
    ) * 100
    return round(raw * 100) / 100


def _power_score(e: SoftPowerHegemonyInput) -> float:
    raw = (
        e.tech_standard_setting_power * 0.4
        + e.diaspora_influence_leverage * 0.35
        + e.soft_power_weaponization_index * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(cultural: float, information: float, normative: float, power: float) -> float:
    return round((cultural * 0.30 + information * 0.25 + normative * 0.25 + power * 0.20) * 100) / 100


def _hegemony_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _hegemony_pattern(e: SoftPowerHegemonyInput) -> str:
    if e.cultural_export_dominance >= 0.70 and e.entertainment_culture_capture >= 0.65:
        return "cultural_monopoly"
    if e.media_narrative_control >= 0.70 and e.algorithmic_culture_shaping >= 0.65:
        return "narrative_hegemony"
    if e.normative_framework_dominance >= 0.70 and e.value_system_colonization >= 0.65:
        return "normative_colonization"
    if e.language_hegemony_index >= 0.70 and e.linguistic_diversity_threat >= 0.65:
        return "linguistic_homogenization"
    if e.soft_power_weaponization_index >= 0.70 and e.cultural_autonomy_erosion >= 0.65:
        return "soft_power_weaponization"
    return "none"


def _hegemony_severity(composite: float) -> str:
    if composite >= 75:
        return "hegemony_emergency"
    if composite >= 50:
        return "high_hegemony_risk"
    if composite >= 25:
        return "hegemony_developing"
    return "cultural_sovereignty_maintained"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "cultural_sovereignty_emergency"
    if risk == "high" and pattern == "narrative_hegemony":
        return "counter_narrative_program"
    if risk == "high":
        return "cultural_resilience_framework"
    if risk == "moderate":
        return "cultural_monitoring"
    return "no_action"


def _hegemony_signal(e: SoftPowerHegemonyInput, risk: str, composite: float) -> str:
    comp_int = int(composite)
    if risk == "critical":
        return (
            f"Critique — domination exportations culturelles {int(e.cultural_export_dominance * 100)}% "
            f"— contrôle narratif médias {int(e.media_narrative_control * 100)}% "
            f"— composite {comp_int}"
        )
    if risk == "high":
        return (
            f"Élevé — hégémonie linguistique {int(e.language_hegemony_index * 100)}% "
            f"— cadrage normatif {int(e.normative_framework_dominance * 100)}% "
            f"— composite {comp_int}"
        )
    if risk == "moderate":
        return (
            f"Modéré — capture culture divertissement {int(e.entertainment_culture_capture * 100)}% "
            f"— composite {comp_int}"
        )
    return "Souveraineté culturelle préservée — pluralisme linguistique intact, autonomie normative maintenue"


def analyze_entity(e: SoftPowerHegemonyInput) -> SoftPowerHegemonyResult:
    cultural = _cultural_score(e)
    information = _information_score(e)
    normative = _normative_score(e)
    power = _power_score(e)
    comp = _composite(cultural, information, normative, power)
    risk = _hegemony_risk(comp)
    pattern = _hegemony_pattern(e)
    severity = _hegemony_severity(comp)
    action = _recommended_action(risk, pattern)
    signal = _hegemony_signal(e, risk, comp)

    return SoftPowerHegemonyResult(
        entity_id=e.entity_id,
        region=e.region,
        power_domain=e.power_domain,
        hegemony_risk=risk,
        hegemony_pattern=pattern,
        hegemony_severity=severity,
        recommended_action=action,
        cultural_score=cultural,
        information_score=information,
        normative_score=normative,
        power_score=power,
        hegemony_composite=comp,
        is_hegemony_crisis=comp >= 60,
        requires_hegemony_intervention=comp >= 40,
        hegemony_signal=signal,
    )


class SoftPowerHegemonyEngine:
    def analyze(self, entities: List[SoftPowerHegemonyInput]) -> Dict[str, Any]:
        results = [analyze_entity(e) for e in entities]
        entity_dicts = [r.to_dict() for r in results]

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}

        total_composite = 0.0
        total_cultural = 0.0
        total_information = 0.0
        total_normative = 0.0
        total_power = 0.0
        crisis_count = 0
        intervention_count = 0

        for r in results:
            risk_counts[r.hegemony_risk] = risk_counts.get(r.hegemony_risk, 0) + 1
            pattern_counts[r.hegemony_pattern] = pattern_counts.get(r.hegemony_pattern, 0) + 1
            severity_counts[r.hegemony_severity] = severity_counts.get(r.hegemony_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1
            total_composite += r.hegemony_composite
            total_cultural += r.cultural_score
            total_information += r.information_score
            total_normative += r.normative_score
            total_power += r.power_score
            if r.is_hegemony_crisis:
                crisis_count += 1
            if r.requires_hegemony_intervention:
                intervention_count += 1

        n = len(results)
        avg_composite = round(total_composite / n * 10) / 10 if n else 0.0

        summary = {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_hegemony_composite": avg_composite,
            "hegemony_crisis_count": crisis_count,
            "hegemony_intervention_count": intervention_count,
            "avg_cultural_score": round(total_cultural / n * 10) / 10 if n else 0.0,
            "avg_information_score": round(total_information / n * 10) / 10 if n else 0.0,
            "avg_normative_score": round(total_normative / n * 10) / 10 if n else 0.0,
            "avg_power_score": round(total_power / n * 10) / 10 if n else 0.0,
            "avg_estimated_hegemony_index": round(avg_composite / 100 * 10, 2),
        }

        return {"entities": entity_dicts, "summary": summary}
