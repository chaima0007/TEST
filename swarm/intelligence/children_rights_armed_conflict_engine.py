from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ENGINE_VERSION = "1.0.0"

@dataclass
class ChildrenRightsArmedConflictEntity:
    entity_id: str
    name: str
    country: str
    child_soldier_recruitment_scale_score: float
    school_hospital_attack_civilian_harm_score: float
    family_separation_displacement_trauma_score: float
    child_protection_mechanism_absence_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_children_rights_armed_conflict_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.child_soldier_recruitment_scale_score * 0.30
            + self.school_hospital_attack_civilian_harm_score * 0.25
            + self.family_separation_displacement_trauma_score * 0.25
            + self.child_protection_mechanism_absence_score * 0.20,
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
        self.estimated_children_rights_armed_conflict_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class ChildrenRightsArmedConflictEngineResult:
    agent: str = "Children Rights Armed Conflict Engine Agent"
    domain: str = "children_rights_armed_conflict"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.89
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = ENGINE_VERSION
    avg_estimated_children_rights_armed_conflict_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ChildrenRightsArmedConflictEntity] = field(default_factory=list)


def run_children_rights_armed_conflict_engine() -> ChildrenRightsArmedConflictEngineResult:
    entities = [
        ChildrenRightsArmedConflictEntity(
            entity_id="CRAC-001",
            name="RDC/Kivu — 30+ Groupes Armés Recrutement Enfants Soldats FARDC, Viols Enfants Arme Guerre, Écoles Détruites & Aucun Mécanisme DDR Effectif",
            country="RDC",
            child_soldier_recruitment_scale_score=95.0,
            school_hospital_attack_civilian_harm_score=88.0,
            family_separation_displacement_trauma_score=90.0,
            child_protection_mechanism_absence_score=85.0,
            primary_pattern="recrutement_enfants_soldats",
        ),
        ChildrenRightsArmedConflictEntity(
            entity_id="CRAC-002",
            name="Yemen — Enfants 70% Victimes Coalition Civils, Écoles Hôpitaux Frappés Saudi Led, Malnutrition Sévère 2.2M Enfants & Recrutement Houthis Mineurs",
            country="Yemen",
            child_soldier_recruitment_scale_score=82.0,
            school_hospital_attack_civilian_harm_score=92.0,
            family_separation_displacement_trauma_score=88.0,
            child_protection_mechanism_absence_score=80.0,
            primary_pattern="attaques_ecoles_hopitaux",
        ),
        ChildrenRightsArmedConflictEntity(
            entity_id="CRAC-003",
            name="Soudan/RSF — Darfour Enlèvements Enfants 2023, Viols Systématiques RSF Mineurs, Villages Incendiés & 8M Déplacés dont Majorité Enfants",
            country="Soudan",
            child_soldier_recruitment_scale_score=90.0,
            school_hospital_attack_civilian_harm_score=85.0,
            family_separation_displacement_trauma_score=86.0,
            child_protection_mechanism_absence_score=82.0,
            primary_pattern="separation_deplacement_enfants",
        ),
        ChildrenRightsArmedConflictEntity(
            entity_id="CRAC-004",
            name="Myanmar — Tatmadaw Recrutement Forcé Rohingya Enfants, Frappes Aériennes Villages, Séparation Familles Opérations & Absence Protection ONU Accès",
            country="Myanmar",
            child_soldier_recruitment_scale_score=88.0,
            school_hospital_attack_civilian_harm_score=80.0,
            family_separation_displacement_trauma_score=84.0,
            child_protection_mechanism_absence_score=78.0,
            primary_pattern="recrutement_enfants_soldats",
        ),
        ChildrenRightsArmedConflictEntity(
            entity_id="CRAC-005",
            name="Sahel — JNIM Boko Haram Enfants Soldats Burkina Mali, Attaques Écoles 800+ Fermées, Déplacement Massif & Réseaux Protection Enfants Absents",
            country="Burkina Faso/Mali",
            child_soldier_recruitment_scale_score=58.0,
            school_hospital_attack_civilian_harm_score=52.0,
            family_separation_displacement_trauma_score=55.0,
            child_protection_mechanism_absence_score=48.0,
            primary_pattern="absence_protection_enfants_conflit",
        ),
        ChildrenRightsArmedConflictEntity(
            entity_id="CRAC-006",
            name="Colombie — Post-Accord FARC Dissidents Enfants Recrutés, Comunidades Sans État, Déplacements Communautaires & Mécanismes DDR Partiellement Actifs",
            country="Colombie",
            child_soldier_recruitment_scale_score=55.0,
            school_hospital_attack_civilian_harm_score=48.0,
            family_separation_displacement_trauma_score=58.0,
            child_protection_mechanism_absence_score=52.0,
            primary_pattern="recrutement_enfants_soldats",
        ),
        ChildrenRightsArmedConflictEntity(
            entity_id="CRAC-007",
            name="Ukraine — Enfants Déplacés 2M Frontières Bombardements, Écoles Abritées Soldats, Séparations Familles & Systèmes Protection Partiellement Actifs",
            country="Ukraine",
            child_soldier_recruitment_scale_score=22.0,
            school_hospital_attack_civilian_harm_score=35.0,
            family_separation_displacement_trauma_score=42.0,
            child_protection_mechanism_absence_score=28.0,
            primary_pattern="separation_deplacement_enfants",
        ),
        ChildrenRightsArmedConflictEntity(
            entity_id="CRAC-008",
            name="Géorgie — Accord Paix Post-Ossétie Mécanismes Protection Enfants, UNICEF Présent, Accès Humanitaire Stable & Faible Recrutement Documenté",
            country="Géorgie",
            child_soldier_recruitment_scale_score=5.0,
            school_hospital_attack_civilian_harm_score=6.0,
            family_separation_displacement_trauma_score=8.0,
            child_protection_mechanism_absence_score=10.0,
            primary_pattern="absence_protection_enfants_conflit",
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

    return ChildrenRightsArmedConflictEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_children_rights_armed_conflict_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_secretary_general_children_armed_conflict_2023",
            "save_the_children_annual_report_2023",
            "child_soldiers_international_annual_report",
            "unicef_grave_violations_monitoring_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_children_rights_armed_conflict_engine()
    print(f"Agent: {result.agent}")
    print(f"Engine version: {result.engine_version}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Confidence score: {result.confidence_score}")
    print(f"Avg index: {result.avg_estimated_children_rights_armed_conflict_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    print(f"Data sources: {result.data_sources}")
    print()
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}] — index={e.estimated_children_rights_armed_conflict_index}")
