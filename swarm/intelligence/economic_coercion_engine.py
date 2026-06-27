"""
Caelum Partners — Economic Coercion Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Détection et analyse de la weaponisation de l'économie mondiale :
sanctions, dépendances stratégiques, guerre commerciale asymétrique
et coercition financière comme instruments de politique étrangère.

La coercition économique est devenue l'arme géopolitique du XXIe siècle —
elle est plus efficace que les bombardements et plus facile à nier.

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
    "guerre_economique_totale": {
        "severity_fr": "Critique",
        "action_fr": "Activation plan de résilience économique nationale — diversification d'urgence des chaînes d'approvisionnement",
        "signal_fr": "dependency_score > 85 AND sanction_exposure > 80 — vulnérabilité coercitive systémique",
    },
    "chantage_strategique": {
        "severity_fr": "Critique",
        "action_fr": "Renforcement des alliances économiques alternatives et réduction des dépendances critiques",
        "signal_fr": "Dépendances critiques exploitées comme levier géopolitique par un acteur dominant",
    },
    "pression_economique_ciblee": {
        "severity_fr": "Élevé",
        "action_fr": "Diversification des partenaires commerciaux et renforcement des réserves stratégiques",
        "signal_fr": "Sanctions sectorielles ou restrictions commerciales ciblées en cours",
    },
    "vulnerabilite_commerciale": {
        "severity_fr": "Modéré",
        "action_fr": "Audit des dépendances stratégiques et plans de contingence commerciale",
        "signal_fr": "Concentration excessive dans les échanges commerciaux — risque de coercition modéré",
    },
    "resilience_economique": {
        "severity_fr": "Faible",
        "action_fr": "Maintien de la veille coercitive et diversification préventive des partenariats",
        "signal_fr": "composite_score < 30 — économie diversifiée et résiliente aux pressions extérieures",
    },
}


@dataclass
class EconomicCoercionEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    dependency_concentration_score: float
    sanction_exposure_score: float
    financial_chokepoint_score: float
    trade_weaponization_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_coercion_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.dependency_concentration_score * 0.30
            + self.sanction_exposure_score * 0.25
            + self.financial_chokepoint_score * 0.25
            + self.trade_weaponization_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_coercion_index = round(self.composite_score / 100 * 10, 2)

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
        if self.dependency_concentration_score >= 85 and self.sanction_exposure_score >= 80:
            return "guerre_economique_totale"
        if self.financial_chokepoint_score >= 75 and self.dependency_concentration_score >= 70:
            return "chantage_strategique"
        if self.composite_score >= 45:
            return "pression_economique_ciblee"
        if self.composite_score >= 25:
            return "vulnerabilite_commerciale"
        return "resilience_economique"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Coercition économique critique pour {n} — dépendances stratégiques exploitées",
                "Exposition aux sanctions et points de contrôle financier au niveau d'alerte maximal",
                "Weaponisation du commerce détectée — autonomie économique compromise",
            ]
        if self.risk_level == "élevé":
            return [
                f"Pression économique élevée sur {n} — vulnérabilité aux leviers coercitifs",
                "Concentrations commerciales excessives créant des angles d'attaque géopolitiques",
                "Risque de chantage stratégique via dépendances critiques identifié",
            ]
        if self.risk_level == "modéré":
            return [
                f"Vulnérabilité coercitive modérée pour {n} — diversification recommandée",
                "Dépendances sectorielles identifiées mais gérables",
                "Résilience économique maintenue avec vigilance stratégique",
            ]
        return [
            f"{n} présente une résilience économique robuste aux pressions coercitives",
            "Diversification commerciale et financière — faible levier coercitif disponible",
            "Autonomie stratégique confirmée — veille coercitive maintenue",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "dependency_concentration_score": self.dependency_concentration_score,
            "sanction_exposure_score": self.sanction_exposure_score,
            "financial_chokepoint_score": self.financial_chokepoint_score,
            "trade_weaponization_score": self.trade_weaponization_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_coercion_index": self.estimated_coercion_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[EconomicCoercionEntity] = [
    EconomicCoercionEntity("EC-001", "Taiwan & Détroit de Formose", "Asie-Pacifique", "Semi-conducteurs & Technologie", 92.0, 85.0, 88.0, 80.0),
    EconomicCoercionEntity("EC-002", "Europe (Dépendance Énergétique)", "Europe", "Énergie & Ressources", 85.0, 78.0, 82.0, 75.0),
    EconomicCoercionEntity("EC-003", "Pays Africains (Piège de Dette)", "Afrique", "Infrastructure & Finance", 80.0, 72.0, 68.0, 78.0),
    EconomicCoercionEntity("EC-004", "Corée du Sud & Japon", "Asie du Nord-Est", "High-Tech & Chaînes Valeur", 70.0, 65.0, 72.0, 62.0),
    EconomicCoercionEntity("EC-005", "Amérique Latine (Dollar Trap)", "Amériques", "Finance & Commodités", 60.0, 58.0, 65.0, 52.0),
    EconomicCoercionEntity("EC-006", "Inde & Asie du Sud-Est", "Asie", "Diversification Stratégique", 42.0, 38.0, 40.0, 35.0),
    EconomicCoercionEntity("EC-007", "États-Unis & Canada", "Amérique du Nord", "Autonomie Économique", 25.0, 22.0, 28.0, 20.0),
    EconomicCoercionEntity("EC-008", "Suisse & Nordiques", "Europe du Nord", "Neutralité & Résilience", 12.0, 8.0, 15.0, 10.0),
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
        "domain": "coercion",
        "confidence_score": 0.84,
        "data_sources": ["trade_dependency_index", "sanctions_tracker", "financial_chokepoints_monitor"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_coercion_index": round(avg / 100 * 10, 2),
    }


def analyze_economic_coercion() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Economic Coercion Engine — {r['total_entities']} régions, avg: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
