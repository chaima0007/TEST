from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class RacialDiscriminationSystemicRacismEntity:
    entity_id: str
    name: str
    country: str
    racial_profiling_police_brutality_severity_score: float
    systemic_economic_housing_discrimination_scale_score: float
    hate_crime_racial_violence_impunity_score: float
    anti_racism_policy_reparation_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_racial_discrimination_systemic_racism_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.racial_profiling_police_brutality_severity_score * 0.30
            + self.systemic_economic_housing_discrimination_scale_score * 0.25
            + self.hate_crime_racial_violence_impunity_score * 0.25
            + self.anti_racism_policy_reparation_deficit_gap_score * 0.20,
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
        self.estimated_racial_discrimination_systemic_racism_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class RacialDiscriminationSystemicRacismEngineResult:
    entities: List[RacialDiscriminationSystemicRacismEntity]
    avg_composite: float
    distribution: dict
    data_sources: List[str]
    agent: str


def run_racial_discrimination_systemic_racism_engine() -> RacialDiscriminationSystemicRacismEngineResult:
    entities = [
        RacialDiscriminationSystemicRacismEntity(
            entity_id="RDS-001",
            name="USA/Apartheid Héritage — George Floyd 1 000 Noirs Tués Police/An, Mass Incarceration 40% Noir, Redlining Persistant & Reparations Bloquées",
            country="USA",
            racial_profiling_police_brutality_severity_score=94.0,
            systemic_economic_housing_discrimination_scale_score=92.0,
            hate_crime_racial_violence_impunity_score=93.0,
            anti_racism_policy_reparation_deficit_gap_score=91.0,
            primary_pattern="racial_profiling_police_brutality_severity",
        ),
        RacialDiscriminationSystemicRacismEntity(
            entity_id="RDS-002",
            name="Brésil/Dalit Noirs — 75% Victimes Homicides Noirs, Police Favela Opération Morro João Pedro, Quilombolas Expulsés & Quota Contourné",
            country="Brésil",
            racial_profiling_police_brutality_severity_score=90.0,
            systemic_economic_housing_discrimination_scale_score=89.0,
            hate_crime_racial_violence_impunity_score=92.0,
            anti_racism_policy_reparation_deficit_gap_score=88.0,
            primary_pattern="racial_profiling_police_brutality_severity",
        ),
        RacialDiscriminationSystemicRacismEntity(
            entity_id="RDS-003",
            name="Inde/Caste-Race — Dalits 165M, Violences Caste 50 000/An, Endogamie Forcée & Discrimination Emploi Systémique",
            country="Inde",
            racial_profiling_police_brutality_severity_score=87.0,
            systemic_economic_housing_discrimination_scale_score=88.0,
            hate_crime_racial_violence_impunity_score=85.0,
            anti_racism_policy_reparation_deficit_gap_score=86.0,
            primary_pattern="systemic_economic_housing_discrimination_scale",
        ),
        RacialDiscriminationSystemicRacismEntity(
            entity_id="RDS-004",
            name="Europe/Roms — Roms Expulsions France/Italie, Stérilisation Forcée Slovaquie, Écoles Séparées & Discrimination Logement Légal",
            country="Europe",
            racial_profiling_police_brutality_severity_score=83.0,
            systemic_economic_housing_discrimination_scale_score=84.0,
            hate_crime_racial_violence_impunity_score=81.0,
            anti_racism_policy_reparation_deficit_gap_score=82.0,
            primary_pattern="systemic_economic_housing_discrimination_scale",
        ),
        RacialDiscriminationSystemicRacismEntity(
            entity_id="RDS-005",
            name="Israël/Arabes — Loi Nation-État 2018, Planification Discriminatoire, Arabes-Israéliens 20% Citoyens Inégaux & Bédouins Villages Non-Reconnus",
            country="Israël",
            racial_profiling_police_brutality_severity_score=56.0,
            systemic_economic_housing_discrimination_scale_score=54.0,
            hate_crime_racial_violence_impunity_score=55.0,
            anti_racism_policy_reparation_deficit_gap_score=57.0,
            primary_pattern="anti_racism_policy_reparation_deficit_gap",
        ),
        RacialDiscriminationSystemicRacismEntity(
            entity_id="RDS-006",
            name="Australie/Aborigènes — Incarcération 15× Moyenne, Décès Garde Policière, Enfants Retirés 20 000 & Pas Traité Constitutionnel",
            country="Australie",
            racial_profiling_police_brutality_severity_score=52.0,
            systemic_economic_housing_discrimination_scale_score=51.0,
            hate_crime_racial_violence_impunity_score=54.0,
            anti_racism_policy_reparation_deficit_gap_score=53.0,
            primary_pattern="racial_profiling_police_brutality_severity",
        ),
        RacialDiscriminationSystemicRacismEntity(
            entity_id="RDS-007",
            name="ECRI/CERD — Commission Européenne Contre Racisme, Comité ONU Élimination Discrimination Raciale & Réseau Europeen Anti-Racisme",
            country="Global",
            racial_profiling_police_brutality_severity_score=27.0,
            systemic_economic_housing_discrimination_scale_score=25.0,
            hate_crime_racial_violence_impunity_score=28.0,
            anti_racism_policy_reparation_deficit_gap_score=26.0,
            primary_pattern="anti_racism_policy_reparation_deficit_gap",
        ),
        RacialDiscriminationSystemicRacismEntity(
            entity_id="RDS-008",
            name="ONU/CERD 1965 — Convention Élimination Discrimination Raciale 1965, DDPA Durban 2001 & SDG 10.3 Inégalités",
            country="Global",
            racial_profiling_police_brutality_severity_score=4.0,
            systemic_economic_housing_discrimination_scale_score=4.0,
            hate_crime_racial_violence_impunity_score=4.0,
            anti_racism_policy_reparation_deficit_gap_score=4.0,
            primary_pattern="racial_profiling_police_brutality_severity",
        ),
    ]

    scores = [e.composite_score for e in entities]
    avg_composite = round(statistics.mean(scores), 2)

    distribution = {}
    for e in entities:
        distribution[e.risk_level] = distribution.get(e.risk_level, 0) + 1

    return RacialDiscriminationSystemicRacismEngineResult(
        entities=entities,
        avg_composite=avg_composite,
        distribution=distribution,
        data_sources=[
            "un_cerd_racial_discrimination_report",
            "human_rights_watch_racial_profiling_report",
            "amnesty_international_systemic_racism_report",
        ],
        agent="Racial Discrimination Systemic Racism Engine Agent",
    )


if __name__ == "__main__":
    result = run_racial_discrimination_systemic_racism_engine()
    print(f"Agent: {result.agent}")
    print(f"avg_composite: {result.avg_composite}")
    print(f"Distribution: {result.distribution}")
    print()
    for e in result.entities:
        print(
            f"  [{e.entity_id}] {e.risk_level.upper():8s} | composite={e.composite_score:5.2f} | index={e.estimated_racial_discrimination_systemic_racism_index} | {e.name[:60]}"
        )
