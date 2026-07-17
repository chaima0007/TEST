from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class SolitaryConfinementEntity:
    entity_id: str
    name: str
    country: str
    isolation_duration_scale_score: float
    psychological_harm_score: float
    juvenile_elderly_application_score: float
    international_prohibition_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_solitary_confinement_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.isolation_duration_scale_score * 0.30
            + self.psychological_harm_score * 0.25
            + self.juvenile_elderly_application_score * 0.25
            + self.international_prohibition_gap_score * 0.20,
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
        self.estimated_solitary_confinement_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class SolitaryConfinementEngineResult:
    agent: str = "Solitary Confinement Engine Agent"
    domain: str = "solitary_confinement"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.83
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_solitary_confinement_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[SolitaryConfinementEntity] = field(default_factory=list)

def run_solitary_confinement_engine() -> SolitaryConfinementEngineResult:
    entities = [
        SolitaryConfinementEntity(
            entity_id="SC-001",
            name="USA — Supermax ADX, 80 000 Détenus Isolement Prolongé & Placements SHU Indéfinis",
            country="Amérique du Nord",
            isolation_duration_scale_score=92.0,
            psychological_harm_score=88.0,
            juvenile_elderly_application_score=90.0,
            international_prohibition_gap_score=85.0,
            primary_pattern="isolation_duration_scale",
        ),
        SolitaryConfinementEntity(
            entity_id="SC-002",
            name="Russie — Shizo/PKT, Isolement Politique, Opposants Navalny & Violation Règles Mandela",
            country="Europe de l'Est",
            isolation_duration_scale_score=85.0,
            psychological_harm_score=88.0,
            juvenile_elderly_application_score=85.0,
            international_prohibition_gap_score=82.0,
            primary_pattern="psychological_harm",
        ),
        SolitaryConfinementEntity(
            entity_id="SC-003",
            name="Chine — Cellules Spéciales Laogai, Isolement Ouïghours & Détention Incommunicado",
            country="Asie du Nord-Est",
            isolation_duration_scale_score=88.0,
            psychological_harm_score=85.0,
            juvenile_elderly_application_score=82.0,
            international_prohibition_gap_score=80.0,
            primary_pattern="isolation_duration_scale",
        ),
        SolitaryConfinementEntity(
            entity_id="SC-004",
            name="Iran — Evin Section 209, Prisonniers Politiques Isolés des Années & Torture Psychologique",
            country="Moyen-Orient",
            isolation_duration_scale_score=80.0,
            psychological_harm_score=82.0,
            juvenile_elderly_application_score=85.0,
            international_prohibition_gap_score=78.0,
            primary_pattern="juvenile_elderly_application",
        ),
        SolitaryConfinementEntity(
            entity_id="SC-005",
            name="Égypte — Isolement Longue Durée, Prisonniers Politiques & Absence Contrôle Judiciaire",
            country="Afrique du Nord",
            isolation_duration_scale_score=52.0,
            psychological_harm_score=55.0,
            juvenile_elderly_application_score=50.0,
            international_prohibition_gap_score=58.0,
            primary_pattern="international_prohibition_gap",
        ),
        SolitaryConfinementEntity(
            entity_id="SC-006",
            name="Mexique — Aislamiento en Cárceles Fédérales, Cartels & Absence Réforme Pénitentiaire",
            country="Amérique Centrale",
            isolation_duration_scale_score=48.0,
            psychological_harm_score=52.0,
            juvenile_elderly_application_score=55.0,
            international_prohibition_gap_score=50.0,
            primary_pattern="juvenile_elderly_application",
        ),
        SolitaryConfinementEntity(
            entity_id="SC-007",
            name="UE/Danemark — Réforme Progressive, Limite 4 Semaines & Interdiction Mineurs",
            country="Europe",
            isolation_duration_scale_score=25.0,
            psychological_harm_score=30.0,
            juvenile_elderly_application_score=28.0,
            international_prohibition_gap_score=22.0,
            primary_pattern="psychological_harm",
        ),
        SolitaryConfinementEntity(
            entity_id="SC-008",
            name="ONU/Règles Mandela — Art. 43-44, Interdiction Isolement Prolongé +15 Jours & Monitoring",
            country="Global",
            isolation_duration_scale_score=4.0,
            psychological_harm_score=5.0,
            juvenile_elderly_application_score=3.0,
            international_prohibition_gap_score=6.0,
            primary_pattern="isolation_duration_scale",
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

    return SolitaryConfinementEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_solitary_confinement_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "solitary_watch_supermax_isolation_global_report_annual",
            "un_subcommittee_prevention_torture_solitary_confinement_report",
            "mandela_rules_un_standard_minimum_treatment_prisoners_2015",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_solitary_confinement_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_solitary_confinement_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
