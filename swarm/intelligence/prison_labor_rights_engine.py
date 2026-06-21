from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class PrisonLaborRightsEntity:
    entity_id: str
    name: str
    country: str
    forced_prison_labor_coercion_severity_score: float
    wage_theft_below_minimum_compensation_scale_score: float
    unsafe_working_conditions_incarcerated_score: float
    legal_protection_prisoner_worker_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_prison_labor_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.forced_prison_labor_coercion_severity_score * 0.30
            + self.wage_theft_below_minimum_compensation_scale_score * 0.25
            + self.unsafe_working_conditions_incarcerated_score * 0.25
            + self.legal_protection_prisoner_worker_gap_score * 0.20,
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
        self.estimated_prison_labor_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class PrisonLaborRightsEngineResult:
    agent: str = "Prison Labor Rights Engine Agent"
    domain: str = "prison_labor_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_prison_labor_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[PrisonLaborRightsEntity] = field(default_factory=list)

def run_prison_labor_rights_engine() -> PrisonLaborRightsEngineResult:
    entities = [
        PrisonLaborRightsEntity(
            entity_id="PLR-001",
            name="USA — 800 000 Détenus Forcés Travailler 0,13-0,52$/h, 13e Amendement Exception Esclavage & UNICOR Profit",
            country="États-Unis",
            forced_prison_labor_coercion_severity_score=96.0,
            wage_theft_below_minimum_compensation_scale_score=93.0,
            unsafe_working_conditions_incarcerated_score=91.0,
            legal_protection_prisoner_worker_gap_score=93.0,
            primary_pattern="forced_prison_labor_coercion_severity",
        ),
        PrisonLaborRightsEntity(
            entity_id="PLR-002",
            name="Chine — Laogai/Laojiao Travail Rééducatif, Camps Xinjiang Ouïghours & Production Exportation Forcée",
            country="Chine",
            forced_prison_labor_coercion_severity_score=94.0,
            wage_theft_below_minimum_compensation_scale_score=91.0,
            unsafe_working_conditions_incarcerated_score=90.0,
            legal_protection_prisoner_worker_gap_score=89.0,
            primary_pattern="forced_prison_labor_coercion_severity",
        ),
        PrisonLaborRightsEntity(
            entity_id="PLR-003",
            name="Russie — Colonies Pénitentiaires IK Travail Obligatoire, Zéro Salaire & Conditions Soviétiques Maintenues",
            country="Russie",
            forced_prison_labor_coercion_severity_score=91.0,
            wage_theft_below_minimum_compensation_scale_score=87.0,
            unsafe_working_conditions_incarcerated_score=87.0,
            legal_protection_prisoner_worker_gap_score=86.0,
            primary_pattern="wage_theft_below_minimum_compensation_scale",
        ),
        PrisonLaborRightsEntity(
            entity_id="PLR-004",
            name="Thaïlande/Asie SE — Détenus Loués Entreprises Privées, Usines Prison Sans EPI & Pas d'Assurance Travail",
            country="Thaïlande/Asie SE",
            forced_prison_labor_coercion_severity_score=89.0,
            wage_theft_below_minimum_compensation_scale_score=85.0,
            unsafe_working_conditions_incarcerated_score=85.0,
            legal_protection_prisoner_worker_gap_score=83.0,
            primary_pattern="unsafe_working_conditions_incarcerated",
        ),
        PrisonLaborRightsEntity(
            entity_id="PLR-005",
            name="Brésil — FUNAP Travail Pénitentiaire, Remise Peine vs Exploitation, Conditions Insalubres & Surpopulation",
            country="Brésil",
            forced_prison_labor_coercion_severity_score=56.0,
            wage_theft_below_minimum_compensation_scale_score=52.0,
            unsafe_working_conditions_incarcerated_score=53.0,
            legal_protection_prisoner_worker_gap_score=52.0,
            primary_pattern="forced_prison_labor_coercion_severity",
        ),
        PrisonLaborRightsEntity(
            entity_id="PLR-006",
            name="UE — Travail Pénitentiaire Légal Majorité États, Salaires 10-25% SMIC & Exclusion Droit Travail Commun",
            country="Union Européenne",
            forced_prison_labor_coercion_severity_score=54.0,
            wage_theft_below_minimum_compensation_scale_score=51.0,
            unsafe_working_conditions_incarcerated_score=51.0,
            legal_protection_prisoner_worker_gap_score=49.0,
            primary_pattern="legal_protection_prisoner_worker_gap",
        ),
        PrisonLaborRightsEntity(
            entity_id="PLR-007",
            name="PRI/Anti-Slavery Int'l — Standards Travail Pénitentiaire, Plaidoyer Salaire Minimum & Abolition Travail Forcé",
            country="Global",
            forced_prison_labor_coercion_severity_score=24.0,
            wage_theft_below_minimum_compensation_scale_score=28.0,
            unsafe_working_conditions_incarcerated_score=26.0,
            legal_protection_prisoner_worker_gap_score=26.0,
            primary_pattern="legal_protection_prisoner_worker_gap",
        ),
        PrisonLaborRightsEntity(
            entity_id="PLR-008",
            name="ONU/ILO — Convention C29 Travail Forcé, Protocole 2014 & Standards Minima Travail Pénitentiaire",
            country="Global",
            forced_prison_labor_coercion_severity_score=4.0,
            wage_theft_below_minimum_compensation_scale_score=5.0,
            unsafe_working_conditions_incarcerated_score=4.0,
            legal_protection_prisoner_worker_gap_score=5.0,
            primary_pattern="forced_prison_labor_coercion_severity",
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

    return PrisonLaborRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_prison_labor_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "aclu_captive_labor_exploitation_prison_workforce_report",
            "human_rights_watch_prison_labor_wages_conditions_report",
            "ilo_forced_labour_convention_c29_prison_labour_review",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_prison_labor_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_prison_labor_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
