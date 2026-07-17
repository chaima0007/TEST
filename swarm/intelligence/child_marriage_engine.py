from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class ChildMarriageEntity:
    entity_id: str
    name: str
    country: str
    prevalence_underage_unions_score: float
    girls_education_dropout_score: float
    health_maternal_mortality_score: float
    legal_enforcement_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_child_marriage_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.prevalence_underage_unions_score * 0.30
            + self.girls_education_dropout_score * 0.25
            + self.health_maternal_mortality_score * 0.25
            + self.legal_enforcement_gap_score * 0.20,
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
        self.estimated_child_marriage_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class ChildMarriageEngineResult:
    agent: str = "Child Marriage Engine Agent"
    domain: str = "child_marriage"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_child_marriage_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ChildMarriageEntity] = field(default_factory=list)

def run_child_marriage_engine() -> ChildMarriageEngineResult:
    entities = [
        ChildMarriageEntity(
            entity_id="CM-001",
            name="Niger — 76% Filles Mariées Avant 18 Ans, Taux Mondial le Plus Élevé & Fistules Obstétricales",
            country="Afrique de l'Ouest",
            prevalence_underage_unions_score=95.0,
            girls_education_dropout_score=90.0,
            health_maternal_mortality_score=92.0,
            legal_enforcement_gap_score=88.0,
            primary_pattern="prevalence_underage_unions",
        ),
        ChildMarriageEntity(
            entity_id="CM-002",
            name="Bangladesh — 59% Filles Mariées Avant 18 Ans, Exception Légale & Violences Conjugales",
            country="Asie du Sud",
            prevalence_underage_unions_score=88.0,
            girls_education_dropout_score=85.0,
            health_maternal_mortality_score=88.0,
            legal_enforcement_gap_score=85.0,
            primary_pattern="health_maternal_mortality",
        ),
        ChildMarriageEntity(
            entity_id="CM-003",
            name="Mali — 52% Filles Mariées Avant 18 Ans, Mariages Forcés Sahel & Abandon Scolaire Massif",
            country="Afrique de l'Ouest",
            prevalence_underage_unions_score=85.0,
            girls_education_dropout_score=88.0,
            health_maternal_mortality_score=82.0,
            legal_enforcement_gap_score=80.0,
            primary_pattern="girls_education_dropout",
        ),
        ChildMarriageEntity(
            entity_id="CM-004",
            name="Inde — 27% Filles Mariées Avant 18 Ans, 15M Mariages Enfants/An & Application Loi Défaillante",
            country="Asie du Sud",
            prevalence_underage_unions_score=80.0,
            girls_education_dropout_score=82.0,
            health_maternal_mortality_score=78.0,
            legal_enforcement_gap_score=82.0,
            primary_pattern="legal_enforcement_gap",
        ),
        ChildMarriageEntity(
            entity_id="CM-005",
            name="Éthiopie — 40% Filles Mariées Avant 18 Ans, Régions Rurales Isolées & Pauvreté Structurelle",
            country="Afrique de l'Est",
            prevalence_underage_unions_score=52.0,
            girls_education_dropout_score=55.0,
            health_maternal_mortality_score=58.0,
            legal_enforcement_gap_score=50.0,
            primary_pattern="health_maternal_mortality",
        ),
        ChildMarriageEntity(
            entity_id="CM-006",
            name="Proche-Orient/Réfugiés Syriens — Mariages Précoces Camps Jordanie/Liban & Vulnérabilité",
            country="Moyen-Orient",
            prevalence_underage_unions_score=48.0,
            girls_education_dropout_score=52.0,
            health_maternal_mortality_score=50.0,
            legal_enforcement_gap_score=55.0,
            primary_pattern="legal_enforcement_gap",
        ),
        ChildMarriageEntity(
            entity_id="CM-007",
            name="ONU/UNICEF Girls Not Brides — Alliance Mondiale 1500 ONG, Plaidoyer & Programmes Éducation",
            country="Global",
            prevalence_underage_unions_score=22.0,
            girls_education_dropout_score=28.0,
            health_maternal_mortality_score=25.0,
            legal_enforcement_gap_score=30.0,
            primary_pattern="girls_education_dropout",
        ),
        ChildMarriageEntity(
            entity_id="CM-008",
            name="ONU/CEDAW — Convention Élimination Discrimination Femmes, Art.16 Mariage Enfants & Suivi",
            country="Global",
            prevalence_underage_unions_score=4.0,
            girls_education_dropout_score=5.0,
            health_maternal_mortality_score=3.0,
            legal_enforcement_gap_score=6.0,
            primary_pattern="prevalence_underage_unions",
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

    return ChildMarriageEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_child_marriage_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unicef_girls_not_brides_global_child_marriage_data_portal",
            "save_the_children_too_young_to_wed_global_report",
            "un_women_child_early_forced_marriage_prevention_framework",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_child_marriage_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_child_marriage_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
