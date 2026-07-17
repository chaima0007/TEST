from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class HousingEvictionDisplacementRightsEntity:
    entity_id: str
    name: str
    country: str
    forced_eviction_land_grabbing_severity_score: float
    homelessness_inadequate_housing_scale_score: float
    discriminatory_housing_segregation_score: float
    housing_affordability_social_protection_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_housing_eviction_displacement_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.forced_eviction_land_grabbing_severity_score * 0.30
            + self.homelessness_inadequate_housing_scale_score * 0.25
            + self.discriminatory_housing_segregation_score * 0.25
            + self.housing_affordability_social_protection_deficit_gap_score * 0.20,
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
        self.estimated_housing_eviction_displacement_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class HousingEvictionDisplacementRightsEngineResult:
    agent: str = "Housing Eviction Displacement Rights Engine Agent"
    domain: str = "housing_eviction_displacement_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_housing_eviction_displacement_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[HousingEvictionDisplacementRightsEntity] = field(default_factory=list)

def run_housing_eviction_displacement_rights_engine() -> HousingEvictionDisplacementRightsEngineResult:
    entities = [
        HousingEvictionDisplacementRightsEntity(
            entity_id="HEDR-001",
            name="Chine/Urbanisation Forcée — 250M Ruraux Déplacés, Expulsions Sans Compensation & Hukou Discrimination",
            country="Asie du Nord-Est",
            forced_eviction_land_grabbing_severity_score=92.0,
            homelessness_inadequate_housing_scale_score=88.0,
            discriminatory_housing_segregation_score=90.0,
            housing_affordability_social_protection_deficit_gap_score=85.0,
            primary_pattern="forced_eviction_land_grabbing_severity",
        ),
        HousingEvictionDisplacementRightsEntity(
            entity_id="HEDR-002",
            name="Éthiopie/Tigré — Déplacements Massifs Conflits, Villages Brûlés & 2M Déplacés Internes",
            country="Afrique de l'Est",
            forced_eviction_land_grabbing_severity_score=95.0,
            homelessness_inadequate_housing_scale_score=92.0,
            discriminatory_housing_segregation_score=88.0,
            housing_affordability_social_protection_deficit_gap_score=90.0,
            primary_pattern="forced_eviction_land_grabbing_severity",
        ),
        HousingEvictionDisplacementRightsEntity(
            entity_id="HEDR-003",
            name="Inde/Adivasis — Expulsions Projets Barrages & Mines, 50M Déplacés Développement Sans Réinstallation",
            country="Asie du Sud",
            forced_eviction_land_grabbing_severity_score=88.0,
            homelessness_inadequate_housing_scale_score=85.0,
            discriminatory_housing_segregation_score=92.0,
            housing_affordability_social_protection_deficit_gap_score=88.0,
            primary_pattern="discriminatory_housing_segregation",
        ),
        HousingEvictionDisplacementRightsEntity(
            entity_id="HEDR-004",
            name="Zimbabwe/Opération Murambatsvina — 700k Expulsés 2005, Bidonvilles Démolis & Sans-Abrisme Massif",
            country="Afrique Australe",
            forced_eviction_land_grabbing_severity_score=85.0,
            homelessness_inadequate_housing_scale_score=90.0,
            discriminatory_housing_segregation_score=85.0,
            housing_affordability_social_protection_deficit_gap_score=92.0,
            primary_pattern="housing_affordability_social_protection_deficit_gap",
        ),
        HousingEvictionDisplacementRightsEntity(
            entity_id="HEDR-005",
            name="USA/Crise Logement Abordable — 600k SDF, Expulsions Moratoriums Levés & Gentrification Communautés",
            country="Amérique du Nord",
            forced_eviction_land_grabbing_severity_score=52.0,
            homelessness_inadequate_housing_scale_score=60.0,
            discriminatory_housing_segregation_score=55.0,
            housing_affordability_social_protection_deficit_gap_score=58.0,
            primary_pattern="homelessness_inadequate_housing_scale",
        ),
        HousingEvictionDisplacementRightsEntity(
            entity_id="HEDR-006",
            name="Brésil/Favelas JO — Expulsions Rio & São Paulo, Gentrification Événements Sportifs & Déficit Logement",
            country="Amérique Latine",
            forced_eviction_land_grabbing_severity_score=55.0,
            homelessness_inadequate_housing_scale_score=52.0,
            discriminatory_housing_segregation_score=58.0,
            housing_affordability_social_protection_deficit_gap_score=50.0,
            primary_pattern="discriminatory_housing_segregation",
        ),
        HousingEvictionDisplacementRightsEntity(
            entity_id="HEDR-007",
            name="HIC/COHRE Habitat International Coalition — Documentation Expulsions Forcées & Plaidoyer Droit Logement",
            country="Global",
            forced_eviction_land_grabbing_severity_score=22.0,
            homelessness_inadequate_housing_scale_score=26.0,
            discriminatory_housing_segregation_score=24.0,
            housing_affordability_social_protection_deficit_gap_score=28.0,
            primary_pattern="housing_affordability_social_protection_deficit_gap",
        ),
        HousingEvictionDisplacementRightsEntity(
            entity_id="HEDR-008",
            name="ONU/PIDESC Art.11 — Droit Logement Adéquat, Rapporteur Spécial & Principes Directeurs Expulsions",
            country="Global",
            forced_eviction_land_grabbing_severity_score=5.0,
            homelessness_inadequate_housing_scale_score=6.0,
            discriminatory_housing_segregation_score=4.0,
            housing_affordability_social_protection_deficit_gap_score=8.0,
            primary_pattern="forced_eviction_land_grabbing_severity",
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

    return HousingEvictionDisplacementRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_housing_eviction_displacement_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_special_rapporteur_adequate_housing_forced_evictions_annual_report",
            "cohre_centre_housing_rights_evictions_global_survey_forced_evictions",
            "un_pidesc_general_comment_4_right_adequate_housing_implementation_guide",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_housing_eviction_displacement_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_housing_eviction_displacement_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
