from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class EcoGriefRightsEntity:
    entity_id: str
    name: str
    country: str
    climate_displacement_trauma_severity_score: float
    ecological_loss_grief_recognition_gap_score: float
    mental_health_climate_support_absence_score: float
    indigenous_land_loss_cultural_trauma_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_eco_grief_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.climate_displacement_trauma_severity_score * 0.30
            + self.ecological_loss_grief_recognition_gap_score * 0.25
            + self.mental_health_climate_support_absence_score * 0.25
            + self.indigenous_land_loss_cultural_trauma_score * 0.20,
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
        self.estimated_eco_grief_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class EcoGriefRightsEngineResult:
    agent: str = "Eco Grief Rights Engine Agent"
    domain: str = "eco_grief_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.83
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_eco_grief_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[EcoGriefRightsEntity] = field(default_factory=list)

def run_eco_grief_rights_engine() -> EcoGriefRightsEngineResult:
    entities = [
        EcoGriefRightsEntity(
            entity_id="EGR-001",
            name="Kiribati/Tuvalu/Pacifique — Submersion Totale, Deuil Territoire & Zéro Soutien Psychologique",
            country="Océanie",
            climate_displacement_trauma_severity_score=95.0,
            ecological_loss_grief_recognition_gap_score=92.0,
            mental_health_climate_support_absence_score=95.0,
            indigenous_land_loss_cultural_trauma_score=92.0,
            primary_pattern="climate_displacement_trauma_severity",
        ),
        EcoGriefRightsEntity(
            entity_id="EGR-002",
            name="Bangladesh — 30M Déplacés Climatiques 2050, Trauma Terres Inondées & Zéro Cadre Légal",
            country="Asie du Sud",
            climate_displacement_trauma_severity_score=90.0,
            ecological_loss_grief_recognition_gap_score=92.0,
            mental_health_climate_support_absence_score=88.0,
            indigenous_land_loss_cultural_trauma_score=88.0,
            primary_pattern="ecological_loss_grief_recognition_gap",
        ),
        EcoGriefRightsEntity(
            entity_id="EGR-003",
            name="Australie/Bushfires — Solastalgie Documentée, Éco-Anxiété & Effondrement Grande Barrière Corail",
            country="Océanie",
            climate_displacement_trauma_severity_score=88.0,
            ecological_loss_grief_recognition_gap_score=88.0,
            mental_health_climate_support_absence_score=88.0,
            indigenous_land_loss_cultural_trauma_score=88.0,
            primary_pattern="mental_health_climate_support_absence",
        ),
        EcoGriefRightsEntity(
            entity_id="EGR-004",
            name="Peuples Autochtones Amazonie/Arctique — Déforestation, Fonte Glaces & Destruction Culture-Nature",
            country="Global",
            climate_displacement_trauma_severity_score=85.0,
            ecological_loss_grief_recognition_gap_score=88.0,
            mental_health_climate_support_absence_score=85.0,
            indigenous_land_loss_cultural_trauma_score=90.0,
            primary_pattern="indigenous_land_loss_cultural_trauma",
        ),
        EcoGriefRightsEntity(
            entity_id="EGR-005",
            name="Sahel/Afrique — Sécheresse Permanente, Éco-Chagrin Non Reconnu & Zéro Soutien Psychosocial",
            country="Afrique",
            climate_displacement_trauma_severity_score=55.0,
            ecological_loss_grief_recognition_gap_score=52.0,
            mental_health_climate_support_absence_score=55.0,
            indigenous_land_loss_cultural_trauma_score=50.0,
            primary_pattern="climate_displacement_trauma_severity",
        ),
        EcoGriefRightsEntity(
            entity_id="EGR-006",
            name="Europe/Jeunesse — Éco-Anxiété 68% Jeunes 16-25, Burnout Activistes & Manque Prise en Charge",
            country="Europe",
            climate_displacement_trauma_severity_score=50.0,
            ecological_loss_grief_recognition_gap_score=52.0,
            mental_health_climate_support_absence_score=52.0,
            indigenous_land_loss_cultural_trauma_score=50.0,
            primary_pattern="ecological_loss_grief_recognition_gap",
        ),
        EcoGriefRightsEntity(
            entity_id="EGR-007",
            name="APA/Lancet Countdown — Reconnaissance Éco-Anxiété, Protocoles Thérapie Climat & Plaidoyer",
            country="Global",
            climate_displacement_trauma_severity_score=22.0,
            ecological_loss_grief_recognition_gap_score=28.0,
            mental_health_climate_support_absence_score=25.0,
            indigenous_land_loss_cultural_trauma_score=30.0,
            primary_pattern="mental_health_climate_support_absence",
        ),
        EcoGriefRightsEntity(
            entity_id="EGR-008",
            name="ONU/OHCHR — Droit Environnement Sain Résolution 2021, SDG 13 Climat & Soutien Trauma",
            country="Global",
            climate_displacement_trauma_severity_score=4.0,
            ecological_loss_grief_recognition_gap_score=5.0,
            mental_health_climate_support_absence_score=3.0,
            indigenous_land_loss_cultural_trauma_score=6.0,
            primary_pattern="indigenous_land_loss_cultural_trauma",
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

    return EcoGriefRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_eco_grief_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "lancet_countdown_climate_change_mental_health_report_2023",
            "american_psychological_association_eco_anxiety_climate_distress_report",
            "unhcr_climate_displacement_psychological_trauma_global_review",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_eco_grief_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_eco_grief_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
