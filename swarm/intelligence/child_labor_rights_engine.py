from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#d97706"


@dataclass
class ChildLaborRightsEntity:
    entity_id: str
    name: str
    country: str
    worst_forms_child_labor_score: float
    hazardous_work_exposure_score: float
    school_exclusion_score: float
    child_labor_supply_chain_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_child_labor_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.worst_forms_child_labor_score * 0.30
            + self.hazardous_work_exposure_score * 0.25
            + self.school_exclusion_score * 0.25
            + self.child_labor_supply_chain_score * 0.20,
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
        self.estimated_child_labor_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class ChildLaborRightsEngineResult:
    agent: str = "Child Labor Rights Engine Agent"
    domain: str = "child_labor_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_child_labor_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ChildLaborRightsEntity] = field(default_factory=list)


def run_child_labor_rights_engine() -> ChildLaborRightsEngineResult:
    entities = [
        ChildLaborRightsEntity(
            entity_id="CLR-001",
            name="Mali — Enfants Mines Or Artisanales, Travail Forcé Conflits Armés & Déscolarisation 60%",
            country="Mali",
            worst_forms_child_labor_score=96.0,
            hazardous_work_exposure_score=94.0,
            school_exclusion_score=93.0,
            child_labor_supply_chain_score=92.0,
            primary_pattern="worst_forms_child_labor_score",
        ),
        ChildLaborRightsEntity(
            entity_id="CLR-002",
            name="RD Congo — Enfants Mines Cobalt Katanga, Travail Danger Chaîne Apple/Tesla & Impunité Totale",
            country="RD Congo",
            worst_forms_child_labor_score=95.0,
            hazardous_work_exposure_score=96.0,
            school_exclusion_score=91.0,
            child_labor_supply_chain_score=94.0,
            primary_pattern="hazardous_work_exposure_score",
        ),
        ChildLaborRightsEntity(
            entity_id="CLR-003",
            name="Myanmar — Enfants Soldats Tatmadaw, Conscription Forcée Post-Coup 2021 & Travail Plantations",
            country="Myanmar",
            worst_forms_child_labor_score=94.0,
            hazardous_work_exposure_score=90.0,
            school_exclusion_score=92.0,
            child_labor_supply_chain_score=89.0,
            primary_pattern="worst_forms_child_labor_score",
        ),
        ChildLaborRightsEntity(
            entity_id="CLR-004",
            name="Bangladesh — Ateliers Textile, 5% Enfants Industrie Vêtement & Accidents Rana Plaza Récurrents",
            country="Bangladesh",
            worst_forms_child_labor_score=88.0,
            hazardous_work_exposure_score=87.0,
            school_exclusion_score=82.0,
            child_labor_supply_chain_score=90.0,
            primary_pattern="child_labor_supply_chain_score",
        ),
        ChildLaborRightsEntity(
            entity_id="CLR-005",
            name="Brésil — Travail Enfants Agriculture Canne à Sucre/Café, Zone Rurale & Lacunes Inspection",
            country="Brésil",
            worst_forms_child_labor_score=52.0,
            hazardous_work_exposure_score=55.0,
            school_exclusion_score=48.0,
            child_labor_supply_chain_score=50.0,
            primary_pattern="hazardous_work_exposure_score",
        ),
        ChildLaborRightsEntity(
            entity_id="CLR-006",
            name="Inde — Enfants Industrie Tapis/Briques, 4,5 Millions Travailleurs & Faible Application Loi",
            country="Inde",
            worst_forms_child_labor_score=47.0,
            hazardous_work_exposure_score=49.0,
            school_exclusion_score=44.0,
            child_labor_supply_chain_score=46.0,
            primary_pattern="hazardous_work_exposure_score",
        ),
        ChildLaborRightsEntity(
            entity_id="CLR-007",
            name="Pérou — Travail Informel Enfants Marchés Andins, Lacunes Scolarisation Zones Rurales",
            country="Pérou",
            worst_forms_child_labor_score=30.0,
            hazardous_work_exposure_score=28.0,
            school_exclusion_score=32.0,
            child_labor_supply_chain_score=27.0,
            primary_pattern="school_exclusion_score",
        ),
        ChildLaborRightsEntity(
            entity_id="CLR-008",
            name="Finlande — Zéro Travail Enfants, Scolarité Obligatoire 18 Ans & Contrôles Chaînes Approvisionnement",
            country="Finlande",
            worst_forms_child_labor_score=11.0,
            hazardous_work_exposure_score=10.0,
            school_exclusion_score=9.0,
            child_labor_supply_chain_score=12.0,
            primary_pattern="child_labor_supply_chain_score",
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

    return ChildLaborRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_child_labor_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ilo_global_estimates_child_labour_2022",
            "unicef_child_labour_statistics_2024",
            "hrw_child_labour_global_documentation",
            "ilo_ipec_worst_forms_child_labour_report",
            "un_crc_committee_concluding_observations",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_child_labor_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
