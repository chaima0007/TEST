from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class MentalHealthRightsEntity:
    entity_id: str
    name: str
    country: str
    forced_institutionalization_score: float
    treatment_access_denial_score: float
    legal_capacity_deprivation_score: float
    stigma_discrimination_barrier_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_mental_health_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.forced_institutionalization_score * 0.30
            + self.treatment_access_denial_score * 0.25
            + self.legal_capacity_deprivation_score * 0.25
            + self.stigma_discrimination_barrier_score * 0.20,
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
        self.estimated_mental_health_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class MentalHealthRightsEngineResult:
    agent: str = "Mental Health Rights Engine Agent"
    domain: str = "mental_health_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_mental_health_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[MentalHealthRightsEntity] = field(default_factory=list)

def run_mental_health_rights_engine() -> MentalHealthRightsEngineResult:
    entities = [
        MentalHealthRightsEntity(
            entity_id="MH-001",
            name="Russie — Psychiatrie Punitive Post-Soviétique, Internements Forcés Opposants & CRPD Non Ratifié",
            country="Europe de l'Est",
            forced_institutionalization_score=95.0,
            treatment_access_denial_score=92.0,
            legal_capacity_deprivation_score=95.0,
            stigma_discrimination_barrier_score=90.0,
            primary_pattern="forced_institutionalization",
        ),
        MentalHealthRightsEntity(
            entity_id="MH-002",
            name="Inde — 7M Institutionnalisés, Dargahs Chaînes, Loi 2017 Non Appliquée & CRPD Violations",
            country="Asie du Sud",
            forced_institutionalization_score=90.0,
            treatment_access_denial_score=92.0,
            legal_capacity_deprivation_score=88.0,
            stigma_discrimination_barrier_score=92.0,
            primary_pattern="treatment_access_denial",
        ),
        MentalHealthRightsEntity(
            entity_id="MH-003",
            name="Ghana/Nigeria — Maisons Prière Patients Enchaînés, 10K+ Captifs & Lois Coloniales",
            country="Afrique de l'Ouest",
            forced_institutionalization_score=88.0,
            treatment_access_denial_score=90.0,
            legal_capacity_deprivation_score=85.0,
            stigma_discrimination_barrier_score=90.0,
            primary_pattern="treatment_access_denial",
        ),
        MentalHealthRightsEntity(
            entity_id="MH-004",
            name="USA — 180K Institutionnalisés, Olmstead Non Appliqué, Prisons Remplacent Asiles",
            country="Amérique du Nord",
            forced_institutionalization_score=85.0,
            treatment_access_denial_score=85.0,
            legal_capacity_deprivation_score=88.0,
            stigma_discrimination_barrier_score=82.0,
            primary_pattern="legal_capacity_deprivation",
        ),
        MentalHealthRightsEntity(
            entity_id="MH-005",
            name="UE/Malte & Hongrie — Tutelle Systémique, Capacité Juridique Restreinte & CRPD Art.12",
            country="Europe",
            forced_institutionalization_score=55.0,
            treatment_access_denial_score=52.0,
            legal_capacity_deprivation_score=58.0,
            stigma_discrimination_barrier_score=50.0,
            primary_pattern="legal_capacity_deprivation",
        ),
        MentalHealthRightsEntity(
            entity_id="MH-006",
            name="Japon — Hospitalisations Involontaires 300+ Jours Moy., Isolement Systémique & CRPD",
            country="Asie de l'Est",
            forced_institutionalization_score=52.0,
            treatment_access_denial_score=48.0,
            legal_capacity_deprivation_score=50.0,
            stigma_discrimination_barrier_score=48.0,
            primary_pattern="forced_institutionalization",
        ),
        MentalHealthRightsEntity(
            entity_id="MH-007",
            name="OMS/IASC — MHPSS Standards, Lignes Directrices Désinstitutionnalisation & Monitoring",
            country="Global",
            forced_institutionalization_score=22.0,
            treatment_access_denial_score=28.0,
            legal_capacity_deprivation_score=25.0,
            stigma_discrimination_barrier_score=30.0,
            primary_pattern="stigma_discrimination_barrier",
        ),
        MentalHealthRightsEntity(
            entity_id="MH-008",
            name="ONU/CRPD — Art.12 Capacité Juridique Égale, Art.14 Liberté & Rapporteur Spécial Handicap",
            country="Global",
            forced_institutionalization_score=4.0,
            treatment_access_denial_score=5.0,
            legal_capacity_deprivation_score=3.0,
            stigma_discrimination_barrier_score=6.0,
            primary_pattern="stigma_discrimination_barrier",
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

    return MentalHealthRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_mental_health_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "who_mental_health_atlas_global_psychiatry_resources",
            "hrw_disability_rights_mental_health_institutionalization_report",
            "crpd_committee_general_comment_1_legal_capacity_article12",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_mental_health_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_mental_health_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
