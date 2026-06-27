from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class IndigenousLandRightsExtractionEntity:
    entity_id: str
    name: str
    country: str
    extractive_industry_territory_invasion_severity_score: float
    fpic_violation_forced_displacement_scale_score: float
    indigenous_environmental_defender_killing_score: float
    legal_title_recognition_land_rights_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_indigenous_land_rights_extraction_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.extractive_industry_territory_invasion_severity_score * 0.30
            + self.fpic_violation_forced_displacement_scale_score * 0.25
            + self.indigenous_environmental_defender_killing_score * 0.25
            + self.legal_title_recognition_land_rights_deficit_gap_score * 0.20,
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
        self.estimated_indigenous_land_rights_extraction_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class IndigenousLandRightsExtractionEngineResult:
    agent: str = "Indigenous Land Rights Extraction Engine Agent"
    domain: str = "indigenous_land_rights_extraction"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_indigenous_land_rights_extraction_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[IndigenousLandRightsExtractionEntity] = field(default_factory=list)

def run_indigenous_land_rights_extraction_engine() -> IndigenousLandRightsExtractionEngineResult:
    entities = [
        IndigenousLandRightsExtractionEntity(
            entity_id="ILE-001",
            name="Brésil/Amazonie — Garimpos Illégaux Yanomami, Terras Indígenas Envahies, Garimpeiros Armés & Lula Belo Monte Concessions",
            country="Brésil",
            extractive_industry_territory_invasion_severity_score=95.0,
            fpic_violation_forced_displacement_scale_score=93.0,
            indigenous_environmental_defender_killing_score=92.0,
            legal_title_recognition_land_rights_deficit_gap_score=94.0,
            primary_pattern="extractive_industry_territory_invasion_severity",
        ),
        IndigenousLandRightsExtractionEntity(
            entity_id="ILE-002",
            name="Canada/Pipeline — TMX Trans Mountain Wet'suwet'en, GRC Expulsions Militarisées, Fracking Terres Sacrées & Site C Barrage Non-Consulté",
            country="Canada",
            extractive_industry_territory_invasion_severity_score=91.0,
            fpic_violation_forced_displacement_scale_score=92.0,
            indigenous_environmental_defender_killing_score=88.0,
            legal_title_recognition_land_rights_deficit_gap_score=90.0,
            primary_pattern="fpic_violation_forced_displacement_scale",
        ),
        IndigenousLandRightsExtractionEntity(
            entity_id="ILE-003",
            name="Philippines/Mindanao — Lumad Schools Fermées Armée, Mines Or Terres Ancestrales, Défenseurs Tués 2020-24 & Permis Extractifs Sans FPIC",
            country="Philippines",
            extractive_industry_territory_invasion_severity_score=88.0,
            fpic_violation_forced_displacement_scale_score=86.0,
            indigenous_environmental_defender_killing_score=89.0,
            legal_title_recognition_land_rights_deficit_gap_score=87.0,
            primary_pattern="indigenous_environmental_defender_killing",
        ),
        IndigenousLandRightsExtractionEntity(
            entity_id="ILE-004",
            name="Pérou/TIPNIS — Communautés Amazonie Expulsées Pétrole, Consultation Simulacre, Défenseurs Criminalisés & Accords Chevron Confidentiels",
            country="Pérou",
            extractive_industry_territory_invasion_severity_score=84.0,
            fpic_violation_forced_displacement_scale_score=82.0,
            indigenous_environmental_defender_killing_score=85.0,
            legal_title_recognition_land_rights_deficit_gap_score=83.0,
            primary_pattern="extractive_industry_territory_invasion_severity",
        ),
        IndigenousLandRightsExtractionEntity(
            entity_id="ILE-005",
            name="Australie/Mines — Aboriginal Sacred Sites Destroyed Rio Tinto Juukan Gorge 2020, Native Title Contournement & Consultation Pro-Forma",
            country="Australie",
            extractive_industry_territory_invasion_severity_score=56.0,
            fpic_violation_forced_displacement_scale_score=54.0,
            indigenous_environmental_defender_killing_score=55.0,
            legal_title_recognition_land_rights_deficit_gap_score=57.0,
            primary_pattern="legal_title_recognition_land_rights_deficit_gap",
        ),
        IndigenousLandRightsExtractionEntity(
            entity_id="ILE-006",
            name="Kenya/Maasai — Expulsions Parc Ngorongoro, Tourisme Sans Bénéfice, Terres Ancestrales Privatisées & Cattle Confiscated",
            country="Kenya",
            extractive_industry_territory_invasion_severity_score=53.0,
            fpic_violation_forced_displacement_scale_score=51.0,
            indigenous_environmental_defender_killing_score=52.0,
            legal_title_recognition_land_rights_deficit_gap_score=54.0,
            primary_pattern="fpic_violation_forced_displacement_scale",
        ),
        IndigenousLandRightsExtractionEntity(
            entity_id="ILE-007",
            name="FILAC/IITC — Fonds Développement Peuples Indigènes, International Indian Treaty Council, Standards FPIC & Monitoring Mécanismes ONU",
            country="Global",
            extractive_industry_territory_invasion_severity_score=27.0,
            fpic_violation_forced_displacement_scale_score=26.0,
            indigenous_environmental_defender_killing_score=28.0,
            legal_title_recognition_land_rights_deficit_gap_score=25.0,
            primary_pattern="legal_title_recognition_land_rights_deficit_gap",
        ),
        IndigenousLandRightsExtractionEntity(
            entity_id="ILE-008",
            name="ONU/DRIP Terres — DRIP Art.26-32 Terres Ressources, Agenda 2030 ODD 15, Mécanisme Expert Peuples Autochtones & Rapporteur Spécial",
            country="Global",
            extractive_industry_territory_invasion_severity_score=4.0,
            fpic_violation_forced_displacement_scale_score=4.0,
            indigenous_environmental_defender_killing_score=4.0,
            legal_title_recognition_land_rights_deficit_gap_score=4.0,
            primary_pattern="extractive_industry_territory_invasion_severity",
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

    return IndigenousLandRightsExtractionEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_indigenous_land_rights_extraction_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "global_witness_land_defender_killings_report",
            "un_special_rapporteur_indigenous_peoples_land",
            "cultural_survival_fpic_violation_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_indigenous_land_rights_extraction_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_indigenous_land_rights_extraction_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
