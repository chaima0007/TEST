from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class MentalHealthRightsEntity:
    entity_id: str
    name: str
    country: str
    forced_institutionalization_coercion_severity_score: float
    psychiatric_treatment_without_consent_scale_score: float
    mental_health_service_access_gap_score: float
    stigma_discrimination_mental_health_barrier_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_mental_health_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.forced_institutionalization_coercion_severity_score * 0.30
            + self.psychiatric_treatment_without_consent_scale_score * 0.25
            + self.mental_health_service_access_gap_score * 0.25
            + self.stigma_discrimination_mental_health_barrier_score * 0.20,
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
            entity_id="MHR-001",
            name="Indonésie — 18 000 Personnes Enchaînées Pasung, Hôpitaux Surpeuplés & Zéro Psychiatres Ruraux",
            country="Indonésie",
            forced_institutionalization_coercion_severity_score=96.0,
            psychiatric_treatment_without_consent_scale_score=94.0,
            mental_health_service_access_gap_score=93.0,
            stigma_discrimination_mental_health_barrier_score=92.0,
            primary_pattern="forced_institutionalization_coercion_severity",
        ),
        MentalHealthRightsEntity(
            entity_id="MHR-002",
            name="Inde — 150M Besoins Santé Mentale, 0,3 Psychiatres/100k, Internement Forcé Famille & ECT Mineurs",
            country="Inde",
            forced_institutionalization_coercion_severity_score=93.0,
            psychiatric_treatment_without_consent_scale_score=91.0,
            mental_health_service_access_gap_score=90.0,
            stigma_discrimination_mental_health_barrier_score=89.0,
            primary_pattern="mental_health_service_access_gap",
        ),
        MentalHealthRightsEntity(
            entity_id="MHR-003",
            name="Afrique Sub-Saharienne — 1 Psychiatre/Million, Guérisseurs Traditionnels Seule Option & Chaînes Thérapeutiques",
            country="Afrique Sub-Saharienne",
            forced_institutionalization_coercion_severity_score=90.0,
            psychiatric_treatment_without_consent_scale_score=87.0,
            mental_health_service_access_gap_score=88.0,
            stigma_discrimination_mental_health_barrier_score=86.0,
            primary_pattern="mental_health_service_access_gap",
        ),
        MentalHealthRightsEntity(
            entity_id="MHR-004",
            name="Russie — Hôpitaux Psychiatriques Punitifs Héritage Soviétique, Dissidents Internés & Zéro Consentement",
            country="Russie",
            forced_institutionalization_coercion_severity_score=87.0,
            psychiatric_treatment_without_consent_scale_score=85.0,
            mental_health_service_access_gap_score=84.0,
            stigma_discrimination_mental_health_barrier_score=83.0,
            primary_pattern="forced_institutionalization_coercion_severity",
        ),
        MentalHealthRightsEntity(
            entity_id="MHR-005",
            name="USA — 500k Sans Abri Troubles Mentaux, Prisons Hôpitaux Psychiatrie, Isolement Cellulaire",
            country="USA",
            forced_institutionalization_coercion_severity_score=56.0,
            psychiatric_treatment_without_consent_scale_score=54.0,
            mental_health_service_access_gap_score=53.0,
            stigma_discrimination_mental_health_barrier_score=52.0,
            primary_pattern="forced_institutionalization_coercion_severity",
        ),
        MentalHealthRightsEntity(
            entity_id="MHR-006",
            name="Europe — ECT Sans Consentement Légal Plusieurs Pays, Contention Physique & Gaps Désinstitutionnalisation",
            country="Europe",
            forced_institutionalization_coercion_severity_score=53.0,
            psychiatric_treatment_without_consent_scale_score=51.0,
            mental_health_service_access_gap_score=50.0,
            stigma_discrimination_mental_health_barrier_score=49.0,
            primary_pattern="psychiatric_treatment_without_consent_scale",
        ),
        MentalHealthRightsEntity(
            entity_id="MHR-007",
            name="WNUSP/MIND — Réforme Psychiatrie, CRPD Article 12 & Mouvement Survivants Psychiatriques",
            country="Global",
            forced_institutionalization_coercion_severity_score=27.0,
            psychiatric_treatment_without_consent_scale_score=26.0,
            mental_health_service_access_gap_score=25.0,
            stigma_discrimination_mental_health_barrier_score=26.0,
            primary_pattern="forced_institutionalization_coercion_severity",
        ),
        MentalHealthRightsEntity(
            entity_id="MHR-008",
            name="ONU/CRPD — Article 12 Capacité Légale Égale, Rapporteur Santé Mentale & SDG 3.4 Bien-Être Mental",
            country="Global",
            forced_institutionalization_coercion_severity_score=4.0,
            psychiatric_treatment_without_consent_scale_score=4.0,
            mental_health_service_access_gap_score=5.0,
            stigma_discrimination_mental_health_barrier_score=4.0,
            primary_pattern="mental_health_service_access_gap",
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
