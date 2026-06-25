from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class IndigenousLandCulturalRightsEntity:
    entity_id: str
    name: str
    country: str
    land_dispossession_extractive_industry_score: float
    free_prior_informed_consent_violation_score: float
    cultural_erasure_language_rights_score: float
    indigenous_legal_framework_enforcement_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_indigenous_land_cultural_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.land_dispossession_extractive_industry_score * 0.30
            + self.free_prior_informed_consent_violation_score * 0.25
            + self.cultural_erasure_language_rights_score * 0.25
            + self.indigenous_legal_framework_enforcement_gap_score * 0.20,
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
        self.estimated_indigenous_land_cultural_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class IndigenousLandCulturalRightsEngineResult:
    agent: str = "Indigenous Land Cultural Rights Engine Agent"
    domain: str = "indigenous_land_cultural_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_indigenous_land_cultural_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[IndigenousLandCulturalRightsEntity] = field(default_factory=list)


def run_indigenous_land_cultural_rights_engine() -> IndigenousLandCulturalRightsEngineResult:
    entities = [
        IndigenousLandCulturalRightsEntity(
            entity_id="ILCR-001",
            name="Brésil/Amazonie — Garimpeiros Yanomami, 200 Décès 2021-2022, Brûlage Terres, Bolsonaro Démantèle FUNAI",
            country="Brésil",
            land_dispossession_extractive_industry_score=96.0,
            free_prior_informed_consent_violation_score=94.0,
            cultural_erasure_language_rights_score=92.0,
            indigenous_legal_framework_enforcement_gap_score=93.0,
            primary_pattern="land_dispossession_extractive_industry",
        ),
        IndigenousLandCulturalRightsEntity(
            entity_id="ILCR-002",
            name="Canada/Systèmes Résidentiels — Héritage Pensionnats, 215 Enfants Kamloops 2021, DRIPA Non Implémentée",
            country="Canada",
            land_dispossession_extractive_industry_score=90.0,
            free_prior_informed_consent_violation_score=88.0,
            cultural_erasure_language_rights_score=91.0,
            indigenous_legal_framework_enforcement_gap_score=89.0,
            primary_pattern="cultural_erasure_language_rights",
        ),
        IndigenousLandCulturalRightsEntity(
            entity_id="ILCR-003",
            name="Philippines/Lumad — Écoles Autochtones Brûlées Armée, Déplacements Mines & Plantations, Militarisation",
            country="Philippines",
            land_dispossession_extractive_industry_score=87.0,
            free_prior_informed_consent_violation_score=85.0,
            cultural_erasure_language_rights_score=84.0,
            indigenous_legal_framework_enforcement_gap_score=86.0,
            primary_pattern="free_prior_informed_consent_violation",
        ),
        IndigenousLandCulturalRightsEntity(
            entity_id="ILCR-004",
            name="Éthiopie/Oromo — Addis-Abeba Expansion, Fermiers Expulsés Sans Compensation, Résistance Réprimée",
            country="Éthiopie",
            land_dispossession_extractive_industry_score=84.0,
            free_prior_informed_consent_violation_score=82.0,
            cultural_erasure_language_rights_score=80.0,
            indigenous_legal_framework_enforcement_gap_score=83.0,
            primary_pattern="indigenous_legal_framework_enforcement_gap",
        ),
        IndigenousLandCulturalRightsEntity(
            entity_id="ILCR-005",
            name="Pérou/Peuples Amazonie — TIPNIS Conflit Hydrocarbures, Consultation FPIC Violée, Leaders Autochtones Tués",
            country="Pérou",
            land_dispossession_extractive_industry_score=58.0,
            free_prior_informed_consent_violation_score=57.0,
            cultural_erasure_language_rights_score=54.0,
            indigenous_legal_framework_enforcement_gap_score=55.0,
            primary_pattern="land_dispossession_extractive_industry",
        ),
        IndigenousLandCulturalRightsEntity(
            entity_id="ILCR-006",
            name="Kenya/Ogiek — Forêt Mau Expulsions, Jugement CADHP 2017 Non Exécuté, Déforestation Continue",
            country="Kenya",
            land_dispossession_extractive_industry_score=54.0,
            free_prior_informed_consent_violation_score=52.0,
            cultural_erasure_language_rights_score=50.0,
            indigenous_legal_framework_enforcement_gap_score=53.0,
            primary_pattern="indigenous_legal_framework_enforcement_gap",
        ),
        IndigenousLandCulturalRightsEntity(
            entity_id="ILCR-007",
            name="ONU/UNDRIP — Déclaration 2007 Droits Peuples Autochtones, FPIC Standard, États Signataires Sans Mise Oeuvre",
            country="Global",
            land_dispossession_extractive_industry_score=27.0,
            free_prior_informed_consent_violation_score=26.0,
            cultural_erasure_language_rights_score=25.0,
            indigenous_legal_framework_enforcement_gap_score=24.0,
            primary_pattern="free_prior_informed_consent_violation",
        ),
        IndigenousLandCulturalRightsEntity(
            entity_id="ILCR-008",
            name="Nouvelle-Zélande/Māori — Tribunal Waitangi Fonctionnel, Treaty Settlements, FPIC Constitutionnel Progressif",
            country="Nouvelle-Zélande",
            land_dispossession_extractive_industry_score=7.0,
            free_prior_informed_consent_violation_score=6.0,
            cultural_erasure_language_rights_score=6.0,
            indigenous_legal_framework_enforcement_gap_score=5.0,
            primary_pattern="indigenous_legal_framework_enforcement_gap",
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

    return IndigenousLandCulturalRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_indigenous_land_cultural_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_special_rapporteur_indigenous_peoples_annual_report",
            "forest_peoples_programme_land_rights_violations",
            "cultural_survival_indigenous_rights_monitor",
            "hrw_indigenous_land_documentation",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_indigenous_land_cultural_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_indigenous_land_cultural_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
