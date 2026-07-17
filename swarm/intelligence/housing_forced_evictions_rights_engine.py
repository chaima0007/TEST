"""
Caelum Partners — Housing Rights & Forced Evictions Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Droit au logement & expulsions forcées — expulsions collectives, sans-abrisme,
spéculation immobilière, discrimination et droit à la vie digne.

Le droit à un logement convenable est reconnu par l'article 11 du Pacte international
relatif aux droits économiques, sociaux et culturels (PIDESC). Le Comité des droits
économiques, sociaux et culturels de l'ONU définit le logement convenable à travers
7 critères : sécurité d'occupation, accessibilité des services, accessibilité financière,
habitabilité, accessibilité pour les groupes vulnérables, emplacement et adéquation culturelle.

Les expulsions forcées — définies par le Comité comme "l'éviction permanente ou temporaire
de personnes, familles ou communautés de leurs maisons contre leur volonté sans bénéficier
d'une protection légale ou autre" — constituent une violation grave du droit au logement.
Chaque année, des millions de personnes sont expulsées de force dans le monde pour cause
de rénovation urbaine, méga-événements sportifs, spéculation foncière ou répression politique.

Risk levels (expulsions forcées, crise logement abordable, vide protection légale, sans-abrisme) :
  critique  -> composite >= 60  (expulsions massives — état droit au logement systémiquement violé)
  élevé     -> composite >= 40  (crise logement sévère — mécanismes protection insuffisants)
  modéré    -> composite >= 20  (défis persistants — protection partielle, réformes en cours)
  faible    -> composite < 20   (cadre protecteur robuste — logement social efficace, faible sans-abrisme)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List
import statistics


@dataclass
class HousingForcedEvictionsRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    forced_eviction_rate_score: float
    housing_affordability_crisis_score: float
    legal_protection_enforcement_deficit_score: float
    homelessness_state_response_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    key_signals: List[str] = field(default_factory=list)
    estimated_housing_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.forced_eviction_rate_score * 0.30
            + self.housing_affordability_crisis_score * 0.25
            + self.legal_protection_enforcement_deficit_score * 0.25
            + self.homelessness_state_response_score * 0.20,
            2,
        )
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_housing_rights_index = round(
            self.composite_score / 100 * 10, 2
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "forced_eviction_rate_score": self.forced_eviction_rate_score,
            "housing_affordability_crisis_score": self.housing_affordability_crisis_score,
            "legal_protection_enforcement_deficit_score": self.legal_protection_enforcement_deficit_score,
            "homelessness_state_response_score": self.homelessness_state_response_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_housing_rights_index": self.estimated_housing_rights_index,
            "last_updated": self.last_updated,
        }


@dataclass
class HousingForcedEvictionsRightsEngineResult:
    agent: str = "Housing Forced Evictions Rights Engine Agent"
    domain: str = "housing_forced_evictions_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_housing_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[HousingForcedEvictionsRightsEntity] = field(default_factory=list)


def run_housing_forced_evictions_rights_engine() -> HousingForcedEvictionsRightsEngineResult:
    entities = [
        HousingForcedEvictionsRightsEntity(
            entity_id="HFE-001",
            name="Inde — 100M+ Sans Logement Adéquat, Démolitions Bidonvilles Massives, Dalit Ciblés",
            country="Inde",
            sector="Expulsions Forcées Bidonvilles & Discrimination Caste",
            forced_eviction_rate_score=93.0,
            housing_affordability_crisis_score=90.0,
            legal_protection_enforcement_deficit_score=91.0,
            homelessness_state_response_score=88.0,
            primary_pattern="forced_eviction_rate",
            key_signals=[
                "100M+ personnes sans logement adéquat — chiffre ONU Habitat 2022",
                "Bulldozers: opérations démolition bidonvilles ciblant Dalit et Musulmans",
                "Projet aménagement Delhi 2021: 60 000 familles expulsées en 3 mois",
                "Supreme Court ordres protection ignorés par autorités locales",
            ],
        ),
        HousingForcedEvictionsRightsEntity(
            entity_id="HFE-002",
            name="Kenya/Nairobi — Kibera 250 000 Expulsés Décennie, Récupération Terrain État sans Indemnité",
            country="Kenya",
            sector="Expulsions Forcées Bidonvilles Africains",
            forced_eviction_rate_score=88.0,
            housing_affordability_crisis_score=84.0,
            legal_protection_enforcement_deficit_score=87.0,
            homelessness_state_response_score=83.0,
            primary_pattern="forced_eviction_rate",
            key_signals=[
                "Kibera: 250 000 personnes expulsées sur 10 ans — plus grand bidonville Afrique Est",
                "Expulsions pour corridor Nairobi Expressway 2021 sans relogement adéquat",
                "Land grabbing: terrains publics cédés à promoteurs privés",
                "Violence policière lors expulsions — SDO Nairobi documentés par HRW",
            ],
        ),
        HousingForcedEvictionsRightsEntity(
            entity_id="HFE-003",
            name="Philippines/Manille — 100 000 Expulsions/An Urban Poor, Duterte Reclaiming Land Programme",
            country="Philippines",
            sector="Expulsions Urbaines Violentes Pauvres Urbains",
            forced_eviction_rate_score=84.0,
            housing_affordability_crisis_score=79.0,
            legal_protection_enforcement_deficit_score=82.0,
            homelessness_state_response_score=80.0,
            primary_pattern="forced_eviction_rate",
            key_signals=[
                "100 000+ personnes expulsées annuellement Zone Métro Manille",
                "Programme reclaiming zones côtières — bidonvilles littoraux détruits",
                "Relocalisation sites Bulacan/Cavite — 80km de Manille, sans emploi",
                "UDHA Loi 1992 protection: appliquée partiellement, contournée par NHA",
            ],
        ),
        HousingForcedEvictionsRightsEntity(
            entity_id="HFE-004",
            name="Brésil/Favelas — 170 000 Expulsés JO Rio 2016, Spéculation Immobilière Porto Maravilha",
            country="Brésil",
            sector="Expulsions Méga-Événements & Gentrification",
            forced_eviction_rate_score=79.0,
            housing_affordability_crisis_score=77.0,
            legal_protection_enforcement_deficit_score=76.0,
            homelessness_state_response_score=75.0,
            primary_pattern="forced_eviction_rate",
            key_signals=[
                "170 000 personnes expulsées pour préparation JO Rio 2016",
                "Vila Autódromo: résistance communautaire JO — documentée monde entier",
                "Spéculation Porto Maravilha: hausse loyers 400% en 5 ans",
                "PSOL et MTST — mouvement sans-toit mobilise contre expulsions",
            ],
        ),
        HousingForcedEvictionsRightsEntity(
            entity_id="HFE-005",
            name="USA — 600 000 Sans-Abri/Nuit, Anti-Camping Laws, Gentrification Côtes & Criminalisation SDF",
            country="USA",
            sector="Crise Logement & Criminalisation Sans-Abrisme",
            forced_eviction_rate_score=52.0,
            housing_affordability_crisis_score=58.0,
            legal_protection_enforcement_deficit_score=55.0,
            homelessness_state_response_score=53.0,
            primary_pattern="housing_affordability_crisis",
            key_signals=[
                "653 000 personnes sans-abri nuit comptage janvier 2023 — record",
                "Anti-camping ordinances: 187 villes criminalisent sans-abrisme",
                "Grants Pass arrêt SCOTUS 2024 — autorise démantèlement campements",
                "Côte Ouest: San Francisco loyer médian 3 500$/mois — 37% de leurs revenus",
            ],
        ),
        HousingForcedEvictionsRightsEntity(
            entity_id="HFE-006",
            name="France — 300 000 Sans Domicile, DAL Contesté, Expulsions Hivernales Trêve Contournée",
            country="France",
            sector="Crise Logement Pays Développé & Droits Locataires",
            forced_eviction_rate_score=44.0,
            housing_affordability_crisis_score=50.0,
            legal_protection_enforcement_deficit_score=45.0,
            homelessness_state_response_score=47.0,
            primary_pattern="housing_affordability_crisis",
            key_signals=[
                "330 000 sans domicile fixe France 2023 — doublement en 10 ans",
                "Trêve hivernale contournée: expulsions reprise 1er avril malgré recours",
                "DAL droit opposable logement: 300 000 recours, 70% non relogés",
                "Airbnb: 700 000 logements retirés marché locatif Paris/Lyon/Bordeaux",
            ],
        ),
        HousingForcedEvictionsRightsEntity(
            entity_id="HFE-007",
            name="Pays-Bas — Réforme Logement Social: 170 000 Logements Vendus Secteur Privé, Liste Attente 15 Ans",
            country="Pays-Bas",
            sector="Démantèlement Logement Social Pays Développé",
            forced_eviction_rate_score=28.0,
            housing_affordability_crisis_score=32.0,
            legal_protection_enforcement_deficit_score=26.0,
            homelessness_state_response_score=30.0,
            primary_pattern="housing_affordability_crisis",
            key_signals=[
                "170 000 logements sociaux vendus 2010-2020 sous pression libéralisation",
                "Liste attente logement social Amsterdam: 15 ans en moyenne",
                "Loi Stikstof azote bloque construction 100 000+ nouveaux logements",
                "Woondeals: accords régionaux logement — objectifs rarement atteints",
            ],
        ),
        HousingForcedEvictionsRightsEntity(
            entity_id="HFE-008",
            name="Finlande — Modèle Housing First: Sans-Abrisme Réduit 85%, Y-Foundation Référence Mondiale",
            country="Finlande",
            sector="Logement Digne — Modèle de Référence Mondial",
            forced_eviction_rate_score=6.0,
            housing_affordability_crisis_score=8.0,
            legal_protection_enforcement_deficit_score=5.0,
            homelessness_state_response_score=4.0,
            primary_pattern="homelessness_state_response",
            key_signals=[
                "Housing First depuis 2008: sans-abrisme réduit de 85% en 15 ans",
                "Y-Foundation: 16 000 logements accessibles — modèle copié 14 pays EU",
                "SDF longue durée quasi éliminés: 3 500 personnes en 2023 (vs 19 000 en 2008)",
                "Cost-benefit: 1€ Housing First = 2€ économisés urgences/prisons",
            ],
        ),
    ]

    composites = [e.composite_score for e in entities]
    avg_composite = round(statistics.mean(composites), 2)

    risk_dist: dict = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1

    pattern_dist: dict = {}
    for e in entities:
        pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1

    sorted_entities = sorted(entities, key=lambda x: x.composite_score, reverse=True)
    top_risk = [e.name for e in sorted_entities[:3]]
    alerts = [
        f"{e.name.split('—')[0].strip()}: {e.primary_pattern}"
        for e in sorted_entities[:4]
    ]

    return HousingForcedEvictionsRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_housing_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_habitat_world_cities_report_2022",
            "cohre_global_survey_forced_evictions_2023",
            "amnesty_international_housing_rights_report_2023",
            "feantsa_ethos_homelessness_europe_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_housing_forced_evictions_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_housing_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
