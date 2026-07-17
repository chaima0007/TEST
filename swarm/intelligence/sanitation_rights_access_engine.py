from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class SanitationRightsAccessEntity:
    entity_id: str
    name: str
    country: str
    open_defecation_public_health_score: float
    menstrual_hygiene_management_denial_score: float
    water_sanitation_infrastructure_gap_score: float
    gender_disability_sanitation_exclusion_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_sanitation_rights_access_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.open_defecation_public_health_score * 0.30
            + self.menstrual_hygiene_management_denial_score * 0.25
            + self.water_sanitation_infrastructure_gap_score * 0.25
            + self.gender_disability_sanitation_exclusion_score * 0.20,
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
        self.estimated_sanitation_rights_access_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class SanitationRightsAccessEngineResult:
    agent: str = "Sanitation Rights Access Engine Agent"
    domain: str = "sanitation_rights_access"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_sanitation_rights_access_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[SanitationRightsAccessEntity] = field(default_factory=list)

def run_sanitation_rights_access_engine() -> SanitationRightsAccessEngineResult:
    entities = [
        SanitationRightsAccessEntity(
            entity_id="SA-001",
            name="Inde — 700M Sans Toilettes 2014, Violences Femmes Défécation Plein Air & Caste Exclusion",
            country="Asie du Sud",
            open_defecation_public_health_score=95.0,
            menstrual_hygiene_management_denial_score=92.0,
            water_sanitation_infrastructure_gap_score=92.0,
            gender_disability_sanitation_exclusion_score=92.0,
            primary_pattern="open_defecation_public_health",
        ),
        SanitationRightsAccessEntity(
            entity_id="SA-002",
            name="Niger/Tchad/Burkina — Sahel 80%+ Population Sans Assainissement Amélioré & COVID Amplification",
            country="Afrique de l'Ouest",
            open_defecation_public_health_score=92.0,
            menstrual_hygiene_management_denial_score=90.0,
            water_sanitation_infrastructure_gap_score=92.0,
            gender_disability_sanitation_exclusion_score=88.0,
            primary_pattern="water_sanitation_infrastructure_gap",
        ),
        SanitationRightsAccessEntity(
            entity_id="SA-003",
            name="Bangladesh — Bidonvilles Dhaka, 40% Latrines Partagées Insalubres & Inondations Contamination",
            country="Asie du Sud",
            open_defecation_public_health_score=88.0,
            menstrual_hygiene_management_denial_score=88.0,
            water_sanitation_infrastructure_gap_score=90.0,
            gender_disability_sanitation_exclusion_score=85.0,
            primary_pattern="water_sanitation_infrastructure_gap",
        ),
        SanitationRightsAccessEntity(
            entity_id="SA-004",
            name="Éthiopie — 40% Défécation Plein Air, Écoles Rurales Sans Toilettes Filles & Abandon Scolaire",
            country="Afrique de l'Est",
            open_defecation_public_health_score=85.0,
            menstrual_hygiene_management_denial_score=88.0,
            water_sanitation_infrastructure_gap_score=85.0,
            gender_disability_sanitation_exclusion_score=85.0,
            primary_pattern="menstrual_hygiene_management_denial",
        ),
        SanitationRightsAccessEntity(
            entity_id="SA-005",
            name="Philippines — Manille Bidonvilles, 30% Résidents Taudis, Choléra Endémique & Typhons",
            country="Asie du Sud-Est",
            open_defecation_public_health_score=55.0,
            menstrual_hygiene_management_denial_score=52.0,
            water_sanitation_infrastructure_gap_score=55.0,
            gender_disability_sanitation_exclusion_score=52.0,
            primary_pattern="open_defecation_public_health",
        ),
        SanitationRightsAccessEntity(
            entity_id="SA-006",
            name="Brésil — Favelas Non Raccordées, Nordeste Rural 40% Sans Assainissement & Racisme Environnemental",
            country="Amérique Latine",
            open_defecation_public_health_score=50.0,
            menstrual_hygiene_management_denial_score=48.0,
            water_sanitation_infrastructure_gap_score=52.0,
            gender_disability_sanitation_exclusion_score=50.0,
            primary_pattern="gender_disability_sanitation_exclusion",
        ),
        SanitationRightsAccessEntity(
            entity_id="SA-007",
            name="WaterAid/WASH — SDG 6 Monitoring, 2 Milliards Sans Assainissement Sécurisé & Rapport Global",
            country="Global",
            open_defecation_public_health_score=22.0,
            menstrual_hygiene_management_denial_score=28.0,
            water_sanitation_infrastructure_gap_score=25.0,
            gender_disability_sanitation_exclusion_score=30.0,
            primary_pattern="gender_disability_sanitation_exclusion",
        ),
        SanitationRightsAccessEntity(
            entity_id="SA-008",
            name="ONU/Résolution 64/292 — Droit à l'Eau & Assainissement 2010, Rapporteur Spécial WASH",
            country="Global",
            open_defecation_public_health_score=4.0,
            menstrual_hygiene_management_denial_score=5.0,
            water_sanitation_infrastructure_gap_score=3.0,
            gender_disability_sanitation_exclusion_score=6.0,
            primary_pattern="water_sanitation_infrastructure_gap",
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

    return SanitationRightsAccessEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_sanitation_rights_access_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "who_unicef_joint_monitoring_programme_water_sanitation_hygiene",
            "un_special_rapporteur_human_right_safe_drinking_water_sanitation",
            "wateraid_wash_global_progress_report_sdg6",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_sanitation_rights_access_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_sanitation_rights_access_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
