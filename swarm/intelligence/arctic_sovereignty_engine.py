"""Caelum Partners — Arctic Sovereignty Intelligence Engine
Propriété exclusive de Chaima Mhadbi, Fondatrice Caelum Partners, Bruxelles.
"""
from __future__ import annotations

import dataclasses
import logging
import typing

logger = logging.getLogger("swarm.arctic")

DOMAIN = "arctic"


PATTERNS: list[dict[str, str]] = [
    {
        "name": "tension_territoriale",
        "severity_fr": "crise_tension_territoriale_arctique_systémique",
        "action_fr": "intervention_urgente_souveraineté_territoriale_arctique",
        "signal_fr": "Revendications territoriales arctiques critiques — escalade imminente",
    },
    {
        "name": "militarisation_acceleree",
        "severity_fr": "crise_militarisation_arctique_majeure",
        "action_fr": "renforcement_surveillance_militaire_arctique",
        "signal_fr": "Militarisation accélérée de l'Arctique — présence armée en hausse",
    },
    {
        "name": "ruee_ressources",
        "severity_fr": "crise_ruée_ressources_arctiques_active",
        "action_fr": "surveillance_renforcée_exploitation_ressources_arctiques",
        "signal_fr": "Ruée vers les ressources arctiques — compétition énergétique intense",
    },
    {
        "name": "crise_climatique_arctique",
        "severity_fr": "crise_climatique_arctique_critique",
        "action_fr": "alerte_crise_climatique_arctique_urgente",
        "signal_fr": "Crise climatique arctique — fonte des glaces à un rythme alarmant",
    },
    {
        "name": "stabilite_arctique",
        "severity_fr": "surveillance_stabilité_arctique_continue",
        "action_fr": "veille_géopolitique_arctique_continue",
        "signal_fr": "Stabilité arctique sous surveillance — pas de menace imminente",
    },
]

PATTERN_NAMES = [p["name"] for p in PATTERNS]


def _get_pattern(
    territorial_score: float,
    military_score: float,
    resource_score: float,
    climate_score: float,
) -> dict[str, str]:
    if territorial_score >= 70:
        return PATTERNS[0]
    if military_score >= 70:
        return PATTERNS[1]
    if resource_score >= 70:
        return PATTERNS[2]
    if climate_score >= 70:
        return PATTERNS[3]
    return PATTERNS[4]


def _composite(territorial: float, military: float, resource: float, climate: float) -> float:
    return round(territorial * 0.30 + military * 0.25 + resource * 0.25 + climate * 0.20, 2)


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critique"
    if composite >= 40:
        return "élevé"
    if composite >= 20:
        return "modéré"
    return "faible"


@dataclasses.dataclass
class ArcticEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    territorial_score: float
    military_score: float
    resource_score: float
    climate_score: float
    key_signals: list[str]
    last_updated: str
    disputed_zones: int

    def to_dict(self) -> dict[str, typing.Any]:
        composite = _composite(
            self.territorial_score,
            self.military_score,
            self.resource_score,
            self.climate_score,
        )
        risk = _risk_level(composite)
        pattern = _get_pattern(
            self.territorial_score,
            self.military_score,
            self.resource_score,
            self.climate_score,
        )
        estimated_arctic_index = round(composite / 100 * 10, 2)
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": composite,
            "territorial_score": self.territorial_score,
            "military_score": self.military_score,
            "resource_score": self.resource_score,
            "climate_score": self.climate_score,
            "risk_level": risk,
            "primary_pattern": pattern["name"],
            "key_signals": self.key_signals,
            "estimated_arctic_index": estimated_arctic_index,
            "last_updated": self.last_updated,
            "disputed_zones": self.disputed_zones,
        }


