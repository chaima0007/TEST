"""
Caelum Partners — Migrant Workers Rights Kafala Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Droits des travailleurs migrants et système kafala (exploitation travailleurs Gulf,
travailleurs domestiques sans droits, décès chantiers Qatar Mondial, confiscation passeports).

Le système kafala (sponsorship) lie légalement les travailleurs migrants à leur employeur,
les privant de toute liberté de mouvement ou de changement d'emploi sans permission.
Plus de 25 millions de travailleurs migrants dans le Golfe vivent sous ce régime
documenté comme travail forcé par l'OIT. La confiscation des passeports, pratique illégale
mais systémique, transforme des millions de travailleurs en serfs modernes.

Les décès sur les chantiers qataris liés au Mondial 2022 — estimés à 6 500+ par
The Guardian — illustrent l'impunité totale dont jouissent les employeurs
dans les pays du Golfe. Les travailleurs domestiques, majoritairement des femmes
d'Asie du Sud et d'Afrique, restent exclus des protections du droit du travail
dans la plupart des pays du Golfe, exposées aux abus physiques et sexuels sans recours.

Risk levels (exploitation travailleurs migrants kafala et impunité) :
  critique  -> composite >= 60  (kafala total, travail forcé documenté, impunité bourreaux)
  élevé     -> composite >= 40  (droits partiels, exploitation sans kafala, risque élevé)
  modéré    -> composite >= 20  (protections formelles insuffisantes, quelques recours)
  faible    -> composite < 20   (cadre protecteur effectif, droits migrants respectés)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List
import statistics


@dataclass
class MigrantWorkersRightsKafalaEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    kafala_labor_bondage_score: float
    migrant_worker_death_injury_impunity_score: float
    passport_confiscation_movement_restriction_score: float
    migrant_legal_protection_access_justice_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    key_signals: List[str] = field(default_factory=list)
    estimated_migrant_workers_rights_kafala_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.kafala_labor_bondage_score * 0.30
            + self.migrant_worker_death_injury_impunity_score * 0.25
            + self.passport_confiscation_movement_restriction_score * 0.25
            + self.migrant_legal_protection_access_justice_gap_score * 0.20,
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
        self.estimated_migrant_workers_rights_kafala_index = round(
            self.composite_score / 100 * 10, 2
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "kafala_labor_bondage_score": self.kafala_labor_bondage_score,
            "migrant_worker_death_injury_impunity_score": self.migrant_worker_death_injury_impunity_score,
            "passport_confiscation_movement_restriction_score": self.passport_confiscation_movement_restriction_score,
            "migrant_legal_protection_access_justice_gap_score": self.migrant_legal_protection_access_justice_gap_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_migrant_workers_rights_kafala_index": self.estimated_migrant_workers_rights_kafala_index,
            "last_updated": self.last_updated,
        }


@dataclass
class MigrantWorkersRightsKafalaEngineResult:
    agent: str = "Migrant Workers Rights Kafala Engine Agent"
    domain: str = "migrant_workers_rights_kafala"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.89
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_migrant_workers_rights_kafala_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[MigrantWorkersRightsKafalaEntity] = field(default_factory=list)


def run_migrant_workers_rights_kafala_engine() -> MigrantWorkersRightsKafalaEngineResult:
    entities = [
        MigrantWorkersRightsKafalaEntity(
            entity_id="MWK-001",
            name="Qatar — 6 500+ Décès Mondial 2022, Kafala Total, Passeports Confisqués & Travail Forcé Documenté",
            country="Qatar",
            sector="Construction & Travailleurs Migrants Golfe",
            kafala_labor_bondage_score=97.0,
            migrant_worker_death_injury_impunity_score=96.0,
            passport_confiscation_movement_restriction_score=95.0,
            migrant_legal_protection_access_justice_gap_score=94.0,
            primary_pattern="kafala_labor_bondage",
            key_signals=[
                "6500+ décès chantiers Guardian/Amnesty",
                "kafala intégral sans réforme effective",
                "confiscation passeports systémique",
                "travailleurs domestiques exclus droit du travail",
            ],
        ),
        MigrantWorkersRightsKafalaEntity(
            entity_id="MWK-002",
            name="Arabie Saoudite — Kafala Strict, Travailleurs Domestiques Exclus Code Travail & Expulsions Massives",
            country="Arabie Saoudite",
            sector="Ménages & Construction Kafala",
            kafala_labor_bondage_score=94.0,
            migrant_worker_death_injury_impunity_score=91.0,
            passport_confiscation_movement_restriction_score=93.0,
            migrant_legal_protection_access_justice_gap_score=92.0,
            primary_pattern="kafala_labor_bondage",
            key_signals=[
                "kafala strict sans réforme majeure",
                "travailleurs domestiques exclus code travail",
                "abus physiques/sexuels employeurs non punis",
                "expulsions massives sans recours",
            ],
        ),
        MigrantWorkersRightsKafalaEntity(
            entity_id="MWK-003",
            name="Émirats Arabes Unis — Kafala, Construction Sans Protection Chaleur & Salaires Non Payés Logements Surpeuplés",
            country="Émirats Arabes Unis",
            sector="Construction & Services Kafala",
            kafala_labor_bondage_score=91.0,
            migrant_worker_death_injury_impunity_score=88.0,
            passport_confiscation_movement_restriction_score=90.0,
            migrant_legal_protection_access_justice_gap_score=89.0,
            primary_pattern="passport_confiscation_movement_restriction",
            key_signals=[
                "kafala dominant malgré réformes cosmétiques",
                "décès chaleur chantiers sans enquête",
                "logements surpeuplés sans normes",
                "salaires non payés sans recours effectif",
            ],
        ),
        MigrantWorkersRightsKafalaEntity(
            entity_id="MWK-004",
            name="Koweït — Kafala, Travailleurs Domestiques Asiatiques/Africains Conditions Esclavage & Meurtres Impunis",
            country="Koweït",
            sector="Ménages & Travailleurs Domestiques",
            kafala_labor_bondage_score=88.0,
            migrant_worker_death_injury_impunity_score=86.0,
            passport_confiscation_movement_restriction_score=87.0,
            migrant_legal_protection_access_justice_gap_score=85.0,
            primary_pattern="migrant_worker_death_injury_impunity",
            key_signals=[
                "kafala sans exception travailleurs domestiques",
                "meurtres employeurs impunis documentés HRW",
                "chutes immeubles travailleurs non élucidées",
                "zéro accès justice pour domestiques",
            ],
        ),
        MigrantWorkersRightsKafalaEntity(
            entity_id="MWK-005",
            name="Singapour — Travailleurs Construction Logements Ségrégués, COVID Révèle Conditions & Droits Partiels",
            country="Singapour",
            sector="Construction & Services Migrants",
            kafala_labor_bondage_score=52.0,
            migrant_worker_death_injury_impunity_score=49.0,
            passport_confiscation_movement_restriction_score=46.0,
            migrant_legal_protection_access_justice_gap_score=50.0,
            primary_pattern="migrant_legal_protection_access_justice_gap",
            key_signals=[
                "dortoirs COVID révèlent surpeuplement",
                "droits partiels sans kafala",
                "ségrégation logements construction",
                "syndicats limités pour migrants",
            ],
        ),
        MigrantWorkersRightsKafalaEntity(
            entity_id="MWK-006",
            name="USA — Travailleurs Agricoles H-2A Sans Droits Collectifs, Sans-Papiers Exploités & Menaces ICE",
            country="USA",
            sector="Agriculture & Travail Saisonnier Migrants",
            kafala_labor_bondage_score=48.0,
            migrant_worker_death_injury_impunity_score=47.0,
            passport_confiscation_movement_restriction_score=43.0,
            migrant_legal_protection_access_justice_gap_score=49.0,
            primary_pattern="kafala_labor_bondage",
            key_signals=[
                "H-2A exclus NLRA droit syndical",
                "travailleurs sans-papiers sans recours ICE",
                "confiscation passeports H-2B documentée",
                "travail forcé agriculture documenté Polaris",
            ],
        ),
        MigrantWorkersRightsKafalaEntity(
            entity_id="MWK-007",
            name="Liban — Kafala Travailleurs Domestiques Éthiopiennes, Économie Effondrée & Salaires Non Payés",
            country="Liban",
            sector="Ménages & Travailleurs Domestiques",
            kafala_labor_bondage_score=28.0,
            migrant_worker_death_injury_impunity_score=26.0,
            passport_confiscation_movement_restriction_score=27.0,
            migrant_legal_protection_access_justice_gap_score=25.0,
            primary_pattern="kafala_labor_bondage",
            key_signals=[
                "kafala travailleurs domestiques ethiopiennes",
                "économie effondrée salaires impayés",
                "quelques protections légales nominales",
                "abus documentés mais poursuites rares",
            ],
        ),
        MigrantWorkersRightsKafalaEntity(
            entity_id="MWK-008",
            name="Nouvelle-Zélande — Droits Migrants Protégés, Inspection Travail Effective & Résidence Possible Sans Kafala",
            country="Nouvelle-Zélande",
            sector="Travail Migrants Protégé",
            kafala_labor_bondage_score=8.0,
            migrant_worker_death_injury_impunity_score=7.0,
            passport_confiscation_movement_restriction_score=6.0,
            migrant_legal_protection_access_justice_gap_score=9.0,
            primary_pattern="migrant_legal_protection_access_justice_gap",
            key_signals=[
                "pas de système kafala",
                "inspection travail effective",
                "voies résidence permanente ouvertes",
                "droits collectifs garantis migrants",
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

    return MigrantWorkersRightsKafalaEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_migrant_workers_rights_kafala_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ilo_migrant_workers_report_2023",
            "human_rights_watch_kafala_system_2023",
            "amnesty_international_migrant_workers_gulf_2023",
            "business_human_rights_resource_centre_migrant_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_migrant_workers_rights_kafala_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_migrant_workers_rights_kafala_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
