from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class PrisonHealthcareDenialEntity:
    entity_id: str
    name: str
    country: str
    medical_care_denial_scale_score: float
    mental_health_neglect_score: float
    infectious_disease_spread_score: float
    torture_medical_complicity_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_prison_healthcare_denial_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.medical_care_denial_scale_score * 0.30
            + self.mental_health_neglect_score * 0.25
            + self.infectious_disease_spread_score * 0.25
            + self.torture_medical_complicity_score * 0.20,
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
        self.estimated_prison_healthcare_denial_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class PrisonHealthcareDenialEngineResult:
    agent: str = "Prison Healthcare Denial Engine Agent"
    domain: str = "prison_healthcare_denial"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_prison_healthcare_denial_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[PrisonHealthcareDenialEntity] = field(default_factory=list)

def run_prison_healthcare_denial_engine() -> PrisonHealthcareDenialEngineResult:
    entities = [
        PrisonHealthcareDenialEntity(
            entity_id="PH-001",
            name="USA — 2.2M Détenus, HCV 17x Pop. Générale, COVID Prison 3x & For-Profit Healthcare Denial",
            country="Amérique du Nord",
            medical_care_denial_scale_score=95.0,
            mental_health_neglect_score=92.0,
            infectious_disease_spread_score=95.0,
            torture_medical_complicity_score=88.0,
            primary_pattern="infectious_disease_spread",
        ),
        PrisonHealthcareDenialEntity(
            entity_id="PH-002",
            name="Brésil — 900K Détenus, TB 35x Pop. Générale, Surpopulation 170% & HCV Non Traité",
            country="Amérique Latine",
            medical_care_denial_scale_score=90.0,
            mental_health_neglect_score=88.0,
            infectious_disease_spread_score=92.0,
            torture_medical_complicity_score=88.0,
            primary_pattern="infectious_disease_spread",
        ),
        PrisonHealthcareDenialEntity(
            entity_id="PH-003",
            name="Russie — TB-MR Pénitentiaire, Psychiatrie Punitive Opposants & CEDH Condamnations Soins",
            country="Europe de l'Est",
            medical_care_denial_scale_score=88.0,
            mental_health_neglect_score=92.0,
            infectious_disease_spread_score=88.0,
            torture_medical_complicity_score=90.0,
            primary_pattern="torture_medical_complicity",
        ),
        PrisonHealthcareDenialEntity(
            entity_id="PH-004",
            name="Philippines — Drug War 800% Surpopulation, Maladies Infectieuses, Torture & Soins Absents",
            country="Asie du Sud-Est",
            medical_care_denial_scale_score=85.0,
            mental_health_neglect_score=85.0,
            infectious_disease_spread_score=88.0,
            torture_medical_complicity_score=88.0,
            primary_pattern="medical_care_denial_scale",
        ),
        PrisonHealthcareDenialEntity(
            entity_id="PH-005",
            name="Mexique — Prisons Rurales Sans Médecin, Surpopulation 200%+ & Malnutrition Systémique",
            country="Amérique Latine",
            medical_care_denial_scale_score=55.0,
            mental_health_neglect_score=52.0,
            infectious_disease_spread_score=55.0,
            torture_medical_complicity_score=52.0,
            primary_pattern="medical_care_denial_scale",
        ),
        PrisonHealthcareDenialEntity(
            entity_id="PH-006",
            name="France — Suicide Prison 10x Pop. Générale, Santé Mentale Défaillante & CGLPL Alertes",
            country="Europe",
            medical_care_denial_scale_score=50.0,
            mental_health_neglect_score=55.0,
            infectious_disease_spread_score=48.0,
            torture_medical_complicity_score=48.0,
            primary_pattern="mental_health_neglect",
        ),
        PrisonHealthcareDenialEntity(
            entity_id="PH-007",
            name="PRI/Penal Reform — Standards Mandela Règles 24-35, Monitoring Soins Médicaux & Plaidoyer",
            country="Global",
            medical_care_denial_scale_score=22.0,
            mental_health_neglect_score=28.0,
            infectious_disease_spread_score=25.0,
            torture_medical_complicity_score=30.0,
            primary_pattern="mental_health_neglect",
        ),
        PrisonHealthcareDenialEntity(
            entity_id="PH-008",
            name="ONU/Règles Nelson Mandela — Règles 24-35 Soins Médicaux & Convention Torture Art.16",
            country="Global",
            medical_care_denial_scale_score=4.0,
            mental_health_neglect_score=5.0,
            infectious_disease_spread_score=3.0,
            torture_medical_complicity_score=6.0,
            primary_pattern="torture_medical_complicity",
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

    return PrisonHealthcareDenialEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_prison_healthcare_denial_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "penal_reform_international_prison_health_standards_mandela_rules",
            "who_prison_health_infectious_disease_tuberculosis_hiv_report",
            "hrw_sick_unable_to_get_care_prison_healthcare_denial_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_prison_healthcare_denial_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_prison_healthcare_denial_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
