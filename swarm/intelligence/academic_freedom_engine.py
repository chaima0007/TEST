from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class AcademicFreedomEntity:
    entity_id: str
    name: str
    country: str
    scholar_arrest_persecution_score: float
    curriculum_state_interference_score: float
    campus_surveillance_control_score: float
    international_collaboration_restriction_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_academic_freedom_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.scholar_arrest_persecution_score * 0.30
            + self.curriculum_state_interference_score * 0.25
            + self.campus_surveillance_control_score * 0.25
            + self.international_collaboration_restriction_score * 0.20,
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
        self.estimated_academic_freedom_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class AcademicFreedomEngineResult:
    agent: str = "Academic Freedom Engine Agent"
    domain: str = "academic_freedom"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_academic_freedom_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[AcademicFreedomEntity] = field(default_factory=list)

def run_academic_freedom_engine() -> AcademicFreedomEngineResult:
    entities = [
        AcademicFreedomEntity(
            entity_id="AF-001",
            name="Chine — Purges Académiques Xinjiang/Tibet, Surveillance Campus & Interdiction Pensée Critique",
            country="Asie du Nord-Est",
            scholar_arrest_persecution_score=95.0,
            curriculum_state_interference_score=92.0,
            campus_surveillance_control_score=95.0,
            international_collaboration_restriction_score=88.0,
            primary_pattern="campus_surveillance_control",
        ),
        AcademicFreedomEntity(
            entity_id="AF-002",
            name="Iran — Épurations Universités Post-2022, Arrestations Professeurs & Islamisation Curricula",
            country="Moyen-Orient",
            scholar_arrest_persecution_score=92.0,
            curriculum_state_interference_score=88.0,
            campus_surveillance_control_score=85.0,
            international_collaboration_restriction_score=90.0,
            primary_pattern="scholar_arrest_persecution",
        ),
        AcademicFreedomEntity(
            entity_id="AF-003",
            name="Turquie — 6000 Académiciens Licenciés Post-2016, Pétition Paix & Passeports Confisqués",
            country="Europe/Moyen-Orient",
            scholar_arrest_persecution_score=88.0,
            curriculum_state_interference_score=82.0,
            campus_surveillance_control_score=80.0,
            international_collaboration_restriction_score=88.0,
            primary_pattern="scholar_arrest_persecution",
        ),
        AcademicFreedomEntity(
            entity_id="AF-004",
            name="Russie — Exode Scientifiques Post-Ukraine, Censure Syllabi & Propagande Obligatoire",
            country="Europe de l'Est",
            scholar_arrest_persecution_score=82.0,
            curriculum_state_interference_score=85.0,
            campus_surveillance_control_score=80.0,
            international_collaboration_restriction_score=82.0,
            primary_pattern="curriculum_state_interference",
        ),
        AcademicFreedomEntity(
            entity_id="AF-005",
            name="USA — Lois Anti-DEI, Interdictions Livres Universités & Pressions Politique sur Campus",
            country="Amérique du Nord",
            scholar_arrest_persecution_score=52.0,
            curriculum_state_interference_score=58.0,
            campus_surveillance_control_score=48.0,
            international_collaboration_restriction_score=52.0,
            primary_pattern="curriculum_state_interference",
        ),
        AcademicFreedomEntity(
            entity_id="AF-006",
            name="Hongrie/Orbán — CEU Expulsée, Lois Gender Studies & Contrôle Financement Recherche",
            country="Europe",
            scholar_arrest_persecution_score=48.0,
            curriculum_state_interference_score=55.0,
            campus_surveillance_control_score=50.0,
            international_collaboration_restriction_score=48.0,
            primary_pattern="curriculum_state_interference",
        ),
        AcademicFreedomEntity(
            entity_id="AF-007",
            name="Scholars at Risk — Réseau 600+ Universités, Cas Documentés & Plaidoyer Protection",
            country="Global",
            scholar_arrest_persecution_score=22.0,
            curriculum_state_interference_score=25.0,
            campus_surveillance_control_score=28.0,
            international_collaboration_restriction_score=30.0,
            primary_pattern="scholar_arrest_persecution",
        ),
        AcademicFreedomEntity(
            entity_id="AF-008",
            name="ONU/UNESCO — Recommandation Liberté Académique 1997, Suivi & Mécanismes Rapport",
            country="Global",
            scholar_arrest_persecution_score=4.0,
            curriculum_state_interference_score=5.0,
            campus_surveillance_control_score=3.0,
            international_collaboration_restriction_score=6.0,
            primary_pattern="international_collaboration_restriction",
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

    return AcademicFreedomEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_academic_freedom_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "scholars_at_risk_network_academic_freedom_monitoring_project",
            "academic_freedom_index_global_public_policy_institute_report",
            "human_rights_watch_university_repression_global_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_academic_freedom_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_academic_freedom_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
