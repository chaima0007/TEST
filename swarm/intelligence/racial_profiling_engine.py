from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class RacialProfilingEntity:
    entity_id: str
    name: str
    country: str
    stop_search_racial_disparity_score: float
    criminal_justice_bias_score: float
    surveillance_targeting_race_score: float
    accountability_reform_absence_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_racial_profiling_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.stop_search_racial_disparity_score * 0.30
            + self.criminal_justice_bias_score * 0.25
            + self.surveillance_targeting_race_score * 0.25
            + self.accountability_reform_absence_score * 0.20,
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
        self.estimated_racial_profiling_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class RacialProfilingEngineResult:
    agent: str = "Racial Profiling Engine Agent"
    domain: str = "racial_profiling"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_racial_profiling_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[RacialProfilingEntity] = field(default_factory=list)

def run_racial_profiling_engine() -> RacialProfilingEngineResult:
    entities = [
        RacialProfilingEntity(
            entity_id="RP-001",
            name="USA — Stop & Frisk NYC, Noirs 3x Plus Arrêtés Drogues, Mass Incarceration & Ferguson",
            country="Amérique du Nord",
            stop_search_racial_disparity_score=95.0,
            criminal_justice_bias_score=92.0,
            surveillance_targeting_race_score=95.0,
            accountability_reform_absence_score=90.0,
            primary_pattern="stop_search_racial_disparity",
        ),
        RacialProfilingEntity(
            entity_id="RP-002",
            name="France — Contrôles Faciès CNDS, Noirs/Arabes 6-8x Plus Contrôlés & IGPN Défaillante",
            country="Europe",
            stop_search_racial_disparity_score=88.0,
            criminal_justice_bias_score=88.0,
            surveillance_targeting_race_score=90.0,
            accountability_reform_absence_score=92.0,
            primary_pattern="accountability_reform_absence",
        ),
        RacialProfilingEntity(
            entity_id="RP-003",
            name="UK — Section 60 Stop&Search, Noirs 8x Plus Contrôlés & Metropolitan Police Casey Report",
            country="Europe",
            stop_search_racial_disparity_score=85.0,
            criminal_justice_bias_score=88.0,
            surveillance_targeting_race_score=88.0,
            accountability_reform_absence_score=88.0,
            primary_pattern="criminal_justice_bias",
        ),
        RacialProfilingEntity(
            entity_id="RP-004",
            name="Australie — Aboriginal Surincarcération 27x, Profilage Racial Police & Deaths in Custody",
            country="Océanie",
            stop_search_racial_disparity_score=82.0,
            criminal_justice_bias_score=90.0,
            surveillance_targeting_race_score=82.0,
            accountability_reform_absence_score=85.0,
            primary_pattern="criminal_justice_bias",
        ),
        RacialProfilingEntity(
            entity_id="RP-005",
            name="Canada — Carding Toronto, Noirs/Autochtones Suiciblés, Rapport Waller & Réformes Lentes",
            country="Amérique du Nord",
            stop_search_racial_disparity_score=52.0,
            criminal_justice_bias_score=55.0,
            surveillance_targeting_race_score=52.0,
            accountability_reform_absence_score=58.0,
            primary_pattern="accountability_reform_absence",
        ),
        RacialProfilingEntity(
            entity_id="RP-006",
            name="Espagne — Frontière Melilla Profilage Migrants, Refoulements Collectifs & Racisme Institutionnel",
            country="Europe",
            stop_search_racial_disparity_score=48.0,
            criminal_justice_bias_score=52.0,
            surveillance_targeting_race_score=50.0,
            accountability_reform_absence_score=50.0,
            primary_pattern="criminal_justice_bias",
        ),
        RacialProfilingEntity(
            entity_id="RP-007",
            name="Open Society Justice Initiative/ECRI — Rapport Profilage Racial & Standards Européens",
            country="Global",
            stop_search_racial_disparity_score=22.0,
            criminal_justice_bias_score=25.0,
            surveillance_targeting_race_score=28.0,
            accountability_reform_absence_score=30.0,
            primary_pattern="accountability_reform_absence",
        ),
        RacialProfilingEntity(
            entity_id="RP-008",
            name="ONU/CERD — Art.5 Non-Discrimination, Recommandation Générale XXXI Profilage Racial",
            country="Global",
            stop_search_racial_disparity_score=4.0,
            criminal_justice_bias_score=5.0,
            surveillance_targeting_race_score=3.0,
            accountability_reform_absence_score=6.0,
            primary_pattern="surveillance_targeting_race",
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

    return RacialProfilingEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_racial_profiling_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "open_society_justice_initiative_ethnic_profiling_europe_report",
            "ecri_council_europe_racial_profiling_recommendations",
            "mapping_police_violence_racial_disparity_database",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_racial_profiling_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_racial_profiling_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
