from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#be123c"


@dataclass
class HumanTraffickingRightsEntity:
    entity_id: str
    name: str
    country: str
    sex_trafficking_score: float
    labor_trafficking_score: float
    organ_trafficking_score: float
    victim_protection_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_human_trafficking_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.sex_trafficking_score * 0.30
            + self.labor_trafficking_score * 0.25
            + self.organ_trafficking_score * 0.25
            + self.victim_protection_gap_score * 0.20,
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
        self.estimated_human_trafficking_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class HumanTraffickingRightsEngineResult:
    agent: str = "HumanTraffickingRights Engine Agent"
    domain: str = "human_trafficking_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_human_trafficking_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[HumanTraffickingRightsEntity] = field(default_factory=list)


def run_human_trafficking_rights_engine() -> HumanTraffickingRightsEngineResult:
    entities = [
        # --- 4 CRITIQUE (>=60) ---
        HumanTraffickingRightsEntity(
            entity_id="HTR-001",
            name="Corée du Nord — Trafic femmes vers Chine & organ harvesting",
            country="Corée du Nord",
            sex_trafficking_score=98.0,
            labor_trafficking_score=95.0,
            organ_trafficking_score=96.0,
            victim_protection_gap_score=99.0,
            primary_pattern="State-sponsored trafficking & forced organ extraction",
        ),
        HumanTraffickingRightsEntity(
            entity_id="HTR-002",
            name="Syrie — Esclavage sexuel ISIS, trafic réfugiés",
            country="Syrie",
            sex_trafficking_score=92.0,
            labor_trafficking_score=85.0,
            organ_trafficking_score=78.0,
            victim_protection_gap_score=94.0,
            primary_pattern="Conflict-driven sexual slavery & refugee trafficking",
        ),
        HumanTraffickingRightsEntity(
            entity_id="HTR-003",
            name="Afghanistan — Bacha bazi, filles vendues, traite Iran",
            country="Afghanistan",
            sex_trafficking_score=86.0,
            labor_trafficking_score=80.0,
            organ_trafficking_score=70.0,
            victim_protection_gap_score=88.0,
            primary_pattern="Taliban-era child trafficking & forced marriage",
        ),
        HumanTraffickingRightsEntity(
            entity_id="HTR-004",
            name="Thaïlande — Hub traite Asie-Pacifique, tourisme sexuel",
            country="Thaïlande",
            sex_trafficking_score=82.0,
            labor_trafficking_score=80.0,
            organ_trafficking_score=65.0,
            victim_protection_gap_score=84.0,
            primary_pattern="Sex tourism hub & forced fishery labour",
        ),
        # --- 2 ÉLEVÉ (40-59) ---
        HumanTraffickingRightsEntity(
            entity_id="HTR-005",
            name="Mexique — Cartels, traite frontalière, 80k victimes/an",
            country="Mexique",
            sex_trafficking_score=58.0,
            labor_trafficking_score=55.0,
            organ_trafficking_score=48.0,
            victim_protection_gap_score=56.0,
            primary_pattern="Cartel-controlled border trafficking corridor",
        ),
        HumanTraffickingRightsEntity(
            entity_id="HTR-006",
            name="UE (Roumanie/Bulgarie) — 40% victimes traite identifiées en EU",
            country="Roumanie/Bulgarie",
            sex_trafficking_score=50.0,
            labor_trafficking_score=46.0,
            organ_trafficking_score=38.0,
            victim_protection_gap_score=48.0,
            primary_pattern="Intra-EU source countries, exploitation networks",
        ),
        # --- 1 MODÉRÉ (20-39) ---
        HumanTraffickingRightsEntity(
            entity_id="HTR-007",
            name="USA — Demande prostitution, trafficking interstate",
            country="États-Unis",
            sex_trafficking_score=34.0,
            labor_trafficking_score=28.0,
            organ_trafficking_score=18.0,
            victim_protection_gap_score=30.0,
            primary_pattern="Demand-side trafficking, Palermo Protocol ratified",
        ),
        # --- 1 FAIBLE (<20) ---
        HumanTraffickingRightsEntity(
            entity_id="HTR-008",
            name="Pays-Bas — Modèle nordique, criminalisation acheteurs",
            country="Pays-Bas",
            sex_trafficking_score=14.0,
            labor_trafficking_score=10.0,
            organ_trafficking_score=8.0,
            victim_protection_gap_score=12.0,
            primary_pattern="Nordic model buyer criminalisation, GRETA compliance",
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

    return HumanTraffickingRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_human_trafficking_rights_index=round(
            avg_composite / 100 * 10, 2
        ),
        data_sources=[
            "unodc_global_report_trafficking_persons_2024",
            "ilo_forced_labour_sexual_exploitation_2022",
            "us_department_state_tip_report_tier_rankings_2024",
            "ecpat_international_child_sexual_exploitation",
            "global_modern_slavery_index_walk_free_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_human_trafficking_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
