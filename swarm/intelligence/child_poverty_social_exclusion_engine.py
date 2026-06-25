from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class ChildPovetrySocialExclusionEntity:
    entity_id: str
    name: str
    country: str
    material_deprivation_severity_score: float
    education_access_barrier_score: float
    healthcare_nutrition_denial_score: float
    social_exclusion_stigma_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_child_poverty_social_exclusion_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.material_deprivation_severity_score * 0.30
            + self.education_access_barrier_score * 0.25
            + self.healthcare_nutrition_denial_score * 0.25
            + self.social_exclusion_stigma_score * 0.20,
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
        self.estimated_child_poverty_social_exclusion_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class ChildPovetrySocialExclusionEngineResult:
    agent: str = "Child Poverty Social Exclusion Engine Agent"
    domain: str = "child_poverty_social_exclusion"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.87
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_child_poverty_social_exclusion_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ChildPovetrySocialExclusionEntity] = field(default_factory=list)

def run_child_poverty_social_exclusion_engine() -> ChildPovetrySocialExclusionEngineResult:
    entities = [
        ChildPovetrySocialExclusionEntity(
            entity_id="CP-001",
            name="Yémen — 2.2M Enfants Malnutrition Aiguë Sévère, Guerre & Effondrement Systèmes Services",
            country="Moyen-Orient",
            material_deprivation_severity_score=95.0,
            education_access_barrier_score=92.0,
            healthcare_nutrition_denial_score=95.0,
            social_exclusion_stigma_score=90.0,
            primary_pattern="healthcare_nutrition_denial",
        ),
        ChildPovetrySocialExclusionEntity(
            entity_id="CP-002",
            name="RDC — 6.9M Enfants Insécurité Alimentaire Sévère, Conflits Est & Scolarisation 60%",
            country="Afrique Centrale",
            material_deprivation_severity_score=92.0,
            education_access_barrier_score=90.0,
            healthcare_nutrition_denial_score=90.0,
            social_exclusion_stigma_score=90.0,
            primary_pattern="material_deprivation_severity",
        ),
        ChildPovetrySocialExclusionEntity(
            entity_id="CP-003",
            name="Madagascar — 92% Population Sous Seuil Pauvreté, Enfants Travailleurs & UNICEF Urgence",
            country="Afrique de l'Est",
            material_deprivation_severity_score=90.0,
            education_access_barrier_score=88.0,
            healthcare_nutrition_denial_score=88.0,
            social_exclusion_stigma_score=88.0,
            primary_pattern="material_deprivation_severity",
        ),
        ChildPovetrySocialExclusionEntity(
            entity_id="CP-004",
            name="USA — 14M Enfants Pauvreté, Race Gap Structurel, Child Tax Credit Expiré & Housing Crisis",
            country="Amérique du Nord",
            material_deprivation_severity_score=85.0,
            education_access_barrier_score=85.0,
            healthcare_nutrition_denial_score=82.0,
            social_exclusion_stigma_score=88.0,
            primary_pattern="social_exclusion_stigma",
        ),
        ChildPovetrySocialExclusionEntity(
            entity_id="CP-005",
            name="UE/Bulgarie & Roumanie — Pauvreté Enfants Roms 30%+, Ségrégation Scolaire & Garantie Enfance",
            country="Europe",
            material_deprivation_severity_score=55.0,
            education_access_barrier_score=55.0,
            healthcare_nutrition_denial_score=52.0,
            social_exclusion_stigma_score=55.0,
            primary_pattern="education_access_barrier",
        ),
        ChildPovetrySocialExclusionEntity(
            entity_id="CP-006",
            name="UK — Pauvreté Enfants 30% Post-Austérité, Food Banks Scolaires & Two-Child Benefit Cap",
            country="Europe",
            material_deprivation_severity_score=50.0,
            education_access_barrier_score=48.0,
            healthcare_nutrition_denial_score=50.0,
            social_exclusion_stigma_score=50.0,
            primary_pattern="material_deprivation_severity",
        ),
        ChildPovetrySocialExclusionEntity(
            entity_id="CP-007",
            name="UNICEF/Save the Children — Monitoring Pauvreté Enfants Global, Rapport & Plaidoyer ODD",
            country="Global",
            material_deprivation_severity_score=22.0,
            education_access_barrier_score=28.0,
            healthcare_nutrition_denial_score=25.0,
            social_exclusion_stigma_score=30.0,
            primary_pattern="education_access_barrier",
        ),
        ChildPovetrySocialExclusionEntity(
            entity_id="CP-008",
            name="ONU/CRC — Art.27 Niveau de Vie Adéquat Enfant, Protocole Facultatif & Comité Droits Enfant",
            country="Global",
            material_deprivation_severity_score=4.0,
            education_access_barrier_score=5.0,
            healthcare_nutrition_denial_score=3.0,
            social_exclusion_stigma_score=6.0,
            primary_pattern="social_exclusion_stigma",
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

    return ChildPovetrySocialExclusionEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_child_poverty_social_exclusion_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unicef_state_worlds_children_poverty_exclusion_report",
            "save_the_children_global_childhood_report_deprivation",
            "un_crc_committee_general_comment_26_childrens_rights_environment",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_child_poverty_social_exclusion_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_child_poverty_social_exclusion_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
