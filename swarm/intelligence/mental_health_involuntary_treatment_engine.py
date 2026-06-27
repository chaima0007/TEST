from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class MentalHealthInvoluntaryTreatmentEntity:
    entity_id: str
    name: str
    country: str
    involuntary_psychiatric_hospitalization_severity_score: float
    electroconvulsive_chemical_restraint_scale_score: float
    mental_health_criminal_justice_diversion_failure_score: float
    community_mental_health_service_absence_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_mental_health_involuntary_treatment_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.involuntary_psychiatric_hospitalization_severity_score * 0.30
            + self.electroconvulsive_chemical_restraint_scale_score * 0.25
            + self.mental_health_criminal_justice_diversion_failure_score * 0.25
            + self.community_mental_health_service_absence_deficit_gap_score * 0.20,
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
        self.estimated_mental_health_involuntary_treatment_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class MentalHealthInvoluntaryTreatmentEngineResult:
    agent: str = "Mental Health Involuntary Treatment Engine Agent"
    domain: str = "mental_health_involuntary_treatment"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_mental_health_involuntary_treatment_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[MentalHealthInvoluntaryTreatmentEntity] = field(default_factory=list)


def run_mental_health_involuntary_treatment_engine() -> MentalHealthInvoluntaryTreatmentEngineResult:
    entities = [
        MentalHealthInvoluntaryTreatmentEntity(
            entity_id="MHI-001",
            name="Russie/Belarus — Psychiatrie Punitive Dissidents, Serbsky Centre Abus, Internements Forcés Longue Durée & Médicaments Forcés",
            country="Russie/Belarus",
            involuntary_psychiatric_hospitalization_severity_score=95.0,
            electroconvulsive_chemical_restraint_scale_score=93.0,
            mental_health_criminal_justice_diversion_failure_score=92.0,
            community_mental_health_service_absence_deficit_gap_score=91.0,
            primary_pattern="involuntary_psychiatric_hospitalization_severity",
        ),
        MentalHealthInvoluntaryTreatmentEntity(
            entity_id="MHI-002",
            name="Chine — Ankang Hôpitaux Psychiatrie Police, Falun Gong Internements, Activistes Psychiatrisés & Conditions Inhumaines",
            country="Chine",
            involuntary_psychiatric_hospitalization_severity_score=92.0,
            electroconvulsive_chemical_restraint_scale_score=90.0,
            mental_health_criminal_justice_diversion_failure_score=89.0,
            community_mental_health_service_absence_deficit_gap_score=88.0,
            primary_pattern="electroconvulsive_chemical_restraint_scale",
        ),
        MentalHealthInvoluntaryTreatmentEntity(
            entity_id="MHI-003",
            name="USA — 250 000 Personnes Santé Mentale Incarcérées, Crisis Intervention Manque, Taser Deaths & Rikers Island",
            country="USA",
            involuntary_psychiatric_hospitalization_severity_score=89.0,
            electroconvulsive_chemical_restraint_scale_score=87.0,
            mental_health_criminal_justice_diversion_failure_score=86.0,
            community_mental_health_service_absence_deficit_gap_score=85.0,
            primary_pattern="mental_health_criminal_justice_diversion_failure",
        ),
        MentalHealthInvoluntaryTreatmentEntity(
            entity_id="MHI-004",
            name="Inde/Asie Sud — Chaînes Patients Hôpitaux, Exorcisme Pratiques, Stigmatisation Suicide Criminalisé & Soins Zéro Rural",
            country="Inde/Asie Sud",
            involuntary_psychiatric_hospitalization_severity_score=86.0,
            electroconvulsive_chemical_restraint_scale_score=84.0,
            mental_health_criminal_justice_diversion_failure_score=83.0,
            community_mental_health_service_absence_deficit_gap_score=82.0,
            primary_pattern="community_mental_health_service_absence_deficit_gap",
        ),
        MentalHealthInvoluntaryTreatmentEntity(
            entity_id="MHI-005",
            name="Europe — Involuntary Placement 5-20% Hospitalisations, Électrochocs Sans Consentement, Longue Détention & CRPD Violations",
            country="Europe",
            involuntary_psychiatric_hospitalization_severity_score=57.0,
            electroconvulsive_chemical_restraint_scale_score=55.0,
            mental_health_criminal_justice_diversion_failure_score=54.0,
            community_mental_health_service_absence_deficit_gap_score=53.0,
            primary_pattern="electroconvulsive_chemical_restraint_scale",
        ),
        MentalHealthInvoluntaryTreatmentEntity(
            entity_id="MHI-006",
            name="Afrique/MENA — Budget Santé Mentale 0.5%, Guérisseurs Traditionnels Seuls, Médicaments Indisponibles & Lois Coloniales",
            country="Afrique/MENA",
            involuntary_psychiatric_hospitalization_severity_score=54.0,
            electroconvulsive_chemical_restraint_scale_score=52.0,
            mental_health_criminal_justice_diversion_failure_score=51.0,
            community_mental_health_service_absence_deficit_gap_score=50.0,
            primary_pattern="community_mental_health_service_absence_deficit_gap",
        ),
        MentalHealthInvoluntaryTreatmentEntity(
            entity_id="MHI-007",
            name="WHO/MHRN — Global Mental Health Action Plan, Réseau Recherche, CRPD Art.12 Capacité Juridique & Standards Soins",
            country="Global",
            involuntary_psychiatric_hospitalization_severity_score=27.0,
            electroconvulsive_chemical_restraint_scale_score=26.0,
            mental_health_criminal_justice_diversion_failure_score=25.0,
            community_mental_health_service_absence_deficit_gap_score=25.0,
            primary_pattern="involuntary_psychiatric_hospitalization_severity",
        ),
        MentalHealthInvoluntaryTreatmentEntity(
            entity_id="MHI-008",
            name="ONU/CRPD Art.12-17 — Capacité Juridique, Intégrité Personne, Convention Torture & SDG 3.4 Santé Mentale",
            country="Global",
            involuntary_psychiatric_hospitalization_severity_score=5.0,
            electroconvulsive_chemical_restraint_scale_score=4.0,
            mental_health_criminal_justice_diversion_failure_score=4.0,
            community_mental_health_service_absence_deficit_gap_score=4.0,
            primary_pattern="mental_health_criminal_justice_diversion_failure",
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

    return MentalHealthInvoluntaryTreatmentEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_mental_health_involuntary_treatment_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "who_mental_health_atlas_global_report",
            "mental_disability_rights_international_behind_closed_doors",
            "mdri_human_rights_psychiatric_institutions_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_mental_health_involuntary_treatment_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_mental_health_involuntary_treatment_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
