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


# ── Canonical summary (13-key format for Caelum swarm orchestrator) ───────────

_RISK_MAP = {"critical": "critique", "high": "élevé", "moderate": "modéré", "low": "faible"}
_PATTERN_LABELS = {
    "saturation_epistemique": {"severity_fr": "Critique", "action_fr": "Activation protocole souveraineté informationnelle — contre-narratifs sous 48h", "signal_fr": "Effondrement épistémique imminent — saturation informationnelle détectée"},
    "manipulation_strategique": {"severity_fr": "Critique", "action_fr": "Déploiement unités de fact-checking d'urgence et alerte plateformes numériques", "signal_fr": "Campagnes coordonnées acteurs étatiques — manipulation institutionnelle"},
    "erosion_confiance": {"severity_fr": "Élevé", "action_fr": "Renforcement médias publics et éducation aux médias ciblée", "signal_fr": "Érosion progressive confiance institutionnelle — vulnérabilité démocratique"},
    "pollution_informationnelle": {"severity_fr": "Modéré", "action_fr": "Surveillance écosystèmes informationnels et signalement contenus manipulatoires", "signal_fr": "Pollution espace informationnel gérable — vigilance épistémique"},
    "resilience_cognitive": {"severity_fr": "Faible", "action_fr": "Maintien programmes littératie numérique et veille informationnelle continue", "signal_fr": "composite_score < 30 — résilience cognitive confirmée"},
}

_MOCK = [
    ("CW-001", "Russie & Espace Post-Soviétique", "Eurasie", "Opérations Informationnelles", 92.0, 85.0, 88.0, 80.0),
    ("CW-002", "Chine & Sphère d'Influence", "Asie-Pacifique", "Influence Stratégique", 88.0, 78.0, 82.0, 75.0),
    ("CW-003", "Moyen-Orient & Golfe", "MENA", "Propagande Régionale", 80.0, 72.0, 76.0, 68.0),
    ("CW-004", "Amérique Latine", "Amériques", "Polarisation Politique", 65.0, 60.0, 62.0, 55.0),
    ("CW-005", "Afrique Sub-Saharienne", "Afrique", "Manipulation Électorale", 70.0, 75.0, 65.0, 60.0),
    ("CW-006", "Europe Occidentale", "Europe", "Désinformation Hybride", 48.0, 42.0, 45.0, 38.0),
    ("CW-007", "Amérique du Nord", "Amériques", "Polarisation Démocratique", 52.0, 38.0, 50.0, 45.0),
    ("CW-008", "Scandinavie & Pays Baltes", "Europe du Nord", "Résilience Cognitive", 15.0, 12.0, 18.0, 10.0),
]

def _make_entity(row: tuple) -> dict:
    eid, name, country, sector, s1, s2, s3, s4 = row
    comp = round(s1*0.30 + s2*0.25 + s3*0.25 + s4*0.20, 2)
    if comp >= 60: rl = "critique"
    elif comp >= 40: rl = "élevé"
    elif comp >= 20: rl = "modéré"
    else: rl = "faible"
    if s1 >= 85 and s2 >= 80: pat = "saturation_epistemique"
    elif s3 >= 75 and s4 >= 70: pat = "manipulation_strategique"
    elif comp >= 45: pat = "erosion_confiance"
    elif comp >= 25: pat = "pollution_informationnelle"
    else: pat = "resilience_cognitive"
    if rl == "critique":
        signals = [f"Guerre cognitive critique pour {name} — saturation épistémique en cours", "Vélocité désinformation au-delà des seuils de résilience démocratique", "Capture narrative institutionnelle — processus décisionnels compromis"]
    elif rl == "élevé":
        signals = [f"Manipulation informationnelle élevée pour {name} — confiance institutionnelle érodée", "Campagnes coordonnées identifiées dans l'espace numérique", "Vulnérabilité cognitive population en hausse significative"]
    elif rl == "modéré":
        signals = [f"Pollution informationnelle modérée pour {name} — vigilance épistémique requise", "Signaux de manipulation détectés dans les réseaux sociaux", "Résilience cognitive maintenue mais sous pression croissante"]
    else:
        signals = [f"{name} maintient une souveraineté épistémique robuste", "Écosystème informationnel sain — faible vulnérabilité aux manipulations", "Littératie numérique élevée — bouclier cognitif effectif"]
    return {"entity_id": eid, "name": name, "country": country, "sector": sector, "composite_score": comp, "disinfo_velocity_score": s1, "epistemic_resilience_gap_score": s2, "narrative_capture_score": s3, "cognitive_vulnerability_score": s4, "risk_level": rl, "primary_pattern": pat, "key_signals": signals, "estimated_cogwar_index": round(comp/100*10, 2), "last_updated": "2026-06-20"}

def summary() -> dict:
    """Canonical 13-key summary for the Caelum swarm orchestrator."""
    entities = [_make_entity(r) for r in _MOCK]
    n = len(entities)
    avg = round(sum(e["composite_score"] for e in entities) / n, 2)
    risk_dist: dict = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    pattern_dist: dict = {k: 0 for k in _PATTERN_LABELS}
    critical_alerts, top_risk = [], []
    for e in entities:
        risk_dist[e["risk_level"]] = risk_dist.get(e["risk_level"], 0) + 1
        pattern_dist[e["primary_pattern"]] = pattern_dist.get(e["primary_pattern"], 0) + 1
        if e["risk_level"] == "critique":
            critical_alerts.append(f"{e['name']}: {e['primary_pattern'].replace('_', ' ')}")
            top_risk.append(e["name"])
    return {"total_entities": n, "avg_composite": avg, "risk_distribution": risk_dist, "pattern_distribution": pattern_dist, "top_risk_entities": top_risk, "critical_alerts": critical_alerts, "last_analysis": "2026-06-20", "engine_version": "1.0.0", "domain": "cognitivewarfare", "confidence_score": 0.82, "data_sources": ["disinfo_tracker", "epistemic_security_index", "narrative_analysis_lab"], "entities": entities, "avg_estimated_cogwar_index": round(avg/100*10, 2)}

def analyze_cognitive_warfare() -> dict:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()
