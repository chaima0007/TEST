from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class InternetShutdownEntity:
    entity_id: str
    name: str
    country: str
    shutdown_duration_frequency_score: float
    economic_civil_harm_score: float
    political_protest_targeting_score: float
    legal_accountability_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_internet_shutdown_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.shutdown_duration_frequency_score * 0.30
            + self.economic_civil_harm_score * 0.25
            + self.political_protest_targeting_score * 0.25
            + self.legal_accountability_gap_score * 0.20,
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
        self.estimated_internet_shutdown_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class InternetShutdownEngineResult:
    agent: str = "Internet Shutdown Engine Agent"
    domain: str = "internet_shutdown"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_internet_shutdown_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[InternetShutdownEntity] = field(default_factory=list)

def run_internet_shutdown_engine() -> InternetShutdownEngineResult:
    entities = [
        InternetShutdownEntity(
            entity_id="IS-001",
            name="Myanmar — Coupures Post-Coup 2021, 4 Ans Restrictions & Populations Rurales Isolées",
            country="Asie du Sud-Est",
            shutdown_duration_frequency_score=95.0,
            economic_civil_harm_score=90.0,
            political_protest_targeting_score=95.0,
            legal_accountability_gap_score=92.0,
            primary_pattern="shutdown_duration_frequency",
        ),
        InternetShutdownEntity(
            entity_id="IS-002",
            name="Éthiopie/Tigray — Coupure 2 Ans Guerre, Génocide Sans Témoins & Humanitaire Aveugle",
            country="Afrique de l'Est",
            shutdown_duration_frequency_score=88.0,
            economic_civil_harm_score=88.0,
            political_protest_targeting_score=92.0,
            legal_accountability_gap_score=88.0,
            primary_pattern="political_protest_targeting",
        ),
        InternetShutdownEntity(
            entity_id="IS-003",
            name="Inde/Cachemire — Coupure 213 Jours Record Mondial, Répression Post-Art.370 & Presse Muselée",
            country="Asie du Sud",
            shutdown_duration_frequency_score=90.0,
            economic_civil_harm_score=85.0,
            political_protest_targeting_score=88.0,
            legal_accountability_gap_score=82.0,
            primary_pattern="shutdown_duration_frequency",
        ),
        InternetShutdownEntity(
            entity_id="IS-004",
            name="Iran — Coupures Systématiques Protestations, Mahsa Amini 2022 & Blocages Plateformes",
            country="Moyen-Orient",
            shutdown_duration_frequency_score=82.0,
            economic_civil_harm_score=80.0,
            political_protest_targeting_score=85.0,
            legal_accountability_gap_score=82.0,
            primary_pattern="political_protest_targeting",
        ),
        InternetShutdownEntity(
            entity_id="IS-005",
            name="Afrique/Élections — Coupures Cameroun/Mali/Tchad Périodes Électorales & Manipulation Info",
            country="Afrique Sub-Saharienne",
            shutdown_duration_frequency_score=52.0,
            economic_civil_harm_score=55.0,
            political_protest_targeting_score=58.0,
            legal_accountability_gap_score=52.0,
            primary_pattern="political_protest_targeting",
        ),
        InternetShutdownEntity(
            entity_id="IS-006",
            name="Russie/Ukraine — Blocages RT/Médias, DPI Technologie Surveillance & Internet Souverain RuNet",
            country="Europe de l'Est",
            shutdown_duration_frequency_score=48.0,
            economic_civil_harm_score=52.0,
            political_protest_targeting_score=55.0,
            legal_accountability_gap_score=50.0,
            primary_pattern="legal_accountability_gap",
        ),
        InternetShutdownEntity(
            entity_id="IS-007",
            name="Access Now/NetBlocks — ONG Détection Coupures, Alertes Temps Réel & Plaidoyer Global",
            country="Global",
            shutdown_duration_frequency_score=22.0,
            economic_civil_harm_score=25.0,
            political_protest_targeting_score=28.0,
            legal_accountability_gap_score=30.0,
            primary_pattern="shutdown_duration_frequency",
        ),
        InternetShutdownEntity(
            entity_id="IS-008",
            name="ONU/IGF — Forum Gouvernance Internet, Résolutions Liberté Expression & Normes Non Contraignantes",
            country="Global",
            shutdown_duration_frequency_score=4.0,
            economic_civil_harm_score=5.0,
            political_protest_targeting_score=3.0,
            legal_accountability_gap_score=6.0,
            primary_pattern="legal_accountability_gap",
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

    return InternetShutdownEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_internet_shutdown_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "access_now_keepiton_internet_shutdowns_annual_report",
            "netblocks_cost_internet_shutdowns_global_tracker",
            "freedom_house_freedom_net_global_internet_freedom_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_internet_shutdown_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_internet_shutdown_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
