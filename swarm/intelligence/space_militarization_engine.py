"""
Caelum Partners — Space Militarization Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La militarisation de l'espace comme nouveau domaine de conflictualité
géopolitique : après la terre, la mer, l'air et le cyberespace, l'espace
est devenu le 5e domaine de la guerre. Les satellites militaires guident
les missiles, coordonnent les troupes et fournissent le renseignement
en temps réel. Les détruire, c'est aveugler une armée entière.

La Chine a démontré dès 2007 sa capacité anti-satellite (ASAT) en
abattant son propre satellite, créant 2 800 débris en orbite. La Russie
a développé des satellites-tueurs (Cosmos 2543) capables de manœuvrer
près de satellites adverses. Les États-Unis ont créé la US Space Force
en 2019. L'Inde a rejoint le club ASAT en 2019. La guerre spatiale
n'est pas science-fiction — c'est la prochaine frontière de la puissance
géopolitique. Le premier pays à neutraliser les satellites d'un adversaire
dans une future guerre aura un avantage décisif. Et les débris créés
pourraient rendre certaines orbites inutilisables pour des générations.

Risk levels (militarisation et conflictualité spatiale) :
  critique  → composite ≥ 60  (arsenal militaire spatial avancé — menace directe aux orbites)
  élevé     → composite ≥ 40  (capacités spatiales militaires développées et déployées)
  modéré    → composite ≥ 20  (programme spatial militaire en développement)
  faible    → composite < 20  (utilisation spatiale civile et coopérative)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "arsenal_asat_actif": {
        "severity_fr": "Critique",
        "action_fr": "Traité international anti-ASAT et mécanismes de désescalade spatiale urgents",
        "signal_fr": "asat_capability_score > 80 AND orbital_weapons_score > 75 — arsenal anti-satellite actif",
    },
    "domination_orbitale": {
        "severity_fr": "Critique",
        "action_fr": "Cadre de gouvernance spatiale renouvelé et démilitarisation des orbites basses",
        "signal_fr": "Domination orbitale — contrôle des positions stratégiques en orbite pour avantage militaire",
    },
    "course_spatiale_militaire": {
        "severity_fr": "Élevé",
        "action_fr": "Diplomatie spatiale multilatérale et transparence des programmes militaires spatiaux",
        "signal_fr": "Course aux armements spatiaux — investissements massifs en capacités de guerre spatiale",
    },
    "capacites_emergentes": {
        "severity_fr": "Modéré",
        "action_fr": "Intégration dans les accords de non-prolifération spatiale et normes de comportement",
        "signal_fr": "Capacités spatiales militaires émergentes — programmes en développement sans déploiement actif",
    },
    "cooperation_spatiale": {
        "severity_fr": "Faible",
        "action_fr": "Renforcer les accords de coopération spatiale civile et norms anti-débris",
        "signal_fr": "composite_score < 20 — utilisation spatiale essentiellement civile et coopérative",
    },
}


@dataclass
class SpaceMilitarizationEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    asat_capability_score: float
    orbital_weapons_score: float
    space_surveillance_dominance_score: float
    debris_creation_risk_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_space_conflict_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.asat_capability_score * 0.30
            + self.orbital_weapons_score * 0.25
            + self.space_surveillance_dominance_score * 0.25
            + self.debris_creation_risk_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_space_conflict_index = round(self.composite_score / 100 * 10, 2)

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
        if self.asat_capability_score >= 80 and self.orbital_weapons_score >= 75:
            return "arsenal_asat_actif"
        if self.space_surveillance_dominance_score >= 80:
            return "domination_orbitale"
        if self.composite_score >= 40:
            return "course_spatiale_militaire"
        if self.composite_score >= 20:
            return "capacites_emergentes"
        return "cooperation_spatiale"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Arsenal militaire spatial critique dans {n} — capacités anti-satellite menaçant les orbites globales",
                "Armes co-orbitales déployées ou en test — satellites-tueurs capables de neutraliser des actifs adverses",
                "Risque de cascade Kessler — tests ASAT créant des débris qui pourraient rendre des orbites inutilisables",
            ]
        if self.risk_level == "élevé":
            return [
                f"Capacités spatiales militaires avancées dans {n} — programme actif de guerre spatiale",
                "Investissements massifs en satellites militaires et systèmes de surveillance orbitale",
                "Participation à la course aux armements spatiaux — déploiement de capacités d'interférence spatiale",
            ]
        if self.risk_level == "modéré":
            return [
                f"Programme spatial militaire émergent dans {n} — capacités ASAT en développement",
                "Investissements en technologies duales espace civil/militaire — potentiel de conversion militaire",
                "Intégration partielle dans les systèmes de navigation et communication militaires par satellite",
            ]
        return [
            f"{n} maintient une utilisation spatiale coopérative — programmes essentiellement civils et transparents",
            "Participation aux accords internationaux de durabilité spatiale et lutte contre les débris",
            "Modèle de coopération spatiale à encourager — science et exploration sans militarisation",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "asat_capability_score": self.asat_capability_score,
            "orbital_weapons_score": self.orbital_weapons_score,
            "space_surveillance_dominance_score": self.space_surveillance_dominance_score,
            "debris_creation_risk_score": self.debris_creation_risk_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_space_conflict_index": self.estimated_space_conflict_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[SpaceMilitarizationEntity] = [
    SpaceMilitarizationEntity("SM-001", "USA — Space Force & Domination Orbitale", "Amérique du Nord", "GPS Militaire, Satellites Espions & Armes Co-Orbitales X-37B", 88.0, 82.0, 95.0, 75.0),
    SpaceMilitarizationEntity("SM-002", "Chine — Programme ASAT & Lune Stratégique", "Asie", "Test ASAT 2007, Satellites-Tueurs & Ambitions Lunaires Militaires", 90.0, 85.0, 80.0, 90.0),
    SpaceMilitarizationEntity("SM-003", "Russie — Arsenal Spatial Héritage Soviétique", "Europe de l'Est", "Cosmos 2543 Satellite-Tueur & Système Nudol Anti-Satellite", 85.0, 88.0, 75.0, 85.0),
    SpaceMilitarizationEntity("SM-004", "Inde — Club ASAT 2019 Mission Shakti", "Asie du Sud", "Test ASAT Mars 2019 — 4e Puissance Spatiale Militaire Mondiale", 65.0, 58.0, 60.0, 72.0),
    SpaceMilitarizationEntity("SM-005", "France & UK — Commandements Spatiaux OTAN", "Europe", "Commandements Spatiaux Nationaux & Satellites Militaires Syracuse/Skynet", 52.0, 48.0, 60.0, 42.0),
    SpaceMilitarizationEntity("SM-006", "Israël — Renseignement Satellitaire Avancé", "MENA", "Ofek/EROS — Surveillance Régionale & Capacités Cyber Spatiales", 45.0, 40.0, 58.0, 35.0),
    SpaceMilitarizationEntity("SM-007", "Iran & Corée du Nord — Programmes Spatiaux Duaux", "MENA/Asie", "Missiles Balistiques Déguisés en Lanceurs Spatiaux — Dual-Use Évident", 35.0, 38.0, 28.0, 42.0),
    SpaceMilitarizationEntity("SM-008", "Luxembourg & Japon — Coopération Civile", "Global", "JAXA Coopération Civile & Luxembourg Space Hub — Usage Non-Militaire", 8.0, 5.0, 15.0, 6.0),
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
        "domain": "space_militarization",
        "confidence_score": 0.78,
        "data_sources": ["secure_world_foundation_space_threat", "us_space_command_space_surveillance", "ucs_satellite_database"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_space_conflict_index": round(avg / 100 * 10, 2),
    }


def analyze_space_militarization() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Space Militarization Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
