from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class HumanTraffickingEntity:
    entity_id: str
    name: str
    country: str
    labor_sex_exploitation_scale_score: float
    border_recruitment_deception_score: float
    victim_identification_failure_score: float
    prosecution_conviction_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_human_trafficking_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.labor_sex_exploitation_scale_score * 0.30
            + self.border_recruitment_deception_score * 0.25
            + self.victim_identification_failure_score * 0.25
            + self.prosecution_conviction_gap_score * 0.20,
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
        self.estimated_human_trafficking_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class HumanTraffickingEngineResult:
    agent: str = "Human Trafficking Engine Agent"
    domain: str = "human_trafficking"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_human_trafficking_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[HumanTraffickingEntity] = field(default_factory=list)

def run_human_trafficking_engine() -> HumanTraffickingEngineResult:
    entities = [
        HumanTraffickingEntity(
            entity_id="HT-001",
            name="Asie du Sud-Est/Arnaques Téléphoniques — Esclavage Moderne Myanmar/Cambodge, 100K Forcés Centres Fraude",
            country="Asie du Sud-Est",
            labor_sex_exploitation_scale_score=92.0,
            border_recruitment_deception_score=95.0,
            victim_identification_failure_score=90.0,
            prosecution_conviction_gap_score=88.0,
            primary_pattern="border_recruitment_deception",
        ),
        HumanTraffickingEntity(
            entity_id="HT-002",
            name="Moyen-Orient/Kafala — Travailleurs Domestiques Piégés, Passeports Confisqués & Travail Forcé",
            country="Moyen-Orient",
            labor_sex_exploitation_scale_score=88.0,
            border_recruitment_deception_score=85.0,
            victim_identification_failure_score=88.0,
            prosecution_conviction_gap_score=85.0,
            primary_pattern="labor_sex_exploitation_scale",
        ),
        HumanTraffickingEntity(
            entity_id="HT-003",
            name="Europe/Balkans — Réseaux Prostitution Forcée Roumanie/Bulgarie, Mafia & Corridors Trafic",
            country="Europe",
            labor_sex_exploitation_scale_score=82.0,
            border_recruitment_deception_score=85.0,
            victim_identification_failure_score=82.0,
            prosecution_conviction_gap_score=80.0,
            primary_pattern="border_recruitment_deception",
        ),
        HumanTraffickingEntity(
            entity_id="HT-004",
            name="Libye/Méditerranée — Migrants Torturés/Vendus Geôliers, Rançons Familles & Travail Forcé",
            country="Afrique du Nord",
            labor_sex_exploitation_scale_score=80.0,
            border_recruitment_deception_score=78.0,
            victim_identification_failure_score=85.0,
            prosecution_conviction_gap_score=82.0,
            primary_pattern="victim_identification_failure",
        ),
        HumanTraffickingEntity(
            entity_id="HT-005",
            name="USA — Travail Agricole Forcé, Exploitation Sexuelle Mineurs & Identification Victimes Lacunaire",
            country="Amérique du Nord",
            labor_sex_exploitation_scale_score=52.0,
            border_recruitment_deception_score=55.0,
            victim_identification_failure_score=58.0,
            prosecution_conviction_gap_score=50.0,
            primary_pattern="victim_identification_failure",
        ),
        HumanTraffickingEntity(
            entity_id="HT-006",
            name="Inde/Népal — Traite Femmes/Filles Vers Mumbai/Delhi, Mariages Forcés & Travail Domestique",
            country="Asie du Sud",
            labor_sex_exploitation_scale_score=50.0,
            border_recruitment_deception_score=52.0,
            victim_identification_failure_score=55.0,
            prosecution_conviction_gap_score=48.0,
            primary_pattern="prosecution_conviction_gap",
        ),
        HumanTraffickingEntity(
            entity_id="HT-007",
            name="La Strada/Polaris — ONG Anti-Traite, Lignes Écoute, Refuges & Plaidoyer Politique",
            country="Global",
            labor_sex_exploitation_scale_score=22.0,
            border_recruitment_deception_score=25.0,
            victim_identification_failure_score=28.0,
            prosecution_conviction_gap_score=30.0,
            primary_pattern="labor_sex_exploitation_scale",
        ),
        HumanTraffickingEntity(
            entity_id="HT-008",
            name="ONU/Protocole Palermo — Convention Crime Organisé, Définition Traite & Standards Protection",
            country="Global",
            labor_sex_exploitation_scale_score=4.0,
            border_recruitment_deception_score=5.0,
            victim_identification_failure_score=3.0,
            prosecution_conviction_gap_score=6.0,
            primary_pattern="prosecution_conviction_gap",
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

    return HumanTraffickingEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_human_trafficking_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unodc_global_report_trafficking_persons_2024",
            "ilo_forced_labour_modern_slavery_global_estimates_report",
            "polaris_project_human_trafficking_trends_annual_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_human_trafficking_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_human_trafficking_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
