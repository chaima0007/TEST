from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class ClimateLitigationRightsEntity:
    entity_id: str
    name: str
    country: str
    environmental_right_recognition_score: float
    state_duty_climate_action_score: float
    corporate_climate_liability_score: float
    litigation_access_justice_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_climate_litigation_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.environmental_right_recognition_score * 0.30
            + self.state_duty_climate_action_score * 0.25
            + self.corporate_climate_liability_score * 0.25
            + self.litigation_access_justice_score * 0.20,
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
        self.estimated_climate_litigation_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class ClimateLitigationRightsEngineResult:
    agent: str = "Climate Litigation Rights Engine Agent"
    domain: str = "climate_litigation_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_climate_litigation_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ClimateLitigationRightsEntity] = field(default_factory=list)

def run_climate_litigation_rights_engine() -> ClimateLitigationRightsEngineResult:
    entities = [
        ClimateLitigationRightsEntity(
            entity_id="CL-001",
            name="Philippines — Commission Droits Humains, 50 Entreprises Fossiles & Premier Tribunal Climatique Mondial",
            country="Asie du Sud-Est",
            environmental_right_recognition_score=95.0,
            state_duty_climate_action_score=92.0,
            corporate_climate_liability_score=95.0,
            litigation_access_justice_score=90.0,
            primary_pattern="corporate_climate_liability",
        ),
        ClimateLitigationRightsEntity(
            entity_id="CL-002",
            name="Pays-Bas/Urgenda — Cour Suprême 2019, État Condamné -25% GES & Modèle Litige Climatique Global",
            country="Europe",
            environmental_right_recognition_score=92.0,
            state_duty_climate_action_score=95.0,
            corporate_climate_liability_score=88.0,
            litigation_access_justice_score=92.0,
            primary_pattern="state_duty_climate_action",
        ),
        ClimateLitigationRightsEntity(
            entity_id="CL-003",
            name="Shell/La Haye — Cour District 2021, -45% Émissions 2030 Scope3 & Responsabilité Corporative",
            country="Europe",
            environmental_right_recognition_score=88.0,
            state_duty_climate_action_score=85.0,
            corporate_climate_liability_score=92.0,
            litigation_access_justice_score=88.0,
            primary_pattern="corporate_climate_liability",
        ),
        ClimateLitigationRightsEntity(
            entity_id="CL-004",
            name="Colombie — Cour Suprême Amazonie 2018, Droits Générations Futures & Déforestation Systémique",
            country="Amérique Latine",
            environmental_right_recognition_score=88.0,
            state_duty_climate_action_score=85.0,
            corporate_climate_liability_score=82.0,
            litigation_access_justice_score=88.0,
            primary_pattern="environmental_right_recognition",
        ),
        ClimateLitigationRightsEntity(
            entity_id="CL-005",
            name="Torres Strait/ONU — Peuples Autochtones Australie, CCPR Violations & Inaction État Condamnée",
            country="Océanie",
            environmental_right_recognition_score=55.0,
            state_duty_climate_action_score=55.0,
            corporate_climate_liability_score=50.0,
            litigation_access_justice_score=55.0,
            primary_pattern="litigation_access_justice",
        ),
        ClimateLitigationRightsEntity(
            entity_id="CL-006",
            name="CEDH/Duarte Agostinho — Portugal & 32 États, Jeunes Requérants & Inaction Climatique Europe",
            country="Europe",
            environmental_right_recognition_score=50.0,
            state_duty_climate_action_score=52.0,
            corporate_climate_liability_score=48.0,
            litigation_access_justice_score=48.0,
            primary_pattern="state_duty_climate_action",
        ),
        ClimateLitigationRightsEntity(
            entity_id="CL-007",
            name="Sabin Center/ClientEarth — 2000+ Cas Répertoriés, Base Données Mondiale & Stratégie Litige",
            country="Global",
            environmental_right_recognition_score=22.0,
            state_duty_climate_action_score=28.0,
            corporate_climate_liability_score=25.0,
            litigation_access_justice_score=30.0,
            primary_pattern="litigation_access_justice",
        ),
        ClimateLitigationRightsEntity(
            entity_id="CL-008",
            name="ONU/HRC Res.48/13 — Droit Environnement Sain Reconnu 2021 & Rapporteur Spécial Nommé",
            country="Global",
            environmental_right_recognition_score=4.0,
            state_duty_climate_action_score=5.0,
            corporate_climate_liability_score=3.0,
            litigation_access_justice_score=6.0,
            primary_pattern="environmental_right_recognition",
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

    return ClimateLitigationRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_climate_litigation_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "sabin_center_climate_change_litigation_database",
            "un_hrc_resolution_48_13_right_healthy_environment",
            "clientearth_strategic_climate_litigation_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_climate_litigation_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_climate_litigation_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
