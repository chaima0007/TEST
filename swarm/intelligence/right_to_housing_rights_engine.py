from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#16a34a"


@dataclass
class RightToHousingRightsEntity:
    entity_id: str
    name: str
    country: str
    forced_eviction_score: float
    homelessness_criminalization_score: float
    housing_affordability_crisis_score: float
    indigenous_land_displacement_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_right_to_housing_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.forced_eviction_score * 0.30
            + self.homelessness_criminalization_score * 0.25
            + self.housing_affordability_crisis_score * 0.25
            + self.indigenous_land_displacement_score * 0.20,
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
        self.estimated_right_to_housing_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class RightToHousingRightsEngineResult:
    agent: str = "Right To Housing Rights Engine Agent"
    domain: str = "right_to_housing_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_right_to_housing_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[RightToHousingRightsEntity] = field(default_factory=list)


def run_right_to_housing_rights_engine() -> RightToHousingRightsEngineResult:
    entities = [
        RightToHousingRightsEntity(
            entity_id="RTH-001",
            name="Cambodge — Boeung Kak Lake Expulsions, 10 000 Familles Sans Recours, PM Hun Sen",
            country="Cambodge",
            forced_eviction_score=96.0,
            homelessness_criminalization_score=94.0,
            housing_affordability_crisis_score=93.0,
            indigenous_land_displacement_score=95.0,
            primary_pattern="forced_eviction",
        ),
        RightToHousingRightsEntity(
            entity_id="RTH-002",
            name="Soudan du Sud — Déplacements Guerre, 2M de Personnes Sans Abri, IDP Camps",
            country="Soudan du Sud",
            forced_eviction_score=90.0,
            homelessness_criminalization_score=88.0,
            housing_affordability_crisis_score=92.0,
            indigenous_land_displacement_score=87.0,
            primary_pattern="conflict_displacement",
        ),
        RightToHousingRightsEntity(
            entity_id="RTH-003",
            name="Brésil Favelas — Opérations Militaires Rio, Démolitions Copa/JO Sans Relogement",
            country="Brésil",
            forced_eviction_score=84.0,
            homelessness_criminalization_score=82.0,
            housing_affordability_crisis_score=85.0,
            indigenous_land_displacement_score=80.0,
            primary_pattern="forced_eviction",
        ),
        RightToHousingRightsEntity(
            entity_id="RTH-004",
            name="Inde — Mumbai Slums, 1M Expulsés Dharavi, Dalits Sans Titre Foncier",
            country="Inde",
            forced_eviction_score=76.0,
            homelessness_criminalization_score=74.0,
            housing_affordability_crisis_score=78.0,
            indigenous_land_displacement_score=72.0,
            primary_pattern="indigenous_land_displacement",
        ),
        RightToHousingRightsEntity(
            entity_id="RTH-005",
            name="USA — 650 000 Sans-Abri, Lois Anti-Camping 187 Villes, Criminalisation SDF",
            country="USA",
            forced_eviction_score=54.0,
            homelessness_criminalization_score=58.0,
            housing_affordability_crisis_score=56.0,
            indigenous_land_displacement_score=50.0,
            primary_pattern="homelessness_criminalization",
        ),
        RightToHousingRightsEntity(
            entity_id="RTH-006",
            name="UK — Section 21 Expulsions, Crise Location, 300 000 Sans-Abri Estimation",
            country="UK",
            forced_eviction_score=52.0,
            homelessness_criminalization_score=50.0,
            housing_affordability_crisis_score=56.0,
            indigenous_land_displacement_score=48.0,
            primary_pattern="housing_affordability_crisis",
        ),
        RightToHousingRightsEntity(
            entity_id="RTH-007",
            name="France — Droit Opposable Logement (DALO) Insuffisant, 4M Mal-Logés",
            country="France",
            forced_eviction_score=26.0,
            homelessness_criminalization_score=28.0,
            housing_affordability_crisis_score=30.0,
            indigenous_land_displacement_score=22.0,
            primary_pattern="housing_affordability_crisis",
        ),
        RightToHousingRightsEntity(
            entity_id="RTH-008",
            name="Finlande/Autriche — Housing First Modèle, SDF Quasi-Éliminés, Droit Constitutionnel",
            country="Finlande/Autriche",
            forced_eviction_score=7.0,
            homelessness_criminalization_score=6.0,
            housing_affordability_crisis_score=8.0,
            indigenous_land_displacement_score=5.0,
            primary_pattern="forced_eviction",
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

    return RightToHousingRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_right_to_housing_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_special_rapporteur_adequate_housing_2024",
            "cohre_forced_evictions_global_database",
            "hrw_evictions_displacement_report_2024",
            "habitat_international_coalition_reports",
            "un_habitat_world_cities_report_2024",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_right_to_housing_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
