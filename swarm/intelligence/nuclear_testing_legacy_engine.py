from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class NuclearTestingLegacyEntity:
    entity_id: str
    name: str
    country: str
    radiation_contamination_scale_score: float
    health_cancer_mortality_score: float
    displaced_communities_score: float
    state_denial_reparations_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_nuclear_testing_legacy_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.radiation_contamination_scale_score * 0.30
            + self.health_cancer_mortality_score * 0.25
            + self.displaced_communities_score * 0.25
            + self.state_denial_reparations_score * 0.20,
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
        self.estimated_nuclear_testing_legacy_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class NuclearTestingLegacyEngineResult:
    agent: str = "Nuclear Testing Legacy Engine Agent"
    domain: str = "nuclear_testing_legacy"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_nuclear_testing_legacy_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[NuclearTestingLegacyEntity] = field(default_factory=list)

def run_nuclear_testing_legacy_engine() -> NuclearTestingLegacyEngineResult:
    entities = [
        NuclearTestingLegacyEntity(
            entity_id="NT-001",
            name="Marshall Islands/USA — 67 Tests Bikini/Enewetak, Populations Irradiées & Déni Compensation",
            country="Océanie/Amérique du Nord",
            radiation_contamination_scale_score=92.0,
            health_cancer_mortality_score=90.0,
            displaced_communities_score=88.0,
            state_denial_reparations_score=88.0,
            primary_pattern="radiation_contamination_scale",
        ),
        NuclearTestingLegacyEntity(
            entity_id="NT-002",
            name="Kazakhstan/URSS — 456 Tests Semipalatinsk, 1,5M Irradiés & Cancers Générationnels",
            country="Asie Centrale",
            radiation_contamination_scale_score=88.0,
            health_cancer_mortality_score=85.0,
            displaced_communities_score=82.0,
            state_denial_reparations_score=85.0,
            primary_pattern="health_cancer_mortality",
        ),
        NuclearTestingLegacyEntity(
            entity_id="NT-003",
            name="Algérie/France — 17 Tests Reggane/Hamoudia, Populations Touareg Contaminées & Secret Défense",
            country="Afrique du Nord",
            radiation_contamination_scale_score=82.0,
            health_cancer_mortality_score=80.0,
            displaced_communities_score=85.0,
            state_denial_reparations_score=88.0,
            primary_pattern="state_denial_reparations",
        ),
        NuclearTestingLegacyEntity(
            entity_id="NT-004",
            name="Polynésie/France — 193 Tests Mururoa/Fangataufa, Vétérans Malades & Indemnisation Minime",
            country="Océanie/France",
            radiation_contamination_scale_score=80.0,
            health_cancer_mortality_score=82.0,
            displaced_communities_score=78.0,
            state_denial_reparations_score=82.0,
            primary_pattern="health_cancer_mortality",
        ),
        NuclearTestingLegacyEntity(
            entity_id="NT-005",
            name="USA/Nevada — Downwinders, Communautés Mormons Irradiées & RECA Compensation Partielle",
            country="Amérique du Nord",
            radiation_contamination_scale_score=52.0,
            health_cancer_mortality_score=55.0,
            displaced_communities_score=50.0,
            state_denial_reparations_score=58.0,
            primary_pattern="state_denial_reparations",
        ),
        NuclearTestingLegacyEntity(
            entity_id="NT-006",
            name="Australie/UK — 12 Tests Maralinga, Peuple Anangu Déplacé & Décontamination Incomplète",
            country="Océanie",
            radiation_contamination_scale_score=48.0,
            health_cancer_mortality_score=52.0,
            displaced_communities_score=55.0,
            state_denial_reparations_score=50.0,
            primary_pattern="displaced_communities",
        ),
        NuclearTestingLegacyEntity(
            entity_id="NT-007",
            name="TPNW/TICE — Traité Interdiction Tests, Compensation Victimes & Assainissement Sites",
            country="Global",
            radiation_contamination_scale_score=22.0,
            health_cancer_mortality_score=28.0,
            displaced_communities_score=30.0,
            state_denial_reparations_score=25.0,
            primary_pattern="radiation_contamination_scale",
        ),
        NuclearTestingLegacyEntity(
            entity_id="NT-008",
            name="ONU/UNSCEAR — Comité Effets Rayonnements Ionisants, Rapports Scientifiques & Suivi",
            country="Global",
            radiation_contamination_scale_score=4.0,
            health_cancer_mortality_score=5.0,
            displaced_communities_score=3.0,
            state_denial_reparations_score=6.0,
            primary_pattern="displaced_communities",
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

    return NuclearTestingLegacyEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_nuclear_testing_legacy_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ican_nuclear_testing_humanitarian_consequences_global_report",
            "atomic_heritage_foundation_nuclear_testing_legacy_database",
            "tpnw_treaty_prohibition_nuclear_weapons_victim_assistance_article_6_7",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_nuclear_testing_legacy_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_nuclear_testing_legacy_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
