from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class JuvenileJusticeEntity:
    entity_id: str
    name: str
    country: str
    child_detention_scale_score: float
    rehabilitation_failure_score: float
    age_criminal_responsibility_score: float
    torture_juvenile_detention_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_juvenile_justice_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.child_detention_scale_score * 0.30
            + self.rehabilitation_failure_score * 0.25
            + self.age_criminal_responsibility_score * 0.25
            + self.torture_juvenile_detention_score * 0.20,
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
        self.estimated_juvenile_justice_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class JuvenileJusticeEngineResult:
    agent: str = "Juvenile Justice Engine Agent"
    domain: str = "juvenile_justice"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_juvenile_justice_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[JuvenileJusticeEntity] = field(default_factory=list)

def run_juvenile_justice_engine() -> JuvenileJusticeEngineResult:
    entities = [
        JuvenileJusticeEntity(
            entity_id="JJ-001",
            name="Chine — Centres Rééducation Mineurs, Travail Forcé & Aucune Garantie Procédurale",
            country="Asie du Nord-Est",
            child_detention_scale_score=90.0,
            rehabilitation_failure_score=85.0,
            age_criminal_responsibility_score=85.0,
            torture_juvenile_detention_score=88.0,
            primary_pattern="child_detention_scale",
        ),
        JuvenileJusticeEntity(
            entity_id="JJ-002",
            name="USA — Jugement Mineurs comme Adultes, Prison à Vie Sans Liberté Conditionnelle & Solitary Confinement",
            country="Amérique du Nord",
            child_detention_scale_score=88.0,
            rehabilitation_failure_score=85.0,
            age_criminal_responsibility_score=90.0,
            torture_juvenile_detention_score=82.0,
            primary_pattern="age_criminal_responsibility",
        ),
        JuvenileJusticeEntity(
            entity_id="JJ-003",
            name="Iran — Exécution Mineurs, Peine de Mort Crimes Commis avant 18 Ans & Tribunaux Spéciaux",
            country="Moyen-Orient",
            child_detention_scale_score=82.0,
            rehabilitation_failure_score=80.0,
            age_criminal_responsibility_score=88.0,
            torture_juvenile_detention_score=85.0,
            primary_pattern="age_criminal_responsibility",
        ),
        JuvenileJusticeEntity(
            entity_id="JJ-004",
            name="Arabie Saoudite — Exécutions Mineurs, Flagellation & Conditions Détention Inhumaines",
            country="Moyen-Orient",
            child_detention_scale_score=78.0,
            rehabilitation_failure_score=82.0,
            age_criminal_responsibility_score=80.0,
            torture_juvenile_detention_score=85.0,
            primary_pattern="torture_juvenile_detention",
        ),
        JuvenileJusticeEntity(
            entity_id="JJ-005",
            name="Inde — POCSO, Tribunaux Juvéniles Surchargés & Conditions Maisons de Correction Déplorables",
            country="Asie du Sud",
            child_detention_scale_score=52.0,
            rehabilitation_failure_score=55.0,
            age_criminal_responsibility_score=58.0,
            torture_juvenile_detention_score=50.0,
            primary_pattern="rehabilitation_failure",
        ),
        JuvenileJusticeEntity(
            entity_id="JJ-006",
            name="Brésil — FEBEM/FUNDAC, Massacres en Centres Jeunes & Surpopulation Systémique",
            country="Amérique Latine",
            child_detention_scale_score=50.0,
            rehabilitation_failure_score=48.0,
            age_criminal_responsibility_score=55.0,
            torture_juvenile_detention_score=52.0,
            primary_pattern="rehabilitation_failure",
        ),
        JuvenileJusticeEntity(
            entity_id="JJ-007",
            name="UE/Norvège — Justice Restaurative, Modèle Nordique & Déjudiciarisation Mineurs",
            country="Europe",
            child_detention_scale_score=22.0,
            rehabilitation_failure_score=30.0,
            age_criminal_responsibility_score=28.0,
            torture_juvenile_detention_score=25.0,
            primary_pattern="child_detention_scale",
        ),
        JuvenileJusticeEntity(
            entity_id="JJ-008",
            name="ONU/UNICEF — Convention Droits Enfant, Règles Beijing & Directives Riyad",
            country="Global",
            child_detention_scale_score=4.0,
            rehabilitation_failure_score=5.0,
            age_criminal_responsibility_score=3.0,
            torture_juvenile_detention_score=6.0,
            primary_pattern="child_detention_scale",
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

    return JuvenileJusticeEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_juvenile_justice_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unicef_justice_children_global_report_annual",
            "child_rights_international_network_juvenile_justice_database",
            "un_committee_rights_child_general_comment_10_juvenile_justice",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_juvenile_justice_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_juvenile_justice_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
