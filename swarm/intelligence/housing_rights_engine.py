from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class HousingRightsEntity:
    entity_id: str
    name: str
    country: str
    forced_eviction_displacement_severity_score: float
    homelessness_inadequate_housing_scale_score: float
    housing_discrimination_marginalized_score: float
    rent_speculation_financialization_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_housing_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.forced_eviction_displacement_severity_score * 0.30
            + self.homelessness_inadequate_housing_scale_score * 0.25
            + self.housing_discrimination_marginalized_score * 0.25
            + self.rent_speculation_financialization_gap_score * 0.20,
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
        self.estimated_housing_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class HousingRightsEngineResult:
    agent: str = "Housing Rights Engine Agent"
    domain: str = "housing_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_housing_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[HousingRightsEntity] = field(default_factory=list)

def run_housing_rights_engine() -> HousingRightsEngineResult:
    entities = [
        HousingRightsEntity(
            entity_id="HR-001",
            name="Kenya/Nairobi — Kibera 700k Habitants Bidonvilles, Expulsions Bulldozer Sans Préavis & Zéro Relogement",
            country="Kenya",
            forced_eviction_displacement_severity_score=95.0,
            homelessness_inadequate_housing_scale_score=92.0,
            housing_discrimination_marginalized_score=93.0,
            rent_speculation_financialization_gap_score=91.0,
            primary_pattern="forced_eviction_displacement_severity",
        ),
        HousingRightsEntity(
            entity_id="HR-002",
            name="Philippines — 3,1M Sans Abri Manille, Expulsions Duterte Drug War & Bidonvilles Inondables",
            country="Philippines",
            forced_eviction_displacement_severity_score=92.0,
            homelessness_inadequate_housing_scale_score=89.0,
            housing_discrimination_marginalized_score=90.0,
            rent_speculation_financialization_gap_score=87.0,
            primary_pattern="forced_eviction_displacement_severity",
        ),
        HousingRightsEntity(
            entity_id="HR-003",
            name="India — 5M Expulsés Projets Infra/Jeux, DUSIB Delhi Démolitions & Dalits/Tribaux Ciblés",
            country="Inde",
            forced_eviction_displacement_severity_score=89.0,
            homelessness_inadequate_housing_scale_score=86.0,
            housing_discrimination_marginalized_score=87.0,
            rent_speculation_financialization_gap_score=84.0,
            primary_pattern="housing_discrimination_marginalized",
        ),
        HousingRightsEntity(
            entity_id="HR-004",
            name="Brazil/Rio — Favelas Pacification Expulsions Forcées, Spéculation Immobilière & Gentrification Olympique",
            country="Brésil",
            forced_eviction_displacement_severity_score=86.0,
            homelessness_inadequate_housing_scale_score=83.0,
            housing_discrimination_marginalized_score=84.0,
            rent_speculation_financialization_gap_score=82.0,
            primary_pattern="rent_speculation_financialization_gap",
        ),
        HousingRightsEntity(
            entity_id="HR-005",
            name="USA — 650k Sans Abri, Sweeps Campements & Criminalization Homelessness Anti-Camping Laws",
            country="USA",
            forced_eviction_displacement_severity_score=55.0,
            homelessness_inadequate_housing_scale_score=53.0,
            housing_discrimination_marginalized_score=52.0,
            rent_speculation_financialization_gap_score=51.0,
            primary_pattern="homelessness_inadequate_housing_scale",
        ),
        HousingRightsEntity(
            entity_id="HR-006",
            name="Western Europe — Crise Logement Amsterdam/London/Paris, Airbnb Speculation & Familles Expulsées",
            country="Europe Occidentale",
            forced_eviction_displacement_severity_score=53.0,
            homelessness_inadequate_housing_scale_score=50.0,
            housing_discrimination_marginalized_score=51.0,
            rent_speculation_financialization_gap_score=49.0,
            primary_pattern="rent_speculation_financialization_gap",
        ),
        HousingRightsEntity(
            entity_id="HR-007",
            name="COHRE/HIC — Centre Droit Logement Expulsions, Plaidoyer Droit Logement & Standards PIDESC",
            country="Global",
            forced_eviction_displacement_severity_score=27.0,
            homelessness_inadequate_housing_scale_score=25.0,
            housing_discrimination_marginalized_score=26.0,
            rent_speculation_financialization_gap_score=24.0,
            primary_pattern="forced_eviction_displacement_severity",
        ),
        HousingRightsEntity(
            entity_id="HR-008",
            name="ONU/PIDESC — Article 11 Droit Logement Convenable, Rapporteur Logement & SDG 11.1",
            country="Global",
            forced_eviction_displacement_severity_score=4.0,
            homelessness_inadequate_housing_scale_score=4.0,
            housing_discrimination_marginalized_score=4.0,
            rent_speculation_financialization_gap_score=5.0,
            primary_pattern="rent_speculation_financialization_gap",
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

    return HousingRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_housing_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "cohre_forced_evictions_violations_human_rights_report",
            "un_habitat_world_cities_report_2022",
            "pidesc_committee_general_comment_4_adequate_housing",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_housing_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_housing_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
