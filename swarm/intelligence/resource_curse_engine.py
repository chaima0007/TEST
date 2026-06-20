"""
Caelum Partners — Resource Curse Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Le paradoxe de la richesse des ressources naturelles : les pays
abondamment dotés en pétrole, minéraux ou gaz souffrent souvent
d'institutions plus faibles, de moins de démocratie, d'une croissance
plus lente et de conflits plus fréquents que leurs voisins moins fortunés.

La malédiction des ressources n'est pas inévitable — la Norvège l'a évitée.
Mais elle frappe ceux qui ne maîtrisent pas la rente, laissant les élites
capturer les richesses pendant que les institutions se dégradent.

Risk levels (intensité de la malédiction des ressources) :
  critique  → composite ≥ 60  (malédiction totale)
  élevé     → composite ≥ 40  (dépendance rentière avancée)
  modéré    → composite ≥ 20  (syndrome hollandais partiel)
  faible    → composite < 20  (diversification réussie)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "malediction_ressources_totale": {
        "severity_fr": "Critique",
        "action_fr": "Réforme radicale de la gouvernance de la rente et diversification économique d'urgence",
        "signal_fr": "resource_dependency > 80 AND institutional_degradation > 75 — malédiction totale confirmée",
    },
    "dependance_rentiere_critique": {
        "severity_fr": "Critique",
        "action_fr": "Fonds souverain et règle budgétaire anti-cyclique — désengagement de la rente par étapes",
        "signal_fr": "Dépendance rentière critique — économie mono-produit sans diversification suffisante",
    },
    "syndrome_hollandais": {
        "severity_fr": "Élevé",
        "action_fr": "Politique industrielle de diversification et protection des secteurs non-rentiers",
        "signal_fr": "Syndrome hollandais actif — désindustrialisation et compétitivité hors-ressources en chute",
    },
    "rente_moderee": {
        "severity_fr": "Modéré",
        "action_fr": "Renforcement des institutions et investissement dans l'économie du savoir",
        "signal_fr": "Rente modérée avec signaux de diversification — trajectoire à surveiller",
    },
    "diversification_reussie": {
        "severity_fr": "Faible",
        "action_fr": "Maintien de la discipline budgétaire et des investissements dans la compétitivité hors-ressources",
        "signal_fr": "composite_score < 20 — diversification réussie, ressources gérées sans malédiction",
    },
}


@dataclass
class ResourceCurseEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    resource_dependency_score: float
    institutional_degradation_score: float
    dutch_disease_score: float
    elite_capture_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_curse_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.resource_dependency_score * 0.30
            + self.institutional_degradation_score * 0.25
            + self.dutch_disease_score * 0.25
            + self.elite_capture_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_curse_index = round(self.composite_score / 100 * 10, 2)

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
        if self.resource_dependency_score >= 80 and self.institutional_degradation_score >= 75:
            return "malediction_ressources_totale"
        if self.resource_dependency_score >= 65:
            return "dependance_rentiere_critique"
        if self.composite_score >= 45:
            return "syndrome_hollandais"
        if self.composite_score >= 25:
            return "rente_moderee"
        return "diversification_reussie"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Malédiction des ressources totale pour {n} — institutions corrompues par la rente",
                "Dépendance mono-produit extrême — économie non diversifiée et vulnérable aux chocs",
                "Capture de la rente par les élites — inégalités structurelles et instabilité chronique",
            ]
        if self.risk_level == "élevé":
            return [
                f"Dépendance rentière avancée dans {n} — syndrome hollandais en cours",
                "Désindustrialisation liée à la rente — secteurs non-ressources en déclin",
                "Capture partielle de la rente — institutions fragilisées mais non effondrées",
            ]
        if self.risk_level == "modéré":
            return [
                f"Rente modérée dans {n} — risque de syndrome hollandais à surveiller",
                "Diversification en cours mais dépendance aux ressources encore significative",
                "Institutions sous pression de la rente — réformes nécessaires",
            ]
        return [
            f"{n} a réussi à transformer la richesse en ressources en développement durable",
            "Fonds souverain et discipline budgétaire permettant la diversification",
            "Modèle de gestion des ressources à étudier et diffuser",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "resource_dependency_score": self.resource_dependency_score,
            "institutional_degradation_score": self.institutional_degradation_score,
            "dutch_disease_score": self.dutch_disease_score,
            "elite_capture_score": self.elite_capture_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_curse_index": self.estimated_curse_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[ResourceCurseEntity] = [
    ResourceCurseEntity("RC-001", "Venezuela — Effondrement Pétrolier", "Amériques", "Malédiction Pétrolière Totale", 95.0, 92.0, 90.0, 88.0),
    ResourceCurseEntity("RC-002", "Nigeria — Pétrole & Corruption", "Afrique", "Delta du Niger & Rente Confisquée", 88.0, 85.0, 82.0, 90.0),
    ResourceCurseEntity("RC-003", "RDC — Minerais & Guerre", "Afrique", "Coltan, Or & Conflits Armés Perpétuels", 85.0, 90.0, 78.0, 92.0),
    ResourceCurseEntity("RC-004", "Angola — Pétrole & Oligarchie", "Afrique", "Rente Pétrolière & Exclusion Massive", 82.0, 80.0, 75.0, 85.0),
    ResourceCurseEntity("RC-005", "Irak — Pétrodépendance Totale", "MENA", "Pétrole & Instabilité Politique Chronique", 78.0, 72.0, 70.0, 75.0),
    ResourceCurseEntity("RC-006", "Arabie Saoudite — Vision 2030", "MENA", "Transition Difficile de la Rente Pétrolière", 72.0, 58.0, 65.0, 60.0),
    ResourceCurseEntity("RC-007", "Botswana — Diamants Bien Gérés", "Afrique", "Réussite Partielle de Diversification", 40.0, 30.0, 35.0, 28.0),
    ResourceCurseEntity("RC-008", "Norvège — Modèle de Gestion", "Europe du Nord", "Fonds Souverain & Diversification Exemplaire", 35.0, 12.0, 18.0, 10.0),
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
        "domain": "resource_curse",
        "confidence_score": 0.83,
        "data_sources": ["natural_resource_governance_index", "imf_resource_tracker", "transparency_international"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_curse_index": round(avg / 100 * 10, 2),
    }


def analyze_resource_curse() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Resource Curse Engine — {r['total_entities']} zones, avg malédiction: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
