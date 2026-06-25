"""Caelum Partners — Algae Energy Intelligence Engine
Propriété exclusive de Chaima Mhadbi, Fondatrice Caelum Partners, Bruxelles.
"""
from __future__ import annotations

import logging
import dataclasses
import typing
from typing import Any

logger = logging.getLogger("swarm.algae")

DOMAIN = "algae"

PATTERNS: list[dict[str, str]] = [
    {
        "key": "rendement_critique",
        "name": "rendement_critique",
        "severity_fr": "Rendement algal critique",
        "action_fr": "Optimisation immédiate des bioreacteurs requise",
        "signal_fr": "Rendement de production algale dépasse le seuil critique",
    },
    {
        "key": "durabilite_compromise",
        "name": "durabilite_compromise",
        "severity_fr": "Durabilité environnementale compromise",
        "action_fr": "Audit environnemental et réduction des intrants chimiques",
        "signal_fr": "Score de durabilité critique — impact environnemental élevé détecté",
    },
    {
        "key": "echelle_bloquee",
        "name": "echelle_bloquee",
        "severity_fr": "Scalabilité industrielle bloquée",
        "action_fr": "Révision du plan d'expansion et des capacités infrastructurelles",
        "signal_fr": "Obstacles majeurs à la montée en échelle des installations algales",
    },
    {
        "key": "efficience_degradee",
        "name": "efficience_degradee",
        "severity_fr": "Efficience opérationnelle dégradée",
        "action_fr": "Optimisation des processus et réduction des pertes énergétiques",
        "signal_fr": "Efficience de conversion énergétique en dessous des standards",
    },
    {
        "key": "systeme_algal_stable",
        "name": "systeme_algal_stable",
        "severity_fr": "Système algal stable",
        "action_fr": "Maintien des pratiques actuelles et veille technologique",
        "signal_fr": "Système de production algale opérationnel dans les paramètres normaux",
    },
]


def _get_pattern(
    productivity_score: float,
    sustainability_score: float,
    scalability_score: float,
    efficiency_score: float,
) -> dict[str, str]:
    if productivity_score >= 70:
        return PATTERNS[0]
    if sustainability_score >= 70:
        return PATTERNS[1]
    if scalability_score >= 70:
        return PATTERNS[2]
    if efficiency_score >= 70:
        return PATTERNS[3]
    return PATTERNS[4]


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critique"
    if composite >= 40:
        return "élevé"
    if composite >= 20:
        return "modéré"
    return "faible"


def _composite_score(
    productivity: float,
    sustainability: float,
    scalability: float,
    efficiency: float,
) -> float:
    return round(
        productivity * 0.30 + sustainability * 0.25 + scalability * 0.25 + efficiency * 0.20,
        2,
    )


@dataclasses.dataclass
class AlgaeEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    productivity_score: float
    sustainability_score: float
    scalability_score: float
    efficiency_score: float
    facility_count: int

    def to_dict(self) -> dict[str, Any]:
        composite = _composite_score(
            self.productivity_score,
            self.sustainability_score,
            self.scalability_score,
            self.efficiency_score,
        )
        risk = _risk_level(composite)
        pattern = _get_pattern(
            self.productivity_score,
            self.sustainability_score,
            self.scalability_score,
            self.efficiency_score,
        )
        estimated_algae_index = round(composite / 100 * 10, 2)

        if risk == "critique":
            key_signals = [
                f"Niveau de risque critique détecté pour {self.name}",
                "Production algale en surcharge — intervention urgente recommandée",
                "Indicateurs d'alerte rouge : rendement et durabilité compromis",
            ]
        elif risk == "élevé":
            key_signals = [
                f"Risque élevé identifié dans les opérations de {self.name}",
                "Surveillance renforcée des paramètres de croissance algale requise",
                "Tendances défavorables détectées sur plusieurs indicateurs clés",
            ]
        elif risk == "modéré":
            key_signals = [
                f"Risque modéré pour {self.name} — suivi régulier recommandé",
                "Performance algale acceptable avec marges d'amélioration identifiées",
                "Optimisation progressive des processus de bioénergie en cours",
            ]
        else:
            key_signals = [
                f"{self.name} affiche une performance algale satisfaisante",
                "Indicateurs de production et durabilité dans les normes",
                "Système algal opérationnel — veille technologique maintenue",
            ]

        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": composite,
            "productivity_score": self.productivity_score,
            "sustainability_score": self.sustainability_score,
            "scalability_score": self.scalability_score,
            "efficiency_score": self.efficiency_score,
            "risk_level": risk,
            "primary_pattern": pattern["name"],
            "key_signals": key_signals,
            "estimated_algae_index": estimated_algae_index,
            "last_updated": "2026-06-20",
            "facility_count": self.facility_count,
        }


