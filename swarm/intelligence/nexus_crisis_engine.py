"""
Caelum Partners — Nexus Crisis Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Analyse de la convergence des crises Eau-Alimentation-Énergie :
le triple nexus qui menace la stabilité de civilisations entières.

La crise du Nexus survient quand les stress hydriques, alimentaires
et énergétiques se renforcent mutuellement, créant un vortex systémique
impossible à gérer de manière sectorielle.

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
    "vortex_nexus_total": {
        "severity_fr": "Critique",
        "action_fr": "Plan d'urgence Nexus inter-agences ONU — coordination PNUE/FAO/AIE sous 72h",
        "signal_fr": "Stress hydrique + déficit alimentaire + dépendance énergétique simultanés > 80",
    },
    "cascade_eau_energie": {
        "severity_fr": "Critique",
        "action_fr": "Déploiement solutions Nexus transfrontalières et accords de coopération régionale urgents",
        "signal_fr": "Couplage eau-énergie critique — effets de cascade inter-sectoriel détectés",
    },
    "tension_nexus_elevee": {
        "severity_fr": "Élevé",
        "action_fr": "Renforcement des infrastructures Nexus et diversification des sources eau/énergie/alimentaire",
        "signal_fr": "Tensions sectorielles convergentes — fragilité systémique croissante du Nexus",
    },
    "stress_sectoriel": {
        "severity_fr": "Modéré",
        "action_fr": "Plans d'adaptation sectoriels et investissements dans l'efficacité Nexus",
        "signal_fr": "Stress modéré dans un ou deux secteurs du Nexus — gestion préventive suffisante",
    },
    "nexus_resilient": {
        "severity_fr": "Faible",
        "action_fr": "Maintien de la veille Nexus et développement durable des ressources",
        "signal_fr": "composite_score < 30 — Nexus eau-alimentation-énergie globalement en équilibre",
    },
}


@dataclass
class NexusCrisisEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    water_stress_score: float
    food_security_deficit_score: float
    energy_dependency_score: float
    nexus_coupling_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_nexus_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.water_stress_score * 0.30
            + self.food_security_deficit_score * 0.25
            + self.energy_dependency_score * 0.25
            + self.nexus_coupling_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_nexus_index = round(self.composite_score / 100 * 10, 2)

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
        if self.water_stress_score >= 80 and self.food_security_deficit_score >= 75 and self.energy_dependency_score >= 75:
            return "vortex_nexus_total"
        if self.water_stress_score >= 75 and self.nexus_coupling_score >= 70:
            return "cascade_eau_energie"
        if self.composite_score >= 45:
            return "tension_nexus_elevee"
        if self.composite_score >= 25:
            return "stress_sectoriel"
        return "nexus_resilient"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Vortex Nexus critique pour {n} — convergence eau-alimentation-énergie en rupture",
                "Effets de cascade inter-sectoriels au-delà des seuils de résilience systémique",
                "Couplage Nexus pathologique — gestion sectorielle insuffisante, intervention systémique requise",
            ]
        if self.risk_level == "élevé":
            return [
                f"Tensions Nexus élevées pour {n} — fragilité systémique croissante",
                "Stress hydrique et alimentaire convergents — pression sur les infrastructures énergétiques",
                "Risque d'amplification réciproque des déficits sectoriels",
            ]
        if self.risk_level == "modéré":
            return [
                f"Stress Nexus modéré pour {n} — surveillance multi-sectorielle recommandée",
                "Tensions localisées dans un ou deux compartiments du Nexus",
                "Plans d'adaptation disponibles — intervention ciblée suffisante",
            ]
        return [
            f"{n} maintient un équilibre Nexus eau-alimentation-énergie sain",
            "Ressources hydriques, alimentaires et énergétiques dans les normes durables",
            "Résilience Nexus confirmée — veille continue maintenue",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "water_stress_score": self.water_stress_score,
            "food_security_deficit_score": self.food_security_deficit_score,
            "energy_dependency_score": self.energy_dependency_score,
            "nexus_coupling_score": self.nexus_coupling_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_nexus_index": self.estimated_nexus_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[NexusCrisisEntity] = [
    NexusCrisisEntity("NX-001", "Sahel & Corne de l'Afrique", "Afrique", "Sécurité Alimentaire Hydrique", 92.0, 88.0, 80.0, 85.0),
    NexusCrisisEntity("NX-002", "Moyen-Orient & Péninsule Arabique", "MENA", "Eau & Énergie Fossile", 90.0, 78.0, 35.0, 82.0),
    NexusCrisisEntity("NX-003", "Asie du Sud (Gange-Indus)", "Asie du Sud", "Agriculture & Eau Souterraine", 82.0, 80.0, 65.0, 78.0),
    NexusCrisisEntity("NX-004", "Asie Centrale (Mer d'Aral)", "Asie Centrale", "Eau & Agriculture", 88.0, 75.0, 70.0, 80.0),
    NexusCrisisEntity("NX-005", "Amérique Centrale", "Amériques", "Corridor de la Sécheresse", 65.0, 62.0, 58.0, 55.0),
    NexusCrisisEntity("NX-006", "Europe Méditerranéenne", "Europe", "Agriculture & Eau Douce", 48.0, 42.0, 38.0, 45.0),
    NexusCrisisEntity("NX-007", "Amérique du Nord", "Amériques", "Aquifères & Énergie", 32.0, 25.0, 28.0, 30.0),
    NexusCrisisEntity("NX-008", "Europe du Nord", "Europe", "Ressources Durables", 12.0, 10.0, 15.0, 8.0),
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
        "domain": "nexus",
        "confidence_score": 0.89,
        "data_sources": ["water_stress_index", "global_food_security_index", "energy_dependency_tracker"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_nexus_index": round(avg / 100 * 10, 2),
    }


def analyze_nexus_crisis() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Nexus Crisis Engine — {r['total_entities']} régions, avg: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
