from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class AcademicFreedomEducationRightsEntity:
    entity_id: str
    name: str
    country: str
    scholar_persecution_imprisonment_severity_score: float
    curriculum_ideological_control_censorship_scale_score: float
    university_autonomy_state_capture_score: float
    girls_education_access_denial_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_academic_freedom_education_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.scholar_persecution_imprisonment_severity_score * 0.30
            + self.curriculum_ideological_control_censorship_scale_score * 0.25
            + self.university_autonomy_state_capture_score * 0.25
            + self.girls_education_access_denial_gap_score * 0.20,
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
        self.estimated_academic_freedom_education_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class AcademicFreedomEducationRightsEngineResult:
    agent: str = "Academic Freedom Education Rights Engine Agent"
    domain: str = "academic_freedom_education_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_academic_freedom_education_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[AcademicFreedomEducationRightsEntity] = field(default_factory=list)


def run_academic_freedom_education_rights_engine() -> AcademicFreedomEducationRightsEngineResult:
    entities = [
        AcademicFreedomEducationRightsEntity(
            entity_id="AFE-001",
            name="Afghanistan/Taliban — Filles Bannies Éducation, Universités Femmes Fermées, Chercheurs Exilés & Manuels Brûlés",
            country="Afghanistan",
            scholar_persecution_imprisonment_severity_score=95.0,
            curriculum_ideological_control_censorship_scale_score=93.0,
            university_autonomy_state_capture_score=92.0,
            girls_education_access_denial_gap_score=91.0,
            primary_pattern="girls_education_access_denial_gap",
        ),
        AcademicFreedomEducationRightsEntity(
            entity_id="AFE-002",
            name="Chine — Uighur Scholars Disparus, Universités Idéologie Xi, Manuels Réécrits Histoire & Chercheurs Étrangers Espionnage",
            country="Chine",
            scholar_persecution_imprisonment_severity_score=92.0,
            curriculum_ideological_control_censorship_scale_score=90.0,
            university_autonomy_state_capture_score=89.0,
            girls_education_access_denial_gap_score=88.0,
            primary_pattern="curriculum_ideological_control_censorship_scale",
        ),
        AcademicFreedomEducationRightsEntity(
            entity_id="AFE-003",
            name="Turquie/Erdoğan — 6 000 Académiciens Virés Post-2016, Pétition Paix Signée→Procès, Universités Recteurs Nommés Gouvernement",
            country="Turquie",
            scholar_persecution_imprisonment_severity_score=89.0,
            curriculum_ideological_control_censorship_scale_score=87.0,
            university_autonomy_state_capture_score=86.0,
            girls_education_access_denial_gap_score=85.0,
            primary_pattern="scholar_persecution_imprisonment_severity",
        ),
        AcademicFreedomEducationRightsEntity(
            entity_id="AFE-004",
            name="Hongrie/Orbán — CEU Expulsé Budapest, Études Genre Interdites, Académie Sciences Sous Contrôle & Think Tanks Fermés",
            country="Hongrie",
            scholar_persecution_imprisonment_severity_score=86.0,
            curriculum_ideological_control_censorship_scale_score=84.0,
            university_autonomy_state_capture_score=83.0,
            girls_education_access_denial_gap_score=82.0,
            primary_pattern="university_autonomy_state_capture",
        ),
        AcademicFreedomEducationRightsEntity(
            entity_id="AFE-005",
            name="Russie/Belarus — Profs Anti-Guerre Licenciés, Étudiants Arrêtés Manifestations, Histoire Réécriture Ukrainienne & LGBTQ+ Curricula Bannis",
            country="Russie/Belarus",
            scholar_persecution_imprisonment_severity_score=57.0,
            curriculum_ideological_control_censorship_scale_score=55.0,
            university_autonomy_state_capture_score=54.0,
            girls_education_access_denial_gap_score=53.0,
            primary_pattern="scholar_persecution_imprisonment_severity",
        ),
        AcademicFreedomEducationRightsEntity(
            entity_id="AFE-006",
            name="USA/UK — DEI Programmes Attaqués, Campus Speech Codes, Donors Political Pressure & Academic Boycott Palestine",
            country="USA/UK",
            scholar_persecution_imprisonment_severity_score=54.0,
            curriculum_ideological_control_censorship_scale_score=52.0,
            university_autonomy_state_capture_score=51.0,
            girls_education_access_denial_gap_score=50.0,
            primary_pattern="university_autonomy_state_capture",
        ),
        AcademicFreedomEducationRightsEntity(
            entity_id="AFE-007",
            name="Scholars at Risk/SAR — Réseau Protection Académiciens Persécutés, Free to Think Report & Monitoring Attaques",
            country="Global",
            scholar_persecution_imprisonment_severity_score=27.0,
            curriculum_ideological_control_censorship_scale_score=26.0,
            university_autonomy_state_capture_score=25.0,
            girls_education_access_denial_gap_score=25.0,
            primary_pattern="scholar_persecution_imprisonment_severity",
        ),
        AcademicFreedomEducationRightsEntity(
            entity_id="AFE-008",
            name="ONU/Art.13 DESC — Droit Éducation, Recommandation UNESCO Chercheurs 1997 & SDG 4 Éducation Qualité",
            country="Global",
            scholar_persecution_imprisonment_severity_score=5.0,
            curriculum_ideological_control_censorship_scale_score=4.0,
            university_autonomy_state_capture_score=4.0,
            girls_education_access_denial_gap_score=4.0,
            primary_pattern="girls_education_access_denial_gap",
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

    return AcademicFreedomEducationRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_academic_freedom_education_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "scholars_at_risk_free_to_think_annual_report",
            "iff_academic_freedom_index_global_ranking",
            "hrw_education_rights_violations_documentation",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_academic_freedom_education_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_academic_freedom_education_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
