"""
Caelum Partners — Space Warfare Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
La militarisation de l'espace : le cinquième domaine de guerre devient le premier.
L'espace est devenu le terrain de confrontation stratégique le plus critique du
XXIe siècle. La destruction d'un seul satellite GPS suffit à paralyser les
communications militaires, la navigation maritime et les systèmes financiers
mondiaux. Les grandes puissances ont transformé l'orbite terrestre en champ
de bataille invisible où se jouent les équilibres géopolitiques futurs.

Les États-Unis opèrent la constellation GPS la plus critique (31 satellites),
les systèmes Starlink de surveillance et les capacités ASAT (anti-satellites)
les plus avancées via le Space Force créé en 2019. La Chine a testé son
missile ASAT SC-19 en 2007 en détruisant son propre satellite — créant 3 000
débris orbitaux — et déploie désormais des satellites co-orbitaux capables de
neutraliser silencieusement les actifs adverses. La Russie a testé son propre
ASAT Nudol en 2021, générant 1 500 débris dangereux pour l'ISS.

L'Inde a rejoint le club ASAT avec Mission Shakti en 2019. La RPDC utilise
des satellites militaires pour la surveillance et le GPS spoofing. La
weaponisation des débris spatiaux constitue désormais une menace de déni
d'accès à l'orbite pour des générations.

Risk levels (militarisation de l'espace et guerre spatiale) :
  critique  → composite ≥ 60  (domination orbitale — capacités ASAT avancées et présence militaire spatiale)
  élevé     → composite ≥ 40  (compétition spatiale active — développement capacités offensives spatiales)
  modéré    → composite ≥ 20  (émergence spatiale — investissements militaires spatiaux sans capacités ASAT)
  faible    → composite < 20  (coopération spatiale civile — respect du Traité de l'Espace Outer Space Treaty)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "domination_orbitale_militaire": {
        "severity_fr": "Critique",
        "action_fr": "Traité ASAT d'urgence — moratoire international sur les tests ASAT destructeurs, registre obligatoire des satellites militaires et mécanisme de désescalade orbitale",
        "signal_fr": "anti_satellite_capability_score > 85 AND orbital_dominance_score > 85 — domination orbitale militaire combinant capacités ASAT avancées et contrôle des orbites stratégiques",
    },
    "destruction_anti_satellite": {
        "severity_fr": "Critique",
        "action_fr": "Coalition anti-débris spatiaux — sanctions contre les États testant des ASAT destructeurs, fonds de compensation pour les opérateurs victimes et normes de comportement responsable",
        "signal_fr": "anti_satellite_capability_score > 85 — capacités ASAT avancées menaçant la durabilité des orbites et l'accès à l'espace pour tous",
    },
    "debris_espace_tactique": {
        "severity_fr": "Critique",
        "action_fr": "Nettoyage orbital forcé — obligation de désorbitage actif des débris créés intentionnellement et responsabilité financière des États pollueurs orbitaux",
        "signal_fr": "space_debris_weaponization_score > 85 — weaponisation des débris spatiaux comme outil de déni d'accès orbital aux adversaires",
    },
    "competition_spatiale_strategique": {
        "severity_fr": "Élevé",
        "action_fr": "Diplomatie spatiale préventive — dialogue bilat USA-Chine-Russie sur les normes spatiales militaires et mécanismes de déconfliction orbitale",
        "signal_fr": "Compétition spatiale stratégique — développement de capacités offensives spatiales sans qualification de domination orbitale",
    },
    "cooperation_spatiale_exemplaire": {
        "severity_fr": "Faible",
        "action_fr": "Renforcer l'Outer Space Treaty — protocoles additionnels sur les armes spatiales, transparence des budgets spatiaux militaires et partage du domaine de conscience situationnelle",
        "signal_fr": "composite_score < 20 — engagement sincère dans la coopération spatiale civile et respect des normes internationales de l'espace",
    },
}


@dataclass
class SpaceWarfareEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    anti_satellite_capability_score: float
    orbital_dominance_score: float
    space_debris_weaponization_score: float
    gps_jamming_spoofing_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_space_warfare_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.anti_satellite_capability_score * 0.30
            + self.orbital_dominance_score * 0.25
            + self.space_debris_weaponization_score * 0.25
            + self.gps_jamming_spoofing_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_space_warfare_index = round(self.composite_score / 100 * 10, 2)

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
        if self.anti_satellite_capability_score >= 85 and self.orbital_dominance_score >= 85:
            return "domination_orbitale_militaire"
        if self.anti_satellite_capability_score >= 85:
            return "destruction_anti_satellite"
        if self.space_debris_weaponization_score >= 85:
            return "debris_espace_tactique"
        if self.composite_score >= 20:
            return "competition_spatiale_strategique"
        return "cooperation_spatiale_exemplaire"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Domination orbitale militaire de {n} — capacités ASAT opérationnelles et constellation de satellites militaires menaçant l'accès à l'espace des adversaires",
                "Weaponisation de l'orbite — satellites co-orbitaux offensifs, GPS spoofing tactique et arsenal de destruction orbitale prêt à l'emploi",
                "Course aux armements spatiaux systémique — investissements massifs dans le Space Force, lasers orbitaux et missiles ASAT de nouvelle génération",
            ]
        if self.risk_level == "élevé":
            return [
                f"Compétition spatiale stratégique de {n} — développement actif de capacités offensives spatiales sans domination orbitale établie",
                "Militarisation croissante — satellites de renseignement, capacités de brouillage GPS et missiles anti-satellites en cours de développement",
                "Risque d'escalade orbitale — toute destruction de satellite pourrait créer des débris menaçant l'ensemble des actifs spatiaux civils et militaires",
            ]
        if self.risk_level == "modéré":
            return [
                f"Émergence spatiale militaire de {n} — investissements spatiaux défensifs sans capacités ASAT avérées mais trajectoire inquiétante",
                "Dépendance satellite croissante — vulnérabilité aux attaques sur les infrastructures spatiales dans un contexte de militarisation accélérée",
                "Risque de prolifération ASAT — pression pour développer des capacités autonomes face aux menaces des grandes puissances spatiales",
            ]
        return [
            f"{n} incarne la coopération spatiale exemplaire — respect de l'Outer Space Treaty, transparence des activités spatiales et désarmement orbital",
            "Usage pacifique de l'espace — satellites civils, coopération scientifique et refus de développer des capacités offensives anti-satellites",
            "Modèle de gouvernance spatiale — promotion des normes de comportement responsable et financement des mécanismes de déconfliction orbitale",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "anti_satellite_capability_score": self.anti_satellite_capability_score,
            "orbital_dominance_score": self.orbital_dominance_score,
            "space_debris_weaponization_score": self.space_debris_weaponization_score,
            "gps_jamming_spoofing_score": self.gps_jamming_spoofing_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_space_warfare_index": self.estimated_space_warfare_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[SpaceWarfareEntity] = [
    SpaceWarfareEntity("SW-001", "USA — Space Force ASAT & Constellation GPS/Starlink", "Amérique du Nord", "Space Force 2019 16Md$ Budget, GPS 31 Satellites Critiques, Starlink 6000+ & ASAT Direct Ascent", 92.0, 95.0, 75.0, 82.0),
    SpaceWarfareEntity("SW-002", "Chine — ASAT SC-19 & Satellites Co-Orbitaux Furtifs", "Asie", "Test ASAT 2007 3000 Débris, Satellites Co-Orbitaux Offensifs, BeiDou 35 Satellites & Lasers Anti-Satellite", 88.0, 85.0, 82.0, 80.0),
    SpaceWarfareEntity("SW-003", "Russie — Nudol ASAT & Guerre Électronique Orbitale", "Europe de l'Est", "Test Nudol 2021 1500 Débris, GLONASS Spoofing Syrie/Finlande, Satellites Espion Kosmos & Brouilleurs GPS", 85.0, 78.0, 92.0, 75.0),
    SpaceWarfareEntity("SW-004", "Inde — Mission Shakti & Programme Spatial Militaire", "Asie du Sud", "Mission Shakti ASAT 2019, ISRO Militarisation Croissante, Satellites ISR & Défense Anti-Missiles Orbitale", 72.0, 68.0, 55.0, 65.0),
    SpaceWarfareEntity("SW-005", "Iran & RPDC — Satellites Militaires & GPS Spoofing", "MENA/Asie", "RPDC Satellite Reconn. Malligyong-1, Iran Pars 1 Militaire, GPS Spoofing Golfe Persique & Cyber Orbital", 48.0, 42.0, 38.0, 62.0),
    SpaceWarfareEntity("SW-006", "France & UE — Espace Militaire Émergent", "Europe", "Syracuse 4A/4B Militaires, Composante Spatiale Opérationnelle, Laser DEW Sirius & Surveillance Orbitale", 40.0, 45.0, 28.0, 52.0),
    SpaceWarfareEntity("SW-007", "Japon & Australie — Partenaires Spatiaux USA", "Asie-Pacifique", "JAXA Dual-Use Spatial, Australie Space Command, Accords Five Eyes Spatiale & Satellites ISR Partagés", 30.0, 28.0, 22.0, 35.0),
    SpaceWarfareEntity("SW-008", "UIT & COPUOS — Gouvernance Spatiale Internationale", "Global", "Outer Space Treaty 1967, COPUOS Lignes Directrices Débris, UIT Fréquences & Rescue Agreement Astronautes", 5.0, 4.0, 3.0, 6.0),
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
        "domain": "space_warfare",
        "confidence_score": 0.79,
        "data_sources": ["secure_world_foundation_space_security", "unidir_space_security_monitor", "us_space_force_strategic_digest"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_space_warfare_index": round(avg / 100 * 10, 2),
    }


def analyze_space_warfare() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Space Warfare Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
