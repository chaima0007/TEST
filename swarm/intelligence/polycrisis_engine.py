"""
Caelum Partners — Polycrisis Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Analyse des crises mondiales simultanées et leurs effets de cascade.

Le moteur Polycrisis détecte les configurations où plusieurs crises systémiques
se renforcent mutuellement, créant un risque civilisationnel amplificateur.

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
    "cascade_systemique": {
        "severity_fr": "Critique",
        "action_fr": "Activation cellule crise inter-ministérielle et coordination ONU d'urgence",
        "signal_fr": "≥4 crises simultanées avec interconnexion > 0.70",
    },
    "amplification_reciproque": {
        "severity_fr": "Critique",
        "action_fr": "Révision des plans de résilience systémique nationaux sous 30 jours",
        "signal_fr": "Boucles de rétroaction détectées entre crises climatiques et sociales",
    },
    "tipping_point_regional": {
        "severity_fr": "Élevé",
        "action_fr": "Déploiement ressources préventives dans zones de convergence de crises",
        "signal_fr": "Région à ≥3 crises majeures simultanées avec trajectoire dégradée",
    },
    "stress_test_systemique": {
        "severity_fr": "Modéré",
        "action_fr": "Renforcement des capacités d'absorption et redondance institutionnelle",
        "signal_fr": "Systèmes critiques sous tension simultanée mais non défaillants",
    },
    "resilience_maintenue": {
        "severity_fr": "Faible",
        "action_fr": "Maintien de la veille polycrise et mise à jour des scenarii de risque",
        "signal_fr": "composite_score < 30 — systèmes fonctionnels et capacités d'adaptation préservées",
    },
}


@dataclass
class PolycrisysEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    crisis_density_score: float
    cascade_velocity_score: float
    institutional_resilience_gap_score: float
    global_contagion_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_polycrisis_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.crisis_density_score * 0.30
            + self.cascade_velocity_score * 0.25
            + self.institutional_resilience_gap_score * 0.25
            + self.global_contagion_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_polycrisis_index = round(self.composite_score / 100 * 10, 2)

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
        if self.crisis_density_score >= 80 and self.cascade_velocity_score >= 75:
            return "cascade_systemique"
        if self.cascade_velocity_score >= 70 and self.global_contagion_score >= 65:
            return "amplification_reciproque"
        if self.crisis_density_score >= 55 and self.institutional_resilience_gap_score >= 50:
            return "tipping_point_regional"
        if self.composite_score >= 30:
            return "stress_test_systemique"
        return "resilience_maintenue"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Polycrise critique détectée pour {n} — confluence de crises systémiques",
                "Vitesse de cascade inter-crises au-delà des seuils d'alerte maximaux",
                "Effondrement potentiel des mécanismes de résilience institutionnelle",
            ]
        if self.risk_level == "élevé":
            return [
                f"Risque polycrise élevé pour {n} — surveillance renforcée requise",
                "Plusieurs vecteurs de crise convergents identifiés",
                "Contagion systémique globale en trajectoire dégradée",
            ]
        if self.risk_level == "modéré":
            return [
                f"{n} sous tension polycrisis modérée — veille active recommandée",
                "Stress systémique gérable avec interventions ciblées",
                "Indicateurs de résilience encore dans les limites opérationnelles",
            ]
        return [
            f"{n} maintient sa résilience face aux chocs multiples",
            "Systèmes d'absorption fonctionnels et capacités adaptatives préservées",
            "Polycrise en phase de surveillance — pas d'action urgente requise",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "crisis_density_score": self.crisis_density_score,
            "cascade_velocity_score": self.cascade_velocity_score,
            "institutional_resilience_gap_score": self.institutional_resilience_gap_score,
            "global_contagion_score": self.global_contagion_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_polycrisis_index": self.estimated_polycrisis_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[PolycrisysEntity] = [
    PolycrisysEntity("PC-001", "Système Méditerranéen", "Europe/Afrique du Nord", "Géopolitique Régionale", 88.0, 82.0, 78.0, 76.0),
    PolycrisysEntity("PC-002", "Asie du Sud-Est", "Asie-Pacifique", "Stabilité Régionale", 82.0, 75.0, 72.0, 68.0),
    PolycrisysEntity("PC-003", "Sahel Sub-Saharien", "Afrique", "Développement & Sécurité", 79.0, 71.0, 85.0, 64.0),
    PolycrisysEntity("PC-004", "Arctique Circumpolaire", "Polaire", "Gouvernance Climatique", 58.0, 55.0, 48.0, 52.0),
    PolycrisysEntity("PC-005", "Bassin Amazonien", "Amérique du Sud", "Biodiversité & Climat", 52.0, 48.0, 44.0, 46.0),
    PolycrisysEntity("PC-006", "Europe Centrale-Est", "Europe", "Sécurité Énergétique", 32.0, 28.0, 30.0, 26.0),
    PolycrisysEntity("PC-007", "Océanie Insulaire", "Pacifique", "Adaptation Climatique", 18.0, 14.0, 12.0, 16.0),
    PolycrisysEntity("PC-008", "Scandinavie", "Europe du Nord", "Gouvernance Durable", 8.0, 10.0, 6.0, 9.0),
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
        "domain": "polycrisis",
        "confidence_score": 0.88,
        "data_sources": ["resilience_index", "crisis_monitor_global", "systemic_risk_tracker"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_polycrisis_index": round(avg / 100 * 10, 2),
    }


def analyze_polycrisis() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    import json
    r = summary()
    print(f"Polycrise — {r['total_entities']} régions, avg: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
