from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class DeathInCustodyPrisonConditionsEntity:
    entity_id: str
    name: str
    country: str
    death_in_custody_impunity_rate_score: float
    prison_overcrowding_inhumane_conditions_score: float
    pretrial_detention_abuse_score: float
    independent_monitoring_access_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_death_in_custody_prison_conditions_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.death_in_custody_impunity_rate_score * 0.30
            + self.prison_overcrowding_inhumane_conditions_score * 0.25
            + self.pretrial_detention_abuse_score * 0.25
            + self.independent_monitoring_access_gap_score * 0.20,
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
        self.estimated_death_in_custody_prison_conditions_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class DeathInCustodyPrisonConditionsEngineResult:
    agent: str = "Death In Custody Prison Conditions Engine Agent"
    domain: str = "death_in_custody_prison_conditions"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.88
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_death_in_custody_prison_conditions_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[DeathInCustodyPrisonConditionsEntity] = field(default_factory=list)


def run_death_in_custody_prison_conditions_engine() -> DeathInCustodyPrisonConditionsEngineResult:
    entities = [
        DeathInCustodyPrisonConditionsEntity(
            entity_id="DIC-001",
            name="Philippines — War on Drugs 2016-2022 : 6000+ Tués Détention/Opérations, EJK Documentés, SOCO Corrompus, Duterte ICC",
            country="Philippines",
            death_in_custody_impunity_rate_score=96.0,
            prison_overcrowding_inhumane_conditions_score=93.0,
            pretrial_detention_abuse_score=94.0,
            independent_monitoring_access_gap_score=92.0,
            primary_pattern="death_in_custody_impunity_rate",
        ),
        DeathInCustodyPrisonConditionsEntity(
            entity_id="DIC-002",
            name="Brésil/Pénitentiaires — 900K Détenus 3e Mondial, Carandiru Héritage, 2017 Manaus Massacres, Facções Contrôlent Prisons",
            country="Brésil",
            death_in_custody_impunity_rate_score=90.0,
            prison_overcrowding_inhumane_conditions_score=92.0,
            pretrial_detention_abuse_score=88.0,
            independent_monitoring_access_gap_score=86.0,
            primary_pattern="prison_overcrowding_inhumane_conditions",
        ),
        DeathInCustodyPrisonConditionsEntity(
            entity_id="DIC-003",
            name="USA/Mass Incarceration — 2.1M Détenus 1er Mondial, Conditions Rikers Island, George Floyd Préfigure, Mort Garde 2022",
            country="USA",
            death_in_custody_impunity_rate_score=82.0,
            prison_overcrowding_inhumane_conditions_score=80.0,
            pretrial_detention_abuse_score=83.0,
            independent_monitoring_access_gap_score=78.0,
            primary_pattern="pretrial_detention_abuse",
        ),
        DeathInCustodyPrisonConditionsEntity(
            entity_id="DIC-004",
            name="Venezuela — Helicoide, Tocuyito Surpopulation 400%, Colectivos Contrôlent Centres, CIDH Rapports Alarmants",
            country="Venezuela",
            death_in_custody_impunity_rate_score=88.0,
            prison_overcrowding_inhumane_conditions_score=91.0,
            pretrial_detention_abuse_score=89.0,
            independent_monitoring_access_gap_score=90.0,
            primary_pattern="independent_monitoring_access_gap",
        ),
        DeathInCustodyPrisonConditionsEntity(
            entity_id="DIC-005",
            name="Pakistan — 90K Détenus pour 55K Places, Gardiens Torturent, 200+ Morts/An Garde à Vue, CPT Accès Refusé",
            country="Pakistan",
            death_in_custody_impunity_rate_score=54.0,
            prison_overcrowding_inhumane_conditions_score=57.0,
            pretrial_detention_abuse_score=59.0,
            independent_monitoring_access_gap_score=60.0,
            primary_pattern="pretrial_detention_abuse",
        ),
        DeathInCustodyPrisonConditionsEntity(
            entity_id="DIC-006",
            name="Cambodge — Prisons Surpeuplées 300%, Prévenus 80% Population Carcérale, COVID Morts Sans Soins 2021",
            country="Cambodge",
            death_in_custody_impunity_rate_score=50.0,
            prison_overcrowding_inhumane_conditions_score=55.0,
            pretrial_detention_abuse_score=56.0,
            independent_monitoring_access_gap_score=53.0,
            primary_pattern="prison_overcrowding_inhumane_conditions",
        ),
        DeathInCustodyPrisonConditionsEntity(
            entity_id="DIC-007",
            name="Mexique — Cefereso Surpopulation, Cartels Corrompent Direction, Puente Grande Conditions CIDH, Moniteurs Sporadiques",
            country="Mexique",
            death_in_custody_impunity_rate_score=30.0,
            prison_overcrowding_inhumane_conditions_score=32.0,
            pretrial_detention_abuse_score=28.0,
            independent_monitoring_access_gap_score=33.0,
            primary_pattern="independent_monitoring_access_gap",
        ),
        DeathInCustodyPrisonConditionsEntity(
            entity_id="DIC-008",
            name="Norvège/Halden — Standard Mondial Humanisation, Cellules Singles, Soins Santé, Réhabilitation 20% Récidive",
            country="Norvège",
            death_in_custody_impunity_rate_score=4.0,
            prison_overcrowding_inhumane_conditions_score=3.0,
            pretrial_detention_abuse_score=4.0,
            independent_monitoring_access_gap_score=3.0,
            primary_pattern="death_in_custody_impunity_rate",
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

    return DeathInCustodyPrisonConditionsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_death_in_custody_prison_conditions_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_special_rapporteur_torture_detention_2023",
            "penal_reform_international_global_prison_trends_2023",
            "amnesty_international_death_in_custody_2023",
            "human_rights_watch_prison_conditions_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_death_in_custody_prison_conditions_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_death_in_custody_prison_conditions_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
