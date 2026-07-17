from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class HumanRightsEducationEntity:
    entity_id: str
    name: str
    country: str
    curriculum_obstruction_score: float
    civil_society_repression_score: float
    access_denial_marginalized_score: float
    international_framework_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_human_rights_education_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.curriculum_obstruction_score * 0.30
            + self.civil_society_repression_score * 0.25
            + self.access_denial_marginalized_score * 0.25
            + self.international_framework_gap_score * 0.20,
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
        self.estimated_human_rights_education_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class HumanRightsEducationEngineResult:
    agent: str = "Human Rights Education Engine Agent"
    domain: str = "human_rights_education"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.83
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_human_rights_education_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[HumanRightsEducationEntity] = field(default_factory=list)

def run_human_rights_education_engine() -> HumanRightsEducationEngineResult:
    entities = [
        HumanRightsEducationEntity(
            entity_id="HRE-001",
            name="Chine — Éducation Patriotique Obligatoire, Suppression Contenu Droits & Contrôle Internet",
            country="Asie du Nord-Est",
            curriculum_obstruction_score=90.0,
            civil_society_repression_score=92.0,
            access_denial_marginalized_score=88.0,
            international_framework_gap_score=85.0,
            primary_pattern="civil_society_repression",
        ),
        HumanRightsEducationEntity(
            entity_id="HRE-002",
            name="Russie — Loi Agents Étrangers ONG, Interdiction Contenu Droits & Écoles Propagande",
            country="Europe de l'Est",
            curriculum_obstruction_score=88.0,
            civil_society_repression_score=90.0,
            access_denial_marginalized_score=85.0,
            international_framework_gap_score=82.0,
            primary_pattern="civil_society_repression",
        ),
        HumanRightsEducationEntity(
            entity_id="HRE-003",
            name="Iran — Curriculum Islamiste Exclusif, ONG Droits Humains Interdites & Femmes Exclus",
            country="Moyen-Orient",
            curriculum_obstruction_score=82.0,
            civil_society_repression_score=85.0,
            access_denial_marginalized_score=88.0,
            international_framework_gap_score=80.0,
            primary_pattern="access_denial_marginalized",
        ),
        HumanRightsEducationEntity(
            entity_id="HRE-004",
            name="Arabie Saoudite — Droits Humains Absents Curricula, Militantes Emprisonnées & Contrôle Religieux",
            country="Moyen-Orient",
            curriculum_obstruction_score=80.0,
            civil_society_repression_score=78.0,
            access_denial_marginalized_score=82.0,
            international_framework_gap_score=85.0,
            primary_pattern="international_framework_gap",
        ),
        HumanRightsEducationEntity(
            entity_id="HRE-005",
            name="Inde — Manuels Scolaires Révisés BJP, Minorités Effacées & ONG Droits sous Pression FCRA",
            country="Asie du Sud",
            curriculum_obstruction_score=52.0,
            civil_society_repression_score=55.0,
            access_denial_marginalized_score=58.0,
            international_framework_gap_score=50.0,
            primary_pattern="access_denial_marginalized",
        ),
        HumanRightsEducationEntity(
            entity_id="HRE-006",
            name="Turquie — Restriction ONG Post-Coup, Contenu Kémaliste Imposé & Minorités Kurdes Exclues",
            country="Europe de l'Est",
            curriculum_obstruction_score=48.0,
            civil_society_repression_score=52.0,
            access_denial_marginalized_score=55.0,
            international_framework_gap_score=50.0,
            primary_pattern="curriculum_obstruction",
        ),
        HumanRightsEducationEntity(
            entity_id="HRE-007",
            name="UE/UNESCO — Programme Mondial EDH, Plan Action 2020-2024 & Intégration Partielle Curricula",
            country="Europe/Global",
            curriculum_obstruction_score=22.0,
            civil_society_repression_score=28.0,
            access_denial_marginalized_score=30.0,
            international_framework_gap_score=25.0,
            primary_pattern="curriculum_obstruction",
        ),
        HumanRightsEducationEntity(
            entity_id="HRE-008",
            name="ONU/HCDH — Déclaration ONU EDH 2011, Rapporteur Spécial & Ressources Pédagogiques",
            country="Global",
            curriculum_obstruction_score=4.0,
            civil_society_repression_score=5.0,
            access_denial_marginalized_score=3.0,
            international_framework_gap_score=6.0,
            primary_pattern="international_framework_gap",
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

    return HumanRightsEducationEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_human_rights_education_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_declaration_human_rights_education_training_2011_implementation_report",
            "amnesty_international_human_rights_education_program_global_survey",
            "hrea_human_rights_education_associates_global_status_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_human_rights_education_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_human_rights_education_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
