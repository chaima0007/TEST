"""
Caelum Partners — Complexity Horizon Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La limite de complexité gouvernable : les sociétés modernes accumulent
des couches réglementaires, institutionnelles et technologiques jusqu'au
point où le système ne peut plus se comprendre lui-même — ni s'adapter
assez vite pour survivre aux chocs. C'est l'horizon de complexité.

Au-delà de cet horizon, les décisions politiques deviennent impossibles
à rationaliser, les institutions perdent leur cohérence interne,
et les systèmes s'effondrent non par manque de ressources mais
par excès de complexité non maîtrisée.

Risk levels (surcharge de complexité) :
  critique  → composite ≥ 60  (horizon de complexité dépassé)
  élevé     → composite ≥ 40  (surcharge systémique)
  modéré    → composite ≥ 20  (tension de gouvernance)
  faible    → composite < 20  (résilience institutionnelle)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "collapse_complexite": {
        "severity_fr": "Critique",
        "action_fr": "Simplification d'urgence des systèmes — réforme institutionnelle radicale et décomplexification",
        "signal_fr": "regulatory_complexity > 80 AND coordination_failure > 75 — horizon de complexité dépassé",
    },
    "surcharge_systemique": {
        "severity_fr": "Critique",
        "action_fr": "Réforme structurelle du cadre institutionnel — réduction de la charge cognitive gouvernementale",
        "signal_fr": "Surcharge systémique critique — incohérence politique chronique et paralysie décisionnelle",
    },
    "horizon_complexite": {
        "severity_fr": "Élevé",
        "action_fr": "Simplification progressive des cadres réglementaires et renforcement des capacités adaptatives",
        "signal_fr": "Horizon de complexité approchant — signaux de saturation institutionnelle détectés",
    },
    "tension_gouvernance": {
        "severity_fr": "Modéré",
        "action_fr": "Amélioration de la cohérence des politiques et investissement dans la capacité d'adaptation",
        "signal_fr": "Tension de gouvernance modérée — complexité croissante mais encore maîtrisable",
    },
    "resilience_institutionnelle": {
        "severity_fr": "Faible",
        "action_fr": "Maintien des systèmes d'adaptation et vigilance sur l'accumulation de complexité réglementaire",
        "signal_fr": "composite_score < 20 — résilience institutionnelle confirmée, complexité sous contrôle",
    },
}


@dataclass
class ComplexityHorizonEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    regulatory_complexity_score: float
    institutional_coordination_failure_score: float
    policy_coherence_deficit_score: float
    adaptive_capacity_degradation_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_complexity_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.regulatory_complexity_score * 0.30
            + self.institutional_coordination_failure_score * 0.25
            + self.policy_coherence_deficit_score * 0.25
            + self.adaptive_capacity_degradation_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_complexity_index = round(self.composite_score / 100 * 10, 2)

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
        if self.regulatory_complexity_score >= 80 and self.institutional_coordination_failure_score >= 75:
            return "collapse_complexite"
        if self.institutional_coordination_failure_score >= 65:
            return "surcharge_systemique"
        if self.composite_score >= 45:
            return "horizon_complexite"
        if self.composite_score >= 25:
            return "tension_gouvernance"
        return "resilience_institutionnelle"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Horizon de complexité dépassé pour {n} — effondrement institutionnel imminent",
                "Surcharge réglementaire chronique — les systèmes ne peuvent plus s'auto-comprendre",
                "Paralysie décisionnelle avancée — adaptation impossible à la vitesse des chocs externes",
            ]
        if self.risk_level == "élevé":
            return [
                f"Surcharge systémique élevée dans {n} — incohérence politique chronique détectée",
                "Coordination institutionnelle défaillante — silos bureaucratiques non communicants",
                "Capacité adaptative en dégradation — réponse aux crises de plus en plus lente",
            ]
        if self.risk_level == "modéré":
            return [
                f"Tension de gouvernance modérée dans {n} — complexité croissante mais maîtrisable",
                "Signaux d'accumulation réglementaire à surveiller — risque de seuil critique",
                "Réformes simplificatrices nécessaires pour préserver la capacité d'adaptation",
            ]
        return [
            f"{n} maintient une résilience institutionnelle solide — complexité sous contrôle",
            "Systèmes d'adaptation opérationnels et cohérence politique préservée",
            "Modèle de gouvernance adaptative à étudier et diffuser",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "regulatory_complexity_score": self.regulatory_complexity_score,
            "institutional_coordination_failure_score": self.institutional_coordination_failure_score,
            "policy_coherence_deficit_score": self.policy_coherence_deficit_score,
            "adaptive_capacity_degradation_score": self.adaptive_capacity_degradation_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_complexity_index": self.estimated_complexity_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[ComplexityHorizonEntity] = [
    ComplexityHorizonEntity("CH-001", "Union Européenne — Bureaucratie Maximale", "Europe", "Surréglementation Supranationale", 90.0, 85.0, 82.0, 78.0),
    ComplexityHorizonEntity("CH-002", "États-Unis — Gridlock Fédéral", "Amérique du Nord", "Polarisation & Paralysie Législative", 85.0, 88.0, 80.0, 75.0),
    ComplexityHorizonEntity("CH-003", "Chine — Complexité Autoritaire", "Asie", "Bureaucratie Planifiée & Contrôle Total", 82.0, 78.0, 75.0, 80.0),
    ComplexityHorizonEntity("CH-004", "Inde — Complexité Démocratique", "Asie du Sud", "États Fédéraux & Diversité Réglementaire", 78.0, 72.0, 68.0, 70.0),
    ComplexityHorizonEntity("CH-005", "Brésil — Complexité Tropicale", "Amériques", "Fiscalité & Réglementation Extrêmes", 72.0, 68.0, 75.0, 65.0),
    ComplexityHorizonEntity("CH-006", "Japon — Sclérose Administrative", "Asie du Nord-Est", "Bureaucratie Consensuelle & Lenteur", 55.0, 52.0, 58.0, 48.0),
    ComplexityHorizonEntity("CH-007", "Allemagne — Rigidité Systémique", "Europe", "Précision Réglementaire & Inertie", 35.0, 30.0, 38.0, 28.0),
    ComplexityHorizonEntity("CH-008", "Singapour & Nouvelles-Zélande", "Asie/Pacifique", "Gouvernance Adaptative Exemplaire", 10.0, 8.0, 12.0, 6.0),
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
        "domain": "complexity",
        "confidence_score": 0.78,
        "data_sources": ["world_bank_doing_business", "regulatory_complexity_index", "institutional_quality_monitor"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_complexity_index": round(avg / 100 * 10, 2),
    }


def analyze_complexity_horizon() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Complexity Horizon Engine — {r['total_entities']} zones, avg: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