MOCK_ENTITIES: list[ArcticEntity] = [
    # ENT-001 — Russia Arctic Command → composite ~79 (critique), tension_territoriale
    ArcticEntity(
        entity_id="ENT-001",
        name="Russia Arctic Command",
        country="Russie",
        sector="Défense & Militaire",
        territorial_score=88.0,
        military_score=85.0,
        resource_score=72.0,
        climate_score=55.0,
        key_signals=[
            "Revendications territoriales massives sur le plateau continental arctique",
            "Déploiement de nouvelles bases militaires en Arctique profond",
            "Contrôle stratégique des routes maritimes nordiques renforcé",
        ],
        last_updated="2026-06-20",
        disputed_zones=7,
    ),
    # ENT-002 — China Arctic Silk Road → composite ~67 (critique), tension_territoriale
    ArcticEntity(
        entity_id="ENT-002",
        name="China Arctic Silk Road",
        country="Chine",
        sector="Infrastructure & Commerce",
        territorial_score=72.0,
        military_score=65.0,
        resource_score=75.0,
        climate_score=52.0,
        key_signals=[
            "Investissements massifs dans les infrastructures portuaires arctiques",
            "Route de la Soie Polaire : accès commercial aux ressources énergétiques",
            "Présence scientifique et économique croissante en Arctique",
        ],
        last_updated="2026-06-20",
        disputed_zones=4,
    ),
    # ENT-003 — US Coast Guard Arctic → composite ~61 (critique), tension_territoriale
    ArcticEntity(
        entity_id="ENT-003",
        name="US Coast Guard Arctic",
        country="États-Unis",
        sector="Sécurité Maritime",
        territorial_score=70.0,
        military_score=68.0,
        resource_score=55.0,
        climate_score=42.0,
        key_signals=[
            "Renforcement des patrouilles maritimes dans les eaux arctiques disputées",
            "Modernisation de la flotte brise-glace pour opérations polaires",
            "Surveillance accrue des activités russes et chinoises en Arctique",
        ],
        last_updated="2026-06-20",
        disputed_zones=3,
    ),
    # ENT-004 — Norway Arctic Council → composite ~53 (élevé), stabilite_arctique
    ArcticEntity(
        entity_id="ENT-004",
        name="Norway Arctic Council",
        country="Norvège",
        sector="Diplomatie & Gouvernance",
        territorial_score=58.0,
        military_score=55.0,
        resource_score=50.0,
        climate_score=48.0,
        key_signals=[
            "Présidence du Conseil Arctique — coordination diplomatique renforcée",
            "Tensions avec la Russie sur les droits de pêche en mer de Barents",
            "Développement des ressources pétrolières offshore en mer de Barents",
        ],
        last_updated="2026-06-20",
        disputed_zones=2,
    ),
    # ENT-005 — Canada Arctic Patrol → composite ~47 (élevé), stabilite_arctique
    ArcticEntity(
        entity_id="ENT-005",
        name="Canada Arctic Patrol",
        country="Canada",
        sector="Surveillance Territoriale",
        territorial_score=52.0,
        military_score=48.0,
        resource_score=45.0,
        climate_score=42.0,
        key_signals=[
            "Dispute sur le passage du Nord-Ouest avec les États-Unis",
            "Renforcement de la souveraineté canadienne dans l'archipel arctique",
            "Exploitation des ressources minières dans les territoires nordiques",
        ],
        last_updated="2026-06-20",
        disputed_zones=2,
    ),
    # ENT-006 — Finland Arctic Strategy → composite ~32 (modéré), stabilite_arctique
    ArcticEntity(
        entity_id="ENT-006",
        name="Finland Arctic Strategy",
        country="Finlande",
        sector="Politique Environnementale",
        territorial_score=35.0,
        military_score=30.0,
        resource_score=32.0,
        climate_score=30.0,
        key_signals=[
            "Stratégie nationale arctique centrée sur le développement durable",
            "Coopération environnementale avec les pays nordiques renforcée",
            "Surveillance des impacts climatiques sur les écosystèmes polaires",
        ],
        last_updated="2026-06-20",
        disputed_zones=1,
    ),
    # ENT-007 — Denmark Greenland Authority → composite ~16 (faible), stabilite_arctique
    ArcticEntity(
        entity_id="ENT-007",
        name="Denmark Greenland Authority",
        country="Danemark",
        sector="Administration Territoriale",
        territorial_score=18.0,
        military_score=15.0,
        resource_score=16.0,
        climate_score=14.0,
        key_signals=[
            "Autonomie croissante du Groenland — négociations constitutionnelles en cours",
            "Exploitation minière limitée pour préserver l'environnement arctique",
            "Coopération scientifique internationale sur le changement climatique",
        ],
        last_updated="2026-06-20",
        disputed_zones=1,
    ),
    # ENT-008 — Iceland Research Station → composite ~9 (faible), stabilite_arctique
    ArcticEntity(
        entity_id="ENT-008",
        name="Iceland Research Station",
        country="Islande",
        sector="Recherche Polaire",
        territorial_score=10.0,
        military_score=8.0,
        resource_score=9.0,
        climate_score=8.0,
        key_signals=[
            "Recherche polaire internationale sur les variations climatiques arctiques",
            "Station d'observation des aurores boréales et phénomènes géophysiques",
            "Coopération scientifique pacifique avec les États arctiques riverains",
        ],
        last_updated="2026-06-20",
        disputed_zones=0,
    ),
]


class ArcticEngine:
    domain: str = DOMAIN

    def analyze(self) -> list[dict[str, typing.Any]]:
        return [e.to_dict() for e in MOCK_ENTITIES]

    def summary(self) -> dict[str, typing.Any]:
        entities = self.analyze()

        risk_distribution: dict[str, int] = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
        pattern_distribution: dict[str, int] = {name: 0 for name in PATTERN_NAMES}
        total_composite = 0.0
        top_risk_entities: list[tuple[float, str]] = []
        critical_alerts: list[str] = []

        for ent in entities:
            rl = ent["risk_level"]
            if rl in risk_distribution:
                risk_distribution[rl] += 1
            pp = ent["primary_pattern"]
            if pp in pattern_distribution:
                pattern_distribution[pp] += 1
            total_composite += ent["composite_score"]
            top_risk_entities.append((ent["composite_score"], ent["name"]))
            if rl == "critique":
                critical_alerts.append(
                    f"ALERTE CRITIQUE — {ent['name']} ({ent['country']}) : score composite {ent['composite_score']:.1f}/100"
                )

        n = len(entities) or 1
        avg_composite = round(total_composite / n, 2)
        top_risk_entities.sort(key=lambda x: x[0], reverse=True)
        top_3_names = [name for _, name in top_risk_entities[:3]]

        return {
            "total_entities": len(entities),
            "avg_composite": avg_composite,
            "risk_distribution": risk_distribution,
            "pattern_distribution": pattern_distribution,
            "top_risk_entities": top_3_names,
            "critical_alerts": critical_alerts,
            "last_analysis": "2026-06-20",
            "engine_version": "1.0.0",
            "domain": DOMAIN,
            "confidence_score": 0.88,
            "data_sources": [
                "arctic_council_reports",
                "satellite_surveillance",
                "geopolitical_risk_db",
            ],
            "entities": entities,
            "avg_estimated_arctic_index": round(avg_composite / 100 * 10, 2),
        }


def analyze_arctic() -> dict[str, typing.Any]:
    engine = ArcticEngine()
    return engine.summary()
