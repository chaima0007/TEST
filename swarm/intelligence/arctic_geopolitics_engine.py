"""
Caelum Partners — Arctic Geopolitics Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
L'Arctique comme nouveau théâtre de la compétition géopolitique mondiale :
la fonte des glaces ouvre des routes maritimes inédites, expose des réserves
colossales d'hydrocarbures et de minéraux critiques, et transforme une région
longtemps coopérative en zone de rivalité militaire croissante.

La Russie a réarmé l'Arctique à une vitesse vertigineuse : 6 bases militaires
arctiques rénovées depuis 2013, missiles S-400 déployés en Arctique, navires
de guerre nucléaires en patrouille, revendication d'un plateau continental
étendu contesté par le Canada et le Danemark. La Chine s'autoproclaime
"nation quasi-arctique" malgré l'absence de territoire polaire — elle investit
dans des brise-glaces de recherche, signe des accords miniers au Groenland
et cherche à contrôler la Route Polaire Maritime Arctique (RPMA). Les États-
Unis ont créé la US Arctic Strategy 2022, investissent dans des brise-glaces
polaires (Coast Guard), et maintiennent une présence via l'Alaska et le NORAD.
Le Canada revendique le Passage du Nord-Ouest comme eaux intérieures — contesté
par les USA qui le considèrent comme détroit international.

Le Groenland est devenu l'enjeu arctique par excellence : 80% de glace, des
gisements de terres rares et d'uranium, et une population autochtone inuit
tiraillée entre indépendance et géopolitique. Donald Trump a proposé de
l'acheter en 2019 — révélant les appétits stratégiques américains.

Risk levels (militarisation et conflictualité arctique) :
  critique  → composite ≥ 60  (puissance militaire arctique active — revendications et déploiements)
  élevé     → composite ≥ 40  (positionnement stratégique — course aux ressources et aux routes)
  modéré    → composite ≥ 20  (intégration arctique OTAN — capacités défensives émergentes)
  faible    → composite < 20  (coopération scientifique arctique — présence non-militaire)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "militarisation_arctique_active": {
        "severity_fr": "Critique",
        "action_fr": "Traité arctique de désescalade militaire et mécanismes de déconfliction dans les zones de revendications superposées",
        "signal_fr": "territorial_sovereignty_dispute_score > 80 AND military_buildup_score > 80 — militarisation arctique active et conflictuelle",
    },
    "course_ressources_arctiques": {
        "severity_fr": "Critique",
        "action_fr": "Régulation internationale de l'exploitation arctique et droits des peuples autochtones dans les décisions minières",
        "signal_fr": "Course aux ressources arctiques — extraction accélérée d'hydrocarbures et terres rares dans zones disputées",
    },
    "positionnement_strategique_arctique": {
        "severity_fr": "Élevé",
        "action_fr": "Renforcement du Conseil Arctique et normes de comportement responsable pour les États non-arctiques",
        "signal_fr": "Positionnement stratégique arctique — investissements en capacités polaires sans conflictualité ouverte",
    },
    "integration_otan_arctique": {
        "severity_fr": "Modéré",
        "action_fr": "Coordination OTAN arctique et capacités défensives collectives pour contrer la militarisation russe",
        "signal_fr": "Intégration OTAN arctique — renforcement défensif dans un contexte de montée des tensions polaires",
    },
    "cooperation_polaire": {
        "severity_fr": "Faible",
        "action_fr": "Renforcer la coopération scientifique arctique et les traités de protection de l'environnement polaire",
        "signal_fr": "composite_score < 20 — coopération polaire scientifique et engagement non-militaire en Arctique",
    },
}


@dataclass
class ArcticGeopoliticsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    territorial_sovereignty_dispute_score: float
    military_buildup_score: float
    resource_extraction_rush_score: float
    arctic_route_control_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_arctic_tension_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.territorial_sovereignty_dispute_score * 0.30
            + self.military_buildup_score * 0.25
            + self.resource_extraction_rush_score * 0.25
            + self.arctic_route_control_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_arctic_tension_index = round(self.composite_score / 100 * 10, 2)

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
        if self.territorial_sovereignty_dispute_score >= 80 and self.military_buildup_score >= 80:
            return "militarisation_arctique_active"
        if self.resource_extraction_rush_score >= 75:
            return "course_ressources_arctiques"
        if self.composite_score >= 40:
            return "positionnement_strategique_arctique"
        if self.composite_score >= 20:
            return "integration_otan_arctique"
        return "cooperation_polaire"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Militarisation arctique critique impliquant {n} — déploiements militaires et revendications souveraines conflictuelles",
                "Course aux ressources polaires — extraction accélérée d'hydrocarbures et terres rares sous la glace fondante",
                "Contrôle des routes maritimes arctiques — enjeu stratégique de la Route du Nord-Est et du Passage du Nord-Ouest",
            ]
        if self.risk_level == "élevé":
            return [
                f"Positionnement stratégique arctique de {n} — investissements capacitaires polaires sans conflit ouvert",
                "Infrastructure polaire duale — brise-glaces, bases et réseaux de surveillance à double usage civil-militaire",
                "Diplomatie arctique active — négociations sur les plateaux continentaux, ressources et droits de passage",
            ]
        if self.risk_level == "modéré":
            return [
                f"Intégration arctique OTAN pour {n} — renforcement défensif face à la militarisation russe et chinoise",
                "Capacités polaires en développement — acquisition de brise-glaces et stations de surveillance nordiques",
                "Participation au Conseil Arctique — engagement diplomatique pour préserver la coopération scientifique",
            ]
        return [
            f"{n} maintient une présence arctique coopérative et scientifique — engagement non-militaire et transparent",
            "Respect du Traité de Svalbard et des conventions internationales polaires — multilateralisme arctique",
            "Modèle de coopération polaire scientifique — partage des données climatiques et environnementales arctiques",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "territorial_sovereignty_dispute_score": self.territorial_sovereignty_dispute_score,
            "military_buildup_score": self.military_buildup_score,
            "resource_extraction_rush_score": self.resource_extraction_rush_score,
            "arctic_route_control_score": self.arctic_route_control_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_arctic_tension_index": self.estimated_arctic_tension_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[ArcticGeopoliticsEntity] = [
    ArcticGeopoliticsEntity("AG-001", "Russie — Remilitarisation Arctique & Route du Nord-Est", "Europe de l'Est/Arctique", "6 Bases Arctiques, S-400 Polaires, RPMA & Revendications Plateau Continental", 92.0, 90.0, 85.0, 88.0),
    ArcticGeopoliticsEntity("AG-002", "Chine — Puissance Quasi-Arctique Auto-Proclamée", "Asie", "Brise-Glaces Xuelong, Mines Groenland & Route Polaire Maritime Arctique", 78.0, 72.0, 80.0, 75.0),
    ArcticGeopoliticsEntity("AG-003", "USA — Alaska, Space Force & Arctic Strategy", "Amérique du Nord", "Fort Greely, NORAD Modernisé & Stratégie Arctique Pentagon 2022", 75.0, 80.0, 72.0, 70.0),
    ArcticGeopoliticsEntity("AG-004", "Canada — Passage du Nord-Ouest Souverain Contesté", "Amériques", "Revendication Eaux Intérieures vs USA + Rangers Canadiens & Bases Nordiques", 65.0, 58.0, 70.0, 68.0),
    ArcticGeopoliticsEntity("AG-005", "Norvège — OTAN Arctique & Svalbard sous Pression Russe", "Europe du Nord", "Svalbard Militarisé, Frigates F310 & Surveillance Sous-Marine Arctique", 52.0, 58.0, 48.0, 55.0),
    ArcticGeopoliticsEntity("AG-006", "Danemark/Groenland — Terres Rares & Indépendance Arctique", "Europe du Nord", "Terres Rares Groenlandaises Convoitées — Uranium & Néodyme sous les Glaces", 55.0, 48.0, 52.0, 50.0),
    ArcticGeopoliticsEntity("AG-007", "Finlande & Suède — OTAN Arctique Nouveau", "Europe du Nord", "Adhésion OTAN 2023-2024 & Capacités Défensives Arctiques Nordiques", 32.0, 35.0, 28.0, 30.0),
    ArcticGeopoliticsEntity("AG-008", "Coopération Polaire ISA — Science sans Armes", "Global", "Programme MOSAIC & Accords Scientifiques Polaires — Recherche Coopérative", 5.0, 4.0, 8.0, 6.0),
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
        "domain": "arctic_geopolitics",
        "confidence_score": 0.82,
        "data_sources": ["arctic_council_monitoring_network", "sipri_arctic_military_database", "nsidc_sea_ice_change_tracker"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_arctic_tension_index": round(avg / 100 * 10, 2),
    }


def analyze_arctic_geopolitics() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Arctic Geopolitics Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")
