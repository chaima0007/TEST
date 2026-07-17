from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class SexEducationRightsEntity:
    entity_id: str
    name: str
    country: str
    abstinence_only_policy_harm_scale_score: float
    lgbtq_exclusion_curriculum_severity_score: float
    reproductive_health_information_denial_score: float
    school_dropout_unwanted_pregnancy_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_sex_education_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.abstinence_only_policy_harm_scale_score * 0.30
            + self.lgbtq_exclusion_curriculum_severity_score * 0.25
            + self.reproductive_health_information_denial_score * 0.25
            + self.school_dropout_unwanted_pregnancy_score * 0.20,
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
        self.estimated_sex_education_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class SexEducationRightsEngineResult:
    agent: str = "Sex Education Rights Engine Agent"
    domain: str = "sex_education_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_sex_education_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[SexEducationRightsEntity] = field(default_factory=list)

def run_sex_education_rights_engine() -> SexEducationRightsEngineResult:
    entities = [
        SexEducationRightsEntity(
            entity_id="SER-001",
            name="USA/États Conservateurs — Abstinence Only 25 États, Grossesses Ados 3x Plus & VIH Ados +60%",
            country="Amérique du Nord",
            abstinence_only_policy_harm_scale_score=95.0,
            lgbtq_exclusion_curriculum_severity_score=88.0,
            reproductive_health_information_denial_score=90.0,
            school_dropout_unwanted_pregnancy_score=85.0,
            primary_pattern="abstinence_only_policy_harm_scale",
        ),
        SexEducationRightsEntity(
            entity_id="SER-002",
            name="Nigeria/Afrique Sub-Sah. — Mariage Précoce, Zéro Sex-Ed Scolaire, VIH/SIDA Ados Non Informés",
            country="Afrique de l'Ouest",
            abstinence_only_policy_harm_scale_score=85.0,
            lgbtq_exclusion_curriculum_severity_score=88.0,
            reproductive_health_information_denial_score=92.0,
            school_dropout_unwanted_pregnancy_score=95.0,
            primary_pattern="school_dropout_unwanted_pregnancy",
        ),
        SexEducationRightsEntity(
            entity_id="SER-003",
            name="Philippines — Église Catholique Bloque Loi RH 2012, Zéro Sex-Ed & Avortement Illégal Toujours",
            country="Asie du Sud-Est",
            abstinence_only_policy_harm_scale_score=88.0,
            lgbtq_exclusion_curriculum_severity_score=85.0,
            reproductive_health_information_denial_score=92.0,
            school_dropout_unwanted_pregnancy_score=88.0,
            primary_pattern="reproductive_health_information_denial",
        ),
        SexEducationRightsEntity(
            entity_id="SER-004",
            name="Inde — Tabou Culturel, Grossesses Ados Rurales, Manuels Scolaires Expurgés & Honte Institutionnelle",
            country="Asie du Sud",
            abstinence_only_policy_harm_scale_score=85.0,
            lgbtq_exclusion_curriculum_severity_score=85.0,
            reproductive_health_information_denial_score=88.0,
            school_dropout_unwanted_pregnancy_score=90.0,
            primary_pattern="school_dropout_unwanted_pregnancy",
        ),
        SexEducationRightsEntity(
            entity_id="SER-005",
            name="Pologne — Loi Anti-LGBT 2019, Sex-Ed Interdite Écoles, Zones Sans Idéologie Genre & CEDH",
            country="Europe",
            abstinence_only_policy_harm_scale_score=55.0,
            lgbtq_exclusion_curriculum_severity_score=52.0,
            reproductive_health_information_denial_score=52.0,
            school_dropout_unwanted_pregnancy_score=50.0,
            primary_pattern="lgbtq_exclusion_curriculum_severity",
        ),
        SexEducationRightsEntity(
            entity_id="SER-006",
            name="Brésil — Programme Sex-Ed Supprimé Bolsonaro, Manuels Révisés Bible & Avortement Criminalisé",
            country="Amérique Latine",
            abstinence_only_policy_harm_scale_score=52.0,
            lgbtq_exclusion_curriculum_severity_score=55.0,
            reproductive_health_information_denial_score=50.0,
            school_dropout_unwanted_pregnancy_score=50.0,
            primary_pattern="abstinence_only_policy_harm_scale",
        ),
        SexEducationRightsEntity(
            entity_id="SER-007",
            name="SIECUS/UNESCO — Standards CSE Globaux 2018, Éducation Sexuelle Complète & Plaidoyer Droits",
            country="Global",
            abstinence_only_policy_harm_scale_score=22.0,
            lgbtq_exclusion_curriculum_severity_score=28.0,
            reproductive_health_information_denial_score=25.0,
            school_dropout_unwanted_pregnancy_score=30.0,
            primary_pattern="lgbtq_exclusion_curriculum_severity",
        ),
        SexEducationRightsEntity(
            entity_id="SER-008",
            name="ONU Femmes/IPPF — Droit Sex-Ed Complète, CEDAW Art.10, SDG 4 & Rapport CSE Global 2021",
            country="Global",
            abstinence_only_policy_harm_scale_score=4.0,
            lgbtq_exclusion_curriculum_severity_score=5.0,
            reproductive_health_information_denial_score=3.0,
            school_dropout_unwanted_pregnancy_score=6.0,
            primary_pattern="reproductive_health_information_denial",
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

    return SexEducationRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_sex_education_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "siecus_state_of_sex_education_united_states_report",
            "unesco_international_technical_guidance_sexuality_education_cse",
            "ippf_comprehensive_sexuality_education_rights_global_review",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_sex_education_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_sex_education_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
