from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#dc2626"


@dataclass
class ForcedLaborRightsEntity:
    entity_id: str
    name: str
    country: str
    forced_labor_prevalence_score: float
    debt_bondage_score: float
    trafficking_exploitation_score: float
    corporate_supply_chain_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_forced_labor_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.forced_labor_prevalence_score * 0.30
            + self.debt_bondage_score * 0.25
            + self.trafficking_exploitation_score * 0.25
            + self.corporate_supply_chain_score * 0.20,
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
        self.estimated_forced_labor_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class ForcedLaborRightsEngineResult:
    agent: str = "ForcedLaborRights Engine Agent"
    domain: str = "forced_labor_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_forced_labor_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ForcedLaborRightsEntity] = field(default_factory=list)


def run_forced_labor_rights_engine() -> ForcedLaborRightsEngineResult:
    entities = [
        ForcedLaborRightsEntity(
            entity_id="FLR-001",
            name="Corée du Nord — Export main-d'oeuvre forcée",
            country="Corée du Nord",
            forced_labor_prevalence_score=97,
            debt_bondage_score=95,
            trafficking_exploitation_score=96,
            corporate_supply_chain_score=94,
            primary_pattern="Travail forcé d'État systématique & export de main-d'oeuvre",
        ),
        ForcedLaborRightsEntity(
            entity_id="FLR-002",
            name="Érythrée — Service national indéfini",
            country="Érythrée",
            forced_labor_prevalence_score=91,
            debt_bondage_score=90,
            trafficking_exploitation_score=88,
            corporate_supply_chain_score=89,
            primary_pattern="Esclavage d'État par conscription forcée indéfinie",
        ),
        ForcedLaborRightsEntity(
            entity_id="FLR-003",
            name="Myanmar — Tatmadaw travail forcé post-coup",
            country="Myanmar",
            forced_labor_prevalence_score=85,
            debt_bondage_score=83,
            trafficking_exploitation_score=86,
            corporate_supply_chain_score=84,
            primary_pattern="Travail forcé militaire & exploitation minière enfants",
        ),
        ForcedLaborRightsEntity(
            entity_id="FLR-004",
            name="Qatar — Système kafala & morts Coupe du Monde",
            country="Qatar",
            forced_labor_prevalence_score=79,
            debt_bondage_score=77,
            trafficking_exploitation_score=78,
            corporate_supply_chain_score=76,
            primary_pattern="Servitude migrant kafala & dette recrutement",
        ),
        ForcedLaborRightsEntity(
            entity_id="FLR-005",
            name="Inde — Bonded laborers BLN & travail enfants",
            country="Inde",
            forced_labor_prevalence_score=56,
            debt_bondage_score=54,
            trafficking_exploitation_score=55,
            corporate_supply_chain_score=53,
            primary_pattern="8 millions bonded laborers agriculture/briques/tapis",
        ),
        ForcedLaborRightsEntity(
            entity_id="FLR-006",
            name="Brésil — Escravidão contemporânea",
            country="Brésil",
            forced_labor_prevalence_score=47,
            debt_bondage_score=46,
            trafficking_exploitation_score=48,
            corporate_supply_chain_score=45,
            primary_pattern="2 000+ libérations annuelles agriculture & textile",
        ),
        ForcedLaborRightsEntity(
            entity_id="FLR-007",
            name="États-Unis — Prison labor & immigration detention",
            country="États-Unis",
            forced_labor_prevalence_score=33,
            debt_bondage_score=31,
            trafficking_exploitation_score=32,
            corporate_supply_chain_score=30,
            primary_pattern="1,5M détenus travail <$1/h & détention immigration",
        ),
        ForcedLaborRightsEntity(
            entity_id="FLR-008",
            name="OIT/OCDE — Cadre normatif international",
            country="International",
            forced_labor_prevalence_score=12,
            debt_bondage_score=11,
            trafficking_exploitation_score=10,
            corporate_supply_chain_score=13,
            primary_pattern="Conventions 29/105 ratifiées & CSDDD 2024 due diligence",
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

    return ForcedLaborRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_forced_labor_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ilo_global_estimates_modern_slavery_2022",
            "walk_free_foundation_global_slavery_index_2023",
            "us_department_state_trafficking_persons_report_2024",
            "business_human_rights_resource_center_supply_chains",
            "hrw_forced_labor_documentation_global",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_forced_labor_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_forced_labor_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
