"""
Caelum Partners — AI Alignment Risk Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Le risque d'alignement de l'IA comme menace géopolitique existentielle :
la course aux armements IA entre grandes puissances crée des incitations
à sacrifier la sécurité pour la vitesse, déployant des systèmes de plus en
plus puissants sans garantie d'alignement avec les valeurs humaines.

Ce n'est plus de la science-fiction — c'est le calcul stratégique actuel
de chaque laboratoire d'IA et de chaque gouvernement qui finance la course.
La géopolitique de l'alignement IA est la question sécuritaire du siècle.

Risk levels (risque d'alignement IA géopolitique) :
  critique  → composite ≥ 60  (course catastrophique)
  élevé     → composite ≥ 40  (désalignement systémique)
  modéré    → composite ≥ 20  (vigilance requise)
  faible    → composite < 20  (précaution exemplaire)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "course_catastrophique": {
        "severity_fr": "Critique",
        "action_fr": "Traité international sur la sécurité IA d'urgence — moratoire sur les déploiements non-alignés",
        "signal_fr": "arms_race > 80 AND governance_lag > 75 — course à l'IA catastrophique en cours",
    },
    "desalignement_systemique": {
        "severity_fr": "Critique",
        "action_fr": "Investissement massif en recherche sur l'alignement et standards de sécurité contraignants",
        "signal_fr": "Désalignement systémique — puissance IA croissant plus vite que la capacité de contrôle",
    },
    "risque_emergeant": {
        "severity_fr": "Élevé",
        "action_fr": "Renforcement des protocoles de sécurité IA et coopération internationale sur l'alignement",
        "signal_fr": "Risque d'alignement émergent — pression compétitive compromettant la sécurité IA",
    },
    "vigilance_requise": {
        "severity_fr": "Modéré",
        "action_fr": "Développement des capacités d'évaluation de sécurité IA et dialogue multilatéral",
        "signal_fr": "Vigilance requise — dynamiques de course partielles mais cadres de sécurité existants",
    },
    "precaution_exemplaire": {
        "severity_fr": "Faible",
        "action_fr": "Maintien des standards de sécurité IA et leadership mondial sur les normes d'alignement",
        "signal_fr": "composite_score < 20 — précaution exemplaire, alignement IA priorité confirmée",
    },
}


@dataclass
class AIAlignmentRiskEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    arms_race_acceleration_score: float
    alignment_research_deficit_score: float
    governance_lag_score: float
    catastrophic_deployment_risk_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_alignment_risk_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.arms_race_acceleration_score * 0.30
            + self.alignment_research_deficit_score * 0.25
            + self.governance_lag_score * 0.25
            + self.catastrophic_deployment_risk_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_alignment_risk_index = round(self.composite_score / 100 * 10, 2)

    def _risk(self) -> str:
        s = self.composite_score
        if s >= 60:
            return "critique"
        if s >= 40:
            return "élevé"
        if s >= 20:
            return "modéré"
        return "faible"

    def _pattern(self) -> str:
        if self.arms_race_acceleration_score >= 80 and self.governance_lag_score >= 75:
            return "course_catastrophique"
        if self.alignment_research_deficit_score >= 70:
            return "desalignement_systemique"
        if self.composite_score >= 45:
            return "risque_emergeant"
        if self.composite_score >= 25:
            return "vigilance_requise"
        return "precaution_exemplaire"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Course IA catastrophique dans {n} — puissance IA sans garantie d'alignement",
                "Pression compétitive sacrifiant la sécurité à la vitesse de déploiement",
                "Gouvernance IA en retard critique sur la puissance des systèmes déployés",
            ]
        if self.risk_level == "élevé":
            return [
                f"Désalignement systémique émergent dans {n} — risques de déploiement non-aligné",
                "Investissements en alignement IA insuffisants face à la course à la puissance",
                "Cadres de gouvernance IA inadaptés aux capacités réelles des systèmes",
            ]
        if self.risk_level == "modéré":
            return [
                f"Vigilance requise dans {n} — dynamiques de course partielles détectées",
                "Standards de sécurité IA en développement mais encore insuffisants",
                "Coopération internationale sur l'alignement nécessaire et en construction",
            ]
        return [
            f"{n} maintient une précaution exemplaire sur l'alignement IA",
            "Investissements en recherche sur la sécurité IA proportionnels à la puissance développée",
            "Leadership mondial sur les normes d'alignement et de gouvernance IA",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "arms_race_acceleration_score": self.arms_race_acceleration_score,
            "alignment_research_deficit_score": self.alignment_research_deficit_score,
            "governance_lag_score": self.governance_lag_score,
            "catastrophic_deployment_risk_score": self.catastrophic_deployment_risk_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_alignment_risk_index": self.estimated_alignment_risk_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[AIAlignmentRiskEntity] = [
    AIAlignmentRiskEntity("AR-001", "Chine — Course IA Totale", "Asie", "Domination IA Militaire & Civile", 95.0, 85.0, 92.0, 88.0),
    AIAlignmentRiskEntity("AR-002", "Espac IA Global (OpenAI/Anthropic/Google)", "Cyberespace", "Compétition Privée Accélérée", 85.0, 72.0, 80.0, 78.0),
    AIAlignmentRiskEntity("AR-003", "Russie — IA Militaire", "Europe de l'Est", "Armement IA Autonome", 82.0, 80.0, 85.0, 75.0),
    AIAlignmentRiskEntity("AR-004", "USA — Silicon Valley Race", "Amérique du Nord", "Course Privée vs Réglementation", 78.0, 65.0, 75.0, 72.0),
    AIAlignmentRiskEntity("AR-005", "Golfe & MENA — IA Achetée", "MENA", "Déploiement sans Expertise Alignement", 60.0, 68.0, 62.0, 55.0),
    AIAlignmentRiskEntity("AR-006", "Europe — DSA & AI Act", "Europe", "Régulation mais Pression Compétitive", 40.0, 38.0, 42.0, 35.0),
    AIAlignmentRiskEntity("AR-007", "UK — Frontier AI Safety", "Europe", "Leadership Sécurité IA Partiel", 30.0, 22.0, 28.0, 25.0),
    AIAlignmentRiskEntity("AR-008", "Instituts de Recherche (Anthropic/DeepMind)", "Global", "Précaution Exemplaire & Safety First", 15.0, 8.0, 18.0, 10.0),
]


def summary() -> dict[str, Any]:
    entities = MOCK_ENTITIES
    n = len(entities)
    avg = round(sum(e.composite_score for e in entities) / n, 2)

    risk_dist: dict[str, int] = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    pattern_dist: dict[str, int] = {k: 0 for k in PATTERNS}
    critical_alerts: list[str] = []
    top_risk: list[str] = []

    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
        pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1
        if e.risk_level == "critique":
            critical_alerts.append(f"{e.name}: {e.primary_pattern.replace('_', ' ')}")
            top_risk.append(e.name)

    return {
        "total_entities": n,
        "avg_composite": avg,
        "risk_distribution": risk_dist,
        "pattern_distribution": pattern_dist,
        "top_risk_entities": top_risk,
        "critical_alerts": critical_alerts,
        "last_analysis": "2026-06-20",
        "engine_version": "1.0.0",
        "domain": "ai_alignment",
        "confidence_score": 0.73,
        "data_sources": ["ai_safety_research_index", "frontier_ai_tracker", "arms_race_monitor"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_alignment_risk_index": round(avg / 100 * 10, 2),
    }


def analyze_ai_alignment_risk() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"AI Alignment Risk Engine — {r['total_entities']} zones, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
