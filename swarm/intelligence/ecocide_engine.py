"""
Caelum Partners — Ecocide Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Écocide : la destruction délibérée des écosystèmes comme crime international.
L'écocide — terme popularisé par le juriste Polly Higgins — désigne la destruction
massive ou durable d'un écosystème par des activités humaines délibérées. Le
Parlement européen a adopté en 2021 une résolution appelant à la reconnaissance
de l'écocide comme cinquième crime devant la Cour Pénale Internationale, aux côtés
du génocide, des crimes contre l'humanité, des crimes de guerre et de l'agression.

La déforestation de l'Amazonie brésilienne représente l'écocide le plus visible
du XXIe siècle : sous Bolsonaro (2019-2022), le taux de déforestation a atteint
des records avec 11 088 km² détruits en 2019. Des incendies criminels sont
délibérément allumés pour "nettoyer" les terres indigènes en vue de l'agriculture
intensive. La disparition de la forêt amazonienne menace le "point de bascule"
climatique au-delà duquel la forêt se transformerait en savane.

En Chine, la pollution industrielle délibérée de rivières et de nappes phréatiques
a créé des "villages du cancer" (cancer villages) — terme officiellement reconnu
en 2013 par le gouvernement lui-même. Les déchets toxiques sont régulièrement
déversés illégalement dans des zones protégées. En Russie, les incendies de
Sibérie s'intensifient chaque année, alimentés par des acteurs industriels qui
brûlent délibérément des terres pour y développer des activités extractives.

Risk levels (écocide et destruction délibérée des écosystèmes) :
  critique  -> composite >= 60  (écocide systémique — destruction délibérée massive d'écosystèmes)
  élevé     -> composite >= 40  (dégradation active — pollution industrielle et déforestation non maîtrisées)
  modéré    -> composite >= 20  (risque environnemental — impacts documentés sans destruction systémique)
  faible    -> composite < 20   (protection écosystémique exemplaire — normes environnementales effectives)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "ecocide_delibere_industriel": {
        "severity_fr": "Critique",
        "action_fr": "Criminalisation CPI écocide — cinquième crime international, poursuites des dirigeants d'entreprises responsables et fonds de restauration écologique financé par les pollueurs",
        "signal_fr": "deliberate_ecosystem_destruction_score > 85 AND deforestation_carbon_arson_score > 85 — écocide délibéré combinant destruction systématique des écosystèmes et incendies criminels de masse",
    },
    "contamination_toxique_systematique": {
        "severity_fr": "Critique",
        "action_fr": "Tribunal international pollution — responsabilité civile et pénale des pollueurs transfrontaliers, fonds de décontamination obligatoire et interdiction d'exportation des polluants",
        "signal_fr": "toxic_contamination_weaponization_score > 85 — contamination toxique systématique de l'eau, des sols et de l'air avec connaissance des conséquences sur les populations et la biodiversité",
    },
    "deforestation_criminelle": {
        "severity_fr": "Critique",
        "action_fr": "Traçabilité des chaînes d'approvisionnement — due diligence obligatoire sur les produits de déforestation, sanctions aux importateurs complices et mécanisme de compensation carbone forestier",
        "signal_fr": "deforestation_carbon_arson_score > 85 — déforestation criminelle systématique via incendies délibérés, abattage illégal massif et destruction de forêts primaires pour l'agriculture intensive",
    },
    "degradation_ecosysteme_active": {
        "severity_fr": "Élevé",
        "action_fr": "Mécanismes REDD+ renforcés — paiements pour services écosystémiques, audit environnemental indépendant et conditionnalité verte des financements publics et privés",
        "signal_fr": "Dégradation écosystémique active — destruction progressive sans franchir le seuil de l'écocide délibéré mais avec des impacts irréversibles sur la biodiversité et le climat",
    },
    "protection_ecosystemique_exemplaire": {
        "severity_fr": "Faible",
        "action_fr": "Exporter les standards de protection — financement PNUE, partage des meilleures pratiques réglementaires et aide aux États vulnérables pour leurs politiques environnementales",
        "signal_fr": "composite_score < 20 — protection écosystémique effective: réserves naturelles fonctionnelles, standards d'émissions respectés et gouvernance environnementale indépendante",
    },
}


@dataclass
class EcocideEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    deliberate_ecosystem_destruction_score: float
    toxic_contamination_weaponization_score: float
    deforestation_carbon_arson_score: float
    biodiversity_collapse_acceleration_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_ecocide_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.deliberate_ecosystem_destruction_score * 0.30
            + self.toxic_contamination_weaponization_score * 0.25
            + self.deforestation_carbon_arson_score * 0.25
            + self.biodiversity_collapse_acceleration_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_ecocide_index = round(self.composite_score / 100 * 10, 2)

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
        if self.deliberate_ecosystem_destruction_score >= 85 and self.deforestation_carbon_arson_score >= 85:
            return "ecocide_delibere_industriel"
        if self.toxic_contamination_weaponization_score >= 85:
            return "contamination_toxique_systematique"
        if self.deforestation_carbon_arson_score >= 85:
            return "deforestation_criminelle"
        if self.composite_score >= 20:
            return "degradation_ecosysteme_active"
        return "protection_ecosystemique_exemplaire"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Écocide critique de {n} — destruction délibérée et massive d'écosystèmes avec connaissance des conséquences irréversibles sur la biodiversité et les communautés dépendantes",
                "Crime environnemental international — la destruction systématique d'écosystèmes primaires constitue un préjudice à l'humanité et à la biosphère justifiant des poursuites au CPI",
                "Tipping points climatiques menacés — la destruction des puits de carbone naturels accélère le changement climatique et risque de déclencher des boucles de rétroaction irréversibles",
            ]
        if self.risk_level == "élevé":
            return [
                f"Dégradation écosystémique active de {n} — pollution industrielle et déforestation non maîtrisées causant des dommages documentés à la biodiversité et aux populations locales",
                "Impunité environnementale — l'absence de sanctions effectives contre les pollueurs et déforesteurs crée un avantage concurrentiel déloyale pour les acteurs les moins scrupuleux",
                "Communautés indigènes en danger — la destruction des écosystèmes prive les peuples autochtones de leurs moyens de subsistance, de leur culture et de leurs droits territoriaux",
            ]
        if self.risk_level == "modéré":
            return [
                f"Risque environnemental documenté de {n} — impacts sur les écosystèmes sans franchir le seuil de la destruction systémique ou délibérée des ressources naturelles",
                "Réglementation insuffisante — les normes environnementales existantes ne sont pas appliquées suffisamment pour prévenir la dégradation progressive des habitats naturels",
                "Risque de régression — la pression économique et le recul des politiques environnementales pourraient intensifier les impacts sur la biodiversité",
            ]
        return [
            f"{n} incarne la protection écosystémique exemplaire — réserves naturelles fonctionnelles, standards d'émissions respectés et gouvernance environnementale indépendante",
            "Biodiversité protégée — mécanismes de conservation fonctionnels, corridors écologiques maintenus et espèces menacées effectivement protégées",
            "Modèle environnemental à exporter — financement PNUE, coopération internationale sur la conservation et aide technique aux États vulnérables",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "deliberate_ecosystem_destruction_score": self.deliberate_ecosystem_destruction_score,
            "toxic_contamination_weaponization_score": self.toxic_contamination_weaponization_score,
            "deforestation_carbon_arson_score": self.deforestation_carbon_arson_score,
            "biodiversity_collapse_acceleration_score": self.biodiversity_collapse_acceleration_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_ecocide_index": self.estimated_ecocide_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[EcocideEntity] = [
    EcocideEntity("EC-001", "Brésil/Amazonie — 11 000 km² Déforestés/An & Incendies Criminels", "Amérique du Sud", "Bolsonaro 11 088 km2 2019, Incendies Criminels INPE, Terres Indigènes Envahies & Garimpo Mercure Yanomami", 92.0, 75.0, 95.0, 85.0),
    EcocideEntity("EC-002", "Chine/Industrie — Villages Cancer, Rivières Polluées & Smog Délibéré", "Asie", "Villages Cancer Officiels 2013, Rivières Polluées Métaux Lourds, Déchets Toxiques Export & Nappes Phréatiques", 85.0, 92.0, 72.0, 82.0),
    EcocideEntity("EC-003", "Russie/Sibérie — Incendies Industriels & Permafrost Exploitation", "Europe de l'Est", "Incendies Sibérie Records, Pétrole Norilsk Déversements, Permafrost Exploitation Méthane & Lac Baïkal Pollution", 78.0, 82.0, 88.0, 75.0),
    EcocideEntity("EC-004", "Indonésie/Bornéo — Palmiers Huile, Orangs-Outans & Tourbières Brûlées", "Asie du Sud-Est", "Tourbières Brûlées CO2, Palme Huile Déforestation Massive, Orangs-Outans Extinction & Haze Transfrontalier", 80.0, 72.0, 82.0, 88.0),
    EcocideEntity("EC-005", "Nigeria/Delta Niger — Shell-Esso Déversements 50 Ans & Communautés Empoisonnées", "Afrique de l'Ouest", "50 Ans Déversements Pétroliers, 11M Barils Déversés Ogoniland, PNUE Rapport 2011 & Impunité Totale", 55.0, 72.0, 48.0, 62.0),
    EcocideEntity("EC-006", "Canada/Sables Bitumineux — Athabasca, Tailings Ponds & Cancers Autochtones", "Amérique du Nord", "Sables Bitumineux 142 000 km2, Étangs Résidus Toxiques, Rivière Athabasca Contaminée & Nations Premières", 52.0, 58.0, 48.0, 55.0),
    EcocideEntity("EC-007", "Australie/Grande Barrière & Espèces Menacées Politiques Charbon", "Océanie", "Grande Barrière 50% Coraux Morts, Gouvernement Pro-Charbon, Kangourous Abattages & Koalas Menacés", 28.0, 25.0, 32.0, 35.0),
    EcocideEntity("EC-008", "PNUE/Accord Paris — Protection Environnementale Internationale", "Global", "PNUE 193 États, Accord Paris 196 Parties, Convention Biodiversité CBD & Cadre Kunming-Montréal 30x30", 5.0, 4.0, 3.0, 6.0),
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
        "domain": "ecocide",
        "confidence_score": 0.81,
        "data_sources": ["pnue_global_environment_outlook", "global_witness_deforestation_monitor", "iucn_red_list_threatened_species"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_ecocide_index": round(avg / 100 * 10, 2),
    }


def analyze_ecocide() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Ecocide Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} -> {e.risk_level} ({e.composite_score})")
