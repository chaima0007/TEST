"""
Module 323 — Caelum Partners — Cognitive Warfare & Information Operations Intelligence Engine
Chaima Mhadbi, Fondatrice, Bruxelles
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class CognitiveWarfareInput:
    entity_id: str
    operation_type: str
    region: str
    # 17 float fields (0.0-1.0)
    disinformation_velocity: float = 0.0
    deepfake_deployment_rate: float = 0.0
    narrative_weaponization_index: float = 0.0
    epistemic_attack_precision: float = 0.0
    perception_management_depth: float = 0.0
    social_media_amplification_weaponization: float = 0.0
    adversarial_ai_content_generation: float = 0.0
    influence_bot_network_density: float = 0.0
    cognitive_vulnerability_exploitation: float = 0.0
    memory_hole_operation_rate: float = 0.0
    truth_decay_acceleration: float = 0.0
    institutional_trust_erosion_rate: float = 0.0
    resilience_to_cognitive_attack: float = 0.0  # inverse: high=good
    media_literacy_gap: float = 0.0
    fact_checking_bypass_sophistication: float = 0.0
    cross_domain_narrative_coherence: float = 0.0
    psychological_operation_reach: float = 0.0


def _compute_scores(inp: CognitiveWarfareInput):
    disinformation_score = (
        inp.disinformation_velocity * 0.4
        + inp.deepfake_deployment_rate * 0.35
        + inp.adversarial_ai_content_generation * 0.25
    ) * 100

    influence_score = (
        inp.influence_bot_network_density * 0.4
        + inp.social_media_amplification_weaponization * 0.35
        + inp.psychological_operation_reach * 0.25
    ) * 100

    erosion_score = (
        inp.truth_decay_acceleration * 0.4
        + inp.institutional_trust_erosion_rate * 0.35
        + inp.memory_hole_operation_rate * 0.25
    ) * 100

    vulnerability_score = (
        inp.cognitive_vulnerability_exploitation * 0.4
        + inp.media_literacy_gap * 0.35
        + (1 - inp.resilience_to_cognitive_attack) * 0.25
    ) * 100

    composite = (
        disinformation_score * 0.30
        + influence_score * 0.25
        + erosion_score * 0.25
        + vulnerability_score * 0.20
    )

    return disinformation_score, influence_score, erosion_score, vulnerability_score, composite


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    elif composite >= 40:
        return "high"
    elif composite >= 20:
        return "moderate"
    else:
        return "low"


def _detect_pattern(inp: CognitiveWarfareInput) -> str:
    if inp.deepfake_deployment_rate >= 0.70 and inp.adversarial_ai_content_generation >= 0.65:
        return "deepfake_information_war"
    if inp.truth_decay_acceleration >= 0.70 and inp.institutional_trust_erosion_rate >= 0.65:
        return "epistemic_collapse"
    if inp.influence_bot_network_density >= 0.70 and inp.social_media_amplification_weaponization >= 0.65:
        return "influence_network_dominance"
    if inp.narrative_weaponization_index >= 0.70 and inp.cross_domain_narrative_coherence >= 0.65:
        return "narrative_siege"
    if inp.cognitive_vulnerability_exploitation >= 0.70 and inp.resilience_to_cognitive_attack <= 0.40:
        return "cognitive_immune_failure"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 75:
        return "info_war_emergency"
    elif composite >= 50:
        return "high_cognitive_threat"
    elif composite >= 25:
        return "cognitive_attack_developing"
    else:
        return "cognitive_resilient"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "cognitive_emergency_response"
    if risk == "high" and pattern == "epistemic_collapse":
        return "truth_restoration_program"
    if risk == "high":
        return "counter_narrative_operations"
    if risk == "moderate":
        return "cognitive_monitoring"
    return "no_action"


def _french_signal(risk: str, pattern: str) -> str:
    signals = {
        "critical": "🔴 ALERTE CRITIQUE: Opération de guerre cognitive détectée — Réponse d'urgence requise",
        "high": "🟠 MENACE ÉLEVÉE: Campagne d'influence active — Intervention nécessaire",
        "moderate": "🟡 SURVEILLANCE: Activité cognitive suspecte — Monitoring renforcé",
        "low": "🟢 RÉSILIENCE: Environnement cognitif stable — Veille standard",
    }
    pattern_signals = {
        "deepfake_information_war": " | Guerre deepfake en cours",
        "epistemic_collapse": " | Effondrement épistémique détecté",
        "influence_network_dominance": " | Dominance des réseaux d'influence",
        "narrative_siege": " | Siège narratif identifié",
        "cognitive_immune_failure": " | Défaillance immunitaire cognitive",
        "none": "",
    }
    return signals.get(risk, "") + pattern_signals.get(pattern, "")


class CognitiveWarfareResult:
    def __init__(self, inp: CognitiveWarfareInput):
        dis, inf, ero, vul, comp = _compute_scores(inp)
        risk = _risk_level(comp)
        pattern = _detect_pattern(inp)
        severity = _severity(comp)
        action = _recommended_action(risk, pattern)
        signal = _french_signal(risk, pattern)

        self.entity_id = inp.entity_id
        self.region = inp.region
        self.operation_type = inp.operation_type
        self.warfare_risk = risk
        self.warfare_pattern = pattern
        self.warfare_severity = severity
        self.recommended_action = action
        self.disinformation_score = round(dis, 2)
        self.influence_score = round(inf, 2)
        self.erosion_score = round(ero, 2)
        self.vulnerability_score = round(vul, 2)
        self.warfare_composite = round(comp, 2)
        self.is_warfare_crisis = comp >= 60
        self.requires_warfare_intervention = comp >= 40
        self.warfare_signal = signal

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "operation_type": self.operation_type,
            "warfare_risk": self.warfare_risk,
            "warfare_pattern": self.warfare_pattern,
            "warfare_severity": self.warfare_severity,
            "recommended_action": self.recommended_action,
            "disinformation_score": self.disinformation_score,
            "influence_score": self.influence_score,
            "erosion_score": self.erosion_score,
            "vulnerability_score": self.vulnerability_score,
            "warfare_composite": self.warfare_composite,
            "is_warfare_crisis": self.is_warfare_crisis,
            "requires_warfare_intervention": self.requires_warfare_intervention,
            "warfare_signal": self.warfare_signal,
        }


class CognitiveWarfareEngine:
    def analyze(self, entities: list[CognitiveWarfareInput]) -> dict:
        results = [CognitiveWarfareResult(e) for e in entities]
        dicts = [r.to_dict() for r in results]

        composites = [r.warfare_composite for r in results]
        avg_composite = sum(composites) / len(composites) if composites else 0.0

        crises = [r for r in results if r.is_warfare_crisis]
        interventions = [r for r in results if r.requires_warfare_intervention]

        patterns = {}
        for r in results:
            patterns[r.warfare_pattern] = patterns.get(r.warfare_pattern, 0) + 1

        risks = {}
        for r in results:
            risks[r.warfare_risk] = risks.get(r.warfare_risk, 0) + 1

        return {
            "module": "Module 323 — Cognitive Warfare & Information Operations Intelligence Engine",
            "analyst": "Chaima Mhadbi, Fondatrice, Bruxelles",
            "total_entities": len(entities),
            "warfare_crises": len(crises),
            "requires_intervention": len(interventions),
            "avg_estimated_cognitive_warfare_index": round(avg_composite / 100 * 10, 2),
            "avg_warfare_composite": round(avg_composite, 2),
            "risk_distribution": risks,
            "pattern_distribution": patterns,
            "critical_entities": [r.entity_id for r in results if r.warfare_risk == "critical"],
            "crisis_entities": [r.entity_id for r in results if r.is_warfare_crisis],
            "top_threat": max(results, key=lambda r: r.warfare_composite).entity_id if results else None,
            "entities": dicts,
        }
