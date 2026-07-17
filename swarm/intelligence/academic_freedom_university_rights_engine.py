from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class AcademicFreedomUniversityRightsEntity:
    entity_id: str
    name: str
    country: str
    scholar_arrest_exile_persecution_severity_score: float
    curriculum_ideology_state_control_scale_score: float
    research_publication_censorship_score: float
    university_autonomy_governance_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_academic_freedom_university_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.scholar_arrest_exile_persecution_severity_score * 0.30
            + self.curriculum_ideology_state_control_scale_score * 0.25
            + self.research_publication_censorship_score * 0.25
            + self.university_autonomy_governance_deficit_gap_score * 0.20,
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
        self.estimated_academic_freedom_university_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class AcademicFreedomUniversityRightsEngineResult:
    agent: str = "Academic Freedom University Rights Engine Agent"
    domain: str = "academic_freedom_university_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_academic_freedom_university_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[AcademicFreedomUniversityRightsEntity] = field(default_factory=list)


def run_academic_freedom_university_rights_engine() -> AcademicFreedomUniversityRightsEngineResult:
    entities = [
        AcademicFreedomUniversityRightsEntity(
            entity_id="AFU-001",
            name="Chine/Confucius Instituts Censure — Surveillance Étudiants Étrangers, Auto-Censure Universités Mondiales & Propagande Xi dans Campus Internationaux",
            country="Chine",
            scholar_arrest_exile_persecution_severity_score=93.0,
            curriculum_ideology_state_control_scale_score=92.0,
            research_publication_censorship_score=91.0,
            university_autonomy_governance_deficit_gap_score=90.0,
            primary_pattern="curriculum_ideology_state_control_scale",
        ),
        AcademicFreedomUniversityRightsEntity(
            entity_id="AFU-002",
            name="Turkménistan/Universités Contrôle Total Idéologique — Manuels Réécrits Culte Dirigeant, Chercheurs Interdits Voyager & Internet Académique Bloqué",
            country="Turkménistan",
            scholar_arrest_exile_persecution_severity_score=91.0,
            curriculum_ideology_state_control_scale_score=93.0,
            research_publication_censorship_score=90.0,
            university_autonomy_governance_deficit_gap_score=92.0,
            primary_pattern="university_autonomy_governance_deficit_gap",
        ),
        AcademicFreedomUniversityRightsEntity(
            entity_id="AFU-003",
            name="Iran/Université Épurations Professeures — 800 Académiciennes Exclues 2023, Arrestations Protestants Campus & Interdiction Sciences Politiques Femmes",
            country="Iran",
            scholar_arrest_exile_persecution_severity_score=90.0,
            curriculum_ideology_state_control_scale_score=88.0,
            research_publication_censorship_score=87.0,
            university_autonomy_governance_deficit_gap_score=89.0,
            primary_pattern="scholar_arrest_exile_persecution_severity",
        ),
        AcademicFreedomUniversityRightsEntity(
            entity_id="AFU-004",
            name="Turquie/3 500 Académiciens Révoqués Post-Coup — Décrets Urgence Suppressions, Passeports Confisqués Chercheurs & Pétition Paix 2016 Procès Masse",
            country="Turquie",
            scholar_arrest_exile_persecution_severity_score=88.0,
            curriculum_ideology_state_control_scale_score=85.0,
            research_publication_censorship_score=84.0,
            university_autonomy_governance_deficit_gap_score=87.0,
            primary_pattern="scholar_arrest_exile_persecution_severity",
        ),
        AcademicFreedomUniversityRightsEntity(
            entity_id="AFU-005",
            name="Hongrie/CEU Expulsion Budapest Orbán — Central European University Forcée Vienne 2019, Études Genre Interdites & ONG Académiques Taxées",
            country="Hongrie",
            scholar_arrest_exile_persecution_severity_score=57.0,
            curriculum_ideology_state_control_scale_score=58.0,
            research_publication_censorship_score=55.0,
            university_autonomy_governance_deficit_gap_score=59.0,
            primary_pattern="university_autonomy_governance_deficit_gap",
        ),
        AcademicFreedomUniversityRightsEntity(
            entity_id="AFU-006",
            name="Russie/Académiciens Anti-Guerre Radiés — 1 400 Chercheurs Exilés Post-2022, Poursuites Discrédit Scientifique & Censure Publications Ukraine",
            country="Russie",
            scholar_arrest_exile_persecution_severity_score=55.0,
            curriculum_ideology_state_control_scale_score=56.0,
            research_publication_censorship_score=57.0,
            university_autonomy_governance_deficit_gap_score=54.0,
            primary_pattern="research_publication_censorship",
        ),
        AcademicFreedomUniversityRightsEntity(
            entity_id="AFU-007",
            name="Scholars at Risk/AAUP Network — Monitoring Attaques Académiciens Worldwide, Free to Think Report Annuel & Réseau Accueil Chercheurs Persécutés",
            country="Global",
            scholar_arrest_exile_persecution_severity_score=27.0,
            curriculum_ideology_state_control_scale_score=26.0,
            research_publication_censorship_score=25.0,
            university_autonomy_governance_deficit_gap_score=26.0,
            primary_pattern="scholar_arrest_exile_persecution_severity",
        ),
        AcademicFreedomUniversityRightsEntity(
            entity_id="AFU-008",
            name="ONU/UNESCO Recommandation Enseignement Supérieur 1997 — Cadre Normatif Liberté Académique, Autonomie Universitaire & Protection Statut Enseignants",
            country="Global",
            scholar_arrest_exile_persecution_severity_score=5.0,
            curriculum_ideology_state_control_scale_score=5.0,
            research_publication_censorship_score=5.0,
            university_autonomy_governance_deficit_gap_score=5.0,
            primary_pattern="university_autonomy_governance_deficit_gap",
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

    return AcademicFreedomUniversityRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_academic_freedom_university_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "scholars_at_risk_free_to_think_annual_report",
            "academic_freedom_index_global_public_policy_institute",
            "iff_university_autonomy_scorecard_worldwide",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_academic_freedom_university_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_academic_freedom_university_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
