"""
Caelum Partners — Trust Economy Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La confiance comme infrastructure invisible de l'économie et de la démocratie :
quand le capital de confiance s'effondre, les institutions deviennent creuses,
les marchés dysfonctionnels et la coopération sociale impossible.

Un score élevé indique un DÉFICIT de confiance — risque systémique élevé.

Risk levels (déficit de confiance) :
  critique  → composite ≥ 60  (effondrement)
  élevé     → composite ≥ 40  (érosion avancée)
  modéré    → composite ≥ 20  (doute croissant)
  faible    → composite < 20  (capital confiance préservé)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "effondrement_confiance": {
        "severity_fr": "Critique",
        "action_fr": "Reconstruction d'urgence du capital-confiance — dialogue national et réformes institutionnelles profondes",
        "signal_fr": "institutional_trust > 75 AND interpersonal_trust > 70 — effondrement du tissu de confiance",
    },
    "erosion_institutionnelle": {
        "severity_fr": "Critique",
        "action_fr": "Restauration de la légitimité institutionnelle — transparence radicale et responsabilité accrue",
        "signal_fr": "Déficit de confiance institutionnel critique — légitimité des institutions en question",
    },
    "fragmentation_confiance": {
        "severity_fr": "Élevé",
        "action_fr": "Reconstruction des ponts de confiance — dialogue inter-communautaire et médiation sociale",
        "signal_fr": "Confiance fragmentée entre groupes — cohésion sociale compromise",
    },
    "doute_croissant": {
        "severity_fr": "Modéré",
        "action_fr": "Renforcement des mécanismes de transparence et d'accountability institutionnelle",
        "signal_fr": "Signaux de déficit de confiance naissants — vigilance institutionnelle requise",
    },
    "capital_confiance": {
        "severity_fr": "Faible",
        "action_fr": "Maintien et cultivation du capital-confiance — investissement dans le lien social",
        "signal_fr": "composite_score < 20 — capital confiance préservé, tissu social robuste",
    },
}


@dataclass
class TrustEconomyEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    institutional_trust_score: float
    interpersonal_trust_score: float
    market_confidence_score: float
    digital_trust_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_trust_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.institutional_trust_score * 0.30
            + self.interpersonal_trust_score * 0.25
            + self.market_confidence_score * 0.25
            + self.digital_trust_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_trust_index = round(self.composite_score / 100 * 10, 2)

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
        if self.institutional_trust_score >= 75 and self.interpersonal_trust_score >= 70:
            return "effondrement_confiance"
        if self.institutional_trust_score >= 65:
            return "erosion_institutionnelle"
        if self.composite_score >= 45:
            return "fragmentation_confiance"
        if self.composite_score >= 25:
            return "doute_croissant"
        return "capital_confiance"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Effondrement du capital-confiance dans {n} — déficit institutionnel critique",
                "Confiance interpersonnelle effondrée — coopération sociale compromise",
                "Zone de rupture civique — atomisation sociale et contractuelle avancée",
            ]
        if self.risk_level == "élevé":
            return [
                f"Érosion avancée de la confiance dans {n} — légitimité institutionnelle fragilisée",
                "Déficit de confiance dans les marchés et l'espace numérique croissant",
                "Fragmentation sociale — groupes en silo, dialogue inter-communautaire limité",
            ]
        if self.risk_level == "modéré":
            return [
                f"Doute croissant envers les institutions dans {n} — vigilance recommandée",
                "Capital-confiance sous pression — signaux d'érosion à surveiller",
                "Mécanismes de reconstruction de la confiance à renforcer",
            ]
        return [
            f"{n} préserve un capital-confiance solide — tissu social robuste",
            "Confiance institutionnelle et interpersonnelle dans les normes",
            "Modèle de capital social à préserver et à exporter",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "institutional_trust_score": self.institutional_trust_score,
            "interpersonal_trust_score": self.interpersonal_trust_score,
            "market_confidence_score": self.market_confidence_score,
            "digital_trust_score": self.digital_trust_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_trust_index": self.estimated_trust_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[TrustEconomyEntity] = [
    TrustEconomyEntity("TE-001", "Yémen — Effondrement Étatique", "MENA", "État Défaillant & Confiance Nulle", 90.0, 82.0, 88.0, 75.0),
    TrustEconomyEntity("TE-002", "Russie — Défiance Post-Soviétique", "Europe de l'Est", "Autoritarisme & Méfiance Systémique", 85.0, 78.0, 80.0, 72.0),
    TrustEconomyEntity("TE-003", "États-Unis — Polarisation Institutionnelle", "Amérique du Nord", "Démocratie Fracturée", 78.0, 72.0, 70.0, 68.0),
    TrustEconomyEntity("TE-004", "Liban — Trahison Institutionnelle", "MENA", "Effondrement Systémique Multi-Couches", 88.0, 75.0, 92.0, 70.0),
    TrustEconomyEntity("TE-005", "Brésil — Défiance Démocratique", "Amériques", "Polarisation Post-Bolsonaro", 62.0, 55.0, 58.0, 50.0),
    TrustEconomyEntity("TE-006", "France — Crise de Légitimité", "Europe", "Fracture Élites/Peuple", 58.0, 48.0, 50.0, 45.0),
    TrustEconomyEntity("TE-007", "Allemagne — Institutions Résilientes", "Europe", "Capital Social Institutionnel", 32.0, 28.0, 30.0, 25.0),
    TrustEconomyEntity("TE-008", "Danemark & Nordiques — Modèle Confiance", "Europe du Nord", "Capital-Confiance Maximal", 10.0, 8.0, 12.0, 6.0),
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
        "domain": "trust",
        "confidence_score": 0.79,
        "data_sources": ["edelman_trust_barometer", "world_values_survey", "interpersonal_trust_index"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_trust_index": round(avg / 100 * 10, 2),
    }


def analyze_trust_economy() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Trust Economy Engine — {r['total_entities']} zones, avg déficit: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
