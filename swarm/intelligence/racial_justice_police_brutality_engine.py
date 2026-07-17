from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class RacialJuticePoliceBrutalityEntity:
    entity_id: str
    name: str
    country: str
    police_killings_racial_disparity_score: float
    mass_incarceration_racial_targeting_score: float
    racial_profiling_stop_search_score: float
    accountability_impunity_systemic_racism_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_racial_justice_police_brutality_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.police_killings_racial_disparity_score * 0.30
            + self.mass_incarceration_racial_targeting_score * 0.25
            + self.racial_profiling_stop_search_score * 0.25
            + self.accountability_impunity_systemic_racism_score * 0.20,
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
        self.estimated_racial_justice_police_brutality_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class RacialJuticePoliceBrutalityEngineResult:
    agent: str = "Racial Justice Police Brutality Engine Agent"
    domain: str = "racial_justice_police_brutality"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.88
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_racial_justice_police_brutality_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[RacialJuticePoliceBrutalityEntity] = field(default_factory=list)


def run_racial_justice_police_brutality_engine() -> RacialJuticePoliceBrutalityEngineResult:
    entities = [
        RacialJuticePoliceBrutalityEntity(
            entity_id="RJP-001",
            name="USA — 1000+ Tués/An Police, Noirs 3x Plus Ciblés, Mass Incarceration 2.3M, George Floyd & Impunité Systémique",
            country="USA",
            police_killings_racial_disparity_score=92.0,
            mass_incarceration_racial_targeting_score=91.0,
            racial_profiling_stop_search_score=88.0,
            accountability_impunity_systemic_racism_score=90.0,
            primary_pattern="mass_incarceration_racial_targeting",
        ),
        RacialJuticePoliceBrutalityEntity(
            entity_id="RJP-002",
            name="Brésil — 6000+ Tués Police/An dont 80% Noirs, Favelas Militarisées, Marielle Franco Assassinée & Rio Opérations",
            country="Brésil",
            police_killings_racial_disparity_score=94.0,
            mass_incarceration_racial_targeting_score=88.0,
            racial_profiling_stop_search_score=87.0,
            accountability_impunity_systemic_racism_score=91.0,
            primary_pattern="police_killings_racial_disparity",
        ),
        RacialJuticePoliceBrutalityEntity(
            entity_id="RJP-003",
            name="Kenya — IPOA 700+ Plaintes Brutalité 2022, COVID Couvre-Feu Meurtres Impunis & Manifestations 2024 Tirs Létaux",
            country="Kenya",
            police_killings_racial_disparity_score=85.0,
            mass_incarceration_racial_targeting_score=80.0,
            racial_profiling_stop_search_score=82.0,
            accountability_impunity_systemic_racism_score=88.0,
            primary_pattern="accountability_impunity_systemic_racism",
        ),
        RacialJuticePoliceBrutalityEntity(
            entity_id="RJP-004",
            name="Philippines — Guerre Drogues 30K+ Tués 2016-2022, Pauvres/Minorités Ciblés, Duterte ICC Enquête",
            country="Philippines",
            police_killings_racial_disparity_score=88.0,
            mass_incarceration_racial_targeting_score=84.0,
            racial_profiling_stop_search_score=80.0,
            accountability_impunity_systemic_racism_score=90.0,
            primary_pattern="police_killings_racial_disparity",
        ),
        RacialJuticePoliceBrutalityEntity(
            entity_id="RJP-005",
            name="France — Profilage Racial Documenté Défenseur Droits, Nahel Tué 2023, 13 Tués Police/An & Violences Maintien Ordre",
            country="France",
            police_killings_racial_disparity_score=58.0,
            mass_incarceration_racial_targeting_score=52.0,
            racial_profiling_stop_search_score=62.0,
            accountability_impunity_systemic_racism_score=55.0,
            primary_pattern="racial_profiling_stop_search",
        ),
        RacialJuticePoliceBrutalityEntity(
            entity_id="RJP-006",
            name="Royaume-Uni — Windrush Scandal, Stop & Search 10x Plus Noirs, Deaths in Custody Impunies & Macpherson Report Non-Suivi",
            country="Royaume-Uni",
            police_killings_racial_disparity_score=50.0,
            mass_incarceration_racial_targeting_score=55.0,
            racial_profiling_stop_search_score=60.0,
            accountability_impunity_systemic_racism_score=52.0,
            primary_pattern="racial_profiling_stop_search",
        ),
        RacialJuticePoliceBrutalityEntity(
            entity_id="RJP-007",
            name="Canada — Autochtones Surreprésentés Détention 5x, Enquête MMIWG & Quelques Réformes Police Post-2020",
            country="Canada",
            police_killings_racial_disparity_score=32.0,
            mass_incarceration_racial_targeting_score=38.0,
            racial_profiling_stop_search_score=35.0,
            accountability_impunity_systemic_racism_score=30.0,
            primary_pattern="mass_incarceration_racial_targeting",
        ),
        RacialJuticePoliceBrutalityEntity(
            entity_id="RJP-008",
            name="Nouvelle-Zélande — Données Raciales Policing Transparentes, Commission Waitangi Active & Réformes Progressives Réelles",
            country="Nouvelle-Zélande",
            police_killings_racial_disparity_score=12.0,
            mass_incarceration_racial_targeting_score=15.0,
            racial_profiling_stop_search_score=14.0,
            accountability_impunity_systemic_racism_score=10.0,
            primary_pattern="police_killings_racial_disparity",
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

    return RacialJuticePoliceBrutalityEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_racial_justice_police_brutality_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "mapping_police_violence_database_2023",
            "human_rights_watch_racial_justice_2023",
            "amnesty_international_police_brutality_2023",
            "un_special_rapporteur_racism_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_racial_justice_police_brutality_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_racial_justice_police_brutality_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
