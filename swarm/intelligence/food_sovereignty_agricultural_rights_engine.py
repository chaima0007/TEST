"""
Caelum Partners — Food Sovereignty Agricultural Rights Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Accaparement des terres, monopoles semenciers et dépendance alimentaire systémique.

La souveraineté alimentaire — le droit des peuples à définir leur propre système
alimentaire et agricole — est garantie par l'article 11 du PIDESC. Or, l'accaparement
des terres à grande échelle, le monopole des semences par les corporations et la
dépendance aux importations alimentaires violent ce droit fondamental de centaines de
millions de personnes à travers le monde.

L'Inde a connu plus de 300.000 suicides d'agriculteurs entre 1995 et 2022, largement
liés à la dépendance aux semences OGM Bt Cotton de Monsanto/Bayer et aux cycles de
dettes insurmontables. La FAO estime que 80% des terres accaparées depuis 2000 se
situent dans des pays où la faim est endémique. Monsanto/Bayer contrôle 28% du marché
mondial des semences, tandis que la concentration au sein des 4 plus grands opérateurs
(BASF, Bayer, ChemChina-Syngenta, Corteva) dépasse 60% du marché.

Risk levels (souveraineté alimentaire et droits agricoles) :
  critique  -> composite >= 60  (dépendance totale — accaparement massif et monopole corporatif)
  élevé     -> composite >= 40  (vulnérabilité structurelle — dépendances économiques profondes)
  modéré    -> composite >= 20  (risques gérables — pressions avec solutions partielles)
  faible    -> composite < 20   (souveraineté exemplaire — système alimentaire diversifié et résilient)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "accaparement_terres_deplacementpaysans": {
        "severity_fr": "Critique",
        "action_fr": "Réforme agraire urgente — moratoire sur les acquisitions de terres à grande échelle, restitution des terres accaparées illégalement et renforcement des titres fonciers communautaires des populations paysannes et autochtones",
        "signal_fr": "land_grabbing_smallholder_displacement_score > 85 — acquisition massive de terres agricoles par des acteurs étrangers ou corporatifs déplaçant des millions de paysans sans compensation ni alternative",
    },
    "monopole_semences_dependance_corporative": {
        "severity_fr": "Critique",
        "action_fr": "Réglementation antitrust semencière — démantèlement des monopoles corporatifs, protection des semences paysannes traditionnelles, financement des banques de semences communautaires et interdiction des brevets sur le vivant",
        "signal_fr": "corporate_seed_monopoly_farmer_dependency_score > 85 — dépendance quasi-totale aux semences propriétaires de grandes corporations créant des cycles de dette insurmontables pour les agriculteurs",
    },
    "dependance_alimentaire_chocs_prix": {
        "severity_fr": "Élevé",
        "action_fr": "Souveraineté alimentaire structurelle — diversification de la production locale, stocks stratégiques de sécurité alimentaire, protection douanière des marchés agricoles locaux et réduction de la dépendance aux marchés spéculatifs",
        "signal_fr": "food_import_dependency_price_shock_vulnerability_score > 70 — dépendance aux importations alimentaires exposant la population à des crises alimentaires lors des chocs de prix internationaux",
    },
    "erosion_savoirs_traditionnels": {
        "severity_fr": "Élevé",
        "action_fr": "Protection des savoirs agricoles — documentation et protection légale des semences et pratiques agricoles traditionnelles, financement de la recherche agroécologique et création de centres de préservation des savoirs paysans",
        "signal_fr": "traditional_farming_knowledge_erosion_score > 70 — perte accélérée des variétés semencières locales et des pratiques agricoles traditionnelles sous la pression de l'agro-industrie",
    },
    "souverainete_alimentaire_exemplaire": {
        "severity_fr": "Faible",
        "action_fr": "Diffuser le modèle — partager les politiques de souveraineté alimentaire réussies, financer Via Campesina et les mouvements paysans internationaux, soutenir les standards FAO de protection des droits des agriculteurs",
        "signal_fr": "composite_score < 20 — système alimentaire diversifié, semences paysannes protégées, terres agricoles sécurisées et accès aux marchés locaux garanti",
    },
}


@dataclass
class FoodSovereigntyAgriculturalRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    land_grabbing_smallholder_displacement_score: float
    corporate_seed_monopoly_farmer_dependency_score: float
    food_import_dependency_price_shock_vulnerability_score: float
    traditional_farming_knowledge_erosion_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_food_sovereignty_agricultural_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.land_grabbing_smallholder_displacement_score * 0.30
            + self.corporate_seed_monopoly_farmer_dependency_score * 0.25
            + self.food_import_dependency_price_shock_vulnerability_score * 0.25
            + self.traditional_farming_knowledge_erosion_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_food_sovereignty_agricultural_rights_index = round(self.composite_score / 100 * 10, 2)

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
        if self.land_grabbing_smallholder_displacement_score >= 85:
            return "accaparement_terres_deplacementpaysans"
        if self.corporate_seed_monopoly_farmer_dependency_score >= 85:
            return "monopole_semences_dependance_corporative"
        if self.food_import_dependency_price_shock_vulnerability_score >= 70:
            return "dependance_alimentaire_chocs_prix"
        if self.composite_score >= 20:
            return "erosion_savoirs_traditionnels"
        return "souverainete_alimentaire_exemplaire"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Crise agricole critique de {n} — accaparement des terres et/ou monopole semencier créant des conditions de dépendance et de vulnérabilité alimentaire systémique pour des millions d'agriculteurs",
                "Violation du droit à l'alimentation — l'article 11 du PIDESC est directement menacé par la concentration corporative des ressources agricoles et l'élimination des systèmes alimentaires paysans traditionnels",
                "Spirale de la dette agricole — les dépendances aux intrants industriels (semences, pesticides, engrais) génèrent des cycles de dette insurmontables poussant des centaines de milliers d'agriculteurs à la ruine et au suicide",
            ]
        if self.risk_level == "élevé":
            return [
                f"Vulnérabilité structurelle agricole de {n} — dépendances économiques profondes vis-à-vis des marchés internationaux et des grandes corporations agro-industrielles réduisant la résilience alimentaire locale",
                "Érosion de la biodiversité agricole — la standardisation des semences industrielles réduit drastiquement la diversité génétique des cultures, fragilisant les écosystèmes et la capacité d'adaptation aux changements climatiques",
                "Déplacement des petits agriculteurs — la concurrence des importations subventionnées et des grandes exploitations industrielles expulse des millions de familles paysannes de leurs terres et de leurs moyens de subsistance",
            ]
        if self.risk_level == "modéré":
            return [
                f"Pressions agricoles modérées de {n} — tensions entre modèle agro-industriel et souveraineté alimentaire locale avec solutions partielles insuffisantes pour protéger les droits des agriculteurs",
                "Risques de monopolisation progressive — la concentration du secteur semencier et de la distribution alimentaire crée des dépendances croissantes sans législation antitrust adaptée",
                "Savoirs traditionnels menacés — les pratiques agricoles ancestrales et les variétés locales s'érodent sous la pression des modèles d'agriculture intensive sans programme de préservation adéquat",
            ]
        return [
            f"{n} incarne la souveraineté alimentaire exemplaire — diversité des systèmes agricoles, protection des semences paysannes et accès sécurisé à la terre pour les petits agriculteurs",
            "Droits des agriculteurs respectés — traité FAO sur les ressources phytogénétiques appliqué, banques de semences communautaires financées et pratiques agroécologiques soutenues",
            "Modèle résilient exportable — politiques alimentaires locales protectrices, marchés de proximité développés et programmes de soutien à l'agriculture paysanne durables",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "land_grabbing_smallholder_displacement_score": self.land_grabbing_smallholder_displacement_score,
            "corporate_seed_monopoly_farmer_dependency_score": self.corporate_seed_monopoly_farmer_dependency_score,
            "food_import_dependency_price_shock_vulnerability_score": self.food_import_dependency_price_shock_vulnerability_score,
            "traditional_farming_knowledge_erosion_score": self.traditional_farming_knowledge_erosion_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_food_sovereignty_agricultural_rights_index": self.estimated_food_sovereignty_agricultural_rights_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[FoodSovereigntyAgriculturalRightsEntity] = [
    FoodSovereigntyAgriculturalRightsEntity(
        "FSAR-001",
        "Inde/Suicides Agriculteurs Dettes Bt Cotton Monsanto 300K Morts",
        "Asie du Sud",
        "300.000 Suicides Agriculteurs 1995-2022, Bt Cotton Monsanto Dépendance, Cycles Dette Insurmontables, Maharashtra Epicentre & Loi Semences Propriétaires 2020 Retirée",
        85.0, 90.0, 72.0, 80.0,
    ),
    FoodSovereigntyAgriculturalRightsEntity(
        "FSAR-002",
        "Éthiopie/Accaparement Terres 3.6M Hectares Investisseurs Étrangers",
        "Afrique de l'Est",
        "3.6M Ha Cédés 2000-2015, Saudi Arabia/India/China Investisseurs, Villages Oromia Déplacés, Gambella 70.000 Expulsés & Oakland Institute Rapport Violations",
        88.0, 68.0, 62.0, 72.0,
    ),
    FoodSovereigntyAgriculturalRightsEntity(
        "FSAR-003",
        "Zambie/Monsanto Semences OGM Dépendance Totale Maïs",
        "Afrique Australe",
        "Monsanto DK Maïs OGM 80% Marché Zambie, Semences Paysannes Illégales, Accord PGS Monsanto, Petits Agriculteurs Endettés & Bayer-Monsanto Fusion Monopole",
        72.0, 86.0, 68.0, 74.0,
    ),
    FoodSovereigntyAgriculturalRightsEntity(
        "FSAR-004",
        "Brésil/Déforestation Amazonie Soja Agrobusiness Cerrado",
        "Amérique du Sud",
        "13.000 Km2/An Amazonie Déforestation, Soja Cerrado Expansion, Grilagem Accaparement Terres Autochtones, Quilombolas Expulsés & Bolsonaro FUNAI Démantèlement",
        80.0, 68.0, 55.0, 62.0,
    ),
    FoodSovereigntyAgriculturalRightsEntity(
        "FSAR-005",
        "Philippines/Dépendance Agro-industrielle Riz Importé WTO",
        "Asie du Sud-Est",
        "Accords WTO Libéralisation Riz, Tarifficação 2019, Agriculteurs Locaux Concurrence Importations, CARP Réforme Agraire Inachevée & IRRI Semences Hybrides Dépendance",
        52.0, 56.0, 62.0, 54.0,
    ),
    FoodSovereigntyAgriculturalRightsEntity(
        "FSAR-006",
        "Haïti/Dépendance Importations Alimentaires 60% Post-Tremblement de Terre",
        "Caraïbes",
        "60% Alimentation Importée, Riz USA Dumping Détruit Agriculture Locale, Tremblements de Terre 2010+2021, Aide Alimentaire Dépendance & Semences Hybrides Don Monsanto Refusé",
        46.0, 52.0, 82.0, 58.0,
    ),
    FoodSovereigntyAgriculturalRightsEntity(
        "FSAR-007",
        "Mexique/ALENA Maïs Natif Menacé Importations USA",
        "Amérique du Nord",
        "59 Variétés Maïs Natif Menacées, ALENA Maïs USA Dumping, Milpa Système Traditionnel Déclin, Décret OGM Maïs 2023 Annulé Pression USA & 4M Agriculteurs Déplacés ALENA",
        30.0, 34.0, 38.0, 42.0,
    ),
    FoodSovereigntyAgriculturalRightsEntity(
        "FSAR-008",
        "Via Campesina ONU Traité Ressources Phytogénétiques",
        "Global",
        "Via Campesina 182 Organisations 81 Pays, Traité FAO Ressources Phytogénétiques 2004, UPOV-CBD Équilibre Semences Paysannes, Agroécologie Transition Soutenue & Rapporteur Spécial Droit Alimentation",
        8.0, 10.0, 12.0, 8.0,
    ),
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
        "last_analysis": "2026-06-21",
        "engine_version": "1.0.0",
        "domain": "food_sovereignty_agricultural_rights",
        "confidence_score": 0.85,
        "data_sources": [
            "fao_treaty_plant_genetic_resources_2004",
            "oakland_institute_land_grab_reports",
            "grain_org_landgrabbing_database_2023",
            "via_campesina_food_sovereignty_reports",
        ],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_food_sovereignty_agricultural_rights_index": round(avg / 100 * 10, 2),
    }


def analyze_food_sovereignty_agricultural_rights() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Food Sovereignty Agricultural Rights Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} -> {e.risk_level} ({e.composite_score})")
