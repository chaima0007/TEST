"""
Caelum Partners — Longevity Inequality Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La divergence des espérances de vie comme nouvelle fracture civilisationnelle :
quand les riches vivent 20 ans de plus que les pauvres dans la même ville,
et que les technologies de longévité créent une nouvelle classe d'immortels
potentiels pendant que la majorité meurt prématurément, la démocratie
elle-même est menacée par cette asymétrie temporelle fondamentale.

Celui qui vit plus longtemps accumule plus — de capital, de savoirs,
de pouvoir. La longévité inégale est l'inégalité ultime.

Risk levels (fracture de longévité) :
  critique  → composite ≥ 60  (bifurcation mortelle)
  élevé     → composite ≥ 40  (exclusion de longévité avancée)
  modéré    → composite ≥ 20  (disparité croissante)
  faible    → composite < 20  (accès équitable à la longévité)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "bifurcation_mortelle": {
        "severity_fr": "Critique",
        "action_fr": "Politique de santé universelle d'urgence et régulation des technologies de longévité",
        "signal_fr": "lifespan_gap > 80 AND longevity_tech_exclusion > 75 — bifurcation mortelle en cours",
    },
    "exclusion_longevite": {
        "severity_fr": "Critique",
        "action_fr": "Garantie constitutionnelle d'accès aux technologies de longévité — réforme des soins de santé",
        "signal_fr": "Exclusion de longévité critique — nouvelles classes d'âge créant des castes biologiques",
    },
    "fracture_sante_profonde": {
        "severity_fr": "Élevé",
        "action_fr": "Investissement massif en santé préventive et démocratisation des thérapies de longévité",
        "signal_fr": "Fracture sanitaire profonde — espérance de vie divergeant entre groupes socio-économiques",
    },
    "disparite_croissante": {
        "severity_fr": "Modéré",
        "action_fr": "Renforcement des systèmes de santé universels et encadrement des bio-inégalités émergentes",
        "signal_fr": "Disparités de longévité croissantes — signaux précoces de bifurcation biologique",
    },
    "acces_equitable": {
        "severity_fr": "Faible",
        "action_fr": "Maintien et extension des politiques de santé équitables et veille sur les nouvelles thérapies",
        "signal_fr": "composite_score < 20 — accès équitable à la longévité, écarts d'espérance de vie limités",
    },
}


@dataclass
class LongevityInequalityEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    lifespan_gap_score: float
    health_access_inequality_score: float
    longevity_tech_exclusion_score: float
    demographic_bifurcation_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_longevity_fracture_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.lifespan_gap_score * 0.30
            + self.health_access_inequality_score * 0.25
            + self.longevity_tech_exclusion_score * 0.25
            + self.demographic_bifurcation_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_longevity_fracture_index = round(self.composite_score / 100 * 10, 2)

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
        if self.lifespan_gap_score >= 80 and self.longevity_tech_exclusion_score >= 75:
            return "bifurcation_mortelle"
        if self.health_access_inequality_score >= 70:
            return "exclusion_longevite"
        if self.composite_score >= 45:
            return "fracture_sante_profonde"
        if self.composite_score >= 25:
            return "disparite_croissante"
        return "acces_equitable"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Bifurcation mortelle critique dans {n} — classes biologiques émergentes par accès aux soins",
                "Écarts d'espérance de vie de 20+ ans entre groupes socio-économiques",
                "Technologies de longévité réservées aux ultra-riches — inégalité biologique institutionnalisée",
            ]
        if self.risk_level == "élevé":
            return [
                f"Exclusion de longévité avancée dans {n} — accès inégal aux soins et thérapies",
                "Fracture sanitaire profonde entre classes sociales — mortalité prématurée évitable",
                "Accumulation d'inégalités biologiques compromettant la cohésion sociale",
            ]
        if self.risk_level == "modéré":
            return [
                f"Disparités de longévité croissantes dans {n} — signaux précoces à surveiller",
                "Accès aux soins préventifs inégalement réparti — risque de bifurcation future",
                "Régulation des bio-inégalités émergentes nécessaire",
            ]
        return [
            f"{n} maintient un accès équitable à la longévité — système de santé universel opérationnel",
            "Écarts d'espérance de vie limités et tendances à la convergence",
            "Modèle d'équité sanitaire à préserver et à exporter",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "lifespan_gap_score": self.lifespan_gap_score,
            "health_access_inequality_score": self.health_access_inequality_score,
            "longevity_tech_exclusion_score": self.longevity_tech_exclusion_score,
            "demographic_bifurcation_score": self.demographic_bifurcation_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_longevity_fracture_index": self.estimated_longevity_fracture_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[LongevityInequalityEntity] = [
    LongevityInequalityEntity("LI-001", "États-Unis — Santé Privatisée", "Amérique du Nord", "Inégalité Sanitaire Maximale", 88.0, 90.0, 85.0, 82.0),
    LongevityInequalityEntity("LI-002", "Afrique Subsaharienne — Accès Zéro", "Afrique", "Exclusion Totale Soins & Longévité", 92.0, 88.0, 95.0, 80.0),
    LongevityInequalityEntity("LI-003", "Chine — Dualisme Urbain/Rural", "Asie", "Fracture Sanitaire Géographique", 78.0, 82.0, 75.0, 72.0),
    LongevityInequalityEntity("LI-004", "Inde — Inégalité Sanitaire Extrême", "Asie du Sud", "Castes & Accès aux Soins", 82.0, 85.0, 78.0, 70.0),
    LongevityInequalityEntity("LI-005", "Brésil — Fracture Raciale & Sanitaire", "Amériques", "Inégalités Structurelles de Longévité", 68.0, 72.0, 65.0, 62.0),
    LongevityInequalityEntity("LI-006", "Europe Centrale & Orientale", "Europe", "Fracture Est/Ouest de Longévité", 45.0, 48.0, 42.0, 40.0),
    LongevityInequalityEntity("LI-007", "Europe Occidentale — Accès Partiel", "Europe", "Systèmes Universels Sous Pression", 25.0, 28.0, 22.0, 20.0),
    LongevityInequalityEntity("LI-008", "Nordiques & Japon — Modèle Équité", "Europe du Nord/Asie", "Longévité Équitable Exemplaire", 8.0, 10.0, 6.0, 5.0),
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
        "domain": "longevity_ineq",
        "confidence_score": 0.80,
        "data_sources": ["who_lifespan_data", "health_inequality_tracker", "longevity_tech_access_monitor"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_longevity_fracture_index": round(avg / 100 * 10, 2),
    }


def analyze_longevity_inequality() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Longevity Inequality Engine — {r['total_entities']} zones, avg: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
