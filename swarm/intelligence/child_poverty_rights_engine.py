from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#1a0f06"
PREFIX = "CPR"
DOMAIN = "child_poverty_rights"


@dataclass
class ChildPovertyRightsEntity:
    entity_id: str
    name: str
    country: str
    malnutrition_stunting_score: float
    education_deprivation_score: float
    child_labor_exploitation_score: float
    social_protection_absence_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_child_poverty_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.malnutrition_stunting_score * 0.30
            + self.education_deprivation_score * 0.25
            + self.child_labor_exploitation_score * 0.25
            + self.social_protection_absence_score * 0.20,
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
        self.estimated_child_poverty_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class ChildPovertyRightsEngineResult:
    agent: str = "Child Poverty Rights Engine Agent"
    domain: str = DOMAIN
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_child_poverty_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ChildPovertyRightsEntity] = field(default_factory=list)


def run_child_poverty_rights_engine() -> ChildPovertyRightsEngineResult:
    entities = [
        ChildPovertyRightsEntity(
            entity_id="CPR-001",
            name="Somalia — 1.8M Enfants Risque Famine Aiguë, Malnutrition Sévère Systémique, Effondrement Système Protection & Conflit Armé Accélérateur",
            country="Somalia",
            malnutrition_stunting_score=90.0,
            education_deprivation_score=88.0,
            child_labor_exploitation_score=87.0,
            social_protection_absence_score=82.0,
            primary_pattern="malnutrition_stunting",
        ),
        ChildPovertyRightsEntity(
            entity_id="CPR-002",
            name="CAR Centrafrique — 73% Enfants Pauvreté Extrême, Éducation Totalement Effondrée, Travail Enfants Généralisé & Groupes Armés Recruteurs",
            country="CAR",
            malnutrition_stunting_score=87.0,
            education_deprivation_score=85.0,
            child_labor_exploitation_score=84.0,
            social_protection_absence_score=79.0,
            primary_pattern="education_deprivation",
        ),
        ChildPovertyRightsEntity(
            entity_id="CPR-003",
            name="Madagascar — 77% Enfants Pauvreté Chronique, Retard Croissance 49% Enfants Moins 5 Ans, Travail Enfants Agriculture & Cyclones Aggravants",
            country="Madagascar",
            malnutrition_stunting_score=84.0,
            education_deprivation_score=82.0,
            child_labor_exploitation_score=81.0,
            social_protection_absence_score=76.0,
            primary_pattern="malnutrition_stunting",
        ),
        ChildPovertyRightsEntity(
            entity_id="CPR-004",
            name="Nigeria Northern States — 10.5M Enfants Non-Scolarisés Kano/Sokoto/Zamfara, Malnutrition Chronique Sahel, Almajiri Système & Boko Haram Enlèvements",
            country="Nigeria",
            malnutrition_stunting_score=81.0,
            education_deprivation_score=79.0,
            child_labor_exploitation_score=78.0,
            social_protection_absence_score=73.0,
            primary_pattern="education_deprivation",
        ),
        ChildPovertyRightsEntity(
            entity_id="CPR-005",
            name="India Bihar/Uttar Pradesh — Travail Enfants Mines Mica/Briques Fours, Malnutrition 35% Enfants, Travaux Domestiques Filles & Mariages Précoces",
            country="India",
            malnutrition_stunting_score=60.0,
            education_deprivation_score=58.0,
            child_labor_exploitation_score=57.0,
            social_protection_absence_score=52.0,
            primary_pattern="child_labor_exploitation",
        ),
        ChildPovertyRightsEntity(
            entity_id="CPR-006",
            name="Brazil Favelas — 40% Enfants Pauvreté Relative, Accès Santé/Éducation Inégal, Recrutement Gangs Mineurs & Violence Structurelle Milícias",
            country="Brazil",
            malnutrition_stunting_score=57.0,
            education_deprivation_score=55.0,
            child_labor_exploitation_score=54.0,
            social_protection_absence_score=49.0,
            primary_pattern="social_protection_absence",
        ),
        ChildPovertyRightsEntity(
            entity_id="CPR-007",
            name="USA Child Poverty — 12M Enfants Sous Seuil Pauvreté, Lacunes Food Stamps SNAP, Inégalités Raciales Persistantes & Sans-Abri Familles En Hausse",
            country="USA",
            malnutrition_stunting_score=35.0,
            education_deprivation_score=33.0,
            child_labor_exploitation_score=32.0,
            social_protection_absence_score=27.0,
            primary_pattern="social_protection_absence",
        ),
        ChildPovertyRightsEntity(
            entity_id="CPR-008",
            name="Nordic Countries — Filet Social Enfants Universel, Taux Pauvreté Enfants Moins 3%, Allocation Familiale Universelle & Meilleure Pratique Mondiale UNICEF",
            country="Nordic",
            malnutrition_stunting_score=17.0,
            education_deprivation_score=15.0,
            child_labor_exploitation_score=14.0,
            social_protection_absence_score=9.0,
            primary_pattern="malnutrition_stunting",
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

    return ChildPovertyRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_child_poverty_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unicef_state_worlds_children_2025",
            "world_bank_child_poverty_global_database",
            "ilo_child_labour_global_estimates_2022",
            "save_the_children_global_childhood_report_2025",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_child_poverty_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_child_poverty_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
