from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class ArmedConflictCivilianProtectionEntity:
    entity_id: str
    name: str
    country: str
    civilian_targeting_indiscriminate_attack_severity_score: float
    siege_starvation_collective_punishment_scale_score: float
    hospital_school_infrastructure_attack_score: float
    humanitarian_access_aid_blockage_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_armed_conflict_civilian_protection_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.civilian_targeting_indiscriminate_attack_severity_score * 0.30
            + self.siege_starvation_collective_punishment_scale_score * 0.25
            + self.hospital_school_infrastructure_attack_score * 0.25
            + self.humanitarian_access_aid_blockage_deficit_gap_score * 0.20,
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
        self.estimated_armed_conflict_civilian_protection_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class ArmedConflictCivilianProtectionEngineResult:
    entities: List[ArmedConflictCivilianProtectionEntity]
    avg_composite: float
    distribution: dict
    data_sources: List[str]
    agent: str


def run_armed_conflict_civilian_protection_engine() -> ArmedConflictCivilianProtectionEngineResult:
    entities = [
        ArmedConflictCivilianProtectionEntity(
            entity_id="ACP-001",
            name="Gaza/Israël 2023-24 — 40 000 Civils Tués, 70% Femmes/Enfants, Hôpitaux Bombardés & Blocus Humanitaire Total",
            country="Palestine",
            civilian_targeting_indiscriminate_attack_severity_score=96.0,
            siege_starvation_collective_punishment_scale_score=94.0,
            hospital_school_infrastructure_attack_score=95.0,
            humanitarian_access_aid_blockage_deficit_gap_score=93.0,
            primary_pattern="civilian_targeting_indiscriminate_attack_severity",
        ),
        ArmedConflictCivilianProtectionEntity(
            entity_id="ACP-002",
            name="Syrie/Assad-Russie — 500 000 Morts Civils, Barils Explosifs Alep, Hôpitaux M2020 Ciblés & Chlore Attaques Chimiques",
            country="Syrie",
            civilian_targeting_indiscriminate_attack_severity_score=92.0,
            siege_starvation_collective_punishment_scale_score=93.0,
            hospital_school_infrastructure_attack_score=90.0,
            humanitarian_access_aid_blockage_deficit_gap_score=91.0,
            primary_pattern="siege_starvation_collective_punishment_scale",
        ),
        ArmedConflictCivilianProtectionEntity(
            entity_id="ACP-003",
            name="Yemen/Coalition — 24 000 Frappes Documentées, Mariages/Funérailles Bombardés, Blocus Port Hodeidah & Choléra 2.5M Cas",
            country="Yemen",
            civilian_targeting_indiscriminate_attack_severity_score=88.0,
            siege_starvation_collective_punishment_scale_score=86.0,
            hospital_school_infrastructure_attack_score=89.0,
            humanitarian_access_aid_blockage_deficit_gap_score=87.0,
            primary_pattern="humanitarian_access_aid_blockage_deficit_gap",
        ),
        ArmedConflictCivilianProtectionEntity(
            entity_id="ACP-004",
            name="Ukraine/Russie — Bucha Massacres, Zaporizhzhia Centrales Nucléaires Ciblées, Missiles Résidentiels & Déportations Forcées Enfants",
            country="Ukraine",
            civilian_targeting_indiscriminate_attack_severity_score=84.0,
            siege_starvation_collective_punishment_scale_score=82.0,
            hospital_school_infrastructure_attack_score=85.0,
            humanitarian_access_aid_blockage_deficit_gap_score=83.0,
            primary_pattern="civilian_targeting_indiscriminate_attack_severity",
        ),
        ArmedConflictCivilianProtectionEntity(
            entity_id="ACP-005",
            name="Myanmar/Tatmadaw — Villages Brûlés Civils, Jade/Chin Populations Ciblées, Aide Bloquée & Médecins Arrêtés",
            country="Myanmar",
            civilian_targeting_indiscriminate_attack_severity_score=56.0,
            siege_starvation_collective_punishment_scale_score=54.0,
            hospital_school_infrastructure_attack_score=55.0,
            humanitarian_access_aid_blockage_deficit_gap_score=57.0,
            primary_pattern="hospital_school_infrastructure_attack",
        ),
        ArmedConflictCivilianProtectionEntity(
            entity_id="ACP-006",
            name="Éthiopie/Tigré — Blocus Alimentaire 900 Jours, Massacres Axum/Mahbere Dego, Accès Humanitaire Refusé & Violences Sexuelles Arme Guerre",
            country="Éthiopie",
            civilian_targeting_indiscriminate_attack_severity_score=53.0,
            siege_starvation_collective_punishment_scale_score=51.0,
            hospital_school_infrastructure_attack_score=54.0,
            humanitarian_access_aid_blockage_deficit_gap_score=52.0,
            primary_pattern="siege_starvation_collective_punishment_scale",
        ),
        ArmedConflictCivilianProtectionEntity(
            entity_id="ACP-007",
            name="CICR/MSF — Droit International Humanitaire, Médecins Sans Frontières Protection & Comité CICR Supervision Conflits Armés",
            country="Global",
            civilian_targeting_indiscriminate_attack_severity_score=27.0,
            siege_starvation_collective_punishment_scale_score=25.0,
            hospital_school_infrastructure_attack_score=28.0,
            humanitarian_access_aid_blockage_deficit_gap_score=26.0,
            primary_pattern="humanitarian_access_aid_blockage_deficit_gap",
        ),
        ArmedConflictCivilianProtectionEntity(
            entity_id="ACP-008",
            name="ONU/Genève IV — Conventions Genève 1949 & Protocoles Additionnels, Rome Statute ICC & Standards DIH Minimaux",
            country="Global",
            civilian_targeting_indiscriminate_attack_severity_score=4.0,
            siege_starvation_collective_punishment_scale_score=4.0,
            hospital_school_infrastructure_attack_score=4.0,
            humanitarian_access_aid_blockage_deficit_gap_score=4.0,
            primary_pattern="civilian_targeting_indiscriminate_attack_severity",
        ),
    ]

    scores = [e.composite_score for e in entities]
    avg_composite = round(statistics.mean(scores), 2)

    distribution = {}
    for e in entities:
        distribution[e.risk_level] = distribution.get(e.risk_level, 0) + 1

    return ArmedConflictCivilianProtectionEngineResult(
        entities=entities,
        avg_composite=avg_composite,
        distribution=distribution,
        data_sources=[
            "icrc_international_humanitarian_law_report",
            "airwaves_civilian_harm_monitoring_report",
            "un_ocha_humanitarian_access_report",
        ],
        agent="Armed Conflict Civilian Protection Engine Agent",
    )


if __name__ == "__main__":
    result = run_armed_conflict_civilian_protection_engine()
    print(f"Agent: {result.agent}")
    print(f"avg_composite: {result.avg_composite}")
    print(f"Distribution: {result.distribution}")
    print()
    for e in result.entities:
        print(
            f"  [{e.entity_id}] {e.risk_level.upper():8s} | composite={e.composite_score:5.2f} | index={e.estimated_armed_conflict_civilian_protection_index} | {e.name[:60]}"
        )
