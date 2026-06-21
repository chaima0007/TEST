from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class NeurodiversityRightsEntity:
    entity_id: str
    name: str
    country: str
    educational_inclusion_denial_severity_score: float
    employment_discrimination_neurodivergent_scale_score: float
    diagnostic_access_barrier_score: float
    stigma_criminalization_autistic_pattern_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_neurodiversity_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.educational_inclusion_denial_severity_score * 0.30
            + self.employment_discrimination_neurodivergent_scale_score * 0.25
            + self.diagnostic_access_barrier_score * 0.25
            + self.stigma_criminalization_autistic_pattern_score * 0.20,
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
        self.estimated_neurodiversity_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class NeurodiversityRightsEngineResult:
    agent: str = "Neurodiversity Rights Engine Agent"
    domain: str = "neurodiversity_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_neurodiversity_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[NeurodiversityRightsEntity] = field(default_factory=list)

def run_neurodiversity_rights_engine() -> NeurodiversityRightsEngineResult:
    entities = [
        NeurodiversityRightsEntity(
            entity_id="NDR-001",
            name="Chine — Autisme Institutionnalisé, Éducation Séparée & Stigmatisation Honte Familiale",
            country="Asie de l'Est",
            educational_inclusion_denial_severity_score=95.0,
            employment_discrimination_neurodivergent_scale_score=92.0,
            diagnostic_access_barrier_score=92.0,
            stigma_criminalization_autistic_pattern_score=95.0,
            primary_pattern="stigma_criminalization_autistic_pattern",
        ),
        NeurodiversityRightsEntity(
            entity_id="NDR-002",
            name="Inde — TDAH Non Reconnu Légalement, 40M Dyslexiques Sans Aménagement & Caste Diagnostic",
            country="Asie du Sud",
            educational_inclusion_denial_severity_score=92.0,
            employment_discrimination_neurodivergent_scale_score=88.0,
            diagnostic_access_barrier_score=95.0,
            stigma_criminalization_autistic_pattern_score=88.0,
            primary_pattern="diagnostic_access_barrier",
        ),
        NeurodiversityRightsEntity(
            entity_id="NDR-003",
            name="Afrique Sub-Sah. — Autisme = Sorcellerie, Exorcismes Forcés & Zéro École Inclusive",
            country="Afrique",
            educational_inclusion_denial_severity_score=92.0,
            employment_discrimination_neurodivergent_scale_score=85.0,
            diagnostic_access_barrier_score=88.0,
            stigma_criminalization_autistic_pattern_score=92.0,
            primary_pattern="educational_inclusion_denial_severity",
        ),
        NeurodiversityRightsEntity(
            entity_id="NDR-004",
            name="Brésil — 2,4M Autistes Sans Services, Classes Spéciales Ségrégatrices & INSS Bloqué",
            country="Amérique Latine",
            educational_inclusion_denial_severity_score=88.0,
            employment_discrimination_neurodivergent_scale_score=88.0,
            diagnostic_access_barrier_score=85.0,
            stigma_criminalization_autistic_pattern_score=85.0,
            primary_pattern="employment_discrimination_neurodivergent_scale",
        ),
        NeurodiversityRightsEntity(
            entity_id="NDR-005",
            name="USA — ADA Gaps TDAH Emploi, Surdiagnostic Minorités & Prison Pipeline Neurodivers",
            country="Amérique du Nord",
            educational_inclusion_denial_severity_score=52.0,
            employment_discrimination_neurodivergent_scale_score=55.0,
            diagnostic_access_barrier_score=52.0,
            stigma_criminalization_autistic_pattern_score=55.0,
            primary_pattern="employment_discrimination_neurodivergent_scale",
        ),
        NeurodiversityRightsEntity(
            entity_id="NDR-006",
            name="France — TDAH Sous-Diagnostiqué Adultes, Classe ULIS Insuffisante & Refus RQTH",
            country="Europe",
            educational_inclusion_denial_severity_score=52.0,
            employment_discrimination_neurodivergent_scale_score=52.0,
            diagnostic_access_barrier_score=55.0,
            stigma_criminalization_autistic_pattern_score=50.0,
            primary_pattern="diagnostic_access_barrier",
        ),
        NeurodiversityRightsEntity(
            entity_id="NDR-007",
            name="Autistic Self Advocacy Network/ASAN — Neurodiversité Droits, CRPD Art.24 & Inclusion",
            country="Global",
            educational_inclusion_denial_severity_score=22.0,
            employment_discrimination_neurodivergent_scale_score=28.0,
            diagnostic_access_barrier_score=25.0,
            stigma_criminalization_autistic_pattern_score=30.0,
            primary_pattern="stigma_criminalization_autistic_pattern",
        ),
        NeurodiversityRightsEntity(
            entity_id="NDR-008",
            name="ONU/CDPH — Convention Droits Personnes Handicap Art.24, SDG 4 Éducation Inclusive",
            country="Global",
            educational_inclusion_denial_severity_score=4.0,
            employment_discrimination_neurodivergent_scale_score=5.0,
            diagnostic_access_barrier_score=3.0,
            stigma_criminalization_autistic_pattern_score=6.0,
            primary_pattern="educational_inclusion_denial_severity",
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

    return NeurodiversityRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_neurodiversity_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "autistic_self_advocacy_network_asan_neurodiversity_rights_framework",
            "un_crpd_convention_rights_persons_disabilities_article24_inclusive_education",
            "lancet_psychiatry_adhd_autism_global_prevalence_access_report_2023",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_neurodiversity_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_neurodiversity_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
