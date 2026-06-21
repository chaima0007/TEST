from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class RightToEducationAccessEntity:
    entity_id: str
    name: str
    country: str
    school_exclusion_gender_ethnic_score: float
    conflict_education_disruption_attack_score: float
    quality_access_inequality_score: float
    legal_right_education_enforcement_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_right_to_education_access_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.school_exclusion_gender_ethnic_score * 0.30
            + self.conflict_education_disruption_attack_score * 0.25
            + self.quality_access_inequality_score * 0.25
            + self.legal_right_education_enforcement_gap_score * 0.20,
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
        self.estimated_right_to_education_access_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class RightToEducationAccessEngineResult:
    agent: str = "Right To Education Access Engine Agent"
    domain: str = "right_to_education_access"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.88
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_right_to_education_access_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[RightToEducationAccessEntity] = field(default_factory=list)

def run_right_to_education_access_engine() -> RightToEducationAccessEngineResult:
    entities = [
        RightToEducationAccessEntity(
            entity_id="REA-001",
            name="Afghanistan/Talibans 2021 — 1M+ Filles Exclues Secondaire, Universités Femmes Fermées & 8M Enfants Hors École",
            country="Asie du Sud",
            school_exclusion_gender_ethnic_score=98.0,
            conflict_education_disruption_attack_score=92.0,
            quality_access_inequality_score=95.0,
            legal_right_education_enforcement_gap_score=96.0,
            primary_pattern="school_exclusion_gender_ethnic",
        ),
        RightToEducationAccessEntity(
            entity_id="REA-002",
            name="Mali/Conflit Sahel — 1200+ Écoles Fermées Attaques JNIM/GSIM, 400K Enfants Déplacés & Enseignants Ciblés",
            country="Afrique de l'Ouest",
            school_exclusion_gender_ethnic_score=80.0,
            conflict_education_disruption_attack_score=92.0,
            quality_access_inequality_score=85.0,
            legal_right_education_enforcement_gap_score=82.0,
            primary_pattern="conflict_education_disruption_attack",
        ),
        RightToEducationAccessEntity(
            entity_id="REA-003",
            name="Yémen/Guerre — 8.1M Enfants Hors École, 2500+ Écoles Détruites/Occupées Armées & Recrutement Mineurs",
            country="MENA",
            school_exclusion_gender_ethnic_score=82.0,
            conflict_education_disruption_attack_score=94.0,
            quality_access_inequality_score=88.0,
            legal_right_education_enforcement_gap_score=84.0,
            primary_pattern="conflict_education_disruption_attack",
        ),
        RightToEducationAccessEntity(
            entity_id="REA-004",
            name="Nigeria/Borno — Boko Haram Kidnapping Élèves Chibok 276 Filles, 10M Enfants Hors École Nord & UBEC Budget Insuffisant",
            country="Afrique de l'Ouest",
            school_exclusion_gender_ethnic_score=85.0,
            conflict_education_disruption_attack_score=88.0,
            quality_access_inequality_score=80.0,
            legal_right_education_enforcement_gap_score=82.0,
            primary_pattern="school_exclusion_gender_ethnic",
        ),
        RightToEducationAccessEntity(
            entity_id="REA-005",
            name="Inde/Castes — Dalits/Adivasis Exclusion Systématique, Toilettes Séparées, Enseignants Abusifs & 47M Adultes Analphabètes",
            country="Asie du Sud",
            school_exclusion_gender_ethnic_score=58.0,
            conflict_education_disruption_attack_score=25.0,
            quality_access_inequality_score=55.0,
            legal_right_education_enforcement_gap_score=52.0,
            primary_pattern="school_exclusion_gender_ethnic",
        ),
        RightToEducationAccessEntity(
            entity_id="REA-006",
            name="Myanmar/Rohingya Post-Coup — 700K Réfugiés Aucun Accès Écoles Bangladesh, Coup 2021 = 12M Élèves Perturbés",
            country="Asie du Sud-Est",
            school_exclusion_gender_ethnic_score=62.0,
            conflict_education_disruption_attack_score=58.0,
            quality_access_inequality_score=48.0,
            legal_right_education_enforcement_gap_score=52.0,
            primary_pattern="school_exclusion_gender_ethnic",
        ),
        RightToEducationAccessEntity(
            entity_id="REA-007",
            name="Brésil/Inégalités — Nordeste Écoles Sans Eau/Électricité, 20M Adultes Analphabètes & Quilombola Distances",
            country="Amérique du Sud",
            school_exclusion_gender_ethnic_score=28.0,
            conflict_education_disruption_attack_score=10.0,
            quality_access_inequality_score=35.0,
            legal_right_education_enforcement_gap_score=30.0,
            primary_pattern="quality_access_inequality",
        ),
        RightToEducationAccessEntity(
            entity_id="REA-008",
            name="Finlande/Référence — PISA Top Mondial, Inclusion Handicap, Financement Égal Zones Rurales & 0 Frais Scolarité",
            country="Europe du Nord",
            school_exclusion_gender_ethnic_score=4.0,
            conflict_education_disruption_attack_score=2.0,
            quality_access_inequality_score=3.0,
            legal_right_education_enforcement_gap_score=4.0,
            primary_pattern="legal_right_education_enforcement_gap",
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

    return RightToEducationAccessEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_right_to_education_access_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unicef_out_of_school_children_initiative_2023",
            "unesco_global_education_monitoring_report_2023",
            "global_coalition_protect_education_conflict_2023",
            "human_rights_watch_right_to_education_reports_2023",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_right_to_education_access_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_right_to_education_access_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
