from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class DeathPenaltyExtrajudicialKillingsEntity:
    entity_id: str
    name: str
    country: str
    extrajudicial_killing_state_sanctioned_severity_score: float
    death_penalty_wrongful_execution_scale_score: float
    enforced_disappearance_targeted_assassination_score: float
    accountability_impunity_state_violence_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_death_penalty_extrajudicial_killings_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.extrajudicial_killing_state_sanctioned_severity_score * 0.30
            + self.death_penalty_wrongful_execution_scale_score * 0.25
            + self.enforced_disappearance_targeted_assassination_score * 0.25
            + self.accountability_impunity_state_violence_deficit_gap_score * 0.20,
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
        self.estimated_death_penalty_extrajudicial_killings_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class DeathPenaltyExtrajudicialKillingsEngineResult:
    agent: str = "Death Penalty Extrajudicial Killings Engine Agent"
    domain: str = "death_penalty_extrajudicial_killings"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_death_penalty_extrajudicial_killings_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[DeathPenaltyExtrajudicialKillingsEntity] = field(default_factory=list)


def run_death_penalty_extrajudicial_killings_engine() -> DeathPenaltyExtrajudicialKillingsEngineResult:
    entities = [
        DeathPenaltyExtrajudicialKillingsEntity(
            entity_id="DPE-001",
            name="Philippines/Duterte — Guerre Drogues 30 000 Morts Extrajudiciaires, Escadrons Mort PNP, Impunité Totale & Autodafé Suspects",
            country="Philippines",
            extrajudicial_killing_state_sanctioned_severity_score=96.0,
            death_penalty_wrongful_execution_scale_score=92.0,
            enforced_disappearance_targeted_assassination_score=94.0,
            accountability_impunity_state_violence_deficit_gap_score=90.0,
            primary_pattern="extrajudicial_killing_state_sanctioned_severity",
        ),
        DeathPenaltyExtrajudicialKillingsEntity(
            entity_id="DPE-002",
            name="Chine Exécutions — Plus Grand Nombre Mondial Exécutions, Peine Mort Crimes Non-Violents, Organes Prisonniers Conscience & Exécutions Secrètes",
            country="Chine",
            extrajudicial_killing_state_sanctioned_severity_score=93.0,
            death_penalty_wrongful_execution_scale_score=90.0,
            enforced_disappearance_targeted_assassination_score=89.0,
            accountability_impunity_state_violence_deficit_gap_score=88.0,
            primary_pattern="death_penalty_wrongful_execution_scale",
        ),
        DeathPenaltyExtrajudicialKillingsEntity(
            entity_id="DPE-003",
            name="Iran Pendaisons — Exécutions Mineurs, Pendaisons Publiques, Peine Mort Homosexualité & Prisonniers Politiques Exécutés",
            country="Iran",
            extrajudicial_killing_state_sanctioned_severity_score=90.0,
            death_penalty_wrongful_execution_scale_score=87.0,
            enforced_disappearance_targeted_assassination_score=86.0,
            accountability_impunity_state_violence_deficit_gap_score=85.0,
            primary_pattern="enforced_disappearance_targeted_assassination",
        ),
        DeathPenaltyExtrajudicialKillingsEntity(
            entity_id="DPE-004",
            name="Syrie/Russie — Assassinats Ciblés Opposants, Disparitions Forcées Journalistes, Bombardements Civils Impunis & Wagner Exécutions Filmées",
            country="Syrie/Russie",
            extrajudicial_killing_state_sanctioned_severity_score=87.0,
            death_penalty_wrongful_execution_scale_score=83.0,
            enforced_disappearance_targeted_assassination_score=84.0,
            accountability_impunity_state_violence_deficit_gap_score=82.0,
            primary_pattern="accountability_impunity_state_violence_deficit_gap",
        ),
        DeathPenaltyExtrajudicialKillingsEntity(
            entity_id="DPE-005",
            name="USA/Arabie Saoudite — Peine Mort Débat Innocents Exécutés USA, Décapitations Arabie Saoudite & Disparités Raciales Couloir Mort",
            country="USA/Arabie Saoudite",
            extrajudicial_killing_state_sanctioned_severity_score=57.0,
            death_penalty_wrongful_execution_scale_score=55.0,
            enforced_disappearance_targeted_assassination_score=54.0,
            accountability_impunity_state_violence_deficit_gap_score=53.0,
            primary_pattern="death_penalty_wrongful_execution_scale",
        ),
        DeathPenaltyExtrajudicialKillingsEntity(
            entity_id="DPE-006",
            name="Brésil/Inde — Violences Policières Favelas Brésil, Rencontres Policières Inde & Impunité Systémique Forces Ordre",
            country="Brésil/Inde",
            extrajudicial_killing_state_sanctioned_severity_score=54.0,
            death_penalty_wrongful_execution_scale_score=52.0,
            enforced_disappearance_targeted_assassination_score=51.0,
            accountability_impunity_state_violence_deficit_gap_score=50.0,
            primary_pattern="extrajudicial_killing_state_sanctioned_severity",
        ),
        DeathPenaltyExtrajudicialKillingsEntity(
            entity_id="DPE-007",
            name="Amnesty/Reprieve — Documentation Condamnés Innocents, Plaidoyer Abolition Mondiale & Représentation Légale Condamnés Mort",
            country="Global",
            extrajudicial_killing_state_sanctioned_severity_score=28.0,
            death_penalty_wrongful_execution_scale_score=26.0,
            enforced_disappearance_targeted_assassination_score=25.0,
            accountability_impunity_state_violence_deficit_gap_score=24.0,
            primary_pattern="accountability_impunity_state_violence_deficit_gap",
        ),
        DeathPenaltyExtrajudicialKillingsEntity(
            entity_id="DPE-008",
            name="ONU/2ème Protocole — Protocole Facultatif Abolition Peine Mort, Rapporteur Spécial Exécutions Extrajudiciaires & Moratoire Universel",
            country="Global",
            extrajudicial_killing_state_sanctioned_severity_score=5.0,
            death_penalty_wrongful_execution_scale_score=4.0,
            enforced_disappearance_targeted_assassination_score=4.0,
            accountability_impunity_state_violence_deficit_gap_score=3.0,
            primary_pattern="enforced_disappearance_targeted_assassination",
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

    return DeathPenaltyExtrajudicialKillingsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_death_penalty_extrajudicial_killings_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "amnesty_international_death_penalty_global_report",
            "reprieve_extrajudicial_killing_documentation",
            "un_special_rapporteur_extrajudicial_executions_reports",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_death_penalty_extrajudicial_killings_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_death_penalty_extrajudicial_killings_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
