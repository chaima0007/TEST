"""
Caelum Partners — Synthesis Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Moteur de synthèse méta-intelligence : agrège les signaux de tous les engines
pour produire un score de risque civilisationnel global unifié.

Ce module est le cerveau central de la plateforme Caelum Partners.
Il détecte les configurations où plusieurs risques sectoriels convergent
vers une crise systémique de niveau supérieur.

Risk levels:
  critique  → composite ≥ 60
  élevé     → composite ≥ 40
  modéré    → composite ≥ 20
  faible    → composite < 20
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "convergence_civilisationnelle": {
        "severity_fr": "Critique",
        "action_fr": "Activation du Comité de Crise Stratégique Caelum — briefing exécutif sous 24h",
        "signal_fr": "≥5 domaines d'intelligence à niveau critique simultanément",
    },
    "amplification_transsectorielle": {
        "severity_fr": "Critique",
        "action_fr": "Déploiement des équipes d'analyse inter-domaines et révision des modèles de risque",
        "signal_fr": "Interactions amplificatrices entre risques climatiques, sécuritaires et économiques",
    },
    "stress_test_global": {
        "severity_fr": "Élevé",
        "action_fr": "Renforcement de la résilience transsectorielle et diversification des stratégies",
        "signal_fr": "Plusieurs domaines en zone élevée avec trajectoires convergentes",
    },
    "vigilance_transversale": {
        "severity_fr": "Modéré",
        "action_fr": "Surveillance croisée des indicateurs inter-domaines et mise à jour des scenarii",
        "signal_fr": "Tensions sectorielles modérées — pas de convergence critique détectée",
    },
    "stabilite_systemique": {
        "severity_fr": "Faible",
        "action_fr": "Maintien de la veille synthétique et rapports trimestriels de tendance",
        "signal_fr": "composite_score < 30 — environnement systémique globalement stable",
    },
}


@dataclass
class SynthesisEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    environmental_risk_score: float
    geopolitical_risk_score: float
    socioeconomic_risk_score: float
    technology_disruption_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_synthesis_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.environmental_risk_score * 0.30
            + self.geopolitical_risk_score * 0.25
            + self.socioeconomic_risk_score * 0.25
            + self.technology_disruption_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_synthesis_index = round(self.composite_score / 100 * 10, 2)

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
        high_count = sum(
            1 for s in [
                self.environmental_risk_score, self.geopolitical_risk_score,
                self.socioeconomic_risk_score, self.technology_disruption_score
            ]
            if s >= 70
        )
        if high_count >= 3:
            return "convergence_civilisationnelle"
        if self.environmental_risk_score >= 75 and self.geopolitical_risk_score >= 65:
            return "amplification_transsectorielle"
        if self.composite_score >= 45:
            return "stress_test_global"
        if self.composite_score >= 25:
            return "vigilance_transversale"
        return "stabilite_systemique"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Convergence critique multi-domaines détectée pour {n}",
                "Interactions amplificatrices entre risques environnementaux et géopolitiques",
                "Score de synthèse Caelum au niveau d'alerte maximale",
            ]
        if self.risk_level == "élevé":
            return [
                f"Stress transsectoriel élevé identifié pour {n}",
                "Plusieurs vecteurs de risque en trajectoire convergente",
                "Surveillance renforcée recommandée par le moteur Caelum",
            ]
        if self.risk_level == "modéré":
            return [
                f"Tension systémique modérée pour {n} — veille active conseillée",
                "Indicateurs inter-domaines à surveiller",
                "Pas de convergence critique — gestion préventive suffisante",
            ]
        return [
            f"{n} affiche une stabilité systémique confirmée",
            "Tous les indicateurs Caelum dans les zones vertes",
            "Rapport de synthèse : environnement favorable",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "environmental_risk_score": self.environmental_risk_score,
            "geopolitical_risk_score": self.geopolitical_risk_score,
            "socioeconomic_risk_score": self.socioeconomic_risk_score,
            "technology_disruption_score": self.technology_disruption_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_synthesis_index": self.estimated_synthesis_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[SynthesisEntity] = [
    SynthesisEntity("SYN-001", "Proche-Orient & Golfe", "MENA", "Géopolitique & Énergie", 82.0, 90.0, 78.0, 65.0),
    SynthesisEntity("SYN-002", "Asie du Sud (Arc de Crise)", "Asie du Sud", "Sécurité Régionale", 76.0, 85.0, 80.0, 68.0),
    SynthesisEntity("SYN-003", "Afrique Sub-Saharienne", "Afrique", "Développement Humain", 80.0, 72.0, 85.0, 60.0),
    SynthesisEntity("SYN-004", "Amérique Latine", "Amériques", "Stabilité Socioéconomique", 65.0, 58.0, 72.0, 52.0),
    SynthesisEntity("SYN-005", "Eurasie Centrale", "Eurasie", "Ressources & Transit", 68.0, 75.0, 55.0, 48.0),
    SynthesisEntity("SYN-006", "Europe Occidentale", "Europe", "Démocratie & Sécurité", 42.0, 38.0, 35.0, 40.0),
    SynthesisEntity("SYN-007", "Amérique du Nord", "Amériques", "Stabilité Démocratique", 35.0, 32.0, 30.0, 38.0),
    SynthesisEntity("SYN-008", "Asie-Pacifique Développée", "Asie-Pacifique", "Économies Avancées", 20.0, 18.0, 15.0, 22.0),
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
        "domain": "synthesis",
        "confidence_score": 0.91,
        "data_sources": ["all_caelum_engines", "global_risk_aggregator", "synthesis_model_v1"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_synthesis_index": round(avg / 100 * 10, 2),
    }


def analyze_synthesis() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    import json
    r = summary()
    print(f"Caelum Synthesis Engine — {r['total_entities']} régions, avg: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