MOCK_ENTITIES: list[AlgaeEntity] = [
    # ENT-001: critique — productivity>=70 → rendement_critique
    AlgaeEntity(
        entity_id="ENT-001",
        name="SolarAlgae Industries",
        country="États-Unis",
        sector="Bioénergie",
        productivity_score=82.0,
        sustainability_score=68.0,
        scalability_score=65.0,
        efficiency_score=60.0,
        facility_count=12,
    ),
    # ENT-002: critique — sustainability>=70 → durabilite_compromise
    AlgaeEntity(
        entity_id="ENT-002",
        name="BioPetro Algae",
        country="Brésil",
        sector="Pétrochimie Verte",
        productivity_score=68.0,
        sustainability_score=75.0,
        scalability_score=60.0,
        efficiency_score=52.0,
        facility_count=8,
    ),
    # ENT-003: critique — scalability>=70 → echelle_bloquee
    AlgaeEntity(
        entity_id="ENT-003",
        name="AlgaFuel Nordic",
        country="Norvège",
        sector="Carburants Alternatifs",
        productivity_score=65.0,
        sustainability_score=62.0,
        scalability_score=72.0,
        efficiency_score=42.0,
        facility_count=5,
    ),
    # ENT-004: élevé — no sub-score >= 70 → systeme_algal_stable
    AlgaeEntity(
        entity_id="ENT-004",
        name="Spirulina Power SA",
        country="France",
        sector="Nutraceutique & Énergie",
        productivity_score=58.0,
        sustainability_score=52.0,
        scalability_score=50.0,
        efficiency_score=42.0,
        facility_count=3,
    ),
    # ENT-005: élevé — no sub-score >= 70 → systeme_algal_stable
    AlgaeEntity(
        entity_id="ENT-005",
        name="MicroBloom Tech",
        country="Australie",
        sector="Biotechnologie Marine",
        productivity_score=50.0,
        sustainability_score=46.0,
        scalability_score=42.0,
        efficiency_score=35.0,
        facility_count=7,
    ),
    # ENT-006: modéré — no sub-score >= 70 → systeme_algal_stable
    AlgaeEntity(
        entity_id="ENT-006",
        name="Chlorella Energy GmbH",
        country="Allemagne",
        sector="Énergie Renouvelable",
        productivity_score=30.0,
        sustainability_score=28.0,
        scalability_score=26.0,
        efficiency_score=22.0,
        facility_count=2,
    ),
    # ENT-007: faible — systeme_algal_stable
    AlgaeEntity(
        entity_id="ENT-007",
        name="AquaGreen Labs",
        country="Pays-Bas",
        sector="Recherche Appliquée",
        productivity_score=15.0,
        sustainability_score=14.0,
        scalability_score=12.0,
        efficiency_score=10.0,
        facility_count=1,
    ),
    # ENT-008: faible — systeme_algal_stable
    AlgaeEntity(
        entity_id="ENT-008",
        name="BlueTide Bioenergy",
        country="Danemark",
        sector="Énergie Côtière",
        productivity_score=8.0,
        sustainability_score=7.0,
        scalability_score=6.0,
        efficiency_score=6.0,
        facility_count=1,
    ),
]


class AlgaeEngine:
    domain: str = DOMAIN

    def analyze(self) -> list[dict[str, Any]]:
        logger.debug("AlgaeEngine.analyze() — %d entities", len(MOCK_ENTITIES))
        return [entity.to_dict() for entity in MOCK_ENTITIES]

    def summary(self) -> dict[str, Any]:
        entities = self.analyze()

        risk_distribution: dict[str, int] = {
            "critique": 0,
            "élevé": 0,
            "modéré": 0,
            "faible": 0,
        }
        pattern_distribution: dict[str, int] = {
            "rendement_critique": 0,
            "durabilite_compromise": 0,
            "echelle_bloquee": 0,
            "efficience_degradee": 0,
            "systeme_algal_stable": 0,
        }
        critical_alerts: list[str] = []
        total_composite = 0.0
        top_risk: list[tuple[float, str]] = []

        for e in entities:
            risk = e["risk_level"]
            risk_distribution[risk] = risk_distribution.get(risk, 0) + 1
            pattern = e["primary_pattern"]
            pattern_distribution[pattern] = pattern_distribution.get(pattern, 0) + 1
            total_composite += e["composite_score"]
            top_risk.append((e["composite_score"], e["name"]))

            if risk == "critique":
                critical_alerts.append(
                    f"{e['name']}: {e['primary_pattern'].replace('_', ' ')}"
                )

        n = len(entities) or 1
        avg_composite = round(total_composite / n, 2)

        top_risk.sort(key=lambda x: x[0], reverse=True)
        top_risk_entities = [name for _, name in top_risk[:3]]

        avg_estimated_algae_index = round(avg_composite / 100 * 10, 2)

        logger.info(
            "AlgaeEngine summary — avg_composite=%.2f risk_dist=%s",
            avg_composite,
            risk_distribution,
        )

        return {
            "total_entities": len(entities),
            "avg_composite": avg_composite,
            "risk_distribution": risk_distribution,
            "pattern_distribution": pattern_distribution,
            "top_risk_entities": top_risk_entities,
            "critical_alerts": critical_alerts,
            "last_analysis": "2026-06-20",
            "engine_version": "1.0.0",
            "domain": DOMAIN,
            "confidence_score": 0.85,
            "data_sources": [
                "bioreactor_sensors",
                "carbon_capture_data",
                "biomass_yield_reports",
            ],
            "entities": entities,
            "avg_estimated_algae_index": avg_estimated_algae_index,
        }


def analyze_algae() -> dict[str, Any]:
    engine = AlgaeEngine()
    return engine.summary()
