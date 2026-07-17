"""
Caelum Partners — Black Swan Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Détection des événements à faible probabilité mais impact civilisationnel extrême.

Un Black Swan est un événement imprévisible avec trois caractéristiques :
1. Extrêmement rare et inattendu
2. Impact massif et potentiellement irréversible
3. Rationalisé rétrospectivement comme prévisible

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
    "cygne_noir_imminent": {
        "severity_fr": "Critique",
        "action_fr": "Activation protocole de résilience extrême et plans de continuité civilisationnelle",
        "signal_fr": "tail_risk_score > 85 AND detectability_gap > 80",
    },
    "accumulation_risques_opaques": {
        "severity_fr": "Critique",
        "action_fr": "Déploiement d'observatoires de risques extrêmes et révision des modèles de prévision",
        "signal_fr": "detectability_gap > 75 ET systemic_fragility > 70",
    },
    "fragility_systemique": {
        "severity_fr": "Élevé",
        "action_fr": "Construction de tampons de résilience et diversification des systèmes critiques",
        "signal_fr": "systemic_fragility entre 50-70 avec dépendances cachées identifiées",
    },
    "signal_faible_critique": {
        "severity_fr": "Élevé",
        "action_fr": "Renforcement des capacités d'écoute des signaux faibles et modèles non-linéaires",
        "signal_fr": "tail_risk_score entre 40-60 avec signaux non-linéaires détectés",
    },
    "vigilance_maintenue": {
        "severity_fr": "Faible",
        "action_fr": "Maintien de la veille systémique et mise à jour des scenarii de choc extrême",
        "signal_fr": "composite_score < 30 — profil de risque normal avec queues de distribution maîtrisées",
    },
}


@dataclass
class BlackSwanEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    tail_risk_score: float
    detectability_gap_score: float
    systemic_fragility_score: float
    cascade_amplification_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_blackswan_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.tail_risk_score * 0.30
            + self.detectability_gap_score * 0.25
            + self.systemic_fragility_score * 0.25
            + self.cascade_amplification_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_blackswan_index = round(self.composite_score / 100 * 10, 2)

    def _risk(self) -> str:
        if self.composite_score >= 60:
            return "critique"
        if self.composite_score >= 40:
            return "élevé"
        if self.composite_score >= 20:
            return "modéré"
        return "faible"

    def _pattern(self) -> str:
        if self.tail_risk_score >= 85 and self.detectability_gap_score >= 80:
            return "cygne_noir_imminent"
        if self.detectability_gap_score >= 75 and self.systemic_fragility_score >= 70:
            return "accumulation_risques_opaques"
        if self.systemic_fragility_score >= 50:
            return "fragility_systemique"
        if self.tail_risk_score >= 40:
            return "signal_faible_critique"
        return "vigilance_maintenue"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Cygne noir potentiel détecté pour {n} — probabilité extrême hors modèles standards",
                "Distribution de queue pathologique — risque catastrophique sous-estimé",
                "Opacité systémique critique — angles morts majeurs dans l'évaluation des risques",
            ]
        if self.risk_level == "élevé":
            return [
                f"Accumulation de fragilités cachées pour {n} — vigilance renforcée requise",
                "Signaux faibles non-linéaires détectés dans les systèmes critiques",
                "Dépendances systémiques opaques à risque d'amplification",
            ]
        if self.risk_level == "modéré":
            return [
                f"Profil de risque extrême modéré pour {n} — suivi régulier conseillé",
                "Fragilités systémiques identifiées mais gérables",
                "Scénarios de choc extrême à modéliser et anticiper",
            ]
        return [
            f"{n} présente un profil de risque extrême maîtrisé",
            "Distribution de risque dans les normes — queues de distribution surveillées",
            "Résilience systémique confirmée — veille continue maintenue",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "tail_risk_score": self.tail_risk_score,
            "detectability_gap_score": self.detectability_gap_score,
            "systemic_fragility_score": self.systemic_fragility_score,
            "cascade_amplification_score": self.cascade_amplification_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_blackswan_index": self.estimated_blackswan_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[BlackSwanEntity] = [
    BlackSwanEntity("BS-001", "Système Financier Global", "Mondial", "Finance Systémique", 92.0, 88.0, 82.0, 78.0),
    BlackSwanEntity("BS-002", "Internet & Infrastructures Numériques", "Mondial", "Infrastructure Critique", 85.0, 80.0, 75.0, 72.0),
    BlackSwanEntity("BS-003", "Chaînes Alimentaires Mondiales", "Mondial", "Sécurité Alimentaire", 78.0, 72.0, 80.0, 68.0),
    BlackSwanEntity("BS-004", "Systèmes Géomagnétiques", "Planète", "Risques Naturels", 55.0, 50.0, 48.0, 52.0),
    BlackSwanEntity("BS-005", "IA Transformative Unbounded", "Mondial", "Technologie Extrême", 58.0, 62.0, 45.0, 48.0),
    BlackSwanEntity("BS-006", "Pandémie Pathogène Inconnu", "Mondial", "Santé Globale", 30.0, 28.0, 32.0, 26.0),
    BlackSwanEntity("BS-007", "Événements Géophysiques Majeurs", "Planète", "Risques Naturels", 16.0, 12.0, 14.0, 18.0),
    BlackSwanEntity("BS-008", "Institutions Multilatérales", "Mondial", "Gouvernance Globale", 8.0, 10.0, 6.0, 9.0),
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
        "domain": "blackswan",
        "confidence_score": 0.72,
        "data_sources": ["tail_risk_models", "systemic_fragility_index", "black_swan_observatory"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_blackswan_index": round(avg / 100 * 10, 2),
    }


def analyze_blackswan() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    import json
    r = summary()
    print(f"Black Swan Engine — {r['total_entities']} domaines, avg: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
