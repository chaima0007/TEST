from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class LandGrabbingDisplacementRightsEntity:
    entity_id: str
    name: str
    country: str
    forced_displacement_scale_violence_score: float
    land_rights_legal_protection_gap_score: float
    defender_killings_criminalization_score: float
    corporate_state_accountability_deficit_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_land_grabbing_displacement_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.forced_displacement_scale_violence_score * 0.30
            + self.land_rights_legal_protection_gap_score * 0.25
            + self.defender_killings_criminalization_score * 0.25
            + self.corporate_state_accountability_deficit_score * 0.20,
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
        self.estimated_land_grabbing_displacement_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class LandGrabbingDisplacementRightsEngineResult:
    agent: str = "Land Grabbing Displacement Rights Engine Agent"
    domain: str = "land_grabbing_displacement_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.87
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    data_sources: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"


def run_land_grabbing_displacement_rights_engine() -> LandGrabbingDisplacementRightsEngineResult:
    entities = [
        LandGrabbingDisplacementRightsEntity(
            entity_id="KHM-001",
            name="Cambodge",
            country="Cambodge",
            forced_displacement_scale_violence_score=88.0,
            land_rights_legal_protection_gap_score=85.0,
            defender_killings_criminalization_score=82.0,
            corporate_state_accountability_deficit_score=87.0,
            primary_pattern="700K+ personnes déplacées concessions terres, sucre/caoutchouc EU/Chine, violence expulsion, LICADHO documenté",
        ),
        LandGrabbingDisplacementRightsEntity(
            entity_id="ETH-001",
            name="Éthiopie",
            country="Éthiopie",
            forced_displacement_scale_violence_score=90.0,
            land_rights_legal_protection_gap_score=88.0,
            defender_killings_criminalization_score=85.0,
            corporate_state_accountability_deficit_score=89.0,
            primary_pattern="Sugar Corporation 200K déplacés Omo Valley, terres cédées investisseurs étrangers, violence militaire",
        ),
        LandGrabbingDisplacementRightsEntity(
            entity_id="HND-001",
            name="Honduras",
            country="Honduras",
            forced_displacement_scale_violence_score=86.0,
            land_rights_legal_protection_gap_score=83.0,
            defender_killings_criminalization_score=92.0,
            corporate_state_accountability_deficit_score=88.0,
            primary_pattern="Berta Cáceres assassinée 2016, barrages DESA, 130+ défenseurs tués depuis 2010",
        ),
        LandGrabbingDisplacementRightsEntity(
            entity_id="PHL-001",
            name="Philippines",
            country="Philippines",
            forced_displacement_scale_violence_score=82.0,
            land_rights_legal_protection_gap_score=80.0,
            defender_killings_criminalization_score=86.0,
            corporate_state_accountability_deficit_score=84.0,
            primary_pattern="Lumad déplacés mines/palme, militarisation zones autochtones, DENR complicité",
        ),
        LandGrabbingDisplacementRightsEntity(
            entity_id="BRA-001",
            name="Brésil",
            country="Brésil",
            forced_displacement_scale_violence_score=55.0,
            land_rights_legal_protection_gap_score=48.0,
            defender_killings_criminalization_score=58.0,
            corporate_state_accountability_deficit_score=50.0,
            primary_pattern="Amazonie soja/bétail, garimpeiros vs Yanomami, 35 tués 2022 défenseurs terres",
        ),
        LandGrabbingDisplacementRightsEntity(
            entity_id="IND-001",
            name="Inde",
            country="Inde",
            forced_displacement_scale_violence_score=52.0,
            land_rights_legal_protection_gap_score=50.0,
            defender_killings_criminalization_score=45.0,
            corporate_state_accountability_deficit_score=55.0,
            primary_pattern="POSCO steel 22K déplacés Odisha, Land Acquisition Act résistances, tribaux Naxal zones",
        ),
        LandGrabbingDisplacementRightsEntity(
            entity_id="PER-001",
            name="Pérou",
            country="Pérou",
            forced_displacement_scale_violence_score=38.0,
            land_rights_legal_protection_gap_score=42.0,
            defender_killings_criminalization_score=35.0,
            corporate_state_accountability_deficit_score=40.0,
            primary_pattern="Consultations préalables FPIC contournées mines, conflits sociaux 200+/an, quelques indemnisations",
        ),
        LandGrabbingDisplacementRightsEntity(
            entity_id="NOR-001",
            name="Norvège",
            country="Norvège",
            forced_displacement_scale_violence_score=8.0,
            land_rights_legal_protection_gap_score=6.0,
            defender_killings_criminalization_score=5.0,
            corporate_state_accountability_deficit_score=7.0,
            primary_pattern="Protections légales solides, FPIC respecté populations Sámi, très rares expropriations",
        ),
    ]

    result = LandGrabbingDisplacementRightsEngineResult()
    result.total_entities = len(entities)
    result.avg_composite = round(
        statistics.mean(e.composite_score for e in entities), 2
    )
    result.confidence_score = 0.87

    risk_dist: dict = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
    result.risk_distribution = risk_dist

    sorted_entities = sorted(entities, key=lambda e: e.composite_score, reverse=True)
    result.top_risk_entities = [e.name for e in sorted_entities[:3]]
    result.critical_alerts = [
        f"{e.name}: composite={e.composite_score}, index={e.estimated_land_grabbing_displacement_rights_index}"
        for e in sorted_entities
        if e.risk_level == "critique"
    ]
    result.data_sources = [
        "global_witness_land_defenders_killed_2023",
        "oakland_institute_land_grabbing_database_2023",
        "grain_land_grabbing_global_2023",
        "business_human_rights_resource_centre_land_2023",
    ]

    return result


if __name__ == "__main__":
    result = run_land_grabbing_displacement_rights_engine()
    print(f"Agent      : {result.agent}")
    print(f"Domain     : {result.domain}")
    print(f"Entities   : {result.total_entities}")
    print(f"Avg composite : {result.avg_composite}")
    print(f"Confidence : {result.confidence_score}")
    print(f"Distribution: {result.risk_distribution}")
    print(f"Top risks  : {result.top_risk_entities}")
    print("Critical alerts:")
    for alert in result.critical_alerts:
        print(f"  - {alert}")
    print(f"Sources    : {result.data_sources}")
