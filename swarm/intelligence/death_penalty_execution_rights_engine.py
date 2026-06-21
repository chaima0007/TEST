from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class DeathPenaltyExecutionRightsEntity:
    entity_id: str
    name: str
    country: str
    execution_scale_arbitrariness_score: float
    juvenile_wrongful_execution_risk_score: float
    fair_trial_due_process_violation_score: float
    abolition_moratorium_accountability_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_death_penalty_execution_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.execution_scale_arbitrariness_score * 0.30
            + self.juvenile_wrongful_execution_risk_score * 0.25
            + self.fair_trial_due_process_violation_score * 0.25
            + self.abolition_moratorium_accountability_gap_score * 0.20,
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
        self.estimated_death_penalty_execution_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class DeathPenaltyExecutionRightsEngineResult:
    agent: str = "Death Penalty Execution Rights Engine Agent"
    domain: str = "death_penalty_execution_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.89
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_death_penalty_execution_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[DeathPenaltyExecutionRightsEntity] = field(default_factory=list)


def run_death_penalty_execution_rights_engine() -> DeathPenaltyExecutionRightsEngineResult:
    entities = [
        DeathPenaltyExecutionRightsEntity(
            entity_id="DPE-001",
            name="Chine — 2000+ Exécutions/An, Secret État, Ouïghours Condamnés Masse & Prélèvement Organes Prisonniers Documenté",
            country="Chine",
            execution_scale_arbitrariness_score=98.0,
            juvenile_wrongful_execution_risk_score=95.0,
            fair_trial_due_process_violation_score=97.0,
            abolition_moratorium_accountability_gap_score=99.0,
            primary_pattern="execution_scale_arbitrariness",
        ),
        DeathPenaltyExecutionRightsEntity(
            entity_id="DPE-002",
            name="Iran — 582 Exécutions 2023, Mineurs Exécutés, Pendaison Manifestants 2022 & Drogues Peine de Mort",
            country="Iran",
            execution_scale_arbitrariness_score=93.0,
            juvenile_wrongful_execution_risk_score=91.0,
            fair_trial_due_process_violation_score=90.0,
            abolition_moratorium_accountability_gap_score=95.0,
            primary_pattern="juvenile_wrongful_execution_risk",
        ),
        DeathPenaltyExecutionRightsEntity(
            entity_id="DPE-003",
            name="Arabie Saoudite — 196 Exécutions 2022, Décapitation, Crimes Drogues/Blasphème & Mineurs au Moment des Faits",
            country="Arabie Saoudite",
            execution_scale_arbitrariness_score=88.0,
            juvenile_wrongful_execution_risk_score=86.0,
            fair_trial_due_process_violation_score=90.0,
            abolition_moratorium_accountability_gap_score=92.0,
            primary_pattern="fair_trial_due_process_violation",
        ),
        DeathPenaltyExecutionRightsEntity(
            entity_id="DPE-004",
            name="Corée du Nord — Exécutions Publiques Infractions Mineures, Familles Exécutées avec Condamnés & Secret Total",
            country="Corée du Nord",
            execution_scale_arbitrariness_score=92.0,
            juvenile_wrongful_execution_risk_score=88.0,
            fair_trial_due_process_violation_score=96.0,
            abolition_moratorium_accountability_gap_score=98.0,
            primary_pattern="fair_trial_due_process_violation",
        ),
        DeathPenaltyExecutionRightsEntity(
            entity_id="DPE-005",
            name="USA — 24 Exécutions 2023, Innocents Exécutés (Innocence Project 190+), Inégalités Raciales & Texas Dominant",
            country="USA",
            execution_scale_arbitrariness_score=52.0,
            juvenile_wrongful_execution_risk_score=58.0,
            fair_trial_due_process_violation_score=48.0,
            abolition_moratorium_accountability_gap_score=60.0,
            primary_pattern="juvenile_wrongful_execution_risk",
        ),
        DeathPenaltyExecutionRightsEntity(
            entity_id="DPE-006",
            name="Singapour — Pendaison Trafic Drogue, Taux Exécution/Habitant Parmi Plus Élevés & Procès Équitables Mais Loi Inéquitable",
            country="Singapour",
            execution_scale_arbitrariness_score=48.0,
            juvenile_wrongful_execution_risk_score=42.0,
            fair_trial_due_process_violation_score=40.0,
            abolition_moratorium_accountability_gap_score=55.0,
            primary_pattern="abolition_moratorium_accountability_gap",
        ),
        DeathPenaltyExecutionRightsEntity(
            entity_id="DPE-007",
            name="Japon — 3 Exécutions 2023, Secret Total Jusqu&apos;au Dernier Moment & Couloir de la Mort 10+ Ans",
            country="Japon",
            execution_scale_arbitrariness_score=28.0,
            juvenile_wrongful_execution_risk_score=22.0,
            fair_trial_due_process_violation_score=30.0,
            abolition_moratorium_accountability_gap_score=35.0,
            primary_pattern="fair_trial_due_process_violation",
        ),
        DeathPenaltyExecutionRightsEntity(
            entity_id="DPE-008",
            name="Portugal — Abolition 1867 Pionnière, Aucune Exécution & Lobbying International Abolitionniste Actif",
            country="Portugal",
            execution_scale_arbitrariness_score=2.0,
            juvenile_wrongful_execution_risk_score=2.0,
            fair_trial_due_process_violation_score=2.0,
            abolition_moratorium_accountability_gap_score=2.0,
            primary_pattern="abolition_moratorium_accountability_gap",
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

    return DeathPenaltyExecutionRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_death_penalty_execution_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "amnesty_international_death_penalty_global_report_2023",
            "death_penalty_information_center_2023",
            "hands_off_cain_world_report_executions_2023",
            "cornell_center_death_penalty_worldwide_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_death_penalty_execution_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_death_penalty_execution_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
