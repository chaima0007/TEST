from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class MentalHealthRightsPsychiatricViolenceEntity:
    entity_id: str
    name: str
    country: str
    involuntary_commitment_abuse_score: float
    psychiatric_coercion_treatment_without_consent_score: float
    mental_health_legal_protection_deficit_score: float
    community_care_absence_institutionalization_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_mental_health_rights_psychiatric_violence_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.involuntary_commitment_abuse_score * 0.30
            + self.psychiatric_coercion_treatment_without_consent_score * 0.25
            + self.mental_health_legal_protection_deficit_score * 0.25
            + self.community_care_absence_institutionalization_score * 0.20,
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
        self.estimated_mental_health_rights_psychiatric_violence_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class MentalHealthRightsPsychiatricViolenceEngineResult:
    agent: str = "Mental Health Rights Psychiatric Violence Engine Agent"
    domain: str = "mental_health_rights_psychiatric_violence"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_mental_health_rights_psychiatric_violence_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[MentalHealthRightsPsychiatricViolenceEntity] = field(default_factory=list)


def run_mental_health_rights_psychiatric_violence_engine() -> MentalHealthRightsPsychiatricViolenceEngineResult:
    entities = [
        MentalHealthRightsPsychiatricViolenceEntity(
            entity_id="MHRPV-001",
            name="Russie/Psychiatrie Punitive — Internements Politiques Dissidents, Hôpitaux Psychiatriques Répression & Diagnostics Falsifiés",
            country="Russie",
            involuntary_commitment_abuse_score=90.0,
            psychiatric_coercion_treatment_without_consent_score=88.0,
            mental_health_legal_protection_deficit_score=85.0,
            community_care_absence_institutionalization_score=82.0,
            primary_pattern="involuntary_commitment_abuse",
        ),
        MentalHealthRightsPsychiatricViolenceEntity(
            entity_id="MHRPV-002",
            name="Chine/Ankang Politique — Internements Psychiatriques Militants, Falun Gong Forcés Hôpitaux & Absence Recours Légaux",
            country="Chine",
            involuntary_commitment_abuse_score=88.0,
            psychiatric_coercion_treatment_without_consent_score=85.0,
            mental_health_legal_protection_deficit_score=90.0,
            community_care_absence_institutionalization_score=80.0,
            primary_pattern="mental_health_legal_protection_deficit",
        ),
        MentalHealthRightsPsychiatricViolenceEntity(
            entity_id="MHRPV-003",
            name="Inde/Asiles Coloniaux — Institutions Surpeuplées Héritées Colonialisme, Mauvais Traitements Chroniques & Loi Santé Mentale Lacunaire",
            country="Inde",
            involuntary_commitment_abuse_score=82.0,
            psychiatric_coercion_treatment_without_consent_score=80.0,
            mental_health_legal_protection_deficit_score=78.0,
            community_care_absence_institutionalization_score=85.0,
            primary_pattern="community_care_absence_institutionalization",
        ),
        MentalHealthRightsPsychiatricViolenceEntity(
            entity_id="MHRPV-004",
            name="USA/Involuntary Hold 5150 — Hospitalisations Forcées Sans Consentement Éclairé, Criminalisation Maladie Mentale & Incarcération vs Soins",
            country="USA",
            involuntary_commitment_abuse_score=72.0,
            psychiatric_coercion_treatment_without_consent_score=75.0,
            mental_health_legal_protection_deficit_score=68.0,
            community_care_absence_institutionalization_score=70.0,
            primary_pattern="psychiatric_coercion_treatment_without_consent",
        ),
        MentalHealthRightsPsychiatricViolenceEntity(
            entity_id="MHRPV-005",
            name="Brésil/Réforme Psychiatrique Inachevée — Désinstitutionnalisation Partielle, CAPS Sous-Financés & Retour Hospitalisations Longue Durée",
            country="Brésil",
            involuntary_commitment_abuse_score=52.0,
            psychiatric_coercion_treatment_without_consent_score=55.0,
            mental_health_legal_protection_deficit_score=48.0,
            community_care_absence_institutionalization_score=50.0,
            primary_pattern="psychiatric_coercion_treatment_without_consent",
        ),
        MentalHealthRightsPsychiatricViolenceEntity(
            entity_id="MHRPV-006",
            name="Nigeria/Psychiatrie Sous-Financée — 0.1% Budget Santé Santé Mentale, Recours Tradipraticiens Forcés & Absence Législation Protectrice",
            country="Nigeria",
            involuntary_commitment_abuse_score=48.0,
            psychiatric_coercion_treatment_without_consent_score=50.0,
            mental_health_legal_protection_deficit_score=52.0,
            community_care_absence_institutionalization_score=45.0,
            primary_pattern="mental_health_legal_protection_deficit",
        ),
        MentalHealthRightsPsychiatricViolenceEntity(
            entity_id="MHRPV-007",
            name="France/HO Hospitalisations Sans Consentement — Hausse Soins Contraints, Contrôle Judiciaire Insuffisant & Droits Patients Partiels",
            country="France",
            involuntary_commitment_abuse_score=28.0,
            psychiatric_coercion_treatment_without_consent_score=30.0,
            mental_health_legal_protection_deficit_score=25.0,
            community_care_absence_institutionalization_score=22.0,
            primary_pattern="psychiatric_coercion_treatment_without_consent",
        ),
        MentalHealthRightsPsychiatricViolenceEntity(
            entity_id="MHRPV-008",
            name="Finlande/Open Dialogue Modèle — Approche Dialogique Sans Contention, Résultats Schizophrénie Excellents & Référence Mondiale",
            country="Finlande",
            involuntary_commitment_abuse_score=4.0,
            psychiatric_coercion_treatment_without_consent_score=5.0,
            mental_health_legal_protection_deficit_score=3.0,
            community_care_absence_institutionalization_score=6.0,
            primary_pattern="involuntary_commitment_abuse",
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

    return MentalHealthRightsPsychiatricViolenceEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_mental_health_rights_psychiatric_violence_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "who_mental_health_atlas_2023",
            "disability_rights_international_psychiatric_report",
            "mad_in_america_forced_treatment_database",
            "mental_health_europe_annual_report_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_mental_health_rights_psychiatric_violence_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_mental_health_rights_psychiatric_violence_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
