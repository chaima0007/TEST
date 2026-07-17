from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class MenopauseWorkplaceRightsEntity:
    entity_id: str
    name: str
    country: str
    workplace_symptom_accommodation_denial_score: float
    age_gender_intersectional_discrimination_scale_score: float
    medical_recognition_menopause_disability_gap_score: float
    career_penalty_forced_exit_pattern_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_menopause_workplace_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.workplace_symptom_accommodation_denial_score * 0.30
            + self.age_gender_intersectional_discrimination_scale_score * 0.25
            + self.medical_recognition_menopause_disability_gap_score * 0.25
            + self.career_penalty_forced_exit_pattern_score * 0.20,
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
        self.estimated_menopause_workplace_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class MenopauseWorkplaceRightsEngineResult:
    agent: str = "Menopause Workplace Rights Engine Agent"
    domain: str = "menopause_workplace_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.82
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_menopause_workplace_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[MenopauseWorkplaceRightsEntity] = field(default_factory=list)

def run_menopause_workplace_rights_engine() -> MenopauseWorkplaceRightsEngineResult:
    entities = [
        MenopauseWorkplaceRightsEntity(
            entity_id="MWR-001",
            name="Japon — Ménopause Tabou Total, Femmes Poussées Vers Retraite Anticipée & Karoshi Femmes",
            country="Asie de l'Est",
            workplace_symptom_accommodation_denial_score=95.0,
            age_gender_intersectional_discrimination_scale_score=95.0,
            medical_recognition_menopause_disability_gap_score=92.0,
            career_penalty_forced_exit_pattern_score=92.0,
            primary_pattern="age_gender_intersectional_discrimination_scale",
        ),
        MenopauseWorkplaceRightsEntity(
            entity_id="MWR-002",
            name="Corée du Sud — 84% Femmes Cachent Symptômes Travail, Licenciement Déguisé & Silence Médical",
            country="Asie de l'Est",
            workplace_symptom_accommodation_denial_score=92.0,
            age_gender_intersectional_discrimination_scale_score=90.0,
            medical_recognition_menopause_disability_gap_score=88.0,
            career_penalty_forced_exit_pattern_score=90.0,
            primary_pattern="career_penalty_forced_exit_pattern",
        ),
        MenopauseWorkplaceRightsEntity(
            entity_id="MWR-003",
            name="Inde — Ménopause = Honte, Femmes Rurales Sans Accès THS, Discrimination RH & ESIC Gap",
            country="Asie du Sud",
            workplace_symptom_accommodation_denial_score=90.0,
            age_gender_intersectional_discrimination_scale_score=88.0,
            medical_recognition_menopause_disability_gap_score=92.0,
            career_penalty_forced_exit_pattern_score=85.0,
            primary_pattern="medical_recognition_menopause_disability_gap",
        ),
        MenopauseWorkplaceRightsEntity(
            entity_id="MWR-004",
            name="Afrique Sub-Sah. — Zéro THS Accessible, Ménopause Précoce Non Traitée & Exclusion Emploi",
            country="Afrique",
            workplace_symptom_accommodation_denial_score=88.0,
            age_gender_intersectional_discrimination_scale_score=85.0,
            medical_recognition_menopause_disability_gap_score=88.0,
            career_penalty_forced_exit_pattern_score=88.0,
            primary_pattern="workplace_symptom_accommodation_denial",
        ),
        MenopauseWorkplaceRightsEntity(
            entity_id="MWR-005",
            name="USA — Pas de Protection Légale Ménopause, 1M Femmes/An Quittent Emploi & ADA Gap",
            country="Amérique du Nord",
            workplace_symptom_accommodation_denial_score=55.0,
            age_gender_intersectional_discrimination_scale_score=52.0,
            medical_recognition_menopause_disability_gap_score=55.0,
            career_penalty_forced_exit_pattern_score=52.0,
            primary_pattern="workplace_symptom_accommodation_denial",
        ),
        MenopauseWorkplaceRightsEntity(
            entity_id="MWR-006",
            name="France — Ménopause Invisible RH, 70% Femmes Sans Aménagement & Égalité Pro Lacunaire",
            country="Europe",
            workplace_symptom_accommodation_denial_score=52.0,
            age_gender_intersectional_discrimination_scale_score=52.0,
            medical_recognition_menopause_disability_gap_score=50.0,
            career_penalty_forced_exit_pattern_score=55.0,
            primary_pattern="career_penalty_forced_exit_pattern",
        ),
        MenopauseWorkplaceRightsEntity(
            entity_id="MWR-007",
            name="UK Menopause Taskforce/CIPD — Politiques Lieu Travail, Flexibilité & Loi Égalité 2010",
            country="Europe",
            workplace_symptom_accommodation_denial_score=22.0,
            age_gender_intersectional_discrimination_scale_score=28.0,
            medical_recognition_menopause_disability_gap_score=25.0,
            career_penalty_forced_exit_pattern_score=30.0,
            primary_pattern="age_gender_intersectional_discrimination_scale",
        ),
        MenopauseWorkplaceRightsEntity(
            entity_id="MWR-008",
            name="OMS/ONU Femmes — Santé Reproductive Femmes 40-55, CEDAW Art.11 Emploi & SDG 5",
            country="Global",
            workplace_symptom_accommodation_denial_score=4.0,
            age_gender_intersectional_discrimination_scale_score=5.0,
            medical_recognition_menopause_disability_gap_score=3.0,
            career_penalty_forced_exit_pattern_score=6.0,
            primary_pattern="medical_recognition_menopause_disability_gap",
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

    return MenopauseWorkplaceRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_menopause_workplace_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "cipd_menopause_workplace_policy_uk_survey_2023",
            "british_menopause_society_employment_discrimination_health_report",
            "un_women_cedaw_reproductive_health_employment_rights_review",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_menopause_workplace_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_menopause_workplace_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
